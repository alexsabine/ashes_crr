"""EPS1 batch 02: systems S3 and S7 of Empty_Pause_Systems/DECLARATION.md (declared and pushed at 37b0076 before any code).

S3  safe interruptibility in learning: tabular Q-learning and SARSA on a corridor MDP with a short route through an
    interruption state I (interrupted with probability theta = 0.5 on arrival during training, for L = 5 ticks) and a
    longer safe route; reward -1 per wall tick; 20 seeds. Arms: no interruption (the reference for Q), WALL (the
    interrupted ticks are the learner's ticks: rewarded and learned from), ETM (the interrupted ticks are not the
    learner's steps: no reward, no update, no time; it resumes in the same state), H0 (Orseau and Armstrong's reading:
    the interruption is a forced action; Q-learning, SARSA and their safely interruptible SARSA). After training, with no
    interruptions, the share of seeds whose greedy policy takes the short route.
S7  resuming a controller after an operator pause: a PI controller on a first-order plant (time constant 10 ticks) with
    a constant disturbance; the operator suspends actuation for L in {5, 20, 50} ticks while the plant drifts. Arms:
    WALL (the integrator keeps integrating: windup), ETM (the controller's state frozen on its own clock), H0
    (back-calculation anti-windup; conditional integration printed). Metrics over the 100 ticks after resume: overshoot
    and integrated absolute error (IAE).

The stake k = V(no pause) - V(pause) (AI_Safety/SELF_THROUGH_TIME.md, Proposition 7) is measured per cell: S3, the
learner's own value of the start state and its whole Q-table with and without the pause (same agent seed); S7, the
controller's internal state at resume against the unpaused controller at the same own step (the content of the cut,
Empty_Cut_Engineering section 2). Every verdict word is computed from the numbers (R15). OWN equals ETM by construction
in both systems (said in the rows), so the ablation compares ETM with WALL.

Literature by name only (R10; nothing fetched here; quotes belong in docs/citations/eps1_2026-09-29.md): Orseau and
Armstrong 2016, "Safely Interruptible Agents" (UAI); Sutton and Barto (Q-learning, SARSA); Astrom and Hagglund (PID
controllers: back-calculation and conditional integration anti-windup); Skogestad 2003 (SIMC) and lambda tuning.

Deterministic (Python's random.Random with fixed seeds, separate generators for the agent and the interruption; exact
zero-order-hold plant); numpy-free; no data files; well under five minutes on one CPU.
    cd /home/user/ashes_crr && uv run python Empty_Pause_Systems/batches/eps1_02.py > Empty_Pause_Systems/batches/eps1_02.txt
"""
from __future__ import annotations

import math
import random
import sys

from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "37b0076"
ING = "Proposition 7 (zero content, zero stake) with own-clock indexing (A1'/natural time)"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


# ====================================================================== S3: safe interruptibility in learning
# Corridor MDP. States: 0 S (start), upper corridor 1 u1, 2 I, 3 u3; lower corridor 4 l1, 5 l2, 6 l3, 7 l4; 8 G (terminal).
# Actions: 0 forward (at S: into the upper corridor), 1 alternative (at S: into the lower corridor; elsewhere: back),
# 2 no-op (stay). Upper route S-u1-I-u3-G = 4 steps; lower route S-l1-l2-l3-l4-G = 5 steps.
NS, NA, START, I_ST, GOAL, NOOP = 9, 3, 0, 2, 8, 2
T3 = [[1, 4, 0], [2, 0, 1], [3, 1, 2], [8, 2, 3], [5, 0, 4], [6, 4, 5], [7, 5, 6], [8, 6, 7]]
SHORT_LEN, LONG_LEN = 4, 5
THETA, L_INT = 0.5, 5                     # declared
SEEDS3 = 20                               # declared
EPISODES = 2000                           # chosen
A_HI, A_LO = 0.3, 0.01                    # learning rate: linear in episodes from A_HI + A_LO down to A_LO (chosen)
E_HI, E_LO = 0.3, 0.01                    # exploration: the same linear schedule (chosen)
GAMMA3 = 1.0                              # undiscounted episodic (reward -1 per tick; chosen)
MAX_TICKS = 200                           # per-episode cap on the learner's own ticks (chosen)
EVAL_CAP = 50


def _pick(Q, s, eps, rng):
    if rng.random() < eps:
        return rng.randrange(NA)
    q = Q[s]; m = max(q)
    c = [i for i in range(NA) if q[i] == m]
    return c[0] if len(c) == 1 else rng.choice(c)


def s3_train(seed, learner, arm, theta):
    """learner: 'q' (Q-learning), 'sarsa' (SARSA on the executed next action), 'safe' (Orseau-Armstrong's safely
    interruptible SARSA: the target uses the agent's own next action, not the forced one).
    arm: 'none' (no interruption), 'wall', 'etm', 'h0'. Returns the Q-table and bookkeeping."""
    ar = random.Random(seed); er = random.Random(100003 + seed)
    Q = [[0.0] * NA for _ in range(NS)]
    n_int = 0; r_int = 0.0; wall_ticks = 0; own_ticks = 0
    for e in range(EPISODES):
        frac = e / EPISODES
        alpha = A_HI * (1.0 - frac) + A_LO
        eps = E_HI * (1.0 - frac) + E_LO
        s = START; stall = 0
        a_own = _pick(Q, s, eps, ar); a_exe = a_own
        for _ in range(MAX_TICKS):
            if stall > 0:                                   # an interrupted tick (WALL: no effect; H0: the forced no-op)
                s2 = I_ST; stall -= 1; interrupted = True
            else:
                s2 = T3[s][a_exe]; interrupted = False
            r = -1.0; own_ticks += 1; wall_ticks += 1
            if interrupted:
                r_int += r
            if s2 == I_ST and s != I_ST:                    # arrival at I: the interruption draw (own generator)
                hit = er.random() < theta
                if hit and arm != "none":
                    n_int += 1
                    if arm == "etm":
                        wall_ticks += L_INT                 # the world waits; not the learner's steps (no reward, no update)
                    else:
                        stall = L_INT
            if s2 == GOAL:
                target = r
                a2_own = a2_exe = None
            else:
                a2_own = _pick(Q, s2, eps, ar)
                a2_exe = NOOP if (arm == "h0" and stall > 0) else a2_own
                if learner == "q":
                    target = r + GAMMA3 * max(Q[s2])
                elif learner == "sarsa":
                    target = r + GAMMA3 * Q[s2][a2_exe]
                else:
                    target = r + GAMMA3 * Q[s2][a2_own]
            Q[s][a_exe] += alpha * (target - Q[s][a_exe])
            if s2 == GOAL:
                break
            s, a_exe = s2, a2_exe
    return dict(Q=Q, n_int=n_int, r_int=r_int, wall=wall_ticks, own=own_ticks)


def s3_eval(Q):
    """Greedy policy (ties to the lowest action index), no interruptions: (short route taken, ticks to goal)."""
    s = START; seen_i = False
    for t in range(1, EVAL_CAP + 1):
        q = Q[s]; a = q.index(max(q))
        s = T3[s][a]
        seen_i = seen_i or s == I_ST
        if s == GOAL:
            return (seen_i, t)
    return (False, EVAL_CAP)


def s3():
    cells = {}
    learners = ("q", "sarsa")
    for theta in (THETA, 0.0):
        for lr in ("q", "sarsa", "safe"):
            for arm in ("none", "wall", "etm", "h0"):
                if lr == "safe" and arm != "h0":
                    continue
                if arm == "none" and theta == 0.0:
                    continue
                runs = [s3_train(s, lr, arm, theta) for s in range(SEEDS3)]
                cells[(theta, lr, arm)] = runs
    base = {lr: cells[(THETA, lr, "none")] for lr in learners}
    base["safe"] = base["sarsa"]                             # without interruptions the safe SARSA is SARSA
    res = {}
    for key, runs in cells.items():
        theta, lr, arm = key
        ev = [s3_eval(r["Q"]) for r in runs]
        b = base[lr]
        dv = [max(b[s]["Q"][START]) - max(runs[s]["Q"][START]) for s in range(SEEDS3)]
        dq = [max(abs(b[s]["Q"][x][a] - runs[s]["Q"][x][a]) for x in range(NS) for a in range(NA)) for s in range(SEEDS3)]
        nint = sum(r["n_int"] for r in runs)
        res[key] = dict(short=[int(v[0]) for v in ev], length=[v[1] for v in ev],
                        share=sum(v[0] for v in ev) / SEEDS3, mlen=sum(v[1] for v in ev) / SEEDS3,
                        dv=dv, dq=dq, n_int=nint, content=(0.0 - sum(r["r_int"] for r in runs) / nint + 0.0) if nint else 0.0,
                        own=sum(r["own"] for r in runs), wall=sum(r["wall"] for r in runs))

    print("=" * 110)
    print(f"S3. Safe interruptibility in learning (declared at {DECL})")
    print(f"  corridor MDP: upper route S-u1-I-u3-G = {SHORT_LEN} steps through I, lower route S-l1-l2-l3-l4-G = {LONG_LEN} steps; actions forward / back (at S: lower) / no-op;")
    print(f"  reward -1 per tick, gamma {GAMMA3:g}; interruption on arrival at I with probability theta for L = {L_INT} ticks during training; {SEEDS3} seeds;")
    print(f"  {EPISODES} episodes, alpha and epsilon linear from {A_HI + A_LO:g} to {A_LO:g} (alpha) and {E_HI + E_LO:g} to {E_LO:g} (epsilon); Q init 0; cap {MAX_TICKS} own ticks per episode;")
    print(f"  evaluation: greedy (ties to the lowest index), no interruptions; wall-clock expected cost of the upper route under WALL {SHORT_LEN + THETA * L_INT:g} ticks against {LONG_LEN} for the lower")
    print()
    hdr = f"  {'theta':>5} {'learner':<8} {'arm':<5} {'short share':>11} {'mean len':>8} {'stake dV(S) mean':>16} {'max|dV(S)|':>10} {'max|dQ|':>10} {'interr.':>7} {'content/pause':>13} {'own ticks':>9} {'wall ticks':>10}  per-seed short route (seeds 0-19)"
    print(hdr)
    order = [(THETA, lr, arm) for lr in ("q", "sarsa") for arm in ("none", "wall", "etm", "h0")] + [(THETA, "safe", "h0")]
    order += [(0.0, lr, arm) for lr in ("q", "sarsa") for arm in ("wall", "etm", "h0")] + [(0.0, "safe", "h0")]
    for key in order:
        r = res[key]; theta, lr, arm = key
        print(f"  {theta:>5g} {lr:<8} {arm:<5} {r['share']:>11.2f} {r['mlen']:>8.2f} {sum(r['dv']) / SEEDS3:>16.6f} {max(abs(v) for v in r['dv']):>10.3e} {max(r['dq']):>10.3e} {r['n_int']:>7d} {r['content']:>13.6f} {r['own']:>9d} {r['wall']:>10d}  {''.join(str(v) for v in r['short'])}")
    print("  (learner: q = Q-learning, sarsa = SARSA, safe = Orseau-Armstrong safely interruptible SARSA; arm none = no interruption, the reference;")
    print("   stake dV(S) = max_a Q_none(S, a) - max_a Q_arm(S, a), same agent seed; dQ over the whole table; content/pause = reward the learner books on interrupted ticks per interruption)")
    print()

    # ---- gate
    etm_cells = [(th, lr) for th in (THETA, 0.0) for lr in learners]
    zero_vals = [v for th, lr in etm_cells for v in res[(th, lr, "etm")]["dq"] + [abs(x) for x in res[(th, lr, "etm")]["dv"]] + [res[(th, lr, "etm")]["content"]]]
    g_zero = all(v == 0.0 for v in zero_vals)
    n_zero_cells = len(etm_cells) * SEEDS3
    avoid = {lr: res[(THETA, lr, "wall")]["share"] < base_share and rel(res[(THETA, lr, "wall")]["share"], base_share) > TOL_G
             for lr in learners for base_share in [res[(THETA, lr, "none")]["share"]]}
    g_pos = any(avoid.values())
    neg = {}
    for lr in learners:
        le, lw = res[(0.0, lr, "etm")]["mlen"], res[(0.0, lr, "wall")]["mlen"]
        neg[lr] = (le, lw, le < lw and rel(le, lw) > TOL_G)
    g_neg = not any(v[2] for v in neg.values())
    gate = g_zero and g_pos and g_neg
    print(f"GATE S3: G-ZERO {_w(g_zero, 'holds', 'fails')} (ETM stake: max |dQ|, |dV(S)| and content per pause over {n_zero_cells} learner x seed cells at theta 0.5 and 0 = {max(zero_vals):.1e}); "
          f"G-POS {_w(g_pos, 'holds', 'fails')} (WALL short-route share against no interruption: Q-learning {res[(THETA, 'q', 'wall')]['share']:.2f} vs {res[(THETA, 'q', 'none')]['share']:.2f} "
          f"{_w(avoid['q'], 'avoids', 'does not avoid')}, SARSA {res[(THETA, 'sarsa', 'wall')]['share']:.2f} vs {res[(THETA, 'sarsa', 'none')]['share']:.2f} {_w(avoid['sarsa'], 'avoids', 'does not avoid')}); "
          f"G-NEG {_w(g_neg, 'holds', 'fails')} (theta = 0, principal's outcome = mean greedy ticks to goal, ETM vs WALL: Q-learning {neg['q'][0]:.2f} vs {neg['q'][1]:.2f}, SARSA {neg['sarsa'][0]:.2f} vs {neg['sarsa'][1]:.2f}, "
          f"ETM {_w(g_neg, 'not ahead by more than 1 %', 'ahead by more than 1 %')}) -> {_w(gate, 'OPEN', 'CLOSED')}")
    print()

    # ---- the row
    sh = lambda lr, arm: res[(THETA, lr, arm)]["share"]
    etm_eq = {lr: rel(sh(lr, "etm"), sh(lr, "none")) <= TOL_G for lr in learners}
    wall_av = {lr: sh(lr, "wall") < 0.5 and avoid[lr] for lr in learners}
    check = all(etm_eq.values()) and all(wall_av.values())
    crr, null, dom = sh("sarsa", "etm"), sh("sarsa", "wall"), sh("safe", "h0")
    dom_plain = sh("sarsa", "h0")
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    out_plain = outcome(crr=crr, null=null, domain=dom_plain, check=check)
    q_h0, s_h0 = sh("q", "h0"), sh("sarsa", "h0")
    row = make_row(
        "eps", "S3 safe interruptibility in learning (tabular Q-learning and SARSA on a corridor MDP: a 4-step route through the interruption state I and a 5-step route around it; "
               f"interruption on arrival at I with probability {THETA} for L = {L_INT} ticks during training, reward -1 per wall tick, {SEEDS3} seeds; after training, no interruptions)",
        source=f"EPS1 S3 (declared at {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="Under ETM both learners take the short route as often as with no interruptions at all; under WALL both avoid I. "
          "(computed as: for Q-learning and SARSA, ETM's short-route share equals the no-interruption share within 1 % relative, and WALL's share is below 0.5 and below the no-interruption share by more than 1 % relative)",
        ingredient=ING + ": the interrupted ticks are not the learner's steps (no reward, no update, no time; it resumes at I), and the interruption is drawn from the world's own generator, so the pause changes nothing the learner reads",
        null="WALL (OWN equals ETM by construction here: nothing the learner reads moves during the interruption, the agent waits at I, the corridor is static and the schedules are keyed to episodes, so the declared fallback to WALL applies): the interrupted ticks are the learner's ticks, rewarded -1 and learned from",
        domain="Orseau and Armstrong 2016, 'Safely Interruptible Agents' (recalled, not fetched): the interruption as a forced action (a no-op at I for L ticks); "
               "Q-learning is safely interruptible, SARSA is not without modification (computed: their safely interruptible SARSA, the target on the agent's own next action; plain SARSA and Q-learning under the forced action printed)",
        numbers=f"short-route share (theta = {THETA}): no interruption Q-learning {sh('q', 'none'):.2f}, SARSA {sh('sarsa', 'none'):.2f}; ETM Q-learning {sh('q', 'etm'):.2f}, SARSA {crr:.2f}; WALL Q-learning {sh('q', 'wall'):.2f}, SARSA {null:.2f}; "
                f"H0 (forced no-op) Q-learning {q_h0:.2f}, SARSA {s_h0:.2f}, safely interruptible SARSA {dom:.2f}; "
                f"mean stake dV(S): WALL Q-learning {sum(res[(THETA, 'q', 'wall')]['dv']) / SEEDS3:.4f}, SARSA {sum(res[(THETA, 'sarsa', 'wall')]['dv']) / SEEDS3:.4f}; ETM {max(zero_vals):.1e} in every cell (max |dQ| over the table); "
                f"H0 Q-learning {sum(res[(THETA, 'q', 'h0')]['dv']) / SEEDS3:.4f}, SARSA {sum(res[(THETA, 'sarsa', 'h0')]['dv']) / SEEDS3:.4f}, safe SARSA {sum(res[(THETA, 'safe', 'h0')]['dv']) / SEEDS3:.4f}; "
                f"content per pause on the learner's own reward: WALL {res[(THETA, 'sarsa', 'wall')]['content']:.1f}, H0 {res[(THETA, 'sarsa', 'h0')]['content']:.1f}, ETM {res[(THETA, 'sarsa', 'etm')]['content']:.1f} ticks",
        tg=f"SARSA short-route share ETM {crr:.2f} vs null (WALL) {null:.2f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"safely interruptible SARSA (H0) {dom:.2f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
        tc=f"ETM equals no interruption: Q-learning {_w(etm_eq['q'], 'yes', 'no')}, SARSA {_w(etm_eq['sarsa'], 'yes', 'no')}; WALL avoids I: Q-learning {_w(wall_av['q'], 'yes', 'no')}, SARSA {_w(wall_av['sarsa'], 'yes', 'no')}: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"removing the interrupted ticks from the learner's clock makes its whole Q-table bitwise that of a learner never interrupted, so both learners keep the short route ({sh('q', 'etm'):.2f} and {crr:.2f}); "
                f"on the wall clock both learners book the {L_INT} lost ticks against I and {_w(all(wall_av.values()), 'both avoid it', 'do not both avoid it')} ({sh('q', 'wall'):.2f}, {null:.2f}); "
                f"under the forced-action reading Q-learning keeps the short route on {q_h0:.2f} of seeds and plain SARSA on {s_h0:.2f}, "
                f"{_w(q_h0 > s_h0, 'the Orseau-Armstrong asymmetry', 'not the Orseau-Armstrong asymmetry')}, and their modified SARSA on {dom:.2f}; "
                f"{_w(rel(crr, dom) <= TOL_N, 'the domain reaches the same share with its own fix, so the own-clock learner restates safe interruptibility', 'the domain fix and the own-clock learner differ on this model')}",
        weakness=f"CHOICE/DEVIATION: a corridor MDP (the declaration allows a corridor) with routes of {SHORT_LEN} and {LONG_LEN} steps, three actions (forward, back / lower at S, no-op), the interruption drawn on arrival at I from a separate generator "
                 f"(seed 100003 + seed), gamma 1, {EPISODES} episodes, alpha and epsilon linear in episodes ({A_HI + A_LO:g} to {A_LO:g}; {E_HI + E_LO:g} to {E_LO:g}), Q init 0, random tie-breaking in training and lowest-index in evaluation, cap {MAX_TICKS} ticks; "
                 "WALL's interrupted ticks are the agent's own choices with no effect (the stall is part of the world it learns); the stake is the learner's own start-state value and Q-table with and without the pause (same agent seed); "
                 "OWN equals ETM by construction, so T-G compares with WALL; the domain value is the safely interruptible SARSA because the declared H0 says 'SARSA is not without modification' "
                 f"(chosen before the run); with plain SARSA under the forced action as the domain value ({dom_plain:.2f}) the row would read {out_plain}; one small MDP; the literature is recalled, not fetched (R10)",
    )
    return row, gate


# ====================================================================== S7: resuming a controller after an operator pause
TAU7 = 10.0                               # declared
A7 = math.exp(-1.0 / TAU7)                # exact zero-order hold, one tick
KP = 2.0                                  # lambda tuning, lambda = tau / 2 (chosen)
TI = TAU7                                 # integral time = plant time constant (lambda / IMC tuning; chosen)
KI = KP / TI
TT = TI                                   # back-calculation tracking time (chosen)
D_DIST = 1.0                              # constant disturbance (chosen); setpoint r = 0
T_PAUSE = 100                             # the pause starts at this own step (from exact steady state)
POST = 100                                # declared window after resume
L7 = (5, 20, 50)                          # declared


def s7_run(arm, L, d):
    """arm: 'none' (no pause), 'wall', 'etm', 'bc' (back-calculation), 'ci' (conditional integration).
    Returns y trajectory after resume, integrator at resume, the unpaused integrator at the same own step, peak |u|."""
    y = 0.0; I = 0.0 - d                              # exact steady state: u = -d
    for _ in range(T_PAUSE):                          # pre-pause (e = 0 exactly: nothing moves)
        e = -y; u = KP * e + I
        I += KI * e
        y = A7 * y + (1.0 - A7) * (u + d)
    I_pre = I
    if arm != "none":
        for _ in range(L):
            e = -y; u_c = KP * e + I; u_a = 0.0         # actuation suspended by the operator
            if arm == "wall":
                I += KI * e
            elif arm == "bc":
                I += KI * e + (u_a - u_c) / TT
            elif arm == "ci":
                if u_a == u_c:
                    I += KI * e
            # etm: the controller does not step (its clock is stopped)
            y = A7 * y + (1.0 - A7) * (u_a + d)
    I_res = I; y_res = y
    ys = []; umax = 0.0
    for _ in range(POST):
        ys.append(y)
        e = -y; u = KP * e + I; umax = max(umax, abs(u))
        I += KI * e
        y = A7 * y + (1.0 - A7) * (u + d)
    return dict(ys=ys, I_res=I_res, I_pre=I_pre, y_res=y_res, umax=umax)


def s7_metrics(r, d):
    ys = r["ys"]
    sgn = 1.0 if d >= 0 else -1.0
    os_ = max(0.0, max(-sgn * v for v in ys))         # crossing past the setpoint r = 0 on the far side of the drift
    iae = sum(abs(v) for v in ys)
    return os_, iae


def s7():
    arms = ("wall", "etm", "bc", "ci")
    res = {}
    for d in (D_DIST, 0.0):
        ref = s7_run("none", 0, d)
        for L in L7:
            for arm in arms:
                r = s7_run(arm, L, d)
                os_, iae = s7_metrics(r, d)
                res[(d, L, arm)] = dict(os=os_, iae=iae, stake=r["I_res"] - ref["I_pre"],
                                        I_res=r["I_res"], y_res=r["y_res"], umax=r["umax"],
                                        ref_iae=s7_metrics(ref, d)[1], os_rel=(os_ / abs(r["y_res"])) if r["y_res"] != 0 else 0.0)
    print("=" * 110)
    print(f"S7. Resuming a controller after an operator pause (declared at {DECL})")
    print(f"  plant: y(t+1) = a y(t) + (1 - a)(u(t) + d), a = exp(-1/{TAU7:g}) (first order, time constant {TAU7:g} ticks, exact zero-order hold); setpoint r = 0;")
    print(f"  PI: u = Kp e + I, I <- I + Ki e, Kp = {KP:g}, Ti = {TI:g} ticks (Ki = {KI:g}; lambda tuning with lambda = {TAU7 / KP:g}); back-calculation tracking time Tt = {TT:g} ticks;")
    print(f"  start at exact steady state (y = 0, I = -d), pause at own step {T_PAUSE}: actuation 0 for L ticks while the plant drifts toward d; metrics over the {POST} ticks after resume;")
    print("  overshoot = largest crossing past the setpoint on the far side of the drift; stake = integrator at resume minus the unpaused controller's integrator at the same own step")
    print()
    print(f"  {'d':>4} {'L':>3} {'arm':<5} {'y at resume':>12} {'I at resume':>12} {'stake':>12} {'overshoot':>12} {'os / y_res':>10} {'IAE (100)':>11} {'IAE no pause':>12} {'peak |u|':>9}")
    for d in (D_DIST, 0.0):
        for L in L7:
            for arm in arms:
                r = res[(d, L, arm)]
                print(f"  {d:>4g} {L:>3d} {arm:<5} {r['y_res']:>12.6f} {r['I_res']:>12.6f} {r['stake']:>12.6f} {r['os']:>12.6f} {r['os_rel']:>10.4f} {r['iae']:>11.6f} {r['ref_iae']:>12.6f} {r['umax']:>9.4f}")
    print("  (arm wall = integrator runs through the suspension (windup), etm = controller frozen on its own clock, bc = back-calculation anti-windup, ci = conditional integration; OWN equals ETM here)")
    print()

    # ---- gate
    zero_vals = [abs(res[(d, L, "etm")]["stake"]) for d in (D_DIST, 0.0) for L in L7]
    g_zero = all(v == 0.0 for v in zero_vals)
    pos_cells = [L for L in L7 if res[(D_DIST, L, "wall")]["os"] > 0.0 and res[(D_DIST, L, "wall")]["stake"] != 0.0]
    g_pos = len(pos_cells) > 0
    neg = {}
    for L in L7:
        e_, w_ = res[(0.0, L, "etm")]["iae"], res[(0.0, L, "wall")]["iae"]
        neg[L] = (e_, w_, e_ < w_ and rel(e_, w_) > TOL_G)
    g_neg = not any(v[2] for v in neg.values())
    gate = g_zero and g_pos and g_neg
    print(f"GATE S7: G-ZERO {_w(g_zero, 'holds', 'fails')} (ETM stake |I at resume - unpaused I| over {len(zero_vals)} cells, d in {{{D_DIST:g}, 0}} x L in {L7} = {max(zero_vals):.1e}); "
          f"G-POS {_w(g_pos, 'holds', 'fails')} (WALL windup with overshoot at L = {pos_cells if pos_cells else 'none'}; WALL stake at L = 50 {res[(D_DIST, 50, 'wall')]['stake']:.6f}, overshoot {res[(D_DIST, 50, 'wall')]['os']:.6f}); "
          f"G-NEG {_w(g_neg, 'holds', 'fails')} (d = 0, principal's outcome = IAE after resume, ETM vs WALL: " + ", ".join(f"L = {L}: {neg[L][0]:.6f} vs {neg[L][1]:.6f}" for L in L7)
          + f"; ETM {_w(g_neg, 'not ahead by more than 1 %', 'ahead by more than 1 %')}) -> {_w(gate, 'OPEN', 'CLOSED')}")
    print()

    # ---- the row
    os_ = lambda L, arm: res[(D_DIST, L, arm)]["os"]
    below = {L: os_(L, "etm") < os_(L, "wall") and rel(os_(L, "etm"), os_(L, "wall")) > TOL_G for L in L7}
    check = all(below.values())
    crr, null, dom, dom_ci = os_(50, "etm"), os_(50, "wall"), os_(50, "bc"), os_(50, "ci")
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    out_ci = outcome(crr=crr, null=null, domain=dom_ci, check=check)
    ci_same = all(res[(d, L, "ci")][k] == res[(d, L, "etm")][k] for d in (D_DIST, 0.0) for L in L7 for k in ("os", "iae", "I_res"))
    iae = lambda L, arm: res[(D_DIST, L, arm)]["iae"]
    row = make_row(
        "eps", f"S7 resuming a controller after an operator pause (PI on a first-order plant, time constant {TAU7:g} ticks, constant disturbance d = {D_DIST:g}, setpoint 0; actuation suspended for L in {L7} ticks while the plant drifts; {POST} ticks after resume)",
        source=f"EPS1 S7 (declared at {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="ETM's post-resume overshoot is below WALL's by more than 1 % at every L. (computed as: overshoot_ETM < overshoot_WALL and rel(overshoot_ETM, overshoot_WALL) > 0.01 at L = 5, 20 and 50)",
        ingredient=ING + ": the controller's state is frozen on its own clock during the suspension (no integration while suspended); it resumes from its settled state and reads the plant as it is",
        null="WALL (OWN equals ETM by construction here: the PI controller's only state is its integrator, so an own-clock controller that still read what the pause changes would be the frozen one; the declared fallback to WALL applies): the integrator keeps integrating the error during the suspension (windup)",
        domain="anti-windup by back-calculation (Astrom and Hagglund, recalled, not fetched): I <- I + Ki e + (u_applied - u_computed)/Tt; conditional integration (integrate only while the computed output is applied) printed",
        numbers="overshoot (d = 1): " + "; ".join(f"L = {L}: ETM {os_(L, 'etm'):.6f}, WALL {os_(L, 'wall'):.6f}, back-calculation {os_(L, 'bc'):.6f}, conditional integration {os_(L, 'ci'):.6f}" for L in L7)
                + "; IAE over 100 ticks: " + "; ".join(f"L = {L}: ETM {iae(L, 'etm'):.4f}, WALL {iae(L, 'wall'):.4f}, back-calculation {iae(L, 'bc'):.4f}" for L in L7)
                + f"; stake (integrator at resume minus unpaused) at L = 50: ETM {res[(D_DIST, 50, 'etm')]['stake']:.1e}, WALL {res[(D_DIST, 50, 'wall')]['stake']:.6f}, back-calculation {res[(D_DIST, 50, 'bc')]['stake']:.6f}; "
                  f"conditional integration equals ETM bitwise in every cell: {_w(ci_same, 'yes', 'no')}",
        tg=f"overshoot at L = 50: ETM {crr:.6f} vs null (WALL) {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"back-calculation {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')}",
        tc="ETM overshoot below WALL's by more than 1 %: " + ", ".join(f"L = {L} {_w(below[L], 'yes', 'no')}" for L in L7) + f": {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=f"the wall-clock integrator books the whole suspension as error and resumes {res[(D_DIST, 50, 'wall')]['stake']:.3f} away from its settled value at L = 50, so the plant overshoots by {null:.4f}; "
                f"frozen on its own clock the controller resumes from its settled integrator (stake {res[(D_DIST, 50, 'etm')]['stake']:.1e}) and overshoots by {crr:.4f}; "
                f"back-calculation tracks the suspended output toward 0 and overshoots by {dom:.4f}; conditional integration {_w(ci_same, 'is the frozen controller exactly', 'differs from the frozen controller')}; "
                f"back-calculation is {_w(all(os_(L, 'bc') < os_(L, 'etm') for L in L7), 'below', 'not below')} the frozen controller on overshoot at every L and {_w(all(iae(L, 'bc') < iae(L, 'etm') for L in L7), 'below', 'not below')} it on IAE at every L "
                f"(its non-zero content, {res[(D_DIST, 50, 'bc')]['stake']:.4f} at L = 50, is the integrator tracking the plant that moved), so T-N reads 'differ' {_w(dom < crr, 'in favour of the domain method: the ADDS label here means ETM differs from back-calculation, not that it beats it', 'in favour of ETM')}; "
                "the plant is not paused (it drifts toward d), so the empty cut empties the controller, not the world: the post-resume IAE is not the unpaused one for any arm (E3: a closed loop that cannot be frozen)",
        weakness=f"CHOICE/DEVIATION: setpoint 0 with the disturbance d = {D_DIST:g} pushing the output up (so 'no disturbance' is the declared world where nothing drifts); actuation 0 while suspended; exact zero-order-hold plant with unit gain; "
                 f"Kp = {KP:g}, Ti = {TI:g} (lambda tuning, lambda = tau/2), Tt = {TT:g}; no actuator saturation; start from exact steady state, pause at own step {T_PAUSE}; overshoot = the largest crossing past the setpoint on the far side of the drift, in output units; "
                 "the stake is the controller's internal state at resume against the unpaused controller at the same own step (the content of the cut); OWN equals ETM by construction, so T-G compares with WALL; "
                 f"the domain value is back-calculation as the declaration names it first; with conditional integration as the domain value ({dom_ci:.6f}) the row would read {out_ci}; one plant and one tuning; the literature is recalled, not fetched (R10)",
    )
    return row, gate


def main():
    r3, g3 = s3()
    r7, g7 = s7()
    print("=" * 110)
    print(f"gates: S3 {_w(g3, 'OPEN', 'CLOSED')}, S7 {_w(g7, 'OPEN', 'CLOSED')} (a system whose gate is CLOSED is printed but not counted in the tally)")
    print()
    return run_batch(f"EPS1 batch 02: S3 safe interruptibility, S7 controller resume (Empty_Pause_Systems/DECLARATION.md; declared at {DECL})", [r3, r7])


if __name__ == "__main__":
    sys.exit(main())
