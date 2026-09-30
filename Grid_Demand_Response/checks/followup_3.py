"""POST HOC (critic follow-up 3; not declared)

DR1 follow-up 3 to check DATA: the attribution of C5 (the scarcity exclusion) and part (b) under a dossier-consistent rule.
An unscored re-reading; dr_data.py and dr_data.txt are not edited (dr_data.py is imported unchanged).

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 3, declared
expectation "Its revenue is below 1 % of the fleet's compute cost in an ordinary season (G7)" and position G7 "MIXED
(expected: small, with exceptions in scarcity events)". Nothing in this file was declared. It was written after DR1's first
run and after the DR1 verification (Grid_Demand_Response/checks/verification.md, DATA) found that dr_data.py's choice C5
drops the whole W2022/23 season from part (b) as "the season the F2 sources mark as the scarcity exception [DFS-2223]",
while the F2 dossier's reading, tightened 2026-09-30, marks only that winter's live events as the exception (the
GBP 3,000/MWh test GAP is not), and W2023/24 is scored as ordinary although it also had live (margin) events
(docs/citations/dr1_followup3_2026-09-29.md).

What this does. dr_data.py's records, events (price 'mean', C1), fleet, jobs, compute cost and online rule are reused
unchanged. Part (b) is recomputed under:
  OLD  C5 as scored: every season except W2022/23 (must reproduce dr_data.txt's pinned shares and part (b) line);
  A    the critic's reading: W2022/23 scored with only its events typed Live left out; the other seasons as scored;
  B    the dossier-consistent rule (the corrected line): in every season, events whose price is at or above the DFS-2223
       live-event average (GBP 4,559/MWh, sourced) are left out of part (b); every season is scored;
  B-min, B-max  B with the event classified by its lowest / highest accepted bid (dr_data's C1 sensitivity readings).
A left-out event is not offered to the fleet (the online rule is rerun on the kept events; the fleet's period and compute
cost stay those of the full season, C4); the rerun is cross-checked against subtracting the left-out events' revenue from
the scored run. Part (a) is unchanged (the exclusion concerns G7's part (b) only, as C5 did). Every verdict word printed is
computed from the numbers (R15). An application calculation on public data: no ledger row; a note, not evidence (R8).
Deterministic; stdlib only (via drlib and dr_data).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/followup_3.py > Grid_Demand_Response/checks/followup_3.txt
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
F2, FU = "dr1_f2_2026-09-29.md", "dr1_followup3_2026-09-29.md"
TEXT = {k: (CIT / k).read_text(encoding="utf-8") for k in (F2, FU)}
PINNED = (HERE / "dr_data.txt").read_text(encoding="utf-8")
ZERO = Fr(0)
BUG_FIXES: list[str] = []      # bug fixes after this script's first run (none so far)


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


# id, dossier, citation, verbatim quote (checked whitespace-normalised against the dossier text)
QUOTES = [
    ("LIVE-DEF", FU, "NESO DFS winter 2022/23 review",
     "A live event could be triggered when insufficient upwards flexibility was foreseen at the day ahead stage and we believed "
     "the inadequacy could not be solved by our existing services and market incentives."),
    ("LIVE-2223", FU, "NESO DFS winter 2022/23 review",
     "There were two live activations of DFS over winter 2022/23. These took place on 23 and 24 January 2023"),
    ("GAP-2223", FU, "NESO DFS winter 2022/23 review", "Prices higher than the GAP were rejected for test events"),
    ("LIVE-PRICE-2223", FU, "NESO DFS winter 2022/23 review",
     "For live events, the average price for demand reduction was £4,559/MWh and the highest accepted price was £6,500/MWh, "
     "although a sizeable portion of participants were accepted at £3,000/MWh (see Figure 8)."),
    ("LIVE-2324", FU, "NESO DFS Winter 23/24 End of Year Report",
     "A total of 14 test events along with 2 live events were run over the winter."),
    ("MARGIN-2324", FU, "NESO DFS Winter 23/24 End of Year Report",
     "This team conducted assessments at the day ahead stage to identify whether available supply was able to meet the "
     "forecasted demand and positive margin required, which on two occasions led to live events being run."),
    ("ENHANCED-2324", FU, "NESO DFS Winter 23/24 End of Year Report",
     "As detailed within winter order of actions, market-based solutions alone would not be able to meet reserve requirements "
     "and so enhanced actions were deemed necessary."),
    ("T6-1", FU, "NESO DFS Winter 23/24 End of Year Report, Table 6", "29/11/2023 17:00 day-ahead 449 332.4 -26.0 £776,213"),
    ("T6-2", FU, "NESO DFS Winter 23/24 End of Year Report, Table 6", "01/12/2023 16:30 day-ahead 452 298.8 -33.9 £746,458"),
]
# the F2 dossier's tightened Reading (an investigator's reading, not a source quote; line-wrapped in the dossier)
F2_READING = ('Only the live events are "exceptions in scarcity events" in the declaration\'s sense; the £3,000/MWh was a '
              "guaranteed test price")
# the live-event starts the sources give (dates; for 2023/24 also the first SP of each, Table 6)
SRC_LIVE = {"W2022/23": [(dt.date(2023, 1, 23), None), (dt.date(2023, 1, 24), None)],
            "W2023/24": [(dt.date(2023, 11, 29), "17:00"), (dt.date(2023, 12, 1), "16:30")]}


def f(x, d=6) -> str:
    return dd.f(x, d)


def pct(x, d=5) -> str:
    return dd.pct(x, d)


def main() -> int:
    print("POST HOC (critic follow-up 3; not declared)")
    print()
    print("DR1 follow-up 3 to check DATA: C5's scarcity exclusion re-attributed; part (b) (G7) under a dossier-consistent rule.")
    print(f"Binding declaration Grid_Demand_Response/DECLARATION.md (declared at {dl.DECL_AT}; not edited). dr_data.py and "
          "dr_data.txt are not edited:")
    print("dr_data.py is imported unchanged. An application calculation on public data: no ledger row; a note, not evidence (R8).")
    print()

    # ------------------------------------------------------------------------------------------------ data and sources
    man = dd.manifest()
    bad = [n for n in sorted(man) if hashlib.sha256((dd.RAW / n).read_bytes()).hexdigest() != man[n]]
    print(f"DATA: {len(man)} raw files; sha256 matches Grid_Demand_Response/data/MANIFEST.md for {len(man) - len(bad)} of {len(man)}")
    if bad or not man:
        print("RESULT FOLLOW-UP 3: not computable (raw files differ from the manifest)")
        return 0
    vals, rep = dd.load_sources()
    miss = [r[0] for r in rep if not (r[4] and r[5])]
    print(f"dr_data.py's own sources (dr_data.load_sources, unchanged): {len(rep) - len(miss)} of {len(rep)} found")
    T = vals["DFS-2223"]["live_avg"]
    print(f"  [DFS-2223] (dr1_f2) \"For live events, the average price paid was £4,559/MWh.\" -> T = {dl.g(T)} GBP/MWh (the threshold of "
          "rule B; SOURCED)")
    print()
    print("SOURCED QUOTES (each checked verbatim, whitespace-normalised, at run time against its dossier)")
    qmiss = []
    for qid, dos, cite, quote in QUOTES:
        ok = ws(quote) in ws(TEXT[dos])
        qmiss += [] if ok else [qid]
        print(f"  [{qid}] {cite} ({dos}): found {dl.yn(ok)}")
        print(f"      '{quote}'")
    rd = ws(F2_READING) in ws(TEXT[F2])
    print(f"  F2 dossier's tightened Reading of the 2022/23 review (an investigator's reading, not a quote; whitespace-normalised "
          f"match): '{F2_READING}' -> found {dl.yn(rd)}")
    if miss or qmiss or not rd:
        print("RESULT FOLLOW-UP 3: not computable (a sourced input was not found)")
        return 0
    print()

    # ------------------------------------------------------------------------------------------------ the scored setting
    bidir = dt.date(int(vals["DFS-BIDIR"]["year"]), 4, int(vals["DFS-BIDIR"]["day"]))
    sps, _ = dd.load_sps(bidir)
    evs, _ = dd.build_events(sps, "mean")
    C = dd.compute_cost_mwh(vals, dd.PRIMARY_PRICE, dd.FX)
    jobs = [dl.Job(dd.W, dd.W + dd.SLACK_STEP * i, dd.R, name=f"J{i:03d}") for i in range(1, dd.N_JOBS + 1)]
    seas = [s for s in sorted({r["season"] for r in sps}, key=lambda s: (s[1:5], s[0] == "W")) if s in evs]
    period = {}
    for s in seas:
        e = evs[s]
        period[s] = (Fr((e[0]["date"] - dd.EPOCH).days * 24), Fr((e[-1]["date"] - dd.EPOCH).days * 24 + 24))
    for s in seas:
        for e in evs[s]:
            e["pmin"] = min(sp["p_min"] for sp in e["sps"])
            e["pmax"] = max(sp["p_max"] for sp in e["sps"])

    def run(keep: dict, Cx: Fr) -> dict:
        out = {}
        for s in seas:
            if s not in keep:
                continue
            st, en = period[s]
            kept = [e for e in evs[s] if keep[s](e)]
            t = dd.simulate(kept, st, en, dl.ETM, jobs, Cx)
            cost = dd.FLEET_MW * (en - st) * Cx
            out[s] = dict(n=len(kept), n_all=len(evs[s]), all100=t["events_all"], revenue=t["revenue"], cost=cost,
                          share=t["revenue"] / cost, ev_join=t["ev_join"], kept=kept)
        return out

    full = run({s: (lambda e: True) for s in seas}, C)
    print(f"SCORED SETTING (dr_data.py, unchanged): price 'mean' (C1); C = {f(C, 4)} GBP per MWh of compute [IDX-NEO, fx "
          f"{dl.g(dd.FX)} ASSUMED]; R = {dl.g(dd.R)} h (ASSUMED); fleet {dl.g(dd.FLEET_MW)} MW (ASSUMED); the ETM arm")
    print()

    # ------------------------------------------------------------------------------------------------ OLD reproduces the pin
    print("REPRODUCTION OF THE PINNED dr_data.txt (Q lines): ETM's revenue share per season, all events offered")
    rep_ok = 0
    for s in seas:
        m = re.search(rf"^  {re.escape(s)}\s+ETM joined with all 100 jobs (\d+) of (\d+) events .*?ETM revenue share ([\d.]+ %)",
                      PINNED, re.M)
        mine = pct(full[s]["share"], 5)
        same = m is not None and m.group(3) == mine and int(m.group(1)) == full[s]["all100"] and int(m.group(2)) == full[s]["n"]
        rep_ok += int(same)
        print(f"  {s:9} here {full[s]['all100']} of {full[s]['n']} events, share {mine}; pinned "
              f"{m.group(1) + ' of ' + m.group(2) + ', share ' + m.group(3) if m else '-'} -> same: {dl.yn(same)}")
    pin_b = re.search(r"part \(b\) below 1 % in every ordinary season: (\w+) \((\d+) of (\d+)\)", PINNED)
    pin_c5 = re.search(r"^  C5 (.*)$", PINNED, re.M)
    print(f"  reproduced in {rep_ok} of {len(seas)} seasons")
    print(f"  pinned C5 line: 'C5 {pin_c5.group(1) if pin_c5 else '-'}'")
    print(f"  pinned part (b): '{pin_b.group(0) if pin_b else '-'}'")
    if rep_ok != len(seas):
        print("RESULT FOLLOW-UP 3: not computable (the pinned run is not reproduced)")
        return 0
    qa = all(full[s]["all100"] == full[s]["n"] for s in seas)
    qa_n = sum(int(full[s]["all100"] == full[s]["n"]) for s in seas)
    print()

    # ------------------------------------------------------------------------------------------------ the events at issue
    print(f"THE EVENTS AT ISSUE: every event typed Live, or with any accepted bid at or above T = {dl.g(T)} GBP/MWh, in any season")
    print(f"  {'season':9} {'#':>3} {'date':10} {'from':5} {'H':>4} {'type':9} {'price':>9} {'min':>8} {'max':>8}  "
          f"price>=T min>=T max>=T  ETM jobs joined")
    live = {}
    for s in seas:
        for i, e in enumerate(evs[s]):
            if "Live" in e["types"].split("/") and s in SRC_LIVE:
                live.setdefault(s, []).append(e)
            if (s in SRC_LIVE and "Live" in e["types"].split("/")) or e["pmax"] >= T:
                print(f"  {s:9} {i + 1:>3} {str(e['date']):10} {e['sps'][0]['frm']:5} {dl.g(e['H']):>4} {e['types']:9} "
                      f"{f(e['price'], 2):>9} {f(e['pmin'], 2):>8} {f(e['pmax'], 2):>8}  {dl.yn(e['price'] >= T):>8} "
                      f"{dl.yn(e['pmin'] >= T):>5} {dl.yn(e['pmax'] >= T):>5}  {full[s]['ev_join'][i]:>3}")
    others = sum(int("Live" in e["types"].split("/")) for s in seas if s not in SRC_LIVE for e in evs[s])
    print(f"  events typed Live in the later seasons (the service's competitive form; not listed): {others}; of them at or above T "
          f"on any bid: {sum(int(e['pmax'] >= T) for s in seas if s not in SRC_LIVE for e in evs[s])}")
    for s, want in SRC_LIVE.items():
        got = [(e["date"], e["sps"][0]["frm"]) for e in live.get(s, [])]
        ok = len(got) == len(want) and all(g[0] == w[0] and (w[1] is None or g[1] == w[1]) for g, w in zip(got, want))
        print(f"  {s}: the events typed Live in the records start {', '.join(f'{d} {t}' for d, t in got)}; the sources' live "
              f"events [{'LIVE-2223' if s == 'W2022/23' else 'LIVE-2324, T6-1, T6-2'}] -> same: {dl.yn(ok)}")
    print()

    # ------------------------------------------------------------------------------------------------ the rules
    rules = [
        ("OLD", "C5 as scored: every season except W2022/23 (dr_data.py's SCARCITY)",
         {s: (lambda e: True) for s in seas if s != dd.SCARCITY}),
        ("A", "the critic's reading: W2022/23 scored without its events typed Live; the other seasons as scored",
         {s: ((lambda e: "Live" not in e["types"].split("/")) if s == "W2022/23" else (lambda e: True)) for s in seas}),
        ("B", f"CORRECTED: in every season, events whose price (C1 'mean') is >= T = {dl.g(T)} [DFS-2223] left out; all seasons",
         {s: (lambda e: e["price"] < T) for s in seas}),
        ("B-min", "sensitivity: as B, the event classified by its lowest accepted bid",
         {s: (lambda e: e["pmin"] < T) for s in seas}),
        ("B-max", "sensitivity: as B, the event classified by its highest accepted bid",
         {s: (lambda e: e["pmax"] < T) for s in seas}),
    ]
    print("PART (b) UNDER EACH RULE: per scored season, events kept of all, the ETM rerun on the kept events (joined with all 100")
    print("jobs), revenue (GBP), share of the compute cost over the full season's period, below 1 %; and the cross-check: the")
    print("scored run's revenue minus the left-out events' revenue in the scored run equals the rerun's revenue")
    res = {}
    for rid, text, keep in rules:
        out = run(keep, C)
        xc_ok = 0
        print(f"  rule {rid}: {text}")
        for s in seas:
            if s not in out:
                print(f"    {s:9} not scored")
                continue
            o = out[s]
            dropped = sum((evs[s][i]["price"] * evs[s][i]["H"] * dd.P_JOB * full[s]["ev_join"][i]
                           for i in range(len(evs[s])) if not keep[s](evs[s][i])), ZERO)
            xc = full[s]["revenue"] - dropped == o["revenue"]
            xc_ok += int(xc)
            print(f"    {s:9} kept {o['n']:>3} of {o['n_all']:>3}; ETM all-100 {o['all100']:>3} of {o['n']:>3}; revenue "
                  f"{f(o['revenue'], 2):>12}; share {pct(o['share'], 5):>11} -> below 1 %: {dl.yn(o['share'] < dd.G7_BOUND):3}; "
                  f"cross-check {dl.yn(xc)}")
        nb = sum(int(out[s]["share"] < dd.G7_BOUND) for s in out)
        qb = nb == len(out) and len(out) > 0
        res[rid] = dict(out=out, nb=nb, n=len(out), qb=qb, xc=xc_ok)
        print(f"    -> part (b) below 1 % in every scored season: {dl.yn(qb)} ({nb} of {len(out)}); cross-check {xc_ok} of "
              f"{len(out)}; with part (a) {dl.yn(qa)} ({qa_n} of {len(seas)} seasons) -> Q {'holds' if (qa and qb) else 'fails'}")
    old_same = pin_b is not None and res["OLD"]["nb"] == int(pin_b.group(2)) and res["OLD"]["n"] == int(pin_b.group(3)) \
        and dl.yn(res["OLD"]["qb"]) == pin_b.group(1)
    print(f"  rule OLD reproduces the pinned part (b) line: {dl.yn(old_same)}")
    print()

    # ------------------------------------------------------------------------------------------------ the task-text check
    print(f"CHECK OF THE CRITIC'S STATEMENT that W2023/24's live events paid 'above the GBP 4,559 that defines the exception':")
    for e in live.get("W2023/24", []):
        print(f"  {e['date']} {e['sps'][0]['frm']}: price (C1 'mean') {f(e['price'], 2)} -> at or above T: {dl.yn(e['price'] >= T)}; "
              f"highest accepted bid {f(e['pmax'], 2)} -> at or above T: {dl.yn(e['pmax'] >= T)}")
    print()

    # ------------------------------------------------------------------------------------------------ sensitivity to C
    print("SENSITIVITY (not scored): rule B's part (b) at every sourced compute price and USD/GBP in {1.20, 1.35, 1.50} (ASSUMED),")
    print("as dr_data.py's SENSITIVITY 1; per cell the seasons below 1 % of those scored, and the shares of W2022/23 and W2023/24")
    keepB = rules[2][2]
    cells = holds = 0
    rows_ = []
    for key in dd.PRICE_KEYS:
        for fx in sorted({dd.FX, *dd.FX_SENS}):
            Cx = dd.compute_cost_mwh(vals, key, fx)
            o = run(keepB, Cx)
            nb = sum(int(o[s]["share"] < dd.G7_BOUND) for s in o)
            cells += 1
            holds += int(nb == len(o))
            rows_.append((key, fx, Cx, o))
            print(f"  {key:10} fx {dl.g(fx):4} C {f(Cx, 1):>9}: below 1 % in {nb} of {len(o)} -> part (b) {dl.yn(nb == len(o)):3}; "
                  f"W2022/23 {pct(o['W2022/23']['share'], 4)}; W2023/24 {pct(o['W2023/24']['share'], 4)}")
    print(f"  part (b) under rule B holds in {holds} of {cells} cells")
    print("  closed form (valid while ETM's joined events do not change with C): a season's share falls below 1 % iff C > revenue /")
    print("  (0.01 x 100 MW x period hours); per season under rule B at the scored run's revenue, that C and its H100 GPU-hour price")
    print(f"  equivalent (x {dl.g(vals['DGX']['kw'])} kW / {dl.g(vals['DGX']['gpus'])} GPUs x fx {dl.g(dd.FX)}):")
    flip = {}
    for s, o in res["B"]["out"].items():
        st, en = period[s]
        cf = o["revenue"] / (dd.G7_BOUND * dd.FLEET_MW * (en - st))
        flip[s] = cf
        gpu_h = cf * vals["DGX"]["kw"] / 1000 * dd.FX / vals["DGX"]["gpus"]
        print(f"    {s:9} C_flip {f(cf, 2):>9} GBP/MWh (scored C {f(C, 2)}; below 1 % at the scored C: {dl.yn(C > cf)}); "
              f"{f(gpu_h, 4)} USD per GPU-hour (scored {dl.g(vals['IDX-NEO']['gpu_h'])})")
    agree = n_ag = 0
    for key, fx, Cx, o in rows_:
        for s in o:
            if o[s]["revenue"] == res["B"]["out"][s]["revenue"]:
                n_ag += 1
                agree += int((o[s]["share"] < dd.G7_BOUND) == (Cx > flip[s]))
    print(f"  the closed form agrees with the grid in {agree} of {n_ag} (cell, season) pairs where ETM's revenue equals the scored "
          f"run's ({len(rows_) * len(seas) - n_ag} pairs with a different revenue not compared)")
    print()

    # ------------------------------------------------------------------------------------------------ the listed fix
    print("LISTED FIX (post first run of dr_data.py; listed here, NOT applied, since this follow-up may edit no other file):")
    print(f"  dr_data.py sets SCARCITY = \"{dd.SCARCITY}\" and prints C5 as 'the season the F2 sources mark as the scarcity exception")
    print("  [DFS-2223]'. The attribution is wrong: the F2 dossier's tightened Reading and the reviews "
          "[LIVE-DEF, LIVE-2223, GAP-2223, LIVE-2324,")
    print("  MARGIN-2324, ENHANCED-2324] mark live (margin) events, not a season, as the scarcity exception, and W2023/24 had two.")
    print(f"  Corrected C5 (rule B): in every season, events priced at or above the DFS-2223 live average (T = {dl.g(T)} GBP/MWh)")
    print("  are the scarcity exception and are left out of part (b); every season is scored. The old rule is kept beside it above.")
    print("BUG FIXES IN THIS SCRIPT AFTER ITS FIRST RUN: " + ("none" if not BUG_FIXES else "; ".join(BUG_FIXES)))
    print()

    b, o_ = res["B"], res["OLD"]
    corrected = (f"part (b) below 1 % in every season, events priced at or above GBP {dl.g(T)}/MWh [DFS-2223] left out: "
                 f"{dl.yn(b['qb'])} ({b['nb']} of {b['n']}; W2022/23 {pct(b['out']['W2022/23']['share'], 5)}, W2023/24 "
                 f"{pct(b['out']['W2023/24']['share'], 5)}) -> Q {'holds' if (qa and b['qb']) else 'fails'}")
    print("CORRECTED LINE (rule B; the line the G7 sentence is to quote):")
    print(f"  {corrected}")
    print("OLD LINE (rule OLD, as pinned in dr_data.txt):")
    print(f"  part (b) below 1 % in every ordinary season (all but {dd.SCARCITY}): {dl.yn(o_['qb'])} ({o_['nb']} of {o_['n']})")
    print()
    words = {k: dl.yn(v["qb"]) for k, v in res.items()}
    print(f"RESULT FOLLOW-UP 3: part (b) OLD {words['OLD']} ({o_['nb']} of {o_['n']}); A {words['A']} ({res['A']['nb']} of "
          f"{res['A']['n']}); B (corrected) {words['B']} ({b['nb']} of {b['n']}); B-min {words['B-min']} ({res['B-min']['nb']} of "
          f"{res['B-min']['n']}); B-max {words['B-max']} ({res['B-max']['nb']} of {res['B-max']['n']}); part (a) {dl.yn(qa)} "
          f"({qa_n} of {len(seas)}), so Q {'holds' if (qa and b['qb']) else 'fails'} under every rule "
          f"{'(unchanged)' if not any(qa and v['qb'] for v in res.values()) else '(CHANGES under some rule)'}; rule B's part (b) "
          f"holds in {holds} of {cells} compute-cost cells")
    return 0


if __name__ == "__main__":
    sys.exit(main())
