"""DR1 check DATA, the fetch step (Grid_Demand_Response/DECLARATION.md section 3, pushed at e67e8ee; binding, never edited here).

Fetches the first reachable public event-level demand-response record with times and prices, in the declared order:
  1. GB NESO's Demand Flexibility Service (DFS): the service-requirement, utilisation and utilisation-summary reports of every
     season on the NESO data portal (CKAN), with the CKAN package metadata of each dataset (the version record);
  2. a US ISO/RTO event history with prices (tried only if 1 is unreachable);
  3. any other system operator's event list with prices (tried only if 1 and 2 are unreachable).
The URLs are the dataset leads of docs/citations/dr1_f2_2026-09-29.md section 7 (the 2022/23 and 2023/24 file URLs are read from
the CKAN package metadata fetched here). Writes every raw file into Grid_Demand_Response/data/raw/, a JSON fetch log
(raw/FETCH_LOG.json: UTC time, URL, HTTP status, bytes, sha256 per file) and Grid_Demand_Response/data/MANIFEST.md.

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/data/fetch_dfs.py

Not deterministic (the current-season NESO files are updated daily); the sha256 in MANIFEST.md pins what was fetched, and
checks/dr_data.py refuses to compute if a raw file no longer matches it.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
CKAN = "https://api.neso.energy/api/3/action/package_show?id="

# (CKAN package id, season label, local prefix, {resource-name substring: local suffix})
PACKAGES = [
    ("demand-flexibility", "archive 2025/26 and current 2026/27 (package)", None, None),
    ("demand-flexibility-service", "2023/24", "s2324", {"Service Requirements": "sr", "Utilisation Report Summary": "sum",
                                                         "Utilisation Report": "util"}),
    ("demand-flexibility-service-live-events", "2022/23 live", "s2223L", {"Service Requirement": "sr",
                                                                          "Utilisation Report Summary": "sum",
                                                                          "Utilisation Report": "util"}),
    ("demand-flexibility-service-test-events", "2022/23 test", "s2223T", {"Service Requirement": "sr",
                                                                          "Utilisation Report Summary": "sum",
                                                                          "Utilisation Report": "util"}),
]
# the 'demand-flexibility' package: resource id -> local name (URLs as listed in the F2 dossier, section 7)
DF_RESOURCES = {
    "3635fd80-49d7-4d02-964d-cc8c08d50302": ("cur_sr.csv", "current (2026/27, from April 2026)"),
    "705e573c-ddac-4675-b410-82916b35c4fe": ("cur_sum.csv", "current (2026/27, from April 2026)"),
    "3ebf77d7-05df-466e-a023-dc45a90efeea": ("cur_util.csv", "current (2026/27, from April 2026)"),
    "f5605e2b-b677-424c-8df7-d0ce4ee03cef": ("a25_sr.csv", "archive 2025/26 (from November 2024)"),
    "25698259-0b66-42f0-ac59-ef0df5245812": ("a25_sum.csv", "archive 2025/26 (from November 2024)"),
    "cc36fff5-5f6f-4fde-8932-c935d982ecd8": ("a25_util.csv", "archive 2025/26 (from November 2024)"),
}


def get(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": "ashes_crr-dr1-fetch/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # noqa: BLE001 - any failure is 'not reached', logged
        print(f"  NOT REACHED {url}: {type(e).__name__}: {e}")
        return 0, b""


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    log = []

    def save(name, url, status, body, meta):
        sha = hashlib.sha256(body).hexdigest() if body else None
        if status == 200 and body:
            (RAW / name).write_bytes(body)
        log.append(dict(file=name, url=url, status=status, bytes=len(body), sha256=sha, fetched_utc=now(), **meta))
        print(f"  {status} {len(body):>9} {name} {url}")

    for pkg, season, prefix, want in PACKAGES:
        url = CKAN + pkg
        st, body = get(url)
        save(f"ckan_{pkg}.json", url, st, body, dict(season=season, kind="CKAN package metadata", version=None,
                                                             package_modified=(json.loads(body)["result"].get("metadata_modified")
                                                                               if st == 200 else None)))
        if st != 200:
            continue
        res = json.loads(body)["result"]
        for r in res["resources"]:
            sea = season
            if pkg == "demand-flexibility":
                name, sea = DF_RESOURCES.get(r["id"], (None, season))
            else:
                name = None
                # longest matching resource-name key first ('Utilisation Report Summary' before 'Utilisation Report')
                for key in sorted(want, key=len, reverse=True):
                    if key in r["name"]:
                        name = f"{prefix}_{want[key]}.csv"
                        break
            if name is None:
                continue
            st2, b2 = get(r["url"])
            save(name, r["url"], st2, b2, dict(season=sea, kind=r["name"], version=r.get("last_modified"),
                                               package_modified=res.get("metadata_modified"), resource_id=r["id"]))

    (RAW / "FETCH_LOG.json").write_text(json.dumps(log, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    ok = [e for e in log if e["status"] == 200]
    total = sum(e["bytes"] for e in ok)
    reached = any(e["status"] == 200 and e["file"].endswith(".csv") for e in log)
    print(f"  files fetched {len(ok)} of {len(log)}; raw bytes {total}")

    # ---------------------------------------------------------------------------------------- MANIFEST.md
    L = []
    L.append("# DR1 check DATA: manifest of the raw demand-response records")
    L.append("")
    L.append("Written by `Grid_Demand_Response/data/fetch_dfs.py` (declaration section 3, pushed at e67e8ee). Every raw file is in")
    L.append("`Grid_Demand_Response/data/raw/`; `checks/dr_data.py` verifies each sha256 below before it computes anything.")
    L.append("")
    L.append("**What was tried, in the declared order.**")
    L.append(f"1. GB NESO Demand Flexibility Service (NESO data portal, CKAN): **{'reached' if reached else 'NOT REACHED'}**; "
             "every season's service-requirement, utilisation and utilisation-summary reports fetched (the industry-notification "
             "files were not fetched: they carry no prices).")
    if reached:
        L.append("2. A US ISO/RTO event history (PJM, ERCOT; leads in `docs/citations/dr1_f2_2026-09-29.md` section 7): not tried, "
                 "because source 1 was reachable (declared order: the first reachable).")
        L.append("3. Any other operator: not tried, for the same reason.")
    L.append("")
    L.append("**Provenance.** Publisher: National Energy System Operator (NESO), GB. Portal: https://api.neso.energy (CKAN). "
             "Version = the CKAN resource `last_modified` time (and the package `metadata_modified` time) at download. The "
             "current-season files (`cur_*`) are updated as events happen: the copy here is the one fetched at the time shown. "
             "These records had never been opened in CRR work (they are not model carriers); the F2 dossier checked their "
             "reachability with one-byte range requests only.")
    L.append("")
    L.append(f"Download date: {log[0]['fetched_utc'][:10] if log else '-'} (UTC); total raw bytes {total} "
             f"({'above' if total > 5 * 10 ** 6 else 'not above'} 5 MB, so the raw files are "
             f"{'gitignored' if total > 5 * 10 ** 6 else 'kept in the repository'}).")
    L.append("")
    L.append("| file | season | NESO resource | version (last_modified) | fetched (UTC) | HTTP | bytes | sha256 | URL |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for e in log:
        L.append(f"| `{e['file']}` | {e['season']} | {e['kind']} | {e.get('version') or e.get('package_modified') or '-'} | "
                 f"{e['fetched_utc']} | {e['status']} | {e['bytes']} | `{e['sha256'] or '-'}` | {e['url']} |")
    L.append("")
    (HERE / "MANIFEST.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"  wrote {HERE / 'MANIFEST.md'}")
    return 0 if reached else 1


if __name__ == "__main__":
    sys.exit(main())
