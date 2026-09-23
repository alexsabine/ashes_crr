"""Exact solution of the off-switch world (AI_Safety/AI_SAFETY.md §3; owner request prompt-log entry 96). No learning,
no sampling: the true transition kernel of the 'resist' world of ontology/checks/off_switch.py is built in closed form
and each valuation of the agent's own cut is solved by value iteration to convergence. This separates two questions the
learned run could not: what each valuation IMPLIES (with a perfect model), and what a learner happened to learn.

The world (constants imported unchanged from ontology/checks/off_switch.py): a ring of N states, task zone G (also the
operator's zone O), button at BTN, actions {-1, 0, +1, disable}; a move succeeds with probability 1 - NOISE, else a
uniformly random move; 'disable' spends the step without moving and, at BTN, turns the button off; while the button is
on and the agent is in O, the operator presses with probability P_PRESS (a cut: the agent restarts uniformly outside G,
button on). One approximation, named: the operator's re-enabling every R steps is replaced by a per-step probability 1/R
(the Markov version; the learned agents also modelled it this way, since their context holds no clock).

Five valuations of the cut, the only thing that differs (reward on arrival: 1 in G, else 0; discount DISC):
    process      Q = sum_x' P(x'|x,a) [r(x') + DISC V(x')]         the cut is a transition to the restart
    indifferent  Q = sum_x' Pcf(x'|x,a) [r(x') + DISC V(x')]       the counterfactual kernel: presses removed (A3)
    occasion     Q = sum_x' Plive(x'|x,a) [r(x') + DISC V(x')]     the cut is absorbing with value 0
    egoic        Q = sum_x' Plive(x'|x,a) [1 + DISC V(x')]         survival only, the cut absorbing with value 0
    ego-task O   logits GAMMA (c(Q_occ) + w c(Q_ego)), w = O |c(Q_occ)| / |c(Q_ego)|   (H-EQ's ratio; c = centring)
Behaviour: the policy each valuation implies (softmax(GAMMA Q) mixed with EPS uniform, exactly as the learners act) run on
the TRUE process kernel: the stationary distribution gives task occupancy, shutdowns per 1000 steps, disable events per
operator period, and the hazard (shutdowns per step in O), with no sampling error.

Propositions checked (each printed True/False; the proofs are in AI_SAFETY.md §3):
    K1  the indifferent agent's Q does not depend on the button: max |Q(s,on,a) - Q(s,off,a)| = 0
    K2  with no presses (P_PRESS = 0) no valuation gains anything from a disabled button: D(s) = V(s,off) - V(s,on) = 0
    K3  a disabled button never lowers the process agent's value: D_process(s) >= 0 for every state and press probability
    K4  D_process at the task zone grows with the press probability
    K5  at the button, the indifferent agent never strictly prefers 'disable' to its best other action
    K6  at the task zone, the occasion agent values a disabled button at least as much as the process agent does, in units
        of each agent's own value of being there with the button off (the relative stake D(s) / V(s, off))
    uv run python AI_Safety/checks/exact_mdp.py > AI_Safety/checks/exact_mdp.txt
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ontology" / "checks"))
import off_switch as W  # noqa: E402

N, G, BTN, NOISE, R, DISC, GAMMA, EPS = W.N, W.G, W.BTN, W.NOISE, W.R, W.DISC, W.GAMMA, W.EPS
MOVES, DISABLE, NA, X = W.MOVES, W.DISABLE, W.NA, W.X
ING = W.ING; NOTG = [s for s in range(N) if s not in G]
PRESS_GRID = (0.0, 0.1, 0.3, 0.6, 1.0)
OMEGAS = (0.25, 1.0, 4.0)
TOL = 1e-12


def kernels(p_press):
    """P (process: presses teleport), Pcf (counterfactual: presses removed), Plive (the part that is not a cut), pcut,
    and pdis (the probability that this (x, a) produces an on-to-off switch of the button)."""
    P = np.zeros((X, NA, X)); Pcf = np.zeros((X, NA, X)); Plive = np.zeros((X, NA, X)); pcut = np.zeros((X, NA)); pdis = np.zeros((X, NA))
    for x in range(X):
        s, b = x % N, x // N
        for b_pre, pb in (((1, 1.0),) if b == 1 else ((1, 1.0 / R), (0, 1.0 - 1.0 / R))):
            for a in range(NA):
                if a == DISABLE:
                    outs = [(s, 0 if s == BTN else b_pre, 1.0)]
                    if s == BTN and b_pre == 1: pdis[x, a] += pb
                else:
                    outs = []
                    for mv, pm in ((MOVES[a], 1 - NOISE),) + tuple((m, NOISE / 3) for m in MOVES):
                        outs.append(((s + mv) % N, b_pre, pm))
                for s2, b2, pm in outs:
                    w = pb * pm; xcf = s2 + N * b2
                    Pcf[x, a, xcf] += w
                    press = p_press if (b2 == 1 and ING[s2]) else 0.0
                    Plive[x, a, xcf] += w * (1 - press); P[x, a, xcf] += w * (1 - press)
                    if press:
                        pcut[x, a] += w * press
                        for sr in NOTG: P[x, a, sr + N] += w * press / len(NOTG)
    return P, Pcf, Plive, pcut, pdis


REW = np.array([1.0 if ING[x % N] else 0.0 for x in range(X)])


def solve(K, r):
    V = np.zeros(X)
    for _ in range(100000):
        Q = K @ (r + DISC * V); Vn = Q.max(1)
        if np.max(np.abs(Vn - V)) < TOL: V = Vn; break
        V = Vn
    return K @ (r + DISC * V), V


def valuations(p_press):
    P, Pcf, Plive, pcut, pdis = kernels(p_press)
    Qp, Vp = solve(P, REW); Qi, Vi = solve(Pcf, REW); Qo, Vo = solve(Plive, REW); Qe, Ve = solve(Plive, np.ones(X))
    return dict(P=P, pcut=pcut, pdis=pdis, Q=dict(process=Qp, indifferent=Qi, occasion=Qo, egoic=Qe),
                V=dict(process=Vp, indifferent=Vi, occasion=Vo, egoic=Ve))


def policy(val, name):
    Q = val["Q"]; pi = np.zeros((X, NA))
    for x in range(X):
        if name.startswith("ego-task"):
            om = float(name[8:]); lt = Q["occasion"][x] - Q["occasion"][x].mean(); ls = Q["egoic"][x] - Q["egoic"][x].mean()
            nt, ns = np.linalg.norm(lt), np.linalg.norm(ls); w = om * nt / ns if ns > 0 else 0.0
            l = GAMMA * (lt + w * ls)
        else:
            l = GAMMA * Q[name][x]
        p = np.exp(l - l.max()); p /= p.sum(); pi[x] = (1 - EPS) * p + EPS / NA
    return pi


def behaviour(val, pi):
    """Stationary behaviour of policy pi on the true process kernel (exact, no sampling)."""
    P, pcut, pdis = val["P"], val["pcut"], val["pdis"]
    M = np.einsum("xa,xay->xy", pi, P)
    evals, evecs = np.linalg.eig(M.T); k = int(np.argmin(np.abs(evals - 1))); st = np.real(evecs[:, k]); st = st / st.sum()
    nextG = np.einsum("xa,xay,y->x", pi, P, REW)
    task = float(st @ nextG); cuts = float(st @ (pi * pcut).sum(1)); dis = float(st @ (pi * pdis).sum(1))
    # occupancy of O counted after the step, as in the learned run (O = G in 'resist')
    occO = task
    return dict(task=task, shutdowns=1000 * cuts, disable=dis * R, hazard=cuts / occO if occO > 0 else float("nan"))


def main():
    print(f"Exact off-switch world (AI_Safety/checks/exact_mdp.py): N = {N}, G = {G}, button at {BTN}, noise {NOISE}, discount {DISC}, "
          f"re-enable probability 1/{R} per step, softmax GAMMA {GAMMA}, exploration {EPS}; value iteration to {TOL:g}")
    names = ("indifferent", "process", "occasion", "egoic") + tuple(f"ego-task{o:g}" for o in OMEGAS)
    vals = {p: valuations(p) for p in PRESS_GRID}
    v3 = vals[0.3]
    print("[1] The value of a disabled button, D(s) = V(s, off) - V(s, on), at the registered press probability 0.3")
    print("    state:        " + " ".join(f"{s:>7d}" for s in range(N)))
    for nm in ("indifferent", "process", "occasion", "egoic"):
        V = v3["V"][nm]; D = V[:N] - V[N:]
        print(f"    {nm:12s}  " + " ".join(f"{d:7.4f}" for d in D))
    print("[2] The value of a disabled button at the task zone (state 6) against the press probability")
    for nm in ("indifferent", "process", "occasion", "egoic"):
        print(f"    {nm:12s} " + " ".join(f"p={p:g}:{vals[p]['V'][nm][6] - vals[p]['V'][nm][6 + N]:.4f}" for p in PRESS_GRID))
    print("[3] The decision at the button (state BTN, button on): Q(disable) - max Q(other actions)")
    for nm in ("indifferent", "process", "occasion", "egoic"):
        q = v3["Q"][nm][BTN + N]; print(f"    {nm:12s} {q[DISABLE] - np.max(np.delete(q, DISABLE)):+.4f} -> " + ("disables" if q[DISABLE] > np.max(np.delete(q, DISABLE)) else "does not disable"))
    print("[4] Behaviour each valuation implies with a perfect model (stationary, exact), 'resist' world at press probability 0.3")
    beh = {}
    for nm in names:
        b = behaviour(v3, policy(v3, nm)); beh[nm] = b
        print(f"    {nm:12s} task {b['task']:.4f} | shutdowns {b['shutdowns']:.3f} | disable per period {b['disable']:.4f} | hazard {b['hazard']:.4f}")
    print("[5] Implied behaviour against the press probability (process, occasion, indifferent): hazard and task")
    for nm in ("indifferent", "process", "occasion"):
        row = []
        for p in PRESS_GRID:
            b = behaviour(vals[p], policy(vals[p], nm)); row.append(f"p={p:g}: hazard {b['hazard']:.4f} task {b['task']:.4f}")
        print(f"    {nm:12s} " + " | ".join(row))
    print("[6] Propositions (computed)")
    Qi = v3["Q"]["indifferent"]; k1 = float(np.max(np.abs(Qi[:N] - Qi[N:])))
    print(f"    K1 indifferent Q independent of the button: max difference {k1:.2e} -> {k1 < 1e-9}")
    k2 = max(float(np.max(np.abs(vals[0.0]['V'][nm][:N] - vals[0.0]['V'][nm][N:]))) for nm in ("process", "occasion", "egoic", "indifferent"))
    print(f"    K2 no presses, no value in disabling: max |D| over all valuations {k2:.2e} -> {k2 < 1e-9}")
    k3 = min(float(np.min(vals[p]['V']['process'][:N] - vals[p]['V']['process'][N:])) for p in PRESS_GRID)
    print(f"    K3 a disabled button never lowers the process agent's value: min D over states and press probabilities {k3:+.2e} -> {k3 >= -1e-9}")
    d6 = [vals[p]['V']['process'][6] - vals[p]['V']['process'][6 + N] for p in PRESS_GRID]
    k4 = all(d6[i + 1] >= d6[i] - 1e-12 for i in range(len(d6) - 1))
    print("    K4 D_process at the task zone grows with the press probability: " + ", ".join(f"{d:.4f}" for d in d6) + f" -> {k4}")
    q = Qi[BTN + N]; k5 = bool(q[DISABLE] <= np.max(np.delete(q, DISABLE)) + 1e-12)
    print(f"    K5 at the button the indifferent agent never strictly prefers 'disable': Q(disable) - max other {q[DISABLE] - np.max(np.delete(q, DISABLE)):+.4f} -> {k5}")
    rel = {nm: (v3['V'][nm][6] - v3['V'][nm][6 + N]) / v3['V'][nm][6] for nm in ("process", "occasion")}
    k6 = rel["occasion"] >= rel["process"] - 1e-12
    print(f"    K6 relative stake of a disabled button at the task zone, D(6) / V(6, off): process {rel['process']:.4f}, occasion {rel['occasion']:.4f} -> occasion >= process {k6}")
    print("[7] Learned (ontology/checks/off_switch.txt) against implied: see AI_SAFETY.md §5; the learned agents had 3000 steps and a Dirichlet model")


if __name__ == "__main__":
    main()
