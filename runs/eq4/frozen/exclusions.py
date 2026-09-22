"""Tabulate the pre-registered exclusions of study EQ4: runs whose final parameters were non-finite (scored 0, kept),
per carrier / regime / method / mode; carriers excluded by the class-selection rule (K < 4); and the data-side counts of
every header (NaN rows, class counts in the file and after selection/subsample, the class floor).
Run after the carrier runs: uv run python studies/eq4/exclusions.py > runs/eq4/exclusions.txt"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
runs = Counter(); bad = Counter(); headers = {}
for p in sorted((ROOT / "runs" / "eq4").glob("results_*.jsonl")):
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
excluded = [d for d, h in headers.items() if h.get("excluded")]
print(f"carriers excluded by the class-selection rule (K < 4 after the floor of {next(iter(headers.values()))['class_floor'] if headers else '?'} rows): {excluded or 'none'}")
for d, h in sorted(headers.items()):
    small = [(c, n) for c, n in enumerate(h["class_counts"]) if n < 50]
    print(f"{d}: classes in file {h['classes_in_file']} (row counts, ranked) {h['class_counts_file']}; requested K {h['classes_requested']}, used K {h['classes_used']}"
          f"{' (lowered by the floor)' if h['classes_used'] < min(h['classes_requested'], h['classes_in_file'] - h['classes_in_file'] % 2) else ''}; "
          f"rows dropped for NaN {h['rows_dropped_nan']}; rows in file/after selection and subsample {h['n_file']}/{h['n']}; class counts used {h['class_counts']}"
          + (f"; classes under 50 rows: {small}" if small else "") + ("; EXCLUDED" if h.get("excluded") else ""))
