"""SEC_Analysis A7 and A8, with forecasts F7 and F8 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257):
do carrier properties predict SEC's success, and was SEC4's family easy?

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads the pinned run records through sec_lib.load_all()
(validated first: loader_check.txt, every pinned count REPRODUCED) over the 42 scored carriers of SEC1, SCL3, SEC3, SEC4 and
SEC5, and nothing else: it opens no data and trains nothing. Tuned lambda, step, not behind and the transferred lambda are
sec_lib's (the frozen scorers' definitions); none is re-derived here.

A7  properties, per carrier, from each file's header line (sec_lib): d; K; n_train; per-task n = n_train / number of tasks;
    imbalance = largest over smallest used class count (sec_lib C["imbalance"]); number of tasks (C["n_tasks"]; named in the
    lead's task, not in the declaration's list; per_task = 2 on every carrier, asserted, so it is K / 2 and gives exactly K's
    partitions: it cannot change a best error); family (= study; the declaration's list).
    labels  SEC not behind: sec_lib.arm_nb(C, 'bayes_sec') on all 42 carriers (the declared label for F7);
            clipped SEC not behind: sec_lib.arm_nb(C, 'bayes_sec_clip') on the 14 carriers of SEC4 and SEC5 (REPORT).
    split   numeric property: every threshold t at a midpoint between consecutive sorted distinct values, both directions
            ('>' predicts not behind where x > t; '<' where x < t); errors = carriers whose label differs from the prediction.
            A property's best split is its fewest errors; the number of (t, direction) pairs that reach it is printed, and the
            first of them (t ascending, '>' before '<') is shown with its misclassified carriers. The trivial split (every
            carrier predicted alike) is not a threshold and is printed beside it as the majority baseline.
            family is categorical: its split is a bipartition of the families (predict not behind on one set of families);
            the best bipartition gives each family its majority label, so errors = the sum over families of the minority count.
    F7 HOLDS iff the fewest errors over every property (the six numeric and family) for the SEC label over the 42 carriers
    is >= 3 (DECLARATION.md F7: "No single property separates: the best split misclassifies at least 3 carriers").
    REPORT (decides nothing): the same for the clipped label on its 14 carriers; the best error over the declaration's own
    list alone (number of tasks dropped); the minimum per-task n as a further property; and a label-permutation null for the
    best error over the F7 property set (NPERM permutations of each label vector, numpy default_rng(SEED); the share of
    permutations whose best error is <= the observed one: how often labels with no link to the properties split as well).
A8  per family (= study): SD (ddof 1) of log10 lambda*_raw (with its min, median and max); the transferred lambda's not-behind
    count and share (SEC4-T's rule as sec_lib computes it for every study: exp of the median of log lambda*_raw over the other
    carriers of the study, snapped to EWC_COARSE by nearest log; its raw-grid seed mean against the tuned mean, a - tacc > -step);
    the not-behind counts of SEC ('bayes_sec'), the clipped SEC ('bayes_sec_clip', SEC4 and SEC5), raw Laplace ('bayes') and
    the one-factor SEC ('bayes_s1'). SEC's own saving: on the carriers where the transferred lambda is behind, how many SEC
    (and the clipped SEC) is not behind; beside it, the carriers where the transferred lambda is not behind and SEC is (REPORT).
    F8 HOLDS iff SEC4's transferred-lambda not-behind share >= SEC5's (DECLARATION.md F8).
The words HOLDS and FAILS are computed here from the printed numbers. Decisive numbers are printed at full precision beside the
rounded value (CLAUDE.md §7).

    uv run python SEC_Analysis/checks/a7_a8.py > SEC_Analysis/checks/a7_a8.txt
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sec_lib as L  # noqa: E402

D = L.load_all(); BY = L.by_study(D); CS = list(D.values()); N = len(CS)
SEC, CLIP, LAP, S1 = "bayes_sec", "bayes_sec_clip", "bayes", "bayes_s1"
F7_MIN = 3                                                            # DECLARATION.md F7: at least 3 misclassified
NPERM, SEED = 5000, 0                                                 # the REPORT permutation null
BAR = "=" * 150
assert all(C["per_task"] == 2 for C in CS) and all(C["n_tasks"] == C["K"] // 2 for C in CS)
PROPS = [("d", lambda C: float(C["d"])), ("K", lambda C: float(C["K"])), ("n_train", lambda C: float(C["n_train"])),
         ("per-task n", lambda C: C["n_train"] / C["n_tasks"]), ("imbalance", lambda C: float(C["imbalance"])),
         ("tasks", lambda C: float(C["n_tasks"]))]
DECL = ("d", "K", "n_train", "per-task n", "imbalance", "family")      # the declaration's list (A7)
REP_PROPS = [("min per-task n", lambda C: float(min(C["per_task_n"])))]


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "Y" if b else "N"


def frac(k, n):
    return f"{k}/{n} = {k / n!r} ({k / n:.3f})"


def splits(x, y):
    """Every (errors, t, dir) of a numeric property x (N,) against the bool label y (N,), t ascending, '>' before '<'."""
    xs = np.unique(x); out = []
    for lo, hi in zip(xs[:-1], xs[1:]):
        t = (lo + hi) / 2; above = x > t
        out.append((int(np.sum(above != y)), float(t), ">")); out.append((int(np.sum((~above) != y)), float(t), "<"))
    return out


def best_numeric(x, y):
    sp = splits(x, y); e = min(s[0] for s in sp); opt = [s for s in sp if s[0] == e]
    _, t, dr = opt[0]; pred = (x > t) if dr == ">" else (x < t)
    return dict(err=e, n_opt=len(opt), t=t, dir=dr, pred=pred, n_thr=len(sp) // 2)


def best_family(fam, y):
    fams = sorted(set(fam), key=L.STUDIES.index); err = 0; maj = {}; pred = np.zeros(len(y), bool); tied = []
    for f in fams:
        m = np.array([g == f for g in fam]); k = int(y[m].sum()); n = int(m.sum())
        maj[f] = k * 2 >= n; err += min(k, n - k); pred[m] = maj[f]
        if 2 * k == n:
            tied.append(f)
    return dict(err=err, maj=maj, pred=pred, tied=tied, fams=fams)


def perm_best(Xs, fam, y, rng):
    """The best error over the numeric properties Xs and family, for NPERM permutations of y (the count of passes fixed)."""
    n = len(y); Y = np.array([rng.permutation(y) for _ in range(NPERM)])            # (P, n)
    best = np.full(NPERM, n, dtype=int)
    for x in Xs:
        xs = np.unique(x); ts = (xs[:-1] + xs[1:]) / 2
        A = x[None, :] > ts[:, None]                                                 # (T, n)
        e_gt = (A[None, :, :] != Y[:, None, :]).sum(-1)                              # (P, T); '<' errors are n - e_gt
        best = np.minimum(best, np.minimum(e_gt, n - e_gt).min(1))
    ef = np.zeros(NPERM, dtype=int)
    for f in sorted(set(fam)):
        m = np.array([g == f for g in fam]); k = Y[:, m].sum(1); ef += np.minimum(k, m.sum() - k)
    return np.minimum(best, ef)


def a7(Cs, mode, title):
    y = np.array([L.arm_nb(C, mode) for C in Cs]); fam = [C["family"] for C in Cs]; n = len(Cs); k = int(y.sum())
    print(f"\n{title}: label = {mode} not behind; {n} carriers, not behind {k}, behind {n - k};"
          f" majority baseline (no split, every carrier predicted {'not behind' if 2 * k >= n else 'behind'}) errors {min(k, n - k)}")
    print(f"   {'property':24} {'thresholds':>11} {'best errors':>11} {'optimal splits':>14} {'first best split':>30}  misclassified at that split")
    res = {}
    for name, f in PROPS + REP_PROPS:
        x = np.array([f(C) for C in Cs]); b = best_numeric(x, y); res[name] = b
        mis = [C["carrier"] for C, p, yy in zip(Cs, b["pred"], y) if p != yy]
        tag = " (REPORT)" if name in dict(REP_PROPS) else ""; rule = f"not behind if x {b['dir']} {b['t']:.6g}"
        print(f"   {name + tag:24} {b['n_thr']:>11d} {b['err']:>11d} {b['n_opt']:>14d} {rule:>30}  " + ", ".join(mis))
    fb = best_family(fam, y); res["family"] = fb
    mis = [C["carrier"] for C, p, yy in zip(Cs, fb["pred"], y) if p != yy]
    print(f"   {'family':24} {'bipartition':>11} {fb['err']:>11d} {'':>14} {'majority per family':>30}  " + ", ".join(mis))
    print("   family majorities: " + "; ".join(
        f"{f} {int(y[[g == f for g in fam]].sum())}/{fam.count(f)} -> {'not behind' if fb['maj'][f] else 'behind'}"
        + (" (tied; either side gives the same errors)" if f in fb["tied"] else "") for f in fb["fams"]))
    return y, fam, res


def rows_best(res, names):
    e = min(res[p]["err"] for p in names); return e, [p for p in names if res[p]["err"] == e]


# ---------------------------------------------------------------------------------------------------------------- header
print(BAR)
print("SEC_Analysis A7 and A8 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): forecasts F7 and F8")
print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecasts, never PASS")
print(BAR)
print(f"carriers: {N} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); SEC arm '{SEC}' on every carrier; clipped SEC"
      f" '{CLIP}' on {sum(CLIP in C['primary'] for C in CS)}; raw Laplace '{LAP}' on {sum(LAP in C['primary'] for C in CS)};"
      f" one-factor SEC '{S1}' on {sum(S1 in C['primary'] for C in CS)}")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); not behind = arm - tacc > -step (strict); points are per cent"
      " accuracy")

# ------------------------------------------------------------------------------------------------------------------- A7
print(); print(BAR)
print("A7  do carrier properties predict success?  best single-property threshold split against the not-behind label")
print(BAR)
print("per carrier (per-task n = n_train / tasks; imbalance = largest / smallest used class count; min n_t = the smallest task's"
      " training rows, REPORT)")
print(f"   {'study':5} {'carrier':34} {'d':>5} {'K':>3} {'tasks':>5} {'n_train':>7} {'per-task n':>10} {'min n_t':>7} {'imbalance':>9}"
      f"  {'SEC nb':>6} {'clip nb':>7}")
for C in CS:
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['d']:5d} {C['K']:3d} {C['n_tasks']:5d} {C['n_train']:7d}"
          f" {C['n_train'] / C['n_tasks']:10.2f} {min(C['per_task_n']):7d} {C['imbalance']:9.3f}  {yn(L.arm_nb(C, SEC)):>6}"
          f" {yn(L.arm_nb(C, CLIP)) if CLIP in C['primary'] else '-':>7}")
print(f"number of tasks = K / 2 on all {N} carriers (per_task = 2 everywhere): its splits are K's, so its best error equals K's")

y7, fam7, R7 = a7(CS, SEC, "A7 (declared, F7)")
F7_SET = [p for p, _ in PROPS] + ["family"]
e7, arg7 = rows_best(R7, F7_SET); eD, argD = rows_best(R7, list(DECL))
assert R7["tasks"]["err"] == R7["K"]["err"]
print(f"   best over the F7 property set ({', '.join(F7_SET)}): {e7} misclassified, reached by {', '.join(arg7)}")
print(f"   REPORT: best over the declaration's own list alone ({', '.join(DECL)}): {eD} misclassified, reached by {', '.join(argD)}")
Xs7 = [np.array([f(C) for C in CS]) for _, f in PROPS]
pb7 = perm_best(Xs7, fam7, y7, np.random.default_rng(SEED))
print(f"   REPORT permutation null ({NPERM} permutations of the {N} labels, seed {SEED}; F7 property set): best error median"
      f" {float(np.median(pb7)):g}, 5th percentile {float(np.percentile(pb7, 5)):g}, min {int(pb7.min())}, max {int(pb7.max())};"
      f" share with best error <= observed {e7}: {frac(int(np.sum(pb7 <= e7)), NPERM)}")

CC = [C for C in CS if CLIP in C["primary"]]
yc, famc, RC = a7(CC, CLIP, "A7 (REPORT, the clipped label on SEC4 and SEC5)")
ec, argc = rows_best(RC, F7_SET)
print(f"   best over the F7 property set: {ec} misclassified, reached by {', '.join(argc)}")
Xsc = [np.array([f(C) for C in CC]) for _, f in PROPS]
pbc = perm_best(Xsc, famc, yc, np.random.default_rng(SEED))
print(f"   REPORT permutation null ({NPERM} permutations of the {len(CC)} labels, seed {SEED}; F7 property set): best error median"
      f" {float(np.median(pbc)):g}, 5th percentile {float(np.percentile(pbc, 5)):g}, min {int(pbc.min())}, max {int(pbc.max())};"
      f" share with best error <= observed {ec}: {frac(int(np.sum(pbc <= ec)), NPERM)}")

f7 = e7 >= F7_MIN
print(f"\nF7  fewest errors of any single-property split, SEC label, {N} carriers: {e7} ({', '.join(arg7)}) >= {F7_MIN} -> {f7}")
print(f"F7: {word(f7)}  (the forecast read: \"No single property separates: the best split misclassifies at least 3 carriers\")")
print(f"    (report: the clipped label's best split on its {len(CC)} carriers misclassifies {ec}; >= {F7_MIN}: {ec >= F7_MIN})")

# ------------------------------------------------------------------------------------------------------------------- A8
print(); print(BAR)
print("A8  was SEC4's family easy?  per family: spread of lambda*_raw, the transferred lambda (SEC4-T's rule), and each arm's"
      " not-behind count")
print(BAR)
print("per carrier: loco = exp(median log lambda*_raw of the other carriers of the study) (unsnapped | snapped to EWC_COARSE);"
      " loco acc = its raw-grid seed mean; nb = not behind the tuned lambda")
print(f"   {'study':5} {'carrier':34} {'lam*_raw':>10} {'tacc':>8} {'step':>6} {'loco':>9} {'snap':>6} {'loco acc':>8} {'loco st':>8}"
      f"  {'loco':>4} {'SEC':>3} {'clip':>4} {'Lap':>3} {'s1':>3}")
NB = {}
for C in CS:
    k = (C["study"], C["carrier"])
    NB[k] = dict(loco=L.not_behind(C["loco_acc"], C["tacc"], C["step"]), sec=L.arm_nb(C, SEC), lap=L.arm_nb(C, LAP),
                 s1=L.arm_nb(C, S1), clip=L.arm_nb(C, CLIP) if CLIP in C["primary"] else None)
    r = NB[k]
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:10.6g} {C['tacc']:8.4f} {C['step']:6.3f} {C['loco_lam']:9.4g}"
          f" {C['loco']:6g} {C['loco_acc']:8.4f} {L.margin_steps(C, C['loco_acc']):+8.3f}  {yn(r['loco']):>4} {yn(r['sec']):>3}"
          f" {'-' if r['clip'] is None else yn(r['clip']):>4} {yn(r['lap']):>3} {yn(r['s1']):>3}")

print("\nper family (SD of log10 lambda*_raw with ddof 1; counts are not behind / carriers; clip only where recorded)")
print(f"   {'family':6} {'N':>3} {'SD lg lam*':>10} {'min lam*':>10} {'median':>10} {'max lam*':>10} {'decades':>7}"
      f" {'loco nb':>8} {'loco share':>10} {'SEC':>6} {'clip':>6} {'Lap':>6} {'s1':>6}")
SH = {}
for s in L.STUDIES + ("pooled",):
    Cs = CS if s == "pooled" else BY[s]; ks = [(C["study"], C["carrier"]) for C in Cs]; n = len(Cs)
    lg = np.log10([C["tuned"] for C in Cs]); lam = [C["tuned"] for C in Cs]
    c = {a: sum(bool(NB[k][a]) for k in ks) for a in ("loco", "sec", "lap", "s1")}
    ncl = [k for k in ks if NB[k]["clip"] is not None]; ccl = sum(NB[k]["clip"] for k in ncl)
    SH[s] = (c["loco"], n)
    print(f"   {s:6} {n:3d} {float(np.std(lg, ddof=1)):10.4f} {min(lam):10.4g} {float(np.median(lam)):10.4g} {max(lam):10.4g}"
          f" {float(lg.max() - lg.min()):7.3f} {c['loco']:>4d}/{n:<3d} {c['loco'] / n:10.4f} {c['sec']:>3d}/{n:<2d}"
          f" {(f'{ccl}/{len(ncl)}' if ncl else '-'):>6} {c['lap']:>3d}/{n:<2d} {c['s1']:>3d}/{n:<2d}")
print("   (pooled: SD over all 42 lambda*_raw; each carrier's transferred lambda is still taken within its own study)")

print("\nSEC's own saving: on the carriers where the transferred lambda is behind, the arms that are not behind (REPORT beside it:"
      " where the transferred lambda is not behind, the arms that are behind)")
print(f"   {'family':6} {'loco behind':>11} {'SEC nb there':>12} {'clip nb there':>13} {'Lap nb there':>12}"
      f" {'s1 nb there':>11} | {'loco nb':>7} {'SEC behind there':>16} {'clip behind there':>17}  carriers where loco is behind")
for s in L.STUDIES + ("pooled",):
    Cs = CS if s == "pooled" else BY[s]; ks = [(C["study"], C["carrier"]) for C in Cs]
    B = [k for k in ks if not NB[k]["loco"]]; G = [k for k in ks if NB[k]["loco"]]
    Bc = [k for k in B if NB[k]["clip"] is not None]; Gc = [k for k in G if NB[k]["clip"] is not None]
    cB = f"{sum(NB[k]['clip'] for k in Bc)}/{len(Bc)}" if Bc else "-"
    cG = f"{sum(not NB[k]['clip'] for k in Gc)}/{len(Gc)}" if Gc else "-"
    print(f"   {s:6} {len(B):11d} {sum(NB[k]['sec'] for k in B):>8d}/{len(B):<3d} {cB:>13}"
          f" {sum(NB[k]['lap'] for k in B):>8d}/{len(B):<3d} {sum(NB[k]['s1'] for k in B):>7d}/{len(B):<3d} |"
          f" {len(G):7d} {sum(not NB[k]['sec'] for k in G):>12d}/{len(G):<3d} {cG:>17}  "
          + (", ".join(k[1] for k in B) if s != "pooled" else "(the per-family lists)"))

(k4, n4), (k5, n5) = SH["sec4"], SH["sec5"]; sh4, sh5 = k4 / n4, k5 / n5
f8 = sh4 >= sh5
print(f"\nF8  transferred-lambda not-behind share: sec4 {frac(k4, n4)} >= sec5 {frac(k5, n5)} -> {f8}")
print(f"F8: {word(f8)}  (the forecast read: \"SEC4's family has a transferred-lambda not-behind share at least as high as SEC5's:"
      " part of SEC4's pass is the family's ease\")")

print(); print(BAR)
print("summary (words computed above)")
print(f"   F7    {word(f7)}   best single-property split, SEC label: {e7} misclassified of {N} ({', '.join(arg7)}; >= {F7_MIN});"
      f" report: clipped label {ec} of {len(CC)}")
print(f"   F8    {word(f8)}   transferred-lambda not-behind share sec4 {k4}/{n4} = {sh4:.4f} >= sec5 {k5}/{n5} = {sh5:.4f}")
print(BAR)
