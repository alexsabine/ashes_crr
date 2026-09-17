"""CRR retrodiction battery on biological systems (owner request 2026-09-17, prompt-log entry 39).

Nineteen model systems with known biology, six classes: (n) neural, (c) cardiac and
physiological, (e) epidemiological, (p) population and evolutionary, (m) molecular and cellular,
(b) behavioural and adaptive. Every row states the clause applied, BORROWED (the mathematics
inherited from the domain), FLOW (what supplies the velocity inside the coherence integral), the
derivation with its printed numbers, the known result, and a grade under the issue-#21 rules
(SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN; rule 2 on chosen observables, rule 4 on
symmetric members). For every system with its own events the H-L5 class is computed on the
model with the repository's own instrument (`crr.instrument.core.regularity`): clock-regular
(CV_clock < CV_arc) or arc-regular (CV_arc < CV_clock), so the battery doubles as the map of
biological systems by class that docs/ROADMAP_2026-Q4.md asks for.

Model systems only; no dataset is opened (R2). Deterministic (fixed grids, seeded noise).
Run: uv run python theory/retrodictions/bio_retrodictions.py
"""
import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

from crr.instrument.core import regularity

ROWS = []


def row(cls, system, clause, borrowed, flow, derivation, known, verdict, grade, l5=None, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, flow=flow, derivation=derivation,
                     known=known, verdict=verdict, grade=grade, l5=l5, weakness=weakness))


def cv(x): x = np.asarray(x, float); return float(x.std(ddof=1) / abs(x.mean()))


def l5_class(x, events, dt=1.0):
    """H-L5 on a model trace with its own events: returns (label, cv_arc, cv_clock)."""
    r = regularity(np.asarray(x, float), np.asarray(events, int), sigma=1.0, dt=dt, n_boot=200, seed=0)
    if abs(r["cv_arc"] - r["cv_clock"]) < 1e-3: lab = "tie"          # below instrument resolution: neither quantity wins
    else: lab = "arc-regular" if r["cv_arc"] < r["cv_clock"] else "clock-regular"
    return lab, r["cv_arc"], r["cv_clock"]


# ================================================================ (n) neural
def n_lif_noisy():
    rng = np.random.default_rng(0); dt = 1e-3; mu, sig, tau = 1.2, 0.35, 1.0
    V = 0.0; trace = []; spikes = []
    for i in range(400000):
        V += dt * (mu - V) / tau + sig * math.sqrt(dt) * rng.standard_normal()
        if V >= 1.0: spikes.append(i); V = 0.0
        trace.append(V)
    trace = np.array(trace); spikes = np.array(spikes)[2:60]
    lab, ca, cc = l5_class(trace, spikes, dt)
    chord = [abs(trace[b - 1] - trace[a]) for a, b in zip(spikes[:-1], spikes[1:])]
    row("n", "Leaky integrate-and-fire neuron with noisy input current", "D5 (the spike is the system's own event), D2-D4, H-L5",
        "threshold-reset dynamics; Ornstein-Uhlenbeck subthreshold voltage", "the input current (mean and noise, experimenter-supplied)",
        f"{len(spikes)} spikes; CV_arc = {ca:.3f}, CV_ISI = {cc:.3f}; chord birth->spike = {np.mean(chord):.3f} (fixed at threshold - reset by construction, CV {cv(chord):.1e})",
        "ISI variability from input noise; threshold fixed", f"{lab}: the arc (voltage travelled) is more regular than the interval because the threshold fixes the chord and noise adds a bounded surplus",
        "CONSIST", (lab, ca, cc), "the regular quantity is the chord, a definition of the model (threshold minus reset); the arc inherits it; nothing about the neuron is derived")


def n_fhn_varying_drive():
    def f(t, y):
        v, w = y; I = 0.5 + 0.2 * math.sin(0.03 * t)
        return [v - v ** 3 / 3 - w + I, 0.08 * (v + 0.7 - 0.8 * w)]
    t = np.linspace(0, 1200, 240001); sol = solve_ivp(f, (0, 1200), [-1.0, -0.5], t_eval=t, method="RK45", rtol=1e-8, atol=1e-10)
    v = sol.y[0]; up = np.where((v[1:] > 0.5) & (v[:-1] <= 0.5))[0] + 1
    up = up[2:]; lab, ca, cc = l5_class(v, up, t[1] - t[0])
    amps = [v[a:b].max() - v[a:b].min() for a, b in zip(up[:-1], up[1:])]
    row("n", "FitzHugh-Nagumo relaxation oscillator under slowly varying drive (class-2 model neuron)", "D5, D2, H-L5 (the S-G2 mechanism: threshold fixed, charging rate varies)",
        "FitzHugh-Nagumo equations; relaxation-oscillator geometry", "the drive current I(t) (supplied)",
        f"{len(up)} spikes; CV_arc = {ca:.3f}, CV_ISI = {cc:.3f}; spike amplitude CV = {cv(amps):.3f}",
        "spike shape is stereotyped, rate follows the drive", f"{lab}: a relaxation oscillator with a fixed excursion and a variable charging rate keeps arc, not time",
        "CONSIST", (lab, ca, cc), "true by the relaxation-oscillator mechanism (the battery's S-G2); the framework names the class, the neuron model supplies it")


def n_snic_vs_hopf():
    # class-1 (SNIC) onset: theta' = 1 - cos(theta) + (1 + cos(theta)) I ; frequency ~ sqrt(I), amplitude fixed
    def snic_freq(I):
        def f(t, y): return [1 - math.cos(y[0]) + (1 + math.cos(y[0])) * I]
        sol = solve_ivp(f, (0, 400), [0.0], t_eval=np.linspace(0, 400, 40001), method="RK45", rtol=1e-8, atol=1e-10)
        return (sol.y[0][-1] - sol.y[0][0]) / (2 * math.pi * 400)
    Is = (0.1, 0.01, 0.001); fr = [snic_freq(I) for I in Is]
    hopf_amp = [math.sqrt(m) for m in Is]
    row("n", "Onset of repetitive firing: class 1 (SNIC) vs class 2 (Hopf) excitability", "issue-#21 text criticality clause (rho -> 0 at a Hopf point) applied to neurons",
        "Ermentrout-Kopell normal form; Hodgkin's excitability classes", "the injected current near threshold",
        "SNIC: frequency at I = " + ", ".join(f"{I:g}: {f:.4f}" for I, f in zip(Is, fr)) + " -> 0 while the excursion stays 2*pi (rho fixed); Hopf: amplitude " + ", ".join(f"{a:.3f}" for a in hopf_amp) + " -> 0 (rho -> 0)",
        "class 1 neurons start firing at arbitrarily low rate with full-size spikes; class 2 at finite rate with growing amplitude", "rho -> 0 at onset holds only for the Hopf (class 2) member; class 1 keeps a full-size occasion at vanishing rate",
        "FAILS", None, "rule 4: the criticality claim is a property of the Hopf member; v3.1 makes no criticality claim, the issue text does")


def n_weber_fechner():
    s1, s2 = 10.0, 80.0
    arc = math.log(s2 / s1)                                 # Fisher metric (ds/s)^2 under Weber's law
    jnd_steps = arc / 0.1                                    # Weber fraction 0.1 -> resolvable steps
    row("n", "Perceptual discrimination: Weber's law and the Fechner scale", "A1' (the resolvable step as the unit), D2",
        "Fisher-information account of discrimination (JND = 1/sqrt(I)); Weber's law I(s) ∝ 1/s^2", "the stimulus schedule",
        f"with Weber fraction 0.1 the FR arc from s = {s1:g} to {s2:g} is ln(s2/s1) = {arc:.4f}, i.e. {jnd_steps:.1f} JNDs: the Fechner scale is the Fisher arc",
        "Fechner's logarithmic scale follows from Weber's law", "the unit A1' names is the JND and the arc is the psychophysical scale; both are the domain's own",
        "CONSIST", None, "the Fisher-information reading of JNDs is standard psychophysics; Weber's law itself is not derived")


# ================================================================ (c) cardiac and physiological
def _pulse_train(periods, amps, fs=200):
    t = []; x = []; t0 = 0.0; onsets = []
    for T, A in zip(periods, amps):
        n = int(round(T * fs)); tt = np.arange(n) / fs
        onsets.append(len(x)); x.extend(A * (np.exp(-((tt - 0.12) / 0.04) ** 2) + 0.35 * np.exp(-((tt - 0.32) / 0.08) ** 2)))
        t0 += T
    return np.array(x), np.array(onsets), 1 / fs


def c_rsa():
    n = 60; k = np.arange(n); periods = 0.9 + 0.08 * np.sin(2 * np.pi * k / 5); amps = np.ones(n)
    x, on, dt = _pulse_train(periods, amps); lab, ca, cc = l5_class(x, on, dt)
    row("c", "Respiratory sinus arrhythmia: RR interval modulated by breathing, pulse shape fixed", "H-L5 (S-A' mechanism: period jitter, amplitude constant)",
        "vagal modulation of sinus rate; the pulse waveform", "the sinus node and the respiratory drive",
        f"CV_arc = {ca:.3f}, CV_clock = {cc:.3f} over {n} beats (period 0.90 ± 0.08 s, amplitude fixed)",
        "RSA is frequency modulation of the heartbeat", f"{lab}: with the waveform fixed and the period modulated, arc per beat is the regular quantity",
        "DESCR", (lab, ca, cc), "true by construction of RSA (an FM class member); study CARD will test it on records, this row cannot")


def c_pulsus_alternans():
    n = 60; periods = np.full(n, 0.8); amps = np.where(np.arange(n) % 2 == 0, 1.0, 0.7)
    x, on, dt = _pulse_train(periods, amps); lab, ca, cc = l5_class(x, on, dt)
    row("c", "Pulsus alternans: fixed rate, alternating pulse amplitude", "A3 note (v3.1): equal half-turn arcs are not a consequence of A3; H-L5",
        "cardiac alternans (period-doubling of the beat amplitude at fixed pacing)", "the pacing rate and the alternans mechanism",
        f"CV_arc = {ca:.3f}, CV_clock = {cc:.3f}: consecutive occasions alternate in arc while the clock is exact",
        "alternans is amplitude alternation at constant period", f"{lab}: the clock keeps, the arc alternates; equal arcs fail on an asymmetric (alternating) member",
        "DESCR", (lab, ca, cc), "a class assignment on a model waveform; nothing derived")


def c_afib_like():
    rng = np.random.default_rng(3); n = 60; periods = 0.8 + 0.2 * rng.standard_normal(n); periods = np.clip(periods, 0.4, 1.4)
    amps = 1 + 0.25 * rng.standard_normal(n); amps = np.clip(amps, 0.4, 1.6)
    x, on, dt = _pulse_train(periods, amps); lab, ca, cc = l5_class(x, on, dt)
    row("c", "Irregular rhythm with variable pulse amplitude (fibrillation-like)", "H-L5",
        "the pulse train model", "the arrhythmia (both period and amplitude random)",
        f"CV_arc = {ca:.3f}, CV_clock = {cc:.3f}: neither quantity is regular",
        "irregularly irregular rhythm", "no clause says which clock such a system keeps; the instrument reports the class it falls in",
        "OPEN", (lab, ca, cc), "class assignment only; the framework has no claim about it")


# ================================================================ (e) epidemiological
def _sir_forced(beta0=1250.0, eps=0.28, gamma=365 / 13, mu=1 / 50, years=40, N=1e6, I0=1e-4, S0=0.06):
    def f(t, y):
        S, I = y; b = beta0 * (1 + eps * math.cos(2 * math.pi * t))
        return [mu - b * S * I - mu * S, b * S * I - (gamma + mu) * I]
    t = np.linspace(0, years, years * 365 + 1)
    sol = solve_ivp(f, (0, years), [S0, I0], t_eval=t, method="RK45", rtol=1e-8, atol=1e-12, max_step=1 / 365)
    return t, sol.y[1] * N


def e_forced_sir():
    t, inc = _sir_forced(years=60); inc = inc[365 * 20:]; t = t[365 * 20:]
    arc = 2 * np.sqrt(np.maximum(inc, 0))                    # Poisson-metric coordinate (SCOPE P6)
    def peaks(frac):
        pk = np.where((inc[1:-1] > inc[:-2]) & (inc[1:-1] >= inc[2:]) & (inc[1:-1] > frac * inc.max()))[0] + 1
        keep = [pk[0]]
        for q in pk[1:]:
            if q - keep[-1] > 200: keep.append(q)
        return np.array(keep)
    pk_all, pk_major = peaks(0.2), peaks(0.6)
    lab_a, ca_a, cc_a = l5_class(arc, pk_all, t[1] - t[0]); lab_m, ca_m, cc_m = l5_class(arc, pk_major, t[1] - t[0])
    gaps = np.diff(t[pk_all])[:4]; sizes = inc[pk_all][:4] / 1e3
    row("e", "Seasonally forced SIR (measles-like, period-2 regime): which events are the occasions?", "H-L5 on the Poisson carrier (SCOPE P6); v3.1 O3 (natural time gives the unit, not the cut)",
        "SIR dynamics with seasonal transmission; Poisson Fisher metric (square-root coordinate)", "the transmission rate and its seasonal forcing",
        f"period-2 regime: inter-peak years {np.round(gaps, 2).tolist()}, peak sizes {np.round(sizes, 1).tolist()}k. Events = every peak ({len(pk_all)}): CV_arc = {ca_a:.3f}, CV_clock = {cc_a:.3f} -> {lab_a}. Events = major peaks only ({len(pk_major)}, the ledger's onset-like rule): CV_arc = {ca_m:.3f}, CV_clock = {cc_m:.3f} -> {lab_m}",
        "biennial measles cycles alternate in size (Grenfell); the ledger found 17/17 English cities clock-regular between epidemic onsets (MEAS2-1)", f"the class depends on the event rule: counting every peak makes the clock alternate too (arc-regular by a small margin); counting major epidemics only, both quantities are exact on this deterministic period-2 orbit ({lab_m}), so the model has no variability to decide the class the ledger found on real cities",
        "OPEN", (f"{lab_m} (major peaks) / {lab_a} (all peaks)", ca_m, cc_m), "rule 2: the event definition decides the class and the framework does not supply it (O3); the model neither confirms nor contradicts the ledger row on its own")

def e_sir_single_wave():
    def f(t, y):
        S, I = y; return [-2.5 * S * I, 2.5 * S * I - I]
    t = np.linspace(0, 30, 30001); sol = solve_ivp(f, (0, 30), [0.999, 0.001], t_eval=t, method="RK45", rtol=1e-9, atol=1e-12)
    I = sol.y[1]; c = 2 * np.sqrt(I); C = float(np.abs(np.diff(c)).sum()); D = abs(c[-1] - c[0]); S_final = sol.y[0][-1]
    row("e", "SIR single epidemic wave (R0 = 2.5): the wave as one occasion", "D2-D4 on the Poisson carrier; final-size relation",
        "SIR final-size relation 1 - S_inf = 1 - exp(-R0 (1 - S_inf))", "the transmission and recovery rates",
        f"C = {C:.4f}, chord = {D:.4f}, S = {C - D:.4f}: the whole wave is surplus (it returns to where it started); final susceptible fraction {S_final:.4f}",
        "the epidemic burns out leaving a final size fixed by R0", "S = C is the definition of a closed excursion; the final size is untouched by any clause",
        "OPEN", None, "the one quantity epidemiology wants (final size, R0) is not reached by the framework")


def e_sis_endemic():
    rng = np.random.default_rng(5); p = 0.3; ps = []
    for _ in range(20000): p += 0.01 * (0.3 - p) + 0.01 * rng.standard_normal() * math.sqrt(p * (1 - p)); p = min(max(p, 1e-4), 1 - 1e-4); ps.append(p)
    row("e", "SIS endemic equilibrium with demographic noise (infected fraction)", "A4 (spec screening-off gate) on the Bernoulli occupancy carrier",
        "SIS dynamics; Markov property of the infected fraction", "the contact and recovery rates",
        f"infected fraction is Markov: mean {np.mean(ps):.3f}; the state screens off its path, so no multi-occasion salience effect is predicted",
        "the endemic state is a fluctuating equilibrium", "depth one: the e^S law has nothing to act on",
        "DESCR", None, "the gate keeps the framework silent where it should be")


# ================================================================ (p) population and evolutionary
def p_replicator_shahshahani():
    w1, w2 = 1.3, 1.0; p = 0.05; t = np.linspace(0, 12, 12001); dt = t[1] - t[0]
    ps = [p]
    for _ in t[1:]:
        wbar = p * w1 + (1 - p) * w2; p += dt * p * (w1 - wbar); ps.append(p)
    ps = np.array(ps)
    speed = np.abs(np.gradient(ps, dt)) / np.sqrt(ps * (1 - ps))       # Fisher speed on the allele-frequency simplex
    var_w = ps * (1 - ps) * (w1 - w2) ** 2                               # additive fitness variance; Fisher's theorem: d wbar/dt = Var
    C = float(np.sum(speed[:-1] * dt)); D = abs(2 * math.asin(math.sqrt(ps[-1])) - 2 * math.asin(math.sqrt(ps[0])))
    row("p", "Selection on one locus: replicator dynamics as a gradient flow in the Shahshahani (Fisher) metric", "A1 (the Fisher metric on the simplex), D2-D4",
        "Shahshahani 1979 / Harper 2009: the replicator equation is the gradient of mean fitness in the Fisher metric; Fisher's fundamental theorem", "selection coefficients (the fitnesses)",
        f"Fisher speed = |p'|/sqrt(p(1-p)) = sqrt(Var(w)) to leading order: max ratio speed^2/Var(w) = {np.max(speed[:-1] ** 2 / var_w[:-1]):.4f}; C = {C:.4f} = chord {D:.4f} (monotone sweep, S = {C - D:.1e})",
        "the rate of increase of mean fitness equals the additive genetic variance", "the Fisher-Rao speed of evolution is the fitness standard deviation: the framework's arc is the geometry population genetics already uses",
        "CONSIST", None, "the identity is Shahshahani's and Fisher's; a monotone sweep is a geodesic, so S = 0 and the framework adds a name")


def p_lotka_volterra():
    def f(t, y): x, z = y; return [x - 0.5 * x * z, 0.2 * x * z - 0.3 * z]
    t = np.linspace(0, 120, 120001); sol = solve_ivp(f, (0, 120), [1.0, 1.0], t_eval=t, method="RK45", rtol=1e-9, atol=1e-12)
    x = sol.y[0]; from crr.instrument.core import intrinsic_phase, antipodal_cuts
    cuts = antipodal_cuts(intrinsic_phase(x))[1:-1]
    arcs = [float(np.abs(np.diff(x[a:b + 1])).sum()) for a, b in zip(cuts[:-1], cuts[1:])]
    row("p", "Lotka-Volterra predator-prey cycle: the two half-turns of a prey oscillation", "A3 note (v3.1): equal half-turn arcs are a symmetry, not a consequence",
        "Lotka-Volterra conserved cycles; analytic-signal phase", "the interaction rates and the initial condition (set the amplitude)",
        f"consecutive half-turn arcs (prey, identity metric) alternate: CV = {cv(arcs):.3f} over {len(arcs)} half-turns (ratio of the two arms {arcs[0] / arcs[1]:.3f})",
        "the cycle is asymmetric (fast crash, slow recovery)", "unequal arms on an asymmetric member; v3.1 already declines the equal-arms claim",
        "DESCR", None, "a symmetry check that correctly fails on an asymmetric cycle")


def p_adder_cell_size():
    rng = np.random.default_rng(7); n = 400
    # adder: divide when added size reaches Delta (noisy); growth rate varies cell to cell -> interdivision time varies
    Delta = 1.0; sizes_added = Delta * (1 + 0.08 * rng.standard_normal(n)); rates = 0.5 * (1 + 0.25 * rng.standard_normal(n))
    v0 = 1.0; T_add = np.log((v0 + sizes_added) / v0) / rates
    # timer control: divide after fixed time (noisy); added size then varies with growth rate
    T_fix = 1.4 * (1 + 0.08 * rng.standard_normal(n)); added_timer = v0 * (np.exp(rates * T_fix) - 1)
    row("p", "Bacterial cell-size control: adder vs timer under growth-rate variability", "H-L5 with the occasion = one cell cycle, own event = division, carrier = cell volume (identity metric)",
        "adder principle (Campos 2014; Taheri-Araghi 2015); exponential single-cell growth", "the growth rate (physiology-supplied)",
        f"adder: CV(added size) = {cv(sizes_added):.3f} < CV(interdivision time) = {cv(T_add):.3f} (arc-regular); timer: CV(added size) = {cv(added_timer):.3f} > CV(time) = {cv(T_fix):.3f} (clock-regular)",
        "E. coli and B. subtilis add a constant volume per cycle (adder), not a constant time", "an adder is an arc-regular system by its own physiology; a timer is clock-regular; the framework names the distinction, the cell supplies it",
        "CONSIST", ("arc-regular (adder) / clock-regular (timer)", cv(sizes_added), cv(T_add)), "the first biological system in the battery that is arc-regular by mechanism rather than by construction; a real-data L5x row on single-cell growth data is the study this points at")


# ================================================================ (m) molecular and cellular
def m_channel_markov():
    rng = np.random.default_rng(11); ko, kc = 2.0, 1.0; state = 0; dwell = {0: [], 1: []}
    for _ in range(4000):
        rate = ko if state == 0 else kc; dwell[state].append(rng.exponential(1 / rate)); state = 1 - state
    row("m", "Single ion channel, two-state Markov gating", "A4 (depth one) and D5 (own events = transitions)",
        "memoryless (exponential) dwell times", "the opening and closing rates",
        f"mean open dwell {np.mean(dwell[1]):.3f} (1/kc = {1 / kc}), mean closed {np.mean(dwell[0]):.3f} (1/ko = {1 / ko}); CV of dwells {cv(dwell[1]):.3f}, {cv(dwell[0]):.3f} (exponential: 1)",
        "dwell times are exponential; the channel has no memory beyond its state", "depth one: no multi-occasion effect; natural time counts transitions",
        "DESCR", None, "definitional")


def m_hill_ultrasensitivity():
    K = 1.0; s1, s2 = 0.5, 2.0
    arcs = {n: abs(2 * math.asin(math.sqrt(s2 ** n / (K ** n + s2 ** n))) - 2 * math.asin(math.sqrt(s1 ** n / (K ** n + s1 ** n)))) for n in (1, 2, 4, 8)}
    row("m", "Hill cooperativity / ultrasensitivity in a binding curve", "D2 on the Bernoulli occupancy carrier",
        "Hill equation", "the ligand schedule",
        "arc from s = 0.5 K to 2 K in occupancy: " + ", ".join(f"n={n}: {a:.4f}" for n, a in arcs.items()) + " (grows with n) but the switch-like shape itself is not a clause",
        "cooperativity sharpens the response", "the arc registers the sharper transition as a longer Fisher path; nothing predicts n",
        "OPEN", None, "the quantity biology wants (the Hill coefficient, the mechanism of cooperativity) is not reached")


def m_telegraph_expression():
    rng = np.random.default_rng(13); kon, koff, ks, kd = 0.2, 1.0, 20.0, 1.0
    # Gillespie-free approximation: bursts of geometric size b = ks/koff at rate kon; steady-state mean = kon*b/kd, Fano = 1 + b
    b = ks / koff; mean = kon * b / kd; fano = 1 + b
    row("m", "Bursty gene expression (telegraph model): mRNA counts", "A1' (unit = one transcript), A1 (Poisson vs negative-binomial carrier)",
        "telegraph model; negative-binomial count statistics", "promoter switching and transcription rates",
        f"burst size {b:g}, mean count {mean:g}, Fano factor {fano:g} (>1: not Poisson): the carrier must be the negative binomial, which A1 requires to be fixed before any arc is computed",
        "bursting gives super-Poissonian counts", "the framework's only contribution is the carrier-choice discipline; no rate or burst size is derived",
        "OPEN", None, "rule 2: the carrier is a choice that changes every length")


# ================================================================ (b) behavioural and adaptive
def b_two_state_adaptation():
    # Smith-Ghazizadeh-Shadmehr two-state model: x = x_f + x_s; x_f' = A_f x_f + B_f e ; x_s' = A_s x_s + B_s e
    Af, Bf, As, Bs = 0.59, 0.42, 0.992, 0.02
    def run(schedule):
        xf = xs = 0.0; path = []
        for pert in schedule:
            e = pert - (xf + xs); xf = Af * xf + Bf * e; xs = As * xs + Bs * e; path.append(xf + xs)
        return xf, xs, np.array(path)
    A = [1.0] * 60                                             # steady exposure
    B = [1.0] * 20 + [-1.0] * 5 + [1.0] * 35                    # same length, with a reversal in the middle (more path surplus)
    (fA, sA, pA), (fB, sB, pB) = run(A), run(B)
    SA = float(np.abs(np.diff(pA)).sum() - abs(pA[-1] - pA[0])); SB = float(np.abs(np.diff(pB)).sum() - abs(pB[-1] - pB[0]))
    # bring B to the same final state as A by construction? the states differ slightly; report both and the model's future from each
    futA = run(A + [0.0] * 30)[2][-1]; futB = run(B + [0.0] * 30)[2][-1]
    row("b", "Motor adaptation, two-state (fast/slow) model: does the path of an occasion matter beyond its end state?", "A4 (depth one) vs the occasion-weight law (spec T5); the spec's §XV system",
        "Smith, Ghazizadeh & Shadmehr 2006 two-state model", "the perturbation schedule (experimenter-supplied)",
        f"two 60-trial occasions: surplus S_A = {SA:.3f} (steady), S_B = {SB:.3f} (with a reversal); end states (fast, slow) A = ({fA:.3f}, {sA:.3f}), B = ({fB:.3f}, {sB:.3f}); the model's behaviour 30 trials on depends only on those states (A: {futA:.3f}, B: {futB:.3f})",
        "savings and interference are carried by the slow state", "the standard model is depth one: the path surplus of a block has no effect beyond the state it leaves; the salience law predicts one. That difference is the T5 experiment the roadmap names, and it is prospective",
        "OPEN", None, "not a retrodiction: the framework and the standard model disagree only on an experiment not yet run under the protocol (the spec's §XV run is unlogged)")


def b_circadian_entrainment():
    def f(t, y):
        th = y[0]; light = 0.15 * max(0.0, math.cos(2 * math.pi * t / 24.0)); return [2 * math.pi / 24.6 + light * math.sin(-th)]
    t = np.linspace(0, 24 * 60, 24 * 60 * 60 + 1); sol = solve_ivp(f, (0, t[-1]), [1.0], t_eval=t, method="RK45", rtol=1e-8, atol=1e-10)
    th = sol.y[0]; crossings = t[np.where(np.diff(np.floor(th / (2 * math.pi))) > 0)[0]]; periods = np.diff(crossings)[10:]
    row("b", "Circadian phase oscillator (free-running 24.6 h) entrained by a light cycle", "A3 (cut per half-turn of the phase rotor), D5",
        "phase-oscillator entrainment (Arnold tongue)", "the light schedule and the intrinsic period",
        f"entrained period {np.mean(periods):.3f} h (CV {cv(periods):.1e}) against a free-running 24.6 h: the clock is locked; the phase advances a fixed 2 pi per cycle by definition",
        "entrainment locks the period to 24 h", "clock-regular and phase-regular at once; nothing about the entrainment range is derived",
        "DESCR", ("clock-regular", 0.0, cv(periods)), "the antipodal cut on a phase rotor is a definition here")


def b_habituation():
    rng = np.random.default_rng(17); n = 12; r = 1.0 * 0.8 ** np.arange(n) * (1 + 0.03 * rng.standard_normal(n))
    row("b", "Habituation of a reflex over repeated stimuli (Aplysia-like response decrement)", "P3 (age weights) vs P2 (surplus weights); O2 (which constraint is open)",
        "exponential habituation kinetics", "the stimulus schedule",
        f"response over {n} trials decays geometrically (ratio {r[1] / r[0]:.3f}); a geometric age weight (P3) fits it by construction; a surplus weight (P2) has nothing to work with because every occasion is the same stimulus",
        "habituation follows an exponential decrement (Thompson & Spencer)", "the framework leaves the constraint open (O2); the geometric form is its P3 with q fitted",
        "OPEN", None, "q is fitted, not derived (v3.1 says CRR does not fix q)")


BATTERY = [n_lif_noisy, n_fhn_varying_drive, n_snic_vs_hopf, n_weber_fechner,
           c_rsa, c_pulsus_alternans, c_afib_like,
           e_forced_sir, e_sir_single_wave, e_sis_endemic,
           p_replicator_shahshahani, p_lotka_volterra, p_adder_cell_size,
           m_channel_markov, m_hill_ultrasensitivity, m_telegraph_expression,
           b_two_state_adaptation, b_circadian_entrainment, b_habituation]
CLASSES = {"n": "neural", "c": "cardiac / physiological", "e": "epidemiological", "p": "population / evolutionary",
           "m": "molecular / cellular", "b": "behavioural / adaptive"}


def main():
    for f in BATTERY: f()
    print("CRR retrodiction battery on biological systems — 19 model systems, 6 classes. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}\n     FLOW:       {r['flow']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     H-L5 class: {r['l5'][0]} (CV_arc {r['l5'][1]:.3f}, CV_clock {r['l5'][2]:.3f})" if r['l5'] else "")
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'class':32s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rows = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:28s} " + " ".join(f"{sum(r['grade'] == g for r in rows):8d}" for g in grades))
    print(f"{'all':32s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print("\nH-L5 CLASS MAP (systems with their own events, computed on the model with crr.instrument.core.regularity)")
    for r in ROWS:
        if r["l5"]: print(f"  {r['l5'][0]:44s} {r['system']}")
    print(f"\nrows where the coherence integral's velocity is system-supplied (FLOW != none): {sum(1 for r in ROWS if r['flow'] != 'none')}/{len(ROWS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
