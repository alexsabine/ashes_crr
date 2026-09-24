"""SCL3-I2: the ARFF loader on OpenML copies of SEEN datasets (their records are in data/SEEN.md; no unseen record is read).
It checks, per file: the md5 against the description, that the reader parses every data line, that the used feature count
is NumberOfFeatures - 1 minus the dropped attributes, the rows dropped for missing values against NumberOfMissingValues > 0,
and the class counts; then the class-selection rule. Files go to a scratch folder outside the repository.
Run: uv run python studies/scl3/loader_check.py <scratch dir> > prereg/scl3/loader_check.txt"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scl3_score as T  # noqa: E402

SEEN_IDS = {182: "satimage", 54: "vehicle", 40984: "segment", 458: "analcatdata_authorship", 469: "analcatdata_dmft", 16: "mfeat-karhunen",
            40499: "texture", 307: "vowel", 40975: "car", 6: "letter", 12: "mfeat-factors", 28: "optdigits"}
tmp = Path(sys.argv[1]); tmp.mkdir(parents=True, exist_ok=True)
ok_all = True
print("SCL3-I2 the ARFF loader on OpenML copies of SEEN datasets")
for did, nm in SEEN_IDS.items():
    dj = tmp / f"{did}.json"
    if not dj.exists(): subprocess.run(["curl", "-sSfL", "-o", str(dj), f"https://www.openml.org/api/v1/json/data/{did}"], check=True)
    d = json.loads(dj.read_text())["data_set_description"]
    fa = tmp / f"{did}.arff"
    if not fa.exists(): subprocess.run(["curl", "-sSfL", "-o", str(fa), d["url"]], check=True)
    md5 = hashlib.md5(fa.read_bytes()).hexdigest() == d["md5_checksum"]
    ql = tmp / f"{did}.q.json"
    if not ql.exists(): subprocess.run(["curl", "-sSfL", "-o", str(ql), f"https://www.openml.org/api/v1/json/data/qualities/{did}"], check=True)
    q = {x["name"]: x["value"] for x in json.loads(ql.read_text())["data_qualities"]["quality"]}
    drop = set()
    for key in ("row_id_attribute", "ignore_attribute"):
        v = d.get(key)
        if v: drop |= set(v if isinstance(v, list) else [v])
    attrs, rows = T.read_arff(fa)
    X, y, dropped, used = T._parse_rows(attrs, rows, d["default_target_attribute"], drop)
    n = int(float(q["NumberOfInstances"])); f = int(float(q["NumberOfFeatures"])); miss = int(float(q.get("NumberOfMissingValues", 0)))
    nstr = sum(1 for a in attrs if a[1] in ("string", "date"))
    ok = md5 and len(rows) == n and len(used) == f - 1 - len(drop) - nstr and (dropped == 0) == (miss == 0) and len(set(y.tolist())) == int(float(q["NumberOfClasses"]))
    Xs, ys, meta = T.select_classes(X, y, min(int(float(q["NumberOfClasses"])), 10) // 2 * 2)
    ok_all &= ok
    print(f"   {did:6d} {nm:24s} md5 {md5}; rows read {len(rows)} of {n}; features used {len(used)} (OpenML {f} incl. target; dropped attrs {len(drop)}; string/date {nstr}); "
          f"rows dropped (missing) {dropped} (OpenML missing values {miss}); classes {len(set(y.tolist()))}; selection K {meta['classes_used']}, n {meta['n']} -> {'ok' if ok else 'MISMATCH'}")
print("SCL3-I2 " + ("holds" if ok_all else "FAILS"))
