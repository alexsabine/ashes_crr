"""Synthesis batch 05: rows 21-25 of QUEUE.md (prompt-log entry 61). All five from Daniel's battery
runs/phaseA/crr_retrodictions.txt (script crr_retrodictions.py at the repository root):
[a3] Boltzmann two-level populations vs temperature (DESCR); [a4] chemical relaxation A<=>B, surplus on a monotone
occasion (DESCR); [b1] pure qubit on the Bloch sphere, Fisher half-turn = orthogonal state (CONSIST); [c1] ideal-gas
isotherm, D2 arc = thermodynamic length (CONSIST); [c2] Schottky anomaly vs the Fisher peak (CONSIST).
Models re-implemented from the source functions (_a3_two_level, _a4_relaxation_surplus, _b1_bures_antipode,
_c1_ideal_gas, _c2_schottky); nothing imported from theory/retrodictions. Deterministic, no data (R2).
Run:  uv run python theory/retrodictions/synthesis_batches/batch_05.py
"""
import math
import sys

import numpy as np
from scipy import optimize

from crr.instrument.core import antipodal_cuts, arc_length, intrinsic_phase, surplus
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _p_excited(x):
    """Two-level canonical excited fraction, x = Delta/(k T) = beta Delta."""
    return 1.0 / (1.0 + np.exp(x))


def _schottky_x():
    """x = beta Delta at the heat-capacity maximum: dC/dx = 0 <=> (2 + x)(1 + e^x) - 2 x e^x = 0 (source row c2)."""
    return float(optimize.brentq(lambda x: (2.0 + x) * (1.0 + math.exp(x)) - 2.0 * x * math.exp(x), 1.0, 4.0, xtol=1e-14))


def _word(cond, yes, no):
    return yes if cond else no


# ---------------------------------------------------------------- 21 [a3] the two-level cut is the beta = 0 boundary
def r1():
    p_cut = float(_p_excited(0.0))                                   # A3 antipode of the pole p = 0 on the Bernoulli family
    arc_pos = 2.0 * math.asin(math.sqrt(p_cut))                      # D2 arc T = 0 -> beta = 0 (pole to cut)
    arc_neg = 2.0 * math.asin(math.sqrt(1.0)) - arc_pos              # D2 arc beta = 0 -> T = 0- (cut to the inverted pole)
    x_sch = _schottky_x(); p_sch = float(_p_excited(x_sch)); arc_sch = 2.0 * math.asin(math.sqrt(p_sch))
    g = 4.0
    x_g = float(optimize.brentq(lambda x: g * math.exp(-x) / (1.0 + g * math.exp(-x)) - 0.5, 0.1, 5.0, xtol=1e-14))
    p_ramsey = float(_p_excited(0.0))                                # the domain: populations equal at beta = 0 (Ramsey)
    check = rel(arc_pos, arc_neg) <= 1e-9 and rel(arc_pos, math.pi / 2.0) <= 1e-9
    out = outcome(crr=p_cut, null=p_sch, domain=p_ramsey, check=check)
    return make_row("thermo", "Canonical two-level system: Bernoulli family in the excited fraction p(x) = 1/(1 + e^x), x = Delta/(k T), pole-start occasion from T = 0 (Daniel's battery row a3 re-read)",
                    source="runs/phaseA/crr_retrodictions.txt [a3] (DESCR)",
                    Q="the occasion begun at T = 0 closes at the infinite-temperature state beta = 0 (p = 1/2), and the successor occasion is the negative-temperature branch beta < 0, of the same arc: the population-inversion boundary is the antipode of the ground state",
                    ingredient="A3 (pole-start antipodal cut on the Bernoulli family), D5 (the inverted branch as the next occasion), D2 (arc 2 asin sqrt p)",
                    null="the domain's own landmark for 'where the system changes most', the Schottky heat-capacity peak (an extremum cut on the same axis)",
                    domain="Ramsey's negative temperatures: beta = 0 is the boundary between the positive- and negative-temperature branches, the populations are equal there, and the branch beyond it is the inverted one",
                    numbers=f"cut at x = 0 (T = infinity): p = {p_cut:.4f}; arc T = 0 -> cut = {arc_pos:.4f}, arc cut -> T = 0- (p = 1/2 -> 1) = {arc_neg:.4f}, pi/2 = {math.pi / 2:.4f}; Schottky peak at x = {x_sch:.4f}: p = {p_sch:.4f}, arc from the pole {arc_sch:.4f}; degeneracy probe g = {g:g}: p = 1/2 at x = {x_g:.4f} = ln g = {math.log(g):.4f} (the antipode is still p = 1/2, at finite T)",
                    tg=f"p at the A3 cut {p_cut:.4f} vs null p at the Schottky peak {p_sch:.4f}: {_word(rel(p_cut, p_sch) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the domain's boundary (populations equal at beta = 0) gives p = {p_ramsey:.4f}: {_word(rel(p_cut, p_ramsey) <= TOL_N, 'the domain has Q', 'the domain does not give Q')}",
                    tc=f"the two half-turns are equal and each is pi/2: {_word(check, 'holds', 'fails')} (computed; not the deciding test, the label stops at T-N)",
                    out=out,
                    reading=f"the cut reading of the canonical family restates the beta = 0 boundary that negative-temperature thermodynamics already draws, and the equal arcs on either side of it are the Bernoulli family's symmetry p <-> 1 - p; CRR supplies the word 'antipode' and fixes no temperature scale (the source row's own weakness stands); the label is {out}",
                    weakness="one carrier (the Bernoulli family in p); the extremum null is the heat-capacity peak because p(x) itself is monotone and has no extremum; the degeneracy probe moves the cut to finite T without changing p = 1/2, which is the family's geometry, not the domain's thermodynamics",
                    elegance="The antipode of the frozen system is the fair coin: equal populations at infinite temperature, and the same half-turn again reaches the fully inverted state. One arc of length pi cut at its middle, with no knobs, and the picture carries negative temperature without a formula.",
                    child="Imagine a box of tiny switches that are all off when it is freezing cold. Heat the box and more switches flip on, but even at the hottest it can ever get, exactly half are on, like a fair coin. Getting more than half on is what physicists call 'hotter than infinitely hot', and the fair-coin point, halfway along, is the natural place to draw the line between the two.")


# ---------------------------------------------------------------- 22 [a4] the surplus of a monotone relaxation (P1's equality case)
def r2():
    xe, lam, x0, T_end = 0.8, 1.0, 0.05, 6.0
    ts = np.linspace(0.0, T_end, 400001)
    xs = xe + (x0 - xe) * np.exp(-lam * ts)
    y = 2.0 * np.arcsin(np.sqrt(xs))                                  # Bhattacharyya angle: the Bernoulli Fisher metric is the identity in y
    C, Cs, S = surplus(y)
    a, w, x0p = 0.15, 6.0, 0.3                                        # the source row's synthetic non-monotone probe
    xp = xe + (x0p - xe) * np.exp(-ts) + a * np.exp(-ts) * np.sin(w * ts)
    Cp, Csp, Sp = surplus(2.0 * np.arcsin(np.sqrt(xp)))
    C_quad = float(np.trapezoid(np.abs(np.gradient(xs, ts)) / np.sqrt(xs * (1.0 - xs)), ts))   # the source row's estimator
    monotone = bool(np.all(np.diff(xs) > 0)); nonmono = bool(np.any(np.diff(xp) < 0))
    # proper ingredients tried
    ph = intrinsic_phase(xs); span = float(ph[-1] - ph[0]); cuts = antipodal_cuts(ph)
    t_fake = float(ts[cuts[1]]) if len(cuts) > 1 else None
    N = 100
    steps = {xx: (1.0 / N) / math.sqrt(xx * (1.0 - xx)) for xx in (x0, 0.5, xe)}
    check = abs(S) < 1e-7 and Sp > 1e-3 and monotone and nonmono
    out = outcome(crr=Sp, null=Sp, domain=None, check=check)
    tried = (f"A3: the path is monotone, so there is no rotor (O3) and no cut is defined; run blind, the analytic-signal phase spans {span:.4f} rad on it and antipodal_cuts fires at t = {t_fake:.4f} on a trace with no cycle (an artefact of the Hilbert transform, not an occasion); "
             f"A6: a single occasion has no settled past to regenerate from; "
             f"A1': one conversion event among N = {N} molecules is {steps[x0]:.4f}, {steps[0.5]:.4f}, {steps[xe]:.4f} Fisher units at x = {x0:g}, 0.5, {xe:g}: the event unit is not one number along the path (the source battery's row a5)")
    return make_row("chem", "Reversible first-order relaxation A <=> B, x(t) = x_eq + (x0 - x_eq) e^(-lambda t) on the Bernoulli family in the mole fraction x, one occasion x0 = 0.05 -> x_eq = 0.8 (Daniel's battery row a4 re-read)",
                    source="runs/phaseA/crr_retrodictions.txt [a4] (DESCR)",
                    Q="the surplus of the monotone relaxation is zero and that of a non-monotone trace is positive: S measures the backtracking of the mole fraction",
                    ingredient="D4 (surplus C - C*) on the Bhattacharyya-angle coordinate y = 2 asin sqrt x, with D2, D3 and P1 - NOT CRR-proper: every symbol is information geometry's",
                    null="the same S computed by information geometry alone (identical by construction)",
                    domain=None,
                    numbers=f"monotone occasion: C = {C:.8f}, C* = {Cs:.8f}, S = {S:.2e} (monotone: {monotone}); the source row's quadrature estimator gives C = {C_quad:.8f}; non-monotone probe (x0 = {x0p:g}, amplitude {a:g}, frequency {w:g}): C = {Cp:.4f}, C* = {Csp:.4f}, S = {Sp:.4f} (non-monotone: {nonmono}); proper ingredients tried - {tried}",
                    tg=f"S {Sp:.4f} vs null S {Sp:.4f}: {_word(rel(Sp, Sp) <= TOL_G, 'agree', 'differ')} (no CRR-proper ingredient in Q)",
                    tn="none cited: chemical kinetics has no surplus; its own theorem (reversible first-order A <=> B relaxes monotonically as a single exponential) is what makes S vanish",
                    tc=f"|S| < 1e-7 on the monotone occasion and S > 1e-3 on the probe: {_word(check, 'holds', 'fails')} (true, and it is P1's equality case)",
                    out=out,
                    reading=f"the source row's content is exactly P1's equality case, a true and checkable statement that CRR did not add; each CRR-proper ingredient was tried and none forms a Q on this carrier (no rotor to cut, one occasion to regenerate from, an event unit that varies along the path), so the label is {out}",
                    weakness="the probe trace is the source row's synthetic one; the blind-phase artefact is recorded as a caution for any prereg that runs antipodal_cuts on a monotone carrier, not as a finding",
                    elegance="'If you never turn back, the road you walked is exactly how far you got.' P1's equality case is a rule with no knobs; it is geometry's, not CRR's, and it says in one sentence what the surplus measures.",
                    child="Think of walking to a friend's house. If you walk straight there, the distance you walked equals how far away the house is. If you wander back and forth on the way, you walked more than that, and the extra is the surplus. A chemical reaction that settles smoothly walks straight, so its surplus is zero.")


# ---------------------------------------------------------------- 23 [b1] three readings of A3 on the two-level carrier
def _qubit_readings(theta, omega=1.0, n=200001, t_max=4.0 * math.pi):
    """Pure state cos(theta/2)|0> + sin(theta/2)|1> under H = diag(0, omega): precession on the Bloch circle of latitude theta.
    Returns dE, the arc reading t_arc (Fisher arc 2 dE t = pi), the orthogonality time t_perp (None if unreached), the
    minimum overlap, the rotor reading t_rot (antipodal_cuts on the Bloch x-component), the overlap at t_arc and the
    chord (Fubini-Study, orthogonal = pi) at the rotor cut."""
    t = np.linspace(0.0, t_max, n)
    dE = 0.5 * math.sin(theta)
    t_arc = math.pi / (2.0 * dE)
    c2, s2 = math.cos(theta / 2.0) ** 2, math.sin(theta / 2.0) ** 2
    ov = np.abs(c2 + s2 * np.exp(-1j * omega * t))
    i = int(np.argmin(ov[1:]) + 1)
    r = optimize.minimize_scalar(lambda tt: abs(c2 + s2 * np.exp(-1j * omega * tt)), bounds=(t[i - 1], t[i + 1]), method="bounded", options=dict(xatol=1e-12))
    ov_min = float(r.fun); t_far = float(r.x); t_perp = t_far if ov_min < 1e-6 else None
    cuts = antipodal_cuts(intrinsic_phase(math.sin(theta) * np.cos(omega * t)))
    t_rot = float(t[cuts[1]])
    ov_at_arc = float(abs(c2 + s2 * np.exp(-1j * omega * t_arc)))
    chord_rot = 2.0 * math.acos(min(1.0, float(abs(c2 + s2 * np.exp(-1j * omega * t_rot)))))
    return dict(theta=theta, dE=dE, t_arc=t_arc, t_perp=t_perp, ov_min=ov_min, t_rot=t_rot, t_far=t_far, ov_at_arc=ov_at_arc, chord_rot=chord_rot)


def r3():
    omega = 1.0
    res = [_qubit_readings(th, omega) for th in (math.pi / 2.0, math.pi / 3.0, math.pi / 6.0)]
    names = {res[0]["theta"]: "pi/2", res[1]["theta"]: "pi/3", res[2]["theta"]: "pi/6"}
    agree = {q["theta"]: (q["t_perp"] is not None and rel(q["t_arc"], q["t_perp"]) <= TOL_G and rel(q["t_rot"], q["t_arc"]) <= TOL_G) for q in res}
    internal = not all(agree.values())
    out = outcome(internal=internal)
    eq = res[0]; t_mt = math.pi / (2.0 * eq["dE"]); dt = 4.0 * math.pi / 200000
    mt_word = _word(rel(t_mt, eq["t_arc"]) <= TOL_N and rel(t_mt, eq["t_rot"]) <= TOL_N, "is", "is not")
    sub = outcome(crr=eq["t_arc"], null=eq["t_perp"], domain=t_mt, check=True) if eq["t_perp"] is not None else "UNSTATED"
    n_agree = sum(agree.values())
    numbers = "; ".join(
        f"theta = {names[q['theta']]}: dE = {q['dE']:.4f}, rotor reading t = {q['t_rot']:.4f} (far point of the orbit, chord {q['chord_rot']:.4f}, at t = {q['t_far']:.4f}), arc reading t = {q['t_arc']:.4f} (overlap there {q['ov_at_arc']:.4f}), "
        + (f"orthogonal state at t = {q['t_perp']:.4f}" if q["t_perp"] is not None else f"no orthogonal state (minimum overlap {q['ov_min']:.4f} = cos theta)")
        for q in res) + f"; omega = {omega:g}, pi = {math.pi:.4f}, Mandelstam-Tamm time on the equator = {t_mt:.4f}"
    tg = "; ".join(f"theta = {names[q['theta']]}: rotor {q['t_rot']:.4f} / arc {q['t_arc']:.4f} / antipode " + (f"{q['t_perp']:.4f}" if q["t_perp"] is not None else "none") + f": {_word(agree[q['theta']], 'agree', 'differ')}" for q in res) + f"; readings agree at {n_agree} of {len(res)} states"
    return make_row("qm", "Pure qubit cos(theta/2)|0> + sin(theta/2)|1> precessing under H = diag(0, omega), Fubini-Study metric (orthogonal = pi), the source row's carrier CP^1 (Daniel's battery row b1 re-read; synthesis.py row 4 found A3 INTERNAL on three levels)",
                    source="runs/phaseA/crr_retrodictions.txt [b1] (CONSIST)",
                    Q="for every pure qubit state the A3 cut of the precession is the orthogonal state (the source row's stipulation 'Fisher half-turn = orthogonal state')",
                    ingredient="A3 in its three readings on this carrier: (i) the rotor reading, the axiom's text - the intrinsic phase (Bloch azimuth) advances half a turn, antipodal_cuts on the Bloch x-component; (ii) the arc reading - the Fisher arc 2 dE t reaches pi, half the closed geodesic; (iii) the antipode reading - the first orthogonal state",
                    null="the domain's own events: the Mandelstam-Tamm time pi/(2 dE) and the orthogonality time",
                    domain="Mandelstam-Tamm bound t_perp >= pi/(2 dE), attained iff the evolution is a Fubini-Study geodesic (Anandan-Aharonov), i.e. iff the state is an equal-weight superposition of the two eigenstates (theta = pi/2)",
                    numbers=numbers, tg=tg,
                    tn=f"on the equator the domain's Mandelstam-Tamm time {t_mt:.4f} {mt_word} the cut time (within {TOL_N:g}): the sub-case label from outcome(arc reading, orthogonality time, MT time) is {sub}; off the equator the domain has both times and the statement that they differ",
                    tc="not reached: the readings must agree before Q can be checked, and they agree only on the geodesic set",
                    out=out,
                    reading=f"the two-level carrier does not escape row 4's INTERNAL, it sharpens it: the three readings of A3 coincide at {n_agree} of {len(res)} states (the equal-weight superposition) and there the cut is the domain's Mandelstam-Tamm event ({sub}); elsewhere the rotor reading fires at t = pi/omega for every theta at the far point of the orbit, whose chord 2 theta is not pi, the arc reading fires later, at pi/(omega sin theta), and at theta = pi/6 it fires when the state has returned to itself (overlap {res[2]['ov_at_arc']:.4f}); the set on which A3 is one rule is the geodesic set, which the domain already names (Anandan-Aharonov)",
                    weakness=f"omega = 1 and three values of theta; the rotor reading takes the Bloch x-component as the trace (one choice of intrinsic phase, R5) and antipodal_cuts returns the sample nearest the interpolated crossing (grid step {dt:.2e}); which reading is A3 on a projective carrier is a theory decision (v3.2), not this row's",
                    elegance="A state reaches its opposite only when it runs the equator; on any other latitude it circles back without ever being opposite. 'Halfway round' and 'as far as you can get' are the same thing only on a great circle, and the picture needs no formula.",
                    child="Picture an ant walking round a globe. If it walks along the equator, halfway round it stands exactly on the opposite side of the world. If it walks round a small circle near the North Pole, halfway round it is as far from home as that path allows, but nowhere near the opposite side. A quantum bit is like the ant: only the equator path ever reaches the exactly-opposite state.")


# ---------------------------------------------------------------- 24 [c1] the isotherm's thermodynamic length
def r4():
    NkB = 1.0
    V = np.linspace(1.0, 2.0, 100001)
    L_quad = float(np.trapezoid(np.sqrt(NkB / V ** 2), V))                  # D2 with the Ruppeiner metric g_VV = -d2S/dV2 = N k_B / V^2
    L_inst = arc_length(math.sqrt(NkB) * np.log(V))                           # the same arc in the flat coordinate phi = sqrt(N k_B) ln V
    L_closed = math.sqrt(NkB) * math.log(2.0)
    h = 1e-3; U0, V0 = 1.0, 1.0
    S_ = lambda U, Vv: NkB * (math.log(Vv) + 1.5 * math.log(U))
    g_UV = -(S_(U0 + h, V0 + h) - S_(U0 + h, V0 - h) - S_(U0 - h, V0 + h) + S_(U0 - h, V0 - h)) / (4.0 * h * h)
    N_big = 1.0e4; steps = math.sqrt(N_big) * math.log(2.0)
    L_start = [float(np.trapezoid(np.sqrt(NkB / Vv ** 2), Vv)) for Vv in (np.linspace(3.0, 6.0, 100001), np.linspace(10.0, 20.0, 100001))]
    check = rel(L_inst, L_closed) <= 1e-9
    out = outcome(crr=L_inst, null=L_quad, domain=L_closed, check=check)
    return make_row("thermo", "Ideal gas in the entropy representation S(U, V) = N k_B (ln V + 3/2 ln U), Ruppeiner metric, isotherm V -> 2V (Daniel's battery row c1 re-read)",
                    source="runs/phaseA/crr_retrodictions.txt [c1] (CONSIST)",
                    Q="the D2 arc of the isotherm V -> 2V is sqrt(N k_B) ln 2, the same from every starting volume",
                    ingredient="D2 (arc) with A1 (the Ruppeiner metric as the Fisher-Rao metric of the thermal family) - NOT CRR-proper: D2 itself says 'on a thermal family this is thermodynamic length'",
                    null="the same length by thermodynamic geometry alone (the quadrature of sqrt g_VV, identical by construction)",
                    domain="Ruppeiner's thermodynamic length on the ideal-gas isotherm, L = sqrt(N k_B) ln(V2/V1), on a flat metric",
                    numbers=f"N k_B = {NkB:g}: arc by the instrument on the flat coordinate = {L_inst:.10f}, by quadrature of sqrt g_VV = {L_quad:.10f}, closed form sqrt(N k_B) ln 2 = {L_closed:.10f} (relative difference {rel(L_inst, L_closed):.2e}); V -> 2V from V = 3: {L_start[0]:.6f}, from V = 10: {L_start[1]:.6f}; mixed component |g_UV| by central differences = {abs(g_UV):.2e} (the metric is diagonal and flat); proper ingredient tried - A1': in the metric's own unit (one fluctuation) the isotherm for N = {N_big:.0f} spans rho = sqrt(N) ln 2 = {steps:.2f} resolvable steps (D1: reported, never predicted), which is the distinguishability count thermodynamic geometry already reads off the same length; the Weinhold (energy-representation) length is this times sqrt T, a convention the axioms do not fix",
                    tg=f"arc {L_inst:.6f} vs null {L_quad:.6f}: {_word(rel(L_inst, L_quad) <= TOL_G, 'agree', 'differ')} (no CRR-proper ingredient in Q)",
                    tn=f"Ruppeiner's length gives {L_closed:.6f}: {_word(rel(L_inst, L_closed) <= TOL_N, 'the domain has Q', 'the domain does not give Q')}",
                    tc=f"arc equals sqrt(N k_B) ln 2 within 1e-9: {_word(check, 'holds', 'fails')} (true, and it is thermodynamic geometry's)",
                    out=out,
                    reading=f"the source row's content is exactly D2 read on a thermal family, which D2 names as thermodynamic length; the one proper ingredient with purchase (A1', the unit) returns the count of distinguishable states that the domain reads off the same length, so the label is {out}",
                    weakness="one isotherm on one flat family; N k_B = 1 fixes the scale by choice",
                    elegance="Doubling the volume is the same length wherever you start: the isotherm's length depends only on the ratio V2/V1. A rule with no knobs (it is the scale invariance of the logarithm), and it is the domain's.",
                    child="Blowing a balloon up from one cup of air to two cups is the same amount of change as blowing it from ten cups to twenty. This kind of length counts change by ratios, like the steps up a piano keyboard, not by cups.")


# ---------------------------------------------------------------- 25 [c2] which peak is the Fisher peak
def r5():
    xs = np.linspace(0.0, 12.0, 120001)
    p = _p_excited(xs); I_beta = p * (1.0 - p)                                # Fisher information of the family wrt beta (Delta = 1)
    I_lnT = xs ** 2 * I_beta                                                 # wrt ln beta (= wrt ln T): beta^2 Var(E) = C/k_B
    Ts = np.linspace(0.02, 20.0, 200001)
    I_T = np.exp(1.0 / Ts) / (1.0 + np.exp(1.0 / Ts)) ** 2 / Ts ** 4         # wrt T
    I_U = 1.0 / I_beta                                                       # wrt U/Delta, the energy in quanta (A1' 'one quantum' unit): 1/(p(1-p))
    x_lnT = float(xs[np.argmax(I_lnT)]); x_beta = float(xs[np.argmax(I_beta)]); I_beta_max = float(I_beta.max())
    T_peak = float(Ts[np.argmax(I_T)]); x_sch = _schottky_x(); T_sch = 1.0 / x_sch
    x_Umin = float(xs[np.argmin(I_U)]); I_U_min = float(I_U.min()); I_U_end = float(I_U[-1])
    arc_total = 2.0 * math.asin(math.sqrt(0.5))
    check = rel(x_lnT, x_sch) <= 1e-3
    out = outcome(crr=x_lnT, null=x_sch, domain=x_sch, check=check)
    return make_row("thermo", "Two-level Schottky system over temperature: heat capacity C/k_B = x^2 e^x/(1 + e^x)^2, x = beta Delta, and the Fisher information of the Bernoulli family in four coordinates (Daniel's battery row c2 re-read)",
                    source="runs/phaseA/crr_retrodictions.txt [c2] (CONSIST)",
                    Q="the Schottky heat-capacity peak is the peak of the family's Fisher information in the log-temperature coordinate",
                    ingredient="A1 (the Fisher metric) in a chosen coordinate - NOT CRR-proper; the proper ingredient tried as the selector of the coordinate is A1' (the system's own unit, one quantum Delta)",
                    null="the same peak by the domain's fluctuation identity C/k_B = beta^2 Var(E) (the same function, identical by construction)",
                    domain="the fluctuation-dissipation identity C_V = k_B beta^2 Var(E): the heat capacity is beta^2 times the beta-Fisher information, i.e. the Fisher information in ln beta",
                    numbers=f"Fisher peak in ln T at x = {x_lnT:.4f} (grid), Schottky peak (root of the stationarity condition) at x = {x_sch:.4f} = T/Delta {T_sch:.4f}; Fisher peak in beta at x = {x_beta:.4f} (T = infinity, value {I_beta_max:.4f}); Fisher peak in T at T/Delta = {T_peak:.4f} (x = {1.0 / T_peak:.4f}); Fisher information in U/Delta (the A1' one-quantum coordinate): minimum {I_U_min:.4f} at x = {x_Umin:.4f}, {I_U_end:.2e} at x = 12 - no peak, it diverges at both ends; in the arc coordinate the density is 1 by definition over a total arc {arc_total:.4f} = pi/2 - no peak",
                    tg=f"ln-T Fisher peak {x_lnT:.4f} vs null (the identity's C peak) {x_sch:.4f}: {_word(rel(x_lnT, x_sch) <= TOL_G, 'agree', 'differ')} (no CRR-proper ingredient in Q)",
                    tn=f"the fluctuation identity gives {x_sch:.4f}: {_word(rel(x_lnT, x_sch) <= TOL_N, 'the domain has Q', 'the domain does not give Q')}",
                    tc=f"ln-T Fisher peak within 1e-3 of the Schottky peak: {_word(check, 'holds', 'fails')} (true, and it is the domain's identity)",
                    out=out,
                    reading=f"four coordinates, four answers (x = {x_beta:.4f}, {1.0 / T_peak:.4f}, {x_lnT:.4f}, none): the Fisher 'peak' is a density and a density has no coordinate-free maximum; A1' was tried as the selector and gives the energy-in-quanta coordinate, where the information has a minimum, not a peak; the one coordinate that reproduces the Schottky peak does so by the domain's own identity, so no Q with a CRR-proper ingredient forms and the label is {out}; the source row's finding (none selected by the framework) stands",
                    weakness=f"Delta = 1; the grids fix the peak locations to their spacing ({xs[1] - xs[0]:.1e} in x, {Ts[1] - Ts[0]:.1e} in T); the A1' coordinate is one reading of 'one quantum' (the source battery's row a5 has three)")


def main():
    return run_batch("Synthesis batch 05: rows 21-25 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
