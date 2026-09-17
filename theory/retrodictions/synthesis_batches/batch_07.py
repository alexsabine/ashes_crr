"""Synthesis batch 07: rows 31-35 of QUEUE.md (prompt-log entry 61). Daniel's battery [d5] N-probe phase estimation
CRB (the QFI of a Ramsey probe as one minus the overlap with its A3 half-turn image); [e1] Hopf normal form: extent,
relaxation, D8 depth (H-L5's class boundary on the nonisochronous normal form; 'D8' is v3.1's O1, which declines);
[e2] driven damped Duffing: antipode vs extremum (three named intrinsic phases place the antipode differently);
[e4] ideal LC tank: the perfectly symmetric baseline (every proper quantity against its null, and no unit);
[f2] Omori sequence p = 1: retention consistency (Fisher arc per aftershock in the system's own unit)."""
import math
import sys

import numpy as np
from scipy.stats import spearmanr

from crr.instrument.core import antipodal_cuts, arc_length, chord, cv, intrinsic_phase, peak_cuts, unit_sigma
from crr.synthesis.harness import TOL_G, TOL_N, make_row, outcome, rel, run_batch


def _word(cond, yes, no):
    return yes if cond else no


def _sz(v, nd=4):
    """signed fixed-point, without a signed zero."""
    return f"{0.0:.{nd}f}" if abs(v) < 0.5 * 10 ** (-nd) else f"{v:+.{nd}f}"


# ---------------------------------------------------------------- 31 [d5] the Ramsey probe and its A3 half-turn image
def r1():
    def overlap_sq(p, phi):                                          # |<psi_0|psi_phi>|^2 for sqrt(p)|0> + e^{i phi} sqrt(1-p)|1>
        return abs(p + (1.0 - p) * np.exp(1j * phi)) ** 2
    def fq(p): return 4.0 * p * (1.0 - p)                            # pure-qubit QFI, generator sigma_z/2: 4 Var G = 1 - <sigma_z>^2
    def fringe(p, phi, chi=0.0):                                     # P(+) of a readout along cos(chi) x + sin(chi) y after the phase
        return 0.5 * (1.0 + 2.0 * math.sqrt(p * (1.0 - p)) * math.cos(phi - chi))
    def f_cl(p, phi, chi=0.0):                                       # classical Fisher information of that readout
        P = fringe(p, phi, chi); dP = -math.sqrt(p * (1.0 - p)) * math.sin(phi - chi)
        return dP * dP / (P * (1.0 - P)) if 0.0 < P < 1.0 else 0.0
    phis = np.linspace(0.0, 2.0 * math.pi, 200001)
    res = {}
    for p in (0.5, 1.0 / 3.0):
        # reading (i) of A3, the rotor: the phase orbit closes at 2 pi, the half-turn is phi = pi
        ov_half = overlap_sq(p, math.pi)
        # reading (ii), the antipode: the first orthogonal state on the orbit, if any
        ov = overlap_sq(p, phis); i_min = int(np.argmin(ov)); ov_min = float(ov[i_min]); phi_min = float(phis[i_min])
        # the null: the fringe extremum of the standard readout (chi = 0), a peak cut on the Ramsey signal
        fr = np.asarray([fringe(p, ph) for ph in phis]); i_ext = int(np.argmin(fr)); phi_ext = float(phis[i_ext])
        ov_ext = overlap_sq(p, phi_ext)
        # a rotated readout (chi = pi/2) moves the fringe extremum; the half-turn does not move
        fr2 = np.asarray([fringe(p, ph, math.pi / 2.0) for ph in phis]); phi_ext2 = float(phis[int(np.argmin(fr2))])
        ov_ext2 = overlap_sq(p, phi_ext2)
        # arc and chord of the half-turn on the projective carrier (source convention: orthogonal states at pi/2)
        arc_half = 0.5 * math.sqrt(fq(p)) * math.pi                  # ds = (1/2) sqrt(F_Q) dphi along the orbit
        chord_half = math.acos(math.sqrt(ov_half))
        res[p] = dict(fq=fq(p), ov_half=ov_half, one_minus=1.0 - ov_half, ov_min=ov_min, phi_min=phi_min, phi_ext=phi_ext,
                      null=1.0 - ov_ext, phi_ext2=phi_ext2, null2=1.0 - ov_ext2, arc=arc_half, chord=chord_half, S=arc_half - chord_half,
                      fcl_q=f_cl(p, math.pi / 2.0), fcl_half=f_cl(p, math.pi))
    pg = np.linspace(0.0, 1.0, 100001)
    max_dev = float(np.max(np.abs(fq(pg) - (1.0 - overlap_sq(pg, math.pi)))))     # the identity over the whole family
    p_opt = float(pg[int(np.argmax(fq(pg)))])
    # the source's parenthesis: 'the balanced probe (the state at the A3-antipode of |0>)' on the preparation meridian
    fq_pole_antipode = fq(0.0)                                       # the meridian's half-turn from |0> is |1> (p = 0)
    arc_pole_to_bal = math.acos(math.sqrt(0.5)); arc_pole_to_pole = math.acos(0.0)   # Fubini-Study arcs |0> -> balanced, |0> -> |1>
    q = res[1.0 / 3.0]; h = res[0.5]
    crr, null, dom = q["one_minus"], q["null"], q["fq"]
    check = max_dev < 1e-12 and rel(p_opt, 0.5) <= 1e-3 and h["ov_min"] < 1e-9
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("qm",
        "N independent Ramsey probes sqrt(p)|0> + e^{i phi} sqrt(1-p)|1> of a phase phi (generator sigma_z/2); quantum Fisher information per probe F_Q = 4p(1-p), unit under A1' = 1/sqrt(N F_Q); the phase orbit as the rotor (A3), Fubini-Study carrier with orthogonal states at pi/2 (the source rows' convention)",
        source="runs/phaseA/crr_retrodictions.txt [d5] (CONSIST)",
        Q="the quantum Fisher information of a pure Ramsey probe is one minus its squared overlap with its own A3 half-turn image, F_Q = 1 - |<psi_0|psi_pi>|^2, so the optimal probe (F_Q = 1) is the one probe whose half-turn image is its antipode (orthogonal): the balanced probe, which is the midpoint of the meridian from |0> to its antipode |1>, not the antipode of |0>",
        ingredient="A3 (the cut at half a turn of the intrinsic phase phi; the rotor and antipode readings of synthesis.py row 4 compared on this carrier), D5",
        null="the fringe extremum of the standard Ramsey readout (a peak cut on the signal P(phi) = (1 + 2 sqrt(p(1-p)) cos phi)/2): one minus the squared overlap at that extremum",
        domain="Braunstein-Caves 1994: for a pure state F_Q = 4 Var(G); for a qubit with G = sigma_z/2 this is 1 - <sigma_z>^2 = 4p(1-p), maximal on the equator",
        numbers=(f"p = 1/3 (the source's off-balance probe): 1 - |<psi_0|psi_pi>|^2 = {crr:.6f}, F_Q = 4p(1-p) = {dom:.6f}; fringe extremum at phi = {q['phi_ext']:.4f} (half-turn pi = {math.pi:.4f}), 1 - overlap^2 there = {null:.6f}; "
                 f"readout rotated by pi/2: extremum at phi = {q['phi_ext2']:.4f}, 1 - overlap^2 there = {q['null2']:.6f}; minimum squared overlap on the orbit {q['ov_min']:.6f} at phi = {q['phi_min']:.4f} (no antipode: the orbit never reaches an orthogonal state); "
                 f"half-turn arc {q['arc']:.4f}, chord {q['chord']:.4f}, surplus S = {q['S']:.4f}; classical Fisher information of the standard readout: {q['fcl_q']:.6f} at the quarter-turn phi = pi/2 (= F_Q), {q['fcl_half']:.6f} at the half-turn; "
                 f"p = 1/2: 1 - overlap^2 at the half-turn = {h['one_minus']:.6f} = F_Q {h['fq']:.6f}, minimum squared overlap {h['ov_min']:.2e} at phi = {h['phi_min']:.4f} (the half-turn image is the antipode), arc {h['arc']:.4f} = chord {h['chord']:.4f}, S = {h['S']:.1e}; "
                 f"identity F_Q = 1 - overlap^2 over p in [0, 1]: max deviation {max_dev:.1e}; argmax F_Q at p = {p_opt:.4f}; the source's parenthesis: the A3 half-turn of the preparation meridian from |0> is |1>, F_Q(|1>) = {fq_pole_antipode:.4f}; "
                 f"Fubini-Study arc |0> -> balanced probe {arc_pole_to_bal:.4f} = {arc_pole_to_bal / arc_pole_to_pole:.2f} x the arc |0> -> |1> ({arc_pole_to_pole:.4f})"),
        tg=f"1 - overlap^2 at the A3 half-turn {crr:.6f} vs null at the fringe extremum {null:.6f}: {_word(tg_ok, 'agree', 'differ')} (the half-turn of the phase orbit is the fringe minimum of the aligned readout)",
        tn=f"the pure-qubit QFI 4p(1-p) = {dom:.6f}: the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"identity within 1e-12 over the family, optimum at p = 1/2, and the balanced probe's half-turn image orthogonal: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the half-turn of the Ramsey phase is where the aligned readout's fringe turns, so the cut and the peak cut {_word(tg_ok, 'coincide', 'do not coincide')} (a symmetric orbit: CRR.md's own 'nothing to test'), and the identity itself {_word(tn_ok, 'is', 'is not')} the domain's F_Q = 1 - <sigma_z>^2; "
                 f"what the row adds to the wave-1 reading of A3 is a placement: the metrologist's optimal probe is exactly the one state on which A3's rotor reading (phi = pi) and antipode reading (orthogonality) agree (p = 1/2: squared overlap {h['ov_min']:.1e}, S = {h['S']:.1e}), every other probe leaving A3 INTERNAL on this carrier (p = 1/3: minimum squared overlap {q['ov_min']:.4f}, S = {q['S']:.4f}); "
                 f"the source row's parenthesis 'the balanced probe (the state at the A3-antipode of |0>)' does not survive the axiom's text: the half-turn of the meridian from |0> is |1>, where F_Q = {fq_pole_antipode:.1f}, and the balanced probe is the meridian's quarter-turn"),
        weakness=(f"the identity is the two-level one (4 Var G = 1 - <sigma_z>^2 needs a spectrum of two points), so the source's 'no clause reaches entangled probes' stands; the null moves with the readout basis (rotated by pi/2 it gives {q['null2']:.4f}, not {crr:.4f}), so T-G's agreement is for the aligned readout only, "
                  "and a basis-free null (the orbit's own geometry) would be D3, information geometry's"),
        elegance="The best way to sense a turn is to stand halfway between a point and its opposite, not at the opposite: from the midpoint every small turn shows, from the far point nothing does.",
        child="Imagine a friend on the other side of a merry-go-round: if you sit right across from them, a tiny turn hardly changes how they look to you. If you sit a quarter of the way round, every little turn shows. The best seat for noticing turns is a quarter of the way round, not the far side.")


# ---------------------------------------------------------------- 32 [e1] the Hopf normal form under slow modulation: H-L5's class boundary
def r2():
    mu_bar, a, eps, dt = 0.25, 0.4, 0.02, 0.02
    T_tr = 200.0; n_mod = 2; T = T_tr + n_mod * 2.0 * math.pi / eps; n = int(round(T / dt))
    bs = (0.0, 2.0, 4.0, 6.0, 8.0)
    def run(b):
        z = 0.1 + 0j; zs = np.empty(n + 1, complex); zs[0] = z
        def f(z, t):
            mu = mu_bar * (1.0 + a * math.sin(eps * t)); return (mu + 1j) * z + (-1.0 + 1j * b) * abs(z) ** 2 * z
        for i in range(n):                                           # fixed-grid RK4
            t = i * dt; k1 = f(z, t); k2 = f(z + 0.5 * dt * k1, t + 0.5 * dt); k3 = f(z + 0.5 * dt * k2, t + 0.5 * dt); k4 = f(z + dt * k3, t + dt)
            z = z + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0; zs[i + 1] = z
        return zs[int(T_tr / dt):]
    res = {}
    for b in bs:
        zs = run(b); x, y = zs.real, zs.imag
        cuts = antipodal_cuts(intrinsic_phase(x))
        C, Tk, A, Tq, Cq = [], [], [], [], []
        for p, q in zip(cuts[:-1], cuts[1:]):
            seg = np.column_stack([x[p:q + 1], y[p:q + 1]])
            C.append(arc_length(seg)); Tk.append((q - p) * dt); A.append(np.ptp(x[p:q + 1]))
            mu_k = mu_bar * (1.0 + a * math.sin(eps * (T_tr + 0.5 * (p + q) * dt)))         # the domain's relations at the occasion's midpoint
            Tq.append(math.pi / (1.0 + b * mu_k)); Cq.append(math.pi * math.sqrt(mu_k))
        C, Tk, A, Tq, Cq = map(np.asarray, (C, Tk, A, Tq, Cq))
        res[b] = dict(n=len(C), cvC=cv(C), cvA=cv(A), cvT=cv(Tk), index=cv(Tk) / cv(C), index_amp=cv(Tk) / cv(A),
                      pred=2.0 * b * mu_bar / (1.0 + b * mu_bar), index_qs=(cv(Tq) / cv(Cq)) if b > 0 else float(cv(Tq)),
                      meanT=float(Tk.mean()), T_qs=math.pi / (1.0 + b * mu_bar))
    def crossing(key):
        idx = np.asarray([res[b][key] for b in bs]); bb = np.asarray(bs); k = int(np.argmax(idx >= 1.0))
        return float(bb[k - 1] + (1.0 - idx[k - 1]) * (bb[k] - bb[k - 1]) / (idx[k] - idx[k - 1])) if k > 0 else float("nan")
    b_cross, b_cross_qs = crossing("index"), crossing("index_qs")
    b_star = 1.0 / mu_bar
    r4 = res[4.0]
    crr, null, dom = r4["index"], r4["index_amp"], r4["index_qs"]
    out = outcome(crr=crr, null=null, domain=dom, check=None)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("bif",
        f"Hopf normal form with shear (nonisochronicity) b, zdot = (mu(t) + i) z + (-1 + i b) |z|^2 z, cycle radius sqrt(mu), phase speed 1 + b mu, amplitude relaxation rate 2 mu; mu(t) = {mu_bar:g} (1 + {a:g} sin({eps:g} t)) modulated slowly against the relaxation (2 mu >= {2 * mu_bar * (1 - a):g}); fixed-grid RK4, dt = {dt:g}, {n_mod} modulation periods after a transient of {T_tr:g}; occasion = A3 half-turn of the intrinsic phase of x, arc in the (x, y) plane",
        source="runs/phaseA/crr_retrodictions.txt [e1] (CONSIST)",
        Q="under slow modulation of mu the Hopf oscillator is clock-regular (H-L5 fails) for shear b mu < 1 and arc-regular (H-L5 holds) for b mu > 1: the class index CV(clock)/CV(arc) is the period's elasticity to the amplitude, 2 b mu/(1 + b mu), and the isochronous normal form (b = 0), the source row's, is the clock-regular limit in which natural time is the clock over pi",
        ingredient="H-L5 (the class claim between own occasions), A3/D5 (occasion = half-turn of the intrinsic phase), A1'/D5 natural time (occasion count); D2 with the identity metric of the (x, y) plane (not proper)",
        null="control (i) of H-L5: the peak-to-trough amplitude of x over the occasion, which on a near-circular orbit is the arc over pi/2",
        domain="the normal form's own relations: r = sqrt(mu) and theta-dot = 1 + b r^2, so the quasi-static half-period is pi/(1 + b mu(t)) and the quasi-static arc pi sqrt(mu(t)), evaluated at the occasions; to first order in the modulation their CV ratio is the elasticity 2 b mu/(1 + b mu), which is 1 at b mu = 1",
        numbers="; ".join(f"b = {b:g}: {r['n']} occasions, CV(arc) = {r['cvC']:.4f}, CV(amplitude) = {r['cvA']:.4f}, CV(clock) = {r['cvT']:.4f}, index CV(clock)/CV(arc) = {r['index']:.4f} (quasi-static relations at the occasions: {r['index_qs']:.4f}; first-order elasticity 2 b mu/(1 + b mu) = {r['pred']:.4f}), mean half-turn {r['meanT']:.4f} (pi/(1 + b mu) = {r['T_qs']:.4f})" for b, r in res.items())
                + f"; index crosses 1 at b = {b_cross:.2f} (b mu = {b_cross * mu_bar:.2f}); the quasi-static index crosses at b = {b_cross_qs:.2f} (b mu = {b_cross_qs * mu_bar:.2f}); the first-order elasticity's root b* = 1/mu = {b_star:g}; b = 0 quasi-static CV(clock) = {res[0.0]['index_qs']:.4f} (isochronous: no clock content)",
        tg=f"index with the arc {crr:.4f} vs null with the amplitude control {null:.4f} (b = 4): {_word(tg_ok, 'agree', 'differ')}",
        tn=f"the normal form's relations evaluated at the occasions give {dom:.4f} at b = 4 (first-order elasticity {r4['pred']:.4f}): the domain {_word(tn_ok, 'has', 'does not have')} the index",
        tc="not reached: the crossover in Q is the root of the domain's elasticity, printed above",
        out=out,
        reading=(f"the source row's two clauses are not in CRR.md v3.1: there is no criticality clause (D1 says rho is measured, never predicted) and 'D8' is v3.1's O1, which declines any retention law until one is derived for an oscillatory state model, so the D8 route (v ~ sqrt(k) -> K ~ v -> d -> infinity) has no clause to stand on and the relaxation rate 2 mu is normal-form mathematics, as the source said; "
                 f"what survives for a proper ingredient is the class claim, and on the isochronous form every natural-time quantity is the clock over pi (b = 0: CV(clock) = {res[0.0]['cvT']:.4f}, index {res[0.0]['index']:.4f}), so shear is what gives natural time and clock different content; "
                 f"there the arc is the amplitude (T-G {_word(tg_ok, 'agree', 'differ')}) and the class index {_word(tn_ok, 'is', 'is not within TOL_N of')} the domain's period-amplitude relation, whose first-order root is b mu = 1 (measured crossing b mu = {b_cross * mu_bar:.2f}, the exact quasi-static relation's {b_cross_qs * mu_bar:.2f}): the pendulum's criterion of batch 03 row 4 (d ln T/d ln A = 1) restated on the Hopf carrier, with the normal form's shear as the knob that switches the class"),
        weakness=(f"one modulation depth and one rate; at b = 4 the measured index {crr:.4f} sits {100 * (crr - 1.0):.1f} % above the first-order elasticity's 1.0000, the second-order effect of a {100 * a:.0f} % modulation that the exact quasi-static relations recover ({dom:.4f}); "
                  "the source's shear probe mu (x^2 - y^2) breaks the orbit's shape, not its isochrony, which is why it left the source's numbers unchanged; the unit is the plane's, not the system's (A1' would need a noisy carrier, batch 04 row 5)"))


# ---------------------------------------------------------------- 33 [e2] driven damped Duffing: the antipode under three named intrinsic phases
def r3():
    delta, F, om, dt = 0.5, 1.0, 1.0, 0.005
    T_tr, T_end = 100.0, 400.0; T = 2.0 * math.pi / om
    def run(alpha):
        n = int(round(T_end / dt)); x = 0.0; v = 0.0; xs = np.empty(n + 1); vs = np.empty(n + 1); xs[0] = x; vs[0] = v
        def f(x, v, t): return v, F * math.cos(om * t) - delta * v - x - alpha * x * x - x ** 3
        for i in range(n):                                           # fixed-grid RK4
            t = i * dt
            k1x, k1v = f(x, v, t); k2x, k2v = f(x + 0.5 * dt * k1x, v + 0.5 * dt * k1v, t + 0.5 * dt)
            k3x, k3v = f(x + 0.5 * dt * k2x, v + 0.5 * dt * k2v, t + 0.5 * dt); k4x, k4v = f(x + dt * k3x, v + dt * k3v, t + dt)
            x = x + dt * (k1x + 2 * k2x + 2 * k3x + k4x) / 6.0; v = v + dt * (k1v + 2 * k2v + 2 * k3v + k4v) / 6.0; xs[i + 1] = x; vs[i + 1] = v
        i_tr = int(T_tr / dt); return xs[i_tr:], vs[i_tr:]
    def advance(ph, i0, target):                                     # sub-sample index at which ph - ph[i0] first reaches target
        adv = ph[i0:] - ph[i0]; j = int(np.argmax(adv >= target)); p0, p1 = adv[j - 1], adv[j]
        return j - 1 + (target - p0) / (p1 - p0)
    res = {}
    for alpha in (0.0, 0.5):
        x, v = run(alpha); ts = np.arange(len(x)) * dt; xm = x - x.mean()
        cross = np.where(np.diff(np.sign(xm)) > 0)[0]; T_meas = float(np.median(np.diff(ts[cross])))
        ph_as = intrinsic_phase(x)                                   # (i) the analytic-signal phase, the instrument's and the source's
        ph_pp = np.unwrap(np.arctan2(-v, xm))                        # (ii) the phase-plane angle of (x - mean, v): the oscillator's own plane
        ph_pp2 = np.unwrap(np.arctan2(-v / 2.0, xm))                 # the same with the velocity rescaled (the plane needs a scale)
        span = int(1.3 * T / dt)
        loc = np.where((xm[1:-1] > xm[:-2]) & (xm[1:-1] >= xm[2:]) & (xm[1:-1] > 0.5 * xm.max()))[0] + 1
        loc = loc[(loc > span) & (loc + span < len(xm) - 1)]
        f_as, f_pp, f_pp2, f_min = [], [], [], []
        for i0 in loc:                                               # anchor at every maximum, as the source did
            f_as.append(advance(ph_as, i0, math.pi) * dt / T); f_pp.append(advance(ph_pp, i0, math.pi) * dt / T)
            f_pp2.append(advance(ph_pp2, i0, math.pi) * dt / T); f_min.append(int(np.argmin(xm[i0:i0 + span])) * dt / T)
        f_as, f_pp, f_pp2, f_min = map(np.asarray, (f_as, f_pp, f_pp2, f_min))
        f_dr = 0.5                                                   # (iii) the drive's phase (the Poincare phase of a period-1 response): half a period
        skew = float(abs(np.mean(x ** 3)) / np.mean(x ** 2) ** 1.5); dc = float(x.mean())
        res[alpha] = dict(n=len(loc), T_meas=T_meas, as_=float(f_as.mean()), as_sd=float(f_as.std()), pp=float(f_pp.mean()), pp_sd=float(f_pp.std()),
                          pp2=float(f_pp2.mean()), mn=float(f_min.mean()), mn_sd=float(f_min.std()), dr=f_dr, skew=skew, dc=dc,
                          off_as=float(f_as.mean() - f_min.mean()), off_pp=float(f_pp.mean() - f_min.mean()), off_dr=float(f_dr - f_min.mean()),
                          pp_vs_min_max=float(np.max(np.abs(f_pp - f_min))))
    s, z = res[0.5], res[0.0]
    offs = (s["off_as"], s["off_pp"], s["off_dr"])
    max_rel = max(rel(u, w) for u in offs for w in offs)
    spread = max(offs) - min(offs); split_as = abs(s["off_as"])
    internal = max_rel > TOL_G
    all_zero = max(abs(z["off_as"]), abs(z["off_pp"]), abs(z["off_dr"]))
    out = outcome(internal=internal)
    return make_row("osc",
        f"Driven damped Duffing oscillator x'' + {delta:g} x' + x + alpha x^2 + x^3 = {F:g} cos({om:g} t), alpha in (0, 1/2), from rest; fixed-grid RK4, dt = {dt:g}, window t in [{T_tr:g}, {T_end:g}]; period-1 response (median zero-crossing interval {s['T_meas']:.4f} vs drive period {T:.4f})",
        source="runs/phaseA/crr_retrodictions.txt [e2] (DESCR)",
        Q="on the asymmetric member (alpha = 1/2), where the source row says A3 becomes testable, the A3 antipode of a maximum is one point of the cycle (attempted; the named intrinsic phases must agree for Q to have a value)",
        ingredient="A3 in three readings of 'intrinsic phase' on the same trace: (i) the analytic-signal phase (the instrument's intrinsic_phase, the source's choice); (ii) the phase-plane angle of (x - mean, x') (the oscillator's own plane, CRR.md's named alternative of a section phase); (iii) the drive's phase (the Poincare phase of a period-1 forced response); with H-CUT's antipode-not-extremum reading",
        null="the opposite extremum (the minimum after the maximum): the peak cut that A3 is set against",
        domain=None,
        numbers=(f"alpha = 0 ({z['n']} cycles, skew {z['skew']:.4f}, dc {z['dc']:.4f}): antipode at {z['as_']:.4f} +/- {z['as_sd']:.4f} (i), {z['pp']:.4f} +/- {z['pp_sd']:.4f} (ii), {z['dr']:.4f} (iii) cycles after the maximum; minimum at {z['mn']:.4f} +/- {z['mn_sd']:.4f}; largest offset from the minimum {all_zero:.4f}; "
                 f"alpha = 1/2 ({s['n']} cycles, skew {s['skew']:.4f}, dc {s['dc']:.4f}): antipode at {s['as_']:.4f} +/- {s['as_sd']:.4f} (i), {s['pp']:.4f} +/- {s['pp_sd']:.4f} (ii), {s['dr']:.4f} (iii); minimum at {s['mn']:.4f} +/- {s['mn_sd']:.4f}; "
                 f"offsets from the minimum: (i) {_sz(s['off_as'])}, (ii) {_sz(s['off_pp'])}, (iii) {_sz(s['off_dr'])} cycles; reading (ii) with the velocity rescaled by 1/2: {s['pp2']:.4f} (unchanged: the half-turn of the plane angle from a point with x' = 0 is the next point with x' = 0 on the other side of the mean, whatever the scale; largest per-cycle |(ii) - minimum| = {s['pp_vs_min_max']:.1e}); "
                 f"largest relative disagreement among the three offsets {max_rel:.2f} (TOL_G {TOL_G:g}); spread of the three offsets {spread:.4f} cycles against the analytic-signal split {split_as:.4f}"),
        tg=f"offset of the antipode from the extremum, alpha = 1/2: (i) {_sz(s['off_as'])} vs (ii) {_sz(s['off_pp'])} vs (iii) {_sz(s['off_dr'])} cycles: {_word(internal, 'differ', 'agree')} (the ingredient has three values on the domain); alpha = 0: all three within {all_zero:.4f} of the extremum",
        tn="none cited: no domain law locates an oscillator's cut (the source's own known-physics line); H-CUT needs the system's own events and a forced oscillator has none",
        tc="not reached: the readings of the ingredient must agree before Q can be checked",
        out=out,
        reading=(f"the split the source row found is a property of the analytic-signal phase, not of the waveform: under the oscillator's own phase (the plane angle) the half-turn from a maximum is the next minimum identically, because the angle of (x - mean, x') passes 0 and pi only where x' = 0, so on that reading A3 is the peak cut for every 1-D trace and H-CUT is empty; "
                 f"under the drive's phase the antipode is half a period exactly, {_sz(s['off_dr'])} cycles from the minimum; under the analytic signal it is {_sz(s['off_as'])}; three readings, three offsets, and their spread ({spread:.4f} cycles) {_word(spread > split_as, 'exceeds', 'does not exceed')} the split the source reported on ({split_as:.4f}), so on the one carrier class where A3 is said to become testable the axiom is not yet one rule (the wave-1 INTERNAL of A3 on projective carriers, here on a classical one); "
                 f"on the reversible member (alpha = 0) all three coincide within {all_zero:.4f} of the extremum, the source's time-reversal reading"),
        weakness="the plane-angle reading needs the mean of x removed (a detrender) and, for the sub-sample phase, a velocity scale that the half-turn happens not to depend on; the drive phase is the driver's clock, admissible as a Poincare phase only while the response is period-1 (locked); one drive amplitude, one damping, two alpha",
        elegance="Half a turn depends on what you call a turn: on a lopsided wave three reasonable clocks put 'halfway round' at three different places, so a rule about the halfway point must first say which clock it uses.",
        child="If a race track is a perfect circle, everyone agrees where halfway is. On a lopsided track, halfway by distance, halfway by time and halfway by the number of bends are three different spots. Before you can check a rule about the halfway point you have to say which halfway you mean.")


# ---------------------------------------------------------------- 34 [e4] the ideal LC tank: every proper quantity against its null
def r4():
    N, n_per = 400, 40
    k = np.arange(N * n_per + 1); x = np.sin(2.0 * math.pi * k / N); y = np.cos(2.0 * math.pi * k / N)   # charge and current, commensurate grid
    ph = intrinsic_phase(x)
    pk = peak_cuts(x, prominence=0.5, distance=N // 4)
    cuts_zero = antipodal_cuts(ph, start=0)[2:-2]                    # cut sequence started at sample 0 (a zero crossing)
    cuts_max = antipodal_cuts(ph, start=int(pk[0]))[2:-2]            # started at the first maximum
    off_zero = np.asarray([int(np.min(np.abs(pk - c))) for c in cuts_zero]); off_max = np.asarray([int(np.min(np.abs(pk - c))) for c in cuts_max])
    pk_in = pk[(pk >= cuts_max[0]) & (pk <= cuts_max[-1])]
    same = len(pk_in) == len(cuts_max) and bool(np.all(pk_in == cuts_max))
    def occ(cuts):
        C, Tk, A, Cs = [], [], [], []
        for p, q in zip(cuts[:-1], cuts[1:]):
            seg = np.column_stack([x[p:q + 1], y[p:q + 1]]); C.append(arc_length(seg)); Cs.append(chord(seg)); Tk.append(q - p); A.append(np.ptp(x[p:q + 1]))
        return tuple(map(np.asarray, (C, Cs, Tk, A)))
    C, Cs, Tk, A = occ(cuts_max); Cp, _, _, _ = occ(pk_in)
    S = C - Cs
    try:
        sig = unit_sigma(A); unit_msg = f"sigma = {sig:.3e}"
    except ValueError as e:
        sig = None; unit_msg = f"rejected ('{e}')"
    crr, null, dom = float(C.mean()), float(Cp.mean()), math.pi
    check = same and float(np.max(off_max)) == 0.0 and cv(C) < 1e-9 and cv(Tk) < 1e-9 and cv(A) < 1e-9 and sig is None
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("osc",
        f"Ideal LC tank: charge sin(2 pi t/T) and current cos(2 pi t/T) on the (q, i) circle, {N} samples per period, {n_per} periods, interior occasions scored (edge cuts dropped)",
        source="runs/phaseA/crr_retrodictions.txt [e4] (DESCR)",
        Q="on the ideal tank every CRR-proper quantity is its own null: the antipodal cut sequence started at an extremum is the peak-cut sequence sample for sample, every occasion carries the same arc, clock and amplitude, and A1' assigns no unit (the residual of the occasion statistic is degenerate, the record is rejected, rho is undefined); the only thing that picks a cut is where the count starts",
        ingredient="A3/D5 (antipodal_cuts on the intrinsic phase), H-L5 (CV of arc, clock, amplitude across occasions), A1'/D1 (unit_sigma on the per-occasion amplitude, rho = extent/sigma)",
        null="the peak cut (extrema of the charge), the clock (samples per occasion), the amplitude, and the instrument's sample grid as an outside step",
        domain="the sinusoid: uniform speed on the circle, half-turn arc pi r, chord 2r; a constant statistic has no spread",
        numbers=(f"{len(cuts_max)} interior cuts started at a maximum: offset from the nearest extremum {int(off_max.min())}..{int(off_max.max())} samples, {'identical to' if same else 'different from'} the peak-cut sequence; started at a zero crossing: offset {int(off_zero.min())}..{int(off_zero.max())} samples (a quarter turn, N/4 = {N // 4}); "
                 f"per occasion: arc {crr:.6f} (CV {cv(C):.1e}; pi = {math.pi:.6f}), chord {Cs.mean():.6f} (2r = 2), surplus S = {S.mean():.6f} (pi - 2 = {math.pi - 2:.6f}: the half circle is not a geodesic of the plane), clock {Tk.mean():.1f} samples (CV {cv(Tk):.1e}), amplitude {A.mean():.6f} (CV {cv(A):.1e}); arc per peak-cut occasion {null:.6f}; "
                 f"unit_sigma on the per-occasion amplitude: {unit_msg}; rho = extent/sigma: undefined"),
        tg=f"arc per A3 occasion {crr:.6f} vs null arc per peak-cut occasion {null:.6f}: {_word(tg_ok, 'agree', 'differ')} (the two cut sequences {'coincide' if same else 'do not coincide'})",
        tn=f"the half circle's length pi = {dom:.6f}: the domain {_word(tn_ok, 'has', 'does not have')} it",
        tc=f"cuts on the extrema, all three CVs below 1e-9, unit rejected: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the source row's content is exactly this and the harness says so with numbers: on a perfectly symmetric rotor the cut is the extremum, the occasion is the amplitude is the clock, and there is no unit, so nothing CRR names has a value of its own; "
                 f"the one number that is not a coincidence, the surplus pi - 2 = {math.pi - 2:.4f} per half-turn, is information geometry's (the plane's straight line against the circle's arc) and is not zero because the plane, not the circle, was named as the carrier; "
                 f"the row is the negative control of every H in CRR.md, computed on the carrier the source chose"),
        weakness="a commensurate grid makes the statistic exactly constant; on an incommensurate grid unit_sigma would return the sampling residual, which A1' says is not the unit, and the rejection would have to come from the prereg's quantisation floor instead; the first thing that would give the tank a unit is its own thermal noise, not run here",
        elegance="On a perfectly round trip nothing marks a place: the only special point is where you started counting. A rule can only be tested on something lopsided.",
        child="Walk around a perfectly round pond and every spot looks the same, so nobody can say where the 'special' place is except the place you started. To test a rule about special places you need a pond with a bumpy edge.")


# ---------------------------------------------------------------- 35 [f2] Omori sequence: Fisher arc per aftershock in the system's own unit
def r5():
    K, c, T_end, Delta = 20000.0, 0.05, 100.0, 1.0                   # events per day at t + c = 1 day, offset, window, count-window (one day)
    rng = np.random.default_rng(35)
    def events(p):                                                   # exact inversion of the compensator: natural-time increments Exp(1)
        A = np.cumsum(rng.exponential(1.0, 400000))
        if p == 1.0:
            t = c * np.exp(A / K) - c
        else:
            base = c ** (1.0 - p) + (1.0 - p) * A / K                # for p > 1 the base turns negative past the sequence's end: those A are beyond every t
            t = base[base > 0.0] ** (1.0 / (1.0 - p)) - c
        return np.concatenate([[0.0], t[t <= T_end]])
    def lam(t, p): return K * (t + c) ** (-p)
    res = {}
    for p in (0.8, 1.0, 1.2):
        t = events(p); l = lam(t, p)
        nat = np.abs(np.diff(np.log(l)))                             # A1' natural-time reading: one event = one step, window 1/lambda; Fisher arc = |d ln lambda|
        win = 2.0 * math.sqrt(Delta) * np.abs(np.diff(np.sqrt(l)))   # the count-window reading (the measles carrier): Poisson(lambda Delta), arc = 2 sqrt(Delta) |d sqrt lambda|
        clk = np.diff(t)
        n = len(nat); q = n // 4
        res[p] = dict(n=n, nat_mean=float(nat.mean()), nat_se=float(nat.std(ddof=1) / math.sqrt(n) / nat.mean()), nat_cv=cv(nat), nat_trend=float(nat[-q:].mean() / nat[:q].mean()), nat_rho=float(spearmanr(np.arange(n), nat)[0]),
                      l5=bool(cv(nat) < cv(clk)),
                      win_mean=float(win.mean()), win_cv=cv(win), win_trend=float(win[-q:].mean() / win[:q].mean()), clk_cv=cv(clk), clk_trend=float(clk[-q:].mean() / clk[:q].mean()))
    # P5 at p = 1: retention e^{-A/rho} is a power of the current rate, R = (lambda(t)/lambda(0))^{K/rho}
    def A_of(t, p): return K * math.log((t + c) / c) if p == 1.0 else K * ((t + c) ** (1.0 - p) - c ** (1.0 - p)) / (1.0 - p)
    rho = 2.0 * K
    R1 = math.exp(-A_of(1.0, 1.0) / rho); R1_rate = (lam(1.0, 1.0) / lam(0.0, 1.0)) ** (K / rho)
    def local_exp(p, t):                                             # d ln R / d ln lambda at t
        h = 1e-6 * (t + c)
        return (math.log(math.exp(-A_of(t + h, p) / rho)) - math.log(math.exp(-A_of(t - h, p) / rho))) / (math.log(lam(t + h, p)) - math.log(lam(t - h, p)))
    ex = {p: (local_exp(p, 1.0), local_exp(p, 10.0)) for p in (0.8, 1.0, 1.2)}
    r1_ = res[1.0]
    crr, null, dom = r1_["nat_mean"], r1_["win_mean"], 1.0 / K
    check = rel(crr, dom) <= 0.05 and 0.8 <= r1_["nat_trend"] <= 1.25 and not (0.8 <= res[0.8]["nat_trend"] <= 1.25) and not (0.8 <= res[1.2]["nat_trend"] <= 1.25)
    out = outcome(crr=crr, null=null, domain=dom, check=check)
    tg_ok = rel(crr, null) <= TOL_G; tn_ok = rel(crr, dom) <= TOL_N
    return make_row("seis",
        f"Omori aftershock sequence lambda(t) = K (t + c)^-p as an inhomogeneous Poisson process (K = {K:g} per day, c = {c:g} day, window {T_end:g} days, p in (0.8, 1, 1.2); exact time-rescaling inversion, seed 35), read in the system's own unit",
        source="runs/phaseA/crr_retrodictions.txt [f2] (CONSIST)",
        Q="measured in the system's own unit (A1': one event = one step, the Fisher metric of the waiting-time family, arc = |d ln lambda|), the Omori intensity moves by a stationary Fisher arc per aftershock, i.i.d. with mean 1/K, exactly when p = 1: P5's 'power law in clock time iff p = 1' is 'constant arc per occasion iff p = 1', and the retention e^(-A/rho) is then a power of the current rate, R = (lambda(t)/lambda(0))^(K/rho)",
        ingredient="A1'/D1 (one event = one step; natural time), D5 (occasion = inter-event interval), P5 (retention in natural time), H-L5's class language (arc per occasion against clock per occasion)",
        null="the count-window reading of A1' (Poisson(lambda Delta) per clock window, Delta = one day, the measles carrier): arc per event 2 sqrt(Delta) |d sqrt lambda|",
        domain="Omori-Utsu with p = 1: K events per e-fold of (t + c), so the log-rate falls by 1/K per event; for p != 1 the events per e-fold scale as (t + c)^(1 - p); Ogata's time-rescaling: the compensator increments are i.i.d. Exp(1) for every p",
        numbers="; ".join(f"p = {p:g}: {r['n']} occasions, natural-time arc per event mean {r['nat_mean']:.7f} (1/K = {1 / K:.7f}; relative standard error of the mean {100 * r['nat_se']:.2f} %), CV {r['nat_cv']:.3f}, last-quarter/first-quarter ratio {r['nat_trend']:.3f}, Spearman with event index {r['nat_rho']:+.3f}; count-window arc per event mean {r['win_mean']:.7f}, CV {r['win_cv']:.3f}, ratio {r['win_trend']:.3f}; clock per event CV {r['clk_cv']:.3f}, ratio {r['clk_trend']:.1f}; CV(arc) < CV(clock): {r['l5']}" for p, r in res.items())
                + f"; retention at t = 1 day with rho = 2K, p = 1: e^(-A/rho) = {R1:.6f}, (lambda(1)/lambda(0))^(K/rho) = {R1_rate:.6f}; local exponent d ln R/d ln lambda at t = 1 and t = 10 days: p = 0.8: {ex[0.8][0]:.4f}, {ex[0.8][1]:.4f}; p = 1: {ex[1.0][0]:.4f}, {ex[1.0][1]:.4f}; p = 1.2: {ex[1.2][0]:.4f}, {ex[1.2][1]:.4f}",
        tg=f"natural-time arc per event {crr:.7f} vs null count-window arc per event {null:.7f} (p = 1): {_word(tg_ok, 'agree', 'differ')}; stationarity ratios {r1_['nat_trend']:.3f} vs {r1_['win_trend']:.3f}",
        tn=f"Omori-Utsu at p = 1 gives 1/K = {dom:.7f} per event (relative difference {rel(crr, dom):.2e}, standard error {r1_['nat_se']:.2e}): the domain {_word(tn_ok, 'has', 'does not have')} Q",
        tc=f"mean within 5 % of 1/K and stationary (ratio in [0.8, 1.25]) at p = 1 only: {_word(check, 'holds', 'fails')}",
        out=out,
        reading=(f"the natural-time reading of A1' does work against the window reading (T-G: the window arc per event trends as (t + c)^-1/2 even at p = 1, ratio {r1_['win_trend']:.3f}, because the reporting day sits inside its unit, the INTERNAL of batch 01 row 3), and what it produces {_word(tn_ok, 'is', 'is not within TOL_N of')} the domain's own statement: at p = 1 the aftershock count per e-fold of time is K, so each event lowers the log-rate by 1/K, an i.i.d. Exp(1)/K step by time-rescaling (CV {r1_['nat_cv']:.3f}); "
                 f"P5's consistency relation reads, in this unit, 'each aftershock erases the same share of the mainshock's memory, so the memory left is a fixed power of the present rate' (exponent {ex[1.0][0]:.4f} at 1 day and {ex[1.0][1]:.4f} at 10 days; at p = 0.8 it drifts from {ex[0.8][0]:.4f} to {ex[0.8][1]:.4f}), which is P5 rewritten, not added; "
                 f"the clock per event is trending at every p (ratio {r1_['clk_trend']:.0f} at p = 1), so H-L5's inequality {_word(all(r['l5'] for r in res.values()), 'holds at every p', 'does not hold at every p')} for the reason batch 04 row 1 gave, the time-rescaling theorem, and not as a class finding"),
        weakness=f"rho is unfixed (O1), so the exponent K/rho is a fit; 'retention' names nothing on a fault in the source row; K was raised from 200 to {K:g} per day after the first run so that the mean's standard error ({100 * r1_['nat_se']:.2f} %) sits well below TOL_N (at K = 200 it scales to {100 * r1_['nat_se'] * math.sqrt(K / 200.0):.1f} %, and a Monte Carlo mean cannot be held to a 1 % theorem at that error); one c and one window",
        elegance="Count aftershocks, not days: each one wears away the same share of the big quake's memory, and when they thin out as one over time that share-per-event turns into the slow, long fading everyone sees on the calendar.",
        child="After a big earthquake, little ones keep coming, fewer and fewer each day. If you count the little ones instead of the days, the memory of the big one fades by the same amount with every little quake. Counting that way turns a slow, dragged-out fading on the calendar into a plain steady one.")


def main():
    return run_batch("Synthesis batch 07: rows 31-35 (prompt-log entry 61)", [r1(), r2(), r3(), r4(), r5()])


if __name__ == "__main__":
    sys.exit(main())
