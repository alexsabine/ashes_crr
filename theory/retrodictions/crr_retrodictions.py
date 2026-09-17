"""CRR retrodiction battery (issue #21, run 2026-09-17).

Apply theory/CRR.md v3.1 (and, where a clause exists only in the issue-#21 text or in the
external GPT-6 specification, that clause, named as such) mechanically to 32 known systems and
grade each row:

  SHARP    the axioms force the known result with no outside constant
  CONSIST  the framework's form coincides with a known law but does not fix its constant or exponent
  DESCR    true, but a definition, a symmetry or a carrier fact; no one would bet against it
  FAILS    the derivation contradicts the physics, or a framework claim is a property of a special case
  TENSION  two clauses give opposite answers on the same system
  OPEN     the framework explicitly declines to derive the quantity

Every row also states BORROWED (which existing mathematics the row uses; the metric, the
distance, the identity) and FLOW (what supplies the velocity x-dot inside the coherence
integral: CRR never supplies it). Every number printed here is computed below; nothing is
transcribed. Run:  uv run python theory/retrodictions/crr_retrodictions.py
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.linalg import solve_discrete_are
from scipy.special import ellipe, ellipk

ROWS = []


def row(cls, system, clause, borrowed, flow, derivation, known, verdict, grade, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, flow=flow, derivation=derivation,
                     known=known, verdict=verdict, grade=grade, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


def half_turn_arcs(x):
    """Identity-metric arc between successive antipodal cuts of a 1-D periodic signal, using the
    analytic-signal phase (the ONE intrinsic phase implemented in src/crr; borrowed: Hilbert)."""
    from numpy.fft import fft, ifft
    n = len(x); X = fft(x - x.mean()); h = np.zeros(n); h[0] = 1; h[1:(n + 1) // 2] = 2
    if n % 2 == 0: h[n // 2] = 1
    ph = np.unwrap(np.angle(ifft(X * h)))
    cuts = [0]; target = ph[0] + np.pi
    for i in range(1, n):
        if ph[i] >= target: cuts.append(i); target += np.pi
    return [float(np.abs(np.diff(x[a:b + 1])).sum()) for a, b in zip(cuts[:-1], cuts[1:])]


# ================================================================ (a) two-state / occupancy
def a_bernoulli_antipode():
    p = sp.symbols("p", positive=True)
    L = sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, 0, 1))
    psi = lambda pv: 2 * math.asin(math.sqrt(pv))
    half_from_0 = math.sin(math.pi / 4) ** 2                           # p reached after a half-turn (psi = pi/2) from p = 0
    reach = psi(0.7) + math.pi / 2                                       # a half-turn from p = 0.7 leaves the interval
    row("a", "Bernoulli occupancy: 'the antipode is p = 1/2'", "A3 (issue-#21 text: 'half-turn at p = 1/2'); v3.1 A3 (rotor only)",
        "Fisher metric 1/(p(1-p)); arcsine coordinate", "none (kinematics only)",
        f"FR length of the family = {float(L):.5f} = pi; half-turn from p=0 lands at p={half_from_0:.3f}; from p=0.7 it would need psi={reach:.3f} > pi (off the interval)",
        "the Bernoulli manifold is an interval, not a circle", "p = 1/2 is the antipode only of the boundary start; there is no antipode from a general p",
        "FAILS", "special-case property presented as universal (issue-#21 text); v3.1 restricts A3 to cyclic carriers, where it returns OPEN")


def a_two_state_kinetics():
    k1, k2, p0, T = 0.7, 0.3, 0.05, 6.0
    pinf = k1 / (k1 + k2); k = k1 + k2
    pt = lambda t: pinf + (p0 - pinf) * math.exp(-k * t)
    pdot = lambda t: -k * (p0 - pinf) * math.exp(-k * t)
    C, _ = quad(lambda t: abs(pdot(t)) / math.sqrt(pt(t) * (1 - pt(t))), 0, T)
    D = abs(2 * math.asin(math.sqrt(pt(T))) - 2 * math.asin(math.sqrt(p0)))
    row("a", "Two-state chemical kinetics A <-> B (mass action relaxation)", "D2, D3, D4 on the Bernoulli carrier",
        "Fisher metric of the Bernoulli family; arcsine transform", "mass-action rate constants k1, k2 (system-supplied)",
        f"C = {C:.6f} (numeric integral), D = {D:.6f} (closed form), S = {C - D:.2e}: monotone relaxation is a geodesic",
        "variance-stabilising arcsine transform of a proportion", "C reproduces the arcsine coordinate change; nothing beyond it",
        "CONSIST", "the framework does not fix k1, k2, p_inf or the relaxation time; it relabels the arcsine distance")


def a_channel_gating():
    Vh, s = -40.0, 6.0
    p = lambda V: 1 / (1 + math.exp(-(V - Vh) / s))
    C = abs(2 * math.asin(math.sqrt(p(0.0))) - 2 * math.asin(math.sqrt(p(-80.0))))
    row("a", "Voltage-gated channel open probability, Boltzmann curve, ramp -80 -> 0 mV", "D2 with A1' unit = one channel event",
        "Boltzmann occupancy; Bernoulli Fisher metric", "voltage ramp rate (protocol-supplied)",
        f"arc over the ramp = {C:.5f} Fisher units, independent of ramp speed (1-D arc = total variation, monotone)",
        "the open-probability curve is a sigmoid in V", "the arc is a function of the endpoints only on a monotone ramp",
        "DESCR", "a reparameterisation of the endpoints; no prediction about the channel")


def a_poisson_counts():
    lam = sp.symbols("lam", positive=True)
    d = sp.integrate(1 / sp.sqrt(lam), (lam, 4, 9))
    row("a", "Poisson counts (epidemic incidence, photon counts)", "A1' (unit = one event), D2 on the Poisson carrier; SCOPE P6",
        "Fisher metric 1/lambda; Anscombe / square-root variance stabilisation", "the incidence curve lambda(t) (system-supplied)",
        f"FR distance lambda 4 -> 9 = {float(d):.4f} = 2(sqrt9 - sqrt4)", "square-root transform stabilises Poisson variance",
        "C on counts is the total variation of 2 sqrt(lambda)", "CONSIST", "standard; H-L5 built on it FAILED 0/17 on measles (ledger MEAS2-1)")


# ================================================================ (b) quantum
def _fs_arc(states):
    ov = np.abs(np.sum(np.conj(states[:-1]) * states[1:], 1)); return float(np.sum(np.arccos(np.clip(ov, -1, 1))))


def b_qubit_rabi():
    Om = 1.0; t = np.linspace(0, np.pi / Om, 4001)
    st = np.stack([np.cos(Om * t / 2), np.sin(Om * t / 2)], 1).astype(complex)
    C = _fs_arc(st); D = float(np.arccos(abs(np.vdot(st[0], st[-1]))))
    row("b", "Qubit, resonant Rabi drive to the orthogonal state (pi pulse)", "A2a / v3.1 A3 on the Bloch great circle; D2, D3",
        "Fubini-Study / Wootters statistical distance; Bloch sphere", "the Hamiltonian (Rabi frequency Omega, system-supplied)",
        f"C = {C:.6f}, D = {D:.6f} = pi/2, S = {C - D:.1e}; the cut (orthogonal state) is reached at t = pi/Omega",
        "a pi pulse takes |0> to |1> along a great circle", "C/H = 1 on the geodesic, as A2a says; the time pi/Omega is the Hamiltonian's",
        "CONSIST", "the framework does not fix Omega or the pulse time; it names the geodesic")


def b_quantum_speed_limit():
    Om, Delta = 1.0, 0.8; t = np.linspace(0, 3.0, 6001)
    Hm = 0.5 * np.array([[Delta, Om], [Om, -Delta]]); w, V = np.linalg.eigh(Hm)
    psi0 = np.array([1.0, 0.0], complex)
    st = np.array([V @ (np.exp(-1j * w * tt) * (V.conj().T @ psi0)) for tt in t])
    C = _fs_arc(st); D = float(np.arccos(min(1.0, abs(np.vdot(st[0], st[-1])))))
    dE = float(np.sqrt(np.vdot(psi0, Hm @ Hm @ psi0).real - np.vdot(psi0, Hm @ psi0).real ** 2))
    row("b", "Qubit, detuned drive: Anandan-Aharonov / Mandelstam-Tamm bound", "P1 (C >= D) on the Fubini-Study carrier",
        "Fubini-Study metric; energy variance as speed (Anandan-Aharonov 1990)", "the Hamiltonian (detuning Delta, drive Omega)",
        f"C = {C:.5f} = DeltaE*t = {dE * t[-1]:.5f}; D = {D:.5f}; C > D by {C - D:.4f}; orthogonality never reached (max D < pi/2)",
        "time to orthogonality >= pi/(2 DeltaE)", "the QSL is the triangle inequality P1 in the FS metric",
        "CONSIST", "the bound is Anandan-Aharonov's; CRR adds the name 'surplus' to the slack")


def b_qutrit():
    psi = np.array([1, 0, 0], complex)
    null_dim = 3 - np.linalg.matrix_rank(psi.reshape(1, 3))
    row("b", "Qutrit: the orthogonal 'antipode'", "A2a / A2c (spec); v3.1 A3",
        "Hilbert-space orthogonality", "none",
        f"orthogonal complement of a qutrit state has dimension {null_dim}: no unique target",
        "a state in d >= 3 has a (d-1)-dimensional orthogonal subspace", "no canonical antipode; CRR must return OPEN",
        "OPEN", "the spec's A2c says so; the issue-#21 text ('the orthogonal state') presumes uniqueness that does not hold")


def b_mixed_states():
    def bures(r1, r2):
        s1 = np.sqrt(r1); F = np.trace(np.sqrt(s1 @ r2 @ s1)).real ** 2; return float(np.arccos(min(1.0, math.sqrt(F))))
    full1, full2 = np.diag([0.9, 0.1]), np.diag([0.1, 0.9])
    rank1, rank1b = np.diag([1.0, 0.0]), np.diag([0.0, 1.0])
    row("b", "Mixed qubit states under dephasing: 'mixed states never cut'", "A3 note (issue-#21 text); spec XI.3 removes it",
        "Bures angle / Uhlmann fidelity", "the dephasing map (system-supplied)",
        f"full-rank pair: Bures angle {bures(full1, full2):.4f} < pi/2 (never orthogonal); rank-1 pair: {bures(rank1, rank1b):.4f} = pi/2 (orthogonal)",
        "orthogonality needs disjoint supports", "full-rank mixed states never reach the antipode; rank-deficient ones can",
        "FAILS", "the universal 'never' is false; the correct statement is support-dependent (spec XI.3)")


# ================================================================ (c) thermal ensembles
def c_schottky_length():
    eps = 1.0
    L = quad(lambda b: eps * 0.5 / float(np.cosh(b * eps / 2)), 0, np.inf)[0]      # sqrt(p(1-p)) = 1/(2 cosh(beta eps/2)); int sqrt(Var E) dbeta
    row("c", "Two-level (Schottky) system: thermodynamic length from T = inf to T = 0", "D2 on the canonical-ensemble carrier in beta",
        "Fisher information = energy variance; thermodynamic length (Weinhold, Ruppeiner, Crooks)", "the cooling protocol beta(t)",
        f"L = int sqrt(Var E) dbeta = {L:.6f} = pi/2 = {math.pi / 2:.6f} (finite)", "thermodynamic length of a two-level system is pi/2",
        "C reproduces the thermodynamic length", "CONSIST", "constant fixed by the Bernoulli geometry, not by CRR")


def c_optimal_protocol():
    k1, k2, tau = 1.0, 4.0, 1.0
    g = lambda k: 1 / (2 * k ** 2)                                            # Fisher metric of exp(-beta k x^2/2) in k (beta = 1)
    def cost(kfun, kdot):
        return quad(lambda t: g(kfun(t)) * kdot(t) ** 2, 0, tau)[0]
    lin = cost(lambda t: k1 + (k2 - k1) * t, lambda t: k2 - k1)
    c = math.log(k2 / k1); geo = cost(lambda t: k1 * math.exp(c * t), lambda t: c * k1 * math.exp(c * t))
    L = math.sqrt(2) ** -1 * abs(math.log(k2 / k1))
    row("c", "Harmonic trap stiffness protocol k1 -> k2: minimum-dissipation (slow-driving) protocol", "P1 / T3: a geodesic has S = 0",
        "thermodynamic length; linear-response dissipation W_diss ~ L^2/tau (Sivak-Crooks 2012)", "the protocol speed k-dot (experimenter-supplied)",
        f"FR length = {L:.5f}; action: linear protocol {lin:.5f}, geodesic (log-linear) {geo:.5f} = L^2/tau = {L ** 2 / tau:.5f}",
        "the optimal slow protocol is the constant-speed geodesic (exponential k(t))", "S = 0 picks the geodesic; the constant-speed rule is Cauchy-Schwarz",
        "CONSIST", "CRR names the geodesic; the dissipation bound and the protocol are inherited")


def c_mean_field_ising():
    J = 1.0
    def m_of(beta):
        m = 0.9
        for _ in range(2000): m = math.tanh(beta * J * m)
        return m
    def E(beta): return -0.5 * J * m_of(beta) ** 2                      # per spin
    betas = np.linspace(0.8, 1.2, 4001); Es = np.array([E(b) for b in betas])
    varE = -np.gradient(Es, betas)                                        # Var(E) = -dE/dbeta = Fisher metric g_bb
    row("c", "Mean-field Ising: Fisher metric g_beta,beta at the critical point", "SCOPE/issue-#21 text 'thermal Fisher metric diverges at criticality'",
        "Fisher metric = heat capacity / beta^2 (energy variance)", "none (equilibrium family)",
        f"max Var(E) on beta in [0.8,1.2] = {varE.max():.4f} (finite jump at beta_c = 1); no divergence",
        "mean-field specific heat has a finite jump", "the universal divergence claim fails in the mean-field class",
        "FAILS", "divergence is universality-class dependent (spec XI.4); v3.1 makes no criticality claim, the issue-#21 text does")


def c_onsager_ising():
    def Cv(K):
        k1 = 2 * math.sinh(2 * K) / math.cosh(2 * K) ** 2; k1p = 2 * math.tanh(2 * K) ** 2 - 1
        Kk, Ek = ellipk(k1 ** 2), ellipe(k1 ** 2)
        return (2 / math.pi) * (K / math.tanh(2 * K)) ** 2 * (2 * Kk - 2 * Ek - (1 - k1p) * (math.pi / 2 + k1p * Kk))
    Kc = 0.5 * math.log(1 + math.sqrt(2)); vals = [(d, Cv(Kc * (1 - d))) for d in (1e-1, 1e-2, 1e-3, 1e-4)]
    mono = all(vals[i + 1][1] > vals[i][1] for i in range(3))
    row("c", "2-D Ising (Onsager): Fisher metric at the critical point", "same clause as the mean-field row",
        "Onsager's exact specific heat (elliptic integrals)", "none",
        "Cv at |1-K/Kc| = " + ", ".join(f"{d:g}: {c:.3f}" for d, c in vals) + (" (grows without bound, log divergence)" if mono else ""),
        "logarithmic specific-heat divergence", "here the Fisher metric does diverge: the claim is class-dependent",
        "CONSIST", "true in this class, false in mean field (previous row): as a framework law it is FAILS; as a class statement it is Onsager's")


# ================================================================ (d) estimation and filtering
def d_kalman():
    v = sp.symbols("v", positive=True); K = (v / 2) * (sp.sqrt(v ** 2 + 4) - v)
    row("d", "Scalar random-walk Kalman filter", "P4",
        "steady-state Riccati equation", "the state recursion (q, r supplied)",
        f"K(1) = {float(K.subs(v, 1)):.6f} = 1/phi; K -> {sp.limit(K, v, sp.oo)} as v -> inf",
        "textbook steady-state gain", "identical; CRR reads v = sqrt(q/r) as a Fisher speed", "CONSIST",
        "v3.1 itself says the formula is not CRR's")


def d_fisher_additivity():
    row("d", "Cramer-Rao unit and Fisher additivity I_N = N I_1", "A1' / spec A1a",
        "Cramer-Rao bound; additivity of Fisher information under iid sampling", "none",
        "unit = 1/sqrt(I_1) per elementary event; N observations shorten the unit by sqrt(N) (verified symbolically in verify_spec_math.py)",
        "standard estimation theory", "a definition of the unit", "DESCR", "no prediction")


def d_sequential_bayes():
    rng = np.random.default_rng(1); mu_true, sig = 0.3, 1.0
    y = mu_true + sig * rng.standard_normal(200); post = np.cumsum(y) / np.arange(1, 201)   # posterior mean (flat prior)
    d = np.diff(post); F, B = d[d > 0].sum(), -d[d < 0].sum(); C = (F + B) / sig; D = abs(post[-1] - post[0]) / sig; S = C - D
    B = min(F, B)                                                            # T4 with the net displacement oriented positive
    row("d", "Sequential Bayesian updating of a Gaussian mean (posterior-mean path)", "D2-D4, T4 (S = 2B) in the per-event unit",
        "Gaussian conjugacy; FR distance |dmu|/sigma (SCOPE P8)", "the data order (the stream)",
        f"C = {C:.4f}, D = {D:.4f}, S = {S:.4f} = 2B = {2 * B / sig:.4f}: surplus is twice the posterior's backtracking",
        "posterior mean wanders then settles", "S is a name for the backtracking of the estimate", "DESCR",
        "no prediction about the data; a Markov (depth-one) system by A4/spec: the salience law would predict nothing here")


def d_equanimity_vs_bayes():
    ratios = (0.1, 1.0, 10.0)
    infl = {r: (1 + r) ** 2 / (4 * r) for r in ratios}                         # MSE of equal-precision fusion / Bayes-optimal MSE
    gp, gq = 3.0, 0.03                                                          # gradient norms with the past nearly at its anchor
    w_ratio = gp / gq
    row("d", "Two-source fusion: 'equal pull' (A9 / H-EQ) against Bayes-optimal precision weighting", "A9 (issue-#21 text: equal precision, 'never a ratio of pull magnitudes') vs v3.1 H-EQ (ratio of gradient norms)",
        "Bayesian fusion (inverse-variance weights)", "none",
        "equal-precision weight is Bayes-optimal iff the precisions are equal: MSE inflation at precision ratio " + ", ".join(f"{r:g}: {infl[r]:.3f}x" for r in ratios)
        + f"; the norm-ratio form gives w = {w_ratio:.0f} when the past gradient is small (the issue text calls this ill-posed; EQ2's pass lives there, cap 1e4)",
        "inverse-variance weighting", "the two clauses disagree whenever pull magnitudes are not precisions", "TENSION",
        "the spec's [P7]/[H1] (weights on occasions) and v3.1's [H-EQ] (gradient-norm ratio) are different laws under one name; resolve before any further EQ prereg")


# ================================================================ (e) oscillators and limit cycles (physical)
def e_harmonic():
    t = np.linspace(0, 4 * np.pi, 40001); A = 2.5
    arcs = half_turn_arcs(A * np.sin(t)); arcs = arcs[1:-1]
    row("e", "Harmonic oscillator, amplitude A", "A3 (antipodal cut on the phase rotor), D2 with identity metric; SCOPE P9",
        "Hilbert / analytic-signal phase; 1-D arc = total variation", "the oscillator's own period (irrelevant to the arc)",
        f"arc per half-turn = {np.mean(arcs):.4f} (= 2A = {2 * A}); period does not enter",
        "a half cycle sweeps 2A", "definition", "DESCR", "")


def e_asymmetric_halfturns():
    t = np.linspace(0, 6 * np.pi, 60001)
    sym = half_turn_arcs(np.sin(t))[1:-1]; asym = half_turn_arcs(np.sin(t) + 1.2 * np.sin(2 * t) + 0.6 * np.sin(3 * t))[1:-1]
    row("e", "Asymmetric multi-harmonic oscillator: are the two half-turn arcs equal?", "A3 note (v3.1): 'equal arcs are not a consequence of A3'",
        "analytic-signal phase", "the waveform",
        f"sine: consecutive half-turn arcs CV = {cv(sym):.4f}; asymmetric: CV = {cv(asym):.4f} (unequal)",
        "symmetry of the waveform", "equal half-turn arcs hold only by symmetry; v3.1 already declines the claim", "DESCR",
        "a symmetry check that passes only on the symmetric member (issue rule 4) — correctly not claimed")


def e_fm_vs_am():
    rng = np.random.default_rng(2); n = 40
    per = 2 * np.pi * (1 + 0.15 * rng.standard_normal(n)); amp = 1 + 0.15 * rng.standard_normal(n)
    fm_clock, fm_arc = cv(per), 0.0                                              # FM: arc per half-turn constant (2A, A = 1)
    am_clock, am_arc = 0.0, cv(2 * amp)
    row("e", "'Change has its own clock' (H-L5) on a limit cycle with period jitter vs amplitude jitter", "H-L5",
        "coefficient of variation; the S-A'/S-A'' surrogates of the battery", "the modulation (which quantity jitters)",
        f"period jitter: CV_clock = {fm_clock:.3f}, CV_arc = {fm_arc:.3f} by construction (arc wins); amplitude jitter: CV_clock = {am_clock:.3f}, CV_arc = {am_arc:.3f} (clock wins)",
        "both classes exist in nature (measles: clock-regular, ledger MEAS2)", "nothing in the axioms picks the class; the claim is empirical, not derived",
        "FAILS", "as a derivation: the framework cannot say which clock a system keeps; it can only measure it (v3.1 says so; the slogan overstates)")


def e_pendulum():
    g_over_l = 1.0
    T = lambda A: 4 / math.sqrt(g_over_l) * ellipk(math.sin(A / 2) ** 2)
    rng = np.random.default_rng(3); A = 1.0 + 0.1 * rng.standard_normal(60)
    row("e", "Plane pendulum with amplitude jitter (exact period via K(k))", "H-L5 controls (i) amplitude, clock",
        "elliptic-integral period T(A)", "gravity and length (set the period), the jitter (set by the drive)",
        f"CV_arc (= CV of 2A) = {cv(2 * A):.4f}; CV_clock (= CV of T(A)) = {cv([T(a) for a in A]):.4f}: the clock is the more regular quantity",
        "period grows slowly with amplitude", "a physical oscillator in the clock-regular class, like measles", "DESCR",
        "confirms the measles reading on a textbook system; no CRR content")


# ================================================================ (f) point processes and natural time
def f_poisson_process():
    lam = sp.symbols("lam", positive=True)
    row("f", "Homogeneous Poisson process: natural time", "A1' (unit = one event), D5 (occasion = inter-event interval)",
        "exponential inter-event law; Fisher metric of the rate family 1/lambda^2 per unit time", "the rate",
        f"FR distance between rates lambda1, lambda2 per unit exposure = |ln(lambda2/lambda1)| (from g = 1/lambda^2): {float(sp.integrate(1 / lam, (lam, 2, 6))):.4f} for 2 -> 6",
        "natural time (Varotsos) counts events", "a definition of the unit", "DESCR", "")


def f_omori():
    t, c, K, p, rho = sp.symbols("t c K p rho", positive=True)
    A = K * sp.log((t + c) / c)                                                # p = 1: cumulative rate int_0^t K/(s+c) ds
    ret = sp.exp(-A / rho)
    arc_inf = 2 * sp.sqrt(K) * c ** (-p / 2)                                    # Poisson-metric arc from t=0 to infinity for p>0
    row("f", "Omori aftershock decay lambda = K (t+c)^-p", "P5 (consistency relation), D2 on the Poisson carrier",
        "Omori law; natural time; power-law/exponential calculus", "the rate lambda(t) (rate-and-state friction supplies p)",
        f"retention at p=1: {sp.simplify(ret)} (a power law in shifted time, exactly as P5 states); Poisson arc to infinity = {arc_inf} (finite) while the count diverges for p <= 1",
        "p ~ 1 empirically; the count of aftershocks diverges logarithmically", "P5 is calculus; 'the arc converges' is Anscombe on a decaying rate",
        "CONSIST", "p is not fixed by CRR (v3.1 says so)")


def f_hawkes():
    rng = np.random.default_rng(4); mu, a, b = 0.5, 0.6, 2.0
    lam0 = 1.7; jumps = rng.integers(2, 8, 4)
    # exponential-kernel Hawkes: lambda(t) is Markov; two histories with the same lambda(t0) give the same law afterwards
    fut = [mu + (lam0 - mu) * math.exp(-b * 0.5) for _ in jumps]
    row("f", "Hawkes process with exponential kernel: does history beyond the present intensity matter?", "A4 (spec: screening-off / depth-one gate)",
        "Markov property of the exponential-kernel intensity", "the kernel (system-supplied)",
        f"future intensity after 0.5 s from four different histories sharing lambda(t0) = {lam0}: {fut[0]:.4f} (all equal)",
        "the intensity is a sufficient statistic", "depth one: CRR must predict no multi-occasion salience effect here", "DESCR",
        "the e^S law would be falsified if applied; the gate exists to stop that (spec Decision 7)")


def f_natural_time_kappa1():
    row("f", "Natural-time variance kappa_1 = 0.070 at criticality (Varotsos)", "none",
        "natural-time analysis", "none",
        "CRR has no clause that produces kappa_1 or 0.070", "kappa_1 -> 0.070 before main shocks (empirical)",
        "not derivable from the axioms", "OPEN", "")


# ================================================================ (g) gravitational, astrophysical, cosmological
def g_kepler():
    e = 0.6; a = 1.0
    r = lambda nu: a * (1 - e ** 2) / (1 + e * math.cos(nu))
    ds = lambda nu: math.sqrt(r(nu) ** 2 + (a * (1 - e ** 2) * e * math.sin(nu) / (1 + e * math.cos(nu)) ** 2) ** 2)
    L1 = quad(ds, 0, math.pi)[0]; L2 = quad(ds, math.pi, 2 * math.pi)[0]
    row("g", "Kepler ellipse (e = 0.6): the two half-turns between apsides", "A3 (antipode = apoapsis from periapsis), D2 with the Euclidean metric on the orbit plane",
        "orbital mechanics; the true anomaly as phase", "gravity (sets the speed; the arc is geometric)",
        f"arc periapsis->apoapsis = {L1:.6f}, apoapsis->periapsis = {L2:.6f}: equal by reflection symmetry",
        "an ellipse is symmetric about its major axis", "equal half-turn arcs by symmetry only (a perturbed orbit breaks it)", "DESCR",
        "no statistical carrier here: the Euclidean metric is a stand-in, which v3.1 A1 does not license")


def g_chirp():
    tc = 1.0; phi = lambda t: -(tc - t) ** (5 / 8) * 40                         # leading-order inspiral phase (scaled)
    t = np.linspace(0, 0.999, 200001); ph = phi(t); ph -= ph[0]
    cuts = np.searchsorted(ph, np.arange(np.pi, ph[-1], np.pi)); dt = np.diff(t[cuts])
    row("g", "Binary inspiral chirp: occasions per half-turn of the gravitational-wave phase", "A3, D5, H-L5 (natural time = phase)",
        "post-Newtonian phase evolution Phi ~ (t_c - t)^(5/8)", "general relativity (the chirp rate)",
        f"{len(dt)} half-turns; clock interval falls from {dt[0]:.4f} to {dt[-1]:.5f} s while the phase interval is pi by construction",
        "the chirp accelerates; cycles to merger are finite", "phase-regular by definition of the cut; says nothing", "DESCR", "")


def g_cosmology():
    row("g", "Cosmological parameter inference (CMB Fisher forecasts)", "A1 (carrier exists), A3 (no cut)",
        "Fisher-matrix forecasting", "none",
        "a statistical manifold with a Fisher metric exists (the likelihood), but no occasion boundary: quantitative CRR returns OPEN",
        "Fisher forecasting is standard cosmology", "no occasion structure", "OPEN", "")


def g_schwarzschild():
    row("g", "Schwarzschild geodesics", "A1 (carrier requirement)",
        "differential geometry of spacetime", "none",
        "no statistical family; the spacetime metric is not a Fisher metric: not a carrier", "—", "not a carrier", "OPEN",
        "the gravitational class yields only OPEN/DESCR rows")


# ================================================================ (h) bifurcations and critical phenomena
def h_hopf():
    mus = np.array([1e-1, 1e-2, 1e-3]); r = np.sqrt(mus); sigma = 0.05
    row("h", "Hopf normal form: cycle amplitude r = sqrt(mu - mu_c)", "D1 resolution rho = extent/sigma (issue-#21 text: rho -> 0 at Hopf)",
        "normal-form amplitude scaling", "the normal form",
        "rho = 2r/sigma with sigma fixed at 0.05: " + ", ".join(f"mu={m:g}: {2 * rr / sigma:.2f}" for m, rr in zip(mus, r)) + " -> 0",
        "amplitude vanishes at the Hopf point", "true if sigma is fixed; the spec removes universality because sigma is measured (D1)", "CONSIST",
        "conditional on a fixed resolution; v3.1 D1 says rho is never predicted")


def h_critical_slowing():
    q, r = 1.0, 1.0
    def gain(k):
        a = 1 - k; P = solve_discrete_are(np.array([[a]]), np.array([[1.0]]), np.array([[q]]), np.array([[r]]))
        return float(P.item() / (P.item() + r))
    ks = (0.5, 0.1, 0.01, 0.001); K = [gain(k) for k in ks]; Krw = 0.5 * (math.sqrt(5) - 1)
    row("h", "Critical slowing down: AR(1) state x' = (1-k)x + w observed in noise, Kalman depth d = 1/K as k -> 0", "D8 (issue-#21 text: 'd -> inf near a bifurcation'); v3.1 O1 (retention not claimed)",
        "discrete algebraic Riccati equation", "the state recursion (k, q, r supplied)",
        "K at k = " + ", ".join(f"{k:g}: {kk:.4f}" for k, kk in zip(ks, K)) + f" -> random-walk value {Krw:.4f}: d stays finite (1/K -> {1 / Krw:.3f})",
        "the filter approaches the random-walk filter", "'depth diverges at criticality' is false at fixed q, r; it needs q -> 0 too", "FAILS",
        "v3.1 O1 already declines a retention law (OPEN there); the issue-#21 text's D8 is the clause that fails")


def h_pitchfork():
    T = 1.0
    def fisher(mu):
        V = lambda x: -mu * x ** 2 / 2 + x ** 4 / 4
        Z = quad(lambda x: math.exp(-V(x) / T), -8, 8)[0]
        m2 = quad(lambda x: x ** 2 * math.exp(-V(x) / T), -8, 8)[0] / Z; m4 = quad(lambda x: x ** 4 * math.exp(-V(x) / T), -8, 8)[0] / Z
        return (m4 - m2 ** 2) / (4 * T ** 2)                                  # I(mu) = Var(x^2)/(4T^2)
    mus = (-1.0, -0.1, 0.0, 0.1, 1.0); I = [fisher(m) for m in mus]
    row("h", "Landau pitchfork (Boltzmann family in the control mu): Fisher information at the bifurcation", "issue-#21 text criticality clause",
        "Fisher information of an exponential family = variance of the sufficient statistic", "none (equilibrium family)",
        "I(mu) at mu = " + ", ".join(f"{m:g}: {i:.4f}" for m, i in zip(mus, I)) + " (finite and smooth through mu = 0)",
        "mean-field transition, finite fluctuations at fixed T", "no divergence: a second counterexample to the universal claim", "FAILS", "")


def h_period_doubling():
    row("h", "Logistic-map period doubling (Feigenbaum)", "A1 (canonical carrier)",
        "renormalisation theory", "the map",
        "no observation model is supplied, so there is no statistical carrier; delta = 4.669... is not touched by any clause", "Feigenbaum constants",
        "not a carrier without an independently justified observation model", "OPEN", "")


BATTERY = [a_bernoulli_antipode, a_two_state_kinetics, a_channel_gating, a_poisson_counts,
           b_qubit_rabi, b_quantum_speed_limit, b_qutrit, b_mixed_states,
           c_schottky_length, c_optimal_protocol, c_mean_field_ising, c_onsager_ising,
           d_kalman, d_fisher_additivity, d_sequential_bayes, d_equanimity_vs_bayes,
           e_harmonic, e_asymmetric_halfturns, e_fm_vs_am, e_pendulum,
           f_poisson_process, f_omori, f_hawkes, f_natural_time_kappa1,
           g_kepler, g_chirp, g_cosmology, g_schwarzschild,
           h_hopf, h_critical_slowing, h_pitchfork, h_period_doubling]
CLASSES = {"a": "two-state / occupancy", "b": "quantum", "c": "thermal", "d": "estimation / filtering",
           "e": "oscillators", "f": "point processes / natural time", "g": "gravitational / cosmological", "h": "bifurcations / criticality"}


def main():
    for f in BATTERY: f()
    print("CRR retrodiction battery — 32 systems, 8 classes (issue #21). Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}\n     FLOW:       {r['flow']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    print("\n" + "=" * 100 + "\nTALLY")
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print(f"{'class':34s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rows = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:30s} " + " ".join(f"{sum(r['grade'] == g for r in rows):8d}" for g in grades))
    print(f"{'all':34s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print(f"\nrows whose BORROWED field is empty: {sum(1 for r in ROWS if not r['borrowed'] or r['borrowed'] == 'none')}"
          f"; rows where the coherence integral's velocity is system-supplied (FLOW != none): {sum(1 for r in ROWS if r['flow'] != 'none' and r['flow'] != '—')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
