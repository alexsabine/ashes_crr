"""Download the PMLB datasets named in a study's PREREG.md and write a sha256 manifest.
Run ONLY after the prereg tag exists (CLAUDE.md R2).

    uv run python data/fetch_pmlb.py [--manifest <study>] <name> ...
    uv run python data/fetch_pmlb.py optdigits pendigits letter                 # study EQX (default manifest)
    uv run python data/fetch_pmlb.py --manifest eq2 mfeat_fourier mfeat_pixel texture
"""
import datetime as dt
import hashlib
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "pmlb"; RAW.mkdir(parents=True, exist_ok=True)
ARGS = sys.argv[1:]
STUDY = ARGS.pop(ARGS.index("--manifest") + 1) if "--manifest" in ARGS else "eqx"
if "--manifest" in ARGS: ARGS.remove("--manifest")
MAN = ROOT / "data" / "manifests" / f"{STUDY}.sha256"
# PMLB stores the .tsv.gz files in Git LFS: the raw.githubusercontent URL named in the prereg
# returns a 131-byte pointer carrying the object's sha256 (oid). The bytes come from the LFS
# media host; the pointer's oid is checked against the downloaded file (independent integrity check).
PTR = "https://raw.githubusercontent.com/EpistasisLab/pmlb/master/datasets/{n}/{n}.tsv.gz"
BASE = "https://media.githubusercontent.com/media/EpistasisLab/pmlb/master/datasets/{n}/{n}.tsv.gz"

lines = []
for n in ARGS:
    url = BASE.format(n=n); dest = RAW / f"{n}.tsv.gz"
    with urllib.request.urlopen(PTR.format(n=n), timeout=120) as r:
        ptr = r.read().decode()
    oid = [l.split("sha256:")[1] for l in ptr.splitlines() if l.startswith("oid sha256:")][0]
    # Transport for the LFS object: curl (the proxy CA bundle is accepted by curl but rejected by
    # Python 3.14's OpenSSL for lacking a key-usage extension). Integrity is the oid check below.
    subprocess.run(["curl", "-sSfL", "--max-time", "300", "-o", str(dest), url], check=True)
    h = hashlib.sha256(dest.read_bytes()).hexdigest()
    assert h == oid, f"{n}: sha256 {h} != LFS pointer oid {oid}"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines.append(f"{h}  {dest.relative_to(ROOT)}  {url}  lfs-oid-verified  downloaded {stamp}  bytes {dest.stat().st_size}")
    print(lines[-1], flush=True)
MAN.parent.mkdir(exist_ok=True)
MAN.write_text("\n".join(lines) + "\n")
print("manifest ->", MAN.relative_to(ROOT))
