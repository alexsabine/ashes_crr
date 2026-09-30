"""POST HOC (critic follow-up 4; not declared)

DR1 follow-up 4 to check DATA: the ASSUMED inputs behind part (b) (G7: ETM's revenue below 1 % of the fleet's compute cost
in an ordinary season) replaced one at a time, and then together, by SOURCED values, with the break-even compute cost C, PUE
and USD/GBP rate printed for each season. An unscored re-reading; dr_data.py and dr_data.txt are not edited (dr_data.py is
imported unchanged).

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 3. Nothing in this
file was declared. It was written after DR1's first run and after the DR1 verification (Grid_Demand_Response/checks/
verification.md, DATA, skeptics 2 and 3). They found that part (b) rests on ASSUMED inputs with margins of about 1 %: W2023/24
sits at 0.98842 % against the 1 % bound; PUE = 1 is ASSUMED; USD/GBP = 1.35 is ASSUMED; one 2026-04-18 H100 index price
[IDX-NEO] is applied to every season from 2022 on (anachronistic); and the phrase 'below 1 % only within about 11 %'
misstates the margin.

What this does. dr_data.py's records, events (price 'mean', C1), fleet, jobs, R, the ETM arm, the online rule and C5 (the
ordinary seasons: every season except W2022/23) are reused unchanged. Only the compute cost C (GBP per MWh) changes:
    C = (H100 price, USD per GPU-hour) x 8 GPUs / (10.2 kW / 1000) / (USD per GBP) / PUE        [DGX; dr_data's formula]
With PUE = 1 and USD/GBP = 1.35 this is dr_data.compute_cost_mwh exactly (checked at run time). PUE enters as a division:
a 100 MW grid-metered fleet holds 100/PUE MW of IT load, so its compute cost per grid MWh is C/PUE (ASSUMED: the facility
overhead falls in proportion when the IT load pauses, so a curtailed job sheds its overhead too). ETM's entry price C R/H
moves with C, so every row is a full rerun of the online rule (dd.simulate), not a rescaling.

Inputs (each quote checked whitespace-normalised against docs/citations/dr1_followup4_2026-09-29.md at run time; the number
parsed out of the quote): PUE from Google's environmental reports and data-centre page (Google's fleet and, as Google quotes
it, the Uptime Institute survey average; Uptime's own survey report was NOT REACHED); USD/GBP from the Bank of England daily
series XUDLUSS (every daily value between each season's first and last event day, quoted in the dossier); H100 rental prices
nearer each season from Silicon Data (blog posts and index page), IEEE Spectrum's report of the Silicon Data index, and Bandi
& Su arXiv:2607.12156 v3 (via dr_data's own source [IDX-NEO]). Every verdict word printed is computed from the numbers (R15).
An application calculation on public data: no ledger row; a note, not evidence (R8). Deterministic; stdlib only (via drlib
and dr_data).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/followup_4.py > Grid_Demand_Response/checks/followup_4.txt
"""
from __future__ import annotations

import datetime as dt
import hashlib
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402
import dr_data as dd  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CIT = REPO / "docs" / "citations"
FU = "dr1_followup4_2026-09-29.md"
TEXT = (CIT / FU).read_text(encoding="utf-8")
PINNED = (HERE / "dr_data.txt").read_text(encoding="utf-8")
ZERO, ONE = Fr(0), Fr(1)
BUG_FIXES: list[str] = []      # bug fixes after this script's first run (none so far)
WINDOW = Fr(4)                 # CHOICE: the break-even scan covers C in [C0 / 4, 4 C0] (C0 the scored C)
EPS = Fr(1, 10**6)             # CHOICE: the verification step just above the break-even C (relative)
CRITIC = dict(dC=Fr("0.0117"), pue_w=Fr("1.012"), pue_s=Fr("1.043"), phrase=Fr("0.11"))   # the critic's figures (task text)


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def f(x, d=6) -> str:
    return dd.f(x, d)


def pct(x, d=5) -> str:
    return dd.pct(x, d)


def D(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


# ============================================================================================ sourced quotes
# (id, citation, verbatim quote as in the dossier (whitespace-normalised match))
QUOTES = [
    ("PUE-G2022", "Google 2023 Environmental Report",
     "In 2022, the average annual power usage effectiveness (PUE) 76 for our global fleet of data centers was 1.10, compared "
     "with the industry average of 1.55"),
    ("PUE-U2022", "Google 2023 Environmental Report, endnote 77",
     "According to the Uptime Institute’s 2022 Global Data Center Survey, the global average PUE of respondents’ data "
     "centers was around 1.55."),
    ("PUE-G2023", "Google 2024 Environmental Report",
     "In 2023, the average annual power usage effectiveness for our data centers was 1.10 compared with the industry average "
     "of 1.58,"),
    ("PUE-U2023", "Google 2024 Environmental Report, endnote",
     "According to the Uptime Institute’s 2023 Global Data Center Survey, the global average PUE of respondents’ data "
     "centers was around 1.58."),
    ("PUE-G2024", "Google 2025 Environmental Report",
     "In 2024, the average annual PUE for our global fleet of data centers was 1.09, compared with the industry average of "
     "1.56,"),
    ("PUE-U2024", "Google 2025 Environmental Report, endnote",
     "According to the Uptime Institute’s 2024 Global Data Center Survey, the global average PUE of respondents’ data "
     "centers was 1.56."),
    ("PUE-G2025", "Google data centers, Power usage effectiveness page (fetched 2026-09-30)",
     "In 2025, the average annual power usage effectiveness for our global fleet of data centers was 1.09."),
    ("PUE-U2025", "Google data centers, Power usage effectiveness page, footnote 1",
     "According to the Uptime Institute’s 2025 Global Data Center Survey, the global average PUE of respondents’ data "
     "centers was 1.54."),
    ("BOE-SERIES", "Bank of England Database, series XUDLUSS (CSV with titles)",
     "XUDLUSS,Spot exchange rate - US $ into Sterling"),
    ("SD-TL-HEAD", "Silicon Data blog, H100 Rental Price Over Time (2023–2025) (Dec 21, 2025), table header",
     "H100 Rental Price Over Time (Per GPU-Hour) Period Hyperscaler Marketplace Neocloud Data-driven context"),
    ("SD-TL-2023", "Silicon Data blog, H100 Rental Price Over Time, table",
     "2023-08 to 2023-12 $7.62–$7.77 (med $7.76) Only Hyperscaler is present, prices are tightly clustered around ~$7.7"),
    ("SD-TL-2024A", "Silicon Data blog, H100 Rental Price Over Time, table",
     "2024-01 to 2024-05 $7.37–$8.24 (med $7.92) Still Hyperscaler-only"),
    ("IEEE-LAUNCH", "IEEE Spectrum, Price Index Could Clarify Opaque GPU Costs for AI (Moore, 28 May 2025)",
     "She founded the startup Silicon Data to create a solution: the first worldwide rental price index for a GPU. That "
     "rental price index, called the SDH100RT, launched today."),
    ("IEEE-0527", "IEEE Spectrum (Moore, 28 May 2025)",
     "Average hourly rental prices for an Nvidia H100 GPU were US $2.37 on 27 May 2025."),
    ("IEEE-WINTER", "IEEE Spectrum (Moore, 28 May 2025)",
     "On DeepSeek’s debut, the H100 price went up mildly to $2.50 per hour, but that was still in the $2.40 per hour to "
     "$2.60 per hour range from the months before. It then slid to $2.30 per hour for much of February before it started "
     "climbing again."),
    ("SD-SEP25-T", "Silicon Data blog, H100 Rental Market Cools in September (Oct 20, 2025)",
     "the Silicon Data H100 Rental Index (Bloomberg Ticker: SDH100RT) moved within a narrow range."),
    ("SD-SEP25-A", "Silicon Data blog (Oct 20, 2025)",
     "In August, the H100 Rental Index held steady, fluctuating modestly between 2.22 and 2.26,"),
    ("SD-SEP25-S", "Silicon Data blog (Oct 20, 2025)",
     "By mid-September, the index dipped as low as 2.13, before staging a mild recovery toward 2.16 as the month closed."),
    ("SD-SPIKE", "Silicon Data blog, H100 Price Spike (Jan 9, 2026)",
     "Our GPU Rental Index revealed a startling 10% price jump for H100 rentals between December 9, 2025 and January 6, "
     "2026. Hourly rates climbed from $2.00 to $2.20 in just four weeks."),
    ("SD-MAY26-A", "Silicon Data blog, H100 index April-May 2026",
     "The Neocloud index opened April at $2.63, fell to a $2.47 trough by April 8 — about 6% in a week — then recovered "
     "most of the way back, closing April at $2.59."),
    ("SD-MAY26-M", "Silicon Data blog, H100 index April-May 2026",
     "The index opened at $2.55 and rose in steps to $2.73 by May 31, peaking at $2.76 on May 30"),
    ("SD-MAY26-T", "Silicon Data blog, H100 index April-May 2026",
     "The Neocloud index is the one Silicon Data distributes on Bloomberg, under the ticker SDH100RT; it stood at $2.75 in "
     "early June,"),
    ("SD-MJ26-A", "Silicon Data blog, H200 vs H100 Rental Prices, May to July 2026",
     "The H100 Neo-Cloud rate rose too, but half as much and all of it early: $2.57 on May 4, $2.73 by the end of May, and "
     "$2.75 on July 27 after a June round trip."),
    ("SD-MJ26-B", "Silicon Data blog, H200 vs H100 Rental Prices, May to July 2026",
     "The H100 ran to its series high of $2.79 on June 5 just as the H200 was chopping lower,"),
    ("SD-MJ26-C", "Silicon Data blog, H200 vs H100 Rental Prices, May to July 2026",
     "The H100 faded through late June to $2.59 while the H200 recovered,"),
    ("SD-IDX-HEAD", "Silicon Data H100 Rental Price Index page (fetched 2026-09-30), header",
     "The Neo-Cloud index is published daily as ticker SDH100RT. Getting Started Talk to sales Neo-Cloud Hyperscaler As of "
     "Sep 29, 2026 2.73 USD / GPU-hour"),
    ("SD-IDX-FAQ", "Silicon Data H100 Rental Price Index page (fetched 2026-09-30), FAQ",
     "The current H100 rental price is $2.53 per GPU-hour, based on the Silicon Data H100 Rental Price Index (Neo-Cloud "
     "ticker SDH100RT)."),
]

# PUE: (quote id, source, year, regex giving the value)
PUE_SRC = [
    ("PUE-G2022", "Google", 2022, r"was ([\d.]+), compared"), ("PUE-U2022", "Uptime", 2022, r"was around ([\d.]+)\.$"),
    ("PUE-G2023", "Google", 2023, r"was ([\d.]+) compared"), ("PUE-U2023", "Uptime", 2023, r"was around ([\d.]+)\.$"),
    ("PUE-G2024", "Google", 2024, r"was ([\d.]+), compared"), ("PUE-U2024", "Uptime", 2024, r"was ([\d.]+)\.$"),
    ("PUE-G2025", "Google", 2025, r"was ([\d.]+)\.$"), ("PUE-U2025", "Uptime", 2025, r"was ([\d.]+)\.$"),
]

# H100 index points: (quote id, regex over the quote, group, dated interval (CHOICE: the investigator's reading of the quote's
# words as dates), segment). NEO = the Silicon Data neo-cloud index SDH100RT (the scored [IDX-NEO] series); HS = hyperscaler.
H100_PTS = [
    ("SD-TL-2023", r"^2023-08 to 2023-12 \$([\d.]+)–\$([\d.]+)", 1, "2023-08-01", "2023-12-31", "HS"),
    ("SD-TL-2023", r"^2023-08 to 2023-12 \$([\d.]+)–\$([\d.]+)", 2, "2023-08-01", "2023-12-31", "HS"),
    ("SD-TL-2024A", r"^2024-01 to 2024-05 \$([\d.]+)–\$([\d.]+)", 1, "2024-01-01", "2024-05-31", "HS"),
    ("SD-TL-2024A", r"^2024-01 to 2024-05 \$([\d.]+)–\$([\d.]+)", 2, "2024-01-01", "2024-05-31", "HS"),
    ("IEEE-WINTER", r"in the \$([\d.]+) per hour to \$([\d.]+) per hour range from the months before", 1, "2024-10-01", "2025-01-19", "NEO"),
    ("IEEE-WINTER", r"in the \$([\d.]+) per hour to \$([\d.]+) per hour range from the months before", 2, "2024-10-01", "2025-01-19", "NEO"),
    ("IEEE-WINTER", r"went up mildly to \$([\d.]+) per hour", 1, "2025-01-20", "2025-01-31", "NEO"),
    ("IEEE-WINTER", r"slid to \$([\d.]+) per hour for much of February", 1, "2025-02-01", "2025-02-28", "NEO"),
    ("IEEE-0527", r"US \$([\d.]+) on 27 May 2025", 1, "2025-05-27", "2025-05-27", "NEO"),
    ("SD-SEP25-A", r"between ([\d.]+) and ([\d.]+),", 1, "2025-08-01", "2025-08-31", "NEO"),
    ("SD-SEP25-A", r"between ([\d.]+) and ([\d.]+),", 2, "2025-08-01", "2025-08-31", "NEO"),
    ("SD-SEP25-S", r"as low as ([\d.]+), .*toward ([\d.]+) as", 1, "2025-09-01", "2025-09-30", "NEO"),
    ("SD-SEP25-S", r"as low as ([\d.]+), .*toward ([\d.]+) as", 2, "2025-09-01", "2025-09-30", "NEO"),
    ("SD-SPIKE", r"from \$([\d.]+) to \$([\d.]+) in", 1, "2025-12-09", "2025-12-09", "NEO"),
    ("SD-SPIKE", r"from \$([\d.]+) to \$([\d.]+) in", 2, "2026-01-06", "2026-01-06", "NEO"),
    ("IDX-NEO", None, None, "2026-04-18", "2026-04-18", "NEO"),        # dr_data's own source (Bandi & Su v3, Table 1)
    ("SD-MAY26-A", r"opened April at \$([\d.]+)", 1, "2026-04-01", "2026-04-01", "NEO"),
    ("SD-MAY26-A", r"a \$([\d.]+) trough by April 8", 1, "2026-04-08", "2026-04-08", "NEO"),
    ("SD-MAY26-A", r"closing April at \$([\d.]+)\.", 1, "2026-04-30", "2026-04-30", "NEO"),
    ("SD-MAY26-M", r"opened at \$([\d.]+)", 1, "2026-05-01", "2026-05-01", "NEO"),
    ("SD-MAY26-M", r"to \$([\d.]+) by May 31", 1, "2026-05-31", "2026-05-31", "NEO"),
    ("SD-MAY26-M", r"peaking at \$([\d.]+) on May 30", 1, "2026-05-30", "2026-05-30", "NEO"),
    ("SD-MAY26-T", r"stood at \$([\d.]+) in early June", 1, "2026-06-01", "2026-06-10", "NEO"),
    ("SD-MJ26-A", r"\$([\d.]+) on May 4", 1, "2026-05-04", "2026-05-04", "NEO"),
    ("SD-MJ26-A", r"\$([\d.]+) on July 27", 1, "2026-07-27", "2026-07-27", "NEO"),
    ("SD-MJ26-B", r"series high of \$([\d.]+) on June 5", 1, "2026-06-05", "2026-06-05", "NEO"),
    ("SD-MJ26-C", r"late June to \$([\d.]+) while", 1, "2026-06-20", "2026-06-30", "NEO"),
    ("SD-IDX-HEAD", r"As of Sep 29, 2026 ([\d.]+) USD / GPU-hour", 1, "2026-09-29", "2026-09-29", "NEO"),
    ("SD-IDX-FAQ", r"is \$([\d.]+) per GPU-hour", 1, "2026-09-29", "2026-09-29", "NEO"),
]

BOE_ROW = re.compile(r"(\d{2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4}),(\d+(?:\.\d+)?)")
MONTHS = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def boe_rows() -> dict:
    """The daily XUDLUSS values quoted in the dossier's section 'Bank of England XUDLUSS daily values' (blockquotes)."""
    sec = TEXT.split("<!-- BOE-DATA-BEGIN -->")[1].split("<!-- BOE-DATA-END -->")[0]
    out = {}
    for line in sec.splitlines():
        if not line.startswith("> "):
            continue
        for m in BOE_ROW.finditer(line):
            d = dt.date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))
            if d in out:
                raise ValueError(f"duplicate BoE date {d}")
            out[d] = dl.q(m.group(4))
    return out


def cost(vals: dict, gpu_h: Fr, fx: Fr, pue: Fr) -> Fr:
    gpus, kw = vals["DGX"]["gpus"], vals["DGX"]["kw"]
    return gpu_h * gpus / (kw / 1000) / fx / pue


def main() -> int:
    print("POST HOC (critic follow-up 4; not declared)")
    print()
    print("DR1 follow-up 4 to check DATA: part (b) (G7) with its ASSUMED PUE, USD/GBP and H100 price replaced by SOURCED values;")
    print("the break-even compute cost C, PUE and USD/GBP per season.")
    print(f"Binding declaration Grid_Demand_Response/DECLARATION.md (declared at {dl.DECL_AT}; not edited). dr_data.py and "
          "dr_data.txt are not edited:")
    print("dr_data.py is imported unchanged. An application calculation on public data: no ledger row; a note, not evidence (R8).")
    print()

    # ------------------------------------------------------------------------------------------------ data and sources
    man = dd.manifest()
    bad = [n for n in sorted(man) if hashlib.sha256((dd.RAW / n).read_bytes()).hexdigest() != man[n]]
    print(f"DATA: {len(man)} raw files; sha256 matches Grid_Demand_Response/data/MANIFEST.md for {len(man) - len(bad)} of {len(man)}")
    if bad or not man:
        print("RESULT FOLLOW-UP 4: not computable (raw files differ from the manifest)")
        return 0
    vals, rep = dd.load_sources()
    miss = [r[0] for r in rep if not (r[4] and r[5])]
    print(f"dr_data.py's own sources (dr_data.load_sources, unchanged): {len(rep) - len(miss)} of {len(rep)} found; used here: "
          f"[IDX-NEO] H100 neo-cloud index {dl.g(vals['IDX-NEO']['gpu_h'])} USD/GPU-hour on 2026-04-18, [DGX] "
          f"{dl.g(vals['DGX']['gpus'])} GPUs, {dl.g(vals['DGX']['kw'])} kW")
    print()
    print(f"SOURCED QUOTES (each checked verbatim, whitespace-normalised, at run time against docs/citations/{FU})")
    qtext, qmiss = {}, []
    for qid, cite, quote in QUOTES:
        ok = ws(quote) in ws(TEXT)
        qmiss += [] if ok else [qid]
        qtext[qid] = quote
        print(f"  [{qid}] {cite}: found {dl.yn(ok)}")
        print(f"      '{quote}'")
    boe = boe_rows()
    print(f"  [BOE-DATA] Bank of England XUDLUSS daily values quoted in the dossier (section 3): {len(boe)} days, "
          f"{min(boe) if boe else '-'} .. {max(boe) if boe else '-'}")
    if miss or qmiss or not boe:
        print(f"RESULT FOLLOW-UP 4: not computable (sourced input not found: {', '.join(miss + qmiss) or 'BoE data'})")
        return 0
    print()

    # ------------------------------------------------------------------------------------------------ the scored setting
    bidir = dt.date(int(vals["DFS-BIDIR"]["year"]), 4, int(vals["DFS-BIDIR"]["day"]))
    sps, _ = dd.load_sps(bidir)
    evs, _ = dd.build_events(sps, "mean")
    GPU0, FX0, PUE0 = vals["IDX-NEO"]["gpu_h"], dd.FX, ONE
    C0 = dd.compute_cost_mwh(vals, dd.PRIMARY_PRICE, dd.FX)
    same_formula = cost(vals, GPU0, FX0, PUE0) == C0
    jobs = [dl.Job(dd.W, dd.W + dd.SLACK_STEP * i, dd.R, name=f"J{i:03d}") for i in range(1, dd.N_JOBS + 1)]
    seas = [s for s in sorted({r["season"] for r in sps}, key=lambda s: (s[1:5], s[0] == "W")) if s in evs]
    ordinary = [s for s in seas if s != dd.SCARCITY]
    per = {}
    for s in seas:
        e = evs[s]
        per[s] = dict(st=Fr((e[0]["date"] - dd.EPOCH).days * 24), en=Fr((e[-1]["date"] - dd.EPOCH).days * 24 + 24),
                      d0=e[0]["date"], d1=e[-1]["date"])
        per[s]["K"] = dd.G7_BOUND * dd.FLEET_MW * (per[s]["en"] - per[s]["st"])     # share >= 1 % iff revenue / K >= C
    memo: dict = {}

    def run(s: str, C: Fr) -> dict:
        k = (s, C)
        if k not in memo:
            p = per[s]
            t = dd.simulate(evs[s], p["st"], p["en"], dl.ETM, jobs, C)
            memo[k] = dict(rev=t["revenue"], all100=t["events_all"], n=len(evs[s]),
                           share=t["revenue"] / (dd.FLEET_MW * (p["en"] - p["st"]) * C))
        return memo[k]

    print(f"SCORED SETTING (dr_data.py, unchanged): price 'mean' (C1); C0 = {f(C0, 4)} GBP per MWh of compute = "
          f"{dl.g(GPU0)} USD/GPU-hour [IDX-NEO] x {dl.g(vals['DGX']['gpus'])} / {dl.g(vals['DGX']['kw'])} kW / {dl.g(FX0)} USD per GBP "
          f"(ASSUMED) / PUE {dl.g(PUE0)} (ASSUMED); this script's formula reproduces dr_data.compute_cost_mwh exactly: "
          f"{dl.yn(same_formula)}")
    print(f"  R = {dl.g(dd.R)} h (ASSUMED); fleet {dl.g(dd.FLEET_MW)} MW (ASSUMED); the ETM arm; ordinary seasons (C5 as scored): "
          f"{', '.join(ordinary)}")
    print("  ASSUMED (this follow-up): a PUE above 1 scales the fleet's compute cost per grid MWh by 1/PUE and the facility overhead")
    print("  falls in proportion while a job is paused (the curtailed grid MW stays 1 MW per job)")
    rep_ok = 0
    for s in seas:
        m = re.search(rf"^  {re.escape(s)}\s+ETM joined with all 100 jobs (\d+) of (\d+) events .*?ETM revenue share ([\d.]+ %)",
                      PINNED, re.M)
        r0 = run(s, C0)
        same = m is not None and m.group(3) == pct(r0["share"], 5) and int(m.group(1)) == r0["all100"]
        rep_ok += int(same)
        print(f"  {s:9} period {per[s]['d0']}..{per[s]['d1']}; here ETM all-100 {r0['all100']} of {r0['n']}, share "
              f"{pct(r0['share'], 5)}; pinned {m.group(3) if m else '-'} -> same: {dl.yn(same)}")
    print(f"  reproduced in {rep_ok} of {len(seas)} seasons")
    if rep_ok != len(seas) or not same_formula:
        print("RESULT FOLLOW-UP 4: not computable (the pinned run is not reproduced)")
        return 0
    print()

    # ------------------------------------------------------------------------------------------------ break-even scan
    print(f"BREAK-EVEN (scored setting): per season, ETM's revenue is piecewise constant in C (the online rule changes a decision")
    print("only where an event's payment equals its charge, C = price x H / R); the share = revenue / (100 MW x period hours x C).")
    print(f"Every such breakpoint in [C0/{dl.g(WINDOW)}, {dl.g(WINDOW)} C0] and one point inside every piece between them is run;")
    print("C_flip = the largest C in the window at which the share is at least 1 % (the share is below 1 % iff C > C_flip when")
    print("the share crosses 1 % once). Equivalent break-evens at the other inputs fixed at the scored values: PUE_flip = C0 /")
    print("C_flip (below 1 % iff PUE < PUE_flip), FX_flip = 1.35 C0 / C_flip USD per GBP (below 1 % iff USD/GBP < FX_flip),")
    print("H100_flip = 2.50 C_flip / C0 USD per GPU-hour (below 1 % iff the H100 price > H100_flip).")
    lo_w, hi_w = C0 / WINDOW, C0 * WINDOW
    m0 = dl.Model(jobs[0], dl.ETM)
    flip = {}
    for s in seas:
        K = per[s]["K"]
        bps = set()
        for e in evs[s]:
            he = m0.heff(e["H"])
            c = m0.charge(1, he) - m0.charge(0, ZERO)
            b = e["price"] * m0.e1 * he / c
            if lo_w < b < hi_w:
                bps.add(b)
        grid = [lo_w] + sorted(bps) + [hi_w]
        pts = []                                   # (C, kind, T = revenue / K); kind 'p' a point, 'i' a piece (lo, hi)
        for i, c in enumerate(grid):
            pts.append((c, "p", run(s, c)["rev"] / K, None))
            if i + 1 < len(grid):
                mid = (c + grid[i + 1]) / 2
                pts.append((mid, "i", run(s, mid)["rev"] / K, (c, grid[i + 1])))
        cand, status = [], []
        for c, kind, T, iv in pts:
            if kind == "p":
                good = T >= c
                status.append(good)
                if good:
                    cand.append(c)
            else:
                a, b = iv
                if T >= b:
                    status.append(True)
                    cand.append(b)
                elif T > a:
                    status += [True, False]
                    cand.append(T)
                else:
                    status.append(False)
        up = sum(int((not status[i]) and status[i + 1]) for i in range(len(status) - 1))
        down = sum(int(status[i] and not status[i + 1]) for i in range(len(status) - 1))
        revs = [run(s, c)["rev"] for c, _, _, _ in pts]
        nonmono = sum(int(revs[i + 1] > revs[i]) for i in range(len(revs) - 1))
        cf = max(cand) if cand else None
        at_edge = cf is not None and (cf == hi_w or cf == lo_w)
        v_at = run(s, cf)["share"] if cf is not None else None
        v_up = run(s, cf * (1 + EPS))["share"] if cf is not None else None
        ok = (cf is not None and not at_edge and v_at >= dd.G7_BOUND and v_up < dd.G7_BOUND and up == 0 and down == 1)
        flip[s] = dict(cf=cf, ok=ok, up=up, down=down, nonmono=nonmono, n_bp=len(bps), v_at=v_at, v_up=v_up)
        tag = "" if s in ordinary else "  (W2022/23: not an ordinary season under C5; above the bound at C0)"
        print(f"  {s:9} breakpoints in window {len(bps):>3}; runs {len(pts):>3}; revenue rises with C at {nonmono} step(s); the share "
              f"crosses 1 % downward {down} time(s), upward {up} -> single crossing: {dl.yn(up == 0 and down == 1)}{tag}")
        if cf is None or at_edge:
            print(f"            C_flip not in the window (candidate {f(cf, 4) if cf is not None else '-'}): not computable here")
            continue
        print(f"            C_flip {f(cf, 4)} GBP/MWh (exact {cf}); share at C_flip {pct(v_at, 6)}, at C_flip x (1 + 1e-6) "
              f"{pct(v_up, 6)} -> verified: {dl.yn(ok)}")
        print(f"            C_flip / C0 - 1 = {pct(cf / C0 - 1, 4)}; PUE_flip {f(C0 / cf, 5)}; FX_flip {f(FX0 * C0 / cf, 5)} USD per "
              f"GBP; H100_flip {f(GPU0 * cf / C0, 4)} USD/GPU-hour")
    print()
    w, sm = flip.get("W2023/24"), flip.get("S2026")
    if w and sm and w["ok"] and sm["ok"]:
        fall_w, fall_s = 1 - w["cf"] / C0, 1 - sm["cf"] / C0
        pw, ps = C0 / w["cf"], C0 / sm["cf"]
        print("THE CRITIC'S FIGURES (task text) against the break-evens:")
        print(f"  'a 1.17 % fall in C crosses it' (W2023/24): fall to C_flip {pct(fall_w, 4)} -> rounds to 1.17 %: "
              f"{dl.yn(round(fall_w * 10000) == round(CRITIC['dC'] * 10000))}")
        print(f"  'a PUE of 1.012 or more flips W2023/24': PUE_flip {f(pw, 5)} -> 1.012 flips it: {dl.yn(CRITIC['pue_w'] >= pw)}; "
              f"1.011 flips it: {dl.yn(Fr('1.011') >= pw)}")
        print(f"  '1.043 flips S2026': PUE_flip {f(ps, 5)} -> 1.043 flips it: {dl.yn(CRITIC['pue_s'] >= ps)}; 1.042 flips it: "
              f"{dl.yn(Fr('1.042') >= ps)}")
        lg = re.search(r"largest ETM share over these cells per ordinary season: (.*)$", PINNED, re.M)
        shares = {k: dl.q(v) / 100 for k, v in re.findall(r"(\S+) ([\d.]+) % \(below 1 %", lg.group(1))} if lg else {}
        top = max(shares.items(), key=lambda kv: kv[1]) if shares else None
        if top:
            over = top[1] / dd.G7_BOUND - 1
            print(f"  the phrase 'below 1 % only within about 11 %': the largest pinned SENSITIVITY-1 share is {top[0]} "
                  f"{pct(top[1], 4)}, which is {pct(over, 2)} ABOVE the bound (an overshoot in the worst cell, not a margin); the")
            print(f"    margins to the bound at the scored inputs are a {pct(fall_w, 2)} fall in C (W2023/24) and {pct(fall_s, 2)} "
                  f"(S2026) -> the phrase's 11 % is within 1 point of either margin: "
                  f"{dl.yn(abs(CRITIC['phrase'] - fall_w) <= Fr(1, 100) or abs(CRITIC['phrase'] - fall_s) <= Fr(1, 100))}")
    print()

    # ------------------------------------------------------------------------------------------------ the sourced inputs
    pue = {}
    for qid, src, yr, rx in PUE_SRC:
        m = re.search(rx, ws(qtext[qid]))
        pue[(src, yr)] = dl.q(m.group(1))
    print("SOURCED PUE (annual fleet averages; Uptime's values as Google quotes them; Uptime's own survey report was NOT REACHED):")
    for src in ("Google", "Uptime"):
        print(f"  {src:6} " + "; ".join(f"{yr} {dl.g(pue[(src, yr)])}" for yr in sorted({y for s_, y in pue if s_ == src})))
    last_year = max(y for _, y in pue)

    def pue_year(s: str) -> int:
        """CHOICE: the calendar year holding most of the season's period (ties: the later year); years after the latest
        published annual value use the latest (2026 -> 2025)."""
        d0, d1 = per[s]["d0"], per[s]["d1"]
        days = {}
        d = d0
        while d <= d1:
            days[d.year] = days.get(d.year, 0) + 1
            d += dt.timedelta(days=1)
        yr = max(days, key=lambda y: (days[y], y))
        return min(yr, last_year)

    print(f"  CHOICE: a season takes the PUE of the calendar year holding most of its period; years after {last_year} take {last_year}: "
          + "; ".join(f"{s} -> {pue_year(s)}" for s in seas))
    print()
    print("SOURCED USD/GBP (Bank of England XUDLUSS, daily spot; every quoted day from the season's first to its last event day):")
    fx = {}
    for s in seas:
        xs = [v for d, v in boe.items() if per[s]["d0"] <= d <= per[s]["d1"]]
        fx[s] = dict(n=len(xs), mean=sum(xs, ZERO) / len(xs), lo=min(xs), hi=max(xs))
        print(f"  {s:9} days {fx[s]['n']:>3}; mean {f(fx[s]['mean'], 5)}; min {dl.g(fx[s]['lo'])}; max {dl.g(fx[s]['hi'])} "
              f"(ASSUMED in dr_data: {dl.g(FX0)}; mean below it: {dl.yn(fx[s]['mean'] < FX0)})")
    print("  (ECB reference rates were fetched as well and are not used; the Bank of England series is sterling's own central bank's)")
    print()
    print("SOURCED H100 PRICES NEARER EACH SEASON (USD per GPU-hour). CHOICE: a quoted value counts for a season when its dated")
    print("interval (the investigator's reading of the quote's words, printed) overlaps the season's period; the neo-cloud index")
    print("SDH100RT (the scored [IDX-NEO] series) where any value exists, else the hyperscaler (HS) segment, flagged as not")
    print("like-for-like; else NOT FOUND. Low and high = the smallest and largest counted value.")
    pts_all = []
    for qid, rx, grp, a, b, seg in H100_PTS:
        if qid == "IDX-NEO":
            v = vals["IDX-NEO"]["gpu_h"]
        else:
            m = re.search(rx, ws(qtext[qid]))
            v = dl.q(m.group(grp))
        pts_all.append(dict(qid=qid, v=v, a=D(a), b=D(b), seg=seg))
    h100 = {}
    for s in seas:
        ins = [p for p in pts_all if p["a"] <= per[s]["d1"] and p["b"] >= per[s]["d0"]]
        neo = [p for p in ins if p["seg"] == "NEO"]
        hs = [p for p in ins if p["seg"] == "HS"]
        use, seg = (neo, "NEO") if neo else ((hs, "HS") if hs else ([], None))
        if not use:
            h100[s] = None
            print(f"  {s:9} NOT FOUND in the fetched sources (earliest counted interval starts {min(p['a'] for p in pts_all)}; the "
                  f"season's period ends {per[s]['d1']})")
            continue
        lo, hi = min(p["v"] for p in use), max(p["v"] for p in use)
        h100[s] = dict(lo=lo, hi=hi, seg=seg)
        print(f"  {s:9} segment {seg}{' (NOT like-for-like with IDX-NEO)' if seg == 'HS' else ''}; values {len(use)}: "
              + ", ".join(f"{dl.g(p['v'])} [{p['qid']} {p['a']}..{p['b']}]" for p in use)
              + f" -> low {dl.g(lo)}, high {dl.g(hi)} (scored {dl.g(GPU0)} dated 2026-04-18)")
    idx_head = [p["v"] for p in pts_all if p["qid"] == "SD-IDX-HEAD"][0]
    idx_faq = [p["v"] for p in pts_all if p["qid"] == "SD-IDX-FAQ"][0]
    print(f"  note: the index page's header ({dl.g(idx_head)}, as of 2026-09-29) and its FAQ ({dl.g(idx_faq)}, 'current') disagree; "
          "both are counted for S2026")
    print()

    # ------------------------------------------------------------------------------------------------ sensitivity rows
    rows = []
    for key in sorted(set(pue.values())):
        srcs = ", ".join(f"{s_} {y}" for (s_, y), v in sorted(pue.items()) if v == key)
        rows.append((f"PUE {dl.g(key)}", f"PUE {dl.g(key)} ({srcs}) in every season; H100 {dl.g(GPU0)}, fx {dl.g(FX0)}",
                     {s: (GPU0, FX0, key) for s in seas}))
    for src in ("Google", "Uptime"):
        rows.append((f"PUE {src} yr", f"PUE {src} of the season's year; H100 {dl.g(GPU0)}, fx {dl.g(FX0)}",
                     {s: (GPU0, FX0, pue[(src, pue_year(s))]) for s in seas}))
    for k, lab in (("mean", "mean"), ("lo", "min"), ("hi", "max")):
        rows.append((f"FX {lab}", f"USD/GBP the season's BoE {lab}; H100 {dl.g(GPU0)}, PUE 1",
                     {s: (GPU0, fx[s][k], ONE) for s in seas}))
    for k, lab in (("lo", "low"), ("hi", "high")):
        rows.append((f"H100 {lab}", f"H100 the season's sourced {lab}; fx {dl.g(FX0)}, PUE 1",
                     {s: (h100[s][k], FX0, ONE) for s in seas if h100[s]}))
    for k, lab in (("lo", "low"), ("hi", "high")):
        for src in ("Google", "Uptime"):
            rows.append((f"ALL {lab}/{src}", f"ALL SOURCED: H100 {lab}, BoE mean, PUE {src} of the season's year",
                         {s: (h100[s][k], fx[s]["mean"], pue[(src, pue_year(s))]) for s in seas if h100[s]}))
    print("SENSITIVITY ROWS (not scored; SOURCED inputs replacing the ASSUMED ones). Per row and season: C (GBP/MWh), ETM's events")
    print("joined with all 100 jobs, ETM's revenue share; per row, part (b) (below 1 % in every ordinary season, C5 as scored).")
    print("Every cell is a full rerun of dr_data's online rule; cells inside the break-even window are cross-checked against the")
    print("scan (the same C gives the same decision: share < 1 % iff C > C_flip).")
    res, xc_n, xc_ok = [], 0, 0
    for rid, text, spec in rows:
        print(f"  [{rid}] {text}")
        cells, nb, nord, missing_ord = [], 0, 0, []
        for s in seas:
            if s not in spec:
                cells.append(f"{s} -")
                if s in ordinary:
                    missing_ord.append(s)
                continue
            g_, x_, p_ = spec[s]
            C = cost(vals, g_, x_, p_)
            r = run(s, C)
            below = r["share"] < dd.G7_BOUND
            if s in ordinary:
                nord += 1
                nb += int(below)
            fl = flip[s]
            if fl["ok"] and lo_w <= C <= hi_w:
                xc_n += 1
                xc_ok += int(below == (C > fl["cf"]))
            cells.append(f"{s} C {f(C, 1)} {r['all100']}/{r['n']} {pct(r['share'], 4)}")
        qb = nb == nord and nord > 0 and not missing_ord
        res.append(dict(rid=rid, nb=nb, nord=nord, qb=qb, missing=missing_ord))
        print("      " + "; ".join(cells))
        print(f"      -> below 1 % in {nb} of {nord} ordinary seasons computed"
              + (f" ({', '.join(missing_ord)} not computable: no sourced H100 price)" if missing_ord else "")
              + f"; part (b) {dl.yn(qb)}")
    print(f"  cross-check against the break-even scan: {xc_ok} of {xc_n} in-window cells agree")
    print()

    # ------------------------------------------------------------------------------------------------ break-even H100 price at sourced FX and PUE
    print("BREAK-EVEN H100 PRICE AT THE SOURCED FX (season's BoE mean) AND PUE (Google, Uptime of the season's year): the season")
    print("is below 1 % iff the H100 price exceeds H100* = C_flip x (10.2 kW / 1000) x PUE x fx / 8; against the season's sourced")
    print("H100 range (from the scan's C_flip; valid where the scan verified a single crossing)")
    verdicts = {}
    for s in seas:
        fl = flip[s]
        for src in ("Google", "Uptime"):
            p_ = pue[(src, pue_year(s))]
            if not fl["ok"]:
                print(f"  {s:9} {src:6}: not computable (no verified single crossing)")
                continue
            hstar = fl["cf"] * (vals["DGX"]["kw"] / 1000) * p_ * fx[s]["mean"] / vals["DGX"]["gpus"]
            if h100[s]:
                lo, hi = h100[s]["lo"], h100[s]["hi"]
                word = ("below 1 % over the whole sourced range" if lo > hstar else
                        ("at or above 1 % over the whole sourced range" if hi <= hstar else "straddles 1 % within the sourced range"))
                rng = f"sourced {h100[s]['seg']} {dl.g(lo)}..{dl.g(hi)}"
            else:
                word, rng = "no sourced H100 price", "-"
            verdicts[(s, src)] = word
            print(f"  {s:9} {src:6}: PUE {dl.g(p_)}, fx {f(fx[s]['mean'], 4)} -> H100* {f(hstar, 4)} USD/GPU-hour; {rng} -> {word}"
                  f"{'' if s in ordinary else ' (not an ordinary season under C5)'}")
    print()

    # ------------------------------------------------------------------------------------------------ result
    base = [r for r in res if r["rid"].startswith("PUE ") and not r["rid"].endswith("yr")]
    pue_hold = sum(int(r["qb"]) for r in base)
    fx_rows = [r for r in res if r["rid"].startswith("FX")]
    h_rows = [r for r in res if r["rid"].startswith("H100")]
    all_rows = [r for r in res if r["rid"].startswith("ALL")]
    print("LISTED FIXES (post first run of dr_data.py; listed here, NOT applied, since this follow-up may edit no other file):")
    print("  (1) dr_data.py prints PUE 1 and USD/GBP 1.35 as ASSUMED; both are sourced above. (2) [IDX-NEO] is a 2026-04-18 price")
    print("  applied to seasons from 2022 on; the season-matched values above replace it where found. (3) the margin of part (b) is")
    print("  the break-even table above, not 'about 11 %'.")
    print("BUG FIXES IN THIS SCRIPT AFTER ITS FIRST RUN: " + ("none" if not BUG_FIXES else "; ".join(BUG_FIXES)))
    print()
    wf = flip.get("W2023/24", {})
    sf = flip.get("S2026", {})
    print(f"RESULT FOLLOW-UP 4: break-evens (scored inputs) W2023/24 C_flip {f(wf.get('cf'), 2)} GBP/MWh "
          f"(PUE_flip {f(C0 / wf['cf'], 5) if wf.get('cf') else '-'}, FX_flip {f(FX0 * C0 / wf['cf'], 4) if wf.get('cf') else '-'}), "
          f"S2026 C_flip {f(sf.get('cf'), 2)} (PUE_flip {f(C0 / sf['cf'], 5) if sf.get('cf') else '-'}, FX_flip "
          f"{f(FX0 * C0 / sf['cf'], 4) if sf.get('cf') else '-'}); part (b) holds at {pue_hold} of {len(base)} sourced PUE values; "
          f"at the season's BoE rate: " + ", ".join(f"{r['rid'][3:]} {dl.yn(r['qb'])}" for r in fx_rows)
          + "; at the season's H100 price: " + ", ".join(f"{r['rid'][5:]} {dl.yn(r['qb'])} ({r['nb']} of {r['nord']})" for r in h_rows)
          + "; all sourced together: " + ", ".join(f"{r['rid'][4:]} {dl.yn(r['qb'])} ({r['nb']} of {r['nord']})" for r in all_rows)
          + f"; DR1's pinned part (b) (yes, 5 of 5) survives every sourced row: {dl.yn(all(r['qb'] for r in res))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
