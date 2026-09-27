"""Study SEC3 — does the secant-calibrated Laplace weight (SEC) let a continual learner take on a NEW task stream without paying
to rediscover the forgetting weight? Owner request: prompt-log entry 227; plan item CL-1 of Empty_Centre/REVIEW_AND_NEXT_STEPS.md
(replication toward PASS-1/PASS-2, with ENERGY1's compute accounting inside it); prereg/sec3/PREREG.md.

WHAT IS FROZEN BESIDE THIS FILE (runs/sec3/frozen/):
  sec1_score.py, scl2_score.py, scl3_score.py  byte copies of runs/scl3/frozen/ (the learner, the SEC calibration, SEC1's arms and
               run_all; SCL3's ARFF reader, OpenML loader and class-selection rule)
This file adds only:
  (1) SEC3's carriers (a second unseen family, OpenML study 271; prereg/sec3/carrier_selection.txt), fed to SCL3's loader;
  (2) run_guard(): SEC with a stability-edge guard (mode 'bayes_sec_g'): at the start of each task, if the calibrated penalty's
      largest per-coordinate curvature makes the step unstable, lr * w * max(imp) >= GUARD (the explicit-Euler bound for the
      penalty's linear contraction 1 - 2 lr w imp_i), that task uses the raw Laplace importance instead; otherwise the code
      path is SEC1's run() exactly (instrument check G-ID: with GUARD = inf the arm equals 'bayes_sec' bit for bit);
  (3) CPU-time accounting: every run() is timed with time.process_time into a separate timing file (never in the results file,
      so the byte-identical rerun check (R9) is unaffected);
  (4) score(): the replication rows (SEC3-0..4, the exact SCL3 thresholds, on SEC as SCL3 ran it), the saving rows (SEC3-T,
      SEC3-P, SEC3-K), the sensitivity (SEC3-S, the declared window change: cells with a 0.05 window dropped, as learned on
      SCL3) and reports; the guarded arm is REPORT ONLY (rows *-GR): its gate closed on 2026-09-27 (AGENT_LOG 167);
  (5) gate(): SEC1's gate (as SCL3) and the guard gate on two SEEN SCL3 carriers (cnae-9, the failure; wall-robot-navigation,
      a pass) and on SEC1's synthetic stream.

    uv run python studies/sec3/sec3_score.py gate
    uv run python studies/sec3/sec3_score.py check              # data step: raw files against data/manifests/sec3.sha256
    uv run python studies/sec3/sec3_score.py all <data_id> [--out F] [--times T]
    uv run python studies/sec3/sec3_score.py score <results.jsonl ...>
    uv run python studies/sec3/sec3_score.py smokefull [--out F]
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np  # noqa: E402

_HERE = Path(__file__).resolve()
FROZEN = _HERE.parent.name == "frozen"
ROOT = _HERE.parents[3] if FROZEN else _HERE.parents[2]
sys.path.insert(0, str(_HERE.parent if FROZEN else ROOT / "runs" / "scl3" / "frozen"))
import scl3_score as L  # noqa: E402  (SCL3's loader; it imports SCL2's harness and SEC1's learner)
S = L.S                  # SEC1's learner module

# ---------------------------------------------------------------- carriers (prereg/sec3/carrier_selection.txt)
SCL3_DATASETS = dict(L.DATASETS)                    # SEEN since 2026-09-25: used only by the guard gate
DATASETS = {1596: ('covertype', 6, 2), 41167: ('dionis', 10, 2), 41164: ('fabert', 6, 2), 41169: ('helena', 10, 2),
            41168: ('jannis', 4, 2), 40685: ('shuttle', 6, 2), 41166: ('volkert', 10, 2)}
L.DATASETS = DATASETS                               # SCL3's load_openml reads its module-level DATASETS
# ---------------------------------------------------------------- registered constants (PREREG.md)
GUARD = 1.0                    # the stability bound lr * w * max(imp) >= GUARD triggers the raw-Laplace fallback for the task
SENS_GUARD = 0.5               # the guard's sensitivity cell (a stricter bound)
KEEP_CELLS = [(fs, fe) for fs in S.SENS_FS for fe in S.SENS_FE if fs > 0.05 and fe > 0.05 and (fs, fe) != (S.FS, S.FE)]
THREE = (1.0, 30.0, 1000.0)    # the 3-point mini-sweep (a subset of SEC1's coarse grid, one per 1.5 decades)
SHARE = 0.75                   # SCL3-3's carrier share (SEC1's 9 of 12)
MIN_B = 3                      # SEC3-T needs at least 3 carriers where the transferred lambda is behind
SEEDS = S.SEEDS
TIMES: list = []


# ---------------------------------------------------------------- the timed run (the learner itself is untouched)
_run = S.run


def _timed(*a, **k):
    t0 = time.process_time(); o = _run(*a, **k)
    TIMES.append(dict(mode=o["mode"], value=o["value"], seed=o["seed"], fs=o["fs"], fe=o["fe"], cpu_s=time.process_time() - t0))
    return o


S.run = _timed                  # SEC1's run_all looks run() up in its module at call time


def run_guard(seed, Xtr, ytr, Xte, yte, K, per_task, fs=S.FS, fe=S.FE, guard=GUARD, lr=S.LR, bs=S.BS, epochs=S.EPOCHS, hidden=S.HID):
    """SEC1's run() for mode 'bayes_sec', with the guard. Every line not marked GUARD is SEC1's (runs/scl3/frozen/sec1_score.py)."""
    t0 = time.process_time()
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    imp_bayes = np.zeros(n); imp_bayes_raw = np.zeros(n); theta_star = None             # GUARD: the raw accumulation kept beside
    wlog = []; svals = []; n_fallback = 0; fired = 0; margins = []
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            imp_used = imp_bayes / n_task
            if theta_star is not None:                                                    # GUARD
                m = lr * S.BAYES_W * float(np.max(imp_used)); margins.append(m)
                if not (m < guard):
                    imp_used = imp_bayes_raw / n_task; fired += 1
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
                        net.set_flat(theta_before - lr * g_p); continue
                    dth = theta_before - theta_star; g_q = 2 * imp_used * dth
                    w = S.BAYES_W
                    wlog.append(float(w))
                    net.set_flat(theta_before - lr * (g_p + w * g_q))
            theta_now = net.flat().copy()
            f = np.zeros(n)
            for _ in range(S.N_FISHER):
                ii = ii_task[rng.integers(0, len(ii_task), bs)]; f += S.ce_loss_grad(net, Xtr[ii], ytr[ii])[1] ** 2
            f_task = f / S.N_FISHER * bs
            dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)
            c = float(dg @ dth) / nn if nn > S.DTH_FLOOR else float("nan"); rho = float((f_task * dth) @ dth) / nn if nn > S.DTH_FLOOR else float("nan")
            if nn > S.DTH_FLOOR and np.isfinite(c) and np.isfinite(rho) and c > 0 and rho > 0: s = c / rho
            else: s = 1.0; n_fallback += 1
            svals.append(float(s))
            imp_bayes = imp_bayes + n_task * s * f_task
            imp_bayes_raw = imp_bayes_raw + n_task * f_task                                 # GUARD
            theta_star = theta_now
    rec = dict(mode="bayes_sec_g", value=float(guard), seed=int(seed), fs=float(fs), fe=float(fe), acc=100 * net.acc(Xte, yte), s=svals,
               n_fallback=int(n_fallback), guard_fired=int(fired), guard_margins=[round(m, 6) for m in margins],
               w_med=float(np.median(wlog)) if wlog else None, finite=bool(np.all(np.isfinite(net.flat()))))
    TIMES.append(dict(mode=rec["mode"], value=rec["value"], seed=rec["seed"], fs=rec["fs"], fe=rec["fe"], cpu_s=time.process_time() - t0))
    return rec


# ---------------------------------------------------------------- one carrier
def run_carrier(did, out, tout, synthetic=False):
    if synthetic:
        X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); name = "synthetic"; meta = dict(file="synthetic", sha256="none", openml_id=did, **meta)
    else:
        name = DATASETS[did][0]; Xs, ys, meta = L.load_openml(did)
    per_task = 2
    if meta["excluded"]:
        print(json.dumps(dict(dataset=name, **meta)), file=out, flush=True); return
    K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    S.run_all(name, data, K, per_task, meta, out)                     # every SEC1 arm, unchanged (header first)
    for seed in SEEDS:
        for (fs, fe), g in [((S.FS, S.FE), GUARD)] + [(c, GUARD) for c in KEEP_CELLS] + [((S.FS, S.FE), SENS_GUARD)]:
            o = run_guard(seed, *data, K, per_task, fs=fs, fe=fe, guard=g); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True)
    for t in TIMES:
        t["dataset"] = name; print(json.dumps(t), file=tout, flush=True)
    TIMES.clear()


# ---------------------------------------------------------------- scoring
def _mean(rows, mode, value=None, fs=S.FS, fe=S.FE):
    v = [r["acc"] for r in rows if r.get("mode") == mode and (value is None or abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value)))
         and r["fs"] == fs and r["fe"] == fe]
    return (float(np.mean(v)), v) if v else (None, [])


def _grid(rows, mode):
    vals = sorted({r["value"] for r in rows if r.get("mode") == mode and r["fs"] == S.FS and r["fe"] == S.FE})
    return {w: _mean(rows, mode, w) for w in vals}


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
    excl = sorted(d for d, v in by.items() if v is None)
    names = sorted(d for d, v in by.items() if v is not None)
    print("=" * 118)
    print("SEC3 scoring (prereg/sec3/PREREG.md): SCL3's thresholds, the declared window change, the guard, the saving rows")
    print("=" * 118)
    print(f"carriers scored {len(names)}: {names}; excluded {len(excl)}: {excl}")
    R = {}
    for d in names:
        rows = by[d]; g = _grid(rows, "fixed"); gs = _grid(rows, "fixed_sec")
        tuned = max(g, key=lambda w: g[w][0]); tv = g[tuned][1]; step = S.step_of(tv)
        tuned_s = max(gs, key=lambda w: gs[w][0])
        best3 = max(THREE, key=lambda w: g[w][0]) if all(w in g for w in THREE) else None
        r = dict(step=step, tuned=tuned, tuned_acc=g[tuned][0], tuned_s=tuned_s, grid=g, n_cfg=len(g),
                 bayes=_mean(rows, "bayes", 0.0)[0], sec=_mean(rows, "bayes_sec", 0.0)[0], s1=_mean(rows, "bayes_s1", 0.0)[0],
                 eq=_mean(rows, "eq", 1.0)[0], best3=best3, best3_acc=g[best3][0] if best3 else None,
                 secg=_mean(rows, "bayes_sec_g", GUARD)[0], secg_seeds=_mean(rows, "bayes_sec_g", GUARD)[1],
                 sec_seeds=_mean(rows, "bayes_sec", 0.0)[1],
                 fired=sum(o["guard_fired"] for o in rows if o.get("mode") == "bayes_sec_g" and o["value"] == GUARD and o["fs"] == S.FS and o["fe"] == S.FE),
                 sens_u={c: _mean(rows, "bayes_sec", 0.0, *c)[0] for c in KEEP_CELLS},
                 sens_g={**{c: _mean(rows, "bayes_sec_g", GUARD, *c)[0] for c in KEEP_CELLS}, "guard0.5": _mean(rows, "bayes_sec_g", SENS_GUARD)[0]},
                 tasks=len(next(o["s"] for o in rows if o.get("mode") == "bayes_sec")), n_seeds=len(tv))
        R[d] = r
    # the transferred lambda: leave-one-carrier-out median of the other carriers' tuned raw lambda (log scale), snapped to the coarse grid
    for d in names:
        others = [math.log(R[o]["tuned"]) for o in names if o != d]
        if others:
            lam = math.exp(float(np.median(others))); snap = min(S.EWC_COARSE, key=lambda w: abs(math.log(w) - math.log(lam)))
            R[d]["loco"] = snap; R[d]["loco_acc"] = R[d]["grid"][snap][0]
        else:
            R[d]["loco"] = None; R[d]["loco_acc"] = None
    for d in names:
        r = R[d]
        print(f"\n[{d}] step {r['step']:.4f}; tuned lambda {r['tuned']:g} ({r['n_cfg']} grid configurations): {r['tuned_acc']:.4f}")
        print("   raw grid: " + "  ".join(f"{w:g}:{v[0]:.2f}" for w, v in r["grid"].items()))
        print(f"   SEC (unguarded) {r['sec']:.4f} [{' '.join(f'{a:.2f}' for a in r['sec_seeds'])}] −tuned {r['sec'] - r['tuned_acc']:+.4f}; "
              f"SEC guarded {r['secg']:.4f} [{' '.join(f'{a:.2f}' for a in r['secg_seeds'])}] −tuned {r['secg'] - r['tuned_acc']:+.4f}; guard fired {r['fired']} of {r['n_seeds'] * (r['tasks'] - 1)} task starts")
        print(f"   raw Laplace {r['bayes']:.4f} −tuned {r['bayes'] - r['tuned_acc']:+.4f}; one factor {r['s1']:.4f}; rule Ω=1 {r['eq']:.4f} −tuned {r['eq'] - r['tuned_acc']:+.4f}")
        if r["best3"] is not None:
            print(f"   3-point sweep {THREE}: best {r['best3']:g} {r['best3_acc']:.4f}; SEC − best3 {r['sec'] - r['best3_acc']:+.4f}")
        if r["loco"] is not None:
            print(f"   transferred lambda (LOCO median, snapped) {r['loco']:g}: {r['loco_acc']:.4f} −tuned {r['loco_acc'] - r['tuned_acc']:+.4f}")
        print("   window cells (unguarded, guarded) − tuned: " + "  ".join(f"{c[0]:g}/{c[1]:g}:{r['sens_u'][c] - r['tuned_acc']:+.2f},{r['sens_g'][c] - r['tuned_acc']:+.2f}" for c in KEEP_CELLS)
              + f"  guard {SENS_GUARD}: {r['sens_g']['guard0.5'] - r['tuned_acc']:+.2f}")
    N = len(names); need = math.ceil(SHARE * N)
    nb = lambda a, r: a - r["tuned_acc"] > -r["step"]                      # noqa: E731  "not behind the tuned lambda"
    print("\n" + "-" * 118)
    M = [d for d in names if R[d]["bayes"] - R[d]["tuned_acc"] <= -R[d]["step"]]
    dec = len(M) >= S.MIN_MISCAL
    print(f"SEC3-0 precondition: miscalibrated carriers (raw Laplace behind the tuned lambda by a step) {M} ({len(M)}; need >= {S.MIN_MISCAL}) -> {'DECIDABLE' if dec else 'NOT DECIDABLE'}")
    for tag, key in (("", "sec"), ("-GR", "secg")):
        if tag and not dec: continue
        if tag: print("   (SEC3-*-GR rows: the guarded arm, REPORT ONLY: the guard gate closed on SCL3's cnae-9, prereg/sec3/gate_SEC3.txt)")
        if dec:
            ok = [d for d in M if R[d][key] - R[d]["bayes"] >= S.CLOSE_FRAC * (R[d]["tuned_acc"] - R[d]["bayes"])]
            need1 = math.ceil(S.CLOSE_SHARE * len(M))
            print(f"SEC3-1{tag} closes at least half the raw gap on M: {len(ok)}/{len(M)} (need {need1}) -> {('PASS' if len(ok) >= need1 else 'FAIL') if not tag else 'report'}; "
                  + ", ".join(f"{d}: gap {R[d]['tuned_acc'] - R[d]['bayes']:.2f} gain {R[d][key] - R[d]['bayes']:+.2f}" for d in M))
        else:
            print("SEC3-1: NOT DECIDABLE (SEC3-0)")
        out_m = [d for d in names if d not in M]
        harm = [d for d in out_m if not (R[d][key] - R[d]["bayes"] > -R[d]["step"])]
        print(f"SEC3-2{tag} no harm outside M: " + (f"{len(out_m) - len(harm)}/{len(out_m)} -> {('PASS' if not harm else 'FAIL') if not tag else 'report'}" if out_m else "NOT DECIDABLE (no carrier outside M)"))
    for tag, key in (("", "sec"), ("-GR", "secg")):
        k = sum(nb(R[d][key], R[d]) for d in names)
        print(f"SEC3-3{tag} tuning-free (not behind the tuned lambda): {k}/{N} (need {need}) -> {('PASS' if k >= need else 'FAIL') if not tag else 'report'}; "
              + ", ".join(f"{d}:{R[d][key] - R[d]['tuned_acc']:+.4f} (step {R[d]['step']:.2f})" for d in names))
    kb = sum(nb(R[d]["bayes"], R[d]) for d in names); ke = sum(nb(R[d]["eq"], R[d]) for d in names)
    print(f"   beside it: raw Laplace not behind {kb}/{N}; the rule Ω=1 not behind {ke}/{N}")
    raw_span = max(R[d]["tuned"] for d in names) / min(R[d]["tuned"] for d in names) if N else float("nan")
    cal_span = max(R[d]["tuned_s"] for d in names) / min(R[d]["tuned_s"] for d in names) if N else float("nan")
    print(f"SEC3-4 span collapse: tuned raw lambda span {raw_span:.2f}x, calibrated {cal_span:.2f}x (need <= raw / {S.SPAN_FACTOR:g}) -> {'PASS' if cal_span <= raw_span / S.SPAN_FACTOR else 'FAIL'}")
    B = [d for d in names if R[d]["loco"] is not None and not nb(R[d]["loco_acc"], R[d])]
    if len(B) >= MIN_B:
        kt = sum(nb(R[d]["sec"], R[d]) for d in B); needt = math.ceil(SHARE * len(B))
        print(f"SEC3-T the saving is SEC's (where a transferred lambda is behind): B = {B} ({len(B)}); SEC not behind on {kt}/{len(B)} (need {needt}) -> {'PASS' if kt >= needt else 'FAIL'}")
    else:
        print(f"SEC3-T: NOT DECIDABLE (the transferred lambda is behind on only {len(B)} carriers, need >= {MIN_B}): a reused lambda would have saved the sweep without SEC")
    kp = sum(R[d]["best3"] is not None and R[d]["sec"] - R[d]["best3_acc"] > -R[d]["step"] for d in names)
    print(f"SEC3-P SEC (1 configuration) not behind the 3-point mini-sweep (3 configurations): {kp}/{N} (need {need}) -> {'PASS' if kp >= need else 'FAIL'}")
    for tag, key, sk in (("", "sec", "sens_u"), ("-GR", "secg", "sens_g")):
        flips = sum(nb(R[d][key], R[d]) != nb(v, R[d]) for d in names for v in R[d][sk].values())
        cells = sum(len(R[d][sk]) for d in names)
        print(f"SEC3-S{tag} sensitivity: 'not behind' flips in {flips} of {cells} cells -> {('FRAGILE' if flips > 1 else 'not fragile') if not tag else 'report'}")
    print("SEC3-K compute (report; configurations x 5 seeds each; CPU seconds from the timing files):")
    for d in names:
        t = times.get(d, [])
        cpu = lambda mode, val=None, fs=S.FS, fe=S.FE: sum(x["cpu_s"] for x in t if x["mode"] == mode and x["fs"] == fs and x["fe"] == fe  # noqa: E731
                                                          and (val is None or abs(x["value"] - val) <= 1e-6 * max(1.0, abs(val))))
        full = cpu("fixed"); three = sum(cpu("fixed", w) for w in THREE); sec = cpu("bayes_sec", 0.0); secg = cpu("bayes_sec_g", GUARD); raw = cpu("bayes", 0.0)
        if full > 0:
            print(f"   {d}: configurations full sweep {R[d]['n_cfg']}, 3-point 3, SEC 1 (config share {1 / R[d]['n_cfg']:.4f}); CPU s full {full:.1f}, 3-point {three:.1f}, "
                  f"SEC {sec:.1f} (share {sec / full:.4f}), SEC guarded {secg:.1f} (share {secg / full:.4f}), raw Laplace {raw:.1f} (SEC overhead x{sec / raw if raw else float('nan'):.3f})")
        else:
            print(f"   {d}: configurations full sweep {R[d]['n_cfg']}, 3-point 3, SEC 1 (config share {1 / R[d]['n_cfg']:.4f}); no timing file")
    print("SEC3-E calibration and guard (report): " + "; ".join(f"{d}: guard fired {R[d]['fired']}" for d in names))


# ---------------------------------------------------------------- gate (R4) — run on SEEN data and synthetic streams only
def _tuned_from_pinned(path):
    rows = [json.loads(line) for line in open(path)]
    rows = [r for r in rows if r.get("mode") == "fixed" and r["fs"] == S.FS and r["fe"] == S.FE]
    g = {}
    for r in rows: g.setdefault(r["value"], []).append(r["acc"])
    tuned = max(g, key=lambda w: np.mean(g[w])); return tuned, float(np.mean(g[tuned])), S.step_of(g[tuned])


def gate():
    print("SEC3 gate (prereg/sec3/PREREG.md): SEC1's gate, then the guard gate")
    print("=" * 100)
    S.gate()
    print("=" * 100)
    ok = {}
    # G-ID: with an infinite bound the guarded arm is SEC1's bayes_sec bit for bit (synthetic stream)
    X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    same = []
    for seed in SEEDS:
        a = _run("bayes_sec", 0.0, seed, *data, K, 2); b = run_guard(seed, *data, K, 2, guard=float("inf"))
        same.append(a["acc"] == b["acc"] and a["s"] == b["s"] and b["guard_fired"] == 0)
    ok["G-ID"] = all(same)
    print(f"G-ID (MUST_PASS) guard at +inf equals SEC1's bayes_sec on the synthetic stream: {sum(same)}/{len(same)} seeds identical -> {'holds' if ok['G-ID'] else 'FAILS'}")
    L.DATASETS = SCL3_DATASETS
    try:
        for did, lab in ((1468, "G-RESCUE"), (1497, "G-QUIET")):
            name = SCL3_DATASETS[did][0]; Xs, ys, meta = L.load_openml(did); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
            tuned, tacc, step = _tuned_from_pinned(ROOT / "runs" / "scl3" / f"results_{did}.jsonl")
            u = [_run("bayes_sec", 0.0, s, *data, K, 2) for s in SEEDS]; g = [run_guard(s, *data, K, 2) for s in SEEDS]
            ua = float(np.mean([o["acc"] for o in u])); ga = float(np.mean([o["acc"] for o in g])); fired = sum(o["guard_fired"] for o in g)
            print(f"[{name}] (SEEN; SCL3's pinned tuned lambda {tuned:g}: {tacc:.4f}, step {step:.4f})")
            print(f"   unguarded SEC {ua:.4f} [{' '.join('%.2f' % o['acc'] for o in u)}] −tuned {ua - tacc:+.4f}")
            print(f"   guarded SEC   {ga:.4f} [{' '.join('%.2f' % o['acc'] for o in g)}] −tuned {ga - tacc:+.4f}; guard fired {fired}; "
                  f"margins {[o['guard_margins'] for o in g]}")
            if lab == "G-RESCUE":
                ok[lab] = fired >= 1 and (ga - tacc > -step) and not (ua - tacc > -step)
                print(f"{lab} (MUST_PASS) on SCL3's failure the guard fires, the unguarded arm is behind and the guarded arm is not: -> {'holds' if ok[lab] else 'FAILS'}")
            else:
                ok[lab] = fired == 0 and all(a["acc"] == b["acc"] for a, b in zip(u, g))
                print(f"{lab} (MUST_PASS) on an SCL3 pass the guard never fires and the arm equals SEC per seed: -> {'holds' if ok[lab] else 'FAILS'}")
    finally:
        L.DATASETS = DATASETS
    print("=" * 100)
    print("GUARD GATE " + ("OPEN" if all(ok.values()) else "CLOSED") + ": " + ", ".join(f"{k} {'holds' if v else 'FAILS'}" for k, v in ok.items()))


def data_check():
    man = {}
    for line in open(ROOT / "data" / "manifests" / "sec3.sha256"):
        if line.strip(): h_, pth = line.split()[:2]; man[pth] = h_
    bad = []
    for did, (name, _, _) in DATASETS.items():
        for ext in ("arff", "json"):
            pth = f"data/raw/openml/{did}_{name}.{ext}"; got = S.sha256(ROOT / pth) if (ROOT / pth).exists() else None
            print(f"{did} {name} .{ext}: sha256 {got} manifest {man.get(pth)} -> {'ok' if got and got == man.get(pth) else 'MISMATCH'}")
            if not got or got != man.get(pth): bad.append(f"{name}.{ext}")
    print("data check: " + (f"all {2 * len(DATASETS)} raw files match data/manifests/sec3.sha256" if not bad else f"MISMATCH {bad}: the study stops"))
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "gate": gate()
    elif cmd == "check": sys.exit(0 if data_check() else 1)
    elif cmd == "all":
        did = int(sys.argv[2])
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/sec3/results_{did}.jsonl"
        tp = sys.argv[sys.argv.index("--times") + 1] if "--times" in sys.argv else outp.replace("results_", "times_")
        with open(outp, "w") as out, open(tp, "w") as tout: run_carrier(did, out, tout)
    elif cmd == "score": score(sys.argv[2:])
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/results_sec3_smoke.jsonl"
        with open(outp, "w") as out, open(outp.replace("results_", "times_"), "w") as tout: run_carrier(0, out, tout, synthetic=True)
        score([outp])
    else: raise SystemExit(__doc__)
