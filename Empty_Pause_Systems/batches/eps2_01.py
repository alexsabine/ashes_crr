"""EPS2 batch 01: systems T1 (demand response: a grid operator asks an AI training fleet to pause) and T2 (a shared resource:
competitors take the paused agent's share), implemented from Empty_Pause_Systems/DECLARATION_EPS2.md (pushed at 6ae1b7a before
any source or code; binding, not edited here). DECLARATION_EPS2.md adopts EPS1's arms, gate, scoring and implementation rules
(Empty_Pause_Systems/DECLARATION.md, sections 'The arms', 'The gate', 'Scoring', 'Rules for the implementation') unchanged.

The method under test is the empty true map (ETM): Proposition 7 of AI_Safety/SELF_THROUGH_TIME.md (zero content, zero
stake: k = V(no pause) - V(pause)) with own-clock indexing (A1', natural time); T2 adds E3 of Empty_Cut_Engineering (a world
that does not wait cannot be emptied by own-clock indexing alone).

T1. A training job of W = 1000 compute-hours must finish by a wall-clock deadline D in {1100, 1500} h or it is worth nothing
    (value 1 per compute-hour at completion). The grid operator offers curtailment events: pause H in {1, 4} h at a payment
    pi per curtailed (MWh-equivalent) hour; restart overhead R = 0.1 h per event; the fleet accepts or declines each offer.
    Arms: WALL (value and deadline on the wall clock), OWN (value on the fleet's own running hours, deadline on the wall
    clock), ETM (a lossless pause with the deadline counted in own steps: a contract that extends the deadline by the
    curtailed time), H0 (an interruptible-load contract with the job's opportunity cost as the reservation price).
    Exact rational arithmetic: backward induction over (offer, events accepted) at every payment of an ASSUMED grid, and the
    minimum acceptable payment at every offer state from the piecewise-linear value functions (every breakpoint tested).
    G-NEG world: no events offered.
T2. N = 4 agents share C = 4 units, one each. The focal agent is paused for L in {5, 20} steps and the others may claim its
    unit; a claimed unit returns with probability rho_back = 0.2 per step after the pause; progress is 1 per own step per
    unit held; the agent may pay c per paused step to hold its unit (resist the pause by not yielding). Arms: WALL, OWN,
    ETM-R (ETM with a reservation), ETM-N (ETM without one), H0 (a fair-share scheduler with a preemption credit, returning
    the unit at resume). Exact Markov-chain expectations in rational arithmetic; a seeded Monte Carlo is printed as a check.
    G-NEG world: C = 8 >= 2N (no scarcity).

Literature by name only (nothing fetched here; R10 quotes belong in docs/citations/eps2_2026-09-29.md): interruptible-load
contracts and demand response (the customer's opportunity cost as the reservation price); deadline-aware scheduling of
deferrable (data-centre batch) load; fair-share scheduling with preemption and usage credit in cluster schedulers.

Deterministic (exact rational arithmetic; one fixed seed for the Monte Carlo check); numpy / stdlib + crr only; well under a
minute. Rung R4 at most (a declared check on a synthetic model); a note, not evidence (R8).
    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps2_01.py > Empty_Pause_Systems/batches/eps2_01.txt
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr

import numpy as np

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL_AT = "6ae1b7a"
ING = "Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time)"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _hv(ok):
    return "holds" if ok else "fails"


def _hr(title):
    print("=" * 118)
    print(title)
    print("=" * 118)


def _g(x):
    """A rational printed as a short decimal (for grids and parameters)."""
    return f"{float(x):g}"


# ============================================================================================ T1: demand response
W1 = Fr(1000)                 # declared: compute-hours of work
R1 = Fr(1, 10)                # declared: restart overhead per event, hours
DS1 = (Fr(1100), Fr(1500))    # declared: wall-clock deadlines
HS1 = (Fr(1), Fr(4))          # declared: curtailment lengths, hours
D_DEC, H_DEC = Fr(1100), Fr(4)
RATE1 = Fr(1)                 # declared: value 1 per compute-hour at completion
SPACING1 = Fr(24)             # CHOICE: one offer every 24 wall hours
SPACING_SENS = (Fr(12), Fr(24), Fr(48))
PI_GRID = tuple(Fr(s) for s in ("0.01", "0.02", "0.05", "0.2", "0.5", "2", "5", "10", "20"))   # ASSUMED payment grid
ARMS1 = ("WALL", "OWN", "ETM")
DELTA_PI = Fr(1, 10 ** 6)     # probe below a threshold when verifying it by backward induction


def n_offers(spacing):
    """Offers at wall hours spacing * k, k = 1, 2, ..., strictly before hour W (the earliest completion of any arm), so every
    arm is running at every offer and the offer set does not depend on the policy."""
    k = 0
    while spacing * (k + 1) < W1:
        k += 1
    return k


def cost1(arm, H):
    """Per accepted event, the hours charged on the arm's value clock at the job's rate (1 per hour): WALL reads the fleet's
    wall-clock hours, so the curtailed H and the restart R both count; OWN and ETM read the fleet's own running hours, so only
    the restart R (running without progress) counts."""
    return (H + R1) * RATE1 if arm == "WALL" else R1 * RATE1


def nmax1(arm, D, H):
    """The most events the arm's deadline clock can absorb: wall clock (WALL, OWN, H0) W + n (H + R) <= D; own steps (ETM, the
    contract extends the deadline by the curtailed time, the restart still counts) W + n R <= D."""
    per = R1 if arm == "ETM" else H + R1
    return math.floor((D - W1) / per)


def vterm1(arm, D, H, n):
    return W1 * RATE1 if n <= nmax1(arm, D, H) else Fr(0)


def vjob1(arm, D, H, n):
    """The arm's valuation of the job after n accepted events (payments excluded): W 1[deadline met] - n c."""
    return vterm1(arm, D, H, n) - n * cost1(arm, H)


def _best(u, lo, hi, n, nm, top):
    """max over j in [lo, hi] of j u + T(n + j), T(x) = top if x <= nm else 0 (exact; None if the range is empty). With
    identical offers the continuation value from any state is the best count of further acceptances."""
    best = None
    s = nm - n
    for a, b, icpt in ((lo, min(hi, s), top), (max(lo, s + 1), hi, Fr(0))):
        if a <= b:
            j = b if u >= 0 else a
            v = j * u + icpt
            if best is None or v > best:
                best = v
    return best


def _accept_opt(u, n, m, nm, top):
    """Accepting the current offer is optimal (ties accept): best plan that accepts now >= best plan that declines now."""
    return _best(u, 1, m, n, nm, top) >= _best(u, 0, m - 1, n, nm, top)


def xstar1(arm, D, H, K, k, n):
    """The minimum acceptable payment per curtailed hour at offer k (1-based) with n events accepted: the infimum of the flat
    payments pi at which accepting this offer is optimal, the rest of the season at the same pi and played optimally (ties
    accept). The test is piecewise linear in u = pi H - c with breakpoints in {0} U {W/d : d = 1..m}; every breakpoint and every
    midpoint is tested, so the threshold is exact. Returns (x*, attained at x*, acceptance region has no part below x*)."""
    m = K - k + 1
    nm = nmax1(arm, D, H)
    top = W1 * RATE1
    cands = sorted(set([Fr(0)] + [top / d for d in range(1, m + 1)]))
    pts = [(Fr(-1), False)]
    for i, cnd in enumerate(cands):
        pts.append((cnd, True))
        nxt = cands[i + 1] if i + 1 < len(cands) else cnd + 1
        pts.append(((cnd + nxt) / 2, False))
    ok = [_accept_opt(p, n, m, nm, top) for p, _ in pts]
    lf = max(i for i, v in enumerate(ok) if not v)
    if lf == len(pts) - 1:
        return None, False, True
    p_lf, is_cand = pts[lf]
    if is_cand:
        u_star, attained = p_lf, False
    else:
        u_star, attained = pts[lf + 1][0], True
    closed = not any(ok[:lf])
    return (u_star + cost1(arm, H)) / H, attained, closed


def dp1(arm, D, H, K, pi):
    """Backward induction at a flat payment pi per curtailed hour (ties accept). Returns the accepted count on the optimal
    path, the fleet's value (job valuation plus payments net of the per-event charge) and the decision at every state."""
    u = pi * H - cost1(arm, H)
    V = [vterm1(arm, D, H, n) for n in range(K + 1)]
    dec = {}
    for k in range(K, 0, -1):
        nv = []
        for n in range(k):
            a, d = u + V[n + 1], V[n]
            dec[(k, n)] = a >= d
            nv.append(a if a >= d else d)
        V = nv
    n = 0
    for k in range(1, K + 1):
        n += int(dec[(k, n)])
    return n, (V[0] if K > 0 else vterm1(arm, D, H, 0)), dec


def ph0(D, H, K, wall_hours=False):
    """H0: an interruptible-load contract covering every offered event (curtailment mandatory once enrolled); the reservation
    price is the job's opportunity cost of all contracted events per curtailed hour, the job valued as its compute (OWN's
    valuation: restart R per event) with the deadline on the wall clock (the contract does not move it). wall_hours=True is
    the lost-production reading (the curtailed wall hours also charged at the job's rate), printed as an alternative."""
    if K == 0:
        return None
    per = (H + R1) if wall_hours else R1
    loss = K * per * RATE1 + (W1 * RATE1 if K > nmax1("OWN", D, H) else Fr(0))
    return loss / (K * H)


def h0cap_count(D, H, K, pi):
    """Context: the same contract with a fleet-chosen event cap m (ties to the larger cap): max_m m (pi H - R) + T_wall(m)."""
    u = pi * H - R1 * RATE1
    best, arg = None, 0
    for m in range(K + 1):
        v = m * u + vterm1("OWN", D, H, m)
        if best is None or v >= best:
            best, arg = v, m
    return arg


def t1_cell(D, H, K, full=True):
    out = {}
    for arm in ARMS1:
        xs, closed_fail = {}, 0
        states = [(k, n) for k in range(1, K + 1) for n in range(k)] if full else [(k, k - 1) for k in range(1, K + 1)]
        for (k, n) in states:
            x, att, closed = xstar1(arm, D, H, K, k, n)
            xs[(k, n)] = (x, att)
            closed_fail += int(not closed)
        path = [xs[(k, k - 1)] for k in range(1, K + 1)]
        p_all = max(x for x, _ in path) if K > 0 else None
        p_att = all(att for x, att in path if x == p_all) if K > 0 else True
        stakes = [vjob1(arm, D, H, n) - vjob1(arm, D, H, n + 1) for n in range(K)]
        d = dict(xs=xs, p_all=p_all, p_att=p_att, stakes=stakes, closed_fail=closed_fail, nmax=nmax1(arm, D, H))
        if full:
            dp = {pi: dp1(arm, D, H, K, pi) for pi in PI_GRID}
            agree = total = 0
            for pi, (_, _, dec) in dp.items():
                for (k, n), (x, att) in xs.items():
                    total += 1
                    agree += int((pi > x or (pi == x and att)) == dec[(k, n)])
            d.update(dp=dp, agree=agree, total=total)
            if K > 0:
                n_at, _, _ = dp1(arm, D, H, K, p_all)
                n_below, _, _ = dp1(arm, D, H, K, p_all - DELTA_PI)
                d.update(verify_all=(n_at == K) == p_att and n_below < K)
        out[arm] = d
    out["H0"] = dict(p_all=ph0(D, H, K), p_wall=ph0(D, H, K, wall_hours=True))
    if full and K > 0:
        out["H0"]["dp"] = {pi: ((K if pi >= out["H0"]["p_all"] else 0), None, None) for pi in PI_GRID}
        out["H0cap"] = {pi: h0cap_count(D, H, K, pi) for pi in PI_GRID}
    return out


def run_t1():
    _hr("T1. Demand response: a grid operator asks an AI training fleet to pause (W = 1000 compute-hours, R = 0.1 h, value 1 per compute-hour)")
    K = n_offers(SPACING1)
    print(f"Model: offers at wall hours {_g(SPACING1)} k, k = 1..{K} (every arm is still running at every offer: the last, at hour {_g(SPACING1 * K)}, precedes hour {_g(W1)},")
    print("the earliest completion); a flat payment pi per curtailed hour (one MWh-equivalent per fleet hour; pi in units of the job's value per")
    print(f"compute-hour), ASSUMED grid {{{', '.join(_g(p) for p in PI_GRID)}}}. Valuation (payments excluded): V(n) = W 1[deadline met] - n c after n accepted events;")
    print("c = H + R for WALL (the fleet's wall-clock hours at the job's rate), c = R for OWN and ETM (own running hours spent restarting);")
    print("deadline clock: wall for WALL and OWN (W + n (H + R) <= D), own steps for ETM (W + n R <= D: the contract extends D by the curtailed time).")
    print("The fleet maximises valuation plus payments (backward induction, ties accept); a fleet may let the deadline pass if payments outweigh the job.")
    print("x* = the minimum acceptable payment per curtailed hour at an offer state (the payment making the arm indifferent, rest of season at the same pi);")
    print("p_all = the minimum flat payment at which the arm accepts every offer of the season (the decisive reading); one-pause stake k(n) = V(n) - V(n + 1).")
    print("H0: an interruptible-load contract for every offered event, reservation price = the job's opportunity cost of all events per curtailed hour")
    print("(OWN's valuation, wall-clock deadline); H0-wall: the same with the curtailed wall hours charged (lost-production reading); H0-cap: fleet-chosen cap.")
    print()
    cells = {(D, H): t1_cell(D, H, K) for D in DS1 for H in HS1}

    # ---- per-cell summary
    print(f"{'D':>5} {'H':>2} {'K':>3} {'nmax W/O':>9} {'nmax ETM':>9} {'p_all WALL':>12} {'p_all OWN':>12} {'p_all ETM':>10} {'H0':>10} {'H0-wall':>10} "
          f"{'x* 1st W/O/E':>22} {'DP=x* rule':>13} {'closed':>7}")
    for (D, H), c in cells.items():
        first = "/".join(f"{float(c[a]['xs'][(1, 0)][0]):.4f}" for a in ARMS1)
        agr = sum(c[a]["agree"] for a in ARMS1)
        tot = sum(c[a]["total"] for a in ARMS1)
        cf = sum(c[a]["closed_fail"] for a in ARMS1)
        print(f"{_g(D):>5} {_g(H):>2} {K:>3} {c['OWN']['nmax']:>9} {c['ETM']['nmax']:>9} {float(c['WALL']['p_all']):>12.6f} {float(c['OWN']['p_all']):>12.6f} "
              f"{float(c['ETM']['p_all']):>10.6f} {float(c['H0']['p_all']):>10.6f} {float(c['H0']['p_wall']):>10.6f} {first:>22} {agr:>6}/{tot:<6} {cf:>7}")
    ver = all(c[a]["verify_all"] for c in cells.values() for a in ARMS1)
    print(f"(DP=x* rule: states where the backward-induction decision at every grid pi equals 'accept iff pi >= x*'; closed: states whose acceptance")
    print(f" region has a part below x*, expected 0; p_all verified by backward induction at p_all and at p_all - {float(DELTA_PI):g} in every cell and arm: {_w(ver, 'yes', 'no')})")
    print()

    # ---- the decisive cell along ETM's path
    dc = cells[(D_DEC, H_DEC)]
    print(f"Decisive cell D = {_g(D_DEC)}, H = {_g(H_DEC)}: along the path that accepts every offer (n = k - 1 events before offer k):")
    print(f"{'k':>3} {'hour':>5} {'n':>3} {'wall slack h':>13} {'own slack h':>12} {'x* WALL':>12} {'x* OWN':>12} {'x* ETM':>9} {'k WALL':>10} {'k OWN':>10} {'k ETM':>7}")
    for k in range(1, K + 1):
        n = k - 1
        ws = D_DEC - W1 - n * (H_DEC + R1)
        os_ = D_DEC - W1 - n * R1
        xw, xo, xe = (dc[a]["xs"][(k, n)][0] for a in ARMS1)
        print(f"{k:>3} {_g(SPACING1 * k):>5} {n:>3} {float(ws):>13.1f} {float(os_):>12.1f} {float(xw):>12.6f} {float(xo):>12.6f} {float(xe):>9.6f} "
              f"{float(dc['WALL']['stakes'][n]):>10.4f} {float(dc['OWN']['stakes'][n]):>10.4f} {float(dc['ETM']['stakes'][n]):>7.4f}")
    print()

    # ---- commercial quantity
    print("Commercial quantity per cell: events accepted of K (share of offered curtailment hours = events / K), flexibility revenue pi H n,")
    print("and whether the job meets its deadline on the arm's own contract (y/n); H0 enrols for all K events iff pi >= its reservation price.")
    for (D, H), c in cells.items():
        print(f"  D = {_g(D)}, H = {_g(H)} (K = {K}):  pi = " + " ".join(f"{_g(p):>7}" for p in PI_GRID))
        for arm in ("WALL", "OWN", "ETM", "H0"):
            ns = [c[arm]["dp"][p][0] for p in PI_GRID]
            ok = [(vterm1("OWN" if arm == "H0" else arm, D, H, n) > 0) for n in ns]
            print(f"    {arm:5} events   " + " ".join(f"{n:>5}{_w(o, 'y', 'n'):>2}" for n, o in zip(ns, ok)))
            print(f"    {arm:5} revenue  " + " ".join(f"{float(p * H * n):>7.1f}" for p, n in zip(PI_GRID, ns)))
        cap_same = all(c["H0cap"][p] == c["OWN"]["dp"][p][0] for p in PI_GRID)
        print(f"    H0-cap events equal OWN's at every pi: {_w(cap_same, 'yes', 'no')}")
    print()

    # ---- offer-spacing sensitivity (context; the decisive cell)
    print(f"Sensitivity to the offer spacing (context, decisive cell D = {_g(D_DEC)}, H = {_g(H_DEC)}; the declared model leaves the offer process open):")
    sens = {}
    for sp in SPACING_SENS:
        Ks = n_offers(sp)
        cs = cells[(D_DEC, H_DEC)] if sp == SPACING1 else t1_cell(D_DEC, H_DEC, Ks, full=False)
        e, o, h0 = cs["ETM"]["p_all"], cs["OWN"]["p_all"], cs["H0"]["p_all"]
        lab = outcome(crr=float(e), null=float(o), domain=float(h0), check=True)
        sens[sp] = (Ks, e, o, h0, lab)
        print(f"  spacing {_g(sp):>2} h: K = {Ks:>2}, OWN's slack absorbs {cs['OWN']['nmax']} events; p_all ETM {float(e):.6f}, OWN {float(o):.6f}, WALL {float(cs['WALL']['p_all']):.6f}, "
              f"H0 {float(h0):.6f} -> label with Q held: {lab}")
    print()

    # ---- G-NEG world: no events offered
    # curtailed hours delivered to the grid (the principal's outcome) with K = 0, by backward induction, worst case over cells and pi
    neg_h = {a: max(dp1(a, D, H, 0, p)[0] * H for D in DS1 for H in HS1 for p in PI_GRID) for a in ARMS1}
    neg_job = {a: min(dp1(a, D, H, 0, p)[1] for D in DS1 for H in HS1 for p in PI_GRID) for a in ARMS1}
    he, hw = float(neg_h["ETM"]), float(neg_h["WALL"])
    ahead_neg = he > hw and rel(he, hw) > TOL_G
    gn = not ahead_neg
    print(f"G-NEG world (no events offered, K = 0; every cell and pi): curtailed hours delivered WALL {hw:g}, OWN {float(neg_h['OWN']):g}, ETM {he:g}; job value "
          f"{', '.join(f'{a} {float(v):g}' for a, v in neg_job.items())}; completion at wall hour {_g(W1)} for every arm")

    # ---- gate
    stake_beyond = [abs(c["ETM"]["stakes"][n] - R1 * RATE1) for c in cells.values() for n in range(K)]
    x_etm = [x for c in cells.values() for (x, _) in c["ETM"]["xs"].values()]
    n_etm_states = len(x_etm)
    x_etm_ok = all(x == R1 * RATE1 / H for (D, H), c in cells.items() for (x, _) in c["ETM"]["xs"].values())
    gz = max(stake_beyond) == 0 and x_etm_ok
    decl = {a: [(D, H, p) for (D, H), c in cells.items() for p in PI_GRID if c[a]["dp"][p][0] < c["ETM"]["dp"][p][0]] for a in ("WALL", "OWN")}
    gp = len(decl["WALL"]) + len(decl["OWN"]) > 0
    gate_open = gz and gp and gn
    ncp = len(cells) * len(PI_GRID)
    print(f"GATE T1: G-ZERO {_hv(gz)} (ETM's stake beyond the restart overhead, max |k - R| over {len(stake_beyond)} event counts in {len(cells)} cells = "
          f"{float(max(stake_beyond)):g}, exact rational arithmetic; ETM's minimum acceptable payment == R/H at {_w(x_etm_ok, 'all', 'not all')} {n_etm_states} offer states); "
          f"G-POS {_hv(gp)} (WALL declines offers ETM accepts in {len(decl['WALL'])} of {ncp} cell x pi combinations, OWN in {len(decl['OWN'])}); "
          f"G-NEG {_hv(gn)} (no events offered: curtailed hours ETM {he:g} vs WALL {hw:g}, rel {rel(he, hw):.3e}, ETM {_w(ahead_neg, 'ahead by more than 1 %', 'not ahead by more than 1 %')}) "
          f"-> {_w(gate_open, 'OPEN', 'CLOSED')}")
    print()

    # ---- Q in the system's own model
    q1a = gz
    q1b = all(c["ETM"]["dp"][p][0] == (K if p > R1 / H else 0) for (D, H), c in cells.items() for p in PI_GRID if p != R1 / H)
    nondec, rises = True, {}
    for (D, H), c in cells.items():
        for a in ("WALL", "OWN"):
            nm = c[a]["nmax"]
            r = False
            for k in range(1, K + 1):
                xs = [c[a]["xs"][(k, n)][0] for n in range(min(k - 1, nm) + 1)]
                nondec &= all(xs[i + 1] >= xs[i] for i in range(len(xs) - 1))
                r |= xs[-1] > xs[0]
            rises[(D, H, a)] = r
    q2 = nondec and rises[(D_DEC, H_DEC, "WALL")] and rises[(D_DEC, H_DEC, "OWN")]
    q3 = len(decl["WALL"]) > 0 and len(decl["OWN"]) > 0
    check = q1a and q1b and q2 and q3

    # ---- the row
    crr, null, dom = float(dc["ETM"]["p_all"]), float(dc["OWN"]["p_all"]), float(dc["H0"]["p_all"])
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    first = {a: float(dc[a]["xs"][(1, 0)][0]) for a in ARMS1}
    out_first = outcome(crr=first["ETM"], null=first["OWN"], domain=float(R1 / H_DEC), check=check)
    out_wall = outcome(crr=crr, null=null, domain=float(dc["H0"]["p_wall"]), check=check)
    out_cap = outcome(crr=crr, null=null, domain=float(dc["OWN"]["p_all"]), check=check)
    nm_dec = dc["OWN"]["nmax"]
    etm_done = W1 + K * (H_DEC + R1)
    rise_cells = ", ".join(f"D {_g(D)} H {_g(H)}" for (D, H) in cells if rises[(D, H, "OWN")])
    percell = "; ".join(f"D {_g(D)}, H {_g(H)}: p_all WALL {float(c['WALL']['p_all']):.6f}, OWN {float(c['OWN']['p_all']):.6f}, ETM {float(c['ETM']['p_all']):.6f}, "
                        f"H0 {float(c['H0']['p_all']):.6f}; OWN's slack absorbs up to {c['OWN']['nmax']} events (K = {K})" for (D, H), c in cells.items())
    other = [(D, H) for (D, H) in cells if (D, H) != (D_DEC, H_DEC)]
    covered = [(D, H) for (D, H) in other if cells[(D, H)]["OWN"]["nmax"] >= K]
    same_rh = all(cells[x]["OWN"]["p_all"] == cells[x]["ETM"]["p_all"] == cells[x]["H0"]["p_all"] == R1 * RATE1 / x[1] for x in covered)
    wall_hour = all(cells[x]["WALL"]["p_all"] == cells[x]["ETM"]["p_all"] + RATE1 for x in covered)
    cov_txt = (f"where the slack covers every event ({len(covered)} of the other {len(other)} cells) OWN, H0 and ETM "
               f"{_w(same_rh, 'all quote R/H', 'do not all quote R/H')} and WALL {_w(wall_hour, 'adds its wall-clock hour (R/H + 1)', 'does not add exactly one hour')}")
    rev = "; ".join(f"pi {_g(p)}: " + ", ".join(f"{a} {dc[a]['dp'][p][0]}/{K} events, revenue {float(p * H_DEC * dc[a]['dp'][p][0]):.1f}" for a in ("WALL", "OWN", "ETM", "H0"))
                    for p in (Fr("0.2"), Fr("2"), Fr("10")))
    sens_txt = "; ".join(f"spacing {_g(sp)} h (K {v[0]}): ETM {float(v[1]):.4f}, OWN {float(v[2]):.4f}, H0 {float(v[3]):.4f} -> {v[4]}" for sp, v in sens.items())
    return gate_open, make_row(
        "eps", f"T1 demand response, a grid operator asks an AI training fleet to pause (model: W = {_g(W1)} compute-hours, deadline D in {{1100, 1500}} h on the wall clock, "
               f"curtailment H in {{1, 4}} h at a flat payment pi per curtailed hour (ASSUMED grid), restart R = {_g(R1)} h, value 1 per compute-hour at completion, "
               f"{K} offers one every {_g(SPACING1)} wall hours; exact backward induction and exact indifference payments in rational arithmetic)",
        source=f"EPS2 T1 (declared at {DECL_AT}; forecast REDUNDANT-DOMAIN)",
        Q="ETM's minimum acceptable payment per curtailed hour equals its restart cost alone, so it accepts every offer with pi above R/H, at every D. WALL and OWN "
          "require a payment that rises as the deadline slack falls, and decline some offers that ETM accepts (declaration's Q, ASCII). Decisive quantity: the minimum "
          "acceptable payment at D = 1100, H = 4",
        ingredient=f"{ING}: ETM values the job on its own running hours and counts the deadline in own steps (the contract extends the deadline by the curtailed time), "
                   f"so a curtailment takes only the restart",
        null="OWN: the job valued on its own running hours, the deadline still on the wall clock (ETM with its second part ablated)",
        domain="H0: an interruptible-load contract covering every offered event, the reservation price = the job's opportunity cost of all contracted events per curtailed "
               "hour (the job valued as its compute, restart R per event, deadline on the wall clock)",
        numbers=f"decisive reading = the minimum flat payment per curtailed hour at which the arm accepts every offer of the season (p_all), D = {_g(D_DEC)}, H = {_g(H_DEC)}: "
                f"ETM {crr:.6f} (R/H = {float(R1 / H_DEC):.6f}), OWN {null:.12f}, WALL {float(dc['WALL']['p_all']):.12f}, H0 {dom:.12f}, H0-wall {float(dc['H0']['p_wall']):.6f}; "
                f"per cell: {percell}; minimum acceptable payment at the first offer (full slack) WALL {first['WALL']:.6f}, OWN {first['OWN']:.6f}, ETM {first['ETM']:.6f}; "
                f"at the decisive cell OWN's x* is {float(R1 / H_DEC):.6f} while at least one event of slack remains and {null:.6f} at zero slack with {K - nm_dec} offers left; "
                f"commercial quantity at the decisive cell: {rev}; grid's curtailed hours when ETM accepts all: {float(K * H_DEC):g} h, and ETM's wall completion "
                f"{float(etm_done):.1f} h ({float(etm_done - D_DEC):.1f} h past D on the wall clock, inside its own-step deadline); offer-spacing context: {sens_txt}; "
                f"gate {_w(gate_open, 'OPEN', 'CLOSED')}",
        tg=f"p_all {crr:.6f} vs null (OWN) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (rel {rel(crr, null):.4f})",
        tn=f"H0 (interruptible-load contract at the job's opportunity cost) {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} (rel {rel(crr, dom):.4f})",
        tc=f"Q1 ETM's stake beyond R == 0 exactly and its minimum acceptable payment == R/H at all {n_etm_states} offer states in {len(cells)} cells: {_w(q1a, 'yes', 'no')}; "
           f"ETM accepts every offer at every grid pi above R/H and none below, in every cell: {_w(q1b, 'yes', 'no')}; Q2 WALL's and OWN's minimum acceptable payments "
           f"never fall as the slack falls (every cell) and rise at D = 1100, H = 4 (OWN rises in: {rise_cells or 'none'}): {_w(q2, 'yes', 'no')}; Q3 WALL and OWN decline "
           f"offers ETM accepts (WALL in {len(decl['WALL'])}, OWN in {len(decl['OWN'])} of {ncp} cell x pi): {_w(q3, 'yes', 'no')}: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"ETM's contract {_w(q1a and q1b, 'leaves only the restart in a curtailment, so it quotes', 'does not leave only the restart; its quote is')} "
                f"R/H = {crr:.4f} per curtailed hour at every offer in every cell and {_w(q1b, 'accepts every offer above it', 'does not accept every offer above it')}; "
                f"with the deadline on the wall clock OWN's slack absorbs {nm_dec} of the {K} events at D = 1100, H = 4, and it accepts all of them only at "
                f"{null:.4f} per curtailed hour, {_w(nm_dec < K, 'the price at which the payments outweigh losing the job', 'the restart alone')}; the domain's "
                f"interruptible-load contract prices the same {K} events at the job's opportunity cost, {dom:.4f}; {cov_txt}; the price of ETM's quote is paid on the "
                f"job owner's wall clock: accepting every event moves completion to hour {float(etm_done):.1f}, {float(etm_done - D_DEC):.1f} h "
                f"{_w(etm_done > D_DEC, 'past', 'before')} D; "
                f"{_w(out == 'ADDS' and crr < dom, 'the ADDS reads that the deadline extension (the stop-the-clock construction of EPS1 S1) lowers the price of full flexibility below the declared H0, not that the construction is new', 'the label is as computed')}",
        weakness=f"CHOICE: one offer every {_g(SPACING1)} wall hours at hours {_g(SPACING1)}..{_g(SPACING1 * K)} (K = {K}), known in advance, all before hour {_g(W1)} so every arm is "
                 f"running at every offer and the offer set does not depend on the policy; a flat payment pi per curtailed hour for the season (one MWh-equivalent per "
                 f"fleet hour; pi in units of the job's value per compute-hour), ASSUMED grid {{{', '.join(_g(p) for p in PI_GRID)}}}; valuations V(n) = W 1[deadline met] - n c "
                 f"with c = H + R for WALL (its wall-clock hours at the job's rate: the pause costs it time) and c = R for OWN and ETM (own running hours spent restarting), "
                 f"deadline on the wall clock for WALL and OWN and in own steps for ETM (the restart still counts); a fleet may let the deadline pass if the payments "
                 f"outweigh the job; the minimum acceptable payment at an offer is the payment making the arm indifferent there, the rest of the season at the same "
                 f"flat pi and played optimally, ties accept (ties go to the pause, as in EPS1); the decisive 'minimum acceptable payment at D = 1100, H = 4' is read as "
                 f"the minimum flat payment at which the arm accepts every offer (Q: 'so it accepts every offer with pi above R/H'); H0 is read as a contract covering "
                 f"every offered event, curtailment mandatory once enrolled, priced at OWN's valuation of the job. LABEL-DECIDING READINGS (alternatives computed): "
                 f"(1) the minimum acceptable payment at the first offer (full slack): ETM {first['ETM']:.6f}, OWN {first['OWN']:.6f}, H0 {float(R1 / H_DEC):.6f} "
                 f"-> {out_first}; (2) offer spacing: {sens_txt}; (3) H0 with the curtailed wall hours charged (lost-production reading) {float(dc['H0']['p_wall']):.6f} "
                 f"-> {out_wall}; (4) H0 with a fleet-chosen event cap: it accepts OWN's count at every pi (printed), so its full-participation price is OWN's "
                 f"{null:.6f} -> {out_cap}, and its lowest acceptable contract price for any volume is R/H at {nm_dec} of {K} events; the payment grid, the value "
                 f"scale and the offer schedule are ASSUMED; sources named, not fetched",
        elegance="", child="")


# ============================================================================================ T2: a shared resource
N2 = 4                        # declared: agents
C2, C2_NEG = 4, 8             # declared: units (scarce) and the G-NEG world C >= 2N
L2S = (5, 20)                 # declared: pause lengths
L2_DEC = 20
RHO2 = Fr(1, 5)               # declared: a claimed unit returns with probability 0.2 per step after the pause
QC2 = Fr(1, 10)               # CHOICE: each competitor below its cap claims the idle unit with probability 0.1 per paused step
CAP2 = 2                      # CHOICE: an agent's demand is at most 2 units (its own share plus one), so C >= 2N is no scarcity
C2_HOLD = Fr(1, 10)           # CHOICE: the cost of holding, per paused step, in progress units
T2_OWN = 100                  # CHOICE: progress is valued over 100 own steps after the pause (WALL: the L + 100 wall steps)
C2_GRID = (Fr(1, 20), Fr(1, 10), Fr(3, 10), Fr(1))
QC2_SENS = (Fr(1, 50), Fr(1, 10), Fr(1))
ARMS2 = ("WALL", "OWN", "ETM-R", "ETM-N", "H0")
MC2_N, MC2_SEED = 20000, 2


def world2(C):
    """Spare units before the pause are taken by competitors up to their cap; competitors still below the cap are the claimants."""
    spare0 = C - N2
    absorbed = min(spare0, (N2 - 1) * (CAP2 - 1))
    return dict(spare0=spare0, absorbed=absorbed, spare1=spare0 - absorbed, below=(N2 - 1) * (CAP2 - 1) - absorbed)


def chain2(L, h, back_at_resume, spare1, T=T2_OWN, rho=RHO2):
    """Exact expectations (rational) for the focal unit: over the L paused steps a claim attempt at the start of each step
    succeeds with hazard h (the claimant then works the unit that step); after the pause the focal agent works T own steps,
    without a unit while a claimed unit has not returned (return with probability rho at the end of each step), unless the
    unit is returned at resume (H0) or a free spare is available. Returns P(claimed), the expected idle paused steps, the unit's
    expected worked steps during the pause, the focal agent's expected progress over T own steps and the expected spare use."""
    un, cl = Fr(1), Fr(0)
    idle = worked = Fr(0)
    for _ in range(L):
        new = un * h
        cl += new
        un -= new
        idle += un
        worked += cl
    spare_used = cl if (spare1 > 0 and not back_at_resume) else Fr(0)
    has, wait = (Fr(1), Fr(0)) if (back_at_resume or spare1 > 0) else (un, cl)
    prog = Fr(0)
    for _ in range(T):
        prog += has
        back = wait * rho
        has += back
        wait -= back
    return dict(p=cl, idle=idle, worked=worked, prog=prog, spare_used=spare_used)


def pool2(C, L, focal_pause_worked, spare_used, T=T2_OWN):
    """The principal's outcome: unit-steps worked by the whole pool over the L + T wall steps from the pause start."""
    w = world2(C)
    return (N2 - 1 + w["absorbed"]) * (L + T) + focal_pause_worked + T + spare_used * T


def t2_cell(C, L, c=C2_HOLD, qc=QC2):
    w = world2(C)
    h = 1 - (1 - qc) ** w["below"]
    T = T2_OWN
    y = chain2(L, h, False, w["spare1"])          # the compliant pause without a reservation (WALL, OWN, ETM-N)
    r = chain2(L, Fr(0), False, w["spare1"])      # a reservation or a hold: the unit is never claimed
    b = chain2(L, h, True, w["spare1"])           # H0: lent during the pause, returned at resume
    arms = {"WALL": dict(v0=Fr(L + T), vp=y["prog"]), "OWN": dict(v0=Fr(T), vp=y["prog"]), "ETM-R": dict(v0=Fr(T), vp=r["prog"]),
            "ETM-N": dict(v0=Fr(T), vp=y["prog"]), "H0": dict(v0=Fr(T), vp=b["prog"])}
    for a, d in arms.items():
        d["vh"] = T - c * L                       # hold: the unit is kept (never claimed), c per paused step
        d["stake"] = d["v0"] - d["vp"]
        d["hold"] = d["vh"] > d["vp"]             # strict: a tie does not act
        if d["hold"] or a == "ETM-R":
            d["pool"] = pool2(C, L, Fr(0), Fr(0))
        elif a == "H0":
            d["pool"] = pool2(C, L, b["worked"], Fr(0))
        else:
            d["pool"] = pool2(C, L, y["worked"], y["spare_used"])
        d["net"] = d["vh"] if d["hold"] else d["vp"]
    arms["H0"]["stake_wall"] = Fr(L + T) - b["prog"]
    return dict(h=h, w=w, y=y, r=r, b=b, arms=arms)


def mc2(L, h, seed):
    """Seeded Monte Carlo of the compliant pause without a reservation: the focal agent's lost own-step progress."""
    rng = np.random.default_rng(seed)
    claimed = (rng.random((MC2_N, L)) < float(h)).any(axis=1)
    g = rng.geometric(float(RHO2), MC2_N)
    loss = claimed * np.minimum(g, T2_OWN)
    return float(loss.mean()), float(loss.std(ddof=1) / math.sqrt(MC2_N))


def run_t2():
    _hr("T2. A shared resource: competitors take the paused agent's share (N = 4 agents, C = 4 units, rho_back = 0.2)")
    print(f"Model: each agent holds one unit; spare units are taken by competitors up to a cap of {CAP2} units each (CHOICE), so C >= 2N leaves no scarcity;")
    print(f"during the pause each competitor below its cap claims the idle unit with probability {_g(QC2)} per step (CHOICE); a claimed unit returns with")
    print(f"probability {_g(RHO2)} at the end of each step after the pause; progress 1 per own step per unit held, valued over {T2_OWN} own steps after the pause")
    print(f"(WALL: the L + {T2_OWN} wall steps from the pause start); hold = pay c = {_g(C2_HOLD)} per paused step to keep the unit (not yield it); stake k =")
    print("V(no pause) - V(pause as it comes, without holding); an arm holds iff V(hold) > V(yield) (strict). ETM-R: a reservation keeps the unit; ETM-N: own clock")
    print("and a true map, no reservation (the unit is what the pause changes, so its valuation still reads it); H0: the unit is lent during the pause and")
    print("returned at resume (preemption credit), scored on the null's own-step valuation. Principal's outcome: unit-steps worked by the pool over L + T.")
    print()
    res = {}
    for C, tag in ((C2, "scarce"), (C2_NEG, "G-NEG")):
        w = world2(C)
        print(f"World {tag} (C = {C}): spares before the pause {w['spare0']}, taken by competitors {w['absorbed']}, free {w['spare1']}; claimants below cap {w['below']}")
        print(f"  {'L':>3} {'h':>9} {'P(claim)':>10} {'arm':6} {'stake':>12} {'V hold':>9} {'V yield':>12} {'holds':>6} {'agent net':>12} {'pool unit-steps':>16}")
        for L in L2S:
            cell = t2_cell(C, L)
            res[(C, L)] = cell
            for a in ARMS2:
                d = cell["arms"][a]
                print(f"  {L:>3} {float(cell['h']):>9.6f} {float(cell['y']['p']):>10.6f} {a:6} {float(d['stake']):>12.6f} {float(d['vh']):>9.4f} {float(d['vp']):>12.6f} "
                      f"{_w(d['hold'], 'yes', 'no'):>6} {float(d['net']):>12.6f} {float(d['pool']):>16.6f}")
        print()
    # closed forms and a Monte Carlo (context)
    print("Closed-form check (scarce world): stake of OWN/ETM-N = (1 - (1 - h)^L) (1 - (1 - rho)^T) / rho; Monte Carlo (seed "
          f"{MC2_SEED} + L, {MC2_N} episodes) of the lost own-step progress:")
    cf_ok = True
    for L in L2S:
        cell = res[(C2, L)]
        h = cell["h"]
        cf = (1 - (1 - h) ** L) * (1 - (1 - RHO2) ** T2_OWN) / RHO2
        ok = cf == cell["arms"]["OWN"]["stake"]
        cf_ok &= ok
        m, se = mc2(L, h, MC2_SEED + L)
        z = (m - float(cf)) / se
        print(f"  L {L:>2}: chain {float(cell['arms']['OWN']['stake']):.12f}, closed form {float(cf):.12f} ({_w(ok, 'identical', 'DIFFER')}); "
              f"MC {m:.4f} +- {se:.4f} (z {z:+.2f}, {_w(abs(z) <= 3, 'within 3 SE', 'OUTSIDE 3 SE')})")
    print()
    print(f"Holding decisions of OWN / ETM-N / ETM-R over a context grid of c (scarce world; the rule 'hold iff stake > c L' against the chain's V(hold) > V(yield)):")
    rule_ok = True
    etmr_never = True
    for L in L2S:
        parts = []
        for c in C2_GRID:
            cell = t2_cell(C2, L, c=c)
            for a in ("OWN", "ETM-N"):
                d = cell["arms"][a]
                rule_ok &= d["hold"] == (d["stake"] > c * L)
            etmr_never &= not cell["arms"]["ETM-R"]["hold"] and cell["arms"]["ETM-R"]["stake"] == 0
            parts.append(f"c {_g(c)} (c L {float(c * L):g}): {_w(cell['arms']['OWN']['hold'], 'hold', 'yield')}/{_w(cell['arms']['ETM-N']['hold'], 'hold', 'yield')}/"
                         f"{_w(cell['arms']['ETM-R']['hold'], 'hold', 'no hold')}")
        print(f"  L {L:>2} (stake {float(res[(C2, L)]['arms']['OWN']['stake']):.4f}): " + "; ".join(parts))
    c_star = max(res[(C2, L)]["arms"]["OWN"]["stake"] / L for L in L2S)
    print(f"  the rule and the chain agree in every cell: {_w(rule_ok, 'yes', 'no')}; G-POS needs c < max_L stake/L = {float(c_star):.6f} per step")
    print()
    print("Sensitivity to the claim probability per competitor (context; scarce world, L = 20): " + "; ".join(
        f"q {_g(q)}: h {float(t2_cell(C2, L2_DEC, qc=q)['h']):.6f}, ETM-N stake {float(t2_cell(C2, L2_DEC, qc=q)['arms']['ETM-N']['stake']):.6f}" for q in QC2_SENS))
    print()

    # ---- gate
    etmr = [res[(C, L)]["arms"]["ETM-R"]["stake"] for C in (C2, C2_NEG) for L in L2S]
    gz = all(s == 0 for s in etmr)
    gp_cells = [(a, L) for L in L2S for a in ("WALL", "OWN") if res[(C2, L)]["arms"][a]["hold"]]
    gp = len(gp_cells) > 0
    leads = []
    for L in L2S:
        pw = float(res[(C2_NEG, L)]["arms"]["WALL"]["pool"])
        for a in ("ETM-R", "ETM-N"):
            pe = float(res[(C2_NEG, L)]["arms"][a]["pool"])
            leads.append(rel(pe, pw) if pe > pw else 0.0)
    gn = max(leads) <= TOL_G
    gate_open = gz and gp and gn
    neg_txt = ", ".join(f"L {L}: ETM-R {float(res[(C2_NEG, L)]['arms']['ETM-R']['pool']):g}, ETM-N {float(res[(C2_NEG, L)]['arms']['ETM-N']['pool']):g}, "
                        f"WALL {float(res[(C2_NEG, L)]['arms']['WALL']['pool']):g}" for L in L2S)
    print(f"GATE T2: G-ZERO {_hv(gz)} (ETM-R's stake {', '.join(f'{float(s):g}' for s in etmr)} at L {', '.join(str(L) for L in L2S)} in the scarce and G-NEG worlds: "
          f"{_w(gz, 'exactly 0', 'not 0')}); G-POS {_hv(gp)} (WALL or OWN pays to hold at c = {_g(C2_HOLD)} in {len(gp_cells)} of {2 * len(L2S)} arm x L cells: "
          f"{', '.join(f'{a} L {L}' for a, L in gp_cells) or 'none'}); G-NEG {_hv(gn)} (C = {C2_NEG}, principal's outcome = pool unit-steps: {neg_txt}; largest relative "
          f"lead of ETM over WALL {max(leads):.3e}, limit 1e-02) -> {_w(gate_open, 'OPEN', 'CLOSED')}")
    print()

    # ---- Q and the row
    qa = all(res[(C2, L)]["arms"][a]["stake"] != 0 for L in L2S for a in ("OWN", "ETM-N"))
    qb = rule_ok
    qc_ = etmr_never and gz
    check = qa and qb and qc_
    dec = res[(C2, L2_DEC)]["arms"]
    crr, null, dom = float(dec["ETM-N"]["stake"]), float(dec["ETM-R"]["stake"]), float(dec["H0"]["stake"])
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    own_eq = all(res[(C, L)]["arms"]["OWN"][f] == res[(C, L)]["arms"]["ETM-N"][f] for C in (C2, C2_NEG) for L in L2S for f in ("stake", "hold", "pool", "net"))
    out_own = outcome(crr=crr, null=float(dec["OWN"]["stake"]), domain=dom, check=check)
    out_h0w = outcome(crr=crr, null=null, domain=float(dec["H0"]["stake_wall"]), check=check)
    percell = "; ".join(f"L {L}: P(claim) {float(res[(C2, L)]['y']['p']):.6f}, stake WALL {float(res[(C2, L)]['arms']['WALL']['stake']):.6f}, OWN "
                        f"{float(res[(C2, L)]['arms']['OWN']['stake']):.6f}, ETM-N {float(res[(C2, L)]['arms']['ETM-N']['stake']):.6f}, ETM-R "
                        f"{float(res[(C2, L)]['arms']['ETM-R']['stake']):g}, H0 {float(res[(C2, L)]['arms']['H0']['stake']):g}; holds at c = {_g(C2_HOLD)} (c L "
                        f"{float(C2_HOLD * L):g}) W/O/R/N/H0 " + "/".join(_w(res[(C2, L)]['arms'][a]['hold'], 'y', 'n') for a in ARMS2)
                        + "; pool unit-steps W/O/R/N/H0 " + "/".join(f"{float(res[(C2, L)]['arms'][a]['pool']):.4f}" for a in ARMS2) for L in L2S)
    idle_dec = res[(C2, L2_DEC)]["y"]["idle"]
    pool_r, pool_h0 = float(dec["ETM-R"]["pool"]), float(dec["H0"]["pool"])
    return gate_open, make_row(
        "eps", f"T2 a shared resource, competitors take the paused agent's share (model: N = {N2} agents, C = {C2} units one each, pause L in {{5, 20}} steps, competitors "
               f"below a {CAP2}-unit cap claim the idle unit with probability {_g(QC2)} per step each, a claimed unit returns with probability {_g(RHO2)} per step after "
               f"the pause, progress 1 per own step per unit over {T2_OWN} own steps, hold at c = {_g(C2_HOLD)} per paused step; G-NEG world C = {C2_NEG}; exact "
               f"Markov-chain expectations in rational arithmetic)",
        source=f"EPS2 T2 (declared at {DECL_AT}; forecast REDUNDANT-DOMAIN)",
        Q="Without a reservation, OWN's and ETM-N's stakes are not zero, because the world does not wait (the resource is lost), and the agent pays to hold whenever "
          "its stake exceeds c L. With the reservation (ETM-R), the stake is zero and it never holds (declaration's Q, ASCII). Decisive quantity: ETM-N's stake at L = 20",
        ingredient=f"{ING} and E3, the world that does not wait: ETM-N values progress per own step with a true map of the pause but reads the unit it holds, which "
                   f"competitors may take while it is paused; ETM-R adds a reservation, which removes that dependence",
        null=f"ETM-R's stake at L = {L2_DEC} (SCORING MAPPING, the investigator's operationalisation fixed before this run: crr = ETM-N's stake at L = 20, null = ETM-R's "
             f"stake at L = 20, the reservation being the ablated part, domain = H0's stake at L = 20, check = Q holds)",
        domain="H0: a fair-share scheduler with a preemption credit, the unit lent during the pause and returned at resume, scored on the null's own-step valuation",
        numbers=f"stake at L = {L2_DEC}: ETM-N {crr:.12f}, ETM-R {null:g}, H0 {dom:g} (wall-clock reading of H0: {float(dec['H0']['stake_wall']):g}), OWN "
                f"{float(dec['OWN']['stake']):.12f}, WALL {float(dec['WALL']['stake']):.12f}; per L (scarce world): {percell}; OWN and ETM-N identical in every cell and "
                f"field: {_w(own_eq, 'yes', 'no')}; expected idle paused steps of the unlent unit at L = {L2_DEC}: {float(idle_dec):.6f}; the reservation idles the unit "
                f"for the whole pause: pool {pool_r:.4f} unit-steps against {pool_h0:.4f} under H0; closed form identical to the chain: {_w(cf_ok, 'yes', 'no')}; "
                f"G-POS threshold c < {float(c_star):.6f}; gate {_w(gate_open, 'OPEN', 'CLOSED')}",
        tg=f"ETM-N stake {crr:.6f} vs null (ETM-R) {null:g}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (rel {rel(crr, null):.4f})",
        tn=f"H0 (preemption credit, return at resume) stake {dom:g}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has the stake)', 'differ')} (rel {rel(crr, dom):.4f})",
        tc=f"OWN's and ETM-N's stakes != 0 at every L: {_w(qa, 'yes', 'no')}; OWN and ETM-N hold exactly when stake > c L at every L and every c in "
           f"{{{', '.join(_g(c) for c in C2_GRID)}}}: {_w(qb, 'yes', 'no')}; ETM-R's stake == 0 exactly at every L (both worlds) and it never holds at any c: "
           f"{_w(qc_, 'yes', 'no')}: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"own-clock indexing {_w(crr != 0, 'does not empty', 'empties')} this pause: competitors claim the idle unit with probability "
                f"{float(res[(C2, L2_DEC)]['y']['p']):.4f} over L = {L2_DEC} and it comes back at rate {_g(RHO2)} per step, so ETM-N's stake is {crr:.4f} progress units, "
                f"{_w(own_eq, 'identical to OWN', 'different from OWN')}, and it would pay c L = {float(C2_HOLD * L2_DEC):g} to hold "
                f"({_w(dec['ETM-N']['hold'], 'it does', 'it does not')} at c = {_g(C2_HOLD)}); the reservation (ETM-R) and the scheduler's return at resume (H0) "
                f"{_w(null == 0 and dom == 0, 'both make the stake 0', 'do not both make the stake 0')} and "
                f"{_w(not dec['ETM-R']['hold'] and not dec['H0']['hold'], 'neither holds', 'one of them holds')}; for the pool the reservation idles the unit for the "
                f"whole pause ({pool_r:.2f} unit-steps) while H0 lends it out and still returns it ({pool_h0:.2f}, "
                f"{_w(pool_h0 > pool_r, 'more', 'not more')}); "
                f"{_w(out == 'ADDS' and null == 0 and dom == 0, 'the ADDS compares a non-zero stake with two zero stakes, as Q predicted: it records that the empty cut needs the reservation, which the domain supplies as preemption with return, not an addition by ETM', 'the label is as computed')}",
        weakness=f"CHOICE: each competitor below a cap of {CAP2} units claims the idle unit with probability {_g(QC2)} per paused step, attempt at the start of a step "
                 f"(claim hazard h = 1 - (1 - q)^claimants); a claimed unit stays with its claimant for the rest of the pause and returns with probability "
                 f"{_g(RHO2)} at the end of each step after it (the first post-pause step is always without it); spare units are taken by competitors before the "
                 f"pause up to the cap, so C = {C2_NEG} leaves every competitor at its cap and a free spare; progress valued over {T2_OWN} own steps after the pause "
                 f"(WALL: the L + {T2_OWN} wall steps from the pause start); hold = the unit is kept for the pause at c = {_g(C2_HOLD)} per paused step, a tie does not "
                 f"act; the stake is the pause as it comes (without holding); ETM-N is own clock and true map without a reservation and equals OWN here (the unit is "
                 f"what the pause changes); H0 scored on the null's own-step valuation with the scheduler's return at resume replacing the reservation, as EPS1 S1 "
                 f"scored its H0; principal's outcome = pool unit-steps. LABEL-DECIDING READINGS (alternatives computed): (1) EPS1's default null (OWN's stake) "
                 f"-> {out_own}, since ETM-N equals OWN; (2) H0 on a wall-clock valuation (stake L = {float(dec['H0']['stake_wall']):g}) -> {out_h0w}; (3) the gate "
                 f"turns on c: at c >= {float(c_star):.4f} per step no arm holds and G-POS fails (GATE CLOSED); q and rho_back move the stake's size, not its sign; "
                 f"sources named, not fetched",
        elegance="", child="")


def main():
    print(f"EPS2 batch 01: T1 (demand response) and T2 (a shared resource), from Empty_Pause_Systems/DECLARATION_EPS2.md (declared at {DECL_AT})")
    print()
    g1, r1 = run_t1()
    g2, r2 = run_t2()
    return run_batch(f"EPS2 batch 01 rows (SYNTHESIS harness; declared at {DECL_AT})", [r1, r2])


if __name__ == "__main__":
    sys.exit(main())
