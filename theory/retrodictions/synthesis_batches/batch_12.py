"""Synthesis batch 12: rows 56-60 of QUEUE.md (prompt-log entry 61). Bio battery [5] respiratory sinus arrhythmia (RR
interval modulated by breathing, pulse shape fixed; DESCR); [6] pulsus alternans (fixed rate, alternating amplitude;
DESCR); [10] SIS endemic equilibrium with demographic noise (DESCR); [11] selection on one locus, replicator dynamics as
a Shahshahani gradient flow (CONSIST); [12] Lotka-Volterra predator-prey cycle, the two half-turns of a prey oscillation
(DESCR). All five source rows are in theory/retrodictions/bio_retrodictions.txt; their models are re-implemented here
(nothing imported from the battery scripts). Deterministic (fixed seeds, fixed grids, explicit RK4 and Euler-Maruyama);
no data file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_12.py
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/bio_retrodictions.txt"


def _word(cond, yes, no):
    return yes if cond else no


def _agree(a, b, tol=TOL_G):
    return _word(rel(a, b) <= tol, "agree", "differ")


def _tv(x):
    return float(np.abs(np.diff(np.asarray(x, float))).sum())


# ---------------------------------------------------------------- 56 [5] respiratory sinus arrhythmia: both respiratory modulations
def _pulse_train(periods, amps, fs):
    """The source row's pulse train (two Gaussians per beat, the second the dicrotic bump), amplitude A per beat."""
    x, on = [], []
    for T, A in zip(periods, amps):
        n = int(round(T * fs)); tt = np.arange(n) / fs; on.append(len(x))
        x.extend(A * (np.exp(-((tt - 0.12) / 0.04) ** 2) + 0.35 * np.exp(-((tt - 0.32) / 0.08) ** 2)))
    return np.array(x), np.array(on), 1.0 / fs


def r1():
    n, T0, a, fs, f_resp = 60, 0.9, 0.08, 2000, 0.2                # the source's 60 beats, RR = 0.90 +/- 0.08 s, one breath per 5 beats
    k = np.arange(n); s_rr = np.sin(2 * np.pi * f_resp * k)        # respiratory phase sampled at the beats
    s_amp = np.sin(2 * np.pi * f_resp * k + 0.3)                    # the amplitude modulation, 0.3 rad behind the RR modulation
    depth_f = a / T0                                                # RSA (RIFV) depth, fractional
    grid = (0.0, 0.04, depth_f, 0.14)                               # RIAV depth b: none, below, at and above the RSA depth
    res = []
    for b in grid:
        x, on, dt = _pulse_train(T0 + a * s_rr, 1.0 + b * s_amp, fs)
        r = regularity(x, on, sigma=1.0, dt=dt, n_boot=500)         # inclusive: the pulse returns to baseline, no reset jump at the onset
        idx = r["cv_clock"] / r["cv_arc"] if r["cv_arc"] > 1e-12 else math.inf   # CV(arc) at round-off: the index is undefined
        pred = depth_f / b if b > 0 else math.inf                    # the domain's ratio of the two modulation depths
        res.append((b, r, idx, pred))
    b1, r1_, idx1, pred1 = res[1]
    crr, null = r1_["cv_arc"], r1_["cv_amp"]
    dom = b1 * float(np.std(s_amp, ddof=1)) / float(np.mean(1.0 + b1 * s_amp))   # the RIAV depth's own CV: the domain's number for CV(arc)
    idx_ok = all(rel(idx, pred) <= 0.01 for b, r, idx, pred in res[1:])
    def cls(r):
        d = r["cv_arc"] - r["cv_clock"]
        return "tie" if abs(d) < 1e-3 else _word(d < 0, "arc-regular", "clock-regular")
    cls_ok = cls(res[1][1]) == "arc-regular" and cls(res[3][1]) == "clock-regular" and cls(res[2][1]) == "tie"
    check = idx_ok and cls_ok
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("bio",
        f"Heartbeat under breathing as a fixed-shape pulse train with the two respiratory modulations the pulse literature names: RR-interval (frequency) modulation of depth a/T0 = {depth_f:.4f} (the source's RSA, 0.90 +/- 0.08 s) and pulse-amplitude modulation of depth b, {n} beats at {fs} Hz, onsets as the system's own events",
        source=f"{SRC} [5] (DESCR)",
        Q="under breathing the heartbeat is in H-L5's arc-regular class iff the respiratory frequency-modulation depth (RSA) exceeds the respiratory amplitude-modulation depth: CV(clock)/CV(arc) = (a/T0)/b, because on a fixed-shape pulse the arc of a beat is its amplitude",
        ingredient="H-L5 (the class claim: arc against clock between own events), D5 [M] (occasion = onset to onset), D2 with the identity metric (arc = total variation of the trace, SCOPE.md section 2)",
        null="H-L5's control (i): the peak-to-peak amplitude of the occasion",
        domain="the PPG-derived-respiration literature's three respiratory modulations (frequency RIFV, amplitude RIAV, baseline RIIV; Charlton et al. 2016 review): RSA depth and pulse-amplitude modulation depth are both measured quantities, and their ratio is the class index",
        numbers="; ".join(f"b = {b:.4f}: CV(arc) = {r['cv_arc']:{'.1e' if r['cv_arc'] < 1e-6 else '.4f'}}, CV(clock) = {r['cv_clock']:.4f}, CV(amplitude) = {r['cv_amp']:{'.1e' if r['cv_amp'] < 1e-6 else '.4f'}}, class index CV(clock)/CV(arc) " + (f"= {idx:.4f} (depth ratio (a/T0)/b = {pred:.4f})" if b > 0 else "undefined (no amplitude modulation: the arc is constant to round-off)") + f", CI95 of CV(arc) - CV(clock) [{r['ci95'][0]:.4f}, {r['ci95'][1]:.4f}]: {cls(r)}" for b, r, idx, pred in res),
        tg=f"CV(arc) {crr:.4f} vs null CV(amplitude) {null:.4f} (b = {b1:g}): {_agree(crr, null)}",
        tn=f"the amplitude-modulation depth's own CV gives {dom:.4f} for CV(arc): the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"class index within 1 % of the depth ratio at every b > 0 ({_word(idx_ok, 'yes', 'no')}) and the class flips from arc-regular below a/T0 through a tie at a/T0 to clock-regular above it ({_word(cls_ok, 'yes', 'no')}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"on a fixed-shape pulse the arc of a beat is its amplitude (T-G: the two CVs agree to {rel(crr, null):.1e}), so H-L5 is its own control (i) and the class is decided by which of the domain's two respiratory modulations is deeper; "
                 f"the source row's arc-regular verdict is the b = 0 corner of that ratio (RSA alone), and the crossover at b = a/T0 = {depth_f:.4f} is the domain's ratio of modulation depths, not CRR's; the pendulum row (batch 03 row 4) said the same for a one-dimensional swing"),
        weakness="a model waveform with the two modulations sinusoidal at the breathing rate; real pulses also change shape with breathing (a third modulation the domain names, baseline/intensity), which would break arc = amplitude and is the case a prereg on records (study CARD) would meet; the amplitude modulation's phase lag (0.3 rad) does not enter the CVs",
        elegance="Breathing bends the heartbeat two ways: it stretches the gaps between beats and it changes the size of the beats. Whichever bend is bigger decides which of the two clocks the heart keeps: no knobs, a ratio of two depths.",
        child="When you breathe in and out, your heartbeats get a little closer together and further apart, and each beat also gets a little bigger and smaller. If the timing wobbles more than the size, then the size is the steady thing; if the size wobbles more, the timing is the steady thing.")


# ---------------------------------------------------------------- 57 [6] pulsus alternans: A6 regeneration inside the restitution map
def r2():
    Amax, alpha, tau = 300.0, 200.0, 60.0                            # APD restitution F(DI) = Amax - alpha exp(-DI/tau), ms (Nolasco-Dahlen form)
    F = lambda D: Amax - alpha * math.exp(-max(D, 0.0) / tau)
    Fp = lambda D: alpha / tau * math.exp(-D / tau)

    def fixed_point(BCL):
        return brentq(lambda A: F(BCL - A) - A, 1.0, BCL - 1e-9, xtol=1e-13)

    def multiplier(BCL, q, n=400, eps=1e-6):
        """Renormalised tangent iteration of the memory map (a_n, M_n): the dominant multiplier of the 1:1 fixed point."""
        A = fixed_point(BCL); Ds = BCL - A
        da, dM = eps, 0.0; g = []
        for i in range(n):
            a, M = A + da, Ds + dM
            D = BCL - a; M = (1 - q) * D + q * M; a = F(M)          # A6/P3: the DI the next APD responds to is the age-weighted mean of settled DIs
            da, dM = a - A, M - Ds
            nrm = math.hypot(da, dM); g.append(nrm / eps)
            da, dM = da / nrm * eps, dM / nrm * eps
        return float(np.exp(np.mean(np.log(g[n // 2:]))))

    def steady_alternans(BCL, q, n=20000):
        A = fixed_point(BCL); M = BCL - A; a = A + 1e-3; amps = []
        for i in range(n):
            D = BCL - a; M = (1 - q) * D + q * M; a_new = F(M); amps.append(abs(a_new - a)); a = a_new
        return float(np.mean(amps[-200:]))

    res = []
    for q in (0.0, 0.2, 0.4):
        lo, hi = 105.0, 400.0
        for _ in range(45):
            mid = 0.5 * (lo + hi)
            if multiplier(mid, q) > 1.0: lo = mid
            else: hi = mid
        Bc = 0.5 * (lo + hi); A = fixed_point(Bc); s = Fp(Bc - A)
        res.append((q, Bc, A, Bc - A, s, (1 + q) / (1 - q), steady_alternans(0.98 * Bc, q), steady_alternans(1.02 * Bc, q)))
    s0, s2, s4 = res[0][4], res[1][4], res[2][4]
    crr, null, dom = s4, s0, 1.0
    check = all(rel(s, pred) <= 0.01 and below > 1.0 and above < 1e-6 for q, Bc, A, D, s, pred, below, above in res)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("bio",
        f"Cardiac alternans in the APD-restitution map A(n+1) = F(DI(n)), DI(n) = BCL - A(n), F(DI) = {Amax:g} - {alpha:g} exp(-DI/{tau:g}) ms, with A6 regeneration: the diastolic interval the next beat responds to is the P3 age-weighted mean of the settled diastolic intervals, M(n) = (1 - q) DI(n) + q M(n - 1)",
        source=f"{SRC} [6] (DESCR)",
        Q="regeneration memory raises the restitution-slope threshold for alternans from 1 to (1 + q)/(1 - q): the 1:1 rhythm's multiplier is q - s(1 - q), so period doubling needs s > (1 + q)/(1 - q), and the onset moves to faster pacing",
        ingredient="A6 (the next occasion seeded from settled occasions, bounded strength) with P3 (geometric age weights q^k), D5 (occasion = one beat); on the 1-D duration carrier the Fisher-Rao Frechet mean is the weighted mean",
        null="q = 0: the memoryless restitution map, where each beat responds to the last diastolic interval only",
        domain="Nolasco-Dahlen 1968 / Guevara et al. 1984: alternans appears where the restitution slope F'(DI*) exceeds 1",
        numbers="; ".join(f"q = {q:g}: onset BCL = {Bc:.2f} ms (A* = {A:.2f}, DI* = {D:.2f}), slope at onset {s:.4f} (predicted (1 + q)/(1 - q) = {pred:.4f}), steady alternans amplitude |A(n+1) - A(n)| at 0.98 x onset {below:.2f} ms and at 1.02 x onset {above:.1e} ms" for q, Bc, A, D, s, pred, below, above in res),
        tg=f"threshold slope {crr:.4f} (q = 0.4) vs null {null:.4f} (q = 0): {_agree(crr, null)}",
        tn=f"the restitution criterion gives {dom:.4f}: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"onset slope within 1 % of (1 + q)/(1 - q) at every q, alternans present 2 % below the onset and absent 2 % above it: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"integrated with the domain's own map, the regeneration axiom makes a definite, checkable statement the memoryless criterion does not: memory over settled beats damps the beat-to-beat alternation, the threshold slope rises from {s0:.4f} to {s2:.4f} (q = 0.2) and {s4:.4f} (q = 0.4), and the pacing interval at onset falls from {res[0][1]:.1f} to {res[2][1]:.1f} ms; "
                 f"the label is a candidate only: whether the domain's memory-restitution models already contain this threshold is the expert's question (protocol section 4), and the source row's clock-regular class is untouched (the pacing is fixed by construction)"),
        weakness="q is not fixed by CRR (P3), so the row prints a grid; any exponential-kernel memory on the diastolic interval gives the same multiplier, so the CRR content is the weights' geometric shape and the bounded strength, not the existence of memory (the same reading of A6 as synthesis row 8, the adder); the domain has memory-restitution models (Otani-Gilmour 1997; Fox et al. 2002; Tolkacheva et al. 2003, by name and year only, not fetched here, R10) in which memory can stabilise or destabilise the 1:1 rhythm, so the expert's answer to question 1 may be yes",
        elegance="A beat that copies only the beat before it can be pushed into big-small-big-small forever; a beat that takes the average of a few settled beats smooths the see-saw out. The rule is one sentence: remember a little, and alternation needs a steeper push.",
        child="Imagine each heartbeat deciding how long to last by looking only at the one before it: a small wobble can bounce back and forth, long-short-long-short, without stopping. If each beat instead looks at a few earlier beats and takes their average, the wobble gets evened out, and it takes a much harder push to make the heart see-saw.")


# ---------------------------------------------------------------- 58 [10] SIS endemic equilibrium: the surplus weight on a diffusion carrier
def r3():
    lam, p_star, sg = 0.01, 0.3, 0.01                                # the source's per-step model as an SDE: dp = lam (p* - p) dt + sg sqrt(p(1-p)) dW
    dt, n = 0.1, 200000                                              # fine grid; the coarse grid (every 10th sample, dt = 1) is the source's grid
    rng = np.random.default_rng(5)
    p = np.empty(n + 1); p[0] = p_star; xi = rng.standard_normal(n) * math.sqrt(dt)
    for i in range(n):                                               # Euler-Maruyama, clipped as the source clips
        v = p[i]; p[i + 1] = min(max(v + lam * (p_star - v) * dt + sg * math.sqrt(v * (1 - v)) * xi[i], 1e-4), 1 - 1e-4)
    sig_p = sg * math.sqrt(p_star * (1 - p_star) / (2 * lam))        # the linear-noise stationary spread (van Kampen)

    def events(x, level, band):                                      # own events [M]: up-crossings of p* after an excursion one spread below it
        ev, armed = [], False
        for i in range(1, len(x)):
            if x[i] < level - band: armed = True
            if armed and x[i - 1] < level <= x[i]: ev.append(i); armed = False
        return np.asarray(ev)

    res = {}
    for sub in (1, 10):
        x = p[::sub]; d = dt * sub; ev = events(x, p_star, sig_p)
        th = 2.0 * np.arcsin(np.sqrt(x))                             # the Fisher coordinate of the Bernoulli carrier (P7 on two classes)
        rt = regularity(th, ev, sigma=1.0, dt=d, n_boot=2000)        # inclusive: no reset jump sits at an up-crossing
        rp = regularity(x, ev, sigma=1.0, dt=d, n_boot=2000)
        C = np.array([_tv(th[a:b + 1]) for a, b in zip(ev[:-1], ev[1:])]); Cs = np.abs(th[ev[1:]] - th[ev[:-1]]); S = C - Cs; T = np.diff(ev) * d
        res[sub] = dict(n=len(C), rt=rt, rp=rp, cvS=cv(S), cvT=cv(T), corr=float(np.corrcoef(S, T)[0, 1]), chord_frac=float((Cs / C).mean()),
                        kappa=float(C.sum() / T.sum()), cv_ratio=cv(S / T), per_sample=float(C.sum() / np.diff(ev).sum()), lln=sg * math.sqrt(d) * math.sqrt(2 / math.pi), meanT=float(T.mean()))
    f, c = res[1], res[10]
    crr, null, dom = f["cvS"], f["cvT"], f["cvT"]
    ratio = f["kappa"] / c["kappa"]
    check = f["chord_frac"] < 0.01 and f["corr"] > 0.99 and c["corr"] > 0.99 and rel(ratio, math.sqrt(10.0)) <= 0.05
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    def cls(r):
        lo, hi = r["ci95"]
        return "CI includes 0" if lo <= 0.0 <= hi else _word(r["cv_arc"] < r["cv_clock"], "arc-regular (CI excludes 0)", "clock-regular (CI excludes 0)")
    return make_row("bio",
        f"SIS endemic equilibrium with demographic noise (the source's model as an SDE: relaxation {lam:g}, endemic fraction {p_star:g}, noise {sg:g} sqrt(p(1-p))), own events [M] = up-crossings of the endemic level after an excursion one stationary spread ({sig_p:.4f}) below it; Fisher coordinate theta = 2 arcsin sqrt(p); Euler-Maruyama at dt = {dt:g} and the same path at dt = {10 * dt:g} (the source's grid)",
        source=f"{SRC} [10] (DESCR)",
        Q="on the endemic carrier the surplus weight law P2 reduces to a clock weight: every return occasion has zero chord, so its surplus is its whole arc, and the arc of a diffusion is the occasion's duration times a rate the sampling step sets, so exp(beta S_m) = exp(beta kappa Delta t_m) and the settled past is weighted by elapsed time only",
        ingredient="P2 (occasion weights pi_m ∝ exp(beta S_m)) with D4/D5 (S_m = C_m - C*_m per return occasion); the diffusion-carrier theorem (cognitive-collective battery row 1, AGENT_LOG 21; batch 06 row 5) applied before any arc-clock reading",
        null="the clock weight exp(beta' Delta t_m): the occasion's duration, which the domain's renewal description already has",
        domain="the law of large numbers over the increments of a diffusion: E[C | Delta t] = Delta t E|d theta|/dt, so CV(S) = CV(Delta t) at leading order; in the arcsine (Fisher) coordinate the demographic noise of a two-class carrier is homogeneous (Fisher's angular transformation), so the arc per sample is the constant sigma sqrt(dt) sqrt(2/pi)",
        numbers=(f"dt = {dt:g}: {f['n']} return occasions (mean {f['meanT']:.1f} time units): CV(S) = {f['cvS']:.4f}, CV(clock) = {f['cvT']:.4f}, corr(S, Delta t) = {f['corr']:.4f}, mean chord/arc = {f['chord_frac']:.1e}, CV(S/Delta t) = {f['cv_ratio']:.4f}, arc rate kappa = {f['kappa']:.5f} per unit time, arc per sample {f['per_sample']:.5f} rad (LLN {f['lln']:.5f}); "
                 f"theta-arc H-L5 reading: CV(C) = {f['rt']['cv_arc']:.4f} vs CV(clock) = {f['rt']['cv_clock']:.4f}, CI95 [{f['rt']['ci95'][0]:.4f}, {f['rt']['ci95'][1]:.4f}] ({cls(f['rt'])}); identity-metric (p-units) reading: CV(C) = {f['rp']['cv_arc']:.4f}, CI95 [{f['rp']['ci95'][0]:.4f}, {f['rp']['ci95'][1]:.4f}] ({cls(f['rp'])}); "
                 f"dt = {10 * dt:g}: {c['n']} occasions: CV(S) = {c['cvS']:.4f}, CV(clock) = {c['cvT']:.4f}, corr = {c['corr']:.4f}, CV(S/Delta t) = {c['cv_ratio']:.4f}, kappa = {c['kappa']:.5f}, arc per sample {c['per_sample']:.5f} (LLN {c['lln']:.5f}); theta-arc CI95 [{c['rt']['ci95'][0]:.4f}, {c['rt']['ci95'][1]:.4f}] ({cls(c['rt'])}), p-units CI95 [{c['rp']['ci95'][0]:.4f}, {c['rp']['ci95'][1]:.4f}] ({cls(c['rp'])}); "
                 f"arc-rate ratio between the grids {ratio:.3f} (sqrt(10) = {math.sqrt(10):.3f})"),
        tg=f"CV(S) {crr:.4f} vs null CV(clock) {null:.4f}: {_agree(crr, null)}; on the coarse grid {c['cvS']:.4f} vs {c['cvT']:.4f}: {_agree(c['cvS'], c['cvT'])}",
        tn=f"the law of large numbers gives CV(S) = CV(clock) = {dom:.4f} at leading order, and the arc per sample {f['per_sample']:.5f} against Fisher's homogeneous-noise constant {f['lln']:.5f}: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"chord below 1 % of the arc, corr(S, Delta t) > 0.99 on both grids, arc rate scaling as sqrt(10) within 5 %: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the source row kept CRR silent by the spec's screening gate (a Markov state has no path to weight); the synthesis says why the weight law would have nothing to act on even without that gate: on this carrier S is Delta t times {f['kappa']:.5f} (fine grid) or {c['kappa']:.5f} (the source's grid), a rate that belongs to the sampling step ({ratio:.3f} between grids), so beta per unit surplus is beta kappa per unit time and P2 is the clock weight it was meant to replace; "
                 f"the identity-metric arc carries a {rel(f['rp']['cv_arc'], f['rp']['cv_clock']):.3f} excursion-depth signal (its CI {_word(f['rp']['ci95'][0] <= 0.0 <= f['rp']['ci95'][1], 'includes', 'excludes')} 0) that the Fisher coordinate {_word(f['rt']['ci95'][0] <= 0.0 <= f['rt']['ci95'][1], 'removes', 'does not remove')} (theta-arc CI {_word(f['rt']['ci95'][0] <= 0.0 <= f['rt']['ci95'][1], 'includes', 'excludes')} 0), which is the variance-stabilising property of the arcsine transform, statistics' own"),
        weakness="the source's model has no population size, so A1' (one infection as the step) cannot be applied and the unit is one radian of theta (the CVs are unit-free); the return event needs a band (one stationary spread) that is the domain's linear-noise scale, not a CRR quantity; a prereg on incidence data would have to name a smoothing scale or the Poisson-rate carrier (SCOPE.md P6) before any arc could be read",
        elegance="",
        child="")


# ---------------------------------------------------------------- 59 [11] one locus with selection: A6 regeneration as a seed bank, two readings
def r4():
    N, K, R, G, burn, s_sel = 500, 25, 20000, 2000, 500, 0.05

    def decay_rate(q, frechet, seed=0):
        """Loss of heterozygosity per generation when the next generation is drawn from the A6 seed of the settled generations."""
        rng = np.random.default_rng(seed)
        hist = np.full((K, R), 0.5); w = (1 - q) * q ** np.arange(K); w /= w.sum()
        H = np.empty(G)
        for g in range(G):
            if frechet:                                              # reading (i): A6 as written, the Fisher-Rao Frechet mean on the Bernoulli family (mean in theta = 2 arcsin sqrt p)
                m = np.sin((w[:, None] * 2.0 * np.arcsin(np.sqrt(hist))).sum(0) / 2.0) ** 2
            else:                                                    # reading (ii): the mixture, the domain's seed bank (mean in p)
                m = (w[:, None] * hist).sum(0)
            pn = rng.binomial(2 * N, np.clip(m, 0.0, 1.0)) / (2 * N)   # the weighted mean of fixed cohorts rounds to 1 + 2e-16
            hist = np.roll(hist, 1, axis=0); hist[0] = pn
            H[g] = float(np.mean(pn * (1 - pn)))
        t = np.arange(G); ok = H > 0
        return -float(np.polyfit(t[burn:][ok[burn:]], np.log(H[burn:][ok[burn:]]), 1)[0])

    def sweep_time(q, frechet, p0=0.05, p1=0.95):
        """Deterministic selection (viability 1 + s on the seeded generation): generations from p0 to p1."""
        w = (1 - q) * q ** np.arange(K); w /= w.sum(); hist = np.full(K, p0); t = 0
        while True:
            m = float(np.sin((w * 2.0 * np.arcsin(np.sqrt(hist))).sum() / 2.0) ** 2) if frechet else float((w * hist).sum())
            pn = m * (1 + s_sel) / (1 + s_sel * m); t += 1
            hist = np.roll(hist, 1); hist[0] = pn
            if pn >= p1: return t

    rate0 = decay_rate(0.0, False); t0 = sweep_time(0.0, False)
    rows = {}
    for q in (0.3, 0.5):
        rF, rM = decay_rate(q, True), decay_rate(q, False); tF, tM = sweep_time(q, True), sweep_time(q, False)
        kaj = -math.log(1.0 - (1 - q) ** 2 / (2 * N))                # Kaj-Krone-Lascoux 2001: N_e = N E[B]^2 with E[B] = 1/(1 - q) under P3 weights
        rows[q] = dict(rF=rF, rM=rM, tF=tF, tM=tM, kaj=kaj, effM=(rate0 / rM) * (t0 / tM), effF=(rate0 / rF) * (t0 / tF))
    q = 0.5; d = rows[q]
    internal = rel(d["rF"], d["rM"]) > TOL_G
    out = outcome(internal=internal)
    worst = max([rel(rate0, -math.log(1.0 - 1.0 / (2 * N)))] + [rel(r_["rM"], r_["kaj"]) for r_ in rows.values()])   # the largest gap between a mixture-reading rate and its theorem
    return make_row("bio",
        f"One locus in a Wright-Fisher population (N = {N} diploids) with A6 regeneration: the next generation is drawn from the P3 age-weighted seed of the settled generations (weights q^k over age k) instead of the last one; drift measured as the decay rate of heterozygosity ({R} replicate loci, {G} generations, fitted after {burn}); selection s = {s_sel:g} in the deterministic limit as the sweep time from 0.05 to 0.95",
        source=f"{SRC} [11] (CONSIST)",
        Q="A6 with P3 weights makes one locus a seed bank: drift slows by (1 - q)^2 (N_e = N/(1 - q)^2) and selection by (1 - q), so the efficacy of selection relative to drift, N_e s_e, rises by 1/(1 - q); the two readings of the A6 seed (the Fisher-Rao Frechet mean A6 names, and the mixture the domain's seed bank is) must agree for Q to be checkable",
        ingredient="A6 (the next occasion seeded from settled occasions at bounded strength) with P3 (geometric age weights), D5 [M] (occasion = one generation); A1 on the Bernoulli family (the source's Shahshahani metric) fixes the Frechet mean as the mean in theta = 2 arcsin sqrt(p)",
        null="q = 0: the plain Wright-Fisher generation, seeded from the last generation only",
        domain="Kaj, Krone and Lascoux 2001 (weak seed bank): the coalescent runs at rate 1/E[B]^2, N_e = N E[B]^2, B the age of the parent generation; under P3 weights E[B] = 1/(1 - q); the selection factor (1 - q) follows from the deterministic recursion m(t+1) = m(t) + (1 - q) s m(1 - m) + O(s^2)",
        numbers=(f"q = 0: decay rate {rate0:.3e} per generation (1/(2N) = {1 / (2 * N):.3e}), sweep time {t0} generations; " +
                 "; ".join(f"q = {qq:g}: decay rate under the Frechet seed {r_['rF']:.3e}, under the mixture seed {r_['rM']:.3e} (Kaj-Krone-Lascoux (1 - q)^2/(2N) = {r_['kaj']:.3e}; mixture/theorem = {r_['rM'] / r_['kaj']:.4f}, Frechet/theorem = {r_['rF'] / r_['kaj']:.4f}); sweep time {r_['tF']} (Frechet) and {r_['tM']} (mixture) generations against t0/(1 - q) = {t0 / (1 - qq):.1f}; efficacy ratio N_e s_e/(N s) from the measured rates: mixture {r_['effM']:.3f}, Frechet {r_['effF']:.3f} (1/(1 - q) = {1 / (1 - qq):.3f})" for qq, r_ in rows.items()) +
                 f"; relative difference between the two readings' drift rates at q = 0.5: {rel(d['rF'], d['rM']):.4f} (TOL_G {TOL_G:g})"),
        tg=f"reading (i) Frechet-seed drift rate {d['rF']:.3e} vs reading (ii) mixture-seed drift rate {d['rM']:.3e} (q = 0.5): {_agree(d['rF'], d['rM'])} (the ingredient has two values on the domain)",
        tn=f"the seed-bank theorem gives {d['kaj']:.3e} for the mixture reading (observed {d['rM']:.3e}, relative difference {rel(d['rM'], d['kaj']):.4f}) and nothing for the Frechet reading",
        tc="not reached: the two readings of the A6 seed must agree before Q can be checked",
        out=out,
        reading=(f"the mixture reading is the domain's seed bank and the domain has its theorem (drift rate {_word(rel(d['rM'], d['kaj']) <= worst, 'within', 'outside')} {100 * worst:.1f} % of Kaj-Krone-Lascoux at q = 0.5, selection slowed by {t0 / d['tM']:.3f} against 1 - q = 0.5); the Frechet reading, which is what A6 says and what the source's Fisher metric on the simplex demands, is not a mixture: averaging in the arcsine coordinate pulls the seed toward the nearer boundary whenever the settled generations differ, an extra drift toward fixation that raises the loss of heterozygosity by {d['rF'] / d['rM']:.2f} x at q = 0.5 (selection is slowed almost identically, {d['tF']} against {d['tM']} generations, because the deterministic cohorts barely differ); "
                 f"which of the two A6 is has to be fixed before the domain can be asked, and the fix is a theory choice (v3.2), not an estimator choice; the source row's own content (Fisher speed = fitness standard deviation, S = 0 on a monotone sweep) is information geometry's and synthesis row 6 already read the replicator flow"),
        weakness=f"the seed-bank theorem is asymptotic in N and the fit uses {G - burn} generations after a burn-in, so the mixture reading is compared at the {100 * worst:.1f} % level (the largest gap between a mixture-reading rate and its theorem, q = 0 included), not the 1 % of TOL_N; the boundary pull of the Frechet seed scales with the spread of the settled generations (order 1/N per generation), so the factor between the readings depends on N and q and only its sign is general; citations by name and year only, not fetched here (R10)",
        elegance="",
        child="")


# ---------------------------------------------------------------- 60 [12] Lotka-Volterra prey oscillation: three readings of the A3 rotor
def r5():
    h, n_per = 0.002, 40
    x, y = 1.0, 1.0; T_guess = 12.4; n = int(n_per * T_guess / h)
    xs = np.empty(n + 1); xs[0] = x
    f = lambda x, y: (x - 0.5 * x * y, 0.2 * x * y - 0.3 * y)       # the source's rates
    for i in range(n):                                               # fixed-grid RK4
        k1 = f(x, y); k2 = f(x + 0.5 * h * k1[0], y + 0.5 * h * k1[1]); k3 = f(x + 0.5 * h * k2[0], y + 0.5 * h * k2[1]); k4 = f(x + h * k3[0], y + h * k3[1])
        x += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6; y += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6; xs[i + 1] = x
    dx = np.diff(xs); mins = np.where((dx[:-1] < 0) & (dx[1:] >= 0))[0] + 1; maxs = np.where((dx[:-1] > 0) & (dx[1:] <= 0))[0] + 1
    T = float(np.mean(np.diff(mins))) * h; T_sd = float(np.std(np.diff(mins))) * h
    ph = intrinsic_phase(xs)
    adv = float((ph[mins[len(mins) // 2 + 1]] - ph[mins[len(mins) // 2]]) / (2 * math.pi))
    def hilbert_split(start):
        cuts = antipodal_cuts(ph, start=int(start))[:11]              # ten occasions from the middle of the record
        fr = np.diff(cuts) * h / T; arcs = np.array([_tv(xs[a:b + 1]) for a, b in zip(cuts[:-1], cuts[1:])])
        return fr, arcs
    fr_min, arc_min = hilbert_split(mins[len(mins) // 2]); fr_max, arc_max = hilbert_split(maxs[len(maxs) // 2])
    mm = np.sort(np.concatenate([mins, maxs])); i0 = len(mm) // 2 - (len(mm) // 2) % 2
    fr_ext = np.diff(mm[i0:i0 + 5]) * h / T; arc_ext = np.array([_tv(xs[a:b + 1]) for a, b in zip(mm[i0:i0 + 4], mm[i0 + 1:i0 + 5])])
    first_is_max = bool(mm[i0] in set(maxs.tolist()))                 # the interval that opens at a prey maximum is the crash (max -> min)
    f_crash, f_recov = (float(fr_ext[0]), float(fr_ext[1])) if first_is_max else (float(fr_ext[1]), float(fr_ext[0]))
    half = int(round(T / 2 / h)); s0 = int(mins[len(mins) // 2]); ci = [s0 + k * half for k in range(5)]
    arc_clk = np.array([_tv(xs[a:b + 1]) for a, b in zip(ci[:-1], ci[1:])])
    f_i, f_ii, f_ii_max, f_iii = 0.5, float(fr_min[0]), float(fr_max[0]), float(fr_ext[0])
    internal = rel(f_i, f_ii) > TOL_G
    out = outcome(internal=internal)
    return make_row("bio",
        f"Lotka-Volterra predator-prey cycle (the source's rates: prey 1 - 0.5 y, predator 0.2 x - 0.3; x0 = y0 = 1), fixed-grid RK4 at h = {h:g} over {n_per} periods; period T = {T:.4f} (spread {T_sd:.1e} over {len(mins) - 1} cycles), prey between {xs.min():.4f} and {xs.max():.4f}",
        source=f"{SRC} [12] (DESCR)",
        Q="the two A3 occasions of a prey oscillation are the two halves of the period: on a one-degree-of-freedom conservative oscillator the rotor A3 names is the canonical angle, which advances uniformly (Arnold-Liouville), so the half-turn cut falls at T/2 after the last cut wherever the sequence starts, and the two occasions carry unequal arcs because the cycle is asymmetric",
        ingredient="A3 (the oriented antipode on the carrier's rotor) in three readings the repository names: (i) the domain's canonical angle, (ii) the analytic-signal phase of the prey trace (intrinsic_phase, the one implemented reading), (iii) a Poincare section (CLAUDE.md section 3.1, item 2), here at dx/dt = 0, the prey extrema",
        null="the clock: T/2 after the last cut, which is reading (i) itself",
        domain="Arnold-Liouville: a 1-dof integrable system has action-angle coordinates in which the angle advances at 2 pi / T(V), so half a turn of the system's own phase is half a period; the LV first integral V = 0.2 x - 0.3 ln x + 0.5 y - ln y is conserved",
        numbers=(f"reading (i), canonical angle: occasions {f_i:.4f} T and {1 - f_i:.4f} T by the theorem, arcs from a prey minimum {arc_clk[0]:.4f}, {arc_clk[1]:.4f}, {arc_clk[2]:.4f}, {arc_clk[3]:.4f} (ratio {arc_clk[0] / arc_clk[1]:.4f}); "
                 f"reading (ii), analytic-signal phase (advance per period {adv:.5f} turns): sequence started at a prey minimum: occasions {fr_min[0]:.4f}, {fr_min[1]:.4f}, {fr_min[2]:.4f}, {fr_min[3]:.4f} T (spread of the ten {np.std(fr_min[::2]):.1e}), arcs {arc_min[0]:.4f}, {arc_min[1]:.4f}, {arc_min[2]:.4f}, {arc_min[3]:.4f} (ratio {arc_min[0] / arc_min[1]:.4f}, CV over ten {cv(arc_min):.4f}); started at a prey maximum: occasions {fr_max[0]:.4f}, {fr_max[1]:.4f} T, arcs {arc_max[0]:.4f}, {arc_max[1]:.4f} (ratio {arc_max[0] / arc_max[1]:.4f}); "
                 f"reading (iii), Poincare section at the prey extrema: occasions {f_crash:.4f} T from maximum to minimum (the crash) and {f_recov:.4f} T from minimum to maximum (the recovery), so the crash is the {_word(f_crash < f_recov, 'shorter', 'longer')}; arcs {arc_ext[0]:.4f}, {arc_ext[1]:.4f}, {arc_ext[2]:.4f}, {arc_ext[3]:.4f} (equal by construction: each is x_max - x_min)"),
        tg=f"reading (i) first occasion {f_i:.4f} T vs reading (ii) {f_ii:.4f} T (started at a minimum; {f_ii_max:.4f} T started at a maximum) vs reading (iii) {f_iii:.4f} T: {_agree(f_i, f_ii)} (the ingredient has three values on the domain)",
        tn="the action-angle theorem fixes reading (i), the half period, under which the cut is the clock by definition and adds nothing",
        tc="not reached: the readings of A3's rotor must agree before Q can be checked",
        out=out,
        reading=(f"on a planar conservative oscillator the three rotors the repository names put the cut in three places: the canonical angle at {f_i:.4f} T (the clock, so A3 is redundant with it), the analytic-signal phase at {f_ii:.4f} T or {f_ii_max:.4f} T depending on where the sequence starts (batch 03 row 3's start dependence, with the even harmonics of the LV cycle), the extremum section at {f_iii:.4f} T (which CRR.md says is not the cut); "
                 f"every reading gives unequal arcs except the extremum one, whose arcs are equal by construction, so the source row's 'equal half-turn arcs are a symmetry, not a consequence' stands under all of them (ratios {arc_clk[0] / arc_clk[1]:.3f}, {arc_min[0] / arc_min[1]:.3f}, {arc_max[0] / arc_max[1]:.3f}, {arc_ext[0] / arc_ext[1]:.3f}); which rotor A3 means on a carrier with a canonical angle is a theory choice"),
        weakness="the source row printed CV 0.338 and arm ratio 0.525 from a sequence started at t = 0 on a ten-period record with edge cuts included; here the sequence starts at an interior extremum of a forty-period record, which is why the reading-(ii) numbers differ; a single orbit (V fixed), so nothing varies between cycles and H-L5 has no purchase",
        elegance="",
        child="")


def main():
    return run_batch("Synthesis batch 12: rows 56-60 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
