"""Synthesis batch 30: Lee Smolin's mathematics taken with CRR whole (owner request 2026-09-24, prompt-log entry 130;
declared in DECLARATION_29_30.md, pushed before this script). Three rows on model systems (no data, R2): [1] the
principle of precedence with A6's bounded memory against precedence as stated (a Polya urn with immigration) and against
quantum mechanics' i.i.d. outcomes; [2] cosmological natural selection with A6 inheritance (a universe seeded from the
bounded age-weighted mean of its lineage) against parent-only inheritance and Gaussian mutation-selection balance;
[3] cosmological natural selection counted in natural time (generations, D5 occasions) against clock time.
Sources (docs/citations/smolin_rovelli_gough_2026-09-24.md, versions seen 2026-09-24): Smolin 1205.3707 v1
(Postulate 6, the lock-in problem); hep-th/0612185 v1 (Hypotheses I-II, the unproved convergence claim); Altenberg
1302.1293 v2 (the reduction principle for CNS). Named by name and year only: Kimura / Lande (Gaussian mutation-selection
balance); Karlin 1982 (the reduction principle). Deterministic; under 60 s."""
import math
import sys

import numpy as np

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _w(cond, yes, no):
    return yes if cond else no


# ---------------------------------------------------------------- [1] precedence with bounded memory
def _precedence(q, eps=0.05, p=0.3, worlds=200, n=10000, free=5, seed=301):
    """Vectorised over worlds. q None: precedence as stated (uniform over all past outcomes: Polya urn with immigration);
    q in (0, 1): A6 (age-weighted precedent, weights q^k, never an accumulated count). eps: the share of free draws (Born)."""
    rng = np.random.default_rng(seed)
    c = np.zeros(worlds); m = np.full(worlds, np.nan); out = np.zeros((n, worlds), np.int8)
    for k in range(n):
        u = rng.random(worlds); v = rng.random(worlds); w = rng.random(worlds)
        freep = (k < free) | (u < eps)
        prec = c / max(k, 1) if q is None else np.where(np.isnan(m), p, m)
        o = np.where(freep, w < p, v < prec).astype(np.int8)
        out[k] = o; c += o
        if q is not None: m = np.where(np.isnan(m), o, q * m + (1 - q) * o)
    x = out[n // 2:].astype(float); f = x.mean(0); xc = x - f
    den = (xc ** 2).sum(0); ac = np.where(den > 0, (xc[1:] * xc[:-1]).sum(0) / np.where(den > 0, den, 1), 1.0)
    return f, ac


def r1():
    p = 0.3; n_win = 5000
    fA, acA = _precedence(0.9); fU, acU = _precedence(None)
    spread_crr = float(fA.std()); spread_null = float(fU.std()); lag_crr = float(acA.mean()); lag_null = float(acU.mean())
    binom = math.sqrt(p * (1 - p) / n_win)
    crr = spread_crr; null = spread_null; domain = binom
    check = spread_crr <= 3 * binom and abs(lag_crr) < 0.01
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("prec", "a binary measurement with Born probability p = 0.3 repeated 10000 times on identically prepared systems, in 200 independent worlds; the first 5 outcomes and 5 % of the rest are free (drawn from Born), the others follow precedent; statistics over the last 5000 draws",
                    source="smolin dossier 3 (1205.3707 v1, Postulate 6; the lock-in problem: 'all future measurements would repeat the first random choice')",
                    Q="precedence with A6's bounded memory (the precedent is the age-weighted record, weights q^k, q = 0.9, never an accumulated count) forgets the first accidents and so reproduces Born statistics: the across-world spread of the long-run frequency is binomial and successive outcomes are independent",
                    ingredient="A6 (regeneration from the settled occasions by a bounded, age-weighted mean) with P3's geometric weights",
                    null="precedence as Smolin states it: a uniform draw from all past outcomes (a Polya urn with 5 % immigration)",
                    domain="quantum mechanics: outcomes on independently prepared systems are i.i.d. Bernoulli(p); the spread of a 5000-draw frequency is sqrt(p(1-p)/5000), the lag-1 correlation is 0",
                    numbers=f"across-world spread of the frequency: A6 {spread_crr:.4f}, Polya {spread_null:.4f}, binomial {binom:.4f}; mean frequency A6 {fA.mean():.4f}, Polya {fU.mean():.4f} (Born {p}); mean lag-1 correlation A6 {lag_crr:+.4f}, Polya {lag_null:+.4f}",
                    tg=f"spread {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the binomial law gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc=f"spread within 3x binomial and lag-1 below 0.01: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"bounded memory treats Smolin's lock-in (the spread across worlds falls from {spread_null:.4f} to {spread_crr:.4f}, because an early accident is forgotten) but breaks what quantum mechanics requires: with a finite memory the precedent is a small, self-feeding sample, so successive outcomes are correlated (lag-1 {lag_crr:+.4f}) and the frequency wanders ({spread_crr / binom:.1f}x the binomial spread); precedence as stated keeps independence (lag-1 {lag_null:+.4f}) but locks in; neither recovers Born statistics from precedent alone, which is the dossier's open problem, and A6's 'never an accumulated count' is on the wrong side of it for quantum outcomes",
                    weakness="one free-draw share (5 %) and one memory (q = 0.9); the lag-1 correlation falls as q -> 1, which is the accumulated count A6 forbids; Smolin's small-n regime is unspecified, so the free-draw rule is this row's choice",
                    elegance="", child="")


# ---------------------------------------------------------------- [2] CNS with A6 inheritance
def _gauss_eq(q, mu=0.01, w2=1.0, iters=20000):
    S = np.eye(2) * 0.1; e = np.array([1.0, 0.0])
    A = np.array([[1 - q, q], [1 - q, q]]); M = np.array([[mu, 0.0], [0.0, 0.0]])
    for _ in range(iters):
        S = S - np.outer(S @ e, S @ e) / (S[0, 0] + w2)                        # selection: offspring number ~ exp(-x^2 / 2 w2)
        S = A @ S @ A.T + M                                                     # inheritance: seed = (1-q) x + q m, x' = seed + N(0, mu), m' = seed
    return S


def _approach(q, mu=0.01, w2=1.0, d0=1.0, gens=4000):
    S = _gauss_eq(q, mu, w2); mean = np.array([d0, d0]); e = np.array([1.0, 0.0]); A = np.array([[1 - q, q], [1 - q, q]])
    for g in range(gens):
        mean = mean - (S @ e) * mean[0] / (S[0, 0] + w2); mean = A @ mean
        if abs(mean[0]) < d0 / 2: return g + 1
    return gens


def r2():
    mu, w2 = 0.01, 1.0
    Vq = float(_gauss_eq(0.5)[0, 0]); V0 = float(_gauss_eq(0.0)[0, 0])
    Vd = (-mu + math.sqrt(mu * mu + 4 * mu * w2)) / 2 + mu                      # the domain's balance (variance before selection) for parent-only inheritance
    load = lambda V: 0.5 * math.log(1 + V / w2)                                 # the mean log-fitness deficit of a Gaussian population at the optimum
    crr = load(Vq); null = load(V0)
    check = crr < null
    out = outcome(crr=crr, null=null, domain=None, check=check)
    h_q = _approach(0.5); h_0 = _approach(0.0)
    return make_row("cns", "cosmological natural selection as a Gaussian replicator-mutator: parameter x, offspring number (black holes) ~ exp(-x^2 / 2 w^2), w^2 = 1, mutation variance mu = 0.01 per generation, lineage memory m",
                    source="smolin dossier 1d problems 1-2 (the mutation kernel is unspecified; convergence asserted, not proved); Altenberg 1302.1293 v2",
                    Q="with A6 inheritance (a universe's seed is the bounded age-weighted mean of its lineage, q = 0.5: seed = (1-q) x_parent + q m_lineage) the equilibrium ensemble sits closer to the fitness peak: its parameter variance and mutation load are lower than under parent-only inheritance",
                    ingredient="A6 (regeneration from the settled past by a bounded Frechet mean; on this 1-D Gaussian carrier the weighted mean) with P3's geometric age weights",
                    null="parent-only inheritance, q = 0 (Smolin's Hypothesis II as usually read)",
                    domain=None,
                    numbers=f"equilibrium variance before selection: A6 (q = 0.5) {Vq:.5f}, parent-only {V0:.5f} (the domain's closed form for parent-only {Vd:.5f}); mutation load (mean log-fitness deficit): A6 {crr:.5f}, parent-only {null:.5f}; generations to halve a unit displacement from the peak: A6 {h_q}, parent-only {h_0}",
                    tg=f"load {crr:.5f} vs null {null:.5f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn="no closed form for the A6 kernel found; the domain's formula reproduces the null (parent-only) exactly",
                    tc=f"the exact Gaussian recursion gives a lower load under A6: {_w(check, 'holds', 'fails')}",
                    out=out,
                    reading=f"CRR supplies the inheritance law CNS leaves open and it has a checkable consequence: lineage memory lowers the equilibrium load ({crr:.5f} against {null:.5f}), so universes sit closer to a local maximum of black-hole production, which sharpens Smolin's master prediction M; the price is a slower climb ({h_q} generations to halve a displacement against {h_0}); Altenberg's reduction principle already says selection favours more faithful inheritance, so the direction is the domain's and only the specific kernel (A6 with P3) is new",
                    weakness="the transgenerational and maternal-inheritance literature (Kirkpatrick and Lande 1989; Day and Bonduriansky 2011) may already contain this kernel and its load; not fetched; a Gaussian landscape near one peak; the black-hole fitness and the bounce's inheritance are Smolin's unproved hypotheses I and II",
                    elegance="A family of universes that remembers its grandparents, not only its parents, stays nearer the top of the hill.",
                    child="Baby universes are copies of their parents with small mistakes. If each baby also copies a bit from its grandparents, the mistakes cancel out a little, and the family stays closer to the best recipe.")


# ---------------------------------------------------------------- [3] CNS in natural time (generations) against clock time
def r3():
    p = np.linspace(-1.0, 1.0, 401); f = 2.0 * np.exp(-(p - 0.3) ** 2 / 0.1) + 0.5; tau = np.exp(1.5 * p)
    Kx = np.exp(-(p[:, None] - p[None, :]) ** 2 / (2 * 0.02 ** 2)); Kx /= Kx.sum(0, keepdims=True)
    Gg = Kx * f[None, :]                                                        # generation operator: offspring density = K f rho
    ev, V = np.linalg.eig(Gg); v = np.abs(np.real(V[:, np.argmax(np.real(ev))])); crr = float(p[np.argmax(v)])
    Gt = Kx * (f / tau)[None, :] - np.diag(1.0 / tau)                            # clock-time generator: each universe lives tau, then leaves f offspring
    ev2, V2 = np.linalg.eig(Gt); v2 = np.abs(np.real(V2[:, np.argmax(np.real(ev2))])); null = float(p[np.argmax(v2)])
    domain = float(p[np.argmax(f)])                                             # the generation-indexed branching process concentrates at argmax f under small mutation
    malthus = float(p[np.argmax((f - 1) / tau)])
    out = outcome(crr=crr, null=null, domain=domain, check=None)
    return make_row("cns", "an ensemble of universes on a 1-D parameter p: mean black-hole number f(p) = 2 exp(-(p - 0.3)^2 / 0.1) + 0.5, lifetime tau(p) = exp(1.5 p) (universes that make more black holes on the right take longer), mutation width 0.02",
                    source="smolin dossier 1d problem 4 ('a time is required to count generations'; the measure over generations)",
                    Q="counted in natural time (generations: one occasion per universe, D5; H-L5's 'change has its own clock'), the ensemble concentrates at the maximum of f, which is Smolin's fitness; counted in clock time it concentrates at the Malthusian optimum and the prediction moves",
                    ingredient="D5 (occasions: one universe = one occasion) with H-L5's natural time (count occasions, not clock time)",
                    null="the clock-time ensemble (continuous-time branching: the leading eigenvector of K f/tau - 1/tau)",
                    domain="the generation-indexed branching process (Galton-Watson, multitype): under small mutation its type distribution concentrates at argmax f",
                    numbers=f"ensemble mode: in generations {crr:.4f}, in clock time {null:.4f}; argmax f {domain:.4f}; argmax of the Malthusian rate (f - 1)/tau {malthus:.4f}",
                    tg=f"mode {crr:.4f} vs null {null:.4f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
                    tn=f"the generation theorem gives {domain:.4f}: {_w(rel(crr, domain) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
                    tc="not needed (the domain has Q)",
                    out=out,
                    reading=f"CNS's prediction depends on the clock that counts the ensemble: in generations the typical universe sits at the peak of black-hole number ({crr:.4f}), in clock time it moves to {null:.4f} whenever fitter universes are slower; CRR's natural time picks the generation count, which is what Smolin's fitness assumes but his measure problem leaves open; the number is branching-process theory's",
                    weakness="a toy landscape with an assumed lifetime trade-off; whether there is a clock time across universes at all is itself open (each universe has its own)",
                    elegance="If you count families by generations, the best parents win; if you count by the calendar, the fastest ones do.",
                    child="Some baby universes make lots of babies but take a long time; others make fewer but quickly. If you count by generations, the big families win. If you count by the clock, the quick ones win. CRR says count by generations.")


def main():
    return run_batch("Synthesis batch 30: Smolin (prompt-log entry 130; DECLARATION_29_30.md)", [r1(), r2(), r3()])


if __name__ == "__main__":
    sys.exit(main())
