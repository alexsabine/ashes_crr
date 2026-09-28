"""SEC4 carrier selection (prereg/sec4/PREREG.md): SCL3's rule applied to a third family, the Penn Machine Learning Benchmarks
(PMLB). Metadata only: prereg/sec4/pmlb_all_summary_stats.tsv (PMLB's own summary table, fetched 2026-09-28 from
raw.githubusercontent.com/EpistasisLab/pmlb/master/pmlb/all_summary_stats.tsv). No dataset record is read.
The rule: classification; n_classes >= 4; n_instances >= 400 and <= 1,000,000 (SEC3's loader-cost floor); n_features <= 1000;
not SEEN: the name (lower-cased, '-' read as '_') is not a name in data/SEEN.md, and the dataset does not hold records already
opened under another name (ALIASES, below); K requested = the largest even number <= min(n_classes, 10).
    python3 studies/sec4/select_carriers.py > prereg/sec4/carrier_selection.txt
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TSV = ROOT / "prereg" / "sec4" / "pmlb_all_summary_stats.tsv"
# records opened under another name (data/SEEN.md; SCL3 and SEC3 carriers are OpenML copies of UCI/AutoML sets)
ALIASES = {"shuttle": "OpenML 40685 shuttle (SEC3)", "mnist": "the MNIST family (Split-MNIST)", "covertype": "OpenML 1596 (SEC3)",
           "har": "OpenML 1478 (SCL3)", "isolet": "OpenML 300 (SCL3)", "semeion": "OpenML 1501 (SCL3)", "cnae_9": "OpenML 1468 (SCL3)",
           "wall_robot_navigation": "OpenML 1497 (SCL3)", "steel_plates_fault": "OpenML 40982 (SCL3)", "eucalyptus": "OpenML 188 (SCL3)",
           "segment": "segmentation (PMLB)", "car": "car_evaluation (PMLB)", "kr_vs_k": "krkopt (PMLB)",
           "satellite_image": "satimage (PMLB; 294_satellite_image is the same Landsat records)", "294_satellite_image": "satimage"}


def norm(s): return s.lower().replace("-", "_").strip()


def main():
    seen_txt = (ROOT / "data" / "SEEN.md").read_text()
    seen = {norm(n) for n in re.findall(r"`([A-Za-z0-9_.\-]+)`", seen_txt)}
    seen |= {norm(n) for line in seen_txt.splitlines() for n in re.findall(r"\b\d{2,6} ([A-Za-z][A-Za-z0-9_.\-]+)", line)}
    rows = list(csv.DictReader(open(TSV), delimiter="\t"))
    print(f"SEC4 carrier selection from PMLB's summary table ({len(rows)} datasets; metadata only)")
    chosen = []
    for r in sorted(rows, key=lambda r: norm(r["dataset"])):
        if r["task"] != "classification": continue
        nm = norm(r["dataset"]); n = int(float(r["n_instances"])); f = int(float(r["n_features"])); c = int(float(r["n_classes"]))
        why = None
        if c < 4: continue
        if n < 400: why = f"{n} rows (< 400)"
        elif n > 1_000_000: why = f"{n} rows (> 1000000)"
        elif f > 1000: why = f"{f} features (> 1000)"
        elif nm in seen: why = "SEEN (data/SEEN.md)"
        elif nm.startswith("mfeat_"): why = "SEEN records (mfeat)"
        elif nm in ALIASES: why = f"SEEN records ({ALIASES[nm]})"
        k = min(c, 10); k -= k % 2
        print(f"   {r['dataset'][:36]:36s} rows {n:8d} features {f:5d} classes {c:3d} K {k:2d} -> " + (f"excluded ({why})" if why else "CHOSEN"))
        if not why: chosen.append((r["dataset"], k))
    print(f"chosen ({len(chosen)}): " + "; ".join(f"{d} K {k}" for d, k in chosen))
    print("DATASETS = {" + ", ".join(f"{d!r}: {k}" for d, k in chosen) + "}")


if __name__ == "__main__":
    main()
