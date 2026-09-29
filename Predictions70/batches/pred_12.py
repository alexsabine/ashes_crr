"""PRED70 batch P12: climate and earth (Predictions70/DECLARATION.md; declared.py pushed at 8397478 before this file existed).
[1] Budyko-Sellers energy balance with a dynamic ice line (Widiasih form), the albedo set by the A6-remembered ice line:
hysteresis width; [2] Stommel's two-box thermohaline model under slow freshwater forcing: collapse against half the arc
from on to off; [3] Daisyworld with daisy growth on A6-remembered local temperature: the regulated luminosity range;
[4] a Saltzman-Maasch glacial oscillator with noise: H-L5 between terminations; [5] annual floods (Gumbel maxima from
Poisson flood events with exponential peaks): exceedances of the 10-year flood in natural time. Literature named by name
and year only (R10): Budyko 1969; Sellers 1969; Widiasih 2013; Stommel 1961; Watson and Lovelock 1983; Saltzman and
Maasch 1990; Gumbel 1958; Varotsos, Sarlis and Skordas 2002 (natural time). Q, null and H0 are printed
verbatim from declared.py. Deterministic (fixed seeds, fixed grids, explicit RK4); under two minutes."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P as _DECLARED  # noqa: E402

from crr.instrument.core import regularity  # noqa: E402
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch  # noqa: E402

D = {p[0]: p for p in _DECLARED}
QGRID = (0.25, 0.5, 0.75)
Q_A6 = 0.5


def _w(cond, yes, no):
    return yes if cond else no


def _src(pid):
    return f"PRED70 {pid} (declared at 8397478; forecast {D[pid][8]})"


def _held(check):
    return "-> not computable" if check is None else _w(check, "-> Q holds", "-> Q fails")


def _ci(r):
    return f"[{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}]"


# ---------------------------------------------------------------- [1] Budyko-Sellers with an A6-remembered ice line
BA, BB, BC, A1, A2, TC = 202.0, 1.9, 3.04, 0.32, 0.62, -10.0                  # W/m2, W/m2/C, W/m2/C, albedos, ice-line temperature (C)
A0 = (A1 + A2) / 2; WID = 0.05                                                 # albedo at the ice edge; width of the smoothed albedo step


def _s(y):
    return 1 - 0.241 * (3 * y * y - 1)


def _abar(e):
    S = e - 0.241 * (e ** 3 - e)
    return A1 * S + A2 * (1 - S)


def _h(eta, M, Q):
    """Equilibrium temperature at the ice line eta when the albedo follows the ice line M (M = eta: Budyko)."""
    al = A0 + (A2 - A1) / 2 * math.tanh((eta - M) / WID)
    Tbar = (Q * (1 - _abar(M)) - BA) / BB
    return (Q * _s(eta) * (1 - al) - BA + BC * Tbar) / (BB + BC)


def _Qc(e):
    """Q at which eta is an equilibrium (h(eta, eta, Q) = TC): h is linear in Q."""
    return (TC * (BB + BC) + BA * (1 + BC / BB)) / (_s(e) * (1 - A0) + (BC / BB) * (1 - _abar(e)))


def _budyko_eps():
    lo, hi = 0.61, 1.0                                                         # the small-cap equilibrium at Q = 343 by bisection
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if _Qc(mid) < 343.0: lo = mid
        else: hi = mid
    e = 0.5 * (lo + hi); d = 1e-6
    slope = (_h(e + d, e + d, 343.0) - _h(e - d, e - d, 343.0)) / (2 * d)
    return 1e-3 / abs(slope), e, slope                                         # eps: ice-line relaxation time 1000 yr at Q = 343


def _budyko_static(Tm, eps, grid=np.linspace(0.0, 1.0, 20001)):
    """Quasi-static loop of the (eta, M) system: equilibria are M = eta, Q = Qc(eta); the down-jump is where the stable
    small-cap branch (followed from eta = 1 downwards) first loses stability (eigenvalue of the 2x2 Jacobian with
    non-negative real part) or folds; the up-jump leaves the snowball (eta = 0) at Qc(0)."""
    q = np.array([_Qc(e) for e in grid]); ifold = int(np.argmin(q)); d = 1e-6; lost = None
    for i in range(len(grid) - 1, ifold, -1):
        e = grid[i]; Q = q[i]
        he = (_h(e + d, e, Q) - _h(e - d, e, Q)) / (2 * d); hm = (_h(e, e + d, Q) - _h(e, e - d, Q)) / (2 * d)
        J = np.array([[eps * he, eps * hm], [1.0 / Tm, -1.0 / Tm]]) if Tm > 0 else np.array([[eps * (he + hm)]])
        if np.linalg.eigvals(J).real.max() >= 0: lost = (float(e), float(Q)); break
    qdown = lost[1] if lost else float(q[ifold])
    return _Qc(0.0) - qdown, qdown, _Qc(0.0), float(grid[ifold]), lost


def _budyko_ramp(Tm, eps, legyears, dt, det=0.3):
    """Q ramps 360 -> 280 -> 460 W/m2 at 45 W/m2 per legyears; RK4; eta clamped to [0, 1]; jump detected when eta crosses det."""
    rate = 45.0 / legyears; eta = M = 1.0; Q = 360.0; leg = -1; qd = qu = None

    def f(eta, M, Q):
        de = eps * (_h(eta, M if Tm > 0 else eta, Q) - TC)
        if (eta <= 0.0 and de < 0) or (eta >= 1.0 and de > 0): de = 0.0
        return de, (0.0 if Tm == 0 else (eta - M) / Tm)
    while True:
        Qm, Qn = Q + leg * rate * dt / 2, Q + leg * rate * dt
        k1 = f(eta, M, Q); k2 = f(eta + dt / 2 * k1[0], M + dt / 2 * k1[1], Qm); k3 = f(eta + dt / 2 * k2[0], M + dt / 2 * k2[1], Qm)
        k4 = f(eta + dt * k3[0], M + dt * k3[1], Qn)
        en = min(1.0, max(0.0, eta + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6)); M += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        if leg < 0 and qd is None and eta >= det > en: qd = Qn
        if leg > 0 and qu is None and eta < det <= en: qu = Qn
        eta, Q = en, Qn
        if leg < 0 and Q <= 280.0: leg = 1
        if leg > 0 and Q >= 460.0: break
    return (qu - qd) if (qu is not None and qd is not None) else float("nan"), qd, qu


def r1():
    pid = "P12-1"; d = D[pid]
    eps, e343, slope = _budyko_eps(); occ = 1000.0                                   # occasion = the ice line's own relaxation time, 1000 yr
    Tm = occ * Q_A6 / (1 - Q_A6)
    Wm, qdm, qum, efold, lostm = _budyko_static(Tm, eps); W0, qd0, qu0, _, lost0 = _budyko_static(0.0, eps)
    Wdom = _Qc(0.0) - min(_Qc(e) for e in np.linspace(0.0, 1.0, 200001))       # Budyko's static loop, closed form on a finer grid
    crr, null, dom = Wm, W0, Wdom; check = Wm > 1.01 * W0
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    qg = "; ".join(f"q {q}: T_m {occ * q / (1 - q):.0f} yr, quasi-static width {_budyko_static(occ * q / (1 - q), eps)[0]:.4f}" for q in QGRID)
    dyn = []
    for ly, dt in ((1e5, 5.0), (1e6, 20.0), (1e7, 100.0)):
        wn = _budyko_ramp(0.0, eps, ly, dt); wm = _budyko_ramp(Tm, eps, ly, dt)
        dyn.append((ly, wn[0], wm[0], wm[0] / wn[0] - 1))
    dyn_txt = "; ".join(f"45 W/m2 per {ly:.0e} yr: width {wn:.3f} without memory, {wm:.3f} with (widening {wd:+.4f})" for ly, wn, wm, wd in dyn)
    flips = [ly for ly, wn, wm, wd in dyn if (wd > 0.01) != check]
    return make_row(d[2], d[3] + f"; model: Budyko's annual-mean EBM with Legendre insolation s(y) = 1 - 0.241 (3 y^2 - 1), A = {BA:g}, B = {BB}, C = {BC}, albedo {A1}/{A2} (edge {A0:.2f}, smoothed step width {WID}), T_c = {TC:g} C; ice line d eta/dt = eps (T(eta) - T_c) (Widiasih), eps set so the ice line relaxes in 1000 yr at Q = 343 W/m2 (eta = {e343:.4f})",
                    source=_src(pid), Q=d[5] + " (computed as: the quasi-static loop width in Q (W/m2), the down-jump where the stable small-cap branch of the (eta, M) system folds or loses stability, the up-jump where the snowball ends; finite-rate ramps printed as sensitivity)",
                    ingredient=d[4] + f" with P3's exponential kernel on the ice line the albedo follows: dM/dt = (eta - M)/T_m, T_m = q/(1 - q) occasions, q = {Q_A6}; occasion = the ice line's own relaxation time, {occ:.0f} yr",
                    null=d[6], domain=d[7],
                    numbers=f"quasi-static: with memory width {Wm:.4f} W/m2 (down-jump {qdm:.4f}{_w(lostm is None, ' at the fold', ' at a loss of stability before the fold')}, up-jump {qum:.4f}); without memory {W0:.4f} (down {qd0:.4f}, up {qu0:.4f}); Budyko's closed form {Wdom:.4f} (fold at eta = {efold:.4f}); q-grid: {qg}; finite-rate ramps (jump at eta = 0.3): {dyn_txt}",
                    tg=f"width {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the static bistability gives {dom:.4f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"quasi-static width with memory above 1.01 x without ({crr:.4f} against {1.01 * null:.4f}): {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"a remembered ice line has the same equilibria (M = eta) and {_w(lostm is None, 'keeps the small-cap branch stable up to the fold', 'destabilises part of the branch')}, so the quasi-static loop is {_w(rel(Wm, W0) <= TOL_G, 'unchanged', 'changed')} ({Wm:.4f} against {W0:.4f} W/m2), as the static theory says; at a finite forcing rate the memory adds lag and the loop {_w(all(x[3] > 0 for x in dyn), 'widens', 'changes')} ({', '.join(f'{wd:+.4f} at 45 W/m2 per {ly:.0e} yr' for ly, wn, wm, wd in dyn)}), a rate effect that {_w(all(abs(b_[3]) < abs(a_[3]) for a_, b_ in zip(dyn[:-1], dyn[1:])), 'shrinks at every tenfold slowing of the ramp', 'does not shrink at every tenfold slowing of the ramp')}",
                    weakness=f"DEVIATION: declared.py does not say whether the loop is quasi-static or swept at a finite rate; the decisive width is the quasi-static one (the loop as a property of the system, H0's reading); ramp rates on which the finite-rate widening would flip the verdict: {', '.join(f'{ly:.0e} yr per leg' for ly in flips) if flips else 'none'} ({len(flips)} of {len(dyn)}){_w(len(flips) > 1, ', so the verdict is FRAGILE to the protocol: it holds only in the quasi-static limit', '')}. The occasion (1000 yr) and eps are named choices; the quasi-static verdict does not depend on them. A smoothed albedo step (width {WID}) replaces Budyko's discontinuity so that the remembered line enters smoothly",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] Stommel: collapse against half the arc from on to off
E1, E3 = 3.0, 0.3


def _stommel_sn():
    """Equilibria with q = T - S > 0: T = E1/(1 + q), S = F/(E3 + q), so F(q) = (E3 + q)(E1/(1 + q) - q); the saddle-node is max F."""
    qs = np.linspace(1e-6, 3.0, 3000001); F = (E3 + qs) * (E1 / (1 + qs) - qs); i = int(np.argmax(F))
    return float(qs[i]), float(F[i]), (-1 + math.sqrt(1 + 4 * E1)) / 2


def _stommel_run(rate, dt=0.01, hold=200.0):
    """dT/dt = E1 - T - |T - S| T, dS/dt = F - E3 S - |T - S| S; F ramps from 0 at `rate` until the circulation reverses
    (q < 0), then is held while the system settles on the off state. RK4."""
    q_on = (-1 + math.sqrt(1 + 4 * E1)) / 2; T = E1 / (1 + q_on); S = 0.0; F = 0.0; qs = [T - S]; Fs = [F]; held = None

    def f(T, S, F):
        q = T - S
        return E1 - T - abs(q) * T, F - E3 * S - abs(q) * S
    while True:
        k1 = f(T, S, F); k2 = f(T + dt / 2 * k1[0], S + dt / 2 * k1[1], F); k3 = f(T + dt / 2 * k2[0], S + dt / 2 * k2[1], F)
        k4 = f(T + dt * k3[0], S + dt * k3[1], F)
        T += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; S += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        if held is None:
            F += rate * dt
            if T - S < 0: held = 0.0
        else:
            held += dt
            if held > hold: break
        qs.append(T - S); Fs.append(F)
    return np.array(qs), np.array(Fs)


def _stommel_positions(rate, F_sn):
    q, F = _stommel_run(rate); s = np.r_[0.0, np.cumsum(np.abs(np.diff(q)))]; tot = float(s[-1])
    i_sn = int(np.argmax(F >= F_sn)); i_col = int(np.argmax(np.abs(np.diff(q)))); i_zero = int(np.argmax(q < 0)); i_anti = int(np.argmax(s >= tot / 2))
    return dict(tot=tot, anti=tot / 2, sn=float(s[i_sn]), col=float(s[i_col]), zero=float(s[i_zero]), F_anti=float(F[i_anti]),
                F_col=float(F[i_col]), q_off=float(q[-1]))


def r2():
    pid = "P12-2"; d = D[pid]
    q_sn, F_sn, q_on = _stommel_sn()
    P = _stommel_positions(1e-4, F_sn); Pf = _stommel_positions(1e-3, F_sn)
    crr, null, dom = P["anti"], P["sn"], q_on - q_sn
    check = rel(P["col"], P["anti"]) <= TOL_N
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    nearer = _w(abs(P["col"] - P["anti"]) < abs(P["col"] - P["sn"]), "the antipode", "the saddle-node")
    return make_row(d[2], d[3] + f"; model: dT/dt = eta1 - T - |T - S| T, dS/dt = F - eta3 S - |T - S| S, eta1 = {E1}, eta3 = {E3}, circulation q = T - S; F ramped from 0 at 1e-4 per unit time until q < 0, then held 200 time units; RK4 dt 0.01",
                    source=_src(pid), Q=d[5] + " (computed as: the arc of q (identity metric) from the on state at F = 0 to the settled off state; the antipode at half of it; the collapse is the system's own event, the steepest change of q; positions compared in arc, within 1 %)",
                    ingredient=d[4] + " (the carrier does not oscillate, so the analytic-signal phase is not used; the antipode is read, as declared, as half the arc from on to off)",
                    null=d[6], domain=d[7],
                    numbers=f"total arc on -> off {P['tot']:.4f} (q from {q_on:.4f} to {P['q_off']:.4f}); arc position of the antipode {P['anti']:.4f}, of the ramp passing the saddle-node F = {F_sn:.4f} {P['sn']:.4f}, of the collapse (steepest change of q) {P['col']:.4f}, of the reversal q = 0 {P['zero']:.4f}; Stommel's quasi-static arc to the saddle-node q_on - q_SN = {dom:.4f} (q_SN = {q_sn:.4f}); forcing at the antipode {P['F_anti']:.4f}, at the collapse {P['F_col']:.4f}; the collapse lies nearer {nearer}; faster ramp (1e-3): antipode {Pf['anti']:.4f}, saddle-node {Pf['sn']:.4f}, collapse {Pf['col']:.4f}",
                    tg=f"antipode {crr:.4f} vs saddle-node {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Stommel's quasi-static saddle-node at arc {dom:.4f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"collapse at arc {P['col']:.4f} within 1 % of the antipode {P['anti']:.4f}: {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"half the arc from on to off falls at {P['anti']:.4f}, {_w(P['anti'] < P['sn'], 'before', 'after')} the saddle-node ({P['sn']:.4f}) and {_w(P['anti'] < P['col'], 'before', 'after')} the collapse ({P['col']:.4f}): the circulation weakens along the on branch and then drops in one jump, and where the midpoint of that path lies depends on how far the on state sits from the fold, not on the fold; in forcing the collapse comes at F = {P['F_col']:.4f} against the saddle-node {F_sn:.4f} ({rel(P['F_col'], F_sn):.4f} relative, {_w(rel(P['F_col'], F_sn) <= TOL_N, 'where the domain says', 'away from where the domain says')}) and the antipode at F = {P['F_anti']:.4f} ({rel(P['F_anti'], P['F_col']):.4f} from the collapse)",
                    weakness="the on state is taken at zero freshwater forcing and the off state is the one reached with the forcing held at reversal; other endpoints move the antipode (the arc depends on them), which is itself a reason the half-arc cannot be the collapse law; one parameter set",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] Daisyworld with A6-remembered temperature
DS, SIG, QH, AW, AB, AG, GAM = 917.0, 5.67e-8, 2.06e9, 0.75, 0.25, 0.5, 0.3


def _daisy(Tm, dur, L0=0.5, L1=1.8, dt=0.2, floor=0.01, every=10):
    """Watson-Lovelock 1983: d aw/dt = aw (x beta(Tw) - gamma), d ab/dt = ab (x beta(Tb) - gamma), x = 1 - aw - ab,
    beta(T) = max(0, 1 - 0.003265 (22.5 - T)^2); local T_i^4 = q (A - A_i) + Te^4; growth uses the A6-remembered local
    temperature M_i, dM_i/dt = (T_i - M_i)/Tm (Tm = 0: instantaneous); L ramps from L0 to L1 over `dur`; seeds kept at 0.01."""
    def temps(aw, ab, L):
        A = aw * AW + ab * AB + (1 - aw - ab) * AG; Te4 = DS * L * (1 - A) / SIG
        return (QH * (A - AW) + Te4) ** 0.25 - 273.15, (QH * (A - AB) + Te4) ** 0.25 - 273.15

    def beta(T):
        return max(0.0, 1 - 0.003265 * (22.5 - T) ** 2)

    def f(aw, ab, Mw, Mb, L):
        Tw, Tb = temps(aw, ab, L); x = 1 - aw - ab
        if Tm > 0:
            return aw * (x * beta(Mw) - GAM), ab * (x * beta(Mb) - GAM), (Tw - Mw) / Tm, (Tb - Mb) / Tm
        return aw * (x * beta(Tw) - GAM), ab * (x * beta(Tb) - GAM), 0.0, 0.0
    aw = ab = floor; L = L0; Mw, Mb = temps(aw, ab, L); n = int(round(dur / dt)); rate = (L1 - L0) / dur; Ls, cov = [], []
    for i in range(n):
        s = (aw, ab, Mw, Mb); Lm, Ln = L + rate * dt / 2, L + rate * dt
        k1 = f(*s, L); k2 = f(*[a + dt / 2 * b for a, b in zip(s, k1)], Lm); k3 = f(*[a + dt / 2 * b for a, b in zip(s, k2)], Lm)
        k4 = f(*[a + dt * b for a, b in zip(s, k3)], Ln)
        aw, ab, Mw, Mb = (a + dt * (b + 2 * c + 2 * e + g) / 6 for a, b, c, e, g in zip(s, k1, k2, k3, k4))
        aw = max(aw, floor); ab = max(ab, floor); L = Ln
        if i % every == 0: Ls.append(L); cov.append(aw + ab)
    return np.array(Ls), np.array(cov)


def _range(Ls, cov, thr):
    idx = np.where(cov >= thr)[0]
    return (float(Ls[idx[-1]] - Ls[idx[0]]), float(Ls[idx[0]]), float(Ls[idx[-1]])) if len(idx) else (0.0, float("nan"), float("nan"))


def r3():
    pid = "P12-3"; d = D[pid]
    occ = 1.0 / GAM; Tm = occ * Q_A6 / (1 - Q_A6); dur = 20000.0; thr = 0.05
    Lm_, cm = _daisy(Tm, dur); L0_, c0 = _daisy(0.0, dur)
    (wm, lm, hm), (w0, l0, h0) = _range(Lm_, cm, thr), _range(L0_, c0, thr)
    crr, null = wm, w0; check = wm < 0.99 * w0
    out = outcome(crr=crr, null=null, domain=None, check=check)
    qg = []
    for q in QGRID:
        if q == Q_A6: qg.append((q, occ * q / (1 - q), wm)); continue
        Lq, cq = _daisy(occ * q / (1 - q), dur); qg.append((q, occ * q / (1 - q), _range(Lq, cq, thr)[0]))
    thr2 = [(t_, _range(Lm_, cm, t_)[0], _range(L0_, c0, t_)[0]) for t_ in (0.2,)]
    Lf, cf = _daisy(Tm, 5000.0); Lf0, cf0 = _daisy(0.0, 5000.0); wf, wf0 = _range(Lf, cf, thr)[0], _range(Lf0, cf0, thr)[0]
    sens = [(f"cover threshold {t_}", a_, b_) for t_, a_, b_ in thr2] + [("ramp over 5000 time units", wf, wf0)]
    flips = [nm for nm, a_, b_ in sens if (a_ < 0.99 * b_) != check]
    return make_row(d[2], d[3] + f"; model: Watson and Lovelock 1983 (S = {DS:g} W/m2, q = {QH:g} K^4, albedos {AW}/{AB}/{AG}, gamma = {GAM}, seeds 0.01); luminosity ramped from 0.5 to 1.8 over {dur:.0f} time units; RK4 dt 0.2; regulated range = luminosities at which the daisy cover is at least {thr}",
                    source=_src(pid), Q=d[5] + f" (computed as: the width of the luminosity interval with daisy cover >= {thr} on the slow up-ramp, with growth on the A6-remembered local temperatures against the instantaneous ones)",
                    ingredient=d[4] + f" with P3's exponential kernel: dM_i/dt = (T_i - M_i)/T_m, T_m = q/(1 - q) occasions, q = {Q_A6}; occasion = one daisy lifetime 1/gamma = {occ:.3f} time units",
                    null=d[6], domain=d[7],
                    numbers=f"regulated range: with memory {wm:.4f} (L {lm:.4f} to {hm:.4f}), without {w0:.4f} (L {l0:.4f} to {h0:.4f}); relative change {wm / w0 - 1:+.4f}; q-grid: " + "; ".join(f"q {q}: T_m {t:.3f}, width {w:.4f}" for q, t, w in qg) + "; sensitivity (with / without memory): " + "; ".join(f"{nm}: {a_:.4f} / {b_:.4f}" for nm, a_, b_ in sens),
                    tg=f"width {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"width with memory below 0.99 x without ({crr:.4f} against {0.99 * null:.4f}): {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"remembered temperature leaves Daisyworld's equilibria where they were and only adds lag to a slow ramp, so the regulated range {_w(wm < w0, 'narrows', 'widens')} by {abs(wm / w0 - 1):.4f} (relative), {_w(rel(wm, w0) <= TOL_G, 'within 1 %: the regulation is a property of the daisy-albedo feedback at steady state, not of how quickly the daisies read the temperature', 'beyond 1 %: how quickly the daisies read the temperature changes the regulation')}",
                    weakness=f"the regulated range is read from one slow ramp (Watson and Lovelock's protocol), not from a continuation of equilibria; sensitivity cells that flip the verdict: {', '.join(flips) if flips else 'none'} ({len(flips)} of {len(sens)}); the occasion (one daisy lifetime) is a named choice, the q-grid spans a factor {qg[-1][1] / qg[0][1]:.0f} in memory length",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] Saltzman-Maasch glacial oscillator: H-L5 between terminations
SMP = (1.0, 1.2, 0.8, 0.8)                                                     # p, q, r, s


def _sm(units, sig, seed, dt=0.01, tc=0.1, burn=100.0):
    """dX/dt = -X - Y + xi, dY/dt = -p Z + r Y + s Z^2 - Z^2 Y, dZ/dt = -q (X + Z) (X ice volume, Y CO2, Z deep-ocean
    temperature; time unit 10 kyr); xi an OU process (sd sig, correlation time tc) on the ice-volume tendency. RK4."""
    p, q, r, s = SMP; rng = np.random.default_rng(seed); n = int(round(units / dt)); a = math.exp(-dt / tc); b = sig * math.sqrt(1 - a * a)
    e = rng.standard_normal(n); z = 0.0; X, Y, Z = 0.1, 0.1, 0.1; out = np.empty((n + 1, 3)); out[0] = (X, Y, Z)

    def f(X, Y, Z, xi):
        return -X - Y + xi, -p * Z + r * Y + s * Z * Z - Z * Z * Y, -q * (X + Z)
    for i in range(n):
        z = a * z + b * e[i]
        k1 = f(X, Y, Z, z); k2 = f(X + dt / 2 * k1[0], Y + dt / 2 * k1[1], Z + dt / 2 * k1[2], z)
        k3 = f(X + dt / 2 * k2[0], Y + dt / 2 * k2[1], Z + dt / 2 * k2[2], z); k4 = f(X + dt * k3[0], Y + dt * k3[1], Z + dt * k3[2], z)
        X += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; Y += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        Z += dt * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6; out[i + 1] = (X, Y, Z)
    return out[int(round(burn / dt)):]


def _terminations(X, h=0.5):
    """Own events: a deglaciation is a fall of X from above mean + h sd to below mean - h sd; the event is the sample where
    X crosses its mean on that fall (a Schmitt trigger, so noise cannot double-count)."""
    m, sd = X.mean(), X.std(); hi = False; ev = []
    for i in range(1, len(X)):
        if X[i] > m + h * sd: hi = True
        if hi and X[i] < m - h * sd:
            j = i
            while X[j] < m: j -= 1
            ev.append(j + 1); hi = False
    return np.array(ev)


def r4():
    pid = "P12-4"; d = D[pid]
    O = _sm(2200.0, 0.5, 7); ev = _terminations(O[:, 0])
    r = regularity(O[:, 0], ev, dt=0.01); r3 = regularity(O / O.std(axis=0), ev, dt=0.01)
    crr, null = r["cv_arc"], r["cv_clock"]; check = r["ci95"][1] < 0
    out = outcome(crr=crr, null=null, domain=None, check=check)
    sens = []
    for sg in (0.2, 1.0):
        Os = _sm(1200.0, sg, 8); sens.append((sg, regularity(Os[:, 0], _terminations(Os[:, 0]), dt=0.01)))
    flips = [sg for sg, x in sens if (x["ci95"][1] < 0) != check] + (["three-variable arc"] if (r3["ci95"][1] < 0) != check else [])
    T = float(np.mean(np.diff(ev)) * 0.01)
    return make_row(d[2], d[3] + f"; model: dX/dt = -X - Y + xi, dY/dt = -p Z + r Y + s Z^2 - Z^2 Y, dZ/dt = -q (X + Z), (p, q, r, s) = {SMP} (a Saltzman-Maasch parameter set giving a ~100-kyr cycle; time unit 10 kyr); OU noise sd 0.5, correlation 1 kyr, on the ice tendency; RK4 dt 0.01 over 2200 units, first 100 discarded; own events = terminations (Schmitt trigger at +-0.5 sd); {r['n']} cycles, mean period {T:.3f} units, seed 7",
                    source=_src(pid), Q=d[5] + " (computed as: arc of the ice volume X between terminations against the time between them; paired bootstrap n_boot 2000 seed 0, CI excluding 0 below)",
                    ingredient=d[4] + " (regularity on X, identity metric, segment_end inclusive)",
                    null=d[6], domain=d[7],
                    numbers=f"CV(arc per cycle) {crr:.4f}, CV(period) {null:.4f}, difference {r['diff']:+.4f}, 95 % CI {_ci(r)}; amplitude control CV {r['cv_amp']:.4f}; three-variable arc (X, Y, Z each in its own sd): CV {r3['cv_arc']:.4f}, CI {_ci(r3)}; noise sensitivity (1100 units, seed 8): " + "; ".join(f"sd {sg}: CV(arc) {x['cv_arc']:.4f}, CV(period) {x['cv_clock']:.4f}, CI {_ci(x)}" for sg, x in sens),
                    tg=f"CV(arc) {crr:.4f} vs null CV(period) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"CV(arc) - CV(period) CI {_ci(r)} lies below 0: {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"the glacial cycle of this oscillator is {_w(crr < null, 'arc-regular', 'clock-regular')}: under noise the ice-volume arc per cycle varies {_w(crr > null, 'more', 'less')} (CV {crr:.4f}) than the time between terminations (CV {null:.4f}), and the size of the excursion varies {_w(r['cv_amp'] > crr, 'more', 'less')} than the arc (CV {r['cv_amp']:.4f}); this unforced limit cycle with CO2 and deep-ocean feedback keeps its timing {_w(null < r['cv_amp'], 'better', 'worse')} than its amplitude",
                    weakness=f"one parameter set of the Saltzman-Maasch form, unforced (orbital forcing, which could pace the period, is absent); noise enters the tendency through a smooth OU process so the arc converges as dt shrinks; sensitivity cells that flip the verdict: {', '.join(str(x) for x in flips) if flips else 'none'} ({len(flips)} of 3)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] annual floods: exceedances of the 10-year flood in natural time
def _floods(nu, years, seed, beta=1.0, block=10):
    """Flood events Poisson(nu) per year with exponential peaks (scale beta) above a base level, so annual maxima are Gumbel
    (location beta ln nu, scale beta); the 10-year flood x10 is the Gumbel 0.9 quantile. Natural time counts events; one
    natural-time year is nu events. Returns rates, dispersion indices of exceedance counts per block and the annual check."""
    rng = np.random.default_rng(seed); n = rng.poisson(nu, years); N = int(n.sum()); mags = rng.exponential(beta, N)
    x10 = beta * math.log(nu) - beta * math.log(-math.log(0.9)); exc = mags > x10
    yr = np.repeat(np.arange(years), n); ann_exc = np.zeros(years, bool); ann_exc[yr[exc]] = True
    r_clock = exc.sum() / years; r_nat = exc.sum() / N * nu
    cb = np.bincount(yr[exc] // block, minlength=years // block)[: years // block]
    kb = int(round(block * nu)); nb = N // kb; nbk = exc[: nb * kb].reshape(nb, kb).sum(axis=1)
    return dict(N=N, x10=x10, r_clock=float(r_clock), r_nat=float(r_nat), D_clock=float(cb.var(ddof=1) / cb.mean()),
                D_nat=float(nbk.var(ddof=1) / nbk.mean()), ann=float(ann_exc.mean()), p=-math.log(0.9) / nu, nblk=(len(cb), nb))


def r5():
    pid = "P12-5"; d = D[pid]
    nu = 3.0; F = _floods(nu, 1_000_000, 12); lam = -math.log(0.9)
    Dnat_exact = 1.0 - F["p"]; poisson_ok = abs(Dnat_exact - 1.0) <= TOL_N; rate_ok = rel(F["r_nat"], lam) <= TOL_N
    crr, null, dom = F["r_nat"], F["r_clock"], lam; check = poisson_ok and rate_ok
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    sens = [(v, 1.0 - lam / v) for v in (1.65, 5.0)]; nu_min = lam / TOL_N
    se = math.sqrt(2.0 / (F["nblk"][1] - 1))
    return make_row(d[2], d[3] + f"; model: flood events Poisson with nu = {nu:g} per year and exponential peaks above a base level (so annual maxima are Gumbel), {1_000_000:,} years, seed 12; x10 = the Gumbel 0.9 quantile; natural time = event count, one natural-time year = nu events",
                    source=_src(pid), Q=d[5] + " (computed as: the exceedance rate per natural-time year against per clock year, and the index of dispersion of exceedance counts in blocks of 10 natural-time years (Poisson: 1), exact and simulated; both within 1 %)",
                    ingredient=d[4] + " (natural time: time counted in the system's own events, normalised to one year per nu events)",
                    null=d[6], domain=d[7],
                    numbers=f"{F['N']:,} flood events; x10 = {F['x10']:.4f} (peak scale 1); fraction of years whose maximum exceeds x10 {F['ann']:.5f} (Gumbel: 0.1); exceedance rate per natural-time year {F['r_nat']:.5f}, per clock year {F['r_clock']:.5f}, return-period theory -ln(0.9) = {lam:.5f}; dispersion index: natural time exact 1 - p = {Dnat_exact:.5f} (p = {F['p']:.5f} per event), simulated {F['D_nat']:.4f} (+- {se:.4f}, {F['nblk'][1]} blocks); clock time exact 1, simulated {F['D_clock']:.4f} ({F['nblk'][0]} blocks); other event rates (exact natural-time dispersion): " + "; ".join(f"nu {v}: {dd:.4f}" for v, dd in sens) + f"; natural-time counts are within 1 % of Poisson only for nu >= {nu_min:.2f} events per year",
                    tg=f"natural-time rate {crr:.5f} vs clock rate {null:.5f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"return-period theory gives {dom:.5f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has the rate)', 'differ')}",
                    tc=f"same rate within 1 % ({_w(rate_ok, 'yes', 'no')}) and natural-time counts Poisson within 1 % (exact dispersion {Dnat_exact:.5f}: {_w(poisson_ok, 'yes', 'no')}): {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"counted in floods, the exceedance rate {_w(rel(crr, null) <= TOL_G, 'is', 'is not')} the clock rate ({crr:.5f} against {null:.5f}), because a stationary Poisson stream of events turns natural time into a relabelled clock; but in natural time an exceedance is a coin toss per flood, a Bernoulli process, so counts are binomial with dispersion 1 - p = {Dnat_exact:.5f}, {_w(poisson_ok, 'within', 'more than')} 1 % from Poisson at {nu:g} floods per year; the Poisson law of return-period theory is a clock-time law",
                    weakness="DEVIATION: declared.py speaks of annual maxima; a series of annual maxima alone makes natural time identical to clock time (one event per year), so the flood events behind the maxima (a peaks-over-threshold stream, nu = 3 per year, a typical POT rate) are simulated and counted; the verdict depends on nu (Poisson within 1 % above the printed nu), and the natural-time unit (nu events per year) is a normalisation needed to compare rates",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P12: climate and earth (Predictions70/DECLARATION.md; declared.py at 8397478)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
