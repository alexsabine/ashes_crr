"""Synthesis batch 01: rows 1-5 of QUEUE.md (prompt-log entry 61). [2] two-state chemical kinetics A <-> B (CONSIST);
[3] voltage-gated channel open probability on a ramp (DESCR); [4] Poisson counts (CONSIST); [5] qubit resonant Rabi
pi pulse (CONSIST); [6] qubit detuned drive, Anandan-Aharonov / Mandelstam-Tamm bound (CONSIST). All five source rows
are in theory/retrodictions/crr_retrodictions.txt; their models are re-implemented here (nothing imported from the
battery scripts). Deterministic; no data file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_01.py
"""
import math
import sys

import numpy as np
from scipy.integrate import quad

from crr.instrument.core import antipodal_cuts, intrinsic_phase, peak_cuts
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/crr_retrodictions.txt"


def _agree(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def _holds(flag):
    return "holds" if flag else "fails"


# ---------------------------------------------------------------- 1  two-state chemical kinetics (source row [2])
def r1():
    k1, k2, p0, T, N = 0.7, 0.3, 0.05, 6.0, 1000                    # the source row's constants; N molecules is added for A1'
    pinf = k1 / (k1 + k2); k = k1 + k2
    pt = lambda t: pinf + (p0 - pinf) * math.exp(-k * t)
    pdot = lambda t: -k * (p0 - pinf) * math.exp(-k * t)
    C, _ = quad(lambda t: abs(pdot(t)) / math.sqrt(pt(t) * (1 - pt(t))), 0, T)     # D2 on the Bernoulli carrier
    D = abs(2 * math.asin(math.sqrt(pt(T))) - 2 * math.asin(math.sqrt(p0)))       # D3 = the arcsine distance (information geometry's)
    S = C - D
    rho_fisher = math.sqrt(N) * D                                    # A1' unit = one molecule: binomial(N) Fisher metric N/(p(1-p))
    rho_ident = N * abs(pt(T) - p0)                                  # the same unit under the identity metric (H-L5 control ii)
    check = abs(S) < 1e-9
    out = outcome(crr=C, null=D, domain=D, check=check)
    return make_row("chem", f"Two-state chemical kinetics A <-> B, mass-action relaxation k1 = {k1:g}, k2 = {k2:g} from p0 = {p0:g} over T = {T:g} (Bernoulli carrier)",
                    source=f"{SRC} [2] (CONSIST)",
                    Q="the coherence of a monotone mass-action relaxation is the arcsine distance between its endpoints (S = 0: the relaxation is a Fisher-Rao geodesic)",
                    ingredient="D2 (arc), D3 (chord), D4 (surplus) - NOT CRR-proper: all three are information geometry's; no CRR-proper ingredient could be attached to the source row (see weakness)",
                    null="the arcsine coordinate change itself, information geometry's closed-form geodesic distance on the Bernoulli family (identical by construction)",
                    domain="the variance-stabilising arcsine transform of a proportion: d = 2 |asin sqrt(p2) - asin sqrt(p1)|",
                    numbers=f"C = {C:.6f} (numeric integral of the Fisher speed), D = {D:.6f} (closed form), S = {S:.2e}; A1' tried with one molecule as the unit (N = {N}): rho = sqrt(N) D = {rho_fisher:.4f} standard errors under the binomial Fisher metric, {rho_ident:.2f} net conversions under the identity metric (control ii)",
                    tg=f"C {C:.6f} vs null (arcsine distance) {D:.6f}: {_agree(C, D)} (no CRR-proper ingredient in Q)",
                    tn=f"the domain's transform gives {D:.6f}: {_agree(C, D, TOL_N)} - the domain has Q",
                    tc=f"|S| < 1e-9 (geodesic): {_holds(check)} (true, and it is P1 on a monotone segment, which CRR.md itself says is not a result of CRR)",
                    out=out,
                    reading=f"the source row's content is exactly D2-D4 on a monotone path, and T-G shows CRR did not add it: the arc is the arcsine coordinate change and the surplus is zero by P1; the row reads {out} by construction, as synthesis.py row 6 does",
                    weakness=f"CRR-proper ingredients tried and dropped: A3/D5 - a monotone relaxation has no rotor (O3), so there is no cut and no occasion; A1'/D1 with one molecule as the unit - rho = {rho_fisher:.4f} is Fisher additivity (sqrt N times the arcsine distance, queue row 10), the domain's stoichiometry under the identity metric, and D1 says CRR does not predict rho; H-L5 with every reaction event as its own cut - the arc per event is one unit by the definition in A1', so its regularity is D1 read back, not a class claim; A6 - no occasions to regenerate from")


# ---------------------------------------------------------------- 2  voltage-gated channel on a ramp (source row [3])
def r2():
    Vh, s, N, V0, V1 = -40.0, 6.0, 100, -80.0, 0.0                   # Boltzmann curve of the source row; N channels in the patch is added for A1'
    p = lambda V: 1 / (1 + math.exp(-(V - Vh) / s))
    dp = lambda V: p(V) * (1 - p(V)) / s
    D = abs(2 * math.asin(math.sqrt(p(V1))) - 2 * math.asin(math.sqrt(p(V0))))   # the source row's arc for one channel
    rho_crr = math.sqrt(N) * D                                       # A1'/D1: unit = one channel of N; binomial(N) Fisher metric
    rho_null = N * abs(p(V1) - p(V0))                                # the same unit, identity metric (H-L5 control ii)
    rho_dom, _ = quad(lambda V: math.sqrt(N * dp(V) ** 2 / (p(V) * (1 - p(V)))), V0, V1)   # Cramer-Rao: standard errors of V-hat spanned, I_N = N I_1
    rates = (1.0, 10.0)                                              # mV per unit time
    arc_t = []
    for r in rates:                                                  # the same arc as a time integral over the ramp, two ramp speeds
        Tr = (V1 - V0) / r
        val, _ = quad(lambda t: math.sqrt(N) * abs(dp(V0 + r * t) * r) / math.sqrt(p(V0 + r * t) * (1 - p(V0 + r * t))), 0, Tr)
        arc_t.append(val)
    rho_mv = (V1 - V0) / 1.0                                         # another outside unit: one millivolt of command voltage
    check = rel(rho_dom, rho_crr) <= 1e-6 and rel(arc_t[0], arc_t[1]) <= 1e-6
    out = outcome(crr=rho_crr, null=rho_null, domain=rho_dom, check=check)
    return make_row("chan", f"Voltage-gated channel open probability, Boltzmann curve (V_half = {Vh:g} mV, slope {s:g} mV), ramp {V0:g} -> {V1:g} mV, a patch of N = {N} channels",
                    source=f"{SRC} [3] (DESCR)",
                    Q=f"between {V0:g} and {V1:g} mV a patch of N = {N} channels passes through rho = {rho_crr:.2f} resolvable steps of open probability (one standard error of the open-channel count each), whatever the ramp speed",
                    ingredient="A1'/D1 (the unit is the system's own step: one channel event out of N; rho = extent / unit), D2 on the binomial carrier",
                    null="the same unit under the identity metric (H-L5 control ii): net change of the open fraction in channel units",
                    domain="the Cramer-Rao bound with Fisher additivity I_N = N I_1: the number of standard errors of V-hat spanned by the ramp is the integral of sqrt(N I_1(V)) dV",
                    numbers=f"one-channel arc = {D:.5f}; rho with the A1' unit = sqrt(N) x arc = {rho_crr:.4f}; identity-metric null = {rho_null:.4f}; Cramer-Rao quadrature = {rho_dom:.4f}; the arc as a time integral at ramp speeds {rates[0]:g} and {rates[1]:g} mV per unit time = {arc_t[0]:.5f} and {arc_t[1]:.5f} (relative difference {rel(arc_t[0], arc_t[1]):.1e}); one millivolt of command voltage as the unit gives {rho_mv:.4f} steps",
                    tg=f"rho {rho_crr:.4f} vs null {rho_null:.4f}: {_agree(rho_crr, rho_null)}",
                    tn=f"Cramer-Rao with I_N = N I_1 gives {rho_dom:.4f}: {_agree(rho_crr, rho_dom, TOL_N)} - the domain has Q",
                    tc=f"quadrature equals the closed form within 1e-6 and the two ramp speeds agree within 1e-6: {_holds(check)}",
                    out=out,
                    reading=f"naming one channel as the unit turns the source row's arc into the Cramer-Rao count of standard errors across the activation range, which is Fisher additivity (battery row 14, DESCR) applied to the Boltzmann curve; the domain states rho as sqrt(N) times the arcsine distance without D1, and D1 itself says CRR does not predict rho, so no number in Q is CRR's: {out}",
                    weakness=f"the identity-metric null is one outside unit among many (one millivolt of command voltage, {rho_mv:.4f} steps vs rho {rho_crr:.4f}: {_agree(rho_mv, rho_crr)}) and none of them is the domain's; a class claim (H-L5) on the channel's own gating events would need the kinetics alpha(V), beta(V), which the source row does not carry, and was not attempted")


# ---------------------------------------------------------------- 3  Poisson counts: two readings of the unit (source row [4])
def r3():
    l1, l2, lam_mc, n_mc = 4.0, 9.0, 5.0, 200000
    arc_window = 2 * (math.sqrt(l2) - math.sqrt(l1))                # count reading: Poisson(lam * Delta) per window, Fisher Delta/lam, Delta = 1
    arc_window2 = math.sqrt(2.0) * arc_window                        # the same at Delta = 2 (the arc scales with sqrt Delta)
    arc_event = math.log(l2 / l1)                                    # event reading: one event = one step; waiting time Exp(lam), Fisher 1/lam^2
    arc_natural, _ = quad(lambda lam: math.sqrt((1.0 / lam) / lam), l1, l2)   # count reading with the natural-time window Delta = 1/lam (one expected event per window)
    rng = np.random.default_rng(0)                                   # the two Fisher informations, checked as score variances (the domain's own definition)
    x = rng.poisson(lam_mc, n_mc); I_count = float((x / lam_mc - 1.0).var())
    tau = rng.exponential(1.0 / lam_mc, n_mc); I_event = float((1.0 / lam_mc - tau).var())
    internal = rel(arc_window, arc_event) > TOL_G
    out = outcome(crr=arc_event, null=arc_window, domain=None, check=None, internal=internal)
    return make_row("count", f"Poisson counts (epidemic incidence, photon counts): a rate change lambda = {l1:g} -> {l2:g} events per unit time, the unit read from A1' (one event = one step)",
                    source=f"{SRC} [4] (CONSIST)",
                    Q="the coherence of a rate change counted in the system's own unit (A1': one event = one step, time = natural time) is the Fisher-Rao arc per event, |ln lambda2 - ln lambda1|, not the per-window arc 2 |sqrt lambda2 - sqrt lambda1| that the source row and the ledger's carrier use",
                    ingredient="A1' (unit = one event, natural time), D2 on the Poisson carrier",
                    null="the per-window count reading: Poisson(lambda Delta) counts in a clock window Delta, Fisher information Delta / lambda (the carrier of core.poisson_transform, to which the measles study MEAS2 fed biweekly counts: Delta = the reporting fortnight)",
                    domain="the variance-stabilising transforms of the two families: 2 sqrt for Poisson counts (Anscombe), log for exponential waiting times",
                    numbers=f"per-window arc (Delta = 1) = {arc_window:.4f}, at Delta = 2 it is {arc_window2:.4f} (scales with sqrt Delta); per-event arc = ln({l2:g}/{l1:g}) = {arc_event:.4f}; per-window arc with the natural-time window Delta = 1/lambda (one expected event per window) = {arc_natural:.4f}; Fisher information at lambda = {lam_mc:g} as a score variance over {n_mc} draws (seed 0): per unit-window count {I_count:.4f} (closed form 1/lambda = {1 / lam_mc:.4f}), per event {I_event:.5f} (closed form 1/lambda^2 = {1 / lam_mc ** 2:.5f})",
                    tg=f"event reading {arc_event:.4f} vs window reading {arc_window:.4f}: {_agree(arc_event, arc_window)} - and both are readings of the same ingredient A1', so the disagreement is internal",
                    tn="each reading is a domain transform (2 sqrt for counts, log for waiting times); whichever the theory fixes, the domain already has it",
                    tc="not reached: the two readings of the ingredient must agree before Q can be checked",
                    out=out,
                    reading=f"A1' says the unit of a point process is one event and time is the event count; the Fisher metric that belongs to that unit is the waiting-time family's, 1/lambda^2 per event, whose arc is logarithmic ({arc_event:.4f}); the carrier the source row and the ledger's measles study used is the count family's, Delta/lambda per clock window, whose arc is {arc_window:.4f} at Delta = 1 and {arc_window2:.4f} at Delta = 2 - the reporting interval, an outside constant, sits inside the unit; the two readings coincide when the window is the natural-time one, Delta = 1/lambda (count arc {arc_natural:.4f} vs event arc {arc_event:.4f}: {_agree(arc_natural, arc_event)}); which reading is A1' on a Poisson carrier is a theory decision (v3.2) to make before an H-L5 verdict on counts (MEAS2-1, scored on the count reading at the reporting fortnight) is read as a verdict on the theory: {out}",
                    weakness="the log arc is the count arc with a rate-dependent window, so the fix is a choice of window, not a new metric; the row does not say which choice would have changed the measles verdict, and nothing here re-scores that study (R3)")


# ---------------------------------------------------------------- 4, 5  qubit: the readings of A3 on the Bloch sphere
def _cross(t, y, level):
    """First time y reaches `level` (linear interpolation on the grid), or None."""
    i = int(np.argmax(y >= level))
    if i == 0:
        return None
    return float(t[i - 1] + (level - y[i - 1]) / (y[i] - y[i - 1]) * (t[i] - t[i - 1]))


def _qubit(Om, Delta, n_periods=8, n=80001):
    """State path of a qubit from |0> under H = (Delta sigma_z + Om sigma_x)/2 on a fixed grid of n points over n_periods precession
    periods, in the source rows' Fubini-Study convention (arc = arccos |<psi|phi>| between neighbours; orthogonality at pi/2)."""
    Omp = math.sqrt(Om ** 2 + Delta ** 2)
    t = np.linspace(0.0, n_periods * 2 * math.pi / Omp, n)
    Hm = 0.5 * np.array([[Delta, Om], [Om, -Delta]]); w, V = np.linalg.eigh(Hm)
    psi0 = np.array([1.0, 0.0], complex); coef = V.conj().T @ psi0
    st = (V @ (np.exp(-1j * np.outer(w, t)) * coef[:, None])).T
    ov = np.abs(np.sum(np.conj(st[:-1]) * st[1:], 1))
    C = np.concatenate([[0.0], np.cumsum(np.arccos(np.clip(ov, -1.0, 1.0)))])          # D2, accumulated from t = 0
    chord = np.arccos(np.clip(np.abs(st @ np.conj(psi0)), -1.0, 1.0))                  # D3 to the start
    sz = 1.0 - 2.0 * np.abs(st[:, 1]) ** 2                                             # <sigma_z>(t), the domain's observable
    dE = float(np.sqrt(np.vdot(psi0, Hm @ Hm @ psi0).real - np.vdot(psi0, Hm @ psi0).real ** 2))
    period = 2 * math.pi / Omp
    d = dict(Om=Om, Delta=Delta, Omp=Omp, dE=dE, period=period, dt=float(t[1] - t[0]))
    d["t_arc"] = _cross(t, C, math.pi / 2)                                             # reading (i): the arc has advanced half a turn (C = pi/2)
    d["t_mt"] = math.pi / (2 * dE)                                                     # Mandelstam-Tamm time (closed form of reading (i))
    first = slice(0, n // n_periods + 1)
    d["chord_max"] = float(chord[first].max()); d["t_chord_max"] = float(t[first][int(np.argmax(chord[first]))])
    d["t_anti"] = _cross(t, chord, math.pi / 2 - 1e-6)                                 # reading (ii): the antipode (first orthogonal state), if any
    cuts = antipodal_cuts(intrinsic_phase(sz))                                         # reading (iii): the rotor - the instrument's oriented phase criterion on <sigma_z>
    d["t_rotor"] = float(t[cuts[1]]); d["C_rotor"] = float(np.interp(d["t_rotor"], t, C))
    d["t_rotor_closed"] = math.pi / Omp                                                # half the precession period about the effective field
    d["L"] = float(np.interp(period, t, C)); d["L_closed"] = math.pi * Om / Omp        # rotor circumference: arc over one precession period = pi sin(cone angle)
    pk = peak_cuts(sz, prominence=0.1, distance=10)
    d["t_peak"] = float(t[pk[0]] if pk[0] != 0 else t[pk[1]])                          # the population extremum (the domain's pi-pulse marker; H-CUT's extremum)
    return d


def r4():
    d = _qubit(1.0, 0.0)
    readings = [d["t_arc"], d["t_anti"], d["t_rotor"]]
    internal = any(v is None for v in readings) or any(rel(readings[0], v) > TOL_G for v in readings[1:])
    check = (d["t_anti"] is not None) and rel(d["t_anti"], d["t_chord_max"]) <= 1e-3 and abs(d["chord_max"] - math.pi / 2) < 1e-6
    out = outcome(crr=d["t_rotor"], null=d["t_peak"], domain=math.pi / d["Om"], check=check, internal=internal)
    return make_row("qm", f"Qubit, resonant Rabi drive Omega = {d['Om']:g} from |0> (pi pulse); Fubini-Study carrier in the source rows' convention (orthogonality at pi/2; synthesis.py row 4 uses twice this)",
                    source=f"{SRC} [5] (CONSIST)",
                    Q="the first cut of a resonantly driven qubit is the pi pulse: A3 fires at t = pi/Omega, the first orthogonal state, and every reading of A3 (arc half-turn, antipode, rotor half-turn) places it there",
                    ingredient="A3 (the cut) read three ways: (i) the arc has advanced half a turn, C = pi/2; (ii) the antipode = the first orthogonal state; (iii) the rotor: the instrument's antipodal_cuts on the intrinsic phase of <sigma_z>(t); with D5",
                    null="the population extremum (the first interior extremum of <sigma_z>, a peak cut): the domain's own marker of the pi pulse, and the extremum H-CUT sets against the antipode",
                    domain="a pi pulse takes |0> to |1> at t = pi/Omega along a great circle (the Hamiltonian's number)",
                    numbers=f"dE = {d['dE']:.4f}; reading (i) arc half-turn at t = {d['t_arc']:.4f} (Mandelstam-Tamm time pi/(2 dE) = {d['t_mt']:.4f}); reading (ii) antipode at t = {d['t_anti']:.4f} (chord maximum {d['chord_max']:.4f} at t = {d['t_chord_max']:.4f}, |chord max - pi/2| = {abs(d['chord_max'] - math.pi / 2):.1e}); reading (iii) rotor cut at t = {d['t_rotor']:.4f} (closed form pi/Omega' = {d['t_rotor_closed']:.4f}; rotor circumference L = arc over one period = {d['L']:.4f}, closed form pi Omega/Omega' = {d['L_closed']:.4f}; C at the cut = {d['C_rotor']:.4f} vs L/2 = {d['L'] / 2:.4f}: {_agree(d['C_rotor'], d['L'] / 2)}); population extremum at t = {d['t_peak']:.4f}; grid step {d['dt']:.2e}",
                    tg=f"rotor cut {d['t_rotor']:.4f} vs null extremum {d['t_peak']:.4f}: {_agree(d['t_rotor'], d['t_peak'])}; the three readings of A3 {'agree' if not internal else 'differ'} among themselves ((i) {d['t_arc']:.4f}, (ii) {d['t_anti']:.4f}, (iii) {d['t_rotor']:.4f}), so the ingredient is fixed on this carrier",
                    tn=f"the domain's pi-pulse time pi/Omega = {math.pi / d['Om']:.4f}: {_agree(d['t_rotor'], math.pi / d['Om'], TOL_N)}",
                    tc=f"the cut is at the first orthogonal state (chord reaches pi/2 within 1e-6 at the antipode time): {_holds(check)}",
                    out=out,
                    reading=f"on the resonant drive the antipode and the population extremum coincide, which CRR.md's H-CUT names as the case where A3 cannot be tested (symmetric cycles); the cut A3 places is the pi pulse the domain defined by its population inversion, and T-G shows the peak finder places it too: {out}; the three readings that split on the detuned drive (row 5) agree here because the path is a great circle (a geodesic)",
                    weakness="the resonant qubit is the pure-sine negative control of the quantum battery; the source row's CONSIST was the P1 equality C = D on a geodesic, which is information geometry's",
                    elegance="Half a turn, no knobs: on a great circle, going halfway round lands you at the point opposite your start, and that point is also the farthest you can get and the top of the population swing. One picture gives A3's rule and, in the same stroke, why the rule cannot be tested on a perfectly round trip: the far point and the turning point are one place.",
                    child="Imagine walking halfway around a big ball. You end up exactly opposite where you began, and that is also the farthest you can ever get from your start. On a perfectly round trip 'halfway round' and 'farthest away' are the same spot, so you cannot tell which one a rule is really using. To tell them apart you need a lopsided trip.")


def r5():
    d = _qubit(1.0, 0.8)
    exists = d["t_anti"] is not None
    internal = (not exists) or rel(d["t_arc"], d["t_rotor"]) > TOL_G or rel(d["t_arc"], d["t_anti"]) > TOL_G
    out = outcome(crr=d["t_rotor"], null=d["t_peak"], domain=d["t_rotor_closed"], check=None, internal=internal)
    anti_txt = f"at t = {d['t_anti']:.4f}" if exists else f"none: chord maximum {d['chord_max']:.4f} < pi/2 = {math.pi / 2:.4f}, reached at t = {d['t_chord_max']:.4f}"
    order = "later" if d["t_arc"] > d["t_rotor"] else "earlier"
    half = ("inside the second half of the precession" if d["period"] / 2 < d["t_arc"] < d["period"]
            else "inside the first half of the precession" if d["t_arc"] <= d["period"] / 2 else "after the first precession")
    ortho = f"the orthogonal reading never fires ({d['chord_max']:.4f} < pi/2)" if not exists else f"the orthogonal reading fires at {d['t_anti']:.4f}"
    return make_row("qm", f"Qubit, detuned drive Omega = {d['Om']:g}, Delta = {d['Delta']:g} from |0> (generalised Rabi frequency Omega' = {d['Omp']:.4f}); Fubini-Study carrier as row 4",
                    source=f"{SRC} [6] (CONSIST)",
                    Q="the first cut of a detuned qubit is one time fixed by A3 (attempted; the readings of A3 must agree for Q to have a value)",
                    ingredient="A3 read three ways as in row 4: (i) arc half-turn C = pi/2; (ii) the antipode (first orthogonal state); (iii) the rotor: antipodal_cuts on the intrinsic phase of <sigma_z>(t), i.e. half a precession about the effective field (Omega, 0, Delta)/Omega'",
                    null="the population extremum (peak cut on <sigma_z>)",
                    domain="the generalised Rabi formula P1(t) = (Omega/Omega')^2 sin^2(Omega' t / 2): population maximum at pi/Omega'; Anandan-Aharonov / Mandelstam-Tamm: orthogonality, if reached at all, not before pi/(2 dE)",
                    numbers=f"dE = {d['dE']:.4f}, precession period 2 pi/Omega' = {d['period']:.4f}; reading (i) arc half-turn at t = {d['t_arc']:.4f} (Mandelstam-Tamm time pi/(2 dE) = {d['t_mt']:.4f}); reading (ii) antipode {anti_txt}; reading (iii) rotor cut at t = {d['t_rotor']:.4f} (closed form pi/Omega' = {d['t_rotor_closed']:.4f}; L = arc over one period = {d['L']:.4f}, closed form pi Omega/Omega' = {d['L_closed']:.4f}; C at the cut = {d['C_rotor']:.4f} vs L/2 = {d['L'] / 2:.4f}: {_agree(d['C_rotor'], d['L'] / 2)}); population extremum at t = {d['t_peak']:.4f}; grid step {d['dt']:.2e}",
                    tg=f"arc reading {d['t_arc']:.4f} vs rotor reading {d['t_rotor']:.4f}: {_agree(d['t_arc'], d['t_rotor'])}; antipode reading: {'present' if exists else 'absent'}; rotor reading vs null extremum {d['t_peak']:.4f}: {_agree(d['t_rotor'], d['t_peak'])}",
                    tn=f"every reading that exists is a number the domain owns: the rotor half-turn is the generalised-Rabi population maximum pi/Omega' = {d['t_rotor_closed']:.4f} ({_agree(d['t_rotor'], d['t_rotor_closed'], TOL_N)}), the arc half-turn is the Mandelstam-Tamm time {d['t_mt']:.4f} ({_agree(d['t_arc'], d['t_mt'], TOL_N)})",
                    tc="not reached: the readings of the ingredient must agree before Q can be checked",
                    out=out,
                    reading=f"the detuned qubit is genuinely cyclic, so unlike the three-level case of synthesis.py row 4 the rotor reading of A3 exists and is well defined: the Bloch vector precesses about the effective field and the instrument's phase cut fires at half a precession, t = {d['t_rotor']:.4f}, where the population turns - the extremum again, so H-CUT is untestable here too; the arc reading fires {order}, at {d['t_arc']:.4f}, {half}, and {ortho}; whichever reading the theory fixes lands on a number the domain already has, so the row can only fall to REDUNDANT-DOMAIN or stay {out} - the decision is item 3 of the synthesis note's section 7",
                    weakness="the source rows' Fubini-Study convention halves the arcs of synthesis.py row 4; the three readings and their disagreement do not depend on it; the rotor reading is taken on <sigma_z>, one observable of the precession, and the closed form shows any observable of the precession gives the same phase")


def main():
    return run_batch("Synthesis batch 01: rows 1-5 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
