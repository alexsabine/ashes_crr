"""PRED70 batch P09: economics and finance (Predictions70/DECLARATION.md; prompt-log entry 234). Rows P09-1..P09-5 of
Predictions70/declared.py (pushed in commit 8397478 before any model existed). [1] GARCH(1,1) volatility against an A6
bounded mean of squared returns; [2] a discrete Kaldor business cycle with investment on A6-remembered income; [3] Metzler's
inventory cycle with A6 sales expectations; [4] P3 geometric weights as a discount function against hyperbolic discounting;
[5] trading at A3 antipodal cuts of a causal price phase on a random walk with volatility regimes. Literature named by name
and year only (R10): Bollerslev 1986; Kaldor 1940; Metzler 1941; Strotz 1955; Mazur 1987. Deterministic; about 15 s."""
import math
import sys
from pathlib import Path

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.signal import hilbert, lfilter

from crr.instrument.core import antipodal_cuts, intrinsic_phase
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from declared import P  # noqa: E402

D = {p[0]: p for p in P}
QGRID = (0.25, 0.5, 0.75)
Q0 = 0.5


def _w(cond, yes, no):
    return yes if cond else no


def _decl(pid):
    _, _, cls, system, ingredient, Q, null, H0, forecast = D[pid]
    return cls, system, ingredient, Q, null, H0, f"PRED70 {pid} (declared at 8397478; forecast {forecast})"


def _qh(check):
    return _w(check is None, "-> not computable", _w(check, "-> Q holds", "-> Q fails"))


# ---------------------------------------------------------------- [1] GARCH(1,1) against an A6 bounded mean
G_OM, G_AL, G_BE = 0.05, 0.10, 0.85


def _garch_path(n, burn, seed=0):
    z = np.random.default_rng(seed).standard_normal(n + burn).tolist()
    v = G_OM / (1 - G_AL - G_BE); s2 = [0.0] * (n + burn); r = [0.0] * (n + burn)
    for t in range(n + burn):
        s2[t] = v; rt = math.sqrt(v) * z[t]; r[t] = rt; v = G_OM + G_AL * rt * rt + G_BE * v
    return np.array(s2), np.array(r)


def _a6_forecast(r2, q, f0):
    """f[t] = (1 - q) r2[t] + q f[t-1]: the A6 bounded mean (weights (1 - q) q^k over occasion age k), made at t for t + 1."""
    return lfilter([1 - q], [1, -q], r2, zi=[q * f0])[0]


def _garch_ratio_theory(q, M=6000):
    """MSE(A6 q)/MSE(GARCH) against r^2_{t+1}, from GARCH's ARMA(1,1) representation of r^2 (Bollerslev 1986):
    r^2_t - s^2_t = v_t is a martingale difference, s^2_{t+1} - mu = sum_m alpha phi^m v_{t-m}; the A6 mean loads
    (1 - q)[q^m + alpha (phi^m - q^m)/(phi - q)] on v_{t-m}; the ratio is 1 + sum_m (a_m - b_m)^2."""
    phi = G_AL + G_BE; m = np.arange(M)
    a = (1 - q) * (q ** m + G_AL * (phi ** m - q ** m) / (phi - q)); b = G_AL * phi ** m
    return float(1.0 + np.sum((a - b) ** 2))


def r1():
    cls, system, ing, Q, nul, H0, src = _decl("P09-1")
    n, burn = 2_000_000, 10_000
    s2, r = _garch_path(n, burn); r2 = r * r; mu = G_OM / (1 - G_AL - G_BE)
    target = r2[burn + 1:]; g = s2[burn + 1:]; mse_g = float(np.mean((target - g) ** 2))
    sim, thy, lat = {}, {}, {}
    for q in QGRID:
        f = _a6_forecast(r2, q, mu)[burn:-1]
        sim[q] = float(np.mean((target - f) ** 2)) / mse_g; thy[q] = _garch_ratio_theory(q)
        lat[q] = float(np.mean((g - f) ** 2)) / float(np.mean(g ** 2))
    fgeo = np.exp(lfilter([1 - Q0], [1, -Q0], np.log(r2), zi=[Q0 * math.log(mu)])[0])[burn:-1]
    geo = float(np.mean((target - fgeo) ** 2)) / mse_g
    crr, null, domain = sim[Q0], 1.0, thy[Q0]
    check = crr <= 1.0 + TOL_G
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    grid = "; ".join(f"q = {q}: simulated {sim[q]:.4f}, theory {thy[q]:.4f}" for q in QGRID)
    return make_row(cls, f"{system} (computed as: z ~ N(0,1), {n} steps after {burn} burn-in, seed 0; one-step forecasts of r^2_(t+1); GARCH at its true parameters)",
                    source=src, Q=Q, ingredient=f"{ing}: f_(t+1) = (1 - q) r_t^2 + q f_t, q = 0.5 per occasion (one return per occasion), weights (1 - q) q^k over age k",
                    null=nul, domain=H0,
                    numbers=f"MSE ratio A6/GARCH against the realised r^2_(t+1): {crr:.6f} (q = 0.5, decides); GARCH-ARMA theory for the same ratio {domain:.6f}; "
                            f"q-grid (sensitivity only): {grid}; against the latent s^2_(t+1) (where GARCH's error is 0) the A6 relative MSE is {lat[Q0]:.4f}; "
                            f"Fisher-Rao reading (geometric mean of squared returns, q = 0.5): ratio {geo:.4f}",
                    tg=f"A6 ratio {crr:.4f} vs GARCH {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the GARCH-ARMA representation gives {domain:.4f} for the A6 tracker's ratio: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has the number)', 'differ')}",
                    tc=f"A6 MSE within 1 % of GARCH's (ratio {crr:.4f} <= {1 + TOL_G:.2f}): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"an A6 mean at q = 0.5 is an exponential moving average with decay 0.5 and no constant; GARCH is the same filter with decay beta = {G_BE} plus a constant, so the A6 tracker is a misspecified GARCH and its mean squared error is {_w(crr > 1, 'above', 'not above')} GARCH's by {100 * (crr - 1):.1f} %; the domain's own ARMA algebra predicts the ratio to within {100 * rel(crr, domain):.2f} %; "
                            f"on the q-grid the ratio {_w(sim[0.25] > sim[0.5] > sim[0.75], 'falls toward 1 as q approaches beta', 'does not fall monotonically as q approaches beta')} (q = 0.75: {sim[0.75]:.4f}); "
                            f"the Fisher-Rao reading (geometric mean) gives {geo:.4f}, {_w(geo > crr, 'worse than', 'better than')} the arithmetic reading and {_w(geo <= 1.0 + TOL_G, 'within', 'outside')} 1 % of GARCH",
                    weakness="GARCH is scored at its true parameters (the domain model), not estimated; the target is the realised squared return (the standard proxy); the A6 mean is read as the arithmetic weighted mean of squared returns, the synthesis batches' A6 convention (the Fisher-Rao Frechet mean of Gaussian variances is the geometric mean; it is printed as a second reading, not deciding); Gaussian innovations",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] discrete Kaldor cycle with remembered income
K_A, K_S, K_B, K_D = 0.5, 0.3, 0.2, 0.1        # investment slope at equilibrium, saving rate, capital effect, depreciation


def _kaldor_amp(q, alpha=1.5, n=40000, burn=20000):
    """y_{t+1} = y_t + alpha (i_t - s y_t), k_{t+1} = (1 - d) k_t + i_t, i_t = a arctan(m_t) - b k_t,
    m_t = (1 - q) y_t + q m_{t-1} (A6-remembered income; q = 0 is instantaneous income). Deviations from equilibrium."""
    y, k, m = 0.1, 0.0, 0.1; lo, hi = float("inf"), -float("inf")
    for t in range(n):
        m = (1 - q) * y + q * m
        i = K_A * math.atan(m) - K_B * k
        y, k = y + alpha * (i - K_S * y), (1 - K_D) * k + i
        if t >= burn:
            lo = min(lo, y); hi = max(hi, y)
    return (hi - lo) / 2


def _kaldor_modulus(q, alpha=1.5):
    J = np.array([[1 - alpha * K_S + alpha * K_A * (1 - q), -alpha * K_B, alpha * K_A * q],
                  [K_A * (1 - q), 1 - K_D - K_B, K_A * q], [1 - q, 0.0, q]])
    return float(np.abs(np.linalg.eigvals(J)).max())


def r2():
    cls, system, ing, Q, nul, H0, src = _decl("P09-2")
    amp = {q: _kaldor_amp(q) for q in (0.0,) + QGRID}
    crr, null = amp[Q0], amp[0.0]
    shrink = (null - crr) / null; check = shrink > TOL_G
    out = outcome(crr=crr, null=null, domain=None, check=check)
    scan = "; ".join(f"alpha = {al}: q = 0 {_kaldor_amp(0.0, al):.4f}, q = 0.5 {_kaldor_amp(Q0, al):.4f}" for al in (2.0, 3.0))
    mod0, modq = _kaldor_modulus(0.0), _kaldor_modulus(Q0)
    sc = [(_kaldor_amp(0.0, al), _kaldor_amp(Q0, al)) for al in (2.0, 3.0)]
    sc_small = all(b_ < a_ for a_, b_ in sc); sc_alive = all(b_ > 1e-6 for _, b_ in sc)
    return make_row(cls, f"{system} (computed as: discrete Kaldor map in deviations, y' = y + alpha (I - s y), k' = (1 - d) k + I, I = a arctan(m) - b k, alpha = 1.5, a = {K_A}, s = {K_S}, b = {K_B}, d = {K_D}; one occasion = one period; amplitude = half the range of y over iterates 20000-39999)",
                    source=src, Q=Q, ingredient=f"{ing}: m_t = (1 - q) y_t + q m_(t-1), q = 0.5, the income investment responds to",
                    null=nul, domain=H0,
                    numbers=f"limit-cycle amplitude of income: A6 {crr:.6g}, instantaneous {null:.6f}; shrink {100 * shrink:.2f} %; largest eigenvalue modulus at the equilibrium: instantaneous {mod0:.4f} ({_w(mod0 > 1, 'unstable, a cycle', 'stable')}), A6 {modq:.4f} ({_w(modq > 1, 'unstable, a cycle', 'stable')}); "
                            f"q-grid (sensitivity only): " + "; ".join(f"q = {q}: {amp[q]:.4g}" for q in QGRID) + f"; robustness over the adjustment speed: {scan}",
                    tg=f"amplitude {crr:.4g} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no theorem cited for the memory variant",
                    tc=f"amplitude shrinks by more than 1 % ({100 * shrink:.2f} %): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"investment on remembered income {_w(crr < null, 'shrinks', 'does not shrink')} the Kaldor cycle; at alpha = 1.5 the equilibrium's largest modulus goes from {mod0:.4f} to {modq:.4f}, so {_w(modq < 1, 'the cycle disappears (a Neimark-Sacker bifurcation is undone)', 'the cycle survives')}; at faster adjustment (alpha = 2.0, 3.0) the cycle {_w(sc_alive, 'survives', 'does not survive')} and is {_w(sc_small, 'smaller with memory', 'not smaller with memory in every case')} ({scan}); Kaldor models with lags and adaptive expectations are an existing literature that may contain this (not checked)",
                    weakness="one discrete-time Kaldor map with arctan investment; the parameters were chosen to put the memoryless equilibrium just past its Neimark-Sacker point (modulus above 1), where any stabilising term can remove the cycle; the robustness scan is printed for that reason; savings respond to current income, only investment to remembered income (one choice of where A6 acts)",
                    elegance="", child="")


# ---------------------------------------------------------------- [3] Metzler inventory cycle with A6 expectations
M_B = 0.8     # marginal propensity to consume


def _metzler(q, b=M_B):
    """Deviations. Sales_t = b y_t; expected sales E_t = (1 - q) b y_{t-1} + q E_{t-1} (A6; q = 0 is naive, E_t = b y_{t-1});
    production y_t = E_t + (b y_{t-1} - E_{t-1}) (production for sale plus replacing last period's unintended depletion).
    State (y_{t-1}, E_{t-1}) -> (y_t, E_t)."""
    J = np.array([[b * (2 - q), -(1 - q)], [(1 - q) * b, q]])
    ev = np.linalg.eigvals(J); k = int(np.argmax(np.abs(ev))); lam = ev[k]
    return float(math.log(abs(lam))), float(abs(np.angle(lam))), float(np.linalg.det(J))


def r3():
    cls, system, ing, Q, nul, H0, src = _decl("P09-3")
    res = {q: _metzler(q) for q in (0.0,) + QGRID}
    crr, null = res[Q0][0], res[0.0][0]; domain = math.log(math.sqrt(M_B))
    diff = crr - null; check = (null - crr) > TOL_G * abs(null)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    dec = {q: -res[q][0] * 2 * math.pi / res[q][1] for q in (0.0, Q0)}
    per = {q: 2 * math.pi / res[q][1] for q in (0.0, Q0)}
    grid = "; ".join(f"q = {q}: real part {res[q][0]:.6f}, det {res[q][2]:.6f}" for q in QGRID)
    return make_row(cls, f"{system} (computed as: Metzler's pure inventory cycle in deviations, b = {M_B}, production = expected sales + replacement of last period's unintended inventory depletion; damping = ln|lambda_max| per period, the real part of the continuous-time exponent)",
                    source=src, Q=Q, ingredient=f"{ing}: E_t = (1 - q) sales_(t-1) + q E_(t-1), q = 0.5",
                    null=nul, domain=H0,
                    numbers=f"real part ln|lambda|: A6 {crr:.12f}, naive {null:.12f}, difference {diff:.2e}; Metzler's closed form for the pure inventory cycle ln sqrt(b) = {domain:.12f}; "
                            f"cycle period (periods): A6 {per[Q0]:.3f}, naive {per[0.0]:.3f}; log decrement per cycle (not the Q's quantity): A6 {dec[Q0]:.4f}, naive {dec[0.0]:.4f}; q-grid (sensitivity only): {grid}",
                    tg=f"real part {crr:.6f} vs null {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Metzler's ln sqrt(b) = {domain:.6f}: {_w(rel(crr, domain) <= TOL_N, 'agree', 'differ')}",
                    tc=f"real part more negative with memory by more than 1 % (difference {diff:.2e}): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"the determinant of the A6 Metzler map is b = {res[Q0][2]:.6f} {_w(all(abs(res[q][2] - M_B) < 1e-12 for q in (0.0,) + QGRID), 'at every q on the grid', 'NOT at every q on the grid')} (the q terms cancel: b[q(2 - q) + (1 - q)^2] = b), so while the roots are complex ({_w(all(res[q][1] > 1e-9 for q in (0.0,) + QGRID), 'they are, at every q on the grid', 'they are NOT at every q on the grid')}) their modulus is sqrt(b) and the damping per period is {_w(abs(diff) < 1e-9, 'exactly unchanged', 'changed')} by memory; memory {_w(per[Q0] > per[0.0], 'lengthens', 'shortens')} the cycle from {per[0.0]:.3f} to {per[Q0]:.3f} periods, so the decay per cycle {_w(dec[Q0] > dec[0.0], 'rises', 'falls')}, but the Q names the real part",
                    weakness="one reading of Metzler's model (constant normal inventory, the pure inventory cycle); Metzler's own expectation coefficient is extrapolative, not the adaptive A6 mean, so H0's number is the naive case; a model with a desired inventory proportional to expected sales would give a different determinant",
                    elegance="The inventory cycle's decay per period is fixed by how much of their income people spend, whatever memory the firms use for their sales forecasts: memory changes the rhythm, not the fade.",
                    child="Shops that guess next month's sales from a blend of past months make the ups and downs slower, but the ups and downs fade away just as fast each month as before.")


# ---------------------------------------------------------------- [4] P3 geometric weights as a discount function
def _reversals(D, ratios, gaps, delays):
    rev = ties = total = 0
    for x2 in ratios:
        for d in gaps:
            prefs = []
            for tau in delays:
                a, b = 1.0 * D(tau), x2 * D(tau + d)
                if abs(a - b) <= 1e-12 * max(a, b):
                    ties += 1; continue
                prefs.append(a > b)
            total += 1
            if len(set(prefs)) > 1:
                rev += 1
    return rev, ties, total


def r4():
    cls, system, ing, Q, nul, H0, src = _decl("P09-4")
    ratios = [round(1.05 + 0.1 * k, 2) for k in range(90)]; gaps = range(1, 11); delays = range(0, 21); HK = 1.0
    geo = {q: _reversals(lambda t, q=q: q ** t, ratios, gaps, delays) for q in QGRID}
    hyp = _reversals(lambda t: 1.0 / (1.0 + HK * t), ratios, gaps, delays)
    crr, null, domain = float(geo[Q0][0]), float(hyp[0]), 0.0
    check = geo[Q0][0] == 0
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row(cls, f"{system} (computed as: choices between 1 unit at delay tau and x units at tau + d; x in 1.05..9.95 step 0.1, d in 1..10 periods, front-end delay tau in 0..20; a pair shows a reversal when its preference changes sign across tau; hyperbolic D = 1/(1 + k t), k = {HK} per period)",
                    source=src, Q=Q, ingredient=f"{ing}: D(t) = q^t, q = 0.5 per occasion (one period per occasion)",
                    null=nul, domain=H0,
                    numbers=f"pairs with a preference reversal: geometric (q = 0.5) {geo[Q0][0]} of {geo[Q0][2]} (ties excluded {geo[Q0][1]}); hyperbolic {hyp[0]} of {hyp[2]} (ties {hyp[1]}); Strotz: 0; "
                            f"q-grid (sensitivity only): " + "; ".join(f"q = {q}: {geo[q][0]} reversals" for q in QGRID),
                    tg=f"reversals {crr:.0f} vs null {null:.0f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"Strotz's theorem gives {domain:.0f} reversals for exponential discounting: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"no preference reversal under P3 weights ({geo[Q0][0]} reversals): {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"P3's geometric age weights are exponential discounting with factor q per occasion; the ratio D(tau + d)/D(tau) = q^d does not depend on tau, so no choice reverses as the choice is pushed into the future ({geo[Q0][0]} reversals against hyperbolic {hyp[0]}); {_w(rel(crr, domain) <= TOL_N, 'this is the theorem of Strotz, which the domain has had since 1955', 'this departs from the theorem of Strotz')}",
                    weakness="the choice grid and the hyperbolic k are one choice each; P3 fixes only the form, so the row is the domain's theorem restated in CRR's terms",
                    elegance="If each step into the future counts the same fraction less than the step before, you never change your mind just because time has passed.",
                    child="Suppose every extra day of waiting makes a treat feel half as good. Then whether you pick the small treat now or the big one later, you will make the same choice today, tomorrow and next week.")


# ---------------------------------------------------------------- [5] trading at A3 cuts of the price phase
PW = 128      # causal phase window (samples)


def _causal_phase(p, W=PW, chunk=20000):
    """At each t >= W - 1: the instrument's intrinsic phase (analytic signal of the mean-removed window) at the last
    sample of the window p[t-W+1 .. t] (uses no future sample). Wrapped; unwrapped over t by the caller."""
    out = np.full(len(p), np.nan); win = sliding_window_view(p, W)
    for s in range(0, win.shape[0], chunk):
        X = win[s:s + chunk]; X = X - X.mean(axis=1, keepdims=True)
        out[s + W - 1:s + W - 1 + X.shape[0]] = np.angle(hilbert(X, axis=1)[:, -1])
    return out


def _trade(seed, n=50000, drift=0.0, sig=(0.01, 0.03), switch=1 / 250):
    rng = np.random.default_rng(seed)
    sw = rng.random(n) < switch; reg = np.cumsum(sw) % 2
    s = np.where(reg == 0, sig[0], sig[1]); m = np.where(reg == 0, drift, -drift)
    dp = m + s * rng.standard_normal(n); dp[0] = 0.0; p = np.cumsum(dp)
    ph = np.unwrap(_causal_phase(p)[PW - 1:])
    cuts = antipodal_cuts(ph) + (PW - 1)
    ex = cuts[1:] + 1; ex = ex[ex < n - 1]          # a cut at c is known by sample c + 1: trade at the close of c + 1
    pos = np.zeros(n)
    for k in range(1, len(ex)):
        e = ex[k]; nxt = ex[k + 1] if k + 1 < len(ex) else n
        pos[e:nxt] = -np.sign(p[e] - p[ex[k - 1]])  # contrarian: the cut is a half-turn, so bet on the reversal
    strat = pos[:-1] * dp[1:]
    return strat[ex[1]:], dp[ex[1] + 1:], len(cuts)


def _stat(x):
    m = float(np.mean(x)); se = float(np.std(x, ddof=1) / math.sqrt(len(x)))
    return m, se, (m - 1.96 * se, m + 1.96 * se)


def r5():
    cls, system, ing, Q, nul, H0, src = _decl("P09-5")
    seeds = range(8)
    runs = [_trade(sd) for sd in seeds]
    S = np.concatenate([a for a, _, _ in runs]); B = np.concatenate([b for _, b, _ in runs]); ncut = sum(c for _, _, c in runs)
    ms, ses, cis = _stat(S); mb, seb, cib = _stat(B)
    res_s = cis[0] > 0 or cis[1] < 0; res_b = cib[0] > 0 or cib[1] < 0
    crr = ms if res_s else 0.0; null = mb if res_b else 0.0; domain = 0.0
    check = cis[0] > 0
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    druns = [_trade(sd, drift=0.002, sig=(0.02, 0.02)) for sd in seeds]
    Sd = np.concatenate([a for a, _, _ in druns]); md, sed, cid = _stat(Sd)
    pc = np.cumsum(np.random.default_rng(99).standard_normal(400))
    ok = abs(_causal_phase(pc)[300] - float(np.angle(np.exp(1j * intrinsic_phase(pc[300 - PW + 1:301])[-1])))) < 1e-9
    return make_row(cls, f"{system} (computed as: log price a Gaussian random walk, zero drift, volatility switching between 0.01 and 0.03 with probability 1/250 per step; 8 seeds x 50000 steps; causal phase = the instrument's intrinsic phase at the last sample of a trailing {PW}-sample window, unwrapped over time; A3 cuts by antipodal_cuts; trades at the close after each cut is known, contrarian over the last occasion; zero cost)",
                    source=src, Q=Q, ingredient=f"{ing}: antipodal_cuts on the causal intrinsic phase (the batched window phase equals intrinsic_phase on the window: {_w(ok, 'yes', 'NO')})",
                    null=nul, domain=H0,
                    numbers=f"mean return per step: cut strategy {ms:.3e} (95 % CI {cis[0]:.3e} to {cis[1]:.3e}, t = {ms / ses:.2f}, {ncut} cuts); buy-and-hold {mb:.3e} (CI {cib[0]:.3e} to {cib[1]:.3e}); "
                            f"values at resolution passed to the harness (0 when the CI includes 0): cut {crr:.3e}, buy-and-hold {null:.3e}, EMH {domain:.1f}; "
                            f"sensitivity (not deciding): drift regimes +-0.002 at volatility 0.02, cut strategy {md:.3e} (CI {cid[0]:.3e} to {cid[1]:.3e})",
                    tg=f"cut strategy {crr:.3e} vs buy-and-hold {null:.3e} (at resolution): {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"efficient markets give {domain:.1f}: {_w(rel(crr, domain) <= TOL_N, 'agree', 'differ')}",
                    tc=f"a positive mean return, CI lower bound {cis[0]:.3e} above 0: {_w(check, 'holds', 'fails')} {_qh(check)}",
                    out=out,
                    reading=f"on a martingale price any position chosen from the past earns zero in expectation, and the cut strategy's mean return is {_w(res_s, 'resolved from', 'not resolved from')} zero (t = {ms / ses:.2f}); the antipodal cut of a causal phase is one more rule chosen from the past; with drift regimes the contrarian cut rule {_w(cid[1] < 0, 'loses resolvably', _w(cid[0] > 0, 'gains resolvably', 'is not resolved from zero'))}{_w(cid[1] < 0, ', because regime drift rewards following, not reversing', '')}",
                    weakness="DEVIATION: 'positive' is read at one resolvable step (the 95 % CI of the mean excludes 0, R5), because on a random walk a bare positive point estimate is a coin toss; the raw means are printed; the harness receives the means at resolution (0 when the CI includes 0), because a relative tolerance on two noise-level zeros is undefined. The instrument's global intrinsic phase uses future samples and cannot be traded, so a trailing window is used (window length a choice); the regime shifts are in volatility, keeping the price a martingale as H0 states; the direction (contrarian) is one choice and momentum is its exact negative",
                    elegance="", child="")


def main():
    return run_batch("PRED70 batch P09: economics and finance (Predictions70/DECLARATION.md; prompt-log entry 234; declared at 8397478)",
                     [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
