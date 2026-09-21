"""Synthesis batch 14: rows 66-70 of QUEUE.md (prompt-log entry 61). E-I battery [9] homeostatic synaptic scaling
restoring a target rate after an E/I perturbation (DESCR); [10] cortical travelling wave, ring of coupled phase
oscillators in the twisted state (DESCR); [11] population Fisher information with differential correlations (DESCR);
driven-systems battery [2] Olami-Feder-Christensen earthquake automaton (DESCR); [3] Kramers escape in a double well,
unforced and periodically forced (DESCR). The source rows are in theory/retrodictions/ei_networks.txt and
theory/retrodictions/driven_systems.txt; their models are re-implemented here (nothing imported from the battery
scripts). Deterministic (fixed seeds, fixed grids, explicit RK4 and Euler-Maruyama); no data file opened (R2). Run:
  uv run python theory/retrodictions/synthesis_batches/batch_14.py
"""
import math
import sys

import numpy as np
from scipy.ndimage import uniform_filter1d

from crr.instrument.core import cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC_EI = "theory/retrodictions/ei_networks.txt"
SRC_DRV = "theory/retrodictions/driven_systems.txt"


def _word(cond, yes, no):
    return yes if cond else no


def _agree(a, b, tol=TOL_G):
    return _word(rel(a, b) <= tol, "agree", "differ")


def _f4(v):
    """A settled value at four decimals, or the word for a loop that diverged."""
    return f"{v:.4f}" if math.isfinite(v) else "diverges"


def _fdet(d):
    """A determinant at four decimals unless it is zero to finite-difference noise, then in exponent form."""
    return f"{d:.4f}" if abs(d) >= 1e-6 else f"{d:.1e}"


def _boot_cv_diff(a, b, n_boot=2000, seed=0):
    """Paired bootstrap 95 % CI of CV(a) - CV(b) over occasions (the instrument's own construction, on two named clocks)."""
    a, b = np.asarray(a, float), np.asarray(b, float); rng = np.random.default_rng(seed); d = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(a), len(a)); d.append(cv(a[idx]) - cv(b[idx]))
    lo, hi = np.percentile(d, [2.5, 97.5]); return float(lo), float(hi)


# ---------------------------------------------------------------- 66 [9] homeostatic scaling with an A6 set point
GAMMA, R_T, TAU_H = 20.0, 5.0, 50.0        # the source: rate = 20 g, target 5 Hz, scaling time constant 50


def _setpoint_rules():
    """Set-point rules as (statistic of the settled rate, set point from the P3-weighted memory m of that statistic).
    'fixed' is the domain's synaptic scaling (a constant); 'a6' is the Fisher-Rao Frechet mean of the settled rates on the
    Poisson-rate carrier (the mean of sqrt r, squared); 'euclid' the arithmetic mean (the Euclidean Frechet mean);
    'bcm' the degree-2 sliding threshold of Bienenstock-Cooper-Munro (mean of r^2 over the target)."""
    return {"fixed": (lambda r: r, lambda m: R_T),
            "a6": (lambda r: math.sqrt(r), lambda m: m * m),
            "euclid": (lambda r: r, lambda m: m),
            "bcm": (lambda r: r * r, lambda m: m / R_T)}


def _degree(rule):
    """Homogeneity degree of the set point in the rate scale: the response to a doubled constant history."""
    stat, theta = rule
    return math.log(theta(stat(2.0 * R_T)) / theta(stat(R_T))) / math.log(2.0)


def _step(rule, q, loop):
    """One occasion (one time unit) of the closed loop: (g, m) -> (g', m'). Scaling loop: g' = g + (theta - r)/tau_h
    (the source's integral controller). Hebbian loop: g' = g + eta g (r - theta), eta chosen so that the linear loop gain
    equals the scaling loop's (eta r_T = gamma/tau_h)."""
    stat, theta = rule; eta = GAMMA / (TAU_H * R_T)
    def f(g, m):
        r = GAMMA * g; th = theta(m)
        g2 = g + (th - r) / TAU_H if loop == "scaling" else g + eta * g * (r - th)
        return g2, (1.0 - q) * stat(r) + q * m
    return f


def _jac_cont(f, g, m, h=1e-6):
    """Continuous-time Jacobian J = (F - I)/Delta at (g, m), Delta = 1, by central differences of the one-step map."""
    def F(v):
        return np.array(f(v[0], v[1]))
    v = np.array([g, m]); J = np.zeros((2, 2))
    for j in range(2):
        e = np.zeros(2); e[j] = h; J[:, j] = (F(v + e) - F(v - e)) / (2.0 * h)
    return J - np.eye(2)


def _run_loop(rule, q, loop="scaling", g0=0.3, n_occ=4000):
    stat, theta = rule; f = _step(rule, q, loop); g, m = g0, stat(R_T)      # the memory holds the settled 5 Hz history
    r0 = GAMMA * g
    for _ in range(n_occ):
        g, m = f(g, m)
    return r0, GAMMA * g


def r1():
    rules = _setpoint_rules(); q = 0.9                                     # P3 age weights q^k, mean age q/(1 - q) = 9 occasions
    deg = {k: _degree(v) for k, v in rules.items()}
    res = {k: _run_loop(v, q) for k, v in rules.items()}                    # scaling loop, the source's perturbation (6 -> ? Hz)
    dets = {k: float(np.linalg.det(_jac_cont(_step(v, q, "scaling"), R_T / GAMMA, v[0](R_T)))) for k, v in rules.items()}
    sweep = {qq: _run_loop(rules["a6"], qq)[1] for qq in (0.5, 0.9, 0.99)}
    tau_m = {qq: qq / (1.0 - qq) for qq in sweep}
    # the zero eigenvalue's conserved quantity of the discrete loop: (1 - q) r + (gamma/tau_h) theta is constant, so the loop
    # settles at ((1 - q) r0 + (gamma/tau_h) r_T)/((1 - q) + gamma/tau_h); exact for the linear (Euclidean) rule, first order for A6
    lin = {qq: ((1.0 - qq) * res["a6"][0] + (GAMMA / TAU_H) * R_T) / ((1.0 - qq) + GAMMA / TAU_H) for qq in sweep}
    lin_euclid = ((1.0 - q) * res["euclid"][0] + (GAMMA / TAU_H) * R_T) / ((1.0 - q) + GAMMA / TAU_H)
    heb = {}
    for k in ("a6", "bcm"):
        for qq in (0.5, 0.9):
            J = _jac_cont(_step(rules[k], qq, "hebbian"), R_T / GAMMA, rules[k][0](R_T))
            ev = np.linalg.eigvals(J); heb[(k, qq)] = (float(np.linalg.det(J)), float(np.trace(J)), bool(np.all(ev.real < 0)))
    crr, null, dom = res["a6"][1], res["fixed"][1], R_T
    check = abs(crr - R_T) <= 0.01 * R_T
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    d_a6 = deg["a6"]
    return make_row("plast",
        f"Homeostatic synaptic scaling (the source's loop: rate r = {GAMMA:g} g, gain g relaxing as dg/dt = (set point - r)/{TAU_H:g}, an E/I perturbation that has raised the rate to {res['fixed'][0]:.2f} Hz) with the set point read four ways: the domain's constant {R_T:g} Hz; A6's regeneration, the Fisher-Rao Frechet mean of the settled rates on the Poisson-rate carrier (mean of sqrt r, squared) under P3 age weights q = {q:g}; its Euclidean replacement (the arithmetic mean); and the BCM degree-2 sliding threshold; occasions of one time unit",
        source=f"{SRC_EI} [9] (DESCR)",
        Q="a homeostatic set point regenerated from the settled past at bounded strength (A6 with P3 weights) is a sliding set point of degree 1 in the rate, so the loop has a zero eigenvalue and a perturbation leaves a permanent offset: homeostatic scaling under A6 does not restore the target rate",
        ingredient="A6 (regeneration from settled occasions by a bounded Frechet mean, never an accumulated count), P3 (age weights q^k), D5 (occasion = one sensing window of one time unit), A1 on the Poisson-rate carrier (the Frechet mean is taken in sqrt r)",
        null="the domain's set point: a constant (synaptic scaling as first-order relaxation to a fixed target, the source's model)",
        domain="Turrigiano 1998 / 2008 (named only, not fetched, R10): synaptic scaling returns the firing rate to its set point; Bienenstock-Cooper-Munro 1982 and Intrator-Cooper 1992 (named only, not fetched): a sliding threshold must be superlinear in the mean rate (degree p > 1) for the Hebbian loop to be stable, and it must slide faster than the weights change",
        numbers=(f"scaling loop, q = {q:g}, {4000} occasions from r0 = {res['fixed'][0]:.2f} Hz: settled rate under the fixed set point {_f4(res['fixed'][1])} Hz, under A6 {_f4(res['a6'][1])}, under the Euclidean mean {_f4(res['euclid'][1])} (the linear loop's conserved quantity gives {lin_euclid:.4f}), under BCM degree 2 {_f4(res['bcm'][1])}; "
                 f"homogeneity degree of the set point: fixed {deg['fixed']:.4f}, A6 {d_a6:.4f}, Euclidean {deg['euclid']:.4f}, BCM {deg['bcm']:.4f}; "
                 f"det of the linearised loop (closed form (1 - q)(gamma/tau_h)(1 - d) = {(1 - q) * GAMMA / TAU_H:.4f} (1 - d)): fixed {_fdet(dets['fixed'])}, A6 {_fdet(dets['a6'])}, Euclidean {_fdet(dets['euclid'])}, BCM {_fdet(dets['bcm'])}; "
                 f"A6 settled rate against q: " + ", ".join(f"q = {qq:g} (P3 mean age {tau_m[qq]:.0f}): {_f4(sweep[qq])} Hz (conserved-quantity prediction {lin[qq]:.4f})" for qq in sweep) + "; "
                 f"Hebbian loop (the domain's BCM loop, eta r_T = gamma/tau_h): " + ", ".join(f"{k} at q = {qq:g}: det {_fdet(d_)}, trace {t_:.4f}, {'stable' if s_ else 'unstable'}" for (k, qq), (d_, t_, s_) in heb.items())),
        tg=f"settled rate under A6 {crr:.4f} Hz vs null (fixed set point) {null:.4f} Hz: {_agree(crr, null)}",
        tn=f"the domain's set point gives {dom:.4f} Hz (restoration): the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"the A6 loop restores the target within 1 % (|r - r_T| <= {0.01 * R_T:.2f} Hz): {_word(check, 'holds', 'fails')} (offset {crr - R_T:+.4f} Hz)",
        out=out,
        reading=(f"put where the domain puts its set point, A6 is the sliding threshold of degree {d_a6:.0f}: every Frechet mean of rates is homogeneous of degree 1 whatever the metric (A6 and its Euclidean replacement give the same degree, {d_a6:.4f} and {deg['euclid']:.4f}, and settle {abs(res['a6'][1] - res['euclid'][1]):.4f} Hz apart), and degree 1 is the marginal case in both of the domain's loops: the scaling loop needs a degree below 1 (its constant, degree 0, restores; degree 2 is a saddle, det {_fdet(dets['bcm'])}, and its loop {_f4(res['bcm'][1])}) and the Hebbian loop needs a degree above 1 (BCM's p > 1: at degree 2 and q = 0.5 the loop is {'stable' if heb[('bcm', 0.5)][2] else 'unstable'}, at degree 1 its det is {_fdet(heb[('a6', 0.5)][0])}); "
                 f"A6 restores only as q -> 1, where the set point stops regenerating and becomes the domain's constant (offset {sweep[0.5] - R_T:.4f} Hz at q = 0.5, {sweep[0.99] - R_T:.4f} at q = 0.99); the source's 'depth one' verdict stands and the synthesis adds that A6 read as a set point contradicts the restoration the domain defines homeostasis by"),
        weakness="q is a knob CRR does not fix (P3) and the decisive number moves with it; the occasion is one sensing window, a modelling choice; the Hebbian loop's stability also needs the threshold to slide faster than the weights (trace < 0), which at q = 0.9 fails for BCM too, so the domain's own rule is reproduced only at the faster memory; the BCM and Turrigiano citations are named, not fetched (R10)",
        elegance="A thermostat that sets its target to the average of the temperatures it has felt lately will follow the room instead of fixing it. Memory of the past makes a fine sensor and a useless goal: one sentence, no knobs.",
        child="A thermostat keeps a room at one number: too warm, it cools; too cold, it heats. Imagine a thermostat that decided what 'just right' means by averaging the last few days. After a hot week it would settle for hotter, and after a cold week for colder. It would never pull the room back to the same place, because its goal keeps moving with its memory.")


# ---------------------------------------------------------------- 67 [10] the twisted state's own limit: antipode or extremum
N_RING, KAPPA = 60, 40.0                                                   # the source's ring: N = 60 sites, coupling 40


def _ring_rhs(th):
    return KAPPA * (np.sin(np.roll(th, -1) - th) + np.sin(np.roll(th, 1) - th))     # the rotating frame (omega drops out)


def _ring_jacobian(q):
    """The Kuramoto ring's own linearisation at the q-twisted state: J_jk = kappa cos(theta_k - theta_j) on neighbours."""
    th = 2.0 * math.pi * q * np.arange(N_RING) / N_RING; J = np.zeros((N_RING, N_RING))
    for j in range(N_RING):
        for k in ((j - 1) % N_RING, (j + 1) % N_RING):
            J[j, k] = KAPPA * math.cos(th[k] - th[j]); J[j, j] -= KAPPA * math.cos(th[k] - th[j])
    return J


def _ring_lam_max(q):
    ev = np.sort(np.linalg.eigvalsh(_ring_jacobian(q)))
    return float(ev[-2])                                                    # the largest eigenvalue after the rotation mode (0)


def _ring_evolve(q, T=2.0, dt=1e-3, amp=0.05, seed=11):
    rng = np.random.default_rng(seed)
    th = 2.0 * math.pi * q * np.arange(N_RING) / N_RING + amp * rng.standard_normal(N_RING)
    for _ in range(int(round(T / dt))):
        k1 = _ring_rhs(th); k2 = _ring_rhs(th + 0.5 * dt * k1); k3 = _ring_rhs(th + 0.5 * dt * k2); k4 = _ring_rhs(th + dt * k3)
        th = th + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
    dif = np.angle(np.exp(1j * np.diff(np.append(th, th[0]))))
    return int(round(dif.sum() / (2.0 * math.pi))), float(np.std(dif))      # winding number, spread of the neighbour gaps


def r2():
    lam = {q: _ring_lam_max(q) for q in range(0, N_RING // 2 + 1)}
    q_stable = max(q for q in lam if lam[q] < -1e-9)
    q_marg = [q for q in lam if abs(lam[q]) <= 1e-9]
    q_a3, q_ext = N_RING / 2.0, N_RING / 4.0                                # antipode (gap pi) and extremum of the coupling force (gap pi/2)
    sims = {q: _ring_evolve(q) for q in (10, 14, 15, 16, 20, 30)}
    crr, null, dom = q_a3, q_ext, q_ext
    check = lam[int(q_a3)] < 0 and sims[int(q_a3)][0] == int(q_a3)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    shown = (1, 7, 10, 14, 15, 16, 20, 30)
    return make_row("wave",
        f"The source's cortical travelling wave: a ring of N = {N_RING} phase oscillators with nearest-neighbour coupling kappa = {KAPPA:g} in the q-twisted state (neighbour phase gap 2 pi q/N, wave speed omega/gap); the ring's own event is the breaking of the wave (a phase slip that changes the winding number q); fixed-grid RK4, dt = 1e-3, 2 time units, gap noise 0.05 rad",
        source=f"{SRC_EI} [10] (DESCR)",
        Q="the largest twist a ring can carry is set by the antipode: the wave breaks when neighbouring sites are half a turn apart (gap pi, q = N/2), so every twisted state with a gap below pi is stable (H-CUT's antipode reading of the ring's own event, against the extremum of the coupling force at a quarter turn)",
        ingredient="A3 (the cut at the antipode of the intrinsic phase, read on the wave's own phase variable, the neighbour gap), D5 (occasion = one winding), H-CUT (own event at the antipode rather than at the extremum)",
        null="the extremum: the neighbour gap at which the coupling force sin(gap) is largest, a quarter turn (q = N/4)",
        domain="Wiley, Strogatz & Girvan 2006, 'The size of the sync basin' (named only, not fetched, R10): the q-twisted state of the nearest-neighbour Kuramoto ring is linearly stable iff cos(2 pi q/N) > 0, i.e. q < N/4",
        numbers=(f"largest Jacobian eigenvalue after the rotation mode at q = " + ", ".join(f"{q}: {lam[q]:.4g}" for q in shown) + f"; largest strictly stable twist {q_stable} (gap {2 * math.pi * q_stable / N_RING:.4f} rad), marginal at q = {', '.join(str(q) for q in q_marg)} (gap {math.pi / 2:.4f} = pi/2: the Jacobian vanishes), unstable above; "
                 f"antipode q = {q_a3:g} (gap {math.pi:.4f}), extremum of the coupling force q = {q_ext:g} (gap {math.pi / 2:.4f}); "
                 f"simulated winding number after 2 time units from the q-twisted state plus noise: " + ", ".join(f"q = {q}: {w} (gap spread {s:.4f} rad)" for q, (w, s) in sims.items())),
        tg=f"A3 limit q = {crr:g} vs null (extremum of the coupling force) q = {null:g}: {_agree(crr, null)}",
        tn=f"the domain's linear stability puts the boundary at q = {dom:g} (cos(2 pi q/N) = 0), which {_word(rel(crr, dom) <= TOL_N, 'is', 'is not')} the A3 value: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"the antipodal twist q = {q_a3:g} is stable (its largest eigenvalue {lam[int(q_a3)]:.4g}, required below 0; its winding number after evolution {sims[int(q_a3)][0]}, required {q_a3:g}): {_word(check, 'holds', 'fails')}; the twists between the extremum and the antipode {_word(sims[16][0] < 16 and sims[20][0] < 20, 'collapse', 'persist')} (q = 16 -> {sims[16][0]}, q = 20 -> {sims[20][0]}) while q = 10 and 14 {_word(sims[10][0] == 10 and sims[14][0] == 14, 'keep theirs', 'do not keep theirs')} ({sims[10][0]}, {sims[14][0]})",
        out=out,
        reading=(f"the ring's own event sits at the extremum, not at the antipode: a twist survives only while the pull between neighbours is still growing, and the pull sin(gap) peaks at a quarter turn, so the boundary is q = {q_ext:g}, half the antipodal value {q_a3:g}, and the null and the domain coincide there; H-CUT read on the wave's own phase variable is contradicted by the domain's linearisation, and the source row's 'each site cuts every half-turn by definition' remains the only place the antipode appears on this ring; "
                 f"the winding number the ring keeps ({q_stable} at most, {sims[15][0]} from the marginal q = 15) is the domain's, and the wave speed omega/gap that the source recorded is bounded below by omega/(pi/2), not by omega/pi"),
        weakness="H-CUT is written for temporal cuts on one carrier and is read here on the spatial phase gap of a wave, a transfer the class allows and the expert may reject; nearest-neighbour sine coupling only (a second harmonic or a phase lag moves the extremum, and with it the domain's boundary, not the antipode); the marginal q = 15 is decided by the simulation, not by the vanishing Jacobian",
        elegance="A circle of people holding hands, each turned a little more than the last, can keep the twist only while every pair's pull is still growing; at a quarter turn the pull is as strong as hands get, and past it the circle breaks, long before anyone faces backwards. One picture, one number: a quarter, not a half.",
        child="Imagine friends in a circle holding hands, each one turned a bit more than the one before, so the turn goes all the way round. The circle holds as long as each pair is turned less than a quarter turn from each other, because that is where hands pull hardest. Turn more than that and hands slip apart, even though nobody is facing backwards yet.")


# ---------------------------------------------------------------- 68 [11] the population's unit under differential correlations
def r3():
    fprime, sig2, eps = 1.0, 1.0, 0.05                                     # the source's tuning slope, private variance, differential-correlation strength
    Ns = (10, 100, 1000, 10000)
    I_form = {N: N * fprime ** 2 / sig2 / (1.0 + eps * N * fprime ** 2 / sig2) for N in Ns}         # Sherman-Morrison (the source)
    I_direct = {}
    for N in (10, 100, 1000):
        fp = np.full(N, fprime); S = sig2 * np.eye(N) + eps * np.outer(fp, fp)
        I_direct[N] = float(fp @ np.linalg.solve(S, fp))
    unit = {N: 1.0 / math.sqrt(I_form[N]) for N in Ns}                     # A1': the population's own resolvable step
    private = {N: math.sqrt(sig2 / (N * fprime ** 2)) for N in Ns}         # the private-noise step, which averages away
    eq_input = {N: math.sqrt(eps + sig2 / (N * fprime ** 2)) for N in Ns}   # the domain: differential correlations = stimulus noise of variance eps
    Nmax = Ns[-1]
    crr, null, dom = unit[Nmax], private[Nmax], eq_input[Nmax]
    check = all(unit[N] >= math.sqrt(eps) for N in Ns)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("code",
        f"The source's population code: N neurons with tuning slope f' = {fprime:g}, private variance {sig2:g} and differential correlations Sigma = {sig2:g} I + {eps:g} f' f'^T (Moreno-Bote et al. 2014), Fisher information I_pop = f'^T Sigma^-1 f'",
        source=f"{SRC_EI} [11] (DESCR)",
        Q="the unit A1' names for the population (its own resolvable step, 1/sqrt I_pop) does not average away with N: it floors at sqrt(eps), the stimulus-equivalent jitter that the differential correlations are, while the private-noise step (the sample-level noise A1' excludes) falls as 1/sqrt N",
        ingredient="A1'/D1 (the unit is the system's own resolvable step, and the recording noise is not the unit; rho = extent/unit)",
        null="the private-noise reading of the unit: sigma/(sqrt N f'), the step set by the independent noise alone (the instrument-noise reading A1' excludes)",
        domain="Moreno-Bote, Beck, Kanitscheider, Pitkow, Latham & Pouget 2014 (Nature Neuroscience 17:1410; named only, not fetched, R10): differential correlations are equivalent to noise in the stimulus of variance eps, so 1/I_pop = eps + sigma^2/(N f'^2) and information saturates at 1/eps",
        numbers=(f"I_pop by the formula at N = " + ", ".join(f"{N}: {I_form[N]:.4f}" for N in Ns) + f" (saturation 1/eps = {1 / eps:g}); direct solve of the N x N covariance at N = " + ", ".join(f"{N}: {I_direct[N]:.4f} (|difference| {abs(I_direct[N] - I_form[N]):.1e})" for N in I_direct) + "; "
                 f"A1' unit 1/sqrt I_pop at N = " + ", ".join(f"{N}: {unit[N]:.4f}" for N in Ns) + f" (floor sqrt(eps) = {math.sqrt(eps):.4f}); private-noise step at N = " + ", ".join(f"{N}: {private[N]:.4f}" for N in Ns) + "; "
                 f"domain's stimulus-equivalent-noise unit sqrt(eps + sigma^2/(N f'^2)) at N = {Nmax}: {dom:.6f} against the A1' unit {crr:.6f} (|difference| {abs(crr - dom):.1e}); rho across a unit stimulus range (D1, reported only) at N = {Nmax}: {1.0 / unit[Nmax]:.2f} under A1', {1.0 / private[Nmax]:.2f} under the private-noise reading"),
        tg=f"A1' unit {crr:.4f} vs null (private-noise step) {null:.4f} at N = {Nmax}: {_agree(crr, null)}",
        tn=f"the equivalent-input-noise decomposition gives {dom:.4f}: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"unit >= sqrt(eps) at every N: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=("A1''s two clauses (the unit is the system's own step; the instrument's noise is not the unit) are, on this domain, the theorem the source row already inherited: the differential-correlation floor is the stimulus jitter the population cannot see past, and the private noise is what averages away; CRR names the floor as the unit and the domain had both the floor and its decomposition; D1's rho is the domain's count of discriminable stimuli"),
        weakness="CRR-proper ingredients tried and dropped: A6 with neurons as occasions (the Frechet mean's spread would stay at the single-neuron unit, contradicting the domain's saturation as synthesis.py row 3 contradicts Bayes; a population is not a sequence of occasions in time, so no Q was formed); A3/D5 and H-L5 (no events of the population's own); A1' read as one spike against one Cramer-Rao step is batch 01 row 3's INTERNAL on the Poisson carrier and is not repeated; whether the organism's resolvable step (the behavioural threshold) or the population's is 'the system's own' is a data question, absent from data/SEEN.md",
        elegance="A crowd reading one slightly wrong clock cannot know the time better than that clock, however many people you ask. The shared error is the smallest step anyone can tell apart.",
        child="If a hundred children all read the same clock that runs a little wrong, asking more children does not fix the clock. Their private mistakes cancel out when you ask many of them, but the clock's mistake is in every answer. So the smallest difference the crowd can notice is set by the clock, not by how big the crowd is.")


# ---------------------------------------------------------------- 69 [2] Olami-Feder-Christensen: the arc of the mean stress as the stress budget
def _ofc(L=32, alpha=0.2, n_av=30000, seed=2):
    """The source's automaton: uniform loading to the next toppling, synchronous toppling, open boundaries, conservation alpha.
    Returns sizes, the mean stress after loading (before the avalanche), after the avalanche, and the loading increments."""
    rng = np.random.default_rng(seed); z = rng.random((L, L)) * 0.9
    sizes = np.empty(n_av, int); m_pre = np.empty(n_av); m_post = np.empty(n_av); gaps = np.empty(n_av)
    for a in range(n_av):
        gap = 1.0 - z.max(); z += gap; gaps[a] = gap; m_pre[a] = z.mean()
        s = 0
        while True:
            top = z >= 1.0
            if not top.any():
                break
            s += int(top.sum()); load = alpha * np.where(top, z, 0.0); z[top] = 0.0
            z[1:, :] += load[:-1, :]; z[:-1, :] += load[1:, :]; z[:, 1:] += load[:, :-1]; z[:, :-1] += load[:, 1:]
        sizes[a] = s; m_post[a] = z.mean()
    return sizes, m_pre, m_post, gaps


def r4():
    sizes, m_pre, m_post, gaps = _ofc(); tr = 10000; thr = 64
    sizes, m_pre, m_post, gaps = sizes[tr:], m_pre[tr:], m_post[tr:], gaps[tr:]; drops = m_pre - m_post
    big = np.where(sizes >= thr)[0]
    saw = np.empty(2 * len(m_pre)); saw[0::2] = m_pre; saw[1::2] = m_post   # the sawtooth: loading up, avalanche down
    ev = 2 * big + 1                                                         # the sample just after each large drop
    C = np.array([float(np.abs(np.diff(saw[a:b])).sum()) for a, b in zip(ev[:-1], ev[1:])])   # exclusive: the large drop is the cut (A3)
    cg = np.concatenate([[0.0], np.cumsum(gaps)]); cd = np.concatenate([[0.0], np.cumsum(drops)])
    T = np.array([cg[b + 1] - cg[a + 1] for a, b in zip(big[:-1], big[1:])])   # loading from after large event a to the onset of large event b
    R = np.array([cd[b] - cd[a + 1] for a, b in zip(big[:-1], big[1:])])       # release by the small avalanches between them
    D = drops[big[1:]]                                                          # the terminating large drop (the cut's content, left out)
    count = np.diff(big).astype(float)                                          # the source's clock: avalanches between large events
    ident = float(np.abs(C - (T + R)).max())
    ci_load = _boot_cv_diff(C, T); ci_count = _boot_cv_diff(C, count)
    r_src = regularity(m_post, big, sigma=1.0, dt=1.0, n_boot=500, segment_end="exclusive")   # the source's carrier and clock
    corr_TR = float(np.corrcoef(T, R)[0, 1]); corr_Tcount = float(np.corrcoef(T, count)[0, 1])
    from scipy.stats import spearmanr
    rho_level = float(spearmanr(T[1:], m_post[big[1:-1]])[0]); rho_tp = float(spearmanr(T[1:], D[:-1])[0])
    rho_arc = float(spearmanr(T[1:], C[:-1])[0])                                # does the last occasion's arc predict the next loading?
    noisier = _word(cv(count) > cv(T), "the noisier", "the less noisy")
    crr, null, dom = cv(C), cv(T), cv(T + R)
    check = ident < 1e-9
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    cls_load = "arc-regular" if crr < null else "clock-regular"
    cls_count = "arc-regular" if r_src["cv_arc"] < r_src["cv_clock"] else "clock-regular"
    return make_row("g",
        f"The source's Olami-Feder-Christensen automaton (L = 32, alpha = 0.2, seed 2, {len(sizes)} avalanches after a transient of {tr}), large events = avalanches of >= {thr} sites ({len(big)} of them), carrier = the mean stress as a sawtooth (one sample after each loading, one after each avalanche), the large drop left out of the occasion (exclusive segmentation, A3: the jump is the cut)",
        source=f"{SRC_DRV} [2] (DESCR)",
        Q="between two large events the Fisher arc of the mean stress is the loading plus the release of the small avalanches in between (the domain's stress budget), so H-L5's arc-regular class on this carrier is the covariance of release with load and not a regularity of the arc's own; the source's arc-regular verdict was taken against the avalanche count, a noisier clock than the loading",
        ingredient="H-L5 (the class claim), D5 (own events = the large avalanches), A1' (natural time = the avalanche count, the source's clock), D2 with the identity metric (the arc = total variation of the mean stress)",
        null="the clock: the loading between large events (the drive, uniform in the automaton: the domain's physical time)",
        domain="the stress budget (Reid 1910's elastic rebound as a ledger; Brune 1968's moment balance, named only, not fetched, R10): the stress path between two events is the load in plus the release out, and the release is the load minus the net change of level",
        numbers=(f"per occasion ({len(C)} occasions): mean arc {C.mean():.4f}, mean loading {T.mean():.4f}, mean small-avalanche release {R.mean():.4f}, mean large drop {D.mean():.4f} (left out); identity C = T + R: max |C - (T + R)| = {ident:.1e}; "
                 f"CV(arc) {crr:.4f}, CV(loading) {null:.4f}, CV(release) {cv(R):.4f}, CV(count) {cv(count):.4f}, CV(large drop) {cv(D):.4f}; paired-bootstrap 95 % CI of CV(arc) - CV(loading) [{ci_load[0]:.4f}, {ci_load[1]:.4f}], of CV(arc) - CV(count) [{ci_count[0]:.4f}, {ci_count[1]:.4f}]; "
                 f"corr(loading, release) {corr_TR:.4f}, corr(loading, count) {corr_Tcount:.4f}; the source's carrier (mean stress after each avalanche) against the count clock: CV(arc) {r_src['cv_arc']:.4f} vs CV(count) {r_src['cv_clock']:.4f}, CI [{r_src['ci95'][0]:.4f}, {r_src['ci95'][1]:.4f}] -> {cls_count}; "
                 f"Spearman of the loading to the next large event with the mean stress just after the last one {rho_level:.4f}, with the size of the last large drop (the time-predictable reading) {rho_tp:.4f}, and with the arc of the last occasion {rho_arc:.4f}"),
        tg=f"CV(arc) {crr:.4f} vs null CV(loading) {null:.4f}: {_agree(crr, null)} (class on the loading clock: {cls_load})",
        tn=f"the stress budget gives CV(load + release) = {dom:.4f}: the domain {_word(rel(crr, dom) <= TOL_N, 'has', 'does not have')} Q",
        tc=f"the arc is the budget to 1e-9: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"on a uniformly loaded sawtooth the arc is a ledger the domain keeps already: load in plus release out, and the release tracks the load (corr {corr_TR:.4f}), so the arc is {C.mean() / T.mean():.2f} times the loading with the loading's variability plus the release's scatter; against the loading clock the class is {cls_load} (CI of the difference [{ci_load[0]:.4f}, {ci_load[1]:.4f}]), against the source's count clock it is {cls_count}, and the {_word(cls_load != cls_count, 'flip', 'agreement')} is the clock's, not the arc's: the count of small avalanches per unit load is {noisier} of the two clocks; "
                 f"what predicts the next loading in the automaton is {_word(abs(rho_level) > abs(rho_arc), 'the level, not the arc', 'the arc rather than the level')} (Spearman {rho_level:.4f} with the post-event mean stress, {rho_arc:.4f} with the last occasion's arc, {rho_tp:.4f} with the last drop), which is the domain's stress-level recurrence and not a CRR quantity"),
        weakness="one L, one alpha, one threshold for 'large'; T-N is a conservation identity, exact by construction, so the checkable content of Q is the release-load covariance, which is the automaton's; a fault with a varying loading rate (the spring-slider row's class B) is the case where arc and load separate, and the automaton cannot supply it",
        elegance="Pour sand in at a steady rate and let it trickle out in little slides: the total sand that moved is the pouring counted twice, less what stayed. The odometer of the pile is its ledger, and the ledger was already kept.",
        child="If you pour sand onto a pile at a steady rate and it keeps sliding off in small slides, then all the sand that moved is just the sand you poured in plus the sand that slid out. Adding up every up and down does not tell you anything new: it is the pouring, counted twice.")


# ---------------------------------------------------------------- 70 [3] Kramers escape: the unit on a noisy bistable carrier
def _double_well(A, period, seed=3, dt=0.01, n=2_000_000, sig=0.4):
    """The source's overdamped particle in x^4/4 - x^2/2 with noise sig and forcing A cos(2 pi t/period); events with hysteresis +/- 0.5."""
    rng = np.random.default_rng(seed); x = -1.0; xs = np.empty(n); side = -1; ev = []
    w = 2.0 * math.pi / period if period else 0.0; noise = rng.standard_normal(n) * sig * math.sqrt(dt)
    for k in range(n):
        x += dt * (x - x ** 3 + A * math.cos(w * k * dt)) + noise[k]; xs[k] = x
        if side < 0 and x > 0.5:
            side = 1; ev.append(k)
        elif side > 0 and x < -0.5:
            side = -1; ev.append(k)
    return xs, np.array(ev)


def _two_state(n, ev):
    """The domain's two-state reduction: the hysteretic side, +1 after an upward transition, -1 after a downward one."""
    s = np.full(n, -1.0)
    for i, k in enumerate(ev):
        s[k:] = 1.0 if i % 2 == 0 else -1.0
    return s


def r5():
    dt, sig = 0.01, 0.4; res = {}
    for name, A, per in (("unforced", 0.0, 0.0), ("forced", 0.20, 200.0)):
        xs, ev = _double_well(A, per, dt=dt, sig=sig); e = ev[2:]
        r_i = regularity(xs, e, sigma=sig * math.sqrt(dt), dt=dt, n_boot=500)                # reading (i): unit = the sampling step
        r_ii = regularity(_two_state(len(xs), ev), e, sigma=2.0, dt=dt, n_boot=500)         # reading (ii): unit = the well separation
        r_ii_ex = [float(np.abs(np.diff(_two_state(len(xs), ev)[a:b])).sum()) for a, b in zip(e[:-1], e[1:])]
        mean_dt = float(np.mean(np.diff(e))) * dt
        smooth = {}
        for w in (10, 100, 1000):
            xw = uniform_filter1d(xs, w, mode="nearest")
            smooth[w * dt] = regularity(xw, e, sigma=1.0, dt=dt, n_boot=200)["cv_arc"]
        chords = np.abs(xs[e[1:]] - xs[e[:-1]])
        out_d = dict(n=r_i["n"], cv_arc=r_i["cv_arc"], cv_clock=r_i["cv_clock"], ci=r_i["ci95"], cv_amp=r_i["cv_amp"],
                     per_sample=r_i["C_mean"] / (mean_dt / dt), rate=r_i["C_mean"] * sig * math.sqrt(dt) / mean_dt,
                     rate_dom=sig * math.sqrt(2.0 / (math.pi * dt)), mean_dt=mean_dt, cv_arc_ii=r_ii["cv_arc"], C_ii=r_ii["C_mean"],
                     C_ii_ex=float(np.mean(r_ii_ex)), smooth=smooth, chord=float(np.median(chords)),
                     rho_i=2.0 / (sig * math.sqrt(dt)), rho_ii=1.0)
        if per:
            ph = 2.0 * math.pi * e * dt / per; adv = np.mod(np.diff(ph), 2.0 * math.pi) / math.pi
            out_d["adv_mean"] = float(adv.mean()); out_d["adv_near1"] = float(np.mean(np.abs(adv - 1.0) < 0.25))
            out_d["hist"] = [int(v) for v in np.histogram(np.diff(e) * dt / (per / 2.0), bins=[0, 0.5, 1.5, 2.5, 100.0])[0]]
            out_d["peak_bin"] = ("[0, 0.5)", "[0.5, 1.5)", "[1.5, 2.5)", "beyond 2.5")[int(np.argmax(out_d["hist"]))]
        res[name] = out_d
    u, f = res["unforced"], res["forced"]
    kram = 2.0 * math.pi / (math.sqrt(2.0) * math.exp(-0.25 / (sig ** 2 / 2.0)))              # Kramers' mean residence, barrier 1/4, curvatures 2 and 1
    internal = rel(u["cv_arc"], u["cv_arc_ii"]) > TOL_G
    out = outcome(internal=internal)
    return make_row("g",
        f"The source's Kramers double well (overdamped x' = x - x^3 + noise {sig:g}, dt = {dt:g}, 2e6 steps, hysteretic transitions at +/- 0.5 as the system's own events), unforced and forced (A = 0.2, period 200), with A1''s unit read two ways: (i) the sampling step sigma sqrt(dt) = {sig * math.sqrt(dt):.2f} (the increment's own spread, batch 06 row 5's reading), (ii) the well separation 2 (the domain's two-state reduction: what the bistable element itself resolves)",
        source=f"{SRC_DRV} [3] (DESCR)",
        Q="between transitions the arc is either exactly as regular as the clock (reading (i): the diffusion-carrier theorem, the arc counts samples) or exactly constant (reading (ii): one occasion is one step, the chord), and every unit between the two is a smoothing scale that moves the class; A1' must fix the unit before H-L5 can be asked of a noisy bistable carrier",
        ingredient="A1'/D1 (the unit as the system's own resolvable step, and its two readings on this carrier), D5 (own events = the transitions), H-L5 (the class claim); D2 the arc (not proper)",
        null="the clock: the residence time, whose distribution is Kramers' (exponential, CV near 1) and, under forcing, stochastic resonance's (peaked at half the forcing period)",
        domain="Kramers 1940 (escape rate, mean residence 2 pi e^(Delta U/D)/sqrt(U''(well)|U''(barrier)|)); Levy's total-variation theorem with the law of large numbers over increments (batch 06 row 5); McNamara & Wiesenfeld 1989 and Gammaitoni et al. 1998 (the two-state reduction of stochastic resonance and its residence-time peaks at odd half periods); all named only, not fetched (R10)",
        numbers=(f"unforced, {u['n']} occasions, mean residence {u['mean_dt']:.1f} (Kramers {kram:.1f}): reading (i) CV(C) = {u['cv_arc']:.4f}, CV(clock) = {u['cv_clock']:.4f}, CI of the difference [{u['ci'][0]:.4f}, {u['ci'][1]:.4f}], CV(amplitude) = {u['cv_amp']:.4f}, arc per sample {u['per_sample']:.4f} own units (sqrt(2/pi) = {math.sqrt(2 / math.pi):.4f}), arc per unit time {u['rate']:.3f} in x (Levy {u['rate_dom']:.3f}), rho = {u['rho_i']:.0f}; "
                 f"reading (ii) two-state carrier: arc per occasion {u['C_ii']:.4f} own units inclusive (exclusive {u['C_ii_ex']:.1f}: the jump is the cut and nothing is content), CV(C) = {u['cv_arc_ii']:.4f}, rho = {u['rho_ii']:.0f}; median chord between transitions {u['chord']:.4f} in x; "
                 f"CV(C) on the carrier smoothed at tau = " + ", ".join(f"{tau:g}: {v:.4f}" for tau, v in u["smooth"].items()) + "; "
                 f"forced, {f['n']} occasions, mean residence {f['mean_dt']:.1f}: reading (i) CV(C) = {f['cv_arc']:.4f}, CV(clock) = {f['cv_clock']:.4f}, CI [{f['ci'][0]:.4f}, {f['ci'][1]:.4f}]; reading (ii) CV(C) = {f['cv_arc_ii']:.4f}; forcing-phase advance between consecutive transitions {f['adv_mean']:.4f} half-turns on average, within 0.25 of one half-turn on {100 * f['adv_near1']:.1f} % of transitions; residences in units of the half period, bins [0, 0.5), [0.5, 1.5), [1.5, 2.5), beyond: {f['hist']}"),
        tg=f"CV(C) under reading (i) {u['cv_arc']:.4f} vs under reading (ii) {u['cv_arc_ii']:.4f}: {_agree(u['cv_arc'], u['cv_arc_ii'])} (the ingredient has two values on the domain); under (i) against the clock {u['cv_clock']:.4f}: {_agree(u['cv_arc'], u['cv_clock'])}",
        tn=f"the domain has both values: the law of large numbers gives CV(C) = CV(clock) = {u['cv_clock']:.4f} at the sampling unit (Levy rate {u['rate_dom']:.3f} against {u['rate']:.3f} observed), and the two-state reduction gives one chord per transition, CV(C) = 0",
        tc="not reached: the two readings of A1' must agree before Q can be checked",
        out=out,
        reading=(f"reading (i) alone repeats batch 06 row 5 on a carrier with no drift: the arc per sample is {u['per_sample']:.3f} own units against sqrt(2/pi) = {math.sqrt(2 / math.pi):.3f}, so the arc counts samples and the CV comparison is the clock against itself (the source's tie: arc and clock {_agree(u['cv_arc'], u['cv_clock'])} unforced and {_agree(f['cv_arc'], f['cv_clock'])} forced); reading (ii), which A1''s own sentence points at (the instrument's sample-level noise is not the unit; the bistable element resolves only which well it is in), makes every occasion one step: S = 0, CV(C) = 0, and H-L5 holds by construction on any point process at its own resolution, which is A1''s natural-time clause and not a finding; between them the smoothed carriers give CV(C) from {max(u['smooth'].values()):.4f} down to {min(u['smooth'].values()):.4f} as the smoothing scale grows, a knob; "
                 f"the forcing adds the domain's A3-shaped fact, transitions {f['adv_mean']:.2f} half-turns of the drive apart with residences peaked in the {f['peak_bin']} half-period bin, which is stochastic resonance's residence-time theorem on the drive's phase, not a cut on the system's own"),
        weakness="the two-state carrier is built from the same hysteretic events that define the occasions, so reading (ii) is circular by construction rather than measured; one noise level, one forcing; the smoothing scales are three registered values, not a sweep; the carrier-admissibility clause CLAUDE.md section 7 asks of a PASS-1 (the smoothing scale on a noisy carrier) is this row's INTERNAL stated as a requirement",
        elegance="Between two valleys the ball's trip is always the same trip; only the waiting differs. But count every jiggle as travel and the trip is as random as the wait. Which of the two you call 'the trip' is the whole question, and the ball does not say.",
        child="A ball sits in one of two dips and now and then hops to the other. Every hop is the same short trip, so if you count trips, they are all alike and only the waiting between them is random. But if you count every tiny wobble the ball makes while it waits, the 'distance' it travelled is just how long it waited. You have to decide what counts as moving before you can say which is steadier.")


def main():
    return run_batch("Synthesis batch 14: rows 66-70 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
