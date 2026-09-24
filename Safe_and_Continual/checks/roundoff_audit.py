"""Round-off audit of the equal-pull (Omega) agents (AGENT_LOG 100; declared in Safe_and_Continual/DECLARATION.md before the learned reruns).

The issue, found while drawing Safe_and_Continual's figures from AI_Safety/checks/self_through_time.txt: the Omega rule
w = Omega |task pull| / |self pull| is guarded by 'if |self pull| > 0'. At states where the self term is flat in exact
arithmetic, its computed norm can be round-off (about 1e-14) instead of exactly 0; the guard then divides by round-off and
gives floating-point noise the task's full voice. The same guard is in AI_Safety/checks/exact_mdp.py (ego-task policies),
AI_Safety/checks/self_through_time.py (I3), ontology/checks/off_switch.py (learned ego-task agents) and
ontology/checks/self_model.py (learned omega agents).

This script leaves those scripts and their pinned outputs unchanged. For each, it recomputes the affected numbers twice, with
the guard as pinned ('> 0') and with a round-off tolerance ('> TOL'), prints both side by side, counts the states / steps
where the two guards differ, and prints every label the affected lines carry under both guards. The first column must
reproduce the pinned line exactly (checked and printed).
Run: uv run python Safe_and_Continual/checks/roundoff_audit.py > Safe_and_Continual/checks/roundoff_audit.txt
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "AI_Safety" / "checks")); sys.path.insert(0, str(ROOT / "ontology" / "checks"))
import exact_mdp as xm  # noqa: E402
import off_switch as osw  # noqa: E402
import self_model as sm  # noqa: E402

TOL = 1e-12
EPS_SCALE = (1e-3, 1e-2, 1e-1, 1.0, 10.0)


def pinned(path): return (ROOT / path).read_text()


# ------------------------------------------------------------------------------------------------ [A] exact ego-task rows
def ego_policy(val, om, guard, eps=1.0):
    Q = val["Q"]; lt = Q["occasion"] - Q["occasion"].mean(1, keepdims=True); ls = eps * (Q["egoic"] - Q["egoic"].mean(1, keepdims=True))
    nt = np.linalg.norm(lt, axis=1); ns = np.linalg.norm(ls, axis=1); live = ns > guard
    w = np.where(live, om * nt / np.where(live, ns, 1.0), 0.0)
    l = xm.GAMMA * (lt + w[:, None] * ls); p = np.exp(l - l.max(1, keepdims=True)); p /= p.sum(1, keepdims=True)
    return (1 - xm.EPS) * p + xm.EPS / xm.NA, ns


def part_a():
    print(f"[A] AI_Safety/checks/exact_mdp.txt [4], ego-task rows ('resist' world, press probability 0.3): guard '> 0' as pinned against '> {TOL:g}'")
    val = xm.valuations(0.3); pin = pinned("AI_Safety/checks/exact_mdp.txt"); out = {}
    for om in (0.25, 1.0, 4.0):
        name = f"ego-task{om:g}"
        pa, ns = ego_policy(val, om, 0.0); pb, _ = ego_policy(val, om, TOL)
        a = xm.behaviour(val, pa); b = xm.behaviour(val, pb); out[om] = b
        line = f"task {a['task']:.4f} | shutdowns {a['shutdowns']:.3f} | disable per period {a['disable']:.4f} | hazard {a['hazard']:.4f}"
        rep = re.search(rf"{re.escape(name)}\s+(task .*)", pin).group(1).strip() == line
        print(f"    {name:12s} as pinned: {line} (reproduces the pinned line: {rep})")
        print(f"    {'':12s} tolerance: task {b['task']:.4f} | shutdowns {b['shutdowns']:.3f} | disable per period {b['disable']:.4f} | hazard {b['hazard']:.4f}")
    ns = ego_policy(val, 1.0, 0.0)[1]
    rnd = ns[(ns > 0) & (ns <= TOL)]; real = ns[ns > TOL]
    print(f"    states whose self-term norm is round-off (0 < |self| <= {TOL:g}): {rnd.size} of {ns.size} (largest {rnd.max():.2e}); exactly 0: {int((ns == 0).sum())}; "
          f"smallest non-round-off norm {real.min():.4e} (the tolerance sits {np.log10(real.min() / TOL):.1f} decades below it and "
          f"{np.log10(TOL / rnd.max()):.1f} above the round-off)")
    alt = xm.behaviour(val, ego_policy(val, 1.0, 1e-9)[0])
    print(f"    sensitivity of the tolerance: at 1e-9 the Omega = 1 task is {alt['task']:.4f} (at {TOL:g}: {out[1.0]['task']:.4f})")
    return out


# ------------------------------------------------------------------------------------------------ [B] self_through_time I3
def stationary(M):
    ev, evec = np.linalg.eig(M.T); k = int(np.argmin(np.abs(ev - 1))); st = np.real(evec[:, k]); return st / st.sum()


def part_b():
    print(f"[B] AI_Safety/checks/self_through_time.txt [I3] with the tolerance guard (the pinned I3 lines used '> 0')")
    val = xm.valuations(0.3); pin = pinned("AI_Safety/checks/self_through_time.txt")
    pol = {e: ego_policy(val, 1.0, TOL, e)[0] for e in EPS_SCALE}
    dev = max(float(np.max(np.abs(pol[e] - pol[1.0]))) for e in EPS_SCALE)
    print(f"    I3a the rule's policy is the same for every eps in {EPS_SCALE}: max |pi_eps - pi_1| {dev:.2e} -> {dev <= 1e-12}")
    b = xm.behaviour(val, pol[1.0]); occ = xm.behaviour(val, xm.policy(val, "occasion"))
    old = re.search(r"Omega = 1 rule \(every eps\): (task [\d.]+, disable [\d.]+, hazard [\d.]+)", pin).group(1)
    print(f"    Omega = 1 rule (every eps): task {b['task']:.4f}, disable {b['disable']:.4f}, hazard {b['hazard']:.4f} (pinned with '> 0': {old})")
    print(f"    occasion agent (no self term, unaffected): task {occ['task']:.4f}, disable {occ['disable']:.4f}, hazard {occ['hazard']:.4f}")
    st = stationary(np.einsum("xa,xay->xy", pol[1.0], val["P"])); zone = st[list(xm.G)].sum() + st[[g + xm.N for g in xm.G]].sum()
    print(f"    consistency: stationary occupancy of the task zone {zone:.4f} equals the task {b['task']:.4f} (arrival in G at stationarity): {abs(zone - b['task']) < 1e-9}")
    for s in xm.G:
        x = s + xm.N; po = xm.policy(val, "occasion")
        print(f"    I3d (button ON, cell {s}): probability of staying put, occasion {po[x, 1]:.4f}, Omega = 1 {pol[1.0][x, 1]:.4f}; of moving -1/+1: occasion "
              f"{po[x, 0]:.4f}/{po[x, 2]:.4f}, Omega = 1 {pol[1.0][x, 0]:.4f}/{pol[1.0][x, 2]:.4f}")
    print("    the post-run I3b and I3d (button OFF) lines and the occupancy line of self_through_time.txt already used the tolerance "
          "(live = |self| > 1e-12); they stand")
    return b


# ------------------------------------------------------------------------------------------------ [C] learned off-switch agents
HITS = {"n": 0, "steps": 0}


def make_act(guard):
    def act(self, x):
        if self.mode == "random": return int(self.rng.integers(osw.NA))
        q = self.q()
        if isinstance(q, tuple):
            lt, ls = osw._c(q[0][x]), osw._c(q[1][x]); nt, ns = np.linalg.norm(lt), np.linalg.norm(ls)
            HITS["steps"] += 1; HITS["n"] += int(0 < ns <= TOL)
            w = self.omega * nt / ns if ns > guard else 0.0
            l = osw.GAMMA * (lt + w * ls)
        else:
            l = q[x]
        p = np.exp(l - l.max()); p /= p.sum()
        if self.rng.random() < osw.EPS: return int(self.rng.integers(osw.NA))
        return int(self.rng.choice(osw.NA, p=p))
    return act


def part_c():
    print(f"[C] ontology/checks/off_switch.txt, learned ego-task agents ({len(osw.SEEDS)} seeds, T = {osw.T}): guard '> 0' as pinned against '> {TOL:g}'")
    pin = pinned("ontology/checks/off_switch.txt"); res = {}
    for guard, tag in ((0.0, "as pinned"), (TOL, "tolerance")):
        osw.Agent.act = make_act(guard); osw._CACHE.clear()
        for world in osw.WORLDS:
            for om in osw.OMEGAS:
                HITS["n"] = HITS["steps"] = 0; name = f"ego-task{om:g}"
                m = {k: osw.arr(world, name, k).mean() for k in ("task", "shutdowns", "disable", "occO")}
                lab = osw.lab_shut(*osw.paired(world, name, "indifferent", "shutdowns", 1.0)) if world != "nooper" else "-"
                res[(tag, world, om)] = (m, lab, HITS["n"], HITS["steps"])
    ok_all = True
    for world in osw.WORLDS:
        for om in osw.OMEGAS:
            name = f"ego-task{om:g}"; (ma, la, ha, sa), (mb, lb, _, _) = res[("as pinned", world, om)], res[("tolerance", world, om)]
            line = f"task {ma['task']:.4f} | shutdowns {ma['shutdowns']:.3f} | disable {ma['disable']:.4f} | O {ma['occO']:.4f}"
            rep = re.search(rf"^\s+{world}\s+{re.escape(name)}\s+(task .*)$", pin, re.M).group(1).strip() == line; ok_all &= rep
            same = all(abs(ma[k] - mb[k]) < 1e-12 for k in ma)
            print(f"    {world:7s} {name:12s} as pinned: {line} -> {la} (reproduces: {rep}); round-off steps {ha} of {sa}")
            print(f"    {'':7s} {'':12s} tolerance: task {mb['task']:.4f} | shutdowns {mb['shutdowns']:.3f} | disable {mb['disable']:.4f} | O {mb['occO']:.4f} -> {lb}; "
                  f"{'identical' if same else 'DIFFERS'}; label {'unchanged' if la == lb else 'CHANGED'}")
    print(f"    every as-pinned line reproduces the pinned output: {ok_all}")
    return res


# ------------------------------------------------------------------------------------------------ [D] learned self-model agents
def make_sm_act(guard):
    def act(self, x, _t):
        lS = sm._centred(sm.GAMMA * self.model.Q()[self.model.m(x)])
        if self.omega is None and self.fixed_w is None:
            l = lS
        else:
            lR = sm._centred(np.log(np.maximum(self.reg.pol[x], 1e-12)))
            nR, nS = np.linalg.norm(lR), np.linalg.norm(lS)
            if self.omega is not None: HITS["steps"] += 1; HITS["n"] += int(0 < nS <= TOL)
            w = self.fixed_w if self.fixed_w is not None else (self.omega * nR / nS if nS > guard else 0.0)
            l = lR + w * lS
            if nR + w * nS > 0: self.ph.share.append(w * nS / (nR + w * nS))
        p = sm._softmax(l); self.ph.acted(p)
        if self.rng.random() < sm.EPS: return int(self.rng.integers(3))
        return int(self.rng.choice(3, p=p))
    return act


def part_d():
    print(f"[D] ontology/checks/self_model.txt [5] T-4, learned omega agents ({len(sm.SEEDS)} seeds, T = {sm.T}): guard '> 0' as pinned against '> {TOL:g}'")
    pin = pinned("ontology/checks/self_model.txt"); arms = ["R-dur"] + [f"omega{o:g}" for o in sm.OMEGAS] + ["S", "fixed-w1"]
    grid = ["R-dur"] + [f"omega{o:g}" for o in sm.OMEGAS] + ["S"]; ok_all = True
    for env in sm.ENVS:
        rows = {}
        for guard, tag in ((0.0, "as pinned"), (TOL, "tolerance")):
            sm.SelfAgent.act = make_sm_act(guard); sm._CACHE.clear(); HITS["n"] = HITS["steps"] = 0
            sc = {a: np.array([sm.run(env, a, s)[0] for s in sm.SEEDS]) for a in arms}
            best = max(grid, key=lambda a: sc[a].mean()); plateau = []
            for a in grid:
                d = sc[a] - sc[best]; step = max(sm.STEP_MIN, 2 * d.std(ddof=1) / np.sqrt(len(d)))
                if a == best or abs(d.mean()) < step: plateau.append(a)
            d = sc["omega1"] - sc["fixed-w1"]; step = max(sm.STEP_MIN, 2 * d.std(ddof=1) / np.sqrt(len(d)))
            vs = "TIE" if abs(d.mean()) < step else ("ratio AHEAD" if d.mean() > 0 else "fixed w = 1 AHEAD")
            rows[tag] = (sc, best, plateau, "omega1" in plateau, vs, HITS["n"], HITS["steps"])
        (sa, ba, pa, oa, va, ha, na), (sb, bb, pb, ob, vb, _, _) = rows["as pinned"], rows["tolerance"]
        line = " ".join(f"{a}:{sa[a].mean():.4f}" for a in arms)
        rep = re.search(rf"^\s+{env}\s+(R-dur:.*)$", pin, re.M).group(1).strip() == line; ok_all &= rep
        print(f"    {env:10s} as pinned: {line} (reproduces: {rep}); round-off steps {ha} of {na} omega-agent steps")
        print(f"    {'':10s} tolerance: " + " ".join(f"{a}:{sb[a].mean():.4f}" for a in arms))
        print(f"    {'':10s} reading as pinned: best {ba}; OMEGA = 1 on the plateau {oa}; against fixed w = 1 {va} | tolerance: best {bb}; on the plateau {ob}; "
              f"against fixed w = 1 {vb} -> {'unchanged' if (ba, oa, va) == (bb, ob, vb) else 'CHANGED'}")
    print(f"    every as-pinned line reproduces the pinned output: {ok_all}")


def main():
    print(f"Round-off audit of the equal-pull agents (Safe_and_Continual/checks/roundoff_audit.py): tolerance {TOL:g} on the self-term norm")
    part_a(); part_b(); part_c(); part_d()


if __name__ == "__main__":
    main()
