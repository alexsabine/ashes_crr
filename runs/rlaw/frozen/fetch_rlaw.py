"""Download the RLAW sources named in prereg/rlaw/PREREG.md and write data/manifests/rlaw.sha256.
Run ONLY after the RLAW prereg hash is pushed (CLAUDE.md R2) and on or after the day the prereg allows (R3).

    uv run python data/fetch_rlaw.py

Transport is curl (see fetch_pmlb.py for why). Each file's sha256, url, HTTP Last-Modified (when sent) and download time go
into the manifest. The SPF workbook is checked to be a zip (xlsx) because the Philadelphia Fed returns HTTP 200 with an
HTML page for a wrong path. Raw files stay under data/raw/rlaw/ (gitignored); the S&P and Dow Jones files may not be
reproduced (FRED notes), so only their sha256 is committed, as for every file here."""
import datetime as dt
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists())  # works from data/ and from runs/rlaw/frozen/
RAW = ROOT / "data" / "raw" / "rlaw"
MAN = ROOT / "data" / "manifests" / "rlaw.sha256"

FRED = {  # series: (cosd, coed)
    "CPIAUCSL": ("1967-01-01", "2026-08-01"), "UNRATE": ("1968-01-01", "2026-08-01"), "HOUST": ("1968-01-01", "2026-08-01"),
    "TB3MS": ("1981-01-01", "2026-08-01"), "GS10": ("1991-01-01", "2026-08-01"), "CPILFESL": ("2006-01-01", "2026-08-01"),
    "PCEPI": ("2006-01-01", "2026-07-01"), "PCEPILFE": ("2006-01-01", "2026-07-01"), "MICH": ("1978-01-01", "2024-03-01"),
    "VIXCLS": ("2016-09-26", "2026-09-22"), "SP500": ("2016-09-26", "2026-09-22"),
    "VXNCLS": ("2001-02-02", "2026-09-22"), "NASDAQ100": ("2001-02-01", "2026-09-22"),
    "OVXCLS": ("2007-05-10", "2026-09-22"), "DCOILWTICO": ("2007-05-09", "2026-09-22"),
    "EVZCLS": ("2007-11-01", "2025-03-11"), "DEXUSEU": ("2007-10-31", "2025-03-11"),
    "VXDCLS": ("2016-09-26", "2026-09-22"), "DJIA": ("2016-09-26", "2026-09-22"),
}
SPF = "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/survey-of-professional-forecasters/historical-data/medianLevel.xlsx"
USCRN = "https://www.ncei.noaa.gov/pub/data/uscrn/products/daily01/2025/"
KOOL = "https://raw.githubusercontent.com/wkool/tradeoffs/6f849e13a8fe32c0b62ad768d3578068b93ee69e/data/daw%20paradigm/"


def curl(url, dest):
    hdr = dest.with_suffix(dest.suffix + ".headers")
    subprocess.run(["curl", "-sSfL", "--retry", "3", "--max-time", "900", "-D", str(hdr), "-o", str(dest), url], check=True)
    h = hdr.read_text(errors="replace"); hdr.unlink()
    lm = re.findall(r"(?im)^last-modified:\s*(.+?)\s*$", h); ct = re.findall(r"(?im)^content-type:\s*(.+?)\s*$", h)
    return (lm[-1] if lm else "none"), (ct[-1] if ct else "none")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()


def main():
    lines = []
    def rec(dest, url, lm, extra=""):
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        lines.append(f"{sha(dest)}  {dest.relative_to(ROOT)}  {url}  last-modified {lm}  downloaded {stamp}  bytes {dest.stat().st_size}{extra}")
        print(lines[-1], flush=True)
    (RAW / "fred").mkdir(parents=True, exist_ok=True)
    for s, (a, b) in FRED.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}&cosd={a}&coed={b}"; dest = RAW / "fred" / f"{s}.csv"
        lm, ct = curl(url, dest); head = dest.read_text()[:200]
        assert "," in head.splitlines()[0] and s in head.splitlines()[0], f"{s}: unexpected header {head[:80]!r} ({ct})"
        rec(dest, url, lm)
    dest = RAW / "spf_medianLevel.xlsx"; lm, ct = curl(SPF, dest)
    assert dest.read_bytes()[:2] == b"PK" and "html" not in ct.lower(), f"SPF: not an xlsx ({ct})"
    rec(dest, SPF, lm, f"  content-type {ct}")
    (RAW / "uscrn2025").mkdir(parents=True, exist_ok=True); idx = RAW / "uscrn2025" / "index.html"; lm, _ = curl(USCRN, idx)
    rec(idx, USCRN, lm)
    names = sorted(set(re.findall(r'href="(CRND0103-2025-[^"]+\.txt)"', idx.read_text())))
    print(f"USCRN 2025 station files listed: {len(names)}", flush=True)
    for n in names:
        dest = RAW / "uscrn2025" / n; lm, _ = curl(USCRN + n, dest); rec(dest, USCRN + n, lm)
    (RAW / "kool").mkdir(parents=True, exist_ok=True)
    for n in ("data.mat", "subinfo.mat"):
        dest = RAW / "kool" / n; lm, _ = curl(KOOL + n, dest)
        assert dest.read_bytes()[:10] == b"MATLAB 5.0", f"{n}: not a MATLAB 5.0 MAT-file"
        rec(dest, KOOL + n, lm)
    MAN.parent.mkdir(exist_ok=True); MAN.write_text("\n".join(lines) + "\n"); print("manifest ->", MAN.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
