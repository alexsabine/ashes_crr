"""SEC_Analysis: the shared loader and primitives (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; prompt-log entry 257).

POST HOC on SEEN records. It reads the pinned run records of SEC1, SCL3, SEC3, SEC4 and SEC5 and nothing else: it opens no
data, trains nothing and adds no ledger row. Every SEC_Analysis check imports it. It is validated by loader_check.py, which
must reproduce each study's pinned headline counts before any analysis output is read (DECLARATION.md, "The loader is
validated first").  Validation: uv run python SEC_Analysis/checks/loader_check.py > SEC_Analysis/checks/loader_check.txt

INPUTS. runs/{sec1,scl3,sec3,sec4,sec5}/results_*.jsonl only (never rerun_*.jsonl, never times_*.jsonl). A line without
"mode" is the carrier's header (d, K, n_train, class_counts, per_task, ...); a loader-excluded carrier has only a header,
with "excluded": true. A line with "mode" is a run record. SCL3's operator-harness records carry "arm" and no window
fields: they are not SEC1 arms and are skipped (as runs/sec4/frozen/sec4_score.py _pinned skips them; counted).

THE FROZEN SCORERS' DEFINITIONS, REPLICATED (runs/sec1/frozen/sec1_score.py score, step_of; runs/scl3/frozen/scl3_score.py
score; runs/sec3/frozen/sec3_score.py score; runs/sec4/frozen/sec4_score.py score; runs/sec5/frozen/sec5_score.py score):
  primary window  fs == 0.1, fe == 0.1, distort None. Every other (value, fs, fe) of an arm is a sensitivity cell.
  raw grid        {lambda: Arm} of mode 'fixed' at the primary window, sorted by lambda; calibrated grid: 'fixed_sec'.
  tuned lambda    max over the lambda-sorted grid of the seed mean (Python max: ties go to the smallest lambda).
  step            max(1, 2 * std(ddof=1) / sqrt(n)) of the tuned raw arm's seed accuracies (sec1_score.step_of).
  tuned_sec       the same on 'fixed_sec' (step_sec from its tuned arm; the scorers print only tuned_sec itself).
  primary arms    PRIMARY_VALUE below: bayes 0, bayes_sec 0, bayes_s1 0, eq 1.0, bayes_sec_clip 0.5 (kappa),
                  bayes_sec_scale 0.5, bayes_sec_raw 1.0 (SEC4's raw-fallback bound), bayes_sec_g 1.0 (SEC3's GUARD).
  not behind      a - tacc > -step (strict), a an arm's seed mean, tacc the tuned raw arm's seed mean.
  transferred     SEC3-T/SEC4-T/SEC5-T's lambda: exp of the median of log tuned raw lambda over the OTHER carriers of the
  lambda (loco)   same study, snapped to EWC_COARSE by nearest log (ties to the smaller); loco_acc its raw-grid mean.
                  Computed identically for all five studies (SEC1 and SCL3 did not compute it).

API. C is one carrier's dict, as load_all() returns it.
  load_all() -> {(study, carrier): C}, studies in STUDIES order, carriers sorted by name within a study (the 42 scored).
      C["study"], C["carrier"], C["family"] (= study), C["path"], C["header"] (the raw header line)
      C["d"], C["K"], C["n"], C["n_train"], C["n_test"], C["per_task"] (classes per task), C["n_tasks"], C["class_counts"],
      C["imbalance"] (max / min used class count), C["per_task_n"] (training rows per task: the 80/20 stratified split of
      sec1_score.split_standardise, recomputed from class_counts; checked to sum to n_train)
      C["arms"]       {(mode, value, fs, fe): Arm} every run record of the carrier (harness records excluded)
      C["raw"], C["sec"]            {lambda: Arm} the raw and calibrated grids (primary window, lambda-sorted)
      C["raw_means"], C["sec_means"] {lambda: seed mean}
      C["tuned"], C["tacc"], C["tv"] (the tuned Arm), C["step"]; C["tuned_sec"], C["tacc_sec"], C["step_sec"]
      C["primary"]    {mode: Arm} the arms of PRIMARY_VALUE that exist for this carrier, at the primary window
      C["cells"]      {mode: {(value, fs, fe): Arm}} every other record set of those modes (window and guard cells)
      C["loco_lam"], C["loco"], C["loco_acc"]  the transferred lambda (unsnapped, snapped) and its raw-grid mean
      C["n_harness"]  SCL3 operator-harness records skipped
  load_excluded() -> {(study, carrier): header} the loader-excluded carriers (headers with "excluded": true)
  Arm             .mode .value .fs .fe .recs (seed-sorted records) .seeds .acc (np.ndarray) .mean .finite (list of bool)
  step_of(accs) -> float                         sec1_score.step_of
  not_behind(a, tacc, step) -> bool              a - tacc > -step
  arm_nb(C, mode) -> bool                        not_behind of the primary arm `mode` against the carrier's tuned lambda
  margin(C, a) -> float                          a - C["tacc"];  margin_steps(C, a) -> (a - tacc) / step
  plateau(grid_means, best, step) -> dict        set (sorted grid values with mean > best - step), lo, hi, decades
                                                 (log10(hi / lo), 0 for one point), gaps (grid points in [lo, hi] not in set)
  brackets(p, x) -> bool                         p["lo"] <= x <= p["hi"] for a plateau p
  s_stats(arm, ddof=1) -> dict                   all (every s over tasks and seeds, as recorded, fallbacks included), n,
                                                 gmean, median, min, max, n_fallback, sd_within (the SD of log10 s across
                                                 tasks within a seed, ddof as given, averaged over seeds)
  guard_stats(arm) -> dict                       fired (sum of guard_fired), starts (task starts guarded), margins (all),
                                                 max_margin, per_seed_fired
  diverged(seed_accs, tacc, finite=None) -> bool any seed < DIV_FRAC * tacc, or any seed accuracy non-finite, or (when
                                                 given) any record non-finite. With finite=None it is SEC4-2 / SEC5-2's rule.
  arm_diverged(C, mode) -> bool                  diverged() of a primary arm with its records' finite flags
  by_study(D) -> {study: [C, ...]}
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
STUDIES = ("sec1", "scl3", "sec3", "sec4", "sec5")
FS = 0.1; FE = 0.1                                   # the registered primary calibration windows (SEC1 PREREG.md)
TEST_FRAC = 0.2                                      # sec1_score.split_standardise
DIV_FRAC = 0.5                                       # SEC4-2 / SEC5-2: a seed below half the tuned accuracy
EWC_COARSE = (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0)   # sec1_score.EWC_COARSE
GRID_MODES = ("fixed", "fixed_sec")
PRIMARY_VALUE = {"bayes": 0.0, "bayes_sec": 0.0, "bayes_s1": 0.0, "eq": 1.0, "bayes_sec_clip": 0.5, "bayes_sec_scale": 0.5,
                 "bayes_sec_raw": 1.0, "bayes_sec_g": 1.0}
SEEDS = (0, 1, 2, 3, 4)


def _same(a, b):                                     # the scorers' value match (sec3/4/5 _mean; SEC1's 1e-6 is stricter only below 1)
    return abs(a - b) <= 1e-6 * max(1.0, abs(b))


class Arm:
    """One arm at one (mode, value, fs, fe): its records sorted by seed; mean is the seed mean the scorers compare."""

    def __init__(self, recs):
        self.recs = sorted(recs, key=lambda r: r["seed"])
        r0 = self.recs[0]
        self.mode, self.value, self.fs, self.fe = r0["mode"], r0["value"], r0["fs"], r0["fe"]
        self.seeds = [r["seed"] for r in self.recs]
        self.acc = np.array([r["acc"] for r in self.recs], dtype=float)
        self.mean = float(self.acc.mean())
        self.finite = [bool(r["finite"]) for r in self.recs]

    def __repr__(self):
        return f"Arm({self.mode}, {self.value:g}, {self.fs:g}/{self.fe:g}, mean {self.mean:.4f}, seeds {self.seeds})"


def step_of(accs):
    return max(1.0, 2 * float(np.std(accs, ddof=1)) / math.sqrt(len(accs)))


def not_behind(a, tacc, step):
    return a - tacc > -step


def margin(C, a):
    return a - C["tacc"]


def margin_steps(C, a):
    return (a - C["tacc"]) / C["step"]


def arm_nb(C, mode):
    return not_behind(C["primary"][mode].mean, C["tacc"], C["step"])


def _tuned(grid):
    means = {w: a.mean for w, a in grid.items()}     # grid is lambda-sorted: max keeps the first maximum
    t = max(means, key=means.get)
    return t, means


def _read(path):
    hdrs, recs, n_h, n_d = [], [], 0, 0
    for line in open(path):
        if not line.strip():
            continue
        o = json.loads(line)
        if "mode" not in o:
            hdrs.append(o)
        elif "arm" in o:
            n_h += 1                                 # SCL3's operator harness (not a SEC1 arm)
        elif o.get("distort") is not None:
            n_d += 1                                 # gate records (none are expected in results files)
        else:
            recs.append(o)
    return hdrs, recs, n_h, n_d


def _per_task_n(cc, per_task):
    tr = [c - int(round(TEST_FRAC * c)) for c in cc]  # sec1_score.split_standardise: n_te = int(round(0.2 * n_c)) per class
    return [sum(tr[i:i + per_task]) for i in range(0, len(cc), per_task)]


def plateau(grid_means, best, step):
    vals = sorted(grid_means)
    st = [w for w in vals if grid_means[w] > best - step]
    if not st:
        return dict(set=[], lo=None, hi=None, decades=None, gaps=None)
    lo, hi = st[0], st[-1]
    return dict(set=st, lo=lo, hi=hi, decades=math.log10(hi / lo) if hi > lo else 0.0,
                gaps=sum(1 for w in vals if lo <= w <= hi and w not in st))


def brackets(p, x):
    return p["lo"] is not None and p["lo"] <= x <= p["hi"]


def s_stats(arm, ddof=1):
    per_seed = [list(map(float, r["s"])) for r in arm.recs]
    s = np.array([x for ss in per_seed for x in ss], dtype=float)
    ls = np.log10(s)
    return dict(all=s.tolist(), n=int(s.size), gmean=float(10 ** ls.mean()), median=float(np.median(s)), min=float(s.min()),
                max=float(s.max()), n_fallback=int(sum(r["n_fallback"] for r in arm.recs)),
                sd_within=float(np.mean([np.std(np.log10(ss), ddof=ddof) for ss in per_seed])))


def guard_stats(arm):
    m = [float(x) for r in arm.recs for x in r.get("guard_margins", [])]
    return dict(fired=int(sum(r.get("guard_fired", 0) for r in arm.recs)), starts=len(m), margins=m,
                max_margin=max(m) if m else None, per_seed_fired=[int(r.get("guard_fired", 0)) for r in arm.recs])


def diverged(seed_accs, tacc, finite=None):
    a = np.asarray(seed_accs, dtype=float)
    return bool(np.any(~np.isfinite(a)) or np.any(a < DIV_FRAC * tacc) or (finite is not None and not all(finite)))


def arm_diverged(C, mode):
    A = C["primary"][mode]
    return diverged(A.acc, C["tacc"], A.finite)


def _carrier(study, path, hdr, recs, n_h):
    by = {}
    for r in recs:
        by.setdefault((r["mode"], r["value"], r["fs"], r["fe"]), []).append(r)
    arms = {k: Arm(v) for k, v in by.items()}
    for k, a in arms.items():
        assert len(set(a.seeds)) == len(a.seeds), (study, hdr["dataset"], k, a.seeds)
    C = dict(study=study, carrier=hdr["dataset"], family=study, path=os.path.relpath(path, ROOT), header=hdr, arms=arms,
             n_harness=n_h)
    cc = list(hdr["class_counts"])
    C.update(d=hdr["d"], K=hdr["K"], n=hdr["n"], n_train=hdr["n_train"], n_test=hdr["n_test"], per_task=hdr["per_task"],
             n_tasks=len(range(0, hdr["K"], hdr["per_task"])), class_counts=cc, imbalance=max(cc) / min(cc),
             per_task_n=_per_task_n(cc, hdr["per_task"]))
    assert sum(C["per_task_n"]) == C["n_train"], (study, C["carrier"], C["per_task_n"], C["n_train"])
    assert all(len(r["s"]) == C["n_tasks"] for r in recs), (study, C["carrier"])            # one s per task in every record
    for gm in GRID_MODES:
        g = {k[1]: a for k, a in sorted(arms.items(), key=lambda kv: kv[0][1]) if k[0] == gm and k[2] == FS and k[3] == FE}
        vals = list(g)
        assert all(round(w, 6) == w for w in vals), (study, C["carrier"], gm)   # SEC1's round(value, 6) keys are the same keys
        assert all(not _same(a, b) for a, b in zip(vals, vals[1:])), (study, C["carrier"], gm)   # no two values merge
        assert all(a.seeds == list(SEEDS) for a in g.values()), (study, C["carrier"], gm)
        C["raw" if gm == "fixed" else "sec"] = g
    C["tuned"], C["raw_means"] = _tuned(C["raw"]); C["tv"] = C["raw"][C["tuned"]]
    C["tacc"] = C["raw_means"][C["tuned"]]; C["step"] = step_of(C["tv"].acc)
    C["tuned_sec"], C["sec_means"] = _tuned(C["sec"])
    C["tacc_sec"] = C["sec_means"][C["tuned_sec"]]; C["step_sec"] = step_of(C["sec"][C["tuned_sec"]].acc)
    prim, cells = {}, {}
    for (mode, v, fs, fe), a in sorted(arms.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2], kv[0][3])):
        if mode in GRID_MODES:
            continue
        if mode in PRIMARY_VALUE and fs == FS and fe == FE and _same(v, PRIMARY_VALUE[mode]):
            assert mode not in prim and a.seeds == list(SEEDS), (study, C["carrier"], mode)
            prim[mode] = a
        else:
            cells.setdefault(mode, {})[(v, fs, fe)] = a
    C["primary"] = prim; C["cells"] = cells
    return C


def _loco(Cs):
    names = sorted(Cs)
    for d in names:
        others = [math.log(Cs[o]["tuned"]) for o in names if o != d]
        lam = math.exp(float(np.median(others)))
        snap = min(EWC_COARSE, key=lambda w: abs(math.log(w) - math.log(lam)))
        Cs[d]["loco_lam"] = lam; Cs[d]["loco"] = snap; Cs[d]["loco_acc"] = Cs[d]["raw_means"][snap]


def _paths(study):
    return sorted(glob.glob(os.path.join(ROOT, "runs", study, "results_*.jsonl")))


def load_all():
    D = {}
    for study in STUDIES:
        Cs = {}
        for p in _paths(study):
            hdrs, recs, n_h, n_d = _read(p)
            assert len(hdrs) == 1 and n_d == 0, (p, len(hdrs), n_d)
            hdr = hdrs[0]
            if hdr.get("excluded"):
                assert not recs, p
                continue
            assert all(r["dataset"] == hdr["dataset"] for r in recs), p
            Cs[hdr["dataset"]] = _carrier(study, p, hdr, recs, n_h)
        _loco(Cs)
        for name in sorted(Cs):
            D[(study, name)] = Cs[name]
    return D


def load_excluded():
    E = {}
    for study in STUDIES:
        for p in _paths(study):
            hdr = _read(p)[0][0]
            if hdr.get("excluded"):
                E[(study, hdr["dataset"])] = hdr
    return dict(sorted(E.items(), key=lambda kv: (STUDIES.index(kv[0][0]), kv[0][1])))


def by_study(D):
    out = {s: [] for s in STUDIES}
    for (s, _), C in D.items():
        out[s].append(C)
    return out
