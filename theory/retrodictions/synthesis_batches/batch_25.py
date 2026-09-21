"""Synthesis batch 25: rows 121-125 of QUEUE.md (prompt-log entry 61). All five from the loop-gravity battery
theory/retrodictions/loop_gravity.txt (script loop_gravity.py):
[1] black-hole entropy by state counting on a punctured horizon, the Immirzi parameter fixed by S = A/4 (DESCR);
[2] the LQG area spectrum: a fundamental quantum of area against CRR's estimated unit (DESCR);
[4] the massless scalar as LQC's relational clock: the volume's logarithmic speed in the phi clock (DESCR);
[5] cyclic loop cosmology with a Tolman entropy increment: are the cycles arc- or clock-regular (DESCR);
[6] spin-j coherent states: the antipode and the Fisher length of a half-turn (DESCR).
Earlier synthesis readings on these systems are not repeated: synthesis.py row 11 named the smallest area quantum as
the unit (entropy per named step, REDUNDANT-DOMAIN), row 9 read the Tolman cycles against A6 (WRONG), row 10 read
thermal time (UNSTATED); batch 01 row 4 and batch 05 row 3 read the spin-1/2 coherent state's three A3 readings
(INTERNAL). Models re-implemented from the source functions (bh_entropy_immirzi, area_spectrum_unit,
relational_clock, cyclic_tolman, spin_coherent_states); nothing imported from theory/retrodictions. Planck units.
Deterministic (fixed grids, fixed-step RK4, seed 0), no data (R2). Literature by name and year only, not fetched (R10).
Run:  uv run python theory/retrodictions/synthesis_batches/batch_25.py
"""
import itertools
import math
import sys

import numpy as np
from scipy import optimize
from scipy.linalg import expm

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts, regularity, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _word(cond, yes, no):
    return yes if cond else no


def _hf(cond):
    return _word(cond, "holds", "fails")


# ---------------------------------------------------------------- the countings (source row 1), shared by rows 1 and 2
_JS = np.arange(1, 400) / 2.0
_X = np.sqrt(_JS * (_JS + 1))


def _gamma(mult):
    """Immirzi parameter of a counting with `mult` states per puncture of spin j: sum_j mult_j e^(-2 pi gamma x_j) = 1."""
    return float(optimize.brentq(lambda g: float(np.sum(mult * np.exp(-2 * math.pi * g * _X))) - 1.0, 0.05, 1.0, xtol=1e-14))


# ---------------------------------------------------------------- 121 [1] A1' estimated on the punctures
def _counting(name, gamma, mult, seed=0, n_draw=2000):
    """The dominant configuration of a counting: Gibbs weights p_j = mult_j e^(-2 pi gamma x_j) (they sum to 1 by the
    gamma condition); the puncture as the occasion, its area a_j = 8 pi gamma x_j as the occasion statistic."""
    p = mult * np.exp(-2 * math.pi * gamma * _X)
    a = 8 * math.pi * gamma * _X
    mean_a = float((p * a).sum())
    H = float(-(p * np.log(p)).sum())                                      # entropy of the composition
    ln_m = float((p * np.log(mult)).sum())                                 # mean log of the states per puncture
    per_event = mean_a / 4.0                                               # S = A/4 = N <a>/4: entropy per puncture (one puncture = one step)
    cum = np.cumsum(p); i_med = int(np.searchsorted(cum, 0.5)); med = float(a[i_med]); j_med = float(_JS[i_med])
    dev = np.abs(a - med); order = np.argsort(dev, kind="stable"); cumd = np.cumsum(p[order])
    mad = float(dev[order][int(np.searchsorted(cumd, 0.5))])               # population MAD about the median (constant detrender)
    sig_pop = 1.4826 * mad
    rng = np.random.default_rng(seed); draw = rng.choice(a, size=n_draw, p=p / p.sum())
    try:
        sig_inst = unit_sigma(draw)                                        # the instrument as registered (savgol 9/2, MAD)
    except ValueError:
        sig_inst = None
    return dict(name=name, gamma=gamma, p_half=float(p[0]), j_med=j_med, mean_a=mean_a, H=H, ln_m=ln_m, per_event=per_event,
                a_min=float(a[0]), sig_pop=sig_pop, sig_inst=sig_inst, pop_std=float(math.sqrt((p * (a - mean_a) ** 2).sum())))


def r1():
    g_two = _gamma(2.0 * np.ones_like(_JS)); g_deg = _gamma(2 * _JS + 1)
    g_half = math.log(2.0) / (math.pi * math.sqrt(3.0)); a_half = 8 * math.pi * g_half * math.sqrt(0.75)
    two = _counting("all-j two-state (Domagala-Lewandowski, Meissner)", g_two, 2.0 * np.ones_like(_JS))
    deg = _counting("all-j (2j+1)-state (Ghosh-Mitra)", g_deg, 2 * _JS + 1)
    try:
        unit_sigma(np.full(2000, a_half)); half_msg = "unit_sigma returned a value"
    except ValueError as e:
        half_msg = f"unit_sigma raised '{e}'"
    crr = two["per_event"]; null = two["a_min"] / 4.0                      # the event reading; D1's named quantum (synthesis row 11)
    domain = two["mean_a"] / 4.0
    identity = all(rel(c["per_event"], c["H"] + c["ln_m"]) <= 1e-12 for c in (two, deg))
    resid_two = two["sig_inst"] / 4.0 if two["sig_inst"] is not None else None
    internal = resid_two is None or rel(crr, resid_two) > TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=identity, internal=internal)
    n_degenerate = sum(1 for c in (two, deg) if c["sig_pop"] == 0.0) + 1  # + the j = 1/2 counting (all punctures equal)

    def desc(c):
        pop = f"population MAD about the median = {c['sig_pop'] / 1.4826:.4f} -> sigma = {c['sig_pop']:.4f} l_P^2" + (" (degenerate: record rejected, no floor)" if c["sig_pop"] == 0.0 else f" -> {c['sig_pop'] / 4:.4f} nats per step")
        inst = f"instrument unit_sigma on {2000} seeded draws (savgol 9/2, MAD) = {c['sig_inst']:.4f} l_P^2 -> {c['sig_inst'] / 4:.4f} nats per step" if c["sig_inst"] is not None else "instrument unit_sigma raised"
        return (f"{c['name']}: gamma = {c['gamma']:.4f}, p(j = 1/2) = {c['p_half']:.4f}, median puncture j = {c['j_med']:g}, <a> = {c['mean_a']:.4f} l_P^2, A_min = {c['a_min']:.4f}; "
                f"event reading (one puncture = one step): S/N = <a>/4 = {c['per_event']:.4f} nats = {c['per_event'] / math.log(2):.4f} bits, and H(p) + <ln m_j> = {c['H'] + c['ln_m']:.4f}; "
                f"residual reading: {pop}; {inst}; population std of the puncture area {c['pop_std']:.4f}")

    return make_row("bh", "A quantum horizon of N punctures with S = A/4 under the source row's three countings (j = 1/2 two-state; all-j two-state; all-j (2j+1)-state), the puncture as the occasion and its area as the occasion statistic, A1' applied as written (estimated, never named); synthesis.py row 11 named the smallest quantum as the unit and is not repeated",
                    source="theory/retrodictions/loop_gravity.txt [1] (DESCR)",
                    Q="the entropy per resolvable step of the horizon, with the step taken from A1' as written: under A1''s point-process reading (one puncture = one step) it is the counting's entropy per puncture, <a>/4 = H(p) + <ln m_j> nats; under A1''s residual reading (sigma = 1.4826 MAD of the occasion statistic, no floor) the horizon is rejected as a record wherever the majority puncture is the same puncture",
                    ingredient="A1'/D1 in its two operational readings (the event unit; the residual-scale unit with the MAD scale and no floor) on the puncture composition the counting fixes; D1's rho = A/sigma reported, never predicted",
                    null="D1's named step, the smallest quantum A(1/2) (the domain's 'quantum of area'; synthesis row 11's unit): entropy per named step A_min/4",
                    domain="the countings themselves: S = A/4 = N <a>/4 on the dominant configuration, whose Gibbs weight is p_j proportional to m_j e^(-2 pi gamma sqrt(j(j+1))) (Meissner 2004; Domagala-Lewandowski 2004; Ghosh-Mitra 2005), so the entropy per puncture is <a>/4 = H(p) + <ln m_j>",
                    numbers=f"j = 1/2 two-state counting: gamma = {g_half:.4f}, every puncture a = {a_half:.4f} l_P^2, S/N = ln 2 = {a_half / 4:.4f} nats; residual reading: {half_msg}. " + desc(two) + ". " + desc(deg)
                            + f". Countings under which the residual reading rejects the horizon as a record (population MAD = 0): {n_degenerate} of 3",
                    tg=f"event reading {crr:.4f} nats per step vs null (per named quantum, A_min/4) {null:.4f}: {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')} (two-state all-j counting)",
                    tn=f"the counting's S = N <a>/4 gives {domain:.4f} nats per puncture: {_word(rel(crr, domain) <= TOL_N, 'agree (the event reading is the domain', 'differ (the event reading is not the domain')}'s entropy per puncture); the identity <a>/4 = H(p) + <ln m_j> {_hf(identity)} on both all-j countings",
                    tc=f"not reached: the two readings of A1' give {crr:.4f} nats per step (event) and " + (f"{resid_two:.4f} (residual, on the instrument's seeded draw; the population residual is degenerate)" if resid_two is not None else "no unit (residual)") + " on the same horizon",
                    out=out,
                    reading=f"A1' estimated on a punctured horizon has two readings and they do not meet: the event reading returns the domain's entropy per puncture (the count is a definition, as the source row said), and the residual reading has nothing to estimate wherever the majority puncture is the same puncture, which is the case under the j = 1/2 counting (all equal) and under the two-state all-j counting (p(1/2) = {two['p_half']:.4f} > 1/2, so the median deviation is 0) and not under the (2j+1) counting (p(1/2) = {deg['p_half']:.4f}, median puncture j = {deg['j_med']:g}, sigma = {deg['sig_pop']:.4f} l_P^2, {deg['sig_pop'] / 4:.4f} nats per step, a number no counting names); the instrument's registered detrender on a seeded draw returns the composition's sampling scatter ({two['sig_inst']:.4f} and {deg['sig_inst']:.4f} l_P^2), which is the source battery's row-8 point again: the estimated unit is the scatter, not the quantum. The label is {out}; which reading is A1' on a fundamentally discrete carrier is a theory decision, and under either the entropy per step is the counting's",
                    weakness="the composition is the dominant configuration, not a sample of a horizon; the instrument's detrender assumes an order the punctures do not have (the draw order is the seed's), so its sigma is a sampling artefact by construction; which counting is right is the field's question (the source row's weakness stands); citations by name and year only, not fetched (R10)",
                    elegance="You cannot measure the size of a brick by how much the bricks differ if they are all the same brick. A rule about measuring with no knobs, and it says exactly where CRR's own unit stops working: on anything built from identical pieces.",
                    child="One way to learn how big a brick is, without a ruler, is to look at how much the bricks in a wall differ from each other. But if every brick is exactly the same, there is no difference to look at, and that way of measuring gives up; you just have to pick up one brick. In this theory a black hole's surface is a wall of mostly identical bricks, so the difference-measuring rule gives up on it.")


# ---------------------------------------------------------------- 122 [2] A1' as the smallest change of the total-area spectrum
def r2():
    gamma = _gamma(2.0 * np.ones_like(_JS)); jmax = 3.0
    js = np.arange(1, int(2 * jmax) + 1) / 2.0; a = 8 * math.pi * gamma * np.sqrt(js * (js + 1))
    single_gaps = np.diff(a); a_gap = float(a[0]); asym = 4 * math.pi * gamma        # consecutive j differ by 1/2: gap -> 8 pi gamma / 2
    res = []
    for N in range(1, 13):
        vals = np.array([sum(a[i] for i in comb) for comb in itertools.combinations_with_replacement(range(len(js)), N)])
        u = np.unique(np.round(vals, 9)); gaps = np.diff(u)
        res.append(dict(N=N, n=len(vals), n_distinct=len(u), min_gap=float(gaps.min()), mean_spacing=float((u[-1] - u[0]) / (len(u) - 1)) if len(u) > 1 else float("nan"), lo=float(u[0]), hi=float(u[-1])))
    by_N = {r["N"]: r for r in res}
    pairs = list(itertools.combinations_with_replacement(range(len(js)), 2)); sums2 = np.array([a[i] + a[k] for i, k in pairs])
    o = np.argsort(sums2); g2 = np.diff(sums2[o]); m = int(np.argmin(g2))
    pair_lo, pair_hi = pairs[o[m]], pairs[o[m + 1]]                          # the two configurations that realise the N = 2 spacing
    pair_txt = f"spins ({js[pair_lo[0]]:g}, {js[pair_lo[1]]:g}) against ({js[pair_hi[0]]:g}, {js[pair_hi[1]]:g})"
    crr = by_N[8]["min_gap"]; null = a_gap; domain = by_N[8]["min_gap"]
    monotone = all(res[k + 1]["min_gap"] <= res[k]["min_gap"] + 1e-12 for k in range(len(res) - 1))
    check = monotone and crr < single_gaps.min() / 100.0
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    x_half = math.sqrt(0.75); x_three = math.sqrt(12.0)
    return make_row("kin", f"The LQG area spectrum of a surface with exactly N punctures, A = 8 pi gamma sum_i sqrt(j_i (j_i + 1)), j_i in {{1/2, ..., {jmax:g}}}, gamma = {gamma:.4f} (the source's two-state all-j value), N = 1..12 enumerated; the source row set the fundamental quantum against CRR's estimated unit",
                    source="theory/retrodictions/loop_gravity.txt [2] (DESCR)",
                    Q=f"under A1' as written (the unit is the smallest change the system itself resolves, and the instrument's step is not the unit) a horizon's unit of area is the smallest spacing of its own total-area spectrum, not the area gap: at N = 2 punctures the spacing is {by_N[2]['min_gap']:.4f} l_P^2, 1/{a_gap / by_N[2]['min_gap']:.0f} of the gap, at N = 8 it is {by_N[8]['min_gap']:.2e} and at N = 12 {by_N[12]['min_gap']:.2e}, so rho = A/sigma of a many-puncture horizon is not its puncture count and D1's step on this carrier is not the domain's quantum",
                    ingredient="A1'/D1 (the unit as the smallest change the system itself resolves; rho = extent/unit, reported)",
                    null=f"the area gap A(1/2) = {a_gap:.4f} l_P^2 (the domain's 'quantum of area', the source row's and synthesis row 11's unit: the smallest eigenvalue, named)",
                    domain="Rovelli 1996 and Barreira-Carfora-Rovelli 1996 (named, not fetched): the area spectrum of a large surface is quasi-continuous, its spacings shrinking with the number of punctures, so a quantum black hole's emission spectrum is effectively continuous, against Bekenstein-Mukhanov 1995's equally spaced levels; the spectrum enumerated here is Rovelli-Smolin / Ashtekar-Lewandowski's",
                    numbers=f"single puncture: A(1/2) = {a_gap:.4f}, consecutive gaps {single_gaps[0]:.4f} .. {single_gaps[-1]:.4f} l_P^2 (asymptote 4 pi gamma = {asym:.4f}); exactly N punctures: " + "; ".join(f"N = {r['N']}: {r['n']} configurations, {r['n_distinct']} distinct eigenvalues on [{r['lo']:.2f}, {r['hi']:.2f}], smallest spacing {r['min_gap']:.3e}, mean spacing {r['mean_spacing']:.3e}" for r in res)
                            + f"; exact coincidences within one N: {sum(r['n'] - r['n_distinct'] for r in res)} (across N the spectrum has them: 4 sqrt(3/4) = {4 * x_half:.6f} = sqrt(12) = {x_three:.6f}); smallest spacing non-increasing in N: {monotone}",
                    tg=f"A1' unit at N = 8, the smallest spacing {crr:.3e} l_P^2, vs null (the area gap) {null:.4f}: {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the domain's own spectrum enumerated gives the same spacing {domain:.3e} at N = 8: {_word(rel(crr, domain) <= TOL_N, 'agree (the domain has Q: the quasi-continuity of the many-puncture spectrum is its 1996 result)', 'differ')}",
                    tc=f"smallest spacing non-increasing in N and below one hundredth of the smallest single-puncture gap by N = 8: {_hf(check)} (computed; not the deciding test, the label stops at T-N)",
                    out=out,
                    reading=f"read as written, A1' does not pick the quantum: the smallest change a horizon of N punctures resolves is the smallest spacing of its total-area spectrum, which is below the gap by a factor {a_gap / by_N[2]['min_gap']:.0f} already at N = 2 ({pair_txt}) and by {a_gap / by_N[12]['min_gap']:.0f} at N = 12, and the domain computed exactly this in 1996 to answer Bekenstein-Mukhanov: the many-puncture spectrum is quasi-continuous and the emission lines are dense. The source row's contrast stands (the domain's unit is fixed and CRR's is estimated), with the addition that the fixed unit the source and synthesis row 11 named, the gap, is a prereg's naming and not A1''s text; A1''s text reaches the domain's quasi-continuity theorem, so the label is {out}",
                    weakness=f"spins capped at j = {jmax:g} and N at 12 (the enumeration is combinatorial); the spacing is the arithmetic of a sum of square roots, and whether a horizon 'resolves' a change of {by_N[12]['min_gap']:.1e} l_P^2 is a question about transitions the kinematical spectrum does not answer; citations by name and year only, not fetched (R10)")


# ---------------------------------------------------------------- 123 [4] the arc clock through the bounce
def r3():
    rho_c = 0.41; k = math.sqrt(12 * math.pi); K = math.sqrt(24 * math.pi * rho_c)
    t = np.linspace(-20.0, 20.0, 40001); i0 = 20000
    a = (1 + 24 * math.pi * rho_c * t ** 2) ** (1.0 / 6.0); v = a ** 3                  # massless scalar, effective LQC, v_b = 1
    H = 8 * math.pi * rho_c * t / (1 + 24 * math.pi * rho_c * t ** 2)                     # H = a'/a in closed form
    p_phi = math.sqrt(2 * rho_c)                                                           # rho = p_phi^2 / (2 v^2) = rho_c at v_b = 1
    phi = np.arcsinh(K * t) / k; solution_err = float(np.max(np.abs(v - np.cosh(k * phi))))   # the source's v(phi) = cosh(sqrt(12 pi) phi)
    C_rate = 3.0 * np.abs(H); phi_rate = p_phi / v; v_rate = 3.0 * H * v
    dC_dphi = C_rate / phi_rate
    zeros = int(np.sum(dC_dphi < 1e-12)); t_max_phi = float(t[np.argmax(phi_rate)])
    lv = np.log(v); C_t = arc_length(lv)
    phig = np.linspace(float(phi[0]), float(phi[-1]), 40001); C_phi = arc_length(np.log(np.cosh(k * phig)))
    crr = float(C_rate[i0]); null = float(phi_rate[i0]); domain = float(abs(v_rate[i0]))
    grid_C = float(np.abs(np.gradient(lv, t))[i0]); grid_v = float(np.gradient(v, t)[i0])
    check = zeros == 1 and t_max_phi == 0.0 and crr == 0.0
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("cos", f"LQC with a massless scalar, effective dynamics, flat: a(t) = (1 + 24 pi rho_c t^2)^(1/6), v = a^3 (v_b = 1), rho_c = {rho_c:g}, p_phi = v_b sqrt(2 rho_c) = {p_phi:.4f}, phi(t) = asinh(sqrt(24 pi rho_c) t) / sqrt(12 pi), so v = cosh(sqrt(12 pi) phi) (the source row's exact solution; max |v - cosh(k phi)| = {solution_err:.1e}), t in [-20, 20] on 40001 points",
                    source="theory/retrodictions/loop_gravity.txt [4] (DESCR)",
                    Q="the arc of the volume carrier taken as the universe's own clock ('change has its own clock': O3's natural time from the system's own variable, A7's tense read off another of its variables) is a relational clock everywhere except at the bounce, where its rate against proper time, 3|H|, and against the scalar clock both vanish; LQC's scalar clock does the opposite, ticking fastest at the bounce (phi' = p_phi / v is maximal there), which is why the domain deparametrises with phi and not with the volume",
                    ingredient="O3 / H-L5's slogan (the D2 arc as the clock) and A7 (relational tense); D2 on ln v (not proper)",
                    null="the domain's clock: the massless scalar phi, a Dirac observable's parameter with p_phi conserved",
                    domain="Ashtekar-Pawlowski-Singh 2006 (named, not fetched): phi is the internal time because phi' = p_phi / V never vanishes; the volume is not a clock because v' = 0 at the bounce (a clock variable must be monotone with non-vanishing rate)",
                    numbers=f"at the bounce (t = 0): arc-clock rate dC/dt = 3|H| = {crr:.4f} (grid {grid_C:.4f}), scalar-clock rate dphi/dt = {null:.4f} (its maximum over the interval is at t = {t_max_phi:g}; at t = +/-20 it is {float(phi_rate[-1]):.5f}), volume rate dv/dt = {domain:.4f} (grid {grid_v:.4f}); dC/dphi at the bounce {float(dC_dphi[i0]):.4f}, at t = 20 {float(dC_dphi[-1]):.4f} (closed form sqrt(12 pi) = {k:.4f}, the source's constant); zeros of dC/dphi on the grid: {zeros}; maximum of dC/dt: {float(C_rate.max()):.4f}; the arc of ln v over the interval on the t grid {C_t:.5f}, on the phi grid {C_phi:.5f}, closed form 2 ln v(20) = {2 * math.log(float(v[-1])):.5f} (D2 is clock-invariant: geometry's)",
                    tg=f"arc-clock rate at the bounce {crr:.4f} vs null (scalar-clock rate at the bounce) {null:.4f}: {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the domain's reason for rejecting the volume as a clock, its rate at the bounce, is {domain:.4f}: {_word(rel(crr, domain) <= TOL_N, 'agree (the domain has Q: the arc clock inherits the zero the volume was rejected for)', 'differ')}",
                    tc=f"dC/dphi vanishes at exactly one point of the grid, the bounce, where dphi/dt is maximal: {_hf(check)} (computed; not the deciding test, the label stops at T-N)",
                    out=out,
                    reading=f"the arc clock is the volume clock with its turning point unfolded: C = |ln v - ln v_b| on each branch is monotone, so it passes the monotonicity test the volume fails, but its rate is |v'|/v and inherits the volume's zero at the bounce exactly, so as a relational clock it is degenerate at the one instant LQC was built to describe, and the domain's scalar clock is its mirror image, fastest there ({null:.4f}) and slowest far away ({float(phi_rate[-1]):.5f}); the source's constant speed {float(dC_dphi[-1]):.4f} far from the bounce is the exact solution's, as it said. 'Change has its own clock' is true of this universe and that clock stops at the bounce; CRR supplies the words and the domain the objection, so the label is {out}",
                    weakness="one exact solution (massless scalar, flat, effective dynamics); the volume is a chosen carrier with the identity metric on ln v (the source's rule 2), not a statistical family; an arc clock could be rescued by counting the bounce as a cut (A3) and restarting, which is a choice the row does not make; citations by name and year only, not fetched (R10)",
                    elegance="A clock that counts change stands still at the moment the universe turns around, because at that moment nothing is changing. One sentence, no knobs, and it explains why the physicists chose a different clock.",
                    child="Imagine measuring time not with a ticking clock but by how much the world changes: lots of change, lots of time. In this theory the universe shrinks, stops for an instant, and grows again. At that instant the size is not changing at all, so the change-clock freezes. The physicists use a field that keeps sliding even then, so their clock never stops; in fact it runs fastest right at the turn.")


# ---------------------------------------------------------------- 124 [5] Tolman cycles: H-L5 beyond the amplitude control
def _tolman_cycles(rho_c=0.41, E0=400.0, lam=0.02, dt=0.02, n_bounces=22):
    """Closed radiation universe with the effective LQC bounce: a'^2 = F(a, E) = (8 pi/3)(E/a^2 - E^2/(rho_c a^6)) - 1, with
    E = rho_r a^4 grown by Tolman's irreversibility as E' = lam E |H| (entropy S ~ E^(3/4)); integrated as
    a'' = F_a/2 + F_E E'/(2 a') with fixed-step RK4 from the first bounce (the root of F at E0)."""
    c = 8 * math.pi / 3

    def F(a, E): return c * (E / a ** 2 - E ** 2 / (rho_c * a ** 6)) - 1.0

    def Fa(a, E): return c * (-2 * E / a ** 3 + 6 * E ** 2 / (rho_c * a ** 7))

    def FE(a, E): return c * (1 / a ** 2 - 2 * E / (rho_c * a ** 6))

    def rhs(s):
        a, ad, E = s
        sg = 1.0 if ad > 0 else (-1.0 if ad < 0 else 0.0)
        return (ad, 0.5 * Fa(a, E) + 0.5 * FE(a, E) * lam * E * sg / a, lam * E * abs(ad) / a)

    a_rho = (E0 / rho_c) ** 0.25
    a0 = optimize.brentq(lambda x: F(x, E0), a_rho, 2 * a_rho, xtol=1e-14)
    s = (a0, 0.0, E0); t = 0.0; k = 0; prev_ad = 0.0
    la, times, ev, Es, cons = [], [], [], [], []
    while len(ev) < n_bounces:
        k1 = rhs(s); s2 = tuple(si + 0.5 * dt * ki for si, ki in zip(s, k1))
        k2 = rhs(s2); s3 = tuple(si + 0.5 * dt * ki for si, ki in zip(s, k2))
        k3 = rhs(s3); s4 = tuple(si + dt * ki for si, ki in zip(s, k3))
        k4 = rhs(s4)
        s = tuple(si + dt * (q1 + 2 * q2 + 2 * q3 + q4) / 6 for si, q1, q2, q3, q4 in zip(s, k1, k2, k3, k4))
        t += dt; k += 1
        la.append(math.log(s[0])); times.append(t)
        if prev_ad < 0 and s[1] >= 0:                                  # the bounce: the lower of the two samples straddling a' = 0
            ev.append(k - 1 if la[k - 1] <= la[k - 2] else k - 2); Es.append(s[2]); cons.append(F(s[0], s[2]) - s[1] ** 2)
        prev_ad = s[1]
    return np.array(la), np.array(times), np.array(ev), np.array(Es), np.array(cons), a0, a_rho, c


def r4():
    dt = 0.02; rho_c = 0.41; lam = 0.02; E0 = 400.0
    la, times, ev, Es, cons, a0, a_rho, c = _tolman_cycles(rho_c=rho_c, E0=E0, lam=lam, dt=dt, n_bounces=24)
    ev2 = ev[2:23]; Es2 = Es[2:23]                                        # bounces 3-23 scored; the series runs past the last scored bounce
    r = regularity(la, ev2, sigma=1.0, dt=dt, segment_end="inclusive", n_boot=2000)
    periods = np.diff(times[ev2]); a_b = np.exp(la[ev2])
    a_max = np.array([float(np.exp(la[i:j]).max()) for i, j in zip(ev2[:-1], ev2[1:])])
    arcs = np.array([arc_length(la[i:j + 1]) for i, j in zip(ev2[:-1], ev2[1:])]); amps = np.array([float(np.ptp(la[i:j + 1])) for i, j in zip(ev2[:-1], ev2[1:])])
    arc_minus = arcs - 2 * amps; growth_b = -np.log(a_b[1:] / a_b[:-1])
    E_growth = Es2[1:] / Es2[:-1]
    # the domain's closed forms: period 2 a_max, a_max = sqrt(c E), a_b = (E / rho_c)^(1/4) at the bounce values of E
    E_cyc = Es2[:-1]
    dom_arc = 2 * np.log(np.sqrt(c * E_cyc) / (E_cyc / rho_c) ** 0.25) - np.log((Es2[1:] / E_cyc) ** 0.25)
    cv_dom_arc = cv(dom_arc); cv_dom_clock = cv(2 * a_max)
    # control (iii): peak-detected boundaries (minima of ln a) and the antipodal cuts of its analytic-signal phase, against the bounces
    pk = peak_cuts(la, prominence=1.0, distance=100); minima = np.array([p for p in pk if la[p] <= la[max(p - 1, 0)] and la[p] <= la[min(p + 1, len(la) - 1)]])
    off_peak = max(int(np.min(np.abs(minima - e))) for e in ev2)
    near_min = np.array([int(minima[np.argmin(np.abs(minima - e))]) for e in ev2])
    cv_arc_peak = cv(np.array([arc_length(la[i:j + 1]) for i, j in zip(near_min[:-1], near_min[1:])]))
    ac = antipodal_cuts(intrinsic_phase(la))
    off_anti = np.array([float(np.min(np.abs(ac - e))) / float(ev2[k + 1] - ev2[k] if k + 1 < len(ev2) else ev2[k] - ev2[k - 1]) for k, e in enumerate(ev2)])
    margin = 0.01
    d_amp = r["cv_arc"] - r["cv_amp"]; d_clock = r["cv_arc"] - r["cv_clock"]
    arc_reg = r["ci95"][1] < 0.0 and d_clock < -margin
    beats_amp = r["ci95_amp"][1] < 0.0 and d_amp < -margin
    amp_tie = abs(d_amp) < margin and r["ci95_amp"][0] <= 0.0 <= r["ci95_amp"][1]
    crr = r["cv_arc"]; null = r["cv_amp"]; domain = cv_dom_arc
    out = outcome(crr=crr, null=null, domain=domain, check=arc_reg and beats_amp)
    return make_row("cos", f"Closed radiation universe with the effective LQC bounce, a'^2 = (8 pi/3)(E/a^2 - E^2/(rho_c a^6)) - 1, E = rho_r a^4 grown by Tolman's irreversibility as E' = lambda E |H| (entropy S ~ E^(3/4)), rho_c = {rho_c:g}, E_0 = {E0:g}, lambda = {lam:g}, fixed-step RK4 dt = {dt:g} from the first bounce (a_b = {a0:.4f}, against (E_0/rho_c)^(1/4) = {a_rho:.4f}), {len(ev)} bounces integrated, bounces 3-{len(ev2) + 2} scored ({r['n']} cycles); the bounce as the system's own event and cut; carrier ln a with the identity metric (the source's)",
                    source="theory/retrodictions/loop_gravity.txt [5] (DESCR)",
                    Q="the Tolman cycles are in H-L5's arc-regular class beyond the amplitude control: the log-arc of a bounce-to-bounce cycle is more regular than its period and more regular than its log-amplitude ln(a_max / a_b)",
                    ingredient="H-L5 (the class claim beyond its controls (i) amplitude, (ii) metric, (iii) peak-detected boundaries), D5 (occasion = bounce to bounce), A3 [M] (the bounce as the own event), D2 on ln a (identity metric)",
                    null="H-L5's control (i): the log-amplitude of the cycle, ln(a_max / a_b)",
                    domain="Tolman 1934 (named, not fetched): entropy production makes successive cycles larger and longer; a closed radiation universe has a(eta) = a_max sin(eta), t = a_max (1 - cos eta), so its period is 2 a_max, and its turning points are a_max = sqrt(8 pi E / 3), a_b = (E / rho_c)^(1/4) (up to the curvature term): the arc 2 ln(a_max / a_b) and the period follow from the entropy sequence alone",
                    numbers=f"{r['n']} cycles: CV(arc) = {r['cv_arc']:.4f}, CV(clock) = {r['cv_clock']:.4f}, CV(amplitude) = {r['cv_amp']:.4f}, C_mean = {r['C_mean']:.4f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) = [{r['ci95'][0]:.4f}, {r['ci95'][1]:.4f}], of CV(arc) - CV(amplitude) = [{r['ci95_amp'][0]:.1e}, {r['ci95_amp'][1]:.1e}]; arc - 2 amplitude per cycle: mean {float(arc_minus.mean()):+.4f} (min {float(arc_minus.min()):+.4f}, max {float(arc_minus.max()):+.4f}), against -ln(a_b,n+1 / a_b,n): max |difference| {float(np.max(np.abs(arc_minus - growth_b))):.1e}; E growth per cycle {float(E_growth[0]):.4f} -> {float(E_growth[-1]):.4f} (S ~ E^(3/4): {float(E_growth[0]) ** 0.75:.4f} -> {float(E_growth[-1]) ** 0.75:.4f}); period / a_max: {float((periods / a_max).min()):.4f} .. {float((periods / a_max).max()):.4f} (closed form 2); a_max {a_max[0]:.2f} -> {a_max[-1]:.2f}, a_b {a_b[0]:.4f} -> {a_b[-1]:.4f}, periods {periods[0]:.2f} -> {periods[-1]:.2f}; domain's closed-form sequences: CV(arc) = {cv_dom_arc:.4f}, CV(period = 2 a_max) = {cv_dom_clock:.4f}; control (iii): the minima found by peak_cuts (prominence 1, distance 100) sit within {off_peak} samples of the bounces and the arc between consecutive peak-detected minima has CV {cv_arc_peak:.4f}; the antipodal cuts of the analytic-signal phase of ln a: {len(ac)} cuts against {len(ev2)} bounces, nearest cut {float(off_anti.min()):.3f} .. {float(off_anti.max()):.3f} periods from a bounce (the phase of a trace with a growing period and a rising trend; a diagnostic, never scored); control (ii): no statistical metric on this carrier (identity only); Friedmann constraint residual at the bounces {float(np.abs(cons[2:]).max()):.1e}",
                    tg=f"CV(arc) {crr:.4f} vs null CV(log-amplitude) {null:.4f}: {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Tolman's sequences give CV(arc) = {domain:.4f} for the same target: {_word(rel(crr, domain) <= TOL_N, 'agree', 'differ')}; and CV(period) = {cv_dom_clock:.4f} against the integrated {r['cv_clock']:.4f}: {_word(rel(cv_dom_clock, r['cv_clock']) <= TOL_N, 'agree', 'differ')}",
                    tc=f"arc-regular (CI of CV(arc) - CV(clock) below 0 and the difference beyond the {margin:g} margin): {_hf(arc_reg)}; arc beats the amplitude control (CI below 0 and beyond the margin): {_hf(beats_amp)} (tie within the margin with the CI including 0: {amp_tie})",
                    out=out,
                    reading=f"geometry, as batches 11, 13 and 18 read the neuron, the adder and the geyser: a bounce-to-bounce cycle on the log carrier is two monotone branches, so its arc is twice its log-amplitude less the growth of the bounce volume (arc - 2 amp = -ln(a_b,n+1 / a_b,n) to {float(np.max(np.abs(arc_minus - growth_b))):.1e}), and the amplitude control is the arc to within CV {abs(d_amp):.1e}; the class is arc-regular (CV {r['cv_arc']:.4f} against {r['cv_clock']:.4f}, CI below 0: {r['ci95'][1] < 0.0}) and it is the log of a growing sequence against the sequence itself, as the source row said, with the clock side the domain's closed-universe period 2 a_max (period / a_max = {float((periods / a_max).mean()):.4f}); the own event is an extremum, so control (iii) with the minima is the own-event cut (CV {cv_arc_peak:.4f}) and H-CUT has nothing to test on it; synthesis row 9 read A6 on these cycles (WRONG) and this row adds nothing beyond H-L5's controls: the label is {out}",
                    weakness=f"lambda is a knob (E grows by {float(E_growth[0]):.4f} .. {float(E_growth[-1]):.4f} per cycle at lambda = {lam:g}) and the growth is injected through |H| (a toy of Tolman's irreversibility); the bounce regularisation is the simplest effective-LQC form, not the closed-model one (Ashtekar-Pawlowski-Singh-Vandersloot 2007, named, not fetched); the identity metric on ln a is the source's stand-in; the sign term makes the RK4 error grow (constraint residual printed); citations by name and year only (R10)",
                    elegance="Measure a universe's cycle in doublings and every cycle is nearly the same; measure it in years and each one is longer than the last. But the doublings are just the height of the bounce, so the steadiness belongs to the size, not to the clock.",
                    child="Suppose the universe grows, shrinks, bounces and grows again, and each time it grows a little bigger than before. Counted in years, each round trip takes longer. Counted in 'how many times did it double', each round trip is almost the same. That sounds like a magic clock, but it only says the bounce grows slowly, a little bigger each time.")


# ---------------------------------------------------------------- 125 [6] spin-j coherent states: the three readings of A3 at higher j
def _jmats(j):
    m = np.arange(j, -j - 1, -1); n = len(m)
    Jp = np.zeros((n, n))
    for i in range(1, n):
        Jp[i - 1, i] = math.sqrt(j * (j + 1) - m[i] * (m[i] + 1))
    Jy = (Jp - Jp.T) / 2j
    return Jy, np.diag(m)


def _spin_readings(j, n_grid=40001):
    Jy, Jz = _jmats(j); psi0 = np.zeros(int(2 * j + 1), complex); psi0[0] = 1.0
    qfi = float(4 * (psi0.conj() @ Jy @ Jy @ psi0 - (psi0.conj() @ Jy @ psi0) ** 2).real)      # 4 Var(J_y): the metric of the rotation
    ov = lambda th: float(abs(psi0.conj() @ expm(-1j * th * Jy) @ psi0))
    dth = 1e-4; rate = 2.0 * math.acos(min(1.0, ov(dth))) / dth                                   # local arc rate from the chord (orthogonal = pi)
    th_arc = math.pi / math.sqrt(qfi)                                                              # arc sqrt(qfi) theta reaches pi
    # the antipode: the coherent state is the symmetric product of 2j copies of one qubit (the domain's structure), so its
    # overlap is the qubit amplitude to the power 2j; the qubit amplitude crosses zero linearly and its root is sharp, where
    # the (2j+1)-dimensional overlap's minimum is flat below machine precision for large j
    Jy1, _ = _jmats(0.5); up = np.array([1.0, 0.0], complex)
    amp1 = lambda th: complex(up.conj() @ expm(-1j * th * Jy1) @ up)
    ths = np.linspace(0.0, 2 * math.pi, 2000)                                                     # pi is not a grid point
    product_err = float(max(abs(ov(th) - abs(amp1(th)) ** (2 * j)) for th in ths))
    imag_err = float(max(abs(amp1(th).imag) for th in ths))
    re1 = np.array([amp1(th).real for th in ths]); i = int(np.argmax(re1 <= 0.0))                  # first non-positive amplitude
    th_perp = float(optimize.brentq(lambda th: amp1(th).real, ths[i - 1], ths[i], xtol=1e-14))
    t = np.linspace(0.0, 4 * math.pi, n_grid); cuts = antipodal_cuts(intrinsic_phase(j * np.cos(t)))
    th_rot = float(t[cuts[1]])
    return dict(j=j, qfi=qfi, rate=rate, th_arc=th_arc, ov_arc=ov(th_arc), th_perp=th_perp, ov_perp=ov(th_perp), th_rot=th_rot,
                arc_perp=math.sqrt(qfi) * th_perp, th_mt=math.pi / (2 * math.sqrt(qfi / 4)), product_err=product_err, imag_err=imag_err)


def r5():
    res = [_spin_readings(j) for j in (0.5, 1.0, 2.0, 5.0, 20.0)]
    agree = {q["j"]: (rel(q["th_arc"], q["th_perp"]) <= TOL_G and rel(q["th_rot"], q["th_perp"]) <= TOL_G) for q in res}
    rot_perp = {q["j"]: rel(q["th_rot"], q["th_perp"]) <= TOL_G for q in res}
    mt_arc = {q["j"]: rel(q["th_mt"], q["th_arc"]) <= TOL_N for q in res}
    internal = not all(agree.values()); out = outcome(internal=internal)
    n_agree = sum(agree.values()); n_rot = sum(rot_perp.values()); n_mt = sum(mt_arc.values())
    lim = math.exp(-math.pi ** 2 / 8)
    dt_grid = 4 * math.pi / 40000
    numbers = "; ".join(
        f"j = {q['j']:g}: QFI = {q['qfi']:.4f} (local arc rate from the chord {q['rate']:.4f}, sqrt(2j) = {math.sqrt(2 * q['j']):.4f}), rotor reading theta = {q['th_rot']:.4f}, arc reading theta = {q['th_arc']:.4f} (overlap with the start there {q['ov_arc']:.4f}), "
        + f"antipode (first zero of the qubit amplitude) theta = {q['th_perp']:.4f} (full-matrix overlap there {q['ov_perp']:.1e}, arc there {q['arc_perp']:.4f}, surplus at the antipode {q['arc_perp'] - math.pi:.4f}; product structure |<j,j|theta>| = |<up|theta>|^(2j) holds on the grid to {q['product_err']:.1e}, qubit amplitude real to {q['imag_err']:.1e})"
        + f", Mandelstam-Tamm angle pi/(2 Delta J_y) = {q['th_mt']:.4f}" for q in res) + f"; limit of the overlap at the arc reading as j -> infinity, e^(-pi^2/8) = {lim:.4f}; pi = {math.pi:.4f}"
    tg = "; ".join(f"j = {q['j']:g}: rotor {q['th_rot']:.4f} / arc {q['th_arc']:.4f} / antipode {q['th_perp']:.4f}: {_word(agree[q['j']], 'agree', 'differ')}" for q in res) + f"; the three readings agree at {n_agree} of {len(res)} spins, the rotor and antipode readings at {n_rot} of {len(res)}"
    return make_row("kin", "Spin-j coherent state |j, j> rotated about a perpendicular axis, |theta> = e^(-i theta J_y) |j, j>, on the projective carrier with the quantum Fisher (Fubini-Study) metric normalised to orthogonality = pi (batch 05 row 3's convention), j in {1/2, 1, 2, 5, 20}, matrices built and exponentiated; the source row's carrier (the building block of coherent intertwiners)",
                    source="theory/retrodictions/loop_gravity.txt [6] (DESCR)",
                    Q="for every spin the A3 cut of the rotation is the antipodal coherent state |j, -j> at theta = pi (the source row's 'the antipode exists for every j and is reached at theta = pi')",
                    ingredient="A3 in its three readings on this carrier: (i) the rotor reading, the axiom's text - the intrinsic phase of <J_z> = j cos(theta) advances half a turn (antipodal_cuts); (ii) the arc reading - the Fisher arc sqrt(2j) theta reaches pi, half the closed geodesic; (iii) the antipode reading - the first orthogonal state",
                    null="the domain's own events: the orthogonality angle of the rotated coherent state and the Mandelstam-Tamm angle pi/(2 Delta J_y)",
                    domain="Radcliffe 1971 / Perelomov 1972 (named, not fetched): |<j, j | theta>| = cos^(2j)(theta/2), zero only at theta = pi; Mandelstam-Tamm / Anandan-Aharonov 1990: orthogonality needs theta >= pi/(2 Delta J_y), attained iff the path is a Fubini-Study geodesic, which the rotation of |j, j> is only for j = 1/2 (the Bloch great circle)",
                    numbers=numbers, tg=tg,
                    tn=f"the Mandelstam-Tamm angle equals the arc reading at {n_mt} of {len(res)} spins and the orthogonality angle pi equals the rotor and antipode readings at {n_rot} of {len(res)}: each reading is a domain number, and the domain's statement that they coincide only on a geodesic (j = 1/2) is the disagreement between them",
                    tc="not reached: the readings must agree before Q can be checked, and they agree only at j = 1/2",
                    out=out,
                    reading=f"the higher spins do not resolve batch 05 row 3's INTERNAL, they invert it: on the qubit off the equator the antipode never occurred and the arc reading fired late; on the spin-j rotation the antipode always occurs (the qubit amplitude's zero, at theta = {min(q['th_perp'] for q in res):.4f} .. {max(q['th_perp'] for q in res):.4f}), the rotor and antipode readings coincide there ({n_rot} of {len(res)}), and the arc reading fires early, at pi/sqrt(2j) (theta = {res[1]['th_arc']:.4f} at j = 1, {res[-1]['th_arc']:.4f} at j = 20), where the state still overlaps its start by {res[1]['ov_arc']:.4f} .. {res[-1]['ov_arc']:.4f} (limit {lim:.4f}): as j grows the arc reading cuts after the first distinguishable state and the antipode after sqrt(2j) of them (arc at the antipode {res[-1]['arc_perp']:.4f} at j = 20, surplus {res[-1]['arc_perp'] - math.pi:.4f}), so the two readings diverge as sqrt(2j) and the 'more classical' spins make the choice of reading matter more, not less; whichever reading v3.2 fixes, its number is the domain's (the QFI, the Mandelstam-Tamm angle, the orthogonality angle), and the label is {out}",
                    weakness=f"one rotation axis (perpendicular to the spin; a rotation about z leaves the state fixed and no reading fires) and five spins; the rotor trace <J_z> is one choice of intrinsic phase (R5), and antipodal_cuts returns the sample nearest the interpolated crossing (grid step {dt_grid:.1e}); which reading is A3 on a projective carrier is a theory decision (v3.2), not this row's; citations by name and year only, not fetched (R10)",
                    elegance="A big spinning top turned by a small angle already looks nothing like it did, but it takes a half-turn to point the opposite way; only the smallest spin has 'looks different' and 'points opposite' at the same angle. A picture of why 'halfway' needs a rule before it can be a rule.",
                    child="Turn a small compass needle and it takes a full half-turn before it points the opposite way, and only then does it look truly different. A big heavy top is different: turn it just a little and it already looks like a new top, but it still needs the whole half-turn to point the other way. So 'when has it changed enough to count?' has two answers for the big top, and the theory has not yet said which one it means.")


def main():
    return run_batch("Synthesis batch 25: rows 121-125 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
