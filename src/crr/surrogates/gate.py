"""Hypothesis gate (CLAUDE.md R4).

    uv run python -m crr.surrogates.gate L5
    uv run python -m crr.surrogates.gate CUT
    uv run python -m crr.surrogates.gate T1

Prints one row per surrogate: the statistic, PASS/FAIL under the candidate
criterion, and whether that outcome is the one theory/CRR.md requires. Commit
the output into prereg/<study>/gate_<hyp>.txt (the standing Phase-A outputs
are committed at runs/phaseA/gate_<hyp>.txt). A hypothesis whose row for a
"must fail" surrogate reads PASS may not enter a pre-registration.
"""
from __future__ import annotations

import sys

import numpy as np

from crr.instrument.core import (antipodal_cuts, intrinsic_phase, kl_gauss, path_length,
                                 peak_cuts, regularity, rho)
from crr.surrogates.battery import BATTERY, LEARNER_BATTERY

# Negative controls: the hypothesis MUST fail here (no CRR content, or nothing to distinguish).
MUST_FAIL = {
    "L5": {"S-A sine", "S-A'' AM sine (constant period)",
           "S-G relaxation osc. (clock-regular, amplitude-variable)"},
    "CUT": {"S-A sine", "S-F van der Pol mu=5.0", "S-F van der Pol mu=1.0"},
    "T1": {"S-H convex learner (endpoint-sufficient)"},
}
# Positive controls: the hypothesis is TRUE by construction here and MUST pass,
# otherwise the instrument cannot see it.
MUST_PASS = {
    "L5": {"S-A' FM sine (constant amplitude)", "S-G2 relaxation osc. (arc-regular by construction)"},
    "CUT": {"S-E asymmetric multi-harmonic"},
    "T1": {"S-H2 wear learner (path-dependent by construction)"},
}


def gate_L5(x, ev, meta):
    """CV(arc) < CV(clock) with the amplitude control: a PASS requires the arc
    inequality to hold AND arc to beat the amplitude-only CV.

    The criterion is SCALE-FREE: CV is invariant under any positive rescaling
    of the statistic, so no sigma enters the comparison and the unit_sigma
    estimate is not consulted here (a degenerate unit scale must not flip a
    verdict). rho = extent/sigma (extent = mean peak-to-peak of a half-turn
    trace) is REPORTED per row, never used inside the criterion (R5)."""
    if ev is None or len(ev) < 12:
        return None
    r = regularity(x, ev, sigma=1.0)
    extent = float(np.mean([np.ptp(x[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])]))
    res = rho(extent, 1.0)
    passes = (r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0) and (r["cv_arc"] < r["cv_amp"])
    detail = (f"cv_arc={r['cv_arc']:.3f} cv_clock={r['cv_clock']:.3f} cv_amp={r['cv_amp']:.3f} "
              f"ci={r['ci95'][0]:.3f},{r['ci95'][1]:.3f} C_mean={r['C_mean']:.2f}sigma rho={res:.2f}")
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


GATES = {"L5": gate_L5, "CUT": gate_CUT, "T1": gate_T1}
LEARNER_GATES = {"T1"}


def main(hyp: str):
    g = GATES[hyp]
    print(f"gate for {hyp}\n  must FAIL on {sorted(MUST_FAIL[hyp])}\n  must PASS on {sorted(MUST_PASS[hyp])}\n")
    bad = 0
    for gen in (LEARNER_BATTERY if hyp in LEARNER_GATES else BATTERY):
        x, ev, meta = gen()
        out = g(x, ev, meta)
        name = meta["name"]
        if out is None:
            print(f"  {name:55s} n/a")
            continue
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
        bad += (not ok)
        print(f"  {name:55s} {'PASS' if passes else 'FAIL':4s}  {detail}{ref}{flag}")
    if hyp in LEARNER_GATES:
        print("\n  (EQ is not gated yet: gate_EQ needs a replay learner and the ER-sum control; see SCOPE.md §6)")
    print()
    print("GATE OPEN" if bad == 0 else f"GATE CLOSED ({bad} violation(s)): restate the hypothesis or add a control")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
