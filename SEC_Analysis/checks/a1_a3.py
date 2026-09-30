"""SEC_Analysis A1-A3 and forecasts F1, F2, F3(a), F3(b) (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; Amendment 1 at
347cb90; prompt-log entry 257): where SEC's margin comes from, whether the calibration collapses the optimum's location, and
whether SEC's pass is the plateau containing 1/2.

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads the pinned run records through sec_lib.load_all()
(validated first: loader_check.txt, every pinned count REPRODUCED) over all 42 scored carriers of SEC1, SCL3, SEC3, SEC4 and
SEC5, and nothing else: it opens no data and trains nothing. The SEC arm is the unclipped 'bayes_sec' on every carrier. The
clipped SEC ('bayes_sec_clip', SEC4 and SEC5 only) is printed beside it as a report and is never scored against a forecast.

Definitions (the declaration's, through sec_lib's primitives; tuned lambda, step and not-behind are never re-derived here).
The step is the carrier's step at lambda*_raw (sec_lib C["step"]) on every axis and in every unit conversion.
  A1  shape gain    = tacc_sec - tacc  (lambda*_sec's seed mean minus lambda*_raw's)
      location cost = SEC - tacc_sec   (SEC's seed mean minus lambda*_sec's)
      both in points and in steps; their sum is SEC's margin against the tuned lambda (asserted).
      F1 HOLDS iff (i) among the carriers where SEC is not behind (SEC - tacc > -step), the share with |location cost| < step
      is >= 0.75, AND (ii) the number of carriers, of all 42, with shape gain > step is < 21 (fewer than half).
      "Within a step" is read two-sided and strict, |location cost| < step: the declaration's other "within a step" (FM4,
      "a TIE") is two-sided, m_checks.py scores FM4 as |M4 - C0| < step, and not behind is strict. The one-sided reading
      (location cost > -step) is printed beside it as a report, with a line naming the ambiguity. Where shape gain <= 0, the
      lower half of (i) is forced by not behind (location = margin - shape >= margin > -step); the upper half is not; both
      counts are printed.
  A2  log10(lambda*_raw / 0.5) and log10(lambda*_sec / 0.5) per carrier; SD (ddof=1), min, max and range (max - min) of
      each per family (family = study) and pooled. F2 HOLDS iff SD_sec <= 0.5 * SD_raw in each of the five families.
  A3  per carrier and axis the not-behind set (sec_lib.plateau): the grid points whose seed mean is > best - step, with
      best = tacc on the raw axis ('fixed') and best = tacc_sec on the calibrated axis ('fixed_sec'); its lowest and highest
      grid point, width in decades log10(hi / lo) (0 for one point), size and gaps (grid points inside [lo, hi] not in the
      set). bracket = lo <= 0.5 <= hi on the calibrated axis (sec_lib.brackets).
      F3(a) HOLDS iff the share of the 42 carriers with bracket == (SEC not behind) is >= 0.90.
      F3(b) HOLDS iff (median over the 42 of the raw width) / (median over the 42 of the calibrated width) lies in [0.5, 2]
      (a zero calibrated median gives an infinite ratio: FAILS).
0.5 IS SEC'S NOMINAL WEIGHT, NOT ITS EFFECTIVE ONE ON THE CALIBRATED AXIS. In runs/sec1/frozen/sec1_score.run, 'bayes_sec'
applies w = 1/2 to imp_bayes / n_t = sum_j (n_j / n_t) s_j f_j while task t trains, and 'fixed_sec' applies lambda * sum_j
s_j f_j. So SEC's effective multiplier on old task j is 0.5 * n_j / n_t (n = training rows per task, sec_lib per_task_n), which
is 0.5 only where the per-task n are equal. The declaration fixes 0.5 for A2 and A3 and the scored numbers use it exactly;
A1's location cost therefore includes this task-size reweighting as well as the choice of 1/2. The effective range
[min, max] of 0.5 n_j / n_t over old tasks j < current task t is printed per carrier as a report, with whether the calibrated
plateau overlaps it.
Reports, never scored: per-family breakdowns of every count; the clipped SEC's decomposition and its not-behind label against
the same bracket (SEC4 and SEC5); tied grid points at the best seed mean, read with a tolerance TIE_TOL (far below one test
row) with the full tied range (the scorers take the smallest tied lambda, which then sets lambda* in A2), and F2 under the
largest tied lambda and the tied range's geometric midpoint; F3(a)'s disagreeing carriers with A1's parts beside them; plateaus
touching their grid's lowest or highest point (their widths are lower bounds; the calibrated grid starts a decade below the
raw one) and F3(b) with the calibrated plateau restricted to the carrier's raw grid range; F3(a) and F3(b) under two other
readings of A3 (the calibrated set read against tacc, and with step_sec); and Amendment 1's report: F1, F2, F3(a) and F3(b)
recomputed with the floor-bound carriers removed (floor = 100 * the majority class's share of the loaded rows, from the
header's class_counts; floor-bound iff tacc - floor < 3 steps), labelled post hoc. The declaration's reading of F1 ("SEC works
mainly because ...") is forecast text, not a computation; it is printed once, as such, with the computed qualifiers beside it.
Accuracies are the frozen scorers' (per cent; a non-finite run is recorded as 0 and enters the seed mean as 0). Decisive
numbers are printed at full precision beside the rounded value.

    uv run python SEC_Analysis/checks/a1_a3.py > SEC_Analysis/checks/a1_a3.txt
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sec_lib as L  # noqa: E402

D = L.load_all(); BY = L.by_study(D); CS = list(D.values())
SEC, CLIP, W = "bayes_sec", "bayes_sec_clip", 0.5
F1_SHARE, F2_RATIO, F3A_SHARE, F3B_LO, F3B_HI = 0.75, 0.5, 0.90, 0.5, 2.0
FLOOR_STEPS = 3.0                                    # Amendment 1 (A12): floor-bound iff tacc - floor < 3 steps
TIE_TOL = 1e-9                                       # points; tied grid means (report only)
BAR = "=" * 150


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "Y" if b else "N"


def frac(k, n):
    return f"{k}/{n} = {k / n!r} ({k / n:.3f})" if n else f"{k}/{n} (empty)"


def key(C):
    return (C["study"], C["carrier"])


def a1(C, mode):
    a = C["primary"][mode].mean; st = C["step"]
    shape = C["tacc_sec"] - C["tacc"]; loc = a - C["tacc_sec"]
    assert abs(shape + loc - L.margin(C, a)) < 1e-9, (C["carrier"], mode)
    return dict(a=a, shape=shape, loc=loc, shape_s=shape / st, loc_s=loc / st, marg_s=L.margin_steps(C, a),
                nb=L.not_behind(a, C["tacc"], st), loc_ok=abs(loc) < st, loc_lo=loc > -st, shape_big=shape > st)


def a1_table(rows, mode):
    print(f"   {'study':5} {'carrier':34} {'lam*_raw':>9} {'tacc':>8} {'step':>6} {'lam*_sec':>9} {'tacc_sec':>8} {mode:>14}"
          f" {'shape pp':>9} {'steps':>7} {'loc pp':>9} {'steps':>7} {'margin st':>9}  nb |loc|<st loc>-st shape>st")
    for C, r in rows:
        print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:9.4g} {C['tacc']:8.4f} {C['step']:6.3f} {C['tuned_sec']:9.4g}"
              f" {C['tacc_sec']:8.4f} {r['a']:14.4f} {r['shape']:+9.4f} {r['shape_s']:+7.3f} {r['loc']:+9.4f} {r['loc_s']:+7.3f}"
              f" {r['marg_s']:+9.3f}   {yn(r['nb'])}     {yn(r['loc_ok'])}       {yn(r['loc_lo'])}       {yn(r['shape_big'])}")


def f1_eval(rows):
    nb = [r for r in rows if r["nb"]]
    k1, n1 = sum(r["loc_ok"] for r in nb), len(nb); k2, n2 = sum(r["shape_big"] for r in rows), len(rows)
    i = n1 > 0 and k1 / n1 >= F1_SHARE; ii = k2 < n2 / 2
    return dict(k1=k1, n1=n1, k2=k2, n2=n2, i=i, ii=ii, ok=i and ii)


def sd_or_none(v):
    return float(np.std(np.asarray(v, dtype=float), ddof=1)) if len(v) >= 2 else None


def f2_eval(xs):
    """xs: {key: (x_raw, x_sec)}. Per family SD ratio; the word is FAILS if a family with defined SDs fails, NOT DECIDABLE if
    none fails but some family has fewer than 2 carriers (SD undefined), HOLDS otherwise."""
    fams = []
    for fam in L.STUDIES:
        ks = [k for k in xs if k[0] == fam]
        sdr, sds = sd_or_none([xs[k][0] for k in ks]), sd_or_none([xs[k][1] for k in ks])
        ok = None if sdr is None else sds <= F2_RATIO * sdr
        fams.append((fam, len(ks), sdr, sds, ok))
    if any(ok is False for *_, ok in fams):
        w = "FAILS"
    elif any(ok is None for *_, ok in fams):
        w = "NOT DECIDABLE"
    else:
        w = "HOLDS"
    return fams, w


def f3b_eval(wr, wc):
    wr = [x for x in wr if x is not None]; wc = [x for x in wc if x is not None]
    mr, mc = float(np.median(wr)), float(np.median(wc))
    ratio = mr / mc if mc > 0 else math.inf
    return mr, mc, ratio, F3B_LO <= ratio <= F3B_HI, len(wr), len(wc)


def tied(means, best):
    return [w for w in sorted(means) if abs(means[w] - best) <= TIE_TOL]


def eff_range(C):
    n = C["per_task_n"]
    e = [W * n[j] / n[t] for t in range(1, len(n)) for j in range(t)]
    return min(e), max(e)


def floor_of(C):
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * max(cc) / sum(cc)


def edge(p, grid):
    g = sorted(grid)
    return ("lo" if p["lo"] == g[0] else "") + ("hi" if p["hi"] == g[-1] else "") or "-"


# ---------------------------------------------------------------------------------------------------------------- header
print(BAR)
print("SEC_Analysis A1-A3 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; Amendment 1 at 347cb90): F1, F2, F3(a), F3(b)")
print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecasts, never PASS")
print(BAR)
print(f"carriers: {len(CS)} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); SEC arm '{SEC}' on every carrier;"
      f" clipped SEC '{CLIP}' on {sum(CLIP in C['primary'] for C in CS)} (report only)")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); not behind = arm - tacc > -step (strict); points"
      " are per cent accuracy")
print("0.5 is SEC's nominal weight: on the calibrated axis its effective multiplier on old task j while task t trains is"
      " 0.5 n_j / n_t (sec1_score.run: w = 1/2 on imp_bayes / n_t);")
print(f"   it is 0.5 exactly on {sum(eff_range(C) == (W, W) for C in CS)} of {len(CS)} carriers (equal per-task n); the"
      " declaration fixes 0.5 for A2 and A3, and A1's location cost includes this reweighting (report in A3)")

# ------------------------------------------------------------------------------------------------------------------- A1
print(); print(BAR)
print("A1  where does SEC's margin come from?  shape gain = tacc_sec - tacc; location cost = SEC - tacc_sec; margin = sum")
print(BAR)
R1 = [(C, a1(C, SEC)) for C in CS]
A1R = {key(C): r for C, r in R1}
a1_table(R1, SEC)
print("per family (report):")
for s in L.STUDIES:
    rr = [(C, r) for C, r in R1 if C["study"] == s]; nb = [r for _, r in rr if r["nb"]]
    print(f"   {s:5} SEC not behind {len(nb)}/{len(rr)}; of those, |location cost| < step {sum(r['loc_ok'] for r in nb)}/{len(nb)}"
          f" (location cost > -step {sum(r['loc_lo'] for r in nb)}/{len(nb)}); shape gain > step"
          f" {sum(r['shape_big'] for _, r in rr)}/{len(rr)}; shape gain < -step {sum(r['shape'] < -C['step'] for C, r in rr)}/{len(rr)}")
F1 = f1_eval([r for _, r in R1])
nbR = [r for _, r in R1 if r["nb"]]
print("pooled over the 42 (report): median shape gain in steps"
      f" {float(np.median([r['shape_s'] for _, r in R1])):+.3f}, median location cost in steps"
      f" {float(np.median([r['loc_s'] for _, r in R1])):+.3f}; among the {F1['n1']} not behind: shape gain"
      f" {float(np.median([r['shape_s'] for r in nbR])):+.3f}, location cost {float(np.median([r['loc_s'] for r in nbR])):+.3f}")
pos = [r for r in nbR if r["shape"] > 0]; neg = [r for r in nbR if r["shape"] <= 0]
print(f"arithmetic (report): where shape gain <= 0, not behind forces the lower half of (i) (location = margin - shape >= margin"
      f" > -step); the upper half (location cost < step) is not forced.")
print(f"   shape gain <= 0 on {len(neg)} of the {F1['n1']}: |location cost| < step on {sum(r['loc_ok'] for r in neg)}/{len(neg)};"
      f" shape gain > 0 on {len(pos)}: |location cost| < step on {sum(r['loc_ok'] for r in pos)}/{len(pos)}, location cost >"
      f" -step on {sum(r['loc_lo'] for r in pos)}/{len(pos)}")
print("ambiguity (named): the declaration's \"within a step\" is read two-sided and strict, |location cost| < step (as FM4's"
      " \"within a step ... (a TIE)\", scored |M4 - C0| < step in m_checks.py)")
print(f"   one-sided reading (report): location cost > -step on {sum(r['loc_lo'] for r in nbR)}/{F1['n1']} of the {F1['n1']};"
      f" largest location cost among them {max(r['loc_s'] for r in nbR):+.3f} steps, smallest {min(r['loc_s'] for r in nbR):+.3f}")
print(f"F1 (i)  |location cost| < step among the {F1['n1']} carriers where SEC is not behind: {frac(F1['k1'], F1['n1'])} >="
      f" {F1_SHARE} -> {F1['i']}")
print(f"F1 (ii) shape gain > step on {F1['k2']} of {F1['n2']} carriers; fewer than half (< {F1['n2'] / 2:g}) -> {F1['ii']}")
print(f"F1: {word(F1['ok'])}")

print("\nA1 report (not a forecast): the clipped SEC's decomposition on SEC4 and SEC5 (same shape gain; location cost ="
      " clipped SEC - tacc_sec)")
RC = [(C, a1(C, CLIP)) for C in CS if CLIP in C["primary"]]
a1_table(RC, CLIP)
for s in ("sec4", "sec5"):
    rr = [r for C, r in RC if C["study"] == s]; nb = [r for r in rr if r["nb"]]
    print(f"   {s:5} clipped SEC not behind {len(nb)}/{len(rr)}; of those, |location cost| < step"
          f" {sum(r['loc_ok'] for r in nb)}/{len(nb)} (> -step {sum(r['loc_lo'] for r in nb)}/{len(nb)}); shape gain > step"
          f" {sum(r['shape_big'] for r in rr)}/{len(rr)}")
nbC = [r for _, r in RC if r["nb"]]
print(f"   pooled {len(RC)}: clipped SEC not behind {len(nbC)}/{len(RC)}; of those, |location cost| < step"
      f" {sum(r['loc_ok'] for r in nbC)}/{len(nbC)} (> -step {sum(r['loc_lo'] for r in nbC)}/{len(nbC)})")

# ------------------------------------------------------------------------------------------------------------------- A2
print(); print(BAR)
print("A2  does the calibration collapse the optimum's location?  x_raw = log10(lambda*_raw / 0.5), x_sec = log10(lambda*_sec / 0.5)")
print(BAR)
print(f"   {'study':5} {'carrier':34} {'lam*_raw':>10} {'x_raw':>8} {'lam*_sec':>10} {'x_sec':>8}")
X = {}
for C in CS:
    xr, xs = math.log10(C["tuned"] / W), math.log10(C["tuned_sec"] / W)
    X[key(C)] = (xr, xs)
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:10.6g} {xr:+8.4f} {C['tuned_sec']:10.6g} {xs:+8.4f}")

print(f"tied grid points at the best seed mean (report; |mean - best| <= {TIE_TOL:g} points, while one test row moves a seed"
      f" mean by >= {min(100.0 / (len(L.SEEDS) * C['n_test']) for C in CS):.3g} points on every carrier):")
TR = {key(C): (tied(C["raw_means"], C["tacc"]), tied(C["sec_means"], C["tacc_sec"])) for C in CS}
for C in CS:
    tr, ts = TR[key(C)]
    if len(tr) > 1 or len(ts) > 1:
        print(f"   {C['study']:5} {C['carrier'][:34]:34} raw {len(tr)} tied ({tr[0]:g} to {tr[-1]:g}); calibrated {len(ts)} tied"
              f" ({ts[0]:g} to {ts[-1]:g})")
print(f"   the scorers' lambda* is the smallest tied lambda on {sum(TR[key(C)][0][0] == C['tuned'] for C in CS)}/{len(CS)} (raw)"
      f" and {sum(TR[key(C)][1][0] == C['tuned_sec'] for C in CS)}/{len(CS)} (calibrated)")


def spread(v):
    v = np.asarray(v, dtype=float)
    return float(np.std(v, ddof=1)), float(v.min()), float(v.max()), float(v.max() - v.min())


print(f"   {'family':6} {'n':>3} {'SD_raw':>8} {'min':>8} {'max':>8} {'range':>7} | {'SD_sec':>8} {'min':>8} {'max':>8} {'range':>7}"
      f" | {'SD_sec/SD_raw':>13}  SD_sec <= 0.5 SD_raw")
for fam in list(L.STUDIES) + ["pooled"]:
    keys = [k for k in X if fam == "pooled" or k[0] == fam]
    sr, ss = spread([X[k][0] for k in keys]), spread([X[k][1] for k in keys])
    tail = "   (report; F2 is per family, no pooled criterion)" if fam == "pooled" else f"  {ss[0] <= F2_RATIO * sr[0]}"
    print(f"   {fam:6} {len(keys):3d} {sr[0]:8.4f} {sr[1]:+8.4f} {sr[2]:+8.4f} {sr[3]:7.4f} | {ss[0]:8.4f} {ss[1]:+8.4f} {ss[2]:+8.4f}"
          f" {ss[3]:7.4f} | {ss[0] / sr[0]:13.4f}{tail}")
F2, F2W = f2_eval(X)
for fam, n, sdr, sds, ok in F2:
    print(f"F2 {fam:5}: SD_sec {sds!r} <= 0.5 * SD_raw {F2_RATIO * sdr!r} (SD_raw {sdr!r}; ratio {sds / sdr:.4f}) -> {ok}")
print(f"F2: {F2W}  (families where SD_sec <= 0.5 SD_raw: {sum(bool(ok) for *_, ok in F2)} of {len(F2)})")

print("F2 under other tie rules (report; the scored rule is the scorers' smallest tied lambda; 'largest' takes the largest"
      " tied lambda, 'midpoint' the tied range's geometric midpoint, on both axes):")
RULES = {"smallest": lambda t: t[0], "largest": lambda t: t[-1], "midpoint": lambda t: math.sqrt(t[0] * t[-1])}
F2T = {}
for rule, pick in RULES.items():
    xs = {k: (math.log10(pick(TR[k][0]) / W), math.log10(pick(TR[k][1]) / W)) for k in X}
    F2T[rule] = f2_eval(xs)
    print(f"   {rule:8} " + "; ".join(f"{fam} {sds / sdr:.4f} {yn(ok)}" for fam, n, sdr, sds, ok in F2T[rule][0])
          + f"  -> F2 {F2T[rule][1]}")
dep = [fam for i, fam in enumerate(L.STUDIES) if len({F2T[r][0][i][4] for r in RULES}) > 1]
print(f"   families whose SD_sec <= 0.5 SD_raw result depends on the tie rule: {', '.join(dep) if dep else 'none'};"
      f" the F2 word depends on it: {len({F2T[r][1] for r in RULES}) > 1}")

# ------------------------------------------------------------------------------------------------------------------- A3
print(); print(BAR)
print("A3  is SEC's pass the plateau containing 1/2?  not-behind set per axis: grid points with mean > best - step"
      " (raw best = tacc, calibrated best = tacc_sec)")
print(BAR)
print("   edge: the set's lowest (lo) or highest (hi) point is the carrier's grid minimum or maximum on that axis (the width is"
      " then a lower bound)")
print(f"   {'study':5} {'carrier':34} | {'raw lo':>9} {'raw hi':>9} {'dec':>6} {'n':>3} {'gap':>3} {'edge':>4} | {'cal lo':>9}"
      f" {'cal hi':>9} {'dec':>6} {'n':>3} {'gap':>3} {'edge':>4} | brackets 0.5  SEC nb  agree")
R3 = []
for C in CS:
    pr, pc = L.plateau(C["raw_means"], C["tacc"], C["step"]), L.plateau(C["sec_means"], C["tacc_sec"], C["step"])
    br, nb = L.brackets(pc, W), L.arm_nb(C, SEC)
    er, ec = edge(pr, C["raw_means"]), edge(pc, C["sec_means"])
    R3.append((C, pr, pc, br, nb, er, ec))
    print(f"   {C['study']:5} {C['carrier'][:34]:34} | {pr['lo']:9.4g} {pr['hi']:9.4g} {pr['decades']:6.3f} {len(pr['set']):3d}"
          f" {pr['gaps']:3d} {er:>4} | {pc['lo']:9.4g} {pc['hi']:9.4g} {pc['decades']:6.3f} {len(pc['set']):3d} {pc['gaps']:3d}"
          f" {ec:>4} |      {yn(br)}          {yn(nb)}      {yn(br == nb)}")
print("per family (report): bracket == SEC not behind; confusion (bracket, not behind): YY YN NY NN")
for fam in list(L.STUDIES) + ["pooled"]:
    rr = [t for t in R3 if fam == "pooled" or t[0]["study"] == fam]
    cf = [sum(t[3] == b and t[4] == v for t in rr) for b, v in ((1, 1), (1, 0), (0, 1), (0, 0))]
    print(f"   {fam:6} agree {sum(t[3] == t[4] for t in rr)}/{len(rr)};  YY {cf[0]}  YN {cf[1]}  NY {cf[2]}  NN {cf[3]}")
ka, na = sum(t[3] == t[4] for t in R3), len(R3)
f3a = ka / na >= F3A_SHARE
print("   disagreeing carriers, with A1's parts in steps (the bracket is read against tacc_sec, not behind against tacc):")
for t in R3:
    if t[3] != t[4]:
        r = A1R[key(t[0])]
        print(f"      {t[0]['study']:5} {t[0]['carrier'][:34]:34} bracket {yn(t[3])}, SEC nb {yn(t[4])};"
              f" shape gain {r['shape_s']:+.3f}, location cost {r['loc_s']:+.3f}, margin {r['marg_s']:+.3f} steps")
print(f"F3(a) bracket == SEC not behind on {frac(ka, na)} >= {F3A_SHARE} -> {f3a}")
print(f"F3(a): {word(f3a)}")
mr, mc, ratio, f3b, _, _ = f3b_eval([t[1]["decades"] for t in R3], [t[2]["decades"] for t in R3])
print("per family (report): median width in decades, raw | calibrated")
for fam in L.STUDIES:
    rr = [t for t in R3 if t[0]["study"] == fam]
    print(f"   {fam:6} {float(np.median([t[1]['decades'] for t in rr])):.4f} | {float(np.median([t[2]['decades'] for t in rr])):.4f}")
print(f"F3(b) median width over the {na}: raw {mr!r} ({mr:.4f}) decades, calibrated {mc!r} ({mc:.4f}) decades;"
      f" ratio raw / calibrated {ratio!r} ({ratio:.4f}) in [{F3B_LO}, {F3B_HI}] -> {f3b}")
print(f"F3(b): {word(f3b)}")

print("\nA3 report (not a forecast): grid edges and the calibrated plateau restricted to the raw grid's range")
for ax, i, gname in (("raw", 5, "raw_means"), ("calibrated", 6, "sec_means")):
    lo = sum("lo" in t[i] for t in R3); hi = sum("hi" in t[i] for t in R3); an = sum(t[i] != "-" for t in R3)
    gmin = sorted({min(t[0][gname]) for t in R3}); gmax = sorted({max(t[0][gname]) for t in R3})
    print(f"   {ax:10} plateaus touching the grid minimum {lo}/{na}, the grid maximum {hi}/{na}, either {an}/{na};"
          f" grid minima {', '.join(f'{g:g}' for g in gmin)}; grid maxima {', '.join(f'{g:g}' for g in gmax)}")
wres, n_empty = [], 0
for t in R3:
    g = sorted(t[0]["raw_means"]); rs = [w for w in t[2]["set"] if g[0] <= w <= g[-1]]
    n_empty += not rs
    wres.append(math.log10(rs[-1] / rs[0]) if rs else None)
m1, m2, rt, ok, _, n2 = f3b_eval([t[1]["decades"] for t in R3], wres)
print(f"   F3(b) with the calibrated set restricted to [raw grid min, raw grid max] per carrier ({n_empty} left empty, {n2}"
      f" widths): raw {m1:.4f} / calibrated {m2:.4f} = {rt!r} ({rt:.4f}) in [{F3B_LO}, {F3B_HI}] -> {word(ok)} (report)")

print("\nA3 report (not a forecast): F3(a) and F3(b) under two other readings of the calibrated not-behind set")
for name, best_of, st_key in (("read against tacc (mean > tacc - step)", "tacc", "step"),
                               ("with step_sec (mean > tacc_sec - step_sec)", "tacc_sec", "step_sec")):
    ps = [L.plateau(t[0]["sec_means"], t[0][best_of], t[0][st_key]) for t in R3]
    k = sum(L.brackets(p, W) == t[4] for p, t in zip(ps, R3)); ne = sum(not p["set"] for p in ps)
    dis = [f"{t[0]['carrier']}" for p, t in zip(ps, R3) if L.brackets(p, W) != t[4]]
    m1, m2, rt, ok, _, n2 = f3b_eval([t[1]["decades"] for t in R3], [p["decades"] for p in ps])
    print(f"   {name}: F3(a) {frac(k, na)} -> {word(k / na >= F3A_SHARE)}; F3(b) raw {m1:.4f} / calibrated {m2:.4f} over {n2}"
          f" non-empty sets ({ne} empty) = {rt:.4f} -> {word(ok)}")
    print(f"      disagreeing: {', '.join(dis)}")

print("\nA3 report (not a forecast): SEC's effective multiplier range on the calibrated axis, [min, max] of 0.5 n_j / n_t over"
      " old tasks j < current task t, against the calibrated plateau")
print(f"   {'study':5} {'carrier':34} {'per-task n':>34} {'eff min':>8} {'eff max':>8} | {'cal lo':>9} {'cal hi':>9} |"
      f" overlaps  brackets 0.5  SEC nb  overlap==nb")
kov = 0
for t in R3:
    C, pc = t[0], t[2]; lo, hi = eff_range(C)
    ov = pc["lo"] is not None and pc["lo"] <= hi and pc["hi"] >= lo; kov += ov == t[4]
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {str(C['per_task_n']):>34} {lo:8.4g} {hi:8.4g} | {pc['lo']:9.4g} {pc['hi']:9.4g} |"
          f"    {yn(ov)}          {yn(t[3])}          {yn(t[4])}        {yn(ov == t[4])}")
print(f"   largest effective multiplier > 2 x 0.5 (a largest n_j / n_t above 2) on {sum(eff_range(t[0])[1] > 2 * W for t in R3)}"
      f"/{na}; overlap == SEC not behind on {frac(kov, na)} (report; F3(a) is scored on the nominal 0.5)")

print("\nA3 report (not a forecast): the clipped SEC's not-behind label against the same bracket, SEC4 and SEC5")
rc = [(t, L.arm_nb(t[0], CLIP)) for t in R3 if CLIP in t[0]["primary"]]
for t, nbc in rc:
    print(f"   {t[0]['study']:5} {t[0]['carrier'][:34]:34} brackets 0.5 {yn(t[3])}  clipped SEC nb {yn(nbc)}  agree {yn(t[3] == nbc)}")
print(f"   agree {sum(t[3] == nbc for t, nbc in rc)}/{len(rc)}")

# ------------------------------------------------------------------------------------------------------ Amendment 1 (A12)
print(); print(BAR)
print("Amendment 1 report (POST HOC in origin; 347cb90): F1, F2, F3(a), F3(b) with the floor-bound carriers removed")
print(BAR)
print(f"   floor = 100 x the majority class's share of the loaded rows (header class_counts); floor-bound iff tacc - floor <"
      f" {FLOOR_STEPS:g} steps")
print(f"   {'study':5} {'carrier':34} {'floor':>8} {'tacc':>8} {'step':>6} {'(tacc-floor)/step':>18}  floor-bound")
FB = {}
for C in CS:
    fl = floor_of(C); FB[key(C)] = C["tacc"] - fl < FLOOR_STEPS * C["step"]
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {fl:8.4f} {C['tacc']:8.4f} {C['step']:6.3f} {(C['tacc'] - fl) / C['step']:+18.3f}"
          f"  {yn(FB[key(C)])}")
print("   floor-bound per study: " + "; ".join(f"{s} {sum(FB[key(C)] for C in BY[s])}/{len(BY[s])}" for s in L.STUDIES)
      + f"; all {sum(FB.values())}/{len(CS)}; held-out (SCL3, SEC3, SEC4, SEC5)"
      f" {sum(FB[key(C)] for s in L.STUDIES[1:] for C in BY[s])}/{sum(len(BY[s]) for s in L.STUDIES[1:])}")
KEEP = [C for C in CS if not FB[key(C)]]
nk = len(KEEP)
print(f"   kept: {nk} carriers (" + ", ".join(f"{s} {sum(C['study'] == s for C in KEEP)}" for s in L.STUDIES) + ")")
F1K = f1_eval([A1R[key(C)] for C in KEEP])
print(f"   F1 (i)  |location cost| < step among the {F1K['n1']} kept carriers where SEC is not behind:"
      f" {frac(F1K['k1'], F1K['n1'])} >= {F1_SHARE} -> {F1K['i']}")
print(f"   F1 (ii) shape gain > step on {F1K['k2']} of {F1K['n2']}; fewer than half (< {F1K['n2'] / 2:g}) -> {F1K['ii']}")
print(f"   F1 floor-bound removed (report): {word(F1K['ok'])}")
F2K, F2KW = f2_eval({key(C): X[key(C)] for C in KEEP})
for fam, n, sdr, sds, ok in F2K:
    print(f"   F2 {fam:5} n {n:2d}: " + (f"SD_raw {sdr:.4f}, SD_sec {sds:.4f}, ratio {sds / sdr:.4f} <= {F2_RATIO} -> {ok}"
                                        if sdr is not None else "SD undefined (n < 2)"))
print(f"   F2 floor-bound removed (report): {F2KW}  (families with SD defined {sum(ok is not None for *_, ok in F2K)} of"
      f" {len(F2K)}; of those SD_sec <= 0.5 SD_raw {sum(bool(ok) for *_, ok in F2K)})")
R3K = [t for t in R3 if not FB[key(t[0])]]
kk = sum(t[3] == t[4] for t in R3K)
print(f"   F3(a) bracket == SEC not behind on {frac(kk, nk)} >= {F3A_SHARE} -> {kk / nk >= F3A_SHARE}")
print(f"   F3(a) floor-bound removed (report): {word(kk / nk >= F3A_SHARE)}")
m1, m2, rtk, okk, _, _ = f3b_eval([t[1]["decades"] for t in R3K], [t[2]["decades"] for t in R3K])
print(f"   F3(b) median width over the {nk}: raw {m1:.4f}, calibrated {m2:.4f}; ratio {rtk!r} ({rtk:.4f}) in [{F3B_LO}, {F3B_HI}]"
      f" -> {okk}")
print(f"   F3(b) floor-bound removed (report): {word(okk)}")

# -------------------------------------------------------------------------------------------------------------- summary
print(); print(BAR)
print("summary (words computed above; the words for the declared forecasts are those on all 42 carriers)")
print(f"   F1    {word(F1['ok'])}   (i) {F1['k1']}/{F1['n1']} |location cost| < step where SEC not behind (>= {F1_SHARE});"
      f" (ii) {F1['k2']}/{F1['n2']} shape gain > step (< {F1['n2'] / 2:g})")
print(f"   F2    {F2W}   " + "; ".join(f"{fam} {sds / sdr:.3f}" for fam, n, sdr, sds, _ in F2)
      + f" (SD_sec / SD_raw, each <= {F2_RATIO})")
print(f"   F3(a) {word(f3a)}   {ka}/{na} bracket == SEC not behind (>= {F3A_SHARE})")
print(f"   F3(b) {word(f3b)}   median width raw {mr:.4f} / calibrated {mc:.4f} = {ratio:.4f} (in [{F3B_LO}, {F3B_HI}])")
print(f"   floor-bound removed ({nk} carriers; Amendment 1 report, post hoc): F1 {word(F1K['ok'])}, F2 {F2KW},"
      f" F3(a) {word(kk / nk >= F3A_SHARE)}, F3(b) {word(okk)}")
print("the declaration's reading of F1 (forecast text, not computed here): \"SEC works mainly because 1/2 lands near the"
      " calibrated optimum, not because the calibrated shape beats the raw one\"")
print(f"   computed qualifiers: F1(i)'s lower half is forced by not behind on {len(neg)} of its {F1['n1']} carriers (shape gain"
      f" <= 0); F3(a) {word(f3a)} ({ka}/{na}); 0.5 is SEC's effective multiplier on {sum(eff_range(C) == (W, W) for C in CS)}"
      f" of {len(CS)} carriers only, so the location cost includes the task-size reweighting; with the floor-bound carriers"
      f" removed F1 reads {word(F1K['ok'])}")
