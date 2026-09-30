"""DR1 check H8 (Grid_Demand_Response/DECLARATION.md section 2, pushed at e67e8ee; binding, never edited here):
the value to the grid: curtailable MW-hours per season under each arm's minimum payment, at a price grid.

Declared prediction Q: at every payment above R/H, ETM supplies all the flexibility; OWN supplies it only while slack lasts.
Declared forecast: Q holds.
Also printed: the gate's G-ZERO and G-NEG in this check's own terms (G-NEG: no events offered, ETM not ahead of WALL on any
outcome by more than 1 %), and, as context read from the pinned outputs, the G-NEG words of H1-H7 (the whole battery).

Arithmetic: Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; selftest pinned in drlib_selftest.txt).
Every verdict word below is computed from the numbers (R15). Rung R4 (synthetic model); a note, not evidence (R8).
Deterministic, stdlib only (exact Fractions). Runtime several minutes.

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h8.py > Grid_Demand_Response/checks/dr_h8.txt
"""
from __future__ import annotations

import bisect
import datetime
import re
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CIT = REPO / "docs" / "citations"
CHECKS = Path(__file__).resolve().parent
ZERO, ONE = Fr(0), Fr(1)
TOL = Fr(1, 100)                     # G-NEG's declared 1 % (DECLARATION.md section 2, the gate)

# ------------------------------------------------------------------------------------------------ sourced inputs (quotes)
Q_PHX = ("Each event required the cluster to reduce power by 25% with respect to the average base load during the peak demand "
         "period, sustain the reduction for 3 hours")
Q_PHX_FILE = "dr1_f1_2026-09-29.md"
Q_PHX_SRC = "Colangelo et al., arXiv:2507.00909 v1 (the Phoenix field trial)"
Q_FLEX = ("(b) Flex 1: up to 10% performance (average throughput) reduction allowed over a 3-6 hour period; (c) Flex 2: up to "
          "25% allowed; (d) Flex 3: up to 50% allowed.")
Q_FLEX_FILE = "dr1_f1_2026-09-29.md"
Q_DFS = ("Month Number of Events Bid Volume MWh Delivered Volume MWh Accuracy % of delivered vs bid volume December 6 326.5 "
         "244.8 66.69% January 8 1335.6 865.6 64.81% February 13 1839 1206.9 65.63% March 17 1948.6 1600.5 82.14% Total 44 "
         "5449.6 3917.7 71.90%")
Q_DFS_FILE = "dr1_f2_2026-09-29.md"
Q_DFS_SRC = "NESO, DFS winter 2024/25 report (published 3 July 2025)"
Q_KOK = "assuming Daly-Young optimal checkpointing with 5 minute restart overhead and 5 minute checkpoint write overhead."
Q_KOK_FILE = "dr1_f4_2026-09-29.md"
Q_KOK_SRC = "Kokolis et al., 'Revisiting Reliability in Large-Scale Machine Learning Research Clusters' (HPCA 2025, arXiv:2410.21680v2)"

# ------------------------------------------------------------------------------------------------ inputs
W = dl.q(1000)                       # DECLARED (DR1 section 2 adopts EPS2 T1's units)
R = dl.q("0.1")                      # ASSUMED (EPS2 T1 model constant; no fetched source supplies R)
N_JOBS = 100                         # ASSUMED via DECLARATION section 3 ('running jobs of the H3 portfolio'; H3: 100 jobs)
SLACK_STEP = dl.q(5)                 # ASSUMED (H3's scored spread: slack_i = 5 i h, i = 1..100)
HS = (dl.q(1), dl.q(3), dl.q(4))     # 1, 4 ASSUMED (EPS2 T1); 3 SOURCED (Phoenix event, 3 h)
SPACING = dl.q(24)                   # CHOICE (EPS2 T1: one offer every 24 wall hours at hours 24..984)
P_JOB = dl.q(1)                      # ASSUMED (section 3's 100 MW fleet (ASSUMED) over 100 jobs: 1 MW per job)
GRID = tuple(dl.q(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))  # ASSUMED (EPS2 T1)
TIER_XS = (dl.q("0.10"), dl.q("0.25"), dl.q("0.50"))   # SOURCED (Flex 1-3)
TIER_WS = (dl.q(3), dl.q(6))                           # SOURCED range '3-6 hour period'; CHOICE: its two ends
SPACING_SENS = (dl.q(12), dl.q(48))  # CHOICE (EPS2 T1's spacing sensitivity; not scored)
SPREADS_SENS = ((dl.q(1), "slack_i = 1 i h (1..100 h)"),
                (dl.q("0.05"), "slack_i = 0.05 i h (0.05..5 h)"),
                (dl.q(10), "slack_i = 10 i h (10..1000 h)"))   # ASSUMED (H3's sensitivity spreads; not scored)
SLOT = dl.q(24)                      # CHOICE (drlib's Poisson variant: at most one event per 24 h slot; sensitivity only)

POST_FIRST_RUN_CHANGES: list[str] = []


# ------------------------------------------------------------------------------------------------ helpers
def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def relx(a: Fr, b: Fr) -> Fr:
    """The harness formula |a - b| / max(|a|, |b|), exactly (0 when both are 0)."""
    m = max(abs(a), abs(b))
    return ZERO if m == 0 else abs(a - b) / m


def quote_found(quote: str, fname: str) -> bool:
    return quote in (CIT / fname).read_text(encoding="utf-8")


def dfs_rate():
    months = re.findall(r"(December|January|February|March) (\d+) ", Q_DFS)
    total = int(re.search(r"Total (\d+) ", Q_DFS).group(1))
    days = (datetime.date(2025, 4, 1) - datetime.date(2024, 12, 1)).days
    return total, months, days, Fr(total, days * 24)


def kok_overheads():
    m = re.findall(r"(\d+) minute (restart overhead|checkpoint write overhead)", Q_KOK)
    vals = {k: Fr(int(v), 60) for v, k in m}
    return vals["restart overhead"], vals["checkpoint write overhead"]


def portfolio(step: Fr, R_=R, S_=ZERO) -> list[dl.Job]:
    return [dl.Job(W, W + step * i, R_, S=S_, name=f"J{i:03d}") for i in range(1, N_JOBS + 1)]


def tier_arms():
    return [dl.tier(x, w, name=f"T{int(x * 100)}/{dl.g(w)}h") for x in TIER_XS for w in TIER_WS]


def ref_all(m: dl.Model, n, L, he) -> bool:
    """Q-a's reference: accept every offer the job is running for (all the flexibility)."""
    return True


def ref_slack(m: dl.Model, n, L, he) -> bool:
    """Q-b's reference: accept an offer iff one more event still meets the arm's deadline (the slack lasts)."""
    return m.met(n + 1, L + he)


def run_policy(job: dl.Job, arm: dl.Arm, offs, decide, ref=None) -> dict:
    """Exact expectation (p = 1: the single path) of a season under the decision rule decide(k, n, L) -> accept?; with a
    reference rule ref, the probability mass of reached, made offers at which the rule declines where ref accepts (short) and
    accepts where ref declines (beyond)."""
    m = dl.Model(job, arm)
    dist = {(0, ZERO): ONE}
    pay_e = live = short = beyond = ZERO
    for k, of in enumerate(offs):
        he = m.heff(of.H)
        new = {}
        for (n, L), w in dist.items():
            if m.running(of.t, n, L):
                wp = w * of.p
                live += wp
                acc = decide(k, n, L)
                if ref is not None:
                    r = ref(m, n, L, he)
                    if r and not acc:
                        short += wp
                    if acc and not r:
                        beyond += wp
                if acc:
                    s1 = (n + 1, L + he)
                    new[s1] = new.get(s1, ZERO) + wp
                    pay_e += wp * m.e1 * he
                    if of.p < 1:
                        new[(n, L)] = new.get((n, L), ZERO) + w * (1 - of.p)
                    continue
            new[(n, L)] = new.get((n, L), ZERO) + w
        dist = new
    ev = sum((w * n for (n, L), w in dist.items()), ZERO)
    Lx = sum((w * L for (n, L), w in dist.items()), ZERO)
    pmet = sum((w for (n, L), w in dist.items() if m.met(n, L)), ZERO)
    val = sum((w * m.vjob(n, L) for (n, L), w in dist.items()), ZERO)
    comp = sum((w * m.completion(n, L) for (n, L), w in dist.items()), ZERO)
    return dict(live=live, events=ev, fh=m.energy(Lx), MWh=m.energy(Lx) * P_JOB, pay_e=pay_e, p_met=pmet, valuation=val,
                completion=comp, short=short, beyond=beyond)


class Pieces:
    """One job under one arm: its outcome as an exact piecewise-constant function of the flat payment pi >= 0. The x*-rule
    policy (accept iff pi > x*, or pi == x* and attained; valid when every acceptance region is [x*, inf), 'closed') depends
    on pi only through its order against the job's distinct x* values, so it is constant at each such value and on each open
    interval between consecutive values; every piece is evaluated once, exactly."""

    def __init__(self, job: dl.Job, arm: dl.Arm, offs, floor: Fr, ref=None):
        self.job, self.arm, self.offs, self.floor = job, arm, offs, floor
        F = dl.value_fns(job, arm, offs)
        self.xs = dl.xstar_all(job, arm, offs, F)
        self.pa = dl.p_all(job, arm, offs, F)
        self.closed = all(x.closed for x in self.xs.values())
        self.n_states = len(self.xs)
        th = {x.x for x in self.xs.values() if x.kind == "threshold" and x.x >= 0}
        self.base = sorted(th | {ZERO, floor})
        self.at, self.op = [], []
        for i, b in enumerate(self.base):
            nxt = self.base[i + 1] if i + 1 < len(self.base) else b + 2
            self.at.append(self._eval(b, ref))
            self.op.append(self._eval((b + nxt) / 2, ref))

    def _eval(self, pi, ref):
        xs = self.xs
        return run_policy(self.job, self.arm, self.offs, lambda k, n, L: dl.accepts_at(xs[(k, n, L)], pi), ref)

    def at_pi(self, pi) -> dict:
        i = bisect.bisect_left(self.base, pi)
        if i < len(self.base) and self.base[i] == pi:
            return self.at[i]
        if i == 0:
            raise ValueError("pi below 0 is not evaluated")
        return self.op[i - 1]

    def just_above(self) -> dict:
        """The piece on the open interval just above the floor."""
        return self.op[self.base.index(self.floor)]

    def above(self):
        """The pieces with every payment strictly above the floor: (label, lower end, inclusive?, result)."""
        out = []
        for i, b in enumerate(self.base):
            if b > self.floor:
                out.append((b, True, self.at[i]))
            if b >= self.floor:
                out.append((b, False, self.op[i]))
        return out


def first_bad(pcs: Pieces, key: str):
    """The lowest payment above the floor at which the piece's mismatch `key` is positive: (x, inclusive?) or None."""
    for b, inc, r in pcs.above():
        if r[key] > 0:
            return (b, inc)
    return None


def fmt_pt(p) -> str:
    if p is None:
        return "-"
    b, inc = p
    return (f"{float(b):.6f}" if inc else f">{float(b):.6f}")


# ------------------------------------------------------------------------------------------------ one cell
def run_cell(jobs, H: Fr, offs, scored: bool, arms_ctx=True) -> dict:
    """ETM against Q-a's reference, OWN against Q-b's, and (scored) WALL, TIER and H0 for the value table."""
    job0 = jobs[0]
    floor = job0.rate * job0.overhead / H
    assert all(of.t < W for of in offs)          # every offer precedes the earliest completion: every job runs at every offer
    out = dict(H=H, offs=offs, K=len(offs), floor=floor, rows=[])
    tiers = tier_arms() if (scored and arms_ctx) else []
    for job in jobs:
        r = dict(job=job, nm={}, pc={}, h0=None)
        r["pc"]["ETM"] = Pieces(job, dl.ETM, offs, floor, ref_all)
        r["pc"]["OWN"] = Pieces(job, dl.OWN, offs, floor, ref_slack)
        for a in (dl.ETM, dl.OWN, dl.WALL):
            r["nm"][a.name] = dl.nmax(job, a, H)
        if scored and arms_ctx:
            r["pc"]["WALL"] = Pieces(job, dl.WALL, offs, floor, ref_slack)
            for t in tiers:
                r["pc"][t.name] = Pieces(job, t, offs, floor, None)
            r["h0"] = dl.h0_price(job, offs, dl.H0)
        # the offered flexibility (full pause, every offer): sum of p H P per job; the slack-limited supply (Q-b's reference)
        r["offered"] = sum((of.p * of.H for of in offs), ZERO) * P_JOB
        r["slack_ref"] = run_policy(job, dl.OWN, offs, lambda k, n, L, m=dl.Model(job, dl.OWN), o=offs: m.met(n + 1, L + m.heff(o[k].H)))
        out["rows"].append(r)
    out["tiers"] = tiers
    return out


def score(cell: dict) -> dict:
    rows = cell["rows"]
    comp = all(r["pc"][a].closed for r in rows for a in ("ETM", "OWN"))
    s = dict(computable=comp)
    qa_jobs = [r for r in rows if all(res["short"] == 0 and res["beyond"] == 0 for _, _, res in r["pc"]["ETM"].above())]
    qb_short = [r for r in rows if any(res["short"] > 0 for _, _, res in r["pc"]["OWN"].above())]
    qb_beyond = [r for r in rows if any(res["beyond"] > 0 for _, _, res in r["pc"]["OWN"].above())]
    s["qa_n"] = len(qa_jobs)
    s["qb_short_n"] = len(qb_short)
    s["qb_beyond_n"] = len(qb_beyond)
    s["qa"] = comp and s["qa_n"] == len(rows)
    s["qb_while"] = comp and s["qb_short_n"] == 0
    s["qb_only"] = comp and s["qb_beyond_n"] == 0
    s["qb"] = s["qb_while"] and s["qb_only"]
    s["holds"] = s["qa"] and s["qb"]
    ab = [first_bad(r["pc"]["OWN"], "beyond") for r in rows]
    ab = [p for p in ab if p is not None]
    s["abandon"] = min(ab, key=lambda p: (p[0], not p[1])) if ab else None
    et = [first_bad(r["pc"]["ETM"], "short") for r in rows]
    et = [p for p in et if p is not None]
    s["etm_short_at"] = min(et, key=lambda p: (p[0], not p[1])) if et else None
    return s


def fleet_curve(cell: dict, arm: str):
    """The exact fleet supply curve of the arm over pi >= 0: merged runs of pieces with equal (fleet MWh, jobs meeting their
    deadline, expected events)."""
    rows = cell["rows"]
    pts = sorted({b for r in rows for b in r["pc"][arm].base})
    segs = []
    for i, b in enumerate(pts):
        nxt = pts[i + 1] if i + 1 < len(pts) else None
        for inc, pi in ((True, b), (False, (b + nxt) / 2 if nxt is not None else b + 2)):
            res = [r["pc"][arm].at_pi(pi) for r in rows]
            v = (sum((x["MWh"] for x in res), ZERO), sum((x["p_met"] for x in res), ZERO))
            segs.append(((b, inc), (b, True) if inc else (nxt, False), v))
    merged = []
    for lo, hi, v in segs:
        if merged and merged[-1][2] == v:
            merged[-1][1] = hi
        else:
            merged.append([lo, hi, v])
    return merged


def seg_txt(lo, hi) -> str:
    (a, ai), (b, bi) = lo, hi
    left = "[" if ai else "("
    if b is None:
        return f"{left}{float(a):.6f}, inf)"
    if a == b and ai and bi:
        return f"[{float(a):.6f}]"
    return f"{left}{float(a):.6f}, {float(b):.6f}{']' if bi else ')'}"


def h0_curve(cell: dict):
    rows = cell["rows"]
    prices = sorted({r["h0"] for r in rows if r["h0"] is not None})
    out = []
    for p in prices:
        n = sum(int(r["h0"] is not None and r["h0"] <= p) for r in rows)
        out.append((p, n))
    return out


# ------------------------------------------------------------------------------------------------ main
def main() -> int:
    print(f"DR1 check H8: the value to the grid, curtailable MW-hours per season under each arm's minimum payment, at a price grid "
          f"(Grid_Demand_Response/DECLARATION.md section 2, declared at {dl.DECL_AT})")
    print("Declared Q: at every payment above R/H, ETM supplies all the flexibility; OWN supplies it only while slack lasts.")
    print("Declared forecast: Q holds.  Rung R4 (synthetic model); a note, not evidence (R8).")
    print()
    f_phx, f_flex, f_dfs, f_kok = (quote_found(Q_PHX, Q_PHX_FILE), quote_found(Q_FLEX, Q_FLEX_FILE), quote_found(Q_DFS, Q_DFS_FILE),
                                   quote_found(Q_KOK, Q_KOK_FILE))
    total, months, days, lam_dfs = dfs_rate()
    R_k, S_k = kok_overheads()
    print("INPUTS")
    print("  DECLARED W = 1000 compute-hours per job, value 1 per compute-hour at completion (section 2 adopts EPS2 T1's units)")
    print("  ASSUMED  R = 0.1 h restart overhead per pause event (EPS2 T1 model constant; docs/citations/eps2_2026-09-29.md, Reading (T1):")
    print("           'no fetched source supplies or contradicts that number'); S = 0 (save time), lost = 0 (EPS2 T1 has neither)")
    print("  ASSUMED  the fleet: 100 jobs of 1 MW each (DECLARATION.md section 3: 'A hypothetical AI training fleet of 100 MW (ASSUMED),")
    print("           running jobs of the H3 portfolio'); the H3 portfolio's slack D - W = 5 i h, i = 1..100 (H3's ASSUMED spread; no")
    print("           fetched source gives a distribution of training-job deadline slack); power drawn while paused 0 (EPS2 T1)")
    print(f"  SOURCED  H = 3 h: {Q_PHX_SRC}, docs/citations/{Q_PHX_FILE}; quote found verbatim in the dossier: {dl.yn(f_phx)}:")
    print(f"           \"{Q_PHX}\"")
    print("  ASSUMED  H = 1 h and H = 4 h (EPS2 T1's event lengths)")
    print("  CHOICE   the season: one offer every 24 wall hours at hours 24..984 (K = 41), the same offers to every job, made with")
    print("           certainty (p = 1; EPS2 T1's schedule); 'per season' = these 41 offers. Spacing 12 and 48 h and Poisson offers are")
    print("           sensitivities (not scored)")
    print(f"  SOURCED  TIER contracts x in {{10, 25, 50}} % over a window w in {{3, 6}} h: docs/citations/{Q_FLEX_FILE}, {Q_PHX_SRC}; quote")
    print(f"           found verbatim in the dossier: {dl.yn(f_flex)}: \"{Q_FLEX}\" (w = 3 and 6: CHOICE, the two ends of the")
    print("           sourced period); TIER's performance-power curve linear (drlib's default): ASSUMED; throttle overhead 0: ASSUMED")
    print("  ASSUMED  payment grid pi in {0.01, 0.02, 0.05, 0.2, 0.5, 2, 5, 10, 20} per curtailed fleet-hour (EPS2 T1), plus R/H of the cell;")
    print("           the scored reading is exact over every payment, not only the grid")
    print(f"  SOURCED  (sensitivity only) Poisson rate lambda_DFS: {Q_DFS_SRC}, docs/citations/{Q_DFS_FILE}; quote found verbatim: {dl.yn(f_dfs)}:")
    print(f"           \"{Q_DFS}\"")
    print(f"           events by month {', '.join(f'{m} {n}' for m, n in months)} (sum {sum(int(n) for _, n in months)}), total {total}; over "
          f"December 2024 - March 2025 = {days} days (CHOICE, as H1) -> lambda_DFS = {total} / ({days} x 24) = {lam_dfs} per wall hour")
    print(f"  SOURCED  (sensitivity only) R = {R_k} h and S = {S_k} h: {Q_KOK_SRC}, docs/citations/{Q_KOK_FILE}; quote found verbatim: "
          f"{dl.yn(f_kok)}:")
    print(f"           \"{Q_KOK}\" (the paper's modelling assumption for its clusters, not a measured pause)")
    print("  ASSUMED  (sensitivity only) slack spreads 1 i, 0.05 i and 10 i h (H3's sensitivity spreads)")
    print()
    print("CHOICES")
    print("  C1 arms (drlib): WALL values the job on the wall clock, wall-clock deadline; OWN on its own steps, wall-clock deadline; ETM")
    print("     a lossless pause with the deadline in own steps (W + n (R + S) <= D); TIER throttles to throughput 1 - x for min(H, w)")
    print("     hours of an event (no checkpoint, own-clock valuation, wall-clock deadline); H0 enrols for the whole season when its")
    print("     payments cover its opportunity cost (ties enrol) and then curtails every offer. WALL, OWN, ETM and each TIER decide every")
    print("     offer by exact backward induction on valuation plus payments (ties accept), the rest of the season at the same flat pi;")
    print("     a job may let its deadline pass.")
    print("  C2 'each arm's minimum payment' = the x* rule: at each offer state the job accepts iff pi > x*, or pi == x* and accepting is")
    print("     optimal there (x* exact from drlib's convex piecewise-linear value functions). Where every acceptance region is")
    print("     [x*, inf) ('closed'), the job's season depends on pi only through its order against the job's distinct x* values, so")
    print("     the season's curtailed MWh is an exact step function of pi; each piece (each x* value, each open interval between")
    print("     consecutive values, the interval above the largest) is evaluated once. 'At every payment above R/H' is scored on every")
    print("     piece lying above R/H: exact over the whole continuum, not only the grid. The x* rule is checked against backward")
    print("     induction (drlib.solve / play) at every grid payment for every arm, job and cell. Q is not computable in a cell where a")
    print("     job's ETM or OWN acceptance region is not closed.")
    print("  C3 'curtailable MW-hours per season' = the fleet's curtailed energy over the season's offers: sum over jobs of the curtailed")
    print("     fleet-hours x 1 MW (a full pause curtails H fleet-hours per event; a TIER x min(H, w) with the linear curve). 'The")
    print("     flexibility' = every offer to every job curtailed by a full pause: 100 jobs x K x H MWh.")
    print("  C4 Q-a ('ETM supplies all the flexibility'): for every job, at every payment above R/H (floor = rate (R + S)/H), ETM accepts")
    print("     every offer it is running for (the reference 'accept all'); equivalently the fleet's ETM MWh equal the flexibility.")
    print("  C5 Q-b ('OWN supplies it only while slack lasts'): for every job, at every payment above R/H, OWN accepts an offer iff one")
    print("     more event still meets its wall-clock deadline (the reference 'accept while the slack lasts'), so it supplies")
    print("     min(K, nmax) events and meets its deadline. Two parts, both scored: 'while' (no offer declined while the slack lasts) and")
    print("     'only' (no offer accepted once the slack is spent: no job gives up its deadline to supply more). The lowest payment at")
    print("     which some job's OWN supplies beyond its slack is printed.")
    print("  C6 Q holds in a cell iff Q-a and both parts of Q-b hold for every job on every piece above R/H; Q holds iff it holds in every")
    print("     scored cell (H = 1, 3, 4); Q is not computable if any cell is not computable. WALL, TIER and H0 are printed (not in Q).")
    print("  C7 the gate: G-ZERO = ETM's one-event stake minus rate (R + S) is exactly 0 at every event count n = 0..K-1 of every job in")
    print("     every scored cell, and ETM's x* == rate (R + S)/H at every offer state; G-NEG = with no events offered (K = 0), for every")
    print("     job of every portfolio run here (scored and sensitivity spreads), every H and every grid pi, ETM not ahead of WALL by")
    print("     more than 1 % (harness rel) on any outcome: per job curtailed MWh, payments, valuation, fleet value, completion hour")
    print("     (earlier is ahead), deadline met; fleet totals MWh, payments, jobs meeting their deadline. G-POS is H1's; not printed.")
    print("  C8 H3's pinned output (Grid_Demand_Response/checks/dr_h3.txt, second reading) was seen before these choices were fixed; it")
    print("     shows OWN's grid supply rising above the slack-limited level at pi = 10 and 20 for H = 3 and 4. C5 is the literal reading")
    print("     of 'only while slack lasts' and was not chosen for its outcome.")
    print()

    # ------------------------------------------------------------------------------------------------ the scored cells
    jobs = portfolio(SLACK_STEP)
    cells = {}
    for H in HS:
        offs = dl.every(SPACING, H, W)
        cells[H] = run_cell(jobs, H, offs, True)
    scores = {H: score(c) for H, c in cells.items()}

    print("PER-EVENT ARITHMETIC (drlib.event: curtailed fleet-hours e, charge c on the arm's valuation, deadline budget used; job J001)")
    for H in HS:
        parts = []
        for a in [dl.WALL, dl.OWN, dl.ETM] + cells[H]["tiers"]:
            ev = dl.event(jobs[0], a, H)
            parts.append(f"{a.name} e {dl.g(ev['e'])} c {dl.g(ev['charge'])} use {dl.g(ev['deadline_use'])}")
        print(f"  H = {dl.g(H)} (R/H = {f(R / H)}): " + "; ".join(parts))
    print()

    # ---- DP = x* rule at the grid
    print("CHECK OF THE x* RULE AGAINST BACKWARD INDUCTION (every grid pi and R/H, every job, cell and arm): per arm, states where")
    print("accepts_at(x*, pi) equals solve()'s decision, and jobs whose play() events and MWh equal the piecewise evaluation")
    ver_ok = True
    for H in HS:
        c = cells[H]
        pis = sorted(set(GRID) | {c["floor"]})
        parts = []
        for arm in [dl.WALL, dl.OWN, dl.ETM] + c["tiers"]:
            st_ok = st_n = pl_ok = pl_n = 0
            for r in c["rows"]:
                pc = r["pc"][arm.name]
                for pi in pis:
                    sol = dl.solve(r["job"], arm, c["offs"], pi)
                    st_n += len(pc.xs)
                    st_ok += sum(int(dl.accepts_at(x, pi) == sol.dec[s]) for s, x in pc.xs.items())
                    pl = dl.play(r["job"], arm, c["offs"], pi, P_JOB, sol=sol)
                    ev = pc.at_pi(pi)
                    pl_n += 1
                    pl_ok += int(pl["events"] == ev["events"] and pl["MWh"] == ev["MWh"] and pl["met"] == (ev["p_met"] == 1))
            ver_ok = ver_ok and st_ok == st_n and pl_ok == pl_n
            parts.append(f"{arm.name} {st_ok}/{st_n} states, {pl_ok}/{pl_n} plays")
        print(f"  H = {dl.g(H)}: " + "; ".join(parts))
    print(f"  the x* rule reproduces backward induction everywhere checked: {dl.yn(ver_ok)}")
    print()

    # ---- per-job tables
    print("PER-JOB TABLES (scored). Per job: slack D - W (h); nmax = events the arm's deadline absorbs (K offers); ref = min(K, nmax OWN),")
    print("the slack-limited events (Q-b's reference); p_all per arm = the minimum flat payment at which the job accepts every offer")
    print("of the season; ETM ok = Q-a holds for the job on every piece above R/H; OWN first = OWN's events on the first")
    print("interval above R/H; OWN beyond at = the lowest payment above R/H at which OWN supplies beyond its slack ('>' = just above);")
    print("short/beyond = pieces above R/H with a declined offer while slack lasts / an accepted offer once slack is spent;")
    print("closed = every ETM and OWN acceptance region is [x*, inf); H0 = the interruptible-load reservation price")
    for H in HS:
        c = cells[H]
        print(f"  cell H = {dl.g(H)} (K = {c['K']}, R/H = {f(c['floor'])}, flexibility per job {dl.g(c['rows'][0]['offered'])} MWh):")
        print(f"    {'job':5} {'slack':>6} {'nmax W/O/E':>13} {'ref':>4} {'p_all ETM':>10} {'ETM ok':>6} {'p_all OWN':>12} {'OWN first':>9} "
              f"{'OWN beyond at':>14} {'short':>5} {'beyond':>6} {'p_all WALL':>12} {'H0':>10} {'closed':>6}")
        for r in c["rows"]:
            pe, po = r["pc"]["ETM"], r["pc"]["OWN"]
            nm = "/".join("inf" if r["nm"][a] is None else str(r["nm"][a]) for a in ("WALL", "OWN", "ETM"))
            ref_ev = r["slack_ref"]["events"]
            ab = pe.above()
            etm_ok = all(res["short"] == 0 and res["beyond"] == 0 for _, _, res in ab)
            oa = po.above()
            first = oa[0][2]["events"] if oa else None
            nshort = sum(int(res["short"] > 0) for _, _, res in oa)
            nbey = sum(int(res["beyond"] > 0) for _, _, res in oa)
            print(f"    {r['job'].name:5} {dl.g(r['job'].slack):>6} {nm:>13} {dl.g(ref_ev):>4} {f(pe.pa.x):>10} {dl.yn(etm_ok):>6} "
                  f"{f(po.pa.x):>12} {dl.g(first) if first is not None else '-':>9} {fmt_pt(first_bad(po, 'beyond')):>14} {nshort:>5} "
                  f"{nbey:>6} {f(r['pc']['WALL'].pa.x):>12} {f(r['h0']):>10} {dl.yn(pe.closed and po.closed):>6}")
        print(f"    TIER entry prices p_all (per curtailed fleet-hour) and events accepted just above R/H, per tier:")
        for t in c["tiers"]:
            pas = [r["pc"][t.name].pa for r in c["rows"]]
            kinds = sorted({p.kind for p in pas})
            xs_ = sorted({p.x for p in pas if p.kind == "threshold"})
            evs = [r["pc"][t.name].just_above()["events"] for r in c["rows"]]
            ev = dl.event(jobs[0], t, H)
            print(f"      {t.name:8} e per event {dl.g(ev['e'])} fleet-hours (of {dl.g(H)}), wall delay {dl.g(ev['wall_delay'])} h; p_all kinds "
                  f"{'/'.join(kinds)}, {len(xs_)} distinct thresholds {f(xs_[0]) if xs_ else '-'}..{f(xs_[-1]) if xs_ else '-'}; jobs accepting "
                  f"all {c['K']} offers just above R/H: {sum(int(e == c['K']) for e in evs)} of {N_JOBS}; closed "
                  f"{sum(int(r['pc'][t.name].closed) for r in c['rows'])} of {N_JOBS}")
    print()

    # ---- the value table at the grid
    print("VALUE TO THE GRID AT THE PRICE GRID (scored cells; fleet of 100 x 1 MW; one season of K offers). Per pi: the flexibility")
    print("(MWh), each arm's curtailed MWh, ETM's and OWN's share of the flexibility, OWN's slack-limited MWh (Q-b's reference), and")
    print("the jobs meeting their deadline (on the arm's contract)")
    for H in HS:
        c = cells[H]
        pis = sorted(set(GRID) | {c["floor"]})
        flex = sum((r["offered"] for r in c["rows"]), ZERO)
        slack_mwh = sum((r["slack_ref"]["MWh"] for r in c["rows"]), ZERO)
        names = ["WALL", "OWN", "ETM"] + [t.name for t in c["tiers"]]
        print(f"  cell H = {dl.g(H)}: flexibility {dl.g(flex)} MWh; OWN's slack-limited supply {dl.g(slack_mwh)} MWh")
        print(f"    {'pi':>9} " + " ".join(f"{n:>9}" for n in names + ["H0"]) + f" {'ETM share':>9} {'OWN share':>9}   met W/O/E/H0")
        for pi in pis:
            vals = {n: sum((r["pc"][n].at_pi(pi)["MWh"] for r in c["rows"]), ZERO) for n in names}
            mets = {n: sum((r["pc"][n].at_pi(pi)["p_met"] for r in c["rows"]), ZERO) for n in ("WALL", "OWN", "ETM")}
            h0p = [dl.play(r["job"], dl.H0, c["offs"], pi, P_JOB) for r in c["rows"]]
            vals["H0"] = sum((x["MWh"] for x in h0p), ZERO)
            mets["H0"] = sum(int(x["met"]) for x in h0p)
            print(f"    {f(pi, 4):>9} " + " ".join(f"{float(vals[n]):>9.1f}" for n in names + ["H0"])
                  + f" {f(vals['ETM'] / flex, 4):>9} {f(vals['OWN'] / flex, 4):>9}   "
                  + "/".join(dl.g(mets[n]) for n in ("WALL", "OWN", "ETM", "H0")))
        print(f"    payments to the fleet (pi x MWh) at each grid pi, ETM / OWN / WALL: " + "; ".join(
            f"{dl.g(pi)}: {float(pi * sum((r['pc']['ETM'].at_pi(pi)['MWh'] for r in c['rows']), ZERO)):.1f} / "
            f"{float(pi * sum((r['pc']['OWN'].at_pi(pi)['MWh'] for r in c['rows']), ZERO)):.1f} / "
            f"{float(pi * sum((r['pc']['WALL'].at_pi(pi)['MWh'] for r in c['rows']), ZERO)):.1f}" for pi in pis))
    print()

    # ---- the exact fleet supply curves
    print("EXACT FLEET SUPPLY CURVES (scored cells): per arm, the season's curtailed MWh and the jobs meeting their deadline as a step")
    print("function of the flat payment pi >= 0 (runs of equal value merged; '[a]' the single payment a)")
    for H in HS:
        c = cells[H]
        flex = sum((r["offered"] for r in c["rows"]), ZERO)
        print(f"  cell H = {dl.g(H)} (flexibility {dl.g(flex)} MWh, R/H = {f(c['floor'])}):")
        for a in ["ETM", "OWN", "WALL"] + [t.name for t in c["tiers"]]:
            cur = fleet_curve(c, a)
            print(f"    {a:8} ({len(cur)} runs): " + "; ".join(f"{seg_txt(lo, hi)} {float(v[0]):.1f} MWh, {dl.g(v[1])} met" for lo, hi, v in cur))
        hc = h0_curve(c)
        print(f"    {'H0':8} ({len(hc)} entry prices; each enrolled job curtails {dl.g(c['rows'][0]['offered'])} MWh): "
              + "; ".join(f"from {f(p)} {n} jobs" for p, n in hc))
    print()

    # ---- scored Q per cell
    print("SCORED Q PER CELL (exact, every piece above R/H)")
    for H in HS:
        s = scores[H]
        if not s["computable"]:
            print(f"  H = {dl.g(H)}: not computable (an ETM or OWN acceptance region is not closed)")
            continue
        npieces_e = sum(len(r["pc"]["ETM"].above()) for r in cells[H]["rows"])
        npieces_o = sum(len(r["pc"]["OWN"].above()) for r in cells[H]["rows"])
        print(f"  H = {dl.g(H)}: Q-a jobs where ETM supplies every offer on every piece above R/H = {s['qa_n']} of {N_JOBS} ({npieces_e} job pieces) "
              f"-> Q-a {'holds' if s['qa'] else 'fails'}; lowest payment above R/H where some ETM job declines {fmt_pt(s['etm_short_at'])}")
        print(f"    Q-b ({npieces_o} job pieces): jobs declining an offer while slack lasts {s['qb_short_n']} -> 'while' {'holds' if s['qb_while'] else 'fails'}; "
              f"jobs supplying beyond their slack {s['qb_beyond_n']} -> 'only' {'holds' if s['qb_only'] else 'fails'}; lowest payment where "
              f"OWN supplies beyond its slack {fmt_pt(s['abandon'])} -> Q-b {'holds' if s['qb'] else 'fails'}")
        rng = ("every payment above R/H" if s["abandon"] is None else
               f"payments in (R/H, {float(s['abandon'][0]):.6f}{')' if s['abandon'][1] else ']'}")
        print(f"    Q-b's two parts both hold on {rng}")
        print(f"    cell: Q {'holds' if s['holds'] else 'fails'}")
    print()

    # ------------------------------------------------------------------------------------------------ sensitivities (not scored)
    sens_cells = []

    def sens_line(label, cell):
        s = score(cell)
        sens_cells.append(cell)
        flex = sum((r["offered"] for r in cell["rows"]), ZERO)
        slack_mwh = sum((r["slack_ref"]["MWh"] for r in cell["rows"]), ZERO)
        me = sum((r["pc"]["ETM"].just_above()["MWh"] for r in cell["rows"]), ZERO)
        mo = sum((r["pc"]["OWN"].just_above()["MWh"] for r in cell["rows"]), ZERO)
        if not s["computable"]:
            return f"{label}: not computable"
        return (f"{label}: Q-a {s['qa_n']} of {N_JOBS} jobs ({'holds' if s['qa'] else 'fails'}); Q-b while {s['qb_short_n']} short, only "
                f"{s['qb_beyond_n']} beyond, OWN beyond its slack from {fmt_pt(s['abandon'])} ({'holds' if s['qb'] else 'fails'}); just above "
                f"floor {f(cell['floor'], 4)}: flexibility {float(flex):.1f}, ETM {float(me):.1f}, OWN {float(mo):.1f} (slack-limited "
                f"{float(slack_mwh):.1f}) MWh -> Q {'holds' if s['holds'] else 'fails'}")

    print("SENSITIVITY 1 (not scored): offer spacing 12 and 48 h (EPS2's), the scored portfolio")
    for sp in SPACING_SENS:
        for H in HS:
            offs = dl.every(sp, H, W)
            print("  " + sens_line(f"spacing {dl.g(sp)} h, H {dl.g(H)} (K = {len(offs)})", run_cell(jobs, H, offs, False)))
    print()
    print("SENSITIVITY 2 (not scored): other slack spreads (ASSUMED, H3's), spacing 24 h")
    spread_jobs = {}
    for step, desc in SPREADS_SENS:
        js = portfolio(step)
        spread_jobs[desc] = js
        for H in HS:
            offs = dl.every(SPACING, H, W)
            print("  " + sens_line(f"{desc}, H {dl.g(H)}", run_cell(js, H, offs, False)))
    print()
    print("SENSITIVITY 3 (not scored): Poisson offers at lambda_DFS (SOURCED) with at most one event per 24 h slot (CHOICE); every")
    print("  quantity an exact expectation; Q-a/Q-b read on every reached made offer (probability mass of mismatches)")
    for H in HS:
        offs, err = dl.poisson_slots(lam_dfs, SLOT, H, W)
        print("  " + sens_line(f"lambda {lam_dfs}, p = {offs[0].p} (rounding error {err:.1e}), H {dl.g(H)}", run_cell(jobs, H, offs, False)))
    print()
    print(f"SENSITIVITY 4 (not scored): overheads R = {R_k} h and S = {S_k} h (SOURCED, Kokolis et al.); floor rate (R + S)/H")
    kjobs = portfolio(SLACK_STEP, R_k, S_k)
    for H in HS:
        offs = dl.every(SPACING, H, W)
        print("  " + sens_line(f"R + S = {R_k + S_k} h, H {dl.g(H)}", run_cell(kjobs, H, offs, False)))
    print()

    # ------------------------------------------------------------------------------------------------ Q
    comp = all(s["computable"] for s in scores.values())
    q_word = "not computable" if not comp else ("holds" if all(s["holds"] for s in scores.values()) else "fails")
    fc = {"holds": "right", "fails": "wrong", "not computable": "not decidable"}[q_word]
    nh = sum(int(s.get("holds", False)) for s in scores.values())
    qa_all = all(s.get("qa", False) for s in scores.values())
    qbw_all = all(s.get("qb_while", False) for s in scores.values())
    qbo_all = all(s.get("qb_only", False) for s in scores.values())
    ab_all = [s["abandon"] for s in scores.values() if s.get("abandon") is not None]
    ab_min = min(ab_all, key=lambda p: (p[0], not p[1])) if ab_all else None
    print(f"Q (scored): cells where Q holds {nh} of {len(scores)}; Q-a {'holds' if qa_all else 'fails'} in every cell: {dl.yn(qa_all)}; "
          f"Q-b 'while' in every cell: {dl.yn(qbw_all)}; Q-b 'only' in every cell: {dl.yn(qbo_all)} (lowest payment where some OWN job "
          f"supplies beyond its slack {fmt_pt(ab_min)}) -> Q {q_word}; the forecast 'Q holds' is {fc}")
    print()

    # ------------------------------------------------------------------------------------------------ the gate
    beyond, xs_n, xs_ok = [], 0, 0
    for H, c in cells.items():
        for r in c["rows"]:
            job = r["job"]
            beyond += [abs(dl.stake(job, dl.ETM, H, n) - job.rate * job.overhead) for n in range(c["K"])]
            xs = r["pc"]["ETM"].xs
            xs_n += len(xs)
            xs_ok += sum(int(x.kind == "threshold" and x.x == job.rate * job.overhead / H) for x in xs.values())
    gz = max(beyond) == 0 and xs_ok == xs_n
    # sensitivity cells (context, not gated)
    sb, sn, sok = [], 0, 0
    for c in sens_cells:
        H = c["H"]
        for r in c["rows"]:
            job = r["job"]
            sb += [abs(dl.stake(job, dl.ETM, H, n) - job.rate * job.overhead) for n in range(c["K"])]
            xs = r["pc"]["ETM"].xs
            sn += len(xs)
            sok += sum(int(x.kind == "threshold" and x.x == job.rate * job.overhead / H) for x in xs.values())
    sb_pos = sum(int(b > 0) for b in sb)

    ahead, maxrel, n_neg = [], ZERO, 0
    all_ports = [("scored", jobs)] + list(spread_jobs.items()) + [("Kokolis overheads", kjobs)]
    for _, js in all_ports:
        for H in HS:
            for pi in GRID:
                fw = [dl.play(j, dl.WALL, (), pi, P_JOB) for j in js]
                fe = [dl.play(j, dl.ETM, (), pi, P_JOB) for j in js]
                for rw, re_ in zip(fw, fe):
                    n_neg += 1
                    for k in ("MWh", "payments", "valuation", "fleet_value"):
                        ahead.append(re_[k] > rw[k] and relx(re_[k], rw[k]) > TOL)
                        maxrel = max(maxrel, relx(re_[k], rw[k]))
                    ahead.append(re_["completion"] < rw["completion"] and relx(re_["completion"], rw["completion"]) > TOL)
                    maxrel = max(maxrel, relx(re_["completion"], rw["completion"]))
                    ahead.append(re_["met"] and not rw["met"])
                for k in ("MWh", "payments"):
                    a_, b_ = sum((x[k] for x in fe), ZERO), sum((x[k] for x in fw), ZERO)
                    ahead.append(a_ > b_ and relx(a_, b_) > TOL)
                    maxrel = max(maxrel, relx(a_, b_))
                me, mw = Fr(sum(int(x["met"]) for x in fe)), Fr(sum(int(x["met"]) for x in fw))
                ahead.append(me > mw and relx(me, mw) > TOL)
                maxrel = max(maxrel, relx(me, mw))
    n_ahead = sum(int(b) for b in ahead)
    gn = n_ahead == 0

    battery = []
    for i in range(1, 8):
        p = CHECKS / f"dr_h{i}.txt"
        word = "missing"
        if p.exists():
            lines = [l for l in p.read_text(encoding="utf-8").splitlines() if l.startswith(f"RESULT H{i}:")]
            m = re.search(r"G-NEG (holds|FAILS)", lines[-1]) if lines else None
            word = m.group(1) if m else "unreadable"
        battery.append((f"H{i}", word))
    battery.append(("H8", "holds" if gn else "FAILS"))
    nb_hold = sum(int(w == "holds") for _, w in battery)

    print("GATE")
    print(f"  G-ZERO: ETM's stake beyond rate (R + S), max over {len(beyond)} (job, event count) pairs in {len(cells)} scored cells = "
          f"{f(max(beyond))} (exact {max(beyond)}); ETM's x* == rate (R + S)/H at {xs_ok} of {xs_n} offer states -> {'holds' if gz else 'FAILS'}")
    print(f"    context (sensitivity cells, not gated): stake beyond rate (R + S) positive at {sb_pos} of {len(sb)} (job, event count) pairs "
          f"(where ETM's own-step deadline cannot absorb the next event); x* == rate (R + S)/H at {sok} of {sn} offer states")
    print(f"  G-NEG (this check's own terms): no events offered (K = 0), {n_neg} job x portfolio x H x pi combinations over {len(all_ports)} "
          f"portfolios plus the fleet totals; ETM ahead of WALL by more than 1 % on {n_ahead} of {len(ahead)} outcome comparisons (per job: "
          f"curtailed MWh, payments, valuation, fleet value, completion, deadline met; fleet: MWh, payments, jobs meeting their deadline); "
          f"max rel over the numeric outcomes {f(maxrel)} -> {'holds' if gn else 'FAILS'}")
    print(f"  G-NEG over the whole battery (H1-H7 read from their pinned RESULT lines, not recomputed here; H8 as computed above): "
          + ", ".join(f"{h} {w}" for h, w in battery) + f" -> {nb_hold} of {len(battery)} hold")
    print()
    print("PRE-RUN NOTE: code-test runs on reduced portfolios (6 and 3 jobs, slack 40 i h, not pinned) preceded the first full run;")
    print("  after them only one table-header wording was changed (no input, choice, reading or threshold)")
    print("POST-FIRST-RUN CHANGES: " + ("none" if not POST_FIRST_RUN_CHANGES else "; ".join(POST_FIRST_RUN_CHANGES)))
    print()
    print(f"RESULT H8: Q {q_word}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - rate (R + S)| = {f(max(beyond))} over {len(beyond)} "
          f"(job, event count) pairs in {len(cells)} cells; ETM x* = (R + S)/H at {xs_ok} of {xs_n} offer states); G-NEG {'holds' if gn else 'FAILS'} "
          f"(no events: ETM ahead of WALL by more than 1 % in {n_ahead} of {len(ahead)} comparisons; battery H1-H8 per pinned RESULT lines: "
          f"{nb_hold} of {len(battery)} hold)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
