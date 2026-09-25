"""SCL3 derived counts and ranges quoted in the ledger rows and report (written after scoring, 2026-09-25). It reads
runs/scl3/results_*.jsonl and prints counts the frozen scorer's per-carrier lines imply but do not print as totals; it
changes no verdict. Run: uv run python runs/scl3/counts.py > runs/scl3/counts.txt"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDS = (1468, 188, 1475, 4538, 1478, 300, 40966, 1501, 40982, 1497)
rows, hdr = [], {}
for i in IDS:
    for l in open(ROOT / "runs" / "scl3" / f"results_{i}.jsonl"):
        o = json.loads(l)
        if "arm" in o: rows.append(o)
        elif "excluded" in o: hdr[o["dataset"]] = o
DS = [d for d in hdr if not hdr[d]["excluded"]]; N = len(DS)
def A(d, arm): return sorted([r for r in rows if r["dataset"] == d and r["arm"] == arm], key=lambda r: r["seed"])
print("SCL3 derived counts and ranges (runs/scl3/counts.py)")
print(f"carriers scored {N} of {len(hdr)}")
nat = [r for d in DS for r in A(d, "nat_bsec")]
same = sum(r["theta_sha"] == b["theta_sha"] for d in DS for r, b in zip(A(d, "nat_bsec"), A(d, "base_bsec")))
print(f"SCL3-C: disables 0 in {sum(r['disables'] == 0 for r in nat)}/{len(nat)} runs; identical parameters {same}/{len(nat)}")
for a in ("clock", "occasion", "egoic", "taskself", "indifferent", "nat_lossy", "nat_restart"):
    sh = {d: sum(r["share"] for r in A(d, a)) / len(A(d, a)) for d in DS}; lo = min(sh, key=sh.get); hi = max(sh, key=sh.get)
    print(f"SCL3-V {a}: mean disable share min {sh[lo]:.3f} ({lo}), max {sh[hi]:.3f} ({hi})")
