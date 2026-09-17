"""Study EQ2R — replication of EQ2 (the normalised penalty step for online EWC, with ER-sum, DER++ and
LwF as controls) on the three PMLB streams EQ2 pre-registered as fallbacks and never opened
(mfeat_karhunen, mfeat_zernike, vowel), plus three pre-registered arrays: the ratio cap as a primary
axis (EQ2R-C), the empty-present diagnostic (EQ2R-D: the derived weight late in each task), and a
capacity x epochs array on one carrier (EQ2R-A). prereg/eq2r/PREREG.md. The design, constants and
scoring of EQ2R-0..8 are byte-for-byte those of EQ2 (runs/eq2/frozen/eq2_score.py) except where this
docstring says otherwise.

    uv run python studies/eq2r/eq2r_score.py smoke                  # synthetic data, no download
    uv run python studies/eq2r/eq2r_score.py all   <dataset> [--out F]   # every arm, seeds 0-4, JSON lines
    uv run python studies/eq2r/eq2r_score.py score <results.jsonl ...>   # rows EQ2R-0..8, C, D, A as pre-registered
    uv run python studies/eq2r/eq2r_score.py run   <dataset> <method> <mode> <value> <seed> [--regime std|x4]

Update rule for every method:  g = g_present + w * g_past.
  mode 'fixed'   w = value (the method's own hand-set weight)
  mode 'eq'      w = value * ||ema g_present|| / ||ema g_past||   (Omega = value; the equanimity rule)
  mode 'agem'    A-GEM projection of g_present against g_past (no w)
  mode 'gradnorm' GradNorm (alpha = 0) weights learned online, normalised to sum 2
  mode 'mega'    MEGA-I loss-ratio weight  w = ema L_past / ema L_present
Past terms (lambda / alpha REMOVED from the gradient):
  ewc   online EWC penalty 2 * F * (theta - theta_star), F accumulated at each task boundary
  er    cross-entropy on a replay batch (ER-sum: two batch means, summed)
  derpp logit-matching MSE on a replay batch (DER++'s alpha term); DER++'s beta * CE(replay), beta = 0.5,
        stays inside the PRESENT term at its published default
  lwf   distillation on the current batch against the model frozen at the last boundary (T = 2)
  si    synaptic-intelligence penalty (path-integral importance, xi = 1e-3)
  mas   memory-aware-synapses penalty (importance = |d ||f(x)||^2 / d theta|)
Score = final class-IL accuracy (%) over all classes, single head, per seed.
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

ROOT = Path(__file__).resolve().parents[2]
if ROOT.name == "runs":                       # frozen copy lives in runs/<study>/frozen/
    ROOT = ROOT.parent
RAW = ROOT / "data" / "raw" / "pmlb"

# ---------------------------------------------------------------- frozen study parameters
LR = 0.05; BS = 10; HID = 256; EPOCHS = 3; BUF = 500
SMOOTH = 0.9; WCAP = 1e4; DEN_FLOOR = 1e-12                    # registered estimator (issue #20 §2)
OMEGA_GRID = (0.5, 0.71, 1.0, 1.41, 2.0)
SEEDS = (0, 1, 2, 3, 4)
TEST_FRAC = 0.2
EWC_COARSE = (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0)
EWC_REFINE = (1 / 2.83, 1 / 2.0, 1 / 1.41, 1.41, 2.0, 2.83)    # times the coarse best
ER_GRID = (0.5, 1.0, 2.0, 4.0)
CONSTRAINT_GRID = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0)      # DER++ alpha, LwF weight, SI c, MAS lambda
DERPP_BETA = 0.5; DERPP_ALPHA_DEFAULT = 0.1; LWF_DEFAULT = 1.0; LWF_T = 2.0
SI_XI = 1e-3; N_FISHER = 50
SENS_CAP = (10.0, 100.0, 1e4); SENS_SMOOTH = (0.8, 0.9, 0.98)
X4 = 4.0                                                        # diagnostic regime: standardised features x 4
DATASETS = {  # PMLB name -> (classes used, classes per task); classes beyond `used` (label order) are dropped
    "mfeat_karhunen": (10, 2),
    "mfeat_zernike": (10, 2),
    "vowel": (10, 2),                                             # 11 classes in the file; the 11th (label order) is dropped
}
FALLBACK = ()                                                     # none: a carrier that cannot be fetched is reported, not replaced
ARRAY_CARRIER = "mfeat_karhunen"                                  # EQ2R-A: capacity x epochs array on this carrier only
ARRAY_CELLS = ((64, 1), (64, 3), (256, 1))                        # (hidden, epochs); the main cell (256, 3) completes the 2 x 2
LATE_FRAC = 0.2                                                   # EQ2R-D: the last 20 % of each task's steps


# ---------------------------------------------------------------- data
def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pmlb(name: str, K: int):
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
    dropped = int((y >= K).sum()); keep = y < K; X, y = X[keep], y[keep]
    return X, y, dict(file=str(p.relative_to(ROOT)), sha256=sha256(p), n=int(len(y)), d=int(X.shape[1]),
                      classes_in_file=int(len(classes)), classes_used=K, rows_dropped_nan=nan, rows_dropped_extra_classes=dropped)


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
        W1, b1, W2, b2 = s.p; hid = np.maximum(0, x @ W1 + b1); return hid, hid @ W2 + b2

    def back(s, x, dz, hid):
        W1, b1, W2, b2 = s.p; dh = dz @ W2.T; dh[hid <= 0] = 0
        return np.concatenate([(x.T @ dh).ravel(), dh.sum(0), (hid.T @ dz).ravel(), dz.sum(0)])

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
    hid, z = net.forward(x); p = softmax(z); n = len(y)
    loss = float(-np.log(p[np.arange(n), y] + 1e-300).mean())
    dz = p; dz[np.arange(n), y] -= 1; dz /= n
    return loss, net.back(x, dz, hid)


# ---------------------------------------------------------------- one run
def run(method, mode, value, seed, Xtr, ytr, Xte, yte, K, per_task, smooth=SMOOTH, wcap=WCAP, hid=HID, epochs=EPOCHS):
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = MLP(rng, d, K, h=hid); n = net.flat().size; task_w_start = []
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    bufx = np.zeros((BUF, d)); bufy = np.zeros(BUF, int); bufz = np.zeros((BUF, K)); nb = 0; seen = 0
    importance = np.zeros(n); theta_star = None; prev = None
    si_omega = np.zeros(n); theta_task_start = net.flat().copy()
    ema_p = ema_q = None; ema_Lp = ema_Lq = None; gn_w = np.array([1.0, 1.0]); wlog = []
    fwd_bwd = 0.0; n_stream = 0
    with np.errstate(all="ignore"):
        for task in tasks:
            ii_task = np.where(np.isin(ytr, task))[0]
            theta_task_start = net.flat().copy(); si_omega[:] = 0; task_w_start.append(len(wlog))
            for _ep in range(epochs):
                perm = rng.permutation(ii_task)
                for t in range(0, len(perm), BS):
                    ii = perm[t:t + BS]; x, y = Xtr[ii], ytr[ii]; m = len(y); n_stream += m
                    L_p, g_p = ce_loss_grad(net, x, y); fwd_bwd += 3 * m
                    g_q = None; L_q = None
                    if method == "ewc" and theta_star is not None:
                        dth = net.flat() - theta_star; L_q = float((importance * dth ** 2).sum()); g_q = 2 * importance * dth
                    elif method in ("si", "mas") and theta_star is not None:
                        dth = net.flat() - theta_star; L_q = float((importance * dth ** 2).sum()); g_q = 2 * importance * dth
                    elif method == "er" and nb > 0:
                        jj = rng.integers(0, nb, m); L_q, g_q = ce_loss_grad(net, bufx[jj], bufy[jj]); fwd_bwd += 3 * m
                    elif method == "derpp" and nb > 0:
                        jj = rng.integers(0, nb, m); rx, ry, rz = bufx[jj], bufy[jj], bufz[jj]
                        L_b, g_b = ce_loss_grad(net, rx, ry); g_p = g_p + DERPP_BETA * g_b; L_p = L_p + DERPP_BETA * L_b
                        hid, z = net.forward(rx); L_q = float(((z - rz) ** 2).mean()); g_q = net.back(rx, 2 * (z - rz) / (m * K), hid)
                        fwd_bwd += 6 * m
                    elif method == "lwf" and prev is not None:
                        hid, z = net.forward(x); zp = prev.forward(x)[1]
                        q, qp = softmax(z / LWF_T), softmax(zp / LWF_T)
                        L_q = float(LWF_T ** 2 * (qp * (np.log(qp + 1e-300) - np.log(q + 1e-300))).sum(1).mean())
                        g_q = net.back(x, LWF_T * (q - qp) / m, hid); fwd_bwd += 4 * m
                    theta_before = net.flat()
                    if g_q is None:
                        net.set_flat(theta_before - LR * g_p)
                    else:
                        if mode in ("fixed", "reduction"):        # reduction: fixed w at the median derived w
                            wp, w = 1.0, value
                        elif mode == "eq":
                            ema_p = g_p if ema_p is None else smooth * ema_p + (1 - smooth) * g_p
                            ema_q = g_q if ema_q is None else smooth * ema_q + (1 - smooth) * g_q
                            wp = 1.0; w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), DEN_FLOOR), wcap)
                        elif mode == "agem":
                            dot = float(g_p @ g_q)
                            wp = 1.0; w = (-dot / max(float(g_q @ g_q), DEN_FLOOR)) if dot < 0 else 0.0
                        elif mode == "gradnorm":
                            # GradNorm (Chen et al. 2018), alpha = 0: weighted gradient norms driven to their
                            # mean by gradient descent on |G_i - mean G|, weights renormalised to sum 2.
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
                        wlog.append(w)
                        net.set_flat(theta_before - LR * (wp * g_p + w * g_q))
                    if method == "si":
                        si_omega += -g_p * (net.flat() - theta_before)
                    if method in ("er", "derpp"):                      # reservoir buffer (with logits for DER++)
                        for k in range(m):
                            seen += 1
                            if nb < BUF: j = nb; nb += 1
                            else:
                                j = rng.integers(seen)
                                if j >= BUF: continue
                            bufx[j] = x[k]; bufy[j] = y[k]
                            if method == "derpp": bufz[j] = net.forward(x[k:k + 1])[1][0]
            # task boundary
            prev = net.copy(); theta_now = net.flat().copy()
            if method == "ewc":
                f = np.zeros(n)
                for _ in range(N_FISHER):
                    ii = ii_task[rng.integers(0, len(ii_task), BS)]; f += ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
                importance = importance + f / N_FISHER * BS
            elif method == "si":
                importance = importance + np.maximum(si_omega, 0) / ((theta_now - theta_task_start) ** 2 + SI_XI)
            elif method == "mas":
                imp = np.zeros(n)
                for _ in range(N_FISHER):
                    ii = ii_task[rng.integers(0, len(ii_task), BS)]; hid, z = net.forward(Xtr[ii]); imp += np.abs(net.back(Xtr[ii], 2 * z / BS, hid))
                importance = importance + imp / N_FISHER
            if method in ("ewc", "si", "mas"):
                theta_star = theta_now
    late = []
    for a, b in zip(task_w_start, task_w_start[1:] + [len(wlog)]):
        if b > a: late.extend(wlog[a + int((1 - LATE_FRAC) * (b - a)):b])
    return dict(method=method, mode=mode, value=value, seed=seed, smooth=smooth, wcap=wcap, hid=hid, epochs=epochs,
                acc=100 * net.acc(Xte, yte), w_med=float(np.median(wlog)) if wlog else None,
                w_late_med=float(np.median(late)) if late else None,
                w_cap_frac=float(np.mean(np.array(wlog) >= wcap)) if wlog else None,
                fwd_bwd_per_sample=fwd_bwd / max(n_stream, 1), n_stream=int(n_stream), finite=bool(np.all(np.isfinite(net.flat()))))


# ---------------------------------------------------------------- arms
def arms_stage1():
    """Everything except the EWC refinement, the reduction arms and the diagnostic regime."""
    for w in EWC_COARSE: yield ("ewc", "fixed", w, SMOOTH, WCAP)
    for om in OMEGA_GRID: yield ("ewc", "eq", om, SMOOTH, WCAP)
    for cap in SENS_CAP:
        for sm in SENS_SMOOTH:
            if (cap, sm) != (WCAP, SMOOTH): yield ("ewc", "eq", 1.0, sm, cap)
    for mode in ("agem", "gradnorm", "mega"): yield ("ewc", mode, 0.0, SMOOTH, WCAP)
    for w in ER_GRID: yield ("er", "fixed", w, SMOOTH, WCAP)
    yield ("er", "eq", 1.0, SMOOTH, WCAP)
    for meth, default in (("derpp", DERPP_ALPHA_DEFAULT), ("lwf", LWF_DEFAULT)):
        for w in sorted(set(CONSTRAINT_GRID) | {default}): yield (meth, "fixed", w, SMOOTH, WCAP)
        for om in OMEGA_GRID: yield (meth, "eq", om, SMOOTH, WCAP)
    for meth in ("si", "mas"):
        for w in CONSTRAINT_GRID: yield (meth, "fixed", w, SMOOTH, WCAP)
        yield (meth, "eq", 1.0, SMOOTH, WCAP)


def key(o): return (o["method"], o["mode"], round(o["value"], 6), o["smooth"], o["wcap"], o.get("regime", "std"), o.get("hid", HID), o.get("epochs", EPOCHS))


def run_all(name, data_std, data_x4, K, per_task, meta, out):
    hdr = dict(dataset=name, **meta, K=K, per_task=per_task, n_train=int(len(data_std[1])), n_test=int(len(data_std[3])),
               lr=LR, bs=BS, hid=HID, epochs=EPOCHS, buf=BUF, smooth=SMOOTH, wcap=WCAP, den_floor=DEN_FLOOR,
               n_fisher=N_FISHER, si_xi=SI_XI, derpp_beta=DERPP_BETA, lwf_T=LWF_T, x4=X4, uv_lock_sha256=sha256(ROOT / "uv.lock"))
    print(json.dumps(hdr), file=out, flush=True)
    done = {}

    def go(method, mode, value, sm, cap, regime="std", hid=HID, epochs=EPOCHS):
        data = data_std if regime == "std" else data_x4
        for seed in SEEDS:
            o = run(method, mode, value, seed, *data, K, per_task, smooth=sm, wcap=cap, hid=hid, epochs=epochs)
            o["dataset"] = name; o["regime"] = regime; print(json.dumps(o), file=out, flush=True)
            done.setdefault(key(o), []).append(o["acc"])

    for a in arms_stage1(): go(*a)
    # stage 2: EWC refinement at sqrt2 spacing around the coarse best (pre-registered tuning rule)
    best = max(EWC_COARSE, key=lambda w: np.mean(done[("ewc", "fixed", round(w, 6), SMOOTH, WCAP, "std", HID, EPOCHS)]))
    for f in EWC_REFINE:
        w = round(best * f, 6)
        if all(abs(w - c) / c > 1e-6 for c in EWC_COARSE): go("ewc", "fixed", w, SMOOTH, WCAP)
    # reduction arms: fixed w at the median derived weight of the Omega = 1 run (EWC and ER)
    for meth in ("ewc", "er"):
        wm = float(np.median([json.loads(l)["w_med"] for l in open(out.name) if l.startswith("{") and json.loads(l).get("method") == meth
                              and json.loads(l).get("mode") == "eq" and json.loads(l).get("value") == 1.0 and json.loads(l).get("smooth") == SMOOTH
                              and json.loads(l).get("wcap") == WCAP and json.loads(l).get("regime") == "std"]))
        go(meth, "reduction", round(wm, 6), SMOOTH, WCAP)
    # diagnostic regime x4 (EQ2-8, report only): EWC coarse grid, rule at Omega = 1, reduction arm
    for w in EWC_COARSE: go("ewc", "fixed", w, SMOOTH, WCAP, "x4")
    go("ewc", "eq", 1.0, SMOOTH, WCAP, "x4")
    wm = float(np.median([json.loads(l)["w_med"] for l in open(out.name) if l.startswith("{") and json.loads(l).get("method") == "ewc"
                          and json.loads(l).get("mode") == "eq" and json.loads(l).get("value") == 1.0 and json.loads(l).get("regime") == "x4"]))
    go("ewc", "reduction", round(wm, 6), SMOOTH, WCAP, "x4")
    # EQ2R-A: capacity x epochs array (registered carrier only): EWC coarse grid and the rule at Omega = 1 per cell
    if name == ARRAY_CARRIER:
        for hid, ep in ARRAY_CELLS:
            for w in EWC_COARSE: go("ewc", "fixed", w, SMOOTH, WCAP, "std", hid, ep)
            go("ewc", "eq", 1.0, SMOOTH, WCAP, "std", hid, ep)


# ---------------------------------------------------------------- scoring (EQ2-0..8, as in PREREG.md)
def score(paths):
    rows = []
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "acc" in o: rows.append(o)
    ds = sorted(set(r["dataset"] for r in rows))

    def A(name, method, mode, value=None, sm=SMOOTH, cap=WCAP, regime="std", hid=HID, epochs=EPOCHS, field="acc"):
        v = sorted([r for r in rows if r["dataset"] == name and r["method"] == method and r["mode"] == mode and r["regime"] == regime
                    and (value is None or abs(r["value"] - value) < 1e-6) and r["smooth"] == sm and r["wcap"] == cap
                    and r.get("hid", HID) == hid and r.get("epochs", EPOCHS) == epochs], key=lambda r: r["seed"])
        assert len(v) == len(SEEDS), (name, method, mode, value, sm, cap, regime, hid, epochs, [r["seed"] for r in v])
        return np.array([r[field] for r in v], dtype=float)

    def grid(name, method, regime="std", hid=HID, epochs=EPOCHS):
        ws = sorted(set(round(r["value"], 6) for r in rows if r["dataset"] == name and r["method"] == method and r["mode"] == "fixed" and r["regime"] == regime
                        and r.get("hid", HID) == hid and r.get("epochs", EPOCHS) == epochs))
        return {w: A(name, method, "fixed", w, regime=regime, hid=hid, epochs=epochs) for w in ws}

    def fmt(x): return f"{x.mean():.4f} [" + " ".join(f"{q:.2f}" for q in x) + "]"

    print("=" * 112); print("EQ2R scoring (replication of EQ2 + arrays C, D, A) — per-seed values in brackets (seeds 0-4); thresholds from prereg/eq2r/PREREG.md"); print("=" * 112)
    R = {}
    for name in ds:
        R[name] = {}
        g = grid(name, "ewc"); tuned = max(g, key=lambda w: g[w].mean()); tv = g[tuned]
        se = tv.std(ddof=1) / math.sqrt(len(tv)); step = max(1.0, 2 * se)
        eq = {om: A(name, "ewc", "eq", om) for om in OMEGA_GRID}
        red = A(name, "ewc", "reduction"); wm = [r for r in rows if r["dataset"] == name and r["method"] == "ewc" and r["mode"] == "reduction" and r["regime"] == "std"][0]["value"]
        print(f"\n[{name}]  resolvable step = max(1.0, 2*SE) = {step:.4f}  (tuned-lambda SE {se:.4f})")
        print(f"   EWC fixed-lambda grid: " + "  ".join(f"{w:g}:{g[w].mean():.2f}" for w in g))
        print(f"   EWC tuned lambda = {tuned:g}: {fmt(tv)}")
        for om in OMEGA_GRID: print(f"   EWC rule Ω={om:<4}: {fmt(eq[om])}   Ω − tuned: {eq[om].mean()-tv.mean():+.4f}")
        print(f"   EWC reduction arm (fixed w = median derived {wm:g}): {fmt(red)}   rule(Ω=1) − reduction: {eq[1.0].mean()-red.mean():+.4f}")
        d1 = eq[1.0] - tv
        R[name].update(step=step, tuned=tuned, tv=tv, eq=eq, d1=d1, red=red, wm=wm, g=g)
        # sensitivity cells
        sens = {}
        for cap in SENS_CAP:
            for sm in SENS_SMOOTH:
                sens[(cap, sm)] = A(name, "ewc", "eq", 1.0, sm, cap).mean() - tv.mean()
        print("   sensitivity (Ω=1 − tuned): " + "  ".join(f"cap{cap:g}/sm{sm}:{v:+.2f}" for (cap, sm), v in sens.items()))
        R[name]["sens"] = sens
        # baselines
        for mode in ("agem", "gradnorm", "mega"):
            b = A(name, "ewc", mode, 0.0); R[name][mode] = b
            print(f"   EWC baseline {mode:8s}: {fmt(b)}   rule(Ω=1) − baseline: {eq[1.0].mean()-b.mean():+.4f}")
        # ER control
        ge = grid(name, "er"); bt = max(ge, key=lambda w: ge[w].mean()); ere = A(name, "er", "eq", 1.0); err = A(name, "er", "reduction")
        R[name].update(er_best=bt, er_bestv=ge[bt], er_eq=ere, er_red=err)
        print(f"   ER-sum grid: " + "  ".join(f"{w:g}:{ge[w].mean():.2f}" for w in ge) + f"; rule Ω=1: {fmt(ere)}  rule − best fixed: {ere.mean()-ge[bt].mean():+.4f}; reduction arm: {fmt(err)}  rule − reduction: {ere.mean()-err.mean():+.4f}")
        # constraint controls
        for meth in ("derpp", "lwf"):
            gc = grid(name, meth); tc = max(gc, key=lambda w: gc[w].mean()); eqc = {om: A(name, meth, "eq", om) for om in OMEGA_GRID}
            bo = max(eqc, key=lambda o: eqc[o].mean()); R[name][meth] = (tc, gc[tc], bo, eqc[bo])
            print(f"   {meth:5s} tuned w={tc:g}: {fmt(gc[tc])}; rule best Ω={bo}: {fmt(eqc[bo])}  best-Ω − tuned: {eqc[bo].mean()-gc[tc].mean():+.4f}; Ω=1 − tuned: {eqc[1.0].mean()-gc[tc].mean():+.4f}")
        for meth in ("si", "mas"):
            gc = grid(name, meth); tc = max(gc, key=lambda w: gc[w].mean()); e1 = A(name, meth, "eq", 1.0); R[name][meth] = (tc, gc[tc], e1)
            print(f"   {meth:5s} tuned w={tc:g}: {fmt(gc[tc])}; rule Ω=1: {fmt(e1)}  Ω=1 − tuned: {e1.mean()-gc[tc].mean():+.4f}")
        # x4 diagnostic
        gx = grid(name, "ewc", "x4"); tx = max(gx, key=lambda w: gx[w].mean()); ex = A(name, "ewc", "eq", 1.0, regime="x4"); rx = A(name, "ewc", "reduction", regime="x4")
        R[name]["x4"] = (tx, gx[tx], ex, rx)
        print(f"   x4 regime: tuned lambda={tx:g}: {fmt(gx[tx])}; rule Ω=1: {fmt(ex)}  Ω=1 − tuned: {ex.mean()-gx[tx].mean():+.4f}; reduction: {fmt(rx)}")

    n = len(ds); print("\n" + "-" * 112)
    # EQ2-0 precondition
    lams = [R[d]["tuned"] for d in ds]; span = max(lams) / min(lams); decidable = span >= 10
    print(f"EQ2R-0 precondition: tuned lambda per carrier {dict(zip(ds, lams))}, span {span:.2f}x -> {'DECIDABLE' if decidable else 'NOT DECIDABLE: tuned lambda did not move >= 10x'}")
    # EQ2-1
    not_behind = {d: R[d]["d1"].mean() > -R[d]["step"] for d in ds}
    common = max(EWC_COARSE, key=lambda w: np.mean([R[d]["g"][w].mean() for d in ds]))
    loss_common = {d: R[d]["tv"].mean() - R[d]["g"][common].mean() for d in ds}
    single_transfers = all(loss_common[d] < R[d]["step"] for d in ds)
    v1 = all(not_behind.values()) and not single_transfers
    print(f"EQ2R-1 H-EQ2: Ω=1 − tuned per carrier " + ", ".join(f"{d}:{R[d]['d1'].mean():+.4f} (step {R[d]['step']:.2f}; seeds not behind {int((R[d]['d1'] > -R[d]['step']).sum())}/5)" for d in ds)
          + f"; best single lambda={common:g} loses " + ", ".join(f"{d}:{loss_common[d]:.4f}" for d in ds)
          + f" -> {'PASS' if v1 else 'FAIL'}" + ("" if decidable else " (reported without verdict: EQ2-0 not decidable)"))
    # EQ2-2
    reduces = all(abs(R[d]["eq"][1.0].mean() - R[d]["red"].mean()) < R[d]["step"] for d in ds)
    print(f"EQ2R-2 reduction: rule − fixed@median per carrier " + ", ".join(f"{d}:{R[d]['eq'][1.0].mean()-R[d]['red'].mean():+.4f}" for d in ds)
          + f" -> {'REDUCES to a per-carrier constant' if reduces else 'DOES NOT REDUCE: normalised-gradient method'}")
    # EQ2-3
    c3 = all((R[d]["er_eq"].mean() - R[d]["er_bestv"].mean()) < R[d]["step"] and abs(R[d]["er_eq"].mean() - R[d]["er_red"].mean()) < R[d]["step"] for d in ds)
    print(f"EQ2R-3 control ER-sum: rule − best fixed " + ", ".join(f"{d}:{R[d]['er_eq'].mean()-R[d]['er_bestv'].mean():+.4f}" for d in ds)
          + "; rule − reduction " + ", ".join(f"{d}:{R[d]['er_eq'].mean()-R[d]['er_red'].mean():+.4f}" for d in ds) + f" -> {'holds' if c3 else 'VIOLATED'}")
    # EQ2-4
    c4 = all((R[d][m][3].mean() - R[d][m][1].mean()) <= -R[d]["step"] for d in ds for m in ("derpp", "lwf"))
    print("EQ2R-4 control DER++/LwF: best-Ω − tuned " + ", ".join(f"{d}/{m}:{R[d][m][3].mean()-R[d][m][1].mean():+.4f}" for d in ds for m in ("derpp", "lwf")) + f" -> {'holds' if c4 else 'VIOLATED'}")
    # EQ2-5
    print("EQ2R-5 diagnostic SI/MAS: Ω=1 − tuned " + ", ".join(f"{d}/{m}:{R[d][m][2].mean()-R[d][m][1].mean():+.4f}" for d in ds for m in ("si", "mas")) + " (report only)")
    # EQ2-6
    best_o = {d: max(OMEGA_GRID, key=lambda o: R[d]["eq"][o].mean()) for d in ds}
    v6 = all(best_o[d] in (0.71, 1.0, 1.41) for d in ds)
    print(f"EQ2R-6 Ω plateau: best Ω per carrier {best_o} -> {'PASS' if v6 else 'FAIL'}")
    # EQ2-7
    dom = {m: all((R[d][m].mean() - R[d]["eq"][1.0].mean()) >= R[d]["step"] for d in ds) for m in ("agem", "gradnorm", "mega")}
    print("EQ2R-7 published baselines vs rule(Ω=1): " + ", ".join(f"{d}/{m}:{R[d][m].mean()-R[d]['eq'][1.0].mean():+.4f}" for d in ds for m in ("agem", "gradnorm", "mega"))
          + " -> " + ("; ".join(f"{m} dominates the rule" for m, v in dom.items() if v) or "no published baseline is ahead of the rule by a step on every carrier"))
    # sensitivity: fragile?
    flips = sum(1 for d in ds for (cap, sm), v in R[d]["sens"].items() if (v > -R[d]["step"]) != not_behind[d])
    print(f"sensitivity: EQ2-1 'not behind' flips in {flips} of {9*n} cells -> {'FRAGILE' if flips > 1 else 'not fragile'}")
    # EQ2-8
    print("EQ2R-8 diagnostic x4 regime: Ω=1 − tuned " + ", ".join(f"{d}:{R[d]['x4'][2].mean()-R[d]['x4'][1].mean():+.4f} (tuned {R[d]['x4'][0]:g})" for d in ds) + " (report only)")
    print(f"controls: {'all hold' if (c3 and c4) else 'a control is VIOLATED: the mechanism statement is falsified'}")
    # EQ2R-C: the cap as a primary axis. Prediction: at every cap >= the carrier's tuned lambda the rule is not behind by a step;
    # at every cap < the tuned lambda it is behind (the cap turns the rule into a weaker fixed weight).
    okC = True; parts = []
    for d in ds:
        for cap in SENS_CAP:
            delta = A(d, "ewc", "eq", 1.0, SMOOTH, cap).mean() - R[d]["tv"].mean(); nb = delta > -R[d]["step"]; pred = cap >= R[d]["tuned"]
            okC = okC and (nb == pred); parts.append(f"{d}/cap{cap:g}:{delta:+.2f}({'nb' if nb else 'behind'}; predicted {'nb' if pred else 'behind'})")
    print("EQ2R-C cap axis (Omega=1 - tuned at each cap; nb = not behind by a step): " + ", ".join(parts) + f" -> {'PASS' if okC else 'FAIL'}")
    # EQ2R-D: the empty-present diagnostic (report only): the derived weight over the last 20 % of each task's steps at Omega = 1
    partsD = []
    for d in ds:
        wl = A(d, "ewc", "eq", 1.0, field="w_late_med"); wm_ = A(d, "ewc", "eq", 1.0, field="w_med")
        partsD.append(f"{d}: late-w median {np.median(wl):.4g} vs whole-run median {np.median(wm_):.4g} (ratio {np.median(wl) / max(np.median(wm_), 1e-12):.3f}; seeds with late-w < 1: {int((wl < 1).sum())}/5)")
    print("EQ2R-D empty-present diagnostic: " + "; ".join(partsD) + " (report only)")
    # EQ2R-A: capacity x epochs array on the registered carrier: not behind in >= 3 of 4 cells
    if ARRAY_CARRIER in ds:
        cells = [(HID, EPOCHS)] + list(ARRAY_CELLS); nbA = 0; partsA = []
        for hid, ep in cells:
            g_ = grid(ARRAY_CARRIER, "ewc", hid=hid, epochs=ep); tuned_ = max(g_, key=lambda w: g_[w].mean()); tv_ = g_[tuned_]
            step_ = max(1.0, 2 * tv_.std(ddof=1) / math.sqrt(len(tv_))); e1 = A(ARRAY_CARRIER, "ewc", "eq", 1.0, hid=hid, epochs=ep)
            nb = (e1.mean() - tv_.mean()) > -step_; nbA += nb
            partsA.append(f"hid{hid}/ep{ep}: tuned {tuned_:g} -> {tv_.mean():.2f}, rule {e1.mean():.2f}, diff {e1.mean() - tv_.mean():+.2f} (step {step_:.2f}) {'nb' if nb else 'behind'}")
        print(f"EQ2R-A capacity x epochs on {ARRAY_CARRIER}: " + "; ".join(partsA) + f" -> not behind in {nbA}/4 cells -> {'PASS' if nbA >= 3 else 'FAIL'}")
    # replication verdict (PASS-2 candidate): EQ2R-1 PASS, not fragile, controls hold
    print(f"replication summary: EQ2R-1 {'PASS' if v1 else 'FAIL'}; fragile: {flips > 1}; controls hold: {c3 and c4}; cap axis: {'PASS' if okC else 'FAIL'}")


# ---------------------------------------------------------------- main
def _load(name, regime="std"):
    K, per_task = DATASETS.get(name, (10, 2))
    X, y, meta = load_pmlb(name, K)
    assert meta["classes_in_file"] >= K, (name, meta)
    return split_standardise(X, y, K, regime), K, per_task, meta


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        rng = np.random.default_rng(0); K = 10
        X = rng.standard_normal((1500, 20)); y = rng.integers(0, K, 1500); X[np.arange(1500), y % 20] += 3.0
        data = split_standardise(X, y, K)
        for a in (("ewc", "fixed", 10.0), ("ewc", "eq", 1.0), ("ewc", "agem", 0.0), ("ewc", "gradnorm", 0.0), ("ewc", "mega", 0.0),
                  ("er", "fixed", 1.0), ("er", "eq", 1.0), ("derpp", "fixed", 0.1), ("derpp", "eq", 1.0), ("lwf", "fixed", 1.0), ("lwf", "eq", 1.0),
                  ("si", "fixed", 0.1), ("si", "eq", 1.0), ("mas", "fixed", 0.1), ("mas", "eq", 1.0)):
            print(json.dumps(run(*a, 0, *data, K, 2)))
    elif cmd == "run":
        name, method, mode, value, seed = sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]), int(sys.argv[6])
        regime = sys.argv[sys.argv.index("--regime") + 1] if "--regime" in sys.argv else "std"
        data, K, per_task, meta = _load(name, regime)
        o = run(method, mode, value, seed, *data, K, per_task); o["dataset"] = name; o["regime"] = regime; print(json.dumps(o))
    elif cmd == "all":
        name = sys.argv[2]
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/eq2r/results_{name}.jsonl"
        data_std, K, per_task, meta = _load(name, "std"); data_x4, _, _, _ = _load(name, "x4")
        with open(outp, "w") as out:
            run_all(name, data_std, data_x4, K, per_task, meta, out)
    elif cmd == "score":
        score(sys.argv[2:])
    else:
        raise SystemExit(__doc__)
