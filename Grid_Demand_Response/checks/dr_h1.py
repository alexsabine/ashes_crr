"""DR1 check H1: online offers arriving as a Poisson process of unknown count; each arm decides per offer.

Binding declaration: Grid_Demand_Response/DECLARATION.md (pushed at e67e8ee; never edited here), section 2, row H1:
  check:      online offers: events arrive as a Poisson process of unknown count; each arm decides per offer
  Q:          ETM's minimum acceptable payment is R/H at every offer; OWN's and WALL's rise as the slack falls
  forecast:   Q holds
This check also prints the gate's G-ZERO, G-NEG and G-POS (G-POS: OWN or WALL declines offers ETM accepts in at least one
cell of H1).

The arithmetic is the shared library Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; its selftest
reproduces EPS2 T1 line for line). Every verdict word printed here is computed from the numbers (R15). Every input number
is either sourced (a verbatim quote from a docs/citations/dr1_*_2026-09-29.md dossier, checked against the dossier text at
run time) or printed as ASSUMED; every modelling choice is printed as CHOICE. Rung R4 at most (synthetic model); a note,
not evidence (R8). Deterministic, stdlib only (via drlib).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h1.py > Grid_Demand_Response/checks/dr_h1.txt
"""
from __future__ import annotations

import datetime
import re
import sys
from fractions import Fraction as Fr
from math import comb
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as d  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CIT = REPO / "docs" / "citations"
ZERO, ONE = Fr(0), Fr(1)

# ------------------------------------------------------------------------------------------------ sourced inputs (quotes)
Q_DFS = ("Month Number of Events Bid Volume MWh Delivered Volume MWh Accuracy % of delivered vs bid volume December 6 326.5 "
         "244.8 66.69% January 8 1335.6 865.6 64.81% February 13 1839 1206.9 65.63% March 17 1948.6 1600.5 82.14% Total 44 "
         "5449.6 3917.7 71.90%")
Q_DFS_FILE = "dr1_f2_2026-09-29.md"
Q_DFS_SRC = "NESO, DFS winter 2024/25 report (published 3 July 2025)"
Q_KOK = "assuming Daly-Young optimal checkpointing with 5 minute restart overhead and 5 minute checkpoint write overhead."
Q_KOK_FILE = "dr1_f4_2026-09-29.md"
Q_KOK_SRC = "Kokolis et al., 'Revisiting Reliability in Large-Scale Machine Learning Research Clusters' (HPCA 2025, arXiv:2410.21680v2)"

# ------------------------------------------------------------------------------------------------ assumed inputs and choices
W = Fr(1000)                                   # DECLARED units (DR1 section 2 adopts EPS2 T1's)
RATE = ONE                                     # DECLARED units
DS = (Fr(1100), Fr(1500))                      # ASSUMED (EPS2 T1)
HS = (Fr(1), Fr(4))                            # ASSUMED (EPS2 T1)
R_EPS2 = Fr(1, 10)                             # ASSUMED (EPS2 T1)
LAMS_ASSUMED = (Fr(1, 240), Fr(1, 48), Fr(1, 12))   # ASSUMED Poisson rates per wall hour
SLOT = Fr(24)                                  # CHOICE: at most one event per 24 h slot (drlib's Poisson variant)
GRID = tuple(Fr(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))   # ASSUMED (EPS2 T1)
ARMS = (d.WALL, d.OWN, d.ETM)


def quote_found(quote: str, fname: str) -> bool:
    """The quote appears verbatim on one line of the dossier (a '> ' quote line)."""
    text = (CIT / fname).read_text(encoding="utf-8")
    return quote in text


def dfs_rate():
    """lambda_DFS = the 2024/25 DFS event count / the hours of the report's months December 2024 - March 2025."""
    months = re.findall(r"(December|January|February|March) (\d+) ", Q_DFS)
    total = int(re.search(r"Total (\d+) ", Q_DFS).group(1))
    days = (datetime.date(2025, 4, 1) - datetime.date(2024, 12, 1)).days
    return total, months, days, Fr(total, days * 24)


def kok_overheads():
    m = re.findall(r"(\d+) minute (restart overhead|checkpoint write overhead)", Q_KOK)
    vals = {k: Fr(int(v), 60) for v, k in m}
    return vals["restart overhead"], vals["checkpoint write overhead"]


def key(x: d.XStar):
    """Order of minimum acceptable payments: 'always' < any threshold < 'never'."""
    if x.kind == "always":
        return (-1, ZERO)
    if x.kind == "threshold":
        return (0, x.x)
    return (1, ZERO)


def xs_str(x: d.XStar) -> str:
    return f"{float(x.x):.6f}" if x.kind == "threshold" else x.kind


def binom_tail(K: int, p: Fr, j0: int) -> Fr:
    """P(more than j0 of K independent offers are made), each with probability p (exact)."""
    return sum((comb(K, j) * p ** j * (1 - p) ** (K - j) for j in range(j0 + 1, K + 1)), ZERO)


# ------------------------------------------------------------------------------------------------ one cell
def run_cell(job: d.Job, H: Fr, lam: Fr, slot: Fr = SLOT, grid=GRID, commercial=True) -> dict:
    offs, err = d.poisson_slots(lam, slot, H, job.W)
    K = len(offs)
    p = offs[0].p
    mf = [sum((o.p for o in offs[k + 1:]), ZERO) for k in range(K)]
    out = dict(job=job, H=H, lam=lam, slot=slot, offs=offs, err=err, K=K, p=p, Eoff=sum((o.p for o in offs), ZERO), arms={})
    target = job.rate * job.overhead / H      # ETM: c / e with c = rate (R + S), e = H (idle power 0)
    for arm in ARMS:
        m = d.Model(job, arm)
        F = d.value_fns(job, arm, offs)
        xs = d.xstar_all(job, arm, offs, F)
        pa = d.p_all(job, arm, offs, F)
        cf = sum(int(x.kind == "threshold" and x.x == d.rule_xstar(job, arm, H, n, mf[k])) for (k, n, L), x in xs.items())
        a = dict(xs=xs, pa=pa, cf=cf, nmax=d.nmax(job, arm, H))
        if commercial:
            sols = {pi: d.solve(job, arm, offs, pi) for pi in grid}
            a["agree"] = sum(int(d.accepts_at(x, pi) == sols[pi].dec[st]) for pi in grid for st, x in xs.items())
            a["exp"] = {pi: d.expect(job, arm, offs, pi, sol=sols[pi]) for pi in grid}
        # Q-b quantities: x* against the remaining deadline slack before the offer
        by_k = {}
        for (k, n, L), x in xs.items():
            s = job.D - job.W - m.g(n, L)
            by_k.setdefault(k, []).append((s, n, L, x))
        mono_pairs = mono_viol = binds = rises = lost = 0
        for k, lst in sorted(by_k.items()):
            he = m.heff(offs[k].H)
            pos = sorted((t for t in lst if t[0] >= 0), key=lambda t: -t[0])
            lost += sum(int(t[0] < 0) for t in lst)
            ks = [key(t[3]) for t in pos]
            mono_pairs += max(len(ks) - 1, 0)
            mono_viol += sum(int(b < a_) for a_, b in zip(ks, ks[1:]))
            zero = [t for t in pos if not m.met(t[1] + 1, t[2] + he)]
            full = [t for t in pos if t[1] == 0]
            if zero:
                binds += 1
                if full and all(key(z[3]) > key(full[0][3]) for z in zero):
                    rises += 1
        a.update(mono_pairs=mono_pairs, mono_viol=mono_viol, binds=binds, rises=rises, lost=lost,
                 n_states=len(xs))
        if arm is d.ETM:
            a["eq"] = sum(int(x.kind == "threshold" and x.x == target) for x in xs.values())
            a["closed"] = sum(int(x.closed) for x in xs.values())
            a["attained"] = sum(int(x.attained) for x in xs.values())
            a["stakes"] = [d.stake(job, arm, H, n) - job.rate * job.overhead for n in range(K)]
        out["arms"][arm.name] = a
    out["target"] = target
    out["h0"] = d.h0_price(job, offs)
    if commercial:
        out["h0exp"] = {pi: d.expect(job, d.H0, offs, pi) for pi in grid}
    nm_own = out["arms"]["OWN"]["nmax"]
    out["p_bind_own"] = binom_tail(K, p, nm_own) if nm_own is not None and nm_own < K else ZERO
    return out


def qa_ok(c) -> bool:
    e = c["arms"]["ETM"]
    return e["eq"] == e["n_states"] and e["closed"] == e["n_states"]


def qb_cell(c, strict_all: bool) -> bool:
    """Reading B (scored): for OWN and WALL, x* never falls as the slack falls (among states that can still meet the deadline),
    and at every offer where a zero-slack state is reachable x* there is strictly above x* at full slack.
    Reading A (strict_all): in addition, a zero-slack state must be reachable in the cell."""
    ok = True
    for a in ("OWN", "WALL"):
        r = c["arms"][a]
        ok &= r["mono_viol"] == 0 and r["rises"] == r["binds"]
        if strict_all:
            ok &= r["binds"] > 0
    return ok


# ------------------------------------------------------------------------------------------------ printing
def print_cell(cid: str, c: dict) -> None:
    job, H, K = c["job"], c["H"], c["K"]
    A = c["arms"]
    print(f"--- cell {cid}: D = {d.g(job.D)}, H = {d.g(H)}, R = {job.R} h, S = {job.S} h (overhead R + S = {job.overhead} h), "
          f"lambda = {c['lam']} per wall hour, slot {d.g(c['slot'])} h")
    print(f"    offers: {K} slots at hours {d.g(c['offs'][0].t)}..{d.g(c['offs'][-1].t)}, each made with p = {float(c['p']):.9f} "
          f"(rational {c['p']}, rounding error {c['err']:.1e}); E[offers] = {float(c['Eoff']):.6f}; "
          f"P(offers made > OWN's nmax {A['OWN']['nmax']}) = {float(c['p_bind_own']):.6e}")
    print(f"    nmax WALL {A['WALL']['nmax']}, OWN {A['OWN']['nmax']}, ETM {A['ETM']['nmax']}; target (R + S)/H = {c['target']} "
          f"= {float(c['target']):.6f}; ETM x* == target at {A['ETM']['eq']} of {A['ETM']['n_states']} states "
          f"(closed {A['ETM']['closed']}, attained {A['ETM']['attained']}); max |ETM stake - rate (R + S)| over n = 0..{K - 1} "
          f"= {float(max(abs(s) for s in A['ETM']['stakes'])):g}")
    for a in ("WALL", "OWN", "ETM"):
        r = A[a]
        extra = f"; DP = x* rule {r['agree']}/{r['n_states'] * len(GRID)}" if "agree" in r else ""
        pa = r["pa"]
        pa_s = f"{float(pa.x):.6f}" if pa.kind == "threshold" else pa.kind
        print(f"    {a:4}: x* == closed form rule_xstar at {r['cf']} of {r['n_states']} states{extra}; "
              f"x* falls as slack falls in {r['mono_viol']} of {r['mono_pairs']} adjacent pairs (slack >= 0); "
              f"offers with a zero-slack state {r['binds']}, strict rise there {r['rises']}; states past the deadline {r['lost']}; "
              f"p_all {pa_s}")
    print(f"    H0 reservation price (expected opportunity cost per expected curtailed hour): {float(c['h0']):.6f}")
    print(f"    Q-a (ETM x* = (R + S)/H at every offer state) {'holds' if qa_ok(c) else 'fails'}; "
          f"Q-b (OWN, WALL rise as slack falls; reading B) {'holds' if qb_cell(c, False) else 'fails'}; "
          f"reading A (a rise must occur in the cell) {'holds' if qb_cell(c, True) else 'fails'}")
    # x* by events accepted so far (the slack), min-max over the offers at which the state is reachable
    print(f"    x* by events accepted n (min-max over the offers k >= n at which (n, n H) is reached); runs of identical rows merged:")
    print(f"      {'n':>9} {'wall slack h':>17} {'own slack h':>17}  {'x* WALL':>21}  {'x* OWN':>21}  {'x* ETM':>19}")
    rows = []
    mW = d.Model(job, d.WALL)
    mE = d.Model(job, d.ETM)
    for n in range(K):
        cols = []
        for a in ("WALL", "OWN", "ETM"):
            vals = [x for (k, nn, L), x in A[a]["xs"].items() if nn == n]
            ths = sorted(x.x for x in vals if x.kind == "threshold")
            other = sorted({x.kind for x in vals if x.kind != "threshold"})
            s = (f"{float(ths[0]):.6f}" if ths[0] == ths[-1] else f"{float(ths[0]):.6f}-{float(ths[-1]):.6f}") if ths else ""
            if other:
                s = (s + "+" if s else "") + "/".join(other)
            cols.append(s)
        ws = job.D - job.W - mW.g(n, n * H)
        os_ = job.D - job.W - mE.g(n, n * H)
        rows.append((n, ws, os_, tuple(cols)))
    i = 0
    while i < len(rows):
        j = i
        while j + 1 < len(rows) and rows[j + 1][3] == rows[i][3]:
            j += 1
        n_s = f"{rows[i][0]}" if i == j else f"{rows[i][0]}..{rows[j][0]}"
        ws_s = f"{float(rows[i][1]):.2f}" if i == j else f"{float(rows[i][1]):.2f}..{float(rows[j][1]):.2f}"
        os_s = f"{float(rows[i][2]):.2f}" if i == j else f"{float(rows[i][2]):.2f}..{float(rows[j][2]):.2f}"
        cw, co, ce = rows[i][3]
        print(f"      {n_s:>9} {ws_s:>17} {os_s:>17}  {cw:>21}  {co:>21}  {ce:>19}")
        i = j + 1
    if "exp" in A["WALL"]:
        print("    expected outcome over the Poisson offers, optimal policy at each flat pi (E[events accepted] / P(deadline met on the arm's contract)):")
        print("      pi           " + " ".join(f"{d.g(p):>15}" for p in GRID))
        for a in ("WALL", "OWN", "ETM", "H0"):
            ex = c["h0exp"] if a == "H0" else A[a]["exp"]
            print(f"      {a:4} E[events] " + " ".join(f"{float(ex[p]['events']):>15.6f}" for p in GRID))
            print(f"      {a:4} P(met)    " + " ".join(f"{float(ex[p]['p_met']):>15.6f}" for p in GRID))
        print("      E[live offers]  " + " ".join(f"{float(A['ETM']['exp'][p]['live']):>15.6f}" for p in GRID))


def main() -> int:
    print("DR1 check H1: online offers, Poisson arrivals of unknown count, each arm decides per offer")
    print(f"Declaration: Grid_Demand_Response/DECLARATION.md (pushed at {d.DECL_AT}; binding, not edited). Library: drlib.py (exact rationals).")
    print("Declared Q: ETM's minimum acceptable payment is R/H at every offer; OWN's and WALL's rise as the slack falls. Forecast: Q holds.")
    print()
    # ---------------------------------------------------------------- inputs
    total, months, days, lam_dfs = dfs_rate()
    R_k, S_k = kok_overheads()
    f_dfs, f_kok = quote_found(Q_DFS, Q_DFS_FILE), quote_found(Q_KOK, Q_KOK_FILE)
    print("INPUTS")
    print(f"  SOURCED  Poisson rate lambda_DFS: {Q_DFS_SRC}, docs/citations/{Q_DFS_FILE}; quote found verbatim in the dossier: {d.yn(f_dfs)}:")
    print(f"           \"{Q_DFS}\"")
    print(f"           events by month {', '.join(f'{a} {b}' for a, b in months)} (sum {sum(int(b) for _, b in months)}), total {total}; "
          f"over the calendar months December 2024 - March 2025 = {days} days (CHOICE: the report's monthly table read as")
    print(f"           these four calendar months) -> lambda_DFS = {total} / ({days} x 24) = {lam_dfs} = {float(lam_dfs):.9f} per wall hour")
    print(f"  SOURCED  overheads R = {R_k} h and S = {S_k} h: {Q_KOK_SRC}, docs/citations/{Q_KOK_FILE}; quote found verbatim: {d.yn(f_kok)}:")
    print(f"           \"{Q_KOK}\"")
    print("           (5 minute restart overhead -> R = 1/12 h; 5 minute checkpoint write -> S = 1/12 h, the save before the power drops;")
    print("           the quote is the paper's own modelling assumption for its RSC clusters, not a measured pause)")
    print(f"  DECLARED W = {W} compute-hours, value {RATE} per compute-hour at completion (DR1 section 2 adopts EPS2 T1's units)")
    print(f"  ASSUMED  R = {R_EPS2} h, S = 0 (EPS2 T1's restart overhead; no save time in EPS2)")
    print(f"  ASSUMED  D in {{{', '.join(d.g(x) for x in DS)}}} h, H in {{{', '.join(d.g(x) for x in HS)}}} h (EPS2 T1's cells)")
    print(f"  ASSUMED  Poisson rates lambda in {{{', '.join(str(x) for x in LAMS_ASSUMED)}}} per wall hour (besides lambda_DFS)")
    print(f"  ASSUMED  payment grid pi in {{{', '.join(d.g(x) for x in GRID)}}} per curtailed fleet-hour (EPS2 T1)")
    print(f"  ASSUMED  (sensitivity only, not scored) D = 1002 h for the boundary cell; slots of 12 and 48 h")
    print()
    print("CHOICES")
    print("  CHOICE Poisson offers: arrivals at rate lambda per wall hour; at most one event per slot of 24 h (further arrivals in the slot")
    print("         are void; the event starts at the slot's start), so each slot carries an offer with p = 1 - exp(-lambda slot), independently;")
    print("         p is the best rational with denominator <= 10^6 and its rounding error is printed. The fleet knows lambda, not the count.")
    print("  CHOICE Slots at hours 24 k strictly before hour W = 1000 (EPS2's offer window: every arm is running at every slot).")
    print("  CHOICE Each arm decides per offer by exact backward induction on its valuation plus payments (ties accept), the rest of the")
    print("         season played optimally at the same flat pi; x* (the minimum acceptable payment) is the start of the final acceptance")
    print("         interval in pi at the state, computed exactly from the convex piecewise-linear value functions (drlib.xstar_all).")
    print("  CHOICE 'At every offer' = at every reachable offer state (k, n, L) of every scored cell; Q-a needs")
    print("         x* == rate (R + S)/H there with an acceptance region [x*, inf) (closed). (R + S)/H is R/H when S = 0: the save time")
    print("         counts as own hours without progress, added to R (drlib's CHOICE).")
    print("  CHOICE 'The slack' = the arm's remaining deadline budget before the offer, D - W - (wall delay so far) for WALL and OWN,")
    print("         D - W - n (R + S) for ETM. 'Rise as the slack falls' (reading B, scored) = for OWN and for WALL, in every cell: among")
    print("         the states that can still meet the deadline (slack >= 0), at each offer x* never falls as the slack falls, and at every")
    print("         offer where a zero-slack state (one more event misses the deadline) is reachable, x* there is strictly above x* at")
    print("         full slack (n = 0); at least one scored cell must reach a zero-slack state, else Q-b is not computable. States past")
    print("         the deadline (slack < 0: the job is already lost) are not part of 'as the slack falls'; they are counted and printed.")
    print("         Reading A (printed, not scored) also requires a zero-slack state to be reachable in every cell.")
    print("  CHOICE Scored grid: EPS2 T1's cells (D x H) x the rates x the two overhead settings above. Sensitivity (printed,")
    print("         not scored): slots of 12 and 48 h at lambda_DFS; a boundary cell where ETM's own-step slack is smaller than the")
    print("         season's possible overheads (D = 1002 h).")
    print("  CHOICE H0 (an interruptible-load contract covering every made offer) is printed for context (its reservation price = expected")
    print("         opportunity cost / expected curtailed hours); TIER is not part of H1 (H2 checks it).")
    print("  CHOICE G-POS per (cell, pi): OWN's or WALL's expected accepted events strictly below ETM's (exact rationals). G-ZERO: ETM's")
    print("         one-event stake minus rate (R + S) at every event count n = 0..K-1 of every scored cell, exactly 0. G-NEG: with no events")
    print("         offered (K = 0, and each cell's realisation with no arrival), ETM not ahead of WALL by more than 1 % (harness rel) on")
    print("         any outcome: curtailed fleet-hours, payments, valuation, fleet value, deadline met, completion hour (earlier is ahead).")
    print()

    # ---------------------------------------------------------------- scored grid
    ovs = (("A", R_EPS2, ZERO, "ASSUMED EPS2"), ("K", R_k, S_k, "SOURCED Kokolis"))
    lams = (("dfs", lam_dfs),) + tuple((f"a{i + 1}", x) for i, x in enumerate(LAMS_ASSUMED))
    cells = {}
    print("PER-CELL TABLES (scored grid)")
    for oid, R, S, _ in ovs:
        for D in DS:
            for H in HS:
                for lid, lam in lams:
                    cid = f"{oid}-D{d.g(D)}-H{d.g(H)}-{lid}"
                    c = run_cell(d.Job(W, D, R, S=S), H, lam)
                    cells[cid] = c
                    print_cell(cid, c)
    print()

    # ---------------------------------------------------------------- summary table
    print("SUMMARY (one row per scored cell)")
    hdr = (f"  {'cell':22} {'K':>3} {'p':>9} {'E[off]':>8} {'nmaxO':>5} {'ETM x*=t':>11} {'OWN x* lo-hi (slack>=0)':>25} "
           f"{'WALL x* lo-hi (slack>=0)':>25} {'bindO':>5} {'riseO':>5} {'bindW':>5} {'riseW':>5} {'Q-a':>5} {'Q-b':>5} {'Q-bA':>5}")
    print(hdr)
    for cid, c in cells.items():
        A = c["arms"]
        rng = {}
        for a in ("OWN", "WALL"):
            m = d.Model(c["job"], getattr(d, a))
            v = [x.x for (k, n, L), x in A[a]["xs"].items() if x.kind == "threshold" and c["job"].D - c["job"].W - m.g(n, L) >= 0]
            rng[a] = f"{float(min(v)):.6f}-{float(max(v)):.6f}"
        print(f"  {cid:22} {c['K']:>3} {float(c['p']):>9.6f} {float(c['Eoff']):>8.4f} {A['OWN']['nmax']:>5} "
              f"{A['ETM']['eq']:>5}/{A['ETM']['n_states']:<5} {rng['OWN']:>25} {rng['WALL']:>25} {A['OWN']['binds']:>5} {A['OWN']['rises']:>5} "
              f"{A['WALL']['binds']:>5} {A['WALL']['rises']:>5} {('holds' if qa_ok(c) else 'fails'):>5} "
              f"{('holds' if qb_cell(c, False) else 'fails'):>5} {('holds' if qb_cell(c, True) else 'fails'):>5}")
    print("  (ETM x*=t: states where ETM's x* equals (R + S)/H; bind/rise: offers with a reachable zero-slack state / with a strict rise there)")
    print()

    # ---------------------------------------------------------------- sensitivity
    print("SENSITIVITY (printed, not scored)")
    sens = {}
    for sl in (Fr(12), Fr(48)):
        c = run_cell(d.Job(W, Fr(1100), R_EPS2), Fr(4), lam_dfs, slot=sl, commercial=False)
        sens[f"slot{d.g(sl)}"] = c
        print_cell(f"S-slot{d.g(sl)}-D1100-H4-dfs", c)
    cb = run_cell(d.Job(W, Fr(1002), R_EPS2), Fr(4), Fr(1, 12), commercial=False)
    sens["boundary"] = cb
    print_cell("S-boundary-D1002-H4-a3", cb)
    eb = cb["arms"]["ETM"]
    print(f"  boundary: ETM's own-step slack absorbs {eb['nmax']} events of overhead {cb['job'].overhead} h against up to {cb['K']} offers; "
          f"ETM x* == R/H at {eb['eq']} of {eb['n_states']} states; max |ETM stake - rate R| = {float(max(abs(s) for s in eb['stakes'])):g}; "
          f"Q-a {'holds' if qa_ok(cb) else 'fails'} there (the overhead still counts against the own-step deadline)")
    for k_, c in sens.items():
        print(f"  {k_}: Q-a {'holds' if qa_ok(c) else 'fails'}, Q-b (reading B) {'holds' if qb_cell(c, False) else 'fails'}, "
              f"reading A {'holds' if qb_cell(c, True) else 'fails'}")
    print()

    # ---------------------------------------------------------------- Q
    n_cells = len(cells)
    qa_n = sum(int(qa_ok(c)) for c in cells.values())
    qb_n = sum(int(qb_cell(c, False)) for c in cells.values())
    qbA_n = sum(int(qb_cell(c, True)) for c in cells.values())
    bind_cells = sum(int(c["arms"]["OWN"]["binds"] > 0 and c["arms"]["WALL"]["binds"] > 0) for c in cells.values())
    etm_states = sum(c["arms"]["ETM"]["n_states"] for c in cells.values())
    etm_eq = sum(c["arms"]["ETM"]["eq"] for c in cells.values())
    mono_v = sum(c["arms"][a]["mono_viol"] for c in cells.values() for a in ("OWN", "WALL"))
    mono_p = sum(c["arms"][a]["mono_pairs"] for c in cells.values() for a in ("OWN", "WALL"))
    binds = sum(c["arms"][a]["binds"] for c in cells.values() for a in ("OWN", "WALL"))
    rises = sum(c["arms"][a]["rises"] for c in cells.values() for a in ("OWN", "WALL"))
    cf_ok = all(c["arms"][a]["cf"] == c["arms"][a]["n_states"] for c in cells.values() for a in ("WALL", "OWN", "ETM"))
    dp_ok = all(c["arms"][a]["agree"] == c["arms"][a]["n_states"] * len(GRID) for c in cells.values() for a in ("WALL", "OWN", "ETM"))
    qa = qa_n == n_cells
    if not qa or qb_n < n_cells:
        qv = "fails"
    elif bind_cells == 0:
        qv = "not computable"
    else:
        qv = "holds"
    qvA = "fails" if (not qa or qbA_n < n_cells) else "holds"
    print("Q")
    print(f"  internal checks: backward-induction x* equals the closed form rule_xstar at every state of every cell and arm: {d.yn(cf_ok)}; "
          f"'accept iff pi >= x*' equals the backward-induction decision at every state and grid pi: {d.yn(dp_ok)}")
    print(f"  Q-a: ETM's x* == (R + S)/H (closed) at {etm_eq} of {etm_states} offer states; cells where it holds at every state {qa_n} of {n_cells} "
          f"-> {'holds' if qa else 'fails'}")
    print(f"  Q-b (reading B): OWN's and WALL's x* falls as the slack falls in {mono_v} of {mono_p} adjacent state pairs; strict rise at "
          f"{rises} of {binds} offers with a zero-slack state; cells where both arms reach zero slack {bind_cells} of {n_cells}; "
          f"cells holding {qb_n} of {n_cells}")
    print(f"  Q (reading B, scored): {qv}; reading A (a rise required in every cell; not scored): {qvA} ({qbA_n} of {n_cells} cells)")
    print(f"  the investigator's forecast (Q holds) is {'right' if qv == 'holds' else 'wrong'}")
    print()

    # ---------------------------------------------------------------- gate
    stakes = [s for c in cells.values() for s in c["arms"]["ETM"]["stakes"]]
    gz = max(abs(s) for s in stakes) == 0 and qa
    pos = {"WALL": 0, "OWN": 0}
    combos = 0
    first = None
    for cid, c in cells.items():
        for pi in GRID:
            combos += 1
            ee = c["arms"]["ETM"]["exp"][pi]["events"]
            for a in ("WALL", "OWN"):
                ea = c["arms"][a]["exp"][pi]["events"]
                if ea < ee:
                    pos[a] += 1
                    if a == "OWN" and first is None:
                        first = (cid, pi, ea, ee)
    gp = pos["WALL"] + pos["OWN"] > 0
    # the largest shortfall in expected events, for scale
    short = max(((c["arms"]["ETM"]["exp"][pi]["events"] - c["arms"][a]["exp"][pi]["events"], cid, a, pi)
                 for cid, c in cells.items() for pi in GRID for a in ("WALL", "OWN")), key=lambda t: t[0])
    own_short = max(((c["arms"]["ETM"]["exp"][pi]["events"] - c["arms"]["OWN"]["exp"][pi]["events"], cid, pi)
                     for cid, c in cells.items() for pi in GRID), key=lambda t: t[0])
    print("GATE")
    print(f"  G-ZERO: max |ETM stake - rate (R + S)| over {len(stakes)} event counts in {n_cells} cells = {float(max(abs(s) for s in stakes)):g} "
          f"(exact); ETM's x* == (R + S)/H at {etm_eq} of {etm_states} states -> {'holds' if gz else 'FAILS'}")
    print(f"  G-POS: expected accepted events below ETM's: WALL in {pos['WALL']}, OWN in {pos['OWN']} of {combos} cell x pi combinations; "
          f"largest shortfall {float(short[0]):.6f} events ({short[2]}, {short[1]}, pi {d.g(short[3])}); OWN's largest {float(own_short[0]):.6f} "
          f"({own_short[1]}, pi {d.g(own_short[2])}) -> {'holds' if gp else 'FAILS'}")
    # G-NEG
    outcomes = (("curtailed fleet-hours", "fleet_hours", +1), ("payments", "payments", +1), ("valuation", "valuation", +1),
                ("fleet value", "fleet_value", +1), ("deadline met", "met", +1), ("completion hour", "completion", -1))
    worst = []
    n_cmp = 0
    ahead = 0
    for cid, c in cells.items():
        for pi in GRID:
            for label, offs, made in (("K = 0", (), None), ("no arrival", c["offs"], [False] * c["K"])):
                pe = d.play(c["job"], d.ETM, offs, pi, made=made)
                pw = d.play(c["job"], d.WALL, offs, pi, made=made)
                for name, fld, sgn in outcomes:
                    a_, b_ = float(pe[fld]), float(pw[fld])
                    r = d.rel(a_, b_)
                    better = (a_ > b_) if sgn > 0 else (a_ < b_)
                    n_cmp += 1
                    if better and r > 1e-2:
                        ahead += 1
                    worst.append((r, name, cid, label, a_, b_))
    wr = max(worst, key=lambda t: t[0])
    gn = ahead == 0
    ex = d.play(cells[next(iter(cells))]["job"], d.ETM, (), GRID[0])
    print(f"  G-NEG: no events offered (K = 0, and the no-arrival realisation of each cell), {n_cmp} comparisons of ETM against WALL on six outcomes; "
          f"ETM ahead by more than 1 % in {ahead}; largest rel {wr[0]:.3e} ({wr[1]}); e.g. ETM curtails {float(ex['fleet_hours']):g} h, completes at "
          f"{float(ex['completion']):g} h -> {'holds' if gn else 'FAILS'}")
    gate = "OPEN" if (gz and gp and gn) else "CLOSED"
    print(f"  gate (H1's G-ZERO, G-POS, G-NEG): {gate}")
    print()
    print(f"RESULT H1: Q {qv}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - rate (R + S)| = {float(max(abs(s) for s in stakes)):g} over "
          f"{len(stakes)} event counts in {n_cells} cells; ETM x* = (R + S)/H at {etm_eq} of {etm_states} offer states); "
          f"G-NEG {'holds' if gn else 'FAILS'} (ETM ahead of WALL by more than 1 % in {ahead} of {n_cmp} no-event comparisons); "
          f"G-POS {'holds' if gp else 'FAILS'} (expected events below ETM's: WALL in {pos['WALL']}, OWN in {pos['OWN']} of {combos} cell x pi; "
          f"OWN's largest shortfall {float(own_short[0]):.6f} events)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
