"""PRED70 batch P07: chemistry and cell biology (Predictions70/DECLARATION.md; prompt-log entry 234). Five declared rows,
read from Predictions70/declared.py (pushed at 8397478 before any model existed); Q, null and H0 are printed verbatim.
[1] P07-1 Michaelis-Menten progress curves in the reaction's own unit (A1');
[2] P07-2 the Gardner toggle switch with noise, arc against residence time (H-L5);
[3] P07-3 the Elowitz-Leibler repressilator with noise, promoter switches against the antipodal cut (H-CUT);
[4] P07-4 the Goodwin circadian oscillator, the light PRC's advance-to-delay crossover against the antipode of noon (A3);
[5] P07-5 the Goldbeter-Dupont-Berridge calcium oscillator under IP3 noise, arc against ISI (H-L5).
Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data file is
opened, no network. Deterministic: fixed seeds, fixed grids, explicit RK4 (Euler-Maruyama for the noisy rows) on a fixed
dt. Literature named by name and year only (R10): Michaelis and Menten 1913; Schnell and Mendoza 1997 (Lambert W);
Gardner, Cantor and Collins 2000; Kramers 1940; Elowitz and Leibler 2000; Gillespie 2000 (chemical Langevin equation);
Goodwin 1965; Gonze et al. 2005; Goldbeter, Dupont and Berridge 1990; Skupin et al. 2008. Run:
  uv run python Predictions70/batches/pred_07.py
"""
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.signal import find_peaks
from scipy.special import lambertw

from crr.instrument.core import antipodal_cuts, arc_length, intrinsic_phase, peak_cuts, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P  # noqa: E402

DECL = {p[0]: p for p in P}
N_BOOT, SEED_BOOT = 2000, 0                                                   # H-L5 margins (DECLARATION: n_boot 2000, seed 0)


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


# ---------------------------------------------------------------- [1] P07-1 Michaelis-Menten in Km units
S0_KM = (0.1, 0.3, 1.0, 3.0, 10.0)                                            # S0/Km, the declared axis
KM = (1.0, 2.0, 0.5, 4.0, 0.25)                                               # a different enzyme per curve (mM)
VMAX = (1.0, 0.5, 2.0, 1.5, 0.8)                                              # mM/min


def _mm_rk4(S0, Km, Vm, n_per=2000, s_end=1e-4):
    dt = (Km + S0) / Vm / n_per
    f = lambda S: -Vm * S / (Km + S)
    t, S, s = [0.0], [S0], S0
    while s > s_end * S0:
        k1 = f(s); k2 = f(s + 0.5 * dt * k1); k3 = f(s + 0.5 * dt * k2); k4 = f(s + dt * k3)
        s = s + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; S.append(s); t.append(t[-1] + dt)
    return np.array(t), np.array(S)


def _collapse_shift(curves, ngrid=200, frac=0.05):
    """Collapse index 1 - max over ordered pairs of the RMS gap between curve j and curve i shifted in time so that i passes
    through j's start; the gap is taken over j's decay to frac of its start and normalised by j's start."""
    worst = 0.0
    for ti, yi in curves:
        for tj, yj in curves:
            if yi[0] <= yj[0]:
                continue
            tstar = np.interp(yj[0], yi[::-1], ti[::-1]); U = np.interp(frac * yj[0], yj[::-1], tj[::-1])
            u = np.linspace(0.0, U, ngrid)
            worst = max(worst, float(np.sqrt(np.mean((np.interp(tstar + u, ti, yi) - np.interp(u, tj, yj)) ** 2)) / yj[0]))
    return 1.0 - worst


def _collapse_norm(curves, span=4.0, ngrid=400):
    """Collapse index for S/S0 against t/t_half (each curve's own clock unit), no shift needed (all start at 1)."""
    g = np.linspace(0.0, span, ngrid); ys = []
    for t, S in curves:
        th = np.interp(0.5 * S[0], S[::-1], t[::-1]); ys.append(np.interp(g * th, t, S / S[0]))
    return 1.0 - max(float(np.sqrt(np.mean((a - b) ** 2))) for a in ys for b in ys)


def r1():
    pid = "P07-1"; d = DECL[pid]
    raw = [_mm_rk4(s0 * k, k, v) for s0, k, v in zip(S0_KM, KM, VMAX)]
    kmu = [(v * t / k, S / k) for (t, S), k, v in zip(raw, KM, VMAX)]
    lw = []
    for s0 in S0_KM:                                                          # H0: s + ln s = s0 + ln s0 - tau (Lambert W)
        tau_end = s0 - 1e-4 * s0 + math.log(1e4); tau = np.linspace(0.0, tau_end, 20001)
        lw.append((tau, lambertw(s0 * np.exp(s0 - tau)).real))
    err = max(float(np.max(np.abs(s - lambertw(s0 * np.exp(s0 - tau)).real))) for (tau, s), s0 in zip(kmu, S0_KM))
    ci_km = _collapse_shift(kmu); ci_raw = _collapse_shift(raw); ci_norm = _collapse_norm(raw); ci_dom = _collapse_shift(lw)
    null = max(ci_raw, ci_norm); thr = 1.0 - TOL_N
    check = ci_km >= thr and ci_raw < thr and ci_norm < thr
    out = outcome(crr=ci_km, null=null, domain=ci_dom, check=check)
    return make_row(d[2], d[3] + f": dS/dt = -Vmax S/(Km + S), five curves S0/Km = {S0_KM} with a different enzyme each (Km = {KM} mM, Vmax = {VMAX} mM/min); RK4, dt = (Km + S0)/(2000 Vmax), to S = 1e-4 S0",
                    source=src(pid),
                    Q=d[5] + " (computed as: collapse index CI = 1 - max over pairs of the normalised RMS gap after a time shift; collapse means CI >= 1 - TOL_N; 'only' means both clock readings stay below it)",
                    ingredient=d[4] + ": substrate in Km, time in Km/Vmax (the reaction's own unit, read from its rate law)",
                    null=d[6] + " (computed as: (a) S in mM against t in min with the same time-shift rule; (b) S/S0 against t/t_half, each curve's own clock; the null value is the better of the two)",
                    domain=d[7] + " (computed as: the Lambert-W curves s = W(s0 exp(s0 - tau)) put through the same collapse index)",
                    numbers=f"CI in Km units {ci_km:.7f}; clock units (a) raw {ci_raw:.4f}, (b) S/S0 against t/t_half {ci_norm:.4f}; Lambert-W curves {ci_dom:.10f}; RK4 against Lambert W, max |s error| in Km units {err:.1e}",
                    tg=f"CI(Km) {ci_km:.6f} vs null (best clock reading) {null:.6f}: {ag(ci_km, null)}",
                    tn=f"CI(Km) {ci_km:.6f} vs Lambert W {ci_dom:.6f}: {ag(ci_km, ci_dom, TOL_N)}",
                    tc=f"collapse in Km units (CI {ci_km:.6f} >= {thr:.2f}): {hf(ci_km >= thr)}; no collapse in clock units (raw {ci_raw:.4f}, S/S0-t/t_half {ci_norm:.4f}, both < {thr:.2f}): {hf(ci_raw < thr and ci_norm < thr)} {qtail(check)}",
                    out=out,
                    reading=f"in Km units every progress curve {_w(ci_km >= thr, 'is', 'is not')} one curve shifted in time, and in clock units they {_w(null < thr, 'are not', 'also are')} (best clock collapse {null:.4f}); the integrated Michaelis-Menten equation already says so: s + ln s = s0 + ln s0 - tau is a single master curve in Km and Km/Vmax units, which is why Km is called the enzyme's own concentration scale",
                    weakness="the collapse needs a time shift (an unknown origin); in raw clock units the same shift rule is used, so the null is not denied the shift; five curves only; A1' here is the rate law's own constant, which the domain names (Km), so the unit is inherited from Michaelis-Menten, not discovered by CRR",
                    elegance="Every enzyme, fast or slow, crowded or starved, draws the same curve once substrate is measured in its own half-saturation amount and time in its own turnover time.",
                    child="Different enzymes eat sugar at different speeds. If each one is timed with its own clock and measured with its own ruler, all their eating stories look exactly the same.")


# ---------------------------------------------------------------- [2] P07-2 toggle switch, arc against residence
TOG_A, TOG_N, TOG_SIG, TOG_T, TOG_DT = 4.0, 2.0, 0.6, 3.0e4, 0.01


def _toggle(seed=0, rec=2):
    f = lambda u: TOG_A / (1 + (TOG_A / (1 + u ** TOG_N)) ** TOG_N) - u
    roots = [brentq(f, a, b) for a, b in ((0.0, 0.5), (0.5, 2.0), (2.0, TOG_A + 1.0))]
    rng = np.random.default_rng(seed); ns = int(round(TOG_T / TOG_DT))
    nz = rng.standard_normal((ns, 2)) * TOG_SIG * math.sqrt(TOG_DT)
    u, v = roots[2], TOG_A / (1 + roots[2] ** TOG_N); out = np.empty((ns // rec, 2)); k = 0; dt = TOG_DT
    for i in range(ns):
        du = TOG_A / (1 + v * v) - u; dv = TOG_A / (1 + u * u) - v
        u = abs(u + du * dt + nz[i, 0]); v = abs(v + dv * dt + nz[i, 1])
        if (i + 1) % rec == 0:
            out[k, 0] = u; out[k, 1] = v; k += 1
    return roots, out


def _switches(dd, D):
    st = 1 if dd[0] > 0 else -1; ev = []
    for i, x in enumerate(dd):
        if st == 1 and x < -D:
            st = -1; ev.append(i)
        elif st == -1 and x > D:
            st = 1; ev.append(i)
    return np.array(ev)


def r2():
    pid = "P07-2"; d = DECL[pid]
    roots, x2 = _toggle()
    D = 0.5 * (roots[2] - TOG_A / (1 + roots[2] ** TOG_N))                    # half the u - v gap of a stable state
    res = {}
    for f, lab in ((1, 0.02), (5, 0.1), (25, 0.5)):
        x = x2[::f]; ev = _switches(x[:, 0] - x[:, 1], D)
        res[lab] = regularity(x, ev, sigma=1.0, dt=TOG_DT * 2 * f, n_boot=N_BOOT, seed=SEED_BOOT)
    r = res[0.1]; kram = 1.0                                                  # H0: exponential residence, CV = 1
    check = r["ci95"][1] < 0.0
    out = outcome(crr=r["cv_arc"], null=r["cv_clock"], domain=kram, check=check)
    sens = "; ".join(f"record step {lab}: CV(arc) {s['cv_arc']:.4f}, CV(res) {s['cv_clock']:.4f}, diff {s['diff']:+.4f} ({_ci(s['ci95'])})" for lab, s in res.items())
    amp_ok = r["ci95_amp"][1] < 0.0
    x = x2[::5]; ev = _switches(x[:, 0] - x[:, 1], D)                          # the decisive record (0.1): arc against residence
    C = np.array([arc_length(x[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])]); Tr = np.diff(ev) * TOG_DT * 10
    slope, icpt = (float(v) for v in np.polyfit(Tr, C, 1)); rr = float(np.corrcoef(Tr, C)[0, 1])
    gaps = [abs(res[lab]["diff"]) for lab in (0.02, 0.1, 0.5)]; widens = gaps[0] < gaps[1] < gaps[2]
    return make_row(d[2], d[3] + f": du/dt = a/(1 + v^n) - u, dv/dt = a/(1 + u^n) - v, a = {TOG_A}, n = {TOG_N} (stable states u = {roots[2]:.4f}, {roots[0]:.4f}), additive noise sd {TOG_SIG} per unit time, reflecting at 0; Euler-Maruyama dt {TOG_DT} over {TOG_T:.0f} time units, seed 0; a switch is the difference u - v passing +-{D:.4f} (half a stable state's gap) into the other basin",
                    source=src(pid),
                    Q=d[5] + " (computed as: CV(arc of (u, v), identity metric) < CV(residence time) with the paired-bootstrap 95 % CI of the difference below 0; path recorded every 0.1 time unit)",
                    ingredient=d[4] + ": regularity() on the own events (switches), n_boot 2000, seed 0",
                    null=d[6],
                    domain=d[7] + " (computed as: CV = 1 for an exponential residence time)",
                    numbers=f"{r['n']} residences; CV(arc) {r['cv_arc']:.4f}, CV(residence) {r['cv_clock']:.4f}, difference {r['diff']:+.4f}, 95 % CI [{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}]; amplitude control CV(amp) {r['cv_amp']:.4f}, CV(arc) - CV(amp) {r['diff_amp']:+.4f} CI [{r['ci95_amp'][0]:+.4f}, {r['ci95_amp'][1]:+.4f}]; sensitivity to the record step: {sens}",
                    tg=f"CV(arc) {r['cv_arc']:.4f} vs CV(residence) {r['cv_clock']:.4f}: {ag(r['cv_arc'], r['cv_clock'])} (relative gap {rel(r['cv_arc'], r['cv_clock']):.4f})",
                    tn=f"CV(arc) {r['cv_arc']:.4f} vs Kramers {kram:.1f}: {ag(r['cv_arc'], kram, TOL_N)}",
                    tc=f"CV(arc) < CV(residence) with the CI below 0: {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"per occasion the arc is {slope:.4f} x residence {_w(icpt >= 0, '+', '-')} {abs(icpt):.4f} (correlation {rr:.4f}): noise path length that grows with the residence time plus a {_w(icpt > 0, 'positive', 'non-positive')} constant, the deterministic transit; so the arc inherits the residence spread (CV(residence) {r['cv_clock']:.4f}, against Kramers' 1: {ag(r['cv_clock'], kram, TOL_N)}), and the constant lowers CV(arc) by arithmetic by {abs(r['diff']):.4f} in CV, a relative gap {_w(rel(r['cv_arc'], r['cv_clock']) <= TOL_G, 'inside', 'outside')} the 1 % tolerance; the excursion amplitude is {_w(r['cv_amp'] < r['cv_arc'], 'more', 'less')} regular than the arc (CV {r['cv_amp']:.4f} against {r['cv_arc']:.4f}; CRR.md control (i), arc beyond amplitude: {hf(amp_ok)})",
                    weakness=f"the arc of a noisy path depends on the record step (printed: the CV gap {_w(widens, 'widens monotonically', 'does not widen monotonically')} as the step coarsens); additive rather than chemical-Langevin noise; identity metric on concentrations; the arc {_w(r['diff'] < 0, 'beats', 'does not beat')} the clock, and the fitted intercept {icpt:.4f} is the additive transit constant, which the H-L5 gate treats as arithmetic, not class membership",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] P07-3 repressilator, promoter switch against the cut
RP_AL, RP_AL0, RP_BE, RP_N, RP_OM, RP_T, RP_DT, RP_REC = 216.0, 0.216, 1.0, 2.0, 40.0, 2000.0, 0.005, 20


def _repressilator(seed=1):
    rng = np.random.default_rng(seed); ns = int(round(RP_T / RP_DT)); dt = RP_DT
    nz = rng.standard_normal((ns, 6)) * math.sqrt(dt / RP_OM)
    m = np.array([1.0, 5.0, 10.0]); p = np.array([2.0, 5.0, 20.0]); out = np.empty((ns // RP_REC, 6)); k = 0
    for i in range(ns):
        pr = RP_AL / (1 + p[[2, 0, 1]] ** RP_N) + RP_AL0                      # gene i repressed by protein i-1
        m = np.abs(m + (pr - m) * dt + np.sqrt(pr + m) * nz[i, :3])
        p = np.abs(p + RP_BE * (m - p) * dt + np.sqrt(RP_BE * (m + p)) * nz[i, 3:])
        if (i + 1) % RP_REC == 0:
            out[k, :3] = m; out[k, 3:] = p; k += 1
    return out


def _schmitt_K(y, K=1.0, b=1.25):
    """Promoter switch: the repressor crosses the half-occupancy level K (occupancy p^2/(1 + p^2) = 1/2); the first
    crossing counts once the repressor has gone on to K/b or K*b (noise chatter at K is one switch)."""
    st = 1 if y[0] > K else -1; first = None; out = []
    for i in range(1, len(y)):
        if first is None and ((st == 1 and y[i - 1] >= K > y[i]) or (st == -1 and y[i - 1] <= K < y[i])):
            first = i
        if st == 1 and y[i] < K / b and first is not None:
            out.append(first); st = -1; first = None
        elif st == -1 and y[i] > K * b and first is not None:
            out.append(first); st = 1; first = None
    return np.array(out)


def _rp_det_min(beta, T=400.0, dt=0.005):
    """Deterministic repressilator (RK4): the minimum of protein 1 over the second half of the run."""
    m = np.array([1.0, 5.0, 10.0]); p = np.array([2.0, 5.0, 20.0]); lo = float("inf"); n = int(round(T / dt))
    f = lambda m, p: (-m + RP_AL / (1 + p[[2, 0, 1]] ** RP_N) + RP_AL0, -beta * (p - m))
    for i in range(n):
        a = f(m, p); b = f(m + .5 * dt * a[0], p + .5 * dt * a[1]); c = f(m + .5 * dt * b[0], p + .5 * dt * b[1]); e = f(m + dt * c[0], p + dt * c[1])
        m = m + dt * (a[0] + 2 * b[0] + 2 * c[0] + e[0]) / 6; p = p + dt * (a[1] + 2 * b[1] + 2 * c[1] + e[1]) / 6
        if i > n // 2:
            lo = min(lo, float(p[0]))
    return lo


def _nearest(ev, S):
    S = np.asarray(S); j = np.searchsorted(S, ev); o = []
    for e, jj in zip(ev, j):
        o.append(min(abs(e - S[k]) for k in (jj - 1, jj) if 0 <= k < len(S)))
    return np.array(o, float)


def r3():
    pid = "P07-3"; d = DECL[pid]
    x = _repressilator()[int(round(20.0 / (RP_DT * RP_REC))):]; dts = RP_DT * RP_REC
    pk0, _ = find_peaks(x[:, 3], prominence=0.3 * np.ptp(x[:, 3])); per = float(np.mean(np.diff(pk0))) * dts
    dist = int(round(0.25 * per / dts))
    tallies = {"repressor": [0, 0, 0, [], []], "own": [0, 0, 0, [], []]}; n_sw = 0; n_tr = 0; n_ok = 0
    for g in range(3):
        rep = x[:, 3 + (g - 1) % 3]; own = x[:, 3 + g]; sw = _schmitt_K(rep); n_sw += len(sw)
        for name, sig in (("repressor", rep), ("own", own)):
            pk, _ = find_peaks(sig, prominence=0.3 * np.ptp(sig))
            cuts = antipodal_cuts(intrinsic_phase(sig), start=int(pk[0]))       # A3 from the first own event (a protein peak)
            ext = peak_cuts(sig, prominence=0.3 * np.ptp(sig), distance=dist)
            ok = (sw > max(cuts[0], ext[0])) & (sw < min(cuts[-1], ext[-1]))
            dc = _nearest(sw[ok], cuts) * dts; de = _nearest(sw[ok], ext) * dts
            t = tallies[name]; t[0] += int(np.sum(dc < de)); t[1] += int(np.sum(de < dc)); t[2] += int(np.sum(dc == de)); t[3] += list(dc); t[4] += list(de)
            if name == "repressor":
                pp, _ = find_peaks(sig, prominence=0.3 * np.ptp(sig), distance=dist); tr, _ = find_peaks(-sig, prominence=0.3 * np.ptp(sig), distance=dist)
                n_tr += int(np.sum(_nearest(sw[ok], tr) < _nearest(sw[ok], pp))); n_ok += int(np.sum(ok))
    fr = {k: (v[0] / (v[0] + v[1] + v[2]), v[1] / (v[0] + v[1] + v[2]), v[0] + v[1] + v[2], float(np.mean(v[3])), float(np.mean(v[4])), v[2]) for k, v in tallies.items()}
    a, b = fr["repressor"], fr["own"]
    chk_a = a[0] > a[1]; chk_b = b[0] > b[1]; internal = chk_a != chk_b
    f_tr = n_tr / n_ok; min1 = _rp_det_min(RP_BE); min5 = _rp_det_min(5.0)
    out = outcome(crr=a[0], null=a[1], domain=None, check=chk_a, internal=internal)
    return make_row(d[2], d[3] + f": dm_i/dt = -m_i + alpha/(1 + p_(i-1)^n) + alpha0, dp_i/dt = -beta (p_i - m_i), alpha = {RP_AL}, alpha0 = {RP_AL0}, n = {RP_N}, beta = {RP_BE}; chemical Langevin noise with system size {RP_OM:.0f} (K = 1 is {RP_OM:.0f} molecules), Euler-Maruyama dt {RP_DT} over {RP_T:.0f} time units, seed 1, first 20 units dropped; mean period {per:.3f}",
                    source=src(pid),
                    Q=d[5] + " (computed as: per promoter switch, the distance to the nearest antipodal cut against the nearest protein extremum; 'nearer' as H-CUT's 'more often': the fraction of switches nearer the cut exceeds the fraction nearer the extremum; pooled over the three genes)",
                    ingredient=d[4] + " read two ways: (a) antipodal_cuts on the intrinsic phase of the repressor protein that acts on the promoter, (b) the same on the gene's own protein; cuts start at the first protein peak (the declared own event) and fire every half turn",
                    null=d[6] + f" (computed as: peak_cuts, maxima and minima, prominence 0.3 of the range, distance a quarter period = {dist} samples)",
                    domain=d[7],
                    numbers=f"{n_sw} promoter switches (half-occupancy crossings, K = 1, band 1.25); reading (a) repressor phase: nearer the cut {a[0]:.4f}, nearer the extremum {a[1]:.4f}, ties {a[5]}, of {a[2]}; mean distance to cut {a[3]:.3f}, to extremum {a[4]:.3f}; reading (b) own protein phase: nearer the cut {b[0]:.4f}, nearer the extremum {b[1]:.4f}, ties {b[5]}, of {b[2]}; mean distance to cut {b[3]:.3f}, to extremum {b[4]:.3f}",
                    tg=f"reading (a): fraction nearer the cut {a[0]:.4f} vs nearer the extremum {a[1]:.4f}: {ag(a[0], a[1])}",
                    tn="no domain theorem cited for the promoter switch against the antipode",
                    tc=f"reading (a) the switch nearer the cut more often: {hf(chk_a)}; reading (b): {hf(chk_b)}; the readings {_w(internal, 'disagree', 'agree')} {qtail(chk_a if not internal else None)}",
                    out=out,
                    reading=f"the promoter switches when its repressor crosses the half-occupancy level; the nearest repressor extremum is a trough for {f_tr:.4f} of the switches, and the antipodal cut lands {_w(a[3] > a[4], 'farther', 'nearer')} than the extremum on average ({a[3]:.3f} against {a[4]:.3f} time units) and {_w(a[0] > a[1], 'more', 'less')} often nearer; on the gene's own protein the extremum is {_w(b[4] < b[3], 'nearer', 'farther')} than the cut ({b[4]:.3f} against {b[3]:.3f}); the switch is a threshold crossing of the repressor, which is what the Hill function says, and neither the antipode nor the extremum is its cause",
                    weakness=f"beta = {RP_BE} is chosen so that the repressor crosses its half-occupancy level every cycle: the deterministic minimum of a protein is {min1:.4f} at beta = {RP_BE} and {min5:.4f} at beta = 5 (Elowitz and Leibler's other value), where the promoter {_w(min5 > 1.0, 'never', 'does')} switch{_w(min5 > 1.0, 'es', '')} without noise; the switch is a threshold crossing of a continuous occupancy, not a stochastic binding event; the Schmitt band 1.25 and the peak-finder prominence 0.3 are named constants, not swept; DEVIATION: declared.py names no parameters, but beta = 1 departs from the beta = 5 often quoted for the repressilator, and 'nearer' is scored per switch as H-CUT's 'more often' (mean distances printed beside it)",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] P07-4 Goodwin oscillator, the light PRC
GW = dict(v1=0.7, v2=0.35, k3=0.7, v4=0.35, k5=0.7, v6=0.35, n=6)             # Gonze et al. 2005 rates, Hill n = 6
GW_DT = 0.01


def _gw_scalar(x, y, z, L, sc):
    n = GW["n"]
    return (sc * (GW["v1"] / (1 + z ** n) - GW["v2"] * x / (1 + x)) + L, sc * (GW["k3"] * x - GW["v4"] * y / (1 + y)),
            sc * (GW["k5"] * y - GW["v6"] * z / (1 + z)))


def _gw_step(s, L, sc, dt=GW_DT):
    x, y, z = s
    a = _gw_scalar(x, y, z, L, sc); b = _gw_scalar(x + .5 * dt * a[0], y + .5 * dt * a[1], z + .5 * dt * a[2], L, sc)
    c = _gw_scalar(x + .5 * dt * b[0], y + .5 * dt * b[1], z + .5 * dt * b[2], L, sc); e = _gw_scalar(x + dt * c[0], y + dt * c[1], z + dt * c[2], L, sc)
    return (x + dt * (a[0] + 2 * b[0] + 2 * c[0] + e[0]) / 6, y + dt * (a[1] + 2 * b[1] + 2 * c[1] + e[1]) / 6, z + dt * (a[2] + 2 * b[2] + 2 * c[2] + e[2]) / 6)


def _gw_vec(X, L, sc, dt=GW_DT):
    n = GW["n"]
    def f(X):
        x, y, z = X[:, 0], X[:, 1], X[:, 2]
        return np.stack([sc * (GW["v1"] / (1 + z ** n) - GW["v2"] * x / (1 + x)) + L, sc * (GW["k3"] * x - GW["v4"] * y / (1 + y)), sc * (GW["k5"] * y - GW["v6"] * z / (1 + z))], -1)
    a = f(X); b = f(X + 0.5 * dt * a); c = f(X + 0.5 * dt * b); e = f(X + dt * c)
    return X + dt * (a + 2 * b + 2 * c + e) / 6


def _gw_period():
    s = (0.1, 0.2, 2.5)
    for _ in range(150000):
        s = _gw_step(s, 0.0, 1.0)
    zs = []
    for _ in range(6000):
        s = _gw_step(s, 0.0, 1.0); zs.append(s[2])
    zc = 0.5 * (min(zs) + max(zs)); ups = []; zp = s[2]
    for i in range(20000):
        s = _gw_step(s, 0.0, 1.0)
        if zp < zc <= s[2]:
            ups.append((i - 1 + (zc - zp) / (s[2] - zp)) * GW_DT)
        zp = s[2]
    return (ups[-1] - ups[0]) / (len(ups) - 1), zc, s


def _gw_floquet(n, settle=3000.0, dt=GW_DT):
    """Largest non-unit Floquet multiplier of the unforced cycle with Hill exponent n (monodromy by finite differences)."""
    def f(v):
        x, y, z = v
        return np.array([GW["v1"] / (1 + z ** n) - GW["v2"] * x / (1 + x), GW["k3"] * x - GW["v4"] * y / (1 + y), GW["k5"] * y - GW["v6"] * z / (1 + z)])
    def step(v, h):
        a = f(v); b = f(v + .5 * h * a); c = f(v + .5 * h * b); e = f(v + h * c); return v + h * (a + 2 * b + 2 * c + e) / 6
    v = np.array([0.1, 0.2, 2.5])
    for _ in range(int(settle / dt)):
        v = step(v, dt)
    zs = []; w = v.copy()
    for _ in range(int(60 / dt)):
        w = step(w, dt); zs.append(w[2])
    zc = 0.5 * (min(zs) + max(zs)); ups = []; zp = v[2]; w = v.copy()
    for i in range(int(200 / dt)):
        w = step(w, dt)
        if zp < zc <= w[2]:
            ups.append((i - 1 + (zc - zp) / (w[2] - zp)) * dt)
        zp = w[2]
    T = (ups[-1] - ups[0]) / (len(ups) - 1); N = int(round(T / dt)); h = T / N; eps = 1e-6
    def flow(u):
        for _ in range(N):
            u = step(u, h)
        return u
    base = flow(v.copy()); M = np.column_stack([(flow(v + eps * np.eye(3)[k]) - base) / eps for k in range(3)])
    mu = sorted(np.abs(np.linalg.eigvals(M)), key=lambda m: abs(m - 1.0))
    return T, float(max(mu[1:]))


def _gw_ct0(s, sc, L_ent, days=150):
    """LD 12:12 with light L_ent added to X production, lights on at ZT0; the state at ZT0 is released into constant darkness
    for ten 24-h cycles, so the returned state is on the limit cycle at CT0 (its asymptotic phase is ZT0's)."""
    for _ in range(days):
        for i in range(2400):
            s = _gw_step(s, L_ent if i < 1200 else 0.0, sc)
    for _ in range(24000):
        s = _gw_step(s, 0.0, sc)
    return np.array(s)


def _gw_marker(s, sc, zc, n_cyc=3):
    t = 0.0; zp = s[2]; s = tuple(s)
    for i in range(int(24 * n_cyc / GW_DT)):
        s = _gw_step(s, 0.0, sc)
        if zp < zc <= s[2] and i * GW_DT > 24 * (n_cyc - 1.5):
            return ((i - 1 + (zc - zp) / (s[2] - zp)) * GW_DT) % 24.0
        zp = s[2]
    return float("nan")


def _gw_prc(S0, sc, zc, cts, amps, kick=1e-4, days=8):
    """Pulses of 1 h centred at CT c (light amp added to X production) and instantaneous kicks of X by `kick` at CT c, all
    from the CT0 state; the phase shift is read from the Z upward mid-crossing after six cycles (advance positive)."""
    m = len(cts); N = m * (len(amps) + 1) + 1
    X = np.repeat(S0[None], N, 0); tt = np.concatenate([np.tile(cts, len(amps) + 1), [1e9]])
    amp = np.concatenate([np.repeat(amps, m), np.zeros(m + 1)]); is_kick = np.zeros(N, bool); is_kick[len(amps) * m:N - 1] = True
    kicked = np.zeros(N, bool); zz = []
    for i in range(int(round(24 * days / GW_DT))):
        t = i * GW_DT
        kk = is_kick & (~kicked) & (t >= tt - 1e-9); X[kk, 0] += kick; kicked |= kk
        L = np.where((~is_kick) & (t >= tt - 0.5 - 1e-9) & (t < tt + 0.5 - 1e-9), amp, 0.0)
        X = _gw_vec(X, L, sc); zz.append(X[:, 2].copy())
    zz = np.array(zz); ts = np.arange(1, len(zz) + 1) * GW_DT; mk = []
    for k in range(N):
        zk = zz[:, k]; i = np.nonzero((zk[:-1] < zc) & (zk[1:] >= zc) & (ts[:-1] > 24 * 6))[0][0]
        mk.append(ts[i] + (zc - zk[i]) / (zk[i + 1] - zk[i]) * GW_DT)
    mk = np.array(mk); sh = (mk[-1] - mk[:-1] + 12.0) % 24.0 - 12.0
    return [sh[j * m:(j + 1) * m] for j in range(len(amps))], sh[len(amps) * m:] / kick


def _crossings(cts, v, down=True, step=None):
    step = step or (cts[1] - cts[0]); o = []
    for k in range(len(cts)):
        a, b = v[k], v[(k + 1) % len(cts)]
        if (down and a > 0 >= b) or ((not down) and a < 0 <= b):
            o.append(float((cts[k] + step * a / (a - b)) % 24.0))
    return o


def _near(c, ref):
    return c + 24.0 * round((ref - c) / 24.0)


def r4():
    pid = "P07-4"; d = DECL[pid]
    T0, zc, s = _gw_period(); sc = T0 / 24.0
    S0 = _gw_ct0(s, sc, 1e-3)
    cts = np.arange(0.0, 24.0, 0.25); amps = (0.01, 0.03)
    prcs, iprc = _gw_prc(S0, sc, zc, cts, amps)
    noon = 6.0; anti = noon + 12.0                                             # subjective noon = ZT6 of the entraining LD 12:12
    x_fin = _crossings(cts, prcs[0]); x_inf = _crossings(cts, iprc); x_fin3 = _crossings(cts, prcs[1])
    u_fin = _crossings(cts, prcs[0], down=False); u_inf = _crossings(cts, iprc, down=False)
    if len(x_fin) != 1 or len(x_inf) != 1:
        out = outcome(unstated=True)
        return make_row(d[2], d[3], source=src(pid), Q=d[5], ingredient=d[4], null=d[6], domain=d[7],
                        numbers=f"advance-to-delay crossings: finite pulse {x_fin}, iPRC {x_inf}", tg="not formed", tn="not formed",
                        tc=f"the PRC does not have exactly one advance-to-delay crossover (finite {len(x_fin)}, infinitesimal {len(x_inf)}) {qtail(None)}",
                        out=out, reading="Q names one crossover; this PRC has none or several", weakness="")
    null = _near(x_fin[0], anti); dom = _near(x_inf[0], anti); tol = 0.01 * 24.0
    check = abs(null - anti) <= tol
    sens = []
    for Le in (3e-4, 3e-3):                                                   # CT origin under other entraining light levels
        off = (_gw_marker(_gw_ct0(s, sc, Le), sc, zc) - _gw_marker(S0, sc, zc) + 12.0) % 24.0 - 12.0
        sens.append(f"entraining light {Le:g}: crossover at CT {(x_fin[0] - off) % 24:.3f}")
    day_int = float(np.sum(iprc[cts < 12.0]) * 0.25 * 1e-3); night_int = float(np.sum(iprc[cts >= 12.0]) * 0.25 * 1e-3)
    in_day = 0.0 <= x_fin[0] < 12.0; locked = abs(day_int) < 0.1 * abs(night_int)
    u_near = _near(u_fin[0], anti) if u_fin else float("nan"); other_ok = abs(u_near - anti) <= tol
    T4, mu4 = _gw_floquet(4); T6, mu6 = _gw_floquet(GW["n"])
    out = outcome(crr=anti, null=null, domain=dom, check=check)
    return make_row(d[2], d[3] + f": dX/dt = v1/(1 + Z^n) - v2 X/(1 + X) + L, dY/dt = k3 X - v4 Y/(1 + Y), dZ/dt = k5 Y - v6 Z/(1 + Z) (Gonze et al. 2005 rates, n = {GW['n']}), time rescaled so the free-running period {T0:.4f} h becomes 24 h; CT defined by entrainment to LD 12:12 with light 1e-3 on X production (150 days), subjective noon = ZT6 = CT6; RK4 dt {GW_DT} h; PRC from 1-h pulses of amplitude {amps[0]} centred on 96 CTs, read after six cycles",
                    source=src(pid),
                    Q=d[5] + f" (computed as: the CT where the PRC changes sign from advance to delay as CT increases, against CT {anti:.1f}; 'at' within 1 % of the period, {tol:.2f} h)",
                    ingredient=d[4] + ": the cut half a turn (12 h of a 24-h rotor) from subjective noon",
                    null=d[6] + f" (computed as: the finite-pulse PRC's advance-to-delay crossing, pulse amplitude {amps[0]})",
                    domain=d[7] + " (computed as: the advance-to-delay crossing of the response to an instantaneous kick of X, 1e-4, divided by the kick)",
                    numbers=f"antipode of noon CT {anti:.2f}; advance-to-delay crossover: finite pulse CT {x_fin[0]:.3f} (amplitude {amps[1]}: CT {x_fin3[0] if x_fin3 else float('nan'):.3f}), infinitesimal PRC CT {x_inf[0]:.3f}; delay-to-advance crossover: finite CT {u_fin[0] if u_fin else float('nan'):.3f}, infinitesimal CT {u_inf[0] if u_inf else float('nan'):.3f}; max advance {float(np.max(prcs[0])):.3f} h, max delay {float(-np.min(prcs[0])):.3f} h; weak-light locking check: 1e-3 x iPRC integrated over subjective day {day_int:+.4f} h, over subjective night {night_int:+.4f} h; sensitivity: {'; '.join(sens)}",
                    tg=f"antipode CT {anti:.3f} vs the PRC's own crossover CT {null:.3f} (unwrapped to the nearest turn): {ag(anti, null)}",
                    tn=f"antipode CT {anti:.3f} vs the infinitesimal PRC's crossover CT {dom:.3f}: {ag(anti, dom, TOL_N)}",
                    tc=f"|crossover - antipode| = {abs(null - anti):.3f} h <= {tol:.2f} h: {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"the advance-to-delay crossover lies at CT {x_fin[0]:.3f}, {abs(_near(x_fin[0], noon) - noon):.3f} h from subjective noon and {abs(null - anti):.3f} h from its antipode, {_w(in_day, 'inside', 'outside')} the subjective day; phase-response theory says where it must be: an oscillator whose free period equals the day locks where the light window's integrated PRC is zero and falling, and here the weak entraining light integrated over the subjective day shifts the phase by {day_int:+.4f} h against {night_int:+.4f} h over the night ({_w(locked, 'near zero', 'not near zero')}: below a tenth of the night's {_w(locked, 'holds', 'fails')}), so the day sits across the advance-to-delay crossover; the other crossover (delay to advance, CT {u_fin[0] if u_fin else float('nan'):.3f}) is {abs(u_near - anti):.3f} h from the antipode ({_w(other_ok, 'within', 'outside')} {tol:.2f} h)",
                    weakness=f"'from advance to delay' is read literally (sign change + to - as CT increases); the other sign change is printed and is {_w(other_ok, 'within', 'outside')} the tolerance too; light acts on X production only (Gonze et al. 2005); Hill n = {GW['n']} instead of Gonze's n = 4: the largest non-unit Floquet multiplier of the unforced cycle is {mu4:.4f} per {T4:.2f}-h cycle at n = 4 against {mu6:.4f} per {T6:.2f}-h cycle at n = {GW['n']}, so the n = 4 cycle is {_w(mu4 > mu6, 'the more weakly attracting', 'not the more weakly attracting')} one, and the phase reduction that defines CT and the iPRC needs a strongly attracting cycle; subjective noon is defined by entrainment to LD 12:12, one of several conventions (an activity-onset marker would move it); 1-h pulses; DEVIATION: Hill n = 6 rather than the n = 4 of Gonze et al. 2005, and subjective noon fixed by entrainment to LD 12:12 with light on X production (declared.py names neither)",
                    elegance="", child="")


# ---------------------------------------------------------------- [5] P07-5 calcium spikes under IP3 noise
CA = dict(v0=1.0, k=10.0, kf=1.0, v1=7.3, VM2=65.0, VM3=500.0, K2=1.0, KR=2.0, KA=0.9)
CA_DT, CA_T, CA_SD, CA_TAU, CA_REC = 0.001, 400.0, 0.05, 2.0, 10
CA_LEVELS = (0.3, 0.35, 0.4)


def _ca_f(Z, Y, b):
    v2 = CA["VM2"] * Z * Z / (CA["K2"] ** 2 + Z * Z)
    v3 = CA["VM3"] * Y * Y / (CA["KR"] ** 2 + Y * Y) * Z ** 4 / (CA["KA"] ** 4 + Z ** 4)
    return CA["v0"] + CA["v1"] * b - v2 + v3 + CA["kf"] * Y - CA["k"] * Z, v2 - v3 - CA["kf"] * Y


def _ca_run(bbar, seed):
    rng = np.random.default_rng(seed); ns = int(round(CA_T / CA_DT)); e = rng.standard_normal(ns); dt = CA_DT
    a = math.exp(-dt / CA_TAU); s = CA_SD * math.sqrt(1 - a * a)
    Z, Y, eta = 0.2, 1.5, 0.0; out = np.empty(ns // CA_REC); j = 0
    for i in range(ns):
        eta = a * eta + s * e[i]; b = min(max(bbar + eta, 0.0), 1.0)          # IP3 saturation beta: OU noise, clipped to [0, 1]
        k1 = _ca_f(Z, Y, b); k2 = _ca_f(Z + .5 * dt * k1[0], Y + .5 * dt * k1[1], b)
        k3 = _ca_f(Z + .5 * dt * k2[0], Y + .5 * dt * k2[1], b); k4 = _ca_f(Z + dt * k3[0], Y + dt * k3[1], b)
        Z += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; Y += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
        if (i + 1) % CA_REC == 0:
            out[j] = Z; j += 1
    return out


def _ca_spikes(z, up=0.75, arm=0.45):
    ev = []; armed = False
    for i in range(1, len(z)):
        if z[i] < arm:
            armed = True
        if armed and z[i - 1] < up <= z[i]:
            ev.append(i); armed = False
    return np.array(ev)


def r5():
    pid = "P07-5"; d = DECL[pid]
    res = {}; isi_stats = []; amps = []
    for k, bb in enumerate(CA_LEVELS):
        z = _ca_run(bb, seed=k); ev = _ca_spikes(z); ev = ev[ev * CA_DT * CA_REC > 2.0]
        r = regularity(z, ev, sigma=1.0, dt=CA_DT * CA_REC, n_boot=N_BOOT, seed=SEED_BOOT); res[bb] = r
        isi = np.diff(ev) * CA_DT * CA_REC; isi_stats.append((float(isi.mean()), float(isi.std(ddof=1))))
        amps.append(float(np.mean([np.ptp(z[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])])))
    mu = np.array([m for m, _ in isi_stats]); sd = np.array([s for _, s in isi_stats])
    skupin = float(np.sum(mu * sd) / np.sum(mu * mu))                        # SD = alpha * mean, least squares through 0
    r = res[CA_LEVELS[0]]; check = r["ci95"][1] < 0.0
    d_amp = rel(amps[0], amps[-1]); d_isi = rel(mu[0], mu[-1])
    out = outcome(crr=r["cv_arc"], null=r["cv_clock"], domain=skupin, check=check)
    per = "; ".join(f"beta {bb}: {res[bb]['n']} ISIs, mean {m:.3f} s, CV(arc) {res[bb]['cv_arc']:.4f}, CV(ISI) {res[bb]['cv_clock']:.4f} ({_ci(res[bb]['ci95'])}), CV(amp) {res[bb]['cv_amp']:.4f}" for bb, (m, _) in zip(CA_LEVELS, isi_stats))
    amp_ok = r["ci95_amp"][1] < 0.0
    return make_row(d[2], d[3] + f": the Goldbeter-Dupont-Berridge two-pool model (v0 1, k 10, kf 1, v1 7.3, VM2 65, VM3 500, K2 1, KR 2, KA 0.9; m = n = 2, p = 4), IP3 saturation beta = beta_bar + Ornstein-Uhlenbeck noise (sd {CA_SD}, time constant {CA_TAU} s) clipped to [0, 1]; RK4 dt {CA_DT} s over {CA_T:.0f} s per level; a spike is cytosolic Ca crossing 0.75 uM upward after falling below 0.45 uM; decisive level beta_bar = {CA_LEVELS[0]}",
                    source=src(pid),
                    Q=d[5] + " (computed as: regularity() on the Ca trace between spikes, identity metric, the paired-bootstrap CI of CV(arc) - CV(ISI) below 0)",
                    ingredient=d[4] + ": regularity() on the own events (Ca spikes), n_boot 2000, seed 0",
                    null=d[6],
                    domain=d[7] + f" (computed as: the Skupin slope alpha of SD(ISI) = alpha mean(ISI) fitted through 0 over beta_bar in {CA_LEVELS})",
                    numbers=f"beta_bar {CA_LEVELS[0]}: CV(arc) {r['cv_arc']:.4f}, CV(ISI) {r['cv_clock']:.4f}, difference {r['diff']:+.4f}, 95 % CI [{r['ci95'][0]:+.4f}, {r['ci95'][1]:+.4f}]; amplitude control CV(amp) {r['cv_amp']:.4f}, CV(arc) - CV(amp) {r['diff_amp']:+.4f} CI [{r['ci95_amp'][0]:+.4f}, {r['ci95_amp'][1]:+.4f}]; Skupin slope {skupin:.4f}; per level: {per}",
                    tg=f"CV(arc) {r['cv_arc']:.4f} vs CV(ISI) {r['cv_clock']:.4f}: {ag(r['cv_arc'], r['cv_clock'])}",
                    tn=f"CV(arc) {r['cv_arc']:.4f} vs the Skupin slope {skupin:.4f}: {ag(r['cv_arc'], skupin, TOL_N)}",
                    tc=f"CV(arc) < CV(ISI) with the CI below 0: {hf(check)} {qtail(check)}",
                    out=out,
                    reading=f"IP3 noise spreads the spike times (CV(ISI) {r['cv_clock']:.4f}) {_w(r['cv_arc'] < r['cv_clock'], 'more', 'less')} than the arc per spike (CV {r['cv_arc']:.4f}): calcium-induced calcium release fires a stereotyped excursion: across the three IP3 levels the mean spike amplitude goes {amps[0]:.3f}, {amps[1]:.3f}, {amps[2]:.3f} uM (relative change {d_amp:.3f}) while the mean ISI goes {mu[0]:.3f}, {mu[1]:.3f}, {mu[2]:.3f} s (relative change {d_isi:.3f}), so IP3 sets the {_w(d_isi > d_amp, 'frequency more than the amplitude', 'amplitude at least as much as the frequency')}; the arc's regularity is the amplitude's: CRR.md's control (i), arc beyond amplitude, {hf(amp_ok)} (CV(amp) {r['cv_amp']:.4f} against CV(arc) {r['cv_arc']:.4f}); constant spike amplitude with frequency coding is the domain's textbook picture (Berridge's frequency encoding), so the {out} label rests on the bare inequality the declaration wrote, not on H-L5 with its controls",
                    weakness=f"the declared Q is the bare inequality; CRR.md's H-L5 adds three controls, and the amplitude control {hf(amp_ok)} here, so a gate-level reading {_w(amp_ok, 'would', 'would not')} count this as class membership; one noise model (OU on beta) and no calcium-channel noise (Skupin's puffs); identity metric on the Ca concentration",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P07: chemistry and cell biology (prompt-log entry 234; Predictions70/DECLARATION.md; declared at 8397478)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
