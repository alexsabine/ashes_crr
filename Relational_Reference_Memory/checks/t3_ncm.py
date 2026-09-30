"""RRM2 T3 (DECLARATION_2.md Part T, pushed at a2719f0 before this file): relational nearest-class-mean classification without
replay (SDC's use of drift compensation, with kept anchors instead of current-task data). Learner ANCH1 (t_lib.train); at the
end classify by the nearest prototype in feature space with STALE, RRM, DECOY or ORACLE prototypes.
Gate T3 (POS): NCM-RRM ahead of NCM-STALE by more than a step (step of NCM-STALE), and NCM-DECOY behind NCM-STALE by more
than a step. Reported: NEG2, and NCM-RRM against ANCH1's own softmax head. The SEEN-carrier report is t1_seen.txt (ANCH1 rows).
Run: uv run python Relational_Reference_Memory/checks/t3_ncm.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Replay_Quality_Memory" / "checks"))
import t_lib as T  # noqa: E402
import phase_a as PA  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    print("RRM2 T3: relational NCM on the ANCH1 learner (DECLARATION_2.md Part T); 20 first-task anchors; beta 0.01; seeds 0-4; accuracy (%)")
    res = {}
    for name in ("POS", "NEG2"):
        data, K = PA.stream(name); Xtr, ytr, Xte, yte = data
        a = {k: [] for k in ("softmax", "ORACLE", "STALE", "RRM", "DECOY")}
        for s in SEEDS:
            net, anchors, rec, cuts = T.train(s, *data, K, "ANCH1")
            a["softmax"].append(100 * net.acc(Xte, yte))
            for w in ("ORACLE", "STALE", "RRM", "DECOY"):
                a[w].append(T.ncm_acc(net, Xte, yte, T.prototypes(net, Xtr, ytr, anchors, rec, cuts, s, w)))
        res[name] = a
        print(f"\n[{name}]")
        for k, v in a.items():
            print(f"   {('NCM-' + k) if k != 'softmax' else 'softmax':11} mean {np.mean(v):7.2f}  seeds " + " ".join(f"{x:6.2f}" for x in v))
    print("\n" + "-" * 100)
    a = res["POS"]; st = step_of(a["STALE"])
    d1 = np.mean(a["RRM"]) - np.mean(a["STALE"]); d2 = np.mean(a["DECOY"]) - np.mean(a["STALE"])
    ok1 = d1 > st; ok2 = d2 < -st
    print(f"G-T3 NCM-RRM - NCM-STALE on POS {d1:+.4f} (step {st:.4f}) -> {'holds' if ok1 else 'FAILS'}")
    print(f"G-T3 NCM-DECOY - NCM-STALE on POS {d2:+.4f} (step {st:.4f}): behind by more than a step -> {'holds' if ok2 else 'FAILS'}")
    print("T3 GATE " + ("OPEN" if ok1 and ok2 else "CLOSED"))
    print("\nreported beside the gate (not gating):")
    for name in ("POS", "NEG2"):
        a = res[name]
        print(f"   {name}: NCM-RRM - NCM-STALE {np.mean(a['RRM']) - np.mean(a['STALE']):+.4f}; NCM-RRM - softmax {np.mean(a['RRM']) - np.mean(a['softmax']):+.4f}; "
              f"NCM-ORACLE - NCM-RRM {np.mean(a['ORACLE']) - np.mean(a['RRM']):+.4f}")


if __name__ == "__main__":
    main()
