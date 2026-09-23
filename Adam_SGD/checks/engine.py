"""Batched trajectory engine for the drifting-world battery (Adam_SGD/DECLARATION_2.md).

Runs a whole grid of fixed weights (or several Omega values) and a set of seeds at once. The array theta has shape
(L, S, d): L knobs, S seeds, d parameters. Every knob sees the same random draws for a given seed (common random numbers),
so the comparisons are paired. The draws are taken per seed in the order of common.run (present noise, then past noise,
each step), so a stationary two-task world reproduces common.run exactly (checked as [E0] in drift_battery.py).

Worlds are diagonal quadratics (the matrices of omega_sweeps.make_model are diagonal):
  TWO   one present task (h, a) and one past term (f, b); the learner sees the past gradient
        c_t (f (theta - b) + noise_q xi) (noise scaled with the units) or c_t f (theta - b) + noise_q xi (noise unscaled);
        the objective is L_p + L_q (the 'unit' reading) or L_p + c_t L_q ('imp'); start at b
  SEQ   K tasks of T steps; task k's present gradient h_k (theta - a_k) + noise xi; the past term is online EWC:
        precision P_k = sum_{j<k} u_j h_j anchored at theta at the end of task k-1, gradient P_k (theta - anchor) (exact);
        u_j is the units error of task j's Fisher (1 when calibrated); the objective is the mean over tasks seen of
        L_j = 0.5 sum h_j (theta - a_j)^2; start at a_0
Arms: 'fixed' (weight lambda), 'sched' (lambda / c_t: the oracle that knows the units), 'rule' (w = Omega |ema g_p| /
|ema g_q|, cap and floor of omega_sweeps; smoothing 0 is the VQGAN-style ratio).
Optimisers: 'sgd'; 'mom' (heavy ball, beta 0.9, theta -= lr v); 'adam' (Adam on the whole step, coupled); 'adamd'
(Adam on the present gradient at lr, the past pull applied outside it at lr_q; the rule's weight then equals Omega
|ema of the applied present step| / (lr_q |ema g_q|), as adam_checks.py [A5]).
The score is the anytime objective: the mean over evaluation points (every EVAL_EVERY steps) of the objective; a
trajectory whose parameters leave |theta| <= 1e6 or become non-finite is diverged (nan).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as cm  # noqa: E402

EVAL_EVERY = 100
BETA_M = 0.9
FLOOR = cm.om.DEN_FLOOR; CAP = cm.om.WCAP


class World:
    """kind 'TWO' or 'SEQ'. For TWO: c_path(seed) -> array (steps,) of the units scale; reading; scale_noise.
    For SEQ: K, T, u_draw(seed) -> array (K,) of units errors."""
    def __init__(self, kind, steps, **kw):
        self.kind = kind; self.steps = steps; self.__dict__.update(kw)
        H, F, a, b = cm.om.make_model(mismatch=kw.get("mismatch", 16.0))     # mismatch 16 is omega_sweeps' default
        self.h = np.diag(H).copy(); self.f = np.diag(F).copy(); self.a = a.copy(); self.b = b.copy()
        if kind == "SEQ":
            rng = np.random.default_rng(self.task_seed); d = len(self.h)
            self.hs = rng.uniform(0.5, 2.0, (self.K, d)); a0 = rng.standard_normal(d)
            self.as_ = np.vstack([a0] + [a0 + 1.5 * rng.standard_normal(d) for _ in range(self.K - 1)])


def simulate(world, arm, knobs, seeds, opt="sgd", lr=cm.LR, lr_q=None, smooth=cm.om.SMOOTH, noise=cm.NOISE,
             noise_q=None, final=False, log_w=False):
    """log_w: also return the median over the second half of the run of the effective weight w c_t (TWO worlds), per knob
    and seed; the default return is unchanged."""
    knobs = np.asarray(knobs, float); L = len(knobs); S = len(seeds); d = len(world.h)
    steps = world.steps if world.kind == "TWO" else (world.K - 1) * world.T
    noise_q = noise if noise_q is None else noise_q
    draws = np.stack([np.random.default_rng(s).standard_normal((steps, 2, d)) for s in seeds], axis=1)  # (steps,S,2,d)
    if world.kind == "TWO":
        cpath = np.stack([world.c_path(s) for s in seeds], axis=1)          # (steps,S)
        th = np.broadcast_to(world.b, (L, S, d)).copy()
    else:
        cpath = None
        u = np.stack([world.u_draw(s) for s in seeds], axis=0)              # (S,K)
        th = np.broadcast_to(world.as_[0], (L, S, d)).copy()                # task 0 already learned
        anchor = th.copy(); P = np.zeros((S, d))
    ema_p = ema_q = None; m = np.zeros_like(th); v = np.zeros_like(th); vel = np.zeros_like(th)
    dead = np.zeros((L, S), bool); acc = np.zeros((L, S)); n_eval = 0; wlog = []
    for t in range(steps):
        xp = noise * draws[t, :, 0, :]; xq = noise_q * draws[t, :, 1, :]      # (S,d)
        if world.kind == "TWO":
            c = cpath[t][None, :, None]
            g_p = world.h * (th - world.a) + xp
            g_q = c * (world.f * (th - world.b) + xq) if world.scale_noise else c * (world.f * (th - world.b)) + xq
        else:
            k = 1 + t // world.T                                             # tasks 1 .. K-1 are learned in turn
            if t % world.T == 0:                                             # boundary: accumulate task k-1's precision, re-anchor
                P = P + u[:, k - 1, None] * world.hs[k - 1]
                anchor = th.copy()
            Pk = np.broadcast_to(np.sum(world.hs[:k], axis=0), (S, d)) if arm == "sched" else P
            g_p = world.hs[k] * (th - world.as_[k]) + xp
            g_q = Pk[None] * (th - anchor)
        if arm == "fixed":
            w = np.broadcast_to(knobs[:, None], (L, S))
        elif arm == "sched":                                                 # the oracle that knows the units
            w = np.broadcast_to(knobs[:, None] / cpath[t][None, :], (L, S)) if world.kind == "TWO" else np.broadcast_to(knobs[:, None], (L, S))
        else:
            pres = g_p
            if opt == "adamd":                                               # the applied present step (Adam direction)
                m2 = cm.B1 * m + (1 - cm.B1) * g_p; v2 = cm.B2 * v + (1 - cm.B2) * g_p * g_p
                pres = lr * (m2 / (1 - cm.B1 ** (t + 1))) / (np.sqrt(v2 / (1 - cm.B2 ** (t + 1))) + cm.EPS)
            ema_p = pres if (ema_p is None or smooth == 0) else smooth * ema_p + (1 - smooth) * pres
            ema_q = g_q if (ema_q is None or smooth == 0) else smooth * ema_q + (1 - smooth) * g_q
            den = np.linalg.norm(ema_q, axis=-1) * (lr_q if opt == "adamd" else 1.0)
            w = np.minimum(knobs[:, None] * np.linalg.norm(ema_p, axis=-1) / np.maximum(den, FLOOR), CAP)
        if log_w and world.kind == "TWO" and t >= steps // 2:
            wlog.append(np.asarray(w) * cpath[t][None, :])
        wv = w[..., None]
        if opt == "sgd":
            th = th - lr * (g_p + wv * g_q)
        elif opt == "mom":
            vel = BETA_M * vel + (g_p + wv * g_q); th = th - lr * vel
        elif opt == "adam":
            st = g_p + wv * g_q
            m = cm.B1 * m + (1 - cm.B1) * st; v = cm.B2 * v + (1 - cm.B2) * st * st
            th = th - lr * (m / (1 - cm.B1 ** (t + 1))) / (np.sqrt(v / (1 - cm.B2 ** (t + 1))) + cm.EPS)
        else:                                                                # adamd
            m = cm.B1 * m + (1 - cm.B1) * g_p; v = cm.B2 * v + (1 - cm.B2) * g_p * g_p
            th = th - lr * (m / (1 - cm.B1 ** (t + 1))) / (np.sqrt(v / (1 - cm.B2 ** (t + 1))) + cm.EPS) - lr_q * wv * g_q
        fin = np.all(np.isfinite(th), axis=-1)
        bad = ~fin | (np.linalg.norm(np.where(np.isfinite(th), th, 0.0), axis=-1) > 1e6)
        if bad.any():
            dead |= bad; th[bad] = 0.0; m[bad] = 0.0; v[bad] = 0.0; vel[bad] = 0.0
            if ema_p is not None: ema_p[bad] = 0.0; ema_q[bad] = 0.0
            if world.kind == "SEQ": anchor = anchor.copy(); anchor[bad] = 0.0
        if (t + 1) % EVAL_EVERY == 0:
            acc += _objective(world, th, t, cpath); n_eval += 1
    out = _objective(world, th, steps - 1, cpath) if final else acc / n_eval
    out = np.where(dead, np.nan, out)                                       # (L,S)
    if log_w:
        return out, (np.median(np.stack(wlog), axis=0) if wlog else None)
    return out


def _objective(world, th, t, cpath):
    if world.kind == "TWO":
        Lp = 0.5 * np.sum(world.h * (th - world.a) ** 2, axis=-1); Lq = 0.5 * np.sum(world.f * (th - world.b) ** 2, axis=-1)
        return Lp + (cpath[t][None, :] * Lq if world.reading == "imp" else Lq)
    k = 1 + t // world.T
    ls = [0.5 * np.sum(world.hs[j] * (th - world.as_[j]) ** 2, axis=-1) for j in range(k + 1)]
    return np.mean(ls, axis=0)
