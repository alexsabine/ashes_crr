"""RRM2 T5 (DECLARATION_2.md Part T, pushed at a2719f0 before this file; runs only if T2's gate opened): development of RRM-1
on the 30 SEEN carriers (DECLARATION.md section 5, RRM-1 alone, no selection).
  D-COUNT  RRM-1 not behind ER-20 by a step (step of ER-20) on >= ceil(0.75 N_dev) carriers
  D-REL    RRM-1 ahead of STALE-1 by a step (step of STALE-1) on >= ceil(N_dev / 3) carriers
Reported: ANCH-1, JOINT, per carrier. Seeds 0-4. Output: t5_dev.txt; per-run records t5_dev.jsonl.
Run: uv run python Relational_Reference_Memory/checks/t5_dev.py
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rrm_lib as L  # noqa: E402
import t_lib as T  # noqa: E402

R = L.R
SEEDS = (0, 1, 2, 3, 4)
OUT = Path(__file__).resolve().parent / "t5_dev.jsonl"


def step_of(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))


def main():
    print("RRM2 T5: development of RRM-1 on the SEEN carriers (DECLARATION_2.md Part T); seeds 0-4; class-IL accuracy (%)")
    rows = []
    with open(OUT, "w") as f:
        for study, did in T.seen_carriers():
            d = T.load_seen_cached(study, did)
            if d is None:
                print(f"{study} {did}: excluded by the loader"); continue
            Xtr, ytr, Xte, yte, K, name = d; data = (Xtr, ytr, Xte, yte)
            a = {k: [] for k in ("ER-20", "ANCH-1", "STALE-1", "RRM-1", "JOINT")}
            for s in SEEDS:
                a["ER-20"].append(R.run_er_pc(s, *data, K, 20)); a["ANCH-1"].append(L.run_rrm(s, *data, K, "1", "anch"))
                a["STALE-1"].append(L.run_rrm(s, *data, K, "1", "stale")); a["RRM-1"].append(L.run_rrm(s, *data, K, "1", "rrm"))
                a["JOINT"].append(R.run_joint(s, *data, K))
            f.write(json.dumps(dict(study=study, did=did, name=name, K=K, **a)) + "\n"); f.flush()
            se = step_of(a["ER-20"]); ss = step_of(a["STALE-1"]); m = np.mean(a["RRM-1"])
            nb = m - np.mean(a["ER-20"]) > -se; ah = m - np.mean(a["STALE-1"]) > ss
            rows.append((name, nb, ah))
            print(f"[{study} {did} {name[:24]}] K {K}: " + "  ".join(f"{k} {np.mean(v):6.2f}" for k, v in a.items())
                  + f"  | RRM-1 - ER-20 {m - np.mean(a['ER-20']):+.4f} (step {se:.4f}) {'not behind' if nb else 'BEHIND'}; "
                  f"RRM-1 - STALE-1 {m - np.mean(a['STALE-1']):+.4f} (step {ss:.4f}) {'ahead' if ah else 'not ahead'}")
    n = len(rows); c1 = sum(r[1] for r in rows); c2 = sum(r[2] for r in rows)
    need1 = math.ceil(0.75 * n); need2 = math.ceil(n / 3)
    print(f"\nN_dev {n}")
    print(f"D-COUNT RRM-1 not behind ER-20 on {c1}/{n} (need {need1}) -> {'holds' if c1 >= need1 else 'FAILS'}")
    print(f"D-REL RRM-1 ahead of STALE-1 on {c2}/{n} (need {need2}) -> {'holds' if c2 >= need2 else 'FAILS'}")
    print("D-GATE " + ("OPEN" if c1 >= need1 and c2 >= need2 else "CLOSED"))


if __name__ == "__main__":
    main()
