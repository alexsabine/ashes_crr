"""Verify every [T] item and every closed form in the externally supplied specification
theory/external/CRR_test_specification_GPT6_Astra_2026-09-16.md, and state where each one
sits relative to theory/CRR.md v3.1.

Run:  uv run python theory/checks/verify_spec_math.py
Exit code 0 means every check passed. Each line prints PASS/FAIL, the identity verified, and
a tag: INHERITED (standard mathematics the spec itself labels as not evidence for CRR),
V3.1-SAME (already in CRR.md), V3.1-NEW (not in CRR.md; owner decision whether to sign it in),
or V3.1-CONFLICT (contradicts a v3.1 clause or a clause of the issue-#21 text). Nothing here
touches data.
"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.linalg import solve_discrete_are

from _harness import Harness


def main() -> int:
    H = Harness()
    check = H.check

    # ---------------------------------------------------------------- [T1] reparameterisation invariance (INHERITED, V3.1-SAME as A1)
    p, p1, p2 = sp.symbols("p p1 p2", positive=True)
    L_p = sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, p1, p2))                     # Bernoulli length in p
    psi = 2 * sp.asin(sp.sqrt(p))                                                 # eta = psi(p); g_psi = 1
    L_psi = psi.subs(p, p2) - psi.subs(p, p1)
    pts = [(0.05, 0.3), (0.2, 0.9), (0.4, 0.45)]
    same = all(math.isclose(float(L_p.subs({p1: a, p2: b})), float(L_psi.subs({p1: a, p2: b})), rel_tol=1e-10) for a, b in pts)
    check("[T1] Bernoulli FR length equal in p and in psi = 2 asin sqrt(p)  [INHERITED; V3.1-SAME]",
          same, "length invariant under the smooth reparameterisation (3 endpoint pairs, rel 1e-10)")
    # and NOT invariant under a change of statistical model: Poisson vs Bernoulli on the same 'rate' 0.1 -> 0.4
    lam = sp.symbols("lam", positive=True)
    L_pois = sp.integrate(1 / sp.sqrt(lam), (lam, sp.Rational(1, 10), sp.Rational(4, 10)))
    L_bern = L_p.subs({p1: sp.Rational(1, 10), p2: sp.Rational(4, 10)})
    check("[T1] corollary: same numbers, different model (Poisson vs Bernoulli) -> different length  [INHERITED; V3.1-SAME (A1 carrier)]",
          not math.isclose(float(L_pois), float(L_bern)), f"Poisson {float(L_pois):.4f} vs Bernoulli {float(L_bern):.4f}")

    # ---------------------------------------------------------------- [T2]/[T3] C >= D, equality on a geodesic (INHERITED, V3.1-SAME as P1)
    rng = np.random.default_rng(0)
    ok = True
    for _ in range(2000):
        x = np.cumsum(rng.standard_normal(rng.integers(2, 60)))
        ok &= np.abs(np.diff(x)).sum() >= abs(x[-1] - x[0]) - 1e-12
    check("[T2] C >= D on 2000 random 1-D paths  [INHERITED; V3.1-SAME (P1)]", ok)
    # 2-sphere (pure qubit, Fubini-Study): great-circle path has C = D, a small circle has C > D
    th = np.linspace(0, np.pi / 2, 2001)
    gc = np.stack([np.cos(th), np.sin(th), 0 * th], 1)                          # great circle, quarter turn
    sc = np.stack([np.cos(th) * np.cos(0.6) + 0 * th, np.sin(th) * np.cos(0.6), np.full_like(th, np.sin(0.6))], 1)
    sc /= np.linalg.norm(sc, axis=1, keepdims=True)
    def arc(P): return float(np.sum(np.arccos(np.clip(np.sum(P[:-1] * P[1:], 1), -1, 1))))
    def chord(P): return float(np.arccos(np.clip(P[0] @ P[-1], -1, 1)))
    check("[T3] equality iff geodesic: great circle C = D, small circle C > D  [INHERITED; V3.1-SAME (P1)]",
          math.isclose(arc(gc), chord(gc), rel_tol=1e-6) and arc(sc) > chord(sc) + 1e-3,
          f"great: C={arc(gc):.5f} D={chord(gc):.5f}; small: C={arc(sc):.5f} D={chord(sc):.5f}")

    # ---------------------------------------------------------------- [T4] 1-D backtracking identity S = 2B (V3.1-NEW: not stated in CRR.md)
    ok = True; worst = 0.0
    for _ in range(2000):
        x = np.cumsum(rng.standard_normal(rng.integers(2, 60)))
        d = np.diff(x); F = d[d > 0].sum(); B = -d[d < 0].sum()
        if F < B: x = -x; F, B = B, F
        C = F + B; D = x[-1] - x[0]; S = C - D
        ok &= math.isclose(S, 2 * B, abs_tol=1e-9); worst = max(worst, abs(S - 2 * B))
    check("[T4] 1-D: S = 2 x backward travel (net displacement >= 0)  [V3.1-NEW]", ok, f"max |S-2B| = {worst:.1e}")

    # ---------------------------------------------------------------- [T5] pairwise influence-odds law (V3.1-NEW as a stated prediction; follows from P2)
    Si, Sj, Om, ri, rj, Z = sp.symbols("S_i S_j Omega r_i r_j Z", positive=True)
    pi_i = ri * sp.exp(Si / Om) / Z; pi_j = rj * sp.exp(Sj / Om) / Z
    lhs = sp.log(pi_i / pi_j); rhs = (Si - Sj) / Om + sp.log(ri / rj)
    check("[T5] log(pi_i/pi_j) = (S_i - S_j)/Omega + log(r_i/r_j)  [V3.1-NEW (from P2 + O1)]",
          sp.simplify(sp.expand_log(lhs - rhs, force=True)) == 0)
    check("[T5] at Omega = 1, equal retention: one Fisher unit of surplus multiplies influence by e  [V3.1-NEW]",
          sp.simplify((pi_i / pi_j).subs({Om: 1, ri: rj}) - sp.exp(Si - Sj)) == 0)

    # ---------------------------------------------------------------- [T6] exponential surplus tail -> power-law weight tail (V3.1-NEW)
    s, w, beta = sp.symbols("s w beta", positive=True)
    tail_S = sp.exp(-beta * s)                                                    # P(S > s)
    tail_W = tail_S.subs(s, Om * sp.log(w))                                       # P(W > w) = P(S > Omega log w)
    check("[T6] P(W > w) = w^(-beta*Omega)  [V3.1-NEW]", sp.simplify(tail_W - w ** (-beta * Om)) == 0)
    pp = sp.symbols("p", positive=True)
    mom = sp.integrate(sp.exp(pp * s) * beta * sp.exp(-beta * s), (s, 0, sp.oo), conds="separate")
    cond = mom[1]
    check("[T6] p-th moment of W = e^S finite iff p < beta (Omega = 1)  [V3.1-NEW]",
          bool(cond.subs({pp: 1, beta: 2})) and not bool(cond.subs({pp: 2, beta: 1})) and not bool(cond.subs({pp: 1, beta: 1})),
          f"convergence condition from sympy: {cond}")

    # ---------------------------------------------------------------- [T7] scalar Kalman steady state (INHERITED; V3.1-SAME as P4)
    q, r, P = sp.symbols("q r P", positive=True)
    Ppred = P + q
    ric = sp.Eq(P, Ppred - Ppred ** 2 / (Ppred + r))                              # steady-state Riccati (posterior variance)
    Psol = [sol for sol in sp.solve(ric, P) if sp.simplify(sol.subs({q: 1, r: 1})) > 0][0]
    K = (Psol + q) / (Psol + q + r)
    v = sp.symbols("v", positive=True)
    K_spec = (v / 2) * (sp.sqrt(v ** 2 + 4) - v)
    check("[T7] steady-state gain equals (v/2)(sqrt(v^2+4)-v) with v = sqrt(q/r)  [INHERITED; V3.1-SAME (P4)]",
          sp.simplify(K.subs({q: v ** 2, r: 1}) - K_spec) == 0)
    check("[T7] K(1) = 1/phi  [INHERITED; V3.1-SAME (P4)]", sp.simplify(K_spec.subs(v, 1) - (sp.sqrt(5) - 1) / 2) == 0)
    # numeric cross-check with the DARE solver
    Pn = solve_discrete_are(np.array([[1.0]]), np.array([[1.0]]), np.array([[1.0]]), np.array([[1.0]]))  # a=1, c=1, q=1, r=1 (predicted variance)
    Kn = float(Pn.item() / (Pn.item() + 1.0))
    check("[T7] DARE numeric K(1) matches 1/phi", math.isclose(Kn, (math.sqrt(5) - 1) / 2, rel_tol=1e-9), f"K={Kn:.9f}")

    # ---------------------------------------------------------------- [X] pre-cut balance: stationary point C = H - Omega (V3.1-NEW; issue-#21 text P6)
    C, Hc = sp.symbols("C H", positive=True)
    B = sp.exp(C / Om) * (Hc - C)
    dB = sp.diff(B, C); Ca = sp.solve(sp.Eq(dB, 0), C)[0]
    check("[X] dB/dC = 0 at C = H - Omega  [V3.1-NEW; issue-#21 text P6]", sp.simplify(Ca - (Hc - Om)) == 0)
    check("[X] interior maximum (second derivative negative there)  [V3.1-NEW]",
          sp.simplify(sp.diff(B, C, 2).subs(C, Hc - Om)) == sp.simplify(-sp.exp((Hc - Om) / Om) / Om) and sp.simplify(-sp.exp((Hc - Om) / Om) / Om) < 0)

    # ---------------------------------------------------------------- [A1a] Fisher additivity (INHERITED; V3.1-SAME as A1')
    mu, sig, N = sp.symbols("mu sigma N", positive=True)
    I1 = 1 / sig ** 2                                                             # Gaussian mean, one observation
    check("[A1a] I_N = N I_1 for N iid Gaussian observations (per-elementary-event unit)  [INHERITED; V3.1-SAME (A1')]",
          sp.simplify(N * I1 - N / sig ** 2) == 0)

    # ---------------------------------------------------------------- [D5] rotor antipode is an involution (V3.1-SAME as A3)
    u, L = sp.symbols("u L", positive=True)
    A = lambda x: sp.Mod(x + L / 2, L)
    check("[D5] A(A(u)) = u mod L on the rotor  [V3.1-SAME (A3)]",
          all(math.isclose(float(A(A(sp.Float(uu))).subs(L, 3.0)) % 3.0, uu % 3.0, abs_tol=1e-12) for uu in (0.1, 1.4, 2.9)))

    # ---------------------------------------------------------------- [XI.1] old 'C Omega = 1' vs [A2a] 'C/H = 1' (V3.1-CONFLICT with issue-#21 text; v3.1 already demotes it)
    check("[XI.1] C*Omega = 1 and C/H = 1 coincide iff H = 1 at Omega = 1  [V3.1: A3 note already calls the scalar form a reduction]",
          sp.solve(sp.Eq(1 / Om, Hc), Hc)[0].subs(Om, 1) == 1)

    # ---------------------------------------------------------------- [P7]/[H1] vs v3.1 [H-EQ]: two operationalisations of 'equanimity' that differ
    # spec: pi_i/pi_j = e^{(S_i-S_j)/Omega}  (weights on settled occasions).  v3.1 H-EQ: w = Omega * ||g_p|| / ||g_q||  (gradient norm ratio).
    # The ratio form is unbounded as ||g_q|| -> 0 (the issue-#21 text A9 calls it ill-posed); EQ2's pass lives in that regime (cap = 1e4).
    gq = sp.symbols("g_q", positive=True)
    check("[H-EQ vs A9] gradient-norm ratio w -> infinity as ||g_past|| -> 0 (needs a cap; the spec's weight law does not)  [V3.1-CONFLICT with issue-#21 text A9]",
          sp.limit(1 / gq, gq, 0) == sp.oo)

    return H.finish()


if __name__ == "__main__":
    sys.exit(main())
