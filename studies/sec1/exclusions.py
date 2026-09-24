"""Tabulate the pre-registered exclusions of study SEC1: runs whose final parameters were non-finite (scored 0, kept), per
carrier / mode; calibration fallbacks (s_j = 1) per carrier and mode; carriers excluded by the class-selection rule (K < 4);
and the data-side counts of every header. Run after the carrier runs: uv run python runs/sec1/frozen/exclusions.py > runs/sec1/exclusions.txt"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] if Path(__file__).resolve().parent.name == "frozen" else Path(__file__).resolve().parents[2]
runs = Counter(); bad = Counter(); fb = Counter(); ntask = Counter(); headers = {}
for p in sorted((ROOT / "runs" / "sec1").glob("results_*.jsonl")):
    for line in open(p):
        if not line.startswith("{"):
            continue
        o = json.loads(line)
        if "acc" not in o:
            headers[o["dataset"]] = o
            continue
        k = (o["dataset"], o["mode"]); runs[k] += 1; bad[k] += (not o["finite"]); fb[k] += o["n_fallback"]; ntask[k] += len(o["s"])
print(f"{'carrier':20s} {'mode':10s} {'runs':>5s} {'non-finite':>10s} {'fallback tasks':>15s}")
for k in sorted(runs):
    print(f"{k[0]:20s} {k[1]:10s} {runs[k]:5d} {bad[k]:10d} {fb[k]:8d} of {ntask[k]}")
print(f"total runs {sum(runs.values())}, non-finite {sum(bad.values())} (kept, scored 0, as pre-registered); calibration fallbacks {sum(fb.values())} of {sum(ntask.values())} task-ends")
excluded = [d for d, h in headers.items() if h.get("excluded")]
print(f"carriers excluded by the class-selection rule (K < 4): {excluded or 'none'}")
for d, h in sorted(headers.items()):
    print(f"{d}: classes in file {h['classes_in_file']} (row counts, ranked) {h['class_counts_file']}; requested K {h['classes_requested']}, used K {h['classes_used']}; "
          f"rows dropped for NaN {h['rows_dropped_nan']}; rows in file/after selection and subsample {h['n_file']}/{h['n']}; class counts used {h['class_counts']}; sha256 {h['sha256']}")
