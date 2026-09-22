"""Cross-verification of the Omega = 1 rule against the rules existing catastrophic-forgetting methods use to set the past
pull, on one model where every rule can be run exactly (owner request 2026-09-22, prompt-log entry 73). The model is the
two-task quadratic of theory/checks/omega_sweeps.py (present loss with Hessian H, past penalty with Fisher F sixteen times
H, learner starting at the old-task optimum, mini-batch noise on both gradients). Each method is the update rule its
paper states, reduced to this model; each is run with ONE knob setting, then (a) with the past curvature F multiplied by 16
(the same knob), to see which rules survive a change of units without retuning, and (b) with its own knob multiplied by 10,
to see which rules have a divergence edge. Quality is measured against the best fixed weight on the same scale (tuned in
sample, which favours the baseline). Every label is computed from the numbers (R15). Pinned: omega_vs_methods.txt.
Run: uv run python theory/checks/omega_vs_methods.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import omega_sweeps as om  # noqa: E402

LR = 0.05; STEPS = 4000; NOISE = 0.5; SEEDS = 5
FIXED_GRID = (0.003, 0.01, 0.03, 0.1, 0.3, 0.6, 1.0, 1.2, 1.5, 3.0)


def run(method, knob, H, F, a, b, seed, lr=LR, steps=STEPS, noise=NOISE):
    """One trajectory. Returns (theta, ok). Methods (knob in brackets):
    fixed[lambda]       theta <- theta - lr (g_p + lambda g_q)                       (EWC / L2-SP / a KL penalty at fixed weight)
    omega[Omega]        w = Omega |ema g_p| / |ema g_q| (smooth 0.9, cap 1e4)        (the rule under test)
    gradnorm[-]         GradNorm alpha = 0, weights renormalised to sum 2            (Chen et al. 2018)
    mega[-]             w = ema L_q / ema L_p                                        (MEGA-I loss ratio)
    agem[-]             project g_p off g_q when they conflict                      (A-GEM)
    softproj[c]         remove a fraction c of the conflicting component            (a PCR-style soft projection)
    subspace[k]         project g_p off the top-k eigenvectors of F, no past term    (OGD / OGPSA / SafeAnchor-style protection)
    klctrl[target]      fixed-form controller: w <- w (1 + 0.1 clip((L_q - target)/target, -0.2, 0.2)) every 10 steps (Ziegler-style)
    select[q]           fixed lambda = 1, skip present steps whose |g_p| is above the q-quantile of the last 50 (gradient-based sample selection)
    """
    rng = np.random.default_rng(seed)
    th = b.copy(); ema_p = ema_q = None; ema_Lp = ema_Lq = None; gn_w = np.array([1.0, 1.0]); w_ctrl = 1.0; recent = []
    if method == "subspace":
        evals, evecs = np.linalg.eigh(F); P = evecs[:, np.argsort(evals)[::-1][:int(knob)]]
    for t in range(steps):
        g_p = H @ (th - a) + noise * rng.standard_normal(len(th)); g_q = F @ (th - b) + noise * rng.standard_normal(len(th))
        L_p, L_q = om.losses(H, F, a, b, th)
        if method == "fixed":
            step = g_p + knob * g_q
        elif method == "omega":
            ema_p = g_p if ema_p is None else om.SMOOTH * ema_p + (1 - om.SMOOTH) * g_p
            ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
            step = g_p + om.rule_w(ema_p, ema_q, knob) * g_q
        elif method == "gradnorm":
            Gp, Gq = gn_w[0] * np.linalg.norm(g_p), gn_w[1] * np.linalg.norm(g_q); Gbar = 0.5 * (Gp + Gq)
            grad_w = np.array([np.sign(Gp - Gbar) * np.linalg.norm(g_p), np.sign(Gq - Gbar) * np.linalg.norm(g_q)])
            gn_w = np.maximum(gn_w - 0.025 * grad_w / max(np.abs(grad_w).max(), om.DEN_FLOOR), 1e-3); gn_w = 2 * gn_w / gn_w.sum()
            step = gn_w[0] * g_p + gn_w[1] * g_q
        elif method == "mega":
            ema_Lp = L_p if ema_Lp is None else om.SMOOTH * ema_Lp + (1 - om.SMOOTH) * L_p
            ema_Lq = L_q if ema_Lq is None else om.SMOOTH * ema_Lq + (1 - om.SMOOTH) * L_q
            step = g_p + min(ema_Lq / max(ema_Lp, om.DEN_FLOOR), om.WCAP) * g_q
        elif method in ("agem", "softproj"):
            dot = float(g_p @ g_q); c = 1.0 if method == "agem" else knob
            step = g_p - c * (dot / max(float(g_q @ g_q), om.DEN_FLOOR)) * g_q if dot < 0 else g_p
        elif method == "subspace":
            step = g_p - P @ (P.T @ g_p)
        elif method == "klctrl":
            if t % 10 == 0 and t > 0:
                w_ctrl = w_ctrl * (1 + 0.1 * float(np.clip((L_q - knob) / knob, -0.2, 0.2)))
            step = g_p + w_ctrl * g_q
        elif method == "select":
            recent.append(np.linalg.norm(g_p)); recent = recent[-50:]
            skip = len(recent) >= 10 and np.linalg.norm(g_p) > np.quantile(recent, knob)
            step = (0.0 * g_p if skip else g_p) + 1.0 * g_q
        else:
            raise ValueError(method)
        th = th - lr * step
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6:
            return th, False
    return th, True


def evaluate(method, knob, H, F, a, b):
    tot = []; Lps = []; Lqs = []; ok_all = True
    for s in range(SEEDS):
        th, ok = run(method, knob, H, F, a, b, s); ok_all = ok_all and ok
        Lp, Lq = om.losses(H, F, a, b, th) if ok else (np.nan, np.nan); tot.append(Lp + Lq); Lps.append(Lp); Lqs.append(Lq)
    return float(np.mean(Lps)), float(np.mean(Lqs)), float(np.mean(tot)), ok_all


def tuned_fixed(H, F, a, b):
    best = None
    for lam in FIXED_GRID:
        Lp, Lq, tot, ok = evaluate("fixed", lam, H, F, a, b)
        if ok and (best is None or tot < best[1]): best = (lam, tot)
    return best


METHODS = [  # (name, knob, class, needs)
    ("fixed", 1.0, "fixed weight (EWC/L2-SP/KL penalty); lambda = 1 is also the Bayes/ER-sum weight in this model", "a sweep of lambda"),
    ("omega", 1.0, "normalised gradient (the rule under test)", "smoothing, cap, floor"),
    ("gradnorm", 0.0, "learned task weights (GradNorm alpha = 0)", "a weight learning rate"),
    ("mega", 0.0, "loss ratio (MEGA-I)", "smoothing"),
    ("agem", 0.0, "conflict projection (A-GEM)", "nothing"),
    ("softproj", 0.5, "soft conflict projection (PCR-style)", "a fraction c"),
    ("subspace", 2, "protected subspace, no past term (OGD / OGPSA / SafeAnchor-style)", "a rank k"),
    ("klctrl", 1.0, "target controller on the past loss (adaptive-KL-style)", "a target"),
    ("select", 0.8, "gradient-based sample selection at fixed lambda = 1", "a quantile"),
]


def main():
    print("Omega = 1 against the rules other methods use, on the two-task quadratic of omega_sweeps.py (F = 16 H; noise 0.5; lr 0.05; 4000 steps; 5 seeds; start at the old-task optimum)")
    H, F, a, b = om.make_model()
    H16, F16 = H, 16 * F
    lam_edge = (2.0 / LR - np.diag(H).max()) / np.diag(F).max(); lam_edge16 = (2.0 / LR - np.diag(H).max()) / np.diag(F16).max()
    t1 = tuned_fixed(H, F, a, b); t16 = tuned_fixed(H16, F16, a, b)
    print(f"stability edge of a fixed weight: lambda* = {lam_edge:.4f} at F, {lam_edge16:.4f} at 16F; tuned fixed weight (in-sample, grid {FIXED_GRID}): lambda = {t1[0]:g} total {t1[1]:.4f} at F, lambda = {t16[0]:g} total {t16[1]:.4f} at 16F")
    print()
    print(f"{'method':10s} {'knob':>6s}  {'L_present':>9s} {'L_past':>8s} {'total':>8s} {'/tuned':>7s} | {'16F: total':>10s} {'/tuned':>7s} | {'knob x10':>9s} | label")
    rows = []
    for name, knob, cls, needs in METHODS:
        Lp, Lq, tot, ok = evaluate(name, knob, H, F, a, b)
        Lp16, Lq16, tot16, ok16 = evaluate(name, knob, H16, F16, a, b)
        big = knob * 10 if knob else 0.0
        okb = evaluate(name, big, H, F, a, b)[3] if name not in ("gradnorm", "mega", "agem", "select") else None
        if name == "subspace": okb = evaluate(name, 4, H, F, a, b)[3]
        if name == "softproj": okb = evaluate(name, 1.0, H, F, a, b)[3]
        r1 = tot / t1[1] if ok else float("inf"); r16 = tot16 / t16[1] if ok16 else float("inf")
        robust = ok and ok16 and r1 <= 1.10 and r16 <= 1.10
        edge = (okb is False)
        label = ("scale-robust" if robust else "not scale-robust") + ("; has a divergence edge in its knob" if edge else ("; no knob" if okb is None else "; no edge found at knob x10"))
        rows.append((name, cls, needs, r1, r16, robust, edge, ok, ok16, Lq, Lq16))
        print(f"{name:10s} {knob:6g}  {Lp:9.4f} {Lq:8.4f} {tot:8.4f} {r1:7.3f} | {tot16 if ok16 else float('nan'):10.4f} {r16:7.3f} | {'n/a' if okb is None else ('finite' if okb else 'DIVERGES'):>9s} | {label}")
    print()
    print("computed:")
    for name, cls, needs, r1, r16, robust, edge, ok, ok16, Lq, Lq16 in rows:
        print(f"  {name:10s} [{cls}; needs {needs}] -> within 10 % of the tuned fixed weight at F: {r1 <= 1.10}, at 16F with the same knob: {r16 <= 1.10}; scale-robust: {robust}; divergence edge: {edge}")
    tuned_Lq = evaluate("fixed", t1[0], H, F, a, b)[1]
    print(f"  scale-robust methods (within 10 % of the tuned fixed weight at both F and 16F with one knob setting): {[r[0] for r in rows if r[5]]}")
    print(f"  methods that diverge at 16F with the knob that worked at F: {[r[0] for r in rows if not r[8]]}")
    print(f"  methods that forget (L_past more than 10 x the tuned fixed weight's {tuned_Lq:.4f}) at F: {[r[0] for r in rows if r[7] and r[9] > 10 * tuned_Lq]}")
    print(f"  methods with a divergence edge in their own knob: {[r[0] for r in rows if r[6]]}")
    print("  reading (from the lists above): the rules that weight the past pull by a fixed number, a learned number or a loss ratio carry that number's units and fail when the past curvature changes scale; the rules that project rather than weight never diverge but drop the past wherever the two gradients do not conflict; the rule that scales the past pull by the present pull is the one in this list whose quality survives the change of scale, because its step is bounded by the present step")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
