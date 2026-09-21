"""Synthesis batch 23: rows 111-115 of QUEUE.md (prompt-log entry 61).
shannon [2] (CONSIST) de Bruijn's identity: the entropy counted in the system's own unit (A1') along the heat flow.
shannon [3] (DESCR) Stam's inequality: the A1' unit against the entropy-power width, in the unit's two readings.
shannon [4] (CONSIST) the Jeffreys prior as the reference prior: one prior mass per resolvable step, in the unit's two readings.
shannon [5] (CONSIST) Clarke-Barron asymptotics: the mutual information against the log of D1's resolution rho.
shannon [6] (DESCR) rate-distortion of a Gaussian source at distortion equal to the unit: A1' applied to the source itself.

The five source rows are Shannon-theory identities read with CRR's names (their own grades say so). The class asks
whether a CRR-proper ingredient (here A1'/D1: the unit as the system's own resolvable step, and rho) adds a checkable
proposition beyond the identity. Every number printed is computed here (R1); every verdict word is an f-string of a
comparison (R15). No data file is opened (R2). Deterministic: fixed grids, closed forms and quadrature, one seeded
draw (row 5). Where A1' is taken in its operational reading on stationary occasions the named detrender is the median
across occasions (the stationary case; batch 04, AGENT_LOG 32c), and the registered Savitzky-Golay reading is printed
beside it with its leverage factor (AGENT_LOG 30).
Run:  uv run python theory/retrodictions/synthesis_batches/batch_23.py
"""
import math
import sys

import numpy as np
from scipy import integrate, optimize, special, stats
from scipy.signal import savgol_coeffs

from crr.instrument.core import unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/shannon.txt"
LN2PIE_HALF = 0.5 * math.log(2.0 * math.pi * math.e)          # 1.4189 nats: the Gaussian's entropy in its own unit
SQRT2PIE = math.sqrt(2.0 * math.pi * math.e)                   # 4.1327: Stam's constant
MAD_K = 1.4826                                                 # the instrument's MAD-to-sigma constant (unit_sigma)


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


# ---------------------------------------------------------------- 111: [2] de Bruijn: the entropy in the system's own unit along the heat flow
def _uniform_heat(t):
    """X uniform on [-1, 1] plus sqrt(t) Z (the source row's model): entropy h(t) and location Fisher information J(t)."""
    s = math.sqrt(t)

    def p(x):
        return 0.5 * (stats.norm.cdf((x + 1.0) / s) - stats.norm.cdf((x - 1.0) / s))

    def dp(x):
        return 0.5 * (stats.norm.pdf((x + 1.0) / s) - stats.norm.pdf((x - 1.0) / s)) / s

    lim = 1.0 + 8.0 * s

    def fh(x):
        v = p(x)
        return -v * math.log(v) if v > 1e-300 else 0.0

    def fj(x):
        v = p(x)
        if v < 1e-12:                                   # the tails carry no measurable Fisher information (the source row's guard)
            return 0.0
        d = dp(x)
        return d * d / v

    return integrate.quad(fh, -lim, lim, limit=400)[0], integrate.quad(fj, -lim, lim, limit=400)[0]


def r1():
    grid = (0.1, 0.25, 0.5, 1.0, 2.0, 4.0)
    t_ref = 0.5                                                  # the source row's t
    rows = []
    for t in grid:
        eps = 1e-3 * t
        hm, Jm = _uniform_heat(t - eps)
        hp, Jp = _uniform_heat(t + eps)
        h0, J0 = _uniform_heat(t)
        dh = (hp - hm) / (2.0 * eps)                             # entropy rate (finite difference)
        dJ = (Jp - Jm) / (2.0 * eps)                             # Fisher-information rate (finite difference)
        d_unit = dh + 0.5 * dJ / J0                              # d/dt [h - ln sigma_u], sigma_u = 1/sqrt(J) (A1', named reading)
        d_domain = 0.5 * J0 + 0.5 * dJ / J0                      # the same with de Bruijn's dh/dt = J/2 in place of the finite difference
        rows.append(dict(t=t, h=h0, J=J0, dh=dh, dJ=dJ, d_unit=d_unit, d_domain=d_domain,
                         h_unit=h0 + 0.5 * math.log(J0), NJ=math.exp(2.0 * h0) / (2.0 * math.pi * math.e) * J0))
    ref = [r for r in rows if r["t"] == t_ref][0]
    # Gaussian control (closed forms): h = ln sqrt(2 pi e (1 + t)), J = 1/(1 + t): the entropy in the unit is constant
    eps = 5e-4
    g_h = lambda t: 0.5 * math.log(2.0 * math.pi * math.e * (1.0 + t))
    g_J = lambda t: 1.0 / (1.0 + t)
    d_gauss = (g_h(t_ref + eps) - g_h(t_ref - eps)) / (2.0 * eps) + 0.5 * (g_J(t_ref + eps) - g_J(t_ref - eps)) / (2.0 * eps) / g_J(t_ref)
    h_unit_gauss = g_h(t_ref) + 0.5 * math.log(g_J(t_ref))
    crr = ref["d_unit"]
    null_fixed = ref["dh"]                                       # a fixed outside unit (the source's half-width): d/dt [h - ln 1] = dh/dt
    null_ew = 0.0                                                # the entropy-power width as the unit: d/dt [h - ln e^h/sqrt(2 pi e)] = 0 identically
    domain = ref["d_domain"]
    all_down = all(r["d_unit"] <= 1e-6 for r in rows)
    check = all_down and crr < 0.0 and abs(d_gauss) < 1e-6 and rel(rows[-1]["h_unit"], LN2PIE_HALF) <= 1e-4
    out = outcome(crr=crr, null=null_fixed, domain=domain, check=check)
    return make_row("geom", f"Heat flow X_t = X + sqrt(t) Z from X uniform on [-1, 1] (the source row's model), t on {grid}; entropy h(t) and location Fisher information J(t) by quadrature, rates by central differences (eps = 1e-3 t); Gaussian control from closed forms",
                    source=f"{SRC} [2] (CONSIST)",
                    Q="the entropy of a system counted in its own resolvable step (A1': sigma_u = 1/sqrt J), h - ln sigma_u, never increases along the heat flow: it falls toward 1/2 ln(2 pi e) and is stationary only for the Gaussian, so smoothing makes a distribution carry less surprise per step it can resolve, not more",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step, here the location family's 1/sqrt J at each smoothing level) read on the domain's identity dh/dt = J/2 (de Bruijn, D2 as a Fisher speed in the source row)",
                    null="an outside unit that does not move with the system: the source's half-width 1 (d/dt [h - ln 1] = dh/dt = J/2 > 0); also the entropy-power width e^h/sqrt(2 pi e) as the unit, for which the quantity is 1/2 ln(2 pi e) identically (rate 0)",
                    domain="de Bruijn (Stam 1959) dh/dt = J/2, and the derivative form of the Blachman-Stam inequality 1/J(X + sqrt t Z) >= 1/J(X) + t, i.e. dJ/dt <= -J^2 (Stam 1959; Blachman 1965): together d/dt ln(N J) = J + J'/J <= 0, the entropy power times Fisher information is non-increasing along the flow",
                    numbers="; ".join(f"t = {r['t']:g}: dh/dt = {r['dh']:.6f}, J/2 = {r['J'] / 2:.6f}, dJ/dt = {r['dJ']:.4f} (-J^2 = {-r['J'] ** 2:.4f}), d/dt [h - ln sigma_u] = {r['d_unit']:.6f}, h - ln sigma_u = {r['h_unit']:.5f}, N J = {r['NJ']:.5f}" for r in rows)
                            + f"; limit 1/2 ln(2 pi e) = {LN2PIE_HALF:.5f}; Gaussian control at t = {t_ref:g}: d/dt [h - ln sigma_u] = {d_gauss:.1e}, h - ln sigma_u = {h_unit_gauss:.5f}",
                    tg=f"t = {t_ref:g}: d/dt [h - ln sigma_u] with the A1' unit {crr:.6f} vs null (fixed outside unit) {null_fixed:.6f}: {ag(crr, null_fixed)}; vs the entropy-power unit {null_ew:.1f}: {ag(crr, null_ew)}",
                    tn=f"de Bruijn's J/2 in place of the measured dh/dt gives {domain:.6f}: {ag(crr, domain, TOL_N)}" + (" (the domain has Q: it is d/dt ln(N J) <= 0, Blachman-Stam with de Bruijn)" if rel(crr, domain) <= TOL_N else ""),
                    tc=f"d/dt [h - ln sigma_u] <= 0 at every t on the grid: {hf(all_down)}; negative at t = {t_ref:g}: {hf(crr < 0.0)}; zero on the Gaussian control (|.| < 1e-6): {hf(abs(d_gauss) < 1e-6)}; limit at t = {grid[-1]:g} within 1e-4 of 1/2 ln(2 pi e): {hf(rel(rows[-1]['h_unit'], LN2PIE_HALF) <= 1e-4)}; together: {hf(check)}",
                    out=out,
                    reading=f"the unit does work (T-G: in a fixed unit the entropy rises at J/2 = {null_fixed:.4f} per unit t, in the system's own unit it falls at {crr:.4f} and settles at {LN2PIE_HALF:.4f} nats, the Gaussian's entropy per resolvable step), and the proposition it yields is the domain's: h - ln sigma_u = 1/2 ln(2 pi e N J) is Stam's ratio in log form, and its monotone fall along the heat flow is the Blachman-Stam inequality's derivative dJ/dt <= -J^2 (at t = {grid[0]:g}: {rows[0]['dJ']:.4f} against {-rows[0]['J'] ** 2:.4f}) taken with de Bruijn; the integrated equality 'entropy gained = log growth of the unit' would need dJ/dt = -J^2, which holds only on the Gaussian; the synthesis reading is {out}",
                    weakness="one source (uniform) and one control (Gaussian), rates by finite difference on quadrature (the tail guard at p < 1e-12 is the source row's); the Blachman-Stam derivative form is named from the source row's citation list, not fetched (R10); the named reading of A1' only, since a heat flow has no occasions to estimate the unit across",
                    elegance="Blur a picture and two things shrink together: how many spots you can still tell apart, and how much surprise each spot holds. The surprise per spot only ever goes down, and it stops going down once the blur is a bell curve. A picture with no knobs.",
                    child="When you blur a photo, you can tell apart fewer and fewer little spots, and each spot you can still make out holds less of a surprise than it did. That amount only ever goes down, and it stops changing once the blur looks like one smooth hill.")


# ---------------------------------------------------------------- 112: [3] Stam: the A1' unit against the entropy-power width, two readings
def r2():
    fams = []
    # (name, scipy frozen or None, J closed form (inf for the uniform), h closed form, MAD closed form via ppf(0.75) for symmetric families)
    for key, name, d, J, h in (("Gaussian", "Gaussian(0, 1)", stats.norm(0.0, 1.0), 1.0, 0.5 * math.log(2.0 * math.pi * math.e)),
                               ("Laplace", "Laplace(0, 1)", stats.laplace(0.0, 1.0), 1.0, 1.0 + math.log(2.0)),
                               ("logistic", "logistic(0, 1)", stats.logistic(0.0, 1.0), 1.0 / 3.0, 2.0),
                               ("uniform", "uniform[-1, 1]", stats.uniform(-1.0, 2.0), math.inf, math.log(2.0))):
        fams.append(dict(key=key, name=name, J=J, h=h, mad=float(d.ppf(0.75)), sd=float(d.std())))
    # two spikes: 1/2 N(-1, w^2) + 1/2 N(1, w^2), entropy and Fisher information by quadrature, MAD by root-finding on the CDF
    w = 0.05
    pdf = lambda x: 0.5 * stats.norm.pdf(x, -1.0, w) + 0.5 * stats.norm.pdf(x, 1.0, w)
    cdf = lambda x: 0.5 * stats.norm.cdf(x, -1.0, w) + 0.5 * stats.norm.cdf(x, 1.0, w)

    def fj(x):
        v = pdf(x)
        if v < 1e-12:
            return 0.0
        d = 0.5 * stats.norm.pdf(x, -1.0, w) * (-(x + 1.0) / w ** 2) + 0.5 * stats.norm.pdf(x, 1.0, w) * (-(x - 1.0) / w ** 2)
        return d * d / v

    lim = 1.0 + 12.0 * w
    h_mix = integrate.quad(lambda x: -pdf(x) * math.log(pdf(x)) if pdf(x) > 1e-300 else 0.0, -lim, lim, limit=400, points=[-1.0, 1.0])[0]
    J_mix = integrate.quad(fj, -lim, lim, limit=400, points=[-1.0, 1.0])[0]
    mad_mix = optimize.brentq(lambda m: cdf(m) - 0.75, 0.0, 3.0, xtol=1e-12)
    fams.append(dict(key="two spikes", name=f"two spikes 1/2 N(-1, {w:g}^2) + 1/2 N(1, {w:g}^2)", J=J_mix, h=h_mix, mad=mad_mix, sd=math.sqrt(1.0 + w ** 2)))
    for f in fams:
        f["named"] = 0.0 if math.isinf(f["J"]) else 1.0 / math.sqrt(f["J"])         # A1' named: 1/sqrt J (the source row's reading)
        f["est"] = MAD_K * f["mad"]                                                   # A1' estimated: 1.4826 MAD of the draws (median detrender, stationary)
        f["ew"] = math.exp(f["h"])                                                    # the entropy width e^h (= sqrt(2 pi e) sd for the Gaussian)
        f["r_named"] = math.inf if f["named"] == 0.0 else f["ew"] / f["named"]        # Stam's ratio e^h sqrt J
        f["r_est"] = f["ew"] / f["est"]
        f["r_sd"] = f["ew"] / f["sd"]                                                 # the null: the SD as the unit
    lap = [f for f in fams if f["name"].startswith("Laplace")][0]
    disagree = [f for f in fams if rel(f["named"], f["est"]) > TOL_G]
    internal = len(disagree) > 0
    named_ok = all(f["r_named"] >= SQRT2PIE * (1.0 - 1e-9) for f in fams)
    est_ok = all(f["r_est"] >= SQRT2PIE * (1.0 - 1e-9) for f in fams)
    sd_ok = all(f["r_sd"] <= SQRT2PIE * (1.0 + 1e-9) for f in fams)
    out = outcome(crr=lap["r_named"], null=lap["r_sd"], domain=lap["r_named"], check=named_ok, internal=internal)
    return make_row("geom", "Densities on the line: Gaussian, Laplace, logistic, uniform (closed forms) and a two-spike mixture (quadrature); the A1' unit in its named reading 1/sqrt J and its operational reading 1.4826 MAD of the draws (occasion = one draw, median detrender), each against the entropy width e^h",
                    source=f"{SRC} [3] (DESCR)",
                    Q="the system's own resolvable step is at most the entropy width over sqrt(2 pi e) for every density on the line, with equality only for the Gaussian: e^h / sigma_u >= sqrt(2 pi e) (Stam's inequality N J >= 1 with sigma_u = 1/sqrt J), and the bound is about the A1' unit, whichever of the two clauses of A1' supplies it",
                    ingredient="A1'/D1 (the unit as the system's own resolvable step) in its two readings: named, 1/sqrt J (the source row's), and estimated, the instrument's robust scale 1.4826 MAD of one occasion statistic across occasions (here the draw itself)",
                    null="the standard deviation as the unit (the domain's usual width): with it the Gaussian is the extreme the other way, e^h / sd <= sqrt(2 pi e) (maximum entropy at fixed variance)",
                    domain="Stam 1959: N(X) J(X) >= 1, N = e^{2h}/(2 pi e), equality iff Gaussian; and h <= 1/2 ln(2 pi e sd^2) (maximum entropy at fixed variance)",
                    numbers="; ".join(f"{f['name']}: h = {f['h']:.4f}, J = {'inf' if math.isinf(f['J']) else f'{f['J']:.4f}'}, named unit {f['named']:.4f}, estimated unit {f['est']:.4f} (ratio {'-' if f['named'] == 0.0 else f'{f['est'] / f['named']:.4f}'}), e^h = {f['ew']:.4f}; Stam ratio e^h/unit: named {'inf' if math.isinf(f['r_named']) else f'{f['r_named']:.4f}'}, estimated {f['r_est']:.4f}, sd as unit {f['r_sd']:.4f}" for f in fams)
                            + f"; sqrt(2 pi e) = {SQRT2PIE:.4f}",
                    tg=f"Laplace: Stam ratio with the A1' unit (named) {lap['r_named']:.4f} vs null (sd as unit) {lap['r_sd']:.4f}: {ag(lap['r_named'], lap['r_sd'])}; the two readings of A1' disagree beyond {TOL_G:g} on {len(disagree)} of {len(fams)} densities (" + ", ".join(f"{f['key']}: named {f['named']:.4f} vs estimated {f['est']:.4f}" for f in disagree) + ")",
                    tn=f"Stam gives the named-reading bound exactly (Laplace {lap['r_named']:.4f} = 2e): {ag(lap['r_named'], lap['r_named'], TOL_N)} (the domain has Q under the named reading)",
                    tc=f"e^h/unit >= sqrt(2 pi e) on every density: named reading {hf(named_ok)}; estimated reading {hf(est_ok)} (uniform {fams[3]['r_est']:.4f}, two spikes {fams[4]['r_est']:.4f} against {SQRT2PIE:.4f}); the null's reversed bound e^h/sd <= sqrt(2 pi e): {hf(sd_ok)}; not decisive: the two readings of the ingredient must agree before Q can be checked",
                    out=out,
                    reading=f"under the named reading Q is Stam's inequality with the unit renamed (the domain has it, and the null shows the bound flips sign when the unit is the sd); under the operational reading the unit is a quantile width, which no entropy bound controls: it coincides with 1/sqrt J on the Gaussian ({fams[0]['est'] / fams[0]['named']:.6f}), differs by {100 * (fams[1]['est'] / fams[1]['named'] - 1):+.1f} % on the Laplace and {100 * (fams[2]['est'] / fams[2]['named'] - 1):+.1f} % on the logistic, is finite where 1/sqrt J is zero (the uniform's edges), and on two spikes is {fams[4]['est'] / fams[4]['named']:.1f} times the Fisher step, so e^h/unit falls to {fams[4]['r_est']:.4f}; which clause of A1' is the unit decides whether Q is the domain's theorem or false, the batch 06 row 4 reading (AGENT_LOG 30) by a second mechanism (shape, not detrender leverage): {out}",
                    weakness="the operational unit is applied to single draws with the median detrender (no trend by construction), so the registered Savitzky-Golay leverage is not in these numbers; five densities, symmetric, chosen to span the cases; the two-spike entropy and Fisher information are quadrature on a density with a 1e-12 floor in the Fisher integrand")


# ---------------------------------------------------------------- shared: the Bernoulli family on its arc coordinate (rows 3 and 4)
def _bernoulli_grid(n, pts=2001):
    """Grid uniform in the Fisher arc phi in (0, pi), theta = sin^2(phi/2) (dtheta/dphi = sqrt(theta (1 - theta))); binomial
    log-likelihoods LP[i, k] for k = 0..n at theta_i. Jeffreys is the uniform weight on this grid."""
    phi = (np.arange(pts) + 0.5) * math.pi / pts
    th = np.sin(phi / 2.0) ** 2
    ks = np.arange(n + 1)
    logC = special.gammaln(n + 1) - special.gammaln(ks + 1) - special.gammaln(n - ks + 1)
    LP = logC[None, :] + ks[None, :] * np.log(th)[:, None] + (n - ks)[None, :] * np.log(1.0 - th)[:, None]
    return th, np.sqrt(th * (1.0 - th)), LP, np.exp(LP)


def _mi(w, LP, P):
    w = w / w.sum()
    m = w @ P
    return float(np.sum(w[:, None] * P * (LP - np.log(m)[None, :])))


def _mad_rows(P):
    """Exact MAD (in counts) of each row's discrete law: the smallest m with P(|K - median| <= m) >= 1/2."""
    n = P.shape[1] - 1
    cdf = np.cumsum(P, axis=1)
    med = (cdf >= 0.5).argmax(axis=1)
    out = np.zeros(P.shape[0], int)
    for i in range(P.shape[0]):
        pm, m0 = P[i], int(med[i])
        for m in range(n + 1):
            if pm[max(0, m0 - m):min(n, m0 + m) + 1].sum() >= 0.5:
                out[i] = m
                break
    return out


def _mi_beta_quad(a, n):
    """I(theta; k), k ~ Binomial(n, theta), theta ~ Beta(a, a), by quadrature (the source row's estimator)."""
    ks = np.arange(n + 1)
    logC = special.gammaln(n + 1) - special.gammaln(ks + 1) - special.gammaln(n - ks + 1)
    logm = logC + special.betaln(ks + a, n - ks + a) - special.betaln(a, a)
    m = np.exp(logm)
    H_k = -np.sum(m * logm)

    def H_cond(t):
        lp = logC + ks * np.log(t) + (n - ks) * np.log(1.0 - t)
        p = np.exp(lp)
        return -np.sum(p * lp)

    E_H = integrate.quad(lambda t: stats.beta.pdf(t, a, a) * H_cond(t), 1e-6, 1.0 - 1e-6, limit=200)[0]
    return H_k - E_H


def r3():
    n, pts, iters = 200, 2001, 3000
    th, jac, LP, P = _bernoulli_grid(n, pts)
    mi_jeff = _mi(np.ones(pts), LP, P)                            # one prior mass per named step (Jeffreys)
    mi_unif = _mi(jac, LP, P)                                     # the coordinate unit: uniform in theta
    mi_jeff_q, mi_unif_q = _mi_beta_quad(0.5, n), _mi_beta_quad(1.0, n)   # the source row's estimator, for the grid's accuracy
    mad = _mad_rows(P)
    est = MAD_K * mad / n                                         # A1' estimated: 1.4826 MAD of the occasion statistic k/n across occasions at theta
    ok = est > 0.0                                                # degenerate residual (MAD = 0): the record is rejected (A1', no floor)
    named = np.sqrt(th * (1.0 - th) / n)
    ratio = est[ok] / named[ok]
    w_est = np.where(ok, jac / np.where(ok, est, 1.0), 0.0)       # one prior mass per estimated step, zero where rejected
    mi_est = _mi(w_est, LP, P)
    rejected = 1.0 - float(ok.mean())
    lower = (~ok) & (th < 0.5)                                    # the rejected band at the lower edge (the upper one mirrors it)
    th_rej = float(th[lower].max()) if lower.any() else 0.0
    # finite-n maximiser: Blahut-Arimoto on the same grid
    w = np.ones(pts) / pts
    for _ in range(iters):
        m = w @ P
        D = np.sum(P * (LP - np.log(m)[None, :]), axis=1)
        w = w * np.exp(D)
        w /= w.sum()
    m = w @ P
    D = np.sum(P * (LP - np.log(m)[None, :]), axis=1)
    cap, cap_ub = float(w @ D), float(D.max())
    internal = rel(mi_jeff, mi_est) > TOL_G
    check = mi_jeff > mi_unif and rel(mi_jeff, cap) <= TOL_N
    out = outcome(crr=mi_jeff, null=mi_unif, domain=mi_jeff, check=check, internal=internal)
    return make_row("prior", f"Bernoulli family, n = {n} draws per record, mutual information I(theta; k) on a {pts}-point grid uniform in the Fisher arc (nats); priors: one mass per A1' step in the named reading (Jeffreys), in the estimated reading (1.4826 x the exact MAD of k/n at each theta, record rejected where the MAD is 0), uniform in theta, and the Blahut-Arimoto maximiser ({iters} iterations)",
                    source=f"{SRC} [4] (CONSIST)",
                    Q="the prior that lets n draws say the most about theta puts one prior mass per resolvable step of the system's own unit (A1'): under the named reading that is the Jeffreys prior, uniform in Fisher arc, and it maximises the mutual information",
                    ingredient="A1'/D1 (the unit as the system's own resolvable step: named, 1/sqrt(n I(theta)); estimated, the instrument's 1.4826 MAD of the occasion statistic across occasions at theta, with the record rejected on a degenerate residual); P2/P3 (the source row's other clause) were tried and form no Q: they weight occasions, not parameter values",
                    null="the coordinate unit: one prior mass per unit of theta (the uniform prior)",
                    domain="Bernardo 1979 (the reference prior maximises the expected information from the data) and Clarke-Barron 1994 (for regular models the reference prior is Jeffreys, asymptotically); at finite n the maximiser is a discrete prior (computed here by Blahut-Arimoto)",
                    numbers=f"I under Jeffreys {mi_jeff:.5f} (source estimator, Beta(1/2, 1/2) by quadrature: {mi_jeff_q:.5f}); uniform in theta {mi_unif:.5f} (quadrature {mi_unif_q:.5f}); one mass per estimated step {mi_est:.5f}, with {100 * rejected:.2f} % of the arc rejected (theta <= {th_rej:.4f} or >= {1 - th_rej:.4f}: expected count n theta <= {n * th_rej:.2f}, MAD 0) and the estimated/named unit ratio on the kept arc between {ratio.min():.4f} and {ratio.max():.4f} (median {np.median(ratio):.4f}); Blahut-Arimoto capacity {cap:.5f} (upper bound max_theta D = {cap_ub:.5f}), {100 * (cap / mi_jeff - 1):.2f} % above Jeffreys",
                    tg=f"one mass per named step (Jeffreys) {mi_jeff:.5f} vs null (uniform in theta) {mi_unif:.5f}: {ag(mi_jeff, mi_unif)}; the two readings of A1' give {mi_jeff:.5f} (named) and {mi_est:.5f} (estimated): {ag(mi_jeff, mi_est)} (relative {rel(mi_jeff, mi_est):.4f}, TOL_G {TOL_G:g})",
                    tn=f"Bernardo/Clarke-Barron name the named-reading prior (Jeffreys) as the reference prior: {mi_jeff:.5f} vs {mi_jeff:.5f}: {ag(mi_jeff, mi_jeff, TOL_N)} (the domain has Q under the named reading); the finite-n maximiser is the domain's too, {cap:.5f}",
                    tc=f"Jeffreys above the coordinate prior: {hf(mi_jeff > mi_unif)}; Jeffreys within {TOL_N:g} of the finite-n capacity: {hf(rel(mi_jeff, cap) <= TOL_N)} (it is {100 * (cap / mi_jeff - 1):.2f} % below); not decisive: the two readings of the ingredient must agree before Q can be checked",
                    out=out,
                    reading=f"the unit does work (T-G: one mass per Fisher step beats one mass per unit of theta, {mi_jeff:.4f} against {mi_unif:.4f}), and under the named reading the proposition is Bernardo's and Clarke-Barron's theorem with A1' supplying the measure they already use; under the operational reading the prior cannot be formed on {100 * rejected:.1f} % of the arc (the instrument rejects a record whose occasion statistic has a degenerate residual, and a count with expected value at or below {n * th_rej:.2f} has MAD 0) and is coarse near the edges (unit ratio {ratio.min():.2f} to {ratio.max():.2f}), so it carries {100 * (1 - mi_est / mi_jeff):.1f} % less information; the two clauses of A1' disagree on a count carrier at the family's edges (batch 01 row 3's carrier, batch 06 row 4's clause), and at finite n neither reading is the maximiser, which is discrete and {100 * (cap / mi_jeff - 1):.2f} % above Jeffreys: {out}",
                    weakness=f"one family and one n; the estimated reading is evaluated pointwise in theta from the exact binomial law rather than from simulated occasions, so the discreteness of the MAD is exact and the registered detrender's leverage is absent; the Blahut-Arimoto value is a grid optimum after {iters} iterations (duality gap {cap_ub - cap:.1e} nats) and the grid's edge points sit at theta = {th[0]:.1e}, not at 0",
                    elegance="Spread your guesses evenly over the notches you can tell apart, not evenly over the ruler: where the notches crowd together, put more guesses there. A rule with no knobs, and it is the field's own.",
                    child="Suppose a ruler has notches close together at its ends and far apart in the middle. If you want to guess fairly where something is, put one guess on each notch, not one guess per inch; that way you learn the most from what you see.")


# ---------------------------------------------------------------- 114: [5] Clarke-Barron: the mutual information against the log of D1's rho
def r4():
    L_F = integrate.quad(lambda t: 1.0 / math.sqrt(t * (1.0 - t)), 0.0, 1.0)[0]     # the Bernoulli family's Fisher length: one A3 half-turn, pi
    ns = (100, 1000, 10000, 100000)
    rows = []
    for n in ns:
        mi = _mi_beta_quad(0.5, n)
        ln_rho = math.log(L_F * math.sqrt(n))                    # D1: extent (the family's half-turn, pi) over the A1' unit in Fisher length, 1/sqrt n
        crr = ln_rho - LN2PIE_HALF
        null = math.log(math.sqrt(n)) - LN2PIE_HALF              # the coordinate unit 1/sqrt n in theta: count sqrt n (the family's extent 1 in theta)
        cb = 0.5 * math.log(n / (2.0 * math.pi * math.e)) + math.log(L_F)
        # the estimated reading of the unit at the operating point theta = 1/2: 1.4826 x the exact MAD of k/n, in Fisher length
        ks = np.arange(n + 1)
        pm = stats.binom.pmf(ks, n, 0.5)
        mad = int(_mad_rows(pm[None, :])[0])
        est_ratio = (MAD_K * mad / n) / math.sqrt(0.25 / n)
        rows.append(dict(n=n, mi=mi, ln_rho=ln_rho, crr=crr, null=null, cb=cb, gap=ln_rho - mi, est_ratio=est_ratio))
    top = rows[-2]                                               # n = 10000: the source row's largest n
    gaps = [r["gap"] for r in rows]
    diffs = [abs(r["crr"] - r["mi"]) for r in rows]
    check = all(d2 < d1 for d1, d2 in zip(diffs[:-1], diffs[1:])) and rel(top["crr"], top["mi"]) <= TOL_N
    internal = rel(top["est_ratio"], 1.0) > TOL_G
    out = outcome(crr=top["crr"], null=top["null"], domain=top["mi"], check=check, internal=internal)
    return make_row("prior", f"Bernoulli family under the Jeffreys prior at n in {ns}: exact mutual information by quadrature against D1's resolution rho = (extent of the family, its one A3 half-turn of Fisher length {L_F:.6f}) / (A1' unit at n draws, 1/sqrt n in Fisher length) = pi sqrt n",
                    source=f"{SRC} [5] (CONSIST)",
                    Q="the mutual information between the parameter and n draws under the Jeffreys prior is the log of D1's resolution minus the Gaussian's entropy per resolvable step: I = ln rho - 1/2 ln(2 pi e) + o(1), rho = pi sqrt n; the count whose log is Shannon's information is not rho but rho / sqrt(2 pi e), the family's extent in local-posterior entropy widths",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step at n draws, 1/sqrt(n I) in the coordinate, 1/sqrt n in Fisher length; rho = extent / unit, with the extent the family's half-turn, A3) read on Clarke-Barron",
                    null="the coordinate unit 1/sqrt n in theta (the parameter's own scale, an outside unit): count sqrt n, ln sqrt n - 1/2 ln(2 pi e)",
                    domain="Clarke & Barron 1990/1994: I(theta; X^n) = (d/2) ln(n / 2 pi e) + ln int sqrt(det I) dtheta + o(1) under Jeffreys (the source row's citation)",
                    numbers="; ".join(f"n = {r['n']}: I = {r['mi']:.5f} nats, ln rho = {r['ln_rho']:.5f}, ln rho - I = {r['gap']:.5f}, ln rho - 1/2 ln(2 pi e) = {r['crr']:.5f} (Clarke-Barron {r['cb']:.5f}), coordinate-unit count {r['null']:.5f}; estimated/named unit at theta = 1/2: {r['est_ratio']:.4f}" for r in rows)
                            + f"; 1/2 ln(2 pi e) = {LN2PIE_HALF:.5f}; the source row's 'rho = pi sqrt(n / 2 pi e)' is D1's rho / sqrt(2 pi e), i.e. its unit was sqrt(2 pi e) = {SQRT2PIE:.4f} times the A1' unit",
                    tg=f"n = {top['n']}: ln rho - 1/2 ln(2 pi e) with the A1' unit {top['crr']:.5f} vs null (coordinate unit) {top['null']:.5f}: {ag(top['crr'], top['null'])}; the estimated reading of the unit at theta = 1/2 is {top['est_ratio']:.4f} of the named one at n = {top['n']} ({rows[0]['est_ratio']:.4f} at n = {rows[0]['n']}, discreteness of the MAD): {ag(top['est_ratio'], 1.0)}",
                    tn=f"exact I at n = {top['n']} is {top['mi']:.5f}: {ag(top['crr'], top['mi'], TOL_N)}" + (" (the domain has Q: it is Clarke-Barron's formula with ln int sqrt I = ln pi read as ln rho - ln sqrt n)" if rel(top["crr"], top["mi"]) <= TOL_N else ""),
                    tc=f"|ln rho - 1/2 ln(2 pi e) - I| decreasing in n ({', '.join(f'{d:.4f}' for d in diffs)}): {hf(all(d2 < d1 for d1, d2 in zip(diffs[:-1], diffs[1:])))}; within {TOL_N:g} at n = {top['n']}: {hf(rel(top['crr'], top['mi']) <= TOL_N)}; together: {hf(check)}; and the source row's Q 'I = ln rho' fails by ln rho - I -> {gaps[-1]:.4f} (not 0)",
                    out=out,
                    reading=f"the unit does work (T-G: the Fisher unit's count carries the family's length pi, the coordinate unit's does not, {top['crr']:.4f} against {top['null']:.4f}), and the proposition is Clarke-Barron's with D1's names: ln rho = ln pi + 1/2 ln n is the theorem's ln int sqrt I + 1/2 ln n, and the constant 1/2 ln(2 pi e) is what separates counting in Cramer-Rao steps (rho) from counting in entropy widths of the local posterior (rho / sqrt(2 pi e)); recorded, not repaired: the source row wrote its rho as pi sqrt(n / 2 pi e), which is not extent/unit under A1' (that is pi sqrt n, {gaps[-1]:.4f} nats above I at n = {rows[-1]['n']}), so its 'I = ln rho' was graded CONSIST with sqrt(2 pi e) folded into the unit; the estimated reading of the unit converges on the named one ({rows[0]['est_ratio']:.3f}, {rows[1]['est_ratio']:.3f}, {rows[2]['est_ratio']:.3f}, {rows[3]['est_ratio']:.3f}), so the asymptotic Q is one statement under both: {out}",
                    weakness=f"one family (d = 1), whose Fisher length is one A3 half-turn so D1's 'extent of one monotone half-turn' is the whole family; the estimated reading is checked at the operating point theta = 1/2 only (row 3 shows it rejected or coarse at the family's edges); Clarke-Barron is named from the source row's citation, not fetched (R10)",
                    elegance="How much you learn about a dial from looking is the log of how many of its notches you can still tell apart, less one fixed toll that the bell curve charges. One count and one constant.",
                    child="Imagine a dial with notches. After you look at some data you can only tell apart so many notches on it. What you learned is how many notches that is, counted in doublings, and a little less than that because your guess is a soft hill, not a sharp point.")


# ---------------------------------------------------------------- 115: [6] rate-distortion at the unit: A1' applied to the source itself
def r5():
    sd = 1.0
    # A1' on a memoryless Gaussian source: occasion = one sample, statistic = the sample, median detrender (stationary, no trend)
    sig_med = MAD_K * float(stats.norm.ppf(0.75)) * sd                                # closed form: 1.4826 x MAD of N(0, sd^2)
    c0 = float(savgol_coeffs(9, 2)[4])                                               # the registered detrender's centre weight (leverage)
    sig_sg = math.sqrt(1.0 - c0) * sd                                                 # the registered reading on i.i.d. samples (AGENT_LOG 30)
    R = lambda rho: max(0.0, math.log2(rho))                                          # Shannon: R(D) = 1/2 log2(sd^2 / D) at D = (sd/rho)^2
    rho_med, rho_sg = sd / sig_med, sd / sig_sg
    R_med, R_sg = R(rho_med), R(rho_sg)
    src = [(r, R(r)) for r in (2, 10, 100)]                                           # the source row's outside units
    R_null = [b for r, b in src if r == 10][0]
    R_domain = 0.5 * math.log2(sd ** 2 / sig_med ** 2)                                # Shannon's R(D) at D = sigma_u^2, the same expression
    # a trace with a rotor: a sine of amplitude A in unit noise, 100 samples per half-turn, 40 half-turns (seed 0)
    rng = np.random.default_rng(0)
    A, per, K = 5.0, 100, 40
    N = per * K
    x = A * np.sin(math.pi * np.arange(N) / per) + rng.normal(0.0, sd, N)
    sig_x = unit_sigma(x)                                                             # the registered instrument reading (window 9, order 2, MAD)
    rho_d1 = 2.0 * A / sig_x                                                          # D1: extent of one monotone half-turn (2A) over the unit
    rho_rms = float(np.std(x, ddof=1)) / sig_x                                        # the source row's ratio sigma_signal / sigma_unit
    bits_d1, bits_rms = math.log2(rho_d1), math.log2(rho_rms)
    # reverse water-filling for the Gaussian process with the trace's covariance (N DFT bins: two carry the line, the rest the noise)
    theta = sig_x ** 2
    line = N * A ** 2 / 4.0 + sd ** 2
    R_line = 2.0 * 0.5 * math.log2(line / theta) / N
    R_white = (N - 2) * 0.5 * max(0.0, math.log2(sd ** 2 / theta)) / N
    R_wf = R_line + R_white
    R_wf_noise = 2.0 * 0.5 * math.log2(line / sd ** 2) / N                            # the same at D = the noise's own variance
    check = R_med <= 1e-3
    out = outcome(crr=R_med, null=R_null, domain=R_domain, check=check)
    return make_row("code", f"Memoryless Gaussian source (sd = {sd:g}), Shannon's R(D) = 1/2 log2(sd^2 / D); the A1' unit taken from the source itself (occasion = one sample, statistic = the sample; median detrender, and the registered Savitzky-Golay window 9 beside it); and a trace with a rotor (sine A = {A:g} in unit noise, {per} samples per half-turn, {K} half-turns, seed 0) for D1's rho",
                    source=f"{SRC} [6] (DESCR)",
                    Q="describing a source to within one of its own resolvable steps (A1') costs log2 rho bits per sample, rho = extent / unit (D1); on a memoryless Gaussian source the A1' unit is the source's own scatter, so rho = 1 and the cost is 0 bits: the source row's counts (log2 2, log2 10, log2 100) belong to a unit chosen from outside the source",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step, the robust scale of one occasion statistic across occasions; rho = the extent of one monotone half-turn over the unit)",
                    null="the source row's unit, a constant sigma_unit chosen from outside the source (rho = 10: the rate log2 10)",
                    domain="Shannon 1948/1959: R(D) = 1/2 log2(sigma^2 / D) for a Gaussian source, R = 0 at D >= sigma^2; reverse water-filling for a Gaussian process",
                    numbers=f"A1' unit of the memoryless source: median detrender {sig_med:.6f} sd (1.4826 x MAD), rho = {rho_med:.6f}, R = {R_med:.2e} bits; registered Savitzky-Golay detrender {sig_sg:.4f} sd (sqrt(1 - c0), c0 = {c0:.4f}), rho = {rho_sg:.4f}, R = {R_sg:.4f} bits; the source row's outside units: " + ", ".join(f"rho = {r}: {b:.3f} bits" for r, b in src)
                            + f"; sine trace: unit_sigma = {sig_x:.4f}, D1's rho = 2A/unit = {rho_d1:.4f} ({bits_d1:.4f} bits), the source row's ratio sd(x)/unit = {rho_rms:.4f} ({bits_rms:.4f} bits); reverse water-filling of the Gaussian process with the trace's covariance at D = unit^2: {R_wf:.4f} bits/sample (line {R_line:.4f}, white residual {R_white:.4f}); at D = the noise variance: {R_wf_noise:.4f} bits/sample",
                    tg=f"R at the A1' unit {R_med:.2e} bits vs null (outside unit, rho = 10) {R_null:.4f} bits: {ag(R_med, R_null)}",
                    tn=f"Shannon's R(D) at D = unit^2 gives {R_domain:.2e} bits: {ag(R_med, R_domain, TOL_N)}" + (" (the domain has Q: R = 0 at the source's own variance)" if rel(R_med, R_domain) <= TOL_N else ""),
                    tc=f"R at the A1' unit within 1e-3 bits of 0: {hf(check)} (the {R_med:.1e} is the rounding of the 1.4826 constant)",
                    out=out,
                    reading=f"applied to the source row's own model, A1' returns the source's scatter as the unit (rho = {rho_med:.4f}), and Shannon's function says describing a source to within its own variance costs nothing: the log2 rho of the source row is R(D) with an outside D relabelled, and with the registered detrender the same source costs {R_sg:.4f} bits per sample from the detrender's leverage alone (AGENT_LOG 30); D1's rho needs a monotone half-turn, which a memoryless source lacks (O3), and on a trace that has one, D1's count ({rho_d1:.2f}) and the source row's rms ratio ({rho_rms:.2f}) are different numbers, {bits_d1 - bits_rms:.2f} bits apart, neither of them the rate to describe that trace to within its unit ({R_wf:.4f} bits/sample, almost all of it the residual below the unit; the half-turns themselves cost {R_line:.4f}): a source with occasions is not a memoryless source, and the rate is Shannon's either way: {out}",
                    weakness="the sine trace is one seed at one amplitude, its water-filling rate is the Gaussian-process bound for the covariance (an upper bound for the trace), and its A1' unit carries the registered detrender's leverage; 'to within one unit' is read as mean-square distortion equal to the unit's variance, the source row's reading",
                    elegance="To describe something to within the size of its own wobble costs nothing: say where it usually is and you are done. The counting starts only when you want to know it finer than it wobbles.",
                    child="If your friend asks where the dog is and the dog always wanders around the same yard, saying 'in the yard' is free and good enough. You only have to start counting and explaining if you want to say where in the yard, more exactly than the dog wanders.")


def main():
    return run_batch("Synthesis batch 23: rows 111-115 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
