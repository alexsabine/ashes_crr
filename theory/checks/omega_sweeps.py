"""The Omega = 1 equanimity rule on existing mathematics (owner request 2026-09-22, prompt-log entry 69):
(1) Bayes: is Omega = 1 the Bayes-optimal combination of a present and a past batch? (conjugate Gaussian mean)
(2) the two-task quadratic model: fixed points of the rule, the knife edge either side of Omega = 1 with exact
    gradients, the stability edge of a fixed penalty weight, and the plateau that mini-batch noise, EMA smoothing
    and the ratio cap produce (the registered estimator of studies EQ2/EQ2R: smooth 0.9, cap 1e4, floor 1e-12)
(3) the Kalman filter: the tuned (Bayes) gain K(v) of P4 against the fixed gains the two readings of Omega = 1
    give (Fisher speed 1 -> K = 1/phi; equal pull -> K = 1/2), closed form and Monte Carlo.
Deterministic, no data. Every verdict word is computed from the numbers (R15). Pinned: theory/checks/omega_sweeps.txt.
Run: uv run python theory/checks/omega_sweeps.py
"""
import math

import numpy as np

OMEGA9 = (0.25, 0.35, 0.5, 0.71, 1.0, 1.41, 2.0, 2.83, 4.0)      # CLAUDE.md section 6 grid
SMOOTH = 0.9; WCAP = 1e4; DEN_FLOOR = 1e-12                         # registered estimator (EQ2, EQ2R)


def rule_w(ema_p, ema_q, omega, cap=WCAP):
    return min(omega * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), DEN_FLOOR), cap)


# ---------------------------------------------------------------- (1) Bayes
def part_bayes():
    print("[1] Bayes: a present batch (n_p samples, mean m_p) and a past batch (n_q samples, mean m_q) of a Gaussian mean with unit noise, flat prior")
    print("     log posterior = -n_p (theta - m_p)^2 / 2 - n_q (theta - m_q)^2 / 2; MAP theta_B = (n_p m_p + n_q m_q) / (n_p + n_q)")
    print("     with batch-MEAN gradients g_p = theta - m_p, g_q = theta - m_q, the combination g_p + w g_q has fixed point (m_p + w m_q)/(1 + w):")
    print("     it is the MAP iff w = n_q / n_p (each sample counted once: summed log-likelihoods, weight 1 each)")
    m_p, m_q = 0.0, 1.0
    for ratio in (0.25, 1.0, 4.0):
        n_p, n_q = 100, int(100 * ratio)
        theta_B = (n_p * m_p + n_q * m_q) / (n_p + n_q)
        w_B = n_q / n_p
        # the Omega rule with exact gradients: fixed points solve (theta - m_p) + Omega |theta - m_p|/|theta - m_q| (theta - m_q) = 0
        # between the means the two terms are antiparallel: the sum is (1 - Omega)(theta - m_p): zero for every theta iff Omega = 1
        ends = {}
        for om in (0.5, 1.0, 2.0):
            for th0 in (0.1, 0.5, 0.9):
                th = th0; ema_p = ema_q = None
                for _ in range(20000):
                    g_p, g_q = th - m_p, th - m_q
                    ema_p = g_p if ema_p is None else SMOOTH * ema_p + (1 - SMOOTH) * g_p
                    ema_q = g_q if ema_q is None else SMOOTH * ema_q + (1 - SMOOTH) * g_q
                    w = rule_w(np.array([ema_p]), np.array([ema_q]), om)
                    th = th - 0.05 * (g_p + w * g_q)
                ends[(om, th0)] = th
        print(f"     n_q/n_p = {ratio:g}: theta_B = {theta_B:.4f} (Bayes weight w_B = {w_B:g}); rule endpoints (exact gradients, registered estimator, lr 0.05, 20000 steps):")
        for om in (0.5, 1.0, 2.0):
            print(f"        Omega = {om:g}: from theta_0 = 0.1 -> {ends[(om, 0.1)]:.4f}, 0.5 -> {ends[(om, 0.5)]:.4f}, 0.9 -> {ends[(om, 0.9)]:.4f}"
                  + (f"   (|end - theta_B| = {abs(ends[(om, 0.1)] - theta_B):.4f}, {abs(ends[(om, 0.5)] - theta_B):.4f}, {abs(ends[(om, 0.9)] - theta_B):.4f})" if om == 1.0 else ""))
    stays = all(abs(ends[(1.0, t)] - t) < 1e-6 for t in (0.1, 0.5, 0.9))
    to_p = all(abs(ends[(0.5, t)] - m_p) < 1e-3 for t in (0.1, 0.5, 0.9))
    to_q = all(abs(ends[(2.0, t)] - m_q) < 0.2 for t in (0.1, 0.5, 0.9))
    print(f"     computed: at Omega = 1 the endpoint is the starting point (every theta between the means is a fixed point): {stays}; Omega = 0.5 ends at the present mean (within 1e-3): {to_p}; Omega = 2 ends within 0.2 of the past mean (it chatters there, where g_q vanishes and the ratio hits the floor): {to_q}")
    print("     so Omega = 1 is the Bayes optimum only when the trajectory happens to stop at theta_B, and the rule contains nothing that selects it; with equal counts the Bayes weight is w = 1 (ER-sum), the constant EQX found the rule reduced to")
    print()


# ---------------------------------------------------------------- (2) two-task quadratic model
def make_model(seed=0, d=5, mismatch=16.0):
    rng = np.random.default_rng(seed)
    H = np.diag(rng.uniform(0.5, 2.0, d)); F = mismatch * np.diag(rng.uniform(0.5, 2.0, d))
    a = rng.standard_normal(d); b = a + 1.5 * rng.standard_normal(d)
    return H, F, a, b


def pareto(H, F, a, b, lam):
    return np.linalg.solve(H + lam * F, H @ a + lam * F @ b)


def losses(H, F, a, b, th):
    return float(0.5 * (th - a) @ H @ (th - a)), float(0.5 * (th - b) @ F @ (th - b))


def lam_eff(H, F, a, b, th):
    """The fixed penalty weight whose equilibrium is nearest th (log grid)."""
    grid = np.logspace(-4, 6, 2001)
    d = [np.linalg.norm(pareto(H, F, a, b, l) - th) for l in grid]
    return float(grid[int(np.argmin(d))]), float(min(d))


def gd(H, F, a, b, mode, value, lr=0.05, steps=4000, noise=0.0, smooth=SMOOTH, cap=WCAP, seed=0, start=None):
    rng = np.random.default_rng(seed)
    th = (b if start is None else start).copy(); ema_p = ema_q = None; wlog = []
    for _ in range(steps):
        g_p = H @ (th - a) + noise * rng.standard_normal(len(th)); g_q = F @ (th - b) + noise * rng.standard_normal(len(th))
        if mode == "fixed":
            w = value
        else:
            ema_p = g_p if (ema_p is None or smooth == 0) else smooth * ema_p + (1 - smooth) * g_p
            ema_q = g_q if (ema_q is None or smooth == 0) else smooth * ema_q + (1 - smooth) * g_q
            w = rule_w(ema_p, ema_q, value, cap)
        wlog.append(w)
        th = th - lr * (g_p + w * g_q)
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6:
            return th, wlog, False
    return th, wlog, True


def part_quadratic():
    H, F, a, b = make_model()
    lr = 0.05
    print("[2] Two-task quadratic model: L_p = (theta - a)' H (theta - a)/2 (present), L_q = (theta - b)' F (theta - b)/2 (past penalty), d = 5, F 16x H (the gate's Fisher-scale mismatch); the learner starts at the past optimum b")
    print(f"     eigenvalues: H in [{np.diag(H).min():.3f}, {np.diag(H).max():.3f}], F in [{np.diag(F).min():.3f}, {np.diag(F).max():.3f}]; |a - b| = {np.linalg.norm(a - b):.4f}")
    # (i) fixed points
    print("     (i) fixed points of g_p + Omega (|g_p|/|g_q|) g_q = 0 need g_p and g_q antiparallel, i.e. theta on the Pareto curve theta(lambda) = (H + lambda F)^-1 (H a + lambda F b); there the update has norm |1 - Omega| |g_p| exactly:")
    for om in (0.9, 1.0, 1.1):
        rel = []
        for lam in np.logspace(-3, 3, 13):
            th = pareto(H, F, a, b, lam); g_p = H @ (th - a); g_q = F @ (th - b)
            rel.append(np.linalg.norm(g_p + om * np.linalg.norm(g_p) / np.linalg.norm(g_q) * g_q) / np.linalg.norm(g_p))
        print(f"        Omega = {om:g}: |update|/|g_p| over 13 points of the curve: min {min(rel):.6f}, max {max(rel):.6f} (|1 - Omega| = {abs(1 - om):.1f})")
    print("        computed: at Omega = 1 every point of the curve is stationary (a continuum of equilibria, one for every fixed lambda); off Omega = 1 none is")
    # (ii) stability edge of a fixed weight
    lam_edge = (2.0 / lr - np.diag(H).max()) / np.diag(F).max()
    print(f"     (ii) a fixed weight lambda diverges under gradient descent at lr {lr} when lr (h_max + lambda f_max) > 2: edge lambda* = {lam_edge:.4f}")
    grid = (0.01, 0.03, 0.1, 0.3, 1.0, 1.5, 3.0, 10.0)
    for lam in grid:
        th, _, ok = gd(H, F, a, b, "fixed", lam, lr=lr)
        Lp, Lq = losses(H, F, a, b, th) if ok else (float("nan"), float("nan"))
        print(f"        fixed lambda = {lam:5g}: {'converged' if ok else 'DIVERGED '} L_present {Lp:.4f} L_past {Lq:.4f} sum {Lp + Lq:.4f}")
    # (iii) the rule with exact gradients and instantaneous norms (no EMA): the knife edge
    Lp_b, Lq_a = losses(H, F, a, b, b)[0], losses(H, F, a, b, a)[1]     # present loss at the past optimum; past loss at the present optimum
    def label(Lp, Lq, dist, le):
        if dist < 1e-2: return f"on the curve at lambda_eff {le:.3g}"
        if Lp < 1e-2 * Lp_b: return "past dropped (at the present optimum)"
        if Lq < 1e-2 * Lq_a: return "present never learned (at the past optimum)"
        return "off the curve (oscillating)"
    print(f"     (iii) the rule with exact gradients and instantaneous norms (smooth 0), from the past optimum, 4000 steps; L_present at b = {Lp_b:.4f}, L_past at a = {Lq_a:.4f}:")
    lab = {}
    for om in OMEGA9:
        th, wlog, ok = gd(H, F, a, b, "eq", om, lr=lr, smooth=0.0)
        Lp, Lq = losses(H, F, a, b, th); le, dist = lam_eff(H, F, a, b, th); lab[om] = (label(Lp, Lq, dist, le), le)
        print(f"        Omega = {om:4g}: L_present {Lp:.4f} L_past {Lq:.4f} sum {Lp + Lq:.4f}; nearest fixed-lambda equilibrium lambda_eff = {le:.4g} (distance {dist:.2e}); median w {np.median(wlog):.4g} -> {lab[om][0]}")
    print("        computed: " + "; ".join(f"Omega {om:g}: {lab[om][0]}" for om in OMEGA9))
    if lab[1.0][0].startswith("on the curve"):
        print(f"        computed: at Omega = 1 the learner stops on the curve at lambda_eff = {lab[1.0][1]:.4g}, which is {'above' if lab[1.0][1] > lam_edge else 'below'} the stability edge {lam_edge:.4f} of a fixed weight")
    print("     (iii b) the same with the registered estimator (EMA 0.9 of the gradient vectors, cap 1e4):")
    for om in OMEGA9:
        th, wlog, ok = gd(H, F, a, b, "eq", om, lr=lr)
        Lp, Lq = losses(H, F, a, b, th); le, dist = lam_eff(H, F, a, b, th)
        print(f"        Omega = {om:4g}: L_present {Lp:.4f} L_past {Lq:.4f} sum {Lp + Lq:.4f}; lambda_eff {le:.4g} (distance {dist:.2e}); median w {np.median(wlog):.4g} -> {label(Lp, Lq, dist, le)}")
    # (iv) noise, smoothing and cap: the plateau
    print("     (iv) mini-batch noise (Gaussian, sd 'noise' on both gradients), registered estimator unless stated, 4000 steps, 5 seeds; total loss L_present + L_past per Omega (the equal-count Bayes objective); plateau = Omegas within 10 % of the best total:")
    widths = {}
    for noise in (0.0, 0.5, 2.0):
        for sm, cap in ((0.9, WCAP), (0.8, WCAP), (0.98, WCAP), (0.9, 100.0), (0.9, 10.0)):
            tot = {}; capfrac = []
            for om in OMEGA9:
                vals = []
                for s_ in range(5):
                    th, wlog, ok = gd(H, F, a, b, "eq", om, lr=lr, noise=noise, smooth=sm, cap=cap, seed=s_)
                    Lp, Lq = losses(H, F, a, b, th); vals.append(Lp + Lq if ok else float("inf")); capfrac.append(np.mean(np.array(wlog) >= cap))
                tot[om] = float(np.mean(vals))
            best = min(tot, key=tot.get)
            plateau = [om for om in OMEGA9 if tot[om] <= 1.1 * tot[best]]
            widths[(noise, sm, cap)] = (len(plateau), best, float(np.mean(capfrac)))
            print(f"        noise {noise:g} smooth {sm} cap {cap:g}: total loss " + " ".join(f"{om:g}:{tot[om]:.3f}" for om in OMEGA9) + f" | best Omega {best:g}; plateau {plateau}; w at cap in {np.mean(capfrac):.2e} of steps")
    print("        computed: plateau width (number of grid Omegas within 10 % of the best) by noise at the registered smoothing and cap: "
          + ", ".join(f"noise {n:g}: {widths[(n, 0.9, WCAP)][0]} (best {widths[(n, 0.9, WCAP)][1]:g})" for n in (0.0, 0.5, 2.0))
          + "; best Omega is 1 in " + f"{sum(1 for k, v in widths.items() if v[1] == 1.0)} of {len(widths)} cells"
          + f"; the cap binds in more than 1 % of steps in {sum(1 for v in widths.values() if v[2] > 0.01)} of {len(widths)} cells (median w here is of order 1; the EQ2 regime, tuned lambda in the hundreds and the cap load-bearing, is not this model's)")
    print()


# ---------------------------------------------------------------- (3) Kalman filter
def kalman_gain(v):
    return (v / 2.0) * (math.sqrt(v * v + 4.0) - v)


def mse_fixed_gain(K, q, r):
    """Steady-state error variance of a fixed-gain filter on the random walk x_{t+1} = x_t + w (var q), y = x + e (var r):
    P = ((1 - K)^2 (P + q) + K^2 r) -> P = ((1 - K)^2 q + K^2 r) / (1 - (1 - K)^2)."""
    return ((1 - K) ** 2 * q + K ** 2 * r) / (1 - (1 - K) ** 2)


def mc_fixed_gain(K, q, r, seed, n=200000):
    rng = np.random.default_rng(seed)
    x = 0.0; xh = 0.0; err = np.empty(n)
    w = math.sqrt(q) * rng.standard_normal(n); e = math.sqrt(r) * rng.standard_normal(n)
    for t in range(n):
        x += w[t]; y = x + e[t]
        xh = xh + K * (y - xh)                      # a priori estimate = last posterior (random walk); posterior after the update
        err[t] = xh - x
    return float(np.mean(err[n // 10:] ** 2))


def part_kalman():
    print("[3] Kalman filter, scalar random walk (process variance q, observation variance r), v = sqrt(q/r) the Fisher speed of P4")
    print("     tuned (Bayes-optimal) gain K(v) = (v/2)(sqrt(v^2 + 4) - v); fixed rules from the two readings of Omega = 1: Fisher speed 1 -> K(1) = 1/phi; equal pull (prior and datum with equal precision) -> K = 1/2")
    k_phi = kalman_gain(1.0); k_half = 0.5
    v_half = None
    # v at which the Bayes gain equals 1/2: (v/2)(sqrt(v^2+4) - v) = 1/2 -> v = 1/sqrt 2
    v_half = 1 / math.sqrt(2)
    print(f"     K(1) = {k_phi:.6f} (1/phi = {(math.sqrt(5) - 1) / 2:.6f}); K(v) = 1/2 at v = {v_half:.6f} (K({v_half:.4f}) = {kalman_gain(v_half):.6f})")
    print("     the normalised-gradient rule applied to the filter update (innovation pull and prior pull scaled to equal norm) is K = 1/2 at every v: a fixed gain, not an adaptive one")
    print("     steady-state MSE ratio fixed / tuned (closed form), P(K) = ((1-K)^2 q + K^2 r)/(1 - (1-K)^2), r = 1, q = v^2:")
    within5 = {"1/phi": [], "1/2": []}; within25 = {"1/phi": [], "1/2": []}
    for v in (0.01, 0.03, 0.1, 0.3, 0.5, 0.707, 1.0, 1.414, 2.0, 3.0, 10.0, 30.0, 100.0):
        q, r = v * v, 1.0
        P_t = mse_fixed_gain(kalman_gain(v), q, r); P_phi = mse_fixed_gain(k_phi, q, r); P_half = mse_fixed_gain(k_half, q, r)
        rp, rh = P_phi / P_t, P_half / P_t
        for name, ratio in (("1/phi", rp), ("1/2", rh)):
            if ratio <= 1.05: within5[name].append(v)
            if ratio <= 1.25: within25[name].append(v)
        print(f"        v = {v:7g}: K_tuned {kalman_gain(v):.4f} MSE {P_t:.4f}; K = 1/phi: ratio {rp:.4f}; K = 1/2: ratio {rh:.4f}")
    print(f"     computed: the 1/phi rule is within 5 % of the tuned filter for v in {within5['1/phi']} and within 25 % for v in {within25['1/phi']}; the 1/2 rule within 5 % for v in {within5['1/2']} and within 25 % for v in {within25['1/2']}")
    print("     Monte Carlo (200000 steps, seeds 0 and 1, first 10 % discarded) against the closed form:")
    for v in (0.3, 1.0, 3.0):
        q, r = v * v, 1.0
        for name, K in (("tuned", kalman_gain(v)), ("1/phi", k_phi), ("1/2", k_half)):
            mc = [mc_fixed_gain(K, q, r, s) for s in (0, 1)]
            print(f"        v = {v:g} K = {name:5s} ({K:.4f}): closed form {mse_fixed_gain(K, q, r):.4f}, Monte Carlo {mc[0]:.4f} {mc[1]:.4f}")
    print("     the tuned gain needs q/r; an innovation-based estimator (Mehra 1970, named, not fetched) supplies it from the data; the fixed rules do not, and lose everywhere but at one speed each")
    print()


def main():
    print("Omega = 1 on existing mathematics (2026-09-22, prompt-log entry 69): Bayes, the two-task quadratic, the Kalman filter")
    print()
    part_bayes(); part_quadratic(); part_kalman()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
