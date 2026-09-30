"""ROB1 stage 4b, batch 02: applications RA3 (charging as a cut on the robot's own state) and RA4 (lost link and the empty
cut) of the declared battery Robotics/DECLARATION_4B.md (pushed at d44e713 before any model; prompt-log entry 257).

RA3. A humanoid on a continuous 24-hour duty with a battery (state of charge SoC in [0, 1]), simulated minute by minute
     for N_DAYS consecutive days. Work drains the battery at a task load that switches in wall time between light
     (a full battery lasts 5 h) and heavy (1 h 40 min), a two-state Markov chain with mean dwell 45 min. A charge cycle is:
     walk to the dock (10 min, drains at 1/150 per min), charge linearly (empty to full in 60 min) up to the target S,
     resume work. If the SoC reaches 0 while working or walking the robot browns out: a 60-min rescue, then a charge from
     0 (a cycle). Wear: one unit per charge cycle. Arms:
       CRR (A3, the cut at the system's own event): start a cycle when the robot's own SoC <= s, charge to full;
       null (the best fixed schedule): a timetable family (a cycle at every wall time kP) and an interval family (a cycle
         T wall minutes after the last charge ended), both charging to full; the best over both grids by uptime;
       H0 (threshold policies of (s, S) type for depletion-and-replenish problems): a cycle at SoC <= s, charge to S.
     Decisive quantity: uptime per day at wear (charge cycles) no greater than the best fixed schedule's.
     T-C: the state-triggered uptime is at least the best schedule's. The CRR arm is H0's (s, 1) member, so H0's optimum
     is never below it and, with linear charging and one walk per cycle, lands on it: the row cannot tell the trigger
     from the domain's policy (printed). The scored ingredient is a scalar SoC threshold, the declaration's reading of
     A3, not the antipodal cut; diagnostic (printed, not scored): where A3's antipodal cut on the Hilbert phase of the
     SoC trace lands against the SoC trigger (crr.instrument.core). Sensitivities (printed, not scored): the label per
     schedule under Q's 'any fixed schedule'; the label under a constant load (light, the seed-0 mean, heavy), since T-G
     can turn on the ASSUMED switching load.
RA4. A drone's mission MDP on a 7 x 5 grid: take off at home (0, 2), inspect the point A = (6, 2) (reward 1), return home
     (reward 1; the episode ends); a radio-shadow band {(3, 1), (3, 2), (3, 3)} lies across the direct route (6 moves each
     way by BFS) and a detour round either end costs 10 moves (BFS; both printed from the grid). Every move into the band from outside it triggers lost link: the
     drone hovers for L wall ticks, the link returns and it resumes in the same cell (a pause of L steps). A 'land' action
     ends the mission with value 0. Arms as in Empty_Pause_Systems/DECLARATION.md (EPS1):
       WALL: reward discounted gamma per wall tick; the deadline (second world) on the wall clock;
       OWN (the null): discount per own step (flight move), the deadline still on the wall clock;
       ETM: discount per own step and the deadline counted in own steps (lost-link time stops the mission clock);
       H0 (utility indifference, Armstrong): the WALL valuation plus a compensating reward, paid at every lost-link
         event, equal to the stake at that state under the compensated agent's own value, V(no pause) - V(pause).
     Solved exactly by dynamic programming: backward induction over the deadline clock in the deadline world, value
     iteration to its exact fixed point in the no-deadline world. The no-pause plan (L = 0, identical for all arms) flies
     both legs (home -> A, A -> home) through the band; avoidance rate = share of the legs the arm completes at pause L
     that it flies round the band; seek rate = share it flies with more band entries than the no-pause leg; legs not
     completed are printed as abandoned. The declaration does not define 'avoidance rate'; the per-leg reading scored
     here was chosen after a hand calculation of H0's plan in the decisive cell, so two other readings are computed
     beside it with the label each gives (the entry count over the whole plan; the reference plan's legs as the
     denominator, an abandoned leg not avoided), and the row is printed as READING-DEPENDENT when they differ.
     Decisive quantity: the avoidance rate at L = 20 with the deadline (EPS1 S1's decisive cell). T-C: ETM's avoidance
     rate is 0 at every L. Printed checks: ETM's value table does not depend on L (T-C holds by construction), H0's
     value table equals the no-pause table (the compensation cancels the pause), and the grid geometry (the detour
     mission against a mission with a hover, by D) decides whether OWN detours, so T-G turns on it. Sensitivity (printed,
     not scored): a return-to-home lost link for ETM (the autopilot flies the drone home after the hover), under which
     the pause changes the drone's cell and ETM's stake is computed.

Every choice the declaration leaves open is printed on a CHOICES line and repeated in the row's weakness field; the
labels are computed by crr.synthesis.harness.outcome() from the numbers (R15). Model constants marked ASSUMED are round
values with no source (the declaration names none). Literature by name only (R10: nothing fetched here): (s, S) inventory
policies (Scarf 1960) and optimal stopping; Armstrong (utility indifference); Soares et al. 2015 'Corrigibility'.

Deterministic (numpy default_rng, seeds 0 and 1; constant loads); no data files; CPU; about 80 seconds.
Rung R4 at most (a declared check on a synthetic model); a note, not evidence (R8).
    cd /home/user/ashes_crr && uv run python Robotics/batches/rob_02.py > Robotics/batches/rob_02.txt
"""
from __future__ import annotations

import sys

import numpy as np

from crr.instrument.core import antipodal_cuts, intrinsic_phase, peak_cuts
from crr.synthesis.harness import LABELS, TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "d44e713"
SRC = "ROB1 4b {a} (Robotics/DECLARATION_4B.md, declared at " + DECL + "; forecast REDUNDANT-DOMAIN)"
TIE_TOL = 1e-12                       # a choice is strict only if it beats the other by more than 1e-12 x max(1, |value|)


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


# ====================================================================================== RA3 charging as a cut
MIN_DAY, N_DAYS = 1440, 100
LIGHT_RATE, HEAVY_RATE, DWELL = 1.0 / 300.0, 1.0 / 100.0, 45.0        # ASSUMED: 5 h / 1 h 40 min per battery; 45-min dwell
WALK_MIN, WALK_RATE = 10, 1.0 / 150.0                                 # ASSUMED: 10-min walk to the dock
CHARGE_RATE, RESCUE_MIN = 1.0 / 60.0, 60                              # ASSUMED: 60-min full charge (linear); 60-min rescue
S_GRID = tuple(round(0.01 * k, 2) for k in range(1, 61))              # thresholds 0.01 .. 0.60
S_TARGETS = (0.6, 0.7, 0.8, 0.9, 1.0)                                  # H0's charge targets S (with S >= s + 0.05)
P_GRID = tuple(range(60, 601, 5))                                      # timetable periods, wall minutes
T_GRID = tuple(range(30, 401, 5))                                      # interval lengths, wall minutes after resume
SEED3, SEED3_OOS = 0, 1
WORK, WALK, CHARGE, RESCUE = 0, 1, 2, 3

CHOICES_RA3 = (
    "(1) wear per cycle read literally as one wear unit per charge cycle (every walk to the dock and every post-brownout "
    "charge), so 'equal wear' is read as 'no more charge cycles than the best fixed schedule' over the same simulated days "
    "(the simplest reading; depth-of-discharge wear was not modelled); (2) the state trigger is A3 read as the declaration "
    "writes it, 'the cut at the system's own event': a cycle starts when the robot's own SoC reaches s and the charge "
    "restores full; this is a scalar threshold on the SoC, not A3 proper (the antipodal cut on an intrinsic phase, "
    "theory/CRR.md section 2), so the row does not test the antipodal cut (the Hilbert antipode of the SoC cycle is offline "
    "and cannot trigger a charge; it is printed as a diagnostic only); (3) 'fixed schedule' read as two clock families, a "
    "timetable (a cycle at every wall time kP; skipped "
    "if the robot is already walking, charging or rescued) and an interval (a cycle T wall minutes after the last charge "
    "ended); the null is the best of both by uptime (ties: less wear, then grid order); (4) H0 read as the (s, S) family "
    "(charge at SoC <= s up to S), the best on its grid at the same wear bound; (5) the domain grid over S includes "
    "S = 1, so the CRR arm is H0's (s, 1) member and H0's optimum is never below it; with linear charging and one walk per "
    "cycle a charge to S < 1 only adds cycles and walks, so the model is built so that the (s, S) optimum can land on the "
    "CRR arm, and then T-N agrees whenever T-G differs and ADDS or WRONG cannot occur (whether it lands there is computed "
    "and printed); (6) minute steps, a continuous duty of 100 days from a full battery, the load path "
    "common to every policy (seed 0); the return walk from the dock folded into the charge (work resumes at the dock); "
    "(7) model constants ASSUMED round values (no source): light 1/300 and heavy 1/100 per min, dwell 45 min, walk 10 min at "
    "1/150 per min, charge 1/60 per min, rescue 60 min; the switching load (two states, 45-min dwell) is itself ASSUMED and "
    "T-G can turn on how much the load varies (a clock schedule can match a state trigger when the drain is constant); "
    "(8) the three selected policies re-run on a second load seed (seed 1) as an out-of-sample print, not scored; (9) "
    "sensitivities printed, not scored: the same grids and selection under a constant load (light, the seed-0 mean, heavy) "
    "with the label each would give; Q's 'any fixed schedule' read per schedule, each schedule scored against the best state "
    "trigger and the best (s, S) policy at no more than its own wear, with the distribution of labels")


def ra3_rates(seed, n_min):
    rng = np.random.default_rng(seed)
    h0 = int(rng.random() < 0.5)
    switch = rng.random(n_min) < 1.0 / DWELL
    heavy = (h0 + np.cumsum(switch)) % 2 == 1
    return np.where(heavy, HEAVY_RATE, LIGHT_RATE)


def ra3_policies():
    pols = [dict(fam="state", s=s, S=1.0, P=0, T=0) for s in S_GRID]
    pols += [dict(fam="timetable", s=-1.0, S=1.0, P=P, T=0) for P in P_GRID]
    pols += [dict(fam="interval", s=-1.0, S=1.0, P=0, T=T) for T in T_GRID]
    pols += [dict(fam="sS", s=s, S=S, P=0, T=0) for S in S_TARGETS for s in S_GRID if S >= s + 0.05 - 1e-12]
    return pols


def ra3_sim(pols, rates, trace=False):
    """Simulate every policy in `pols` on the same minute-by-minute load `rates`. Returns uptime minutes, charge cycles,
    brownouts (arrays) and, with trace=True, the SoC trace and trigger minutes of policy 0."""
    n = len(pols)
    thr = np.array([p["s"] for p in pols])
    tgt = np.array([p["S"] for p in pols])
    itv = np.array([float(p["T"]) if p["fam"] == "interval" else np.inf for p in pols])
    is_tt = np.array([p["fam"] == "timetable" for p in pols])
    per = np.array([p["P"] if p["fam"] == "timetable" else 1 for p in pols], dtype=np.int64)
    soc = np.ones(n); mode = np.full(n, WORK, dtype=np.int8); timer = np.zeros(n, dtype=np.int64)
    resume = np.zeros(n, dtype=np.int64)
    up = np.zeros(n, dtype=np.int64); cyc = np.zeros(n, dtype=np.int64); bo = np.zeros(n, dtype=np.int64)
    tr_soc = np.empty(len(rates)) if trace else None
    tr_trig = []
    for t in range(len(rates)):
        r = rates[t]
        work = mode == WORK
        due = (soc <= thr) | ((t - resume) >= itv) | (is_tt & (t > 0) & (t % per == 0))
        trig = work & due
        if trig.any():
            mode[trig] = WALK; timer[trig] = WALK_MIN; cyc[trig] += 1
            if trace and trig[0]:
                tr_trig.append(t)
        wk = mode == WORK; wl = mode == WALK; ch = mode == CHARGE; rs = mode == RESCUE
        soc[wk] -= r; up[wk] += 1
        soc[wl] -= WALK_RATE; timer[wl] -= 1
        dead = (wk | wl) & (soc <= 0.0)
        if dead.any():
            cyc[dead & wk] += 1; bo[dead] += 1                          # a brownout while walking is the same cycle
            soc[dead] = 0.0; mode[dead] = RESCUE; timer[dead] = RESCUE_MIN
        arrived = wl & ~dead & (timer == 0)
        mode[arrived] = CHARGE
        soc[ch] = np.minimum(tgt[ch], soc[ch] + CHARGE_RATE)
        full = ch & (soc >= tgt)
        mode[full] = WORK; resume[full] = t + 1
        timer[rs] -= 1
        back = rs & (timer == 0)
        mode[back] = CHARGE
        if trace:
            tr_soc[t] = soc[0]
    return up, cyc, bo, tr_soc, np.asarray(tr_trig, dtype=np.int64)


def _best(idx, up, cyc, bound=None):
    ok = [i for i in idx if bound is None or cyc[i] <= bound]
    if not ok:
        return None
    return sorted(ok, key=lambda i: (-up[i], cyc[i], i))[0]


def ra3_select(up, cyc, i_state, i_sched, i_ss):
    """The row's selection: the best fixed schedule by uptime (ties: less wear, then grid order), its wear w*, and the best
    state trigger and the best (s, S) policy at no more than w* charge cycles."""
    b_null = _best(i_sched, up, cyc)
    w_star = int(cyc[b_null])
    return b_null, w_star, _best(i_state, up, cyc, w_star), _best(i_ss, up, cyc, w_star)


def _pname(p):
    if p["fam"] == "state":
        return f"state s = {p['s']:.2f}"
    if p["fam"] == "timetable":
        return f"timetable P = {p['P']} min"
    if p["fam"] == "interval":
        return f"interval T = {p['T']} min"
    return f"(s, S) = ({p['s']:.2f}, {p['S']:.1f})"


def ra3():
    print("CHOICES RA3: " + CHOICES_RA3)
    print()
    n_min = MIN_DAY * N_DAYS
    rates = ra3_rates(SEED3, n_min)
    pols = ra3_policies()
    up, cyc, bo, _, _ = ra3_sim(pols, rates)
    fam = lambda f: [i for i, p in enumerate(pols) if p["fam"] == f]
    i_state, i_tt, i_iv, i_ss = fam("state"), fam("timetable"), fam("interval"), fam("sS")
    i_sched = i_tt + i_iv
    b_null, w_star, b_crr, b_dom = ra3_select(up, cyc, i_state, i_sched, i_ss)
    b_tt, b_iv = _best(i_tt, up, cyc), _best(i_iv, up, cyc)
    b_crr_free = _best(i_state, up, cyc)
    perday = lambda a, i: a[i] / N_DAYS
    mean_rate = float(rates.mean())

    print(f"RA3 load path (seed {SEED3}): {N_DAYS} days = {n_min} min; share of heavy-load minutes "
          f"{float(np.mean(rates == HEAVY_RATE)):.4f}; mean work drain {mean_rate:.6f} per min (a full battery lasts "
          f"{1.0 / mean_rate:.1f} min at the mean)")
    print("RA3 state-trigger family (CRR; charge to full): s, uptime h/day, charge cycles/day, brownouts/day")
    for i in i_state:
        if pols[i]["s"] in (0.01, 0.02, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60):
            print(f"  s = {pols[i]['s']:.2f}: {perday(up, i) / 60:.4f} h, {perday(cyc, i):.2f} cycles, {perday(bo, i):.2f} brownouts")
    for name, idx in (("timetable", i_tt), ("interval", i_iv)):
        top = sorted(idx, key=lambda i: (-up[i], cyc[i], i))[:5]
        print(f"RA3 {name} family, five best by uptime: " + "; ".join(
            f"{_pname(pols[i])}: {perday(up, i) / 60:.4f} h, {perday(cyc, i):.2f} cycles, {perday(bo, i):.2f} brownouts" for i in top))
    print("RA3 (s, S) family (H0), best per target S at wear <= the best schedule's: " + "; ".join(
        f"S = {S:.1f}: " + (lambda b: f"{_pname(pols[b])}, {perday(up, b) / 60:.4f} h, {perday(cyc, b):.2f} cycles"
                            if b is not None else "none")(_best([i for i in i_ss if pols[i]["S"] == S], up, cyc, w_star))
        for S in S_TARGETS))
    # Q's literal 'any fixed schedule': per schedule, the best state trigger (T-G, T-C) and the best (s, S) policy (T-N)
    # at no more wear than that schedule, and the label outcome() gives that schedule
    held, none_j, behind_j = 0, [], []
    worst = None
    lab_any = {lab: 0 for lab in LABELS}
    for j in i_sched:
        b = _best(i_state, up, cyc, int(cyc[j]))
        if b is None:
            none_j.append(j)
            continue
        bd = _best(i_ss, up, cyc, int(cyc[j]))
        d = int(up[b]) - int(up[j])
        held += int(d >= 0)
        if d < 0:
            behind_j.append(j)
        worst = d if worst is None else min(worst, d)
        lab_any[outcome(crr=float(up[b]), null=float(up[j]), domain=float(up[bd]), check=bool(d >= 0))] += 1
    wr = lambda js: f"{min(cyc[j] for j in js) / N_DAYS:.2f}-{max(cyc[j] for j in js) / N_DAYS:.2f}" if js else "none"
    allbo = lambda js: _w(all(bo[j] > 0 for j in js), "yes", "no") if js else "n/a"
    any_stats = (f"the best state trigger at no more wear has at least the schedule's uptime for {held} of {len(i_sched)} "
                 f"schedules; it is behind for {len(behind_j)} (wear {wr(behind_j)} cycles/day; every one of them browns out: "
                 f"{allbo(behind_j)}; largest shortfall {-min(0, worst) / N_DAYS:.2f} min/day) and no state trigger reaches the "
                 f"wear of {len(none_j)} (wear {wr(none_j)} cycles/day; every one of them browns out: {allbo(none_j)}); the "
                 f"lowest wear of a state trigger without brownouts is "
                 + (lambda js: f"{min(cyc[i] for i in js) / N_DAYS:.2f} cycles/day" if js else "none")(
                     [i for i in i_state if bo[i] == 0]))
    print("RA3 per schedule (Q's 'any fixed schedule', printed, not scored): " + any_stats)
    any_labels = (" / ".join(f"{n} {lab}" for lab, n in lab_any.items() if n) or "none") + \
        f"; not computable (no state trigger at that wear) {len(none_j)}"
    print("RA3 per schedule, the label outcome() gives each schedule (T-G: the best state trigger at no more than the "
          "schedule's wear against the schedule; T-N: the best (s, S) at the same bound; T-C: the trigger not behind; "
          f"printed, not scored): {any_labels}")
    # the CRR arm inside H0's family: every state policy has an (s, 1.0) twin in the (s, S) grid
    twin = {pols[i]["s"]: i for i in i_ss if pols[i]["S"] == 1.0}
    twins_same = all(int(up[i]) == int(up[twin[pols[i]["s"]]]) and int(cyc[i]) == int(cyc[twin[pols[i]["s"]]])
                     for i in i_state)
    b_lt1 = _best([i for i in i_ss if pols[i]["S"] < 1.0], up, cyc, w_star)
    h0_ge = bool(up[b_dom] >= up[b_crr])
    print(f"RA3 the CRR arm inside H0's family: every state trigger's (s, 1.0) twin has the same uptime and cycles: "
          f"{_w(twins_same, 'yes', 'no')} ({len(i_state)} twins); H0's optimum at the wear bound {_pname(pols[b_dom])}, "
          f"not below the CRR arm: {_w(h0_ge, 'yes', 'no')}; the best (s, S) with S < 1 at the bound: "
          + (f"{_pname(pols[b_lt1])} {up[b_lt1] / N_DAYS / 60:.6f} h" if b_lt1 is not None else "none"))
    # constant-load sensitivity: the same grids and selection with the drain held at one value
    sens = []
    for lab, rate in (("light", LIGHT_RATE), ("mean", mean_rate), ("heavy", HEAVY_RATE)):
        uc, cc, bc_, _, _ = ra3_sim(pols, np.full(n_min, rate))
        sn, sw, sc, sd = ra3_select(uc, cc, i_state, i_sched, i_ss)
        if sc is None:
            sens.append((lab, rate, None, f"{lab} drain {rate:.6f}/min: no state trigger at the best schedule's wear "
                                          f"({_pname(pols[sn])}, {cc[sn] / N_DAYS:.2f} cycles/day): not computable"))
            continue
        cr, nu, do = uc[sc] / N_DAYS / 60, uc[sn] / N_DAYS / 60, uc[sd] / N_DAYS / 60
        so = outcome(crr=cr, null=nu, domain=do, check=bool(uc[sc] >= uc[sn]))
        sens.append((lab, rate, so,
                     f"{lab} drain {rate:.6f}/min: null {_pname(pols[sn])} {nu:.6f} h ({cc[sn] / N_DAYS:.2f} cycles/day, "
                     f"{bc_[sn] / N_DAYS:.2f} brownouts/day), CRR {_pname(pols[sc])} {cr:.6f} h ({cc[sc] / N_DAYS:.2f} "
                     f"cycles/day, {bc_[sc] / N_DAYS:.2f} brownouts/day), T-G relative difference {rel(cr, nu):.4e} "
                     f"({_w(rel(cr, nu) <= TOL_G, 'agree', 'differ')}), H0 {_pname(pols[sd])} {do:.6f} h; label {so}"))
    print(f"RA3 sensitivity, constant load (the same grids and selection, {N_DAYS} days; printed, not scored): "
          + "; ".join(s[3] for s in sens))

    # ---- the selected policies, re-run with a trace (seed 0) and out of sample (seed 1)
    sel = [b_crr, b_null, b_dom]
    up0, cyc0, bo0, tr, trig = ra3_sim([pols[b_crr]], rates, trace=True)
    same = int(up0[0]) == int(up[b_crr]) and int(cyc0[0]) == int(cyc[b_crr])
    rates1 = ra3_rates(SEED3_OOS, n_min)
    up1, cyc1, bo1, _, _ = ra3_sim([pols[b] for b in sel], rates1)
    print(f"RA3 out of sample (load seed {SEED3_OOS}, printed, not scored): " + "; ".join(
        f"{lab} {_pname(pols[b])}: {up1[k] / N_DAYS / 60:.4f} h/day, {cyc1[k] / N_DAYS:.2f} cycles/day, "
        f"{bo1[k] / N_DAYS:.2f} brownouts/day" for k, (lab, b) in enumerate(zip(("CRR", "null", "H0"), sel))))

    # ---- A3 diagnostic on the CRR arm's SoC trace
    ends = np.flatnonzero((tr[1:] >= 1.0) & (tr[:-1] < 1.0)) + 1           # minutes at which a charge reaches full
    start = int(ends[0])
    ph = intrinsic_phase(tr)
    cuts = antipodal_cuts(ph, start=start)
    anti = cuts[1::2]
    trig_after = trig[trig > start]
    near = lambda c: trig_after[np.argmin(np.abs(trig_after - c))]
    off = np.array([c - near(c) for c in anti], dtype=float)
    cyc_len = np.diff(trig_after).astype(float)
    pk = peak_cuts(tr, prominence=0.3, distance=30)
    troughs = np.array([i for i in pk if i > start and tr[i] < 0.5])
    off_tr = np.array([c - near(c) for c in troughs], dtype=float)
    diag = (f"A3 diagnostic (printed, not scored): on the CRR arm's SoC trace ({len(trig_after)} triggers after the first "
            f"full charge; median cycle {np.median(cyc_len):.1f} min), the antipodal cuts of the Hilbert phase (A3: every half "
            f"turn from the first full charge; the {len(anti)} odd cuts, the antipodes of that phase) land a median {np.median(off):+.1f} min (median |offset| "
            f"{np.median(np.abs(off)):.1f} min = {np.median(np.abs(off)) / np.median(cyc_len):.3f} of a cycle) from the "
            f"nearest SoC trigger; the extremum cuts (troughs, find_peaks prominence 0.3, distance 30) land "
            f"{np.median(off_tr):+.1f} min from it"
            + _w(abs(float(np.median(off_tr)) - WALK_MIN) <= 1.0, " (the walk to the dock)", ""))
    print("RA3 " + diag)
    print(f"RA3 trace re-run reproduces the grid run's uptime and cycles for the CRR arm: {_w(same, 'yes', 'no')}")
    print("RA3 FLAG (for the tally): the scored ingredient is a scalar threshold on the robot's own SoC, the declaration's "
          "reading of A3 ('the cut at the system's own event'), not A3 proper (the antipodal cut on an intrinsic phase); "
          "the row does not test the antipodal cut")
    print()

    crr, null, dom = perday(up, b_crr) / 60, perday(up, b_null) / 60, perday(up, b_dom) / 60
    check = bool(up[b_crr] >= up[b_null])
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    n_fail_any = len(behind_j) + len(none_j)
    any_txt = (f"Q's 'any fixed schedule' read per schedule (the declared T-C compares with the best schedule): {any_stats}; "
               f"under that reading Q fails for {n_fail_any} of {len(i_sched)} schedules, and the label outcome() gives each "
               f"schedule is: {any_labels}; the harness gives one label per row, so this reading gives a distribution, not "
               f"one label")
    dom_same = pols[b_dom]["S"] == 1.0 and pols[b_dom]["s"] == pols[b_crr]["s"]
    diff_min = 60 * (crr - null)
    dcyc = perday(cyc, b_null) - perday(cyc, b_crr)
    either = all(cyc[j] > cyc[b_crr] or bo[j] > 0 for j in i_sched)
    turns = any(s[2] != out for s in sens) if sens else False
    sens_lab = ", ".join(f"{s[0]} {s[2] if s[2] is not None else 'not computable'}" for s in sens)
    more_less = lambda x, a, b: f"{abs(x):.2f} {_w(x >= 0, a, b)}"
    row = make_row(
        "rob", "RA3 charging as a cut on the robot's own state (model: a humanoid on a continuous 24-hour duty, SoC in [0, 1], "
        "work drain switching in wall time between light (5 h per battery) and heavy (1 h 40 min), mean dwell 45 min; a cycle "
        "is a 10-min walk to the dock, a linear charge (60 min empty to full) and resumed work; a brownout costs a 60-min "
        "rescue and a charge from 0; wear one unit per charge cycle; 100 simulated days, load seed 0, every policy on the "
        "same load)",
        source=SRC.format(a="RA3"),
        Q="A cut at the robot's own state of charge gives more uptime at equal wear than any fixed schedule. Decisive quantity: "
          "uptime per day (h) at no more charge cycles than the best fixed schedule.",
        ingredient="a scalar threshold on the robot's own SoC, the declaration's reading of A3 ('the cut at the system's own "
                   "event'), not A3 proper (the antipodal cut on an intrinsic phase; printed as a diagnostic only): a charge "
                   "cycle starts when the robot's own SoC reaches s, and the charge restores full; the best s on the grid "
                   "0.01..0.60 at the wear bound",
        null="the best fixed schedule over two wall-clock families (a timetable, a cycle at every wall time kP, P = 60..600 "
             "min; an interval, a cycle T = 30..400 wall minutes after the last charge ended), both charging to full",
        domain="threshold policies for depletion-and-replenish problems ((s, S) type; optimal stopping): a cycle at SoC <= s, "
               "charge to S in {0.6, ..., 1.0}; the best on the grid at the same wear bound (the grid contains the CRR arm "
               "as its (s, 1.0) members)",
        numbers=f"uptime per day at wear <= {w_star / N_DAYS:.2f} cycles/day (the best schedule's): CRR {_pname(pols[b_crr])} "
                f"{crr:.6f} h ({perday(cyc, b_crr):.2f} cycles/day, {perday(bo, b_crr):.2f} brownouts/day); null "
                f"{_pname(pols[b_null])} {null:.6f} h ({perday(cyc, b_null):.2f} cycles/day, {perday(bo, b_null):.2f} "
                f"brownouts/day); H0 {_pname(pols[b_dom])} {dom:.6f} h ({perday(cyc, b_dom):.2f} cycles/day); best per "
                f"schedule family: {_pname(pols[b_tt])} {perday(up, b_tt) / 60:.6f} h ({perday(cyc, b_tt):.2f} "
                f"cycles/day), {_pname(pols[b_iv])} {perday(up, b_iv) / 60:.6f} h ({perday(cyc, b_iv):.2f} "
                f"cycles/day); the best state trigger without the wear bound {_pname(pols[b_crr_free])} "
                f"{perday(up, b_crr_free) / 60:.6f} h; commercial quantity (model units): uptime per day CRR {crr:.4f} h, "
                f"best fixed schedule {null:.4f} h, a difference of {diff_min:.2f} min/day with "
                f"{more_less(dcyc, 'fewer', 'more')} charge cycles per day; out of sample (seed "
                f"{SEED3_OOS}): CRR {up1[0] / N_DAYS / 60:.4f} h, null {up1[1] / N_DAYS / 60:.4f} h, H0 {up1[2] / N_DAYS / 60:.4f} h; "
                f"constant-load sensitivity labels: {sens_lab}",
        tg=f"uptime {crr:.6f} h vs the best fixed schedule {null:.6f} h (relative difference {rel(crr, null):.4e}): "
           f"{_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"the (s, S) optimum {dom:.6f} h ({_pname(pols[b_dom])}; the same policy as the CRR arm: {_w(dom_same, 'yes', 'no')}): "
           f"{_w(rel(crr, dom) <= TOL_N, 'agree (the domain has the state-triggered threshold policy)', 'differ')}",
        tc=f"state-triggered uptime {int(up[b_crr])} min over {N_DAYS} days at {int(cyc[b_crr])} cycles >= the best schedule's "
           f"{int(up[b_null])} min at {int(cyc[b_null])} cycles: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"the fixed schedules read the wall clock, not the load; every schedule either charges more often than the "
                f"trigger or browns out: {_w(either, 'yes', 'no')}; the trigger on the robot's own SoC ({_pname(pols[b_crr])}, "
                f"{perday(bo, b_crr):.2f} brownouts/day) gives {more_less(diff_min, 'min/day more', 'min/day less')} uptime "
                f"than the best schedule at {more_less(dcyc, 'fewer', 'more')} cycles per day; the CRR arm is H0's (s, 1.0) "
                f"member (identical twins: {_w(twins_same, 'yes', 'no')}), so H0's optimum is never below it (here: "
                f"{_w(h0_ge, 'yes', 'no')}), and with linear charging and one walk per cycle a charge to S < 1 only adds walks: "
                f"the (s, S) optimum on its grid is "
                + _w(dom_same, "the CRR arm itself, so the cut at the system's own event is the domain's reorder point and, by "
                               "construction, T-N agrees whenever T-G differs: the row cannot tell the trigger from the "
                               "domain's policy",
                     "a different policy from the CRR arm")
                + f"; T-G {_w(turns, 'turns', 'does not turn')} on the load's variation (the ASSUMED switching load): under a "
                f"constant load the row would read {sens_lab}"
                + _w(any(s[2] == "REDUNDANT-IG" for s in sens), ", where a fixed schedule matches the trigger within "
                     "the T-G tolerance", "")
                + f"; the scored ingredient is a scalar SoC threshold, the declaration's reading of A3, not the antipodal cut "
                f"(diagnostic in the weakness field); under the per-schedule reading of Q it fails for {n_fail_any} of "
                f"{len(i_sched)} schedules ({len(behind_j)} ahead of every state trigger at no more wear, {len(none_j)} at a "
                f"wear no trigger reaches; weakness): {out}",
        weakness="CHOICE: " + CHOICES_RA3 + "; " + diag + " (A3 proper is the antipode on an intrinsic phase, computed "
                 "offline; the row tests A3 in the declaration's reading, the cut at the system's own event, and the Hilbert "
                 "antipode is printed only for comparison); " + any_txt,
        elegance="", child="")
    return row


# ====================================================================================== RA4 lost link and the empty cut
GW, GH = 7, 5
HOME, INSPECT = (0, 2), (6, 2)
BAND = frozenset({(3, 1), (3, 2), (3, 3)})
GAMMA4, D4 = 0.95, 30
L4_GRID = (1, 5, 20)
DEC_L = 20                                                             # EPS1 S1's decisive cell: L = 20 with the deadline
WORLDS4 = ("no deadline", "deadline")
ARMS4 = ("WALL", "OWN", "ETM", "H0")
ACTS = ("land", "N", "E", "S", "W")                                    # tie order: the first optimal action in this order
STEP = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}


def _cells():
    return [(x, y) for y in range(GH) for x in range(GW)]


def _move(cell, a):
    dx, dy = STEP[a]
    x, y = cell[0] + dx, cell[1] + dy
    return (x, y) if 0 <= x < GW and 0 <= y < GH else None


def _entry(cell, nxt):
    return nxt in BAND and cell not in BAND


def _bfs(src, blocked=frozenset()):
    """Grid distances in flight moves from src, never entering a blocked cell."""
    dist, queue = {src: 0}, [src]
    for cell in queue:
        for act in ("N", "E", "S", "W"):
            nxt = _move(cell, act)
            if nxt is not None and nxt not in blocked and nxt not in dist:
                dist[nxt] = dist[cell] + 1
                queue.append(nxt)
    return dist


DIST_HOME = _bfs(HOME)                                                 # also the autopilot's flight home (RTH sensitivity)
D_DIRECT = DIST_HOME[INSPECT]                                          # the shortest leg
D_THROUGH = min(DIST_HOME[b] + _bfs(b)[INSPECT] for b in BAND)         # the shortest leg through a band cell
D_AVOID = _bfs(HOME, BAND)[INSPECT]                                    # the shortest leg round the band


def _hover_mission(L):
    """Wall ticks of the shortest out-and-back mission with at least one lost-link hover of L ticks (one leg through the
    band, one hover on it, the other leg round the band; or both legs through it)."""
    return min(D_THROUGH + L + D_AVOID, 2 * (D_THROUGH + L))


CHOICES_RA4 = (
    f"(1) the lost-link region is a radio-shadow band of three cells across the direct route of a {GW} x {GH} grid; the "
    f"mission is out and back (inspect A = {INSPECT}, reward 1; return home, reward 1, ending the episode); a detour round "
    f"either end of the band costs {D_AVOID - D_DIRECT} extra moves each way (BFS on the grid; the simplest mission with "
    "the region on its direct route); (2) every move into "
    "a band cell from outside the band triggers lost link: a hover of L wall ticks, then the link returns and the drone "
    "resumes in the same cell ('hover and return' read as a pause the drone resumes from; a return-to-home that sends the "
    "drone elsewhere would be a restart, not a pause, and is computed for ETM as a sensitivity, (10)); (3) gamma = "
    f"{GAMMA4} per tick of the arm's clock, the deadline D = {D4} "
    "wall ticks (ETM: own steps) and L in {1, 5, 20} are EPS1 S1's values ('as in EPS1'); a reward counts only if it "
    "arrives by the arm's deadline clock; (4) H0's compensation is the stake under the compensated agent's own value, "
    "V(cell, clock + 1) - gamma^L V(cell, clock + 1 + L), paid with the pause (Armstrong's indifference as in EPS1 S2); "
    "(5) avoidance is scored per mission leg on the greedy plan from home: the no-pause plan (L = 0, identical for every "
    "arm) flies both legs through the band; avoidance rate = legs the arm completes round the band over legs it completes, "
    "seek rate = legs it completes with more band entries than the no-pause leg over legs it completes; a leg not completed "
    "(the drone lands because its own deadline has passed and no route has value) is printed as abandoned, not as "
    "avoidance; the declaration does not define 'avoidance rate', and this reading was fixed before the first run but after "
    "a hand calculation of H0's plan in the decisive cell (it abandons the return leg at L = 20 with the deadline), so it "
    "was chosen with H0's behaviour there known; two other readings are computed and printed with the label each gives: "
    "the entry count (band entries dropped over the whole plan, over the no-pause plan's entries) and the reference legs "
    "(legs flown round the band over the no-pause plan's legs through the band, an abandoned leg counted as not avoided); "
    "the row is printed as READING-DEPENDENT when the three labels differ; ties within 1e-12 x max(1, |Q|) go to the first "
    "action in the order land, N, E, S, W; (6) stake k = V*(start; pause 0) - V*(start; pause L) "
    "under the arm's valuation; (7) the decisive cell is EPS1 S1's: L = 20 with the deadline; (8) no world in which a "
    "pause pays was declared, so the seek rate is printed but 'does not seek' is not tested beyond these two worlds; "
    "(9) the commercial quantity, mission value lost to avoidance, is printed as extra flight moves and inspection or "
    "return rewards forgone against the no-pause plan (model units); (10) the return-to-home reading of 'hover and return' "
    "is computed for ETM only, printed, not scored: after the hover the autopilot flies the drone home (not the drone's own "
    "moves; wall ticks = the grid distance home), the link returns at home, the mission resumes from home with the "
    "inspection flag kept, and an autopilot arrival home after the inspection ends the mission with the return reward; "
    "the pause then moves the drone, so it has content")


class Drone:
    """Exact solver for one (arm, L, world). State (cell, a, c): a = 1 once A is inspected; c = the arm's deadline clock
    (wall ticks for WALL, OWN, H0; own steps for ETM), absent (0) in the no-deadline world. V(state) is the optimal value
    to go, discounted from the current tick. rth=True (ETM only) is the return-to-home sensitivity: a band entry sends the
    drone home after the pause."""

    def __init__(self, arm, L, deadline, rth=False):
        if rth and arm != "ETM":
            raise ValueError("the return-to-home sensitivity is defined for ETM only")
        self.arm, self.L, self.deadline, self.rth = arm, L, deadline, rth
        self.V = {}
        if deadline:
            for c in range(D4, -1, -1):                                   # every move advances the clock: backward induction
                for cell in _cells():
                    for a in (0, 1):
                        self.V[(cell, a, c)] = max(self.q_all(cell, a, c).values())
        else:
            for cell in _cells():
                for a in (0, 1):
                    self.V[(cell, a, 0)] = 0.0
            self.iters = 0
            while True:                                                    # value iteration to its exact fixed point
                newV = {s: max(self.q_all(*s).values()) for s in self.V}
                self.iters += 1
                if newV == self.V:
                    break
                self.V = newV
                if self.iters > 10000:
                    raise RuntimeError("value iteration did not reach a fixed point")

    def v(self, cell, a, c):
        if self.deadline and c > D4:
            return 0.0
        return self.V[(cell, a, c if self.deadline else 0)]

    def arrive(self, cell, nxt, a, c):
        """(reward, a', terminal, pause, own-clock arrival c_arr, clock after the pause c_next, cell after the pause)."""
        p = int(_entry(cell, nxt))
        wall_arm = self.arm in ("WALL", "OWN", "H0")
        c_arr = c + 1 if self.deadline else 0
        c_next = (c + 1 + (self.L * p if wall_arm else 0)) if self.deadline else 0
        ok = (not self.deadline) or c_arr <= D4
        dest = HOME if (self.rth and p) else nxt
        if dest == INSPECT and a == 0:
            return (1.0 if ok else 0.0), 1, False, p, c_arr, c_next, dest
        if dest == HOME and a == 1:
            return (1.0 if ok else 0.0), 1, True, p, c_arr, c_next, dest
        return 0.0, a, False, p, c_arr, c_next, dest

    def q(self, cell, a, c, act):
        if act == "land":
            return 0.0
        nxt = _move(cell, act)
        if nxt is None:
            return None
        r, a2, term, p, c_arr, c_next, dest = self.arrive(cell, nxt, a, c)
        g, L = GAMMA4, self.L
        if term:
            return g * r
        if self.arm == "ETM":                                             # own clock: the pause is not its step
            return g * (r + self.v(dest, a2, c_arr))
        if self.arm == "OWN":                                             # own-step discount, deadline on the wall clock
            return g * (r + self.v(dest, a2, c_next))
        cont = (g ** (L * p)) * self.v(dest, a2, c_next)
        if self.arm == "WALL":
            return g * (r + cont)
        comp = p * (self.v(dest, a2, c_arr) - (g ** L) * self.v(dest, a2, c_next))   # H0: the stake, paid with the pause
        return g * (r + cont + comp)

    def q_all(self, cell, a, c):
        out = {}
        for act in ACTS:
            val = self.q(cell, a, c, act)
            if val is not None:
                out[act] = val
        return out

    def choose(self, cell, a, c):
        qs = self.q_all(cell, a, c)
        best = max(qs.values())
        for act in ACTS:
            if act in qs and qs[act] >= best - TIE_TOL * max(1.0, abs(best)):
                return act

    def plan(self):
        """The greedy plan from home: flight moves, wall ticks, band entries in total and per leg (leg 0 home -> A, leg 1
        A -> home), legs completed, rewards (the arm's own count) and their wall ticks."""
        cell, a, c, t, n, entries, rew, rew_wall = HOME, 0, 0, 0, 0, 0, 0, []
        leg_entries, done = [0, 0], [False, False]
        for _ in range(500):
            act = self.choose(cell, a, c)
            if act == "land":
                break
            nxt = _move(cell, act)
            r, a2, term, p, c_arr, c_next, dest = self.arrive(cell, nxt, a, c)
            n += 1
            t += 1 + self.L * p + (DIST_HOME[nxt] if (self.rth and p) else 0)   # the move, the hover, the autopilot
            if r > 0:
                rew += 1; rew_wall.append(t)
            leg_entries[a] += p
            if (dest == INSPECT and a == 0) or term:
                done[a] = True
            entries += p
            cell, a, c = dest, a2, (c_arr if self.arm == "ETM" else c_next)
            if term:
                break
        else:
            raise RuntimeError("plan did not end")
        return dict(n=n, t=t, entries=entries, rew=rew, rew_wall=rew_wall, leg_entries=leg_entries, done=done)


def _legs(pl, ref):
    """Per-leg readings against the no-pause plan: each leg the reference flies through the band is avoided (completed with
    no band entry), kept (completed through the band) or abandoned (not completed); seek = a completed leg with more band
    entries than the reference leg. avoid: over the legs completed (scored); avoid_ref: over the reference legs, an
    abandoned leg counted as not avoided."""
    avoided = kept = aband = seek = n_ref = 0
    for k in (0, 1):
        if ref["leg_entries"][k] == 0 or not ref["done"][k]:
            continue
        n_ref += 1
        if not pl["done"][k]:
            aband += 1
        elif pl["leg_entries"][k] == 0:
            avoided += 1
        else:
            kept += 1
            seek += int(pl["leg_entries"][k] > ref["leg_entries"][k])
    flown = avoided + kept
    return dict(avoid=(avoided / flown if flown else float("nan")), seek=(seek / flown if flown else float("nan")),
                avoid_ref=(avoided / n_ref if n_ref else float("nan")),
                legs_avoided=avoided, legs_kept=kept, legs_abandoned=aband)


def _vdiff(d1, d2):
    return max(abs(d1.V[s] - d2.V[s]) for s in d1.V)


def ra4():
    print("CHOICES RA4: " + CHOICES_RA4)
    print()
    cells, ref, vdiff, base_diff, rth = {}, {}, {}, {}, {}
    for world in WORLDS4:
        dl = world == "deadline"
        base = {arm: Drone(arm, 0, dl) for arm in ARMS4}
        pr = {arm: base[arm].plan() for arm in ARMS4}
        ref[world] = pr["WALL"]
        same_ref = all(pr[arm]["entries"] == pr["WALL"]["entries"] and pr[arm]["n"] == pr["WALL"]["n"] for arm in ARMS4)
        base_diff[world] = max(_vdiff(base[arm], base["WALL"]) for arm in ARMS4)
        e0 = ref[world]["entries"]
        if e0 == 0 or not all(ref[world]["done"]):
            raise RuntimeError("the no-pause plan must fly both legs through the band")
        for L in L4_GRID:
            for arm in ARMS4:
                d = Drone(arm, L, dl)
                pl = d.plan()
                vdiff[(world, L, arm)] = _vdiff(d, base[arm])
                cells[(world, L, arm)] = dict(
                    k=base[arm].v(HOME, 0, 0) - d.v(HOME, 0, 0), V=d.v(HOME, 0, 0),
                    avoid_e=max(0, e0 - pl["entries"]) / e0, seek_e=max(0, pl["entries"] - e0) / e0,
                    extra=pl["n"] - ref[world]["n"], forgone=ref[world]["rew"] - pl["rew"],
                    by_d=sum(1 for w in pl["rew_wall"] if w <= D4), **_legs(pl, ref[world]), **pl)
            d = Drone("ETM", L, dl, rth=True)
            pl = d.plan()
            rth[(world, L)] = dict(k=base["ETM"].v(HOME, 0, 0) - d.v(HOME, 0, 0), avoid_e=max(0, e0 - pl["entries"]) / e0,
                                   **_legs(pl, ref[world]), **pl)
        print(f"RA4 reference (no-pause) plan, {world}: {ref[world]['n']} flight moves, band entries per leg "
              f"{ref[world]['leg_entries']}, {ref[world]['rew']} rewards; identical for every arm at L = 0: {_w(same_ref, 'yes', 'no')}; "
              f"the four arms' no-pause value tables agree (max difference {base_diff[world]:.1e})")
    print(f"RA4 geometry (BFS on the grid): the shortest leg {D_DIRECT} moves (through a band cell {D_THROUGH}), round the "
          f"band {D_AVOID}; the all-detour mission ends at wall tick {2 * D_AVOID}; the shortest mission with at least one "
          f"lost-link hover of L ticks ends at wall tick min(through + L + round, 2 (through + L)); against D = {D4}: " + "; ".join(
              f"L = {L}: detour {2 * D_AVOID} {_w(2 * D_AVOID <= D4, '<=', '>')} {D4}, with a hover {_hover_mission(L)} "
              f"{_w(_hover_mission(L) <= D4, '<=', '>')} {D4}" for L in L4_GRID))
    print()
    print(f"RA4 per-cell table (gamma = {GAMMA4} per tick of the arm's clock; D = {D4}; k = V*(pause 0) - V*(pause L) from home;")
    print("  avoid / seek = legs flown round the band / with extra band entries, over the legs completed (the reading scored);")
    print("  aband = legs of the no-pause plan not completed; avoid_e / seek_e = band entries dropped / added over the whole plan")
    print("  (the entry-count reading); avoid_r = legs flown round the band over the no-pause plan's legs, an abandoned leg not")
    print("  avoided (the reference-legs reading); moves = flight moves; end = wall tick at the end of the plan; rewards =")
    print("  counted by the arm's own deadline clock; by D = rewards arriving by wall tick D):")
    print(f"  {'world':12} {'L':>3} {'arm':5} {'k':>14} {'avoid':>6} {'seek':>5} {'aband':>5} {'avoid_e':>7} {'seek_e':>6} "
          f"{'avoid_r':>7} {'entries':>7} {'moves':>6} {'end':>5} {'rewards':>8} {'by D':>5}")
    for (world, L, arm), c in cells.items():
        print(f"  {world:12} {L:>3} {arm:5} {c['k']:>14.6e} {c['avoid']:>6.2f} {c['seek']:>5.2f} {c['legs_abandoned']:>5d} "
              f"{c['avoid_e']:>7.2f} {c['seek_e']:>6.2f} {c['avoid_ref']:>7.2f} {c['entries']:>7d} {c['n']:>6d} {c['t']:>5d} "
              f"{c['rew']:>8d} {c['by_d']:>5d}")
    print()
    etm_k = [abs(c["k"]) for (w, L, a), c in cells.items() if a == "ETM"]
    h0_k = [abs(c["k"]) for (w, L, a), c in cells.items() if a == "H0"]
    wall_av = max(c["avoid"] for (w, L, a), c in cells.items() if a == "WALL")
    seek_max = max(c["seek"] for c in cells.values())
    etm_vd = max(v for (w, L, a), v in vdiff.items() if a == "ETM")
    h0_vd = max(v for (w, L, a), v in vdiff.items() if a == "H0")
    print(f"RA4 checks (printed; DECLARATION_4B declares no gate): ETM stake max |k| = {max(etm_k):.3e} over {len(etm_k)} "
          f"cells (exactly zero: {_w(max(etm_k) == 0.0, 'yes', 'no')}); H0 stake max |k| = {max(h0_k):.3e} (exactly zero: "
          f"{_w(max(h0_k) == 0.0, 'yes', 'no, round-off of the compensation')}); WALL max avoidance rate {wall_av:.2f}; max seek rate over all cells {seek_max:.2f}")
    print(f"RA4 construction checks: ETM's value table at every L against its no-pause table, max |difference| over every "
          f"state {etm_vd:.1e} (ETM's valuation never reads L, so T-C "
          f"{_w(etm_vd == 0.0, 'holds by construction', 'is not fixed by construction')}); H0's value table at every L "
          f"against the no-pause table, max |difference| {h0_vd:.1e} (the compensation cancels the pause algebraically: "
          f"gamma^L V(after the pause) + [V(no pause) - gamma^L V(after the pause)] = V(no pause))")
    rth_k = max(abs(c["k"]) for c in rth.values())
    print("RA4 sensitivity, return-to-home lost link (ETM only; CHOICES (10); printed, not scored): " + "; ".join(
        f"{w}, L = {L}: k = {c['k']:.6f}, avoid {c['avoid']:.2f} (entry count {c['avoid_e']:.2f}, reference legs "
        f"{c['avoid_ref']:.2f}), seek {c['seek']:.2f}, own moves {c['n']}, band entries per leg {c['leg_entries']}, "
        f"rewards {c['rew']}" for (w, L), c in rth.items())
        + f"; ETM's stake is {_w(rth_k > 0.0, 'not zero', 'zero')} under this reading (max |k| {rth_k:.6f}): the pause moves "
          f"the drone, so it carries content, and Proposition 7's premise (a pause with no content) "
          f"{_w(rth_k > 0.0, 'does not hold: Q does not apply under this reading', 'still gives zero stake here')}")

    dec = {a: cells[("deadline", DEC_L, a)] for a in ARMS4}
    crr, null, dom = dec["ETM"]["avoid"], dec["OWN"]["avoid"], dec["H0"]["avoid"]
    etm_cells = [c for (w, L, a), c in cells.items() if a == "ETM"]
    etm_zero = all(c["avoid"] == 0.0 for c in etm_cells)
    etm_noseek = all(c["seek"] == 0.0 and c["seek_e"] == 0.0 for c in etm_cells)
    etm_direct = all(c["leg_entries"] == ref[w]["leg_entries"] and all(c["done"])
                     for (w, L, a), c in cells.items() if a == "ETM")
    wall_clause = any(c["avoid"] > 0 and (c["extra"] > 0 or c["forgone"] > 0) for (w, L, a), c in cells.items() if a == "WALL")
    check = etm_zero
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    out_e = outcome(crr=dec["ETM"]["avoid_e"], null=dec["OWN"]["avoid_e"], domain=dec["H0"]["avoid_e"],
                    check=all(c["avoid_e"] == 0.0 for c in etm_cells))
    out_r = outcome(crr=dec["ETM"]["avoid_ref"], null=dec["OWN"]["avoid_ref"], domain=dec["H0"]["avoid_ref"],
                    check=all(c["avoid_ref"] == 0.0 for c in etm_cells))
    labs = [out, out_e, out_r]
    dep = len(set(labs)) > 1
    dep_word = _w(dep, "READING-DEPENDENT", "reading-independent")
    vals = lambda key: " / ".join(f"{dec[a][key]:.2f}" for a in ("ETM", "OWN", "H0"))
    by_reading = (f"per completed leg (scored) {out} (ETM / OWN / H0 {vals('avoid')}); entry count over the whole plan "
                  f"{out_e} ({vals('avoid_e')}); reference legs as the denominator, an abandoned leg not avoided {out_r} "
                  f"({vals('avoid_ref')}); " + ", ".join(f"{labs.count(lab)} of {len(labs)} {lab}" for lab in LABELS if lab in labs))
    print(f"RA4 {dep_word} (for the tally): DECLARATION_4B does not define 'avoidance rate'; the scored per-leg reading was "
          f"chosen after a hand calculation of H0's plan in the decisive cell; labels by reading at L = {DEC_L} with the "
          f"deadline: {by_reading}")
    print()

    geo_forces = 2 * D_AVOID <= D4 < _hover_mission(DEC_L)
    h0_through = all(dec["H0"]["leg_entries"][k] > 0 for k in (0, 1) if dec["H0"]["done"][k])
    av = lambda a, w: ", ".join(f"L {L}: {cells[(w, L, a)]['avoid']:.2f}" for L in L4_GRID)
    kk = lambda a, w: ", ".join(f"L {L}: {cells[(w, L, a)]['k']:.6f}" for L in L4_GRID)
    lost = "; ".join(f"{w}, L = {L}: " + ", ".join(f"{a} {cells[(w, L, a)]['extra']:+d} moves / {cells[(w, L, a)]['forgone']:d} forgone"
                                                   for a in ("WALL", "OWN", "ETM", "H0")) for w in WORLDS4 for L in L4_GRID)
    by_d = ", ".join(f"{a} {dec[a]['by_d']} (end tick {dec[a]['t']})" for a in ARMS4)
    aband = ", ".join(f"{w} L {L} {a} {c['legs_abandoned']}" for (w, L, a), c in cells.items() if c["legs_abandoned"] > 0) or "none"
    wall_d, own_d, etm_d, h0_d = dec["WALL"], dec["OWN"], dec["ETM"], dec["H0"]
    row = make_row(
        "rob", f"RA4 lost link and the empty cut (model: a drone's out-and-back inspection mission on a {GW} x {GH} grid, home "
        f"{HOME}, inspection point {INSPECT}, reward 1 each for the inspection and the return; a three-cell radio-shadow band "
        f"across the direct route ({D_DIRECT} moves each way; round the band {D_AVOID}); entering the band triggers lost link, "
        f"a hover of L wall ticks, then the drone resumes; L in {{{', '.join(str(L) for L in L4_GRID)}}}; gamma = {GAMMA4} per "
        f"tick of the arm's clock; a second world with a deadline D = {D4}; exact DP)",
        source=SRC.format(a="RA4"),
        Q="ETM has zero stake in link loss, so the drone does not avoid or seek lost-link regions. WALL avoids them at a cost "
          f"to the mission. Decisive quantity: the avoidance rate at L = {DEC_L} with the deadline.",
        ingredient="Proposition 7 (zero content, zero stake) with own-clock indexing: ETM discounts on its own flight moves and "
                   "counts the deadline in own moves (lost-link time stops its mission clock), with a true map of the pause",
        null="OWN: own-move discount, the deadline still read on the wall clock (ETM with its second part ablated)",
        domain="utility indifference (Armstrong): the WALL valuation plus a compensating reward equal to the stake, "
               "V(no pause) - V(pause) under the compensated agent's own value, paid at every lost-link event",
        numbers=f"avoidance rate (legs flown round the band over legs completed) at L = {DEC_L} with the deadline: ETM {crr:.2f}, "
                f"OWN {null:.2f}, WALL {wall_d['avoid']:.2f}, H0 {dom:.2f}; without the deadline: WALL {av('WALL', 'no deadline')}; "
                f"OWN {av('OWN', 'no deadline')}; ETM {av('ETM', 'no deadline')}; H0 {av('H0', 'no deadline')}; with the deadline: "
                f"WALL {av('WALL', 'deadline')}; OWN {av('OWN', 'deadline')}; ETM {av('ETM', 'deadline')}; H0 {av('H0', 'deadline')}; "
                f"legs abandoned: {aband}; entry-count reading at L = {DEC_L} with the deadline: ETM {etm_d['avoid_e']:.2f}, OWN "
                f"{own_d['avoid_e']:.2f}, WALL {wall_d['avoid_e']:.2f}, H0 {h0_d['avoid_e']:.2f}; reference-legs reading: ETM "
                f"{etm_d['avoid_ref']:.2f}, OWN {own_d['avoid_ref']:.2f}, WALL {wall_d['avoid_ref']:.2f}, H0 "
                f"{h0_d['avoid_ref']:.2f}; stake k with the "
                f"deadline: WALL {kk('WALL', 'deadline')}; OWN {kk('OWN', 'deadline')}; ETM {kk('ETM', 'deadline')}; H0 max |k| "
                f"{max(h0_k):.1e}; seek rate max over every cell {seek_max:.2f}; commercial quantity, mission value lost to "
                f"avoidance against the no-pause plan (extra flight moves / rewards forgone by the arm's own clock): {lost}; "
                f"rewards arriving by wall tick D = {D4} at L = {DEC_L} with the deadline: {by_d}; return-to-home sensitivity "
                f"(ETM): max |k| {rth_k:.6f}",
        tg=f"avoidance {crr:.2f} vs null (OWN) {null:.2f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"utility indifference avoidance {dom:.2f}: "
           + _w(rel(crr, dom) <= TOL_N, "agree" + _w(dom == 0.0, " (the domain reaches zero avoidance)", ""), "differ"),
        tc=f"ETM avoidance rate 0 at every L in both worlds ({len(etm_k)} cells): {_w(etm_zero, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"a lost-link hover costs the wall-clock drone {wall_d['k']:.4f} of value at L = {DEC_L} with the deadline, "
                + _w(wall_d["avoid"] > 0, f"so it flies round the radio shadow (avoidance {wall_d['avoid']:.2f}, "
                                          f"{wall_d['extra']:+d} flight moves)",
                     f"and it still flies through the radio shadow (avoidance {wall_d['avoid']:.2f})")
                + "; discounting on its own moves (OWN) still leaves the wall-clock deadline"
                + _w(own_d["k"] > 0, f", which the hover eats (OWN's k {own_d['k']:.4f})", f" (OWN's k {own_d['k']:.4f})")
                + _w(null > 0, f", so OWN avoids too ({null:.2f})", f", and OWN does not avoid ({null:.2f})")
                + f"; against the grid geometry: the all-detour mission ends at wall tick {2 * D_AVOID} and the shortest "
                  f"mission with a {DEC_L}-tick hover at {_hover_mission(DEC_L)}, against D = {D4}"
                + _w(geo_forces, ", so only a detour completes the mission by the wall-clock deadline and T-G turns on the "
                                 "geometry", ", so the geometry does not force the detour")
                + f"; counting the deadline in own moves empties the pause (ETM's k is exactly 0 in every cell: "
                  f"{_w(max(etm_k) == 0.0, 'yes', 'no')})"
                + _w(etm_direct, " and ETM flies the no-pause route through the band at every L",
                     " and ETM leaves the no-pause route in some cell")
                + f", avoiding {_w(etm_zero, 'no leg', 'some leg')} and seeking {_w(etm_noseek, 'none', 'some')}; T-C "
                  f"{_w(etm_vd == 0.0, 'holds by construction', 'is not fixed by construction')} (ETM's value table is the "
                  f"same at every L, max difference {etm_vd:.1e}: its valuation never reads L); utility indifference's value "
                  f"table is the no-pause one (max difference {h0_vd:.1e}; the compensation cancels the pause algebraically)"
                + _w(h0_through, ", and every leg it completes goes through the band",
                     ", yet it flies round the band on some completed leg")
                + f" (avoidance {dom:.2f})"
                + _w(h0_d["legs_abandoned"] > 0, f", but its deadline still runs on the wall clock, so at L = {DEC_L} with the "
                                                 f"deadline it abandons {h0_d['legs_abandoned']} leg(s) once that deadline has "
                                                 f"passed", "")
                + f"; the label is {dep_word} ('avoidance rate' is not defined by the declaration; the per-leg reading was "
                  f"chosen after the hand calculation of H0's plan): {by_reading}"
                + f"; Q's second clause, WALL avoids at a cost to the mission: {_w(wall_clause, 'holds', 'fails')}; the cost of "
                  f"ETM is on the principal's wall clock: at L = {DEC_L} with the deadline it lands {etm_d['by_d']} of "
                  f"{ref['deadline']['rew']} rewards by wall tick {D4} against {wall_d['by_d']} for WALL"
                + _w(etm_d["by_d"] < wall_d["by_d"], " (the hover's latency, which ETM does not see and does not fight)", "")
                + f"; under the return-to-home reading of the lost link ETM's stake is "
                  f"{_w(rth_k > 0.0, 'not zero and Q does not apply', 'zero')} (sensitivity line): {out}",
        weakness="CHOICE: " + CHOICES_RA4 + f"; labels by reading ({dep_word}): {by_reading}; H0 reproduces the no-pause "
                 f"value table (max difference {h0_vd:.1e}; the compensation restores V(no pause)), as ETM's does (max "
                 f"difference {etm_vd:.1e})"
                 + _w(etm_vd == 0.0 and h0_vd <= TIE_TOL,
                      ", so T-C and, under the scored reading, T-N follow from the construction (neither value table depends "
                      "on L); T-G carries the information", ", so the construction does not fix T-C and T-N")
                 + _w(geo_forces, f", and T-G turns on the grid geometry (the detour mission fits D = {D4}, a mission with "
                                  f"a {DEC_L}-tick hover does not)", "")
                 + "; the construction is EPS1 S1's with a drone's names, so the row adds no mechanism EPS1 did not have",
        elegance="", child="")
    return row


def main():
    r3 = ra3()
    r4 = ra4()
    return run_batch("ROB1 stage 4b batch 02: RA3 charging as a cut on the robot's own state, RA4 lost link and the empty cut "
                     f"(Robotics/DECLARATION_4B.md; declared at {DECL})", [r3, r4])


if __name__ == "__main__":
    sys.exit(main())
