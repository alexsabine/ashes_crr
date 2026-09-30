"""DR1 check H4: realistic restart and save overheads (from the F4 dossier), event lengths 0.5-4 h.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 2, row H4:
  check:      realistic restart and save overheads (from the F4 dossier, else ASSUMED ranges), event lengths 0.5-4 h
  Q:          ETM's minimum payment stays below OWN's at every overhead and length; the ratio shrinks as overheads grow
  forecast:   Q holds
This check also prints the gate's G-ZERO and G-NEG (G-POS belongs to H1).

The arithmetic is the shared library Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; its selftest
reproduces EPS2 T1 line for line). Every verdict word printed here is computed from the numbers (R15). Every input number
is either sourced (a verbatim quote from docs/citations/dr1_f4_2026-09-29.md, checked against the dossier text at run
time, the number parsed out of the quote by a regular expression) or printed as ASSUMED; every modelling choice is printed
as CHOICE. Rung R4 at most (synthetic model); a note, not evidence (R8). Deterministic, stdlib only (via drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h4.py > Grid_Demand_Response/checks/dr_h4.txt
"""
from __future__ import annotations

import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as d  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
F4 = "dr1_f4_2026-09-29.md"
F4_TEXT = (REPO / "docs" / "citations" / F4).read_text(encoding="utf-8")
ZERO, ONE = Fr(0), Fr(1)
SEC, MIN = Fr(1, 3600), Fr(1, 60)          # hours per second, per minute

# ------------------------------------------------------------------------------------------------ sourced inputs (quotes)
# Each source: id, short citation, verbatim quote (a substring of the dossier), regex, and the named values it yields:
# (value id, role, group index, unit in hours, CHOICE note). role: 'R' restart, 'S' save, 'lost' (sensitivity), 'unused'.
SOURCES = [
    dict(id="KOK-u0", src="Kokolis et al., arXiv:2410.21680 v2 (HPCA 2025)",
         quote="For the RSC clusters, rf ≈5 × 10−3 failures per GPU node-day of runtime, wcp ≈5 mins, u0 ≈5 −20 mins, and (Nnodesrf)−1 ≳0.1 day.",
         rx=r"wcp ≈(\d+) mins, u0 ≈(\d+) −(\d+) mins",
         vals=[("S-KOK-wcp", "S", 1, MIN, "the paper's checkpoint write estimate for the RSC clusters, read as the save"),
               ("R-KOK-u0lo", "R", 2, MIN, "the low end of the paper's restart-overhead range u0"),
               ("R-KOK-u0hi", "R", 3, MIN, "the high end of the paper's restart-overhead range u0")]),
    dict(id="KOK-lost", src="Kokolis et al., arXiv:2410.21680 v2 (HPCA 2025)",
         quote="we assume that all jobs checkpoint hourly (we find this is a typical checkpoint interval for larger jobs on the RSC clusters), giving an average of half an hour of lost work.",
         rx=r"an average of (half) an hour of lost work",
         vals=[("L-KOK-half", "lost", 1, None, "'half an hour' read as 30 minutes; lost work of an unplanned cut, not a lossless pause: sensitivity only")]),
    dict(id="BR-failover", src="ByteRobust, arXiv:2509.16293 v4 (SOSP '25)",
         quote="We observed that the time cost of failover operations is often more than 10 minutes for the large model training at the scale of 10,000 GPUs.",
         rx=r"often more than (\d+) minutes",
         vals=[("R-BR-failover", "R", 1, MIN, "'more than 10 minutes' taken at its bound, 10 minutes (a failure failover read as a restart)")]),
    dict(id="MS-init-default", src="MegaScale, NSDI '24",
         quote="the initialization time for Megatron-LM on 2,048 NVIDIA Ampere GPUs is approximately 1047 seconds.",
         rx=r"approximately (\d+) seconds",
         vals=[("R-MS-init1047", "R", 1, SEC, "one component (initialisation, default tooling) read as the whole restart")]),
    dict(id="MS-init-mid", src="MegaScale, NSDI '24",
         quote="This reduces the initialization time to 361 seconds on 2,048 GPUs.",
         rx=r"time to (\d+) seconds on 2,048",
         vals=[("R-MS-init361", "R", 1, SEC, "one component (initialisation, first optimisation) read as the whole restart")]),
    dict(id="MS-init-opt", src="MegaScale, NSDI '24",
         quote="The initialization time is reduced to under 5 seconds on 2048 GPUs, and to under 30 seconds on more than 10,000 GPUs with those optimizations.",
         rx=r"under (\d+) seconds on 2048 GPUs, and to under (\d+) seconds on more than 10,000",
         vals=[("R-MS-init5", "R", 1, SEC, "'under 5 seconds' taken at its bound; initialisation only, read as the whole restart"),
               ("R-MS-init30", "R", 2, SEC, "'under 30 seconds' (> 10,000 GPUs) taken at its bound; initialisation only")]),
    dict(id="MS-catchup", src="MegaScale, NSDI '24",
         quote="the system can catch up to the training progress prior to the crash within 15 minutes from the latest checkpoints, maintaining over 90% effective training time rate",
         rx=r"within (\d+) minutes from the latest checkpoints",
         vals=[("U-MS-catchup", "unused", 1, MIN, "crash recovery including re-done lost work, not a lossless pause's restart: not used")]),
    dict(id="BC-405B", src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25), Table 8",
         quote="Text Transformer 405B Megatron-LM 8960 TP=8, DP=70, PP=16 0.59 51.06 129.49",
         rx=r"PP=16 ([\d.]+) ([\d.]+) ([\d.]+)$",
         vals=[("S-BC405-block", "S", 1, SEC, "TBlock read as the save before the power drops when the hosts stay powered"),
               ("S-BC405-save", "S", 2, SEC, "TSave read as the end-to-end persistent save before the power drops"),
               ("R-BC405-load", "R", 3, SEC, "TLoad (one component) read as the whole restart")]),
    dict(id="BC-7B", src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25), Table 8",
         quote="Vision Transformer 7B FSDP 1488 ZeRO-2 0.34 20.13 265.73",
         rx=r"ZeRO-2 ([\d.]+) ([\d.]+) ([\d.]+)$",
         vals=[("S-BC7-block", "S", 1, SEC, "TBlock read as the save before the power drops when the hosts stay powered"),
               ("S-BC7-save", "S", 2, SEC, "TSave read as the end-to-end persistent save before the power drops"),
               ("R-BC7-load", "R", 3, SEC, "TLoad (one component) read as the whole restart")]),
    dict(id="BC-175B", src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25)",
         quote="the average end-to-end time required to save checkpoints of a GPT 175B model, trained on 4096 GPUs, to HDFS can be 200 seconds.",
         rx=r"can be (\d+) seconds",
         vals=[("S-BC175-save", "S", 1, SEC, "an end-to-end save before optimisation, read as the save before the power drops")]),
    dict(id="BC-loader", src="ByteCheckpoint, arXiv:2407.20143 v4 (NSDI '25)",
         quote="the state collection process typically takes around 8 seconds.",
         rx=r"takes around (\d+) seconds",
         vals=[("U-BC-loader", "unused", 1, SEC, "a component of a save (data-loader state), inside the end-to-end saves: not used")]),
    dict(id="GEM-remote", src="GEMINI, SOSP '23",
         quote="it takes 42 minutes to checkpoint the model states of MT-NLG [68] to the remote persistent storage when the bandwidth is 20Gbps.",
         rx=r"it takes (\d+) minutes to checkpoint",
         vals=[("S-GEM-remote", "S", 1, MIN, "a full save to remote storage at 20 Gbps, read as the save before the power drops")]),
    dict(id="PT-dcp", src="PyTorch blog (2024-06-12)",
         quote="Example: 7B model ‘down time’ for a checkpoint goes from an average of 148.8 seconds to 6.3 seconds, or 23.62x faster.",
         rx=r"average of ([\d.]+) seconds to ([\d.]+) seconds",
         vals=[("S-PT-sync", "S", 1, SEC, "synchronous DCP downtime read as the save"),
               ("S-PT-async", "S", 2, SEC, "asynchronous DCP downtime read as the save (hosts stay powered)")]),
    dict(id="PT-visible", src="PyTorch blog (2024-06-12)",
         quote="This is the visible downtime to the user and can take from 6 – 14 seconds for 7B-13B model sizes.",
         rx=r"from (\d+) – (\d+) seconds",
         vals=[("S-PT-vis6", "S", 1, SEC, "the low end of the visible downtime read as the save (hosts stay powered)"),
               ("S-PT-vis14", "S", 2, SEC, "the high end of the visible downtime read as the save (hosts stay powered)")]),
    dict(id="PT-legacy", src="PyTorch blog (2024-06-12)",
         quote="torch.save could take up to 30 minutes to checkpoint a single 11B model (PyTorch 1.13).",
         rx=r"up to (\d+) minutes to checkpoint",
         vals=[("S-PT-legacy", "S", 1, MIN, "'up to 30 minutes' taken at its bound (legacy torch.save), read as the save")]),
    dict(id="CNR-snapshot", src="Check-N-Run, arXiv:2010.08679 v2",
         quote="would stall training in our system for less than 7 seconds.",
         rx=r"less than (\d+) seconds",
         vals=[("S-CNR-snap", "S", 1, SEC, "'less than 7 seconds' taken at its bound; an in-memory snapshot read as the save")]),
]

# ------------------------------------------------------------------------------------------------ assumed inputs
W = Fr(1000)                                   # DECLARED units (DR1 section 2 adopts EPS2 T1's)
RATE = ONE                                     # DECLARED units
DS = (Fr(1100), Fr(1500))                      # ASSUMED (EPS2 T1's deadlines)
HS = (Fr(1, 2), Fr(1), Fr(2), Fr(3), Fr(4))    # ASSUMED grid over the declared 0.5-4 h
SPACING = Fr(24)                               # CHOICE (EPS2 T1): one offer every 24 wall hours before hour W
R_EPS2 = Fr(1, 10)                             # ASSUMED (EPS2 T1's restart overhead, 6 minutes)
S_EPS2 = ZERO                                  # ASSUMED (EPS2 T1 has no save time)
SENS_SPACINGS = (Fr(12), Fr(48))               # ASSUMED sensitivity spacings (EPS2's)
EPS = Fr(1, 10 ** 6)                           # the p_all verification step (EPS2's)


def parse_sources():
    """Parse every sourced number out of its verbatim quote; returns (values, report) with values {id: (hours, role, src, note)}."""
    vals, rep = {}, []
    for s in SOURCES:
        found = s["quote"] in F4_TEXT
        m = re.search(s["rx"], s["quote"])
        rep.append((s, found, m is not None))
        if not (found and m):
            continue
        for vid, role, gi, unit, note in s["vals"]:
            raw = m.group(gi)
            if raw == "half":
                h = Fr(30) * MIN
            else:
                h = d.q(raw) * unit
            vals[vid] = dict(h=h, raw=raw, role=role, src=s["src"], note=note, sid=s["id"])
    return vals, rep


def fmt_s(h: Fr) -> str:
    return f"{float(h / SEC):g} s"


# ------------------------------------------------------------------------------------------------ one (D, H, R, S) cell
_CACHE = {}


def run_cell(D: Fr, H: Fr, R: Fr, S: Fr, lost: Fr = ZERO, spacing: Fr = SPACING, full: bool = True) -> dict:
    key = (D, H, R + S + lost, spacing, full)
    if key in _CACHE:
        return _CACHE[key]
    job = d.Job(W, D, R, S=S, lost=lost, rate=RATE)
    offs = d.every(spacing, H, job.W)
    K = len(offs)
    o = job.overhead
    out = dict(job=job, K=K, o=o, arms={})
    for arm in (d.ETM, d.OWN, d.WALL):
        F = d.value_fns(job, arm, offs)
        pa = d.p_all(job, arm, offs, F)
        a = dict(pa=pa, nmax=d.nmax(job, arm, H))
        if full and arm is not d.WALL:
            # p_all verified by backward induction: at p_all every offer is accepted (if attained), just below it not
            at = d.play(job, arm, offs, pa.x)["events"] if pa.kind == "threshold" else None
            below = d.play(job, arm, offs, pa.x - EPS)["events"] if pa.kind == "threshold" else None
            a["verify"] = pa.kind == "threshold" and ((at == K) == pa.attained) and below < K
            # closed form: c/e, or (c + W rate/(K - nmax))/e at zero slack (rule_xstar with the offers left after it)
            nm = a["nmax"]
            if nm is not None and nm < K:
                cf = d.rule_xstar(job, arm, H, nm, K - 1 - nm)
            else:
                cf = d.rule_xstar(job, arm, H, 0, K - 1)
            a["cf"] = cf
            a["cf_ok"] = pa.kind == "threshold" and pa.x == cf
        if full and arm is d.ETM:
            xs = d.xstar_all(job, arm, offs, F)
            tgt = RATE * o / H
            a["n_states"] = len(xs)
            a["eq"] = sum(int(x.kind == "threshold" and x.closed and x.x == tgt) for x in xs.values())
            a["stakes"] = [d.stake(job, arm, H, n) - RATE * o for n in range(K)]
        out["arms"][arm.name] = a
    out["h0"] = d.h0_price(job, offs) if full else None
    e, w = out["arms"]["ETM"]["pa"], out["arms"]["OWN"]["pa"]
    out["ok_kind"] = e.kind == "threshold" and w.kind == "threshold"
    out["ratio"] = (w.x / e.x) if out["ok_kind"] and e.x != 0 else None
    out["below"] = out["ok_kind"] and e.x < w.x
    out["notabove"] = out["ok_kind"] and e.x <= w.x
    nm = out["arms"]["OWN"]["nmax"]
    out["binds"] = nm is not None and nm < K
    _CACHE[key] = out
    return out


def row_summary(seq):
    """seq: [(o, ratio)] sorted by o (distinct o). Returns rises, falls, flats, first, last."""
    rises = falls = flats = 0
    for (o1, r1), (o2, r2) in zip(seq, seq[1:]):
        if r2 > r1:
            rises += 1
        elif r2 < r1:
            falls += 1
        else:
            flats += 1
    return rises, falls, flats, seq[0][1], seq[-1][1]


def main() -> int:
    print("DR1 check H4: realistic restart and save overheads (F4 dossier), event lengths 0.5-4 h")
    print(f"Declaration: Grid_Demand_Response/DECLARATION.md (pushed at {d.DECL_AT}; binding, not edited). Library: drlib.py (exact rationals).")
    print("Declared Q: ETM's minimum payment stays below OWN's at every overhead and length; the ratio shrinks as overheads grow.")
    print("Forecast: Q holds.")
    print()
    vals, rep = parse_sources()
    all_found = all(f and m for _, f, m in rep)
    # ---------------------------------------------------------------- inputs
    print("INPUTS")
    print(f"  SOURCED  from docs/citations/{F4} (each quote checked verbatim against the dossier text at run time; the number parsed out")
    print("           of the quote by the regular expression shown; units converted to hours exactly):")
    for s, found, parsed in rep:
        print(f"    [{s['id']}] {s['src']}; quote found verbatim: {d.yn(found)}; parsed: {d.yn(parsed)}")
        print(f"      \"{s['quote']}\"")
        print(f"      regex {s['rx']!r}")
        for vid, role, gi, unit, note in s["vals"]:
            if vid in vals:
                v = vals[vid]
                print(f"      -> {vid:15} role {role:6} raw '{v['raw']}' = {fmt_s(v['h'])} = {v['h']} h; CHOICE: {note}")
    print(f"  DECLARED W = {W} compute-hours, value {RATE} per compute-hour at completion (DR1 section 2 adopts EPS2 T1's units)")
    print(f"  ASSUMED  R = {R_EPS2} h (6 minutes; EPS2 T1's restart overhead) as one more restart value, and S = 0 (EPS2 T1 has no save)")
    print(f"           as one more save value: the EPS2 reference point R = 0.1 h, S = 0 sits inside the grid")
    print(f"  ASSUMED  D in {{{', '.join(d.g(x) for x in DS)}}} h (EPS2 T1's deadlines; the declaration fixes no D for H4)")
    print(f"  ASSUMED  event lengths H in {{{', '.join(d.g(x) for x in HS)}}} h (a grid over the declared 0.5-4 h)")
    print(f"  ASSUMED  (sensitivity only, not scored) offer spacings of {', '.join(d.g(x) for x in SENS_SPACINGS)} h (EPS2 T1's sensitivity)")
    print()
    Rs = [("R-EPS2", R_EPS2, "ASSUMED")] + sorted(((k, v["h"], "SOURCED") for k, v in vals.items() if v["role"] == "R"), key=lambda t: (t[1], t[0]))
    Ss = [("S-EPS2", S_EPS2, "ASSUMED")] + sorted(((k, v["h"], "SOURCED") for k, v in vals.items() if v["role"] == "S"), key=lambda t: (t[1], t[0]))
    Rs.sort(key=lambda t: (t[1], t[0]))
    Ss.sort(key=lambda t: (t[1], t[0]))
    print(f"  restart grid ({len(Rs)} values): " + ", ".join(f"{k} {fmt_s(h)}" for k, h, _ in Rs))
    print(f"  save grid ({len(Ss)} values):    " + ", ".join(f"{k} {fmt_s(h)}" for k, h, _ in Ss))
    unused = [(k, v) for k, v in vals.items() if v["role"] == "unused"]
    for k, v in unused:
        print(f"  NOT USED {k}: {fmt_s(v['h'])} ({v['src']}): {v['note']}")
    print("  NOT USED the dossier's other numbers (pre-emption notices and grace periods: H6; power capping and frequency throttling:")
    print("           H7/H2; the Daly-Young '5 minute' quote duplicates wcp and u0's low end; the 600 ms average stall is covered by TBlock)")
    print()
    print("CHOICES")
    print("  CHOICE The overhead grid is the full cross product of every restart value with every save value (the sources do not pair")
    print("         them): overhead o = R + S per event, own running hours without progress (drlib: the save counts as own hours,")
    print("         added to R). OWN and ETM both pay o per event (both are lossless pauses; they differ in the deadline clock).")
    print("  CHOICE A single sourced component (an initialisation or a load time) is read as the whole restart R; a bound ('under',")
    print("         'more than', 'up to', 'less than') is taken at its stated value. Each such reading is printed beside its value.")
    print("  CHOICE Offers as in EPS2 T1: one every 24 wall hours at hours 24, 48, ... strictly before hour W = 1000 (K = 41), known in")
    print("         advance (p = 1); every arm is running at every offer. Payment flat per curtailed fleet-hour.")
    print("  CHOICE 'Minimum payment' = EPS2's decisive reading p_all (drlib.p_all): the minimum flat payment at which the arm accepts")
    print("         every offer of the season; verified in every scored cell by backward induction at p_all and at p_all - 1e-6, and")
    print("         against the closed form (drlib.rule_xstar: (R + S)/H, or ((R + S) + W rate/(K - nmax))/H when OWN's wall-clock slack")
    print("         absorbs fewer than K events).")
    print("  CHOICE 'Stays below' (Q-a, scored) = p_all(ETM) < p_all(OWN) strictly, in every scored cell (D x H x R x S). The non-strict")
    print("         reading (ETM never above OWN) is printed, not scored.")
    print("  CHOICE 'The ratio' = p_all(OWN) / p_all(ETM) (OWN's minimum payment as a multiple of ETM's; ETM's advantage). 'Shrinks as")
    print("         overheads grow' (Q-b, scored) = for every (D, H), along the distinct overheads o in increasing order, the ratio never")
    print("         rises between neighbours and is strictly smaller at the largest o than at the smallest. The non-strict reading (the")
    print("         ratio never rises) is printed, not scored.")
    print("  CHOICE Q holds iff Q-a and Q-b hold; Q is not computable if any sourced quote is not found or not parsed, or if any")
    print("         arm's p_all is not a threshold (always / never).")
    print("  CHOICE G-ZERO: ETM's one-event stake minus rate (R + S), at every event count n = 0..K-1 of every scored cell, exactly 0,")
    print("         and ETM's x* == rate (R + S)/H (closed) at every offer state (as in H1: the save counts with R). The stake minus")
    print("         rate R alone (the declaration's wording 'beyond R') is printed too; it equals rate S.")
    print("  CHOICE G-NEG: with no events offered (K = 0, and each scored cell's realisation in which no offer is made), ETM not ahead of")
    print("         WALL by more than 1 % (harness rel) on any outcome: curtailed fleet-hours, payments, valuation, fleet value, deadline")
    print("         met, completion hour (earlier is ahead); payment pi = ETM's p_all of the cell.")
    print("  CHOICE WALL's p_all and H0's reservation price are printed for context; TIER is not part of H4 (H2 checks it).")
    print()

    # ---------------------------------------------------------------- scored grid
    cells = []
    for D in DS:
        for H in HS:
            for rid, R, rsrc in Rs:
                for sid, S, ssrc in Ss:
                    c = run_cell(D, H, R, S)
                    job = d.Job(W, D, R, S=S, rate=RATE)          # the cell's own job (the cache is keyed on o = R + S)
                    stakes_R = [d.stake(job, d.ETM, H, n) - RATE * R for n in range(c["K"])]
                    cells.append(dict(D=D, H=H, rid=rid, R=R, sid=sid, S=S, c=c, job=job, stakes_R=stakes_R))
    print("PER-CELL TABLE (scored grid; sorted by D, H, overhead o = R + S; p_all per curtailed fleet-hour)")
    hdr = (f"  {'D':>5} {'H':>4} {'restart':>14} {'R s':>8} {'save':>14} {'S s':>8} {'o h':>10} {'K':>3} {'nmaxO':>5} "
           f"{'ETM p_all':>11} {'OWN p_all':>13} {'WALL p_all':>13} {'H0':>11} {'OWN/ETM':>12} {'below':>5} {'bind':>4} {'ver':>3} {'cf':>3}")
    for D in DS:
        for H in HS:
            print(hdr)
            sub = sorted((x for x in cells if x["D"] == D and x["H"] == H), key=lambda x: (x["c"]["o"], x["R"], x["rid"], x["sid"]))
            for x in sub:
                c = x["c"]
                A = c["arms"]
                ok_ver = A["ETM"]["verify"] and A["OWN"]["verify"]
                ok_cf = A["ETM"]["cf_ok"] and A["OWN"]["cf_ok"]
                print(f"  {d.g(D):>5} {d.g(H):>4} {x['rid']:>14} {float(x['R'] / SEC):>8g} {x['sid']:>14} {float(x['S'] / SEC):>8g} "
                      f"{float(c['o']):>10.6f} {c['K']:>3} {A['OWN']['nmax']:>5} {float(A['ETM']['pa'].x):>11.6f} {float(A['OWN']['pa'].x):>13.6f} "
                      f"{float(A['WALL']['pa'].x):>13.6f} {float(c['h0']):>11.6f} {float(c['ratio']):>12.6f} {d.yn(c['below']):>5} "
                      f"{d.yn(c['binds']):>4} {d.yn(ok_ver):>3} {d.yn(ok_cf):>3}")
    print("  (nmaxO: events OWN's wall-clock slack absorbs; bind: nmaxO < K, OWN's slack runs out within the season; ver: p_all verified by")
    print("   backward induction for ETM and OWN; cf: p_all equals the closed form for ETM and OWN)")
    print()

    # ---------------------------------------------------------------- per (D, H) ratio along the overhead axis
    print("THE RATIO ALONG THE OVERHEAD AXIS (one row per (D, H); distinct overheads o in increasing order)")
    print(f"  {'D':>5} {'H':>4} {'n_o':>4} {'o min h':>10} {'o max h':>10} {'ratio at o min':>15} {'ratio at o max':>15} {'ratio max':>12} "
          f"{'rises':>5} {'falls':>5} {'flats':>5} {'binds at o >=':>14} {'Q-a cells':>10} {'Q-b':>6} {'Q-b nonstrict':>13}")
    rows = {}
    for D in DS:
        for H in HS:
            sub = [x for x in cells if x["D"] == D and x["H"] == H]
            by_o = {}
            for x in sub:
                by_o.setdefault(x["c"]["o"], set()).add(x["c"]["ratio"])
            consistent = all(len(v) == 1 for v in by_o.values())
            seq = sorted((o, next(iter(v))) for o, v in by_o.items())
            rises, falls, flats, first, last = row_summary(seq)
            bind_os = [o for o, _ in seq if run_cell(D, H, o, ZERO)["binds"]]
            qa_n = sum(int(x["c"]["below"]) for x in sub)
            qb = consistent and rises == 0 and last < first
            qbn = consistent and rises == 0
            rows[(D, H)] = dict(seq=seq, rises=rises, falls=falls, flats=flats, first=first, last=last, qa_n=qa_n, n=len(sub), qb=qb, qbn=qbn,
                                bind_os=bind_os, consistent=consistent)
            bstr = f"{float(min(bind_os)):.6f}" if bind_os else "never"
            print(f"  {d.g(D):>5} {d.g(H):>4} {len(seq):>4} {float(seq[0][0]):>10.6f} {float(seq[-1][0]):>10.6f} {float(first):>15.6f} "
                  f"{float(last):>15.6f} {float(max(r for _, r in seq)):>12.6f} {rises:>5} {falls:>5} {flats:>5} {bstr:>14} "
                  f"{qa_n:>4}/{len(sub):<5} {('holds' if qb else 'fails'):>6} {('holds' if qbn else 'fails'):>13}")
    print("  (binds at o >=: the smallest overhead at which OWN's wall-clock slack absorbs fewer than K events; the ratio is 1 where it")
    print("   does not bind and 1 + W rate/((K - nmax) o) where it does; rises/falls/flats: neighbour pairs of distinct o; the same o from")
    print("   different (R, S) pairs gives the same ratio in every row: "
          f"{d.yn(all(r['consistent'] for r in rows.values()))})")
    # rises in detail
    print("  every rise of the ratio between neighbouring overheads:")
    nr = 0
    for (D, H), r in rows.items():
        for (o1, r1), (o2, r2) in zip(r["seq"], r["seq"][1:]):
            if r2 > r1:
                nr += 1
                n1 = run_cell(D, H, o1, ZERO)["arms"]["OWN"]["nmax"]
                n2 = run_cell(D, H, o2, ZERO)["arms"]["OWN"]["nmax"]
                print(f"    D {d.g(D)}, H {d.g(H)}: o {float(o1):.6f} -> {float(o2):.6f} h, ratio {float(r1):.6f} -> {float(r2):.6f} "
                      f"(OWN nmax {n1} -> {n2}, K 41)")
    if nr == 0:
        print("    none")
    print()

    # ---------------------------------------------------------------- sensitivity
    print("SENSITIVITY (printed, not scored)")
    lostv = vals.get("L-KOK-half")
    r_lo, r_hi = vals.get("R-KOK-u0lo"), vals.get("R-KOK-u0hi")
    if lostv and r_lo and r_hi:
        print(f"  (i) the pause without a save (Kokolis: lost work {fmt_s(lostv['h'])} per event instead of a save; restart u0 5 or 20 min;")
        print("      not a lossless pause, so ETM's contract is read with the lost work as overhead):")
        for D in DS:
            for H in HS:
                parts = []
                for R in (r_lo["h"], r_hi["h"]):
                    c = run_cell(D, H, R, ZERO, lost=lostv["h"], full=False)
                    A = c["arms"]
                    parts.append(f"R {fmt_s(R)}: o {float(c['o']):.6f} h, ETM {float(A['ETM']['pa'].x):.6f}, OWN {float(A['OWN']['pa'].x):.6f}, "
                                 f"ratio {float(c['ratio']):.6f}, below {d.yn(c['below'])}")
                print(f"      D {d.g(D)}, H {d.g(H)}: " + "; ".join(parts))
    o_all = sorted({x["c"]["o"] for x in cells})
    picks = [("o min", o_all[0]), ("Kokolis u0lo + wcp", (vals["R-KOK-u0lo"]["h"] + vals["S-KOK-wcp"]["h"]) if "R-KOK-u0lo" in vals and "S-KOK-wcp" in vals else None),
             ("o max", o_all[-1])]
    print("  (ii) offer spacing at D = 1100 (K changes with the spacing), three overheads:")
    for sp in SENS_SPACINGS:
        for H in HS:
            parts = []
            for lab, o in picks:
                if o is None:
                    continue
                c = run_cell(Fr(1100), H, o, ZERO, spacing=sp, full=False)
                A = c["arms"]
                parts.append(f"{lab} {float(o):.6f} h: K {c['K']}, nmaxO {A['OWN']['nmax']}, ETM {float(A['ETM']['pa'].x):.6f}, "
                             f"OWN {float(A['OWN']['pa'].x):.6f}, ratio {float(c['ratio']):.6f}")
            print(f"      spacing {d.g(sp)} h, H {d.g(H)}: " + "; ".join(parts))
    print()

    # ---------------------------------------------------------------- Q
    n_cells = len(cells)
    ok_kind = all(x["c"]["ok_kind"] for x in cells)
    qa_n = sum(int(x["c"]["below"]) for x in cells)
    na_n = sum(int(x["c"]["notabove"]) for x in cells)
    eq_n = sum(int(x["c"]["ok_kind"] and x["c"]["arms"]["ETM"]["pa"].x == x["c"]["arms"]["OWN"]["pa"].x) for x in cells)
    bind_n = sum(int(x["c"]["binds"]) for x in cells)
    below_bind = sum(int(x["c"]["below"] and x["c"]["binds"]) for x in cells)
    eq_nobind = sum(int((not x["c"]["below"]) and not x["c"]["binds"]) for x in cells)
    qb_n = sum(int(r["qb"]) for r in rows.values())
    qbn_n = sum(int(r["qbn"]) for r in rows.values())
    rises_tot = sum(r["rises"] for r in rows.values())
    ver_ok = all(x["c"]["arms"][a]["verify"] for x in cells for a in ("ETM", "OWN"))
    cf_ok = all(x["c"]["arms"][a]["cf_ok"] for x in cells for a in ("ETM", "OWN"))
    qa = qa_n == n_cells
    qb = qb_n == len(rows)
    if not all_found or not ok_kind:
        qv = "not computable"
    else:
        qv = "holds" if (qa and qb) else "fails"
    qvn = "not computable" if (not all_found or not ok_kind) else ("holds" if (na_n == n_cells and qbn_n == len(rows)) else "fails")
    ratios = [x["c"]["ratio"] for x in cells]
    print("Q")
    print(f"  inputs: every sourced quote found verbatim and parsed: {d.yn(all_found)}; every p_all a threshold: {d.yn(ok_kind)}")
    print(f"  internal checks: p_all verified by backward induction (at p_all and p_all - 1e-6) for ETM and OWN in every cell: {d.yn(ver_ok)}; "
          f"p_all equals the closed form in every cell: {d.yn(cf_ok)}")
    print(f"  Q-a (ETM's p_all strictly below OWN's): {qa_n} of {n_cells} cells -> {'holds' if qa else 'fails'}; equal in {eq_n}; "
          f"never above in {na_n} of {n_cells}")
    print(f"      OWN's slack binds (nmax < K) in {bind_n} of {n_cells} cells; strictly below in {below_bind} of those; "
          f"not strictly below where the slack does not bind: {eq_nobind} of {n_cells - bind_n}")
    print(f"  Q-b (the ratio OWN/ETM shrinks as the overhead grows, per (D, H)): {qb_n} of {len(rows)} rows -> {'holds' if qb else 'fails'}; "
          f"rises between neighbouring overheads {rises_tot}; non-strict reading (never rises) {qbn_n} of {len(rows)} rows")
    print(f"  ratio OWN/ETM over the scored grid: min {float(min(ratios)):.6f}, max {float(max(ratios)):.6f}")
    print(f"  Q (scored, strict readings): {qv}; non-strict readings (not scored): {qvn}")
    print(f"  the investigator's forecast (Q holds) is {'right' if qv == 'holds' else ('wrong' if qv == 'fails' else 'not decidable')}")
    print()

    # ---------------------------------------------------------------- gate
    stakes = [s for x in cells for s in x["c"]["arms"]["ETM"]["stakes"]]
    stakes_R = [s for x in cells for s in x["stakes_R"]]
    s_vals = sorted({x["S"] for x in cells})
    stakes_R0 = [s for x in cells if x["S"] == 0 for s in x["stakes_R"]]
    etm_states = sum(x["c"]["arms"]["ETM"]["n_states"] for x in cells)
    etm_eq = sum(x["c"]["arms"]["ETM"]["eq"] for x in cells)
    stakeR_is_S = all(s == RATE * x["S"] for x in cells for s in x["stakes_R"])
    gz = max(abs(s) for s in stakes) == 0 and etm_eq == etm_states
    print("GATE")
    print(f"  G-ZERO: max |ETM stake - rate (R + S)| over {len(stakes)} event counts in {n_cells} cells = {float(max(abs(s) for s in stakes)):g} (exact); "
          f"ETM's x* == rate (R + S)/H (closed) at {etm_eq} of {etm_states} offer states -> {'holds' if gz else 'FAILS'}")
    print(f"          (the stake minus rate R alone equals rate S in every cell and event count: {d.yn(stakeR_is_S)}; it ranges over "
          f"{float(min(stakes_R)):g}..{float(max(stakes_R)):g} h; with S = 0 ({len(stakes_R0)} event counts) its max |.| is "
          f"{float(max(abs(s) for s in stakes_R0)):g}; {len(s_vals)} save values)")
    outcomes = (("curtailed fleet-hours", "fleet_hours", +1), ("payments", "payments", +1), ("valuation", "valuation", +1),
                ("fleet value", "fleet_value", +1), ("deadline met", "met", +1), ("completion hour", "completion", -1))
    worst, n_cmp, ahead = [], 0, 0
    seen = set()
    for x in cells:
        c = x["c"]
        job = x["job"]
        pi = c["arms"]["ETM"]["pa"].x
        key = (x["D"], x["H"], c["o"])
        if key in seen:
            continue
        seen.add(key)
        offs = d.every(SPACING, x["H"], job.W)
        for label, of, made in (("K = 0", (), None), ("no offer made", offs, [False] * len(offs))):
            pe = d.play(job, d.ETM, of, pi, made=made)
            pw = d.play(job, d.WALL, of, pi, made=made)
            for name, fld, sgn in outcomes:
                a_, b_ = float(pe[fld]), float(pw[fld])
                r = d.rel(a_, b_)
                better = (a_ > b_) if sgn > 0 else (a_ < b_)
                n_cmp += 1
                if better and r > 1e-2:
                    ahead += 1
                worst.append((r, name))
    wr = max(worst, key=lambda t: t[0])
    gn = ahead == 0
    print(f"  G-NEG: no events offered (K = 0, and the no-offer realisation), {len(seen)} distinct (D, H, o) worlds x 2, {n_cmp} comparisons of ETM "
          f"against WALL on six outcomes; ETM ahead by more than 1 % in {ahead}; largest rel {wr[0]:.3e} ({wr[1]}) -> {'holds' if gn else 'FAILS'}")
    print()
    print("CHANGES AFTER THE FIRST RUN (bug fixes only; no prediction, arm, threshold, grid or reading changed)")
    print("  1. The printed diagnostic 'stake minus rate R alone' (beside G-ZERO) was read from a cell cache keyed on the overhead o = R + S,")
    print("     so it used the R of the first (R, S) pair with that o; it is now computed per cell from the cell's own job. G-NEG likewise")
    print("     now uses the cell's own job (no number changes: only o enters the arms). G-ZERO and Q never read the diagnostic.")
    print()
    print(f"RESULT H4: Q {qv}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - rate (R + S)| = {float(max(abs(s) for s in stakes)):g} over "
          f"{len(stakes)} event counts in {n_cells} cells; ETM x* = (R + S)/H at {etm_eq} of {etm_states} offer states); "
          f"G-NEG {'holds' if gn else 'FAILS'} (ETM ahead of WALL by more than 1 % in {ahead} of {n_cmp} no-event comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
