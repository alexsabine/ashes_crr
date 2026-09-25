"""The Cramer-Rao reading of C*Omega = 1 (prompt-log entry 207).

Declared in docs/notes/2026-09-25_cramer_rao_declaration.md (pushed at 052c2fc before this script existed).
Synthetic families only; deterministic; no data, no study, no ledger row.
Run: uv run python theory/checks/cramer_rao_reading.py
"""
import numpy as np
from scipy.stats import norm

from crr.instrument.core import arc_length, chord

CUT_TOL = 1e-9       # the scalar rule fires when the arc since the last cut reaches 1/Omega - CUT_TOL (float guard)
AT_MODE = 0.01       # CR6: "at the Bayes mode" means within 0.01 Cramer-Rao units (fixed with the script, before its run)


def verdict(ok):
    return 'HOLDS' if ok else 'FAILS'


def cr1():
    print('[CR1] the unit: Gaussian location N(theta, s^2), n data, sigma = 1/sqrt(n I) = s/sqrt(n)')
    s, delta = 2.0, 3.0
    path = np.linspace(0.0, delta, 1001)
    oks = []
    for n in (1, 2, 4):
        c = arc_length(path, sigma=s / np.sqrt(n))
        want = delta * np.sqrt(n) / s
        oks.append(abs(c - want) < 1e-12)
        print(f'     n = {n}: arc {c:.12f} Cramer-Rao steps; |delta| sqrt(n I) = {want:.12f}; '
              f'difference {abs(c - want):.1e}')
    ratio = arc_length(path, sigma=s / np.sqrt(2)) / arc_length(path, sigma=s)
    print(f'     count at n = 2 over n = 1: {ratio:.12f} (sqrt 2 = {np.sqrt(2):.12f}; Fisher additivity)')
    print(f'     {verdict(all(oks) and abs(ratio - np.sqrt(2)) < 1e-12)}: on a monotone path the arc in the '
          'Cramer-Rao unit is the number of standard errors travelled')


def fr_bern(p0, p1):
    return 2.0 * abs(np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p0)))


def local_steps(p):
    mid = 0.5 * (p[1:] + p[:-1])
    return float(np.sum(np.abs(np.diff(p)) / np.sqrt(mid * (1.0 - mid))))


def cr2():
    print('[CR2] a varying information: Bernoulli family, I(p) = 1/(p(1-p))')
    L = fr_bern(0.1, 0.9)
    errs = []
    for N in (10, 100, 1000, 10000):
        c = local_steps(np.linspace(0.1, 0.9, N + 1))
        errs.append(abs(c - L))
        print(f'     monotone 0.1 -> 0.9, {N:5d} steps: sum of local Cramer-Rao steps {c:.10f}; '
              f'Fisher-Rao length {L:.10f}; error {errs[-1]:.2e}')
    conv = all(a > b for a, b in zip(errs, errs[1:])) and errs[-1] < 1e-6
    p = np.concatenate([np.linspace(0.1, 0.9, 10001), np.linspace(0.9, 0.5, 5001)[1:]])
    c_arc = local_steps(p)
    c_ch = fr_bern(0.1, 0.5)
    print(f'     non-monotone 0.1 -> 0.9 -> 0.5: arc {c_arc:.6f} steps; chord (Fisher-Rao distance 0.1 to 0.5) '
          f'{c_ch:.6f}; surplus {c_arc - c_ch:.6f}')
    print(f'     {verdict(conv and c_arc > c_ch)}: the arc counts local resolvable steps exactly in the limit; it equals the '
          'distance from the start (C = C*) only on the monotone segment (P1)')


def cr3():
    print('[CR3] what one step means: two equal-variance Gaussians at Fisher distance d')
    for d in (0.5, 1.0, 2.0, 4.54):
        print(f'     d = {d:4}: KL = d^2/2 = {d * d / 2:.4f} nats; equal-prior Bayes error Phi(-d/2) = {norm.cdf(-d / 2):.4f}')
    e1 = norm.cdf(-0.5)
    print(f'     {verdict(abs(e1 - 0.3085) < 5e-5)}: one Cramer-Rao step is a change barely resolvable from the data the unit '
          f'was defined on (error {e1:.4f} against 0.5 for a coin); a detection threshold, not a bound on travel')


def scalar_rule(x, sigma, omega):
    step = np.abs(np.diff(x)) / sigma
    acc, cuts = 0.0, []
    for i, st in enumerate(step):
        acc += st
        if acc >= 1.0 / omega - CUT_TOL:
            cuts.append(i + 1)
            acc = 0.0
    return cuts


def cr4():
    print('[CR4] the removed rule "cut when the arc since the last cut reaches 1/Omega" on one antipodal half-turn')
    M = 20000
    t = np.linspace(0.0, 1.0, M + 1)
    ok_clean = True
    for rho in (1.0, 2.0, 4.54):
        x = 0.5 * rho * (1.0 - np.cos(np.pi * t))    # monotone half-turn, extent rho units (sigma = 1)
        for om in (0.5, 1.0, 2.0):
            cuts = scalar_rule(x, 1.0, om)
            at_antipode = len(cuts) == 1 and abs(cuts[0] - M) <= 1
            want = int(np.floor(rho * om + CUT_TOL))
            ok_clean &= abs(len(cuts) - want) <= 1 and (at_antipode == (abs(rho * om - 1.0) < 1e-12))
            print(f'     noise-free rho {rho:4}, Omega {om:3}: {len(cuts)} cuts per half-turn; rho Omega = {rho * om:.2f}; '
                  f'the single cut falls on the antipode: {at_antipode}')
    rng = np.random.default_rng(0)
    Mn = 200
    tn = np.linspace(0.0, 1.0, Mn + 1)
    ok_noisy = True
    for rho in (1.0, 4.54):
        x = 0.5 * rho * (1.0 - np.cos(np.pi * tn)) + rng.normal(0.0, 0.02, Mn + 1)
        C, Cs = arc_length(x), chord(x)
        for om in (0.5, 1.0, 2.0):
            n = len(scalar_rule(x, 1.0, om))
            want = int(np.floor(om * C))
            ok_noisy &= want - 1 <= n <= want
            print(f'     noise sd 0.02, rho {rho:4}, Omega {om:3}: C {C:.4f}, C* {Cs:.4f}, S {C - Cs:.4f}; '
                  f'{n} cuts; Omega C = {om * C:.2f}')
    print(f'     {verdict(ok_clean and ok_noisy)}: the rule is a Cramer-Rao step counter; monotone, it fires floor(rho Omega) '
          'times and lands on the antipode only where rho Omega = 1; with noise it fires about Omega C = Omega (C* + S) times')


def gls(F_B, b_B, F_pen, theta_A, lam):
    return np.linalg.solve(F_B + lam * F_pen, b_B + lam * F_pen @ theta_A)


def cr_units(dtheta, F):
    return float(np.sqrt(dtheta @ F @ dtheta))


def setup():
    rng = np.random.default_rng(1)
    d, s = 3, 0.5
    theta_true = np.array([1.0, -2.0, 0.5])
    X_A = rng.normal(size=(40, d)) * np.array([1.0, 0.3, 2.0])
    X_B = rng.normal(size=(40, d)) * np.array([0.4, 1.5, 1.0])
    y_A = X_A @ theta_true + rng.normal(0.0, s, 40)
    y_B = X_B @ (theta_true + np.array([0.8, 0.4, -0.6])) + rng.normal(0.0, s, 40)
    F_A, F_B = X_A.T @ X_A / s**2, X_B.T @ X_B / s**2
    theta_A = np.linalg.solve(F_A, X_A.T @ y_A / s**2)
    b_B = X_B.T @ y_B / s**2
    theta_AB = np.linalg.solve(F_A + F_B, X_A.T @ y_A / s**2 + b_B)
    return F_A, F_B, b_B, theta_A, theta_AB


def cr5():
    print('[CR5] the Laplace weight: Gaussian linear model, known noise, task A then task B, flat prior')
    F_A, F_B, b_B, theta_A, theta_AB = setup()
    F_AB = F_A + F_B
    th1 = gls(F_B, b_B, F_A, theta_A, 1.0)
    e1 = cr_units(th1 - theta_AB, F_AB)
    print(f'     true Fisher, lambda = 1: distance from the sequential-Bayes mode {e1:.2e} Cramer-Rao units (A+B)')
    lams = np.logspace(-2, 2, 4001)
    ok = e1 < 1e-10
    for c in (0.1, 1.0, 10.0):
        dist = [cr_units(gls(F_B, b_B, c * F_A, theta_A, l) - theta_AB, F_AB) for l in lams]
        best = lams[int(np.argmin(dist))]
        at1 = cr_units(gls(F_B, b_B, c * F_A, theta_A, 1.0) - theta_AB, F_AB)
        ok &= abs(np.log(best * c)) <= np.log(lams[1] / lams[0]) + 1e-12
        print(f'     Fisher scaled by c = {c:4}: best lambda {best:.4f} (1/c = {1 / c:.4f}); '
              f'lambda = 1 misses the mode by {at1:.4f} Cramer-Rao units')
    print(f'     {verdict(ok)}: the penalty in Cramer-Rao units with weight 1 is exact Bayes; with a mis-scaled Fisher the right '
          'weight is 1/c, so weight 1 is right only when the unit is right (what SEC calibrates)')


def cr6():
    print('[CR6] the H-EQ rule at Omega = 1 on the same model: w = |g_B| / |g_past|, past term the true-Fisher penalty')
    F_A, F_B, b_B, theta_A, theta_AB = setup()
    F_AB = F_A + F_B
    lr = 0.5 / np.linalg.eigvalsh(F_AB).max()
    th = theta_A.copy()
    for _ in range(20000):
        g_B = F_B @ th - b_B
        g_p = F_A @ (th - theta_A)
        n_p = np.linalg.norm(g_p)
        past = np.zeros_like(th) if n_p == 0.0 else np.linalg.norm(g_B) * g_p / n_p   # w * g_past, w = |g_B|/|g_past|
        th = th - lr * (g_B + past)
    g_B = F_B @ th - b_B
    g_p = F_A @ (th - theta_A)
    cos = float(g_B @ g_p / (np.linalg.norm(g_B) * np.linalg.norm(g_p)))
    dist = cr_units(th - theta_AB, F_AB)
    lab = 'AT THE MODE' if dist < AT_MODE else 'OFF THE MODE'
    print(f'     after 20000 steps: cos(g_B, g_past) = {cos:.6f} (-1 on the Pareto set); |g_B| / |g_past| = '
          f'{np.linalg.norm(g_B) / np.linalg.norm(g_p):.6f}; distance from the Bayes mode {dist:.4f} Cramer-Rao units: {lab}')
    print(f'     {verdict(cos < -0.999 and dist >= AT_MODE)}: the rule stops on the Pareto set where the two gradients are '
          'opposed, not at the Bayes point; the Cramer-Rao reading gives its Omega = 1 no meaning')


def main():
    print('Cramer-Rao reading of C*Omega = 1 (docs/notes/2026-09-25_cramer_rao_declaration.md)')
    for f in (cr1, cr2, cr3, cr4, cr5, cr6):
        f()


if __name__ == '__main__':
    main()
