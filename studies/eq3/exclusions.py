"""Tabulate the pre-registered exclusions of study EQ3: runs whose final parameters were non-finite (scored 0, kept),
per carrier / regime / method / mode, and the data-side counts of every header (NaN rows, extra classes, subsample,
class counts). Run after the carrier runs: uv run python studies/eq3/exclusions.py > runs/eq3/exclusions.txt"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
runs = Counter(); bad = Counter(); headers = {}
for p in sorted((ROOT / "runs" / "eq3").glob("results_*.jsonl")):
    for line in open(p):
        if not line.startswith("{"):
            continue
        o = json.loads(line)
        if "acc" not in o:
            headers[o["dataset"]] = o
            continue
        k = (o["dataset"], o["regime"], o["method"], o["mode"]); runs[k] += 1
        if not o["finite"]:
            bad[k] += 1
print(f"{'carrier':20s} {'regime':6s} {'method':8s} {'mode':10s} {'runs':>5s} {'non-finite':>10s}")
for k in sorted(runs):
    if bad[k]:
        print(f"{k[0]:20s} {k[1]:6s} {k[2]:8s} {k[3]:10s} {runs[k]:5d} {bad[k]:10d}")
print(f"total runs {sum(runs.values())}, non-finite {sum(bad.values())} (kept, scored 0, as pre-registered)")
for d, h in sorted(headers.items()):
    empty = [c for c, n in enumerate(h["class_counts"]) if n == 0]; small = [(c, n) for c, n in enumerate(h["class_counts"]) if 0 < n < 50]
    print(f"{d}: rows dropped for NaN {h['rows_dropped_nan']}; rows dropped beyond the used classes {h['rows_dropped_extra_classes']}; "
          f"rows before/after the pre-registered subsample {h['n_before_subsample']}/{h['n']}; class counts {h['class_counts']}"
          + (f"; classes with 0 rows after {'the pre-registered subsample (their share of 5000 rows rounds to 0)' if h['n_before_subsample'] > h['n'] else 'the NaN rule'} (their task has one class): {empty}" if empty else "") + (f"; classes under 50 rows: {small}" if small else ""))
