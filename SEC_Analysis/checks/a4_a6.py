"""SEC_Analysis A4 and A6, with forecasts F4 and F6 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257).

POST HOC on SEEN records; no ledger row. It reads the pinned run records through sec_lib.load_all() (the 42 scored carriers of
SEC1, SCL3, SEC3, SEC4 and SEC5; the loader is validated by loader_check.py), trains nothing and opens no data.

  s          the calibration factor s_j = c_j / rho_j recorded per task j in each record (SEC1's fallback s = 1 when the secant
             is undefined or non-positive; counted as n_fallback). Every s here is read from the unclipped SEC arm
             ('bayes_sec', w = 1/2, primary window fs = fe = 0.1), over all its tasks and all five seeds (DECLARATION.md A4, A6).
  A4         s-bar = the geometric mean of s over the tasks and seeds of the SEC arm, per carrier. Across the 42 carriers:
             Spearman(log10 lambda*_raw, log10(0.5 s-bar)) and the least-squares line log10 lambda*_raw = a + b log10(0.5 s-bar).
             Beside it, the within-carrier SD of log10 s across tasks (per seed, ddof 1, averaged over seeds; sec_lib.s_stats)
             against the between-carrier SD (ddof 1) of the per-carrier mean log10 s, and the fallback counts.
             F4 HOLDS if Spearman >= 0.6 AND slope in [0.5, 1.5] AND the carriers with median s > 10 are more than half.
  A6         per carrier the maximum and median s; 'diverged' = the unclipped SEC diverged (sec_lib.arm_diverged: a seed below
             0.5 x the tuned raw mean, or a non-finite accuracy or record). F6 HOLDS if the median over the diverged carriers of
             the per-carrier max s is strictly greater than the median over the rest. For the clipped arms (bayes_sec_clip,
             SEC4 and SEC5) the guard firings and the guard margins are printed per carrier.
  guard margin  runs/sec4/frozen/sec4_score.run_guard: m = lr * w * max(imp_used) at each task start after the first, BEFORE the
             guard acts, recorded to 6 dp; the clip fires when m >= kappa (0.5); the penalty step's explicit-Euler edge is m = 1.
             The first start's margin is computed before any guard can act, so it is the same in every guarded arm and in the
             unclipped SEC run of the same seed (checked below where guarded records exist: SEC3, SEC4, SEC5).
Lines marked REPORT are not declared; they decide nothing: A4's statistics under other summaries of s (tasks 1..T-1, since the
last task's s enters no penalty; the median; task 1's s, computed before any penalty; the carriers not diverged), A6's max s over
tasks 1..T-1 and over task 1, the largest first-start guard margin against the edge on the 20 carriers with guarded records, and
the other guarded records (SEC3's guard, SEC4's scale and raw guards, SEC5's kappa 0.25 and 1.0 cells) at the primary window.
The words HOLDS and FAILS are computed here from the printed numbers; F4 and F6 read the declared rows only.

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
W = 118


def hdr(t):
    print("\n" + "=" * W); print(t); print("=" * W)


def fp(x):                                                              # full precision plus rounded (CLAUDE.md §7)
    return f"{x!r} ({x:.3f})"


def word(ok):
    return "HOLDS" if ok else "FAILS"


def fit(x, y):                                                          # least squares y = a + b x, closed form
    x = np.asarray(x, float); y = np.asarray(y, float); xm, ym = x.mean(), y.mean()
    b = float(((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()); return b, float(ym - b * xm)


def rho(x, y):
    r = spearmanr(x, y); return float(r.statistic), float(r.pvalue)


def s_all(arm, drop_last=False):                                        # every recorded s, seed-major; drop_last: tasks 1..T-1
    return np.array([x for r in arm.recs for x in (r["s"][:-1] if drop_last else r["s"])], float)


# ---------------------------------------------------------------- per-carrier quantities
R = {}
for C in CS:
    A = C["primary"][SEC]; st = L.s_stats(A); s = np.asarray(st["all"], float)
    assert s.size == len(A.recs) * C["n_tasks"] and np.all(np.isfinite(s)) and np.all(s > 0), (C["study"], C["carrier"])
    sp = s_all(A, drop_last=True)
    R[(C["study"], C["carrier"])] = dict(
        C=C, st=st, sbar=st["gmean"], x=math.log10(0.5 * st["gmean"]), y=math.log10(C["tuned"]), mlog=float(np.log10(s).mean()),
        med=st["median"], mx=st["max"], mn=st["min"], fb=st["n_fallback"], sdw=st["sd_within"],
        sbar_p=float(10 ** np.log10(sp).mean()), mx_p=float(sp.max()),
        s1max=float(max(r["s"][0] for r in A.recs)), s1g=float(10 ** np.mean([math.log10(r["s"][0]) for r in A.recs])),
        div=L.arm_diverged(C, SEC), div_acc=L.diverged(A.acc, C["tacc"]), minr=float(A.acc.min() / C["tacc"]),
        nonfin=sum(not f for f in A.finite) + int(np.sum(~np.isfinite(A.acc))))
KEYS = list(R)

print("=" * W)
print("SEC_Analysis A4 and A6 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257): forecasts F4 and F6")
print("POST HOC on SEEN records; no ledger row. s is read from the unclipped SEC arm (bayes_sec, w = 1/2, fs = fe = 0.1), all tasks, seeds 0-4")
print("=" * W)
print(f"carriers {N} ({', '.join(f'{s} {len(BY[s])}' for s in L.STUDIES)}); s values per carrier = 5 seeds x tasks; "
      f"s values in all {sum(r['st']['n'] for r in R.values())}")

# ================================================================ A4
hdr("A4  is the calibration a units correction of the raw Fisher?  x = log10(0.5 s-bar), y = log10 lambda*_raw")
print("   s-bar = geometric mean of s over tasks and seeds; resid = y - (a + b x) of the pooled fit below; SDw = the within-carrier SD of")
print("   log10 s across tasks (per seed, ddof 1, averaged over seeds); fb = fallbacks (s = 1) among the carrier's s")
print(f"   {'study':5s} {'carrier':34s} {'tasks':>5s} {'n_s':>4s} {'fb':>3s} {'lambda*_raw':>12s} {'y':>7s} {'s-bar':>11s} {'x':>7s} "
      f"{'resid':>7s} {'median s':>11s} {'min s':>10s} {'max s':>11s} {'mean lg s':>9s} {'SDw':>6s}")
X = np.array([R[k]["x"] for k in KEYS]); Y = np.array([R[k]["y"] for k in KEYS])
b, a = fit(X, Y); rs, ps = rho(X, Y); pr = float(np.corrcoef(X, Y)[0, 1])
for k in KEYS:
    r = R[k]; C = r["C"]
    print(f"   {C['study']:5s} {C['carrier']:34s} {C['n_tasks']:5d} {r['st']['n']:4d} {r['fb']:3d} {C['tuned']:12.6g} {r['y']:+7.3f} "
          f"{r['sbar']:11.5g} {r['x']:+7.3f} {r['y'] - (a + b * r['x']):+7.3f} {r['med']:11.5g} {r['mn']:10.3g} {r['mx']:11.5g} "
          f"{r['mlog']:+9.3f} {r['sdw']:6.3f}")

print(f"\npooled over {N} carriers:")
print(f"   Spearman(y, x) = {fp(rs)}  (ties in lambda*_raw take average ranks; two-sided p {ps:.3g})")
print(f"   least squares y = a + b x: slope b = {fp(b)}, intercept a = {fp(a)}  (Pearson r {pr:.3f}; lambda*_raw = 10^a (0.5 s-bar)^b)")
n_med = sum(R[k]["med"] > F4_MED for k in KEYS)
print(f"   carriers with median s > {F4_MED:g}: {n_med} of {N} (half is {N / 2:g})")
sdw = np.array([R[k]["sdw"] for k in KEYS]); sdb = float(np.std([R[k]["mlog"] for k in KEYS], ddof=1))
print(f"   within-carrier SD of log10 s: mean {sdw.mean():.3f}, median {np.median(sdw):.3f}, min {sdw.min():.3f}, max {sdw.max():.3f} over {N} carriers; "
      f"between-carrier SD of the mean log10 s {sdb:.3f}; mean within / between {sdw.mean() / sdb:.3f}")
print(f"   carriers whose within SD exceeds the between SD: {int(np.sum(sdw > sdb))} of {N}")
fbc = [k for k in KEYS if R[k]["fb"]]
print(f"   fallbacks (s = 1): {sum(R[k]['fb'] for k in KEYS)} of {sum(R[k]['st']['n'] for k in KEYS)} s values, on {len(fbc)} of {N} carriers: "
      + ", ".join(f"{s}/{c} {R[(s, c)]['fb']}" for s, c in fbc))

print("\nper study (Spearman and fit within the study; SDw mean over its carriers; SDb = between-carrier SD of the mean log10 s within the study):")
print(f"   {'study':5s} {'N':>3s} {'Spearman':>9s} {'slope':>8s} {'intercept':>9s} {'med s>10':>8s} {'fb':>4s} {'SDw mean':>8s} {'SDb':>6s}"
      f" {'median s-bar':>12s} {'median lambda*':>14s}")
for s in L.STUDIES:
    ks = [k for k in KEYS if k[0] == s]; xs = [R[k]["x"] for k in ks]; ys = [R[k]["y"] for k in ks]; bs, as_ = fit(xs, ys)
    print(f"   {s:5s} {len(ks):3d} {rho(xs, ys)[0]:+9.3f} {bs:+8.3f} {as_:+9.3f} {sum(R[k]['med'] > F4_MED for k in ks):8d} "
          f"{sum(R[k]['fb'] for k in ks):4d} {np.mean([R[k]['sdw'] for k in ks]):8.3f} {np.std([R[k]['mlog'] for k in ks], ddof=1):6.3f}"
          f" {np.median([R[k]['sbar'] for k in ks]):12.5g} {np.median([R[k]['C']['tuned'] for k in ks]):14.6g}")

print("\nREPORT (not declared; decides nothing; F4's word is the declared row's): the pooled statistics under other summaries of s.")
print("   The last task's s enters no penalty (no task follows it); task 1's s is computed before any penalty acts; a diverged run's")
print("   later s are read after the divergence.")
print(f"   {'summary of s per carrier':58s} {'N':>3s} {'Spearman':>9s} {'slope':>7s} {'intercept':>9s} {'(a)':>4s} {'(b)':>4s}")
ND = [i for i, k in enumerate(KEYS) if not R[k]["div"]]
for lab, xs, idx in (("geometric mean, all tasks and seeds (DECLARED)", X, None),
                     ("geometric mean over tasks 1..T-1", [math.log10(0.5 * R[k]["sbar_p"]) for k in KEYS], None),
                     ("median, all tasks and seeds", [math.log10(0.5 * R[k]["med"]) for k in KEYS], None),
                     ("geometric mean of task 1's s over seeds", [math.log10(0.5 * R[k]["s1g"]) for k in KEYS], None),
                     ("geometric mean, all tasks; carriers not diverged", X, ND)):
    xs = np.asarray(xs, float); ys = Y
    if idx is not None: xs, ys = xs[idx], Y[idx]
    rv = rho(xs, ys)[0]; bv, av = fit(xs, ys)
    print(f"   {lab:58s} {len(xs):3d} {rv:9.4f} {bv:7.3f} {av:+9.3f} {'yes' if rv >= F4_RHO else 'no':>4s} "
          f"{'yes' if F4_SLOPE[0] <= bv <= F4_SLOPE[1] else 'no':>4s}")

c1 = rs >= F4_RHO; c2 = F4_SLOPE[0] <= b <= F4_SLOPE[1]; c3 = n_med > N / 2
print(f"\nF4  (a) Spearman >= {F4_RHO}: {fp(rs)} -> {'yes' if c1 else 'no'}; (b) slope in [{F4_SLOPE[0]}, {F4_SLOPE[1]}]: {fp(b)} -> "
      f"{'yes' if c2 else 'no'}; (c) median s > {F4_MED:g} on more than half: {n_med} of {N} -> {'yes' if c3 else 'no'}")
print(f"F4 {word(c1 and c2 and c3)}")

# ================================================================ A6
hdr("A6  what separates divergence from stability?  s of the unclipped SEC arm; diverged = sec_lib.arm_diverged(C, 'bayes_sec')")
print("   min/tacc = the lowest seed accuracy over the tuned raw mean (diverged below 0.5); nonfin = non-finite seeds or records;")
print("   REPORT columns: max s over tasks 1..T-1 (the s that enter a penalty), max over seeds of task 1's s (computed before any penalty)")
print(f"   {'study':5s} {'carrier':34s} {'max s':>11s} {'median s':>11s} {'min/tacc':>8s} {'nonfin':>6s} {'div':>3s} {'| max s 1..T-1':>14s} {'max s_1':>11s}")
for k in KEYS:
    r = R[k]; C = r["C"]
    print(f"   {C['study']:5s} {C['carrier']:34s} {r['mx']:11.5g} {r['med']:11.5g} {r['minr']:8.3f} {r['nonfin']:6d} {'Y' if r['div'] else 'N':>3s}"
          f" | {r['mx_p']:12.5g} {r['s1max']:11.5g}")
assert all(R[k]["div"] == R[k]["div_acc"] for k in KEYS)
dk = [k for k in KEYS if R[k]["div"]]; rk = [k for k in KEYS if not R[k]["div"]]
print(f"\ndiverged (unclipped SEC): {len(dk)} of {N}: " + ", ".join(f"{s}/{c}" for s, c in dk))
print(f"   the same {len(dk)} under the accuracy-only rule (sec_lib.diverged with finite=None, SEC4-2/SEC5-2's): "
      f"{sum(R[k]['div_acc'] for k in KEYS)} of {N}")


def grp(ks, f):
    return float(np.median([R[k][f] for k in ks])) if ks else float("nan")


print(f"   {'':30s} {'diverged':>12s} {'rest':>12s}")
for f, lab in (("mx", "median of per-carrier max s"), ("med", "median of per-carrier median s"), ("sbar", "median of s-bar"),
               ("mx_p", "REPORT max s over tasks 1..T-1"), ("s1max", "REPORT max s_1")):
    print(f"   {lab:30s} {grp(dk, f):12.5g} {grp(rk, f):12.5g}")
md, mr = grp(dk, "mx"), grp(rk, "mx")
print(f"   carriers with max s above the rest's median ({mr:.5g}): diverged {sum(R[k]['mx'] > mr for k in dk)} of {len(dk)}, "
      f"rest {sum(R[k]['mx'] > mr for k in rk)} of {len(rk)}")

print("\nper study:")
print(f"   {'study':5s} {'N':>3s} {'diverged':>8s} {'median max s (div)':>18s} {'median max s (rest)':>19s}")
for s in L.STUDIES:
    d_ = [k for k in dk if k[0] == s]; r_ = [k for k in rk if k[0] == s]
    print(f"   {s:5s} {len(d_) + len(r_):3d} {len(d_):8d} {grp(d_, 'mx'):18.5g} {grp(r_, 'mx'):19.5g}")

# ---------------------------------------------------------------- the clipped arms (SEC4, SEC5): firings and guard margins
print(f"\nclipped SEC (bayes_sec_clip, kappa {KAPPA}, primary window; SEC4 and SEC5): firings and guard margins per carrier")
print(f"   starts = task starts guarded (tasks - 1 per seed); m >= {KAPPA} and m >= {EDGE} count the margins at or beyond kappa and the edge;")
print("   m first = the first start's margin per seed (the same in the unclipped SEC run); div = the unclipped SEC diverged")
print(f"   {'study':5s} {'carrier':22s} {'fired':>5s} {'starts':>6s} {'per seed':>15s} {'m>=k':>4s} {'m>=1':>4s} {'median m':>8s} {'max m':>7s} "
      f"{'m first (seeds 0-4)':>36s} {'clip nb':>7s} {'div':>3s}")
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
          f"{G[k]['ge1']:4d} {float(np.median(m)):8.4f} {g['max_margin']:7.4f} {' '.join(f'{x:6.3f}' for x in first):>36s} "
          f"{'Y' if G[k]['nb'] else 'N':>7s} {'Y' if R[k]['div'] else 'N':>3s}")
gd = [k for k in G if R[k]["div"]]; gr = [k for k in G if not R[k]["div"]]
print(f"   fired on {sum(G[k]['g']['fired'] > 0 for k in G)} of {len(G)} carriers ({sum(G[k]['g']['fired'] for k in G)} firings); "
      f"on the unclipped-diverged {sum(G[k]['g']['fired'] > 0 for k in gd)} of {len(gd)}, on the rest {sum(G[k]['g']['fired'] > 0 for k in gr)} of {len(gr)}")
print(f"   median of per-carrier max margin: unclipped-diverged {np.median([G[k]['g']['max_margin'] for k in gd]):.4f}, "
      f"rest {np.median([G[k]['g']['max_margin'] for k in gr]):.4f}; any first-start margin >= {EDGE}: diverged "
      f"{sum(max(G[k]['first']) >= EDGE for k in gd)} of {len(gd)}, rest {sum(max(G[k]['first']) >= EDGE for k in gr)} of {len(gr)}")

GP = {k: R[k]["C"]["primary"].get(CLIP) or R[k]["C"]["primary"].get("bayes_sec_g") for k in KEYS}
GP = {k: a for k, a in GP.items() if a is not None}
eq_s1 = sum([r["s"][0] for r in a.recs] == [r["s"][0] for r in R[k]["C"]["primary"][SEC].recs] for k, a in GP.items())
unf = [k for k, a in GP.items() if L.guard_stats(a)["fired"] == 0]
eq_acc = sum(GP[k].acc.tolist() == R[k]["C"]["primary"][SEC].acc.tolist() and [r["s"] for r in GP[k].recs] == [r["s"] for r in R[k]["C"]["primary"][SEC].recs]
             for k in unf)
print(f"   the first start precedes any guard action: task 1's s equal in the guarded arm (clip, or SEC3's guard) and in the unclipped SEC on every"
      f" seed on {eq_s1} of {len(GP)} carriers; where the guard never fired, accuracy and every s equal on {eq_acc} of {len(unf)}")
f1 = {k: max(r["guard_margins"][0] for r in a.recs) for k, a in GP.items()}
g1d = [k for k in GP if R[k]["div"]]; g1r = [k for k in GP if not R[k]["div"]]
print(f"   REPORT (not declared) over the {len(GP)} carriers with guarded records (SEC3's guard included): largest first-start margin >= {EDGE}"
      f" (the unclipped SEC's own, before any penalty step): diverged {sum(f1[k] >= EDGE for k in g1d)} of {len(g1d)} "
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

print(f"\nF6  median of per-carrier max s: diverged ({len(dk)}) {fp(md)} > rest ({len(rk)}) {fp(mr)} -> {'yes' if md > mr else 'no'}")
print(f"F6 {word(bool(dk) and bool(rk) and md > mr)}")
print("\n" + "=" * W)
print(f"F4 {word(c1 and c2 and c3)}; F6 {word(bool(dk) and bool(rk) and md > mr)}")
