"""Synthesis batch 04: rows 16-20 of QUEUE.md (prompt-log entry 61).
main [22] (CONSIST) Omori aftershock decay: the sequence in the system's own unit (natural time).
main [23] (DESCR) Hawkes process, exponential kernel: path vs endpoint (H-T1) on a point process.
main [25] (DESCR) Kepler ellipse e = 0.6: the A3 cut and the two half-orbit arcs.
main [26] (DESCR) Binary inspiral chirp: A3 occasions against the post-Newtonian half-cycle count.
main [29] (CONSIST) Hopf normal form: the resolution rho with the unit measured (A1') instead of fixed.

Every number printed is computed here (R1); every verdict word is an f-string of a comparison (R15). No data
file is opened (R2). Deterministic: fixed seeds, fixed grids, stochastic Heun on a fixed step.
Run:  uv run python theory/retrodictions/synthesis_batches/batch_04.py
"""
import math
import sys

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import kstest, spearmanr

from crr.instrument.core import antipodal_cuts, arc_length, cv, intrinsic_phase, peak_cuts
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def ag(a, b, tol=TOL_G):
    return "agree" if rel(a, b) <= tol else "differ"


def hf(ok):
    return "holds" if ok else "fails"


# ---------------------------------------------------------------- 16: [22] Omori aftershock decay
def _omori_events(K, c, p, T, seed):
    """Inhomogeneous Poisson process with lambda(t) = K (t + c)^-p by Ogata's thinning for a decreasing rate
    (the bound over [t, t'] is lambda(t)); exact, and independent of the compensator used to read the result."""
    rng = np.random.default_rng(seed)
    lam = lambda t: K * (t + c) ** (-p)
    t, ev = 0.0, []
    while True:
        L = lam(t)
        tn = t + rng.exponential(1.0 / L)
        if tn > T:
            break
        if rng.uniform() < lam(tn) / L:
            ev.append(tn)
        t = tn
    return np.asarray(ev)


def r1():
    K, c, p, T = 20000.0, 0.01, 1.1, 365.0
    A = lambda t: K / (1.0 - p) * ((t + c) ** (1.0 - p) - c ** (1.0 - p))       # the compensator, P5's A(t)
    ev = _omori_events(K, c, p, T, seed=22)
    n = len(ev)
    dt = np.diff(ev); dA = np.diff(A(ev)); dN = np.ones(n - 1)
    cv_clock, cv_nat, cv_count = cv(dt), cv(dA), float(np.std(dN, ddof=1) / abs(np.mean(dN)))
    mean_nat = float(dA.mean())
    ks = kstest(dA, "expon"); ks_d, ks_p = float(ks.statistic), float(ks.pvalue)
    rho_trend = float(spearmanr(dA, np.arange(n - 1))[0])
    domain_cv = 1.0                                                              # Exp(1): CV = 1 exactly
    check = abs(mean_nat - 1.0) <= TOL_N and abs(cv_nat - 1.0) <= TOL_N and ks_p > 0.05
    out = outcome(crr=cv_nat, null=cv_clock, domain=domain_cv, check=check)
    return make_row("seis", f"Omori aftershock decay lambda = K (t + c)^-p as an inhomogeneous Poisson process (K = {K:g}, c = {c:g}, p = {p:g}, T = {T:g} days; Ogata thinning, seed 22), read in the system's own unit",
                    source="theory/retrodictions/crr_retrodictions.txt [22] (CONSIST)",
                    Q="measured in the system's own unit (A1': one event = one step; natural time = the compensator A(t) = int lambda, the clock P5 uses), the occasions of an Omori sequence are i.i.d. unit exponential (mean 1, CV 1, no trend) for every p: in natural time the aftershock sequence is a homogeneous Poisson process",
                    ingredient="A1'/D1 (the unit is the system's own step, one event; natural time), D5 (occasion = inter-event interval), P5 (retention in natural time)",
                    null="the clock: the inter-event intervals in clock time, the domain's raw observable",
                    domain="the time-rescaling theorem (Meyer 1971; Ogata 1988, residual analysis of point processes): the compensator maps any point process with intensity lambda(t) to a unit-rate Poisson process",
                    numbers=f"{n} events in {T:g} days (expected A(T) = {A(T):.1f}); clock intervals: CV = {cv_clock:.4f}, first {dt[0]:.2e}, last {dt[-1]:.2e} days; natural-time intervals dA: mean = {mean_nat:.4f}, CV = {cv_nat:.4f}, KS distance to Exp(1) = {ks_d:.4f} (p = {ks_p:.3f}), Spearman(dA, event index) = {rho_trend:+.4f}; the other reading of A1' (natural time = the event count) gives dN = 1 per occasion, CV = {cv_count:.4f} by definition",
                    tg=f"CV(dA) {cv_nat:.4f} vs null CV(dt) {cv_clock:.4f}: {ag(cv_nat, cv_clock)}",
                    tn=f"the time-rescaling theorem gives CV = {domain_cv:.4f} and mean 1 in natural time: {ag(cv_nat, domain_cv, TOL_N)} (the domain has Q)" if rel(cv_nat, domain_cv) <= TOL_N else f"the time-rescaling theorem gives CV = {domain_cv:.4f}: {ag(cv_nat, domain_cv, TOL_N)}",
                    tc=f"mean dA and CV(dA) within {TOL_N:g} of 1 and KS p > 0.05: {hf(check)}",
                    out=out,
                    reading=f"the unit does real work (T-G: the clock intervals span {dt[-1] / dt[0]:.0f}x while the natural-time intervals are stationary), and the object it produces is the compensator: putting an aftershock sequence into natural time and testing it for stationary Poisson is Ogata's residual analysis, the tool seismology uses to check an Omori or ETAS fit; CRR renames it. P5's 'power law iff p = 1' is calculus on the same object, so the source row's CONSIST stands and the synthesis reading is {out}",
                    weakness=f"A1' names natural time as the event count; the count reading makes every occasion one step (CV {cv_count:.1f}, a tautology) and the compensator reading (P5's A(t)) gives the exponential; the row uses the second, and CRR.md D2 rejects the integer counter. K, c and p are the domain's fitted constants, not CRR's",
                    elegance="The shocks keep their own clock. Numbered by their own expected count instead of by the minutes, every aftershock gap is the same kind of gap: a rule with no knobs, and it is also the domain's own test of an Omori fit.",
                    child="After a big earthquake the small ones come fast at first and then slower and slower. If you put away the stopwatch and let the earthquakes count themselves, the gaps stop shrinking: each next shock is just as much of a surprise as the last. The earthquakes have their own clock, and it ticks once per shock.")


# ---------------------------------------------------------------- 17: [23] Hawkes process, exponential kernel
def _hawkes(mu, a, b, n, seed):
    """Exponential-kernel Hawkes process by Ogata thinning on the Markov intensity (bound = current intensity,
    which decays between events). Returns event times, intensity just before and just after each event."""
    rng = np.random.default_rng(seed)
    t, lam, ts, lm, lp = 0.0, mu, [], [], []
    while len(ts) < n:
        d = rng.exponential(1.0 / lam); tn = t + d; ln = mu + (lam - mu) * math.exp(-b * d)
        if rng.uniform() < ln / lam:
            ts.append(tn); lm.append(ln); lp.append(ln + a); lam = ln + a
        else:
            lam = ln
        t = tn
    return np.asarray(ts), np.asarray(lm), np.asarray(lp)


def _path_vs_endpoint(mu, a, b, n=200000, seed=23, k=5, burn=1000, nb=40, nc=3):
    """Held-out forecast of the next inter-event interval from the endpoint (intensity after the cut, nb quantile
    bins) and from endpoint x path (nc terciles of the Fisher arc over the last k occasions inside each bin)."""
    ts, lm, lp = _hawkes(mu, a, b, n, seed)
    arc = 2.0 * (np.sqrt(lp[:-1]) - np.sqrt(lm[1:]))            # Poisson-carrier arc of one occasion; the jump at the event excluded (A3)
    ca = np.r_[0.0, np.cumsum(arc)]
    idx = np.arange(burn, n - 1); E = lp[idx]; C = ca[idx] - ca[idx - k]; Y = ts[idx + 1] - ts[idx]
    tr = (idx % 2 == 0); te = ~tr
    qe = np.quantile(E[tr], np.linspace(0, 1, nb + 1)); be = np.clip(np.searchsorted(qe, E, side="right") - 1, 0, nb - 1)

    def fit(with_path):
        pred = np.zeros(len(Y))
        for j in range(nb):
            m = np.where(be == j)[0]; mt = m[tr[m]]
            if not with_path:
                pred[m] = Y[mt].mean(); continue
            qc = np.quantile(C[mt], np.linspace(0, 1, nc + 1)); bc = np.clip(np.searchsorted(qc, C[m], side="right") - 1, 0, nc - 1)
            for jj in range(nc):
                sel = m[bc == jj]; s_tr = sel[tr[sel]]
                pred[sel] = Y[s_tr].mean() if len(s_tr) else Y[mt].mean()
        res = Y[te] - pred[te]
        return float(math.sqrt(res.var())), float(1.0 - res.var() / Y[te].var())
    rmse_e, r2_e = fit(False); rmse_p, r2_p = fit(True)
    pc = np.array([spearmanr(C[be == j], Y[be == j])[0] for j in range(nb)])
    return dict(n=n, lam_lo=float(lp.min()), lam_hi=float(lp.max()), rmse_e=rmse_e, r2_e=r2_e, rmse_p=rmse_p, r2_p=r2_p,
                ps=float(pc.mean()), ps_se=float(pc.std(ddof=1) / math.sqrt(nb)), corr_ec=float(np.corrcoef(E, C)[0, 1]), arc_min=float(arc.min()))


def r2():
    mu, a, b = 0.5, 0.6, 2.0                                          # the source row's parameters (branching ratio a/b = 0.3)
    s = _path_vs_endpoint(mu, a, b)
    a2 = 1.6; s2 = _path_vs_endpoint(mu, a2, b)                        # a more clustered process (branching ratio 0.8), the stringent check
    gain = s["r2_p"] - s["r2_e"]
    check = gain <= 0.005 and abs(s["ps"]) <= 2.0 * s["ps_se"]
    out = outcome(crr=s["rmse_p"], null=s["rmse_e"], domain=s["rmse_e"], check=check)
    return make_row("pp", f"Hawkes process with exponential kernel (mu = {mu:g}, alpha = {a:g}, beta = {b:g}, branching ratio {a / b:g}; {s['n']} events by Ogata thinning, seed 23): H-T1's path against endpoint read on a point process",
                    source="theory/retrodictions/crr_retrodictions.txt [23] (DESCR)",
                    Q="the next occasion's duration is forecast by the endpoint alone: the Fisher arc travelled over the last five occasions adds nothing to a forecast of the next inter-event interval beyond the intensity at the cut (H-T1's must-fail case, on a point process instead of a convex learner)",
                    ingredient="D6/H-T1 (path vs endpoint), D5 (occasion = inter-event interval), A3 (the jump at the event is the cut, not content: excluded from the arc), D2 on the Poisson carrier (arc = 2 |d sqrt(lambda)|)",
                    null="the endpoint: the intensity just after the event, the domain's state variable",
                    domain="the Markov property of the exponential-kernel intensity (Oakes 1975: the exponential kernel is the one kernel for which lambda(t) is Markov); the intensity is a sufficient statistic for the future, so the endpoint forecast is the optimal one",
                    numbers=f"alpha = {a:g}: intensity after the cut in [{s['lam_lo']:.2f}, {s['lam_hi']:.2f}], corr(endpoint, path) = {s['corr_ec']:+.3f}; held-out RMSE of the next interval: endpoint (40 quantile bins) {s['rmse_e']:.5f} (R2 {s['r2_e']:.4f}), endpoint x path terciles {s['rmse_p']:.5f} (R2 {s['r2_p']:.4f}), R2 gain of the path {gain:+.5f}; within-bin Spearman(path, next interval) = {s['ps']:+.4f} +/- {s['ps_se']:.4f} (SE over 40 bins). alpha = {a2:g} (branching ratio {a2 / b:g}): intensity in [{s2['lam_lo']:.2f}, {s2['lam_hi']:.2f}], RMSE endpoint {s2['rmse_e']:.5f} (R2 {s2['r2_e']:.4f}) vs with path {s2['rmse_p']:.5f} (R2 {s2['r2_p']:.4f}), within-bin Spearman {s2['ps']:+.4f} +/- {s2['ps_se']:.4f}",
                    tg=f"RMSE with the path {s['rmse_p']:.5f} vs null endpoint-only {s['rmse_e']:.5f}: {ag(s['rmse_p'], s['rmse_e'])} (alpha = {a2:g}: {s2['rmse_p']:.5f} vs {s2['rmse_e']:.5f}: {ag(s2['rmse_p'], s2['rmse_e'])})",
                    tn="the Markov property makes the endpoint forecast the domain's own optimum, so the domain's value for the target is the null itself",
                    tc=f"held-out R2 gain of the path {gain:+.5f} <= 0.005 and the partial Spearman within 2 SE ({2.0 * s['ps_se']:.4f}): {hf(check)}",
                    out=out,
                    reading=f"the ingredient did no work because the domain's theorem forbids it: with an exponential kernel the intensity screens off the path, so H-T1 must fail here exactly as CRR.md section 5 says it must on the convex learner; the exponential Hawkes process is the point-process twin of that control, and the source row's depth-one reading is the Markov property under another name. The synthesis reading is {out}",
                    weakness="for a power-law kernel (ETAS) the intensity is not Markov and the path would matter, but the domain's own predictor is then the full intensity, which already carries the history: the CRR path would compete with that, not with a scalar endpoint. One estimator (40 intensity bins x 3 path terciles, even/odd split); the branching ratio was varied, the kernel was not")


# ---------------------------------------------------------------- 18: [25] Kepler ellipse e = 0.6
def r3():
    e, a, n_orb, ns = 0.6, 1.0, 8, 4096
    M = np.arange(n_orb * ns) / ns * 2.0 * math.pi                          # mean anomaly = time (unit mean motion)
    E = M.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))               # Kepler's equation, Newton
    r = a * (1.0 - e * np.cos(E))
    nu = np.unwrap(2.0 * np.arctan2(math.sqrt(1 + e) * np.sin(E / 2), math.sqrt(1 - e) * np.cos(E / 2)))
    x, y = r * np.cos(nu), r * np.sin(nu)
    ph = intrinsic_phase(r)
    cuts = antipodal_cuts(ph, start=0)                                        # A3 on the analytic-signal phase of r(t), started at periapsis
    pk = peak_cuts(r, prominence=0.1, distance=100)                            # the apsides as extrema (the domain's own events)
    apsides = np.arange(0, n_orb * ns, ns // 2)
    off_a3 = int(np.max(np.abs(cuts - apsides[:len(cuts)]))); off_pk = int(np.max(np.abs(pk - apsides[1:len(pk) + 1])))
    arcs = lambda cs: np.array([arc_length(np.column_stack([x[i:j + 1], y[i:j + 1]])) for i, j in zip(cs[:-1], cs[1:])])
    ac, ap = arcs(cuts), arcs(pk)
    ds = lambda v: math.sqrt((a * (1 - e ** 2) / (1 + e * math.cos(v))) ** 2 + (a * (1 - e ** 2) * e * math.sin(v) / (1 + e * math.cos(v)) ** 2) ** 2)
    L1, L2 = quad(ds, 0.0, math.pi)[0], quad(ds, math.pi, 2.0 * math.pi)[0]
    # a generic start (true anomaly pi/2): the next cut under four readings of "the phase"
    i0 = int(np.argmin(np.abs(nu - math.pi / 2)))
    nu_h = float(nu[antipodal_cuts(ph, start=i0)[1]])
    nu_nu = float(nu[int(np.argmin(np.abs(nu - (nu[i0] + math.pi))))])
    nu_E = float(nu[int(np.argmin(np.abs(E - (E[i0] + math.pi))))])
    nu_M = float(nu[int(np.argmin(np.abs(M - (M[i0] + math.pi))))])
    readings = (nu_h, nu_nu, nu_E, nu_M)
    spread = max(rel(p_, q_) for p_ in readings for q_ in readings)
    check = rel(L1, L2) <= 1e-9 and off_a3 == 0 and rel(float(ac.mean()), L1) <= TOL_N
    out = outcome(crr=float(ac.mean()), null=float(ap.mean()), domain=L1, check=check)
    return make_row("orb", f"Kepler ellipse e = {e:g}, a = {a:g}, unit mean motion; {n_orb} orbits at {ns} samples per orbit from Kepler's equation; r(t) as the 1-D trace, orbit-plane position for the arc (Euclidean stand-in metric, as the source row)",
                    source="theory/retrodictions/crr_retrodictions.txt [25] (DESCR)",
                    Q="the occasion of an orbit is the apsis-to-apsis half-orbit: the A3 cut on the intrinsic phase of r(t), started at periapsis, lands on apoapsis and periapsis alternately, and the two half-orbit arcs are equal",
                    ingredient="A3 (antipodal cut on the analytic-signal phase, antipodal_cuts), D5 (occasion = half-turn), D2 with a Euclidean stand-in metric",
                    null="the extremum cut (peak_cuts on r: the apsides as extrema, the domain's own events)",
                    domain="reflection symmetry of the ellipse about its major axis: the two half-orbit arcs are equal (closed form by quadrature)",
                    numbers=f"A3 cuts sit on the apsides (max offset {off_a3} samples), extrema too (max offset {off_pk} samples); per-occasion arc under A3: mean {ac.mean():.6f}, spread {ac.max() - ac.min():.1e} over {len(ac)} half-orbits; under extrema: mean {ap.mean():.6f}; quadrature L(peri->apo) = {L1:.6f}, L(apo->peri) = {L2:.6f}, relative difference {rel(L1, L2):.1e}. Generic start at true anomaly {nu[i0]:.4f}: true anomaly at the next cut = {nu_h:.4f} (analytic-signal phase), {nu_nu:.4f} (true anomaly), {nu_E:.4f} (eccentric anomaly), {nu_M:.4f} (mean anomaly): the four readings {'agree' if spread <= TOL_G else 'differ'} (max relative spread {spread:.3f})",
                    tg=f"mean half-orbit arc under A3 {ac.mean():.6f} vs null under extrema {ap.mean():.6f}: {ag(float(ac.mean()), float(ap.mean()))}",
                    tn=f"quadrature by symmetry gives {L1:.6f}: {ag(float(ac.mean()), L1, TOL_N)}",
                    tc=f"L1 = L2 to 1e-9, A3 cuts on the apsides, arc within {TOL_N:g} of quadrature: {hf(check)}",
                    out=out,
                    reading=f"the source row's content exactly: on a trace symmetric about its extrema the antipode and the extremum coincide, so A3 does no work and the equality is the ellipse's symmetry; CRR supplied a name for the apsides. Away from an apsis the four readings of 'the phase' {'agree' if spread <= TOL_G else 'disagree'} on where the next cut falls, so a cut sequence anchored at a generic point is a choice of phase variable, which is Kepler's equation seen from CRR's side. The synthesis reading is {out}",
                    weakness="no statistical carrier: the Euclidean metric is a stand-in that A1 does not license; four phase readings, one implemented (the analytic signal), and only their agreement at the apsides is used",
                    elegance="The cut is a place a child can point at: the far point of the orbit is the antipode of the near point, and the two halves of the trip are mirror images. It teaches what an occasion is without a formula, though the equality is the ellipse's, not CRR's.",
                    child="A planet goes round the sun on a squashed circle. Start when it is closest. Halfway round, it is farthest away; that is where one lap-half ends and the next begins. The two halves of the trip are mirror images, so they are the same length of road.")


# ---------------------------------------------------------------- 19: [26] binary inspiral chirp
def r4():
    k, tc, n = 2000.0, 1.0, 2 ** 18
    t = np.linspace(0.0, 0.99, n)
    Phi = -k * (tc - t) ** (5.0 / 8.0)                                         # leading-order inspiral phase (the source model, k = 40 -> 2000)
    f = k * (5.0 / 8.0) * (tc - t) ** (-3.0 / 8.0) / (2.0 * math.pi)
    A = (f / f[0]) ** (2.0 / 3.0)                                              # quadrupole amplitude ~ f^(2/3)
    h = A * np.cos(Phi)
    ph = intrinsic_phase(h)
    i0, i1 = int(np.searchsorted(t, 0.05)), int(np.searchsorted(t, 0.98))     # interior window: the analytic-signal edge transient is outside it
    cuts = antipodal_cuts(ph[:i1], start=i0)
    pk = peak_cuts(h, prominence=0.1, distance=10); pk = pk[(pk >= i0) & (pk < i1)]
    n_a3, n_pk, n_dom = len(cuts) - 1, len(pk), (Phi[i1 - 1] - Phi[i0]) / math.pi
    tgt = Phi[i0] + math.pi * np.arange(1, len(cuts)); td = np.interp(tgt, Phi, t)
    half = np.diff(np.r_[t[i0], td]); off = np.abs(t[cuts[1:]] - td) / half
    phase_err = float(np.max(np.abs((ph - ph[i0]) - (Phi - Phi[i0]))[i0:i1]))
    T = np.diff(t[cuts]); C = np.array([arc_length(h[i:j]) for i, j in zip(cuts[:-1], cuts[1:])]); P = np.diff(ph[cuts]) / math.pi
    check = float(off.max()) <= TOL_N
    out = outcome(crr=float(n_a3), null=float(n_pk), domain=float(n_dom), check=check)
    return make_row("gw", f"Binary inspiral chirp at leading post-Newtonian order, dimensionless: Phi(t) = -k (t_c - t)^(5/8), k = {k:g}, t_c = {tc:g}, amplitude ~ f^(2/3), t in [0, 0.99] at 2^18 samples; analysed on t in [0.05, 0.98)",
                    source="theory/retrodictions/crr_retrodictions.txt [26] (DESCR)",
                    Q="the number of occasions the binary completes between two instants is the number of half-turns of its gravitational-wave phase: the model-free A3 count on the strain's intrinsic phase equals the post-Newtonian half-cycle count, and each A3 cut falls on the post-Newtonian half-turn",
                    ingredient="A3 (antipodal cut on the analytic-signal phase of h(t)), D5 (occasion = half-turn), H-L5 read as natural time = phase",
                    null="extremum counting (peak_cuts on h: one extremum per half-cycle)",
                    domain="the post-Newtonian phase: N_half = (Phi(t2) - Phi(t1))/pi with Phi ~ (t_c - t)^(5/8), the cycles-to-merger count every matched filter integrates",
                    numbers=f"window frequency {f[i0]:.1f} -> {f[i1]:.1f} (dimensionless); A3 occasions {n_a3}, extrema {n_pk}, post-Newtonian half-turns {n_dom:.3f}; offset of each A3 cut from its post-Newtonian half-turn instant: max {off.max():.4f}, mean {off.mean():.5f} of the local half-period; max |analytic-signal phase - Phi| in the window = {phase_err:.4f} rad; per occasion: CV(clock) = {cv(T):.4f} (half-period {T[0]:.5f} -> {T[-1]:.5f}), CV(arc, identity metric) = {cv(C):.4f} (arc {C[0]:.3f} -> {C[-1]:.3f}), CV(phase increment) = {cv(P):.5f} (pi by construction of the cut)",
                    tg=f"A3 count {n_a3} vs null extrema count {n_pk}: {ag(float(n_a3), float(n_pk))}",
                    tn=f"post-Newtonian half-turn count {n_dom:.3f}: {ag(float(n_a3), float(n_dom), TOL_N)}",
                    tc=f"every A3 cut within {TOL_N:g} of a half-period of its post-Newtonian instant: {hf(check)}",
                    out=out,
                    reading=f"the source row's 'says nothing' survives synthesis: on a chirp every half-turn carries one extremum, so A3 counts what peak counting counts, and both count what the post-Newtonian phase already integrates; the H-L5 numbers show the chirp is neither arc-regular nor clock-regular (both trend with the frequency) and phase-regular by construction of the cut. The synthesis reading is {out}",
                    weakness="no statistical carrier for the strain (identity metric); the template manifold with the noise-weighted inner product is the domain's Fisher-native carrier and was not used; leading post-Newtonian order only, no noise")


# ---------------------------------------------------------------- 20: [29] Hopf normal form
def _hopf_cut_radii(mu, D, w=1.0, dt=0.01, n_real=1000, burn=20, n_cyc=40, seed=29):
    """Stochastic Hopf normal form dz = ((mu + i w) z - |z|^2 z) dt + sqrt(2D) dW (complex W, independent parts),
    stochastic Heun (weak order 2 for additive noise). Occasion = half-turn of the normal form's own angle;
    returns |z| at every cut after burn-in, over n_real independent realisations."""
    rng = np.random.default_rng(seed)
    z = np.full(n_real, math.sqrt(mu) + 0j); s = math.sqrt(2.0 * D * dt)
    f = lambda z_: (mu + 1j * w) * z_ - np.abs(z_) ** 2 * z_
    n_st = int(round((burn + n_cyc) * 2.0 * math.pi / dt))
    th_prev = np.angle(z); tot = np.zeros(n_real); k_prev = np.floor(tot / math.pi); rs = []
    for st in range(n_st):
        xi = (rng.normal(size=n_real) + 1j * rng.normal(size=n_real)) * s
        zp = z + f(z) * dt + xi
        z = z + 0.5 * (f(z) + f(zp)) * dt + xi
        th = np.angle(z); tot += np.angle(np.exp(1j * (th - th_prev))); th_prev = th
        if st * dt > burn * 2.0 * math.pi:
            kn = np.floor(tot / math.pi); m = kn > k_prev
            if m.any():
                rs.append(np.abs(z[m]))
            k_prev = kn
    return np.concatenate(rs)


def _hopf_density_stats(mu, D):
    """Median and 1.4826 MAD of the stationary radial density P(r) ~ r exp((mu r^2/2 - r^4/4)/D), by quadrature."""
    r = np.linspace(0.0, 3.0 * math.sqrt(mu) + 0.5, 400001)
    lp = np.log(r + 1e-300) + (mu * r ** 2 / 2.0 - r ** 4 / 4.0) / D
    P = np.exp(lp - lp.max()); cdf = np.cumsum(P); cdf /= cdf[-1]
    med = float(np.interp(0.5, cdf, r))
    mad = brentq(lambda a_: np.interp(med + a_, r, cdf) - np.interp(med - a_, r, cdf) - 0.5, 1e-9, 1.0)
    return med, 1.4826 * float(mad)


def r5():
    D, sig_fixed, mus = 1e-4, 0.05, (0.1, 0.3, 1.0)
    rows = []
    for mu in mus:
        s = _hopf_cut_radii(mu, D)
        med = float(np.median(s)); sig = 1.4826 * float(np.median(np.abs(s - med)))     # A1': residual about the named detrender (the median), MAD scale
        med_d, sig_d = _hopf_density_stats(mu, D)
        rows.append(dict(mu=mu, n=len(s), med=med, sig=sig, rho=2.0 * med / sig, med_d=med_d, sig_d=sig_d, rho_d=2.0 * med_d / sig_d,
                         rho_fixed=2.0 * med / sig_fixed, ou=math.sqrt(D / (2.0 * mu))))
    lm = np.log(np.asarray(mus)); slope = lambda key: float(np.polyfit(lm, np.log([r_[key] for r_ in rows]), 1)[0])
    ex_crr, ex_null, ex_dom = slope("rho"), slope("rho_fixed"), slope("rho_d")
    worst = max(rel(r_["rho"], r_["rho_d"]) for r_ in rows)
    check = rel(ex_dom, 1.0) <= 0.02 and worst <= TOL_N
    out = outcome(crr=ex_crr, null=ex_null, domain=ex_dom, check=check)
    return make_row("bif", f"Stochastic Hopf normal form dz = ((mu + i) z - |z|^2 z) dt + sqrt(2D) dW, D = {D:g}, mu in {mus} (mu/sqrt(D) = {mus[0] / math.sqrt(D):.0f}..{mus[-1] / math.sqrt(D):.0f}); stochastic Heun, dt = 0.01, 1000 realisations x 40 cycles after a 20-cycle burn-in, seed 29; occasion = half-turn of the normal form's own angle, occasion statistic = |z| at the cut, unit sigma = 1.4826 MAD about the median across occasions, rho = 2 median/sigma (source model h_hopf, which fixed sigma = {sig_fixed:g})",
                    source="theory/retrodictions/crr_retrodictions.txt [29] (CONSIST)",
                    Q="the resolution of a noisy Hopf oscillator vanishes linearly in the distance to the bifurcation, rho ~ mu (exponent 1), not as the amplitude sqrt(mu): the system's own unit grows as mu^-1/2 while the amplitude shrinks as mu^1/2",
                    ingredient="A1'/D1 (the unit is the system's own resolvable step, measured from the occasion statistic's residual; rho = extent/sigma), A3/D5 (occasion = half-turn of the intrinsic angle)",
                    null=f"the source row's fixed outside unit sigma = {sig_fixed:g} (rho = 2 median/{sig_fixed:g})",
                    domain="the stationary density of the stochastic Hopf normal form, P(r) ~ r exp((mu r^2/2 - r^4/4)/D): the drift is -grad U plus a rotation tangent to U's level sets, so P ~ exp(-U/D); its median and MAD give the same rho by quadrature (the amplitude signal-to-noise ratio of the noisy precursor)",
                    numbers="; ".join(f"mu = {r_['mu']:g}: {r_['n']} occasions, median |z| = {r_['med']:.5f}, measured sigma = {r_['sig']:.5f} (density: median {r_['med_d']:.5f}, sigma {r_['sig_d']:.5f}; linearised sqrt(D/2mu) = {r_['ou']:.5f}), rho measured = {r_['rho']:.2f}, rho from the density = {r_['rho_d']:.2f} (relative difference {rel(r_['rho'], r_['rho_d']):.4f}), rho with sigma fixed = {r_['rho_fixed']:.2f}" for r_ in rows)
                            + f"; exponent d ln rho / d ln mu over the grid: measured unit {ex_crr:.4f}, fixed unit {ex_null:.4f}, density {ex_dom:.4f}",
                    tg=f"exponent with the measured unit {ex_crr:.4f} vs null with the fixed unit {ex_null:.4f}: {ag(ex_crr, ex_null)}",
                    tn=f"the stationary density gives exponent {ex_dom:.4f} and rho within {worst:.4f} (relative) at every mu: {ag(ex_crr, ex_dom, TOL_N)}" + (" (the domain has Q)" if rel(ex_crr, ex_dom) <= TOL_N else ""),
                    tc=f"density exponent within 0.02 of 1 and measured rho within {TOL_N:g} of the density's at every mu: {hf(check)}",
                    out=out,
                    reading=f"A1' does real work (T-G): measuring the unit turns the source row's sqrt(mu) into mu, and 'true if sigma is fixed' was the source row's own caveat. The number it produces is the amplitude signal-to-noise ratio of the noisy normal form, which the stationary density gives in closed form: the domain has the mu law (the noisy-precursor literature computes exactly these fluctuations), and CRR's part is to insist that the unit be measured, which the domain does whenever it computes fluctuations. The synthesis reading is {out}",
                    weakness="the exponent is asymptotic (mu >> sqrt(D)); at mu/sqrt(D) of order one the density is far from Gaussian and neither reading is a power law; the median is the stationary case of A1''s named detrender, and the normal form's own angle stands in for the analytic-signal phase; D is the domain's constant",
                    elegance="One picture with one moving ruler: as the knob approaches the tipping point the wobble shrinks and the system's own ruler grows, so the number of wobbles it can tell apart vanishes twice as fast (in the exponent) as the wobble itself.",
                    child="Think of a wobble that fades out as you turn a knob toward the point where it stops. Near that point the wobble gets small, but it also gets jittery, so the thing is worse and worse at telling one of its own wobbles from the next. Its own ruler gets longer just as the thing it measures gets shorter.")


def main():
    return run_batch("Synthesis batch 04: rows 16-20 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
