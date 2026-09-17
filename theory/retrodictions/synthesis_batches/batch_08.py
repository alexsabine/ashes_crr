"""Synthesis batch 08: rows 36-40 of QUEUE.md (prompt-log entry 61).
daniel [g1] (DESCR) Kepler ellipse half-orbit arcs: H-L5's class under a secular perturbation (batch 04 row 3 read the half-orbit cut).
daniel [g2] (CONSIST) tidal disruption fallback t^-5/3: the finite natural extent of the fallback (A1' natural time, P5).
daniel [g4] (DESCR) CMB acoustic peak phase spacing: the A3 cut on the damped acoustic mode against the extrema.
daniel [h2] (CONSIST) 2-D Ising at Tc, gamma = 7/4: the resolution rho across the critical isotherm (A1'/D1, three readings).
daniel [h3] (CONSIST) Landau mean-field pitchfork: the resolvable steps between the two ordered phases on a correlation volume.

Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data file is
opened (R2). Deterministic: fixed grids, fixed-step RK4, seeded bootstrap. 'D8' in the source rows is a clause of an
older text; CRR.md v3.1 has O1 in its place.
Run:  uv run python theory/retrodictions/synthesis_batches/batch_08.py
"""
import math
import sys
from fractions import Fraction

import numpy as np
from scipy.integrate import quad
from scipy.special import ellipe

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, regularity
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


def _running_mean(x, w):
    """Running mean over w samples with reflected padding (the named detrender of rows 1 and 3)."""
    pad = w // 2
    xp = np.pad(x, (pad, w - 1 - pad), mode="reflect")
    return np.convolve(xp, np.ones(w) / w, mode="valid")


def _extrema(x, lo=1):
    i = np.arange(lo, len(x) - 1)
    return i[((x[i] > x[i - 1]) & (x[i] >= x[i + 1])) | ((x[i] < x[i - 1]) & (x[i] <= x[i + 1]))]


# ---------------------------------------------------------------- 36: [g1] Kepler orbit under a secular perturbation
def _kepler_stark(a=1.0, e=0.3, f=1e-3, n_orb=60, steps=2000):
    """Two-body orbit (mu = 1) with a weak uniform perturbing force (0, f): the classical Stark problem, whose
    orbit-averaged dynamics conserve a and rotate the eccentricity vector. Fixed-step RK4, `steps` per unperturbed period."""
    T = 2.0 * math.pi * a ** 1.5
    dt = T / steps
    y = np.array([a * (1.0 - e), 0.0, 0.0, math.sqrt((1.0 + e) / (a * (1.0 - e)))])

    def rhs(s):
        x, yy, vx, vy = s
        r3 = (x * x + yy * yy) ** 1.5
        return np.array([vx, vy, -x / r3, -yy / r3 + f])

    n = n_orb * steps
    out = np.empty((n + 1, 4))
    out[0] = y
    for i in range(n):
        k1 = rhs(y); k2 = rhs(y + 0.5 * dt * k1); k3 = rhs(y + 0.5 * dt * k2); k4 = rhs(y + dt * k3)
        y = y + dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        out[i + 1] = y
    return np.arange(n + 1) * dt, out, dt, steps


def r1():
    f, n_orb = 1e-3, 60
    t, Y, dt, steps = _kepler_stark(f=f, n_orb=n_orb)
    x, y, vx, vy = Y.T
    r = np.hypot(x, y)
    Hfull = 0.5 * (vx ** 2 + vy ** 2) - 1.0 / r - f * y
    a_osc = -0.5 / (0.5 * (vx ** 2 + vy ** 2) - 1.0 / r)
    e_osc = np.sqrt(np.clip(1.0 - (x * vy - y * vx) ** 2 / a_osc, 0.0, None))
    ext_all = _extrema(r)
    ev = ext_all[(ext_all > steps) & (ext_all < len(r) - steps)]          # interior apsides: the system's own events
    pos = np.column_stack([x, y])
    reg = regularity(pos, ev, sigma=1.0, dt=dt, n_boot=2000, seed=0)
    C = np.array([arc_length(pos[i:j + 1]) for i, j in zip(ev[:-1], ev[1:])])
    T = np.array([t[j] - t[i] for i, j in zip(ev[:-1], ev[1:])])
    amp = np.array([2.0 * a_osc[i] * e_osc[i] for i in ev[:-1]])           # apsidal range r_apo - r_peri = 2 a e: control (i)
    Cd = np.array([2.0 * a_osc[i] * ellipe(e_osc[i] ** 2) for i in ev[:-1]])   # the domain's half-perimeter 2 a E(e^2)
    Td = np.array([math.pi * a_osc[i] ** 1.5 for i in ev[:-1]])             # the domain's half-period pi a^(3/2)
    max_rel_arc = float(np.max(np.abs(C - Cd) / Cd))
    max_rel_clock = float(np.max(np.abs(T - Td) / Td))
    # A3 on the intrinsic phase of r(t): raw (mean removed) and with a one-period running-mean detrender
    offs = {}
    adv = {}
    for name, sig in (("raw", r), ("detrended", r - _running_mean(r, steps))):
        ph = intrinsic_phase(sig)
        cuts = antipodal_cuts(ph, start=int(ev[0]))
        cuts = cuts[cuts <= ev[-1] + steps // 4]
        m = min(len(cuts), len(ev))
        offs[name] = int(np.max(np.abs(cuts[:m] - ev[:m])))
        a_ = np.diff(ph[ev]) / math.pi
        adv[name] = (float(a_.mean()), float(a_.min()), float(a_.max()))
    cv_arc, cv_clock, cv_amp = cv(C), cv(T), cv(amp)
    cv_arc_d, cv_clock_d = cv(Cd), cv(Td)
    lo, hi = reg["ci95"]
    check = (cv_clock < cv_arc) and (lo > 0.0) and (max_rel_arc <= TOL_N)
    out = outcome(crr=cv_arc, null=cv_clock, domain=cv_arc_d, check=check)
    return make_row("orb", f"Kepler orbit (mu = 1, a = 1, e0 = 0.3) under a weak uniform perturbing force (0, f), f = {f:g} (the classical Stark problem: orbit-averaged, a is conserved and the eccentricity vector rotates); {n_orb} orbits by fixed-step RK4 at {steps} steps per unperturbed period; own events = the apsides (extrema of r), occasion = one half-orbit; arc = orbit-plane Euclidean length (the stand-in metric of the source row and of batch 04 row 3)",
                    source="runs/phaseA/crr_retrodictions.txt [g1] (DESCR)",
                    Q="under a secular (orbit-averaged) perturbation the half-orbit occasions of a Kepler orbit belong to H-L5's clock-regular class: the apsis-to-apsis clock stays fixed to the order of the perturbation while the apsis-to-apsis arc varies with the eccentricity, because the clock depends on the semi-major axis alone (Kepler's third law) and the semi-major axis is the secular invariant",
                    ingredient="H-L5 (the class claim: arc-regular against clock-regular), D5 (occasion = half-orbit between the system's own events), A3 (antipodal_cuts on the intrinsic phase of r(t), raw and with a one-period running-mean detrender, checked against the apsides)",
                    null="the clock: the apsis-to-apsis interval, the domain's anomalistic half-period",
                    domain="Kepler's third law T = 2 pi a^(3/2) (T independent of e) with the secular conservation of a (Lagrange's planetary equation da/dt = (2/(n a)) dR/dM vanishes for an orbit-averaged disturbing function R), and the half-perimeter of the osculating ellipse 2 a E(e^2)",
                    numbers=f"{len(C)} half-orbit occasions; osculating e at the apsides {e_osc[ev].min():.4f} -> {e_osc[ev].max():.4f}, osculating a in [{a_osc[ev].min():.6f}, {a_osc[ev].max():.6f}]; Hamiltonian drift {Hfull.max() - Hfull.min():.2e}; CV(arc) = {cv_arc:.4f} (arc {C.min():.4f} -> {C.max():.4f}), CV(clock) = {cv_clock:.4f} (clock {T.min():.4f} -> {T.max():.4f}, mean {T.mean():.5f}, pi a^(3/2) = {math.pi:.5f}), CV(apsidal range 2ae, control i) = {cv_amp:.4f}; paired-bootstrap 95 % CI of CV(arc) - CV(clock) = [{lo:.4f}, {hi:.4f}]; domain closed forms from the osculating elements: CV(2 a E(e^2)) = {cv_arc_d:.4f} (max per-occasion relative difference from the measured arc {max_rel_arc:.2e}), CV(pi a^(3/2)) = {cv_clock_d:.2e} (max relative difference from the measured clock {max_rel_clock:.2e}); A3 cuts against the apsides: raw r(t) max offset {offs['raw']} samples (phase advance per half-orbit {adv['raw'][0]:.4f} half-turns, {adv['raw'][1]:.4f} -> {adv['raw'][2]:.4f}), detrended r(t) max offset {offs['detrended']} samples of {steps // 2} per half-orbit (phase advance {adv['detrended'][0]:.5f} half-turns, {adv['detrended'][1]:.4f} -> {adv['detrended'][2]:.4f})",
                    tg=f"CV(arc) {cv_arc:.4f} vs null CV(clock) {cv_clock:.4f}: {ag(cv_arc, cv_clock)}",
                    tn=f"the third law with a conserved and the half-perimeter 2 a E(e^2) give CV(arc) = {cv_arc_d:.4f} and CV(clock) = {cv_clock_d:.2e}: {ag(cv_arc, cv_arc_d, TOL_N)} (the domain has Q)" if rel(cv_arc, cv_arc_d) <= TOL_N else f"the closed forms give CV(arc) = {cv_arc_d:.4f}: {ag(cv_arc, cv_arc_d, TOL_N)}",
                    tc=f"CV(clock) < CV(arc), the CI of the difference above 0, and every occasion's arc within {TOL_N:g} of 2 a E(e^2): {hf(check)}",
                    out=out,
                    reading=f"the class claim gets its answer from two theorems of the domain: the half-orbit clock is a function of a alone, a is the invariant of every orbit-averaged perturbation, and the half-orbit arc is a function of e, the element the perturbation moves; so a Kepler orbit under secular change is clock-regular (CV(clock) {cv_clock:.4f} against CV(arc) {cv_arc:.4f}), the opposite of H-L5's claim; the closed forms from the osculating elements {ag(cv_arc, cv_arc_d, TOL_N)} with the measured CV(arc), and the clock CV they give ({cv_clock_d:.1e}) lies below the measured {cv_clock:.4f}, the O(f) difference between the osculating half-period and the actual apsis-to-apsis interval. The cut lands on the apsides once the drifting baseline of r(t) is removed (max offset {offs['detrended']} samples; raw, {offs['raw']}), so D5's occasions are the domain's half-orbits. The synthesis reading is {out}",
                    weakness=f"the orbit-plane Euclidean length is a stand-in that A1 does not license (the source row's own free choice); one perturbation (a uniform field) at one strength, and a {n_orb}-orbit window that covers a monotone part of the secular cycle; A1'/D1 could not be formed (a deterministic orbit has no statistical family and no residual to measure a unit from), and A6 across orbits was not attempted: on the unperturbed ellipse every occasion is identical and the Frechet mean of identical contents is that content, so A6 and the endpoint coincide by construction (batch 04 row 3 records the disagreement of four phase variables away from the apsides)",
                    elegance="A planet's year depends on the size of its orbit, not on its shape: a rule with no knobs. So when something slowly squashes the orbit, the half-years stay the same while the roads travelled in them change, and the clock, not the road, is the steady one.",
                    child="A planet's year depends only on how big its orbit is, not on how squashed it is. If something slowly squashes the orbit, each half-year still takes the same time, but the road the planet travels in that half-year gets shorter or longer. So here the clock is the steady thing, not the road.")


# ---------------------------------------------------------------- 37: [g2] tidal disruption fallback in natural time
def r2():
    N, t_min = 1000, 1.0
    N_b = N // 2                                                           # flat dM/dE on [-dE, dE]: the bound half
    dE = 1.0
    E_b = -dE * (np.arange(1, N_b + 1) - 0.5) / N_b                       # bound parcel energies, uniform on (-dE, 0)
    t_j = t_min * (dE / np.abs(E_b)) ** 1.5                                # Keplerian return time of each parcel
    c = t_min
    K = (2.0 / 3.0) * N_b * c ** (2.0 / 3.0)                               # the source row's form lambda = K (t + c)^-5/3
    lam = lambda t: K * (t + c) ** (-5.0 / 3.0)
    A_inf = quad(lam, 0.0, np.inf)[0]
    A_inf_closed = 1.5 * K * c ** (-2.0 / 3.0)
    T_h = 1e6 * t_min
    A_T = quad(lam, 0.0, T_h)[0]
    n_ret = int(np.sum(t_j <= T_h + t_min))
    t_last = float(t_j.max())
    frac_left = (1.0 + T_h / c) ** (-2.0 / 3.0)
    t_of_A = lambda A: t_min * (1.0 - A / N_b) ** (-1.5)                  # clock time as a function of natural time (shifted)
    t_at = t_of_A(N_b * (1.0 - 1e-4)) - t_min
    # P5 retention in the source row's normalisation K = c = rho = 1
    K1, c1, rho1 = 1.0, 1.0, 1.0
    A1 = lambda t: 1.5 * K1 * (c1 ** (-2.0 / 3.0) - (t + c1) ** (-2.0 / 3.0))
    R_nat = lambda t: math.exp(-A1(t) / rho1)
    R_nat_inf = math.exp(-1.5 * K1 * c1 ** (-2.0 / 3.0) / rho1)
    R_clock = lambda t: math.exp(-t / (rho1 * c1))
    R_clock_late = R_clock(T_h)
    A1_p1_T = K1 * math.log((T_h + c1) / c1)                               # the p = 1 (Omori) natural extent at the same horizon
    domain_floor = math.exp(-A_inf / N_b * 1.5 / rho1)                     # the bound-mass integral in the same normalisation (A_inf/N_b = 1)
    check = abs(A_inf - N_b) <= 1e-6 * N_b and t_at >= 0.999 * T_h and lam(T_h) > 0.0
    out = outcome(crr=R_nat_inf, null=R_clock_late, domain=domain_floor, check=check)
    return make_row("tde", f"Tidal disruption fallback: N = {N} equal-mass debris parcels with a flat energy distribution on [-dE, dE] (Rees 1988), the bound half returning after Keplerian periods t_j = t_min (dE/|E_j|)^(3/2), t_min = {t_min:g}; in the source row's form the rate is lambda(t) = K (t + c)^(-5/3) with c = t_min and K = (2/3) N_b c^(2/3) = {K:.4f}",
                    source="runs/phaseA/crr_retrodictions.txt [g2] (CONSIST)",
                    Q="in the system's own time (A1': one debris return = one step, natural time A(t) = the expected count) the fallback has a finite extent A(inf) = N_b = N/2, the bound half of the star, while in clock time it never ends: clock time as a function of natural time, t = t_min (1 - A/N_b)^(-3/2), diverges at a finite natural time, so P5's retention exp(-A/rho) floors at exp(-N_b/rho) instead of decaying to zero",
                    ingredient="A1'/D1 (the unit is one event and time is natural time), D5 (occasion = one return), P5 (retention in natural time)",
                    null="the clock: retention in clock time exp(-t/(rho t_min)) and the clock's extent, which has no end",
                    domain="Rees 1988 / Phinney 1989: with a flat dM/dE half the star is bound, its parcels return after their Keplerian periods, Mdot ∝ t^(-5/3), and the integral of the fallback rate is the bound mass M_*/2 (finite)",
                    numbers=f"natural extent A(inf) = {A_inf:.6f} steps by quadrature (closed form 3K/(2 c^(2/3)) = {A_inf_closed:.6f}; N_b = {N_b}); at the clock horizon T = {T_h:.0e} t_min: A(T) = {A_T:.4f}, natural fraction still to come (1 + T/c)^(-2/3) = {frac_left:.1e}, rate lambda(T) = {lam(T_h):.2e} > 0, parcels returned {n_ret} of {N_b} (the last at t = {t_last:.0f} t_min); clock time at natural time N_b (1 - 1e-4): t = {t_at:.0f} t_min; P5 in the source row's normalisation K = c = rho = 1: R(1) = {R_nat(1.0):.4f}, R(inf) = {R_nat_inf:.5f}; clock-time retention at T: {R_clock_late:.1e}; the p = 1 (Omori) natural extent at the same horizon, K ln((T + c)/c) = {A1_p1_T:.2f}, unbounded",
                    tg=f"natural-time retention floor R(inf) {R_nat_inf:.5f} vs null clock-time retention {R_clock_late:.1e}: {ag(R_nat_inf, R_clock_late)}",
                    tn=f"the bound-mass integral gives A(inf) = N_b exactly (ratio {A_inf / N_b:.6f}; in the source's normalisation A(inf) = {1.5 * K1 * c1 ** (-2.0 / 3.0):.4f}) and hence the floor exp(-A(inf)/rho) = {domain_floor:.5f}: {ag(R_nat_inf, domain_floor, TOL_N)} (the domain has Q)" if rel(R_nat_inf, domain_floor) <= TOL_N else f"the bound-mass integral gives the floor {domain_floor:.5f}: {ag(R_nat_inf, domain_floor, TOL_N)}",
                    tc=f"A(inf) within 1e-6 of N_b, the clock diverging at natural time N_b (t at N_b (1 - 1e-4) >= 0.999 T) and lambda(T) > 0: {hf(check)}",
                    out=out,
                    reading=f"natural time does real work (T-G): it turns a process that never ends on the clock into one of finite extent, and the extent it finds is the bound mass, the number the domain's own integral gives; the source row's lim R != 0 is this finiteness seen through P5, and its p = 5/3 against p = 1 distinction is, in natural time, finite against unbounded extent (Omori's compensator at the same horizon: {A1_p1_T:.2f} and growing). The synthesis reading is {out}",
                    weakness="the parcel model is the flat-dM/dE idealisation (the fallback of a real disruption departs from t^-5/3 early and late); rho is not fixed by CRR, so the floor's value is the domain's N_b over a free constant; the deterministic parcel returns make the natural-time intervals one step each by construction, so no H-L5 statement was attempted (batch 04 row 1 has the stochastic reading for an Omori sequence)",
                    elegance="The debris comes home in order of how tightly it was held, so counted in its own order the fallback ends at 'half the star'; counted by the clock it never ends. One picture: a finite queue served ever more slowly.",
                    child="When a star is torn apart by a black hole, half of it is flung away for good and half comes falling back, the tightly held bits first and the loosely held bits later and later. If you count the pieces as they arrive, the story ends when the last piece is home. If you watch the clock instead, it never quite ends, because the stragglers keep arriving more and more slowly.")


# ---------------------------------------------------------------- 38: [g4] CMB acoustic peaks: the phase cut against the extrema
def r3():
    r_s, Kmax, n = 1.0, 10.0 * math.pi, 200001
    k = np.linspace(-Kmax, Kmax, n)
    dk = k[1] - k[0]
    i0 = int(np.argmin(np.abs(k)))
    per = int(round(2.0 * math.pi / r_s / dk))
    env = lambda kd: np.exp(-((k / kd) ** 2))
    probes = [("pure mode", np.cos(k * r_s)),
              ("k_d = 20 with beta = 0.15 second harmonic", env(20.0) * (np.cos(k * r_s) + 0.15 * np.cos(2.0 * k * r_s))),
              ("k_d = 8", env(8.0) * np.cos(k * r_s))]
    offset = ("k_d = 8 with the baryon-loading offset R = 0.3", env(8.0) * (np.cos(k * r_s) - 0.3))
    kmax_read = 8.0 * math.pi

    def a3_spacings(g):
        """Cut positions in k: antipodal_cuts gives the nearest sample; the crossing of the target phase
        phase[i0] + n pi is then located sub-sample by linear interpolation between the neighbouring samples."""
        ph = intrinsic_phase(g)
        cuts = antipodal_cuts(ph, start=i0)
        kc = [k[i0]]
        for j, c in enumerate(cuts[1:], 1):
            target = ph[i0] + j * math.pi
            lo, hi = max(c - 1, 0), min(c + 1, n - 1)
            kc.append(float(np.interp(target, ph[lo:hi + 1], k[lo:hi + 1])))
        kc = np.asarray(kc)
        kc = kc[kc < kmax_read]
        return kc, np.diff(kc) / (math.pi / r_s)

    def ext_spacings(g):
        e = _extrema(g, lo=i0 + 1)
        p, q, rr = g[e - 1], g[e], g[e + 1]
        ke = (e + 0.5 * (p - rr) / (p - 2.0 * q + rr)) * dk + k[0]
        ke = ke[(ke > 0.5) & (ke < kmax_read)]
        return ke, np.diff(ke) / (math.pi / r_s)

    res = []
    for name, g in probes:
        kc, sa = a3_spacings(g); ke, se = ext_spacings(g)
        res.append((name, len(kc), float(sa.mean()), float(np.abs(sa - 1.0).max()), len(ke), float(se.mean()), float(np.abs(se - 1.0).max()), kc, ke))
    name_o, g_o = offset
    kc_o, sa_o = a3_spacings(g_o); ke_o, se_o = ext_spacings(g_o)
    kc_o2, sa_o2 = a3_spacings(g_o - _running_mean(g_o, per))
    _, sa_3rm = a3_spacings(probes[2][1] - _running_mean(probes[2][1], per))
    dec = res[2]                                                          # the decisive probe: the source row's honesty probe k_d = 8
    a3_mean, a3_max, ex_mean, ex_max = dec[2], dec[3], dec[5], dec[6]
    _, se_dec = ext_spacings(probes[2][1])
    ex_spread = float(se_dec.max() - se_dec.min())
    domain_spacing = 1.0
    check = all(rr[3] <= 0.005 for rr in res)
    out = outcome(crr=a3_mean, null=ex_mean, domain=domain_spacing, check=check)
    per_probe = "; ".join(f"{rr[0]}: A3 cuts at k r_s/pi = {np.array2string(rr[7] / math.pi, precision=4, separator=', ', max_line_width=1000)} ({rr[1]} cuts, spacing mean {rr[2]:.5f}, max |spacing - 1| {rr[3]:.1e}), extrema at {np.array2string(rr[8] / math.pi, precision=4, separator=', ', max_line_width=1000)} (spacing mean {rr[5]:.5f}, max |spacing - 1| {rr[6]:.1e})" for rr in res)
    return make_row("cmb", f"Acoustic transfer function of the photon-baryon fluid in the source row's model: cos(k r_s), r_s = {r_s:g}, times a diffusion envelope exp(-(k/k_d)^2) and a second harmonic beta cos(2 k r_s) (the source's three probes), on the even extension k in [-10 pi, 10 pi] at {n} samples (the transfer function is even in k, so the analytic signal has no edge at k = 0); cuts and extrema read on 0 < k r_s < 8 pi; a fourth probe adds the baryon-loading offset -R",
                    source="runs/phaseA/crr_retrodictions.txt [g4] (DESCR)",
                    Q="the acoustic scale is a phase quantity and the A3 cut on the intrinsic phase estimates it where the peak finder does not: on the damped mode the antipodal cuts on the analytic-signal phase fall at k r_s = n pi while the extrema are pulled inward by the envelope and sit at a spacing below pi/r_s",
                    ingredient="A3 (antipodal cut on the analytic-signal phase, antipodal_cuts), D5 (occasion = one acoustic half-cycle in k), the H-CUT reading (antipode against extremum)",
                    null="the extrema of the transfer function (maxima and minima, sub-sample refined): the domain's raw peak positions",
                    domain="the acoustic scale l_A = pi D_A / r_s is defined by the phase k r_s = n pi of the linear acoustic solution; the displacement of the observed peaks from it is modelled by a per-peak phase shift phi_n (Hu, Fukugita, Zaldarriaga & Tegmark 2001), i.e. the domain reads its peaks through the phase",
                    numbers=per_probe + f"; offset probe ({name_o}): A3 on the mean-removed signal {len(kc_o)} cuts below 8 pi at k r_s/pi = {np.array2string(kc_o / math.pi, precision=4, separator=', ', max_line_width=1000)}, max |spacing - 1| {np.abs(sa_o - 1.0).max():.2f}; with a one-period running-mean detrender {len(kc_o2)} cuts, max |spacing - 1| {np.abs(sa_o2 - 1.0).max():.3f} (the same detrender on the k_d = 8 probe without offset: max |spacing - 1| {np.abs(sa_3rm - 1.0).max():.3f}); extrema of the offset probe: max |spacing - 1| {np.abs(se_o - 1.0).max():.3f}",
                    tg=f"k_d = 8: A3 spacing {a3_mean:.5f} vs null extremum spacing {ex_mean:.5f} (units of pi/r_s): {ag(a3_mean, ex_mean)}",
                    tn=f"the definition of the acoustic scale gives spacing {domain_spacing:.5f}: {ag(a3_mean, domain_spacing, TOL_N)} (the domain has Q)" if rel(a3_mean, domain_spacing) <= TOL_N else f"the definition gives {domain_spacing:.5f}: {ag(a3_mean, domain_spacing, TOL_N)}",
                    tc=f"every A3 spacing within 0.005 of one on the three zero-baseline probes (largest deviation {max(rr[3] for rr in res):.2e}): {hf(check)}",
                    out=out,
                    reading=f"the cut does real work against the peak finder (T-G: the k_d = 8 extrema are spaced at {ex_mean:.4f} pi/r_s on average, a spread of {ex_spread:.4f} among them and a scale {100.0 * (1.0 - ex_mean):.1f} % too small, while the cuts sit at n pi to {a3_max:.1e}), and what it does is demodulation: with the envelope slow against the carrier the analytic-signal phase is the carrier's phase (Bedrosian), and the domain defines the acoustic scale by that phase and models the displacement of its peaks from it. The number is the domain's definition; the synthesis reading is {out}. On the domain's own waveform with the baryon-loading offset the instrument's phase is not the acoustic phase (max spacing error {np.abs(sa_o - 1.0).max():.2f} against {np.abs(se_o - 1.0).max():.2f} for the extrema), so A3 reaches the real spectrum only after the domain removes the baseline it models: the phase that works is the domain's",
                    weakness=f"the source row's model, not a Boltzmann code: r_s = 1 units, no projection to multipoles, no noise, one damping scale per probe; the even extension is exact for these probes and is what removes the edge that a half-line record has; the running-mean detrender that rescues the drifting baseline of row 1 degrades the damped probe here ({np.abs(sa_3rm - 1.0).max():.3f}), so no single named detrender serves both carriers",
                    elegance="The ripples in the sky are spaced by their beat, not by their crests: damping pulls the crests inward, but the beat keeps time. A child can count beats on a fading drum.",
                    child="A drum that is fading still keeps its beat. If you mark where the sound is loudest, the fading pulls those marks a little early; if you mark the beat itself, the marks stay evenly spaced. The pattern of hot and cold spots in the oldest light in the sky is like that fading drum, and scientists measure its beat, not its loudest points.")


# ---------------------------------------------------------------- 39: [h2] 2-D Ising critical isotherm: rho across the divergence
def r4():
    eta, nu, beta_mag = Fraction(1, 4), Fraction(1), Fraction(1, 8)          # declared exact inputs (Onsager; Yang)
    gamma = (2 - eta) * nu
    delta = 1 + gamma / beta_mag
    d = float(delta)
    Bc = 1.0
    beta_c = math.log(1.0 + math.sqrt(2.0)) / 2.0
    m = lambda h: Bc * math.copysign(abs(h) ** (1.0 / d), h)
    chi = lambda h: Bc / d * abs(h) ** (1.0 / d - 1.0)
    I = lambda h: beta_c * chi(h)                                          # Fisher information per spin in the field coordinate
    sig_m = lambda h: math.sqrt(chi(h) / beta_c)                          # sqrt Var(m) per spin (fluctuation-dissipation)
    h1s = (0.1, 0.01, 0.001)
    rows = []
    for h1 in h1s:
        r_i = 2.0 * h1 * math.sqrt(I(h1))                                   # field coordinate, unit at the window edge
        r_ii = 2.0 * m(h1) / sig_m(h1)                                      # magnetisation coordinate, unit at the edge
        r_iii = quad(lambda h: math.sqrt(I(h)), -h1, h1, points=[0.0], limit=200)[0]   # the local unit integrated (D2)
        rows.append((h1, r_i, r_ii, r_iii, 2.0 * h1, 2.0 * m(h1)))
    lh = np.log(np.asarray(h1s))
    slope = lambda col: float(np.polyfit(lh, np.log(np.asarray([rr[col] for rr in rows])), 1)[0])
    s_i, s_ii, s_iii, s_fh, s_fm = slope(1), slope(2), slope(3), slope(4), slope(5)
    exp_domain = (d + 1.0) / (2.0 * d)
    ratio_iii_i = rows[0][3] / rows[0][1]
    ratio_ii_i = rows[0][2] / rows[0][1]
    L_closed = lambda h1: (d / 4.0) * math.sqrt(beta_c * Bc / d) * h1 ** exp_domain   # (15/4) sqrt(beta B_c/15) h1^(8/15)
    h_small = 1e-6
    check = all(abs(s - exp_domain) <= 0.01 for s in (s_i, s_ii, s_iii)) and all(np.isfinite([rr[3] for rr in rows]))
    out = outcome(crr=s_i, null=s_fh, domain=exp_domain, check=check)
    return make_row("ising", f"2-D Ising critical isotherm T = Tc in the scaling regime: m(h) = B_c sgn(h) |h|^(1/delta), chi = dm/dh, Fisher information per spin I_hh = beta_c chi (fluctuation-dissipation), beta_c = ln(1 + sqrt 2)/2 = {beta_c:.6f}, B_c = {Bc:g}; delta = 1 + gamma/beta_mag = {delta} from the declared exact exponents eta = {eta}, nu = {nu}, beta_mag = {beta_mag} (gamma = {gamma})",
                    source="runs/phaseA/crr_retrodictions.txt [h2] (CONSIST)",
                    Q="the resolution across a field window [-h1, h1] on the critical isotherm is finite although the Fisher metric diverges at h = 0, and the number of resolvable magnetisation steps scales as h1^((delta + 1)/(2 delta)) = h1^(8/15): the source row's rho -> inf is the unit taken at the singular point, not the count across the window",
                    ingredient="A1'/D1 (the unit as the system's own step, sqrt Var(m) = the Cramer-Rao length; rho = extent/unit) read three ways: (i) field coordinate with the unit at the window edge; (ii) magnetisation coordinate with the unit at the edge; (iii) the local unit integrated across the window (the Fisher length, D2)",
                    null="an outside unit: a fixed field step (rho = 2 h1, exponent 1) or a fixed magnetisation step (rho = 2 m(h1), exponent 1/delta)",
                    domain="thermodynamic length along the critical isotherm (Ruppeiner; Wootters' count of distinguishable states): L = int sqrt(beta_c chi(h)) dh = (delta/4) sqrt(beta_c B_c/delta) h1^((delta + 1)/(2 delta)), finite because |h|^(-7/15) is integrable; Fisher additivity multiplies it by sqrt N",
                    numbers="; ".join(f"h1 = {h1:g}: rho (i) = {ri:.6f}, (ii) = {rii:.6f}, (iii) = {riii:.6f} (closed form {L_closed(h1):.6f}); null 2 h1 = {fh:.4f}, 2 m(h1) = {fm:.4f}" for h1, ri, rii, riii, fh, fm in rows)
                    + f"; ratios (iii)/(i) = {ratio_iii_i:.4f} (= delta/8 = {d / 8.0:.4f}), (ii)/(i) = {ratio_ii_i:.4f} (= delta); log-log exponents over the grid: (i) {s_i:.4f}, (ii) {s_ii:.4f}, (iii) {s_iii:.4f}, (delta + 1)/(2 delta) = {exp_domain:.4f}; null exponents: fixed field unit {s_fh:.4f}, fixed magnetisation unit {s_fm:.4f}; at h = {h_small:g} the field-coordinate unit 1/sqrt(I) = {1.0 / math.sqrt(I(h_small)):.2e} (-> 0) and the magnetisation unit sqrt Var(m) = {sig_m(h_small):.2e} (-> inf): D1 with one unit taken there reads rho -> inf in the field coordinate and rho -> 0 in the magnetisation coordinate",
                    tg=f"exponent with the system's unit (reading i) {s_i:.4f} vs null fixed field unit {s_fh:.4f}: {ag(s_i, s_fh)}",
                    tn=f"the thermodynamic length gives the exponent {exp_domain:.4f} and reading (iii) is that integral: {ag(s_i, exp_domain, TOL_N)} (the domain has Q)" if rel(s_i, exp_domain) <= TOL_N else f"the thermodynamic length gives {exp_domain:.4f}: {ag(s_i, exp_domain, TOL_N)}",
                    tc=f"the three readings each within 0.01 of {exp_domain:.4f} and finite at every h1: {hf(check)}",
                    out=out,
                    reading=f"the unit does real work against an outside step (T-G), and the finite, delta-fixed count it produces is the thermodynamic length of the critical isotherm, the domain's, with the exponent set by delta, which is external; the field direction here says what batch 02 row 3 said of the temperature direction (an integrable divergence, a finite length), so the source row's rho -> inf and the 'fixed window -> inf' of its weakness line are the unit evaluated at h = 0 rather than integrated. The synthesis reading is {out}. Recorded, not repaired: D1 as written (one sigma for the family) gives three values for the same window, in the ratio 1 : {ratio_iii_i:.3f} : {ratio_ii_i:.1f}, because the unit varies along the family and the two coordinates differ by the factor delta at the edge; only the integrated reading is coordinate-free, and it is D2's",
                    weakness="the scaling form only: no exact m(h, Tc) exists for the 2-D Ising model in a field, so the window must stay inside the scaling regime; B_c and beta_c are unit choices that cancel in the exponent; sqrt Var(m) as the unit is the Gaussian-fluctuation reading of A1' at a point where the magnetisation distribution is not Gaussian; per spin (N = 1), Fisher additivity supplies sqrt N")


# ---------------------------------------------------------------- 40: [h3] Landau pitchfork: resolvable steps between the two phases
def r5():
    a, b, beta, xi0 = 1.0, 1.0, 1.0, 1.0
    taus = (0.1, 0.01, 0.001)
    dims = (2, 3, 4, 5)
    phi0 = lambda tau: math.sqrt(a * tau / b)
    chi_b = lambda tau: 1.0 / (2.0 * a * tau)
    xi = lambda tau: xi0 * tau ** (-0.5)
    rho_own = lambda tau, dim: 2.0 * phi0(tau) / math.sqrt(chi_b(tau) / (beta * xi(tau) ** dim))   # extent 2 phi0 over sqrt Var(phi) on xi^d
    rho_fixedV = lambda tau: 2.0 * phi0(tau) / math.sqrt(chi_b(tau) / beta)                        # the same at fixed volume V = 1
    source_sep = lambda tau: 2.0 * phi0(tau) * math.sqrt(chi_b(tau))                               # the source row's 2 phi0 sqrt(I), I = chi
    lt = np.log(np.asarray(taus))
    slope = lambda f: float(np.polyfit(lt, np.log(np.asarray([f(t) for t in taus])), 1)[0])
    slopes = {dim: slope(lambda t, dim=dim: rho_own(t, dim)) for dim in dims}
    s_fixed_unit = slope(lambda t: 2.0 * phi0(t))
    s_fixedV = slope(rho_fixedV)
    s_source = slope(source_sep)
    ginzburg = {dim: 1.0 - dim / 4.0 for dim in dims}
    check = all(abs(slopes[dim] - ginzburg[dim]) <= 0.01 for dim in dims)
    out = outcome(crr=slopes[3], null=s_fixed_unit, domain=ginzburg[3], check=check)
    return make_row("landau", f"Landau mean-field pitchfork F = a t phi^2/2 + b phi^4/4 - h phi (a = b = {a:g}, beta = {beta:g}) below Tc (t = -tau, tau in {taus}), with Gaussian fluctuations of the order parameter averaged over one correlation volume xi^d, xi = xi0 tau^(-1/2) (mean-field nu = 1/2), xi0 = {xi0:g}, d in {dims}",
                    source="runs/phaseA/crr_retrodictions.txt [h3] (CONSIST)",
                    Q="the number of resolvable steps between the two ordered phases (the antipodal pair +phi0, -phi0: extent 2 phi0 in the system's own unit sigma_phi = sqrt(chi/(beta xi^d))) closes as tau^(1 - d/4) on the approach to Tc: the phases stop being resolvable at the transition for d < 4 and stay resolvable for d > 4",
                    ingredient="A1'/D1 (the unit is the system's own fluctuation of the occasion statistic phi, rho = extent/unit), A3/D5 (the two phases as the antipodal pair; the reversal between them is the cut, batch 06 row 2)",
                    null="an outside fixed unit sigma (rho = 2 phi0/sigma, exponent beta_mag = 1/2); also printed: the source row's own quantity 2 phi0 sqrt(chi) (exponent 0) and the own unit at fixed volume V = 1 (exponent 1)",
                    domain="the Ginzburg criterion (Levanyuk 1959; Ginzburg 1960): mean-field theory is self-consistent while <delta phi^2>_(xi^d) = k_B T chi / xi^d << phi0^2, and the ratio phi0 / sqrt(<delta phi^2>) ∝ |t|^(1 - d/4) gives the upper critical dimension 4",
                    numbers="; ".join(f"d = {dim}: rho = " + ", ".join(f"{rho_own(t, dim):.4f}" for t in taus) + f" at tau = {taus}, log-log exponent {slopes[dim]:+.4f} (1 - d/4 = {ginzburg[dim]:+.2f})" for dim in dims)
                    + f"; fixed outside unit: rho = 2 phi0 = " + ", ".join(f"{2.0 * phi0(t):.4f}" for t in taus) + f", exponent {s_fixed_unit:.4f}; own unit at fixed volume V = 1: rho = " + ", ".join(f"{rho_fixedV(t):.4f}" for t in taus) + f", exponent {s_fixedV:.4f}; the source row's 2 phi0 sqrt(chi) = " + ", ".join(f"{source_sep(t):.4f}" for t in taus) + f" (sqrt(2/b) = {math.sqrt(2.0 / b):.4f}), exponent {s_source:.4f}",
                    tg=f"exponent with the own unit on xi^3, {slopes[3]:.4f}, vs null fixed unit {s_fixed_unit:.4f}: {ag(slopes[3], s_fixed_unit)}",
                    tn=f"the Ginzburg criterion gives 1 - d/4 = {ginzburg[3]:.4f} at d = 3: {ag(slopes[3], ginzburg[3], TOL_N)} (the domain has Q)" if rel(slopes[3], ginzburg[3]) <= TOL_N else f"the Ginzburg criterion gives {ginzburg[3]:.4f}: {ag(slopes[3], ginzburg[3], TOL_N)}",
                    tc=f"the exponent within 0.01 of 1 - d/4 at d = 2, 3, 4 and 5: {hf(check)}",
                    out=out,
                    reading=f"the unit does real work (T-G: a fixed unit sees the phases separate as tau^0.5, the system's own unit on its correlation volume sees them close as tau^{slopes[3]:.2f} at d = 3 and hold at d = 4), and the count it produces is Ginzburg's ratio of the order parameter to its fluctuation over a correlation volume, with the upper critical dimension where the exponent changes sign: the domain's criterion, CRR's name. The synthesis reading is {out}. Recorded, not repaired: the source row's 'two-phase Fisher separation 2 phi0 sqrt(I) = sqrt(2/b), O(1) constant' multiplies a magnetisation by the square root of the field-direction metric; in the order-parameter coordinate the separation is 2 phi0 sqrt(beta V/chi), which closes as tau^{s_fixedV:.1f} at fixed volume, and the source's own h5 row ('the two superradiant phases merge in Fisher distance') is the consistent reading",
                    weakness="mean-field nu and Gaussian fluctuations throughout, so the exponent is the classical one on both sides of the comparison; the correlation volume as the averaging region is the domain's choice, not CRR's (a fixed volume gives exponent 1, and D1 does not say which volume); the two phases are named as antipodes without a rotor being run (the driven reversal is batch 06 row 2); beta_mag = 1/2 and nu = 1/2 are external",
                    elegance="Near the tipping point the two choices move closer together while the jitter grows, and whether the jitter wins depends only on the number of dimensions: below four it does, above four it does not. A rule with one integer and no knobs.",
                    child="Imagine a crowd deciding to face left or right. Near the moment when it cannot decide, 'left' and 'right' look more and more alike, and everyone fidgets more. In our three-dimensional world the fidgeting wins near that moment, so you cannot tell which way the crowd has chosen; in a world with more than four directions you still could.")


def main():
    return run_batch("Synthesis batch 08: rows 36-40 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
