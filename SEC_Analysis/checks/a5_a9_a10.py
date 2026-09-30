"""SEC_Analysis A5, A9 and A10, with forecasts F5, F9 and F10 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; Amendment 1
at 347cb90; prompt-log entry 257): what kind of failure each "behind" is, why SEC4 passed and SEC5 did not carrier by carrier,
and how much of the pass count is tolerance; with Amendment 1's report of F5, F9 and F10 with the floor-bound carriers removed.

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads the pinned run records through sec_lib.load_all()
(validated first: loader_check.txt, every pinned count REPRODUCED) over the 42 scored carriers of SEC1, SCL3, SEC3, SEC4 and
SEC5, and nothing else: it opens no data and trains nothing. SEC is the unclipped 'bayes_sec' (all 42 carriers); the clipped
SEC is 'bayes_sec_clip' at kappa 0.5 (SEC4 and SEC5, 14 carriers). Tuned lambda, step, not behind, the plateau and divergence
are sec_lib's primitives, never re-derived here. step = the carrier's step at lambda*_raw (C["step"]) in every unit and on
both axes, as in a1_a3.py's A3.

  behind       an arm's seed mean a with a - tacc <= -step (sec_lib.not_behind false), tacc the tuned raw arm's seed mean.
  A5           every behind case of SEC (of 42) and of the clipped SEC (of 14) gets the FIRST class in the declared order
               D, C, U, O, N whose condition holds, else X (unclassified, printed with its numbers). With P the calibrated
               not-behind set (sec_lib.plateau of the 'fixed_sec' grid means against tacc_sec with the step above):
                 D  diverged: sec_lib.arm_diverged(C, arm), i.e. a seed below 0.5 x tacc, a non-finite accuracy or a non-finite
                    record;
                 C  (clipped arm only) the declared phrase is "the clip fired and lambda*_sec lies above the not-behind set's
                    reach at 1/2". The script's reading: the clip fired on at least one seed (guard_fired > 0) AND P lies
                    wholly above 0.5 (P's lowest grid point > 0.5), so the set does not reach 1/2 and lambda*_sec (in P) is
                    above it. The phrase names no computation: another reading, "reach at 1/2" as the top of the gap-free run of
                    P whose span contains 1/2 (1/2 itself where no run contains it), is printed as a REPORT with the class it
                    would give and the number of cases where the two readings differ;
                 U  P lies wholly above 0.5 (lowest point > 0.5);
                 O  P lies wholly below 0.5 (highest point < 0.5);
                 N  behind by less than 2 steps (margin in steps > -2) AND P brackets 0.5 (lowest <= 0.5 <= highest).
               Every condition is printed for every case beside the class, so the effect of the order is visible.
               F5 HOLDS iff (i) D is the most common class among the unclipped failures with a share > 0.5 AND (ii) every
               clipped failure is C, U or N (the declaration's text; it implies none is D). The reduced reading of (ii),
               "no clipped failure is D", is printed beside it.
  A9           the 14 carriers of SEC4 and SEC5 side by side: margins of the clipped and unclipped SEC in steps; A1's shape gain
               (tacc_sec - tacc) and location costs (arm - tacc_sec) in steps; the A5 class of each arm ('nb' where not
               behind); s geometric mean and max over tasks and seeds of each arm (sec_lib.s_stats); the clip's firings per seed
               and largest guard margin; d, K, tasks, n_train, per-task n, imbalance; per-seed accuracies of the tuned raw
               lambda, the clipped SEC and the unclipped SEC.
               Also each carrier's accuracy floor and floor-bound flag (Amendment 1, A12's definition; see below), so a tuned
               lambda sitting at the majority-class floor (volcanoes-d4) is visible beside its failure.
               F9 HOLDS iff, over SEC5's clipped failures: (a) at least 2 distinct classes among D, C, U, O, N (X not counted;
               the count with X is printed beside it) AND (b) at least one is C AND (c) at least one failure carrier's tuned
               arm has a low-accuracy seed. The declared text of (c) is "at least one is not caused by the penalty
               (pokerhand's low-accuracy seeds, visible in the tuned arm too)". Two choices here are the SCRIPT'S
               OPERATIONALISATION, not declared: "low-accuracy seed" is read with A5 D's declared line (a seed below 0.5 x
               tacc, or a non-finite record: sec_lib.diverged with the arm's finite flags), and "the tuned arm" is read as the
               tuned lambda*_raw's own five seeds (sec1_score.run names that arm tv). The other reading of "the tuned arm", the
               'fixed' mode at any raw-grid lambda (sec1_score's "tuned-lambda baseline"), is printed beside it with the word
               F9 would take under it, and whether (b) alone decides F9's word. The tuned seeds' spread (max - min, in steps)
               is printed as a report column only; no threshold is put on it. The carriers the declaration names
               (volcanoes-d4 as C; pokerhand's seeds in the tuned arm) are printed as a report beside the rule.
  A10          every carrier's margin SEC - tacc in points (full precision) and steps; among the carriers where SEC is not
               behind, the share with a negative margin (SEC - tacc < 0, strict), per family (= study) and pooled over the 30
               held-out carriers (SCL3, SEC3, SEC4, SEC5). F10 HOLDS iff that pooled share >= 0.25.
  A12 report   Amendment 1 (347cb90; POST HOC in origin): "Every forecast F1-F11 whose decisive count includes floor-bound
               carriers is also printed with them removed, as a report." floor = 100 x the majority class's share of the
               loaded rows (the header's class_counts; the same definition and code as a1_a3.py's Amendment 1 report);
               floor-bound iff tacc - floor < 3 steps. F5 (i) and (ii), F9 (a)-(c) and F10 are reprinted over the carriers that
               are not floor-bound; a condition left with no case is printed as vacuous. These words are reports; the declared
               words are those on all carriers. A12's own analysis and F12 are not computed here.
Lines marked REPORT are not declared; they decide nothing: the cases where more than one A5 condition holds (so the order
decides); C under the other reading of its declared phrase; the A5 conditions (Y/N only, no class) on SEC5's other clip cells
(kappa 0.25 and 1.0), which enter neither F5 nor F9; the raw- and calibrated-grid points with a seed below 0.5 tacc on SEC5's
clipped-failure carriers; all 42 pooled for A10; the clipped SEC's A10 share on SEC4 and SEC5.
Accuracies are the frozen scorers' (per cent; a non-finite run is recorded as 0). The words HOLDS and FAILS are computed here
from the printed numbers.

    uv run python SEC_Analysis/checks/a5_a9_a10.py > SEC_Analysis/checks/a5_a9_a10.txt
"""
from __future__ import annotations

import os
import sys
from collections import Counter

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sec_lib as L  # noqa: E402

D = L.load_all(); BY = L.by_study(D); CS = list(D.values()); N = len(CS)
SEC, CLIP, W0 = "bayes_sec", "bayes_sec_clip", 0.5
ORDER = ("D", "C", "U", "O", "N")                                      # DECLARATION.md A5, in order
N_STEPS = 2.0                                                          # A5 class N: behind by less than 2 steps
F5_SHARE = 0.5; F5_ALLOWED = ("C", "U", "N")                           # F5
F9_CLASSES = 2                                                         # F9 (a): distinct classes
F10_SHARE = 0.25; HELD = ("scl3", "sec3", "sec4", "sec5")              # F10: the 30 held-out carriers
FLOOR_STEPS = 3.0                                                      # Amendment 1 (A12): floor-bound iff tacc - floor < 3 steps
BAR = "=" * 150


def hdr(t):
    print("\n" + BAR); print(t); print(BAR)


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "Y" if b else "N"


def frac(k, n):
    return f"{k}/{n} = {k / n!r} ({k / n:.3f})" if n else f"{k}/0 (undefined)"


def seeds(a):
    return "[" + " ".join(f"{x:6.2f}" for x in a) + "]"


def reach(C, p, x=W0):
    """REPORT reading of C's "the not-behind set's reach at 1/2": the top of the gap-free run of P (consecutive calibrated
    grid points, all in P) whose span contains x; x itself where no run contains it."""
    S, runs, cur = set(p["set"]), [], []
    for w in sorted(C["sec_means"]):
        if w in S:
            cur.append(w)
        elif cur:
            runs.append(cur); cur = []
    runs += [cur] if cur else []
    return next((r[-1] for r in runs if r[0] <= x <= r[-1]), x)


def conds(C, A, mode, fired):
    """A5's five conditions for arm A (mode) on carrier C; C by the script's reading, C_reach by the REPORT reading."""
    p = L.plateau(C["sec_means"], C["tacc_sec"], C["step"]); ms = L.margin_steps(C, A.mean)
    above, below = p["lo"] > W0, p["hi"] < W0; rc = reach(C, p)
    c = dict(D=L.diverged(A.acc, C["tacc"], A.finite), C=mode == CLIP and fired > 0 and above, U=above, O=below,
             N=ms > -N_STEPS and L.brackets(p, W0))
    return p, ms, c, rc, mode == CLIP and fired > 0 and C["tuned_sec"] > rc


def a5(C, mode):
    """A5's conditions and class for one arm on one carrier (called only where the arm is behind)."""
    A = C["primary"][mode]
    fired = L.guard_stats(A)["fired"] if mode == CLIP else None
    p, ms, c, rc, c_reach = conds(C, A, mode, fired)
    assert c["D"] == L.arm_diverged(C, mode)
    cr = dict(c, C=c_reach)
    return dict(C=C, mode=mode, A=A, p=p, ms=ms, fired=fired, c=c, cls=next((k for k in ORDER if c[k]), "X"),
                reach=rc, c_reach=c_reach, cls_reach=next((k for k in ORDER if cr[k]), "X"),
                div_acc=L.diverged(A.acc, C["tacc"]), minr=float(A.acc.min() / C["tacc"]),
                nonfin=sum(not f for f in A.finite) + int(np.sum(~np.isfinite(A.acc))))


def tuned_low(C):
    """F9 (c), the script's operationalisation: A5 D's line on the tuned lambda*_raw's own seeds; and, the other reading of
    "the tuned arm", the raw-grid lambdas whose seeds cross the same line. The spread is a report column only."""
    a = C["tv"].acc; spread = float(a.max() - a.min())
    grid = [w for w, g in C["raw"].items() if L.diverged(g.acc, C["tacc"], g.finite)]
    return dict(low=L.diverged(a, C["tacc"], C["tv"].finite), spread=spread, spread_s=spread / C["step"], grid=grid,
                nonfin=sum(not f for f in C["tv"].finite))


def floor_of(C):
    """Amendment 1 (A12): 100 x the majority class's share of the loaded rows (as a1_a3.py's floor_of)."""
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * max(cc) / sum(cc)


FLOOR = {(C["study"], C["carrier"]): floor_of(C) for C in CS}
FB = {k: D[k]["tacc"] - FLOOR[k] < FLOOR_STEPS * D[k]["step"] for k in D}


def fb(C):
    return FB[(C["study"], C["carrier"])]


assert [(C["study"], C["carrier"]) for C in CS if CLIP in C["primary"]] == \
       [(C["study"], C["carrier"]) for C in CS if C["study"] in ("sec4", "sec5")], "clipped SEC on SEC4 and SEC5 only"

print(BAR)
print("SEC_Analysis A5, A9, A10 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; Amendment 1 at 347cb90; prompt-log entry 257):"
      " forecasts F5, F9, F10")
print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecasts, never PASS")
print(BAR)
print(f"carriers: {N} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); SEC '{SEC}' on all {N};"
      f" clipped SEC '{CLIP}' (kappa 0.5) on {sum(CLIP in C['primary'] for C in CS)} (SEC4 and SEC5)")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); behind = arm - tacc <= -step; points are per cent accuracy")

# ============================================================================================================== A5
hdr("A5  what kind of failure is each 'behind'?  first of D, C, U, O, N whose condition holds, else X (unclassified)")
print("   P = the calibrated not-behind set (fixed_sec grid points with mean > tacc_sec - step); lo, hi its lowest and highest grid point")
print("   D: a seed < 0.5 tacc or non-finite | C (clipped only): fired > 0 AND lo > 0.5 (the script's reading of the declared"
      " phrase, see the REPORT below) | U: lo > 0.5 | O: hi < 0.5 | N: margin > -2 steps AND lo <= 0.5 <= hi")
print(f"   {'study':5} {'carrier':34} {'arm':5} {'mean':>8} {'tacc':>8} {'step':>6} {'margin st':>9} {'min/tacc':>8} {'nonfin':>6}"
      f" {'fired':>5} {'SEC nb':>6} {'P lo':>9} {'P hi':>9} |  D  C  U  O  N | class")
CASES = [a5(C, SEC) for C in CS if not L.arm_nb(C, SEC)] + [a5(C, CLIP) for C in CS if CLIP in C["primary"] and not L.arm_nb(C, CLIP)]
for r in CASES:
    C = r["C"]; c = r["c"]
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {'SEC' if r['mode'] == SEC else 'clip':5} {r['A'].mean:8.4f} {C['tacc']:8.4f}"
          f" {C['step']:6.3f} {r['ms']:+9.3f} {r['minr']:8.3f} {r['nonfin']:6d} {'-' if r['fired'] is None else r['fired']:>5}"
          f" {yn(L.arm_nb(C, SEC)):>6} {r['p']['lo']:9.4g} {r['p']['hi']:9.4g} |  " + "  ".join(yn(c[k]) for k in ORDER)
          + f" | {r['cls']}")
assert all(r["c"]["D"] == r["div_acc"] for r in CASES)
print(f"   D under the accuracy-only rule (sec_lib.diverged with finite=None, SEC4-2/SEC5-2's) agrees with the rule above on"
      f" {sum(r['c']['D'] == r['div_acc'] for r in CASES)}/{len(CASES)} cases")
for r in CASES:
    if r["cls"] == "X":
        C = r["C"]
        print(f"   X: {C['study']}/{C['carrier']} ({'SEC' if r['mode'] == SEC else 'clipped SEC'}): margin {r['ms']!r} steps"
              f" (not > -{N_STEPS:g}), P [{r['p']['lo']:g}, {r['p']['hi']:g}] brackets 0.5 {yn(L.brackets(r['p'], W0))},"
              f" lowest seed / tacc {r['minr']:.4f} (not < {L.DIV_FRAC}); seeds {seeds(r['A'].acc)}, tacc {C['tacc']:.4f}")
multi = [r for r in CASES if sum(r["c"].values()) > 1]
print("REPORT: cases where more than one condition holds (the order decides the class):")
for r in multi:
    print(f"   {r['C']['study']:5} {r['C']['carrier'][:34]:34} {'SEC' if r['mode'] == SEC else 'clip':5} conditions"
          f" {''.join(k for k in ORDER if r['c'][k])} -> {r['cls']}")
print("REPORT: class C's declared phrase, \"the clip fired and lambda*_sec lies above the not-behind set's reach at 1/2\", names no"
      " computation (an ambiguity of the declaration).")
print("   script's reading: fired > 0 AND lo > 0.5. Other reading: fired > 0 AND lambda*_sec > reach, reach = the top of the gap-free"
      " run of P whose span contains 0.5 (0.5 where none does). Every clipped failure:")
print(f"   {'study':5} {'carrier':22} {'fired':>5} {'lam*_sec':>9} {'P lo':>9} {'reach':>9} | C script C reach | class script  class reach")
for r in CASES:
    if r["mode"] == CLIP:
        print(f"   {r['C']['study']:5} {r['C']['carrier'][:22]:22} {r['fired']:5d} {r['C']['tuned_sec']:9.4g} {r['p']['lo']:9.4g}"
              f" {r['reach']:9.4g} | {yn(r['c']['C']):>8} {yn(r['c_reach']):>7} | {r['cls']:>12} {r['cls_reach']:>12}")
ndiff = sum(r["cls"] != r["cls_reach"] for r in CASES if r["mode"] == CLIP)
print(f"   clipped failures whose class differs between the two readings: {ndiff} of {sum(r['mode'] == CLIP for r in CASES)};"
      f" C differs on {sum(r['c']['C'] != r['c_reach'] for r in CASES if r['mode'] == CLIP)}")

UNC = [r for r in CASES if r["mode"] == SEC]; CLP = [r for r in CASES if r["mode"] == CLIP]
KEYS = list(ORDER) + ["X"]


def tally(rs):
    t = Counter(r["cls"] for r in rs); return " ".join(f"{k} {t.get(k, 0)}" for k in KEYS)


print("\nclass counts per family (unclipped SEC failures | clipped SEC failures):")
for s in L.STUDIES:
    u = [r for r in UNC if r["C"]["study"] == s]; k = [r for r in CLP if r["C"]["study"] == s]
    print(f"   {s:6} SEC behind {len(u):2d} of {len(BY[s]):2d}: {tally(u)}   |   clipped behind "
          + (f"{len(k)} of {len(BY[s])}: {tally(k)}" if s in ("sec4", "sec5") else "-  (no clipped arm)"))
print(f"   pooled SEC behind {len(UNC)} of {N}: {tally(UNC)}   |   clipped behind {len(CLP)} of 14: {tally(CLP)}")

tu = Counter(r["cls"] for r in UNC); top = max(tu.values()); modes = [k for k in KEYS if tu.get(k, 0) == top]
kD, nU = tu.get("D", 0), len(UNC)
f5i = modes == ["D"] and kD / nU > F5_SHARE
clp_cls = [r["cls"] for r in CLP]
f5ii = all(c in F5_ALLOWED for c in clp_cls); f5ii_red = "D" not in clp_cls
print(f"F5 (i)  most common class among the {nU} unclipped failures: {'/'.join(modes)} ({top}); D share {frac(kD, nU)} > {F5_SHARE}"
      f" -> {f5i}")
print(f"F5 (ii) every clipped failure is C, U or N: classes {clp_cls} ("
      + ", ".join(f"{r['C']['carrier']} {r['cls']}" for r in CLP) + f") -> {f5ii}")
print(f"        reduced reading, no clipped failure is D: D on {clp_cls.count('D')} of {len(clp_cls)} -> {f5ii_red}"
      f" (agrees with (ii): {f5ii == f5ii_red})")
print(f"F5: {word(f5i and f5ii)}")

print("\nREPORT: the clipped arm's other kappa cells at the primary window (SEC5; not declared): the A5 conditions on each behind"
      " cell's seed mean, Y/N only; no class is assigned")
print(f"   {'carrier':22} {'kappa':>5} {'mean':>8} {'margin st':>9} {'fired/seed':>15} {'nb':>2} |  D  C  U  O  N | C reach")
KCELLS = []
for C in BY["sec5"]:
    for (v, fs, fe), A in sorted(C["cells"].get(CLIP, {}).items()):
        if fs != L.FS or fe != L.FE:
            continue
        KCELLS.append(A)
        ms = L.margin_steps(C, A.mean); nb = L.not_behind(A.mean, C["tacc"], C["step"]); g = L.guard_stats(A)
        head = f"   {C['carrier'][:22]:22} {v:5g} {A.mean:8.4f} {ms:+9.3f} {str(g['per_seed_fired']):>15} {yn(nb):>2} | "
        if nb:
            print(head + " -  -  -  -  - | -")
            continue
        _, _, c, _, c_reach = conds(C, A, CLIP, g["fired"])
        print(head + " " + "  ".join(yn(c[k]) for k in ORDER) + f" | {yn(c_reach)}")
print(f"   cells read: {len(KCELLS)}; of them among F5's cases {sum(any(A is r['A'] for r in CASES) for A in KCELLS)}, among F9's"
      f" {sum(any(A is r['A'] for r in CASES if r['C']['study'] == 'sec5' and r['mode'] == CLIP) for A in KCELLS)}:"
      " these cells enter neither F5 nor F9")

# ============================================================================================================== A9
hdr("A9  why SEC4 passed and SEC5 did not, carrier by carrier (the 14 carriers of SEC4 and SEC5)")
CL5 = {(r["C"]["study"], r["C"]["carrier"], r["mode"]): r["cls"] for r in CASES}
R9 = []
for C in BY["sec4"] + BY["sec5"]:
    k = (C["study"], C["carrier"]); As, Ac = C["primary"][SEC], C["primary"][CLIP]
    ss, sc, g = L.s_stats(As), L.s_stats(Ac), L.guard_stats(Ac)
    R9.append(dict(C=C, ms_c=L.margin_steps(C, Ac.mean), ms_s=L.margin_steps(C, As.mean), shape=(C["tacc_sec"] - C["tacc"]) / C["step"],
                   loc_c=(Ac.mean - C["tacc_sec"]) / C["step"], loc_s=(As.mean - C["tacc_sec"]) / C["step"],
                   cls_c=CL5.get(k + (CLIP,), "nb"), cls_s=CL5.get(k + (SEC,), "nb"), ss=ss, sc=sc, g=g, tn=tuned_low(C)))
print("   margins, A1's parts and location costs in steps; class = A5 ('nb' = not behind); s over tasks and seeds of each arm;"
      " fired = the clip's firings per seed; max m = largest guard margin (fires at >= 0.5)")
print(f"   {'study':5} {'carrier':22} {'clip st':>8} {'SEC st':>8} {'shape st':>8} {'loc clip':>8} {'loc SEC':>8} {'cls clip':>8}"
      f" {'cls SEC':>7} {'s gm SEC':>10} {'s max SEC':>10} {'s gm clip':>10} {'s max clip':>10} {'fired/seed':>15} {'max m':>7}")
for r in R9:
    C = r["C"]
    print(f"   {C['study']:5} {C['carrier'][:22]:22} {r['ms_c']:+8.3f} {r['ms_s']:+8.3f} {r['shape']:+8.3f} {r['loc_c']:+8.3f}"
          f" {r['loc_s']:+8.3f} {r['cls_c']:>8} {r['cls_s']:>7} {r['ss']['gmean']:10.4g} {r['ss']['max']:10.4g} {r['sc']['gmean']:10.4g}"
          f" {r['sc']['max']:10.4g} {str(r['g']['per_seed_fired']):>15} {r['g']['max_margin']:7.4f}")
print("\n   properties (header) and the tuned raw arm's seeds: nonfin = its non-finite records; low = a tuned seed < 0.5 tacc or a"
      " non-finite record (A5 D's line); spread = max - min of the tuned seeds, in points and steps (report column, no threshold);"
      " floor = 100 x majority share; fb = floor-bound (A12: tacc - floor < 3 steps)")
print(f"   {'study':5} {'carrier':22} {'d':>4} {'K':>3} {'tasks':>5} {'n_train':>7} {'imbal':>7} {'per-task n':28} {'lam*_raw':>9}"
      f" {'tacc':>8} {'step':>6} {'nonfin':>6} {'low':>3} {'spread':>7} {'st':>6} {'floor':>8} {'(t-fl)/st':>9} {'fb':>2}")
for r in R9:
    C = r["C"]; t = r["tn"]; fl = FLOOR[(C["study"], C["carrier"])]
    print(f"   {C['study']:5} {C['carrier'][:22]:22} {C['d']:4d} {C['K']:3d} {C['n_tasks']:5d} {C['n_train']:7d} {C['imbalance']:7.2f}"
          f" {str(C['per_task_n']):28} {C['tuned']:9.4g} {C['tacc']:8.4f} {C['step']:6.3f} {t['nonfin']:6d} {yn(t['low']):>3} {t['spread']:7.3f}"
          f" {t['spread_s']:6.3f} {fl:8.4f} {(C['tacc'] - fl) / C['step']:+9.3f} {yn(fb(C)):>2}")
print("\n   per-seed accuracies (seeds 0-4): the tuned raw lambda, the clipped SEC, the unclipped SEC; 0.5 tacc = the divergence line")
print(f"   {'study':5} {'carrier':22} {'0.5 tacc':>8}  {'tuned raw lambda':36}  {'clipped SEC':36}  unclipped SEC")
for r in R9:
    C = r["C"]
    print(f"   {C['study']:5} {C['carrier'][:22]:22} {L.DIV_FRAC * C['tacc']:8.4f}  {seeds(C['tv'].acc):36}  {seeds(C['primary'][CLIP].acc):36}"
          f"  {seeds(C['primary'][SEC].acc):36}")
print("\nper family (report): clipped SEC not behind | unclipped SEC not behind | clip fired on a carrier | median s max (SEC)"
      " | tuned lambda has a low seed | floor-bound")
for s in ("sec4", "sec5"):
    rr = [r for r in R9 if r["C"]["study"] == s]
    print(f"   {s:5} {sum(r['cls_c'] == 'nb' for r in rr)}/{len(rr)} | {sum(r['cls_s'] == 'nb' for r in rr)}/{len(rr)} |"
          f" {sum(r['g']['fired'] > 0 for r in rr)}/{len(rr)} | {float(np.median([r['ss']['max'] for r in rr])):.4g} |"
          f" {sum(r['tn']['low'] for r in rr)}/{len(rr)} | {sum(fb(r['C']) for r in rr)}/{len(rr)}")

F9R = [r for r in R9 if r["C"]["study"] == "sec5" and r["cls_c"] != "nb"]


def f9_eval(rs):
    cls = [r["cls_c"] for r in rs]; dist = sorted(set(cls) - {"X"}, key=KEYS.index)
    low = [r["C"]["carrier"] for r in rs if r["tn"]["low"]]; grid = [r["C"]["carrier"] for r in rs if r["tn"]["grid"]]
    return dict(cls=cls, dist=dist, dist_x=sorted(set(cls), key=KEYS.index), a=len(dist) >= F9_CLASSES, b="C" in cls,
                low=low, c=bool(low), grid=grid, c2=bool(grid))


F9 = f9_eval(F9R); cls9, dist = F9["cls"], F9["dist"]; f9a, f9b, f9c, f9c2 = F9["a"], F9["b"], F9["c"], F9["c2"]
f9 = f9a and f9b and f9c; f9_2 = f9a and f9b and f9c2
print(f"\nF9  SEC5's clipped failures: {len(F9R)} (" + ", ".join(f"{r['C']['carrier']} {r['cls_c']}" for r in F9R) + ")")
print(f"F9 (a) distinct classes among D, C, U, O, N: {len(dist)} {dist} >= {F9_CLASSES} -> {f9a}   (with X counted:"
      f" {len(F9['dist_x'])} {F9['dist_x']})")
print(f"F9 (b) at least one is C: C on {cls9.count('C')} of {len(cls9)} -> {f9b}")
print(f"F9 (c) declared: \"at least one is not caused by the penalty (pokerhand's low-accuracy seeds, visible in the tuned arm too)\"")
print(f"       script's operationalisation (not declared): a failure carrier whose tuned lambda*_raw has a seed < {L.DIV_FRAC} x tacc"
      " or a non-finite record (A5 D's line on the tuned arm's own seeds)")
for r in F9R:
    C = r["C"]; t = r["tn"]
    print(f"       {C['carrier'][:22]:22} tuned seeds {seeds(C['tv'].acc)}; lowest {float(C['tv'].acc.min())!r} vs 0.5 tacc"
          f" {L.DIV_FRAC * C['tacc']!r}; non-finite {t['nonfin']} -> low {yn(t['low'])}   (report: spread {t['spread']!r} ="
          f" {t['spread_s']:.4f} steps)")
print(f"       low on {len(F9['low'])} of {len(F9R)} -> {f9c}")
print("       other reading of \"the tuned arm\": the 'fixed' mode at any raw-grid lambda (sec1_score's \"tuned-lambda baseline\");"
      " a carrier counts if any raw-grid lambda crosses the same line (counts in the REPORT below)")
print(f"       low on {len(F9['grid'])} of {len(F9R)} ({', '.join(F9['grid']) or 'none'}) -> {f9c2}")
print(f"       F9 under that reading: {word(f9_2)}; the word is the same under both readings: {word(f9) == word(f9_2)}"
      + ("; (b) is False, so F9 FAILS whatever (c) reads" if not f9b else ""))
print("REPORT (decides nothing): on each SEC5 clipped-failure carrier, the grid points (primary window) where a seed is"
      " below 0.5 tacc or a record is non-finite, on the raw ('fixed') and calibrated ('fixed_sec') axes; * marks the tuned lambda")
for r in F9R:
    C = r["C"]
    for ax, g, t in (("raw", C["raw"], C["tuned"]), ("cal", C["sec"], C["tuned_sec"])):
        low = [w for w, a in g.items() if L.diverged(a.acc, C["tacc"], a.finite)]
        print(f"       {C['carrier'][:22]:22} {ax} {len(low):2d} of {len(g)}: "
              + (" ".join(f"{w:g}" + ("*" if w == t else "") for w in low) or "none"))
print("REPORT: the carriers the declaration names: " + "; ".join(
    f"{r['C']['carrier']} clipped class {r['cls_c']} (A5 conditions {''.join(k for k in ORDER if c5['c'][k]) or 'none'}),"
    f" tuned lambda low {yn(r['tn']['low'])}, raw-grid lambdas low {len(r['tn']['grid'])}, floor-bound {yn(fb(r['C']))}"
    f" (tacc - floor {r['C']['tacc'] - FLOOR[(r['C']['study'], r['C']['carrier'])]:+.4f} points)"
    for r in F9R if r["C"]["carrier"] in ("volcanoes-d4", "pokerhand")
    for c5 in [x for x in CASES if x["mode"] == CLIP and x["C"] is r["C"]]))
print(f"F9: {word(f9)}")

# ============================================================================================================== A10
hdr("A10  how much of the pass count is tolerance?  margin = SEC - tacc (unclipped SEC), in points (full precision) and steps")
R10 = []
print(f"   {'study':5} {'carrier':34} {'SEC':>8} {'tacc':>8} {'step':>6} {'margin (full precision)':>24} {'steps':>8}  nb  negative")
for C in CS:
    a = C["primary"][SEC].mean; m = L.margin(C, a); ms = L.margin_steps(C, a); nb = L.arm_nb(C, SEC)
    R10.append(dict(C=C, m=m, ms=ms, nb=nb, neg=m < 0))
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {a:8.4f} {C['tacc']:8.4f} {C['step']:6.3f} {m!r:>24} {ms:+8.3f}   {yn(nb)}  {yn(m < 0)}")
print(f"   margins exactly 0: {sum(r['m'] == 0 for r in R10)} of {N}")


def share(rs):
    nb = [r for r in rs if r["nb"]]; return sum(r["neg"] for r in nb), len(nb)


print("\nper family: carriers, SEC not behind, of those with a negative margin (share), passes at zero tolerance (margin >= 0)")
for s in L.STUDIES:
    rr = [r for r in R10 if r["C"]["study"] == s]; k, n = share(rr)
    print(f"   {s:6} {len(rr):3d} carriers; not behind {n:2d}; negative margin {frac(k, n)}; margin >= 0 on {sum(r['m'] >= 0 for r in rr)}")
H = [r for r in R10 if r["C"]["study"] in HELD]; kH, nH = share(H); kA, nA = share(R10)
print(f"   held-out pooled ({'+'.join(HELD)}) {len(H)} carriers; not behind {nH}; negative margin {frac(kH, nH)};"
      f" margin >= 0 on {sum(r['m'] >= 0 for r in H)}")
print(f"   REPORT all 42 pooled; not behind {nA}; negative margin {frac(kA, nA)}; margin >= 0 on {sum(r['m'] >= 0 for r in R10)}")
nbH = [r["ms"] for r in H if r["nb"]]
bins = ((-1.0, -0.5), (-0.5, 0.0), (0.0, 1.0), (1.0, np.inf))
print("   REPORT held-out passes by margin in steps: " + "; ".join(
    f"[{lo:+g}, {hi:+g}) {sum(lo <= x < hi for x in nbH)}" for lo, hi in bins) + f"  (all {len(nbH)} > -1 by not behind)")
print("REPORT: the clipped SEC on SEC4 and SEC5 (not declared): not behind, of those with a negative margin")
for s in ("sec4", "sec5"):
    rr = [(C, L.margin(C, C["primary"][CLIP].mean)) for C in BY[s]]; nb = [m for C, m in rr if L.arm_nb(C, CLIP)]
    print(f"   {s:6} not behind {len(nb)} of {len(rr)}; negative margin {frac(sum(m < 0 for m in nb), len(nb))}")
f10 = nH > 0 and kH / nH >= F10_SHARE
print(f"F10 negative margin among the {nH} held-out passes: {frac(kH, nH)} >= {F10_SHARE} -> {f10}")
print(f"F10: {word(f10)}")

# ============================================================================================ Amendment 1 (A12) report
hdr("Amendment 1 report (POST HOC in origin; 347cb90): F5, F9 and F10 with the floor-bound carriers removed")
print(f"   floor = 100 x the majority class's share of the loaded rows (header class_counts); floor-bound iff tacc - floor <"
      f" {FLOOR_STEPS:g} steps (the definition of a1_a3.py's Amendment 1 report)")
print(f"   {'study':5} {'carrier':34} {'floor':>8} {'tacc':>8} {'step':>6} {'(tacc-floor)/step':>18}  floor-bound")
for C in CS:
    fl = FLOOR[(C["study"], C["carrier"])]
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {fl:8.4f} {C['tacc']:8.4f} {C['step']:6.3f} {(C['tacc'] - fl) / C['step']:+18.3f}"
          f"  {yn(fb(C))}")
print("   floor-bound per study: " + "; ".join(f"{s} {sum(fb(C) for C in BY[s])}/{len(BY[s])}" for s in L.STUDIES)
      + f"; all {sum(FB.values())}/{N}")


def vac(n):
    return " (vacuous: no case left)" if n == 0 else ""


UK = [r for r in UNC if not fb(r["C"])]; CK = [r for r in CLP if not fb(r["C"])]
print(f"   F5's cases floor-bound: unclipped failures {len(UNC) - len(UK)} of {len(UNC)}, clipped failures {len(CLP) - len(CK)} of"
      f" {len(CLP)}")
tk = Counter(r["cls"] for r in UK); topk = max(tk.values()) if tk else 0; modesk = [k for k in KEYS if tk.get(k, 0) == topk and UK]
kDk = tk.get("D", 0)
f5ik = bool(UK) and modesk == ["D"] and kDk / len(UK) > F5_SHARE
clpk = [r["cls"] for r in CK]; f5iik = all(c in F5_ALLOWED for c in clpk)
print(f"   F5 (i)  kept unclipped failures {len(UK)}: {tally(UK)}; most common {'/'.join(modesk) or '-'}; D share {frac(kDk, len(UK))}"
      f" > {F5_SHARE} -> {f5ik}")
print(f"   F5 (ii) kept clipped failures {len(CK)}: {clpk} all in C/U/N -> {f5iik}{vac(len(CK))}")
print(f"   F5 floor-bound removed (report): {word(f5ik and f5iik)}{vac(len(CK)) and ' ((ii) vacuous: no clipped failure left)'}")
F9K = f9_eval([r for r in F9R if not fb(r["C"])]); n9k = len(F9K["cls"])
print(f"   F9's SEC5 clipped failures floor-bound: {len(F9R) - n9k} of {len(F9R)}; kept {n9k}: {F9K['cls']}")
print(f"   F9 (a) {len(F9K['dist'])} distinct {F9K['dist']} >= {F9_CLASSES} -> {F9K['a']}; (b) C on {F9K['cls'].count('C')} -> {F9K['b']};"
      f" (c) tuned lambda low on {len(F9K['low'])} -> {F9K['c']} (any raw-grid lambda: {len(F9K['grid'])} -> {F9K['c2']}){vac(n9k)}")
f9k = F9K["a"] and F9K["b"] and F9K["c"]
print(f"   F9 floor-bound removed (report): {word(f9k)}{vac(n9k)}")
HK = [r for r in H if not fb(r["C"])]; kHk, nHk = share(HK)
print(f"   F10 held-out carriers floor-bound: {len(H) - len(HK)} of {len(H)}; of the {nH} held-out passes {nH - nHk} floor-bound;"
      f" kept passes {nHk} (" + ", ".join(f"{r['C']['carrier']} {'neg' if r['neg'] else 'pos'}" for r in HK if r["nb"]) + ")")
f10k = nHk > 0 and kHk / nHk >= F10_SHARE
print(f"   F10 negative margin among the kept held-out passes: {frac(kHk, nHk)} >= {F10_SHARE} -> {f10k}")
print(f"   F10 floor-bound removed (report): {word(f10k)}{vac(nHk)}")

# ============================================================================================================== summary
print(); print(BAR)
print("summary (words computed above; the words for the declared forecasts are those on all carriers)")
print(f"   F5   {word(f5i and f5ii)}   (i) D {kD}/{nU} unclipped failures ({kD / nU:.3f} > {F5_SHARE}; most common {'/'.join(modes)}) -> {f5i};"
      f" (ii) clipped failures {clp_cls} all in C/U/N -> {f5ii} (none D -> {f5ii_red})")
print(f"   F9   {word(f9)}   SEC5 clipped failures {len(F9R)}: (a) {len(dist)} distinct classes {dist} -> {f9a};"
      f" (b) C on {cls9.count('C')} -> {f9b}; (c) tuned lambda low on {len(F9['low'])} -> {f9c}"
      f" [script's operationalisation; any raw-grid lambda: {len(F9['grid'])} -> {f9c2}, word {word(f9_2)}]")
print(f"   F10  {word(f10)}   {kH}/{nH} held-out passes with a negative margin ({kH / nH:.3f} >= {F10_SHARE})")
print(f"   floor-bound removed (Amendment 1 report, post hoc): F5 {word(f5ik and f5iik)}{vac(len(CK)) and ' ((ii) vacuous)'},"
      f" F9 {word(f9k)}{vac(n9k)}, F10 {word(f10k)} ({kHk}/{nHk})")
