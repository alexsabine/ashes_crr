"""OB1-C1 Phase A (Open_Bottlenecks/C1_DECLARATION.md, pushed at 39e86ce before this file): the stability gap under STEP, ARC,
SHUF, KOURK, MECTA-M, ALIGN, ORACLE on S1 (class-IL), S2 (domain-IL), S0 (no switch). Seeds 0-4; step = max(1, 2 x SE over
seeds) of the comparator. Gate: G-POS, G-TIME, G-DISC, G-HARM, G-FAIL (words computed, R15). Also printed (implementation
check, not gating): ARC with r forced to 1 equals STEP bit for bit.
Run: uv run python Open_Bottlenecks/checks/c1_phase_a.py
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import c1_lib as C  # noqa: E402

SEEDS = (0, 1, 2, 3, 4)


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    print("OB1-C1 Phase A: arc-clocked Adam moments against the stability gap (C1_DECLARATION.md); seeds 0-4")
    print(f"Adam lr {C.LR}, beta1 {C.B1}, beta2 {C.B2}, batch {C.BS}, {C.EPOCHS} epochs per task, {C.HID} hidden; rho {C.RHO}, "
          f"R_MAX {C.R_MAX}, SG window {C.SG_WINDOW} steps")
    print("CHOICES: see c1_lib.py docstring (ARC's arc sets the next step's decay; KOURK uses the current gradient; MECTA-M's D "
          "is the mean over units)")
    res = {}; ident = []
    for sname in ("S1", "S2", "S0"):
        tasks, K = C.stream(sname); res[sname] = {a: [] for a in C.ARMS}
        for s in SEEDS:
            arc = C.run(s, tasks, K, "ARC"); res[sname]["ARC"].append(arc)
            for a in C.ARMS:
                if a == "ARC":
                    continue
                res[sname][a].append(C.run(s, tasks, K, a, r_seq=arc["r"]))
            ident.append(C.run(s, tasks, K, "ARC", force_r1=True)["final"] == res[sname]["STEP"][-1]["final"])
        print(f"\n[{sname}] {len(tasks)} tasks; steps {res[sname]['STEP'][0]['n_steps']}")
        print(f"   {'arm':8} {'avg-SG':>8} {'min-ACC':>8} {'final':>8}   avg-SG per seed")
        for a in C.ARMS:
            r = res[sname][a]
            print(f"   {a:8} {np.mean([x['sg'] for x in r]):8.2f} {np.mean([x['minacc'] for x in r]):8.2f} "
                  f"{np.mean([x['final'] for x in r]):8.2f}   " + " ".join(f"{x['sg']:6.2f}" for x in r))
        rr = np.concatenate([np.array(x["r"]) for x in res[sname]["ARC"]])
        print(f"   ARC's r: median {np.median(rr):.3f}, 99th percentile {np.percentile(rr, 99):.3f}, max {rr.max():.3f}, "
              f"share at R_MAX {np.mean(rr >= C.R_MAX):.4f}")
    print("\n" + "-" * 100)
    sg = lambda s, a: [x["sg"] for x in res[s][a]]  # noqa: E731
    ok = {}
    for s in ("S1", "S2"):
        d = np.mean(sg(s, "ARC")) - np.mean(sg(s, "STEP")); st = step_of(sg(s, "STEP")); ok[f"POS-{s}"] = d < -st
        print(f"G-POS {s}: ARC - STEP avg-SG {d:+.4f} (step {st:.4f}) -> {'holds' if ok[f'POS-{s}'] else 'FAILS'}")
    for s in ("S1", "S2"):
        d = np.mean(sg(s, "ARC")) - np.mean(sg(s, "SHUF")); st = step_of(sg(s, "SHUF")); ok[f"TIME-{s}"] = d < -st
        print(f"G-TIME {s}: ARC - SHUF avg-SG {d:+.4f} (step {st:.4f}) -> {'holds' if ok[f'TIME-{s}'] else 'FAILS'}")
    disc = {}
    for s in ("S1", "S2"):
        dk = np.mean(sg(s, "ARC")) - np.mean(sg(s, "KOURK")); sk = step_of(sg(s, "KOURK"))
        dm = np.mean(sg(s, "ARC")) - np.mean(sg(s, "MECTA-M")); sm = step_of(sg(s, "MECTA-M"))
        disc[s] = dk < -sk and dm < -sm
        print(f"G-DISC {s}: ARC - KOURK {dk:+.4f} (step {sk:.4f}); ARC - MECTA-M {dm:+.4f} (step {sm:.4f}) -> "
              f"{'beats both' if disc[s] else 'does not beat both'}")
    ok["DISC"] = disc["S1"] or disc["S2"]
    print(f"G-DISC (on at least one stream) -> {'holds' if ok['DISC'] else 'FAILS'}")
    fa = [x["final"] for x in res["S0"]["ARC"]]; fs = [x["final"] for x in res["S0"]["STEP"]]
    d = np.mean(fa) - np.mean(fs); st = step_of(fs); ok["HARM"] = d >= -st
    print(f"G-HARM S0: ARC - STEP final accuracy {d:+.4f} (step {st:.4f}): not behind by more than a step -> {'holds' if ok['HARM'] else 'FAILS'}")
    d = np.mean(sg("S1", "ORACLE")) - np.mean(sg("S1", "STEP")); st = step_of(sg("S1", "STEP")); ok["FAIL"] = d < -st
    print(f"G-FAIL S1: ORACLE - STEP avg-SG {d:+.4f} (step {st:.4f}): moment resets move the dip -> {'holds' if ok['FAIL'] else 'FAILS'}")
    print(f"implementation check (not gating): ARC with r forced to 1 == STEP bit for bit (final accuracy): {sum(ident)}/{len(ident)}")
    print("C1 GATE " + ("OPEN" if all(ok.values()) else "CLOSED"))
    print("\nreported (not gating): ALIGN - STEP avg-SG " + ", ".join(
        f"{s} {np.mean(sg(s, 'ALIGN')) - np.mean(sg(s, 'STEP')):+.4f}" for s in ("S1", "S2")))


if __name__ == "__main__":
    main()
