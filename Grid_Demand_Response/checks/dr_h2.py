"""DR1 check H2 (Grid_Demand_Response/DECLARATION.md section 2, pushed at e67e8ee; binding, never edited here):
ETM (the deadline-extension, stop-the-clock contract) against TIER contracts (maximum slowdown 10, 25 or 50 % over a 3-6 h
window), at matched job delay.

Declared prediction Q: at matched delay, ETM and the best tier supply the same curtailed energy within 1 % (ETM is an
unbounded tier). Declared forecast: Q holds (REDUNDANT in substance).

Arithmetic: Grid_Demand_Response/checks/drlib.py (exact rational arithmetic; selftest pinned in drlib_selftest.txt).
Every verdict word below is computed from the numbers (R15). Rung R4 (synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Grid_Demand_Response/checks/dr_h2.py > Grid_Demand_Response/checks/dr_h2.txt
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import drlib as dl  # noqa: E402

ZERO = Fr(0)
TOL = Fr(1, 100)                     # the declared 1 % (DECLARATION.md section 2, H2; and G-NEG's 1 %)

# ------------------------------------------------------------------------------------------------ inputs
W = dl.q(1000)                       # DECLARED (DR1 section 2 adopts EPS2 T1's units)
R = dl.q("0.1")                      # ASSUMED (EPS2 T1 model constant; no fetched source supplies R)
DS = (dl.q(1100), dl.q(1500))        # ASSUMED (EPS2 T1)
HS = (dl.q(1), dl.q(3), dl.q(4), dl.q(6))   # 1, 4 ASSUMED (EPS2 T1); 3 SOURCED (Phoenix event, 3 h); 6 CHOICE (top of the 3-6 h period)
SPACING = dl.q(24)                   # CHOICE (EPS2 T1: one offer every 24 wall hours at hours 24..984)
XS = (dl.q("0.10"), dl.q("0.25"), dl.q("0.50"))   # SOURCED (Flex 1-3)
WINDOWS = (dl.q(3), dl.q(6))         # SOURCED range "3-6 hour period"; CHOICE: its two ends
GRID = tuple(dl.q(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))  # ASSUMED (EPS2 T1)
R_SENS = (dl.q(0), dl.q("0.01"), dl.q("0.025"), dl.q("0.1"))   # ASSUMED sensitivity values (not scored)
PW_POINT = (dl.q("0.9"), dl.q("0.78"))   # SOURCED (POLCA, arXiv:2308.12908 v1: -10 % performance, -22 % peak server power)
PW_ORIGIN = (dl.q(0), dl.q(0))           # ASSUMED (the curve's lower end; a real GPU draws idle power at zero throughput)

POST_FIRST_RUN_CHANGES: list[str] = [
    "(1) sensitivity 2 printed the w = 3 tiers' slopes with the words 'w = 6 alike' written, not computed (R15); it now prints all six",
    "(2) the Q line now also prints the computed direction (breakpoints where ETM supplies less than the best tier); verdict unchanged",
    "(3) code tidy, no output change: the matched-delay table's 'feasible' column read through a redundant conditional",
]


def f(x, d=6) -> str:
    return "-" if x is None else f"{float(x):.{d}f}"


def relx(a: Fr, b: Fr) -> Fr:
    """The harness formula |a - b| / max(|a|, |b|), exactly (0 when both are 0)."""
    m = max(abs(a), abs(b))
    return ZERO if m == 0 else abs(a - b) / m


def tiers(power=dl.power_linear, tag=""):
    return [dl.tier(x, w, power=power, name=f"TIER-{int(x * 100)}%/{dl.g(w)}h{tag}") for x in XS for w in WINDOWS]


def frontier(job: dl.Job, arm: dl.Arm, H: Fr, K: int) -> dict:
    """The arm's season frontier of (job delay, curtailed energy): n accepted events, n = 0..n_use, where n_use is the most
    events that keep the arm's contract deadline (and at most K offers). Delay = wall-clock completion delay."""
    ev = dl.event(job, arm, H)
    nm = dl.nmax(job, arm, H)
    n_use = K if nm is None else min(K, nm)
    L_use = n_use * ev["h_eff"]
    ok_met = dl.met(job, arm, n_use, L_use)
    ok_edge = n_use == K or not dl.met(job, arm, n_use + 1, L_use + ev["h_eff"])
    d, e = ev["wall_delay"], ev["e"]
    return dict(arm=arm, ev=ev, e=e, d=d, slope=(None if d == 0 else e / d), nmax=nm, n_use=n_use,
                dmax=n_use * d, emax=n_use * e, consistent=ok_met and ok_edge)


def score_cell(job: dl.Job, H: Fr, K: int, tier_arms) -> dict:
    """Matched delay (CHOICE: the mean job delay of a fleet of identical jobs, so the frontier is the line through the origin
    and the n_use point; energy at delay Delta = slope * Delta while Delta <= dmax). At each Delta in (0, Delta_top], the best
    tier is the feasible tier (dmax >= Delta) supplying the most energy; rel(ETM, best) is constant between breakpoints, so it
    is evaluated at every breakpoint (each tier's dmax up to Delta_top, and Delta_top)."""
    fe = frontier(job, dl.ETM, H, K)
    ft = [frontier(job, a, H, K) for a in tier_arms]
    top_t = max(x["dmax"] for x in ft)
    top = min(fe["dmax"], top_t)
    rows = []
    if top > 0:
        bps = sorted({x["dmax"] for x in ft if 0 < x["dmax"] <= top} | {top})
        for D_ in bps:
            feas = [x for x in ft if x["dmax"] >= D_]
            best = max(feas, key=lambda x: x["slope"])          # first in order on ties
            Ee, Eb = fe["slope"] * D_, best["slope"] * D_
            rows.append(dict(delta=D_, n_etm=D_ / fe["d"], E_etm=Ee, best=best["arm"].name, E_best=Eb,
                             n_best=D_ / best["d"], rel=relx(Ee, Eb), feas=len(feas)))
    maxrel = max((r["rel"] for r in rows), default=None)
    return dict(fe=fe, ft=ft, top=top, rows=rows, maxrel=maxrel, within=(None if maxrel is None else maxrel <= TOL),
                reach=(None if max(x["emax"] for x in ft) == 0 else fe["emax"] / max(x["emax"] for x in ft)))


def discrete(sc: dict, K: int) -> list:
    """Sensitivity (not scored): one job, no fleet mixing. At each tier's own full-season point (n_use events, delay dmax_T),
    ETM takes the most whole events whose delay does not exceed dmax_T."""
    fe = sc["fe"]
    out = []
    for x in sc["ft"]:
        if x["dmax"] == 0:
            continue
        n = min(fe["n_use"], int(x["dmax"] // fe["d"]))
        out.append((x["arm"].name, x["dmax"], x["emax"], n, n * fe["d"], n * fe["e"], relx(n * fe["e"], x["emax"])))
    return out


def main() -> int:
    print(f"DR1 check H2: ETM (deadline extension) against TIER contracts at matched job delay "
          f"(Grid_Demand_Response/DECLARATION.md section 2, declared at {dl.DECL_AT})")
    print("Declared Q: at matched delay, ETM and the best tier supply the same curtailed energy within 1 % (ETM is an unbounded tier).")
    print("Declared forecast: Q holds (REDUNDANT in substance).  Rung R4 (synthetic model); a note, not evidence (R8).")
    print()
    print("INPUTS")
    print("  W = 1000 compute-hours, value 1 per compute-hour at completion: DECLARED (section 2 adopts EPS2 T1's units)")
    print("  R = 0.1 h restart overhead per pause event: ASSUMED (EPS2 T1 model constant; docs/citations/eps2_2026-09-29.md, Reading (T1):")
    print("    'no fetched source supplies or contradicts that number'); S = 0 (save time), lost = 0: ASSUMED (EPS2 T1 has neither)")
    print("  D in {1100, 1500} h: ASSUMED (EPS2 T1)")
    print("  H (event length) in {1, 3, 4, 6} h: 1 and 4 ASSUMED (EPS2 T1); 3 SOURCED (docs/citations/dr1_f1_2026-09-29.md, Colangelo et al.")
    print("    arXiv:2507.00909 v1: 'Each event required the cluster to reduce power by 25% [...] sustain the reduction for 3 hours'); 6 CHOICE")
    print("    (the top of the tiers' 3-6 h period)")
    print("  one offer every 24 wall hours at hours 24..984 (K = 41), made with certainty (p = 1): CHOICE (EPS2 T1's schedule)")
    print("  tiers x in {10, 25, 50} % over a window w in {3, 6} h: SOURCED (docs/citations/dr1_f1_2026-09-29.md, Colangelo et al. arXiv:2507.00909")
    print("    v1: 'Flex 1: up to 10% performance (average throughput) reduction allowed over a 3-6 hour period; (c) Flex 2: up to 25% allowed;")
    print("    (d) Flex 3: up to 50% allowed'); w = 3 and w = 6 are the two ends of the sourced period (CHOICE)")
    print("  performance-power curve for the throttle: linear, power fraction = throughput fraction: ASSUMED (drlib's default); scored")
    print("  power drawn while paused (ETM): 0 of full power: ASSUMED (EPS2 T1)")
    print("  payment grid {0.01, 0.02, 0.05, 0.2, 0.5, 2, 5, 10, 20} per curtailed fleet-hour: ASSUMED (EPS2 T1); context tables only")
    print("  sensitivity (not scored): R in {0, 0.01, 0.025, 0.1} h ASSUMED; a throttle curve through (throughput 0.9, power 0.78) SOURCED")
    print("    (docs/citations/dr1_f4_2026-09-29.md, Patel et al. POLCA arXiv:2308.12908 v1: 'For Flan-T5 and GPT- NeoX, frequency capping")
    print("    reduces the peak server power by 22% while only impacting the performance by 10%.'; a peak-power figure), (0, 0) and (1, 1)")
    print("    ASSUMED, piecewise linear between them (ASSUMED)")
    print()
    print("CHOICES")
    print("  C1 TIER (drlib): during an offered event the job runs at throughput 1 - x for min(H, w) hours (a throttle, no checkpoint, own")
    print("     overhead 0); curtailed energy per event min(H, w) (1 - power(1 - x)) fleet-hours; wall delay x min(H, w); valued on the own")
    print("     clock with a wall-clock deadline. The 'average throughput reduction over a 3-6 hour period' is read as this throttle.")
    print("  C2 ETM (drlib): a full pause for the H-hour event plus R own hours without progress at full power; curtailed energy H")
    print("     fleet-hours per event; wall delay H + R; deadline counted in own steps (W + n R <= D).")
    print("  C3 job delay = the wall-clock completion delay (completion hour - W); 'matched job delay' = equal mean delay per job across a")
    print("     fleet of identical jobs, so a fleet can realise any delay between whole-event points by letting a fraction of its jobs")
    print("     take one more event: each arm's season frontier is the line from (0, 0) to its (n_use events) point.")
    print("  C4 n_use = the most events that keep the arm's contract deadline (at most K): the frontier is restricted to seasons in which")
    print("     the job meets its deadline under its own contract (ETM: own-step deadline; TIER: wall-clock deadline).")
    print("  C5 the best tier at delay Delta = the tier supplying the most energy at Delta among the tiers that can reach Delta (dmax >= Delta);")
    print("     ties go to the first tier in the order printed.")
    print("  C6 'within 1 %' = rel(E_ETM, E_best) <= 0.01 with the harness formula |a - b| / max(|a|, |b|), non-strict, exact rationals;")
    print("     Q holds iff this is true at every matched delay in (0, Delta_top] (Delta_top = the smaller of ETM's and the tiers' largest")
    print("     delay) in every cell; Q is not computable if some cell has no common delay range.")
    print("  C7 offers are live only while the job runs (drlib); every offer here precedes hour 1000, so every arm is running at every offer.")
    print()

    print("TIER per-event arithmetic (drlib.event; linear power, scored):")
    for H in HS:
        job = dl.Job(W, DS[0], R)
        parts = []
        for a in [dl.ETM] + tiers():
            ev = dl.event(job, a, H)
            parts.append(f"{a.name} e {dl.g(ev['e'])} d {dl.g(ev['wall_delay'])}")
        print(f"  H = {dl.g(H)}: " + "; ".join(parts))
    print()

    # ------------------------------------------------------------------------------------------------ the scored cells
    cells = {}
    for D in DS:
        for H in HS:
            job = dl.Job(W, D, R)
            offs = dl.every(SPACING, H, job.W)
            K = len(offs)
            sc = score_cell(job, H, K, tiers())
            cells[(D, H)] = dict(job=job, offs=offs, K=K, sc=sc)

    print("PER-CELL FRONTIERS (per arm: energy e and wall delay d per event, energy per hour of delay, deadline-limited events n_use,")
    print("largest delay dmax and energy emax on the frontier; 'ok' = the n_use point meets the deadline and n_use + 1 does not, or n_use = K)")
    for (D, H), cl in cells.items():
        sc, K = cl["sc"], cl["K"]
        print(f"  cell D = {dl.g(D)}, H = {dl.g(H)} (K = {K}):")
        print(f"    {'arm':16} {'e/event':>9} {'d/event':>9} {'e per d':>10} {'nmax':>6} {'n_use':>6} {'dmax h':>10} {'emax':>10} {'ok':>4}")
        for x in [sc["fe"]] + sc["ft"]:
            print(f"    {x['arm'].name:16} {f(x['e'], 4):>9} {f(x['d'], 4):>9} {f(x['slope'], 6):>10} "
                  f"{('none' if x['nmax'] is None else str(x['nmax'])):>6} {x['n_use']:>6} {f(x['dmax'], 3):>10} {f(x['emax'], 3):>10} "
                  f"{dl.yn(x['consistent']):>4}")
    print()

    print("PER-CELL MATCHED-DELAY TABLE (scored; at each breakpoint Delta: ETM's mean events per job and energy, the best feasible tier")
    print("and its energy, rel = |E_ETM - E_best| / max; rel is constant on each interval ending at a breakpoint)")
    for (D, H), cl in cells.items():
        sc = cl["sc"]
        print(f"  cell D = {dl.g(D)}, H = {dl.g(H)}: Delta_top = {f(sc['top'], 3)} h")
        print(f"    {'Delta h':>10} {'ETM events':>11} {'E_ETM':>11} {'best tier':>16} {'tier ev.':>9} {'E_best':>11} {'feasible':>9} {'rel':>12}  within 1 %")
        for r in sc["rows"]:
            print(f"    {f(r['delta'], 3):>10} {f(r['n_etm'], 4):>11} {f(r['E_etm'], 4):>11} {r['best']:>16} {f(r['n_best'], 3):>9} "
                  f"{f(r['E_best'], 4):>11} {r['feas']:>9} {f(r['rel'], 9):>12}  {dl.yn(r['rel'] <= TOL)}")
        print(f"    max rel {f(sc['maxrel'], 12)} (exact {sc['maxrel']}); cell within 1 % at every matched delay: "
              f"{'-' if sc['within'] is None else dl.yn(sc['within'])}; ETM's reach: its largest energy / the best tier's largest energy = "
              f"{f(sc['reach'], 4)}")
    print()

    # ------------------------------------------------------------------------------------------------ context: decisions at payments
    print("CONTEXT (not scored): the arms' decisions at payments (drlib backward induction, ties accept). p_all = the minimum flat payment")
    print("at which the arm accepts every offer; per pi: events accepted, 'y'/'n' deadline met on the arm's own contract; the energy and")
    print("delay of the season at pi = 0.2 per curtailed fleet-hour")
    for (D, H), cl in cells.items():
        job, offs, K = cl["job"], cl["offs"], cl["K"]
        print(f"  cell D = {dl.g(D)}, H = {dl.g(H)} (K = {K}):  pi = " + " ".join(f"{dl.g(p):>5}" for p in GRID))
        for a in [dl.ETM] + tiers():
            pa = dl.p_all(job, a, offs)
            plays = [dl.play(job, a, offs, p) for p in GRID]
            r02 = plays[GRID.index(dl.q("0.2"))]
            print(f"    {a.name:16} " + " ".join(f"{r['events']:>3}{('y' if r['met'] else 'n'):>2}" for r in plays)
                  + f"   p_all {f(pa.x, 6) if pa.kind == 'threshold' else pa.kind}; at pi 0.2: energy {f(r02['fleet_hours'], 3)}, "
                  f"delay {f(r02['completion'] - job.W, 3)} h")
    print()

    # ------------------------------------------------------------------------------------------------ Q
    within = [cl["sc"]["within"] for cl in cells.values()]
    if any(w is None for w in within):
        q_word = "not computable"
    else:
        q_word = "holds" if all(within) else "fails"
    n_in = sum(int(bool(w)) for w in within)
    allrel = [cl["sc"]["maxrel"] for cl in cells.values() if cl["sc"]["maxrel"] is not None]
    worst = max(allrel) if allrel else None
    best_ = min(allrel) if allrel else None
    bps_all = [r for cl in cells.values() for r in cl["sc"]["rows"]]
    n_behind = sum(int(r["E_etm"] < r["E_best"]) for r in bps_all)
    n_ahead_q = sum(int(r["E_etm"] > r["E_best"]) for r in bps_all)
    fc_right = {"holds": "right", "fails": "wrong", "not computable": "not decidable"}[q_word]
    print(f"Q (scored): cells within 1 % at every matched delay {n_in} of {len(cells)}; per-cell max rel from {f(best_, 6)} to {f(worst, 6)}"
          f" -> Q {q_word}; the forecast 'Q holds' is {fc_right}")
    print(f"  direction: ETM supplies less energy than the best tier at {n_behind}, more at {n_ahead_q}, the same at "
          f"{len(bps_all) - n_behind - n_ahead_q} of {len(bps_all)} matched-delay breakpoints")
    # the source of the gap, from the numbers: ETM's energy per hour of delay against the tiers'
    for H in HS:
        sc = cells[(DS[0], H)]["sc"]
        se = sc["fe"]["slope"]
        st = sorted({x["slope"] for x in sc["ft"]})
        rstar = H * (1 / (1 - TOL) - 1)        # the R at which ETM's energy per hour of delay H / (H + R) is 1 % below a slope-1 tier
        sc_star = score_cell(dl.Job(W, DS[0], rstar), H, cells[(DS[0], H)]["K"], tiers())
        print(f"  H = {dl.g(H)}: ETM energy per hour of delay {f(se, 6)} (exact {se}); tiers' {', '.join(f(s, 6) for s in st)}; "
              f"R at which the gap is exactly 1 %: {f(rstar, 6)} h (exact {rstar}); scored at that R: max rel {f(sc_star['maxrel'], 9)}, "
              f"within 1 %: {dl.yn(bool(sc_star['within']))}")
    print()

    # ------------------------------------------------------------------------------------------------ sensitivities (not scored)
    print("SENSITIVITY 1 (not scored): the restart overhead R (ASSUMED values); cells within 1 % at every matched delay, and per-cell max rel")
    for r_ in R_SENS:
        res = []
        for (D, H), cl in cells.items():
            s = score_cell(dl.Job(W, D, r_), H, cl["K"], tiers())
            res.append(((D, H), s))
        nin = sum(int(bool(s["within"])) for _, s in res)
        print(f"  R = {dl.g(r_):>5} h: {nin} of {len(res)} cells within 1 %; " +
              "; ".join(f"D {dl.g(D)} H {dl.g(H)}: {f(s['maxrel'], 6)}" for (D, H), s in res))
    print()
    pw = dl.power_pw([PW_ORIGIN, PW_POINT, (dl.q(1), dl.q(1))])
    print("SENSITIVITY 2 (not scored): the throttle's performance-power curve through the sourced point (0.9, 0.78), (0, 0) and (1, 1)")
    print("  ASSUMED; ETM unchanged. Per cell: the best tier at each breakpoint and rel")
    n2 = 0
    for (D, H), cl in cells.items():
        s = score_cell(cl["job"], H, cl["K"], tiers(pw, "*"))
        n2 += int(bool(s["within"]))
        slopes = ", ".join(f"{x['arm'].name} {f(x['slope'], 4)}" for x in s["ft"])
        print(f"  D {dl.g(D)} H {dl.g(H)}: tier energy per hour of delay ({slopes}); ETM {f(s['fe']['slope'], 4)}; "
              + "; ".join(f"Delta {f(r['delta'], 2)}: {r['best']} rel {f(r['rel'], 4)}" for r in s["rows"])
              + f" -> within 1 %: {dl.yn(bool(s['within']))}")
    print(f"  {n2} of {len(cells)} cells within 1 % under this curve")
    print()
    print("SENSITIVITY 3 (not scored): one job, no fleet mixing (C3 dropped). At each tier's own full-season point, ETM takes the most whole")
    print("  events whose delay does not exceed the tier's; rel of the two energies")
    n3 = tot3 = 0
    for (D, H), cl in cells.items():
        rows = discrete(cl["sc"], cl["K"])
        n3 += sum(int(r[-1] <= TOL) for r in rows)
        tot3 += len(rows)
        print(f"  D {dl.g(D)} H {dl.g(H)}: " + "; ".join(
            f"{nm} (delay {f(dT, 2)}, E {f(eT, 2)}) vs ETM {n} ev (delay {f(dE, 2)}, E {f(eE, 2)}) rel {f(rr, 4)}"
            for nm, dT, eT, n, dE, eE, rr in rows))
    print(f"  {n3} of {tot3} tier points within 1 %")
    print()

    # ------------------------------------------------------------------------------------------------ the gate
    # G-ZERO: ETM's stake beyond R exactly 0 in every cell (every event count n = 0..K-1), and its x* == R / H at every offer state
    beyond, xs_n, xs_ok = [], 0, 0
    for (D, H), cl in cells.items():
        job, offs, K = cl["job"], cl["offs"], cl["K"]
        beyond += [abs(dl.stake(job, dl.ETM, H, n) - job.rate * job.overhead) for n in range(K)]
        xa = dl.xstar_all(job, dl.ETM, offs)
        xs_n += len(xa)
        xs_ok += sum(int(x.kind == "threshold" and x.x == job.overhead / H) for x in xa.values())
    gz = max(beyond) == 0 and xs_ok == xs_n
    # G-NEG: no events offered; ETM against WALL on every outcome
    neg = {}
    for a in (dl.WALL, dl.ETM):
        neg[a.name] = [dl.play(dl.Job(W, D, R), a, (), p) for D in DS for H in HS for p in GRID]
    ahead = []
    for rw, re_ in zip(neg["WALL"], neg["ETM"]):
        ahead.append(("curtailed fleet-hours", re_["fleet_hours"] > rw["fleet_hours"] and relx(re_["fleet_hours"], rw["fleet_hours"]) > TOL))
        ahead.append(("valuation", re_["valuation"] > rw["valuation"] and relx(re_["valuation"], rw["valuation"]) > TOL))
        ahead.append(("completion", re_["completion"] < rw["completion"] and relx(re_["completion"], rw["completion"]) > TOL))
        ahead.append(("deadline met", re_["met"] and not rw["met"]))
    n_ahead = sum(int(b) for _, b in ahead)
    maxrel_neg = max(max(relx(re_[k], rw[k]) for k in ("fleet_hours", "valuation", "completion"))
                     for rw, re_ in zip(neg["WALL"], neg["ETM"]))
    gn = n_ahead == 0
    print("GATE")
    print(f"  G-ZERO: ETM's stake beyond its restart overhead, max |stake - R| over {len(beyond)} event counts in {len(cells)} cells = "
          f"{f(max(beyond), 6)} (exact {max(beyond)}); ETM's x* == R/H at {xs_ok} of {xs_n} offer states -> {'holds' if gz else 'FAILS'}")
    print(f"  G-NEG: no events offered (K = 0), {len(neg['ETM'])} cell x pi combinations; ETM ahead of WALL by more than 1 % on "
          f"{n_ahead} of {len(ahead)} outcome comparisons (curtailed hours, valuation, completion, deadline met); max rel over the numeric "
          f"outcomes {f(maxrel_neg, 6)} -> {'holds' if gn else 'FAILS'}")
    print()
    print("POST-FIRST-RUN CHANGES: " + ("none" if not POST_FIRST_RUN_CHANGES else "; ".join(POST_FIRST_RUN_CHANGES)))
    print()
    print(f"RESULT H2: Q {q_word}; G-ZERO {'holds' if gz else 'FAILS'} (max |ETM stake - R| = {f(max(beyond), 6)} over {len(beyond)} event "
          f"counts, x* == R/H at {xs_ok} of {xs_n} offer states); G-NEG {'holds' if gn else 'FAILS'} (no events: ETM ahead of WALL by "
          f"> 1 % on {n_ahead} of {len(ahead)} outcome comparisons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
