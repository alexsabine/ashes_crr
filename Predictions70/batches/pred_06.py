"""PRED70 batch P06: physics, rows P06-1..P06-5 of Predictions70/declared.py (declared at commit 8397478, prompt-log
entry 234, before any model existed). Q, the null, H0 and the forecast are imported from declared.py and printed verbatim;
the model details declared.py leaves open (rates, amplitudes, step sizes, horizons, seeds) are chosen here and printed.
  [1] P06-1 Kuramoto model, N = 200, Lorentzian frequencies, with an A6-remembered mean field (critical coupling)
  [2] P06-2 mean-field Ising with Glauber dynamics and an A6-remembered magnetisation in the field (critical temperature)
  [3] P06-3 radioactive decay chain A -> B -> C: B decays in natural time (H-L5)
  [4] P06-4 driven damped pendulum at resonance: energy dissipated per occasion between antipodal cuts (D5)
  [5] P06-5 flashing Brownian ratchet switched at antipodal cuts of the particle's phase (A3)
Deterministic (fixed seeds, fixed grids, explicit RK4 / Euler-Maruyama), no data files, no network. Every verdict word is
computed from the numbers (R15). Literature named by name and year only (R10): Kuramoto 1975; Ott and Antonsen 2008;
Glauber 1963; Varotsos et al. 2002 (natural time); Cao, Dinis and Parrondo 2004.
Run: uv run python Predictions70/batches/pred_06.py > Predictions70/batches/pred_06.txt
"""
import math
import os
import sys

import numpy as np

from crr.instrument.core import antipodal_cuts, intrinsic_phase, poisson_transform, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P as DECLARED  # noqa: E402

DECL = {p[0]: dict(id=p[0], batch=p[1], cls=p[2], system=p[3], ingredient=p[4], Q=p[5], null=p[6], H0=p[7], forecast=p[8])
        for p in DECLARED}
Q_GRID = (0.25, 0.5, 0.75)          # A6 sensitivity grid (q = 0.5 decides)


def _w(cond, yes, no):
    return yes if cond else no


def _src(D):
    return f"PRED70 {D['id']} (declared at 8397478; forecast {D['forecast']})"


def _qh(check):
    return "-> not computable" if check is None else _w(check, "-> Q holds", "-> Q fails")


# ---------------------------------------------------------------- [1] P06-1 Kuramoto with a remembered mean field
KU_N, KU_G = 200, 1.0
KU_W = KU_G * np.tan(math.pi * (np.arange(KU_N) + 0.5) / KU_N - math.pi / 2)      # deterministic Lorentzian quantiles, centre 0


def _tm(q, gamma=KU_G):
    return (math.pi / gamma) * q / (1 - q)            # mean age q/(1-q) occasions; an occasion = half a turn at frequency gamma


def _kuramoto_r(K, Tm, dt=0.01, t_tr=150.0, t_ms=150.0, seed=0):
    rng = np.random.default_rng(seed); th = rng.uniform(0, 2 * math.pi, KU_N); M = np.mean(np.exp(1j * th))
    def f(th, M):
        Z = np.mean(np.exp(1j * th)); fld = Z if Tm == 0 else M
        return KU_W + K * np.imag(fld * np.exp(-1j * th)), (0.0 if Tm == 0 else (Z - M) / Tm)
    n_tr, n_ms = int(round(t_tr / dt)), int(round(t_ms / dt)); rs = []
    for k in range(n_tr + n_ms):
        a1, b1 = f(th, M); a2, b2 = f(th + 0.5 * dt * a1, M + 0.5 * dt * b1); a3, b3 = f(th + 0.5 * dt * a2, M + 0.5 * dt * b2)
        a4, b4 = f(th + dt * a3, M + dt * b3)
        th = th + dt * (a1 + 2 * a2 + 2 * a3 + a4) / 6; M = M + dt * (b1 + 2 * b2 + 2 * b3 + b4) / 6
        if k >= n_tr:
            rs.append(abs(np.mean(np.exp(1j * th))))
    return float(np.mean(rs))


def _kc_est(Tm, Ks=(3.0, 4.0, 5.0)):
    r = {K: _kuramoto_r(K * KU_G, Tm) for K in Ks}
    return float(np.mean([K * KU_G * (1 - r[K] ** 2) for K in Ks])), r        # Lorentzian (Ott-Antonsen): r^2 = 1 - Kc/K


def _kc_oa(Tm, omega0, gamma=KU_G, grid=np.arange(0.001, 20.0 + 1e-12, 0.001)):
    """Linear threshold of the incoherent state in the Ott-Antonsen reduction, memory taken in a frame where the
    frequency centre is omega0: z' = (i omega0 - gamma) z + (K/2) M, M' = (z - M)/Tm (M = z when Tm = 0)."""
    for K in grid:
        if Tm == 0:
            lam = np.array([1j * omega0 - gamma + K / 2])
        else:
            lam = np.linalg.eigvals(np.array([[1j * omega0 - gamma, K / 2], [1 / Tm, -1 / Tm]], complex))
        if lam.real.max() >= 0:
            return float(K)
    return float("inf")


def r1():
    D = DECL["P06-1"]
    null, rn = _kc_est(0.0)
    est = {q: _kc_est(_tm(q)) for q in Q_GRID}
    crr, rm = est[0.5]; domain = 2 * KU_G
    check = crr > null * (1 + TOL_G)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    oa0 = _kc_oa(_tm(0.5), 0.0); oa_n = _kc_oa(0.0, 0.0); oa1 = {q: _kc_oa(_tm(q), 1.0) for q in Q_GRID}
    oa_rot = oa1[0.5] > oa_n * (1 + TOL_G)
    return make_row(D["cls"], D["system"] + f" [model: d theta_j/dt = omega_j + K Im(F e^(-i theta_j)), N = {KU_N}, omega_j the deterministic Lorentzian quantiles (centre 0, half-width gamma = {KU_G:g}); F = Z (null) or the remembered field dM/dt = (Z - M)/T_m (A6, P3 exponential kernel, mean age q/(1-q) occasions, an occasion = half a turn at frequency gamma, T_m = {_tm(0.5):.4f} at q = 0.5); RK4 dt 0.01, 150 time units discarded, 150 averaged; seed 0 initial phases]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: Kc estimated at N = 200 from the time-averaged order parameter by the Lorentzian law r^2 = 1 - Kc/K at K = 3, 4, 5 gamma; memory raises Kc if the estimate exceeds the instantaneous-field estimate at the same N by more than TOL_G)",
                    ingredient=D["ingredient"] + ": the oscillators couple to the A6-remembered mean field M instead of the instantaneous Z",
                    null=D["null"] + " (computed as: the same estimator with F = Z)",
                    domain=D["H0"] + f" (computed as: Kc = 2 gamma = {domain:g})",
                    numbers=(f"Kc estimate: remembered field {crr:.4f} (r = " + ", ".join(f"{rm[K]:.4f}" for K in (3.0, 4.0, 5.0)) + f" at K = 3, 4, 5), instantaneous {null:.4f} (r = "
                             + ", ".join(f"{rn[K]:.4f}" for K in (3.0, 4.0, 5.0)) + f"), 2 gamma = {domain:g}; q grid: " + ", ".join(f"q = {q:g} (T_m {_tm(q):.3f}): {est[q][0]:.4f}" for q in Q_GRID)
                             + f"; Ott-Antonsen linear threshold (N -> infinity): memory {oa0:.3f}, instantaneous {oa_n:.3f}; with the frequency centre at omega0 = 1 in the frame where memory acts: "
                             + ", ".join(f"q = {q:g}: {oa1[q]:.3f}" for q in Q_GRID) + f" (instantaneous {oa_n:.3f})"),
                    tg=f"Kc {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (relative {rel(crr, null):.4f})",
                    tn=f"Kc = 2 gamma = {domain:g}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')} (relative {rel(crr, domain):.4f})",
                    tc=f"memory raises Kc by more than 1 %: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"with the frequencies centred at zero the locked mean field is static, a remembered static field is the field itself, and the incoherent state loses stability "
                             f"where it did (N -> infinity: {oa0:.3f} against {oa_n:.3f}); at N = 200 the estimates are {crr:.4f} and {null:.4f}; memory {_w(oa_rot, 'raises', 'does not raise')} the threshold "
                             f"only when the ensemble rotates in the frame where the memory is taken ({oa1[0.5]:.3f} at omega0 = 1): a low-pass filter on a rotating field lags and shrinks it, the filtered/delayed-coupling result"),
                    weakness="declared.py does not name the frequency centre; the Kuramoto convention (centre 0) was chosen and decides the verdict, since a remembered field breaks the model's rotation invariance (the omega0 = 1 threshold is printed); the N = 200 estimator uses the N -> infinity Lorentzian law",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] P06-2 mean-field Ising with a remembered magnetisation
IS_J, IS_Z = 1.0, 4


def _ising_tc(q, grid=np.arange(2.0, 6.0 + 1e-12, 1e-4)):
    """Largest temperature at which m = 0 is unstable (scan upward; the first stable T is Tc)."""
    Tm = q / (1 - q)
    for T in grid:
        a = IS_J * IS_Z / T
        lam = np.array([a - 1.0]) if Tm == 0 else np.linalg.eigvals(np.array([[-1.0, a], [1 / Tm, -1 / Tm]]))
        if lam.real.max() < 0:
            return float(T)
    return float("inf")


def _ising_m(q, T, m0=0.01, dt=0.01, tmax=400.0):
    Tm = q / (1 - q); m = M = m0; a = IS_J * IS_Z / T
    f = lambda m, M: (-m + math.tanh(a * (m if Tm == 0 else M)), 0.0 if Tm == 0 else (m - M) / Tm)
    for _ in range(int(round(tmax / dt))):
        k1 = f(m, M); k2 = f(m + 0.5 * dt * k1[0], M + 0.5 * dt * k1[1]); k3 = f(m + 0.5 * dt * k2[0], M + 0.5 * dt * k2[1]); k4 = f(m + dt * k3[0], M + dt * k3[1])
        m += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; M += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
    return m


def r2():
    D = DECL["P06-2"]
    tcs = {q: _ising_tc(q) for q in Q_GRID}; crr = tcs[0.5]; null = _ising_tc(0.0); domain = IS_J * IS_Z
    Tlow = 0.9 * domain
    mstar = 0.5                                                                 # Newton on m = tanh(m Tc/T)
    for _ in range(100):
        g = mstar - math.tanh(mstar * domain / Tlow); dg = 1 - (domain / Tlow) / math.cosh(mstar * domain / Tlow) ** 2; mstar -= g / dg
    mm = _ising_m(0.5, Tlow); m0 = _ising_m(0.0, Tlow); mhi = _ising_m(0.5, 1.05 * domain); mhi0 = _ising_m(0.0, 1.05 * domain)
    check = rel(crr, null) <= TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row(D["cls"], D["system"] + f" [model: Curie-Weiss Glauber equation dm/dt = -m + tanh(J z M_e / T), J = {IS_J:g}, z = {IS_Z}, k_B = 1; M_e = m (null) or the remembered magnetisation dM/dt = (m - M)/T_m, T_m = q/(1-q) Glauber time units (an occasion = one sweep, the Glauber time unit); Tc by the linear stability of m = 0 on a 1e-4 grid; RK4 dt 0.01 over 400 time units for the ordered state]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: Tc with memory within TOL_G of Tc without)",
                    ingredient=D["ingredient"] + ": the local field is built from the A6-remembered magnetisation",
                    null=D["null"] + " (computed as: the same scan with M_e = m)",
                    domain=D["H0"] + f" (computed as: J z = {domain:g})",
                    numbers=(f"Tc: memory (q = 0.5) {crr:.4f}, instantaneous {null:.4f}, J z {domain:g}; q grid: " + ", ".join(f"q = {q:g}: {tcs[q]:.4f}" for q in Q_GRID)
                             + f"; ordered state at T = {Tlow:.2f}: memory m = {mm:.8f}, instantaneous {m0:.8f}, the mean-field root {mstar:.8f}; at T = {1.05 * domain:.2f}: memory m = {mhi:.2e}, instantaneous {mhi0:.2e}"),
                    tg=f"Tc {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"J z = {domain:g}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"Tc unchanged by memory (within 1 %): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"the remembered magnetisation equals the magnetisation at every fixed point, so the self-consistency m = tanh(Jz m/T) and its bifurcation at T = Jz are untouched "
                             f"(Tc {crr:.4f} with memory, {null:.4f} without); the 2x2 Jacobian at m = 0 has trace -1 - 1/T_m < 0 and determinant (1 - Jz/T)/T_m, so the only crossing is the pitchfork at Jz; "
                             f"memory changes how fast the magnet relaxes (at T = {1.05 * domain:.2f}, after 400 time units, the remembered run is at m = {mhi:.2e}, the instantaneous at {mhi0:.2e}: {_w(abs(mhi) > abs(mhi0), 'slower', 'not slower')}), not whether or where it orders"),
                    weakness="the mean-field equation only (no finite-N Monte Carlo); the result follows from the fixed-point algebra, and the scan confirms it",
                    elegance="Remembering the magnet's recent past changes how quickly it settles, but not the temperature at which it can hold a direction at all, because at rest the memory and the present agree.",
                    child="Tiny magnets that copy what their neighbours were doing a moment ago end up agreeing at exactly the same temperature as magnets that copy what their neighbours are doing now; they just take a little longer to get there.")


# ---------------------------------------------------------------- [3] P06-3 decay chain in natural time
def r3():
    D = DECL["P06-3"]
    kA, kB, NA0, nB_target, dt = 0.05, 0.5, 400, 300, 2e-5
    rng = np.random.default_rng(0); t = 0.0; NA, NB = NA0, 0; ev_t, ev_nb = [], []; nb_path = [(0.0, 0)]
    while len(ev_t) < nB_target and (NA + NB) > 0:
        ra, rb = kA * NA, kB * NB; rt = ra + rb
        t += rng.exponential(1.0 / rt)
        if rng.random() < ra / rt:
            NA -= 1; NB += 1
        else:
            NB -= 1; ev_t.append(t)
        nb_path.append((t, NB))
    ev_t = np.array(ev_t); n_s = int(math.ceil(ev_t[-1] / dt)) + 2
    idx = np.round(ev_t / dt).astype(int); coll = int(len(idx) - len(np.unique(idx)))
    count = np.zeros(n_s); np.add.at(count, idx, 1.0); count = np.cumsum(count)          # natural time: B decays so far
    tp = np.array([p[0] for p in nb_path]); nbv = np.array([p[1] for p in nb_path], float)
    grid_t = np.arange(n_s) * dt; nb_grid = nbv[np.searchsorted(tp, grid_t, side="right") - 1]
    reg = regularity(count, idx, sigma=1.0, dt=dt, n_boot=2000, seed=0)
    reg_rate = regularity(poisson_transform(kB * nb_grid), idx, sigma=1.0, dt=dt, n_boot=2000, seed=0)
    crr, null, domain = reg["cv_arc"], reg["cv_clock"], 0.0
    lo, hi = reg["ci95"]
    check = crr < null and hi < 0
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    rate_lo, rate_hi = reg_rate["ci95"]
    rate_win = reg_rate["cv_arc"] < reg_rate["cv_clock"] and rate_hi < 0
    return make_row(D["cls"], D["system"] + f" [model: exact stochastic simulation (Gillespie), k_A = {kA:g}, k_B = {kB:g}, N_A(0) = {NA0}, N_B(0) = 0, seed 0, the first {nB_target} B decays; carriers sampled on a {dt:g} grid ({coll} B decays share a sample)]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: regularity() on the natural-time carrier, the count of B decays, with the B decays as events: CV(natural-time increment) < CV(clock interval) with the paired-bootstrap 95 % CI (n_boot 2000, seed 0) excluding 0)",
                    ingredient=D["ingredient"] + ": the change accumulated between the system's own events, here natural time (the event count)",
                    null=D["null"] + " (computed as: CV of the clock time between consecutive B decays)",
                    domain=D["H0"] + " (computed as: CV of the natural-time increment = 0)",
                    numbers=(f"{reg['n']} occasions; CV natural time {crr:.6f}, CV clock {null:.4f}, difference {reg['diff']:.4f}, 95 % CI [{lo:.4f}, {hi:.4f}]; "
                             f"H-L5's rate reading (Fisher-Rao arc of the B-decay rate k_B N_B, poisson_transform): CV(arc) {reg_rate['cv_arc']:.4f}, CV(clock) {reg_rate['cv_clock']:.4f}, CI [{rate_lo:.4f}, {rate_hi:.4f}] "
                             f"({_w(rate_win, 'the arc is more regular', 'the arc is not more regular')})"),
                    tg=f"CV {crr:.6f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"natural time is uniform by construction, CV {domain:g}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"CV natural {crr:.6f} < CV clock {null:.4f} with the CI excluding 0: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"counted in its own events the decay chain advances by exactly one unit per B decay, so the natural-time increment has CV {crr:.6f} by construction, "
                             f"while the clock intervals of a Poisson-like process have CV {null:.4f}; the prediction holds and is the definition of natural time; "
                             f"the Fisher arc of the decay rate between decays, the reading H-L5 uses on rate carriers, {_w(rate_win, 'is also', 'is not')} more regular than the clock"),
                    weakness="a count carrier makes Q definitional: any point process is uniform in its own event count; the rate-arc reading is the non-trivial one and is printed, not decisive",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] P06-4 driven damped pendulum: dissipation per occasion
def r4():
    D = DECL["P06-4"]
    gam, A, om = 0.1, 0.02, 1.0
    Td = 2 * math.pi / om; spp = 500; dt = Td / spp; n_tr, n_ms = 150 * spp, 205 * spp
    f = lambda t, x, v: (v, -gam * v - math.sin(x) + A * math.cos(om * t))
    x, v, t = 0.0, 0.0, 0.0; X = np.empty(n_ms + 1); V = np.empty(n_ms + 1); tt = np.empty(n_ms + 1)
    for k in range(n_tr + n_ms):
        if k >= n_tr:
            X[k - n_tr], V[k - n_tr], tt[k - n_tr] = x, v, t
        a1 = f(t, x, v); a2 = f(t + dt / 2, x + dt / 2 * a1[0], v + dt / 2 * a1[1]); a3 = f(t + dt / 2, x + dt / 2 * a2[0], v + dt / 2 * a2[1])
        a4 = f(t + dt, x + dt * a3[0], v + dt * a3[1])
        x += dt * (a1[0] + 2 * a2[0] + 2 * a3[0] + a4[0]) / 6; v += dt * (a1[1] + 2 * a2[1] + 2 * a3[1] + a4[1]) / 6; t += dt
    X[-1], V[-1], tt[-1] = x, v, t
    diss = gam * V * V; cumD = np.concatenate([[0.0], np.cumsum(0.5 * (diss[1:] + diss[:-1]) * dt)])
    work = A * np.cos(om * tt) * V; cumW = np.concatenate([[0.0], np.cumsum(0.5 * (work[1:] + work[:-1]) * dt)])
    ph = intrinsic_phase(X); cuts = antipodal_cuts(ph)
    mono = bool(np.all(np.diff(ph) > 0))
    targets = ph[0] + math.pi * np.arange(len(cuts))
    tc = np.interp(targets, ph, tt) if mono else tt[cuts]                     # sub-sample crossing times of the half-turns
    tc = tc[5:-5]                                                             # drop the Hilbert edge occasions
    Docc = np.diff(np.interp(tc, tt, cumD)); occ_len = float(np.mean(np.diff(tc)))
    def per(Delta):
        e = np.arange(tc[0], tc[-1] + 1e-12, Delta); return np.diff(np.interp(e, tt, cumD))
    Dclk = per(1.0); Dper = per(Td); Dhalf = per(occ_len)
    ratio = lambda a: float(a.max() / a.min())
    crr, null, domain = ratio(Docc), ratio(Dclk), ratio(Dper)
    e = np.arange(tc[0], tc[-1] + 1e-12, Td); Wper = np.diff(np.interp(e, tt, cumW)); bal = float(np.max(np.abs(Wper / Dper - 1)))
    Wocc = np.diff(np.interp(tc, tt, cumW)); bal_occ = float(np.max(np.abs(Wocc / Docc - 1)))
    check = crr - 1 <= TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row(D["cls"], D["system"] + f" [model: theta'' + {gam:g} theta' + sin theta = {A:g} cos({om:g} t), the drive at the small-amplitude natural frequency; RK4 {spp} steps per drive period, 150 periods discarded, 205 recorded; occasions between antipodal_cuts of intrinsic_phase(theta), crossing times interpolated on the phase, 5 occasions dropped at each end]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: max/min of the dissipated energy gamma * integral theta'^2 dt over the steady-state occasions <= 1 + TOL_G)",
                    ingredient=D["ingredient"] + ": the interval between consecutive antipodal cuts of the pendulum's analytic-signal phase",
                    null=D["null"] + " (computed as: the same max/min over consecutive clock intervals of 1 time unit)",
                    domain=D["H0"] + " (computed as: the same max/min over consecutive drive periods)",
                    numbers=(f"{len(Docc)} occasions (mean length {occ_len:.5f}, half the drive period {Td / 2:.5f}; phase monotone: {mono}); dissipation per occasion max/min {crr:.8f}; "
                             f"per clock interval of 1: {null:.5f}; per drive period: {domain:.8f}; per clock interval equal to the mean occasion length: {ratio(Dhalf):.8f}; "
                             f"energy balance: max |W/D - 1| per drive period {bal:.2e}, per occasion {bal_occ:.2e}"),
                    tg=f"max/min {crr:.8f} vs null {null:.5f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"per drive period {domain:.8f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"dissipation per occasion constant within 1 %: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"in the periodic steady state every drive period dissipates the same energy, and the symmetric orbit makes every half-period do so too, so the occasions "
                             f"(half-turns, mean length {occ_len:.5f}) are as constant ({crr:.8f}) as the periods ({domain:.8f}), while clock intervals of 1 are not ({null:.5f}); "
                             f"a clock interval equal to the half-period is as constant as the occasion ({ratio(Dhalf):.8f}): the occasion is the drive's own half-period"),
                    weakness="one weakly nonlinear operating point (amplitude about 0.2 rad); the clock-interval length of the null is a choice (1 time unit; the half-period reading is printed)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] P06-5 flashing ratchet switched at antipodal cuts
RT_A, RT_V0, RT_D, RT_DT = 1.0 / 3.0, 5.0, 1.0, 2e-3        # sawtooth: minimum at 0, maximum at a, period 1, height V0 (kT = 1)


def _force(x):
    u = x - np.floor(x)
    return np.where(u < RT_A, -RT_V0 / RT_A, RT_V0 / (1 - RT_A))


def _ratchet(mode, H, n=400, seed=0, t_on=None, t_off=None, record=False):
    rng = np.random.default_rng(seed); steps = int(round(H / RT_DT)); x = np.zeros(n)
    on = np.zeros(n, bool); target = x + 0.5; tr = [] if record else None; sw = [] if record else None
    s = math.sqrt(2 * RT_D * RT_DT)
    for k in range(steps):
        if mode == "periodic":
            ph = (k * RT_DT) % (t_on + t_off); on[:] = ph >= t_off
        elif mode == "cdp":
            u = x - np.floor(x); on = u > RT_A
        x = x + np.where(on, _force(x), 0.0) * RT_DT + s * rng.standard_normal(n)
        if mode == "cut":
            hit = x >= target                                                  # the ring phase 2 pi x has advanced half a turn
            while np.any(hit):
                on = np.where(hit, ~on, on); target = np.where(hit, target + 0.5, target)
                if record and hit[0]:
                    sw.append(k + 1)
                hit = x >= target
        if record:
            tr.append(x[0])
    return float(np.mean(x) / H), (np.array([0.0] + tr) if record else None), sw


def r5():
    D = DECL["P06-5"]
    H = 50.0; TON = (0.02, 0.05, 0.1, 0.2); TOFF = (0.02, 0.05, 0.1, 0.2)
    per = {(a, b): _ratchet("periodic", H, t_on=a, t_off=b)[0] for a in TON for b in TOFF}
    best = max(per, key=per.get); null = per[best]
    crr, tr, sw = _ratchet("cut", H, record=True)
    cdp = _ratchet("cdp", H)[0]
    vH = {h: _ratchet("cut", h)[0] for h in (12.5, 25.0)}
    cuts = antipodal_cuts(2 * math.pi * tr)[1:]
    n_match = sum(1 for c in cuts if np.min(np.abs(np.array(sw) - c)) <= 1) if len(sw) else 0
    check = crr > null
    out = outcome(crr=crr, null=null, domain=cdp, check=check)
    edge = best[0] in (TON[0], TON[-1]) or best[1] in (TOFF[0], TOFF[-1])
    return make_row(D["cls"], D["system"] + f" [model: overdamped dx = F(x) s(t) dt + sqrt(2D dt) N(0,1), D = kT = 1, sawtooth of period 1, height {RT_V0:g} kT, maximum at a = 1/3 (minimum at 0); Euler-Maruyama dt {RT_DT:g}, 400 independent particles from x = 0, horizon {H:g}; drift velocity = mean displacement / horizon, seed 0]",
                    source=_src(D),
                    Q=D["Q"] + " (computed as: the potential toggles each time the particle's ring phase 2 pi x has advanced by pi since the last cut, oriented, the target moving by exactly half a turn; drift velocity above the best periodic on/off schedule)",
                    ingredient=D["ingredient"] + ": the cut on the particle's rotor (position modulo the period), fired at every forward half-turn",
                    null=D["null"] + f" (computed as: the best of t_on in {{{', '.join(f'{a:g}' for a in TON)}}} x t_off in {{{', '.join(f'{b:g}' for b in TOFF)}}})",
                    domain=D["H0"] + " (computed as: the drift velocity of the Cao-Dinis-Parrondo single-particle feedback, potential on iff the force on the particle is forward)",
                    numbers=(f"drift velocity: antipodal switching {crr:.4f} (horizon 12.5: {vH[12.5]:.4f}, 25: {vH[25.0]:.4f}, 50: {crr:.4f}); best periodic {null:.4f} at t_on = {best[0]:g}, t_off = {best[1]:g} "
                             f"({_w(edge, 'on the edge of the grid', 'inside the grid')}); feedback (Cao-Dinis-Parrondo) {cdp:.4f}; "
                             f"instrument check on particle 0: antipodal_cuts of its ring phase {len(cuts)}, online switches {len(sw)}, matched within one step {n_match}"),
                    tg=f"v {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the feedback ratchet {cdp:.4f}: {_w(rel(crr, cdp) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"antipodal switching faster than the best periodic schedule: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=(f"switching at the forward half-turns makes each completed on/off cycle advance one period (on at x = n + 1/2, where the force is forward, off on reaching the next minimum), "
                             f"but the off phase waits for a free diffusion to reach half a period ahead, whose mean first-passage time is infinite, so the velocity falls with the horizon "
                             f"({vH[12.5]:.4f}, {vH[25.0]:.4f}, {crr:.4f}); the rule {_w(check, 'beats', 'loses to')} the best periodic schedule ({null:.4f}) at this horizon, and the feedback ratchet, which switches on as soon as the force is forward "
                             f"and so never lets the particle wander back, reaches {cdp:.4f}"),
                    weakness=("DEVIATION: the phase is the particle's position on the ring (A3's rotor with L the potential period), not the analytic-signal phase of intrinsic_phase, which is "
                              "non-causal and has no meaning for a drifting random walk; the cut logic is antipodal_cuts' (oriented, the target advances by exactly half a turn) and is checked against "
                              "antipodal_cuts on one recorded trajectory. The velocity of the rule depends on the horizon (printed); one potential shape and height"),
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P06: physics (prompt-log entry 234; Predictions70/DECLARATION.md, declared at 8397478)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
