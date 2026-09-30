"""DR1 check H6: response time. A lossless pause must save before the power drops; demand-response products need response
within T.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 2, row H6:
  check:      response time: a lossless pause must save before the power drops; demand-response products need response
              within T
  Q:          where the save time S exceeds T, ETM cannot meet the product without losing work; the feasible product set is
              printed
  forecast:   Q holds
This check also prints the gate's G-ZERO and G-NEG (G-POS belongs to H1).

The arithmetic is the shared library Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; its selftest
reproduces EPS2 T1 line for line). Every verdict word printed here is computed from the numbers (R15). Every input number
is either sourced (a verbatim quote from docs/citations/dr1_f2/f3/f4_2026-09-29.md, checked against the dossier text at run
time, the number parsed out of the quote by a regular expression) or printed as ASSUMED; every modelling choice is printed
as CHOICE. The response times T come from the F2 and F3 dossiers, the save and restart times and the checkpoint interval
from F4 (the same quotes as H4); F4's pre-emption notices and power-control latencies are printed as context, not scored.
Rung R4 at most (synthetic model); a note, not evidence (R8). Deterministic, stdlib only (via drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h6.py > Grid_Demand_Response/checks/dr_h6.txt
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as d  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CIT = REPO / "docs" / "citations"
F2, F3, F4 = "dr1_f2_2026-09-29.md", "dr1_f3_2026-09-29.md", "dr1_f4_2026-09-29.md"
TEXT = {f: (CIT / f).read_text(encoding="utf-8") for f in (F2, F3, F4)}
ZERO, ONE = Fr(0), Fr(1)
SEC, MIN = Fr(1, 3600), Fr(1, 60)          # hours per second, per minute
WORDS = {"ten": 10, "two": 2, "twenty four": 24, "hourly": 1}

# ------------------------------------------------------------------------------------------------ sourced inputs (quotes)
# Each source: id, dossier file, short citation, verbatim quote (a substring of the dossier), regex, and the named values it
# yields: (value id, role, group index, unit in hours, CHOICE note). Roles: 'T' a scored product's response time; 'Tdfs' the
# DFS lead-time bound (not scored: no minimum notice); 'Tx' a context notice (F4, not a demand-response product; not scored);
# 'Tthr' a throttle's control latency (context); 'Hz' the grid frequency for converting cycles; 'S' save; 'R' restart;
# 'I' the periodic checkpoint interval (the lossy route); 'Ichk' a consistency number (lost work = I/2); 'unused'.
# unit 'cyc' means cycles of the grid frequency (converted with the 'Hz' value); unit 'hhmm' means a clock-time difference.
SOURCES = [
    # ---------------- F2: demand-response products (response times)
    dict(id="ERS-10", f=F2, src="ERCOT Nodal Protocols Section 3 (2026-08-01), ERS",
         quote="An ERS Resource participating in ERS-10 must be capable of meeting its event performance obligations relevant to its assigned performance evaluation methodology within ten minutes of an ERCOT Dispatch Instruction to its QSE",
         rx=r"within (ten) minutes of an ERCOT Dispatch Instruction",
         vals=[("T-ERS10", "T", 1, MIN, "ERCOT ERS-10: performance obligations met within ten minutes of the dispatch instruction")]),
    dict(id="ERS-30", f=F2, src="ERCOT Nodal Protocols Section 3 (2026-08-01), ERS",
         quote="An ERS Resource participating in ERS-30 must be capable of meeting its event performance obligations relevant to its assigned performance evaluation methodology within 30 minutes of an ERCOT Dispatch Instruction to its QSE",
         rx=r"within (\d+) minutes of an ERCOT Dispatch Instruction",
         vals=[("T-ERS30", "T", 1, MIN, "ERCOT ERS-30: performance obligations met within 30 minutes of the dispatch instruction")]),
    dict(id="FFR-auto", f=F2, src="ERCOT Nodal Protocols Section 2 (definitions), Fast Frequency Response",
         quote="The automatic self-deployment and provision by a Resource of their obligated response within 15 cycles after frequency meets or drops below a preset threshold",
         rx=r"within (\d+) cycles after frequency",
         vals=[("T-FFR15cyc", "T", 1, "cyc", "ERCOT FFR, automatic mode: 15 cycles of the grid frequency after the trigger (converted at the "
                "sourced 60 Hz; the ten-minute XML mode of the same definition is not in the task's number list and is not used)")]),
    dict(id="PJM-LM", f=F2, src="PJM Manual 18 Rev. 63, Load Management lead times",
         quote="Load management is required to fully respond within 30 minutes of notification unless an exception request for 60 or 120 minutes notification time is approved by PJM.",
         rx=r"within (\d+) minutes of notification unless an exception request for (\d+) or (\d+) minutes",
         vals=[("T-PJM30", "T", 1, MIN, "PJM Load Management, default: full response within 30 minutes of notification"),
               ("T-PJM60", "T", 2, MIN, "PJM Load Management, by approved exception: 60 minutes"),
               ("T-PJM120", "T", 3, MIN, "PJM Load Management, by approved exception: 120 minutes")]),
    dict(id="PJM-2026-09-17", f=F2, src="PJM Estimated DR Activity, September 17, 2026 (a realised event)",
         quote="14:00 14:30 22:00 Pre-Emergency Quick_30",
         rx=r"^(\d+):(\d+) (\d+):(\d+) ",
         vals=[("T-PJMreal", "T", (1, 2, 3, 4), "hhmm", "the realised lead of the 17 Sep 2026 Quick_30 event: deploy time minus "
                "notification time (computed from the two clock times)")]),
    dict(id="CAISO-RDRR", f=F2, src="CAISO RDRR overview (2014-05-08)",
         quote="reaching full curtailment within 40 minutes",
         rx=r"within (\d+) minutes",
         vals=[("T-RDRR40", "T", 1, MIN, "CAISO RDRR: full curtailment within 40 minutes")]),
    dict(id="DFS-lead", f=F2, src="NESO DFS Participation Guidance v18",
         quote="the service can be procured at any time in a day, up to a maximum of twenty four hours ahead of the start of any Service Requirement window.",
         rx=r"up to a maximum of (twenty four) hours ahead",
         vals=[("T-DFSmax", "Tdfs", 1, ONE, "DFS: a MAXIMUM lead of 24 h; the rules state no minimum notice (dossier F2), so DFS has no "
                "stated T: printed, not scored")]),
    # ---------------- F3: grid-reliability products (response times)
    dict(id="RRS-FFR", f=F3, src="ERCOT Ancillary Services Study, Sept 2024",
         quote="RRS-FFR is (full) response when frequency is below 59.85 Hz within 250 ms",
         rx=r"within (\d+) ms",
         vals=[("T-RRSFFR", "T", 1, SEC / 1000, "ERCOT RRS-FFR: full response within 250 ms of the frequency trigger")]),
    dict(id="ECRS", f=F3, src="ERCOT Ancillary Services Study, Sept 2024",
         quote="ECRS is capacity that can respond in 10 minutes",
         rx=r"respond in (\d+) minutes",
         vals=[("T-ECRS", "T", 1, MIN, "ERCOT ECRS: response in 10 minutes")]),
    dict(id="NSPIN", f=F3, src="ERCOT Ancillary Services Study, Sept 2024",
         quote="Reducing consumption based on an ERCOT Extensible Markup Language (XML) instruction within 30 minutes; and ii. Maintaining that deployment until recalled.",
         rx=r"instruction within (\d+) minutes;",
         vals=[("T-NSPIN", "T", 1, MIN, "ERCOT Non-Spin, non-controllable Load Resources: reduce within 30 minutes of the XML instruction")]),
    dict(id="REG", f=F3, src="ERCOT Ancillary Services Study, Sept 2024",
         quote="Regulation Service is capacity that can be deployed by ERCOT systems every 4 seconds to balance supply with demand in between the 5-min Security-Constrained Economic Dispatch (SCED) intervals and maintain frequency close to 60 Hz.",
         rx=r"every (\d+) seconds .* close to (\d+) Hz",
         vals=[("T-REG4s", "T", 1, SEC, "ERCOT Regulation: the 4-second deployment cadence read as the response time (a resource "
                "following Regulation must respond within one cadence)"),
               ("Hz-60", "Hz", 2, ONE, "the nominal frequency of the ERCOT grid, used to convert FFR's 15 cycles to seconds")]),
    dict(id="ERS-ramps", f=F3, src="ERCOT Overview of Demand Response, April 2023",
         quote="Four ERS service types: • Non-Weather Sensitive in 10 and 30 minute ramps",
         rx=r"in (\d+) and (\d+) minute ramps",
         vals=[("C-ERS10", "corr", 1, MIN, "corroborates ERS-10 (F2); not a separate product"),
               ("C-ERS30", "corr", 2, MIN, "corroborates ERS-30 (F2); not a separate product")]),
    dict(id="SB6", f=F3, src="Texas SB 6 (enrolled)",
         quote="ensure that the independent organization provides at least a 24-hour notice to large load customers",
         rx=r"at least a (\d+)-hour notice",
         vals=[("T-SB6", "T", 1, ONE, "Texas SB 6 large-load demand reduction: a notice of AT LEAST 24 h, read as T = 24 h (a lower "
                "bound: a save that fits 24 h fits the actual notice)")]),
    # ---------------- F4: save, restart, checkpoint interval (the same quotes as H4)
    dict(id="KOK-u0", f=F4, src="Kokolis et al., arXiv:2410.21680 v2 (HPCA 2025)",
         quote="For the RSC clusters, rf ≈5 × 10−3 failures per GPU node-day of runtime, wcp ≈5 mins, u0 ≈5 −20 mins, and (Nnodesrf)−1 ≳0.1 day.",
         rx=r"wcp ≈(\d+) mins, u0 ≈(\d+) −(\d+) mins",
         vals=[("S-KOK-wcp", "S", 1, MIN, "the paper's checkpoint write estimate for the RSC clusters, read as the save"),
               ("R-KOK-u0lo", "R", 2, MIN, "the low end of the paper's restart-overhead range u0"),
               ("R-KOK-u0hi", "R", 3, MIN, "the high end of the paper's restart-overhead range u0")]),
    dict(id="KOK-lost", f=F4, src="Kokolis et al., arXiv:2410.21680 v2 (HPCA 2025)",
         quote="we assume that all jobs checkpoint hourly (we find this is a typical checkpoint interval for larger jobs on the RSC clusters), giving an average of half an hour of lost work.",
         rx=r"checkpoint (hourly) .* an average of (half) an hour of lost work",
         vals=[("I-KOK-hourly", "I", 1, ONE, "'checkpoint hourly' read as a periodic checkpoint interval of 1 h (the lossy route)"),
               ("L-KOK-half", "Ichk", 2, None, "'half an hour' of lost work: checks drlib.lossy's expected loss I/2 at I = 1 h")]),
    dict(id="BC-405B", f=F4, src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25), Table 8",
         quote="Text Transformer 405B Megatron-LM 8960 TP=8, DP=70, PP=16 0.59 51.06 129.49",
         rx=r"PP=16 ([\d.]+) ([\d.]+) ([\d.]+)$",
         vals=[("S-BC405-block", "S", 1, SEC, "TBlock read as the save before the power drops (the hosts stay powered to persist)"),
               ("S-BC405-save", "S", 2, SEC, "TSave read as the end-to-end persistent save before the power drops"),
               ("U-BC405-load", "unused", 3, SEC, "TLoad: a restart component; H6 uses the Kokolis restart range")]),
    dict(id="BC-7B", f=F4, src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25), Table 8",
         quote="Vision Transformer 7B FSDP 1488 ZeRO-2 0.34 20.13 265.73",
         rx=r"ZeRO-2 ([\d.]+) ([\d.]+) ([\d.]+)$",
         vals=[("S-BC7-block", "S", 1, SEC, "TBlock read as the save before the power drops (the hosts stay powered to persist)"),
               ("S-BC7-save", "S", 2, SEC, "TSave read as the end-to-end persistent save before the power drops"),
               ("U-BC7-load", "unused", 3, SEC, "TLoad: a restart component; H6 uses the Kokolis restart range")]),
    dict(id="BC-175B", f=F4, src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25)",
         quote="the average end-to-end time required to save checkpoints of a GPT 175B model, trained on 4096 GPUs, to HDFS can be 200 seconds.",
         rx=r"can be (\d+) seconds",
         vals=[("S-BC175-save", "S", 1, SEC, "an end-to-end save before optimisation, read as the save before the power drops")]),
    dict(id="GEM-remote", f=F4, src="GEMINI, SOSP '23",
         quote="it takes 42 minutes to checkpoint the model states of MT-NLG [68] to the remote persistent storage when the bandwidth is 20Gbps.",
         rx=r"it takes (\d+) minutes to checkpoint",
         vals=[("S-GEM-remote", "S", 1, MIN, "a full save to remote storage at 20 Gbps, read as the save before the power drops")]),
    dict(id="PT-dcp", f=F4, src="PyTorch blog (2024-06-12)",
         quote="Example: 7B model ‘down time’ for a checkpoint goes from an average of 148.8 seconds to 6.3 seconds, or 23.62x faster.",
         rx=r"average of ([\d.]+) seconds to ([\d.]+) seconds",
         vals=[("S-PT-sync", "S", 1, SEC, "synchronous DCP downtime read as the save"),
               ("S-PT-async", "S", 2, SEC, "asynchronous DCP downtime read as the save (the hosts stay powered to persist)")]),
    dict(id="PT-visible", f=F4, src="PyTorch blog (2024-06-12)",
         quote="This is the visible downtime to the user and can take from 6 – 14 seconds for 7B-13B model sizes.",
         rx=r"from (\d+) – (\d+) seconds",
         vals=[("S-PT-vis6", "S", 1, SEC, "the low end of the visible downtime read as the save (the hosts stay powered)"),
               ("S-PT-vis14", "S", 2, SEC, "the high end of the visible downtime read as the save (the hosts stay powered)")]),
    dict(id="PT-legacy", f=F4, src="PyTorch blog (2024-06-12)",
         quote="torch.save could take up to 30 minutes to checkpoint a single 11B model (PyTorch 1.13).",
         rx=r"up to (\d+) minutes to checkpoint",
         vals=[("S-PT-legacy", "S", 1, MIN, "'up to 30 minutes' taken at its bound (legacy torch.save), read as the save")]),
    dict(id="CNR-snapshot", f=F4, src="Check-N-Run, arXiv:2010.08679 v2",
         quote="would stall training in our system for less than 7 seconds.",
         rx=r"less than (\d+) seconds",
         vals=[("S-CNR-snap", "S", 1, SEC, "'less than 7 seconds' taken at its bound; an in-memory snapshot read as the save")]),
    # ---------------- F4 context (not scored): pre-emption notices and power-control latencies
    dict(id="AWS-spot", f=F4, src="AWS EC2 User Guide",
         quote="A Spot Instance interruption notice is a warning that is issued two minutes before Amazon EC2 stops or terminates your Spot Instance.",
         rx=r"issued (two) minutes before",
         vals=[("X-AWS", "Tx", 1, MIN, "a cloud pre-emption notice, not a demand-response product: context only")]),
    dict(id="GCP-spot", f=F4, src="Google Cloud Spot VMs doc (2026-09-28)",
         quote="The shutdown period for Spot VMs is best effort and up to 30 seconds, which is shorter than the shutdown period for other instances .",
         rx=r"up to (\d+) seconds",
         vals=[("X-GCP", "Tx", 1, SEC, "a cloud shutdown period ('up to', taken at its bound): context only")]),
    dict(id="K8S-grace", f=F4, src="Kubernetes Pod Lifecycle",
         quote="The default terminationGracePeriodSeconds setting is 30 seconds.",
         rx=r"setting is (\d+) seconds",
         vals=[("X-K8S", "Tx", 1, SEC, "an orchestrator's default grace period: context only")]),
    dict(id="POLCA-lat", f=F4, src="POLCA, arXiv:2308.12908 v1, Table 1",
         quote="Power telemetry delay 2s Power brake latency 5s OOB commands latency 40s",
         rx=r"Power brake latency (\d+)s OOB commands latency (\d+)s",
         vals=[("Y-brake", "Tthr", 1, SEC, "a power brake's latency: how fast a throttle (not a pause) can cut power; context (H7)"),
               ("Y-OOB", "Tthr", 2, SEC, "out-of-band power-capping latency; context (H7)")]),
    dict(id="PERSEUS-sm", f=F4, src="Perseus, arXiv:2312.06902 v3",
         quote="The SM frequency of NVIDIA GPUs can be set via NVML [4] in around 10 ms",
         rx=r"in around (\d+) ms",
         vals=[("Y-SM", "Tthr", 1, SEC / 1000, "a GPU frequency change's latency ('around', taken at its value); context (H7)")]),
]

NOT_USED = [
    ("F2", "DFS 'respond for a minimum of 30 minutes'", "a minimum DURATION of response, not a response time"),
    ("F2", "DFS results 60 min after submission; bid window 1 h", "a procurement timeline, not a notice before the window: the rules "
     "state no minimum notice between acceptance and the window's start"),
    ("F2", "CAISO RDRR sustained >= 4 h; <= 15 events or 48 h per term", "durations and counts, not response times"),
    ("F2", "CPUC ELRP 1-5 h events, <= 60 h/yr", "durations, not response times"),
    ("F2", "ERCOT ERS 24/12 h cumulative deployment", "a cumulative duration, not a response time"),
    ("F2", "prices, payments, caps, VoLL, DFS K factor", "prices and settlement (H8, the data part), not response times"),
    ("F3", "NOGRR282 recovery to >= 90 % within 2 s", "a ride-through RECOVERY after a frequency excursion (the load must come back), "
     "not a curtailment response"),
    ("F3", "three disturbances within 1 minute (transfer scheme)", "a protection trigger, not a product's response time"),
    ("F3", "ramp limits (MW/min), oscillation limits, rebound, ramp events", "ramps and rebound (H5), not response times"),
    ("F4", "MegaScale 'several seconds' (GPU-to-host snapshot)", "no number in the quote; the in-memory snapshots of Check-N-Run and "
     "ByteCheckpoint's TBlock cover it"),
    ("F4", "ByteCheckpoint TLoad, MegaScale initialisation and catch-up, ByteRobust failover", "restart components (H4); H6 uses the Kokolis "
     "restart range"),
]

# ------------------------------------------------------------------------------------------------ assumed inputs
W = Fr(1000)                                   # DECLARED units (DR1 section 2 adopts EPS2 T1's)
RATE = ONE                                     # DECLARED units
D = Fr(1100)                                   # ASSUMED (EPS2 T1's decisive deadline)
H = Fr(4)                                      # ASSUMED (EPS2 T1's decisive event length)
SPACING = Fr(24)                               # CHOICE (EPS2 T1): one offer every 24 wall hours before hour W
R_EPS2 = Fr(1, 10)                             # ASSUMED (EPS2 T1's restart overhead, 6 minutes)
S_EPS2 = ZERO                                  # ASSUMED (EPS2 T1 has no save time)
I_ASSUMED = (Fr(1, 4), Fr(4))                  # ASSUMED periodic checkpoint intervals beside the sourced hourly one
EPS = Fr(1, 10 ** 6)                           # the p_all verification step (EPS2's)


def parse_sources():
    """Parse every sourced number out of its verbatim quote; returns (values, report)."""
    vals, rep = {}, []
    for s in SOURCES:
        found = s["quote"] in TEXT[s["f"]]
        m = re.search(s["rx"], s["quote"])
        rep.append((s, found, m is not None))
        if not (found and m):
            continue
        for vid, role, gi, unit, note in s["vals"]:
            if unit == "hhmm":
                h1, m1, h2, m2 = (int(m.group(i)) for i in gi)
                raw = f"{m.group(gi[0])}:{m.group(gi[1])} -> {m.group(gi[2])}:{m.group(gi[3])}"
                h = Fr(h2 * 60 + m2 - (h1 * 60 + m1)) * MIN
                vals[vid] = dict(h=h, raw=raw, role=role, src=s["src"], note=note, sid=s["id"], f=s["f"], unit=unit)
                continue
            raw = m.group(gi)
            num = d.q(WORDS[raw]) if raw in WORDS else (None if raw == "half" else d.q(raw))
            vals[vid] = dict(h=None, num=num, raw=raw, role=role, src=s["src"], note=note, sid=s["id"], f=s["f"], unit=unit)
            if raw == "half":
                vals[vid]["h"] = Fr(1, 2)
            elif unit != "cyc":
                vals[vid]["h"] = num * unit
    hz = vals.get("Hz-60")
    for v in vals.values():
        if v["unit"] == "cyc":
            v["h"] = (v["num"] / hz["num"]) * SEC if hz else None
    return vals, rep


def fmt_t(h) -> str:
    """A duration in hours, printed in s (below 2 min), min (below 2 h) or h."""
    if h is None:
        return "-"
    if h < 2 * MIN:
        return f"{float(h / SEC):g} s"
    if h < 2:
        return f"{float(h / MIN):g} min"
    return f"{float(h):g} h"


# ------------------------------------------------------------------------------------------------ pricing one job
_CACHE = {}


def price(job: d.Job) -> dict:
    """ETM's and OWN's p_all (minimum flat payment at which every offer of the season is accepted) for one job, verified by
    backward induction; ETM's stakes minus rate o and minus rate R; ETM's x* at every offer state."""
    key = (job.R, job.S, job.lost)
    if key in _CACHE:
        return _CACHE[key]
    offs = d.every(SPACING, H, job.W)
    K = len(offs)
    o = job.overhead
    out = dict(K=K, o=o, arms={})
    for arm in (d.ETM, d.OWN):
        F = d.value_fns(job, arm, offs)
        pa = d.p_all(job, arm, offs, F)
        a = dict(pa=pa, nmax=d.nmax(job, arm, H))
        if pa.kind == "threshold":
            at = d.play(job, arm, offs, pa.x)["events"]
            below = d.play(job, arm, offs, pa.x - EPS)["events"]
            a["verify"] = ((at == K) == pa.attained) and below < K
        else:
            a["verify"] = False
        if arm is d.ETM:
            xs = d.xstar_all(job, arm, offs, F)
            tgt = RATE * o / H
            a["n_states"] = len(xs)
            a["eq"] = sum(int(x.kind == "threshold" and x.closed and x.x == tgt) for x in xs.values())
            a["stake_o"] = [d.stake(job, arm, H, n) - RATE * o for n in range(K)]
            a["stake_R"] = [d.stake(job, arm, H, n) - RATE * job.R for n in range(K)]
        out["arms"][arm.name] = a
    out["ok"] = all(out["arms"][a]["pa"].kind == "threshold" for a in ("ETM", "OWN"))
    _CACHE[key] = out
    return out


def gneg(job: d.Job, pi) -> tuple[int, int, list]:
    """G-NEG for one job: no events offered (K = 0, and the no-offer realisation); ETM against WALL on six outcomes."""
    outcomes = (("curtailed fleet-hours", "fleet_hours", +1), ("payments", "payments", +1), ("valuation", "valuation", +1),
                ("fleet value", "fleet_value", +1), ("deadline met", "met", +1), ("completion hour", "completion", -1))
    offs = d.every(SPACING, H, job.W)
    n_cmp = ahead = 0
    rels = []
    for of, made in (((), None), (offs, [False] * len(offs))):
        pe = d.play(job, d.ETM, of, pi, made=made)
        pw = d.play(job, d.WALL, of, pi, made=made)
        for name, fld, sgn in outcomes:
            a_, b_ = float(pe[fld]), float(pw[fld])
            r = d.rel(a_, b_)
            better = (a_ > b_) if sgn > 0 else (a_ < b_)
            n_cmp += 1
            if better and r > 1e-2:
                ahead += 1
            rels.append((r, name))
    return n_cmp, ahead, rels


def main() -> int:
    print("DR1 check H6: response time; a lossless pause must save before the power drops; products need response within T")
    print(f"Declaration: Grid_Demand_Response/DECLARATION.md (pushed at {d.DECL_AT}; binding, not edited). Library: drlib.py (exact rationals).")
    print("Declared Q: where the save time S exceeds T, ETM cannot meet the product without losing work; the feasible product set is printed.")
    print("Forecast: Q holds.")
    print()
    vals, rep = parse_sources()
    all_found = all(f and m for _, f, m in rep)

    # ---------------------------------------------------------------- inputs
    print("INPUTS")
    print("  SOURCED  from docs/citations/dr1_f2/f3/f4_2026-09-29.md (each quote checked verbatim against its dossier's text at run time;")
    print("           the number parsed out of the quote by the regular expression shown; units converted to hours exactly):")
    for s, found, parsed in rep:
        print(f"    [{s['id']}] {s['f']}: {s['src']}; quote found verbatim: {d.yn(found)}; parsed: {d.yn(parsed)}")
        print(f"      \"{s['quote']}\"")
        print(f"      regex {s['rx']!r}")
        for vid, role, gi, unit, note in s["vals"]:
            if vid in vals:
                v = vals[vid]
                hs = (f"{v['num']} Hz" if role == "Hz" else "-" if v["h"] is None else f"{fmt_t(v['h'])} = {v['h']} h")
                print(f"      -> {vid:15} role {role:6} raw '{v['raw']}' = {hs}; CHOICE: {note}")
    hz = vals.get("Hz-60")
    ffr = vals.get("T-FFR15cyc")
    rrs = vals.get("T-RRSFFR")
    if hz and ffr and rrs:
        print(f"  cross-check: FFR's 15 cycles at the sourced {hz['num']} Hz = {fmt_t(ffr['h'])}; RRS-FFR's sourced response time = {fmt_t(rrs['h'])}; "
              f"equal: {d.yn(ffr['h'] == rrs['h'])}")
    for cid, tid in (("C-ERS10", "T-ERS10"), ("C-ERS30", "T-ERS30")):
        if cid in vals and tid in vals:
            print(f"  cross-check: {cid} (F3, {fmt_t(vals[cid]['h'])}) equals {tid} (F2, {fmt_t(vals[tid]['h'])}): {d.yn(vals[cid]['h'] == vals[tid]['h'])}")
    ik, lk = vals.get("I-KOK-hourly"), vals.get("L-KOK-half")
    if ik and lk:
        lj = d.lossy(d.Job(W, D, R_EPS2), ik["h"])
        print(f"  cross-check: drlib.lossy at the sourced interval {fmt_t(ik['h'])} loses {fmt_t(lj.lost)} per event; the source's average lost work "
              f"{fmt_t(lk['h'])}; equal: {d.yn(lj.lost == lk['h'])}")
    print(f"  DECLARED W = {W} compute-hours, value {RATE} per compute-hour at completion (DR1 section 2 adopts EPS2 T1's units)")
    print(f"  ASSUMED  D = {d.g(D)} h and event length H = {d.g(H)} h (EPS2 T1's decisive cell; they enter the payments only, not feasibility)")
    print(f"  ASSUMED  R = {R_EPS2} h (6 minutes; EPS2 T1's restart overhead) beside the sourced Kokolis u0 range; S = 0 (EPS2 T1 has no save)")
    print("           as one more save value: the EPS2 reference point R = 0.1 h, S = 0 sits inside the grid")
    print(f"  ASSUMED  periodic checkpoint intervals {', '.join(fmt_t(i) for i in I_ASSUMED)} beside the sourced hourly one (the lossy route)")
    print("  NOT USED (numbers in the dossiers' lists that are not response times, saves, restarts or intervals):")
    for fam, what, why in NOT_USED:
        print(f"    {fam}: {what}: {why}")
    print()

    products = sorted(((k, v) for k, v in vals.items() if v["role"] == "T"), key=lambda t: (t[1]["h"], t[0]))
    saves = [("S-EPS2", S_EPS2, "ASSUMED")] + [(k, v["h"], "SOURCED") for k, v in vals.items() if v["role"] == "S"]
    saves.sort(key=lambda t: (t[1], t[0]))
    restarts = [("R-EPS2", R_EPS2, "ASSUMED")] + [(k, v["h"], "SOURCED") for k, v in vals.items() if v["role"] == "R"]
    restarts.sort(key=lambda t: (t[1], t[0]))
    intervals = [(k, v["h"], "SOURCED") for k, v in vals.items() if v["role"] == "I"] + [
        (f"I-ASM-{d.g(i)}h", i, "ASSUMED") for i in I_ASSUMED]
    intervals.sort(key=lambda t: (t[1], t[0]))
    ctx_notices = sorted(((k, v) for k, v in vals.items() if v["role"] == "Tx"), key=lambda t: (t[1]["h"], t[0]))
    thr = sorted(((k, v) for k, v in vals.items() if v["role"] == "Tthr"), key=lambda t: (t[1]["h"], t[0]))
    print(f"  products ({len(products)}, scored): " + ", ".join(f"{k} {fmt_t(v['h'])}" for k, v in products))
    print(f"  saves ({len(saves)}):     " + ", ".join(f"{k} {fmt_t(h)}" for k, h, _ in saves))
    print(f"  restarts ({len(restarts)}):   " + ", ".join(f"{k} {fmt_t(h)}" for k, h, _ in restarts))
    print(f"  checkpoint intervals ({len(intervals)}): " + ", ".join(f"{k} {fmt_t(h)}" for k, h, _ in intervals))
    print()

    print("CHOICES")
    print("  CHOICE A product with response time T is met only if the fleet's power is down by T after the operator's instruction (or")
    print("         the trigger); a later drop is a non-delivery, not a slower delivery. The save starts at the instruction: the fleet")
    print("         does not save pre-emptively before it knows of the event (a pre-emptive save is the periodic checkpoint below).")
    print("  CHOICE The lossless route (ETM as declared): save for S at full power, then the power drops. It meets the product iff")
    print("         S <= T (drlib.response_ok, ties meet). A save is atomic: an interrupted save leaves only the last complete checkpoint.")
    print("  CHOICE The lossy route: the power drops at the instruction without a save (drlib.lossy): the job loses the work since")
    print("         its last periodic checkpoint, I/2 in expectation (the instruction's phase uniform over the interval I), redone as")
    print("         own hours without progress; S = 0. Stopping the computation is taken as instantaneous, so this route meets every")
    print("         product. These two routes are the only ways a pause meets a product; declining the event does not meet it.")
    print("  CHOICE 'ETM cannot meet the product without losing work' (per cell with S > T) = the lossless route does not meet T AND")
    print("         every route that meets T loses work (the least lost work among the meeting routes > 0) AND the pause's stake")
    print("         beyond the restart on that route is > 0 at every event count n = 0..K-1 (ETM's stake - rate R, drlib.stake).")
    print("  CHOICE Q holds iff that reading holds in every scored cell (product x save x restart x interval) with S > T; Q is not")
    print("         computable if any sourced quote is not found or not parsed, if any p_all is not a threshold, or if no scored cell")
    print("         has S > T (Q would be vacuous). The converse (S <= T: the lossless route meets with no lost work) is printed.")
    print("  CHOICE The feasible product set = for each save S, the scored products with S <= T (the lossless route meets them).")
    print("  CHOICE Prices (context for Q, not scored): p_all per curtailed fleet-hour, EPS2's decisive reading (drlib.p_all), for")
    print("         ETM and OWN, one offer every 24 wall hours before hour W (K = 41), known in advance; verified by backward")
    print("         induction at p_all and p_all - 1e-6. The lossless route's overhead is R + S, the lossy route's R + I/2.")
    print("  CHOICE DFS (no minimum notice, a 24 h maximum lead) has no stated T: printed at its two bounds, not scored and counted as")
    print("         an exclusion. F4's cloud pre-emption notices and power-control latencies are printed as context, not scored.")
    print("  CHOICE G-ZERO: on the lossless route, ETM's one-event stake minus rate (R + S) is exactly 0 at every n = 0..K-1 and")
    print("         ETM's x* == rate (R + S)/H (closed) at every offer state, for every (restart, save) pair (as H1 and H4: the save")
    print("         counts with R). The stake minus rate R alone (the declaration's wording 'beyond R') is printed; it equals rate S.")
    print("  CHOICE G-NEG: with no events offered (K = 0, and the no-offer realisation), ETM not ahead of WALL by more than 1 %")
    print("         (harness rel) on any outcome (curtailed fleet-hours, payments, valuation, fleet value, deadline met, completion hour,")
    print("         earlier ahead), on every lossless and lossy job, at pi = ETM's p_all of the job.")
    print("  NOTE   Q follows from the model's definitions once S > T (a save that has not finished leaves only the last periodic")
    print("         checkpoint); the check's content is the arithmetic, the feasible product set and the price of the lossy fallback.")
    print()

    # ---------------------------------------------------------------- feasibility table (product x save)
    print("FEASIBILITY TABLE (lossless route: S <= T; one row per product x save; margin = T - S)")
    print(f"  {'product':>12} {'T':>10} {'save':>14} {'S':>10} {'S<=T':>5} {'margin':>12} {'source of T':>6}")
    feas = {}
    for pid, pv in products:
        for sid, S, _ in saves:
            ok = d.response_ok(d.Job(W, D, R_EPS2, S=S), pv["h"])
            feas[(pid, sid)] = ok
            mg = pv["h"] - S
            sign = "" if mg >= 0 else "-"
            print(f"  {pid:>12} {fmt_t(pv['h']):>10} {sid:>14} {fmt_t(S):>10} {d.yn(ok):>5} {sign + fmt_t(abs(mg)):>12} {pv['f'][4:6]:>6}")
    print()
    print("FEASIBLE PRODUCT SET (per save: the products the lossless route meets)")
    for sid, S, src in saves:
        ps = [pid for pid, _ in products if feas[(pid, sid)]]
        print(f"  {sid:>14} S = {fmt_t(S):>10} ({src}): {len(ps):>2} of {len(products)}: {', '.join(ps) if ps else 'none'}")
    print("PER PRODUCT (the saves that fit)")
    for pid, pv in products:
        ss = [sid for sid, _, _ in saves if feas[(pid, sid)]]
        big = max((S for sid, S, _ in saves if feas[(pid, sid)]), default=None)
        print(f"  {pid:>12} T = {fmt_t(pv['h']):>10}: {len(ss):>2} of {len(saves)} saves fit; the largest that fits {fmt_t(big)}")
    print()
    dfs = vals.get("T-DFSmax")
    print("NOT SCORED: DFS (no stated T)")
    if dfs:
        lo = sum(int(d.response_ok(d.Job(W, D, R_EPS2, S=S), ZERO)) for _, S, _ in saves)
        hi = sum(int(d.response_ok(d.Job(W, D, R_EPS2, S=S), dfs["h"])) for _, S, _ in saves)
        print(f"  at the lower bound (no minimum notice, T = 0): {lo} of {len(saves)} saves fit; at the maximum lead ({fmt_t(dfs['h'])}): {hi} of {len(saves)}.")
        print("  Whether a lossless pause meets a DFS window is decided by the realised notice in the event records (the data part), not by the rules.")
    print("CONTEXT (not scored): F4 pre-emption notices and grace periods as if they were a T")
    for xid, xv in ctx_notices:
        ss = [sid for sid, S, _ in saves if S <= xv["h"]]
        print(f"  {xid:>8} {fmt_t(xv['h']):>8}: {len(ss):>2} of {len(saves)} saves fit: {', '.join(ss)}")
    print("CONTEXT (not scored): a throttle (power capping, H7) cuts power in its control latency, with no save and no lost work")
    for yid, yv in thr:
        ps = [pid for pid, pv in products if yv["h"] <= pv["h"]]
        print(f"  {yid:>8} {fmt_t(yv['h']):>8}: within T for {len(ps):>2} of {len(products)} products: {', '.join(ps)}")
    print()

    # ---------------------------------------------------------------- prices
    print("PRICES: lossless route (per restart x save; overhead o = R + S)")
    hdr = (f"  {'restart':>12} {'save':>14} {'o':>10} {'K':>3} {'ETM nmax':>8} {'OWN nmax':>8} {'ETM p_all':>12} {'(R+S)/H':>12} "
           f"{'OWN p_all':>14} {'ver':>3} {'ETM x*=o/H states':>18}")
    print(hdr)
    ll = {}
    for rid, R, _ in restarts:
        for sid, S, _ in saves:
            job = d.Job(W, D, R, S=S, rate=RATE)
            c = price(job)
            ll[(rid, sid)] = dict(job=job, c=c)
            A = c["arms"]
            print(f"  {rid:>12} {sid:>14} {fmt_t(c['o']):>10} {c['K']:>3} {str(A['ETM']['nmax']):>8} {str(A['OWN']['nmax']):>8} "
                  f"{float(A['ETM']['pa'].x):>12.6f} {float(RATE * c['o'] / H):>12.6f} {float(A['OWN']['pa'].x):>14.6f} "
                  f"{d.yn(A['ETM']['verify'] and A['OWN']['verify']):>3} {A['ETM']['eq']:>8}/{A['ETM']['n_states']:<9}")
    print()
    print("PRICES: lossy route (per restart x checkpoint interval; overhead o = R + I/2; no save)")
    print(f"  {'restart':>12} {'interval':>14} {'lost':>10} {'o':>10} {'ETM nmax':>8} {'OWN nmax':>8} {'ETM p_all':>12} {'OWN p_all':>14} "
          f"{'ver':>3} {'min stake-R':>12} {'max stake-R':>12}")
    lj = {}
    for rid, R, _ in restarts:
        for iid, I, _ in intervals:
            job = d.lossy(d.Job(W, D, R, rate=RATE), I)
            c = price(job)
            lj[(rid, iid)] = dict(job=job, c=c)
            A = c["arms"]
            sr = A["ETM"]["stake_R"]
            print(f"  {rid:>12} {iid:>14} {fmt_t(job.lost):>10} {fmt_t(c['o']):>10} {str(A['ETM']['nmax']):>8} {str(A['OWN']['nmax']):>8} "
                  f"{float(A['ETM']['pa'].x):>12.6f} {float(A['OWN']['pa'].x):>14.6f} {d.yn(A['ETM']['verify'] and A['OWN']['verify']):>3} "
                  f"{float(min(sr)):>12.6f} {float(max(sr)):>12.6f}")
    print("  (stake-R: ETM's one-event stake minus rate R on the lossy route, over n = 0..K-1: the content the pause no longer removes)")
    print()

    # ---------------------------------------------------------------- scored cells
    print("PER-CELL TABLE (scored; one row per product x save at R = R-EPS2; the three lossy columns are the checkpoint intervals;")
    print("  route price = ETM p_all per curtailed fleet-hour; best = the cheaper route that meets T; Q-cell only where S > T)")
    ih = " ".join(f"{('lossy ' + fmt_t(I)):>14}" for _, I, _ in intervals)
    bh = " ".join(f"{('best@' + fmt_t(I)):>16}" for _, I, _ in intervals)
    print(f"  {'product':>12} {'T':>9} {'save':>14} {'S':>9} {'S>T':>4} {'lossless':>10} {ih} {bh} {'Q-cell':>7}")
    cells = []
    for pid, pv in products:
        T = pv["h"]
        for sid, S, _ in saves:
            for rid, R, _ in restarts:
                L = ll[(rid, sid)]
                exceeds = S > T
                lossless_meets = d.response_ok(L["job"], T)
                for iid, I, _ in intervals:
                    Y = lj[(rid, iid)]
                    routes = []                                   # (name, meets, lost, price)
                    routes.append(("lossless", lossless_meets, L["job"].lost, L["c"]["arms"]["ETM"]["pa"].x))
                    routes.append(("lossy", True, Y["job"].lost, Y["c"]["arms"]["ETM"]["pa"].x))
                    meeting = [r for r in routes if r[1]]
                    min_lost = min(r[2] for r in meeting) if meeting else None
                    stake_pos = all(s > 0 for s in Y["c"]["arms"]["ETM"]["stake_R"])
                    best = min(meeting, key=lambda r: (r[3], r[0])) if meeting else None
                    qcell = (not lossless_meets) and min_lost is not None and min_lost > 0 and stake_pos if exceeds else None
                    conv = lossless_meets and L["job"].lost == 0 if not exceeds else None
                    cheaper_lossy = lossless_meets and Y["c"]["arms"]["ETM"]["pa"].x < L["c"]["arms"]["ETM"]["pa"].x
                    cells.append(dict(pid=pid, T=T, sid=sid, S=S, rid=rid, R=R, iid=iid, I=I, exceeds=exceeds, lm=lossless_meets,
                                      min_lost=min_lost, stake_pos=stake_pos, best=best, qcell=qcell, conv=conv, cheaper_lossy=cheaper_lossy))
            row = [c for c in cells if c["pid"] == pid and c["sid"] == sid and c["rid"] == "R-EPS2"]
            L = ll[("R-EPS2", sid)]
            lsp = f"{float(L['c']['arms']['ETM']['pa'].x):.6f}" if row[0]["lm"] else "fails T"
            lys = " ".join(f"{float(lj[('R-EPS2', c['iid'])]['c']['arms']['ETM']['pa'].x):>14.6f}" for c in row)
            bs = " ".join(f"{(c['best'][0] + ' ' + format(float(c['best'][3]), '.4f')):>16}" for c in row)
            qc = [c["qcell"] for c in row]
            qs = "-" if row[0]["qcell"] is None else ("holds" if all(qc) else "fails")
            print(f"  {pid:>12} {fmt_t(T):>9} {sid:>14} {fmt_t(S):>9} {d.yn(S > T):>4} {lsp:>10} {lys} {bs} {qs:>7}")
    print()

    # ---------------------------------------------------------------- Q
    ok_kind = all(x["c"]["ok"] for x in list(ll.values()) + list(lj.values()))
    ver_ok = all(x["c"]["arms"][a]["verify"] for x in list(ll.values()) + list(lj.values()) for a in ("ETM", "OWN"))
    n_all = len(cells)
    exc = [c for c in cells if c["exceeds"]]
    nexc = [c for c in cells if not c["exceeds"]]
    q_n = sum(int(c["qcell"]) for c in exc)
    conv_n = sum(int(c["conv"]) for c in nexc)
    lossless_in_exc = sum(int(c["lm"]) for c in exc)
    stake_fail = sum(int(not c["stake_pos"]) for c in exc)
    lost_zero = sum(int(c["min_lost"] is None or c["min_lost"] <= 0) for c in exc)
    cheaper = [c for c in cells if c["cheaper_lossy"]]
    pairs_exc = sorted({(c["pid"], c["sid"]) for c in exc})
    pairs_all = sorted({(c["pid"], c["sid"]) for c in cells})
    if not all_found or not ok_kind or not exc:
        qv = "not computable"
    else:
        qv = "holds" if q_n == len(exc) else "fails"
    minlost_exc = min((c["min_lost"] for c in exc), default=None)
    print("Q")
    print(f"  inputs: every sourced quote found verbatim and parsed: {d.yn(all_found)}; every p_all a threshold: {d.yn(ok_kind)}; "
          f"p_all verified by backward induction for ETM and OWN on every job: {d.yn(ver_ok)}")
    print(f"  scored cells (product x save x restart x interval): {n_all} = {len(products)} x {len(saves)} x {len(restarts)} x {len(intervals)}; "
          f"with S > T: {len(exc)} ({len(pairs_exc)} of {len(pairs_all)} product x save pairs)")
    print(f"  in the S > T cells: the lossless route meets T in {lossless_in_exc}; the least lost work among the meeting routes is 0 in "
          f"{lost_zero}; the lossy route's stake beyond R is not > 0 at some n in {stake_fail}; the least lost work there is "
          f"{fmt_t(minlost_exc)}")
    print(f"  Q (ETM cannot meet the product without losing work, in every S > T cell): {q_n} of {len(exc)} -> {qv}")
    print("  per product (all restarts and intervals): " + "; ".join(
        f"{pid} {sum(int(c['qcell']) for c in exc if c['pid'] == pid)}/{sum(int(c['pid'] == pid) for c in exc)}" for pid, _ in products))
    print(f"  converse (S <= T: the lossless route meets with no lost work): {conv_n} of {len(nexc)} cells")
    print(f"  the lossy route is cheaper than a lossless route that meets T (a save longer than the expected lost work, R equal): "
          f"{len(cheaper)} of {len(nexc)} S <= T cells, at saves {', '.join(sorted({c['sid'] for c in cheaper}, key=lambda s: [x[1] for x in saves if x[0] == s][0])) or 'none'}")
    fs = {sid: sum(int(feas[(pid, sid)]) for pid, _ in products) for sid, _, _ in saves}
    print(f"  feasible products per save (of {len(products)}): " + ", ".join(f"{sid} {n}" for sid, n in fs.items()))
    print(f"  the investigator's forecast (Q holds) is {'right' if qv == 'holds' else ('wrong' if qv == 'fails' else 'not decidable')}")
    print()

    # ---------------------------------------------------------------- gate
    stakes = [s for x in ll.values() for s in x["c"]["arms"]["ETM"]["stake_o"]]
    stakes_R = [s for x in ll.values() for s in x["c"]["arms"]["ETM"]["stake_R"]]
    stakeR_is_S = all(s == RATE * x["job"].S for x in ll.values() for s in x["c"]["arms"]["ETM"]["stake_R"])
    etm_states = sum(x["c"]["arms"]["ETM"]["n_states"] for x in ll.values())
    etm_eq = sum(x["c"]["arms"]["ETM"]["eq"] for x in ll.values())
    mx = max(abs(s) for s in stakes)
    gz = mx == 0 and etm_eq == etm_states
    n_cmp = ahead = 0
    rels = []
    for x in list(ll.values()) + list(lj.values()):
        a, b, r = gneg(x["job"], x["c"]["arms"]["ETM"]["pa"].x)
        n_cmp += a
        ahead += b
        rels += r
    wr = max(rels, key=lambda t: t[0])
    gn = ahead == 0
    print("GATE")
    print(f"  G-ZERO: lossless route, {len(ll)} (restart, save) jobs: max |ETM stake - rate (R + S)| over {len(stakes)} event counts = {float(mx):g} "
          f"(exact); ETM's x* == rate (R + S)/H (closed) at {etm_eq} of {etm_states} offer states -> {'holds' if gz else 'FAILS'}")
    print(f"          (the stake minus rate R alone equals rate S at every job and event count: {d.yn(stakeR_is_S)}; it ranges over "
          f"{float(min(stakes_R)):g}..{float(max(stakes_R)):g} h)")
    print(f"  G-NEG: no events offered (K = 0, and the no-offer realisation), {len(ll) + len(lj)} jobs (lossless and lossy) x 2, {n_cmp} comparisons "
          f"of ETM against WALL on six outcomes; ETM ahead by more than 1 % in {ahead}; largest rel {wr[0]:.3e} ({wr[1]}) -> {'holds' if gn else 'FAILS'}")
    print()
    print("CHANGES AFTER THE FIRST RUN (bug fixes only; no prediction, arm, threshold, grid or reading changed)")
    print("  1. Display only: the grid frequency (60 Hz, parsed from the Regulation quote) was printed with an hours suffix ('60 h');")
    print("     it now prints as '60 Hz'. The value was already used correctly (FFR's 15 cycles = 0.25 s, cross-checked against RRS-FFR).")
    print("  2. Display only: a per-product count of the S > T cells where Q's reading holds was added to the Q block, and the NOT USED")
    print("     line on DFS's procurement timeline was reworded. No input, cell, reading or verdict changed.")
    print()
    print(f"RESULT H6: Q {qv}; G-ZERO {'holds' if gz else 'FAILS'} "
          f"(max |ETM stake - rate (R + S)| = {float(mx):g} over {len(stakes)} event counts in {len(ll)} jobs; ETM x* = (R + S)/H at "
          f"{etm_eq} of {etm_states} offer states); G-NEG {'holds' if gn else 'FAILS'} (ETM ahead of WALL by more than 1 % in {ahead} of "
          f"{n_cmp} no-event comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
