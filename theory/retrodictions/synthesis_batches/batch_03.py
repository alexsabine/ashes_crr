"""Synthesis batch 03: rows 11-15 of QUEUE.md (prompt-log entry 61).
[15] main battery, sequential Bayesian updating of a Gaussian mean (P2 surplus weights against Gauss-Markov / Basu);
[17] main battery, harmonic oscillator amplitude A (A1'/D1 resolvable step on the oscillator's own carrier, the coherent state);
[18] main battery, asymmetric multi-harmonic oscillator, the two half-turn arcs (A3 on half-wave-symmetric signals);
[20] main battery, plane pendulum with amplitude jitter (H-L5 class against the elasticity of the exact period);
[21] main battery, homogeneous Poisson process, natural time (A6/P3 seed as a forecast against memorylessness).
Every verdict word is computed from the numbers (R15). Deterministic (fixed seeds, fixed grids). No data files (R2).
Run:  uv run python theory/retrodictions/synthesis_batches/batch_03.py
"""
import math
import sys

import numpy as np
from scipy import optimize
from scipy.signal import find_peaks
from scipy.special import ellipk

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _agree(a, b, tol):
    return "agree" if rel(a, b) <= tol else "differ"


# ---------------------------------------------------------------- 11: [15] P2 surplus weights on the Bayesian domain
def r1(n=10, K=16, R=20000, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.normal(0.0, 1.0, (R, K, n))                                   # sigma = 1: the per-event unit of the source row
    post = np.cumsum(y, axis=2) / np.arange(1, n + 1)                     # within-batch posterior-mean path (flat prior)
    d = np.diff(post, axis=2)
    C = np.abs(d).sum(axis=2); D = np.abs(post[..., -1] - post[..., 0]); S = C - D   # D2, D3, D4 on the 1-D carrier
    ybar = post[..., -1]                                                  # the batch posterior mean (sufficient)
    corr = float(np.corrcoef(S.ravel(), ybar.ravel())[0, 1])
    betas = (0.0, 0.5, 1.0, 2.0, 4.0, -1.0)
    infl = {}
    mc = None
    for beta in betas:
        w = np.exp(beta * S); w /= w.sum(axis=1, keepdims=True)           # P2: pi_m ∝ exp(beta S_m), normalised per replication
        infl[beta] = float(K * (w ** 2).sum(axis=1).mean())               # MSE(sum pi ybar) / MSE(grand mean) = K E[sum pi^2]
        if beta == 1.0:
            est = (w * ybar).sum(axis=1); mc = float((est ** 2).mean() * n * K)
    crr, null, domain = infl[1.0], infl[0.0], 1.0
    check = crr <= domain * (1.0 + TOL_N)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    grid = "; ".join(f"beta = {b:g}: {v:.4f}" for b, v in infl.items())
    reading = {
        "WRONG": f"the surplus of an occasion is ancillary to its content (Basu: correlation {corr:+.4f}), so weighting settled occasions by e^(beta S) can only add variance to the seed; the P2 seed reduces to the accumulated estimate only at beta = 0, where the weight law is the constant it replaces; read with synthesis row 3 (the A6 spread does not shrink), the regeneration axiom and its weight law are both contradicted on the Bayesian domain",
    }.get(out, f"the P2 seed did not lose to the accumulated mean in this run: {out}")
    return make_row("stat", "Sequential Bayesian estimation of a Gaussian mean (known variance) from K settled batches, the surplus-weighted seed of the next occasion against the accumulated posterior mean",
                    source="theory/retrodictions/crr_retrodictions.txt [15] (DESCR)",
                    Q="the seed of the next occasion, taken as the surplus-weighted (P2, beta = 1 per unit of surplus) Fisher-Rao Frechet mean of the K settled batch posteriors, is at least as accurate a location for mu as the accumulated posterior mean (relative MSE <= 1)",
                    ingredient="P2 (pi_m ∝ exp(beta S_m)) inside A6 (Frechet mean of settled occasion contents), D5 (occasion = one batch of n draws), D4 (S_m = C_m − C*_m of the within-batch posterior-mean path, per-event unit sigma, the source row's 1-D carrier where the Frechet mean is the weighted arithmetic mean)",
                    null="beta = 0: uniform weights, which is the accumulated posterior mean (the domain's own estimator)",
                    domain="Gauss-Markov (uniform weights are the minimum-variance unbiased combination of equal-precision batch means) with Basu's theorem (S_m is ancillary, independent of the complete sufficient batch mean, so surplus weights carry no information about the location)",
                    numbers=f"K = {K} batches of n = {n} draws, {R} replications: corr(S_m, ybar_m) = {corr:+.4f} (Basu: 0); relative MSE of the P2 seed, closed form K E[sum pi_m^2]: {grid}; Monte-Carlo MSE ratio at beta = 1: {mc:.4f} (closed {crr:.4f}, relative difference {rel(mc, crr):.3f})",
                    tg=f"relative MSE {crr:.4f} (beta = 1) vs null {null:.4f} (beta = 0, the accumulated mean): {_agree(crr, null, TOL_G)}",
                    tn=f"Gauss-Markov gives {domain:.4f} for the optimum, so {'the domain has Q' if rel(crr, domain) <= TOL_N else 'the domain gives the opposite of Q (its optimum is the null)'}",
                    tc=f"Q (relative MSE <= 1 within {TOL_N:g}): {'holds' if check else 'fails'}",
                    out=out, reading=reading,
                    weakness="beta is not fixed by CRR (P2), so the row tests the family at a named beta and prints the grid (every beta != 0 loses, both signs); H-T1 was not used because CRR's own clause excludes the convex learner, which the Gaussian mean is; A3 was not used (O3: no rotor on the posterior path); A6 with uniform weights is synthesis row 3")


# ---------------------------------------------------------------- 12: [17] the oscillator's own resolvable step
def r2(alphas=(2.0, 4.0), m=200001):
    res = []
    for a in alphas:
        th = np.linspace(0.0, math.pi, m)                                 # half a period: alpha(t) = alpha e^{-i omega t}
        z = a * np.exp(-1j * th)
        ov = np.exp(-0.5 * np.abs(z[1:] - z[:-1]) ** 2)                   # |<alpha_i|alpha_{i+1}>| for coherent states
        arc = float((2.0 * np.arccos(np.clip(ov, -1.0, 1.0))).sum())      # D2 with the Fubini-Study metric, orthogonality = pi
        ov_end = math.exp(-0.5 * abs(z[-1] - z[0]) ** 2)                  # |<alpha|-alpha>| = e^{-2 |alpha|^2}
        chord = 2.0 * math.acos(ov_end)                                   # D3
        nbar = a ** 2
        rho = arc / math.pi                                               # D1: half-turn arc over one Fisher step (the distance to an orthogonal state)
        aa = 2.0 * a * math.pi / math.pi                                  # Anandan-Aharonov: (1/pi) ∫ 2 dE dt / hbar with dE = hbar omega sqrt(nbar) over T/2 = pi/omega
        pos = 4.0 * a                                                     # 2A / x_0 with A = 2 x_0 |alpha|
        res.append((a, nbar, arc, chord, ov_end, arc - chord, rho, aa, pos))
    a, nbar, arc, chord, ov_end, S, rho, aa, pos = res[-1]
    check = abs(rho - aa) < 1e-6
    out = outcome(crr=rho, null=pos, domain=aa, check=check)
    numbers = "; ".join(f"alpha = {a_:g} (nbar = {nb_:g}): Fisher arc per half-turn {arc_:.4f} (2 pi sqrt(nbar) = {2 * math.pi * a_:.4f}), chord to the antipode {ch_:.4f} (overlap |<alpha|-alpha>| = {ov_:.1e}), surplus S = {S_:.4f}; rho = {rho_:.4f}; Anandan-Aharonov count {aa_:.4f}; position count 2A/x_0 = {pos_:.4f}" for a_, nb_, arc_, ch_, ov_, S_, rho_, aa_, pos_ in res)
    reading = {
        "REDUNDANT-DOMAIN": f"taking the oscillator's own resolvable step seriously (A1') fixes the source row's free unit and turns 'arc per half-turn = 2A' into a count, 2 sqrt(nbar) = {rho:.4f} at nbar = {nbar:g}; the count is Wootters' and Anandan-Aharonov's number of distinguishable states along the orbit, so the domain has it; the source row's 'the period does not enter' survives (rho depends on nbar only)",
    }.get(out, f"the resolvable-step count did not reproduce the domain's count in this run: {out}")
    return make_row("qm", "Harmonic oscillator with its own resolvable step: a coherent state |alpha e^{-i omega t}> on the projective carrier (quantum Fisher = Fubini-Study metric), the half-period as the half-turn",
                    source="theory/retrodictions/crr_retrodictions.txt [17] (DESCR)",
                    Q="a coherent state of mean quantum number nbar passes 2 sqrt(nbar) resolvable steps in each half-turn of its orbit (D1: rho = half-turn arc / one Fisher step, one step being the distance to an orthogonal state), independently of the period",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step: on the projective carrier one step is the Fisher-Rao distance to orthogonality; rho = arc per half-turn / step), A3 (the half-turn is the half period; the antipode |-alpha> is orthogonal to |alpha> up to e^{-2 nbar}), D2/D3 with A1 = the quantum Fisher metric",
                    null="an outside position unit: the zero-point width x_0 = sqrt(hbar / 2 m omega) as the step, rho = 2A / x_0 = 4 sqrt(nbar)",
                    domain="Anandan-Aharonov 1990 / Wootters 1981: the number of distinguishable states along a curve is (1/pi) ∫ 2 dE dt / hbar; a coherent state has dE = hbar omega sqrt(nbar), so a half period passes 2 sqrt(nbar)",
                    numbers=numbers,
                    tg=f"rho {rho:.4f} (Fisher step) vs null {pos:.4f} (position step x_0): {_agree(rho, pos, TOL_G)}",
                    tn=f"the domain's count gives {aa:.4f}: {'the domain has Q' if rel(rho, aa) <= TOL_N else 'the domain does not produce Q'}",
                    tc=f"rho = 2 sqrt(nbar) to {abs(rho - aa):.1e}: {'holds' if check else 'fails'} (the check is the same computation as T-N)",
                    out=out, reading=reading,
                    weakness=f"the classical source row has no resolvable step, so the synthesis had to move to the quantum oscillator, the one place the domain sets one; the coherent orbit is far from a geodesic (S / C* = {S / chord:.2f} at nbar = {nbar:g}), which D4 names and information geometry owns; citations by name and year only, not fetched here (R10)")


# ---------------------------------------------------------------- 13: [18] A3 on half-wave-symmetric and even-harmonic signals
def _a3_arcs(x, start=0):
    c = antipodal_cuts(intrinsic_phase(x), start=start)
    return np.array([arc_length(x[a:b + 1]) for a, b in zip(c[:-1], c[1:])]), c


def r3(n=60001, per=3, prominence=0.5, distance=100):
    t = np.linspace(0.0, 2 * np.pi * per, n); one = n // per                # one period = `one` samples (grid: 2 pi per 20000 samples)
    half = one // 2
    hw = lambda x: float(np.sqrt(np.mean((x[:2 * one] + x[half:half + 2 * one]) ** 2)))   # RMS of x(t) + x(t + T/2): 0 iff half-wave symmetric
    # the half-wave-symmetric asymmetric signal (odd harmonics only, several extrema per half-period)
    xo = np.sin(t) + 0.6 * np.sin(3 * t) + 0.3 * np.sin(5 * t + 1.0)
    ao, co = _a3_arcs(xo); ao_in = ao[1:-1]
    spacing = float(np.mean(np.diff(t[co])))
    ao2, co2 = _a3_arcs(xo, start=2000); ao2_in = ao2[1:-1]              # a second start (t = 0.6283): Q claims start independence
    spacing2 = float(np.mean(np.diff(t[co2])))
    pco = peak_cuts(xo, prominence=prominence, distance=distance)
    po = np.array([arc_length(xo[a:b + 1]) for a, b in zip(pco[:-1], pco[1:])])[1:-1]
    tv_half = arc_length(xo[:one + 1]) / 2.0                              # the domain's number: half of one period's total variation
    crr, null, domain = float(ao_in.mean()), float(po.mean()), tv_half
    check = (cv(ao_in) < 1e-6) and (abs(spacing - math.pi) < 1e-3) and (cv(ao2_in) < 1e-6) and (abs(spacing2 - math.pi) < 1e-3) and (rel(float(ao2_in.mean()), crr) < 1e-6)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    # the source row's even-harmonic signal: start dependence of the split, and the peak split
    xe = np.sin(t) + 1.2 * np.sin(2 * t) + 0.6 * np.sin(3 * t)
    ae0, ce0 = _a3_arcs(xe); ae0_in = ae0[1:-1]
    ae1, _ = _a3_arcs(xe, start=2000); ae1_in = ae1[1:-1]
    pke = peak_cuts(xe, prominence=prominence, distance=distance)
    pe = np.array([arc_length(xe[a:b + 1]) for a, b in zip(pke[:-1], pke[1:])])[1:-1]
    x_at_cuts = float(np.max(np.abs(xe[ce0])))
    # converse search: an even harmonic with equal A3 arcs (cut started at t = 0)
    def split(phi):
        a, _ = _a3_arcs(np.sin(t) + 0.8 * np.sin(2 * t + phi)); a = a[1:-1]; return float(a[0] - a[1])
    d0 = split(0.0)
    phistar = optimize.brentq(split, 1.1781, 1.5708, xtol=1e-10)
    xs = np.sin(t) + 0.8 * np.sin(2 * t + phistar); as_, _ = _a3_arcs(xs); as_in = as_[1:-1]
    numbers = (f"half-wave-symmetric asymmetric signal sin t + 0.6 sin 3t + 0.3 sin(5t + 1) (RMS of x(t) + x(t + T/2) = {hw(xo):.1e}): A3 cuts every {spacing:.5f} rad (T/2 = {math.pi:.5f}), arcs {', '.join(f'{v:.4f}' for v in ao_in)} (CV {cv(ao_in):.1e}); cut started at t = {t[2000]:.4f} instead: cuts every {spacing2:.5f} rad, arcs {', '.join(f'{v:.4f}' for v in ao2_in)} (CV {cv(ao2_in):.1e}); peak cuts: {len(pco) / per:g} extrema per period, arcs CV {cv(po):.4f}, mean {null:.4f}; one period's total variation / 2 = {tv_half:.4f}. "
               f"Even-harmonic source signal sin t + 1.2 sin 2t + 0.6 sin 3t (RMS asymmetry {hw(xe):.4f}): A3 arcs {', '.join(f'{v:.4f}' for v in ae0_in)} (CV {cv(ae0_in):.4f}) with the cut started at t = 0, where every cut sits at a zero crossing (max |x| at the cuts {x_at_cuts:.1e}); started at t = {t[2000]:.4f} the arcs are {', '.join(f'{v:.4f}' for v in ae1_in)} (CV {cv(ae1_in):.4f}); the peak split at the main extrema gives {', '.join(f'{v:.4f}' for v in pe[:2])} (CV {cv(pe):.4f}). "
               f"Converse search sin t + 0.8 sin(2t + phi), cut started at t = 0: C1 − C2 = {d0:+.4f} at phi = 0, root at phi* = {phistar:.4f} where the arcs are {', '.join(f'{v:.4f}' for v in as_in)} (CV {cv(as_in):.1e}) with the even harmonic present (RMS asymmetry {hw(xs):.4f})")
    reading = {
        "REDUNDANT-DOMAIN": f"on the half-wave-symmetric class A3 is the half-period and every occasion carries half the period's total variation, a two-line lemma of the analytic signal (z(t + T/2) = −z(t)); the source row's asymmetric case is the complement: with an even harmonic the A3 split depends on where the cut sequence starts (CV {cv(ae0_in):.4f} against {cv(ae1_in):.4f} for two starts) and is generically unequal but not always (phi* = {phistar:.4f}), so 'equal arcs hold only by symmetry' is right as a sufficient condition and wrong as a necessary one; the equality is Fourier's, not CRR's",
    }.get(out, f"the A3 arc on the symmetric signal did not match the domain's half-period total variation in this run: {out}")
    return make_row("sig", "Periodic signals with several harmonics under the analytic-signal phase: when are the two A3 occasions of a cycle equal in arc?",
                    source="theory/retrodictions/crr_retrodictions.txt [18] (DESCR)",
                    Q="the A3 occasions of a periodic signal are exactly its half-periods and carry equal arc (half the period's total variation) whenever the signal is half-wave symmetric (x(t + T/2) = −x(t): odd harmonics only), wherever the cut sequence starts and however many extrema a half-period holds",
                    ingredient="A3 (cut at the half-turn of the intrinsic phase, antipodal_cuts), D5 (occasion), D2 with the identity metric (1-D arc = total variation)",
                    null=f"the peak cut (waveform extrema, CRR.md: 'peak detection is not the cut'), prominence {prominence:g}, distance {distance} samples",
                    domain="Fourier: half-wave symmetry ⇔ odd harmonics only; the analytic signal is linear, so z(t + T/2) = −z(t) and its phase advances exactly pi per half-period; total variation is invariant under x → −x, so both halves carry TV/2",
                    numbers=numbers,
                    tg=f"arc per A3 occasion {crr:.4f} vs null arc per peak-cut occasion {null:.4f}: {_agree(crr, null, TOL_G)}",
                    tn=f"the domain's half-period total variation gives {domain:.4f}: {'the domain has Q' if rel(crr, domain) <= TOL_N else 'the domain does not produce Q'}",
                    tc=f"equal arcs (CV < 1e-6) at half-period spacing (within 1e-3 rad) for both starts, same arc at both: {'holds' if check else 'fails'} (and it is the domain's lemma)",
                    out=out, reading=reading,
                    weakness="1-D signal, no metric content; the A3 cut with the analytic-signal phase started at a zero crossing is zero-crossing detection of the demeaned signal (the phase is pi/2 mod pi exactly where x = 0), which is why the even-harmonic split moves with the start phase; the converse counterexample is one root for one start and says only that equality is not a certificate of symmetry",
                    elegance="Flip the wave upside down and slide it half a period: if it lands on itself, the two halves of every cycle carry the same length of road, wherever you start counting. A rule with no knobs, and a picture.",
                    child="Draw a wavy line. Turn the drawing upside down and slide it along by half a wave. If it lies exactly on top of the old line, then every half-wave has the same amount of up-and-down in it, no matter where you start measuring. If it does not land on itself, the two halves usually have different amounts, but not always.")


# ---------------------------------------------------------------- 14: [20] the pendulum's class is the elasticity of its period
def r4(seed=3, n_occ=60, jitter=0.1):
    T = lambda A: 4.0 * ellipk(math.sin(A / 2.0) ** 2)                    # exact period, g/l = 1 (T_0 = 2 pi)
    def elast(A, h=1e-6):
        return A * (math.log(T(A + h)) - math.log(T(A - h))) / (2.0 * h)  # d ln T / d ln A
    Astar = optimize.brentq(lambda A: elast(A) - 1.0, 0.5, 3.1, xtol=1e-12)
    rng = np.random.default_rng(seed); z = rng.standard_normal(n_occ)   # the source row's draw: A = 1 + 0.1 z
    def arm(A0):
        A = A0 + jitter * z                                              # per half-swing amplitude (rad); the half-swing is monotone from +A to −A
        arc = 2.0 * A                                                     # D2, identity metric on the angle: total variation of one half-swing
        amp = 2.0 * A                                                     # control (i): peak-to-trough amplitude of the same occasion
        clock = np.array([T(a) for a in A]) / 2.0                         # one half-period per occasion
        return dict(A=A, cv_arc=cv(arc), cv_amp=cv(amp), cv_clock=cv(clock), index=cv(clock) / cv(arc), index_amp=cv(clock) / cv(amp))
    arms = {A0: arm(A0) for A0 in (1.0, Astar, 2.8)}
    A_cross = optimize.brentq(lambda A0: arm(A0)["index"] - 1.0, 1.0, 2.9, xtol=1e-10)
    src = arms[1.0]
    crr, null, domain = src["index"], src["index_amp"], elast(1.0)
    check = None
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    numbers = ("; ".join(f"A = {A0:.4f} + {jitter:g} z ({n_occ} half-swings): CV(arc = 2A) = {r['cv_arc']:.4f}, CV(amplitude) = {r['cv_amp']:.4f}, CV(half-period) = {r['cv_clock']:.4f}, class index CV(clock)/CV(arc) = {r['index']:.4f} (elasticity d ln T / d ln A at A = {A0:.4f}: {elast(A0):.4f}; max A in the draw {r['A'].max():.4f} rad)" for A0, r in arms.items())
               + f"; elasticity = 1 at A* = {Astar:.4f} rad ({math.degrees(Astar):.1f} deg, T(A*)/T_0 = {T(Astar) / (2 * math.pi):.4f}); for this draw the index crosses 1 at A = {A_cross:.4f} rad")
    reading = {
        "REDUNDANT-IG": f"on a one-dimensional monotone half-swing the arc is the amplitude, so H-L5's regular quantity is its own control (i) and the class index is the elasticity of the period law: clock-regular at small amplitude (index {src['index']:.4f} at A = 1, elasticity {domain:.4f}) and arc-regular near the separatrix (index {arms[2.8]['index']:.4f} at A = 2.8), with the boundary at A* = {Astar:.4f} rad where isochrony fails by one part in one; every symbol is the domain's, and the source row's 'no CRR content' is confirmed with the crossover added",
    }.get(out, f"the arc and the amplitude control did not coincide in this run: {out}")
    return make_row("mech", "Plane pendulum with amplitude jitter, exact period T(A) = 4 sqrt(l/g) K(sin(A/2)), one half-swing (turning point to turning point) as the occasion",
                    source="theory/retrodictions/crr_retrodictions.txt [20] (DESCR)",
                    Q=f"under amplitude jitter the pendulum is clock-regular (H-L5 fails) below the amplitude A* where the period's elasticity d ln T / d ln A reaches 1, and arc-regular (H-L5 holds) above it: one oscillator, both of H-L5's classes, switched by amplitude",
                    ingredient="H-L5 (the class claim: arc against clock regularity between own events), D5 (occasion = one half-swing), D2 with the identity metric on the angle (arc per half-swing = 2A), A3 (on the symmetric swing the antipode is the turning point)",
                    null="control (i) of H-L5: the peak-to-trough amplitude of the occasion, which on a monotone half-swing is the arc itself",
                    domain="the exact period T(A) = 4 sqrt(l/g) K(sin(A/2)): to first order in the jitter CV(T) = (d ln T / d ln A) CV(A), so the class index CV(clock)/CV(arc) is the elasticity of the period law and the class boundary is its root at 1",
                    numbers=numbers,
                    tg=f"class index {crr:.4f} (arc) vs null {null:.4f} (amplitude control): {_agree(crr, null, TOL_G)}",
                    tn=f"the period law's elasticity at A = 1 gives {domain:.4f}: {'the domain has the index' if rel(crr, domain) <= TOL_N else 'the domain does not produce the index'}",
                    tc="not reached: the crossover in Q is the root of the domain's elasticity, printed above",
                    out=out, reading=reading,
                    weakness="the source row's algebraic model (per-occasion amplitude drawn, period from K(k)), not an integrated trajectory; the index is first-order in the jitter, so the finite-jitter crossing sits below A* (the period law is convex in A); at A near pi the draw must stay below the separatrix, which bounds the arm at 2.8",
                    elegance="One pendulum keeps both of CRR's clocks: swung low, its timing is the steady thing and the size of the swing wanders; swung nearly to the top, the size is the steady thing and the timing wanders. The switch is where a one-per-cent bigger swing costs a one-per-cent longer swing: a rule with no knobs.",
                    child="Push a playground swing gently and every back-and-forth takes the same time no matter how high it goes. Push it almost over the top and it hangs near the top for ages, so now how high it goes is the steady thing and the timing is not. The same swing keeps two different clocks depending on how hard you push.")


# ---------------------------------------------------------------- 15: [21] the A6 seed as a forecast on a memoryless process
def r5(lam=1.0, n=200, R=20000, seed=0, qs=(0.3, 0.5, 0.7, 0.9, 0.99), q_named=0.5):
    rng = np.random.default_rng(seed)
    past = rng.exponential(1.0 / lam, (R, n))                             # the settled inter-event intervals (natural time: one event per occasion)
    nxt = rng.exponential(1.0 / lam, R)                                   # the next interval, independent of the past (memorylessness)
    var_next = 1.0 / lam ** 2                                             # the domain: MSE(f) = Var(dt) + E[(f − 1/lam)^2] for any f built from the past
    mse = lambda f: float(var_next + ((f - 1.0 / lam) ** 2).mean())
    acc = past.mean(axis=1)
    fr, eu, fr_mean = {}, {}, {}
    for q in qs:
        w = (1.0 - q) * q ** np.arange(n)[::-1]; w /= w.sum()             # P3: pi_k ∝ q^k over age k (k = 0 the most recent)
        geo = np.exp((w * np.log(past)).sum(axis=1))                      # A6 with A1 on the exponential family (g = 1/tau^2): the Frechet mean is the weighted geometric mean
        fr[q] = mse(geo); fr_mean[q] = float(geo.mean()); eu[q] = mse((w * past).sum(axis=1))
    w = (1.0 - q_named) * q_named ** np.arange(n)[::-1]; w /= w.sum()
    direct = float(((np.exp((w * np.log(past)).sum(axis=1)) - nxt) ** 2).mean())
    crr, null, domain = fr[q_named], mse(acc), var_next
    check = crr <= domain * (1.0 + TOL_N)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    reading = {
        "WRONG": f"on a memoryless process the settled past holds nothing the mean does not, so a bounded-strength seed can only add variance and, in the Fisher-native reading, the downward bias of a geometric mean of exponentials (mean seed {fr_mean[q_named]:.4f} against {1.0 / lam:.4f}); the seed approaches the clock forecast only as q → 1, which is the accumulated count A6 forbids (Euclidean reading at q = {qs[-1]:g}: {eu[qs[-1]]:.4f}); A1' (one event = one step, the source row's definition) is untouched, and A6 on top of it is refuted by the domain's one theorem",
    }.get(out, f"the A6 seed did not lose to the clock forecast in this run: {out}")
    return make_row("point", "Homogeneous Poisson process (rate lambda): the seed of the next occasion from the settled inter-event intervals, as a forecast of the next interval",
                    source="theory/retrodictions/crr_retrodictions.txt [21] (DESCR)",
                    Q=f"the seed of the next occasion (A6: the Fisher-Rao Frechet mean of the settled inter-event intervals under P3 age weights q^k, q = {q_named:g}) forecasts the next inter-event interval of a homogeneous Poisson process at least as well as the clock forecast, the mean interval 1/lambda (A8: a conditional forecast from settled occasions, scored against the conventional one)",
                    ingredient="A6 (bounded-strength Frechet mean of settled occasions, never an accumulated count), P3 (geometric age weights), A8 (comparative forecast), D5 [M] (occasion = one inter-event interval), A1 on the exponential family (g = 1/tau^2, the source row's metric: the Frechet mean is the weighted geometric mean)",
                    null="the accumulated count A6 forbids: the arithmetic mean of all n settled intervals (the maximum-likelihood 1/lambda)",
                    domain="memorylessness of the Poisson process: E[dt_next | past] = 1/lambda, so the minimum-MSE forecast is the constant mean and its MSE is Var(dt) = 1/lambda^2; any forecast f built from the past has MSE = 1/lambda^2 + E[(f − 1/lambda)^2]",
                    numbers=f"lambda = {lam:g}, {R} runs of n = {n} settled intervals, MSE in units of 1/lambda^2: clock forecast {domain:.4f} (exact); accumulated mean {null:.4f} (closed 1 + 1/n = {1 + 1 / n:.4f}); A6 seed, FR Frechet (geometric) mean: " + "; ".join(f"q = {q:g}: {fr[q]:.4f} (mean seed {fr_mean[q]:.4f})" for q in qs) + "; Euclidean weighted mean (not A6's metric): " + "; ".join(f"q = {q:g}: {eu[q]:.4f} (closed 1 + (1 − q)/(1 + q) = {1 + (1 - q) / (1 + q):.4f})" for q in qs) + f"; direct Monte-Carlo MSE of the A6 seed at q = {q_named:g} against a drawn next interval: {direct:.4f}",
                    tg=f"A6 seed MSE {crr:.4f} (q = {q_named:g}) vs null {null:.4f} (accumulated mean): {_agree(crr, null, TOL_G)}",
                    tn=f"memorylessness gives {domain:.4f} for the best forecast: {'the domain has Q' if rel(crr, domain) <= TOL_N else 'the domain gives the opposite of Q (its optimum is the constant)'}",
                    tc=f"Q (A6 seed MSE <= clock MSE within {TOL_N:g}): {'holds' if check else 'fails'}",
                    out=out, reading=reading,
                    weakness="q is not fixed by CRR (P3): the grid shows every q < 1 loses in the Fisher-native reading and the Euclidean reading reduces to the null as q → 1; a homogeneous process is the extreme case (nothing to remember), so this row bounds A6 from the side opposite to synthesis rows 3 and 9, where the domain accumulates: A6 is now contradicted where the domain accumulates and where it forgets",
                    elegance="A process with no memory is the cleanest teacher of what a seed can and cannot do: the past can only add noise, and the only past that helps is all of it, averaged.",
                    child="Raindrops hit a roof at random. If you try to guess when the next one will land by watching the last few and trusting the newest ones most, you do worse than just knowing how often they fall on average. Sometimes the past is not a clue, and remembering it a little is worse than remembering all of it.")


def main():
    return run_batch("Synthesis batch 03: rows 11-15 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
