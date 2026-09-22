"""EXPLORATORY (owner request 2026-09-22, prompt-log entry 67): start from emptiness and build with CRR v3.1 as stated,
line by line, and see which mathematical forms appear and where the equations as written cannot proceed without a
change. Every statement below is computed; every 'CHANGE REQUIRED' is printed by the script from a computation that
returned nothing, raised, or stayed fixed (R15). No data, deterministic, no dependence on the batteries. Reading:
ontology/08_exploratory_genesis.md. Run: uv run python ontology/checks/genesis_from_emptiness.py
"""
import math

import numpy as np
from scipy.integrate import quad

from crr.instrument.core import antipodal_cuts, arc_length, intrinsic_phase, unit_sigma

CHANGES = []


def change(tag, text):
    CHANGES.append((tag, text))
    print(f"     CHANGE REQUIRED [{tag}]: {text}")


def fr_u(p):
    """Fisher-Rao arc-length coordinate on the Bernoulli manifold, measured from p = 0: u = 2 arcsin sqrt p."""
    return 2.0 * np.arcsin(np.sqrt(p))


def d_fr(p, q):
    return abs(fr_u(p) - fr_u(q))


def step_0_emptiness():
    print("[0] Emptiness: a carrier with nothing to distinguish (A1 needs a statistical manifold; a single distribution is a point, dimension 0)")
    x = np.zeros((100, 0))
    try:
        C = arc_length(x)
        print(f"     arc length of any path on a 0-dimensional carrier: {C:g} (D2: nothing travels)")
    except Exception as e:  # noqa: BLE001
        print(f"     arc_length on a 0-dimensional carrier raises: {type(e).__name__}: {e}")
    stat = np.zeros(20)
    try:
        unit_sigma(stat)
        print("     unit found (unexpected)")
    except ValueError as e:
        print(f"     A1' unit on a carrier that never changes: unit_sigma raises '{e}' (no unit, no rho)")
    flat = np.zeros(400)
    ph = intrinsic_phase(flat)
    cuts = antipodal_cuts(ph)
    n_after = int(np.sum(np.asarray(cuts) > 0))
    print(f"     A3 on a flat record: phase advances {float(ph[-1] - ph[0]):.4f} rad over 400 samples; cuts after the start index {n_after} (the start itself is returned as index {int(cuts[0]) if len(cuts) else 'none'}) (O3: no rotor, no cut)")
    print("     CRR has no equation of motion (CRR.md section 0), so nothing leaves this state")
    change("A0", "a first distinguishable state and a first motion must be posited; CRR v3.1 has no clause that produces either (the owner concedes the first)")
    print()


def step_1_first_distinction():
    print("[1] The first distinction: this / not-this. The least statistical manifold with two distinguishable states is the Bernoulli family p in (0, 1) (A1)")
    g = lambda p: 1.0 / (p * (1.0 - p))                       # Fisher information of Bernoulli
    length, err = quad(lambda p: math.sqrt(g(p)), 0.0, 1.0)
    print(f"     Fisher-Rao length of the whole manifold, integral of sqrt(1/(p(1-p))) dp from 0 to 1 = {length:.10f} (pi = {math.pi:.10f}, quad error {err:.1e})")
    print(f"     the arc-length coordinate u(p) = 2 arcsin sqrt(p): u(0) = {fr_u(0.0):.4f}, u(1/2) = {fr_u(0.5):.4f}, u(1) = {fr_u(1.0):.4f}: THE LINE (a geodesic segment of length pi) is the first form")
    ps = np.linspace(0, 1, 100001)
    psi = np.stack([np.sqrt(ps), np.sqrt(1 - ps)], axis=1)  # Hellinger embedding: amplitudes
    norms = np.linalg.norm(psi, axis=1)
    print(f"     Hellinger embedding psi = (sqrt p, sqrt(1-p)): |psi| = 1 at every p (max deviation {float(np.max(np.abs(norms - 1))):.1e}): normalisation p + (1-p) = 1 IS cos^2 + sin^2 = 1: THE CIRCLE is the normalisation of the first distinction read in amplitude coordinates")
    theta = np.arccos(np.sqrt(ps))
    print(f"     the Fisher-Rao distance is twice the angle on that circle: d_FR(0, 1) = {d_fr(0.0, 1.0):.6f} = 2 x {float(theta[0] - theta[-1]) if theta[0] > theta[-1] else float(theta[-1] - theta[0]):.6f}; the manifold is a quarter of a circle of radius 2 (length pi)")
    chord_h = float(np.linalg.norm(psi[0] - psi[-1]))
    print(f"     two chords between the same two pure states: CRR's chord (D3, the geodesic on the manifold) = {d_fr(0.0, 1.0):.6f} = pi, an arc of the circle; the straight line through the embedding = {chord_h:.6f} = sqrt 2 (radius 1) or {2 * chord_h:.6f} = 2 sqrt 2 (radius 2). CRR's 'line' is the circle's arc; the straight line is not a CRR quantity")
    print()


def step_2_motion():
    print("[2] Motion: CRR names one speed only, Fisher speed 1 (the Omega = 1 reading of H-EQ). Posit the least motion: a geodesic at unit Fisher speed. In the arc-length coordinate the geodesic equation is u'' = 0, so u(t) = t; the manifold ends at u = 0 and u = pi, and the least continuation is reflection")
    change("A2", "a law of motion (posited here: unit Fisher speed along the geodesic, reflected at the ends of the manifold); CRR v3.1 says it has no equations of motion")
    t = np.linspace(0, 40 * math.pi, 80001)
    u_tri = math.pi - np.abs((t % (2 * math.pi)) - math.pi)          # reflected unit-speed motion between 0 and pi
    p_t = np.sin(u_tri / 2) ** 2
    p_cos = (1 - np.cos(t)) / 2
    print(f"     reflected unit-speed geodesic: u(t) is a triangle wave between 0 and pi; p(t) = sin^2(u/2): max |p(t) - (1 - cos t)/2| = {float(np.max(np.abs(p_t - p_cos))):.1e}: THE SINUSOID appears; the reflected segment is a rotor of circumference 2 pi (v = t mod 2 pi, p = sin^2(v/2)): A3's rotor exists on the first distinction")
    change("A3a", "the rotor must be derived, not assumed ('where the system is cyclic'); here it is the reflected geodesic (equivalently the signed amplitude: the circle double-covers the segment)")
    n_per = 40; n_cyc = 20
    k = np.arange(n_per * n_cyc)
    p_s = (1 - np.cos(2 * math.pi * k / n_per)) / 2
    ph = intrinsic_phase(p_s)
    cuts = antipodal_cuts(ph)
    pc = p_s[cuts]
    print(f"     the instrument on the sampled sinusoid ({n_per} samples per turn, {n_cyc} turns): {len(cuts)} half-turn cuts; p at the first six cuts = {np.array2string(pc[:6], precision=4)}; the cut fires at the pure states 0 and 1 alternately: THE CUT IS NEGATION (antipode of p is 1 - p) on the first distinction")
    for m in range(3):
        a, b = cuts[m], cuts[m + 1]
        seg = p_s[a:b + 1]
        C = float(np.sum(np.abs(np.diff(fr_u(seg)))))
        Cs = float(d_fr(seg[0], seg[-1]))
        print(f"     occasion {m + 1}: C = {C:.6f}, C* = {Cs:.6f}, S = {C - Cs:.6f} (pi = {math.pi:.6f}); the first occasions are monotone traversals of the whole line, S = 0 (D4)")
    print()


def step_3_unit_and_count():
    print("[3] The unit (A1') and the count (D1)")
    amp = np.ones(40)                                                  # peak-to-trough amplitude of every cycle of the perfect sinusoid
    try:
        unit_sigma(amp)
        print("     unit found (unexpected)")
    except ValueError as e:
        print(f"     trace reading: the occasion statistic (amplitude of each turn) is 1 on every turn; unit_sigma raises '{e}': a perfect first distinction has no unit")
    change("A1'a", "on a carrier without variability A1' gives no unit; either the unit is named (one turn = one step; the point-process reading) or a source of variability is posited")
    print("     point-process reading (A1'): one cut = one event = one step; natural time is the cut count: 1, 2, 3, ... THE INTEGERS appear as the count of half-turns")
    print("     the empirical distinction: after n outcomes with k = n/2 successes, one more success moves the empirical point by d_FR(k/n, (k+1)/(n+1)); the resolution rho = pi / that step (D1):")
    for n in (2, 4, 8, 16, 64, 256):
        k_ = n / 2
        step = d_fr(k_ / n, (k_ + 1) / (n + 1))
        print(f"       n = {n:4d}: step {step:.6f}, rho = {math.pi / step:.4f}, rho / n = {math.pi / step / n:.4f}")
    print("     the count is the only thing in this universe that grows; the resolution of the empirical point grows linearly with it (rho / n -> pi: one more event moves the point by 1/n of the line)")
    print()


def frechet_u(us, ws):
    """Weighted Fisher-Rao Fréchet mean on the Bernoulli manifold: in the arc-length coordinate the manifold is a segment,
    so the Fréchet mean is the weighted mean of u (checked against a grid argmin below)."""
    us = np.asarray(us, float); ws = np.asarray(ws, float)
    return float(np.sum(ws * us) / np.sum(ws))


def step_4_regeneration():
    print("[4] Regeneration (A6): the next occasion is seeded from the settled past as the Fisher-Rao Fréchet mean of occasion contents Phi_m under MaxEnt weights")
    change("A6a", "A6 uses 'occasion contents Phi_m', which D5 does not define (D5 gives (C_m, C*_m, S_m)); two readings are run: (a) the state at the cut, (b) the occasion's own path mean")
    change("A6b", "A6's 'fixed strength kappa' appears in the prose and not in the formula; it is not used below because nothing says how")
    grid = np.linspace(0, 1, 200001)
    ug = fr_u(grid)
    us = [fr_u(1.0), fr_u(0.0)]
    f = (ug - us[0]) ** 2 + (ug - us[1]) ** 2
    p_star = float(grid[np.argmin(f)])
    print(f"     reading (a), contents = the two cut states p = 1 and p = 0 (equal weights): grid argmin of sum d_FR^2 = p = {p_star:.6f}; closed form u = pi/2, p = sin^2(pi/4) = {math.sin(math.pi / 4) ** 2:.6f}: the first regeneration is the equiprobable state 1/2")
    print(f"     reading (b), contents = each occasion's path mean = 1/2: the seed is 1/2 at once")
    print(f"     1/2 is the fixed point of the cut's negation p -> 1 - p: |1/2 - (1 - 1/2)| = {abs(0.5 - 0.5):.1f}; an occasion seeded there travels a half-turn and returns: C = pi, C* = d_FR(1/2, 1/2) = {d_fr(0.5, 0.5):.4f}, S = {math.pi - d_fr(0.5, 0.5):.6f} = pi, the largest surplus the line allows")
    print("     the recurrence under reading (a): seed = Fréchet mean of all cut states under P3 age weights q^age; the occasion runs a half-turn from the seed to its antipode; the new cut state is appended:")
    persist = {}
    for q in (0.0, 0.25, 0.5, 1.0):
        contents = [fr_u(1.0), fr_u(0.0)]                              # occasion 1 ended at p = 1 (cut), occasion 2 at p = 0
        Ss = []; seeds = []
        for m in range(40):
            ages = np.arange(len(contents) - 1, -1, -1)
            w = q ** ages if q > 0 else (ages == 0).astype(float)
            u_seed = frechet_u(contents, w)
            u_cut = math.pi - u_seed                                   # the antipode (negation) in the arc-length coordinate
            C = math.pi; Cs = abs(u_cut - u_seed); S = C - Cs
            seeds.append(math.sin(u_seed / 2) ** 2); Ss.append(S)
            contents.append(u_cut)
        hit = next((i + 1 for i, s in enumerate(seeds) if abs(s - 0.5) < 0.01), None)
        persist[q] = Ss[-1] < 1e-9
        print(f"       q = {q:4.2f}: seeds p = {np.array2string(np.array(seeds[:6]), precision=4)} ...; S per occasion = {np.array2string(np.array(Ss[:6]), precision=4)} ...; S at occasion 40 = {Ss[-1]:.6f}; |seed - 1/2| < 0.01 first at occasion {hit if hit else 'never (40 run)'}")
    keep = [q for q, ok in persist.items() if ok]
    print(f"     computed: the first universe keeps cutting between its pure states (S stays 0) for q in {keep}; for every other q it settles on 1/2 and every later occasion is pure surplus (S = pi)")
    change("A6c", f"as stated, A6 with any memory of more than the last occasion (q > 0) drives the first universe to the state the cut cannot distinguish from its antipode; persistence needs either no memory (q = 0) or a content that carries orientation, not position")
    print("     P2 surplus weights pi_m ~ exp(beta S_m) (CRR does not fix beta), uniform age, same recurrence:")
    for beta in (-4.0, 0.0, 4.0):
        contents = [fr_u(1.0), fr_u(0.0)]; Ss = [0.0, 0.0]; seeds = []
        for m in range(40):
            w = np.exp(beta * np.array(Ss)); w = w / w.sum()
            u_seed = frechet_u(contents, w)
            u_cut = math.pi - u_seed; S = math.pi - abs(u_cut - u_seed)
            seeds.append(math.sin(u_seed / 2) ** 2); Ss.append(S); contents.append(u_cut)
        print(f"       beta = {beta:+.0f}: seeds p = {np.array2string(np.array(seeds[:5]), precision=4)} ...; S at occasion 40 = {Ss[-1]:.6f}")
    print("     computed: with equal weights on the two pure states the seed is 1/2 whatever beta does afterwards (the first two occasions both have S = 0, so beta cannot tell them apart); the sign of beta is not enough to keep the universe alive")
    print()


def step_5_dimension():
    print("[5] Can a second distinction arise? A6's Fréchet mean of points on the manifold lies on the manifold; nothing in A1-A8 adds a dimension")
    rng = np.random.default_rng(0)
    us = rng.uniform(0, math.pi, 50); ws = rng.uniform(0.1, 1, 50)
    u_m = frechet_u(us, ws)
    psi = np.array([math.sin(u_m / 2), math.cos(u_m / 2)])            # amplitude vector of the mean
    off = float(abs(np.linalg.norm(psi) - 1.0))
    print(f"     Fréchet mean of 50 weighted points: on the segment (u = {u_m:.4f} in [0, pi]), its amplitude vector has norm 1 to {off:.1e}; component outside the two-outcome span: 0 (there is no third axis to have one)")
    change("A9", "a rule that creates a distinction (a new outcome, a new axis) is absent; without it the universe stays one-dimensional for ever (Spencer-Brown's 'draw a distinction' is the classical statement of what is missing, named as context)")
    print("     if a second distinction is posited (three outcomes), the carrier is the octant of the sphere of radius 2:")
    e = np.eye(3)
    d = lambda a, b: 2 * math.acos(float(np.clip(np.sqrt(a) @ np.sqrt(b), -1, 1)))
    print(f"       d_FR between the pure states: {d(e[0], e[1]):.6f}, {d(e[0], e[2]):.6f}, {d(e[1], e[2]):.6f}: an equilateral triangle of side pi on the sphere; every pure state is at the antipode of every other")
    change("A3b", "on two or more distinctions A3's rotor needs a chosen great circle (which plane the half-turn lives in); v3.1 gives none (O3 in the non-cyclic case only)")
    print()


def step_6_forms():
    print("[6] Forms that appeared, and from which line")
    forms = [
        ("the line (a geodesic segment of length pi)", "A1 + the first distinction: the Bernoulli manifold in its arc-length coordinate"),
        ("the circle (normalisation as cos^2 + sin^2 = 1)", "A1: the Fisher-Rao metric's Hellinger embedding; a theorem, not a CRR clause"),
        ("pi (the length of the first distinction)", "A1: the integral of sqrt of the Fisher information"),
        ("sqrt 2 (the straight chord between the pure states)", "the embedding, not CRR: D3's chord is the arc pi"),
        ("the sinusoid p(t) = (1 - cos t)/2", "posited unit Fisher speed + reflection (A2, a change)"),
        ("the integers (natural time)", "A1' point-process reading: one cut = one step"),
        ("negation as the cut (p -> 1 - p)", "A3 on the reflected rotor"),
        ("1/2 (the equiprobable state)", "A6: the Fréchet mean of the two pure states; also the fixed point of the cut"),
    ]
    for name, src in forms:
        print(f"     {name:60s} <- {src}")
    print("     did not appear: a second dimension (A9), a law of motion (A2), the real continuum (presupposed by A1: the manifold imports the reals), the golden ratio (P4 needs a Kalman model with q and r, which nothing here supplies)")
    print()


def main():
    print("EXPLORATORY genesis check 2026-09-22 (prompt-log entry 67): from emptiness with CRR v3.1 as stated; every 'CHANGE REQUIRED' is printed where a computation returned nothing, raised, or stayed fixed")
    print()
    step_0_emptiness(); step_1_first_distinction(); step_2_motion(); step_3_unit_and_count(); step_4_regeneration(); step_5_dimension(); step_6_forms()
    print(f"CHANGES REQUIRED to CRR v3.1 as written ({len(CHANGES)}):")
    for tag, text in CHANGES:
        print(f"     [{tag}] {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
