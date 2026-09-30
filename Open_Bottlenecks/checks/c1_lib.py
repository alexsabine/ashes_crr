"""OB1-C1 harness (Open_Bottlenecks/C1_DECLARATION.md, pushed at 39e86ce before this file): Adam with per-step moment decay on
SEC1's MLP, the arms STEP, ARC, SHUF, KOURK, MECTA-M, ALIGN, ORACLE, the streams S1 (class-IL), S2 (domain-IL, rotations),
S0 (no switch), and the stability-gap metric.

CHOICES (printed by the gate script):
  - ARC's arc a_t is the arc of the update just applied (before -> after), on the previous and current batch; it sets the
    decay of the NEXT step (the arc of a step is known only after it).
  - KOURK uses the CURRENT step's gradient norm (its native timing; one step earlier than ARC; the stronger baseline).
  - MECTA-M's D_t is the mean over hidden units of the symmetric KL between diagonal Gaussians (batch vs running), variance
    floor 1e-6; beta_eff = min(beta, exp(-D_t)).
  - Every running mean (abar, gbar, MECTA-M's statistics) starts at its first value and updates at rho = 0.01.
  - Bias correction uses the running products of the effective betas; a reset (ALIGN's first moment, ORACLE's both) restarts
    the corresponding product at 1.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Replay_Quality_Memory" / "checks"))
import rqm_lib as R  # noqa: E402

S = R.S
LR = 1e-3; B1 = 0.9; B2 = 0.999; EPS = 1e-8; BS = 10; EPOCHS = 3; HID = 256
RHO = 0.01; R_MAX = 20.0; SG_WINDOW = 30
ARMS = ("STEP", "ARC", "SHUF", "KOURK", "MECTA-M", "ALIGN", "ORACLE")


def log_softmax(z):
    z = z - z.max(1, keepdims=True); return z - np.log(np.exp(z).sum(1, keepdims=True))


def arc_of(net, theta_before, theta_after, X):
    net.set_flat(theta_before); l0 = log_softmax(net.forward(X)[1])
    net.set_flat(theta_after); l1 = log_softmax(net.forward(X)[1])
    kl = float((np.exp(l0) * (l0 - l1)).sum(1).mean())
    return math.sqrt(max(2.0 * kl, 0.0))


# ---------------------------------------------------------------- streams
def base_data():
    X, y = S._synthetic(); Xs, ys, meta = R.L.select_classes(X, y, 10); K = meta["classes_used"]
    return (*S.split_standardise(Xs, ys, K), K)


def stream(name):
    """Returns (tasks, K): tasks = list of (Xtrain, ytrain, Xtest, ytest) per task; test rows are the task's own."""
    Xtr, ytr, Xte, yte, K = base_data()
    if name == "S1":
        out = []
        for task in R.tasks_of(K):
            i = np.isin(ytr, task); j = np.isin(yte, task); out.append((Xtr[i], ytr[i], Xte[j], yte[j]))
        return out, K
    if name == "S2":
        r = np.random.default_rng(60_000); chunks = np.array_split(r.permutation(len(ytr)), 5); out = []
        for k, ch in enumerate(chunks):
            Q, Rr = np.linalg.qr(np.random.default_rng(61_000 + k).standard_normal((Xtr.shape[1], Xtr.shape[1])))
            Q = Q * np.sign(np.diag(Rr)); out.append((Xtr[ch] @ Q, ytr[ch], Xte @ Q, yte))
        return out, K
    if name == "S0":
        i = np.isin(ytr, list(range(K))); Xu, yu = Xtr[i], ytr[i]
        perm = np.random.default_rng(62_000).permutation(len(yu)); chunks = np.array_split(perm, 5)
        return [(Xu[ch], yu[ch], Xte, yte) for ch in chunks], K
    raise ValueError(name)


# ---------------------------------------------------------------- one run
def run(seed, tasks, K, arm, r_seq=None, force_r1=False):
    """Returns dict: acc_end[k], min_next[k] (min over the first SG_WINDOW steps of task k+1), final (all classes, mean over
    tasks' test rows), r (ARC's r sequence), n_steps."""
    rng = np.random.default_rng(seed); d = tasks[0][0].shape[1]; net = S.MLP(rng, d, K, h=HID)
    n = net.flat().size; m = np.zeros(n); v = np.zeros(n); p1 = 1.0; p2 = 1.0
    r_next = 1.0; abar = None; gbar = None; mu_r = None; var_r = None
    r_log = []; t_global = 0; prevX = None
    acc_end = []; min_next = []
    srng = np.random.default_rng(70_000 + seed)
    r_perm = srng.permutation(len(r_seq)) if (arm == "SHUF" and r_seq is not None) else None
    with np.errstate(all="ignore"):
        for j, (X, y, Xt, yt) in enumerate(tasks):
            if arm == "ORACLE" and j > 0:
                m[:] = 0; v[:] = 0; p1 = 1.0; p2 = 1.0
            watch = j > 0; mins = []
            for _ in range(EPOCHS):
                perm = rng.permutation(len(y))
                for s in range(0, len(perm), BS):
                    ii = perm[s:s + BS]; x, yy = X[ii], y[ii]
                    _, g = S.ce_loss_grad(net, x, yy)
                    b1, b2 = B1, B2
                    if arm == "ARC" and not force_r1:
                        b1, b2 = B1 ** r_next, B2 ** r_next
                    elif arm == "SHUF":
                        rr = r_seq[r_perm[t_global]] if t_global < len(r_seq) else 1.0
                        b1, b2 = B1 ** rr, B2 ** rr
                    elif arm == "KOURK":
                        gn = float(np.linalg.norm(g)); gbar = gn if gbar is None else (1 - RHO) * gbar + RHO * gn
                        rr = min(gn / gbar, R_MAX) if gbar > 0 else 1.0; b1, b2 = B1 ** rr, B2 ** rr
                    elif arm == "MECTA-M":
                        H = net.forward(x)[0]; mu_b = H.mean(0); var_b = np.maximum(H.var(0), 1e-6)
                        if mu_r is None:
                            mu_r, var_r = mu_b.copy(), var_b.copy()
                        D = float(np.mean(0.5 * ((var_b / var_r + var_r / var_b) - 2 + (mu_b - mu_r) ** 2 * (1 / var_r + 1 / var_b))))
                        f = math.exp(-D); b1, b2 = min(B1, f), min(B2, f)
                        mu_r = (1 - RHO) * mu_r + RHO * mu_b; var_r = (1 - RHO) * var_r + RHO * var_b
                    elif arm == "ALIGN":
                        nm = np.linalg.norm(m); ng = np.linalg.norm(g)
                        if nm > 0 and ng > 0 and float(g @ m) / (nm * ng) < 0:
                            m[:] = 0; p1 = 1.0
                    m = b1 * m + (1 - b1) * g; v = b2 * v + (1 - b2) * g * g; p1 *= b1; p2 *= b2
                    mh = m / (1 - p1) if p1 < 1 else m; vh = v / (1 - p2) if p2 < 1 else v
                    th0 = net.flat(); th1 = th0 - LR * mh / (np.sqrt(vh) + EPS); net.set_flat(th1)
                    if arm == "ARC":
                        Xa = x if prevX is None else np.concatenate([prevX, x])
                        a = arc_of(net, th0, th1, Xa); abar = a if abar is None else (1 - RHO) * abar + RHO * a
                        r_next = min(a / abar, R_MAX) if abar > 0 else 1.0; r_log.append(r_next)
                    prevX = x; t_global += 1
                    if watch and len(mins) < SG_WINDOW:
                        pX, py = tasks[j - 1][2], tasks[j - 1][3]; mins.append(100 * net.acc(pX, py))
            if watch:
                min_next.append(min(mins))
            acc_end.append(100 * net.acc(Xt, yt))
    final = float(np.mean([100 * net.acc(t[2], t[3]) for t in tasks]))
    sg = [acc_end[k] - min_next[k] for k in range(len(min_next))]
    return dict(acc_end=acc_end, min_next=min_next, sg=float(np.mean(sg)), minacc=float(np.mean(min_next)), final=final,
                r=r_log, n_steps=t_global)
