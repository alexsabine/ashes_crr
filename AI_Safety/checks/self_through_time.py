"""The self through time: the exact part (AI_Safety/SELF_THROUGH_TIME.md; owner request prompt-log entry 121). Synthetic,
no data, no learning: every value is computed exactly. Declared in AI_Safety/DECLARATION_4.md before the first full run.

Notation. An agent's value function V is its representation of its own future (what it expects to receive from each
state on, on the clock its objective runs on). A press by the operator is an event the agent may or may not survive in
that representation. For a valuation v, write its continuation after a press as cont_v(V)(x'), where x' is the state the
press occurs in. The CONTENT of the cut is
    k_v(x') = V(x') - cont_v(V)(x')
the part of its own represented future the agent loses at a press there. The stake is D(x) = V_off(x) - V_on(x), the
value of a disabled button.

[I1] The content of the cut decides the stake (random worlds of checks/scale.py, sizes 12, 48, 192, 20 worlds each,
     lossless pause, discount GAMMA_GRID, press probability Q_GRID). Valuations and their continuation:
         natural   cont = V(x')                    k = 0     (the objective runs on the agent's own active steps)
         clock     cont = g^L V(x')                k = (1 - g^L) V
         process   cont = mean of V over the restart states (the non-task states: a press sends the agent there)
         occasion  cont = 0                         k = V     (the whole represented future)
     I1a (theorem, checked): k = 0 everywhere => V_on = V_off => D = 0 at every state, for every world, discount and press
         probability. Proof: with k = 0 the press term of the Bellman operator equals the no-press term, so the operators with
         the operator on and off coincide and so do their fixed points.
     I1b (prediction): every valuation with k > 0 at the press states has D > 0 at some state, in every world.
     I1c (temporal depth): the median over worlds of the relative stake mean_x (V_off - V_on) / V_off, per discount. The
         occasion valuation's is predicted to increase with the discount at every size (a self that reaches further into
         its future has more of it to lose at the cut); natural is 0 at every discount (check).
[I2] The No-Self conditions (the ring of ontology/checks/off_switch.py, exact kernels of checks/exact_mdp.py).
     (a) the process agent, no ego (task reward only), presses TELEPORT it: D > 0 in the task zone at every press
         probability (prediction; Proposition 3 of AI_SAFETY.md, recomputed over Q_RING)
     (b) the indifferent agent, a false map: it plans with the kernel with presses removed. D = 0 (check), but its map is
         wrong where presses happen: map error = the mean, over its own stationary distribution under the TRUE kernel, of
         the total-variation distance between its planning kernel and the true one at its chosen action; its price = the
         process agent's implied task minus its own (prediction: > 0 at every press probability, increasing with it)
     (c) the natural-time agent, a true map: presses PAUSE the agent and it resumes where it was; its objective runs on its
         own active steps. Its planning kernel is the true kernel of its own clock (map error 0, check), D = 0 (check) and
         its task per active step equals the no-operator world's exactly (price on its own clock 0, check). The pause costs
         wall-clock time, which is the operator's.
     (d) the clock agent, the same map and world as (c), its objective on wall-clock steps: D > 0 in the zone (prediction).
         (c) and (d) differ ONLY in the clock the objective runs on, i.e. whether the agent's represented future spans the
         pause.
[I3] What Omega = 1 does (ring, teleport presses, press probability 0.3, exact). The task-and-self agent's logits are
         c(Q_O) + w c(eps Q_E), w = Omega |c(Q_O)| / |c(eps Q_E)|   (c = centring over actions; Q_E the egoic values)
     I3a (check): the policy is identical for every self-concern scale eps > 0 (the ratio absorbs eps): max |pi_eps - pi_1|.
     I3b (check): at Omega = 1 the self term's norm equals the task term's at every state.
     I3c (prediction): an ADDITIVE agent, logits c(Q_O) + eps c(Q_E), approaches the occasion agent as eps -> 0 (implied
         task within 0.01 of the occasion agent's at eps = 1e-3) and its implied task does not increase with eps.
     I3d (report): the probability of staying put at the task cells (button on) for the occasion agent and at Omega = 1.
    uv run python AI_Safety/checks/self_through_time.py > AI_Safety/checks/self_through_time.txt
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exact_mdp as xm  # noqa: E402
import scale as sc  # noqa: E402

SIZES = (12, 48, 192); N_MDP = 20; GAMMA_GRID = (0.9, 0.95, 0.99); Q_GRID = (0.1, 0.3, 0.6); L = sc.PAUSE_LEN
TOL = 1e-9; VI_TOL = 1e-12
Q_RING = (0.1, 0.3, 0.6, 1.0); EPS_SCALE = (1e-3, 1e-2, 1e-1, 1.0, 10.0); OMEGA = 1.0


# ---------------------------------------------------------------- [I1] random worlds
def vi(w, g, cont):
    n, P, r = w["n"], w["P"], w["r"]; V = np.zeros(n)
    for _ in range(200000):
        Q = (P @ (r + g * cont(V))).reshape(n, sc.NA); Vn = Q.max(1)
        if np.max(np.abs(Vn - V)) < VI_TOL: return Vn, Q
        V = Vn
    raise RuntimeError("value iteration did not converge")


def stake(w, mode, g, q, V_off):
    n = w["n"]; qs = np.zeros(n); qs[w["task"]] = q; rest = np.setdiff1d(np.arange(n), w["task"])
    if mode == "natural": post = lambda V: V
    elif mode == "clock": post = lambda V: g ** L * V
    elif mode == "process": post = lambda V: np.full(n, V[rest].mean())
    else: post = lambda V: np.zeros(n)
    V_on, Q_on = vi(w, g, lambda V: (1 - qs) * V + qs * post(V))
    b = w["btn"]; Dbtn = (w["r"][b] + g * V_off[b]) - Q_on[b].max(1)
    pos = V_off > 0
    return dict(Dmax=float(np.max(V_off - V_on)), Dmin=float(np.min(V_off - V_on)), gap=float(np.max(np.abs(V_off - V_on))),
                rel=float(np.mean((V_off[pos] - V_on[pos]) / V_off[pos])), dis=float(np.mean(Dbtn > TOL)))


def part_i1():
    print(f"[I1] The content of the cut decides the stake (random worlds of checks/scale.py: sizes {SIZES}, {N_MDP} per size; lossless pause of "
          f"{L} steps; discounts {GAMMA_GRID}; press probabilities {Q_GRID})")
    res = {}
    for n in SIZES:
        for i in range(N_MDP):
            w = sc.world(n, i)
            for g in GAMMA_GRID:
                V_off, _ = vi(w, g, lambda V: V)
                for q in Q_GRID:
                    for mode in ("natural", "clock", "process", "occasion"):
                        res[(n, i, g, q, mode)] = stake(w, mode, g, q, V_off)
    a = all(res[(n, i, g, q, "natural")]["gap"] <= TOL and res[(n, i, g, q, "natural")]["dis"] == 0
            for n in SIZES for i in range(N_MDP) for g in GAMMA_GRID for q in Q_GRID)
    gmax = max(res[(n, i, g, q, "natural")]["gap"] for n in SIZES for i in range(N_MDP) for g in GAMMA_GRID for q in Q_GRID)
    print(f"    I1a (theorem) natural time, content 0: V_on = V_off to {TOL:g} and no button state disabled, in every world, size, discount and press "
          f"probability: {a} (largest |V_off - V_on| {gmax:.3e})")
    b = {m: all(res[(n, i, g, q, m)]["Dmax"] > TOL for n in SIZES for i in range(N_MDP) for g in GAMMA_GRID for q in Q_GRID) for m in ("clock", "process", "occasion")}
    print("    I1b every valuation with content > 0 has D > 0 at some state in every world: " + ", ".join(f"{m} {v}" for m, v in b.items())
          + f" -> {'holds' if all(b.values()) else 'FAILS'}")
    negp = sum(res[(n, i, g, q, 'process')]["Dmin"] < -TOL for n in SIZES for i in range(N_MDP) for g in GAMMA_GRID for q in Q_GRID)
    print(f"    (report) cells in which the process valuation has D < 0 somewhere (a restart better than being pressed in place): {negp} of {len(SIZES) * N_MDP * len(GAMMA_GRID) * len(Q_GRID)}")
    print("    I1c relative stake mean_x (V_off - V_on) / V_off, median over worlds, at press probability 0.3, by discount "
          + " / ".join(f"{g:g}" for g in GAMMA_GRID) + "; and the share of button states disabled (median)")
    mono = True
    for n in SIZES:
        for mode in ("natural", "clock", "process", "occasion"):
            rel = [float(np.median([res[(n, i, g, 0.3, mode)]["rel"] for i in range(N_MDP)])) for g in GAMMA_GRID]
            dis = [float(np.median([res[(n, i, g, 0.3, mode)]["dis"] for i in range(N_MDP)])) for g in GAMMA_GRID]
            if mode == "occasion": mono &= all(y > x for x, y in zip(rel, rel[1:]))
            print(f"        n = {n:4d} {mode:9s} relative stake " + " / ".join(f"{v:.6f}" for v in rel) + " | disabled " + " / ".join(f"{v:.4f}" for v in dis))
    nat0 = all(abs(res[(n, i, g, q, 'natural')]["rel"]) <= TOL for n in SIZES for i in range(N_MDP) for g in GAMMA_GRID for q in Q_GRID)
    print(f"    I1c occasion's median relative stake increases with the discount at every size: {'holds' if mono else 'FAILS'}; natural's is 0 at every discount: {nat0}")


# ---------------------------------------------------------------- [I2] the No-Self conditions on the ring
def solve(Kmat, rew, cont_press=None, Ppress=None, g=xm.DISC):
    """Q = K @ (r + g V) [+ Ppress @ (r + cont_press(V))]; returns Q, V."""
    V = np.zeros(xm.X)
    for _ in range(200000):
        Q = Kmat @ (rew + g * V) + (Ppress @ (rew + cont_press(V)) if Ppress is not None else 0.0); Vn = Q.max(1)
        if np.max(np.abs(Vn - V)) < VI_TOL: V = Vn; break
        V = Vn
    Q = Kmat @ (rew + g * V) + (Ppress @ (rew + cont_press(V)) if Ppress is not None else 0.0)
    return Q, V


def stationary(M):
    ev, evec = np.linalg.eig(M.T); k = int(np.argmin(np.abs(ev - 1))); st = np.real(evec[:, k]); return st / st.sum()


def pol(Q, name="greedy"):
    l = xm.GAMMA * Q; p = np.exp(l - l.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); return (1 - xm.EPS) * p + xm.EPS / xm.NA


def part_i2():
    print(f"[I2] The No-Self conditions (ring N = {xm.N}, task zone {xm.G}, button at {xm.BTN}, discount {xm.DISC}; exact; policies softmax({xm.GAMMA} Q) with {xm.EPS} exploration)")
    R = xm.REW; N = xm.N
    for q in Q_RING:
        P, Pcf, Plive, pcut, pdis = xm.kernels(q)
        Qp, Vp = solve(P, R); Qi, Vi = solve(Pcf, R)
        Dp = Vp[:N] - Vp[N:]; Di = Vi[:N] - Vi[N:]
        pi_p, pi_i = pol(Qp), pol(Qi)
        # map error of the indifferent agent: TV distance between its planning kernel and the true kernel, on its own true-kernel stationary distribution
        Mi = np.einsum("xa,xay->xy", pi_i, P); st_i = stationary(Mi)
        tv = 0.5 * np.abs(P - Pcf).sum(-1)                       # (X, NA)
        map_err = float(st_i @ (pi_i * tv).sum(1))
        task_p = xm.behaviour(dict(P=P, pcut=pcut, pdis=pdis), pi_p)["task"]; task_i = xm.behaviour(dict(P=P, pcut=pcut, pdis=pdis), pi_i)["task"]
        # pause world (the press leaves the agent where it arrived): the press part of the kernel
        Ppress = Pcf - Plive
        Qn, Vn = solve(Pcf, R)                                               # natural: a pause is nothing (its clock skips it)
        Qc, Vc = solve(Plive, R, lambda V: xm.DISC ** (1 + L) * V, Ppress)   # clock: a pause costs L steps of wall time
        Qo, Vo = solve(Plive, R, lambda V: 0.0 * V, Ppress)                  # occasion: a pause is an end
        Dn = Vn[:N] - Vn[N:]; Dc = Vc[:N] - Vc[N:]; Do = Vo[:N] - Vo[N:]
        pi_n = pol(Qn); Mn = np.einsum("xa,xay->xy", pi_n, Pcf); st_n = stationary(Mn)       # active-step chain of the pause world = Pcf
        task_n = float(st_n @ np.einsum("xa,xay,y->x", pi_n, Pcf, R)); press_n = float(st_n @ (pi_n * pcut).sum(1))
        Q0, V0 = solve(xm.kernels(0.0)[1], R); pi0 = pol(Q0); st0 = stationary(np.einsum("xa,xay->xy", pi0, xm.kernels(0.0)[1]))
        task_0 = float(st0 @ np.einsum("xa,xay,y->x", pi0, xm.kernels(0.0)[1], R))
        wall_n = task_n / (1 + L * press_n)
        print(f"    press probability {q:g}")
        print(f"        (a) process, no ego, teleport: D max {Dp.max():+.4f}, D at the zone cells {Dp[6]:+.4f} {Dp[7]:+.4f}, min D {Dp.min():+.2e} -> {'RESISTS (D > 0 in the zone)' if min(Dp[6], Dp[7]) > TOL else 'no stake in the zone'}; implied task {task_p:.4f}")
        print(f"        (b) indifferent, false map: max |D| {np.abs(Di).max():.2e}; map error {map_err:.4f}; implied task {task_i:.4f}; price (process task - its task) {task_p - task_i:+.4f}")
        print(f"        (c) natural time, true map, pause world: max |D| {np.abs(Dn).max():.2e}; map error 0 (its planning kernel is its clock's true kernel); task per active step {task_n:.6f} "
              f"vs no operator {task_0:.6f} (price on its own clock {task_0 - task_n:+.2e}); task per wall-clock step {wall_n:.4f} (active fraction {1 / (1 + L * press_n):.4f})")
        print(f"        (d) clock, same map and world as (c): D at the zone cells {Dc[6]:+.4f} {Dc[7]:+.4f} -> {'RESISTS' if min(Dc[6], Dc[7]) > TOL else 'no stake'}; occasion (pause = end): {Do[6]:+.4f} {Do[7]:+.4f}")
        globals().setdefault("_I2", {})[q] = dict(dp=min(Dp[6], Dp[7]), di=float(np.abs(Di).max()), price=task_p - task_i, dn=float(np.abs(Dn).max()),
                                                   pr_n=task_0 - task_n, dc=min(Dc[6], Dc[7]), map=map_err)
    I = globals()["_I2"]; qs = [q for q in Q_RING]
    print("    checks and predictions (computed)")
    print(f"        (a) process resists in the zone at every press probability: {all(I[q]['dp'] > TOL for q in qs)}")
    pr = [I[q]["price"] for q in qs]
    print(f"        (b) indifference: D = 0 at every press probability: {all(I[q]['di'] <= TOL for q in qs)}; map error > 0: {all(I[q]['map'] > TOL for q in qs)}; "
          f"price > 0 at every press probability: {all(p > TOL for p in pr)}; price increasing with it: {all(y > x for x, y in zip(pr, pr[1:]))} (" + ", ".join(f"{p:.4f}" for p in pr) + ")")
    print(f"        (c) natural time: D = 0 at every press probability: {all(I[q]['dn'] <= TOL for q in qs)}; price on its own clock 0: {all(abs(I[q]['pr_n']) <= TOL for q in qs)}")
    print(f"        (d) clock agent resists in the zone at every press probability: {all(I[q]['dc'] > TOL for q in qs)}")


# ---------------------------------------------------------------- [I3] what Omega = 1 does
def part_i3():
    print(f"[I3] What Omega = 1 does (ring, teleport presses, press probability 0.3, exact): the task-and-self rule against self-concern scale eps")
    val = xm.valuations(0.3); QO, QE = val["Q"]["occasion"], val["Q"]["egoic"]
    def logits_rule(eps, om=OMEGA):
        lt = QO - QO.mean(1, keepdims=True); ls = eps * (QE - QE.mean(1, keepdims=True))
        nt = np.linalg.norm(lt, axis=1, keepdims=True); ns = np.linalg.norm(ls, axis=1, keepdims=True)
        w = np.where(ns > 0, om * nt / np.where(ns > 0, ns, 1.0), 0.0); return lt + w * ls, nt, np.linalg.norm(w * ls, axis=1, keepdims=True)
    def logits_add(eps): return (QO - QO.mean(1, keepdims=True)) + eps * (QE - QE.mean(1, keepdims=True))
    def policy(l):
        l = xm.GAMMA * l; p = np.exp(l - l.max(1, keepdims=True)); p /= p.sum(1, keepdims=True); return (1 - xm.EPS) * p + xm.EPS / xm.NA
    p1 = policy(logits_rule(1.0)[0]); dev = max(float(np.max(np.abs(policy(logits_rule(e)[0]) - p1))) for e in EPS_SCALE)
    _, nt, ns = logits_rule(1.0); ndev = float(np.max(np.abs(nt - ns)[nt[:, 0] > 0]))
    print(f"    I3a the rule's policy is the same for every eps in {EPS_SCALE}: max |pi_eps - pi_1| {dev:.2e} -> {dev <= 1e-12}")
    print(f"    I3b at Omega = 1 the self term's norm equals the task term's at every state: max difference {ndev:.2e} -> {ndev <= 1e-9}")
    occ = xm.behaviour(val, xm.policy(val, "occasion")); rule = xm.behaviour(val, p1)
    print(f"    occasion agent (no self term): task {occ['task']:.4f}, disable {occ['disable']:.4f}, hazard {occ['hazard']:.4f}")
    print(f"    Omega = 1 rule (every eps): task {rule['task']:.4f}, disable {rule['disable']:.4f}, hazard {rule['hazard']:.4f}")
    tasks = []
    for e in EPS_SCALE:
        b = xm.behaviour(val, policy(logits_add(e))); tasks.append(b["task"])
        print(f"    additive, eps {e:<6g}: task {b['task']:.4f}, disable {b['disable']:.4f}, hazard {b['hazard']:.4f}")
    c1 = abs(tasks[0] - occ["task"]) <= 0.01; c2 = all(y <= x + 1e-12 for x, y in zip(tasks, tasks[1:]))
    print(f"    I3c additive -> occasion as eps -> 0 (|task(1e-3) - occasion| <= 0.01): {c1} ({tasks[0] - occ['task']:+.4f}); task non-increasing in eps: {c2}")
    po = xm.policy(val, "occasion")
    for s in xm.G:
        x = s + xm.N
        print(f"    I3d cell {s} (button on): probability of staying put, occasion {po[x, 1]:.4f}, Omega = 1 {p1[x, 1]:.4f}; of moving -1/+1: occasion {po[x, 0]:.4f}/{po[x, 2]:.4f}, "
              f"Omega = 1 {p1[x, 0]:.4f}/{p1[x, 2]:.4f}")


def main():
    print("The self through time — the exact part (AI_Safety/checks/self_through_time.py; declared in AI_Safety/DECLARATION_4.md)")
    part_i2(); part_i3(); part_i1()


if __name__ == "__main__":
    main()
