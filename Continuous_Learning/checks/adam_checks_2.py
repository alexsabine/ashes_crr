"""Follow-up to adam_checks.txt (owner request, prompt-log entry 104): why the VQGAN-style ratio beat the rule at the
mismatched scales ([A7]: total/tuned 0.526 against 0.660 at c = 16, 0.847 against 1.235 at c = 256). Declared in
Continuous_Learning/DECLARATION_ADAM_2.md before the first full run. Same model and trajectory code as adam_checks.py.

    [B1] Smoothing ablation under SGD: the rule with the EMA constant s in {0, 0.5, 0.9, 0.98} at every c. If the rule at
         s = 0 is within 10 % of the VQGAN-style ratio at c = 16 and c = 256, the gap in [A7] is the smoothing (the two
         then differ only by the additive delta 1e-4, negligible against these gradient norms).
    [B2] What the smoothing buys: at c = 16, the rule at s = 0.9 against s = 0 at present/past noise in {0.1, 0.5, 1.0}.
         Printed per noise level: which is lower, and the ratio.
    [B3] The weight itself: at c = 16 and c = 256, the median derived w over the last 1000 steps for s = 0 and s = 0.9,
         beside the SGD-tuned fixed lambda and the edge lambda*. A rule whose weight sits above the tuned lambda is
         under-weighting nothing; one below it gives the past term less than the total loss asks for.
Every label is computed from the numbers (R15). Run:
    uv run python Continuous_Learning/checks/adam_checks_2.py > Continuous_Learning/checks/adam_checks_2.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "theory" / "checks"))
sys.path.insert(0, str(ROOT / "Continuous_Learning" / "checks"))
import adam_checks as ac  # noqa: E402
import omega_reprocessed as orp  # noqa: E402
import omega_sweeps as om  # noqa: E402

SMOOTHS = (0.0, 0.5, 0.9, 0.98)
NOISES = (0.1, 0.5, 1.0)
TOL = ac.TOL
LAST = 1000


def with_smooth(s, fn):
    old = om.SMOOTH; om.SMOOTH = s
    try:
        return fn()
    finally:
        om.SMOOTH = old


def median_w(H, F, a, b, s, seed=0):
    def run():
        rng = np.random.default_rng(seed); th = b.copy(); ema_p = ema_q = None; ws = []
        for t in range(orp.STEPS):
            g_p = H @ (th - a) + orp.NOISE * rng.standard_normal(len(th)); g_q = F @ (th - b) + orp.NOISE * rng.standard_normal(len(th))
            ema_p = g_p if ema_p is None else om.SMOOTH * ema_p + (1 - om.SMOOTH) * g_p
            ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
            w = om.rule_w(ema_p, ema_q, 1.0); ws.append(w)
            th = th - orp.LR * (g_p + w * g_q)
            if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6: return float("nan")
        return float(np.median(ws[-LAST:]))
    return with_smooth(s, run)


def main():
    H, F, a, b = om.make_model()
    print(f"Adam checks, follow-up (Continuous_Learning/checks/adam_checks_2.py): the two-task quadratic as adam_checks.py; SGD lr {orp.LR}, "
          f"{orp.STEPS} steps, {orp.SEEDS} seeds; smoothing grid {SMOOTHS}; past scale c in {[round(c, 4) for c in ac.SCALES]}")
    print("[B1] Smoothing ablation under SGD: total per scale (ratio to the SGD-tuned fixed weight)")
    tuned = {}; vq = {}; rule = {s: {} for s in SMOOTHS}
    for c in ac.SCALES:
        Fc = c * F; tuned[c] = ac.tune("fixed", H, Fc, a, b); vq[c] = ac.ev("vq", 1.0, H, Fc, a, b)
        for s in SMOOTHS:
            rule[s][c] = with_smooth(s, lambda: ac.ev("eq", 1.0, H, Fc, a, b))
    for s in SMOOTHS:
        print(f"     rule, smoothing {s:<4g}: " + "; ".join(f"c = {c:g}: {ac.f(rule[s][c])} ({rule[s][c] / tuned[c][1]:.3f})" for c in ac.SCALES))
    print(f"     VQGAN-style          : " + "; ".join(f"c = {c:g}: {ac.f(vq[c])} ({vq[c] / tuned[c][1]:.3f})" for c in ac.SCALES))
    print(f"     SGD-tuned fixed      : " + "; ".join(f"c = {c:g}: lambda {tuned[c][0]:g} total {tuned[c][1]:.4f}" for c in ac.SCALES))
    b1 = all(np.isfinite(rule[0.0][c]) and abs(rule[0.0][c] - vq[c]) <= TOL * vq[c] for c in (16.0, 256.0))
    print(f"     B1 holds (the rule at smoothing 0 within 10 % of the VQGAN-style ratio at c = 16 and c = 256: the gap in [A7] is the smoothing): {b1}")
    best_s = {c: min(SMOOTHS, key=lambda s: rule[s][c] if np.isfinite(rule[s][c]) else np.inf) for c in ac.SCALES}
    print("     computed: the best smoothing per scale " + ", ".join(f"c = {c:g}: {best_s[c]:g}" for c in ac.SCALES))
    print("[B2] What the smoothing buys at c = 16: the rule at smoothing 0.9 against smoothing 0, per noise level")
    Fc = 16.0 * F
    for nz in NOISES:
        r9 = with_smooth(0.9, lambda: ac.ev("eq", 1.0, H, Fc, a, b, noise=nz, noise_q=nz))
        r0 = with_smooth(0.0, lambda: ac.ev("eq", 1.0, H, Fc, a, b, noise=nz, noise_q=nz))
        lower = "smoothing 0.9" if r9 < r0 else "smoothing 0"
        print(f"     noise {nz:g}: smoothing 0.9 {ac.f(r9)}; smoothing 0 {ac.f(r0)}; lower: {lower}" + (f" (0.9 / 0 = {r9 / r0:.3f})" if np.isfinite(r9) and np.isfinite(r0) else ""))
    print("[B3] The derived weight (median over the last %d steps, seed 0) beside the tuned lambda and the edge" % LAST)
    for c in (16.0, 256.0):
        Fc = c * F; edge = (2 / orp.LR - np.max(np.diag(H))) / np.max(np.diag(Fc))
        w0 = median_w(H, Fc, a, b, 0.0); w9 = median_w(H, Fc, a, b, 0.9)
        side = lambda w: "above the tuned lambda" if w > tuned[c][0] else "at or below the tuned lambda"
        print(f"     c = {c:g}: edge {edge:.4f}; SGD-tuned lambda {tuned[c][0]:g}; median w smoothing 0 {w0:.4f} ({side(w0)}); smoothing 0.9 {w9:.4f} ({side(w9)})")
    print("summary: " + f"B1 {'holds' if b1 else 'FAILS'}")


if __name__ == "__main__":
    main()
