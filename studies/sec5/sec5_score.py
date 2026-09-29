"""Study SEC5 — the replication of SEC4's clipped SEC on a FOURTH unseen family (OpenML suites 293 / 454 / 445, by the rule in
prereg/sec5/DEV_DECLARATION.md), with kappa swept, and a CRR-guided refinement (A6's bounded strength: the past importance
averaged over settled tasks, not summed) developed on SEEN carriers and tested only if its gate opens.
Owner request: prompt-log entry 238; prereg/sec5/DEV_DECLARATION.md (design, development stage) and prereg/sec5/PREREG.md.

WHAT IS FROZEN BESIDE THIS FILE (runs/sec5/frozen/): byte copies of runs/sec4/frozen/*.py. The primary arm is SEC4's
run_guard(variant='clip', kappa=0.5), imported unchanged. This file adds only:
  (1) run_a6(): SEC4's run_guard for 'clip' with one change, marked A6: the summed importance is divided by the number of
      settled tasks before use; divisor_one=True restores SEC4's arithmetic bit for bit (D-ID);
  (2) dev_one() / dev_report(): the development stage on the 22 SEEN carriers and the gate D-GATE-C;
  (3) run_carrier() and score() for the fourth family: SEC1's run_all (every arm, unchanged), the clip at the primary window,
      at SEC4's three retained window cells and at kappa 0.25 and 1.0, and the chosen A6 candidate if D-GATE-C opened.

    uv run python studies/sec5/sec5_score.py devid                       # D-ID on SEC1's synthetic stream
    uv run python studies/sec5/sec5_score.py devone <study> <OpenML id> --out F   # one SEEN carrier (JSON line)
    uv run python studies/sec5/sec5_score.py devreport <devid.txt> <F ...>        # the development table and D-GATE-C
    uv run python studies/sec5/sec5_score.py all <OpenML id> [--out F]
    uv run python studies/sec5/sec5_score.py score <results.jsonl ...>
    uv run python studies/sec5/sec5_score.py check
    uv run python studies/sec5/sec5_score.py smokefull [--out F]
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
sys.path.insert(0, str(_HERE.parent if FROZEN else ROOT / "runs" / "sec4" / "frozen"))
import sec4_score as P4  # noqa: E402  (SEC4's scorer, unchanged: its run_guard is the primary arm)
P3 = P4.P3; L = P4.L; S = P4.S

# ---------------------------------------------------------------- registered constants (DEV_DECLARATION.md, PREREG.md)
KAPPA = P4.KAPPA                 # 0.5, SEC4's clip margin: the primary arm, unchanged
KAPPA_CELLS = (0.25, 1.0)        # the kappa sweep (sensitivity): one factor of 2 either side; 1.0 is the stability edge
KEEP_CELLS = P4.KEEP_CELLS       # SEC4's three retained window cells
THREE = P4.THREE; SHARE = P4.SHARE; MIN_B = P4.MIN_B; MIN_N = P4.MIN_N; DIV_FRAC = P4.DIV_FRAC; SEEDS = S.SEEDS
A6_VARIANTS = ("a6mean", "a6mean_clip")          # tie order of the selection rule (DEV_DECLARATION.md)
C_CHOSEN = None                  # prereg/sec5/dev_SEC5.txt: D-GATE-C CLOSED (D-ADDS fails), so no A6 arm runs on the fourth family (R12)
DEV_TABLES = (("scl3", dict(P3.SCL3_DATASETS)), ("sec3", {k: v for k, v in P3.DATASETS.items() if k not in P4.DEV_EXCLUDED}),
              ("sec4", {k: P4.DATASETS[k] for k in (375, 46906, 1459, 1466, 1476, 377)}))   # the 22 SEEN carriers SEC was scored on
DIVERGED = ("cnae-9", "dionis", "fabert", "anneal", "cardiotocography", "synthetic_control")
DATASETS = {57: ('hypothyroid', 4, 2), 155: ('pokerhand', 10, 2), 1503: ('spoken-arabic-digit', 10, 2), 1509: ('walking-activity', 10, 2),
            1529: ('volcanoes-a3', 4, 2), 1530: ('volcanoes-a4', 4, 2), 1532: ('volcanoes-b2', 4, 2), 1541: ('volcanoes-d4', 4, 2),
            1549: ('autoUniv-au6-750', 8, 2), 41671: ('microaggregation2', 4, 2), 41972: ('Indian_pines', 8, 2), 41982: ('Kuzushiji-MNIST', 10, 2)}
            # OpenML id -> (name, K requested, classes per task): prereg/sec5/carrier_selection.txt


def run_a6(seed, Xtr, ytr, Xte, yte, K, per_task, variant, fs=S.FS, fe=S.FE, kappa=KAPPA, divisor_one=False,
           lr=S.LR, bs=S.BS, epochs=S.EPOCHS, hidden=S.HID):
    """SEC4's run_guard (runs/sec4/frozen/sec4_score.py) for 'clip', with the A6 change. variant 'a6mean' has no guard,
    'a6mean_clip' SEC4's clip. Every line not marked A6 is SEC4's."""
    t0 = time.process_time()
    rng = np.random.default_rng(seed)
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    imp_bayes = np.zeros(n); theta_star = None
    wlog = []; svals = []; n_fallback = 0; fired = 0; margins = []; n_settled = 0
    cap = kappa / (lr * S.BAYES_W)
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            div = 1 if (divisor_one or n_settled == 0) else n_settled                                   # A6
            imp_used = (imp_bayes / div) / n_task                                                       # A6 (div = 1: SEC's)
            if theta_star is not None:
                m = lr * S.BAYES_W * float(np.max(imp_used)); margins.append(m)
                if variant == "a6mean_clip" and not (m < kappa):
                    imp_used = np.minimum(imp_used, cap); fired += 1
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
            n_settled += 1                                                                              # A6
            theta_star = theta_now
    rec = dict(mode=f"bayes_sec_{variant}", value=float(kappa if variant == "a6mean_clip" else 0.0), seed=int(seed), fs=float(fs), fe=float(fe),
               acc=100 * net.acc(Xte, yte), s=svals, n_fallback=int(n_fallback), guard_fired=int(fired), guard_margins=[round(x, 6) for x in margins],
               w_med=float(np.median(wlog)) if wlog else None, finite=bool(np.all(np.isfinite(net.flat()))), divisor_one=bool(divisor_one))
    P4.TIMES.append(dict(mode=rec["mode"], value=rec["value"], seed=rec["seed"], fs=rec["fs"], fe=rec["fe"], cpu_s=time.process_time() - t0))
    return rec


# ---------------------------------------------------------------- development on the 22 SEEN carriers (DEV_DECLARATION.md)
def devid():
    """D-ID: with the divisor forced to 1, a6mean equals SEC1's bayes_sec and a6mean_clip equals SEC4's clip, bit for bit."""
    X, y = S._synthetic(); Xs, ys, meta = L.select_classes(X, y, 10); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    ok = True
    for v, ref in (("a6mean", lambda s: P3._run("bayes_sec", 0.0, s, *data, K, 2)), ("a6mean_clip", lambda s: P4.run_guard(s, *data, K, 2, "clip"))):
        same = []
        for seed in SEEDS:
            a = ref(seed); b = run_a6(seed, *data, K, 2, v, divisor_one=True)
            same.append(a["acc"] == b["acc"] and a["s"] == b["s"] and (v == "a6mean" or (a["guard_fired"] == b["guard_fired"] and a["guard_margins"] == b["guard_margins"])))
        ok &= all(same)
        print(f"D-ID {v}: divisor forced to 1 equals {'SEC1 bayes_sec' if v == 'a6mean' else 'SEC4 clip'} on the synthetic stream: {sum(same)}/{len(same)} -> {'holds' if all(same) else 'FAILS'}")
    # the divisor matters on this stream (5 tasks), else the candidates would be SEC itself
    diff = [run_a6(s, *data, K, 2, "a6mean")["acc"] != P3._run("bayes_sec", 0.0, s, *data, K, 2)["acc"] for s in SEEDS]
    print(f"the A6 divisor changes the run on the synthetic stream (5 tasks): {sum(diff)}/{len(diff)} seeds")
    print(f"D-ID -> {'holds' if ok else 'FAILS'}")


def dev_one(study, did, out):
    table = dict(DEV_TABLES)[study]; L.DATASETS = table; name = table[did][0]
    Xs, ys, meta = L.load_openml(did); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    tuned, tacc, step, secu = P4._pinned(ROOT / "runs" / study / f"results_{did}.jsonl")
    rec = dict(study=study, did=did, name=name, K=K, tuned=tuned, tacc=tacc, step=step, secu=secu)
    runs = {"clip": [P4.run_guard(s, *data, K, 2, "clip") for s in SEEDS]}
    for v in A6_VARIANTS:
        runs[v] = [run_a6(s, *data, K, 2, v) for s in SEEDS]
    for v, os_ in runs.items():
        rec[v] = dict(acc=float(np.mean([o["acc"] for o in os_])), seeds=[o["acc"] for o in os_], fired=sum(o["guard_fired"] for o in os_))
    P4.TIMES.clear()
    print(json.dumps(rec), file=out, flush=True)


def dev_report(idpath, paths):
    idtxt = Path(idpath).read_text()
    d_id = idtxt.strip().endswith("D-ID -> holds")
    recs = [json.loads(line) for p in paths for line in open(p) if line.strip()]
    recs.sort(key=lambda r: ([t for t, _ in DEV_TABLES].index(r["study"]), r["name"].lower()))
    print("SEC5 CRR-guided development (A6: the past importance averaged over settled tasks) on the 22 SEEN carriers "
          "(prereg/sec5/DEV_DECLARATION.md); tuned lambda and step from pinned results")
    print("=" * 118)
    print(idtxt.rstrip())
    for r in recs:
        print(f"[{r['name']}] ({r['study']}, K {r['K']}) tuned {r['tuned']:g}: {r['tacc']:.4f}, step {r['step']:.4f}; unguarded SEC {r['secu']:.4f} ({r['secu'] - r['tacc']:+.4f})")
        for v in ("clip",) + A6_VARIANTS:
            x = r[v]
            print(f"     {v:11}: {x['acc']:.4f} [{' '.join('%.2f' % a for a in x['seeds'])}] −tuned {x['acc'] - r['tacc']:+.4f}, fired {x['fired']}")
    print("=" * 118)
    N = len(recs)
    nb = lambda v, r: r[v]["acc"] - r["tacc"] > -r["step"]  # noqa: E731
    counts = {v: sum(nb(v, r) for r in recs) for v in ("clip",) + A6_VARIANTS}
    fired = {v: sum(r[v]["fired"] for r in recs) for v in A6_VARIANTS}
    fixes = {v: sum(nb(v, r) for r in recs if r["name"] in DIVERGED) for v in ("clip",) + A6_VARIANTS}
    mean_vs_clip = {v: float(np.mean([r[v]["acc"] - r["clip"]["acc"] for r in recs])) for v in A6_VARIANTS}
    for v in ("clip",) + A6_VARIANTS:
        print(f"{v:11}: not behind {counts[v]}/{N}; divergence carriers not behind {fixes[v]}/{len(DIVERGED)}"
              + (f"; firings {fired[v]}; mean (−clip) over the {N}: {mean_vs_clip[v]:+.4f}" if v in A6_VARIANTS else ""))
    chosen = sorted(A6_VARIANTS, key=lambda v: (-counts[v], fired[v], A6_VARIANTS.index(v)))[0]
    need = math.ceil(0.75 * N)
    d_count = counts[chosen] >= need; d_fix = fixes[chosen] >= 4
    d_adds = counts[chosen] >= counts["clip"] and mean_vs_clip[chosen] >= 0
    print(f"CHOSEN (most not behind; ties: fewest firings, then {A6_VARIANTS}): {chosen}")
    print(f"D-COUNT {counts[chosen]}/{N} (need {need}) -> {'holds' if d_count else 'FAILS'}; D-ID -> {'holds' if d_id else 'FAILS'}; "
          f"D-FIXES {fixes[chosen]}/{len(DIVERGED)} (need 4) -> {'holds' if d_fix else 'FAILS'}; "
          f"D-ADDS not behind {counts[chosen]} vs clip {counts['clip']}, mean −clip {mean_vs_clip[chosen]:+.4f} (need >= clip's count and >= 0) -> {'holds' if d_adds else 'FAILS'}")
    print("D-GATE-C " + ("OPEN" if (N == 22 and d_count and d_id and d_fix and d_adds) else "CLOSED") + (f"" if N == 22 else f" (only {N} of 22 carriers)"))


# ---------------------------------------------------------------- the fourth family
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
        arms = ([("clip", KAPPA, (S.FS, S.FE))] + [("clip", KAPPA, c) for c in KEEP_CELLS] + [("clip", k, (S.FS, S.FE)) for k in KAPPA_CELLS])
        for v, kap, (fs, fe) in arms:
            o = P4.run_guard(seed, *data, K, per_task, v, fs=fs, fe=fe, kappa=kap); o["dataset"] = name
            print(json.dumps(o), file=out, flush=True)
        if C_CHOSEN is not None:
            for fs, fe in [(S.FS, S.FE)] + list(KEEP_CELLS):
                o = run_a6(seed, *data, K, per_task, C_CHOSEN, fs=fs, fe=fe); o["dataset"] = name
                print(json.dumps(o), file=out, flush=True)
    for t in P4.TIMES:
        t["dataset"] = name; print(json.dumps(t), file=tout, flush=True)
    P4.TIMES.clear()


def _mean(rows, mode, value=None, fs=S.FS, fe=S.FE):
    v = [r["acc"] for r in rows if r.get("mode") == mode and (value is None or abs(r["value"] - value) <= 1e-6 * max(1.0, abs(value)))
         and r["fs"] == fs and r["fe"] == fe]
    return (float(np.mean(v)), v) if v else (None, [])


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
    G = "bayes_sec_clip"; C = f"bayes_sec_{C_CHOSEN}" if C_CHOSEN else None; cval = KAPPA if C_CHOSEN == "a6mean_clip" else 0.0
    print("=" * 118)
    print("SEC5 scoring (prereg/sec5/PREREG.md): SEC4's clipped SEC (kappa 0.5) replicated on a fourth unseen family; kappa swept; "
          + (f"the CRR-guided candidate {C_CHOSEN} (A6)" if C_CHOSEN else "no A6 arm (D-GATE-C closed)"))
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
                 u=_mean(rows, "bayes_sec", 0.0)[0], u_seeds=_mean(rows, "bayes_sec", 0.0)[1], raw=_mean(rows, "bayes", 0.0)[0], eq=_mean(rows, "eq", 1.0)[0],
                 sens={("window", c): _mean(rows, G, KAPPA, *c)[0] for c in KEEP_CELLS},
                 best3=max(THREE, key=lambda w: gm[w]) if all(w in gm for w in THREE) else None, n_seeds=len(g[tuned]))
        r["sens"].update({("kappa", k): _mean(rows, G, k)[0] for k in KAPPA_CELLS})
        r["kseeds"] = {k: _mean(rows, G, k)[1] for k in KAPPA_CELLS}
        r["best3_acc"] = gm[r["best3"]] if r["best3"] else None
        if C:
            r["c"] = _mean(rows, C, cval)[0]; r["c_seeds"] = _mean(rows, C, cval)[1]
            r["c_sens"] = {c: _mean(rows, C, cval, *c)[0] for c in KEEP_CELLS}
            r["c_fired"] = sum(o["guard_fired"] for o in rows if o.get("mode") == C and o["fs"] == S.FS and o["fe"] == S.FE)
        R[d] = r
    for d in names:
        others = [math.log(R[o]["tuned"]) for o in names if o != d]
        if others:
            lam = math.exp(float(np.median(others))); snap = min(S.EWC_COARSE, key=lambda w: abs(math.log(w) - math.log(lam)))
            R[d]["loco"] = snap; R[d]["loco_acc"] = R[d]["grid"][snap]
        else:
            R[d]["loco"] = None; R[d]["loco_acc"] = None
    for d in names:
        r = R[d]
        print(f"\n[{d}] step {r['step']:.4f}; tuned lambda {r['tuned']:g} ({r['n_cfg']} grid configurations): {r['tacc']:.4f}")
        print("   raw grid: " + "  ".join(f"{w:g}:{v:.2f}" for w, v in r["grid"].items()))
        print(f"   clipped SEC (kappa 0.5) {r['g']:.4f} [{' '.join('%.2f' % a for a in r['g_seeds'])}] −tuned {r['g'] - r['tacc']:+.4f}; fired {r['fired']}")
        print(f"   unguarded SEC {r['u']:.4f} [{' '.join('%.2f' % a for a in r['u_seeds'])}] −tuned {r['u'] - r['tacc']:+.4f}; raw Laplace {r['raw']:.4f} ({r['raw'] - r['tacc']:+.4f}); "
              f"rule Ω=1 {r['eq']:.4f} ({r['eq'] - r['tacc']:+.4f})")
        for k in KAPPA_CELLS:
            print(f"   clip kappa {k:g}: {r['sens'][('kappa', k)]:.4f} [{' '.join('%.2f' % a for a in r['kseeds'][k])}] −tuned {r['sens'][('kappa', k)] - r['tacc']:+.4f}")
        if r["best3"] is not None:
            print(f"   3-point sweep: best {r['best3']:g} {r['best3_acc']:.4f}; clipped SEC − best3 {r['g'] - r['best3_acc']:+.4f}")
        if r["loco"] is not None:
            print(f"   transferred lambda {r['loco']:g}: {r['loco_acc']:.4f} −tuned {r['loco_acc'] - r['tacc']:+.4f}")
        print("   window cells (clip) − tuned: " + "  ".join(f"{c[0]:g}/{c[1]:g}:{r['sens'][('window', c)] - r['tacc']:+.2f}" for c in KEEP_CELLS))
        if C:
            print(f"   {C_CHOSEN} (A6) {r['c']:.4f} [{' '.join('%.2f' % a for a in r['c_seeds'])}] −tuned {r['c'] - r['tacc']:+.4f}; −clip {r['c'] - r['g']:+.4f}; fired {r['c_fired']}; "
                  "window cells − tuned: " + "  ".join(f"{c[0]:g}/{c[1]:g}:{v - r['tacc']:+.2f}" for c, v in r["c_sens"].items()))
    N = len(names); need = math.ceil(SHARE * N)
    nb = lambda a, r: a - r["tacc"] > -r["step"]  # noqa: E731
    print("\n" + "-" * 118)
    k = sum(nb(R[d]["g"], R[d]) for d in names)
    v1 = "NOT DECIDABLE (fewer than %d carriers scored)" % MIN_N if N < MIN_N else ("PASS" if k >= need else "FAIL")
    print(f"SEC5-1 tuning-free, the clipped SEC (kappa 0.5) not behind the tuned lambda: {k}/{N} (need {need}) -> {v1}; "
          + ", ".join(f"{d}:{R[d]['g'] - R[d]['tacc']:+.4f} (step {R[d]['step']:.2f})" for d in names))
    ku = sum(nb(R[d]["u"], R[d]) for d in names); kr = sum(nb(R[d]["raw"], R[d]) for d in names); ke = sum(nb(R[d]["eq"], R[d]) for d in names)
    print(f"   beside it (report): unguarded SEC {ku}/{N}; raw Laplace {kr}/{N}; the rule Ω=1 {ke}/{N}")
    vol = [d for d in names if d.startswith("volcanoes")]
    if len(vol) > 1:   # PREREG.md: report only, the four volcano image sets of one survey counted once (majority; a tie counts as behind)
        rest = [d for d in names if d not in vol]; vk = sum(nb(R[d]["g"], R[d]) for d in vol)
        n1 = len(rest) + 1; k1 = sum(nb(R[d]["g"], R[d]) for d in rest) + (vk * 2 > len(vol)); need1 = math.ceil(SHARE * n1)
        print(f"   report, the volcanoes counted once ({len(vol)} image sets, {vk} not behind -> {'not behind' if vk * 2 > len(vol) else 'behind'}): "
              f"{k1}/{n1} (need {need1}) -> {'PASS' if (n1 >= MIN_N and k1 >= need1) else ('NOT DECIDABLE' if n1 < MIN_N else 'FAIL')}")
    div = [d for d in names if any(a < DIV_FRAC * R[d]["tacc"] for a in R[d]["g_seeds"])]
    divu = [d for d in names if any(a < DIV_FRAC * R[d]["tacc"] for a in R[d]["u_seeds"])]
    print(f"SEC5-2 no divergence: carriers with a clipped seed below half the tuned accuracy: {div} ({len(div)}) -> {'PASS' if not div else 'FAIL'}; unguarded (report): {divu}")
    B = [d for d in names if R[d]["loco"] is not None and not nb(R[d]["loco_acc"], R[d])]
    if len(B) >= MIN_B:
        kt = sum(nb(R[d]["g"], R[d]) for d in B); needt = math.ceil(SHARE * len(B))
        print(f"SEC5-T the saving is SEC's: B = {B} ({len(B)}); clipped SEC not behind on {kt}/{len(B)} (need {needt}) -> {'PASS' if kt >= needt else 'FAIL'}")
    else:
        print(f"SEC5-T: NOT DECIDABLE (a transferred lambda is behind on only {len(B)} carriers, need >= {MIN_B})")
    kp = sum(R[d]["best3"] is not None and R[d]["g"] - R[d]["best3_acc"] > -R[d]["step"] for d in names)
    print(f"SEC5-P clipped SEC (1 configuration) not behind the 3-point mini-sweep (3): {kp}/{N} (need {need}) -> {'PASS' if kp >= need else 'FAIL'}")
    cells = [c for c in R[names[0]]["sens"]] if names else []
    flips = {c: sum(nb(R[d]["g"], R[d]) != nb(R[d]["sens"][c], R[d]) for d in names) for c in cells}
    tot = sum(flips.values())
    print(f"SEC5-S sensitivity over {len(cells)} cells x {N} carriers (3 window cells, kappa 0.25 and 1.0): flips in {tot} of {len(cells) * N} -> "
          f"{'FRAGILE' if tot > 1 else 'not fragile'}; by cell: " + ", ".join(f"{c[0]} {c[1]}: {v}" for c, v in flips.items()))
    for kk in KAPPA_CELLS:
        kd = [d for d in names if any(a < DIV_FRAC * R[d]["tacc"] for a in R[d]["kseeds"][kk])]
        print(f"   kappa {kk:g}: not behind {sum(nb(R[d]['sens'][('kappa', kk)], R[d]) for d in names)}/{N}; carriers with a seed below half the tuned accuracy: {kd}")
    level = ("PASS-1 candidate (the report states the anchor and admissibility)" if (v1 == "PASS" and tot <= 1 and not div) else
             ("PASS-0 (not PASS-1: " + ", ".join(x for x, bad in (("fragile", tot > 1), ("divergence", bool(div))) if bad) + ")" if v1 == "PASS" else "no PASS"))
    print(f"SEC5-1 level as computed from SEC5-S and SEC5-2: {level}")
    if C:
        kc = sum(nb(R[d]["c"], R[d]) for d in names)
        vc = "NOT DECIDABLE" if N < MIN_N else ("PASS" if kc >= need else "FAIL")
        print(f"SEC5-C the CRR-guided candidate {C_CHOSEN} (A6) not behind the tuned lambda: {kc}/{N} (need {need}) -> {vc}; "
              + ", ".join(f"{d}:{R[d]['c'] - R[d]['tacc']:+.4f}" for d in names))
        cdiv = [d for d in names if any(a < DIV_FRAC * R[d]["tacc"] for a in R[d]["c_seeds"])]
        cfl = sum(nb(R[d]["c"], R[d]) != nb(v, R[d]) for d in names for v in R[d]["c_sens"].values())
        print(f"SEC5-CS sensitivity over the 3 window cells: flips in {cfl} of {3 * N} -> {'FRAGILE' if cfl > 1 else 'not fragile'}; divergent carriers {cdiv}")
        ahead = [d for d in names if R[d]["c"] - R[d]["g"] >= R[d]["step"]]; behind = [d for d in names if R[d]["g"] - R[d]["c"] >= R[d]["step"]]
        print(f"SEC5-CR (report) {C_CHOSEN} against the clip: ahead by a step on {len(ahead)} {ahead}, behind by a step on {len(behind)} {behind}, "
              f"mean −clip {float(np.mean([R[d]['c'] - R[d]['g'] for d in names])):+.4f}")
    print("SEC5-K compute (report; CPU seconds from the timing files):")
    for d in names:
        t = times.get(d, [])
        cpu = lambda mode, val=None, fs=S.FS, fe=S.FE: sum(x["cpu_s"] for x in t if x["mode"] == mode and x["fs"] == fs and x["fe"] == fe  # noqa: E731
                                                          and (val is None or abs(x["value"] - val) <= 1e-6 * max(1.0, abs(val))))
        full = cpu("fixed"); gcpu = cpu(G, KAPPA); raw = cpu("bayes", 0.0)
        print(f"   {d}: configurations full sweep {R[d]['n_cfg']}, clipped SEC 1; CPU s full {full:.1f}, clipped SEC {gcpu:.1f}"
              + (f" (share {gcpu / full:.4f}), raw Laplace {raw:.1f} (overhead x{gcpu / raw if raw else float('nan'):.3f})" if full else ""))
    print("SEC5-E guard firings (report): " + "; ".join(f"{d}: {R[d]['fired']}" for d in names))


def data_check():
    man = {}
    for line in open(ROOT / "data" / "manifests" / "sec5.sha256"):
        if line.strip(): h_, pth = line.split()[:2]; man[pth] = h_
    bad = []
    for did, (name, _, _) in DATASETS.items():
        for ext in ("arff", "json"):
            pth = f"data/raw/openml/{did}_{name}.{ext}"; got = S.sha256(ROOT / pth) if (ROOT / pth).exists() else None
            print(f"{did} {name} .{ext}: sha256 {got} manifest {man.get(pth)} -> {'ok' if got and got == man.get(pth) else 'MISMATCH'}")
            if not got or got != man.get(pth): bad.append(f"{name}.{ext}")
    print("data check: " + (f"all {2 * len(DATASETS)} raw files match data/manifests/sec5.sha256" if not bad else f"MISMATCH {bad}: the study stops"))
    return not bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "devid": devid()
    elif cmd == "devone":
        outp = sys.argv[sys.argv.index("--out") + 1]
        with open(outp, "w") as out: dev_one(sys.argv[2], int(sys.argv[3]), out)
    elif cmd == "devreport": dev_report(sys.argv[2], sys.argv[3:])
    elif cmd == "check": sys.exit(0 if data_check() else 1)
    elif cmd == "all":
        did = int(sys.argv[2])
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else f"runs/sec5/results_{did}.jsonl"
        tp = sys.argv[sys.argv.index("--times") + 1] if "--times" in sys.argv else outp.replace("results_", "times_")
        with open(outp, "w") as out, open(tp, "w") as tout: run_carrier(did, out, tout)
    elif cmd == "score": score(sys.argv[2:])
    elif cmd == "smokefull":
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp/results_sec5_smoke.jsonl"
        with open(outp, "w") as out, open(outp.replace("results_", "times_"), "w") as tout: run_carrier(0, out, tout, synthetic=True)
        score([outp])
    else: raise SystemExit(__doc__)
