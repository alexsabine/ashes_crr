"""CPL1 Phase A (Coupling/DECLARATION.md, pushed at 440e185 before any CPL1 code): coupling SEC4's clipped SEC, anchor-drift
transport of stored class statistics and the empty-cut pause, on SEC1's synthetic stream, the rotated synthetic stream and the 30
SEEN carriers, seeds 0-4. Nothing here is held out: rung R4 on the synthetic streams, a declared check on SEEN data at best; no
ledger row. Every word is computed from the printed numbers (R15). The learner is Coupling/checks/cpl_lib.py.

    uv run python Coupling/checks/cpl_phase_a.py all > Coupling/checks/cpl_phase_a.txt     # C0-ID, every stream (2 processes), the report
    uv run python Coupling/checks/cpl_phase_a.py report                                    # the report from cpl_runs/*.jsonl
    uv run python Coupling/checks/cpl_phase_a.py stream <key> [--out DIR]                  # one stream: every arm x seeds 0-4
    uv run python Coupling/checks/cpl_phase_a.py rerun_cmp > Coupling/checks/cpl_rerun_cmp.txt   # byte-identical rerun (R9)

Records: cpl_runs/<key>.jsonl (a header line with the sha256 of uv.lock and of every file the learner runs, then one line per arm
and seed), cpl_runs/identity.jsonl (C0-ID); CPU seconds in cpl_runs/times/ (never compared); the timing summary in cpl_timing.txt.
"""
from __future__ import annotations

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
sys.dont_write_bytecode = True

import filecmp  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import platform  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cpl_lib as C  # noqa: E402

ROOT = C.ROOT; S = C.S; P4 = C.P4
RUNS = HERE / "cpl_runs"
SCRATCH_DEFAULT = Path("/tmp/claude-0/cpl_rerun")
KMNIST = "sec5_41982"; ROT = "rotated"; SYN = "synthetic"
WORKERS = 2
SEEDS = C.SEEDS
ARMS = (("SEC+T", dict(penalty="sec", transport=True)), ("SEC", dict(penalty="sec", transport=False)),
        ("FT+T", dict(penalty="none", transport=True)), ("FT", dict(penalty="none", transport=False)),
        ("closure", dict(penalty="sec", transport=True, variant="closure")), ("L1", dict(penalty="sec", transport=True, variant="L1")),
        ("L2", dict(penalty="sec", transport=True, variant="L2")), ("L3", dict(penalty="sec", transport=True, variant="L3")))

CHOICES = [
    "streams: SEC1's synthetic stream (RQM's phase_a.stream('POS'), as RRM2's POS); the rotated stream = POS with task j's training and "
    "test rows multiplied by an orthogonal Q_j (QR of a standard normal 20 x 20, signs fixed, worlds.py's ROT construction), drawn in "
    "task order from default_rng(60000), after SEC1's standardisation; the 30 SEEN carriers through t_lib's cache (K from the loader, "
    "per_task from each frozen scorer's DATASETS table, checked against the pinned header). 'Carriers' in every count = these 32 streams",
    "pause: immediately before own-clock step k of a task (k in 0..steps-1); 3 distinct k per task drawn from default_rng([70000, seed]): "
    "the first uniformly from the secant-window steps (the first and the last ceil(0.1 x steps)), the other two uniformly without "
    "replacement from the task's remaining steps; one schedule per seed, shared by the closure run and L1-L3",
    "pause construction: the whole learner state (listed in cpl_lib's docstring) pickled to bytes, the live dict cleared, a fresh learner "
    "rebuilt from the bytes (new MLP object, new Generator with the restored bit-generator state, new arrays); the operator's schedule "
    "is not learner state",
    "L1: the four secant accumulators (start- and end-window sums of parameters and gradients) are zeros after the restore; the window "
    "counts (the divisors) unchanged",
    "L2: every task holds 3 pauses, so under L2 no stored statistic is ever transported (L2 = transport off at every task end)",
    "L3: the window counter k_step (SEC's only use of the step count) advances by D = 50 at each pause; the divisors unchanged; the pause "
    "schedule stays keyed to own steps",
    "stored statistics: hidden features = the ReLU layer on the task's training rows at the task's end; class means, and one diagonal "
    "covariance per task pooled within class (mean over the task's rows of (h - its class mean)^2)",
    "transport: at the end of every task after the first, all stored class means are moved by rrm_lib.hopdc_transport (tau 0.05, k 400) "
    "with the anchor pool = all current-task training rows, H_A(cut) their features under the previous task end's weights (SEC's "
    "theta_star), H_A(now) under the current weights; hopdc's own top-k keeps the 400 most similar anchors per mean; no rng is drawn. "
    "NAMED DEVIATION: the declaration says 'every stored class's statistics are moved by HopDC-type anchor drift'; here only the class "
    "means are moved and the stored diagonal covariances are kept as stored (HopDC's transport moves a point; a translation leaves a "
    "covariance unchanged)",
    "NCM readout: diagonal Gaussian log-likelihood, equal priors, over all K stored classes; each class uses its task's covariance shrunk "
    "toward its mean variance with RQM's ALPHA 0.1 (v' = 0.9 v + 0.1 mean(v); ReLU features have zero-variance units); accuracy 0 if the "
    "test features or the statistics are non-finite (as SEC1's net.acc)",
    "fine-tuning (FT): the same loop with the penalty term removed; the Fisher, the secant and the guard are still computed as "
    "diagnostics, so the training rng is consumed exactly as in the SEC arm; transport on and off are separate runs, and since the "
    "statistics never feed training the head readout's interaction is 0 by construction (computed and printed)",
    "step: every 'by more than a step' or 'within a step' uses the paired per-seed difference d_s over seeds 0-4, step = max(1, 2 SE of d_s); "
    "ahead / positive iff mean d > step, behind / negative iff mean d < -step, within iff |mean d| <= step",
    "C1-EXACT compares the paused run with state closure against the uninterrupted coupled run (SEC+T, no pause) in the final weights "
    "(sha256 of the bytes), every s_j (exact floats) and the stored statistics (sha256 of every mean and covariance); 'differs' is the "
    "negation. Forecast 1's accuracy changes: L1 and L3 on the head readout, L2 on the NCM readout; 'most' = more than half",
    "C0-ID: all 14 SEC4 and SEC5 carriers are checked at seed 0 (the declaration asks at least 3); C0-ID holds iff every checked carrier "
    "and 5/5 synthetic seeds are identical in acc, s, firings and margins",
    "C3: best readout = the readout (head or NCM) with the higher seed mean per carrier; ER-20 = t_lib.train(..., 'ER20') unchanged (20 "
    "raw training rows per class, replay batch = stream batch, SEC1's MLP and SGD, 3 epochs); equal training compute read as the record's "
    "convention (the same epochs, stream batch and stream passes for both; forward/backward rows per stream row printed, not equalised)",
    "G-DRIFT per carrier: NCM(FT+T) - NCM(FT) > step; the gate's G-DRIFT holds iff it holds on at least one of C4's two drift-world streams "
    "(the rotated stream, Kuzushiji-MNIST): 'transport has something to fix' somewhere in the drift world",
    "adds-something rule: over the carriers where G-DRIFT holds, a carrier counts iff C1-EXACT holds on its 5 seeds and I_NCM > step; "
    "ADDS iff the gate is OPEN and the count is at least ceil(2/3 x that number); none such -> does not add",
    "forecast 3 read without a quantifier as every carrier: I_NCM not positive by more than a step on every carrier, and the rule's word "
    "is not ADDS; forecast 2's 'most other SEEN carriers' = more than half of the 29 SEEN carriers other than Kuzushiji-MNIST",
]

POST_HOC = [
    "ORACLE-means NCM: the declared Gaussian NCM readout with every class mean replaced by the mean of its training rows' features "
    "under the final weights (a ceiling an exemplar-free learner cannot have; covariances as stored); recorded per run as "
    "acc_ncm_oracle; ORACLE - STALE is paired per seed on the transport-off arm (FT and SEC), with the declared step",
    "per drift world, the declaration's fixed consequence of a failed G-DRIFT ('transport has nothing to fix in this learner') is "
    "replaced by computed words from ORACLE - STALE and T - STALE under FT (G-DRIFT's penalty); the rotated stream's stale relative "
    "error (FT) is ranked against the 30 SEEN carriers",
    "with the gate CLOSED, the adds-something line prints the I_NCM label counts without an interpretive word (the declaration: C2 is "
    "reported without interpretation); the adds-something verdict is unchanged",
    "under C2, for every stream with I_NCM > step, the transport effect on NCM under each penalty; under C3, ER-20 minus the SEC-only "
    "NCM (no transport) beside ER-20 minus the coupled best readout",
]


# ---------------------------------------------------------------- streams
def keys():
    out = [SYN, ROT]
    for study, did in C.T.seen_carriers():
        if not C.pinned_header(study, did).get("excluded"):
            out.append(f"{study}_{did}")
    return out


def load(key):
    if key == SYN:
        data, K = C.synthetic(); return data, K, 2, "synthetic (POS)"
    if key == ROT:
        data, K = C.rotated(); return data, K, 2, "rotated synthetic"
    study, did = key.split("_"); r = C.seen(study, int(did)); assert r is not None, key
    return r


def provenance():
    fz = ROOT / "runs" / "sec5" / "frozen"
    files = {"uv.lock": ROOT / "uv.lock", "cpl_lib.py": HERE / "cpl_lib.py", "cpl_phase_a.py": Path(__file__).resolve(),
             "sec4_score.py": fz / "sec4_score.py", "sec1_score.py": fz / "sec1_score.py", "scl3_score.py": fz / "scl3_score.py",
             "sec5_score.py": fz / "sec5_score.py", "rrm_lib.py": ROOT / "Relational_Reference_Memory" / "checks" / "rrm_lib.py",
             "t_lib.py": ROOT / "Relational_Reference_Memory" / "checks" / "t_lib.py",
             "rqm_lib.py": ROOT / "Replay_Quality_Memory" / "checks" / "rqm_lib.py", "phase_a.py": ROOT / "Replay_Quality_Memory" / "checks" / "phase_a.py"}
    return dict(sha256={k: C.sha256_file(p) for k, p in files.items()}, numpy=np.__version__, python=platform.python_version())


def run_stream(key, outdir=RUNS):
    outdir = Path(outdir); (outdir / "times").mkdir(parents=True, exist_ok=True)
    data, K, per_task, name = load(key); Xtr, ytr, Xte, yte = data
    with open(outdir / f"{key}.jsonl", "w") as out, open(outdir / "times" / f"{key}.jsonl", "w") as tout:
        print(json.dumps(dict(header=1, key=key, dataset=name, K=K, per_task=per_task, n_train=int(len(ytr)), n_test=int(len(yte)),
                              d=int(Xtr.shape[1]), compute=C.compute_rows(ytr, K, per_task), **provenance())), file=out, flush=True)
        for seed in SEEDS:
            sch = C.pause_schedule(seed, ytr, K, per_task)
            for arm, kw in ARMS:
                kw = dict(kw); paused = "variant" in kw
                t0 = time.process_time()
                o = C.run_cpl(seed, *data, K, per_task, pauses=sch if paused else None, **kw)
                dt = time.process_time() - t0
                if paused:
                    o["pauses"] = sch
                print(json.dumps(dict(arm=arm, key=key, **o)), file=out, flush=True)
                print(json.dumps(dict(arm=arm, key=key, seed=seed, cpu_s=dt)), file=tout, flush=True)
            t0 = time.process_time(); a = C.run_er20(seed, *data, K, per_task); dt = time.process_time() - t0
            print(json.dumps(dict(arm="ER-20", key=key, seed=int(seed), acc_head=a)), file=out, flush=True)
            print(json.dumps(dict(arm="ER-20", key=key, seed=seed, cpu_s=dt)), file=tout, flush=True)
            print(f"[{key}] seed {seed} done", file=sys.stderr, flush=True)
    return key


# ---------------------------------------------------------------- C0-ID
def identity(outp=RUNS / "identity.jsonl"):
    RUNS.mkdir(parents=True, exist_ok=True)
    with open(outp, "w") as out:
        data, K = C.synthetic()
        for seed in SEEDS:
            a = P4.run_guard(seed, *data, K, 2, "clip"); b = C.run_cpl(seed, *data, K, 2, stats=False, transport=False)
            c = C.run_cpl(seed, *data, K, 2)
            print(json.dumps(dict(kind="synthetic", seed=seed, run_guard_acc=a["acc"], cpl_acc=b["acc_head"],
                                  same=bool(a["acc"] == b["acc_head"] and a["s"] == b["s"] and a["guard_fired"] == b["guard_fired"]
                                            and a["guard_margins"] == b["guard_margins"]),
                                  extras_same=bool(c["theta_sha"] == b["theta_sha"] and c["acc_head"] == b["acc_head"] and c["s"] == b["s"]))),
                  file=out, flush=True)
        P4.TIMES.clear()
        for study in ("sec4", "sec5"):
            for did in C.TABLES[study]:
                if C.pinned_header(study, did).get("excluded"):
                    continue
                (Xtr, ytr, Xte, yte), K, per_task, name = C.seen(study, did)
                o = C.run_cpl(0, Xtr, ytr, Xte, yte, K, per_task, stats=False, transport=False)
                p = [r for r in map(json.loads, open(ROOT / "runs" / study / f"results_{did}.jsonl"))
                     if r.get("mode") == "bayes_sec_clip" and r["seed"] == 0 and r["value"] == C.KAPPA and r["fs"] == S.FS and r["fe"] == S.FE]
                assert len(p) == 1, (study, did, len(p)); p = p[0]
                print(json.dumps(dict(kind="pinned", study=study, openml_id=did, dataset=name, pinned_acc=p["acc"], cpl_acc=o["acc_head"],
                                      same_acc=bool(p["acc"] == o["acc_head"]),
                                      same_rest=bool(p["s"] == o["s"] and p["guard_fired"] == o["guard_fired"] and p["guard_margins"] == o["guard_margins"]))),
                      file=out, flush=True)
                print(f"[identity] {study} {name} done", file=sys.stderr, flush=True)


# ---------------------------------------------------------------- the report
def _read(d=None):
    d = RUNS if d is None else d; Rr, H = {}, {}
    for key in keys():
        p = Path(d) / f"{key}.jsonl"
        if not p.exists():
            continue
        for line in open(p):
            o = json.loads(line)
            if o.get("header"):
                H[key] = o; continue
            Rr.setdefault(key, {}).setdefault(o["arm"], []).append(o)
    for key, arms in Rr.items():
        for a, recs in arms.items():
            recs.sort(key=lambda r: r["seed"]); assert [r["seed"] for r in recs] == list(SEEDS), (key, a)
    return Rr, H


def _v(recs, f="acc_head"):
    return np.array([r[f] for r in recs], dtype=float)


def _cmp(d):
    """(mean, step, label) for paired per-seed differences d_s."""
    d = np.asarray(d, dtype=float); m = float(d.mean()); st = C.step_of(d)
    return m, st, ("POSITIVE" if m > st else ("NEGATIVE" if m < -st else "WITHIN"))


def _eff(m):
    return "harms" if m < 0 else ("helps" if m > 0 else "does not change NCM")


def _rel(A, arm):
    """Seed mean of the relative error of the stored old-class means against the current ones (nan if any seed has none)."""
    v = [r["rel_err_old"] for r in A[arm]]
    return float(np.mean(v)) if all(x is not None for x in v) else float("nan")


def _same(u, v):
    return u["theta_sha"] == v["theta_sha"] and u["s"] == v["s"] and u["stats_sha"] == v["stats_sha"]


def _ds(u, v):
    """s_j changes: tasks x seeds that differ, and the median |log10(s_L / s_U)| over those."""
    diff = []; n = 0
    for a, b in zip(u, v):
        for x, y in zip(a["s"], b["s"]):
            n += 1
            if x != y:
                diff.append(abs(math.log10(y / x)) if x > 0 and y > 0 else float("inf"))
    return len(diff), n, (float(np.median(diff)) if diff else 0.0)


def report():
    Rr, H = _read(); K_ = keys(); have = [k for k in K_ if k in Rr and all(a in Rr[k] for a, _ in ARMS) and "ER-20" in Rr[k]]
    prov = provenance()
    W = 128
    print("=" * W)
    print("CPL1 Phase A (Coupling/DECLARATION.md, pushed at 440e185 before any CPL1 code): SEC4's clipped SEC + HopDC-type transport of")
    print("stored class statistics + the empty-cut pause, in one learner (CL-X, Coupling/checks/cpl_lib.py). Seeds 0-4.")
    print("Nothing here is held out: R4 on the synthetic streams, a declared check on SEEN data at best; no ledger row; words computed (R15).")
    print("=" * W)
    print("CHOICES (underspecified points; the most literal, simplest reading; fixed in the code before any CPL1 output was read):")
    for i, c in enumerate(CHOICES, 1):
        print(f"CHOICES {i:2d}: {c}")
    print("POST HOC (added after the first run, at an adversarial review's request; report lines only; no gate, forecast or "
          "adds-something rule changed; the run-1 report is kept as cpl_phase_a_run1.txt):")
    for i, c in enumerate(POST_HOC, 1):
        print(f"POST HOC {i}: {c}")
    print("-" * W)
    print("provenance (R9): " + "; ".join(f"{k} {v[:16]}" for k, v in prov["sha256"].items()) + f"; numpy {prov['numpy']}; python {prov['python']}")
    same_h = [k for k in have if H[k]["sha256"] == prov["sha256"]]
    print(f"record headers carrying the current sha256 of every file above: {len(same_h)}/{len(have)} -> {'SAME' if len(same_h) == len(have) else 'CHANGED'}")
    missing = [k for k in K_ if k not in have]
    print(f"what was run: {len(have)} of {len(K_)} streams complete ({SYN}, {ROT}, {len(K_) - 2} SEEN carriers); per stream and seed the arms "
          f"{', '.join(a for a, _ in ARMS)}, ER-20 (C1 on all, C2 on all, C3 on all); missing: {missing or 'none'}")

    # ---------------- C0-ID
    print("\n" + "=" * W); print("C0-ID: cpl_lib.run_cpl (penalty 'sec', no extras, no pause) against the frozen runs/sec5/frozen/sec4_score.run_guard('clip')"); print("=" * W)
    ids = [json.loads(line) for line in open(RUNS / "identity.jsonl")]
    syn = [r for r in ids if r["kind"] == "synthetic"]; pin = [r for r in ids if r["kind"] == "pinned"]
    k_syn = sum(r["same"] for r in syn); k_ext = sum(r["extras_same"] for r in syn)
    print(f"synthetic stream, seeds 0-4: equal to run_guard('clip') in acc, s, firings and margins on {k_syn}/{len(syn)} -> {'IDENTICAL' if k_syn == len(syn) else 'DIFFERS'}")
    print(f"synthetic stream: with the extras on (statistics and transport), final weights, acc and s equal to extras off on {k_ext}/{len(syn)} -> "
          f"{'IDENTICAL' if k_ext == len(syn) else 'DIFFERS'} (the extras never touch training)")
    print(f"   {'study':5} {'carrier':22} {'id':>6} {'pinned bayes_sec_clip acc':>26} {'run_cpl acc':>20}  acc        s/firings/margins")
    for r in pin:
        print(f"   {r['study']:5} {r['dataset']:22} {r['openml_id']:>6} {r['pinned_acc']!r:>26} {r['cpl_acc']!r:>20}  "
              f"{'IDENTICAL' if r['same_acc'] else 'DIFFERS':10} {'equal' if r['same_rest'] else 'DIFFER'}")
    k_pin = sum(r["same_acc"] and r["same_rest"] for r in pin)
    c0 = k_syn == len(syn) == 5 and k_pin == len(pin) and len(pin) >= 3
    print(f"pinned SEC4/SEC5 carriers at seed 0: IDENTICAL on {k_pin}/{len(pin)} (at least 3 required)")
    print(f"C0-ID -> {'HOLDS' if c0 else 'FAILS'}")

    N = len(have)
    # ---------------- C1
    print("\n" + "=" * W); print("C1: the empty cut on the coupled state (3 pauses per task at own-clock steps, at least one inside a secant window)"); print("=" * W)
    print("per stream: C1-EXACT (closure = uninterrupted in weights, s_j and statistics) seeds; each lossy variant: seeds that differ;")
    print("L1/L3: s_j that differ (of tasks x seeds), median |log10 s ratio|, head acc change (step, label); L2: NCM acc change (step, label)")
    c1 = {}; diff = {v: {} for v in ("L1", "L2", "L3")}; within = {v: {} for v in ("L1", "L2", "L3")}
    for k in have:
        A = Rr[k]; U = A["SEC+T"]
        c1[k] = sum(_same(u, c) for u, c in zip(U, A["closure"]))
        parts = [f"C1-EXACT {c1[k]}/5"]
        for v in ("L1", "L2", "L3"):
            V = A[v]; diff[v][k] = sum(not _same(u, x) for u, x in zip(U, V))
            if v == "L2":
                m, st, lab = _cmp(_v(V, "acc_ncm") - _v(U, "acc_ncm")); within[v][k] = lab == "WITHIN"
                parts.append(f"L2 differs {diff[v][k]}/5, dNCM {m:+.3f} (step {st:.2f}) {lab}")
            else:
                nd, nt, med = _ds(U, V); m, st, lab = _cmp(_v(V) - _v(U)); within[v][k] = lab == "WITHIN"
                mn, _, _ = _cmp(_v(V, "acc_ncm") - _v(U, "acc_ncm"))
                parts.append(f"{v} differs {diff[v][k]}/5, s_j {nd}/{nt} (med {med:.3g}), dhead {m:+.3f} (step {st:.2f}) {lab}, dNCM {mn:+.3f}")
        print(f"  [{H[k]['dataset']}] " + "; ".join(parts))
    n_c1 = sum(c1.values()); c1_all = N > 0 and n_c1 == 5 * N
    print(f"C1-EXACT: bit-identical on {n_c1}/{5 * N} stream-seeds ({sum(c1[k] == 5 for k in have)}/{N} streams on every seed) -> {'HOLDS' if c1_all else 'FAILS'}")
    canfail = {v: sum(diff[v][k] > 0 for k in have) for v in diff}
    g_canfail = all(canfail[v] >= 1 for v in canfail)
    print("G-CANFAIL: streams where the variant differs from the uninterrupted run on at least one seed: "
          + ", ".join(f"{v} {canfail[v]}/{N}" for v in canfail) + f" -> {'holds' if g_canfail else 'FAILS'}")
    print("accuracy changes within a step (L1, L3 head; L2 NCM): " + ", ".join(f"{v} {sum(within[v].values())}/{N}" for v in within))

    # ---------------- C2
    print("\n" + "=" * W); print("C2: do the parts interact? 2 x 2 {clipped SEC, FT} x {transport on, off}; I = (SEC+T - SEC) - (FT+T - FT) per seed"); print("=" * W)
    print("per stream: NCM seed means of the four arms; I_NCM (step, label); I_head; G-DRIFT = NCM(FT+T) - NCM(FT) (step, holds);")
    print("transport's NCM gain under SEC; relative error of the stored old-class means against the current ones (FT stale, FT transported, SEC stale, SEC transported)")
    I = {}; Ih = {}; gd = {}; lab_I = {}; cons = 0
    for k in have:
        A = Rr[k]; ncm = {a: _v(A[a], "acc_ncm") for a in ("SEC+T", "SEC", "FT+T", "FT")}; hd = {a: _v(A[a]) for a in ("SEC+T", "SEC", "FT+T", "FT")}
        mI, sI, lI = _cmp((ncm["SEC+T"] - ncm["SEC"]) - (ncm["FT+T"] - ncm["FT"])); I[k] = (mI, sI); lab_I[k] = lI
        Ih[k] = (hd["SEC+T"] - hd["SEC"]) - (hd["FT+T"] - hd["FT"])
        mD, sD, lD = _cmp(ncm["FT+T"] - ncm["FT"]); gd[k] = lD == "POSITIVE"
        mS, sS, lS = _cmp(ncm["SEC+T"] - ncm["SEC"])
        cons += sum(a["theta_sha"] == b["theta_sha"] and a["acc_head"] == b["acc_head"] for x, y in (("SEC+T", "SEC"), ("FT+T", "FT")) for a, b in zip(A[x], A[y]))
        rel = lambda a: np.mean([r["rel_err_old"] for r in A[a]]) if all(r["rel_err_old"] is not None for r in A[a]) else float("nan")  # noqa: E731
        print(f"  [{H[k]['dataset']}] NCM SEC+T {ncm['SEC+T'].mean():.2f} SEC {ncm['SEC'].mean():.2f} FT+T {ncm['FT+T'].mean():.2f} FT {ncm['FT'].mean():.2f}; "
              f"I_NCM {mI:+.3f} (step {sI:.2f}) {lI}; I_head {Ih[k].mean():+.3f}; G-DRIFT {mD:+.3f} (step {sD:.2f}) {'holds' if gd[k] else 'fails'}; "
              f"SEC gain {mS:+.3f} ({lS}); rel err FT {rel('FT'):.4f}/{rel('FT+T'):.4f} SEC {rel('SEC'):.4f}/{rel('SEC+T'):.4f}")
    print(f"construction: transport on and off give identical weights and head accuracy on {cons}/{10 * N} arm-seeds (the statistics never feed training)")
    ih0 = sum(bool(np.all(Ih[k] == 0)) for k in have)
    print(f"I_head is exactly 0 on every seed on {ih0}/{N} streams")
    cnt = {lab: sum(lab_I[k] == lab for k in have) for lab in ("POSITIVE", "NEGATIVE", "WITHIN")}
    print(f"I_NCM over the {N} streams: positive by more than a step {cnt['POSITIVE']}, negative by more than a step {cnt['NEGATIVE']}, within a step {cnt['WITHIN']}; "
          f"median I_NCM {np.median([I[k][0] for k in have]):+.4f}")
    print(f"G-DRIFT (per stream) holds on {sum(gd.values())}/{N}: {[H[k]['dataset'] for k in have if gd[k]]}")
    for k in have:
        if lab_I[k] != "POSITIVE":
            continue
        A = Rr[k]
        eS, sS_, lS_ = _cmp(_v(A["SEC+T"], "acc_ncm") - _v(A["SEC"], "acc_ncm")); eF, sF_, lF_ = _cmp(_v(A["FT+T"], "acc_ncm") - _v(A["FT"], "acc_ncm"))
        if eS < 0 and eF < 0:
            words = "transport harms under both penalties; SEC damps the harm"
        elif eS > 0 and eF > 0:
            words = "transport helps under both penalties; more under SEC"
        else:
            words = f"transport {_eff(eS)} under SEC and {_eff(eF)} under FT"
        print(f"REPORT (I_NCM > step) [{H[k]['dataset']}] transport effect on NCM (T - STALE): under SEC {eS:+.3f} (step {sS_:.2f}) {lS_}, "
              f"under FT {eF:+.3f} (step {sF_:.2f}) {lF_} -> {words}")
    print("REPORT ORACLE-means NCM (POST HOC diagnostic; the true current class means, a ceiling no exemplar-free learner has; covariances as stored),")
    print("paired per seed against the stale statistics (transport off) and against the transported ones, under FT and under SEC:")
    orc = {}
    for k in have:
        A = Rr[k]; row = {}
        for pen, off, on in (("FT", "FT", "FT+T"), ("SEC", "SEC", "SEC+T")):
            st_ = _v(A[off], "acc_ncm"); o_ = _v(A[off], "acc_ncm_oracle"); t_ = _v(A[on], "acc_ncm")
            row[pen] = dict(oracle=float(o_.mean()), OS=_cmp(o_ - st_), TS=_cmp(t_ - st_))
        orc[k] = row
        print(f"  [{H[k]['dataset']}] " + "; ".join(
            f"{pen}: ORACLE {row[pen]['oracle']:.2f}, ORACLE - STALE {row[pen]['OS'][0]:+.3f} (step {row[pen]['OS'][1]:.2f}) {row[pen]['OS'][2]}, "
            f"T - STALE {row[pen]['TS'][0]:+.3f} ({row[pen]['TS'][2]})" for pen in ("FT", "SEC")))
    for pen in ("FT", "SEC"):
        dr = [k for k in have if orc[k][pen]["OS"][2] == "POSITIVE"]
        fx = [k for k in dr if orc[k][pen]["TS"][2] == "POSITIVE"]; wr = [k for k in dr if orc[k][pen]["TS"][2] == "NEGATIVE"]
        print(f"REPORT under {pen}: ORACLE ahead of STALE by more than a step on {len(dr)}/{N} streams {[H[k]['dataset'] for k in dr]}; "
              f"on those, the transport ahead of STALE by more than a step on {len(fx)}, behind by more than a step on {len(wr)}")

    # ---------------- C4
    print("\n" + "=" * W); print("C4: the drift world (C2 printed separately): the rotated synthetic stream and Kuzushiji-MNIST (the highest-drift SEEN carrier in T7)"); print("=" * W)
    for k in (ROT, KMNIST):
        if k not in have:
            print(f"  [{k}] not run"); continue
        A = Rr[k]
        for a in ("SEC+T", "SEC", "FT+T", "FT"):
            print(f"  [{H[k]['dataset']}] {a:5} NCM [{' '.join('%.2f' % x for x in _v(A[a], 'acc_ncm'))}] head [{' '.join('%.2f' % x for x in _v(A[a]))}]")
        print(f"  [{H[k]['dataset']}] I_NCM {I[k][0]:+.4f} (step {I[k][1]:.2f}) {lab_I[k]}; G-DRIFT {'holds' if gd[k] else 'fails'}")
        print(f"  [{H[k]['dataset']}] REPORT stale relative error of the old-class means against the current ones: FT {_rel(A, 'FT'):.4f}, SEC {_rel(A, 'SEC'):.4f}")
        mO, sO, lO = orc[k]["FT"]["OS"]; mT, sT, lT = orc[k]["FT"]["TS"]
        if lO == "POSITIVE":
            tail = ("this exemplar-free transport recovers part of it by more than a step" if lT == "POSITIVE" else
                    ("this exemplar-free transport does not fix it and lowers NCM by more than a step" if lT == "NEGATIVE" else
                     "this exemplar-free transport does not fix it"))
            print(f"  [{H[k]['dataset']}] REPORT (FT) there is drift to fix (ORACLE - STALE = {mO:+.3f}, step {sO:.2f}); {tail} "
                  f"(T - STALE = {mT:+.3f}, step {sT:.2f})")
        elif lO == "WITHIN":
            print(f"  [{H[k]['dataset']}] REPORT (FT) nothing to fix here (ORACLE - STALE = {mO:+.3f} within a step, step {sO:.2f})")
        else:
            print(f"  [{H[k]['dataset']}] REPORT (FT) nothing to fix here: the ORACLE means are behind the stale ones by more than a step "
                  f"(ORACLE - STALE = {mO:+.3f}, step {sO:.2f})")
    seen_k = [k for k in have if k not in (SYN, ROT)]
    if ROT in have and seen_k:
        rr_ = _rel(Rr[ROT], "FT"); sv = [_rel(Rr[k], "FT") for k in seen_k]; med = float(np.median(sv)); n_hi = sum(v > rr_ for v in sv)
        words = ("the rotated stream drifts less than the median SEEN carrier: the synthetic drift world barely drifts" if rr_ < med else
                 "the rotated stream drifts at least as much as the median SEEN carrier")
        kr_ = f"; Kuzushiji-MNIST {_rel(Rr[KMNIST], 'FT'):.4f}" if KMNIST in have else ""
        print(f"REPORT drift size (stale relative error, FT): rotated {rr_:.4f}; the {len(seen_k)} SEEN carriers median {med:.4f}, "
              f"{n_hi} of {len(seen_k)} above the rotated stream{kr_} -> {words}")
    gdrift = any(gd.get(k, False) for k in (ROT, KMNIST))
    print(f"G-DRIFT (gate; at least one of the two drift-world streams): rotated {'holds' if gd.get(ROT) else 'fails'}, Kuzushiji-MNIST "
          f"{'holds' if gd.get(KMNIST) else 'fails'} -> {'holds' if gdrift else 'FAILS'}")
    gate = g_canfail and gdrift
    print(f"G-CANFAIL -> {'holds' if g_canfail else 'FAILS'}; G-DRIFT -> {'holds' if gdrift else 'FAILS'}")
    print(f"CPL1 GATE {'OPEN' if gate else 'CLOSED'}")
    if not gdrift:
        print("G-DRIFT fails: C2 is reported without interpretation (the declaration); whether there is drift to fix is stated per drift "
              "world above (REPORT, computed from the ORACLE-means diagnostic)")

    # ---------------- the adds-something rule
    Dk = [k for k in have if gd[k]]; need = math.ceil(2 * len(Dk) / 3) if Dk else 0
    ok = [k for k in Dk if c1[k] == 5 and lab_I[k] == "POSITIVE"]
    adds = gate and bool(Dk) and len(ok) >= need
    cD = {lab: sum(lab_I[k] == lab for k in Dk) for lab in ("POSITIVE", "NEGATIVE", "WITHIN")}
    print("\nthe adds-something rule (gate OPEN; C1-EXACT; I_NCM positive by more than a step; on at least two thirds of the streams where G-DRIFT holds):")
    print(f"   streams where G-DRIFT holds {len(Dk)}; of them C1-EXACT on every seed and I_NCM POSITIVE: {len(ok)} (need {need}); "
          f"their I_NCM labels: positive {cD['POSITIVE']}, negative {cD['NEGATIVE']}, within {cD['WITHIN']}")
    if adds:
        word = "ADDS SOMETHING (a candidate; a pre-registration may follow with a data step on a later day)"
    else:
        why = "gate CLOSED" if not gate else ("no stream where G-DRIFT holds" if not Dk else f"{len(ok)} of {len(Dk)} < {need}")
        base = Dk if Dk else have
        c = {lab: sum(lab_I[k] == lab for k in base) for lab in ("NEGATIVE", "WITHIN", "POSITIVE")}
        if not gate:
            word = (f"DOES NOT ADD SOMETHING ({why}): the coupling is an integration, not a new capability; C2 is reported without "
                    f"interpretation: I_NCM labels over {'the G-DRIFT streams' if Dk else 'all streams'}: negative {c['NEGATIVE']}, "
                    f"within {c['WITHIN']}, positive {c['POSITIVE']} (of {len(base)})")
        else:
            top = max(c, key=lambda z: (c[z], z == "WITHIN"))
            reading = {"NEGATIVE": "substitutes (negative interaction)", "WITHIN": "independent (zero interaction)", "POSITIVE": "complements, but short of the rule"}[top]
            word = (f"DOES NOT ADD SOMETHING ({why}): the coupling is an integration, not a new capability; the modal I_NCM label over "
                    f"{'the G-DRIFT streams' if Dk else 'all streams'} is {top} ({c[top]} of {len(base)}): {reading}")
    print(f"   -> {word}")

    # ---------------- C3
    print("\n" + "=" * W); print("C3: the price of exemplar-free: the coupled learner's best readout against ER-20 (20 raw rows per class), same epochs and stream passes"); print("=" * W)
    gap = {}; ahead = 0; behind = 0; ratios_c = []; ratios_e = []; gap2 = {}; ahead2 = 0; behind2 = 0
    lw = lambda lab: 'ER-20 AHEAD' if lab == 'POSITIVE' else ('ER-20 BEHIND' if lab == 'NEGATIVE' else 'within')  # noqa: E731
    for k in have:
        A = Rr[k]; hd = _v(A["SEC+T"]); nc = _v(A["SEC+T"], "acc_ncm"); er = _v(A["ER-20"])
        best, bn = (hd, "head") if hd.mean() >= nc.mean() else (nc, "NCM")
        m, st, lab = _cmp(er - best); gap[k] = m; ahead += lab == "POSITIVE"; behind += lab == "NEGATIVE"
        m2, st2, lab2 = _cmp(er - _v(A["SEC"], "acc_ncm")); gap2[k] = m2; ahead2 += lab2 == "POSITIVE"; behind2 += lab2 == "NEGATIVE"
        cp = H[k]["compute"]; ratios_c.append(cp["cpl_grad"] / cp["stream"]); ratios_e.append(cp["er_grad"] / cp["stream"])
        print(f"  [{H[k]['dataset']}] head {hd.mean():.2f}, NCM {nc.mean():.2f}, best {bn} {best.mean():.2f}; ER-20 {er.mean():.2f}; "
              f"ER-20 - best {m:+.3f} (step {st:.2f}) {lw(lab)}; REPORT ER-20 - SEC NCM (no transport) {m2:+.3f} (step {st2:.2f}) {lw(lab2)}")
    print(f"ER-20 ahead of the best readout by more than a step on {ahead}/{N}, behind on {behind}/{N}, within on {N - ahead - behind}/{N}; "
          f"median gap (ER-20 - best) {np.median(list(gap.values())):+.4f}")
    print(f"REPORT ER-20 against the SEC-only NCM (no transport): ahead by more than a step on {ahead2}/{N}, behind on {behind2}/{N}, within on "
          f"{N - ahead2 - behind2}/{N}; median gap (ER-20 - SEC NCM) {np.median(list(gap2.values())):+.4f}")
    print(f"compute (report): forward+backward rows per stream row, coupled learner min {min(ratios_c):.3f} median {np.median(ratios_c):.3f} max {max(ratios_c):.3f} "
          f"(its Fisher minibatches; plus forward-only rows for the statistics and the transport); ER-20 min {min(ratios_e):.3f} median {np.median(ratios_e):.3f} "
          f"max {max(ratios_e):.3f} (its replay rows)")

    # ---------------- forecasts
    print("\n" + "=" * W); print("Forecasts (DECLARATION.md, written before any code), scored"); print("=" * W)
    half = N / 2
    w1 = {v: sum(within[v].values()) for v in within}
    f1 = c1_all and g_canfail and all(w1[v] > half for v in w1)
    print(f"1. C1-EXACT on every stream and seed ({n_c1}/{5 * N}); L1, L2, L3 each differ (G-CANFAIL {'holds' if g_canfail else 'fails'}); accuracy "
          f"changes within a step on most streams (L1 {w1['L1']}/{N}, L2 {w1['L2']}/{N}, L3 {w1['L3']}/{N}; need more than {half:g}) -> {'HOLDS' if f1 else 'FAILS'}")
    others = [k for k in have if k not in (SYN, ROT, KMNIST)]
    fo = sum(not gd[k] for k in others)
    f2 = bool(gd.get(ROT)) and bool(gd.get(KMNIST)) and fo > len(others) / 2
    print(f"2. G-DRIFT holds on the rotated stream ({'holds' if gd.get(ROT) else 'fails'}) and on Kuzushiji-MNIST ({'holds' if gd.get(KMNIST) else 'fails'}), "
          f"and fails on most other SEEN carriers ({fo}/{len(others)}) -> {'HOLDS' if f2 else 'FAILS'}")
    npos = sum(lab_I[k] == "POSITIVE" for k in have)
    f3 = npos == 0 and not adds
    print(f"3. I_NCM negative or within a step on every stream ({N - npos}/{N}) and the coupling does not add something ({'does not add' if not adds else 'ADDS'}) "
          f"-> {'HOLDS' if f3 else 'FAILS'}")
    f4 = ahead > half
    print(f"4. ER-20 ahead of the coupled learner's best readout on most streams ({ahead}/{N}; need more than {half:g}) -> {'HOLDS' if f4 else 'FAILS'}")

    print("\nCRR's reading (fixed in the declaration, graded here):")
    print(f"   the pause (C1) is Proposition 7's construction: C1-EXACT {'HOLDS' if c1_all else 'FAILS'} -> "
          f"{'the construction holds on the whole coupled state; a check of the construction, not support for CRR' if c1_all else 'the construction does not hold'}")
    print(f"   own-clock keying (L3) is A3's reading and plain engineering: wall-clock-keyed windows change the learner on {canfail['L3']}/{N} streams")
    print(f"   SEC and transport are not CRR rules; CRR's only claim about coupling them (one empty cut covers every piece of state) is C1: "
          f"{'HOLDS' if c1_all else 'FAILS'}")
    print(f"\nsummary: C0-ID {'HOLDS' if c0 else 'FAILS'}; C1-EXACT {'HOLDS' if c1_all else 'FAILS'}; G-CANFAIL {'holds' if g_canfail else 'FAILS'}; "
          f"G-DRIFT {'holds' if gdrift else 'FAILS'}; CPL1 GATE {'OPEN' if gate else 'CLOSED'}; coupling {'ADDS SOMETHING' if adds else 'DOES NOT ADD SOMETHING'}; "
          f"forecasts 1 {'HOLDS' if f1 else 'FAILS'}, 2 {'HOLDS' if f2 else 'FAILS'}, 3 {'HOLDS' if f3 else 'FAILS'}, 4 {'HOLDS' if f4 else 'FAILS'}")


def timing(wall=None):
    tot = {}
    for p in sorted((RUNS / "times").glob("*.jsonl")):
        for line in open(p):
            t = json.loads(line); tot.setdefault(t["key"], {}).setdefault(t["arm"], 0.0); tot[t["key"]][t["arm"]] += t["cpu_s"]
    lines = ["CPL1 timing (CPU seconds from cpl_runs/times/, never compared; process_time per run)"]
    for k, arms in tot.items():
        lines.append(f"  {k}: total {sum(arms.values()):.1f} s; " + ", ".join(f"{a} {v:.1f}" for a, v in arms.items()))
    lines.append(f"all streams: {sum(sum(a.values()) for a in tot.values()):.1f} CPU s over {len(tot)} streams")
    if wall is not None:
        lines.append(f"wall clock of 'all' (identity + streams on {WORKERS} processes + report): {wall:.1f} s")
    return "\n".join(lines)


def rerun_cmp():
    d = SCRATCH_DEFAULT; d.mkdir(parents=True, exist_ok=True)
    print("CPL1 byte-identical rerun (R9): the synthetic and rotated streams (every C1, C2 and C3 arm, seeds 0-4) rerun into a scratch "
          f"directory and compared byte for byte with the pinned records")
    ok = True
    for key in (SYN, ROT):
        run_stream(key, d)
        a = RUNS / f"{key}.jsonl"; b = d / f"{key}.jsonl"
        r = subprocess.run(["cmp", str(a), str(b)], capture_output=True, text=True)
        same = r.returncode == 0 and filecmp.cmp(a, b, shallow=False); ok &= same
        print(f"cmp Coupling/checks/cpl_runs/{key}.jsonl <rerun>/{key}.jsonl: exit {r.returncode} -> {'IDENTICAL' if same else 'DIFFERS ' + r.stdout.strip()}; "
              f"sha256 {C.sha256_file(a)[:16]} / {C.sha256_file(b)[:16]}")
    print(f"rerun -> {'BYTE-IDENTICAL' if ok else 'DIFFERS'}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "all":
        t0 = time.time()
        identity()
        ks = keys()
        cost = {}
        for k in ks:
            if k in (SYN, ROT):
                cost[k] = 0
            else:
                st_, did_ = k.split("_"); h_ = C.pinned_header(st_, int(did_)); cost[k] = h_["n_train"] * h_["d"]
        order = sorted(ks, key=lambda k: (-cost[k], ks.index(k)))            # costliest first
        import multiprocessing as mp
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=WORKERS, mp_context=mp.get_context("fork")) as ex:
            for k in ex.map(run_stream, order):
                print(f"[all] {k} complete", file=sys.stderr, flush=True)
        report()
        (HERE / "cpl_timing.txt").write_text(timing(time.time() - t0) + "\n")
    elif cmd == "report":
        report()
    elif cmd == "identity":
        identity()
    elif cmd == "stream":
        out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else RUNS
        run_stream(sys.argv[2], out)
    elif cmd == "rerun_cmp":
        rerun_cmp()
    elif cmd == "timing":
        print(timing())
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
