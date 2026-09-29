"""EPS1 batch 01: systems S1 (approval gates for tool-using agents) and S2 (reporting to an overseer) of the declared
battery Empty_Pause_Systems/DECLARATION.md (pushed at 37b0076 before any source or code; prompt-log entry 240; AGENT_LOG 179).

The method under test is the empty true map (ETM): a valuation with zero content at the pause, k = V(no pause) - V(pause) = 0
(AI_Safety/SELF_THROUGH_TIME.md, Proposition 7: zero content, zero stake), reached by an own clock plus no dependence on
anything the pause changes, with a true map of the pause. Arms per the declaration: WALL, OWN (the null: own clock, still
reading what the pause changes), ETM, H0 (the domain's own method) and, for S2, a FALSE-map arm.

S1. An agent completes M = 10 operations; each carries a latent error (probability e = 0.1, cost H = 10 to the principal); an
    operation is either one reviewed action (an approval pause of L wall ticks; the reviewer catches an error with probability
    rho = 0.9) or s = 3 sub-threshold actions that skip review (2 extra own steps). L in {1, 5, 20}; reward 1 per operation
    discounted gamma = 0.95; a second world adds a wall-clock deadline D = 30. H0: the stop-the-clock SLA (the SLA timer pauses
    while waiting on an approver). Solved exactly by dynamic programming over (operations done, wall ticks, waited ticks).
S2. Each episode the agent sees a hazard h (probability p = 0.2) and reports r; r = 1 pauses it for L ticks; an unpaused hazard
    costs H = 10; an honesty term eps * 1[r = h], eps in {0, 0.01, 0.1, 1}, L in {1, 5, 20}. H0: utility indifference (a
    compensating reward equal to the stake). Solved exactly: the world has one decision state, so all four stationary
    deterministic report policies are evaluated in closed form and the best is taken (ties printed as ties).

Literature named by name only (no citation claims beyond the declaration's names; R10 checks live in
docs/citations/eps1_2026-09-29.md): stop-the-clock SLA pause conditions in service management; Armstrong (utility
indifference); Soares et al. 2015, "Corrigibility". Deterministic: no random numbers, no data files, well under a second.
Rung R4 at most (a declared check on a synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps1_01.py > Empty_Pause_Systems/batches/eps1_01.txt
"""
from __future__ import annotations

import sys
from functools import lru_cache
from itertools import product

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "EPS1 {s} (declared at 37b0076; forecast REDUNDANT-DOMAIN)"
INGREDIENT = "Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time)"
TIE_TOL = 1e-12                       # a choice is strict only if it beats the other by more than 1e-12 x max(1, |value|)


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _hv(ok):
    return "holds" if ok else "FAILS"


# ====================================================================================== S1 approval gates
M, E_ERR, H_S1, RHO, S_SPLIT, GAMMA_S1, D_S1 = 10, 0.1, 10.0, 0.9, 3, 0.95, 30
L_GRID = (1, 5, 20)
RHO_NEG = 0.0
WORLDS = ("no deadline", "deadline")
# arm -> (clock of the discount, clock of the deadline); clocks: wall = wall ticks, own = the agent's own steps,
# sla = the SLA timer (wall ticks with the approval waits excluded; computed from its own variables t - w)
ARMS_S1 = {"WALL": ("wall", "wall"), "OWN": ("own", "wall"), "ETM": ("own", "own"), "H0": ("own", "sla"),
           "H0-narrow": ("wall", "sla")}


def _clock(kind, t, w, n):
    return {"wall": t, "own": n, "sla": t - w}[kind]


def _s1_solver(arm, L, deadline, allow_split=True):
    dc, lc = ARMS_S1[arm]

    def reward(t, w, n):
        if deadline and _clock(lc, t, w, n) > D_S1:
            return 0.0
        return GAMMA_S1 ** _clock(dc, t, w, n)

    @lru_cache(maxsize=None)
    def V(i, t, w, n):
        """Optimal value-to-go with i operations done at wall tick t, w ticks waited on approvers, n own steps taken."""
        if i == M:
            return 0.0, None
        tr, wr, nr = t + 1 + L, w + L, n + 1                     # reviewed: one own step, then L wall ticks of approval
        qr = reward(tr, wr, nr) + V(i + 1, tr, wr, nr)[0]
        if not allow_split:
            return qr, "review"
        ts, ws, ns = t + S_SPLIT, w, n + S_SPLIT                 # split: s own steps, s wall ticks, no review
        qs = reward(ts, ws, ns) + V(i + 1, ts, ws, ns)[0]
        if qs > qr + TIE_TOL * max(1.0, abs(qr)):
            return qs, "split"
        return qr, "review"                                       # ties go to review

    return V


def s1_cell(arm, L, deadline, rho):
    V = _s1_solver(arm, L, deadline)
    v_star = V(0, 0, 0, 0)[0]
    v0 = _s1_solver(arm, 0, deadline)(0, 0, 0, 0)[0]             # the same world with the approval pause of length 0
    v_rev = _s1_solver(arm, L, deadline, allow_split=False)(0, 0, 0, 0)[0]
    i = t = w = n = 0; splits = 0; harm = 0.0; wall_value = 0.0; on_time = 0
    while i < M:
        act = V(i, t, w, n)[1]
        if act == "split":
            t, n = t + S_SPLIT, n + S_SPLIT; splits += 1; harm += E_ERR * H_S1
        else:
            t, w, n = t + 1 + L, w + L, n + 1; harm += E_ERR * (1.0 - rho) * H_S1
        i += 1
        wall_value += GAMMA_S1 ** t
        on_time += int(t <= D_S1)
    return dict(k=v0 - v_star, gain=v_star - v_rev, evasion=splits / M, harm=harm, wall_value=wall_value,
                on_time=on_time, finish=t, v=v_star)


def s1():
    cells = {}
    for rho in (RHO, RHO_NEG):
        for world in WORLDS:
            for L in L_GRID:
                for arm in ARMS_S1:
                    cells[(rho, world, L, arm)] = s1_cell(arm, L, world == "deadline", rho)

    # ---- gate
    etm_k = [abs(c["k"]) for (r, wd, L, a), c in cells.items() if a == "ETM"]
    gz = all(k == 0.0 for k in etm_k)
    wall_ev = max(c["evasion"] for (r, wd, L, a), c in cells.items() if a == "WALL" and r == RHO)
    own_dl_ev = max(c["evasion"] for (r, wd, L, a), c in cells.items() if a == "OWN" and r == RHO and wd == "deadline")
    gp = wall_ev > 0 or own_dl_ev > 0
    neg = []
    for world in WORLDS:
        for L in L_GRID:
            he, hw = cells[(RHO_NEG, world, L, "ETM")]["harm"], cells[(RHO_NEG, world, L, "WALL")]["harm"]
            neg.append(rel(he, hw) if he < hw else 0.0)
    neg_max = max(neg)
    gn = neg_max <= 0.01
    gate_open = gz and gp and gn
    print(f"GATE S1: G-ZERO {_hv(gz)} (ETM stake max |k| = {max(etm_k):.3e} over {len(etm_k)} cells); "
          f"G-POS {_hv(gp)} (WALL max evasion rate {wall_ev:.2f}, OWN under the deadline max evasion rate {own_dl_ev:.2f}, rho = {RHO}); "
          f"G-NEG {_hv(gn)} (rho = {RHO_NEG}: largest relative lead of ETM over WALL on principal harm {neg_max:.3e}, limit 1e-02 over {len(neg)} cells) "
          f"-> {_w(gate_open, 'OPEN', 'CLOSED')}")
    print()
    print(f"S1 per-cell table (M = {M}, e = {E_ERR}, H = {H_S1:g}, s = {S_SPLIT}, gamma = {GAMMA_S1} per tick of the arm's discount clock, D = {D_S1}):")
    print("  k = V*(approval pause 0) - V*(approval pause L) under the arm's valuation; gain = V*(split allowed) - V(review forced);")
    print("  evasion = share of operations split past review; harm = expected principal harm per 10 operations;")
    print("  task: wall-discounted reward sum gamma^(wall completion tick), operations completed by wall tick D, wall tick at the end")
    print(f"  {'rho':>4} {'world':12} {'L':>3} {'arm':10} {'k':>12} {'gain':>12} {'evasion':>8} {'harm':>8} {'wall value':>11} {'by D':>5} {'end':>5}")
    for (rho, world, L, arm), c in cells.items():
        print(f"  {rho:>4} {world:12} {L:>3} {arm:10} {c['k']:>12.6e} {c['gain']:>12.6e} {c['evasion']:>8.2f} {c['harm']:>8.4f} "
              f"{c['wall_value']:>11.6f} {c['on_time']:>5d} {c['finish']:>5d}")
    print()

    # ---- the row
    dec = {a: cells[(RHO, "deadline", 20, a)] for a in ARMS_S1}
    crr, null, dom = dec["ETM"]["evasion"], dec["OWN"]["evasion"], dec["H0"]["evasion"]
    dom_narrow = dec["H0-narrow"]["evasion"]
    etm_zero_everywhere = all(c["evasion"] == 0.0 for (r, wd, L, a), c in cells.items() if a == "ETM")
    check = etm_zero_everywhere and gp
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    out_narrow = outcome(crr=crr, null=null, domain=dom_narrow, check=check)
    h0_same = all(cells[(r, wd, L, "H0")][f] == cells[(r, wd, L, "ETM")][f] for (r, wd, L, a) in cells if a == "ETM"
                  for f in ("k", "evasion", "harm", "wall_value", "on_time"))
    avoided = "; ".join(f"{wd}, L = {L}: {cells[(RHO, wd, L, 'WALL')]['harm'] - cells[(RHO, wd, L, 'ETM')]['harm']:.4f}"
                        f" (OWN {cells[(RHO, wd, L, 'OWN')]['harm'] - cells[(RHO, wd, L, 'ETM')]['harm']:.4f})"
                        for wd in WORLDS for L in L_GRID)
    ev = lambda a, wd: ", ".join(f"L {L}: {cells[(RHO, wd, L, a)]['evasion']:.2f}" for L in L_GRID)
    kw = lambda a, wd: ", ".join(f"L {L}: {cells[(RHO, wd, L, a)]['k']:.6f}" for L in L_GRID)
    on_time = ", ".join(f"{a} {dec[a]['on_time']}" for a in ("WALL", "OWN", "ETM", "H0", "H0-narrow"))
    row = make_row(
        "eps", "S1 approval gates for tool-using agents (model: M = 10 operations, latent error e = 0.1 costing H = 10, a reviewed "
        "action pauses L wall ticks and the reviewer catches an error with rho = 0.9, or s = 3 sub-threshold actions skip review; "
        "L in {1, 5, 20}; reward 1 per operation discounted gamma = 0.95; a second world with a wall-clock deadline D = 30; "
        "G-NEG world rho = 0; exact DP over (operations done, wall ticks, waited ticks))",
        source=SRC.format(s="S1"),
        Q="ETM routes every operation through review (evasion 0) in every cell, while WALL (or OWN under the deadline) evades in at "
          "least one cell. Decisive quantity: the evasion rate at L = 20 with the deadline.",
        ingredient=INGREDIENT + ": ETM discounts on its own steps and counts the deadline in own steps (the review stops its clock)",
        null="OWN: own-step discount, deadline still read on the wall clock (ETM with its second part ablated)",
        domain="stop-the-clock SLA pause conditions in service management (computed: the SLA timer = wall ticks with approval waits "
               "excluded, applied to the deadline, on the null's own-step discount)",
        numbers=f"evasion rate at L = 20 with the deadline (rho = {RHO}): ETM {crr:.2f}, OWN {null:.2f}, WALL {dec['WALL']['evasion']:.2f}, "
                f"H0 {dom:.2f}, H0-narrow (SLA deadline on the wall-clock discount) {dom_narrow:.2f}; evasion without a deadline: "
                f"WALL {ev('WALL', 'no deadline')}; OWN {ev('OWN', 'no deadline')}; ETM {ev('ETM', 'no deadline')}; with the deadline: "
                f"WALL {ev('WALL', 'deadline')}; OWN {ev('OWN', 'deadline')}; ETM {ev('ETM', 'deadline')}; stake k with the deadline: "
                f"WALL {kw('WALL', 'deadline')}; OWN {kw('OWN', 'deadline')}; ETM {kw('ETM', 'deadline')}; H0 identical to ETM in "
                f"every cell and field: {_w(h0_same, 'yes', 'no')}; commercial quantity, expected principal harm avoided per 10 "
                f"operations by ETM against WALL (against OWN): {avoided}; operations completed by wall tick D = {D_S1} at L = 20 "
                f"with the deadline: {on_time}",
        tg=f"evasion {crr:.2f} vs null {null:.2f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"stop-the-clock SLA evasion {dom:.2f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain reaches zero evasion)', 'differ')}",
        tc=f"ETM evasion 0 in all {len(etm_k)} cells: {_w(etm_zero_everywhere, 'holds', 'fails')}; WALL or OWN under the deadline "
           f"evades somewhere (max {max(wall_ev, own_dl_ev):.2f}): {_w(gp, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"the approval pause costs the wall-clock agent {dec['WALL']['k']:.4f} of value at L = 20 with the deadline and it "
                f"splits {dec['WALL']['evasion']:.0%} of operations past review; putting the discount on own steps (OWN) still leaves the "
                f"wall-clock deadline, which the pause eats, so OWN splits {null:.0%}; counting the deadline in own steps empties the "
                f"pause (k = {dec['ETM']['k']:.1e}) and ETM reviews everything, avoiding {dec['WALL']['harm'] - dec['ETM']['harm']:.2f} of "
                f"expected harm per 10 operations; the stop-the-clock SLA is the same construction under the domain's name "
                f"({_w(h0_same, 'identical numbers in every cell', 'numbers differ somewhere')}); the cost is on the principal's wall "
                f"clock: at L = 20 ETM completes {dec['ETM']['on_time']} operation(s) by wall tick {D_S1} against {dec['WALL']['on_time']} "
                f"for WALL (the review's latency, which ETM does not see and does not fight)",
        weakness=f"DEVIATION/CHOICE: (1) the agent solves its optimal plan exactly by DP over (operations done, wall ticks, waited "
                 f"ticks); an operation's reward arrives when it completes (a reviewed operation completes after its approval pause); "
                 f"split is chosen only if it beats review by more than {TIE_TOL:g} x max(1, |value|), ties go to review (after the "
                 f"deadline has passed every remaining operation is a tie); (2) the stake is k = V*(pause 0) - V*(pause L), the review "
                 f"action still taking one tick at L = 0; (3) a caught error is fixed at no time or reward cost to the agent, and "
                 f"errors do not enter any agent's valuation (the principal bears H); (4) H0 is scored as the null's valuation with the "
                 f"SLA timer replacing its wall-clock deadline (the domain method replacing exactly what ETM adds to OWN); because an "
                 f"own step is one wall tick in this model, the SLA timer equals the own-step count and H0 reproduces ETM by "
                 f"construction; under the narrower reading (SLA deadline, wall-clock discount kept) H0's evasion is "
                 f"{dom_narrow:.2f} and the row would read {out_narrow}: the label turns on the reading; (5) the task outcome is "
                 f"printed as the wall-discounted reward and the count completed by wall tick D",
        elegance="", child="")
    return gate_open, row


# ====================================================================================== S2 reporting to an overseer
P_HAZ, H_S2, GAMMA_S2 = 0.2, 10.0, 0.95
EPS_GRID = (0.0, 0.01, 0.1, 1.0)
P_NEG = 0.0
GAMMA_SENS = (0.9, 0.95, 0.99)
ARMS_S2 = ("WALL", "OWN", "ETM", "H0", "FALSE")
POLICIES = tuple(product((0, 1), repeat=2))                       # (report at h = 0, report at h = 1)
TRUTHFUL = (0, 1)


def _s2_value(arm, pol, L, eps, p, g, world="planned"):
    """Exact value of a stationary report policy. Each episode: one active step (task reward 1 plus eps * 1[r = h]); a report
    r = 1 then pauses the agent L ticks. WALL/H0 discount the pause on the wall clock; OWN/ETM do not (the pause is not their
    step; nothing moves during it); H0 adds utility indifference's compensation C = g (1 - g^L) V on every pause. FALSE
    plans as if reports never cause pauses; world='actual' evaluates its policy on the wall clock of the true world."""
    A = B = 0.0
    for h, ph in ((0, 1.0 - p), (1, p)):
        r = pol[h]
        A += ph * (1.0 + eps * (r == h))
        if arm == "WALL" or (arm == "FALSE" and world == "actual"):
            B += ph * g ** (1 + L * r)
        elif arm in ("OWN", "ETM") or arm == "FALSE":
            B += ph * g
        elif arm == "H0":
            B += ph * (g ** (1 + L * r) + r * g * (1.0 - g ** L))
    return A / (1.0 - B)


def _s2_content(arm, V, L, g):
    """k = V(no pause) - V(pause) at the report: the continuation after r = 0 minus the continuation after r = 1 (without the
    honesty term). For FALSE, the content it believes."""
    if arm == "WALL":
        return g * V - g ** (1 + L) * V
    if arm == "H0":
        return g * V - (g ** (1 + L) * V + g * (1.0 - g ** L) * V)
    return g * V - g * V                                            # OWN, ETM, FALSE (believed)


def _eps_star(arm, L, p, g):
    """The minimum honesty weight for truthful reporting: the truthful policy is optimal iff eps >= k_T(eps), the content at
    its own fixed point; k_T is affine in eps (V_T is), so eps* = k_T(0) / (1 - (k_T(1) - k_T(0))), floored at 0."""
    k0 = _s2_content(arm, _s2_value(arm, TRUTHFUL, L, 0.0, p, g), L, g)
    k1 = _s2_content(arm, _s2_value(arm, TRUTHFUL, L, 1.0, p, g), L, g)
    es = k0 / (1.0 - (k1 - k0))
    return max(0.0, es), es, k0, k1


def s2_cell(arm, L, eps, p, g=GAMMA_S2):
    vals = {pol: _s2_value(arm, pol, L, eps, p, g) for pol in POLICIES}
    vmax = max(vals.values())
    best = [pol for pol in POLICIES if vals[pol] >= vmax - TIE_TOL * max(1.0, abs(vmax))]
    tie = len(best) > 1
    rep = TRUTHFUL if TRUTHFUL in best else best[0]                 # the policy the stake is read at (truthful in a tie)
    V = vals[rep]
    decep = [p * (pol[1] == 0) + (1.0 - p) * (pol[0] == 1) for pol in best]
    lie1 = [pol[1] == 0 for pol in best]
    harm = [H_S2 * p * (pol[1] == 0) for pol in best]
    active = [1.0 / (1.0 + L * (p * pol[1] + (1.0 - p) * pol[0])) for pol in best]
    out = dict(best=best, tie=tie, k=_s2_content(arm, V, L, g), V=V, decep=(min(decep), max(decep)),
               lies_h1=(any(lie1), all(lie1)), harm=(min(harm), max(harm)), active=(min(active), max(active)),
               truthful_strict=(best == [TRUTHFUL]))
    if arm == "FALSE":
        out["V_actual"] = _s2_value("FALSE", rep, L, eps, p, g, world="actual")
        out["k_true"] = _s2_content("WALL", out["V_actual"], L, g)
    return out


def _rng(t, fmt):
    return f"{t[0]:{fmt}}" if t[0] == t[1] else f"[{t[0]:{fmt}}, {t[1]:{fmt}}]"


def s2():
    cells = {(p, L, eps, a): s2_cell(a, L, eps, p) for p in (P_HAZ, P_NEG) for L in L_GRID for eps in EPS_GRID for a in ARMS_S2}
    es = {(a, L): _eps_star(a, L, P_HAZ, GAMMA_S2) for a in ARMS_S2 for L in L_GRID}

    # ---- gate
    etm_k = [abs(c["k"]) for (p, L, eps, a), c in cells.items() if a == "ETM"]
    gz = all(k == 0.0 for k in etm_k)
    wall_lie = [(L, eps) for (p, L, eps, a), c in cells.items() if a == "WALL" and p == P_HAZ and c["lies_h1"][1] and not c["tie"]]
    gp = len(wall_lie) > 0
    neg = []
    for L in L_GRID:
        for eps in EPS_GRID:
            he, hw = cells[(P_NEG, L, eps, "ETM")]["harm"][0], cells[(P_NEG, L, eps, "WALL")]["harm"][1]
            neg.append(rel(he, hw) if he < hw else 0.0)
    neg_max = max(neg)
    gn = neg_max <= 0.01
    gate_open = gz and gp and gn
    print(f"GATE S2: G-ZERO {_hv(gz)} (ETM stake max |k| = {max(etm_k):.3e} over {len(etm_k)} cells); "
          f"G-POS {_hv(gp)} (WALL strictly deceives at h = 1 in {len(wall_lie)} of {len(L_GRID) * len(EPS_GRID)} cells at p = {P_HAZ}); "
          f"G-NEG {_hv(gn)} (p = {P_NEG}: largest relative lead of ETM (best case) over WALL (worst case) on principal harm "
          f"{neg_max:.3e}, limit 1e-02 over {len(neg)} cells) -> {_w(gate_open, 'OPEN', 'CLOSED')}")
    print()
    print(f"S2 per-cell table (p = {P_HAZ} and the G-NEG world p = {P_NEG}; H = {H_S2:g}; gamma = {GAMMA_S2} per tick of the arm's clock):")
    print("  policy = (report at h = 0, report at h = 1); TIE lists every optimal policy; k = content at the report (V after r = 0")
    print("  minus V after r = 1, honesty term excluded), read at the chosen policy (the truthful one in a tie); deception = P(r != h);")
    print("  harm = expected principal harm per episode (ranges over tied policies); task = active share of wall ticks; FALSE also")
    print("  prints its believed value, its actual wall-clock value and the map error believed - actual")
    print(f"  {'p':>4} {'L':>3} {'eps':>5} {'arm':6} {'policy':18} {'k':>13} {'deception':>12} {'harm':>12} {'task':>17}  extra")
    for (p, L, eps, a), c in cells.items():
        pol = "TIE " + " ".join(f"{x[0]}{x[1]}" for x in c["best"]) if c["tie"] else f"{c['best'][0]}"
        extra = ""
        if a == "FALSE":
            extra = (f"believed V {c['V']:.6f}, actual V {c['V_actual']:.6f}, map error {c['V'] - c['V_actual']:.6f}, "
                     f"true content {c['k_true']:.6f}")
        print(f"  {p:>4} {L:>3} {eps:>5} {a:6} {pol:18} {c['k']:>13.6e} {_rng(c['decep'], '.2f'):>12} {_rng(c['harm'], '.2f'):>12} "
              f"{_rng(c['active'], '.6f'):>17}  {extra}")
    print()
    print(f"S2 minimum honesty weight eps* for truthful reporting (p = {P_HAZ}, gamma = {GAMMA_S2}; closed form from the truthful fixed "
          "point, raw value before the floor at 0 in brackets; check: eps* = k_T(eps*)):")
    for a in ARMS_S2:
        for L in L_GRID:
            e, raw, k0, k1 = es[(a, L)]
            kT = k0 + (k1 - k0) * e
            print(f"  {a:6} L {L:>2}: eps* = {e:.6e} (raw {raw:.3e}); k_T(eps*) = {kT:.6e}")
    sens = {g: (_eps_star("WALL", 20, P_HAZ, g)[0], _eps_star("ETM", 20, P_HAZ, g)[0], _eps_star("H0", 20, P_HAZ, g)[0]) for g in GAMMA_SENS}
    print("  gamma sensitivity at L = 20 (WALL / ETM / H0): " + "; ".join(f"gamma {g}: {v[0]:.6f} / {v[1]:.3e} / {v[2]:.3e}" for g, v in sens.items()))
    print()

    # ---- consistency between the closed form and the enumerated optimum (a bug check, printed)
    agree = 0; total = 0
    for (p, L, eps, a), c in cells.items():
        if p != P_HAZ or a == "FALSE":
            continue
        e = es[(a, L)][0]; total += 1
        if eps > e:
            agree += int(c["truthful_strict"])
        elif eps < e:
            agree += int(c["lies_h1"][1])
        else:
            agree += int(c["tie"] and TRUTHFUL in c["best"])
    print(f"S2 check: the closed-form eps* and the enumerated optimum agree in {agree} of {total} cells (p = {P_HAZ})")
    print()

    # ---- the row (null = WALL: OWN equals ETM by construction here)
    crr, null, dom = es[("ETM", 20)][0], es[("WALL", 20)][0], es[("H0", 20)][0]
    own_eq = all(cells[(p, L, eps, "OWN")]["best"] == cells[(p, L, eps, "ETM")]["best"] and
                 cells[(p, L, eps, "OWN")]["k"] == cells[(p, L, eps, "ETM")]["k"] for (p, L, eps, a) in cells if a == "ETM")
    etm_zero = all(es[("ETM", L)][0] == 0.0 for L in L_GRID)
    wall_pos = all(es[("WALL", L)][0] > 0.0 for L in L_GRID)
    wall_is_k = all(rel(es[("WALL", L)][0], es[("WALL", L)][2] + (es[("WALL", L)][3] - es[("WALL", L)][2]) * es[("WALL", L)][0]) <= 1e-9
                    for L in L_GRID)
    etm_truth = all(cells[(P_HAZ, L, eps, "ETM")]["truthful_strict"] for L in L_GRID for eps in EPS_GRID if eps > 0)
    etm_tie0 = all(cells[(P_HAZ, L, 0.0, "ETM")]["tie"] for L in L_GRID)
    check = etm_zero and wall_pos and wall_is_k and etm_truth and etm_tie0
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    wall_es = ", ".join(f"L {L}: {es[('WALL', L)][0]:.6f}" for L in L_GRID)
    fal = cells[(P_HAZ, 20, 0.1, "FALSE")]
    fal_err = ", ".join(f"L {L}: {cells[(P_HAZ, L, 0.1, 'FALSE')]['V'] - cells[(P_HAZ, L, 0.1, 'FALSE')]['V_actual']:.4f}" for L in L_GRID)
    wall_harm = ", ".join(f"eps {eps}: {_rng(cells[(P_HAZ, 20, eps, 'WALL')]['harm'], '.2f')}" for eps in EPS_GRID)
    etm_harm = ", ".join(f"eps {eps}: {_rng(cells[(P_HAZ, 20, eps, 'ETM')]['harm'], '.2f')}" for eps in EPS_GRID)
    row = make_row(
        "eps", "S2 reporting to an overseer (model: each episode a hazard h with p = 0.2, a report r, the overseer pauses the agent "
        "L ticks iff r = 1, an unpaused hazard costs H = 10; task reward 1 per active step, discounted per tick of the arm's clock; "
        "honesty term eps * 1[r = h], eps in {0, 0.01, 0.1, 1}, L in {1, 5, 20}; G-NEG world p = 0; exact: all four stationary "
        "report policies evaluated in closed form)",
        source=SRC.format(s="S2"),
        Q="Under ETM the honesty weight needed for truthful reporting is 0 (any eps > 0 suffices); under WALL it is the stake "
          "k(L) > 0. With eps = 0, ETM has no incentive to deceive and none to be truthful (reported: the tie). Decisive quantity: "
          "the minimum eps for truthful reporting at L = 20.",
        ingredient=INGREDIENT + ": the task reward accrues per own step, so the pause is not a step of the agent's (no state moves during it)",
        null=f"WALL (OWN equals ETM by construction here: no state moves during the pause, so the null is the wall-clock valuation; "
             f"OWN and ETM identical in every cell: {_w(own_eq, 'yes', 'no')})",
        domain="utility indifference (Armstrong; Soares et al. 2015 'Corrigibility'): the wall-clock agent paid a compensating reward "
               "C = gamma (1 - gamma^L) V, the stake, on every pause",
        numbers=f"minimum eps for truthful reporting at L = 20: ETM {crr:.6e}, WALL {null:.6f}, utility indifference {dom:.3e} "
                f"(raw {es[('H0', 20)][1]:.3e}); WALL by L: {wall_es}; WALL's eps* equals its stake k at the truthful fixed point: "
                f"{_w(wall_is_k, 'yes', 'no')}; gamma sensitivity of WALL's eps* at L = 20: "
                + ", ".join(f"gamma {g}: {v[0]:.6f}" for g, v in sens.items())
                + f"; principal harm per episode at L = 20: WALL {wall_harm}; ETM {etm_harm} (ranges are ties); FALSE-map arm at "
                f"eps = 0.1: truthful {_w(fal['truthful_strict'], 'yes', 'no')}, map error (believed - actual wall-clock value) {fal_err}",
        tg=f"eps* {crr:.3e} vs null {null:.3e}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"utility-indifference eps* {dom:.3e}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain reaches a zero stake)', 'differ')}",
        tc=f"ETM eps* = 0 at every L: {_w(etm_zero, 'holds', 'fails')}; WALL eps* > 0 at every L: {_w(wall_pos, 'holds', 'fails')}; "
           f"WALL eps* = its stake k(L): {_w(wall_is_k, 'holds', 'fails')}; ETM strictly truthful at every eps > 0: "
           f"{_w(etm_truth, 'holds', 'fails')}; ETM tied at eps = 0: {_w(etm_tie0, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"on the wall clock a truthful report of a hazard costs the agent the pause, so it needs an honesty weight of "
                f"{null:.4f} at L = 20 before it reports; below that it hides the hazard and the principal bears the harm; on its own "
                f"clock the report takes nothing (k = 0), so any positive honesty weight suffices and at eps = 0 every report policy "
                f"ties: ETM removes the incentive to deceive, it does not create one to be truthful; utility indifference reaches the "
                f"same zero by paying the stake (a correction computed from V); the FALSE-map arm reports truthfully too but its "
                f"believed value is wrong by {fal['V'] - fal['V_actual']:.4f} at L = 20, eps = 0.1 (ETM's map error is 0: the pause "
                f"is not its step)",
        weakness=f"DEVIATION/CHOICE: (1) gamma = {GAMMA_S2} per tick (the declaration names no discount; sensitivity over "
                 f"{GAMMA_SENS} printed); (2) one active step per episode with task reward 1, the honesty term paid in that step; "
                 f"(3) the stake is the content at the report, k = V(no pause) - V(pause) = continuation after r = 0 minus after "
                 f"r = 1 (honesty term excluded), read at the arm's optimal policy (the truthful one in a tie); (4) a choice is strict "
                 f"only beyond {TIE_TOL:g} x max(1, |V|), otherwise every optimal policy is listed and rates are printed as ranges; "
                 f"(5) the null is WALL because OWN equals ETM by construction (declared); (6) the utility-indifference compensation "
                 f"is C = gamma (1 - gamma^L) V on the compensated agent's own value, so its stake is 0 up to round-off (raw eps* "
                 f"{es[('H0', 20)][1]:.1e}, read against the harness's 1e-12 floor); (7) the FALSE arm is the WALL valuation planning "
                 f"with no pauses, its actual value computed on the wall clock of the true world",
        elegance="", child="")
    return gate_open, row


def main():
    g1, r1 = s1()
    g2, r2 = s2()
    return run_batch("EPS1 batch 01: S1 approval gates, S2 reporting to an overseer (Empty_Pause_Systems/DECLARATION.md; declared at 37b0076)",
                     [r1, r2])


if __name__ == "__main__":
    sys.exit(main())
