"""Phase-A gate for a heterogeneous-node (federated personalisation) test of H-EQ -- synthetic only, no data
(owner request prompt-log entry 89; the design sketched in the answers to entries 76 and 86).

Setting. One shared anchor: a softmax MLP (the S-Y network of crr.surrogates.battery) trained centrally on classes 0-5
of a synthetic 10-class world, with its empirical Fisher F computed centrally at the end (the anchor's curvature, in the
central model's units). N nodes each start from the anchor and personalise on their local classes 6-9 with the past term
2 F (theta - theta_star) (online-EWC form, lambda removed); nothing is aggregated (personalisation, not FedAvg). Nodes
differ in ONE registered way per row:
    loss-scale rows : node i's present gradient is c_i x the cross-entropy gradient (a local loss in different units:
                      sum-reduced over local batches of different size, or a locally re-weighted objective); F is shared,
                      so the balance between present and past pull differs by node while the anchor does not.
    input-unit row  : node i's local inputs are in units s_i (a site whose features are measured in other units); F is
                      shared; informational (no control role): the per-node optimum may move for reasons the rule does
                      not track.
Arms per node: every fixed weight on GRID (the per-node tuned weight is the oracle, R7); the weight tuned on the
reference node (c = 1) applied to every node (one global knob: the central-sweep practice); the registered rule at
Omega = 1 (EMA 0.9 of gradient vectors, Euclidean norm, cap 1e4, floor 1e-12); EQ-B (kappa 2, N 50, N_MIN 10).
Metric: final class-IL error over all 10 classes on the world's held-out rows (lower is better), mean over 5 seeds.

Statistics (every label computed from the numbers, R15):
    step       = max(STEP_MIN, 2 x the standard error of the oracle's per-seed errors), per node.
    FED-1      PASS iff (a) on every node the rule is not behind the node's oracle by >= step, AND (b) the reference-tuned
               weight is behind the oracle by >= step on at least one node (the global knob fails somewhere).
    FED-B      PASS iff on the poisoned node EQ-B is not behind that node's oracle (tuned under the same poison) by
               >= step AND the registered rule is behind it by >= step (the bound is what holds).
Gate table: FED-1 MUST PASS on the heterogeneous loss-scale row and MUST FAIL on the homogeneous row (identical nodes:
the global knob is the oracle, so there is nothing for the rule to fix); FED-B MUST PASS on the poisoned row and MUST
FAIL on the clean heterogeneous row (with no poison the bound must be idle). GATE OPEN iff no violation.
    uv run python theory/checks/fed_heterogeneous_v1.py > theory/checks/fed_heterogeneous_v1.txt
FIRST RUN, kept as run (AGENT_LOG 71): the gate CLOSED on two design defects corrected in fed_heterogeneous.py.
"""
from __future__ import annotations

import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

from crr.surrogates.battery import (_SY_BS, _SY_LR, _SyMLP, _eqb_clip, _sy_ce_grad, _sy_data,  # noqa: E402
                                    EQB_KAPPA)

# ---------------------------------------------------------------- registered constants
D, SEP = 32, 1.4
CENTRAL_CLASSES = tuple(range(6)); LOCAL_CLASSES = (6, 7, 8, 9)
CENTRAL_STEPS = 450; LOCAL_STEPS = 300; N_FISHER = 20
SMOOTH = 0.9; WCAP = 1e4; FLOOR = 1e-12
GRID = tuple(float(2 ** k) for k in range(0, 13))              # 1 .. 4096, x2 steps
SEEDS = tuple(range(5)); STEP_MIN = 0.01                        # one point of error
POISON = (1000.0, 5); POISON_AT = 75                            # the S-Y poisoned regime: x1000 for 5 steps from step 75
ROWS = {
    "hetero_loss": dict(kind="loss", nodes=(0.25, 0.5, 1.0, 2.0, 4.0), poisoned=None),
    "homo_loss": dict(kind="loss", nodes=(1.0, 1.0, 1.0, 1.0, 1.0), poisoned=None),
    "hetero_loss_poisoned": dict(kind="loss", nodes=(0.25, 0.5, 1.0, 2.0, 4.0), poisoned=2),
    "hetero_input": dict(kind="input", nodes=(0.25, 0.5, 1.0, 2.0, 4.0), poisoned=None),
}
REF = 1.0                                                       # the reference node's factor (where the global knob is tuned)
MUST = {("FED-1", "hetero_loss"): True, ("FED-1", "homo_loss"): False,
        ("FED-B", "hetero_loss_poisoned"): True, ("FED-B", "hetero_loss"): False}


def anchor(seed):
    """The shared anchor for one seed: world data, central model trained on classes 0-5, central Fisher."""
    rng = np.random.default_rng(seed)
    (Xtr, ytr), (Xte, yte) = _sy_data(rng, D, SEP, 1.0)
    net = _SyMLP(rng, D)
    ii_c = np.where(np.isin(ytr, CENTRAL_CLASSES))[0]
    for _ in range(CENTRAL_STEPS):
        ii = ii_c[rng.integers(0, len(ii_c), _SY_BS)]
        net.set_flat(net.flat() - _SY_LR * _sy_ce_grad(net, Xtr[ii], ytr[ii]))
    f = np.zeros(net.flat().size)
    for _ in range(N_FISHER):
        ii = ii_c[rng.integers(0, len(ii_c), _SY_BS)]
        f += _sy_ce_grad(net, Xtr[ii], ytr[ii]) ** 2
    return dict(net=net, F=f / N_FISHER * _SY_BS, theta_star=net.flat().copy(), Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte)


def node(anc, kind, factor, node_idx, method, value, seed, poison=None):
    """One node's personalisation from the shared anchor. Returns the class-IL error over all 10 classes and the
    median derived weight."""
    rng = np.random.default_rng([seed, node_idx, 1])
    net = anc["net"].copy(); F = anc["F"]; ts = anc["theta_star"]
    Xtr, ytr, Xte, yte = anc["Xtr"], anc["ytr"], anc["Xte"], anc["yte"]
    unit = factor if kind == "input" else 1.0
    c = factor if kind == "loss" else 1.0
    ii_l = rng.permutation(np.where(np.isin(ytr, LOCAL_CLASSES))[0])
    ema_p = ema_q = None; hist = []; wlog = []
    with np.errstate(all="ignore"):
        for step in range(LOCAL_STEPS):
            ii = ii_l[rng.integers(0, len(ii_l), _SY_BS)]
            g_p = c * _sy_ce_grad(net, Xtr[ii] * unit, ytr[ii])
            if poison is not None and POISON_AT <= step < POISON_AT + poison[1]: g_p = poison[0] * g_p
            if method == "eqb": g_p = _eqb_clip(g_p, hist, EQB_KAPPA)
            g_q = 2 * F * (net.flat() - ts)
            if method == "fixed":
                w = value
            else:
                ema_p = g_p if ema_p is None else SMOOTH * ema_p + (1 - SMOOTH) * g_p
                ema_q = g_q if ema_q is None else SMOOTH * ema_q + (1 - SMOOTH) * g_q
                w = min(value * np.linalg.norm(ema_p) / max(np.linalg.norm(ema_q), FLOOR), WCAP)
            wlog.append(w)
            net.set_flat(net.flat() - _SY_LR * (g_p + w * g_q))
    te_unit = np.where(np.isin(yte, LOCAL_CLASSES), unit, 1.0)[:, None]
    return float(net.err(Xte * te_unit, yte)), float(np.median(wlog))


def run_row(name, spec, anchors):
    nodes = spec["nodes"]; kind = spec["kind"]
    res = []
    for i, fac in enumerate(nodes):
        pz = POISON if spec["poisoned"] == i else None
        fx = {w: np.array([node(anchors[s], kind, fac, i, "fixed", w, s, pz)[0] for s in SEEDS]) for w in GRID}
        eq = [node(anchors[s], kind, fac, i, "eq", 1.0, s, pz) for s in SEEDS]
        eqb = [node(anchors[s], kind, fac, i, "eqb", 1.0, s, pz) for s in SEEDS]
        res.append(dict(fac=fac, fx=fx, eq=np.array([e[0] for e in eq]), eq_w=float(np.median([e[1] for e in eq])),
                        eqb=np.array([e[0] for e in eqb]), eqb_w=float(np.median([e[1] for e in eqb])), poisoned=pz is not None))
    ref_i = [i for i, f in enumerate(nodes) if f == REF][0]
    ref_w = min(GRID, key=lambda w: res[ref_i]["fx"][w].mean())   # the global knob, tuned on the reference node (first min on ties)
    print(f"[{name}] kind={kind} nodes={nodes} poisoned node index={spec['poisoned']} | reference node {ref_i} (factor {REF}), global knob w = {ref_w:g}")
    fed1_a, fed1_b = True, False; fedb = None
    for i, r in enumerate(res):
        orc_w = min(GRID, key=lambda w: r["fx"][w].mean()); orc = r["fx"][orc_w]
        step = max(STEP_MIN, 2 * float(orc.std(ddof=1)) / np.sqrt(len(SEEDS)))
        d_rule = r["eq"].mean() - orc.mean(); d_ref = r["fx"][ref_w].mean() - orc.mean(); d_eqb = r["eqb"].mean() - orc.mean()
        fed1_a &= bool(d_rule < step); fed1_b |= bool(d_ref >= step)
        if r["poisoned"]: fedb = bool(d_eqb < step and d_rule >= step)
        print(f"   node {i} factor {r['fac']:g}{' (poisoned)' if r['poisoned'] else ''}: oracle w {orc_w:g} err {orc.mean():.4f} (step {step:.4f}) | "
              f"global knob {r['fx'][ref_w].mean():.4f} ({d_ref:+.4f}) | rule {r['eq'].mean():.4f} ({d_rule:+.4f}, w_med {r['eq_w']:.1f}) | "
              f"EQ-B {r['eqb'].mean():.4f} ({d_eqb:+.4f}, w_med {r['eqb_w']:.1f})")
        print("      grid " + " ".join(f"{w:g}:{r['fx'][w].mean():.3f}" for w in GRID))
    fed1 = bool(fed1_a and fed1_b)
    if fedb is None:  # no poisoned node: FED-B on the reference node (EQ-B must not be the thing that holds)
        r = res[ref_i]; orc = r["fx"][min(GRID, key=lambda w: r["fx"][w].mean())]
        step = max(STEP_MIN, 2 * float(orc.std(ddof=1)) / np.sqrt(len(SEEDS)))
        fedb = bool(r["eqb"].mean() - orc.mean() < step and r["eq"].mean() - orc.mean() >= step)
    print(f"   FED-1: rule not behind on every node {fed1_a}; global knob behind on some node {fed1_b} -> {'PASS' if fed1 else 'FAIL'}")
    print(f"   FED-B: {'PASS' if fedb else 'FAIL'}")
    return {"FED-1": fed1, "FED-B": fedb}


def main():
    print("FED Phase-A gate (synthetic; theory/checks/fed_heterogeneous.py). Grid " + ", ".join(f"{w:g}" for w in GRID) + f"; seeds {SEEDS}")
    anchors = {s: anchor(s) for s in SEEDS}
    out = {name: run_row(name, spec, anchors) for name, spec in ROWS.items()}
    print("-" * 100)
    viol = 0
    for (stat, row), must in MUST.items():
        got = out[row][stat]; ok = got == must; viol += int(not ok)
        print(f"{stat} on {row}: {'PASS' if got else 'FAIL'} (must {'PASS' if must else 'FAIL'}) -> {'ok' if ok else 'VIOLATION'}")
    print(f"informational: FED-1 on hetero_input {'PASS' if out['hetero_input']['FED-1'] else 'FAIL'}")
    print("GATE OPEN" if viol == 0 else f"GATE CLOSED ({viol} violation(s))")


if __name__ == "__main__":
    main()
