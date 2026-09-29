"""PRED70 batch P02: stick-slip, relaxation and recharge (H-L5 class claim; H-CUT on a delayed oscillator).
Rows P02-1..P02-5 of Predictions70/declared.py (declared at 8397478, pushed before any model existed; prompt-log entry 234).
[1] a two-block Burridge-Knopoff spring-slider with rate-and-state friction under slow loading; [2] the Olami-Feder-
Christensen cellular automaton; [3] a dripping faucet (mass-spring with mass loss at detachment); [4] a geyser as an
integrate-and-fire recharge; [5] the Suarez-Schopf delayed oscillator. Q, null and H0 are printed verbatim from
declared.py; labels are computed from the numbers (R15). Deterministic: fixed seeds, fixed grids (a fixed-tolerance
Dormand-Prince integrator for the stiff friction model, explicit RK4 for the faucet, Euler-Maruyama for the delay
equation); no data files, no network."""
import math
import os
import sys

import numpy as np
from scipy.signal import lfilter

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P  # noqa: E402

DECL = {p[0]: p for p in P}
N_BOOT, SEED = 2000, 0            # the declaration's fixed H-L5 knobs


def _w(cond, yes, no):
    return yes if cond else no


def _src(pid):
    return f"PRED70 {pid} (declared at 8397478; forecast {DECL[pid][8]})"


def _hl5(r):
    """Q's H-L5 criterion: CV(arc) < CV(clock) with the paired-bootstrap 95 % CI of the difference below 0; a difference
    below 1e-9 (relative) is not resolvable and never counts (R5)."""
    return bool(r["cv_arc"] < r["cv_clock"] and r["ci95"][1] < 0.0 and rel(r["cv_arc"], r["cv_clock"]) > 1e-9)


def _cls(r):
    lo, hi = r["ci95"]
    if lo <= 0.0 <= hi:
        return "CI includes 0"
    return _w(r["cv_arc"] < r["cv_clock"], "arc-regular (CI below 0)", "clock-regular (CI above 0)")


def _rtxt(r):
    return (f"{r['n']} occasions: CV(arc) = {r['cv_arc']:.6f}, CV(clock) = {r['cv_clock']:.6f}, CV(amplitude) = {r['cv_amp']:.6f}, "
            f"C_mean = {r['C_mean']:.4f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) = [{r['ci95'][0]:.6f}, {r['ci95'][1]:.6f}] ({_cls(r)})")


def _ou(n, dt, tau, seed):
    """Unit-variance Ornstein-Uhlenbeck path on a fixed grid (exact AR(1) update), started at 0."""
    a = math.exp(-dt / tau)
    return lfilter([math.sqrt(1.0 - a * a)], [1.0, -a], np.random.default_rng(seed).standard_normal(n))


# ---------------------------------------------------------------- [1] two-block spring-slider, rate-and-state friction
_C = [0, 1 / 5, 3 / 10, 4 / 5, 8 / 9, 1, 1]
_A = [[], [1 / 5], [3 / 40, 9 / 40], [44 / 45, -56 / 15, 32 / 9], [19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729],
      [9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656], [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84]]
_B5 = [35 / 384, 0, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84, 0]
_B4 = [5179 / 57600, 0, 7571 / 16695, 393 / 640, -92097 / 339200, 187 / 2100, 1 / 40]


def _bk_rhs(a, b1, b2, k1, k2, kc, eta, vL=1.0):
    """Quasi-dynamic two-block spring-slider, nondimensional (sigma = v0 = Dc = 1), aging law, log variables:
    psi = ln v, phi = ln theta; k_i (vL t - u_i) + kc (u_j - u_i) = a psi_i + b_i phi_i + eta v_i differentiated in time;
    the fifth state is the Euclidean arc of the displacement path (u1, u2), integral of sqrt(v1^2 + v2^2)."""
    ex = math.exp

    def f(y):
        p1, p2, f1, f2 = y[0], y[1], y[2], y[3]
        v1 = ex(p1); v2 = ex(p2); d1 = ex(-f1) - v1; d2 = ex(-f2) - v2
        return ((k1 * (vL - v1) + kc * (v2 - v1) - b1 * d1) / (a + eta * v1), (k2 * (vL - v2) + kc * (v1 - v2) - b2 * d2) / (a + eta * v2),
                d1, d2, math.sqrt(v1 * v1 + v2 * v2))
    return f


def _dopri(f, y0, T, rtol=1e-7, atol=1e-9, h=1e-3, hmax=0.5):
    """Dormand-Prince 5(4) with fixed tolerances and a deterministic step controller; returns every accepted step."""
    t = 0.0; y = list(y0); n = len(y); ts = [0.0]; ys = [list(y)]
    while t < T:
        h = min(h, T - t, hmax); K = []
        for s in range(7):
            yy = y if s == 0 else [y[i] + h * sum(_A[s][j] * K[j][i] for j in range(s)) for i in range(n)]
            K.append(f(yy))
        y5 = [y[i] + h * sum(_B5[s] * K[s][i] for s in range(7)) for i in range(n)]
        y4 = [y[i] + h * sum(_B4[s] * K[s][i] for s in range(7)) for i in range(n)]
        err = max(abs(y5[i] - y4[i]) / (atol + rtol * max(abs(y[i]), abs(y5[i]))) for i in range(n))
        if err <= 1.0:
            t += h; y = y5; ts.append(t); ys.append(list(y))
        h = h * (min(5.0, max(0.2, 0.9 * err ** -0.2)) if err > 0 else 5.0)
    return np.asarray(ts), np.asarray(ys)


def _bk_onsets(ts, ys, v_on=100.0, v_off=10.0):
    """Slip onsets: max(v1, v2) crosses v_on upward (interpolated in ln v), re-armed when both fall below v_off."""
    lv = np.maximum(ys[:, 0], ys[:, 1]); on = []; armed = True; lon, loff = math.log(v_on), math.log(v_off)
    for i in range(1, len(ts)):
        if armed and lv[i] > lon:
            fr = (lon - lv[i - 1]) / (lv[i] - lv[i - 1]); on.append(ts[i - 1] + fr * (ts[i] - ts[i - 1])); armed = False
        if lv[i] < loff:
            armed = True
    return np.asarray(on), lv


def r1():
    pid = "P02-1"; d = DECL[pid]
    base = dict(a=0.01, b1=0.015, k1=0.002, eta=1e-5)
    y0 = [math.log(0.5), math.log(1.2), 0.0, 0.1, 0.0]
    scan = []; chosen = None
    for b2 in (0.018, 0.02):                                                # declared scan order; the first aperiodic regime is used
        for kc in (0.0005, 0.001, 0.002):
            ts, ys = _dopri(_bk_rhs(b2=b2, k2=0.002, kc=kc, **base), y0, 4000.0)
            on, _ = _bk_onsets(ts, ys); iv = np.diff(on); iv = iv[len(iv) // 3:]
            u = len(np.unique(np.round(iv, 2))); ap = u >= 0.5 * len(iv)
            scan.append((b2, kc, len(iv), u, ap))
            if ap and chosen is None:
                chosen = (b2, kc)
    b2, kc = chosen
    T, dtg = 20000.0, 0.01
    ts, ys = _dopri(_bk_rhs(b2=b2, k2=0.002, kc=kc, **base), y0, T)
    on, lv = _bk_onsets(ts, ys); on = on[on > 2000.0]                       # first 2000 time units dropped (transient)
    A = ys[:, 4]; dA = np.diff(A); slip = np.maximum(lv[1:], lv[:-1]) > math.log(100.0)
    A_creep = np.concatenate([[0.0], np.cumsum(np.where(slip, 0.0, dA))])
    grid = np.arange(0.0, T, dtg)
    carrier_all = np.interp(grid, ts, A); carrier_creep = np.interp(grid, ts, A_creep)
    ev = np.floor(on / dtg).astype(int)
    r_creep = regularity(carrier_creep, ev, sigma=1.0, dt=dtg, n_boot=N_BOOT, seed=SEED)   # primary: the slip is the cut (A3: no content)
    r_all = regularity(carrier_all, ev, sigma=1.0, dt=dtg, n_boot=N_BOOT, seed=SEED)       # sensitivity: the slip's displacement counted in the occasion it starts
    iv = np.diff(on); u_main = len(np.unique(np.round(iv, 2)))
    r = r_creep; crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=None, check=check)
    alt = _hl5(r_all)
    scan_txt = "; ".join(f"b2 = {s[0]:g}, kc = {s[1]:g}: {s[3]} distinct intervals of {s[2]} ({_w(s[4], 'aperiodic', 'periodic')})" for s in scan)
    return make_row(d[2], d[3] + f" (computed as: quasi-dynamic two-block model, nondimensional, aging law, a = 0.01, b1 = 0.015, b2 = {b2:g}, k1 = k2 = 0.002 (k_crit of block 1 = 0.005), coupling kc = {kc:g}, radiation damping eta = 1e-5, loading vL = 1; Dormand-Prince rtol 1e-7 over t = {T:g}, first 2000 dropped; slip onsets where max(v1, v2) crosses 100 vL; carrier = the Euclidean arc of the displacement path (u1, u2) by quadrature, on a {dtg:g} grid)",
                    source=_src(pid), Q=d[5],
                    ingredient=d[4] + " (regularity(); the slip is the cut: the arc accumulated while max(v) > 100 vL is removed from the carrier, so an occasion carries the displacement since the last slip; the slip-included carrier is the sensitivity)",
                    null=d[6], domain=d[7],
                    numbers=(f"regime scan (T = 4000, the first aperiodic entry is used): {scan_txt}; main run: {len(on)} slips, {u_main} distinct intervals; "
                             f"slip excluded (primary): {_rtxt(r_creep)}; slip included: {_rtxt(r_all)}"),
                    tg=f"CV(arc since the last slip) {crr:.6f} vs null CV(clock) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no domain theorem cited (the L5 claim's own class, synthetic)",
                    tc=f"CV(arc) < CV(clock) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"the displacement since the last slip is {_w(crr < null, 'a more', _w(rel(crr, null) <= TOL_G, 'the same', 'a less'))} regular "
                             f"count than the clock ({_cls(r_creep)}); with the slip's own displacement counted in the occasion the class is {_cls(r_all)}, "
                             f"so the verdict {_w(alt == check, 'does not depend', 'depends')} on whether the slip is read as the cut or as content"),
                    weakness=(f"DEVIATION (reading of the occasion): 'the arc of the block displacement since the last slip' is read as the displacement after the slip, the slip itself being the cut; a reader who counts the slip's own displacement gets {_cls(r_all)} and the label {outcome(crr=r_all['cv_arc'], null=r_all['cv_clock'], domain=None, check=alt)}; "
                              "friction parameters, coupling and damping are this row's choices (declared.py names none): the scan above picks the first aperiodic regime of a "
                              "stated list so that the occasions differ; two blocks slipping in quick succession count as two slips; the identity metric on displacement is a stand-in; "
                              "onset threshold 100 vL and re-arm 10 vL are named constants of this row"),
                    elegance="", child="")


# ---------------------------------------------------------------- [2] Olami-Feder-Christensen automaton
def _ofc(L=50, alpha=0.2, n_ev=250000, seed=7):
    """OFC with open boundaries: uniform driving until the most loaded site reaches 1 (the loading added is the clock at
    unit driving rate), then parallel-equivalent stack relaxation, alpha of a toppling site's load to each neighbour."""
    rng = np.random.default_rng(seed); N = L * L
    F = rng.random(N); off = 0.0
    nb = [[j for j in ((i - L) if i >= L else -1, (i + L) if i < N - L else -1, (i - 1) if i % L else -1, (i + 1) if (i + 1) % L else -1) if j >= 0] for i in range(N)]
    sizes = np.empty(n_ev, np.int64); load = np.empty(n_ev); argmax = F.argmax
    for e in range(n_ev):
        i0 = int(argmax()); dl = 1.0 - (F[i0] + off); off += dl; load[e] = dl
        stack = [i0]; s = 0; first = True
        while stack:
            i = stack.pop(); fi = F[i] + off
            if fi < 1.0 and not (first and i == i0):
                continue
            first = False
            give = alpha * fi; F[i] = -off; s += 1
            for j in nb[i]:
                F[j] += give
                if F[j] + off >= 1.0:
                    stack.append(j)
        sizes[e] = s
    return sizes, load


def r2():
    pid = "P02-2"; d = DECL[pid]; burn = 150000
    sizes, load = _ofc(); sizes, load = sizes[burn:], load[burn:]
    t = np.cumsum(load)                                                      # clock time at unit driving rate = loading accumulated
    med = float(np.median(sizes)); big = np.where(sizes > med)[0]
    C_exact = np.diff(t[big]); count = np.diff(big)                           # loading between large events; Varotsos natural time (events)
    dtg = 1e-4; grid_n = int(t[-1] / dtg) + 2
    carrier = np.arange(grid_n) * dtg                                          # the accumulated loading sampled on the clock grid
    ev = np.round(t[big] / dtg).astype(int); ev_u = np.unique(ev)
    r = regularity(carrier, ev_u, sigma=1.0, dt=dtg, n_boot=N_BOOT, seed=SEED)
    dom = cv(count)
    crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row(d[2], d[3] + f" (computed as: open boundaries, uniform driving at unit rate, {burn} events of transient dropped, {len(sizes)} events kept, seed 7; median size {med:g}, so 'above the median' is size > {med:g}: {len(big)} large events)",
                    source=_src(pid), Q=d[5] + " (computed as: CV(loading accumulated between consecutive large events) < CV(clock time between them), paired-bootstrap CI below 0)",
                    ingredient=d[4] + " (regularity() on the accumulated uniform loading sampled on a clock grid of 1e-4)",
                    null=d[6], domain=d[7] + " (computed as: CV of the number of events between consecutive large events)",
                    numbers=(f"instrument (grid 1e-4; {len(ev) - len(ev_u)} large events merged on the grid): {_rtxt(r)}; exact at event resolution: CV(loading) = {cv(C_exact):.6f}, "
                             f"CV(clock) = {cv(C_exact):.6f} (the same numbers: at unit driving rate the clock is the loading); Varotsos natural time: CV(event count) = {dom:.6f}, mean {count.mean():.3f} events"),
                    tg=f"CV(loading) {crr:.6f} vs null CV(clock) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (relative difference {rel(crr, null):.1e})",
                    tn=f"Varotsos natural time gives CV(event count) = {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"CV(loading) < CV(clock) with the paired-bootstrap CI below 0 and a resolvable difference: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"in the OFC automaton the only input is the uniform loading, and the model's time is that loading divided by the driving rate, so the 'natural-time arc' "
                             f"of loading between large events is the clock itself (relative difference {rel(crr, null):.1e}) and cannot be more regular than it; the domain's natural time "
                             f"is a different count, the number of events (CV {dom:.6f}), which is {_w(dom < null, 'more', 'less')} regular than the clock here"),
                    weakness="the clock of a cellular automaton is defined by its driving; a model with a noisy driving rate would separate loading from time, and that is a different system from the declared one",
                    elegance="In a slowly and steadily pushed system, the push you have given it is the clock: counting the load and counting the minutes are the same count.",
                    child="If you add one grain of sand to a pile every second, then counting grains and counting seconds is the same thing. You cannot get a better clock out of the grains than the seconds already are.")


# ---------------------------------------------------------------- [3] dripping faucet
def _drip(Qf, dt, g=1.0, k=1.0, b=0.2, xc=1.0, beta=0.4, xr=0.2, m0=0.6):
    """Mass-spring drop (nondimensional): m' = Q, x' = v, v' = g - (k x + (b + Q) v)/m (inflow arrives at rest);
    detachment when x >= xc: a fraction beta of the mass leaves, the rest recoils to xr with its velocity. RK4, Q held per step."""
    m, x, v, M = m0, m0 * g / k, 0.0, 0.0; n = len(Qf)
    Ms = np.empty(n); ev = []; mpre = []; mpost = []
    for i in range(n):
        q = Qf[i]
        a1 = v; b1 = g - (k * x + (b + q) * v) / m
        m2 = m + 0.5 * dt * q; a2 = v + 0.5 * dt * b1; b2_ = g - (k * (x + 0.5 * dt * a1) + (b + q) * a2) / m2
        a3 = v + 0.5 * dt * b2_; b3 = g - (k * (x + 0.5 * dt * a2) + (b + q) * a3) / m2
        m4 = m + dt * q; a4 = v + dt * b3; b4 = g - (k * (x + dt * a3) + (b + q) * a4) / m4
        x += dt * (a1 + 2 * a2 + 2 * a3 + a4) / 6.0; v += dt * (b1 + 2 * b2_ + 2 * b3 + b4) / 6.0; m = m4; M += dt * q
        if x >= xc:
            mpre.append(m); m *= 1.0 - beta; mpost.append(m); x = xr; ev.append(i)
        Ms[i] = M
    return Ms, np.asarray(ev), np.asarray(mpre), np.asarray(mpost)


def _threshold_model(Qf, dt, mc, mr):
    """H0: the drop leaves at a fixed critical mass mc and a fixed mass mr stays behind."""
    m = mr; ev = []
    for i in range(len(Qf)):
        m += Qf[i] * dt
        if m >= mc:
            ev.append(i); m = mr
    return np.asarray(ev)


def r3():
    pid = "P02-3"; d = DECL[pid]; dt, n, Q0, tau = 0.05, 600000, 0.005, 10.0; skip = 5
    _, ev0, mp0, _ = _drip(np.full(20000 * 5, Q0), dt)
    iv0 = np.diff(ev0[skip:]) * dt; period1 = bool(np.ptp(iv0) <= dt + 1e-12)
    res = {}
    for s in (0.3, 0.1):
        Qf = Q0 * np.exp(s * _ou(n, dt, tau, seed=3) - s * s / 2.0)
        M, ev, mp, mq = _drip(Qf, dt); ev_all = ev; ev = ev[skip:]
        qrec = np.array([Qf[max(0, e - int(tau / dt)):e + 1].mean() for e in ev_all[skip:]])
        r = regularity(M, ev, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED)
        evd = _threshold_model(Qf, dt, float(mp[skip:].mean()), float(mq[skip:].mean()))[skip:]
        rd = regularity(M, evd, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED)
        res[s] = (r, rd, float(mp[skip:].mean()), float(cv(mp[skip:])), float(np.corrcoef(mp[skip:], qrec)[0, 1]))
    r, rd, mc, cvm, cq = res[0.3]
    crr, null, dom = r["cv_arc"], r["cv_clock"], rd["cv_arc"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    r1_, rd1, _, _, _ = res[0.1]
    return make_row(d[2], d[3] + f" (computed as: nondimensional mass-spring drop g = k = 1, damping 0.2, detachment at x = 1 with a fraction 0.4 of the mass leaving and recoil to x = 0.2; mean flow {Q0:g} with lognormal Ornstein-Uhlenbeck flow noise (log-sd 0.3, correlation time {tau:g}), RK4 at dt = {dt:g}, {n} steps, first {skip} drops dropped, seed 3; carrier = cumulative inflow mass)",
                    source=_src(pid), Q=d[5] + " (computed as: CV(inflow mass between drops) < CV(inter-drop time), paired-bootstrap CI below 0)",
                    ingredient=d[4] + " (regularity() on the cumulative inflow, inclusive segments: the inflow has no jump at a drop)",
                    null=d[6], domain=d[7] + " (computed as: the threshold model run on the same flow path, critical mass and retained mass set to the spring model's means, same grid, same instrument)",
                    numbers=(f"noise-free flow: drop intervals {iv0.min():.2f}-{iv0.max():.2f} ({_w(period1, 'period 1 within one step', 'NOT period 1')}); "
                             f"spring model: {_rtxt(r)}; mass at detachment mean {mc:.5f}, CV {cvm:.6f}, correlation with the mean flow over the last {tau:g} time units {cq:.4f}; threshold model on the same flow: CV(inflow) = {dom:.6f}, CV(clock) = {rd['cv_clock']:.6f}; "
                             f"flow noise log-sd 0.1: spring CV(inflow) {r1_['cv_arc']:.6f}, CV(clock) {r1_['cv_clock']:.6f} ({_cls(r1_)}), threshold model CV(inflow) {rd1['cv_arc']:.6f}"),
                    tg=f"CV(inflow) {crr:.6f} vs null CV(time) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the mass-threshold model on the same flow gives CV(inflow) = {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"CV(inflow) < CV(inter-drop time) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"the drop leaves when the spring has stretched to its limit, which here is {_w(cvm < 0.01, 'nearly a fixed', 'a variable')} mass ({mc:.5f}, CV {cvm:.6f}), so the inflow between drops is "
                             f"{_w(crr < null, 'the more', 'the less')} regular count ({_cls(r)}); the threshold model gives the {_w((dom < rd['cv_clock']) == (crr < null), 'same', 'opposite')} direction, with its own CV(inflow) {dom:.6f} on the same flow "
                             f"against the spring model's {crr:.6f}: the values {_w(rel(crr, dom) <= TOL_N, 'agree', 'differ')}; the spring model's mass at detachment varies (CV {cvm:.6f}) and {_w(abs(cq) > 0.5, 'follows', 'does not follow')} the recent flow (correlation {cq:.4f}): the residual is the spring's own dynamics, not a CRR quantity; "
                             "a relative tolerance on two CVs near zero is a hard test for 'the domain has Q'"),
                    weakness="the drop model, its constants and the flow-noise model are this row's choices (declared.py names the class only); the threshold model is calibrated to the spring model's mean masses; the identity metric on mass",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] geyser, integrate-and-fire recharge
def r4():
    pid = "P02-4"; d = DECL[pid]; H, r0, s, tau, dt, n_er = 1.0, 1.0 / 60.0, 0.3, 60.0, 0.1, 300
    n = int(n_er * (H / r0) / dt * 1.3)
    rate = r0 * np.exp(s * _ou(n, dt, tau, seed=4) - s * s / 2.0)          # a positive recharge rate with lognormal OU noise
    h = np.empty(n); x = 0.0; ev = []; inputs = []
    for k in range(n):
        x += rate[k] * dt
        if x >= H:
            inputs.append(x); x = 0.0; ev.append(k)
        h[k] = x
        if len(ev) > n_er + 1:
            break
    h = h[:k + 1]; ev = np.asarray(ev[1:]); inp = np.asarray(inputs[1:])
    r = regularity(h, ev, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED, segment_end="exclusive")    # the reset is the cut (A3), not arc
    J = np.array([h[b - 1] - h[a] for a, b in zip(ev[:-1], ev[1:])])                              # the IF's integrated input over the same samples
    dom = cv(J)
    ri = regularity(h, ev, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED, segment_end="inclusive")
    # white-noise reading: h' = r0 + sig_w xi (perfect integrate-and-fire, inverse-Gaussian intervals)
    sig_w = 0.02; g = np.random.default_rng(5).standard_normal(n); hw = np.empty(n); x = 0.0; evw = []
    for k in range(n):
        x += r0 * dt + sig_w * math.sqrt(dt) * g[k]
        if x >= H:
            x = 0.0; evw.append(k)
        hw[k] = x
    evw = np.asarray(evw[1:]); rw = regularity(hw, evw, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED, segment_end="exclusive")
    Jw = np.array([hw[b - 1] - hw[a] for a, b in zip(evw[:-1], evw[1:])])
    crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    out_w = outcome(crr=rw["cv_arc"], null=rw["cv_clock"], domain=cv(Jw), check=_hl5(rw))
    return make_row(d[2], d[3] + f" (computed as: dh/dt = r(t), eruption when h >= H = 1, reset to 0; r = r0 exp(s eta - s^2/2), r0 = 1/60 per minute, eta a unit OU process (correlation time {tau:g} min), s = {s:g}; dt = {dt:g} min, {len(ev)} eruptions after the first, seed 4)",
                    source=_src(pid), Q=d[5] + " (computed as: CV(arc of the recharge carrier h between eruptions) < CV(interval), paired-bootstrap CI below 0)",
                    ingredient=d[4] + " (regularity() on h, exclusive segments: the reset at an eruption is the cut, A3)",
                    null=d[6], domain=d[7] + " (computed as: the integrated input h(t_b-) - h(t_a+) over the same samples, and its CV)",
                    numbers=(f"{_rtxt(r)}; the IF's integrated input over the same samples: CV {dom:.6f}; continuous-time integrated input at eruption (the threshold plus one step's overshoot): mean {inp.mean():.5f}, CV {cv(inp):.6f}; "
                             f"reset counted inside the arc (inclusive): CV(arc) {ri['cv_arc']:.6f}; white-noise reading (h' = r0 + {sig_w:g} xi, seed 5): {_rtxt(rw)}, integrated input CV {cv(Jw):.6f}, label {out_w}"),
                    tg=f"CV(arc) {crr:.6f} vs null CV(interval) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the integrate-and-fire's integrated input gives CV {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} (relative difference {rel(crr, dom):.1e})",
                    tc=f"CV(arc) < CV(interval) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"with a positive recharge rate the carrier only rises between eruptions, so its arc is its chord, the integrated input, which the threshold fixes up to one sample "
                             f"(CV {crr:.6f} against the interval's {null:.6f}); {_w(rel(crr, dom) <= TOL_N, 'that is the integrate-and-fire statement itself', 'the integrate-and-fire bookkeeping does not reproduce it')}; under the white-noise reading the carrier wanders, its arc "
                             f"is {_w(rw['cv_arc'] < rw['cv_clock'], 'still below', 'no longer below')} the clock's CV ({rw['cv_arc']:.6f} against {rw['cv_clock']:.6f}) and the label is {out_w}"),
                    weakness=("the rate-noise model is this row's choice (a rate is positive, so a lognormal process; the white reading, printed, lets the level fall); the remaining CV(arc) "
                              "is one sample of recharge, so CV(arc) and the domain's value are both quantisation near zero and agree because they are the same samples"),
                    elegance="A geyser is a bucket that fills and tips. However fast or slow the water comes, it always tips at the same fullness, so counting water is a perfect clock and counting minutes is not.",
                    child="Imagine a bucket under a dripping tap that tips over when it is full. On rainy days it fills fast and on dry days slowly, so the minutes between tips change. But the amount of water in each tip is always the same.")


# ---------------------------------------------------------------- [5] Suarez-Schopf delayed oscillator, H-CUT
def _ss(alpha=0.75, delay=6.0, sig=0.1, dt=0.01, tmax=6000.0, seed=6, t_drop=200.0):
    rng = np.random.default_rng(seed); n = int(round(tmax / dt)); dd = int(round(delay / dt))
    T = np.empty(n + 1); T[:dd + 1] = 0.1; xi = rng.standard_normal(n) * sig * math.sqrt(dt)
    for k in range(dd, n):
        x = T[k]; T[k + 1] = x + dt * (x - x * x * x - alpha * T[k - dd]) + xi[k]
    return T[int(round(t_drop / dt)):], dt


def _ss_score(T, dt, h_frac=0.2):
    """Warm episodes between hysteretic zero crossings (band h_frac x max |T|); per episode: the peak (maximum), the next
    downward sign change, the antipodal cut from the peak (phase + pi), the clock midpoint of the peak-to-peak cycle (a)
    and of the peak-to-trough half (b)."""
    h = h_frac * float(np.max(np.abs(T))); ups, downs = [], []; state = 0
    for i in range(1, len(T)):
        if state != 1 and T[i] > h:
            j = i
            while j > 0 and T[j - 1] > 0:
                j -= 1
            ups.append(j); state = 1
        elif state != -1 and T[i] < -h:
            j = i
            while j > 0 and T[j - 1] < 0:
                j -= 1
            downs.append(j); state = -1
    ups, downs = np.asarray(ups), np.asarray(downs)
    ph = intrinsic_phase(T); rows = []
    for i in range(len(ups) - 1):
        u = ups[i]; dn = downs[downs > u]
        if len(dn) == 0 or dn[0] > ups[i + 1]:
            continue
        dcross = int(dn[0]); p = u + int(np.argmax(T[u:dcross]))
        u2 = ups[i + 1]; dn2 = downs[downs > u2]
        if len(dn2) == 0:
            break
        p2 = u2 + int(np.argmax(T[u2:int(dn2[0])])); tr = dcross + int(np.argmin(T[dcross:u2]))
        cuts = antipodal_cuts(ph[p:p + 2 * (p2 - p) + 1], start=0)       # the first half-turn after the peak (a window of two cycles is enough)
        if len(cuts) < 2:
            break
        rows.append((p, dcross, p + int(cuts[1]), p + (p2 - p) / 2.0, p + (tr - p) / 2.0, p2 - p))
    R = np.asarray(rows, float); p, sc, an, ma, mb, per = R.T
    return dict(n=len(R), lag_sc=float(np.mean(sc - p) * dt), lag_an=float(np.mean(an - p) * dt), lag_ma=float(np.mean(ma - p) * dt),
                lag_mb=float(np.mean(mb - p) * dt), lag_tr=float(np.mean(2.0 * (mb - p)) * dt), frac_a=float(np.mean(np.abs(sc - an) < np.abs(sc - ma))),
                frac_b=float(np.mean(np.abs(sc - an) < np.abs(sc - mb))), period=float(np.mean(per) * dt), cv_period=cv(per))


def r5():
    pid = "P02-5"; d = DECL[pid]; delay = 6.0
    res = {sg: _ss_score(*_ss(sig=sg)) for sg in (0.1, 0.05, 0.2)}
    m = res[0.1]
    crr, null, dom = m["lag_an"], m["lag_ma"], delay                     # predicted lag of the sign change after the peak
    check = m["frac_a"] > 0.5
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    out_b = outcome(crr=crr, null=m["lag_mb"], domain=dom, check=m["frac_b"] > 0.5)
    sens = "; ".join(f"noise {sg:g}: {v['n']} episodes, period {v['period']:.3f}, antipode nearer than midpoint (a) on {v['frac_a']:.3f}, than midpoint (b) on {v['frac_b']:.3f}" for sg, v in res.items() if sg != 0.1)
    flips = [sg for sg, v in res.items() if (v["frac_a"] > 0.5) != check]
    return make_row(d[2], d[3] + f" (computed as: dT/dt = T - T^3 - alpha T(t - delay) + noise, alpha = 0.75, delay = 6, additive white noise of intensity 0.1, Euler-Maruyama at dt = 0.01 over t = 6000, first 200 dropped, seed 6; peaks = maxima of warm episodes between hysteretic zero crossings)",
                    source=_src(pid), Q=d[5] + " (computed as: per warm episode, the next downward sign change against (CRR) the antipodal cut half a turn of intrinsic_phase(T) after the peak and (null) the clock midpoint of the peak-to-next-peak cycle; Q holds if the antipode is strictly nearer on more than half of the episodes)",
                    ingredient=d[4] + " (antipodal_cuts started at the peak, first cut)",
                    null=d[6] + " (reading (a), primary: halfway through the peak-to-peak cycle, the clock's half-turn; reading (b), sensitivity: halfway from the peak to the next trough)",
                    domain=d[7] + " (computed as: a period of 4 delays puts the sign change a quarter period, one delay = 6, after the peak)",
                    numbers=(f"{m['n']} episodes, period {m['period']:.3f} (4 delays = {4 * delay:g}), CV(period) {m['cv_period']:.4f}; mean lag after the peak: sign change {m['lag_sc']:.3f}, antipodal cut {m['lag_an']:.3f}, "
                             f"clock midpoint (a) {m['lag_ma']:.3f}, (b) {m['lag_mb']:.3f}; antipode nearer the sign change than midpoint (a) on {m['frac_a']:.3f} of episodes, than midpoint (b) on {m['frac_b']:.3f}; "
                             f"label with null (b): {out_b}; {sens}"),
                    tg=f"antipode lag {crr:.3f} vs null (clock midpoint (a)) lag {null:.3f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"H0's quarter period (one delay) gives a lag of {dom:g}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"antipode nearer the sign change on more than half of the episodes: {_w(check, 'holds', 'fails')} ({m['frac_a']:.3f}) -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"half a turn of the analytic phase after a warm peak lands {m['lag_an']:.3f} after it (the trough comes at {m['lag_tr']:.3f}), and half the clock cycle at {m['lag_ma']:.3f}; "
                             f"the sign change comes {m['lag_sc']:.3f} after the peak, {_w(abs(m['lag_sc'] - delay) < abs(m['lag_sc'] - m['lag_an']), 'nearer the one-delay lag of the delayed-oscillator picture', 'nearer the half-turn')}; "
                             f"the antipode and the clock half-cycle are {_w(rel(crr, null) <= TOL_G, 'the same prediction here, so which is nearer is decided by noise', 'different predictions here')} ({m['frac_a']:.3f}); "
                             f"against the peak-to-trough midpoint the antipode is nearer on {m['frac_b']:.3f}; the verdict {_w(flips, 'changes', 'does not change')} with the noise level"),
                    weakness=("DEVIATION (reading of the null): the Q's 'halfway in clock time' needs two endpoints that declared.py does not name; the primary reading is the cycle's half (the clock's counterpart of half a turn), "
                              f"the peak-to-trough reading is printed and gives {_w(out_b == out, 'the same label', 'a different label, ' + out_b)}; the model period is {m['period']:.3f} against H0's 4 delays = {4 * delay:g} "
                              f"(relative difference {rel(m['period'], 4 * delay):.3f}); the noise level is this row's choice"),
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P02: stick-slip, relaxation and recharge (declared at 8397478; prompt-log entry 234)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
