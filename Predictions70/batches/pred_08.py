"""PRED70 batch P08: ecology and evolution (Predictions70/DECLARATION.md; prompt-log entry 234). Five declared rows, read
from Predictions70/declared.py (pushed at 8397478 before any model existed); Q, null and H0 are printed verbatim.
[1] P08-1 Rosenzweig-MacArthur predator-prey with the predators' numerical response on A6-remembered prey (A6);
[2] P08-2 MacArthur-Wilson island biogeography with immigration from an A6-remembered species pool (A6);
[3] P08-3 Wright-Fisher drift, N = 100, conditioned on fixation: the Fisher-Rao arc of the frequency path (A1');
[4] P08-4 host-parasite matching-alleles (Red Queen) cycles with drift and mutation: arc per cycle (H-L5);
[5] P08-5 logistic harvest with the quota set on A6-remembered stock: overshoot in the recovery (A6).
A6 in continuous time: the remembered quantity M obeys dM/dt = (X - M)/T with T = Delta/ln(1/q), so the weight on the
past falls by q per occasion of length Delta (P3's geometric weights on a continuous clock); q = 0.5 decides, the grid
q in {0.25, 0.5, 0.75} is printed as a sensitivity only. Every number printed is computed here (R1); every verdict word is
an f-string of a comparison (R15). No data file, no network. Deterministic: fixed seeds, fixed grids, explicit RK4 on a
fixed dt (Euler-Maruyama for the noisy row). Literature named by name and year only (R10): Rosenzweig and MacArthur 1963;
Rosenzweig 1971; MacDonald 1978; MacArthur and Wilson 1963, 1967; Wright 1931; Fisher 1930; Kimura and Ohta 1969;
Hamilton 1980; Clark 1976. Run:
  uv run python Predictions70/batches/pred_08.py
"""
import math
import os
import sys

import numpy as np

from crr.instrument.core import arc_length, cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P  # noqa: E402

DECL = {p[0]: p for p in P}
N_BOOT, SEED_BOOT = 2000, 0                                                   # H-L5 margins (DECLARATION: n_boot 2000, seed 0)
Q_DECIDE, Q_GRID = 0.5, (0.25, 0.5, 0.75)


def _w(cond, yes, no):
    return yes if cond else no


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


def qtail(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _ci(ci):
    return "CI below 0" if ci[1] < 0.0 else ("CI above 0" if ci[0] > 0.0 else "CI includes 0")


def src(pid):
    return f"PRED70 {pid} (declared at 8397478; forecast {DECL[pid][8]})"


def _f(v, nd=6):
    """A value at round-off prints in exponent form, never as -0.000000."""
    return f"{v:.1e}" if abs(v) < 10.0 ** (-nd - 1) else f"{v:.{nd}f}"


def t_mem(q, occasion):
    return occasion / math.log(1.0 / q)


A6_NOTE = "A6 with P3 weights on a continuous clock: dM/dt = (X - M)/T, T = Delta/ln(1/q), q = 0.5 per occasion Delta"


# ---------------------------------------------------------------- [1] P08-1 Rosenzweig-MacArthur, remembered prey
RM = dict(r=1.0, a=1.0, h=1.0, e=0.5, m=0.2)


def _rm_J(K, T):
    r, a, h, e, m = (RM[k] for k in ("r", "a", "h", "e", "m"))
    Ns = m / (a * (e - m * h)); P_ = r * (1 - Ns / K) * (1 + a * h * Ns) / a
    dNN = r * (1 - 2 * Ns / K) - a * P_ / (1 + a * h * Ns) ** 2; dNP = -a * Ns / (1 + a * h * Ns); dPX = e * a * P_ / (1 + a * h * Ns) ** 2
    if T == 0.0:
        return np.array([[dNN, dNP], [dPX, 0.0]])
    return np.array([[dNN, dNP, 0.0], [0.0, 0.0, dPX], [1.0 / T, 0.0, -1.0 / T]])


def _rm_KH(T, step=1e-3, Kmax=20.0):
    Ns = RM["m"] / (RM["a"] * (RM["e"] - RM["m"] * RM["h"]))
    g = lambda K: float(np.linalg.eigvals(_rm_J(K, T)).real.max())
    Ks = np.arange(Ns + step, Kmax, step); lo = hi = None
    for i, K in enumerate(Ks):
        if g(K) >= 0.0:
            lo, hi = float(Ks[i - 1]), float(K); break
    if lo is None:
        return float("inf")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if g(mid) < 0.0 else (lo, mid)
    return 0.5 * (lo + hi)


def r1():
    pid = "P08-1"; d = DECL[pid]; occ = 1.0 / RM["r"]
    Ns = RM["m"] / (RM["a"] * (RM["e"] - RM["m"] * RM["h"])); closed = 1.0 / (RM["a"] * RM["h"]) + 2.0 * Ns
    k0 = _rm_KH(0.0); grid = {q: _rm_KH(t_mem(q, occ)) for q in Q_GRID}; kq = grid[Q_DECIDE]; ksur = _rm_KH(1e-4)
    check = kq < k0 * (1.0 - TOL_G)
    out = outcome(crr=kq, null=k0, domain=closed, check=check)
    sens = ", ".join(f"q = {q}: K_H = {v:.4f}" for q, v in grid.items())
    return make_row(d[2], d[3] + f": dN/dt = r N (1 - N/K) - a N P/(1 + a h N), dP/dt = e a M P/(1 + a h M) - m P, r = {RM['r']}, a = {RM['a']}, h = {RM['h']}, e = {RM['e']}, m = {RM['m']}; the predators' numerical response reads the remembered prey M ({A6_NOTE}, Delta = 1/r, T = {t_mem(Q_DECIDE, occ):.4f}); linear stability of the coexistence equilibrium, K scanned in steps of 1e-3 and refined by bisection",
                    source=src(pid),
                    Q=d[5] + " (computed as: the enrichment K_H where the leading eigenvalue's real part first reaches 0, with memory against without; 'lowers by more than 1 %': K_H(memory) < 0.99 K_H(instantaneous))",
                    ingredient=d[4] + f": {A6_NOTE}",
                    null=d[6] + " (computed as: M = N, the Rosenzweig-MacArthur model)",
                    domain=d[7] + f" (computed as: K_H = 1/(a h) + 2 N*, N* = m/(a (e - m h)) = {Ns:.6f})",
                    numbers=f"K_H with remembered prey (q = {Q_DECIDE}) {kq:.6f}; instantaneous {k0:.6f}; closed form {closed:.6f}; ratio {kq / k0:.4f}; surrogate T = 1e-4 (almost no memory): K_H = {ksur:.6f} ({_w(rel(ksur, k0) <= 1e-3, 'returns to the null, as required', 'VIOLATION')}); q-grid (sensitivity only): {sens}",
                    tg=f"K_H {kq:.6f} vs null {k0:.6f}: {ag(kq, k0)}",
                    tn=f"K_H {kq:.6f} vs the Rosenzweig closed form {closed:.6f} (the memory-free theorem): {ag(kq, closed, TOL_N)}",
                    tc=f"K_H(memory) < 0.99 K_H(instantaneous): {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"when predators breed on the prey they remember, the paradox-of-enrichment Hopf comes at K = {kq:.4f} instead of {k0:.4f}: memory in the numerical response is a distributed delay, and the lag {_w(kq < k0, 'destabilises', 'stabilises')} the equilibrium; the direction {_w(all(v < k0 for v in grid.values()), 'holds', 'does not hold')} over the whole q-grid and the shift {_w(grid[0.25] > grid[0.5] > grid[0.75], 'grows', 'does not grow')} with q; that delays in the predator's response destabilise predator-prey equilibria is a known theme (MacDonald 1978 on distributed delays), so the candidate is the size of the shift for P3 weights, not its direction",
                    weakness="A6 acts on the predators' numerical response only (the kill rate reads the present prey); the occasion Delta = 1/r (one prey generation) sets the memory's time scale and is a modelling choice; the Frechet mean is taken linearly in density (not in a Fisher-Rao coordinate); linear stability only; DEVIATION: declared.py fixes q = 0.5 per occasion for a discrete occasion; this continuous-time model uses the exponential kernel with weight q per occasion of length Delta, and Delta is a modelling choice declared.py leaves open",
                    elegance="Predators that breed on how many prey there used to be, rather than how many there are, start the boom-and-bust cycle on a poorer landscape.",
                    child="If foxes decide how many cubs to have by remembering last season's rabbits, they keep having too many or too few, and the two populations start to swing up and down sooner.")


# ---------------------------------------------------------------- [2] P08-2 island biogeography, remembered pool
MW = dict(I=2.0, E=1.0, P0=100.0, P1=150.0, t_end=1500.0, dt=0.05)


def _mw_run(T):
    I, E, P1 = MW["I"], MW["E"], MW["P1"]; dt = MW["dt"]
    S = MW["P0"] * I / (I + E); M = MW["P0"]; t95 = None; S_star = P1 * I / (I + E); S0 = S
    def f(S, M):
        pool = P1 if T == 0.0 else M
        return I * (1.0 - S / pool) - E * S / P1, (0.0 if T == 0.0 else (P1 - M) / T)
    for i in range(int(round(MW["t_end"] / dt))):
        a = f(S, M); b = f(S + .5 * dt * a[0], M + .5 * dt * a[1]); c = f(S + .5 * dt * b[0], M + .5 * dt * b[1]); e = f(S + dt * c[0], M + dt * c[1])
        S += dt * (a[0] + 2 * b[0] + 2 * c[0] + e[0]) / 6; M += dt * (a[1] + 2 * b[1] + 2 * c[1] + e[1]) / 6
        if t95 is None and (S - S0) >= 0.95 * (S_star - S0):
            t95 = (i + 1) * dt
    return S, t95


def r2():
    pid = "P08-2"; d = DECL[pid]; occ = 1.0
    S0, t0 = _mw_run(0.0); grid = {q: _mw_run(t_mem(q, occ)) for q in Q_GRID}; Sq, tq = grid[Q_DECIDE]
    dom = MW["P1"] * MW["I"] / (MW["I"] + MW["E"])
    check = rel(Sq, S0) <= TOL_G
    out = outcome(crr=Sq, null=S0, domain=dom, check=check)
    sens = ", ".join(f"q = {q}: S = {v[0]:.8f}, t95 = {v[1]:.2f}" for q, v in grid.items())
    return make_row(d[2], d[3] + f": dS/dt = I (1 - S/M) - E S/P, I = {MW['I']}, E = {MW['E']} species per year, the island's immigrants drawn from the remembered pool M ({A6_NOTE}, Delta = 1 year); the mainland pool steps from {MW['P0']:.0f} to {MW['P1']:.0f} species at t = 0 with the island at its old equilibrium; RK4 dt {MW['dt']} to t = {MW['t_end']:.0f}",
                    source=src(pid),
                    Q=d[5] + " (computed as: the richness at t = 1500 after the pool step, with memory against without; 'unchanged' within TOL_G)",
                    ingredient=d[4] + f": {A6_NOTE}",
                    null=d[6] + " (computed as: M = P, the MacArthur-Wilson model)",
                    domain=d[7] + " (computed as: S* = P I/(I + E) with the new pool)",
                    numbers=f"final richness with memory (q = {Q_DECIDE}) {Sq:.10f}, without {S0:.10f}, theorem {dom:.10f}; time to 95 % of the change: with memory {tq:.2f} years, without {t0:.2f} years; q-grid (sensitivity only): {sens}",
                    tg=f"S {Sq:.8f} vs null {S0:.8f}: {ag(Sq, S0)}",
                    tn=f"S {Sq:.8f} vs P I/(I + E) = {dom:.8f}: {ag(Sq, dom, TOL_N)}",
                    tc=f"equilibrium richness unchanged by memory (relative gap {rel(Sq, S0):.2e} <= {TOL_G:g}): {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"a remembered pool is the true pool at rest, so the equilibrium richness {_w(check, 'is', 'is not')} P I/(I + E) with and without memory; memory changes the approach ({tq:.2f} against {t0:.2f} years to 95 %, {_w(tq > t0, 'slower', 'not slower')}); the row reads {out}: A6 with bounded strength returns the settled value at a fixed point, so the ingredient cannot move an equilibrium",
                    weakness="the pool is remembered in the immigration term only; linear immigration and extinction curves; the transient, the only place memory acts, is not what Q asks; DEVIATION: declared.py fixes q = 0.5 per occasion for a discrete occasion; this continuous-time model uses the exponential kernel with weight q per occasion of length Delta, and Delta is a modelling choice declared.py leaves open",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] P08-3 Wright-Fisher, arc against fixation time
WF_N, WF_R = 100, 2000


def _wf_paths(seed):
    """Neutral Wright-Fisher, 2N = 200 copies, a new mutant (1 copy) conditioned on fixation: the h-transform of the
    binomial step is j' = 1 + Binomial(2N - 1, j/2N) (size-biased binomial), exact."""
    M2 = 2 * WF_N; rng = np.random.default_rng(seed); paths = []
    for _ in range(WF_R):
        j = 1; path = [j]
        while j < M2:
            j = 1 + int(rng.binomial(M2 - 1, j / M2)); path.append(j)
        paths.append(np.array(path))
    return paths


def _wf_stats(seed):
    M2 = 2 * WF_N; paths = _wf_paths(seed)
    th = [2.0 * np.arcsin(np.sqrt(p / M2)) for p in paths]                   # Fisher-Rao coordinate of the allele frequency
    xs, ev, off = [], [0], 0.0
    for t in th:                                                              # concatenate, each path translated to start where
        seg = t - t[0] + off; xs.append(seg if not xs else seg[1:]); off = float(seg[-1]); ev.append(ev[-1] + len(t) - 1)   # the last ended
    r = regularity(np.concatenate(xs), np.array(ev), sigma=1.0, dt=1.0, n_boot=N_BOOT, seed=SEED_BOOT)
    geo = np.array([t[-1] - t[0] for t in th]); T = np.array([len(p) - 1 for p in paths], float)
    arcs = np.array([float(np.abs(np.diff(t)).sum()) for t in th])
    return r, geo, T, arcs


def r3():
    pid = "P08-3"; d = DECL[pid]
    r, geo, T, arcs = _wf_stats(0); seeds = {s: _wf_stats(s)[0] for s in (1, 2)}
    p0 = 1.0 / (2 * WF_N); kim = -4.0 * WF_N * (1 - p0) * math.log(1 - p0) / p0
    cv_geo = float(np.std(geo) / np.mean(geo)); cv_T = cv(T)
    slope, icpt = (float(v) for v in np.polyfit(T, arcs, 1)); step_th = math.sqrt(2.0 / math.pi / (2 * WF_N))
    chk_i = cv_geo < cv_T; chk_ii = r["ci95"][1] < 0.0; internal = chk_i != chk_ii
    out = outcome(crr=r["cv_arc"], null=r["cv_clock"], domain=cv_geo, check=chk_ii, internal=internal)
    sens = "; ".join(f"seed {s}: CV(arc) {v['cv_arc']:.4f}, CV(T) {v['cv_clock']:.4f}, relative gap {rel(v['cv_arc'], v['cv_clock']):.4f} ({_ci(v['ci95'])})" for s, v in seeds.items())
    return make_row(d[2], d[3] + f": neutral Wright-Fisher, N = {WF_N} diploids (2N = {2 * WF_N} copies), {WF_R} new mutants conditioned on fixation (exact size-biased binomial step), seed 0; the path in the Fisher-Rao coordinate theta = 2 arcsin(sqrt(p)), where the geodesic from 0 to 1 is pi",
                    source=src(pid),
                    Q=d[5] + " (computed as: regularity() with each fixation as one occasion, CV(path arc) < CV(fixation time) with the paired-bootstrap CI below 0; natural time t/2N rescales the clock and leaves its CV unchanged)",
                    ingredient=d[4] + ", read two ways: (i) the arc the H0 names, the Fisher-Rao distance from the start to fixation (a geodesic); (ii) the arc along the realised frequency path, the literal Q",
                    null=d[6],
                    domain=d[7] + f" (computed as: the CV of reading (i), fixed by construction; and Kimura's conditional mean time -4N (1 - p) ln(1 - p)/p = {kim:.2f} generations as a check of the simulation)",
                    numbers=f"mean fixation time {float(np.mean(T)):.2f} generations (Kimura {kim:.2f}); CV(fixation time) {cv_T:.4f}; reading (i) geodesic {float(np.mean(geo)):.6f} (pi = {math.pi:.6f} from p = 0), CV {cv_geo:.2e}; reading (ii) path arc mean {r['C_mean']:.4f}, CV {r['cv_arc']:.4f}, difference {r['diff']:+.4f}, 95 % CI [{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}], relative gap {rel(r['cv_arc'], r['cv_clock']):.4f}; other seeds: {sens}",
                    tg=f"reading (ii): CV(path arc) {r['cv_arc']:.4f} vs CV(fixation time) {r['cv_clock']:.4f}: {ag(r['cv_arc'], r['cv_clock'])}",
                    tn=f"CV(path arc) {r['cv_arc']:.4f} vs the H0's fixed arc (CV {cv_geo:.2e}): {ag(r['cv_arc'], cv_geo, TOL_N)}",
                    tc=f"reading (i) CV(geodesic) < CV(time): {hf(chk_i)}; reading (ii) CV(path arc) < CV(time) with the CI below 0: {hf(chk_ii)}; the readings {_w(internal, 'disagree', 'agree')}; the literal Q is reading (ii) {qtail(chk_ii)}",
                    out=out,
                    reading=f"in the Fisher-Rao coordinate drift has a constant step size (diffusion theory: mean |step| sqrt(2/pi) sqrt(1/2N) = {step_th:.4f} per generation; observed {r['C_mean'] / float(np.mean(T)):.4f}), so per fixation the path arc is {slope:.4f} x time {_w(icpt >= 0, '+', '-')} {abs(icpt):.4f}, and its CV follows the clock's ({r['cv_arc']:.4f} against {cv_T:.4f}); the arc 'from 0 to 1 is pi' is the geodesic, fixed by construction, which is D3's chord, not a CRR regularity; the path arc {_w(chk_ii, 'beats', 'does not beat')} the clock, {_w(icpt > 0 and chk_ii, 'by the arithmetic of the positive intercept', 'and the intercept does not help it')}",
                    weakness="conditioning on fixation removes the lost mutants; one population size; the arc uses the variance-stabilising angle, so a per-generation step of fixed size is the domain's own diffusion approximation",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] P08-4 Red Queen matching alleles
RQ = dict(sh=1.0, sp=1.0, mu=0.01, N=250.0, T=4000.0, dt=0.01, rec=10)


def _rq_run(seed=0):
    rng = np.random.default_rng(seed); ns = int(round(RQ["T"] / RQ["dt"])); dt = RQ["dt"]
    nz = rng.standard_normal((ns, 2)) * math.sqrt(dt); sh, sp, mu, N = RQ["sh"], RQ["sp"], RQ["mu"], RQ["N"]
    h, p = 0.6, 0.5; out = np.empty((ns // RQ["rec"], 2)); j = 0
    for i in range(ns):
        dh = -sh * h * (1 - h) * (2 * p - 1) + mu * (1 - 2 * h); dp = sp * p * (1 - p) * (2 * h - 1) + mu * (1 - 2 * p)
        h = h + dh * dt + math.sqrt(h * (1 - h) / N) * nz[i, 0]; p = p + dp * dt + math.sqrt(p * (1 - p) / N) * nz[i, 1]
        h = min(max(h, 1e-6), 1 - 1e-6); p = min(max(p, 1e-6), 1 - 1e-6)
        if (i + 1) % RQ["rec"] == 0:
            out[j, 0] = h; out[j, 1] = p; j += 1
    return out


def _rq_events_winding(x):
    ang = np.unwrap(np.arctan2(x[:, 1] - 0.5, x[:, 0] - 0.5)); k = np.floor((ang - ang[0]) / (2 * np.pi))
    return np.nonzero(np.diff(k) > 0)[0] + 1


def _rq_events_schmitt(h, band=0.05):
    ev = []; armed = h[0] < 0.5 - band
    for i in range(1, len(h)):
        if h[i] < 0.5 - band:
            armed = True
        if armed and h[i - 1] < 0.5 <= h[i]:
            ev.append(i); armed = False
    return np.array(ev)


def r4():
    pid = "P08-4"; d = DECL[pid]; dts = RQ["dt"] * RQ["rec"]
    x = _rq_run(); th = 2.0 * np.arcsin(np.sqrt(x))
    ev = _rq_events_winding(x); r = regularity(th, ev, sigma=1.0, dt=dts, n_boot=N_BOOT, seed=SEED_BOOT)
    ev2 = _rq_events_schmitt(x[:, 0]); r2_ = regularity(th, ev2, sigma=1.0, dt=dts, n_boot=N_BOOT, seed=SEED_BOOT)
    per_lin = 4.0 * math.pi / math.sqrt(RQ["sh"] * RQ["sp"])
    ev_c = np.linalg.eigvals(np.array([[-2 * RQ["mu"], -RQ["sh"] / 2], [RQ["sp"] / 2, -2 * RQ["mu"]]]))
    check = r["ci95"][1] < 0.0; amp_ok = r["ci95_amp"][1] < 0.0
    out = outcome(crr=r["cv_arc"], null=r["cv_clock"], domain=None, check=check)
    return make_row(d[2], d[3] + f": dh/dt = -s_h h (1 - h)(2p - 1) + mu (1 - 2h), dp/dt = s_p p (1 - p)(2h - 1) + mu (1 - 2p) (two-allele matching alleles, host h, parasite p), s_h = s_p = {RQ['sh']}, mutation mu = {RQ['mu']}, genetic drift sqrt(x (1 - x)/N), N = {RQ['N']:.0f}; Euler-Maruyama dt {RQ['dt']} over {RQ['T']:.0f} time units, seed 0; one cycle = one full turn of (h - 1/2, p - 1/2) about the centre (unwrapped angle); arc in the Fisher-Rao coordinates 2 arcsin(sqrt(.)) of both frequencies",
                    source=src(pid),
                    Q=d[5] + " (computed as: regularity() between consecutive turns, CV(arc) < CV(period) with the paired-bootstrap CI below 0)",
                    ingredient=d[4] + ": regularity() on the own events (turns of the host-parasite cycle), n_boot 2000, seed 0",
                    null=d[6],
                    domain=d[7],
                    numbers=f"{r['n']} cycles, mean period {float(np.mean(np.diff(ev))) * dts:.3f} (linearised centre: eigenvalues {ev_c[0].real:+.3f} +- {abs(ev_c[0].imag):.3f}i, period {per_lin:.3f}); CV(arc) {r['cv_arc']:.4f}, CV(period) {r['cv_clock']:.4f}, difference {r['diff']:+.4f}, 95 % CI [{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}]; amplitude control CV(amp) {r['cv_amp']:.4f}, CV(arc) - CV(amp) {r['diff_amp']:+.4f} CI [{r['ci95_amp'][0]:+.4f}, {r['ci95_amp'][1]:+.4f}]; other event rule (host frequency up through 1/2 after falling below 0.45): {r2_['n']} cycles, CV(arc) {r2_['cv_arc']:.4f}, CV(period) {r2_['cv_clock']:.4f}, difference {r2_['diff']:+.4f} ({_ci(r2_['ci95'])})",
                    tg=f"CV(arc) {r['cv_arc']:.4f} vs CV(period) {r['cv_clock']:.4f}: {ag(r['cv_arc'], r['cv_clock'])}",
                    tn="no domain theorem cited",
                    tc=f"CV(arc) < CV(period) with the CI below 0: {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"the matching-alleles cycle is a noisy rotation about a damped centre (damping {-ev_c[0].real:.3f} against frequency {abs(ev_c[0].imag):.3f}): drift sets the amplitude of each turn (CV(amp) {r['cv_amp']:.4f}) {_w(r['cv_amp'] > r['cv_clock'], 'more', 'less')} than it sets the duration (CV(period) {r['cv_clock']:.4f}), so the arc per cycle, which follows the amplitude (CV(arc) - CV(amp): {_ci(r['ci95_amp'])}), is {_w(r['cv_arc'] > r['cv_clock'], 'less', 'more')} regular than the period ({r['cv_arc']:.4f} against {r['cv_clock']:.4f}); the Red Queen cycle falls in the {_w(r['cv_arc'] > r['cv_clock'], 'clock-regular', 'arc-regular')} class here, as the measles carrier did (CRR.md, MEAS2); the other event rule {_w((r2_['ci95'][1] < 0.0) == check, 'agrees', 'disagrees')}",
                    weakness="a diffusion approximation with mutation to keep the cycle off the boundaries; one selection strength and population size; the turn counter includes noise-driven turns near the centre",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] P08-5 logistic harvest on remembered stock
HV = dict(r=1.0, K=1.0, F=0.3, shock=0.01, t_end=60.0, dt=0.001)


def _hv_run(T, shock):
    r, K, F, dt = HV["r"], HV["K"], HV["F"], HV["dt"]; xs = K * (1 - F / r); x = (1 - shock) * xs; M = xs; mx = x
    def f(x, M):
        q = x if T == 0.0 else M
        return r * x * (1 - x / K) - F * q, (0.0 if T == 0.0 else (x - M) / T)
    for _ in range(int(round(HV["t_end"] / dt))):
        a = f(x, M); b = f(x + .5 * dt * a[0], M + .5 * dt * a[1]); c = f(x + .5 * dt * b[0], M + .5 * dt * b[1]); e = f(x + dt * c[0], M + dt * c[1])
        x += dt * (a[0] + 2 * b[0] + 2 * c[0] + e[0]) / 6; M += dt * (a[1] + 2 * b[1] + 2 * c[1] + e[1]) / 6; mx = max(mx, x)
    return (mx - xs) / (shock * xs), (mx - xs) / xs, x


def _hv_linear(T, shock):
    r, K, F = HV["r"], HV["K"], HV["F"]; xs = K * (1 - F / r)
    J = np.array([[r - 2 * r * xs / K, -F], [1.0 / T, -1.0 / T]]); w, V = np.linalg.eig(J)
    c = np.linalg.solve(V, np.array([-shock * xs, 0.0])); t = np.arange(0.0, HV["t_end"] + 1e-12, HV["dt"])
    y = np.real((V[0, :][None, :] * c[None, :] * np.exp(np.outer(t, w))).sum(axis=1))
    return float(max(y.max(), 0.0) / (shock * xs)), w


def r5():
    pid = "P08-5"; d = DECL[pid]; occ = 1.0 / HV["r"]; T = t_mem(Q_DECIDE, occ)
    os_m, os_rel, xend = _hv_run(T, HV["shock"]); os_0, _, x0end = _hv_run(0.0, HV["shock"]); os_lin, w = _hv_linear(T, HV["shock"])
    grid = {q: _hv_run(t_mem(q, occ), HV["shock"])[0] for q in Q_GRID}; shocks = {s: _hv_run(T, s)[0] for s in (0.1, 0.3)}
    check = os_m > TOL_G
    out = outcome(crr=os_m, null=os_0, domain=os_lin, check=check)
    stable = bool(np.all(w.real < 0)); cplx = bool(np.any(np.abs(w.imag) > 1e-12))
    sens = ", ".join(f"q = {q}: {v:.4f}" for q, v in grid.items()); ssen = ", ".join(f"shock {s:g}: {v:.4f}" for s, v in shocks.items())
    return make_row(d[2], d[3] + f": dx/dt = r x (1 - x/K) - F M, r = {HV['r']}, K = {HV['K']}, F = {HV['F']} (below the MSY effort r/2), quota F M on the remembered stock M ({A6_NOTE}, Delta = 1/r, T = {T:.4f}); recovery from a sudden {HV['shock']:.0%} depletion of the stock with the memory still at the old equilibrium x* = {HV['K'] * (1 - HV['F'] / HV['r']):.2f}; RK4 dt {HV['dt']} to t = {HV['t_end']:.0f}",
                    source=src(pid),
                    Q=d[5] + " (computed as: the overshoot (max x - x*)/(x* - x0), the control convention of percent overshoot relative to the displacement, against 1 %)",
                    ingredient=d[4] + f": {A6_NOTE}",
                    null=d[6] + " (computed as: quota F x, the logistic with proportional harvest)",
                    domain=d[7] + " (computed as: the overshoot of the linearised two-variable feedback loop from the same displacement, by its eigen-decomposition)",
                    numbers=f"overshoot with memory {os_m:.6f} of the displacement ({os_rel:.6f} of x*), without memory {_f(os_0)}, linear theory {os_lin:.6f}; eigenvalues at x* {w[0].real:+.4f}{w[0].imag:+.4f}i, {w[1].real:+.4f}{w[1].imag:+.4f}i ({_w(stable, 'the equilibrium stays locally stable', 'the equilibrium is unstable')}, {_w(cplx, 'a complex pair', 'real')}); final stock {xend:.6f} and {x0end:.6f}; q-grid (sensitivity only): {sens}; larger shocks (nonlinear): {ssen}",
                    tg=f"overshoot {os_m:.6f} vs null {_f(os_0)}: {ag(os_m, os_0)}",
                    tn=f"overshoot {os_m:.6f} vs linear delayed-feedback theory {os_lin:.6f}: {ag(os_m, os_lin, TOL_N)}",
                    tc=f"overshoot above 1 % of the displacement: {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"a quota that reads the remembered stock keeps taking the old catch after a depletion and eases late after recovery, so the stock {_w(os_m > 0, 'overshoots', 'does not overshoot')} by {os_m:.4f} of the displacement where the instantaneous quota gives {_f(os_0, 4)}; over the q-grid the overshoot exceeds 1 % at {sum(v > TOL_G for v in grid.values())} of {len(grid)} values; the equilibrium {_w(stable, 'stays locally stable', 'loses stability')}, so 'destabilises' holds only in the sense Q's parenthesis gives it, an oscillatory recovery; the linearised feedback loop, the domain's delayed-feedback analysis, gives {os_lin:.4f}",
                    weakness="one effort level F; the overshoot is taken relative to the displacement (percent overshoot), and relative to x* it is printed too; the 1 % shock is chosen so the domain's linear theory is the fair comparison, and larger shocks are printed; the memory starts at the old equilibrium (the quota has not yet seen the depletion); DEVIATION: declared.py fixes q = 0.5 per occasion for a discrete occasion; this continuous-time model uses the exponential kernel with weight q per occasion of length Delta, and Delta is a modelling choice declared.py leaves open",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P08: ecology and evolution (prompt-log entry 234; Predictions70/DECLARATION.md; declared at 8397478)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
