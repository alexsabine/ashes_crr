"""Study SEC7 — the clipped SEC on a stream where the criterion can fail: a seeded random class order (task 1 is two classes
drawn at random, not the two largest) and balanced accuracy as the primary metric, with the must-fail control 'edge' as the
instrument gate. prereg/sec7/DEV_DECLARATION.md (pushed at d377662; Amendment 1 at 77f32cb: the family is the never-opened
eligible datasets of OpenML studies 445, 454 and 293). Prompt-log entry 257; P2 of Applied_Suite/PROGRAMME.md.

WHAT IS FROZEN BESIDE THIS FILE (runs/sec7/frozen/): byte copies of runs/sec6/frozen/*.py. SEC6's scorer is imported for its
constants, its loader path (load_carrier, with Amendment 1's d = 0 rule) and its development cache; the learner loop is
re-implemented here as run7() so that it records per-class recall. Every arm's mechanics are SEC6's, unchanged:
  fixed           SEC1's 'fixed' (raw accumulated Fisher at weight lambda)
  fixed_clip      SEC6's 'fixed_clip' (SEC4's clip at w = lambda)
  bayes           SEC1's 'bayes' (raw Laplace, w = 1/2 on the task-size-weighted raw Fisher)
  bayes_sec       SEC1's 'bayes_sec' (unguarded SEC)
  bayes_sec_clip  SEC4's run_guard(variant='clip') (the clipped SEC; kappa, window cells)
  eq              SEC1's 'eq' (the registered rule, Omega = value)
  si1c            SEC6's SI-1C (SI, c = 1, xi = 1e-3, Omega floored at 0 and capped at kappa / (lr c))
  ar1b            SEC6's AR1-B (w = 1 / (2 lr max_k imp_k) on the raw accumulated Fisher, at each task start)
  edge            SEC6's 'edge' (P1's M6: after task 1 every coordinate at kappa / (lr w), w = 1/2; the must-fail control)
THE STREAM (DEV_DECLARATION.md, "What changes"). After SCL3's loader, SEC1's class rule and SEC1's split and standardisation
(all unchanged: the same rows, split and scaling as SEC1-SEC6), the K used labels are relabelled y -> perm[y] with
perm = numpy default_rng([20261002, openml_id]).permutation(K), fixed per carrier (every seed, every arm); SEC1's tasks are
then consecutive pairs of the permuted labels. With the identity permutation run7 is SEC1 / SEC4 / SEC6 bit for bit (D-ID).
THE METRIC. Balanced accuracy (the mean over the K classes of per-class recall on the test set, x 100; chance 100 / K) is
primary; raw accuracy is recorded and printed beside it. The tuned lambda, the tuned clipped lambda (SEC1's two-stage grid:
EWC_COARSE, then EWC_REFINE around the coarse best, ties to the smallest), the transferred lambda and the 3-point sweep's best
are all chosen on balanced accuracy.

    uv run python studies/sec7/sec7_score.py devid > prereg/sec7/dev/devid.txt           # D-ID (identity permutation, raw acc)
    uv run python studies/sec7/sec7_score.py devlist                                     # the SEEN (study, id) pairs
    uv run python studies/sec7/sec7_score.py devgate <study> <id> --out F                # D-GATE-7's arms on one SEEN carrier
    uv run python studies/sec7/sec7_score.py devgatereport <F ...>                        # the D-GATE-7 block (OPEN / CLOSED)
    uv run python studies/sec7/sec7_score.py devrun <study> <id> --out F                 # D-RUN: the remaining arms, one carrier
    uv run python studies/sec7/sec7_score.py devreport <devid.txt> <gate7.txt> <F ...>   # dev_SEC7.txt (records merged by carrier)
    uv run python studies/sec7/sec7_score.py all <OpenML id> [--out F] [--times F]
    uv run python studies/sec7/sec7_score.py score <results.jsonl ...>
    uv run python studies/sec7/sec7_score.py check                                       # raw files against the manifest; d = 0 self-test
    uv run python studies/sec7/sec7_score.py smokefull [--out F]
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np  # noqa: E402

_HERE = Path(__file__).resolve()
FROZEN = _HERE.parent.name == "frozen"
ROOT = _HERE.parents[3] if FROZEN else _HERE.parents[2]
sys.path.insert(0, str(_HERE.parent if FROZEN else ROOT / "runs" / "sec6" / "frozen"))
import sec6_score as P6  # noqa: E402  (SEC6's scorer, frozen: SEC5's, SEC4's, SCL3's loader and SEC1's learner beneath it)
P5 = P6.P5; P4 = P6.P4; P3 = P6.P3; L = P6.L; S = P6.S

# ---------------------------------------------------------------- registered constants (prereg/sec7/DEV_DECLARATION.md)
KAPPA = P6.KAPPA; KAPPA_CELLS = P6.KAPPA_CELLS; KEEP_CELLS = P6.KEEP_CELLS
THREE = P6.THREE; SHARE = P6.SHARE; MIN_B = P6.MIN_B; MIN_N = P6.MIN_N; DIV_FRAC = P6.DIV_FRAC; SEEDS = S.SEEDS
PERM_SEED = 20261002             # perm = default_rng([PERM_SEED, openml_id]).permutation(K)
SI_C = P6.SI_C["si1c"]; SI_XI = P6.SI_XI["si1c"]   # SI-1C's c = 1, xi = 1e-3 (SEC6)
FLOOR_STEPS = 3                  # D-FLOOR: floor-bound if the tuned lambda's balanced accuracy - 100/K < 3 steps
ARMS7 = ("fixed", "fixed_clip", "bayes", "bayes_sec", "bayes_sec_clip", "eq", "si1c", "ar1b", "edge")
NAMES = {"bayes_sec_clip": "clipped SEC", "bayes_sec": "unguarded SEC", "bayes": "raw Laplace", "eq": "rule Ω=1", "si1c": "SI-1C",
         "ar1b": "AR1-B", "edge": "edge (control)"}
B_SET = ("si1c", "ar1b", "bayes")    # SEC7-B: the clipped SEC strictly ahead in count of each
D0_REASON = P6.D0_REASON
DEV_TABLES = P6.DEV_TABLES
DATASETS = {183: ('abalone', 10, 2), 279: ('meta_stream_intervals.arff', 10, 2), 1534: ('volcanoes-b4', 4, 2), 1538: ('volcanoes-d1', 4, 2),
            1542: ('volcanoes-e1', 4, 2), 1552: ('autoUniv-au7-1100', 4, 2), 40985: ('tamilnadu-electricity', 10, 2),
            46608: ('drug_reviews_druglib_com', 10, 2), 46684: ('HolisticBias', 4, 2), 46709: ('SOCC', 10, 2), 46745: ('Advanced_IoT_Dataset', 6, 2),
            46761: ('mental_health_detection', 10, 2)}
            # OpenML id -> (name, K requested, classes per task): prereg/sec7/carrier_selection.txt (default_rng(20261002), 12 of 23)
TIMES: list = []


def perm_of(openml_id, K):
    return np.random.default_rng([PERM_SEED, int(openml_id)]).permutation(K)


def relabel(data, perm):
    """y -> perm[y] on the training and test labels (after SEC1's split; the rows and the scaling are unchanged)."""
    Xtr, ytr, Xte, yte = data
    return Xtr, perm[ytr], Xte, perm[yte]


def _recall(net, Xte, yte, K):
    with np.errstate(all="ignore"):
        z = net.forward(Xte)[1]
    if not np.all(np.isfinite(z)):
        return [0.0] * K                                      # as SEC1's net.acc: a non-finite output scores 0
    pred = z.argmax(1)
    return [float(np.mean(pred[yte == c] == c)) if np.any(yte == c) else float("nan") for c in range(K)]


def run7(seed, Xtr, ytr, Xte, yte, K, per_task, arm, value=None, fs=S.FS, fe=S.FE, kappa=KAPPA, lr=S.LR, bs=S.BS, epochs=S.EPOCHS,
         hidden=S.HID, smooth=S.SMOOTH, wcap=S.WCAP):
    """One run of any SEC7 arm; the loop is SEC1's run() (same rng consumption order, MLP, minibatching, Fisher estimator and
    SEC calibration) and each arm's lines are SEC1's, SEC4's run_guard's or SEC6's run_b's, unchanged. value: lambda for 'fixed'
    and 'fixed_clip', Omega for 'eq'."""
    if arm not in ARMS7:
        raise ValueError(arm)
    t0 = time.process_time()
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    importance = np.zeros(n); imp_bayes = np.zeros(n); theta_star = None
    Omega = np.zeros(n); omega = np.zeros(n); theta_prev_end = net.flat().copy()          # SI-1C
    ema_p = ema_q = None                                                                     # eq
    wlog = []; svals = []; cvals = []; rhovals = []; n_fallback = 0
    fired = 0; margins = []; n_capped = []; n_floored = []; w_task = []; edge_max = []
    si = arm == "si1c"
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            imp_used = None; w = None
            if theta_star is not None:
                if arm == "fixed":
                    imp_used = importance; w = value
                elif arm == "fixed_clip":                                                    # SEC6: SEC4's clip at w = lambda
                    imp_used = importance; w = value; cap = kappa / (lr * w)
                    if not (lr * w * float(np.max(importance)) < kappa):
                        n_capped.append(int(np.sum(importance > cap))); imp_used = np.minimum(importance, cap); fired += 1
                    else:
                        n_capped.append(0)
                elif arm in ("bayes", "bayes_sec"):
                    imp_used = imp_bayes / n_task; w = S.BAYES_W
                elif arm == "bayes_sec_clip":                                                # SEC4's run_guard('clip')
                    imp_used = imp_bayes / n_task; w = S.BAYES_W; cap = kappa / (lr * S.BAYES_W)
                    m = lr * S.BAYES_W * float(np.max(imp_used)); margins.append(m)
                    if not (m < kappa):
                        imp_used = np.minimum(imp_used, cap); fired += 1
                elif arm == "eq":
                    imp_used = importance                                                    # w per step (SEC1's estimator)
                elif arm == "si1c":                                                          # SEC6's SI-1C
                    w = SI_C; cap = KAPPA / (lr * w); nc = int(np.sum(Omega > cap)); nf = int(np.sum(Omega < 0))
                    imp_used = np.clip(Omega, 0, cap); n_capped.append(nc); n_floored.append(nf); fired += int(nc > 0 or nf > 0)
                elif arm == "ar1b":                                                          # SEC6's AR1-B
                    imp_used = importance; w = float(np.float64(1.0) / (2 * lr * np.max(imp_used)))
                else:                                                                        # edge: SEC6's (P1's M6)
                    w = S.BAYES_W; cap = kappa / (lr * w); m = lr * w * float(np.max(imp_bayes / n_task)); margins.append(m)
                    fired += int(not (m < kappa)); imp_used = np.full(n, cap)
                if arm != "eq":
                    w_task.append(float(w)); edge_max.append(float(np.max(lr * 2 * w * imp_used)))
            total = epochs * int(math.ceil(n_task / bs)); n_s = max(1, int(math.ceil(fs * total))); n_e = max(1, int(math.ceil(fe * total)))
            s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0
            for ep in range(epochs):
                perm_ = rng.permutation(ii_task)
                for t in range(0, len(perm_), bs):
                    ii = perm_[t:t + bs]; x, y = Xtr[ii], ytr[ii]
                    L_p, g_p = S.ce_loss_grad(net, x, y)
                    theta_before = net.flat()
                    if k_step < n_s: s_th += theta_before; s_g += g_p
                    if k_step >= total - n_e: e_th += theta_before; e_g += g_p
                    k_step += 1
                    if theta_star is None:
                        theta_after = theta_before - lr * g_p
                    else:
                        dth = theta_before - theta_star; g_q = 2 * imp_used * dth
                        if arm == "eq":
                            ema_p = g_p if ema_p is None else smooth * ema_p + (1 - smooth) * g_p
                            ema_q = g_q if ema_q is None else smooth * ema_q + (1 - smooth) * g_q
                            w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), S.DEN_FLOOR), wcap)
                        wlog.append(float(w))
                        theta_after = theta_before - lr * (g_p + w * g_q)
                    net.set_flat(theta_after)
                    if si: omega += -g_p * (theta_after - theta_before)
            theta_now = net.flat().copy()
            if si:
                Delta = theta_now - theta_prev_end
                Omega = Omega + omega / (Delta ** 2 + SI_XI)
                omega = np.zeros(n); theta_prev_end = theta_now
            f = np.zeros(n)
            for _ in range(S.N_FISHER):
                ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += S.ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
            f_task = f / S.N_FISHER * bs
            dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)
            c = float(dg @ dth) / nn if nn > S.DTH_FLOOR else float("nan"); rho = float((f_task * dth) @ dth) / nn if nn > S.DTH_FLOOR else float("nan")
            if nn > S.DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho
            else: s = 1.0; n_fallback += 1
            svals.append(float(s)); cvals.append(c if np.isfinite(c) else None); rhovals.append(rho if np.isfinite(rho) else None)
            sc = s if arm in ("bayes_sec", "bayes_sec_clip", "edge") else 1.0
            importance = importance + sc * f_task; imp_bayes = imp_bayes + n_task * sc * f_task
            theta_star = theta_now
    recall = _recall(net, Xte, yte, K)
    default = {"fixed": value, "fixed_clip": value, "eq": value, "bayes_sec_clip": kappa, "edge": kappa, "si1c": SI_C}.get(arm, 0.0)
    rec = dict(mode=arm, value=float(default), seed=int(seed), fs=float(fs), fe=float(fe), acc=100 * net.acc(Xte, yte),
               bal=100 * float(np.nanmean(recall)), recall=recall, s=svals, c=cvals, rho=rhovals, n_fallback=int(n_fallback),
               guard_fired=int(fired), guard_margins=[round(x, 6) for x in margins], n_capped=n_capped, n_floored=n_floored,
               w_task=w_task, edge_max=edge_max, w_med=float(np.median(wlog)) if wlog else None, finite=bool(np.all(np.isfinite(net.flat()))))
    TIMES.append(dict(mode=rec["mode"], value=rec["value"], seed=rec["seed"], fs=rec["fs"], fe=rec["fe"], cpu_s=time.process_time() - t0))
    return rec


def grid7(data, K, per_task, arm, emit):
    """SEC1's two-stage grid for 'fixed' or 'fixed_clip', chosen on balanced accuracy: every lambda of EWC_COARSE at seeds 0-4;
    best = max over EWC_COARSE (in its order: ties to the smallest) of the seed-mean balanced accuracy; then round(best * f, 6)
    for f in EWC_REFINE unless within 1e-6 (relative) of a coarse value. Returns {round(lambda, 6): [records]}."""
    done = {}

    def go(lam):
        for seed in SEEDS:
            o = run7(seed, *data, K, per_task, arm, value=lam); emit(o); done.setdefault(round(o["value"], 6), []).append(o)

    for w in S.EWC_COARSE: go(w)
    best = max(S.EWC_COARSE, key=lambda w: np.mean([o["bal"] for o in done[round(w, 6)]]))
    for fct in S.EWC_REFINE:
        w = round(best * fct, 6)
        if all(abs(w - c) / c > 1e-6 for c in S.EWC_COARSE): go(w)
    return done


def primary_arms(data, K, per_task, emit, arms):
    """Every seed of the non-grid arms (the order is fixed: seed-major)."""
    for seed in SEEDS:
        for arm in arms:
            if arm == "bayes_sec_clip":
                for kap, (fs, fe) in [(KAPPA, (S.FS, S.FE))] + [(KAPPA, c) for c in KEEP_CELLS] + [(k, (S.FS, S.FE)) for k in KAPPA_CELLS]:
                    emit(run7(seed, *data, K, per_task, arm, fs=fs, fe=fe, kappa=kap))
            elif arm == "bayes_sec_clip_primary":
                emit(run7(seed, *data, K, per_task, "bayes_sec_clip"))
            elif arm == "bayes_sec_clip_cells":
                for kap, (fs, fe) in [(KAPPA, c) for c in KEEP_CELLS] + [(k, (S.FS, S.FE)) for k in KAPPA_CELLS]:
                    emit(run7(seed, *data, K, per_task, "bayes_sec_clip", fs=fs, fe=fe, kappa=kap))
            else:
                emit(run7(seed, *data, K, per_task, arm, value=1.0 if arm == "eq" else None))


# ---------------------------------------------------------------- the carriers of the family
def run_carrier(did, out, tout, synthetic=False, table=None):
    if synthetic:
        X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); meta = dict(file="synthetic", sha256="none", openml_id=did, **meta); name = "synthetic"
    else:
        name, Xs, ys, meta = P6.load_carrier(did, DATASETS if table is None else table)
    per_task = 2
    if meta["excluded"]:
        print(json.dumps(dict(dataset=name, **meta)), file=out, flush=True); return
    K = meta["classes_used"]; perm = perm_of(did, K); data = relabel(S.split_standardise(Xs, ys, K), perm)
    hdr = dict(dataset=name, **meta, K=K, per_task=per_task, perm=[int(v) for v in perm], perm_seed=[PERM_SEED, int(did)], n_train=int(len(data[1])),
               n_test=int(len(data[3])), lr=S.LR, bs=S.BS, hidden=S.HID, epochs=S.EPOCHS, n_fisher=S.N_FISHER, bayes_w=S.BAYES_W, fs=S.FS, fe=S.FE,
               kappa=KAPPA, uv_lock_sha256=S.sha256(ROOT / "uv.lock"))
    print(json.dumps(hdr), file=out, flush=True)

    def emit(o):
        o["dataset"] = name; print(json.dumps(o), file=out, flush=True)
    grid7(data, K, per_task, "fixed", emit)
    grid7(data, K, per_task, "fixed_clip", emit)
    primary_arms(data, K, per_task, emit, ("bayes_sec_clip", "bayes", "bayes_sec", "eq", "si1c", "ar1b", "edge"))
    for t in TIMES:
        t["dataset"] = name; print(json.dumps(t), file=tout, flush=True)
    TIMES.clear()


# ---------------------------------------------------------------- development on SEEN data (DEV_DECLARATION.md)
def _pinned_header(study, did):
    with open(ROOT / "runs" / study / f"results_{did}.jsonl") as f:
        return json.loads(f.readline())


def load_seen(study, did):
    """A SEEN carrier through SEC6's cache (its study's frozen loader, SEC1's split), with the raw file's sha256 checked against
    the pinned header and the loaded shapes against it; None if the loader excluded it. The labels are NOT permuted here."""
    hdr = _pinned_header(study, did)
    if hdr.get("excluded"):
        return None
    if S.sha256(ROOT / hdr["file"]) != hdr["sha256"]:
        raise RuntimeError(f"{study} {did}: raw file sha256 differs from the pinned header")
    d = P6._load_seen(study, did)
    Xtr, ytr, Xte, yte, K, name = d
    if (K, len(ytr), len(yte), Xtr.shape[1]) != (hdr["K"], hdr["n_train"], hdr["n_test"], hdr["d"]):
        raise RuntimeError(f"{study} {did}: loaded shapes differ from the pinned header")
    return (Xtr, ytr, Xte, yte), K, hdr["per_task"], name


def dev_list():
    """The 30 SEEN carriers the loaders keep, costliest first (n_train x d, from the pinned headers) for the parallel runs."""
    out = [(study, did, _pinned_header(study, did)) for study, table in DEV_TABLES for did in table]
    out = [(s, d, h["n_train"] * h["d"]) for s, d, h in out if not h.get("excluded")]
    return [(s, d) for s, d, _ in sorted(out, key=lambda t: -t[2])]


ID_PINNED = (("sec4", 377), ("sec4", 46906), ("sec5", 1549), ("sec5", 41671))      # D-ID against SEC4 / SEC5's pinned records
ID_SEC6 = (("sec4", 377), ("sec5", 41671))                                         # D-ID against SEC6's development records
ID_LAMBDAS = (1.0, 100.0)                                                          # 'fixed' at two lambda values
ID_CLIP_LAMBDAS = (1.0, 1000.0)                                                    # 'fixed_clip' at two lambda values


def devid():
    """D-ID: with the identity permutation, run7's raw accuracy equals the pinned records bit for bit on seed 0."""
    print("D-ID (prereg/sec7/DEV_DECLARATION.md): run7 with the IDENTITY permutation, raw accuracy, seed 0, against pinned records")
    held = []
    for study, did in ID_PINNED:
        data, K, per_task, name = load_seen(study, did)
        rows = P6._pinned_rows(ROOT / "runs" / study / f"results_{did}.jsonl")
        pick = lambda mode, value: [r for r in rows if r["mode"] == mode and r["seed"] == 0 and r["fs"] == S.FS and r["fe"] == S.FE  # noqa: E731
                                    and abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value))]
        checks = [("bayes_sec_clip", None, pick("bayes_sec_clip", KAPPA)), ("bayes", None, pick("bayes", 0.0))] \
            + [("fixed", lam, pick("fixed", lam)) for lam in ID_LAMBDAS] + [("bayes_sec", None, pick("bayes_sec", 0.0)), ("eq", 1.0, pick("eq", 1.0))]
        for arm, lam, pin in checks:
            o = run7(0, *data, K, per_task, arm, value=lam)
            same = len(pin) == 1 and o["acc"] == pin[0]["acc"]; held.append(same)
            print(f"   {study} {did} {name} (K {K}) {arm}{'' if lam is None else ' ' + format(lam, 'g')}: run7 {o['acc']!r} pinned {pin[0]['acc'] if pin else None!r} "
                  f"-> {'equal' if same else 'DIFFERS'}; s also equal: {'yes' if pin and o['s'] == pin[0]['s'] else 'no'}", flush=True)
    edge_txt = (ROOT / "prereg" / "sec6" / "dev" / "devid_edge.txt").read_text()
    for study, did in ID_SEC6:
        data, K, per_task, name = load_seen(study, did)
        dev = json.loads((ROOT / "prereg" / "sec6" / "dev" / f"dev_{study}_{did}.jsonl").read_text())
        s1c = json.loads((ROOT / "prereg" / "sec6" / "dev" / f"devsi1c_{study}_{did}.jsonl").read_text())
        fcl = json.loads((ROOT / "prereg" / "sec6" / "dev" / f"devfclip_{study}_{did}.jsonl").read_text())
        m = re.search(rf"^\s+{study} {did} \S+ \(K \d+\) seed 0: edge (\S+) ", edge_txt, re.M)
        grid = {g["value"]: g for g in fcl["arms"]["fixed_clip"]["grid"]}
        checks = [("si1c", None, s1c["arms"]["si1c"]["seeds"][0]), ("ar1b", None, dev["arms"]["ar1b"]["seeds"][0]),
                  ("edge", None, float(m[1]) if m else None)] + [("fixed_clip", lam, grid[lam]["seeds"][0] if lam in grid else None) for lam in ID_CLIP_LAMBDAS]
        for arm, lam, pin in checks:
            o = run7(0, *data, K, per_task, arm, value=lam)
            same = pin is not None and o["acc"] == pin; held.append(same)
            print(f"   {study} {did} {name} (K {K}) {arm}{'' if lam is None else ' ' + format(lam, 'g')}: run7 {o['acc']!r} SEC6 development record {pin!r} "
                  f"-> {'equal' if same else 'DIFFERS'}", flush=True)
    TIMES.clear()
    print(f"D-ID -> {'holds' if all(held) else 'FAILS'} ({sum(held)}/{len(held)} equal; SEC4/SEC5 records on {len(ID_PINNED)} carriers, "
          f"SEC6 development records on {len(ID_SEC6)})")


def _summ(recs):
    return dict(bal=[o["bal"] for o in recs], acc=[o["acc"] for o in recs], finite=[o["finite"] for o in recs], fired=[o["guard_fired"] for o in recs])


def dev_gate(study, did, out):
    """D-GATE-7's arms on one SEEN carrier with the declared permutation: the fixed grid (tuned on balanced accuracy), edge and
    the clipped SEC at the primary window, seeds 0-4."""
    data, K, per_task, name = load_seen(study, did)
    perm = perm_of(did, K); data = relabel(data, perm)
    runs = []
    done = grid7(data, K, per_task, "fixed", runs.append)
    grid = [dict(value=v, **_summ(done[v])) for v in sorted(done)]
    best = max(grid, key=lambda g: np.mean(g["bal"]))
    ra = []; primary_arms(data, K, per_task, ra.append, ("edge", "bayes_sec_clip_primary"))
    arms = {a: _summ([o for o in ra if o["mode"] == a]) for a in ("edge", "bayes_sec_clip")}
    TIMES.clear()
    print(json.dumps(dict(study=study, did=did, name=name, K=K, perm=[int(v) for v in perm], tuned=best["value"], tacc=float(np.mean(best["bal"])),
                          step=S.step_of(best["bal"]), grid=grid, arms=arms)), file=out, flush=True)


def dev_run(study, did, out):
    """D-RUN: the remaining arms on one SEEN carrier with the declared permutation (seeds 0-4): bayes, bayes_sec, eq, si1c,
    ar1b, the clipped SEC's window and kappa cells, and the fixed_clip grid. Nothing is chosen from it."""
    data, K, per_task, name = load_seen(study, did)
    perm = perm_of(did, K); data = relabel(data, perm)
    ra = []; primary_arms(data, K, per_task, ra.append, ("bayes", "bayes_sec", "eq", "si1c", "ar1b", "bayes_sec_clip_cells"))
    arms = {a: _summ([o for o in ra if o["mode"] == a]) for a in ("bayes", "bayes_sec", "eq", "si1c", "ar1b")}
    cells = {}
    for o in ra:
        if o["mode"] == "bayes_sec_clip":
            cells.setdefault(f"{o['value']:g}/{o['fs']:g}/{o['fe']:g}", []).append(o)
    arms["cells"] = {k: _summ(v) for k, v in cells.items()}
    runs = []; done = grid7(data, K, per_task, "fixed_clip", runs.append)
    grid = [dict(value=v, **_summ(done[v])) for v in sorted(done)]
    best = max(grid, key=lambda g: np.mean(g["bal"]))
    arms["fixed_clip"] = dict(grid=grid, tuned=best["value"], tacc=float(np.mean(best["bal"])), step=S.step_of(best["bal"]))
    TIMES.clear()
    print(json.dumps(dict(study=study, did=did, name=name, K=K, run=arms)), file=out, flush=True)


def _merged(paths):
    by = {}
    for p in paths:
        for line in open(p):
            if line.strip():
                r = json.loads(line); by.setdefault((r["study"], r["did"]), {}).update(r)
    order = [t for t, _ in DEV_TABLES]
    return sorted(by.values(), key=lambda r: (order.index(r["study"]), r["name"].lower()))


def gate_report(paths):
    recs = [r for r in _merged(paths) if "tacc" in r]
    N = len(recs)
    print(f"D-GATE-7 (prereg/sec7/DEV_DECLARATION.md) on the {N} SEEN carriers: random class order (default_rng([20261002, openml_id])), balanced accuracy; "
          "tuned lambda on balanced accuracy (SEC1's two-stage grid), step = max(1, 2 SE) at it")
    nb = lambda a, r: a - r["tacc"] > -r["step"]  # noqa: E731
    behind = []; floor = []
    for r in recs:
        e = float(np.mean(r["arms"]["edge"]["bal"])); g = float(np.mean(r["arms"]["bayes_sec_clip"]["bal"])); ch = 100 / r["K"]
        fb = r["tacc"] - ch < FLOOR_STEPS * r["step"]
        if not nb(e, r): behind.append(r["name"])
        if fb: floor.append(r["name"])
        print(f"   [{r['name']}] ({r['study']}, K {r['K']}, perm {r['perm']}) tuned lambda {r['tuned']:g}: balanced {r['tacc']:.4f}, step {r['step']:.4f}; "
              f"chance {ch:.2f} (tuned − chance {(r['tacc'] - ch) / r['step']:+.2f} steps: {'FLOOR-BOUND' if fb else 'not floor-bound'}); "
              f"edge {e:.4f} ({e - r['tacc']:+.4f}: {'not behind' if nb(e, r) else 'BEHIND'}); clipped SEC {g:.4f} ({g - r['tacc']:+.4f}: "
              f"{'not behind' if nb(g, r) else 'BEHIND'})")
    d_fail = len(behind) > N / 2; d_floor = len(floor) < N / 4
    kc = sum(nb(float(np.mean(r["arms"]["bayes_sec_clip"]["bal"])), r) for r in recs)
    print(f"D-FAIL: edge behind the tuned lambda on {len(behind)}/{N} (need more than half, > {N / 2:g}) -> {'holds' if d_fail else 'FAILS'}: {behind}")
    print(f"D-FLOOR: floor-bound (tuned balanced − 100/K < {FLOOR_STEPS} steps) on {len(floor)}/{N} (need fewer than a quarter, < {N / 4:g}) -> "
          f"{'holds' if d_floor else 'FAILS'}: {floor}")
    print(f"   (report) the clipped SEC not behind the tuned lambda (balanced) on {kc}/{N}; edge not behind on {N - len(behind)}/{N}")
    print(f"D-GATE-7 {'OPEN' if (d_fail and d_floor and N == 30) else 'CLOSED'}" + ("" if N == 30 else f" (only {N} of 30 carriers)"))


def dev_report(idpath, gatepath, paths):
    idtxt = Path(idpath).read_text(); gatetxt = Path(gatepath).read_text()
    recs = _merged(paths); N = len(recs)
    print("SEC7 development stage (prereg/sec7/DEV_DECLARATION.md, Amendment 1) on the SEEN carriers of SCL3, SEC3, SEC4 and SEC5, seeds 0-4, with the "
          "declared random class order and balanced accuracy. Nothing is chosen from D-RUN; it is not evidence and adds no ledger row.")
    print("=" * 118); print(idtxt.rstrip()); print("-" * 118); print(gatetxt.rstrip()); print("=" * 118)
    arms = ("bayes_sec_clip", "bayes_sec", "bayes", "eq", "si1c", "ar1b", "edge")
    get = lambda r, a: (r["arms"][a] if a in ("edge", "bayes_sec_clip") else r.get("run", {}).get(a))  # noqa: E731
    fmt = lambda xs: " ".join("%.2f" % v for v in xs)  # noqa: E731
    have_run = [r for r in recs if "run" in r]
    for r in recs:
        fc = r.get("run", {}).get("fixed_clip")
        print(f"[{r['name']}] ({r['study']}, K {r['K']}) tuned lambda {r['tuned']:g}: balanced {r['tacc']:.4f}, step {r['step']:.4f}"
              + (f"; tuned clipped lambda {fc['tuned']:g}: {fc['tacc']:.4f}, step_c {fc['step']:.4f} ({(fc['tacc'] - r['tacc']) / r['step']:+.2f} steps)" if fc else ""))
        for a in arms:
            x = get(r, a)
            if not x: print(f"     {NAMES[a]:15}: not run"); continue
            b = float(np.mean(x["bal"]))
            print(f"     {NAMES[a]:15}: balanced {b:.4f} [{fmt(x['bal'])}] −tuned {b - r['tacc']:+.4f}" + (f"; −tuned clipped {b - fc['tacc']:+.4f}" if fc else "")
                  + f"; raw {np.mean(x['acc']):.4f}; non-finite {sum(not f for f in x['finite'])}; divergent {'yes' if any(v < DIV_FRAC * r['tacc'] for v in x['bal']) else 'no'}")
        for k, x in sorted(r.get("run", {}).get("cells", {}).items()):
            print(f"     clip cell {k}: balanced {np.mean(x['bal']):.4f} −tuned {np.mean(x['bal']) - r['tacc']:+.4f}")
    print("=" * 118)
    print(f"carriers {N}; with D-RUN records {len(have_run)}")
    for a in arms:
        hv = [r for r in recs if get(r, a)]
        k = sum(float(np.mean(get(r, a)["bal"])) - r["tacc"] > -r["step"] for r in hv)
        hc = [r for r in hv if r.get("run", {}).get("fixed_clip")]
        kc = sum(float(np.mean(get(r, a)["bal"])) - r["run"]["fixed_clip"]["tacc"] > -r["run"]["fixed_clip"]["step"] for r in hc)
        dv = [r["name"] for r in hv if any(v < DIV_FRAC * r["tacc"] for v in get(r, a)["bal"])]
        print(f"{NAMES[a]:15}: not behind the tuned lambda {k}/{len(hv)}; not behind the tuned clipped lambda {kc}/{len(hc)}; divergent ({len(dv)}): {dv}")
    old = (ROOT / "prereg" / "sec6" / "dev_SEC6.txt").read_text().splitlines()
    keep = [ln.strip() for ln in old if re.match(r"^(SI-1C|AR1-B) +: not behind the tuned lambda|^\(pinned, not rerun\) (clipped SEC|raw Laplace|unguarded SEC): not behind \d", ln)]
    mline = [ln.strip() for ln in (ROOT / "SEC_Analysis" / "checks" / "m_checks.txt").read_text().splitlines() if ln.strip().startswith("M6: not behind")]
    print("the old stream (largest classes first, raw accuracy), for comparison: prereg/sec6/dev_SEC6.txt reads " + " | ".join(keep)
          + "; SEC_Analysis/checks/m_checks.txt reads " + (mline[0] if mline else "(line not found)"))


# ---------------------------------------------------------------- scoring (SEC7-G, GC, 1, C, B, 2, T, P, S, K)
def _arm(rows, mode, value=None, fs=S.FS, fe=S.FE, field="bal"):
    v = [r[field] for r in rows if r.get("mode") == mode and (value is None or abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value)))
         and r["fs"] == fs and r["fe"] == fe]
    return (float(np.mean(v)), v) if v else (None, [])


def _grid(rows, mode, field):
    g = {}
    for r in rows:
        if r.get("mode") == mode and r["fs"] == S.FS and r["fe"] == S.FE: g.setdefault(r["value"], []).append(r[field])
    return {w: v for w, v in sorted(g.items())}


def score(paths):
    by = {}; reasons = {}; hdrs = {}
    for p in paths:
        for line in open(p):
            o = json.loads(line)
            if "mode" in o: by.setdefault(o["dataset"], []).append(o)
            elif o.get("excluded"): by.setdefault(o["dataset"], None); reasons[o["dataset"]] = o.get("exclusion_reason")
            else: hdrs.setdefault(o["dataset"], o)
    times = {}
    for p in paths:
        tp = Path(str(p).replace("results_", "times_"))
        if tp != Path(p) and tp.exists():
            for line in open(tp):
                t = json.loads(line); times.setdefault(t["dataset"], []).append(t)
    excl = sorted(d for d, v in by.items() if v is None); names = sorted(d for d, v in by.items() if v is not None)
    G = "bayes_sec_clip"
    print("=" * 118)
    print("SEC7 scoring (prereg/sec7/DEV_DECLARATION.md and PREREG.md): the clipped SEC (kappa 0.5) on a random class order with balanced accuracy; "
          "the instrument gate edge (SEC7-G) first")
    print("=" * 118)
    print(f"carriers scored {len(names)}: {names}; excluded {len(excl)}: {excl}; of them by the d = 0 rule (SEC6 Amendment 1): "
          f"{[d for d in excl if reasons.get(d) == D0_REASON]}")
    R = {}
    for d in names:
        rows = by[d]; h = hdrs.get(d, {})
        g = _grid(rows, "fixed", "bal"); gm = {w: float(np.mean(v)) for w, v in g.items()}; tuned = max(gm, key=gm.get)
        gr = _grid(rows, "fixed", "acc"); grm = {w: float(np.mean(v)) for w, v in gr.items()}; tuned_r = max(grm, key=grm.get)
        gc = _grid(rows, "fixed_clip", "bal"); gcm = {w: float(np.mean(v)) for w, v in gc.items()}; tuned_c = max(gcm, key=gcm.get)
        r = dict(K=h.get("K"), perm=h.get("perm"), tuned=tuned, tacc=gm[tuned], step=S.step_of(g[tuned]), grid=gm, n_cfg=len(gm),
                 tuned_r=tuned_r, tacc_r=grm[tuned_r], step_r=S.step_of(gr[tuned_r]),
                 tuned_c=tuned_c, tacc_c=gcm[tuned_c], step_c=S.step_of(gc[tuned_c]), grid_c=gcm,
                 fired=sum(o["guard_fired"] for o in rows if o.get("mode") == G and o["fs"] == S.FS and o["fe"] == S.FE and abs(o["value"] - KAPPA) < 1e-9))
        r["a"] = {m: _arm(rows, m, KAPPA if m == G else None) for m in ("bayes_sec_clip", "bayes_sec", "bayes", "eq", "si1c", "ar1b", "edge")}
        r["araw"] = {m: _arm(rows, m, KAPPA if m == G else None, field="acc")[0] for m in r["a"]}
        r["sens"] = {("window", c): _arm(rows, G, KAPPA, *c)[0] for c in KEEP_CELLS}
        r["sens"].update({("kappa", k): _arm(rows, G, k)[0] for k in KAPPA_CELLS})
        r["kseeds"] = {k: _arm(rows, G, k)[1] for k in KAPPA_CELLS}
        r["best3"] = max(THREE, key=lambda w: gm[w]) if all(w in gm for w in THREE) else None
        r["best3_acc"] = gm[r["best3"]] if r["best3"] else None
        r["chance"] = 100 / r["K"] if r["K"] else float("nan")
        R[d] = r
    for d in names:
        oth = [math.log(R[o]["tuned"]) for o in names if o != d]
        if oth:
            lam = math.exp(float(np.median(oth))); snap = min(S.EWC_COARSE, key=lambda w: abs(math.log(w) - math.log(lam)))
            R[d]["loco"] = snap; R[d]["loco_acc"] = R[d]["grid"][snap]
        else:
            R[d]["loco"] = None; R[d]["loco_acc"] = None
    fmt = lambda xs: " ".join("%.2f" % v for v in xs)  # noqa: E731
    for d in names:
        r = R[d]
        print(f"\n[{d}] K {r['K']} (chance {r['chance']:.2f}), class order perm {r['perm']}; tuned lambda (balanced) {r['tuned']:g} ({r['n_cfg']} configurations): "
              f"{r['tacc']:.4f}, step {r['step']:.4f}; tuned clipped lambda {r['tuned_c']:g}: {r['tacc_c']:.4f}, step_c {r['step_c']:.4f}")
        print("   balanced grid: " + "  ".join(f"{w:g}:{v:.2f}" for w, v in r["grid"].items()))
        print("   balanced clipped grid: " + "  ".join(f"{w:g}:{v:.2f}" for w, v in r["grid_c"].items()))
        for m, (a, seeds) in r["a"].items():
            print(f"   {NAMES[m]}: balanced {a:.4f} [{fmt(seeds)}] −tuned {a - r['tacc']:+.4f}; −tuned clipped {a - r['tacc_c']:+.4f}; raw {r['araw'][m]:.4f}"
                  + (f"; fired {r['fired']}" if m == G else ""))
        for c, v in r["sens"].items():
            print(f"   clip cell {c[0]} {c[1]}: balanced {v:.4f} −tuned {v - r['tacc']:+.4f}")
        if r["best3"] is not None:
            print(f"   3-point sweep: best {r['best3']:g} {r['best3_acc']:.4f}; clipped SEC − best3 {r['a'][G][0] - r['best3_acc']:+.4f}")
        if r["loco"] is not None:
            print(f"   transferred lambda {r['loco']:g}: {r['loco_acc']:.4f} −tuned {r['loco_acc'] - r['tacc']:+.4f}")
        print(f"   raw accuracy (report): tuned lambda on raw {r['tuned_r']:g}: {r['tacc_r']:.4f}, step {r['step_r']:.4f}")
    N = len(names); need = math.ceil(SHARE * N)
    nb = lambda a, r: a - r["tacc"] > -r["step"]  # noqa: E731
    nbc = lambda a, r: a - r["tacc_c"] > -r["step_c"]  # noqa: E731
    dv = lambda seeds, r: any(v < DIV_FRAC * r["tacc"] for v in seeds)  # noqa: E731
    ND = "NOT DECIDABLE (fewer than %d carriers scored)" % MIN_N
    print("\n" + "-" * 118)
    kg = sum(nb(R[d]["a"]["edge"][0], R[d]) for d in names); gate = kg >= need
    print(f"SEC7-G instrument gate: edge (a learner frozen after task 1) not behind the tuned lambda (balanced): {kg}/{N} (closes at {need}) -> "
          f"{'SEC7-G CLOSED' if gate else 'SEC7-G OPEN'}; " + ", ".join(f"{d}:{R[d]['a']['edge'][0] - R[d]['tacc']:+.4f} (step {R[d]['step']:.2f})" for d in names))
    mark = " [UNINFORMATIVE (a learner frozen after task 1 meets the same criterion; SEC7-G)]" if gate else ""
    k = sum(nb(R[d]["a"][G][0], R[d]) for d in names)
    v1 = ND if N < MIN_N else ("PASS" if k >= need else "FAIL")
    print(f"SEC7-1 tuning-free on balanced accuracy: the clipped SEC (kappa 0.5) not behind the tuned lambda: {k}/{N} (need {need}) -> {v1}{mark}; "
          + ", ".join(f"{d}:{R[d]['a'][G][0] - R[d]['tacc']:+.4f} (step {R[d]['step']:.2f})" for d in names))
    print("   beside it (report, balanced): " + "; ".join(f"{NAMES[m]} {sum(nb(R[d]['a'][m][0], R[d]) for d in names)}/{N}" for m in ("bayes_sec", "bayes", "eq", "si1c", "ar1b", "edge")))
    print("   beside it (report, raw accuracy against the tuned lambda chosen on raw accuracy): " + "; ".join(
        f"{NAMES[m]} {sum(R[d]['araw'][m] - R[d]['tacc_r'] > -R[d]['step_r'] for d in names)}/{N}" for m in R[names[0]]["a"]) if names else "")
    print("   floor (report): tuned balanced − chance in steps: " + ", ".join(f"{d}:{(R[d]['tacc'] - R[d]['chance']) / R[d]['step']:+.2f}" for d in names))
    kgc = sum(nbc(R[d]["a"]["edge"][0], R[d]) for d in names); gatec = kgc >= need
    print(f"SEC7-GC instrument gate against the tuned clipped lambda: edge not behind it: {kgc}/{N} (closes at {need}) -> {'SEC7-GC CLOSED' if gatec else 'SEC7-GC OPEN'}; "
          + ", ".join(f"{d}:{R[d]['a']['edge'][0] - R[d]['tacc_c']:+.4f} (step_c {R[d]['step_c']:.2f})" for d in names))
    markc = mark or (" [UNINFORMATIVE (a learner frozen after task 1 meets the same criterion; SEC7-GC)]" if gatec else "")
    kc = sum(nbc(R[d]["a"][G][0], R[d]) for d in names)
    vc = ND if N < MIN_N else ("PASS" if kc >= need else "FAIL")
    print(f"SEC7-C the clipped SEC not behind the tuned clipped lambda: {kc}/{N} (need {need}) -> {vc}{markc}; "
          + ", ".join(f"{d}:{R[d]['a'][G][0] - R[d]['tacc_c']:+.4f} (step_c {R[d]['step_c']:.2f})" for d in names))
    if v1 == "PASS" and vc == "FAIL":
        print("   SEC7-1 rests on the clip (SEC7-C fails)")
    kb = {m: sum(nb(R[d]["a"][m][0], R[d]) for d in names) for m in B_SET}
    beats = {m: k > kb[m] for m in B_SET}
    vb = ND if N < MIN_N else ("PASS" if all(beats.values()) else "FAIL")
    print(f"SEC7-B the clipped SEC not behind the tuned lambda on {k}/{N}; " + "; ".join(f"{NAMES[m]} {kb[m]}/{N} (clipped SEC strictly more: {'yes' if beats[m] else 'NO'})"
                                                                                     for m in B_SET) + f" -> {vb}{mark} (PASS only if strictly more than each)")
    for m in B_SET + ("edge",):
        print(f"   {NAMES[m]}: −tuned " + ", ".join(f"{d}:{R[d]['a'][m][0] - R[d]['tacc']:+.4f}" for d in names)
              + f"; carriers with a seed below half the tuned balanced accuracy: {[d for d in names if dv(R[d]['a'][m][1], R[d])]}")
    div = [d for d in names if dv(R[d]["a"][G][1], R[d])]
    print(f"SEC7-2 no divergence: carriers with a clipped seed below half the tuned balanced accuracy: {div} ({len(div)}) -> {'PASS' if not div else 'FAIL'}{mark}; "
          f"unguarded (report): {[d for d in names if dv(R[d]['a']['bayes_sec'][1], R[d])]}")
    B = [d for d in names if R[d]["loco"] is not None and not nb(R[d]["loco_acc"], R[d])]
    if len(B) >= MIN_B:
        kt = sum(nb(R[d]["a"][G][0], R[d]) for d in B); needt = math.ceil(SHARE * len(B))
        print(f"SEC7-T the saving is SEC's: B = {B} ({len(B)}); clipped SEC not behind on {kt}/{len(B)} (need {needt}) -> {'PASS' if kt >= needt else 'FAIL'}{mark}")
    else:
        print(f"SEC7-T: NOT DECIDABLE (a transferred lambda is behind on only {len(B)} carriers, need >= {MIN_B}){mark}")
    kp = sum(R[d]["best3"] is not None and R[d]["a"][G][0] - R[d]["best3_acc"] > -R[d]["step"] for d in names)
    print(f"SEC7-P clipped SEC (1 configuration) not behind the 3-point mini-sweep (3): {kp}/{N} (need {need}) -> {'PASS' if kp >= need else 'FAIL'}{mark}")
    cells = [c for c in R[names[0]]["sens"]] if names else []
    flips = {c: sum(nb(R[d]["a"][G][0], R[d]) != nb(R[d]["sens"][c], R[d]) for d in names) for c in cells}
    tot = sum(flips.values())
    print(f"SEC7-S sensitivity over {len(cells)} cells x {N} carriers (3 window cells, kappa 0.25 and 1.0): flips in {tot} of {len(cells) * N} -> "
          f"{'FRAGILE' if tot > 1 else 'not fragile'}{mark}; by cell: " + ", ".join(f"{c[0]} {c[1]}: {v}" for c, v in flips.items()))
    for kk in KAPPA_CELLS:
        print(f"   kappa {kk:g}: not behind {sum(nb(R[d]['sens'][('kappa', kk)], R[d]) for d in names)}/{N}; carriers with a seed below half the tuned "
              f"balanced accuracy: {[d for d in names if dv(R[d]['kseeds'][kk], R[d])]}")
    pass1 = v1 == "PASS" and tot <= 1 and not div and not gate
    level = ("PASS-1 candidate (the report states the anchor and admissibility)" if pass1 else
             ("PASS-0 (not PASS-1: " + ", ".join(x for x, bad in (("fragile", tot > 1), ("divergence", bool(div)), ("SEC7-G CLOSED", gate)) if bad) + ")"
              if v1 == "PASS" else "no PASS"))
    print(f"SEC7-1 level as computed from SEC7-S, SEC7-2 and SEC7-G: {level} (a new result on a new stream, never a PASS-2 for SEC4-1)")
    if gate:
        print("   SEC7-G CLOSED: every row above is UNINFORMATIVE and claims no level above PASS-0")
    elif gatec:
        print("   SEC7-GC CLOSED: SEC7-C is UNINFORMATIVE and claims no level above PASS-0")
    print("SEC7-K compute (report; CPU seconds from the timing files):")
    for d in names:
        t = times.get(d, [])
        cpu = lambda mode, val=None: sum(x["cpu_s"] for x in t if x["mode"] == mode and x["fs"] == S.FS and x["fe"] == S.FE  # noqa: E731
                                         and (val is None or abs(x["value"] - val) <= 1e-6 * max(1.0, abs(val))))
        full = cpu("fixed"); gcpu = cpu(G, KAPPA)
        print(f"   {d}: full sweep ({R[d]['n_cfg']}) {full:.1f}, clipped SEC {gcpu:.1f}" + (f" (share {gcpu / full:.4f})" if full else "")
              + f"; tuned clipped sweep {cpu('fixed_clip'):.1f}; " + ", ".join(f"{NAMES[m]} {cpu(m):.1f}" for m in ("bayes", "bayes_sec", "eq", "si1c", "ar1b", "edge")))
    print("SEC7-E guard firings (report): " + "; ".join(f"{d}: {R[d]['fired']}" for d in names))


def d0_selftest():
    """SEC6 Amendment 1's d = 0 rule through SEC7's own load / run / score path, on two synthetic ARFF carriers written to a
    temporary folder (as SEC6's self-test): the d = 0 carrier is excluded with its reason before any run; the d = 1 carrier
    runs every SEC7 arm without error; score counts one scored and one excluded."""
    import contextlib
    import io
    import tempfile
    classes = ("a", "b", "c", "d"); n_per = 60
    table = {990001: ("selftest_d0", 4, 2), 990002: ("selftest_d1", 4, 2)}
    raw0 = L.RAW; res = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp); L.RAW = tmp
        try:
            for did, (name, _, _) in table.items():
                numeric = name.endswith("d1")
                lines = ["@relation selftest", "@attribute note string", "@attribute comment string"] + (["@attribute x numeric"] if numeric else []) \
                    + ["@attribute class {" + ",".join(classes) + "}", "@data"]
                for i in range(n_per * len(classes)):
                    c = i % len(classes)
                    lines.append(f"'note {i}','comment {i % 7}'" + (f",{c + ((i * 37) % 11) / 10}" if numeric else "") + f",{classes[c]}")
                (tmp / f"{did}_{name}.arff").write_text("\n".join(lines) + "\n")
                (tmp / f"{did}_{name}.json").write_text(json.dumps({"data_set_description": {"default_target_attribute": "class", "version": "1"}}))
                with open(tmp / f"results_{name}.jsonl", "w") as out, open(tmp / f"times_{name}.jsonl", "w") as tout:
                    run_carrier(did, out, tout, table=table)
                recs = [json.loads(line) for line in open(tmp / f"results_{name}.jsonl")]
                hdr = recs[0]; runs = [r for r in recs if "mode" in r]
                res[name] = dict(features_used=hdr["features_used"], excluded=hdr["excluded"], reason=hdr.get("exclusion_reason"), n_runs=len(runs),
                                 modes=sorted({r["mode"] for r in runs}), nonfinite=sum(not r.get("finite", True) for r in runs))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                score([tmp / "results_selftest_d0.jsonl", tmp / "results_selftest_d1.jsonl"])
            counted = [line for line in buf.getvalue().splitlines() if line.startswith("carriers scored")][0]
        finally:
            L.RAW = raw0
    r0, r1 = res["selftest_d0"], res["selftest_d1"]
    ok0 = r0["features_used"] == 0 and r0["excluded"] and r0["reason"] == D0_REASON and r0["n_runs"] == 0
    ok1 = r1["features_used"] == 1 and not r1["excluded"] and r1["n_runs"] > 0 and all(m in r1["modes"] for m in ARMS7)
    okc = counted.startswith("carriers scored 1: ['selftest_d1']; excluded 1: ['selftest_d0']")
    print(f"d = 0 self-test: selftest_d0 (2 string attributes, 4-class target, {n_per * len(classes)} rows): features_used {r0['features_used']}, excluded "
          f"{r0['excluded']}, reason {r0['reason']!r}, run records {r0['n_runs']} -> {'as required' if ok0 else 'NOT as required'}")
    print(f"d = 1 self-test: selftest_d1 (one numeric attribute added): features_used {r1['features_used']}, excluded {r1['excluded']}; every SEC7 arm ran: "
          f"{r1['n_runs']} run records, modes {r1['modes']}, non-finite {r1['nonfinite']} -> {'as required' if ok1 else 'NOT as required'}")
    print(f"score on the two: {counted} -> {'as required' if okc else 'NOT as required'}")
    print(f"d = 0 rule self-test -> {'holds' if (ok0 and ok1 and okc) else 'FAILS'}")
    return ok0 and ok1 and okc


def data_check():
    man = {}
    for line in open(ROOT / "data" / "manifests" / "sec7.sha256"):
        if line.strip(): h_, pth = line.split()[:2]; man[pth] = h_
    bad = []
    for did, (name, _, _) in DATASETS.items():
        for ext in ("arff", "json"):
            pth = f"data/raw/openml/{did}_{name}.{ext}"; got = S.sha256(ROOT / pth) if (ROOT / pth).exists() else None
            print(f"{did} {name} .{ext}: sha256 {got} manifest {man.get(pth)} -> {'ok' if got and got == man.get(pth) else 'MISMATCH'}")
            if not got or got != man.get(pth): bad.append(f"{name}.{ext}")
    print("data check: " + (f"all {2 * len(DATASETS)} raw files match data/manifests/sec7.sha256" if not bad else f"MISMATCH {bad}: the study stops"))
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    if cmd == "devid": devid()
    elif cmd == "devlist": print("\n".join(f"{s} {d}" for s, d in dev_list()))
    elif cmd == "devgate":
        with open(outp, "w") as out: dev_gate(sys.argv[2], int(sys.argv[3]), out)
    elif cmd == "devrun":
        with open(outp, "w") as out: dev_run(sys.argv[2], int(sys.argv[3]), out)
    elif cmd == "devgatereport": gate_report(sys.argv[2:])
    elif cmd == "devreport": dev_report(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif cmd == "check":
        ok = data_check(); ok = d0_selftest() and ok
        sys.exit(0 if ok else 1)
    elif cmd == "all":
        did = int(sys.argv[2]); outp = outp or f"runs/sec7/results_{did}.jsonl"
        tp = sys.argv[sys.argv.index("--times") + 1] if "--times" in sys.argv else outp.replace("results_", "times_")
        with open(outp, "w") as out, open(tp, "w") as tout: run_carrier(did, out, tout)
    elif cmd == "score": score(sys.argv[2:])
    elif cmd == "smokefull":
        outp = outp or "/tmp/results_sec7_smoke.jsonl"
        d0_selftest()
        with open(outp, "w") as out, open(outp.replace("results_", "times_"), "w") as tout: run_carrier(0, out, tout, synthetic=True)
        score([outp])
    else: raise SystemExit(__doc__)
