"""CRR against Shannon information theory: where the Fisher-Rao quantities the framework uses meet Shannon's
(owner request 2026-09-17, prompt-log entry 58). The literature status (2026 papers, abstracts and snippets only)
is recorded separately in docs/citations/shannon_2026-09-17.md; every number here is computed by this script.

Twelve rows: (1) the Fisher metric as the Hessian of KL and D6's sqrt(2 KL) step; (2) de Bruijn's identity along
the heat flow; (3) Stam's inequality (entropy power times Fisher information); (4) the Jeffreys prior as the
mutual-information-maximising (reference) prior; (5) Clarke-Barron asymptotics: mutual information is the log of the
number of resolvable steps; (6) rate-distortion at the unit; (7) the data-processing inequality as A4/H-T1;
(8) Landauer's bound at a reset cut; (9) information length as D2 on a path of distributions; (10) binary-symmetric
channel capacity at the Fisher midpoint; (11) natural time as the time-change giving unit entropy per event;
(12) MaxEnt weights (P2) as Shannon-entropy maximisers. Grades under the issue-#21 rules; BORROWED per row.
No dataset opened (R2). Deterministic. Run:
uv run python theory/retrodictions/shannon.py
"""
import math
import sys

import numpy as np
from scipy import integrate, special, stats

from crr.instrument.core import arc_length, kl_gauss

ROWS = []


def row(cls, system, clause, borrowed, derivation, known, verdict, grade, weakness=""):
    ROWS.append(dict(cls=cls, system=system, clause=clause, borrowed=borrowed, derivation=derivation, known=known,
                     verdict=verdict, grade=grade, weakness=weakness))


# ---------------------------------------------------------------- 1 KL curvature and the sqrt(2 KL) step
def kl_curvature():
    kl = kl_gauss(np.array([0.0]), np.array([0.7]), var=1.0); d_exact = 0.7
    def kl_bern(p, q): return p * math.log(p / q) + (1 - p) * math.log((1 - p) / (1 - q))
    def d_fr(p, q): return abs(2 * math.asin(math.sqrt(p)) - 2 * math.asin(math.sqrt(q)))
    p = 0.3; ratios = [(dq, math.sqrt(2 * kl_bern(p, p + dq)) / d_fr(p, p + dq)) for dq in (0.2, 0.05, 0.01, 0.001)]
    row("geom", "The Fisher metric is the Hessian of the Kullback-Leibler divergence; D6's step sqrt(2 KL) is the Fisher-Rao distance to second order", "D6 (C = sum sqrt(2 KL_step)), P8 (exact for a fixed-variance Gaussian), A1",
        "KL divergence; Fisher information as its Hessian (Kullback 1959); SCOPE.md P8",
        f"fixed-variance Gaussian shift 0.7: sqrt(2 KL) = {math.sqrt(2 * kl):.4f} = Fisher-Rao distance {d_exact:.4f} exactly; Bernoulli at p = 0.3, ratio sqrt(2 KL)/d_FR for steps {', '.join(f'{dq:g}: {r:.4f}' for dq, r in ratios)} -> 1 as the step -> 0",
        "KL(p_theta || p_theta+d) = (1/2) g d^2 + O(d^3): the Fisher metric is the local quadratic form of Shannon's divergence",
        "the bridge from CRR's arc to Shannon's divergence is the standard second-order identity; D6's path length is exact only in the small-step limit (or the Gaussian case), and the discretisation error is the domain's, not a CRR quantity",
        "DESCR", "inherited; the framework's arc is Shannon's divergence integrated along the path")


# ---------------------------------------------------------------- 2 de Bruijn's identity
def de_bruijn():
    def p_t(x, t): return 0.5 * (stats.norm.cdf((x + 1) / math.sqrt(t)) - stats.norm.cdf((x - 1) / math.sqrt(t)))
    def h(t):
        def f(x):
            p = p_t(x, t); return -p * math.log(p) if p > 1e-300 else 0.0
        lim = 1 + 8 * math.sqrt(t); return integrate.quad(f, -lim, lim, limit=400)[0]
    def J(t):
        def f(x):
            p = p_t(x, t)
            if p < 1e-12: return 0.0                                   # the tails carry no measurable Fisher information; avoids dp^2 / p blow-up at the density floor
            dp = 0.5 * (stats.norm.pdf((x + 1) / math.sqrt(t)) - stats.norm.pdf((x - 1) / math.sqrt(t))) / math.sqrt(t)
            return dp * dp / p
        lim = 1 + 8 * math.sqrt(t); return integrate.quad(f, -lim, lim, limit=400)[0]
    t0 = 0.5; eps = 1e-3; dh = (h(t0 + eps) - h(t0 - eps)) / (2 * eps); half_J = 0.5 * J(t0)
    row("geom", "de Bruijn's identity: entropy rate along the heat flow equals half the Fisher information", "D2 read on the path of smoothed distributions (a Fisher speed), A1",
        "de Bruijn's identity (Stam 1959); Gaussian convolution of a uniform density",
        f"X uniform on [-1, 1] plus sqrt(t) Z at t = 0.5: dh/dt = {dh:.5f} (finite difference), J/2 = {half_J:.5f}; relative difference {abs(dh - half_J) / half_J:.1e}",
        "d/dt h(X + sqrt t Z) = (1/2) J(X + sqrt t Z): Shannon entropy grows along diffusion at half the Fisher information",
        "along the smoothing path the Fisher information is the entropy's rate of growth: the one classical identity that makes CRR's Fisher quantity a Shannon quantity, and it is Stam's, not CRR's",
        "CONSIST", "inherited (Stam 1959); the framework reads the identity, it did not produce it")


# ---------------------------------------------------------------- 3 Stam's inequality
def stam():
    def NJ(h, J): return math.exp(2 * h) / (2 * math.pi * math.e) * J
    b = 1.0; lap = NJ(1 + math.log(2 * b), 1 / b ** 2); gau = NJ(0.5 * math.log(2 * math.pi * math.e), 1.0)
    row("geom", "Stam's inequality: entropy power times Fisher information is at least one, with equality only for the Gaussian", "A1' (the unit is 1/sqrt(J)), D1 (resolution)",
        "Stam 1959; entropy power N = e^{2h}/(2 pi e)",
        f"N J: Laplace(1) = {lap:.4f} (= 2e/pi), Gaussian = {gau:.4f}; the bound is 1",
        "the Gaussian has the least Fisher information for a given entropy: a resolvable step (1/sqrt J) is never larger than the entropy-power width",
        "CRR's unit (one resolvable step, 1/sqrt J) is bounded above by Shannon's entropy power for every density: the two notions of 'how much room a distribution has' agree up to a factor fixed by Stam, and the factor is the domain's",
        "DESCR", "inherited; a carrier fact about the unit")


# ---------------------------------------------------------------- 4 Jeffreys prior as the reference prior
def _mi_bernoulli(a, n):
    """I(theta; k) for k ~ Binomial(n, theta), theta ~ Beta(a, a), by quadrature (nats)."""
    ks = np.arange(n + 1); logC = special.gammaln(n + 1) - special.gammaln(ks + 1) - special.gammaln(n - ks + 1)
    # marginal m(k) = C(n,k) B(k+a, n-k+a)/B(a,a)
    logm = logC + special.betaln(ks + a, n - ks + a) - special.betaln(a, a); m = np.exp(logm)
    H_k = -np.sum(m * logm)
    def H_cond(th):
        lp = logC + ks * np.log(th) + (n - ks) * np.log(1 - th); p = np.exp(lp); return -np.sum(p * lp)
    E_H = integrate.quad(lambda th: stats.beta.pdf(th, a, a) * H_cond(th), 1e-6, 1 - 1e-6, limit=200)[0]
    return H_k - E_H


def jeffreys_reference():
    n = 200; res = {a: _mi_bernoulli(a, n) for a in (0.25, 0.5, 1.0, 2.0, 4.0)}; best = max(res, key=res.get)
    row("prior", "The Jeffreys prior (density proportional to sqrt g) as the prior that maximises the mutual information between parameter and data", "A1 (Fisher carrier), A1' (the unit is one step of sqrt g), P2/P3 (MaxEnt weights)",
        "Bernardo 1979 reference priors; Clarke & Barron 1994 (Jeffreys is asymptotically reference for regular models)",
        f"Bernoulli, n = {n}, priors Beta(a, a): I(theta; data) in nats = " + ", ".join(f"a = {a:g}: {v:.4f}" for a, v in res.items()) + f"; maximum at a = {best:g} (Jeffreys is a = 0.5)",
        "the prior that lets the data say the most is uniform in Fisher-Rao arc length: one prior mass per resolvable step",
        "Shannon's optimal prior is uniform in CRR's unit: a genuine Fisher-Shannon bridge, and it is Bernardo's and Clarke-Barron's; CRR's A1' unit is the measure that bridge already uses",
        "CONSIST", "inherited; the framework did not produce the reference-prior theorem, it uses its measure")


# ---------------------------------------------------------------- 5 Clarke-Barron: mutual information is the log of the number of resolvable steps
def clarke_barron():
    L_F = math.pi                                                  # Fisher-Rao length of the Bernoulli family (radius-2 sphere quarter turn... = int dtheta/sqrt(theta(1-theta)) = pi)
    out = []
    for n in (100, 1000, 10000):
        mi = _mi_bernoulli(0.5, n); rho = L_F * math.sqrt(n / (2 * math.pi * math.e)); out.append((n, mi, math.log(rho), rho))
    row("prior", "Clarke-Barron asymptotics: the mutual information under the Jeffreys prior is the log of the number of resolvable steps of the carrier", "D1 (rho = extent / unit), A1' (unit = 1/sqrt(n g) at n observations)",
        "Clarke & Barron 1990/1994: I(theta; X^n) = (d/2) log(n / 2 pi e) + log int sqrt(det g) + o(1) under Jeffreys",
        "Bernoulli under Jeffreys: " + "; ".join(f"n = {n}: I = {mi:.4f} nats, log rho = {lr:.4f} (rho = pi sqrt(n/2 pi e) = {rho:.1f} resolvable steps)" for n, mi, lr, rho in out) + f"; the Fisher length of the family is pi = {L_F:.4f}",
        "asymptotically the data distinguish sqrt(n/2 pi e) times the Fisher length of the family many parameter values, and the information is their logarithm",
        "CRR's resolution rho (D1) is exactly the count whose logarithm is Shannon's mutual information at n observations: the strongest bridge in the battery, exact asymptotically, and it is Clarke-Barron's theorem read with CRR's names",
        "CONSIST", "inherited; D1 says rho is reported and never used in a threshold, and this row says why rho is the right thing to report: its log is the information the record carries about where the system is")


# ---------------------------------------------------------------- 6 rate-distortion at the unit
def rate_distortion():
    out = [(rho, math.log2(rho)) for rho in (2, 10, 100)]
    row("code", "Rate-distortion of a Gaussian source at distortion equal to the unit's variance", "A1' (unit sigma), D1 (rho)",
        "Shannon's rate-distortion function R(D) = (1/2) log(sigma^2 / D) for a Gaussian source",
        "distortion D = unit variance: R = log2(sigma_signal / sigma_unit) = log2 rho bits: " + ", ".join(f"rho = {r}: {b:.3f} bits" for r, b in out),
        "describing a Gaussian source to within one unit of error costs log2 rho bits per sample",
        "the unit turns Shannon's rate into log rho by substitution: a definition, and the same count as the Clarke-Barron row from the coding side",
        "DESCR", "rule 3: a change of variables in R(D)")


# ---------------------------------------------------------------- 7 data processing = depth one
def data_processing():
    rng = np.random.default_rng(1); K = 4
    T1 = rng.dirichlet(np.ones(K) * 0.7, K); T2 = rng.dirichlet(np.ones(K) * 0.7, K); px = rng.dirichlet(np.ones(K))
    pxy = px[:, None] * T1; py = pxy.sum(0); pyz = py[:, None] * T2; pxz = (px[:, None, None] * T1[:, :, None] * T2[None, :, :]).sum(1); pz = pxz.sum(0)
    def mi(pab, pa, pb): return float(np.sum(pab * np.log(pab / (pa[:, None] * pb[None, :]) + 1e-300)))
    Ixy, Ixz = mi(pxy, px, py), mi(pxz, px, pz)
    row("code", "The data-processing inequality on a Markov chain: the past adds nothing to the present state", "A4 (depth one), H-T1's convex-learner lemma (the endpoint is a sufficient statistic), O1",
        "data-processing inequality; Markov chains X -> Y -> Z",
        f"random 4-state chain X -> Y -> Z: I(X; Y) = {Ixy:.4f} nats >= I(X; Z) = {Ixz:.4f} nats (difference {Ixy - Ixz:.4f})",
        "no processing of Y can recover information about X that Y has lost",
        "A4's 'depth one' and the ledger's 'the old-probe endpoint predicts forgetting' are the data-processing inequality: when the state is Markov the path carries no information the state does not; where the batteries found path dependence (Preisach, Kovacs) the observed state was not the full state",
        "DESCR", "inherited (Shannon); the framework's path-vs-endpoint question is 'is the observed state Markov?', which information theory answers per system")


# ---------------------------------------------------------------- 8 Landauer at the cut
def landauer_cut():
    out = [(rho, math.log2(rho), math.log(rho)) for rho in (2, 10, 100)]
    row("thermo", "Landauer's bound at a reset cut: erasing the settled occasion's position costs at least kT ln 2 per bit", "A3 ('the cut has no content'), A6 (the settled past is retained as reweighted content, not erased), D1",
        "Landauer 1961; Bennett 1982 (copying is free, erasure is not)",
        "an adder-type cut resets a carrier resolved to rho steps: bits erased = log2 rho, minimum dissipation in kT: " + ", ".join(f"rho = {r}: {b:.2f} bits, {n:.2f} kT" for r, b, n in out),
        "resetting a memory to a standard state dissipates at least kT ln 2 per bit; retaining a record does not",
        "the framework's cut is content-free for the future but a physical reset erases the occasion's position, at a cost Landauer fixes and CRR does not mention; A6 (the past retained as content) and the threshold-reset systems (the past erased) are on opposite sides of Bennett's line, and no clause says which a system does",
        "OPEN", "no clause about the energetics of the cut; a real-data row would need a measured erasure cost per occasion (single-electron or optical-trap memories), gated first")


# ---------------------------------------------------------------- 9 information length
def information_length():
    t = np.linspace(0, 6, 6001); m = 2.0 * np.exp(-t); s = 1.0 + 1.5 * np.exp(-t)                   # mean and sd relax to (0, 1)
    u = m / math.sqrt(2); path = np.c_[u, s]; steps = np.sqrt(np.diff(u) ** 2 + np.diff(s) ** 2) / (0.5 * (s[1:] + s[:-1]))
    L = float(steps.sum()) * math.sqrt(2); a, b = (u[0], s[0]), (u[-1], s[-1])
    chord = math.sqrt(2) * math.acosh(1 + ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) / (2 * a[1] * b[1]))
    L_mean_only = float(np.sum(np.abs(np.diff(2.0 * np.exp(-t)))) / 1.0)
    row("thermo", "Information length of a relaxing Gaussian: D2 on the path of distributions, against its geodesic chord", "D2-D4 on a path of distributions (the Fisher-Rao arc of p_t), P1",
        "information length (Kim and co-workers; Crooks 2007 for the metric); the Gaussian family's Fisher-Rao metric (a hyperbolic half-plane)",
        f"mean 2 -> 0 and sd 2.5 -> 1 relaxing exponentially: information length C = {L:.4f}, geodesic chord C* = {chord:.4f}, surplus S = {L - chord:.4f}; with the sd fixed the length is |delta m| / sigma = {L_mean_only:.4f} exactly (a monotone path, S = 0)",
        "the information length counts the statistically distinguishable states a time-dependent distribution passes through",
        "information length is CRR's coherence on a distribution-valued carrier, and the surplus is the excess over the geodesic: the same objects the thermodynamic-length rows found, with the same verdict: the quantity is the domain's, the naming is CRR's",
        "CONSIST", "inherited; the batteries' thermodynamic-length verdict restated for non-equilibrium PDF paths")


# ---------------------------------------------------------------- 10 BSC capacity at the Fisher midpoint
def bsc_capacity():
    def H2(p): return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
    out = [(p, 1 - H2(p), 1 / (p * (1 - p))) for p in (0.01, 0.1, 0.3, 0.5)]
    row("code", "Binary symmetric channel: capacity against Fisher information across the crossover probability", "the removed 'p = 1/2 antipode' (spec XI.2), A1 (Fisher metric of the Bernoulli family)",
        "Shannon channel capacity of the BSC, C = 1 - H2(p); Fisher information of the Bernoulli family",
        "; ".join(f"p = {p:g}: C = {c:.4f} bits, g = {g:.2f}" for p, c, g in out),
        "capacity vanishes at p = 1/2 and is largest near p = 0 or 1; Fisher information is smallest at 1/2 and diverges at the ends",
        "the Bernoulli family's Fisher midpoint is the channel's dead point: had the older text's 'p = 1/2 antipode' been kept, the cut of a binary carrier would have sat at zero capacity; the spec removed it, and the removal is consistent with Shannon's reading",
        "DESCR", "a carrier fact; the two curves are unrelated functions of p and neither is a CRR result")


# ---------------------------------------------------------------- 11 natural time and entropy per event
def natural_time_entropy():
    out = [(lam, 1 - math.log(lam), 1.0) for lam in (0.1, 1.0, 10.0)]
    row("point", "Natural time as the time-change under which a Poisson process has unit entropy per event", "O3 (natural time gives the unit for point processes), D5 [M] (the event is the cut)",
        "differential entropy of the exponential distribution, h = 1 - ln lambda nats; time change tau = lambda t",
        "; ".join(f"rate {lam:g}: interval entropy in clock time {hc:.4f} nats, in natural time {hn:.4f} nat" for lam, hc, hn in out),
        "rescaling time by the rate makes every Poisson process the unit-rate process",
        "natural time is the clock in which each occasion of a Poisson process carries exactly one nat of interval entropy: a change of variables that says what O3's unit is in Shannon's terms, and nothing more",
        "DESCR", "rule 3: a definition of the unit")


# ---------------------------------------------------------------- 12 MaxEnt weights as entropy maximisers
def maxent_gibbs():
    S = np.array([0.2, 0.9, 1.5, 0.4, 1.1]); beta = 1.3; w = np.exp(beta * S); w /= w.sum(); target = float(w @ S)
    def H(q): return float(-np.sum(q * np.log(q)))
    rng = np.random.default_rng(2); worse = 0; trials = 2000
    for _ in range(trials):
        q = rng.dirichlet(np.ones(5)); q = q + (target - q @ S) * (S - S.mean()) / np.sum((S - S.mean()) ** 2)  # project onto the constraint
        if np.all(q > 0) and abs(q @ S - target) < 1e-9 and H(q) > H(w) + 1e-12: worse += 1
    row("prior", "P2's surplus weights as the Shannon-entropy maximiser under a mean-surplus constraint", "P2 (pi proportional to e^{beta S}), P3, O2",
        "Jaynes 1957 maximum entropy; Gibbs distributions",
        f"five occasions, beta = {beta}: Gibbs weights {np.round(w, 4)} with entropy {H(w):.4f} nats; among {trials} random distributions projected onto the same mean surplus, {worse} had higher entropy",
        "the maximum-entropy distribution under a linear constraint is the Gibbs form",
        "P2 and P3 are Shannon-entropy maximisers by construction (the theory says so: 'standard, Jaynes'); the framework fixes neither beta nor the constraint, and the measured-influence rows found kernels outside both families",
        "DESCR", "rule 3: CRR's weights are Jaynes's")


BATTERY = [kl_curvature, de_bruijn, stam, jeffreys_reference, clarke_barron, rate_distortion, data_processing, landauer_cut, information_length,
           bsc_capacity, natural_time_entropy, maxent_gibbs]
CLASSES = {"geom": "Fisher-Shannon identities", "prior": "priors, mutual information and MaxEnt", "code": "coding and processing", "thermo": "thermodynamics of information", "point": "point processes"}


def main():
    for f in BATTERY: f()
    print(f"CRR against Shannon information theory — {len(ROWS)} rows in {len(CLASSES)} groups. Grades: SHARP CONSIST DESCR FAILS TENSION OPEN\n")
    for i, r in enumerate(ROWS, 1):
        print(f"[{i:2d}] ({r['cls']}) {r['system']}\n     clause:     {r['clause']}\n     BORROWED:   {r['borrowed']}"
              f"\n     derivation: {r['derivation']}\n     known:      {r['known']}\n     verdict:    {r['verdict']}\n     GRADE:      {r['grade']}"
              + (f"\n     weakness:   {r['weakness']}" if r['weakness'] else ""))
    grades = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")
    print("\n" + "=" * 100 + "\nTALLY")
    print(f"{'group':40s} " + " ".join(f"{g:>8s}" for g in grades))
    for c, name in CLASSES.items():
        rs = [r for r in ROWS if r["cls"] == c]
        print(f"({c}) {name:32s} " + " ".join(f"{sum(r['grade'] == g for r in rs):8d}" for g in grades))
    print(f"{'all':40s} " + " ".join(f"{sum(r['grade'] == g for r in ROWS):8d}" for g in grades))
    print(f"\nRows where a CRR clause reaches a result the domain did not already have: {sum(r['grade'] == 'SHARP' for r in ROWS)} of {len(ROWS)}."
          " Every Fisher-Shannon bridge in the battery (de Bruijn, Stam, Bernardo/Clarke-Barron, Landauer, information length, Jaynes) predates the framework; CRR's contribution is the naming.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
