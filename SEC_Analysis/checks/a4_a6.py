"""SEC_Analysis A4 and A6, with forecasts F4 and F6 (SEC_Analysis/DECLARATION.md at 5f64b5f with Amendments 1 (347cb90) and
2 (e15e1ff); prompt-log entry 257). Amendment 2 adds M5, M6 and A13 and bears on nothing here. Amendment 1's report (F4 and F6
with the floor-bound carriers removed) is printed in its own part after A6, and its words are repeated in the summary line.

POST HOC on SEEN records; no ledger row; no word here is a PASS. It reads the pinned run records through sec_lib.load_all()
(the 42 scored carriers of SEC1, SCL3, SEC3, SEC4 and SEC5; the loader is validated by loader_check.py), trains nothing and
opens no data.

  s          the calibration factor s_j = c_j / rho_j recorded per task j in each record (SEC1's fallback s = 1 when the secant
             is undefined or non-positive; counted as n_fallback). Every s here is read from the unclipped SEC arm
             ('bayes_sec', w = 1/2, primary window fs = fe = 0.1), over all its tasks and all five seeds (DECLARATION.md A4, A6).
  A4         s-bar = the geometric mean of s over the tasks and seeds of the SEC arm, per carrier. Across the 42 carriers:
             Spearman(log10 lambda*_raw, log10(0.5 s-bar)) and the least-squares line log10 lambda*_raw = a + b log10(0.5 s-bar).
             Beside it, the within-carrier SD of log10 s across tasks (per seed, ddof 1, averaged over seeds; sec_lib.s_stats)
             against the between-carrier SD (ddof 1) of the per-carrier mean log10 s.
             F4 HOLDS if Spearman >= 0.6 AND slope in [0.5, 1.5] AND the carriers with median s > 10 are more than half.
             lambda*_raw is sec_lib's tuned lambda (ties to the smallest lambda, the frozen scorers' rule).
  A6         per carrier the maximum and median s; 'diverged' = the unclipped SEC diverged (sec_lib.arm_diverged: a seed below
             0.5 x the tuned raw mean, or a non-finite accuracy or record). F6 HOLDS if the median over the diverged carriers of
             the per-carrier max s is strictly greater than the median over the rest. For the clipped arms (bayes_sec_clip,
             SEC4 and SEC5) the guard firings and the guard margins are printed per carrier.
  guard margin  runs/sec4/frozen/sec4_score.run_guard: m = lr * w * max(imp_used) at each task start after the first, BEFORE the
             guard acts at that start, recorded to 6 dp; the clip fires when m >= kappa (0.5); the penalty step's explicit-Euler
             edge is m = 1. The first start's margin is computed from task-1 state before any guard acts, so by construction
             (run_guard follows SEC1's run() until the first guard: SEC4's D-ID, SEC3's G-ID) it equals the margin the unclipped
             SEC would have at that start. The unclipped 'bayes_sec' records store no guard margins, so this is checked only
             indirectly, where guarded records exist (SEC3, SEC4, SEC5): task 1's s bit-equal in the guarded and the unclipped
             records, and accuracy and every s equal where the guard never fired.
  Amendment 1 (A12)  floor = 100 x the majority class's share of the loaded rows (the header's class_counts); a carrier is
             floor-bound iff tacc - floor < 3 steps (tacc, step: the tuned lambda*_raw's seed mean and step). F4 (a), (b), (c) and
             F6 are recomputed with the floor-bound carriers removed, as a REPORT, post hoc in origin. The amendment does not say
             whether "removed" means the floor-bound carriers among all 42 or only among the 30 held-out ones (A12's own counts
             are pooled over the 30 held-out); the most literal reading, all floor-bound carriers removed (as a1_a3.py does), is
             printed first and the held-out-only reading beside it, with a line naming the ambiguity.

DECLARED LINES (the declaration's A4 and A6 rows); every other line or column is labelled REPORT (not declared; decides nothing):
  A4  the per-carrier lambda*_raw, y, s-bar, x, median s, mean log10 s and SDw columns; the pooled Spearman, slope and the
      intercept of the same fit; the count of carriers with median s > 10; the within-carrier SD of log10 s against the
      between-carrier SD; F4.
  A6  the per-carrier max s and median s, with the divergence label and its inputs (min/tacc, nonfin); the diverged/rest
      comparison of the per-carrier max s and median s; for the clipped arms the per-carrier firings and guard margins (fired,
      starts, per seed, m >= kappa, median m, max m, the first start's margin per seed) and the same firings and margins split
      diverged/rest; F6.
REPORT lines: A4's descriptive columns (tasks, n_s, fb, resid, min s, max s, tie); Spearman's p and Pearson's r; the count of
carriers whose within SD exceeds the between SD; the fallback counts; the per-study tables of A4 and A6; A4's statistics under
other summaries of s (tasks 1..T-1, since the last task's s enters no penalty; the median; task 1's s, computed before any
penalty), none of which is F4 or may be quoted as F4; the declared summary on the carriers not diverged (a post hoc exclusion);
carriers whose raw-grid maximum is tied (lambda*_raw is then a tie-break) and F4's statistics under the largest and the
log-middle tied lambda and with those carriers dropped; A6's median of s-bar, the count of carriers above the rest's median
max s, max s over tasks 1..T-1 and over task 1; the clipped table's m >= 1 and clip nb columns; the first-start margin against
the edge (m >= 1) on the clipped carriers and on the 20 carriers with guarded records; the construction check of the first-start
margin; and the other guarded records (SEC3's guard, SEC4's scale and raw guards, SEC5's kappa 0.25 and 1.0 cells) at the
primary window. The words HOLDS and FAILS are computed here from the printed numbers; F4 and F6 read the declared rows only;
the Amendment 1 words are a report beside them.

    uv run python SEC_Analysis/checks/a4_a6.py > SEC_Analysis/checks/a4_a6.txt
"""
from __future__ import annotations

import math
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

import sec_lib as L  # noqa: E402

D = L.load_all(); BY = L.by_study(D); CS = list(D.values()); N = len(CS)
SEC = "bayes_sec"; CLIP = "bayes_sec_clip"; KAPPA = 0.5; EDGE = 1.0
F4_RHO = 0.6; F4_SLOPE = (0.5, 1.5); F4_MED = 10.0                     # DECLARATION.md F4
FLOOR_STEPS = 3.0                                                       # Amendment 1 (A12): floor-bound iff tacc - floor < 3 steps
TIE_TOL = 1e-9                                                          # points; tied raw-grid means (REPORT only; as a1_a3.py)
HELD = L.STUDIES[1:]                                                    # the 30 held-out carriers (SCL3, SEC3, SEC4, SEC5)
W = 118


def hdr(t):
    print("\n" + "=" * W); print(t); print("=" * W)


def fp(x):                                                              # full precision plus rounded (CLAUDE.md §7)
    return f"{x!r} ({x:.3f})"


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "yes" if b else "no"


def fit(x, y):                                                          # least squares y = a + b x, closed form
    x = np.asarray(x, float); y = np.asarray(y, float); xm, ym = x.mean(), y.mean()
    b = float(((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()); return b, float(ym - b * xm)


def rho(x, y):
    r = spearmanr(x, y); return float(r.statistic), float(r.pvalue)


def s_all(arm, drop_last=False):                                        # every recorded s, seed-major; drop_last: tasks 1..T-1
    return np.array([x for r in arm.recs for x in (r["s"][:-1] if drop_last else r["s"])], float)


def floor_of(C):                                                        # Amendment 1: 100 x the majority class's share
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * max(cc) / sum(cc)


def tied(C):                                                            # raw-grid lambdas tied at the best seed mean (REPORT)
    return [w for w in sorted(C["raw_means"]) if abs(C["raw_means"][w] - C["tacc"]) <= TIE_TOL]


# ---------------------------------------------------------------- per-carrier quantities
R = {}
for C in CS:
    A = C["primary"][SEC]; st = L.s_stats(A); s = np.asarray(st["all"], float)
    assert s.size == len(A.recs) * C["n_tasks"] and np.all(np.isfinite(s)) and np.all(s > 0), (C["study"], C["carrier"])
    sp = s_all(A, drop_last=True); fl = floor_of(C)
    R[(C["study"], C["carrier"])] = dict(
        C=C, st=st, sbar=st["gmean"], x=math.log10(0.5 * st["gmean"]), y=math.log10(C["tuned"]), mlog=float(np.log10(s).mean()),
        med=st["median"], mx=st["max"], mn=st["min"], fb=st["n_fallback"], sdw=st["sd_within"],
        sbar_p=float(10 ** np.log10(sp).mean()), mx_p=float(sp.max()),
        s1max=float(max(r["s"][0] for r in A.recs)), s1g=float(10 ** np.mean([math.log10(r["s"][0]) for r in A.recs])),
        div=L.arm_diverged(C, SEC), div_acc=L.diverged(A.acc, C["tacc"]), minr=float(A.acc.min() / C["tacc"]),
        div_lit=bool(any(a < L.DIV_FRAC * C["tacc"] for a in A.acc)),
        nonfin=sum((not f) or (not np.isfinite(a)) for f, a in zip(A.finite, A.acc)),
        tie=tied(C), floor=fl, fb_floor=C["tacc"] - fl < FLOOR_STEPS * C["step"])
KEYS = list(R)
assert all(R[k]["tie"][0] == R[k]["C"]["tuned"] for k in KEYS)         # lambda*_raw is the smallest tied lambda


def f4_stats(ks, ymap=None):                                            # F4's three statistics on a carrier set; ymap overrides y
    xs = [R[k]["x"] for k in ks]; ys = [(ymap or {}).get(k, R[k]["y"]) for k in ks]
    rv = rho(xs, ys)[0]; bv, av = fit(xs, ys); nm = sum(R[k]["med"] > F4_MED for k in ks)
    return dict(n=len(ks), rho=rv, b=bv, a=av, nmed=nm, c1=rv >= F4_RHO, c2=F4_SLOPE[0] <= bv <= F4_SLOPE[1], c3=nm > len(ks) / 2)


print("=" * W)
print("SEC_Analysis A4 and A6 (SEC_Analysis/DECLARATION.md at 5f64b5f with Amendments 1 (347cb90) and 2 (e15e1ff); prompt-log entry 257)")
print("forecasts F4 and F6; Amendment 1's report (F4 and F6 with the floor-bound carriers removed) after A6; Amendment 2 bears on nothing here")
print("POST HOC on SEEN records; no ledger row. s is read from the unclipped SEC arm (bayes_sec, w = 1/2, fs = fe = 0.1), all tasks, seeds 0-4")
print("lines and columns marked REPORT are not declared and decide nothing; F4 and F6 read the declared rows only")
print("=" * W)
print(f"carriers {N} ({', '.join(f'{s} {len(BY[s])}' for s in L.STUDIES)}); s values per carrier = 5 seeds x tasks; "
      f"s values in all {sum(r['st']['n'] for r in R.values())}")

# ================================================================ A4
hdr("A4  is the calibration a units correction of the raw Fisher?  x = log10(0.5 s-bar), y = log10 lambda*_raw")
print("   s-bar = geometric mean of s over tasks and seeds; SDw = the within-carrier SD of log10 s across tasks (per seed, ddof 1,")
print("   averaged over seeds); mean lg s = the mean log10 s (its SD across carriers is the between-carrier SD)")
print("   REPORT columns (descriptive; decide nothing): tasks, n_s, fb = fallbacks (s = 1) among the carrier's s, resid = y - (a + b x)")
print("   of the pooled fit below, min s, max s, tie = T where the raw-grid maximum is tied (lambda*_raw is then the smallest tied lambda)")
print(f"   {'study':5s} {'carrier':34s} {'tasks':>5s} {'n_s':>4s} {'fb':>3s} {'lambda*_raw':>12s} {'y':>7s} {'s-bar':>11s} {'x':>7s} "
      f"{'resid':>7s} {'median s':>11s} {'min s':>10s} {'max s':>11s} {'mean lg s':>9s} {'SDw':>6s} {'tie':>3s}")
X = np.array([R[k]["x"] for k in KEYS]); Y = np.array([R[k]["y"] for k in KEYS])
b, a = fit(X, Y); rs, ps = rho(X, Y); pr = float(np.corrcoef(X, Y)[0, 1])
for k in KEYS:
    r = R[k]; C = r["C"]
    print(f"   {C['study']:5s} {C['carrier']:34s} {C['n_tasks']:5d} {r['st']['n']:4d} {r['fb']:3d} {C['tuned']:12.6g} {r['y']:+7.3f} "
          f"{r['sbar']:11.5g} {r['x']:+7.3f} {r['y'] - (a + b * r['x']):+7.3f} {r['med']:11.5g} {r['mn']:10.3g} {r['mx']:11.5g} "
          f"{r['mlog']:+9.3f} {r['sdw']:6.3f} {'T' if len(r['tie']) > 1 else '-':>3s}")

print(f"\npooled over {N} carriers:")
print(f"   Spearman(y, x) = {fp(rs)}  (ties in lambda*_raw take average ranks)")
print(f"   least squares y = a + b x: slope b = {fp(b)}, intercept a = {fp(a)}  (lambda*_raw = 10^a (0.5 s-bar)^b)")
n_med = sum(R[k]["med"] > F4_MED for k in KEYS)
print(f"   carriers with median s > {F4_MED:g}: {n_med} of {N} (half is {N / 2:g})")
sdw = np.array([R[k]["sdw"] for k in KEYS]); sdb = float(np.std([R[k]["mlog"] for k in KEYS], ddof=1))
print(f"   within-carrier SD of log10 s: mean {sdw.mean():.3f}, median {np.median(sdw):.3f}, min {sdw.min():.3f}, max {sdw.max():.3f} over {N} carriers; "
      f"between-carrier SD of the mean log10 s {sdb:.3f}; mean within / between {sdw.mean() / sdb:.3f}")
print(f"   REPORT: Spearman's two-sided p {ps:.3g}; Pearson r {pr:.3f}")
print(f"   REPORT: carriers whose within SD exceeds the between SD: {int(np.sum(sdw > sdb))} of {N}")
fbc = [k for k in KEYS if R[k]["fb"]]
print(f"   REPORT: fallbacks (s = 1): {sum(R[k]['fb'] for k in KEYS)} of {sum(R[k]['st']['n'] for k in KEYS)} s values, on {len(fbc)} of {N} carriers: "
      + ", ".join(f"{s}/{c} {R[(s, c)]['fb']}" for s, c in fbc))

print("\nREPORT (not declared; decides nothing), per study (Spearman and fit within the study; SDw mean over its carriers; SDb = between-carrier")
print("SD of the mean log10 s within the study):")
print(f"   {'study':5s} {'N':>3s} {'Spearman':>9s} {'slope':>8s} {'intercept':>9s} {'med s>10':>8s} {'fb':>4s} {'SDw mean':>8s} {'SDb':>6s}"
      f" {'median s-bar':>12s} {'median lambda*':>14s}")
for s in L.STUDIES:
    ks = [k for k in KEYS if k[0] == s]; xs = [R[k]["x"] for k in ks]; ys = [R[k]["y"] for k in ks]; bs, as_ = fit(xs, ys)
    print(f"   {s:5s} {len(ks):3d} {rho(xs, ys)[0]:+9.3f} {bs:+8.3f} {as_:+9.3f} {sum(R[k]['med'] > F4_MED for k in ks):8d} "
          f"{sum(R[k]['fb'] for k in ks):4d} {np.mean([R[k]['sdw'] for k in ks]):8.3f} {np.std([R[k]['mlog'] for k in ks], ddof=1):6.3f}"
          f" {np.median([R[k]['sbar'] for k in ks]):12.5g} {np.median([R[k]['C']['tuned'] for k in ks]):14.6g}")

print("\nREPORT (not declared; decides nothing): the pooled statistics under other summaries of s.")
print("   The last task's s enters no penalty (no task follows it); task 1's s is computed before any penalty acts; a diverged run's")
print("   later s are read after the divergence. No row of this table is F4 and none may be quoted as F4: each summary other than")
print("   the declared one was chosen after the declared one was computed (CLAUDE.md §10), so no threshold is applied to it here.")
print(f"   {'summary of s per carrier':58s} {'N':>3s} {'Spearman':>9s} {'slope':>7s} {'intercept':>9s}")
for lab, xs in (("geometric mean, all tasks and seeds (DECLARED)", X),
                ("geometric mean over tasks 1..T-1", [math.log10(0.5 * R[k]["sbar_p"]) for k in KEYS]),
                ("median, all tasks and seeds", [math.log10(0.5 * R[k]["med"]) for k in KEYS]),
                ("geometric mean of task 1's s over seeds", [math.log10(0.5 * R[k]["s1g"]) for k in KEYS])):
    xs = np.asarray(xs, float); rv = rho(xs, Y)[0]; bv, av = fit(xs, Y)
    print(f"   {lab:58s} {len(xs):3d} {rv:9.4f} {bv:7.3f} {av:+9.3f}")
ND = [k for k in KEYS if not R[k]["div"]]; t_nd = f4_stats(ND)
print(f"   REPORT, a post hoc exclusion (R6 forbids it as an exemption; shown only to read what divergence does to s-bar): the declared")
print(f"   summary on the {t_nd['n']} carriers where the unclipped SEC did not diverge: Spearman {t_nd['rho']:.4f}, slope {t_nd['b']:.3f}, "
      f"intercept {t_nd['a']:+.3f}")

TIE = [k for k in KEYS if len(R[k]["tie"]) > 1]
print(f"\nREPORT (not declared; decides nothing): carriers whose raw-grid maximum is tied within {TIE_TOL:g} points ({len(TIE)} of {N});")
print("   lambda*_raw is then the smallest tied lambda (the frozen scorers' tie-break), so y is a tie-break there, not an identified optimum")
for k in TIE:
    t = R[k]["tie"]; g = sorted(R[k]["C"]["raw_means"]); inside = [w for w in g if t[0] <= w <= t[-1]]
    print(f"   {k[0]}/{k[1]}: {len(t)} tied grid points, lambda in [{t[0]:g}, {t[-1]:g}] ({len(inside) - len(t)} untied grid points"
          f" inside), tied mean {R[k]['C']['tacc']!r}; log-middle {10 ** ((math.log10(t[0]) + math.log10(t[-1])) / 2):.6g}; resid {R[k]['y'] - (a + b * R[k]['x']):+.3f}")
print(f"   {'lambda*_raw on the tied carriers':58s} {'N':>3s} {'Spearman':>9s} {'slope':>7s} {'intercept':>9s}")
for lab, ks, ym in (("smallest tied lambda (DECLARED, the scorers' tie-break)", KEYS, None),
                    ("largest tied lambda", KEYS, {k: math.log10(R[k]["tie"][-1]) for k in TIE}),
                    ("log-middle of the tied range", KEYS, {k: (math.log10(R[k]["tie"][0]) + math.log10(R[k]["tie"][-1])) / 2 for k in TIE}),
                    ("tied carriers dropped (a post hoc exclusion)", [k for k in KEYS if k not in TIE], None)):
    t = f4_stats(ks, ym)
    print(f"   {lab:58s} {t['n']:3d} {t['rho']:9.4f} {t['b']:7.3f} {t['a']:+9.3f}")

c1 = rs >= F4_RHO; c2 = F4_SLOPE[0] <= b <= F4_SLOPE[1]; c3 = n_med > N / 2
print(f"\nF4  (a) Spearman >= {F4_RHO}: {fp(rs)} -> {yn(c1)}; (b) slope in [{F4_SLOPE[0]}, {F4_SLOPE[1]}]: {fp(b)} -> "
      f"{yn(c2)}; (c) median s > {F4_MED:g} on more than half: {n_med} of {N} -> {yn(c3)}")
print(f"F4 {word(c1 and c2 and c3)}  (Amendment 1's report with the floor-bound carriers removed follows A6)")

# ================================================================ A6
hdr("A6  what separates divergence from stability?  s of the unclipped SEC arm; diverged = sec_lib.arm_diverged(C, 'bayes_sec')")
print("   min/tacc = the lowest seed accuracy over the tuned raw mean (diverged below 0.5); nonfin = seeds with a non-finite record")
print("   or accuracy; REPORT columns: max s over tasks 1..T-1 (the s that enter a penalty), max over seeds of task 1's s (computed")
print("   before any penalty)")
print(f"   {'study':5s} {'carrier':34s} {'max s':>11s} {'median s':>11s} {'min/tacc':>8s} {'nonfin':>6s} {'div':>3s} {'| max s 1..T-1':>14s} {'max s_1':>11s}")
for k in KEYS:
    r = R[k]; C = r["C"]
    print(f"   {C['study']:5s} {C['carrier']:34s} {r['mx']:11.5g} {r['med']:11.5g} {r['minr']:8.3f} {r['nonfin']:6d} {'Y' if r['div'] else 'N':>3s}"
          f" | {r['mx_p']:12.5g} {r['s1max']:11.5g}")
assert all(R[k]["div"] == R[k]["div_acc"] for k in KEYS)
dk = [k for k in KEYS if R[k]["div"]]; rk = [k for k in KEYS if not R[k]["div"]]
print(f"\ndiverged (unclipped SEC): {len(dk)} of {N}: " + ", ".join(f"{s}/{c}" for s, c in dk))
print(f"   under accuracy alone (sec_lib.diverged with finite=None: a seed below {L.DIV_FRAC} x tacc or a non-finite accuracy): "
      f"{sum(R[k]['div_acc'] for k in KEYS)} of {N}; under SEC4-2/SEC5-2's literal rule (a seed a with a < {L.DIV_FRAC} x tacc): "
      f"{sum(R[k]['div_lit'] for k in KEYS)} of {N}")


def grp(ks, f):
    return float(np.median([R[k][f] for k in ks])) if ks else float("nan")


print(f"   {'':30s} {'diverged':>12s} {'rest':>12s}")
for f, lab in (("mx", "median of per-carrier max s"), ("med", "median of per-carrier median s"), ("sbar", "REPORT median of s-bar"),
               ("mx_p", "REPORT max s over tasks 1..T-1"), ("s1max", "REPORT max s_1")):
    print(f"   {lab:30s} {grp(dk, f):12.5g} {grp(rk, f):12.5g}")
md, mr = grp(dk, "mx"), grp(rk, "mx")
print(f"   REPORT: carriers with max s above the rest's median ({mr:.5g}): diverged {sum(R[k]['mx'] > mr for k in dk)} of {len(dk)}, "
      f"rest {sum(R[k]['mx'] > mr for k in rk)} of {len(rk)}")

print("\nREPORT (not declared; decides nothing), per study:")
print(f"   {'study':5s} {'N':>3s} {'diverged':>8s} {'median max s (div)':>18s} {'median max s (rest)':>19s}")
for s in L.STUDIES:
    d_ = [k for k in dk if k[0] == s]; r_ = [k for k in rk if k[0] == s]
    print(f"   {s:5s} {len(d_) + len(r_):3d} {len(d_):8d} {grp(d_, 'mx'):18.5g} {grp(r_, 'mx'):19.5g}")

# ---------------------------------------------------------------- the clipped arms (SEC4, SEC5): firings and guard margins
print(f"\nclipped SEC (bayes_sec_clip, kappa {KAPPA}, primary window; SEC4 and SEC5): firings and guard margins per carrier")
print(f"   starts = task starts guarded (tasks - 1 per seed); m >= {KAPPA} counts the margins at or beyond kappa (the firings);")
print("   m first = the first start's margin per seed (computed from task-1 state before any guard acts; by construction the unclipped")
print("   SEC's at that start, checked only indirectly below); div = the unclipped SEC diverged")
print(f"   REPORT columns: m >= {EDGE} counts the margins at or beyond the edge; clip nb = the clipped SEC not behind the tuned lambda")
print(f"   {'study':5s} {'carrier':22s} {'fired':>5s} {'starts':>6s} {'per seed':>15s} {'m>=k':>4s} {'median m':>8s} {'max m':>7s} "
      f"{'m first (seeds 0-4)':>36s} {'div':>3s} | {'m>=1':>4s} {'clip nb':>7s}")
G = {}
for k in KEYS:
    C = R[k]["C"]
    if CLIP not in C["primary"]:
        continue
    A = C["primary"][CLIP]; g = L.guard_stats(A); m = np.array(g["margins"])
    first = [r["guard_margins"][0] for r in A.recs]
    assert g["starts"] == 5 * (C["n_tasks"] - 1) and g["fired"] == int(np.sum(m >= KAPPA)), k
    G[k] = dict(g=g, first=first, nb=L.arm_nb(C, CLIP), ge1=int(np.sum(m >= EDGE)))
    print(f"   {C['study']:5s} {C['carrier']:22s} {g['fired']:5d} {g['starts']:6d} {str(g['per_seed_fired']):>15s} {int(np.sum(m >= KAPPA)):4d} "
          f"{float(np.median(m)):8.4f} {g['max_margin']:7.4f} {' '.join(f'{x:6.3f}' for x in first):>36s} {'Y' if R[k]['div'] else 'N':>3s} | "
          f"{G[k]['ge1']:4d} {'Y' if G[k]['nb'] else 'N':>7s}")
gd = [k for k in G if R[k]["div"]]; gr = [k for k in G if not R[k]["div"]]
print(f"   fired on {sum(G[k]['g']['fired'] > 0 for k in G)} of {len(G)} carriers ({sum(G[k]['g']['fired'] for k in G)} firings); "
      f"on the unclipped-diverged {sum(G[k]['g']['fired'] > 0 for k in gd)} of {len(gd)}, on the rest {sum(G[k]['g']['fired'] > 0 for k in gr)} of {len(gr)}")
print(f"   median of per-carrier max margin: unclipped-diverged {np.median([G[k]['g']['max_margin'] for k in gd]):.4f}, "
      f"rest {np.median([G[k]['g']['max_margin'] for k in gr]):.4f}")
print(f"   REPORT (not declared; the edge m >= {EDGE} is not a declared threshold): any first-start margin >= {EDGE}: diverged "
      f"{sum(max(G[k]['first']) >= EDGE for k in gd)} of {len(gd)}, rest {sum(max(G[k]['first']) >= EDGE for k in gr)} of {len(gr)}")

GP = {k: R[k]["C"]["primary"].get(CLIP) or R[k]["C"]["primary"].get("bayes_sec_g") for k in KEYS}
GP = {k: a for k, a in GP.items() if a is not None}
assert not any("guard_margins" in r for k in GP for r in R[k]["C"]["primary"][SEC].recs)   # the unclipped records store no margins
eq_s1 = sum([r["s"][0] for r in a.recs] == [r["s"][0] for r in R[k]["C"]["primary"][SEC].recs] for k, a in GP.items())
unf = [k for k, a in GP.items() if L.guard_stats(a)["fired"] == 0]
eq_acc = sum(GP[k].acc.tolist() == R[k]["C"]["primary"][SEC].acc.tolist() and [r["s"] for r in GP[k].recs] == [r["s"] for r in R[k]["C"]["primary"][SEC].recs]
             for k in unf)
print(f"   REPORT, a construction check: the first-start margin is computed from task-1 state before any guard acts, so by construction")
print(f"   (D-ID/G-ID) it equals the unclipped SEC's; the unclipped records store no margins, so it is checked only indirectly: task 1's s")
print(f"   bit-equal in the guarded arm (clip, or SEC3's guard) and in the unclipped SEC on every seed on {eq_s1} of {len(GP)} carriers;")
print(f"   where the guard never fired, accuracy and every s equal on {eq_acc} of {len(unf)}")
f1 = {k: max(r["guard_margins"][0] for r in a.recs) for k, a in GP.items()}
g1d = [k for k in GP if R[k]["div"]]; g1r = [k for k in GP if not R[k]["div"]]
print(f"   REPORT (not declared) over the {len(GP)} carriers with guarded records (SEC3's guard included): largest first-start margin >= {EDGE}"
      f" (by construction the unclipped SEC's own, computed before any guard acts): diverged {sum(f1[k] >= EDGE for k in g1d)} of {len(g1d)} "
      f"({', '.join(f'{k[1]} {f1[k]:.3f}' for k in g1d)}), rest {sum(f1[k] >= EDGE for k in g1r)} of {len(g1r)} (largest {max(f1[k] for k in g1r):.3f})")

print(f"\nREPORT (not declared): the other guarded records at the primary window (fired / starts; max margin; first-start margins equal to the"
      f" clipped or guarded arm's primary record)")
for k in KEYS:
    C = R[k]["C"]; rows = []
    for mode in ("bayes_sec_g", "bayes_sec_scale", "bayes_sec_raw", CLIP):
        arms = ([(mode, L.PRIMARY_VALUE[mode], C["primary"][mode])] if mode in C["primary"] and mode != CLIP else []) + \
               [(mode, v, a) for (v, fs, fe), a in sorted(C["cells"].get(mode, {}).items()) if fs == L.FS and fe == L.FE]
        rows += arms
    if not rows:
        continue
    ref = C["primary"].get(CLIP) or C["primary"]["bayes_sec_g"]; f0 = [r["guard_margins"][0] for r in ref.recs]
    print(f"   {C['study']:5s} {C['carrier']:22s} " + "; ".join(
        f"{m} {v:g}: {L.guard_stats(a)['fired']}/{L.guard_stats(a)['starts']}, max {L.guard_stats(a)['max_margin']:.4f}, "
        f"first equal {[r['guard_margins'][0] for r in a.recs] == f0}" for m, v, a in rows)
        + f"; div {'Y' if R[k]['div'] else 'N'}")

f6 = bool(dk) and bool(rk) and md > mr
print(f"\nF6  median of per-carrier max s: diverged ({len(dk)}) {fp(md)} > rest ({len(rk)}) {fp(mr)} -> {yn(md > mr)}")
print(f"F6 {word(f6)}  (Amendment 1's report with the floor-bound carriers removed follows)")

# ================================================================ Amendment 1 (A12): F4 and F6 with the floor-bound carriers removed
hdr("Amendment 1 report (POST HOC in origin; 347cb90; decides nothing): F4 and F6 with the floor-bound carriers removed")
print(f"   floor = 100 x the majority class's share of the loaded rows (header class_counts); floor-bound iff tacc - floor < {FLOOR_STEPS:g} steps")
FBK = [k for k in KEYS if R[k]["fb_floor"]]
print(f"   floor-bound: {len(FBK)} of {N}; per study " + "; ".join(f"{s} {sum(k[0] == s for k in FBK)}/{len(BY[s])}" for s in L.STUDIES)
      + f"; held-out (SCL3, SEC3, SEC4, SEC5) {sum(k[0] in HELD for k in FBK)}/{sum(len(BY[s]) for s in HELD)}")
print(f"   {'study':5s} {'carrier':34s} {'floor':>8s} {'tacc':>8s} {'step':>6s} {'(tacc-floor)/step':>18s} {'div':>3s} {'median s':>11s} {'max s':>11s}")
for k in FBK:
    r = R[k]; C = r["C"]
    print(f"   {C['study']:5s} {C['carrier']:34s} {r['floor']:8.4f} {C['tacc']:8.4f} {C['step']:6.3f} {(C['tacc'] - r['floor']) / C['step']:+18.3f}"
          f" {'Y' if r['div'] else 'N':>3s} {r['med']:11.5g} {r['mx']:11.5g}")
print("   AMBIGUITY: the amendment says floor-bound carriers are 'removed' but not whether among all 42 or only among the 30 held-out")
print("   (A12's own counts are pooled over the 30 held-out). The most literal reading, every floor-bound carrier removed (as a1_a3.py")
print("   does), is read first; the other, SEC1 kept whole and only the held-out floor-bound carriers removed, is printed beside it.")
AM = {}
for lab, ks in (("all floor-bound removed", [k for k in KEYS if not R[k]["fb_floor"]]),
                ("held-out floor-bound removed, SEC1 kept whole", [k for k in KEYS if not (R[k]["fb_floor"] and k[0] in HELD)])):
    t = f4_stats(ks); dk_ = [k for k in ks if R[k]["div"]]; rk_ = [k for k in ks if not R[k]["div"]]
    md_, mr_ = grp(dk_, "mx"), grp(rk_, "mx"); f6_ = bool(dk_) and bool(rk_) and md_ > mr_
    AM[lab] = (t, f6_)
    print(f"\n   {lab}: {t['n']} carriers (" + ", ".join(f"{s} {sum(k[0] == s for k in ks)}" for s in L.STUDIES) + ")")
    print(f"   F4  (a) Spearman >= {F4_RHO}: {fp(t['rho'])} -> {yn(t['c1'])}; (b) slope in [{F4_SLOPE[0]}, {F4_SLOPE[1]}]: {fp(t['b'])} -> "
          f"{yn(t['c2'])} (intercept {t['a']:+.3f}); (c) median s > {F4_MED:g} on more than half: {t['nmed']} of {t['n']} -> {yn(t['c3'])}")
    print(f"   F4 {lab} (report): {word(t['c1'] and t['c2'] and t['c3'])}")
    print(f"   F6  median of per-carrier max s: diverged ({len(dk_)}) {fp(md_) if dk_ else 'none'} > rest ({len(rk_)}) {fp(mr_)} -> "
          f"{yn(f6_)}")
    print(f"   F6 {lab} (report): {word(f6_)}")

print("\n" + "=" * W)
print(f"F4 {word(c1 and c2 and c3)}; F6 {word(f6)}  (the declared words, all {N} carriers)")
print("Amendment 1 report (post hoc in origin; decides nothing): " + "; ".join(
    f"{lab} ({t['n']}): F4 {word(t['c1'] and t['c2'] and t['c3'])}, F6 {word(f6_)}" for lab, (t, f6_) in AM.items()))
