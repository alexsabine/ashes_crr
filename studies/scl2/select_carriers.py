"""SCL2 carrier selection (prereg/scl2/PREREG.md): classification sets in PMLB's summary table with >= 4 classes and
>= 400 rows, not in data/SEEN.md; then the named exclusions. Metadata only: no dataset record is read.
Run: uv run python studies/scl2/select_carriers.py > prereg/scl2/carrier_selection.txt"""
import csv
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
seen_text = (ROOT / "data" / "SEEN.md").read_text()
table = list(csv.DictReader(open(ROOT / "prereg" / "scl2" / "pmlb_all_summary_stats.tsv"), delimiter="\t"))
EXCLUDE = {"mnist": "MNIST-family are SEEN (CLAUDE.md §6)", "poker": "EQ4's extreme-imbalance exclusion", "kddcup": "EQ4's extreme-imbalance exclusion",
           "shuttle": "EQ4's extreme-imbalance exclusion"}
print("SCL2 carrier selection from pmlb/all_summary_stats.tsv (fetched 2026-09-23; metadata only)")
chosen = []
for r in sorted(table, key=lambda r: r["dataset"]):
    if r["task"] != "classification" or float(r["n_classes"]) < 4 or int(r["n_instances"]) < 400: continue
    name = r["dataset"]
    if re.search(r"`" + re.escape(name) + r"`", seen_text): continue
    why = EXCLUDE.get(name) or ("a duplicate of a current dataset" if name.startswith("_deprecated") else None)
    k = min(int(float(r["n_classes"])), 10); k -= k % 2
    print(f"   {name:24s} rows {r['n_instances']:>7s} features {r['n_features']:>4s} classes {int(float(r['n_classes'])):3d} imbalance {float(r['imbalance']):.3f} K requested {k:2d} -> "
          + (f"excluded ({why})" if why else "CHOSEN"))
    if not why: chosen.append(name)
print(f"chosen ({len(chosen)}): " + " ".join(chosen))
