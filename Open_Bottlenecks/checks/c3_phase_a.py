"""OB1-C3 Phase A (Open_Bottlenecks/C3_DECLARATION.md, pushed at 38c87e3 before this file): consolidation triggers in a
boundary-free stream. Calibration on seed 100 (lambda by ORACLE; each threshold to 4 consolidations), then seeds 0-4 on
BLURRY (primary) and ABRUPT. Gate: G-MATTER, G-TIMING (BLURRY). If open, the two-sided contest ARC - CHORD (CRR-WIN /
RECORD-WIN / TIE) and the reported differences. Words computed (R15).
Run: uv run python Open_Bottlenecks/checks/c3_phase_a.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c3_lib as C  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    doms, K = C.domains()
    print("OB1-C3 Phase A: consolidation triggers in a boundary-free stream (C3_DECLARATION.md); seeds 0-4; calibration seed 100")
    print(f"SGD lr {C.LR}, batch {C.BS}, {C.HID} hidden; {C.N_STEPS} steps, {C.N_DOM} domains, sigma {C.SIGMA}; window {C.WINDOW} "
          f"inputs; clip kappa {C.KAPPA}; rho {C.RHO}")
    print("CHOICES: see c3_lib.py docstring")
    lam_acc = {lam: C.run(100, doms, K, "BLURRY", "ORACLE", lam)["final"] for lam in C.LAMBDAS}
    lam = max(C.LAMBDAS, key=lambda l: (lam_acc[l], -l))
    print("\ncalibration: ORACLE final accuracy on seed 100 by lambda: " + ", ".join(f"{l:g} {a:.2f}" for l, a in lam_acc.items())
          + f" -> lambda {lam:g}")
    U = {}
    for arm in ("ARC", "CHORD", "LOSS"):
        u, c = C.calibrate(doms, K, arm, lam); U[arm] = u
        print(f"calibration: {arm} threshold U {u:.6g} gives {c} consolidations on seed 100")
    res = {}
    for stream in ("BLURRY", "ABRUPT"):
        res[stream] = {a: [C.run(s, doms, K, stream, a, lam, U.get(a)) for s in SEEDS] for a in C.ARMS}
        print(f"\n[{stream}]")
        print(f"   {'arm':7} {'final':>7} {'forget':>7} {'events':>7}   final per seed")
        for a in C.ARMS:
            r = res[stream][a]
            print(f"   {a:7} {np.mean([x['final'] for x in r]):7.2f} {np.mean([x['forget'] for x in r]):7.2f} "
                  f"{np.mean([len(x['events']) for x in r]):7.2f}   " + " ".join(f"{x['final']:6.2f}" for x in r))
        for a in ("ARC", "CHORD", "LOSS", "COUNT", "ORACLE"):
            print(f"   {a:7} consolidation steps: " + " | ".join(",".join(str(e) for e in x["events"]) for x in res[stream][a]))
    print("\n" + "-" * 100)
    f = lambda st, a: [x["final"] for x in res[st][a]]  # noqa: E731
    d1 = np.mean(f("BLURRY", "ORACLE")) - np.mean(f("BLURRY", "NONE")); s1 = step_of(f("BLURRY", "NONE"))
    d2 = np.mean(f("BLURRY", "ORACLE")) - np.mean(f("BLURRY", "RAND")); s2 = step_of(f("BLURRY", "RAND"))
    g1 = d1 > s1; g2 = d2 > s2
    print(f"G-MATTER BLURRY: ORACLE - NONE {d1:+.4f} (step {s1:.4f}) -> {'holds' if g1 else 'FAILS'}")
    print(f"G-TIMING BLURRY: ORACLE - RAND {d2:+.4f} (step {s2:.4f}) -> {'holds' if g2 else 'FAILS'}")
    print("C3 GATE " + ("OPEN" if g1 and g2 else "CLOSED"))
    if g1 and g2:
        d = np.mean(f("BLURRY", "ARC")) - np.mean(f("BLURRY", "CHORD")); st = step_of(f("BLURRY", "CHORD"))
        word = "CRR-WIN" if d > st else ("RECORD-WIN" if d < -st else "TIE")
        print(f"CONTEST BLURRY: ARC - CHORD {d:+.4f} (step {st:.4f}) -> {word}")
    else:
        print("CONTEST not scored (gate closed); the differences below are reported only")
    for stream in ("BLURRY", "ABRUPT"):
        m = np.mean(f(stream, "ARC"))
        print(f"reported {stream}: ARC - CHORD {m - np.mean(f(stream, 'CHORD')):+.4f}; ARC - COUNT {m - np.mean(f(stream, 'COUNT')):+.4f}; "
              f"ARC - LOSS {m - np.mean(f(stream, 'LOSS')):+.4f}; ARC - ORACLE {m - np.mean(f(stream, 'ORACLE')):+.4f}; "
              f"ARC - NONE {m - np.mean(f(stream, 'NONE')):+.4f}")


if __name__ == "__main__":
    main()
