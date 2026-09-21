"""Synthesis batch 13: rows 61-65 of QUEUE.md (prompt-log entry 61). Bio battery [13] bacterial cell-size control, adder vs
timer under growth-rate variation (CONSIST; the last row on the SHARP review's dynamical-CONSIST list, AGENT_LOG 34: H-L5's
amplitude control on the adder is the first task; synthesis.py row 8 already made the A6/P3 lag-2 proposition, not repeated);
[14] single ion channel, two-state Markov gating (DESCR); [18] circadian phase oscillator entrained by a light cycle (DESCR).
E-I battery [4] balanced E-I network of leaky integrate-and-fire neurons (DESCR; AGENT_LOG 18 records the reset-jump
segmentation bias found on this row); [6] theta-gamma n:m phase-phase coupling (DESCR). Source rows are in
theory/retrodictions/bio_retrodictions.txt and theory/retrodictions/ei_networks.txt; their models are re-implemented here
(nothing imported from the battery scripts). Deterministic (fixed seeds, fixed grids, explicit RK4 and Euler steps); no data
file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_13.py
"""
import math
import sys

import numpy as np

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

BIO = "theory/retrodictions/bio_retrodictions.txt"
EI = "theory/retrodictions/ei_networks.txt"
EULER_GAMMA = 0.5772156649015329


def _word(cond, yes, no):
    return yes if cond else no


def _agree(a, b, tol=TOL_G):
    return _word(rel(a, b) <= tol, "agree", "differ")


def _hf(cond):
    return _word(cond, "holds", "fails")


def _acf(x, k):
    x = np.asarray(x, float)
    return float(np.corrcoef(x[:-k], x[k:])[0, 1])


# ---------------------------------------------------------------- 61 [13] the adder: H-L5's amplitude control
def _lineage(rule, n=400, seed=7, Delta=1.0, noise=0.08, rate_cv=0.25, fs=200, T_fix=1.4):
    """One lineage as a sampled volume trace (the source row's draws: seed 7, Delta = 1, 8 % division noise, 25 % growth-rate
    spread, timer 1.4 with 8 % noise). Exponential growth at lam_n from the birth size v_b; the adder divides at v_b + Delta_n,
    the timer after T_n; the daughter is half. The division is the system's own event; the halving is a reset jump at it."""
    rng = np.random.default_rng(seed)
    added = Delta * (1 + noise * rng.standard_normal(n)); rates = 0.5 * (1 + rate_cv * rng.standard_normal(n))
    T_fixes = T_fix * (1 + noise * rng.standard_normal(n))
    x, ev, vbs, adds, Ts, vb = [], [], [], [], [], 1.0
    for k in range(n):
        T = math.log((vb + added[k]) / vb) / rates[k] if rule == "adder" else T_fixes[k]
        m = int(round(T * fs)); tt = np.arange(m) / fs
        ev.append(len(x)); x.extend(vb * np.exp(rates[k] * tt))
        vd = vb * math.exp(rates[k] * T); vbs.append(vb); adds.append(vd - vb); Ts.append(T); vb = vd / 2.0
    return np.asarray(x), np.asarray(ev), np.asarray(vbs), np.asarray(adds), np.asarray(Ts), 1.0 / fs


def r1(skip=50):
    res = {}
    for rule in ("adder", "timer"):
        x, ev, vbs, adds, Ts, dt = _lineage(rule); ev = ev[skip:]; vbs, adds, Ts = vbs[skip:], adds[skip:], Ts[skip:]
        rx = regularity(x, ev, sigma=1.0, dt=dt, n_boot=2000, segment_end="exclusive")   # the halving is the cut (A3), not arc
        ri = regularity(x, ev, sigma=1.0, dt=dt, n_boot=2000, segment_end="inclusive")   # the halving counted inside every arc
        vd = vbs + adds
        res[rule] = dict(rx=rx, ri=ri, cv_add=cv(adds), cv_T=cv(Ts), cv_vb=cv(vbs), slope=float(np.polyfit(vbs, adds, 1)[0]),
                         cv_pois=cv(2.0 * (np.sqrt(vd) - np.sqrt(vbs))), cv_log=cv(np.log(vd / vbs)))
    a, t = res["adder"], res["timer"]
    rx = a["rx"]
    crr, null, dom = rx["cv_arc"], rx["cv_amp"], a["cv_add"]
    identity = rx["ci95_amp"][0] <= 0.0 <= rx["ci95_amp"][1]                    # control (i) ties the arc: CI of CV(arc) - CV(amplitude) includes 0
    arc_reg = rx["ci95"][1] < 0.0                                                # the bare class: CI of CV(arc) - CV(clock) entirely below 0
    timer_clock = t["rx"]["ci95"][0] > 0.0
    check = identity and arc_reg and timer_clock
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    beyond = outcome(crr=rx["cv_arc"], null=rx["cv_amp"], domain=None, check=(rx["ci95_amp"][1] < 0.0))   # H-L5 as CRR.md states it: the arc must beat control (i)
    def cls(r):
        lo, hi = r["ci95"]
        return "CI includes 0" if lo <= 0.0 <= hi else _word(r["cv_arc"] < r["cv_clock"], "arc-regular", "clock-regular")
    return make_row("bio",
        f"Bacterial cell-size control as one sampled lineage (the source's draws: Delta = 1, 8 % division noise, 25 % growth-rate spread, 400 cycles at 200 samples per unit time, the first {skip} dropped): exponential growth from birth to division, the division as the system's own event, the halving as a reset jump at it; the adder (divide at v_b + Delta) against the timer (divide after a fixed time)",
        source=f"{BIO} [13] (CONSIST)",
        Q="the adder is in H-L5's arc-regular class beyond the amplitude control: on the volume carrier the arc of a cell cycle is the added volume, because a cycle is one monotone traversal (P1's equality: arc = chord), so CV(arc) = CV(amplitude control) identically and the class is the adder principle read in CRR's words",
        ingredient="H-L5 (the class claim: arc against clock between own events, beyond its control (i), the excursion amplitude), D5 [M] (occasion = birth to division), A3 (the halving is the cut: segment_end = exclusive), D2 with the identity metric on volume (the source's carrier)",
        null="H-L5's control (i): the peak-to-peak amplitude of the occasion, the domain's added volume",
        domain="the adder principle (Campos et al. 2014; Taheri-Araghi et al. 2015): E. coli and B. subtilis add a near-constant volume per cycle whatever the growth rate, so the added volume is the regular quantity and the interdivision time inherits the growth-rate spread; Amir 2014's size-control slope of added on birth size (0 adder, 1 timer, -1 sizer)",
        numbers=(f"adder, {rx['n']} occasions, halving excluded: CV(arc) = {rx['cv_arc']:.4f}, CV(clock) = {rx['cv_clock']:.4f}, CV(amplitude) = {rx['cv_amp']:.4f}, C_mean = {rx['C_mean']:.4f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) = [{rx['ci95'][0]:.4f}, {rx['ci95'][1]:.4f}] ({cls(rx)}), of CV(arc) - CV(amplitude) = [{rx['ci95_amp'][0]:.4f}, {rx['ci95_amp'][1]:.4f}]; "
                 f"halving counted inside the arc: CV(arc) = {a['ri']['cv_arc']:.4f}, C_mean = {a['ri']['C_mean']:.4f}, CI of CV(arc) - CV(amplitude) = [{a['ri']['ci95_amp'][0]:.4f}, {a['ri']['ci95_amp'][1]:.4f}]; the lineage's own quantities: CV(added volume) = {a['cv_add']:.4f} (the instrument's arc agrees to {rel(rx['cv_arc'], a['cv_add']):.1e}, one sample of growth), CV(interdivision time) = {a['cv_T']:.4f}, CV(birth size) = {a['cv_vb']:.4f}, slope of added on birth size {a['slope']:.4f}; "
                 f"control (ii), the metric: Poisson-count carrier 2(sqrt v_d - sqrt v_b): CV = {a['cv_pois']:.4f}; log carrier ln(v_d/v_b): CV = {a['cv_log']:.4f} (each a function of the birth/division pair only); "
                 f"timer, {t['rx']['n']} occasions: CV(arc) = {t['rx']['cv_arc']:.4f}, CV(clock) = {t['rx']['cv_clock']:.4f}, CV(amplitude) = {t['rx']['cv_amp']:.4f}, CI of CV(arc) - CV(clock) = [{t['rx']['ci95'][0]:.4f}, {t['rx']['ci95'][1]:.4f}] ({cls(t['rx'])}), slope of added on birth size {t['slope']:.4f}"),
        tg=f"CV(arc) {crr:.4f} vs null CV(amplitude control) {null:.4f}: {_agree(crr, null)}",
        tn=f"the adder's own rule gives CV(added volume) = {dom:.4f} for the same target: {_agree(crr, dom, TOL_N)} (the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q)",
        tc=f"CI of CV(arc) - CV(amplitude) includes 0 ({_word(identity, 'yes', 'no')}), the adder's CI of CV(arc) - CV(clock) lies below 0 ({_word(arc_reg, 'yes', 'no')}), the timer's above 0 ({_word(timer_clock, 'yes', 'no')}): {_hf(check)}",
        out=out,
        reading=(f"on the volume carrier every cycle is one monotone traversal, so its arc is its chord (P1's equality) in whichever coordinate the metric picks: the added volume under the identity metric (CV {rx['cv_arc']:.4f}), 2(sqrt v_d - sqrt v_b) on a count carrier ({a['cv_pois']:.4f}), ln(v_d/v_b) on the log carrier ({a['cv_log']:.4f}), each a function of the birth/division pair the domain measures; "
                 f"H-L5's amplitude control is therefore the arc itself (CI [{rx['ci95_amp'][0]:.4f}, {rx['ci95_amp'][1]:.4f}]) and H-L5 beyond its controls reads {beyond} on the adder: not false, empty. The bare class reading stands ({cls(rx)}, CV(arc) {rx['cv_arc']:.4f} against CV(clock) {rx['cv_clock']:.4f}) and it is the adder principle: the added volume is the controlled quantity and the time inherits the growth-rate spread (the timer, {cls(t['rx'])}, is the other corner). Counting the halving inside the arc lowers CV(arc) to {a['ri']['cv_arc']:.4f}, the AGENT_LOG 18 arithmetic, here with a jump that varies with the division size. "
                 f"The SHARP review's list of dynamical CONSIST rows (AGENT_LOG 34) loses its last row: the prospective single-cell study would re-measure the adder principle in the domain's own coordinate, and the one CRR proposition on this carrier that the domain's model does not make is synthesis row 8's A6/P3 lag-2 term, not repeated here"),
        weakness="a model lineage with the source's draws; real lineages have growth-rate and birth-size correlations across generations (mother-daughter) that this row does not model; the identity metric on volume is the source's stand-in, which A1 does not license, and the count and log carriers are printed as sensitivities, not as a choice; citations by name and year only, not fetched here (R10)",
        elegance="Grow, add a fixed amount, split. A cell that follows that rule is perfectly steady if you count what it added and unsteady if you count the minutes, because fast growers finish sooner. The steadiness sits in the rule, and the arc is just the amount added, with no knob to turn.",
        child="A bacterium grows and then splits in two. It does not split after a fixed number of minutes; it splits when it has grown by a fixed amount, the same amount every time. So if you measure a cell's life by how much it grew, every life is the same length; if you measure it by the clock, the fast-growing cells have short lives and the slow ones long lives. The regular thing is the amount added, and that is the rule the cell itself follows.")


# ---------------------------------------------------------------- 62 [14] the two-state channel: A6 on the dwell carrier
def _two_state(n=4000, seed=11, ko=2.0, kc=1.0):
    """The source row's channel (seed 11): alternating exponential dwells, closed at rate ko, open at rate kc."""
    rng = np.random.default_rng(seed); state = 0; dwell = {0: [], 1: []}
    for _ in range(n):
        rate = ko if state == 0 else kc; dwell[state].append(rng.exponential(1 / rate)); state = 1 - state
    return np.asarray(dwell[1]), np.asarray(dwell[0])


def _seeded_open(q, n, seed, mu=1.0, reading="log"):
    """A6 with P3 weights on the open-dwell carrier: the scale the next open dwell is drawn with is the weighted mean of the
    settled open dwells (weights (1 - q) q^k over age k). 'log': the Fisher-Rao Frechet mean on the exponential family (metric
    1/mu^2, the log coordinate is flat), the reading A1 licenses; 'lin': the identity-metric mean, the stand-in."""
    rng = np.random.default_rng(seed); u = rng.exponential(1.0, n)
    if reading == "log":                                          # carried in ln tau: the scale drifts and would underflow
        lt = np.empty(n); m = math.log(mu); lt[0] = m + math.log(u[0])
        for i in range(1, n):
            m = (1 - q) * lt[i - 1] + q * m; lt[i] = m + math.log(u[i])
        return lt
    tau = np.empty(n); m = mu; tau[0] = mu * u[0]
    for i in range(1, n):
        m = (1 - q) * tau[i - 1] + q * m; tau[i] = m * u[i]
    return tau


def _two_gateway(rates, n_open=40000, seed=3):
    """O1 <-> C1 <-> C2 <-> O2, two gateway states: the domain's smallest mechanism with correlated successive open times.
    Returns the simulated open dwells and the closed-form lag-k correlations (Colquhoun-Hawkes: a geometric kernel whose
    ratio is the second eigenvalue of the open-to-open transition matrix)."""
    a1, b1, c12, c21, b2, a2 = rates
    Qm = np.array([[-a1, a1, 0, 0], [b1, -(b1 + c12), c12, 0], [0, c21, -(c21 + b2), b2], [0, 0, a2, -a2]])
    rng = np.random.default_rng(seed); s = 0; opens = []
    while len(opens) < n_open:
        r = Qm[s].copy(); r[s] = 0.0; tot = r.sum(); d = rng.exponential(1.0 / tot)
        if s in (0, 3): opens.append(d)
        s = int(rng.choice(4, p=r / tot))
    A = np.array([[b1 + c12, -c12], [-c21, c21 + b2]]); u = np.linalg.solve(A, [b1, 0.0])   # P(next open is O1 | closed entered from O1 / O2)
    P = np.array([[u[0], 1 - u[0]], [u[1], 1 - u[1]]]); lam = float(P[0, 0] + P[1, 1] - 1.0)
    w, v = np.linalg.eig(P.T); pi = np.real(v[:, int(np.argmin(abs(w - 1)))]); pi = pi / pi.sum()
    mu = np.array([1 / a1, 1 / a2]); mbar = float(pi @ mu); var = float(pi @ (2 * mu ** 2) - mbar ** 2)
    corr = [float((pi @ (mu * (np.linalg.matrix_power(P, k) @ mu)) - mbar ** 2) / var) for k in (1, 2, 3)]
    return np.asarray(opens), lam, corr


def r2(q=0.3, win=100, n_rep=200, n_gate=10):
    op, cl = _two_state()
    se = 1.0 / math.sqrt(len(op)); lag = [_acf(op, k) for k in (1, 2, 3)]
    # the A6-seeded channel: lag-1 correlation of successive open dwells over windows of `win` dwells, averaged over replicates
    logs = [_seeded_open(q, win, 100 + s, reading="log") for s in range(n_rep)]
    c_log = float(np.mean([_acf(np.exp(lt), 1) for lt in logs]))
    c_lin = float(np.mean([_acf(_seeded_open(q, win, 100 + s, reading="lin"), 1) for s in range(n_rep)]))
    c_mem = float(np.mean([_acf(np.random.default_rng(100 + s).exponential(1.0, win), 1) for s in range(n_rep)]))
    # the seeded scale is not stationary: the log reading drifts by -(1 - q) gamma per dwell (E ln Exp(mu) = ln mu - gamma);
    # measured as the mean increment of ln tau per dwell over the replicate windows
    incs = [(lt[-1] - lt[0]) / (win - 1) for lt in logs]; drift, drift_se = float(np.mean(incs)), float(np.std(incs, ddof=1) / math.sqrt(n_rep))
    tl = _seeded_open(q, 4000, 11, reading="lin"); first, last = float(tl[:100].mean()), float(tl[-100:].mean())
    gate = [_two_gateway((1.0, 1.0, 0.25, 0.25, 1.0, 4.0), seed=3 + s) for s in range(n_gate)]
    lam, corr_th = gate[0][1], gate[0][2]
    sims = np.array([[_acf(o, k) for k in (1, 2, 3)] for o, _, _ in gate]); corr_sim = sims.mean(0); corr_sd = sims.std(0, ddof=1)
    crr, null, dom = c_log, c_mem, 0.0
    check = lag[0] > 2 * se                                              # Q predicts a positive lag-1 correlation on the channel
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("bio",
        f"Single ion channel, two-state Markov gating (the source's channel: opening rate 2, closing rate 1, {2 * len(op)} transitions, seed 11), with A6 regeneration on the open-dwell carrier: the scale the next open dwell is drawn with is the P3 age-weighted Frechet mean of the settled open dwells (q = {q:g})",
        source=f"{BIO} [14] (DESCR)",
        Q="successive open dwells of the channel are correlated, with the geometric lag kernel q^k of P3: the next occasion is seeded from the settled ones (A6), so the memory of past dwells shows in the dwell sequence",
        ingredient="A6 (the next occasion seeded from settled occasions at bounded strength) with P3 (geometric age weights), D5 [M] (occasion = one dwell, the transition is the cut); A1 on the exponential family fixes the Frechet mean as the mean in ln tau (the identity-metric mean is printed as the stand-in, not as a second reading)",
        null="the memoryless channel: every dwell drawn afresh from the state's exponential law (the domain's model)",
        domain="the Markov theorem for a one-gateway mechanism: successive dwell times of a two-state channel are independent (Fredkin, Montal and Rice 1985; Colquhoun and Hawkes 1987: correlations between successive open times need at least two gateway states, and then decay as a sum of geometric terms)",
        numbers=(f"source channel: mean open {op.mean():.3f} (1/kc = 1.000), mean closed {cl.mean():.3f} (1/ko = 0.500), CV {cv(op):.3f}, {cv(cl):.3f}; open-dwell correlation at lags 1, 2, 3: {lag[0]:+.4f}, {lag[1]:+.4f}, {lag[2]:+.4f} (SE {se:.4f}); closed form 0 at every lag; "
                 f"A6-seeded channel, lag-1 correlation over {win}-dwell windows, mean of {n_rep} replicates: Frechet (log) reading {c_log:.4f}, identity-metric reading {c_lin:.4f}, memoryless {c_mem:+.4f}; the seed is not stationary: under the Frechet reading the mean increment of ln tau is {drift:.4f} per dwell (SE {drift_se:.4f}; closed form -(1 - q) gamma_Euler = {-(1 - q) * EULER_GAMMA:.4f}), under the identity reading the scale is a martingale that collapses (mean open dwell {first:.4f} over the first 100 dwells, {last:.1e} over the last 100 of 4000); "
                 f"the domain's own dwell memory, two-gateway scheme O1-C1-C2-O2 (rates 1, 1, 0.25, 0.25, 1, 4), {n_gate} runs of {len(gate[0][0])} open dwells: correlation at lags 1, 2, 3 = {corr_sim[0]:.4f}, {corr_sim[1]:.4f}, {corr_sim[2]:.4f} (spread across runs {corr_sd[0]:.4f}, {corr_sd[1]:.4f}, {corr_sd[2]:.4f}; closed form {corr_th[0]:.4f}, {corr_th[1]:.4f}, {corr_th[2]:.4f}), kernel ratio corr_2/corr_1 = {corr_sim[1] / corr_sim[0]:.4f} (closed form: the eigenvalue lambda = {lam:.4f} of the open-to-open transition matrix)"),
        tg=f"lag-1 correlation under the A6 seed {crr:.4f} vs null (memoryless) {null:+.4f}: {_agree(crr, null)}",
        tn=f"the Markov theorem gives {dom:.4f}: {_agree(crr, dom, TOL_N)} (the domain's value is the null's, not the seed's)",
        tc=f"Q predicts a positive lag-1 correlation on the channel; the source's channel gives {lag[0]:+.4f} at SE {se:.4f} (above 2 SE: {_word(check, 'yes', 'no')}), so Q {_hf(check)}",
        out=out,
        reading=(f"read as a rule for a channel, A6 is contradicted by the domain's central theorem: the seeded channel carries a lag-1 correlation of {c_log:.4f} where the channel has none ({lag[0]:+.4f} at SE {se:.4f}), and the seed has no stationary rate at all (the Frechet mean of exponential dwells is biased below their scale by gamma_Euler, so the open time drifts to zero at {drift:.4f} per dwell; the identity-metric mean collapses as a martingale), which is the third accumulating-or-drifting domain after Bayes and Tolman (synthesis rows 3, 9). "
                 f"Where the domain does have dwell memory, the two-gateway mechanism, the kernel is geometric with ratio {lam:.4f} fixed by the rates (measured {corr_sim[1] / corr_sim[0]:.4f}), so the shape P3 posits is the domain's and the q it leaves free the domain fixes; and it arises from the state the channel is in, not from the settled dwells. The source row's DESCR ('depth one, natural time counts transitions') stands"),
        weakness="the occasion's content is taken as the realised dwell, as in every earlier A6 row; if the content were the state's law itself, the Frechet mean of identical laws returns the law and A6 says nothing (vacuous rather than wrong); the correlation of the seeded channel is measured over 100-dwell windows because the seed has no stationary value; the two-gateway rates are chosen here to make the kernel measurable; citations by name and year only, not fetched here (R10)",
        elegance="A channel is a switch that forgets: how long it stays open next has nothing to do with how long it stayed open before. That is the one thing CRR's regeneration rule cannot say, and a switch is the cleanest place to see it fail.",
        child="Imagine a door that opens and shuts on its own at random. If you time how long it stays open each time, the times are all over the place, and the next opening does not remember the last one at all. CRR has a rule that says the next thing a system does is built from what it settled before. The door says no: it starts fresh every time. So here the rule is wrong, and that is worth knowing.")


# ---------------------------------------------------------------- 63 [18] the entrained circadian oscillator: A3 on the domain's own rotor
def _circadian(h=1.0 / 60, days=80, tau=24.6, eps=0.15, th0=1.0):
    """The source row's phase oscillator: d theta/dt = 2 pi/tau + eps max(0, cos(2 pi t/24)) sin(-theta), fixed-grid RK4."""
    def light(t): return eps * max(0.0, math.cos(2 * math.pi * t / 24.0))
    def rhs(t, th): return 2 * math.pi / tau + light(t) * math.sin(-th)
    n = int(round(days * 24 / h)); t = np.arange(n + 1) * h; th = np.empty(n + 1); th[0] = th0
    for i in range(n):
        k1 = rhs(t[i], th[i]); k2 = rhs(t[i] + h / 2, th[i] + h / 2 * k1); k3 = rhs(t[i] + h / 2, th[i] + h / 2 * k2); k4 = rhs(t[i] + h, th[i] + h * k3)
        th[i + 1] = th[i] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return t, th, rhs, light


def r3(n_last=20):
    t, th, rhs, light = _circadian()
    k_last = math.floor(th[-1] / (2 * math.pi)); ks = np.arange(k_last - n_last, k_last + 1)
    t0 = np.interp(ks * 2 * math.pi, th, t); tpi = np.interp(ks * 2 * math.pi + math.pi, th, t)   # sub-sample cut times on the rotor
    D1 = tpi - t0; D2 = t0[1:] - tpi[:-1]; per = np.diff(t0)
    T = float(per.mean()); d1, d2 = float(D1[1:].mean()), float(D2.mean())
    # the domain's own theorem: the half-turn duration is the integral of d theta / v(theta, t(theta)) over the locked orbit
    def quad(start):
        a = (k_last - 1) * 2 * math.pi + start
        g1 = np.linspace(a, a + math.pi, 20001); g2 = np.linspace(a + math.pi, a + 2 * math.pi, 20001)
        tg1 = np.interp(g1, th, t); tg2 = np.interp(g2, th, t)
        v1 = np.array([rhs(tt, gg) for tt, gg in zip(tg1, g1)]); v2 = np.array([rhs(tt, gg) for tt, gg in zip(tg2, g2)])
        return float(np.trapezoid(1 / v1, g1)), float(np.trapezoid(1 / v2, g2)), float(tg1[-1] - tg1[0]), float(tg2[-1] - tg2[0])
    starts = [(s, quad(s)) for s in (0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4)]
    Q1, Q2, _, _ = starts[0][1]
    i0 = int(np.searchsorted(t, t0[-2])); i1 = int(np.searchsorted(t, t0[-1])) + 1
    v = np.array([rhs(t[i], th[i]) for i in range(i0, i1)])
    lit1 = sum(light(tt) > 0 for tt in np.interp(np.linspace(ks[-2] * 2 * math.pi, ks[-2] * 2 * math.pi + math.pi, 2001), th, t)) * (d1 / 2000)
    lit2 = sum(light(tt) > 0 for tt in np.interp(np.linspace(ks[-2] * 2 * math.pi + math.pi, ks[-1] * 2 * math.pi, 2001), th, t)) * (d2 / 2000)
    # the analytic-signal reading on the observable cos(theta): the open INTERNAL of batch 07 row 3, printed and not re-opened
    ph = intrinsic_phase(np.cos(th)); c = antipodal_cuts(ph, start=int(np.searchsorted(t, t0[0]))); dh = np.diff(t[c])
    crr, null, dom = d1, T / 2.0, Q1
    check = abs(d1 + d2 - T) < 1e-6 and rel(d1, Q1) <= 1e-4 and rel(d2, Q2) <= 1e-4
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("bio",
        f"Circadian phase oscillator (free-running 24.6 h) entrained by a light cycle (the source's model: d theta/dt = 2 pi/24.6 + 0.15 max(0, cos(2 pi t/24)) sin(-theta)), fixed-grid RK4 at one-minute steps over 80 days, the last {n_last} cycles read; A3 cuts on the domain's own rotor theta at every half-turn, sub-sample interpolated",
        source=f"{BIO} [18] (DESCR)",
        Q="under entrainment the two A3 occasions of one circadian cycle are unequal in clock time: the half-turn on which the light delays the oscillator runs slower than the half-turn on which it advances it, and each half-turn's duration is the integral of the domain's own phase velocity over that half of the locked orbit",
        ingredient="A3 (the cut at every half-turn of the rotor; the rotor is the domain's own phase theta, so the ingredient has one reading here), D5 (occasion = half-turn), H-L5's clock reading (the source's 'clock-regular') as the null",
        null="the clock: T/2 after the last cut, half the locked period",
        domain="the phase model's own equation: the entrained phase runs at v(theta, t) = 2 pi/tau + Z(theta) L(t), so a half-turn lasts the integral of d theta / v over it (entrainment theory: the phase of entrainment is where the light's net shift per cycle equals tau - T)",
        numbers=(f"locked period {T:.4f} h (CV {cv(per):.1e} with sub-sample crossings; the source's CV 1.1e-02 is its one-minute crossing detector), theta = 0 at clock hour {t0[-1] % 24:.4f} (light peaks at hour 0); half-turn 0 -> pi: {d1:.4f} h (CV {cv(D1[1:]):.1e}; {lit1:.2f} h lit, light term sin(-theta) < 0: delayed), half-turn pi -> 2 pi: {d2:.4f} h (CV {cv(D2):.1e}; {lit2:.2f} h lit, advanced); sum {d1 + d2:.6f}; phase speed on the orbit {v.min():.4f}-{v.max():.4f} rad/h (free-running {2 * math.pi / 24.6:.4f}); quadrature of the domain's velocity field: {Q1:.5f}, {Q2:.5f} h (relative difference from the cuts {rel(d1, Q1):.1e}, {rel(d2, Q2):.1e}); "
                 f"start dependence of the pair (batch 03 row 3): " + ", ".join(f"start {s:.4f} rad: {a_:.4f}/{b_:.4f} h (quadrature {qa:.4f}/{qb:.4f})" for s, (qa, qb, a_, b_) in starts)
                 + f"; analytic-signal reading on the observable cos(theta): {dh[0]:.4f}/{dh[1]:.4f} h (the intrinsic-phase INTERNAL of batch 07 row 3, not the domain's rotor)"),
        tg=f"first half-turn {crr:.4f} h vs null T/2 = {null:.4f} h: {_agree(crr, null)}",
        tn=f"the domain's quadrature gives {dom:.5f} h: {_agree(crr, dom, TOL_N)} (the domain has Q)",
        tc=f"the two half-turns sum to the locked period within 1e-6 h and each matches the quadrature within 1e-4: {_hf(check)}",
        out=out,
        reading=(f"the rotor A3 names is the domain's own phase, so the cut is theta = k pi and everything about its timing is the domain's phase equation: the delayed half lasts {d1:.4f} h and the advanced half {d2:.4f} h, a {abs(d1 - d2):.2f} h asymmetry the light's phase-response builds and the clock reading (12.0000) hides, and the quadrature of the domain's velocity field reproduces both to {max(rel(d1, Q1), rel(d2, Q2)):.1e}; "
                 f"the source row's 'clock-regular and phase-regular at once' is that both halves are locked (CV {max(cv(D1[1:]), cv(D2)):.1e}), and its CV_arc = 0.000 was typed, not computed (on a rotor the arc per cycle is 2 pi by construction, so it is a correct zero). Nothing about the entrainment range or the phase of entrainment ({t0[-1] % 24:.4f} h after the light peak) comes from A3"),
        weakness="a single locked orbit, so H-L5 has no variation to compare; the asymmetry depends on where the cut sequence starts (printed), which is the A3 start dependence already recorded; the observable's analytic-signal phase puts the cuts elsewhere, the open intrinsic-phase INTERNAL, recorded and not re-opened; no after-effect or history dependence is in the source's model, so A6 was not tried on it",
        elegance="",
        child="")


# ---------------------------------------------------------------- 64 [4] the balanced LIF cell: H-L5 taken whole, the reset as the cut
def _balanced_net(T=6.0, seed=4, NE=320, NI=80, K=40, dt=1e-4, n_tr=5):
    """The source row's network (seed 4, N = 400, K = 40, J = 1/sqrt K, instantaneous kicks, dt = 0.1 ms), run for T seconds
    (the source ran 3 s) with the first n_tr E cells' traces and their E, I and leak increments recorded."""
    rng = np.random.default_rng(seed); N = NE + NI
    J = 1.0 / math.sqrt(K); steps = int(T / dt); tau = 0.02; Vth, Vr = 1.0, 0.0
    mE, mI, gE, gI = 2.0, 1.6, 2.0, 1.8
    W = np.zeros((N, N))
    for i in range(N):
        pre_e = rng.choice(NE, K, replace=False); pre_i = NE + rng.choice(NI, K, replace=False)
        W[i, pre_e] = J; W[i, pre_i] = -J * (gE if i < NE else gI)
    h = np.where(np.arange(N) < NE, mE, mI) * math.sqrt(K) * J
    Wp = np.maximum(W, 0.0); Wn = np.minimum(W, 0.0)
    V = rng.random(N) * 0.5; spikes = [[] for _ in range(n_tr)]; nsp = np.zeros(N)
    tr = np.empty((steps, n_tr)); ke = np.zeros((steps, n_tr)); ki = np.zeros((steps, n_tr)); lk = np.zeros((steps, n_tr))
    for s in range(steps):
        fired = V >= Vth; idx = np.where(fired)[0]; nsp[idx] += 1
        for i in idx:
            if i < n_tr: spikes[i].append(s)
        V[fired] = Vr
        if len(idx):
            e_part = Wp[:, idx].sum(axis=1); i_part = Wn[:, idx].sum(axis=1)
        else:
            e_part = np.zeros(N); i_part = np.zeros(N)
        leak = dt * (h - V) / tau
        V += leak + e_part + i_part
        tr[s] = V[:n_tr]; ke[s] = e_part[:n_tr]; ki[s] = i_part[:n_tr]; lk[s] = leak[:n_tr]
    return tr, spikes, ke, ki, lk, nsp / T, dt, N, K, J


def r4(bins=(1, 4, 16, 64), drop=3):
    tr, spikes, ke, ki, lk, rates, dt, N, K, J = _balanced_net()
    rate_e, rate_i = float(rates[:320].mean()), float(rates[320:].mean())
    cells = []
    for i in range(tr.shape[1]):
        ev = np.asarray(spikes[i][drop:])
        rx = regularity(tr[:, i], ev, sigma=1.0, dt=dt, n_boot=1000, segment_end="exclusive")   # the reset is the cut (AGENT_LOG 18)
        ri = regularity(tr[:, i], ev, sigma=1.0, dt=dt, n_boot=1000, segment_end="inclusive")   # the reset jump counted inside every arc
        arcs = np.array([arc_length(tr[a:b, i]) for a, b in zip(ev[:-1], ev[1:])]); isi = np.diff(ev) * dt
        jump = np.array([tr[b - 1, i] - tr[b, i] for b in ev[1:]])                            # the reset jump at each cut
        traffic = np.array([np.abs(ke[a:b - 1, i]).sum() + np.abs(ki[a:b - 1, i]).sum() for a, b in zip(ev[:-1], ev[1:])])
        leak = np.array([np.abs(lk[a:b - 1, i]).sum() for a, b in zip(ev[:-1], ev[1:])])
        net = np.array([(ke[a:b - 1, i] + ki[a:b - 1, i]).sum() for a, b in zip(ev[:-1], ev[1:])])
        cv_pred = rx["cv_arc"] * arcs.mean() / (arcs.mean() + jump.mean())                    # a constant added to every arc: CV falls by <arc>/(<arc> + c)
        per_bin = []
        for sub in bins:
            evs = np.unique(ev // sub); xs = tr[::sub, i]
            rb = regularity(xs, evs, sigma=1.0, dt=dt * sub, n_boot=1000, segment_end="exclusive")
            per_bin.append((sub, rb, len(ev) - len(evs)))
        cells.append(dict(i=i, rx=rx, ri=ri, arcs=arcs, isi=isi, jump=jump, traffic=traffic, leak=leak, net=net, cv_pred=cv_pred,
                          corr=float(np.corrcoef(arcs, isi)[0, 1]), kappa=float(arcs.sum() / isi.sum()), per_bin=per_bin))
    def cls(r):
        lo, hi = r["ci95"]
        return "CI includes 0" if lo <= 0.0 <= hi else _word(r["cv_arc"] < r["cv_clock"], "arc-regular", "clock-regular")
    n_arc_x = sum(cls(c["rx"]) == "arc-regular" for c in cells); n_arc_i = sum(cls(c["ri"]) == "arc-regular" for c in cells)
    n_clock_x = sum(cls(c["rx"]) == "clock-regular" for c in cells)
    n_bare_i = sum(c["ri"]["cv_arc"] < c["ri"]["cv_clock"] for c in cells)                    # the source's bare criterion with the jump counted
    dec = min(cells, key=lambda c: rel(c["rx"]["cv_arc"], c["rx"]["cv_clock"]))              # the cell where arc and clock are closest
    crr, null = dec["rx"]["cv_arc"], dec["rx"]["cv_clock"]
    check = n_arc_x >= 0.8 * len(cells)                                                        # L5x-1's criterion: arc-regular on >= 80 % of units
    out = outcome(crr=crr, null=null, domain=None, check=check)
    coarse = [rb for c in cells for sub, rb, _ in c["per_bin"] if sub > 1]                    # the coarser bins, all cells
    n_below = sum(rb["ci95"][1] < 0.0 for rb in coarse); n_above = sum(rb["ci95"][0] > 0.0 for rb in coarse); n_incl = len(coarse) - n_below - n_above
    n_incl64 = sum(rb["ci95"][0] <= 0.0 <= rb["ci95"][1] for c in cells for sub, rb, _ in c["per_bin"] if sub == 64)
    tie16 = min(rel(rb["cv_arc"], rb["cv_clock"]) for c in cells for sub, rb, _ in c["per_bin"] if sub == 16)   # the closest the two CVs come at 1.6 ms
    return make_row("neur",
        f"Balanced E-I network of leaky integrate-and-fire neurons (the source's network: N = {N}, K = {K}, J = 1/sqrt K = {J:.3f}, instantaneous kicks, dt = 0.1 ms, seed 4), run for 6 s (the source ran 3 s); H-L5 on the first {len(cells)} E cells with the membrane potential as the carrier (identity metric), spikes as own events, the first {drop} dropped; mean rates E {rate_e:.1f} Hz, I {rate_i:.1f} Hz",
        source=f"{EI} [4] (DESCR)",
        Q="a balanced cell belongs to H-L5's arc-regular class: the arc of the membrane potential between its own spikes is a more regular quantity than the interspike interval once the reset jump is the cut and not arc (A3, the reading AGENT_LOG 18 fixed for this row)",
        ingredient="H-L5 (the class claim), D5 [M] (occasion = interspike interval), A3 (the cut has no content: segment_end = exclusive, decided in AGENT_LOG 18 and applied here; the jump-counted reading is printed as the source's earlier one), D6's path against endpoint (arc against the fixed chord of one threshold)",
        null="the clock: the interspike interval, the domain's own statistic (CV ~ 1 in the asynchronous irregular state)",
        domain=None,
        numbers=("; ".join(f"cell {c['i']}: {c['rx']['n']} occasions, reset excluded: CV(arc) = {c['rx']['cv_arc']:.4f}, CV(clock) = {c['rx']['cv_clock']:.4f}, CI95 of the difference [{c['rx']['ci95'][0]:.4f}, {c['rx']['ci95'][1]:.4f}] ({cls(c['rx'])}); reset counted: CV(arc) = {c['ri']['cv_arc']:.4f}, CI95 [{c['ri']['ci95'][0]:.4f}, {c['ri']['ci95'][1]:.4f}] ({cls(c['ri'])}), arithmetic of a constant jump {c['jump'].mean():.3f} sigma added to every arc: {c['cv_pred']:.4f}; per ISI ({c['isi'].mean() * 1e3:.1f} ms): arc {c['arcs'].mean():.2f} sigma against a chord of one threshold, synaptic traffic (E plus |I|) {c['traffic'].mean():.2f}, leak {c['leak'].mean():.2f}, net recurrent input {c['net'].mean():+.2f}, cancellation inside the 0.1 ms bins {(c['traffic'].mean() + c['leak'].mean() - c['arcs'].mean()) / c['arcs'].mean():.3f} of the arc; corr(arc, ISI) = {c['corr']:.4f}, CV(arc/ISI) = {cv(c['arcs'] / c['isi']):.3f}, arc rate {c['kappa']:.1f} sigma/s; arc per ISI at bins " + ", ".join(f"{sub * 0.1:g} ms: {rb['C_mean']:.2f} ({cls(rb)}{', ' + str(dropped) + ' collided' if dropped else ''})" for sub, rb, dropped in c["per_bin"]) for c in cells)
                 + f"; arc-regular on {n_arc_x}/{len(cells)} cells with the reset excluded ({n_clock_x}/{len(cells)} clock-regular); with it counted, CI below 0 on {n_arc_i}/{len(cells)} and the source's bare CV(arc) < CV(clock) on {n_bare_i}/{len(cells)} (its 3-s run: 4/5); at the coarser bins the CI of CV(arc) - CV(clock) lies below 0 on {n_below}/{len(coarse)} cell-bin pairs, includes 0 on {n_incl} and lies above 0 on {n_above}; closest the two CVs come at 1.6 ms: relative difference {tie16:.4f}"),
        tg=f"CV(arc) {crr:.4f} vs null CV(clock) {null:.4f} on the closest cell ({dec['i']}): {_agree(crr, null)} (the arc is not the clock: it carries the traffic's fluctuation)",
        tn="no domain theorem for the arc of the membrane potential; the domain's own path length (leak integral plus summed |kicks|, the total input van Vreeswijk and Sompolinsky scale as sqrt K) is printed per cell and exceeds the sampled arc by the within-bin cancellation",
        tc=f"arc-regular (CI of CV(arc) - CV(clock) below 0) on at least 80 % of cells: {n_arc_x}/{len(cells)}, so Q {_hf(check)}",
        out=out,
        reading=(f"on a fluctuation-driven membrane the arc between spikes is the synaptic traffic the cell received (E plus |I|, {cells[0]['traffic'].mean():.1f} sigma per ISI on cell 0 against a chord of 1), which scales with the ISI (corr {min(c['corr'] for c in cells):.4f}-{max(c['corr'] for c in cells):.4f}) but fluctuates with the network on top of it (CV(arc/ISI) {min(cv(c['arcs'] / c['isi']) for c in cells):.3f}-{max(cv(c['arcs'] / c['isi']) for c in cells):.3f}), so the arc is the clock plus noise: the clock wins on {n_clock_x}/{len(cells)} cells at 0.1 ms, the arc {_word(n_below == 0, 'never wins', 'wins on ' + str(n_below) + ' pairs')} at the coarser bins (it ties the clock on {n_incl} of {len(coarse)} cell-bin pairs, {_word(n_incl64 == 0, 'none', str(n_incl64))} of them at 6.4 ms, where pooled kicks bring the two CVs within {tie16:.4f} of each other at 1.6 ms, the diffusion-carrier reading of batch 12 row 3, and loses again on {n_above} pairs), while the arc itself has no bin-free value ({cells[0]['per_bin'][0][1]['C_mean']:.2f} to {cells[0]['per_bin'][-1][1]['C_mean']:.2f} sigma per ISI from 0.1 to 6.4 ms on cell 0); "
                 f"the arc-regular reading of the earlier battery (bare CV(arc) < CV(clock) on {n_bare_i}/{len(cells)} with the jump counted, CI below 0 on {n_arc_i}/{len(cells)}) is the arithmetic of a constant added to every arc (predicted {cells[0]['cv_pred']:.4f} against {cells[0]['ri']['cv_arc']:.4f} on cell 0), which is what AGENT_LOG 18 found. H-L5 taken whole reads {out} on a spiking carrier with a network behind it, as it read on measles; the source row's DESCR (clock-regular on the rise) stands with its mechanism now printed"),
        weakness="the identity metric on a voltage is the source's stand-in, which A1 does not license (a Fisher carrier would need the membrane's own noise family); five cells of one network at one drive; the traffic decomposition is exact for the simulation's increments, and a third of the traffic cancels inside the 0.1 ms bins because the simulated network is synchronous at that step, so the arc is neither the total nor the net input; the 80 % criterion is L5x-1's, applied to five units",
        elegance="Between two spikes a neuron's voltage is shoved up and down thousands of times by the crowd around it. Add up all that shoving and you mostly get how long the neuron waited, plus the crowd's noise. So counting the travel is a noisier way of counting the wait, and the clock wins.",
        child="A nerve cell in a busy brain gets pushed up and down all the time by its neighbours, like a boat in choppy water. Between one signal and the next it bobs thousands of times. If you add up all the bobbing, you mostly learn how long it waited, but with extra wobble from the choppiness. So the plain stopwatch is the steadier measure here, and CRR's idea that the travelled distance is steadier does not work for this cell.")


# ---------------------------------------------------------------- 65 [6] theta-gamma n:m coupling: natural time outside the tongue
def _theta_gamma(w_th, w_ga, eps, n=5, m=1, T=200.0, dt=1e-3, skip=5):
    """The source row's pair: theta advances at w_th, gamma at w_ga + eps sin(n theta - m gamma) (explicit Euler at 1 ms, the
    source's grid). Returns the real-valued gamma advance per theta cycle and per theta half-turn (sub-sample interpolated) and
    the source's integer count of gamma 2 pi-crossings per theta cycle."""
    th, ga = 0.0, 0.3; steps = int(T / dt)
    ga_at_cycle, ga_at_half, ga_cross, th_cross = [], [], [], []
    for s in range(steps):
        th_new = th + dt * w_th; ga_new = ga + dt * (w_ga + eps * math.sin(n * th - m * ga))
        if math.floor(th_new / (2 * math.pi)) > math.floor(th / (2 * math.pi)):
            k = math.floor(th_new / (2 * math.pi)); f = (2 * math.pi * k - th) / (th_new - th)
            ga_at_cycle.append(ga + f * (ga_new - ga)); th_cross.append(s)
        if math.floor(th_new / math.pi) > math.floor(th / math.pi):
            k = math.floor(th_new / math.pi); f = (math.pi * k - th) / (th_new - th); ga_at_half.append(ga + f * (ga_new - ga))
        if math.floor(ga_new / (2 * math.pi)) > math.floor(ga / (2 * math.pi)): ga_cross.append(s)
        th, ga = th_new, ga_new
    th_cross = np.asarray(th_cross); ga_cross = np.asarray(ga_cross)
    counts = np.diff(np.asarray(ga_at_cycle))[skip:] / (2 * math.pi)
    halves = np.diff(np.asarray(ga_at_half))[2 * skip:] / (2 * math.pi)
    ints = [int(((ga_cross > a) & (ga_cross <= b)).sum()) for a, b in zip(th_cross[skip:-1], th_cross[skip + 1:])]
    return counts, halves, ints


def r5(grid=(0.0, 3.0, 5.0, 6.0, 6.2, 6.5, 25.0), eps_dec=6.0):
    w_th, w_ga, n = 2 * math.pi * 6, 2 * math.pi * 31, 5; dw = w_ga - n * w_th
    res = []
    for eps in grid:
        counts, halves, ints = _theta_gamma(w_th, w_ga, eps)
        adler = n + math.sqrt(max(dw ** 2 - eps ** 2, 0.0)) / w_th             # Adler: beat frequency sqrt(dw^2 - eps^2) outside the tongue, 0 inside
        res.append((eps, float(counts.mean()), cv(counts), adler, sorted(set(ints)), float(halves.mean()), cv(halves)))
    d = [r for r in res if r[0] == eps_dec][0]
    crr, null, dom = d[1], w_ga / w_th, d[3]
    check = all(rel(mean, adler) <= TOL_N for _, mean, _, adler, _, _, _ in res)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    locked = [r for r in res if r[0] == 25.0][0]
    return make_row("neur",
        f"Theta-gamma n:m phase-phase coupling (the source's pair: theta 6 Hz, gamma 31 Hz, gamma pulled by eps sin(5 theta - gamma), 1 ms Euler steps over 200 s); the theta cycle as the occasion (D5) and the gamma cycle as the unit (A1', natural time), the gamma advance per theta cycle read real-valued at sub-sample theta crossings (D2: no integer floor); detuning |w_gamma - 5 w_theta| = {dw:.4f} rad/s, the source's eps = 25 and a grid below the tongue edge",
        source=f"{EI} [6] (DESCR)",
        Q="below the locking threshold the natural-time length of a theta occasion is not the frequency ratio 31/6 but the Adler mean 5 + sqrt(dw^2 - eps^2)/w_theta: coupling pulls the gamma count per theta cycle toward the integer before it locks, and above the threshold every theta half-turn (A3) holds exactly 2.5 gamma cycles",
        ingredient="A1' (the unit as the system's own step: one gamma cycle, natural time), D5 (occasion = one theta cycle), A3 (the half-turn cut on theta), D2 (a real-valued count, no integer floor)",
        null="the uncoupled pair: the gamma advance per theta cycle is the frequency ratio w_gamma/w_theta = 31/6",
        domain="Adler's equation for the phase difference phi = 5 theta - gamma: d phi/dt = dw - eps sin phi locks for eps >= |dw| and otherwise slips at the mean beat frequency sqrt(dw^2 - eps^2), so the mean gamma frequency is 5 w_theta + sqrt(dw^2 - eps^2) (Adler 1946; Pikovsky, Rosenblum and Kurths 2001)",
        numbers="; ".join(f"eps = {eps:g}: gamma cycles per theta cycle {mean:.5f} (Adler {adler:.5f}; CV {c:.4f}), integer count {ints}, per theta half-turn {hm:.4f} (CV {hc:.1e})" for eps, mean, c, adler, ints, hm, hc in res) + f"; uncoupled ratio 31/6 = {w_ga / w_th:.5f}; largest relative gap from Adler over the grid {max(rel(mean, adler) for _, mean, _, adler, _, _, _ in res):.1e}",
        tg=f"natural-time length at eps = {eps_dec:g}: {crr:.5f} vs null (uncoupled ratio) {null:.5f}: {_agree(crr, null)}",
        tn=f"Adler's formula gives {dom:.5f}: {_agree(crr, dom, TOL_N)} (the domain has Q)",
        tc=f"the natural-time length matches Adler within 1 % at every eps on the grid, locked and unlocked: {_hf(check)}",
        out=out,
        reading=(f"reading the theta occasion in gamma cycles does something the frequency ratio does not (at eps = {eps_dec:g} the count is {crr:.5f}, not {null:.5f}), and what it does is Adler's beat: the count is 5 plus the slip rate in units of the theta frequency, {max(rel(mean, adler) for _, mean, _, adler, _, _, _ in res):.1e} from the closed form across the grid; "
                 f"above the tongue edge the count is 5 to {abs(locked[1] - 5):.1e} with CV {locked[2]:.1e} and each A3 half-turn of theta holds {locked[5]:.4f} gamma cycles, so the source row's 'constant by definition of locking' stands and the unlocked regime adds only what the domain's own equation already says. The Tucker-Luu 'persists long enough' clause is untouched: a threshold in gamma cycles and one in clock time still coincide at fixed theta frequency"),
        weakness="the source's model is two phases with a sinusoidal coupling, the first-order Adler case; a waveform-driven coupling would lock through the drive's fifth harmonic and change the tongue, not the reading; the integer count is the source's statistic and the real-valued count is D2's, both printed; citations by name and year only, not fetched here (R10)",
        elegance="",
        child="")


def main():
    return run_batch("Synthesis batch 13: rows 61-65 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
