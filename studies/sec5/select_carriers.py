"""SEC5 carrier selection (prereg/sec5/DEV_DECLARATION.md, PREREG.md): SEC4's eligibility rule, unchanged, applied to a FOURTH
family, with the pooling and cap fixed in DEV_DECLARATION.md before any suite metadata was fetched:
    suites, in order: OpenML study 293 (AutoML Benchmark Training Datasets, 2022), study 454 (New_OpenML_Suite_2025_classification),
    study 445 (IRT Diverse Dataset Benchmark); suites are added in this order until at least MIN_POOL datasets are eligible;
    if the pool then holds more than CAP, CAP are kept: the sorted eligible OpenML ids permuted by numpy default_rng(DRAW_SEED).
    A suite whose record cannot be fetched is skipped and the skip printed.
Metadata only: the study records and one data list (qualities) per suite, saved in prereg/sec5/. No dataset record is read.

    uv run python studies/sec5/select_carriers.py fetch
    uv run python studies/sec5/select_carriers.py > prereg/sec5/carrier_selection.txt

The eligibility rule (SEC4's, studies/sec4/select_carriers.py):
  - status active, format ARFF;
  - NumberOfClasses >= 4, NumberOfInstances >= 400 and <= 1,000,000, NumberOfFeatures <= 1001;
  - not SEEN (R11): the OpenML id is listed in data/SEEN.md; or the name (lower-cased, '-' read as '_') is a name in
    data/SEEN.md; or the dataset holds records already opened under another name (ALIASES);
  - datasets holding the same records under different feature sets (SHARED) count once: the lowest OpenML id is kept;
  - K requested = the largest even number <= min(NumberOfClasses, 10).
Every pooled dataset is printed once with its decision and reason."""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "prereg" / "sec5"
STUDIES = (293, 454, 445)        # the order fixed in DEV_DECLARATION.md
MIN_POOL = 8; CAP = 12; DRAW_SEED = 20260930
MAX_ROWS_META = 1_000_000
# records opened under another name (data/SEEN.md): SEC4's aliases, plus the one-hundred-plants feature sets (SEC4 opened
# the margin set, 1491; shape and texture hold the same 1600 leaves)
ALIASES = {"segment": "segmentation (PMLB)", "car": "car_evaluation (PMLB)", "led_display_domain_7digit": "led7 (PMLB)",
           "kr_vs_k": "krkopt (PMLB)", "mnist_784": "Split-MNIST (MNIST family)", "fashion_mnist": "Split-Fashion-MNIST",
           "cifar_10": "Split-CIFAR-10", "satellite_image": "satimage (PMLB)", "kddcup99": "SEEN name kddcup (PMLB table)",
           "one_hundred_plants_shape": "the 1600 one-hundred-plants leaves (SEC4 opened the margin set, 1491)",
           "one_hundred_plants_texture": "the 1600 one-hundred-plants leaves (SEC4 opened the margin set, 1491)"}
SHARED: dict = {}


def norm(s): return s.lower().replace("-", "_").strip()


def study_json(s): return OUT / f"openml_study{s}.json"


def list_json(s): return OUT / f"openml_study{s}_datalist.json"


def study_ids(s):
    st = json.loads(study_json(s).read_text())["study"]
    return {int(v) for v in st["data"]["data_id"]}


def fetch():
    for s in STUDIES:
        try:
            subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "300", "-o", str(study_json(s)), f"https://www.openml.org/api/v1/json/study/{s}"], check=True)
            ids = sorted(study_ids(s))
            url = "https://www.openml.org/api/v1/json/data/list/data_id/" + ",".join(str(i) for i in ids) + "/status/all/limit/1000"
            subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "300", "-o", str(list_json(s)), url], check=True)
            print(f"study {s}: saved the record ({len(ids)} data ids) and {list_json(s).relative_to(ROOT)}")
        except Exception as e:  # noqa: BLE001
            print(f"study {s}: fetch failed ({e}); skipped")


def eligible_rows(s, seen, seen_ids):
    rows = json.loads(list_json(s).read_text())["data"]["dataset"]; member = study_ids(s); out = []
    for r in sorted(rows, key=lambda r: (norm(r["name"]), int(r["did"]))):
        q = {x["name"]: x["value"] for x in r.get("quality", [])}
        n = int(float(q.get("NumberOfInstances", 0))); c = int(float(q.get("NumberOfClasses", 0) or 0)); f = int(float(q.get("NumberOfFeatures", 0)))
        miss = int(float(q.get("NumberOfMissingValues", 0) or 0)); nm = norm(r["name"]); did = int(r["did"])
        why = None
        if did not in member: why = "not in the study record"
        elif r.get("status") != "active": why = f"status {r.get('status')}"
        elif r.get("format", "").upper() != "ARFF": why = f"format {r.get('format')}"
        elif c < 4: why = f"{c} classes (< 4)"
        elif n < 400: why = f"{n} rows (< 400)"
        elif f > 1001: why = f"{f} features (> 1001)"
        elif n > MAX_ROWS_META: why = f"{n} rows (> {MAX_ROWS_META})"
        elif did in seen_ids: why = "SEEN (OpenML id in data/SEEN.md)"
        elif nm in seen: why = "SEEN (name in data/SEEN.md)"
        elif nm.startswith("mfeat_"): why = "SEEN records (the mfeat feature sets share the same 2000 digits)"
        elif nm in ALIASES: why = f"SEEN records ({ALIASES[nm]})"
        k = min(c, 10); k -= k % 2
        out.append((did, r["name"], r.get("version"), n, f, c, miss, k, why))
    return out


def select():
    seen_txt = (ROOT / "data" / "SEEN.md").read_text()
    seen = {norm(n) for n in re.findall(r"`([A-Za-z0-9_.\-]+)`", seen_txt)}
    seen_ids = {int(m) for line in seen_txt.splitlines() if "OpenML" in line for m in re.findall(r"\b(\d{1,6}) [A-Za-z]", line)}
    seen |= {norm(n) for line in seen_txt.splitlines() if "OpenML" in line for n in re.findall(r"\b\d{1,6} ([A-Za-z][A-Za-z0-9_.\-]+)", line)}
    print("SEC5 carrier selection (SEC4's rule) from OpenML suites 293 (AutoML Benchmark Training Datasets), 454 (New_OpenML_Suite_2025_classification), "
          "445 (IRT Diverse Dataset Benchmark), pooled in that order until >= 8 eligible; cap 12 by a seeded draw; metadata saved in prereg/sec5/")
    print(f"OpenML ids listed in data/SEEN.md: {len(seen_ids)}")
    pool = {}; used = []
    for s in STUDIES:
        if len(pool) >= MIN_POOL: print(f"study {s}: not needed (the pool already holds {len(pool)} >= {MIN_POOL})"); continue
        if not list_json(s).exists(): print(f"study {s}: no saved record (fetch failed): skipped"); continue
        used.append(s); rows = eligible_rows(s, seen, seen_ids)
        print(f"study {s}: {len(rows)} datasets in the data list")
        for did, name, ver, n, f, c, miss, k, why in rows:
            if not why and did in pool: why = f"already in the pool from study {pool[did][0]}"
            print(f"   {did:6d} {name[:36]:36s} v{ver} rows {n:7d} features {f:5d} classes {c:3d} missing {miss:7d} K requested {k:2d} -> "
                  + (f"excluded ({why})" if why else "ELIGIBLE"))
            if not why: pool[did] = (s, name, k)
        print(f"   pool after study {s}: {len(pool)} eligible")
    ids = sorted(pool)
    if len(ids) > CAP:
        perm = np.random.default_rng(DRAW_SEED).permutation(len(ids)); keep = sorted(ids[i] for i in perm[:CAP])
        print(f"pool {len(ids)} > cap {CAP}: kept by the seeded draw (default_rng({DRAW_SEED}) over the sorted ids): {keep}")
    else:
        keep = ids
    print(f"suites used: {used}; chosen ({len(keep)}): " + "; ".join(f"{d} {pool[d][1]} K {pool[d][2]}" for d in keep))
    print("DATASETS = {" + ", ".join(f"{d}: ({pool[d][1]!r}, {pool[d][2]}, 2)" for d in keep) + "}")


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else select()
