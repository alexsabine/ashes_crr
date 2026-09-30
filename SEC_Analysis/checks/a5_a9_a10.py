"""SEC_Analysis A5, A9 and A10, with forecasts F5, F9 and F10 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log
entry 257): what kind of failure each "behind" is, why SEC4 passed and SEC5 did not carrier by carrier, and how much of the
pass count is tolerance.

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
                 C  (clipped arm only) the clip fired on at least one seed (guard_fired > 0) AND (the unclipped SEC is not
                    behind on that carrier OR P lies wholly above 0.5, i.e. P's lowest grid point > 0.5);
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
               A tuned arm is NOISY iff one of its seeds is below 0.5 x tacc, or its seed spread (max - min) exceeds 4 steps:
               a low-accuracy seed the tuned lambda shows too is not caused by the calibrated penalty.
               F9 HOLDS iff, over SEC5's clipped failures: (a) at least 2 distinct classes among D, C, U, O, N (X not counted;
               the count with X is printed beside it) AND (b) at least one is C AND (c) at least one failure carrier's tuned arm
               is NOISY. The carriers the declaration names (volcanoes-d4 as C; pokerhand's seeds in the tuned arm) are
               printed as a report beside the rule.
  A10          every carrier's margin SEC - tacc in points (full precision) and steps; among the carriers where SEC is not
               behind, the share with a negative margin (SEC - tacc < 0, strict), per family (= study) and pooled over the 30
               held-out carriers (SCL3, SEC3, SEC4, SEC5). F10 HOLDS iff that pooled share >= 0.25.
Lines marked REPORT are not declared; they decide nothing: the cases where more than one A5 condition holds (so the order
decides); the same A5 rule read on SEC5's other clip cells (kappa 0.25 and 1.0); the raw- and calibrated-grid points with a seed
below 0.5 tacc on SEC5's clipped-failure carriers; all 42 pooled for A10; the clipped SEC's A10 share on SEC4 and SEC5.
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
F9_CLASSES = 2; F9_SPREAD = 4.0                                        # F9: distinct classes; tuned-arm spread in steps
F10_SHARE = 0.25; HELD = ("scl3", "sec3", "sec4", "sec5")              # F10: the 30 held-out carriers
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


def a5(C, mode):
    """A5's conditions and class for one arm on one carrier (called only where the arm is behind)."""
    A = C["primary"][mode]; st = C["step"]
    p = L.plateau(C["sec_means"], C["tacc_sec"], st)
    ms = L.margin_steps(C, A.mean)
    fired = L.guard_stats(A)["fired"] if mode == CLIP else None
    above, below = p["lo"] > W0, p["hi"] < W0
    c = dict(D=L.arm_diverged(C, mode), C=mode == CLIP and fired > 0 and (L.arm_nb(C, SEC) or above), U=above, O=below,
             N=ms > -N_STEPS and L.brackets(p, W0))
    return dict(C=C, mode=mode, A=A, p=p, ms=ms, fired=fired, c=c, cls=next((k for k in ORDER if c[k]), "X"),
                div_acc=L.diverged(A.acc, C["tacc"]), minr=float(A.acc.min() / C["tacc"]),
                nonfin=sum(not f for f in A.finite) + int(np.sum(~np.isfinite(A.acc))))


def tuned_noise(C):
    a = C["tv"].acc; low = bool(np.any(a < L.DIV_FRAC * C["tacc"])); spread = float(a.max() - a.min())
    return dict(low=low, spread=spread, spread_s=spread / C["step"], noisy=low or spread > F9_SPREAD * C["step"],
                nonfin=sum(not f for f in C["tv"].finite))


assert [(C["study"], C["carrier"]) for C in CS if CLIP in C["primary"]] == \
       [(C["study"], C["carrier"]) for C in CS if C["study"] in ("sec4", "sec5")], "clipped SEC on SEC4 and SEC5 only"

print(BAR)
print("SEC_Analysis A5, A9, A10 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): forecasts F5, F9, F10")
print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecasts, never PASS")
print(BAR)
print(f"carriers: {N} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); SEC '{SEC}' on all {N};"
      f" clipped SEC '{CLIP}' (kappa 0.5) on {sum(CLIP in C['primary'] for C in CS)} (SEC4 and SEC5)")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); behind = arm - tacc <= -step; points are per cent accuracy")

# ============================================================================================================== A5
hdr("A5  what kind of failure is each 'behind'?  first of D, C, U, O, N whose condition holds, else X (unclassified)")
print("   P = the calibrated not-behind set (fixed_sec grid points with mean > tacc_sec - step); lo, hi its lowest and highest grid point")
print("   D: a seed < 0.5 tacc or non-finite | C (clipped only): fired > 0 AND (unclipped SEC not behind OR lo > 0.5) | U: lo > 0.5 |"
      " O: hi < 0.5 | N: margin > -2 steps AND lo <= 0.5 <= hi")
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

print("\nREPORT: the clipped arm's other kappa cells at the primary window (SEC5; not declared, decides nothing): the same A5 rule"
      " read on each cell's seed mean")
print(f"   {'carrier':22} {'kappa':>5} {'mean':>8} {'margin st':>9} {'fired/seed':>15} {'nb':>2}  class")
for C in BY["sec5"]:
    for (v, fs, fe), A in sorted(C["cells"].get(CLIP, {}).items()):
        if fs != L.FS or fe != L.FE:
            continue
        ms = L.margin_steps(C, A.mean); nb = L.not_behind(A.mean, C["tacc"], C["step"]); g = L.guard_stats(A)
        p = L.plateau(C["sec_means"], C["tacc_sec"], C["step"])
        c = dict(D=L.diverged(A.acc, C["tacc"], A.finite), C=g["fired"] > 0 and (L.arm_nb(C, SEC) or p["lo"] > W0), U=p["lo"] > W0,
                 O=p["hi"] < W0, N=ms > -N_STEPS and L.brackets(p, W0))
        cls = "nb" if nb else next((k for k in ORDER if c[k]), "X")
        print(f"   {C['carrier'][:22]:22} {v:5g} {A.mean:8.4f} {ms:+9.3f} {str(g['per_seed_fired']):>15} {yn(nb):>2}  {cls}")

# ============================================================================================================== A9
hdr("A9  why SEC4 passed and SEC5 did not, carrier by carrier (the 14 carriers of SEC4 and SEC5)")
CL5 = {(r["C"]["study"], r["C"]["carrier"], r["mode"]): r["cls"] for r in CASES}
R9 = []
for C in BY["sec4"] + BY["sec5"]:
    k = (C["study"], C["carrier"]); As, Ac = C["primary"][SEC], C["primary"][CLIP]
    ss, sc, g = L.s_stats(As), L.s_stats(Ac), L.guard_stats(Ac)
    R9.append(dict(C=C, ms_c=L.margin_steps(C, Ac.mean), ms_s=L.margin_steps(C, As.mean), shape=(C["tacc_sec"] - C["tacc"]) / C["step"],
                   loc_c=(Ac.mean - C["tacc_sec"]) / C["step"], loc_s=(As.mean - C["tacc_sec"]) / C["step"],
                   cls_c=CL5.get(k + (CLIP,), "nb"), cls_s=CL5.get(k + (SEC,), "nb"), ss=ss, sc=sc, g=g, tn=tuned_noise(C)))
print("   margins, A1's parts and location costs in steps; class = A5 ('nb' = not behind); s over tasks and seeds of each arm;"
      " fired = the clip's firings per seed; max m = largest guard margin (fires at >= 0.5)")
print(f"   {'study':5} {'carrier':22} {'clip st':>8} {'SEC st':>8} {'shape st':>8} {'loc clip':>8} {'loc SEC':>8} {'cls clip':>8}"
      f" {'cls SEC':>7} {'s gm SEC':>10} {'s max SEC':>10} {'s gm clip':>10} {'s max clip':>10} {'fired/seed':>15} {'max m':>7}")
for r in R9:
    C = r["C"]
    print(f"   {C['study']:5} {C['carrier'][:22]:22} {r['ms_c']:+8.3f} {r['ms_s']:+8.3f} {r['shape']:+8.3f} {r['loc_c']:+8.3f}"
          f" {r['loc_s']:+8.3f} {r['cls_c']:>8} {r['cls_s']:>7} {r['ss']['gmean']:10.4g} {r['ss']['max']:10.4g} {r['sc']['gmean']:10.4g}"
          f" {r['sc']['max']:10.4g} {str(r['g']['per_seed_fired']):>15} {r['g']['max_margin']:7.4f}")
print("\n   properties (header) and the tuned raw arm's seeds: nonfin = its non-finite records; low = a tuned seed < 0.5 tacc;"
      f" spread = max - min of the tuned seeds; noisy = low OR spread > {F9_SPREAD:g} steps")
print(f"   {'study':5} {'carrier':22} {'d':>4} {'K':>3} {'tasks':>5} {'n_train':>7} {'imbal':>7} {'per-task n':28} {'lam*_raw':>9}"
      f" {'tacc':>8} {'step':>6} {'nonfin':>6} {'low':>3} {'spread':>7} {'st':>6} {'noisy':>5}")
for r in R9:
    C = r["C"]; t = r["tn"]
    print(f"   {C['study']:5} {C['carrier'][:22]:22} {C['d']:4d} {C['K']:3d} {C['n_tasks']:5d} {C['n_train']:7d} {C['imbalance']:7.2f}"
          f" {str(C['per_task_n']):28} {C['tuned']:9.4g} {C['tacc']:8.4f} {C['step']:6.3f} {t['nonfin']:6d} {yn(t['low']):>3} {t['spread']:7.3f}"
          f" {t['spread_s']:6.3f} {yn(t['noisy']):>5}")
print("\n   per-seed accuracies (seeds 0-4): the tuned raw lambda, the clipped SEC, the unclipped SEC; 0.5 tacc = the divergence line")
print(f"   {'study':5} {'carrier':22} {'0.5 tacc':>8}  {'tuned raw lambda':36}  {'clipped SEC':36}  unclipped SEC")
for r in R9:
    C = r["C"]
    print(f"   {C['study']:5} {C['carrier'][:22]:22} {L.DIV_FRAC * C['tacc']:8.4f}  {seeds(C['tv'].acc):36}  {seeds(C['primary'][CLIP].acc):36}"
          f"  {seeds(C['primary'][SEC].acc):36}")
print("\nper family (report): clipped SEC not behind | unclipped SEC not behind | clip fired on a carrier | median s max (SEC)"
      " | tuned arm noisy")
for s in ("sec4", "sec5"):
    rr = [r for r in R9 if r["C"]["study"] == s]
    print(f"   {s:5} {sum(r['cls_c'] == 'nb' for r in rr)}/{len(rr)} | {sum(r['cls_s'] == 'nb' for r in rr)}/{len(rr)} |"
          f" {sum(r['g']['fired'] > 0 for r in rr)}/{len(rr)} | {float(np.median([r['ss']['max'] for r in rr])):.4g} |"
          f" {sum(r['tn']['noisy'] for r in rr)}/{len(rr)}")

F9R = [r for r in R9 if r["C"]["study"] == "sec5" and r["cls_c"] != "nb"]
cls9 = [r["cls_c"] for r in F9R]; dist = sorted(set(cls9) - {"X"}, key=KEYS.index); dist_x = sorted(set(cls9), key=KEYS.index)
f9a = len(dist) >= F9_CLASSES; f9b = "C" in cls9; noisy9 = [r["C"]["carrier"] for r in F9R if r["tn"]["noisy"]]; f9c = bool(noisy9)
print(f"\nF9  SEC5's clipped failures: {len(F9R)} (" + ", ".join(f"{r['C']['carrier']} {r['cls_c']}" for r in F9R) + ")")
print(f"F9 (a) distinct classes among D, C, U, O, N: {len(dist)} {dist} >= {F9_CLASSES} -> {f9a}   (with X counted: {len(dist_x)} {dist_x})")
print(f"F9 (b) at least one is C: C on {cls9.count('C')} of {len(cls9)} -> {f9b}")
print(f"F9 (c) rule: a failure carrier whose tuned raw arm has a seed < {L.DIV_FRAC} x tacc, or a seed spread (max - min) > {F9_SPREAD:g}"
      " steps (a low-accuracy seed the tuned lambda shows too is not caused by the penalty)")
for r in F9R:
    C = r["C"]; t = r["tn"]
    print(f"       {C['carrier'][:22]:22} tuned seeds {seeds(C['tv'].acc)}; lowest {float(C['tv'].acc.min())!r} vs 0.5 tacc {L.DIV_FRAC * C['tacc']!r}"
          f" -> low {yn(t['low'])}; spread {t['spread']!r} = {t['spread_s']:.4f} steps (> {F9_SPREAD:g}: {yn(t['spread_s'] > F9_SPREAD)})"
          f" -> noisy {yn(t['noisy'])}")
print(f"       noisy on {len(noisy9)} of {len(F9R)} -> {f9c}")
print("REPORT (not the rule; decides nothing): on each SEC5 clipped-failure carrier, the grid points (primary window) where a seed is"
      " below 0.5 tacc or a record is non-finite, on the raw ('fixed') and calibrated ('fixed_sec') axes; * marks the tuned lambda")
for r in F9R:
    C = r["C"]
    for ax, g, t in (("raw", C["raw"], C["tuned"]), ("cal", C["sec"], C["tuned_sec"])):
        low = [w for w, a in g.items() if L.diverged(a.acc, C["tacc"], a.finite)]
        print(f"       {C['carrier'][:22]:22} {ax} {len(low):2d} of {len(g)}: "
              + (" ".join(f"{w:g}" + ("*" if w == t else "") for w in low) or "none"))
print("REPORT: the carriers the declaration names: " + "; ".join(
    f"{r['C']['carrier']} clipped class {r['cls_c']} (A5 conditions {''.join(k for k in ORDER if c5['c'][k]) or 'none'}),"
    f" tuned arm noisy {yn(r['tn']['noisy'])}"
    for r in F9R if r["C"]["carrier"] in ("volcanoes-d4", "pokerhand")
    for c5 in [x for x in CASES if x["mode"] == CLIP and x["C"] is r["C"]]))
print(f"F9: {word(f9a and f9b and f9c)}")

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

# ============================================================================================================== summary
print(); print(BAR)
print("summary (words computed above)")
print(f"   F5   {word(f5i and f5ii)}   (i) D {kD}/{nU} unclipped failures ({kD / nU:.3f} > {F5_SHARE}; most common {'/'.join(modes)}) -> {f5i};"
      f" (ii) clipped failures {clp_cls} all in C/U/N -> {f5ii} (none D -> {f5ii_red})")
print(f"   F9   {word(f9a and f9b and f9c)}   SEC5 clipped failures {len(F9R)}: (a) {len(dist)} distinct classes {dist} -> {f9a};"
      f" (b) C on {cls9.count('C')} -> {f9b}; (c) tuned arm noisy on {len(noisy9)} -> {f9c}")
print(f"   F10  {word(f10)}   {kH}/{nH} held-out passes with a negative margin ({kH / nH:.3f} >= {F10_SHARE})")
