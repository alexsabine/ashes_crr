"""Download PhysioNet Autonomic Aging 1.0.0 records 0061-0090 (.hea + .dat), the records pre-registered in
prereg/card/PREREG.md (tag prereg-card-2026-09-15), and write a sha256 manifest. Run ONLY after the decision to run CARD
is pushed (labs/L03_pulse/LAB.md; AGENT_LOG 164). Files go to data/raw/autonomic_aging/ (gitignored).

    uv run python data/fetch_autonomic_aging.py
"""
import datetime as dt
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "autonomic_aging"; RAW.mkdir(parents=True, exist_ok=True)
MAN = ROOT / "data" / "manifests" / "card.sha256"
BASE = "https://physionet.org/files/autonomic-aging-cardiovascular/1.0.0/"
RECORDS = [f"{i:04d}" for i in range(61, 91)]

lines = []
for rec in RECORDS:
    for ext in ("hea", "dat"):
        url = f"{BASE}{rec}.{ext}"
        dest = RAW / f"{rec}.{ext}"
        with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as f:
            f.write(r.read())
        h = hashlib.sha256(dest.read_bytes()).hexdigest()
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        line = f"{h}  {dest.relative_to(ROOT)}  {url}  (autonomic-aging-cardiovascular 1.0.0)  downloaded {stamp}  bytes {dest.stat().st_size}"
        lines.append(line)
        print(line, flush=True)
MAN.parent.mkdir(exist_ok=True); MAN.write_text("\n".join(lines) + "\n"); print("manifest ->", MAN.relative_to(ROOT))
