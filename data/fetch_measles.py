"""Download tsiR's twentymeas.RData (named in prereg/meas/PREREG.md) and write a sha256
manifest. Run ONLY after the prereg hash is committed and pushed (CLAUDE.md R2).

    uv run python data/fetch_measles.py
"""
import datetime as dt
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "measles"; RAW.mkdir(parents=True, exist_ok=True)
MAN = ROOT / "data" / "manifests" / "meas.sha256"
URL = "https://raw.githubusercontent.com/adbecker/tsiR/master/data/twentymeas.RData"

dest = RAW / "twentymeas.RData"
with urllib.request.urlopen(URL, timeout=120) as r, open(dest, "wb") as f:
    f.write(r.read())
h = hashlib.sha256(dest.read_bytes()).hexdigest()
stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
line = f"{h}  {dest.relative_to(ROOT)}  {URL}  (tsiR 0.4.2, master)  downloaded {stamp}  bytes {dest.stat().st_size}"
MAN.parent.mkdir(exist_ok=True); MAN.write_text(line + "\n"); print(line); print("manifest ->", MAN.relative_to(ROOT))
