"""Synthesis batch 24: rows 116-120 of QUEUE.md (prompt-log entry 61).
shannon [7] (DESCR) the data-processing inequality on a Markov chain: the past adds nothing beyond the present.
shannon [9] (CONSIST) information length of a relaxing Gaussian: D2 on the path of distributions.
shannon [10] (DESCR) binary symmetric channel: capacity against Fisher information across the crossover.
shannon [11] (DESCR) natural time as the time-change under which a Poisson process has unit entropy per event.
shannon [12] (DESCR) P2's surplus weights as the Shannon-entropy maximiser under a mean-surplus constraint.

All five source rows are in theory/retrodictions/shannon.txt; their models are re-implemented here (nothing imported
from the battery script). Every number printed is computed here (R1); every verdict word is an f-string of a
comparison (R15). No data file is opened (R2). Deterministic: one fixed seed (the source's), fixed grids, quadrature.
Run:  uv run python theory/retrodictions/synthesis_batches/batch_24.py
"""
import math
import sys

import numpy as np
from scipy import integrate, special, stats
from scipy.optimize import brentq
from scipy.stats import spearmanr

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "theory/retrodictions/shannon.txt"


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


def _H(p):
    """Shannon entropy (nats) of a probability array of any shape."""
    p = np.asarray(p, float).ravel(); p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def _r2(y, X):
    """R^2 of y on a linear fit in the columns of X (with intercept)."""
    X = np.atleast_2d(np.asarray(X, float)); X = X.T if X.shape[0] < X.shape[1] else X
    A = np.c_[X, np.ones(len(y))]; c, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ c
    return float(1.0 - res.var() / y.var())


# ---------------------------------------------------------------- 116: [7] data-processing inequality on a Markov chain
def r1():
    rng = np.random.default_rng(1); K = 4                                     # the source's chain, seed 1
    T1 = rng.dirichlet(np.ones(K) * 0.7, K); T2 = rng.dirichlet(np.ones(K) * 0.7, K); px = rng.dirichlet(np.ones(K))
    pxyz = px[:, None, None] * T1[:, :, None] * T2[None, :, :]
    pxy, pyz, pxz = pxyz.sum(2), pxyz.sum(0), pxyz.sum(1); py, pz = pxy.sum(0), pxz.sum(0)
    Ixy = _H(px) + _H(py) - _H(pxy); Ixz = _H(px) + _H(pz) - _H(pxz)         # the source's two numbers
    I_zy = _H(pz) + _H(py) - _H(pyz)                                           # endpoint: forecast Z from the present Y
    I_zxy = _H(pz) + _H(pxy) - _H(pxyz)                                        # path: forecast Z from the settled history (X, Y)
    cond = I_zxy - I_zy                                                        # I(Z; X | Y), the surplus of the path over the endpoint
    # the same chain seen through a symmetric observation channel with error eps (the observed state is not the full state)
    obs = []
    for eps in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.75):
        W = np.full((K, K), eps / (K - 1)); np.fill_diagonal(W, 1.0 - eps)
        q = np.einsum("xyz,xa,yb,zc->abc", pxyz, W, W, W)
        qab, qbc = q.sum(2), q.sum(0); qb, qc = qab.sum(0), qbc.sum(0)
        obs.append((eps, _H(qc) + _H(qb) - _H(qbc), _H(qc) + _H(qab) - _H(q)))
    cond_obs = {e: c2 - c1 for e, c1, c2 in obs}; e_max = max(cond_obs, key=cond_obs.get)
    check = abs(cond) < 1e-9 and Ixz <= Ixy and cond_obs[0.2] > 1e-4
    out = outcome(crr=I_zxy, null=I_zy, domain=I_zy, check=check)
    return make_row("code", f"A three-step Markov chain X -> Y -> Z on {K} states (the source's chain: Dirichlet(0.7) transition rows, Dirichlet(1) start, seed 1), forecasting Z from the settled history against the present, and the same chain seen through a symmetric observation channel with error eps",
                    source=f"{SRC} [7] (DESCR)",
                    Q="H-T1's path term on a Markov carrier is the conditional mutual information I(past; future | present): forecasting Z from the settled path (X, Y) carries no more information than forecasting it from the present Y, I(Z; X, Y) = I(Z; Y), and a surplus of the path over the endpoint appears only when the observed state is not the full state (a lossy observation of the chain)",
                    ingredient="D6/H-T1 (path against endpoint) read in Shannon's units: the path predictor is the whole settled history, the endpoint predictor the present state; D5 (occasion = one transition)",
                    null="the endpoint: the present state Y alone, the domain's Markov state",
                    domain="the Markov property (its definition: I(past; future | present) = 0) and the data-processing inequality I(X; Z) <= I(X; Y) (Cover & Thomas, ch. 2; named only, not fetched, R10)",
                    numbers=f"source reproduced: I(X; Y) = {Ixy:.4f} nats >= I(X; Z) = {Ixz:.4f} nats (difference {Ixy - Ixz:.4f}); forecast of Z: from the present Y, I(Z; Y) = {I_zy:.6f} nats; from the settled path (X, Y), I(Z; X, Y) = {I_zxy:.6f} nats; surplus of the path I(Z; X | Y) = {cond:.1e} nats. Observed chain (error eps): "
                            + "; ".join(f"eps = {e:g}: I(Z'; Y') = {c1:.4f}, I(Z'; X', Y') = {c2:.4f}, surplus {c2 - c1:.5f}" for e, c1, c2 in obs)
                            + f"; the surplus is largest at eps = {e_max:g} ({cond_obs[e_max]:.5f} nats) and is {cond_obs[0.0]:.1e} at eps = 0 (the full state) and {cond_obs[0.75]:.1e} at eps = 0.75 (an uninformative observation of {K} states)",
                    tg=f"I(Z; X, Y) {I_zxy:.6f} vs null I(Z; Y) {I_zy:.6f}: {ag(I_zxy, I_zy)} (surplus {cond:.1e})",
                    tn=f"the Markov property gives I(Z; X | Y) = 0, so the domain's value for the path predictor is the null itself ({I_zy:.6f})",
                    tc=f"|I(Z; X | Y)| < 1e-9 on the chain, the DPI I(X; Z) <= I(X; Y), and a positive surplus ({cond_obs[0.2]:.5f} > 1e-4) on the observed chain at eps = 0.2: {hf(check)}",
                    out=out,
                    reading=f"batch 04 row 2 read the same ingredient on a point process (the exponential Hawkes intensity screens off the path); this row restates it on the queue's own system in Shannon's units and gets the same label, {out}: on a Markov carrier the ingredient does no work because the domain's definition forbids it, and the number that decides H-T1's question ('is the observed state the full state?') is I(past; future | present), which is the domain's own quantity. Where it is positive (a lossy observation, {cond_obs[e_max]:.5f} nats at eps = {e_max:g}) the domain calls it a hidden state, so the source row's DESCR stands: information theory answers CRR's path-versus-endpoint question per system, and the answer is 'name the state'",
                    weakness="one random chain and one observation-channel family; the observed-chain arm is printed, not scored (the outcome is the chain's), and its positive conditional information is the standard hidden-Markov fact; no Fisher arc is computed (the path predictor here is the history itself, the strongest form of the ingredient)",
                    elegance="What a message loses on the way it cannot get back: each step can only pass on what it received. The picture is a line of people whispering, and it needs no formula.",
                    child="Imagine whispering a secret down a line of friends. Each friend can only pass on what they heard, never more. If the third friend garbled it, the fourth cannot fix it by thinking harder, and asking the second friend again only helps if the fourth heard the third one badly.")


# ---------------------------------------------------------------- 117: [9] information length of a relaxing Gaussian
def _source_path():
    """The source's ad hoc relaxation (mean 2 -> 0 and sd 2.5 -> 1 at one rate) and its C, C*, S on the Gaussian half-plane."""
    t = np.linspace(0, 6, 6001); m = 2.0 * np.exp(-t); s = 1.0 + 1.5 * np.exp(-t)
    u = m / math.sqrt(2); steps = np.sqrt(np.diff(u) ** 2 + np.diff(s) ** 2) / (0.5 * (s[1:] + s[:-1]))
    L = float(steps.sum()) * math.sqrt(2); a, b = (u[0], s[0]), (u[-1], s[-1])
    chord = math.sqrt(2) * math.acosh(1 + ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) / (2 * a[1] * b[1]))
    return L, chord, L - chord


def _ou(m0, s0, g=1.0, T=60.0):
    """OU relaxation dx = -g x dt + sqrt(2 g) dW from N(m0, s0^2) to N(0, 1): information length L (D2 on the Gaussian family,
    ds^2 = (dm^2 + 2 dsd^2)/sd^2), Fisher-Rao chord C* to the stationary state, endpoint KL(p_0 || pi), and the total entropy
    production Sigma = int sigma dt with sigma = g (m^2 + (v - 1)^2 / v) (the mean-square drift-current velocity over D = g)."""
    m = lambda tt: m0 * math.exp(-g * tt); v = lambda tt: 1.0 + (s0 ** 2 - 1.0) * math.exp(-2.0 * g * tt)
    speed = lambda tt: g * math.sqrt(m(tt) ** 2 + 2.0 * (v(tt) - 1.0) ** 2 / v(tt)) / math.sqrt(v(tt))
    sigma = lambda tt: g * (m(tt) ** 2 + (v(tt) - 1.0) ** 2 / v(tt))
    L = integrate.quad(speed, 0.0, T, limit=400)[0]; Sig = integrate.quad(sigma, 0.0, T, limit=400)[0]
    Cs = math.sqrt(2.0) * math.acosh(1.0 + ((m0 / math.sqrt(2.0)) ** 2 + (s0 - 1.0) ** 2) / (2.0 * s0 * 1.0))
    E = 0.5 * (m0 ** 2 + s0 ** 2 - 1.0 - math.log(s0 ** 2))
    return L, Cs, E, Sig


def r2():
    C0, Cs0, S0 = _source_path()
    grid = [(m0, s0) for m0 in (0.0, 0.5, 1.0, 2.0, 3.0) for s0 in (0.4, 0.7, 1.0, 1.5, 2.5) if not (m0 == 0.0 and s0 == 1.0)]
    R = np.array([_ou(m0, s0) for m0, s0 in grid]); L, Cs, E, Sig = R.T
    max_rel = float(np.max(np.abs(Sig - E) / E))
    r2_E, r2_EL, r2_L, r2_L2, r2_Cs = _r2(Sig, E), _r2(Sig, np.c_[E, L]), _r2(Sig, L), _r2(Sig, L ** 2), _r2(Sig, Cs)
    sp_L, sp_Cs, sp_E = float(spearmanr(Sig, L)[0]), float(spearmanr(Sig, Cs)[0]), float(spearmanr(Sig, E)[0])
    i_a, i_b = grid.index((0.0, 0.4)), grid.index((0.0, 2.5))                   # two starts with the same information length
    gain = r2_EL - r2_E
    check = max_rel < 1e-8 and gain <= 0.005
    out = outcome(crr=r2_EL, null=r2_E, domain=r2_E, check=check)
    return make_row("thermo", "A Gaussian relaxing under Ornstein-Uhlenbeck dynamics dx = -x dt + sqrt(2) dW (stationary state N(0, 1)): mean m0 e^-t, variance 1 + (s0^2 - 1) e^-2t, on a 24-start grid m0 in {0, 0.5, 1, 2, 3} x s0 in {0.4, 0.7, 1, 1.5, 2.5}; the source's path (mean 2 -> 0 and sd 2.5 -> 1 at one rate) reproduced first",
                    source=f"{SRC} [9] (CONSIST)",
                    Q="on a detailed-balance relaxation the total entropy produced is a function of the endpoint alone, KL(p_0 || pi), so the information length (D2 on the path of distributions, H-T1's path) adds nothing to the endpoint as a predictor of the dissipation: H-T1's must-fail case on a linear system, read in the thermodynamics of information",
                    ingredient="D6/H-T1 (path against endpoint) applied to the information length; D2-D4 themselves are information geometry's (the source row's whole content), so the proper ingredient is H-T1's comparison",
                    null="the endpoint: KL(p_0 || pi), the nonequilibrium free energy of the start",
                    domain="the H-theorem for detailed-balance Fokker-Planck dynamics: the entropy production rate is -d/dt KL(p_t || pi), so Sigma_tot = KL(p_0 || pi) (Esposito & Van den Broeck 2010, named only, not fetched, R10; the identity is verified here by quadrature)",
                    numbers=f"source reproduced: information length C = {C0:.4f}, chord C* = {Cs0:.4f}, surplus S = {S0:.4f} (every symbol information geometry's). OU grid of {len(grid)} starts: max relative |Sigma - KL| = {max_rel:.1e}; R^2 of Sigma on KL {r2_E:.6f}, on (KL, L) {r2_EL:.6f}, on L alone {r2_L:.4f}, on L^2 {r2_L2:.4f}, on the chord C* {r2_Cs:.4f}; Spearman(Sigma, KL) = {sp_E:.4f}, (Sigma, L) = {sp_L:.4f}, (Sigma, C*) = {sp_Cs:.4f}; two starts with the same information length: (m0, s0) = (0, 0.4) has L = {L[i_a]:.4f} and Sigma = {Sig[i_a]:.4f}, (0, 2.5) has L = {L[i_b]:.4f} and Sigma = {Sig[i_b]:.4f}; S = L - C* in [{np.min(L - Cs):.1e}, {np.max(L - Cs):.4f}]",
                    tg=f"R^2 with the path added {r2_EL:.6f} vs null endpoint alone {r2_E:.6f}: {ag(r2_EL, r2_E)} (gain {gain:+.1e})",
                    tn=f"the H-theorem gives Sigma = KL(p_0 || pi) (verified to {max_rel:.1e}), so the domain's value for the target is the null itself",
                    tc=f"Sigma = KL within 1e-8 and R^2 gain of the path <= 0.005: {hf(check)}",
                    out=out,
                    reading=f"the source row's content is D2-D4 on a path of distributions and reads REDUNDANT-IG by construction (synthesis.py row 6): its numbers reproduce and none of them is CRR's. The proper attempt, H-T1, returns {out} for the domain's reason: with detailed balance the dissipation is the endpoint's (R^2 {r2_E:.6f}), the path alone ranks it at Spearman {sp_L:.4f} and R^2 {r2_L:.4f}, and two starts with the same information length {L[i_a]:.4f} dissipate {Sig[i_a]:.4f} and {Sig[i_b]:.4f}. This is the thermodynamic twin of the convex learner on which CRR.md section 5 says H-T1 must fail; the domain's identity says why",
                    weakness="a free relaxation to infinity, not a driven protocol (the driven case is the thermodynamic-length rows, batches 02 and 10, where the path bounds the dissipation and the bound is the domain's); the OU dynamics were chosen so that a stationary state exists; the source's own path (sd relaxing at the mean's rate) is not a Fokker-Planck path and is reproduced only for its numbers; one gamma, one grid",
                    elegance="The disorder a relaxing system creates for good depends only on where it started and where it settles, not on the road between. A rule a child can hold: the price is set by the two ends, and it is the domain's H-theorem, not CRR's.",
                    child="A cup of cocoa left on the table settles to room temperature. The mess it makes in the room's warmth, the part that can never be tidied back up, is fixed by how the cup started and how the room is, not by the road it took to get there. And two cups that look equally far from settled, one too hot and one too cold, can leave different amounts of mess.")


# ---------------------------------------------------------------- 118: [10] binary symmetric channel
def r3():
    H2 = lambda p: 0.0 if p <= 0.0 or p >= 1.0 else -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
    Cap = lambda p: 1.0 - H2(p); th = lambda p: 2.0 * math.asin(math.sqrt(p))
    p = 0.1; ks = (1, 2, 5, 10, 20, 50)
    casc = [(k, (1.0 - (1.0 - 2.0 * p) ** k) / 2.0) for k in ks]
    arc = {k: th(pk) for k, pk in casc}; cap = {k: Cap(pk) for k, pk in casc}
    arc_lim = th(0.5)                                                          # the degrading channel's whole arc, from p = 0 to 1/2
    fires = arc_lim >= math.pi                                                 # a half-turn of a rotor is pi
    p_half = math.sin(math.pi / 4.0) ** 2                                      # half-turn of the family's own length pi from p = 0
    p_anti = math.sin(math.pi / 2.0) ** 2                                      # the Fisher-Rao antipode (chord pi) of p = 0
    cuts = {"half-turn of the family's own length pi": p_half, "the Fisher-Rao antipode (chord pi)": p_anti}
    grid = (0.01, 0.1, 0.3, 0.5)
    dC = {q: math.log2((1 - q) / q) * math.sqrt(q * (1 - q)) for q in grid}    # capacity change per resolvable step of p (A1'/D1)
    h = 1e-4; hess = {q: (Cap(q + h) - 2 * Cap(q) + Cap(q - h)) / h ** 2 for q in grid}
    fish = {q: 1.0 / (q * (1 - q)) / math.log(2.0) for q in grid}
    hess_rel = max(rel(hess[q], fish[q]) for q in grid)
    n = 100; nC = n * Cap(p)
    out = outcome(unstated=True)
    return make_row("code", f"The binary symmetric channel with crossover p on the Bernoulli carrier (Fisher coordinate theta = 2 arcsin sqrt p, family length pi), and the degrading channel p_k = (1 - (1 - 2p)^k)/2 of k cascaded uses at p = {p:g}",
                    source=f"{SRC} [10] (DESCR)",
                    Q="none could be formed: every attempt returned a definition, an unreachable cut, or a row already read",
                    ingredient="tried: A3 (the cut) on the degrading channel and in its two static readings; A1'/D1 (capacity per resolvable step of p; capacity as the log of the number of resolvable messages); H-T1 (the cascade's capacity against its path, which is row 1 of this batch)",
                    null="the domain's own functions of p: C(p) = 1 - H2(p) and the Fisher information g(p) = 1/(p(1 - p))",
                    domain="Shannon 1948: C = 1 - H2(p), zero at p = 1/2, and capacity as the log of the number of distinguishable messages; the Hessian of the binary entropy is minus the Fisher information (the source battery's row 1)",
                    numbers=f"static cut readings from p = 0: {'; '.join(f'{name} -> p = {pc:.4f} (capacity {Cap(pc):.4f} bits, g = ' + (f'{1 / (pc * (1 - pc)):.2f}' if 0 < pc < 1 else 'infinite') + ')' for name, pc in cuts.items())}. Degrading channel at p = {p:g}: arc from p = 0 at k = {', '.join(f'{k}: {arc[k]:.4f} (capacity {cap[k]:.4f})' for k in ks)}; the whole arc to p = 1/2 is {arc_lim:.4f} = pi/2 {'>=' if fires else '<'} pi, so a half-turn {'is' if fires else 'is never'} reached. Capacity per resolvable step dC/dtheta at p = {', '.join(f'{q:g}: {dC[q]:.4f}' for q in grid)} bits per step; C''(p) against g(p)/ln 2 at the same p: max relative difference {hess_rel:.1e}; n = {n} uses at p = {p:g}: 2^(nC) = 2^{nC:.1f} = {2 ** nC:.2e} resolvable messages",
                    tg=f"no decisive quantity: the cut never fires on the degrading channel (arc {arc[50]:.4f} at k = 50 against the half-turn pi), and the two static readings put it at p = {p_half:.4f} (the dead point) and p = {p_anti:.4f} (the perfect inverting channel), neither reachable",
                    tn=f"the domain has every number tried: the dead point p = 1/2, the Hessian identity (relative difference {hess_rel:.1e}), the message count 2^(nC)",
                    tc="none: no Q",
                    out=out,
                    reading=f"the source's DESCR stands ('two curves of p, neither CRR's'). The spec's removed 'p = 1/2 antipode' is, under the half-turn reading of the family's own length, the cut at p = {p_half:.4f} where capacity vanishes, and under the Fisher-Rao antipode reading the perfect inverting channel at p = {p_anti:.4f} with capacity {Cap(p_anti):.4f} bit; a degrading channel reaches neither, its arc saturating at {arc_lim:.4f}, so A3 has no purchase (O3: the Bernoulli carrier is a segment, not a rotor). Batch 09 rows 3-4 already placed the pole-start cut on the fraction carrier as a definition; A1'/D1 returns a change of variables and Shannon's own definition of capacity; H-T1 returns row 1. The outcome is {out}",
                    weakness="one p and one motion (the cascade); the strong data-processing constant (1 - 2p)^2, which is the squared Fisher contraction at the midpoint, was not read because it is the domain's too")


# ---------------------------------------------------------------- 119: [11] natural time and the entropy per event
def _h_gamma_mean1(a):
    """Differential entropy (nats) of Gamma(a, scale 1/a), mean 1: a - ln a + ln Gamma(a) + (1 - a) psi(a)."""
    return a - math.log(a) + math.lgamma(a) + (1.0 - a) * float(special.digamma(a))


def _htilde(a, ap):
    """Interval entropy after rescaling by the integrated hazard of a gamma model of shape ap (mean 1), the rescaled mean
    normalised to 1: h(Lambda(X)) - ln E[Lambda(X)] with h(Lambda(X)) = h(X) + E[ln hazard(X)]. ap = a is the process's
    own compensator; ap = 1 is a constant hazard, i.e. the clock."""
    X = stats.gamma(a, scale=1.0 / a); M = stats.gamma(ap, scale=1.0 / ap); hi = float(X.ppf(1.0 - 1e-12))
    e_lnh = integrate.quad(lambda x: X.pdf(x) * (M.logpdf(x) - M.logsf(x)), 0.0, hi, limit=400)[0]
    e_Lam = integrate.quad(lambda x: X.pdf(x) * (-M.logsf(x)), 0.0, hi, limit=400)[0]
    return _h_gamma_mean1(a) + e_lnh - math.log(e_Lam), e_Lam


def r4():
    shapes = (3.0, 0.5); aps = (0.5, 1.0, 2.0, 3.0, 4.0, 6.0)
    res = {a: {ap: _htilde(a, ap) for ap in aps} for a in shapes}
    pois = [(lam, 1.0 - math.log(lam), 1.0) for lam in (0.1, 1.0, 10.0)]        # the source's row: h = 1 - ln lambda in clock time, 1 in natural time
    a0 = shapes[0]; crr = res[a0][a0][0]; null = res[a0][1.0][0]; domain = 1.0
    best = {a: max(res[a], key=lambda ap: res[a][ap][0]) for a in shapes}
    check = all(best[a] == a and abs(res[a][a][0] - 1.0) < 1e-6 and all(res[a][ap][0] < 1.0 - 1e-3 for ap in aps if ap != a) for a in shapes)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("point", f"Renewal point processes with gamma intervals of mean 1 (shape a = {shapes[0]:g}, CV {1 / math.sqrt(shapes[0]):.3f}, and a = {shapes[1]:g}, CV {1 / math.sqrt(shapes[1]):.3f}), each rescaled by the integrated hazard of a gamma model of shape a' (a' = a is the process's own compensator, a' = 1 the clock), the rescaled mean normalised to 1; entropies by quadrature; the source's Poisson rates reproduced",
                    source=f"{SRC} [11] (DESCR)",
                    Q="natural time is the mean-preserving time change that maximises the interval entropy of a point process: under its own compensator every process has interval entropy 1 nat per event, and under any other monotone time change of the same mean the entropy is lower",
                    ingredient="A1'/D1 (one event = one step; natural time = the compensator, the clock P5 uses), D5 [M] (the event is the cut)",
                    null="the clock: the raw interval at the same mean (a' = 1, a constant hazard)",
                    domain="the time-rescaling theorem (Meyer 1971; Ogata 1988; Brown et al. 2002) with the maximum-entropy property of the exponential at fixed mean (Shannon 1948; Jaynes 1957): Exp(1) has entropy 1 nat and is the unique maximiser; named only, not fetched (R10)",
                    numbers=f"source reproduced: Poisson rate {', '.join(f'{lam:g}: {hc:.4f} nats in clock time, {hn:.4f} in natural time' for lam, hc, hn in pois)}. "
                            + "; ".join(f"a = {a:g} (clock entropy h(X) = {_h_gamma_mean1(a):.4f} nats, closed form): mean-normalised entropy after rescaling by a' = " + ", ".join(f"{ap:g}: {res[a][ap][0]:.4f} (mean {res[a][ap][1]:.4f})" for ap in aps) + f"; maximum at a' = {best[a]:g}" for a in shapes),
                    tg=f"entropy per event in natural time {crr:.4f} nats (a = {a0:g}) vs null in clock time {null:.4f}: {ag(crr, null)}",
                    tn=f"MaxEnt at fixed mean gives {domain:.4f} nat for the maximum: {ag(crr, domain, TOL_N)} (the domain has Q)",
                    tc=f"for both shapes the maximum over the a' grid is at a' = a, equals 1 within 1e-6 and every other a' is below 1 - 1e-3: {hf(check)}",
                    out=out,
                    reading=f"batch 04 row 1 and batch 07 row 5 read natural time on Omori sequences as the compensator that homogenises the events (Ogata's residual analysis); the Shannon reading adds one clause, that of all mean-preserving clocks the system's own is the one under which each occasion is the most uncertain a positive interval of that mean can be (entropy {crr:.4f} against {null:.4f} on the clock for a = {a0:g}, {res[shapes[1]][shapes[1]][0]:.4f} against {res[shapes[1]][1.0][0]:.4f} for a = {shapes[1]:g}), and both halves of that clause are the domain's theorems (rescaling gives Exp(1); Exp(1) is the MaxEnt law at fixed mean). The source's 'a change of variables and nothing more' stands; the outcome is {out}",
                    weakness="the compensator of a renewal process is known in closed form; on data it is a fitted model and the entropy then measures the fit, which is residual analysis again; the a' grid is finite (six models), the alternative clocks are hazards of one family, and the entropies are quadratures, not sample estimates; rho is not involved",
                    elegance="Among all the ways of stretching a clock that keep the average gap the same, the system's own clock, the one that counts expected events, is the one that makes each gap as unpredictable as a gap of that size can be. A rule with no knobs, and it is Shannon's exponential.",
                    child="Imagine heartbeats that sometimes bunch up and sometimes spread out. Measured with a stopwatch, some gaps look predictable. If instead you measure each gap by how many beats you expected in it, every gap becomes a pure surprise, the biggest surprise a gap of that average size can be. The heart's own clock is the one that keeps the most surprise.")


# ---------------------------------------------------------------- 120: [12] P2 as the conditional limit of uniform recall
def _gibbs(S, b):
    v = np.exp(b * S); return v / v.sum()


def _conditioned(S_int, wT, N, T):
    """Exact P(occasion j is the first draw | the total of N i.i.d. draws' scores = T) under the tilted law wT (the conditional
    law is tilt-invariant, so this is the uniform-draw conditional); by exchangeability it is the expected empirical frequency."""
    kern = np.zeros(int(S_int.max()) + 1); kern[S_int] = wT
    P = np.array([1.0])
    for _ in range(N - 1):
        P = np.convolve(P, kern)
    PN = np.convolve(P, kern)
    num = np.array([wT[j] * (P[T - s] if 0 <= T - s < len(P) else 0.0) for j, s in enumerate(S_int)])
    return num / PN[T]


def r5():
    S = np.array([0.2, 0.9, 1.5, 0.4, 1.1]); beta = 1.3; w = _gibbs(S, beta); target = float(w @ S); Hw = _H(w)   # the source's five occasions
    S_int = np.rint(10.0 * S).astype(int); j_top = int(np.argmax(S))
    rows = []
    for N in (20, 100, 500, 2000):
        T = int(round(10.0 * target * N)); tgt = T / (10.0 * N)
        bT = brentq(lambda b: float(_gibbs(S, b) @ S) - tgt, -20.0, 20.0, xtol=1e-14); wT = _gibbs(S, bT)
        cond = _conditioned(S_int, wT, N, T)
        rows.append((N, T, bT, wT, cond, float(np.max(np.abs(cond - wT) / wT)), _H(cond)))
    devs = [r[5] for r in rows]; last = rows[-1]; beta_shift = max(abs(r[2] - beta) for r in rows)
    crr, null, dom = float(w[j_top]), 1.0 / len(S), float(last[4][j_top])
    check = all(d2 < d1 for d1, d2 in zip(devs[:-1], devs[1:])) and devs[-1] < TOL_N
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("prior", f"Five settled occasions with surpluses S = ({', '.join(f'{s:g}' for s in S)}) (the source's) and a regenerating system that recalls them by N uniform random draws conditioned on the mean surplus of the draws equalling P2's target at beta = {beta:g}; N = {', '.join(str(r[0]) for r in rows)}, exact conditional frequencies by the tilted generating polynomial (surpluses on a lattice of 0.1)",
                    source=f"{SRC} [12] (DESCR)",
                    Q="the P2 weights are the recall frequencies of a regenerating system that samples its settled past uniformly under one mean-surplus constraint: conditioned on the mean surplus of the draws, the expected frequency of each occasion converges to e^(beta S_m)/Z with error vanishing in N",
                    ingredient="P2 (surplus weights) inside A6 (regeneration from settled occasions under one history constraint), D5",
                    null="beta = 0: uniform recall (1/5 each), the unconstrained draw",
                    domain="the conditional limit theorem (van Campenhout & Cover 1981; Csiszar 1984; Cover & Thomas thm 11.6.2): the empirical distribution of i.i.d. draws conditioned on a linear constraint converges to the I-projection, which is the Gibbs form; named only, not fetched (R10)",
                    numbers=f"source reproduced: Gibbs weights ({', '.join(f'{x:.4f}' for x in w)}), entropy {Hw:.4f} nats, mean surplus {target:.4f}. Conditioned recall: "
                            + "; ".join(f"N = {N}: total {T} (beta for the lattice target {bT:.6f}), frequencies ({', '.join(f'{x:.4f}' for x in cond)}), max relative deviation from Gibbs {d:.2e}, entropy {Hc:.4f}" for N, T, bT, wT, cond, d, Hc in rows),
                    tg=f"weight on the highest-surplus occasion {crr:.4f} (P2) vs null {null:.4f} (uniform): {ag(crr, null)}",
                    tn=f"the conditional limit at N = {last[0]} gives {dom:.4f}: {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"the maximum relative deviation falls along N ({' -> '.join(f'{d:.1e}' for d in devs)}) and is below {TOL_N:g} at N = {last[0]}: {hf(check)}",
                    out=out,
                    reading=f"batch 03 row 1 read the same weights as an estimator (the surplus-weighted seed loses to the accumulated mean: WRONG); read instead as a law of recall, a system that draws its past at random but must reproduce one mean surplus recalls the P2 weights, and that is the conditional limit theorem, the information-theoretic ground of Jaynes's rule; the source's 'CRR's weights are Jaynes's' stands with Cover's name added. CRR fixes neither beta nor the constraint (O2), and the row shows only that whatever constraint is chosen, the exponential shape is forced. The outcome is {out}",
                    weakness=f"the constraint (mean surplus) is the one thing CRR does not fix (O2), so the row tests the shape, not the choice; the lattice makes the total an integer and moves beta by at most {beta_shift:.1e} over the four N; the theorem is exact and the row checks convergence at four N only",
                    elegance="Pick old days to remember by rolling a die, but keep rolling until the days you picked carry the right average amount of extra: the days you end up favouring follow one fixed exponential curve, and no other shape can come out. The rule has no knobs but the average.",
                    child="Suppose you choose which old days to remember by rolling a die, but you have to keep going until the days you picked have, on average, a certain amount of extra in them. Which days will you have picked most? The ones with the most extra, and by an amount that grows in the same steady way from one day to the next. That is the only pattern that can come out.")


def main():
    return run_batch("Synthesis batch 24: rows 116-120 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
