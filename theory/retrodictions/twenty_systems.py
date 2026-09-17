"""CRR retrodiction battery: twenty model systems in twenty domains none of the eight earlier batteries touched
(owner request 2026-09-18, prompt-log entry 52).

(nuc) radioactive decay chain; (opt) passively Q-switched laser; (geo) geyser eruptions; (clim) ENSO delayed
oscillator; (clim) Paillard three-state ice-age model under synthetic orbital forcing; (plasma) tokamak sawtooth
crashes; (sleep) Borbely two-process model; (micro) bacterial run-and-tumble; (neuro) hippocampal theta phase
precession (the first H-CUT row); (eco) Rosenzweig-MacArthur predator-prey cycles; (ops) the bullwhip effect with
moving-average forecasts (a windowed memory); (mat) fibre-bundle cascading failure; (rl) TD(lambda) eligibility
traces; (mat) the Kovacs memory effect in glasses; (games) Elo ratings against the Kalman gain; (acoust) cricket
chirps and Dolbear's law; (learn) the spacing effect with ACT-R's power-law decay; (econ) the cobweb model;
(surf) RHEED growth oscillations as natural time; (fire) fuel-threshold fire regimes.

Grades under the issue-#21 rules (SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN; rule 2 on chosen observables,
rule 3 on definitions, rule 4 on symmetric members); BORROWED and FLOW per row; H-L5 class where the system has its
own events, exclusive segmentation where the event is a reset (prompt-log entry 41); every class or regime label is
computed from its number; a margin below 0.01 is not a reading; on noisy carriers the arc is the sampled arc at the
stated step (prompt-log entry 48). Model systems only; no dataset opened (R2). Deterministic (seeded). Run:
uv run python theory/retrodictions/twenty_systems.py
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
    r = regularity(np.asarray(x, float), np.asarray(events, int), sigma=1.0, dt=dt, n_boot=200, seed=0, segment_end=segment_end)
    if abs(r["cv_arc"] - r["cv_clock"]) < 1e-3: lab = "tie"
    else: lab = "arc-regular" if r["cv_arc"] < r["cv_clock"] else "clock-regular"
    return lab, r["cv_arc"], r["cv_clock"]


def lab_of(arcs, times):
    d = cv(arcs) - cv(times)
    return "tie" if abs(d) < 1e-3 else ("arc-regular" if d < 0 else "clock-regular")


def reading(lab, ca, cc):
    return lab if (lab == "tie" or abs(ca - cc) >= 0.01) else f"{lab} by {abs(ca - cc):.3f}, below the 0.01 this battery treats as a reading"


def r2(y, X):
    X = np.atleast_2d(np.asarray(X, float)); X = X.T if X.shape[0] < X.shape[1] else X
    A = np.c_[X, np.ones(len(X))]; y = np.asarray(y, float)
    coef, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ coef
    return float(1 - res.var() / y.var())


def threshold_process(rng, rate_cv, thr_cv, reset_cv=0.0, dt=0.01, n_ev=80, ou_rate=0.05):
    """Generic integrate-to-threshold with OU rate noise, per-event threshold jitter and a variable reset level.
    Returns (trace, event indices). The reset is the cut (exclusive segmentation)."""
    ou = 0.0; x = 0.0; trace = []; events = []; thr = 1.0 * (1 + thr_cv * rng.standard_normal(n_ev)); i = 0; t = 0
    while i < n_ev:
        ou += dt * (-ou_rate * ou) + rate_cv * math.sqrt(2 * ou_rate * dt) * rng.standard_normal(); u = max(1.0 + ou, 0.05)
        x += u * dt; trace.append(x); t += 1
        if x >= thr[i]: events.append(t); x = max(0.0, reset_cv * abs(rng.standard_normal())) * thr[i]; i += 1
    return np.array(trace), np.array(events)


# ================================================================ 1 (nuc) radioactive decay chain
def nuc_decay_chain():
    lA, lB = 0.1, 0.5; t = np.linspace(0, 60, 6001)
    NB = lA / (lB - lA) * (np.exp(-lA * t) - np.exp(-lB * t)); k = int(np.argmax(NB)); t_peak = float(t[k]); t_star = math.log(lB / lA) / (lB - lA)
    C = arc_length(NB); Cs = abs(NB[-1] - NB[0]); S = C - Cs
    row("nuc", "Radioactive decay chain A -> B -> C (Bateman): the daughter's rise and fall", "A4 (the state (N_A, N_B) is Markov: depth one), D2-D4 on N_B; O3 (no cut without a rotor)",
        "Bateman 1910 equations", "the decay constants (nuclear-supplied)",
        f"daughter peak at t = {t_peak:.2f} (closed form ln(l_B/l_A)/(l_B - l_A) = {t_star:.2f}); arc of N_B over the run C = {C:.4f}, chord {Cs:.4f}, surplus S = {S:.4f} (the rise and the fall counted, a definition)",
        "the daughter activity peaks at a time set by the two decay constants; the chain is memoryless",
        "a Markov system with no event of its own: the framework says OPEN by its own rule (spec Decision 4); the surplus is the sum of the rise and the fall, a restatement of the curve",
        "OPEN", None, "a control row: the framework is correctly silent, and nothing in the Bateman solution is reached")


# ================================================================ 2 (opt) passively Q-switched laser
def opt_q_switched_laser():
    """Gain builds under pumping until it exceeds the saturable-absorber threshold; a pulse dumps it to a fixed
    residual (fixed pulse energy) or to a variable residual. Registered: pump noise CV 0.15 with fixed threshold and
    fixed reset (Tate-like); fixed pump with threshold jitter CV 0.15."""
    rng = np.random.default_rng(2); out = []
    for name, rc, tc in (("pump noise, fixed threshold", 0.15, 0.0), ("steady pump, threshold jitter", 0.0, 0.15)):
        tr, ev = threshold_process(rng, rc, tc); lab, ca, cc = l5_class(tr, ev[3:], 0.01, segment_end="exclusive"); out.append((name, lab, ca, cc))
    row("opt", "Passively Q-switched laser: pulse train from gain build-up to a saturable-absorber threshold", "D5 (pulse = own event), A3 (the dump is the cut, exclusive segmentation), D2 (arc = gain accumulated), H-L5",
        "Q-switching rate equations (Statz-deMars); pulse-energy clamping by the saturable absorber", "the pump rate (source-supplied) and the absorber threshold",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, lab, ca, cc in out),
        "passively Q-switched pulses have nearly constant energy and a repetition rate that follows the pump; timing jitter comes from pump and threshold noise",
        f"pump noise: {reading(*out[0][1:4])}; threshold jitter: {reading(*out[1][1:4])}; the absorber fixes the chord, so the pulse energy (arc) is the regular quantity when the pump varies: the adder mechanism in optics",
        "DESCR", None, "rule 3: constant pulse energy is the absorber's clamp, not a CRR result")


# ================================================================ 3 (geo) geyser eruptions
def geo_geyser():
    """Reservoir model of a geyser: heat accumulates until boiling; an eruption expels a variable fraction of the
    reservoir; the next interval is the time to refill and reheat what was expelled. Variable release -> forward
    correlation between eruption duration (size) and the following interval; variable threshold -> backward."""
    rng = np.random.default_rng(3); n = 400
    frac = np.clip(0.5 + 0.2 * rng.standard_normal(n), 0.05, 0.95); size = frac.copy(); wait = np.r_[0.0, size[:-1]]
    def corr(a, b): return float(np.corrcoef(a, b)[0, 1])
    fwd = corr(size[:-1], wait[1:]); back = corr(size[1:], wait[1:])
    row("geo", "Geyser eruptions (reservoir model with variable release): eruption size and the following interval", "A6 (the next occasion is seeded from the settled past), D5 (eruption = own event), A8 (comparative forecast from settled occasions)",
        "reservoir/refill models of geysers; the Old Faithful duration-to-next-interval rule", "the heat flux and the released fraction (geyser-supplied)",
        f"variable release, fixed threshold: corr(size_n, following interval) = {fwd:.2f} (forward), corr(size_n, preceding interval) = {back:.2f} (backward)",
        "for Old Faithful the eruption duration predicts the interval to the next eruption (a forward rule used by park rangers)",
        "here the settled occasion does carry the next one, and A6's forward seeding reads it correctly; but the wild-systems battery's pulsar row shows the same clause fails when the threshold rather than the release varies, so what holds is the reservoir model's forward rule, which the geyser literature already had",
        "CONSIST", None, "inherited from the reservoir model (rule 3 borderline); the forward correlation is a class property (variable release), not a consequence of regeneration")


# ================================================================ 4 (clim) ENSO delayed oscillator
def clim_enso_delayed_oscillator():
    """Suarez-Schopf delayed oscillator dT/dt = T - T^3 - alpha T(t - delta) with weather noise; own event = the warm
    peak (T crossing +0.5 upward); carrier = T."""
    rng = np.random.default_rng(4); dt = 0.01; alpha, delta = 0.75, 6.0; n = 600000; lag = int(delta / dt)
    out = []
    for noise in (0.3, 0.6):
        T = np.zeros(n); T[:lag + 1] = 0.3
        for k in range(lag, n - 1):
            T[k + 1] = T[k] + dt * (T[k] - T[k] ** 3 - alpha * T[k - lag]) + noise * math.sqrt(dt) * rng.standard_normal()
        x = T[100000:]; ev = np.where((x[:-1] < 0.5) & (x[1:] >= 0.5))[0]; ev = ev[np.r_[True, np.diff(ev) > int(2.0 / dt)]]
        lab, ca, cc = l5_class(x, ev[2:], dt); per = np.diff(ev[2:]) * dt; out.append((noise, len(ev), float(per.mean()), cv(per), lab, ca, cc))
    row("clim", "ENSO as a delayed oscillator (Suarez-Schopf) with weather noise at two registered levels: warm events as occasions", "D5 (warm event = own event), D2, H-L5",
        "Suarez & Schopf 1988 delayed-oscillator model", "the delay (wave transit time), the feedback strength and the weather noise (ocean- and atmosphere-supplied)",
        "; ".join(f"noise {nz:g}: {n_} warm events, mean period {mp:.1f} (CV {cp:.2f}), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for nz, n_, mp, cp, lab, ca, cc in out),
        "ENSO recurs irregularly every 2-7 years; the delayed oscillator gives a period set by the delay and the feedback, made irregular by noise",
        f"noise 0.3: {reading(*out[0][4:7])}; noise 0.6: {reading(*out[1][4:7])}; the period is the delay's, the irregularity is the noise's, and the class is assigned by the instrument: no clause predicts it",
        "OPEN", (out[1][4], out[1][5], out[1][6]), "class assignment on a model at one delay; on a noisy 1-D carrier the sampled arc carries the noise's total variation (prompt-log entry 48)")


# ================================================================ 5 (clim) Paillard ice ages
def clim_paillard_ice_ages():
    """Paillard 1998 three-state model (i interglacial, g mild glacial, G full glacial) driven by a synthetic
    quasi-periodic insolation (23 and 41 kyr components). Transitions: i -> g when F < i0; g -> G when V > v_max;
    G -> i when F > i1. Ice volume relaxes to the state's target with tau_R. Own event = termination (G -> i)."""
    dt = 0.1; t = np.arange(0, 3000, dt); F = np.sin(2 * math.pi * t / 23.0) + 0.5 * np.sin(2 * math.pi * t / 41.0 + 1.0)
    i0, i1, vmax = -0.75, 0.0, 0.6; tau = {"i": 10.0, "g": 50.0, "G": 50.0}; state = "i"; V = 0.0; Vtr = np.empty(len(t)); term = []
    for k in range(len(t)):
        if state == "i" and F[k] < i0: state = "g"
        elif state == "g" and V > vmax: state = "G"
        elif state == "G" and F[k] > i1: state = "i"; term.append(k)
        target = 0.0 if state == "i" else 1.0; V += dt * (target - V) / tau[state]; Vtr[k] = V
    term = np.array(term); lab, ca, cc = l5_class(Vtr, term[1:], dt); gaps = np.diff(term[1:]) * dt
    row("clim", "Paillard three-state ice-age model under synthetic orbital forcing: glacial terminations as occasions", "D5 (termination = own event), D2 (arc of ice volume), H-L5; A4 (the state is (V, discrete state): depth one)",
        "Paillard 1998 multiple-state threshold model; Milankovitch pacing", "the insolation forcing (orbital) and the thresholds (climate-supplied)",
        f"{len(term)} terminations in 3000 kyr; mean spacing {gaps.mean():.1f} kyr (CV {cv(gaps):.2f}); CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}",
        "terminations are paced by insolation but require enough ice volume: the ~100 kyr cycle emerges from thresholds, not from a 100 kyr forcing",
        f"{reading(lab, ca, cc)}: the ice volume must reach v_max (a chord condition) and the forcing must then cross i1 (a clock condition); the class is decided by which wait dominates, and the framework does not say",
        "OPEN", (lab, ca, cc), "class assignment on a synthetic forcing; the 100 kyr problem is the model's, not reached by any clause")


# ================================================================ 6 (plasma) tokamak sawteeth
def plasma_sawtooth():
    rng = np.random.default_rng(6); out = []
    for name, rc, tc, reset in (("heating noise, complete crash", 0.15, 0.0, 0.0), ("heating noise, incomplete crash (variable residual)", 0.15, 0.0, 0.5)):
        tr, ev = threshold_process(rng, rc, tc, reset_cv=reset); lab, ca, cc = l5_class(tr, ev[3:], 0.01, segment_end="exclusive"); out.append((name, lab, ca, cc))
    row("plasma", "Tokamak sawtooth crashes: core temperature ramps to an instability threshold and crashes, completely or incompletely", "D5 (crash = own event), A3 (the crash is the cut, exclusive segmentation), D2 (arc = temperature ramp), H-L5",
        "Kadomtsev sawtooth model; incomplete reconnection", "the heating power (operator-supplied) and the crash fraction (plasma-supplied)",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, lab, ca, cc in out),
        "the sawtooth period scales with the heating time to the q = 1 threshold; incomplete crashes make the cycle irregular",
        f"complete crash: {reading(*out[0][1:4])}; incomplete crash: {reading(*out[1][1:4])}; the same lesson as the masting tree: a fixed chord makes the arc regular only if the reset is fixed too",
        "DESCR", None, "rule 3: the adder mechanism with and without a variable reset")


# ================================================================ 7 (sleep) two-process model
def sleep_two_process():
    """Borbely two-process model: S rises in wake toward 1 with tau_r, decays in sleep with tau_d; sleep onset when S
    hits the upper threshold H(t), wake when S hits L(t). Entrained: thresholds modulated by a 24 h circadian process.
    Free-running control: flat thresholds with a jittered rise time. Own event = sleep onset."""
    rng = np.random.default_rng(7); dt = 0.01; T = 24 * 60
    def run(circ_amp, tau_jitter):
        S = 0.3; awake = True; tau_r = 18.2; tr = []; onsets = []; t = 0.0; k = 0
        while t < T:
            H = 0.6 + circ_amp * math.sin(2 * math.pi * t / 24); L = 0.17 + circ_amp * math.sin(2 * math.pi * t / 24)
            if awake:
                S += dt * (1 - S) / tau_r
                if S >= H: awake = False; onsets.append(k); tau_r = 18.2 * (1 + tau_jitter * rng.standard_normal())
            else:
                S -= dt * S / 4.2
                if S <= L: awake = True
            tr.append(S); t += dt; k += 1
        return np.array(tr), np.array(onsets)
    out = []
    for name, amp, jit in (("entrained (circadian thresholds)", 0.12, 0.15), ("free-running (flat thresholds, jittered rise)", 0.0, 0.15)):
        tr, ev = run(amp, jit); lab, ca, cc = l5_class(tr, ev[2:], dt); gaps = np.diff(ev[2:]) * dt; out.append((name, len(ev), float(gaps.mean()), cv(gaps), lab, ca, cc))
    row("sleep", "Two-process model of sleep regulation (Borbely): sleep onsets as occasions, entrained vs free-running", "D5 (sleep onset = own event), D2 (arc of the homeostatic pressure S), H-L5",
        "Borbely 1982 two-process model; Daan-Beersma-Borbely thresholds", "the circadian modulation and the homeostatic time constants (physiology-supplied)",
        "; ".join(f"{name}: {n} onsets, mean cycle {mc:.1f} h (CV {cc_:.2f}), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, n, mc, cc_, lab, ca, cc in out),
        "entrained sleep recurs at 24 h; without the circadian gate the sleep-wake cycle free-runs at a homeostatically set period",
        f"entrained: {reading(*out[0][4:7])} (the gate moves the threshold with the clock, so arc and clock vary together); free-running: {reading(*out[1][4:7])} (a fixed threshold makes the homeostat an adder); the class is the gate's, not the framework's",
        "OPEN", (out[0][4], out[0][5], out[0][6]), "class assignment on a model; the known result (entrainment) is the gate's")


# ================================================================ 8 (micro) bacterial run-and-tumble
def micro_run_and_tumble():
    rng = np.random.default_rng(8); n = 400; runs = rng.exponential(1.0, n)
    out = []
    for name, spd_cv in (("constant swimming speed", 0.0), ("speed varying run to run (CV 0.2)", 0.2)):
        v = 20.0 * (1 + spd_cv * rng.standard_normal(n)); arcs = v * runs; out.append((name, cv(arcs), cv(runs), lab_of(arcs, runs)))
    row("micro", "Bacterial run-and-tumble: run length (arc) against run duration (clock)", "D5 (tumble = own event), D2 (arc = distance swum, monotone so S = 0), H-L5",
        "Berg & Brown 1972 run-and-tumble; exponential run durations", "the swimming speed and the tumble rate (cell-supplied)",
        "; ".join(f"{name}: CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, ca, cc, lab in out),
        "runs are exponentially distributed in duration; speed is nearly constant, so run lengths inherit the duration distribution",
        f"constant speed: {reading(out[0][3], out[0][1], out[0][2])} (the arc is the clock times a constant); variable speed: {reading(out[1][3], out[1][1], out[1][2])}; a control row: at constant speed D2 and the clock are one quantity",
        "DESCR", None, "rule 3: the arc of uniform motion is v times t")


# ================================================================ 9 (neuro) theta phase precession (H-CUT)
def neuro_phase_precession():
    """A place cell fires once per theta cycle while the animal is in its field; the spike phase advances from late to
    early across the field (precession, one full cycle). H-CUT says a system's own events sit at the phase antipode.
    Measured: the mean resultant length of spike theta-phases (1 = locked to one phase, 0 = uniform), precessing vs an
    antipode-locked control, with phase jitter 0.5 rad in both."""
    rng = np.random.default_rng(9); n_pass = 60; f_theta = 8.0; L = 0.5
    def phases(precess):
        ph = []
        for _ in range(n_pass):
            speed = 0.3 * (1 + 0.2 * rng.standard_normal()); t = 0.0; x = 0.0
            while x < L:
                x = speed * t; theta_phase = (2 * math.pi * f_theta * t) % (2 * math.pi)
                if precess: target = (math.pi + 2 * math.pi * (1 - x / L)) % (2 * math.pi)
                else: target = math.pi
                ph.append((target + 0.5 * rng.standard_normal()) % (2 * math.pi)); t += 1 / f_theta
        return np.array(ph)
    R = {name: float(abs(np.mean(np.exp(1j * phases(p))))) for name, p in (("precessing", True), ("antipode-locked control", False))}
    row("neuro", "Hippocampal theta phase precession: are a place cell's spikes at the theta antipode?", "H-CUT (own events at the phase antipode), A3, D5",
        "O'Keefe & Recce 1993 phase precession; circular statistics (mean resultant length)", "the running speed and the theta rhythm (animal-supplied)",
        f"mean resultant length of spike phases: precessing cell {R['precessing']:.3f}, antipode-locked control {R['antipode-locked control']:.3f} (1 = one phase, 0 = uniform)",
        "spike phase advances systematically through the theta cycle as the animal crosses the field, so spikes are not locked to any single phase",
        "the system's own events sweep the whole cycle by the domain's own mechanism, so 'own events sit at the antipode' fails on the best-known phase-coded system in neuroscience; H-CUT can hold only on systems without phase coding",
        "FAILS", None, "rule 4 / class dependence: the first H-CUT row in the batteries; v3.1 H-CUT is gated for real data, and this model says which class the gate must exclude")


# ================================================================ 10 (eco) Rosenzweig-MacArthur cycles
def eco_rosenzweig_macarthur():
    """Prey with logistic growth and a type-II predator: a limit cycle for large carrying capacity; environmental
    noise on the prey growth rate. Own event = prey peak (log-prey crossing its mean upward). Carrier: log prey."""
    rng = np.random.default_rng(10); r0, K, a, h, e, m = 1.0, 8.0, 1.0, 1.0, 0.6, 0.25; dt = 0.01; n = 400000
    N, P = 2.0, 0.5; logN = np.empty(n); rr = r0
    for k in range(n):
        if k % 100 == 0: rr = r0 * math.exp(0.15 * rng.standard_normal())
        fr = a * N / (1 + a * h * N); dN = rr * N * (1 - N / K) - fr * P; dP = e * fr * P - m * P
        N = max(N + dt * dN, 1e-6); P = max(P + dt * dP, 1e-6); logN[k] = math.log(N)
    x = logN[100000:]; mu = x.mean(); ev = np.where((x[:-1] < mu) & (x[1:] >= mu))[0]; ev = ev[np.r_[True, np.diff(ev) > int(3.0 / dt)]]
    lab, ca, cc = l5_class(x, ev[2:], dt); per = np.diff(ev[2:]) * dt
    row("eco", "Rosenzweig-MacArthur predator-prey limit cycle with environmental noise (hare-lynx-like): prey peaks as occasions", "D5 (prey peak = own event), D2 on log prey, H-L5",
        "Rosenzweig & MacArthur 1963; paradox of enrichment", "the growth, attack and mortality rates (ecology-supplied) and the noise",
        f"{len(ev)} cycles; mean period {per.mean():.1f} (CV {cv(per):.2f}); CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}",
        "population cycles have a period set by the interaction rates and amplitudes that noise makes irregular",
        f"{reading(lab, ca, cc)}: the class is the instrument's assignment; the period and the amplitude are the model's",
        "OPEN", (lab, ca, cc), "class assignment on a model; the paradox of enrichment (cycle onset with K) is a Hopf, covered earlier")


# ================================================================ 11 (ops) bullwhip effect
def ops_bullwhip():
    """Order-up-to policy with a moving-average forecast over p periods and lead time L on i.i.d. demand: the order
    variance amplification (Chen et al. 2000 lower bound 1 + 2L/p + 2L^2/p^2). The forecast's memory of past demand
    is a box window: uniform over p, zero beyond (a fourth memory class beside recency, wiping-out and primacy)."""
    rng = np.random.default_rng(11); n = 40000; L = 2; D = 10 + rng.standard_normal(n)
    out = []
    for p in (5, 20):
        q = np.empty(n - p - 1)
        for t in range(p + 1, n):
            fc, fc_prev = D[t - p:t].mean(), D[t - p - 1:t - 1].mean(); q[t - p - 1] = D[t - 1] + (L + 1) * (fc - fc_prev)
        ratio = float(q.var() / D.var()); closed = 1 + 2 * (L + 1) / p + 2 * (L + 1) ** 2 / p ** 2; out.append((p, ratio, closed))
    row("ops", "Bullwhip effect: order-variance amplification under moving-average forecasting (a windowed memory)", "A6 (regeneration from the settled past), P3 (age weights), O2",
        "Chen, Drezner, Ryan & Simchi-Levi 2000; order-up-to policies", "the demand process and the forecast window (manager-supplied)",
        "; ".join(f"window p = {p}: Var(orders)/Var(demand) = {r:.2f} (closed form for this policy 1 + 2(L+1)/p + 2(L+1)^2/p^2 = {b:.2f}; Chen et al.'s bound has the same form in their lead-time convention)" for p, r, b in out),
        "amplification falls with the forecast window and rises with the lead time; the bound is attained by the order-up-to policy on i.i.d. demand",
        "the forecast weights the past uniformly over a window and not at all beyond it: neither geometric age (P3) nor surplus (P2); the amplification is the window's, and the framework names none of it",
        "DESCR", None, "the fourth measured memory class in the batteries (window); the T5 prereg must exclude it or model it")


# ================================================================ 12 (mat) fibre bundle
def mat_fibre_bundle():
    """Equal-load-sharing fibre bundle, N fibres with uniform(0,1) thresholds, quasi-static loading: bursts between
    stable states; the critical load 1/4 and the burst-size exponent -5/2."""
    rng = np.random.default_rng(12); N = 20000; thr = np.sort(rng.random(N)); alive = N; bursts = []; loads = []
    F = 0.0
    while alive > 0:
        k = N - alive; F = thr[k] * alive; loads.append(F / N); s = 0
        while alive > 0 and thr[N - alive] * alive <= F:
            alive -= 1; s += 1
        bursts.append(s)
    bursts = np.array(bursts); sig_c = max(loads)
    edges = np.array([1, 2, 4, 8, 16, 32]); cnt = np.array([((bursts >= lo) & (bursts < hi)).sum() for lo, hi in zip(edges[:-1], edges[1:])], float)
    dens = cnt / np.diff(edges); mids = np.sqrt(edges[:-1] * edges[1:]); ok = dens > 0
    slope = float(np.polyfit(np.log(mids[ok]), np.log(dens[ok]), 1)[0])
    row("mat", "Fibre-bundle model of cascading failure: bursts, critical load and the burst-size exponent", "A1' (unit = one fibre), D5 (burst = own event); no clause on exponents or critical loads",
        "Daniels 1945 fibre bundle; Hemmer & Hansen 1992 burst exponent -5/2", "the threshold distribution (material-supplied)",
        f"N = {N}: maximum sustainable load per fibre {sig_c:.4f} (exact 1/4 = 0.25); {len(bursts)} bursts, size-distribution log-log slope on 1..32 = {slope:.2f} (asymptotic -5/2)",
        "equal-load-sharing bundles fail at a critical load with power-law burst sizes of exponent -5/2 near criticality",
        "the critical load and the exponent are the bundle's; the burst is an occasion the framework can count, and nothing else",
        "DESCR", None, "no CRR clause reaches a critical load or an avalanche exponent; a fourth avalanche system with the same verdict")


# ================================================================ 13 (rl) TD(lambda) traces
def rl_td_lambda_traces():
    """19-state random walk; TD(lambda) with accumulating vs replacing eligibility traces (the trace is an age weight
    (gamma lambda)^k by design). RMS value error after 10 episodes, averaged over 50 runs, best alpha per case."""
    rng = np.random.default_rng(13); n_states = 19; true_v = np.linspace(-1, 1, n_states + 2)[1:-1]
    def run(lam, alpha, replacing):
        V = np.zeros(n_states + 2)
        for ep in range(10):
            s = n_states // 2 + 1; z = np.zeros(n_states + 2)
            while 0 < s < n_states + 1:
                s2 = s + (1 if rng.random() < 0.5 else -1); r = 1.0 if s2 == n_states + 1 else (-1.0 if s2 == 0 else 0.0)
                z *= lam; z[s] = 1.0 if replacing else z[s] + 1.0
                delta = r + (V[s2] if 0 < s2 < n_states + 1 else 0.0) - V[s]; V += alpha * delta * z; s = s2
        return float(np.sqrt(np.mean((V[1:-1] - true_v) ** 2)))
    out = []
    for lam in (0.4, 0.8, 0.95):
        best = {}
        for replacing in (False, True):
            errs = {al: np.mean([run(lam, al, replacing) for _ in range(50)]) for al in (0.05, 0.1, 0.2, 0.4)}
            al = min(errs, key=errs.get); best["replacing" if replacing else "accumulating"] = (al, float(errs[al]))
        out.append((lam, best))
    row("rl", "TD(lambda) on a 19-state random walk: accumulating vs replacing eligibility traces", "P3 (age weights: the trace is (gamma lambda)^k by design), A6 ('never an accumulated count': the accumulating trace counts revisits)",
        "Sutton & Barto; Singh & Sutton 1996 (replacing traces)", "the return process and the trace decay (designer-supplied)",
        "; ".join(f"lambda = {lam}: accumulating RMS {b['accumulating'][1]:.3f} (alpha {b['accumulating'][0]}), replacing RMS {b['replacing'][1]:.3f} (alpha {b['replacing'][0]})" for lam, b in out),
        "replacing traces are more robust than accumulating traces at high lambda in tabular problems; both are geometric in age",
        f"the geometric age weight is a design choice (P3 renamed); at lambda = 0.95 the counting trace is {'worse' if out[2][1]['accumulating'][1] > out[2][1]['replacing'][1] else 'better'} than the capped one by {abs(out[2][1]['accumulating'][1] - out[2][1]['replacing'][1]):.3f} RMS, so here A6's distrust of the count is on the winning side, unlike the cache row: the count-vs-cap choice is the learner's, and no clause decides it",
        "DESCR", None, "rule 3 on the kernel; the count question is decided problem by problem (cache: count wins on stationary streams; here: the cap wins at high lambda)")


# ================================================================ 14 (mat) Kovacs memory effect
def mat_kovacs_memory():
    """Two-mode linear model of structural relaxation: delta = a1 + a2, da_i/dt = -(a_i - w_i delta_eq(T)) / tau_i(T),
    tau_i(T) = tau_i0 exp(E (1/T - 1/T0)). Kovacs protocol: quench from T0 to T1, hold t1, then jump to T2 chosen so that
    delta equals delta_eq(T2) at the jump; the volume then departs from equilibrium (a hump) before returning."""
    E, T0 = 8.0, 1.0; w = np.array([0.6, 0.4]); tau0 = np.array([1.0, 20.0])
    def deq(T): return (T - T0) * 0.1
    def tau(T): return tau0 * np.exp(E * (1 / T - 1 / T0))
    def integrate(a, T, t_end, dt=0.01):
        n = int(t_end / dt); out = np.empty(n)
        for k in range(n):
            a = a + dt * (-(a - w * deq(T)) / tau(T)); out[k] = a.sum()
        return a, out
    a = w * deq(T0); T1 = 0.8; a, _ = integrate(a, T1, 30.0)
    # choose T2 with delta_eq(T2) = current delta
    T2 = T0 + a.sum() / 0.1; a2, path = integrate(a.copy(), T2, 400.0)
    hump = float(np.max(np.abs(path - deq(T2)))); start_dev = abs(path[0] - deq(T2))
    # single-step control: equilibrium at T2 stays at equilibrium
    _, ctrl = integrate(w * deq(T2), T2, 400.0); ctrl_dev = float(np.max(np.abs(ctrl - deq(T2))))
    row("mat", "Kovacs memory effect in a two-mode glass model: the same volume at the same temperature, different futures", "A4 (depth one only in the full state), D6/H-T1 class (the path matters), A6",
        "Kovacs 1963 memory experiment; multi-mode (TNM/KAHR-type) linear relaxation", "the mode spectrum and the thermal history (material- and experimenter-supplied)",
        f"after quench to T1 = {T1} for 30 time units and a jump to T2 = {T2:.3f} where delta already equals delta_eq(T2): initial deviation {start_dev:.1e}, maximum later deviation (the Kovacs hump) {hump:.4f}; control started at equilibrium at T2: maximum deviation {ctrl_dev:.1e}",
        "a glass with the same macroscopic volume and temperature can evolve differently depending on its thermal history: the observable state is not the full state",
        "the path matters because the observable (volume) is a projection of a two-dimensional state, not because of any surplus: a textbook hidden-variable memory that D6/H-T1 would read as path dependence and A4 explains away once the full state is named",
        "DESCR", None, "the framework's path-vs-endpoint distinction reduces here to the choice of state variables; nothing about glasses is derived")


# ================================================================ 15 (games) Elo ratings
def games_elo_k_factor():
    """A player's skill follows a random walk with Fisher speed v; Elo updates R <- R + K (S - E) with E = logistic;
    the best K (lowest log-loss against a known-skill opponent) for three v, against the Kalman reading (P4)."""
    rng = np.random.default_rng(15); T = 20000; scale = 400 / math.log(10)
    def logloss(K, v):
        skill = 0.0; R = 0.0; ll = 0.0
        for t in range(T):
            skill += v * 30.0 * rng.standard_normal(); p_true = 1 / (1 + math.exp(-skill / scale)); S = 1.0 if rng.random() < p_true else 0.0
            E = 1 / (1 + math.exp(-R / scale)); ll -= S * math.log(max(E, 1e-9)) + (1 - S) * math.log(max(1 - E, 1e-9)); R += K * (S - E)
        return ll / T
    Ks = (2, 4, 8, 16, 32, 64, 128, 256); res = {v: min(Ks, key=lambda K: logloss(K, v)) for v in (0.03, 0.1, 0.3)}
    mono = all(res[a] <= res[b] for a, b in zip((0.03, 0.1), (0.1, 0.3)))
    row("games", "Elo ratings: the best K-factor against skill volatility, read against the Kalman gain (P4)", "P4 (gain follows the Fisher speed), O1",
        "Elo 1978; Glicko as its Kalman-style extension", "the skill volatility (player-supplied) and the opponent pool",
        "; ".join(f"skill speed v = {v:g}: best K = {K}" for v, K in res.items()) + f" (grid 2-256); best K non-decreasing in v: {mono}",
        "the K-factor is set by convention per federation and by rating age; rating systems with an uncertainty term adapt it",
        f"the best gain {'rises' if mono else 'does not rise monotonically'} with the volatility on this grid, the Kalman reading in a logistic setting; P4 says of itself that it is not CRR's, and no value of K is privileged",
        "DESCR", None, "the Rescorla-Wagner row's conclusion in a different domain")


# ================================================================ 16 (acoust) cricket chirps
def acoust_cricket_dolbear():
    rng = np.random.default_rng(16); n = 300; T = 20 + 4 * np.cumsum(0.1 * rng.standard_normal(n)); T = np.clip(T, 12, 30)
    rate = (T - 4) / 10.0; intervals = 1.0 / rate; chirp_arc = 1.0 * (1 + 0.03 * rng.standard_normal(n))
    row("acoust", "Cricket chirps under drifting temperature (Dolbear's law): a fixed motor pattern at a temperature-set rate", "D5 (chirp = own event), D2 (arc = the chirp's fixed motor excursion), H-L5",
        "Dolbear 1897 (chirp rate linear in temperature); central pattern generation", "the temperature (environment-supplied)",
        f"temperature range {T.min():.1f}-{T.max():.1f}: chirp interval CV {cv(intervals):.3f}, chirp arc CV {cv(chirp_arc):.3f} -> {lab_of(chirp_arc, intervals)}",
        "chirp rate rises linearly with temperature while the chirp's structure is conserved",
        f"{lab_of(chirp_arc, intervals)} by construction: the pattern generator's excursion is fixed and its rate is the environment's; a thermometer made of arc-regularity",
        "DESCR", None, "rule 3: the adder mechanism in bioacoustics")


# ================================================================ 17 (learn) spacing effect
def learn_spacing_effect():
    """ACT-R with the Pavlik-Anderson activation-dependent decay: practice j gets decay d_j = c exp(m_j) + a, where m_j is the
    activation at the moment of practice j from the earlier practices (massed practices arrive at high activation and
    decay faster). Recall activation at test = ln sum_j (T - t_j)^(-d_j). Eight practices massed (1 min apart) vs spaced
    (1 day apart), tested one week after the last. Also the measured influence of a single practice as a function of
    its age, fitted as geometric (P3) and as power-law."""
    c, a = 0.277, 0.177; week = 7 * 24 * 60.0
    def activation_at_test(times, T):
        d = []
        for j, tj in enumerate(times):
            if j == 0: d.append(a)
            else:
                m = math.log(sum((tj - ti) ** (-di) for ti, di in zip(times[:j], d))); d.append(c * math.exp(m) + a)
        return math.log(sum((T - tj) ** (-dj) for tj, dj in zip(times, d)))
    massed = [k * 1.0 for k in range(8)]; spaced = [k * 24 * 60.0 for k in range(8)]
    A_m, A_s = activation_at_test(massed, massed[-1] + week), activation_at_test(spaced, spaced[-1] + week)
    ages = np.array([1, 10, 100, 1000, 10000.0]); infl = ages ** (-a)
    r2_geo = r2(np.log(infl), ages); r2_pow = r2(np.log(infl), np.log(ages))
    row("learn", "The spacing effect (ACT-R with activation-dependent decay): retention after massed vs spaced practice, and the shape of the age kernel", "P3 (geometric age weights from a mean-age constraint), P5 (retention in natural time), O2, A6 (the past is re-weighted, not re-counted)",
        "Anderson & Schooler 1991 base-level learning; Pavlik & Anderson 2005 activation-dependent decay; the spacing effect (Ebbinghaus)", "the decay parameters and the practice schedule (learner- and teacher-supplied)",
        f"activation at test one week after the last practice: massed {A_m:.3f}, spaced {A_s:.3f} ({'spaced' if A_s > A_m else 'massed'} higher by {abs(A_s - A_m):.3f}); influence of one practice at age 1..10^4 min: {', '.join(f'{v:.3f}' for v in infl)}; R^2 of log influence on age (geometric) = {r2_geo:.3f}, on log age (power law) = {r2_pow:.3f}",
        "spaced practice is retained better than massed practice; memory strength decays as a power law of age, faster when practice arrives at high activation",
        f"{'spaced practice wins' if A_s > A_m else 'massed practice wins'} in this model; the age kernel is a power law, not the geometric form a mean-age MaxEnt gives (P3), and not a surplus weight (P2); the spacing effect is the decay rule's dependence on the state at practice, which is a regeneration rule the framework does not have",
        "DESCR", None, "rule 3 on the model; taxonomic value: five memory kernels are now on record (geometric, wiping-out, primacy, window, power law) and the framework's two constraints cover one of them")


# ================================================================ 18 (econ) cobweb model
def econ_cobweb():
    a, b, c, d = 10.0, 1.0, 1.0, 0.8; p = 3.0; ps = []
    for t in range(60): q = c + d * p; p = (a - q) / b; ps.append(p)
    ps = np.array(ps); p_star = (a - c) / (b + d); amp = np.abs(ps - p_star); ratio = float(amp[10] / amp[8])
    row("econ", "Cobweb model of price and lagged supply: convergent oscillation around the equilibrium", "A4 (the state is last period's price: depth one), O3 (no cut without a rotor)",
        "Ezekiel 1938 cobweb; linear first-order difference equation", "the supply and demand slopes (market-supplied)",
        f"equilibrium price {p_star:.3f}; amplitude ratio over one cycle {ratio:.3f} (theory (d/b)^2 = {(d / b) ** 2:.3f})",
        "prices oscillate and converge when supply is less steep than demand; the period is two",
        "a depth-one linear map: the framework is silent by its own rule, and the period-two oscillation is the sign of -d/b",
        "DESCR", None, "a control row like the decay chain: nothing to test")


# ================================================================ 19 (surf) RHEED oscillations
def surf_rheed_oscillations():
    rng = np.random.default_rng(19); dt = 0.01; n_ev = 80
    tr, ev = threshold_process(rng, 0.2, 0.0, dt=dt, n_ev=n_ev, ou_rate=0.02)                                     # coverage per layer = 1 exactly; flux varies
    lab, ca, cc = l5_class(tr, ev[3:], dt, segment_end="exclusive")
    row("surf", "RHEED intensity oscillations in layer-by-layer growth: one oscillation per monolayer under a varying flux", "O3 (natural time = the monolayer count), D5 (layer completion = own event), D2 (arc = coverage), H-L5",
        "Neave, Joyce et al. 1983 RHEED oscillations; layer-by-layer (Frank-van der Merwe) growth", "the deposition flux (source-supplied)",
        f"CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}",
        "growers count monolayers by counting oscillations, whatever the flux does",
        f"{reading(lab, ca, cc)} by construction: each oscillation is one monolayer, and the technique is natural time used as a ruler; the framework describes a practice thirty years old",
        "DESCR", None, "rule 3: natural time as the industry counts it")


# ================================================================ 20 (fire) fuel-threshold fire regime
def fire_regime():
    """Fuel accumulates dF/dt = (F_max - F)/tau; a fire is possible once F > F_thr and then occurs at a hazard h per
    year (ignition-limited); a fire resets F to 0. Registered: fuel-limited (high hazard) vs ignition-limited (low hazard)."""
    rng = np.random.default_rng(20); dt = 0.05; out = []
    for name, h in (("fuel-limited (hazard 5/yr above threshold)", 5.0), ("ignition-limited (hazard 0.2/yr)", 0.2)):
        F = 0.0; tr = []; ev = []; k = 0
        while len(ev) < 80:
            F += dt * (1.0 - F) / 5.0; tr.append(F); k += 1
            if F > 0.6 and rng.random() < h * dt: ev.append(k); F = 0.0
        tr = np.array(tr); ev = np.array(ev); lab, ca, cc = l5_class(tr, ev[3:], dt, segment_end="exclusive"); gaps = np.diff(ev[3:]) * dt
        out.append((name, float(gaps.mean()), cv(gaps), lab, ca, cc))
    row("fire", "Fire regimes: fuel accumulation to a threshold with fuel-limited vs ignition-limited burning", "D5 (fire = own event), A3 (the burn is the cut, exclusive segmentation), D2 (arc = fuel accumulated), H-L5",
        "hazard-of-fire models with fuel build-up (Weibull fire-interval models)", "the fuel recovery time and the ignition hazard (landscape- and weather-supplied)",
        "; ".join(f"{name}: mean interval {mi:.1f} yr (CV {ci:.2f}), CV_arc {ca:.3f} vs CV_clock {cc:.3f} -> {lab}" for name, mi, ci, lab, ca, cc in out),
        "fire intervals are fuel-limited where ignitions are frequent and ignition-limited where they are rare; the hazard rises with time since fire",
        f"fuel-limited: {reading(*out[0][3:6])}; ignition-limited: {reading(*out[1][3:6])} (the fuel saturates while waiting for an ignition, so the chord is fixed by saturation and the arc is regular for a reason that has nothing to do with the fire); the class is the landscape's, and the framework names it",
        "OPEN", (out[1][3], out[1][4], out[1][5]), "class assignment on a model; the known fuel-vs-ignition dichotomy is the ecology's")


BATTERY = [nuc_decay_chain, opt_q_switched_laser, geo_geyser, clim_enso_delayed_oscillator, clim_paillard_ice_ages, plasma_sawtooth,
           sleep_two_process, micro_run_and_tumble, neuro_phase_precession, eco_rosenzweig_macarthur, ops_bullwhip, mat_fibre_bundle,
           rl_td_lambda_traces, mat_kovacs_memory, games_elo_k_factor, acoust_cricket_dolbear, learn_spacing_effect, econ_cobweb,
           surf_rheed_oscillations, fire_regime]

CLASSES = {"nuc": "nuclear physics", "opt": "laser physics", "geo": "geothermal", "clim": "climate", "plasma": "plasma physics",
           "sleep": "sleep physiology", "micro": "microbial motility", "neuro": "systems neuroscience", "eco": "population ecology",
           "ops": "operations management", "mat": "materials", "rl": "reinforcement learning", "games": "rating systems",
           "acoust": "bioacoustics", "learn": "human learning", "econ": "economics", "surf": "surface science", "fire": "fire ecology"}


def main():
    for f in BATTERY: f()
    print(f"CRR retrodiction battery: twenty model systems in eighteen domains — {len(ROWS)} rows. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
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
        print(f"({c}) {name:24s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':32s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print("\nH-L5 class map (model systems with their own events):")
    for r in ROWS:
        if r["l5"]: print(f"  {r['l5'][0]:44s} {r['system']}")
    print(f"\nrows where the coherence integral's velocity is system-supplied (FLOW != none): {sum('none' not in r['flow'] for r in ROWS)}/{len(ROWS)}")
    print(f"Rows where a CRR clause reaches a result the domain did not already have: {sum(r['grade'] == 'SHARP' for r in ROWS)} of {len(ROWS)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
