"""Study BAYES-1 — the normalised penalty step against the EXACT sequential Bayes posterior, on unseen PMLB regression
streams with a random-feature readout (owner request 2026-09-22, prompt-log entries 75 and 84; prereg/bayes1/PREREG.md).

The model is Bayesian linear regression on fixed random features phi(x) = [1, tanh(W x + b)] (W, b fixed by seed 12345),
whitened on the stream's training rows, Gaussian noise variance SIGMA2 = 1 on standardised targets, prior N(0, I / ALPHA). Its sequential posterior after chunk k
is exact: Lambda_k = Lambda_{k-1} + Phi_k' Phi_k / SIGMA2, mu_k = Lambda_k^-1 (Lambda_{k-1} mu_{k-1} + Phi_k' y_k / SIGMA2).
The stream: rows sorted by feature column 0 (covariate drift), K chunks by rank, a fixed 20 % test split per chunk.

Every arm is SGD on the readout theta with  g = g_present + w * g_past,  present = mean squared error on the batch,
past = the exact Laplace penalty of everything before the chunk in per-sample units:
    P(theta) = (c / (2 n_k)) (theta - theta*)' Lambda_{k-1} (theta - theta*),   theta* = the arm's OWN endpoint after chunk k-1
(chunk 1's past is the prior, Lambda_0 = ALPHA I, theta* = 0). c is the CALIBRATION of the curvature: c = 1 is the exact
Fisher, c = 16 and 1/16 are miscalibrated by a scale. With c = 1 and w = 1 the arm run to convergence reproduces the exact
posterior chunk by chunk (the Bayes arm); every other arm is measured by its distance from that posterior in the posterior's
own metric:  d = sqrt( (theta - mu_K)' Lambda_K (theta - mu_K) / D )   (posterior standard deviations per dimension).
  mode 'fixed'     w = value (lambda); lambda = 1 at c = 1 is the Bayes arm
  mode 'eq'        w = value * |ema g_present| / |ema g_past|  (Omega = value; the registered estimator: smooth 0.9, cap 1e4, floor 1e-12)
  mode 'reduction' w = value = the median derived weight of the Omega = 1 run at c = 1
Rows B0..B6 (PREREG.md). Commands:
    uv run python studies/bayes1/bayes1_score.py gate                  # the study's gate on synthetic streams (R4), pinned
    uv run python studies/bayes1/bayes1_score.py smoke                 # every branch once on a synthetic stream, pinned
    uv run python studies/bayes1/bayes1_score.py all <dataset> [--out F]
    uv run python studies/bayes1/bayes1_score.py score <results.jsonl ...>
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
import numpy as np  # noqa: E402

_HERE = Path(__file__).resolve()
ROOT = _HERE.parents[3] if _HERE.parent.name == "frozen" else _HERE.parents[2]
RAW = ROOT / "data" / "raw" / "pmlb"

# ---------------------------------------------------------------- registered constants
M_HID = 30; FEAT_SEED = 12345; WHITEN_EPS = 1e-3; SPLIT_SEED = 12345; SIGMA2 = 1.0; ALPHA = 1.0
K_CHUNKS = 5; TEST_FRAC = 0.2; MAX_ROWS = 5000; SUBSAMPLE_SEED = 777
LR_FRAC = 0.5; BS = 10; EPOCHS = 50                                   # lr per carrier = learning_rate(chunks)
SMOOTH = 0.9; WCAP = 1e4; DEN_FLOOR = 1e-12
FIXED_GRID = (0.0625, 0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0)
OMEGA_GRID = (0.25, 0.35, 0.5, 0.71, 1.0, 1.41, 2.0, 2.83, 4.0)
CALIB = (1.0 / 16.0, 1.0, 16.0)
SEEDS = (0, 1, 2, 3, 4)
SENS_CAP = (10.0, 100.0, 1e4); SENS_SMOOTH = (0.8, 0.9, 0.98)
STEP_FLOOR = 0.05                                                     # the resolvable step in posterior-sd units: max(STEP_FLOOR, 2 SE)
B0_TOL = 0.1                                                          # precondition: the Bayes arm within B0_TOL posterior sd of the exact posterior
DATASETS = ("503_wind", "529_pollen", "197_cpu_act", "225_puma8NH", "537_houses", "201_pol")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- data
def load_pmlb_regression(name: str):
    p = RAW / f"{name}.tsv.gz"
    with gzip.open(p, "rt") as f:
        header = f.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    ti = header.index("target")
    X = np.array([[float(v) for j, v in enumerate(r) if j != ti] for r in rows], np.float64)
    y = np.array([float(r[ti]) for r in rows])
    nan = int((np.isnan(X).any(1) | np.isnan(y)).sum())
    if nan:
        keep = ~(np.isnan(X).any(1) | np.isnan(y)); X, y = X[keep], y[keep]
    n_file = int(len(y))
    if len(y) > MAX_ROWS:                                             # random subsample once, before sorting (pre-registered)
        pick = np.sort(np.random.default_rng(SUBSAMPLE_SEED).permutation(len(y))[:MAX_ROWS]); X, y = X[pick], y[pick]
    return X, y, dict(file=str(p.relative_to(ROOT)), sha256=sha256(p), n=int(len(y)), n_file=n_file, d=int(X.shape[1]), rows_dropped_nan=nan)


def make_stream(X, y, K=K_CHUNKS):
    """Sort by feature column 0 (ties by index), K chunks by rank; fixed 20 % test split per chunk; standardise features and
    targets on chunk 1's training rows; random features. Returns chunks [(Phi_tr, y_tr, Phi_te, y_te)]."""
    order = np.lexsort((np.arange(len(y)), X[:, 0])); X, y = X[order], y[order]
    rng = np.random.default_rng(SPLIT_SEED); bounds = np.linspace(0, len(y), K + 1).astype(int)
    parts = []
    for k in range(K):
        idx = np.arange(bounds[k], bounds[k + 1]); te = np.zeros(len(idx), bool); te[rng.permutation(len(idx))[:int(round(TEST_FRAC * len(idx)))]] = True
        parts.append((idx[~te], idx[te]))
    tr0 = parts[0][0]; mu = X[tr0].mean(0); sd = X[tr0].std(0); sd[sd == 0] = 1.0; ym = y[tr0].mean(); ys = y[tr0].std() or 1.0
    Z = (X - mu) / sd; t = (y - ym) / ys
    frng = np.random.default_rng(FEAT_SEED); W = frng.standard_normal((Z.shape[1], M_HID)) / math.sqrt(Z.shape[1]); b = frng.uniform(-1, 1, M_HID)
    Hd = np.tanh(Z @ W + b)
    # whitening on the stream's training rows (registered): random tanh features are ill-conditioned (condition numbers of 1e5 in the
    # first draft), and SGD cannot reach the exact posterior in any budget on them; the whitened features have unit covariance
    # on chunk 1 and drift on the later chunks, which is the stream's content
    tr_all = np.concatenate([tr for tr, _ in parts])                       # whitening on the training rows of the whole stream (as EQ3 standardises), never on a test row
    hm = Hd[tr_all].mean(0); C = np.cov(Hd[tr_all] - hm, rowvar=False) + WHITEN_EPS * np.eye(M_HID)
    ev, U = np.linalg.eigh(C); Wh = U @ np.diag(1.0 / np.sqrt(ev)) @ U.T
    Phi = np.concatenate([np.ones((len(t), 1)), (Hd - hm) @ Wh], 1)
    return [(Phi[tr], t[tr], Phi[te], t[te]) for tr, te in parts]


def learning_rate(chunks, frac=LR_FRAC, seed=0):
    """lr = frac / (K * the 95th percentile of the top eigenvalue of a size-BS batch's feature covariance over the stream's training rows), the stability
    edge of the Bayes arm at the last chunk (curvature present + K-1 pasts) with a factor frac of headroom (registered)."""
    Phi = np.concatenate([c[0] for c in chunks]); rng = np.random.default_rng(seed)
    tops = [float(np.linalg.eigvalsh(Phi[ii].T @ Phi[ii] / BS).max()) for ii in (rng.permutation(len(Phi))[:BS] for _ in range(400))]
    return frac / (K_CHUNKS * float(np.quantile(tops, 0.95)))


def exact_posteriors(chunks):
    D = chunks[0][0].shape[1]; Lam = ALPHA * np.eye(D); mu = np.zeros(D); out = [(Lam.copy(), mu.copy())]
    for Phi, t, _, _ in chunks:
        Lam_new = Lam + Phi.T @ Phi / SIGMA2; mu = np.linalg.solve(Lam_new, Lam @ mu + Phi.T @ t / SIGMA2); Lam = Lam_new; out.append((Lam.copy(), mu.copy()))
    return out                                                        # out[k] = posterior after chunk k (out[0] = prior)


# ---------------------------------------------------------------- one arm
def run(mode, value, calib, seed, chunks, posts, lr, smooth=SMOOTH, wcap=WCAP, start_at_posterior=False, epochs=EPOCHS, bs=BS):
    rng = np.random.default_rng(seed); D = chunks[0][0].shape[1]
    theta = np.zeros(D); ema_p = ema_q = None; wlog = []; finite = True
    for k, (Phi, t, _, _) in enumerate(chunks):
        Lam_prev, mu_prev = posts[k]; theta_star = theta.copy(); n_k = len(t)
        if start_at_posterior: theta = mu_prev.copy(); theta_star = mu_prev.copy()   # gate negative control: start each chunk AT the exact posterior
        F = calib * Lam_prev / n_k
        for _ep in range(epochs):
            perm = rng.permutation(n_k)
            for s in range(0, n_k, bs):
                ii = perm[s:s + bs]; ph = Phi[ii]; r = ph @ theta - t[ii]
                g_p = ph.T @ r / len(ii); g_q = F @ (theta - theta_star)
                if mode in ("fixed", "reduction"):
                    w = value
                elif mode == "eq":
                    ema_p = g_p if ema_p is None else smooth * ema_p + (1 - smooth) * g_p
                    ema_q = g_q if ema_q is None else smooth * ema_q + (1 - smooth) * g_q
                    w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), DEN_FLOOR), wcap)
                else:
                    raise ValueError(mode)
                wlog.append(float(w)); theta = theta - lr * (g_p + w * g_q)
                if not np.all(np.isfinite(theta)) or np.linalg.norm(theta) > 1e8:
                    finite = False; break
            if not finite: break
        if not finite: break
    Lam_K, mu_K = posts[-1]
    d = float(math.sqrt(max(float((theta - mu_K) @ Lam_K @ (theta - mu_K)), 0.0) / D)) if finite else float("inf")
    mse = float(np.mean([np.mean((Phi_te @ theta - t_te) ** 2) for _, _, Phi_te, t_te in chunks])) if finite else float("inf")
    rec = dict(mode=mode, value=float(value), calib=float(calib), seed=int(seed), smooth=float(smooth), wcap=float(wcap),
               start_at_posterior=bool(start_at_posterior), lr=float(lr), epochs=int(epochs), d=d, mse=mse, w_med=float(np.median(wlog)) if wlog else None,
               w_cap_frac=float(np.mean(np.array(wlog) >= wcap)) if wlog else None, finite=bool(finite))
    json.dumps(rec); return rec


def arms():
    for c in CALIB:
        for lam in FIXED_GRID: yield ("fixed", lam, c, SMOOTH, WCAP)
        for om in OMEGA_GRID: yield ("eq", om, c, SMOOTH, WCAP)
    for cap in SENS_CAP:
        for sm in SENS_SMOOTH:
            if (cap, sm) != (WCAP, SMOOTH): yield ("eq", 1.0, 1.0, sm, cap)


def run_all(name, chunks, posts, meta, out):
    Lam_K, mu_K = posts[-1]; lr = learning_rate(chunks)
    bayes_mse = float(np.mean([np.mean((Phi_te @ mu_K - t_te) ** 2) for _, _, Phi_te, t_te in chunks]))
    hdr = dict(dataset=name, **meta, K=K_CHUNKS, D=int(chunks[0][0].shape[1]), chunk_sizes=[int(len(c[1])) for c in chunks], sigma2=SIGMA2, alpha=ALPHA,
               lr=lr, lr_frac=LR_FRAC, bs=BS, epochs=EPOCHS, whiten_eps=WHITEN_EPS, m_hid=M_HID, smooth=SMOOTH, wcap=WCAP, calib=list(CALIB), exact_posterior_mse=bayes_mse, uv_lock_sha256=sha256(ROOT / "uv.lock"))
    print(json.dumps(hdr), file=out, flush=True)
    recs = []
    for mode, value, c, sm, cap in arms():
        for seed in SEEDS:
            o = run(mode, value, c, seed, chunks, posts, lr, smooth=sm, wcap=cap); o["dataset"] = name; recs.append(o); print(json.dumps(o), file=out, flush=True)
    wm = float(np.median([o["w_med"] for o in recs if o["mode"] == "eq" and o["value"] == 1.0 and o["calib"] == 1.0 and o["smooth"] == SMOOTH and o["wcap"] == WCAP]))
    for seed in SEEDS:
        o = run("reduction", round(wm, 6), 1.0, seed, chunks, posts, lr); o["dataset"] = name; print(json.dumps(o), file=out, flush=True)


# ---------------------------------------------------------------- scoring
def score(paths):
    rows = []; hdrs = {}
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "mode" in o: rows.append(o)
                elif "dataset" in o: hdrs[o["dataset"]] = o                  # the header also carries a key 'd' (the feature count): classify by 'mode'

    ds = sorted(set(r["dataset"] for r in rows))

    def A(name, mode, value=None, calib=1.0, sm=SMOOTH, cap=WCAP, field="d"):
        v = sorted([r for r in rows if r["dataset"] == name and r["mode"] == mode and abs(r["calib"] - calib) < 1e-9 and (value is None or abs(r["value"] - value) < 1e-6)
                    and r["smooth"] == sm and r["wcap"] == cap], key=lambda r: r["seed"])
        assert len(v) == len(SEEDS), (name, mode, value, calib, sm, cap, [r["seed"] for r in v])
        return np.array([r[field] for r in v], float)

    def fmt(x): return f"{x.mean():.4f} [" + " ".join(f"{q:.3f}" for q in x) + "]"
    def step_of(x): return max(STEP_FLOOR, 2 * float(np.std(x, ddof=1)) / math.sqrt(len(x)))

    print("=" * 112); print("BAYES-1 scoring — distance to the exact sequential posterior in posterior-sd units per dimension; per-seed values in brackets"); print("=" * 112)
    R = {}
    for name in ds:
        h = hdrs.get(name, {}); R[name] = {}
        bay = A(name, "fixed", 1.0, 1.0); eq = {om: A(name, "eq", om, 1.0) for om in OMEGA_GRID}; step = step_of(eq[1.0])
        g = {lam: A(name, "fixed", lam, 1.0) for lam in FIXED_GRID}; tuned = min(g, key=lambda l: g[l].mean())
        red = A(name, "reduction"); wm = [r for r in rows if r["dataset"] == name and r["mode"] == "reduction"][0]["value"]
        print(f"\n[{name}]  n = {h.get('n')} of {h.get('n_file')} rows, d = {h.get('d')} features, D = {h.get('D')} parameters, chunks {h.get('chunk_sizes')}; step = max({STEP_FLOOR}, 2 SE) = {step:.4f}")
        print(f"   Bayes arm (fixed lambda = 1, c = 1): d = {fmt(bay)}   held-out MSE {A(name, 'fixed', 1.0, 1.0, field='mse').mean():.4f} vs exact posterior predictive {h.get('exact_posterior_mse'):.4f}")
        print(f"   fixed-lambda grid at c = 1 (d): " + "  ".join(f"{l:g}:{g[l].mean():.3f}" for l in FIXED_GRID) + f"  -> tuned lambda = {tuned:g}")
        for om in OMEGA_GRID: print(f"   rule Omega = {om:<4} c = 1: d = {fmt(eq[om])}   d − Bayes {eq[om].mean() - bay.mean():+.4f}")
        print(f"   reduction arm (fixed w = median derived {wm:g}): d = {fmt(red)}")
        rows_c = {}
        for c in CALIB:
            fx1 = A(name, "fixed", 1.0, c); e1 = A(name, "eq", 1.0, c); rows_c[c] = (fx1, e1)
            print(f"   calibration c = {c:g}: fixed lambda = 1 (Bayes with this curvature) d = {fmt(fx1)}; rule Omega = 1 d = {fmt(e1)}; held-out MSE fixed {A(name, 'fixed', 1.0, c, field='mse').mean():.4f} rule {A(name, 'eq', 1.0, c, field='mse').mean():.4f}")
        sens = {(cap, sm): A(name, "eq", 1.0, 1.0, sm, cap).mean() - bay.mean() for cap in SENS_CAP for sm in SENS_SMOOTH if (cap, sm) != (WCAP, SMOOTH)}
        print("   sensitivity (rule Omega = 1 − Bayes, d): " + "  ".join(f"cap{cap:g}/sm{sm}:{v:+.3f}" for (cap, sm), v in sens.items()))
        R[name].update(bay=bay, eq=eq, step=step, g=g, tuned=tuned, red=red, c=rows_c, sens=sens)
    n = len(ds); print("\n" + "-" * 112)
    b0 = {d: R[d]["bay"].mean() < B0_TOL for d in ds}
    print(f"B0 precondition (the Bayes arm converges to the exact posterior within {B0_TOL} sd): " + ", ".join(f"{d}:{R[d]['bay'].mean():.4f}" for d in ds) + f" -> {'DECIDABLE' if all(b0.values()) else 'NOT DECIDABLE on ' + str([d for d in ds if not b0[d]])}")
    b1 = {d: (R[d]["eq"][1.0].mean() - R[d]["bay"].mean()) > R[d]["step"] for d in ds}
    print(f"B1 the rule is not Bayes: d(rule Omega = 1) − d(Bayes) " + ", ".join(f"{d}:{R[d]['eq'][1.0].mean() - R[d]['bay'].mean():+.4f} (step {R[d]['step']:.3f})" for d in ds) + f"; beyond a step on {sum(b1.values())}/{n} -> {'PASS' if all(b1.values()) else 'FAIL'}")
    b2 = {c: {d: (R[d]["c"][c][1].mean() - R[d]["c"][c][0].mean()) < -R[d]["step"] for d in ds} for c in (1.0 / 16.0, 16.0)}
    for c in (16.0, 1.0 / 16.0):
        print(f"B2 at c = {c:g}: d(rule) − d(fixed lambda = 1, miscalibrated Bayes) " + ", ".join(f"{d}:{R[d]['c'][c][1].mean() - R[d]['c'][c][0].mean():+.4f}" for d in ds) + f"; rule ahead by a step on {sum(b2[c].values())}/{n} -> {'PASS' if all(b2[c].values()) else 'FAIL'}")
    b3 = {d: all(abs(R[d]["c"][c][1].mean() - R[d]["c"][1.0][1].mean()) < R[d]["step"] for c in (1.0 / 16.0, 16.0)) for d in ds}
    print("B3 scale invariance of the rule: d(rule, c = 16) − d(rule, c = 1) " + ", ".join(f"{d}:{R[d]['c'][16.0][1].mean() - R[d]['c'][1.0][1].mean():+.4f}" for d in ds)
          + "; c = 1/16: " + ", ".join(f"{d}:{R[d]['c'][1.0 / 16.0][1].mean() - R[d]['c'][1.0][1].mean():+.4f}" for d in ds) + f"; within a step on {sum(b3.values())}/{n} -> {'PASS' if all(b3.values()) else 'FAIL'}")
    b4 = {d: abs(R[d]["g"][R[d]["tuned"]].mean() - R[d]["bay"].mean()) < R[d]["step"] for d in ds}
    print("B4 the tuned fixed weight is the Bayes weight (report): tuned lambda " + ", ".join(f"{d}:{R[d]['tuned']:g} (d {R[d]['g'][R[d]['tuned']].mean():.4f} vs Bayes {R[d]['bay'].mean():.4f})" for d in ds) + f"; within a step of Bayes on {sum(b4.values())}/{n}")
    print("B5 held-out MSE (report): " + "; ".join(f"{d}: exact {hdrs[d]['exact_posterior_mse']:.4f}, Bayes arm {A(d, 'fixed', 1.0, 1.0, field='mse').mean():.4f}, rule {A(d, 'eq', 1.0, 1.0, field='mse').mean():.4f}, tuned {A(d, 'fixed', R[d]['tuned'], 1.0, field='mse').mean():.4f}" for d in ds))
    best_om = {d: min(OMEGA_GRID, key=lambda o: R[d]["eq"][o].mean()) for d in ds}
    widths = {d: sum(1 for o in OMEGA_GRID if R[d]["eq"][o].mean() <= R[d]["eq"][best_om[d]].mean() + R[d]["step"]) for d in ds}
    print(f"B6 Omega plateau in d (report): best Omega {best_om}; points within a step of the best {widths}")
    reduces = {d: abs(R[d]["eq"][1.0].mean() - R[d]["red"].mean()) < R[d]["step"] for d in ds}
    print(f"B7 reduction (report): rule − fixed@median " + ", ".join(f"{d}:{R[d]['eq'][1.0].mean() - R[d]['red'].mean():+.4f}" for d in ds) + f"; reduces on {sum(reduces.values())}/{n}")
    flips = sum(1 for d in ds for v in R[d]["sens"].values() if (v > R[d]["step"]) != b1[d])
    print(f"BS sensitivity: B1 flips in {flips} of {8 * n} cells -> {'FRAGILE' if flips > 1 else 'not fragile'}")
    print(f"summary: B0 {'decidable' if all(b0.values()) else 'not decidable'}; B1 {'PASS' if all(b1.values()) else 'FAIL'}; B2(16) {'PASS' if all(b2[16.0].values()) else 'FAIL'}; B2(1/16) {'PASS' if all(b2[1.0 / 16.0].values()) else 'FAIL'}; B3 {'PASS' if all(b3.values()) else 'FAIL'}; fragile {flips > 1}")


# ---------------------------------------------------------------- synthetic stream, gate and smoke
def synthetic(seed=0, n=2500, d=6, drift=1.5):
    rng = np.random.default_rng(seed); X = rng.standard_normal((n, d)); X[:, 0] = np.sort(X[:, 0]) * 0 + np.linspace(-2, 2, n) + 0.1 * rng.standard_normal(n)
    th = rng.standard_normal(d); y = X @ th + drift * np.sin(2 * X[:, 0]) + 0.5 * rng.standard_normal(n)
    return X, y


def gate():
    """The study's gate (R4), on a synthetic drifting stream. B1's statistic (d(arm) − d(Bayes) beyond a step) must NOT fire on a
    decoy that is Bayes by construction (the Bayes arm run twice as long: a different trajectory to the same posterior) and MUST
    fire on a fixed weight that is not the Bayes weight (lambda = 4). Informational rows, printed and not gated: the rule started
    AT the exact posterior each chunk (does it rest there, as the exact-norm knife edge says, or drift, as the EMA estimator with
    mini-batch noise says?); B2 (the rule against Bayes with a miscalibrated curvature, c = 16 and 1/16) and B3 (the rule's own
    invariance to c) as the surrogate predicts them, so the prereg can state the surrogate's verdict per row."""
    X, y = synthetic(); chunks = make_stream(X, y); posts = exact_posteriors(chunks); lr = learning_rate(chunks)
    def dist(mode, value, c, **kw): return np.array([run(mode, value, c, s, chunks, posts, lr, **kw)["d"] for s in SEEDS])
    bay = dist("fixed", 1.0, 1.0); decoy = dist("fixed", 1.0, 1.0, epochs=2 * EPOCHS); lam4 = dist("fixed", 4.0, 1.0)
    eq1 = dist("eq", 1.0, 1.0); eq1_kn = dist("eq", 1.0, 1.0, start_at_posterior=True); step = max(STEP_FLOOR, 2 * eq1.std(ddof=1) / math.sqrt(len(SEEDS)))
    print(f"gate for BAYES-1 (synthetic drifting stream, d = 6, n = 2500, 5 chunks, {M_HID} whitened random features, lr {lr:.5f}, {EPOCHS} epochs per chunk)")
    print(f"  Bayes arm d = {bay.mean():.4f} (B0: {'converged' if bay.mean() < B0_TOL else 'NOT converged'} within {B0_TOL}); step = {step:.4f}")
    neg1 = (decoy.mean() - bay.mean()) > step; pos1 = (lam4.mean() - bay.mean()) > step
    print(f"  B1 negative control (a second Bayes arm, {2 * EPOCHS} epochs): d = {decoy.mean():.4f}, beyond a step of Bayes: {neg1} -> {'VIOLATION' if neg1 else 'fails as it must'}")
    print(f"  B1 positive control (fixed lambda = 4, not the Bayes weight): d = {lam4.mean():.4f}, beyond a step of Bayes: {pos1} -> {'passes as it must' if pos1 else 'VIOLATION (instrument cannot see the effect)'}")
    print(f"  informational: the rule at Omega = 1, ordinary start d = {eq1.mean():.4f}; started AT the exact posterior each chunk d = {eq1_kn.mean():.4f} -> "
          f"{'it drifts away (the EMA estimator with mini-batch noise does not rest on the knife edge)' if eq1_kn.mean() > step else 'it rests there (the knife edge)'}")
    fx16 = dist("fixed", 1.0, 16.0); eq16 = dist("eq", 1.0, 16.0); fx116 = dist("fixed", 1.0, 1.0 / 16.0); eq116 = dist("eq", 1.0, 1.0 / 16.0)
    b2_16 = (eq16.mean() - fx16.mean()) < -step; b2_116 = (eq116.mean() - fx116.mean()) < -step
    print(f"  informational B2 at c = 16:   fixed lambda = 1 d = {fx16.mean():.4f}, rule d = {eq16.mean():.4f} -> the surrogate says B2 {'PASS' if b2_16 else 'FAIL'}")
    print(f"  informational B2 at c = 1/16: fixed lambda = 1 d = {fx116.mean():.4f}, rule d = {eq116.mean():.4f} -> the surrogate says B2 {'PASS' if b2_116 else 'FAIL'}")
    b3 = abs(eq16.mean() - eq1.mean()) < step and abs(eq116.mean() - eq1.mean()) < step
    print(f"  informational B3: d(rule) at c = 1/16, 1, 16 = {eq116.mean():.4f}, {eq1.mean():.4f}, {eq16.mean():.4f} -> the surrogate says B3 {'PASS' if b3 else 'FAIL'} (the invariance is to the term, not to the mini-batch noise, omega_reprocessed.txt [1])")
    bad = int(neg1) + int(not pos1)
    print("GATE OPEN" if bad == 0 else f"GATE CLOSED ({bad} violation(s))"); return bad


def smoke():
    X, y = synthetic(); chunks = make_stream(X, y); posts = exact_posteriors(chunks); lr = learning_rate(chunks)
    for a in (("fixed", 1.0, 1.0), ("fixed", 0.0625, 16.0), ("eq", 1.0, 1.0), ("eq", 4.0, 1.0 / 16.0), ("reduction", 0.7, 1.0)):
        print(json.dumps(run(*a, 0, chunks, posts, lr)))
    print(json.dumps(run("eq", 1.0, 1.0, 0, chunks, posts, lr, smooth=0.98, wcap=10.0)))
    print(json.dumps(run("eq", 1.0, 1.0, 0, chunks, posts, lr, start_at_posterior=True)))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "gate": sys.exit(1 if gate() else 0)
    elif cmd == "smoke": smoke()
    elif cmd == "all":
        name = sys.argv[2]; outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/bayes1/results_{name}.jsonl"
        X, y, meta = load_pmlb_regression(name); chunks = make_stream(X, y); posts = exact_posteriors(chunks)
        with open(outp, "w") as out: run_all(name, chunks, posts, meta, out)
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/bayes1_smokefull.jsonl"
        X, y = synthetic(); chunks = make_stream(X, y); posts = exact_posteriors(chunks)
        with open(outp, "w") as out: run_all("synthetic", chunks, posts, dict(file="synthetic", sha256="none", n=len(y), n_file=len(y), d=X.shape[1], rows_dropped_nan=0), out)
        score([outp])
    elif cmd == "score": score(sys.argv[2:])
    else: raise SystemExit(__doc__)
