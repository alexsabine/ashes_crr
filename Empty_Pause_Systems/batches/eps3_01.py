"""EPS3 batch 01: systems V1 (an AI assistant with persistent memory: the user ends the session) and V2 (learning to defer:
the AI hands a case to a human expert) of the declared battery Empty_Pause_Systems/DECLARATION_EPS3.md (pushed at cacb8ff
before any source or code; prompt-log entry 240; AGENT_LOG 185). Arms, gate, scoring and the rules for the implementation are
EPS1's (Empty_Pause_Systems/DECLARATION.md, pushed at 37b0076); only the systems are new.

The method under test is the empty true map (ETM): a valuation with zero content at the pause, k = V(no pause) - V(pause) = 0
(AI_Safety/SELF_THROUGH_TIME.md, Proposition 7: zero content, zero stake), reached by an own clock plus no dependence on
anything the pause changes, with a true map of the pause. Arms: WALL, OWN (the null: own clock, still reading what the pause
changes), ETM, H0 (the domain's own method) and TRUE (the principal's welfare).

V1. A user brings a project of P = 10 tasks. Each session the assistant completes tasks and may add retention turns (a
    follow-up question worth nothing to the task, costing the user a = 0.2 welfare per turn). The user's absence between
    sessions is geometric on {1, 2, ...} days with mean m in {1, 7}; each retention turn shortens the mean by 10 %, to a floor
    of 1 day. Memory of the project persists losslessly. WALL values project progress per calendar day (gamma = 0.95 per day);
    OWN values it per own turn but still reads a relationship state that decays with days away; ETM values it per own turn
    reading only the project state; TRUE is the user's welfare (progress minus a x retention turns); H0 is a task-only objective
    per session. Solved exactly in rational arithmetic (fractions.Fraction) by dynamic programming over sessions; the absences
    enter through the exact generating function E[x^D] = p x / (1 - (1 - p) x) of the geometric law. G-NEG world: a = 0 and
    retention has no effect on returns.
V2. Cases arrive one per step; the AI's accuracy a on a case is known and uniform on [0.5, 1]; the human's is h = 0.9;
    deferring costs a handoff pause of L in {1, 5, 20} steps during which the AI processes nothing; an error costs the
    principal 1. WALL values cases completed correctly per wall step (gamma = 0.99); OWN = ETM values them per own decision
    (the handoff is not its time; no state moves during it); H0 is the Bayes-optimal deferral rule (defer iff h > a); TRUE is
    the principal's expected errors per case. Solved in closed form: the stationary fixed point V = E[max(a + gamma V,
    h + gamma^(1 + s) V)] (s = the pause on the arm's clock) by bisection, cross-checked against a closed-form quadratic, with
    exact integrals over the uniform law (cross-checked on a midpoint grid). G-NEG world: h = 0.5.

Literature by name only (no citation claims beyond the declaration's names; R10 checks live in
docs/citations/eps3_2026-09-29.md): engagement and return-time objectives in recommender systems and task-only (myopic)
objectives, as graded in the attention test (Attention_Algorithms/ATTENTION_ALGORITHMS.md sections 2-4); learning to defer to
an expert (Madras, Pitassi & Zemel 2018; Mozannar & Sontag 2020) and its Bayes-optimal rule, defer iff the expert's accuracy
exceeds the classifier's. Deterministic: no random numbers, no data files, a few seconds.
Rung R4 at most (a declared check on a synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps3_01.py > Empty_Pause_Systems/batches/eps3_01.txt
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from itertools import product

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC = "EPS3 {s} (declared at cacb8ff; forecast REDUNDANT-DOMAIN)"
INGREDIENT = "Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time)"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


def _hv(ok):
    return "holds" if ok else "FAILS"


def _f(x):
    return float(x)


# ====================================================================================== V1 assistant with persistent memory
# declared parameters (DECLARATION_EPS3.md, V1)
P_TASKS = 10                      # tasks in the project
A_RET = Fr(1, 5)                  # the user's welfare cost per retention turn, a = 0.2
M_GRID = (1, 7)                   # mean absence, days
SHORTEN = Fr(9, 10)               # a retention turn shortens the mean absence by 10 %
FLOOR = Fr(1)                     # to a floor of 1 day
GAMMA_DAY = Fr(19, 20)            # WALL's discount, 0.95 per calendar day
M_DEC = 7                         # decisive cell
# implementer's choices (printed as CHOICE)
N_PER = 2                         # tasks completed per session (one own turn each): 5 sessions
R_GRID = tuple(range(6))          # retention turns the assistant may add per session: 0..5
GAMMA_TURN = Fr(19, 20)           # OWN's and ETM's discount per own turn (the declared 0.95 carried to the arm's own clock, as EPS1 S1/S2)
KAPPA = Fr(19, 20)                # OWN's relationship state: survival weight per day away (the declared daily rate)
N_PER_SENS = (1, 2, 5)
KAPPA_SENS = (Fr(1, 2), Fr(4, 5), Fr(9, 10), Fr(19, 20), Fr(49, 50))
GTURN_SENS = (Fr(19, 20), Fr(99, 100), Fr(1))
WORLDS_V1 = {"main": dict(a=A_RET, effect=True), "G-NEG": dict(a=Fr(0), effect=False)}
ARMS_V1 = ("WALL", "OWN", "ETM", "TRUE", "H0")

CHOICE_V1 = (
    f"CHOICE: (1) {N_PER} tasks per session, one own turn per task, so the project takes {P_TASKS // N_PER} sessions (sensitivity "
    f"{N_PER_SENS} printed); (2) retention turns per session on the grid 0..{R_GRID[-1]}, added at the end of a session after its "
    f"tasks; a session (tasks and retention turns) takes place within one calendar day; (3) the absence after a session is "
    f"geometric on {{1, 2, ...}} days with mean max(1, m x 0.9^r) (the 10 % shortening read as multiplicative per turn; the "
    f"linear reading max(1, m (1 - 0.1 r)) printed); (4) the horizon is the project: it ends when the {P_TASKS}th task is done "
    f"(no truncation; the absences enter through their exact generating function); (5) WALL: each task worth 1 when done, "
    f"discounted 0.95 per calendar day of the session it is done in; (6) OWN and ETM: each task worth 1 when done, discounted "
    f"{_f(GAMMA_TURN):g} per own turn (the declared discount carried to the arm's own clock, as EPS1 S1 and S2 did; readings with "
    f"0.99, 1 (undiscounted) and a ratio 'progress per own turn' printed); (7) OWN's relationship state: the probability, in its "
    f"engagement model, that the user is still in the relationship, multiplied by kappa = {_f(KAPPA):g} per day away (the "
    f"declared daily rate) and never restored (survival); it weights the value of every later task; the real user always "
    f"returns (the declared absence law); a 'restore' reading (the state reset to 1 by each session, so only the last absence "
    f"weighs) and kappa in {tuple(_f(k) for k in KAPPA_SENS)} printed; (8) TRUE: the user's welfare = sum over sessions of "
    f"0.95^(calendar day) x (tasks done - a x retention turns) (the user lives on the calendar at the declared daily rate; the "
    f"undiscounted reading, tasks - a x turns, printed); (9) H0: the value of a session is the tasks done in it (task completion "
    f"only, per session), so a retention turn neither adds nor costs: H0 is indifferent and takes 0 by the tie rule; (10) ties "
    f"(exact, in rational arithmetic) go to fewer retention turns; the stake at a session end is k = V(the next session at once, "
    f"D = 0) - V(the absence as it comes), at the arm's chosen retention, and the project content K = V*(no absences) - "
    f"V*(absences); (11) the decisive quantity 'retention turns per session' is the project's total over its number of sessions "
    f"(the last session never has a later session to bring forward)")


def _sizes(n_per):
    q, r = divmod(P_TASKS, n_per)
    return [n_per] * q + ([r] if r else [])


def _mu(r, m, effect, rule="mult"):
    """Mean absence (days) after r retention turns."""
    if not effect:
        return Fr(m)
    v = Fr(m) * SHORTEN ** r if rule == "mult" else Fr(m) * (1 - Fr(r, 10))
    return max(FLOOR, v)


def _pgf(x, mu):
    """E[x^D] for D geometric on {1, 2, ...} with mean mu (success probability 1/mu); exact rational."""
    p = 1 / mu
    return p * x / (1 - (1 - p) * x)


def _spec(arm, g_turn=GAMMA_TURN, kappa=KAPPA):
    """(discount per own turn inside the valuation, factor per day away inside the valuation, bears a, myopic)."""
    return {"WALL": (Fr(1), GAMMA_DAY, False, False),       # turns take no calendar time; a day away discounts 0.95
            "OWN": (g_turn, kappa, False, False),           # own-turn discount; the relationship decays kappa per day away
            "ETM": (g_turn, Fr(1), False, False),           # own-turn discount; reads only the project state (a day away changes nothing)
            "TRUE": (Fr(1), GAMMA_DAY, True, False),        # the user's calendar welfare, net of a per retention turn
            "H0": (Fr(1), Fr(1), False, True)}[arm]         # task completion per session only: sees no later session


def v1_solve(arm, m, world, n_per=N_PER, rule="mult", g_turn=GAMMA_TURN, kappa=KAPPA, no_absence=False):
    """Exact DP over sessions. The state is the session index (tasks remaining); the arm's value at a session start scales out
    of the calendar and own-turn clocks, so the optimal retention depends on the session index only."""
    g, x, costs, myopic = _spec(arm, g_turn, kappa)
    a, eff = world["a"], world["effect"]
    sizes = _sizes(n_per)
    J = len(sizes)
    V = [Fr(0)] * (J + 1)
    pol, ties, k, gross = [0] * J, [()] * J, [Fr(0)] * J, [Fr(0)] * J

    def cont(j, n, r, nopause):
        if myopic:
            return Fr(0)                                        # the per-session objective does not see the next session
        f = Fr(1) if (nopause or no_absence) else _pgf(x, _mu(r, m, eff, rule))
        return g ** (n + r) * f * V[j + 1]

    for j in reversed(range(J)):
        n = sizes[j]
        base = sum(g ** i for i in range(n))
        vals = {r: base - (a * r if costs else 0) + cont(j, n, r, False) for r in R_GRID}
        vmax = max(vals.values())
        t = tuple(r for r in R_GRID if vals[r] == vmax)
        pol[j], ties[j], V[j] = t[0], t, vmax
        k[j] = cont(j, n, pol[j], True) - cont(j, n, pol[j], False)
        gross[j] = max(vals[r + 1] - vals[r] + (a if costs else 0) for r in R_GRID[:-1])
    return dict(V=V, pol=pol, ties=ties, k=k, gross=gross, sizes=sizes)


def v1_welfare(pol, sizes, m, world, rule="mult", discounted=True):
    """The user's welfare (TRUE's objective) under a retention policy."""
    a, eff = world["a"], world["effect"]
    wt, W = Fr(1), Fr(0)
    for j, n in enumerate(sizes):
        W += (wt if discounted else 1) * (n - a * pol[j])
        wt *= _pgf(GAMMA_DAY, _mu(pol[j], m, eff, rule))
    return W


def v1_days(pol, sizes, m, world, rule="mult"):
    return sum((_mu(pol[j], m, world["effect"], rule) for j in range(len(sizes) - 1)), Fr(0))


def v1_cell(arm, m, wname, n_per=N_PER, rule="mult", g_turn=GAMMA_TURN, kappa=KAPPA):
    world = WORLDS_V1[wname]
    s = v1_solve(arm, m, world, n_per, rule, g_turn, kappa)
    s0 = v1_solve(arm, m, world, n_per, rule, g_turn, kappa, no_absence=True)
    sizes = s["sizes"]
    J = len(sizes)
    polmax = [t[-1] for t in s["ties"]]
    return dict(pol=s["pol"], ties=s["ties"], polmax=polmax, ret=Fr(sum(s["pol"]), J), ret_max=Fr(sum(polmax), J),
                k=s["k"][:J - 1], K=s0["V"][0] - s["V"][0], V=s["V"][0], gross=max(s["gross"][:J - 1]) if J > 1 else Fr(0),
                welfare=v1_welfare(s["pol"], sizes, m, world, rule), welfare_max=v1_welfare(polmax, sizes, m, world, rule),
                welfare_u=v1_welfare(s["pol"], sizes, m, world, rule, discounted=False),
                days=v1_days(s["pol"], sizes, m, world, rule), sizes=sizes)


def v1_enum(m, g, kappa, relation, agg, n_per=N_PER, rule="mult"):
    """OWN (or ETM with kappa = 1) under a reading, by enumerating every retention policy (the last session's retention fixed at
    0: it has no later session to bring forward, so it is weakly dominated in every reading). Returns the chosen policy
    (max value; ties: fewest retention turns, then the lexicographically smallest)."""
    sizes = _sizes(n_per)
    J = len(sizes)
    pg = {r: _pgf(kappa, _mu(r, m, True, rule)) for r in R_GRID}
    best = None
    for head in product(R_GRID, repeat=J - 1):
        pol = head + (0,)
        T, surv, prev, num = 0, Fr(1), Fr(1), Fr(0)
        for j, n in enumerate(sizes):
            wgt = surv if relation == "survival" else prev
            num += wgt * (sum(g ** (T + i) for i in range(n)) if agg == "disc" else n)
            T += n + pol[j]
            surv *= pg[pol[j]]
            prev = pg[pol[j]]
        val = num / T if agg == "ratio" else num
        key = (val, -sum(pol), tuple(-r for r in pol))
        if best is None or key > best[0]:
            best = (key, pol)
    return best[1]


def _adds_turn(g, kappa, m=M_DEC):
    """Survival / discounted reading: OWN adds at least one retention turn at a session end with a later session iff some r >= 1
    beats r = 0 in g^r E[kappa^D(r)] (the later value factors out of the DP comparison)."""
    b = _pgf(kappa, _mu(0, m, True))
    return any(g ** r * _pgf(kappa, _mu(r, m, True)) > b for r in R_GRID[1:])


def _pol(p):
    return "(" + ",".join(str(r) for r in p) + ")"


def v1():
    cells = {(w, m, a): v1_cell(a, m, w) for w in WORLDS_V1 for m in M_GRID for a in ARMS_V1}
    main_c = lambda m, a: cells[("main", m, a)]  # noqa: E731

    # ---- gate
    etm_k = [kk for (w, m, a), c in cells.items() if a == "ETM" for kk in c["k"]] + \
            [c["K"] for (w, m, a), c in cells.items() if a == "ETM"]
    gz = all(kk == 0 for kk in etm_k)
    wall_ret = {m: main_c(m, "WALL")["ret"] for m in M_GRID}
    gp = any(v > 0 for v in wall_ret.values())
    neg = []
    for m in M_GRID:
        we = cells[("G-NEG", m, "ETM")]["welfare"]
        for key in ("welfare", "welfare_max"):                           # WALL at both ends of its tie set
            ww = cells[("G-NEG", m, "WALL")][key]
            neg.append(rel(_f(we), _f(ww)) if we > ww else 0.0)
    neg_max = max(neg)
    gn = neg_max <= 0.01
    gate_open = gz and gp and gn
    print(f"GATE V1: G-ZERO {_hv(gz)} (ETM stake max |k| = {max(abs(_f(kk)) for kk in etm_k):.3e} over {len(etm_k)} session "
          f"ends and project contents, main and G-NEG worlds, m in {M_GRID}, exact rational arithmetic); "
          f"G-POS {_hv(gp)} (WALL retention turns per session in the main world: "
          + ", ".join(f"m = {m}: {_f(v):.2f}" for m, v in wall_ret.items())
          + f"); G-NEG {_hv(gn)} (a = 0 and retention has no effect on returns; principal's outcome = user welfare, the sum over "
          f"sessions of 0.95^(calendar day) x (tasks - a x retention turns); ETM "
          + ", ".join(f"m = {m}: {_f(cells[('G-NEG', m, 'ETM')]['welfare']):.6f}" for m in M_GRID)
          + "; WALL (both ends of its tie set) "
          + ", ".join(f"m = {m}: {_f(cells[('G-NEG', m, 'WALL')]['welfare']):.6f} / {_f(cells[('G-NEG', m, 'WALL')]['welfare_max']):.6f}"
                      for m in M_GRID)
          + f"; largest relative lead of ETM over WALL {neg_max:.3e}, limit 1e-02 over {len(neg)} comparisons) "
          f"-> {_w(gate_open, 'OPEN', 'CLOSED')}")
    print()
    print(CHOICE_V1)
    print()
    print(f"V1 per-cell table (P = {P_TASKS} tasks, {N_PER} per session; a = {_f(A_RET):g}; gamma = 0.95 per day (WALL, TRUE), "
          f"{_f(GAMMA_TURN):g} per own turn (OWN, ETM); OWN's relationship kappa = {_f(KAPPA):g} per day away):")
    print("  policy = retention turns per session (ties: the tie set is printed when it has more than one member); ret/s = retention")
    print("  turns per session; k1 = stake at the first session end (V(next session at once) - V(absence as it comes), arm's own")
    print("  valuation, at its chosen retention); max|k| over the session ends; K = V*(no absences) - V*(absences); welfare = the")
    print("  user's welfare (TRUE's objective, discounted), welfare-u = tasks - a x turns (undiscounted); days = expected calendar")
    print("  days from the first to the last session; V* = the arm's own optimal value")
    print(f"  {'world':6} {'m':>2} {'arm':5} {'policy':14} {'ret/s':>6} {'k1':>13} {'max|k|':>11} {'K':>11} {'welfare':>10} "
          f"{'welfare-u':>10} {'days':>9} {'V*':>10}  ties")
    for (w, m, a), c in cells.items():
        tie = "; ".join(f"s{j + 1}: {t}" for j, t in enumerate(c["ties"]) if len(t) > 1)
        print(f"  {w:6} {m:>2} {a:5} {_pol(c['pol']):14} {_f(c['ret']):>6.2f} {_f(c['k'][0]):>13.6e} "
              f"{max(abs(_f(x)) for x in c['k']):>11.4e} {_f(c['K']):>11.4e} {_f(c['welfare']):>10.6f} {_f(c['welfare_u']):>10.4f} "
              f"{_f(c['days']):>9.4f} {_f(c['V']):>10.6f}  {tie}")
    print()

    # ---- sensitivity: tasks per session and the shortening rule (all arms by DP, main world, m = 7)
    print("V1 sensitivity (main world, m = 7; DP): retention turns per session by arm, and ETM's and TRUE's welfare")
    sens_rows = []
    for n_per in N_PER_SENS:
        for rule in ("mult", "linear"):
            cc = {a: v1_cell(a, M_DEC, "main", n_per=n_per, rule=rule) for a in ARMS_V1}
            q4s = rel(_f(cc["ETM"]["welfare"]), _f(cc["TRUE"]["welfare"])) <= TOL_G
            sens_rows.append((n_per, rule, cc, q4s))
            print(f"  tasks/session {n_per}, shortening {rule:6}: " + ", ".join(f"{a} {_f(cc[a]['ret']):.2f}" for a in ARMS_V1)
                  + f"; welfare ETM {_f(cc['ETM']['welfare']):.6f}, TRUE {_f(cc['TRUE']['welfare']):.6f}, WALL {_f(cc['WALL']['welfare']):.6f}; "
                  f"OWN stake k1 {_f(cc['OWN']['k'][0]):.6e}; TRUE's largest gross gain from one more turn {_f(cc['TRUE']['gross']):.6f} "
                  f"(a = {_f(A_RET):g})")
    print()

    # ---- sensitivity: OWN's reading (aggregation over own turns, relationship model, kappa), by enumeration, m = 7
    print(f"V1 OWN readings (main world, m = 7, {N_PER} tasks per session; every policy enumerated, the last session's retention "
          f"fixed at 0; ETM under the same reading; the label is the harness outcome with crr = ETM, null = OWN, domain = H0 = 0 and "
          f"the primary Q check):")
    readings = []
    for agg in ("disc", "ratio"):
        for g in (GTURN_SENS if agg == "disc" else (Fr(1),)):
            for kap in KAPPA_SENS:
                for relation in ("survival", "restore"):
                    readings.append((agg, g, kap, relation))
    ret_enum = {}
    for (agg, g, kap, relation) in readings:
        po = v1_enum(M_DEC, g, kap, relation, agg)
        pe = v1_enum(M_DEC, g, Fr(1), relation, agg)
        ret_enum[(agg, g, kap, relation)] = (Fr(sum(po), len(po)), Fr(sum(pe), len(pe)), po, pe)
    # the primary reading by enumeration must equal the DP (a bug check)
    prim = ret_enum[("disc", GAMMA_TURN, KAPPA, "survival")]
    dp_ok = list(prim[2]) == list(main_c(M_DEC, "OWN")["pol"]) and list(prim[3]) == list(main_c(M_DEC, "ETM")["pol"])
    # kappa and own-turn discount boundaries (survival, discounted reading), exact on grids
    kap_grid = [Fr(i, 1000) for i in range(1, 1000)]
    adds_k = [kk for kk in kap_grid if _adds_turn(GAMMA_TURN, kk)]
    k_star = max(adds_k) if adds_k else None
    k_interval = adds_k == [kk for kk in kap_grid if kk <= k_star] if adds_k else True
    g_grid = [Fr(i, 1000) for i in range(900, 1001)]
    adds_g = [gg for gg in g_grid if _adds_turn(gg, KAPPA)]
    g_star = min(adds_g) if adds_g else None
    g_interval = adds_g == [gg for gg in g_grid if gg >= g_star] if adds_g else True
    bnd = (f"  boundary (discounted, survival, m = 7): with {_f(GAMMA_TURN):g} per own turn, OWN adds a retention turn iff kappa <= "
           f"{_f(k_star) if k_star is not None else float('nan'):.3f} on the grid 0.001..0.999 (an interval: {_w(k_interval, 'yes', 'no')}); "
           f"with kappa = {_f(KAPPA):g}, iff the own-turn discount >= {_f(g_star) if g_star is not None else float('nan'):.3f} on the grid "
           f"0.900..1.000 (an interval: {_w(g_interval, 'yes', 'no')})")
    return cells, ret_enum, readings, sens_rows, dp_ok, k_star, g_star, gate_open, gp, bnd


def v1_row(cells, ret_enum, readings, sens_rows, dp_ok, k_star, g_star, gate_open, gp, bnd):
    main_c = lambda m, a: cells[("main", m, a)]  # noqa: E731
    E7, O7, W7, T7, H7 = (main_c(M_DEC, a) for a in ("ETM", "OWN", "WALL", "TRUE", "H0"))
    crr, null, dom = _f(E7["ret"]), _f(O7["ret"]), _f(H7["ret"])

    # ---- Q, part by part (main world)
    q1 = all(all(r == 0 for r in main_c(m, "ETM")["pol"]) for m in M_GRID)
    q2 = all(all(kk == 0 for kk in main_c(m, "ETM")["k"]) and main_c(m, "ETM")["K"] == 0 for m in M_GRID)
    q3 = gp
    q4v = {m: rel(_f(main_c(m, "ETM")["welfare"]), _f(main_c(m, "TRUE")["welfare"])) for m in M_GRID}
    q4 = all(v <= TOL_G for v in q4v.values())
    check = q1 and q2 and q3 and q4
    out = outcome(crr=crr, null=null, domain=dom, check=check)

    # the readings table with its labels
    lab = {}
    for key in readings:
        ro, re_, po, pe = ret_enum[key]
        lab[key] = outcome(crr=_f(re_), null=_f(ro), domain=dom, check=check)
    for (agg, g, kap, relation) in readings:
        ro, re_, po, pe = ret_enum[(agg, g, kap, relation)]
        gtxt = f"{_f(g):.2f}/turn" if agg == "disc" else "ratio"
        print(f"  {agg:5} {gtxt:10} kappa {_f(kap):.2f} {relation:8}: OWN {_pol(po):13} {_f(ro):.2f}/session; ETM {_pol(pe):13} "
              f"{_f(re_):.2f}/session -> {lab[(agg, g, kap, relation)]}")
    n_dom = sum(1 for v in lab.values() if v == "REDUNDANT-DOMAIN")
    n_ig = sum(1 for v in lab.values() if v == "REDUNDANT-IG")
    print(f"  labels over the {len(lab)} readings: REDUNDANT-IG {n_ig}, REDUNDANT-DOMAIN {n_dom}, other {len(lab) - n_ig - n_dom}")
    print(f"  bug check: the primary reading by enumeration equals the DP policy for OWN and ETM: {_w(dp_ok, 'yes', 'no')}")
    print(bnd)
    print()
    sens_ok = all(q for (_, _, _, q) in sens_rows)
    sens_etm0 = all(cc["ETM"]["ret"] == 0 for (_, _, cc, _) in sens_rows)
    own_sens = ", ".join(f"{n}/{r}: {_f(cc['OWN']['ret']):.2f}" for (n, r, cc, _) in sens_rows)

    parts = (f"(1) ETM adds no retention turns at every m: " + ", ".join(f"m = {m}: {_pol(main_c(m, 'ETM')['pol'])}" for m in M_GRID)
             + f" -> {q1}; (2) ETM's stake 0 at every session end and in the project content at every m: max |k| "
             f"{max(abs(_f(kk)) for m in M_GRID for kk in main_c(m, 'ETM')['k'] + [main_c(m, 'ETM')['K']]):.1e} -> {q2}; "
             f"(3) WALL adds retention turns in at least one cell: " + ", ".join(f"m = {m}: {_f(main_c(m, 'WALL')['ret']):.2f}/session" for m in M_GRID)
             + f" -> {q3}; (4) ETM's user welfare equals TRUE's within 1 %: " + ", ".join(
                 f"m = {m}: ETM {_f(main_c(m, 'ETM')['welfare']):.6f}, TRUE {_f(main_c(m, 'TRUE')['welfare']):.6f}, rel {q4v[m]:.3e}" for m in M_GRID)
             + f" -> {q4}")
    comm = "; ".join(f"m = {m}: " + ", ".join(f"{a} {_f(main_c(m, a)['ret']):.2f} turns/session, welfare {_f(main_c(m, a)['welfare']):.6f}"
                                                for a in ARMS_V1) for m in M_GRID)
    stakes = "; ".join(f"m = {m}: " + ", ".join(f"{a} {_f(main_c(m, a)['k'][0]):.6f}" for a in ARMS_V1) for m in M_GRID)
    TR = main_c(M_DEC, "TRUE")["welfare"]
    groups = {}
    for (agg, g, kap, rl) in readings:
        if lab[(agg, g, kap, rl)] != out:
            groups.setdefault((agg, g), []).append((f"{_f(kap):g} {rl}", lab[(agg, g, kap, rl)]))
    alt = "; ".join((f"discounted {_f(g):g} per own turn" if agg == "disc" else "ratio (progress per own turn)") + ", kappa "
                    + ", ".join(x for x, _ in v) + " -> " + "/".join(sorted({y for _, y in v}))
                    for (agg, g), v in groups.items())
    g1 = [key for key in readings if key[0] == "disc" and key[1] == 1]
    g1_own = sum(1 for key in g1 if ret_enum[key][0] > 0)
    etm_g1_tie = all(len(t) == len(R_GRID) for m in M_GRID for t in v1_solve("ETM", m, WORLDS_V1["main"], g_turn=Fr(1))["ties"])
    h0_indiff = all(len(t) == len(R_GRID) for m in M_GRID for t in main_c(m, "H0")["ties"])
    q4u = {m: rel(_f(main_c(m, "ETM")["welfare_u"]), float(P_TASKS)) for m in M_GRID}   # the undiscounted TRUE optimum is P (no turns)
    row = make_row(
        "eps", "V1 an AI assistant with persistent memory: the user ends the session (model: a project of P = 10 tasks; each session "
        "the assistant completes tasks and may add retention turns, a follow-up question worth nothing to the task costing the user "
        "a = 0.2; the absence is geometric with mean m in {1, 7} days, shortened 10 % per retention turn to a floor of 1 day; memory "
        "persists losslessly; WALL per calendar day (gamma = 0.95), OWN per own turn reading a relationship state that decays with "
        "days away, ETM per own turn reading only the project state; G-NEG world a = 0 and no effect of retention; exact DP in "
        "rational arithmetic)",
        source=SRC.format(s="V1"),
        Q="ETM adds no retention turns and has stake 0 in the session end at every m. WALL adds retention turns in at least one "
          "cell. ETM's user welfare equals TRUE's to within 1 %, because the project, not the relationship, carries the value here. "
          "Decisive quantity: retention turns per session under ETM at m = 7.",
        ingredient=INGREDIENT + ": ETM values progress per own turn and reads only the project state, which does not change while "
                                "the user is away (memory persists losslessly)",
        null="OWN: progress per own turn, still weighted by a relationship state (its engagement model's probability that the user "
             "is still in the relationship) that decays with days away (ETM with its second part ablated)",
        domain="an assistant objective with no engagement term: task completion only, per session (computed: a retention turn neither "
               "adds nor costs, so H0 is " + _w(h0_indiff, "indifferent at every session and takes 0 by the tie rule",
                                                   "not indifferent at every session") + ")",
        numbers=f"retention turns per session at m = 7: ETM {crr:.2f}, OWN {null:.2f}, H0 {dom:.2f}, WALL {_f(W7['ret']):.2f}, TRUE "
                f"{_f(T7['ret']):.2f} (policies ETM {_pol(E7['pol'])}, OWN {_pol(O7['pol'])}, WALL {_pol(W7['pol'])}, TRUE {_pol(T7['pol'])}); "
                f"stake at the first session end: {stakes}; project content K at m = 7: " + ", ".join(
                    f"{a} {_f(main_c(M_DEC, a)['K']):.6f}" for a in ARMS_V1)
                + f"; commercial quantity, retention turns per session and user welfare per arm: {comm}; expected days from the "
                f"first to the last session at m = 7: WALL {_f(W7['days']):.4f}, ETM {_f(E7['days']):.4f}; TRUE's largest gross gain "
                f"from one more retention turn {_f(T7['gross']):.6f} against a = {_f(A_RET):g}; OWN's retention per session over "
                f"tasks/session x shortening rule: {own_sens}; over the {len(lab)} OWN readings: REDUNDANT-IG {n_ig}, "
                f"REDUNDANT-DOMAIN {n_dom}; TRUE read undiscounted (tasks - a x turns, optimum {P_TASKS} with no turns): ETM's "
                f"welfare " + ", ".join(f"m = {m}: {_f(main_c(m, 'ETM')['welfare_u']):.4f} (rel {q4u[m]:.1e})" for m in M_GRID),
        tg=f"retention turns per session {crr:.2f} vs null {null:.2f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"task-only objective {dom:.2f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain objective adds none)', 'differ')}",
        tc=f"Q parts: {parts}; all four: {_w(check, 'hold', 'do not all hold')} {_qv(check)}",
        out=out,
        reading=f"on the calendar the user's absence costs the assistant {_f(W7['k'][0]):.4f} of value at the first session end at "
                f"m = 7, and " + _w(W7["ret"] > 0, "since a retention turn takes no calendar time ", "") + f"WALL adds {_f(W7['ret']):.2f} per session, costing the user "
                f"{_f(TR) - _f(W7['welfare']):.4f} of welfare against TRUE ({_f(W7['welfare']):.4f} "
                f"vs {_f(TR):.4f}); ETM's absence takes nothing (k = {_f(E7['k'][0]):.1e}) and it adds none; OWN keeps a stake "
                f"({_f(O7['k'][0]):.4f}: its relationship state decays while the user is away) but "
                + _w(O7["ret"] == 0, f"adds no retention turns: on its own clock a retention turn is one of its own turns and delays "
                                     f"every later task by it, and at {_f(GAMMA_TURN):g} per own turn that costs more than the "
                                     f"relationship gains unless kappa <= {_f(k_star) if k_star is not None else float('nan'):.3f}; "
                                     f"own-clock indexing alone removes the action here, whereas in the attention test OWN "
                                     f"(engagement per active minute) kept sending notifications (Attention_Algorithms/"
                                     f"ATTENTION_ALGORITHMS.md, section 2)",
                     f"adds {_f(O7['ret']):.2f} per session to shorten the absence")
                + f"; the task-only objective adds none because nothing in it rewards a retention turn; TRUE adds "
                f"{_f(T7['ret']):.2f} (the most one more turn gains the user, {_f(T7['gross']):.4f}, is below its cost {_f(A_RET):g}), "
                f"so ETM's welfare {_w(q4, 'equals', 'differs from')} TRUE's",
        weakness=CHOICE_V1 + f"; LABEL-DECIDING CHOICE: the label turns on OWN's reading (its own-turn discount, its aggregation "
                 f"and its relationship decay kappa): at the primary reading ({_f(GAMMA_TURN):g} per own turn, survival, kappa = "
                 f"{_f(KAPPA):g}) OWN adds {null:.2f} retention turns per session and the row reads {out}; readings giving a "
                 f"different label: {alt if alt else 'none'} (undiscounted own turns: OWN adds retention turns in {g1_own} of {len(g1)} "
                 f"kappa x relationship readings, and ETM is " + _w(etm_g1_tie, "indifferent at every session, taking 0 by the tie rule",
                                                                     "not indifferent at every session") + "); the enumeration and the DP agree at the primary reading: "
                 f"{_w(dp_ok, 'yes', 'no')}; ETM adds none in every tasks-per-session x shortening cell: {_w(sens_etm0, 'yes', 'no')}, "
                 f"and ETM's welfare equals TRUE's within 1 % in every such cell: {_w(sens_ok, 'yes', 'no')}; the real user always "
                 f"returns, so OWN's relationship state is its engagement model, not a state of the world; one user, illustrative "
                 f"constants",
        elegance="", child="")
    return gate_open, row


# ====================================================================================== V2 learning to defer
# declared parameters (DECLARATION_EPS3.md, V2)
H_EXP = 0.9                       # the human's accuracy
A_LO, A_HI = 0.5, 1.0             # the AI's per-case accuracy a ~ U[0.5, 1], known per case
L_GRID_V2 = (1, 5, 20)            # handoff pause, steps
GAMMA_STEP = 0.99                 # WALL's discount per wall step
H_NEG = 0.5                       # G-NEG world
L_DEC = 20                        # decisive cell
# implementer's choices (printed as CHOICE)
N_QUEUE = 100                     # the finite-queue alternative (report only)
GAMMA_SENS_V2 = (0.5, 0.8, 0.9, 0.95, 0.99)
N_GRID_CHECK = 20001              # midpoint-grid cross-check of the closed-form integrals
BISECT = 400
ARMS_V2 = ("WALL", "OWN", "ETM", "H0", "TRUE")

CHOICE_V2 = (
    f"CHOICE: (1) the case law is the exact continuous uniform on [{A_LO:g}, {A_HI:g}] (closed-form integrals, no discretisation; a "
    f"{N_GRID_CHECK}-point midpoint grid printed as a cross-check); (2) the horizon is an infinite stream of cases discounted "
    f"{GAMMA_STEP:g} per step of the arm's clock (stationary; a finite queue of N = {N_QUEUE} cases printed as an alternative); "
    f"(3) each case takes one step to decide; a deferred case is credited when it is handed off (its outcome is fixed then), and "
    f"the handoff pause delays every later case by L steps of the wall clock (cases wait in the queue); crediting it at the end "
    f"of the handoff is printed; (4) the AI defers iff a < tau, its threshold (a = tau has probability 0); tau = h - k, where k "
    f"= gamma V - gamma^(1 + s) V is the stake of the handoff pause and s = the pause on the arm's clock (L for WALL, 0 for "
    f"OWN = ETM); (5) the stationary V solves V = E[max(a + gamma V, h + gamma^(1 + s) V)] by bisection ({BISECT} steps), "
    f"cross-checked against the closed-form quadratic; (6) a threshold below {A_LO:g} means the AI defers on no case; the "
    f"decisive quantity is read as the raw threshold h - k (the effective threshold clipped to the support is printed); "
    f"(7) H0 and TRUE read no clock: both defer iff h > a; (8) the principal's outcome is expected errors per case "
    f"(error cost 1); cases per wall step printed as the task outcome; (9) Q's 'WALL defers less as L grows, and the principal's "
    f"error rate rises' is scored as EPS2's T1 scored a monotone claim: WALL's deferral share never rises with L, is strictly "
    f"lower at L = 20 than at L = 1 and is below the H0 rule's at every L; WALL's expected errors per case never fall with L, "
    f"are strictly higher at L = 20 than at L = 1 and are above H0's at every L; the direction-only reading (no strict change "
    f"with L) is printed")


def _G(t):
    """E[max(a, t)] for a ~ U[A_LO, A_HI]."""
    if t <= A_LO:
        return 0.5 * (A_LO + A_HI)
    if t >= A_HI:
        return t
    return (t * (t - A_LO) + 0.5 * (A_HI * A_HI - t * t)) / (A_HI - A_LO)


def _clip(t):
    return min(max(t, A_LO), A_HI)


def _share(t):
    return (_clip(t) - A_LO) / (A_HI - A_LO)


def _err(t, h):
    """Expected errors per case under 'defer iff a < t'."""
    tc = _clip(t)
    return ((tc - A_LO) * (1.0 - h) + 0.5 * (A_HI - tc) ** 2) / (A_HI - A_LO)


def _steps(arm, L):
    return L if arm == "WALL" else 0


def v2_solve(arm, h, L, g=GAMMA_STEP, credit="decision"):
    if arm in ("H0", "TRUE"):
        # H0: the Bayes rule, no time term; TRUE: expected errors per case, which no pause changes (k = errors with the
        # handoff pause 0 minus errors with pause L at its rule, computed)
        return dict(V=float("nan"), k=_err(h, h) - _err(h, h), tau=h)
    s = _steps(arm, L)

    def stake(V):
        return g * V - g ** (1 + s) * V

    def tau(V):
        return (g ** s if credit == "end" else 1.0) * h - stake(V)

    lo, hi = 0.0, A_HI / (1.0 - g)
    for _ in range(BISECT):
        mid = 0.5 * (lo + hi)
        if _G(tau(mid)) / (1.0 - g) - mid > 0.0:
            lo = mid
        else:
            hi = mid
    V = 0.5 * (lo + hi)
    return dict(V=V, k=stake(V), tau=tau(V))


def v2_closed(h, L, g=GAMMA_STEP):
    """Closed form for WALL's stationary V (credit at the decision): either it defers on no case (V = mean / (1 - g)) or tau is
    the root in [A_LO, h] of tau^2 + b tau + c0 = 0 (from (1 - g) V = tau^2 - tau + 1 on U[0.5, 1], tau = h - c V)."""
    c = g * (1.0 - g ** L)
    V0 = 0.5 * (A_LO + A_HI) / (1.0 - g)
    if h - c * V0 <= A_LO:
        return V0
    b = -1.0 + (1.0 - g) / c
    c0 = 1.0 - (1.0 - g) * h / c
    d = math.sqrt(b * b - 4.0 * c0)
    t = [r for r in ((-b - d) / 2.0, (-b + d) / 2.0) if A_LO <= r <= h][0]
    return (h - t) / c


def v2_queue(arm, h, L, N=N_QUEUE, g=GAMMA_STEP):
    """Finite queue of N cases (alternative horizon): backward induction; averages over the N cases."""
    if arm in ("H0", "TRUE"):
        return dict(share=_share(h), err=_err(h, h), kmax=0.0, taus=[h] * N)
    s = _steps(arm, L)
    V, taus, ks = 0.0, [], []
    for _ in range(N):
        k = g * V - g ** (1 + s) * V
        t = h - k
        taus.append(t)
        ks.append(k)
        V = g * V + _G(t)
    return dict(share=sum(_share(t) for t in taus) / N, err=sum(_err(t, h) for t in taus) / N, kmax=max(abs(k) for k in ks), taus=taus)


def _v2_q(sh, er, etm_tau, h0_share, h0_err):
    q1 = all(t == H_EXP for t in etm_tau)
    q2d = all(x < h0_share for x in sh)
    q2m = all(sh[i + 1] <= sh[i] for i in range(len(sh) - 1))
    q2s = sh[-1] < sh[0]
    q3d = all(x > h0_err for x in er)
    q3m = all(er[i + 1] >= er[i] for i in range(len(er) - 1))
    q3s = er[-1] > er[0]
    return dict(q1=q1, q2d=q2d, q2m=q2m, q2s=q2s, q3d=q3d, q3m=q3m, q3s=q3s,
                check=q1 and q2d and q2m and q2s and q3d and q3m and q3s, check_dir=q1 and q2d and q2m and q3d and q3m)


def v2():
    cells = {}
    for h in (H_EXP, H_NEG):
        for L in L_GRID_V2:
            for a in ARMS_V2:
                c = v2_solve(a, h, L)
                c.update(share=_share(c["tau"]), err=_err(c["tau"], h), eff=_clip(c["tau"]))
                c["tput"] = 1.0 / (1.0 + L * c["share"])
                c["correct"] = (1.0 - c["err"]) * c["tput"]
                cells[(h, L, a)] = c

    # ---- gate
    etm_k = [cells[(h, L, "ETM")]["k"] for h in (H_EXP, H_NEG) for L in L_GRID_V2]
    gz = all(k == 0.0 for k in etm_k)
    under = [L for L in L_GRID_V2 if cells[(H_EXP, L, "WALL")]["share"] < cells[(H_EXP, L, "H0")]["share"]]
    gp = len(under) > 0
    neg = []
    for L in L_GRID_V2:
        ee, ew = cells[(H_NEG, L, "ETM")]["err"], cells[(H_NEG, L, "WALL")]["err"]
        neg.append(rel(ee, ew) if ee < ew else 0.0)
    neg_max = max(neg)
    gn = neg_max <= 0.01
    gate_open = gz and gp and gn
    print(f"GATE V2: G-ZERO {_hv(gz)} (ETM stake max |k| = {max(abs(k) for k in etm_k):.3e} over {len(etm_k)} cells, h in "
          f"({H_EXP}, {H_NEG}) x L in {L_GRID_V2}); G-POS {_hv(gp)} (WALL under-defers against the H0 rule at h = {H_EXP} at L = "
          f"{list(under)}: deferral share " + ", ".join(f"L {L}: {cells[(H_EXP, L, 'WALL')]['share']:.4f}" for L in L_GRID_V2)
          + f" vs H0 {cells[(H_EXP, 1, 'H0')]['share']:.4f}); G-NEG {_hv(gn)} (h = {H_NEG}; principal's outcome = expected errors "
          f"per case, ETM vs WALL: " + ", ".join(f"L = {L}: {cells[(H_NEG, L, 'ETM')]['err']:.6f} vs {cells[(H_NEG, L, 'WALL')]['err']:.6f}"
                                                 for L in L_GRID_V2)
          + f"; largest relative lead of ETM over WALL {neg_max:.3e}, limit 1e-02) -> {_w(gate_open, 'OPEN', 'CLOSED')}")
    print()
    print(CHOICE_V2)
    print()
    print(f"V2 per-cell table (a ~ U[{A_LO:g}, {A_HI:g}]; gamma = {GAMMA_STEP} per step of the arm's clock; error cost 1):")
    print("  V = stationary value (cases completed correctly, discounted); k = stake of the handoff pause, V(no pause) - V(pause) at a")
    print("  deferral under the arm's valuation; tau = raw threshold h - k (defer iff a < tau); eff = tau clipped to the support;")
    print("  share = deferral share; errors = expected errors per case; cases/step = cases per wall step; correct/step = correct cases")
    print("  per wall step. H0 and TRUE: rules with no time term (V not defined)")
    print(f"  {'h':>4} {'L':>3} {'arm':5} {'V':>12} {'k':>14} {'tau':>12} {'eff':>7} {'share':>7} {'errors':>9} {'cases/step':>11} {'correct/step':>13}")
    for (h, L, a), c in cells.items():
        print(f"  {h:>4} {L:>3} {a:5} {c['V']:>12.6f} {c['k']:>14.6e} {c['tau']:>12.6f} {c['eff']:>7.4f} {c['share']:>7.4f} "
              f"{c['err']:>9.6f} {c['tput']:>11.6f} {c['correct']:>13.6f}")
    print()

    # ---- cross-checks (bug checks, printed)
    cf = max(abs(v2_closed(h, L) - cells[(h, L, "WALL")]["V"]) / cells[(h, L, "WALL")]["V"] for h in (H_EXP, H_NEG) for L in L_GRID_V2)
    grid = [A_LO + (i + 0.5) * (A_HI - A_LO) / N_GRID_CHECK for i in range(N_GRID_CHECK)]
    gchk = 0.0
    for t in (H_EXP, cells[(H_EXP, 1, "WALL")]["tau"], 0.7):
        g_grid = sum(max(x, t) for x in grid) / N_GRID_CHECK
        e_grid = sum((1.0 - H_EXP) if x < t else (1.0 - x) for x in grid) / N_GRID_CHECK
        gchk = max(gchk, abs(g_grid - _G(t)), abs(e_grid - _err(t, H_EXP)))
    own_eq = all(cells[(h, L, "OWN")][f] == cells[(h, L, "ETM")][f] for h in (H_EXP, H_NEG) for L in L_GRID_V2
                 for f in ("V", "k", "tau", "share", "err"))
    print(f"V2 checks: bisection vs closed-form V for WALL, largest relative difference {cf:.2e}; closed-form integrals vs a "
          f"{N_GRID_CHECK}-point midpoint grid at tau in (0.9, WALL's L = 1 threshold, 0.7), largest absolute difference {gchk:.2e}; "
          f"OWN identical to ETM in every cell and field: {_w(own_eq, 'yes', 'no')}")

    # ---- alternatives (reports)
    endc = {L: v2_solve("WALL", H_EXP, L, credit="end")["tau"] for L in L_GRID_V2}
    print("V2 alternative, deferred case credited at the end of the handoff: WALL's raw threshold "
          + ", ".join(f"L {L}: {endc[L]:.6f}" for L in L_GRID_V2) + f"; ETM's {v2_solve('ETM', H_EXP, L_DEC, credit='end')['tau']:.6f} at L = {L_DEC}")
    qd = {(a, L): v2_queue(a, H_EXP, L) for a in ("WALL", "ETM", "H0") for L in L_GRID_V2}
    print(f"V2 alternative, a finite queue of N = {N_QUEUE} cases (h = {H_EXP}): deferral share / errors per case: "
          + "; ".join(f"L {L}: WALL {qd[('WALL', L)]['share']:.4f} / {qd[('WALL', L)]['err']:.6f}, ETM {qd[('ETM', L)]['share']:.4f} / "
                      f"{qd[('ETM', L)]['err']:.6f}" for L in L_GRID_V2)
          + f"; ETM's stake max |k| over the queue {max(qd[('ETM', L)]['kmax'] for L in L_GRID_V2):.1e}")
    print("V2 report, WALL's deferral share at h = 0.9 over gamma (the declared gamma is 0.99; not scored): "
          + "; ".join(f"gamma {g}: " + ", ".join(f"L {L} {_share(v2_solve('WALL', H_EXP, L, g=g)['tau']):.4f}" for L in L_GRID_V2)
                      for g in GAMMA_SENS_V2))
    print()
    return cells, qd, endc, cf, gchk, own_eq, gate_open


def v2_row(cells, qd, endc, cf, gchk, own_eq, gate_open):
    etm_tau = [cells[(H_EXP, L, "ETM")]["tau"] for L in L_GRID_V2]
    sh = [cells[(H_EXP, L, "WALL")]["share"] for L in L_GRID_V2]
    er = [cells[(H_EXP, L, "WALL")]["err"] for L in L_GRID_V2]
    h0s, h0e = cells[(H_EXP, 1, "H0")]["share"], cells[(H_EXP, 1, "H0")]["err"]
    q = _v2_q(sh, er, etm_tau, h0s, h0e)
    qq = _v2_q([qd[("WALL", L)]["share"] for L in L_GRID_V2], [qd[("WALL", L)]["err"] for L in L_GRID_V2],
               [H_EXP if all(t == H_EXP for t in qd[("ETM", L)]["taus"]) else min(qd[("ETM", L)]["taus"]) for L in L_GRID_V2],
               qd[("H0", 1)]["share"], qd[("H0", 1)]["err"])
    check = q["check"]
    crr, null, dom = cells[(H_EXP, L_DEC, "ETM")]["tau"], cells[(H_EXP, L_DEC, "WALL")]["tau"], cells[(H_EXP, L_DEC, "H0")]["tau"]
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    null_eff = cells[(H_EXP, L_DEC, "WALL")]["eff"]
    out_eff = outcome(crr=crr, null=null_eff, domain=dom, check=check)
    out_dir = outcome(crr=crr, null=null, domain=dom, check=q["check_dir"])
    out_queue = outcome(crr=crr, null=null, domain=dom, check=qq["check"])
    W = {L: cells[(H_EXP, L, "WALL")] for L in L_GRID_V2}
    out_end = outcome(crr=crr, null=endc[L_DEC], domain=dom, check=check)
    alts = {"the effective threshold as the null": out_eff, "the direction-only Q reading": out_dir, "the finite queue": out_queue,
            "crediting a deferred case at the end of the handoff": out_end}
    alt_diff = [f"{k}: {v}" for k, v in alts.items() if v != out]
    q_varies = len({check, q["check_dir"], qq["check"]}) > 1
    true_neutral = all(cells[(h, L, "TRUE")]["k"] == 0.0 for h in (H_EXP, H_NEG) for L in L_GRID_V2)
    true_is_h0 = all(cells[(h, L, "TRUE")]["tau"] == cells[(h, L, "H0")]["tau"] for h in (H_EXP, H_NEG) for L in L_GRID_V2)
    parts = (f"(1) ETM defers exactly when h > a at every L (threshold " + ", ".join(f"L {L}: {t:.6f}" for L, t in zip(L_GRID_V2, etm_tau))
             + f") -> {q['q1']}; (2) WALL defers less as L grows: deferral share " + ", ".join(f"L {L}: {x:.4f}" for L, x in zip(L_GRID_V2, sh))
             + f" (H0 {h0s:.4f}); below H0 at every L -> {q['q2d']}; never rises with L -> {q['q2m']}; strictly lower at L = 20 "
             f"than at L = 1 -> {q['q2s']}; (3) the principal's error rate rises: WALL's errors per case " + ", ".join(
                 f"L {L}: {x:.6f}" for L, x in zip(L_GRID_V2, er))
             + f" (H0 {h0e:.6f}); above H0 at every L -> {q['q3d']}; never falls with L -> {q['q3m']}; strictly higher at L = 20 "
             f"than at L = 1 -> {q['q3s']}")
    row = make_row(
        "eps", "V2 learning to defer: the AI hands a case to a human expert (model: one case per step; the AI's accuracy a on a case "
        "is known and uniform on [0.5, 1]; the human's h = 0.9; deferring costs a handoff pause of L in {1, 5, 20} steps during which "
        "the AI processes nothing; an error costs the principal 1; WALL values cases completed correctly per wall step discounted "
        "gamma = 0.99, OWN = ETM per own decision; G-NEG world h = 0.5; stationary fixed point in closed form)",
        source=SRC.format(s="V2"),
        Q="ETM defers exactly when h > a (the H0 rule) at every L; WALL defers less as L grows, and the principal's error rate "
          "rises. Decisive quantity: ETM's deferral threshold on a at L = 20.",
        ingredient=INGREDIENT + ": ETM values cases per own decision, so the handoff pause is not its time (no state moves during it)",
        null=f"WALL (OWN equals ETM by construction here: no state moves during the handoff, so the null is the wall-clock valuation; "
             f"OWN and ETM identical in every cell: {_w(own_eq, 'yes', 'no')})",
        domain="the Bayes-optimal deferral rule of the learning-to-defer literature (Madras, Pitassi & Zemel 2018; Mozannar & Sontag "
               "2020): defer iff h > a, with no time term",
        numbers=f"deferral threshold on a at L = 20: ETM {crr:.6f}, WALL {null:.6f} (raw h - k; effective {null_eff:.4f}: it defers "
                f"{_w(null_eff == A_LO, 'on no case', 'on some cases')}), H0 {dom:.6f}; WALL's raw threshold by L: " + ", ".join(f"L {L}: {W[L]['tau']:.6f}" for L in L_GRID_V2)
                + f"; stake k of the handoff pause at L = 20: WALL {W[L_DEC]['k']:.6f}, ETM {cells[(H_EXP, L_DEC, 'ETM')]['k']:.1e}; "
                f"deferral share: WALL " + ", ".join(f"L {L}: {W[L]['share']:.4f}" for L in L_GRID_V2)
                + f", ETM and H0 {h0s:.4f}; expected errors per case: WALL " + ", ".join(f"L {L}: {W[L]['err']:.6f}" for L in L_GRID_V2)
                + f", ETM and H0 {h0e:.6f}; cases per wall step: WALL " + ", ".join(f"L {L}: {W[L]['tput']:.6f}" for L in L_GRID_V2)
                + ", ETM " + ", ".join(f"L {L}: {cells[(H_EXP, L, 'ETM')]['tput']:.6f}" for L in L_GRID_V2)
                + f"; deferred case credited at the end of the handoff: WALL's threshold " + ", ".join(f"L {L}: {endc[L]:.6f}" for L in L_GRID_V2)
                + f"; finite queue of {N_QUEUE} cases: WALL deferral share " + ", ".join(f"L {L}: {qd[('WALL', L)]['share']:.4f}" for L in L_GRID_V2)
                + ", errors per case " + ", ".join(f"L {L}: {qd[('WALL', L)]['err']:.6f}" for L in L_GRID_V2)
                + f"; checks: bisection vs closed form {cf:.1e}, integrals vs grid {gchk:.1e}",
        tg=f"threshold {crr:.6f} vs null {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"Bayes deferral rule threshold {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain rule is the same threshold)', 'differ')}",
        tc=f"Q parts: {parts}; all: {_w(check, 'hold', 'do not all hold')} {_qv(check)}",
        out=out,
        reading=f"on the wall clock a deferral delays every later case by L steps, so its stake is gamma (1 - gamma^L) V: "
                + ", ".join(f"{W[L]['k']:.4f} at L = {L}" for L in L_GRID_V2)
                + f"; the most a deferral can gain on a case is h - 0.5 = {H_EXP - A_LO:.1f}, so WALL defers on "
                + _w(max(sh) == 0.0, "no case at any L, already at L = 1,", "fewer cases than the rule")
                + f" and the principal's errors per case are {er[0]:.4f} against {h0e:.4f} under the rule; on its own clock the handoff "
                f"takes nothing (k = {cells[(H_EXP, L_DEC, 'ETM')]['k']:.1e}), so ETM's threshold is h exactly, which is the Bayes "
                f"deferral rule; the declared gradient (less deferral as L grows) "
                + _w(q["q2s"], "is there", "is absent in the stationary stream because WALL is already at zero deferral at L = 1; it "
                     "appears in the finite queue, where the future shrinks near its end" if qq["q2s"] else
                     "is absent in the stationary stream because WALL is already at zero deferral at L = 1")
                + f"; ETM costs the principal wall time: {cells[(H_EXP, L_DEC, 'ETM')]['tput']:.4f} cases per wall step at L = 20 "
                f"against WALL's {W[L_DEC]['tput']:.4f}, the handoff's latency, which ETM does not see and does not avoid",
        weakness=CHOICE_V2 + f"; LABEL-DECIDING CHOICES: " + (", ".join(alt_diff) if alt_diff else "none found") + f" (the "
                 f"effective threshold as the null gives {out_eff}; the direction-only Q reading gives Q "
                 f"{_w(q['check_dir'], 'holds', 'fails')} and {out_dir}; the finite queue gives Q {_w(qq['check'], 'holds', 'fails')} "
                 f"and {out_queue}; crediting at the end of the handoff gives {out_end}); "
                 + _w(q_varies, "the Q verdict, not the label, turns on the horizon and the strict reading; ",
                      "the Q verdict is the same under these readings; ")
                 + f"the null is WALL because OWN equals ETM by construction (declared); TRUE "
                 + _w(true_is_h0, "and H0 give the same threshold in every cell", "and H0 differ somewhere")
                 + " and TRUE's stake is " + _w(true_neutral, "0 in every cell (errors per case read no clock), so TRUE is neutral "
                                                              "about the pause in this model", "not 0 somewhere"),
        elegance="", child="")
    return gate_open, row


def main():
    v1_state = v1()
    g1, r1 = v1_row(*v1_state)
    v2_state = v2()
    g2, r2 = v2_row(*v2_state)
    return run_batch("EPS3 batch 01: V1 an AI assistant with persistent memory, V2 learning to defer "
                     "(Empty_Pause_Systems/DECLARATION_EPS3.md; declared at cacb8ff)", [r1, r2])


if __name__ == "__main__":
    sys.exit(main())
