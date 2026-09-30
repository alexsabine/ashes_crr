"""RRM2 T2 (DECLARATION_2.md Part T, pushed at a2719f0 before this file): DECLARATION.md section 4's learner gate for RRM-1
alone. Disclosure: part 1 is not blind for this form (its result was known when this test was declared).
  G-REL     on POS, RRM-1 ahead of STALE-1 by more than a step (step of STALE-1)
  G-CANFAIL DECOY-1 behind ER-20 by more than a step (step of ER-20) on POS and on NEG2
  G-FT      FT behind ER-20 by more than a step on both streams
  G-ID      RRM-1 with transport forced off equals STALE-1 bit for bit (10/10)
Reported: RRM-1 - ANCH-1, - ER-20, - JOINT, - IGR-F, - RFR, - HOPDC-1 (Amendment 1: HopDC's transport on the same anchors); memory. Seeds 0-4. Words computed (R15).
Run: uv run python Relational_Reference_Memory/checks/t2_learner.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "Replay_Quality_Memory" / "checks"))
import rrm_lib as L  # noqa: E402
import phase_a as PA  # noqa: E402

R = L.R
SEEDS = (0, 1, 2, 3, 4)


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    print("RRM2 T2: the learner gate for RRM-1 alone (DECLARATION_2.md; part 1 not blind for this form); seeds 0-4; class-IL accuracy (%)")
    print(f"anchors 10/class of task 1 (M 20), beta {L.BETA}, pseudo {L.PSEUDO_BS} + anchors {L.ANCHOR_BS} per step; ER-20 = 20 raw rows per class")
    res = {}; ok = {}
    for name in ("POS", "NEG2"):
        data, K = PA.stream(name)
        a = {k: [] for k in ("FT", "JOINT", "ER-20", "IGR-F", "ANCH-1", "STALE-1", "RRM-1", "DECOY-1", "HOPDC-1")}; ident = []; mem = None
        for s in SEEDS:
            a["FT"].append(R.run_ft(s, *data, K)); a["JOINT"].append(R.run_joint(s, *data, K))
            a["ER-20"].append(R.run_er_pc(s, *data, K, 20)); a["IGR-F"].append(R.run_igr(s, *data, K, "F"))
            a["ANCH-1"].append(L.run_rrm(s, *data, K, "1", "anch")); a["STALE-1"].append(L.run_rrm(s, *data, K, "1", "stale"))
            acc, raw, nums = L.run_rrm(s, *data, K, "1", "rrm", return_mem=True); a["RRM-1"].append(acc); mem = (raw, nums)
            a["DECOY-1"].append(L.run_rrm(s, *data, K, "1", "decoy")); a["HOPDC-1"].append(L.run_rrm(s, *data, K, "1", "hopdc"))
            ident.append(L.run_rrm(s, *data, K, "1", "rrm", force_off=True) == a["STALE-1"][-1])
        rfr = R.run_rfr(*data, K); res[name] = (a, ident, rfr)
        print(f"\n[{name}] K {K}, d {data[0].shape[1]}; RFR (deterministic) {rfr:.2f}; RRM-1 memory: raw rows {mem[0]}, stored numbers {mem[1]}; "
              f"ER-20 raw rows {20 * K}")
        for k, v in a.items():
            print(f"   {k:8} mean {np.mean(v):7.2f}  seeds " + " ".join(f"{x:6.2f}" for x in v))
    print("\n" + "-" * 100)
    a = res["POS"][0]; st = step_of(a["STALE-1"]); d = np.mean(a["RRM-1"]) - np.mean(a["STALE-1"])
    ok["REL"] = d > st
    print(f"G-REL RRM-1 - STALE-1 on POS {d:+.4f} (step {st:.4f}) -> {'holds' if ok['REL'] else 'FAILS'}")
    for name in ("POS", "NEG2"):
        a = res[name][0]; st = step_of(a["ER-20"])
        d = np.mean(a["DECOY-1"]) - np.mean(a["ER-20"]); ok[f"CF-{name}"] = d < -st
        print(f"G-CANFAIL DECOY-1 - ER-20 on {name} {d:+.4f} (step {st:.4f}): behind by more than a step -> {'holds' if ok[f'CF-{name}'] else 'FAILS'}")
        d = np.mean(a["FT"]) - np.mean(a["ER-20"]); ok[f"FT-{name}"] = d < -st
        print(f"G-FT FT - ER-20 on {name} {d:+.4f} (step {st:.4f}) -> {'holds' if ok[f'FT-{name}'] else 'FAILS'}")
    n = sum(sum(res[k][1]) for k in res); ok["ID"] = n == 10
    print(f"G-ID transport forced off == STALE-1 bit for bit: {n}/10 -> {'holds' if ok['ID'] else 'FAILS'}")
    print("T2 GATE " + ("OPEN" if all(ok.values()) else "CLOSED"))
    print("\nreported beside the gate (not gating):")
    for name in ("POS", "NEG2"):
        a, _, rfr = res[name]; m = np.mean(a["RRM-1"])
        print(f"   {name}: RRM-1 - ANCH-1 {m - np.mean(a['ANCH-1']):+.4f}; - ER-20 {m - np.mean(a['ER-20']):+.4f}; - JOINT {m - np.mean(a['JOINT']):+.4f}; "
              f"- IGR-F {m - np.mean(a['IGR-F']):+.4f}; - RFR {m - rfr:+.4f}; - HOPDC-1 {m - np.mean(a['HOPDC-1']):+.4f}")


if __name__ == "__main__":
    main()
