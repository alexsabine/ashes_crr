"""SCL3 carrier selection (prereg/scl3/PREREG.md). Metadata only: no dataset record is read.

    uv run python studies/scl3/select_carriers.py fetch     # saves the OpenML-CC18 study record and the data list (qualities) in prereg/scl3/
    uv run python studies/scl3/select_carriers.py > prereg/scl3/carrier_selection.txt

The source is the OpenML-CC18 benchmark suite (OpenML study 99; Bischl et al., "OpenML Benchmarking Suites"): curated, real
classification datasets. The rule, applied to the saved metadata:
  - status active, format ARFF;
  - NumberOfClasses >= 4 and NumberOfInstances >= 400 (SCL2's floors) and NumberOfFeatures <= 1001 (at most 1000 inputs:
    the numpy MLP's compute; the target is counted by OpenML);
  - not SEEN (R11): the name, lower-cased with '-' read as '_', is not a name in data/SEEN.md, and the dataset does not
    hold the same records as a SEEN one (ALIASES below: the six mfeat-* feature sets share the same 2000 digit records;
    OpenML 'segment' is PMLB 'segmentation', 'car' is 'car_evaluation', 'LED-display-domain-7digit' is 'led7'; the
    MNIST family and CIFAR-10 are SEEN as Split-* streams);
  - K requested = the largest even number <= min(NumberOfClasses, 10), as SCL2.
Every CC18 dataset is printed with its decision and reason."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "prereg" / "scl3"
STUDY_JSON = OUT / "openml_cc18_study99.json"; LIST_JSON = OUT / "openml_cc18_datalist.json"
ALIASES = {"segment": "segmentation (PMLB)", "car": "car_evaluation (PMLB)", "led_display_domain_7digit": "led7 (PMLB)",
           "kr_vs_k": "krkopt (PMLB)", "mnist_784": "Split-MNIST (MNIST family)", "fashion_mnist": "Split-Fashion-MNIST",
           "cifar_10": "Split-CIFAR-10"}


def norm(s): return s.lower().replace("-", "_").strip()


def fetch():
    subprocess.run(["curl", "-sSfL", "--retry", "3", "-o", str(STUDY_JSON), "https://www.openml.org/api/v1/json/study/99"], check=True)
    ids = find_ids(json.loads(STUDY_JSON.read_text()))
    url = "https://www.openml.org/api/v1/json/data/list/data_id/" + ",".join(str(i) for i in ids) + "/status/all/limit/1000"
    subprocess.run(["curl", "-sSfL", "--retry", "3", "-o", str(LIST_JSON), url], check=True)
    print(f"saved {STUDY_JSON.relative_to(ROOT)} ({len(ids)} data ids) and {LIST_JSON.relative_to(ROOT)}")


def find_ids(o):
    if isinstance(o, dict):
        if "data_id" in o: return [int(v) for v in (o["data_id"] if isinstance(o["data_id"], list) else [o["data_id"]])]
        for v in o.values():
            r = find_ids(v)
            if r: return r
    if isinstance(o, list):
        for v in o:
            r = find_ids(v)
            if r: return r
    return []


def select():
    seen = {norm(n) for n in re.findall(r"`([A-Za-z0-9_.\-]+)`", (ROOT / "data" / "SEEN.md").read_text())}
    ids = set(find_ids(json.loads(STUDY_JSON.read_text())))
    rows = json.loads(LIST_JSON.read_text())["data"]["dataset"]
    print("SCL3 carrier selection from the OpenML-CC18 study record (study 99) and data list saved in prereg/scl3/ (metadata only)")
    print(f"CC18 data ids in the study record: {len(ids)}; rows in the data list: {len(rows)}")
    chosen = []
    for r in sorted(rows, key=lambda r: norm(r["name"])):
        q = {x["name"]: x["value"] for x in r.get("quality", [])}
        n = int(float(q.get("NumberOfInstances", 0))); c = int(float(q.get("NumberOfClasses", 0))); f = int(float(q.get("NumberOfFeatures", 0)))
        miss = int(float(q.get("NumberOfMissingValues", 0))); nm = norm(r["name"])
        why = None
        if int(r["did"]) not in ids: why = "not in the study record"
        elif r.get("status") != "active": why = f"status {r.get('status')}"
        elif r.get("format", "").upper() != "ARFF": why = f"format {r.get('format')}"
        elif c < 4: why = f"{c} classes (< 4)"
        elif n < 400: why = f"{n} rows (< 400)"
        elif f > 1001: why = f"{f} features (> 1001)"
        elif nm in seen: why = "SEEN (data/SEEN.md)"
        elif nm.startswith("mfeat_"): why = "SEEN records (the mfeat feature sets share the same 2000 digits)"
        elif nm in ALIASES: why = f"SEEN records ({ALIASES[nm]})"
        k = min(c, 10); k -= k % 2
        print(f"   {int(r['did']):6d} {r['name'][:36]:36s} v{r.get('version')} rows {n:7d} features {f:5d} classes {c:3d} missing {miss:6d} K requested {k:2d} -> "
              + (f"excluded ({why})" if why else "CHOSEN"))
        if not why: chosen.append((int(r["did"]), r["name"], k))
    print(f"chosen ({len(chosen)}): " + "; ".join(f"{d} {nm} K {k}" for d, nm, k in chosen))
    print("DATASETS = {" + ", ".join(f"{d}: ({nm!r}, {k}, 2)" for d, nm, k in chosen) + "}")


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else select()
