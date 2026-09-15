"""Verify the closed forms used in theory/SCOPE.md (proposed P6–P9 and the
convex-learner lemma behind gate_T1). Companion to verify_math.py, kept
separate because these propositions are not yet in theory/CRR.md: they are
candidates for v3.1 and must not be read as canonical until merged.

Run:  uv run python theory/checks/verify_scope_math.py
Exit code 0 means every check passed. Nothing here touches data.

The check/FAILS scaffolding is shared with verify_math.py via _harness.py;
main() returns the process exit code.
"""
import sys

import numpy as np
import sympy as sp

from _harness import Harness


def main() -> int:
    H = Harness()
    check = H.check

    # ---------------------------------------------------------------- P6 (proposed)
    # Poisson family: g(lambda) = 1/lambda, so the FR distance is 2|sqrt(l2) - sqrt(l1)|.
    l1, l2, lam = sp.symbols("l1 l2 lam", positive=True)
    d_pois = sp.integrate(1 / sp.sqrt(lam), (lam, l1, l2))
    check("P6: Poisson FR distance = 2(sqrt(l2) - sqrt(l1))",
          sp.simplify(d_pois - 2 * (sp.sqrt(l2) - sp.sqrt(l1))) == 0, str(sp.simplify(d_pois)))
    # and sqrt(2 KL) agrees with it to second order in the step
    delta = sp.symbols("delta", real=True)
    KL_pois = l1 * sp.log(l1 / (l1 + delta)) - l1 + (l1 + delta)
    lhs = sp.series(sp.sqrt(2 * KL_pois), delta, 0, 2).removeO()
    rhs = sp.series(2 * (sp.sqrt(l1 + delta) - sp.sqrt(l1)), delta, 0, 2).removeO()
    check("P6: sqrt(2 KL) = FR distance to first order in the step (Poisson)",
          sp.simplify(lhs - rhs) == 0, f"lhs={lhs}, rhs={rhs}")

    # ---------------------------------------------------------------- P7 (proposed)
    # Categorical family on the simplex: FR distance = 2 arccos(sum sqrt(p_i q_i)).
    # Verified against the Bernoulli line integral of 1/sqrt(p(1-p)).
    p, q = sp.symbols("p q", positive=True)
    d_line = sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, p, q))  # 2 asin(sqrt q) - 2 asin(sqrt p)
    d_bhat = 2 * sp.acos(sp.sqrt(p * q) + sp.sqrt((1 - p) * (1 - q)))
    rng = np.random.default_rng(0)
    worst = 0.0
    for _ in range(200):
        a, b = np.sort(rng.uniform(0.02, 0.98, 2))
        worst = max(worst, abs(float(d_line.subs({p: a, q: b})) - float(d_bhat.subs({p: a, q: b}))))
    check("P7: categorical FR distance = 2 arccos(Bhattacharyya) (Bernoulli check, 200 pairs)",
          worst < 1e-9, f"max |diff|={worst:.2e}")
    check("P7: simplex diameter = pi (opposite vertices)", abs(2 * np.arccos(0.0) - np.pi) < 1e-12)

    # ---------------------------------------------------------------- P8 (proposed)
    # Fixed-variance Gaussian: sqrt(2 KL) = |mu1 - mu2| / sigma EXACTLY (not only to
    # second order). This is the predictive family of a linear regression model.
    m1, m2, sg = sp.symbols("m1 m2 sigma", real=True)
    KL_g = (m1 - m2) ** 2 / (2 * sg**2)
    check("P8: sqrt(2 KL) = |Delta mu| / sigma exactly for fixed-variance Gaussians",
          sp.simplify(sp.sqrt(2 * KL_g) - sp.Abs(m1 - m2) / sp.Abs(sg)) == 0)

    # ---------------------------------------------------------------- P9 (proposed)
    # On a 1-D carrier with metric g(x) > 0, FR arc = total variation of y = int sqrt(g).
    # So a "Fisher arc" of a 1-D trace is a total variation after a fixed
    # reparametrisation, and differs from the identity-metric arc only through it.
    rng = np.random.default_rng(1)
    x = np.abs(np.cumsum(rng.standard_normal(500))) + 1.0  # positive trace (a rate)
    tv_ident = np.abs(np.diff(x)).sum()
    # Poisson metric g = 1/x  ->  y = 2 sqrt(x)
    tv_fisher = np.abs(np.diff(2 * np.sqrt(x))).sum()
    # midpoint quadrature of int sqrt(g(x)) |dx| with each sample step subdivided 200x
    sub = np.linspace(0, 1, 201)
    xf = (x[:-1, None] + np.diff(x)[:, None] * sub[None, :]).ravel()
    mid = 0.5 * (xf[1:] + xf[:-1])
    quad = (np.abs(np.diff(xf)) / np.sqrt(mid)).sum()
    check("P9: 1-D Poisson-metric arc = TV(2 sqrt x) (refined quadrature agrees to 1e-5 rel.)",
          abs(quad - tv_fisher) / tv_fisher < 1e-5, f"TV_id={tv_ident:.2f} TV_fisher={tv_fisher:.2f} quad={quad:.4f}")
    check("P9: identity and Fisher 1-D arcs are NOT proportional (ratio varies across segments)",
          np.std([np.abs(np.diff(x[i:i + 50])).sum() / np.abs(np.diff(2 * np.sqrt(x[i:i + 50]))).sum()
                  for i in range(0, 450, 50)]) > 1e-3)

    # ---------------------------------------------------------------- Convex-learner lemma (gate_T1)
    # Linear model, squared loss, task-A optimum theta_0, fixed-variance Gaussian
    # predictive on the task-A probe X_A. Then forgetting on that probe is
    #     F(theta) = L_A(theta) - L_A(theta_0) = (1/n)||X_A (theta - theta_0)||^2
    # and the endpoint KL on the same probe is E_old = ||X_A (theta - theta_0)||^2 / (2 n s^2),
    # so F = 2 s^2 E_old exactly: the endpoint on the old probe is a SUFFICIENT
    # statistic for forgetting and no path quantity can beat it. This is why
    # H-T1 must FAIL on S-H, and why E_old (not only E_new) is a required baseline.
    rng = np.random.default_rng(2)
    n, d = 200, 20
    XA = rng.standard_normal((n, d)); thA = rng.standard_normal(d)
    yA = XA @ thA + 0.3 * rng.standard_normal(n)
    th0 = np.linalg.lstsq(XA, yA, rcond=None)[0]
    worst = 0.0
    for _ in range(100):
        th = th0 + rng.standard_normal(d) * rng.uniform(0.1, 2.0)
        F = np.mean((XA @ th - yA) ** 2) - np.mean((XA @ th0 - yA) ** 2)
        E_old = np.mean((XA @ th - XA @ th0) ** 2) / 2.0  # s^2 = 1
        worst = max(worst, abs(F - 2 * E_old) / max(F, 1e-12))
    check("Lemma: F = 2 s^2 E_old exactly for a linear model at its task-A optimum (100 endpoints)",
          worst < 1e-9, f"max rel. diff={worst:.2e}")

    return H.finish()


if __name__ == "__main__":
    sys.exit(main())
