"""Download OpenML datasets (by data id) named in a study's PREREG.md and write a sha256 manifest.
Run ONLY after the prereg hash is pushed (CLAUDE.md R2) and on the day the prereg allows (R3).

    uv run python data/fetch_openml.py --manifest <study> <data_id> ...

For each id: the dataset description (JSON, OpenML API v1) is saved beside the file (it names the target attribute, the
row-id and ignore attributes and the file's md5); the ARFF file is downloaded from the description's url; its md5 is
checked against the description's md5_checksum (an independent integrity check, as fetch_pmlb.py checks the Git LFS oid);
the manifest records the sha256 of the ARFF and of the description, the url, the version and the download time.
Transport is curl (the proxy CA bundle is accepted by curl but rejected by Python 3.14's OpenSSL; see fetch_pmlb.py).
"""
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "openml"; RAW.mkdir(parents=True, exist_ok=True)
ARGS = sys.argv[1:]
if "--manifest" not in ARGS: raise SystemExit(__doc__)
STUDY = ARGS.pop(ARGS.index("--manifest") + 1); ARGS.remove("--manifest")
MAN = ROOT / "data" / "manifests" / f"{STUDY}.sha256"
API = "https://www.openml.org/api/v1/json/data/{i}"


def curl(url, dest):
    subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "900", "-o", str(dest), url], check=True)


def digest(p, algo):
    h = hashlib.new(algo)
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()


lines = []
for i in ARGS:
    tmp = RAW / f"{i}.desc.tmp"; curl(API.format(i=int(i)), tmp)
    desc = json.loads(tmp.read_text())["data_set_description"]
    name = desc["name"]; stem = f"{int(i)}_{name}"
    djson = RAW / f"{stem}.json"; tmp.rename(djson)
    assert desc.get("format", "").upper() == "ARFF", f"{i}: format {desc.get('format')} (only ARFF is read)"
    dest = RAW / f"{stem}.arff"; curl(desc["url"], dest)
    md5 = digest(dest, "md5")
    assert md5 == desc["md5_checksum"], f"{i} {name}: md5 {md5} != description md5_checksum {desc['md5_checksum']}"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines.append(f"{digest(dest, 'sha256')}  {dest.relative_to(ROOT)}  {desc['url']}  md5-verified  version {desc.get('version')}  "
                 f"downloaded {stamp}  bytes {dest.stat().st_size}")
    lines.append(f"{digest(djson, 'sha256')}  {djson.relative_to(ROOT)}  {API.format(i=int(i))}  description  downloaded {stamp}")
    print(lines[-2], flush=True)
MAN.parent.mkdir(exist_ok=True)
MAN.write_text("\n".join(lines) + "\n")
print("manifest ->", MAN.relative_to(ROOT))
