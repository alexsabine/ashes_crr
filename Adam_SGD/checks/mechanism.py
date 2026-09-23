"""Mechanism check: is the ratio rule's win in the drifting worlds a coincidence of equal gradient noise? (owner request,
prompt-log entry 107; declared in Adam_SGD/DECLARATION_4.md before its first full run). Synthetic (rung R4); labels computed.

The explanation under test (AGENT_LOG 93): at equilibrium the signal parts of the present and past pulls cancel, so the
unsmoothed ratio w = |g_p| / |g_q| is set by the ratio of the two gradients' NOISE magnitudes. Declaration 3's worlds gave
both the same noise (0.5, scaled with the units), so the rule's effective weight w c_t came out near 1, which is the
oracle's weight in those worlds. If so, making the past gradient r times noisier than the present one should move the
rule's effective weight to about 1/r and remove its advantage.

World: T0' of drift_battery_2.py (two tasks, make_model(mismatch=1), units c_t a log-OU path, 'unit' reading, past noise
scaled with the units), with the past gradient's noise set to r x the present noise, r in {0.25, 0.5, 1, 2, 4}, and a
noise-free past (r = 0), SGD. Per r: the constant (lambda x learning rate), the ratio rule (s 0) and the registered rule
(s 0.9) (learning rate), and the oracle that knows the units (lambda x learning rate), all tuned on seeds 0-9 and scored
on held-out seeds 10-19 on drift_battery_2's grids; the effective weight w c_t (median over the second half of the run,
median over held-out seeds) of both rules.
  [M1] the ratio rule's effective weight tracks 1/r: |weff x r - 1| <= 0.25 at every r > 0
  [M2] the ratio rule reads AHEAD of the constant at r = 1 and at no r with |log2 r| >= 2 (r = 0.25, 4)
  [M3] with a noise-free past (r = 0) the ratio rule's label and effective weight are reported (no prediction)
Run: uv run python Adam_SGD/checks/mechanism.py > Adam_SGD/checks/mechanism.txt
"""
from __future__ import annotations

import multiprocessing
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as cm  # noqa: E402
import drift_battery as db  # noqa: E402
import drift_battery_2 as d2  # noqa: E402
import engine as en  # noqa: E402

RS = (0.25, 0.5, 1.0, 2.0, 4.0, 0.0)
WNAME = "T0'"


def _job(args):
    arm, lr, r, knobs, smooth = args
    sc = en.simulate(d2.world(WNAME), arm, knobs, d2.TUNE, opt="sgd", lr=lr, smooth=smooth, noise_q=r * cm.NOISE)
    return args, np.where(np.all(np.isfinite(sc), axis=1), np.mean(np.where(np.isfinite(sc), sc, 0.0), axis=1), np.inf)


def best(pool, arm, r, smooth=0.9):
    knobs = d2.LAM if arm in ("fixed", "sched") else (1.0,)
    b = (None, None, np.inf)
    for args, means in pool.map(_job, [(arm, lr, r, knobs, smooth) for lr in d2.LR_SGD]):
        i = int(np.argmin(means))
        if means[i] < b[2]: b = (knobs[i], args[1], float(means[i]))
    return b


def held(arm, st, r, smooth=0.9):
    if st[0] is None: return np.full(len(d2.EVAL), np.inf), None
    sc, weff = en.simulate(d2.world(WNAME), arm, [st[0]], d2.EVAL, opt="sgd", lr=st[1], smooth=smooth, noise_q=r * cm.NOISE, log_w=True)
    return np.where(np.isfinite(sc[0]), sc[0], np.inf), (float(np.median(weff[0])) if weff is not None else None)


def main():
    print(f"Mechanism check (Adam_SGD/checks/mechanism.py): world {WNAME} of drift_battery_2.py, SGD, past noise = r x present noise (0.5); "
          f"tune seeds {d2.TUNE[0]}-{d2.TUNE[-1]}, held-out {d2.EVAL[0]}-{d2.EVAL[-1]}")
    labs = {}; weffs = {}
    with ProcessPoolExecutor(max_workers=4, mp_context=multiprocessing.get_context("fork")) as pool:
        for r in RS:
            fx = best(pool, "fixed", r); r0 = best(pool, "rule", r, 0.0); rg = best(pool, "rule", r, 0.9); orc = best(pool, "sched", r)
            s_fx, _ = held("fixed", fx, r); s_r0, w0 = held("rule", r0, r, 0.0); s_rg, w9 = held("rule", rg, r, 0.9); s_or, _ = held("sched", orc, r)
            m = {k: float(np.mean(v)) for k, v in (("fx", s_fx), ("r0", s_r0), ("rg", s_rg), ("or", s_or))}
            l0 = db.label(m["r0"] / m["fx"]); l9 = db.label(m["rg"] / m["fx"]); labs[r] = l0; weffs[r] = w0
            print(f"  r = {r:g}: constant lambda {fx[0]:.4g} (lr {fx[1]:.4g}) -> {cm.f(m['fx'])}; oracle lambda {orc[0]:.4g} -> {cm.f(m['or'])} (headroom {m['or'] / m['fx']:.3f}); "
                  f"ratio rule -> {cm.f(m['r0'])} (/constant {m['r0'] / m['fx']:.3f}, {l0}; ahead on {int(np.sum(s_r0 < s_fx))}/{len(d2.EVAL)} seeds; effective weight {w0:.4g}"
                  + (f", x r = {w0 * r:.3f}" if r > 0 else "") + f"); registered -> {cm.f(m['rg'])} (/constant {m['rg'] / m['fx']:.3f}, {l9}; effective weight {w9:.4g})")
    m1 = all(abs(weffs[r] * r - 1) <= 0.25 for r in RS if r > 0)
    m2 = labs[1.0] == "AHEAD" and all(labs[r] != "AHEAD" for r in (0.25, 4.0))
    print(f"[M1] the ratio rule's effective weight tracks 1/r (|weff x r - 1| <= 0.25 at every r > 0): {m1}")
    print(f"[M2] the ratio rule is AHEAD at r = 1 and not AHEAD at r = 0.25 or 4: {m2}  (labels by r: " + ", ".join(f"{r:g}: {labs[r]}" for r in RS) + ")")
    print(f"[M3] noise-free past (r = 0): ratio rule {labs[0.0]}, effective weight {weffs[0.0]:.4g}")
    print(f"summary: M1 {'holds' if m1 else 'FAILS'}, M2 {'holds' if m2 else 'FAILS'}; " +
          ("the ratio rule's win is set by the noise ratio (an equal-noise coincidence)" if (m1 and m2) else "the noise-ratio explanation is not confirmed as declared"))


if __name__ == "__main__":
    main()
