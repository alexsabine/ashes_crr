"""Study EQX — the equanimity rule (Omega = 1) against the constants it may reduce to,
on class-incremental streams built from datasets absent from data/SEEN.md.

    uv run python studies/eqx/eqx_score.py run   <dataset> <method> <value> <seed> [--metric fisher|euclid]
    uv run python studies/eqx/eqx_score.py all    <dataset>            # every arm, seeds 0-4, JSON lines
    uv run python studies/eqx/eqx_score.py score  <results.jsonl>      # scores EQX-1..5 as pre-registered
    uv run python studies/eqx/eqx_score.py smoke                       # synthetic data, no download

Pipeline: single online pass, MLP d-256-K (ReLU), SGD lr 0.05, batch 10, reservoir buffer
500, class-IL (single head, tested on all classes). Ported from
archive/cl_ledger_2026-09-14/mlp_bench.py with (a) the number of classes a parameter,
(b) the ER-sum arm made explicit (fixed w = 1 on two batch means), (c) one thread and
one RNG so two runs are byte-identical (R9), (d) no method other than er / fixed / eq.

The adaptive estimator is FROZEN as the archive's final choice, which was selected after
seeing KMNIST seed 0 on 2026-09-14 (R3: named here, used on a different day, on datasets
that estimator never touched): ratio = ema of the two mean gradients, smoothing 0.98,
Fisher diagonal = running EMA of (batch-mean gradient)^2 * batch^2, w capped at 50.
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
RAW = ROOT / "data" / "raw" / "pmlb"

# ---------------------------------------------------------------- frozen study parameters
LR = 0.05; BS = 10; HID = 256; BUF = 500; REPLAY = 0.2
SMOOTH = 0.98; WCAP = 50.0
FIXED_GRID = (0.2, 0.5, 1.0, 2.0, 4.0)
OMEGA_GRID = (0.5, 0.71, 1.0, 1.41, 2.0)
SEEDS = (0, 1, 2, 3, 4)
TEST_FRAC = 0.2
DATASETS = {  # PMLB name -> (classes used, classes per task)
    "optdigits": (10, 2),
    "pendigits": (10, 2),
    "letter": (26, 2),
}


# ---------------------------------------------------------------- data
def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pmlb(name: str):
    p = RAW / f"{name}.tsv.gz"
    with gzip.open(p, "rt") as f:
        header = f.readline().rstrip("\n").split("\t")
        rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    ti = header.index("target")
    X = np.array([[float(v) for j, v in enumerate(r) if j != ti] for r in rows], np.float32)
    y = np.array([int(float(r[ti])) for r in rows])
    classes = np.unique(y); remap = {c: i for i, c in enumerate(classes)}
    y = np.array([remap[c] for c in y])
    nan = int(np.isnan(X).any(1).sum())
    if nan:
        keep = ~np.isnan(X).any(1); X, y = X[keep], y[keep]
    return X, y, dict(file=str(p.relative_to(ROOT)), sha256=sha256(p), n=len(y), d=X.shape[1], classes=len(classes), rows_dropped_nan=nan)


def split_standardise(X, y, K):
    """Fixed 80/20 stratified split (seed 12345, independent of run seed); standardise
    features on the training part only."""
    rng = np.random.default_rng(12345)
    tr, te = [], []
    for c in range(K):
        idx = rng.permutation(np.where(y == c)[0]); n_te = int(round(TEST_FRAC * len(idx)))
        te.append(idx[:n_te]); tr.append(idx[n_te:])
    tr = np.concatenate(tr); te = np.concatenate(te)
    mu = X[tr].mean(0); sd = X[tr].std(0); sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    return Z[tr], y[tr], Z[te], y[te]


# ---------------------------------------------------------------- model
class MLP:
    def __init__(s, rng, d, K, h=HID):
        s.W1 = rng.normal(0, math.sqrt(2 / d), (d, h)).astype(np.float32); s.b1 = np.zeros(h, np.float32)
        s.W2 = rng.normal(0, math.sqrt(2 / h), (h, K)).astype(np.float32); s.b2 = np.zeros(K, np.float32)
        s.K = K

    def params(s): return [s.W1, s.b1, s.W2, s.b2]

    def forward(s, x):
        h = np.maximum(0, x @ s.W1 + s.b1); return h, h @ s.W2 + s.b2

    def loss_grad(s, x, y):
        h, z = s.forward(x); z = z - z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
        n = len(y); dz = p.copy(); dz[np.arange(n), y] -= 1; dz /= n
        gW2 = h.T @ dz; gb2 = dz.sum(0); dh = dz @ s.W2.T; dh[h <= 0] = 0; gW1 = x.T @ dh; gb1 = dh.sum(0)
        return [gW1, gb1, gW2, gb2]

    def step(s, grads, lr):
        for p, g in zip(s.params(), grads): p -= lr * g

    def acc(s, x, y): return float((s.forward(x)[1].argmax(1) == y).mean())


def flat(gs): return np.concatenate([g.ravel() for g in gs])


def make_stream(rng, Xtr, ytr, K, per_task):
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    xs, ys = [], []
    for t in tasks:
        ii = np.concatenate([np.where(ytr == c)[0] for c in t]); ii = rng.permutation(ii)
        xs.append(Xtr[ii]); ys.append(ytr[ii])
    return np.concatenate(xs), np.concatenate(ys), tasks


# ---------------------------------------------------------------- one run
def run(method: str, value: float, seed: int, Xtr, ytr, Xte, yte, K, per_task, metric="fisher"):
    """method: 'er' (concatenated batch mean, replay fraction = value),
               'fixed' (g = g_stream + value * g_replay),
               'eq' (g = g_stream + w * g_replay, w = value * ||ema g_stream|| / ||ema g_replay||)."""
    rng = np.random.default_rng(seed)
    sx, sy, tasks = make_stream(rng, Xtr, ytr, K, per_task)
    d = Xtr.shape[1]; net = MLP(rng, d, K)
    bufx = np.zeros((BUF, d), np.float32); bufy = np.zeros(BUF, int); nb = 0; seen = 0
    r = value if method == "er" else REPLAY
    rb_int = int(r * BS); rb_frac = r * BS - rb_int
    Fd = None; ev = [None, None]; wlog = []; compute = 0.0
    for t in range(0, len(sy), BS):
        x, y = sx[t:t + BS], sy[t:t + BS]
        rb = rb_int + (1 if rng.random() < rb_frac else 0)
        rx = ry = None
        if nb > 0 and rb > 0:
            sel = rng.choice(nb, min(rb, nb), replace=False); rx, ry = bufx[sel], bufy[sel]
        if method == "er" or rx is None:
            xx = x if rx is None else np.concatenate([x, rx]); yy = y if ry is None else np.concatenate([y, ry])
            g = net.loss_grad(xx, yy); compute += 3 * len(yy)
        else:
            gn = net.loss_grad(x, y); gp = net.loss_grad(rx, ry); compute += 3 * (len(y) + len(ry))
            if method == "fixed":
                w = value
            elif method == "eq":
                gn_f, gp_f = flat(gn), flat(gp)
                if Fd is None: Fd = np.full(gn_f.size, 1e-3, np.float32)
                if ev[0] is None: ev[0], ev[1] = gn_f.copy(), gp_f.copy()
                else: ev[0] = SMOOTH * ev[0] + (1 - SMOOTH) * gn_f; ev[1] = SMOOTH * ev[1] + (1 - SMOOTH) * gp_f
                M = Fd if metric == "fisher" else 1.0
                w = min(value * math.sqrt(float(np.sum(M * ev[0] * ev[0])) / max(float(np.sum(M * ev[1] * ev[1])), 1e-12)), WCAP)
            else:
                raise ValueError(method)
            wlog.append(w)
            g = [a + w * b for a, b in zip(gn, gp)]
        net.step(g, LR)
        if method == "eq":
            gf = flat(g)
            if Fd is None: Fd = np.full(gf.size, 1e-3, np.float32)
            Fd = 0.99 * Fd + 0.01 * (gf ** 2) * len(y) ** 2
        for i in range(len(y)):  # reservoir
            seen += 1
            if nb < BUF: j = nb; nb += 1
            else:
                j = rng.integers(seen)
                if j >= BUF: continue
            bufx[j] = x[i]; bufy[j] = y[i]
    last = tasks[-1]; m = np.isin(yte, last)
    return dict(method=method, value=value, seed=seed, metric=metric if method == "eq" else None,
                acc=net.acc(Xte, yte), last_task_acc=net.acc(Xte[m], yte[m]),
                compute_per_sample=compute / len(sy), w_med=float(np.median(wlog)) if wlog else None,
                w_cap_frac=float(np.mean(np.array(wlog) >= WCAP)) if wlog else None, n_stream=int(len(sy)))


def arms():
    for w in FIXED_GRID: yield ("fixed", w, "fisher")
    for om in OMEGA_GRID: yield ("eq", om, "fisher")
    yield ("eq", 1.0, "euclid")
    for r in (REPLAY, 1.0): yield ("er", r, "fisher")


def run_all(name, Xtr, ytr, Xte, yte, K, per_task, meta):
    print(json.dumps(dict(dataset=name, **meta, K=K, per_task=per_task, n_train=int(len(ytr)), n_test=int(len(yte)),
                          lr=LR, bs=BS, hid=HID, buf=BUF, replay=REPLAY, smooth=SMOOTH, wcap=WCAP)), flush=True)
    for seed in SEEDS:
        for method, value, metric in arms():
            o = run(method, value, seed, Xtr, ytr, Xte, yte, K, per_task, metric)
            o["dataset"] = name; print(json.dumps(o), flush=True)


# ---------------------------------------------------------------- scoring (EQX-1..5, as in PREREG.md)
def score(paths):
    rows = []
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "acc" in o: rows.append(o)
    ds = sorted(set(r["dataset"] for r in rows))

    def a(name, method, value, metric=None):
        v = sorted([r for r in rows if r["dataset"] == name and r["method"] == method and abs(r["value"] - value) < 1e-9
                    and (metric is None or r.get("metric") == metric)], key=lambda r: r["seed"])
        assert len(v) == len(SEEDS), (name, method, value, metric, [r["seed"] for r in v])
        return np.array([r["acc"] * 100 for r in v])

    def fmt(x): return f"{x.mean():.4f} [" + " ".join(f"{q:.2f}" for q in x) + "]"

    print("=" * 110); print("EQX scoring — per-seed values in brackets (seeds 0-4); thresholds from prereg/eqx/PREREG.md"); print("=" * 110)
    v1 = v2 = v3 = v4 = 0
    for name in ds:
        eq1 = a(name, "eq", 1.0, "fisher"); eu = a(name, "eq", 1.0, "euclid")
        fx = {w: a(name, "fixed", w) for w in FIXED_GRID}; er02 = a(name, "er", REPLAY); er1 = a(name, "er", 1.0)
        om = {o: a(name, "eq", o, "fisher") for o in OMEGA_GRID}
        wmed = np.median([r["w_med"] for r in rows if r["dataset"] == name and r["method"] == "eq" and r["value"] == 1.0 and r.get("metric") == "fisher"])
        consts = dict(**{f"fixed w={w}": fx[w] for w in FIXED_GRID}, **{f"ER({REPLAY})": er02})
        best_c = max(consts, key=lambda k: consts[k].mean())
        d1 = eq1 - consts[best_c]
        print(f"\n[{name}]  EQ(Ω=1,fisher) = {fmt(eq1)}   median w = {wmed:.3f}")
        for k, v in consts.items(): print(f"   {k:14s} {fmt(v)}   EQ − this: {eq1.mean()-v.mean():+.3f}")
        print(f"   ER(1.0)        {fmt(er1)}   compute {[r['compute_per_sample'] for r in rows if r['dataset']==name and r['method']=='er' and r['value']==1.0][0]:.3f} vs EQ {[r['compute_per_sample'] for r in rows if r['dataset']==name and r['method']=='eq' and r['value']==1.0][0]:.3f}")
        print(f"   Ω landscape: " + "  ".join(f"{o}:{om[o].mean():.2f}" for o in OMEGA_GRID))
        # EQX-1 reduction
        red = d1.mean() < 1.0
        print(f"   EQX-1 reduction: EQ − best constant ({best_c}) = {d1.mean():+.4f}, per seed {[f'{q:+.2f}' for q in d1]}, seeds with EQ better by ≥1.0: {int((d1>=1).sum())}/5"
              f"  -> {'REDUCES to a constant' if red else 'adaptive rule ahead of every constant on this dataset'}")
        v1 += red
        # EQX-2 theory value
        best_o = max(om, key=lambda o: om[o].mean()); c71 = om[1.0].mean() - om[0.71].mean(); c141 = om[1.0].mean() - om[1.41].mean()
        ok2 = best_o == 1.0 and c71 > 1.0 and c141 > 1.0
        print(f"   EQX-2 theory value: best Ω = {best_o}; Ω=1 − Ω=0.71 = {c71:+.2f}, Ω=1 − Ω=1.41 = {c141:+.2f} -> {'PASS' if ok2 else 'FAIL'}")
        v2 += ok2
        # EQX-3 vs ER-sum
        d3 = eq1 - fx[1.0]; ok3 = d3.mean() >= 1.0 and (d3 > 0).sum() >= 4
        print(f"   EQX-3 vs ER-sum (fixed w=1): {d3.mean():+.4f}, per seed {[f'{q:+.2f}' for q in d3]}, positive in {int((d3>0).sum())}/5 -> {'PASS' if ok3 else 'FAIL'}")
        v3 += ok3
        # EQX-4 metric
        d4 = eq1 - eu; ok4 = abs(d4.mean()) < 1.0
        print(f"   EQX-4 Fisher − Euclid: {d4.mean():+.4f}, per seed {[f'{q:+.2f}' for q in d4]} -> {'metric immaterial' if ok4 else 'metric matters'}")
        v4 += ok4
        # EQX-5 compute claim (report)
        d5 = eq1 - er1
        print(f"   EQX-5 EQ(0.2) − ER(1.0): {d5.mean():+.4f}, per seed {[f'{q:+.2f}' for q in d5]} (report only)")
    n = len(ds)
    print("\n" + "-" * 110)
    print(f"EQX-1 (reduction) triggers on {v1}/{n} datasets -> {'REDUCES: Ω = 1 ≡ a fixed replay weight' if v1 >= 2 else 'does not reduce on ≥2 datasets'}")
    print(f"EQX-2 (theory value) PASS on {v2}/{n} datasets -> {'PASS' if v2 >= 2 else 'FAIL'} (needs ≥ 2 of 3)")
    print(f"EQX-3 (beats ER-sum by ≥1.0, ≥4/5 seeds) PASS on {v3}/{n} datasets -> {'PASS' if v3 >= 2 else 'FAIL'} (needs ≥ 2 of 3)")
    print(f"EQX-4 (Fisher immaterial) on {v4}/{n} datasets")


# ---------------------------------------------------------------- main
def _load(name):
    K, per_task = DATASETS[name]
    X, y, meta = load_pmlb(name)
    assert meta["classes"] == K, (name, meta)
    Xtr, ytr, Xte, yte = split_standardise(X, y, K)
    return Xtr, ytr, Xte, yte, K, per_task, meta


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        rng = np.random.default_rng(0); K = 10
        X = rng.standard_normal((3000, 40)).astype(np.float32); y = rng.integers(0, K, 3000)
        X[np.arange(3000), y % 40] += 3.0
        Xtr, ytr, Xte, yte = split_standardise(X, y, K)
        for method, value, metric in (("er", 0.2, "fisher"), ("fixed", 1.0, "fisher"), ("eq", 1.0, "fisher"), ("eq", 1.0, "euclid")):
            print(json.dumps(run(method, value, 0, Xtr, ytr, Xte, yte, K, 2, metric)))
    elif cmd == "run":
        name, method, value, seed = sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
        metric = sys.argv[sys.argv.index("--metric") + 1] if "--metric" in sys.argv else "fisher"
        Xtr, ytr, Xte, yte, K, per_task, meta = _load(name)
        o = run(method, value, seed, Xtr, ytr, Xte, yte, K, per_task, metric); o["dataset"] = name; print(json.dumps(o))
    elif cmd == "all":
        name = sys.argv[2]
        Xtr, ytr, Xte, yte, K, per_task, meta = _load(name)
        run_all(name, Xtr, ytr, Xte, yte, K, per_task, meta)
    elif cmd == "score":
        score(sys.argv[2:])
    else:
        raise SystemExit(__doc__)
