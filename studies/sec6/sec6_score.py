"""Study SEC6 — SEC4's clipped SEC replicated on a FIFTH unseen family (OpenML suite 454, then 445, by the rule in
prereg/sec6/DEV_DECLARATION.md), against the published tuning-free baselines closest to it (R7): Synaptic Intelligence (SI,
arXiv 1703.04200 v3) at c = 1 and at c = 0.1, and AR1's strength bound (arXiv 1806.08568 v3) as published and as a bound.
Owner request: prompt-log entry 257 ("We should then run more tests on sec4"); P2 of Applied_Suite/PROGRAMME.md;
prereg/sec6/DEV_DECLARATION.md (pushed at 66ff6c7 before any SEC6 code) fixes everything below.

WHAT IS FROZEN BESIDE THIS FILE (runs/sec6/frozen/): byte copies of runs/sec5/frozen/*.py (themselves byte copies of SEC4's).
The primary arm is SEC4's run_guard(variant='clip', kappa=0.5), imported unchanged. This file adds only:
  (1) run_b(): SEC1's run() loop (runs/sec5/frozen/sec1_score.py: same rng consumption order, same MLP, same minibatching,
      same Fisher estimator and its draws, same SEC calibration arithmetic, recorded) with the four baseline penalties of
      DEV_DECLARATION.md, each in SEC1's parametrisation (penalty gradient w * 2 * imp * (theta - theta*)):
        'si1'   SI, c = 1, xi = 1e-3: per step omega += -g_p * (theta_after - theta_before), g_p the clean present-task
                minibatch gradient, theta_after - theta_before the update actually applied; at each task end
                Omega += omega / (Delta**2 + xi), Delta = theta(task end) - theta(previous task end) (task 1: theta at
                training start), omega reset; imp = Omega (summed over past tasks, not task-size weighted), w = c,
                theta* = theta at the previous task's end
        'si01'  SI, c = 0.1, xi = 0.1
        'ar1p'  AR1 as published: imp = min(mean over past tasks of f_task, 0.001) elementwise, w = 1 / (2 * lr * 0.001)
        'ar1b'  AR1's bound as the strength: imp = the raw accumulated Fisher exactly as SEC1's 'fixed' arm accumulates it
                (sum of f_task), w = 1 / (2 * lr * max_k imp_k) recomputed at each task start
      None of them is clipped. The extra accumulations consume no training rng, so for the same w the trajectory is SEC1's
      (D-MAP: si1 with c forced to 0 equals SEC1's run('fixed', 0.0) bit for bit).
  (2) the P1-conditional hook: CARRIED (filled by the lead from SEC_Analysis/checks/m_checks.json by the declared rule) and
      run_carried(), which runs each carried arm through m_checks.py's run function.
  (3) the development stage on SEEN data (devid, devmap, devone, devreport; output prereg/sec6/dev_SEC6.txt).
  (4) run_carrier() and score() for the fifth family: SEC1's run_all (every arm, unchanged); the clip at the primary window,
      at SEC4's 3 retained window cells and at kappa 0.25 and 1.0; the four baselines and every CARRIED arm at the primary
      window; CPU timing to the times file only (never the results file, R9).

    uv run python studies/sec6/sec6_score.py devid  > prereg/sec6/dev/devid.txt        # D-ID (seed 0 of 14 + 2 SEC1 carriers)
    uv run python studies/sec6/sec6_score.py devmap > prereg/sec6/dev/devmap.txt       # D-MAP on SEC1's synthetic stream
    uv run python studies/sec6/sec6_score.py devlist                                   # the SEEN (study, id) pairs of D-RUN
    uv run python studies/sec6/sec6_score.py devone <study> <OpenML id> --out F        # D-RUN on one SEEN carrier (JSON line)
    uv run python studies/sec6/sec6_score.py devreport <devid.txt> <devmap.txt> <F ...> # dev_SEC6.txt
    uv run python studies/sec6/sec6_score.py dev                                       # all of the above, one process
    uv run python studies/sec6/sec6_score.py all <OpenML id> [--out F] [--times F]
    uv run python studies/sec6/sec6_score.py score <results.jsonl ...>
    uv run python studies/sec6/sec6_score.py check
    uv run python studies/sec6/sec6_score.py smokefull [--out F]
"""
from __future__ import annotations

import importlib
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
sys.path.insert(0, str(_HERE.parent if FROZEN else ROOT / "runs" / "sec5" / "frozen"))
import sec5_score as P5  # noqa: E402  (SEC5's scorer, unchanged: it loads SEC4's scorer, SCL3's loader and SEC1's learner)
P4 = P5.P4; P3 = P5.P3; L = P5.L; S = P5.S

# ---------------------------------------------------------------- registered constants (prereg/sec6/DEV_DECLARATION.md)
KAPPA = P4.KAPPA                 # 0.5, SEC4's clip margin: the primary arm, unchanged
KAPPA_CELLS = P5.KAPPA_CELLS     # (0.25, 1.0), SEC5's kappa sweep
KEEP_CELLS = P4.KEEP_CELLS       # SEC4's three retained window cells
THREE = P4.THREE; SHARE = P4.SHARE; MIN_B = P4.MIN_B; MIN_N = P4.MIN_N; DIV_FRAC = P4.DIV_FRAC; SEEDS = S.SEEDS
SI_C = {"si1": 1.0, "si01": 0.1}            # SI's strength c: 1 ("equal weighting of old and new memories"); 0.1 (permuted MNIST)
SI_XI = {"si1": 1e-3, "si01": 0.1}          # SI's damping xi: 1e-3 (split MNIST); 0.1 (permuted MNIST, with c = 0.1)
AR1_MAXF = 0.001                            # AR1's clip of the averaged Fisher ("Fk values are averaged and clipped to 0.001")
BASELINES = ("si1", "si01", "ar1p", "ar1b")  # SI-1, SI-0.1, AR1-P, AR1-B
BASELINE_NAMES = {"si1": "SI-1", "si01": "SI-0.1", "ar1p": "AR1-P", "ar1b": "AR1-B"}
SEC1_DID = ("led7", "yeast")                # D-ID's two SEC1 carriers (runs/sec1 pinned records): small, 5 and 3 tasks

# ---------------------------------------------------------------- the P1-conditional arms (DEV_DECLARATION.md, section 3)
# >>> FILLED BY THE LEAD BEFORE THE HASH, from SEC_Analysis/checks/m_checks.json, by the rule fixed in DEV_DECLARATION.md and
# >>> SEC_Analysis/DECLARATION.md: M1 (model-Fisher Laplace) and M2 (endpoint-curvature SEC) are carried if not behind the
# >>> tuned lambda on at least (the clipped SEC's count - 1) of the 30 SEEN carriers; M4 (the arc secant) if ahead of the
# >>> clipped SEC by more than a step on at least 3 of them. This file does not read m_checks.json: the tuple IS the record.
CARRIED: tuple = ()              # the arm names exactly as m_checks.py's run function takes them, e.g. ("m1", "m2")
M_RUN = "run_m"                  # >>> the lead sets the name of m_checks.py's run function when CARRIED is filled; it is called
#                                    as M_RUN(seed, Xtr, ytr, Xte, yte, K, per_task, arm, fs=..., fe=...) and must return a
#                                    record dict with 'acc' (test accuracy in %), 'seed', 'fs', 'fe'. m_checks.py is frozen
#                                    beside this file (runs/sec6/frozen/) when CARRIED is not empty.

# ---------------------------------------------------------------- the fifth family (prereg/sec6/carrier_selection.txt)
DATASETS = {46584: ('Student_Performance_on_an_Entrance_Examination', 4, 2), 46593: ('HCV_data', 4, 2), 46597: ('Estimation_of_Obesity_Levels', 6, 2),
            46603: ('regensburg_pediatric_appendicitis', 4, 2), 46652: ('news_channel', 6, 2), 46653: ('wine_reviews', 10, 2), 46676: ('WBCAtt', 4, 2),
            46686: ('DBPedia', 10, 2), 46708: ('Wikipedia_Talk_Labels', 10, 2), 46721: ('Mental_Health_Dataset', 4, 2),
            46737: ('agriculture_dataset_karnataka', 10, 2), 46762: ('air-quality-and-pollution-assessment', 4, 2)}
            # OpenML id -> (name, K requested, classes per task): the declared draw default_rng(20261001), 12 of 19 eligible in study 454

# ---------------------------------------------------------------- the SEEN development carriers (D-ID, D-RUN)
DEV_TABLES = (("scl3", dict(P3.SCL3_DATASETS)), ("sec3", dict(P3.DATASETS)), ("sec4", dict(P4.DATASETS)), ("sec5", dict(P5.DATASETS)))
DEV_CACHE = Path("/tmp/claude-0/rrm_cache")   # npz cache outside the repository (Relational_Reference_Memory/checks/t_lib.py's)


def run_b(seed, Xtr, ytr, Xte, yte, K, per_task, arm, fs=S.FS, fe=S.FE, si_c=None, lr=S.LR, bs=S.BS, epochs=S.EPOCHS, hidden=S.HID):
    """SEC1's run() (runs/sec5/frozen/sec1_score.py) with a baseline penalty. Every line not marked B is SEC1's; the lines
    marked B compute the baseline's imp and w (at each task start) or accumulate SI's path integral (per step, task end).
    si_c (D-MAP only) overrides SI's c."""
    if arm not in BASELINES:
        raise ValueError(arm)
    t0 = time.process_time()
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    importance = np.zeros(n); theta_star = None
    si = arm in SI_C                                                                                  # B
    c_si = (SI_C[arm] if si_c is None else float(si_c)) if si else None; xi = SI_XI.get(arm)          # B
    Omega = np.zeros(n); omega = np.zeros(n); theta_prev_end = net.flat().copy()                      # B (SI)
    f_sum = np.zeros(n); n_past = 0                                                                   # B (AR1-P)
    wlog = []; svals = []; cvals = []; rhovals = []; n_fallback = 0
    w_task = []; imp_max = []; imp_min = []; edge = []                                                # B (record)
    w = None; imp_used = None
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            if theta_star is not None:                                                                # B
                if si:
                    imp_used = Omega; w = c_si
                elif arm == "ar1p":
                    imp_used = np.minimum(f_sum / n_past, AR1_MAXF); w = 1.0 / (2 * lr * AR1_MAXF)
                else:                                                                                 # ar1b
                    imp_used = importance; w = float(np.float64(1.0) / (2 * lr * np.max(imp_used)))
                w_task.append(float(w)); imp_max.append(float(np.max(imp_used))); imp_min.append(float(np.min(imp_used)))
                edge.append(float(np.max(lr * 2 * w * imp_used)))
            total = epochs * int(math.ceil(n_task / bs)); n_s = max(1, int(math.ceil(fs * total))); n_e = max(1, int(math.ceil(fe * total)))
            s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0
            for ep in range(epochs):
                perm = rng.permutation(ii_task)
                for t in range(0, len(perm), bs):
                    ii = perm[t:t + bs]; x, y = Xtr[ii], ytr[ii]
                    L_p, g_p = S.ce_loss_grad(net, x, y)
                    theta_before = net.flat()
                    if k_step < n_s: s_th += theta_before; s_g += g_p
                    if k_step >= total - n_e: e_th += theta_before; e_g += g_p
                    k_step += 1
                    if theta_star is None:
                        theta_after = theta_before - lr * g_p
                    else:
                        dth = theta_before - theta_star; g_q = 2 * imp_used * dth
                        wlog.append(float(w))
                        theta_after = theta_before - lr * (g_p + w * g_q)
                    net.set_flat(theta_after)
                    if si: omega += -g_p * (theta_after - theta_before)                              # B (SI's path integral)
            theta_now = net.flat().copy()
            if si:                                                                                    # B (SI's consolidation)
                Delta = theta_now - theta_prev_end
                Omega = Omega + omega / (Delta ** 2 + xi)
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
            sc = 1.0                                                                                  # SEC1's 'fixed' arm
            importance = importance + sc * f_task
            f_sum = f_sum + f_task; n_past += 1                                                       # B (AR1-P)
            theta_star = theta_now
    value = c_si if si else (AR1_MAXF if arm == "ar1p" else 0.0)
    rec = dict(mode=arm, value=float(value), seed=int(seed), fs=float(fs), fe=float(fe), acc=100 * net.acc(Xte, yte),
               s=svals, c=cvals, rho=rhovals, n_fallback=int(n_fallback), w_task=w_task, imp_max=imp_max, imp_min=imp_min, edge=edge,
               xi=xi, w_med=float(np.median(wlog)) if wlog else None, finite=bool(np.all(np.isfinite(net.flat()))))
    P4.TIMES.append(dict(mode=rec["mode"], value=rec["value"], seed=rec["seed"], fs=rec["fs"], fe=rec["fe"], cpu_s=time.process_time() - t0))
    return rec


def clip_arm(seed, data, K, per_task, fs=S.FS, fe=S.FE, kappa=KAPPA):
    """The primary arm through SEC6's harness: SEC4's run_guard(variant='clip'), unchanged."""
    return P4.run_guard(seed, *data, K, per_task, "clip", fs=fs, fe=fe, kappa=kappa)


def _m_checks():
    where = str(_HERE.parent if FROZEN else ROOT / "SEC_Analysis" / "checks")
    if where not in sys.path: sys.path.insert(0, where)
    return importlib.import_module("m_checks")


def run_carried(arm, seed, data, K, per_task, fs=S.FS, fe=S.FE):
    """A carried P1 arm through m_checks.py's run function (named M_RUN); its record is kept whole, with mode 'carried_<arm>'
    (the original mode, if any, kept as 'm_mode')."""
    t0 = time.process_time()
    o = dict(getattr(_m_checks(), M_RUN)(seed, *data, K, per_task, arm, fs=fs, fe=fe))
    if "mode" in o: o["m_mode"] = o["mode"]
    o["mode"] = f"carried_{arm}"; o.setdefault("value", 0.0); o.setdefault("seed", int(seed)); o.setdefault("fs", float(fs)); o.setdefault("fe", float(fe))
    o.pop("arm", None)
    P4.TIMES.append(dict(mode=o["mode"], value=o["value"], seed=o["seed"], fs=o["fs"], fe=o["fe"], cpu_s=time.process_time() - t0))
    return o


# ---------------------------------------------------------------- development on SEEN data (DEV_DECLARATION.md)
def _load_seen(study, did):
    """A SEEN carrier through its study's frozen loader (SCL3's load_openml with the study's table, SEC1's split), cached as
    npz outside the repository (t_lib.load_seen_cached's cache and file names); None if the loader excludes it."""
    DEV_CACHE.mkdir(parents=True, exist_ok=True); f = DEV_CACHE / f"{study}_{did}.npz"
    if f.exists():
        z = np.load(f, allow_pickle=False)
        if int(z["excluded"]):
            return None
        return z["Xtr"], z["ytr"], z["Xte"], z["yte"], int(z["K"]), str(z["name"])
    table = dict(DEV_TABLES)[study]; L.DATASETS = table
    Xs, ys, meta = L.load_openml(did)
    if meta["excluded"]:
        np.savez(f, excluded=1); return None
    K = meta["classes_used"]; Xtr, ytr, Xte, yte = S.split_standardise(Xs, ys, K)
    np.savez(f, excluded=0, Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte, K=K, name=table[did][0])
    return Xtr, ytr, Xte, yte, K, table[did][0]


def _pinned_rows(path):
    """The SEC1-arm and guard records of a pinned results file (SCL3's operator-harness rows, labelled 'arm', skipped)."""
    return [r for r in (json.loads(line) for line in open(path) if line.strip()) if "mode" in r and "arm" not in r]


def _pinned_seeds(rows, mode, value, fs=S.FS, fe=S.FE):
    v = sorted((r for r in rows if r["mode"] == mode and abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value)) and r["fs"] == fs and r["fe"] == fe),
               key=lambda r: r["seed"])
    return [r["acc"] for r in v]


def _pinned_clip(study, did):
    """The clipped SEC's pinned seed accuracies: SEC4's and SEC5's results files, or SEC5's development records (prereg/sec5/dev,
    covered by SEC5's hash) for the SCL3 and SEC3 carriers."""
    if study in ("sec4", "sec5"):
        return _pinned_seeds(_pinned_rows(ROOT / "runs" / study / f"results_{did}.jsonl"), "bayes_sec_clip", KAPPA)
    p = ROOT / "prereg" / "sec5" / "dev" / f"dev_{study}_{did}.jsonl"
    return json.loads(p.read_text())["clip"]["seeds"] if p.exists() else []


def _synthetic_data():
    X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); K = meta["classes_used"]
    return S.split_standardise(Xs, ys, K), K, meta


def devid():
    """D-ID: the clipped SEC through SEC6's harness equals the pinned bayes_sec_clip accuracy bit for bit on seed 0 of every
    SEC4 and SEC5 carrier (14); SEC1's bayes_sec equals SEC1's pinned records on 2 SEC1 carriers."""
    print("D-ID (prereg/sec6/DEV_DECLARATION.md): the clipped SEC (kappa 0.5) through SEC6's harness against the pinned bayes_sec_clip, seed 0")
    held = []; excl = []
    for study in ("sec4", "sec5"):
        for did, (name, _, per_task) in dict(DEV_TABLES)[study].items():
            d = _load_seen(study, did)
            if d is None: excl.append(f"{study}:{name}"); continue
            Xtr, ytr, Xte, yte, K, _ = d
            pin = [r for r in _pinned_rows(ROOT / "runs" / study / f"results_{did}.jsonl") if r["mode"] == "bayes_sec_clip" and r["seed"] == 0
                   and r["fs"] == S.FS and r["fe"] == S.FE and abs(r["value"] - KAPPA) < 1e-9]
            o = clip_arm(0, (Xtr, ytr, Xte, yte), K, per_task)
            same = len(pin) == 1 and o["acc"] == pin[0]["acc"]
            extra = len(pin) == 1 and o["s"] == pin[0]["s"] and o["guard_fired"] == pin[0]["guard_fired"] and o["guard_margins"] == pin[0]["guard_margins"]
            held.append(same)
            print(f"   {study} {did} {name} (K {K}): rerun {o['acc']!r} pinned {pin[0]['acc'] if pin else None!r} -> {'equal' if same else 'DIFFERS'}"
                  f"; s, firings and margins also equal: {'yes' if extra else 'no'}", flush=True)
    P4.TIMES.clear()
    print(f"   loader-excluded (no pinned arm): {len(excl)} {excl}")
    ok1 = len(held) == 14 and all(held)
    print(f"D-ID clipped SEC: {sum(held)}/{len(held)} carriers equal (need 14/14) -> {'holds' if ok1 else 'FAILS'}")
    held2 = []
    for name in SEC1_DID:
        K_req, per_task = S.DATASETS[name]; X, y, meta = S.load_pmlb(name, K_req); K = meta["classes_used"]
        data = S.split_standardise(X, y, K)
        pin = [r for r in _pinned_rows(ROOT / "runs" / "sec1" / f"results_{name}.jsonl") if r["mode"] == "bayes_sec" and r["seed"] == 0
               and r["fs"] == S.FS and r["fe"] == S.FE and abs(r["value"]) < 1e-9]
        o = P3._run("bayes_sec", 0.0, 0, *data, K, per_task)
        same = len(pin) == 1 and o["acc"] == pin[0]["acc"]; extra = len(pin) == 1 and o["s"] == pin[0]["s"]
        held2.append(same)
        print(f"   sec1 {name} (K {K}): bayes_sec rerun {o['acc']!r} pinned {pin[0]['acc'] if pin else None!r} -> {'equal' if same else 'DIFFERS'}; s also equal: {'yes' if extra else 'no'}")
    ok2 = len(held2) == 2 and all(held2)
    print(f"D-ID SEC1 bayes_sec: {sum(held2)}/{len(held2)} carriers equal (need 2/2) -> {'holds' if ok2 else 'FAILS'}")
    held3 = []                          # report only (not part of the declared D-ID): the data cache D-RUN reads for SCL3 and SEC3
    for study in ("scl3", "sec3"):
        for did, (name, _, per_task) in dict(DEV_TABLES)[study].items():
            d = _load_seen(study, did)
            if d is None: continue
            Xtr, ytr, Xte, yte, K, _ = d
            pin = _pinned_clip(study, did); o = clip_arm(0, (Xtr, ytr, Xte, yte), K, per_task)
            held3.append(bool(pin) and o["acc"] == pin[0])
    P4.TIMES.clear()
    print(f"(report, not part of D-ID) the data D-RUN reads for the SCL3 and SEC3 carriers: the clipped SEC on seed 0 equals SEC5's pinned "
          f"development record (prereg/sec5/dev) on {sum(held3)}/{len(held3)}")
    print(f"D-ID -> {'holds' if (ok1 and ok2) else 'FAILS'}")


def devmap():
    """D-MAP on SEC1's synthetic stream (through SCL3's class selection, as SEC5's smoke), seeds 0-4."""
    data, K, _ = _synthetic_data()
    print(f"D-MAP (prereg/sec6/DEV_DECLARATION.md) on SEC1's synthetic stream (K {K}, {K // 2} tasks, seeds 0-4); lr {S.LR!r}")
    same = []; moved = []
    for seed in SEEDS:
        a = P3._run("fixed", 0.0, seed, *data, K, 2); b = run_b(seed, *data, K, 2, "si1", si_c=0.0); c1 = run_b(seed, *data, K, 2, "si1")
        same.append(a["acc"] == b["acc"] and a["s"] == b["s"] and a["c"] == b["c"] and a["rho"] == b["rho"] and a["finite"] == b["finite"])
        moved.append(c1["acc"] != a["acc"] or c1["s"] != a["s"])
        print(f"   seed {seed}: fine-tuning (fixed, w 0) {a['acc']!r}; SI-1 with c forced to 0 {b['acc']!r}; SI-1 (c 1) {c1['acc']!r}; "
              f"SI-1 max Omega per task {['%.6g' % v for v in c1['imp_max']]}, min {['%.6g' % v for v in c1['imp_min']]}")
    ok1 = all(same)
    print(f"D-MAP SI-1 with c forced to 0 equals SEC1's run('fixed', 0.0) (acc, s, c, rho): {sum(same)}/{len(same)} -> {'holds' if ok1 else 'FAILS'}; "
          f"SI-1 at c = 1 moves the run on {sum(moved)}/{len(moved)} seeds (report: the check is not vacuous)")
    dev_b = []
    for seed in SEEDS:
        o = run_b(seed, *data, K, 2, "ar1b")
        dev_b += [abs(e - 1.0) for e in o["edge"]]
        print(f"   seed {seed}: AR1-B w per task {[repr(w) for w in o['w_task']]}; max_k(lr 2 w imp_k) per task {[repr(e) for e in o['edge']]}; acc {o['acc']!r}")
    ok2 = len(dev_b) > 0 and max(dev_b) <= 1e-12
    print(f"D-MAP AR1-B: max_k(lr 2 w imp_k) = 1.0 at every task start: largest |deviation| {max(dev_b):.3e} (need <= 1e-12) -> {'holds' if ok2 else 'FAILS'}")
    mx = []
    for seed in SEEDS:
        o = run_b(seed, *data, K, 2, "ar1p")
        mx += o["imp_max"]
        print(f"   seed {seed}: AR1-P w {o['w_task'][0]!r}; max imp per task {[repr(v) for v in o['imp_max']]}; max_k(lr 2 w imp_k) {[repr(e) for e in o['edge']]}; acc {o['acc']!r}")
    ok3 = len(mx) > 0 and max(mx) <= AR1_MAXF
    print(f"D-MAP AR1-P: imp never above {AR1_MAXF}: largest {max(mx)!r} -> {'holds' if ok3 else 'FAILS'}")
    for arm in ("si01",):
        o = [run_b(seed, *data, K, 2, arm) for seed in SEEDS]
        print(f"   (report) {BASELINE_NAMES[arm]} (c {SI_C[arm]}, xi {SI_XI[arm]}) runs: acc {[round(x['acc'], 4) for x in o]}")
    P4.TIMES.clear()
    print(f"D-MAP -> {'holds' if (ok1 and ok2 and ok3) else 'FAILS'}")


def dev_list():
    return [(study, did) for study, table in DEV_TABLES for did in table]


def dev_one(study, did, out):
    table = dict(DEV_TABLES)[study]; name, _, per_task = table[did]
    d = _load_seen(study, did)
    if d is None:
        print(json.dumps(dict(study=study, did=did, name=name, excluded=True)), file=out, flush=True); return
    Xtr, ytr, Xte, yte, K, _ = d
    path = ROOT / "runs" / study / f"results_{did}.jsonl"
    tuned, tacc, step, _ = P4._pinned(path); rows = _pinned_rows(path)
    rec = dict(study=study, did=did, name=name, K=K, tuned=tuned, tacc=tacc, step=step,
               ref=dict(clip=_pinned_clip(study, did), bayes=_pinned_seeds(rows, "bayes", 0.0), bayes_sec=_pinned_seeds(rows, "bayes_sec", 0.0)), arms={})
    for arm in BASELINES:
        os_ = [run_b(s, Xtr, ytr, Xte, yte, K, per_task, arm) for s in SEEDS]
        rec["arms"][arm] = dict(acc=float(np.mean([o["acc"] for o in os_])), seeds=[o["acc"] for o in os_], finite=[o["finite"] for o in os_],
                                edge=[o["edge"] for o in os_], w_task=[o["w_task"] for o in os_], imp_min=[o["imp_min"] for o in os_])
    P4.TIMES.clear()
    print(json.dumps(rec), file=out, flush=True)


def dev_report(idpath, mappath, paths):
    idtxt = Path(idpath).read_text(); maptxt = Path(mappath).read_text()
    d_id = idtxt.strip().endswith("D-ID -> holds"); d_map = maptxt.strip().endswith("D-MAP -> holds")
    recs = [json.loads(line) for p in paths for line in open(p) if line.strip()]
    order = [t for t, _ in DEV_TABLES]
    recs.sort(key=lambda r: (order.index(r["study"]), r["name"].lower()))
    excl = [f"{r['study']}:{r['name']}" for r in recs if r.get("excluded")]; recs = [r for r in recs if not r.get("excluded")]
    print("SEC6 development stage (prereg/sec6/DEV_DECLARATION.md) on SEEN data only: D-ID, D-MAP and D-RUN (the published baselines "
          "SI-1, SI-0.1, AR1-P, AR1-B on the SEEN carriers of SCL3, SEC3, SEC4 and SEC5, seeds 0-4); tuned lambda and step from pinned results")
    print("Nothing is chosen from D-RUN: every baseline's constants come from its paper. D-RUN is not evidence and adds no ledger row.")
    print("=" * 118)
    print(idtxt.rstrip()); print("-" * 118); print(maptxt.rstrip()); print("=" * 118)
    fmt = lambda xs: " ".join("%.2f" % a for a in xs)  # noqa: E731
    div = lambda seeds, r: any((a < DIV_FRAC * r["tacc"]) or not math.isfinite(a) for a in seeds)  # noqa: E731
    nb = lambda a, r: a - r["tacc"] > -r["step"]  # noqa: E731
    for r in recs:
        ref = r["ref"]
        print(f"[{r['name']}] ({r['study']}, K {r['K']}) tuned {r['tuned']:g}: {r['tacc']:.4f}, step {r['step']:.4f}; pinned: "
              + "; ".join(f"{lab} {np.mean(ref[k]) - r['tacc']:+.4f}" if ref[k] else f"{lab} none" for k, lab in (("clip", "clipped SEC"), ("bayes", "raw Laplace"), ("bayes_sec", "unguarded SEC"))))
        for arm in BASELINES:
            x = r["arms"][arm]; emax = max((max(e) for e in x["edge"] if e), default=float("nan"))
            print(f"     {BASELINE_NAMES[arm]:7}: {x['acc']:.4f} [{fmt(x['seeds'])}] −tuned {x['acc'] - r['tacc']:+.4f} ({'not behind' if nb(x['acc'], r) else 'BEHIND'})"
                  f"; largest max_k(lr 2 w imp_k) {emax:.4g}; non-finite seeds {sum(not f for f in x['finite'])}; divergent {'yes' if div(x['seeds'], r) else 'no'}"
                  + (f"; w per task (seed 0) {['%.4g' % w for w in x['w_task'][0]]}" if arm == "ar1b" else "")
                  + (f"; negative Omega entries at a task start (seed 0 min {min(x['imp_min'][0]):.3g})" if arm in SI_C and x["imp_min"][0] and min(x["imp_min"][0]) < 0 else ""))
    print("=" * 118)
    N = len(recs)
    print(f"carriers {N} (loader-excluded {len(excl)}: {excl})")
    for arm in BASELINES:
        k = sum(nb(r["arms"][arm]["acc"], r) for r in recs); dv = [r["name"] for r in recs if div(r["arms"][arm]["seeds"], r)]
        print(f"{BASELINE_NAMES[arm]:7}: not behind the tuned lambda {k}/{N}; carriers with a seed below {DIV_FRAC} x the tuned accuracy ({len(dv)}): {dv}")
    for key, lab in (("clip", "clipped SEC"), ("bayes", "raw Laplace"), ("bayes_sec", "unguarded SEC")):
        have = [r for r in recs if r["ref"][key]]
        k = sum(nb(float(np.mean(r["ref"][key])), r) for r in have); dv = [r["name"] for r in have if div(r["ref"][key], r)]
        print(f"(pinned, not rerun) {lab}: not behind {k}/{len(have)}; divergent carriers ({len(dv)}): {dv}")
    print(f"D-ID -> {'holds' if d_id else 'FAILS'}; D-MAP -> {'holds' if d_map else 'FAILS'}; D-RUN ran every baseline on {N} SEEN carriers, seeds 0-4")


# ---------------------------------------------------------------- the fifth family
def run_carrier(did, out, tout, synthetic=False):
    if synthetic:
        X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); meta = dict(file="synthetic", sha256="none", openml_id=did, **meta); name = "synthetic"
    else:
        L.DATASETS = DATASETS; name = DATASETS[did][0]; Xs, ys, meta = L.load_openml(did)
    per_task = 2
    if meta["excluded"]:
        print(json.dumps(dict(dataset=name, **meta)), file=out, flush=True); return
    K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    S.run = P4._timed
    try:
        S.run_all(name, data, K, per_task, meta, out)
    finally:
        S.run = P3._run
    for seed in SEEDS:
        arms = ([(KAPPA, (S.FS, S.FE))] + [(KAPPA, c) for c in KEEP_CELLS] + [(k, (S.FS, S.FE)) for k in KAPPA_CELLS])
        for kap, (fs, fe) in arms:
            o = clip_arm(seed, data, K, per_task, fs=fs, fe=fe, kappa=kap); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True)
        for arm in BASELINES:
            o = run_b(seed, *data, K, per_task, arm); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True)
        for arm in CARRIED:
            o = run_carried(arm, seed, data, K, per_task); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True)
    for t in P4.TIMES:
        t["dataset"] = name; print(json.dumps(t), file=tout, flush=True)
    P4.TIMES.clear()


def _mean(rows, mode, value=None, fs=S.FS, fe=S.FE):
    v = [r["acc"] for r in rows if r.get("mode") == mode and (value is None or abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value)))
         and r["fs"] == fs and r["fe"] == fe]
    return (float(np.mean(v)), v) if v else (None, [])


def _pinned_primary(study):
    """The clipped SEC's primary row of an earlier family, read from its pinned score file (R1): (k, N, need, verdict)."""
    p = ROOT / "runs" / study / "score.txt"
    for line in (p.read_text().splitlines() if p.exists() else []):
        m = re.match(rf"{study.upper()}-1 .*not behind the tuned lambda: (\d+)/(\d+) \(need (\d+)\) -> (\S+)", line)
        if m: return int(m[1]), int(m[2]), int(m[3]), m[4].rstrip(";")
    return None


def score(paths):
    by = {}
    for p in paths:
        for line in open(p):
            o = json.loads(line)
            if "mode" in o: by.setdefault(o["dataset"], []).append(o)
            elif o.get("excluded"): by.setdefault(o["dataset"], None)
    times = {}
    for p in paths:
        tp = Path(str(p).replace("results_", "times_"))
        if tp != Path(p) and tp.exists():
            for line in open(tp):
                t = json.loads(line); times.setdefault(t["dataset"], []).append(t)
    excl = sorted(d for d, v in by.items() if v is None); names = sorted(d for d, v in by.items() if v is not None)
    G = "bayes_sec_clip"
    others = [(b, BASELINE_NAMES[b]) for b in BASELINES] + [("bayes", "raw Laplace")] + [(f"carried_{a}", f"carried {a}") for a in CARRIED]
    print("=" * 118)
    print("SEC6 scoring (prereg/sec6/DEV_DECLARATION.md and PREREG.md): SEC4's clipped SEC (kappa 0.5) replicated on a fifth unseen family; kappa swept; "
          "against SI-1, SI-0.1, AR1-P, AR1-B, raw Laplace" + (f" and the carried P1 arms {list(CARRIED)}" if CARRIED else " (no P1 arm carried)"))
    print("=" * 118)
    print(f"carriers scored {len(names)}: {names}; excluded {len(excl)}: {excl}")
    R = {}
    for d in names:
        rows = by[d]
        g = {}
        for r in rows:
            if r.get("mode") == "fixed" and r["fs"] == S.FS and r["fe"] == S.FE: g.setdefault(r["value"], []).append(r["acc"])
        gm = {w: float(np.mean(v)) for w, v in sorted(g.items())}
        tuned = max(gm, key=gm.get); step = S.step_of(g[tuned])
        guard_rows = [o for o in rows if o.get("mode") == G and o["fs"] == S.FS and o["fe"] == S.FE and abs(o["value"] - KAPPA) < 1e-9]
        r = dict(step=step, tuned=tuned, tacc=gm[tuned], grid=gm, n_cfg=len(gm),
                 g=_mean(rows, G, KAPPA)[0], g_seeds=_mean(rows, G, KAPPA)[1], fired=sum(o["guard_fired"] for o in guard_rows),
                 u=_mean(rows, "bayes_sec", 0.0)[0], u_seeds=_mean(rows, "bayes_sec", 0.0)[1], eq=_mean(rows, "eq", 1.0)[0],
                 sens={("window", c): _mean(rows, G, KAPPA, *c)[0] for c in KEEP_CELLS},
                 best3=max(THREE, key=lambda w: gm[w]) if all(w in gm for w in THREE) else None, n_seeds=len(g[tuned]))
        r["sens"].update({("kappa", k): _mean(rows, G, k)[0] for k in KAPPA_CELLS})
        r["kseeds"] = {k: _mean(rows, G, k)[1] for k in KAPPA_CELLS}
        r["best3_acc"] = gm[r["best3"]] if r["best3"] else None
        r["b"] = {m: _mean(rows, m, 0.0 if m == "bayes" else None) for m, _ in others}
        r["b_edge"] = {m: max((max(o["edge"]) for o in rows if o.get("mode") == m and o["fs"] == S.FS and o["fe"] == S.FE and o.get("edge")), default=float("nan"))
                       for m in BASELINES}
        r["b_finite"] = {m: sum(not o.get("finite", True) for o in rows if o.get("mode") == m and o["fs"] == S.FS and o["fe"] == S.FE) for m, _ in others}
        R[d] = r
    for d in names:
        oth = [math.log(R[o]["tuned"]) for o in names if o != d]
        if oth:
            lam = math.exp(float(np.median(oth))); snap = min(S.EWC_COARSE, key=lambda w: abs(math.log(w) - math.log(lam)))
            R[d]["loco"] = snap; R[d]["loco_acc"] = R[d]["grid"][snap]
        else:
            R[d]["loco"] = None; R[d]["loco_acc"] = None
    fmt = lambda xs: " ".join("%.2f" % a for a in xs)  # noqa: E731
    for d in names:
        r = R[d]
        print(f"\n[{d}] step {r['step']:.4f}; tuned lambda {r['tuned']:g} ({r['n_cfg']} grid configurations): {r['tacc']:.4f}")
        print("   raw grid: " + "  ".join(f"{w:g}:{v:.2f}" for w, v in r["grid"].items()))
        print(f"   clipped SEC (kappa 0.5) {r['g']:.4f} [{fmt(r['g_seeds'])}] −tuned {r['g'] - r['tacc']:+.4f}; fired {r['fired']}")
        print(f"   unguarded SEC {r['u']:.4f} [{fmt(r['u_seeds'])}] −tuned {r['u'] - r['tacc']:+.4f}; rule Ω=1 {r['eq']:.4f} ({r['eq'] - r['tacc']:+.4f})")
        for m, lab in others:
            a, seeds = r["b"][m]
            print(f"   {lab}: {a:.4f} [{fmt(seeds)}] −tuned {a - r['tacc']:+.4f}; −clipped SEC {a - r['g']:+.4f}; non-finite seeds {r['b_finite'][m]}"
                  + (f"; largest max_k(lr 2 w imp_k) {r['b_edge'][m]:.4g}" if m in BASELINES else ""))
        for k in KAPPA_CELLS:
            print(f"   clip kappa {k:g}: {r['sens'][('kappa', k)]:.4f} [{fmt(r['kseeds'][k])}] −tuned {r['sens'][('kappa', k)] - r['tacc']:+.4f}")
        if r["best3"] is not None:
            print(f"   3-point sweep: best {r['best3']:g} {r['best3_acc']:.4f}; clipped SEC − best3 {r['g'] - r['best3_acc']:+.4f}")
        if r["loco"] is not None:
            print(f"   transferred lambda {r['loco']:g}: {r['loco_acc']:.4f} −tuned {r['loco_acc'] - r['tacc']:+.4f}")
        print("   window cells (clip) − tuned: " + "  ".join(f"{c[0]:g}/{c[1]:g}:{r['sens'][('window', c)] - r['tacc']:+.2f}" for c in KEEP_CELLS))
    N = len(names); need = math.ceil(SHARE * N)
    nb = lambda a, r: a - r["tacc"] > -r["step"]  # noqa: E731
    dv = lambda seeds, r: any(a < DIV_FRAC * r["tacc"] for a in seeds)  # noqa: E731  (SEC5-2's rule)
    print("\n" + "-" * 118)
    k = sum(nb(R[d]["g"], R[d]) for d in names)
    v1 = "NOT DECIDABLE (fewer than %d carriers scored)" % MIN_N if N < MIN_N else ("PASS" if k >= need else "FAIL")
    print(f"SEC6-1 tuning-free, the clipped SEC (kappa 0.5) not behind the tuned lambda: {k}/{N} (need {need}) -> {v1}; "
          + ", ".join(f"{d}:{R[d]['g'] - R[d]['tacc']:+.4f} (step {R[d]['step']:.2f})" for d in names))
    ku = sum(nb(R[d]["u"], R[d]) for d in names); ke = sum(nb(R[d]["eq"], R[d]) for d in names)
    print(f"   beside it (report): unguarded SEC {ku}/{N}; the rule Ω=1 {ke}/{N}")
    div = [d for d in names if dv(R[d]["g_seeds"], R[d])]
    divu = [d for d in names if dv(R[d]["u_seeds"], R[d])]
    print(f"SEC6-2 no divergence: carriers with a clipped seed below half the tuned accuracy: {div} ({len(div)}) -> {'PASS' if not div else 'FAIL'}; unguarded (report): {divu}")
    kb = {m: sum(nb(R[d]["b"][m][0], R[d]) for d in names) for m, _ in others}
    beats = {m: k > kb[m] for m, _ in others}
    print(f"SEC6-B against the published baselines: the clipped SEC not behind the tuned lambda on {k}/{N}; "
          + "; ".join(f"{lab} {kb[m]}/{N} (clipped SEC strictly more: {'yes' if beats[m] else 'NO'})" for m, lab in others)
          + f" -> {'PASS' if all(beats.values()) else 'FAIL'} (PASS only if strictly more than every one)")
    for m, lab in others:
        print(f"   {lab}: −tuned " + ", ".join(f"{d}:{R[d]['b'][m][0] - R[d]['tacc']:+.4f}" for d in names)
              + f"; carriers with a seed below half the tuned accuracy (SEC6-2's rule): {[d for d in names if dv(R[d]['b'][m][1], R[d])]}")
    B = [d for d in names if R[d]["loco"] is not None and not nb(R[d]["loco_acc"], R[d])]
    if len(B) >= MIN_B:
        kt = sum(nb(R[d]["g"], R[d]) for d in B); needt = math.ceil(SHARE * len(B))
        print(f"SEC6-T the saving is SEC's: B = {B} ({len(B)}); clipped SEC not behind on {kt}/{len(B)} (need {needt}) -> {'PASS' if kt >= needt else 'FAIL'}")
    else:
        print(f"SEC6-T: NOT DECIDABLE (a transferred lambda is behind on only {len(B)} carriers, need >= {MIN_B})")
    kp = sum(R[d]["best3"] is not None and R[d]["g"] - R[d]["best3_acc"] > -R[d]["step"] for d in names)
    print(f"SEC6-P clipped SEC (1 configuration) not behind the 3-point mini-sweep (3): {kp}/{N} (need {need}) -> {'PASS' if kp >= need else 'FAIL'}")
    cells = [c for c in R[names[0]]["sens"]] if names else []
    flips = {c: sum(nb(R[d]["g"], R[d]) != nb(R[d]["sens"][c], R[d]) for d in names) for c in cells}
    tot = sum(flips.values())
    print(f"SEC6-S sensitivity over {len(cells)} cells x {N} carriers (3 window cells, kappa 0.25 and 1.0): flips in {tot} of {len(cells) * N} -> "
          f"{'FRAGILE' if tot > 1 else 'not fragile'}; by cell: " + ", ".join(f"{c[0]} {c[1]}: {v}" for c, v in flips.items()))
    for kk in KAPPA_CELLS:
        kd = [d for d in names if dv(R[d]["kseeds"][kk], R[d])]
        print(f"   kappa {kk:g}: not behind {sum(nb(R[d]['sens'][('kappa', kk)], R[d]) for d in names)}/{N}; carriers with a seed below half the tuned accuracy: {kd}")
    pass1 = v1 == "PASS" and tot <= 1 and not div
    level = ("PASS-1 candidate (the report states the anchor and admissibility)" if pass1 else
             ("PASS-0 (not PASS-1: " + ", ".join(x for x, bad in (("fragile", tot > 1), ("divergence", bool(div))) if bad) + ")" if v1 == "PASS" else "no PASS"))
    print(f"SEC6-1 level as computed from SEC6-S and SEC6-2: {level}")
    p4 = _pinned_primary("sec4"); p5 = _pinned_primary("sec5")
    fam = [("SEC4-1", p4[3] if p4 else None), ("SEC5-1", p5[3] if p5 else None), ("SEC6-1", v1)]
    print("   the clipped SEC's family record (primary rows; SEC4 and SEC5 read from runs/sec4/score.txt and runs/sec5/score.txt): "
          + "; ".join(f"{i} {v}" + (f" ({p[0]}/{p[1]})" if p else "") for (i, v), p in zip(fam, (p4, p5, (k, N, need, v1))))
          + f" -> PASS on {sum(v == 'PASS' for _, v in fam)} of {len(fam)} families")
    if pass1 and p4 and p4[3] == "PASS":
        print("   by the letter of CLAUDE.md section 7, SEC4-1 (PASS-1, ledger) and SEC6-1 together are PASS-2 (a later day, a fresh pre-registration, "
              "the same frozen code); beside it: SEC5-1 "
              + (f"{p5[3]} on the fourth family ({p5[0]}/{p5[1]}, need {p5[2]})" if p5 else "not read (runs/sec5/score.txt missing)"))
    print("SEC6-K compute (report; CPU seconds from the timing files):")
    for d in names:
        t = times.get(d, [])
        cpu = lambda mode, val=None, fs=S.FS, fe=S.FE: sum(x["cpu_s"] for x in t if x["mode"] == mode and x["fs"] == fs and x["fe"] == fe  # noqa: E731
                                                          and (val is None or abs(x["value"] - val) <= 1e-6 * max(1.0, abs(val))))
        full = cpu("fixed"); gcpu = cpu(G, KAPPA); raw = cpu("bayes", 0.0)
        print(f"   {d}: configurations full sweep {R[d]['n_cfg']}, clipped SEC 1; CPU s full {full:.1f}, clipped SEC {gcpu:.1f}"
              + (f" (share {gcpu / full:.4f}), raw Laplace {raw:.1f} (overhead x{gcpu / raw if raw else float('nan'):.3f})" if full else "")
              + "; " + ", ".join(f"{BASELINE_NAMES[m]} {cpu(m):.1f}" for m in BASELINES))
    print("SEC6-E guard firings (report): " + "; ".join(f"{d}: {R[d]['fired']}" for d in names))


def data_check():
    man = {}
    for line in open(ROOT / "data" / "manifests" / "sec6.sha256"):
        if line.strip(): h_, pth = line.split()[:2]; man[pth] = h_
    bad = []
    for did, (name, _, _) in DATASETS.items():
        for ext in ("arff", "json"):
            pth = f"data/raw/openml/{did}_{name}.{ext}"; got = S.sha256(ROOT / pth) if (ROOT / pth).exists() else None
            print(f"{did} {name} .{ext}: sha256 {got} manifest {man.get(pth)} -> {'ok' if got and got == man.get(pth) else 'MISMATCH'}")
            if not got or got != man.get(pth): bad.append(f"{name}.{ext}")
    print("data check: " + (f"all {2 * len(DATASETS)} raw files match data/manifests/sec6.sha256" if not bad else f"MISMATCH {bad}: the study stops"))
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "devid": devid()
    elif cmd == "devmap": devmap()
    elif cmd == "devlist": print("\n".join(f"{s} {d}" for s, d in dev_list()))
    elif cmd == "devone":
        outp = sys.argv[sys.argv.index("--out") + 1]
        with open(outp, "w") as out: dev_one(sys.argv[2], int(sys.argv[3]), out)
    elif cmd == "devreport": dev_report(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif cmd == "dev":
        dd = ROOT / "prereg" / "sec6" / "dev"; dd.mkdir(parents=True, exist_ok=True)
        import contextlib
        for fn, f in ((devid, "devid.txt"), (devmap, "devmap.txt")):
            with open(dd / f, "w") as fo, contextlib.redirect_stdout(fo): fn()
        outs = []
        for s, d in dev_list():
            outs.append(dd / f"dev_{s}_{d}.jsonl")
            with open(outs[-1], "w") as out: dev_one(s, d, out)
        with open(ROOT / "prereg" / "sec6" / "dev_SEC6.txt", "w") as fo, contextlib.redirect_stdout(fo):
            dev_report(dd / "devid.txt", dd / "devmap.txt", outs)
    elif cmd == "check": sys.exit(0 if data_check() else 1)
    elif cmd == "all":
        did = int(sys.argv[2])
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/sec6/results_{did}.jsonl"
        tp = sys.argv[sys.argv.index("--times") + 1] if "--times" in sys.argv else outp.replace("results_", "times_")
        with open(outp, "w") as out, open(tp, "w") as tout: run_carrier(did, out, tout)
    elif cmd == "score": score(sys.argv[2:])
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/results_sec6_smoke.jsonl"
        with open(outp, "w") as out, open(outp.replace("results_", "times_"), "w") as tout: run_carrier(0, out, tout, synthetic=True)
        score([outp])
    else: raise SystemExit(__doc__)
