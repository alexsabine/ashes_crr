"""Identity checks: the Omega = 1 rule against two-objective Pareto methods (MGDA, IMTL-G). Deterministic; no verdict.

Standard linear algebra, printed so the literature note of 2026-09-25 (prompt-log entry 176) quotes a committed script (R1).
For two gradients g_p (present) and g_q (past), with unit vectors u = g/|g|:
  [1] the rule's direction at Omega = 1, g_p + (|g_p|/|g_q|) g_q, equals |g_p| (u_p + u_q): the bisector of the two
      unit gradients;
  [2] that direction has equal projections on u_p and u_q: the IMTL-G condition ("impartial"), for two tasks;
  [3] MGDA's min-norm convex combination applied to the unit gradients is (u_p + u_q)/2: the same direction;
      MGDA on the raw gradients is not (it weights toward the shorter gradient);
  [4] on the Pareto curve of two quadratics (g_q = -g_p/lambda) all of them vanish: every Pareto point is stationary
      for the rule at Omega = 1, for IMTL-G and for MGDA, while the rule at Omega != 1 leaves (1 - Omega) g_p;
  [5] the step lengths differ: the rule keeps |g_p| as its scale; normalised MGDA and IMTL-G (unit weights) do not.
"""
import numpy as np


def rule(gp, gq, omega=1.0):
    return gp + omega * np.linalg.norm(gp) / np.linalg.norm(gq) * gq


def mgda2(g1, g2):
    """Min-norm point of the segment {a g1 + (1-a) g2, a in [0,1]} (closed form for two vectors)."""
    d = g1 - g2; den = float(d @ d)
    a = 0.5 if den == 0 else float(np.clip((g2 - g1) @ g2 / den, 0.0, 1.0))
    return a * g1 + (1 - a) * g2, a


def imtl_g2(g1, g2):
    """IMTL-G for two tasks: weights a, 1-a (sum 1) so that the aggregate has equal projections on u1 and u2."""
    u1, u2 = g1 / np.linalg.norm(g1), g2 / np.linalg.norm(g2)
    den = float((g1 - g2) @ (u1 - u2))
    a = float(g2 @ (u2 - u1) / den)
    return a * g1 + (1 - a) * g2, a


def cosang(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na > 0 and nb > 0 else float("nan")


def main():
    rng = np.random.default_rng(20260925)
    print("Pareto identities: the Omega = 1 rule against MGDA and IMTL-G (two objectives); standard algebra, no verdict")
    worst = dict(bis=0.0, proj=0.0, mgda_u=0.0, imtl=0.0)
    mgda_raw_cos = []
    for _ in range(1000):
        d = int(rng.integers(2, 12)); gp = rng.normal(size=d) * 10 ** rng.uniform(-3, 3); gq = rng.normal(size=d) * 10 ** rng.uniform(-3, 3)
        up, uq = gp / np.linalg.norm(gp), gq / np.linalg.norm(gq)
        r = rule(gp, gq)
        worst["bis"] = max(worst["bis"], float(np.linalg.norm(r - np.linalg.norm(gp) * (up + uq)) / np.linalg.norm(r)))
        worst["proj"] = max(worst["proj"], abs(float(r @ up - r @ uq)) / np.linalg.norm(r))
        m_u, _ = mgda2(up, uq)
        worst["mgda_u"] = max(worst["mgda_u"], 1 - cosang(m_u, r))
        im, _ = imtl_g2(gp, gq)
        worst["imtl"] = max(worst["imtl"], 1 - abs(cosang(im, r)))
        m_raw, _ = mgda2(gp, gq); mgda_raw_cos.append(cosang(m_raw, r))
    print(f"[1] rule(Omega=1) = |g_p|(u_p + u_q): max relative deviation over 1000 random pairs (dims 2-11, scales 1e-3..1e3) {worst['bis']:.3e}")
    print(f"[2] equal projections on u_p and u_q (IMTL-G condition): max |r.u_p - r.u_q|/|r| {worst['proj']:.3e}")
    print(f"[3] MGDA on unit gradients has the rule's direction: max (1 - cos) {worst['mgda_u']:.3e}; IMTL-G (two tasks) max (1 - |cos|) {worst['imtl']:.3e}")
    q = np.quantile(mgda_raw_cos, [0.0, 0.5])
    print(f"    MGDA on raw gradients vs the rule: cos min {q[0]:.4f}, median {q[1]:.4f} (not the same direction in general)")
    # [4] on the Pareto curve of two quadratics
    H = np.diag([1.0, 2.0, 0.5, 1.5, 3.0]); F = 16 * np.diag([2.0, 0.5, 1.0, 3.0, 0.25])
    a = np.array([2.0, 1.0, -1.0, 0.5, 0.0]); b = np.zeros(5)
    print("[4] on the Pareto curve theta(lam) = (H + lam F)^-1 (H a + lam F b):")
    print("    lam | |rule O=1|/|g_p| | |rule O=0.9|/|g_p| | |rule O=1.1|/|g_p| | |MGDA raw| / |g_p| | |MGDA unit| | |IMTL-G|/|g_p|")
    for lam in (0.01, 0.1, 1.0, 10.0, 100.0):
        th = np.linalg.solve(H + lam * F, H @ a + lam * F @ b); gp = H @ (th - a); gq = F @ (th - b)
        n = np.linalg.norm(gp); up, uq = gp / n, gq / np.linalg.norm(gq)
        m_raw, _ = mgda2(gp, gq); m_u, _ = mgda2(up, uq); im, _ = imtl_g2(gp, gq) if np.linalg.norm(up - uq) > 0 else (np.zeros(5), 0)
        print(f"    {lam:g} | {np.linalg.norm(rule(gp, gq, 1.0)) / n:.3e} | {np.linalg.norm(rule(gp, gq, 0.9)) / n:.6f} | {np.linalg.norm(rule(gp, gq, 1.1)) / n:.6f} | "
              f"{np.linalg.norm(m_raw) / n:.3e} | {np.linalg.norm(m_u):.3e} | {np.linalg.norm(im) / n:.3e}")
    # [5] scale: rescaling the past term by c
    gp = np.array([1.0, 0.3, -0.2]); gq = np.array([-0.5, 0.4, 0.9])
    print("[5] step length when the past term is rescaled by c (present fixed): the rule keeps |g_p| as its scale")
    for c in (1 / 16, 1.0, 16.0, 256.0):
        m_raw, a_raw = mgda2(gp, c * gq); im, a_im = imtl_g2(gp, c * gq)
        print(f"    c {c:g}: |rule| {np.linalg.norm(rule(gp, c * gq)):.6f}; |MGDA raw| {np.linalg.norm(m_raw):.6f} (weight on present {a_raw:.6f}); "
              f"|IMTL-G| {np.linalg.norm(im):.6f} (weight on present {a_im:.6f})")
    print("reading (computed above, not a verdict): at Omega = 1 the rule is the bisector of the unit gradients, which is MGDA on "
          "normalised gradients and, for two tasks, the IMTL-G equal-projection direction; all three are stationary at every Pareto point.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
