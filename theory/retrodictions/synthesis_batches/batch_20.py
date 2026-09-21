"""Synthesis batch 20: rows 96-100 of QUEUE.md (prompt-log entry 61).
twenty [17] (DESCR) the spacing effect (ACT-R with Pavlik-Anderson activation-dependent decay): H-T1 read on the activation
    trajectory, path against endpoint, with the practice count controlled (the ARC-T1b lesson).
twenty [18] (DESCR) cobweb model: suppliers who expect the P3 age-weighted mean of settled prices (A6) instead of last period's.
twenty [19] (DESCR) RHEED oscillations: H-T1 read on the damping of the oscillation, path grown against the present surface.
emptiness [1] (DESCR) the empty occasion: every CRR-proper ingredient tried on a carrier that does not move.
emptiness [2] (DESCR) the cut as a Dirac delta in phase: its mass against the clock.

Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data file is
opened (R2). The source rows' models are re-implemented (nothing imported from theory/retrodictions/*.py).
Deterministic: fixed seeds, fixed grids, fixed steps.
Run:  uv run python theory/retrodictions/synthesis_batches/batch_20.py
"""
import math
import sys

import numpy as np
from scipy.stats import spearmanr

from crr.instrument.core import antipodal_cuts, intrinsic_phase, kl_gauss, path_length, peak_cuts, regularity, rho, surplus, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC_T = "theory/retrodictions/twenty_systems.txt"
SRC_E = "theory/retrodictions/emptiness.txt"


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


def yn(ok):
    return "yes" if ok else "no"


def _r2_fit(ytr, xtr, yte, xte):
    """Linear fit on the training pairs, R^2 scored on the test pairs (held-out; sign of the slope is fitted)."""
    A = np.c_[xtr, np.ones(len(xtr))]
    coef, *_ = np.linalg.lstsq(A, ytr, rcond=None)
    pred = np.c_[xte, np.ones(len(xte))] @ coef
    return float(1.0 - ((yte - pred) ** 2).sum() / ((yte - yte.mean()) ** 2).sum())


def _r2(y, x):
    return _r2_fit(y, x, y, x)


def _resid(v, z):
    A = np.c_[z, np.ones(len(z))]
    coef, *_ = np.linalg.lstsq(A, v, rcond=None)
    return v - A @ coef


# ---------------------------------------------------------------- 1 (learn) the spacing effect: path vs endpoint, n controlled
def _pa_decays(times, c=0.277, a=0.177):
    """Pavlik-Anderson: practice j gets decay d_j = c exp(m_j) + a, m_j the activation at the moment of practice j."""
    d = []
    for j, tj in enumerate(times):
        if j == 0:
            d.append(a)
        else:
            m = math.log(sum((tj - ti) ** (-di) for ti, di in zip(times[:j], d)))
            d.append(c * math.exp(m) + a)
    return d


def _act(times, d, t):
    return math.log(sum((t - tj) ** (-dj) for tj, dj in zip(times, d) if t > tj))


def spacing_effect():
    week = 7 * 24 * 60.0; delta = 1.0; ns = (2, 4, 8); gaps = (1, 3, 10, 30, 100, 300, 1000, 3000); per_int = 2000
    rec = []
    for n in ns:
        for gi, g in enumerate(gaps):
            times = [k * float(g) for k in range(n)]; d = _pa_decays(times)
            test = _act(times, d, times[-1] + week); end = _act(times, d, times[-1] + delta)
            pre = float(np.mean([_act(times, d, tj) for tj in times[1:]]))
            ts = [np.linspace(times[j] + delta, times[j + 1], per_int, endpoint=False) for j in range(n - 1)]
            ts.append(np.array([times[-1] + delta])); ts = np.concatenate(ts)
            m = np.array([_act(times, d, t) for t in ts])
            C = float(np.abs(np.diff(m)).sum()); Cs = abs(float(m[-1] - m[0]))
            rec.append(dict(n=n, gi=gi, g=g, test=test, end=end, pre=pre, C=C, S=C - Cs, lnn=math.log(n)))
    R = {k: np.array([r[k] for r in rec]) for k in rec[0]}
    y = R["test"]; tr = R["gi"] % 2 == 0; te = ~tr
    keys = ("C", "S", "end", "pre")
    pooled = {k: _r2_fit(y[tr], R[k][tr], y[te], R[k][te]) for k in keys}
    yr = _resid(y, R["lnn"]); ctrl = {k: _r2_fit(yr[tr], _resid(R[k], R["lnn"])[tr], yr[te], _resid(R[k], R["lnn"])[te]) for k in keys}
    per_n = {}
    for n in ns:
        s = R["n"] == n
        per_n[n] = dict(r2={k: _r2_fit(y[s & tr], R[k][s & tr], y[s & te], R[k][s & te]) for k in keys},
                        rho={k: float(spearmanr(y[s], R[k][s]).statistic) for k in ("C", "end")})
    # the source's two schedules, reproduced
    massed = [k * 1.0 for k in range(8)]; spaced = [k * 24 * 60.0 for k in range(8)]
    A_m = _act(massed, _pa_decays(massed), massed[-1] + week); A_s = _act(spaced, _pa_decays(spaced), spaced[-1] + week)
    crr, null = ctrl["C"], ctrl["end"]
    end_per_n = ", ".join(f"{per_n[n]['r2']['end']:.4f}" for n in ns); c_per_n = ", ".join(f"{per_n[n]['r2']['C']:.4f}" for n in ns)
    close_per_n = all(abs(per_n[n]["r2"]["end"] - per_n[n]["r2"]["C"]) < 0.05 for n in ns)
    e = {(r["n"], r["g"]): r["end"] for r in rec}
    end_rises_n = all(e[(8, g)] > e[(2, g)] for g in gaps); end_falls_g = all(e[(n, 3000)] < e[(n, 1)] for n in ns)
    ret_rises_g = all(rec_["test"] > rec_prev["test"] for rec_prev, rec_ in zip(rec, rec[1:]) if rec_["n"] == rec_prev["n"])
    pooled_win = pooled["C"] >= pooled["end"] + 0.05
    ctrl_win = crr >= null + 0.05
    per_n_win = all(per_n[n]["r2"]["C"] >= per_n[n]["r2"]["end"] + 0.05 for n in ns)
    check = ctrl_win and per_n_win
    out = outcome(crr=crr, null=null, domain=None, check=check)
    return make_row("learn", "The spacing effect in ACT-R with the Pavlik-Anderson activation-dependent decay (c = 0.277, a = 0.177; the source's model): 24 schedules, n in {2, 4, 8} practices at gaps of 1, 3, 10, 30, 100, 300, 1000, 3000 min, retention = activation one week after the last practice; the activation trajectory m(t) = ln sum_j (t - t_j)^-d_j sampled 2000 points per interval from 1 min after each practice; predictors fitted on the schedules with gaps 1, 10, 100, 1000 min and scored on those with gaps 3, 30, 300, 3000 min (held-out); ln n partialled out of retention and predictor over all 24 schedules before the split",
                    source=f"{SRC_T} [17] (DESCR)",
                    Q="retention at test tracks the path of the activation trajectory over the practice schedule (its total variation C, D6) rather than the endpoint (the activation just after the last practice), with the number of practices controlled, as H-T1 states for learners",
                    ingredient="D6/H-T1 (path against endpoint, the practice count in the role of the learning rate: controlled by residualising on ln n and by scoring within each n), D5 (occasion = one inter-practice interval)",
                    null="the endpoint: the activation 1 min after the last practice (the state at the end of learning), the same fit and the same held-out schedules",
                    domain="Pavlik & Anderson 2005 (activation-dependent decay: a trace laid down at high activation decays faster) and Anderson & Schooler 1991 (base-level learning); the domain's rule reads the state at each practice, not a path. Named only, not fetched (R10)",
                    numbers=f"source schedules reproduced: massed (8 x 1 min) {A_m:.3f}, spaced (8 x 1 day) {A_s:.3f} ({'spaced' if A_s > A_m else 'massed'} higher); endpoint activation at gap 1 min: n = 2 {e[(2, 1)]:.3f}, n = 8 {e[(8, 1)]:.3f}; at gap 3000 min: n = 2 {e[(2, 3000)]:.3f}, n = 8 {e[(8, 3000)]:.3f} (it {'rises' if end_rises_n else 'does not rise'} with n at every gap and {'falls' if end_falls_g else 'does not fall'} with the gap at every n, while retention {'rises' if ret_rises_g else 'does not rise'} with the gap at every n); held-out R^2 pooled over all 24 schedules: C {pooled['C']:.4f}, S {pooled['S']:.4f}, endpoint {pooled['end']:.4f}, mean activation at practice (the domain's state) {pooled['pre']:.4f}; with ln n partialled out: C {ctrl['C']:.4f}, S {ctrl['S']:.4f}, endpoint {ctrl['end']:.4f}, state at practice {ctrl['pre']:.4f}; "
                            + "; ".join(f"n = {n}: held-out R^2 C {per_n[n]['r2']['C']:.4f}, S {per_n[n]['r2']['S']:.4f}, endpoint {per_n[n]['r2']['end']:.4f}, state at practice {per_n[n]['r2']['pre']:.4f}; Spearman(C, retention) {per_n[n]['rho']['C']:+.3f}, Spearman(endpoint, retention) {per_n[n]['rho']['end']:+.3f}" for n in ns),
                    tg=f"held-out R^2 of the path {crr:.4f} vs null (endpoint) {null:.4f}, ln n partialled out: {ag(crr, null)}",
                    tn="none cited: the domain's rule is a per-practice decay rule, not a theorem for a path's R^2 (it passes vacuously)",
                    tc=f"path ahead of the endpoint by >= 0.05 pooled and uncontrolled: {yn(pooled_win)}; with ln n partialled out: {yn(ctrl_win)}; within every n: {yn(per_n_win)}: {hf(check)}",
                    out=out,
                    reading=f"uncontrolled, the path is {'ahead' if pooled_win else 'not ahead'} ({pooled['C']:.4f} against {pooled['end']:.4f}) and the lead is the practice count: more practices lengthen the path and raise retention while the endpoint activation {'rises' if end_rises_n else 'does not rise'} with n and {'falls' if end_falls_g else 'does not fall'} with the gap, so the pooled endpoint fit is scrambled. With the count controlled the endpoint predicts retention {'better than' if null > crr else 'no worse than'} the path ({null:.4f} against {crr:.4f}; within each n the endpoint's held-out R^2 is {end_per_n} against the path's {c_per_n}, {'within 0.05 of each other in every n' if close_per_n else 'not within 0.05 in every n'}), and it predicts it {'backwards' if per_n[8]['rho']['end'] < 0 else 'forwards'} (Spearman {per_n[8]['rho']['end']:+.3f} at n = 8): the higher the activation at the end of the session, the less is kept a week later. That backwards endpoint is the spacing effect as the domain states it (a trace laid down at high activation decays faster), so the ARC-T1b lesson repeats on this carrier: the path beat the wrong comparison, and once the count is controlled H-T1's claim {hf(check)}. The source row's 'a regeneration rule the framework does not have' stands; the synthesis reading is {out}",
                    weakness="the practice count plays the role of the learning rate by analogy, and the control (partialling out ln n; scoring within n) is this row's choice; 24 schedules on one decay parameter pair; the path is sampled from 1 min after each practice because the model's activation diverges at the practice itself, so C depends on that offset (a named constant, not swept here); no data (retention experiments with recorded schedules, none opened, none in data/SEEN.md)",
                    elegance="How well you feel you know something at the end of a session predicts how much you will keep a week later, but backwards; spreading the same practice out makes each session feel harder and the memory last longer. One sentence, no knobs, and it is the endpoint that carries it, not the path.",
                    child="If you practise the same thing eight times in a row, it feels really easy by the end, and a week later most of it is gone. If you spread those eight practices over days, each one feels harder, and that is exactly why it sticks. Feeling sure at the end of a session is the worst sign, not the best.")


# ---------------------------------------------------------------- 2 (econ) cobweb with a P3-smoothed price expectation
def _cobweb(alpha, d, a=10.0, b=1.0, c=1.0, n=60, p0=3.0):
    """Supply q_t = c + d p^e_t, demand p_t = (a - q_t)/b; expectation p^e_{t+1} = (1 - alpha) p^e_t + alpha p_t
    (alpha = 1: last period's price, the source's cobweb; alpha < 1: the P3 kernel alpha (1 - alpha)^k over age k)."""
    pe = p0; ps = []
    for _ in range(n):
        p = (a - (c + d * pe)) / b; ps.append(p); pe = (1.0 - alpha) * pe + alpha * p
    return np.asarray(ps), (a - c) / (b + d)


def _cobweb_mean(d, a=10.0, b=1.0, c=1.0, n=200, p0=3.0):
    """The accumulated rule A6 excludes: the expectation is the plain mean of every settled price."""
    ps = [p0]
    for _ in range(n):
        pe = float(np.mean(ps)); ps.append((a - (c + d * pe)) / b)
    return np.asarray(ps[1:]), (a - c) / (b + d)


def cobweb():
    b = 1.0; alphas = (1.0, 0.5, 0.25); ds = (0.8, 1.5, 2.5); cells = {}
    for al in alphas:
        for d in ds:
            ps, pst = _cobweb(al, d); dev = ps - pst
            ratio = abs(dev[4] / dev[3]); sign = float(np.sign(dev[4] * dev[3]))
            root = 1.0 - al * (1.0 + d / b)
            cells[(al, d)] = (ratio, sign, root)
    max_rel = max(rel(v[0], abs(v[2])) for v in cells.values())
    sign_ok = all((v[1] < 0) == (v[2] < 0) for v in cells.values())
    # the stability boundary d/b < (2 - alpha)/alpha at alpha = 0.5: 3.0
    edge = {}
    for d in (2.9, 3.1):
        ps, pst = _cobweb(0.5, d, n=40); dev = np.abs(ps - pst); edge[d] = (float(dev[-1] / dev[0]), 1.0 - 0.5 * (1.0 + d / b))
    stable_ok = edge[2.9][0] < 1.0 and edge[3.1][0] > 1.0
    mean_rule = {d: float(np.abs(_cobweb_mean(d)[0][-10:] - _cobweb_mean(d)[1]).max()) for d in (2.5, 5.0)}
    crr = cells[(0.5, 1.5)][0]; null = cells[(1.0, 1.5)][0]; dom = abs(cells[(0.5, 1.5)][2])
    made = f"{'an unstable' if null > 1.0 else 'a stable'} market made {'convergent' if crr < 1.0 else 'divergent'}"
    mean_word = "converges" if max(mean_rule.values()) < 1e-6 else "does not converge"
    check = max_rel <= 1e-6 and sign_ok and stable_ok
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("econ", "Cobweb market (demand p = 10 - q, supply q = 1 + d p^e, the source's parameters with d/b in {0.8, 1.5, 2.5}) whose suppliers expect the P3 age-weighted mean of settled prices, p^e_{t+1} = (1 - alpha) p^e_t + alpha p_t (weights alpha (1 - alpha)^k, alpha in {1, 0.5, 0.25}); 60 periods from an initial expected price of 3",
                    source=f"{SRC_T} [18] (DESCR)",
                    Q="a supplier who regenerates the expected price from the settled past with P3 age weights (A6, bounded strength alpha) turns the cobweb's root -d/b into 1 - alpha (1 + d/b): the market converges whenever d/b < (2 - alpha)/alpha, beyond the naive cobweb's d/b < 1, and it oscillates only while alpha (1 + d/b) > 1, otherwise it converges without a period-two swing",
                    ingredient="A6 (the next occasion's expectation seeded from the settled past at bounded strength, never an accumulated count), P3 (geometric age weights q = 1 - alpha), D5 (occasion = one market period)",
                    null="the source's cobweb: the expectation is last period's price (alpha = 1, depth one), root -d/b",
                    domain="Nerlove 1958 (adaptive expectations and cobweb phenomena: root 1 - alpha (1 + d/b), stable for d/b < (2 - alpha)/alpha); Ezekiel 1938; Carlson 1968 (the mean of all past prices: an invariably stable cobweb). Named only, not fetched (R10)",
                    numbers="; ".join(f"alpha = {al:g}, d/b = {d / b:g}: measured per-period ratio {cells[(al, d)][0]:.6f} (sign of consecutive deviations {'-' if cells[(al, d)][1] < 0 else '+'}), root 1 - alpha (1 + d/b) = {cells[(al, d)][2]:+.4f}" for al in alphas for d in ds)
                            + f"; largest relative difference between measured ratio and |root| over the 9 cells {max_rel:.1e}; boundary at alpha = 0.5 ((2 - alpha)/alpha = {(2 - 0.5) / 0.5:g}): d/b = 2.9 deviation at period 40 / deviation at period 1 = {edge[2.9][0]:.3e} (root {edge[2.9][1]:+.3f}), d/b = 3.1: {edge[3.1][0]:.3e} (root {edge[3.1][1]:+.3f}); the accumulated mean of all settled prices (the rule A6 excludes), largest deviation over periods 191-200: d/b = 2.5 {mean_rule[2.5]:.2e}, d/b = 5 {mean_rule[5.0]:.2e} (it {mean_word} at both)",
                    tg=f"per-period amplitude ratio with the P3 expectation {crr:.4f} vs null (last period's price) {null:.4f} at d/b = 1.5: {ag(crr, null)}",
                    tn=f"Nerlove's root gives {dom:.4f}: {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"measured ratio = |1 - alpha (1 + d/b)| within 1e-6 in all 9 cells: {yn(max_rel <= 1e-6)}; oscillation iff alpha (1 + d/b) > 1 in all 9 cells: {yn(sign_ok)}; convergent at d/b = 2.9 and divergent at 3.1 for alpha = 0.5: {yn(stable_ok)}: {hf(check)}",
                    out=out,
                    reading=f"A6 with P3 does work on the source's control row (T-G: the ratio {'falls' if crr < null else 'rises'} from {null:.4f} to {crr:.4f} at d/b = 1.5, {made}) and what it produces is Nerlove's adaptive-expectations cobweb of 1958, root for root: the P3 kernel is exponential smoothing of the price, and the domain has had the stability region (2 - alpha)/alpha and the loss of the period-two swing below alpha (1 + d/b) = 1 since 1958, twenty years after Ezekiel's cobweb. The bounded-strength clause of A6 excludes the expectation rule that {mean_word} at every slope tried, the mean of every settled price (deviation {mean_rule[5.0]:.2e} at d/b = 5 after 200 periods; Carlson's invariably stable cobweb), as it excluded the accumulated forecast on the bullwhip row (batch 18 row 5): regeneration is not estimation. The source's 'nothing to test' becomes 'the domain tested it in 1958'; the synthesis reading is {out}",
                    weakness="a linear cobweb with one smoothing constant; the mean-age constraint of P3 is not fixed by CRR, so alpha is the domain's parameter under a CRR name; citations by name and year only, not fetched (R10)",
                    elegance="Farmers who plant on a fading average of past prices instead of last year's price alone turn a runaway hog cycle into a settling one; the memory does the calming, not the market. A rule with one number, how fast the past fades.",
                    child="Imagine farmers deciding how many pigs to raise. If they only look at last year's price, they all raise too many when it was high, the price crashes, then they all raise too few, and the swings can grow. If they remember several past years and let the old ones fade, the swings die down instead.")


# ---------------------------------------------------------------- 3 (surf) RHEED damping: path grown vs the present surface
def _grow(profile, L=64, D=50.0, dt=0.002, seed=0, n_ml=8, stride=0.05):
    """2-D solid-on-solid growth on an L x L periodic lattice: deposition at rate F(t) per site (binomial per step); an
    adatom (a site strictly higher than its four neighbours) hops at rate D to its lowest neighbour. The kinematic
    out-of-phase intensity I = |sum_n p_n (-1)^n|^2 on the height distribution p_n, the interface width w^2 = Var(h),
    the Fisher-Rao arc of p (categorical carrier, 2 sqrt p) sampled every `stride` monolayers of natural time, and the
    chord from the flat start 2 arccos sqrt(p_0), all recorded at integer coverage."""
    rng = np.random.default_rng(seed); h = np.zeros((L, L), int); N = L * L; dep = 0; t = 0.0; out = []; nxt = 1
    C_fr = 0.0; p_prev = None; next_sample = 0.0
    di = np.array([-1, 1, 0, 0]); dj = np.array([0, 0, -1, 1])
    while dep < n_ml * N:
        F = profile(t); k = rng.binomial(N, min(F * dt, 1.0))
        if k:
            idx = rng.integers(0, N, k); np.add.at(h.reshape(-1), idx, 1); dep += k
        nb = np.stack([np.roll(h, 1, 0), np.roll(h, -1, 0), np.roll(h, 1, 1), np.roll(h, -1, 1)])
        mv = (h > nb).all(axis=0) & (rng.random((L, L)) < D * dt)
        if mv.any():
            ii, jj = np.nonzero(mv); lo = np.argmin(nb[:, ii, jj], axis=0)
            h[ii, jj] -= 1; np.add.at(h, ((ii + di[lo]) % L, (jj + dj[lo]) % L), 1)
        t += dt
        if dep / N >= next_sample:
            p = np.bincount((h - h.min()).reshape(-1), minlength=64)[:64] / N
            if p_prev is not None:
                C_fr += 2.0 * float(np.linalg.norm(np.sqrt(p) - np.sqrt(p_prev)))
            p_prev = p; next_sample += stride
            while dep >= nxt * N and nxt <= n_ml:
                I = float(abs((p * (-1.0) ** np.arange(len(p))).sum()) ** 2); w2 = float(h.var()); p0 = float((h == 0).mean())
                out.append(dict(n=nxt, t=t, I=I, w2=w2, C=C_fr, E=2.0 * math.acos(math.sqrt(p0)))); nxt += 1
    return out


def rheed_damping():
    profiles = {"constant F = 1": lambda t: 1.0, "constant F = 0.1": lambda t: 0.1,
                "fast then slow (F = 1.9 for t < 2, then 0.1)": lambda t: 1.9 if t < 2.0 else 0.1,
                "slow then fast (F = 0.1 for t < 20, then 1.9)": lambda t: 0.1 if t < 20.0 else 1.9}
    res = {name: _grow(pf) for name, pf in profiles.items()}
    y = np.array([math.log(r["I"]) for o in res.values() for r in o])
    X = {k: np.array([r[k] for o in res.values() for r in o]) for k in ("n", "C", "E", "w2")}
    r2 = {k: _r2(y, X[k]) for k in X}
    slope_w2 = float(np.polyfit(X["w2"], y, 1)[0])
    fs = res["fast then slow (F = 1.9 for t < 2, then 0.1)"]; i4, i5 = fs[3], fs[4]
    recovers = i5["I"] > i4["I"] and i5["C"] > i4["C"] and i5["w2"] < i4["w2"]
    at8 = {name: o[-1] for name, o in res.items()}
    spread8 = max(r["I"] for r in at8.values()) / min(r["I"] for r in at8.values())
    crr = max(r2["n"], r2["C"]); null = r2["w2"]; dom = 1.0
    chord_sat = all(o[-1]["E"] >= math.pi - 1e-3 for o in res.values())
    check = crr >= null + 0.05
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("surf", "Layer-by-layer growth on a 64 x 64 solid-on-solid lattice (deposition at flux F per site, adatoms hopping to their lowest neighbour at rate D = 50, dt = 0.002, seed 0) to 8 monolayers under four flux histories, with the kinematic out-of-phase RHEED intensity I = |sum_n p_n (-1)^n|^2 read at every completed monolayer",
                    source=f"{SRC_T} [19] (DESCR)",
                    Q="the damping of the RHEED oscillation tracks the path grown (the monolayers deposited, A1' natural time, or the Fisher-Rao arc the height distribution has travelled, D6) rather than the present surface, so at equal path two flux histories show the same envelope",
                    ingredient="D6/H-T1 (path against endpoint) with A1' (one monolayer = one step of natural time, the source's ruler); D2 on the categorical height carrier (not proper)",
                    null="the endpoint: the present surface's own state, its interface width w^2 = Var(h), the same linear fit on the same 32 (history, monolayer) points",
                    domain="kinematic diffraction (Neave, Joyce, Dobson & Norton 1983 for the oscillations; Cohen, Petrich, Pukite, Whaley & Arrott 1989 for the level-resolved form): the out-of-phase intensity is the squared characteristic function of the present height distribution, I = |sum_n p_n e^{i pi n}|^2, a state functional with no history term. Named only, not fetched (R10)",
                    numbers="; ".join(f"{name}: at 1, 4, 8 ML clock t = {o[0]['t']:.1f}, {o[3]['t']:.1f}, {o[7]['t']:.1f}; I = {o[0]['I']:.4f}, {o[3]['I']:.4f}, {o[7]['I']:.4f}; w^2 = {o[0]['w2']:.3f}, {o[3]['w2']:.3f}, {o[7]['w2']:.3f}; Fisher arc C = {o[0]['C']:.2f}, {o[3]['C']:.2f}, {o[7]['C']:.2f}; chord from the flat start {o[0]['E']:.3f}, {o[3]['E']:.3f}, {o[7]['E']:.3f}" for name, o in res.items())
                            + f"; envelope at 8 ML across the four histories: largest / smallest = {spread8:.1f}; fast then slow, 4 -> 5 ML: I {i4['I']:.4f} -> {i5['I']:.4f} ({'rises' if i5['I'] > i4['I'] else 'falls'}) while C {i4['C']:.2f} -> {i5['C']:.2f} and w^2 {i4['w2']:.3f} -> {i5['w2']:.3f}; R^2 of ln I over the 32 points: on monolayers deposited {r2['n']:.4f}, on the Fisher arc {r2['C']:.4f}, on the chord from the start {r2['E']:.4f} (it {'reaches' if chord_sat else 'does not reach'} pi = {math.pi:.3f} by 8 ML in every history: level 0 is buried), on w^2 {r2['w2']:.4f} (fitted slope {slope_w2:.2f} per unit w^2; the Gaussian-height approximation gives -pi^2 = {-math.pi ** 2:.2f})",
                    tg=f"R^2 of the log envelope on the path (best of monolayers and Fisher arc) {crr:.4f} vs null (the present width w^2) {null:.4f}: {ag(crr, null)}",
                    tn=f"the kinematic theorem gives ln I exactly from the present p_n (R^2 = {dom:.4f} by identity): {ag(crr, dom, TOL_N)}",
                    tc=f"path ahead of the present-state predictor by >= 0.05: {yn(check)}; envelope recovers under a slow spell while the path grows: {yn(recovers)}: {hf(check)}",
                    out=out,
                    reading=f"the path does not carry the damping: at equal natural-time path (8 ML) the envelope differs by a factor {spread8:.1f} across histories, the Fisher arc explains R^2 {r2['C']:.4f} of the log envelope, and under a fast-then-slow flux the envelope {'rises' if recovers else 'does not rise'} between 4 and 5 ML ({i4['I']:.4f} -> {i5['I']:.4f}) as the low-flux spell lets the surface smooth (w^2 {i4['w2']:.3f} -> {i5['w2']:.3f}) while both path measures grow (monolayers 4 -> 5, C {i4['C']:.2f} -> {i5['C']:.2f}). The present width predicts the log envelope with R^2 {null:.4f} against {crr:.4f} for the best path, because the beam reads the surface's height distribution as it is now: the kinematic intensity is a state functional, which is the domain's theorem, and H-T1 read on the damping {hf(check)}. The source row's natural-time reading stands for the oscillation count (one per monolayer whatever the flux); the synthesis reading for the envelope is {out}",
                    weakness="a solid-on-solid model with one relaxation rule (downhill hops) and one seed, 64 x 64 sites, so the intensities carry finite-size scatter, and the w^2 fit's slope is not the Gaussian-height -pi^2 because the height distribution is discrete and narrow; the Fisher arc is sampled at 0.05 ML of natural time so that its accumulated sampling noise does not measure the clock; the chord from the flat start reaches pi once level 0 is buried and is not a usable endpoint, which is why the endpoint is taken as the domain's own state variable (the ARC-T1b lesson); citations by name and year only, not fetched (R10)",
                    elegance="The electron beam sees the wall as it is now, not the story of how it was built: slow down and let the bumps fill in, and the flicker brightens again. The count of layers is a clock; the shine is a state.",
                    child="When you build a wall one layer of bricks at a time, a light shining on it flickers once for every layer. How bright the flicker is depends on how bumpy the top is right now, not on how many layers you have laid: if you slow down and let the bumps fill in, the flicker gets bright again.")


# ---------------------------------------------------------------- 4 (def) the empty occasion: every proper ingredient tried
def _raised(fn, *a, **k):
    try:
        v = fn(*a, **k); return f"returned {v!r}"[:60]
    except Exception as e:
        return f"raised {type(e).__name__}: {e}"


def empty_occasion():
    x = np.zeros(200)
    C, Cs, S = surplus(x, sigma=1.0)
    ph = intrinsic_phase(x); cuts = antipodal_cuts(ph); n_occ = len(cuts) - 1
    unit = _raised(unit_sigma, np.zeros(40))
    a6 = [float(sum([])) for _ in (-1.0, 0.0, 1.0)]          # A6 objective sum_m pi_m d^2(y, Phi_m) over an empty set of settled occasions
    reg = _raised(regularity, x, np.asarray([], int))
    pl = path_length([np.zeros((5, 1))] * 4, kl=kl_gauss)
    one = np.array([0.0, 1.0]); C1, Cs1, S1 = surplus(one, sigma=1.0); rho1 = rho(float(np.ptp(one)), 1.0)
    out = outcome(unstated=True)
    return make_row("def", "The empty occasion (a carrier that does not move: 200 samples of zero), each CRR-proper ingredient applied to it in turn, and the smallest non-empty occasion beside it (one step of one unit)",
                    source=f"{SRC_E} [1] (DESCR)",
                    Q="none could be formed: on a carrier that does not move every CRR-proper ingredient returns nothing, an exception, or an identity, and no domain is named by any of them",
                    ingredient="A3/D5 (the cut on the intrinsic phase), A1'/D1 (the unit), A6 (the seed from settled occasions), H-L5 (regularity across occasions), D6 (path against endpoint), each tried",
                    null="none: there is no decisive quantity to ablate",
                    domain=None,
                    numbers=f"D2-D4: C = {C:.1f}, C* = {Cs:.1f}, S = {S:.1f}; A3: intrinsic phase spans {float(np.ptp(ph)):.4f} rad, antipodal_cuts returns {cuts.tolist()} ({n_occ} occasions); A1': unit_sigma on the constant statistic {unit}; A6 with no settled occasion: the objective sum_m pi_m d^2(y, Phi_m) at y = -1, 0, 1 is {a6[0]:.1f}, {a6[1]:.1f}, {a6[2]:.1f} (every point minimises: the first seed is unconstrained); H-L5: regularity with no events {reg}; D6 on four identical snapshots: C = {pl['C']:.1f}, E = {pl['E']:.1f}, S = {pl['S']:.1f}; the smallest non-empty occasion (one step of one unit): C = {C1:.1f}, C* = {Cs1:.1f}, S = {S1:.1f}, rho = {rho1:.1f}",
                    tg="no decisive quantity: the arc, the cut count, the unit, the seed objective and the path all read zero, none or every point",
                    tn="none: no domain theorem is engaged (a fixed point of a flow, a stationary state and a degenerate statistic were considered; synthesis row 10 already found the arc clock silent on a stationary state)",
                    tc="none",
                    out=out,
                    reading="what was tried is printed: the cut needs a phase that advances (it does not), the unit needs a residual (there is none, and the instrument rejects the record rather than returning zero), the seed needs a settled occasion (with none, A6 constrains nothing), the regularity needs occasions to compare, and the path is zero. A carrier that does not move is outside every proper ingredient's domain of definition, not a case of any of them; the source row's 'the framework cannot count on a carrier that does not change' is the whole content, and the synthesis reading is " + out,
                    weakness="the honest outcome for a definitional row: silence; the one number that is not zero, rho = 1 for the one-step occasion, is a definition (D1)")


# ---------------------------------------------------------------- 5 (def) the cut as a delta in phase: its mass against the clock
def phase_delta():
    f0, k, T, dt, eps = 1.0, 0.5, 6.0, 5e-5, 5e-3; L = 2.0 * math.pi
    t = np.arange(0.0, T, dt); u = 2.0 * math.pi * (f0 * t + 0.5 * k * t * t); udot = 2.0 * math.pi * (f0 + k * t)
    m = np.arange(1, int((u[-1] - u[0]) / (L / 2)) + 1); tk = (-f0 + np.sqrt(f0 ** 2 + k * m)) / k       # u(t_k) = u(0) + k L/2
    uk = 2.0 * math.pi * (f0 * tk + 0.5 * k * tk * tk); udk = 2.0 * math.pi * (f0 + k * tk)
    mass = np.array([float(np.trapezoid(np.exp(-(u - uc) ** 2 / (2 * eps ** 2)) / (eps * math.sqrt(2 * math.pi)), t)) for uc in uk])
    mass_phase = float(np.trapezoid(np.exp(-(np.linspace(-1, 1, 20001)) ** 2 / (2 * eps ** 2)) / (eps * math.sqrt(2 * math.pi)), np.linspace(-1, 1, 20001)))
    max_rel = float(np.max(np.abs(mass * udk - 1.0)))
    sum_mass = float(mass[:-1].sum()); sum_dt = float(np.diff(tk).sum() / (L / 2))
    x = np.cos(u); n_a3 = len(antipodal_cuts(intrinsic_phase(x))); n_pk = len(peak_cuts(x, prominence=0.5, distance=int(0.05 / dt)))
    crr = float(mass[0]); null = 1.0; dom = float(1.0 / udk[0])
    check = max_rel <= 1e-4
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("def", f"A3's cut delta(u(t) - u(t_n) - L/2) on a linear chirp u(t) = 2 pi (t + t^2/4) over {T:g} s (phase velocity rising from {udot[0]:.3f} to {udot[-1]:.3f} rad/s), the delta realised as a Gaussian of width {eps:g} rad in phase and integrated against the clock at each of its {len(tk)} cuts",
                    source=f"{SRC_E} [2] (DESCR)",
                    Q="the cut counts once in phase and 1/|du/dt| in clock time: written as a delta in phase, A3's cut carries clock-time mass 1/|u'(t_k)| at its k-th cut, which is the duration of the half-turn it closes divided by the half-turn L/2 to first order, so the same train of cuts measures occasions when integrated in phase and clock time when integrated in time",
                    ingredient="A3 (the cut as a delta in the intrinsic phase, no duration and no content), D5 (the occasion it closes)",
                    null="the peak cut: a delta in clock time at a detected extremum, mass 1 per event by construction (the instrument's peak_cuts)",
                    domain="the composition rule for the delta distribution, delta(g(t)) = sum_k delta(t - t_k)/|g'(t_k)| over the simple zeros of g (Gel'fand & Shilov 1964, Generalized Functions vol. 1). Named only, not fetched (R10)",
                    numbers=f"mass of the phase delta integrated in phase {mass_phase:.6f}; integrated in time at cuts 1, 2, 3, {len(tk)}: {mass[0]:.6f}, {mass[1]:.6f}, {mass[2]:.6f}, {mass[-1]:.6f} against 1/u'(t_k) = {1 / udk[0]:.6f}, {1 / udk[1]:.6f}, {1 / udk[2]:.6f}, {1 / udk[-1]:.6f} (largest relative difference {max_rel:.1e}); sum of the masses of cuts 1..{len(tk) - 1} = {sum_mass:.4f} against the sum of the half-turn durations over L/2 = {sum_dt:.4f} (relative difference {rel(sum_mass, sum_dt):.3f}, first order in the chirp rate); on cos u(t) the instrument finds {n_a3} antipodal cuts (start included) and {n_pk} peak cuts",
                    tg=f"clock-time mass of the first A3 cut {crr:.4f} vs null (a peak cut's mass) {null:.4f}: {ag(crr, null)}",
                    tn=f"the composition rule gives 1/u'(t_1) = {dom:.4f}: {ag(crr, dom, TOL_N)} (the domain has Q)",
                    tc=f"mass = 1/|u'(t_k)| within 1e-4 at every cut: {yn(check)}: {hf(check)}",
                    out=out,
                    reading=f"A3 fixes its delta in phase, and a delta in phase is not a delta in time: at each cut it weighs 1/|u'(t_k)| against the clock, which is the half-turn's own duration in units of L/2 (the {len(tk) - 1} masses sum to {sum_mass:.4f} against {sum_dt:.4f} for the durations), so integrated over a record the cut train reads the clock and integrated over the phase it reads the count; the source row's 'unit count, zero measure' is the phase reading, and the clock reading is the composition rule of distribution theory, which the domain has. Nothing here is a proposition about a system; the synthesis reading is {out}",
                    weakness="a definition read against the clock; the delta is realised at a finite width in phase, so its time mass is exact only to that width (the largest relative difference is printed); a chirp with a monotone phase, so every zero of u(t) - u_k is simple",
                    elegance="A finish line has no width, but ask how much of the race each finish line took and the answer is the time between lines, longer when the runner is slow; counted in laps every line is exactly one. One picture for a cut that has no duration and still knows the clock.",
                    child="A finish line has no width. But if you ask how much of the race each finish line took, the answer is the time between one line and the next, which is longer when the runner is slow. Counted in laps, every finish line is just one lap.")


def main():
    return run_batch("Synthesis batch 20: rows 96-100 (prompt-log entry 61)",
                     [spacing_effect(), cobweb(), rheed_damping(), empty_occasion(), phase_delta()])


if __name__ == "__main__":
    sys.exit(main())
