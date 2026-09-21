"""Synthesis batch 22: rows 106-110 of QUEUE.md (prompt-log entry 61). emptiness [9] the MaxEnt occasion weights at zero
surplus, zero temperature and zero age (DESCR); emptiness [10] signal below one resolvable step: does the antipodal cut
fire on nothing (DESCR); emptiness [11] zero, one, two and three events: what the regularity statistic can say (DESCR);
emptiness [13] zero surplus: the monotone path (P1's equality case) against one that turns back (DESCR); shannon [1] the
Fisher metric is the Hessian of the Kullback-Leibler divergence; D6's step sqrt(2 KL) is the Fisher-Rao distance to
second order (DESCR)."""
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.stats import binomtest

from crr.instrument.core import antipodal_cuts, cv, intrinsic_phase, kl_step, path_length, peak_cuts, regularity, surplus
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _ad(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def _hf(flag):
    return "holds" if flag else "fails"


# ---------------------------------------------------------------- 1 P3 at zero occasions: RLS forgetting and estimator windup
def _rls_gains(lam, n_ex, gap, aging):
    """Scalar RLS in information form, I_t = lam I_{t-1} + phi_t^2, gain phi_t / I_t; phi = 1 when excited, 0 in the gap.
    aging = 'sample': the forgetting factor acts at every sample (the domain's RLS); 'occasion': it acts only when an
    occasion (an excited sample) arrives (P3's age in natural time, A1'); 'conditional': the domain's conditional
    updating (skip the update when the regressor carries no information)."""
    I, gains = 0.0, []
    for phi in [1.0] * n_ex + [0.0] * gap + [1.0]:
        if aging == "sample" or phi != 0.0:
            I = lam * I + phi * phi
        gains.append(phi / I if I > 0 else float("nan"))
    return gains


def r1():
    q, n_ex, gap = 0.9, 200, 30
    gs, go, gc = (_rls_gains(q, n_ex, gap, a) for a in ("sample", "occasion", "conditional"))
    g_before_s, g_before_o = gs[n_ex - 1], go[n_ex - 1]
    g_after_s, g_after_o, g_after_c = gs[-1], go[-1], gc[-1]
    closed_s = 1.0 / (q ** (gap + 1) / (1.0 - q) + 1.0)
    k = np.arange(n_ex); w0 = q ** k / (q ** k).sum(); w1 = q ** (k + gap) / (q ** (k + gap)).sum()
    w_diff = float(np.max(np.abs(w1 - w0)))
    I1 = 0.0
    for _ in range(100):
        I1 = 1.0 * I1 + 1.0
    g_q1 = 1.0 / I1
    check = (abs(g_before_o - (1 - q)) < 1e-6 and abs(g_after_o - (1 - q)) < 1e-6 and abs(g_after_s - closed_s) < 1e-6)
    out = outcome(crr=g_after_o, null=g_after_s, domain=g_after_c, check=check)
    return make_row("sysid", f"Recursive least squares with exponential forgetting (forgetting factor lambda = q = {q:g}, scalar regressor phi = 1 when excited), the domain in which P3's two ends have names: lambda = 1 is the estimator that falls asleep (gain 1/t) and lambda -> 0 keeps only the newest datum; the domain's zero is a stretch of m = {gap} unexcited samples (phi = 0), where the standard estimator winds up (covariance windup)",
                    source="theory/retrodictions/emptiness.txt [9] (DESCR)",
                    Q="an exponential-forgetting estimator whose age is counted in occasions (A1' natural time: an unexcited sample is not an occasion, so the settled weights do not age through it) keeps its steady-state gain 1 - q across an unexcited stretch, while the same forgetting factor counted in samples winds up: its gain on the first datum after m empty samples rises from 1 - q toward 1, as 1/(q^(m+1)/(1 - q) + 1)",
                    ingredient="P3 (geometric age weights q^k, normalised inside A6 at bounded strength) with A1'/D5 [M] (age in natural time: the excited sample is the event, the empty sample is nothing); P2 at zero surplus (all S_m equal: uniform weights, which is lambda = 1)",
                    null="the same forgetting factor aged by the sample clock: the domain's standard RLS with lambda < 1",
                    domain="Astrom and Wittenmark 1995 (Adaptive Control: covariance windup under lambda < 1 without excitation; remedy: conditional updating, forget only when the regressor carries information); Ljung 1999 (steady-state RLS with forgetting is the exponentially weighted mean with weights (1 - lambda) lambda^k)",
                    numbers=f"steady-state gain before the gap: sample-aged {g_before_s:.4f}, occasion-aged {g_before_o:.4f} (1 - q = {1 - q:.4f}); gain on the first excited sample after {gap} empty samples: sample-aged {g_after_s:.4f} (closed form {closed_s:.4f}), occasion-aged {g_after_o:.4f}, conditional-update RLS {g_after_c:.4f}; normalised P3 weights of the {n_ex} settled occasions before and after aging every one by {gap} samples: max |difference| {w_diff:.1e}; share of the next datum's noise variance passed into the estimate: sample-aged {g_after_s ** 2:.4f}, occasion-aged {g_after_o ** 2:.4f}; the two ends of the family: q = 1 (P2 at zero surplus, uniform weights): gain after 100 occasions {g_q1:.4f} and falling as 1/t; q -> 0: gain 1 (only Now)",
                    tg=f"gain after the gap {g_after_o:.4f} (occasion age) vs null {g_after_s:.4f} (sample age): {_ad(g_after_o, g_after_s)}",
                    tn=f"conditional updating gives {g_after_c:.4f}: {_ad(g_after_o, g_after_c, TOL_N)} (the domain has Q)",
                    tc=f"occasion-aged gain equal to 1 - q before and after the gap within 1e-6 and sample-aged gain equal to its closed form within 1e-6: {_hf(check)}",
                    out=out,
                    reading=f"the source row's endpoints get the domain's names (q = 1 is the estimator that falls asleep, gain {g_q1:.4f} after 100 occasions; q -> 0 is the newest datum alone) and its zero becomes the domain's zero, the unexcited stretch: counting age in occasions rather than samples keeps the gain at {g_after_o:.4f} where the sample clock lets it wind up to {g_after_s:.4f} (T-G), and the domain's own remedy, conditional updating, is that rule ({g_after_c:.4f}); the normalised weights are invariant under aging without occasions (max difference {w_diff:.1e}), which is why. The synthesis reading is {out}",
                    weakness="a scalar Euclidean carrier, where A6's Frechet mean is the weighted mean; the equivalence between the P3-weighted mean and RLS holds only at the steady state under constant excitation; conditional updating is one of the domain's several remedies (variable, directional and constant-trace forgetting are others); citations by name and year only, not fetched (R10)",
                    elegance="A memory that fades by the calendar forgets even while nothing happens, and then over-trusts the next thing it sees; a memory that fades by the event keeps its footing through the quiet. One rule, no knobs: age is counted in things that happened.",
                    child="Imagine you keep a running guess of how fast your friend runs, trusting recent races most. If you let old races fade just because days pass, then after a long break with no races you have forgotten everything and the next race, good or bad, becomes your whole opinion. If you let races fade only when a new race happens, the break changes nothing.")


# ---------------------------------------------------------------- 2 A3 below one resolvable step: the sine in Rice's noise
def _band_noise(n, f0, sf, seed):
    rng = np.random.default_rng(seed); w = rng.standard_normal(n)
    W = np.fft.rfft(w); f = np.fft.rfftfreq(n, 1.0); H = np.exp(-0.5 * ((f - f0) / sf) ** 2)
    x = np.fft.irfft(W * H, n); x /= x.std(); return x, f


def r2():
    n, f0, sf, fs = 2 ** 18, 0.05, 0.005, 0.03
    x, f = _band_noise(n, f0, sf, 0)
    P = np.abs(np.fft.rfft(x)) ** 2; fbar = float((f * P).sum() / P.sum()); frms = math.sqrt(float((f * f * P).sum() / P.sum()))
    kedem = math.acos(float(np.corrcoef(x[:-1], x[1:])[0, 1])) / math.pi
    t = np.arange(n); grid = []
    for rho_ in (0.0, 0.2, 0.5, 1.0, 2.0, 4.0, 8.0):
        a = rho_ / 2.0; y = a * np.sin(2 * math.pi * fs * t + 0.3) + x
        ph = intrinsic_phase(y); cuts = antipodal_cuts(ph); rate = (len(cuts) - 1) / (cuts[-1] - cuts[0])
        net = (ph[-1] - ph[0]) / math.pi / (n - 1)
        law = 2.0 * (fs + (fbar - fs) * math.exp(-a * a / 2.0))
        zc = float(np.mean(np.sign(y[:-1]) != np.sign(y[1:])))
        pk = peak_cuts(y, prominence=0.0, distance=1); pkr = (len(pk) - 1) / (pk[-1] - pk[0])
        grid.append((rho_, rate, net, law, zc, pkr))
    rng = np.random.default_rng(2); wn = rng.standard_normal(4001); phw = intrinsic_phase(wn); cw = antipodal_cuts(phw)
    w_rate = (len(cw) - 1) / (cw[-1] - cw[0]); w_net = (phw[-1] - phw[0]) / math.pi / 4000
    w_zc = float(np.mean(np.sign(wn[:-1]) != np.sign(wn[1:]))); w_kedem = math.acos(float(np.corrcoef(wn[:-1], wn[1:])[0, 1])) / math.pi
    fw = np.fft.rfftfreq(4001, 1.0); Pw = np.abs(np.fft.rfft(wn)) ** 2; w_cent = 2 * float((fw * Pw).sum() / Pw.sum()); w_theory = math.acos(0.0) / math.pi
    g2 = [g for g in grid if g[0] == 2.0][0]
    crr_r, null_r, dom_r = g2[1], g2[4], g2[3]
    crr_x, null_x, dom_x = g2[1] - 2 * fs, g2[4] - 2 * fs, g2[3] - 2 * fs
    law_ok = all(rel(g[1], g[3]) <= TOL_N for g in grid); above_ok = all(g[4] > g[1] and g[5] > g[1] for g in grid)
    check = law_ok and above_ok
    out = outcome(crr=crr_r, null=null_r, domain=dom_r, check=check)
    return make_row("sig", f"Gaussian noise band-limited about f_n = {f0:g} cycles/sample (spectral width {sf:g}; 10 samples per half-turn, inside the instrument's sampling rule) with a sine of frequency f_s = {fs:g} added at rho = 0, 0.2, 0.5, 1, 2, 4, 8 resolvable steps (D1: rho = 2a / sigma_noise, the source row's scale); 2^{int(math.log2(n))} samples, seed 0; the domain's named case is Rice's sine wave plus random noise, and the zero is rho = 0",
                    source="theory/retrodictions/emptiness.txt [10] (DESCR)",
                    Q="the A3 occasion rate on a record whose signal sits rho resolvable steps above the noise is 2 [f_s + (f_n - f_s) e^(-rho^2/8)] half-turns per sample: the noise's own centroid rate at rho = 0 and the signal's rate as rho grows, with D1's rho entering the domain's signal-to-noise ratio as R = rho^2/8; the crossing count (Rice) and the extremum count are different statistics and sit above it",
                    ingredient="A3 (the oriented half-turn of the analytic-signal phase, antipodal_cuts), D1 (rho), D5",
                    null="the unoriented zero-crossing count (Rice 1944; Kedem's arccos(r_1)/pi for a sampled process), the domain's count of the same record; the extremum count (peak_cuts) printed beside it",
                    domain="the mean instantaneous frequency of a sinusoid in narrowband Gaussian noise, f_s + (f_n - f_s) e^(-R) with R = a^2 / (2 sigma^2) (Rice 1948, sine wave plus random noise; it follows from E[dn/dt | n] = 2 pi i f_n n for the analytic noise and the two-dimensional Gauss law E[Re u / |u|^2] = (1 - e^(-R)) / a for u ~ CN(a, 2 sigma^2))",
                    numbers=f"noise alone: centroid f_n = {fbar:.5f} (2 f_n = {2 * fbar:.5f}), 2 f_rms = {2 * frms:.5f}, Kedem crossing rate {kedem:.5f}; per rho (half-turns per sample): " + "; ".join(f"rho = {g[0]:g}: A3 rate {g[1]:.5f} (net phase / pi {g[2]:.5f}), law {g[3]:.5f} (relative difference {rel(g[1], g[3]):.4f}), zero crossings {g[4]:.5f}, extrema {g[5]:.5f}" for g in grid) + f"; 2 f_s = {2 * fs:.5f}; excess over 2 f_s at rho = 2: A3 {crr_x:.5f}, zero crossings {null_x:.5f}, law {dom_x:.5f}; white noise at one sample per step (outside the sampling rule, the source row's carrier): A3 rate {w_rate:.4f}, net unwrapped phase / pi {w_net:.4f}, twice the periodogram centroid {w_cent:.4f}, zero crossings {w_zc:.4f} (Kedem {w_kedem:.4f}, arccos(0)/pi = {w_theory:.4f}): the unwrap misreads phase increments beyond pi, so there the count is not the centroid's",
                    tg=f"A3 rate at rho = 2: {crr_r:.5f} vs null (zero crossings) {null_r:.5f}: {_ad(crr_r, null_r)}",
                    tn=f"the mean-frequency law gives {dom_r:.5f} at rho = 2: {_ad(crr_r, dom_r, TOL_N)} (the domain has Q)",
                    tc=f"A3 rate within 1 % of the law at every rho: {'yes' if law_ok else 'no'}; crossing and extremum counts above the A3 rate at every rho: {'yes' if above_ok else 'no'}: {_hf(check)}",
                    out=out,
                    reading=f"the source row's 'the cut fires on nothing at the noise's own rate' becomes a formula: at rho = 0 the occasion rate is twice the noise centroid ({grid[0][1]:.5f} against {2 * fbar:.5f}) and it moves to twice the signal frequency as e^(-rho^2/8), so a signal one step above the noise (rho = 1) has already moved the count {(2 * fbar - grid[3][1]) / (2 * fbar - 2 * fs):.3f} of the way and a signal at rho = 4 {(2 * fbar - grid[5][1]) / (2 * fbar - 2 * fs):.3f} of the way; the oriented count is not the crossing count (T-G: {crr_r:.5f} against {null_r:.5f}; in excess over the signal {crr_x:.5f} against {null_x:.5f}), and what it is, the mean instantaneous frequency with D1's rho as the square root of eight times the signal-to-noise ratio, is Rice's. The synthesis reading is {out}",
                    weakness="1-D, analytic-signal phase (which intrinsic phase A3 cuts on is the INTERNAL of batch 07 row 3); the noise is centred away from the signal so that the two rates differ; the law is exact for Gaussian noise and the closed form is derived here, with Rice 1948 cited by name and year only, not fetched (R10); the white-noise case is printed to show the sampling rule doing its work, not as a reading of A3",
                    elegance="Even silence, counted in half-turns, has a rate: the average pitch of the hiss. A faint signal does not add occasions, it bends that rate toward its own, and how far it bends is set by how many steps above the hiss it stands.",
                    child="Radio hiss still wobbles up and down at some average speed. If a quiet whistle is hidden in the hiss, the wobble speed drifts toward the whistle's note, and the louder the whistle, the closer it gets. So counting wobbles on an empty channel does not give zero; it gives the hiss's own speed.")


# ---------------------------------------------------------------- 3 three events: the local statistic
def r3():
    rng = np.random.default_rng(0); m = 200000
    X = rng.exponential(1.0, (m, 2))
    inst = np.sqrt(2.0) * np.abs(X[:, 0] - X[:, 1]) / (X[:, 0] + X[:, 1])       # the instrument's cv on two values, closed form
    inst_direct = np.array([cv(r) for r in X[:2000]])
    cv2 = 2.0 * np.abs(X[:, 1] - X[:, 0]) / (X[:, 1] + X[:, 0])
    ident = float(np.max(np.abs(inst_direct - cv2[:2000] / math.sqrt(2.0))))
    e_inst, e_cv2 = float(inst.mean()), float(cv2.mean())
    B = rng.exponential(1.0, (m, 2)); cvb = np.sqrt(2.0) * np.abs(B[:, 0] - B[:, 1]) / (B[:, 0] + B[:, 1])
    p_win = float(np.mean(inst < cvb))
    ecv = {}
    for k in (2, 3, 5, 10, 100):
        Y = rng.exponential(1.0, (20000, k)); ecv[k] = float(np.mean(np.std(Y, axis=1, ddof=1) / Y.mean(axis=1)))
    floors = {k: float(binomtest(k, k, 0.5, alternative="two-sided").pvalue) for k in (3, 4, 5, 6)}
    x = np.sin(np.linspace(0, 4 * math.pi, 400)); r = regularity(x, np.array([0, 100, 199]), sigma=1.0)
    # a carrier whose arc drifts slowly while the clock jitters: the local and the global reading
    n_occ = 100; arc = np.linspace(1.0, 1.5, n_occ); clock = 1.0 + 0.05 * rng.standard_normal(n_occ)
    g_arc, g_clock = cv(arc), cv(clock)
    l_arc = float(np.mean([cv(arc[i:i + 2]) for i in range(n_occ - 1)])); l_clock = float(np.mean([cv(clock[i:i + 2]) for i in range(n_occ - 1)]))
    g_cls = "arc-regular" if g_arc < g_clock else "clock-regular"; l_cls = "arc-regular" if l_arc < l_clock else "clock-regular"
    opposite = l_cls != g_cls
    check = ident < 1e-12 and rel(e_inst, e_cv2 / math.sqrt(2.0)) <= TOL_N and opposite
    out = outcome(crr=e_inst, null=e_cv2 / math.sqrt(2.0), domain=1.0 / math.sqrt(2.0), check=check)
    return make_row("neuro", "Three events (two occasions) under the instrument's regularity statistic, read in the spike-train domain where the two-interval statistic has a name: Holt's CV2 = 2 |I_2 - I_1| / (I_2 + I_1) (Holt, Softky, Koch and Douglas 1996), the local measure built to remove slow rate modulation from the global CV; Poisson intervals as the domain's null, 200000 pairs, seed 0",
                    source="theory/retrodictions/emptiness.txt [11] (DESCR)",
                    Q="the regularity statistic at its minimum count is the domain's CV2 divided by sqrt 2, on the arc and on the clock alike; under the domain's Poisson null its expectation is 1/sqrt 2 (E[CV2] = 1), so a three-event unit under-reads irregularity by the same factor on both sides, its H-L5 verdict has probability 1/2 under exchangeability, and what it can say is the local thing: on a carrier whose arc drifts slowly under a jittered clock the three-event reading and the all-events reading give opposite classes",
                    ingredient="H-L5's per-unit CV (R6) at n = 2 occasions; no CRR-proper ingredient does work in Q (the statistic is the domain's, and the class claim needs the count it lacks)",
                    null="Holt's CV2 / sqrt 2 on the same two intervals",
                    domain="Holt et al. 1996 (CV2); E[CV2] = 1 for a Poisson process (I_1 / (I_1 + I_2) is uniform, so CV2 = 2 |2U - 1|); the exact sign test's floor p = 2^(1 - n) for n units all won",
                    numbers=f"identity cv(I_1, I_2) = CV2 / sqrt 2: max |difference| {ident:.1e} over 2000 pairs; Poisson pairs: E[instrument cv] = {e_inst:.4f}, E[CV2] / sqrt 2 = {e_cv2 / math.sqrt(2.0):.4f}, 1/sqrt 2 = {1 / math.sqrt(2):.4f}; E[cv] at n occasions: " + ", ".join(f"n = {k}: {v:.4f}" for k, v in ecv.items()) + f" (the asymptote is 1); P(cv_arc < cv_clock) for two exchangeable Poisson pairs: {p_win:.4f}; exact two-sided sign-test p with every unit won: " + ", ".join(f"n = {k}: {v:.4f}" for k, v in floors.items()) + f"; the source row's three-event unit: cv_arc {r['cv_arc']:.4f}, cv_clock {r['cv_clock']:.4f}, paired-bootstrap CI of the difference [{r['ci95'][0]:.4f}, {r['ci95'][1]:.4f}] (includes 0: {r['ci95'][0] <= 0 <= r['ci95'][1]}); drifting arc (1 -> 1.5 over {n_occ} occasions) under a 5 % jittered clock: global CV(arc) {g_arc:.4f} vs CV(clock) {g_clock:.4f} ({g_cls}), mean three-event cv(arc) {l_arc:.4f} vs cv(clock) {l_clock:.4f} ({l_cls})",
                    tg=f"E[cv] at two occasions {e_inst:.4f} vs null E[CV2] / sqrt 2 {e_cv2 / math.sqrt(2.0):.4f}: {_ad(e_inst, e_cv2 / math.sqrt(2.0))} (identity to {ident:.1e})",
                    tn=f"the domain's E[CV2] = 1 gives {1 / math.sqrt(2):.4f}: {_ad(e_inst, 1 / math.sqrt(2), TOL_N)} (the domain has the statistic and its null value)",
                    tc=f"identity below 1e-12 and expectation within 1 % of 1/sqrt 2, and the local and global classes of the drifting carrier differ ({'yes' if opposite else 'no'}): {_hf(check)} (the first two are a definition)",
                    out=out,
                    reading=f"below the count at which a class can be scored, the instrument's statistic is the domain's local CV2 (to a factor sqrt 2), its Poisson expectation {e_inst:.4f} rather than the asymptotic 1, and its verdict a coin ({p_win:.4f}); what three events can say is the local thing, and the domain built CV2 to say exactly that: on the drifting carrier the local reading is {l_cls} while the global reading is {g_cls}; the source row's 'silence enforced by the instrument' is right, and the domain has the statistic the silence leaves. The synthesis reading is {out}",
                    weakness="the drifting carrier is a construction (a slow arc drift and a jittered clock), included to show that the three-event reading is local, not to grade a class; H-L5 as written is the global CV across occasions, so the local reading is the domain's, not CRR's; Holt et al. 1996 by name and year only, not fetched (R10)",
                    elegance="Two steps can tell you whether they matched each other; they can never tell you whether the walker is steady. The smallest question has a name in the spike-train literature, and it is the local one.",
                    child="If you hear only two heartbeats, you can say whether the gap between them was about the same as the one before, and that is all. To say whether a heart is steady you need many beats. Doctors and brain scientists use the two-beat question on purpose, because it ignores slow speeding up and slowing down.")


# ---------------------------------------------------------------- 4 zero surplus against one reversal: kinematic hardening
def _af_path(eps_path, c, gam, n=20000):
    """Armstrong-Frederick dX = c d(eps_p) - gam X |d(eps_p)| along a piecewise-linear plastic-strain path; RK4 on the arc parameter."""
    X, p = 0.0, 0.0
    for e0, e1 in zip(eps_path[:-1], eps_path[1:]):
        de = (e1 - e0) / n
        f = lambda X_: c * de - gam * X_ * abs(de)
        for _ in range(n):
            k1 = f(X); k2 = f(X + 0.5 * k1); k3 = f(X + 0.5 * k2); k4 = f(X + k3)
            X += (k1 + 2 * k2 + 2 * k3 + k4) / 6.0; p += abs(de)
    return X, p


def r4():
    c, gam, sy = 20000.0, 200.0, 100.0
    mono = np.array([0.0, 0.02]); rev = np.array([0.0, 0.03, 0.02])
    Xm, pm = _af_path(mono, c, gam); Xr, pr = _af_path(rev, c, gam)
    Xm_c = (c / gam) * (1 - math.exp(-gam * 0.02)); X1 = (c / gam) * (1 - math.exp(-gam * 0.03)); Xr_c = -c / gam + (X1 + c / gam) * math.exp(-gam * 0.01)
    Pm, Pr = c * mono[-1], c * rev[-1]
    sm, sr = surplus(mono, sigma=1.0), surplus(rev, sigma=1.0)
    d_af, d_pr, d_cl = Xr - Xm, Pr - Pm, Xr_c - Xm_c
    check = abs(Xm - Xm_c) < 1e-6 and abs(Xr - Xr_c) < 1e-6 and d_pr == 0.0
    out = outcome(crr=d_af, null=d_pr, domain=d_cl, check=check)
    return make_row("mat", f"Kinematic hardening in metal plasticity: the backstress X under the Armstrong-Frederick rule dX = c d(eps_p) - gamma X |d(eps_p)| (c = {c:g} MPa, gamma = {gam:g}) against Prager's linear rule X = c eps_p, on the source row's two paths in plastic strain: a monotone ramp 0 -> 0.02 (S = 0) and a ramp with one reversal 0 -> 0.03 -> 0.02 (the same endpoint, S = 0.02); RK4 on the arc parameter, 20000 steps per segment; the reversal's named effect is Bauschinger's",
                    source="theory/retrodictions/emptiness.txt [13] (DESCR)",
                    Q="the material's memory of its loading direction (the backstress, which sets where it yields on reversal) is a function of the arc travelled, the domain's accumulated plastic strain p = integral |d(eps_p)|, and not of the endpoint: two paths with the same endpoint plastic strain and different surplus end at different backstresses, by an amount the recovery term fixes, and under the endpoint-only (Prager) rule the difference is zero",
                    ingredient="D6/H-T1 (path against endpoint: the memory decays with arc travelled, not with displacement), D5 (the reversal as the source row's boundary), D4 (S = the backtrack; not proper)",
                    null="Prager's linear kinematic hardening, X = c eps_p: a function of the endpoint alone",
                    domain="Armstrong and Frederick 1966 (Frederick and Armstrong 2007): on a monotone segment of arc dp the backstress relaxes to +-c/gamma as X = X_0 e^(-gamma dp) +- (c/gamma)(1 - e^(-gamma dp)); the accumulated plastic strain p is the model's own state variable (Chaboche 1986)",
                    numbers=f"monotone path: X = {Xm:.4f} MPa (closed form {Xm_c:.4f}), p = {pm:.4f}, (C, C*, S) = ({sm[0]:.4f}, {sm[1]:.4f}, {sm[2]:.1e}); reversal path: X = {Xr:.4f} MPa (closed form {Xr_c:.4f}), p = {pr:.4f}, (C, C*, S) = ({sr[0]:.4f}, {sr[1]:.4f}, {sr[2]:.4f}); Prager: X = {Pm:.4f} on both paths; backstress difference at the same endpoint: Armstrong-Frederick {d_af:.4f} (closed form {d_cl:.4f}), Prager {d_pr:.4f}; elastic range [X - sigma_y, X + sigma_y] with sigma_y = {sy:g}: [{Xm - sy:.2f}, {Xm + sy:.2f}] after the monotone path (reverse yield at {Xm - sy:.2f}, the Bauschinger effect), [{Xr - sy:.2f}, {Xr + sy:.2f}] after the reversal path; saturation c/gamma = {c / gam:.1f} MPa, saturation arc 1/gamma = {1 / gam:.4f}",
                    tg=f"backstress difference between the two paths {d_af:.4f} (Armstrong-Frederick, arc-driven recovery) vs null {d_pr:.4f} (Prager, endpoint only): {_ad(d_af, d_pr)}",
                    tn=f"the Armstrong-Frederick closed form gives {d_cl:.4f}: {_ad(d_af, d_cl, TOL_N)} (the domain has Q)",
                    tc=f"RK4 within 1e-6 of the closed form on both paths and Prager's difference exactly 0: {_hf(check)}",
                    out=out,
                    reading=f"the source row's two paths, put into a domain where a reversal has a name, separate cleanly: the same endpoint carries a backstress of {Xm:.2f} MPa after the monotone path and {Xr:.2f} MPa after the reversal (T-G: {d_af:.2f} against Prager's {d_pr:.2f}), so the material's memory tracks the road and not the place, which is H-T1's sentence; and the road is the domain's accumulated plastic strain, the state variable of the nonlinear kinematic-hardening laws since 1966, so the domain has Q with the closed form to match ({d_cl:.4f}). CRR renames p as the arc. The synthesis reading is {out}",
                    weakness="the model's path dependence runs through p and the order of the segments, not through S alone (two paths with equal S and endpoint but a different reversal order are not compared here); the unit is the strain itself, no A1' estimate; Prager as the endpoint null is the domain's own older model, so T-G compares two domain rules; citations by name and year only, not fetched (R10)",
                    elegance="Bend a paperclip and it remembers not where it is but how far it has been bent, out and back counted together: a paperclip counts road, not distance. One rule, no knobs, and it is why a bent clip gives way more easily when bent back.",
                    child="Bend a paperclip a little one way and it gets stubborn in that direction. Bend it far and then part-way back, so it ends up in the same place as before, and now it is stubborn the other way. The clip does not remember where it is; it remembers how much bending it has been through.")


# ---------------------------------------------------------------- 5 D6's step on a named learner: separable logistic regression
def _sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def _klb(p, q):
    return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))


def r5():
    eta, T = 0.5, 20000; probe = np.array([0.5, 1.0, 1.5, 2.0])
    w, ws = 0.0, [0.0]
    for _ in range(T):
        w -= eta * (-(1.0 - _sig(w))); ws.append(w)                 # loss = mean over x = +1 (y = 1) and x = -1 (y = 0) of -log sigmoid(y w x): gradient -(1 - sigmoid(w))
    ws = np.asarray(ws)
    snaps = [np.column_stack([_sig(w_ * probe), 1.0 - _sig(w_ * probe)]) for w_ in ws]
    pl = path_length(snaps, kl=kl_step)
    C_rev = sum(math.sqrt(2 * kl_step(b, a)) for a, b in zip(snaps[:-1], snaps[1:]))
    C_jef = sum(math.sqrt(kl_step(a, b) + kl_step(b, a)) for a, b in zip(snaps[:-1], snaps[1:]))
    def g(w_):
        p = _sig(w_ * probe); return float(np.mean(probe ** 2 * p * (1 - p)))
    L_exact = quad(lambda w_: math.sqrt(g(w_)), 0.0, float(ws[-1]), limit=500)[0]
    L_inf = quad(lambda w_: math.sqrt(g(w_)), 0.0, 200.0, limit=500)[0]
    eucl = float(ws[-1] - ws[0]); ln_eta_T = math.log(eta * T)
    p0, p1 = 0.1, 0.6; dfr = abs(2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p0))); conv = []
    for N in (4, 16, 64, 256):
        ps = np.linspace(p0, p1, N + 1)
        Cf = sum(math.sqrt(2 * _klb(a, b)) for a, b in zip(ps[:-1], ps[1:])); Cb = sum(math.sqrt(2 * _klb(b, a)) for a, b in zip(ps[:-1], ps[1:]))
        Cj = sum(math.sqrt(_klb(a, b) + _klb(b, a)) for a, b in zip(ps[:-1], ps[1:])); conv.append((N, Cf - dfr, Cb - dfr, Cj - dfr))
    ratio_f = conv[-2][1] / conv[-1][1]; ratio_b = conv[-2][2] / conv[-1][2]; ratio_j = conv[-2][3] / conv[-1][3]
    orders_ok = (3.5 < ratio_f < 4.5) and (3.5 < ratio_b < 4.5) and (14 < ratio_j < 18) and (conv[-1][1] < 0 < conv[-1][2])
    check = orders_ok and rel(pl["C"], L_exact) <= TOL_G and pl["C"] < L_inf and eucl > 5 * L_inf and pl["S"] < 0
    out = outcome(crr=pl["C"], null=L_exact, domain=None, check=check)
    return make_row("learn", f"Logistic regression on linearly separable data (x = +-1 with matching labels, one weight w) under gradient descent (learning rate {eta:g}, {T} steps), the named case in which the parameter diverges as ln t (Soudry, Hoffer, Nacson, Gunasekar and Srebro 2018, the implicit bias of gradient descent); D6's path length on a probe of four inputs against the exact Fisher-Rao length of the same predictive path in the probe-averaged metric, with the reverse-oriented and the symmetrised (Jeffreys) steps; convergence orders on a Bernoulli path {p0:g} -> {p1:g}",
                    source="theory/retrodictions/shannon.txt [1] (DESCR)",
                    Q="D6's C = sum sqrt(2 KL_t) is the Fisher-Rao length of the predictive path to first order in the step for either orientation (errors of opposite sign, each falling as 1/N) and to second order for the symmetrised step; on the separable run the predictive path has finite Fisher-Rao length, bounded by the distance to certainty, while the parameter path diverges as ln(eta t); and C* = sqrt(2 E) is not the chord: on this monotone path it exceeds the arc, so the estimator's S is negative where the geometry's is zero",
                    ingredient="D6 (the path in KL steps on a fixed probe, H-T1's quantity); no CRR-proper ingredient does work in Q: the arc, the chord and their discretisation are information geometry's (Kullback's second-order identity), which is the source row's content",
                    null="the exact Fisher-Rao length integral sqrt(mean_probe g(w)) dw of the same path, information geometry alone",
                    domain="Kullback 1959 (KL(p_theta || p_theta+d) = (1/2) g d^2 + O(d^3)); Soudry et al. 2018 (w_t = ln t + o(ln t) on separable data); no domain theorem is cited for the same target as T-G, which is the identity itself",
                    numbers=f"w_T = {ws[-1]:.4f} (ln(eta T) = {ln_eta_T:.4f}); D6 path on the probe: C (forward, the instrument) = {pl['C']:.4f}, reverse orientation {C_rev:.4f}, Jeffreys {C_jef:.4f}, exact Fisher-Rao length {L_exact:.4f} (relative difference of C {rel(pl['C'], L_exact):.4f}); Fisher-Rao length to certainty (w -> infinity) {L_inf:.4f}; Euclidean parameter path {eucl:.4f}; endpoint E = KL(p_0 || p_T) = {pl['E']:.4f}, C* = sqrt(2 E) = {pl['Cstar']:.4f}, S = C - C* = {pl['S']:.4f} on a monotone path (the exact chord equals the exact length {L_exact:.4f}); Bernoulli path {p0:g} -> {p1:g}, error of the summed step against the exact length: " + "; ".join(f"N = {N}: forward {ef:+.3e}, reverse {eb:+.3e}, Jeffreys {ej:+.3e}" for N, ef, eb, ej in conv) + f"; error ratios from N = 64 to 256: forward {ratio_f:.2f}, reverse {ratio_b:.2f}, Jeffreys {ratio_j:.2f} (first order 4, second order 16)",
                    tg=f"C {pl['C']:.4f} vs null exact Fisher-Rao length {L_exact:.4f}: {_ad(pl['C'], L_exact)} (no CRR-proper ingredient in Q)",
                    tn="none cited for the same target: the second-order identity is the domain's, and T-G already decides",
                    tc=f"orders (forward and reverse ratios near 4 with opposite signs, Jeffreys near 16), C within 1 % of the exact length and below the length to certainty, parameter path more than five times the bound, S < 0: {_hf(check)} (and every item is information geometry's)",
                    out=out,
                    reading=f"the source row's content is exactly this: D6's step is Kullback's identity, and on a named learner the identity holds to {rel(pl['C'], L_exact):.4f} while the domain's own divergence (the parameter, {eucl:.4f} against a predictive path bounded by {L_inf:.4f}) shows why the path is measured on the predictive and not on the weights; the one number CRR should notice is S = {pl['S']:.4f} on a monotone path: sqrt(2 E) is the chord only to second order, so D6's surplus is not P1's surplus at finite displacement and its sign distribution must be reported (the instrument's docstring says so). The synthesis reading is {out}",
                    weakness="a one-parameter model, so the predictive path is monotone by construction and the surplus question is only the estimator's; the probe-averaged metric is the instrument's reading of 'averaged over the probe' (the per-probe mean of distances is smaller by Jensen and not computed here); Soudry et al. 2018 and Kullback 1959 by name and year only, not fetched (R10)",
                    elegance="You can walk forever in the space of weights and get nowhere new in what the model predicts: once it is sure, more sureness is not more distance. Measured where it matters, the road to certainty is short and has an end.",
                    child="A model that is already sure of its answer keeps making its numbers bigger and bigger for ever, but its answers stop changing. If you measure how far it has travelled by its answers instead of by its numbers, the trip is short and it ends.")


def main():
    return run_batch("Synthesis batch 22: rows 106-110 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
