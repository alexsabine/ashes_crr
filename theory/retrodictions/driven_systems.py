"""CRR retrodiction battery on engineered, geophysical and driven-dissipative model systems
(owner request 2026-09-17, prompt-log entry 42).

Nine model systems in five classes, none of which any earlier battery covered: (g) geophysical
threshold systems (a spring-slider fault with strength or loading variability; the Olami-Feder-
Christensen earthquake automaton; Kramers escape in a double well, unforced and periodically
forced, as a tipping/Dansgaard-Oeschger prototype); (m) materials with memory (Paris-law fatigue
under variable-amplitude loading; the Preisach hysteresis ensemble, the first system in any
battery where the influence of every settled occasion on the final state is MEASURED, so the
occasion-weight law T5 can be scored); (e) engineered loops (AIMD congestion control with
buffer-limited and random loss; the M/M/1 queue's busy periods as natural time); (c) chemical
(the Oregonator relaxation oscillator under slowly drifting recovery time or stoichiometry); (t) thermodynamic
(a two-parameter harmonic-trap protocol in linear response: does the surplus S order the excess
work? the roadmap's open item, docs/ROADMAP_2026-Q4.md section 2).

Grades under the issue-#21 rules (SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN; rule 2 on
chosen observables, rule 4 on symmetric members); BORROWED and FLOW per row; H-L5 class where the
system has its own events, with the segmentation named where the event is a jump (prompt-log
entry 41: a jump located at the event is the cut, not arc). Model systems only; no dataset
opened (R2). Deterministic (seeded). Run:
uv run python theory/retrodictions/driven_systems.py
"""
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

from crr.instrument.core import arc_length, regularity

ROWS = []


def row(cls, system, clause, borrowed, flow, derivation, known, verdict, grade, l5=None, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, flow=flow, derivation=derivation,
                     known=known, verdict=verdict, grade=grade, l5=l5, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


def l5_class(x, events, dt=1.0, segment_end="inclusive"):
    """H-L5 on a model trace with its own events: (label, cv_arc, cv_clock). |diff| < 1e-3 is a tie (instrument resolution)."""
    r = regularity(np.asarray(x, float), np.asarray(events, int), sigma=1.0, dt=dt, n_boot=200, seed=0, segment_end=segment_end)
    if abs(r["cv_arc"] - r["cv_clock"]) < 1e-3: lab = "tie"
    else: lab = "arc-regular" if r["cv_arc"] < r["cv_clock"] else "clock-regular"
    return lab, r["cv_arc"], r["cv_clock"]


def r2(y, x):
    """R^2 of y on a linear fit in x."""
    x = np.asarray(x, float); y = np.asarray(y, float); A = np.c_[x, np.ones_like(x)]
    coef, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ coef
    return float(1 - res.var() / y.var())


# ================================================================ (g) geophysical threshold systems
def g_spring_slider():
    """Spring-slider fault, stress carrier tau(t) = k (v t - x): rises during stick, drops at slip (a jump, so the
    segmentation is exclusive: the drop is the event). Variant A: constant loading, per-event strength jitter.
    Variant B: fixed strength, Ornstein-Uhlenbeck loading rate. Variant C: both."""
    rng = np.random.default_rng(1); dt = 0.001; k = 1.0; Fd = 0.5; n_ev = 60
    def run(strength_cv, rate_cv):
        Fs = 1.0 * (1 + strength_cv * rng.standard_normal(n_ev)); v = 1.0; ou = 0.0
        tau = Fd; trace = []; events = []; i = 0; t = 0
        while i < n_ev and t < 4000000:
            ou += dt * (-0.02 * ou) + rate_cv * math.sqrt(2 * 0.02 * dt) * rng.standard_normal()
            v = max(1.0 + ou, 0.05); tau += k * v * dt; trace.append(tau); t += 1
            if tau >= Fs[i]:
                events.append(t); tau = Fd; i += 1
        return np.array(trace), np.array(events)
    out = []
    for name, sc, rc in (("A strength jitter", 0.10, 0.0), ("B loading jitter", 0.0, 0.10), ("C both", 0.10, 0.10)):
        tr, ev = run(sc, rc); lab, ca, cc = l5_class(tr, ev[3:], dt, segment_end="exclusive"); out.append((name, lab, ca, cc, len(ev)))
    def reading(o): return o[1] if (o[1] == "tie" or abs(o[2] - o[3]) >= 0.01) else f"{o[1]} by {abs(o[2] - o[3]):.3f}, below the 0.01 this battery treats as a reading"
    row("g", "Spring-slider fault (stick-slip), stress carrier: strength jitter vs loading-rate jitter vs both", "D5 (slip = own event), A3 (the drop is the cut, exclusive segmentation), H-L5 (the L5x question)",
        "single-degree-of-freedom slider with static/dynamic strength; Ornstein-Uhlenbeck loading", "the loading rate and the strength sequence (fault-supplied)",
        "; ".join(f"{name}: {n} slips, CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, lab, ca, cc, n in out),
        "the recurrence of laboratory stick-slip depends on loading rate and on strength evolution (rate-and-state friction); which varies more is an empirical property of the fault",
        f"the class is set by which of the two the fault varies: with strength jitter arc and clock are the same variable ({reading(out[0])}), with loading jitter the arc is the regular one ({reading(out[1])}), with both: {reading(out[2])}; the framework names the two classes and does not say which a fault belongs to (rule 2): that is the L5x study",
        "OPEN", None, "the p4581 result in CLAUDE.md section 0 (arc-regular at 11/12 levels) would say the lab fault is in class B; the model cannot confirm or deny it, and the study that can is gated but not run")


def g_ofc_earthquakes():
    """Olami-Feder-Christensen automaton, L x L, conservation alpha, open boundaries, synchronous toppling."""
    rng = np.random.default_rng(2); L = 32; alpha = 0.2; z = rng.random((L, L)) * 0.9
    n_av = 30000; sizes = np.empty(n_av, int); mean_stress = np.empty(n_av); drive = np.empty(n_av)
    T = 0.0
    for a in range(n_av):
        gap = 1.0 - z.max(); z += gap; T += gap; drive[a] = T
        s = 0
        while True:
            top = z >= 1.0
            if not top.any(): break
            s += int(top.sum()); load = alpha * np.where(top, z, 0.0); z[top] = 0.0
            z[1:, :] += load[:-1, :]; z[:-1, :] += load[1:, :]; z[:, 1:] += load[:, :-1]; z[:, :-1] += load[:, 1:]
        sizes[a] = s; mean_stress[a] = z.mean()
    sizes_t = sizes[10000:]; ms = mean_stress[10000:]; dr = drive[10000:]
    # size distribution slope on 1..64
    edges = np.array([1, 2, 4, 8, 16, 32, 64]); cnt = np.array([((sizes_t >= lo) & (sizes_t < hi)).sum() for lo, hi in zip(edges[:-1], edges[1:])], float)
    dens = cnt / np.diff(edges); mids = np.sqrt(edges[:-1] * edges[1:]); ok = dens > 0
    slope = float(np.polyfit(np.log(mids[ok]), np.log(dens[ok]), 1)[0])
    # H-L5 on large events: carrier = mean stress sampled per avalanche (natural drive time = the loading, uniform), events = avalanches >= 64 sites
    big = np.where(sizes_t >= 64)[0]
    lab, ca, cc = l5_class(ms, big[:200], 1.0, segment_end="exclusive") if len(big) > 8 else ("n/a", float("nan"), float("nan"))
    frac_big = len(big) / len(sizes_t)
    row("g", "Olami-Feder-Christensen earthquake automaton (L = 32, alpha = 0.2): avalanche sizes and the recurrence of large events", "A1' (unit = one site), D5 (large avalanche = own event), H-L5; no clause on exponents",
        "OFC 1992 spring-block automaton; self-organised criticality", "the uniform loading (drive) and the conservation parameter alpha",
        f"{len(sizes_t)} avalanches after transient; size-distribution log-log slope on 1..64: {slope:.2f}; fraction of avalanches >= 64 sites: {frac_big:.4f}; large events ({len(big)}), carrier = mean stress, events counted in avalanches: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}",
        "OFC gives a Gutenberg-Richter-like size distribution whose exponent depends on alpha; large events recur quasi-periodically only near conservation",
        "the exponent is the automaton's; the recurrence class of large events is assigned by the instrument, and no clause predicts it",
        "DESCR", (lab, ca, cc), "class assignment on a model at one alpha and one L; the exponent's alpha-dependence is not reached by any clause")


def g_kramers_double_well():
    """Overdamped particle in x^4/4 - x^2/2 with noise: well-to-well transitions are the events. Unforced (Kramers)
    and periodically forced (stochastic-resonance regime, the Dansgaard-Oeschger prototype)."""
    def run(A, period, seed, dt=0.01, n=2_000_000, sig=0.4):
        rng = np.random.default_rng(seed); x = -1.0; xs = np.empty(n); side = -1; ev = []
        w = 2 * math.pi / period if period else 0.0; noise = rng.standard_normal(n) * sig * math.sqrt(dt)
        for k in range(n):
            x += dt * (x - x ** 3 + A * math.cos(w * k * dt)) + noise[k]; xs[k] = x
            if side < 0 and x > 0.5: side = 1; ev.append(k)
            elif side > 0 and x < -0.5: side = -1; ev.append(k)
        return xs, np.array(ev)
    out = []
    for name, A, per in (("unforced", 0.0, 0.0), ("forced A = 0.20, period 200", 0.20, 200.0)):
        xs, ev = run(A, per, 3); lab, ca, cc = l5_class(xs, ev[2:], 0.01); tt = np.diff(ev[2:]) * 0.01
        out.append((name, len(ev), lab, ca, cc, float(np.mean(tt)), float(np.std(tt, ddof=1) / np.mean(tt))))
    row("g", "Kramers escape in a double well: well-to-well transitions, unforced and periodically forced (tipping / Dansgaard-Oeschger prototype)", "D5 (transition = own event), D2 (arc on the state carrier), H-L5",
        "Kramers rate theory; stochastic resonance", "the noise (D) and the forcing (A, period)",
        "; ".join(f"{name}: {n} transitions, mean residence {mt:.1f} (CV {cvt:.2f}), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, n, lab, ca, cc, mt, cvt in out),
        "unforced escapes are Poisson (residence-time CV near 1); with weak periodic forcing near the matching noise level the transitions synchronise to the forcing (stochastic resonance)",
        f"unforced: {out[0][2]} — in the fluctuation-driven regime the arc between transitions is the noise's total variation, which grows with elapsed time, so arc and clock carry the same variability (prompt-log entry 41's finding, here on a system with no threshold); forced: {out[1][2]} (residence CV {out[1][6]:.2f} against {out[0][6]:.2f} unforced); no clause predicts either",
        "DESCR", None, "the arc of a noise-dominated 1-D path is a clock: H-L5 can discriminate only where the surplus is small against the chord, which is a limit of the instrument to write into every L5-type prereg")


# ================================================================ (m) materials with memory
def m_paris_fatigue():
    """Paris law da/dN = Cp (dK)^m, dK = dsigma Y sqrt(pi a), under blocks of random amplitude. Separable ODE: the final
    crack length is a function of the Miner sum sum_i dsigma_i^m n_i alone. Compare the Fisher-arc-like sum (m = 1),
    the Miner sum, and the endpoint (last block's amplitude) as predictors across random sequences."""
    rng = np.random.default_rng(4); m = 3.0; Cp = 1e-11; Y = 1.0; a0 = 1e-3; n_blocks = 12; n_cyc = 2000; runs = 200
    def crack(seq):
        a = a0
        for ds in seq:
            for _ in range(20):                                              # 20 sub-steps per block, explicit Euler in N
                dK = ds * Y * math.sqrt(math.pi * a); a += Cp * dK ** m * (n_cyc / 20)
        return a
    af, miner, arc1, endpoint = [], [], [], []
    for _ in range(runs):
        seq = rng.uniform(60, 140, n_blocks); af.append(crack(seq)); miner.append(np.sum(seq ** m) * n_cyc); arc1.append(np.sum(seq) * n_cyc); endpoint.append(seq[-1])
    af = np.log(np.array(af) / a0)
    R = dict(miner=r2(af, np.log(miner)), arc=r2(af, np.log(arc1)), endpoint=r2(af, np.log(endpoint)))
    row("m", "Paris-law fatigue crack growth under variable-amplitude loading: does damage track the path, and which path functional?", "H-T1 class (path vs endpoint) read onto a wear system; D2 (the Fisher arc with the identity metric is sum |dsigma| n)",
        "Paris 1963 law; Palmgren-Miner linear damage", "the material constants Cp, m and the load sequence",
        f"{runs} random 12-block sequences: R^2 of log crack growth on log Miner sum (exponent m = {m:g}) = {R['miner']:.3f}; on the arc-like sum (exponent 1) = {R['arc']:.3f}; on the endpoint (last amplitude) = {R['endpoint']:.3f}",
        "under Paris without load interaction the damage is a function of the Miner sum alone (separable ODE); the endpoint carries nothing",
        f"path-dependent by construction (the S-H2 class), so 'path beats endpoint' holds ({R['miner']:.3f} and {R['arc']:.3f} against {R['endpoint']:.3f}); but the path functional the material obeys carries the exponent m, and the Fisher arc (m = 1) is the wrong functional by {R['miner'] - R['arc']:.3f} in R^2: the domain supplies the exponent, CRR supplies only 'a path integral'",
        "DESCR", None, "H-T1 names path-dependence; it does not say which path functional, and here the correct one is not the Fisher arc")


def m_preisach_hysteresis():
    """Preisach ensemble: hysterons with switching thresholds (alpha up, beta down) uniform on the triangle
    -1 <= beta < alpha <= 1. Input: n excursions from 0 up to a_i and back to 0 (C* = 0, S_i = C_i = 2 a_i in input units).
    The influence of occasion i on the final output is MEASURED: remove occasion i and re-run. The occasion-weight law
    (spec T5 / v3.1 P2 at beta = 1): log(pi_i / pi_j) = S_i - S_j. Preisach's wiping-out property: only the running
    maximum survives, so all but the largest excursion have zero influence."""
    rng = np.random.default_rng(5); n_h = 4000
    pts = rng.uniform(-1, 1, (n_h * 3, 2)); pts = pts[pts[:, 1] < pts[:, 0]][:n_h]; alpha_h, beta_h = pts[:, 0], pts[:, 1]
    def output(excursions):
        state = np.full(n_h, -1.0)
        for a in excursions:
            for u in (a, 0.0):                                               # up to a, back to 0
                state = np.where(u >= alpha_h, 1.0, np.where(u <= beta_h, -1.0, state))
        return float(state.mean())
    amps = np.array([0.30, 0.55, 0.80, 0.45, 0.65, 0.20]); S = 2 * amps
    full = output(amps); infl = np.array([abs(full - output(np.delete(amps, i))) for i in range(len(amps))])
    order = np.argsort(-S); top, second = order[0], order[1]
    law_pred = S[top] - S[second]; measured = (math.log(infl[top] / infl[second]) if infl[second] > 0 else float("inf"))
    n_zero = int((infl == 0).sum()); mono = float(np.corrcoef(S, infl)[0, 1])
    row("m", "Preisach hysteresis ensemble: measured influence of each settled excursion on the final state vs the occasion-weight law", "spec T5 / v3.1 P2 (pi_m proportional to exp(beta S_m), read at beta = 1), A6 (regeneration from settled occasions), D4 (S of a closed excursion = its arc)",
        "Preisach 1935 model; Mayergoyz wiping-out and congruency properties", "the input sequence (the excursion amplitudes) and the hysteron density",
        f"6 excursions with S = {', '.join(f'{s:.2f}' for s in S)}; measured influence (remove-one change in output) = {', '.join(f'{v:.4f}' for v in infl)}; {n_zero} of 6 occasions have exactly zero influence; correlation(S, influence) = {mono:.3f}; "
        f"law's log-odds between the two largest occasions = S_i - S_j = {law_pred:.2f}, measured log-odds = {'infinite (zero influence)' if measured == float('inf') else f'{measured:.2f}'}",
        "wiping-out: an excursion is erased from memory by any later larger excursion; the final state depends on the running maximum only",
        "the influence of a settled occasion is 1 or 0 by the wiping-out rule, not exp(S): the log-odds law gives a finite number where the system gives an infinite one, and five of six occasions with positive surplus have no influence at all; T5 FAILS on the first system where influence is measured rather than imposed",
        "FAILS", None, "rule 4 / class dependence: a memory with return-point (wiping-out) structure is outside the law's MaxEnt form; the spec's own class restriction (A4, 'depth one says OPEN') does not cover it because Preisach has depth greater than one and still contradicts the weights")


# ================================================================ (e) engineered loops
def e_aimd_congestion():
    """AIMD congestion window: +1 per round trip, halved at a loss. Buffer-limited loss (at cwnd = B) with jittered RTT
    is arc-regular by construction (the halving fixes the chord and the arc). Random per-packet loss makes the window at
    loss random. The loss is a jump in the carrier: exclusive segmentation."""
    rng = np.random.default_rng(6); B = 64.0; n_ev = 80
    def run(random_loss_p, rtt_cv):
        w = B / 2; t = 0.0; trace = []; times = []; events = []
        while len(events) < n_ev:
            rtt = 1.0 * (1 + rtt_cv * rng.standard_normal()); rtt = max(rtt, 0.2)
            w += 1.0; t += rtt; trace.append(w); times.append(t)
            lost = (w >= B) if random_loss_p == 0 else (rng.random() < 1 - (1 - random_loss_p) ** w)
            if lost: events.append(len(trace)); w = w / 2
        trace = np.array(trace); events = np.array(events)
        # clock time of an occasion = accumulated RTTs between losses; regularity() uses index * dt, so pass a resampled trace on a uniform grid
        times = np.array(times); grid = np.arange(0, times[-1], 0.05); tr_u = np.interp(grid, times, trace); ev_u = np.searchsorted(grid, times[events - 1])
        return tr_u, ev_u
    out = []
    for name, p, rc in (("buffer-limited, RTT CV 0.15", 0.0, 0.15), ("random loss p = 0.002, RTT CV 0.15", 0.002, 0.15)):
        tr, ev = run(p, rc); lab, ca, cc = l5_class(tr, ev[3:], 0.05, segment_end="exclusive"); out.append((name, lab, ca, cc))
    row("e", "AIMD congestion control (TCP-like): loss events with buffer-limited vs random loss under round-trip-time jitter", "D5 (loss = own event), A3 (the halving is the cut, exclusive segmentation), H-L5",
        "additive-increase multiplicative-decrease (Chiu-Jain 1989); fluid model of TCP", "the round-trip time sequence and the loss process (network-supplied)",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, lab, ca, cc in out),
        "with a fixed buffer the window sawtooth has a fixed amplitude B/2 and a period set by the RTT; with random loss the amplitude is random",
        f"arc-regular in both variants ({out[0][1]}, {out[1][1]}) and by construction: the window rises by one per round trip, so the arc of a cycle is its round-trip count and only the RTT jitter separates clock from arc, whatever the loss process (the S-G2 mechanism in an engineered loop); the framework names the class and the protocol supplies it",
        "DESCR", None, "the first engineered system in the batteries that is arc-regular by design rather than by physics; nothing about TCP is derived")


def e_mm1_busy_periods():
    """M/M/1 queue, lambda = 0.5, mu = 1: busy periods as occasions; natural time = customers served. On a counting carrier
    (queue length) with the identity metric the Fisher arc of a busy period is 2 N - 1 exactly: natural time IS the arc."""
    rng = np.random.default_rng(7); lam, mu = 0.5, 1.0; n_bp = 3000
    Ns, Ts = [], []
    for _ in range(n_bp):
        q = 1; served = 0; t = 0.0
        while q > 0:
            r = lam + mu; t += rng.exponential(1 / r)
            if rng.random() < lam / r: q += 1
            else: q -= 1; served += 1
        Ns.append(served); Ts.append(t)
    Ns = np.array(Ns, float); Ts = np.array(Ts)
    arc = 2 * Ns - 1
    row("e", "M/M/1 queue busy periods: natural time (customers served) against clock duration", "O3 (natural time gives the unit for point processes), D2 (arc on the count carrier), A4 (Markov: depth one)",
        "M/M/1 busy-period theory (Borel-Tanner); memoryless service and arrivals", "the arrival and service rates",
        f"{n_bp} busy periods at rho = {lam / mu:g}: mean customers served {Ns.mean():.2f} (theory 1/(1 - rho) = {1 / (1 - lam / mu):.2f}), mean duration {Ts.mean():.2f} (theory 1/(mu - lambda) = {1 / (mu - lam):.2f}); CV(natural time) {cv(Ns):.3f}, CV(arc = 2N - 1) {cv(arc):.3f}, CV(duration) {cv(Ts):.3f}; correlation(arc, duration) {np.corrcoef(arc, Ts)[0, 1]:.3f}",
        "busy-period length and customers served are both heavy-tailed at rho near 1 and are functions of the same random walk",
        "the arc of a counting carrier is the event count: 'natural time' and 'coherence' are one statistic here (a definition), and the queue is Markov so nothing settled beyond the present length has any effect (A4)",
        "DESCR", None, "the arc adds nothing to the count; the count's regularity against the clock is the random walk's, not CRR's")


# ================================================================ (c) chemical
def c_oregonator():
    """Tyson's two-variable Oregonator (eps = 0.04, q = 8e-4) under two registered slow deterministic drifts (sums of
    incommensurate sines, +-40 %): (i) the slow variable's time scale tau_z (recovery time), (ii) the stoichiometric
    factor f. Carrier: log10 x; own event: the excitation (x crossing 0.1 upward)."""
    eps, q = 0.04, 8e-4
    def drift(t): return 1.0 + 0.40 * (math.sin(0.021 * t) + 0.6 * math.sin(0.0137 * t + 1.0) + 0.4 * math.sin(0.0071 * t + 2.0)) / 2.0
    def run(which):
        def rhs(t, y):
            x, z = y; f = 1.0 * (drift(t) if which == "f" else 1.0); tz = drift(t) if which == "tau_z" else 1.0
            return [(x * (1 - x) - f * z * (x - q) / (x + q)) / eps, (x - z) / tz]
        t = np.linspace(0, 3000, 300001); sol = solve_ivp(rhs, (0, 3000), [0.5, 0.1], t_eval=t, method="Radau", rtol=1e-7, atol=1e-10)
        lx = np.log10(np.clip(sol.y[0][30000:], 1e-9, None)); dt = t[1] - t[0]
        ev = np.where((lx[:-1] < -1.0) & (lx[1:] >= -1.0))[0]
        lab, ca, cc = l5_class(lx, ev[2:], dt); periods = np.diff(ev[2:]) * dt
        return len(ev), float(periods.mean()), cv(periods), lab, ca, cc
    out = {w: run(w) for w in ("tau_z", "f")}
    def reading(o): return o[3] if abs(o[4] - o[5]) >= 0.01 else f"{o[3]} by {abs(o[4] - o[5]):.3f}, below the 0.01 this battery treats as a reading"
    row("c", "Oregonator (Belousov-Zhabotinsky) relaxation oscillator under slowly drifting recovery time or stoichiometry: cycle class", "D5 (the excitation = own event), D2 on log10 x, H-L5",
        "Field-Koros-Noyes mechanism; Tyson 1985 two-variable reduction", "the rate constants and the registered drift (experimenter-supplied)",
        "; ".join(f"drift in {w}: {n} excitations, period mean {pm:.2f} (CV {pc:.3f}), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for w, (n, pm, pc, lab, ca, cc) in out.items()),
        "the BZ period is set by the slow variable's recovery; the excursion shape is nearly fixed by the fast subsystem; the stoichiometric factor moves the period little inside the oscillatory range",
        f"recovery-time drift: {reading(out['tau_z'])} (the fast excursion is fixed and the recovery time varies, the S-G2 mechanism); stoichiometry drift: {reading(out['f'])}; the drift, not the framework, decides the class",
        "OPEN", (out["tau_z"][3], out["tau_z"][4], out["tau_z"][5]), "class assignment on a model under two registered drifts; the Hopf-side behaviour of the Oregonator is covered by the Hopf rows of the earlier batteries")


# ================================================================ (t) thermodynamic
def t_two_parameter_trap():
    """Overdamped particle in a harmonic trap with control lambda = (x0, k) (centre and stiffness), kT = 1, friction gamma = 1.
    The Boltzmann family is N(x0, 1/k): its Fisher metric is g = diag(k/kT, 1/(2k^2)), i.e. (dx0^2 + 2 dsigma^2)/sigma^2
    with sigma^2 = kT/k: a hyperbolic half-plane in (x0/sqrt2, sigma), whose geodesics are semicircles centred on sigma = 0
    (closed form). Linear response (Sivak-Crooks): W_ex = int dlambda/dt^T zeta dlambda/dt dt with the exact trap friction
    tensor zeta = diag(gamma, gamma kT/(4 k^3)) (conjugate-force autocorrelation times gamma/k and gamma/(2k)); zeta is
    NOT a scalar multiple of g, so the minimum-dissipation geodesic is zeta's, not g's. Three protocols with the same
    endpoints and duration: the g-geodesic at constant Fisher speed (S = 0), a detour at constant Fisher speed (S > 0),
    the g-geodesic traversed at a bursty speed (S = 0). Does S order W_ex?"""
    kT = 1.0; gamma = 1.0
    def g(lam): return np.diag([lam[1] / kT, 1.0 / (2 * lam[1] ** 2)])
    def zeta(lam): return np.diag([gamma, gamma * kT / (4 * lam[1] ** 3)])
    def length(path, metric):
        return float(sum(math.sqrt((b - a) @ metric((a + b) / 2) @ (b - a)) for a, b in zip(path[:-1], path[1:])))
    def excess_work(path, tau):
        dt = tau / (len(path) - 1)
        return float(sum(((b - a) / dt) @ zeta((a + b) / 2) @ ((b - a) / dt) * dt for a, b in zip(path[:-1], path[1:])))
    A = np.array([0.0, 1.0]); B = np.array([2.0, 4.0]); n = 2000; tau = 50.0
    # closed-form g-geodesic: half-plane coordinates (u, sigma) = (x0 / sqrt 2, sqrt(kT / k)); semicircle through both endpoints
    to_hp = lambda lam: np.array([lam[0] / math.sqrt(2), math.sqrt(kT / lam[1])]); from_hp = lambda u, sg: np.c_[u * math.sqrt(2), kT / sg ** 2]
    a, b = to_hp(A), to_hp(B); c = ((b[0] ** 2 + b[1] ** 2) - (a[0] ** 2 + a[1] ** 2)) / (2 * (b[0] - a[0])); R = math.hypot(a[0] - c, a[1])
    th = np.linspace(math.atan2(a[1], a[0] - c), math.atan2(b[1], b[0] - c), n); geo = from_hp(c + R * np.cos(th), R * np.sin(th))
    Cstar = math.sqrt(2) * math.acosh(1 + ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) / (2 * a[1] * b[1]))       # hyperbolic distance (closed form)
    def const_speed(path):
        seg = np.array([math.sqrt((q - p_) @ g((p_ + q) / 2) @ (q - p_)) for p_, q in zip(path[:-1], path[1:])]); cum = np.r_[0, np.cumsum(seg)]; u = cum / cum[-1]
        tgt = np.linspace(0, 1, len(path)); return np.c_[np.interp(tgt, u, path[:, 0]), np.interp(tgt, u, path[:, 1])]
    geo = const_speed(geo); sgrid = np.linspace(0, 1, n)
    detour = const_speed(np.c_[A[0] + sgrid * (B[0] - A[0]) + 1.2 * np.sin(math.pi * sgrid), A[1] + sgrid * (B[1] - A[1]) - 1.5 * np.sin(math.pi * sgrid)])
    warp = np.where(sgrid < 0.3, 0.9 * sgrid / 0.3, 0.9 + 0.1 * (sgrid - 0.3) / 0.7)                         # 90 % of the length in 30 % of the time
    bursty = np.c_[np.interp(warp, sgrid, geo[:, 0]), np.interp(warp, sgrid, geo[:, 1])]
    res = [(name, length(p_, g), length(p_, g) - Cstar, length(p_, zeta), excess_work(p_, tau)) for name, p_ in (("g-geodesic, constant speed", geo), ("detour, constant speed", detour), ("g-geodesic, bursty speed", bursty))]
    bound_ok = all(W >= Lz ** 2 / tau * (1 - 1e-6) for _, _, _, Lz, W in res)
    Wg, Wd, Wb = res[0][4], res[1][4], res[2][4]; ordered_by_S = (res[1][2] > res[2][2]) and (Wd > Wb)
    row("t", "Two-parameter harmonic-trap protocol (centre and stiffness) in linear response: does the surplus S order the excess work?", "D2-D4 (C, C*, S on the control manifold with the Fisher metric), P1; the roadmap's open item (section 2)",
        "Sivak-Crooks 2012 thermodynamic length (W_ex >= L_zeta^2 / tau); Crooks 2007 Fisher metric of the Boltzmann family; the exact harmonic-trap friction tensor", "the protocol speed and the friction tensor (system-supplied)",
        "; ".join(f"{name}: C = {C:.3f}, S = {S:.3f}, L_zeta = {Lz:.3f}, W_ex = {W:.4f}" for name, C, S, Lz, W in res) + f"; C* = {Cstar:.3f} (closed form; numerical geodesic length {res[0][1]:.3f}); bound W_ex >= L_zeta^2/tau holds on all three: {bound_ok}; ordering by S alone: {'yes' if ordered_by_S else 'no'} (the bursty g-geodesic has S = 0 and W_ex {Wb / Wg:.2f}x the constant-speed g-geodesic's; the detour has S > 0 and W_ex {Wd / Wg:.2f}x)",
        "minimum-dissipation protocols are constant-speed geodesics of the friction metric zeta; W_ex >= L_zeta^2 / tau by Cauchy-Schwarz",
        "the constant-speed geodesic is optimal (inherited from Sivak-Crooks, CONSIST on paper as the earlier batteries said); S orders the excess work only among constant-speed protocols: a zero-surplus protocol traversed at uneven speed dissipates more than a positive-surplus one at constant speed, so S is not a dissipation ordering, the speed profile in the friction metric is; and here the friction metric is not the Fisher metric up to a scalar, so even the geodesic CRR names is not the optimal one",
        "DESCR", None, "answers the roadmap's 2-D question negatively on the model: to order dissipation one needs the full speed profile in zeta, which is the thermodynamic-length result, not a CRR quantity")


BATTERY = [g_spring_slider, g_ofc_earthquakes, g_kramers_double_well, m_paris_fatigue, m_preisach_hysteresis,
           e_aimd_congestion, e_mm1_busy_periods, c_oregonator, t_two_parameter_trap]

CLASSES = {"g": "geophysical / threshold", "m": "materials with memory", "e": "engineered loops", "c": "chemical", "t": "thermodynamic"}


def main():
    for f in BATTERY: f()
    print(f"CRR retrodiction battery on engineered, geophysical and driven-dissipative systems — {len(ROWS)} model systems, {len(CLASSES)} classes. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}\n     FLOW:       {r['flow']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     H-L5 class: {r['l5'][0]} (CV_arc {r['l5'][1]:.3f}, CV_clock {r['l5'][2]:.3f})" if r['l5'] else "")
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'class':32s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rs = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:28s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':32s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print("\nH-L5 class map (model systems with their own events):")
    for r in ROWS:
        if r["l5"]: print(f"  {r['l5'][0]:44s} {r['system']}")
    print(f"\nrows where the coherence integral's velocity is system-supplied (FLOW != none): {sum('none' not in r['flow'] for r in ROWS)}/{len(ROWS)}")
    print("Rows where a CRR clause reaches a result the domain did not already have: " + str(sum(r["grade"] in ("SHARP",) for r in ROWS)) + f" of {len(ROWS)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
