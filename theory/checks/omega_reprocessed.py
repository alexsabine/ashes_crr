"""H-EQ reprocessed after the cross-verification (owner request 2026-09-22, prompt-log entry 74).
What the cross-verification taught (Continuous_Learning/CROSS_VERIFICATION.md section 4): the rule's one distinct
property is that no number in it carries the past term's units, so its step is bounded by the present step; it is
blind to the shape of the past curvature; it presumes the past gradient's length measures distance from the past;
and it answers a single extreme present batch by amplifying the past step in proportion. Each of those is made a
checkable statement here on the two-task quadratic of omega_sweeps.py, and the enhanced rule that follows from them
(EQ-B, "bounded equanimity": the present gradient clipped at kappa x the largest kept length among its recent batches,
the ratio then taken on the clipped gradient) is run beside the registered rule. Every label is computed (R15).
Pinned: omega_reprocessed.txt.   Run: uv run python theory/checks/omega_reprocessed.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import omega_sweeps as om  # noqa: E402

LR = 0.05; STEPS = 4000; NOISE = 0.5; SEEDS = 5
KAPPA = 2.0; N_HIST = 50; N_MIN = 10          # EQ-B clip: kappa x the largest kept length among the last N_HIST present batches, active once N_MIN are known
POISON_STEP = 2000; POISON = 100.0            # one present batch with its gradient multiplied by POISON
ADAM_LR = 0.01; B1 = 0.9; B2 = 0.999; EPS = 1e-8


def clip_present(g_p, hist, kappa=KAPPA, n_hist=N_HIST, n_min=N_MIN):
    """EQ-B present bound: clip to kappa x the largest KEPT length among the last n_hist present batches (no clip until n_min
    are known). The history holds kept lengths, so a run of extreme batches raises the bound by at most kappa per batch. The
    window maximum, not the median, is the reference: on a softmax stream the median present-gradient length collapses toward
    zero as a task is learned and a median bound clips the informative batches (src/crr/surrogates/battery.py _eqb_clip, AGENT_LOG 63)."""
    n = np.linalg.norm(g_p)
    tau = kappa * float(np.max(hist[-n_hist:])) if len(hist) >= n_min else np.inf
    if n > tau:
        hist.append(tau); return g_p * (tau / n), True, tau
    hist.append(n); return g_p, False, tau


def traj(method, knob, H, F, a, b, seed, lr=LR, steps=STEPS, noise=NOISE, poison=None, optimizer="sgd", record=False, noise_q=None):
    """method: fixed[lambda] | eq[Omega] | eqb[Omega] | fixedclip[lambda]. poison=(step, factor) multiplies that step's
    present gradient. optimizer 'sgd' or 'adam' (the rule applied UPSTREAM of Adam: w multiplies the raw past gradient,
    Adam preconditions the sum). Returns theta, ok, and per-step diagnostics."""
    rng = np.random.default_rng(seed); noise_q = noise if noise_q is None else noise_q
    th = b.copy(); ema_p = ema_q = None; hist = []; m = np.zeros_like(th); v = np.zeros_like(th)
    wlog = []; ratio_raw = []; ratio_ema = []; step_abs = []; clipped = 0; path = []
    for t in range(steps):
        g_p = H @ (th - a) + noise * rng.standard_normal(len(th)); g_q = F @ (th - b) + noise_q * rng.standard_normal(len(th))
        if poison is not None and poison[0] <= t < poison[0] + poison[2]: g_p = poison[1] * g_p
        if method in ("eqb", "fixedclip"):
            g_p, was, _tau = clip_present(g_p, hist); clipped += int(was)
        if method in ("fixed", "fixedclip"):
            w = knob
        else:
            ema_p = g_p if ema_p is None else om.SMOOTH * ema_p + (1 - om.SMOOTH) * g_p
            ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
            w = om.rule_w(ema_p, ema_q, knob)
            ratio_raw.append(np.linalg.norm(g_p + w * g_q) / max(np.linalg.norm(g_p), om.DEN_FLOOR))
            ratio_ema.append(np.linalg.norm(ema_p + w * ema_q) / max(np.linalg.norm(ema_p), om.DEN_FLOOR))
        wlog.append(w)
        step = g_p + w * g_q; step_abs.append(float(np.linalg.norm(step)))
        if optimizer == "adam":
            m = B1 * m + (1 - B1) * step; v = B2 * v + (1 - B2) * step * step
            mh = m / (1 - B1 ** (t + 1)); vh = v / (1 - B2 ** (t + 1))
            th = th - ADAM_LR * mh / (np.sqrt(vh) + EPS)
        else:
            th = th - lr * step
        if record: path.append(th.copy())
        if not np.all(np.isfinite(th)) or np.linalg.norm(th) > 1e6:
            return th, False, dict(w=wlog, ratio_raw=ratio_raw, ratio_ema=ratio_ema, step_abs=step_abs, clipped=clipped, path=path, t_fail=t)
    return th, True, dict(w=wlog, ratio_raw=ratio_raw, ratio_ema=ratio_ema, step_abs=step_abs, clipped=clipped, path=path, t_fail=None)


def evaluate(method, knob, H, F, a, b, **kw):
    tot = []; ok_all = True; Lqs = []
    for s in range(SEEDS):
        th, ok, _ = traj(method, knob, H, F, a, b, s, **kw); ok_all = ok_all and ok
        Lp, Lq = om.losses(H, F, a, b, th) if ok else (np.nan, np.nan); tot.append(Lp + Lq); Lqs.append(Lq)
    return float(np.mean(tot)), ok_all, float(np.mean(Lqs))


GRID = (0.003, 0.01, 0.03, 0.1, 0.3, 0.6, 1.0, 1.2, 1.5, 3.0)


def tuned(method, H, F, a, b, **kw):
    best = None
    for lam in GRID:
        tot, ok, _ = evaluate(method, lam, H, F, a, b, **kw)
        if ok and (best is None or tot < best[1]): best = (lam, tot)
    return best


def main():
    H, F, a, b = om.make_model()
    print("H-EQ reprocessed (2026-09-22, prompt-log entry 74): the two-task quadratic of omega_sweeps.py (d = 5, F 16x H, noise 0.5, lr 0.05, 4000 steps, 5 seeds, start at the past optimum b)")
    print()
    # [1] scale invariance (exact) and shape dependence
    print("[1] The rule is invariant to the SCALE of the past term (exactly, when the past term's noise scales with it) and not to its SHAPE")
    c = 16.0
    perm = np.array([4, 3, 2, 1, 0]); F_perm = np.diag(np.diag(F)[perm])          # same eigenvalues, reassigned to other coordinates
    d_scaled = []; d_fixed = []; d_shape = []
    for s in range(SEEDS):
        thF, okF, dF = traj("eq", 1.0, H, F, a, b, s, record=True)
        thc, okc, dc = traj("eq", 1.0, H, c * F, a, b, s, record=True, noise_q=c * NOISE)     # mini-batch noise of a 16x term is 16x
        thu, oku, du = traj("eq", 1.0, H, c * F, a, b, s, record=True)                        # noise left at 0.5 on both
        thp, okp, _ = traj("eq", 1.0, H, F_perm, a, b, s)
        d_scaled.append(max(np.linalg.norm(p - q) for p, q in zip(dF["path"], dc["path"])) if okF and okc else np.nan)
        d_fixed.append(max(np.linalg.norm(p - q) for p, q in zip(dF["path"], du["path"])) if okF and oku else np.nan)
        d_shape.append(np.linalg.norm(thF - thp) if okF and okp else np.nan)
    d_scaled = float(np.nanmax(d_scaled)); d_fixed = float(np.nanmax(d_fixed)); d_shape = float(np.nanmean(d_shape))
    print(f"     max over steps and seeds of |theta_t(F) - theta_t({c:g}F)| under the rule, past noise scaled with the term: {d_scaled:.3e}  -> {'identical trajectories: w(cF) = w(F)/c exactly, the EMA being linear in g_q' if d_scaled < 1e-9 else 'trajectories differ'}")
    print(f"     the same with the past noise left at {NOISE:g} (not scaled): {d_fixed:.3e}  -> {'the invariance is to the term, not to a noise of fixed size added to it' if d_fixed > 1e-6 else 'identical'}")
    print(f"     mean endpoint distance between F and F with its diagonal reversed (same eigenvalues, other coordinates): {d_shape:.4f}  -> {'the shape of F changes the endpoint; the rule does not see shape' if d_shape > 1e-3 else 'no shape dependence'}")
    print("     consequence: every method that changes the importance estimate (which coordinate is protected how much) composes with the rule and is untouched by it; the 16F test of omega_vs_methods.py measures scale only")
    print()
    # [2] the step bound
    print("[2] The step bound |g_p + w g_q| <= (1 + Omega) |g_p|: on which gradients does it hold, and what does EQ-B add to it?")
    absmax = {}
    for name, meth in (("rule", "eq"), ("EQ-B", "eqb")):
        rr = []; re = []; am = []
        for s in range(SEEDS):
            _, ok, d = traj(meth, 1.0, H, F, a, b, s); rr += d["ratio_raw"]; re += d["ratio_ema"]; am += d["step_abs"]
        rr = np.array(rr); re = np.array(re); absmax[name] = float(np.max(am))
        print(f"     {name:5s} smoothed: max |ema_p + w ema_q| / |ema_p| = {re.max():.4f}, fraction above 2: {float(np.mean(re > 2)):.4f}  -> {'bound holds' if re.max() <= 2 + 1e-9 else 'bound violated on the smoothed gradients'}")
        print(f"     {name:5s} raw:      max |g_p + w g_q| / |g_p| = {rr.max():.4f}, fraction above 2: {float(np.mean(rr > 2)):.4f}, median {np.median(rr):.4f}; max |g_p + w g_q| = {absmax[name]:.4f}")
    print(f"     computed: the ratio bound is a bound on the smoothed pull; the raw ratio exceeds 2 on a fraction of steps for both rules (a small |g_p| in the denominator), and EQ-B {'lowers' if absmax['EQ-B'] < absmax['rule'] else 'does not lower'} the largest raw step ({absmax['EQ-B']:.4f} vs {absmax['rule']:.4f}): what EQ-B bounds is the present gradient's LENGTH (kappa x the largest kept length of its recent batches), hence the absolute step, not the ratio")
    print()
    # [3] a rank-deficient past term (a constraint, not a loss on the past)
    print("[3] Does a past term whose minimum is a SET (rank-deficient F: a constraint on a subspace) break the rule's premise that |g_q| measures distance from the past? (the candidate mechanism for the two-signed LwF control of EQ3-4)")
    F_def = F.copy(); F_def[3, 3] = 0.0; F_def[4, 4] = 0.0
    for name, FF in (("full-rank F", F), ("rank-3 F (two free directions)", F_def)):
        wmax = []; capfrac = []; tot = []; okk = True
        for s in range(SEEDS):
            th, ok, d = traj("eq", 1.0, H, FF, a, b, s); okk = okk and ok
            w = np.array(d["w"]); wmax.append(w.max()); capfrac.append(float(np.mean(w >= om.WCAP)))
            tot.append(sum(om.losses(H, FF, a, b, th)) if ok else np.nan)
        # analytic: fixed points need g_p antiparallel to g_q; with g_q in range(F) that needs H(theta - a) in range(F), which the present optimum a satisfies only if the null-space components of theta - a vanish
        print(f"     {name:32s} max w {np.nanmax(wmax):.4g}, fraction of steps at the cap {np.mean(capfrac):.4f}, finite {okk}, total loss {np.nanmean(tot):.4f}")
    # where does the trajectory go in the free directions?
    drift = []
    for s in range(SEEDS):
        th, ok, _ = traj("eq", 1.0, H, F_def, a, b, s)
        if ok: drift.append(np.abs(th[3:] - a[3:]).max())
    print(f"     free directions under rank-3 F: max |theta - a| over the two free coordinates at the end = {np.mean(drift):.4f} (the present optimum is reached there: the constraint says nothing about them, and the rule's w is driven by the constrained directions only)")
    w_full = [np.median(traj('eq', 1.0, H, F, a, b, s)[2]['w']) for s in range(SEEDS)]; w_def = [np.median(traj('eq', 1.0, H, F_def, a, b, s)[2]['w']) for s in range(SEEDS)]
    set_breaks = abs(np.mean(w_def) - np.mean(w_full)) > 0.05 * np.mean(w_full) or np.mean(capfrac) > 0
    print(f"     median derived w: full-rank {np.mean(w_full):.4f}, rank-3 {np.mean(w_def):.4f}  -> {'the set-valued minimum moves the derived weight: a candidate mechanism' if set_breaks else 'NO: on a quadratic constraint the free directions relax to the present optimum and the derived weight is unchanged; the quadratic model supplies no mechanism for the two-signed LwF control, which stays an empirical statement (EQ3-4) with the softmax non-identifiability argument as the open candidate'}")
    print()
    # [4] the poisoned batch: a sweep over factor and run length; the failure threshold is read off, not chosen
    print("[4] Poisoned present batches (gradient x factor for `run` consecutive steps from step 2000): which rule fails first, and whether EQ-B (present gradient clipped at kappa x the largest kept length of its recent batches) survives")
    t1 = tuned("fixed", H, F, a, b)
    print(f"     clean reference: tuned fixed lambda = {t1[0]:g}, total {t1[1]:.4f}; clean totals: rule {evaluate('eq', 1.0, H, F, a, b)[0]:.4f}, EQ-B {evaluate('eqb', 1.0, H, F, a, b)[0]:.4f}")
    arms = (("fixed", "fixed", t1[0]), ("fixed+clip", "fixedclip", t1[0]), ("rule", "eq", 1.0), ("EQ-B", "eqb", 1.0))
    first_fail = {name: None for name, _, _ in arms}; table = []
    print(f"     {'factor':>7s} {'run':>4s} | " + " | ".join(f"{name:>22s}" for name, _, _ in arms) + "   (total after 4000 steps; DIVERGED if any seed is non-finite; max w of the rule arms)")
    for factor in (10.0, 100.0, 1000.0, 10000.0):
        for run_len in (1, 5):
            cells = []
            for name, meth, knob in arms:
                tot, ok, _ = evaluate(meth, knob, H, F, a, b, poison=(POISON_STEP, factor, run_len))
                wmax = max(max(traj(meth, knob, H, F, a, b, s, poison=(POISON_STEP, factor, run_len))[2]["w"]) for s in range(SEEDS))
                cells.append(f"{tot:10.4f} w<={wmax:8.3g}" if ok else f"{'DIVERGED':>10s} w<={wmax:8.3g}")
                if not ok and first_fail[name] is None: first_fail[name] = (factor, run_len)
            table.append((factor, run_len, cells))
            print(f"     {factor:7g} {run_len:4d} | " + " | ".join(f"{c:>22s}" for c in cells))
    print("     computed: first (factor, run) at which each arm diverges, in sweep order: " + "; ".join(f"{k}: {v if v else 'never'}" for k, v in first_fail.items()))
    clean_tot = {name: evaluate(meth, knob, H, F, a, b)[0] for name, meth, knob in arms}
    first_degrade = {name: None for name, _, _ in arms}
    for factor, run_len, cells in table:
        for (name, _, _), cell in zip(arms, cells):
            bad = cell.strip().startswith("DIVERGED") or float(cell.split()[0]) > 2 * clean_tot[name]
            if bad and first_degrade[name] is None: first_degrade[name] = (factor, run_len)
    print("     computed: first (factor, run) at which each arm's total exceeds twice its clean total (or diverges): " + "; ".join(f"{k}: {v if v else 'never'}" for k, v in first_degrade.items()))
    rule_deg = first_degrade["rule"]; fixed_deg = first_degrade["fixed"]
    print(f"     computed: the registered rule degrades before the tuned fixed weight does: {rule_deg is not None and (fixed_deg is None or rule_deg < fixed_deg)}; EQ-B degrades in the sweep: {first_degrade['EQ-B'] is not None}")
    rule_fails = first_fail["rule"] is not None; eqb_ok = first_fail["EQ-B"] is None; fixed_fails = first_fail["fixed"] is not None
    print(f"     computed: the registered rule has a poison threshold in this sweep: {rule_fails}; EQ-B survives the whole sweep: {eqb_ok}; the tuned fixed weight has a threshold: {fixed_fails}"
          + (f"; the rule fails where the fixed weight does not: {rule_fails and (not fixed_fails or first_fail['rule'] < first_fail['fixed'])}" if rule_fails else ""))
    eqb_c = evaluate('eqb', 1.0, H, F, a, b)[0]; eq_c = evaluate('eq', 1.0, H, F, a, b)[0]
    print(f"     computed: on the clean stream EQ-B is within 1 % of the registered rule: {abs(eqb_c - eq_c) <= 0.01 * eq_c} (totals {eqb_c:.4f} vs {eq_c:.4f}); the bound is {'idle on the clean stream' if abs(eqb_c - eq_c) <= 0.01 * eq_c else 'NOT idle on the clean stream'}")
    print()
    # [5] the Fisher-norm ratio (H-EQ as written) has the same fixed-point set
    print("[5] The Fisher-norm ratio of H-EQ as written (|.|_F^-1 on both gradients) has the same fixed-point set as the Euclidean one: any positive scalar w needs g_p antiparallel to g_q, i.e. theta on the Pareto curve")
    Finv = np.linalg.inv(F)
    def fnorm(g): return float(np.sqrt(g @ Finv @ g))
    ends = []
    for s in range(SEEDS):
        rng = np.random.default_rng(s); th = b.copy(); ema_p = ema_q = None
        for t in range(STEPS):
            g_p = H @ (th - a) + NOISE * rng.standard_normal(5); g_q = F @ (th - b) + NOISE * rng.standard_normal(5)
            ema_p = g_p if ema_p is None else om.SMOOTH * ema_p + (1 - om.SMOOTH) * g_p
            ema_q = g_q if ema_q is None else om.SMOOTH * ema_q + (1 - om.SMOOTH) * g_q
            w = min(fnorm(ema_p) / max(fnorm(ema_q), om.DEN_FLOOR), om.WCAP)
            th = th - LR * (g_p + w * g_q)
        ends.append(th)
    lams = np.logspace(-3, 3, 601)
    def lam_of(th):
        j = int(np.argmin([np.linalg.norm(th - om.pareto(H, F, a, b, l)) for l in lams])); return lams[j], np.linalg.norm(th - om.pareto(H, F, a, b, lams[j]))
    eu = [lam_of(traj("eq", 1.0, H, F, a, b, s)[0]) for s in range(SEEDS)]; fi = [lam_of(th) for th in ends]
    print(f"     Euclidean ratio: nearest Pareto lambda {np.mean([e[0] for e in eu]):.4f} at distance {np.mean([e[1] for e in eu]):.4f} | Fisher ratio: lambda {np.mean([f[0] for f in fi]):.4f} at distance {np.mean([f[1] for f in fi]):.4f}")
    print(f"     computed: both endpoints sit within 0.2 of the curve: {all(e[1] < 0.2 for e in eu) and all(f[1] < 0.2 for f in fi)}; the metric moves the stopping point along the curve, it does not change the set (A1's metric is a choice of stopping point, not of mechanism)")
    print()
    # [6] Adam
    print("[6] Under Adam (the rule upstream of the preconditioner) the divergence edge disappears for every method and the scale test becomes a question of endpoint quality")
    tA = tuned("fixed", H, F, a, b, optimizer="adam"); tA16 = tuned("fixed", H, 16 * F, a, b, optimizer="adam")
    print(f"     tuned fixed lambda under Adam: {tA[0]:g} (total {tA[1]:.4f}) at F; {tA16[0]:g} (total {tA16[1]:.4f}) at 16F")
    res = {}
    for name, meth, knob in (("fixed lambda (tuned at F)", "fixed", tA[0]), ("rule Omega = 1", "eq", 1.0), ("EQ-B Omega = 1", "eqb", 1.0)):
        r1 = evaluate(meth, knob, H, F, a, b, optimizer="adam"); r16 = evaluate(meth, knob, H, 16 * F, a, b, optimizer="adam")
        res[name] = (r1[0] / tA[1], r16[0] / tA16[1], r1[1], r16[1])
        print(f"     {name:26s} F: total {r1[0]:.4f} (/tuned {r1[0] / tA[1]:.3f}, finite {r1[1]}) | 16F, same knob: total {r16[0]:.4f} (/tuned {r16[0] / tA16[1]:.3f}, finite {r16[1]})")
    robust = [k for k, v in res.items() if v[2] and v[3] and v[0] <= 1.10 and v[1] <= 1.10]
    adam_fixed_robust = "fixed lambda (tuned at F)" in robust
    print(f"     computed: scale-robust under Adam (within 10 % of the Adam-tuned fixed weight at both scales): {robust}; every arm finite: {all(v[2] and v[3] for v in res.values())}")
    print(f"     computed: {'the fixed weight is scale-robust under Adam too: the rule has no scale advantage under Adam in this model, its property is an SGD property' if adam_fixed_robust else 'the fixed weight is not scale-robust under Adam; the rule keeps its advantage'}")
    print()
    print("[7] What changes in H-EQ (proposal for the v3.2 list; theory/CRR.md is not edited here), each line conditional on the numbers above:")
    print(f"     (a) scope: {'a set-valued past minimum moves the derived weight ([3]): constraints are outside the clause by mechanism' if set_breaks else 'the quadratic model gives NO mechanism for excluding constraint terms ([3]); the narrowing of H-EQ to losses on the past rests on EQ3-4 (empirical, two-signed) and is stated as an empirical scope, not a derived one'};")
    print("     (b) the bound is the mechanism ([2]): the claim is 'the past pull never exceeds (1 + Omega) x the present pull in the smoothed gradients', not 'equal pull is optimal' (omega_sweeps.txt [1]-[2]);")
    print(f"     (c) present bound: {'the registered rule degrades at poison ' + str(rule_deg) + ' (diverges at ' + str(first_fail['rule']) + ') where EQ-B ' + ('survives the whole sweep' if first_degrade['EQ-B'] is None else 'degrades too') + ' ([4]); EQ-B is the enhancement to test, with the poisoned stream as its positive control and the clean stream as its negative control (the bound must be idle there)' if rule_deg is not None else 'no poison in the sweep degrades the registered rule ([4]); EQ-B has no positive control in this model and would need one before any prereg'};")
    print(f"     (d) the metric is a stopping point on the Pareto curve, not a mechanism ([5]); (e) the optimiser is a registered parameter ([6]){', and under Adam the fixed weight is scale-robust too, so the scale claim is SGD-only' if adam_fixed_robust else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
