"""Study SEC1 — the Laplace (Bayes) weight on a secant-calibrated Fisher, on the twelve SEEN PMLB carriers of EQ3 and EQ4.
Owner request: prompt-log entry 120 (after entries 111-119); prereg/sec1/PREREG.md. Confirmatory on seen data only (R11):
every carrier was opened in EQ3 (2026-09-22) or EQ4 (2026-09-23); no held-out claim is made.

The calibration (SEC). At the end of every task j the per-sample empirical Fisher f_j (EQ3/EQ4's estimator) is rescaled by
    s_j = c_j / rho_j,   c_j = <dg, dth> / <dth, dth>,   rho_j = <f_j dth, dth> / <dth, dth>
where dth and dg are the differences between the END-window and START-window means of the parameters and of the clean
present-task gradient over task j's own training steps (the start window is the first ceil(FS x steps) steps of the task,
the end window the last ceil(FE x steps)); c_j is the curvature the present loss showed along the path the learner
actually travelled (a secant, as in Barzilai-Borwein), rho_j the curvature the Fisher claims along the same path. If
|dth|^2 <= 1e-12, c_j <= 0 or rho_j <= 0, s_j = 1 and the task is counted as a fallback (reported, never excluded).

Arms (online EWC; network, optimiser, data handling and Fisher estimator exactly those of EQ4):
  mode 'fixed'      w = value on the accumulated raw Fisher (the tuned-lambda baseline, two-stage grid, in-sample)
  mode 'fixed_sec'  w = value on the accumulated calibrated Fisher (sum s_j f_j), two-stage grid (SEC1-4)
  mode 'bayes'      the Laplace weight w = 1/2 on the task-size-weighted raw Fisher (EQ3/EQ4's Bayes arm)
  mode 'bayes_sec'  the Laplace weight w = 1/2 on the task-size-weighted calibrated Fisher (the arm under test)
  mode 'bayes_s1'   the Laplace weight w = 1/2 with ONE calibration factor, task 1's s, applied to every task (R7: the
                    strongest simple alternative, "fix the units once"; if it equals 'bayes_sec', only a global scale matters)
  mode 'eq'         the registered rule, Omega = value (R7 comparison; EQ2-EQ4's estimator)
Gate (R4): the same run() on a synthetic stream with the Fisher deliberately distorted (per-task units error, global
units error, shape-only noise); see `gate`.

    uv run python studies/sec1/sec1_score.py smoke
    uv run python studies/sec1/sec1_score.py smokefull [--out F]
    uv run python studies/sec1/sec1_score.py gate
    uv run python studies/sec1/sec1_score.py all <dataset> [--out F]
    uv run python studies/sec1/sec1_score.py score <results.jsonl ...>
    uv run python studies/sec1/sec1_score.py run <dataset> <mode> <value> <seed>
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
ROOT = _HERE.parents[3] if _HERE.parent.name == "frozen" else _HERE.parents[2]   # runs/sec1/frozen/ or studies/sec1/
RAW = ROOT / "data" / "raw" / "pmlb"

# ---------------------------------------------------------------- registered constants (PREREG.md)
LR = 0.05; BS = 10; HID = 256; EPOCHS = 3                         # as EQ3/EQ4
SMOOTH = 0.9; WCAP = 1e4; DEN_FLOOR = 1e-12                      # the registered rule's estimator (R7 arm)
N_FISHER = 50; BAYES_W = 0.5
FS = 0.1; FE = 0.1                                                # SEC windows (fractions of the task's steps)
SENS_FS = (0.05, 0.1, 0.2); SENS_FE = (0.05, 0.1, 0.2)            # SEC1-S
DTH_FLOOR = 1e-12
SEEDS = (0, 1, 2, 3, 4)
TEST_FRAC = 0.2
MAX_ROWS = 5000; SUBSAMPLE_SEED = 777; CLASS_FLOOR = 40
EWC_COARSE = (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0)
EWC_REFINE = (1 / 2.83, 1 / 2.0, 1 / 1.41, 1.41, 2.0, 2.83)
SEC_COARSE = (0.01, 0.03) + EWC_COARSE                            # the calibrated arm's grid reaches below 0.1 (its Bayes value is 1/2 x task-size ratio)
DATASETS = {  # PMLB name -> (K requested, classes per task): EQ3's six (K as EQ3) and EQ4's six (K as EQ4), all through EQ4's class-selection rule
    "mfeat_factors": (10, 2), "mfeat_morphological": (10, 2), "led7": (10, 2), "led24": (10, 2), "krkopt": (10, 2), "fars": (8, 2),
    "satimage": (6, 2), "segmentation": (6, 2), "yeast": (6, 2), "wine_quality_white": (4, 2), "sleep": (4, 2), "page_blocks": (4, 2),
}
# thresholds (PREREG.md)
MIN_MISCAL = 3; CLOSE_FRAC = 0.5; CLOSE_SHARE = 2 / 3; TUNING_FREE_MIN = 9; SPAN_FACTOR = 10.0
# gate (R4)
GATE_U_RANGE = 16.0; GATE_GLOBAL = (1 / 16, 16.0); GATE_SHAPE_SD = 1.5; DISTORT_SEED = 4242


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pmlb(name: str, K_req: int):
    """EQ4's loader and class-selection rule, unchanged."""
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


def split_standardise(X, y, K):
    """EQ4's fixed 80/20 stratified split (seed 12345) and standardisation on the training part."""
    rng = np.random.default_rng(12345)
    tr, te = [], []
    for c in range(K):
        idx = rng.permutation(np.where(y == c)[0]); n_te = int(round(TEST_FRAC * len(idx)))
        te.append(idx[:n_te]); tr.append(idx[n_te:])
    tr = np.concatenate(tr); te = np.concatenate(te)
    mu = X[tr].mean(0); sd = X[tr].std(0); sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    return Z[tr], y[tr], Z[te], y[te]


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

    def acc(s, x, y):
        with np.errstate(all="ignore"):
            z = s.forward(x)[1]
        if not np.all(np.isfinite(z)):
            return 0.0
        return float((z.argmax(1) == y).mean())


def softmax(z):
    z = z - z.max(1, keepdims=True); p = np.exp(z); return p / p.sum(1, keepdims=True)


def ce_loss_grad(net, x, y):
    act, z = net.forward(x); p = softmax(z); n = len(y)
    loss = float(-np.log(p[np.arange(n), y] + 1e-300).mean())
    dz = p; dz[np.arange(n), y] -= 1; dz /= n
    return loss, net.back(x, dz, act)


# ---------------------------------------------------------------- one run
def run(mode, value, seed, Xtr, ytr, Xte, yte, K, per_task, fs=FS, fe=FE, distort=None, lr=LR, bs=BS, epochs=EPOCHS, hidden=HID,
        smooth=SMOOTH, wcap=WCAP):
    """distort (gate only): None | ('unit', range) per-task factor log-uniform on [1/range, range] | ('global', U) |
    ('shape', sd) per-parameter factor exp(N(0, sd)), fresh per task. Applied to f_j before accumulation in every mode."""
    rng = np.random.default_rng(seed); drng = np.random.default_rng(DISTORT_SEED + seed)
    d = Xtr.shape[1]; net = MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    importance = np.zeros(n); imp_bayes = np.zeros(n); theta_star = None
    ema_p = ema_q = None; wlog = []; svals = []; cvals = []; rhovals = []; n_fallback = 0
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            imp_used = (imp_bayes / n_task) if mode in ("bayes", "bayes_sec", "bayes_s1") else importance
            total = epochs * int(math.ceil(n_task / bs)); n_s = max(1, int(math.ceil(fs * total))); n_e = max(1, int(math.ceil(fe * total)))
            s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0
            for ep in range(epochs):
                perm = rng.permutation(ii_task)
                for t in range(0, len(perm), bs):
                    ii = perm[t:t + bs]; x, y = Xtr[ii], ytr[ii]
                    L_p, g_p = ce_loss_grad(net, x, y)
                    theta_before = net.flat()
                    if k_step < n_s: s_th += theta_before; s_g += g_p
                    if k_step >= total - n_e: e_th += theta_before; e_g += g_p
                    k_step += 1
                    if theta_star is None:
                        net.set_flat(theta_before - lr * g_p); continue
                    dth = theta_before - theta_star; g_q = 2 * imp_used * dth
                    if mode in ("fixed", "fixed_sec"): w = value
                    elif mode in ("bayes", "bayes_sec", "bayes_s1"): w = BAYES_W
                    elif mode == "eq":
                        ema_p = g_p if ema_p is None else smooth * ema_p + (1 - smooth) * g_p
                        ema_q = g_q if ema_q is None else smooth * ema_q + (1 - smooth) * g_q
                        w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), DEN_FLOOR), wcap)
                    else:
                        raise ValueError(mode)
                    wlog.append(float(w))
                    net.set_flat(theta_before - lr * (g_p + w * g_q))
            theta_now = net.flat().copy()
            f = np.zeros(n)
            for _ in range(N_FISHER):
                ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
            f_task = f / N_FISHER * bs
            if distort is not None:
                kind, par = distort
                if kind == "unit": f_task = f_task * math.exp(drng.uniform(-math.log(par), math.log(par)))
                elif kind == "global": f_task = f_task * par
                elif kind == "shape": f_task = f_task * np.exp(drng.normal(0.0, par, n))
                else: raise ValueError(kind)
            dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)
            c = float(dg @ dth) / nn if nn > DTH_FLOOR else float("nan"); rho = float((f_task * dth) @ dth) / nn if nn > DTH_FLOOR else float("nan")
            if nn > DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho
            else: s = 1.0; n_fallback += 1
            svals.append(float(s)); cvals.append(c if np.isfinite(c) else None); rhovals.append(rho if np.isfinite(rho) else None)
            sc = s if mode in ("fixed_sec", "bayes_sec") else (svals[0] if mode == "bayes_s1" else 1.0)
            importance = importance + sc * f_task; imp_bayes = imp_bayes + n_task * sc * f_task
            theta_star = theta_now
    rec = dict(mode=mode, value=float(value), seed=int(seed), fs=float(fs), fe=float(fe), distort=list(distort) if distort else None,
               lr=float(lr), bs=int(bs), epochs=int(epochs), hidden=int(hidden), acc=100 * net.acc(Xte, yte),
               s=svals, c=cvals, rho=rhovals, n_fallback=int(n_fallback), w_med=float(np.median(wlog)) if wlog else None,
               finite=bool(np.all(np.isfinite(net.flat()))))
    json.dumps(rec)
    return rec


# ---------------------------------------------------------------- arms
def key(o): return (o["mode"], round(o["value"], 6), o["fs"], o["fe"])


def run_all(name, data, K, per_task, meta, out):
    hdr = dict(dataset=name, **meta, K=K, per_task=per_task, n_train=int(len(data[1])), n_test=int(len(data[3])), lr=LR, bs=BS,
               hidden=HID, epochs=EPOCHS, n_fisher=N_FISHER, bayes_w=BAYES_W, fs=FS, fe=FE, smooth=SMOOTH, wcap=WCAP,
               max_rows=MAX_ROWS, subsample_seed=SUBSAMPLE_SEED, uv_lock_sha256=sha256(ROOT / "uv.lock"))
    print(json.dumps(hdr), file=out, flush=True)
    done = {}

    def go(mode, value, fs=FS, fe=FE):
        for seed in SEEDS:
            o = run(mode, value, seed, *data, K, per_task, fs=fs, fe=fe); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True); done.setdefault(key(o), []).append(o["acc"])

    for mode, coarse in (("fixed", EWC_COARSE), ("fixed_sec", SEC_COARSE)):
        for w in coarse: go(mode, w)
        best = max(coarse, key=lambda w: np.mean(done[(mode, round(w, 6), FS, FE)]))
        for fct in EWC_REFINE:
            w = round(best * fct, 6)
            if all(abs(w - c) / c > 1e-6 for c in coarse): go(mode, w)
    go("bayes", 0.0); go("bayes_sec", 0.0); go("bayes_s1", 0.0); go("eq", 1.0)
    for fs in SENS_FS:
        for fe in SENS_FE:
            if (fs, fe) != (FS, FE): go("bayes_sec", 0.0, fs, fe)


# ---------------------------------------------------------------- scoring (SEC1-0..4, R, S, E; PREREG.md)
def step_of(tv): return max(1.0, 2 * float(np.std(tv, ddof=1)) / math.sqrt(len(tv)))


def score(paths):
    rows = []; hdrs = {}
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "acc" in o: rows.append(o)
                elif "dataset" in o: hdrs[o["dataset"]] = o
    ds = [d for d in DATASETS if d in set(r["dataset"] for r in rows)]
    excl = [d for d, h in hdrs.items() if h.get("excluded")]

    def A(name, mode, value=None, fs=FS, fe=FE, field="acc"):
        v = sorted([r for r in rows if r["dataset"] == name and r["mode"] == mode and (value is None or abs(r["value"] - value) < 1e-6)
                    and r["fs"] == fs and r["fe"] == fe], key=lambda r: r["seed"])
        assert len(v) == len(SEEDS), (name, mode, value, fs, fe, [r["seed"] for r in v])
        return np.array([r[field] for r in v], dtype=float) if field != "s" else [r["s"] for r in v]

    def grid(name, mode):
        ws = sorted(set(round(r["value"], 6) for r in rows if r["dataset"] == name and r["mode"] == mode and r["fs"] == FS and r["fe"] == FE))
        return {w: A(name, mode, w) for w in ws}

    def fmt(x): return f"{x.mean():.4f} [" + " ".join(f"{q:.2f}" for q in x) + "]"

    print("=" * 112); print("SEC1 scoring — SEEN carriers (confirmatory only, R11); per-seed values in brackets (seeds 0-4); thresholds from prereg/sec1/PREREG.md"); print("=" * 112)
    R = {}
    for name in ds:
        h = hdrs.get(name, {})
        print(f"\n[{name}]  K = {h.get('classes_used')} of {h.get('classes_in_file')} classes (requested {h.get('classes_requested')}); class counts {h.get('class_counts')}; n = {h.get('n')} of {h.get('n_file')} rows")
        g = grid(name, "fixed"); tuned = max(g, key=lambda w: g[w].mean()); tv = g[tuned]; step = step_of(tv)
        gs = grid(name, "fixed_sec"); tuned_s = max(gs, key=lambda w: gs[w].mean())
        braw = A(name, "bayes", 0.0); bsec = A(name, "bayes_sec", 0.0); bs1 = A(name, "bayes_s1", 0.0); eq = A(name, "eq", 1.0)
        svals = [x for seed_s in A(name, "bayes_sec", 0.0, field="s") for x in seed_s]
        nfb = int(A(name, "bayes_sec", 0.0, field="n_fallback").sum())
        print(f"   resolvable step = max(1.0, 2*SE of the tuned raw-lambda arm) = {step:.4f}")
        print(f"   EWC raw-Fisher lambda grid: " + "  ".join(f"{w:g}:{g[w].mean():.2f}" for w in g))
        print(f"   EWC calibrated-Fisher lambda grid: " + "  ".join(f"{w:g}:{gs[w].mean():.2f}" for w in gs))
        print(f"   tuned lambda (raw) = {tuned:g}: {fmt(tv)}; tuned lambda (calibrated) = {tuned_s:g}: {fmt(gs[tuned_s])}")
        print(f"   Bayes raw (w 1/2): {fmt(braw)}   Bayes raw − tuned: {braw.mean() - tv.mean():+.4f}")
        print(f"   Bayes SEC (w 1/2): {fmt(bsec)}   Bayes SEC − tuned: {bsec.mean() - tv.mean():+.4f}; Bayes SEC − Bayes raw: {bsec.mean() - braw.mean():+.4f}")
        print(f"   Bayes s1 (one factor, task 1's): {fmt(bs1)}   Bayes s1 − tuned: {bs1.mean() - tv.mean():+.4f}; Bayes SEC − Bayes s1: {bsec.mean() - bs1.mean():+.4f}")
        print(f"   rule Ω=1: {fmt(eq)}   rule − tuned: {eq.mean() - tv.mean():+.4f}; Bayes SEC − rule: {bsec.mean() - eq.mean():+.4f}")
        print(f"   calibration factors s_j (Bayes SEC arm, all tasks x seeds): median {np.median(svals):.4g}, min {min(svals):.4g}, max {max(svals):.4g}; fallbacks {nfb} of {len(svals)}")
        sens = {}
        for fs in SENS_FS:
            for fe in SENS_FE:
                if (fs, fe) != (FS, FE): sens[(fs, fe)] = A(name, "bayes_sec", 0.0, fs, fe).mean() - tv.mean()
        print("   sensitivity (Bayes SEC − tuned) by (start, end) window: " + "  ".join(f"{a:g}/{b:g}:{v:+.2f}" for (a, b), v in sens.items()))
        R[name] = dict(step=step, tuned=tuned, tuned_s=tuned_s, tv=tv, braw=braw, bsec=bsec, bs1=bs1, eq=eq, sens=sens, s=svals, nfb=nfb)

    n = len(ds); print("\n" + "-" * 112)
    print(f"carriers scored {n}; excluded by the class-selection rule: {excl or 'none'}")
    miscal = [d for d in ds if R[d]["braw"].mean() - R[d]["tv"].mean() <= -R[d]["step"]]
    calib = [d for d in ds if d not in miscal]
    dec = len(miscal) >= MIN_MISCAL
    print(f"SEC1-0 precondition: carriers where raw Bayes trails the tuned lambda by a step (miscalibrated): {miscal} ({len(miscal)}; need >= {MIN_MISCAL}) -> {'DECIDABLE' if dec else 'NOT DECIDABLE'}")
    closes = {}
    for d in miscal:
        gap = R[d]["tv"].mean() - R[d]["braw"].mean(); gain = R[d]["bsec"].mean() - R[d]["braw"].mean(); closes[d] = gain >= CLOSE_FRAC * gap
    need1 = math.ceil(CLOSE_SHARE * len(miscal)) if miscal else 0; v1 = dec and sum(closes.values()) >= need1
    print("SEC1-1 the calibrated Laplace weight closes at least half of the raw Laplace gap on the miscalibrated carriers: "
          + ", ".join(f"{d}: gap {R[d]['tv'].mean() - R[d]['braw'].mean():.4f}, gain {R[d]['bsec'].mean() - R[d]['braw'].mean():+.4f} ({'closes' if closes[d] else 'does not'})" for d in miscal)
          + f"; {sum(closes.values())}/{len(miscal)} (needs >= {need1}) -> " + ("PASS" if v1 else ("FAIL" if dec else "NOT DECIDABLE")))
    harm = {d: R[d]["bsec"].mean() - R[d]["braw"].mean() > -R[d]["step"] for d in calib}
    print("SEC1-2 no harm where raw Bayes is already within a step of the tuned lambda: Bayes SEC − Bayes raw "
          + ", ".join(f"{d}:{R[d]['bsec'].mean() - R[d]['braw'].mean():+.4f} (step {R[d]['step']:.2f})" for d in calib)
          + f"; not behind on {sum(harm.values())}/{len(calib)} -> {'PASS' if all(harm.values()) else 'FAIL'}")
    nb = {d: R[d]["bsec"].mean() - R[d]["tv"].mean() > -R[d]["step"] for d in ds}
    nb_raw = sum(1 for d in ds if R[d]["braw"].mean() - R[d]["tv"].mean() > -R[d]["step"])
    nb_eq = sum(1 for d in ds if R[d]["eq"].mean() - R[d]["tv"].mean() > -R[d]["step"])
    v3 = sum(nb.values()) >= TUNING_FREE_MIN
    print("SEC1-3 tuning-free: Bayes SEC − tuned lambda " + ", ".join(f"{d}:{R[d]['bsec'].mean() - R[d]['tv'].mean():+.4f} (step {R[d]['step']:.2f})" for d in ds)
          + f"; not behind on {sum(nb.values())}/{n} (needs >= {TUNING_FREE_MIN}) -> {'PASS' if v3 else 'FAIL'}; for comparison raw Bayes not behind on {nb_raw}/{n}, the rule Ω=1 on {nb_eq}/{n}")
    lr_ = [R[d]["tuned"] for d in ds]; ls_ = [R[d]["tuned_s"] for d in ds]
    span_r = max(lr_) / min(lr_); span_s = max(ls_) / min(ls_); v4 = span_s <= span_r / SPAN_FACTOR
    print(f"SEC1-4 span collapse: tuned lambda raw {dict(zip(ds, lr_))} span {span_r:.2f}x; calibrated {dict(zip(ds, ls_))} span {span_s:.2f}x; "
          f"calibrated span <= raw span / {SPAN_FACTOR:g}: {v4} -> {'PASS' if v4 else 'FAIL'}")
    print("SEC1-G one global factor (R7, report): Bayes SEC − Bayes s1 " + ", ".join(f"{d}:{R[d]['bsec'].mean() - R[d]['bs1'].mean():+.4f} (step {R[d]['step']:.2f})" for d in ds)
          + f"; per-task calibration ahead of one factor by a step on {sum(1 for d in ds if R[d]['bsec'].mean() - R[d]['bs1'].mean() >= R[d]['step'])}/{n}, behind by a step on {sum(1 for d in ds if R[d]['bsec'].mean() - R[d]['bs1'].mean() <= -R[d]['step'])}/{n}")
    print("SEC1-R the registered rule (R7, report): rule − tuned " + ", ".join(f"{d}:{R[d]['eq'].mean() - R[d]['tv'].mean():+.4f}" for d in ds)
          + "; Bayes SEC − rule " + ", ".join(f"{d}:{R[d]['bsec'].mean() - R[d]['eq'].mean():+.4f}" for d in ds))
    flips = sum(1 for d in ds for v in R[d]["sens"].values() if (v > -R[d]["step"]) != nb[d])
    print(f"SEC1-S sensitivity: SEC1-3 'not behind' flips in {flips} of {8 * n} window cells -> {'FRAGILE' if flips > 1 else 'not fragile'}")
    print("SEC1-E calibration factors (report): " + "; ".join(f"{d}: median s {np.median(R[d]['s']):.3g} (fallbacks {R[d]['nfb']})" for d in ds))
    print(f"summary: SEC1-0 {'DECIDABLE' if dec else 'NOT DECIDABLE'} ({len(miscal)} miscalibrated); SEC1-1 {'PASS' if v1 else ('FAIL' if dec else 'NOT DECIDABLE')}; "
          f"SEC1-2 {'PASS' if all(harm.values()) else 'FAIL'}; SEC1-3 {'PASS' if v3 else 'FAIL'} ({sum(nb.values())}/{n}); SEC1-4 {'PASS' if v4 else 'FAIL'}; fragile: {flips > 1}")


# ---------------------------------------------------------------- gate (R4)
def _synthetic(K=10, n=1500, d=20):
    rng = np.random.default_rng(0)
    X = rng.standard_normal((n, d)); y = rng.integers(0, K, n); X[np.arange(n), y % d] += 3.0
    return X, y


def gate():
    """GATE for SEC1 (R4; v2, AGENT_LOG 96: v1 closed because its units rows were not load-bearing on this stream, the raw
    Laplace arm being about 500x under-scaled, and the calibrated arm's invariance to a units change is an algebraic
    identity, not evidence). On a synthetic ten-class stream through the same run():
      POS    (MUST_PASS) the positive control: raw Laplace trails the tuned lambda (raw grid) by at least a step, and the
             calibrated Laplace closes at least half of that gap (SEC1-1's criterion)
      INV    (MUST_PASS) implementation check: the calibrated arm is unchanged (to 1e-9) under per-task and global units
             distortions of the Fisher
      SHAPE  (MUST_FAIL) a shape-only distortion (per-parameter factor exp(N(0, sd))): the calibrated arm must NOT stay within
             a step of its undistorted value (it corrects one scale per task and is blind to shape)
    One-factor arm (task 1's s for every task) and the registered rule printed beside it."""
    X, y = _synthetic(); K = 10; data = split_standardise(X, y, K)
    def arm(mode, dist=None, value=0.0): return np.array([run(mode, value, s, *data, K, 2, distort=dist)["acc"] for s in SEEDS])
    g = {w: arm("fixed", value=w) for w in EWC_COARSE}; tuned = max(g, key=lambda w: g[w].mean()); tv = g[tuned]; step = step_of(tv)
    b0 = arm("bayes"); s0 = arm("bayes_sec"); s1 = arm("bayes_s1"); eq = arm("eq", value=1.0)
    gap = tv.mean() - b0.mean(); gain = s0.mean() - b0.mean()
    pos = gap >= step and gain >= CLOSE_FRAC * gap
    print(f"GATE SEC1 v2 (synthetic ten-class stream, 5 tasks, seeds 0-4); step {step:.4f}")
    print("   raw lambda grid: " + "  ".join(f"{w:g}:{g[w].mean():.2f}" for w in g) + f"; tuned lambda {tuned:g}: {tv.mean():.4f}")
    print(f"   raw Laplace {b0.mean():.4f}; calibrated Laplace {s0.mean():.4f}; one-factor Laplace {s1.mean():.4f}; rule Omega=1 {eq.mean():.4f}")
    print(f"   POS   [MUST_PASS] gap tuned - raw {gap:.4f} (>= step: {gap >= step}); gain calibrated - raw {gain:+.4f} (>= half the gap: {gain >= CLOSE_FRAC * gap}) -> {'PASS' if pos else 'FAIL'}")
    inv_dev = 0.0
    for dist in (("unit", GATE_U_RANGE), ("global", GATE_GLOBAL[0]), ("global", GATE_GLOBAL[1])):
        inv_dev = max(inv_dev, float(np.max(np.abs(arm("bayes_sec", dist) - s0))))
    inv = inv_dev < 1e-9
    print(f"   INV   [MUST_PASS] calibrated arm under per-task x[1/16,16] and global x1/16, x16 distortions: max change {inv_dev:.2e} -> {'PASS' if inv else 'FAIL'}")
    sh = arm("bayes_sec", ("shape", GATE_SHAPE_SD)); shape_inv = abs(sh.mean() - s0.mean()) < step
    print(f"   SHAPE [MUST_FAIL] calibrated arm under a shape distortion exp(N(0,{GATE_SHAPE_SD})): {sh.mean():.4f} (moved {sh.mean() - s0.mean():+.4f}) -> {'PASS (VIOLATION: the must-fail row passed)' if shape_inv else 'FAIL (as required)'}")
    print(f"GATE {'OPEN' if (pos and inv and not shape_inv) else 'CLOSED'}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        X, y = _synthetic(); K = 10; data = split_standardise(X, y, K)
        for mode, v in (("fixed", 10.0), ("fixed_sec", 1.0), ("bayes", 0.0), ("bayes_sec", 0.0), ("bayes_s1", 0.0), ("eq", 1.0)):
            print(json.dumps(run(mode, v, 0, *data, K, 2)))
        print(json.dumps(run("bayes_sec", 0.0, 0, *data, K, 2, fs=0.05, fe=0.2)))
        for dist in (("unit", 16.0), ("global", 16.0), ("shape", 1.5)): print(json.dumps(run("bayes_sec", 0.0, 0, *data, K, 2, distort=dist)))
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/sec1_smokefull.jsonl"
        X, y = _synthetic(); K = 10
        meta = dict(file="synthetic", sha256="none", n=len(y), n_file=len(y), d=X.shape[1], classes_in_file=K, classes_requested=K, classes_used=K,
                    rows_dropped_nan=0, class_counts_file=[int((y == c).sum()) for c in range(K)], class_counts=[int((y == c).sum()) for c in range(K)],
                    class_floor=CLASS_FLOOR, excluded=False)
        with open(outp, "w") as out:
            run_all("mfeat_factors", split_standardise(X, y, K), K, 2, meta, out)       # synthetic data under a registered name, for the scorer's carrier order
        score([outp])
    elif cmd == "gate":
        gate()
    elif cmd == "run":
        name, mode, value, seed = sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
        K_req, per_task = DATASETS[name]; X, y, meta = load_pmlb(name, K_req)
        if meta["excluded"]: print(json.dumps(dict(dataset=name, **meta))); sys.exit(0)
        K = meta["classes_used"]; o = run(mode, value, seed, *split_standardise(X, y, K), K, per_task); o["dataset"] = name; print(json.dumps(o))
    elif cmd == "all":
        name = sys.argv[2]
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/sec1/results_{name}.jsonl"
        K_req, per_task = DATASETS[name]; X, y, meta = load_pmlb(name, K_req)
        with open(outp, "w") as out:
            if meta["excluded"]:
                print(json.dumps(dict(dataset=name, **meta)), file=out, flush=True)
            else:
                K = meta["classes_used"]; run_all(name, split_standardise(X, y, K), K, per_task, meta, out)
    elif cmd == "score":
        score(sys.argv[2:])
    else:
        raise SystemExit(__doc__)
