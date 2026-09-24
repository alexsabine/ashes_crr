"""RLAW instrument: the regeneration law's estimators (Regeneration_Law/DECLARATION_1.md, DECLARATION_2.md).

The law (CRR 2.0, prompt-log entry 137): a system that regenerates from its settled past weights its newest input by
alpha* = K(v), K(v) = (v/2)(sqrt(v^2 + 4) - v), v = the environment's drift per occasion in the system's own resolvable steps.

Estimators (every constant is a named argument, R5):
- v_hat: maximum likelihood of the local-level model (random walk + white noise) on the environment series, the variance
  ratio q = v^2 found on a fixed log grid and refined by a parabola through the three grid points at the minimum; the
  observation scale is concentrated out. Missing values (NaN) are skipped by the filter (prediction only).
- own unit: v_own = sigma_eta / sqrt(sigma_eps^2 + delta^2 / 12), delta the system's reporting quantum (A1').
- alpha_hat: partial-adjustment least squares with intercept, s_t - s_{t-1} = alpha (x_t - s_{t-1}) + c.
- the two-step second stage: per-subject ML of a delta-rule learner (alpha on a fixed log grid, beta by bounded scalar fit).
Deterministic: no random numbers are drawn here."""
import math

import numpy as np
from scipy.optimize import minimize_scalar

LOGV_LO, LOGV_HI, LOGV_N = -3.0, 2.0, 1001


def K(v):
    v = np.asarray(v, float); return (v / 2.0) * (np.sqrt(v * v + 4.0) - v)


def _conc_nll(Y, logv_grid):
    """Concentrated negative log-likelihood of the local-level model. Y (B, n) with NaN = missing.
    Returns nll (B, G) and r_hat (B, G) (the observation variance at each grid point)."""
    Y = np.atleast_2d(np.asarray(Y, float)); B, n = Y.shape; q = (10.0 ** logv_grid) ** 2; G = q.size
    first = np.argmax(~np.isnan(Y), axis=1)
    m = np.zeros((B, G)); P = np.full((B, G), np.nan); S = np.zeros((B, G)); L = np.zeros((B, G)); N = np.zeros((B, 1))
    for t in range(n):
        y = Y[:, t:t + 1]; obs = ~np.isnan(y); start = (first == t)[:, None]
        started = ~np.isnan(P)
        # predict
        P = np.where(started, P + q, P)
        upd = obs & started
        F = P + 1.0; e = np.where(upd, y - m, 0.0); Kg = P / F
        S = S + np.where(upd, e * e / F, 0.0); L = L + np.where(upd, np.log(np.where(upd, F, 1.0)), 0.0); N = N + upd[:, :1]
        m = np.where(upd, m + Kg * e, m); P = np.where(upd, P / F, P)
        # initialise at the first observation (diffuse start: the first datum fixes the level, prior variance 1 obs unit)
        m = np.where(start & obs, np.broadcast_to(y, m.shape), m); P = np.where(start & obs, 1.0, P)
    r = S / np.maximum(N, 1.0)
    nll = 0.5 * N * np.log(np.maximum(r, 1e-300)) + 0.5 * L
    return nll, r


def ml_v(Y, logv_lo=LOGV_LO, logv_hi=LOGV_HI, logv_n=LOGV_N):
    """ML local-level fit. Returns dict of arrays (B,): v, sigma_eta2, sigma_eps2, edge (True if the minimum is at a grid end)."""
    grid = np.linspace(logv_lo, logv_hi, logv_n); nll, r = _conc_nll(Y, grid)
    i = np.argmin(nll, axis=1); B = nll.shape[0]; lv = grid[i].copy(); edge = (i == 0) | (i == logv_n - 1)
    for b in range(B):
        if 0 < i[b] < logv_n - 1:
            y0, y1, y2 = nll[b, i[b] - 1], nll[b, i[b]], nll[b, i[b] + 1]; den = y0 - 2 * y1 + y2
            if den > 0: lv[b] = grid[i[b]] + 0.5 * (grid[1] - grid[0]) * (y0 - y2) / den
    v = 10.0 ** lv
    # observation variance at the refined v: recompute per series (one grid point each)
    s_eps2 = np.array([_conc_nll(np.atleast_2d(np.asarray(Y, float))[b:b + 1], np.array([lv[b]]))[1][0, 0] for b in range(B)])
    return dict(v=v, sigma_eps2=s_eps2, sigma_eta2=v * v * s_eps2, edge=edge)


def mom_v(y):
    """Method of moments on first differences (Declaration 1, M9): var(dy) = s_eta^2 + 2 s_eps^2, cov(dy_t, dy_t-1) = -s_eps^2.
    NaNs are dropped first. Returns (v, s_eta2, s_eps2); a non-positive drift variance gives v = 0, a non-positive noise
    variance gives v = inf."""
    y = np.asarray(y, float); y = y[~np.isnan(y)]; d = np.diff(y); d = d - d.mean()
    g0 = float(np.mean(d * d)); g1 = float(np.mean(d[1:] * d[:-1])); s_eps2 = max(-g1, 0.0); s_eta2 = g0 - 2 * s_eps2
    if s_eta2 <= 0: return 0.0, 0.0, s_eps2
    if s_eps2 <= 0: return float("inf"), s_eta2, 0.0
    return math.sqrt(s_eta2 / s_eps2), s_eta2, s_eps2


def v_own(sigma_eta2, sigma_eps2, delta):
    return np.sqrt(np.asarray(sigma_eta2, float) / (np.asarray(sigma_eps2, float) + delta * delta / 12.0))


def alpha_hat(s, x):
    """Partial adjustment with intercept: s_t - s_{t-1} = alpha (x_t - s_{t-1}) + c. s and x aligned (x_t is the input the
    system has at occasion t). Rows with any NaN are dropped. Returns (alpha, c, n_used)."""
    s = np.asarray(s, float); x = np.asarray(x, float)
    z = s[1:] - s[:-1]; u = x[1:] - s[:-1]; ok = ~(np.isnan(z) | np.isnan(u))
    z, u = z[ok], u[ok]
    if z.size < 3: return float("nan"), float("nan"), int(z.size)
    A = np.column_stack([u, np.ones_like(u)]); coef, *_ = np.linalg.lstsq(A, z, rcond=None)
    return float(coef[0]), float(coef[1]), int(z.size)


# ---------------------------------------------------------------- the two-step second stage
ALPHA_GRID = np.exp(np.linspace(math.log(0.005), math.log(1.0), 200))
BETA_BOUNDS = (0.0, 50.0)


def q2_diffs(state2, choice2, win, valid, alphas=ALPHA_GRID, q0=0.0):
    """For each alpha on the grid: the chosen-minus-unchosen Q difference before each valid second-stage choice.
    state2 in {0, 1}, choice2 in {0, 1}, win in {0, 1}; valid masks missed trials. Q starts at q0 (0 in Kool 2016's code).
    Returns D (A, T_valid)."""
    A = alphas.size; Q = np.full((A, 2, 2), float(q0)); out = []
    for t in range(len(state2)):
        if not valid[t]: continue
        s, c, r = int(state2[t]), int(choice2[t]), float(win[t])
        out.append(Q[:, s, c] - Q[:, s, 1 - c])
        Q[:, s, c] = Q[:, s, c] + alphas * (r - Q[:, s, c])
    return np.array(out).T if out else np.zeros((A, 0))


def fit_q2(state2, choice2, win, valid, alphas=ALPHA_GRID, beta_bounds=BETA_BOUNDS, q0=0.0):
    """Per-subject ML over (alpha, beta). Returns (alpha_hat, beta_hat, nll, at_alpha_edge)."""
    D = q2_diffs(state2, choice2, win, valid, alphas, q0); best = (math.inf, None, None)
    for a in range(alphas.size):
        d = D[a]
        f = lambda b: float(np.sum(np.logaddexp(0.0, -b * d)))
        res = minimize_scalar(f, bounds=beta_bounds, method="bounded", options=dict(xatol=1e-6))
        if res.fun < best[0] - 1e-12: best = (float(res.fun), a, float(res.x))
    nll, a, b = best
    return float(alphas[a]), b, nll, bool(a == 0 or a == alphas.size - 1)


def arm_env(ps, state2, choice2, valid):
    """The two-step environment one subject faced, from the per-trial reward probabilities ps (T, 4) in Kool's column order
    (state 0 arm 0, state 0 arm 1, state 1 arm 0, state 1 arm 1). Returns sd of the per-trial drift (pooled over arms),
    the mean gap between consecutive visits of the same (state, arm), sigma_eps = sqrt(mean p(1-p)) at the visited arm, and
    v = sd_drift sqrt(mean gap) / sigma_eps (drift per occasion = per visit, in the outcome noise)."""
    ps = np.asarray(ps, float); inc = np.diff(ps, axis=0).ravel(); sd = float(np.sqrt(np.mean(inc * inc)))
    last = {}; gaps = []; pq = []
    for t in range(len(state2)):
        if not valid[t]: continue
        k = (int(state2[t]), int(choice2[t])); p = ps[t, 2 * k[0] + k[1]]; pq.append(p * (1 - p))
        if k in last: gaps.append(t - last[k])
        last[k] = t
    g = float(np.mean(gaps)) if gaps else float("nan"); se = float(math.sqrt(np.mean(pq)))
    return dict(sd_drift=sd, mean_gap=g, sigma_eps=se, v=sd * math.sqrt(g) / se)


# ---------------------------------------------------------------- the two-step arm's optimal constant rate (M13 rule)
TABLE_GAPS = (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0)


def optimal_rate(gbar, sd=0.025, lo=0.25, hi=0.75, seeds=200, visits=2000, burn=200, seed0=1300):
    """The constant delta-rule rate minimising the mean squared one-step error of a reward probability that follows a
    Gaussian random walk (sd per trial, reflecting at lo and hi) observed as a Bernoulli outcome on visits separated by
    geometric gaps of mean gbar (Declaration 2, M13). Grid 0.002 to 0.600, step 0.002."""
    al = np.arange(0.002, 0.602, 0.002); rng = np.random.default_rng(seed0 + int(round(gbar * 100)))
    p = rng.uniform(lo, hi, size=seeds); m = np.full((seeds, al.size), 0.5); se = np.zeros(al.size)
    for k in range(visits):
        steps = rng.geometric(1.0 / gbar, size=seeds) if gbar > 1 else np.ones(seeds, int)
        for j in range(int(steps.max())):
            mv = steps > j; p = np.where(mv, p + sd * rng.normal(size=seeds), p)
            p = np.where(p > hi, 2 * hi - p, p); p = np.where(p < lo, 2 * lo - p, p)
        r = (rng.uniform(size=seeds) < p).astype(float)
        if k >= burn: se += np.mean((p[:, None] - m) ** 2, axis=0)
        m = m + al[None, :] * (r[:, None] - m)
    return float(al[np.argmin(se)])


def rate_table(gaps=TABLE_GAPS):
    return np.array(gaps, float), np.array([optimal_rate(g) for g in gaps])


def table_rate(gbar, table):
    g, r = table; return float(np.interp(math.log(min(max(gbar, g[0]), g[-1])), np.log(g), r))
