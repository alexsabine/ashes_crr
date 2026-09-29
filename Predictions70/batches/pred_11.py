"""PRED70 batch P11: physiology (Predictions70/DECLARATION.md; declared.py pushed at 8397478 before this file existed).
[1] Bergman's minimal glucose-insulin model after a meal, remote insulin action X remembered by A6; [2] Borbely's
two-process sleep model, sleep onset against the antipodal cut of process C; [3] respiratory sinus arrhythmia (an IPFM
sinus node modulated by breathing), H-L5 per breath; [4] repeated dosing with first-order elimination, A6 accumulation
against the pharmacokinetic accumulation factor; [5] a reduced ovarian-pituitary hormone oscillator with noise, H-L5
between ovulations. Literature named by name and year only (R10): Bergman et al. 1979; Borbely 1982; Daan, Beersma and
Borbely 1984; Hirsch and Bishop 1981; Hyndman and Mohn 1975 (IPFM); Rowland and Tozer (textbook accumulation factor);
Keener and Sneyd 2009. Q, null and H0 are printed verbatim from declared.py. Deterministic (fixed seeds, fixed grids,
explicit RK4); under two minutes."""
import math
import os
import sys

import numpy as np
from scipy.signal import find_peaks

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P as _DECLARED  # noqa: E402

from crr.instrument.core import antipodal_cuts, intrinsic_phase, regularity  # noqa: E402
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


# ---------------------------------------------------------------- [1] Bergman minimal model with A6-remembered X
BP = dict(p1=0.03, p2=0.02, p3=1.3e-5, Gb=90.0, Ib=10.0, n=0.2, gam=0.1, Dm=60.0, ka=0.04)


def _bergman(Tm, dt=0.1, tend=600.0):
    """Glucose after a meal. dG/dt = -(p1 + Xe) G + p1 Gb + Ra(t); dX/dt = -p2 X + p3 (I - Ib);
    dI/dt = -n (I - Ib) + gam (G - Gb)^+; Ra = Dm ka^2 t exp(-ka t). Xe = X (Bergman) or the A6-remembered M,
    dM/dt = (X - M)/Tm (P3's exponential kernel, mean age Tm). Returns (peak, nadir after the peak, nadir time)."""
    p1, p2, p3, Gb, Ib, n_, gam, Dm, ka = (BP[k] for k in ("p1", "p2", "p3", "Gb", "Ib", "n", "gam", "Dm", "ka"))

    def f(t, G, X, I, M):
        Xe = X if Tm == 0 else M
        return (-(p1 + Xe) * G + p1 * Gb + Dm * ka * ka * t * math.exp(-ka * t), -p2 * X + p3 * (I - Ib),
                -n_ * (I - Ib) + gam * max(G - Gb, 0.0), 0.0 if Tm == 0 else (X - M) / Tm)
    s = (Gb, 0.0, Ib, 0.0); t = 0.0; Gs = [Gb]
    for _ in range(int(round(tend / dt))):
        k1 = f(t, *s); k2 = f(t + dt / 2, *[a + dt / 2 * b for a, b in zip(s, k1)])
        k3 = f(t + dt / 2, *[a + dt / 2 * b for a, b in zip(s, k2)]); k4 = f(t + dt, *[a + dt * b for a, b in zip(s, k3)])
        s = tuple(a + dt * (b + 2 * c + 2 * d + e) / 6 for a, b, c, d, e in zip(s, k1, k2, k3, k4)); t += dt; Gs.append(s[0])
    Gs = np.array(Gs); ip = int(np.argmax(Gs)); j = ip + int(np.argmin(Gs[ip:]))
    return float(Gs[ip]), float(Gs[j]), j * dt


def r1():
    pid = "P11-1"; d = D[pid]
    occ = 1.0 / BP["p2"]                                                       # occasion = X's own time constant (min)
    Tm = occ * Q_A6 / (1 - Q_A6)
    pk0, nad0, tn0 = _bergman(0.0); pkm, nadm, tnm = _bergman(Tm)
    crr, null, dom = nadm, nad0, nad0
    change = rel(crr, null); check = change < 0.01
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    grid = [(q, occ * q / (1 - q), rel(_bergman(occ * q / (1 - q))[1], nad0)) for q in QGRID]
    occs = [(o, rel(_bergman(o * Q_A6 / (1 - Q_A6))[1], nad0)) for o in (1.0, 10.0, 300.0)]
    sweep = np.geomspace(1.0, 3000.0, 41)                                      # occasion scan (min), q = 0.5: where is the change below 1 %?
    below = [rel(_bergman(o * Q_A6 / (1 - Q_A6))[1], nad0) < 0.01 for o in sweep]
    bands, k = [], 0
    while k < len(sweep):
        if below[k]:
            j = k
            while j + 1 < len(sweep) and below[j + 1]: j += 1
            bands.append((sweep[k], sweep[j])); k = j + 1
        else:
            k += 1
    bands_txt = "; ".join(f"{a:.1f}-{b:.1f} min" for a, b in bands) if bands else "none"
    n_long = _bergman(sweep[-1] * Q_A6 / (1 - Q_A6))[1]
    dep0, depm = BP["Gb"] - nad0, BP["Gb"] - nadm
    return make_row(d[2], d[3] + f"; model: dG/dt = -(p1 + X) G + p1 Gb + Ra(t), dX/dt = -p2 X + p3 (I - Ib), dI/dt = -n (I - Ib) + gam (G - Gb)^+, meal Ra = D ka^2 t e^(-ka t); p1 {BP['p1']}/min, p2 {BP['p2']}/min, p3 {BP['p3']:g}, Gb {BP['Gb']:g} mg/dl, Ib {BP['Ib']:g} uU/ml, n {BP['n']}/min, gam {BP['gam']}, D {BP['Dm']:g} mg/dl, ka {BP['ka']}/min; RK4 dt 0.1 min over 600 min",
                    source=_src(pid), Q=d[5] + " (computed as: the glucose minimum after the post-meal peak, with glucose driven by the A6-remembered M in place of X, against Bergman's X; relative change)",
                    ingredient=d[4] + f" with P3's exponential kernel: dM/dt = (X - M)/T_m, mean age T_m = q/(1 - q) occasions, q = {Q_A6}; occasion = X's own time constant 1/p2 = {occ:.1f} min, so T_m = {Tm:.1f} min",
                    null=d[6], domain=d[7],
                    numbers=f"nadir: with A6 {nadm:.4f} mg/dl at {tnm:.1f} min, with X {nad0:.4f} mg/dl at {tn0:.1f} min (peak {pkm:.3f} against {pk0:.3f}); relative change {change:.4f}; q-grid (occasion {occ:.0f} min): " + "; ".join(f"q {q}: T_m {t:.1f} min, change {c:.4f}" for q, t, c in grid) + "; occasion sweep at q = 0.5: " + "; ".join(f"occasion {o:.0f} min: change {c:.4f}" for o, c in occs) + f"; occasions (41-point log scan, 1-3000 min) with the change below 1 %: {bands_txt}",
                    tg=f"nadir {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Bergman's model (X alone) gives {dom:.4f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"relative change of the nadir {change:.4f} below 0.01: {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"remembering X at a mean age of one occasion of X's own length lags insulin action further, so the glucose nadir {_w(nadm < nad0, 'deepens', 'rises')} from {nad0:.3f} to {nadm:.3f} mg/dl ({change:.4f} relative); X is an exponential memory already, but a second exponential memory in series is a different kernel (gamma-2), not a no-op; the change is below 1 % only on the scanned occasion bands {bands_txt}; at the longest scanned occasion ({sweep[-1]:.0f} min) the nadir is {n_long:.3f} mg/dl, {_w(n_long > nad0, 'above', 'below')} Bergman's{_w(len(bands) > 1 and n_long > nad0, ', so the later band is where a deeper lagged dip and a weaker insulin action cross: a coincidence of two effects, not an absence of effect', '')}",
                    weakness=f"DEVIATION: declared.py names no occasion for A6 in a single-meal response (CRR's [O3]: no rotor sets it); the decisive occasion is X's own time constant 1/p2 (the unit in which the model states X's memory), and the verdict flips on the occasion bands {bands_txt} (printed). The meal and secretion terms are added because Bergman's minimal model is an IVGTT model; the nadir is dominated by the basal level: the depth below basal changes from {dep0:.3f} to {depm:.3f} mg/dl ({rel(depm, dep0):.4f} relative)",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] Borbely two-process model: onset against the antipodal cut
def _c_skew(t):
    w = 2 * math.pi / 24.0
    return 0.97 * math.sin(w * t) + 0.22 * math.sin(2 * w * t) + 0.07 * math.sin(3 * w * t) + 0.03 * math.sin(4 * w * t) + 0.001 * math.sin(5 * w * t)


def _borbely(cfun, days=40, dt=1.0 / 60.0, tw=18.2, ts=4.2, H0=0.67, L0=0.17, a=0.12):
    n = int(round(days * 24 / dt)); t = np.arange(n + 1) * dt; C = np.array([cfun(x) for x in t])
    S = 0.5; awake = True; on, wk = [], []
    ew, es = math.exp(-dt / tw), math.exp(-dt / ts)
    for i in range(n):
        if awake:
            S = 1.0 - (1.0 - S) * ew
            if S >= H0 + a * C[i + 1]: awake = False; on.append(i + 1)
        else:
            S = S * es
            if S <= L0 + a * C[i + 1]: awake = True; wk.append(i + 1)
    ph = intrinsic_phase(C)
    rows = []
    for w_ in wk:
        if t[w_] < 5 * 24 or t[w_] > (days - 5) * 24: continue                 # drop the transient and the Hilbert edges
        nxt = [o for o in on if o > w_]
        if not nxt: continue
        cut = antipodal_cuts(ph, start=w_)[1]
        rows.append(((nxt[0] - w_) * dt, (cut - w_) * dt, (ph[nxt[0]] - ph[w_]) / math.pi))
    return np.array(rows)


def r2():
    pid = "P11-2"; d = D[pid]
    R = _borbely(_c_skew); onset, anti, adv = R[:, 0], R[:, 1], R[:, 2]
    per_day = np.array([rel(a_, o_) <= TOL_N for a_, o_ in zip(anti, onset)])
    crr, null, dom = float(np.mean(anti)), float(np.mean(onset)), float(np.mean(onset))
    check = bool(per_day.all()); out = outcome(crr=crr, null=null, domain=dom, check=check)
    Rs = _borbely(lambda t: math.sin(2 * math.pi * t / 24.0))
    sleep_h = 24.0 - null
    return make_row(d[2], d[3] + "; model: S rises as 1 - (1 - S) e^(-dt/18.2 h) awake and decays as S e^(-dt/4.2 h) asleep; onset when S reaches 0.67 + 0.12 C(t), wake when S falls to 0.17 + 0.12 C(t); C the Daan-Beersma-Borbely skewed sine (five harmonics); 40 days at 1-min steps, days 5-35 scored",
                    source=_src(pid), Q=d[5] + " (computed as: from each wake-up, the first antipodal cut of the analytic-signal phase of C (half a turn later) against the model's sleep onset; per day, within 1 %)",
                    ingredient=d[4] + " (antipodal_cuts on intrinsic_phase of C, started at the wake-up sample)",
                    null=d[6], domain=d[7],
                    numbers=f"{len(R)} days scored; wake-to-onset {null:.4f} h (S-threshold crossing), wake-to-antipodal-cut {crr:.4f} h; circadian phase advanced from wake to onset {np.mean(adv):.4f} pi (the antipode is 1 pi); days with the cut within 1 % of the onset: {int(per_day.sum())}/{len(per_day)}; sensitivity, pure-sine C: onset {np.mean(Rs[:, 0]):.4f} h, cut {np.mean(Rs[:, 1]):.4f} h, phase advanced {np.mean(Rs[:, 2]):.4f} pi",
                    tg=f"cut {crr:.4f} h vs S-threshold onset {null:.4f} h: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the two-process onset {dom:.4f} h: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"onset at the antipodal cut on every scored day ({int(per_day.sum())}/{len(per_day)}): {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"the antipode of C's phase comes {null - crr:.3f} h {_w(crr < null, 'before', 'after')} the modelled onset: the sleeper stays awake for {np.mean(adv):.4f} pi of circadian phase, not pi, because onset is set by where the rising homeostatic pressure meets the upper threshold, and a {null:.2f}-h wake / {sleep_h:.2f}-h sleep day is {_w(rel(null, 12.0) <= TOL_N, 'a half-turn', 'not a half-turn')}",
                    weakness="the two-process model is deterministic, so every day is identical after the transient; the phase is the Hilbert phase of C (the one implemented intrinsic phase); a Poincare phase was not tried",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] respiratory sinus arrhythmia: H-L5 per breath
def _rsa(nb=400, mb=4.0, cvb=0.2, cvv=0.15, m0=0.07, lf=0.02, jit=0.01, RR0=0.85, seed=11, fs=20.0, h=0.002):
    rng = np.random.default_rng(seed)
    k = 1.0 / cvb ** 2; Tb = rng.gamma(k, mb / k, nb); on = np.r_[0.0, np.cumsum(Tb)]
    sv = math.sqrt(math.log(1 + cvv ** 2)); V = np.exp(rng.normal(-0.5 * sv * sv, sv, nb)); ph_lf = rng.uniform(0, 2 * math.pi)
    t = np.arange(0.0, on[-1], h); j = np.minimum(np.searchsorted(on, t, side="right") - 1, nb - 1)
    vol = V[j] * (1 - np.cos(2 * math.pi * (t - on[j]) / Tb[j])) / 2
    rate = (1 + m0 * vol + lf * np.sin(2 * math.pi * 0.1 * t + ph_lf)) / RR0         # IPFM: a beat each time the integral reaches 1
    Phi = np.r_[0.0, np.cumsum(0.5 * (rate[1:] + rate[:-1]) * h)]
    beats = np.interp(np.arange(1, int(Phi[-1]) + 1), Phi, t)
    rr = np.diff(beats) * (1 + jit * rng.standard_normal(len(beats) - 1)); tb = beats[1:]
    grid = np.arange(tb[0], tb[-1], 1.0 / fs); x = np.interp(grid, tb, rr)
    ev = np.array([int(round((o - grid[0]) * fs)) for o in on if grid[0] <= o <= grid[-1]])
    return regularity(x, ev, dt=1.0 / fs), len(beats)


def r3():
    pid = "P11-3"; d = D[pid]
    r, nbeat = _rsa()
    crr, null = r["cv_arc"], r["cv_clock"]; check = r["ci95"][1] < 0
    out = outcome(crr=crr, null=null, domain=None, check=check)
    sens = [("no beat jitter", dict(jit=0.0)), ("no jitter, no Mayer wave", dict(jit=0.0, lf=0.0)),
            ("pure RSA (constant tidal volume, no jitter, no Mayer wave)", dict(jit=0.0, lf=0.0, cvv=0.0))]
    srows = [(nm, _rsa(**kw)[0]) for nm, kw in sens]
    regular = [nm for nm, x in srows if x["ci95"][1] < 0]
    flips = [nm for nm, x in srows if (x["ci95"][1] < 0) != check]
    return make_row(d[2], d[3] + f"; model: breaths gamma-distributed (mean 4 s, CV 0.2), tidal volume per breath lognormal (CV 0.15); an IPFM sinus node with rate (1 + 0.07 x lung volume + 0.02 sin(2 pi 0.1 t)) / 0.85 s and 1 % beat jitter; the heart-period series resampled at 20 Hz; own events = inspiration onsets; {r['n']} breaths, {nbeat} beats, seed 11",
                    source=_src(pid), Q=d[5] + " (computed as: CV of the arc of the resampled heart-period series between inspiration onsets against CV of the breath duration, paired bootstrap n_boot 2000 seed 0, CI excluding 0 below)",
                    ingredient=d[4] + " (regularity, identity metric on the heart period, segment_end inclusive)",
                    null=d[6], domain=d[7],
                    numbers=f"CV(arc per breath) {crr:.4f}, CV(breath duration) {null:.4f}, difference {r['diff']:+.4f}, 95 % CI {_ci(r)}; amplitude control CV(peak-to-trough per breath) {r['cv_amp']:.4f}; sensitivity: " + "; ".join(f"{nm}: CV(arc) {s['cv_arc']:.4f}, CV(clock) {s['cv_clock']:.4f}, CI {_ci(s)}" for nm, s in srows),
                    tg=f"CV(arc) {crr:.4f} vs null CV(breath duration) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"CV(arc) - CV(breath) CI {_ci(r)} lies below 0: {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"the heart-period arc per breath is {_w(crr < null, 'more', 'less')} regular than the breath ({crr:.4f} against {null:.4f}); removing the other sources in turn gives CV(arc) " + ", ".join(f"{x['cv_arc']:.4f} ({nm})" for nm, x in srows) + f": {_w(all(a_ > b_ for a_, b_ in zip([crr] + [x['cv_arc'] for _, x in srows], [x['cv_arc'] for _, x in srows])), 'each of beat jitter, the 0.1-Hz Mayer wave and tidal-volume variation adds arc variability that is not tied to the breath', 'the sources do not add arc variability monotonically')}; the sensitivity variants that are arc-regular (CI below 0): {', '.join(regular) if regular else 'none'}",
                    weakness=f"one synthetic IPFM model; the RSA gain is flat in breathing frequency (vagal transfer taken as flat); a frequency-dependent RSA transfer (larger swings for slower breaths) was not tried; the noise levels are named choices; sensitivity variants that flip the verdict: {', '.join(flips) if flips else 'none'} ({len(flips)} of {len(srows)})",
                    elegance="", child="")


# ---------------------------------------------------------------- [4] repeated dosing: A6 accumulation against 1/(1 - e^{-kT})
def _pk_trough_ratio(kT, nd=60, steps=200):
    """Bolus dose 1 every T, dC/dt = -k C integrated by RK4 (steps per interval); trough = level just before a dose."""
    C = 0.0; tr = []; h = kT / steps
    for _ in range(nd):
        C += 1.0
        for _ in range(steps):
            k1 = -C; k2 = -(C + h / 2 * k1); k3 = -(C + h / 2 * k2); k4 = -(C + h * k3); C += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        tr.append(C)
    return tr[-1] / tr[0]


def _a6_ratio(q, nd=60):
    """A6: the remembered level M_n = (1 - q) x_n + q M_{n-1}, one occasion per dose, the body empty at the start."""
    M = 0.0; ms = []
    for _ in range(nd):
        M = (1 - q) * 1.0 + q * M; ms.append(M)
    return ms[-1] / ms[0]


def r4():
    pid = "P11-4"; d = D[pid]
    regs = (0.5, 1.0, 2.0)                                                     # dosing interval T in half-lives
    a6 = _a6_ratio(Q_A6); rows = []
    for r_ in regs:
        kT = r_ * math.log(2.0); dom = 1.0 / (1.0 - math.exp(-kT)); sim = _pk_trough_ratio(kT)
        rows.append((r_, dom, sim, rel(a6, sim) <= TOL_N))
    worst = max(rows, key=lambda z: rel(a6, z[1]))
    crr, null, dom = a6, 1.0, worst[1]
    check = all(z[3] for z in rows); out = outcome(crr=crr, null=null, domain=dom, check=check)
    per = "; ".join(f"T = {r_} half-lives: accumulation factor {dm:.4f} (RK4 trough ratio {sm:.4f}), A6 {a6:.4f}, {_w(ok, 'equal', 'differ')}, per-regimen label {outcome(crr=a6, null=1.0, domain=dm, check=ok)}" for r_, dm, sm, ok in rows)
    qg = "; ".join(f"q {q}: {_a6_ratio(q):.4f}" for q in QGRID)
    return make_row(d[2], d[3] + "; model: unit bolus every T, dC/dt = -k C by RK4 (200 steps per interval), 60 doses; trough = the level just before a dose; accumulation = steady-state trough / first trough; regimens T/t_half in {0.5, 1, 2}",
                    source=_src(pid), Q=d[5] + " (computed as: the A6 remembered level, one occasion per dose, steady state over first occasion, against the steady-state over first trough ratio of first-order elimination, on each of three dosing regimens; all must agree within 1 %)",
                    ingredient=d[4] + f" with P3's geometric weights, q = {Q_A6} per occasion, occasion = one dosing interval (a dose is the system's own event, CRR [M])",
                    null=d[6], domain=d[7],
                    numbers=f"A6 accumulation factor {a6:.4f} whatever the regimen; {per}; q-grid (A6 factor): {qg}; decisive regimen (largest gap): T = {worst[0]} half-lives",
                    tg=f"A6 {crr:.4f} vs no memory {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the accumulation factor at T = {worst[0]} half-lives is {dom:.4f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"A6 equals the simulated trough ratio on {sum(z[3] for z in rows)}/{len(rows)} regimens: {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"A6 with a fixed q = {Q_A6} per dose accumulates by 1/(1 - q) = {a6:.4f}, which is the pharmacokinetic factor only when a dose is given once per half-life (e^(-kT) = q); at other intervals the drug's own elimination sets the factor and a fixed memory weight cannot know it; the geometric series is the same, the weight is the drug's",
                    weakness="DEVIATION: declared.py names no dosing regimen and CRR fixes q = 0.5 while the accumulation factor depends on kT, so Q is scored on three regimens (all must hold) and the harness is given the regimen with the largest gap; on the once-per-half-life regimen alone the row would read REDUNDANT-DOMAIN (printed per regimen)",
                    elegance="Take a pill each time half of the last one has left your body and your body settles at twice the first dose: the same halving rule as remembering with q = 1/2.",
                    child="If your body gets rid of half the medicine before the next pill, the medicine builds up until there is twice as much as after the first pill, and then it stays there.")


# ---------------------------------------------------------------- [5] a reduced ovarian-pituitary oscillator: H-L5 between ovulations
MP = dict(g=0.5, s0=1e-3, Kp=0.1, Ke=0.7, nE=20, tauE=1.0, syn=0.1, c=2.0, r0=0.002, r1=20.0, kov=20.0, Lov=0.3, tauC=8.0)


def _mens(days, sig, seed, dt=0.01, tc=2.0):
    """F follicle, E estradiol, R pituitary LH reserve, L serum LH, P progesterone (corpus luteum).
    dF = g (1 + xi) fsh F (1 - F) + s0 fsh - kov H(L) F; dE = (F - E)/tauE; dR = syn - rel R; dL = rel R - c L;
    dP = kov H(L) F - P/tauC; fsh = 1/(1 + (P/Kp)^2); rel = r0 + r1 E^nE/(Ke^nE + E^nE); H(L) = L^8/(Lov^8 + L^8);
    xi an OU process (sd sig, correlation time tc days) on the follicular growth rate."""
    g, s0, Kp, Ke, nE, tauE, syn, c, r0, r1, kov, Lov, tauC = (MP[k] for k in ("g", "s0", "Kp", "Ke", "nE", "tauE", "syn", "c", "r0", "r1", "kov", "Lov", "tauC"))

    def f(F, E, R, L, P, xi):
        fsh = 1.0 / (1.0 + (P / Kp) ** 2); rel_ = r0 + r1 * E ** nE / (Ke ** nE + E ** nE); ov = kov * L ** 8 / (Lov ** 8 + L ** 8) * F
        return (g * (1 + xi) * fsh * F * (1 - F) + s0 * fsh - ov, (F - E) / tauE, syn - rel_ * R, rel_ * R - c * L, ov - P / tauC)
    rng = np.random.default_rng(seed); n = int(round(days / dt)); a = math.exp(-dt / tc); b = sig * math.sqrt(1 - a * a)
    e = rng.standard_normal(n); z = 0.0; s = (0.01, 0.01, 2.5, 0.0, 0.0); out = np.empty((n + 1, 5)); out[0] = s
    for i in range(n):
        z = a * z + b * e[i]
        k1 = f(*s, z); k2 = f(*[p + dt / 2 * q for p, q in zip(s, k1)], z); k3 = f(*[p + dt / 2 * q for p, q in zip(s, k2)], z)
        k4 = f(*[p + dt * q for p, q in zip(s, k3)], z)
        s = tuple(p + dt * (u + 2 * v + 2 * w + y) / 6 for p, u, v, w, y in zip(s, k1, k2, k3, k4)); out[i + 1] = s
    Z = out[int(round(200 / dt)):]                                             # discard 200 days of transient
    ev, _ = find_peaks(Z[:, 3], prominence=0.1, distance=int(round(5 / dt)))  # ovulation = the LH surge peak
    X = np.column_stack([Z[:, 1], Z[:, 3], Z[:, 4]]); X = X / X.std(axis=0)   # hormone state (E2, LH, P4), each in its own sd
    return regularity(X, ev, dt=dt), float(np.mean(np.diff(ev)) * dt)


def r5():
    pid = "P11-5"; d = D[pid]
    r, T = _mens(3400.0, 0.2, 5)
    crr, null = r["cv_arc"], r["cv_clock"]; check = r["ci95"][1] < 0
    out = outcome(crr=crr, null=null, domain=None, check=check)
    sens = [(s_, _mens(2200.0, s_, 6)[0]) for s_ in (0.1, 0.3)]
    return make_row(d[2], d[3] + f"; model (reduced, in the Keener-Sneyd pool form): follicle F under FSH suppressed by progesterone, estradiol E lagging F by 1 day, an LH reserve released by E (Hill 20), serum LH, ovulation at rate 20 H(LH) F with a Hill-8 LH threshold, corpus-luteum progesterone decaying over 8 days; OU noise (sd 0.2, correlation 2 days) on follicular growth; RK4 dt 0.01 day, 3400 days, first 200 discarded; own events = LH surge peaks; {r['n']} cycles, mean length {T:.3f} model days, seed 5",
                    source=_src(pid), Q=d[5] + " (computed as: arc of the hormone state (E2, LH, P4), each scaled by its own sd, between consecutive LH surge peaks, against the cycle length; paired bootstrap n_boot 2000 seed 0, CI excluding 0 below)",
                    ingredient=d[4] + " (regularity on the three-hormone state, segment_end inclusive)",
                    null=d[6], domain=d[7],
                    numbers=f"CV(arc per cycle) {crr:.4f}, CV(cycle length) {null:.4f}, difference {r['diff']:+.4f}, 95 % CI {_ci(r)}; amplitude control CV(peak-to-trough) {r['cv_amp']:.4f} (CI of CV(arc) - CV(amp) [{r['ci95_amp'][0]:+.4f}, {r['ci95_amp'][1]:+.4f}]); noise sensitivity: " + "; ".join(f"sd {s_}: CV(arc) {x['cv_arc']:.4f}, CV(clock) {x['cv_clock']:.4f}, CI {_ci(x)}" for s_, x in sens),
                    tg=f"CV(arc) {crr:.4f} vs null CV(cycle length) {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited",
                    tc=f"CV(arc) - CV(cycle) CI {_ci(r)} lies below 0: {_w(check, 'holds', 'fails')} {_held(check)}",
                    out=out,
                    reading=f"noise on follicular growth moves the day of the surge {_w(r['cv_amp'] < null, 'more', 'less')} than it changes the size of the hormonal excursion (CV {null:.4f} against {r['cv_amp']:.4f}), and in this model the hormone arc per cycle is {_w(crr < null, 'more', 'less')} regular than the cycle length ({crr:.4f} against {null:.4f}); the amplitude control is {_w(r['cv_amp'] < crr, 'more regular than the arc', 'less regular than the arc')} ({r['cv_amp']:.4f}; CI of the difference [{r['ci95_amp'][0]:+.4f}, {r['ci95_amp'][1]:+.4f}]), so the arc {_w(r['ci95_amp'][0] > 0, 'does worse than the size of the excursion alone', _w(r['ci95_amp'][1] < 0, 'beats the size of the excursion alone', 'ties the size of the excursion alone'))} (H-L5's control (i) in CRR.md, not part of the declared Q)",
                    weakness=f"DEVIATION: the published Keener-style / Selgrade models have 10 or more variables; this is a five-variable reduction written for this row (same mechanisms: FSH suppression by progesterone, estradiol-triggered LH release from a reserve pool, LH-triggered ovulation, luteal decay), with rates chosen so that it oscillates, and its mean cycle is {T:.1f} model days rather than 28 (CVs are scale-free). Noise enters the growth rate, not the state, so the arc converges as dt shrinks",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P11: physiology (Predictions70/DECLARATION.md; declared.py at 8397478)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
