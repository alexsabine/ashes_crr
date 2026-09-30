"""ROB1 stage 4b batch 01: applications RA1 (gait phase and the cut) and RA2 (odometry drift has its own clock) of the
declared battery Robotics/DECLARATION_4B.md (pushed at d44e713 before any model; prompt-log entry 257; AGENT_LOG 223).
Each row fixes, as declared, the model, Q, the CRR-proper ingredient, the null (T-G), the domain's own theorem (T-N), the
check (T-C) and the investigator's forecast; the harness labels are computed from the numbers by outcome() (R15).

RA1. The simplest passive walker (Garcia et al. 1998; the limit of a point-mass hip and massless feet, time in units of
     sqrt(l/g)): stance angle theta'' = sin(theta - gamma), swing angle phi'' = sin(phi)(theta'^2 - cos(theta - gamma))
     + sin(theta - gamma); heel strike where phi - 2 theta crosses 0 upward after mid-stance (theta = 0; the mid-stance scuff
     is ignored, as the model does); reset theta+ = -theta-, theta'+ = cos(2 theta-) theta'-, phi+ = -2 theta-,
     phi'+ = cos(2 theta-)(1 - cos(2 theta-)) theta'-. Slope gamma = 0.009; the period-one gait is found by Newton on the
     stride map; small noise is a Gaussian kick of sd 1e-4 to the stance-leg speed at every heel strike (sd 1e-3, the
     first choice, made the walker fall at step 168; see CHOICES). 20 transient steps are discarded and 200 recorded; the stance angle is sampled 400 times per fixed-point step on a uniform clock grid.
     A3: antipodal_cuts on intrinsic_phase of the recorded stance angle, counting from the second detected extremum (as
     the gate's CUT and A3 tests and study CARD count). Null: peak_cuts of the same angle. Domain: the Poincare section at
     heel strike (offset 0). Scored quantity: the mean over cuts of |cut - nearest heel strike| in mean step periods.
RA2. A differential-drive robot on a straight path at a time-varying speed (levels uniform on [0.1, 2.0] m/s, held for
     exponential dwell times of mean 20 s), wheel base 0.5 m, time step 0.1 s; each wheel's measured increment carries a
     Gaussian slip error of variance k |ds| with k = 1e-4 m (variance grows with distance, the declaration's
     Borenstein-Feng type); 200 robots share the profile and draw independent slip. Drift = the odometer's distance error
     (the mean of the two wheels' errors). Occasions: 1000 clock windows of 10 s. Per window, the drift variance (across
     robots) per arc (the true path's arc_length in the window) and per clock (the window's 10 s); Q: CV per arc < CV per
     clock. Domain: the error model's law, variance = (k/2) x distance, applied to the same windows. T-C: the ratio of the
     CVs against the law's prediction (sampling theory of a Gaussian variance estimate), within two bootstrap standard
     errors. A clock-driven drift (variance proportional to time) is printed as a control, not scored.

CHOICES (every underspecified point, the most literal and simplest reading; also printed in each row's weakness line):
see CHOICES_RA1 and CHOICES_RA2 below. Nothing was tuned after a run.

Literature named by name only, as the declaration names it (no citation claim beyond the names): Garcia, Chatterjee,
Ruina and Coleman 1998 (the simplest walking model); Borenstein and Feng (odometry error). Deterministic: fixed seeds,
DOP853 at fixed tolerances, no data files, no network; about half a minute on a CPU. Rung R4 at most (a declared check on
a synthetic model); a note, not evidence (R8).

    cd /home/user/ashes_crr && uv run python Robotics/batches/rob_01.py > Robotics/batches/rob_01.txt
"""
from __future__ import annotations

import math
import sys

import numpy as np
from scipy.integrate import solve_ivp

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch

DECL = "Robotics/DECLARATION_4B.md at d44e713"


def _w(cond, yes, no):
    return yes if cond else no


def _qv(check):
    return "-> not computable" if check is None else ("-> Q holds" if check else "-> Q fails")


# ====================================================================================== RA1 the simplest walker
GAMMA = 0.009                 # slope (rad), shallow
SIG_KICK = 1e-4               # sd of the Gaussian kick to the stance-leg speed at each heel strike (|theta'*| is about 0.2)
N_TRANS, N_REC = 20, 200      # steps discarded, steps recorded
PER_STEP = 400                # clock samples per fixed-point step period
SEED_WALK = 0
PROM_FRAC, DIST_FRAC = 0.3, 0.4   # peak_cuts: prominence = 0.3 x range, distance = 0.4 x period (the gate's CUT values)
TOL_TC1 = 0.05                # T-C: offset within 5 % of the step period (declared)
LEG_M = 1.0                   # leg length for the robotics reading only (time unit sqrt(l/g))
OPT = dict(method="DOP853", rtol=1e-11, atol=1e-12, dense_output=True)
CHOICES_RA1 = (
    "CHOICES: (1) gamma = 0.009 and the period-one gait found by Newton on the stride map (the declaration fixes a shallow slope, "
    "no value); (2) 'small noise' = a Gaussian kick of sd 1e-4 to the stance-leg speed at each heel strike, applied before the reset "
    "map so the post-impact state stays on it (CHANGE AFTER THE FIRST RUN: sd 1e-3 made the walker fall at step 168 of 220, before any "
    "cut was computed; the model's basin is small, so the noise was cut tenfold, and nothing else was changed); "
    "the walk starts on the Newton fixed point, 20 steps discarded, 200 recorded, seed 0; "
    "(3) the stance angle is Garcia's theta (always the current stance leg), sampled 400 times per fixed-point step; (4) the "
    "antipodal count starts at the second detected extremum, as the gate's CUT and A3 tests and study CARD start it; the anchor itself "
    "is not scored; (5) 'the mean cut-to-heel-strike offset' is read per cut: each antipodal cut's distance to the nearest heel "
    "strike, averaged over all cuts, in mean step periods; the reverse reading (each heel strike's distance to the nearest cut) is "
    "printed, not scored; (6) the null is peak_cuts (maxima and minima) with the gate's CUT parameters, scored the same way; "
    "(7) T-N passes the declared offset 0 of the Poincare section to outcome(): under the harness's relative tolerance only an "
    "offset below its 1e-12 floor could agree; (8) the robotics reading uses a 1 m leg; (9) printed, not scored: the anchor sweep "
    "(the count started at eighths of the first recorded step), one physical leg's angle as the carrier (theta while it stands, "
    "theta - phi while it swings), 200 and 800 samples per step, and the noise-free walk")


def _rhs(t, y):
    th, thd, ph, phd = y
    s = math.sin(th - GAMMA)
    return [thd, s, phd, math.sin(ph) * (thd * thd - math.cos(th - GAMMA)) + s]


def _ev_mid(t, y):             # mid-stance: the stance leg passes the slope normal (theta = 0, downward)
    return y[0]


_ev_mid.terminal = True
_ev_mid.direction = -1


def _ev_hs(t, y):              # heel strike: phi - 2 theta crosses 0 upward (after mid-stance)
    return y[2] - 2.0 * y[0]


_ev_hs.terminal = True
_ev_hs.direction = 1


def _step(y0):
    """One step from a post-impact state: (t_mid, t_heelstrike, dense solution before and after mid-stance, pre-impact state)."""
    s1 = solve_ivp(_rhs, (0.0, 20.0), y0, events=_ev_mid, **OPT)
    if s1.status != 1:
        return None
    t1, y1 = float(s1.t_events[0][0]), s1.y_events[0][0]
    s2 = solve_ivp(_rhs, (t1, t1 + 20.0), y1, events=_ev_hs, **OPT)
    if s2.status != 1:
        return None
    return t1, float(s2.t_events[0][0]), s1.sol, s2.sol, s2.y_events[0][0]


def _impact(ym):
    th, thd = ym[0], ym[1]
    c = math.cos(2.0 * th)
    return np.array([-th, c * thd, -2.0 * th, c * (1.0 - c) * thd])


def _post(th, thd):
    return np.array([th, thd, 2.0 * th, (1.0 - math.cos(2.0 * th)) * thd])


def _stride(z):
    r = _step(_post(z[0], z[1]))
    y = _impact(r[4])
    return np.array([y[0], y[1]]), r[1]


def _fixed_point():
    z = np.array([0.2, -0.2])
    for _ in range(30):
        f, _ = _stride(z)
        res = f - z
        if np.max(np.abs(res)) < 1e-13:
            break
        J = np.empty((2, 2))
        for j in range(2):
            h = np.zeros(2); h[j] = 1e-7
            J[:, j] = (_stride(z + h)[0] - _stride(z - h)[0]) / 2e-7
        z = z - np.linalg.solve(J - np.eye(2), res)
    f, tau = _stride(z)
    J = np.empty((2, 2))
    for j in range(2):
        h = np.zeros(2); h[j] = 1e-7
        J[:, j] = (_stride(z + h)[0] - _stride(z - h)[0]) / 2e-7
    return z, tau, float(np.max(np.abs(f - z))), np.linalg.eigvals(J)


def _walk(z, sig, seed):
    rng = np.random.default_rng(seed)
    y = _post(z[0], z[1])
    steps = []
    for k in range(N_TRANS + N_REC):
        r = _step(y)
        if r is None:
            return None, k
        if k >= N_TRANS:
            steps.append(r)
        ym = np.array(r[4], float)
        ym[1] += sig * rng.standard_normal()
        y = _impact(ym)
    return steps, None


def _sample(steps, dt):
    """Uniform clock grid over the recorded steps: stance angle theta, leg-A angle (theta while leg A stands, theta - phi while it
    swings), heel-strike times T_0 = 0 .. T_N (T_0 opens the first recorded step, T_N closes the last)."""
    T = np.concatenate([[0.0], np.cumsum([s[1] for s in steps])])
    n = int(math.ceil(T[-1] / dt))
    t = np.arange(n) * dt
    t = t[t < T[-1]]
    th = np.empty(len(t)); leg = np.empty(len(t))
    j = np.searchsorted(T, t, side="right") - 1
    for k, (t1, t2, sol1, sol2, _) in enumerate(steps):
        m = np.where(j == k)[0]
        if len(m) == 0:
            continue
        tl = t[m] - T[k]
        Y = np.where(tl <= t1, sol1(np.minimum(tl, t1)), sol2(np.maximum(tl, t1)))
        th[m] = Y[0]
        leg[m] = Y[0] if k % 2 == 0 else Y[0] - Y[2]
    return t, th, leg, T


def _offsets(tc, T, tau_bar):
    j = np.clip(np.searchsorted(T, tc), 1, len(T) - 1)
    return np.minimum(np.abs(tc - T[j - 1]), np.abs(T[j] - tc)) / tau_bar


def _cuts(x):
    ph = intrinsic_phase(x)
    period = 2 * np.pi / max(float(np.median(np.diff(ph))), 1e-9)
    pk = peak_cuts(x, prominence=PROM_FRAC * float(np.ptp(x)), distance=max(int(DIST_FRAC * period), 2))
    return ph, pk, antipodal_cuts(ph, start=int(pk[1]))


def _read(x, t, T, tau_bar, anchor=None):
    """Offsets of the antipodal cuts (counted from the second detected extremum unless an anchor sample is given; the anchor is
    not scored) and of the extremum cuts: per cut, the distance to the nearest heel strike; per heel strike (the heel strikes
    after the anchor and before the last cut), the distance to the nearest cut; all in mean step periods."""
    ph, pk, a = _cuts(x)
    if anchor is not None:
        a = antipodal_cuts(ph, start=int(anchor))
    ca = a[1:]
    off_a = _offsets(t[ca], T, tau_bar)
    off_p = _offsets(t[pk], T, tau_bar)
    hs = T[(T > t[a[0]]) & (T < t[ca[-1]])]
    hs_to_cut = np.array([np.min(np.abs(t[ca] - h)) for h in hs]) / tau_bar
    hs_to_pk = np.array([np.min(np.abs(t[pk] - h)) for h in hs]) / tau_bar
    return dict(ph=ph, pk=pk, a=a, ca=ca, off_a=off_a, off_p=off_p, hs_to_cut=hs_to_cut, hs_to_pk=hs_to_pk)


def _where(tc, T, taus):
    """Fraction of its step elapsed at each time tc."""
    j = np.clip(np.searchsorted(T, tc, side="right") - 1, 0, len(taus) - 1)
    return (tc - T[j]) / taus[j]


ANCHORS = tuple(k / 8 for k in range(8))   # anchor sensitivity: the count started at these fractions of the first recorded step


def ra1():
    z, tau_star, fp_res, mult = _fixed_point()
    steps, fell = _walk(z, SIG_KICK, SEED_WALK)
    if steps is None:
        raise RuntimeError(f"the walker fell at step {fell}")
    dt = tau_star / PER_STEP
    t, th, leg, T = _sample(steps, dt)
    taus = np.diff(T); tau_bar = float(taus.mean())
    r = _read(th, t, T, tau_bar)
    crr, null, dom = float(r["off_a"].mean()), float(r["off_p"].mean()), 0.0
    check = crr <= TOL_TC1
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    per_step = len(r["ca"]) / N_REC
    turns = float((r["ph"][-1] - r["ph"][0]) / (2 * np.pi * (t[-1] - t[0]) / tau_bar))
    # where the cuts land: the half-turn cuts (odd count from the anchor) and the full-turn cuts (even count)
    half, full = r["off_a"][0::2], r["off_a"][1::2]
    frac_half = _where(t[r["ca"][0::2]], T, taus)
    th_half = th[r["ca"][0::2]]
    frac_mid = float(np.mean([s[0] / s[1] for s in steps]))          # mid-stance (theta = 0) as a fraction of its step
    ph_hs = np.array([np.interp(h, t, r["ph"]) for h in T[1:-1]]) % (2 * np.pi)
    # second reading (not scored): each heel strike's distance to the nearest cut
    rev, rev_pk = float(r["hs_to_cut"].mean()), float(r["hs_to_pk"].mean())
    out_rev = outcome(crr=rev, null=rev_pk, domain=0.0, check=rev <= TOL_TC1)
    # anchor sensitivity (not scored): the count started at fractions f of the first recorded step after its heel strike
    anch = {}
    for f in ANCHORS:
        i0 = int(np.argmin(np.abs(t - (T[1] + f * taus[1]))))
        ra = _read(th, t, T, tau_bar, anchor=i0)
        anch[f] = (float(ra["off_a"].mean()), float(ra["hs_to_cut"].mean()))
    per_cut_min = min(v[0] for v in anch.values())
    rev_hold = [f for f in ANCHORS if anch[f][1] <= TOL_TC1]
    # the carrier read as one physical leg's angle (period two steps; not scored)
    rl = _read(leg, t, T, tau_bar)
    crr_l, null_l = float(rl["off_a"].mean()), float(rl["off_p"].mean())
    out_leg = outcome(crr=crr_l, null=null_l, domain=0.0, check=crr_l <= TOL_TC1)
    per_step_l = len(rl["ca"]) / N_REC
    # sampling sensitivity (not scored): the same walk at 200 and 800 samples per step
    samp = {}
    for ps in (200, 800):
        t2, th2, _, _ = _sample(steps, tau_star / ps)
        samp[ps] = float(_read(th2, t2, T, tau_bar)["off_a"].mean())
    # noise-free walk on the limit cycle (not scored)
    steps0, _ = _walk(z, 0.0, SEED_WALK)
    t0, th0, _, T0 = _sample(steps0, dt)
    nf = float(_read(th0, t0, T0, float(np.diff(T0).mean()))["off_a"].mean())
    sens_flip = [k for k, v in (("200 samples per step", samp[200]), ("800 samples per step", samp[800]), ("noise-free", nf))
                 if (v <= TOL_TC1) != check]
    unit_s = math.sqrt(LEG_M / 9.81)
    anch_txt = "; ".join(f"f = {f:g}: per cut {anch[f][0]:.6f}, per heel strike {anch[f][1]:.6f}" for f in ANCHORS)
    return make_row(
        "robotics", f"RA1 gait phase and the cut: the simplest passive walker (Garcia et al. 1998) on a slope gamma = {GAMMA:g}, "
                    f"{N_REC} steps on its limit cycle with a speed kick of sd {SIG_KICK:g} at each heel strike",
        source=f"ROB1 RA1 (declared in {DECL}; forecast REDUNDANT-DOMAIN or WRONG)",
        Q="A3's antipodal cut on the Hilbert phase of the stance angle lands at heel strike: the mean cut-to-heel-strike offset is "
          "small against the step period (computed as: the mean over antipodal cuts of |cut - nearest heel strike| / mean step period)",
        ingredient="A3 (antipodal_cuts on intrinsic_phase of the stance angle theta, counted from the second detected extremum)",
        null="extremum cuts (peak_cuts, maxima and minima) of the same angle, scored the same way",
        domain="the Poincare section at heel strike, the hybrid model's own reset event (offset 0)",
        numbers=(f"fixed point theta* = {z[0]:.8f}, theta'* = {z[1]:.8f} (stride-map residual {fp_res:.1e}), step period "
                 f"{tau_star:.6f}, stride-map multipliers {', '.join(f'{m:.4f}' for m in mult)} (moduli "
                 f"{', '.join(f'{abs(m):.4f}' for m in mult)}); recorded steps {N_REC}, mean step {tau_bar:.6f} "
                 f"(CV {cv(taus):.2e}), {len(t)} samples (dt {dt:.6f}); the Hilbert phase of theta turns {turns:.4f} times per step; "
                 f"{len(r['ca'])} antipodal cuts ({per_step:.3f} per step), {len(r['pk'])} extremum cuts; mean offset per cut: antipodal "
                 f"{crr:.6f} step periods, extremum {null:.6f}; half-turn cuts (odd count from the anchor) {half.mean():.6f}, full-turn "
                 f"cuts (even count) {full.mean():.6f}; the half-turn cuts sit at {frac_half.mean():.4f} of their step (sd "
                 f"{frac_half.std(ddof=1):.4f}), where theta = {th_half.mean():.5f} rad (mid-stance, theta = 0, is at "
                 f"{frac_mid:.4f} of the step); Hilbert phase at the heel strikes, mod 2 pi: mean {ph_hs.mean():.4f} rad (3 pi/2 = "
                 f"{1.5 * math.pi:.4f}), sd {ph_hs.std(ddof=1):.4f}; reverse reading (each heel strike to its nearest cut, not scored): "
                 f"antipodal {rev:.6f}, extremum {rev_pk:.6f}; anchor sensitivity (not scored; the count started at fraction f of a "
                 f"step after a heel strike): {anch_txt}; one leg's angle (not scored): {len(rl['ca'])} antipodal cuts "
                 f"({per_step_l:.3f} per step), per-cut offset antipodal {crr_l:.6f}, extremum {null_l:.6f}; sampling and noise "
                 f"(not scored): 200 and 800 samples per step {samp[200]:.6f} and {samp[800]:.6f}, noise-free walk {nf:.6f}; "
                 f"robotics reading (cutting error, 1 m leg, time unit {unit_s:.4f} s): antipodal {crr * tau_bar * unit_s:.4f} s per "
                 f"cut on a {tau_bar * unit_s:.4f} s step, extremum {null * tau_bar * unit_s:.4f} s"),
        tg=f"antipodal offset {crr:.6f} vs null extremum offset {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')}",
        tn=f"the Poincare section's offset 0: {_w(rel(crr, dom) <= TOL_N, 'agree', 'differ')} (relative difference {rel(crr, dom):.3f})",
        tc=f"mean offset {crr:.6f} <= {TOL_TC1:g} of the step period: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"the stance angle theta always belongs to the current stance leg, so it ramps from +{z[0]:.4f} to -{z[0]:.4f} rad and "
                 f"is reset at every heel strike: its Hilbert phase turns {turns:.4f} times per step and puts the heel strikes at "
                 f"{ph_hs.mean():.4f} rad (sd {ph_hs.std(ddof=1):.4f}); A3 cuts every half turn, {per_step:.3f} times per step: "
                 f"counted from an extremum, the full-turn cuts are {full.mean():.6f} step periods from a heel strike and the half-turn "
                 f"cuts, the antipodes, sit at {frac_half.mean():.4f} of the step ({half.mean():.6f} from a heel strike; theta = 0 at "
                 f"{frac_mid:.4f}); per cut the offset is {crr:.6f}, so Q {_w(check, 'holds', 'fails')} and the row reads {out}; no "
                 f"start of the count brings the per-cut offset to {TOL_TC1:g} (smallest over {len(ANCHORS)} starts: {per_cut_min:.6f}): "
                 f"the two families of cuts are antipodes and at most one can sit on the heel strike; the extremum cuts are "
                 f"{null:.6f} from a heel strike ({_w(null <= TOL_TC1, 'the reset puts the extrema there', 'not at the reset')}); the "
                 f"reverse reading (each heel strike to its nearest cut, {rev:.6f}) is not scored and would read {out_rev}; it holds "
                 f"for {len(rev_hold)} of {len(ANCHORS)} starts of the count (f = {', '.join(f'{f:g}' for f in rev_hold) or 'none'}), "
                 f"so where the heel strike is hit is set by where counting starts, not by A3; read on one leg's angle (period two "
                 f"steps; not scored), A3 cuts {per_step_l:.3f} times per step at a per-cut offset of {crr_l:.6f} against the "
                 f"extremum's {null_l:.6f}, which would read {out_leg}; the scored verdict {_w(sens_flip, 'changes under ' + ', '.join(sens_flip), 'does not change')} "
                 f"with the sampling (200, 800 per step) or without noise"),
        weakness=(CHOICES_RA1 + "; the stance angle carries the reset in its waveform, so the heel strike is where its phase is most "
                  "sharply marked, and the antipode of that phase is set by the ramp's shape (the carrier), not by any event of the "
                  "walker's; the anchor sweep uses the first recorded step only"),
        elegance="", child="")


# ====================================================================================== RA2 odometry drift
DT2, WIN, K_WIN, N_ROB = 0.1, 10.0, 1000, 200
K_SLIP = 1e-4                 # m: each wheel's slip variance is K_SLIP x |ds| (m^2)
BASE = 0.5                    # m, wheel base (heading channel, printed only)
V_LO, V_HI, DWELL = 0.1, 2.0, 20.0
SEED_V, SEED_SLIP, SEED_CLK, SEED_BOOT, N_BOOT = 1, 2, 3, 0, 2000
CHOICES_RA2 = (
    "CHOICES: (1) a straight path, so both wheels roll forward the same true distance (the law is the same on a curve while both "
    "wheels roll forward); (2) speed levels uniform on [0.1, 2.0] m/s held for exponential dwell times of mean 20 s, time step 0.1 s, "
    "seed 1; (3) slip: each wheel's measured increment = true + N(0, k |ds|), k = 1e-4 m, 200 robots on the one profile, seed 2; "
    "(4) drift = the odometer's distance error, the mean of the two wheels' errors, whose variance the law makes k/2 per metre (the "
    "heading error is also proportional to distance and is printed; the Cartesian cross-track error grows as distance cubed and is not "
    "the law's quantity); (5) occasions = 1000 clock windows of 10 s (the declaration names no events); per window the drift "
    "variance is the across-robot variance (ddof 1) of the window's drift increment, per arc = divided by the true path's arc_length "
    "in the window, per clock = divided by 10 s; (6) T-N: the law's prediction (k/2) x arc applied to the same windows, and the CV "
    "of measured/predicted variance; (7) T-C: 'matches' = the measured CV ratio within two bootstrap standard errors (2000 "
    "window resamples, seed 0) of the law's prediction, CV_arc = sqrt(2/(N-1)) (a Gaussian variance estimate from N robots) and "
    "CV_clock = sqrt((1 + c_s^2)(1 + 2/(N-1)) - 1), c_s the CV of the window distances; (8) the clock-driven control (variance "
    "proportional to time, the same mean rate; seed 3) is printed, not scored")


def _speed_profile(n, rng):
    v = np.empty(n)
    i = 0
    while i < n:
        L = max(1, int(round(rng.exponential(DWELL) / DT2)))
        v[i:i + L] = rng.uniform(V_LO, V_HI)
        i += L
    return v


def _window_vars(ds, n_per, rng, per_step_var):
    """Across-robot variance of each window's drift increment; per_step_var(ds_block) gives the per-step variance of each wheel."""
    out = np.empty((K_WIN, 2))
    for m in range(K_WIN):
        sd = np.sqrt(per_step_var(ds[m * n_per:(m + 1) * n_per]))
        dL = rng.standard_normal((N_ROB, n_per)) * sd
        dR = rng.standard_normal((N_ROB, n_per)) * sd
        out[m, 0] = ((dL + dR) / 2).sum(axis=1).var(ddof=1)
        out[m, 1] = ((dR - dL) / BASE).sum(axis=1).var(ddof=1)
    return out


def ra2():
    n_per = int(round(WIN / DT2)); n = K_WIN * n_per
    v = _speed_profile(n, np.random.default_rng(SEED_V))
    ds = v * DT2
    x = np.concatenate([[0.0], np.cumsum(ds)])                     # the true path (one dimension along the straight line)
    arcs = np.array([arc_length(x[m * n_per:(m + 1) * n_per + 1]) for m in range(K_WIN)])
    clock = np.full(K_WIN, WIN)
    var = _window_vars(ds, n_per, np.random.default_rng(SEED_SLIP), lambda b: K_SLIP * np.abs(b))
    vs, vh = var[:, 0], var[:, 1]
    r_arc, r_clk = vs / arcs, vs / clock
    crr, null = cv(r_arc), cv(r_clk)
    law = (K_SLIP / 2.0) * arcs
    dom = cv(vs / law)
    c_s = cv(arcs)
    cva_pred = math.sqrt(2.0 / (N_ROB - 1))
    cvc_pred = math.sqrt((1 + c_s ** 2) * (1 + 2.0 / (N_ROB - 1)) - 1)
    ratio, ratio_pred = crr / null, cva_pred / cvc_pred
    rng = np.random.default_rng(SEED_BOOT)
    br, bd = [], []
    for _ in range(N_BOOT):
        idx = rng.integers(0, K_WIN, K_WIN)
        a, c = cv(r_arc[idx]), cv(r_clk[idx])
        br.append(a / c); bd.append(a - c)
    se = float(np.std(br, ddof=1)); lo, hi = np.percentile(bd, [2.5, 97.5])
    check = abs(ratio - ratio_pred) <= 2.0 * se
    q_ineq = bool(crr < null and hi < 0.0)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    # heading channel (printed only)
    h_arc, h_clk = cv(vh / arcs), cv(vh / clock)
    # clock-driven control: per-step variance proportional to dt at the same mean rate (not scored)
    q_rate = (K_SLIP / 2.0) * float(arcs.sum() / clock.sum())       # m^2 per second on the distance channel
    varc = _window_vars(ds, n_per, np.random.default_rng(SEED_CLK), lambda b: np.full(len(b), 2.0 * q_rate * DT2))[:, 0]
    c_arc, c_clk = cv(varc / arcs), cv(varc / clock)
    # robotics reading: drift per km and per hour
    rate = float(vs.sum() / arcs.sum())                             # m^2 per metre, pooled
    per_km, per_km_law = math.sqrt(rate * 1000.0), math.sqrt(K_SLIP / 2.0 * 1000.0)
    per_h = {u: math.sqrt(rate * u * 3600.0) for u in (V_LO, float(v.mean()), V_HI)}
    return make_row(
        "robotics", f"RA2 odometry drift has its own clock: a differential-drive robot on a straight path at a time-varying speed "
                    f"({V_LO:g} to {V_HI:g} m/s), wheel slip of variance k |ds| per wheel (k = {K_SLIP:g} m), {N_ROB} robots, "
                    f"{K_WIN} windows of {WIN:g} s",
        source=f"ROB1 RA2 (declared in {DECL}; forecast REDUNDANT-DOMAIN)",
        Q="drift is more regular per unit distance (arc) than per unit time: CV of drift variance per arc < CV per clock (computed "
          "as: across the clock windows, CV of the window's drift variance divided by its arc, against the same divided by its duration)",
        ingredient="H-L5 (the arc, arc_length of the true path in each occasion, against the clock as the index of change)",
        null="clock time (the window's duration)",
        domain="the error model's own law: variance = (k/2) x distance on the odometer's distance channel, applied to the same windows",
        numbers=(f"window distances: mean {arcs.mean():.4f} m, CV c_s = {c_s:.4f}; mean speed {v.mean():.4f} m/s; drift variance per "
                 f"window: CV per arc {crr:.6f}, CV per clock {null:.6f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) "
                 f"[{lo:.4f}, {hi:.4f}]; CV of measured/law variance {dom:.6f}; law's sampling prediction CV_arc "
                 f"{cva_pred:.6f}, CV_clock {cvc_pred:.6f}; ratio of CVs measured {ratio:.6f}, law {ratio_pred:.6f}, bootstrap "
                 f"se {se:.6f}; heading channel (variance 2k/b^2 x distance, printed only): CV per arc {h_arc:.6f}, per clock "
                 f"{h_clk:.6f}; clock-driven control (variance proportional to time, not scored): CV per arc {c_arc:.6f}, per clock "
                 f"{c_clk:.6f}; robotics reading: distance drift sd per km {per_km:.4f} m (law {per_km_law:.4f} m), per hour "
                 + ", ".join(f"{per_h[u]:.4f} m at {u:.4f} m/s" for u in per_h)),
        tg=f"CV per arc {crr:.6f} vs null CV per clock {null:.6f}: {_w(rel(crr, null) <= TOL_G, 'agree', 'differ')} (Q's inequality "
           f"with the CI below 0: {_w(q_ineq, 'holds', 'fails')})",
        tn=f"the law's normalisation gives CV {dom:.6f}: {_w(rel(crr, dom) <= TOL_N, 'agree (the domain has Q)', 'differ')} "
           f"(relative difference {rel(crr, dom):.1e})",
        tc=f"ratio of CVs {ratio:.6f} against the law's {ratio_pred:.6f}: |difference| {abs(ratio - ratio_pred):.6f} "
           f"<= 2 se {2 * se:.6f}: {_w(check, 'holds', 'fails')} {_qv(check)}",
        out=out,
        reading=(f"the slip model puts the variance on the metre, so the drift variance per window divided by the arc varies only by "
                 f"the sampling of a variance from {N_ROB} robots (CV {crr:.6f} against sqrt(2/(N-1)) = {cva_pred:.6f}), and per clock it "
                 f"carries the window's speed as well (CV {null:.6f}, window distances CV {c_s:.4f}); the arc is the law's own index: the "
                 f"law's prediction differs from the arc by the constant k/2 and a CV is scale-free, so T-N "
                 f"{_w(rel(crr, dom) <= 1e-12, 'agrees to round-off', 'differs')} and the row reads {out}; with a clock-driven drift "
                 f"(not scored) the order {_w(c_clk < c_arc, 'flips', 'does not flip')} (per clock {c_clk:.6f}, per arc {c_arc:.6f}), "
                 f"so which index is the regular one is set by the noise law, which the domain states before CRR does"),
        weakness=(CHOICES_RA2 + "; the model puts the law in (the slip is defined per metre), so the row checks that H-L5 recovers the "
                  "law and nothing more; a real robot's drift has clock-driven parts (gyro bias, thermal drift) that this model leaves out"),
        elegance="", child="")


def main():
    return run_batch("ROB1 stage 4b batch 01: RA1 gait phase and the cut, RA2 odometry drift has its own clock "
                     f"(Robotics/DECLARATION_4B.md; declared at d44e713)", [ra1(), ra2()])


if __name__ == "__main__":
    sys.exit(main())
