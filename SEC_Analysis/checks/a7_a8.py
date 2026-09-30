"""SEC_Analysis A7 and A8, with forecasts F7 and F8 (SEC_Analysis/DECLARATION.md at 5f64b5f with Amendments 1 (347cb90) and
2 (e15e1ff); prompt-log entry 257): do carrier properties predict SEC's success, and was SEC4's family easy? Amendment 2 adds
M5, M6 and A13 and bears on nothing here. Amendment 1's report (F7 and F8 with the floor-bound carriers removed) is printed in
its own part after A8, and its words are repeated in the summary.

POST HOC on SEEN records. No ledger row; no word here is a PASS. It reads the pinned run records through sec_lib.load_all()
(validated first: loader_check.txt, every pinned count REPRODUCED) over the 42 scored carriers of SEC1, SCL3, SEC3, SEC4 and
SEC5, and nothing else: it opens no data and trains nothing. Tuned lambda, step, not behind and the transferred lambda are
sec_lib's (the frozen scorers' definitions); none is re-derived here.

A7  properties, per carrier, from each file's header line (sec_lib), exactly the declaration's list: d; K; n_train; per-task
    n = n_train / number of tasks; imbalance = largest over smallest used class count (sec_lib C["imbalance"]); family
    (= study). Five numeric properties and family.
    labels  the two A7 names ("against SEC's and the clipped SEC's not-behind label"):
            SEC not behind: sec_lib.arm_nb(C, 'bayes_sec') on all 42 carriers;
            clipped SEC not behind: sec_lib.arm_nb(C, 'bayes_sec_clip') on the 14 carriers of SEC4 and SEC5 (the only ones
            with a clipped record).
    split   numeric property: every threshold t at a midpoint between consecutive sorted distinct values, both directions
            ('>' predicts not behind where x > t; '<' where x < t); errors = carriers whose label differs from the prediction.
            A property's best split is its fewest errors; the number of (t, direction) pairs that reach it is printed, and the
            first of them (t ascending, '>' before '<') is shown with its misclassified carriers. The trivial split (every
            carrier predicted alike) is not a threshold; it is printed once per label as the majority baseline and is never a
            property's split.
            family is categorical: its split is a non-trivial bipartition of the families present (predict not behind on a
            non-empty proper subset S of them). Every such S is enumerated (bit order over the families in study order); the
            fewest errors, the number of S reaching it and the first such S are printed. The all-one-side bipartition is the
            trivial split and is excluded, as for the numeric thresholds; with one family present there is no family split.
    F7  AMBIGUITY: A7 computes against two labels ("SEC's and the clipped SEC's not-behind label"); F7 ("No single property
        separates: the best split misclassifies at least 3 carriers") names neither. The most literal reading applies F7 to
        each label A7 names: F7 HOLDS iff, for EACH label, the fewest errors of any property's split (the declaration's five
        numeric properties and family) is >= 3. Both per-label words are printed, and the combined word is the F7 word. A
        label vector with one class only (every carrier not behind, or every carrier behind) has nothing to separate: its
        word is UNDEFINED, printed as such.
    REPORT (undeclared; decides nothing): two further properties, the number of tasks (C["n_tasks"]; per_task = 2 on every
    carrier, asserted, so it is K / 2 and gives exactly K's partitions) and the minimum per-task n (the smallest task's training
    rows); and a label-permutation null for the best error over F7's property set (NPERM permutations of each label vector,
    numpy default_rng(SEED); the share of permutations whose best error is <= the observed one). The null is post hoc and not
    declared; its share is not a test and is not quoted as one.
A8  per family (= study), the declared columns: SD (ddof 1) of log10 lambda*_raw; the transferred lambda's not-behind count
    and share (SEC4-T's rule as sec_lib computes it for every study: exp of the median of log lambda*_raw over the other
    carriers of the study, snapped to EWC_COARSE by nearest log; its raw-grid seed mean against the tuned mean,
    a - tacc > -step); SEC's ('bayes_sec') and the one-factor SEC's ('bayes_s1') not-behind counts. REPORT columns (not in
    A8's list): lambda*_raw's min, median, max and decades; the clipped SEC ('bayes_sec_clip', SEC4 and SEC5) and raw Laplace
    ('bayes') counts. F8 HOLDS iff SEC4's transferred-lambda not-behind share >= SEC5's (DECLARATION.md F8).
    REPORT (undeclared, post hoc; decides nothing): (i) the transferred lambda's failures read as divergence: per carrier the
    seeds that are non-finite at the transferred lambda (the raw-grid records' finite flags; a non-finite run is recorded
    as acc 0) and sec_lib.diverged() there; per family, of the carriers where the transferred lambda is behind, how many
    have a non-finite seed or diverge. (ii) A SEC-T analogue ("SEC's own saving"): on the set B of carriers where the
    transferred lambda is behind, how many of each arm are not behind; beside it, where the transferred lambda is not behind,
    how many SEC and the clipped SEC are behind. SEC-T was registered only for SEC3 (on SEC), SEC4 and SEC5 (on the clipped
    SEC), with a minimum |B| = MIN_B read from runs/sec3/frozen/sec3_score.py (sec4_score and sec5_score import it); a family
    with |B| < MIN_B is marked below the registered minimum and its counts are not printed (SEC4-T was NOT DECIDABLE there).
Amendment 1 (A12)  floor = 100 x the majority class's share of the loaded rows (the header's class_counts); a carrier is
    floor-bound iff tacc - floor < 3 steps (tacc, step: the tuned lambda*_raw's seed mean and step). F7 (both labels and
    combined) and F8 are recomputed with the floor-bound carriers removed, as a REPORT, post hoc in origin. The transferred
    lambda is not re-derived on the kept carriers (it stays sec_lib's, from the whole study); only the counts drop carriers.
    AMBIGUITY (as in a4_a6.py): the amendment does not say whether "removed" means the floor-bound carriers among all 42 or
    only among the 30 held-out; the most literal reading, every floor-bound carrier removed (as a1_a3.py does), is read
    first and the held-out-only reading beside it. The clipped label and F8 read only SEC4 and SEC5 (held-out), so on them
    the two readings coincide (checked and printed).
The words HOLDS, FAILS and UNDEFINED are computed here from the printed numbers. Decisive numbers are printed at full precision
beside the rounded value (CLAUDE.md §7).

    uv run python SEC_Analysis/checks/a7_a8.py > SEC_Analysis/checks/a7_a8.txt
"""
from __future__ import annotations

import os
import re
import sys

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sec_lib as L  # noqa: E402

D = L.load_all(); BY = L.by_study(D); CS = list(D.values()); N = len(CS)
SEC, CLIP, LAP, S1 = "bayes_sec", "bayes_sec_clip", "bayes", "bayes_s1"
F7_MIN = 3                                                            # DECLARATION.md F7: at least 3 misclassified
FLOOR_STEPS = 3.0                                                     # Amendment 1 (A12): floor-bound iff tacc - floor < 3 steps
HELD = L.STUDIES[1:]                                                  # the 30 held-out carriers (SCL3, SEC3, SEC4, SEC5)
NPERM, SEED = 5000, 0                                                 # the REPORT permutation null
MINB_SRC = "runs/sec3/frozen/sec3_score.py"                           # SEC3-T's registered minimum |B| (SEC4/SEC5 import it)
_m = re.findall(r"^MIN_B\s*=\s*(\d+)", open(os.path.join(L.ROOT, MINB_SRC)).read(), re.M)
assert len(_m) == 1, _m
MIN_B = int(_m[0])
BAR = "=" * 150
assert all(C["per_task"] == 2 for C in CS) and all(C["n_tasks"] == C["K"] // 2 for C in CS)
PROPS = [("d", lambda C: float(C["d"])), ("K", lambda C: float(C["K"])), ("n_train", lambda C: float(C["n_train"])),
         ("per-task n", lambda C: C["n_train"] / C["n_tasks"]), ("imbalance", lambda C: float(C["imbalance"]))]
REP_PROPS = [("tasks", lambda C: float(C["n_tasks"])), ("min per-task n", lambda C: float(min(C["per_task_n"])))]
DECL = ("d", "K", "n_train", "per-task n", "imbalance", "family")      # the declaration's list (A7)
F7_SET = [p for p, _ in PROPS] + ["family"]
assert tuple(F7_SET) == DECL


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "Y" if b else "N"


def frac(k, n):
    return f"{k}/{n} = {k / n!r} ({k / n:.3f})"


def key(C):
    return (C["study"], C["carrier"])


def floor_of(C):                                                        # Amendment 1: 100 x the majority class's share
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * max(cc) / sum(cc)


def splits(x, y):
    """Every (errors, t, dir) of a numeric property x (N,) against the bool label y (N,), t ascending, '>' before '<'."""
    xs = np.unique(x); out = []
    for lo, hi in zip(xs[:-1], xs[1:]):
        t = (lo + hi) / 2; above = x > t
        out.append((int(np.sum(above != y)), float(t), ">")); out.append((int(np.sum((~above) != y)), float(t), "<"))
    return out


def best_numeric(x, y):
    sp = splits(x, y)
    if not sp:                                                          # one distinct value: no threshold exists
        return None
    e = min(s[0] for s in sp); opt = [s for s in sp if s[0] == e]
    _, t, dr = opt[0]; pred = (x > t) if dr == ">" else (x < t)
    return dict(err=e, n_opt=len(opt), t=t, dir=dr, pred=pred, n_thr=len(sp) // 2)


def fam_masks(fams):
    """The non-trivial bipartitions of the families: bool (M, F), row b-1 = bit pattern b (bit i: family i predicted not behind)."""
    F = len(fams)
    return np.array([[(b >> i) & 1 for i in range(F)] for b in range(1, 2 ** F - 1)], dtype=bool).reshape(-1, F)


def best_family(fam, y):
    fams = sorted(set(fam), key=L.STUDIES.index)
    idx = {f: np.array([g == f for g in fam]) for f in fams}
    k = {f: int(y[idx[f]].sum()) for f in fams}; n = {f: int(idx[f].sum()) for f in fams}
    if len(fams) < 2:
        return dict(err=None, fams=fams, k=k, n=n)
    M = fam_masks(fams)
    errs = [sum((n[f] - k[f]) if m[i] else k[f] for i, f in enumerate(fams)) for m in M]
    e = min(errs); opt = [j for j, v in enumerate(errs) if v == e]
    S = [f for i, f in enumerate(fams) if M[opt[0]][i]]
    pred = np.zeros(len(y), bool)
    for f in S:
        pred |= idx[f]
    return dict(err=e, n_opt=len(opt), n_bip=len(M), S=S, pred=pred, fams=fams, k=k, n=n)


def perm_best(Xs, fam, y, rng):
    """The best error over the numeric properties Xs and family (non-trivial bipartitions), for NPERM permutations of y."""
    n = len(y); Y = np.array([rng.permutation(y) for _ in range(NPERM)])            # (P, n)
    best = np.full(NPERM, n, dtype=int)
    for x in Xs:
        xs = np.unique(x)
        if len(xs) < 2:
            continue
        ts = (xs[:-1] + xs[1:]) / 2
        A = x[None, :] > ts[:, None]                                                 # (T, n)
        e_gt = (A[None, :, :] != Y[:, None, :]).sum(-1)                              # (P, T); '<' errors are n - e_gt
        best = np.minimum(best, np.minimum(e_gt, n - e_gt).min(1))
    fams = sorted(set(fam), key=L.STUDIES.index)
    if len(fams) >= 2:
        idx = [np.array([g == f for g in fam]) for f in fams]
        kk = np.stack([Y[:, m].sum(1) for m in idx], 1)                              # (P, F)
        nf = np.array([m.sum() for m in idx]); M = fam_masks(fams).astype(int)       # (M, F)
        ef = (nf[None, :] - kk) @ M.T + kk @ (1 - M).T                               # (P, M)
        best = np.minimum(best, ef.min(1))
    return best


def a7(Cs, mode, title):
    y = np.array([L.arm_nb(C, mode) for C in Cs]); fam = [C["family"] for C in Cs]; n = len(Cs); k = int(y.sum())
    print(f"\n{title}: label = {mode} not behind; {n} carriers, not behind {k}, behind {n - k};"
          f" majority baseline (the trivial split, every carrier predicted {'not behind' if 2 * k >= n else 'behind'}; not a"
          f" property's split) errors {min(k, n - k)}")
    print(f"   {'property':36} {'thresholds':>11} {'best errors':>11} {'optimal splits':>14} {'first best split':>30}  misclassified at that split")
    res = {}
    for name, f in PROPS + REP_PROPS:
        x = np.array([f(C) for C in Cs]); b = best_numeric(x, y); res[name] = b
        tag = " (REPORT, undeclared)" if name in dict(REP_PROPS) else ""
        if b is None:
            print(f"   {name + tag:36} {0:>11d} {'-':>11} {'-':>14} {'(one distinct value)':>30}"); continue
        mis = [C["carrier"] for C, p, yy in zip(Cs, b["pred"], y) if p != yy]
        rule = f"not behind if x {b['dir']} {b['t']:.6g}"
        print(f"   {name + tag:36} {b['n_thr']:>11d} {b['err']:>11d} {b['n_opt']:>14d} {rule:>30}  " + ", ".join(mis))
    fb = best_family(fam, y); res["family"] = fb if fb["err"] is not None else None
    if fb["err"] is None:
        print(f"   {'family':36} {0:>11d} {'-':>11} {'-':>14} {'(one family: no bipartition)':>30}")
    else:
        mis = [C["carrier"] for C, p, yy in zip(Cs, fb["pred"], y) if p != yy]
        rule = "not behind on {" + ", ".join(fb["S"]) + "}"
        print(f"   {'family':36} {str(fb['n_bip']) + ' bip.':>11} {fb['err']:>11d} {fb['n_opt']:>14d} {rule:>30}  " + ", ".join(mis))
    print("   family counts (not behind / carriers): " + "; ".join(f"{f} {fb['k'][f]}/{fb['n'][f]}" for f in fb["fams"])
          + "; the family row is the best NON-TRIVIAL bipartition (the all-one-side split is the majority baseline above)")
    if fb["err"] is not None:
        print(f"   family row equals the majority baseline's errors: {yn(fb['err'] == min(k, n - k))}")
    for name in dict(REP_PROPS):
        if name == "tasks" and res["tasks"] is not None and res["K"] is not None:
            assert res["tasks"]["err"] == res["K"]["err"]
    return y, fam, res


def rows_best(res, names):
    got = [p for p in names if res[p] is not None]
    e = min(res[p]["err"] for p in got); return e, [p for p in got if res[p]["err"] == e]


def f7_word(y, e):
    """F7 for one label: UNDEFINED with one class only; else HOLDS iff e >= F7_MIN."""
    if y.all() or not y.any():
        return "UNDEFINED", None
    return word(e >= F7_MIN), e >= F7_MIN


def f7_report_line(lab, y, e, arg, w):
    if w == "UNDEFINED":
        print(f"   F7 {lab} (report): one label only ({int(y.sum())} of {len(y)} not behind), so there is nothing to separate"
              f" (any property's split misclassifies >= 1 by construction; fewest {e}) -> {w}")
    else:
        print(f"   F7 {lab} (report): fewest errors {e} ({', '.join(arg)}) >= {F7_MIN} -> {w}")


def combine(ws):
    """The combined F7 word: FAILS if any label FAILS; UNDEFINED if none FAILS and one is UNDEFINED; else HOLDS."""
    return "FAILS" if "FAILS" in ws else ("UNDEFINED" if "UNDEFINED" in ws else "HOLDS")


# ---------------------------------------------------------------------------------------------------------------- header
print(BAR)
print("SEC_Analysis A7 and A8 (SEC_Analysis/DECLARATION.md at 5f64b5f; Amendments 1 (347cb90) and 2 (e15e1ff); prompt-log entry 257):"
      " forecasts F7 and F8")
print("POST HOC on SEEN records; no ledger row; the words are HOLDS / FAILS against the declared forecasts, never PASS."
      " Amendment 2 bears on nothing here; Amendment 1's report follows A8")
print(BAR)
print(f"carriers: {N} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); SEC arm '{SEC}' on every carrier; clipped SEC"
      f" '{CLIP}' on {sum(CLIP in C['primary'] for C in CS)}; raw Laplace '{LAP}' on {sum(LAP in C['primary'] for C in CS)};"
      f" one-factor SEC '{S1}' on {sum(S1 in C['primary'] for C in CS)}")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); not behind = arm - tacc > -step (strict); points are per cent"
      " accuracy")

# ------------------------------------------------------------------------------------------------------------------- A7
print(); print(BAR)
print("A7  do carrier properties predict success?  best single-property threshold split against each not-behind label A7 names")
print(BAR)
print("per carrier (per-task n = n_train / tasks; imbalance = largest / smallest used class count; tasks and min n_t = the smallest"
      " task's training rows are REPORT, undeclared)")
print(f"   {'study':5} {'carrier':34} {'d':>5} {'K':>3} {'tasks':>5} {'n_train':>7} {'per-task n':>10} {'min n_t':>7} {'imbalance':>9}"
      f"  {'SEC nb':>6} {'clip nb':>7}")
for C in CS:
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['d']:5d} {C['K']:3d} {C['n_tasks']:5d} {C['n_train']:7d}"
          f" {C['n_train'] / C['n_tasks']:10.2f} {min(C['per_task_n']):7d} {C['imbalance']:9.3f}  {yn(L.arm_nb(C, SEC)):>6}"
          f" {yn(L.arm_nb(C, CLIP)) if CLIP in C['primary'] else '-':>7}")
print(f"number of tasks = K / 2 on all {N} carriers (per_task = 2 everywhere): its splits are K's, so its best error equals K's")
print(f"F7's property set is the declaration's list: {', '.join(F7_SET)} (five numeric properties and family)")


def perm_line(Cs, fam, y, e, lab):
    Xs = [np.array([f(C) for C in Cs]) for _, f in PROPS]
    pb = perm_best(Xs, fam, y, np.random.default_rng(SEED))
    print(f"   REPORT, undeclared, post hoc; decides nothing (not a test): label-permutation null, {NPERM} permutations of the"
          f" {len(Cs)} {lab} labels, seed {SEED}, F7's property set: best error median {float(np.median(pb)):g}, 5th percentile"
          f" {float(np.percentile(pb, 5)):g}, min {int(pb.min())}, max {int(pb.max())}; share with best error <= observed {e}:"
          f" {frac(int(np.sum(pb <= e)), NPERM)}")


y7, fam7, R7 = a7(CS, SEC, "A7, label 1 of 2 (SEC)")
e7, arg7 = rows_best(R7, F7_SET)
print(f"   best over F7's property set ({', '.join(F7_SET)}): {e7} misclassified, reached by {', '.join(arg7)}")
e7r, arg7r = rows_best(R7, F7_SET + [p for p, _ in REP_PROPS])
print(f"   REPORT: best with the two undeclared properties added: {e7r} misclassified, reached by {', '.join(arg7r)}")
perm_line(CS, fam7, y7, e7, "SEC")

CC = [C for C in CS if CLIP in C["primary"]]
yc, famc, RC = a7(CC, CLIP, "A7, label 2 of 2 (the clipped SEC, SEC4 and SEC5)")
ec, argc = rows_best(RC, F7_SET)
print(f"   best over F7's property set ({', '.join(F7_SET)}): {ec} misclassified, reached by {', '.join(argc)}")
ecr, argcr = rows_best(RC, F7_SET + [p for p, _ in REP_PROPS])
print(f"   REPORT: best with the two undeclared properties added: {ecr} misclassified, reached by {', '.join(argcr)}")
perm_line(CC, famc, yc, ec, "clipped SEC")

w7s, _ = f7_word(y7, e7); w7c, _ = f7_word(yc, ec); w7 = combine([w7s, w7c])
print("\nAMBIGUITY: A7 computes against \"SEC's and the clipped SEC's not-behind label\"; F7 (\"No single property separates: the best"
      " split misclassifies at least 3 carriers\") names neither.")
print("   The most literal reading applies F7 to each label A7 names: F7 HOLDS only if it holds on both. Both per-label words are"
      " printed; the combined word is the F7 word.")
print(f"F7 label SEC ({N} carriers): fewest errors of any single-property split {e7} ({', '.join(arg7)}) >= {F7_MIN} -> {w7s}")
print(f"F7 label clipped SEC ({len(CC)} carriers): fewest errors of any single-property split {ec} ({', '.join(argc)}) >= {F7_MIN}"
      f" -> {w7c}")
print(f"F7: {w7}  (HOLDS only if both labels hold; the forecast read: \"No single property separates: the best split misclassifies"
      " at least 3 carriers\")")

# ------------------------------------------------------------------------------------------------------------------- A8
print(); print(BAR)
print("A8  was SEC4's family easy?  per family: spread of lambda*_raw, the transferred lambda (SEC4-T's rule), and each arm's"
      " not-behind count")
print(BAR)
print("per carrier: loco = exp(median log lambda*_raw of the other carriers of the study) (unsnapped | snapped to EWC_COARSE);"
      " loco acc = its raw-grid seed mean; nb = not behind the tuned lambda")
print("   REPORT columns (undeclared, post hoc): nf = seeds non-finite at the transferred lambda (recorded as acc 0); div ="
      " sec_lib.diverged() there (a seed < 0.5 tacc, or a non-finite accuracy or record)")
print(f"   {'study':5} {'carrier':34} {'lam*_raw':>10} {'tacc':>8} {'step':>6} {'loco':>9} {'snap':>6} {'loco acc':>8} {'loco st':>8}"
      f" {'nf':>2} {'div':>3}  {'loco':>4} {'SEC':>3} {'clip':>4} {'Lap':>3} {'s1':>3}")
NB = {}
for C in CS:
    k = key(C); la = C["raw"][C["loco"]]
    assert la.mean == C["loco_acc"]
    NB[k] = dict(loco=L.not_behind(C["loco_acc"], C["tacc"], C["step"]), sec=L.arm_nb(C, SEC), lap=L.arm_nb(C, LAP),
                 s1=L.arm_nb(C, S1), clip=L.arm_nb(C, CLIP) if CLIP in C["primary"] else None,
                 nf=sum(not f for f in la.finite), div=L.diverged(la.acc, C["tacc"], la.finite))
    r = NB[k]
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:10.6g} {C['tacc']:8.4f} {C['step']:6.3f} {C['loco_lam']:9.4g}"
          f" {C['loco']:6g} {C['loco_acc']:8.4f} {L.margin_steps(C, C['loco_acc']):+8.3f} {r['nf']:2d} {yn(r['div']):>3}"
          f"  {yn(r['loco']):>4} {yn(r['sec']):>3} {'-' if r['clip'] is None else yn(r['clip']):>4} {yn(r['lap']):>3} {yn(r['s1']):>3}")

print("\nper family (SD of log10 lambda*_raw with ddof 1; counts are not behind / carriers). Declared columns: SD lg lam*, loco nb,"
      " loco share, SEC, s1; REPORT columns (not in A8's list): min / median / max lam*, decades, clip (where recorded), Lap")
print(f"   {'family':6} {'N':>3} {'SD lg lam*':>10} {'min lam*':>10} {'median':>10} {'max lam*':>10} {'decades':>7}"
      f" {'loco nb':>8} {'loco share':>10} {'SEC':>6} {'clip':>6} {'Lap':>6} {'s1':>6}")
SH = {}
for s in L.STUDIES + ("pooled",):
    Cs = CS if s == "pooled" else BY[s]; ks = [key(C) for C in Cs]; n = len(Cs)
    lg = np.log10([C["tuned"] for C in Cs]); lam = [C["tuned"] for C in Cs]
    c = {a: sum(bool(NB[k][a]) for k in ks) for a in ("loco", "sec", "lap", "s1")}
    ncl = [k for k in ks if NB[k]["clip"] is not None]; ccl = sum(NB[k]["clip"] for k in ncl)
    SH[s] = (c["loco"], n)
    print(f"   {s:6} {n:3d} {float(np.std(lg, ddof=1)):10.4f} {min(lam):10.4g} {float(np.median(lam)):10.4g} {max(lam):10.4g}"
          f" {float(lg.max() - lg.min()):7.3f} {c['loco']:>4d}/{n:<3d} {c['loco'] / n:10.4f} {c['sec']:>3d}/{n:<2d}"
          f" {(f'{ccl}/{len(ncl)}' if ncl else '-'):>6} {c['lap']:>3d}/{n:<2d} {c['s1']:>3d}/{n:<2d}")
print(f"   (pooled: SD over all {N} lambda*_raw; each carrier's transferred lambda is still taken within its own study)")

print("\nREPORT (undeclared, post hoc; decides nothing): the transferred lambda's behind cases read as divergence at that lambda")
print(f"   {'family':6} {'loco behind':>11} {'with a non-finite seed':>22} {'non-finite seeds':>16} {'diverged (sec_lib)':>18}"
      "  carriers behind with a non-finite seed (seeds)")
for s in L.STUDIES + ("pooled",):
    Cs = CS if s == "pooled" else BY[s]; B = [key(C) for C in Cs if not NB[key(C)]["loco"]]
    Bn = [k for k in B if NB[k]["nf"] > 0]
    print(f"   {s:6} {len(B):11d} {len(Bn):>18d}/{len(B):<3d} {sum(NB[k]['nf'] for k in B):>11d}/{len(L.SEEDS) * len(B):<4d}"
          f" {sum(NB[k]['div'] for k in B):>14d}/{len(B):<3d}  "
          + (", ".join(f"{k[1]} ({NB[k]['nf']})" for k in Bn) if s != "pooled" else "(the per-family lists)"))

print(f"\nREPORT (undeclared, post hoc; decides nothing): a SEC-T analogue, 'SEC's own saving', on every family. B = the carriers"
      f" where the transferred lambda is behind. SEC-T was registered only")
print(f"   for sec3 (on SEC), sec4 and sec5 (on the clipped SEC), with |B| >= MIN_B = {MIN_B} ({MINB_SRC}; sec4_score and sec5_score"
      f" import it); sec1 and scl3 registered none. A family with |B| < MIN_B is")
print("   marked below the registered minimum and its B counts are not printed. Left: arms not behind on B. Right: where the"
      " transferred lambda is not behind (G), arms that are behind.")
print(f"   {'family':6} {'|B|':>4} {'vs MIN_B':>36} {'SEC nb':>8} {'clip nb':>8} {'Lap nb':>8} {'s1 nb':>8} | {'|G|':>4}"
      f" {'SEC behind':>10} {'clip behind':>11}  carriers in B")
for s in L.STUDIES + ("pooled",):
    Cs = CS if s == "pooled" else BY[s]; ks = [key(C) for C in Cs]
    B = [k for k in ks if not NB[k]["loco"]]; G = [k for k in ks if NB[k]["loco"]]
    Bc = [k for k in B if NB[k]["clip"] is not None]; Gc = [k for k in G if NB[k]["clip"] is not None]
    below = len(B) < MIN_B
    status = f"{len(B)} < {MIN_B}: below the registered minimum" if below else f"{len(B)} >= {MIN_B}"
    if below:
        left = f"{'-':>8} {'-':>8} {'-':>8} {'-':>8}"
    else:
        cB = f"{sum(NB[k]['clip'] for k in Bc)}/{len(Bc)}" if Bc else "-"
        left = (f"{sum(NB[k]['sec'] for k in B):>4d}/{len(B):<3d} {cB:>8} {sum(NB[k]['lap'] for k in B):>4d}/{len(B):<3d}"
                f" {sum(NB[k]['s1'] for k in B):>4d}/{len(B):<3d}")
    cG = f"{sum(not NB[k]['clip'] for k in Gc)}/{len(Gc)}" if Gc else "-"
    print(f"   {s:6} {len(B):4d} {status:>36} {left} | {len(G):4d} {sum(not NB[k]['sec'] for k in G):>6d}/{len(G):<3d} {cG:>11}  "
          + (", ".join(k[1] for k in B) if s != "pooled" else "(the per-family lists; pooled is not a registered set)"))

(k4, n4), (k5, n5) = SH["sec4"], SH["sec5"]; sh4, sh5 = k4 / n4, k5 / n5
f8 = sh4 >= sh5
print(f"\nF8  transferred-lambda not-behind share: sec4 {frac(k4, n4)} >= sec5 {frac(k5, n5)} -> {f8}")
print(f"F8: {word(f8)}  (the forecast read: \"SEC4's family has a transferred-lambda not-behind share at least as high as SEC5's:"
      " part of SEC4's pass is the family's ease\")")
B4 = [key(C) for C in BY["sec4"] if not NB[key(C)]["loco"]]; B5 = [key(C) for C in BY["sec5"] if not NB[key(C)]["loco"]]
print(f"   REPORT: of the transferred lambda's behind cases, with a non-finite seed at that lambda: sec4"
      f" {sum(NB[k]['nf'] > 0 for k in B4)} of {len(B4)}, sec5 {sum(NB[k]['nf'] > 0 for k in B5)} of {len(B5)}"
      " (part of the gap is divergence at the transferred lambda, not where the optimum sits)")

# ------------------------------------------------------------------------------------------------------ Amendment 1 (A12)
print(); print(BAR)
print("Amendment 1 report (POST HOC in origin; 347cb90; decides nothing): F7 (both labels) and F8 with the floor-bound carriers removed")
print(BAR)
print(f"   floor = 100 x the majority class's share of the loaded rows (header class_counts); floor-bound iff tacc - floor <"
      f" {FLOOR_STEPS:g} steps")
FB = {key(C): C["tacc"] - floor_of(C) < FLOOR_STEPS * C["step"] for C in CS}
print(f"   {'study':5} {'carrier':34} {'floor':>8} {'tacc':>8} {'step':>6} {'(tacc-floor)/step':>18}  floor-bound")
for C in CS:
    fl = floor_of(C)
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {fl:8.4f} {C['tacc']:8.4f} {C['step']:6.3f} {(C['tacc'] - fl) / C['step']:+18.3f}"
          f"  {yn(FB[key(C)])}")
print("   floor-bound per study: " + "; ".join(f"{s} {sum(FB[key(C)] for C in BY[s])}/{len(BY[s])}" for s in L.STUDIES)
      + f"; all {sum(FB.values())}/{N}; held-out (SCL3, SEC3, SEC4, SEC5)"
      f" {sum(FB[key(C)] for s in HELD for C in BY[s])}/{sum(len(BY[s]) for s in HELD)}")
print("   AMBIGUITY: the amendment says floor-bound carriers are 'removed' but not whether among all 42 or only among the 30 held-out")
print("   (A12's own counts are pooled over the 30 held-out). The most literal reading, every floor-bound carrier removed (as a1_a3.py")
print("   and a4_a6.py do), is read first; the other, SEC1 kept whole and only the held-out floor-bound carriers removed, is printed beside it.")
print("   The transferred lambda is sec_lib's, from the whole study; only the counts drop carriers.")
AM = {}
for lab, keep in (("all floor-bound removed", lambda C: not FB[key(C)]),
                  ("held-out floor-bound removed, SEC1 kept whole", lambda C: not (FB[key(C)] and C["study"] in HELD))):
    KS = [C for C in CS if keep(C)]; KC = [C for C in KS if CLIP in C["primary"]]
    print(f"\n   {lab}: {len(KS)} carriers (" + ", ".join(f"{s} {sum(C['study'] == s for C in KS)}" for s in L.STUDIES)
          + f"); clipped label on {len(KC)} (" + ", ".join(C["carrier"] for C in KC) + ")")
    yk, _, Rk = a7(KS, SEC, f"   A7 {lab}, label SEC")
    ek, argk = rows_best(Rk, F7_SET); wks, _ = f7_word(yk, ek)
    f7_report_line(f"label SEC {lab}", yk, ek, argk, wks)
    ykc, _, Rkc = a7(KC, CLIP, f"   A7 {lab}, label clipped SEC")
    ekc, argkc = rows_best(Rkc, F7_SET); wkc, _ = f7_word(ykc, ekc)
    f7_report_line(f"label clipped SEC {lab}", ykc, ekc, argkc, wkc)
    wk = combine([wks, wkc])
    print(f"   F7 {lab} (report): {wk}  (FAILS if either label FAILS; UNDEFINED if neither FAILS and one is UNDEFINED)")
    k4k = [key(C) for C in KS if C["study"] == "sec4"]; k5k = [key(C) for C in KS if C["study"] == "sec5"]
    a4 = sum(NB[k]["loco"] for k in k4k); a5 = sum(NB[k]["loco"] for k in k5k)
    if k4k and k5k:
        f8k = a4 / len(k4k) >= a5 / len(k5k); w8k = word(f8k)
        print(f"   F8  sec4 {frac(a4, len(k4k))} >= sec5 {frac(a5, len(k5k))} -> {f8k}")
    else:
        w8k = "UNDEFINED"
        print(f"   F8  a family has no carrier left (sec4 {len(k4k)}, sec5 {len(k5k)}): share undefined")
    print(f"   F8 {lab} (report): {w8k}  (kept: sec4 " + ", ".join(k[1] for k in k4k) + "; sec5 " + ", ".join(k[1] for k in k5k) + ")")
    AM[lab] = dict(n=len(KS), nc=len(KC), clip_set=[key(C) for C in KC], f8_set=(k4k, k5k), w7s=wks, w7c=wkc, w7=wk, w8=w8k,
                   e7=ek, e7c=ekc)
labs = list(AM)
same_c = AM[labs[0]]["clip_set"] == AM[labs[1]]["clip_set"]; same_8 = AM[labs[0]]["f8_set"] == AM[labs[1]]["f8_set"]
print(f"\n   the two readings coincide on the clipped label's carriers: {yn(same_c)}; on F8's carriers: {yn(same_8)}")

print(); print(BAR)
print("summary (words computed above; the declared words are those on all carriers)")
print(f"   F7    {w7}   label SEC {w7s} ({e7} misclassified of {N}, {', '.join(arg7)}; >= {F7_MIN}); label clipped SEC {w7c}"
      f" ({ec} of {len(CC)}, {', '.join(argc)}; >= {F7_MIN}); HOLDS only if both (the most literal reading; the ambiguity is named"
      " above)")
print(f"   F8    {word(f8)}   transferred-lambda not-behind share sec4 {k4}/{n4} = {sh4:.4f} >= sec5 {k5}/{n5} = {sh5:.4f};"
      f" report: behind cases with a non-finite seed at the transferred lambda sec4 {sum(NB[k]['nf'] > 0 for k in B4)} of"
      f" {len(B4)}, sec5 {sum(NB[k]['nf'] > 0 for k in B5)} of {len(B5)}")
print("   Amendment 1 report (post hoc in origin; decides nothing): " + "; ".join(
    f"{lab} ({a['n']} carriers, clipped {a['nc']}): F7 {a['w7']} (SEC {a['w7s']} {a['e7']}, clipped {a['w7c']}), F8 {a['w8']}"
    for lab, a in AM.items()))
print(BAR)
