"""Study T1x — path length against endpoint displacement as a predictor of forgetting, with the learning rate controlled
(CLAUDE.md section 5; owner request prompt-log entries 86-87; prereg/t1x/PREREG.md). Model (d): a numpy MLP (d-64-1, ReLU,
squared loss) on unseen PMLB regression streams; models (a)-(c) of CLAUDE.md section 5 are not available in this environment.

Per carrier: task 1 = rows with feature 0 below its median, task 2 = the rest (covariate drift); 80/20 train/test per task
(seed 12345); features and targets standardised on task 1's training rows. One base model theta_0 per carrier (task 1, 30
epochs, lr 0.01, batch 10, seed 0). Each RUN fine-tunes theta_0 on task 2 for 20 epochs under (schedule, lr, seed):
    schedules: const | sawtooth (lr x triangle, period T/4) | cosine_restarts (period T/4) | noise1.0, noise3.0 (Gaussian
               gradient noise of that sd x the running gradient scale) | loop (odd epochs revisit task 1: the path returns near
               the start) | short (5 epochs) | long (40 epochs) | restart (10 epochs, reset to theta_0, 10 epochs: the path
               doubles, the endpoint is a const run's)
    lr in {0.0025, 0.005, 0.01, 0.02}; seeds {0, 1, 2}   -> 108 runs per carrier (>= 60)
Per run: forgetting F = task-1 test MSE after minus before; predictors on fixed probes (task-1 test rows = the OLD probe,
task-2 test rows = the NEW probe), predictive means snapshotted every SNAP steps: C = sum sqrt(2 KL_gauss) (path), E = KL
(base -> final) (endpoint), on each probe; S = C - C* on the old probe; the EWC Fisher-weighted endpoint distance
(theta_T - theta_0)' diag(F_1) (theta_T - theta_0) with F_1 the diagonal empirical Fisher of task 1 at theta_0.
Rows T1x-0..2, S, sensitivity (PREREG.md). Every verdict word computed (R15).
    uv run python studies/t1x/t1x_score.py smoke                  # synthetic carrier, every branch
    uv run python studies/t1x/t1x_score.py all <dataset> [--out F]
    uv run python studies/t1x/t1x_score.py score <results.jsonl ...>
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
from scipy.stats import spearmanr  # noqa: E402

_HERE = Path(__file__).resolve()
ROOT = _HERE.parents[3] if _HERE.parent.name == "frozen" else _HERE.parents[2]
RAW = ROOT / "data" / "raw" / "pmlb"

# ---------------------------------------------------------------- registered constants
HID = 64; BS = 10; SPLIT_SEED = 12345; MAX_ROWS = 5000; SUBSAMPLE_SEED = 777; TEST_FRAC = 0.2
BASE_EPOCHS = 30; BASE_LR = 0.01; BASE_SEED = 0
FT_EPOCHS = 20; SNAP = 5; SNAP_INTERVALS = (5, 10, 20)                # snapshots kept every SNAP steps; C computed at three intervals (sensitivity)
LR_GRID = (0.0025, 0.005, 0.01, 0.02); FIXED_LR = 0.01
SCHEDULES = ("const", "sawtooth", "cosine_restarts", "noise1.0", "noise3.0", "loop", "short", "long", "restart")
EPOCHS_OF = {"short": 5, "long": 40}                                  # training length is a schedule parameter; every other schedule runs FT_EPOCHS
DIVERGED_FACTOR = 100.0                                               # a run whose final task-2 test MSE exceeds DIVERGED_FACTOR x the base model's task-2 test MSE is diverged: dropped and counted
SEEDS = (0, 1, 2)
PROBE_MAX = 500; VAR = 1.0
LOG_FLOOR = 1e-6
MARGIN = 0.05; SPAN_MIN = 3.0; RHO_MIN = 0.6; RHO_GAP = 0.2
DATASETS = ("218_house_8L", "344_mv", "564_fried", "215_2dplanes", "1193_BNG_lowbwt", "294_satellite_image")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def kl_gauss(mu_old, mu_new, var=VAR):
    return float(np.mean((np.asarray(mu_old) - np.asarray(mu_new)) ** 2) / (2.0 * var))


# ---------------------------------------------------------------- data
def load_pmlb_regression(name):
    p = RAW / f"{name}.tsv.gz"
    with gzip.open(p, "rt") as f:
        header = f.readline().rstrip("\n").split("\t"); rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]
    ti = header.index("target")
    X = np.array([[float(v) for j, v in enumerate(r) if j != ti] for r in rows], np.float64); y = np.array([float(r[ti]) for r in rows])
    nan = int((np.isnan(X).any(1) | np.isnan(y)).sum())
    if nan:
        keep = ~(np.isnan(X).any(1) | np.isnan(y)); X, y = X[keep], y[keep]
    n_file = int(len(y))
    if len(y) > MAX_ROWS:
        pick = np.sort(np.random.default_rng(SUBSAMPLE_SEED).permutation(len(y))[:MAX_ROWS]); X, y = X[pick], y[pick]
    return X, y, dict(file=str(p.relative_to(ROOT)), sha256=sha256(p), n=int(len(y)), n_file=n_file, d=int(X.shape[1]), rows_dropped_nan=nan)


def make_tasks(X, y):
    med = np.median(X[:, 0]); t1 = X[:, 0] <= med; t2 = ~t1
    rng = np.random.default_rng(SPLIT_SEED); tasks = []
    for mask in (t1, t2):
        idx = np.where(mask)[0]; perm = rng.permutation(len(idx)); n_te = int(round(TEST_FRAC * len(idx)))
        tasks.append((idx[perm[n_te:]], idx[perm[:n_te]]))
    tr1 = tasks[0][0]; mu = X[tr1].mean(0); sd = X[tr1].std(0); sd[sd == 0] = 1.0; ym = y[tr1].mean(); ys = y[tr1].std() or 1.0
    Z = (X - mu) / sd; t = (y - ym) / ys
    return [(Z[tr], t[tr], Z[te], t[te]) for tr, te in tasks]


# ---------------------------------------------------------------- model
class MLP:
    def __init__(self, rng, d, h=HID):
        self.W1 = rng.normal(0, math.sqrt(2 / d), (d, h)); self.b1 = np.zeros(h); self.W2 = rng.normal(0, math.sqrt(1 / h), (h, 1)); self.b2 = np.zeros(1)
    def flat(self): return np.concatenate([self.W1.ravel(), self.b1, self.W2.ravel(), self.b2])
    def set_flat(self, v):
        i = 0
        for a in (self.W1, self.b1, self.W2, self.b2):
            a[...] = v[i:i + a.size].reshape(a.shape); i += a.size
    def predict(self, X):
        return (np.maximum(0, X @ self.W1 + self.b1) @ self.W2 + self.b2)[:, 0]
    def grad(self, X, y):
        """gradient of the batch mean squared error 1/2 (pred - y)^2, flattened"""
        Hp = X @ self.W1 + self.b1; Hr = np.maximum(0, Hp); pred = (Hr @ self.W2 + self.b2)[:, 0]; r = (pred - y) / len(y)
        dW2 = Hr.T @ r[:, None]; db2 = np.array([r.sum()]); dH = (r[:, None] @ self.W2.T) * (Hp > 0)
        return np.concatenate([(X.T @ dH).ravel(), dH.sum(0), dW2.ravel(), db2])
    def per_sample_sq_grad(self, X, y):
        """diagonal empirical Fisher: mean over samples of the squared per-sample gradient of 1/2 (pred - y)^2"""
        Hp = X @ self.W1 + self.b1; Hr = np.maximum(0, Hp); pred = (Hr @ self.W2 + self.b2)[:, 0]; r = pred - y
        gW2 = (Hr * r[:, None]) ** 2; gb2 = r ** 2; dH = (r[:, None] @ self.W2.T) * (Hp > 0)
        gW1 = np.einsum("ni,nj->ij", X ** 2, dH ** 2) / len(y); gb1 = (dH ** 2).mean(0)
        return np.concatenate([gW1.ravel(), gb1, gW2.mean(0), [gb2.mean()]])


def mse(net, X, y): return float(np.mean((net.predict(X) - y) ** 2))


def train_base(tasks, d):
    rng = np.random.default_rng(BASE_SEED); net = MLP(rng, d); Xtr, ytr = tasks[0][0], tasks[0][1]
    for _ in range(BASE_EPOCHS):
        perm = rng.permutation(len(ytr))
        for s in range(0, len(perm), BS):
            ii = perm[s:s + BS]; net.set_flat(net.flat() - BASE_LR * net.grad(Xtr[ii], ytr[ii]))
    return net


def lr_at(schedule, lr, step, T):
    if schedule == "sawtooth":
        P = max(T // 4, 1); ph = (step % P) / P; return lr * (2 * ph if ph < 0.5 else 2 * (1 - ph)) * 2   # triangle, mean lr
    if schedule == "cosine_restarts":
        P = max(T // 4, 1); ph = (step % P) / P; return lr * (1 + math.cos(math.pi * ph))              # cosine with warm restarts, mean lr
    return lr


def run(schedule, lr, seed, tasks, base, fisher, snap=SNAP):
    rng = np.random.default_rng(1000 * seed + 7); net = MLP(np.random.default_rng(0), tasks[0][0].shape[1]); net.set_flat(base.flat().copy())
    theta0 = base.flat().copy()
    X1, y1, X1te, y1te = tasks[0]; X2, y2, X2te, y2te = tasks[1]
    old_probe = (X1te[:PROBE_MAX], y1te[:PROBE_MAX]); new_probe = (X2te[:PROBE_MAX], y2te[:PROBE_MAX])
    f_before = mse(net, X1te, y1te)
    snaps_old = [net.predict(old_probe[0])]; snaps_new = [net.predict(new_probe[0])]
    epochs = EPOCHS_OF.get(schedule, FT_EPOCHS)
    n_steps_ep = int(math.ceil(len(y2) / BS)); T = epochs * n_steps_ep; step = 0; gscale = None; noise_sd = {"noise1.0": 1.0, "noise3.0": 3.0}.get(schedule, 0.0)
    for ep in range(epochs):
        if schedule == "restart" and ep == epochs // 2: net.set_flat(theta0.copy())        # reset to the base model half-way: the path doubles
        on_old = (schedule == "loop" and ep % 2 == 1)
        Xc, yc = (X1, y1) if on_old else (X2, y2); perm = rng.permutation(len(yc))
        for s in range(0, len(perm), BS):
            ii = perm[s:s + BS]; g = net.grad(Xc[ii], yc[ii])
            gn = float(np.linalg.norm(g)); gscale = gn if gscale is None else 0.99 * gscale + 0.01 * gn
            if noise_sd: g = g + noise_sd * gscale * rng.standard_normal(len(g)) / math.sqrt(len(g))
            net.set_flat(net.flat() - lr_at(schedule, lr, step, T) * g); step += 1
            if step % snap == 0:
                snaps_old.append(net.predict(old_probe[0])); snaps_new.append(net.predict(new_probe[0]))
            if s + BS >= len(perm) and ep == epochs - 1 and step % snap != 0:
                snaps_old.append(net.predict(old_probe[0])); snaps_new.append(net.predict(new_probe[0]))
    thetaT = net.flat(); new_loss = mse(net, X2te, y2te); base_new = mse(base, X2te, y2te)
    finite = bool(np.all(np.isfinite(thetaT))) and np.isfinite(new_loss) and new_loss <= DIVERGED_FACTOR * base_new
    out = dict(schedule=schedule, lr=float(lr), seed=int(seed), epochs=int(epochs), f_before=f_before, f_after=mse(net, X1te, y1te), forgetting=mse(net, X1te, y1te) - f_before,
               new_loss=new_loss, ewc_dist=float(np.sum(fisher * (thetaT - theta0) ** 2)), n_steps=int(step), finite=finite)
    for tag, snaps in (("old", snaps_old), ("new", snaps_new)):
        for k in SNAP_INTERVALS:
            sub = snaps[::k // snap] if k // snap > 1 else snaps
            if sub[-1] is not snaps[-1]: sub = list(sub) + [snaps[-1]]
            C = float(sum(math.sqrt(2 * kl_gauss(a, b)) for a, b in zip(sub[:-1], sub[1:])))
            out[f"C_{tag}_{k}"] = C
        E = kl_gauss(snaps[0], snaps[-1]); out[f"E_{tag}"] = E; out[f"Cstar_{tag}"] = math.sqrt(2 * E); out[f"S_{tag}"] = out[f"C_{tag}_{SNAP}"] - math.sqrt(2 * E)
    json.dumps(out); return out


def run_all(name, tasks, meta, out):
    d = tasks[0][0].shape[1]; base = train_base(tasks, d); fisher = base.per_sample_sq_grad(tasks[0][0], tasks[0][1])
    hdr = dict(dataset=name, **meta, n_task1_train=int(len(tasks[0][1])), n_task1_test=int(len(tasks[0][3])), n_task2_train=int(len(tasks[1][1])), n_task2_test=int(len(tasks[1][3])),
               hid=HID, base_epochs=BASE_EPOCHS, base_lr=BASE_LR, ft_epochs=FT_EPOCHS, epochs_of=EPOCHS_OF, diverged_factor=DIVERGED_FACTOR, bs=BS, snap=SNAP, lr_grid=list(LR_GRID), schedules=list(SCHEDULES), seeds=list(SEEDS),
               base_task1_test_mse=mse(base, tasks[0][2], tasks[0][3]), base_task2_test_mse=mse(base, tasks[1][2], tasks[1][3]), uv_lock_sha256=sha256(ROOT / "uv.lock"))
    print(json.dumps(hdr), file=out, flush=True)
    for schedule in SCHEDULES:
        for lr in LR_GRID:
            for seed in SEEDS:
                o = run(schedule, lr, seed, tasks, base, fisher); o["dataset"] = name; print(json.dumps(o), file=out, flush=True)


# ---------------------------------------------------------------- scoring
def _logs(rs, key): return np.log(np.maximum(np.array([r[key] for r in rs], float), LOG_FLOOR))


def heldout_r2(rs, pred_key, fit_mask, control_lr=True):
    """OLS of log F on log predictor (+ log lr), fitted on fit_mask, R^2 on the rest."""
    y = _logs(rs, "forgetting"); x = _logs(rs, pred_key); lr = np.log(np.array([r["lr"] for r in rs]))
    A = np.column_stack([np.ones(len(y)), x, lr]) if control_lr else np.column_stack([np.ones(len(y)), x])
    beta = np.linalg.lstsq(A[fit_mask], y[fit_mask], rcond=None)[0]; te = ~fit_mask
    res = y[te] - A[te] @ beta; tot = y[te] - y[te].mean()
    return float(1 - np.sum(res ** 2) / max(np.sum(tot ** 2), 1e-12))


def splits(rs):
    """three registered fit/score splits: (i) alternate runs in (schedule, lr, seed) order; (ii) seeds {0, 1} fit, seed 2 score; (iii) the other parity"""
    n = len(rs); idx = np.arange(n)
    return {"alternate": idx % 2 == 0, "by_seed": np.array([r["seed"] in (0, 1) for r in rs]), "alternate_b": idx % 2 == 1}


def score(paths):
    rows = []; hdrs = {}
    for p in paths:
        for line in open(p):
            if line.startswith("{"):
                o = json.loads(line)
                if "schedule" in o: rows.append(o)
                elif "dataset" in o: hdrs[o["dataset"]] = o
    ds = sorted(set(r["dataset"] for r in rows))
    print("=" * 112); print("T1x scoring — held-out R^2 of log forgetting on log predictor with log lr as a covariate; thresholds from prereg/t1x/PREREG.md"); print("=" * 112)
    R = {}
    for name in ds:
        rs = sorted([r for r in rows if r["dataset"] == name and r["finite"]], key=lambda r: (SCHEDULES.index(r["schedule"]), r["lr"], r["seed"]))
        h = hdrs.get(name, {}); n_nonfinite = sum(1 for r in rows if r["dataset"] == name and not r["finite"])
        print(f"\n[{name}] n = {h.get('n')} of {h.get('n_file')} rows, d = {h.get('d')}; base task-1 test MSE {h.get('base_task1_test_mse'):.4f}, task-2 {h.get('base_task2_test_mse'):.4f}; runs {len(rs)} kept, {n_nonfinite} diverged or non-finite (dropped, counted)")
        # T1x-0: within each lr the path spans >= 3x across schedules and seeds (old probe, SNAP interval)
        spans = {}
        for lr in LR_GRID:
            v = [r[f"C_old_{SNAP}"] for r in rs if r["lr"] == lr]; spans[lr] = (max(v) / max(min(v), 1e-12)) if v else float("nan")
        ok0 = all(s >= SPAN_MIN for s in spans.values())
        print("   T1x-0 path span across schedules within each lr (C_old max/min): " + "  ".join(f"lr{lr:g}:{spans[lr]:.2f}x" for lr in LR_GRID) + f" -> {'decidable' if ok0 else 'NOT DECIDABLE (span < 3x)'}")
        fg = np.array([r["forgetting"] for r in rs]); print(f"   forgetting: median {np.median(fg):.4f}, range [{fg.min():.4f}, {fg.max():.4f}]; negative (task 1 improved) in {int((fg < 0).sum())}/{len(rs)} runs (floored at {LOG_FLOOR} on the log scale)")
        S_old = np.array([r["S_old"] for r in rs]); print(f"   S = C − C* on the old probe: median {np.median(S_old):.4f}, S < 0 in {int((S_old < 0).sum())}/{len(rs)} runs (round-off only, P1); S/C* median {np.median([r['S_old'] / max(r['Cstar_old'], 1e-12) for r in rs]):.3f}")
        sp = splits(rs); main = sp["alternate"]
        preds = {"C_new": f"C_new_{SNAP}", "C_old": f"C_old_{SNAP}", "E_new": "E_new", "E_old": "E_old", "ewc": "ewc_dist"}
        r2 = {k: heldout_r2(rs, key, main) for k, key in preds.items()}
        best_path = max(r2["C_new"], r2["C_old"]); best_end = max(r2["E_new"], r2["E_old"], r2["ewc"]); gap = best_path - best_end
        v1 = "PASS" if gap >= MARGIN else ("FAIL" if gap <= -MARGIN else "INCONCLUSIVE")
        print("   T1x-1 held-out R^2 (lr controlled, split 'alternate'): " + "  ".join(f"{k}:{v:.3f}" for k, v in r2.items()) + f"  -> best path {best_path:.3f}, best endpoint {best_end:.3f}, path − endpoint {gap:+.3f} -> {v1}")
        # sensitivity: 3 splits x 3 snapshot intervals
        cells = {}
        for sname, m in sp.items():
            for k in SNAP_INTERVALS:
                bp = max(heldout_r2(rs, f"C_new_{k}", m), heldout_r2(rs, f"C_old_{k}", m)); be = max(heldout_r2(rs, "E_new", m), heldout_r2(rs, "E_old", m), heldout_r2(rs, "ewc_dist", m))
                g = bp - be; cells[(sname, k)] = "PASS" if g >= MARGIN else ("FAIL" if g <= -MARGIN else "INCONCLUSIVE")
        flips = sum(1 for v in cells.values() if v != v1)
        print("   sensitivity (split x snapshot interval): " + "  ".join(f"{s}/{k}:{v}" for (s, k), v in cells.items()) + f" -> flips {flips}/9")
        # T1x-2 on the fixed-lr arm
        fx = [r for r in rs if r["lr"] == FIXED_LR]; fF = np.array([r["forgetting"] for r in fx])
        rho = {k: float(spearmanr(np.array([r[key] for r in fx]), fF).correlation) for k, key in preds.items()}
        v2 = (rho["C_old"] >= RHO_MIN) and (rho["E_new"] < rho["C_old"] - RHO_GAP)
        print(f"   T1x-2 fixed lr {FIXED_LR:g} ({len(fx)} runs), Spearman with forgetting: " + "  ".join(f"{k}:{v:+.3f}" for k, v in rho.items()) + f" -> C_old >= {RHO_MIN}: {rho['C_old'] >= RHO_MIN}; E_new < C_old − {RHO_GAP}: {rho['E_new'] < rho['C_old'] - RHO_GAP} -> {'PASS' if v2 else 'FAIL'}")
        # do high-S runs fall off the endpoint curve? residual of the E_old fit (in-sample, report) vs S
        y = _logs(rs, "forgetting"); x = _logs(rs, "E_old"); lrl = np.log(np.array([r["lr"] for r in rs])); A = np.column_stack([np.ones(len(y)), x, lrl])
        res = np.abs(y - A @ np.linalg.lstsq(A, y, rcond=None)[0]); rho_S = float(spearmanr(S_old, res).correlation)
        print(f"   S diagnostic (report): Spearman(S_old, |residual of the E_old fit|) = {rho_S:+.3f} -> high-S runs {'do' if rho_S > 0.3 else 'do not'} fall off the endpoint curve (threshold 0.3, report only)")
        R[name] = dict(ok0=ok0, v1=v1, gap=gap, r2=r2, flips=flips, v2=v2, rho=rho, rho_S=rho_S)
    n = len(ds); print("\n" + "-" * 112)
    dec = [d for d in ds if R[d]["ok0"]]
    print(f"T1x-0 precondition: decidable on {len(dec)}/{n} carriers" + ("" if len(dec) == n else f" (not decidable: {[d for d in ds if not R[d]['ok0']]})"))
    passes = [d for d in dec if R[d]["v1"] == "PASS"]; fails = [d for d in dec if R[d]["v1"] == "FAIL"]
    print("T1x-1 path vs endpoint (held-out, lr controlled): " + ", ".join(f"{d}:{R[d]['gap']:+.3f} {R[d]['v1']}" for d in ds)
          + f" -> PASS on {len(passes)}/{len(dec)}, FAIL on {len(fails)}/{len(dec)} -> {'PASS' if len(passes) == len(dec) and dec else ('FAIL' if fails else 'INCONCLUSIVE')}")
    print("T1x-2 fixed-lr arm: " + ", ".join(f"{d}:{'PASS' if R[d]['v2'] else 'FAIL'} (rho C_old {R[d]['rho']['C_old']:+.3f}, E_new {R[d]['rho']['E_new']:+.3f}, E_old {R[d]['rho']['E_old']:+.3f})" for d in ds) + f" -> PASS on {sum(R[d]['v2'] for d in ds)}/{n}")
    print("T1x-3 surrogate control: prereg/t1x/gate_T1.txt (S-H must FAIL, S-H2 must PASS; the gate reads its own verdict)")
    tot_flips = sum(R[d]["flips"] for d in ds)
    print(f"T1x-S sensitivity: T1x-1 flips in {tot_flips} of {9 * n} cells -> {'FRAGILE' if tot_flips > 1 else 'not fragile'}")
    print("T1x-D S diagnostic: " + ", ".join(f"{d}:{R[d]['rho_S']:+.3f}" for d in ds) + " (report only)")
    print(f"summary: T1x-1 {'PASS' if len(passes) == len(dec) and dec else ('FAIL' if fails else 'INCONCLUSIVE')} on {len(dec)} decidable carriers; T1x-2 PASS on {sum(R[d]['v2'] for d in ds)}/{n}; fragile {tot_flips > 1}")


def synthetic(n=2400, d=6, seed=0):
    rng = np.random.default_rng(seed); X = rng.standard_normal((n, d)); X[:, 0] = np.linspace(-2, 2, n) + 0.05 * rng.standard_normal(n)
    y = np.sin(2 * X[:, 0]) + 0.5 * X[:, 1] * X[:, 2] + 0.3 * rng.standard_normal(n); return X, y


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        X, y = synthetic(); tasks = make_tasks(X, y); base = train_base(tasks, X.shape[1]); fisher = base.per_sample_sq_grad(tasks[0][0], tasks[0][1])
        for sch in SCHEDULES: print(json.dumps(run(sch, 0.01, 0, tasks, base, fisher)))
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/t1x_smokefull.jsonl"
        X, y = synthetic(); tasks = make_tasks(X, y)
        with open(outp, "w") as out: run_all("synthetic", tasks, dict(file="synthetic", sha256="none", n=len(y), n_file=len(y), d=X.shape[1], rows_dropped_nan=0), out)
        score([outp])
    elif cmd == "all":
        name = sys.argv[2]; outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/t1x/results_{name}.jsonl"
        X, y, meta = load_pmlb_regression(name); tasks = make_tasks(X, y)
        with open(outp, "w") as out: run_all(name, tasks, meta, out)
    elif cmd == "score": score(sys.argv[2:])
    else: raise SystemExit(__doc__)
