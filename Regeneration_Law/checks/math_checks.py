"""The mathematics of the regeneration law (CRR 2.0), declared in Regeneration_Law/DECLARATION_1.md (pushed in f5f3647
before this file existed). Prompt-log entry 137. No data. Deterministic.
Run: uv run python Regeneration_Law/checks/math_checks.py > Regeneration_Law/checks/math_checks.txt"""
import math
import sys

import numpy as np
import sympy as sp
from scipy.optimize import minimize


def K(v):
    v = np.asarray(v, float); return (v / 2.0) * (np.sqrt(v * v + 4.0) - v)


def ewma_state_var(alpha, s_eta, s_eps):
    """Stationary variance of d = level - EWMA estimate for a local-level environment (derivation in M3)."""
    return ((1 - alpha) ** 2 * s_eta ** 2 + alpha ** 2 * s_eps ** 2) / (1 - (1 - alpha) ** 2)


def mom_v(y):
    """Method-of-moments local-level fit on first differences: var(dy) = s_eta^2 + 2 s_eps^2, cov(dy_t, dy_{t-1}) = -s_eps^2.
    Returns (v_hat, s_eta2_hat, s_eps2_hat); a non-positive drift variance gives v_hat = 0 (counted by callers)."""
    d = np.diff(np.asarray(y, float)); d = d - d.mean()
    g0 = float(np.mean(d * d)); g1 = float(np.mean(d[1:] * d[:-1]))
    s_eps2 = max(-g1, 0.0); s_eta2 = g0 - 2 * s_eps2
    if s_eta2 <= 0 or s_eps2 <= 0: return 0.0 if s_eta2 <= 0 else float("inf"), s_eta2, s_eps2
    return math.sqrt(s_eta2 / s_eps2), s_eta2, s_eps2


def ll_negloglik(params, y):
    q, r = math.exp(params[0]), math.exp(params[1]); m, P = y[0], r * 10.0; nll = 0.0
    for t in range(1, len(y)):
        P = P + q; S = P + r; e = y[t] - m; nll += 0.5 * (math.log(2 * math.pi * S) + e * e / S)
        k = P / S; m = m + k * e; P = (1 - k) * P
    return nll


def ml_v(y):
    y = np.asarray(y, float); v0 = np.var(np.diff(y))
    res = minimize(ll_negloglik, x0=[math.log(v0 / 3), math.log(v0 / 3)], args=(y,), method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-8, maxiter=4000))
    q, r = math.exp(res.x[0]), math.exp(res.x[1]); return math.sqrt(q / r)


def alpha_hat(s, y):
    """Least squares for s_t = s_{t-1} + alpha (y_t - s_{t-1}) + noise, through the origin."""
    s = np.asarray(s, float); y = np.asarray(y, float); x = y[1:] - s[:-1]; z = s[1:] - s[:-1]
    return float(np.dot(x, z) / np.dot(x, x))


def simulate(n, s_eta, s_eps, alpha, s_rep, seed, phi=1.0):
    rng = np.random.default_rng(seed); mu = np.zeros(n); y = np.zeros(n); s = np.zeros(n)
    for t in range(1, n):
        mu[t] = phi * mu[t - 1] + s_eta * rng.normal()
    y = mu + s_eps * rng.normal(size=n)
    for t in range(1, n): s[t] = s[t - 1] + alpha * (y[t] - s[t - 1])
    return y, s + s_rep * rng.normal(size=n)


def main():
    print("Regeneration law (CRR 2.0): mathematical checks (Regeneration_Law/DECLARATION_1.md)")
    ok_all = True
    # M1
    vv = sp.symbols("v", positive=True); P = (vv ** 2 + vv * sp.sqrt(vv ** 2 + 4)) / 2    # steady prior variance in units of R: P^2 - Q P - Q R = 0, Q = v^2 R
    Kr = P / (P + 1); Kc = (vv / 2) * (sp.sqrt(vv ** 2 + 4) - vv)
    cross = sp.simplify(sp.expand(2 * (vv ** 2 + vv * sp.sqrt(vv ** 2 + 4)) - (vv * sp.sqrt(vv ** 2 + 4) - vv ** 2) * (vv ** 2 + vv * sp.sqrt(vv ** 2 + 4) + 2)))
    riccati = sp.simplify(P ** 2 - vv ** 2 * P - vv ** 2)
    grid = np.array([0.01, 0.1, 0.5, 1.0, 2.0, 10.0]); num = max(abs(float(Kr.subs(vv, g)) - float(K(g))) for g in grid)
    m1 = cross == 0 and riccati == 0 and num < 1e-12; ok_all &= m1
    print(f"M1 steady-state Kalman gain: Riccati residual {riccati}, cross-multiplied identity residual {cross}, max numeric difference {num:.1e} -> {'holds' if m1 else 'FAILS'}")
    # M2
    m2 = abs(float(K(1.0)) - (math.sqrt(5) - 1) / 2) < 1e-15; ok_all &= m2
    print(f"M2 K(1) = {float(K(1.0)):.15f}, 1/phi = {(math.sqrt(5) - 1) / 2:.15f} -> {'holds' if m2 else 'FAILS'}")
    # M3
    al = np.arange(1e-4, 1.0, 1e-4); worst = 0.0; parts = []
    for v in (0.05, 0.2, 1.0, 3.0):
        V = ewma_state_var(al, v, 1.0); a_opt = float(al[np.argmin(V)]); worst = max(worst, abs(a_opt - float(K(v)))); parts.append(f"v {v}: argmin {a_opt:.4f}, K {float(K(v)):.4f}")
    m3 = worst < 1e-3; ok_all &= m3
    print(f"M3 Muth: the EWMA weight minimising the stationary error equals K(v): " + "; ".join(parts) + f" -> {'holds' if m3 else 'FAILS'}")
    # M4
    parts = []; vE = 0.3
    for r in (0.0, 0.5, 1.0, 2.0):
        v_own = vE / math.sqrt(1 + r * r / 12); parts.append(f"delta/s_eps {r}: v_own {v_own:.4f}, alpha* {float(K(v_own)):.4f} (instrument unit {float(K(vE)):.4f})")
    print("M4 the own unit (reporting quantum delta): " + "; ".join(parts) + " -> the own unit lowers alpha* whenever delta > 0 (load-bearing where delta is comparable to s_eps)")
    # M5
    lo, hi = float(K(1e-9)), float(K(1e9))
    print(f"M5 limits: K(1e-9) = {lo:.3e} (q -> 1, the accumulated count A6 forbids: the law and A6 conflict only at v = 0), K(1e9) = {hi:.9f} (no memory); q < 1 for every v > 0: {'holds' if 0 < lo < 1 else 'FAILS'}")
    # M6
    k0 = 0.3; w = k0 * (1 - k0) ** np.arange(0, 2000); mean_age = float(np.sum(np.arange(0, 2000) * w) / np.sum(w)); m6 = abs(mean_age - (1 - k0) / k0) < 1e-9; ok_all &= m6
    print(f"M6 P3: mean age of the weights at K = {k0}: {mean_age:.10f}, (1 - K)/K = {(1 - k0) / k0:.10f} -> {'holds' if m6 else 'FAILS'}")
    # M7
    vh = float(sp.nsolve(Kc - sp.Rational(1, 2), vv, 0.7))
    print(f"M7 equal pull (H-EQ, Omega = 1) needs K = 1/2: at v = {vh:.6f} (1/sqrt 2 = {1 / math.sqrt(2):.6f}); pull ratio datum:past = K/(1-K) is 1 only there (e.g. v = 0.1: {float(K(0.1)) / (1 - float(K(0.1))):.4f}; v = 3: {float(K(3.0)) / (1 - float(K(3.0))):.4f}) -> the law is not H-EQ; O1's 'at Omega = 1' cannot be kept")
    # M8
    phi, s_eta, s_eps = 0.7, 1.0, 1.0
    Pp = 1.0
    for _ in range(10000): Pp = phi ** 2 * (Pp - Pp ** 2 / (Pp + s_eps ** 2)) + s_eta ** 2
    k_ar = Pp / (Pp + s_eps ** 2)
    y, _s = simulate(20000, s_eta, s_eps, 0.5, 0.0, 808, phi=phi); vhat = mom_v(y)[0]
    print(f"M8 scope: AR(1) environment (phi {phi}, s_eta {s_eta}, s_eps {s_eps}): optimal steady gain {k_ar:.4f}; local-level fit v_hat {vhat:.4f} -> K(v_hat) {float(K(vhat)):.4f}; relative difference {abs(float(K(vhat)) - k_ar) / k_ar:.3f} (the random-walk approximation is part of the law's operationalisation)")
    # M9
    print("M9 estimator recovery (v_true 0.3, alpha_true = K(0.3), system report noise 0.05 s_eps; 50 seeds each):")
    vt = 0.3; at = float(K(vt))
    for n in (170, 200, 500, 2500):
        vm, va, am = [], [], []
        for sd in range(50):
            y, s = simulate(n, vt, 1.0, at, 0.05, 9000 + sd); vm.append(mom_v(y)[0]); am.append(alpha_hat(s, y))
            if n <= 500 and sd < 10: va.append(ml_v(y))
        vm, am = np.array(vm), np.array(am); nz = int(np.sum(vm == 0))
        print(f"   n {n}: alpha_hat mean {am.mean():.4f} (true {at:.4f}, bias {(am.mean() - at) / at:+.3f}, sd {am.std():.4f}); v_hat (moments) median {np.median(vm):.4f} (true {vt}), zero-drift estimates {nz}/50; "
              + (f"v_hat (ML, 10 seeds) median {np.median(va):.4f}; " if va else "") + f"K(v_hat) median {float(np.median(K(vm))):.4f}")
    # M10
    y, s = simulate(2500, vt, 1.0, at, 0.05, 4242); c = 7.3
    m10 = abs(mom_v(y)[0] - mom_v(c * y)[0]) < 1e-9 and abs(alpha_hat(s, y) - alpha_hat(c * s, c * y)) < 1e-12; ok_all &= m10
    print(f"M10 unit invariance under rescaling by {c}: v_hat and alpha_hat unchanged -> {'holds' if m10 else 'FAILS'}")
    print(f"summary: identities M1, M2, M3, M6, M10 {'all hold' if ok_all else 'NOT all hold'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
