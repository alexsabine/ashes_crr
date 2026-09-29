"""PRED70 batch P01: oscillators with events of their own (H-L5 class claim; H-CUT antipode against extremum).
Rows P01-1..P01-5 of Predictions70/declared.py (declared at 8397478, pushed before any model existed; prompt-log entry 234).
[1] Hodgkin-Huxley neuron with current noise; [2] Morris-Lecar type I near the SNIC with noise; [3] Stuart-Landau with
frequency noise (phase diffusion); [4] the Oregonator (Tyson's two-variable reduction) in the relaxation regime, H-CUT;
[5] the Lorenz system, lobe switches as own events. Q, null and H0 are printed verbatim from declared.py; the harness
labels are computed from the numbers (R15). Deterministic: fixed seeds, fixed grids (Euler-Maruyama for the SDEs, explicit
RK4 for Lorenz, fixed-grid RK45 for the Oregonator); no data files, no network."""
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks, lfilter

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P  # noqa: E402

DECL = {p[0]: p for p in P}
N_BOOT, SEED = 2000, 0            # the declaration's fixed H-L5 knobs (paired bootstrap of the instrument)


def _w(cond, yes, no):
    return yes if cond else no


def _src(pid):
    return f"PRED70 {pid} (declared at 8397478; forecast {DECL[pid][8]})"


def _hl5(r):
    """Q's H-L5 criterion as declared: CV(arc) < CV(clock) with the paired-bootstrap 95 % CI of the difference below 0.
    A difference below 1e-9 (relative) is not resolvable and never counts (R5)."""
    return bool(r["cv_arc"] < r["cv_clock"] and r["ci95"][1] < 0.0 and rel(r["cv_arc"], r["cv_clock"]) > 1e-9)


def _cls(r):
    lo, hi = r["ci95"]
    if lo <= 0.0 <= hi:
        return "CI includes 0"
    return _w(r["cv_arc"] < r["cv_clock"], "arc-regular (CI below 0)", "clock-regular (CI above 0)")


def _rtxt(r):
    return (f"{r['n']} occasions: CV(arc) = {r['cv_arc']:.4f}, CV(clock) = {r['cv_clock']:.4f}, CV(amplitude) = {r['cv_amp']:.4f}, "
            f"C_mean = {r['C_mean']:.3f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) = [{r['ci95'][0]:.4f}, {r['ci95'][1]:.4f}] ({_cls(r)}), "
            f"of CV(arc) - CV(amplitude) = [{r['ci95_amp'][0]:.4f}, {r['ci95_amp'][1]:.4f}]")


def _beyond_amp(r):
    """H-L5 as CRR.md states it also needs control (i): the arc must beat the excursion amplitude (CI of CV(arc) - CV(amp) below 0)."""
    return _w(r["ci95_amp"][1] < 0.0, "the arc beats control (i), the amplitude",
              _w(r["ci95_amp"][0] > 0.0, "control (i), the amplitude, is the more regular quantity", "the arc ties control (i), the amplitude"))


# ---------------------------------------------------------------- [1] Hodgkin-Huxley with current noise
def _hh(I0=10.0, sig=1.0, dt=0.01, n_spk=202, seed=1, per_step=False, n_max=600000):
    """Euler-Maruyama on the HH equations (standard squid parameters, V in mV, t in ms). Noise reading: intensity sig
    (dV gets sig sqrt(dt)/C N(0,1) per step) or, per_step=True, an i.i.d. current of sd sig held over each step (sig dt/C N)."""
    rng = np.random.default_rng(seed); xi = rng.standard_normal(n_max)
    gNa, gK, gL, ENa, EK, EL, C = 120.0, 36.0, 0.3, 50.0, -77.0, -54.387, 1.0
    amp = (sig * dt if per_step else sig * math.sqrt(dt)) / C
    V, m, h, n = -65.0, 0.0529, 0.5961, 0.3177
    out = np.empty(n_max); up = []; ex = math.exp
    for k in range(n_max):
        am = 0.1 * (V + 40.0) / (1.0 - ex(-(V + 40.0) / 10.0)) if abs(V + 40.0) > 1e-7 else 1.0
        bm = 4.0 * ex(-(V + 65.0) / 18.0); ah = 0.07 * ex(-(V + 65.0) / 20.0); bh = 1.0 / (1.0 + ex(-(V + 35.0) / 10.0))
        an = 0.01 * (V + 55.0) / (1.0 - ex(-(V + 55.0) / 10.0)) if abs(V + 55.0) > 1e-7 else 0.1
        bn = 0.125 * ex(-(V + 65.0) / 80.0)
        Iion = gNa * m ** 3 * h * (V - ENa) + gK * n ** 4 * (V - EK) + gL * (V - EL)
        Vn = V + dt * (I0 - Iion) / C + amp * xi[k]
        m += dt * (am * (1.0 - m) - bm * m); h += dt * (ah * (1.0 - h) - bh * h); n += dt * (an * (1.0 - n) - bn * n)
        out[k] = Vn
        if V < 0.0 <= Vn:
            up.append(k)
        V = Vn
        if len(up) >= n_spk:
            return out[:k + 1], np.asarray(up)
    raise RuntimeError("HH: too few spikes in n_max steps")


def r1():
    pid = "P01-1"; d = DECL[pid]; dt = 0.01
    V, up = _hh(); ev = up[2:]                                           # 200 spikes after the first two (transient)
    res = {}
    for sub in (1, 5, 10):                                               # sampling: the integration grid, 0.05 ms, 0.1 ms
        res[sub] = regularity(V[::sub], np.unique(ev // sub), sigma=1.0, dt=dt * sub, n_boot=N_BOOT, seed=SEED)
    Vp, upp = _hh(per_step=True); rp = regularity(Vp, upp[2:], sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED)
    r = res[1]
    crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=None, check=check)
    sens = "; ".join(f"sampled every {dt * s:g} ms: CV(arc) {res[s]['cv_arc']:.4f}, CV(clock) {res[s]['cv_clock']:.4f}, CI [{res[s]['ci95'][0]:.4f}, {res[s]['ci95'][1]:.4f}] ({_cls(res[s])})" for s in (5, 10))
    flips = [s for s in (5, 10) if _hl5(res[s]) != check] + ([] if _hl5(rp) == check else ["per-step"])
    return make_row(d[2], d[3] + f" (computed as: standard squid HH, I0 = 10 uA/cm2 plus white current noise of intensity 1 uA/cm2 ms^1/2, Euler-Maruyama at dt = {dt:g} ms, seed 1; spikes = upward crossings of 0 mV, 200 spikes after the first two; arc = identity-metric arc of V in mV)",
                    source=_src(pid), Q=d[5], ingredient=d[4] + " (regularity() of the instrument, inclusive segments: a continuous ODE has no reset jump at the spike)",
                    null=d[6], domain=d[7] + " (gives no value for CV(arc): passed as none to T-N)",
                    numbers=f"{_rtxt(r)}; sensitivities: {sens}; noise read as an i.i.d. current of sd 1 per {dt:g}-ms step (intensity 0.1): {_rtxt(rp)}",
                    tg=f"CV(arc) {crr:.4f} vs null CV(ISI) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="the renewal statement fixes the ISI's statistics, not the arc's; no value for CV(arc) is cited (none)",
                    tc=f"CV(arc) < CV(ISI) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"the arc between spikes averages {r['C_mean']:.1f} mV; the excursion amplitude is {_w(r['cv_amp'] < r['cv_arc'], 'more', 'less')} regular than the arc "
                             f"(CV(amplitude) {r['cv_amp']:.4f}) and the arc is {_w(crr < null, 'more', 'less')} regular than the interval (CV(ISI) {null:.4f}): the neuron is {_cls(r)} on the integration grid; "
                             f"H-L5 beyond its first control reads: {_beyond_amp(r)}, so {_w(r['ci95_amp'][0] > 0.0, 'the spike height is more regular still: the stereotyped spike that neurophysiology already names', 'the spike height is not the more regular quantity')}; "
                             f"the verdict {_w(flips, 'changes', 'does not change')} across the sampling and noise-reading sensitivities{_w(flips, ' (' + ', '.join(str(f) for f in flips) + ')', '')}"),
                    weakness=(f"DEVIATION (noise reading): 'white noise sd 1' is read as a current-noise intensity of 1 uA/cm2 ms^1/2; read as an i.i.d. current of sd 1 per step the class is {_cls(rp)} (the verdict {_w(_hl5(rp) == check, 'is the same', 'changes')}); "
                              "the arc of a noisy voltage is not a property of the neuron alone: the white-noise part of the arc grows as the sampling step shrinks (C_mean "
                              f"{res[1]['C_mean']:.1f} mV at 0.01 ms against {res[10]['C_mean']:.1f} mV at 0.1 ms); "
                              "the identity metric on V is a stand-in that A1 does not license; one seed, one current"),
                    elegance="", child="")


# ---------------------------------------------------------------- [2] Morris-Lecar type I near the SNIC
def _ml(I0, sig, dt=0.05, n_spk=202, seed=2, n_max=8000000):
    """Euler-Maruyama on Morris-Lecar with the Rinzel-Ermentrout type-I parameters (C = 20, gCa = 4, gK = 8, gL = 2,
    VCa = 120, VK = -84, VL = -60, V1 = -1.2, V2 = 18, V3 = 12, V4 = 17.4, phi = 1/15); noise intensity sig on the current."""
    rng = np.random.default_rng(seed)
    C, gCa, gK, gL, VCa, VK, VL, V1, V2, V3, V4, phi = 20.0, 4.0, 8.0, 2.0, 120.0, -84.0, -60.0, -1.2, 18.0, 12.0, 17.4, 1.0 / 15.0
    V, w = -30.0, 0.0; out = []; up = []; amp = sig * math.sqrt(dt) / C; th, ch = math.tanh, math.cosh
    block = 200000; k = 0
    while k < n_max:
        xi = rng.standard_normal(block)
        for j in range(block):
            minf = 0.5 * (1.0 + th((V - V1) / V2)); winf = 0.5 * (1.0 + th((V - V3) / V4)); tau = 1.0 / ch((V - V3) / (2.0 * V4))
            Vn = V + dt * (I0 - gCa * minf * (V - VCa) - gK * w * (V - VK) - gL * (V - VL)) / C + amp * xi[j]
            w += dt * phi * (winf - w) / tau
            out.append(Vn)
            if V < 0.0 <= Vn:
                up.append(k)
            V = Vn; k += 1
            if len(up) >= n_spk:
                return np.asarray(out), np.asarray(up)
    raise RuntimeError("ML: too few spikes")


def _ml_period(I0, dt=0.05):
    V, up = _ml(I0, 0.0, dt=dt, n_spk=4, n_max=400000)
    return float(np.diff(up)[-1] * dt)


def r2():
    pid = "P01-2"; d = DECL[pid]; dt = 0.05; I0, sig = 40.0, 1.0
    per = {I: _ml_period(I) for I in (40.0, 40.5)}
    V, up = _ml(I0, sig); ev = up[2:]
    res = {s: regularity(V[::s], np.unique(ev // s), sigma=1.0, dt=dt * s, n_boot=N_BOOT, seed=SEED) for s in (1, 4, 20)}
    V3, up3 = _ml(I0, 3.0); r3 = regularity(V3, up3[2:], sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED)
    r = res[1]; crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=None, check=check)
    flips = [s for s in (4, 20) if _hl5(res[s]) != check] + ([] if _hl5(r3) == check else ["noise 3"])
    sens = "; ".join(f"sampled every {dt * s:g} ms: CV(arc) {res[s]['cv_arc']:.4f}, CV(clock) {res[s]['cv_clock']:.4f}, CI [{res[s]['ci95'][0]:.4f}, {res[s]['ci95'][1]:.4f}] ({_cls(res[s])})" for s in (4, 20))
    return make_row(d[2], d[3] + f" (computed as: Rinzel-Ermentrout type-I parameters, SNIC between I = 39.5 and 40 uA/cm2; I0 = {I0:g} (noise-free period {per[40.0]:.1f} ms; {per[40.5]:.1f} ms at I = 40.5), current-noise intensity {sig:g} uA/cm2 ms^1/2, Euler-Maruyama at dt = {dt:g} ms, seed 2; spikes = upward crossings of 0 mV, 200 after the first two)",
                    source=_src(pid), Q=d[5] + " (computed as: CV(arc of V between spikes) < CV(ISI), paired-bootstrap CI of the difference below 0)",
                    ingredient=d[4] + " (regularity(), inclusive segments)", null=d[6], domain=d[7] + " (gives no value for CV(arc): passed as none to T-N)",
                    numbers=f"{_rtxt(r)}; sensitivities: {sens}; noise intensity 3: {_rtxt(r3)}",
                    tg=f"CV(arc) {crr:.4f} vs null CV(ISI) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="the type-I statement locates the ISI's variance in the slow passage near the ghost; it gives no value for CV(arc) (none)",
                    tc=f"CV(arc) < CV(ISI) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"near the SNIC the interval is set by the slow passage past the ghost (CV(ISI) {null:.4f}); the arc between spikes (C_mean {r['C_mean']:.1f} mV) is "
                             f"{_w(crr < null, 'the more', 'the less')} regular quantity (CV(arc) {crr:.4f}): {_cls(r)}; H-L5 beyond its first control reads: {_beyond_amp(r)} "
                             f"(CV(amplitude) {r['cv_amp']:.4f}); the verdict {_w(flips, 'changes', 'does not change')} across the sensitivities"
                             f"{_w(flips, ' (' + ', '.join(str(f) for f in flips) + ')', '')}"),
                    weakness=("the noise part of the arc depends on the sampling step (C_mean "
                              f"{res[1]['C_mean']:.1f} mV at {dt:g} ms against {res[20]['C_mean']:.1f} mV at {20 * dt:g} ms); I0 and the noise intensity are this row's choices "
                              "(declared.py names neither); identity metric on V; one seed"),
                    elegance="Near the tipping point a neuron waits a long and variable time before it fires, but each spike is the same size. Most of the unevenness lives in the wait, so counting the distance the voltage travels is steadier than counting the time, and the steadiest thing of all is the height of the spike.",
                    child="Think of a sleepy frog that sometimes waits a little and sometimes a lot before it jumps, but every jump is the same height. If you measure the frog by how far it moved, its turns look more alike than if you measure by the clock. The most alike thing of all is the height of each jump.")


# ---------------------------------------------------------------- [3] Stuart-Landau with frequency noise
def _sl(D=0.05, omega=1.0, n_cyc=2000, per_period=100, seed=3, tau_c=None):
    """Frequency noise leaves |z| = 1 on the Stuart-Landau attractor (the noise rotates z), so the phase carries the
    dynamics exactly: white reading dtheta = omega dt + sqrt(D) dW (var theta(t) = D t, the convention of H0's formula);
    coloured reading (tau_c): omega + eta, eta an OU process of variance D/(2 tau_c), same long-time diffusion D."""
    T0 = 2 * math.pi / omega; dt = T0 / per_period; n = int(n_cyc * per_period * 1.1)
    rng = np.random.default_rng(seed); g = rng.standard_normal(n)
    if tau_c is None:
        inc = omega * dt + math.sqrt(D * dt) * g
    else:
        a = math.exp(-dt / tau_c); s = math.sqrt(D / (2 * tau_c))
        eta = lfilter([s * math.sqrt(1 - a * a)], [1, -a], g); inc = (omega + eta) * dt
    th = np.concatenate([[0.0], np.cumsum(inc)])
    ev = np.searchsorted(np.maximum.accumulate(th), 2 * math.pi * np.arange(1, int(th.max() / (2 * math.pi)) + 1))
    ev = ev[ev < len(th)][: n_cyc + 1]
    z = np.column_stack([np.cos(th), np.sin(th)])
    return z, th, ev, dt, T0


def r3():
    pid = "P01-3"; d = DECL[pid]; D = 0.05
    res = {}
    for key, kw in (("white/100", dict(per_period=100)), ("white/1000", dict(per_period=1000, n_cyc=1000)), ("white/20", dict(per_period=20)),
                    ("OU tau 0.1 T0", dict(per_period=100, tau_c=0.2 * math.pi))):
        z, th, ev, dt, T0 = _sl(D=D, **kw)
        r = regularity(z, ev, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED)
        dom = cv(np.diff(th[ev]))                                         # H0's arc per cycle: r x net phase advance between the same event samples (r = 1)
        res[key] = (r, dom, dt, T0)
    r, dom, dt, T0 = res["white/100"]
    cv_theory = math.sqrt(D * T0) / T0
    crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    ro, do_ = res["OU tau 0.1 T0"][0], res["OU tau 0.1 T0"][1]
    out_ou = outcome(crr=ro["cv_arc"], null=ro["cv_clock"], domain=do_, check=_hl5(ro))
    sens = "; ".join(f"{k}: CV(arc) {v[0]['cv_arc']:.4f}, CV(period) {v[0]['cv_clock']:.4f}, H0's CV(r x net advance) {v[1]:.4f}, C_mean {v[0]['C_mean']:.3f}, CI [{v[0]['ci95'][0]:.4f}, {v[0]['ci95'][1]:.4f}] ({_cls(v[0])}), T-N {_w(rel(v[0]['cv_arc'], v[1]) <= TOL_N, 'agree', 'differ')}"
                     for k, v in res.items() if k != "white/100")
    return make_row(d[2], d[3] + f" (computed as: dz = (1 + i omega) z - |z|^2 z with multiplicative frequency noise, omega = 1, |z| = 1 on the attractor, so theta carries it exactly; white frequency noise with var theta(t) = D t, D = {D:g} (the convention of H0's formula), 2000 cycles sampled {100} times per mean period (dt = {dt:.5f}), seed 3; cycle = first passage of theta through the next multiple of 2 pi; arc = identity-metric arc of (Re z, Im z))",
                    source=_src(pid), Q=d[5] + " (computed as: CV(arc per cycle) < CV(period), paired-bootstrap CI of the difference below 0)",
                    ingredient=d[4] + " (regularity() on the two-dimensional carrier z, inclusive segments)", null=d[6],
                    domain=d[7] + " (computed as: H0's arc per cycle, r x the net phase advance between the same event samples, and its CV)",
                    numbers=f"{_rtxt(r)}; H0's period CV sqrt(D T)/T = {cv_theory:.4f} (observed CV(period) {null:.4f}); H0's arc (r x net advance): CV {dom:.4f}; sensitivities: {sens}",
                    tg=f"CV(arc) {crr:.4f} vs null CV(period) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"H0's arc per cycle (r x net phase advance) gives CV {dom:.4f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"CV(arc) < CV(period) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"the period's CV is {null:.4f} against H0's sqrt(D T)/T = {cv_theory:.4f} (relative difference {rel(null, cv_theory):.3f}); the sampled arc per cycle is 2 pi r plus twice the phase's "
                             f"backtracking (C_mean {r['C_mean']:.3f} against 2 pi = {2 * math.pi:.3f}), and its CV ({crr:.4f}) is {_w(rel(crr, dom) <= TOL_N, 'the same as', 'not the same as')} H0's net-advance value ({dom:.4f}); "
                             f"with smooth (OU) frequency noise the arc's CV is {res['OU tau 0.1 T0'][0]['cv_arc']:.4f} against H0's {res['OU tau 0.1 T0'][1]:.4f}; the class reading is {_cls(r)} on the declared grid"),
                    weakness=("the noise is read as white (the reading under which H0's period formula is exact) and the sampling "
                              "step is this row's choice; the arc of a white-noise phase has no continuum limit (it diverges as the step shrinks), so the arc's value and the T-N "
                              f"comparison depend on the sampling (printed at three steps and with an OU reading; the class verdict is {_w(all(_hl5(v[0]) == check for v in res.values()), 'the same', 'not the same')} in all four); the relative T-N tolerance is not meaningful for a CV near 0; "
                              f"the same harness rule on the OU (smooth frequency noise) reading gives {out_ou}"),
                    elegance="", child="")


# ---------------------------------------------------------------- [4] Oregonator, H-CUT
def _oregonator(eps=0.04, q=0.002, f=1.0, T=130.0, dt=0.001, t_drop=20.0):
    def rhs(t, y):
        x, z = y
        return [(x - x * x - f * z * (x - q) / (x + q)) / eps, x - z]
    t = np.arange(0.0, T, dt)
    s = solve_ivp(rhs, (0.0, T), [0.1, 0.1], method="RK45", t_eval=t, rtol=1e-9, atol=1e-12)
    keep = s.t >= t_drop
    return s.y[0][keep], dt


def _hcut_fraction(ph, start, own, ext, margin):
    cuts = antipodal_cuts(ph, start=start)
    e = own[(own > start + margin) & (own < cuts[-1] - margin)]
    da = np.array([np.min(np.abs(cuts - k)) for k in e]); de = np.array([np.min(np.abs(ext - k)) for k in e])
    return float(np.mean(da < de)), da, de, len(e)


def r4():
    pid = "P01-4"; d = DECL[pid]
    x, dt = _oregonator()
    ph = intrinsic_phase(x)
    mx, _ = find_peaks(x, prominence=0.3 * np.ptp(x)); period = float(np.mean(np.diff(mx))) * dt
    P = int(round(period / dt)); half = P / 2.0
    ext = peak_cuts(x, prominence=0.3 * np.ptp(x), distance=max(int(0.4 * P), 2))    # the gate's extremum settings
    dx = np.gradient(x, dt)
    own, _ = find_peaks(dx, prominence=0.3 * np.ptp(dx), distance=max(int(0.4 * P), 2))   # the fast rise: steepest ascent of x per cycle
    wrapped_zero = np.where((np.floor(ph[1:] / (2 * math.pi)) > np.floor(ph[:-1] / (2 * math.pi))))[0] + 1
    readings = {"(i) gate convention, start at the second detected extremum": int(ext[1]),
                "(ii) instrument default, start at the first sample": 0,
                "(iii) the analytic phase's own zero, start where theta crosses a multiple of 2 pi": int(wrapped_zero[0])}
    rd = {}
    for k, s in readings.items():
        fr, da, de, n = _hcut_fraction(ph, s, own, ext, P)
        rd[k] = (fr, float(np.median(da)) / half, float(np.median(de)) / half, n, fr >= 2.0 / 3.0)
    scan_starts = [int(mx[0] + j * P / 48.0) for j in range(48)]
    scan = [_hcut_fraction(ph, s, own, ext, P)[0] >= 2.0 / 3.0 for s in scan_starts]
    verdicts = {v[4] for v in rd.values()}
    internal = len(verdicts) > 1
    k0 = list(rd)[0]; fr0, dA, dE, n0, ok0 = rd[k0]
    out = outcome(crr=dA, null=dE, domain=None, check=ok0, internal=internal)
    rtxt = "; ".join(f"{k}: own event nearer the antipodal cut on {v[0]:.3f} of {v[3]} cycles, median distance to the cut {v[1]:.4f} half-turns, to the extremum {v[2]:.4f} half-turns (at least 2/3: {_w(v[4], 'yes', 'no')})" for k, v in rd.items())
    return make_row(d[2], d[3] + f" (computed as: Tyson's two-variable reduction eps dx/dt = x - x^2 - f z (x - q)/(x + q), dz/dt = x - z, q = 0.002, f = 1, fixed-grid RK45 at dt = {dt:g}, rtol 1e-9, first 20 time units dropped; period {period:.4f})",
                    source=_src(pid), Q=d[5] + " (computed as: per cycle, the own event = the steepest rise of x; distance to the nearest antipodal_cuts() cut on intrinsic_phase(x) against distance to the nearest peak_cuts() extremum with the gate's settings; Q holds if the cut is strictly nearer on at least 2/3 of cycles)",
                    ingredient=d[4] + " (antipodal_cuts on intrinsic_phase; A3 does not fix where the cut sequence starts, so three readings of the start are computed)",
                    null=d[6], domain=d[7],
                    numbers=f"{rtxt}; anchor scan (48 starts evenly over one period from the first maximum): Q's criterion met for {sum(scan)} of 48 starts",
                    tg=f"reading (i): median distance to the cut {dA:.4f} vs to the extremum {dE:.4f} half-turns: {_w(rel(dA, dE) <= TOL_G, 'agree', 'differ')}",
                    tn="no domain theorem cited",
                    tc=(f"the three readings of A3's start give {_w(internal, 'different verdicts', 'the same verdict')} (" + ", ".join(_w(v[4], 'holds', 'fails') for v in rd.values()) + ")"
                        + _w(internal, " -> not computable", f": {_w(ok0, 'holds', 'fails')} -> {_w(ok0, 'Q holds', 'Q fails')}")),
                    out=out,
                    reading=(f"the Oregonator is exactly periodic, so every cycle gives the same answer and the only free choice is where the half-turn sequence begins; "
                             f"the fast rise sits {float(np.median([np.min(np.abs(mx - k)) for k in own])) * dt:.4f} time units from the nearest maximum, and whether a half-turn cut lands nearer to it "
                             f"than the extremum does is decided by that start ({sum(scan)} of 48 starts satisfy Q): "
                             + _w(internal, "the readings disagree, so A3 as written does not fix Q's value here", "the readings agree")),
                    weakness=("deterministic model (declared.py names no noise); q and f are this row's choices (Tyson's standard values); the own event is read as the steepest rise; "
                              "the analytic-signal phase of a pulse train advances unevenly, which is why the start matters; distances are in half-turns of the mean period"),
                    elegance="", child="")


# ---------------------------------------------------------------- [5] Lorenz lobe switches
def _lorenz(dt=0.005, T=2000.0, t_drop=50.0, s=10.0, r=28.0, b=8.0 / 3.0):
    n = int(round(T / dt)); x, y, z = 1.0, 1.0, 1.0; X = np.empty(n)
    for k in range(n):
        k1x, k1y, k1z = s * (y - x), x * (r - z) - y, x * y - b * z
        x2, y2, z2 = x + 0.5 * dt * k1x, y + 0.5 * dt * k1y, z + 0.5 * dt * k1z
        k2x, k2y, k2z = s * (y2 - x2), x2 * (r - z2) - y2, x2 * y2 - b * z2
        x3, y3, z3 = x + 0.5 * dt * k2x, y + 0.5 * dt * k2y, z + 0.5 * dt * k2z
        k3x, k3y, k3z = s * (y3 - x3), x3 * (r - z3) - y3, x3 * y3 - b * z3
        x4, y4, z4 = x + dt * k3x, y + dt * k3y, z + dt * k3z
        k4x, k4y, k4z = s * (y4 - x4), x4 * (r - z4) - y4, x4 * y4 - b * z4
        x += dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6; y += dt * (k1y + 2 * k2y + 2 * k3y + k4y) / 6; z += dt * (k1z + 2 * k2z + 2 * k3z + k4z) / 6
        X[k] = x
    return X[int(round(t_drop / dt)):], dt


def r5():
    pid = "P01-5"; d = DECL[pid]
    x, dt = _lorenz()
    ev = np.where(np.sign(x[1:]) != np.sign(x[:-1]))[0] + 1
    r = regularity(x, ev, sigma=1.0, dt=dt, n_boot=N_BOOT, seed=SEED)
    xs, dts = x[::4], dt * 4; evs = np.where(np.sign(xs[1:]) != np.sign(xs[:-1]))[0] + 1
    rs = regularity(xs, evs, sigma=1.0, dt=dts, n_boot=N_BOOT, seed=SEED)
    C = np.array([arc_length(x[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])]); T = np.diff(ev) * dt
    corr = float(np.corrcoef(C, T)[0, 1]); slope, icpt = np.polyfit(T, C, 1)
    crr, null = r["cv_arc"], r["cv_clock"]; check = _hl5(r)
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row(d[2], d[3] + f" (computed as: explicit RK4 at dt = {dt:g} from (1, 1, 1) over t = 2000, first 50 dropped; own events = sign changes of x; arc = identity-metric arc of x)",
                    source=_src(pid), Q=d[5] + " (computed as: CV(arc) < CV(time between switches), paired-bootstrap CI of the difference below 0)",
                    ingredient=d[4] + " (regularity(), inclusive segments)", null=d[6], domain=d[7] + " (no value for CV(arc): none)",
                    numbers=f"{_rtxt(r)}; per residence arc against time: corr {corr:.4f}, arc = {slope:.3f} x time + {icpt:.3f}; sampled every {dts:g}: CV(arc) {rs['cv_arc']:.4f}, CV(clock) {rs['cv_clock']:.4f}, CI [{rs['ci95'][0]:.4f}, {rs['ci95'][1]:.4f}] ({_cls(rs)})",
                    tg=f"CV(arc) {crr:.4f} vs null CV(time) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no domain theorem cited for the arc",
                    tc=f"CV(arc) < CV(time between switches) with the paired-bootstrap CI below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=(f"a residence on one lobe is a number of loops; its arc tracks the time spent (corr {corr:.4f}) with an intercept of {icpt:.3f} "
                             f"({_w(icpt > 0, 'a fixed excursion per residence, which lowers the arc CV below the clock CV by arithmetic, the mechanism the regularity docstring names for reset jumps', 'no fixed excursion')}); "
                             f"the arc's CV ({crr:.4f}) is {_w(crr < null, 'below', 'above')} the clock's ({null:.4f}): {_cls(r)}; H-L5 beyond its first control reads: {_beyond_amp(r)} "
                             f"(CV(amplitude) {r['cv_amp']:.4f})"),
                    weakness="one trajectory; the identity metric on x alone is declared",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P01: oscillators with events of their own (declared at 8397478; prompt-log entry 234)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
