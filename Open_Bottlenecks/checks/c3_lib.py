"""OB1-C3 harness (Open_Bottlenecks/C3_DECLARATION.md, pushed at 38c87e3 before this file): consolidation triggers in a
boundary-free domain-incremental stream. Online-EWC penalty (anchor and accumulated window Fisher at each consolidation),
SEC4's clip for stability. Triggers NONE, ORACLE, COUNT, RAND, ARC, CHORD, LOSS.

CHOICES (printed by the gate script):
  - ARC: a_t = sqrt(2 KL) of each update on its own batch (before -> after); accumulated since the last consolidation.
  - CHORD: D_t = sum_i M_i (theta_i - theta*_i)^2 with M the last consolidation's window Fisher F (not the accumulated Omega);
    before the first consolidation, M and theta* are the window Fisher and the parameters at step 20.
  - LOSS: CUSUM of max(0, l_t - lbar_t), l_t the batch loss before the update, lbar its running mean at rho = 0.01 (starts at
    the first loss); reset to 0 at each consolidation.
  - The window Fisher is the mean of per-sample squared gradients over the last 200 inputs seen (fewer if fewer seen).
  - Accuracy is checked every 12 steps (and at the end) on every domain's test set, for forgetting.
"""
from __future__ import annotations

import math
import sys
from collections import deque
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c1_lib as C1  # noqa: E402

S = C1.S
LR = 0.05; BS = 10; HID = 256; N_STEPS = 360; N_DOM = 5; SIGMA = 0.06; WINDOW = 200; KAPPA = 0.5; RHO = 0.01
CHECK_EVERY = 12; M0_STEP = 20
LAMBDAS = (0.1, 1.0, 10.0, 100.0)
ARMS = ("NONE", "ORACLE", "COUNT", "RAND", "ARC", "CHORD", "LOSS")


def domains():
    Xtr, ytr, Xte, yte, K = C1.base_data()
    chunks = np.array_split(np.random.default_rng(60_000).permutation(len(ytr)), N_DOM)
    doms = []
    for k in range(N_DOM):
        Q, Rr = np.linalg.qr(np.random.default_rng(61_000 + k).standard_normal((Xtr.shape[1], Xtr.shape[1])))
        Q = Q * np.sign(np.diag(Rr)); doms.append(dict(Xtr=Xtr[chunks[k]] @ Q, ytr=ytr[chunks[k]], Xte=Xte @ Q, yte=yte))
    return doms, K


def batches(seed, doms, kind):
    r = np.random.default_rng(80_000 + seed); c = (np.arange(N_DOM) + 0.5) / N_DOM; out = []
    for s in range(N_STEPS):
        tau = (s + 0.5) / N_STEPS
        if kind == "BLURRY":
            w = np.exp(-(tau - c) ** 2 / (2 * SIGMA ** 2)); w = w / w.sum(); ks = r.choice(N_DOM, size=BS, p=w)
        else:
            ks = np.full(BS, min(int(tau * N_DOM), N_DOM - 1))
        X = np.empty((BS, doms[0]["Xtr"].shape[1])); y = np.empty(BS, dtype=doms[0]["ytr"].dtype)
        for i, k in enumerate(ks):
            j = r.integers(0, len(doms[k]["ytr"])); X[i] = doms[k]["Xtr"][j]; y[i] = doms[k]["ytr"][j]
        out.append((X, y))
    return out


def window_fisher(net, win):
    X = np.concatenate([w[0] for w in win]); y = np.concatenate([w[1] for w in win]); F = None
    for i in range(len(y)):
        _, g = S.ce_loss_grad(net, X[i:i + 1], y[i:i + 1]); F = g * g if F is None else F + g * g
    return F / len(y)


def run(seed, doms, K, stream, arm, lam, U=None):
    rng = np.random.default_rng(seed); d = doms[0]["Xtr"].shape[1]; net = S.MLP(rng, d, K, h=HID)
    n = net.flat().size; Omega = np.zeros(n); theta_star = net.flat().copy(); cap = KAPPA / (LR * lam)
    win = deque(maxlen=WINDOW // BS); B = batches(seed, doms, stream)
    events = []; acc_acc = 0.0; lbar = None; cusum = 0.0; M = None; rand_steps = None
    if arm == "RAND":
        rand_steps = set(np.random.default_rng(90_000 + seed).choice(np.arange(1, N_STEPS), size=4, replace=False).tolist())
    oracle_steps = {int(N_STEPS * k / N_DOM) for k in range(1, N_DOM)}
    best = np.full(N_DOM, -1.0)
    with np.errstate(all="ignore"):
        for s, (x, y) in enumerate(B):
            loss, g = S.ce_loss_grad(net, x, y); th0 = net.flat()
            g = g + lam * Omega * (th0 - theta_star)
            th1 = th0 - LR * g; net.set_flat(th1); win.append((x, y))
            fire = False
            if arm == "ORACLE":
                fire = (s + 1) in oracle_steps
            elif arm == "COUNT":
                fire = (s + 1) % (N_STEPS // N_DOM) == 0 and (s + 1) < N_STEPS
            elif arm == "RAND":
                fire = (s + 1) in rand_steps
            elif arm == "ARC":
                acc_acc += C1.arc_of(net, th0, th1, x); net.set_flat(th1); fire = acc_acc >= U
            elif arm == "CHORD":
                if M is None and s + 1 == M0_STEP:
                    M = window_fisher(net, win); theta_star_c = net.flat().copy()
                if M is not None:
                    ref = theta_star if events else theta_star_c
                    fire = float(np.sum(M * (net.flat() - ref) ** 2)) >= U
            elif arm == "LOSS":
                lbar = loss if lbar is None else (1 - RHO) * lbar + RHO * loss
                cusum += max(0.0, loss - lbar); fire = cusum >= U
            if fire and s + 1 < N_STEPS:
                F = window_fisher(net, win); Omega = np.minimum(Omega + F, cap); theta_star = net.flat().copy()
                events.append(s + 1); acc_acc = 0.0; cusum = 0.0
                if arm == "CHORD":
                    M = F
            if (s + 1) % CHECK_EVERY == 0 or s + 1 == N_STEPS:
                for k in range(N_DOM):
                    best[k] = max(best[k], 100 * net.acc(doms[k]["Xte"], doms[k]["yte"]))
    final = np.array([100 * net.acc(dm["Xte"], dm["yte"]) for dm in doms])
    return dict(final=float(final.mean()), forget=float(np.mean(best - final)), events=events)


def calibrate(doms, K, arm, lam, target=4, seed=100, stream="BLURRY", iters=40):
    """Bisection in log U so that the trigger fires `target` times on the calibration run; returns (U, count)."""
    lo, hi = 1e-6, 1e6
    best = None
    for _ in range(iters):
        mid = math.sqrt(lo * hi); c = len(run(seed, doms, K, stream, arm, lam, mid)["events"])
        if best is None or abs(c - target) < abs(best[1] - target) or (abs(c - target) == abs(best[1] - target) and mid < best[0]):
            best = (mid, c)
        if c > target:
            lo = mid
        elif c < target:
            hi = mid
        else:
            hi = mid
            if hi / lo < 1.0001:
                break
    return best
