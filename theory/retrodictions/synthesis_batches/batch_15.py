"""Synthesis batch 15: rows 71-75 of QUEUE.md (prompt-log entry 61).
driven [4] (DESCR) Paris-law fatigue crack growth under variable-amplitude loading: H-T1's path against the damage functional.
driven [6] (DESCR) AIMD congestion control, buffer-limited and random loss under RTT jitter: the H-L5 class of a congestion epoch.
driven [7] (DESCR) M/M/1 queue busy periods: natural time against clock, and what the two boundary jumps do to the class.
driven [9] (DESCR) Two-parameter harmonic-trap protocol in linear response: does the surplus S order the excess work? (batch 10
row 5 read the same trap on other endpoints; this row restates it on the source's own protocol and says so).
cognitive [2] (DESCR) Rescorla-Wagner learning rate against the steady-state Kalman gain: what the learning-rate reading adds
beyond the two Omega = 1 readings of batches 02 (row 4) and 06 (row 3).

Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). The source models are
re-implemented (nothing imported from theory/retrodictions/*.py). No data file is opened (R2). Deterministic: fixed seeds and
grids, closed forms where the domain has them. Run:  uv run python theory/retrodictions/synthesis_batches/batch_15.py
"""
import math
import sys

import numpy as np
from scipy.signal import lfilter
from scipy.special import gammaln

from crr.instrument.core import arc_length, cv, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

SRC_D = "theory/retrodictions/driven_systems.txt"
SRC_C = "theory/retrodictions/cognitive_collective.txt"


def _agree(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def _holds(flag):
    return "holds" if flag else "fails"


def _r2(y, x):
    """R^2 of y on a linear fit in x (with intercept)."""
    x = np.asarray(x, float); y = np.asarray(y, float); A = np.c_[x, np.ones_like(x)]
    coef, *_ = np.linalg.lstsq(A, y, rcond=None); res = y - A @ coef
    return float(1 - res.var() / y.var())


# ---------------------------------------------------------------- 71 [4] Paris-law fatigue: H-T1's path against the damage functional
def r1():
    """Paris law da/dN = Cp (dK)^m, dK = dsigma Y sqrt(pi a): a separable ODE, so a^(1-m/2) decreases by kappa D with
    D = sum_i dsigma_i^m n_i (the Palmgren-Miner sum). The source's model (seed 4, 200 random 12-block sequences, 2000 cycles
    per block, amplitudes uniform on [60, 140]) is reproduced with the closed form in place of its Euler integrator."""
    rng = np.random.default_rng(4); m = 3.0; Cp = 1e-11; Y = 1.0; a0 = 1e-3; nb = 12; ncyc = 2000; runs = 200
    kappa = Cp * Y ** m * math.pi ** (m / 2) * (m / 2 - 1)
    def crack(seq):
        D = float(np.sum(seq ** m) * ncyc)
        return (a0 ** (1 - m / 2) - kappa * D) ** (1 / (1 - m / 2)), D
    seqs = [rng.uniform(60, 140, nb) for _ in range(runs)]
    af, D, arc1, endp = [], [], [], []
    for s in seqs:
        a_, D_ = crack(s); af.append(a_); D.append(D_); arc1.append(2.0 * float(s.sum()) * ncyc); endp.append(float(s[-1]))
    af, D, arc1, endp = map(np.asarray, (af, D, arc1, endp))
    dmg = a0 ** (1 - m / 2) - af ** (1 - m / 2)                      # the exact damage variable (linear in D)
    lng = np.log(af / a0)
    R_arc, R_miner, R_end = _r2(dmg, arc1), _r2(dmg, D), _r2(dmg, endp)
    Rl_arc, Rl_miner, Rl_end = _r2(lng, np.log(arc1)), _r2(lng, np.log(D)), _r2(lng, np.log(endp))   # the source's regression
    # an equal-arc pair: the same CRR path length, different damage
    sA = np.full(nb, 100.0); sB = np.r_[np.full(nb // 2, 60.0), np.full(nb // 2, 140.0)]
    aA, DA = crack(sA); aB, DB = crack(sB)
    arcA, arcB = 2.0 * float(sA.sum()) * ncyc, 2.0 * float(sB.sum()) * ncyc
    dmgA, dmgB = a0 ** (1 - m / 2) - aA ** (1 - m / 2), a0 ** (1 - m / 2) - aB ** (1 - m / 2)
    # the escape: a metric on the stress line with sqrt(g) = sigma^(m-1) makes the per-cycle arc 2 dsigma^m / m (R = 0 cycles)
    arc_m = np.array([2.0 * float(np.sum(s ** m)) / m * ncyc for s in seqs]); R_arc_m = _r2(dmg, arc_m)
    ratio_m = float(np.std(D / arc_m) / np.mean(D / arc_m))
    # ... and at R = sigma_min/sigma_max > 0 the line integral (sigma_max^m - sigma_min^m)/m is not dsigma^m: the per-cycle unit
    smax, smin = 80.0, 40.0; line_int = (smax ** m - smin ** m) / m; per_cycle = (smax - smin) ** m
    pair_word = "equal" if arcA == arcB else "unequal"
    beats_word = "beats" if R_arc > R_end else "does not beat"
    miner_word = "the Miner sum exactly" if ratio_m < 1e-9 else "not proportional to the Miner sum"
    crr, null = R_arc, R_miner
    check = R_arc >= 0.99
    out = outcome(crr=crr, null=null, domain=R_miner, check=check)
    return make_row("mat", f"Paris-law fatigue crack growth da/dN = Cp (dsigma Y sqrt(pi a))^m, m = {m:g}, Cp = {Cp:g}, a0 = {a0:g} m, under {runs} random {nb}-block load sequences of {ncyc} cycles per block (amplitudes uniform on [60, 140], seed 4; the source's model with its separable ODE solved in closed form)",
                    source=f"{SRC_D} [4] (DESCR)",
                    Q="the damage of a load history is a function of the Fisher path travelled on the stress carrier (D2 with A1': the identity metric at one global scale, so C = sum over cycles of 2 dsigma_i n_i) and not of the endpoint (H-T1 read on a wear system)",
                    ingredient="D6/H-T1 (path against endpoint) with A1' (one unit, fixed once, so the path is the total variation of the stress in that unit)",
                    null="the domain's damage functional: the Palmgren-Miner sum D = sum dsigma_i^m n_i, whose exponent is the material's (a unit that varies with the amplitude, not a global one)",
                    domain="Paris 1963 with Palmgren-Miner: under a separable growth law without load interaction the final crack length is a function of D alone (a^(1-m/2) is linear in D), so R^2 = 1 on the exact damage variable",
                    numbers=f"exact damage variable a0^(1-m/2) - af^(1-m/2): R^2 on the CRR path (exponent 1) = {R_arc:.4f}, on the Miner sum (exponent {m:g}) = {R_miner:.6f}, on the endpoint (last amplitude) = {R_end:.4f}; the source's log-log regression reproduced: {Rl_arc:.3f} (path), {Rl_miner:.3f} (Miner), {Rl_end:.3f} (endpoint); equal-arc pair (twelve blocks at 100 against six at 60 and six at 140): arcs {arcA:.4g} and {arcB:.4g} ({pair_word}), Miner sums ratio {DB / DA:.4f}, damage ratio {dmgB / dmgA:.4f}; a metric with sqrt(g) = sigma^(m-1) on the stress line gives per-cycle arc 2 dsigma^m/m and R^2 = {R_arc_m:.6f} (D / arc CV {ratio_m:.1e}: {miner_word}), but at R = {smin / smax:g} (sigma {smin:g} -> {smax:g}) its line integral (sigma_max^m - sigma_min^m)/m = {line_int:.0f} against the per-cycle dsigma^m = {per_cycle:.0f} (ratio {line_int / per_cycle:.4f})",
                    tg=f"R^2 of the CRR path {R_arc:.4f} vs null (Miner sum) {R_miner:.6f}: {_agree(crr, null)}",
                    tn=f"the domain's functional gives R^2 = {R_miner:.6f} for the same target; the CRR path gives {R_arc:.4f}: {_agree(crr, R_miner, TOL_N)}",
                    tc=f"damage a function of the CRR path alone (R^2 >= 0.99): {_holds(check)} (R^2 = {R_arc:.4f}; two histories of equal arc differ in damage by {100 * (dmgB / dmgA - 1):.1f} %)",
                    out=out,
                    reading=f"path {beats_word} endpoint here ({R_arc:.4f} against {R_end:.4f}), and the domain says why: the crack integrates a separable law, so any history statistic that is not the endpoint carries something; but the statistic it integrates is the Miner sum with the material's exponent, and the Fisher path at one global unit is a different functional (R^2 {R_arc:.4f}, two equal-arc histories {100 * (dmgB / dmgA - 1):.1f} % apart in damage): {out}. The escape is a unit that grows with the amplitude as dsigma^(m-1), which is the Paris law read back as a metric (R^2 {R_arc_m:.6f}) and the domain's, as batch 02 row 2's local relaxation time was the domain's",
                    weakness=f"the stress line is not a statistical manifold, so the identity metric is a stand-in that A1 does not license; the source's model has no mean-stress dependence (R = 0), and the numbers show the metric escape does not survive R > 0 (line integral against per-cycle amplitude, ratio {line_int / per_cycle:.4f} at R = {smin / smax:g}), where the domain itself modifies Paris (Walker, Forman; named only, not fetched, R10); one exponent m = {m:g} and one amplitude range",
                    elegance="Two load histories with the same total travel wear the metal differently: six hard blocks and six soft ones do half again the damage of twelve middling ones. The road length is not the wear; how hard each step lands counts, and it counts as a cube.",
                    child="Bend a paper clip back and forth and it breaks. If you bend it the same total amount but with some big bends and some tiny ones, it breaks sooner than with all medium bends. Counting how far you bent it in total is not enough: the big bends count extra.")


# ---------------------------------------------------------------- 72 [6] AIMD congestion control: the H-L5 class of a congestion epoch
def _aimd_source(rng, random_loss_p, rtt_cv, B=64.0, n_ev=80):
    """The source's estimator path: window trace per round, resampled on a 0.05 grid, events at the loss rounds."""
    w = B / 2; t = 0.0; trace = []; times = []; events = []; wl = []
    while len(events) < n_ev:
        rtt = 1.0 * (1 + rtt_cv * rng.standard_normal()); rtt = max(rtt, 0.2)
        w += 1.0; t += rtt; trace.append(w); times.append(t)
        lost = (w >= B) if random_loss_p == 0 else (rng.random() < 1 - (1 - random_loss_p) ** w)
        if lost:
            events.append(len(trace)); wl.append(w); w = w / 2
    trace = np.array(trace); events = np.array(events); times = np.array(times)
    grid = np.arange(0, times[-1], 0.05); tr_u = np.interp(grid, times, trace); ev_u = np.searchsorted(grid, times[events - 1])
    return tr_u, ev_u, np.array(wl)


def _aimd_rounds(rng, random_loss_p, rtt_cv, B=64.0, n_ev=20000):
    """The same loop in its own units: per epoch the round count N (the window's monotone rise, the halving is the cut and not
    arc), the clock T = the epoch's RTTs summed, the window at the start and at the loss."""
    w = B / 2; n = 0; T = 0.0; w0 = w; N, Tk, ws, wl, rtts = [], [], [], [], []
    while len(N) < n_ev:
        rtt = 1.0 * (1 + rtt_cv * rng.standard_normal()); rtt = max(rtt, 0.2); rtts.append(rtt)
        w += 1.0; T += rtt; n += 1
        lost = (w >= B) if random_loss_p == 0 else (rng.random() < 1 - (1 - random_loss_p) ** w)
        if lost:
            N.append(n); Tk.append(T); ws.append(w0); wl.append(w); w = w / 2; w0 = w; n = 0; T = 0.0
    return np.array(N, float), np.array(Tk), np.array(ws), np.array(wl), np.array(rtts)


def r2():
    rng = np.random.default_rng(6); B = 64.0; rtt_cv = 0.15
    variants = (("buffer-limited", 0.0), ("random loss p = 0.002", 0.002))
    src = {}
    for name, p in variants:                                            # the source's own run order and seed
        tr, ev, wl = _aimd_source(rng, p, rtt_cv)
        r = regularity(tr, ev[3:], sigma=1.0, dt=0.05, n_boot=200, seed=0, segment_end="exclusive")
        arcs = np.array([arc_length(tr[a:b]) for a, b in zip(ev[3:-1], ev[4:])]); w_end = wl[4:]
        # per occasion: the resampled arc = descent from the previous loss (w_prev -> w_prev/2 + 1) plus the rise to this loss
        pred = w_end - 2.0; maxdev = float(np.max(np.abs(arcs - pred)))
        src[name] = (r["cv_arc"], r["cv_clock"], r["cv_amp"], r["n"], maxdev, float(arcs.mean()), float(w_end.mean()))
    ex = {}
    rng2 = np.random.default_rng(6)
    for name, p in variants:
        N, T, ws, wl, rtts = _aimd_rounds(rng2, p, rtt_cv)
        amp = wl - ws
        cvN = cv(N) if N.std() > 0 else 0.0; cvA = cv(amp) if amp.std() > 0 else 0.0
        wald = math.sqrt(cvN ** 2 + cv(rtts) ** 2 / N.mean())            # the compound-sum identity: Var(T) = Var(N) mu^2 + E[N] Var(RTT)
        ex[name] = (cvN, cv(T), cvA, wald, float(N.mean()), cv(rtts), len(N), bool(np.allclose(amp, N)))
    b, rl = ex["buffer-limited"], ex["random loss p = 0.002"]
    crr, null = rl[0], rl[1]                                              # decisive: the random-loss loop, where the source claimed a separation
    domain = math.sqrt(max(rl[1] ** 2 - rl[5] ** 2 / rl[4], 0.0))         # the identity solved for CV(N) from the measured clock and jitter
    margin = 0.01                                                         # the source battery's convention: a CV margin below 0.01 is not a reading
    cls = lambda a, c: f"tie (margin {abs(a - c):.4f} below {margin:g})" if abs(a - c) < margin else ("arc-regular" if a < c else "clock-regular")
    check = (rl[0] < rl[1]) and (rl[0] < rl[2])                           # H-L5 beyond the amplitude control (strict)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    sb, sr = src["buffer-limited"], src["random loss p = 0.002"]
    ctrl_word = "not met on either variant" if (rl[7] and b[7]) else "met on at least one variant"
    return make_row("net", f"AIMD congestion control (window +1 per round trip, halved at a loss; buffer B = {B:g}; RTT jitter CV {rtt_cv:g}): buffer-limited loss and random per-packet loss p = 0.002, the source's model (seed 6) read in its own units (rounds) beside the source's resampled-trace estimator",
                    source=f"{SRC_D} [6] (DESCR)",
                    Q="a congestion epoch is in H-L5's arc-regular class whatever the loss process: the Fisher arc of an epoch (the window's rise between the halving and the next loss; the halving is the cut, A3, and not arc) is more regular than its clock duration, beyond the amplitude control",
                    ingredient="H-L5 (the class claim) with D5/A3 (loss = own event; the halving is the cut, exclusive segmentation), D2 on the window carrier (identity metric)",
                    null="the clock: the epoch's duration, the round-trip times summed",
                    domain="additive increase of one segment per round trip (Chiu-Jain 1989; Jacobson 1988's ack clock): the arc of an epoch is its round count N, and the duration is the compound sum of N round-trip times, Var(T) = Var(N) mu^2 + E[N] Var(RTT), so CV(T)^2 = CV(N)^2 + CV(RTT)^2 / E[N]",
                    numbers=f"in rounds ({rl[6]} epochs per variant): buffer-limited: E[N] = {b[4]:.2f}, CV(N) = {b[0]:.4f}, CV(T) = {b[1]:.4f} (identity {b[3]:.4f}), CV(amplitude) = {b[2]:.4f} (amplitude = N exactly: {b[7]}); random loss: E[N] = {rl[4]:.2f}, CV(N) = {rl[0]:.4f}, CV(T) = {rl[1]:.4f} (identity {rl[3]:.4f}; RTT CV {rl[5]:.4f}), CV(amplitude) = {rl[2]:.4f} (amplitude = N exactly: {rl[7]}); the source's estimator reproduced (resampled trace, {sb[3]} occasions): buffer-limited CV(arc) {sb[0]:.3f}, CV(clock) {sb[1]:.3f}, CV(amp) {sb[2]:.4f}; random loss CV(arc) {sr[0]:.3f}, CV(clock) {sr[1]:.3f}, CV(amp) {sr[2]:.3f}; on that trace each occasion's arc equals the window at its own loss minus 2 to within {sr[4]:.2f} (mean arc {sr[5]:.2f}, mean loss window {sr[6]:.2f}): the interpolated descent from the previous loss is counted inside the next occasion",
                    tg=f"random-loss loop: CV(arc = N) {crr:.4f} vs null CV(clock) {null:.4f}: {_agree(crr, null)}; buffer-limited: {b[0]:.4f} vs {b[1]:.4f}: {_agree(b[0], b[1])} (the buffer fixes N = B/2 = {b[4]:.0f} rounds)",
                    tn=f"the compound-sum identity gives CV(N) = {domain:.4f} from the measured clock and jitter: {_agree(crr, domain, TOL_N)}; buffer-limited: it gives CV(T) = CV(RTT)/sqrt(B/2) = {b[3]:.4f} against {b[1]:.4f} measured",
                    tc=f"random-loss loop: CV(arc) < CV(clock) and CV(arc) < CV(amplitude): {_holds(check)} (class by the numbers: {cls(rl[0], rl[1])}; amplitude control: {'tie' if rl[7] else 'differs'}); buffer-limited: {cls(b[0], b[1])} by construction, amplitude control {'tie' if b[7] else 'differs'}",
                    out=out,
                    reading=f"read in the loop's own units the ingredient does no work on the random-loss loop: the arc of an epoch is its round count, the clock is that count compounded with the RTT jitter, and at the registered jitter the two CVs differ by {100 * abs(rl[1] - rl[0]) / rl[1]:.2f} % ({out}); the source's separation (CV(arc) {sr[0]:.3f} against CV(clock) {sr[1]:.3f}) was the resampled trace counting the descent from the previous loss inside the next occasion (AGENT_LOG 18's segmentation bias reintroduced by interpolation), so its arc was the loss window, not the path; on the buffer-limited loop the arc is B/2 rounds exactly and the regularity is the buffer's, with the amplitude control an exact tie (amplitude = N: {b[7]} buffer-limited, {rl[7]} random loss), so H-L5's 'beyond control (i)' is {ctrl_word}; the domain writes its throughput laws per round already (the ack clock is natural time)",
                    weakness=f"one jitter level (CV {rtt_cv:g}); the identity says the arc-clock gap grows with CV(RTT)^2 / E[N], so a loop with large jitter and short epochs would separate them, still with the amplitude tied to the arc; the window carrier has no statistical metric (identity stand-in)")


# ---------------------------------------------------------------- 73 [7] M/M/1 busy periods: natural time, the arc, and the two boundary jumps
def _borel_tanner_moments(rho, nmax=200000):
    """Customers served in an M/M/1 busy period: P(N = n) = (1/n) C(2n-2, n-1) rho^(n-1) / (1 + rho)^(2n-1)."""
    n = np.arange(1, nmax + 1, dtype=float)
    lp = -np.log(n) + gammaln(2 * n - 1) - 2 * gammaln(n) + (n - 1) * np.log(rho) - (2 * n - 1) * np.log(1 + rho)
    p = np.exp(lp); EN = float((n * p).sum()); VN = float(((n - EN) ** 2 * p).sum())
    return float(p.sum()), EN, VN, float(p[0])


def _mm1_sim(rho, n_bp, seed):
    """Vectorised gambler's ruin from queue length 1 (up with probability rho/(1+rho)); the duration given the step count
    2N - 1 is Gamma(2N - 1, lambda + mu) exactly (memoryless holding times)."""
    rng = np.random.default_rng(seed); lam, mu = rho, 1.0; pu = lam / (lam + mu)
    q = np.ones(n_bp, int); served = np.zeros(n_bp, int); active = np.ones(n_bp, bool)
    while active.any():
        up = rng.random(n_bp) < pu
        q = np.where(active, q + np.where(up, 1, -1), q); served += (active & ~up); active = q > 0
    B = rng.gamma(2 * served - 1, 1.0 / (lam + mu))
    return served.astype(float), B


def r3():
    rhos = (0.25, 0.5, 0.75); rows = {}
    for rho in rhos:
        mass, EN, VN, p1 = _borel_tanner_moments(rho); sd = math.sqrt(VN)
        cvB = math.sqrt((1 + rho) / (1 - rho))                                  # Takacs: E[B] = 1/(mu - lambda), Var(B) = (1 + rho)/(mu^2 (1 - rho)^3)
        readings = {"N (both jumps counted; natural time)": (sd / EN, math.sqrt(rho)),
                    "2N - 1 (one jump counted; the source's arc)": (sd / (EN - 0.5), 2 * math.sqrt(rho) / (1 + rho)),
                    "2N - 2 (no jump counted; A3, the cut has no content)": (sd / (EN - 1.0), 1 / math.sqrt(rho))}
        N, B = _mm1_sim(rho, 200000, 7)
        sim = (cv(N), cv(2 * N - 1), cv(2 * N - 2), cv(B))
        rows[rho] = (mass, EN, VN, p1, cvB, readings, sim)
    sim_dev = max(max(rel(s, e) for s, e in zip(rows[rho][6], [v[0] for v in rows[rho][5].values()] + [rows[rho][4]])) for rho in rhos)
    rho0 = 0.5; mass, EN, VN, p1, cvB, rd, sim = rows[rho0]
    ratios = {k: v[0] / cvB for k, v in rd.items()}
    cls = lambda r: "arc-regular" if r < 1 else ("clock-regular" if r > 1 else "tie")
    classes = {k: cls(r) for k, r in ratios.items()}
    internal = len(set(classes.values())) > 1
    crr = rd["2N - 2 (no jump counted; A3, the cut has no content)"][0]; null = cvB
    out = outcome(crr=crr, null=null, domain=None, check=None, internal=internal)
    def line(rho):
        mass, EN, VN, p1, cvB, rd, sim = rows[rho]
        return (f"rho = {rho:g}: E[N] = {EN:.4f} (1/(1 - rho) = {1 / (1 - rho):.4f}), Var(N) = {VN:.4f} (rho(1 + rho)/(1 - rho)^3 = {rho * (1 + rho) / (1 - rho) ** 3:.4f}), P(N = 1) = {p1:.4f}, CV(B) = {cvB:.4f}; "
                + "; ".join(f"{k}: CV {v[0]:.4f}, ratio to CV(B) {v[0] / cvB:.4f} (closed form {v[1]:.4f}) -> {cls(v[0] / cvB)}" for k, v in rd.items())
                + f"; simulation (200000 busy periods, seed 7): CV(N) {sim[0]:.4f}, CV(2N - 1) {sim[1]:.4f}, CV(2N - 2) {sim[2]:.4f}, CV(B) {sim[3]:.4f}")
    return make_row("queue", "M/M/1 queue (mu = 1, rho = lambda/mu in {0.25, 0.5, 0.75}; the source's rho = 0.5): the busy period as the occasion on the queue-length carrier (identity metric), its own events the arrival to an empty queue and the departure that empties it",
                    source=f"{SRC_D} [7] (DESCR)",
                    Q="the busy period is in H-L5's arc-regular class: the arc of the queue-length path between the cuts is more regular than the busy period's duration, and by the Borel-Tanner moments the ratio of the CVs is a closed form in rho",
                    ingredient="A3/D5 (the cut has no content: the two boundary jumps, 0 -> 1 at the start and 1 -> 0 at the end, are cuts and not arc) with A1' (natural time = customers served) and H-L5 (the class claim); D2 on the count carrier",
                    null="the clock: the busy-period duration B",
                    domain="Borel-Tanner (customers served: E[N] = 1/(1 - rho), Var(N) = rho(1 + rho)/(1 - rho)^3) and Takacs (duration: E[B] = 1/(mu - lambda), Var(B) = (1 + rho)/(mu^2 (1 - rho)^3)); the queue-length path has N - 1 up-steps and N down-steps, so every reading of the arc is an affine function of N",
                    numbers="; ".join(line(rho) for rho in rhos) + f"; Borel-Tanner mass to n = 200000: {mass:.9f}",
                    tg=f"rho = {rho0:g}: reading 2N - 2 CV {crr:.4f} vs null CV(B) {null:.4f}: {_agree(crr, null)}; the three readings' ratios to CV(B): " + ", ".join(f"{r:.4f}" for r in ratios.values()) + " (sqrt rho, 2 sqrt rho/(1 + rho), 1/sqrt rho)",
                    tn="the domain's moments give every reading in closed form (the CV of an affine function of N), so whichever reading is fixed, the domain has its value",
                    tc="not reached: the readings of the ingredient give different classes on the domain (" + "; ".join(f"{k.split(' (')[0]}: {c}" for k, c in classes.items()) + ")",
                    out=out,
                    reading=f"the source's 'natural time and coherence are one statistic' is right up to an affine shift, and the shift decides the class: counting both boundary jumps (natural time N) makes the busy period arc-regular with margin sqrt rho, counting one (the source's 2N - 1) arc-regular with margin 2 sqrt rho/(1 + rho) (below 1 by AM-GM, equal to 1 only at rho = 1), and counting neither, which is what A3's 'the cut has no content' says, makes it clock-regular at every rho (1/sqrt rho); at rho = {rho0:g} a fraction {p1:.4f} of the occasions serve one customer and have zero arc under the A3 reading while their duration is exponential: {out}. On a carrier whose occasions are a few unit steps, which steps are the cut is the class, and the ledger's segmentation rule (a jump at the event is the cut, prompt-log entry 41) puts the busy period in the clock-regular class",
                    weakness=f"the queue-length carrier has no statistical metric (identity stand-in, as the source); the exact moments are the domain's and the simulation only checks them (largest relative deviation {sim_dev:.4f} over the four CVs and three rho); rho -> 1 sends all three ratios to 1 (heavy-tailed busy periods, the random walk's, not CRR's)",
                    elegance="Whether the person who walks up to an empty counter and the person who leaves it empty count as part of the rush or as its edges decides whether the rush is steadier counted in people or in minutes. The rule 'the edge has no content' is a real choice with a real consequence, and a child can see it at any shop counter.",
                    child="Watch a shop counter. A rush starts when someone walks up to an empty counter and ends when the last person leaves. If you count the first and last person as part of the rush, the rushes are steadier counted in people than in minutes. If you count neither (they are the edges, not the rush), most rushes are one person with nothing inside, and then the minutes are steadier. Where you draw the edge changes the answer.")


# ---------------------------------------------------------------- 74 [9] the two-parameter trap on the source's own protocol
def r4():
    """The source's model verbatim: overdamped particle in a harmonic trap, control (x0, k), kT = gamma = 1, Boltzmann family
    N(x0, 1/k) with Fisher metric g = diag(k, 1/(2k^2)) (a hyperbolic half-plane in (x0/sqrt2, sqrt(1/k)), geodesics semicircles),
    friction tensor zeta = diag(gamma, gamma kT/(4k^3)), endpoints (0, 1) -> (2, 4), tau = 50, three protocols. Added: the domain's
    optimum (zeta is flat in (x0, k^-1/2): a straight line there at constant speed) and the Cauchy-Schwarz decomposition of every
    protocol's excess work into L_zeta^2/tau plus tau times the variance of its zeta-speed."""
    kT = 1.0; gamma = 1.0; tol_dec = 1e-9
    def g(lam): return np.diag([lam[1] / kT, 1.0 / (2 * lam[1] ** 2)])
    def zeta(lam): return np.diag([gamma, gamma * kT / (4 * lam[1] ** 3)])
    def length(path, metric):
        return float(sum(math.sqrt((b - a) @ metric((a + b) / 2) @ (b - a)) for a, b in zip(path[:-1], path[1:])))
    def zspeed(path, tau):
        dt = tau / (len(path) - 1)
        return np.array([math.sqrt(((b - a) / dt) @ zeta((a + b) / 2) @ ((b - a) / dt)) for a, b in zip(path[:-1], path[1:])])
    def const_speed(path, metric):
        seg = np.array([math.sqrt((q - p_) @ metric((p_ + q) / 2) @ (q - p_)) for p_, q in zip(path[:-1], path[1:])]); cum = np.r_[0, np.cumsum(seg)]; u = cum / cum[-1]
        tgt = np.linspace(0, 1, len(path)); return np.c_[np.interp(tgt, u, path[:, 0]), np.interp(tgt, u, path[:, 1])]
    to_hp = lambda lam: np.array([lam[0] / math.sqrt(2), math.sqrt(kT / lam[1])]); from_hp = lambda u, sg: np.c_[u * math.sqrt(2), kT / sg ** 2]
    def fisher_geodesic(A, B, n):
        """Closed form: a semicircle centred on sigma = 0 in the half-plane (x0/sqrt2, sqrt(kT/k)), at constant Fisher speed."""
        a, b = to_hp(A), to_hp(B); c = ((b[0] ** 2 + b[1] ** 2) - (a[0] ** 2 + a[1] ** 2)) / (2 * (b[0] - a[0])); R = math.hypot(a[0] - c, a[1])
        th = np.linspace(math.atan2(a[1], a[0] - c), math.atan2(b[1], b[0] - c), n)
        Cstar = math.sqrt(2) * math.acosh(1 + ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) / (2 * a[1] * b[1]))
        return const_speed(from_hp(c + R * np.cos(th), R * np.sin(th)), g), Cstar
    def W_of(path, tau):
        v = zspeed(path, tau); return float((v ** 2).sum() * tau / (len(path) - 1))
    # batch 10 row 5's endpoints recomputed here so the restatement quotes no number from another pinned output
    A10, B10, tau10 = np.array([0.0, 1.0]), np.array([1.0, 4.0]), 1.0
    geo10, _ = fisher_geodesic(A10, B10, 2000); W10 = W_of(geo10, tau10)
    W10_min = gamma * ((B10[0] - A10[0]) ** 2 + (B10[1] ** -0.5 - A10[1] ** -0.5) ** 2) / tau10
    A = np.array([0.0, 1.0]); B = np.array([2.0, 4.0]); n = 2000; tau = 50.0
    geo, Cstar = fisher_geodesic(A, B, n); s = np.linspace(0, 1, n)
    detour = const_speed(np.c_[A[0] + s * (B[0] - A[0]) + 1.2 * np.sin(math.pi * s), A[1] + s * (B[1] - A[1]) - 1.5 * np.sin(math.pi * s)], g)
    warp = np.where(s < 0.3, 0.9 * s / 0.3, 0.9 + 0.1 * (s - 0.3) / 0.7)
    bursty = np.c_[np.interp(warp, s, geo[:, 0]), np.interp(warp, s, geo[:, 1])]
    wA, wB = A[1] ** -0.5, B[1] ** -0.5
    opt = const_speed(np.c_[A[0] + s * (B[0] - A[0]), (wA + s * (wB - wA)) ** -2.0], zeta)
    W_closed = gamma * ((B[0] - A[0]) ** 2 + (wB - wA) ** 2) / tau
    prot = []
    for name, p_ in (("g-geodesic, constant Fisher speed", geo), ("detour, constant Fisher speed", detour), ("g-geodesic, bursty speed", bursty), ("domain optimum: zeta-geodesic, constant zeta speed", opt)):
        v = zspeed(p_, tau); Lz = length(p_, zeta); W = W_of(p_, tau)
        prot.append((name, length(p_, g), length(p_, g) - Cstar, Lz, W, Lz ** 2 / tau, tau * float(v.var())))
    Wg, Wd, Wb, Wo = prot[0][4], prot[1][4], prot[2][4], prot[3][4]
    Sg, Sd, Sb, So = prot[0][2], prot[1][2], prot[2][2], prot[3][2]
    ordered = all((W2 >= W1) for (_, _, S1, _, W1, _, _), (_, _, S2, _, W2, _, _) in zip(sorted(prot, key=lambda r: r[2])[:-1], sorted(prot, key=lambda r: r[2])[1:]))
    decomp_ok = all(abs(W - (Lb + ex)) < tol_dec for _, _, _, _, W, Lb, ex in prot)
    ratio_k = [float(np.diag(zeta(np.array([0.0, k])) @ np.linalg.inv(g(np.array([0.0, k]))))[0] / np.diag(zeta(np.array([0.0, k])) @ np.linalg.inv(g(np.array([0.0, k]))))[1]) for k in (1.0, 2.0, 4.0)]
    crr, null = Wg, Wo
    out = outcome(crr=crr, null=null, domain=W_closed, check=ordered)
    return make_row("thermo", f"Overdamped particle in a harmonic trap, control (x0, k) from ({A[0]:g}, {A[1]:g}) to ({B[0]:g}, {B[1]:g}) in tau = {tau:g} (kT = gamma = 1), linear response W_ex = int lambda-dot^T zeta lambda-dot dt with the exact friction tensor zeta = diag(1, 1/(4k^3)); the source's three protocols reproduced and the domain's optimum added",
                    source=f"{SRC_D} [9] (DESCR)",
                    Q="the surplus S of a protocol (D4 in the Fisher metric at one global scale, A1') orders its excess work among protocols of equal endpoints and duration, and the S = 0 protocol at constant Fisher speed is the minimum (the roadmap's 2-D question)",
                    ingredient="A1' (the metric is Fisher-Rao with its scale fixed once) with D4/P1 (S = 0 selects the geodesic; S as the ordering)",
                    null="the domain's optimum: the geodesic of the friction tensor zeta at constant zeta-speed, a straight line in (x0, k^-1/2) where zeta is flat",
                    domain="Sivak-Crooks 2012: W_ex >= L_zeta^2/tau (Cauchy-Schwarz), equality on the constant-speed zeta-geodesic; for this trap W_min = (dx0^2 + d(k^-1/2)^2)/tau in closed form, and every protocol's excess above L_zeta^2/tau is tau times the time-variance of its zeta-speed",
                    numbers="; ".join(f"{name}: C = {C:.4f}, S = {S:.4f}, L_zeta = {Lz:.4f}, W_ex = {W:.5f} = L_zeta^2/tau {Lb:.5f} + tau Var(zeta-speed) {ex:.5f}" for name, C, S, Lz, W, Lb, ex in prot)
                    + f"; C* = {Cstar:.4f} (closed form); domain minimum in closed form {W_closed:.5f}; zeta g^-1 = diag(1/k, 1/2k), component ratio {ratio_k[0]:.4f}, {ratio_k[1]:.4f}, {ratio_k[2]:.4f} at k = 1, 2, 4 (not a scalar); decomposition W = L_zeta^2/tau + tau Var(v_zeta) within {tol_dec:g} on all four: {decomp_ok}; batch 10 row 5's endpoints ({A10[0]:g}, {A10[1]:g}) -> ({B10[0]:g}, {B10[1]:g}), tau = {tau10:g}, recomputed here: Fisher geodesic W_ex {W10:.5f} against the domain minimum {W10_min:.5f} (gap {100 * (W10 / W10_min - 1):+.2f} %); bursty S = 0 protocol at {Wb / Wg:.2f} x the constant-speed geodesic's W_ex, detour (S = {Sd:.3f}) at {Wd / Wg:.2f} x, domain optimum (S = {So:.3f}) at {Wo / Wg:.2f} x",
                    tg=f"CRR's S = 0 constant-Fisher-speed protocol W_ex {crr:.5f} vs null (domain optimum) {null:.5f}: {_agree(crr, null)} (relative gap {100 * (crr / null - 1):+.2f} %)",
                    tn=f"the domain's closed-form minimum {W_closed:.5f} vs the CRR value {crr:.5f}: {_agree(crr, W_closed, TOL_N)}",
                    tc=f"W_ex non-decreasing in S over the four protocols: {_holds(ordered)} (S = 0 bursty {Wb:.5f} > S = {Sd:.3f} detour {Wd:.5f}: {Wb > Wd}; S = {So:.3f} optimum {Wo:.5f} < S = 0 geodesic {Wg:.5f}: {Wo < Wg})",
                    out=out,
                    reading=f"batch 10 row 5's result restated on the source's own endpoints, and it is the same: with both dials driven the friction is Fisher times diag(1/k, 1/2k), no scalar unit makes the Fisher geodesic the optimum ({100 * (crr / null - 1):+.2f} % here, {100 * (W10 / W10_min - 1):+.2f} % on batch 10's endpoints recomputed), and the domain's optimum carries Fisher surplus {So:.4f} while dissipating least; what this row's own protocols add is the other direction of the same failure, which the source noticed without the domain's decomposition: a zero-surplus protocol at uneven speed dissipates {Wb / Wg:.2f} x the constant-speed one, and the domain's Cauchy-Schwarz gap says exactly how much (tau Var(v_zeta) = {prot[2][6]:.5f}), a quantity of the speed profile that no length, S included, can see: {out}",
                    weakness=f"one system, one pair of endpoints, linear response (the exact finite-time optimum with its end jumps is outside the cited functional); the source's protocols are reproduced from its code, the domain optimum is its closed form checked by the decomposition to {tol_dec:g}",
                    elegance="Even on the best road, rushing and then dawdling costs more than walking evenly, and the extra cost is exactly how unevenly you walked. How far you strayed from the road is a different number and cannot see it.",
                    child="Suppose you carry a full cup across a room. Walking at one steady pace spills the least. If you rush the first part and creep the rest, you spill more even on the very same path. How much more depends only on how uneven your speed was, not on the path.")


# ---------------------------------------------------------------- 75 [2] Rescorla-Wagner as A6 with P3 age weights, against the Kalman gain
def r5():
    """Rescorla-Wagner V <- V + alpha (obs - V) is the exponentially weighted mean of the settled trials with weights
    alpha (1 - alpha)^k: A6's Frechet mean (the fixed-variance Gaussian family is flat, so the Frechet mean is the weighted mean)
    over occasions with P3's geometric age weights q = 1 - alpha at bounded strength (the weights sum to 1). On a random-walk
    reward with Fisher speed v = sqrt(q_rw/r) the MSE-optimal alpha is the steady-state Kalman gain K(v) (P4), so the domain fixes
    the age weight: q = 1 - K(v). Source model (seed 2) with the stream lengthened to T = 1e6 and the alpha grid refined."""
    K = lambda v: (v / 2) * (math.sqrt(v * v + 4) - v); r = 1.0; T = 1_000_000; burn = T // 10
    alphas = np.round(np.arange(0.005, 1.0, 0.005), 3); res = {}
    for v in (0.01, 0.1, 0.3, 1.0):
        rng = np.random.default_rng(2); qrw = v * v
        lam = np.cumsum(math.sqrt(qrw) * rng.standard_normal(T)); obs = lam + math.sqrt(r) * rng.standard_normal(T)
        k = K(v)
        mse = lambda al: float(np.mean((lfilter([al], [1, -(1 - al)], obs) - lam)[burn:] ** 2))
        mse_k = mse(k); closed = ((1 - k) ** 2 * qrw + k ** 2 * r) / (k * (2 - k))
        acc = np.cumsum(obs) / np.arange(1, T + 1); mse_acc = float(np.mean((acc - lam)[burn:] ** 2))
        grid = np.array([mse(al) for al in alphas]); best = float(alphas[int(np.argmin(grid))])
        res[v] = (k, 1 - k, (1 - k) / k, mse_k, closed, k * r, mse_acc, best)
    # the stationary reward (v = 0): the domain's gain is 0, the age weight 1, the mean age infinite (the accumulator A6 forbids)
    rng = np.random.default_rng(2); obs0 = rng.standard_normal(T)
    st = {al: (float(np.mean(lfilter([al], [1, -(1 - al)], obs0)[burn:] ** 2)), al / (2 - al)) for al in (0.05, 0.1, 0.3)}
    acc0 = float(np.mean((np.cumsum(obs0) / np.arange(1, T + 1))[burn:] ** 2))
    v0 = 1.0; k, q_age, age, mse_k, closed, Kr, mse_acc, best = res[v0]
    phi_inv = (math.sqrt(5) - 1) / 2
    crr, null, domain = mse_k, mse_acc, Kr
    check = all(abs(res[v][7] - res[v][0]) <= 0.0025 + 1e-12 for v in res)      # grid-best alpha within half a grid step of K(v)
    out = outcome(crr=crr, null=null, domain=domain, check=check)
    return make_row("cog", f"Rescorla-Wagner learning on a random-walk reward (process variance v^2, observation variance {r:g}, Fisher speed v; T = {T} trials, seed 2, first {burn} dropped), the learner read as A6 regeneration with P3 age weights q = 1 - alpha",
                    source=f"{SRC_C} [2] (DESCR)",
                    Q="the Rescorla-Wagner learner is CRR's regenerator: its associative strength is the Frechet mean of the settled trials under P3's geometric age weights at bounded strength (A6), and the volatility-matched learning rate is the age weight the domain fixes, q = 1 - K(v), with mean age 1/K(v) - 1 trials (1/phi at v = 1)",
                    ingredient="A6 (regeneration from settled occasions by a bounded Frechet mean, never an accumulated count) with P3 (geometric age weights) and D5 (occasion = one trial); P4 is the domain's",
                    null="the accumulated count: the running mean of all observations (the Kalman filter for a stationary reward), which A6 forbids",
                    domain="steady-state Kalman filter of a random walk (Riccati; P4): gain K(v) = (v/2)(sqrt(v^2 + 4) - v), steady-state error variance K(v) r; the fixed-gain filter's error variance ((1 - alpha)^2 v^2 + alpha^2 r)/(alpha (2 - alpha)) is minimised at alpha = K(v) (Dayan-Kakade 2001: Kalman as the normative Rescorla-Wagner)",
                    numbers="; ".join(f"v = {v:g}: K = {k_:.6f}, age weight q = {q_:.6f}, mean age {ag_:.4f} trials; MSE of the regenerator at q = 1 - K: {m_:.6f} (fixed-gain closed form {c_:.6f}; Kalman K r = {kr_:.6f}); accumulated mean MSE {ma_:.1f}; grid-best alpha {b_:.3f}" for v, (k_, q_, ag_, m_, c_, kr_, ma_, b_) in res.items())
                    + f"; 1/phi = {phi_inv:.6f}; stationary reward (v = 0, K = 0, q = 1): regenerator MSE at alpha = 0.05, 0.1, 0.3: " + ", ".join(f"{m_:.4f} (closed form alpha/(2 - alpha) = {c_:.4f})" for m_, c_ in st.values()) + f"; accumulated mean {acc0:.2e}",
                    tg=f"v = {v0:g}: regenerator MSE {crr:.6f} vs null (accumulated mean) {null:.1f}: {_agree(crr, null)}",
                    tn=f"the Kalman steady state gives K r = {domain:.6f}: {_agree(crr, domain, TOL_N)} (the domain has Q: the volatility-matched Rescorla-Wagner learner is the steady-state Kalman filter)",
                    tc=f"grid-best alpha within half a grid step (0.0025) of K(v) at every v: {_holds(check)}",
                    out=out,
                    reading=f"what the learning-rate reading adds to the two Omega = 1 readings (batches 02 and 06, INTERNAL) is a reparametrisation: Rescorla-Wagner is A6 with P3's weights, alpha = 1 - q, so 'bounded strength, never an accumulated count' is the fixed learning rate itself, and the number CRR does not fix (P3: 'CRR does not fix q') is the one the domain fixes from the environment's speed, q = 1 - K(v) ({out}); at v -> 0 the domain's q -> 1 and the mean age {res[0.01][2]:.1f} trials at v = 0.01 grows without bound, so the optimal learner becomes the accumulator A6 forbids, and on a stationary reward the regenerator's floor ({st[0.1][0]:.4f} at alpha = 0.1) sits above the accumulator's {acc0:.2e}: A6 is the domain's optimum exactly when the world moves, which is the source's 'rule 2' point (the observable v is the environment's) seen from the axiom's side; nothing beyond this forms, and the golden ratio at v = 1 is arithmetic on P4",
                    weakness="one-parameter Gaussian learner, so 'Frechet mean' is a weighted average and 'occasion' is a trial (no cut, O3); the Kalman-as-Rescorla-Wagner reading is the domain's (Dayan-Kakade, Kakade-Dayan; named, not fetched, R10), and the age-weight identity is algebra on the update rule; the stationary arm is the batch 03 row 1 finding again (regeneration is not estimation)",
                    elegance="Learn a little from each surprise and let the old lessons fade at the same rate: that is one rule with one knob, and the knob is how fast the world moves. A world that never changes wants a memory that never fades, which the rule cannot give.",
                    child="When you guess how long the school bus will take, you mostly trust the last few days and slowly forget older ones. If the traffic keeps changing, trust the newest days more and forget faster; if nothing ever changes, the best thing is to remember every day forever, and a rule that always forgets can never quite do that.")


def main():
    return run_batch("Synthesis batch 15: rows 71-75 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
