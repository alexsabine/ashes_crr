"""POST HOC (critic follow-up 2; not declared).

DR1 follow-up 2: the restart overhead R that decides H2, H3 and DATA, swept over the sourced F4 range.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here). This script is NOT declared
there: it is a post hoc follow-up to the completeness critic (declaration section 4, 'one follow-up round'). It changes no
declared prediction, arm, threshold or named parameter, and it edits no pinned file. It reruns the scored Q predicate of
three pinned checks with one input changed, R (the restart overhead per pause event), which the pinned checks take as
R = 0.1 h ASSUMED (EPS2 T1's model constant):
  - H2 (dr_h2.py): dr_h2.score_cell over the same eight (D, H) cells, the same tiers, the same 1 % rule;
  - H3 (dr_h3.py): dr_h3.portfolio / analyse / score over the same three H cells (the module constant dr_h3.R, which the
    predicate reads, is set to each value and restored);
  - DATA (dr_data.py): dr_data.simulate for the ETM arm on the same NESO DFS events (sha256 against MANIFEST.md), the same
    compute cost C, the same season split; Q = part (a) ETM joins every event with all 100 jobs in every season AND part (b)
    ETM's revenue share is below 1 % in every ordinary season (dr_data.py's C10).
The R values: every restart value dr_h4.py parses from the F4 dossier (docs/citations/dr1_f4_2026-09-29.md; each quote
checked verbatim against the dossier at run time by dr_h4.parse_sources), plus the ASSUMED 0.1 h. The closed-form flip
threshold of each predicate is printed and verified by the predicate itself at the threshold and one step above it.

Every verdict word printed is computed from the numbers (R15). Rung R4 at most (synthetic model; DATA an application
calculation); a note, not evidence (R8). Deterministic, exact rationals (stdlib only, via drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/followup_2.py > Grid_Demand_Response/checks/followup_2.txt
"""
from __future__ import annotations

import datetime as dt
import hashlib
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import drlib as dl  # noqa: E402
import dr_h2  # noqa: E402
import dr_h3  # noqa: E402
import dr_h4  # noqa: E402
import dr_data as dd  # noqa: E402

REPO = HERE.parents[1]
ZERO = Fr(0)
SEC = Fr(1, 3600)                     # hours per second
R_ASSUMED = Fr(1, 10)                 # ASSUMED (EPS2 T1's model constant, the value in dr_h2.py, dr_h3.py, dr_data.py)
STEP = Fr(1, 10 ** 6)                 # CHOICE: the step (hours) above a threshold at which a flip is verified (drlib's p_all step)
LABEL_OLD = "no fetched source supplies"
LABEL_NEW = "ASSUMED, inside the sourced F4 range"


def s_(h: Fr) -> str:
    return f"{float(h / SEC):.2f} s"


def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def pinned_q(fname: str, cid: str) -> str | None:
    m = re.search(rf"^RESULT {cid}: Q (holds|fails|not computable)", (HERE / fname).read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else None


# ============================================================================================ the three predicates
def h2_q(R: Fr) -> dict:
    cells = []
    for D in dr_h2.DS:
        for H in dr_h2.HS:
            job = dl.Job(dr_h2.W, D, R)
            K = len(dl.every(dr_h2.SPACING, H, job.W))
            sc = dr_h2.score_cell(job, H, K, dr_h2.tiers())
            cells.append(dict(D=D, H=H, within=sc["within"], maxrel=sc["maxrel"], cf=R / (H + R)))
    if any(c["within"] is None for c in cells):
        word = "not computable"
    else:
        word = "holds" if all(c["within"] for c in cells) else "fails"
    return dict(word=word, cells=cells, n_in=sum(int(bool(c["within"])) for c in cells),
                cf_agree=sum(int(c["maxrel"] == c["cf"]) for c in cells))


def h3_q(R: Fr) -> dict:
    old = dr_h3.R
    dr_h3.R = R
    try:
        jobs = dr_h3.portfolio(dr_h3.SLACK_STEP)
        cells = []
        for H in dr_h3.HS:
            an = dr_h3.analyse(jobs, H, dr_h3.SPACING, False)
            cells.append(dict(H=H, K=an["K"], s=dr_h3.score(an)))
    finally:
        dr_h3.R = old
    if not all(c["s"]["computable"] for c in cells):
        word = "not computable"
    else:
        word = "holds" if all(c["s"]["holds"] for c in cells) else "fails"
    return dict(word=word, cells=cells, slack_min=min(j.slack for j in jobs))


class Data:
    def __init__(self):
        man = dd.manifest()
        self.sha_ok = bool(man) and all(
            (dd.RAW / n).exists() and hashlib.sha256((dd.RAW / n).read_bytes()).hexdigest() == h for n, h in man.items())
        self.n_files = len(man)
        vals, rep = dd.load_sources()
        self.src_ok = all(fo and pa for *_, fo, pa in rep)
        self.vals = vals
        bidir = dt.date(int(vals["DFS-BIDIR"]["year"]), 4, int(vals["DFS-BIDIR"]["day"]))
        sps, _ = dd.load_sps(bidir)
        evs, _ = dd.build_events(sps, "mean")
        self.seasons = sorted(evs, key=lambda s: (s[1:5], s[0] == "W"))     # dr_data.py's season order
        self.evs = evs
        self.C = dd.compute_cost_mwh(vals, dd.PRIMARY_PRICE, dd.FX)

    def bounds(self, C: Fr | None = None) -> dict:
        C = self.C if C is None else C
        price = min(((e["price"] * e["H"] / C, s, e) for s in self.seasons for e in self.evs[s]), key=lambda x: x[0])
        gaps = [(b["t"] - (a["t"] + a["H"]), s) for s in self.seasons for a, b in zip(self.evs[s], self.evs[s][1:])]
        nmax = max(len(self.evs[s]) for s in self.seasons)
        return dict(price=price, gap=min(gaps, key=lambda x: x[0]), nmax=nmax)

    def q(self, R: Fr) -> dict:
        jobs = [dl.Job(dd.W, dd.W + dd.SLACK_STEP * i, R, name=f"J{i:03d}") for i in range(1, dd.N_JOBS + 1)]
        rows = {}
        for s in self.seasons:
            e = self.evs[s]
            start = Fr((e[0]["date"] - dd.EPOCH).days * 24)
            end = Fr((e[-1]["date"] - dd.EPOCH).days * 24 + 24)
            t = dd.simulate(e, start, end, dl.ETM, jobs, self.C)
            rows[s] = dict(all=t["events_all"], n=len(e), price=t["price_declined"], dead=t["deadline_declined"],
                           blocked=t["blocked"], share=t["revenue"] / (dd.FLEET_MW * (end - start) * self.C))
        ordinary = [s for s in rows if s != dd.SCARCITY]
        qa = all(r["all"] == r["n"] for r in rows.values())
        qb = len(ordinary) > 0 and all(rows[s]["share"] < dd.G7_BOUND for s in ordinary)
        return dict(word="holds" if (qa and qb) else "fails", qa=qa, qb=qb, rows=rows, slack_min=min(j.slack for j in jobs))


# ============================================================================================ main
def main() -> int:
    print("POST HOC (critic follow-up 2; not declared)")
    print(f"DR1 follow-up 2: the restart overhead R that decides H2, H3 and DATA, swept over the sourced F4 range "
          f"(Grid_Demand_Response/DECLARATION.md, declared at {dl.DECL_AT}; not declared there)")
    print("Rung R4 at most; a note, not evidence (R8). No pinned file is edited; the pinned predicates are imported and rerun.")
    print()

    # ------------------------------------------------------------------------------------------------ the R values
    vals, rep = dr_h4.parse_sources()
    n_found = sum(int(fo and pa) for _, fo, pa in rep)
    sourced = sorted(((v["h"], vid, v) for vid, v in vals.items() if v["role"] == "R"), key=lambda x: (x[0], x[1]))
    print("THE R VALUES")
    print(f"  F4 quotes found verbatim in docs/citations/dr1_f4_2026-09-29.md and parsed (dr_h4.parse_sources): {n_found} of {len(rep)}")
    print(f"  SOURCED restart values (role R in dr_h4.py): {len(sourced)}")
    for h, vid, v in sourced:
        print(f"    {vid:15} {s_(h):>10} = {f(h, 6)} h  [{v['src']}]  CHOICE (dr_h4.py): {v['note']}")
    R_lo, R_hi = sourced[0][0], sourced[-1][0]
    inside = R_lo <= R_ASSUMED <= R_hi
    print(f"  ASSUMED        {s_(R_ASSUMED):>10} = {f(R_ASSUMED, 6)} h  (EPS2 T1's model constant, the value in the pinned H2, H3, DATA)")
    print(f"  sourced range {s_(R_lo)} to {s_(R_hi)}; the ASSUMED 0.1 h lies inside it: {dl.yn(inside)}")
    print(f"  note: dr_h4.py's 'restart grid (10 values)' is these {len(sourced)} sourced values plus the ASSUMED 0.1 h (R-EPS2)")
    mods = dict(H2=dr_h2.R, H3=dr_h3.R, DATA=dd.R)
    print("  the pinned scripts' R: " + "; ".join(f"{k} {f(v, 4)} h" for k, v in mods.items())
          + f" -> all equal the ASSUMED 0.1 h: {dl.yn(all(v == R_ASSUMED for v in mods.values()))}")
    print()
    sweep = [(h, vid) for h, vid, _ in sourced] + [(R_ASSUMED, "ASSUMED-0.1h")]
    sweep.sort(key=lambda x: (x[0], x[1]))

    # ------------------------------------------------------------------------------------------------ H2
    print("H2 (dr_h2.score_cell; Q: at matched delay ETM and the best tier supply the same curtailed energy within 1 %, in all 8 cells)")
    print(f"  {'R id':15} {'R':>10} {'cells within 1 %':>17} {'max rel over cells':>19} {'rel == R/(H+R)':>15}  Q")
    h2 = {}
    for h, vid in sweep:
        r = h2_q(h)
        h2[vid] = r
        mx = max(c["maxrel"] for c in r["cells"])
        print(f"  {vid:15} {s_(h):>10} {r['n_in']:>11} of {len(r['cells'])} {f(mx, 6):>19} {r['cf_agree']:>9} of {len(r['cells'])}  {r['word']}")
    tol = dr_h2.TOL
    per_h = {H: H * tol / (1 - tol) for H in dr_h2.HS}
    t2 = min(per_h.values())
    at, above = h2_q(t2), h2_q(t2 + STEP)
    ok2 = at["word"] == "holds" and above["word"] == "fails"
    print(f"  closed form: per cell rel = R/(H + R) (ETM's energy per hour of delay H/(H + R) against the tiers' 1); within 1 % iff "
          f"R <= H/99: " + ", ".join(f"H {dl.g(H)}: {s_(v)}" for H, v in per_h.items()))
    print(f"  flip threshold (binding H = {dl.g(min(dr_h2.HS))}): R* = {t2} h = {s_(t2)}; the predicate at R*: {at['word']}; at R* + "
          f"{STEP} h: {above['word']} -> threshold verified: {dl.yn(ok2)}")
    print()

    # ------------------------------------------------------------------------------------------------ H3
    print("H3 (dr_h3.portfolio/analyse/score; Q: ETM's firm supply curve flat at R/H, OWN's and WALL's rising, gap largest for the tight")
    print("tercile, in all 3 H cells). Per cell: jobs (of 100) whose ETM entry price is R/H attained; rising OWN/WALL; tight OWN/WALL")
    h3 = {}
    for h, vid in sweep:
        r = h3_q(h)
        h3[vid] = r
        parts = [f"H {dl.g(c['H'])}: {c['s']['etm_at_rh']} flat {dl.yn(c['s']['flat'])}, rising "
                 f"{dl.yn(c['s']['rising']['OWN'])}/{dl.yn(c['s']['rising']['WALL'])}, tight "
                 f"{dl.yn(c['s']['tight']['OWN'])}/{dl.yn(c['s']['tight']['WALL'])}" for c in r["cells"] if c["s"]["computable"]]
        print(f"  {vid:15} {s_(h):>10}  " + "; ".join(parts) + f"  -> Q {r['word']}")
    Ks = sorted({c["K"] for r in h3.values() for c in r["cells"]})
    smin = next(iter(h3.values()))["slack_min"]
    t3 = smin / max(Ks)
    at3, above3 = h3_q(t3), h3_q(t3 + STEP)
    flat_at = all(c["s"]["flat"] for c in at3["cells"])
    flat_above = all(c["s"]["flat"] for c in above3["cells"])
    ok3 = flat_at and not flat_above and at3["word"] == "holds" and above3["word"] == "fails"
    n_other = sum(int(all(c["s"]["rising"].values()) and all(c["s"]["tight"].values()))
                  for r in list(h3.values()) + [at3, above3] for c in r["cells"])
    n_cells = sum(len(r["cells"]) for r in list(h3.values()) + [at3, above3])
    print(f"  closed form for 'flat': ETM's deadline counts own steps (W + n R <= D), so the tightest job (slack {dl.g(smin)} h) accepts all K = "
          f"{', '.join(str(k) for k in Ks)} offers at R/H iff K R <= {dl.g(smin)} h")
    print(f"  flip threshold: R* = {t3} h = {f(t3, 6)} h = {s_(t3)}; at R*: flat {dl.yn(flat_at)}, Q {at3['word']}; "
          f"at R* + {STEP} h: flat {dl.yn(flat_above)}, Q {above3['word']} -> threshold verified: {dl.yn(ok3)}")
    print(f"  the other two parts (rising, tight, for OWN and WALL) hold in {n_other} of {n_cells} evaluated cells (no closed form printed "
          f"for them)")
    print()

    # ------------------------------------------------------------------------------------------------ DATA
    D_ = Data()
    print("DATA (dr_data.simulate, ETM arm; Q: (a) ETM joins every event with all 100 jobs in every season AND (b) ETM's revenue share")
    print(f"< 1 % in every ordinary season, all seasons except {dd.SCARCITY})")
    print(f"  raw files matching MANIFEST.md sha256: {dl.yn(D_.sha_ok)} ({D_.n_files} files); dr_data sourced quotes found and parsed: "
          f"{dl.yn(D_.src_ok)}; C = {f(D_.C, 4)} GBP per MWh of compute (dr_data.py's scored C)")
    if not (D_.sha_ok and D_.src_ok):
        print("  DATA not computable (raw files or sources missing)")
        return 1
    print("  per season: events joined with all 100 jobs / events; job-events declined on price / deadline / blocked; ETM revenue share")
    dq = {}
    for h, vid in sweep:
        r = D_.q(h)
        dq[vid] = r
        print(f"  {vid:15} {s_(h):>10}  " + "; ".join(
            f"{s} {x['all']}/{x['n']} ({x['price']}/{x['dead']}/{x['blocked']}) {f(x['share'] * 100, 5)} %" for s, x in r["rows"].items())
            + f"  -> (a) {dl.yn(r['qa'])}, (b) {dl.yn(r['qb'])}, Q {r['word']}")
    b = D_.bounds()
    rp, sp, ep = b["price"]
    gap, sg = b["gap"]
    dead = next(iter(dq.values()))["slack_min"] / b["nmax"]
    t4 = min(rp, gap, dead)
    at4, above4 = D_.q(t4), D_.q(t4 + STEP)
    ok4 = at4["qa"] and not above4["qa"] and at4["word"] == "holds" and above4["word"] == "fails"
    print("  closed form for part (a): ETM joins an event iff (price / C) H >= R (its only charge is R, own clock), the event starts no")
    print("  earlier than the previous event's end plus R (else blocked), and n R <= slack (own-step deadline). Bounds:")
    print(f"    price: R <= min over events of price H / C = {f(rp, 8)} h = {s_(rp)} (event {sp} {ep['date']} {ep['sps'][0]['frm']}, "
          f"H {dl.g(ep['H'])} h, price {f(ep['price'], 2)} GBP/MWh)")
    print(f"    block: R <= the shortest gap between consecutive events = {dl.g(gap)} h = {s_(gap)} ({sg})")
    print(f"    deadline (sufficient): R <= tightest slack / most events in a season = {dl.g(next(iter(dq.values()))['slack_min'])}/{b['nmax']} h = "
          f"{s_(dead)}")
    print(f"  flip threshold: R* = the smallest bound = {f(t4, 8)} h = {s_(t4)} (exact {t4}); at R*: (a) {dl.yn(at4['qa'])}, Q {at4['word']}; "
          f"at R* + {STEP} h: (a) {dl.yn(above4['qa'])}, Q {above4['word']} -> threshold verified: {dl.yn(ok4)}")
    nb = sum(int(r["qb"]) for r in dq.values())
    print(f"  part (b) holds at {nb} of {len(dq)} swept values (its largest share, at full participation, is set by the prices, not by R)")
    print("  CONTEXT (not scored): the price bound under every compute cost of dr_data.py's SENSITIVITY 1 (C from each sourced price,")
    print("  USD/GBP in {1.20, 1.35, 1.50} ASSUMED); R* moves with C as 1/C")
    ctx = []
    for key in dd.PRICE_KEYS:
        for fx in sorted({dd.FX, *dd.FX_SENS}):
            Cx = dd.compute_cost_mwh(D_.vals, key, fx)
            ctx.append((D_.bounds(Cx)["price"][0], key, fx, Cx))
    for rpx, key, fx, Cx in ctx:
        print(f"    {key:10} fx {dl.g(fx):4} C {f(Cx, 1):>9} GBP/MWh: price bound {s_(rpx):>11}")
    print(f"  price bound range over these {len(ctx)} costs: {s_(min(c[0] for c in ctx))} to {s_(max(c[0] for c in ctx))}")
    print("  per sourced R: the number of these costs whose price bound is >= R (necessary for part (a); the block and deadline bounds")
    print("  above do not depend on C)")
    print("    " + "; ".join(f"{vid} {s_(h)}: {sum(int(c[0] >= h) for c in ctx)} of {len(ctx)}" for h, vid, _ in sourced))
    print()

    # ------------------------------------------------------------------------------------------------ reproduction of the pinned verdicts
    pins = dict(H2=pinned_q("dr_h2.txt", "H2"), H3=pinned_q("dr_h3.txt", "H3"), DATA=pinned_q("dr_data.txt", "DATA"))
    here = dict(H2=h2["ASSUMED-0.1h"]["word"], H3=h3["ASSUMED-0.1h"]["word"], DATA=dq["ASSUMED-0.1h"]["word"])
    txt = (HERE / "dr_data.txt").read_text(encoding="utf-8")
    pin_rows = {m[0]: (m[1], m[2]) for m in re.findall(
        r"^  (\S+)\s+ETM joined with all 100 jobs (\d+ of \d+) events.*revenue share ([\d.]+) %", txt, re.M)}
    rows_here = {s: (f"{x['all']} of {x['n']}", f"{float(x['share'] * 100):.5f}") for s, x in dq["ASSUMED-0.1h"]["rows"].items()}
    same_rows = pin_rows == rows_here
    print("REPRODUCTION AT THE ASSUMED 0.1 h (the sweep's value against the pinned RESULT lines)")
    for k in pins:
        print(f"  {k:5} pinned Q {pins[k]}; rerun here Q {here[k]} -> same: {dl.yn(pins[k] == here[k])}")
    print(f"  DATA per season (events joined with all jobs, revenue share) equal to the pinned 'Q (scored, primary inputs)' lines: "
          f"{dl.yn(same_rows)} ({len(rows_here)} seasons)")
    print()

    # ------------------------------------------------------------------------------------------------ decided by R
    def tally(res: dict) -> tuple[int, int, str]:
        ws = [res[vid]["word"] for _, vid, _ in sourced]
        nh, nf = ws.count("holds"), ws.count("fails")
        return nh, nf, ("yes" if nh and nf else "no")

    thr = dict(H2=(t2, ok2), H3=(t3, ok3), DATA=(t4, ok4))
    res = dict(H2=h2, H3=h3, DATA=dq)
    summ = (HERE / "dr_summary.txt").read_text(encoding="utf-8")
    srows = re.findall(r"^  (H\d|DATA)\s+(holds|fails|not computable)\s+(Q holds|Q fails)\s+(hit|miss)", summ, re.M)
    print("SUMMARY WITH A 'DECIDED BY R' COLUMN (rows parsed from the pinned dr_summary.txt, which is not edited; 'decided by R' =")
    print(f"the Q verdict differs between sourced values in {s_(R_lo)}..{s_(R_hi)}; computed for H2, H3, DATA only)")
    print(f"  {'check':6} {'Q (pinned)':12} {'forecast':9} {'hit':5} {'decided by R':13} detail")
    for cid, qw, fc, hit in srows:
        if cid in res:
            nh, nf, dec = tally(res[cid])
            t, ok = thr[cid]
            detail = (f"Q holds at {nh}, fails at {nf} of {len(sourced)} sourced R; holds iff R <= {s_(t)} (verified {dl.yn(ok)}); "
                      f"at the ASSUMED 0.1 h: {res[cid]['ASSUMED-0.1h']['word']}")
        else:
            src = (HERE / f"dr_{cid.lower()}.py").read_text(encoding="utf-8")
            m = re.search(r"^(R|R_EPS2) = (?:Fr\(1, 10\)|dl\.q\(\"0\.1\"\))\s+# ASSUMED", src, re.M)
            if cid == "H4":
                dec, detail = "swept inside", "dr_h4.py scores every value of its F4 restart grid (its Q is over all of them)"
            else:
                dec = "not swept"
                detail = (f"ASSUMED {m.group(1)} = 0.1 h in dr_{cid.lower()}.py; outside this follow-up" if m else
                          f"no ASSUMED R = 0.1 h found in dr_{cid.lower()}.py by this script's pattern")
        print(f"  {cid:6} {qw:12} {fc:9} {hit:5} {dec:13} {detail}")
    print()

    # ------------------------------------------------------------------------------------------------ the label
    print(f"THE LABEL (the files are not edited here; each line carrying '{LABEL_OLD}' is listed with the label this follow-up's")
    print(f"numbers support)")
    hits = []
    for p in sorted(HERE.glob("*.py")) + sorted(HERE.glob("*.txt")):
        if p.name.startswith("followup_"):
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if LABEL_OLD in line:
                hits.append((p.name, i))
    eps2 = (REPO / "docs" / "citations" / "eps2_2026-09-29.md").read_text(encoding="utf-8")
    eps2_line = next((i for i, l in enumerate(eps2.splitlines(), 1) if LABEL_OLD in l), None)
    print(f"  origin: docs/citations/eps2_2026-09-29.md line {eps2_line} (EPS2's reading, written before the DR1 F4 dossier existed)")
    print(f"  lines in Grid_Demand_Response/checks/: {len(hits)}: " + ", ".join(f"{n}:{i}" for n, i in hits))
    print(f"  supported label: R = 0.1 h {LABEL_NEW if inside else 'ASSUMED, outside the sourced F4 range'} "
          f"({s_(R_lo)} to {s_(R_hi)}, docs/citations/dr1_f4_2026-09-29.md via dr_h4.py)")
    print()

    print("POST-FIRST-RUN CHANGES: (1) output text only: H3's threshold line printed the fraction twice ('5/41 h = 5/41 h'); "
          "(2) added, context only (not scored): per sourced R, the number of the 24 compute costs whose DATA price bound is >= R; "
          "no input, predicate, threshold or verdict changed")
    print()
    print("RESULT FOLLOWUP-2 (POST HOC): " + "; ".join(
        f"{cid} Q holds at {tally(res[cid])[0]} of {len(sourced)} sourced R, flips above {s_(thr[cid][0])} (verified "
        f"{dl.yn(thr[cid][1])}), decided by R {tally(res[cid])[2]}, pinned verdict at 0.1 h reproduced {dl.yn(pins[cid] == here[cid])}"
        for cid in ("H2", "H3", "DATA")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
