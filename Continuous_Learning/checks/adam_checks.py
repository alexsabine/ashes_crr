"""Why the rule's advantage vanishes under Adam, and where it returns (owner request, prompt-log entry 104).
Declared in Continuous_Learning/DECLARATION_ADAM.md before the first full run. Synthetic, no data: the two-task quadratic
of theory/checks/omega_sweeps.py (d = 5, F = 16 H, noise 0.5, 4000 steps, 5 seeds, start at the past optimum b), reusing
the trajectory code of theory/checks/omega_reprocessed.py unchanged. The past term's curvature is scaled by c in
{1/16, 1, 16, 256} (the "units" of the past term); the evaluation is the total L_p + L_q at that scale.

    [A1] Adam is invariant to rescaling the WHOLE gradient (Kingma and Ba's property): both terms and their noise times c.
    [A2] The stability edge: under SGD a fixed lambda diverges beyond an edge that moves as 1/c; under Adam (the past pull
         inside the preconditioner, "coupled") no lambda on the grid diverges at any c.
    [A3] Under coupled Adam the fixed lambda tuned at c = 1 stays within 10 % of the Adam-tuned fixed weight at every c.
    [A4] Under SGD the rule's advantage over the tuned fixed weight appears exactly where the edge falls below lambda = 1
         (the summed-loss weight, optimal for the total at every c), and not where the edge is above it.
    [A5] Decoupled application (AdamW-style): the present gradient through Adam, the past pull applied outside it,
         theta <- theta - ADAM_LR * u(g_p) - LR_Q * w * g_q. The edge returns for the fixed weight; the decoupled rule,
         w = Omega * ||EMA of the applied present step|| / (LR_Q * ||EMA of g_q||), is finite at every c.
    [A6] Poison under Adam: five present batches x 1000 at step 2000. Adam's second moment absorbs them.
    [A7] The gradient-ratio family (prior art): a VQGAN-style ratio (instantaneous norms, additive delta 1e-4, no smoothing)
         and a max/mean ratio with the weight smoothed (EMA 0.9 on w) are finite at every c under SGD, as the rule is.
    [A8] Heavy-ball momentum (beta 0.9, step LR x (1 - beta) so the long-run step matches SGD's): the fixed weight's edge
         exists (lambda* = (2 (1 + beta) / lr_m - h_max) / f_max, Polyak's quadratic bound) and moves as 1/c; the rule at
         Omega = 1 is finite at every c. The rule's advantage is then a property of the step-size family, not of plain SGD.
Every label is computed from the numbers (R15). Run:
    uv run python Continuous_Learning/checks/adam_checks.py > Continuous_Learning/checks/adam_checks.txt
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "theory" / "checks"))
import omega_reprocessed as orp  # noqa: E402
import omega_sweeps as om  # noqa: E402

SCALES = (1 / 16, 1.0, 16.0, 256.0)
LR_Q = orp.LR                     # the step of a decoupled past pull: the SGD learning rate (named choice)
DELTA_VQ = 1e-4                   # VQGAN-style additive guard
ALPHA_W = 0.9                     # EMA on the weight for the max/mean variant
TOL = 0.10                        # "within 10 %" as in omega_vs_methods
POISON = (2000, 1000.0, 5)
BETA_M = 0.9                      # heavy-ball momentum
LR_M = orp.LR * (1 - BETA_M)      # momentum step with the same long-run step as SGD (named choice)


def adam_step(state, step, t):
    m, v = state
    m = orp.B1 * m + (1 - orp.B1) * step; v = orp.B2 * v + (1 - orp.B2) * step * step
    mh = m / (1 - orp.B1 ** (t + 1)); vh = v / (1 - orp.B2 ** (t + 1))
    return (m, v), mh / (np.sqrt(vh) + orp.EPS)


def traj_x(method, knob, H, F, a, b, seed, optimizer="sgd", poison=None, noise_q=None):
    """Variants not in omega_reprocessed.traj: decoupled application under Adam, and the two prior-art ratio rules.
    method: dfixed / deq (decoupled fixed / decoupled rule, Adam), vq (VQGAN-style), maxmean (max/mean with EMA on w),
    mfixed / meq (heavy-ball momentum with a fixed weight / the rule at Omega = knob)."""
    rng = np.random.default_rng(seed); nq = orp.NOISE if noise_q is None else noise_q
    th = b.copy(); st = (np.zeros_like(th), np.zeros_like(th)); ema_u = ema_q = None; w_s = None; vel = np.zeros_like(th)
    for t in range(orp.STEPS):
        g_p = H @ (th - a) + orp.NOISE * rng.standard_normal(len(th)); g_q = F @ (th - b) + nq * rng.standard_normal(len(th))
        if poison is not None and poison[0] <= t < poison[0] + poison[2]: g_p = poison[1] * g_p
        if method in ("dfixed", "deq"):
            st, u = adam_step(st, g_p, t); d_p = orp.ADAM_LR * u
            if method == "dfixed":
                w = knob
            else:
                ema_u = d_p if ema_u is None else om.SMOOTH * ema_u + (1 - om.SMOOTH) * d_p
                ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
                w = min(knob * np.linalg.norm(ema_u) / max(LR_Q * np.linalg.norm(ema_q), om.DEN_FLOOR), om.WCAP)
            th = th - d_p - LR_Q * w * g_q
        elif method in ("mfixed", "meq"):
            if method == "mfixed":
                w = knob
            else:
                ema_u = g_p if ema_u is None else om.SMOOTH * ema_u + (1 - om.SMOOTH) * g_p
                ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
                w = om.rule_w(ema_u, ema_q, knob)
            vel = BETA_M * vel + (g_p + w * g_q); th = th - LR_M * vel
        else:
            if method == "vq":
                w = knob * np.linalg.norm(g_p) / (np.linalg.norm(g_q) + DELTA_VQ)
            else:
                w_hat = knob * np.max(np.abs(g_p)) / max(np.mean(np.abs(g_q)), om.DEN_FLOOR)
                w_s = w_hat if w_s is None else (1 - ALPHA_W) * w_s + ALPHA_W * w_hat
                w = w_s
            w = min(w, om.WCAP); step = g_p + w * g_q
            if optimizer == "adam":
                st, u = adam_step(st, step, t); th = th - orp.ADAM_LR * u
            else:
                th = th - orp.LR * step
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6: return th, False
    return th, True


def ev(method, knob, H, F, a, b, **kw):
    """Mean total over seeds; nan if any seed diverges."""
    tots = []
    for s in range(orp.SEEDS):
        if method in ("fixed", "eq", "eqb", "fixedclip"):
            th, ok, _ = orp.traj(method, knob, H, F, a, b, s, **kw)
        else:
            th, ok = traj_x(method, knob, H, F, a, b, s, **kw)
        if not ok: return float("nan")
        Lp, Lq = om.losses(H, F, a, b, th); tots.append(Lp + Lq)
    return float(np.mean(tots))


def tune(method, H, F, a, b, **kw):
    best = (None, float("inf"))
    for lam in orp.GRID:
        v = ev(method, lam, H, F, a, b, **kw)
        if np.isfinite(v) and v < best[1]: best = (lam, v)
    return best


def f(v): return "diverges" if not np.isfinite(v) else f"{v:.4f}"


def main():
    H, F, a, b = om.make_model()
    print("Adam checks (Continuous_Learning/checks/adam_checks.py): the two-task quadratic, d = 5, F = 16 H, 4000 steps, 5 seeds; "
          f"SGD lr {orp.LR}, Adam lr {orp.ADAM_LR} (b1 {orp.B1}, b2 {orp.B2}, eps {orp.EPS}); past scale c in {[round(c, 4) for c in SCALES]}")
    # [A1]
    print("[A1] Adam is invariant to rescaling the whole gradient (both terms and their noise times c)")
    th0, _, _ = orp.traj("fixed", 1.0, H, F, a, b, 0, optimizer="adam")
    dmax = []
    for c in SCALES:
        th, _, _ = orp.traj("fixed", 1.0, c * H, c * F, a, b, 0, optimizer="adam", noise=orp.NOISE * c, noise_q=orp.NOISE * c)
        d = float(np.max(np.abs(th - th0))); dmax.append(d); print(f"     c = {c:g}: max |theta_c - theta_1| = {d:.3e}")
    a1 = max(dmax) <= 1e-6; print(f"     A1 holds (<= 1e-6): {a1}")
    # [A2]
    print("[A2] Divergence of the fixed weight over the grid, per scale: SGD against coupled Adam (lambda values that diverge)")
    edge_sgd = {}; a2_sgd_moves = True; a2_adam_none = True
    for c in SCALES:
        Fc = c * F
        div_s = [lam for lam in orp.GRID if not np.isfinite(ev("fixed", lam, H, Fc, a, b))]
        div_a = [lam for lam in orp.GRID if not np.isfinite(ev("fixed", lam, H, Fc, a, b, optimizer="adam"))]
        lam_star = (2 / orp.LR - np.max(np.diag(H))) / np.max(np.diag(Fc)); edge_sgd[c] = lam_star
        print(f"     c = {c:g}: SGD edge lambda* = {lam_star:.4f}; SGD diverges at {div_s}; Adam diverges at {div_a}")
        a2_adam_none &= not div_a
    a2 = a2_adam_none and any(edge_sgd[c] < 1 for c in SCALES) and any(edge_sgd[c] > 1 for c in SCALES)
    print(f"     A2 holds (the SGD edge crosses lambda = 1 across scales; Adam diverges nowhere): {a2}")
    # [A3] and [A4]
    print("[A3/A4] Totals per scale: tuned fixed weight (SGD, Adam), the fixed weight tuned at c = 1 kept, the rule at Omega = 1")
    t1_sgd = tune("fixed", H, F, a, b); t1_adam = tune("fixed", H, F, a, b, optimizer="adam")
    a3 = True; a4 = True
    for c in SCALES:
        Fc = c * F
        ts = tune("fixed", H, Fc, a, b); ta = tune("fixed", H, Fc, a, b, optimizer="adam")
        keep_a = ev("fixed", t1_adam[0], H, Fc, a, b, optimizer="adam"); keep_s = ev("fixed", t1_sgd[0], H, Fc, a, b)
        rule_s = ev("eq", 1.0, H, Fc, a, b); rule_a = ev("eq", 1.0, H, Fc, a, b, optimizer="adam")
        ka = keep_a / ta[1] if np.isfinite(keep_a) else float("inf")
        adv = rule_s / ts[1]
        print(f"     c = {c:g}: SGD tuned lambda {ts[0]:g} total {ts[1]:.4f}; kept lambda {t1_sgd[0]:g} {f(keep_s)}; rule {f(rule_s)} (rule/tuned {adv:.3f}) | "
              f"Adam tuned lambda {ta[0]:g} total {ta[1]:.4f}; kept lambda {t1_adam[0]:g} {f(keep_a)} (kept/tuned {ka:.3f}); rule {f(rule_a)} (rule/tuned {rule_a / ta[1]:.3f})")
        a3 &= ka <= 1 + TOL
        edge_below = edge_sgd[c] < 1.0
        a4 &= (adv < 1 - TOL) if edge_below else (adv >= 1 - TOL)
    print(f"     A3 holds (the Adam fixed weight tuned at c = 1 within 10 % of the Adam-tuned weight at every c): {a3}")
    print(f"     A4 holds (under SGD the rule is ahead by more than 10 % exactly at the scales whose edge is below lambda = 1): {a4}")
    # [A5]
    print("[A5] Decoupled application (the past pull outside Adam, step LR_Q = %g)" % LR_Q)
    td1 = tune("dfixed", H, F, a, b); a5_edge = False; a5_rule = True
    for c in SCALES:
        Fc = c * F
        keep = ev("dfixed", td1[0], H, Fc, a, b); one = ev("dfixed", 1.0, H, Fc, a, b); rule = ev("deq", 1.0, H, Fc, a, b); tdc = tune("dfixed", H, Fc, a, b)
        div = [lam for lam in orp.GRID if not np.isfinite(ev("dfixed", lam, H, Fc, a, b))]
        print(f"     c = {c:g}: decoupled fixed tuned lambda {tdc[0]} total {f(tdc[1]) if tdc[0] is not None else 'none finite'}; lambda tuned at c = 1 ({td1[0]:g}) {f(keep)}; "
              f"lambda = 1 {f(one)}; diverges at {div}; decoupled rule {f(rule)}")
        a5_edge |= bool(div); a5_rule &= bool(np.isfinite(rule))
    print(f"     A5 holds (the edge returns for the decoupled fixed weight at some scale, and the decoupled rule is finite at every scale): {a5_edge and a5_rule}")
    # [A6]
    print("[A6] Poison (5 present batches x 1000 at step 2000), c = 1: clean and poisoned totals")
    rows = {}
    for opt in ("sgd", "adam"):
        for meth, knob in (("fixed", t1_sgd[0] if opt == "sgd" else t1_adam[0]), ("eq", 1.0), ("eqb", 1.0)):
            cl = ev(meth, knob, H, F, a, b, optimizer=opt); po = ev(meth, knob, H, F, a, b, optimizer=opt, poison=POISON)
            rows[(opt, meth)] = (cl, po); print(f"     {opt:4s} {meth:5s} clean {f(cl)} poisoned {f(po)}" + (f" (ratio {po / cl:.3f})" if np.isfinite(po) else ""))
    rs = rows[("adam", "eq")]; ra = rows[("adam", "eqb")]
    a6a = np.isfinite(rs[1]) and rs[1] <= 2 * rs[0]
    a6b = np.isfinite(ra[1]) and abs(rs[1] - ra[1]) <= TOL * ra[1]
    print(f"     A6a holds (under Adam the poisoned rule stays within 2x of its clean total): {a6a}")
    print(f"     A6b holds (under Adam EQ-B and the rule are within 10 % of each other under poison): {a6b}")
    # [A7]
    print("[A7] The gradient-ratio family under SGD: finite at every scale?  total per scale (ratio to the SGD-tuned fixed weight)")
    a7 = True
    for meth, name in (("eq", "the rule (EMA of gradient vectors, L2 norms)"), ("vq", "VQGAN-style (instantaneous L2 norms, + delta)"), ("maxmean", "max/mean ratio, weight smoothed")):
        vals = []
        for c in SCALES:
            Fc = c * F; v = ev(meth, 1.0, H, Fc, a, b); ts = tune("fixed", H, Fc, a, b); vals.append((c, v, v / ts[1] if np.isfinite(v) else float("inf")))
        a7 &= all(np.isfinite(v) for _, v, _ in vals)
        print(f"     {name:48s} " + "; ".join(f"c = {c:g}: {f(v)} ({r:.3f})" for c, v, r in vals))
    print(f"     A7 holds (every member of the family finite at every scale under SGD): {a7}")
    # [A8]
    print("[A8] Heavy-ball momentum (beta %g, step %g): the fixed weight's edge and the rule, per scale" % (BETA_M, LR_M))
    edge_m = {}; a8_rule = True; a8_div = True
    for c in SCALES:
        Fc = c * F
        lam_m = (2 * (1 + BETA_M) / LR_M - np.max(np.diag(H))) / np.max(np.diag(Fc)); edge_m[c] = lam_m
        div = [lam for lam in orp.GRID if not np.isfinite(ev("mfixed", lam, H, Fc, a, b))]
        tm = tune("mfixed", H, Fc, a, b); rule = ev("meq", 1.0, H, Fc, a, b)
        print(f"     c = {c:g}: edge lambda* = {lam_m:.4f}; diverges at {div}; tuned lambda {tm[0]} total {f(tm[1]) if tm[0] is not None else 'none finite'}; "
              f"rule {f(rule)}" + (f" (rule/tuned {rule / tm[1]:.3f})" if tm[0] is not None and np.isfinite(rule) else ""))
        a8_rule &= bool(np.isfinite(rule))
        a8_div &= all(lam > lam_m for lam in div) and all(lam <= lam_m or lam in div for lam in orp.GRID)
    a8 = a8_rule and a8_div and any(bool([l for l in orp.GRID if l > edge_m[c]]) for c in SCALES)
    print(f"     A8 holds (the momentum edge predicts the divergent grid points at every scale, some scale has one, and the rule is finite at every scale): {a8}")
    print("summary: " + ", ".join(f"{k} {'holds' if v else 'FAILS'}" for k, v in (("A1", a1), ("A2", a2), ("A3", a3), ("A4", a4), ("A5", a5_edge and a5_rule), ("A6a", a6a), ("A6b", a6b), ("A7", a7), ("A8", a8))))


if __name__ == "__main__":
    main()
