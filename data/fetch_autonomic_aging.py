"""Download PhysioNet Autonomic Aging 1.0.0 records 0061-0090 (.hea + .dat), the records pre-registered in
prereg/card/PREREG.md (tag prereg-card-2026-09-15), and write a sha256 manifest. Run ONLY after the decision to run CARD
is pushed (labs/L03_pulse/LAB.md; AGENT_LOG 164). Files go to data/raw/autonomic_aging/ (gitignored).

    uv run python data/fetch_autonomic_aging.py
"""
import datetime as dt
import hashlib
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "autonomic_aging"; RAW.mkdir(parents=True, exist_ok=True)
MAN = ROOT / "data" / "manifests" / "card.sha256"
BASE = "https://physionet.org/files/autonomic-aging-cardiovascular/1.0.0/"
RECORDS = [f"{i:04d}" for i in range(61, 91)]

def remote_size(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=120) as r:
        return int(r.headers["Content-Length"])


def fetch(url, dest):
    """Resumable: a file already present with the server's Content-Length is kept; otherwise download, up to 5 tries
    with backoff 2, 4, 8, 16 s (the first run of 2026-09-26 lost its proxy tunnel at 0068.dat)."""
    for k in range(5):
        try:
            size = remote_size(url)
            if dest.exists() and dest.stat().st_size == size:
                return
            with urllib.request.urlopen(url, timeout=300) as r:
                data = r.read()
            if len(data) != size:
                raise IOError(f"short read {len(data)} of {size}")
            dest.write_bytes(data)
            return
        except Exception as e:  # noqa: BLE001
            print(f"retry {k + 1} for {url}: {e}", flush=True)
            time.sleep(2 ** (k + 1))
    raise SystemExit(f"failed: {url}")


lines = []
for rec in RECORDS:
    for ext in ("hea", "dat"):
        url = f"{BASE}{rec}.{ext}"
        dest = RAW / f"{rec}.{ext}"
        fetch(url, dest)
        h = hashlib.sha256(dest.read_bytes()).hexdigest()
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        line = f"{h}  {dest.relative_to(ROOT)}  {url}  (autonomic-aging-cardiovascular 1.0.0)  downloaded {stamp}  bytes {dest.stat().st_size}"
        lines.append(line)
        print(line, flush=True)
MAN.parent.mkdir(exist_ok=True); MAN.write_text("\n".join(lines) + "\n"); print("manifest ->", MAN.relative_to(ROOT))
