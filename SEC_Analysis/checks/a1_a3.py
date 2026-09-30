"""SEC_Analysis A1-A3 and forecasts F1, F2, F3(a), F3(b) (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log
entry 257): where SEC's margin comes from, whether the calibration collapses the optimum's location, and whether SEC's
pass is the plateau containing 1/2.

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads the pinned run records through sec_lib.load_all()
(validated first: loader_check.txt, every pinned count REPRODUCED) over all 42 scored carriers of SEC1, SCL3, SEC3, SEC4 and
SEC5, and nothing else: it opens no data and trains nothing. The SEC arm is the unclipped 'bayes_sec' on every carrier. The
clipped SEC ('bayes_sec_clip', SEC4 and SEC5 only) is printed beside it as a report and is never scored against a forecast.

Definitions (the declaration's, through sec_lib's primitives; tuned lambda, step and not-behind are never re-derived here).
The step is the carrier's step at lambda*_raw (sec_lib C["step"]) on every axis and in every unit conversion.
  A1  shape gain    = tacc_sec - tacc  (lambda*_sec's seed mean minus lambda*_raw's)
      location cost = SEC - tacc_sec   (SEC's seed mean minus lambda*_sec's)
      both in points and in steps; their sum is SEC's margin against the tuned lambda (asserted).
      F1 HOLDS iff (i) among the carriers where SEC is not behind (SEC - tacc > -step), the share with location cost > -step
      is >= 0.75, AND (ii) the number of carriers, of all 42, with shape gain > step is < 21 (fewer than half).
      "Within a step" is scored one-sided (location cost > -step), as not behind is; the two-sided count |location cost| <
      step is printed beside it as a report. Where shape gain <= 0, (i) is forced by not behind (location = margin - shape
      >= margin > -step); the count of carriers where it is informative (shape gain > 0) is printed.
  A2  log10(lambda*_raw / 0.5) and log10(lambda*_sec / 0.5) per carrier; SD (ddof=1), min, max and range (max - min) of
      each per family (family = study) and pooled. F2 HOLDS iff SD_sec <= 0.5 * SD_raw in each of the five families.
  A3  per carrier and axis the not-behind set (sec_lib.plateau): the grid points whose seed mean is > best - step, with
      best = tacc on the raw axis ('fixed') and best = tacc_sec on the calibrated axis ('fixed_sec'); its lowest and highest
      grid point, width in decades log10(hi / lo) (0 for one point), size and gaps (grid points inside [lo, hi] not in the
      set). bracket = lo <= 0.5 <= hi on the calibrated axis (sec_lib.brackets).
      F3(a) HOLDS iff the share of the 42 carriers with bracket == (SEC not behind) is >= 0.90.
      F3(b) HOLDS iff (median over the 42 of the raw width) / (median over the 42 of the calibrated width) lies in [0.5, 2]
      (a zero calibrated median gives an infinite ratio: FAILS).
Reports, never scored: per-family breakdowns of every count; the clipped SEC's decomposition and its not-behind label against
the same bracket (SEC4 and SEC5); the carriers whose best grid mean is an exact tie (the scorers take the smallest tied
lambda, which then sets lambda* in A2); F3(a)'s disagreeing carriers with A1's parts beside them.
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
BAR = "=" * 150


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "Y" if b else "N"


def frac(k, n):
    return f"{k}/{n} = {k / n!r} ({k / n:.3f})"


def a1(C, mode):
    a = C["primary"][mode].mean; st = C["step"]
    shape = C["tacc_sec"] - C["tacc"]; loc = a - C["tacc_sec"]
    assert abs(shape + loc - L.margin(C, a)) < 1e-9, (C["carrier"], mode)
    return dict(a=a, shape=shape, loc=loc, shape_s=shape / st, loc_s=loc / st, marg_s=L.margin_steps(C, a),
                nb=L.not_behind(a, C["tacc"], st), loc_ok=loc > -st, shape_big=shape > st)


def a1_table(rows, mode):
    print(f"   {'study':5} {'carrier':34} {'lam*_raw':>9} {'tacc':>8} {'step':>6} {'lam*_sec':>9} {'tacc_sec':>8} {mode:>14}"
          f" {'shape pp':>9} {'steps':>7} {'loc pp':>9} {'steps':>7} {'margin st':>9}  nb loc>-st shape>st")
    for C, r in rows:
        print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:9.4g} {C['tacc']:8.4f} {C['step']:6.3f} {C['tuned_sec']:9.4g}"
              f" {C['tacc_sec']:8.4f} {r['a']:14.4f} {r['shape']:+9.4f} {r['shape_s']:+7.3f} {r['loc']:+9.4f} {r['loc_s']:+7.3f}"
              f" {r['marg_s']:+9.3f}   {yn(r['nb'])}     {yn(r['loc_ok'])}       {yn(r['shape_big'])}")


# ---------------------------------------------------------------------------------------------------------------- header
print(BAR)
print("SEC_Analysis A1-A3 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f): F1, F2, F3(a), F3(b)")
print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecasts, never PASS")
print(BAR)
print(f"carriers: {len(CS)} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); SEC arm '{SEC}' on every carrier;"
      f" clipped SEC '{CLIP}' on {sum(CLIP in C['primary'] for C in CS)} (report only)")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); not behind = arm - tacc > -step (strict); points"
      " are per cent accuracy")

# ------------------------------------------------------------------------------------------------------------------- A1
print(); print(BAR)
print("A1  where does SEC's margin come from?  shape gain = tacc_sec - tacc; location cost = SEC - tacc_sec; margin = sum")
print(BAR)
R1 = [(C, a1(C, SEC)) for C in CS]
a1_table(R1, SEC)
print("per family (report):")
for s in L.STUDIES:
    rr = [r for C, r in R1 if C["study"] == s]; nb = [r for r in rr if r["nb"]]
    print(f"   {s:5} SEC not behind {sum(r['nb'] for r in rr)}/{len(rr)}; of those, location cost > -step"
          f" {sum(r['loc_ok'] for r in nb)}/{len(nb)}; shape gain > step {sum(r['shape_big'] for r in rr)}/{len(rr)};"
          f" shape gain < -step {sum(r['shape'] < -C['step'] for C, r in R1 if C['study'] == s)}/{len(rr)}")
nbR = [r for _, r in R1 if r["nb"]]
k1, n1 = sum(r["loc_ok"] for r in nbR), len(nbR)
k2, n2 = sum(r["shape_big"] for _, r in R1), len(R1)
f1i = k1 / n1 >= F1_SHARE; f1ii = k2 < n2 / 2
print("pooled over the 42 (report): median shape gain in steps"
      f" {float(np.median([r['shape_s'] for _, r in R1])):+.3f}, median location cost in steps"
      f" {float(np.median([r['loc_s'] for _, r in R1])):+.3f}; among the {n1} not behind: shape gain"
      f" {float(np.median([r['shape_s'] for r in nbR])):+.3f}, location cost {float(np.median([r['loc_s'] for r in nbR])):+.3f}")
pos = [r for r in nbR if r["shape"] > 0]
print(f"arithmetic (report): where shape gain <= 0, not behind forces location cost > -step (location = margin - shape >="
      f" margin > -step); that holds on {n1 - len(pos)} of the {n1}; on the {len(pos)} with shape gain > 0 location cost >"
      f" -step on {sum(r['loc_ok'] for r in pos)}/{len(pos)}")
print(f"two-sided reading (report): |location cost| < step on {sum(abs(r['loc']) < C['step'] for C, r in R1 if r['nb'])}/{n1}"
      f" of the {n1}; largest location cost among them {max(r['loc_s'] for r in nbR):+.3f} steps")
print(f"F1 (i)  location cost > -step among the {n1} carriers where SEC is not behind: {frac(k1, n1)} >= {F1_SHARE} -> {f1i}")
print(f"F1 (ii) shape gain > step on {k2} of {n2} carriers; fewer than half (< {n2 / 2:g}) -> {f1ii}")
print(f"F1: {word(f1i and f1ii)}  (the forecast read: \"SEC works mainly because 1/2 lands near the calibrated optimum, not"
      " because the calibrated shape beats the raw one\")")

print("\nA1 report (not a forecast): the clipped SEC's decomposition on SEC4 and SEC5 (same shape gain; location cost ="
      " clipped SEC - tacc_sec)")
RC = [(C, a1(C, CLIP)) for C in CS if CLIP in C["primary"]]
a1_table(RC, CLIP)
for s in ("sec4", "sec5"):
    rr = [r for C, r in RC if C["study"] == s]; nb = [r for r in rr if r["nb"]]
    print(f"   {s:5} clipped SEC not behind {len(nb)}/{len(rr)}; of those, location cost > -step"
          f" {sum(r['loc_ok'] for r in nb)}/{len(nb)}; shape gain > step {sum(r['shape_big'] for r in rr)}/{len(rr)}")
nbC = [r for _, r in RC if r["nb"]]
print(f"   pooled {len(RC)}: clipped SEC not behind {len(nbC)}/{len(RC)}; of those, location cost > -step"
      f" {sum(r['loc_ok'] for r in nbC)}/{len(nbC)}")

# ------------------------------------------------------------------------------------------------------------------- A2
print(); print(BAR)
print("A2  does the calibration collapse the optimum's location?  x_raw = log10(lambda*_raw / 0.5), x_sec = log10(lambda*_sec / 0.5)")
print(BAR)
print(f"   {'study':5} {'carrier':34} {'lam*_raw':>10} {'x_raw':>8} {'lam*_sec':>10} {'x_sec':>8}")
X = {}
for C in CS:
    xr, xs = math.log10(C["tuned"] / W), math.log10(C["tuned_sec"] / W)
    X[(C["study"], C["carrier"])] = (xr, xs)
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:10.6g} {xr:+8.4f} {C['tuned_sec']:10.6g} {xs:+8.4f}")


print("exact ties at the best seed mean (report; the scorers' rule takes the smallest tied lambda, which sets lambda* here):")
for C in CS:
    tr = [w for w, m in C["raw_means"].items() if m == C["tacc"]]; ts = [w for w, m in C["sec_means"].items() if m == C["tacc_sec"]]
    if len(tr) > 1 or len(ts) > 1:
        print(f"   {C['study']:5} {C['carrier'][:34]:34} raw {len(tr)} tied ({tr[0]:g} to {tr[-1]:g}); calibrated {len(ts)} tied"
              f" ({ts[0]:g} to {ts[-1]:g})")


def spread(v):
    v = np.asarray(v, dtype=float)
    return float(np.std(v, ddof=1)), float(v.min()), float(v.max()), float(v.max() - v.min())


print(f"   {'family':6} {'n':>3} {'SD_raw':>8} {'min':>8} {'max':>8} {'range':>7} | {'SD_sec':>8} {'min':>8} {'max':>8} {'range':>7}"
      f" | {'SD_sec/SD_raw':>13}  SD_sec <= 0.5 SD_raw")
f2 = []
for fam in list(L.STUDIES) + ["pooled"]:
    keys = [k for k in X if fam == "pooled" or k[0] == fam]
    sr, ss = spread([X[k][0] for k in keys]), spread([X[k][1] for k in keys])
    ok = ss[0] <= F2_RATIO * sr[0]
    if fam != "pooled":
        f2.append((fam, sr[0], ss[0], ok))
    print(f"   {fam:6} {len(keys):3d} {sr[0]:8.4f} {sr[1]:+8.4f} {sr[2]:+8.4f} {sr[3]:7.4f} | {ss[0]:8.4f} {ss[1]:+8.4f} {ss[2]:+8.4f}"
          f" {ss[3]:7.4f} | {ss[0] / sr[0]:13.4f}  {ok}" + ("   (report; F2 is per family)" if fam == "pooled" else ""))
for fam, sdr, sds, ok in f2:
    print(f"F2 {fam:5}: SD_sec {sds!r} <= 0.5 * SD_raw {F2_RATIO * sdr!r} (SD_raw {sdr!r}; ratio {sds / sdr:.4f}) -> {ok}")
print(f"F2: {word(all(ok for *_, ok in f2))}  (families where SD_sec <= 0.5 SD_raw: {sum(ok for *_, ok in f2)} of {len(f2)})")

# ------------------------------------------------------------------------------------------------------------------- A3
print(); print(BAR)
print("A3  is SEC's pass the plateau containing 1/2?  not-behind set per axis: grid points with mean > best - step"
      " (raw best = tacc, calibrated best = tacc_sec)")
print(BAR)
print(f"   {'study':5} {'carrier':34} | {'raw lo':>9} {'raw hi':>9} {'dec':>6} {'n':>3} {'gap':>3} | {'cal lo':>9} {'cal hi':>9}"
      f" {'dec':>6} {'n':>3} {'gap':>3} | brackets 0.5  SEC nb  agree")
R3 = []
for C in CS:
    pr, pc = L.plateau(C["raw_means"], C["tacc"], C["step"]), L.plateau(C["sec_means"], C["tacc_sec"], C["step"])
    br, nb = L.brackets(pc, W), L.arm_nb(C, SEC)
    R3.append((C, pr, pc, br, nb))
    print(f"   {C['study']:5} {C['carrier'][:34]:34} | {pr['lo']:9.4g} {pr['hi']:9.4g} {pr['decades']:6.3f} {len(pr['set']):3d}"
          f" {pr['gaps']:3d} | {pc['lo']:9.4g} {pc['hi']:9.4g} {pc['decades']:6.3f} {len(pc['set']):3d} {pc['gaps']:3d} |"
          f"      {yn(br)}          {yn(nb)}      {yn(br == nb)}")
print("per family (report): bracket == SEC not behind; confusion (bracket, not behind): YY YN NY NN")
for fam in list(L.STUDIES) + ["pooled"]:
    rr = [t for t in R3 if fam == "pooled" or t[0]["study"] == fam]
    cf = [sum(t[3] == b and t[4] == v for t in rr) for b, v in ((1, 1), (1, 0), (0, 1), (0, 0))]
    print(f"   {fam:6} agree {sum(t[3] == t[4] for t in rr)}/{len(rr)};  YY {cf[0]}  YN {cf[1]}  NY {cf[2]}  NN {cf[3]}")
ka, na = sum(t[3] == t[4] for t in R3), len(R3)
f3a = ka / na >= F3A_SHARE
A1R = {(C["study"], C["carrier"]): r for C, r in R1}
print("   disagreeing carriers, with A1's parts in steps (the bracket is read against tacc_sec, not behind against tacc):")
for t in R3:
    if t[3] != t[4]:
        r = A1R[(t[0]["study"], t[0]["carrier"])]
        print(f"      {t[0]['study']:5} {t[0]['carrier'][:34]:34} bracket {yn(t[3])}, SEC nb {yn(t[4])};"
              f" shape gain {r['shape_s']:+.3f}, location cost {r['loc_s']:+.3f}, margin {r['marg_s']:+.3f} steps")
print(f"F3(a) bracket == SEC not behind on {frac(ka, na)} >= {F3A_SHARE} -> {f3a}")
print(f"F3(a): {word(f3a)}")
wr = [t[1]["decades"] for t in R3]; wc = [t[2]["decades"] for t in R3]
mr, mc = float(np.median(wr)), float(np.median(wc))
ratio = mr / mc if mc > 0 else math.inf
f3b = F3B_LO <= ratio <= F3B_HI
print("per family (report): median width in decades, raw | calibrated")
for fam in L.STUDIES:
    rr = [t for t in R3 if t[0]["study"] == fam]
    print(f"   {fam:6} {float(np.median([t[1]['decades'] for t in rr])):.4f} | {float(np.median([t[2]['decades'] for t in rr])):.4f}")
print(f"F3(b) median width over the {na}: raw {mr!r} ({mr:.4f}) decades, calibrated {mc!r} ({mc:.4f}) decades;"
      f" ratio raw / calibrated {ratio!r} ({ratio:.4f}) in [{F3B_LO}, {F3B_HI}] -> {f3b}")
print(f"F3(b): {word(f3b)}")

print("\nA3 report (not a forecast): the clipped SEC's not-behind label against the same bracket, SEC4 and SEC5")
rc = [(t, L.arm_nb(t[0], CLIP)) for t in R3 if CLIP in t[0]["primary"]]
for t, nbc in rc:
    print(f"   {t[0]['study']:5} {t[0]['carrier'][:34]:34} brackets 0.5 {yn(t[3])}  clipped SEC nb {yn(nbc)}  agree {yn(t[3] == nbc)}")
print(f"   agree {sum(t[3] == nbc for t, nbc in rc)}/{len(rc)}")

# -------------------------------------------------------------------------------------------------------------- summary
print(); print(BAR)
print("summary (words computed above)")
print(f"   F1    {word(f1i and f1ii)}   (i) {k1}/{n1} location cost > -step where SEC not behind (>= {F1_SHARE});"
      f" (ii) {k2}/{n2} shape gain > step (< {n2 / 2:g})")
print(f"   F2    {word(all(ok for *_, ok in f2))}   " + "; ".join(f"{fam} {sds / sdr:.3f}" for fam, sdr, sds, _ in f2)
      + f" (SD_sec / SD_raw, each <= {F2_RATIO})")
print(f"   F3(a) {word(f3a)}   {ka}/{na} bracket == SEC not behind (>= {F3A_SHARE})")
print(f"   F3(b) {word(f3b)}   median width raw {mr:.4f} / calibrated {mc:.4f} = {ratio:.4f} (in [{F3B_LO}, {F3B_HI}])")
