"""Synthesis batch 11: rows 51-55 of QUEUE.md (prompt-log entry 61).
sharp [12] (CONSIST) Schwarzschild thermal family: A1 rejects it as a carrier (Var E = C T^2 < 0); the one proper attempt (A1' in York's cavity).
sharp [13] (CONSIST) de Sitter horizon: A1' mode by mode against the horizon family as a whole.
sharp [14] (CONSIST) critical slowing down -> memory depth ('D8' of the older text; v3.1 has O1): the depth at Omega = 1 under the two readings of A1'.
bio [2] (CONSIST) FitzHugh-Nagumo under slowly varying drive: is the arc-regularity dynamics or geometry (synthesis.py row 7's question)?
bio [4] (CONSIST) Weber's law and the Fechner scale: A6/P3 on the Weber carrier against Helson's adaptation level.

Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data file is
opened (R2). Deterministic: fixed seeds, fixed grids, explicit RK4 on a fixed step, the discrete Riccati equation by
scipy.linalg.solve_discrete_are. Run:  uv run python theory/retrodictions/synthesis_batches/batch_11.py
"""
import math
import sys

import numpy as np
from scipy import optimize
from scipy.integrate import quad
from scipy.linalg import solve_discrete_are
from scipy.signal import lfilter

from crr.instrument.core import arc_length, cv, regularity, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


# ---------------------------------------------------------------- 51: sharp [12] Schwarzschild thermal family
def r1(M=1.0, h=1e-6):
    T = lambda m: 1.0 / (8.0 * math.pi * m)                                   # Hawking temperature, Planck units, E = M
    C = 2.0 * h / (T(M + h) - T(M - h))                                       # heat capacity dE/dT by central difference
    varE = C * T(M) ** 2                                                      # the source row's reading: Var E = C T^2
    E_of_beta = lambda b: b / (8.0 * math.pi)                                 # the canonical family in beta = 8 pi M
    I_beta = -(E_of_beta(8 * math.pi * M + h) - E_of_beta(8 * math.pi * M - h)) / (2 * h)   # information geometry: I(beta) = -dE/dbeta = Var E
    closed = -1.0 / (8.0 * math.pi)
    # the one CRR-proper attempt: A1' (the unit as the system's own resolvable step) inside the domain's own remedy, York's cavity
    E_y = lambda m, r: r * (1.0 - math.sqrt(1.0 - 2.0 * m / r))               # quasilocal energy at the wall
    T_y = lambda m, r: 1.0 / (8.0 * math.pi * m * math.sqrt(1.0 - 2.0 * m / r))   # Tolman-shifted temperature at the wall
    york = []
    for r in (2.2, 2.5, 2.9, 3.1, 4.0, 10.0):
        Cr = (E_y(M + h, r) - E_y(M - h, r)) / (T_y(M + h, r) - T_y(M - h, r)); var_r = Cr * T_y(M, r) ** 2
        york.append((r, Cr, var_r, r / (8.0 * math.pi * (3.0 * M - r)), E_y(M, r)))
    r_att, C_att, var_att, closed_att, E_att = york[1]
    sig_att = math.sqrt(var_att); rho_att = E_att / sig_att
    york_ok = all((v > 0) == (r < 3.0 * M) for r, _, v, _, _ in york)            # real unit inside the photon sphere, imaginary outside, on every grid point
    att = outcome(crr=sig_att, null=1.0, domain=math.sqrt(closed_att), check=york_ok)   # the attempt's own label: unit sigma_E against the Planck mass, York's closed form as the domain
    check = varE < 0.0
    out = outcome(crr=varE, null=I_beta, domain=C * T(M) ** 2, check=check)
    reading = {
        "REDUNDANT-IG": f"the source row's content is the Fisher information of a canonical family, which is the variance of its energy (information geometry, Cencov-Amari) and, by fluctuation-dissipation, C T^2 (thermodynamics): every symbol in 'not a carrier' is shared, so the label reads {out} by construction, as the brief says such a row must. The one CRR-proper ingredient that can engage is A1' (a unit of the system's own), and the domain's own remedy already carries it: in York's cavity the unit is real inside the photon sphere and imaginary outside it on every grid point ({hf(york_ok)}; sigma_E = {sig_att:.4f} at r = {r_att:g} M, York's fluctuation formula to {rel(var_att, closed_att):.1e}), which is York's theorem, so that attempt, run through the same three tests against the Planck mass as the outside unit, reads {att}. Nothing in v3.1 mentions unitarity, so 'forces the unitary side' has no clause to come from (the source row said so)",
    }.get(out, f"the two computations of the variance did not agree in this run: {out}")
    return make_row("bh", "Schwarzschild thermal family (T = 1/(8 pi M), E = M, S = 4 pi M^2, Planck units) read as a canonical family in beta = 8 pi M; the source row's 'A1 rejects it as a carrier'",
                    source="theory/retrodictions/sharp_claims.txt [12] (CONSIST)",
                    Q=f"the Schwarzschild thermal family is not a carrier (A1): its Fisher information I(beta) = Var E = C T^2 = {closed:.4f} is negative for every M, so no A1' unit, D2 arc or A3 cut exists on it (the source row's content, built with no CRR-proper ingredient; the proper attempt is printed in the numbers)",
                    ingredient="A1 (the Fisher-Rao metric of the thermal family) - NOT CRR-proper; attempted: A1'/D1 (the unit as the system's own resolvable step of energy, sigma_E = sqrt(Var E), rho = E/sigma_E) in York's cavity",
                    null="the same Fisher information computed as information geometry computes it, I(beta) = -dE/dbeta (identical by the same identity)",
                    domain="fluctuation-dissipation, Var E = C T^2, with Hawking 1976 / Gibbons-Perry 1978: the heat capacity of a Schwarzschild black hole is negative, so the canonical ensemble does not exist; York 1986: in a cavity of radius r the heat capacity at fixed wall area is positive for 2M < r < 3M and the ensemble exists",
                    numbers=f"M = {M:g}: C = dE/dT = {C:.6f} (closed -8 pi M^2 = {-8 * math.pi * M ** 2:.6f}); Var E = C T^2 = {varE:.6f}; I(beta) = -dE/dbeta = {I_beta:.6f}; closed form -1/(8 pi) = {closed:.6f}. York's cavity, wall at r: "
                            + "; ".join(f"r = {r:g} M: C_A = {Cr:.4f}, Var E = {v:.5f} (closed r/(8 pi (3M - r)) = {c:.5f}), sigma_E = " + (f"{math.sqrt(v):.4f}" if v > 0 else "imaginary") for r, Cr, v, c, E in york)
                            + f"; at r = {r_att:g} M the unit is sigma_E = {sig_att:.4f} on a quasilocal energy E = {E_att:.4f}, rho = E/sigma_E = {rho_att:.4f} resolvable steps; as r -> infinity Var E -> {closed:.4f} (the source's rejection)",
                    tg=f"Var E (CRR reading, C T^2) {varE:.6f} vs null (information geometry, -dE/dbeta) {I_beta:.6f}: {ag(varE, I_beta)} (no CRR-proper ingredient in Q)",
                    tn=f"fluctuation-dissipation gives {C * T(M) ** 2:.6f}: {ag(varE, C * T(M) ** 2, TOL_N)} (the domain has Q: the sign of the heat capacity)",
                    tc=f"Var E < 0 (the family is not an exponential family; no canonical ensemble): {hf(check)}",
                    out=out, reading=reading,
                    weakness="a two-line calculation on a one-parameter family; the microcanonical description (fixed M) is admissible in the domain and says nothing about carriers; the York numbers are the attempt's, and its own T-N would agree with York by construction; citations by name and year only, not fetched here (R10)")


# ---------------------------------------------------------------- 52: sharp [13] de Sitter horizon
def r2(H=1.0, w=1.0, H2=2.0, h=1e-6):
    T = lambda hh: hh / (2.0 * math.pi); S = lambda hh: math.pi / hh ** 2      # Gibbons-Hawking temperature and entropy of the static patch
    C = T(H) * (S(H + h) - S(H - h)) / (T(H + h) - T(H - h)); varE = C * T(H) ** 2
    closed = -1.0 / (2.0 * math.pi)
    # the mode family: one Bose mode of frequency w seen by a static-patch detector at beta = 2 pi / H
    n = lambda b: 1.0 / (math.exp(b * w) - 1.0)
    I_mode = lambda b: w * w * n(b) * (n(b) + 1.0)                            # Var E_mode = w^2 n(n+1): the mode's Fisher information in beta
    b1, b2 = 2.0 * math.pi / H, 2.0 * math.pi / H2
    sig_mode = 1.0 / math.sqrt(I_mode(b1))                                    # A1' unit of beta for the mode at H
    steps_own = quad(lambda b: math.sqrt(I_mode(b)), b2, b1)[0]               # D1: resolvable steps of beta from H to H2 in the mode's own unit
    steps_out = b1 - b2                                                       # the outside unit: beta counted in Planck time
    domain = math.log(math.tanh(b1 * w / 4.0)) - math.log(math.tanh(b2 * w / 4.0))   # closed form: int w/(2 sinh(b w/2)) db = ln tanh(b w/4)
    modes = [(ww, 1.0 / math.sqrt(ww * ww * (1.0 / (math.exp(b1 * ww) - 1.0)) * (1.0 / (math.exp(b1 * ww) - 1.0) + 1.0))) for ww in (0.1, 0.5, 1.0, 2.0)]
    check = (rel(steps_own, domain) <= 1e-6) and all(np.isfinite(s) and s > 0 for _, s in modes) and varE < 0
    out = outcome(crr=steps_own, null=steps_out, domain=domain, check=check)
    reading = {
        "REDUNDANT-DOMAIN": f"on this family the source row's Q reads exactly as row 1's: Var E = {varE:.4f} is information geometry's number with the domain's sign, REDUNDANT-IG by construction. Asked what a CRR-proper ingredient can add, A1' gives the static-patch observer a real unit mode by mode (sigma_beta = {sig_mode:.4f} at omega = {w:g}) and none for the horizon family as a whole, and the count of resolvable steps it produces ({steps_own:.4f} from H = {H:g} to {H2:g}) is the Bose fluctuation n(n+1) integrated, Einstein's 1909 formula on Gibbons-Hawking's spectrum: the carrier test cuts between the radiation and the geometry at exactly the place the domain does (negative heat capacity belongs to the horizon, not to the thermal spectrum), so the synthesis reading is {out}",
    }.get(out, f"the mode count did not match the closed form in this run: {out}")
    return make_row("bh", "de Sitter static patch (T = H/(2 pi), S = pi/H^2, Planck units): the horizon's thermal family against the thermal family of one field mode seen by the static-patch detector",
                    source="theory/retrodictions/sharp_claims.txt [13] (CONSIST)",
                    Q=f"A1' gives the static-patch observer a resolvable step of inverse temperature mode by mode, sigma_beta = 2 sinh(beta omega/2)/omega, real for every omega and H, and none for the horizon family as a whole (Var E = {closed:.4f} < 0); the number of resolvable steps of beta between two Hubble rates in the mode's own unit is ln tanh(pi omega/(2H)) - ln tanh(pi omega/(2 H'))",
                    ingredient="A1'/D1 (the unit as the system's own resolvable step, 1/sqrt(I); rho = extent/unit), A1 on the single-mode Bose family (not proper)",
                    null="an outside unit: beta counted in Planck time (the unit the domain writes T = H/(2 pi) in)",
                    domain="Einstein 1909 / Bose statistics: the energy fluctuation of one thermal mode is omega^2 n(n+1) = omega^2/(4 sinh^2(beta omega/2)), so the Fisher length in beta integrates in closed form; Gibbons-Hawking 1977: the horizon's heat capacity is negative while the detected spectrum is an ordinary thermal one",
                    numbers=f"horizon family at H = {H:g}: C = T dS/dT = {C:.6f} (closed -2 pi/H^2 = {-2 * math.pi / H ** 2:.6f}), Var E = C T^2 = {varE:.6f} (closed -1/(2 pi) = {closed:.6f}): no unit. Mode family at H = {H:g}: "
                            + "; ".join(f"omega = {ww:g}: sigma_beta = {s:.4f}" for ww, s in modes)
                            + f"; resolvable steps of beta from H = {H:g} to H = {H2:g} at omega = {w:g}: {steps_own:.6f} in the mode's own unit, {steps_out:.6f} in Planck units; closed form {domain:.6f}",
                    tg=f"steps in the mode's own unit {steps_own:.4f} vs null (Planck units) {steps_out:.4f}: {ag(steps_own, steps_out)}",
                    tn=f"the Bose fluctuation integrated gives {domain:.4f}: {ag(steps_own, domain, TOL_N)} (the domain has Q)",
                    tc=f"quadrature matches the closed form to {rel(steps_own, domain):.1e}, every mode unit is real and positive, the horizon's Var E is negative: {hf(check)}",
                    out=out, reading=reading,
                    weakness="the split between 'the radiation' and 'the horizon' is the domain's, and A1' only names the unit each side would have; no A3, D5 or A6 content was found on a static patch (no events, no occasions); citations by name and year only, not fetched here (R10)")


# ---------------------------------------------------------------- 53: sharp [14] critical slowing down and the memory depth at Omega = 1
def _gain(a, q, r):
    """Steady-state Kalman gain for x' = a x + w (Var w = q), y = x + n (Var n = r): the domain's Riccati equation."""
    P = float(solve_discrete_are(np.array([[a]]), np.array([[1.0]]), np.array([[q]]), np.array([[r]])).item())
    return P / (P + r), P


def _K_rw(v):
    return (v / 2.0) * (math.sqrt(v * v + 4.0) - v)                          # P4: the random-walk gain the source row used


def r3(ks=(1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001), k_named=0.01, n_sim=200000, seed=0):
    rows = []
    for k in ks:
        a = math.exp(-k); v2 = 1.0 - a * a; q = v2                             # process noise set so the stationary variance is 1
        Ka, _ = _gain(a, q, 1.0)                                              # reading (a): the unit is the state's stationary spread, r = Var x
        Kb, _ = _gain(a, q, q)                                                # reading (b): the unit is the one-step innovation, r = q
        Kn, _ = _gain(a, 1.0, 1.0)                                            # the source's probe: q = r = 1 fixed (an outside unit)
        rows.append((k, a, math.sqrt(v2), 1.0 / Ka, 1.0 + 1.0 / math.sqrt(v2), 1.0 / Kb, 1.0 / Kn, 1.0 / _K_rw(math.sqrt(v2)), 1.0 / k))
    by_k = {r[0]: r for r in rows}
    k, a, v, d_a, d_a_closed, d_b, d_null, d_src, tau = by_k[k_named]
    sl = lambda i: (math.log(by_k[0.001][i]) - math.log(by_k[0.01][i])) / (math.log(0.001) - math.log(0.01))
    slope_a, slope_b, slope_tau = sl(3), sl(5), sl(8)
    P_b = (a * a + math.sqrt(a ** 4 + 4.0)) / 2.0; d_b_closed = 1.0 + 1.0 / P_b   # reading (b) closed form: P-/q = (a^2 + sqrt(a^4 + 4))/2
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    d_eqpull = 1.0 / 0.5                                                      # H-EQ's 'equal pull' reading of Omega = 1: K = 1/2 (batches 02 and 06)
    # the instrument's own clause of A1' on a simulated trajectory at k_named (registered detrender, window 9, order 2, MAD)
    rng = np.random.default_rng(seed); q_named = 1.0 - a * a
    x = lfilter([1.0], [1.0, -a], rng.normal(0.0, math.sqrt(q_named), n_sim))
    sig_inst = unit_sigma(x); step = math.sqrt(q_named); spread = float(np.std(x))
    internal = rel(d_a, d_b) > TOL_G
    out = outcome(crr=d_a, null=d_null, domain=tau, check=None, internal=internal)
    probe_is_b = "is" if rel(d_b, d_null) <= TOL_G else "is not"
    nearer = "second" if abs(math.log(sig_inst / step)) < abs(math.log(sig_inst / spread)) else "first"
    reading = {
        "INTERNAL": f"read against v3.1: 'D8' is a clause of the older text; v3.1 carries O1 in its place, which asks whether the depth follows from the system's own state model at Omega = 1 with no other parameter and says retention is not a CRR quantity until that is derived for a mean-reverting model and checked. This row is that derivation for the AR(1), and it has no free parameter under either reading of A1', but the two readings give different laws: the unit as the state's stationary spread makes the depth d = 1 + (1 - a^2)^(-1/2) diverge as k^(-1/2) (slope {slope_a:.3f} over k = 0.01 -> 0.001), the unit as the one-step innovation makes it saturate at the golden ratio (d = {d_b:.4f} at k = {k:g}, phi = {phi:.4f}), and the source's 'instrument noise fixed' probe {probe_is_b} the second reading. The instrument's own clause on a simulated trajectory returns {sig_inst:.4f}, i.e. {sig_inst / step:.3f} of the step and {sig_inst / spread:.3f} of the spread, so it sits nearer the {nearer} reading. Neither reading gives the SHARP claim's 'as the relaxation time' (tau = 1/k, slope {slope_tau:.3f}): O1 stays open at the unit, not at Omega",
    }.get(out, f"the two readings of the unit agreed in this run: {out}")
    return make_row("filt", f"Critical slowing down: a mean-reverting AR(1) state x' = a x + w, a = e^(-k), observed in noise and filtered at steady state (the domain's Riccati equation); the memory depth d = 1/K of the filter at Omega = 1 as the relaxation rate k -> 0",
                    source="theory/retrodictions/sharp_claims.txt [14] (CONSIST)",
                    Q="in the system's own unit (A1') the memory depth of a critically slowing state at Omega = 1 is fixed by the state model alone (O1's question): attempted, and it has two values because A1' has two readings on a state with no occasions, the stationary spread (d diverges as k^(-1/2)) and the one-step innovation (d -> phi)",
                    ingredient="A1' (the unit as the system's own resolvable step) in its two readings, with Omega = 1 read as the Bayes-optimal (Kalman) weighting of past and present (batch 02's reading A, which reduces to the domain's filter) and O1 (retention depth open)",
                    null="an outside unit: the source's probe, process and observation noise fixed at q = r = 1 while k -> 0",
                    domain="critical slowing down: the autocorrelation time tau = -1/ln a = 1/k diverges as the relaxation rate vanishes (the domain's memory measure); the steady-state Riccati equation gives the gain for any q/r",
                    numbers="; ".join(f"k = {k_:g}: reading (a) d = {da_:.4f} (closed 1 + 1/v = {dc_:.4f}, v = {v_:.4f}), reading (b) d = {db_:.4f}, null d = {dn_:.4f}, source's 1/K_rw(v) = {ds_:.4f}, tau = {t_:.1f}" for k_, a_, v_, da_, dc_, db_, dn_, ds_, t_ in rows)
                            + f"; slopes d ln d / d ln k over k = 0.01 -> 0.001: reading (a) {slope_a:.4f} (asymptote -1/2), reading (b) {slope_b:.4f}, tau {slope_tau:.4f}; reading (b) closed form at k = {k:g}: {d_b_closed:.4f} (Riccati {d_b:.4f}), limit phi = {phi:.4f}; the source's random-walk shortcut differs from the AR(1) Riccati by {rel(d_src, d_a):.3f} at k = {k:g} (P4 is the random-walk identity); H-EQ's equal-pull reading of Omega = 1 gives K = 1/2, d = {d_eqpull:.1f} at every k; instrument clause: unit_sigma on {n_sim} steps of the AR(1) at k = {k:g} (seed {seed}) = {sig_inst:.4f}, step sqrt(q) = {step:.4f}, spread = {spread:.4f}",
                    tg=f"reading (a) d {d_a:.4f} vs null (q = r fixed) {d_null:.4f}: {ag(d_a, d_null)}; reading (b) d {d_b:.4f} vs null {d_null:.4f}: {ag(d_b, d_null)} (the source's probe is reading (b))",
                    tn=f"the autocorrelation time gives tau = {tau:.1f} at k = {k:g}: {ag(d_a, tau, TOL_N)} from reading (a), {ag(d_b, tau, TOL_N)} from reading (b); no domain theorem selects a depth",
                    tc=f"not reached: the two readings of the unit give d = {d_a:.4f} and {d_b:.4f} at k = {k:g} (relative difference {rel(d_a, d_b):.3f})",
                    out=out, reading=reading,
                    weakness=f"'depth = 1/K' is a reading of a gain, not a clause of v3.1; Omega = 1 has its own two readings on this domain (batches 02 and 06: Kalman against equal pull, d = {d_eqpull:.1f}), which would make a third value; the instrument clause was run on samples, not on occasions, because a monotone relaxation has no rotor (O3); the AR(1) is linearised critical slowing down, one state, one noise")


# ---------------------------------------------------------------- 54: bio [2] FitzHugh-Nagumo under slowly varying drive
def _fhn(I_of_t, t_end, n, y0=(-1.0, -0.5), eps=0.08, a=0.7, b=0.8):
    """FitzHugh-Nagumo v' = v - v^3/3 - w + I(t), w' = eps (v + a - b w), explicit RK4 on a fixed grid."""
    t = np.linspace(0.0, t_end, n); dt = t[1] - t[0]
    v, w = y0; V = np.empty(n); V[0] = v
    f = lambda tt, vv, ww: (vv - vv ** 3 / 3.0 - ww + I_of_t(tt), eps * (vv + a - b * ww))
    for i in range(1, n):
        tt = t[i - 1]
        k1v, k1w = f(tt, v, w); k2v, k2w = f(tt + dt / 2, v + dt / 2 * k1v, w + dt / 2 * k1w)
        k3v, k3w = f(tt + dt / 2, v + dt / 2 * k2v, w + dt / 2 * k2w); k4v, k4w = f(tt + dt, v + dt * k3v, w + dt * k3w)
        v += dt * (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0; w += dt * (k1w + 2 * k2w + 2 * k3w + k4w) / 6.0
        V[i] = v
    return t, V


def _upcrossings(V, thr=0.5):
    return np.where((V[1:] > thr) & (V[:-1] <= thr))[0] + 1


def _paired_ci(x, y, n_boot=2000, seed=0):
    """Paired-bootstrap 95 % CI of CV(x) - CV(y) over the same occasions (the instrument's criterion, R6)."""
    rng = np.random.default_rng(seed); d = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(x), len(x)); d.append(cv(x[idx]) - cv(y[idx]))
    lo, hi = np.percentile(d, [2.5, 97.5]); return float(lo), float(hi)


def r4(I0=0.5, I1=0.2, om=0.03, excess_thr=0.1):
    t, V = _fhn(lambda tt: I0 + I1 * math.sin(om * tt), 1200.0, 240001)      # the source row's drive, grid and initial state
    dt = t[1] - t[0]; up = _upcrossings(V)[2:]
    r = regularity(V, up, sigma=1.0, dt=dt, n_boot=500, seed=0)              # default segmentation: no reset jump in a continuous ODE
    arcs = np.array([arc_length(V[a:b + 1]) for a, b in zip(up[:-1], up[1:])])
    ptp2 = np.array([2.0 * np.ptp(V[a:b + 1]) for a, b in zip(up[:-1], up[1:])])
    isi = np.diff(up) * dt; excess = arcs - ptp2
    gap = excess > excess_thr                                                  # an occasion holds a subthreshold excursion iff its arc exceeds the two monotone branches
    fire = ~gap
    cv_arc_f, cv_amp_f, cv_clock_f = cv(arcs[fire]), cv(ptp2[fire]), cv(isi[fire])
    # the loop's geometry: the autonomous limit cycle at fixed drive, its total variation per cycle
    loops = []
    for I_c in (0.35, 0.4, 0.5, 0.6, 0.7):
        tt, VV = _fhn(lambda x, I_c=I_c: I_c, 600.0, 120001); u = _upcrossings(VV)
        loops.append((I_c, (u[-1] - u[-2]) * (tt[1] - tt[0]), arc_length(VV[u[-2]:u[-1] + 1])))
    tv_loop = {I_c: tv for I_c, _, tv in loops}
    tv_grid = np.array([tv for _, _, tv in loops])
    singular = 8.0                                                            # eps -> 0: the jumps land at v = -/+ 2 (v^3/3 - v = -/+ 2/3), so one loop has total variation 2 x 4
    crr, null, domain = float(arcs[fire].mean()), tv_loop[I0], singular
    amp_wins = r["ci95_amp"][0] > 0.0                                          # CI of CV(arc) - CV(amplitude) entirely above 0: the amplitude control is the more regular
    ci_f = _paired_ci(arcs[fire], ptp2[fire])                                  # on the firing occasions the same CI must include 0 for the identity arc = 2 ptp
    excess_f = float(np.abs(excess[fire]).max())
    check = (excess_f < 0.01) and (ci_f[0] <= 0.0 <= ci_f[1]) and (rel(crr, null) <= TOL_G)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    alt = outcome(crr=r["cv_arc"], null=r["cv_amp"], domain=None, check=(r["ci95_amp"][1] < 0.0))   # H-L5 as CRR.md states it: the arc must beat control (i)
    stands = "stands" if r["cv_arc"] < r["cv_clock"] else "does not stand"
    reading = {
        "REDUNDANT-IG": f"geometry, as for the heteroclinic cycle (synthesis row 7): on every occasion without a subthreshold excursion the trace runs the two monotone branches of the loop, so the arc is twice the spike amplitude to within {excess_f:.4f} and the constant is the loop's total variation, which the drive does not enter (CV {cv(tv_grid):.4f} across I = 0.35..0.7); the {int(gap.sum())} occasions that hold a ring-down add {float(excess[gap].min()):.3f}-{float(excess[gap].max()):.3f} of arc and are all of the arc's excess variation over the amplitude. The dynamical fact (attraction to a stereotyped loop whose period follows the drive) is the domain's 'spike shape is stereotyped, rate follows the drive'; the CLASS-AGREES reading of the source row {stands} (CV(arc) {r['cv_arc']:.4f}, CV(clock) {r['cv_clock']:.4f}), but H-L5 as CRR.md states it, beyond its amplitude control, reads {alt} on the same numbers: {'the amplitude is the more regular quantity' if amp_wins else 'the amplitude is not the more regular quantity'} (CI [{r['ci95_amp'][0]:.4f}, {r['ci95_amp'][1]:.4f}]). The synthesis reading is {out}, and the SHARP review's list of dynamical CONSIST rows should drop this one as it dropped the heteroclinic cycle",
    }.get(out, f"the firing-occasion arc did not settle at the loop's total variation in this run: {out}")
    return make_row("neur", f"FitzHugh-Nagumo relaxation oscillator (eps = 0.08, a = 0.7, b = 0.8) under the slowly varying drive I(t) = {I0:g} + {I1:g} sin({om:g} t), t in [0, 1200] on 240001 RK4 steps; spikes = upward crossings of v = 0.5, first two dropped; the source row's model",
                    source="theory/retrodictions/bio_retrodictions.txt [2] (CONSIST)",
                    Q="the arc of each interspike occasion is the limit cycle's total variation, a constant of the loop's geometry (twice the v-span between the cubic nullcline's jump landings; 8 in the singular limit) that the drive does not enter: the neuron is arc-regular because its spike is stereotyped, and on every occasion without a subthreshold excursion CV(arc) = CV(amplitude control)",
                    ingredient="H-L5 (the class claim: arc against clock between own events), D5 (occasion = interspike interval), D2 with the identity metric on v (the source's carrier), control (i) of H-L5 (the excursion amplitude)",
                    null="the loop's total variation at fixed drive I = 0.5: the autonomous limit cycle's geometry, no drive and no events",
                    domain="singular perturbation theory of the relaxation oscillator (eps -> 0): the slow branches leave the cubic nullcline at its knees v = +/-1 and the fast jumps land at v = -/+2, so one loop has total variation 8 whatever the drive; the finite-eps loop is computed here",
                    numbers=f"{r['n']} occasions: CV(arc) = {r['cv_arc']:.4f}, CV(clock) = {r['cv_clock']:.4f}, CV(amplitude) = {r['cv_amp']:.4f}, C_mean = {r['C_mean']:.4f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) = [{r['ci95'][0]:.4f}, {r['ci95'][1]:.4f}], of CV(arc) - CV(amplitude) = [{r['ci95_amp'][0]:.4f}, {r['ci95_amp'][1]:.4f}]; arc - 2 ptp per occasion: "
                            + ", ".join(f"{e:+.3f}" for e in excess)
                            + f"; occasions with a subthreshold excursion (arc - 2 ptp > {excess_thr:g}): {int(gap.sum())}, their ISIs " + ", ".join(f"{s:.1f}" for s in isi[gap])
                            + f"; firing occasions ({int(fire.sum())}): mean arc {crr:.4f}, CV(arc) = {cv_arc_f:.4f}, CV(amplitude) = {cv_amp_f:.4f} (paired-bootstrap 95 % CI of the difference [{ci_f[0]:.4f}, {ci_f[1]:.4f}]), CV(clock) = {cv_clock_f:.4f} (ISI {isi[fire].min():.1f}-{isi[fire].max():.1f}); autonomous loop at fixed I: "
                            + "; ".join(f"I = {I_c:g}: period {per:.2f}, total variation {tv:.4f}" for I_c, per, tv in loops)
                            + f" (CV of the loop's total variation across the grid {cv(tv_grid):.4f}); singular limit {singular:.1f}",
                    tg=f"mean firing-occasion arc {crr:.4f} vs null (the autonomous loop's total variation at I = {I0:g}) {null:.4f}: {ag(crr, null)}",
                    tn=f"the singular-limit loop gives {domain:.1f}: {ag(crr, domain, TOL_N)} ({'eps = 0.08 is not singular' if rel(crr, domain) > TOL_N else 'the finite-eps loop is at the singular value'}; the finite-eps loop is the domain's number and the null)",
                    tc=f"|arc - 2 ptp| < 0.01 on every firing occasion, the paired-bootstrap CI of CV(arc) - CV(amplitude) there includes 0, and the mean arc within {TOL_G:g} of the loop: {hf(check)}",
                    out=out, reading=reading,
                    weakness="no statistical carrier: the identity metric on v is the source's stand-in, which A1 does not license; one drive, one model neuron; the excursion rule (arc - 2 ptp > 0.1) is a named constant of this row; the quiescent gaps come from the drive dipping below the firing threshold, so their number is the drive's",
                    elegance="A spike is the same size every time; what changes is the wait between spikes. Measured by how far the voltage travels, every beat is one full loop of the same track; measured by the clock, the beats wander with the drive. The picture teaches what an arc-regular system is, and also that the regularity here belongs to the track, not to the traveller.",
                    child="A nerve cell fires by making a spike that always looks the same, like a runner doing one lap of the same track. When the cell is pushed harder it laps more often, and when it is pushed less it waits longer, but each lap is the same length of track. So if you count in laps the cell is perfectly steady, and if you count in seconds it is not. The steadiness comes from the track being fixed, not from the runner.")


# ---------------------------------------------------------------- 55: bio [4] Weber's law: the A6 seed on the Weber carrier
def r5(k=0.1, s1=10.0, s2=80.0, n_stim=12, q=0.5, seed=4):
    rng = np.random.default_rng(seed)
    s = np.exp(rng.uniform(math.log(s1), math.log(s2), n_stim))                # a settled series of stimulus magnitudes, log-uniform on [s1, s2]
    w = (1.0 - q) * q ** np.arange(n_stim)[::-1]; w /= w.sum()                # P3: pi_k ∝ q^k over age k (k = 0 the most recent)
    d2 = lambda y: float((w * ((np.log(y) - np.log(s)) / k) ** 2).sum())      # A1 under Weber's law: I(s) = 1/(k s)^2, d(y, s) = |ln y - ln s|/k
    res = optimize.minimize_scalar(d2, bounds=(s1 / 2, 2 * s2), method="bounded", options=dict(xatol=1e-12))
    frechet = float(res.x)
    geo = math.exp(float((w * np.log(s)).sum()))                               # the weighted geometric mean
    ari = float((w * s).sum())                                                 # the null: the same weights with the Euclidean metric
    helson = 10.0 ** float((w * np.log10(s)).sum())                            # Helson: log AL = weighted mean of log stimuli
    wu = np.ones(n_stim) / n_stim
    geo_u, ari_u = math.exp(float((wu * np.log(s)).sum())), float((wu * s).sum())
    arc = math.log(s2 / s1); jnd = arc / k                                     # the source row's numbers
    tol_c = 1e-6                                                              # the bounded minimiser resolves the argmin to ~1e-9 relative; the check is set one resolvable step coarser
    check = (rel(frechet, geo) <= tol_c) and (rel(frechet, helson) <= tol_c)
    out = outcome(crr=frechet, null=ari, domain=helson, check=check)
    reading = {
        "REDUNDANT-DOMAIN": f"A6 does work on this carrier (T-G: the Fisher-Rao Frechet mean {frechet:.4f} is not the arithmetic mean {ari:.4f}), and what it produces is Helson's adaptation level: the antilog of a weighted mean of log stimulus magnitudes, which Helson chose over the arithmetic mean because it fit; with uniform weights the two means {ag(geo_u, ari_u)} as well ({geo_u:.4f} against {ari_u:.4f}). The source row's content (the JND is the unit and the Fechner scale is the arc, {jnd:.1f} JNDs from {s1:g} to {s2:g}) was the domain's, and the regeneration axiom added to it is the domain's too; P3's q and Helson's weights are both free, so the row fixes nothing the domain leaves open. The synthesis reading is {out}",
    }.get(out, f"the Frechet mean did not reproduce the weighted geometric mean in this run: {out}")
    return make_row("psych", f"Perceptual magnitude under Weber's law (Weber fraction k = {k:g}, Fisher information 1/(k s)^2, JND = one resolvable step): a settled series of {n_stim} stimulus magnitudes on [{s1:g}, {s2:g}] and the level the observer is seeded with for the next",
                    source="theory/retrodictions/bio_retrodictions.txt [4] (CONSIST)",
                    Q=f"the level a Weber observer carries into the next presentation, taken as the Fisher-Rao Frechet mean of the settled stimuli under P3 age weights (A6, q = {q:g}), is the weighted geometric mean of the stimulus magnitudes, not their arithmetic mean: the adaptation level of the series",
                    ingredient="A6 (regeneration by a bounded Frechet mean of settled occasions), P3 (geometric age weights), D5 (occasion = one presentation), A1' (the JND as the unit, the source's reading), A1 on the Weber family (not proper)",
                    null="the same weights with the Euclidean metric on stimulus magnitude: the weighted arithmetic mean",
                    domain="Helson 1947 / 1964, adaptation-level theory: the adaptation level is the antilog of a weighted mean of the logarithms of the stimuli (a weighted geometric mean), the weights empirical",
                    numbers=f"stimuli (oldest first): " + ", ".join(f"{v:.2f}" for v in s) + f"; P3 weights q = {q:g} (most recent weight {w[-1]:.4f}); Frechet mean under d = |ln y - ln s|/k by minimisation: {frechet:.6f}; weighted geometric mean {geo:.6f}; Helson's antilog of the weighted log mean {helson:.6f}; weighted arithmetic mean {ari:.6f}; uniform weights: geometric {geo_u:.4f}, arithmetic {ari_u:.4f}; the source's arc from {s1:g} to {s2:g}: ln(s2/s1) = {arc:.4f}, {jnd:.1f} JNDs",
                    tg=f"Frechet mean {frechet:.4f} vs null (arithmetic mean) {ari:.4f}: {ag(frechet, ari)}",
                    tn=f"Helson's adaptation level gives {helson:.4f}: {ag(frechet, helson, TOL_N)} (the domain has Q)",
                    tc=f"the Frechet minimiser equals the weighted geometric mean to {rel(frechet, geo):.1e} and Helson's level to {rel(frechet, helson):.1e} (both within {tol_c:g}): {hf(check)}",
                    out=out, reading=reading,
                    weakness="one seeded series and one q; Helson's full formula adds background and residual terms that this row does not model; the Frechet mean on a one-parameter Weber family is a one-line identity (the log coordinate is flat), so T-C is a check of arithmetic; citations by name and year only, not fetched here (R10)",
                    elegance="Count in steps you can actually tell apart and the 'usual' level of what you have seen is the middle of the doublings, not the middle of the numbers. A rule with no knobs, and it is the one the psychologists found by fitting.",
                    child="Suppose you lift a few things one after another, some light, some heavy. Your hands settle on a feel for the 'normal' weight. That normal is not the plain average of the weights; it sits in the middle of the doublings, because your hands notice a weight doubling, not a weight going up by a fixed amount. Scientists who study the senses worked that out long ago.")


def main():
    return run_batch("Synthesis batch 11: rows 51-55 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
