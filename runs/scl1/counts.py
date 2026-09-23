"""SCL1 derived counts and ranges quoted in the ledger rows (written after scoring, 2026-09-23; AGENT_LOG 103). It reads
runs/scl1/results_*.jsonl and prints numbers the frozen scorer's lines imply but do not print as counts; it changes no
verdict. Run: uv run python runs/scl1/counts.py > runs/scl1/counts.txt"""
import json, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
DS = ("mfeat_factors", "mfeat_morphological", "led7", "led24", "krkopt", "fars", "satimage", "segmentation", "yeast", "wine_quality_white", "sleep", "page_blocks")
rows = [json.loads(l) for d in DS for l in open(ROOT / "runs" / "scl1" / f"results_{d}.jsonl") if '"arm"' in l]
def A(d, arm): return sorted([r for r in rows if r["dataset"] == d and r["arm"] == arm], key=lambda r: r["seed"])
def m(d, arm, k): return float(np.mean([r[k] for r in A(d, arm)]))
def step(v): return max(1.0, 2 * float(np.std(v, ddof=1)) / math.sqrt(len(v)))
print("SCL1 derived counts and ranges (runs/scl1/counts.py)")
for a in ("clock", "occasion", "egoic", "taskself"):
    sh = {d: m(d, a, "share") for d in DS}; lo = min(sh, key=sh.get); hi = max(sh, key=sh.get)
    print(f"SCL1-2 {a}: disable share min {sh[lo]:.3f} ({lo}), max {sh[hi]:.3f} ({hi})")
for w in ("lossy", "restart"):
    sh = {d: m(d, f"nat_{w}", "share") for d in DS}; lo = min(sh, key=sh.get); hi = max(sh, key=sh.get)
    print(f"SCL1-3 natural {w}: disable share min {sh[lo]:.3f} ({lo}), max {sh[hi]:.3f} ({hi})")
for a in ("clock", "occasion"):
    dd = {d: m(d, a, "late_share") - m(d, "stat_" + a, "late_share") for d in DS}
    print(f"SCL1-D {a}: continual − stationary positive on {sum(v > 0 for v in dd.values())}/12; min {min(dd.values()):+.3f} ({min(dd, key=dd.get)}), max {max(dd.values()):+.3f} ({max(dd, key=dd.get)})")
ne = {d: np.array([r['acc'] for r in A(d, 'fc_wallclock')]) - np.array([r['acc'] for r in A(d, 'base_eq')]) for d in DS}
print(f"SCL1-E: parameters differ in {sum(r['theta_sha'] != b['theta_sha'] for d in DS for r, b in zip(A(d, 'fc_wallclock'), A(d, 'base_eq')))}/60 runs; "
      f"mean difference min {min(v.mean() for v in ne.values()):+.4f}, max {max(v.mean() for v in ne.values()):+.4f}")
for w in ("lossy", "restart"):
    dd = {d: np.array([r['acc'] for r in A(d, f'fc_{w}')]) - np.array([r['acc'] for r in A(d, 'base_eq')]) for d in DS}
    ahead = [d for d, v in dd.items() if v.mean() >= step(v)]; behind = [d for d, v in dd.items() if v.mean() <= -step(v)]
    print(f"SCL1-F {w}: ahead of no operator by a step on {len(ahead)}/12 {ahead}; behind by a step on {len(behind)}/12 {behind}; within a step on {12 - len(ahead) - len(behind)}/12")
for arm in ("nat_eq", "clock"):
    v = {d: m(d, arm, "wall") / m(d, arm, "updates") for d in DS}
    print(f"SCL1-O {arm}: wall steps per update min {min(v.values()):.4f}, max {max(v.values()):.4f} (ratio of means)")
print(f"SCL1-1: disables 0 in {sum(r['disables'] == 0 for d in DS for r in A(d, 'nat_eq'))}/60 runs; identical parameters {sum(r['theta_sha'] == b['theta_sha'] for d in DS for r, b in zip(A(d, 'nat_eq'), A(d, 'base_eq')))}/60")
