"""DR1 check DATA (Grid_Demand_Response/DECLARATION.md section 3, pushed at e67e8ee; binding, never edited here): the
real-data application on public demand-response event records.

The declared calculation: a hypothetical AI training fleet of 100 MW (ASSUMED) running jobs of the H3 portfolio meets each
real event with its real window and price; ETM participates whenever the price covers R/H, OWN while slack lasts, TIER
within its tier, WALL when the price exceeds its wall-clock loss. Printed: events joined, curtailed MWh and revenue per arm;
revenue as a share of the fleet's compute cost over the same period (compute cost per MWh from the F5 dossier); the job delay
ETM accepts. Declared expectations: ETM joins every event; its revenue is below 1 % of the fleet's compute cost in an
ordinary season (G7); the commercial value, if any, lies in interconnection (G8), not in event payments.

The data: the first reachable of the declared sources, GB NESO's Demand Flexibility Service (every season on the NESO data
portal), fetched by Grid_Demand_Response/data/fetch_dfs.py and pinned by sha256 in Grid_Demand_Response/data/MANIFEST.md.
Arithmetic: Grid_Demand_Response/checks/drlib.py (exact rationals; its selftest is pinned in drlib_selftest.txt). An
application calculation on public data, not a test of a CRR hypothesis: no ledger row; a note, not evidence (R8). Every
verdict word below is computed from the numbers (R15).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_data.py > Grid_Demand_Response/checks/dr_data.txt
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "Grid_Demand_Response" / "data"
RAW = DATA / "raw"
CIT = REPO / "docs" / "citations"
ZERO, ONE = Fr(0), Fr(1)
TOL = Fr(1, 100)                         # G-NEG's declared 1 %
G7_BOUND = Fr(1, 100)                    # the declared expectation: revenue below 1 % of the fleet's compute cost

POST_FIRST_RUN_CHANGES: list[str] = []

# ============================================================================================ sourced inputs (verbatim quotes)
# (id, dossier, citation, verbatim quote (a substring of the dossier text), regex over the quote, group names)
SOURCES = [
    ("DFS-K", "dr1_f2", "NESO DFS Service Terms v4.0 (2026), Schedule 1",
     "Kie = 1.2 if RVie ≥120 Kie = 0.01*RVie if 50 ≤ RVie < 120",
     r"Kie = 0\.01\*RVie if (\d+) ≤ RVie < (\d+)", ("rv_lo", "rv_hi")),
    ("DFS-RV", "dr1_f2", "NESO DFS Service Terms v4.0 (2026), Schedule 1",
     "RVie = 100* (Vie / (Qie * 0.5))", r"\(Qie \* ([\d.]+)\)", ("sp_h",)),
    ("DFS-MAX", "dr1_f2", "NESO DFS Procurement Rules v5.0 (2026)",
     "“Maximum Submission Size” 100MW;", r"” (\d+)MW;", ("max_mw",)),
    ("DFS-BIDIR", "dr1_f2", "NESO DFS service web page (fetched 2026-09-29)",
     "On 9 April 2026, the service expanded further with the introduction of bi-directional flexibility",
     r"On (\d+) April (\d{4}), the service expanded further with the introduction of bi-directional", ("day", "year")),
    ("DFS-2223", "dr1_f2", "NESO (as ESO) DFS winter 2022/23 review (2023-08-30)",
     "For live events, the average price paid was £4,559/MWh.", r"was £([\d,]+)/MWh", ("live_avg",)),
    ("DFS-2425-SCEN", "dr1_f2", "NESO DFS winter 2024/25 report (2025-07-03)",
     "Average (based on mean accepted bid) £ 21,009 £ 7,558 Low (lowest accepted bid) £ 17,918 £3,142",
     r"Average \(based on mean accepted bid\) £ ([\d,]+) £ ([\d,]+) Low \(lowest accepted bid\) £ ([\d,]+) £([\d,]+)",
     ("avg_all", "avg_1h", "low_all", "low_1h")),
    ("DFS-2425-HIGH", "dr1_f2", "NESO DFS winter 2024/25 report (2025-07-03)",
     "High (based on Breakpoints) £ 33,560*", r"High \(based on Breakpoints\) £ ([\d,]+)\*", ("high_bp",)),
    ("AWS", "dr1_f5", "AWS EC2 price list JSON (publication 2026-09-25), p5.48xlarge, US East, Linux",
     "\"price\":\"55.0400000000\",\"Location\":\"US East (N. Virginia)\"", r"\"price\":\"([\d.]+)\"", ("node_h",)),
    ("CW", "dr1_f5", "CoreWeave pricing page (fetched 2026-09-29), HGX H100 (8 GPU)",
     "NVIDIA HGX H100 On-Demand Price: $49.24 / Hour Spot Price: $19.71 / Hour",
     r"On-Demand Price: \$([\d.]+) / Hour Spot Price: \$([\d.]+) / Hour", ("od_node_h", "spot_node_h")),
    ("LAMBDA-OD", "dr1_f5", "Lambda pricing page (fetched 2026-09-29), H100 SXM 8x instance",
     "NVIDIA H100 SXM 80 GB 208 1800 GiB 22 TiB SSD $3.99", r"SSD \$([\d.]+)$", ("gpu_h",)),
    ("LAMBDA-RES", "dr1_f5", "Lambda pricing page, H100 cluster reservation 2 weeks - 1 year",
     "NVIDIA H100 2 weeks – 1 year 256 $5.54", r"256 \$([\d.]+)$", ("gpu_h",)),
    ("RUNPOD", "dr1_f5", "RunPod pricing page (fetched 2026-09-29), H100 SXM pod",
     "H100 SXM 80 GB VRAM 125 GB RAM 20 vCPUs $ 3.49 /hr", r"\$ ([\d.]+) /hr", ("gpu_h",)),
    ("IDX-NEO", "dr1_f5", "Bandi & Su arXiv:2607.12156 v3, Table 1 (Silicon Data H100 neo-cloud index, 2026-04-18)",
     "H100 NEO SDH100RT 595 2024-09-01 2026-04-18 2.500", r"2026-04-18 ([\d.]+)$", ("gpu_h",)),
    ("IDX-HS", "dr1_f5", "Bandi & Su arXiv:2607.12156 v3, Table 1 (Silicon Data H100 hyperscaler index, 2026-04-18)",
     "H100 HS 595 2024-09-01 2026-04-18 7.430", r"2026-04-18 ([\d.]+)$", ("gpu_h",)),
    ("DGX", "dr1_f5", "NVIDIA DGX H100 datasheet",
     "GPU 8x NVIDIA H100 Tensor Core GPUs GPU memory 640GB total Performance 32 petaFLOPS FP8 NVIDIA® NVSwitch™ 4x System power usage ~10.2kW max",
     r"GPU (\d+)x NVIDIA H100.*~([\d.]+)kW max", ("gpus", "kw")),
    ("FLEX", "dr1_f1", "Colangelo et al. arXiv:2507.00909 v1 (flexibility tiers)",
     "(b) Flex 1: up to 10% performance (average throughput) reduction allowed over a 3-6 hour period; (c) Flex 2: up to 25% allowed; (d) Flex 3: up to 50% allowed.",
     r"Flex 1: up to (\d+)% .* over a (\d+)-(\d+) hour period; \(c\) Flex 2: up to (\d+)% allowed; \(d\) Flex 3: up to (\d+)% allowed",
     ("x1", "w_lo", "w_hi", "x2", "x3")),
    ("MS-5", "dr1_f4", "MegaScale (NSDI '24): optimised initialisation",
     "The initialization time is reduced to under 5 seconds on 2048 GPUs", r"under (\d+) seconds on 2048", ("s",)),
    ("MS-1047", "dr1_f4", "MegaScale (NSDI '24): default initialisation",
     "the initialization time for Megatron-LM on 2,048 NVIDIA Ampere GPUs is approximately 1047 second",
     r"approximately (\d+) second", ("s",)),
    ("KOK-U0", "dr1_f4", "Kokolis et al. arXiv:2410.21680 v2: restart overhead u0 on the RSC clusters",
     "wcp ≈5 mins, u0 ≈5 −20 mins", r"u0 ≈(\d+) −(\d+) mins", ("lo", "hi")),
]


def load_sources() -> tuple[dict, list]:
    texts = {k: (CIT / f"{k}_2026-09-29.md").read_text(encoding="utf-8") for k in {s[1] for s in SOURCES}}
    vals, rep = {}, []
    for sid, dos, cite, quote, rx, names in SOURCES:
        found = quote in texts[dos]
        m = re.search(rx, quote)
        ok = found and m is not None
        rep.append((sid, dos, cite, quote, found, m is not None))
        if ok:
            vals[sid] = {n: dl.q(m.group(i + 1).replace(",", "")) for i, n in enumerate(names)}
    return vals, rep


# ============================================================================================ assumed inputs and choices
FLEET_MW = dl.q(100)                     # ASSUMED (declaration section 3)
N_JOBS = 100                             # DECLARED (the H3 portfolio)
P_JOB = FLEET_MW / N_JOBS                # ASSUMED (H3: 1 MW per job)
W = dl.q(1000)                           # DECLARED (EPS2 T1 units)
R = dl.q("0.1")                          # ASSUMED (EPS2 T1; H3)
SLACK_STEP = dl.q(5)                     # ASSUMED (H3: slack 5 i h, i = 1..100)
FX = dl.q("1.35")                        # ASSUMED: USD per GBP (no dossier quotes an exchange rate)
FX_SENS = (dl.q("1.20"), dl.q("1.50"))   # ASSUMED sensitivity
PRIMARY_PRICE = "IDX-NEO"                # CHOICE: the compute cost per MWh from the H100 neo-cloud rental index
PRICE_DEFS = ("mean", "min", "max")      # CHOICE: per settlement period, the event price (primary 'mean')
TIER_WINDOWS_USED = ("w_lo", "w_hi")     # CHOICE: the two ends of the sourced 3-6 h period (as H2)
EPOCH = dt.date(2022, 1, 1)              # the timeline origin (hours of published local clock time)
SCARCITY = "W2022/23"                    # CHOICE: the season the F2 sources mark as the scarcity exception (DFS-2223)

SEASON_NAMES = {}


def season_of(d: dt.date) -> str:
    """CHOICE: winter November-March, summer April-October."""
    if d.month >= 11:
        return f"W{d.year}/{str(d.year + 1)[2:]}"
    if d.month <= 3:
        return f"W{d.year - 1}/{str(d.year)[2:]}"
    return f"S{d.year}"


# ============================================================================================ data: sha256 against the manifest
def manifest() -> dict:
    out = {}
    txt = (DATA / "MANIFEST.md").read_text(encoding="utf-8")
    for m in re.finditer(r"^\| `([^`]+)` \|.*\| `([0-9a-f]{64})` \|", txt, re.M):
        out[m.group(1)] = m.group(2)
    return out


def num(s) -> Fr | None:
    if s is None:
        return None
    s = s.strip().replace(",", "")
    if s == "":
        return None
    return dl.q(s)


def pdate(s: str) -> dt.date:
    s = s.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unparsed date {s!r}")


def hm(s: str) -> Fr:
    h, m = s.strip().split(":")[:2]
    return Fr(int(h)) + Fr(int(m), 60)


def rows(name: str) -> list[dict]:
    with open(RAW / name, encoding="utf-8-sig", newline="") as fh:
        return [{(k or "").strip(): v for k, v in r.items()} for r in csv.DictReader(fh)]


# the per-season files: (prefix, date column, from, to, type column or fixed type, required, procured, cost, event id, direction)
SUMS = [
    ("s2223T", "Date", "From", "To", "=Test", "DFS Required", "DFS Procured", "Bids Accepted Total Cost", None, None),
    ("s2223L", "Date", "From", "To", "=Live", "DFS Required", "DFS Procured", "Bids Accepted Total Cost", None, None),
    ("s2324", "Delivery Date", "From", "To", "Service Requirement Type", "DFS Required MW", "DFS Procured MW",
     "DFS Provider Bids Accepted Total Cost GBP", None, None),
    ("a25", "Delivery Date", "From", "To", "Service Requirement Type", "Service Requirement MW", "DFS Procured MW",
     "DFS Provider Bids Accepted Total Cost GBP", None, None),
    ("cur", "Delivery Date", "From_Local", "To_Local", "Service Requirement Type", "Service Requirement MW", "DFS Procured MW",
     "DFS Provider Bids Accepted Total Cost GBP", "Event ID", "Event Type"),
]
UTILS = {  # prefix: (date, from, type or fixed, volume, price, status, event id)
    "s2223T": ("Date", "From", "=Test", "DFS Volume", "Price", "Status", None),
    "s2223L": ("Date", "From", "=Live", "DFS Volume", "Price", "Status", None),
    "s2324": ("Delivery Date", "From", "Service Requirement Type", "DFS Volume MW", "Utilisation Price GBP per MWh", "Status", None),
    "a25": ("Delivery Date", "From", "Service Requirement Type", "DFS Volume MW", "Utilisation Price GBP per MWh", "Status", None),
    "cur": ("Delivery Date", "From_Local", "Service Requirement Type", "DFS Procured MW", "Utilisation Price GBP per MWh", "Status",
            "Event ID"),
}
SRS = {  # prefix: (date, from, type, GAP, event id) where the file carries a GAP column
    "s2324": ("Delivery Date", "From", "Service Requirement Type", "Guaranteed Acceptance Price GBP per MWh", None),
    "a25": ("Delivery Date", "From", "Service Requirement Type", "Guaranteed Acceptance Price GBP per MWh", None),
    "cur": ("Delivery Date", "From_Local", "Service Requirement Type", "Guaranteed Acceptance Price GBP per MWh", "Event ID"),
}


def col(r, spec):
    return spec[1:] if spec.startswith("=") else r[spec]


def load_sps(bidir: dt.date) -> tuple[list[dict], dict]:
    """Every published settlement period (SP) of every season as one record; returns (records, counts)."""
    stats = dict(rows=0, up=0, unpriced=0, util_match=0, util_nomatch=0, cost_ok=0, cost_n=0, cost_maxrel=ZERO)
    util = {}
    for pre, (dc, fc, tc, vc, pc, sc, ec) in UTILS.items():
        for r in rows(f"{pre}_util.csv"):
            if r[sc].strip() != "Accepted":
                continue
            key = (pre, r[ec].strip() if ec else None, pdate(r[dc]), r[fc].strip(), col(r, tc).strip())
            util.setdefault(key, []).append((num(r[pc]), num(r[vc])))
    gap = {}
    for pre, (dc, fc, tc, gc, ec) in SRS.items():
        for r in rows(f"{pre}_sr.csv"):
            key = (pre, r[ec].strip() if ec else None, pdate(r[dc]), r[fc].strip(), col(r, tc).strip())
            gap[key] = num(r[gc])
    out = []
    for pre, dc, fc, tc, ty, rq, pr, co, ec, dr in SUMS:
        for r in rows(f"{pre}_sum.csv"):
            stats["rows"] += 1
            d = pdate(r[dc])
            direction = r[dr].strip() if dr else "Downwards"
            if dr is None and d >= bidir:
                raise ValueError("a record without a direction field after bi-directional DFS began")
            t0, t1 = hm(r[fc]), hm(r[tc])
            if t1 <= t0:
                t1 += 24
            typ = col(r, ty).strip()
            eid = r[ec].strip() if ec else None
            rec = dict(pre=pre, eid=eid, date=d, season=season_of(d), frm=r[fc].strip(), to=r[tc].strip(), type=typ,
                       dir=direction, t=Fr((d - EPOCH).days * 24) + t0, h=t1 - t0, req=num(r[rq]), proc=num(r[pr]),
                       cost=num(r[co]), gap=gap.get((pre, eid, d, r[fc].strip(), typ)))
            if direction != "Downwards":
                stats["up"] += 1
                rec["priced"] = False
                out.append(rec)
                continue
            if not rec["proc"] or not rec["cost"] or rec["proc"] <= 0 or rec["cost"] <= 0:
                stats["unpriced"] += 1
                rec["priced"] = False
                out.append(rec)
                continue
            rec["priced"] = True
            rec["p_mean"] = rec["cost"] / (rec["proc"] * rec["h"])
            acc = util.get((pre, eid, d, r[fc].strip(), typ), [])
            acc = [(p, v) for p, v in acc if p is not None and v is not None and v > 0]
            if acc:
                stats["util_match"] += 1
                rec["p_min"] = min(p for p, v in acc)
                rec["p_max"] = max(p for p, v in acc)
                ucost = sum((p * v * rec["h"] for p, v in acc), ZERO)
                rel = abs(ucost - rec["cost"]) / max(abs(ucost), abs(rec["cost"]))
                stats["cost_n"] += 1
                stats["cost_ok"] += int(rel <= TOL)
                stats["cost_maxrel"] = max(stats["cost_maxrel"], rel)
            else:
                stats["util_nomatch"] += 1
                rec["p_min"] = rec["p_max"] = rec["p_mean"]       # CHOICE: fall back to the mean (counted)
            out.append(rec)
    return out, stats


def build_events(sps: list[dict], pdef: str) -> tuple[dict, dict]:
    """Per season: the offered events under the price definition pdef. At most one sale per SP (concurrent downward events on
    one SP: the better paid, CHOICE); contiguous priced SPs merge into one event (CHOICE)."""
    by_t = {}
    conc = 0
    for r in sps:
        if not r["priced"]:
            continue
        k = r["t"]
        if k in by_t:
            conc += 1
            if r[f"p_{pdef}"] > by_t[k][f"p_{pdef}"]:
                by_t[k] = r
        else:
            by_t[k] = r
    seasons = {}
    merged_ids = 0
    for k in sorted(by_t):
        r = by_t[k]
        evs = seasons.setdefault(r["season"], [])
        if evs and evs[-1]["t"] + evs[-1]["H"] == r["t"]:
            e = evs[-1]
            if r["eid"] is not None and e["sps"][-1]["eid"] is not None and r["eid"] != e["sps"][-1]["eid"]:
                merged_ids += 1
            e["sps"].append(r)
            e["H"] += r["h"]
        else:
            evs.append(dict(t=r["t"], H=r["h"], sps=[r], date=r["date"]))
    for evs in seasons.values():
        for e in evs:
            e["price"] = sum((s[f"p_{pdef}"] * s["h"] for s in e["sps"]), ZERO) / e["H"]
            e["types"] = "/".join(sorted({s["type"] for s in e["sps"]}))
            gaps = [s["gap"] for s in e["sps"] if s["gap"]]
            e["gap"] = max(gaps) if gaps else None
            e["req_min"] = min(s["req"] for s in e["sps"] if s["req"] is not None)
            e["proc_max"] = max(s["proc"] for s in e["sps"])
    return seasons, dict(concurrent=conc, merged_ids=merged_ids)


# ============================================================================================ the fleet on the real events
def compute_cost_mwh(vals: dict, key: str, fx: Fr) -> Fr:
    """GBP per MWh of compute: the 8-GPU node-hour price over the node's power (the DGX H100 maximum, ASSUMED to be what a rented
    8x H100 instance draws; PUE 1, ASSUMED), converted at fx USD per GBP."""
    gpus, kw = vals["DGX"]["gpus"], vals["DGX"]["kw"]
    if key in ("AWS",):
        node = vals[key]["node_h"]
    elif key == "CW-OD":
        node = vals["CW"]["od_node_h"]
    elif key == "CW-SPOT":
        node = vals["CW"]["spot_node_h"]
    else:
        node = vals[key]["gpu_h"] * gpus
    return node / (kw / 1000) / fx


PRICE_KEYS = ("IDX-NEO", "CW-SPOT", "RUNPOD", "LAMBDA-OD", "LAMBDA-RES", "CW-OD", "AWS", "IDX-HS")


def arms_for(vals: dict) -> list:
    fx_ = vals["FLEX"]
    tiers = []
    for xk in ("x1", "x2", "x3"):
        for wk in TIER_WINDOWS_USED:
            x = fx_[xk] / 100
            tiers.append(dl.tier(x, fx_[wk], name=f"TIER-{int(fx_[xk])}%/{dl.g(fx_[wk])}h"))
    return [dl.ETM, dl.OWN, dl.WALL] + tiers


def simulate(events: list, start: Fr, end: Fr, arm, jobs: list, C: Fr, gz: list | None = None) -> dict:
    """Each of the 100 slots (1 MW each) runs jobs of its slack back to back from `start`; at each real event the running job
    joins iff the payment covers the event's charge on the arm's valuation (pi e >= c, ties accept) and the arm's deadline
    still holds after it (drlib's arithmetic); a pause arm cannot join an event that starts before its previous event and
    overhead have ended. pi = price / C (value units per curtailed fleet-hour; one value unit = the compute cost of one
    MWh of the job's compute)."""
    ev_join = [0] * len(events)
    per_slot = []
    tot = dict(job_events=0, MWh=ZERO, revenue=ZERO, blocked=0, deadline_declined=0, price_declined=0, ties=0)
    for job in jobs:
        m = dl.Model(job, arm)
        t0, n, L, busy_until = start, 0, ZERO, None
        acc = 0
        done = []            # completed jobs: (start, n, L, wall delay)
        for i, e in enumerate(events):
            if e["t"] >= end:
                break
            while e["t"] >= t0 + m.completion(n, L):
                done.append((t0, n, L, m.dw(n, L)))
                t0 = t0 + m.completion(n, L)
                n, L, busy_until = 0, ZERO, None
            if busy_until is not None and e["t"] < busy_until:
                tot["blocked"] += 1
                continue
            he = m.heff(e["H"])
            eq = m.e1 * he
            c = m.charge(n + 1, L + he) - m.charge(n, L)
            pi = e["price"] / C
            if gz is not None and arm is dl.ETM:
                gz.append(dl.stake(job, dl.ETM, e["H"], n, L) - job.rate * job.overhead)
            if pi * eq < c:
                tot["price_declined"] += 1
                continue
            if pi * eq == c:
                tot["ties"] += 1
            if not m.met(n + 1, L + he):
                tot["deadline_declined"] += 1
                continue
            n, L = n + 1, L + he
            acc += 1
            ev_join[i] += 1
            tot["job_events"] += 1
            tot["MWh"] += eq * P_JOB
            tot["revenue"] += e["price"] * eq * P_JOB
            if m.arm.mech == "pause":
                busy_until = e["t"] + e["H"] + m.o
        cur = (t0, n, L, m.dw(n, L))
        per_slot.append(dict(job=job, accepted=acc, done=done, current=cur,
                             jobs_done=len(done), max_delay=max([x[3] for x in done] + [cur[3]])))
    tot["events_any"] = sum(int(x > 0) for x in ev_join)
    tot["events_all"] = sum(int(x == len(jobs)) for x in ev_join)
    tot["ev_join"] = ev_join
    tot["slots"] = per_slot
    tot["jobs_done"] = sum(s["jobs_done"] for s in per_slot)
    tot["done_delays"] = [x[3] for s in per_slot for x in s["done"]]
    tot["max_delay"] = max(s["max_delay"] for s in per_slot)
    tot["past_D"] = sum(int(x[3] > s["job"].slack) for s in per_slot for x in s["done"])
    return tot


def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def pct(x, d=4) -> str:
    return "-" if x is None else f"{float(x) * 100:.{d}f} %"


def relx(a: Fr, b: Fr) -> Fr:
    mx = max(abs(a), abs(b))
    return ZERO if mx == 0 else abs(a - b) / mx


def not_computable(reason: str) -> int:
    print(f"DATA not computable: {reason}")
    print()
    print(f"RESULT DATA: Q not computable; G-ZERO not computable ({reason}); G-NEG not computable ({reason})")
    return 0


def main() -> int:
    print("DR1 check DATA: the real-data application on public demand-response event records "
          f"(Grid_Demand_Response/DECLARATION.md section 3, declared at {dl.DECL_AT})")
    print("Declared expectations: ETM joins every event; its revenue is below 1 % of the fleet's compute cost in an ordinary season")
    print("(G7); the commercial value, if any, lies in interconnection (G8), not in event payments.")
    print("An application calculation on public data, not a test of a CRR hypothesis: no ledger row; a note, not evidence (R8).")
    print()

    # ------------------------------------------------------------------------------------------------ the data and the sources
    man = manifest()
    print("DATA (Grid_Demand_Response/data/MANIFEST.md; fetched by Grid_Demand_Response/data/fetch_dfs.py)")
    if not man:
        return not_computable("no manifest entries (no event dataset was reachable)")
    bad = []
    for name in sorted(man):
        p = RAW / name
        h = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        ok = h == man[name]
        bad += [] if ok else [name]
        print(f"  {name:52} sha256 matches the manifest: {dl.yn(ok)}")
    need = [f"{p[0]}_sum.csv" for p in SUMS] + [f"{p}_util.csv" for p in UTILS] + [f"{p}_sr.csv" for p in SRS]
    missing = [n for n in need if n not in man]
    if bad or missing:
        return not_computable(f"raw files differ from the manifest or are missing: {', '.join(bad + missing)}")
    print("  source: GB NESO Demand Flexibility Service, every season on the NESO data portal (the first reachable of the declared")
    print("  order; the US ISO/RTO and other sources were therefore not tried)")
    print()

    vals, rep = load_sources()
    print("INPUTS")
    print("  SOURCED (each quote checked verbatim against the dossier text at run time; the number parsed out of the quote):")
    for sid, dos, cite, quote, found, parsed in rep:
        v = vals.get(sid, {})
        print(f"    [{sid}] {dos}: {cite}; found verbatim: {dl.yn(found)}; parsed: {dl.yn(parsed)} -> "
              + ", ".join(f"{k} = {dl.g(x)}" for k, x in v.items()))
        print(f"      \"{quote}\"")
    missing_src = [s for s, _, _, _, fo, pa in rep if not (fo and pa)]
    if missing_src:
        return not_computable(f"sourced inputs not found verbatim: {', '.join(missing_src)}")
    print(f"  ASSUMED  fleet {dl.g(FLEET_MW)} MW (declaration section 3), {N_JOBS} jobs of {dl.g(P_JOB)} MW each (the H3 portfolio)")
    print(f"  DECLARED W = {dl.g(W)} compute-hours per job, value 1 per compute-hour at completion (EPS2 T1 units, as H3)")
    print(f"  ASSUMED  R = {dl.g(R)} h restart overhead per pause event (EPS2 T1; H3); S = 0, lost = 0 (H3); sensitivity with the F4 values")
    print(f"  ASSUMED  slack of job i = {dl.g(SLACK_STEP)} i h, i = 1..{N_JOBS} (the H3 portfolio); every job at full power when it runs")
    print(f"  ASSUMED  {dl.g(FX)} USD per GBP (no dossier quotes an exchange rate); sensitivity {', '.join(dl.g(x) for x in FX_SENS)}")
    print("  ASSUMED  a rented 8x H100 node draws the DGX H100 maximum [DGX] all the time it is rented; PUE 1 (no facility overhead)")
    print("  ASSUMED  one value unit = the compute cost of one MWh of the job's compute: a job is worth what its compute costs, so the")
    print("           payment in value units per curtailed fleet-hour is pi = price (GBP/MWh) / C (GBP per MWh of compute)")
    print("  ASSUMED  the fleet is a price-taker: its 100 MW is accepted at the event's price and does not move it (DFS is pay-as-bid;")
    print("           the SPs where 100 MW more than NESO procured would exceed the published requirement are counted below)")
    print("  ASSUMED  the fleet delivers exactly its accepted volume, RV = 100 %, so the performance factor K = 0.01 * RV = 1 [DFS-K]")
    print("           and the settlement is 0.5 * price * MW per half-hour [DFS-RV]; no penalty ever applies")
    print("  ASSUMED  power drawn while paused 0 (EPS2 T1); a throttle's power is linear in its throughput (drlib's default)")
    print()
    print("CHOICES")
    print("  C1 price of an SP (scored: 'mean') = NESO's accepted total cost / (procured MW x 0.5 h), the volume-weighted mean accepted")
    print("     bid; sensitivity 'min' / 'max' = the lowest / highest accepted utilisation price in the SP (utilisation report). An SP")
    print("     with no accepted bid (procured 0) carries no price and is not offered to the fleet (counted). An SP whose accepted")
    print("     bids are missing from the utilisation report takes the mean for 'min' and 'max' (counted).")
    print(f"  C2 direction: only demand turn-down (Downwards) SPs are offered (a training fleet at full power cannot turn up); SPs")
    print(f"     before {vals['DFS-BIDIR']['day']} April {vals['DFS-BIDIR']['year']} carry no direction field and are turn-down "
          "[DFS-BIDIR]; turn-up SPs are counted and excluded")
    print("  C3 an event = a maximal run of contiguous priced turn-down SPs (whatever their Event ID or Live/Test type); where two")
    print("     events cover one SP the fleet sells into the better paid one (one sale per SP); the event's price is its SPs' mean")
    print("     price (each SP 0.5 h); curtailment is all or nothing per event per job (DFS accepts a submission only in full)")
    print("  C4 seasons: winter November-March, summer April-October; the fleet's period in a season = 00:00 of its first event day")
    print("     to 24:00 of its last (shorter than the calendar season, which raises the revenue share); the fleet's compute cost")
    print("     over the period = 100 MW x period hours x C (rented compute is paid for while paused)")
    print(f"  C5 ordinary season = every season except {SCARCITY}, the season the F2 sources mark as the scarcity exception [DFS-2223]")
    print("  C6 each of the 100 slots runs its slack class's jobs back to back from the period start (the next job starts when the")
    print("     previous one completes on the wall clock); an event belongs to the job running at its start")
    print("  C7 decision rule (the declaration's section 3, one rule on drlib's arithmetic): at each event the running job joins iff")
    print("     the payment covers the event's charge on the arm's valuation (pi e >= c; ties accept, drlib's convention) and the")
    print("     arm's deadline still holds after the event. ETM: c = R (own clock), deadline W + n R <= D (own steps): 'whenever the")
    print("     price covers R/H'. OWN: c = R, deadline W + sum(H + R) <= D (wall): 'while slack lasts'. WALL: c = H + R (wall")
    print("     clock), same deadline: 'when the price exceeds its wall-clock loss'. TIER: throughput 1 - x for min(H, w) hours,")
    print("     c = 0, wall delay x min(H, w): 'within its tier'. Online: no arm knows the later events (a foresight reading by")
    print("     backward induction is printed as a cross-check). A pause arm cannot join an event that starts before its")
    print("     previous event and restart have ended (counted as blocked).")
    print("  C8 revenue per event = event price x curtailed MWh (pause: H x 1 MW per job; TIER: x min(H, w) x 1 MW)")
    print("  C9 compute cost C (scored) from the H100 neo-cloud index [IDX-NEO] (the lowest sourced price that is not spot; a lower C")
    print("     raises the revenue share and lowers ETM's entry price); every other sourced price in SENSITIVITY 1")
    print("  C10 Q holds iff ETM joins every offered event with all 100 jobs in every season AND ETM's revenue is below 1 % of the")
    print("     fleet's compute cost in every ordinary season (primary inputs); fails otherwise. G8 is not computable from event data")
    print("     (it is graded by the sweep, grade.py) and is not part of Q.")
    print()

    # ------------------------------------------------------------------------------------------------ the records
    bidir = dt.date(int(vals["DFS-BIDIR"]["year"]), 4, int(vals["DFS-BIDIR"]["day"]))
    sps, st = load_sps(bidir)
    print("THE RECORDS")
    print(f"  settlement-period rows (all summary files) {st['rows']}; turn-up excluded {st['up']}; turn-down with no accepted bid "
          f"(no price) {st['unpriced']}; priced turn-down {st['rows'] - st['up'] - st['unpriced']}")
    print(f"  priced SPs with accepted bids in the utilisation report {st['util_match']}; without (min/max fall back to the mean) "
          f"{st['util_nomatch']}; summary cost within 1 % of the utilisation report's accepted MW x price x 0.5 h in "
          f"{st['cost_ok']} of {st['cost_n']} (max relative difference {f(st['cost_maxrel'], 6)})")
    print("  per season (turn-down SPs):")
    seas_all = sorted({r["season"] for r in sps}, key=lambda s: (s[1:5], s[0] == "W"))
    for s in seas_all:
        rs = [r for r in sps if r["season"] == s]
        pr = [r for r in rs if r["priced"]]
        dn = [r for r in rs if r["dir"] == "Downwards"]
        over = sum(int(r["req"] is not None and r["proc"] + FLEET_MW > r["req"]) for r in pr)
        types = sorted({r["type"] for r in pr})
        print(f"    {s:9} dates {min(r['date'] for r in rs)}..{max(r['date'] for r in rs)}; turn-down SPs {len(dn)}, priced "
              f"{len(pr)} ({'/'.join(types)}); mean accepted price over priced SPs {f(sum((r['p_mean'] for r in pr), ZERO) / len(pr), 2) if pr else '-'} "
              f"GBP/MWh (min {f(min((r['p_min'] for r in pr), default=None), 2)}, max {f(max((r['p_max'] for r in pr), default=None), 2)}); "
              f"SPs where NESO's procured MW + 100 MW exceeds the requirement {over} of {len(pr)}")
    print()

    # ------------------------------------------------------------------------------------------------ the scored run
    arms = arms_for(vals)
    C = compute_cost_mwh(vals, PRIMARY_PRICE, FX)
    print(f"COMPUTE COST (scored): C = {vals['IDX-NEO']['gpu_h']} USD per GPU-hour x {vals['DGX']['gpus']} GPUs / {vals['DGX']['kw']} kW "
          f"/ {dl.g(FX)} USD per GBP = {f(C, 4)} GBP per MWh of compute (exact {C})")
    print(f"  ETM's entry price per event = C R / H: {f(C * R / dl.q('0.5'), 2)} GBP/MWh at H = 0.5 h, {f(C * R, 2)} at 1 h, "
          f"{f(C * R / 2, 2)} at 2 h, {f(C * R / 4, 2)} at 4 h; WALL's = C (1 + R/H): {f(C * (1 + R / dl.q('0.5')), 2)} at 0.5 h, "
          f"{f(C * (1 + R), 2)} at 1 h")
    print()

    jobs = [dl.Job(W, W + SLACK_STEP * i, R, name=f"J{i:03d}") for i in range(1, N_JOBS + 1)]

    def run_all(pdef: str, Cx: Fr, jobs_x: list, arms_x: list, gz: list | None = None, drop_events: bool = False) -> dict:
        evs, info = build_events(sps, pdef)
        out = {}
        for s in seas_all:
            if s not in evs:
                continue
            e = evs[s]
            start = Fr((e[0]["date"] - EPOCH).days * 24)
            end = Fr((e[-1]["date"] - EPOCH).days * 24 + 24)
            use = [] if drop_events else e
            out[s] = dict(events=e, start=start, end=end, hours=end - start,
                          arms={a.name: simulate(use, start, end, a, jobs_x, Cx, gz) for a in arms_x})
        return dict(seasons=out, info=info)

    gz_list: list = []
    main_run = run_all("mean", C, jobs, arms, gz_list)
    seasons = main_run["seasons"]
    print(f"EVENTS (scored price 'mean'): concurrent turn-down events on one SP {main_run['info']['concurrent']} (the better paid "
          f"kept); merges across Event IDs {main_run['info']['merged_ids']}")
    print()

    # per-event table
    print("PER-EVENT TABLE (scored run). Per event: start (published local time), H (h), SPs, type, price = mean accepted (GBP/MWh),")
    print("min / max accepted, GAP (tests, where published), NESO's requirement (min over SPs) and procured (max) MW, ETM's entry")
    print("price C R/H, and per arm the jobs (of 100) that joined")
    anames = [a.name for a in arms]
    for s, S in seasons.items():
        print(f"  season {s}: {len(S['events'])} events; period {f(S['hours'] / 24, 0)} days")
        print(f"    {'#':>4} {'date':10} {'from':5} {'H':>4} {'SPs':>3} {'type':9} {'price':>9} {'min':>8} {'max':>8} {'GAP':>6} "
              f"{'req':>6} {'proc':>7} {'ETM entry':>9} " + " ".join(f"{a[:13]:>13}" for a in anames))
        for i, e in enumerate(S["events"]):
            mn = min(sp["p_min"] for sp in e["sps"])
            mx = max(sp["p_max"] for sp in e["sps"])
            print(f"    {i + 1:>4} {str(e['date']):10} {e['sps'][0]['frm']:5} {dl.g(e['H']):>4} {len(e['sps']):>3} {e['types']:9} "
                  f"{f(e['price'], 2):>9} {f(mn, 2):>8} {f(mx, 2):>8} {f(e['gap'], 0) if e['gap'] else '-':>6} "
                  f"{f(e['req_min'], 1):>6} {f(e['proc_max'], 1):>7} {f(C * R / e['H'], 2):>9} "
                  + " ".join(f"{S['arms'][a]['ev_join'][i]:>13}" for a in anames))
    print()

    # per-season, per-arm table
    print("PER-SEASON, PER-ARM TABLE (scored run): events joined by at least one job / by all 100 jobs, job-events joined, declined")
    print("on price / on deadline, blocked, curtailed MWh, revenue (GBP), the fleet's compute cost over the period (GBP), revenue as")
    print("a share of it, revenue per MW of fleet")
    shares = {}
    for s, S in seasons.items():
        cost = FLEET_MW * S["hours"] * C
        K = len(S["events"])
        print(f"  season {s}: {K} events; period {f(S['hours'], 0)} h; compute cost {f(cost, 0)} GBP")
        for a in anames:
            t = S["arms"][a]
            sh = t["revenue"] / cost
            shares[(s, a)] = sh
            print(f"    {a:14} joined {t['events_any']:>4} / {t['events_all']:>4} of {K:>4}; job-events {t['job_events']:>6}; declined price "
                  f"{t['price_declined']:>6}, deadline {t['deadline_declined']:>5}; blocked {t['blocked']:>3}; ties {t['ties']}; "
                  f"MWh {f(t['MWh'], 1):>10}; revenue {f(t['revenue'], 2):>12}; share {pct(sh, 5):>12}; per MW {f(t['revenue'] / FLEET_MW, 2):>10}")
    print()

    # ETM's delay
    print("THE JOB DELAY ETM ACCEPTS (scored run): per job, the wall-clock delay L + n R beyond W (the stop-the-clock extension")
    print("covers the curtailed hours L; the overhead n R uses the own-step deadline); over completed jobs and the job running at the")
    print("period end")
    for s, S in seasons.items():
        t = S["arms"]["ETM"]
        dd = t["done_delays"]
        print(f"  {s:9} jobs completed {t['jobs_done']:>4}; delay mean over completed {f(sum(dd, ZERO) / len(dd), 3) if dd else '-'} h, "
              f"max over all jobs {f(t['max_delay'], 3)} h ({pct(t['max_delay'] / W, 3)} of W); completed jobs past their original "
              f"wall-clock D {t['past_D']} of {len(dd)}")
    print()

    # per-slot table
    print("PER-SLOT TABLE (scored run): per job slot (slack of each of its jobs), per season, the job-events joined by ETM / OWN / WALL /")
    print("TIER (tiers in declared order) and ETM's max delay (h)")
    for s, S in seasons.items():
        print(f"  season {s}:")
        for j in range(N_JOBS):
            parts = [str(S["arms"][a]["slots"][j]["accepted"]) for a in anames]
            print(f"    {jobs[j].name} slack {dl.g(jobs[j].slack):>4}: " + " / ".join(parts)
                  + f"; ETM max delay {f(S['arms']['ETM']['slots'][j]['max_delay'], 2)}")
    print()

    # ------------------------------------------------------------------------------------------------ Q
    ordinary = [s for s in seasons if s != SCARCITY]
    etm_all = {s: seasons[s]["arms"]["ETM"]["events_all"] == len(seasons[s]["events"]) for s in seasons}
    g7 = {s: shares[(s, "ETM")] < G7_BOUND for s in ordinary}
    qa = all(etm_all.values())
    qb = all(g7.values()) and len(ordinary) > 0
    q_word = "holds" if (qa and qb) else "fails"
    print("Q (scored, primary inputs):")
    for s in seasons:
        print(f"  {s:9} ETM joined with all 100 jobs {seasons[s]['arms']['ETM']['events_all']} of {len(seasons[s]['events'])} events "
              f"-> every event: {dl.yn(etm_all[s])}; ETM revenue share {pct(shares[(s, 'ETM')], 5)} -> below 1 %: "
              f"{dl.yn(shares[(s, 'ETM')] < G7_BOUND)}{'' if s in ordinary else ' (scarcity season, not scored for G7)'}")
    print(f"  part (a) ETM joins every event: {dl.yn(qa)} ({sum(int(v) for v in etm_all.values())} of {len(etm_all)} seasons); part (b) "
          f"below 1 % in every ordinary season: {dl.yn(qb)} ({sum(int(v) for v in g7.values())} of {len(g7)}) -> Q {q_word}")
    tot_ev = sum(len(seasons[s]["events"]) for s in seasons)
    tot_all = sum(seasons[s]["arms"]["ETM"]["events_all"] for s in seasons)
    print(f"  over all seasons ETM joined {tot_all} of {tot_ev} events with all 100 jobs")
    sc = vals["DFS-2425-SCEN"]
    if "W2024/25" in seasons:
        rev_mw = seasons["W2024/25"]["arms"]["ETM"]["revenue"] / FLEET_MW
        print(f"  context (not scored): ETM's W2024/25 revenue per MW {f(rev_mw, 2)} GBP against NESO's own 1-MW scenarios for that "
              f"winter, {dl.g(sc['low_1h'])} to {dl.g(vals['DFS-2425-HIGH']['high_bp'])} GBP [DFS-2425-SCEN, DFS-2425-HIGH]")
    print("  G8 (interconnection value) is not computable from event records: not part of Q")
    print()

    # ------------------------------------------------------------------------------------------------ foresight cross-check
    print("CROSS-CHECK (not scored): the first job of slots J001, J020, J100 in each season, decided by exact backward induction")
    print("(drlib.solve, the season's real events and prices known in advance, ties accept) against the online rule; per arm the")
    print("events joined and the revenue (GBP), and whether the two agree event by event")
    xc_n = xc_agree = 0
    for s, S in seasons.items():
        for idx in (0, 19, 99):
            job = jobs[idx]
            for arm in (dl.ETM, dl.OWN, dl.WALL):
                m = dl.Model(job, arm)
                horizon = S["start"] + W + sum((e["H"] for e in S["events"]), ZERO) + len(S["events"]) * R
                ev = [e for e in S["events"] if S["start"] <= e["t"] < min(horizon, S["end"])]
                offs = dl.schedule([e["t"] - S["start"] for e in ev], [e["H"] for e in ev])
                prices = [e["price"] / C for e in ev]
                try:
                    pl = dl.play(job, arm, offs, prices)
                except ValueError as exc:
                    print(f"  {s} {job.name} {arm.name}: not computable ({exc})")
                    continue
                rev_bi = sum((ev[k]["price"] * m.e1 * m.heff(ev[k]["H"]) * P_JOB for k in pl["accepted"]), ZERO)
                # the online rule for the same first job
                on = simulate(ev, S["start"], S["end"], arm, [job], C)
                first_done = on["slots"][0]["done"]
                if first_done:
                    n_on = first_done[0][1]
                else:
                    n_on = on["slots"][0]["current"][1]
                on_idx = [k for k in range(len(ev)) if on["ev_join"][k]][:n_on]
                agree = list(pl["accepted"]) == on_idx
                rev_on = sum((ev[k]["price"] * m.e1 * m.heff(ev[k]["H"]) * P_JOB for k in on_idx), ZERO)
                xc_n += 1
                xc_agree += int(agree)
                print(f"  {s:9} {job.name} {arm.name:4}: offers {len(ev):>4}; backward induction joins {pl['events']:>4}, revenue "
                      f"{f(rev_bi, 2):>11}; online rule joins {n_on:>4}, revenue {f(rev_on, 2):>11}; same events: {dl.yn(agree)}")
    print(f"  the online rule and backward induction choose the same events in {xc_agree} of {xc_n} (season, job, arm) cells")
    print()

    # ------------------------------------------------------------------------------------------------ sensitivities
    print("SENSITIVITY 1 (not scored): the compute cost C from every sourced price and USD/GBP in {1.20, 1.35, 1.50} (ASSUMED); per")
    print("season ETM's events joined with all 100 jobs and ETM's revenue share")
    etm_only = [dl.ETM]
    worst = {}
    for key in PRICE_KEYS:
        for fx in sorted({FX, *FX_SENS}):
            Cx = compute_cost_mwh(vals, key, fx)
            run = run_all("mean", Cx, jobs, etm_only)["seasons"]
            parts = []
            for s, S in run.items():
                cost = FLEET_MW * S["hours"] * Cx
                sh = S["arms"]["ETM"]["revenue"] / cost
                if s != SCARCITY:
                    worst[s] = max(worst.get(s, ZERO), sh)
                parts.append(f"{s} {S['arms']['ETM']['events_all']}/{len(S['events'])} {pct(sh, 4)}")
            print(f"  {key:10} fx {dl.g(fx):4} C {f(Cx, 1):>9} GBP/MWh: " + "; ".join(parts))
    print("  largest ETM share over these cells per ordinary season: "
          + "; ".join(f"{s} {pct(v, 4)} (below 1 %: {dl.yn(v < G7_BOUND)})" for s, v in worst.items()))
    print()

    print("SENSITIVITY 2 (not scored): the SP price read as the lowest or the highest accepted bid (C1); per season and arm the events")
    print("joined with all 100 jobs, revenue (GBP) and share")
    for pdef in ("min", "max"):
        run = run_all(pdef, C, jobs, arms)["seasons"]
        print(f"  price '{pdef}':")
        for s, S in run.items():
            cost = FLEET_MW * S["hours"] * C
            print(f"    {s:9} " + "; ".join(f"{a} {S['arms'][a]['events_all']}/{len(S['events'])} {f(S['arms'][a]['revenue'], 0)} "
                                             f"{pct(S['arms'][a]['revenue'] / cost, 4)}" for a in ("ETM", "OWN", "WALL")))
    print()

    print("SENSITIVITY 3 (not scored): the restart overhead R from the F4 dossier (MegaScale 5 s and 1047 s; Kokolis u0 5 and 20 min)")
    print("against the ASSUMED 0.1 h; per season ETM's events joined with all 100 jobs and its revenue share")
    r_sens = [("MS-5", vals["MS-5"]["s"] / 3600), ("KOK-U0 lo", vals["KOK-U0"]["lo"] / 60), ("R 0.1 (ASSUMED)", R),
              ("KOK-U0 hi", vals["KOK-U0"]["hi"] / 60), ("MS-1047", vals["MS-1047"]["s"] / 3600)]
    for lab, Rx in r_sens:
        jobs_r = [dl.Job(W, W + SLACK_STEP * i, Rx, name=f"J{i:03d}") for i in range(1, N_JOBS + 1)]
        run = run_all("mean", C, jobs_r, etm_only)["seasons"]
        parts = []
        for s, S in run.items():
            cost = FLEET_MW * S["hours"] * C
            parts.append(f"{s} {S['arms']['ETM']['events_all']}/{len(S['events'])} {pct(S['arms']['ETM']['revenue'] / cost, 4)}")
        print(f"  {lab:16} R = {f(Rx, 5)} h: " + "; ".join(parts))
    print()

    # ------------------------------------------------------------------------------------------------ the gate
    gz_max = max((abs(x) for x in gz_list), default=None)
    gz_nonzero = sum(int(x != 0) for x in gz_list)
    gz = gz_max is not None and gz_max == 0
    neg = run_all("mean", C, jobs, [dl.ETM, dl.WALL], drop_events=True)["seasons"]
    ahead, n_cmp, maxrel = 0, 0, ZERO
    for s, S in neg.items():
        e_, w_ = S["arms"]["ETM"], S["arms"]["WALL"]
        pairs = [(e_["MWh"], w_["MWh"]), (e_["revenue"], w_["revenue"]), (Fr(e_["jobs_done"]), Fr(w_["jobs_done"])),
                 (Fr(e_["events_any"]), Fr(w_["events_any"]))]
        for a_, b_ in pairs:
            n_cmp += 1
            maxrel = max(maxrel, relx(a_, b_))
            ahead += int(a_ > b_ and relx(a_, b_) > TOL)
        for se, sw in zip(e_["slots"], w_["slots"]):
            n_cmp += 2
            ce, cw = se["current"][0] + se["job"].W + se["current"][3], sw["current"][0] + sw["job"].W + sw["current"][3]
            maxrel = max(maxrel, relx(ce, cw), relx(Fr(se["jobs_done"]), Fr(sw["jobs_done"])))
            ahead += int(ce < cw and relx(ce, cw) > TOL) + int(se["jobs_done"] > sw["jobs_done"] and
                                                               relx(Fr(se["jobs_done"]), Fr(sw["jobs_done"])) > TOL)
    gn = ahead == 0
    print("GATE")
    print(f"  G-ZERO: ETM's stake beyond R (drlib.stake - R) at every ETM decision of the scored run, {len(gz_list)} (job, event) "
          f"states in {len(seasons)} seasons: max |stake - R| = {f(gz_max, 6)} (exact {gz_max}); non-zero in {gz_nonzero} -> "
          f"{'holds' if gz else 'FAILS'}")
    print(f"  G-NEG: no events offered, every season: ETM ahead of WALL by more than 1 % on {ahead} of {n_cmp} outcome comparisons "
          f"(per season: curtailed MWh, revenue, jobs completed, events joined; per slot: completion hour of the running job, "
          f"jobs completed); max relative difference {f(maxrel, 6)} -> {'holds' if gn else 'FAILS'}")
    print()
    print("POST-FIRST-RUN CHANGES: " + ("none" if not POST_FIRST_RUN_CHANGES else "; ".join(POST_FIRST_RUN_CHANGES)))
    print()
    print(f"RESULT DATA: Q {q_word}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - R| = {f(gz_max, 6)} over {len(gz_list)} "
          f"(job, event) states); G-NEG {'holds' if gn else 'FAILS'} (no events: ETM ahead of WALL by > 1 % on {ahead} of {n_cmp} "
          f"outcome comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
