"""Synthesis batch 17: rows 81-85 of QUEUE.md (prompt-log entry 61). Cognitive-collective battery [9] Bass diffusion of
an innovation, the adoption wave as one occasion (DESCR); wild-systems battery [2] handwriting strokes (minimum-jerk),
the isochrony principle vs constant-speed timing (DESCR); [5] immune imprinting (antigenic seniority), measured
influence of each exposure (DESCR; the queue asks whether A6 with any MaxEnt weight can produce primacy, computed);
[6] maintenance scheduling, odometer (usage-based) vs calendar intervals (DESCR); [7] dripping tap, Tate's-law drops
under variable flow vs variable pinch-off (DESCR). Source rows in theory/retrodictions/cognitive_collective.txt and
theory/retrodictions/wild_systems.txt; their models are re-implemented here (nothing imported from the battery
scripts). Deterministic (fixed seeds, fixed grids, explicit RK4); no data file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_17.py
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.special import gamma as Gamma, gammaincc

from crr.instrument.core import cv, regularity, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC_COG = "theory/retrodictions/cognitive_collective.txt"
SRC_WILD = "theory/retrodictions/wild_systems.txt"


def _word(cond, yes, no):
    return yes if cond else no


def _agree(a, b, tol=TOL_G):
    return _word(rel(a, b) <= tol, "agree", "differ")


# ---------------------------------------------------------------- 81 [cog 9] Bass diffusion with P3-weighted word of mouth
def _bass_fading(p, q, kappa, dt=0.001, t_max=60.0):
    """dF/dt = (p + q W)(1 - F), dW/dt = dF/dt - kappa W: the imitation pressure is the kernel-weighted adopter fraction
    W(t) = int kappa e^{-kappa (t - s)} dF(s) (P3 age weights, bounded strength W <= F) instead of the accumulated
    fraction F; kappa = 0 is the Bass model (W = F). Fixed-grid RK4."""
    n = int(round(t_max / dt)); F = np.empty(n + 1); W = np.empty(n + 1); F[0] = W[0] = 0.0

    def rhs(f, w):
        df = (p + q * w) * (1.0 - f)
        return df, df - kappa * w

    f, w = 0.0, 0.0
    for i in range(n):
        k1 = rhs(f, w); k2 = rhs(f + 0.5 * dt * k1[0], w + 0.5 * dt * k1[1])
        k3 = rhs(f + 0.5 * dt * k2[0], w + 0.5 * dt * k2[1]); k4 = rhs(f + dt * k3[0], w + dt * k3[1])
        f += dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0; w += dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        F[i + 1] = f; W[i + 1] = w
    t = dt * np.arange(n + 1); dF = (p + q * W) * (1.0 - F)
    return t, F, W, dF


def r1():
    p, q = 0.03, 0.38                                                   # the source's Bass coefficients (per year)
    F_star, t_star = (q - p) / (2 * q), math.log(q / p) / (p + q)       # Bass 1969: peak fraction and peak time
    grid = (0.0, 0.1, 0.3, 1.0)                                         # kernel rate kappa per year (mean age of the weight 1/kappa)
    res = []
    for kappa in grid:
        t, F, W, dF = _bass_fading(p, q, kappa)
        k = int(np.argmax(dF)); Fk, Wk = F[k], W[k]
        hk = p + q * Wk
        peak_rel = abs(q * (1.0 - Fk) * hk - q * kappa * Wk - hk * hk) / (hk * hk)   # F'' = 0 in the model's own calculus
        gap = q * (W - F)                                                 # hazard F'/(1 - F) minus the Bass line p + q F
        i_half = int(np.argmin(np.abs(F - 0.5)))
        curv0 = (dF[1] - dF[0]) / (t[1] - t[0])                           # F''(0) numerically; p (q - p) in closed form
        q_eff = p / (1.0 - 2.0 * Fk)                                      # the Bass q that would give this peak fraction
        t_eff = math.log(q_eff / p) / (p + q_eff)                         # ... and its Bass peak time
        res.append(dict(kappa=kappa, t=float(t[k]), F=float(Fk), W=float(Wk), peak_rel=float(peak_rel), gap_max=float(gap[1:].max()),
                        gap_half=float(gap[i_half]), curv0=float(curv0), q_eff=float(q_eff), t_eff=float(t_eff)))
    bass, crr_row = res[0], res[2]
    curv_ok = all(rel(r["curv0"], p * (q - p)) <= 0.01 for r in res)
    below = all(r["gap_max"] <= 1e-9 and r["gap_half"] < 0 for r in res[1:])
    lower = all(r["F"] < F_star - 0.005 for r in res[1:])
    rel_ok = all(r["peak_rel"] <= 1e-3 for r in res)
    check = curv_ok and below and lower and rel_ok
    out = outcome(crr=crr_row["F"], null=bass["F"], domain=F_star, check=check)
    later = all(r["t"] > bass["t"] for r in res[1:])
    not_bass = all(rel(r["t"], r["t_eff"]) > TOL_G for r in res[1:])
    return make_row("soc", "Bass diffusion of an innovation (p = 0.03, q = 0.38 per year, the source's coefficients) with the imitation pressure on a non-adopter taken as the P3 kernel-weighted adopter fraction W (rate kappa) instead of the accumulated adopted fraction F; occasion = one adoption (D5 [M] for a point process); fixed-grid RK4, dt = 0.001, t in [0, 60]",
        source=f"{SRC_COG} [9] (DESCR)",
        Q="if the settled adoptions act on the next one through a bounded age-weighted content (A6: reweighted, never an accumulated count) the Bass plot, hazard F'/(1 - F) against F, bends below the line p + q F, the peak of the wave comes at a lower adopted fraction than (q - p)/(2 q), and the condition for an interior peak, q > p, is unchanged (F''(0) = p (q - p) for every kappa); the Bass model is the kappa = 0 member",
        ingredient="A6 (the next occasion seeded from the settled past at bounded strength, never an accumulated count) with P3 (exponential age weights, rate kappa), D5 [M] (occasion = one adoption)",
        null="kappa = 0: the Bass model, whose imitation term q F is the accumulated count of settled adoptions",
        domain="Bass 1969: the adoption rate peaks at t* = ln(q/p)/(p + q) with F* = (q - p)/(2 q) adopted, and the hazard is linear in F (the Bass plot, the basis of the OLS fit of p and q)",
        numbers=f"Bass closed form: F* = {F_star:.4f}, t* = {t_star:.4f}; " + "; ".join(
            f"kappa = {r['kappa']:g}: peak at t = {r['t']:.3f}, F = {r['F']:.4f} (W = {r['W']:.4f}), hazard - Bass line: max {r['gap_max']:.1e}, at F = 0.5 {r['gap_half']:.4f}; F''(0) = {r['curv0']:.5f} (p (q - p) = {p * (q - p):.5f}); peak relation residual {r['peak_rel']:.1e}; a Bass model with the same peak fraction would need q = {r['q_eff']:.4f} and peak at t = {r['t_eff']:.3f}"
            for r in res),
        tg=f"peak fraction {crr_row['F']:.4f} (kappa = {crr_row['kappa']:g}) vs null {bass['F']:.4f} (kappa = 0, the accumulated count): {_agree(crr_row['F'], bass['F'])}",
        tn=f"Bass's theorem gives F* = {F_star:.4f} (the null reproduces it: relative difference {rel(bass['F'], F_star):.1e}); for kappa > 0 it gives {_word(rel(crr_row['F'], F_star) <= TOL_N, 'the same value', 'a different value')}, so the domain {_word(rel(crr_row['F'], F_star) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"F''(0) within 1 % of p (q - p) at every kappa: {_word(curv_ok, 'yes', 'no')}; hazard at or below the Bass line everywhere and strictly below at F = 0.5 for every kappa > 0: {_word(below, 'yes', 'no')}; peak fraction below F* by more than 0.005 for every kappa > 0: {_word(lower, 'yes', 'no')}; the peak satisfies the model's own F'' = 0 relation to 1e-3: {_word(rel_ok, 'yes', 'no')}: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=f"integrated with the domain's own equation, the regeneration axiom makes a definite statement the Bass model does not: word of mouth that fades with the age of the adoption bends the Bass plot below its line and moves the peak to a lower adopted fraction ({bass['F']:.4f} at kappa = 0 to {res[1]['F']:.4f}, {res[2]['F']:.4f}, {res[3]['F']:.4f} at kappa = {grid[1]:g}, {grid[2]:g}, {grid[3]:g}) and {_word(later, 'later', 'earlier')} in time, while the existence of a peak still needs only q > p; the bent model is not a Bass model with a smaller q (the q that matches the peak fraction puts the peak at a different time at every kappa: {_word(not_bass, 'yes', 'no')}), so the data test is the straightness of the Bass plot; the label is a candidate only: whether the diffusion literature's non-uniform-influence or decaying word-of-mouth models already contain this is the expert's question (protocol section 4)",
        weakness="kappa is not fixed by CRR (P3), so the row prints a grid; any exponential-kernel memory on the adopter count gives the same bending, so the CRR content is the weights' shape and the bounded strength (the same reading of A6 as batch 12 row 2 and synthesis row 8); W is a bounded weighted sum, not the normalised Frechet mean A6 names (on a carrier whose occasion content is 'adopted' the normalised mean is 1); the domain has non-uniform-influence models (Easingwood, Mahajan and Muller 1983, by name and year only, not fetched, R10) in which the imitation term is not linear in F, so the expert's answer to question 1 may be yes; the check is in the model, the data test (Bass's own eleven durables series, absent from data/SEEN.md) is not run here",
        elegance="", child="")


# ---------------------------------------------------------------- 82 [wild 2] handwriting: the arc in the motor system's own unit
def r2():
    rng = np.random.default_rng(2); n = 200                             # the source's draw: 200 strokes, lognormal amplitude, 5 % timing noise
    A = np.exp(0.5 * rng.standard_normal(n)); noise = 1.0 + 0.05 * rng.standard_normal(n)
    laws = (("isochrony (T fixed)", np.ones(n)), ("constant peak speed (T ~ A)", A.copy()), ("empirical T ~ A^0.25", A ** 0.25))
    b = 0.1                                                             # Schmidt's slope (a scale; the CVs do not depend on it)
    sig_rec = unit_sigma(A)                                             # A1' as implemented: one sigma per record from the amplitude residual
    res = []
    for name, T0 in laws:
        T = T0 * noise
        for a_frac in (0.0, 0.25):
            a = a_frac * b * float(np.mean(A / T))                      # intercept of the speed-accuracy line, as a fraction of the mean spread
            sig = a + b * A / T                                         # Schmidt et al. 1979: effective target width W_e = a + b A / MT
            res.append(dict(law=name, a_frac=a_frac, cv_own=cv(A / sig), cv_out=cv(A / sig_rec), cv_T=cv(T), cv_A=cv(A)))
    iso = res[0]                                                        # isochrony, a = 0: the decisive cell
    crr, null, dom = iso["cv_own"], iso["cv_out"], iso["cv_T"]
    exact = all(rel(r["cv_own"], r["cv_T"]) <= 1e-9 for r in res if r["a_frac"] == 0.0)
    check = exact
    out = outcome(crr=crr, null=null, domain=dom, check=check)

    def cls(ca, cc):
        d = ca - cc
        return "tie" if abs(d) < 1e-3 else _word(d < 0, "arc-regular", "clock-regular")

    return make_row("motor", "Handwriting strokes of random amplitude A (lognormal, 200 strokes, the source's draw) under three timing laws (isochrony, constant peak speed, T ~ A^0.25), read in the motor system's own unit: Schmidt's law, effective endpoint spread W_e = a + b A / T",
        source=f"{SRC_WILD} [2] (DESCR)",
        Q="measured in the motor system's own resolvable step (A1': the endpoint spread of the stroke, which Schmidt's law makes proportional to its speed A / T), every stroke has arc A / W_e = T / b, so the arc in own units is the clock itself for every timing law: an isochronous hand is arc-regular in its own unit, and H-L5's comparison is a tie by identity rather than a clock-regular verdict",
        ingredient="A1'/D1 (the unit is the system's own resolvable step, here the stroke's endpoint spread; arc in units of sigma), H-L5 (the class claim), D5 (occasion = one stroke), D2 (the stroke is monotone: arc = A)",
        null="the instrument's unit: one sigma per record from unit_sigma on the amplitude residual (A1' as implemented), an outside constant under which the arc is A itself",
        domain="Schmidt, Zelaznik, Hawkins, Frank and Quinn 1979 (the linear speed-accuracy trade-off): W_e = a + b (A / MT); with a = 0, A / W_e = MT / b exactly, so CV(arc in own units) = CV(MT)",
        numbers=f"sigma per record (unit_sigma, window 9, order 2, MAD) = {sig_rec:.4f}; CV(A) = {iso['cv_A']:.4f}; " + "; ".join(
            f"{r['law']}, a/b(A/T)_mean = {r['a_frac']:g}: CV(A / W_e) = {r['cv_own']:.4f}, CV(A / sigma_rec) = {r['cv_out']:.4f}, CV(T) = {r['cv_T']:.4f}, class in own unit {cls(r['cv_own'], r['cv_T'])}, in the record unit {cls(r['cv_out'], r['cv_T'])}"
            for r in res),
        tg=f"CV(arc in own unit) {crr:.4f} vs null CV(arc in the record unit) {null:.4f} (isochrony, a = 0): {_agree(crr, null)}",
        tn=f"Schmidt's law gives CV(A / W_e) = CV(T) = {dom:.4f}: {_agree(crr, dom, TOL_N)} (the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q)",
        tc=f"A / W_e = T / b to 1e-9 in CV under all three timing laws at a = 0: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=f"the unit does real work (T-G: {null:.4f} against {crr:.4f}) and what it produces is Schmidt's identity: a stroke's own resolvable step grows with its speed, so the arc counted in that step is the duration, and the source row's clock-regular verdict (CV(A) {iso['cv_A']:.4f} against CV(T) {iso['cv_T']:.4f}) becomes a tie under every timing law, not because the hand is arc-regular but because the unit absorbs the timing law; with an intercept in the speed-accuracy line the identity is only approximate (CV(A / W_e) = {res[1]['cv_own']:.4f} at a/b(A/T)_mean = 0.25) and the class returns toward the record-unit one. The synthesis reading is {out}",
        weakness="A1' as written takes one sigma per record from the residual across occasions (the null here); a per-stroke unit is A1''s motivation ('the smallest change the system itself resolves') read with signal-dependent noise, which the text does not license, the same named-against-estimated split as synthesis row 11 and batch 06 row 4; Schmidt's law is for rapid timed movements and its intercept is not zero in the data (a is a registered fraction here, not a fitted value); citation by name and year only, not fetched (R10)",
        elegance="A bigger stroke is a sloppier stroke, by exactly as much as it is bigger and faster. Counted in its own sloppiness every stroke is the same length, and that is the same sentence as 'every stroke takes the same time': one rule, no knobs, and the unit is the hand's, not the ruler's.",
        child="When you write a big letter as fast as a small one, your hand wobbles more. If you measure each letter in wobbles instead of in centimetres, the big letter and the small letter come out the same size. That is why they take the same time to write.")


# ---------------------------------------------------------------- 83 [wild 5] immune imprinting: can a MaxEnt age weight produce primacy?
def _maxent_age(target, n):
    """MaxEnt over ages k = 0..n-1 with <k> fixed at `target`: pi_k ∝ e^{-lambda k}; returns q = e^{-lambda} (any sign of lambda)."""
    k = np.arange(n)

    def mean_age(lam):
        w = np.exp(-lam * (k - k.mean())); return float((k * w).sum() / w.sum())

    lam = brentq(lambda l: mean_age(l) - target, -50.0, 50.0, xtol=1e-14)
    return math.exp(-lam)


def r3():
    rng = np.random.default_rng(5); s = 0.6; n = 6                       # the source's draw: six exposures, seniority weight s^(m-1)
    pos = np.cumsum(rng.uniform(0.5, 1.5, n)); test = pos[-1] + 0.5
    w = s ** np.arange(n); age = np.arange(n)[::-1]; k = np.arange(n)
    res = {}
    for name, sim in (("equal cross-reactivity", np.ones(n)), ("antigenic-distance kernel", np.exp(-np.abs(test - pos) / 2.0))):
        full = float(np.sum(w * sim)); infl = np.array([full - float(np.sum((w * sim)[np.arange(n) != i])) for i in range(n)])
        by_age = infl[np.argsort(age)]                                    # influence by age k = 0 (last exposure) .. 5 (first)
        mean_age = float((k * by_age).sum() / by_age.sum())
        q_fin = _maxent_age(mean_age, n)                                  # reading (i): MaxEnt on the finite settled history
        q_inf = mean_age / (1.0 + mean_age)                               # reading (ii): CRR.md P3, <k> = q/(1-q) (infinite horizon, q < 1)
        pi_fin = q_fin ** k / (q_fin ** k).sum(); pi_inf = q_inf ** k / (q_inf ** k).sum()
        mean_inf = float((k * pi_inf).sum())                              # the mean age reading (ii)'s profile actually has on six occasions
        fit_err = float(np.max(np.abs(pi_fin - by_age / by_age.sum())))  # MaxEnt profile against the measured influence profile
        slope, icpt = np.polyfit(k, np.log(by_age), 1); r2 = 1.0 - float(np.var(np.log(by_age) - (slope * k + icpt)) / np.var(np.log(by_age)))
        turns = int(np.sum(np.diff(np.sign(np.diff(by_age))) != 0))       # sign changes of the profile's slope: 0 for any one-constraint MaxEnt
        res[name] = dict(infl=by_age, mean_age=mean_age, q_fin=q_fin, q_inf=q_inf, mean_inf=mean_inf, fit_err=fit_err, r2=r2, turns=turns)
    eq = res["equal cross-reactivity"]; ker = res["antigenic-distance kernel"]
    internal = rel(eq["q_fin"], eq["q_inf"]) > TOL_G
    out = outcome(internal=internal)
    primacy_fin = eq["q_fin"] > 1.0
    return make_row("immu", "Immune imprinting as antigenic seniority (the source's model: six exposures, response weight s^(m-1) with s = 0.6, influence of each settled exposure measured by removal, with and without an antigenic-distance kernel), asked whether A6's MaxEnt age weight (P3) can produce a primacy profile",
        source=f"{SRC_WILD} [5] (DESCR)",
        Q="primacy is not a third memory class outside P3 but its lambda < 0 branch: MaxEnt over the settled exposures with the mean age fixed above the midpoint of the history gives geometric weights with q > 1, and with the mean age of the seniority profile it returns q = 1/s exactly; CRR.md's normalisation <k> = q/(1 - q) is the infinite-horizon, q < 1 form and cannot represent it",
        ingredient="A6 (weights are a MaxEnt distribution over occasions subject to one history constraint) with P3 (mean age fixed) in two readings: (i) MaxEnt on the finite settled history (n = 6 occasions, any sign of the multiplier), (ii) CRR.md's closed form <k> = q/(1 - q)",
        null="P2 (surplus weights): every exposure has the same surplus, so the weights are uniform (q = 1, mean age 2.5), the source row's own finding",
        domain="antigenic seniority (Lessler et al. 2012 as the seniority form): the response weight of the m-th exposure is s^(m-1), i.e. geometric in age with ratio 1/s",
        numbers=f"equal cross-reactivity: influence by age (last exposure first) = {', '.join(f'{v:.3f}' for v in eq['infl'])}, mean age {eq['mean_age']:.4f} (midpoint of six occasions 2.5); reading (i) finite-history MaxEnt q = {eq['q_fin']:.6f} (1/s = {1 / s:.6f}, max profile error {eq['fit_err']:.1e}); reading (ii) q = <k>/(1 + <k>) = {eq['q_inf']:.4f}, whose six-occasion profile has mean age {eq['mean_inf']:.4f}, not {eq['mean_age']:.4f}; log-linear R^2 of influence on age {eq['r2']:.4f}, slope sign changes {eq['turns']}. antigenic-distance kernel: influence by age = {', '.join(f'{v:.3f}' for v in ker['infl'])}, mean age {ker['mean_age']:.4f}; reading (i) q = {ker['q_fin']:.4f} (max profile error {ker['fit_err']:.4f}), reading (ii) q = {ker['q_inf']:.4f}; log-linear R^2 {ker['r2']:.4f}, slope sign changes {ker['turns']} (a one-constraint MaxEnt profile is monotone: 0 sign changes)",
        tg=f"reading (i) q = {eq['q_fin']:.4f} vs reading (ii) q = {eq['q_inf']:.4f} (equal cross-reactivity): {_agree(eq['q_fin'], eq['q_inf'])} (the ingredient has two values on the domain); against the null (uniform, q = 1): reading (i) {_agree(eq['q_fin'], 1.0)}",
        tn=f"the seniority definition gives q = 1/s = {1 / s:.4f}; reading (i) reproduces it (relative difference {rel(eq['q_fin'], 1 / s):.1e}), reading (ii) does not (relative difference {rel(eq['q_inf'], 1 / s):.4f})",
        tc="not reached: the two readings of P3 must agree before Q can be checked",
        out=out,
        reading=f"the queue's question has a computed answer: A6 with the P3 constraint {_word(primacy_fin, 'does', 'does not')} produce primacy on a finite history (q = {eq['q_fin']:.4f} > 1 because the seniority profile's mean age {eq['mean_age']:.4f} lies above the midpoint 2.5, so the Lagrange multiplier is negative), and the profile it returns is the seniority model itself, so under reading (i) the source row's third memory class is the sign of one multiplier and Q is the domain's own definition read back; under reading (ii), CRR.md's <k> = q/(1 - q), no q reproduces the profile (the closed form assumes an infinite past and q < 1), primacy is outside P3, and the source row's taxonomy stands; which P3 is has to be fixed before the domain can be asked, and it is a theory choice (v3.2). The distance-kernel profile turns ({ker['turns']} slope sign change{'s' if ker['turns'] != 1 else ''}) and no one-constraint MaxEnt weight is non-monotone: there the second constraint is the domain's similarity kernel, not age or surplus",
        weakness="the source's model encodes the answer (its own rule 3): the influence profile is geometric because the seniority weight is; the row shows only that P3's derivation, unlike its stated normalisation, contains that geometry with either sign; P2 is not tested because the toy gives every exposure the same surplus; citation by name and year only, not fetched (R10)",
        elegance="'First is strongest' and 'newest is strongest' are the same ladder read from opposite ends: one rule, each step a fixed fraction of the last, and only the direction differs.",
        child="Your body remembers the first flu it ever met best, and each later one a little less. That is the same rule as remembering the newest thing best, just turned upside down: each step back is the same fraction bigger instead of the same fraction smaller.")


# ---------------------------------------------------------------- 84 [wild 6] maintenance: A6 regeneration as Kijima's virtual age
def _kijima(kind, q, n, beta, eta, seed):
    """Weibull(beta, eta) baseline hazard; after the n-th failure the virtual age is V_n = q (V_{n-1} + X_n) (type II: the
    settled intervals re-weighted geometrically, bounded strength) or V_n = V_{n-1} + q X_n (type I: an accumulated count).
    X_n | V_{n-1} = v is drawn from the conditional Weibull: X = eta ((v/eta)^beta - ln U)^(1/beta) - v."""
    rng = np.random.default_rng(seed); U = rng.uniform(size=n); X = np.empty(n); v = 0.0
    for i in range(n):
        x = eta * ((v / eta) ** beta - math.log(U[i])) ** (1.0 / beta) - v; X[i] = x
        v = q * (v + x) if kind == "II" else v + q * x
    return X, v


def _kijima2_chain(q, beta, eta, n_grid=6001, z_max=60.0, n_iter=400):
    """The domain's own value for type II with beta = 2: Z = (V/eta)^2 obeys Z' = q^2 (Z + E), E ~ Exp(1); the stationary
    density is found by iterating the kernel on a grid; E[X | z] = eta (e^z Gamma(3/2, z) - sqrt z) in closed form."""
    assert beta == 2.0
    if q == 0.0:                                                          # perfect repair: Z = 0, a Weibull renewal process
        return float(eta * Gamma(1.5)), 0.0
    z = np.linspace(0.0, z_max, n_grid); dz = z[1] - z[0]
    f = np.exp(-z); f /= f.sum() * dz
    for _ in range(n_iter):
        G = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] * np.exp(z[1:]) + f[:-1] * np.exp(z[:-1])) * dz)])   # int_0^y f(z) e^z dz
        y = z / (q * q); Gy = np.interp(y, z, G, right=G[-1])
        f_new = np.exp(-y) * Gy / (q * q); f_new /= f_new.sum() * dz
        f = f_new
    ex_given_z = eta * (np.exp(z) * Gamma(1.5) * gammaincc(1.5, z) - np.sqrt(z))
    return float((f * ex_given_z).sum() * dz), float((f * z).sum() * dz)


def renewal_mean(eta, beta):
    return float(eta * Gamma(1.0 + 1.0 / beta))


def r4():
    beta, eta, n = 2.0, 1.0, 40000; half = n // 2; dec = n // 10
    res = {}
    for q in (0.0, 0.5, 0.8):
        X2, v2 = _kijima("II", q, n, beta, eta, seed=6); X1, v1 = _kijima("I", q, n, beta, eta, seed=6)
        ex_chain, ez_chain = _kijima2_chain(q, beta, eta)
        v_law = math.sqrt(q * n)                                          # type I, beta = 2: dV/dn = q E[X | V] ~ q / (2 V), so V_n ~ sqrt(q n)
        x_law = 1.0 / (2.0 * math.sqrt(q * (n - dec / 2))) if q > 0 else renewal_mean(eta, beta)   # ... and E[X_n] ~ 1 / (2 V_n) at the last decile's midpoint
        res[q] = dict(m2=float(X2[half:].mean()), cv2=cv(X2[half:]), v2=v2, m1_first=float(X1[:dec].mean()), m1=float(X1[-dec:].mean()), v1=v1,
                      v_law=v_law, x_law=x_law, chain=ex_chain, z_chain=ez_chain, z_theory=q * q / (1.0 - q * q))
    renewal = renewal_mean(eta, beta)                                     # q = 0: perfect repair, a Weibull renewal process
    r5, r8 = res[0.5], res[0.8]
    crr, null, dom = r5["m2"], r5["m1"], r5["chain"]
    chain_ok = all(rel(res[q]["m2"], res[q]["chain"]) <= TOL_N for q in (0.5, 0.8)) and rel(res[0.0]["m2"], renewal) <= TOL_N
    type1_law = all(rel(res[q]["v1"], res[q]["v_law"]) <= 0.02 and rel(res[q]["m1"], res[q]["x_law"]) <= 0.05 for q in (0.5, 0.8))
    check = chain_ok and type1_law
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("eng", "A repairable component with a Weibull(2, 1) baseline hazard (increasing failure rate), failure = own event, repair = the cut, with A6 regeneration: the age the next occasion starts from is the geometric (P3) re-weighting of the settled inter-failure intervals, V_n = q (V_n-1 + X_n), against the accumulated alternative V_n = V_n-1 + q X_n; 40000 failures, seed 6",
        source=f"{SRC_WILD} [6] (DESCR)",
        Q="a component whose repair seeds the next occasion from the settled intervals at bounded strength (A6 with P3 weights q^k) has a stationary inter-failure time (a bounded virtual age), while one whose repair accumulates them (a count) has intervals that shrink without limit; in the domain's terms the first is Kijima's type-II imperfect repair with degree q and the second his type I",
        ingredient="A6 (the next occasion seeded from the settled past at bounded strength, never an accumulated count) with P3 (geometric age weights), D5 (occasion = one inter-failure interval), A3 read as the source row did (the replacement is the cut)",
        null="the accumulated reading: V_n = V_n-1 + q X_n (Kijima type I), the same q",
        domain="Kijima 1989 (general repair): type II virtual age V_n = q (V_n-1 + X_n) has a stationary regime under an increasing failure rate, type I V_n = V_n-1 + q X_n has V_n -> infinity; for beta = 2 the type-II chain Z = (V/eta)^2 is Z' = q^2 (Z + E) with E ~ Exp(1) (stationary mean q^2/(1 - q^2)) and E[X | z] = eta (e^z Gamma(3/2, z) - sqrt z) in closed form, and the type-I model's own asymptotics are V_n ~ sqrt(q n), E[X_n] ~ 1/(2 V_n)",
        numbers=f"q = 0 (perfect repair): simulated mean interval {res[0.0]['m2']:.4f}, Weibull renewal mean eta Gamma(3/2) = {renewal:.4f}, chain {res[0.0]['chain']:.4f}; " + "; ".join(
            f"q = {q:g}: type II (A6) mean interval over the last {half} failures {res[q]['m2']:.4f} (CV {res[q]['cv2']:.4f}), chain stationary value {res[q]['chain']:.4f} (mean Z {res[q]['z_chain']:.4f}, theory {res[q]['z_theory']:.4f}), virtual age at the end {res[q]['v2']:.4f}; type I (count) mean interval first decile {res[q]['m1_first']:.5f}, last decile {res[q]['m1']:.5f} (1/(2 V) law {res[q]['x_law']:.5f}), virtual age at the end {res[q]['v1']:.2f} (sqrt(q n) = {res[q]['v_law']:.2f})"
            for q in (0.5, 0.8)),
        tg=f"type II mean interval {crr:.4f} vs null type I {null:.5f} (q = 0.5, last decile): {_agree(crr, null)}",
        tn=f"the type-II chain gives {dom:.4f}: {_agree(crr, dom, TOL_N)} (the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q; at q = 0.8, {r8['m2']:.4f} against {r8['chain']:.4f}: {_agree(r8['m2'], r8['chain'], TOL_N)})",
        tc=f"type II within 1 % of its chain at both q and of the renewal mean at q = 0: {_word(chain_ok, 'yes', 'no')}; type I's virtual age within 2 % of sqrt(q n) and its last-decile mean interval within 5 % of 1/(2 V) at both q: {_word(type1_law, 'yes', 'no')}: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=f"the ingredient does real work (T-G: {crr:.4f} against {null:.5f}) and what it produces is the reliability literature's own dichotomy: A6's 'reweighted content, never an accumulated count' is Kijima's type-II against type-I virtual age, with P3's q as his degree of repair, and the domain has both models and the theorem that separates them (the type-II value {dom:.4f} is the stationary chain's; the type-I intervals fall from {r5['m1_first']:.5f} to {r5['m1']:.5f} as the virtual age climbs to {r5['v1']:.2f}, on the model's sqrt(q n) law); CRR renames it. The source row's class map (odometer against calendar) is untouched; this row reads the reset, not the clock. The synthesis reading is {out}",
        weakness="the A6 seed here is a weighted sum with strength q/(1 - q), not the normalised Frechet mean the axiom names (the 1-D duration carrier makes the Frechet mean a weighted mean, and the virtual age is that mean times the strength); A6's clause 'a system that re-counts its past stops cutting' reads the other way on this domain: the accumulating type-I component cuts ever faster, not never; the chain is exact only at beta = 2 (the Rayleigh baseline); Kijima 1989 by name and year only, not fetched (R10)",
        elegance="Three ways to fix a machine: as good as new (forget everything), as bad as old (keep everything), or in between (keep a fixed fraction of the past). Only the first two are famous; the third is the one where the memory stays bounded and the machine keeps a steady pace.",
        child="Imagine a bike that gets repaired every time it breaks. If each repair makes it brand new, its past does not matter. If each repair only patches it, all the old wear stays, and it breaks faster and faster. In between, a repair undoes part of the wear, so the bike remembers only a bit of its past and keeps breaking at a steady pace.")


# ---------------------------------------------------------------- 85 [wild 7] dripping tap: the drop mass as arc, amplitude and natural-time spacing
def _tap(flow_cv, mass_cv, dt=0.005, n_ev=100, seed=7):
    """The source's model: flow Q(t) Ornstein-Uhlenbeck about 1 (rate 0.1), hanging mass m grows at Q, pinch-off when m reaches
    a per-drop mass m* (CV mass_cv), reset to 0. Same draw order as the source (thresholds first, then one normal per step)."""
    rng = np.random.default_rng(seed); ou = 0.0; m = 0.0; trace = []; flow = []; events = []
    mstar = 1.0 * (1 + mass_cv * rng.standard_normal(n_ev)); i = 0; t = 0
    while i < n_ev:
        ou += dt * (-0.1 * ou) + flow_cv * math.sqrt(2 * 0.1 * dt) * rng.standard_normal(); Q = max(1.0 + ou, 0.05)
        m += Q * dt; trace.append(m); flow.append(Q); t += 1
        if m >= mstar[i]:
            events.append(t); m = 0.0; i += 1
    return np.array(trace), np.array(flow), np.array(events), mstar


def r5():
    dt = 0.005
    tr, flow, ev, mstar = _tap(0.2, 0.03, dt=dt)
    ev_used = ev[3:]
    r = regularity(tr, ev_used, sigma=1.0, dt=dt, n_boot=500, seed=0, segment_end="exclusive")
    arcs = np.array([tr[b - 1] - tr[a] for a, b in zip(ev_used[:-1], ev_used[1:])])
    T = np.diff(ev_used) * dt
    Qbar = np.array([flow[a + 1:b].mean() for a, b in zip(ev_used[:-1], ev_used[1:])])   # occasion-averaged flow: arc = (n - 1) Qbar dt exactly
    m_drop = mstar[4:]                                                   # the thresholds the used occasions crossed
    vol = np.cumsum(flow) * dt                                            # natural time: cumulative volume delivered
    nat_spacing = np.diff(vol[ev_used - 1])                               # spacing of the drops in delivered volume
    v_T, v_m, v_Q = (float(np.var(np.log(v), ddof=1)) for v in (T, arcs, Qbar))        # T = m / Qbar: ln T = ln m - ln Qbar
    cov_mQ = float(np.cov(np.log(arcs), np.log(Qbar))[0, 1])
    crr, null, dom = r["cv_arc"], r["cv_amp"], cv(m_drop)
    lv_ok = abs(v_T - v_m - v_Q) / v_T <= 0.05                            # the two sources add in log-variance (independent m and Qbar)
    check = lv_ok
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    amp_ci = r["ci95_amp"]; clock_ci = r["ci95"]
    return make_row("fluid", "Dripping tap in the Tate regime (the source's model and draw: flow Ornstein-Uhlenbeck with CV 0.2, drop mass CV 0.03, 100 drops, seed 7; own event = pinch-off, the reset is the cut, exclusive segmentation), the hanging mass as the carrier",
        source=f"{SRC_WILD} [7] (DESCR)",
        Q="in the Tate regime the tap is a flow meter: the drops are equally spaced in delivered volume (natural time) with CV equal to that of the drop mass, and H-L5's regular quantity, the arc of the hanging mass between pinch-offs, is the drop mass itself, so control (i) of H-L5 (the excursion's amplitude) ties it identically: the tap is arc-regular by the bare inequality and Tate's law, not by any quantity beyond the drop mass",
        ingredient="H-L5 (the class claim: arc against clock between own events), D5 (occasion = one drop), A1' (one drop = one step; natural time = delivered volume / drop mass), D2 on the monotone mass carrier (arc = the mass gained)",
        null="H-L5's control (i): the peak-to-peak amplitude of the occasion, which on a monotone fill is the arc",
        domain="Tate's law (1864): the drop detaches when its weight reaches the surface-tension force, so the drop mass is fixed by the nozzle and the liquid, and the drip interval is the drop mass over the occasion-averaged flow, T = m*/Qbar, a ratio of independent quantities: CV(arc) = CV(m*), and var(ln T) = var(ln m*) + var(ln Qbar)",
        numbers=f"{r['n']} occasions: CV(arc) = {r['cv_arc']:.4f}, CV(amplitude) = {r['cv_amp']:.4f} (CI95 of the difference [{amp_ci[0]:.1e}, {amp_ci[1]:.1e}]), CV(clock) = {r['cv_clock']:.4f} (CI95 of CV(arc) - CV(clock) [{clock_ci[0]:.4f}, {clock_ci[1]:.4f}]); CV of the drop masses crossed = {cv(m_drop):.4f}; spacing of the drops in delivered volume: mean {nat_spacing.mean():.4f}, CV {cv(nat_spacing):.4f}; CV of the occasion-averaged flow = {cv(Qbar):.4f}; log-variances: clock {v_T:.5f}, arc {v_m:.5f}, flow {v_Q:.5f}, sampled covariance of ln arc and ln flow {cov_mQ:.5f}; class index CV(clock)/CV(arc) = {r['cv_clock'] / r['cv_arc']:.3f}",
        tg=f"CV(arc) {crr:.4f} vs null CV(amplitude) {null:.4f}: {_agree(crr, null)}",
        tn=f"Tate's law gives CV(arc) = CV(m*) = {dom:.4f}: {_agree(crr, dom, TOL_N)} (the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q)",
        tc=f"var(ln clock) within 5 % of var(ln arc) + var(ln flow) (relative gap {abs(v_T - v_m - v_Q) / v_T:.4f}): {_word(check, 'holds', 'fails')}",
        out=out,
        reading=f"on a monotone fill the arc is the amplitude (T-G: {crr:.4f} against {null:.4f}, CI of the difference at round-off), so H-L5 as stated fails on the tap even though the bare inequality holds by {r['cv_clock'] - r['cv_arc']:.4f} (CI [{clock_ci[0]:.4f}, {clock_ci[1]:.4f}]): the regular quantity is the drop mass, the domain's Tate constant, and the drops' spacing in delivered volume (CV {cv(nat_spacing):.4f}) is that constant seen in natural time; the source row's 'the law, not the framework, says where the class holds' survives, and the same reading applies to the odometer and every integrate-and-fire carrier (batch 03 row 4 and batch 12 row 1 said it for a swing and a pulse). The synthesis reading is {out}",
        weakness="a physical mass, not a statistical carrier: A1 supplies no metric and control (ii) of H-L5 is void; the chaotic dripping regime (Shaw 1984), where the drop mass depends on the residual oscillation left by the last pinch-off, is the case where the arc on a fuller carrier would not be the drop mass, and it is not modelled here",
        elegance="A drop lets go when it gets too heavy to hang on, so every drop is the same size: a drop is a unit of water, not of time. Nurses set an intravenous drip by counting drops per minute for exactly this reason. To know how much water came out, count the drops and put the stopwatch away.",
        child="A dripping tap makes drops that are all the same size, because a drop falls when it gets too heavy to hold on. So if you want to know how much water came out, count the drops. Do not watch the clock: the tap can drip fast or slow, but each drop is the same.")


def main():
    return run_batch("Synthesis batch 17: rows 81-85 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
