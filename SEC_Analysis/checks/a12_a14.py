"""SEC_Analysis A12, A13 and A14, with forecasts F12, F13 and F14 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; A12 and F12
from its Amendment 1 (347cb90), A13 and F13 from its Amendment 2 (e15e1ff), A14 and F14 from its Amendment 3 (34b4765); prompt-log
entry 257). The declaration: "A12 (Amendment 1) and A13 (Amendment 2) are scripted with A14 in checks/a12_a14.py."

POST HOC in origin (Amendments 1-3); declared checks on seen records; no ledger row; no word here is a PASS. Every carrier read
here was opened by SEC1, SCL3, SEC3, SEC4 or SEC5 (and again by the M runs and SEC6's development stage) before this file was
written. It trains nothing and opens no data. It reads, and nothing else:
  runs/{sec1,scl3,sec3,sec4,sec5}/results_*.jsonl   through sec_lib.load_all() (validated first: loader_check.txt, every pinned
                                                    count REPRODUCED): the 42 scored carriers, their headers, tuned lambda*_raw,
                                                    tacc, step, the primary arms and the transferred lambda (sec_lib's loco)
  SEC_Analysis/checks/m_runs/*.jsonl                the M records (C0 the clipped SEC and M6 EDGE; seeds 0-4) through
                                                    m_checks._read_mruns() (m_checks.py is imported, never run or edited);
                                                    m_checks.json is read only to cross-check C0's capped fractions
  prereg/sec6/dev/{dev,devsi1c,devfclip}_<study>_<id>.jsonl   SEC6's development records (read-only): AR1-B ('ar1b' in dev_*),
                                                    SI-1C ('si1c' in devsi1c_*) and the fixed_clip grid (devfclip_*)
  prereg/sec6/dev_SEC6.txt                          only to check that the A13 counts reproduce SEC6's development report
  SEC_Analysis/checks/{a1_a3,a4_a6,a5_a9_a10,a7_a8,a11_grade}.txt   only to cite where Amendment 1's floor-bound-removed reports
                                                    of F1-F11 are already printed (no duplication: nothing is recomputed here)

DEFINITIONS (the declaration's, read literally; tacc, step: the tuned lambda*_raw's seed mean and max(1, 2 SE), sec_lib's)
  floor          100 x max(class_counts) / n, class_counts the header's used counts (asserted: sum == n)
  floor-bound    tacc - floor < 3 steps (strict), the definition of the Amendment 1 reports in a1_a3.py, a4_a6.py, a5_a9_a10.py
  task-1 share   100 x (the sum of the two largest used class counts) / n. The frozen loader ranks classes by count and relabels
                 them in that order (runs/sec5/frozen/scl3_score.py select_classes), and SEC1's tasks are consecutive label pairs;
                 checked here from the headers: class_counts is non-increasing and per_task == 2 on every carrier, so these two
                 counts are task 1's (a tie at ranks 2/3 changes which class is in task 1, never the share).
  not behind     arm - tacc > -step (strict; sec_lib.not_behind), an arm's value its seed mean over seeds 0-4
  A12            per study (SCL3, SEC3, SEC4, SEC5) and pooled over those 30 held-out carriers: the number floor-bound, and the
                 not-behind rates (k/n) of the unclipped SEC ('bayes_sec'), the clipped SEC ('bayes_sec_clip', SEC4 and SEC5 only,
                 14 carriers), raw Laplace ('bayes') and the transferred lambda (sec_lib's loco_acc) on the floor-bound carriers
                 and on the rest (the held-out carriers that are not floor-bound).
                 F12 HOLDS iff (a) 4 x (floor-bound among the 30) >= 30 ("at least a quarter") AND (b) the unclipped SEC's
                 not-behind rate on the floor-bound held-out carriers > its rate on the rest (strict).
                 Amendment 1's "every forecast F1-F11 whose decisive count includes floor-bound carriers is also printed with them
                 removed" is already done by the scripts that decide F1-F11; this script finds each such line in their pinned
                 outputs and cites file and line (it stops with an error if one is missing). Nothing is reprinted.
  A13            on the 30 SEEN carriers of the M runs (SCL3, SEC3, SEC4, SEC5):
                 tuned clipped lambda  the best seed mean over the fixed_clip grid of devfclip_* (values sorted ascending, Python
                                       max: ties to the smallest lambda, the tuned lambda's own rule); tacc_c its seed mean;
                                       step_c = max(1, 2 SE) of its five seeds (sec_lib.step_of). Checked against the record's
                                       own 'tuned', 'acc' and 'step' fields.
                 not behind the tuned lambda (a - tacc > -step) and not behind the tuned clipped lambda (a - tacc_c > -step_c) for
                 SI-1C, AR1-B and the clipped SEC. The clipped SEC is C0 read from m_runs on all 30 carriers; on the 14 SEC4 and
                 SEC5 carriers C0 is checked seed for seed against the pinned 'bayes_sec_clip' (equal on all 14 means the counts are
                 the same whichever of the two is read there); SCL3 and SEC3 have no pinned 'bayes_sec_clip' in runs/, so C0 is the
                 only record there (a REPORT compares it with the reference SEC6's development records carry).
                 The tuned clipped lambda against the unclipped tuned lambda: ahead iff tacc_c - tacc > step, behind iff
                 tacc - tacc_c > step (strict; step the unclipped tuned lambda's).
                 The fraction of capped coordinates: C0's frac_capped from m_runs (per guarded task start; 0 where the clip did not
                 fire), mean and max over task starts and seeds, per carrier (cross-checked against m_checks.json).
                 F13 HOLDS iff the tuned clipped lambda is ahead by more than a step on at least a third of the 30 (3 x count >= 30).
  A14            over the 30 carriers of the M runs: Spearman (scipy.stats.spearmanr; average ranks for ties) of M6's seed-mean
                 accuracy with the task-1 share; over all 42: Spearman of SEC's margin in steps, (bayes_sec - tacc) / step, with
                 the task-1 share; the same for the clipped SEC (pinned 'bayes_sec_clip', 14) and for C0 (m_runs, 30), each margin
                 over the unclipped tuned lambda in its step.
                 F14 HOLDS iff Spearman(M6 accuracy, share) >= 0.8 AND Spearman(SEC margin, share) > 0.
AMBIGUITIES, each resolved by the most literal reading and named in a printed line: A12's "per study" (the four held-out studies;
SEC1 is printed as a REPORT line outside the pool); F12's "the rest" (the held-out carriers that are not floor-bound); A13's "C0
from m_runs or the pinned bayes_sec_clip" (m_runs on all 30, the pinned record checked equal where it exists); A14's task-1 share
over n (all loaded rows, as declared; the test split's share is a REPORT); A14's margins of the clipped SEC and C0 (over the
unclipped tuned lambda, as SEC's).
REPORT lines (not declared; they decide nothing): the per-carrier table's columns beyond the declared ones (n, (tacc - floor) / step,
the clipped SEC's and C0's margins, the not-behind flags); the test split's task-1 share; A12's SEC1 row and its all-42 row; the
dev records' 'tuned' field against sec_lib's tie rule; C0 against the clipped-SEC reference of SEC6's development records on SCL3 and
SEC3; the tuned clipped lambda at the top of its grid; the capped fraction over the starts where the clip fired only; the firings
at the ahead carriers; the reproduction of SEC6's development counts; Spearman's p-values, the SEC margin over the 30 only, M6's
margin and Spearman(M6 accuracy, floor). Accuracies are the records' (per cent; a non-finite run is recorded as 0).
The words HOLDS and FAILS are computed here from the printed numbers (R15).

    uv run python SEC_Analysis/checks/a12_a14.py > SEC_Analysis/checks/a12_a14.txt
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

import sec_lib as L  # noqa: E402
import m_checks as M  # noqa: E402  (imported for its reader _read_mruns only; never run, never edited)

ROOT = L.ROOT
D = L.load_all(); BY = L.by_study(D); CS = list(D.values()); N = len(CS)
SEC, CLIP, LAP = "bayes_sec", "bayes_sec_clip", "bayes"
HELD = ("scl3", "sec3", "sec4", "sec5")                       # the 30 held-out carriers (A12) = the 30 carriers of the M runs
FLOOR_STEPS = 3.0                                             # Amendment 1: floor-bound iff tacc - floor < 3 steps
F12_QUARTER = 4                                               # F12 (a): 4 x floor-bound >= 30
F13_THIRD = 3                                                 # F13: 3 x ahead >= 30
F14_RHO = 0.8                                                 # F14 (a): Spearman(M6 accuracy, share) >= 0.8
DEV = os.path.join(ROOT, "prereg", "sec6", "dev")
DEV_RE = re.compile(r"^(dev|devsi1c|devfclip)_(scl3|sec3|sec4|sec5)_(\d+)\.jsonl$")
BAR = "=" * 150


def hdr(t):
    print("\n" + BAR); print(t); print(BAR)


def word(ok):
    return "HOLDS" if ok else "FAILS"


def yn(b):
    return "Y" if b else "N"


def rate(k, n):
    return f"{k}/{n} = {k / n!r} ({k / n:.3f})" if n else f"{k}/0 (undefined)"


def short(k, n):
    return f"{k}/{n}" + (f" ({k / n:.3f})" if n else " (undef)")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def group_sha(paths):
    """One sha256 over the sorted (relative path, sha256) lines of a group of input files."""
    lines = "".join(f"{os.path.relpath(p, ROOT)}  {sha256(p)}\n" for p in sorted(paths))
    return hashlib.sha256(lines.encode()).hexdigest()


def key(C):
    return (C["study"], C["carrier"])


# ============================================================================================================== definitions
def floor_of(C):
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * max(cc) / C["n"]


def share_of(C):
    cc = C["class_counts"]
    assert sum(cc) == C["n"], (C["carrier"], sum(cc), C["n"])
    return 100.0 * sum(sorted(cc, reverse=True)[:2]) / C["n"]


def test_share_of(C):
    """REPORT: the task-1 share of the stratified test split (sec1_score.split_standardise: n_te = int(round(0.2 n_c)) per class)."""
    te = [int(round(L.TEST_FRAC * c)) for c in C["class_counts"]]
    assert sum(te) == C["n_test"], (C["carrier"], sum(te), C["n_test"])
    return 100.0 * sum(sorted(te, reverse=True)[:2]) / sum(te)


FLOOR = {key(C): floor_of(C) for C in CS}
SHARE = {key(C): share_of(C) for C in CS}
FB = {key(C): C["tacc"] - FLOOR[key(C)] < FLOOR_STEPS * C["step"] for C in CS}
DESC = {key(C): all(a >= b for a, b in zip(C["class_counts"], C["class_counts"][1:])) for C in CS}
PT2 = {key(C): C["per_task"] == 2 for C in CS}
TIE23 = [key(C) for C in CS if len(C["class_counts"]) > 2 and C["class_counts"][1] == C["class_counts"][2]]

# ============================================================================================================== the M records
R, MH, MF = M._read_mruns()
MK = [key(C) for C in CS if C["study"] in HELD]
assert sorted(R) == sorted(MK), (sorted(set(R) ^ set(MK)))
assert all(set(R[k]) >= {"C0", "M6"} for k in MK)
MEAN = {k: {a: float(np.mean([r["acc"] for r in R[k][a]])) for a in ("C0", "M6")} for k in MK}
MJ = json.load(open(os.path.join(HERE, "m_checks.json")))

# ============================================================================================================== SEC6's dev records
DEVF = {}
for fn in sorted(os.listdir(DEV)):
    m = DEV_RE.match(fn)
    if m:
        DEVF.setdefault((m.group(2), int(m.group(3))), {})[m.group(1)] = os.path.join(DEV, fn)
DEVR = {}                                                     # (study, carrier) -> {"dev": rec, "devsi1c": rec, "devfclip": rec}
n_excl = 0
for (st, did), files in sorted(DEVF.items()):
    recs = {}
    for kind, p in files.items():
        lines = [ln for ln in open(p) if ln.strip()]
        assert len(lines) == 1, p
        recs[kind] = json.loads(lines[0])
    if any(r.get("excluded") for r in recs.values()):
        assert all(r.get("excluded") for r in recs.values()), (st, did); n_excl += 1
        continue
    names = {r["name"] for r in recs.values()}
    assert len(names) == 1 and set(recs) == {"dev", "devsi1c", "devfclip"}, (st, did, names, set(recs))
    DEVR[(st, names.pop())] = recs
assert sorted(DEVR) == sorted(MK), sorted(set(DEVR) ^ set(MK))


def tuned_clip(fc):
    """The tuned clipped lambda from the fixed_clip grid: values ascending, Python max (ties to the smallest lambda)."""
    grid = sorted(fc["grid"], key=lambda g: g["value"])
    vals = [g["value"] for g in grid]
    assert all(a < b for a, b in zip(vals, vals[1:])), vals
    assert all(len(g["seeds"]) == 5 for g in grid)
    means = {g["value"]: float(np.mean(np.asarray(g["seeds"], dtype=float))) for g in grid}
    t = max(means, key=means.get)
    g = next(x for x in grid if x["value"] == t)
    return dict(lam=t, acc=means[t], seeds=list(map(float, g["seeds"])), step=L.step_of(np.asarray(g["seeds"], dtype=float)),
                fired=list(g["fired"]), top=t == vals[-1], n_grid=len(grid), nonfinite=sum(x["nonfinite"] for x in grid),
                rec_same=(t == fc["tuned"] and means[t] == fc["acc"] and L.step_of(np.asarray(g["seeds"], dtype=float)) == fc["step"]))


def arm_mean(a):
    m = float(np.mean(np.asarray(a["seeds"], dtype=float)))
    assert m == a["acc"], (m, a["acc"])
    return m


A13 = {}
for k in MK:
    C = D[k]; rr = DEVR[k]
    for kind in ("dev", "devsi1c", "devfclip"):
        assert rr[kind]["tacc"] == C["tacc"] and rr[kind]["step"] == C["step"], (k, kind)
    tc = tuned_clip(rr["devfclip"]["arms"]["fixed_clip"])
    c0 = R[k]["C0"]
    fc = [x for r in c0 for x in r["frac_capped"]]
    fired_fc = [x for x in fc if x > 0]                       # a firing caps at least the largest coordinate; 0 where it did not fire
    assert len(fired_fc) == sum(r["guard_fired"] for r in c0), (k, len(fired_fc))
    assert all(len(r["frac_capped"]) == len(r["guard_margins"]) for r in c0), k
    A13[k] = dict(C=C, tc=tc, si1c=arm_mean(rr["devsi1c"]["arms"]["si1c"]), ar1b=arm_mean(rr["dev"]["arms"]["ar1b"]),
                  c0=MEAN[k]["C0"], cap_mean=float(np.mean(fc)), cap_max=float(np.max(fc)),
                  cap_fired=float(np.mean(fired_fc)) if fired_fc else None, n_fired=len(fired_fc),
                  seeds_fired=sum(r["guard_fired"] > 0 for r in c0), fired=sum(r["guard_fired"] for r in c0),
                  dev_tuned=rr["dev"]["tuned"], ref_clip=rr["dev"]["ref"]["clip"])

# ============================================================================================================== header
print(BAR)
print("SEC_Analysis A12, A13, A14 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; Amendment 1 (347cb90): A12, F12; Amendment 2 (e15e1ff):"
      " A13, F13; Amendment 3 (34b4765): A14, F14; prompt-log entry 257)")
print("POST HOC in origin (Amendments 1-3); declared checks on seen records; no ledger row; the words are HOLDS / FAILS against the"
      " declared forecasts, never PASS")
print(BAR)
print(f"carriers: {N} (" + ", ".join(f"{s} {len(BY[s])}" for s in L.STUDIES) + f"); held-out (A12) = the carriers of the M runs (A13, A14):"
      f" {len(MK)} ({'+'.join(HELD)})")
print("step = the carrier's step at lambda*_raw, max(1, 2 SE over seeds); not behind = arm - tacc > -step (strict); points are per cent"
      " accuracy; margins in steps are (arm - tacc) / step")
print("inputs (sha256 over the sorted 'path  sha256' lines of each group):")
print(f"   runs/*/results_*.jsonl read by sec_lib ({sum(len(L._paths(s)) for s in L.STUDIES)} files): "
      f"{group_sha([p for s in L.STUDIES for p in L._paths(s)])}")
MR_PATHS = [os.path.join(M.MRUNS, fn) for fn, _ in MF]
print(f"   SEC_Analysis/checks/m_runs/*.jsonl ({len(MR_PATHS)} files): {group_sha(MR_PATHS)}")
DEV_PATHS = [p for fs in DEVF.values() for p in fs.values()]
print(f"   prereg/sec6/dev/{{dev,devsi1c,devfclip}}_*.jsonl ({len(DEV_PATHS)} files; {n_excl} loader-excluded carriers x 3 carry only a"
      f" header): {group_sha(DEV_PATHS)}")
print(f"   SEC_Analysis/checks/m_checks.json {sha256(os.path.join(HERE, 'm_checks.json'))}; uv.lock {sha256(os.path.join(ROOT, 'uv.lock'))}")

# ============================================================================================================== definitions check
hdr("DEFINITIONS  floor = 100 max(class_counts) / n; floor-bound iff tacc - floor < 3 steps; task-1 share = 100 (two largest counts) / n")
print(f"   header class_counts: sum == n on {sum(sum(C['class_counts']) == C['n'] for C in CS)}/{N} (asserted); non-increasing on"
      f" {sum(DESC.values())}/{N}; per_task == 2 on {sum(PT2.values())}/{N}")
ok_def = all(DESC.values()) and all(PT2.values())
print("   -> " + ("class_counts is in descending (non-increasing) order in every header and every task holds 2 classes, so the two largest"
                  " used counts are task 1's (labels 0 and 1), as the frozen loader's ranking implies" if ok_def else
                  "NOT VERIFIED: the two largest counts are not task 1's on every carrier (the share is still computed as declared)"))
print(f"   carriers whose 2nd and 3rd counts tie ({len(TIE23)}; the loader's tie-break by class decides which class is in task 1; the"
      f" share is the same): " + ", ".join(f"{s}:{c}" for s, c in TIE23))
dts = max(abs(SHARE[key(C)] - test_share_of(C)) for C in CS)
print(f"   REPORT: largest |task-1 share over n - task-1 share of the stratified test split| over the {N} carriers: {dts!r} ({dts:.4f}) points")
print("   AMBIGUITY (A14): the task-1 share is read over n, all loaded rows, as declared; the test split's share is the REPORT above only")

# ============================================================================================================== per-carrier table
hdr("PER CARRIER  (all 42; M6 and C0 from m_runs on the 30 held-out carriers, '-' elsewhere; clip = the pinned bayes_sec_clip, SEC4 and SEC5)")
print(f"   {'study':5} {'carrier':34} {'K':>3} {'n':>6} {'floor':>8} {'share':>8} {'tacc':>8} {'step':>7} {'(t-fl)/st':>9} {'fb':>2}"
      f" {'M6 acc':>8} {'C0 acc':>8} {'SEC st':>8} {'clip st':>8} {'C0 st':>8} | nb: SEC clip Lap tr")
for C in CS:
    k = key(C); P = C["primary"]; held = k in MEAN; NA = f"{'-':>8}"
    ms = lambda a: f"{L.margin_steps(C, a):+8.3f}"  # noqa: E731
    nbf = lambda m: yn(L.arm_nb(C, m)) if m in P else "-"  # noqa: E731
    m6_s = f"{MEAN[k]['M6']:8.4f}" if held else NA
    c0_s = f"{MEAN[k]['C0']:8.4f}" if held else NA
    c0_m = ms(MEAN[k]["C0"]) if held else NA
    cl_m = ms(P[CLIP].mean) if CLIP in P else NA
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['K']:3d} {C['n']:6d} {FLOOR[k]:8.4f} {SHARE[k]:8.4f} {C['tacc']:8.4f} {C['step']:7.3f}"
          f" {(C['tacc'] - FLOOR[k]) / C['step']:+9.3f} {yn(FB[k]):>2} {m6_s} {c0_s} {ms(P[SEC].mean)} {cl_m} {c0_m} |"
          f"      {nbf(SEC)}    {nbf(CLIP)}   {nbf(LAP)}  {yn(L.not_behind(C['loco_acc'], C['tacc'], C['step']))}")
print("   (share = task-1 share; fb = floor-bound; st = margin in steps; nb = not behind the tuned lambda; tr = the transferred lambda;"
      " '-' = no such record: SEC1 carriers are not in the M runs, the clipped SEC exists on SEC4 and SEC5 only)")

# ============================================================================================================== A12
hdr("A12  how much of the pass count sits at the accuracy floor?  not-behind rates on the floor-bound carriers against the rest")
print("   AMBIGUITY: 'per study' is read as the four held-out studies whose 30 carriers are pooled; SEC1 is printed as a REPORT line and"
      " enters no pool. 'The rest' is read as the held-out carriers that are not floor-bound.")
ARMS12 = (("SEC", lambda C: L.arm_nb(C, SEC), lambda C: True), ("clipSEC", lambda C: L.arm_nb(C, CLIP), lambda C: CLIP in C["primary"]),
          ("Laplace", lambda C: L.arm_nb(C, LAP), lambda C: True),
          ("transf", lambda C: L.not_behind(C["loco_acc"], C["tacc"], C["step"]), lambda C: True))
LONG12 = dict(SEC="the unclipped SEC (bayes_sec)", clipSEC="the clipped SEC (bayes_sec_clip; SEC4, SEC5)", Laplace="raw Laplace (bayes)",
              transf="the transferred lambda (sec_lib loco_acc)")


def a12_row(label, cs):
    fb = [C for C in cs if FB[key(C)]]; rest = [C for C in cs if not FB[key(C)]]
    out = {}
    cells = []
    for name, f, has in ARMS12:
        a = [C for C in fb if has(C)]; b = [C for C in rest if has(C)]
        ka, kb = sum(f(C) for C in a), sum(f(C) for C in b)
        out[name] = (ka, len(a), kb, len(b))
        cells.append(f"{short(ka, len(a)):>13} {short(kb, len(b)):>13}" if (a or b) else f"{'-':>13} {'-':>13}")
    print(f"   {label:34} {len(cs):3d} {len(fb):3d} | " + " | ".join(cells))
    return len(fb), out


print("   arms: " + "; ".join(f"{a} = {b}" for a, b in LONG12.items()) + "; n = carriers, fb = floor-bound")
print(f"   {'':34} {'n':>3} {'fb':>3} | " + " | ".join(f"{name + ' fb':>13} {name + ' rest':>13}" for name, _, _ in ARMS12))
ROWS12 = {}
for s in HELD:
    ROWS12[s] = a12_row(s, BY[s])
H30 = [C for C in CS if C["study"] in HELD]
nfb30, P30 = a12_row(f"held-out pooled ({len(H30)})", H30)
print("   REPORT (not held out; in no pool):")
a12_row("sec1", BY["sec1"])
a12_row(f"all {N} pooled", CS)
print("   (each cell: not behind k/n (rate) on the floor-bound carriers, then on the rest; the clipped SEC exists on SEC4 and SEC5 only)")
print("\n   the held-out pool at full precision:")
for name, _, _ in ARMS12:
    ka, na, kb, nb = P30[name]
    print(f"   {name:8} floor-bound {rate(ka, na)}; rest {rate(kb, nb)}")
print("   floor-bound held-out carriers: " + ", ".join(f"{C['study']}:{C['carrier']}" for C in H30 if FB[key(C)]))
ka, na, kb, nb = P30["SEC"]
f12a = F12_QUARTER * nfb30 >= len(H30)
f12b = na > 0 and nb > 0 and ka / na > kb / nb
print(f"F12 (a) floor-bound among the {len(H30)} held-out carriers: {nfb30} >= {len(H30)}/{F12_QUARTER} = {len(H30) / F12_QUARTER:g} -> {f12a}")
print(f"F12 (b) unclipped SEC not-behind rate on the floor-bound {rate(ka, na)} > on the rest {rate(kb, nb)} -> {f12b}")
print(f"F12: {word(f12a and f12b)}")

print("\nAmendment 1: 'Every forecast F1-F11 whose decisive count includes floor-bound carriers is also printed with them removed, as a report.'")
print("   Each is already printed by the script that decides the forecast; cited here (file, line, the word printed there), not reprinted:")
ALL, HO = "all floor-bound removed", "held-out floor-bound removed, SEC1 kept whole"
CITE = (                                                      # (forecast, pinned output, pattern, the removal it prints)
    ("F1", "a1_a3.txt", r"^\s*F1 floor-bound removed \(report\): (.+)$", ALL),
    ("F2", "a1_a3.txt", r"^\s*F2 floor-bound removed \(report\): (NOT DECIDABLE|HOLDS|FAILS)", ALL),
    ("F3(a)", "a1_a3.txt", r"^\s*F3\(a\) floor-bound removed \(report\): (.+)$", ALL),
    ("F3(b)", "a1_a3.txt", r"^\s*F3\(b\) floor-bound removed \(report\): (.+)$", ALL),
    ("F4", "a4_a6.txt", r"^\s*F4 all floor-bound removed \(report\): (.+)$", ALL),
    ("F4", "a4_a6.txt", r"^\s*F4 held-out floor-bound removed, SEC1 kept whole \(report\): (.+)$", HO),
    ("F5", "a5_a9_a10.txt", r"^\s*F5 floor-bound removed \(report\): (.+)$", ALL + " (F5's failure cases)"),
    ("F6", "a4_a6.txt", r"^\s*F6 all floor-bound removed \(report\): (.+)$", ALL),
    ("F6", "a4_a6.txt", r"^\s*F6 held-out floor-bound removed, SEC1 kept whole \(report\): (.+)$", HO),
    ("F7", "a7_a8.txt", r"^\s*F7 all floor-bound removed \(report\): (UNDEFINED|HOLDS|FAILS)", ALL),
    ("F7", "a7_a8.txt", r"^\s*F7 held-out floor-bound removed, SEC1 kept whole \(report\): (UNDEFINED|HOLDS|FAILS)", HO),
    ("F8", "a7_a8.txt", r"^\s*F8 all floor-bound removed \(report\): (HOLDS|FAILS)", ALL),
    ("F8", "a7_a8.txt", r"^\s*F8 held-out floor-bound removed, SEC1 kept whole \(report\): (HOLDS|FAILS)", HO),
    ("F9", "a5_a9_a10.txt", r"^\s*F9 floor-bound removed \(report\): (.+)$", "floor-bound removed from SEC5's clipped failures"),
    ("F10", "a5_a9_a10.txt", r"^\s*F10 floor-bound removed \(report\): (.+)$", "floor-bound removed from the 30 held-out"),
    ("F11", "a11_grade.txt", r"with them removed, (geometric-mean s > 1 on \d+/\d+, more than half: (?:True|False))", ALL + " ((b-iv))"),
)
for fid, fn, pat, how in CITE:
    lines = open(os.path.join(HERE, fn)).read().splitlines()
    hits = [(i + 1, m.group(1).strip()) for i, ln in enumerate(lines) for m in [re.search(pat, ln)] if m]
    assert len(hits) == 1, (fid, fn, pat, hits)
    ln, w = hits[0]
    extra = ""
    if fid == "F11":
        assert "Amendment 1 report ((b-iv) counts carriers" in lines[ln - 2], lines[ln - 2]
        extra = f" (lines {ln - 1}-{ln}: part (b-iv), the only sentence of F11 that counts carriers)"
    print(f"   {fid:6} SEC_Analysis/checks/{fn}:{ln}{extra}  [{how}]  ->  {w}")
print("   cited files (sha256): " + "; ".join(f"{fn} {sha256(os.path.join(HERE, fn))}" for fn in sorted({c[1] for c in CITE})))
print("   nothing of F1-F11 is reprinted here; A12's own analysis and F12 are above")

# ============================================================================================================== A13
hdr("A13  the development arms as mechanism evidence: SI-1C, AR1-B, the clipped SEC (C0) and the tuned clipped lambda, against the"
    " tuned lambda with and without the clip (30 SEEN carriers)")
print("   the tuned clipped lambda: the best seed mean over SEC6's fixed_clip grid (ties to the smallest lambda); tacc_c its mean; step_c ="
      " max(1, 2 SE) of its seeds")
print("   AMBIGUITY: 'C0 from m_runs or the pinned bayes_sec_clip' is read as C0 from m_runs on all 30 carriers, with the pinned record"
      " checked equal where it exists (below)")
id14 = [k for k in MK if CLIP in D[k]["primary"]]
eq14 = [k for k in id14 if [r["acc"] for r in R[k]["C0"]] == D[k]["primary"][CLIP].acc.tolist()]
print(f"   C0 (m_runs) against the pinned bayes_sec_clip, all five seeds: equal on {len(eq14)}/{len(id14)} of the SEC4 and SEC5 carriers"
      f" ({5 * len(eq14)}/{5 * len(id14)} seeds) -> the counts below are the same whichever of the two is read there")
no_pin = [k for k in MK if CLIP not in D[k]["primary"]]
eqref = [k for k in no_pin if [r["acc"] for r in R[k]["C0"]] == A13[k]["ref_clip"]]
print(f"   the {len(no_pin)} SCL3 and SEC3 carriers have no pinned bayes_sec_clip in runs/: C0 (m_runs) is the only record read. REPORT: it"
      f" equals the clipped-SEC reference in SEC6's development records (from SEC5's development runs, prereg/sec5/dev) on {len(eqref)}/{len(no_pin)}"
      f" carriers, all five seeds")
recsame = sum(A13[k]["tc"]["rec_same"] for k in MK)
print(f"   the tuned clipped lambda, tacc_c and step_c recomputed here equal the devfclip record's own 'tuned', 'acc' and 'step' on"
      f" {recsame}/{len(MK)}; grid configurations per carrier {sorted({A13[k]['tc']['n_grid'] for k in MK})}; non-finite runs in the grids"
      f" {sum(A13[k]['tc']['nonfinite'] for k in MK)}")
tie_dev = [f"{k[1]} (record {A13[k]['dev_tuned']:g}, sec_lib {D[k]['tuned']:g})" for k in MK if A13[k]["dev_tuned"] != D[k]["tuned"]]
print(f"   the dev records' tacc and step equal sec_lib's on {len(MK)}/{len(MK)} (asserted). REPORT: their 'tuned' field differs from"
      f" sec_lib's tie rule on {len(tie_dev)} ({'; '.join(tie_dev) or 'none'}); tacc and step are the same there, so nothing below moves")

print(f"\n   {'study':5} {'carrier':34} {'lam*_raw':>9} {'tacc':>8} {'step':>7} | {'lam*_clip':>9} {'tacc_c':>8} {'step_c':>7} {'top':>3}"
      f" {'fired':>15} | {'tacc_c - tacc (full precision)':>30} {'steps':>8} {'A/B':>3}")
for k in MK:
    x = A13[k]; C = x["C"]; t = x["tc"]; d = t["acc"] - C["tacc"]
    ab = "A" if d > C["step"] else ("B" if -d > C["step"] else "-")
    x.update(d=d, ds=d / C["step"], ahead=d > C["step"], behind=-d > C["step"])
    print(f"   {C['study']:5} {C['carrier'][:34]:34} {C['tuned']:9.4g} {C['tacc']:8.4f} {C['step']:7.3f} | {t['lam']:9.4g} {t['acc']:8.4f}"
          f" {t['step']:7.3f} {yn(t['top']):>3} {str(t['fired']):>15} | {d!r:>30} {d / C['step']:+8.3f} {ab:>3}")
print("   (top = the tuned clipped lambda is the largest lambda of its grid (REPORT: the grid, SEC1's, may not reach its optimum); fired ="
      " the clip's firings per seed at it; A = ahead by more than a step, B = behind by more than a step, step the unclipped one)")

print(f"\n   {'study':5} {'carrier':34} | {'SI-1C':>8} {'st':>7} {'st_c':>7} | {'AR1-B':>8} {'st':>7} {'st_c':>7} | {'C0':>8} {'st':>7} {'st_c':>7}"
      f" | {'C0 fired':>8} {'seeds':>5} {'cap mean':>9} {'cap max':>9} {'fired mean':>10}")
for k in MK:
    x = A13[k]; C = x["C"]; t = x["tc"]
    cols = []
    for a in ("si1c", "ar1b", "c0"):
        v = x[a]; s1 = (v - C["tacc"]) / C["step"]; s2 = (v - t["acc"]) / t["step"]
        f1 = " " if L.not_behind(v, C["tacc"], C["step"]) else "*"; f2 = " " if v - t["acc"] > -t["step"] else "*"
        cols.append(f"{v:8.4f} {s1:+6.2f}{f1} {s2:+6.2f}{f2}")
    fm = "-" if x["cap_fired"] is None else f"{x['cap_fired']:.3e}"
    print(f"   {C['study']:5} {C['carrier'][:34]:34} | " + " | ".join(cols)
          + f" | {x['fired']:8d} {x['seeds_fired']:5d} {x['cap_mean']:9.3e} {x['cap_max']:9.3e} {fm:>10}")
print("   (st = (arm - tacc) / step, against the tuned lambda; st_c = (arm - tacc_c) / step_c, against the tuned clipped lambda; * = behind"
      " that reference (arm - reference <= -its step); C0 fired = the clip's firings over seeds and task starts; seeds = seeds with a firing; cap mean / max = C0's")
print("    frac_capped over every guarded task start and seed (0 where the clip did not fire); fired mean (REPORT) = its mean over the"
      " starts where the clip fired only)")
mj = MJ["per_carrier"]
capsame = sum(mj[f"{k[0]}:{k[1]}"]["c0_frac_capped_mean"] == A13[k]["cap_mean"] and mj[f"{k[0]}:{k[1]}"]["c0_frac_capped_max"] == A13[k]["cap_max"]
              for k in MK)
print(f"   C0's capped fractions equal m_checks.json's per-carrier c0_frac_capped_mean and _max on {capsame}/{len(MK)}")

print("\ncounts over the 30 carriers:")
NB = {}
for lab, a in (("SI-1C", "si1c"), ("AR1-B", "ar1b"), ("clipped SEC (C0)", "c0")):
    k1 = [k for k in MK if L.not_behind(A13[k][a], D[k]["tacc"], D[k]["step"])]
    k2 = [k for k in MK if A13[k][a] - A13[k]["tc"]["acc"] > -A13[k]["tc"]["step"]]
    NB[a] = (len(k1), len(k2))
    print(f"   {lab:18} not behind the tuned lambda {len(k1)}/{len(MK)}; not behind the tuned clipped lambda {len(k2)}/{len(MK)}"
          f"   (behind the tuned clipped lambda: {', '.join(k[1] for k in MK if k not in k2) or 'none'})")
AH = [k for k in MK if A13[k]["ahead"]]; BH = [k for k in MK if A13[k]["behind"]]
NBc = [k for k in MK if L.not_behind(A13[k]["tc"]["acc"], D[k]["tacc"], D[k]["step"])]
print(f"   the tuned clipped lambda against the unclipped tuned lambda: ahead by more than a step on {len(AH)}/{len(MK)}"
      f" ({', '.join(k[1] for k in AH)}); behind by more than a step on {len(BH)}/{len(MK)} ({', '.join(k[1] for k in BH) or 'none'});"
      f" within a step on {len(MK) - len(AH) - len(BH)}; REPORT: not behind (tacc_c - tacc > -step) on {len(NBc)}/{len(MK)}")
TOP = [k for k in MK if A13[k]["tc"]["top"]]
print(f"   REPORT: the tuned clipped lambda at the top of its grid on {len(TOP)}/{len(MK)} ({', '.join(k[1] for k in TOP)}); of the {len(AH)} ahead,"
      f" {sum(k in TOP for k in AH)} are at the top")
FIRED = [k for k in MK if A13[k]["fired"] > 0]
cm = [A13[k]["cap_mean"] for k in FIRED]; cf = [A13[k]["cap_fired"] for k in FIRED]
print(f"   C0's clip fired (at least one seed) on {len(FIRED)}/{len(MK)} carriers; over those, the per-carrier mean capped fraction: median"
      f" {float(np.median(cm)):.3e}, range [{min(cm):.3e}, {max(cm):.3e}]; largest capped fraction at any start {max(A13[k]['cap_max'] for k in MK):.3e}"
      f" ({', '.join(k[1] for k in MK if A13[k]['cap_max'] == max(A13[k2]['cap_max'] for k2 in MK))}); REPORT, where it fired only:"
      f" median {float(np.median(cf)):.3e}, range [{min(cf):.3e}, {max(cf):.3e}]")
print(f"   REPORT: of the {len(AH)} carriers where the tuned clipped lambda is ahead, C0's clip fired on {sum(k in FIRED for k in AH)};"
      f" the tuned clipped lambda's own clip fired (any seed) on {sum(sum(A13[k]['tc']['fired']) > 0 for k in AH)}")
ordered = sorted(MK, key=lambda k: -A13[k]["ds"])
assert set(ordered[:len(AH)]) == set(AH)
b10 = ordered[len(AH) - 1] if AH else None
b11 = ordered[len(AH)] if len(AH) < len(MK) else None
print("   the boundary (full precision): "
      + (f"the smallest ahead, {b10[1]}: (tacc_c - tacc) / step = {A13[b10]['ds']!r}; " if b10 else "")
      + (f"the largest not ahead, {b11[1]}: {A13[b11]['ds']!r}" if b11 else ""))

dev_txt = open(os.path.join(ROOT, "prereg", "sec6", "dev_SEC6.txt")).read()
chk = []
for lab, pat, val in (("SI-1C not behind the tuned lambda", r"^SI-1C  : not behind the tuned lambda (\d+)/30", NB["si1c"][0]),
                      ("AR1-B not behind the tuned lambda", r"^AR1-B  : not behind the tuned lambda (\d+)/30", NB["ar1b"][0]),
                      ("clipped SEC not behind the tuned lambda", r"^\(pinned, not rerun\) clipped SEC: not behind (\d+)/30", NB["c0"][0]),
                      ("SI-1C not behind the tuned clipped lambda", r"^\s+SI-1C  : not behind the tuned clipped lambda (\d+)/30", NB["si1c"][1]),
                      ("AR1-B not behind the tuned clipped lambda", r"^\s+AR1-B  : not behind the tuned clipped lambda (\d+)/30", NB["ar1b"][1]),
                      ("clipped SEC not behind the tuned clipped lambda",
                       r"^\s+\(pinned, not rerun\) clipped SEC: not behind the tuned clipped lambda (\d+)/30", NB["c0"][1]),
                      ("tuned clipped lambda ahead by more than a step", r"ahead of the tuned lambda by more than a step \(the tuned lambda's step\): (\d+)/30", len(AH)),
                      ("tuned clipped lambda behind by more than a step", r"behind by more than a step: (\d+)/30", len(BH))):
    m = re.findall(pat, dev_txt, flags=re.M)
    assert len(m) == 1, (lab, m)
    chk.append((lab, int(m[0]), val))
print("   REPORT: the same counts in prereg/sec6/dev_SEC6.txt (SEC6's development report; its clipped SEC on SCL3/SEC3 is SEC5's development"
      " record): " + "; ".join(f"{lab} {a} vs here {b}" for lab, a, b in chk)
      + f" -> {'REPRODUCED' if all(a == b for _, a, b in chk) else 'DIFFERS'}")
f13 = F13_THIRD * len(AH) >= len(MK)
print(f"F13 the tuned clipped lambda ahead of the unclipped tuned lambda by more than a step (tacc_c - tacc > step): {len(AH)}/{len(MK)} >="
      f" {len(MK)}/{F13_THIRD} = {len(MK) / F13_THIRD:g} -> {f13}")
print(f"F13: {word(f13)}")

# ============================================================================================================== A14
hdr("A14  does the benchmark's class order explain the pass counts?  Spearman with the task-1 share")


def spear(ks, vals):
    x = [SHARE[k] for k in ks]; r = spearmanr(vals, x)
    return float(r[0]), float(r[1]), len(ks)


print("   margins are over the unclipped tuned lambda in its step, (arm - tacc) / step, for SEC, the clipped SEC and C0 alike (the"
      " declaration's 'the same for the clipped SEC and for C0'); M6 enters as its seed-mean accuracy, not a margin")
m6 = spear(MK, [MEAN[k]["M6"] for k in MK])
sec = spear(list(D), [L.margin_steps(D[k], D[k]["primary"][SEC].mean) for k in D])
K14 = [k for k in D if CLIP in D[k]["primary"]]
clp = spear(K14, [L.margin_steps(D[k], D[k]["primary"][CLIP].mean) for k in K14])
c0s = spear(MK, [L.margin_steps(D[k], MEAN[k]["C0"]) for k in MK])
sec30 = spear(MK, [L.margin_steps(D[k], D[k]["primary"][SEC].mean) for k in MK])
m6m = spear(MK, [L.margin_steps(D[k], MEAN[k]["M6"]) for k in MK])
m6fl = spearmanr([MEAN[k]["M6"] for k in MK], [FLOOR[k] for k in MK])
for lab, (rho, p, n) in (("M6 seed-mean accuracy (m_runs)", m6), ("SEC margin in steps (bayes_sec, pinned)", sec),
                         ("clipped SEC margin in steps (bayes_sec_clip, pinned)", clp), ("C0 margin in steps (m_runs)", c0s)):
    print(f"   Spearman({lab}, task-1 share) over {n:2d} carriers: rho {rho!r} ({rho:+.3f}); p {p:.3g} (REPORT)")
print(f"   REPORT: SEC margin in steps over the {sec30[2]} held-out carriers only: rho {sec30[0]!r} ({sec30[0]:+.3f}); M6 margin in steps over"
      f" {m6m[2]}: rho {m6m[0]!r} ({m6m[0]:+.3f}); Spearman(M6 accuracy, floor) over {len(MK)}: rho {float(m6fl[0])!r} ({float(m6fl[0]):+.3f})")
f14a = m6[0] >= F14_RHO; f14b = sec[0] > 0
print(f"F14 (a) Spearman(M6 accuracy, task-1 share) = {m6[0]!r} ({m6[0]:.3f}) >= {F14_RHO} -> {f14a}")
print(f"F14 (b) Spearman(SEC margin in steps, task-1 share) over {sec[2]} = {sec[0]!r} ({sec[0]:.3f}) > 0 -> {f14b}")
print(f"F14: {word(f14a and f14b)}")

# ============================================================================================================== summary
print(); print(BAR)
print("summary: POST HOC in origin (Amendments 1-3); declared checks on seen records; no ledger row; the words are computed above")
print(f"   F12  {word(f12a and f12b)}   (a) floor-bound {nfb30}/{len(H30)} held-out (>= {len(H30) / F12_QUARTER:g}) -> {f12a}; (b) unclipped SEC not"
      f" behind on floor-bound {ka}/{na} ({ka / na:.3f}) > rest {kb}/{nb} ({kb / nb:.3f}) -> {f12b}")
print(f"   F13  {word(f13)}   the tuned clipped lambda ahead of the unclipped tuned lambda by more than a step on {len(AH)}/{len(MK)}"
      f" (need >= {len(MK) / F13_THIRD:g}); behind by more than a step on {len(BH)}; SI-1C / AR1-B / C0 not behind the tuned lambda"
      f" {NB['si1c'][0]} / {NB['ar1b'][0]} / {NB['c0'][0]}, the tuned clipped lambda {NB['si1c'][1]} / {NB['ar1b'][1]} / {NB['c0'][1]} of {len(MK)};"
      f" at the boundary: the smallest ahead {b10[1]} {A13[b10]['ds']:.3f} steps, the largest not ahead {b11[1]} {A13[b11]['ds']:.3f};"
      f" the tuned clipped lambda at the top of its grid on {sum(k in TOP for k in AH)} of the {len(AH)} ahead")
print(f"   F14  {word(f14a and f14b)}   (a) Spearman(M6 accuracy, share) {m6[0]:.3f} >= {F14_RHO} -> {f14a}; (b) Spearman(SEC margin, share)"
      f" {sec[0]:.3f} > 0 -> {f14b}; clipped SEC {clp[0]:.3f} ({clp[2]}), C0 {c0s[0]:.3f} ({c0s[2]})")
print("   Amendment 1's F1-F11 with the floor-bound carriers removed: cited above, printed in a1_a3.txt, a4_a6.txt, a5_a9_a10.txt, a7_a8.txt"
      " and a11_grade.txt")
