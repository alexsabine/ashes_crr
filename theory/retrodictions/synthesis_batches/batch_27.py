"""Synthesis batch 27: the free-energy principle (FEP) and CRR's clock (owner request 2026-09-22, prompt-log entries 77-78).
Five rows on synthetic FEP systems (no data, R2): [1] the relaxation theorem (natural-gradient flow on variational free
energy: arc = integral of the Fisher speed, dF/dt = -speed^2, so the domain has its OWN clock, free energy); [2] the
linear-Gaussian case (a Kalman filter with switching process noise, events = innovation-gated resets); [3] a discrete
active-inference agent with time-varying policy precision, events = policy switches; [4] the two controls in the domain
(predictive-coding relaxations with clock-scheduled and arc-scheduled stimulus switches); [5] precision shifts (attention)
as the events. H-L5's claim in this domain is sharper than 'arc beats clock': arc must beat the domain's own clock, the
free-energy drop, and it can only do so where the Fisher speed varies (changing precision). Literature named by name and
year only, not fetched (R10): Friston 2010 (the FEP), Parr, Pezzulo and Friston 2022 (active inference), Da Costa et al.
2021 (Bayesian mechanics), Crooks 2007 and Kim 2021 (information length), Costa, Santos and Strapasson 2015 (the Fisher-Rao
distance between Gaussians), Rao and Ballard 1999 (predictive coding). Deterministic; under 60 s."""
import math
import sys

import numpy as np

from crr.instrument.core import cv
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _word(cond, yes, no):
    return yes if cond else no


def fr_gauss(m1, s1, m2, s2):
    """Fisher-Rao distance between N(m1, s1^2) and N(m2, s2^2) (Costa, Santos, Strapasson 2015; metric ds^2 = (dm^2 + 2 ds^2)/s^2)."""
    d = (m1 - m2) / math.sqrt(2.0)
    a = math.sqrt(d * d + (s1 + s2) ** 2); b = math.sqrt(d * d + (s1 - s2) ** 2)
    return math.sqrt(2.0) * math.log((a + b) / max(a - b, 1e-300))


def fr_cat(p, q):
    """Fisher-Rao distance on the simplex (Bhattacharyya angle): 2 arccos sum sqrt(p q)."""
    return 2.0 * math.acos(min(1.0, float(np.sum(np.sqrt(p * q)))))


def cvs(arc, chord, clock, dF):
    return dict(arc=cv(np.array(arc)), chord=cv(np.array(chord)), clock=cv(np.array(clock)), dF=cv(np.array(dF)))


# ---------------------------------------------------------------- [1] the relaxation theorem: arc = chord on a complete monotone relaxation
def r1():
    """Gaussian belief N(mu, s^2) (belief variance fixed) descending F(mu) = pi (mu - mu*)^2 / 2 by natural gradient:
    dmu/dt = -s^2 pi (mu - mu*); Fisher speed = s pi |mu - mu*|; dF/dt = -speed^2. The target mu* jumps at random times
    (random jump sizes) and the precision pi switches between epochs (the Fisher speed varies). Between jumps the belief
    relaxes; arc, chord, clock and free-energy drop per interval."""
    rng = np.random.default_rng(27); s = 1.0; dt = 1e-3
    n_int = 60; arcs = []; chords = []; clocks = []; dFs = []; jumps = []
    mu = 0.0
    for k in range(n_int):
        pi = rng.choice([0.5, 2.0, 8.0]); T = rng.uniform(4.0, 12.0); J = rng.normal(0.0, 1.0) + 3.0 * np.sign(rng.normal())
        target = mu + J; n = int(T / dt); mu0 = mu; arc = 0.0; dF = 0.0
        for _ in range(n):
            v = -s * s * pi * (mu - target); speed = abs(v) / s
            arc += speed * dt; dF += speed * speed * dt; mu += v * dt
        arcs.append(arc); chords.append(abs(mu - mu0) / s); clocks.append(T); dFs.append(dF); jumps.append(abs(J) / s)
    c = cvs(arcs, chords, clocks, dFs); c_jump = cv(np.array(jumps))
    crr, null, dom = c["arc"], c["chord"], c_jump                      # domain theorem: a complete relaxation covers the jump: arc = |J|/s
    check = crr < min(c["clock"], c["dF"])
    bound_ok = all(a * a <= T * f * (1 + 1e-9) for a, T, f in zip(arcs, clocks, dFs))
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "natural-gradient relaxation of a Gaussian belief toward a jumping target under switching precision",
        source="H-L5 (arc since the last cut regular) against the FEP's own clock, the free-energy drop; Da Costa et al. 2021, Crooks 2007 (names only)",
        Q="between target jumps, the Fisher arc of the belief is more regular than the clock AND than the free-energy drop, and the domain's theorem for a complete monotone relaxation (arc = the jump's Fisher length |J|/s, precision-free) already gives it",
        ingredient="H-L5: CV(arc between cuts) as the regular quantity; the cut = the target jump (A3, the jump is the cut, not content)",
        null="the chord (information geometry's): CV of the Fisher distance start-to-end of each interval",
        domain="the relaxation theorem: dF/dt = -speed^2 and arc = integral of speed; a complete relaxation has arc = |J|/s exactly, so CV(arc) = CV(|J|) (Cauchy-Schwarz: arc^2 <= clock x dF)",
        numbers=(f"{n_int} intervals, pi in {{0.5, 2, 8}}, T ~ U(4, 12), |J| ~ 3 + N(0,1): CV(arc) {c['arc']:.4f}, CV(chord) {c['chord']:.4f}, CV(clock) {c['clock']:.4f}, "
                 f"CV(dF) {c['dF']:.4f}, CV(|J|/s) {c_jump:.4f}; arc^2 <= clock x dF on every interval: {bound_ok}"),
        tg=f"arc vs chord: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree (the arc IS the chord on a monotone relaxation)', 'differ')}",
        tn=f"arc vs the jump length: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'the domain theorem gives the arc', 'the theorem does not give it')}",
        tc=f"CV(arc) < min(CV(clock), CV(dF)): {check}",
        out=out,
        reading=(f"the arc between jumps equals the jump's own Fisher length because the relaxation is monotone and complete; its regularity is the regularity of the stimulus, "
                 f"precision-free by construction (dF carries the precision, the arc does not); H-L5 {_word(check, 'holds here', 'fails here')} for the domain's own reason, not CRR's"),
        weakness="a Gaussian belief with fixed variance is the simplest FEP node; the precision switches only the speed, never the geometry; the bound arc^2 <= clock x dF is Cauchy-Schwarz, cited as the domain's",
        elegance="Descending a bowl, the path length you travel is the depth of the bowl no matter how fast you fall: the arc forgets the precision and remembers only the jump.",
        child="If you slide down a slide, how far you slide depends on how long the slide is, not on how fast you go. So measuring the slide length tells you about the slide, not about your speed.")


# ---------------------------------------------------------------- [2] the linear-Gaussian FEP: Kalman filter, switching process noise, innovation-gated resets
def r2():
    rng = np.random.default_rng(272); n = 20000; r = 1.0
    x = 0.0; m = 0.0; P = 1.0; gate = 3.0
    q_now = 0.05; q_switch = 0.002
    arcs = []; chords = []; clocks = []; surps = []
    arc = 0.0; surp = 0.0; t0 = 0; m0, P0 = m, P; n_ev = 0
    for t in range(n):
        if rng.random() < q_switch: q_now = 0.05 if q_now == 0.5 else 0.5     # precision of the process switches (the Fisher speed varies)
        x = x + math.sqrt(q_now) * rng.normal(); y = x + math.sqrt(r) * rng.normal()
        Pp = P + 0.05                                                        # the filter assumes q = 0.05 (the world's precision is hidden from it)
        S = Pp + r; nu = y - m
        surp += 0.5 * (nu * nu / S + math.log(2 * math.pi * S))
        if abs(nu) / math.sqrt(S) > gate and t - t0 > 5:                     # event: gated reset (the jump is the cut, A3 exclusive)
            arcs.append(arc); chords.append(fr_gauss(m0, math.sqrt(P0), m, math.sqrt(P))); clocks.append(t - t0); surps.append(surp)
            m = y; P = r; arc = 0.0; surp = 0.0; t0 = t; m0, P0 = m, P; n_ev += 1
            continue
        K = Pp / S; m_new = m + K * nu; P_new = (1 - K) * Pp
        arc += fr_gauss(m, math.sqrt(P), m_new, math.sqrt(P_new)); m, P = m_new, P_new
    c = cvs(arcs, chords, clocks, surps)
    crr, null, dom = c["arc"], c["chord"], c["dF"]
    check = crr < min(c["clock"], c["dF"])
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "Kalman filter (the linear-Gaussian FEP) with hidden switching process noise; events = innovation-gated resets",
        source="H-L5 against the domain's own clock (accumulated surprise, the evidence); Mehra 1970 (innovation gating), Costa et al. 2015 (the Gaussian Fisher-Rao distance), names only",
        Q="between gated resets the Fisher arc of the posterior path is more regular than the number of steps and than the surprise accumulated",
        ingredient="H-L5 with A3: the reset is the cut, excluded from content; arc = sum of Fisher-Rao steps between consecutive posteriors (mean and variance)",
        null="the chord: the Fisher-Rao distance between the posterior at the reset and the posterior at the next reset",
        domain="the domain's own clock: the accumulated negative log predictive density between resets (surprise = the FEP's quantity)",
        numbers=f"{n_ev} resets in {n} steps (gate 3 sigma, process variance switching 0.05 <-> 0.5 at rate {q_switch}): CV(arc) {c['arc']:.4f}, CV(chord) {c['chord']:.4f}, CV(clock) {c['clock']:.4f}, CV(surprise) {c['dF']:.4f}",
        tg=f"arc vs chord: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"arc vs surprise: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'agree', 'differ')}",
        tc=f"CV(arc) < min(CV(clock), CV(surprise)): {check}",
        out=out,
        reading=(f"the most regular quantity between resets is {min(c, key=c.get)} (CV {min(c.values()):.4f}); "
                 f"{_word(rel(crr, dom) <= TOL_N, 'the arc and the surprise are the same clock within tolerance (both accumulate the noise-driven wiggle of the posterior step by step)', _word(check, 'the arc beats both the clock and the surprise', 'the arc does not beat the domain clock'))}; "
                 f"the chord {_word(null < crr, 'is more regular than the arc: what is steady between resets is the displacement, not the travel', 'is less regular than the arc')}"),
        weakness="the filter's model precision is fixed while the world's switches, so the surprise is that of a misspecified model; the gate threshold (3 sigma) and the minimum spacing (5 steps) are named constants with no sweep here",
        elegance="A filter that resets when surprised makes its own boundaries; the question is only which quantity between two surprises keeps a steady size.",
        child="Imagine you flinch every time something startles you. Between two flinches, is the time the same each time, or the amount your mind moved, or how surprised you were? Here we count all three.")


# ---------------------------------------------------------------- [3] discrete active inference with time-varying policy precision; events = policy switches
def _agent(seed, g_lo, g_hi, n=12000, p_switch=0.02, p_hit=0.8):
    rng = np.random.default_rng(seed)
    c = 0; q = np.array([0.5, 0.5]); a_prev = None
    arcs = []; chords = []; clocks = []; Fs = []; n_ev = 0
    arc = 0.0; F = 0.0; t0 = 0; q0 = q.copy()
    for t in range(n):
        if rng.random() < p_switch: c = 1 - c
        gamma = math.exp(math.log(g_lo) + (math.log(g_hi) - math.log(g_lo)) * 0.5 * (1 + math.sin(2 * math.pi * t / 1500.0)))   # policy precision sweeps g_lo..g_hi (the Fisher speed varies)
        G = np.array([-(q[0] * p_hit + q[1] * (1 - p_hit)), -(q[1] * p_hit + q[0] * (1 - p_hit))])   # expected free energy (risk only): minus expected reward
        pa = np.exp(-gamma * G); pa /= pa.sum(); a = int(rng.random() < pa[1])
        o = int(rng.random() < (p_hit if a == c else 1 - p_hit))                                       # 1 = reward
        like = np.array([p_hit if (a == 0) == (o == 1) else 1 - p_hit, p_hit if (a == 1) == (o == 1) else 1 - p_hit])
        q_new = q * like; ev = q_new.sum(); q_new /= ev
        F += -math.log(ev)                                                                             # the domain's clock: surprise accumulated (F = -log evidence for exact inference)
        arc += fr_cat(q, q_new)
        q = np.array([p_switch, 1 - p_switch])[::-1] * 0 + np.array([(1 - p_switch) * q_new[0] + p_switch * q_new[1], (1 - p_switch) * q_new[1] + p_switch * q_new[0]])
        if a_prev is not None and a != a_prev:
            arcs.append(arc); chords.append(fr_cat(q0, q)); clocks.append(t - t0); Fs.append(F); n_ev += 1
            arc = 0.0; F = 0.0; t0 = t; q0 = q.copy()
        a_prev = a
    return cvs(arcs, chords, clocks, Fs), n_ev


def r3():
    n = 12000; p_switch = 0.02
    cc, n_ev = _agent(273, 2.0, 16.0)                                        # registered range
    cs, n_ev_s = _agent(273, 1.0, 8.0)                                       # sensitivity: a noisier policy (more exploratory flips)
    crr, null, dom = cc["arc"], cc["chord"], cc["dF"]
    beats_domain = crr < min(cc["clock"], cc["dF"]); chord_passes = null < min(cc["clock"], cc["dF"])
    check = beats_domain and crr < null                                       # H-L5's content is the TRAVEL: the arc must beat the chord too
    check_s = cs["arc"] < min(cs["clock"], cs["dF"]) and cs["arc"] < cs["chord"]
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "discrete active-inference agent (two contexts, two actions, hit rate 0.8) with policy precision sweeping 2..16; events = policy switches",
        source="H-L5 in the agent's own belief geometry (the simplex's Fisher-Rao angle); Parr, Pezzulo and Friston 2022 (policy precision gamma), names only",
        Q="between policy switches the Fisher arc of the belief over contexts is the steadiest quantity: more regular than the number of trials, than the surprise accumulated, AND than the chord (H-L5's content is the travel, not the displacement)",
        ingredient="H-L5 with the categorical Fisher-Rao arc (2 arccos sum sqrt(q q')); the switch is the cut",
        null="the chord: the Fisher-Rao angle between the belief at one switch and at the next",
        domain="the agent's own clock: accumulated surprise -log p(o_t | o_<t) between switches",
        numbers=(f"{n_ev} policy switches in {n} trials (context switch rate {p_switch}, gamma 2..16): CV(arc) {cc['arc']:.4f}, CV(chord) {cc['chord']:.4f}, CV(clock) {cc['clock']:.4f}, CV(surprise) {cc['dF']:.4f}; "
                 f"sensitivity gamma 1..8 ({n_ev_s} switches): CV(arc) {cs['arc']:.4f}, CV(chord) {cs['chord']:.4f}, CV(clock) {cs['clock']:.4f}, CV(surprise) {cs['dF']:.4f} -> check {check_s}"),
        tg=f"arc vs chord: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"arc vs surprise: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'agree', 'differ')}",
        tc=f"CV(arc) < min(CV(clock), CV(surprise)): {beats_domain}; and CV(arc) < CV(chord): {crr < null} -> {check}",
        out=out,
        reading=(f"the most regular quantity between switches is {min(cc, key=cc.get)} (CV {min(cc.values()):.4f}); "
                 f"{_word(beats_domain, 'the arc beats the trial count and the surprise', 'the arc does not beat the domain clock')}; "
                 f"{_word(chord_passes, 'the chord passes the same test' + _word(null < crr, ' and is MORE regular than the arc: what is steady between decisions is the belief displacement, which is the domain\'s own decision rule (a policy switch is the belief crossing the decision boundary, so the displacement between crossings is set by the boundary); the arc inherits it', ''), 'the chord does not pass the same test: the travel, not the displacement, is what is steady')}; "
                 f"verdict {_word(check == check_s, 'stable', 'FLIPS')} across the two precision ranges"),
        weakness="expected free energy reduced to risk (no ambiguity term); the precision schedule is a fixed sinusoid; a two-state belief has a one-dimensional geometry where the arc and the chord differ only by back-and-forth travel; every CV here is above 1 (heavy-tailed intervals), so 'more regular' orders three irregular quantities",
        elegance="A decision is a cut the agent makes itself; whether its beliefs travel a fixed distance between decisions is a question the agent can be asked without asking it anything.",
        child="Every time the robot changes its mind about which button to press, we ask: did its guess wander the same distance as last time, did the same number of tries pass, or was it equally surprised? Three clocks, one robot.")


# ---------------------------------------------------------------- [4] the two controls in the domain: clock-scheduled vs arc-scheduled stimulus switches on a predictive-coding node
def _pc_run(rng, mode, n_int=60, dt=1e-3):
    """Two-level predictive coding on a scalar (Rao-Ballard / Friston): belief mu under sensory precision pi_s and prior precision
    pi_p about a prior m; gradient descent on F = pi_s (x - mu)^2/2 + pi_p (mu - m)^2/2. The stimulus x is piecewise constant.
    mode 'clock': switch times on a jittered clock (CV 0.05), jump sizes irregular (|J| ~ U(2, 4)).
    mode 'arc':   the stimulus switches when the belief has travelled a target arc since the last switch (target jittered 5 %)."""
    pi_s, pi_p, m = 4.0, 1.0, 0.0; s = 1.0 / math.sqrt(pi_s + pi_p)        # belief Fisher unit: the posterior sd
    mu = 0.0; x = 0.0
    arcs = []; chords = []; clocks = []; dFs = []
    for k in range(n_int):
        J = (2.0 + rng.uniform(0.0, 2.0)) * np.sign(rng.normal()); x = mu + J                  # the stimulus jumps relative to the current belief (stationary geometry); |J| in [2, 4] so every relaxation exceeds the arc target
        mu0 = mu; arc = 0.0; dF = 0.0; t = 0.0
        if mode == "clock":
            T = 6.0 * (1 + 0.05 * rng.normal()); target_arc = None
        else:
            T = None; target_arc = 0.6 * (1 + 0.05 * rng.normal())
        while True:
            g = pi_s * (mu - x) + pi_p * (mu - m); v = -g; speed = abs(v) * s
            arc += speed * dt; dF += g * g * dt; mu += v * dt; t += dt
            if (T is not None and t >= T) or (target_arc is not None and (arc >= target_arc or t > 60.0)):
                break
        arcs.append(arc); chords.append(abs(mu - mu0) * s); clocks.append(t); dFs.append(dF)
    return cvs(arcs, chords, clocks, dFs)


def r4():
    rng = np.random.default_rng(274)
    neg = _pc_run(rng, "clock"); pos = _pc_run(rng, "arc")
    neg_fails = not (neg["arc"] < neg["clock"]); pos_passes = pos["arc"] < min(pos["clock"], pos["dF"])
    crr, null, dom = pos["arc"], pos["chord"], pos["dF"]
    check = neg_fails and pos_passes
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "predictive-coding node with clock-scheduled (negative control) and arc-scheduled (positive control) stimulus switches",
        source="R4 in the domain: the FEP analogues of S-G (clock-regular by construction) and S-G2 (arc-regular by construction); Rao and Ballard 1999, name only",
        Q="the instrument sees H-L5 in this domain: it fails where the stimulus is clocked and passes where the stimulus is paced by belief travel, and the pass is not the chord's",
        ingredient="H-L5 with A3 (the stimulus switch is the cut) on the belief's Fisher arc in its posterior unit",
        null="the chord of each interval",
        domain="the free-energy drop per interval (the domain's clock)",
        numbers=(f"negative (clock-scheduled): CV(arc) {neg['arc']:.4f}, CV(chord) {neg['chord']:.4f}, CV(clock) {neg['clock']:.4f}, CV(dF) {neg['dF']:.4f}; "
                 f"positive (arc-scheduled): CV(arc) {pos['arc']:.4f}, CV(chord) {pos['chord']:.4f}, CV(clock) {pos['clock']:.4f}, CV(dF) {pos['dF']:.4f}"),
        tg=f"positive control, arc vs chord: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree (the pass is the chord as much as the arc)', 'differ')}",
        tn=f"positive control, arc vs dF: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'agree', 'differ')}",
        tc=f"negative control fails {neg_fails} and positive control passes {pos_passes}: {check}",
        out=out,
        reading=(f"the controls behave as constructed: {_word(neg_fails, 'clocked stimuli defeat the arc', 'clocked stimuli do NOT defeat the arc (the instrument passes on a negative control)')}, "
                 f"{_word(pos_passes, 'arc-paced stimuli pass', 'arc-paced stimuli do not pass')}; on monotone relaxations the arc and the chord {_word(rel(crr, null) <= TOL_G, 'coincide, so the positive control is a chord result', 'separate')}"),
        weakness="both controls are constructed; the positive control makes the world pace itself by the belief's arc, which no FEP system is known to do; the row establishes what the instrument can see, not that anything in the domain does it",
        elegance="A test is only as honest as its two controls: one world that must fool the clock and one that must satisfy it, built before any real world is looked at.",
        child="Before checking whether a stopwatch is right, you time something you know is regular and something you know is not. If it gets both right, then you can trust it on the thing you don't know.")


# ---------------------------------------------------------------- [5] precision shifts (attention) as the events
def r5():
    rng = np.random.default_rng(275); n_int = 60; dt = 1e-2
    pi_p, m = 1.0, 0.0; mu = 0.0
    arcs = []; chords = []; clocks = []; dFs = []; speeds = []
    for k in range(n_int):
        pi_s = rng.choice([0.5, 2.0, 8.0]); T = rng.uniform(5.0, 15.0); n = int(T / dt); s = 1.0 / math.sqrt(pi_s + pi_p)
        mu0 = mu; arc = 0.0; dF = 0.0
        for _ in range(n):
            x = 1.0 + rng.normal() / math.sqrt(pi_s)                                   # noisy input at the current sensory precision
            g = pi_s * (mu - x) + pi_p * (mu - m); v = -0.2 * g; speed = abs(v) * s
            arc += speed * dt; dF += g * g * dt; mu += v * dt
        arcs.append(arc); chords.append(abs(mu - mu0) * s); clocks.append(T); dFs.append(dF); speeds.append(arc / T)
    c = cvs(arcs, chords, clocks, dFs); c_speed = cv(np.array(speeds))
    crr, null, dom = c["arc"], c["chord"], c["dF"]
    check = crr < min(c["clock"], c["dF"])
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    return make_row("fep", "predictive-coding node whose sensory precision (attention) switches at random times; events = the precision shifts",
        source="H-L5 with the FEP's own event kind (a change of precision, Friston 2010; Feldman and Friston 2010 'attention as precision', names only)",
        Q="between shifts of attention the Fisher arc of the belief is more regular than the dwell time and than the free-energy dissipated",
        ingredient="H-L5 with A3: the precision shift is the cut",
        null="the chord per dwell",
        domain="the free-energy dissipated per dwell (the domain's clock)",
        numbers=(f"{n_int} dwells, pi_s in {{0.5, 2, 8}}, dwell ~ U(5, 15): CV(arc) {c['arc']:.4f}, CV(chord) {c['chord']:.4f}, CV(clock) {c['clock']:.4f}, CV(dF) {c['dF']:.4f}; "
                 f"CV of the mean Fisher speed per dwell {c_speed:.4f}"),
        tg=f"arc vs chord: rel {rel(crr, null):.2e} -> {_word(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"arc vs dF: rel {rel(crr, dom):.2e} -> {_word(rel(crr, dom) <= TOL_N, 'agree', 'differ')}",
        tc=f"CV(arc) < min(CV(clock), CV(dF)): {check}",
        out=out,
        reading=(f"within a dwell the belief jitters at a speed set by the precision (CV of the mean speed {c_speed:.4f}), so the arc per dwell is dwell time x a precision-dependent speed and inherits both variabilities; "
                 f"{_word(check, 'the arc still beats the clock and dF', 'the arc is LESS regular than the clock: H-L5 fails on attention-shift events, and the reason is printed above')}"),
        weakness="attention shifts are imposed, not chosen by the node; a node that chose its own shifts (an agent) would be row 3's question",
        elegance="Noise-driven travel is time times speed; when the speed changes with the precision, the travel remembers both, and no clock made of it can be steadier than the clock it contains.",
        child="If you wiggle in your seat faster when you are nervous, then how much you wiggled during a lesson depends on how long the lesson was AND how nervous you were. Counting wiggles is a worse clock than the wall clock.")


def main():
    return run_batch("Synthesis batch 27: the free-energy principle and CRR's clock (prompt-log entries 77-78)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
