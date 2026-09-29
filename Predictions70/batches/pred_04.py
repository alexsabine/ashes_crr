"""PRED70 batch P04: learning and cognition (Predictions70/DECLARATION.md; prompt-log entry 234). Rows P04-1..P04-5 of
Predictions70/declared.py (pushed at 8397478 before any model existed): [1] Rescorla-Wagner on a switching reward against
an A6 bounded Frechet-mean tracker; [2] drift-diffusion decision time in evidence-arc units (A1'); [3] serial-position
recency against P3's geometric occasion weights; [4] the power law of practice against an A6 learner; [5] TD relearning
after a reward change with A6-bounded value memory against 1/n. A6's weight is q = 0.5 per occasion (decides); q in
{0.25, 0.5, 0.75} is printed as a sensitivity only. Literature named by name and year only (R10, not fetched): Rescorla and
Wagner 1972; Wald 1945; Ratcliff 1978; Murdock 1962; Newell and Rosenbloom 1981; Heathcote, Brown and Mewhort 2000; Sutton
and Barto 2018. Deterministic; under two minutes."""
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize_scalar

from crr.instrument.core import arc_length, cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from declared import P  # noqa: E402

D = {p[0]: p for p in P}
QGRID = (0.25, 0.5, 0.75)
Q0 = 0.5


def _w(cond, yes, no):
    return yes if cond else no


def _src(i):
    return f"PRED70 {i} (declared at 8397478; forecast {D[i][8]})"


def _decl(i):
    d = D[i]
    return dict(system=d[3], ingredient=d[4], Q=d[5], null=d[6], H0=d[7])


# ---------------------------------------------------------------- P04-1 Rescorla-Wagner against the A6 tracker
RW_SEEDS, RW_BLOCKS, RW_L = 200, 20, 50
ALPHAS = np.round(np.arange(0.01, 1.0 + 1e-9, 0.01), 2)


def _rw_data(bernoulli=True):
    p = np.repeat(np.tile([0.2, 0.8], RW_BLOCKS // 2), RW_L)
    rng = np.random.default_rng(20260929)
    r = (rng.random((RW_SEEDS, p.size)) < p).astype(float) if bernoulli else np.tile(p, (RW_SEEDS, 1))
    return p, r


def _rw_mse(p, r, alpha, v0=0.5):
    """Delta rule V <- V + alpha (r - V); prediction before each trial; MSE against the latent reward rate."""
    V = np.full(r.shape[0], v0); se = 0.0
    for n in range(r.shape[1]):
        se += float(((V - p[n]) ** 2).sum()); V = V + alpha * (r[:, n] - V)
    return se / r.size


def _frechet_mse(p, r, q, v0=0.5):
    """Bounded Frechet mean of the past rewards with geometric weights q^k (normalised over the available past)."""
    num = np.zeros(r.shape[0]); den = 0.0; se = 0.0
    for n in range(r.shape[1]):
        pred = np.full(r.shape[0], v0) if den == 0.0 else num / den
        se += float(((pred - p[n]) ** 2).sum()); num = r[:, n] + q * num; den = 1.0 + q * den
    return se / r.size


def r1():
    i = "P04-1"; d = _decl(i)
    p, r = _rw_data(True)
    rw = np.array([_rw_mse(p, r, a) for a in ALPHAS]); kb = int(np.argmin(rw))
    crr = _frechet_mse(p, r, Q0); null = float(rw[kb]); domain = _rw_mse(p, r, 1 - Q0)
    check = crr < null
    sens = "; ".join(f"q = {q}: A6 {_frechet_mse(p, r, q):.6f} (RW at alpha = {1 - q}: {_rw_mse(p, r, 1 - q):.6f})" for q in QGRID)
    pd_, rd = _rw_data(False)
    rwd = np.array([_rw_mse(pd_, rd, a) for a in ALPHAS]); kd = int(np.argmin(rwd)); ad = _frechet_mse(pd_, rd, Q0)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("learn", d["system"] + f"; model: Bernoulli rewards with rate 0.2 / 0.8 alternating every {RW_L} trials, {RW_BLOCKS} blocks, {RW_SEEDS} seeded learners; prediction before each trial scored by squared error against the latent rate; RW V0 = 0.5, alpha on a 0.01 grid in [0.01, 1]",
                    source=_src(i),
                    Q=d["Q"] + " (computed as: MSE of the A6 tracker against the smallest MSE of RW over the alpha grid)",
                    ingredient=d["ingredient"] + " (the weighted mean of past rewards, weights q^k normalised over the past seen, q = 0.5)",
                    null=d["null"] + f" (alpha* = {ALPHAS[kb]:.2f} on the grid)",
                    domain=d["H0"] + f" (computed: RW at alpha = 1 - q = {1 - Q0})",
                    numbers=f"MSE: A6 {crr:.6f}, RW at its best rate alpha = {ALPHAS[kb]:.2f} {null:.6f}, RW at alpha = 1 - q {domain:.6f}; q-grid sensitivity: {sens}; deterministic-reward reading (reward equal to the rate): A6 {ad:.6f}, RW best alpha = {ALPHAS[kd]:.2f} {rwd[kd]:.6f} (A6 {_w(ad < rwd[kd], 'lower', 'not lower')})",
                    tg=f"MSE {crr:.6f} vs null {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the delta rule at alpha = 1 - q gives {domain:.6f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has the A6 tracker)', 'differ')}",
                    tc=f"A6 MSE {crr:.6f} < RW best {null:.6f}: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"the A6 tracker is the delta rule with alpha = 1 - q (they differ only in the first trials, where the Frechet mean normalises over the short past), so it cannot beat the delta rule at its best rate unless that rate is 1 - q; here the best rate is {ALPHAS[kb]:.2f} and A6 is {_w(check, 'lower', 'higher')} in MSE by {abs(crr - null):.6f}",
                    weakness="the latent-rate scoring and V0 = 0.5 are my choices; the deterministic-reading line shows the verdict does not rest on them; the best RW rate is chosen in-sample (an oracle), which is what 'at its best rate' asks",
                    elegance="", child="")


# ---------------------------------------------------------------- P04-2 drift-diffusion in evidence-arc units
MU, BOUND, SD = 0.2, 1.0, 1.0


def _ddm(n_trials, dt, seed=20260929, chunk=4096):
    rng = np.random.default_rng(seed); paths = []
    for _ in range(n_trials):
        x0 = 0.0; seg = [np.zeros(1)]
        while True:
            inc = MU * dt + SD * math.sqrt(dt) * rng.standard_normal(chunk)
            xs = x0 + np.cumsum(inc)
            hit = np.flatnonzero(np.abs(xs) >= BOUND)
            if hit.size:
                seg.append(xs[:hit[0] + 1]); break
            seg.append(xs); x0 = xs[-1]
        paths.append(np.concatenate(seg))
    return paths


def _ddm_stats(dt, n_trials, with_reg=True):
    paths = _ddm(n_trials, dt)
    sig = SD * math.sqrt(dt)                                   # one step's noise sd: the resolvable step (A1')
    reg = None
    if with_reg:
        x = np.concatenate(paths); starts = np.cumsum([0] + [len(pth) for pth in paths])
        reg = regularity(x, starts, sigma=sig, dt=dt, n_boot=2000, seed=0, segment_end="exclusive")
    Tdec = np.array([(len(pth) - 1) * dt for pth in paths]); arcs = np.array([arc_length(pth, sig) for pth in paths])
    ev = np.array([abs(pth[-1]) for pth in paths])
    # the decisive statistic: per decision, arc against the decision time itself (N dt). regularity's clock is (b - a) dt,
    # which counts the reset sample as one more step ((N + 1) dt); the same paired bootstrap as regularity (n_boot 2000,
    # seed 0, resampling decisions) is run here on the exact decision times.
    rng = np.random.default_rng(0); diffs = []
    for _ in range(2000):
        idx = rng.integers(0, len(arcs), len(arcs)); diffs.append(cv(arcs[idx]) - cv(Tdec[idx]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    direct = dict(cv_arc=cv(arcs), cv_clock=cv(Tdec), diff=cv(arcs) - cv(Tdec), ci95=(float(lo), float(hi)),
                  arc_per_step=float(arcs.sum() / (Tdec.sum() / dt)))
    return reg, direct, cv(ev), float(Tdec.mean())


def r2():
    i = "P04-2"; d = _decl(i)
    reg, dr, cvE, mT = _ddm_stats(0.001, 2000)
    crr, null, domain = dr["cv_arc"], dr["cv_clock"], cvE
    lo, hi = dr["ci95"]; check = hi < 0
    sens = []
    for dts in (0.01, 0.0001):
        _, drs, cvEs, _ = _ddm_stats(dts, 2000, with_reg=False)
        labs = outcome(crr=drs["cv_arc"], null=drs["cv_clock"], domain=cvEs, check=drs["ci95"][1] < 0)
        sens.append(f"dt = {dts:g}: CV(arc) {drs['cv_arc']:.6f}, CV(clock) {drs['cv_clock']:.6f}, CI [{drs['ci95'][0]:+.6f}, {drs['ci95'][1]:+.6f}], evidence CV {cvEs:.6f}, label there {labs}")
    wald = (BOUND / MU) * math.tanh(BOUND * MU / SD ** 2)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("learn", d["system"] + f"; model: evidence dx = {MU} dt + {SD} dW from 0 to the first |x| >= {BOUND} (symmetric bounds), Euler-Maruyama dt = 0.001, 2000 seeded trials; arc by the instrument's arc_length in units of one step's noise sd; per-decision CVs with regularity's paired bootstrap (n_boot 2000, seed 0) on the exact decision times; regularity itself (trials concatenated, reset to 0 as the cut, segment_end='exclusive') printed beside it",
                    source=_src(i),
                    Q=d["Q"] + " (computed as: CV of the evidence arc per decision against CV of the decision time, the paired-bootstrap CI of CV(arc) - CV(clock) entirely below 0)",
                    ingredient=d["ingredient"] + " (decision time counted in the arc of the evidence path, in the path's own resolvable steps)",
                    null=d["null"],
                    domain=d["H0"] + " (computed: CV of the evidence |x| at decision, the chord)",
                    numbers=f"n = {reg['n']} decisions, mean decision time {mT:.4f} (Wald's mean {wald:.4f}); CV(arc) {crr:.6f}, CV(clock) {null:.6f}, CV(arc) - CV(clock) {dr['diff']:+.6f}, 95 % CI [{lo:+.6f}, {hi:+.6f}]; arc per step {dr['arc_per_step']:.4f} sigma (sqrt(2/pi) = {math.sqrt(2 / math.pi):.4f}); instrument regularity on the concatenated record (clock counts the reset sample): CV(arc) {reg['cv_arc']:.6f}, CV(clock) {reg['cv_clock']:.6f}, CI [{reg['ci95'][0]:+.6f}, {reg['ci95'][1]:+.6f}]; CV of the evidence at decision (Wald's constant chord, overshoot only) {cvE:.6f}; step sensitivity (same seed, dt = 0.001 decides): " + "; ".join(sens),
                    tg=f"CV(arc) {crr:.6f} vs null {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Wald's constant evidence at decision, CV {domain:.6f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"CI of CV(arc) - CV(clock) [{lo:+.6f}, {hi:+.6f}] entirely below 0: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"each step of a diffusing evidence path adds about sqrt(2/pi) sigma of arc whatever its sign ({dr['arc_per_step']:.4f} here), so the arc per decision is the step count times a constant up to averaging noise: the two CVs differ by {dr['diff']:+.6f} with a CI that {_w(lo <= 0 <= hi, 'contains', 'excludes')} 0; what Wald makes constant is the chord (net evidence at the bound, CV {domain:.6f}), not the arc; the natural-time unit the domain already has is the bound itself",
                    weakness="the arc of a Brownian path depends on the sampling step (it grows as dt -> 0), and so does the label (the step-sensitivity lines print it at each dt; dt = 0.001 was fixed in the code before the first run); a Fisher-Rao arc of the posterior belief (a monotone reparametrisation of x) was not computed; the decisive bootstrap is regularity's scheme re-run on exact decision times because the instrument's clock adds the reset sample to every occasion (both printed)",
                    elegance="", child="")


# ---------------------------------------------------------------- P04-3 serial position (P3), UNSTATED
def r3():
    i = "P04-3"; d = _decl(i)
    lags = np.arange(20)[::-1]                                  # item 1..20, lag to the test after item 20
    slope = lambda s: float(np.polyfit(np.arange(16, 21), np.log(s[15:]), 1)[0])  # recency slope: log strength over positions 16-20
    p3 = slope(Q0 ** lags); eq = slope(np.ones(20))
    lams = (0.1, 0.3, math.log(2.0), 1.0, 2.0)
    exps = [(lam, slope(np.exp(-lam * lags))) for lam in lams]
    sens = "; ".join(f"q = {q}: slope {slope(q ** lags):.4f}" for q in QGRID)
    out = outcome(unstated=True)
    return make_row("learn", d["system"] + "; recency component on the last five positions: P3 weight q^lag (one item per occasion), exponential decay exp(-lambda lag)",
                    source=_src(i),
                    Q=d["Q"],
                    ingredient=d["ingredient"] + " (weight q^k on the item k occasions back, q = 0.5)",
                    null=d["null"],
                    domain=d["H0"] + " (recency exp(-lambda lag); lambda is not named in declared.py)",
                    numbers=f"recency slope (log strength per position, positions 16-20): P3 {p3:.4f}, equal weights {eq:.4f}; exponential decay at lambda per item = " + ", ".join(f"{lam:.4f}: {s:.4f}" for lam, s in exps) + f"; q-grid sensitivity: {sens}",
                    tg=f"P3 slope {p3:.4f} vs equal weights {eq:.4f}: {_w(rel(p3, eq) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the exponential model's slope is lambda per position (log strength rising toward the end of the list) for every lambda; it equals P3's {p3:.4f} only at lambda = ln(1/q) = {math.log(1 / Q0):.4f} per item",
                    tc="tried: (i) the shape: both are log-linear in lag for every lambda, so shape agreement is automatic and not Q; (ii) the slope value: agreement within 1 % holds iff lambda lies within 1 % of ln 2 per item, a free parameter of the domain model that declared.py does not name and no simulation can fix; fixing it would choose the verdict; the data that would (a free-recall serial-position set such as Murdock 1962) is not in data/SEEN.md and was not opened -> not computable",
                    out=out,
                    reading="P3's geometric occasion weights are an exponential decay counted in items; whether the slope matches the domain's decay model depends only on the domain's decay rate per item, which the declaration leaves open, so the row is UNSTATED rather than decided by an implementer's choice of lambda; primacy by rehearsal does not enter the recency slope in this construction",
                    weakness="an implementer could pick lambda = ln 2 (Q holds trivially) or any other value (Q fails); both are refused as choosing the verdict",
                    elegance="", child="")


# ---------------------------------------------------------------- P04-4 power law of practice
N_TR = np.arange(1, 101, dtype=float)
N_LEARN, NOISE = 50, 0.05


def _fit(y, kind):
    """Three-parameter fit y ~ A + B g(N; c) (exponential g = exp(-c (N-1)), power g = N^-c), A and B by linear least
    squares, c by a log grid then a bounded scalar refinement. Returns the SSE."""
    def sse(c):
        g = np.exp(-c * (N_TR - 1)) if kind == "exp" else N_TR ** (-c)
        X = np.column_stack([np.ones_like(g), g]); beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        return float(((y - X @ beta) ** 2).sum())
    grid = np.geomspace(1e-4, 20.0, 400); vals = np.array([sse(c) for c in grid]); k = int(np.argmin(vals))
    a, b = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    res = minimize_scalar(sse, bounds=(a, b), method="bounded", options={"xatol": 1e-10})
    return min(float(res.fun), float(vals[k]))


def _learners(kind, q=Q0, seed=20260929):
    rng = np.random.default_rng(seed); ys = []
    for _ in range(N_LEARN):
        A = rng.uniform(0.4, 0.6); B = rng.uniform(0.1, 0.3, 3); e = NOISE * rng.standard_normal(N_TR.size)
        if kind == "a6":                  # three components, each remembered by A6 at q per trial
            y = A + sum(Bc * q ** (N_TR - 1) for Bc in B)
        elif kind == "apex":              # Heathcote et al.'s exponential, rate ln(1/q) per trial
            y = A + B.sum() * np.exp(-math.log(1 / q) * (N_TR - 1))
        elif kind == "mix":               # components at the three grid values of q
            y = A + sum(Bc * qq ** (N_TR - 1) for Bc, qq in zip(B, QGRID))
        else:                             # the power law N^-0.5
            y = A + B.sum() * N_TR ** (-0.5)
        ys.append(y + e)
    return ys


def _frac_exp(ys):
    wins = [(_fit(y, "exp") < _fit(y, "pow")) for y in ys]
    return sum(wins) / len(wins)


def r4():
    i = "P04-4"; d = _decl(i)
    crr = _frac_exp(_learners("a6")); null = _frac_exp(_learners("pow")); domain = _frac_exp(_learners("apex"))
    check = crr == 1.0
    sens = "; ".join(f"q = {q}: {_frac_exp(_learners('a6', q)):.2f}" for q in QGRID) + f"; three components at q = 0.25, 0.5, 0.75 together: {_frac_exp(_learners('mix')):.2f}"
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("learn", d["system"] + f"; model: {N_LEARN} seeded learners, RT_N = A + sum of three components B_c q^(N-1) (each an A6 memory at q per trial) + Gaussian noise sd {NOISE}, N = 1..100; exponential A + B exp(-c(N-1)) and power A + B N^-c fitted by least squares (three parameters each)",
                    source=_src(i),
                    Q=d["Q"] + " (computed as: the fraction of learners whose exponential SSE is lower than the power SSE; Q holds only if it is 1, per learner)",
                    ingredient=d["ingredient"] + " (bounded memory with geometric weights: an exponential approach per component)",
                    null=d["null"] + " (learners generated by RT = A + B N^-0.5 + noise)",
                    domain=d["H0"] + " (computed: learners generated by the exponential with rate ln(1/q) per trial, the same draws)",
                    numbers=f"fraction with the exponential better: A6 learners {crr:.2f}, power-law learners {null:.2f}, Heathcote exponential learners {domain:.2f}; q-grid sensitivity (A6 learners): {sens}",
                    tg=f"{crr:.2f} vs null {null:.2f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Heathcote's exponential learners {domain:.2f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"exponential better on every A6 learner ({crr:.2f}): {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"a learner whose components are A6 memories at one q is an exponential learner (the components add to one exponential), yet the exponential fits better on {crr:.2f} of the learners, not all: at this noise a steep power law (large exponent) can mimic a fast exponential drop over the first few trials; the domain's own exponential learners give {domain:.2f}, so the shortfall {_w(rel(crr, domain) <= TOL_N, 'is the fit failing to separate the forms, not the memory', 'differs from the domain learners')}; the mixture line ({_frac_exp(_learners('mix')):.2f}) shows components forgetting at different rates pushing the curve toward a power law",
                    weakness="the Q is close to circular: data generated by an exponential are fitted better by an exponential; 'every learner' (per learner, R6) was fixed in the code before the first run, and a majority reading would read the other way; the noise level, the number of trials and the power-law exponent of the null are my choices; the domain comparator uses the same random draws, so T-N agreement is by construction",
                    elegance="", child="")


# ---------------------------------------------------------------- P04-5 TD relearning on a 5-state chain
TD_SEEDS, TD_EP, TD_CHANGE = 200, 2000, 500
TRUE_OLD = np.arange(1, 6) / 6.0; TRUE_NEW = 1.0 - TRUE_OLD


def _td(rule, alpha=0.5, seed=20260929):
    """Sutton-Barto 5-state random walk (start in the middle, left/right with probability 1/2). Reward 1 on the right exit
    before episode TD_CHANGE, on the left exit from then on. TD(0), V0 = 0.5. rule: 'a6' V <- (1-q) target + q V;
    'const' V <- V + alpha (target - V); 'inv' alpha = 1/n(s). All seeds run in lockstep with identical walks.
    Returns the seed-mean value vector after each episode (TD_EP, 5) and the per-run RMS error after each episode."""
    rng = np.random.default_rng(seed); S = TD_SEEDS
    V = np.full((S, 5), 0.5); cnt = np.zeros((S, 5)); ar = np.arange(S)
    meanV = np.empty((TD_EP, 5)); rms = np.empty((TD_EP, S))
    for ep in range(TD_EP):
        right = 1.0 if ep < TD_CHANGE else 0.0
        s = np.full(S, 2); live = np.ones(S, bool)
        while live.any():
            step = np.where(rng.random(S) < 0.5, 1, -1); s2 = s + step
            term_r = s2 == 5; term_l = s2 == -1; term = term_r | term_l
            r = np.where(term_r, right, np.where(term_l, 1.0 - right, 0.0))
            v2 = np.where(term, 0.0, V[ar, np.clip(s2, 0, 4)])
            tgt = r + v2; idx = ar[live]; si = s[live]
            if rule == "a6":
                V[idx, si] = (1 - alpha) * tgt[live] + alpha * V[idx, si]
            elif rule == "const":
                V[idx, si] = V[idx, si] + alpha * (tgt[live] - V[idx, si])
            else:
                cnt[idx, si] += 1.0; V[idx, si] = V[idx, si] + (tgt[live] - V[idx, si]) / cnt[idx, si]
            live = live & ~term; s = np.where(live, s2, s)
        truth = TRUE_OLD if ep < TD_CHANGE else TRUE_NEW
        meanV[ep] = V.mean(axis=0); rms[ep] = np.sqrt(((V - truth) ** 2).mean(axis=1))
    return meanV, rms


HALF = 0.5 * float(np.sqrt(((TRUE_OLD - TRUE_NEW) ** 2).mean()))


def _relearn(meanV):
    """Episodes after the change until the seed-mean value vector is within half the old-new distance of the new truth
    (RMS); censored at the horizon (encoded as the horizon)."""
    d = np.sqrt(((meanV[TD_CHANGE:] - TRUE_NEW) ** 2).mean(axis=1))
    hit = np.flatnonzero(d <= HALF)
    return (float(hit[0] + 1), False) if hit.size else (float(TD_EP - TD_CHANGE), True)


def r5():
    i = "P04-5"; d = _decl(i)
    mA, rA = _td("a6", alpha=Q0); mI, rI = _td("inv"); mC, rC = _td("const", alpha=1 - Q0)
    (crr, cA), (null, cI), (domain, cC) = _relearn(mA), _relearn(mI), _relearn(mC)
    check = crr < null
    noise = lambda r: float(r[TD_CHANGE - 100:TD_CHANGE].mean())
    sens = "; ".join(f"q = {q}: {_relearn(_td('a6', alpha=q)[0])[0]:.0f} episodes" for q in QGRID)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    cens = lambda c: _w(c, " (censored: not reached by the horizon)", "")
    return make_row("learn", d["system"] + f"; model: Sutton-Barto 5-state random walk, reward 1 on the right exit, moved to the left exit at episode {TD_CHANGE}; TD(0), V0 = 0.5, {TD_SEEDS} seeded runs of {TD_EP} episodes with identical walks across rules",
                    source=_src(i),
                    Q=d["Q"] + f" (computed as: episodes after the change until the seed-mean value vector is within half the old-to-new distance ({HALF:.4f} RMS) of the new values)",
                    ingredient=d["ingredient"] + " (V(s) <- (1 - q) target + q V(s), q = 0.5: the settled past at bounded strength)",
                    null=d["null"] + " (alpha = 1/n(s), the sample average of the targets)",
                    domain=d["H0"] + f" (computed: constant alpha = 1 - q = {1 - Q0})",
                    numbers=f"relearning episodes: A6 {crr:.0f}{cens(cA)}, 1/n {null:.0f}{cens(cI)}, constant alpha = 1 - q {domain:.0f}{cens(cC)}; per-run RMS error over the 100 episodes before the change (tracking noise): A6 {noise(rA):.4f}, 1/n {noise(rI):.4f}, constant alpha {noise(rC):.4f}; q-grid sensitivity (A6): {sens}",
                    tg=f"{crr:.0f} vs null {null:.0f} episodes: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"constant step-size TD at alpha = 1 - q, {domain:.0f} episodes: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"A6 relearning {crr:.0f} < 1/n relearning {null:.0f}: {_w(check, 'holds', 'fails')} -> {_w(check, 'Q holds', 'Q fails')}",
                    out=out,
                    reading=f"A6-bounded value memory is constant step-size TD with alpha = 1 - q, so it relearns in {crr:.0f} episodes where the sample average needs {null:.0f}{cens(cI)}; the price is tracking noise before the change ({noise(rA):.4f} against {noise(rI):.4f} RMS); Sutton and Barto's constant step size is the domain's name for the same learner",
                    weakness="the relearning criterion (half the old-new distance, on the seed mean) is my choice; the A6 and constant-step learners are the same recursion written two ways, so T-N agreement is an identity",
                    elegance=_w(check, "A learner that gives the past a fixed, limited say can change its mind when the world changes; one that averages everything it has ever seen gets stuck in the old world.", ""),
                    child=_w(check, "If you always trust the last few days a lot, you notice quickly when things change. If you add up everything since the beginning, it takes you ages to notice.", ""))


def main():
    return run_batch("PRED70 batch P04: learning and cognition (Predictions70/DECLARATION.md; prompt-log entry 234)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
