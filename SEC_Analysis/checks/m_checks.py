"""SEC_Analysis mechanism checks M0-M6 (SEC_Analysis/DECLARATION.md, pushed at 5f64b5f; M5, M6 and A13's capped fraction from its
Amendment 2; prompt-log entry 257): which part of the clipped SEC does the work? New runs on the 30 carriers of SCL3, SEC3, SEC4
and SEC5 that their loaders keep, seeds 0-4.

POST HOC on SEEN carriers. Every carrier here was opened by SCL3, SEC3, SEC4 or SEC5 before this file was written, so these are
declared checks on seen data, not a test: no ledger row, and no word printed here is a PASS. The words HOLDS / FAILS against
FM0-FM6 and the SEC6 consequences are computed from the printed counts (R15).

THE LEARNER. The frozen runs/sec4/frozen/sec4_score.py is imported and never modified (S = SEC1's learner module as sec4_score
exposes it; the carrier tables are the frozen scorers' DATASETS: SCL3 and SEC3 through sec3_score, SEC4's own, and SEC5's from
runs/sec5/frozen/sec5_score.py). run_m() below re-implements sec4_score.run_guard(variant='clip') line for line, with three
switches (fisher, calib, penalty). In every arm, at each task start after the first, the guard margin m = lr w max(imp) is
recorded and the clip FIRES iff m >= kappa (kappa 0.5, SEC4's); firings are recorded, and so is frac_capped, per guarded task:
the fraction of coordinates whose importance is at or above the cap kappa / (lr w) when the clip fires (0 when it does not),
read before the clip (Amendment 2, A13):
  C0  empirical, chord,    clip    the clipped SEC itself (SEC4's primary arm): the importance is clipped per coordinate at the cap
                                   when the clip fires; the reference
  M1  model,     none,     clip    w = 1/2 on the task-size-weighted MODEL Fisher, s = 1 (true-Fisher Laplace): the same 50
                                   minibatches (their indices drawn from the training rng exactly as SEC draws them), one label per
                                   row sampled from the model's softmax with rng default_rng([LABEL_SEED, seed]), independent of the
                                   training rng. WHAT M1 TESTS: it keeps SEC's estimator f = mean over the 50 minibatches of
                                   (minibatch-mean gradient)^2 x bs and swaps in sampled labels only. With labels sampled from the
                                   model the cross terms have zero expectation, so f is unbiased for the per-sample model-Fisher
                                   diagonal; with the data labels (C0) f also carries about (bs - 1) x (mean gradient)^2. M1 against C0
                                   therefore changes the label source, the calibration and that mean-gradient term together: M1 is
                                   "SEC's batch Fisher estimator with model-sampled labels, uncalibrated", not a clean empirical-vs-
                                   true Fisher contrast in Kunstner et al.'s per-sample sense, and a gap to C0 cannot be assigned to
                                   the label source alone. The arm is as declared and is not changed.
  M2  empirical, endpoint, clip    s = c_end / rho, c_end = <g(th + eps u) - g(th - eps u), u> / (2 eps) at the task's end th,
                                   u = dth / |dth| (dth SEC's window difference), eps = EPS_FRAC |dth|, g the clean mean CE gradient
                                   over up to N_END_ROWS of the task's training rows (all if fewer; else drawn with
                                   default_rng([ROWS_SEED, seed, task]) without replacement); SEC's fallback rule
  M4  empirical, arc5,     clip    ARC_WINDOWS = 6 windows of W = ceil(0.1 x steps) steps, window k starting at step (k (steps - W))
                                   // 5 (the first is SEC's start window, the last its end window); with window means th_k, g_k and
                                   d_k = th_{k+1} - th_k, e_k = g_{k+1} - g_k: c_arc = sum <e_k, d_k> / sum |d_k|^2, rho_arc =
                                   sum <f d_k, d_k> / sum |d_k|^2, s = c_arc / rho_arc; SEC's fallback rule (sum |d_k|^2 <= 1e-12, or
                                   c_arc or rho_arc non-finite or <= 0: s = 1)
  M5  empirical, chord,    freeze  FREEZE-TOP (Amendment 2): SEC's calibrated importance on M5's OWN path (c, rho and s computed as in
                                   C0) only chooses the mask, the coordinates at or above the cap when the clip fires (none when it
                                   does not); after every update theta[mask] = theta_star[mask] (snapped to the anchor), and there is
                                   no penalty anywhere else. frac_capped is then the fraction frozen per task; n_moved counts masked
                                   coordinates that end a task off the anchor (0 by construction; printed as a construction check).
  M6  empirical, chord,    edge    EDGE (Amendment 2, a must-fail control): after task 1 the importance is the cap on every coordinate
                                   (lr 2 w cap = 2 kappa = 1: every step pulls each coordinate back to its anchor), a uniform freeze
                                   with no Fisher in it. The Fisher, s, c, rho and the guard margin are still computed, as diagnostics
                                   only, so that the training rng is consumed exactly as in C0; frac_capped = 1.
  M3  (not run) the pinned 'bayes_s1' records, read through sec_lib.
None of the extra computations (sampled labels, finite differences, window sums, capped fractions, masks) draws from the training
rng, and the finite difference restores the parameters exactly, so C0 is bit-identical to sec4_score.run_guard('clip'):
'identity' checks this against run_guard itself on SEC1's synthetic stream and against the pinned records (M0). c_end is computed
as a diagnostic in every arm (it feeds the importance only in M2); c and rho are SEC's chord and Fisher Rayleigh quotient on each
arm's own path.

THE CARRIERS. Each study's frozen loader (runs/<study>/frozen/scl3_score.py and sec1_score.py are byte copies of
runs/sec4/frozen's; 'identity' prints the hashes), K requested and classes per task from that study's DATASETS table, SEC1's
split_standardise; the loaded data are checked against the pinned header (dataset, K, per_task, n_train, n_test, d) and the raw
ARFF against the header's sha256. The parse is cached in CACHE, outside the repository, written only by load() below from the
frozen loader; each cache file carries the study, the id and the raw ARFF's sha256, all asserted on every hit. The data are
checked bit for bit by 'identity': M0 on the 14 SEC4 and SEC5 carriers, and on the 16 SCL3 and SEC3 carriers
sec4_score.run_guard('none') (SEC1's bayes_sec, SEC4's D-ID) at seed 0 against the pinned bayes_sec seed 0 in acc and s; 'score'
repeats the check for free on every C0 seed whose clip never fired (then C0 is SEC1's bayes_sec on the same data and rng).

THE RECORDS (R9). m_runs/<study>_<id>.jsonl: a header line {"header": 1, ...} with the sha256 of uv.lock, of this file, of the
frozen sec4_score.py and sec1_score.py and of the raw ARFF, and the numpy and Python versions; then one line per arm and seed.
CPU seconds go to m_runs/times/ (never compared). m_rerun_cmp.sh reruns all 30 carriers into a scratch directory and compares
every results file byte for byte (pinned: m_rerun_cmp.txt).

SCORING ('score'): the tuned lambda*_raw, its seed mean and the step are sec_lib's (validated in loader_check.txt; the frozen
scorers' rule). Not behind: arm - tacc > -step (strict). An arm's value is its seed mean over seeds 0-4. "Within a step" is read
two-sided and strict, |arm - C0| < step (the declaration's "(a TIE)"; a1_a3.py reads F1 the same way); the one-sided count
arm - C0 > -step is printed beside FM4 and FM5 as a report.
  FM0  C0 seed 0 equals the pinned bayes_sec_clip seed-0 accuracy bit for bit on the 14 SEC4 and SEC5 carriers: HOLDS iff 14/14
  FM1  HOLDS iff M1 is behind the tuned lambda on more of the 30 carriers than C0
  FM2  HOLDS iff (a) the median over tasks of c / c_end is > 1 AND (b) M2 is behind on more of the 30 carriers than C0. (a) is
       decided on the M2 arm's own path (c and c_end both on M2's trajectory), pooled over carriers, seeds and tasks, every task
       with c and c_end finite and c_end != 0 (tasks with c <= 0 or c_end <= 0, where SEC falls back to s = 1, are kept). The
       declaration names no path; this choice was in the code before any M output was read. The same median on C0's path (SEC's
       own c) is printed beside it with AGREE / DISAGREE, and both medians over the tasks with c > 0 and c_end > 0, as reports.
  FM3  HOLDS iff the pinned bayes_s1 is behind on more of the 42 carriers of runs/{sec1,scl3,sec3,sec4,sec5} than bayes_sec
       (one line per carrier: both margins in steps, with the behind flag)
  FM4  HOLDS iff |M4 - C0| < step on at least 80 % of the 30 carriers (a TIE)
  FM5  over the carriers where the clip fired (C0's guard fired on at least one of seeds 0-4; the carriers where it fired on
       every seed are a report), HOLDS iff |M5 - C0| < step on at least 80 % of them
  FM6  HOLDS iff M6 is behind the tuned lambda on most of the 30 carriers (more than half)
  SEC6 consequences (DECLARATION.md, "What the results may change"): M1 (M2) is carried as a baseline iff its not-behind count
       is at least C0's minus 1; M4 may be carried as a two-sided candidate iff M4 - C0 > step on at least 3 carriers.
  Provenance (R1, R9): the sha256 of uv.lock, of this file and of every m_runs file read, and each file's header against the
  current uv.lock and this file (SAME / CHANGED). Written to SEC_Analysis/checks/m_checks.json (with the per-carrier arm means,
  C0's firings and capped fractions for A13).

    uv run python SEC_Analysis/checks/m_checks.py identity > SEC_Analysis/checks/m_identity.txt   # M0, the data path, the synthetic checks
    uv run python SEC_Analysis/checks/m_checks.py list                                              # the 30 carriers: "<study> <id>"
    uv run python SEC_Analysis/checks/m_checks.py run <study> <openml_id> [--out F]                 # C0, M1, M2, M4, M5, M6 x seeds 0-4
    nohup bash SEC_Analysis/checks/m_run_all.sh > /tmp/claude-0/m_run_all.log 2>&1 &              # the full run, 3 at a time
    bash SEC_Analysis/checks/m_rerun_cmp.sh > SEC_Analysis/checks/m_rerun_cmp.txt                 # the byte-identical rerun (R9)
    uv run python SEC_Analysis/checks/m_checks.py score > SEC_Analysis/checks/m_checks.txt         # FM0-FM6 from m_runs/*.jsonl
"""
from __future__ import annotations

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")                    # as the frozen scorers, before numpy is imported
sys.dont_write_bytecode = True                        # nothing is written into the frozen folders

import glob  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import platform  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import sec_lib as SL  # noqa: E402  (the validated loader of the pinned records)

sys.path.insert(0, str(ROOT / "runs" / "sec4" / "frozen"))
import sec4_score as P4  # noqa: E402  (frozen, unmodified: SEC4's run_guard, SEC3's and SCL3's tables and loader, SEC1's learner)

P3 = P4.P3; LD = P4.L; S = P4.S
_spec = importlib.util.spec_from_file_location("sec5_score", ROOT / "runs" / "sec5" / "frozen" / "sec5_score.py")
P5 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(P5)      # SEC5's DATASETS table only

# ---------------------------------------------------------------- fixed by DECLARATION.md
M_STUDIES = ("scl3", "sec3", "sec4", "sec5")
TABLES = {"scl3": dict(P3.SCL3_DATASETS), "sec3": dict(P3.DATASETS), "sec4": dict(P4.DATASETS), "sec5": dict(P5.DATASETS)}
KAPPA = P4.KAPPA                                     # 0.5, SEC4's clip, in every arm
ARMS = {"C0": ("empirical", "chord", "clip"), "M1": ("model", "none", "clip"), "M2": ("empirical", "endpoint", "clip"),
        "M4": ("empirical", "arc5", "clip"), "M5": ("empirical", "chord", "freeze"), "M6": ("empirical", "chord", "edge")}   # Amendment 2: M5, M6
N_END_ROWS = 1000; EPS_FRAC = 0.01                   # M2's finite difference
ARC_WINDOWS = 6; ARC_FRAC = 0.1                      # M4: 6 windows of ceil(0.1 x steps) (= SEC's window fraction)
LABEL_SEED = 91_001; ROWS_SEED = 92_001              # the extra rngs (never the training rng)
N_IDENTITY = 14                                      # FM0: every SEC4 and SEC5 carrier
FM4_SHARE = 0.8; M4_AHEAD_MIN = 3; CARRY_SLACK = 1
FM5_SHARE = 0.8                                      # Amendment 2: M5 within a step of C0 where the clip fired
FM6_MOST = 0.5                                       # Amendment 2: M6 behind on more than half
SEEDS = S.SEEDS
MRUNS = HERE / "m_runs"
CACHE = Path("/tmp/claude-0/sec_analysis_m_cache")    # written only by load() below; study, id and raw sha256 asserted on every hit


# ---------------------------------------------------------------- data
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def provenance():
    """The run environment (R9): sha256 of uv.lock, of this file and of the frozen learner, and the numpy and Python versions."""
    fz = ROOT / "runs" / "sec4" / "frozen"
    return dict(uv_lock_sha256=sha256(ROOT / "uv.lock"), m_checks_sha256=sha256(Path(__file__).resolve()),
                sec4_score_sha256=sha256(fz / "sec4_score.py"), sec1_score_sha256=sha256(fz / "sec1_score.py"),
                numpy=np.__version__, python=platform.python_version())


def pinned_header(study, did):
    p = ROOT / "runs" / study / f"results_{did}.jsonl"
    with open(p) as f:
        h = json.loads(f.readline())
    assert "mode" not in h, p
    return h


def load(study, did):
    """(Xtr, ytr, Xte, yte, K, per_task, name) from the study's frozen loader and table, or None if the loader excludes it."""
    name, _, per_task = TABLES[study][did]; hdr = pinned_header(study, did)
    assert hdr["dataset"] == name and hdr["openml_id"] == did, (study, did, hdr["dataset"])
    if hdr.get("excluded"):
        return None
    assert sha256(ROOT / hdr["file"]) == hdr["sha256"], (study, did, "raw ARFF sha256 differs from the pinned header")
    CACHE.mkdir(parents=True, exist_ok=True); f = CACHE / f"{study}_{did}.npz"
    if f.exists():
        z = np.load(f, allow_pickle=False)
        assert (str(z["study"]), int(z["openml_id"]), str(z["raw_sha256"])) == (study, did, hdr["sha256"]), (study, did, "cache binding")
        assert not int(z["excluded"]), (study, did)
        Xtr, ytr, Xte, yte, K = z["Xtr"], z["ytr"], z["Xte"], z["yte"], int(z["K"])
    else:
        LD.DATASETS = TABLES[study]
        Xs, ys, meta = LD.load_openml(did)
        assert not meta["excluded"], (study, did)
        K = meta["classes_used"]; Xtr, ytr, Xte, yte = S.split_standardise(Xs, ys, K)
        tmp = CACHE / f"{study}_{did}.tmp.npz"
        np.savez(tmp, excluded=0, Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte, K=K, name=name, study=study, openml_id=did, raw_sha256=hdr["sha256"])
        os.replace(tmp, f)
    assert (K, per_task, len(ytr), len(yte), Xtr.shape[1]) == (hdr["K"], hdr["per_task"], hdr["n_train"], hdr["n_test"], hdr["d"]), \
        (study, did, K, per_task, len(ytr), len(yte), Xtr.shape[1])
    return Xtr, ytr, Xte, yte, K, per_task, name


def carriers():
    """The 30 carriers the loaders keep (pinned headers), costliest first (n_train x d) for the parallel run."""
    out = []
    for study in M_STUDIES:
        for did in TABLES[study]:
            h = pinned_header(study, did)
            if not h.get("excluded"):
                out.append((study, did, h["n_train"] * h["d"]))
    return [(s, d) for s, d, _ in sorted(out, key=lambda t: (-t[2], M_STUDIES.index(t[0]), t[1]))]


# ---------------------------------------------------------------- the learner (sec4_score.run_guard 'clip', with switches)
def _fin(x):
    return float(x) if x is not None and np.isfinite(x) else None


def _sample_labels(net, x, lrng):
    """One label per row from the model's softmax (M1); lrng is never the training rng."""
    p = S.softmax(net.forward(x)[1]); u = lrng.random(len(x))
    return np.minimum((np.cumsum(p, 1) < u[:, None]).sum(1), p.shape[1] - 1)


def _c_end(net, theta, dth, nn, Xtr, ytr, ii_task, seed, ti):
    """Hessian Rayleigh quotient along u = dth / |dth| at theta by a central difference of the clean mean gradient (M2).
    The parameters are restored to theta exactly (set_flat copies)."""
    if not (nn > S.DTH_FLOOR and np.isfinite(nn) and np.all(np.isfinite(theta))):
        return float("nan")
    if len(ii_task) <= N_END_ROWS:
        rows = ii_task
    else:
        rows = np.sort(np.random.default_rng([ROWS_SEED, seed, ti]).choice(ii_task, N_END_ROWS, replace=False))
    norm = math.sqrt(nn); u = dth / norm; eps = EPS_FRAC * norm
    net.set_flat(theta + eps * u); gp = S.ce_loss_grad(net, Xtr[rows], ytr[rows])[1]
    net.set_flat(theta - eps * u); gm = S.ce_loss_grad(net, Xtr[rows], ytr[rows])[1]
    net.set_flat(theta)
    return float((gp - gm) @ u) / (2 * eps)


def run_m(seed, Xtr, ytr, Xte, yte, K, per_task, fisher="empirical", calib="chord", penalty="clip", fs=S.FS, fe=S.FE, kappa=KAPPA,
          arc_windows=ARC_WINDOWS, lr=S.LR, bs=S.BS, epochs=S.EPOCHS, hidden=S.HID):
    """sec4_score.run_guard(variant='clip') line for line; fisher in {'empirical', 'model'}, calib in {'chord', 'none',
    'endpoint', 'arc5'}, penalty in {'clip', 'freeze', 'edge'}. With ('empirical', 'chord', 'clip') it is run_guard('clip') exactly."""
    assert fisher in ("empirical", "model") and calib in ("chord", "none", "endpoint", "arc5") and penalty in ("clip", "freeze", "edge")
    rng = np.random.default_rng(seed)                                    # the training rng, consumed exactly as run_guard's
    lrng = np.random.default_rng([LABEL_SEED, seed])                     # M1's sampled labels only
    d = Xtr.shape[1]; net = S.MLP(rng, d, K, h=hidden); n = net.flat().size
    tasks = [tuple(range(i, i + per_task)) for i in range(0, K, per_task)]
    imp_bayes = np.zeros(n); theta_star = None
    svals = []; cvals = []; rhovals = []; cends = []; carcs = []; rhoarcs = []; n_fallback = 0; fired = 0; margins = []
    fracs = []; moved = []; mask = None                                  # Amendment 2: capped (M5: frozen) fraction per guarded task
    cap = kappa / (lr * S.BAYES_W)
    arc = calib == "arc5"
    if arc:
        assert fs == ARC_FRAC and fe == ARC_FRAC, "the arc's first and last windows are SEC's windows"
    with np.errstate(all="ignore"):
        for ti, task in enumerate(tasks):
            ii_task = np.where(np.isin(ytr, task))[0]; n_task = len(ii_task)
            imp_used = imp_bayes / n_task
            if theta_star is not None:                                                        # SEC4's clip, every arm
                m = lr * S.BAYES_W * float(np.max(imp_used)); margins.append(m)
                hit = not (m < kappa)
                at_cap = imp_used >= cap if hit else np.zeros(n, dtype=bool)                  # read before the clip
                if penalty == "clip" and hit:
                    imp_used = np.minimum(imp_used, cap)
                elif penalty == "freeze":                                                     # M5: the capped set, frozen
                    mask = at_cap
                elif penalty == "edge":                                                       # M6: every coordinate at the cap
                    imp_used = np.full(n, cap); at_cap = np.ones(n, dtype=bool)
                if hit:
                    fired += 1
                fracs.append(float(np.mean(at_cap)))
            total = epochs * int(math.ceil(n_task / bs)); n_s = max(1, int(math.ceil(fs * total))); n_e = max(1, int(math.ceil(fe * total)))
            s_th = np.zeros(n); s_g = np.zeros(n); e_th = np.zeros(n); e_g = np.zeros(n); k_step = 0
            if arc:                                                                           # M4's windows (the training is untouched)
                W = max(1, int(math.ceil(ARC_FRAC * total))); starts = [(k * (total - W)) // (arc_windows - 1) for k in range(arc_windows)]
                a_th = np.zeros((arc_windows, n)); a_g = np.zeros((arc_windows, n))
            for ep in range(epochs):
                perm = rng.permutation(ii_task)
                for t in range(0, len(perm), bs):
                    ii = perm[t:t + bs]; x, y = Xtr[ii], ytr[ii]
                    L_p, g_p = S.ce_loss_grad(net, x, y)
                    theta_before = net.flat()
                    if k_step < n_s: s_th += theta_before; s_g += g_p
                    if k_step >= total - n_e: e_th += theta_before; e_g += g_p
                    if arc:
                        for k in range(arc_windows):
                            if starts[k] <= k_step < starts[k] + W: a_th[k] += theta_before; a_g[k] += g_p
                    k_step += 1
                    if theta_star is None:
                        net.set_flat(theta_before - lr * g_p); continue
                    if penalty == "freeze":                                                   # no penalty; snap the mask
                        th = theta_before - lr * g_p; th[mask] = theta_star[mask]; net.set_flat(th); continue
                    dth = theta_before - theta_star; g_q = 2 * imp_used * dth
                    w = S.BAYES_W
                    net.set_flat(theta_before - lr * (g_p + w * g_q))
            theta_now = net.flat().copy()
            if penalty == "freeze" and theta_star is not None:
                moved.append(int(np.sum(theta_now[mask] != theta_star[mask])))
            f = np.zeros(n)
            for _ in range(S.N_FISHER):
                ii = ii_task[rng.integers(0, len(ii_task), bs)]
                yy = ytr[ii] if fisher == "empirical" else _sample_labels(net, Xtr[ii], lrng)
                f += S.ce_loss_grad(net, Xtr[ii], yy)[1] ** 2
            f_task = f / S.N_FISHER * bs
            dth = e_th / n_e - s_th / n_s; dg = e_g / n_e - s_g / n_s; nn = float(dth @ dth)
            c = float(dg @ dth) / nn if nn > S.DTH_FLOOR else float("nan"); rho = float((f_task * dth) @ dth) / nn if nn > S.DTH_FLOOR else float("nan")
            c_end = _c_end(net, theta_now, dth, nn, Xtr, ytr, ii_task, seed, ti)          # diagnostic in every arm; M2's numerator
            c_arc = rho_arc = float("nan")
            if arc:
                mt = a_th / W; mg = a_g / W; dts = [mt[k + 1] - mt[k] for k in range(arc_windows - 1)]
                dgs = [mg[k + 1] - mg[k] for k in range(arc_windows - 1)]
                na = sum(float(v @ v) for v in dts)
                if na > S.DTH_FLOOR:
                    c_arc = sum(float(e @ v) for e, v in zip(dgs, dts)) / na; rho_arc = sum(float((f_task * v) @ v) for v in dts) / na
            if calib == "none":
                s = 1.0
            else:
                num, den, ok = {"chord": (c, rho, nn > S.DTH_FLOOR), "endpoint": (c_end, rho, nn > S.DTH_FLOOR),
                                "arc5": (c_arc, rho_arc, arc and na > S.DTH_FLOOR)}[calib]
                if ok and np.isfinite(num) and np.isfinite(den) and num > 0 and den > 0: s = num / den
                else: s = 1.0; n_fallback += 1
            svals.append(float(s)); cvals.append(_fin(c)); rhovals.append(_fin(rho)); cends.append(_fin(c_end))
            carcs.append(_fin(c_arc)); rhoarcs.append(_fin(rho_arc))
            imp_bayes = imp_bayes + n_task * s * f_task
            theta_star = theta_now
    return dict(fisher=fisher, calib=calib, penalty=penalty, kappa=float(kappa), seed=int(seed), fs=float(fs), fe=float(fe),
                acc=100 * net.acc(Xte, yte), s=svals, c=cvals, rho=rhovals, c_end=cends, c_arc=carcs if arc else None,
                rho_arc=rhoarcs if arc else None, n_fallback=int(n_fallback), guard_fired=int(fired),
                guard_margins=[round(x, 6) for x in margins], frac_capped=fracs, n_moved=moved if penalty == "freeze" else None,
                finite=bool(np.all(np.isfinite(net.flat()))))


# ---------------------------------------------------------------- identity (M0)
def identity():
    print("=" * 118)
    print("SEC_Analysis M0 identity (SEC_Analysis/DECLARATION.md): m_checks.run_m C0 against the frozen sec4_score.run_guard('clip'),")
    print("the data path, and the construction of M5 and M6 (Amendment 2) on SEC1's synthetic stream")
    print("POST HOC on SEEN carriers; declared checks on seen data, not a test; no ledger row")
    print("=" * 118)
    ref = {m: sha256(ROOT / "runs" / "sec4" / "frozen" / f"{m}.py") for m in ("sec1_score", "scl3_score", "sec4_score")}
    for m, h in ref.items():
        same = [st for st in ("scl3", "sec3", "sec4", "sec5") if (ROOT / "runs" / st / "frozen" / f"{m}.py").exists()
                and sha256(ROOT / "runs" / st / "frozen" / f"{m}.py") == h]
        print(f"frozen {m}.py: runs/sec4/frozen sha256 {h[:16]}...; byte-identical copies in runs/{{{','.join(same)}}}/frozen")
    X, y = S._synthetic(); Xs, ys, meta = LD.select_classes(X, y, 10); K = meta["classes_used"]; data = S.split_standardise(Xs, ys, K)
    k_rg = k_arc = k_e = 0; n_mv = 0; fz = []
    for seed in SEEDS:
        a = P4.run_guard(seed, *data, K, 2, "clip"); b = run_m(seed, *data, K, 2); c = run_m(seed, *data, K, 2, calib="arc5", arc_windows=2)
        f5 = run_m(seed, *data, K, 2, penalty="freeze"); e6 = run_m(seed, *data, K, 2, penalty="edge")
        k_rg += (a["acc"] == b["acc"] and a["s"] == b["s"] and a["guard_fired"] == b["guard_fired"] and a["guard_margins"] == b["guard_margins"])
        k_arc += (c["acc"] == b["acc"] and c["s"] == b["s"])
        n_mv += sum(f5["n_moved"]); fz += f5["frac_capped"]
        k_e += all(x == 1.0 for x in e6["frac_capped"]) and len(e6["frac_capped"]) == len(e6["s"]) - 1
    P4.TIMES.clear()
    print(f"synthetic stream (SEC1's, K {K}, seeds 0-4): C0 equals sec4_score.run_guard('clip') in acc, s, firings and margins on "
          f"{k_rg}/{len(SEEDS)} -> {'IDENTICAL' if k_rg == len(SEEDS) else 'DIFFERS'}")
    print(f"synthetic stream: the arc secant with 2 windows (1 segment) equals C0 in acc and s on {k_arc}/{len(SEEDS)} -> "
          f"{'IDENTICAL' if k_arc == len(SEEDS) else 'DIFFERS'}")
    n_fz = sum(x > 0 for x in fz)
    print(f"synthetic stream: M5 (FREEZE-TOP) froze coordinates on {n_fz} of {len(fz)} guarded tasks (mean fraction {np.mean(fz):.4g}); "
          f"masked coordinates off the anchor at a task's end: {n_mv} -> {'FROZEN' if n_mv == 0 else 'NOT FROZEN'}")
    print(f"synthetic stream: M6 (EDGE) has every coordinate at the cap on every guarded task on {k_e}/{len(SEEDS)} -> "
          f"{'HOLDS' if k_e == len(SEEDS) else 'FAILS'}")
    D = SL.load_all()
    rows = [(st, C) for (st, _), C in D.items() if st in ("sec4", "sec5")]
    print(f"\npinned bayes_sec_clip (kappa 0.5, window 0.1/0.1), seed 0, on the {len(rows)} SEC4 and SEC5 carriers:")
    print(f"   {'study':5} {'carrier':22} {'id':>6} {'pinned acc':>20} {'C0 acc':>20}  acc       s/firings/margins")
    k = 0
    for st, C in rows:
        did = C["header"]["openml_id"]; Xtr, ytr, Xte, yte, K, per_task, name = load(st, did)
        t0 = time.process_time(); o = run_m(0, Xtr, ytr, Xte, yte, K, per_task); dt = time.process_time() - t0
        p = C["primary"]["bayes_sec_clip"].recs[0]; assert p["seed"] == 0 and p["value"] == KAPPA and p["fs"] == S.FS and p["fe"] == S.FE
        same = o["acc"] == p["acc"]; rest = o["s"] == p["s"] and o["guard_fired"] == p["guard_fired"] and o["guard_margins"] == p["guard_margins"]
        k += same
        print(f"   {st:5} {name:22} {did:>6} {p['acc']!r:>20} {o['acc']!r:>20}  {'IDENTICAL' if same else 'DIFFERS':9} {'equal' if rest else 'DIFFER'}")
        print(f"[timing] {st} {name}: C0 seed 0 cpu {dt:.2f} s", file=sys.stderr, flush=True)
    print(f"\nFM0 (identity on {N_IDENTITY} of {N_IDENTITY}): IDENTICAL on {k}/{len(rows)} -> {'HOLDS' if k == N_IDENTITY == len(rows) else 'FAILS'}")
    rows = [(st, C) for (st, _), C in D.items() if st in ("scl3", "sec3")]
    print(f"\ndata path (a check, not a declared forecast): sec4_score.run_guard('none') (SEC1's bayes_sec, SEC4's D-ID), seed 0, against the "
          f"pinned bayes_sec seed 0\non the {len(rows)} SCL3 and SEC3 carriers (no pinned clipped record), data through load() and its cache:")
    print(f"   {'study':5} {'carrier':34} {'id':>6} {'pinned acc':>20} {'rerun acc':>20}  acc       s")
    k = 0
    for st, C in rows:
        did = C["header"]["openml_id"]; Xtr, ytr, Xte, yte, K, per_task, name = load(st, did)
        t0 = time.process_time(); o = P4.run_guard(0, Xtr, ytr, Xte, yte, K, per_task, "none"); dt = time.process_time() - t0
        p = C["primary"]["bayes_sec"].recs[0]; assert p["seed"] == 0 and p["fs"] == S.FS and p["fe"] == S.FE
        same = o["acc"] == p["acc"] and o["s"] == p["s"]; k += same
        print(f"   {st:5} {name:34} {did:>6} {p['acc']!r:>20} {o['acc']!r:>20}  {'IDENTICAL' if o['acc'] == p['acc'] else 'DIFFERS':9} "
              f"{'equal' if o['s'] == p['s'] else 'DIFFER'}")
        print(f"[timing] {st} {name}: run_guard('none') seed 0 cpu {dt:.2f} s", file=sys.stderr, flush=True)
    P4.TIMES.clear()
    print(f"\ndata path on the {len(rows)} SCL3 and SEC3 carriers: acc and s IDENTICAL on {k}/{len(rows)} -> "
          f"{'IDENTICAL' if k == len(rows) else 'DIFFERS'}")


# ---------------------------------------------------------------- one carrier
def run_carrier(study, did, outp):
    d = load(study, did)
    if d is None:
        print(f"{study} {did}: excluded by the loader; nothing run", file=sys.stderr); sys.exit(2)
    Xtr, ytr, Xte, yte, K, per_task, name = d
    tp = Path(outp).resolve().parent / "times" / Path(outp).name           # CPU seconds, kept out of the results file (R9)
    tp.parent.mkdir(parents=True, exist_ok=True)
    with open(outp, "w") as out, open(tp, "w") as tout:
        print(json.dumps(dict(header=1, study=study, dataset=name, openml_id=did, raw_sha256=pinned_header(study, did)["sha256"],
                              **provenance())), file=out, flush=True)
        for arm, (fisher, calib, penalty) in ARMS.items():
            for seed in SEEDS:
                t0 = time.process_time()
                o = run_m(seed, Xtr, ytr, Xte, yte, K, per_task, fisher=fisher, calib=calib, penalty=penalty)
                dt = time.process_time() - t0
                print(json.dumps(dict(arm=arm, study=study, dataset=name, openml_id=did, **o)), file=out, flush=True)
                print(json.dumps(dict(arm=arm, study=study, dataset=name, seed=seed, cpu_s=dt)), file=tout, flush=True)
                print(f"[{study} {name}] {arm} seed {seed}: acc {o['acc']:.4f} fired {o['guard_fired']} fallback {o['n_fallback']} cpu {dt:.2f} s",
                      file=sys.stderr, flush=True)


# ---------------------------------------------------------------- scoring
def _read_mruns():
    """({(study, dataset): {arm: [records by seed]}}, {(study, dataset): header}, [(file name, sha256)])."""
    R, H, F = {}, {}, []
    for p in sorted(glob.glob(str(MRUNS / "*.jsonl"))):
        F.append((Path(p).name, sha256(p)))
        for line in open(p):
            if not line.strip():
                continue
            o = json.loads(line)
            if o.get("header"):
                H[(o["study"], o["dataset"])] = o; continue
            R.setdefault((o["study"], o["dataset"]), {}).setdefault(o["arm"], []).append(o)
    for key, arms in R.items():
        for a, recs in arms.items():
            recs.sort(key=lambda r: r["seed"])
            assert [r["seed"] for r in recs] == list(SEEDS), (key, a, [r["seed"] for r in recs])
    return R, H, F


def _med(v):
    return float(np.median(v)) if len(v) else float("nan")


def _ratios(recs, positive=False):
    """c / c_end over every task of every record with c and c_end finite and c_end != 0 (positive: c > 0 and c_end > 0 only)."""
    out = []
    for r in recs:
        for c, ce in zip(r["c"], r["c_end"]):
            if c is None or ce is None or ce == 0 or (positive and not (c > 0 and ce > 0)):
                continue
            out.append(c / ce)
    return out


def score():
    # the scorer prints Python major.minor only (.python-version pins it; the patch level differs across machines and would make this
    # output machine-dependent, AGENT_LOG 240); each run's full version stays in its m_runs header
    D = SL.load_all(); R, H, F = _read_mruns(); prov = dict(provenance(), python=".".join(platform.python_version_tuple()[:2]))
    want = [(st, name) for (st, name) in D if st in M_STUDIES]
    have = [k for k in want if k in R and all(a in R[k] for a in ARMS)]
    complete = len(have) == len(want)
    print("=" * 118)
    print("SEC_Analysis mechanism checks M0-M6 (SEC_Analysis/DECLARATION.md; M5, M6 from its Amendment 2): C0 (clipped SEC), M1 (model-Fisher")
    print("Laplace), M2 (endpoint curvature), M4 (arc secant), M5 (FREEZE-TOP), M6 (EDGE), all with SEC4's clip (kappa 0.5); M3 (bayes_s1)")
    print("from the pinned records")
    print("POST HOC on SEEN carriers; declared checks on seen data, not a test; no ledger row. tuned lambda, tacc, step: sec_lib")
    print("=" * 118)

    # ---- provenance (R1, R9)
    print(f"provenance: uv.lock sha256 {prov['uv_lock_sha256']}; m_checks.py sha256 {prov['m_checks_sha256']}")
    print(f"            frozen sec4_score.py {prov['sec4_score_sha256']}; sec1_score.py {prov['sec1_score_sha256']}; numpy {prov['numpy']}, "
          f"Python {prov['python']}")
    print(f"the m_runs files read ({len(F)}), with the header each carries (the runner's uv.lock and m_checks.py against the current):")
    k_lock = k_self = k_frz = 0; HF = {f"{v['study']}_{v['openml_id']}.jsonl": v for v in H.values()}
    for fn, h in F:
        hd = HF.get(fn)
        if hd is None:
            print(f"   {fn:22} {h}  no header line"); continue
        sl = hd["uv_lock_sha256"] == prov["uv_lock_sha256"]; ss = hd["m_checks_sha256"] == prov["m_checks_sha256"]
        sf = hd["sec4_score_sha256"] == prov["sec4_score_sha256"] and hd["sec1_score_sha256"] == prov["sec1_score_sha256"]
        k_lock += sl; k_self += ss; k_frz += sf
        print(f"   {fn:22} {h}  uv.lock {'SAME' if sl else 'CHANGED'}, m_checks.py {'SAME' if ss else 'CHANGED'}, frozen {'SAME' if sf else 'CHANGED'}")
    print(f"   headers: uv.lock SAME on {k_lock}/{len(F)}; m_checks.py SAME on {k_self}/{len(F)} (CHANGED means this file was edited after "
          f"the run: the runner's sha256 is in the header); frozen learner SAME on {k_frz}/{len(F)}")

    print(f"\ncarriers with all six arms x seeds 0-4 in m_runs: {len(have)}/{len(want)}" + ("" if complete else
          "; missing: " + ", ".join(f"{s}:{n}" for s, n in want if (s, n) not in have)))
    mean = {k: {a: float(np.mean([r["acc"] for r in R[k][a]])) for a in ARMS} for k in have}
    fired = {k: {a: sum(r["guard_fired"] for r in R[k][a]) for a in ARMS} for k in have}

    # ---- table 1: C0, M1, M2, M4
    print(f"\n{'study':5} {'carrier':34} {'step':>6} {'tuned':>7} {'tacc':>8} | {'C0-tuned':>9} {'fired':>5} | "
          f"{'M1-tuned':>9} {'M1-C0':>8} {'fired':>5} | {'M2-tuned':>9} {'M2-C0':>8} {'fired':>5} | {'M4-tuned':>9} {'M4-C0':>8} {'fired':>5} | c/c_end M2")
    for k in have:
        C = D[k]; st, name = k; mm = mean[k]
        nb = lambda a: "" if SL.not_behind(mm[a], C["tacc"], C["step"]) else "*"  # noqa: E731
        print(f"{st:5} {name:34} {C['step']:6.3f} {C['tuned']:7g} {C['tacc']:8.4f} | {mm['C0'] - C['tacc']:+8.4f}{nb('C0'):1} {fired[k]['C0']:5d} | "
              + " | ".join(f"{mm[a] - C['tacc']:+8.4f}{nb(a):1} {mm[a] - mm['C0']:+8.4f} {fired[k][a]:5d}" for a in ("M1", "M2", "M4"))
              + f" | {_med(_ratios(R[k]['M2'])):.4g}")
    print("   (* = behind the tuned lambda: arm - tacc <= -step; differences are seed means in points; fired = guard firings over seeds and tasks)")

    # ---- table 2: M5, M6 and C0's capped fraction (A13)
    print(f"\n{'study':5} {'carrier':34} {'step':>6} | {'C0 fired':>8} {'seeds':>5} {'C0 capped':>9} {'max':>7} | {'M5-tuned':>9} {'M5-C0':>8} "
          f"{'frozen':>8} {'moved':>5} | {'M6-tuned':>9} {'M6-C0':>8}")
    pc = {}
    for k in have:
        C = D[k]; st, name = k; mm = mean[k]
        nb = lambda a: "" if SL.not_behind(mm[a], C["tacc"], C["step"]) else "*"  # noqa: E731
        c0f = [x for r in R[k]["C0"] for x in r["frac_capped"]]; m5f = [x for r in R[k]["M5"] for x in r["frac_capped"]]
        seeds_f = sum(r["guard_fired"] > 0 for r in R[k]["C0"]); mv = sum(sum(r["n_moved"]) for r in R[k]["M5"])
        pc[f"{st}:{name}"] = dict(study=st, carrier=name, step=C["step"], tuned=C["tuned"], tacc=C["tacc"], means=mm, fired=fired[k],
                                  c0_fired_seeds=seeds_f, c0_frac_capped_mean=float(np.mean(c0f)), c0_frac_capped_max=float(np.max(c0f)),
                                  m5_frac_frozen_mean=float(np.mean(m5f)), m5_moved=mv)
        print(f"{st:5} {name:34} {C['step']:6.3f} | {fired[k]['C0']:8d} {seeds_f:5d} {np.mean(c0f):9.4f} {np.max(c0f):7.4f} | "
              f"{mm['M5'] - C['tacc']:+8.4f}{nb('M5'):1} {mm['M5'] - mm['C0']:+8.4f} {np.mean(m5f):8.4f} {mv:5d} | "
              f"{mm['M6'] - C['tacc']:+8.4f}{nb('M6'):1} {mm['M6'] - mm['C0']:+8.4f}")
    print("   (C0 fired: firings over seeds and tasks; seeds: seeds with a firing; C0 capped: the fraction of coordinates at or above the")
    print("    cap, mean and max over guarded tasks and seeds (0 where the clip did not fire); frozen: M5's frozen fraction, mean over")
    print("    guarded tasks and seeds; moved: M5's masked coordinates off the anchor at a task's end, summed (0 by construction))")

    # ---- counts
    N = len(have)
    nbc = {a: sum(SL.not_behind(mean[k][a], D[k]["tacc"], D[k]["step"]) for k in have) for a in ARMS}
    beh = {a: N - nbc[a] for a in ARMS}
    within4 = sum(abs(mean[k]["M4"] - mean[k]["C0"]) < D[k]["step"] for k in have)
    one4 = sum(mean[k]["M4"] - mean[k]["C0"] > -D[k]["step"] for k in have)
    ahead4 = sum(mean[k]["M4"] - mean[k]["C0"] > D[k]["step"] for k in have)
    fk = [k for k in have if fired[k]["C0"] > 0]; fk_all = [k for k in fk if all(r["guard_fired"] > 0 for r in R[k]["C0"])]
    within5 = sum(abs(mean[k]["M5"] - mean[k]["C0"]) < D[k]["step"] for k in fk)
    one5 = sum(mean[k]["M5"] - mean[k]["C0"] > -D[k]["step"] for k in fk)
    within5_all = sum(abs(mean[k]["M5"] - mean[k]["C0"]) < D[k]["step"] for k in fk_all)
    moved = sum(pc[f"{k[0]}:{k[1]}"]["m5_moved"] for k in have)
    print("\ncounts over the carriers scored here (not behind = arm - tacc > -step):")
    for a in ARMS:
        print(f"   {a}: not behind {nbc[a]}/{N}, behind {beh[a]}/{N}; guard firings {sum(fired[k][a] for k in have)}; "
              f"fallbacks {sum(r['n_fallback'] for k in have for r in R[k][a])}")
    print(f"   M4 against C0: within a step (|M4 - C0| < step) on {within4}/{N}; one-sided M4 - C0 > -step (report) on {one4}/{N}; "
          f"ahead by more than a step on {ahead4}/{N}")
    print(f"   the clip fired (C0, at least one seed) on {len(fk)}/{N} carriers, on every seed on {len(fk_all)}/{N}")
    print(f"   M5 against C0 where the clip fired: within a step on {within5}/{len(fk)}; one-sided M5 - C0 > -step (report) on {one5}/{len(fk)}; "
          f"where it fired on every seed (report): within a step on {within5_all}/{len(fk_all)}")
    print(f"   M5 construction: masked coordinates off the anchor at a task's end, over all records: {moved} -> "
          f"{'FROZEN' if moved == 0 else 'NOT FROZEN'}")

    # ---- FM2's ratio on both paths
    r2 = [x for k in have for x in _ratios(R[k]["M2"])]; r0 = [x for k in have for x in _ratios(R[k]["C0"])]
    r2p = [x for k in have for x in _ratios(R[k]["M2"], True)]; r0p = [x for k in have for x in _ratios(R[k]["C0"], True)]
    n_tasks = {a: sum(len(r["c"]) for k in have for r in R[k][a]) for a in ("M2", "C0")}
    neg2 = len(r2) - len(r2p); neg0 = len(r0) - len(r0p)
    med, med_c0 = _med(r2), _med(r0)
    agree = (med > 1) == (med_c0 > 1)
    print("\nFM2(a), the median over tasks of c / c_end (pooled over carriers, seeds and tasks; c_end != 0 and both finite):")
    print(f"   M2 arm's own path (decisive): median {med!r} ({med:.4g}) over {len(r2)} of {n_tasks['M2']} tasks (c or c_end <= 0 in {neg2}) "
          f"-> > 1: {med > 1}")
    print(f"   C0's path, SEC's own c (report): median {med_c0!r} ({med_c0:.4g}) over {len(r0)} of {n_tasks['C0']} tasks (c or c_end <= 0 in "
          f"{neg0}) -> > 1: {med_c0 > 1}")
    print(f"   the two paths {'AGREE' if agree else 'DISAGREE'} on FM2(a)")
    print(f"   report, tasks with c > 0 and c_end > 0 only: M2 path median {_med(r2p):.4g} over {len(r2p)}; C0 path median {_med(r0p):.4g} "
          f"over {len(r0p)}")

    # ---- the data path, for free (report)
    ck = ci = 0; cc = []; unchecked = []
    for k in have:
        P = D[k]["primary"]["bayes_sec"].recs; n0 = 0
        for r, p in zip(R[k]["C0"], P):
            assert r["seed"] == p["seed"]
            if r["guard_fired"] == 0:
                n0 += 1; ck += 1; ci += (r["acc"] == p["acc"] and r["s"] == p["s"])
        (cc if n0 else unchecked).append(k)
    print(f"\ndata path (report): C0 seeds whose clip never fired against the pinned bayes_sec seed (acc and s): IDENTICAL on {ci}/{ck} seeds "
          f"of {len(cc)} carriers -> {'IDENTICAL' if ci == ck else 'DIFFERS'}")
    print(f"   carriers with no such seed (checked by 'identity' instead, m_identity.txt): "
          + (", ".join(f"{s}:{n}" for s, n in unchecked) if unchecked else "none"))

    # ---- FM3, per carrier (R6)
    all42 = list(D)
    nb42 = {m: sum(SL.arm_nb(D[k], m) for k in all42) for m in ("bayes_sec", "bayes_s1")}
    beh42 = {m: len(all42) - nb42[m] for m in nb42}
    print(f"\nFM3 per carrier (the pinned records, all {len(all42)}): margins against the tuned lambda in steps, * = behind")
    print(f"   {'study':5} {'carrier':34} {'step':>6} {'bayes_sec':>10} {'bayes_s1':>10}")
    for k in all42:
        C = D[k]; ms = {m: SL.margin_steps(C, C["primary"][m].mean) for m in ("bayes_sec", "bayes_s1")}
        fl = {m: "" if SL.arm_nb(C, m) else "*" for m in ms}
        print(f"   {k[0]:5} {k[1]:34} {C['step']:6.3f} {ms['bayes_sec']:+9.3f}{fl['bayes_sec']:1} {ms['bayes_s1']:+9.3f}{fl['bayes_s1']:1}")
    print(f"   pinned (all {len(all42)} carriers of runs/{{sec1,scl3,sec3,sec4,sec5}}): bayes_sec not behind {nb42['bayes_sec']}/{len(all42)} "
          f"(behind {beh42['bayes_sec']}); bayes_s1 not behind {nb42['bayes_s1']}/{len(all42)} (behind {beh42['bayes_s1']})")

    # ---- FM0 from the m_runs C0 records against the pinned bayes_sec_clip (seed 0; all seeds as a report)
    idk = [k for k in have if k[0] in ("sec4", "sec5")]
    id0 = sum(R[k]["C0"][0]["acc"] == D[k]["primary"]["bayes_sec_clip"].recs[0]["acc"] for k in idk)
    idall = sum(all(r["acc"] == p["acc"] for r, p in zip(R[k]["C0"], D[k]["primary"]["bayes_sec_clip"].recs)) for k in idk)

    tag = "" if complete else " [INCOMPLETE: not decided]"
    w = lambda b: ("HOLDS" if b else "FAILS") if complete else "NOT DECIDED"  # noqa: E731
    fm = dict(FM0=len(idk) == N_IDENTITY and id0 == N_IDENTITY, FM1=beh["M1"] > beh["C0"], FM2=(med > 1) and beh["M2"] > beh["C0"],
              FM3=beh42["bayes_s1"] > beh42["bayes_sec"], FM4=within4 >= FM4_SHARE * N,
              FM5=len(fk) > 0 and within5 >= FM5_SHARE * len(fk), FM6=beh["M6"] > FM6_MOST * N)
    print("\nforecasts (DECLARATION.md; FM5, FM6 from Amendment 2):" + tag)
    print(f"   FM0 C0 seed 0 equals the pinned bayes_sec_clip on the SEC4 and SEC5 carriers: {id0}/{len(idk)} (need {N_IDENTITY}/{N_IDENTITY}) -> {w(fm['FM0'])}; "
          f"all five seeds equal on {idall}/{len(idk)} (report)")
    print(f"   FM1 M1 behind on more carriers than C0: M1 {beh['M1']}, C0 {beh['C0']} -> {w(fm['FM1'])}")
    print(f"   FM2 median c / c_end > 1 on the M2 path ({med:.4g}: {med > 1}; C0 path {med_c0:.4g}, {'AGREE' if agree else 'DISAGREE'}) and M2 "
          f"behind on more carriers than C0 (M2 {beh['M2']}, C0 {beh['C0']}: {beh['M2'] > beh['C0']}) -> {w(fm['FM2'])}")
    print(f"   FM3 bayes_s1 behind on more of the {len(all42)} carriers than bayes_sec: {beh42['bayes_s1']} vs {beh42['bayes_sec']} -> {w(fm['FM3'])}")
    print(f"   FM4 M4 within a step of C0 (two-sided) on at least {FM4_SHARE:.0%} of carriers: {within4}/{N} (need {math.ceil(FM4_SHARE * N)}) "
          f"-> {w(fm['FM4'])}; one-sided {one4}/{N} (report)")
    print(f"   FM5 M5 within a step of C0 (two-sided) on at least {FM5_SHARE:.0%} of the {len(fk)} carriers where the clip fired: {within5}/{len(fk)} "
          f"(need {math.ceil(FM5_SHARE * len(fk))}) -> {w(fm['FM5'])}; one-sided {one5}/{len(fk)} (report)")
    print(f"   FM6 M6 behind the tuned lambda on most carriers: {beh['M6']}/{N} (need more than {FM6_MOST * N:g}) -> {w(fm['FM6'])}")
    carry = {a: nbc[a] >= nbc["C0"] - CARRY_SLACK for a in ("M1", "M2")}; carry4 = ahead4 >= M4_AHEAD_MIN
    wc = lambda b, yes, no: (yes if b else no) if complete else "NOT DECIDED"  # noqa: E731
    print("\nSEC6 consequences (DECLARATION.md, 'What the results may change'):" + tag)
    for a in ("M1", "M2"):
        print(f"   {a} not behind {nbc[a]} vs C0 {nbc['C0']} (carried iff >= {nbc['C0'] - CARRY_SLACK}) -> "
              + wc(carry[a], "CARRIED as a baseline that could win (R7)", "NOT CARRIED"))
    print(f"   M4 ahead of C0 by more than a step on {ahead4} (needs >= {M4_AHEAD_MIN}) -> "
          + wc(carry4, "MAY BE CARRIED as a two-sided candidate", "a TIE or a loss, NOT CARRIED"))
    out = dict(complete=complete, n_carriers=N, not_behind=nbc, behind=beh, pinned42=dict(n=len(all42), not_behind=nb42, behind=beh42),
               median_c_over_cend_M2=med, n_ratio_tasks=len(r2), median_c_over_cend_C0=med_c0, fm2a_paths_agree=agree,
               median_c_over_cend_positive=dict(M2=_med(r2p), C0=_med(r0p)), m4_within_step=within4, m4_one_sided=one4,
               m4_ahead_step=ahead4, clip_fired_carriers=len(fk), clip_fired_every_seed=len(fk_all), m5_within_step=within5,
               m5_one_sided=one5, m5_moved=moved, identity_seed0=id0, identity_all_seeds=idall, n_identity=len(idk),
               data_path=dict(seeds=ck, identical=ci, carriers=len(cc)),
               forecasts={k: (("HOLDS" if v else "FAILS") if complete else "NOT DECIDED") for k, v in fm.items()},
               sec6=dict(M1=carry["M1"], M2=carry["M2"], M4=carry4) if complete else None, per_carrier=pc,
               provenance=dict(prov, m_runs={fn: h for fn, h in F}))
    with open(HERE / "m_checks.json", "w") as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write("\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "identity":
        identity()
    elif cmd == "list":
        for st, did in carriers():
            print(st, did)
    elif cmd == "run":
        st, did = sys.argv[2], int(sys.argv[3])
        MRUNS.mkdir(parents=True, exist_ok=True)
        outp = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else str(MRUNS / f"{st}_{did}.jsonl")
        run_carrier(st, did, outp)
    elif cmd == "score":
        score()
    else:
        raise SystemExit(__doc__)
