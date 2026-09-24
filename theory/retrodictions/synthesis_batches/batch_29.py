"""Synthesis batch 29: Carlo Rovelli's mathematics taken with CRR whole (owner request 2026-09-24, prompt-log entry 130;
declared in DECLARATION_29_30.md, pushed before this script). Five rows on model systems (no data, R2): [1] thermal
time (Connes-Rovelli) against CRR's natural time (the arc of the state); [2] equilibrium as equal natural-time rates
(H-EQ between two systems) against Haggard-Rovelli's thermal time and the zeroth law; [3] A3's cut on the thermal-time
flow of a Gibbs state; [4] RQM's stable facts against A3's cut of the environment's record (Zurek's spin environment);
[5] the black-to-white-hole lifetime's undetermined boundary-state spread against H-EQ's equal pull.
Sources (docs/citations/smolin_rovelli_gough_2026-09-24.md, versions seen 2026-09-24): Connes & Rovelli gr-qc/9406019;
Haggard & Rovelli 1302.0724; Christodoulou & D'Ambrosio 1801.03027 v3 eqs. 53-58. Named by name and year only: Yao & Qi
2010, de Boer et al. 2019 (capacity of entanglement); Zurek 1982; Enestrom-Kakeya. Deterministic; under 60 s."""
import math
import sys

import numpy as np

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _w(cond, yes, no):
    return yes if cond else no


def _gibbs(E, beta):
    p = np.exp(-beta * (E - E.min())); return p / p.sum()


# ---------------------------------------------------------------- [1] thermal time against natural time
def r1():
    E = np.sort(np.random.default_rng(291).normal(0.0, 1.0, 40)); beta = 1.3
    p = _gibbs(E, beta); K = -np.log(p)                                        # the modular Hamiltonian of the reduced state, K = -ln rho
    def overlap(s): return abs(np.sum(p * np.exp(-1j * s * K)))                # <TFD| e^{-i s K_A} |TFD>: the one-sided modular (thermal-time) flow
    ds = 1e-4; crr = math.acos(min(1.0, overlap(ds))) / ds                     # CRR natural time per unit thermal time: the Fubini-Study arc rate of the purification
    null = 1.0                                                                 # thermal time's own rate per unit modular parameter
    S = float(-np.sum(p * np.log(p))); CE = float(np.sum(p * np.log(p) ** 2) - S ** 2)
    C = beta ** 2 * float(np.sum(p * E ** 2) - np.sum(p * E) ** 2)
    domain = math.sqrt(CE)                                                     # capacity of entanglement: Var(K) (Yao-Qi; de Boer et al.)
    check = rel(crr, math.sqrt(C)) <= TOL_N                                    # and, for a Gibbs state, Var(K) = beta^2 Var(H) = C (heat capacity in k_B)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("tt", "Gibbs state of a 40-level spectrum (levels drawn N(0, 1), seed 291) at beta = 1.3, purified as a thermofield double; the thermal-time flow of Connes-Rovelli is the modular flow of the reduced state, applied one-sidedly to the purification",
                    source="rovelli dossier 2(a) (gr-qc/9406019; synthesis.txt row 10 read UNSTATED)",
                    Q="CRR's natural time (the arc the state travels, H-L5/O3: change has its own clock) counted along thermal time ticks at sqrt(Var K) per unit of the modular parameter, which for a Gibbs state is sqrt(C), the square root of the heat capacity in k_B: a proposition relating the rate of change of the state to the rate of the state's own flow, which synthesis.txt row 10 did not find",
                    ingredient="H-L5/O3 (the clock is the arc of the state, not a flow parameter) on the Fubini-Study metric of the purification (D2 is information geometry's)",
                    null="thermal time itself: rate 1 per unit modular parameter",
                    domain="the capacity of entanglement C_E = Var(K) = <(ln rho)^2> - S^2 (Yao and Qi 2010; de Boer, Jarvela and Keski-Vakkuri 2019), and Mandelstam-Tamm (the arc rate of a pure state under a generator is its standard deviation)",
                    numbers=f"arc rate per unit modular parameter {crr:.6f}; sqrt(capacity of entanglement) {domain:.6f}; sqrt(heat capacity C/k_B) {math.sqrt(C):.6f}; entanglement entropy {S:.4f}",
                    tg=f"{crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the capacity of entanglement gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"arc rate within 1 % of sqrt(C) (the Gibbs identity Var K = C): {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"there is a proposition after all: CRR's clock and thermal time measure different things (the state's change and the state's own flow) and their ratio is sqrt(Var K), the capacity of entanglement, {domain:.4f} here; the domain named it: a Gibbs state's thermal time carries the heat capacity's square root of distinguishable change per unit, and a state with no energy spread (zero capacity) has thermal time but no natural time",
                    weakness="one random finite spectrum; for type III algebras (local QFT) Var K diverges with the cutoff (the capacity of entanglement is UV-divergent for a region), so the rate is defined only with a regulator",
                    elegance="Thermal time and 'change time' differ by exactly one number, the square root of how much heat the system can hold: a hot system that can hold heat changes a lot per tick, a system that cannot has a clock that ticks over nothing.",
                    child="Rovelli says a warm thing has its own clock. CRR says time is how much something changes. They agree if you count the changes: the more heat something can soak up, the more it changes each tick of its warm clock.")


# ---------------------------------------------------------------- [2] equilibrium as equal natural-time rates
def _C_modes(T, w):
    x = w / T; return float(np.sum(x ** 2 * np.exp(x) / np.expm1(x) ** 2))   # heat capacity (k_B) of quantum harmonic modes


def r2():
    w1 = np.linspace(0.05, 0.2, 4); w2 = np.linspace(0.05, 0.2, 16); T1 = 1.0     # system 1: 4 modes, system 2: 16 modes (the same band)
    rate1 = math.sqrt(_C_modes(T1, w1)) * T1                                    # natural-time rate per unit physical time: sqrt(C) T (row 1, t = beta s)
    lo, hi = 1e-3, 10.0
    for _ in range(200):                                                        # solve sqrt(C2(T2)) T2 = rate1 (equal pull between the two arc clocks, H-EQ at Omega = 1)
        mid = 0.5 * (lo + hi)
        if math.sqrt(_C_modes(mid, w2)) * mid < rate1: lo = mid
        else: hi = mid
    T2 = 0.5 * (lo + hi); crr = T2 / T1
    null = 1.0                                                                  # Haggard-Rovelli: tau = kT t / hbar, equal rates -> T2 = T1
    domain = 1.0                                                                # the zeroth law
    wb = np.linspace(0.05, 0.2, 64)                                             # heat current between the two, golden rule over a shared band: J ~ sum w (n1 - n2)
    nB = lambda w, T: 1.0 / np.expm1(w / T)
    J = float(np.sum(wb * (nB(wb, T1) - nB(wb, T2)))); Jscale = float(np.sum(wb * nB(wb, T1)))
    check = abs(J) / Jscale < 1e-3                                              # equilibrium means no net heat flow
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("tt", "two systems of quantum harmonic modes in the same band (0.05-0.2, units kT1 = 1): system 1 with 4 modes, system 2 with 16, coupled weakly (golden-rule heat current)",
                    source="rovelli dossier 2(a) (Haggard & Rovelli 1302.0724: thermal time counts distinguishable states; equilibrium = equal thermal-time rates)",
                    Q="two systems are in equilibrium when their natural-time rates are equal (H-EQ at Omega = 1 between the two arc clocks), i.e. sqrt(C1) T1 = sqrt(C2) T2, so T2/T1 = sqrt(C1/C2) and not 1",
                    ingredient="H-EQ (equal pull, Omega = 1) between two systems' H-L5 arc clocks (row 1: rate sqrt(C) T per unit physical time)",
                    null="Haggard-Rovelli's thermal time tau = kT t/hbar (one distinguishable state per kT/hbar): equal rates give T2/T1 = 1",
                    domain="the zeroth law: equilibrium is T1 = T2",
                    numbers=f"C1 {_C_modes(T1, w1):.4f}, C2 at the CRR point {_C_modes(T2, w2):.4f}; CRR's equilibrium T2/T1 = {crr:.4f}; net heat current there {J:+.4e} (relative {abs(J) / Jscale:.3e} of the one-way current)",
                    tg=f"T2/T1 {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the zeroth law gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"no net heat flow at the CRR point (relative current below 1e-3): {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"equal natural-time rates are not equilibrium: at T2/T1 = {crr:.4f} heat flows (relative current {abs(J) / Jscale:.3e}); what equalises at equilibrium is Haggard-Rovelli's count per degree of freedom, kT/hbar, not the arc of the whole state, which carries sqrt(C) and so grows with the size of the system; CRR's equanimity read as equal clock rates between systems is contradicted by the zeroth law, and thermal time, not the arc clock, is the equilibrium clock",
                    weakness="harmonic modes in the classical-leaning regime (C close to the mode count); the arc rate is the purification's, one of several ways to give a mixed state a clock",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] A3's cut on the thermal-time flow
def r3():
    beta_d = 1.0; x = math.exp(-beta_d); N = 400
    pk = x ** np.arange(N); pk /= pk.sum()
    th = np.linspace(0.0, 2 * math.pi, 40001)
    A = np.abs(np.exp(-1j * np.outer(th, np.arange(N))) @ pk)
    crr = float(A.min())                                                        # the closest approach to the antipode along the flow (0 = the cut fires)
    pu = np.ones(N) / N; Au = np.abs(np.exp(-1j * np.outer(th, np.arange(N))) @ pu)
    null = float(Au.min())                                                      # infinite temperature: uniform weights, the cut fires
    domain = (1 - x) / (1 + x)                                                  # the oscillator's characteristic function |(1-x)/(1-x e^{-i theta})| at theta = pi
    check = crr > 0.0 and rel(crr, domain) <= TOL_N
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("tt", "Gibbs state of an equally spaced spectrum (gap Delta, 400 levels, beta Delta = 1) under its thermal-time (Hamiltonian) flow, angle theta = t Delta over one period",
                    source="rovelli dossier 2(b) problem 4 (every faithful state is in equilibrium with its own flow)",
                    Q="A3's cut (the antipode: a state orthogonal to where the flow started) never fires on the thermal-time flow of a finite-temperature Gibbs state with an equally spaced spectrum; the closest approach is (1 - x)/(1 + x), x = e^(-beta Delta)",
                    ingredient="A3 (the occasion ends at the antipode of the intrinsic phase) on the purification's flow",
                    null="the same flow at infinite temperature (uniform weights), where the overlap reaches 0 and the cut fires",
                    domain="the characteristic function of the geometric (oscillator) distribution in closed form; Enestrom-Kakeya: a polynomial with strictly decreasing positive coefficients has no zero on or inside the unit circle",
                    numbers=f"minimum overlap along one period: {crr:.6f} at beta Delta = {beta_d:g}; closed form {domain:.6f}; at infinite temperature {null:.2e}",
                    tg=f"{crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the closed form gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"overlap stays positive and equals the closed form: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"thermal time is a flow without cuts: at any finite temperature the state never reaches an antipode along its own flow (closest approach {crr:.4f}), so no CRR occasion completes in thermal time; occasions need something the Gibbs state's own flow cannot supply (an interaction, a measurement, a record). The domain's closed form carries the number; the metaphysical reading is CRR's: Rovelli's time flows, CRR's time happens",
                    weakness="an equally spaced spectrum; for dense many-body spectra the overlap can come exponentially close to zero (the spectral form factor's dip) and exact zeros appear only in the thermodynamic limit (dynamical phase transitions)",
                    elegance="A warm thing's own clock goes round and round but never gets to the opposite side: to have a real event something else has to happen to it.",
                    child="Imagine a spinning top that is a little bit sleepy (warm). It keeps turning, but it never turns all the way to facing the other way. For something new to happen, something has to bump it.")


# ---------------------------------------------------------------- [4] RQM stable facts against A3's cut of the record
def _record(g, t):
    return np.prod(np.abs(np.cos(np.outer(t, g))), axis=1)                      # Zurek: decoherence factor |r(t)| = prod |cos(g_k t)|


def r4():
    t = np.linspace(0.0, 40.0, 400001)
    g_big = np.random.default_rng(294).uniform(0.5, 1.5, 12); g_small = np.array([0.83, 1.27])
    res = {}
    for nm, g in (("N = 12", g_big), ("N = 2", g_small)):
        r = _record(g, t); tc = math.pi / (2 * g.max()); i = int(np.searchsorted(t, tc))
        after = float(r[i + 1:].max())
        above = np.where(r > 0.1)[0]; t_stab = float(t[above[-1] + 1]) if len(above) and above[-1] + 1 < len(t) else float("inf")
        res[nm] = (tc, after, t_stab, float(np.sum(g ** 2)))
    tc, after, t_stab, s2 = res["N = 12"]
    crr = tc                                                                    # CRR: the fact is fixed at the record's first cut (orthogonal branch records)
    null = t_stab                                                               # decoherence's own stability time (record overlap stays below 0.1 thereafter, in the window)
    domain = math.sqrt(2 * math.log(10.0) / s2)                                # Zurek's Gaussian short-time law: exp(-t^2 sum g^2 / 2) = 0.1
    check = all(v[1] <= 0.1 for v in res.values())                              # after the cut the record stays within 0.1 of orthogonality, for both environments
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    big, small = res["N = 12"], res["N = 2"]
    big_st = f"becomes stable only from t = {big[2]:.4f}, {big[2] / big[0]:.1f} times its cut time" if big[2] < float("inf") else "never becomes stable in the window"
    small_st = f"becomes stable from t = {small[2]:.4f}" if small[2] < float("inf") else "never becomes stable in the window"
    reading = (f"the cut does not mark a stable fact: it fires in both environments at the time one spin records perfectly, and afterwards the branches "
               f"partly recohere in both (max overlap after the cut {big[1]:.4f} for N = 12, {small[1]:.4f} for N = 2); the large environment {big_st}, the small one "
               f"{small_st}; stability is decoherence's many-record property (how many spins hold the record), not a single orthogonality event, so RQM's "
               f"stable facts are not CRR occasions without the domain's redundancy (quantum Darwinism)")
    return make_row("rqm", "Zurek's spin environment: a system qubit coupled to N environment spins with couplings g_k; the two branch records have overlap r(t) = prod cos(g_k t); N = 12 (g uniform on [0.5, 1.5], seed 294) and N = 2 (g = 0.83, 1.27)",
                    source="rovelli dossier 1 (relational QM; Di Biagio and Rovelli, stable and relative facts via decoherence)",
                    Q="a relative fact becomes a stable fact at A3's cut of the environment's record: the first time the branch records are orthogonal, t = pi/(2 g_max), after which the record stays at the antipode",
                    ingredient="A3/D5 (the occasion and its fact are fixed at the antipode: here the orthogonality of the two branch records)",
                    null="decoherence's own criterion: the first time after which the record overlap stays below 0.1 for the rest of the window",
                    domain="Zurek 1982: the decoherence factor falls as exp(-t^2 sum g_k^2 / 2) at short times; its time to 0.1 is sqrt(2 ln 10 / sum g^2)",
                    numbers=f"N = 12: first cut at t = {res['N = 12'][0]:.4f}, max overlap after it {res['N = 12'][1]:.4f}, stable (overlap below 0.1 thereafter) from t = {res['N = 12'][2]:.4f}; N = 2: first cut at t = {res['N = 2'][0]:.4f}, max overlap after it {res['N = 2'][1]:.4f}, stable from t = {res['N = 2'][2]:.4g}; Zurek's time to 0.1 (N = 12) {domain:.4f}",
                    tg=f"cut time {crr:.4f} vs decoherence's stability time {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Zurek's Gaussian law gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"after the cut the record stays within 0.1 of orthogonality for both environments: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=reading,
                    weakness="pure-dephasing spin model with a fixed window (t up to 40); for N = 12 recurrences exist beyond any fixed window (Poincare), so 'stable' is window-relative in both readings",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] the black-to-white-hole lifetime's spread
def r5():
    XI = 1820.0; masses = np.arange(10, 16)                                     # Xi ~ 1820 (Rovelli and Vidotto 2024; Christodoulou-D'Ambrosio fig. 7), masses 10..15 in Planck units (their numerics)
    t_eq = 1.0 / masses ** 2                                                    # H-EQ: sqrt(t) / 1 = (1/sqrt(t)) / m^2  (equal relative spreads of zeta and A, A ~ m^2)
    t_abs = np.ones_like(t_eq)                                                  # null: equal absolute spreads sqrt(t) = 1/sqrt(t)
    t_bal = np.sqrt((1.0 / masses ** 2) * 1.0) ** 2                             # the domain's balanced state: sqrt(t) the geometric mean of the window bounds 1/m^2 and 1 (eq. 54-56)
    n_eq = -float(np.polyfit(np.log(masses), np.log(t_eq), 1)[0]); n_abs = -float(np.polyfit(np.log(masses), np.log(t_abs), 1)[0])
    n_bal = -float(np.polyfit(np.log(masses), np.log(t_bal), 1)[0])
    crr = float(t_eq[0]); null = float(t_abs[0]); domain = float(t_bal[0])
    inwin = bool(np.all((1.0 / masses ** 2 < np.sqrt(t_eq)) & (np.sqrt(t_eq) < 1.0)))
    out = outcome(crr=crr, null=null, domain=domain, check=inwin)
    logtau = XI / t_eq
    return make_row("bh", "the LQG black-to-white-hole transition amplitude with a heat-kernel coherent boundary state of spread parameter t: Delta zeta ~ sqrt(t), Delta A ~ hbar G/sqrt(t), A ~ m^2 (Christodoulou-D'Ambrosio 1801.03027 v3 eq. 53), lifetime tau ~ e^{Xi/t(m)}",
                    source="rovelli dossier 4(b) problem 1 (the lifetime depends on the spread t(m); 'we do not have a better argument for what should be the chosen value of t')",
                    Q="equal pull between the two conjugate relative spreads (H-EQ at Omega = 1: Delta zeta / 1 = Delta A / A) fixes the boundary state's spread at t = hbar G/m^2 (n = 2 in t = m^-n), hence tau ~ m e^{m^2 Xi/hbar G}",
                    ingredient="H-EQ (Omega = 1: equal pull of two terms, each in its own unit: the relative spread of each conjugate variable)",
                    null="equal absolute spreads (Delta zeta = Delta A in Planck units): t = 1, n = 0, outside the semiclassical window",
                    domain="Christodoulou-D'Ambrosio eq. 56: the balanced semiclassical state, sqrt(t) the geometric mean of the window hbar G/m^2 << sqrt(t) << 1, t = hbar G/m^2",
                    numbers=f"t at m = 10: CRR {crr:.4g}, null {null:.4g}, balanced {domain:.4g}; fitted exponent n: CRR {n_eq:.4f}, null {n_abs:.4f}, balanced {n_bal:.4f}; CRR's t inside the semiclassical window at every mass: {inwin}; log tau = Xi/t from {logtau[0]:.4g} (m = 10) to {logtau[-1]:.4g} (m = 15)",
                    tg=f"t {crr:.4g} vs null {null:.4g}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the balanced state gives {domain:.4g}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"inside the semiclassical window at every mass: {_w(inwin, 'holds', 'fails')}",
                    out=out,
                    reading="equanimity is the domain's balanced state: equal pull between the relative spreads of the conjugate pair is the geometric mean of the semiclassical window, which Christodoulou and D'Ambrosio chose for want of a better argument; CRR supplies a reason for their choice (each variable held in its own unit with equal pull) but not a new number, and the open problem (why this state) moves to why Omega = 1, which CRR does not derive either",
                    weakness="the lifetime formula is the first-order vertex-expansion estimate the authors themselves call not reliable for this observable; Xi is their fitted constant; the reason offered is a reading, not a derivation of the boundary state",
                    elegance="The white hole's clock is set by holding its size and its shape equally loosely: not the size exactly and the shape vaguely, nor the other way round.",
                    child="If you want to guess when a bubble will pop, you should be equally unsure about how big it is and about how it is bending. Being very sure about one and very unsure about the other gives a silly answer.")


def main():
    return run_batch("Synthesis batch 29: Rovelli (prompt-log entry 130; DECLARATION_29_30.md)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
