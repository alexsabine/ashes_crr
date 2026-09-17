"""CRR at zero: a boundary battery on emptiness (owner request 2026-09-18, prompt-log entry 54).

"Emptiness / 0" enters CRR in two ways. (i) The theory's own statements of no content: the cut "has no
duration and no content" (A3), "the future has no content" (A8). (ii) The value zero in every quantity
the theory defines: an occasion with no travel (C = 0), zero surplus (S = 0, the geodesic case of P1),
a closed loop (C* = 0), an empty carrier (a flat channel, a count series of zeros), the boundary of a
Fisher-native carrier (p = 0, lambda = 0, a simplex vertex), a zero gradient in the equanimity rule, zero
Fisher speed in the Kalman identity, zero surplus or zero age in the MaxEnt weights, a resolution below
one step (rho < 1), fewer events than the instrument needs, and the quantum vacuum under displacement.

Each row computes what the definitions and the repository's own instrument do at that zero, and grades
the statement under the issue-#21 rules (SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN). Every number
is printed by this script; exceptions raised by the instrument are caught and printed as the result.
No dataset opened (R2). Deterministic. Run:
uv run python theory/retrodictions/emptiness.py
"""
import math
import sys

import numpy as np
import sympy as sp

from crr.instrument.core import (antipodal_cuts, arc_length, chord, intrinsic_phase, occasions, poisson_transform, regularity,
                                 rho, sign_test_units, surplus, unit_sigma)

ROWS = []


def row(cls, system, clause, borrowed, derivation, known, verdict, grade, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, derivation=derivation, known=known,
                     verdict=verdict, grade=grade, weakness=weakness))


def raised(fn, *a, **k):
    try:
        v = fn(*a, **k); return f"returned {v!r}"[:80]
    except Exception as e:
        return f"raised {type(e).__name__}: {e}"


# ---------------------------------------------------------------- 1 the empty occasion
def empty_occasion():
    x = np.zeros(100); C, Cs, S = surplus(x, sigma=1.0)
    u = raised(unit_sigma, np.zeros(40))
    row("def", "The empty occasion: a carrier that does not move", "D2-D4 (C, C*, S at zero), P1 (equality), A1'/D1 (the unit)",
        "arc length of a constant path",
        f"C = {C:.1f}, C* = {Cs:.1f}, S = {S:.1f} (P1 holds with equality); the unit on a constant statistic: unit_sigma {u}",
        "a path of zero length has zero length",
        "the quantities are all zero by definition and the unit does not exist: the framework cannot count on a carrier that does not change, which is what A1' says (the unit is a resolvable step of the system's own change)",
        "DESCR", "the instrument rejects the record rather than reporting zero occasions: an empty carrier has no unit, not a unit of zero")


# ---------------------------------------------------------------- 2 the cut has no content
def cut_no_content():
    x = sp.symbols("x", real=True)
    integral = sp.integrate(sp.DiracDelta(x), (x, -1, 1)); support = sp.integrate(sp.Heaviside(x) - sp.Heaviside(x - 0), (x, -1, 1))
    deriv = sp.diff(sp.Heaviside(x), x)
    row("def", "The cut as a Dirac delta in phase: unit count, zero measure", "A3 ('the cut has no duration and no content'), D5",
        "distributions: delta and Heaviside",
        f"integral of delta over a half-turn = {integral} (the cut counts once); measure of its support = {support}; d/dx Heaviside = {deriv} (Now is the derivative of the settlement function)",
        "a delta has unit integral and zero support",
        "A3's 'no content' is the zero-measure support of a delta and 'partitions the history' is the Heaviside it differentiates; both are definitions, and they hold exactly",
        "DESCR", "the theory's first statement about emptiness is a definition that cannot fail")


# ---------------------------------------------------------------- 3 the closed loop: endpoint empty, path full
def closed_loop():
    t = np.linspace(0, 2 * math.pi, 4001); path = np.c_[np.cos(t), np.sin(t)]
    C, Cs, S = surplus(path, sigma=1.0)
    row("def", "A closed loop: the endpoint says nothing changed, the arc says everything did", "D3 (C* = 0 on a closed loop), D4 (S = C), D6/H-T1 (path vs endpoint)",
        "arc length of the unit circle",
        f"unit circle traversed once: C = {C:.4f} (2 pi = {2 * math.pi:.4f}), C* = {Cs:.2e}, S = {S:.4f}: all of the arc is surplus",
        "a loop has zero displacement and positive length",
        "the one place where CRR's reading and an endpoint reading differ maximally is the loop: an empty endpoint displacement with a full arc; this is the content of D4 and the design of the 'loop' schedules in T1x, and it is a definition until a system's forgetting is shown to track it (the ledger's T1 rows say the old-probe endpoint won)",
        "DESCR", "true by definition; whether any system cares about S when C* = 0 is exactly what H-T1 and the Preisach/reservoir rows tested, and they said no")


# ---------------------------------------------------------------- 4 the future has no content
def empty_future():
    t = np.linspace(0, 10, 1001); x = np.sin(2 * math.pi * t); ph = intrinsic_phase(x); cuts = antipodal_cuts(ph)
    n_settled = np.searchsorted(cuts, np.arange(len(t)), side="right")                      # number of cuts up to each sample
    ahead = [len(cuts) - n for n in n_settled]
    row("def", "The future has no content: the settled sum has no terms ahead of Now", "A8 ('the future has no content'), A7 (nothing is fed by a future), D5",
        "counting cuts",
        f"{len(cuts)} cuts on 10 cycles; at the midpoint the settled count is {n_settled[500]} and the terms the settled sum can contain from ahead of Now: 0 by construction (the terms 'ahead', {ahead[500]}, exist only once the run is over)",
        "one cannot sum what has not happened",
        "A8 is the statement that the sum over settled occasions has an upper limit n(t), a step function; the framework then permits a comparative forecast (A8 v3.1) but never a content: a definition of tense, not a claim about the world",
        "DESCR", "the theory's second statement about emptiness is also a definition; it becomes testable only as the comparative forecasts it licenses (F1, gated but not built)")


# ---------------------------------------------------------------- 5 the boundary of a Fisher-native carrier
def fisher_boundary():
    lam = 1.0; d_pois = float(abs(poisson_transform(np.array([lam]))[0] - poisson_transform(np.array([0.0]))[0]))
    p = sp.symbols("p", positive=True); g_bern = 1 / (p * (1 - p)); d_bern = float(2 * sp.asin(sp.sqrt(sp.Rational(1, 2))) - 2 * sp.asin(0)); d_full = float(2 * sp.asin(1))
    vertex = 2 * math.acos(0.0)                                                              # simplex vertex to vertex on the radius-2 sphere
    row("carrier", "The boundary of a Fisher-native carrier: empty rate, empty category, empty probability", "A1 (Fisher-Rao carrier), P6/P7 (SCOPE.md), D1",
        "Fisher-Rao distances of the Poisson, Bernoulli and categorical families (Cencov)",
        f"Poisson: distance from lambda = 0 to lambda = 1 is 2 sqrt(lambda) = {d_pois:.4f} while the metric 1/lambda diverges at 0; Bernoulli: metric {g_bern} diverges at p = 0, distance from p = 0 to 1/2 is {d_bern:.4f} and to p = 1 is {d_full:.4f} (= pi); categorical: an empty category is a simplex vertex at distance {vertex:.4f} (= pi) from any other vertex",
        "the Fisher metric of an exponential family is singular at the boundary but the boundary is at finite distance",
        "emptiness on a Fisher carrier is infinitely curved and finitely far: a carrier fact the geometry supplies, on which the framework's unit and cut are then defined; nothing about zero is derived",
        "DESCR", "inherited (Cencov); the spec's removal of the Bernoulli 'p = 1/2 antipode' is the same fact read from the other end")


# ---------------------------------------------------------------- 6 the empty count carrier
def empty_count_carrier():
    rng = np.random.default_rng(1); counts = np.zeros(200); counts[rng.choice(200, 8, replace=False)] = rng.integers(1, 4, 8)
    y = poisson_transform(counts); arc = arc_length(y); ev = np.where(counts > 0)[0]
    isolated = bool(np.all(np.diff(ev) > 1)); expected = float(np.sum(4 * np.sqrt(counts[ev])))
    u = raised(unit_sigma, counts[:60])
    row("carrier", "A count carrier that is mostly zero (a sparse spike train or case series)", "A1' (unit from residuals), P6 (arc = total variation of 2 sqrt lambda), R11 (flat-channel gate)",
        "the Poisson transform; total variation",
        f"200 bins, {len(ev)} non-zero (all isolated: {isolated}): Fisher arc of the whole series = {arc:.3f}; sum over events of 4 sqrt(k) = {expected:.3f} (equal iff the events are isolated); the unit from a training window of zeros: unit_sigma {u}",
        "a sparse count series has a residual scale of zero almost everywhere",
        "on a mostly-empty carrier the arc is a sum of event-sized jumps and the unit does not exist: the framework's own quality gate (R11) rejects the record, so emptiness is not a state the framework describes but one it excludes",
        "DESCR", "the measles carrier avoided this because its counts were never zero; a spike-train carrier would hit it, and the prereg would have to name a rate-smoothing window (which the diffusion-carrier row also demands)")


# ---------------------------------------------------------------- 7 the equanimity rule at zero gradient
def equanimity_at_zero():
    gp, gq, Om = sp.symbols("g_p g_q Omega", positive=True); w = Om * gp / gq
    lim_past0 = sp.limit(w, gq, 0); lim_present0 = sp.limit(w, gp, 0)
    row("rule", "The normalised step (v3.1 H-EQ) when the past or the present gradient is zero", "H-EQ (w = Omega ||g_present|| / ||g_past||), the EQ2 cap; A9 of the issue text",
        "limits of a ratio",
        f"w as ||g_past|| -> 0: {lim_past0} (an empty past is weighted infinitely: the cap the EQ2 prereg had to add); w as ||g_present|| -> 0: {lim_present0} (an empty present silences the past entirely)",
        "a ratio has opposite limits at the two zeros",
        "the rule's two zero limits are opposite in kind: nothing left to remember is weighted without bound, nothing left to learn drops the past to zero; the second is a behaviour (a converged learner stops protecting old tasks) that no ledger row has tested and the EQ2 report did not name",
        "TENSION", "internal: the two emptinesses of the rule are not symmetric, and one of them (empty present) is the ordinary end state of every training run")


# ---------------------------------------------------------------- 8 the Kalman identity at zero speed
def kalman_at_zero():
    v = sp.symbols("v", nonnegative=True); K = (v / 2) * (sp.sqrt(v ** 2 + 4) - v)
    K0 = sp.limit(K, v, 0); Kinf = sp.limit(K, v, sp.oo); K1 = sp.nsimplify(K.subs(v, 1))
    row("rule", "The Kalman identity (P4) at zero Fisher speed and at infinite speed", "P4 (K(v)), O1",
        "steady-state Riccati equation",
        f"K(0) = {K0}: with nothing happening the present is ignored and the past kept whole; K(oo) = {Kinf}: with an empty (uninformative) past the present is taken whole; K(1) = {K1}",
        "the Kalman gain runs from 0 to 1 with the process-to-observation noise ratio",
        "the two emptinesses are the two ends of the gain, and the golden-ratio value sits at v = 1 between them; P4 says of itself that the formula is not CRR's",
        "DESCR", "standard; a control for the H-EQ row: here the two limits are the expected ones")


# ---------------------------------------------------------------- 9 MaxEnt weights at zero
def maxent_at_zero():
    S = np.array([0.0, 0.0, 0.0, 0.0]); beta = 1.0; w_S = np.exp(beta * S) / np.exp(beta * S).sum()
    k = np.arange(4); w_q0 = np.array([1.0, 0.0, 0.0, 0.0]); q = 0.999; w_q1 = q ** k / (q ** k).sum()
    row("rule", "The MaxEnt occasion weights at zero surplus, zero temperature and zero age", "P2 (pi proportional to e^{beta S}), P3 (pi proportional to q^k), O2",
        "Gibbs and geometric distributions",
        f"all surpluses zero: weights {w_S} (uniform: emptiness of surplus is indifference); beta = 0 gives the same; q -> 0: {w_q0} (only Now); q -> 1: {np.round(w_q1, 3)} (all ages equal, mean age unbounded)",
        "a Gibbs distribution with equal energies is uniform; a geometric distribution degenerates at its endpoints",
        "with nothing to distinguish occasions the framework weights them equally, and with q at its ends it keeps only the present or everything: definitions of the two constraint families, and CRR fixes neither beta nor q",
        "DESCR", "O2 says the choice between the families is untested; the batteries have since found five kernels, one of them in these families")


# ---------------------------------------------------------------- 10 below one resolvable step: the instrument cuts on nothing
def below_one_step():
    rng = np.random.default_rng(2); t = np.linspace(0, 20, 4001); true_cycles = 20
    out = []
    for amp in (1.0, 0.1, 0.0):
        x = amp * np.sin(2 * math.pi * t) + 1.0 * rng.standard_normal(len(t)); cuts = antipodal_cuts(intrinsic_phase(x))
        out.append((amp, len(cuts), rho(2 * amp, 1.0)))
    row("inst", "Signal below one resolvable step: does the antipodal cut fire on emptiness?", "A3 (the cut is a phase criterion, scale-free), D1 (rho reported), R5/R11 (rho floor as a quality gate)",
        "analytic-signal phase of noise",
        "; ".join(f"amplitude {a:g} sigma (rho = {r:g}): {n} cuts on {true_cycles} true cycles" for a, n, r in out),
        "the analytic-signal phase of pure noise still advances, so a phase criterion fires on nothing",
        "the cut is scale-free and fires on an empty signal at the noise's own rate: emptiness produces occasions unless the quality gate removes the record; that is why rho is reported and a floor is pre-registered, and it is an instrument property, not a claim",
        "DESCR", "the gate (S-D rows) handles this; a prereg that forgets the rho floor would count occasions in noise")


# ---------------------------------------------------------------- 11 fewer events than the instrument needs
def too_few_events():
    x = np.sin(np.linspace(0, 4 * math.pi, 400))
    r2 = raised(regularity, x, np.array([0, 199]), sigma=1.0); r3d = regularity(x, np.array([0, 100, 199]), sigma=1.0); r3 = f"returned n = {r3d['n']} occasions, cv_arc {r3d['cv_arc']:.3f}, cv_clock {r3d['cv_clock']:.3f}"
    s0 = raised(sign_test_units, []); s1 = sign_test_units([dict(cv_arc=0.1, cv_clock=0.2)])
    row("inst", "Zero, one, two and three events: what the regularity statistic can say", "H-L5 (CV across occasions), R6 (per-unit scoring), O3 (natural time needs events)",
        "the definition of a coefficient of variation",
        f"two events (one occasion): regularity {r2}; three events (two occasions): {r3}; zero units: sign_test_units {s0}; one unit: win fraction {s1[0]:.1f}, exact binomial p = {s1[1]:.2f}",
        "a variance needs two samples and a sign test needs many",
        "with fewer than two occasions there is no regularity to compare, and with one unit the sign test cannot reject anything (p = 1): emptiness of events is silence, enforced by the instrument rather than stated by the theory",
        "DESCR", "the minimum counts belong in every prereg's exclusion rules (R6)")


# ---------------------------------------------------------------- 12 the vacuum and its antipode
def vacuum_antipode():
    alphas = (0.5, 1.0, 2.0, 3.0); d = [(a, 2 * math.acos(math.exp(-a * a / 2))) for a in alphas]     # Fubini-Study on the radius-2 convention used in the main battery
    row("quantum", "The quantum vacuum displaced to a coherent state: how far is emptiness from its antipode?", "A3 (cut at the antipode), A1 (Fubini-Study carrier), the main battery's qubit rows",
        "Fubini-Study distance; overlap of coherent states |<0|alpha>|^2 = exp(-|alpha|^2)",
        "; ".join(f"|alpha| = {a:g}: distance {dd:.3f}" for a, dd in d) + f" (antipode at pi = {math.pi:.3f}, reached only as |alpha| -> infinity)",
        "a coherent state is never orthogonal to the vacuum",
        "the empty mode has an antipode that displacement never reaches, so A3 never fires on this path: the framework says OPEN by its own rule (no canonical cut), and the vacuum is a carrier point like any other",
        "OPEN", "a control: emptiness in the quantum sense is not special to the framework; only orthogonality is, and displacement never produces it")


# ---------------------------------------------------------------- 13 zero surplus: the geodesic case
def zero_surplus_geodesic():
    x = np.linspace(0, 3, 301); C, Cs, S = surplus(x, sigma=1.0)
    y = np.r_[np.linspace(0, 2, 201), np.linspace(2, 1, 101)]; C2, Cs2, S2 = surplus(y, sigma=1.0)
    row("def", "Zero surplus: the monotone path (P1's equality case) against one with a single reversal", "P1 (S >= 0, equality iff geodesic), D4",
        "the triangle inequality",
        f"monotone ramp: C = {C:.3f}, C* = {Cs:.3f}, S = {S:.1e}; ramp with one reversal: C = {C2:.3f}, C* = {Cs2:.3f}, S = {S2:.3f} (twice the backtrack)",
        "a path has zero surplus iff it never backtracks (in one dimension)",
        "emptiness of surplus is the absence of backtracking: a definition (P1 says of itself that it is the triangle inequality), and the quantity every 'wear' row (Paris law, annealing) was shown to be the wrong functional for",
        "DESCR", "the surplus is well defined at zero; whether anything reads it is the T5 question, which failed twice")


BATTERY = [empty_occasion, cut_no_content, closed_loop, empty_future, fisher_boundary, empty_count_carrier, equanimity_at_zero, kalman_at_zero,
           maxent_at_zero, below_one_step, too_few_events, vacuum_antipode, zero_surplus_geodesic]

CLASSES = {"def": "the theory's definitions at zero", "carrier": "empty carriers", "rule": "rules at zero", "inst": "the instrument at zero", "quantum": "the vacuum"}


def main():
    for f in BATTERY: f()
    print(f"CRR at zero — {len(ROWS)} boundary checks in {len(CLASSES)} groups. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'group':36s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rs = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:28s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':36s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print("\nWhat the framework says about emptiness: two definitions (the cut has no content; the future has no content), both exact;"
          " at every other zero the definitions behave as their mathematics dictates, the instrument refuses to count (no unit, too few events),"
          f" and one rule (the normalised step) has opposite limits at its two zeros. Rows where a clause reaches a result the domain did not have: {sum(r['grade'] == 'SHARP' for r in ROWS)} of {len(ROWS)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
