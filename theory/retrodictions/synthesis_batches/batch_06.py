"""Synthesis batch 06: rows 26-30 of QUEUE.md (prompt-log entry 61). Daniel's battery [c3] finite-time thermodynamics,
length vs dissipated work; [c4] Curie-Weiss magnet (cycled below Tc: hysteresis reversals as own events); [d1] scalar
random-walk Kalman gain (two readings of Omega = 1); [d2] Cramer-Rao unit 1/sqrt(I) (named vs estimated A1' unit);
[d3] drifted Brownian 1/sqrt(T) scaling (level crossings: the arc is the clock, AGENT_LOG 21)."""
import math
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.signal import savgol_coeffs
from scipy.stats import norm

from crr.instrument.core import intrinsic_phase, antipodal_cuts, peak_cuts, regularity, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _word(cond, yes, no):
    return yes if cond else no


# ---------------------------------------------------------------- 26 [c3] finite-time thermodynamics: path against endpoint
def r1():
    def w_diss(ps, ts):                                              # W = int pdot^2 / (p(1-p)) dt: friction = Fisher metric, relaxation time 1
        dps = np.gradient(ps, ts)
        return float(np.trapezoid(dps ** 2 / (ps * (1 - ps)), ts))
    tau, p0, p1, pk = 1.0, 0.2, 0.8, 0.9
    s0, s1, sk = (math.asin(math.sqrt(p)) for p in (p0, p1, pk))
    d = 2.0 * (s1 - s0)                                              # chord: geodesic distance on the Bernoulli family
    L = 2.0 * (sk - s0) + 2.0 * (sk - s1)                            # arc of the overshoot path 0.2 -> 0.9 -> 0.8
    S = L - d
    ts = np.linspace(0.0, tau, 200001)
    geo = np.sin(s0 + (s1 - s0) * ts / tau) ** 2                     # direct protocol at constant Fisher speed (the source's const_speed)
    lop = p0 + (p1 - p0) * (ts / tau) ** 2                           # the source's lopsided monotone protocol (same endpoints, S = 0)
    t_turn = tau * 2.0 * (sk - s0) / L
    sv = np.where(ts <= t_turn, s0 + (sk - s0) * ts / t_turn, sk - (sk - s1) * (ts - t_turn) / (tau - t_turn))
    over = np.sin(sv) ** 2                                           # overshoot protocol at constant Fisher speed along its own path
    w_geo, w_lop, w_over = w_diss(geo, ts), w_diss(lop, ts), w_diss(over, ts)
    def arc_num(ps, ts):                                             # Fisher arc of a sampled protocol: int |pdot| / sqrt(p(1-p)) dt
        return float(np.trapezoid(np.abs(np.gradient(ps, ts)) / np.sqrt(ps * (1 - ps)), ts))
    S_geo, S_lop, S_over_num = arc_num(geo, ts) - d, arc_num(lop, ts) - d, arc_num(over, ts) - d
    S_mono = max(abs(S_geo), abs(S_lop))                             # the larger |S| of the two monotone protocols (P1 equality predicts 0)
    crr, null, dom = L * L / tau, d * d / tau, L * L / tau
    excess_pred = S * (2.0 * d + S) / tau
    check = rel(w_over, crr) <= 1e-3 and w_over > w_geo and rel(w_over - w_geo, excess_pred) <= 1e-3
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("thermo",
        "Finite-time thermodynamics of a driven two-level system (Bernoulli family, Fisher metric dp^2/(p(1-p)) as the friction, relaxation time 1): dissipated work W = int pdot^2/(p(1-p)) dt over protocols of duration tau = 1 from p = 0.2 to p = 0.8, including one that overshoots to p = 0.9",
        source="runs/phaseA/crr_retrodictions.txt [c3] (CONSIST)",
        Q="the minimum dissipation of a protocol is set by the length of the path it takes (the arc L), not by the displacement between its endpoints (the chord d): an overshooting protocol 0.2 -> 0.9 -> 0.8 dissipates at least L^2/tau > d^2/tau, and its excess over the direct protocol is S(2d + S)/tau with S = L - d",
        ingredient="D6/H-T1 (path against endpoint) read on a thermodynamic protocol; D2/D3/D4 supply L, d and S (not CRR-proper)",
        null="the endpoint predictor: the chord d (geodesic distance between the initial and final states) squared over tau",
        domain="Salamon-Berry 1983: dissipated availability >= L^2/tau x (relaxation time) for a path of thermodynamic length L, saturated at constant thermodynamic speed",
        numbers=(f"chord d = {d:.4f}, overshoot arc L = {L:.4f}, surplus S = {S:.4f}; direct protocol at constant speed: W = {w_geo:.4f} (d^2/tau = {null:.4f}); "
                 f"the source's lopsided monotone protocol: W = {w_lop:.4f}; surplus integrated from the sampled paths: direct {S_geo:.2e}, lopsided {S_lop:.2e} (P1 equality on a monotone 1-D path), overshoot {S_over_num:.4f} (closed form {S:.4f}); overshoot at constant speed: W = {w_over:.4f} (L^2/tau = {crr:.4f}); "
                 f"excess over the direct protocol {w_over - w_geo:.4f} against S(2d + S)/tau = {excess_pred:.4f}"),
        tg=f"path predictor L^2/tau {crr:.4f} vs endpoint predictor d^2/tau {null:.4f}: {_word(tg_ok, 'agree', 'differ')}",
        tn=f"Salamon-Berry gives L^2/tau = {dom:.4f} for the path taken: the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"numerical W of the constant-speed overshoot protocol {w_over:.4f} against L^2/tau {crr:.4f} (relative difference {rel(w_over, crr):.1e}), above the direct protocol's {w_geo:.4f}, excess matching S(2d + S)/tau: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the path-against-endpoint reading of dissipation is the domain's own theorem: the bound is written in the length of the path taken, and the excess of a detour is its excess length times (2d + S), information geometry's algebra; "
                 f"the source row's S orders nothing on the two monotone protocols (|S| at most {S_mono:.1e} for both while their dissipation differs, {w_geo:.3f} against {w_lop:.3f}: the speed profile, not the length, separates them), which the source recorded"),
        weakness="the overshoot protocol is chosen to make L differ from d; on any monotone 1-D protocol path and endpoint coincide and Q is empty; no proper ingredient beyond the path/endpoint reading was found (A3 has no rotor on an open protocol, A6 has no occasions)",
        elegance="Cheapest change: take the shortest road and walk it at one steady pace; every detour and every burst of speed is paid for in waste. No knobs: a length and a duration.",
        child="Pushing a heavy box from one spot to another wastes the least effort if you go by the shortest path at one steady speed. Taking a detour costs extra, and so does rushing and then stopping.")


# ---------------------------------------------------------------- 27 [c4] Curie-Weiss magnet cycled below Tc: reversals as antipodal cuts
def r2():
    a = b = 1.0; t_red = -1.0; H = 0.6; om = 0.02
    T = 2.0 * math.pi / om; n_per = 6400; dt = T / n_per; half = n_per // 2
    h_sp = 2.0 / (3.0 * math.sqrt(3.0)) * (-a * t_red) ** 1.5 / math.sqrt(b)   # spinodal (coercive) field of the Landau free energy
    def f(m, t): return -(a * t_red * m + b * m ** 3 - H * math.sin(om * t))
    n_cyc_tr, n_cyc = 1, 6
    n = (n_cyc_tr + n_cyc) * n_per; m = 0.9; ms = np.empty(n + 1); ms[0] = m
    for i in range(n):                                               # fixed-grid RK4
        t = i * dt; k1 = f(m, t); k2 = f(m + 0.5 * dt * k1, t + 0.5 * dt); k3 = f(m + 0.5 * dt * k2, t + 0.5 * dt); k4 = f(m + dt * k3, t + dt)
        m = m + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0; ms[i + 1] = m
    x = ms[n_cyc_tr * n_per:]; tg_ = np.arange(len(x)) * dt
    anti = float(np.max(np.abs(x[half:] + x[:-half])))               # the domain's symmetry on the attractor: m(t + T/2) = -m(t)
    zc = np.where(np.diff(np.sign(x)) != 0)[0] + 1                   # own events: the reversals (sign flips of m at the jump)
    ph = intrinsic_phase(x)
    adv = np.diff(ph[zc])[1:-1] / math.pi                            # phase advance between consecutive interior reversals, in half-turns
    clk = np.diff(tg_[zc])[1:-1] / (T / 2.0)                         # the same intervals on the drive's clock, in half-periods
    cuts = antipodal_cuts(ph, start=int(zc[1]))
    land = [int(np.min(np.abs(cuts - z))) for z in zc[1:-1]]         # samples between each reversal and the nearest antipodal cut
    pk = peak_cuts(x, prominence=0.5, distance=half // 2)
    offs = np.asarray([min(abs(ph[z] - ph[e]) for e in pk) / math.pi for z in zc[1:-1]])
    h_rev = float(np.mean(np.abs(H * np.sin(om * tg_[zc[1:-1]]))))
    ext_after = [int(pk[np.searchsorted(pk, z)]) for z in zc[1:-1]]  # the first extremum of m after each interior reversal
    q_off = np.asarray([(e - z) * dt / (T / 4.0) for z, e in zip(zc[1:-1], ext_after)])   # its clock offset in quarter periods
    t_fmax = [(math.floor(om * e * dt / math.pi) * math.pi + math.pi / 2.0) / om for e in ext_after]   # the field's extremum in the same half-cycle
    lag = np.asarray([(e * dt - tf) / (T / 4.0) for e, tf in zip(ext_after, t_fmax)])     # lag of the m-extremum behind the field's, in quarter periods
    crr, null, dom = float(adv.mean()), float(clk.mean()), 1.0
    check = float(np.max(np.abs(adv - 1.0))) < 0.01 and float(offs.min()) > 0.1
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("mag",
        f"Curie-Weiss / Landau mean-field magnet below Tc (a = b = 1, t = -1, spinodal field h_sp = {h_sp:.4f}), overdamped mdot = -(a t m + b m^3 - h) driven by h(t) = H sin(omega t) with H = {H:g} > h_sp, omega = {om:g} (a hysteresis loop; fixed-grid RK4, {n_per} steps per period, {n_cyc} cycles scored after {n_cyc_tr} transient)",
        source="runs/phaseA/crr_retrodictions.txt [c4] (CONSIST)",
        Q="the magnetisation reversals (the system's own events: the sign flips of m at the spinodal jump) are the antipodal cuts of the intrinsic phase of m(t): each reversal is exactly half a turn of phase after the previous one, and it sits away from the extremum of m (H-CUT's antipode-not-extremum reading on a hysteresis loop)",
        ingredient="A3 (antipodal cut on the intrinsic phase, antipodal_cuts), D5 (occasion = one reversal to the next), H-CUT",
        null="the drive's own clock: half a period of the field, T/2",
        domain="the Z2 symmetry of the Landau free energy (m -> -m, h -> -h) with a half-wave antisymmetric drive h(t + T/2) = -h(t): on the periodic attractor m(t + T/2) = -m(t), so reversals are T/2 apart and the analytic signal z(t + T/2) = -z(t) advances its phase by exactly pi between them",
        numbers=(f"{len(zc)} reversals ({len(adv)} interior intervals): phase advance between reversals {crr:.5f} +/- {adv.std():.5f} half-turns; clock advance {null:.5f} +/- {clk.std():.5f} half-periods; "
                 f"antisymmetry max|m(t + T/2) + m(t)| = {anti:.1e}; antipodal cuts seeded at a reversal land within {max(land)} sample(s) of every later reversal; "
                 f"phase offset of a reversal from the nearest extremum of m: {offs.mean():.3f} +/- {offs.std():.3f} half-turns ({len(pk)} extrema); clock offset from a reversal to the next extremum of m: {q_off.mean():.4f} +/- {q_off.std():.4f} quarter periods; lag of the extremum of m behind the extremum of the field: {lag.mean():.4f} +/- {lag.std():.4f} quarter periods; |h| at reversal {h_rev:.4f} against h_sp {h_sp:.4f} (the zero crossing comes after the spinodal at this sweep rate)"),
        tg=f"phase advance {crr:.5f} vs null clock advance {null:.5f} (in half-turns / half-periods): {_word(tg_ok, 'agree', 'differ')}",
        tn=f"the symmetry gives exactly {dom:.1f} half-turn per reversal: the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"every interval within 0.01 of one half-turn and every reversal more than 0.1 half-turn from an extremum: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the antipode lands on the reversal, and so does the clock: {_word(tg_ok, 'the cut adds nothing beyond the half period that the domain symmetry already fixes', 'the cut and the clock disagree')}; "
                 f"the antipode-not-extremum distinction is real (offset {offs.mean():.3f} half-turns, {q_off.mean():.2f} quarter periods on the clock) and is the domain's timing: the extremum of m {_word(abs(lag.mean()) < 0.1, 'sits at', 'does not sit at')} the extremum of the field (lag {lag.mean():.3f} quarter periods) while the reversal is where the spinodal jump completes within the half-cycle; "
                 f"on the paramagnetic side, where the source row lives, no proper-ingredient Q formed: the chi divergence is A1's, and D1's rho across the critical isotherm is the Fisher length, Wootters' count of distinguishable states, information geometry's"),
        weakness="one drive amplitude and one sweep rate; the reversal is located at the zero crossing of m, which at this rate comes after the spinodal field; a drive without half-wave antisymmetry (a biased field) would break the symmetry and is the case where the antipode and the half period could differ, not run here",
        elegance="Push a magnet's field up and then down and it flips over at the same push both ways: the two flips are mirror images, and 'half a turn' is just the mirror.",
        child="A magnet that you push back and forth clicks over at the same push each way, like a light switch. Going up and coming down are mirror images of each other, so the click always comes exactly halfway round.")


# ---------------------------------------------------------------- 28 [d1] scalar random-walk Kalman gain: two readings of Omega = 1
def r3():
    def K_riccati(v, r=1.0):
        q = v * v * r
        M = (q + math.sqrt(q * q + 4.0 * q * r)) / 2.0                  # steady state of M = M r/(M + r) + q
        return M / (M + r), M
    def K_closed(v): return (v / 2.0) * (math.sqrt(v * v + 4.0) - v)  # the source's closed form
    K1, M1 = K_riccati(1.0)
    inv_phi = (math.sqrt(5.0) - 1.0) / 2.0
    K_eq = 0.5                                                       # equal pull: equal precisions 1/M = 1/r
    v_eq = brentq(lambda v: K_closed(v) - K_eq, 0.1, 5.0, xtol=1e-14)
    K_eq_r, M_eq = K_riccati(v_eq)
    K2 = K_closed(2.0)
    internal = rel(K1, K_eq) > TOL_G
    out = outcome(internal=internal)
    return make_row("filt",
        "Scalar random-walk Kalman filter (process variance q, observation variance r, Fisher speed v = sqrt(q/r)); steady-state Riccati M = M r/(M + r) + q, gain K = M/(M + r)",
        source="runs/phaseA/crr_retrodictions.txt [d1] (CONSIST)",
        Q="at Omega = 1 the filter's steady-state gain is fixed by CRR with no constant chosen: reading (i), the source row's, Omega = 1 sets the Fisher speed v = 1 and K = 1/phi; reading (ii), H-EQ's text ('settled past and present exert equal pull in the Fisher norm'), gives the prior and the datum equal precision, M = r, so K = 1/2, which the Riccati equation places at v = 1/sqrt(2)",
        ingredient="H-EQ (Omega = 1, the normalised step) integrated with P4 (the Riccati identity, which CRR.md says is not CRR's)",
        null="the Riccati gain at any v (the domain fixes nothing at any particular speed)",
        domain="steady-state Kalman gain of a random walk (textbook Riccati): K(v) = (v/2)(sqrt(v^2 + 4) - v), K -> 1 as v -> inf, K -> 0 as v -> 0",
        numbers=(f"reading (i): v = 1 -> Riccati M = {M1:.6f}, K = {K1:.6f} (closed form {K_closed(1.0):.6f}; 1/phi = {inv_phi:.6f}); "
                 f"reading (ii): equal precisions M = r -> K = {K_eq:.6f}, reached at v = {v_eq:.6f} (1/sqrt(2) = {1 / math.sqrt(2):.6f}; Riccati check M = {M_eq:.6f}, K = {K_eq_r:.6f}); "
                 f"source's probe v = 2: K = {K2:.6f}; relative difference between the two readings' gains {rel(K1, K_eq):.4f} (TOL_G {TOL_G:g})"),
        tg=f"reading (i) K = {K1:.6f} vs reading (ii) K = {K_eq:.6f}: {_word(rel(K1, K_eq) <= TOL_G, 'agree', 'differ')} (the ingredient has two values on the domain)",
        tn="the Riccati equation gives both gains, at v = 1 and at v = 1/sqrt(2), and selects neither",
        tc="not reached: the two readings of Omega = 1 must agree before Q can be checked",
        out=out,
        reading=(f"the golden-ratio gain belongs to the reading 'Omega = 1 is v = 1', which the source's own weakness line calls the only framework content; the equanimity reading puts the balanced filter at v = {v_eq:.4f} and gives K = {K_eq:.1f}; "
                 f"which of the two Omega = 1 is must be fixed before the domain can be asked, and H-EQ's ledger status (within seed noise of a fixed w = 1 on EQX, cap-dependent on EQ2) offers no third number"),
        weakness="the map from H-EQ's batch gradients to a one-step Gaussian update is a reading, not a derivation: at the prior the past gradient vanishes and the rule's norm ratio is undefined, so the precision (Hessian) form of 'equal pull' is used; P4 says of itself that the formula is not CRR's")


# ---------------------------------------------------------------- 29 [d2] Cramer-Rao unit: the named unit against the estimated unit
def r4():
    rng = np.random.default_rng(0); s, n, K = 1.0, 10, 100000
    means = rng.normal(0.0, s, (K, n)).mean(axis=1)                 # occasion statistic: the occasion mean
    single = rng.normal(0.0, s, K)                                   # per-datum occasions (n = 1)
    named = s / math.sqrt(n)                                         # A1' as the source reads it: 1/sqrt(n I), I = 1/s^2
    est9, est9_std = unit_sigma(means), unit_sigma(means, scale="std")
    est21, est21_std = unit_sigma(means, detrend_window=21), unit_sigma(means, detrend_window=21, scale="std")
    c0_9 = float(savgol_coeffs(9, 2)[4]); c0_21 = float(savgol_coeffs(21, 2)[10])
    pred9, pred21 = named * math.sqrt(1.0 - c0_9), named * math.sqrt(1.0 - c0_21)
    est1, pred1 = unit_sigma(single), s * math.sqrt(1.0 - c0_9)
    internal = rel(named, est9) > TOL_G
    out = outcome(internal=internal)
    return make_row("stat",
        f"Gaussian location family N(mu, s^2), s = {s:g}, observed in occasions of n = {n} draws (K = {K} occasions, occasion statistic = the occasion mean; also per-datum occasions, n = 1)",
        source="runs/phaseA/crr_retrodictions.txt [d2] (DESCR)",
        Q="the unit A1' names (the Cramer-Rao length of the occasion, 1/sqrt(n I) = s/sqrt(n)) is the unit A1''s operational clause estimates (1.4826 MAD of the occasion statistic's residual under the named detrender, unit_sigma), so the two clauses of A1' agree on the one family where the unit is known in closed form",
        ingredient="A1'/D1 (the unit as the system's own resolvable step) in its two readings: named, 1/sqrt(I) (the source's), and estimated, unit_sigma with the registered detrender (window 9, order 2, MAD)",
        null="the Cramer-Rao length itself, the domain's unit",
        domain="Cramer-Rao (Fisher 1925; Rao 1945; Cramer 1946): var >= 1/(n I), I = 1/s^2; and the leverage of a local least-squares fit: the residual of a Savitzky-Golay fit of white noise has variance (1 - c0) times the noise variance, c0 the filter's centre weight",
        numbers=(f"named unit s/sqrt(n) = {named:.6f}; estimated unit (window 9): {est9:.6f} (MAD), {est9_std:.6f} (std); predicted by the leverage sqrt(1 - c0) s/sqrt(n) = {pred9:.6f} with c0 = {c0_9:.6f} (= 59/231); "
                 f"window 21: {est21:.6f} (MAD), {est21_std:.6f} (std), predicted {pred21:.6f} with c0 = {c0_21:.6f}; per datum (n = 1): named {s:.6f}, estimated {est1:.6f}, predicted {pred1:.6f}; "
                 f"ratio estimated/named at window 9: {est9 / named:.4f} (sqrt(1 - c0) = {math.sqrt(1 - c0_9):.4f}); relative difference {rel(named, est9):.4f} (TOL_G {TOL_G:g})"),
        tg=f"named unit {named:.6f} vs estimated unit {est9:.6f}: {_word(rel(named, est9) <= TOL_G, 'agree', 'differ')} (the ingredient has two values on the domain)",
        tn="Cramer-Rao gives the named value and least-squares leverage gives the estimated one: the domain has both numbers and the factor between them",
        tc="not reached: the two readings of A1' must agree before Q can be checked",
        out=out,
        reading=(f"the two clauses of A1' disagree by the factor the detrender sets (sqrt(1 - c0) = {math.sqrt(1 - c0_9):.4f} at window 9, {math.sqrt(1 - c0_21):.4f} at window 21): the operational unit is biased low by the leverage of its own detrender on a family with no trend to remove, and the two readings are one only after the residual scale is divided by sqrt(1 - c0), a correction the instrument does not make; "
                 f"the source's per-datum-versus-per-window question is answered by naming the occasion (D5): the unit scales as 1/sqrt(n) with the occasion's size (per datum {est1:.4f}, per window of {n} {est9:.4f}), which is Fisher additivity, the domain's"),
        weakness=f"the factor is a property of unit_sigma's registered constants, not of the family; every study prereg names the detrender, so the bias is registered, but the rho those studies report is inflated by 1/sqrt(1 - c0) = {1 / math.sqrt(1 - c0_9):.4f} relative to the Cramer-Rao unit on white residuals (a candidate R14 entry for the instrument, not a repair made here)")


# ---------------------------------------------------------------- 30 [d3] drifted Brownian motion: between level crossings the arc is the clock
def r5():
    rng = np.random.default_rng(1); mu, sg, D, dt_f, N = 1.0, 1.0, 1.0, 1e-3, 300000
    X = np.concatenate([[0.0], np.cumsum(mu * dt_f + sg * math.sqrt(dt_f) * rng.normal(size=N))])
    def crossings(x, D):
        run = np.maximum.accumulate(x); ev = [0]; k = 1
        while True:
            j = int(np.searchsorted(run, k * D))                     # first passage of level k D
            if j >= len(x):
                break
            ev.append(j); k += 1
        return np.asarray(ev)
    def eabs(dt):                                                    # E|dX| for dX ~ N(mu dt, sigma^2 dt), per unit time
        z = mu * math.sqrt(dt) / sg
        return sg * math.sqrt(dt) * (math.sqrt(2.0 / math.pi) * math.exp(-z * z / 2.0) + z * (1.0 - 2.0 * norm.cdf(-z))) / dt
    res = {}
    for dt, sub in ((dt_f, 1), (10 * dt_f, 10)):
        x = X[::sub]; ev = crossings(x, D)
        r = regularity(x, ev, sigma=sg * math.sqrt(dt), dt=dt, n_boot=500)   # unit: the increment's own spread sigma sqrt(dt) (per-datum A1' reading)
        mean_dt = float(np.mean(np.diff(ev))) * dt
        r["rate"] = r["C_mean"] * sg * math.sqrt(dt) / mean_dt       # arc per unit time in X units
        r["rate_dom"] = eabs(dt); r["steps_per_sample"] = r["C_mean"] / (mean_dt / dt); r["mean_dt"] = mean_dt
        res[dt] = r
    rf, rc = res[dt_f], res[10 * dt_f]
    crr, null, dom = rf["cv_arc"], rf["cv_clock"], rf["cv_clock"]
    ratio = rf["rate"] / rc["rate"]
    check = (rf["ci95"][0] <= 0.0 <= rf["ci95"][1]) and (rc["ci95"][0] <= 0.0 <= rc["ci95"][1]) and rel(ratio, math.sqrt(10.0)) <= 0.05
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tg_ok_c = rel(rc["cv_arc"], rc["cv_clock"]) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("stoch",
        f"Drifted Brownian motion dX = mu dt + sigma dW (mu = {mu:g}, sigma = {sg:g}) whose own events are the first passages of the levels k Delta (Delta = {D:g}), sampled at dt = {dt_f:g} and the same path at dt = {10 * dt_f:g}",
        source="runs/phaseA/crr_retrodictions.txt [d3] (CONSIST)",
        Q="between consecutive level crossings the Fisher arc (in the increment's own unit sigma sqrt(dt)) is exactly as regular as the clock, CV(C) = CV(Delta t): C is the discretised total variation, Delta t times a constant that the sampling step sets (it scales as 1/sqrt(dt)) up to a sqrt(Delta t) fluctuation, so H-L5 can assign this carrier to neither class",
        ingredient="D5/A1' point-process reading (own events = level crossings, natural time), H-L5's class claim; D2 the arc (not proper)",
        null="the clock: the first-passage (inverse-Gaussian) interval statistics the domain already has",
        domain="Levy: a Brownian path has infinite total variation and finite quadratic variation; on a grid E|dX| = sigma sqrt(dt) [sqrt(2/pi) e^(-z^2/2) + z(1 - 2 Phi(-z))], z = mu sqrt(dt)/sigma, so E[C | Delta t] = Delta t E|dX|/dt by the law of large numbers over the increments: CV(C) = CV(Delta t) at leading order",
        numbers=(f"dt = {dt_f:g}: {rf['n']} occasions, CV(C) = {rf['cv_arc']:.4f}, CV(clock) = {rf['cv_clock']:.4f}, paired-bootstrap 95 % CI of the difference [{rf['ci95'][0]:.4f}, {rf['ci95'][1]:.4f}]; arc per unit time {rf['rate']:.3f} (domain E|dX|/dt = {rf['rate_dom']:.3f}); arc in own units per sample {rf['steps_per_sample']:.4f} (sqrt(2/pi) = {math.sqrt(2 / math.pi):.4f}); "
                 f"dt = {10 * dt_f:g}: {rc['n']} occasions, CV(C) = {rc['cv_arc']:.4f}, CV(clock) = {rc['cv_clock']:.4f}, CI [{rc['ci95'][0]:.4f}, {rc['ci95'][1]:.4f}]; arc per unit time {rc['rate']:.3f} (domain {rc['rate_dom']:.3f}); per sample {rc['steps_per_sample']:.4f}; "
                 f"arc-rate ratio between the grids {ratio:.3f} (sqrt(10) = {math.sqrt(10):.3f}); mean occasion {rf['mean_dt']:.4f} time units (Delta/mu = {D / mu:g})"),
        tg=f"CV(C) {crr:.4f} vs null CV(clock) {null:.4f}: {_word(tg_ok, 'agree', 'differ')}; on the coarse grid {rc['cv_arc']:.4f} vs {rc['cv_clock']:.4f}: {_word(tg_ok_c, 'agree', 'differ')}",
        tn=f"the law of large numbers gives CV(C) = CV(clock) = {dom:.4f} at leading order, and E|dX|/dt = {rf['rate_dom']:.3f} against the observed {rf['rate']:.3f}: the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"CI of CV(C) - CV(clock) includes 0 on both grids and the arc rate scales as sqrt(10) within 5 %: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the diffusion-carrier theorem of the cognitive-collective battery (row 1; AGENT_LOG 21) in the harness's own language: on a diffusion carrier the arc is the clock times a constant the sampling step sets (arc per sample {rf['steps_per_sample']:.3f} and {rc['steps_per_sample']:.3f} own units on the two grids: the arc counts samples), "
                 f"so the CV comparison is the clock against itself and the ingredient did no work; the domain has the theorem; the source row's own content, the sigma/sqrt(T) unit of the drift, is Fisher additivity on the rectifiable carrier (the drift estimate) that a prereg on such data would have to name"),
        weakness="one drift-to-noise ratio and one level spacing; the arc-regular / clock-regular classes are undefined here rather than decided, which is the theorem, not a finding about the process",
        elegance="A shaky path has no length of its own: the closer you look, the longer it gets. So on a shaky road the odometer is only a clock in disguise.",
        child="Measure a very wiggly line with a smaller and smaller ruler and it keeps getting longer and never settles. So for a shaky, wiggly path, adding up the wiggles only tells you how long you watched, like a clock.")


def main():
    return run_batch("Synthesis batch 06: rows 26-30 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
