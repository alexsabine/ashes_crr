"""SEC4 carrier selection (prereg/sec4/PREREG.md): SCL3's rule with SEC3's two additions, applied to a THIRD family.

PMLB was tried first and is exhausted (prereg/sec4/carrier_selection_pmlb.txt, studies/sec4/select_carriers_pmlb.py: two valid
carriers, solar_flare_2 and kddcup). The third family is therefore the pooled OpenML benchmark suites that are neither CC18
(SCL3's family, study 99) nor the AutoML Benchmark classification suite of 2021 (SEC3's family, study 271):
    study 14   OpenML-100 (2017)
    study 218  AutoML Benchmark (2019)
    study 379  TabZilla Hard Datasets
    study 457  TabArena-v0.1 Suite
Metadata only: the study records and one data list (qualities), saved in prereg/sec4/. No dataset record is read.

    uv run python studies/sec4/select_carriers.py fetch
    uv run python studies/sec4/select_carriers.py > prereg/sec4/carrier_selection.txt

The rule, applied to the saved metadata:
  - status active, format ARFF;
  - NumberOfClasses >= 4, NumberOfInstances >= 400 and <= 1,000,000 (SEC3's loader-cost floor), NumberOfFeatures <= 1001;
  - not SEEN (R11): the OpenML id is listed in data/SEEN.md; or the name (lower-cased, '-' read as '_') is a name in
    data/SEEN.md; or the dataset holds records already opened under another name (ALIASES, below);
  - datasets holding the same records under different feature sets (SHARED) count once: the lowest OpenML id is kept;
  - K requested = the largest even number <= min(NumberOfClasses, 10), as SCL2.
OpenML-100 (study 14) was first unreachable (a timeout on 2026-09-28) and was fetched on a retry the same day, before the
selection was run on it. Every pooled dataset is printed once with its decision and reason."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "prereg" / "sec4"
STUDIES = (14, 218, 379, 457)
LIST_JSON = OUT / "openml_suites_datalist.json"
MAX_ROWS_META = 1_000_000
# records opened under another name (data/SEEN.md): SEC3's and PMLB's aliases, plus the MNIST/CIFAR families
ALIASES = {"segment": "segmentation (PMLB)", "car": "car_evaluation (PMLB)", "led_display_domain_7digit": "led7 (PMLB)",
           "kr_vs_k": "krkopt (PMLB)", "mnist_784": "Split-MNIST (MNIST family)", "fashion_mnist": "Split-Fashion-MNIST",
           "cifar_10": "Split-CIFAR-10", "satellite_image": "satimage (PMLB)", "kddcup99": "SEEN name kddcup (PMLB table)"}


# unseen datasets that hold the SAME records under different feature sets: one carrier per group (the lowest OpenML id),
# so that N counts independent record sets (declared in PREREG.md; the rule is SEC4's, the mfeat analogue of R11)
SHARED = {"one_hundred_plants_margin": "the 1600 one-hundred-plants leaves", "one_hundred_plants_shape": "the 1600 one-hundred-plants leaves",
          "one_hundred_plants_texture": "the 1600 one-hundred-plants leaves"}


def SHARED_IDS(rows): return [(int(r["did"]), norm(r["name"])) for r in rows]


def norm(s): return s.lower().replace("-", "_").strip()


def study_json(s): return OUT / f"openml_study{s}.json"


def study_ids(s):
    st = json.loads(study_json(s).read_text())["study"]
    return {int(v) for v in st["data"]["data_id"]}


def fetch():
    ids = set()
    for s in STUDIES:
        subprocess.run(["curl", "-sSfL", "--retry", "3", "-o", str(study_json(s)), f"https://www.openml.org/api/v1/json/study/{s}"], check=True)
        ids |= study_ids(s)
    url = "https://www.openml.org/api/v1/json/data/list/data_id/" + ",".join(str(i) for i in sorted(ids)) + "/status/all/limit/1000"
    subprocess.run(["curl", "-sSfL", "--retry", "3", "-o", str(LIST_JSON), url], check=True)
    print(f"saved {len(STUDIES)} study records ({len(ids)} distinct data ids) and {LIST_JSON.relative_to(ROOT)}")


def select():
    seen_txt = (ROOT / "data" / "SEEN.md").read_text()
    seen = {norm(n) for n in re.findall(r"`([A-Za-z0-9_.\-]+)`", seen_txt)}
    seen_ids = {int(m) for line in seen_txt.splitlines() if "OpenML" in line for m in re.findall(r"\b(\d{1,6}) [A-Za-z]", line)}
    seen |= {norm(n) for line in seen_txt.splitlines() if "OpenML" in line for n in re.findall(r"\b\d{1,6} ([A-Za-z][A-Za-z0-9_.\-]+)", line)}
    member = {}
    for s in STUDIES:
        for i in study_ids(s): member.setdefault(i, []).append(s)
    rows = json.loads(LIST_JSON.read_text())["data"]["dataset"]
    print("SEC4 carrier selection (SCL3's rule + SEC3's additions) from the pooled OpenML suites 14 (OpenML-100), 218 (AutoML Benchmark 2019), "
          "379 (TabZilla Hard), 457 (TabArena v0.1); metadata saved in prereg/sec4/")
    print(f"distinct data ids across the study records: {len(member)}; rows in the data list: {len(rows)}; "
          f"OpenML ids listed in data/SEEN.md: {len(seen_ids)}")
    chosen = []
    for r in sorted(rows, key=lambda r: (norm(r["name"]), int(r["did"]))):
        q = {x["name"]: x["value"] for x in r.get("quality", [])}
        n = int(float(q.get("NumberOfInstances", 0))); c = int(float(q.get("NumberOfClasses", 0) or 0)); f = int(float(q.get("NumberOfFeatures", 0)))
        miss = int(float(q.get("NumberOfMissingValues", 0) or 0)); nm = norm(r["name"]); did = int(r["did"])
        why = None
        if did not in member: why = "not in the study records"
        elif r.get("status") != "active": why = f"status {r.get('status')}"
        elif r.get("format", "").upper() != "ARFF": why = f"format {r.get('format')}"
        elif c < 4: why = f"{c} classes (< 4)"
        elif n < 400: why = f"{n} rows (< 400)"
        elif f > 1001: why = f"{f} features (> 1001)"
        elif n > MAX_ROWS_META: why = f"{n} rows (> {MAX_ROWS_META}; SEC3's loader-cost floor)"
        elif did in seen_ids: why = "SEEN (OpenML id in data/SEEN.md)"
        elif nm in seen: why = "SEEN (name in data/SEEN.md)"
        elif nm.startswith("mfeat_"): why = "SEEN records (the mfeat feature sets share the same 2000 digits)"
        elif nm in ALIASES: why = f"SEEN records ({ALIASES[nm]})"
        elif nm in SHARED and did != min(d for d, n2 in SHARED_IDS(rows) if SHARED.get(n2) == SHARED[nm]):
            why = f"shares its records with a lower OpenML id ({SHARED[nm]}): counted once"
        k = min(c, 10); k -= k % 2
        print(f"   {did:6d} {r['name'][:36]:36s} v{r.get('version')} studies {','.join(map(str, member.get(did, [])))} rows {n:7d} features {f:5d} "
              f"classes {c:3d} missing {miss:7d} K requested {k:2d} -> " + (f"excluded ({why})" if why else "CHOSEN"))
        if not why: chosen.append((did, r["name"], k))
    print(f"chosen ({len(chosen)}): " + "; ".join(f"{d} {nm} K {k}" for d, nm, k in chosen))
    print("DATASETS = {" + ", ".join(f"{d}: ({nm!r}, {k}, 2)" for d, nm, k in chosen) + "}")


if __name__ == "__main__":
    fetch() if sys.argv[1:] == ["fetch"] else select()
