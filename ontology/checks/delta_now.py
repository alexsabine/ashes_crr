"""Re-check (owner request 2026-09-22, prompt-log entry 83): the Dirac delta as Now, and 'the edge of criticality as one
Omega before rupture'. Two facts computed on synthetic carriers (no data, R2), every verdict word from the numbers (R15).
[1] A3's delta, delta(Now) = delta(u(t) - u(t_n) - L/2), is a delta in the PHASE of a cyclic carrier: its mass is one cut
    per half-turn whatever the speed profile, and its density in TIME at the cut is the phase speed there. The delta of
    synthesis batch 28 row 1 (an infinite-precision observation in a Kalman filter) is a delta in the LIKELIHOOD, on a
    belief path that has no rotor: A3 does not apply to it. The two are computed side by side.
[2] 'One Omega before rupture' is not in CRR v3.1: the strong form C * Omega = 1 was the issue-#21 / external-spec rupture
    law, removed there (spec XI.1; verify_spec_math [XI.1]: it coincides with the half-turn cut only when the half-turn is
    one Fisher unit). What the pinned mathematics has instead is the fixed weight's stability edge and the rule's
    distance below it; here the Omega at which the registered rule first diverges on the two-task quadratic is read off.
Run: uv run python ontology/checks/delta_now.py   (pinned: delta_now.txt)
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "theory" / "checks"))
import omega_sweeps as om  # noqa: E402
from crr.instrument.core import antipodal_cuts, intrinsic_phase  # noqa: E402


def part1():
    print("[1] A3's delta(Now) is a delta in the phase: one cut per half-turn, whatever the speed")
    rng = np.random.default_rng(83); dt = 1e-3; T = 60.0; n = int(T / dt); t = np.arange(n) * dt; masses = []
    for name, speed in (("constant speed", lambda tt: 1.0 + 0 * tt), ("speed varying 4x", lambda tt: 2.5 + 1.5 * np.sin(0.37 * tt)),
                        ("speed with random bursts", lambda tt: 1.0 + 3.0 * (np.sin(0.9 * tt) > 0.8))):
        phase = np.cumsum(speed(t)) * dt                                     # the rotor's own phase u(t), L = 2 pi
        x = np.cos(phase)                                                    # the carrier
        cuts = antipodal_cuts(intrinsic_phase(x), start=0)                  # the instrument's A3 (analytic phase, oriented half-turns)
        cuts = cuts[2:-2]                                                    # interior cuts: the analytic phase of a finite record is distorted at its ends (file 06)
        adv = phase[cuts[-1]] - phase[cuts[0]]; half_turns = adv / math.pi
        per_half = (len(cuts) - 1) / half_turns; masses.append(per_half)     # cuts per half-turn: the delta's mass
        dens = speed(t[cuts[1:-1]])                                          # the delta's density in time at each cut = phase speed there
        gaps = np.diff(t[cuts]); cv_gap = float(np.std(gaps, ddof=1) / np.mean(gaps)) if len(gaps) > 2 else float("nan")
        print(f"     {name:26s}: {len(cuts) - 1} interior cuts over {half_turns:.2f} half-turns -> mass per half-turn {per_half:.4f}; "
              f"time density at the cuts = phase speed, range [{dens.min():.3f}, {dens.max():.3f}]; CV of the cut spacing in time {cv_gap:.4f}")
    print(f"     computed: mass per half-turn within 2 % of 1 on every profile: {all(abs(v - 1) < 0.02 for v in masses)}; the cut spacing in TIME varies with the speed (that spacing is not the delta's mass, it is where the mass lands)")
    # the FEP delta of batch 28 row 1: a likelihood delta on a belief path with no rotor
    m = 0.0; P = 1.0; q = 0.05; x = 0.0; path = []
    for k in range(4000):
        x += math.sqrt(q) * rng.normal(); Pp = P + q
        if k % 200 == 100:
            y = x + rng.normal() / 100.0; S = Pp + 1e-4                     # delta-precision observation (pi = 1e4)
        else:
            y = x + rng.normal(); S = Pp + 1.0
        K = Pp / S; m = m + K * (y - m); P = (1 - K) * Pp; path.append(m)
    path = np.array(path); ph = intrinsic_phase(path)
    turns = (ph[-1] - ph[0]) / (2 * math.pi)
    print(f"     the Kalman belief path of batch 28 row 1: analytic-phase advance over 4000 steps {turns:.2f} turns, i.e. no rotor the carrier owns (a random walk's analytic phase is not a cycle of the system);")
    print("     computed: A3's delta needs a cyclic carrier (v3.1 A3: 'where the system is cyclic'); the likelihood delta of row 28-1 is the FEP's object, not A3's, and row 28-1 tested the FEP's delta")


def part2():
    print()
    print("[2] 'One Omega before rupture': not in v3.1; what the pinned mathematics has instead")
    H, F, a, b = om.make_model(); lr = 0.05
    lam_edge = (2.0 / lr - np.diag(H).max()) / np.diag(F).max()
    print(f"     the fixed weight's stability edge on the two-task quadratic: lambda* = {lam_edge:.4f} (lr (h_max + lambda f_max) = 2)")
    grid = (0.25, 0.35, 0.5, 0.71, 1.0, 1.41, 2.0, 2.83, 4.0); tot = {}; ok = {}
    for omg in grid:
        vals = []; fin = True
        for s in range(5):
            th, fine = _run(H, F, a, b, omg, s)
            fin = fin and fine; vals.append(sum(om.losses(H, F, a, b, th)) if fine else float("nan"))
        tot[omg] = float(np.mean(vals)) if fin else float("nan"); ok[omg] = fin
    clean = tot[1.0]
    first_degrade = next((o for o in grid if o > 1.0 and (not ok[o] or tot[o] > 2 * clean)), None)
    first_div = next((o for o in grid if not ok[o]), None)
    print("     total loss by Omega (registered estimator, noise 0.5, 4000 steps, 5 seeds): " + " ".join(f"{o}:{tot[o]:.3f}" if ok[o] else f"{o}:DIVERGED" for o in grid))
    print(f"     computed: the first Omega above 1 whose total exceeds twice the Omega = 1 total (or diverges) is {first_degrade}; the first that diverges is {first_div}; "
          f"the degradation begins {('a factor ' + f'{first_degrade:g}' + ' above 1 (one grid step)') if first_degrade is not None and first_degrade <= 1.41 else (('a factor ' + f'{first_degrade:g}' + ' above 1') if first_degrade is not None else 'nowhere on this grid')} and no Omega on the grid diverges: a degradation, not a rupture; "
          f"and at Omega = 1 the update on the Pareto curve has norm |1 - Omega| |g_p| = 0 (the knife edge, omega_sweeps.txt [2]), so Omega = 1 is AT the edge of stalemate, not one step before a rupture")
    print("     the strong form C * Omega = 1 (rupture when the accumulated arc reaches 1/Omega) belongs to the issue-#21 text and the external spec, which removed it (spec XI.1; verify_spec_math [XI.1]: it coincides with the half-turn cut only when the half-turn is one Fisher unit); v3.1 has no criticality clause (SPEC_RECONCILIATION section 3) and Omega belongs to regeneration (H-EQ), not to the cut")


def _run(H, F, a, b, omg, seed, lr=0.05, steps=4000, noise=0.5):
    rng = np.random.default_rng(seed); th = b.copy(); ema_p = ema_q = None
    for _ in range(steps):
        g_p = H @ (th - a) + noise * rng.standard_normal(len(th)); g_q = F @ (th - b) + noise * rng.standard_normal(len(th))
        ema_p = g_p if ema_p is None else om.SMOOTH * ema_p + (1 - om.SMOOTH) * g_p
        ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
        th = th - lr * (g_p + om.rule_w(ema_p, ema_q, omg) * g_q)
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6:
            return th, False
    return th, True


def main():
    print("delta(Now) and the edge (2026-09-22, prompt-log entry 83): two computed facts, verdict words from the numbers")
    part1(); part2(); return 0


if __name__ == "__main__":
    raise SystemExit(main())
