"""Assumption audit: the value of a fixed parameter in the earlier checks (owner request, prompt-log entry 107).
Declared in Adam_SGD/DECLARATION_1.md before the first full run. Synthetic, no data. Every label is computed (R15).

The earlier Adam and SGD checks (Continuous_Learning/checks/adam_checks*.py) compared the Omega rule with a fixed weight
lambda on the two-task quadratic, with the past term's scale multiplied by c. Four choices were made there without being
tested; each is a check here.
  [AS1] Which fixed weight is right in principle. For the noise-free equilibrium of a fixed weight, theta_lambda =
        (H + lambda c F)^-1 (H a + lambda c F b), the objective L_p + c L_q ('imp' reading: c is the past term's true
        importance) is minimised at lambda = 1, and L_p + L_q ('unit' reading: c is a units error) at lambda = 1/c.
        Checked on a fine log grid of lambda at every c.
  [AS2] Which reading and which noise the earlier checks used. The trajectory code here, with the 'imp' reading and the
        noise not scaled by c, must reproduce adam_checks.ev exactly (the rule and one fixed weight at c = 16).
  [AS3] The earlier comparison re-scored under the 'unit' reading with a pure change of units (the noise scaled with c):
        the rule (smoothing 0.9 and 0), the fixed weight tuned on seeds 0-4 at each c and scored on seeds 5-9, and the
        fixed weight tuned at c = 1 deployed unchanged at every c. The rule's invariance is printed (the spread of its
        score across c). [AS3b] the same with the noise not scaled (the earlier noise choice).
  [AS4] Selection bias: under the earlier reading ('imp', noise unscaled), the fine-grid constant's score on the seeds it
        was tuned on against its score on held-out seeds, at c = 1 and 16; the rule on both seed sets.
  [AS5] The step size is a fixed parameter too. Under the earlier reading at c = 16 and c = 256: the fixed weight at its
        in-principle value lambda = 1 with the learning rate tuned on 0.05 x 2^-k (k = 0..10), the rule with the same
        learning-rate grid, and the fixed weight tuned jointly over (lambda, learning rate); all tuned on seeds 0-4 and
        scored on seeds 5-9, 4000 steps.
  [AS6] Tuning cost: trajectories spent by each arm's search.
Run: uv run python Adam_SGD/checks/assumptions.py > Adam_SGD/checks/assumptions.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as cm  # noqa: E402

ROOT = cm.ROOT
sys.path.insert(0, str(ROOT / "Continuous_Learning" / "checks"))
import adam_checks as ac  # noqa: E402

SCALES = (1 / 16, 1.0, 16.0, 256.0)
LR_GRID = tuple(cm.LR * 2.0 ** -k for k in range(11))
LAM_JOINT = tuple(float(v) for v in np.logspace(-4, 1, 21))
TOL = 0.10


def as1(H, F, a, b):
    print("[AS1] The fixed weight that is right in principle (noise-free equilibrium, 2001-point log grid 1e-6 .. 1e3)")
    grid = np.logspace(-6, 3, 2001); ok = True
    for c in SCALES:
        eq = [cm.om.pareto(H, c * F, a, b, l) for l in grid]
        imp = [cm.objective(H, F, a, b, th, c, "imp") for th in eq]; unit = [cm.objective(H, F, a, b, th, c, "unit") for th in eq]
        li = float(grid[int(np.argmin(imp))]); lu = float(grid[int(np.argmin(unit))])
        hi = abs(li - 1) <= 0.02; hu = abs(lu * c - 1) <= 0.02; ok &= hi and hu
        print(f"     c = {c:g}: 'imp' argmin lambda = {li:.4f} (expected 1); 'unit' argmin lambda = {lu:.6g}, times c = {lu * c:.4f} (expected 1)")
    print(f"     AS1 holds (within the grid's 2 %): {ok}")
    return ok


def as2(H, F, a, b):
    print("[AS2] The earlier checks' reading and noise: this code ('imp', noise unscaled) against adam_checks.ev at c = 16")
    ok = True
    for meth, knob, cmeth in (("rule", 1.0, "eq"), ("fixed", 0.03, "fixed")):
        mine = cm.score(meth, knob, H, F, a, b, range(ac.orp.SEEDS), c=16.0, reading="imp", scale_noise=False)
        theirs = ac.ev(cmeth, knob, H, 16.0 * F, a, b)
        same = abs(mine - theirs) <= 1e-9 * max(1.0, abs(theirs)); ok &= same
        print(f"     {meth} {knob:g}: here {mine:.10f}; adam_checks.ev {theirs:.10f}; identical: {same}")
    print(f"     AS2 holds (the earlier checks used the 'imp' reading with unscaled noise): {ok}")
    return ok


def as3(H, F, a, b, scale_noise):
    tag = "AS3" if scale_noise else "AS3b"
    print(f"[{tag}] 'unit' reading, noise {'scaled with c (a pure change of units)' if scale_noise else 'not scaled (the earlier choice)'}: "
          "constants tuned on seeds 0-4, everything scored on seeds 5-9")
    kw = dict(reading="unit", scale_noise=scale_noise)
    lam1 = cm.tune("fixed", cm.FINE, H, F, a, b, cm.TUNE_SEEDS, c=1.0, **kw)[0]
    rules = {0.9: [], 0.0: []}; rows = []
    for c in SCALES:
        lt = cm.tune("fixed", cm.FINE, H, F, a, b, cm.TUNE_SEEDS, c=c, **kw)[0]
        fixed_ho = cm.score("fixed", lt, H, F, a, b, cm.EVAL_SEEDS, c=c, **kw) if lt is not None else float("inf")
        fixed_c1 = cm.score("fixed", lam1, H, F, a, b, cm.EVAL_SEEDS, c=c, **kw)
        r9 = cm.score("rule", 1.0, H, F, a, b, cm.EVAL_SEEDS, c=c, smooth=0.9, **kw)
        r0 = cm.score("rule", 1.0, H, F, a, b, cm.EVAL_SEEDS, c=c, smooth=0.0, **kw)
        rules[0.9].append(r9); rules[0.0].append(r0)
        lab = lambda r: "AHEAD" if r < 1 - TOL else ("BEHIND" if r > 1 + TOL else "TIES")
        rows.append((c, lab(r9 / fixed_ho), lab(r0 / fixed_ho)))
        print(f"     c = {c:g}: constant tuned here {lt if lt is None else f'{lt:.6g}'} -> {cm.f(fixed_ho)}; constant tuned at c = 1 ({lam1:.6g}) deployed here -> {cm.f(fixed_c1)}; "
              f"rule s=0.9 {cm.f(r9)} (/tuned {r9 / fixed_ho:.3f}, {lab(r9 / fixed_ho)}); rule s=0 {cm.f(r0)} (/tuned {r0 / fixed_ho:.3f}, {lab(r0 / fixed_ho)})")
    for s in (0.9, 0.0):
        v = np.array(rules[s]); spread = float((np.nanmax(v) - np.nanmin(v)) / np.nanmean(v)) if np.all(np.isfinite(v)) else float("inf")
        print(f"     rule s={s:g}: relative spread of its score across c = {spread:.3e} -> {'invariant (spread <= 1e-6)' if spread <= 1e-6 else 'not invariant'}")
    return rows


def as4(H, F, a, b):
    print("[AS4] Selection bias under the earlier reading ('imp', noise unscaled): the fine-grid constant on its tuning seeds and on held-out seeds")
    kw = dict(reading="imp", scale_noise=False)
    for c in (1.0, 16.0):
        lt, ins = cm.tune("fixed", cm.FINE, H, F, a, b, cm.TUNE_SEEDS, c=c, **kw)
        ho = cm.score("fixed", lt, H, F, a, b, cm.EVAL_SEEDS, c=c, **kw)
        r_in = cm.score("rule", 1.0, H, F, a, b, cm.TUNE_SEEDS, c=c, **kw); r_ho = cm.score("rule", 1.0, H, F, a, b, cm.EVAL_SEEDS, c=c, **kw)
        print(f"     c = {c:g}: constant {lt:.6g}: tuning seeds {ins:.4f}, held-out seeds {cm.f(ho)} (held-out / tuning {ho / ins:.4f}); "
              f"rule: seeds 0-4 {cm.f(r_in)}, seeds 5-9 {cm.f(r_ho)}; rule / constant: in-sample {r_in / ins:.3f}, held-out {r_ho / ho:.3f}")


def as5(H, F, a, b):
    print("[AS5] The step size is a fixed parameter too ('imp', noise unscaled, 4000 steps; tuned on seeds 0-4, scored on 5-9)")
    kw = dict(reading="imp", scale_noise=False); out = {}
    for c in (16.0, 256.0):
        best1 = (None, float("inf")); bestr = (None, float("inf")); bestj = (None, float("inf"))
        for lr in LR_GRID:
            v1 = cm.score("fixed", 1.0, H, F, a, b, cm.TUNE_SEEDS, c=c, lr=lr, **kw)
            if np.isfinite(v1) and v1 < best1[1]: best1 = (lr, v1)
            vr = cm.score("rule", 1.0, H, F, a, b, cm.TUNE_SEEDS, c=c, lr=lr, **kw)
            if np.isfinite(vr) and vr < bestr[1]: bestr = (lr, vr)
            for lam in LAM_JOINT:
                vj = cm.score("fixed", lam, H, F, a, b, cm.TUNE_SEEDS, c=c, lr=lr, **kw)
                if np.isfinite(vj) and vj < bestj[1]: bestj = ((lam, lr), vj)
        nan = float("nan")
        e1 = cm.score("fixed", 1.0, H, F, a, b, cm.EVAL_SEEDS, c=c, lr=best1[0], **kw) if best1[0] is not None else nan
        er = cm.score("rule", 1.0, H, F, a, b, cm.EVAL_SEEDS, c=c, lr=bestr[0], **kw) if bestr[0] is not None else nan
        er05 = cm.score("rule", 1.0, H, F, a, b, cm.EVAL_SEEDS, c=c, **kw)
        ej = cm.score("fixed", bestj[0][0], H, F, a, b, cm.EVAL_SEEDS, c=c, lr=bestj[0][1], **kw) if bestj[0] is not None else nan
        f05 = cm.tune("fixed", cm.FINE, H, F, a, b, cm.TUNE_SEEDS, c=c, **kw)[0]
        e05 = cm.score("fixed", f05, H, F, a, b, cm.EVAL_SEEDS, c=c, **kw) if f05 is not None else nan
        fmt = lambda x: "none finite" if x is None else (f"({x[0]:.4g}, {x[1]:.6g})" if isinstance(x, tuple) else f"{x:.6g}")
        out[c] = (e1, er, ej)
        print(f"     c = {c:g}: lambda = 1 with lr tuned ({fmt(best1[0])}) -> {cm.f(e1)}; rule with lr tuned ({fmt(bestr[0])}) -> {cm.f(er)}; "
              f"rule at lr 0.05 -> {cm.f(er05)}; fixed lambda tuned at lr 0.05 ({fmt(f05)}) -> {cm.f(e05)}; joint (lambda, lr) = {fmt(bestj[0])} -> {cm.f(ej)}")
        lab = lambda r: "AHEAD" if r < 1 - TOL else ("BEHIND" if r > 1 + TOL else "TIES")
        rr = lambda x, y: (f"{x / y:.3f} -> {lab(x / y)}" if np.isfinite(x) and np.isfinite(y) else "undefined (an arm has no finite setting)")
        print(f"          computed: rule (lr tuned) / lambda = 1 (lr tuned) {rr(er, e1)}; rule (lr tuned) / joint {rr(er, ej)}")
    return out


def main():
    H, F, a, b = cm.om.make_model()
    print("Assumption audit (Adam_SGD/checks/assumptions.py): the two-task quadratic of omega_sweeps.py (d = 5, F = 16 H), SGD lr 0.05, "
          f"4000 steps, noise 0.5; fine grid {len(cm.FINE)} weights {cm.FINE[0]:g} .. {cm.FINE[-1]:g}; tuning seeds {cm.TUNE_SEEDS}, scoring seeds {cm.EVAL_SEEDS}")
    a1 = as1(H, F, a, b); a2 = as2(H, F, a, b)
    as3(H, F, a, b, True); as3(H, F, a, b, False)
    as4(H, F, a, b); as5(H, F, a, b)
    n_fine = len(cm.FINE) * len(cm.TUNE_SEEDS); n_lr = len(LR_GRID) * len(cm.TUNE_SEEDS); n_joint = len(LR_GRID) * len(LAM_JOINT) * len(cm.TUNE_SEEDS)
    print(f"[AS6] Tuning cost in trajectories: fine-grid constant {n_fine}; lambda = 1 with lr tuned {n_lr}; rule with lr tuned {n_lr}; joint (lambda, lr) {n_joint}; rule at a given lr 0")
    print(f"summary: AS1 {'holds' if a1 else 'FAILS'}, AS2 {'holds' if a2 else 'FAILS'}")


if __name__ == "__main__":
    main()
