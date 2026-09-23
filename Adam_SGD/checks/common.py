"""Shared trajectory code for the Adam/SGD checks (owner request, prompt-log entry 107).

The two-task quadratic of theory/checks/omega_sweeps.py (make_model: d = 5, F = 16 H), extended with the two choices the
earlier checks fixed silently:
  scale c and noise   the past term the learner sees is c (F (theta - b) + noise xi) when scale_noise is True (a pure change
                      of units: every number in the past gradient is multiplied by c), and c F (theta - b) + noise xi when it
                      is False (the curvature rescaled, the noise not: the choice of adam_checks.py and omega_reprocessed.py)
  the reading         'imp'  the scale is the past term's true importance: the objective is L_p + c L_q
                      'unit' the scale is a units error (a miscalibrated Fisher, a loss scale): the objective is L_p + L_q
The random draws are taken in the order of omega_reprocessed.traj (present noise, then past noise, each step), so with
scale_noise False the trajectories reproduce the earlier checks exactly (assumptions.py [AS2] verifies this).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "theory" / "checks"))
import omega_reprocessed as orp  # noqa: E402
import omega_sweeps as om  # noqa: E402

LR = orp.LR; STEPS = orp.STEPS; NOISE = orp.NOISE
ADAM_LR = orp.ADAM_LR; B1 = orp.B1; B2 = orp.B2; EPS = orp.EPS
FINE = tuple(float(v) for v in np.logspace(-5, 1, 73))       # the fine tuning grid: 12 points per decade, 1e-5 to 10
TUNE_SEEDS = (0, 1, 2, 3, 4); EVAL_SEEDS = (5, 6, 7, 8, 9)    # tune on one set of seeds, score on another


def run(method, knob, H, F, a, b, seed, c=1.0, scale_noise=True, lr=LR, optimizer="sgd", smooth=om.SMOOTH, steps=None,
        noise=NOISE):
    """method 'fixed' (knob = lambda) or 'rule' (knob = Omega, EMA constant smooth; smooth 0 is the VQGAN-style ratio).
    Returns theta and a finite flag."""
    steps = STEPS if steps is None else steps
    rng = np.random.default_rng(seed); th = b.copy(); ema_p = ema_q = None
    m = np.zeros_like(th); v = np.zeros_like(th)
    for t in range(steps):
        g_p = H @ (th - a) + noise * rng.standard_normal(len(th))
        xi = noise * rng.standard_normal(len(th))
        g_q = c * (F @ (th - b) + xi) if scale_noise else c * (F @ (th - b)) + xi
        if method == "fixed":
            w = knob
        else:
            ema_p = g_p if (ema_p is None or smooth == 0) else smooth * ema_p + (1 - smooth) * g_p
            ema_q = g_q if (ema_q is None or smooth == 0) else smooth * ema_q + (1 - smooth) * g_q
            w = om.rule_w(ema_p, ema_q, knob)
        step = g_p + w * g_q
        if optimizer == "adam":
            m = B1 * m + (1 - B1) * step; v = B2 * v + (1 - B2) * step * step
            th = th - ADAM_LR * (m / (1 - B1 ** (t + 1))) / (np.sqrt(v / (1 - B2 ** (t + 1))) + EPS)
        else:
            th = th - lr * step
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6:
            return th, False
    return th, True


def objective(H, F, a, b, th, c, reading):
    Lp, Lq = om.losses(H, F, a, b, th)
    return Lp + (c * Lq if reading == "imp" else Lq)


def score(method, knob, H, F, a, b, seeds, c=1.0, reading="unit", **kw):
    """Mean objective over seeds; nan if any seed diverges."""
    vals = []
    for s in seeds:
        th, ok = run(method, knob, H, F, a, b, s, c=c, **kw)
        if not ok: return float("nan")
        vals.append(objective(H, F, a, b, th, c, reading))
    return float(np.mean(vals))


def tune(method, grid, H, F, a, b, seeds, **kw):
    """Best knob on the grid over the given seeds: (knob, mean objective), or (None, inf) if none is finite."""
    best = (None, float("inf"))
    for k in grid:
        val = score(method, k, H, F, a, b, seeds, **kw)
        if np.isfinite(val) and val < best[1]: best = (k, val)
    return best


def f(v):
    return "diverges" if not np.isfinite(v) else f"{v:.4f}"
