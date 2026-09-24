"""SEC1-X (pre-registered instrument check): on the six EQ4 carriers, SEC1's 'fixed' (coarse grid), 'bayes' and 'eq' (Omega 1)
arms must reproduce runs/eq4/results_*.jsonl per seed exactly (same code path, same random draws).
Run: uv run python runs/sec1/frozen/repro_eq4.py > runs/sec1/repro_eq4.txt"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] if Path(__file__).resolve().parent.name == "frozen" else Path(__file__).resolve().parents[2]
EQ4 = ("satimage", "segmentation", "yeast", "wine_quality_white", "sleep", "page_blocks")
COARSE = (0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0, 10000.0)
n = 0; bad = []
for d in EQ4:
    old = {}
    for line in open(ROOT / "runs" / "eq4" / f"results_{d}.jsonl"):
        o = json.loads(line)
        if "acc" not in o or o["method"] != "ewc" or o["regime"] != "std" or o["smooth"] != 0.9 or o["wcap"] != 1e4: continue
        if o["lr"] != 0.05 or o["bs"] != 10 or o["hidden"] != 256 or o["epochs"] != 3: continue
        if o["mode"] in ("fixed", "bayes") or (o["mode"] == "eq" and o["value"] == 1.0):
            old[(o["mode"], round(o["value"], 6), o["seed"])] = o["acc"]
    for line in open(ROOT / "runs" / "sec1" / f"results_{d}.jsonl"):
        o = json.loads(line)
        if "acc" not in o or o["fs"] != 0.1 or o["fe"] != 0.1: continue
        if (o["mode"] == "fixed" and o["value"] in COARSE) or o["mode"] == "bayes" or (o["mode"] == "eq" and o["value"] == 1.0):
            k = (o["mode"], round(o["value"], 6), o["seed"]); n += 1
            if k not in old: bad.append((d, k, "absent in EQ4")); continue
            if old[k] != o["acc"]: bad.append((d, k, old[k], o["acc"]))
print(f"SEC1-X: {n} runs compared against runs/eq4/results_*.jsonl; mismatches {len(bad)}")
for b in bad[:50]: print("   ", b)
print("SEC1-X " + ("REPRODUCED exactly" if n > 0 and not bad else "NOT REPRODUCED"))
