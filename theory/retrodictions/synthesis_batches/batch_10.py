"""Synthesis batch 10: rows 46-50 of QUEUE.md (prompt-log entry 61). All five source rows are in
theory/retrodictions/sharp_claims.txt (external SHARP claims re-derived and regraded). [5] Fermi-Dirac occupation,
'f(E = mu) = 1/2, the chemical potential is the antipode' (DESCR); [7] Langmuir adsorption, 'theta = 1/2 at P = 1/K'
(DESCR); [8] qubit precession, 'the cut time reproduces the Mandelstam-Tamm limit' (CONSIST), re-read on the one
version of the qubit that has events of its own (resonance fluorescence: quantum jumps); [10] two-flavour neutrino
oscillation, 'the flavour state reaches its antipode iff mixing is maximal' (CONSIST), re-read in matter (MSW);
[11] finite-time thermodynamics, 'minimum dissipation is the constant-Fisher-speed protocol; S^2 bounds excess
dissipation' (CONSIST), re-read on the trap with both parameters driven (batch 02 row 2 did the stiffness alone).
Models re-implemented here (nothing imported from the battery scripts). Deterministic; no data file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_10.py
"""
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, minimize, minimize_scalar

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase, peak_cuts
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/sharp_claims.txt"


def _agree(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def _holds(flag):
    return "holds" if flag else "fails"


def _fs_arc(st):
    """Fubini-Study arc of a sampled pure-state path (rows of `st` normalised), orthogonality at pi/2 (the batch 01
    convention). Step = asin of the norm of the component of psi_{i+1} orthogonal to psi_i: no cancellation for small
    steps (arccos of the overlap loses sqrt(eps) per step)."""
    ov = np.sum(np.conj(st[:-1]) * st[1:], axis=1)
    perp = st[1:] - st[:-1] * ov[:, None]
    return np.concatenate([[0.0], np.cumsum(np.arcsin(np.clip(np.linalg.norm(perp, axis=1), 0.0, 1.0)))])


# ---------------------------------------------------------------- 46 [5] Fermi-Dirac occupation: the antipode on three carriers
def r1():
    Ts = (0.1, 1.0, 10.0)
    f = lambda E, T: 1.0 / (math.exp(E / T) + 1.0)                            # E measured from mu
    arc_fd = []                                                              # D2 on the Bernoulli carrier: g_EE = f(1-f)/T^2, arc from the empty pole (E -> +inf) to E = mu
    for T in Ts:
        arc_fd.append(quad(lambda E: math.sqrt(f(E, T) * (1.0 - f(E, T))) / T, 0.0, 60.0 * T, limit=200)[0])
    closed = 2.0 * math.asin(math.sqrt(0.5))                                 # the arcsine distance from p = 0 to p = 1/2 (information geometry)
    total = 2.0 * math.asin(1.0)                                             # the Bernoulli family's whole length
    # Bose-Einstein: per-mode number distribution is geometric, P(n) = (1-x) x^n, x = e^{-(E-mu)/T}; Fisher I(x) = 1/(x(1-x)^2)
    arc_be = lambda x: quad(lambda y: 1.0 / (math.sqrt(y) * (1.0 - y)), 0.0, x, limit=200)[0]
    be_pts = [(dE, arc_be(math.exp(-dE))) for dE in (1.0, 0.1, 0.01)]        # E - mu in units of T, approaching mu
    x_half = 1.0 / 3.0                                                       # BE occupation x/(1-x) = 1/2 at x = 1/3, i.e. E - mu = T ln 3 (the source's probe)
    arc_be_half = arc_be(x_half)
    # Maxwell-Boltzmann: per-mode number is Poisson with mean n = e^{-(E-mu)/T}; arc from n = 0 is 2 sqrt(n)
    arc_mb_mu = 2.0 * math.sqrt(1.0); arc_mb_far = 2.0 * math.sqrt(math.exp(5.0))
    crr = arc_fd[1]
    check = all(abs(a - closed) < 1e-9 for a in arc_fd)
    out = outcome(crr=crr, null=closed, domain=closed, check=check)
    return make_row("stat", "Fermi-Dirac occupation f(E) = 1/(e^((E - mu)/T) + 1) on its Bernoulli carrier (one mode: occupied or empty), beside the Bose-Einstein (geometric) and Maxwell-Boltzmann (Poisson) occupation carriers, E measured from mu",
                    source=f"{SRC} [5] (DESCR)",
                    Q="the chemical potential is the midpoint of the occupancy arc: the Fisher-Rao arc from the empty mode (E -> +inf) to E = mu is pi/2, half the carrier's whole length pi, at every temperature; on the Bose-Einstein carrier the arc to mu diverges and on the Maxwell-Boltzmann carrier the family has one pole, so neither has an antipode",
                    ingredient="D2 (arc), D3 (chord) on the Bernoulli carrier - NOT CRR-proper: information geometry's; no CRR-proper ingredient could be attached to the source row (see weakness)",
                    null="the arcsine distance 2 asin sqrt(1/2) - 0, information geometry's closed form (identical by construction)",
                    domain="particle-hole symmetry of the Fermi function, f(mu + x) = 1 - f(mu - x), which places f = 1/2 at E = mu; the arcsine (Bhattacharyya) distance on the Bernoulli family",
                    numbers=f"arc from the empty pole to E = mu at T = {Ts[0]:g}, {Ts[1]:g}, {Ts[2]:g}: {arc_fd[0]:.6f}, {arc_fd[1]:.6f}, {arc_fd[2]:.6f} (closed form 2 asin sqrt(1/2) = {closed:.6f}; whole family pi = {total:.6f}); Bose-Einstein arc from the empty pole to E - mu = T, 0.1 T, 0.01 T: {be_pts[0][1]:.4f}, {be_pts[1][1]:.4f}, {be_pts[2][1]:.4f} (logarithmic divergence at mu; the source's n = 1/2 point, E - mu = T ln 3 = {math.log(3):.4f} T, sits at arc {arc_be_half:.4f} of an infinite family); Maxwell-Boltzmann arc from the empty pole to E = mu: {arc_mb_mu:.4f}, to E = mu - 5 T: {arc_mb_far:.4f} (unbounded, one pole)",
                    tg=f"arc to mu {crr:.6f} vs null (arcsine closed form) {closed:.6f}: {_agree(crr, closed)} (no CRR-proper ingredient in Q)",
                    tn=f"the domain's symmetry and the arcsine distance give {closed:.6f}: {_agree(crr, closed, TOL_N)} - the domain has Q",
                    tc=f"|arc - pi/2| < 1e-9 at all three temperatures: {_holds(check)}" + (" (true, and it is the Bernoulli family's geometry, which depends on f alone)" if check else ""),
                    out=out,
                    reading=f"the source row's content is D2 on the Bernoulli carrier: the antipode is the midpoint of a compact family and f = 1/2 is its midpoint whatever the curve, so mu is the antipode because the Fermi function is the one occupation statistic that puts f = 1/2 at mu (its particle-hole symmetry); temperature only stretches the energy extent of the half-turn (D1's rho, which CRR does not predict); the other two carriers show what 'antipode' needs, a second pole, and neither has one: {out} by construction, as batch 01 row 1",
                    weakness="CRR-proper ingredients tried and dropped: A3/D5 - the occupancy is monotone in E, no rotor (O3), and on the temperature line at fixed E the antipode is T = inf, batch 02 row 1's reading; A1'/D1 with one particle per mode as the unit on N modes - rho = sqrt(N) x pi/2 is Fisher additivity (batch 01 row 2, the Cramer-Rao count), and D1 says CRR does not predict rho; A6, P2/P3 - no occasions; H-L5 - the source model has no events of its own")


# ---------------------------------------------------------------- 47 [7] Langmuir adsorption: the same content under a change of coordinate
def r2():
    Ks = (0.5, 2.0, 20.0)                                                    # the source's K = 2 and two others
    theta = lambda P, K: K * P / (1.0 + K * P)
    arcs = []                                                                # D2 in ln P: g = theta(1-theta) since d theta / d ln P = theta (1 - theta); arc from P = 0 to P = 1/K
    for K in Ks:
        arcs.append(quad(lambda u: math.sqrt(theta(math.exp(u), K) * (1.0 - theta(math.exp(u), K))), -60.0, -math.log(K), limit=200)[0])
    closed = 2.0 * math.asin(math.sqrt(0.5))
    # the isotherm IS the Fermi function under x = -ln(KP) <-> (E - mu)/T
    Ps = np.logspace(-4, 4, 2001); fd = 1.0 / (np.exp(-np.log(2.0 * Ps)) + 1.0); gap = float(np.abs(theta(Ps, 2.0) - fd).max())
    # asymmetric members (Toth): theta = KP / (1 + (KP)^t)^(1/t); theta(P = 1/K) = 2^(-1/t); antipode theta = 1/2 at KP = (2^t - 1)^(-1/t)
    toth = {t: (2.0 ** (-1.0 / t), (2.0 ** t - 1.0) ** (-1.0 / t)) for t in (0.5, 2.0)}
    toth_theta_half = {t: kp / (1.0 + kp ** t) ** (1.0 / t) for t, (_, kp) in toth.items()}   # theta at that pressure (must be 1/2)
    toth_arc = {}
    for t, (_, kp_half) in toth.items():                                    # arc from P = 0 to the antipode on each member
        th_t = lambda u, t=t: math.exp(u) / (1.0 + math.exp(t * u)) ** (1.0 / t)
        dth = lambda u, t=t, h=1e-6: (th_t(u + h) - th_t(u - h)) / (2 * h)
        toth_arc[t] = quad(lambda u: abs(dth(u)) / math.sqrt(th_t(u) * (1.0 - th_t(u))), -60.0, math.log(kp_half), limit=200)[0]
    # BET: coverage in monolayers, unbounded as x = P/P0 -> 1; on a Poisson carrier (mean layers) the arc from x = 0 is 2 sqrt(theta_BET)
    c = 100.0; bet = lambda x: c * x / ((1.0 - x) * (1.0 + (c - 1.0) * x))
    bet_pts = [(x, 2.0 * math.sqrt(bet(x))) for x in (0.5, 0.9, 0.99)]
    crr = arcs[1]
    check = all(abs(a - closed) < 1e-9 for a in arcs) and all(abs(v - closed) < 1e-6 for v in toth_arc.values()) and all(abs(v - 0.5) < 1e-12 for v in toth_theta_half.values())
    out = outcome(crr=crr, null=closed, domain=closed, check=check)
    return make_row("chem", f"Langmuir adsorption theta = KP/(1 + KP) on its Bernoulli carrier (one site: occupied or empty), K = {Ks[1]:g} as in the source, with the Toth asymmetric members and the BET isotherm as probes",
                    source=f"{SRC} [7] (DESCR)",
                    Q="theta = 1/2 is the midpoint of the coverage arc on every member of the isotherm family (arc pi/2 from the bare surface), and P = 1/K is where the Langmuir member, and only it, reaches that midpoint: the Langmuir isotherm is the Fermi function under ln(KP) <-> -(E - mu)/T",
                    ingredient="D2 (arc), D3 (chord) on the Bernoulli carrier - NOT CRR-proper: information geometry's; no CRR-proper ingredient could be attached (see weakness)",
                    null="the arcsine distance 2 asin sqrt(theta) from theta = 0, information geometry's closed form (identical by construction)",
                    domain="K is defined by the half-coverage pressure (the source's DESCR); the Langmuir isotherm is the grand-canonical lattice gas, theta = 1/(1 + e^((eps - mu)/T)) with e^(mu/T) proportional to P (the Fermi function)",
                    numbers=f"arc from P = 0 to P = 1/K at K = {Ks[0]:g}, {Ks[1]:g}, {Ks[2]:g}: {arcs[0]:.6f}, {arcs[1]:.6f}, {arcs[2]:.6f} (closed form {closed:.6f}: the pressure moves with K, the arc does not); max |theta_Langmuir(P) - f_FD(-ln 2P)| over P in [1e-4, 1e4]: {gap:.1e}; Toth t = 0.5: theta(1/K) = {toth[0.5][0]:.4f}, antipode theta = 1/2 at KP = {toth[0.5][1]:.4f} (theta there {toth_theta_half[0.5]:.6f}), arc to it {toth_arc[0.5]:.6f}; Toth t = 2: theta(1/K) = {toth[2.0][0]:.4f}, antipode at KP = {toth[2.0][1]:.4f} (theta there {toth_theta_half[2.0]:.6f}), arc to it {toth_arc[2.0]:.6f}; BET (c = {c:g}) on a Poisson carrier: arc at P/P0 = {bet_pts[0][0]:g}, {bet_pts[1][0]:g}, {bet_pts[2][0]:g}: {bet_pts[0][1]:.3f}, {bet_pts[1][1]:.3f}, {bet_pts[2][1]:.3f} (unbounded, one pole)",
                    tg=f"arc to P = 1/K {crr:.6f} vs null (arcsine closed form) {closed:.6f}: {_agree(crr, closed)} (no CRR-proper ingredient in Q)",
                    tn=f"the domain's definition of K and the arcsine distance give {closed:.6f}: {_agree(crr, closed, TOL_N)} - the domain has Q",
                    tc=f"arc to the antipode = pi/2 on the Langmuir member at three K and on both Toth members: {_holds(check)}" + (" (true, and it is the Bernoulli family's geometry, which depends on theta alone)" if check else ""),
                    out=out,
                    reading=f"row 1 again under a change of coordinate: the antipode is theta = 1/2 on every isotherm because the carrier is compact and the arc depends on theta alone, and 'at P = 1/K' is the Langmuir member's definition of K (the Toth members put theta(1/K) at {toth[0.5][0]:.4f} and {toth[2.0][0]:.4f} while their antipodes stay at theta = 1/2 and move to other pressures); the BET carrier has one pole and no antipode: {out} by construction",
                    weakness="CRR-proper ingredients tried and dropped: A3/D5 - Langmuir kinetics d theta/dt = k_a P (1 - theta) - k_d theta is a monotone relaxation, no rotor (O3), and its arc is the arcsine distance of batch 01 row 1; A1'/D1 with one site as the unit on N sites - the Cramer-Rao count of batch 01 row 2; D6/H-T1 on a pressure-swing cycle - Salamon-Berry's path-length bound (batch 06 row 1) with a coverage-dependent relaxation time (batch 02 row 2), not attempted; A6, P2/P3 - no occasions")


# ---------------------------------------------------------------- 48 [8] the qubit with events of its own: resonance fluorescence
def _nojump(Om, Gam, n=200001):
    """Conditional (no-jump) evolution of a resonantly driven two-level atom from |g> under H_eff = (Om/2) sigma_x - i (Gam/2) |e><e|
    (quantum-jump unravelling: each emission resets the state to |g>, the system's own event). Grid of n points over a window
    long enough for the waiting-time density to be exhausted. Returns the grid, the density w(t) = Gam |<e|psi~(t)>|^2, and the
    per-occasion statistics as functions of the waiting time T: Fisher arc C(T), amplitude A(T) = max p_e (control i), total
    variation of p_e (control ii on the population trace), Euclidean arc of the Bloch vector (control ii on the state)."""
    tmax = 60.0 * (2.0 / Gam + Gam / Om ** 2)
    t = np.linspace(0.0, tmax, n)
    Heff = np.array([[0.0, Om / 2], [Om / 2, -1j * Gam / 2]])
    w, V = np.linalg.eig(-1j * Heff); coef = np.linalg.solve(V, np.array([1.0, 0.0], complex))
    st = (V @ (np.exp(np.outer(w, t)) * coef[:, None])).T                    # unnormalised psi~(t)
    nrm2 = (np.abs(st) ** 2).sum(axis=1); wt = Gam * np.abs(st[:, 1]) ** 2
    psi = st / np.sqrt(nrm2)[:, None]
    C = _fs_arc(psi)
    pe = np.abs(psi[:, 1]) ** 2; A = np.maximum.accumulate(pe)
    TV = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(pe)))])
    bloch = np.column_stack([2 * (np.conj(psi[:, 0]) * psi[:, 1]).real, 2 * (np.conj(psi[:, 0]) * psi[:, 1]).imag, 1 - 2 * pe])
    EU = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(bloch, axis=0), axis=1))])
    return dict(t=t, wt=wt, C=C, A=A, TV=TV, EU=EU, pe=pe, Z=float(np.trapezoid(wt, t)))


def _quad_stats(d):
    t, wt = d["t"], d["wt"]; Z = d["Z"]
    mean = lambda f: float(np.trapezoid(wt * f, t) / Z)
    def cvq(f):
        m = mean(f); return math.sqrt(mean((f - m) ** 2)) / abs(m)
    return dict(Z=Z, cvT=cvq(t), cvC=cvq(d["C"]), cvA=cvq(d["A"]), cvTV=cvq(d["TV"]), cvEU=cvq(d["EU"]),
                meanT=mean(t), meanC=mean(d["C"]), Cinf=float(d["C"][-1]), Ainf=float(d["A"][-1]))


def _label(s):
    if rel(s["cvC"], s["cvT"]) <= TOL_G:
        return "arc = clock"
    if s["cvC"] < s["cvT"] and s["cvC"] < s["cvA"]:
        return "arc-regular"
    if s["cvC"] < s["cvT"]:
        return "arc < clock but amplitude wins"
    return "clock-regular"


def r3():
    Om, Gam = 1.3, 1.0                                                       # the source's Omega; Gamma = 1 sets the unit of rate
    ratios = (0.1, 0.25, 0.5, 0.65, 0.8, 1.0, 1.3, 2.6, 10.0)
    tab = {r: _quad_stats(_nojump(Om, Om / r)) for r in ratios}
    labels = {r: _label(s) for r, s in tab.items()}
    dec = tab[Om / Gam]
    cross = brentq(lambda r: (lambda s: s["cvC"] - s["cvT"])(_quad_stats(_nojump(Om, Om / r))), 0.65, 1.3, xtol=1e-4)
    # the no-jump fixed point below the exceptional point Om = Gam/2: the conditional angle obeys phi' = Om/2 - (Gam/4) sin 2 phi
    fp = {r: (math.asin(2 * r) / 2 if r < 0.5 else None) for r in ratios}
    d_weak = _nojump(Om, Om / 0.25); merid = float(np.abs(d_weak["A"] - np.sin(d_weak["C"]) ** 2).max())     # A = sin^2 C on the meridian
    # a seeded emission record at the decisive point: waiting times by inverse CDF of w(t), paired bootstrap on CV(C) - CV(T)
    d = _nojump(Om, Gam); t, wt = d["t"], d["wt"]
    cdf = np.concatenate([[0.0], np.cumsum(0.5 * (wt[1:] + wt[:-1]) * np.diff(t))]); cdf /= cdf[-1]
    rng = np.random.default_rng(0); n_rec = 20000; T = np.interp(rng.random(n_rec), cdf, t)
    Cs, As = np.interp(T, t, d["C"]), np.interp(T, t, d["A"])
    diffs = []
    for _ in range(2000):
        idx = rng.integers(0, n_rec, n_rec); diffs.append(cv(Cs[idx]) - cv(T[idx]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    eu_ratio = float(np.mean(d["EU"][1:] / d["C"][1:]))
    n_arc = sum(1 for v in labels.values() if v == "arc-regular"); n_clock = sum(1 for v in labels.values() if v == "clock-regular")
    n_tie = sum(1 for v in labels.values() if v == "arc = clock")
    check = all(v == "arc-regular" for v in labels.values())
    out = outcome(crr=dec["cvC"], null=dec["cvT"], domain=None, check=check)
    rows_txt = "; ".join(f"Om/Gam = {r:g}: CV(T) {s['cvT']:.4f}, CV(C) {s['cvC']:.4f}, CV(A) {s['cvA']:.4f}, CV(TV p_e) {s['cvTV']:.4f} -> {labels[r]}" for r, s in tab.items())
    return make_row("qm", f"Resonance fluorescence of the source's qubit: resonant Rabi drive Omega = {Om:g} with spontaneous emission at rate Gamma (quantum-jump unravelling; each emission resets the state to |g> and is the atom's own event; the reset is the cut, not arc), scanned over Omega/Gamma; Fubini-Study arc with orthogonality at pi/2",
                    source=f"{SRC} [8] (CONSIST)",
                    Q="the driven atom, having events of its own, is in H-L5's arc-regular class: the Fisher arc its conditional state travels between consecutive emissions is more regular than the waiting time and than the excursion amplitude (control i), at every drive",
                    ingredient="H-L5 (the class claim) with D5 (occasion = one inter-emission interval, own event = the quantum jump), D2 on the pure-state carrier; the three A3 readings of the closed qubit are batch 01 rows 4-5 and batch 05 row 3 and are not repeated",
                    null="the clock: the waiting time between emissions, whose distribution is the domain's",
                    domain=None,
                    numbers=f"per drive (exact quadrature against the waiting-time density w(t) = Gamma |<e|psi~(t)>|^2, normalisation {min(s['Z'] for s in tab.values()):.6f}-{max(s['Z'] for s in tab.values()):.6f}): {rows_txt}; class boundary CV(C) = CV(T) at Om/Gam = {cross:.4f}; exceptional point of the no-jump evolution Om/Gam = 0.5, below it the conditional state settles at the angle asin(2 Om/Gam)/2: {fp[0.25]:.6f} against the computed arc limit {tab[0.25]['Cinf']:.6f} at Om/Gam = 0.25; on the meridian A = sin^2 C, max deviation {merid:.1e}; decisive point Om/Gam = {Om / Gam:g}: seeded record of {n_rec} emissions (seed 0): CV(T) {cv(T):.4f}, CV(C) {cv(Cs):.4f}, CV(A) {cv(As):.4f}, paired-bootstrap 95 % CI of CV(C) - CV(T) = [{lo:.4f}, {hi:.4f}]; control ii on the state (identity metric on the Bloch vector) is {eu_ratio:.4f} x the Fisher arc at every step (CV identical: {tab[Om / Gam]['cvEU']:.4f} vs {tab[Om / Gam]['cvC']:.4f}); strong drive Om/Gam = 10: CV(C) {tab[10.0]['cvC']:.4f} vs CV(T) {tab[10.0]['cvT']:.4f} ({_agree(tab[10.0]['cvC'], tab[10.0]['cvT'])}), mean arc / mean waiting time {tab[10.0]['meanC'] / tab[10.0]['meanT']:.4f} against the unitary rate Om/2 = {Om / 2:.4f}",
                    tg=f"CV(C) {dec['cvC']:.4f} vs null CV(T) {dec['cvT']:.4f} at the decisive point: {_agree(dec['cvC'], dec['cvT'])}; across the scan the two agree within 1 % at {n_tie} of {len(ratios)} drives",
                    tn=f"the domain (quantum-trajectory theory: Carmichael et al. 1989, Dalibard-Castin-Molmer 1992) has the waiting-time density and hence CV(T) = {dec['cvT']:.4f}, and no theorem for the arc between emissions: none cited for Q's target",
                    tc=f"arc-regular at every scanned drive: {_holds(check)} (arc-regular at {n_arc} of {len(ratios)}, clock-regular at {n_clock}, tie at {n_tie}; at the decisive point the CI of CV(C) - CV(T) lies {'above' if lo > 0 else 'below' if hi < 0 else 'across'} 0)",
                    out=out,
                    reading=f"the one way to give the source's qubit events of its own puts H-L5's class claim to a check in the domain's own mathematics, and the class depends on the drive: below Om/Gam = {cross:.2f} the arc is the regular quantity and beats the amplitude, above it the waiting time is, and at strong drive the arc rate and the unitary rate Om/2 {_agree(tab[10.0]['meanC'] / tab[10.0]['meanT'], Om / 2)} ({tab[10.0]['meanC'] / tab[10.0]['meanT']:.4f} against {Om / 2:.4f}) and the arc reduces to the clock; at the source's Omega with Gamma = 1 the clock wins ({dec['cvT']:.4f} against {dec['cvC']:.4f}, CI excluding 0): {out}; the arc-regular regime contains the whole overdamped range Om/Gam < 0.5 (arc-regular at {sum(1 for r in ratios if r < 0.5 and labels[r] == 'arc-regular')} of {sum(1 for r in ratios if r < 0.5)} such drives), where the conditional state settles at a fixed angle before most emissions, so the arc per occasion is a saturating function of the waiting time and its lead over the amplitude is the concavity of the angle in the population (A = sin^2 C), information geometry's",
                    weakness="the class boundary is not the exceptional point (0.81 against 0.5): between them the state no longer settles but the arc is still the more regular quantity, which the row reports and does not explain; Gamma = 1 with the source's Omega is one decisive point, and the row's verdict is the scan; control ii is not separable on a pure-state carrier (the Bloch-vector arc is exactly twice the Fisher arc), so it is reported on the population trace instead; the seeded record samples the exact density, not a stochastic integration",
                    elegance="An atom lit gently leans over to a fixed tilt and waits there to blink, so the road between blinks is nearly always the same short road while the waits are random; lit hard it keeps spinning, and the road between blinks is as random as the wait. One picture says when 'change has its own clock' and when it does not.",
                    child="Imagine a spinning top that gives a flash and stands back up every so often. Pushed gently, it tips to one lean and just waits there until the next flash: every trip between flashes is about the same length, even though the waiting is random. Pushed hard, it never stops spinning, so a long wait means a long trip. Only the gently pushed top keeps its own clock.")


# ---------------------------------------------------------------- 49 [10] two-flavour neutrino oscillation, in matter
def _nu(th, a, n=200001):
    """Two-flavour flavour state |nu_e> under H = [[-cos 2th + a, sin 2th], [sin 2th, cos 2th - a]] in units Delta m^2 / (4E) = 1
    (L in units of 4E / Delta m^2; a = A / Delta m^2 with A = 2 sqrt2 G_F N_e E the matter term). Three readings of A3 on the
    first precession period about the matter axis, the extremum (peak cut) and the domain's numbers."""
    H = np.array([[-math.cos(2 * th) + a, math.sin(2 * th)], [math.sin(2 * th), math.cos(2 * th) - a]])
    Omp = 2.0 * math.sqrt((a - math.cos(2 * th)) ** 2 + math.sin(2 * th) ** 2)   # precession rate about the matter eigen-axis
    L = np.linspace(0.0, 2 * 2 * math.pi / Omp, n)
    w, V = np.linalg.eigh(H); coef = V.T @ np.array([1.0, 0.0])
    st = (V @ (np.exp(-1j * np.outer(w, L)) * coef[:, None])).T
    C = _fs_arc(st); chord = np.arccos(np.clip(np.abs(st[:, 0]), -1.0, 1.0)); Pee = np.abs(st[:, 0]) ** 2
    i = int(np.argmax(C >= math.pi / 2)); t_arc = float(np.interp(math.pi / 2, C, L)) if i > 0 else None
    cuts = antipodal_cuts(intrinsic_phase(Pee)); t_rot = float(L[cuts[1]])
    first = slice(0, n // 2 + 1); cmax = float(chord[first].max()); t_cmax = float(L[first][int(np.argmax(chord[first]))])
    j = int(np.argmax(chord >= math.pi / 2 - 1e-6)); t_anti = float(L[j]) if j > 0 else None
    pk = peak_cuts(Pee, prominence=1e-3, distance=10); t_peak = float(L[pk[0]] if pk[0] != 0 else L[pk[1]])
    s2m = math.sin(2 * th) ** 2 / (math.sin(2 * th) ** 2 + (math.cos(2 * th) - a) ** 2)      # sin^2 2 theta_m (the domain)
    return dict(dE=math.sin(2 * th), t_arc=t_arc, t_mt=math.pi / (2 * math.sin(2 * th)), t_rot=t_rot, t_rot_closed=math.pi / Omp, cmax=cmax,
                t_cmax=t_cmax, t_anti=t_anti, t_peak=t_peak, minov=float(np.abs(st[:, 0]).min()), s2m=s2m, Pmax=float(1.0 - Pee.min()), dL=float(L[1] - L[0]))


def r4():
    ths = (0.27, 0.53, math.pi / 4)                                          # the source's grid without theta = 0 (no oscillation)
    vac = {th: _nu(th, 0.0) for th in ths}
    th = ths[0]
    a_anti = minimize_scalar(lambda a: _nu(th, a, 20001)["minov"], bounds=(0.0, 2.0), method="bounded", options=dict(xatol=1e-9)).x     # antipode criterion: the overlap with |nu_e> reaches 0
    a_peak = minimize_scalar(lambda a: -_nu(th, a, 20001)["Pmax"], bounds=(0.0, 2.0), method="bounded", options=dict(xatol=1e-9)).x    # extremum criterion: the conversion maximum is largest
    a_res = math.cos(2 * th)                                                 # MSW resonance: A = Delta m^2 cos 2 theta
    res = _nu(th, a_anti)
    readings = [res["t_arc"], res["t_anti"], res["t_rot"]]
    coincide = all(v is not None for v in readings) and all(rel(readings[0], v) <= TOL_G for v in readings[1:])
    check = rel(a_anti, a_res) <= 1e-6 and coincide and abs(res["cmax"] - math.pi / 2) < 1e-6
    out = outcome(crr=a_anti, null=a_peak, domain=a_res, check=check)
    vac_txt = "; ".join(f"theta = {t_:.4f}: rotor cut at L = {v['t_rot']:.4f} (closed form pi/2 = {v['t_rot_closed']:.4f}, the first oscillation maximum, peak cut {v['t_peak']:.4f}), arc half-turn at L = {v['t_arc']:.4f} (Mandelstam-Tamm pi/(2 sin 2 theta) = {v['t_mt']:.4f}), antipode " + (f"at L = {v['t_anti']:.4f}" if v['t_anti'] is not None else f"none (chord maximum {v['cmax']:.4f} < pi/2, minimum overlap {v['minov']:.4f} = |cos 2 theta|)") + f", P_max = {v['Pmax']:.4f}" for t_, v in vac.items())
    return make_row("nu", f"Two-flavour neutrino oscillation, |nu_e> = cos theta |nu_1> + sin theta |nu_2>, in vacuum and in matter of constant density (MSW), L in units of 4E / Delta m^2 (vacuum oscillation length pi, first maximum at pi/2), matter term a = A / Delta m^2; Fubini-Study carrier as batch 01",
                    source=f"{SRC} [10] (CONSIST)",
                    Q=f"in matter the flavour state reaches its antipode (A3's antipode reading: the orthogonal state, full conversion) if and only if the electron density is at the MSW resonance a = cos 2 theta, and there the three readings of A3 coincide at the first oscillation maximum L = pi/(2 sin 2 theta); in vacuum the rotor reading fires at the first oscillation maximum for every theta, the arc reading later, and the antipode only at theta = pi/4",
                    ingredient="A3 (antipode reading; rotor and arc readings reported), D5 (occasion = one half-precession of the flavour state about the matter axis)",
                    null="the extremum: the peak cut on the survival probability and, for the density, the largest conversion maximum (the domain's own marker)",
                    domain="Mikheyev-Smirnov-Wolfenstein: sin^2 2 theta_m = sin^2 2 theta / (sin^2 2 theta + (cos 2 theta - a)^2), maximal at the resonance a = cos 2 theta; vacuum oscillation length 4 pi E / Delta m^2",
                    numbers=f"vacuum: {vac_txt}; matter at theta = {th:g}: density at which the antipode appears (minimum overlap -> 0) a = {a_anti:.8f}, density of the largest conversion maximum a = {a_peak:.8f}, resonance cos 2 theta = {a_res:.8f}; at that density: minimum overlap {res['minov']:.1e}, sin^2 2 theta_m = {res['s2m']:.6f}, arc half-turn at L = {res['t_arc']:.4f}, antipode at L = {res['t_anti']:.4f}, rotor cut at L = {res['t_rot']:.4f}, peak cut at L = {res['t_peak']:.4f}, Mandelstam-Tamm pi/(2 sin 2 theta) = {res['t_mt']:.4f} (dE = sin 2 theta = {res['dE']:.4f}, unchanged by the matter term); grid step {res['dL']:.1e}",
                    tg=f"antipode density {a_anti:.6f} vs null (largest conversion maximum) {a_peak:.6f}: {_agree(a_anti, a_peak)}",
                    tn=f"the MSW resonance gives cos 2 theta = {a_res:.6f}: {_agree(a_anti, a_res, TOL_N)} - the domain has Q",
                    tc=f"antipode density equals the resonance within 1e-6, chord reaches pi/2 there, and the three readings of A3 coincide within 1 %: {_holds(check)}",
                    out=out,
                    reading=f"the neutrino carrier repeats the qubit of batch 05 row 3 with a knob the qubit lacks, the matter density, which moves the precession axis: the antipode exists only where the matter mixing is maximal, and that density is the resonance the domain defined by the same condition (sin^2 2 theta_m = 1, full conversion possible), so the antipode reading and the extremum reading name one density: {out}; off resonance the readings split as before (in vacuum at theta = {th:g}: rotor {vac[th]['t_rot']:.4f}, arc {vac[th]['t_arc']:.4f}, antipode none), and the rotor reading is the domain's first oscillation maximum for every theta; the mixing angle itself is fixed by nothing here",
                    weakness="constant density only; in a varying profile (the Sun) the adiabatic conversion is a monotone path with no event of its own, so H-L5 has no purchase; the theta grid is the source's; nothing here re-opens the A3 decision (synthesis note section 7, item 3)",
                    elegance="A neutrino can turn completely into the other flavour only if the two are mixed exactly half-and-half, and the Sun's matter can tune the mixing to half-and-half at one density: the resonance is where the path is lifted onto the equator. A picture with one dial, and the dial is the Sun's.",
                    child="A neutrino is born as one kind and can change into another as it flies. It can change all the way only if the two kinds are mixed exactly half-and-half, which they usually are not. Inside the Sun the crowd of electrons changes the mix, and at one depth it becomes exactly half-and-half: there, and only there, the neutrino can turn completely into the other kind.")


# ---------------------------------------------------------------- 50 [11] the trap with both parameters driven: constant Fisher speed against the domain's friction
def r5():
    x0a, ka, x0b, kb, tau = 0.0, 1.0, 1.0, 4.0, 1.0                          # translate the trap by 1 and stiffen it 1 -> 4 (the source's k1, k2) in tau = 1; beta = gamma = 1
    # the domain's friction tensor (Sivak-Crooks 2012): zeta_ij = beta int <dF_i(0) dF_j(t)> dt, F = -dH/d lambda, H = k (x - x0)^2 / 2; OU autocorrelations
    zeta_x = lambda k: quad(lambda t: k ** 2 * (1.0 / k) * math.exp(-k * t), 0.0, np.inf)[0]                 # F_x0 = k (x - x0): <dF dF(t)> = k^2 <y y(t)>
    zeta_k = lambda k: quad(lambda t: 0.25 * 2.0 * (1.0 / k) ** 2 * math.exp(-2.0 * k * t), 0.0, np.inf)[0]   # F_k = -y^2/2: <dF dF(t)> = 2 <y y(t)>^2 / 4
    g_x, g_k = (lambda k: k), (lambda k: 1.0 / (2.0 * k ** 2))                # Fisher metric of N(x0, 1/k): diag(k, 1/(2k^2))
    zk = {k: (zeta_x(k), zeta_k(k)) for k in (1.0, 2.0, 4.0)}
    aniso = {k: (zx / g_x(k), zkk / g_k(k)) for k, (zx, zkk) in zk.items()}   # zeta g^-1: the two relaxation times
    t = np.linspace(0.0, tau, 200001)
    W = lambda x0, k: float(np.trapezoid(np.gradient(x0, t) ** 2 + np.gradient(k, t) ** 2 / (4.0 * k ** 3), t))           # the domain's functional
    WF = lambda x0, k: float(np.trapezoid(k * np.gradient(x0, t) ** 2 + np.gradient(k, t) ** 2 / (2.0 * k ** 2), t))     # the source's functional (Fisher metric as the friction)
    arcF = lambda x0, k: float(np.trapezoid(np.sqrt(k * np.gradient(x0, t) ** 2 + np.gradient(k, t) ** 2 / (2.0 * k ** 2)), t))
    def dF(xa, ka_, xb, kb_):                                                 # Fisher-Rao distance: hyperbolic half-plane in (x0/sqrt2, k^-1/2), curvature -1/2
        u1, s1, u2, s2 = xa / math.sqrt(2), ka_ ** -0.5, xb / math.sqrt(2), kb_ ** -0.5
        return math.sqrt(2) * math.acosh(1.0 + ((u2 - u1) ** 2 + (s2 - s1) ** 2) / (2.0 * s1 * s2))
    d = dF(x0a, ka, x0b, kb)
    # CRR's protocol: the Fisher geodesic (a semicircle in the half-plane) at constant Fisher speed
    u1, s1, u2, s2 = x0a / math.sqrt(2), ka ** -0.5, x0b / math.sqrt(2), kb ** -0.5
    c = (u2 ** 2 + s2 ** 2 - u1 ** 2 - s1 ** 2) / (2.0 * (u2 - u1)); R = math.hypot(u1 - c, s1)
    l1, l2 = (math.log(math.tan(math.atan2(s, u - c) / 2)) for u, s in ((u1, s1), (u2, s2)))
    phi = 2.0 * np.arctan(np.exp(l1 + (l2 - l1) * t / tau)); x0g, kg = (c + R * np.cos(phi)) * math.sqrt(2), 1.0 / (R * np.sin(phi)) ** 2
    speed = np.sqrt(kg * np.gradient(x0g, t) ** 2 + np.gradient(kg, t) ** 2 / (2.0 * kg ** 2)); speed_cv = float(speed.std() / speed.mean())
    S_geo = arcF(x0g, kg) - d
    W_geoF = W(x0g, kg)
    # the domain's optimum: zeta is flat in (x0, w = -k^-1/2), so the straight line at constant speed; W_min = (dx0^2 + dw^2)/tau
    w1, w2 = -ka ** -0.5, -kb ** -0.5
    x0d, kd = x0a + (x0b - x0a) * t / tau, 1.0 / (w1 + (w2 - w1) * t / tau) ** 2
    W_dom = W(x0d, kd); W_min = ((x0b - x0a) ** 2 + (w2 - w1) ** 2) / tau
    S_dom = arcF(x0d, kd) - d
    # numerical minimum over a Fourier family started AT the Fisher geodesic
    tt = np.linspace(0.0, tau, 4001); M = 6
    phit = 2.0 * np.arctan(np.exp(l1 + (l2 - l1) * tt / tau)); x0g2, kg2 = (c + R * np.cos(phit)) * math.sqrt(2), 1.0 / (R * np.sin(phit)) ** 2
    def path(a):
        dx = sum(a[m] * np.sin((m + 1) * math.pi * tt / tau) for m in range(M)); dl = sum(a[M + m] * np.sin((m + 1) * math.pi * tt / tau) for m in range(M))
        return x0g2 + dx, kg2 * np.exp(dl)
    Wtt = lambda x0, k: float(np.trapezoid(np.gradient(x0, tt) ** 2 + np.gradient(k, tt) ** 2 / (4.0 * k ** 3), tt))
    opt = minimize(lambda a: Wtt(*path(a)), np.zeros(2 * M), method="BFGS", options=dict(gtol=1e-10))
    # a sequential protocol (translate, then stiffen, each leg at constant Fisher speed): S > 0
    dA, dB = dF(x0a, ka, x0b, ka), dF(x0b, ka, x0b, kb); t1 = tau * dA / (dA + dB)
    x0s = np.where(t <= t1, x0a + (x0b - x0a) * t / t1, x0b); ks = np.where(t <= t1, ka, ka * np.exp(np.log(kb / ka) * (t - t1) / (tau - t1)))
    W_seq, S_seq = W(x0s, ks), arcF(x0s, ks) - d
    # the source's own numbers (stiffness alone, Fisher metric as the friction): <v^2> >= <v>^2 on its lopsided protocol
    cc = math.log(kb / ka); lop_k = lambda s: ka * math.exp(cc * s ** 2); lop_kd = lambda s: 2 * cc * s * ka * math.exp(cc * s ** 2)
    v2 = quad(lambda s: g_k(lop_k(s)) * lop_kd(s) ** 2, 0, tau)[0]; v1 = quad(lambda s: math.sqrt(g_k(lop_k(s))) * abs(lop_kd(s)), 0, tau)[0]
    bound_dom_holds = (W_dom - W_min) >= S_dom ** 2 / tau - 1e-9            # the S^2 bound on the domain's optimum
    bound_seq_holds = (W_seq - W_min) >= S_seq ** 2 / tau
    check = rel(W_geoF, W_min) <= TOL_N and bound_dom_holds
    out = outcome(crr=W_geoF, null=W_dom, domain=W_min, check=check)
    return make_row("thermo", f"Overdamped particle in a harmonic trap with BOTH parameters driven, centre x0: {x0a:g} -> {x0b:g} and stiffness k: {ka:g} -> {kb:g} in tau = {tau:g} (beta = gamma = 1), excess work in the slow-driving form W = int zeta_ij lambda_i' lambda_j' dt with the friction tensor from the OU autocorrelations; the source's stiffness-only protocol is batch 02 row 2",
                    source=f"{SRC} [11] (CONSIST)",
                    Q="the minimum-dissipation protocol is the constant-speed geodesic of the Fisher-Rao metric with one global scale (A1'), and every protocol's excess over the minimum is at least S^2/tau with S its Fisher surplus",
                    ingredient="A1' (the metric is Fisher-Rao with its scale fixed once by the system's unit) with D4/P1 (S = 0 selects the geodesic; the surplus as the bound)",
                    null="the geodesic of the domain's own friction tensor zeta = g x diag(tau_x, tau_(x^2)), the two relaxation times, at constant zeta-speed",
                    domain="Sivak-Crooks 2012: W >= L_zeta^2 / tau (Cauchy-Schwarz), equality on the constant-speed zeta-geodesic; for the trap zeta is flat in (x0, -k^-1/2) so the optimum is a straight line there",
                    numbers=f"friction tensor from the autocorrelation integrals at k = 1, 2, 4: zeta_x0x0 = {zk[1.0][0]:.6f}, {zk[2.0][0]:.6f}, {zk[4.0][0]:.6f} (closed form 1), zeta_kk = {zk[1.0][1]:.6f}, {zk[2.0][1]:.6f}, {zk[4.0][1]:.6f} (closed form 1/(4k^3) = {1 / 4:.6f}, {1 / 32:.6f}, {1 / 256:.6f}); zeta g^-1 = diag(tau_x, tau_(x^2)) = ({aniso[1.0][0]:.4f}, {aniso[1.0][1]:.4f}) at k = 1, ({aniso[4.0][0]:.4f}, {aniso[4.0][1]:.4f}) at k = 4: ratio {aniso[1.0][0] / aniso[1.0][1]:.4f} at every k (not a scalar factor); Fisher chord d = {d:.5f}, Fisher geodesic arc - chord = {S_geo:.1e}, speed CV {speed_cv:.1e}; W under the domain's functional: Fisher geodesic {W_geoF:.5f}, domain's straight line {W_dom:.5f} (closed form (dx0^2 + dw^2)/tau = {W_min:.5f}), sequential protocol {W_seq:.5f}; numerical minimum over a {2 * M}-mode family started at the Fisher geodesic: {opt.fun:.5f} (first mode coefficient {opt.x[0]:.4f}, {opt.nit} BFGS iterations); Fisher surplus of the domain's optimum S = {S_dom:.5f} with excess {W_dom - W_min:.1e} against S^2/tau = {S_dom ** 2 / tau:.5f}; sequential protocol S = {S_seq:.5f}, excess {W_seq - W_min:.5f} against S^2/tau = {S_seq ** 2 / tau:.5f}; under the source's own functional (Fisher metric as the friction) the Fisher geodesic gives {WF(x0g, kg):.5f} = d^2/tau = {d ** 2 / tau:.5f} and the domain's line {WF(x0d, kd):.5f}; the source's stiffness-only numbers reproduced: <v^2> = {v2:.4f} >= <v>^2 = {v1 ** 2:.4f}",
                    tg=f"Fisher-geodesic dissipation {W_geoF:.5f} vs null (zeta-geodesic) {W_dom:.5f}: {_agree(W_geoF, W_dom)} (relative gap {(W_geoF - W_min) / W_min * 100:+.2f} %)",
                    tn=f"the domain's minimum (dx0^2 + dw^2)/tau = {W_min:.5f} vs the CRR value {W_geoF:.5f}: {_agree(W_geoF, W_min, TOL_N)}",
                    tc=f"Fisher geodesic within 1 % of the minimum: {_holds(rel(W_geoF, W_min) <= TOL_N)}; S^2/tau bounds the excess of the domain's optimum: {_holds(bound_dom_holds)} (excess {W_dom - W_min:.1e} < S^2/tau {S_dom ** 2 / tau:.5f}); of the sequential protocol: {_holds(bound_seq_holds)}",
                    out=out,
                    reading=f"the second parameter closes the escape batch 02 row 2 left open: there the domain's friction was the Fisher metric times one relaxation time, conformal to Fisher, so a unit allowed to vary along the path could have recovered the domain's rule; here the centre and the width of the trap relax at different rates (tau_x = 1/k for the centre and tau_(x^2) = 1/2k for the width, ratio {aniso[1.0][0] / aniso[1.0][1]:.0f}), the friction is Fisher times a matrix, and no scalar unit makes CRR's geodesic the optimum ({(W_geoF - W_min) / W_min * 100:+.2f} %); the S^2 clause fails on the domain's own optimum, which has zero excess and Fisher surplus {S_dom:.4f}: {out}; under the source's functional the geodesic is optimal by Cauchy-Schwarz and the bound holds by P1, Salamon-Berry's and information geometry's (batch 06 row 1)",
                    weakness="one system and one pair of endpoints, linear response only (the exact finite-time optimum with its end jumps is outside the cited functional); the Fisher geodesic is written in closed form and checked by its surplus and speed CV, the domain's optimum by a 12-mode minimiser started at CRR's protocol",
                    elegance="Slide a cup and tighten its spring at once: the cup's position settles twice as slowly as its jiggle-width, so the cheapest plan goes slower on the slow dial. One speed on one ruler is right only when every dial settles alike, and here they do not.",
                    child="Suppose you have to move a wobbly tray and also tighten the strap that holds it, in the same amount of time. The tray's place takes longer to settle than its wobble does, so you go slower on the moving part and quicker on the tightening part. Doing both at one steady pace wastes effort.")


def main():
    return run_batch("Synthesis batch 10: rows 46-50 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
