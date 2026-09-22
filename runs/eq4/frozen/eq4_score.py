"""Study EQ4 — the BOUNDED normalised penalty step (EQ-B: the present gradient clipped at kappa x the running median of
its own recent length, the equanimity ratio then taken on the clipped gradient, Omega = 1) for online EWC on unseen PMLB
streams, beside the registered rule (EQ2/EQ3), with the controls of EQ3 (ER-sum, DER++, LwF, SI, MAS; A-GEM, GradNorm,
MEGA-I; the Bayes arm; the nine-point Omega grid; the lr x batch array) and one addition: a POISONED regime, in which
five consecutive present batches per task (from the second task) carry gradients multiplied by POISON_FACTOR, where the
enhancement is predicted to be load-bearing (theory/checks/omega_reprocessed.py [4]) and the R7 baseline is the fixed
weight WITH the same present clip. Owner request: prompt-log entry 74; prereg/eq4/PREREG.md. The design, constants and
scoring of the EQ3 rows are those of runs/eq3/frozen/eq3_score.py except where this docstring or PREREG.md says
otherwise (the capacity x epochs array and the x4 diagnostic regime are dropped; the class-selection rule is new).

    uv run python studies/eq4/eq4_score.py smoke                       # every (method, mode) branch once on synthetic data
    uv run python studies/eq4/eq4_score.py smokefull [--out F]         # run_all + score end to end on synthetic data
    uv run python studies/eq4/eq4_score.py all   <dataset> [--out F]   # every arm, seeds 0-4, JSON lines
    uv run python studies/eq4/eq4_score.py score <results.jsonl ...>   # rows EQ4-0..7, S, P, B, D, I
    uv run python studies/eq4/eq4_score.py run   <dataset> <method> <mode> <value> <seed> [--regime std|poison]

Update rule for every method:  g = wp * g_present + w * g_past.
  mode 'fixed'     w = value (the method's own hand-set weight)
  mode 'fixedclip' w = value, with the present gradient clipped as in 'eqb' (the R7 baseline for the poisoned regime)
  mode 'eq'        w = value * ||ema g_present|| / ||ema g_past||   (Omega = value; the registered rule, EQ2/EQ3)
  mode 'eqb'       the present gradient g_p is first clipped to length kappa x max(KEPT |g_p| over the last n_hist batches)
                   (the history holds the kept, post-clip lengths, so a run of extreme batches raises the bound by at most
                   a factor kappa per batch; no clip until N_MIN lengths are known; the window MAXIMUM, not the median,
                   because on a softmax stream the median present-gradient length collapses toward zero as a task is
                   learned and a median bound clips the informative batches, AGENT_LOG 63); then
                   w = value * ||ema g_p_clipped|| / ||ema g_past||
  mode 'bayes'     (ewc only) the Laplace weight, w = 1/2 on the task-size-weighted Fisher (EQ3)
  mode 'agem' / 'gradnorm' / 'mega'   as EQ3
  mode 'reduction' w = value = the median derived weight of the eqb Omega = 1 run (the constant the rule reduces to)
Regime 'poison': in the first epoch of every task after the first, from batch min(max(N_MIN, floor(POISON_AT * n_batches)), n_batches - run),
run = max(1, min(POISON_RUN, floor(POISON_RUN_FRAC * n_batches))) consecutive batches have g_present multiplied by POISON_FACTOR (before any clip). The EQ-B
clip history restarts at every task boundary (RESET_HIST). Past terms as EQ3. Score = final class-IL accuracy (%).
Class selection (new, pre-registered): classes ranked by row count (ties by remapped label); the K largest are used
if the K-th has >= CLASS_FLOOR rows after the subsample, else K is lowered to the largest even number that satisfies
it; a carrier with K < 4 is excluded and counted (exclusions.py).
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np  # noqa: E402

_HERE = Path(__file__).resolve()
ROOT = _HERE.parents[3] if _HERE.parent.name == "frozen" else _HERE.parents[2]   # runs/eq4/frozen/ or studies/eq4/
RAW = ROOT / "data" / "raw" / "pmlb"

# ---------------------------------------------------------------- registered constants (PREREG.md)
LR = 0.05; BS = 10; HID = 256; EPOCHS = 3; BUF = 500
SMOOTH = 0.9; WCAP = 1e4; DEN_FLOOR = 1e-12                    # registered estimator (EQ2, EQ2R, EQ3)
KAPPA = 2.0; N_HIST = 50; N_MIN = 10                            # EQ-B present clip (theory/checks/omega_reprocessed.py [4]; kappa chosen on the S-Y gate rows and the seen-carrier dev run, runs/eq4_dev)
SENS_KAPPA = (1.5, 2.0, 4.0); SENS_NHIST = (20, 50, 200)        # EQ4-S, with SENS_CAP x SENS_SMOOTH
POISON_AT = 0.25; POISON_RUN = 5; POISON_RUN_FRAC = 0.05; POISON_FACTOR = 1000.0   # regime 'poison': from batch floor(POISON_AT * n_batches) of the first epoch of each task after the first, max(1, min(POISON_RUN, floor(POISON_RUN_FRAC * n_batches))) batches carry g_present x POISON_FACTOR (omega_reprocessed.py [4]: the registered rule degrades at (100, 5), diverges at (1000, 5))
RESET_HIST = True                                                # the EQ-B clip history restarts at every task boundary (a new task's first gradients are not judged by the old task's)
OMEGA_GRID = (0.5, 0.71, 1.0, 1.41, 2.0)                        # DER++ / LwF arms (as EQ3; report only here)
OMEGA_GRID_EWC = (0.25, 0.35, 0.5, 0.71, 1.0, 1.41, 2.0, 2.83, 4.0)   # EWC arm, rule and EQ-B (plateau width, EQ4-P)
SEEDS = (0, 1, 2, 3, 4)
TEST_FRAC = 0.2
MAX_ROWS = 5000; SUBSAMPLE_SEED = 777; CLASS_FLOOR = 40
EWC_COARSE = (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0)
EWC_REFINE = (1 / 2.83, 1 / 2.0, 1 / 1.41, 1.41, 2.0, 2.83)    # times the coarse best
BAYES_W = 0.5
ER_GRID = (0.5, 1.0, 2.0, 4.0)
CONSTRAINT_GRID = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0)
DERPP_BETA = 0.5; DERPP_ALPHA_DEFAULT = 0.1; LWF_DEFAULT = 1.0; LWF_T = 2.0
SI_XI = 1e-3; N_FISHER = 50
SENS_CAP = (10.0, 100.0, 1e4); SENS_SMOOTH = (0.8, 0.9, 0.98)
X4 = 4.0                                                        # kept for split_standardise's signature; the x4 regime is not run
LOAD_BEARING_STEPS = 2.0
DATASETS = {  # PMLB name -> (K requested, classes per task); K may be lowered by the class-selection rule
    "satimage": (6, 2),
    "segmentation": (6, 2),                                       # 7 classes in the file: the 6 largest (ties by label)
    "yeast": (6, 2),                                              # 10 classes in the file, several tiny: the rule decides K
    "wine_quality_white": (4, 2),                                 # 7 classes, two tiny
    "sleep": (4, 2),                                              # 5 classes; 105908 rows -> subsample
    "page_blocks": (4, 2),                                        # 5 classes, imbalanced
}
FALLBACK = ()
ARRAY_CARRIER = "satimage"                                        # EQ4-I on this carrier only
INVAR_CELLS = ((0.0125, 10), (0.2, 10), (0.05, 5), (0.05, 20))    # EQ4-I: (lr, bs); the main cell (0.05, 10) completes the set of five
LATE_FRAC = 0.2


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pmlb(name: str, K_req: int):
    p = RAW / f"{name}.tsv.gz"
    with gzip.open(p, "rt") as f:
        header = f.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    ti = header.index("target")
    X = np.array([[float(v) for j, v in enumerate(r) if j != ti] for r in rows], np.float64)
    y = np.array([int(float(r[ti])) for r in rows])
    classes = np.unique(y); remap = {c: i for i, c in enumerate(classes)}
    y = np.array([remap[c] for c in y])
    nan = int(np.isnan(X).any(1).sum())
    if nan:
        keep = ~np.isnan(X).any(1); X, y = X[keep], y[keep]
    n_file = int(len(y))
    # class-selection rule: rank by row count (ties by remapped label), take the K largest, subsample, then check the floor
    counts = {c: int((y == c).sum()) for c in range(len(classes))}
    ranked = sorted(counts, key=lambda c: (-counts[c], c))
    K = min(K_req, len(ranked)); K -= K % 2
    while K >= 2:
        chosen = ranked[:K]; sel = np.isin(y, chosen); Xs, ys = X[sel], y[sel]
        order = {c: i for i, c in enumerate(chosen)}; ys = np.array([order[c] for c in ys])
        if len(ys) > MAX_ROWS:
            rng = np.random.default_rng(SUBSAMPLE_SEED); pick = []
            for c in range(K):
                idx = np.where(ys == c)[0]; n_c = int(round(MAX_ROWS * len(idx) / len(ys)))
                pick.append(rng.permutation(idx)[:n_c])
            pick = np.sort(np.concatenate(pick)); Xs, ys = Xs[pick], ys[pick]
        cc = [int((ys == c).sum()) for c in range(K)]
        if min(cc) >= CLASS_FLOOR: break
        K -= 2
    if K < 2: Xs, ys, cc = X[:0], y[:0], []
    return Xs, ys, dict(file=str(p.relative_to(ROOT)), sha256=sha256(p), n=int(len(ys)), n_file=n_file, d=int(X.shape[1]),
                        classes_in_file=int(len(classes)), classes_requested=K_req, classes_used=K, rows_dropped_nan=nan,
                        class_counts_file=[counts[c] for c in ranked], class_counts=cc, class_floor=CLASS_FLOOR,
                        excluded=bool(K < 4))


def split_standardise(X, y, K, regime="std"):
    """Fixed 80/20 stratified split (seed 12345, independent of run seed); standardise on the
    training part; regime 'x4' multiplies the standardised features by X4 (diagnostic only)."""
    rng = np.random.default_rng(12345)
    tr, te = [], []
    for c in range(K):
        idx = rng.permutation(np.where(y == c)[0]); n_te = int(round(TEST_FRAC * len(idx)))
        te.append(idx[:n_te]); tr.append(idx[n_te:])
    tr = np.concatenate(tr); te = np.concatenate(te)
    mu = X[tr].mean(0); sd = X[tr].std(0); sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    if regime == "x4":
        Z = Z * X4
    return Z[tr], y[tr], Z[te], y[te]


# ---------------------------------------------------------------- model
class MLP:
    def __init__(s, rng, d, K, h=HID):
        s.p = [rng.normal(0, math.sqrt(2 / d), (d, h)), np.zeros(h), rng.normal(0, math.sqrt(2 / h), (h, K)), np.zeros(K)]
        s.K = K

    def forward(s, x):
        W1, b1, W2, b2 = s.p; act = np.maximum(0, x @ W1 + b1); return act, act @ W2 + b2

    def back(s, x, dz, act):
        W1, b1, W2, b2 = s.p; dh = dz @ W2.T; dh[act <= 0] = 0
        return np.concatenate([(x.T @ dh).ravel(), dh.sum(0), (act.T @ dz).ravel(), dz.sum(0)])

    def flat(s): return np.concatenate([a.ravel() for a in s.p])

    def set_flat(s, v):
        i = 0
        for a in s.p:
            a[...] = v[i:i + a.size].reshape(a.shape); i += a.size

    def copy(s):
        m = MLP.__new__(MLP); m.p = [a.copy() for a in s.p]; m.K = s.K; return m

    def acc(s, x, y):
        with np.errstate(all="ignore"):
            z = s.forward(x)[1]
        if not np.all(np.isfinite(z)):
            return 0.0                                   # a diverged model scores zero
        return float((z.argmax(1) == y).mean())


def softmax(z):
    z = z - z.max(1, keepdims=True); p = np.exp(z); return p / p.sum(1, keepdims=True)


def ce_loss_grad(net, x, y):
    act, z = net.forward(x); p = softmax(z); n = len(y)
    loss = float(-np.log(p[np.arange(n), y] + 1e-300).mean())
    dz = p; dz[np.arange(n), y] -= 1; dz /= n
    return loss, net.back(x, dz, act)


# ---------------------------------------------------------------- one run
def run(method, mode, value, seed, Xtr, ytr, Xte, yte, K, per_task, smooth=SMOOTH, wcap=WCAP, hidden=HID, epochs=EPOCHS, lr=LR, bs=BS,
        kappa=KAPPA, n_hist=N_HIST, poison=False):
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = MLP(rng, d, K, h=hidden); n = net.flat().size; task_w_start = []
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    bufx = np.zeros((BUF, d)); bufy = np.zeros(BUF, int); bufz = np.zeros((BUF, K)); nb = 0; seen = 0
    importance = np.zeros(n); imp_bayes = np.zeros(n); theta_star = None; prev = None
    si_omega = np.zeros(n); theta_task_start = net.flat().copy()
    ema_p = ema_q = None; ema_Lp = ema_Lq = None; gn_w = np.array([1.0, 1.0]); wlog = []
    hist = []; n_clip = 0; n_clip_steps = 0; n_poisoned = 0
    fwd_bwd = 0.0; n_stream = 0
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            theta_task_start = net.flat().copy(); si_omega[:] = 0; task_w_start.append(len(wlog))
            imp_used = (imp_bayes / n_task) if mode == "bayes" else importance
            if RESET_HIST: hist = []
            n_batches = int(math.ceil(n_task / bs)); p_run = max(1, min(POISON_RUN, int(math.floor(POISON_RUN_FRAC * n_batches))))
            p_start = min(max(N_MIN, int(math.floor(POISON_AT * n_batches))), max(0, n_batches - p_run))   # never before the clip history is populated
            for ep in range(epochs):
                perm = rng.permutation(ii_task)
                for bi, t in enumerate(range(0, len(perm), bs)):
                    ii = perm[t:t + bs]; x, y = Xtr[ii], ytr[ii]; m = len(y); n_stream += m
                    L_p, g_p = ce_loss_grad(net, x, y); fwd_bwd += 3 * m
                    g_q = None; L_q = None
                    if method == "ewc" and theta_star is not None:
                        dth = net.flat() - theta_star; L_q = float((imp_used * dth ** 2).sum()); g_q = 2 * imp_used * dth
                    elif method in ("si", "mas") and theta_star is not None:
                        dth = net.flat() - theta_star; L_q = float((importance * dth ** 2).sum()); g_q = 2 * importance * dth
                    elif method == "er" and nb > 0:
                        jj = rng.integers(0, nb, m); L_q, g_q = ce_loss_grad(net, bufx[jj], bufy[jj]); fwd_bwd += 3 * m
                    elif method == "derpp" and nb > 0:
                        jj = rng.integers(0, nb, m); rx, ry, rz = bufx[jj], bufy[jj], bufz[jj]
                        L_b, g_b = ce_loss_grad(net, rx, ry); g_p = g_p + DERPP_BETA * g_b; L_p = L_p + DERPP_BETA * L_b
                        act, z = net.forward(rx); L_q = float(((z - rz) ** 2).mean()); g_q = net.back(rx, 2 * (z - rz) / (m * K), act)
                        fwd_bwd += 6 * m
                    elif method == "lwf" and prev is not None:
                        act, z = net.forward(x); zp = prev.forward(x)[1]
                        q, qp = softmax(z / LWF_T), softmax(zp / LWF_T)
                        L_q = float(LWF_T ** 2 * (qp * (np.log(qp + 1e-300) - np.log(q + 1e-300))).sum(1).mean())
                        g_q = net.back(x, LWF_T * (q - qp) / m, act); fwd_bwd += 4 * m
                    if poison and ti >= 1 and ep == 0 and p_start <= bi < p_start + p_run:
                        g_p = POISON_FACTOR * g_p; n_poisoned += 1
                    if mode in ("eqb", "fixedclip"):                       # EQ-B present bound, maintained on every batch (history of KEPT lengths, reference = window max)
                        gn = float(np.linalg.norm(g_p)); tau = kappa * float(np.max(hist[-n_hist:])) if len(hist) >= N_MIN else np.inf
                        n_clip_steps += 1
                        if gn > tau: g_p = g_p * (tau / gn); hist.append(tau); n_clip += 1
                        else: hist.append(gn)
                    theta_before = net.flat()
                    if g_q is None:
                        net.set_flat(theta_before - lr * g_p)
                    else:
                        if mode in ("fixed", "fixedclip", "reduction"):    # reduction: fixed w at the median derived w
                            wp, w = 1.0, value
                        elif mode == "bayes":
                            wp, w = 1.0, BAYES_W
                        elif mode in ("eq", "eqb"):
                            ema_p = g_p if ema_p is None else smooth * ema_p + (1 - smooth) * g_p
                            ema_q = g_q if ema_q is None else smooth * ema_q + (1 - smooth) * g_q
                            wp = 1.0; w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), DEN_FLOOR), wcap)
                        elif mode == "agem":
                            dot = float(g_p @ g_q)
                            wp = 1.0; w = (-dot / max(float(g_q @ g_q), DEN_FLOOR)) if dot < 0 else 0.0
                        elif mode == "gradnorm":
                            Gp, Gq = gn_w[0] * np.linalg.norm(g_p), gn_w[1] * np.linalg.norm(g_q)
                            Gbar = 0.5 * (Gp + Gq)
                            grad_w = np.array([np.sign(Gp - Gbar) * np.linalg.norm(g_p), np.sign(Gq - Gbar) * np.linalg.norm(g_q)])
                            gn_w = np.maximum(gn_w - 0.025 * grad_w / max(np.abs(grad_w).max(), DEN_FLOOR), 1e-3)
                            gn_w = 2 * gn_w / gn_w.sum(); wp, w = float(gn_w[0]), min(float(gn_w[1]), wcap)
                        elif mode == "mega":
                            ema_Lp = L_p if ema_Lp is None else smooth * ema_Lp + (1 - smooth) * L_p
                            ema_Lq = L_q if ema_Lq is None else smooth * ema_Lq + (1 - smooth) * L_q
                            wp = 1.0; w = min(ema_Lq / max(ema_Lp, DEN_FLOOR), wcap)
                        else:
                            raise ValueError(mode)
                        wlog.append(float(w))
                        net.set_flat(theta_before - lr * (wp * g_p + w * g_q))
                    if method == "si":
                        si_omega += -g_p * (net.flat() - theta_before)
                    if method in ("er", "derpp"):
                        for k in range(m):
                            seen += 1
                            if nb < BUF: j = nb; nb += 1
                            else:
                                j = rng.integers(seen)
                                if j >= BUF: continue
                            bufx[j] = x[k]; bufy[j] = y[k]
                            if method == "derpp": bufz[j] = net.forward(x[k:k + 1])[1][0]
            prev = net.copy(); theta_now = net.flat().copy()
            if method == "ewc":
                f = np.zeros(n)
                for _ in range(N_FISHER):
                    ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
                f_task = f / N_FISHER * bs
                importance = importance + f_task; imp_bayes = imp_bayes + n_task * f_task
            elif method == "si":
                importance = importance + np.maximum(si_omega, 0) / ((theta_now - theta_task_start) ** 2 + SI_XI)
            elif method == "mas":
                imp = np.zeros(n)
                for _ in range(N_FISHER):
                    ii = ii_task[rng.integers(0, len(ii_task), bs)]; act, z = net.forward(Xtr[ii]); imp += np.abs(net.back(Xtr[ii], 2 * z / bs, act))
                importance = importance + imp / N_FISHER
            if method in ("ewc", "si", "mas"):
                theta_star = theta_now
    late = []
    for a, b in zip(task_w_start, task_w_start[1:] + [len(wlog)]):
        if b > a: late.extend(wlog[a + int((1 - LATE_FRAC) * (b - a)):b])
    rec = dict(method=method, mode=mode, value=float(value), seed=int(seed), smooth=float(smooth), wcap=float(wcap), hidden=int(hidden), epochs=int(epochs),
               lr=float(lr), bs=int(bs), kappa=float(kappa), n_hist=int(n_hist), poison=bool(poison),
               acc=100 * net.acc(Xte, yte), w_med=float(np.median(wlog)) if wlog else None,
               w_late_med=float(np.median(late)) if late else None, w_max=float(np.max(wlog)) if wlog else None,
               w_cap_frac=float(np.mean(np.array(wlog) >= wcap)) if wlog else None,
               clip_frac=(n_clip / n_clip_steps) if n_clip_steps else None, n_poisoned=int(n_poisoned),
               fwd_bwd_per_sample=float(fwd_bwd / max(n_stream, 1)), n_stream=int(n_stream), finite=bool(np.all(np.isfinite(net.flat()))))
    json.dumps(rec)
    return rec


# ---------------------------------------------------------------- arms
def arms_stage1():
    """Everything except the refinements, the reduction arms and the array. Tuples: (method, mode, value, smooth, wcap, regime, kappa, n_hist)."""
    S, C, KP, NH = SMOOTH, WCAP, KAPPA, N_HIST
    for w in EWC_COARSE: yield ("ewc", "fixed", w, S, C, "std", KP, NH)
    for om in OMEGA_GRID_EWC: yield ("ewc", "eq", om, S, C, "std", KP, NH)
    for om in OMEGA_GRID_EWC: yield ("ewc", "eqb", om, S, C, "std", KP, NH)
    for cap in SENS_CAP:
        for sm in SENS_SMOOTH:
            if (cap, sm) != (C, S): yield ("ewc", "eqb", 1.0, sm, cap, "std", KP, NH)
    for kp in SENS_KAPPA:
        for nh in SENS_NHIST:
            if (kp, nh) != (KP, NH): yield ("ewc", "eqb", 1.0, S, C, "std", kp, nh)
    yield ("ewc", "bayes", 0.0, S, C, "std", KP, NH)
    for mode in ("agem", "gradnorm", "mega"): yield ("ewc", mode, 0.0, S, C, "std", KP, NH)
    for w in ER_GRID: yield ("er", "fixed", w, S, C, "std", KP, NH)
    yield ("er", "eq", 1.0, S, C, "std", KP, NH); yield ("er", "eqb", 1.0, S, C, "std", KP, NH)
    for meth, default in (("derpp", DERPP_ALPHA_DEFAULT), ("lwf", LWF_DEFAULT)):
        for w in sorted(set(CONSTRAINT_GRID) | {default}): yield (meth, "fixed", w, S, C, "std", KP, NH)
        yield (meth, "eq", 1.0, S, C, "std", KP, NH); yield (meth, "eqb", 1.0, S, C, "std", KP, NH)
    for meth in ("si", "mas"):
        for w in CONSTRAINT_GRID: yield (meth, "fixed", w, S, C, "std", KP, NH)
        yield (meth, "eqb", 1.0, S, C, "std", KP, NH)
    # poisoned regime: the fixed weight, the fixed weight with the clip (R7 baseline), the registered rule, EQ-B
    for w in EWC_COARSE: yield ("ewc", "fixed", w, S, C, "poison", KP, NH)
    for w in EWC_COARSE: yield ("ewc", "fixedclip", w, S, C, "poison", KP, NH)
    yield ("ewc", "eq", 1.0, S, C, "poison", KP, NH); yield ("ewc", "eqb", 1.0, S, C, "poison", KP, NH)


def key(o): return (o["method"], o["mode"], round(o["value"], 6), o["smooth"], o["wcap"], o.get("regime", "std"), o.get("hidden", HID),
                    o.get("epochs", EPOCHS), o.get("lr", LR), o.get("bs", BS), o.get("kappa", KAPPA), o.get("n_hist", N_HIST))


def run_all(name, data_std, K, per_task, meta, out, array_carrier=ARRAY_CARRIER):
    hdr = dict(dataset=name, **meta, K=K, per_task=per_task, n_train=int(len(data_std[1])), n_test=int(len(data_std[3])),
               lr=LR, bs=BS, hidden=HID, epochs=EPOCHS, buf=BUF, smooth=SMOOTH, wcap=WCAP, den_floor=DEN_FLOOR, bayes_w=BAYES_W,
               kappa=KAPPA, n_hist=N_HIST, n_min=N_MIN, reset_hist=RESET_HIST, poison_at=POISON_AT, poison_run=POISON_RUN, poison_run_frac=POISON_RUN_FRAC, poison_factor=POISON_FACTOR,
               n_fisher=N_FISHER, si_xi=SI_XI, derpp_beta=DERPP_BETA, lwf_T=LWF_T, max_rows=MAX_ROWS, subsample_seed=SUBSAMPLE_SEED,
               uv_lock_sha256=sha256(ROOT / "uv.lock"))
    print(json.dumps(hdr), file=out, flush=True)
    done = {}

    def go(method, mode, value, sm, cap, regime="std", kappa=KAPPA, n_hist=N_HIST, hidden=HID, epochs=EPOCHS, lr=LR, bs=BS):
        for seed in SEEDS:
            o = run(method, mode, value, seed, *data_std, K, per_task, smooth=sm, wcap=cap, hidden=hidden, epochs=epochs, lr=lr, bs=bs,
                    kappa=kappa, n_hist=n_hist, poison=(regime == "poison"))
            o["dataset"] = name; o["regime"] = regime; print(json.dumps(o), file=out, flush=True)
            done.setdefault(key(o), []).append(o["acc"])

    def median_w(meth, mode, regime):
        return float(np.median([o["w_med"] for o in recs if o["method"] == meth and o["mode"] == mode and o["value"] == 1.0
                                and o["smooth"] == SMOOTH and o["wcap"] == WCAP and o["regime"] == regime and o["hidden"] == HID
                                and o["epochs"] == EPOCHS and o["lr"] == LR and o["bs"] == BS and o["kappa"] == KAPPA and o["n_hist"] == N_HIST]))

    for a in arms_stage1(): go(*a)
    # stage 2: refinement at sqrt2 spacing around the coarse best, clean fixed and poisoned fixedclip (pre-registered tuning rule)
    for mode, regime in (("fixed", "std"), ("fixedclip", "poison")):
        best = max(EWC_COARSE, key=lambda w: np.mean(done[("ewc", mode, round(w, 6), SMOOTH, WCAP, regime, HID, EPOCHS, LR, BS, KAPPA, N_HIST)]))
        for f in EWC_REFINE:
            w = round(best * f, 6)
            if all(abs(w - c) / c > 1e-6 for c in EWC_COARSE): go("ewc", mode, w, SMOOTH, WCAP, regime)
    # reduction arms: fixed w at the median derived weight of the EQ-B Omega = 1 run (EWC and ER)
    recs = [json.loads(l) for l in open(out.name) if l.startswith("{")]; recs = [o for o in recs if "acc" in o]
    for meth in ("ewc", "er"):
        go(meth, "reduction", round(median_w(meth, "eqb", "std"), 6), SMOOTH, WCAP)
    # EQ4-I (lr x batch) on the registered carrier only: EWC coarse grid and EQ-B at Omega = 1 per cell
    if name == array_carrier:
        for lr, bs in INVAR_CELLS:
            for w in EWC_COARSE: go("ewc", "fixed", w, SMOOTH, WCAP, "std", KAPPA, N_HIST, HID, EPOCHS, lr, bs)
            go("ewc", "eqb", 1.0, SMOOTH, WCAP, "std", KAPPA, N_HIST, HID, EPOCHS, lr, bs)


# ---------------------------------------------------------------- scoring (EQ4-0..7, S, P, B, D, I; PREREG.md)
def step_of_public(tv): return max(1.0, 2 * float(np.std(tv, ddof=1)) / math.sqrt(len(tv)))


def score(paths, array_carrier=ARRAY_CARRIER):
    rows = []; hdrs = {}
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "acc" in o: rows.append(o)
                elif "dataset" in o: hdrs[o["dataset"]] = o
    ds = sorted(set(r["dataset"] for r in rows))

    def A(name, method, mode, value=None, sm=SMOOTH, cap=WCAP, regime="std", hidden=HID, epochs=EPOCHS, lr=LR, bs=BS, kappa=KAPPA, n_hist=N_HIST, field="acc"):
        v = sorted([r for r in rows if r["dataset"] == name and r["method"] == method and r["mode"] == mode and r["regime"] == regime
                    and (value is None or abs(r["value"] - value) < 1e-6) and r["smooth"] == sm and r["wcap"] == cap
                    and r["hidden"] == hidden and r["epochs"] == epochs and r["lr"] == lr and r["bs"] == bs
                    and r["kappa"] == kappa and r["n_hist"] == n_hist], key=lambda r: r["seed"])
        assert len(v) == len(SEEDS), (name, method, mode, value, sm, cap, regime, hidden, epochs, lr, bs, kappa, n_hist, [r["seed"] for r in v])
        return np.array([r[field] for r in v], dtype=float)

    def grid(name, method, mode="fixed", regime="std", hidden=HID, epochs=EPOCHS, lr=LR, bs=BS):
        ws = sorted(set(round(r["value"], 6) for r in rows if r["dataset"] == name and r["method"] == method and r["mode"] == mode and r["regime"] == regime
                        and r["hidden"] == hidden and r["epochs"] == epochs and r["lr"] == lr and r["bs"] == bs))
        return {w: A(name, method, mode, w, regime=regime, hidden=hidden, epochs=epochs, lr=lr, bs=bs) for w in ws}

    def fmt(x): return f"{x.mean():.4f} [" + " ".join(f"{q:.2f}" for q in x) + "]"
    def step_of(tv): return max(1.0, 2 * tv.std(ddof=1) / math.sqrt(len(tv)))

    print("=" * 112); print("EQ4 scoring — per-seed values in brackets (seeds 0-4); thresholds from prereg/eq4/PREREG.md"); print("=" * 112)
    R = {}
    for name in ds:
        R[name] = {}; h = hdrs.get(name, {})
        print(f"\n[{name}]  K = {h.get('classes_used')} of {h.get('classes_in_file')} classes (requested {h.get('classes_requested')}; floor {h.get('class_floor')}); class counts {h.get('class_counts')}; n = {h.get('n')} of {h.get('n_file')} rows")
        g = grid(name, "ewc"); tuned = max(g, key=lambda w: g[w].mean()); tv = g[tuned]; step = step_of(tv)
        eq = {om: A(name, "ewc", "eq", om) for om in OMEGA_GRID_EWC}; eqb = {om: A(name, "ewc", "eqb", om) for om in OMEGA_GRID_EWC}
        red = A(name, "ewc", "reduction"); wm = [r for r in rows if r["dataset"] == name and r["method"] == "ewc" and r["mode"] == "reduction" and r["regime"] == "std"][0]["value"]
        bay = A(name, "ewc", "bayes", 0.0)
        print(f"   resolvable step = max(1.0, 2*SE) = {step:.4f}  (tuned-lambda SE {tv.std(ddof=1) / math.sqrt(len(tv)):.4f})")
        print(f"   EWC fixed-lambda grid: " + "  ".join(f"{w:g}:{g[w].mean():.2f}" for w in g))
        print(f"   EWC tuned lambda = {tuned:g}: {fmt(tv)}")
        for om in OMEGA_GRID_EWC: print(f"   EWC rule Ω={om:<4}: {fmt(eq[om])}   Ω − tuned: {eq[om].mean()-tv.mean():+.4f}  | EQ-B Ω={om:<4}: {fmt(eqb[om])}   EQ-B − tuned: {eqb[om].mean()-tv.mean():+.4f}")
        clipf = A(name, "ewc", "eqb", 1.0, field="clip_frac")
        print(f"   EQ-B clip fraction at Ω=1 (clean): {clipf.mean():.4f} [" + " ".join(f"{q:.3f}" for q in clipf) + "]")
        print(f"   EWC reduction arm (fixed w = median derived {wm:g} of EQ-B): {fmt(red)}   EQ-B(Ω=1) − reduction: {eqb[1.0].mean()-red.mean():+.4f}")
        print(f"   EWC Bayes arm (Laplace weight {BAYES_W}): {fmt(bay)}   Bayes − tuned: {bay.mean()-tv.mean():+.4f}; EQ-B(Ω=1) − Bayes: {eqb[1.0].mean()-bay.mean():+.4f}")
        d1 = eq[1.0] - tv; d1b = eqb[1.0] - tv
        R[name].update(step=step, tuned=tuned, tv=tv, eq=eq, eqb=eqb, d1=d1, d1b=d1b, red=red, wm=wm, g=g, bay=bay)
        sens = {}
        for cap in SENS_CAP:
            for sm in SENS_SMOOTH:
                if (cap, sm) != (WCAP, SMOOTH): sens[("cap", cap, sm)] = A(name, "ewc", "eqb", 1.0, sm, cap).mean() - tv.mean()
        for kp in SENS_KAPPA:
            for nh in SENS_NHIST:
                if (kp, nh) != (KAPPA, N_HIST): sens[("clip", kp, nh)] = A(name, "ewc", "eqb", 1.0, kappa=kp, n_hist=nh).mean() - tv.mean()
        print("   sensitivity (EQ-B Ω=1 − tuned): " + "  ".join((f"cap{b:g}/sm{c}:{v:+.2f}" if a == "cap" else f"k{b:g}/N{c}:{v:+.2f}") for (a, b, c), v in sens.items()))
        R[name]["sens"] = sens
        for mode in ("agem", "gradnorm", "mega"):
            b = A(name, "ewc", mode, 0.0); R[name][mode] = b
            print(f"   EWC baseline {mode:8s}: {fmt(b)}   EQ-B(Ω=1) − baseline: {eqb[1.0].mean()-b.mean():+.4f}")
        ge = grid(name, "er"); bt = max(ge, key=lambda w: ge[w].mean()); ere = A(name, "er", "eq", 1.0); erb = A(name, "er", "eqb", 1.0); err = A(name, "er", "reduction")
        R[name].update(er_best=bt, er_bestv=ge[bt], er_eq=ere, er_eqb=erb, er_red=err)
        print(f"   ER-sum grid: " + "  ".join(f"{w:g}:{ge[w].mean():.2f}" for w in ge) + f"; rule Ω=1: {fmt(ere)}; EQ-B Ω=1: {fmt(erb)}  EQ-B − best fixed: {erb.mean()-ge[bt].mean():+.4f}; reduction arm: {fmt(err)}  EQ-B − reduction: {erb.mean()-err.mean():+.4f}")
        for meth in ("derpp", "lwf"):
            gc = grid(name, meth); tc = max(gc, key=lambda w: gc[w].mean()); e1 = A(name, meth, "eq", 1.0); b1 = A(name, meth, "eqb", 1.0)
            finite = [gc[w].mean() for w in gc if all(r["finite"] for r in rows if r["dataset"] == name and r["method"] == meth and r["mode"] == "fixed" and abs(r["value"] - w) < 1e-6 and r["regime"] == "std")]
            span = (max(finite) - min(finite)) if finite else 0.0; lb = span >= LOAD_BEARING_STEPS * step
            R[name][meth] = (tc, gc[tc], e1, b1, lb, span)
            print(f"   {meth:5s} tuned w={tc:g}: {fmt(gc[tc])}; rule Ω=1: {fmt(e1)} ({e1.mean()-gc[tc].mean():+.4f}); EQ-B Ω=1: {fmt(b1)} ({b1.mean()-gc[tc].mean():+.4f}); finite-grid span {span:.4f} -> {'load-bearing' if lb else 'inert'} (report only: outside the narrowed H-EQ)")
        for meth in ("si", "mas"):
            gc = grid(name, meth); tc = max(gc, key=lambda w: gc[w].mean()); b1 = A(name, meth, "eqb", 1.0); R[name][meth] = (tc, gc[tc], b1)
            print(f"   {meth:5s} tuned w={tc:g}: {fmt(gc[tc])}; EQ-B Ω=1: {fmt(b1)}  EQ-B − tuned: {b1.mean()-gc[tc].mean():+.4f}")
        # poisoned regime
        gp = grid(name, "ewc", "fixed", "poison"); tp = max(gp, key=lambda w: gp[w].mean())
        gpc = grid(name, "ewc", "fixedclip", "poison"); tpc = max(gpc, key=lambda w: gpc[w].mean()); tvp = gpc[tpc]; stepp = step_of(tvp)
        eqp = A(name, "ewc", "eq", 1.0, regime="poison"); eqbp = A(name, "ewc", "eqb", 1.0, regime="poison")
        finp = A(name, "ewc", "eq", 1.0, regime="poison", field="finite"); wmaxp = A(name, "ewc", "eq", 1.0, regime="poison", field="w_max")
        R[name].update(p_tuned=tp, p_tv=gp[tp], pc_tuned=tpc, pc_tv=tvp, p_step=stepp, p_eq=eqp, p_eqb=eqbp, p_eq_finite=finp)
        print(f"   POISON (x{POISON_FACTOR:g} for up to {POISON_RUN} batches per task from task 2): step = {stepp:.4f}; fixed tuned lambda={tp:g}: {fmt(gp[tp])}; fixed+clip tuned lambda={tpc:g}: {fmt(tvp)}; rule Ω=1: {fmt(eqp)} (finite {int(finp.sum())}/5; max w {np.median(wmaxp):.4g} median over seeds); EQ-B Ω=1: {fmt(eqbp)}")
        print(f"          EQ-B − fixed+clip tuned: {eqbp.mean()-tvp.mean():+.4f}; rule − EQ-B: {eqp.mean()-eqbp.mean():+.4f}; fixed(no clip) tuned − fixed+clip tuned: {gp[tp].mean()-tvp.mean():+.4f}")

    n = len(ds); print("\n" + "-" * 112)
    lams = [R[d]["tuned"] for d in ds]; span = max(lams) / min(lams); decidable = span >= 10
    print(f"EQ4-0 precondition: tuned lambda per carrier {dict(zip(ds, lams))}, span {span:.2f}x -> {'DECIDABLE' if decidable else 'NOT DECIDABLE: tuned lambda did not move >= 10x'}")
    common = max(EWC_COARSE, key=lambda w: np.mean([R[d]["g"][w].mean() for d in ds]))
    loss_common = {d: R[d]["tv"].mean() - R[d]["g"][common].mean() for d in ds}
    single_transfers = all(loss_common[d] < R[d]["step"] for d in ds)
    nbB = {d: R[d]["d1b"].mean() > -R[d]["step"] for d in ds}; nbR = {d: R[d]["d1"].mean() > -R[d]["step"] for d in ds}
    v1 = all(nbB.values()) and not single_transfers; v1r = all(nbR.values()) and not single_transfers
    print(f"EQ4-1 H-EQ-B (clean): EQ-B(Ω=1) − tuned per carrier " + ", ".join(f"{d}:{R[d]['d1b'].mean():+.4f} (step {R[d]['step']:.2f}; seeds not behind {int((R[d]['d1b'] > -R[d]['step']).sum())}/5)" for d in ds)
          + f"; best single lambda={common:g} loses " + ", ".join(f"{d}:{loss_common[d]:.4f}" for d in ds)
          + f"; not behind on {sum(nbB.values())}/{n} -> {'PASS' if v1 else 'FAIL'}" + ("" if decidable else " (reported without verdict: EQ4-0 not decidable)"))
    print(f"EQ4-1r registered rule (EQ3-1 on fresh carriers): Ω=1 − tuned " + ", ".join(f"{d}:{R[d]['d1'].mean():+.4f}" for d in ds) + f"; not behind on {sum(nbR.values())}/{n} -> {'PASS' if v1r else 'FAIL'}")
    idle = {d: abs(R[d]["eqb"][1.0].mean() - R[d]["eq"][1.0].mean()) < R[d]["step"] for d in ds}
    print(f"EQ4-2 bound idle on clean streams: EQ-B(Ω=1) − rule(Ω=1) " + ", ".join(f"{d}:{R[d]['eqb'][1.0].mean()-R[d]['eq'][1.0].mean():+.4f}" for d in ds) + f"; within a step on {sum(idle.values())}/{n} -> {'IDLE' if all(idle.values()) else 'NOT IDLE'}")
    nb3 = {d: (R[d]["p_eqb"].mean() - R[d]["pc_tv"].mean()) > -R[d]["p_step"] for d in ds}
    print(f"EQ4-3 poisoned: EQ-B(Ω=1) − tuned fixed+clip " + ", ".join(f"{d}:{R[d]['p_eqb'].mean()-R[d]['pc_tv'].mean():+.4f} (step {R[d]['p_step']:.2f})" for d in ds) + f"; not behind on {sum(nb3.values())}/{n} -> {'PASS' if all(nb3.values()) else 'FAIL'}")
    beh4 = {d: (R[d]["p_eq"].mean() - R[d]["p_eqb"].mean()) <= -R[d]["p_step"] for d in ds}; need = (n + 1) // 2
    print(f"EQ4-4 poisoned mechanism (positive control of the enhancement): rule(Ω=1) − EQ-B(Ω=1) " + ", ".join(f"{d}:{R[d]['p_eq'].mean()-R[d]['p_eqb'].mean():+.4f} (rule finite {int(R[d]['p_eq_finite'].sum())}/5)" for d in ds)
          + f"; rule behind EQ-B by a step on {sum(beh4.values())}/{n} (needs >= {need}) -> {'LOAD-BEARING' if sum(beh4.values()) >= need else 'INERT: the poison does not separate the two rules on these carriers'}")
    c5 = all((R[d]["er_eqb"].mean() - R[d]["er_bestv"].mean()) < R[d]["step"] and abs(R[d]["er_eqb"].mean() - R[d]["er_red"].mean()) < R[d]["step"] for d in ds)
    print(f"EQ4-5 control ER-sum: EQ-B − best fixed " + ", ".join(f"{d}:{R[d]['er_eqb'].mean()-R[d]['er_bestv'].mean():+.4f}" for d in ds)
          + "; EQ-B − reduction " + ", ".join(f"{d}:{R[d]['er_eqb'].mean()-R[d]['er_red'].mean():+.4f}" for d in ds) + f" -> {'holds' if c5 else 'VIOLATED'}")
    reduces = all(abs(R[d]["eqb"][1.0].mean() - R[d]["red"].mean()) < R[d]["step"] for d in ds)
    print(f"EQ4-6 reduction: EQ-B − fixed@median per carrier " + ", ".join(f"{d}:{R[d]['eqb'][1.0].mean()-R[d]['red'].mean():+.4f}" for d in ds)
          + f" -> {'REDUCES to a per-carrier constant' if reduces else 'DOES NOT REDUCE: normalised-gradient method'}")
    dom = {m: all((R[d][m].mean() - R[d]["eqb"][1.0].mean()) >= R[d]["step"] for d in ds) for m in ("agem", "gradnorm", "mega")}
    print("EQ4-7 published baselines vs EQ-B(Ω=1): " + ", ".join(f"{d}/{m}:{R[d][m].mean()-R[d]['eqb'][1.0].mean():+.4f}" for d in ds for m in ("agem", "gradnorm", "mega"))
          + " -> " + ("; ".join(f"{m} dominates EQ-B" for m, v in dom.items() if v) or "no published baseline is ahead of EQ-B by a step on every carrier"))
    flips = sum(1 for d in ds for k, v in R[d]["sens"].items() if (v > -R[d]["step"]) != nbB[d])
    print(f"EQ4-S sensitivity: EQ4-1 'not behind' flips in {flips} of {16*n} cells -> {'FRAGILE' if flips > 1 else 'not fragile'}")
    partsP = []; widths = []
    for d in ds:
        means = {o: R[d]["eqb"][o].mean() for o in OMEGA_GRID_EWC}; b = max(means.values())
        within = [o for o in OMEGA_GRID_EWC if means[o] >= b - R[d]["step"]]
        idx = [OMEGA_GRID_EWC.index(o) for o in within]; contiguous = (max(idx) - min(idx) + 1 == len(idx))
        widths.append(len(within)); partsP.append(f"{d}: {len(within)} of 9 within a step of the best ({min(within):g}..{max(within):g}, {'contiguous' if contiguous else 'not contiguous'})")
    print("EQ4-P plateau width of EQ-B on the nine-point grid: " + "; ".join(partsP) + f"; median width {float(np.median(widths)):g} (report only)")
    nbBay = sum(1 for d in ds if (R[d]["bay"].mean() - R[d]["tv"].mean()) > -R[d]["step"])
    print("EQ4-B Bayes arm (Laplace weight 1/2): Bayes − tuned " + ", ".join(f"{d}:{R[d]['bay'].mean()-R[d]['tv'].mean():+.4f}" for d in ds)
          + "; EQ-B(Ω=1) − Bayes " + ", ".join(f"{d}:{R[d]['eqb'][1.0].mean()-R[d]['bay'].mean():+.4f}" for d in ds) + f"; Bayes not behind tuned on {nbBay}/{n} (report only)")
    print("EQ4-D DER++/LwF (outside the narrowed H-EQ; report only): EQ-B(Ω=1) − tuned " + ", ".join(f"{d}/{m}:{R[d][m][3].mean()-R[d][m][1].mean():+.4f}{'' if R[d][m][4] else ' (inert)'}" for d in ds for m in ("derpp", "lwf"))
          + "; SI/MAS: " + ", ".join(f"{d}/{m}:{R[d][m][2].mean()-R[d][m][1].mean():+.4f}" for d in ds for m in ("si", "mas")))
    if array_carrier in ds:
        cells = [(LR, BS)] + list(INVAR_CELLS); nbI = 0; partsI = []
        for lr, bs in cells:
            g_ = grid(array_carrier, "ewc", lr=lr, bs=bs); tuned_ = max(g_, key=lambda w: g_[w].mean()); tv_ = g_[tuned_]
            step_ = step_of(tv_); e1 = A(array_carrier, "ewc", "eqb", 1.0, lr=lr, bs=bs)
            nb = (e1.mean() - tv_.mean()) > -step_; nbI += nb
            partsI.append(f"lr{lr:g}/bs{bs}: tuned {tuned_:g} -> {tv_.mean():.2f}, EQ-B {e1.mean():.2f}, diff {e1.mean() - tv_.mean():+.2f} (step {step_:.2f}) {'nb' if nb else 'behind'}")
        print(f"EQ4-I lr x batch invariance on {array_carrier}: " + "; ".join(partsI) + f" -> not behind in {nbI}/5 cells -> {'PASS' if nbI >= 4 else 'FAIL'}")
    print(f"summary: EQ4-1 {'PASS' if v1 else 'FAIL'} (EQ-B not behind on {sum(nbB.values())}/{n}); EQ4-1r {'PASS' if v1r else 'FAIL'} (rule not behind on {sum(nbR.values())}/{n}); bound idle: {all(idle.values())}; poisoned EQ4-3 {'PASS' if all(nb3.values()) else 'FAIL'}; mechanism EQ4-4 {'LOAD-BEARING' if sum(beh4.values()) >= need else 'INERT'}; fragile: {flips > 1}; ER-sum control {'holds' if c5 else 'violated'}")


# ---------------------------------------------------------------- main
def _load(name):
    K_req, per_task = DATASETS.get(name, (6, 2))
    X, y, meta = load_pmlb(name, K_req)
    if meta["excluded"]:
        return None, meta["classes_used"], per_task, meta
    return split_standardise(X, y, meta["classes_used"]), meta["classes_used"], per_task, meta


def _synthetic(K=10, n=1500, d=20):
    rng = np.random.default_rng(0)
    X = rng.standard_normal((n, d)); y = rng.integers(0, K, n); X[np.arange(n), y % d] += 3.0
    return X, y


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        X, y = _synthetic(); K = 10
        data = split_standardise(X, y, K)
        for a in (("ewc", "fixed", 10.0), ("ewc", "fixedclip", 10.0), ("ewc", "eq", 1.0), ("ewc", "eqb", 1.0), ("ewc", "bayes", 0.0), ("ewc", "reduction", 5.0), ("ewc", "agem", 0.0), ("ewc", "gradnorm", 0.0), ("ewc", "mega", 0.0),
                  ("er", "fixed", 1.0), ("er", "eq", 1.0), ("er", "eqb", 1.0), ("er", "reduction", 1.0), ("derpp", "fixed", 0.1), ("derpp", "eq", 1.0), ("derpp", "eqb", 1.0), ("lwf", "fixed", 1.0), ("lwf", "eq", 1.0), ("lwf", "eqb", 1.0),
                  ("si", "fixed", 0.1), ("si", "eqb", 1.0), ("mas", "fixed", 0.1), ("mas", "eqb", 1.0)):
            print(json.dumps(run(*a, 0, *data, K, 2)))
        for a in (("ewc", "fixed", 10.0), ("ewc", "fixedclip", 10.0), ("ewc", "eq", 1.0), ("ewc", "eqb", 1.0)):
            print(json.dumps(run(*a, 0, *data, K, 2, poison=True)))
        for kp, nh in ((1.5, 20), (4.0, 200)): print(json.dumps(run("ewc", "eqb", 1.0, 0, *data, K, 2, kappa=kp, n_hist=nh)))
        for lr, bs in INVAR_CELLS: print(json.dumps(run("ewc", "eqb", 1.0, 0, *data, K, 2, lr=lr, bs=bs)))
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/eq4_smokefull.jsonl"
        X, y = _synthetic(); K = 10
        meta = dict(file="synthetic", sha256="none", n=len(y), n_file=len(y), d=X.shape[1], classes_in_file=K, classes_requested=K, classes_used=K,
                    rows_dropped_nan=0, class_counts_file=[int((y == c).sum()) for c in range(K)], class_counts=[int((y == c).sum()) for c in range(K)],
                    class_floor=CLASS_FLOOR, excluded=False)
        with open(outp, "w") as out:
            run_all("synthetic", split_standardise(X, y, K), K, 2, meta, out, array_carrier="synthetic")
        score([outp], array_carrier="synthetic")
    elif cmd == "run":
        name, method, mode, value, seed = sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), int(sys.argv[6])
        regime = sys.argv[sys.argv.index("--regime") + 1] if "--regime" in sys.argv else "std"
        data, K, per_task, meta = _load(name)
        if data is None: print(json.dumps(dict(dataset=name, excluded=True, **meta))); sys.exit(0)
        o = run(method, mode, value, seed, *data, K, per_task, poison=(regime == "poison")); o["dataset"] = name; o["regime"] = regime; print(json.dumps(o))
    elif cmd == "all":
        name = sys.argv[2]
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/eq4/results_{name}.jsonl"
        data_std, K, per_task, meta = _load(name)
        with open(outp, "w") as out:
            if data_std is None:
                print(json.dumps(dict(dataset=name, **meta)), file=out, flush=True)   # excluded carrier: header only
            else:
                run_all(name, data_std, K, per_task, meta, out)
    elif cmd == "score":
        score(sys.argv[2:])
    else:
        raise SystemExit(__doc__)
