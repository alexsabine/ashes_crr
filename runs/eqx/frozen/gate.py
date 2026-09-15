"""Hypothesis gate (CLAUDE.md R4).

    uv run python surrogates/gate.py L5
    uv run python surrogates/gate.py CUT
    uv run python surrogates/gate.py T1
    uv run python surrogates/gate.py EQ

Prints one row per surrogate: the statistic, PASS/FAIL under the candidate
criterion, and whether that outcome is the one theory/CRR.md requires. Commit
the output into prereg/<study>/gate_<hyp>.txt. A hypothesis whose row for a
"must fail" surrogate reads PASS may not enter a pre-registration.
"""
from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")
from instrument.core import (antipodal_cuts, intrinsic_phase, kl_gauss, path_length,  # noqa: E402
                             peak_cuts, regularity, unit_sigma)
from surrogates.battery import BATTERY, LEARNER_BATTERY, REPLAY_BATTERY  # noqa: E402

# Negative controls: the hypothesis MUST fail here (no CRR content, or nothing to distinguish).
MUST_FAIL = {
    "L5": {"S-A sine", "S-A'' AM sine (constant period)",
           "S-G relaxation osc. (clock-regular, amplitude-variable)"},
    "CUT": {"S-A sine", "S-F van der Pol mu=5.0"},
    "T1": {"S-H convex learner (endpoint-sufficient)"},
    "EQ": {"S-R convex replay, constant label scale (adaptivity idle)"},
}
# Positive controls: the hypothesis is TRUE by construction here and MUST pass,
# otherwise the instrument cannot see it.
MUST_PASS = {
    "L5": {"S-A' FM sine (constant amplitude)", "S-G2 relaxation osc. (arc-regular by construction)"},
    "CUT": {"S-E asymmetric multi-harmonic"},
    "T1": {"S-H2 wear learner (path-dependent by construction)"},
    "EQ": {"S-V convex replay, 16x label-scale swings (adaptivity load-bearing)"},
}


def gate_L5(x, ev, meta):
    """CV(arc) < CV(clock) with the amplitude control: a PASS requires the arc
    inequality to hold AND arc to beat the amplitude-only CV."""
    if ev is None or len(ev) < 12:
        return None
    seg_amp = np.array([np.ptp(x[a:b]) for a, b in zip(ev[:-1], ev[1:])])
    try:
        sig = unit_sigma(seg_amp[: len(seg_amp) // 2])
    except ValueError:
        sig = 1.0
    r = regularity(x, ev, sigma=sig)
    passes = (r["cv_arc"] < r["cv_clock"]) and (r["ci95"][1] < 0) and (r["cv_arc"] < r["cv_amp"])
    return passes, f"cv_arc={r['cv_arc']:.3f} cv_clock={r['cv_clock']:.3f} cv_amp={r['cv_amp']:.3f} ci={r['ci95'][0]:.3f},{r['ci95'][1]:.3f}"


def gate_CUT(x, ev, meta):
    """Testability of A3: do antipodal and dominant-extremum cuts disagree?
    Period is taken from the phase; peak detection uses one max + one min per
    cycle (distance = 0.4 period, prominence = 0.3 range), as a physiology
    pipeline would. Phase counting starts at the first detected peak, so on a
    symmetric cycle antipodes land on troughs and the two coincide -> FAIL."""
    ph = intrinsic_phase(x)
    period = 2 * np.pi / max(np.median(np.diff(ph)), 1e-9)
    p = peak_cuts(x, prominence=0.3 * np.ptp(x), distance=max(int(0.4 * period), 2))
    if len(p) < 5:
        return None
    a = antipodal_cuts(ph, start=int(p[1]))
    if len(a) < 5:
        return None
    d = np.array([np.min(np.abs(p - c)) for c in a[1:]])
    disagree = np.median(d) / (period / 2)
    return disagree > 0.05, f"median |antipode-extremum| = {disagree:.3f} half-turns"


def _heldout_r2(pred, F, fit_mask):
    """OLS F ~ a + b*pred on the fit half; R^2 on the held-out half (never in-sample)."""
    A = np.c_[np.ones(fit_mask.sum()), pred[fit_mask]]
    coef = np.linalg.lstsq(A, F[fit_mask], rcond=None)[0]
    Fh = F[~fit_mask]; Fp = coef[0] + coef[1] * pred[~fit_mask]
    return 1.0 - np.sum((Fh - Fp) ** 2) / np.sum((Fh - Fh.mean()) ** 2)


def gate_T1(runs, _ev, meta, margin=0.05):
    """H-T1 in the T1x-1 form: held-out R^2 of the best PATH predictor (C_new, C_old)
    beats the best ENDPOINT predictor (E_new, E_old) by >= margin. E_old is a
    required baseline: on a convex learner it is a sufficient statistic for
    forgetting (SCOPE.md lemma), so a path win over E_new alone would only show
    that the old probe beats the new probe. Split: even seeds fit, odd seeds score."""
    if len(runs) < 20:
        return None
    q = {k: [] for k in ("C_new", "C_old", "E_new", "E_old", "S_new", "S_old")}
    F = np.array([r["F"] for r in runs])
    for r in runs:
        pn = path_length(r["pred_new"], kl=kl_gauss); po = path_length(r["pred_old"], kl=kl_gauss)
        q["C_new"].append(pn["C"]); q["E_new"].append(pn["E"]); q["S_new"].append(pn["S"])
        q["C_old"].append(po["C"]); q["E_old"].append(po["E"]); q["S_old"].append(po["S"])
    fit = np.array([r["seed"] % 2 == 0 for r in runs])
    r2 = {k: _heldout_r2(np.asarray(v), F, fit) for k, v in q.items() if k[0] in "CE"}
    best_C = max(r2["C_new"], r2["C_old"]); best_E = max(r2["E_new"], r2["E_old"])
    passes = best_C >= best_E + margin
    detail = " ".join(f"R2({k})={v:.3f}" for k, v in r2.items())
    detail += f"  |  path-endpoint={best_C - best_E:+.3f}  n={len(runs)}  S<0 in {np.mean(np.asarray(q['S_old']) < 0):.0%} of runs (old probe)"
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


GATES = {"L5": gate_L5, "CUT": gate_CUT, "T1": gate_T1, "EQ": gate_EQ}
LEARNER_GATES = {"T1"}
REPLAY_GATES = {"EQ"}


def main(hyp: str):
    g = GATES[hyp]
    print(f"gate for {hyp}\n  must FAIL on {sorted(MUST_FAIL[hyp])}\n  must PASS on {sorted(MUST_PASS[hyp])}\n")
    bad = 0
    battery = LEARNER_BATTERY if hyp in LEARNER_GATES else REPLAY_BATTERY if hyp in REPLAY_GATES else BATTERY
    for gen in battery:
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
        flag = "" if ok else f"   <-- VIOLATION: {why}"
        bad += (not ok)
        print(f"  {name:55s} {'PASS' if passes else 'FAIL':4s}  {detail}{flag}")
    if hyp in LEARNER_GATES:
        print("\n  (EQ is not gated yet: gate_EQ needs a replay learner and the ER-sum control; see SCOPE.md §6)")
    print()
    print("GATE OPEN" if bad == 0 else f"GATE CLOSED ({bad} violation(s)): restate the hypothesis or add a control")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
