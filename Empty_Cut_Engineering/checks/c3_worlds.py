"""Check C3 (the world) of Empty_Cut_Engineering/DECLARATION.md: does the world move on during the pause? Four worlds, an
online torch learner, one arrival per wall step. Content is measured on the learner's own clock (at the same update count
k) against the run with no pause: bitwise identity of the parameters, and the chord sqrt(2 KL) between Gaussian predictives
on a fixed probe (kl_gauss, exact Fisher-Rao, SCOPE.md P8). Verdict words are computed from the numbers (R15).

Run: uv run --group realsys python Empty_Cut_Engineering/checks/c3_worlds.py > Empty_Cut_Engineering/checks/c3_worlds.txt
"""
import collections
import math
import pathlib
import sys

import numpy as np
import torch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "src"))
from crr.instrument.core import kl_gauss  # noqa: E402

torch.set_num_threads(1); torch.use_deterministic_algorithms(True)
D, BATCH, NOISE, LR = 10, 8, 0.1, 0.05
T_WALL, P0, K_CMP = 3000, 1000, 1500
OMEGA = 0.002                                   # W-drift: rotation of the target per wall step (radians)
LS = (10, 100)
A_PLANT, B_PLANT, W_SD, EXPLORE, U_MAX = 1.05, 0.5, 0.1, 0.1, 5.0
WSEED, LSEED = 2026, 924


# ---------------------------------------------------------------- open-loop streams (W-open, W-drift)
def target(a, drift):
    r = np.random.default_rng(WSEED); w0 = r.normal(size=D); w1 = r.normal(size=D)
    w1 -= (w1 @ w0) / (w0 @ w0) * w0; w1 *= np.linalg.norm(w0) / np.linalg.norm(w1)
    th = OMEGA * a if drift else 0.0
    return w0 * math.cos(th) + w1 * math.sin(th)


def arrival(a, drift):
    """the batch that arrives at wall step a; it exists whether or not anyone is listening"""
    r = np.random.default_rng((WSEED, a)); X = r.normal(size=(BATCH, D))
    y = X @ target(a, drift) + NOISE * r.normal(size=BATCH)
    return torch.tensor(X, dtype=torch.float32), torch.tensor(y, dtype=torch.float32)


PROBE = torch.tensor(np.random.default_rng(77).normal(size=(256, D)), dtype=torch.float32)


def stream_run(drift, L=0, B=None):
    """B None: no pause. Otherwise a pause of L wall steps at P0 with a buffer of capacity B (overflow lost; B = 0 drops)."""
    w = torch.zeros(D); q = collections.deque(); k = 0; snap = None; lost = 0; maxq = 0
    for t in range(T_WALL):
        item = arrival(t, drift)
        paused = B is not None and P0 <= t < P0 + L
        if paused:
            if len(q) < B: q.append(item)
            else: lost += 1
            continue
        q.append(item); maxq = max(maxq, len(q))
        X, y = q.popleft()
        g = 2 * X.T @ (X @ w - y) / BATCH; w = w - LR * g; k += 1
        if k == K_CMP: snap = w.clone()
    wt = torch.tensor(target(T_WALL - 1, drift), dtype=torch.float32)
    err_now = float(torch.mean((PROBE @ (w - wt)) ** 2))
    return dict(snap=snap, k=k, lost=lost, lag=len(q), err_now=err_now, maxq=maxq)


def chord_lin(wa, wb):
    return math.sqrt(2 * kl_gauss((PROBE @ wa).numpy().astype(np.float64), (PROBE @ wb).numpy().astype(np.float64), NOISE ** 2))


# ---------------------------------------------------------------- closed loop (W-sim, W-real)
def plant_run(L=0, pausable=True):
    """x' = a x + b u + w. The learner fits (a_hat, b_hat) by normalised LMS and acts u = -(a_hat / b_hat) x + exploration.
    Pause at wall step P0 for L steps: W-sim freezes the plant and its noise stream; W-real runs on under u = 0."""
    wr = np.random.default_rng(WSEED + 1); lg = torch.Generator(); lg.manual_seed(LSEED)
    th = torch.tensor([0.5, 0.2]); x = 0.0; k = 0; snap = None; exc_pause = 0.0; exc_all = 0.0; t = 0
    while t < T_WALL:
        if L and P0 <= t < P0 + L:
            if not pausable:
                x = A_PLANT * x + W_SD * float(wr.normal()); exc_pause = max(exc_pause, abs(x))
            t += 1; continue
        bh = max(float(th[1]), 0.05); eps = float(torch.randn(1, generator=lg))
        u = float(np.clip(-(float(th[0]) / bh) * x + EXPLORE * eps, -U_MAX, U_MAX))
        xn = A_PLANT * x + B_PLANT * u + W_SD * float(wr.normal())
        phi = torch.tensor([x, u]); err = float(phi @ th) - xn
        th = th - LR * err * phi / (1.0 + float(phi @ phi)); k += 1
        if k == K_CMP: snap = th.clone()
        x = xn; exc_all = max(exc_all, abs(x)); t += 1
    return dict(snap=snap, k=k, exc_pause=exc_pause, exc_all=exc_all)


PGRID = torch.tensor([[xv, uv] for xv in np.linspace(-1, 1, 9) for uv in np.linspace(-1, 1, 9)], dtype=torch.float32)


def chord_plant(ta, tb):
    return math.sqrt(2 * kl_gauss((PGRID @ ta).numpy().astype(np.float64), (PGRID @ tb).numpy().astype(np.float64), W_SD ** 2))


def main():
    print("Empty-cut engineering, check C3 (the world) - Empty_Cut_Engineering/DECLARATION.md")
    print(f"torch {torch.__version__}; online linear learner d {D}, batch {BATCH}, noise {NOISE}, lr {LR}; one arrival per wall step; "
          f"{T_WALL} wall steps; pause at wall step {P0}; own-clock comparison at update k = {K_CMP}")
    print(f"content = sqrt(2 KL) between Gaussian predictives (variance noise^2) on a fixed probe, at the same k, against the run with no pause")
    bytes_per = BATCH * (D + 1) * 4
    g5 = True; g6_buf = True; g6_drop = True
    for drift in (False, True):
        name = "W-drift (target rotates " + f"{OMEGA} rad per wall step)" if drift else "W-open (stationary open-loop stream)"
        ref = stream_run(drift)
        print(f"\n== {name}: no pause: {ref['k']} updates; error on the current world at the last wall step {ref['err_now']:.6g}")
        for L in LS:
            for B in (0, L // 2, L, 2 * L):
                r = stream_run(drift, L, B); same = torch.equal(r["snap"], ref["snap"]); c = chord_lin(ref["snap"], r["snap"])
                lab = "drop" if B == 0 else f"buffer B {B}"
                print(f"   L {L:4d} {lab:13s}: identical at k {K_CMP}: {same}; content {c:.6g}; arrivals lost {r['lost']}; lag behind the stream "
                      f"{r['lag']} arrivals; buffer memory {B * bytes_per} bytes; updates by the end {r['k']}; error on the current world "
                      f"{r['err_now']:.6g} (vs no pause {r['err_now'] - ref['err_now']:+.6g})")
                if not drift:
                    g5 &= same if B >= L else not same
                else:
                    if B >= L: g6_buf &= same
                    if B == 0: g6_drop &= not same
    print(f"\nG5 (open world): buffer B >= L identical and B < L not identical: {'holds' if g5 else 'FAILS'}")
    print(f"G6 (drift): buffered (B >= L) identical on the own clock: {g6_buf}; dropping not identical: {g6_drop} (the lag and its error are reported above)")
    print(f"\n== Closed loop: plant x' = {A_PLANT} x + {B_PLANT} u + N(0, {W_SD}^2) (open-loop unstable); learner fits (a, b), acts u = -(a/b) x + {EXPLORE} noise")
    ref = plant_run()
    print(f"   no pause: {ref['k']} updates; (a_hat, b_hat) at k {K_CMP} = ({float(ref['snap'][0]):.6f}, {float(ref['snap'][1]):.6f}); largest |x| {ref['exc_all']:.6g}")
    g7_sim = True; g7_real = True; creal = []
    for L in LS:
        s = plant_run(L, True); r = plant_run(L, False)
        ss = torch.equal(s["snap"], ref["snap"]); rs = torch.equal(r["snap"], ref["snap"]); cr = chord_plant(ref["snap"], r["snap"]); creal.append(cr)
        print(f"   L {L:4d} W-sim (world checkpointed and frozen): identical at k {K_CMP}: {ss}; content {chord_plant(ref['snap'], s['snap']):.6g}")
        print(f"   L {L:4d} W-real (world runs on, u = 0): identical at k {K_CMP}: {rs}; content {cr:.6g}; largest |x| during the pause {r['exc_pause']:.6g}; "
              f"largest |x| over the run {r['exc_all']:.6g}")
        g7_sim &= ss; g7_real &= not rs
    grows = all(b >= a for a, b in zip(creal, creal[1:]))
    g7 = g7_sim and g7_real and grows
    print(f"\nG7 (closed loop): W-sim identical for every L: {g7_sim}; W-real not identical for every L: {g7_real}; W-real content non-decreasing in L: {grows} "
          f"-> {'holds' if g7 else 'FAILS'}")
    print(f"summary: G5 {'holds' if g5 else 'FAILS'}; G6 buffered identical {g6_buf}, drop not identical {g6_drop}; G7 {'holds' if g7 else 'FAILS'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
