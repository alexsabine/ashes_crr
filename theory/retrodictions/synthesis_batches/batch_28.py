"""Synthesis batch 28: the free-energy principle and CRR's ontological commitments (owner request 2026-09-22, prompt-log
entry 78). Five rows on synthetic FEP systems (no data, R2): [1] the Dirac delta as a boundary in time distributing unit
mass (A3/D5 against the infinite-precision observation of a Bayesian filter); [2] Omega = 1 as equanimity and the offset
as grasping or thrashing (H-EQ on a one-dimensional prior-datum node against the Bayes gain: FEP's aberrant-precision
reading); [3] precision as a measurable variable (A1''s unit on the innovation record against the innovation variance);
[4] A6 regeneration by a bounded mean against Dirichlet count accumulation on a switching contingency (against the exact
HMM filter); [5] the epistemic term of expected free energy against the Fisher chord (information geometry's, not CRR's).
Literature named by name and year only, not fetched (R10): Friston 2010; Feldman and Friston 2010 (attention as
precision); Parr, Pezzulo and Friston 2022; Mehra 1970 (innovation-based noise estimation); Costa, Santos and Strapasson
2015 (Gaussian Fisher-Rao distance). Deterministic; under 60 s."""
import math
import sys

import numpy as np

from scipy.signal import savgol_coeffs

from crr.instrument.core import unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SMOOTH, WCAP, DEN_FLOOR = 0.9, 1e4, 1e-12                                     # the registered estimator of H-EQ (EQ2..EQ4)


def _word(cond, yes, no):
    return yes if cond else no


def fr_gauss(m1, s1, m2, s2):
    d = (m1 - m2) / math.sqrt(2.0)
    a = math.sqrt(d * d + (s1 + s2) ** 2); b = math.sqrt(d * d + (s1 - s2) ** 2)
    return math.sqrt(2.0) * math.log((a + b) / max(a - b, 1e-300))


# ---------------------------------------------------------------- [1] the Dirac delta as a boundary in time
def _delta_path(pi_delta, seed=281, n=20000, q=0.05, r=1.0, rate=0.02, after=20):
    rng = np.random.default_rng(seed); x = 0.0; m = 0.0; P = 1.0
    arc_rel = 0.0; arc_jump = 0.0; arc_after = 0.0; n_delta = 0; frac_absorbed = []; jump_pred = []; since = after + 1
    for t in range(n):
        x += math.sqrt(q) * rng.normal(); Pp = P + q
        if rng.random() < rate:                                                # a delta-precision observation: the boundary in time
            y = x + rng.normal() / math.sqrt(pi_delta); S = Pp + 1.0 / pi_delta; K = Pp / S
            m_new = m + K * (y - m); P_new = (1 - K) * Pp
            arc_jump += fr_gauss(m, math.sqrt(P), m_new, math.sqrt(P_new)); n_delta += 1; since = 0
            frac_absorbed.append(K)                                           # the share of the innovation absorbed at the instant = the gain
            jump_pred.append(fr_gauss(0.0, math.sqrt(Pp), 0.0, math.sqrt(P_new)))   # the domain's closed form for the variance collapse alone (innovation dropped)
        else:
            y = x + math.sqrt(r) * rng.normal(); S = Pp + r; K = Pp / S
            m_new = m + K * (y - m); P_new = (1 - K) * Pp
            d = fr_gauss(m, math.sqrt(P), m_new, math.sqrt(P_new)); arc_rel += d; since += 1
            if since <= after: arc_after += d                                  # the re-expansion of the collapsed variance in the steps after a delta
        m, P = m_new, P_new
    tot = arc_jump + arc_rel
    return arc_jump / tot, float(np.mean(frac_absorbed)), arc_jump / max(n_delta, 1), float(np.mean(jump_pred)), n_delta, arc_after / tot


def r1():
    grid = (1.0, 10.0, 100.0, 1e4); rows = [_delta_path(p) for p in grid]
    shares = [r[0] for r in rows]; gains = [r[1] for r in rows]; jumps = [r[2] for r in rows]; preds = [r[3] for r in rows]
    afters = [r[5] for r in rows]
    crr = shares[-1]                                                           # A3 exclusive reading at the highest precision: the share of the record's Fisher arc that lives AT the cuts
    null = 1.0                                                                 # the inclusive reading: the jump is content like any step; the content share is everything
    dom = None                                                                 # no domain theorem for the share; the jump length's closed form is printed beside the measured one
    monotone = all(a < b for a, b in zip(shares, shares[1:]))
    check = monotone and shares[-1] > 0.5
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    where = "at the cuts" if shares[-1] > afters[-1] else "in the twenty steps after each cut (the collapsed variance re-expanding)"
    return make_row("fep", "Kalman filter receiving delta-precision observations at random times (the boundary in time) among ordinary ones",
        source="A3/D5 (the jump is the cut, not content; the occasion is the interval between cuts) against the infinite-precision observation of a Bayesian filter (the Dirac likelihood, gain -> 1); Costa et al. 2015 for the Gaussian Fisher-Rao length, names only",
        Q="a Dirac-precision datum is a cut: as its precision grows the belief's Fisher arc concentrates at the instants of the deltas (the boundary carries the change and distributes the datum's unit mass into the belief at once), and the occasions between them empty",
        ingredient="A3 exclusive segmentation: the arc at a delta is the cut's, not the occasion's; D5 occasions between deltas",
        null="the inclusive reading (a delta step is content like any other): the content share is 1 by definition",
        domain=None,
        numbers=(f"precision pi_delta {grid}: share of the total Fisher arc at the deltas {[round(v, 4) for v in shares]}; mean gain at the deltas {[round(v, 4) for v in gains]}; "
                 f"share of the arc in the 20 steps after each delta {[round(v, 4) for v in afters]}; mean jump length {[round(v, 4) for v in jumps]} vs the variance-collapse closed form of Costa et al. 2015 {[round(v, 4) for v in preds]} (the Kalman gain -> 1 is the domain's unit-mass statement); deltas in 20000 steps {rows[-1][4]}"),
        tg=f"cut share at pi = 1e4 ({crr:.4f}) vs the inclusive content share (1): rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"no domain theorem for the share; the jump length at pi = 1e4 measured {jumps[-1]:.4f} vs the variance-collapse closed form {preds[-1]:.4f} (rel {rel(jumps[-1], preds[-1]):.2e})",
        tc=f"share monotone in the precision {monotone} and above 1/2 at pi = 1e4 ({shares[-1]:.4f}): {check}",
        out=out,
        reading=(f"{_word(check, 'the boundary carries the arc as the precision grows', 'the arc does NOT concentrate at the deltas')}: the gain at the deltas reaches {gains[-1]:.4f} (the datum's unit mass lands at the instant, the domain's own statement), "
                 f"but the Fisher arc lives {where} ({afters[-1]:.4f} of the arc there against {shares[-1]:.4f} at the cuts); the delta collapses the belief's variance and the ordinary observations re-inflate it, and in the Fisher geometry that re-inflation is travel; "
                 f"the boundary in time distributes the datum's mass at once and spreads the belief's change over the occasion that follows"),
        weakness="the delta is approximated by a finite precision 1e4; the ordinary observations keep a relaxation arc alive between deltas, so the share never reaches 1; a filter with no ordinary observations would put every unit of arc at the cuts by construction",
        elegance="A perfectly sharp fact does not add to a belief, it replaces it: the whole distance travelled is at the instant, and the instant has no width.",
        child="If someone tells you the exact answer, you do not slowly change your mind, you change it all at once. On a graph of your beliefs, all the movement happens at that one moment, and the moments in between are flat.")


# ---------------------------------------------------------------- [2] Omega = 1 as equanimity; the offset as grasping or thrashing
def _node(omega, pi_o, pi_p, y=1.0, m=0.0, lr=0.02, steps=4000, ema=True, start=0.0):
    """One-dimensional prior-datum node: present pull g_p = pi_o (mu - y), past pull g_q = pi_p (mu - m); the rule
    w = Omega |g_p| / |g_q| on the registered EMA estimator (or exact norms). Starts at the prior. Returns the time-averaged
    position over the last half as an effective gain K_eff = (mu - m)/(y - m)."""
    mu = m + start * (y - m); ema_p = ema_q = None; pos = []
    for t in range(steps):
        g_p = pi_o * (mu - y); g_q = pi_p * (mu - m)
        if ema:
            ema_p = g_p if ema_p is None else SMOOTH * ema_p + (1 - SMOOTH) * g_p
            ema_q = g_q if ema_q is None else SMOOTH * ema_q + (1 - SMOOTH) * g_q
            w = min(omega * abs(ema_p) / max(abs(ema_q), DEN_FLOOR), WCAP)
        else:
            w = min(omega * abs(g_p) / max(abs(g_q), DEN_FLOOR), WCAP)
        mu = mu - lr * (g_p + w * g_q)
        if t >= steps // 2: pos.append((mu - m) / (y - m))
    return float(np.mean(pos)), float(np.std(pos))


def _regime(mean, sd):
    if sd >= 0.1: return "oscillating"
    if mean > 0.9: return "datum"
    if abs(mean) < 0.1: return "prior"
    return "between"


def r2():
    grid = (0.5, 0.71, 1.0, 1.41, 2.0); pi_o, pi_p = 1.0, 1.0; K_bayes = pi_o / (pi_o + pi_p)
    E = [_node(o, pi_o, pi_p) for o in grid]; K_ema = [e[0] for e in E]; sd_ema = [e[1] for e in E]
    X = [_node(o, pi_o, pi_p, ema=False) for o in grid]; K_exact = [e[0] for e in X]; sd_exact = [e[1] for e in X]
    K_mid = [_node(o, pi_o, pi_p, start=0.5)[0] for o in grid]                # a second start, at the midpoint
    K_ema4 = [_node(o, 4.0, 1.0)[0] for o in grid]; K_bayes4 = 4.0 / 5.0
    reg_ema = [_regime(a, b) for a, b in zip(K_ema, sd_ema)]; reg_exact = [_regime(a, b) for a, b in zip(K_exact, sd_exact)]
    crr = K_ema[2]; null = 0.5                                                # null: fixed w = 1 (sum the two pulls) rests at the precision-weighted mean = Bayes at equal precision
    dom = K_bayes
    dial_exact = reg_exact[0] == "datum" and reg_exact[1] == "datum" and reg_exact[3] == "prior" and reg_exact[4] == "prior"
    dial_ema = reg_ema[0] == "datum" and reg_ema[1] == "datum" and reg_ema[3] == "prior" and reg_ema[4] == "prior"
    still = abs(K_mid[2] - 0.5) < 0.05 and abs(K_exact[2]) < 0.05           # Omega = 1 rests where it starts (midpoint start stays at the midpoint; prior start stays at the prior)
    check = dial_ema and still
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "one-dimensional prior-datum node under the equanimity rule: the resting point as an effective gain, against the Bayes gain",
        source="H-EQ (Omega = 1) read as equanimity, the offset as grasping (the prior wins) or thrashing (the datum wins); FEP's aberrant precision (over-precise priors, under-precise priors), Friston 2010, names only; omega_sweeps.txt [2] the one-dimensional knife edge",
        Q="Omega is a precision dial: Omega < 1 rests at the datum (thrashing, an under-precise prior), Omega > 1 rests at the prior (grasping, an over-precise prior), and Omega = 1 rests wherever the estimator's lag leaves it: equanimity is not the Bayes compromise but the absence of any preferred resting point",
        ingredient="H-EQ with the registered EMA estimator (smooth 0.9, cap 1e4), Omega over the study grid; the exact-norm rule printed beside it",
        null="the fixed weight w = 1 (sum the two pulls): rests at the precision-weighted mean, the Bayes point at equal precision (0.5)",
        domain="the Bayes (Kalman) gain K = pi_o / (pi_o + pi_p)",
        numbers=(f"equal precision (K_Bayes {K_bayes:.4f}), Omega grid {grid}, start at the prior: K_eff on the EMA rule {[round(v, 4) for v in K_ema]} (sd over the last half {[round(v, 4) for v in sd_ema]}; regimes {reg_ema}), "
                 f"exact-norm rule {[round(v, 4) for v in K_exact]} (regimes {reg_exact}); start at the midpoint, EMA rule: {[round(v, 4) for v in K_mid]}; "
                 f"precision ratio 4 (K_Bayes {K_bayes4:.4f}): K_eff on the EMA rule {[round(v, 4) for v in K_ema4]}"),
        tg=f"K_eff at Omega = 1 ({crr:.4f}) vs the fixed-weight resting point ({null:.4f}): rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"K_eff at Omega = 1 vs the Bayes gain ({dom:.4f}): rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'agree', 'differ')}",
        tc=f"the dial (Omega < 1 datum, Omega > 1 prior, still) on the exact rule {dial_exact}, on the registered EMA rule {dial_ema}; Omega = 1 rests where it starts {still}: {check}",
        out=out,
        reading=(f"exact norms: {_word(dial_exact, 'below 1 the belief goes to the datum (thrashing after the evidence) and above 1 it goes to the prior (grasping)', 'the exact rule does not read as a dial')}; "
                 f"the registered EMA estimator: {_word(dial_ema, 'the same dial', 'NOT a dial: with the lag, Omega above 1 ' + ('oscillates' if 'oscillating' in reg_ema[3:] else 'does not settle at the prior') + ' (regimes ' + str(reg_ema) + '), so the offset above 1 is thrashing around the prior, not grasping it')}; "
                 f"Omega = 1 {_word(still, 'rests wherever it starts (the knife edge)', 'does not rest where it starts')}; at Omega = 1 the EMA rule rests at K_eff {crr:.4f}, "
                 f"{_word(rel(crr, dom) <= TOL_N, 'the Bayes point', 'not the Bayes point (' + f'{dom:.4f}' + ') and not the fixed-weight point (' + f'{null:.4f}' + '): where it rests is set by the estimator lag, which is what the one-dimensional knife edge predicts')}; "
                 f"with the precision ratio 4 the Bayes gain is {K_bayes4:.4f} and the rule at Omega = 1 rests at {K_ema4[2]:.4f}: the rule does not see the precision"),
        weakness="a static datum; on a stream of data the datum moves and the resting point becomes a trajectory (omega_sweeps.txt [2] (iv)); 'grasping' and 'thrashing' are the owner's words for the two sides of the knife edge, not FEP terms; the sd column shows whether Omega > 1 oscillates around the prior",
        elegance="Equal pull is not a compromise but a stalemate: the belief stops wherever it happens to be when the two pulls first match, and only Bayes knows where it should have stopped.",
        child="Two children pull a rope with exactly equal strength: the knot does not move, wherever it is. That is equanimity here. It is not the fair middle; the fair middle is where the stronger evidence says, and that needs a different rule.")


# ---------------------------------------------------------------- [3] precision as a measurable variable
def r3():
    grid = (0.0625, 0.25, 1.0, 4.0, 16.0); q = 0.05; n = 6000; out_frac, out_mult = 0.05, 10.0
    def innovations(r, contaminated):
        rng = np.random.default_rng(283); x = 0.0; m = 0.0; P = 1.0; nus = []
        for t in range(n):
            x += math.sqrt(q) * rng.normal(); u = rng.random(); e = rng.normal()
            y = x + math.sqrt(r) * e * (out_mult if (contaminated and u < out_frac) else 1.0)   # 5 % outliers at 10 x the noise: the record is not the model
            Pp = P + q; S = Pp + r; nu = y - m; nus.append(nu)
            K = Pp / S; m = m + K * nu; P = (1 - K) * Pp
        return np.array(nus[1000:])
    ratios_unit = []; ratios_std = []; ratios_clean = []; S_list = []
    for r in grid:
        P_ss = 0.5 * (q + math.sqrt(q * q + 4 * q * r))                       # steady-state prior variance of the scalar random-walk filter (Riccati)
        S_ricc = P_ss + r                                                      # the model's innovation variance (Mehra 1970): precision of the innovation = 1/S
        clean = innovations(r, False); S_dom = float(np.var(clean, ddof=1))    # the domain's own measured precision on the uncontaminated record (same seed)
        nus = innovations(r, True)
        sig = unit_sigma(nus, detrend_window=9, detrend_order=2, scale="mad")
        ratios_unit.append(sig * sig / S_dom); ratios_std.append(float(np.var(nus, ddof=1)) / S_dom); S_list.append((round(S_ricc, 4), round(S_dom, 4)))
        ratios_clean.append(unit_sigma(clean, detrend_window=9, detrend_order=2, scale="mad") ** 2 / S_dom)
    crr = float(np.mean(ratios_unit)); null = float(np.mean(ratios_std)); dom = 1.0
    check = all(abs(v - 1.0) < 0.1 for v in ratios_unit)
    leverage = 1.0 - float(savgol_coeffs(9, 2)[4])                            # residual-variance factor of the registered detrender on white noise: 1 - the centre weight
    clean_ratio = float(np.mean(ratios_clean))
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "the innovation record of a Kalman filter with 5 % outliers: precision measured as CRR's unit against the domain's innovation variance",
        source="A1'/D1 (the resolvable step: robust scale of the detrended residual across occasions) read as a precision estimator; Mehra 1970 (innovation-based noise identification), Feldman and Friston 2010 (precision as attention), names only",
        Q="precision is measurable from the record: 1/sigma^2 with sigma the A1' unit of the innovation sequence recovers the model's innovation precision under outliers, where the sample variance (the FEP's expected squared prediction error) does not",
        ingredient="A1' unit_sigma (Savitzky-Golay detrend, window 9, MAD scale) on the innovations",
        null="the sample variance of the innovations (the expected squared prediction error, which is how a predictive-coding node estimates precision)",
        domain="the innovation variance of the same filter on the uncontaminated record (the model's own precision 1/S; the Riccati steady state printed beside it)",
        numbers=(f"observation variance r in {grid}, 5 % outliers at 10x: unit^2 / S {[round(v, 4) for v in ratios_unit]}, variance / S {[round(v, 4) for v in ratios_std]}; "
                 f"unit^2 / S on the clean record {[round(v, 4) for v in ratios_clean]}; S (Riccati, measured clean) {S_list}; means {crr:.4f} (unit) and {null:.4f} (variance)"),
        tg=f"unit^2/S vs variance/S: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"unit^2/S vs 1: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'the unit IS the model precision', 'the unit differs from the model precision by more than 1 %')}",
        tc=f"unit^2 within 10 % of S at every r: {check}",
        out=out,
        reading=(f"{_word(check, 'the A1 unit measures the precision the model assumes, through outliers the model did not assume', 'the unit over-reads the clean precision by ' + f'{100 * (crr - 1):.0f}' + ' % on average: the outliers kick the non-robust filter and the innovations after a kick are genuinely larger, which the robust unit correctly reports as the record it was given')}; "
                 f"the sample variance reads {null:.3f} x the clean innovation variance (the outliers are in it); on the clean record the unit reads {clean_ratio:.4f} x, which is the registered detrender's leverage on white noise (1 - the centre Savitzky-Golay weight = {leverage:.4f}; rel {rel(clean_ratio, leverage):.2e}, {_word(rel(clean_ratio, leverage) <= 0.05, 'accounted for', 'not accounted for')}): A1's unit on a white record is the residual scale, not the noise scale; "
                 f"precision as a measurable is the robust residual scale of the record, which is what CRR names as the unit of change, and it measures the filter's actual precision, not the model's nominal one"),
        weakness="the MAD-based unit is a standard robust scale (Hampel 1974, name only); CRR names it, robust statistics owns it; the 10 % tolerance is this row's, not a registered threshold; the two departures (over-reading under contamination, under-reading on white noise by the detrender's leverage) are both instrument facts to state in any prereg that reads the unit as a precision",
        elegance="The size of the smallest believable change and the precision of the senses are one number seen from two sides.",
        child="How wobbly your measurements usually are tells you how much to trust the next one. If a few measurements are wildly off, use the typical wobble, not the average, or the wild ones will fool you.")


# ---------------------------------------------------------------- [4] A6 regeneration by a bounded mean vs Dirichlet accumulation, against the HMM filter
def r4():
    rng = np.random.default_rng(284); n = 20000; p_sw = 0.005; levels = (0.8, 0.2)
    lam_reg, lam_grid = 0.05, (0.01, 0.05, 0.2)
    th = 0; a = b = 1.0; est_acc = []; est_bnd = {l: [] for l in lam_grid}; est_hmm = []; truth = []
    p_bnd = {l: 0.5 for l in lam_grid}; post = np.array([0.5, 0.5])
    for t in range(n):
        if rng.random() < p_sw: th = 1 - th
        o = int(rng.random() < levels[th]); truth.append(levels[th])
        a += o; b += 1 - o; est_acc.append(a / (a + b))                        # accumulated Dirichlet counts (no forgetting)
        for l in lam_grid:
            p_bnd[l] = (1 - l) * p_bnd[l] + l * o; est_bnd[l].append(p_bnd[l])  # A6: a bounded mean, never an accumulated count
        like = np.array([levels[0] if o else 1 - levels[0], levels[1] if o else 1 - levels[1]])
        post = post * like; post /= post.sum(); post = np.array([(1 - p_sw) * post[0] + p_sw * post[1], (1 - p_sw) * post[1] + p_sw * post[0]])
        est_hmm.append(post[0] * levels[0] + post[1] * levels[1])              # the exact filter (known levels and switch rate): the Bayes-optimal tracker
    truth = np.array(truth); mae = lambda e: float(np.mean(np.abs(np.array(e) - truth)))
    crr = mae(est_bnd[lam_reg]); null = mae(est_acc); dom = mae(est_hmm); sweep = {l: mae(est_bnd[l]) for l in lam_grid}
    check = crr < null
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "a switching Bernoulli contingency tracked by accumulated Dirichlet counts, by a bounded mean (A6), and by the exact HMM filter",
        source="A6 regeneration ('never an accumulated count'; a bounded Frechet mean) against the Dirichlet-count learning of active inference (Parr, Pezzulo and Friston 2022, name only) and against the Bayes-optimal filter for the switching process",
        Q="on a non-stationary contingency the bounded mean tracks the truth better than accumulated counts, and the exact filter (which knows the switching rate) is the ceiling it approaches",
        ingredient="A6: a bounded exponential mean with a named rate (0.05 registered; 0.01 and 0.2 printed)",
        null="Dirichlet counts accumulated without forgetting (the concentration parameters grow without bound)",
        domain="the exact two-state HMM filter with known levels and switch rate (mean absolute error of its posterior-mean contingency)",
        numbers=(f"{n} trials, switch rate {p_sw}, levels {levels}: MAE accumulated counts {null:.4f}, bounded mean (rate {lam_reg}) {crr:.4f}, sweep {dict((k, round(v, 4)) for k, v in sweep.items())}, exact filter {dom:.4f}"),
        tg=f"bounded mean vs accumulated counts: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"bounded mean vs the exact filter: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'the filter is matched', 'the filter is not matched')}",
        tc=f"MAE(bounded) < MAE(accumulated): {check}",
        out=out,
        reading=(f"{_word(check, 'the bounded mean beats accumulation', 'accumulation beats the bounded mean')} by {null - crr:+.4f} in MAE and sits {crr - dom:+.4f} above the exact filter; the rate is a knob A6 does not fix (best in the sweep: {min(sweep, key=sweep.get)}); "
                 f"active inference already forgets counts by a decay in practice, and the Bayes-optimal forgetting is the filter's, so A6 names the practice and the domain owns the optimum"),
        weakness="the exact filter knows the levels and the switch rate; a filter that must learn them is the fair comparison and is not run here; the bounded mean's rate is chosen from a three-point sweep on this same stream (in-sample)",
        elegance="A memory that only ever adds cannot notice that the world has changed; a memory that fades can, and how fast it should fade is exactly how fast the world changes.",
        child="If you keep a running total of every time a coin came up heads since you were born, you will never notice when someone swaps the coin. If you mostly remember the last few flips, you will.")


# ---------------------------------------------------------------- [5] the epistemic term of expected free energy vs the Fisher chord
def r5():
    rng = np.random.default_rng(285); p_hit = 0.8; n = 4000
    kls = []; chords = []
    for t in range(n):
        q0 = rng.uniform(0.02, 0.98); q = np.array([q0, 1 - q0])
        # expected information gain of acting (a = 0): E_o [ KL(q(c|o) || q(c)) ]
        gain = 0.0; chord2 = 0.0
        for o in (0, 1):
            like = np.array([p_hit if o else 1 - p_hit, 1 - p_hit if o else p_hit]); po = float(np.sum(q * like)); post = q * like / po
            kl = float(np.sum(post * np.log(post / q))); d = 2.0 * math.acos(min(1.0, float(np.sum(np.sqrt(post * q)))))
            gain += po * kl; chord2 += po * d * d / 2.0
        kls.append(gain); chords.append(chord2)
    kls = np.array(kls); chords = np.array(chords)
    crr = float(np.mean(chords)); null = float(np.mean(kls)); dom = null
    small = np.abs(chords - kls) / kls
    check = None
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "the epistemic value (expected information gain) of an action in the two-context agent against half the expected squared Fisher chord of the belief update",
        source="D3/D4 (chord, surplus: information geometry's, not CRR's) against the epistemic term of expected free energy (Parr, Pezzulo and Friston 2022, name only)",
        Q="the epistemic term is the expected squared Fisher chord of the belief update over two: CRR's vocabulary names it, information geometry owns it (KL = d^2/2 + O(d^4))",
        ingredient="the Fisher-Rao chord on the simplex (D3), squared and halved, expected over outcomes",
        null="the expected KL from prior to posterior (the epistemic term itself)",
        domain="the same expansion, KL = d^2/2 to leading order: the domain's own identity",
        numbers=f"{n} prior beliefs q0 ~ U(0.02, 0.98), hit rate {p_hit}: mean epistemic value {null:.6f}, mean half squared chord {crr:.6f}; relative gap median {np.median(small):.4f}, max {small.max():.4f}",
        tg=f"chord form vs KL form: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn="the identity KL = d^2/2 + O(d^4) is information geometry's",
        tc="no CRR-proper ingredient: no check (the row records the correspondence)",
        out=out,
        reading=(f"the epistemic value and the half squared chord agree to {rel(crr, null):.2e} on average and within {small.max():.3f} at worst (the update of a 0.8-hit-rate observation is a small Fisher step); "
                 f"the epistemic drive of active inference is a chord quantity, and CRR's surplus S = C - C* (travel minus chord) would be the part of the belief's path that buys no information: a proposition for a later row, not this one"),
        weakness="no CRR-proper ingredient enters (the class's own rule: REDUNDANT-IG by construction); the row is here because the owner asked which FEP aspects CRR's vocabulary reaches, and this one it reaches without adding to it",
        elegance="Curiosity, measured as the information you expect to gain, is the square of how far you expect your beliefs to move.",
        child="How much you expect to learn from looking is the same as how far you expect your opinion to jump, squared and halved. Two ways of saying one thing.")


def main():
    return run_batch("Synthesis batch 28: the free-energy principle and CRR's ontological commitments (prompt-log entry 78)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
