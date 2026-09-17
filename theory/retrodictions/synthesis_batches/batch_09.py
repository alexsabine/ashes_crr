"""Synthesis batch 09: rows 41-45 of QUEUE.md (prompt-log entry 61). Two from Daniel's battery runs/phaseA/crr_retrodictions.txt
(script crr_retrodictions.py at the repository root): [h4] critical opalescence, observability of the Fisher divergence (DESCR);
[h5] superradiant QPT (Dicke), soft-mode closure and the D8 route (CONSIST; CRR.md v3.1 has O1, retention depth open, where the
older text had D8). Three from theory/retrodictions/sharp_claims.txt (script sharp_claims.py): [1] first-order decay, 'the cut is
the half-life' (DESCR); [3] Michaelis-Menten / Hill, 'theta = 1/2 at S = K_M for every n' (DESCR); [4] acid-base titration,
'ionised fraction 1/2 at pH = pKa' (DESCR). The three sharp rows are pole-start cuts at p = 1/2 on Bernoulli-type families, a
reading batch 02 row 1 and batch 05 row 1 already made on the two-level family; here each is re-read on the carrier the system
itself has (the decay's rate family, the receptor's ligation-state family, the acid's species family) to see what, if anything,
A3 adds beyond the family's symmetry. Models re-implemented from the source functions (_h4_critical_opalescence,
_h5_superradiant_qpt, a_first_order_decay, a_michaelis_menten, a_titration); nothing imported from theory/retrodictions.
Deterministic, no data (R2). Run:  uv run python theory/retrodictions/synthesis_batches/batch_09.py
"""
import math
import sys

import numpy as np

from crr.instrument.core import arc_length
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _word(cond, yes, no):
    return yes if cond else no


def _half_arc_point(u, cum, total):
    """Coordinate u at which the cumulative arc `cum` reaches total/2 (linear interpolation between grid points)."""
    i = int(np.searchsorted(cum, total / 2.0))
    f = (total / 2.0 - cum[i - 1]) / (cum[i] - cum[i - 1])
    return float(u[i - 1] + f * (u[i] - u[i - 1])), i


def _categorical_path(P, u):
    """Fisher-Rao arc along a categorical path P (n, k): steps 2 |d sqrt p| (vertex-to-vertex geodesic = pi), cumulative and total."""
    steps = 2.0 * np.linalg.norm(np.diff(np.sqrt(P), axis=0), axis=1)
    cum = np.concatenate([[0.0], np.cumsum(steps)])
    return steps, cum, float(cum[-1])


# ---------------------------------------------------------------- 41 [h4] critical opalescence: the fluid's own unit is one correlation volume
def r1():
    fam = {"2-D Ising lattice gas, exact (nu = 1, gamma = 7/4, beta = 1/8)": (2, 1.0, 1.75, 0.125),
           "mean field in d = 4 (nu = 1/2, gamma = 1, beta = 1/2)": (4, 0.5, 1.0, 0.5),
           "mean-field exponents used in d = 3": (3, 0.5, 1.0, 0.5)}
    res = {}
    for name, (d, nu, gam, beta) in fam.items():
        own = (d * nu - gam) / 2.0                     # sigma_n/n over one correlation volume xi^d: Var N/<N> = n kT kappa_T, <N> = n xi^d
        instr = -gam / 2.0                             # sigma_n/n over a fixed (instrument) volume
        res[name] = dict(own=own, instr=instr, beta=beta, rho_own=beta - own, rho_instr=beta + gam / 2.0)
    d3, nu3, gam3 = 3, 0.63, 1.24                      # the source row's 3-D numbers (no beta cited there)
    own3 = (d3 * nu3 - gam3) / 2.0
    ex = res["2-D Ising lattice gas, exact (nu = 1, gamma = 7/4, beta = 1/8)"]
    # Ornstein-Zernike probe in the source row's form S(q) = |t|^-gamma / (1 + q^2 |t|^-2 nu), xi = |t|^-nu (2-D exponents)
    nu, gam, q0 = 1.0, 1.75, 1.0
    ts = np.logspace(-2.0, -6.0, 5)
    S_fixed = ts ** (-gam) / (1.0 + q0 ** 2 * ts ** (-2.0 * nu))
    S_own = ts ** (-gam) / (1.0 + 1.0)                 # q = 1/xi: q xi = 1
    sl_fixed = float((np.diff(np.log(S_fixed)) / np.diff(np.log(ts)))[-1])
    sl_own = float((np.diff(np.log(S_own)) / np.diff(np.log(ts)))[-1])
    check = abs(ex["rho_own"]) < 1e-12
    out = outcome(crr=ex["own"], null=ex["instr"], domain=ex["beta"], check=check)
    numbers = ("exponents of sigma_n/n, the relative density fluctuation of one volume, from Var N/<N> = n kT kappa_T ~ |t|^-gamma: in the fluid's own volume xi^d, (d nu - gamma)/2; in a fixed instrument volume, -gamma/2; the coexistence gap Delta n/n ~ |t|^beta; rho = Delta n / sigma_n (D1); "
               + "; ".join(f"{k}: own {v['own']:.4f}, instrument {v['instr']:.4f}, beta {v['beta']:.4f} -> rho exponent own {v['rho_own']:.4f}, instrument {v['rho_instr']:.4f}" for k, v in res.items())
               + f"; the source row's 3-D numbers (nu = {nu3:g}, gamma = {gam3:g}): own {own3:.4f} (no beta cited here, R10); Ornstein-Zernike at fixed optical q0 = 1 (xi units, 2-D exponents): local log-slope of S(q0) at |t| = 1e-5..1e-6 is {sl_fixed:.4f} (2 nu - gamma = {2 * nu - gam:.4f}, the source row's saturation), at the fluid's own scale q = 1/xi it is {sl_own:.4f} (-gamma)")
    return make_row("crit", "Near-critical fluid on the grand-canonical density family (Daniel's battery row h4 re-read): I_mumu = beta^2 Var N, Var N/<N> = n kT kappa_T (fluctuation-compressibility sum rule), kappa_T ~ |t|^-gamma, xi ~ |t|^-nu, coexistence gap ~ |t|^beta; exact 2-D Ising lattice-gas exponents as the source battery's row h2 lists them, mean field, and the source row's 3-D numbers",
                    source="runs/phaseA/crr_retrodictions.txt [h4] (DESCR)",
                    Q="in the fluid's own unit (A1': the density fluctuation of one correlation volume xi^d is the smallest density change the fluid itself resolves), the coexisting liquid and gas stay a fixed number of resolvable steps apart as T -> Tc (rho exponent 0), whereas in an instrument's unit (a fixed scattering volume) they merge below one step",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step, rho = extent / unit); D2 with A1 supplies nothing here beyond the sum rule",
                    null="the instrument's unit: the density fluctuation of a fixed volume (the scattering volume at one optical wavelength, the source row's fixed q0)",
                    domain="the hyperscaling relation d nu = 2 beta + gamma (exact in 2-D; holds for the true exponents at d <= 4, fails for mean-field exponents below d = 4)",
                    numbers=numbers,
                    tg=f"own-unit exponent {ex['own']:.4f} vs instrument-unit exponent {ex['instr']:.4f} (2-D exact): {_word(rel(ex['own'], ex['instr']) <= TOL_G, 'agree', 'differ')}",
                    tn=f"hyperscaling gives the own-unit exponent as beta = {ex['beta']:.4f}: {_word(rel(ex['own'], ex['beta']) <= TOL_N, 'the domain has Q', 'the domain does not give Q')}",
                    tc=f"rho in the own unit has exponent {ex['rho_own']:.4f} (|.| < 1e-12 with the exact 2-D exponents): {_word(check, 'holds', 'fails')} (and it is the hyperscaling identity; with mean-field exponents in d = 3 the exponent is {res['mean-field exponents used in d = 3']['rho_own']:.4f}, where the domain says hyperscaling fails)",
                    out=out,
                    reading=f"A1' read on the fluid (the smallest density change the fluid resolves is the fluctuation of one of its own correlation volumes, not of the instrument's scattering volume) turns the source row's observability remark into one statement: in the fluid's own unit the coexisting phases stay a fixed number of resolvable steps apart as they merge, in the instrument's unit they merge below one step and the fixed-q0 intensity stops diverging (local slope {sl_fixed:+.4f}, the source row's saturation); that statement is the hyperscaling relation, which the domain has, so the label is {out}; the source row's flag (read the resolution on xi, not on a fixed wavelength) is the same choice of unit in the source's words",
                    weakness="exponent arithmetic only: the sum rule and the Ornstein-Zernike form are used as the domain gives them and no fluid is simulated; the 3-D case cannot be closed here without a cited beta (R10); where hyperscaling fails Q fails with it, which is the domain's own statement, not CRR's",
                    elegance="Count in patches, not in metres: near the critical point the liquid and the gas are made of ever-larger patches, and measured in patches they stay the same number of steps apart even as they become alike. A rule with no knobs, and it is the domain's (hyperscaling).",
                    child="Near one special temperature a liquid and its steam start to look the same, and the liquid turns milky because it is full of patches, some thicker and some thinner, that grow bigger and bigger. If you use a patch as your ruler, the liquid and the steam stay the same number of patches apart right up to the end; it is only a fixed ruler that sees them melt together.")


# ---------------------------------------------------------------- 42 [h5] Dicke soft mode: the own unit of the depth route, three ways
def _omega_soft(g, w0, w):
    T = w0 ** 2 + w ** 2
    detK = w0 * w * (w0 * w - g * g)
    return math.sqrt(max(0.0, (T - math.sqrt(T * T - 4.0 * detK)) / 2.0))


def _K_gain(v):
    return (v / 2.0) * (math.sqrt(v * v + 4.0) - v)


def _A_of(g, w0, w):
    """Ground-state precision matrix K^(1/2) of the quadratic form H = p.p/2 + x.K x/2 (thermodynamic-limit Dicke, source row h5)."""
    Kmat = np.array([[w0 ** 2, -g * math.sqrt(w0 * w)], [-g * math.sqrt(w0 * w), w ** 2]])
    lam, U = np.linalg.eigh(Kmat)
    return (U * np.sqrt(lam)) @ U.T


def _overlap(A, B):
    return float((np.linalg.det(A) ** 0.25 * np.linalg.det(B) ** 0.25) / math.sqrt(np.linalg.det((A + B) / 2.0)))


def _bures_metric(g, h, w0, w):
    """Fubini-Study metric along g of the pure Gaussian ground state (orthogonal = pi convention): g_gg = tr((A^-1 A')^2)/2."""
    A = _A_of(g, w0, w)
    Ap = (_A_of(g + h, w0, w) - _A_of(g - h, w0, w)) / (2.0 * h)
    M = np.linalg.inv(A) @ Ap
    return float(0.5 * np.trace(M @ M))


def _dicke_readings(w0, w, dt=1.0, D=1.0):
    gc = math.sqrt(w0 * w)
    C = 2.0 * (w0 * w) ** 1.5 / (w0 ** 2 + w ** 2)
    eps = np.logspace(-2.0, -8.0, 7)
    d_own, d_det, d_instr, tau = [], [], [], []
    for e in eps:
        k = _omega_soft(gc - e, w0, w)
        v_own = math.sqrt(1.0 - math.exp(-2.0 * k * dt))                       # unit = the soft mode's equilibrium fluctuation (h1's own-unit OU)
        v_det = 1.0 - math.exp(-k * dt)                                        # unit = the soft mode's own displacement (h1's deterministic path)
        v_ins = math.sqrt((1.0 - math.exp(-2.0 * k * dt)) / (2.0 * k * dt))    # unit = fixed instrument noise r = 2 D dt (the null)
        d_own.append(1.0 / _K_gain(v_own)); d_det.append(1.0 / _K_gain(v_det)); d_instr.append(1.0 / _K_gain(v_ins)); tau.append(1.0 / k)
    def slope(a):
        a = np.asarray(a); return float((np.diff(np.log(a)) / np.diff(np.log(eps)))[-1])
    gm, gm_num = [], []
    for e in eps[:5]:
        g = gc - e; h = e * 1e-3
        gm.append(_bures_metric(g, h, w0, w))
        gm_num.append((2.0 * math.acos(min(1.0, _overlap(_A_of(g - h / 2.0, w0, w), _A_of(g + h / 2.0, w0, w)))) / h) ** 2)
    L = []
    for e in (1e-1, 1e-2, 1e-3, 1e-4):
        gs = np.unique(np.concatenate([np.linspace(0.0, gc - 0.2, 2001), gc - np.logspace(math.log10(0.2), math.log10(e), 4001)]))
        sp = np.array([math.sqrt(_bures_metric(g, min(1e-6, (gc - g) * 1e-3), w0, w)) for g in gs])
        L.append(float(np.trapezoid(sp, gs)))
    return dict(gc=gc, C=C, eps=eps, d_own=d_own, d_det=d_det, d_instr=d_instr, tau=tau, s_own=slope(d_own), s_det=slope(d_det),
                s_instr=slope(d_instr), s_tau=slope(tau), gm=gm, gm_num=gm_num, s_gm=float((np.diff(np.log(gm)) / np.diff(np.log(eps[:5])))[-1]),
                gm_gap=max(rel(a, b) for a, b in zip(gm, gm_num)), L=L, dL=[L[i + 1] - L[i] for i in range(3)])


def r2():
    R = {"omega0 = omega = 1": _dicke_readings(1.0, 1.0), "detuned omega0 = 1, omega = 2 (the source row's probe)": _dicke_readings(1.0, 2.0)}
    r = R["omega0 = omega = 1"]
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    internal = rel(r["s_own"], r["s_det"]) > TOL_G
    out = outcome(internal=internal)
    numbers = "; ".join(
        f"{k}: gc = {v['gc']:.4f}, Omega_-^2 ~ C (gc - g) with C = {v['C']:.4f}; depth d = 1/K(v) at gc - g = 1e-2 / 1e-8: fluctuation reading {v['d_own'][0]:.4f} / {v['d_own'][-1]:.4f} (local exponent {v['s_own']:.4f}), deterministic reading {v['d_det'][0]:.4f} / {v['d_det'][-1]:.4f} (exponent {v['s_det']:.4f}), instrument-unit null {v['d_instr'][0]:.4f} / {v['d_instr'][-1]:.4f} (exponent {v['s_instr']:.4f}), domain's tau = 1/Omega_- {v['tau'][0]:.4f} / {v['tau'][-1]:.4f} (exponent {v['s_tau']:.4f}); "
        f"Bures metric along g at gc - g = 1e-2: {v['gm'][0]:.4e} (from overlaps {v['gm_num'][0]:.4e}; trace and overlap formulas within {v['gm_gap']:.1e} over five decades), at 1e-6: {v['gm'][4]:.4e}, exponent {v['s_gm']:.4f}; arc from g = 0 to gc - eps for eps = 1e-1, 1e-2, 1e-3, 1e-4: {v['L'][0]:.4f}, {v['L'][1]:.4f}, {v['L'][2]:.4f}, {v['L'][3]:.4f} (increments per decade {v['dL'][0]:.4f}, {v['dL'][1]:.4f}, {v['dL'][2]:.4f})"
        for k, v in R.items()) + f"; golden ratio {phi:.4f}; the source row's symbolic limits: fluctuation reading -1/4, domain -1/2; batch 02 row 3's finite length through the 2-D Ising point for contrast"
    return make_row("qpt", "Dicke model in the thermodynamic limit on the source row's quadratic form (stiffness K = [[omega0^2, -g sqrt(omega0 omega)], [., omega^2]], soft mode Omega_- closing at gc = sqrt(omega0 omega)), the soft mode read as an OU relaxation at rate k = Omega_- with step dt = 1 (Daniel's battery row h5 re-read; the older text's D8 is v3.1's O1)",
                    source="runs/phaseA/crr_retrodictions.txt [h5] (CONSIST)",
                    Q="the memory depth of the soft mode, counted in the system's own unit, diverges at the superradiant transition as (gc - g)^(-1/4) (the source row's D8 route: own-unit Fisher speed v per step, depth 1/K(v) by P4)",
                    ingredient="A1' (the own unit) on a fluctuating carrier, in its two readings from the source battery's row h1: (i) the soft mode's equilibrium fluctuation as the unit, v^2 = 1 - e^(-2 k dt); (ii) the soft mode's own displacement as the unit, v = 1 - e^(-k dt); P4 supplies K(v); and, on the state family itself (the source row's carrier line), (iii) the Bures step along g",
                    null="the instrument's unit: a fixed observation noise r = 2 D dt, under which v -> 1 and the depth tends to the random-walk value 1/K(1) = golden ratio",
                    domain="critical slowing down: relaxation time tau = 1/Omega_- ~ (gc - g)^(-1/2) (nu = 1/2, z = 1); the fidelity susceptibility diverges at gc (direction only in the source row)",
                    numbers=numbers,
                    tg=f"fluctuation reading: depth exponent {r['s_own']:.4f} vs null (instrument unit) exponent {r['s_instr']:.4f} with depth -> {r['d_instr'][-1]:.4f}: {_word(rel(r['s_own'], r['s_instr']) <= TOL_G, 'agree', 'differ')} (the own unit does work); fluctuation reading {r['s_own']:.4f} vs deterministic reading {r['s_det']:.4f}: {_word(rel(r['s_own'], r['s_det']) <= TOL_G, 'agree', 'differ')} - both are readings of A1'",
                    tn=f"the domain's tau has exponent {r['s_tau']:.4f}: the fluctuation reading {r['s_own']:.4f} {_word(rel(r['s_own'], r['s_tau']) <= TOL_N, 'agrees', 'differs')}, the deterministic reading {r['s_det']:.4f} {_word(rel(r['s_det'], r['s_tau']) <= TOL_N, 'agrees (the domain has that one)', 'differs')}",
                    tc="not reached: the two readings of the own unit give different exponents, and v3.1's O1 says the depth is not derived for a mean-reverting state model",
                    out=out,
                    reading=f"under v3.1 the source row's D8 is O1, and the row shows why it is open: 'the system's own unit' on the soft mode is two different objects, its equilibrium fluctuation or its own displacement, giving depth exponents {r['s_own']:.4f} and {r['s_det']:.4f}, the second being the domain's relaxation time and the first a number the domain does not name; on the state family itself the unit goes the other way: the Bures step along g shrinks as (gc - g)^1 (metric exponent {r['s_gm']:.4f}), so the arc to gc grows by {r['dL'][2]:.4f} per decade without bound, a logarithmic divergence where the 2-D Ising thermal family has a finite length; {out} until v3.2 fixes which object is the unit, and until then no depth exponent is CRR's",
                    weakness=f"the thermodynamic-limit quadratic form is exact only at N = infinity, where the ground state is Gaussian and its Bures metric is the pure-state Fubini-Study metric (orthogonal = pi convention; overlap and trace formulas agree within {r['gm_gap']:.1e}); the OU readings inherit h1's choices (dt = 1, k = Omega_-), the null fixes r = 2 D dt by choice, and the local exponents are read at gc - g = 1e-8 (the symbolic limits are -1/4 and -1/2); no depth is measured on any Dicke system")


# ---------------------------------------------------------------- 43 sharp [1] first-order decay: the cut on the fraction carrier and on the rate carrier
def r3():
    k, T, n = 0.7, 200.0, 2000001
    t = np.linspace(0.0, T, n)
    laws = {1: np.exp(-k * t), 2: 1.0 / (1.0 + k * t), 3: (1.0 + 2.0 * k * t) ** -0.5}     # dN/dt = -k N^n, N0 = 1
    res = {}
    for order, N in laws.items():
        rate = k * N ** order
        psi_occ = 2.0 * np.arcsin(np.sqrt(N))                                   # Bernoulli (fraction remaining) carrier, pole to pole = pi
        cum_occ = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(psi_occ)))])
        t_occ, _ = _half_arc_point(t, cum_occ, math.pi)
        out_d = {}
        for Delta in (1.0, 4.0):                                                # Poisson (count-rate) carrier, counts in a window Delta: arc 2 sqrt(lambda Delta)
            psi_rate = 2.0 * np.sqrt(rate * Delta)
            cum_rate = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(psi_rate)))])
            t_rate, _ = _half_arc_point(t, cum_rate, 2.0 * math.sqrt(k * Delta))
            out_d[Delta] = (t_rate, float(cum_rate[-1]))
        res[order] = dict(t_occ=t_occ, N_occ=float(np.interp(t_occ, t, N)), t_rate=out_d[1.0][0], N_rate=float(np.interp(out_d[1.0][0], t, N)),
                          t_rate4=out_d[4.0][0], arc_occ=float(cum_occ[-1]), arc_rate=out_d[1.0][1], frac_pred=2.0 ** (-2.0 / order),
                          def_occ=math.pi - float(cum_occ[-1]), def_rate=2.0 * math.sqrt(k) - out_d[1.0][1])
    r1_ = res[1]; t_half = math.log(2.0) / k
    t_nat = float(np.interp(0.5, 1.0 - laws[1], t))                          # natural time: half the decays have happened (1 - N = 1/2)
    def_max = max(max(v["def_occ"], v["def_rate"]) for v in res.values())
    inside = all(v["arc_occ"] > math.pi / 2.0 and v["arc_rate"] > math.sqrt(k) for v in res.values())   # every half-total reached on the grid
    internal = rel(r1_["t_occ"], r1_["t_rate"]) > TOL_G
    out = outcome(internal=internal)
    numbers = (f"k = {k:g}, N0 = 1, grid to t = {T:g}; first order: fraction carrier cut at t = {r1_['t_occ']:.4f} (ln 2 / k = {t_half:.4f}), fraction remaining {r1_['N_occ']:.4f}, arc reached {r1_['arc_occ']:.4f} of pi; rate carrier cut at t = {r1_['t_rate']:.4f} (2 ln 2 / k = {2.0 * t_half:.4f}), fraction remaining {r1_['N_rate']:.4f} (2^(-2/n) = {r1_['frac_pred']:.4f}), arc reached {r1_['arc_rate']:.4f} of 2 sqrt k = {2.0 * math.sqrt(k):.4f}; the window Delta cancels in the cut: Delta = 4 gives t = {r1_['t_rate4']:.4f}; natural time (A1' for a point process: one decay = one step) has half the decays at t = {t_nat:.4f}, which O3 says is a unit and not a cut; "
               + "; ".join(f"order {o}: fraction cut t = {v['t_occ']:.4f} (remaining {v['N_occ']:.4f}, arc reached {v['arc_occ']:.4f} of pi), rate cut t = {v['t_rate']:.4f} (remaining {v['N_rate']:.4f}, 2^(-2/n) = {v['frac_pred']:.4f}, arc reached {v['arc_rate']:.4f} of {2.0 * math.sqrt(k):.4f})" for o, v in res.items() if o > 1)
               + f"; 1/k = {1.0 / k:.4f} (the second-order half-time of the source row); largest arc left beyond the grid {def_max:.4f}; every half-total (pi/2 = {math.pi / 2.0:.4f}, sqrt k = {math.sqrt(k):.4f}) is reached on the grid: {inside}, so every cut lies inside it")
    return make_row("chem", "Decay dN/dt = -k N^n (k = 0.7, the source row's rate; n = 1, and the source row's second-order probe n = 2, plus n = 3), on two carriers the process has: the Bernoulli family in the fraction remaining (the source row's occupancy reading) and the Poisson count-rate family in lambda = k N^n (what a counter sees; the carrier of the ledger's measles study)",
                    source="theory/retrodictions/sharp_claims.txt [1] (DESCR)",
                    Q="the pole-start cut of a first-order decay is the half-life on every carrier the decay has (the source row's 'the cut is the half-life', read beyond the fraction carrier)",
                    ingredient="A3 as the sharp rows read it on a non-cyclic carrier (the cut at half the arc from the starting pole to the far pole), on A1's carrier for the decay: the fraction family (arc 2 asin sqrt N, total pi) and the rate family (arc 2 sqrt(lambda Delta), total 2 sqrt(k Delta))",
                    null="the domain's half-life, defined as the time to N = N0/2",
                    domain="t_1/2 = ln 2 / k for first-order kinetics; a second-order half-time 1/k (the source row's probe)",
                    numbers=numbers,
                    tg=f"rate-carrier cut {r1_['t_rate']:.4f} vs null (half-life {t_half:.4f}): {_word(rel(r1_['t_rate'], t_half) <= TOL_G, 'agree', 'differ')}; fraction-carrier cut {r1_['t_occ']:.4f} vs the same: {_word(rel(r1_['t_occ'], t_half) <= TOL_G, 'agree', 'differ')} - the two carriers are two readings of the ingredient and they {_word(internal, 'differ', 'agree')}",
                    tn=f"the domain's half-life gives {t_half:.4f}: the fraction reading is the domain's definition; no theorem of the domain names two half-lives ({2.0 * t_half:.4f}, a quarter remaining); on second-order kinetics both readings give the domain's 1/k = {res[2]['t_rate']:.4f}",
                    tc="not reached: the two readings of the ingredient must agree before Q can be checked, and they agree only for second-order kinetics",
                    out=out,
                    reading=f"on the fraction carrier the pole-start cut is the half-life by the family's symmetry, as the source row said; on the rate carrier, which is what a counter records and the carrier the ledger's measles study scored, the same axiom cuts first-order decay at two half-lives ({r1_['N_rate']:.4f} remaining) and n-th order decay at 2^(-2/n) remaining, so the two carriers agree only for n = 2; the half-life is the domain's definition and one of the two readings, the other is a point the domain does not name; {out} until the carrier of a decay is fixed (A1 names 'a statistical manifold', not which); batch 01 row 3 found a second choice, the counting window, inside the rate carrier's unit, and the cut here is free of that one",
                    weakness=f"the pole-start half-arc is the sharp rows' reading of A3 on a carrier with no rotor (O3: nothing sets L), inherited here; the rate carrier's arc depends on the counting window Delta while its cut does not; the poles are reached only as t -> infinity, so the totals are the closed forms and the grid leaves at most {def_max:.4f} of arc beyond its end (third order, fraction carrier)")


# ---------------------------------------------------------------- 44 sharp [3] Michaelis-Menten / Hill: the receptor's own carrier
def _receptor(a, L=14.0, n=400001):
    """Binding polynomial Z = sum a_i S^i (a_0 = 1) over ln S in [-L, L]: ligation-state distribution p_i = a_i S^i / Z (the receptor's own
    carrier), fractional saturation Y = sum i p_i / m (the domain's carrier), the A3 pole-start cut at half the categorical arc, S_50 and
    Wyman's median ligand activity x_m = a_m^(-1/m)."""
    a = np.asarray(a, float); m = len(a) - 1
    u = np.linspace(-L, L, n); S = np.exp(u)
    P = np.array([a[i] * S ** i for i in range(m + 1)]).T
    P /= P.sum(axis=1, keepdims=True)
    Y = (P * np.arange(m + 1)).sum(axis=1) / m
    steps, cum, tot = _categorical_path(P, u)
    u_cut, i = _half_arc_point(u, cum, tot)
    speed = float(steps[i - 1] / (u[1] - u[0]))
    u50, _ = _half_arc_point(u, Y, 1.0)
    # reflection S -> x_m^2 / S maps p_i to p_(m-i) iff a_i a_m^(1 - 2 i / m) = a_(m-i) for every i (for m = 3: a_2 = a_1 a_3^(1/3))
    sym_gap = max(abs(a[i] * a[m] ** (1.0 - 2.0 * i / m) - a[m - i]) / max(a[i], a[m - i], 1e-300) for i in range(m + 1))
    return dict(S_cut=math.exp(u_cut), S50=math.exp(u50), xm=float(a[m] ** (-1.0 / m)), tot=tot, tot_inst=arc_length(2.0 * np.sqrt(P)),
                speed=speed, Y_cut=float(np.interp(u_cut, u, Y)), symmetric=bool(sym_gap < 1e-12))


def r4():
    models = {"MM, one site (a = 1, 1; K_M = 1)": (1, 1), "Hill n = 4, all-or-none (a = 1, 0, 0, 0, 1)": (1, 0, 0, 0, 1),
              "two sites, negative cooperativity (a = 1, 10, 1)": (1, 10, 1), "two sites, positive cooperativity (a = 1, 0.1, 1)": (1, 0.1, 1),
              "three independent sites (a = 1, 3, 3, 1)": (1, 3, 3, 1), "three sites, symmetric polynomial (a = 1, 10, 10, 1)": (1, 10, 10, 1),
              "three sites, asymmetric (a = 1, 10, 0.1, 1)": (1, 10, 0.1, 1), "three sites, asymmetric (a = 1, 3, 1, 1)": (1, 3, 1, 1),
              "four sites, asymmetric (a = 1, 10, 0.1, 0.1, 1)": (1, 10, 0.1, 0.1, 1)}
    R = {k: _receptor(v) for k, v in models.items()}
    sym = [k for k in R if rel(R[k]["S_cut"], R[k]["S50"]) <= 1e-6]
    asym = [k for k in R if rel(R[k]["S_cut"], R[k]["S50"]) > 1e-6]
    same_sets = set(sym) == {k for k in R if R[k]["symmetric"]}
    two = R["two sites, negative cooperativity (a = 1, 10, 1)"]; three = R["three sites, asymmetric (a = 1, 10, 0.1, 1)"]
    sub = outcome(crr=two["S_cut"], null=two["S50"], domain=two["xm"], check=True)
    check = len(asym) == 0
    out = outcome(crr=three["S_cut"], null=three["S50"], domain=three["S50"], check=check)
    numbers = "; ".join(f"{k}: cut {v['S_cut']:.4f}, S_50 {v['S50']:.4f}, x_m {v['xm']:.4f}, Y at the cut {v['Y_cut']:.4f}, arc {v['tot']:.4f}, Fisher speed at the cut {v['speed']:.4f} per e-fold of S" for k, v in R.items()) \
              + f"; cut = S_50 (within 1e-6) on {len(sym)} of {len(R)} models; binding polynomial reflection-symmetric (a_i a_m^(1 - 2i/m) = a_(m-i); for three sites a_2 = a_1 a_3^(1/3), i.e. K_2^2 = K_1 K_3 in sequential constants) on {sum(v['symmetric'] for v in R.values())} of {len(R)}; the two sets coincide: {same_sets}; the arc by the instrument on the MM model is {R['MM, one site (a = 1, 1; K_M = 1)']['tot_inst']:.4f} (pi less {math.pi - R['MM, one site (a = 1, 1; K_M = 1)']['tot_inst']:.4f} left beyond the grid ends)"
    return make_row("bio", "Ligand binding to a receptor with m sites, Adair binding polynomial Z(S) = sum a_i S^i: the receptor's own carrier is its ligation-state distribution p_i = a_i S^i / Z (categorical, m + 1 states), the domain's is the fractional saturation Y (Bernoulli); Michaelis-Menten is m = 1, the Hill equation is the all-or-none m-site member; constants illustrative, S_50 = 1 by choice of units where the polynomial is symmetric",
                    source="theory/retrodictions/sharp_claims.txt [3] (DESCR)",
                    Q="on the receptor's own carrier the A3 pole-start cut (half the Fisher-Rao arc from the empty to the full state) is the half-saturation constant for every receptor, which would make 'theta = 1/2 at K_M for every n' a fact of the receptor's geometry and not a definition on the fraction carrier",
                    ingredient="A3 as the sharp rows read it (cut at half the pole-to-pole arc), on the receptor's own categorical carrier (A1: the system's state is its distribution over its own states), D5",
                    null="the domain's carrier: the fractional saturation Y, whose half-point is K_M / K_half by definition",
                    domain="K_M (K_half) is defined as the half-saturation concentration; for two sites S_50 = a_2^(-1/2), the geometric mean of the sequential constants, which is also Wyman's median ligand activity x_m = a_m^(-1/m)",
                    numbers=numbers,
                    tg=f"three sites, asymmetric: cut {three['S_cut']:.4f} vs null (S_50) {three['S50']:.4f}: {_word(rel(three['S_cut'], three['S50']) <= TOL_G, 'agree', 'differ')}; two sites: cut {two['S_cut']:.4f} vs {two['S50']:.4f}: {_word(rel(two['S_cut'], two['S50']) <= TOL_G, 'agree', 'differ')} (sub-case label from outcome(cut, S_50, x_m): {sub})",
                    tn=f"the domain's constants for the asymmetric three-site receptor: S_50 {three['S50']:.4f} {_word(rel(three['S_cut'], three['S50']) <= TOL_N, 'agrees', 'differs')}, x_m {three['xm']:.4f} {_word(rel(three['S_cut'], three['xm']) <= TOL_N, 'agrees', 'differs')}: the domain does not name the receptor's own cut there",
                    tc=f"cut = S_50 on every model: {_word(check, 'holds', 'fails')} ({len(asym)} of {len(R)} models differ, the asymmetric ones; Y at the receptor's cut {three['Y_cut']:.4f} for a = 1, 10, 0.1, 1)",
                    out=out,
                    reading=f"on one and two sites, and on any receptor whose binding polynomial is reflection-symmetric about S_50, the receptor's own cut is the half-saturation point because the reflection S -> S_50^2 / S swaps the empty and full poles and fixes the arc's midpoint: the coincidence is the binding polynomial's symmetry, the domain's (S_50 = the geometric mean for two sites), and the sub-case label is {sub}; off that family the receptor's own cut leaves K_half ({three['S_cut']:.4f} against {three['S50']:.4f}) and leaves Wyman's median ({three['xm']:.4f}) too, landing at a point the domain does not name and nothing here can check; so 'theta = 1/2 at K_M for every n' is a definition on the fraction carrier that the receptor's own geometry reproduces only by symmetry: {out} for the universal Q",
                    weakness="the ligation-state distribution is one reading of the receptor's own carrier (an MWC receptor carries conformational states too, which would change the arc); the constants are illustrative, not fitted to any protein; the pole-start half-arc is the sharp rows' reading of A3 on a carrier with no rotor (O3), and on strongly stalled paths (negative cooperativity) the cut's location is fixed by the symmetry rather than resolved by the arc, so the Fisher speed at the cut is printed",
                    elegance="A grabber with two hands is exactly half full at one amount of ligand, however much the hands help or hinder each other: the geometric mean of the two grip strengths. A rule with no knobs, and it is the domain's; the picture stops at two hands.",
                    child="Imagine a toy with two hands that can each hold a ball, and a room with balls floating around. Whether the hands help each other or get in each other's way, there is one amount of balls in the room at which the toy is exactly half full, and you can work it out from the two grip strengths alone. With three hands that easy rule can stop working.")


# ---------------------------------------------------------------- 45 sharp [4] titration: the acid's own carrier
def _diprotic(pKa1, pKa2, n=400001, Ca=0.1, Kw=1e-14):
    pH = np.linspace(pKa1 - 8.0, pKa2 + 8.0, n); H = 10.0 ** (-pH); K1, K2 = 10.0 ** -pKa1, 10.0 ** -pKa2
    Z = 1.0 + K1 / H + K1 * K2 / H ** 2
    P = np.stack([1.0 / Z, (K1 / H) / Z, (K1 * K2 / H ** 2) / Z], axis=1)                # H2A, HA-, A2-: the acid's own carrier
    steps, cum, tot = _categorical_path(P, pH)
    pH_cut, i = _half_arc_point(pH, cum, tot)
    speed = float(steps[i - 1] / (pH[1] - pH[0]))
    nbar = P[:, 1] + 2.0 * P[:, 2]                                                     # mean ionisation, the source row's 'ionised fraction' x 2
    pH_nbar1, _ = _half_arc_point(pH, nbar, 2.0)
    mask = (pH > 0.0) & (pH < 14.0); pHt, Ht = pH[mask], H[mask]
    nb = (Kw / Ht - Ht + Ca * nbar[mask]) / Ca                                          # titration curve: equivalents of strong base per acid
    slope = np.gradient(pHt, nb)                                                       # dpH/dn_b; its local maxima are the equivalence points
    idx = np.where((slope[1:-1] > slope[:-2]) & (slope[1:-1] > slope[2:]))[0] + 1
    first = [(float(nb[j]), float(pHt[j]), float(slope[j])) for j in idx if 0.5 < nb[j] < 1.5]
    first = max(first, key=lambda z: z[2]) if first else None
    return dict(pH_cut=pH_cut, speed=speed, pH_nbar1=pH_nbar1, tot=tot, first=first, p1max=float(P[:, 1].max()), mid=0.5 * (pKa1 + pKa2))


def r5():
    pairs = {"pKa 2 and 10": (2.0, 10.0), "pKa 3 and 8": (3.0, 8.0), "pKa 4 and 5": (4.0, 5.0)}
    R = {k: _diprotic(*v) for k, v in pairs.items()}
    pKa = 4.76                                                                         # the source row's monoprotic acid
    pH1 = np.linspace(pKa - 8.0, pKa + 8.0, 400001); a1 = 1.0 / (1.0 + 10.0 ** (pKa - pH1))
    _, cum1, tot1 = _categorical_path(np.stack([1.0 - a1, a1], axis=1), pH1)
    pH_cut1, _ = _half_arc_point(pH1, cum1, tot1)
    wide = R["pKa 2 and 10"]; close = R["pKa 4 and 5"]
    H_cut, H_first, H_dom = 10.0 ** -wide["pH_cut"], 10.0 ** -wide["first"][1], 10.0 ** -wide["mid"]
    Ka1, Ka2, Ca, Kw = 10.0 ** -pairs["pKa 2 and 10"][0], 10.0 ** -pairs["pKa 2 and 10"][1], 0.1, 1e-14   # C_a and K_w as _diprotic uses them
    Ka1_over_C = Ka1 / Ca                                                            # the finite-concentration correction to the ampholyte pH
    H_exact = math.sqrt(Ka1 * (Ka2 * Ca + Kw) / (Ka1 + Ca))                           # exact ampholyte [H+]: sqrt(Ka1 (Ka2 C_a + K_w)/(Ka1 + C_a))
    check = all(abs(v["pH_cut"] - v["mid"]) < 1e-3 for v in R.values())
    out = outcome(crr=H_cut, null=H_first, domain=H_dom, check=check)
    numbers = "; ".join(f"{k}: species cut at pH {v['pH_cut']:.4f} (Fisher speed there {v['speed']:.4f} per pH unit, HA- peak fraction {v['p1max']:.4f}), (pKa1 + pKa2)/2 = {v['mid']:.4f}, mean ionisation 1 at pH {v['pH_nbar1']:.4f}, arc pole to pole {v['tot']:.4f}, "
                        + (f"first-equivalence inflection of the titration curve (C_a = 0.1 M, K_w = 1e-14) at n_b = {v['first'][0]:.4f}, pH {v['first'][1]:.4f} (dpH/dn_b = {v['first'][2]:.1f})" if v["first"] else "no local maximum of dpH/dn_b for n_b in (0.5, 1.5): the titration curve shows no first equivalence point")
                        for k, v in R.items()) + f"; monoprotic pKa {pKa:g} (the source row): cut at pH {pH_cut1:.4f}, arc {tot1:.4f} (pi less {math.pi - tot1:.4f} beyond the grid ends); [H+] at the wide pair's cut {H_cut:.4e} M, at its inflection {H_first:.4e} M, sqrt(Ka1 Ka2) = {H_dom:.4e} M, exact ampholyte [H+] at 0.1 M, sqrt(Ka1 (Ka2 C_a + K_w)/(Ka1 + C_a)) = {H_exact:.4e} M (Ka1/C_a = {Ka1_over_C:.4f})"
    return make_row("chem", "Diprotic acid H2A on its own carrier, the species distribution (H2A, HA-, A2-) over pH, for three pKa pairs, against the source row's ionised-fraction carrier and the titration curve n_b(pH) of 0.1 M acid with strong base; the source row's monoprotic acid (pKa 4.76) beside it",
                    source="theory/retrodictions/sharp_claims.txt [4] (DESCR)",
                    Q="the acid's own cut (A3 pole-start on its species distribution, from all-H2A to all-A2-) is the pH at which it is the ampholyte, (pKa1 + pKa2)/2, for every pair of pKa's, including pairs so close that the titration curve shows no first equivalence point",
                    ingredient="A3 as the sharp rows read it (cut at half the pole-to-pole arc) on the acid's own categorical carrier (A1), D5",
                    null="the domain's extremum landmark: the first equivalence point as the local maximum of dpH/dn_b on the titration curve (a peak cut), in [H+]",
                    domain="pH of the amphiprotic species = (pKa1 + pKa2)/2, i.e. [H+] = sqrt(Ka1 Ka2) (the standard first-equivalence-point formula)",
                    numbers=numbers,
                    tg=f"[H+] at the species cut {H_cut:.4e} vs null (the titration inflection) {H_first:.4e} for pKa 2 and 10: {_word(rel(H_cut, H_first) <= TOL_G, 'agree', 'differ')} (relative gap {rel(H_cut, H_first):.3f}: the inflection sits within {rel(H_first, H_exact):.1e} of the exact ampholyte [H+] {H_exact:.4e}, which the finite-concentration term Ka1/C_a = {Ka1_over_C:.4f} moves off sqrt(Ka1 Ka2)); for pKa 4 and 5 the null does not exist and the cut is at pH {close['pH_cut']:.4f}",
                    tn=f"sqrt(Ka1 Ka2) = {H_dom:.4e}: {_word(rel(H_cut, H_dom) <= TOL_N, 'the domain has Q', 'the domain does not give Q')}",
                    tc=f"cut within 1e-3 pH of (pKa1 + pKa2)/2 on all {len(R)} pairs: {_word(check, 'holds', 'fails')} (and it is the reflection symmetry pH -> pKa1 + pKa2 - pH of the species distribution, which swaps H2A and A2-; the mean-ionisation carrier gives the same point by the same symmetry)",
                    out=out,
                    reading=f"the acid's own cut is the ampholyte pH, the domain's first-equivalence-point formula, for every pair; it exists for the close pair where the titration curve has no first equivalence inflection, and the domain's formula holds there too, because both rest on the same reflection symmetry of the species distribution; the monoprotic case (cut at pH {pH_cut1:.4f} = pKa) is the definition the source row named, the diprotic case is the domain's theorem: {out}",
                    weakness="a triprotic acid with unequally spaced pKa's (pKa2 not the mean of pKa1 and pKa3) is the asymmetric three-site receptor of row 4, where the species cut leaves every domain landmark; C_a and K_w enter only the null; at wide spacing the cut lies on the HA- plateau (Fisher speed printed) and its location is fixed by the symmetry rather than resolved by the arc",
                    elegance="Giving away the first proton and taking back the second are mirror images, so the in-between form of a two-proton acid sits exactly halfway between its two pKa's, whatever they are. A picture with no knobs, and it is the domain's.",
                    child="A two-proton acid can give away two hydrogen 'balls'. Letting go of the first and getting the second back are mirror images of each other, so the moment when it holds exactly one ball is exactly halfway between the two sourness levels where each ball comes off. That is true for every such acid, so you never need to look it up.")


def main():
    return run_batch("Synthesis batch 09: rows 41-45 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
