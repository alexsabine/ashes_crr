"""Hypothesis gate (CLAUDE.md R4).

    uv run python -m crr.surrogates.gate L5
    uv run python -m crr.surrogates.gate CUT
    uv run python -m crr.surrogates.gate T1
    uv run python -m crr.surrogates.gate EQ      # replay weighting (convex replay learners)
    uv run python -m crr.surrogates.gate L5R     # H-L5 on count/rate carriers, Poisson and identity metric
    uv run python -m crr.surrogates.gate A3      # antipodal-cut vs peak-cut arc regularity (diagnostic)

Prints one row per surrogate: the statistic, PASS/FAIL under the candidate
criterion, and whether that outcome is the one theory/CRR.md requires. Commit
the output into prereg/<study>/gate_<hyp>.txt (the standing Phase-A outputs
are committed at runs/phaseA/gate_<hyp>.txt). A hypothesis whose row for a
"must fail" surrogate reads PASS may not enter a pre-registration.
"""
from __future__ import annotations

import sys

import numpy as np

from crr.instrument.core import (antipodal_cuts, arc_length, cv, intrinsic_phase, kl_gauss,
                                 path_length, peak_cuts, poisson_transform, regularity, rho,
                                 unit_sigma)
from crr.surrogates.battery import BATTERY, LEARNER_BATTERY, RATE_BATTERY, REPLAY_BATTERY, SALIENCE_BATTERY

# Negative controls: the hypothesis MUST fail here (no CRR content, or nothing to distinguish).
MUST_FAIL = {
    "L5": {"S-A sine", "S-A'' AM sine (constant period)",
           "S-G relaxation osc. (clock-regular, amplitude-variable)"},
    "CUT": {"S-A sine", "S-F van der Pol mu=5.0", "S-F van der Pol mu=1.0"},
    "T1": {"S-H convex learner (endpoint-sufficient)"},
    "EQ": {"S-R convex replay, constant label scale (adaptivity idle)"},
    # EQ2 (issue #20 §3): same-units replay stays redundant, and a constraint whose
    # tuned weight is a small fraction of the present pull is over-regularised by
    # same-length pulling. If either passes, the mechanism statement is wrong.
    "EQ2": {"S-R convex replay, constant label scale (adaptivity idle)",
            "S-X constraint learner, tuned weight a small fraction of present norm",
            "S-Y/LwF softmax MLP, distillation constraint (input scale 4)"},
    "SAL": {"S-SAL-F equal task difficulty (surplus flat)",
            "S-SAL-D surplus inflated by gradient noise (decoupled from forgetting)"},
    "L5R": {"S-P AM epidemics (constant period, variable peak)",
            "S-P AM+FM epidemics (the concavity trap: no CRR content)",
            "S-P clock-regular two-hump (constant period, variable arc)"},
    # L5x-3 (CLAUDE.md §4): where antipode and extremum coincide there is nothing to test
    "A3": {"S-A sine", "S-A'' AM sine (constant period)", "S-F van der Pol mu=5.0"},
}
# Positive controls: the hypothesis is TRUE by construction here and MUST pass,
# otherwise the instrument cannot see it.
MUST_PASS = {
    "L5": {"S-A' FM sine (constant amplitude)", "S-G2 relaxation osc. (arc-regular by construction)"},
    "CUT": {"S-E asymmetric multi-harmonic"},
    "T1": {"S-H2 wear learner (path-dependent by construction)"},
    "EQ": {"S-V convex replay, 16x label-scale swings (adaptivity load-bearing)"},
    # EQ2 (issue #20 §3): the exact Laplace penalty of a past quadratic loss with a
    # 16x curvature-scale mismatch is where the rule has a use (tuning-free EWC step).
    # PR #23 showed the convex S-W row cannot open (a fixed weight is metric-optimal on a
    # quadratic); S-W stays as an informational row. The positive control is the nonconvex
    # S-Y row, where the present gradient decays within a task.
    "EQ2": {"S-Y softmax MLP, online EWC, 16x Fisher-scale mismatch (input scale 4)"},
    "SAL": {"S-SAL-P unequal task difficulty (surplus tracks forgetting)"},
    "L5R": {"S-P FM two-hump compensating (arc constant, amplitude variable)"},
    "A3": set(),   # no positive control is known for this comparison; stated in the prereg that uses it
}


def gate_L5(x, ev, meta):
    """CV(arc) < CV(clock) with the amplitude control: a PASS requires the arc
    inequality to hold AND arc to beat the amplitude-only CV.

    The criterion is SCALE-FREE: CV is invariant under any positive rescaling
    of the statistic, so no sigma enters the comparison and the unit_sigma
    estimate is not consulted here (a degenerate unit scale must not flip a
    verdict). rho = extent/sigma (extent = mean peak-to-peak of an occasion
    trace) is REPORTED per row, never used inside the criterion (R5).

    Amplitude control (CRR.md [H-L5] control (i)), scored as CRR.md prescribes
    — by the PAIRED bootstrap on the CV difference, not by point CVs: it
    vetoes only when amplitude alone is significantly more regular than the
    arc (ci95_amp excluding 0 on the amplitude side). Point CVs of arc and
    peak-to-peak amplitude are proportional on constant-period carriers and
    tie at instrument resolution (a ~1e-14 relative gap is float dust, which
    a strict point comparison turned into a spurious veto)."""
    if ev is None or len(ev) < 12:
        return None
    r = regularity(x, ev, sigma=1.0)
    extent = float(np.mean([np.ptp(x[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])]))
    res = rho(extent, 1.0)
    passes = ((r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0)
              and not (r["ci95_amp"][0] > 0))
    detail = (f"cv_arc={r['cv_arc']:.3f} cv_clock={r['cv_clock']:.3f} cv_amp={r['cv_amp']:.3f} "
              f"ci={r['ci95'][0]:.3f},{r['ci95'][1]:.3f} ci_amp={r['ci95_amp'][0]:.3f},{r['ci95_amp'][1]:.3f} "
              f"C_mean={r['C_mean']:.2f}sigma rho={res:.2f}")
    return passes, detail


def gate_CUT(x, ev, meta, prominence_frac=0.3, distance_frac=0.4, disagree_threshold=0.05):
    """Testability of A3: do antipodal and dominant-extremum cuts disagree?
    Period is taken from the phase; peak detection uses one max + one min per
    cycle (distance = distance_frac * period, prominence = prominence_frac *
    range; both named parameters), as a physiology pipeline would. Phase
    counting starts at the SECOND detected peak (p[1]), so on a symmetric
    cycle antipodes land on troughs and the two coincide -> FAIL.

    S-D rows are noise reference lines (SCOPE.md §7.4): they report the
    antipode-extremum disagreement on noise-only signals at a given rho.
    They are neither positive nor negative controls and carry no verdict
    weight; main() annotates them as such."""
    ph = intrinsic_phase(x)
    period = 2 * np.pi / max(np.median(np.diff(ph)), 1e-9)
    p = peak_cuts(x, prominence=prominence_frac * np.ptp(x),
                  distance=max(int(distance_frac * period), 2))
    if len(p) < 5:
        return None
    a = antipodal_cuts(ph, start=int(p[1]))
    if len(a) < 5:
        return None
    d = np.array([np.min(np.abs(p - c)) for c in a[1:]])
    disagree = np.median(d) / (period / 2)
    return disagree > disagree_threshold, f"median |antipode-extremum| = {disagree:.3f} half-turns"


def _heldout_r2(pred, F, fit_mask, covariates=None):
    """OLS F ~ a + b*pred (optionally + nuisance covariate columns, e.g. lr)
    on the fit half; R^2 on the held-out half (never in-sample).

    Raises ValueError when the fit half has < 2 rows or the held-out half has
    zero variance: R^2 is undefined there, and a NaN would silently lose
    every comparison. gate_T1 turns that into an n/a row."""
    if int(fit_mask.sum()) < 2:
        raise ValueError("fewer than 2 fit rows: R^2 undefined")
    cols = [np.ones(int(fit_mask.sum())), pred[fit_mask]]
    if covariates is not None:
        cols.append(np.asarray(covariates)[fit_mask])
    A = np.column_stack(cols)
    coef = np.linalg.lstsq(A, F[fit_mask], rcond=None)[0]
    Fh = F[~fit_mask]
    hcols = [np.ones(int((~fit_mask).sum())), pred[~fit_mask]]
    if covariates is not None:
        hcols.append(np.asarray(covariates)[~fit_mask])
    Fp = np.column_stack(hcols) @ coef
    ss_h = float(np.sum((Fh - Fh.mean()) ** 2))
    if ss_h <= 0.0:
        raise ValueError("held-out half has zero variance: R^2 undefined")
    return 1.0 - float(np.sum((Fh - Fp) ** 2)) / ss_h


def gate_T1(runs, _ev, meta, margin=0.05):
    """H-T1 in the T1x-1 form: held-out R^2 of the best PATH predictor (C_new, C_old)
    beats the best ENDPOINT predictor (E_new, E_old) by >= margin. E_old is a
    required baseline: on a convex learner it is a sufficient statistic for
    forgetting (SCOPE.md lemma), so a path win over E_new alone would only show
    that the old probe beats the new probe. Split: even seeds fit, odd seeds score.

    Surrogate-only limitation: the pooled best-vs-best margin is THE criterion
    here, but lr is NOT controlled across runs (each run carries its own lr
    from the grid). Pre-registered scoring must control lr per CLAUDE.md §5
    (T1x-1). For visibility the detail string also reports the partial R^2
    (controlling for lr) of the winning path and endpoint predictors; those
    columns do not decide the gate."""
    if len(runs) < 20:
        return None
    q = {k: [] for k in ("C_new", "C_old", "E_new", "E_old", "S_new", "S_old")}
    F = np.array([r["F"] for r in runs])
    for r in runs:
        pn = path_length(r["pred_new"], kl=kl_gauss); po = path_length(r["pred_old"], kl=kl_gauss)
        q["C_new"].append(pn["C"]); q["E_new"].append(pn["E"]); q["S_new"].append(pn["S"])
        q["C_old"].append(po["C"]); q["E_old"].append(po["E"]); q["S_old"].append(po["S"])
    lr = np.array([float(r["lr"]) for r in runs])
    fit = np.array([r["seed"] % 2 == 0 for r in runs])
    try:
        r2 = {k: _heldout_r2(np.asarray(v), F, fit) for k, v in q.items() if k[0] in "CE"}
    except ValueError:
        # R^2 undefined on this battery split: report an n/a row instead of a
        # NaN comparison (which would read as a spurious FAIL/PASS).
        return None
    best_C = max(r2["C_new"], r2["C_old"]); best_E = max(r2["E_new"], r2["E_old"])
    passes = best_C >= best_E + margin
    detail = " ".join(f"R2({k})={v:.3f}" for k, v in r2.items())
    detail += f"  |  path-endpoint={best_C - best_E:+.3f}  n={len(runs)}  S<0 in {np.mean(np.asarray(q['S_old']) < 0):.0%} of runs (old probe)"
    key_C = "C_new" if r2["C_new"] >= r2["C_old"] else "C_old"
    key_E = "E_new" if r2["E_new"] >= r2["E_old"] else "E_old"
    try:
        pr2 = {k: _heldout_r2(np.asarray(q[k]), F, fit, covariates=lr) for k in (key_C, key_E)}
        detail += "  |  partial-R2(+lr): " + " ".join(f"R2({k}|lr)={v:.3f}" for k, v in pr2.items())
    except ValueError:
        pass  # partial R^2 undefined on this split; omit the visibility column
    return passes, detail


def gate_EQ(runner, _ev, meta, seeds=range(5), fixed_grid=(0.25, 0.5, 1.0, 2.0, 4.0),
            omega_grid=(0.5, 0.71, 1.0, 1.41, 2.0), margin=0.05):
    """H-EQ in the reduction form (CLAUDE.md §6 EQ-1 / theory [H-EQ]): the adaptive rule at
    Omega = 1 counts as a result only if it beats ER-sum (fixed w = 1) AND the best fixed w,
    where the fixed grid is extended by the adaptive rule's own median w (the constant it
    reduces to). Metric: normalised held-out MSE over all tasks, lower is better; PASS if
    the relative improvement over the best fixed w is >= margin in the seed mean AND in a
    majority of seeds. Omega landscape reported, not gated."""
    seeds = list(seeds)
    fixed_grid = tuple(meta.get("fixed_grid", fixed_grid))   # a row may widen the grid so its baseline can win (R7)
    eq = {om: np.array([runner("eq", om, s)["metric"] for s in seeds]) for om in omega_grid}
    wmed = float(np.median([runner("eq", 1.0, s)["w_med"] for s in seeds]))
    grid = tuple(sorted(set(fixed_grid) | {round(wmed, 3)}))
    fx = {w: np.array([runner("fixed", w, s)["metric"] for s in seeds]) for w in grid}
    best_w = min(fx, key=lambda w: fx[w].mean())
    rel = (fx[best_w] - eq[1.0]) / fx[best_w]           # >0 means adaptive better
    rel_sum = (fx[1.0] - eq[1.0]) / fx[1.0]
    passes = (rel.mean() >= margin) and (np.mean(rel > 0) > 0.5) and (rel_sum.mean() >= margin)
    best_om = min(eq, key=lambda o: eq[o].mean())
    detail = (f"EQ(Ω=1)={eq[1.0].mean():.4f} ER-sum(w=1)={fx[1.0].mean():.4f} best fixed w={best_w}:{fx[best_w].mean():.4f} "
              f"(w_med of EQ={wmed:.3f}) | rel.gain vs best fixed {rel.mean():+.3f} (seeds>0: {int((rel>0).sum())}/{len(seeds)}) "
              f"vs ER-sum {rel_sum.mean():+.3f} | best Ω={best_om} landscape " + " ".join(f"{o}:{eq[o].mean():.3f}" for o in omega_grid))
    return passes, detail


def gate_EQ2(runner, _ev, meta, seeds=range(5), fixed_grid=(0.0625, 0.25, 0.5, 1.0, 2.0, 4.0),
             omega_grid=(0.5, 0.71, 1.0, 1.41, 2.0), margin=0.05):
    """EQ2 statistic (issue #20 §3): the rule at Omega = 1 is NOT BEHIND the tuned
    fixed weight by a step. The fixed weight is tuned ON THE SCORED SEEDS -- in-sample
    bias that favours the baseline, and that is the design intent: the criterion is
    one-sided, the rule need only not lose. A step is the relative margin `margin`
    (gate_EQ's); the rule is behind by a step iff mean((rule - tuned)/tuned) > margin,
    counted per seed and reported. fixed_grid is gate_EQ's grid extended to 0.0625:
    the 16x-stiff Laplace penalty moves the tuned weight below the replay family's,
    and R7 requires the baseline to be able to win. The Omega landscape and the
    reduction arm (fixed w at the rule's own median w, the constant it reduces to)
    are reported, not gated."""
    seeds = list(seeds)
    fixed_grid = tuple(meta.get("fixed_grid", fixed_grid))   # a row may widen the grid so its baseline can win (R7)
    eq = {om: np.array([runner("eq", om, s)["metric"] for s in seeds]) for om in omega_grid}
    wmed = float(np.median([runner("eq", 1.0, s)["w_med"] for s in seeds]))
    wm = round(wmed, 3)
    grid = tuple(sorted(set(fixed_grid) | {wm}))
    fx = {w: np.array([runner("fixed", w, s)["metric"] for s in seeds]) for w in grid}
    tuned_w = min(fx, key=lambda w: fx[w].mean())
    behind = (eq[1.0] - fx[tuned_w]) / fx[tuned_w]      # >0: the rule is behind the tuned weight
    passes = bool(behind.mean() <= margin)
    best_om = min(eq, key=lambda o: eq[o].mean())
    detail = (f"EQ(Ω=1)={eq[1.0].mean():.4f} tuned w={tuned_w}:{fx[tuned_w].mean():.4f} "
              f"(w_med of EQ={wmed:.3f}) | behind-by {behind.mean():+.3f} (seeds>step: {int((behind > margin).sum())}/{len(seeds)}) "
              f"| best Ω={best_om} landscape " + " ".join(f"{o}:{eq[o].mean():.3f}" for o in omega_grid)
              + f" | reduction arm w={wm}:{fx[wm].mean():.4f}")
    return passes, detail


def gate_SAL(runner, _ev, meta, seeds=range(5), lam_grid=(-1.0, -0.5, -0.25, 0.0, 0.1, 0.25, 0.5, 1.0, 2.0), margin=1.0, min_seeds=4):
    """Study-SAL instrument-sensitivity statistic: SOME lambda on the pre-registered grid makes
    salience-weighted replay beat uniform replay (lambda = 0) by >= `margin` accuracy points on
    the seed mean, positive in >= `min_seeds` seeds. This is the gate for the spec's three-way
    protocol (lambda = 0 / lambda = 1 / free lambda): a positive control must show the instrument
    can see a salience effect at all; the law's own value lambda = 1 is then scored by the study,
    and its gain is printed here for the record. Also printed: the anti-salience arm, the
    surplus values under lambda = 0, and the Spearman correlation across past tasks between
    surplus and forgetting."""
    from scipy.stats import spearmanr
    seeds = list(seeds)
    acc = {lam: np.array([runner(lam, s)["acc"] for s in seeds]) for lam in lam_grid}
    r0 = [runner(0.0, s) for s in seeds]
    gain = {lam: acc[lam] - acc[0.0] for lam in lam_grid}
    best = max(lam_grid, key=lambda l: gain[l].mean())
    passes = bool(gain[best].mean() >= margin and int((gain[best] > 0).sum()) >= min_seeds)
    S_mean = np.mean([r["S"] for r in r0], 0)
    rho = float(np.mean([spearmanr(r["S"][:-1], r["forgetting"][:-1]).statistic for r in r0]))
    detail = (f"acc(lam=0) {acc[0.0].mean():.2f} | gain over lam=0: " + " ".join(f"{l:+g}:{gain[l].mean():+.2f}({int((gain[l] > 0).sum())})" for l in lam_grid)
              + f" | best lam={best:+g} | lam=1 gain {gain[1.0].mean():+.2f} | S per task {np.round(S_mean, 2).tolist()} | Spearman(S, forgetting) {rho:+.2f}")
    return passes, detail

def gate_L5R(x, ev, meta, metric="poisson"):
    """H-L5 on a count/rate carrier, scored as study MEAS pre-registers it.

    metric="poisson": y = 2*sqrt(x) (Fisher-Rao arc of the rate, P6/P9);
    metric="identity": y = x (arc = total variation of the counts).
    PASS requires ALL of: cv_arc < cv_clock; paired-bootstrap 95% CI of
    (cv_arc - cv_clock) below 0; AND control (i) beaten SIGNIFICANTLY: the paired
    95% CI of (cv_arc - cv_amp), amplitude measured in the same metric, below 0.
    A tie with amplitude is not 'beyond' amplitude, whichever way float dust falls.
    Note the one-hump FM row: arc ties amplitude there and must therefore FAIL this
    criterion although it passes the plain inequality — it is not a positive control
    for 'beyond control (i)'; the two-hump compensating row is."""
    if ev is None or len(ev) < 12:
        return None
    y = poisson_transform(x) if metric == "poisson" else np.asarray(x, float)
    r = regularity(y, ev, sigma=1.0)
    passes = (r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0) and (r["ci95_amp"][1] < 0)
    return passes, (f"cv_arc={r['cv_arc']:.3f} cv_clock={r['cv_clock']:.3f} cv_amp={r['cv_amp']:.3f} "
                    f"ci={r['ci95'][0]:.3f},{r['ci95'][1]:.3f} ci_amp={r['ci95_amp'][0]:.3f},{r['ci95_amp'][1]:.3f}")


def gate_A3(x, ev, meta, n_boot=2000, seed=0):
    """L5x-3 as study CARD scores it: CV of the arc between ANTIPODAL cuts (intrinsic phase,
    counting from the first detected peak) vs CV of the arc between PEAK cuts (maxima and
    minima, find_peaks). PASS iff cv_antipodal < cv_peak and the bootstrap 95% CI of the
    difference lies below 0. On symmetric carriers the two cut sets coincide, so the
    comparison must read FAIL there (nothing to test)."""
    x = np.asarray(x, float)
    ph = intrinsic_phase(x)
    period = 2 * np.pi / max(np.median(np.diff(ph)), 1e-9)
    pk = peak_cuts(x, prominence=0.3 * np.ptp(x), distance=max(int(0.4 * period), 2))
    if len(pk) < 12:
        return None
    ant = antipodal_cuts(ph, start=int(pk[1]))
    if len(ant) < 12:
        return None
    Ca = np.array([arc_length(x[a:b + 1]) for a, b in zip(ant[:-1], ant[1:]) if b > a])
    Cp = np.array([arc_length(x[a:b + 1]) for a, b in zip(pk[:-1], pk[1:]) if b > a])
    rng = np.random.default_rng(seed)
    d = [cv(Ca[rng.integers(0, len(Ca), len(Ca))]) - cv(Cp[rng.integers(0, len(Cp), len(Cp))]) for _ in range(n_boot)]
    lo, hi = np.percentile(d, [2.5, 97.5])
    passes = bool(cv(Ca) < cv(Cp) and hi < 0)
    return passes, f"cv_antipodal={cv(Ca):.3f} cv_peakcut={cv(Cp):.3f} ci={lo:.3f},{hi:.3f} n_ant={len(ant)} n_pk={len(pk)}"


GATES = {"L5": gate_L5, "CUT": gate_CUT, "T1": gate_T1, "EQ": gate_EQ, "EQ2": gate_EQ2, "L5R": gate_L5R, "A3": gate_A3, "SAL": gate_SAL}
LEARNER_GATES = {"T1"}
REPLAY_GATES = {"EQ", "EQ2"}
SALIENCE_GATES = {"SAL"}
RATE_GATES = {"L5R"}


def _score_row(out, name, hyp):
    """Print one gate row; return 1 if it violates its control role, else 0."""
    if out is None:
        print(f"  {name:55s} n/a")
        return 0
    passes, detail = out
    if name in MUST_FAIL[hyp]:
        ok = not passes; why = "passes on a negative control"
    elif name in MUST_PASS[hyp]:
        ok = passes; why = "fails on a positive control (instrument cannot see the effect)"
    else:
        ok = True; why = ""
    # S-D rows are noise reference lines (SCOPE.md §7.4), not controls.
    ref = " (noise reference line, SCOPE §7.4)" if hyp == "CUT" and name.startswith("S-D") else ""
    flag = "" if ok else f"   <-- VIOLATION: {why}"
    print(f"  {name:55s} {'PASS' if passes else 'FAIL':4s}  {detail}{ref}{flag}")
    return int(not ok)


def main(hyp: str):
    g = GATES[hyp]
    print(f"gate for {hyp}\n  must FAIL on {sorted(MUST_FAIL[hyp])}\n  must PASS on {sorted(MUST_PASS[hyp])}\n")
    bad = 0
    battery = (LEARNER_BATTERY if hyp in LEARNER_GATES else REPLAY_BATTERY if hyp in REPLAY_GATES
               else SALIENCE_BATTERY if hyp in SALIENCE_GATES else RATE_BATTERY if hyp in RATE_GATES else BATTERY)
    metrics = ("poisson", "identity") if hyp in RATE_GATES else (None,)
    for metric in metrics:
        if metric is not None:
            print(f"  --- metric = {metric} ---")
        for gen in battery:
            x, ev, meta = gen()
            out = g(x, ev, meta) if metric is None else g(x, ev, meta, metric=metric)
            bad += _score_row(out, meta["name"], hyp)
    print()
    print("GATE OPEN" if bad == 0 else f"GATE CLOSED ({bad} violation(s)): restate the hypothesis or add a control")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
