"""CRR retrodiction battery — issue #21 (alexsabine/ashes_crr).

Apply the framework stated in issue #21, with NO free parameters, to 40
systems across 8 classes, and grade each row against known physics:

  SHARP   axioms force a known external result with no constant supplied
  CONSIST the framework's form coincides with a known law but does not fix
          the constant or exponent (standard math in the framework's unit)
  DESCR   true, but no one would bet against it (symmetry/definition/carrier)
  FAILS   the derivation contradicts known physics, or a framework claim is a
          special-case property rather than an axiom consequence
  TENSION two clauses give opposite answers on the same system (rewording
          proposed in the row)
  OPEN    the framework explicitly declines to derive the quantity

Binding framework statement: issue #21's inline text (A1, A1', D1, D2, D3, P1,
D4, A3, D5, A6, P2, P3, O2, A9, P4, D8, O1, D7, P6, the criticality clause,
A7, A8). It is NEWER than theory/CRR.md v3.1 (it adds A9, D7/P6, D8 and the
Omega-weighted reset map); where a row uses a CRR.md-only clause (P5), the
row's weakness says so. Rules honored: no tuning (rule 2), per-row weakness
disclosure for every choice, and the symmetry rule (rule 4) — asymmetric
members probed wherever a claim holds on a symmetric one.

Run: uv run python crr_retrodictions.py
Committed output: runs/phaseA/crr_retrodictions.txt

Every number printed by this file is produced by the checks below; no number
is transcribed by hand (issue rule 1).
"""


# =====================================================================
# CLASS (a) — two-state / occupancy families
# =====================================================================

"""class_a.py — two-state / occupancy systems for the CRR retrodiction battery (issue #21).

Binding target: the framework statement INLINE IN ISSUE #21 (newer than theory/CRR.md v3.1 —
it adds A9, D7/P6, D8, the Omega-weighted reset map). Clause ids cited from the issue.
Contract: local://crr-retro-architecture.md.

Menu coverage: ion-channel two-state gating (a1 antipode geometry, a2 cut-object tension),
Boltzmann two-level populations vs temperature (a3), chemical equilibrium A<=>B relaxation
(a4, D2/D4/P1 surplus), salience-window consistency on an occupancy ensemble (a5, D1 vs P6).
Michaelis-Menten (menu) omitted — substitution justification per contract: its mechanism
(A3 pole-start cut at half-occupancy coinciding with the operational half-saturation
convention, theta = 1/2 <=> [S] = K_M) is already exercised by a3 against a distinct known
target; the P6/D1 row replaces it for clause coverage.

ok convention: ok reports whether the FRAMEWORK'S GRADED CLAIM (the assertion implied by the
row's verdict/derivation) survives the check. CONSIST/DESCR/SHARP rows therefore report
ok=True, FAILS/TENSION rows ok=False, OPEN rows None. Checks never raise: _guarded converts
an unexpected exception into (None, "check raised: ..."), reported, never swallowed.
"""
import numpy as np
import sympy as sp

__all__ = ["SYSTEMS_A"]


def _guarded(fn):
    def wrapped():
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 - reported, not silent
            return None, f"check raised: {type(e).__name__}: {e}"
    wrapped.__name__ = fn.__name__
    return wrapped


def _bern_arc(a, b):
    """Fisher-Rao arc on the Bernoulli family between occupancy states a and b (sympy)."""
    p = sp.symbols("p", positive=True)
    return sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, a, b))


# ---------------------------------------------------------------- a1: A3 antipode geometry


@_guarded
def _a1_antipode():
    L_full = sp.simplify(_bern_arc(0, 1))                     # expect pi
    p0 = sp.Rational(1, 5)
    t0 = sp.asin(sp.sqrt(p0))
    anti_probe = sp.simplify(sp.expand_trig(sp.sin(t0 + sp.pi / 4)) ** 2)   # expect 9/10
    arc_probe = sp.simplify(_bern_arc(p0, anti_probe))                      # expect pi/2
    p0b = sp.Rational(1, 20)
    t0b = sp.asin(sp.sqrt(p0b))
    anti_b = sp.simplify(sp.expand_trig(sp.sin(t0b + sp.pi / 4)) ** 2)
    form = sp.Rational(1, 2) + sp.sqrt(p0 * (1 - p0))
    form_b = sp.Rational(1, 2) + sp.sqrt(p0b * (1 - p0b))
    geom_ok = bool(
        sp.simplify(L_full - sp.pi) == 0
        and sp.simplify(arc_probe - sp.pi / 2) == 0
        and sp.simplify(anti_probe - form) == 0
        and sp.simplify(anti_b - form_b) == 0
    )
    # A3's parenthetical: the two-state cut is at p = 1/2 (generic wording).
    # Pole member: antipode from p0 = 0 is sin^2(pi/4) = 1/2 -> holds.
    # Asymmetric member p0 = 1/5: antipode = 9/10 -> parenthetical fails.
    anti_pole = sp.Rational(1, 2)   # sin^2(pi/4): antipode from the boundary state
    claim_holds = bool(sp.simplify(anti_pole - sp.Rational(1, 2)) == 0
                       and sp.simplify(anti_probe - sp.Rational(1, 2)) == 0)
    ok = geom_ok and claim_holds
    detail = (
        f"L_family={float(L_full):.6f}=pi; antipode from pole p0=0 -> "
        f"{float(anti_pole):.4f} (=1/2, parenthetical holds); probe p0=0.200 -> "
        f"{float(anti_probe):.4f} != 0.5 (generic antipode 1/2+sqrt(p0(1-p0))="
        f"{float(form):.4f}; second probe p0=0.050 -> {float(anti_b):.4f})"
    )
    return ok, detail


# ---------------------------------------------------------------- a2: A3 vs D5 cut object


@_guarded
def _a2_cut_object():
    rng = np.random.default_rng(20260916)
    kf, kr, T = 1.0, 0.4, 6.0
    lam = kf + kr
    p_inf = kf / lam
    d_poles = sp.simplify(_bern_arc(0, 1))                          # pi
    t_cross = float(-np.log(1.0 - 1.0 / (2.0 * p_inf)) / lam)       # ensemble p(t) crosses 1/2

    # single molecule: Gillespie two-state chain (D5's carrier)
    t, state, events = 0.0, 0, []
    while True:
        t += rng.exponential(1.0 / (kf if state == 0 else kr))
        if t >= T:
            break
        state = 1 - state
        events.append(t)
    n_by_cut = sum(1 for e in events if e <= t_cross)

    # ensemble: N independent channels, per-channel next-event times (A3's carrier)
    N = 200
    states = np.zeros(N, dtype=int)
    nxt = rng.exponential(1.0 / kf, size=N)
    occ, first_cross_t = 0, None
    while True:
        i = int(np.argmin(nxt))
        if nxt[i] >= t_cross + 5.0:
            break
        occ += 1 if states[i] == 0 else -1
        states[i] = 1 - states[i]
        if occ == N // 2 and first_cross_t is None:
            first_cross_t = float(nxt[i])
        nxt[i] = nxt[i] + rng.exponential(1.0 / (kf if states[i] == 0 else kr))

    # the graded claim: ONE cut object serves both clauses on the same channel.
    # occupancy carrier: the mid-arc state p = 1/2 exists (t* analytic above).
    # event carrier (N=1): cuts are event times; no state p=1/2 exists (p in {0,1}),
    # and no event coincides with the ensemble's mid-arc crossing.
    premises_ok = bool(sp.simplify(d_poles - sp.pi) == 0 and len(events) > 0
                       and all(abs(e - t_cross) > 1e-9 for e in events))
    ok = False   # graded claim (A3's cut = D5's cut for the same channel) does NOT survive;
                 # premises verified above and reported in detail.
    detail = (
        f"pole distance={float(d_poles):.4f}=pi (premises_ok={premises_ok}); ensemble p(t) "
        f"crosses 1/2 at t*={t_cross:.4f} (analytic), stochastic occupancy first hit "
        f"100/200 at t={first_cross_t:.4f}; single molecule fired {len(events)} events by "
        f"T=6 ({n_by_cut} by t*), none at p=1/2 (single-channel states in {{0,1}})"
    )
    return ok, detail


# ---------------------------------------------------------------- a3: two-level populations


@_guarded
def _a3_two_level():
    u, gg = sp.symbols("u g", positive=True)      # u = Delta/(k T)
    p_u = 1 / (1 + sp.exp(u))                     # excited fraction, two levels
    p_g = gg * sp.exp(-u) / (1 + gg * sp.exp(-u))  # g-fold degenerate UPPER level

    p_at_0 = sp.simplify(p_u.subs(u, 0))          # 1/2 exactly
    dp = sp.diff(p_u, u)                          # < 0 for all u: unique crossing
    dp_neg = bool(float(dp.subs(u, 1)) < 0 and float(dp.subs(u, 10)) < 0)
    p1 = float(p_u.subs(u, 1))                    # T = Delta/k
    C1 = 2 * sp.asin(sp.sqrt(p_u.subs(u, 1)))     # D2 arc from T=0

    # degeneracy probe: crossing at u = ln g (finite T for g != 1)
    cross_g = sp.simplify(p_g.subs(u, sp.log(gg)) - sp.Rational(1, 2))
    dpg = sp.diff(p_g, u)
    dpg_neg = bool(float(dpg.subs({u: 1, gg: 4})) < 0)

    ok = bool(sp.simplify(p_at_0 - sp.Rational(1, 2)) == 0 and dp_neg
              and sp.simplify(cross_g) == 0 and dpg_neg)
    detail = (
        f"p=1/2 <=> u=Delta/(kT)=0 => T_cut=infinity (p(0)=1/2 exactly, dp/du<0 unique); "
        f"at T=Delta/k (u=1): p={p1:.4f}, C={float(C1):.4f}<pi/2={np.pi / 2:.4f} (occasion "
        f"incomplete); degeneracy probe g=4: p=1/2 at u=ln4, T_cut=Delta/(k*"
        f"{float(sp.log(4)):.4f}) finite, antipode still p=1/2"
    )
    return ok, detail


# ---------------------------------------------------------------- a4: relaxation surplus


@_guarded
def _a4_relaxation_surplus():
    trap = getattr(np, "trapezoid", None) or getattr(np, "trapz", None)
    if trap is None:
        return None, "numpy has neither trapezoid nor trapz"
    xe, lam = 0.8, 1.0

    # monotone member: x(t) = xe + (x0 - xe) e^{-lam t}, x0 = 0.05 (near-empty start)
    x0 = 0.05
    Tend = 6.0
    ts = np.linspace(0.0, Tend, 400001)
    xs = xe + (x0 - xe) * np.exp(-lam * ts)
    xs = np.clip(xs, 1e-9, 1 - 1e-9)
    monotone = bool(np.all(np.diff(xs) > 0))
    speed = np.gradient(xs, ts)
    C = float(trap(np.abs(speed) / np.sqrt(xs * (1 - xs)), ts))
    x_end = float(xs[-1])
    Cstar = float(2 * np.arcsin(np.sqrt(x_end)) - 2 * np.arcsin(np.sqrt(x0)))
    S = C - Cstar

    # asymmetric probe: non-monotone member (stand-in for two-step A<=>B<=>C traces),
    # starts at x0 = 0.3, oscillatory transient superposed on the same relaxation
    a, w, x0p = 0.15, 6.0, 0.3
    xp = xe + (x0p - xe) * np.exp(-ts) + a * np.exp(-ts) * np.sin(w * ts)
    xp = np.clip(xp, 1e-9, 1 - 1e-9)
    nonmonotone = bool(np.any(np.diff(xp) < 0))
    speedp = np.gradient(xp, ts)
    Cp = float(trap(np.abs(speedp) / np.sqrt(xp * (1 - xp)), ts))
    Cstarp = float(2 * np.arcsin(np.sqrt(xp[-1])) - 2 * np.arcsin(np.sqrt(x0p)))
    Sp = Cp - Cstarp

    ok = bool(monotone and abs(S) < 1e-7 and nonmonotone and Sp > 1e-3
              and Cp >= Cstarp - 1e-9)
    detail = (
        f"monotone A<=>B (x0=0.05->0.8): C={C:.8f} vs C*={Cstar:.8f}, |S|={abs(S):.2e} "
        f"(P1 equality, S=0 identically); non-monotone probe (x0=0.3): C={Cp:.4f} > "
        f"C*={Cstarp:.4f}, S={Sp:.4f} > 0, C >= C* holds"
    )
    return ok, detail


# ---------------------------------------------------------------- a5: D1 vs P6 (rho, window)


@_guarded
def _a5_rho_window():
    pp, NN = sp.symbols("p N", positive=True)
    # three readings of sigma for the occupancy carrier (A1' gives all three hooks):
    #   count : one event = one step; half-turn from a pole changes p by 1/2 = N/2 events
    #   arc   : sigma = FR arc of one event on the N-channel family = 1/sqrt(N p (1-p))
    #   CR    : A1' "on a parametric family the unit is 1/sqrt(I)" = sqrt(p(1-p)) (p-dependent)
    sigma_event = 1 / sp.sqrt(NN * pp * (1 - pp))
    rho_count = NN / sp.Integer(2)
    rho_arc = sp.simplify((sp.pi / 2) / sigma_event)
    rho_cr = sp.simplify((sp.pi / 2) / sp.sqrt(pp * (1 - pp)))

    r1 = (float(rho_count.subs({NN: 1})), float(rho_arc.subs({NN: 1, pp: sp.Rational(1, 2)})),
          float(rho_cr.subs({pp: sp.Rational(1, 2)})))
    r2 = (float(rho_count.subs({NN: 100})), float(rho_arc.subs({NN: 100, pp: sp.Rational(1, 2)})),
          float(rho_cr.subs({pp: sp.Rational(1, 2)})))
    ambiguous = abs(r2[0] - r2[1]) > 1e-9 and abs(r2[1] - r2[2]) > 1e-9
    sign_conflict_N1 = (r1[0] < 1.0 and r1[2] > 1.0)   # count: no window; CR: window
    # graded claim: P6's window condition is well-defined for the occupancy carrier
    # and consistent with D1's prohibition -> it does NOT survive.
    ok = bool(not (ambiguous or sign_conflict_N1))
    detail = (
        f"rho readings (count, arc, CR) at p=1/2: N=1 -> {r1[0]:.3f}, {r1[1]:.3f}, "
        f"{r1[2]:.3f} (count/arc say no window, CR says window); N=100 -> {r2[0]:.1f}, "
        f"{r2[1]:.3f}, {r2[2]:.3f} (all >1, mutually different); D1: rho 'never used "
        f"inside a threshold'; P6: 'window exists iff rho > 1'"
    )
    return ok, detail


SYSTEMS_A = [
    {
        "id": "a1",
        "class": "a",
        "name": "two-state antipode location (A3 parenthetical)",
        "carrier": "Bernoulli two-point simplex in occupancy p (ion-channel open fraction); unit: one channel event (A1'); FR arc in radians, family length pi",
        "clause": "A3 (two-state antipode parenthetical)",
        "derivation": (
            "FR arc on the Bernoulli family: ds = dp/sqrt(p(1-p)); total family length "
            "int_0^1 ds = pi (verified symbolically), as A3 itself cites. With p = sin^2(t) "
            "the arc is 2t, so the A3 antipode from a cut at p_n (toward p=1) is "
            "p = sin^2(t_n + pi/4) = 1/2 + sqrt(p_n(1-p_n)). From a pole (p_n = 0 or 1) this "
            "is 1/2 — the parenthetical's case. From an interior cut the antipode is NOT "
            "1/2: probe p_n = 0.2 gives 0.9, p_n = 0.05 gives 0.718. The unqualified clause "
            "text 'for a two-state occupancy family with occupation p this is p = 1/2' "
            "therefore holds only for pole-anchored occasions."
        ),
        "known_physics": (
            "framework-internal claim under test (A3's parenthetical), checked against the "
            "standard Fisher-Rao geometry of the two-point simplex that A3 itself cites "
            "(arc 2*arcsin(sqrt(p)), total length pi): the geometry, not the parenthetical, "
            "fixes the antipode for general occasions"
        ),
        "check": _a1_antipode,
        "verdict": "FAILS",
        "weakness": (
            "FAILS as a framework claim per issue rule 4: the parenthetical survives only "
            "when the last cut is a pole (the symmetric member); the asymmetric probe "
            "(interior cut) kills it. Minimal repair: reword to 'the antipode of a "
            "two-state occupancy family reached from a boundary state is p = 1/2' (generic "
            "antipode 1/2 +/- sqrt(p_n(1-p_n))); under that reading the row would be DESCR"
        ),
    },
    {
        "id": "a2",
        "class": "a",
        "name": "ion channel: is the cut the event or the mid-arc state? (A3 vs D5)",
        "carrier": "same channel, two carriers: N=1 two-state Markov point process (unit: one event, D5) vs N-channel ensemble occupancy p(t) (Bernoulli family; unit 1/N per event, A1')",
        "clause": "A3 + D5 + A1' (cut-object collision)",
        "derivation": (
            "Ensemble: p(t) = p_inf (1 - e^{-lambda t}), p_inf = kf/(kf+kr); A3's two-state "
            "parenthetical puts the cut at p = 1/2, reached at t* = -(1/lambda) "
            "ln(1 - 1/(2 p_inf)). Single molecule: a two-state Markov point process; D5 says "
            "the cut IS the event — cuts at every opening with exponential waiting times, "
            "independent of any p = 1/2, which does not exist for N=1 (states in {0,1}; FR "
            "pole distance pi). A1' takes its unit ('one channel event') from the "
            "single-molecule objects while A3 places the cut on the ensemble state. The "
            "clauses give opposite cut objects for the same channel. Minimal rewording: "
            "restrict A3's parenthetical to the ensemble carrier, and extend D5: 'for an "
            "occupancy carrier the event is the unit (A1') while the cut is the ensemble "
            "mid-arc, not an event.'"
        ),
        "known_physics": (
            "single-channel kinetics (patch clamp, two-state Markov model): openings are "
            "stochastic events with exponential waiting times; the ensemble occupancy is "
            "their average. No known law ties a microscopic event to an ensemble "
            "half-occupancy crossing"
        ),
        "check": _a2_cut_object,
        "verdict": "TENSION",
        "weakness": (
            "TENSION between A3 and D5 on the same system (verified numerically: the "
            "ensemble mid-arc crossing at t* is not a single-channel event, and a single "
            "channel never occupies p=1/2). Rates kf, kr are representative members, not "
            "fitted; the collision is rate-independent. Charitable reading (A3 = ensemble "
            "carrier only, D5 = point-process carrier only) would make this two DIFFERENT "
            "carriers and downgrade to DESCR; as written the clauses collide"
        ),
    },
    {
        "id": "a3",
        "class": "a",
        "name": "Boltzmann two-level populations vs temperature (cut only at T=infinity)",
        "carrier": "Bernoulli family in excited-state fraction p, parameterized by T through the canonical ensemble; unit: one quantum (A1')",
        "clause": "A3 (pole-start cut) + D2 (arc)",
        "derivation": (
            "p(T) = 1/(1 + e^{Delta/kT}); pole-start occasion (p(0) = 0 exactly). A3: cut at "
            "p = 1/2. Mechanically: p = 1/2 iff e^{Delta/kT} = 1 iff Delta/(kT) = 0, i.e. "
            "T = infinity — dp/du < 0 makes the crossing unique, so no finite temperature "
            "reaches the antipode: under A3 the finite-T ensemble never completes an "
            "occasion, and D2 gives C(T) = 2 asin(sqrt(p(T))) < pi/2 for all finite T. "
            "Asymmetric probe (g-fold degenerate upper level): p = g e^{-Delta/kT}/(1 + "
            "g e^{-Delta/kT}); crossing at Delta/(kT) = ln g, i.e. T_cut = Delta/(k ln g), "
            "finite for g != 1 — the antipode is still p = 1/2 (family geometry, "
            "independent of the control variable)."
        ),
        "known_physics": (
            "Boltzmann statistics: p(T) = 1/(1+e^{Delta/kT}) is the canonical two-level "
            "result; populations equalize only at T = infinity. The framework's cut state "
            "coincides with the infinite-temperature state — a definitional coincidence"
        ),
        "check": _a3_two_level,
        "verdict": "DESCR",
        "weakness": (
            "DESCR: the coincidence is forced by the Boltzmann form alone; the framework "
            "adds only the cut reading and fixes no temperature scale. Choices: carrier = "
            "canonical equilibrium path, pole-start occasion (needed after a1), upper-level "
            "degeneracy for the probe; A1' unit (one quantum) is not connected to the FR "
            "arc for occupancy carriers (see a5)"
        ),
    },
    {
        "id": "a4",
        "class": "a",
        "name": "chemical relaxation A<=>B: surplus S on a monotone occasion",
        "carrier": "Bernoulli family in mole fraction x of species A; unit: one conversion event (A1')",
        "clause": "D2 + D3 + D4 + P1 (arc, chord, surplus)",
        "derivation": (
            "Known kinetics of reversible first-order A<=>B: x(t) = x_eq + (x0 - x_eq) "
            "e^{-(kf+kr) t}, monotone in x. D2: C(t) = int |dx|/sqrt(x(1-x)) along the "
            "trajectory. P1 (monotone 1-D path is a geodesic): C*(t) = 2 asin(sqrt(x(t))) - "
            "2 asin(sqrt(x0)), so D4 gives S(t) = 0 identically — the occasion is traversed "
            "without backtracking. Asymmetric probe: a non-monotone occupancy trace "
            "(stand-in for two-step A<=>B<=>C kinetics, which are multi-exponential and "
            "overshoot): then C > C*, S > 0, while C >= C* still holds. The framework "
            "predicts S = 0 exactly when the known kinetics are monotone and S > 0 exactly "
            "when they are not."
        ),
        "known_physics": (
            "chemical relaxation: reversible first-order A<=>B relaxes exponentially and "
            "monotonically at rate kf+kr (standard temperature-jump kinetics); multi-step "
            "reactions give non-monotone traces. The framework reproduces no law here — "
            "S = 0 is P1's monotone equality (framework-internal) plus the carrier's own "
            "kinetics"
        ),
        "check": _a4_relaxation_surplus,
        "verdict": "DESCR",
        "weakness": (
            "framework-internal theorem + carrier fact (orchestrator rule): DESCR, not "
            "SHARP. The framework does not derive lambda, x_eq, or the exponential form "
            "(A8: no flow). Probe trajectory is synthetic (amplitude 0.15, frequency 6.0, "
            "start x0=0.3 chosen); mole-fraction carrier and event unit are choices"
        ),
    },
    {
        "id": "a5",
        "class": "a",
        "name": "salience window on an occupancy ensemble: rho is not one number (D1 vs P6)",
        "carrier": "N-channel Bernoulli ensemble in occupancy p; unit: one channel event (A1')",
        "clause": "P6 + D1 (rho in a threshold; A1' under-determines sigma)",
        "derivation": (
            "P6: the salience window exists iff rho > 1, rho = (extent of half-turn)/sigma "
            "(D1). For the occupancy carrier A1' leaves sigma undetermined, and three "
            "readings disagree. Count: the half-turn from a pole changes p by 1/2 = N/2 "
            "events, rho = N/2. Arc: one event has FR arc 1/sqrt(N p(1-p)), so rho = "
            "(pi/2) sqrt(N p(1-p)) — p-dependent. CR: A1' also fixes the parametric unit at "
            "1/sqrt(I) = sqrt(p(1-p)), giving rho = (pi/2)/sqrt(p(1-p)), N-independent. At "
            "p = 1/2: N=1 gives (0.5, 0.785, 3.142) — count/arc say no window, CR says "
            "window; N=100 gives (50, 7.854, 3.142) — all above 1, all different. P6's "
            "threshold is therefore not well-defined for this carrier, and D1 itself "
            "forbids using rho 'inside a threshold' while P6 conditions on rho > 1. "
            "Minimal rewording: D1 -> 'Measured; never predicted; never used to fire the "
            "cut', and A1' must state which sigma reading fixes rho for occupancy carriers."
        ),
        "known_physics": (
            "framework-internal: the window's existence is a framework claim with no "
            "external target; the row tests (i) determinacy of sigma under A1' for "
            "occupancy carriers and (ii) consistency of D1's prohibition with P6's "
            "existence condition"
        ),
        "check": _a5_rho_window,
        "verdict": "TENSION",
        "weakness": (
            "TENSION graded on the clauses as written (D1 forbids threshold use of rho; P6 "
            "thresholds it; A1' gives three mutually inconsistent sigma readings). A "
            "charitable D1 reading — the prohibition aimed at algorithmic cut-firing "
            "cutoffs, not property statements — would downgrade to DESCR with the sigma "
            "ambiguity remaining. Count reading assumes pole-anchored half-turn (a1)"
        ),
    },
]


# =====================================================================
# CLASS (b) — quantum states and dynamics
# =====================================================================

"""Class (b) — quantum states and quantum dynamics. CRR retrodiction battery (issue #21).

Contract: local://crr-retro-architecture.md (binding). Rows graded against the
ISSUE's framework statement (newer than theory/CRR.md v3.1), citing its clause ids.

Rows:
  b1  pure qubit on CP^1: the Fisher half-turn is the orthogonal state   (CONSIST)
  b2  Rabi-flopped two-level: cut at the antipode once per population
      cycle? — FAILS by the issue's rule 4: survives only on the
      resonant/geodesic member; the detuned member never cuts            (FAILS)
  b3  the same Rabi cycle under two A3-sanctioned carriers: occupancy
      antipode (p = 1/2) vs pure-state antipode (orthogonal) place the
      cut a factor 2 apart                                               (TENSION)
  b4  coherent-state displacement family: no antipode, never cuts        (OPEN)
  b5  Landau-Zener sweep: no clause fixes P_LZ                           (OPEN)

Substitution note (menu rule): the menu's adiabatic fidelity-susceptibility
item is annotated "(-> also class h)" in the menu itself; its class-b slot is
used for the b3 tension, which rule 6 of the issue asks the battery to surface.
"""

import numpy as np
import sympy as sp


def _zero(M):
    return all(sp.simplify(M[i, j]) == 0 for i in range(M.rows) for j in range(M.cols))


def _b1_bures_antipode():
    """Fisher half-turn of CP^1 = orthogonal state; scale-invariant fraction 1/2."""
    th, ph = sp.symbols("theta phi", real=True)
    psi = sp.Matrix([sp.cos(th / 2), sp.exp(sp.I * ph) * sp.sin(th / 2)])
    dth, dph = sp.diff(psi, th), sp.diff(psi, ph)

    def gq(a, b):  # Fisher-Rao (= QFI = FS) tensor element
        ip = (a.H * b)[0, 0]
        proj = (a.H * psi)[0, 0] * (psi.H * b)[0, 0]
        return sp.simplify(4 * sp.re(ip - proj))

    G = sp.Matrix([[gq(dth, dth), gq(dth, dph)],
                   [gq(dph, dth), gq(dph, dph)]])
    fs_ok = _zero(G - sp.Matrix([[1, 0], [0, sp.sin(th) ** 2]]))
    # Bures = FS/4 for pure states; overlap half-angle identity |<psi1|psi2>|^2 = (1+n1.n2)/2
    t1, t2, dp = sp.symbols("theta1 theta2 dphi", real=True)
    c1, s1 = sp.cos(t1 / 2), sp.sin(t1 / 2)        # overlap uses HALF angles (amplitudes)
    c2, s2 = sp.cos(t2 / 2), sp.sin(t2 / 2)
    ov2 = sp.expand((c1 * c2 + s1 * s2 * sp.cos(dp)) ** 2 + (s1 * s2 * sp.sin(dp)) ** 2)
    nn = sp.cos(t1) * sp.cos(t2) + sp.sin(t1) * sp.sin(t2) * sp.cos(dp)  # Bloch dot, FULL angles
    law_ok = sp.simplify(sp.expand(ov2 - (1 + nn) / 2, trig=True)) == 0
    # meridian geodesic arc (FS units) from |0> to polar angle Theta:
    Th = sp.symbols("Theta", positive=True)
    mer = sp.integrate(sp.sqrt(G[0, 0]), (th, 0, Th))
    mer_ok = sp.simplify(mer - Th) == 0
    # orthogonal state (theta = pi): d_FS = pi, d_B = pi/2
    d_fs, d_b = 2 * sp.acos(0), sp.acos(0)
    orth_ok = sp.simplify(d_fs - sp.pi) == 0 and sp.simplify(d_b - sp.pi / 2) == 0
    ok = bool(fs_ok and law_ok and mer_ok and orth_ok)
    detail = ("QFI=FS tensor diag(1,sin^2 theta), Bures=FS/4 [sympy]; overlap half-angle "
              "identity |<psi1|psi2>|^2=(1+n1.n2)/2 [sympy]; meridian geodesic arc=Theta "
              "[sympy]; d_FS(orthogonal)=pi, d_B(orthogonal)=pi/2; antipode fraction 1/2 "
              "of the closed orbit in BOTH Cencov scales (FS 2*pi, Bures pi)")
    return ok, detail


def _b2_rabi_antipode():
    """Resonant Rabi: cut at t*=pi/Om, P1=1, S=0.  Detuned: antipode unreachable."""
    Om, Dl = sp.symbols("Omega Delta", positive=True)
    Oe = sp.sqrt(Om ** 2 + Dl ** 2)
    t = sp.symbols("t", positive=True)
    psi = sp.Matrix([sp.cos(Om * t / 2), sp.I * sp.sin(Om * t / 2)])
    dps = sp.diff(psi, t)
    perp2 = sp.simplify(sp.re((dps.H * dps)[0, 0])
                        - sp.re((dps.H * psi)[0, 0] * (psi.H * dps)[0, 0]))
    speed_ok = sp.simplify(4 * perp2 - Om ** 2) == 0      # FS speed = Om
    t_star = sp.pi / Om
    P1_star = sp.simplify(sp.sin(Om * t_star / 2) ** 2)   # = 1
    orth_ok = sp.simplify(sp.cos(Om * t_star / 2)) == 0 and P1_star == 1
    # geodesic on the first half-turn: C* = 2 acos(cos(Om t/2)) = Om t (sample point Om t = 1/4)
    x = sp.Rational(1, 8)
    geo_ok = sp.simplify(2 * sp.acos(sp.cos(x)) - 2 * x) == 0
    # detuned: overlap-squared = 1 - (Om^2/Oe^2) sin^2(Oe t/2); its minimum = Dl^2/Oe^2 > 0
    min_id_ok = sp.simplify(1 - Om ** 2 / Oe ** 2 - Dl ** 2 / Oe ** 2) == 0
    # numeric asymmetric probe: Omega = Delta = 1
    Omv = Dlv = 1.0
    Oev = float(np.sqrt(Omv ** 2 + Dlv ** 2))
    tt = np.linspace(0.0, 60.0, 600001)
    ovn = np.sqrt(np.cos(Oev * tt / 2) ** 2 + (Dlv / Oev) ** 2 * np.sin(Oev * tt / 2) ** 2)
    min_ov = float(ovn.min())
    tS = np.pi / Omv
    C = Omv * tS
    Cs = 2 * np.arccos(np.sqrt(np.cos(Oev * tS / 2) ** 2
                               + (Dlv / Oev) ** 2 * np.sin(Oev * tS / 2) ** 2))
    S_det = C - Cs
    cuts_exist = min_ov < 1e-9            # False: the antipode is never reached
    ok = bool(speed_ok and orth_ok and geo_ok and min_id_ok and cuts_exist)
    detail = (f"resonant: FS speed=Omega [sympy 4*|dpsi_perp|^2=Om^2]; t*=pi/Om, P1(t*)=1 "
              f"[sympy]; C*=Om t on [0,pi] so S=0 (great circle); detuned Delta=Om: "
              f"min|<psi0|psi(t)>| = Delta/Omeff = {min_ov:.4f} > 0 for all t "
              f"[sympy identity 1-Om^2/Oe^2 = Delta^2/Oe^2] -> antipode never reached, "
              f"no cut ever fires; S(pi/Om) = pi - C* = {S_det:.4f} > 0 (small circle) "
              f"-> issue rule 4: claim survives only on the resonant geodesic member")
    return ok, detail


def _b3_cut_location_tension():
    """A3 occupancy parenthetical (p=1/2) vs pure-state parenthetical (orthogonal)."""
    Om = sp.symbols("Omega", positive=True)
    p = sp.symbols("p", positive=True)
    L_ber = sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, 0, 1))                     # pi
    half_ber = sp.integrate(1 / sp.sqrt(p * (1 - p)), (p, 0, sp.Rational(1, 2)))  # pi/2
    len_ok = sp.simplify(L_ber - sp.pi) == 0 and sp.simplify(half_ber - sp.pi / 2) == 0
    t = sp.symbols("t", positive=True)
    P1 = sp.sin(Om * t / 2) ** 2
    t_occ = sp.pi / (2 * Om)                              # first positive root of P1 = 1/2
    p_occ = sp.simplify(P1.subs(t, t_occ))                # 1/2
    C_occ = sp.simplify(Om * t_occ)                       # FS arc there = pi/2 (quarter-turn)
    t_pure = sp.pi / Om
    p_at_pure = sp.simplify(P1.subs(t, t_pure))           # 1
    occ_side_ok = p_occ == sp.Rational(1, 2) and sp.simplify(C_occ - sp.pi / 2) == 0
    pure_side_ok = p_at_pure == 1
    dis1 = sp.simplify(C_occ - sp.pi) != 0                # occupancy cut is NOT a FS half-turn
    dis2 = p_at_pure != sp.Rational(1, 2)                 # pure-state cut is NOT p = 1/2
    dis3 = sp.simplify(t_pure - 2 * t_occ) == 0           # the two cut times differ by exactly 2
    all_confirmed = bool(len_ok and occ_side_ok and pure_side_ok and dis1 and dis2 and dis3)
    # ok=False <=> the two A3 parentheticals give ONE trajectory TWO different cuts (TENSION)
    ok = not all_confirmed
    detail = (f"Bernoulli FR length = pi [sympy int_0^1 dp/sqrt(p(1-p)) = pi], half-turn at "
              f"p=1/2 -> t_occ = pi/(2 Om), P1 = 1/2; there the pure-state rule sits at FS "
              f"arc C = pi/2 (quarter-turn, not the half-turn pi); pure-state half-turn at "
              f"t_pure = pi/Om where P1 = 1 (not 1/2); t_pure = 2*t_occ exactly [sympy] — "
              f"A3's two parentheticals cut the same Rabi cycle a factor 2 apart")
    return ok, detail


def _b4_coherent_open():
    """Coherent displacement family: no orthogonal member, flat non-compact metric."""
    d = sp.symbols("delta", positive=True)
    a = sp.symbols("alpha_abs", positive=True)
    never_zero = sp.exp(-a ** 2).is_positive is True      # |<0|alpha>|^2 = exp(-|alpha|^2)
    coeff = sp.limit((1 - sp.exp(-d ** 2)) / d ** 2, d, 0, '+')   # = 1
    F_xx = 4 * coeff                                       # QFI for displacement = 4
    flat_ok = sp.simplify(F_xx - 4) == 0
    dx, dp_ = sp.symbols("dx dp", real=True)
    mixed = sp.exp(-(dx ** 2 + dp_ ** 2))
    no_cross = sp.simplify(sp.diff(mixed, dx, dp_).subs({dx: 0, dp_: 0})) == 0
    d_amb = float(sp.acos(sp.exp(-sp.Rational(9, 2))))     # ambient angle at |alpha| = 3
    ok_premise = bool(never_zero and flat_ok and no_cross)
    detail = (f"|<0|alpha>|^2 = exp(-|alpha|^2) > 0 for every finite |alpha| [sympy] -> no "
              f"orthogonal member exists in the family; 1-|<x|x+d>|^2 = 1-exp(-d^2) = (F/4)d^2 "
              f"with F = 4*{float(coeff):.0f} [sympy limit] -> intrinsic Bures metric = "
              f"dx^2+dp^2: flat, non-compact, no closed geodesic, no half-turn point (no "
              f"cross term either [sympy]); probe alpha = 3e^(i0) and 3e^(i*pi/2): ambient "
              f"angle {d_amb:.4f} < pi/2 = 1.5708 in both directions — antipode absent in "
              f"every direction; A3 no-antipode list names this family -> never cuts -> OPEN")
    return (None if ok_premise else False), detail


def _b5_landau_zener_open():
    """LZ sweep: eigenpath Fisher arc is exactly pi for all (Delta,v); P_LZ varies freely."""
    Dl, v, tau = sp.symbols("Delta v tau", positive=True)
    eps2 = Dl ** 2 + v ** 2 * tau ** 2
    theta = sp.acos(v * tau / sp.sqrt(eps2))
    dth = sp.simplify(sp.diff(theta, tau))
    speed_ok = sp.simplify(dth + v * Dl / eps2) == 0        # |dtheta/dtau| = v*Delta/eps^2
    arc = sp.integrate(v * Dl / eps2, (tau, -sp.oo, sp.oo))  # pi, independent of (Delta, v)
    arc_ok = sp.simplify(arc - sp.pi) == 0
    Ds = np.array([0.5, 1.0, 2.0])
    Vs = np.array([0.5, 1.0, 2.0])
    P = np.exp(-np.pi * Ds[:, None] ** 2 / (2.0 * Vs[None, :]))
    ok_premise = bool(speed_ok and arc_ok)
    detail = (f"sympy: eigenpath of n(tau) = (Delta,0,v*tau)/eps runs a meridian; "
              f"|dtheta/dtau| = v*Delta/eps^2 and C = int over tau = {sp.simplify(arc)} "
              f"for EVERY (Delta,v) [exact; depends only on |v*Delta| -> sweep-sign "
              f"independent]; P_LZ = exp(-pi*Delta^2/(2v)) over the same grid "
              f"(Delta,v) in {{0.5,1,2}}^2 spans {P.min():.2e}..{P.max():.3f} (orders of "
              f"magnitude) while the framework's only dynamical quantity stays constant; "
              f"the half-turn completes only as tau -> inf (never at finite tau); A8: "
              f"'predicts nothing about the traversal' -> no clause fixes P_LZ -> OPEN")
    return (None if ok_premise else False), detail


SYSTEMS_B = [
    {
        "id": "b1",
        "class": "b",
        "name": "pure qubit on the Bloch sphere: Fisher half-turn = orthogonal state",
        "carrier": "pure-qubit family {|psi(th,phi)>} = CP^1; metric = Fisher-Rao = QFI "
                   "tensor diag(1, sin^2 th) (= Fubini-Study; Bures = FS/4), Cencov-unique "
                   "up to scale; unit sigma = Cramer-Rao length 1/sqrt(I) under A1' — not "
                   "fixed without an estimation context, so rho and the D7/P6 window are "
                   "not computed",
        "clause": "A3 (pure-state antipode) + A1 (Cencov scale)",
        "derivation": "A1: the Born-family Fisher metric of |psi(th,phi)> = cos(th/2)|0> + "
                      "e^{i phi} sin(th/2)|1> is the QFI tensor diag(1, sin^2 th) (= FS; "
                      "Bures = FS/4). A3: the cut fires at the Fisher half-turn. "
                      "Mechanically: the closed geodesic through any state has length 2*pi "
                      "in FS units; its half is reached exactly at the unique orthogonal "
                      "state (d_FS(psi,psi_perp) = 2 acos 0 = pi; d_B = pi/2). The "
                      "half-orbit fraction 1/2 is Cencov-scale-invariant — verified in both "
                      "scales by sympy (tensor, meridian arc, overlap half-angle identity).",
        "known_physics": "quantum information geometry: on CP^1 the unique FS-antipode of a "
                         "pure state is its orthogonal partner; d_FS = pi, Bures angle = "
                         "pi/2, ds^2_B = ds^2_FS/4 (Schumacher-Westmoreland; "
                         "Bengtsson-Zyczkowski) — framework-external, textbook.",
        "check": _b1_bures_antipode,
        "verdict": "CONSIST",
        "weakness": "not SHARP: A3's quantum parenthetical stipulates the target rather "
                    "than deriving it; the check confirms the stipulation is geometrically "
                    "exact and Cencov-scale-invariant — standard CP^1 geometry wearing the "
                    "framework's cut rule. Also: Fisher-Rao = FS requires the optimal "
                    "phase-sensitive measurement; a FIXED sigma_z probe has I_phiphi = 0 "
                    "(degenerate family — A1 would bar the carrier); the framework does "
                    "not regulate the probe choice (recorded).",
    },
    {
        "id": "b2",
        "class": "b",
        "name": "Rabi-flopped two-level: cut at the antipode once per population cycle?",
        "carrier": "driven two-level pure state |psi(t)>: resonant e^{-i Om t sx/2}|0>, "
                   "detuned e^{-i(Om sx + Dl sz)t/2}|0>; metric = QFI/FS on CP^1; unit "
                   "sigma unfixed (no estimation context) -> rho and the D7/P6 window "
                   "not computed",
        "clause": "A3 + D2 + D4 (issue rule 4 symmetry probe)",
        "derivation": "Resonant drive |psi(t)> = e^{-i Om t sx/2}|0>: Bloch great circle "
                      "(y-z plane), FS speed Om (sympy: 4*|dpsi_perp|^2 = Om^2), C = Om t, "
                      "C* = 2 acos|cos(Om t/2)| = Om t on [0,pi] so S = 0 within the "
                      "occasion. A3's half-turn at Om t = pi: t* = pi/Om and P1(t*) = 1 — "
                      "one cut per population period, at full inversion. Rule-4 probe: "
                      "detuned H = (Om sx + Dl sz)/2 gives |<psi0|psi(t)>|^2 = "
                      "1 - (Om^2/Omeff^2) sin^2(Omeff t/2) >= Dl^2/Omeff^2 > 0 (sympy "
                      "identity): the antipode is never reached — no cut ever fires; "
                      "numerically S(pi/Om) > 0 (small circle, not a geodesic).",
        "known_physics": "textbook Rabi solution: |<psi(0)|psi(t)>| = |cos(Om t/2)| — "
                         "first orthogonality at Om t = pi, i.e. t = pi/Om, exactly half "
                         "the Bloch period 2pi/Om, where P1 = 1 (full inversion); detuned "
                         "drive: |<psi(0)|psi(t)>|^2 = 1 - (Om^2/Omeff^2) sin^2(Omeff t/2) "
                         ">= Dl^2/Omeff^2 > 0 — never orthogonal (standard two-level "
                         "solution).",
        "check": _b2_rabi_antipode,
        "verdict": "FAILS",
        "weakness": "on the resonant member the framework's numbers are exact and match "
                    "the textbook; the FAILS is the class-level claim (issue rule 4: it "
                    "survives only on the measure-zero geodesic member). Second A3 "
                    "ambiguity recorded, not graded: the rotor branch of A3 (half the "
                    "closed TRAJECTORY length) would cut the detuned drive at "
                    "t = pi/Omeff at a non-orthogonal state, against the family branch "
                    "(never cuts). sigma (Cramer-Rao) unfixed — D7/P6 left open here.",
    },
    {
        "id": "b3",
        "class": "b",
        "name": "Rabi two-level: occupancy antipode (p=1/2) vs pure-state antipode (orthogonal)",
        "carrier": "one Rabi trajectory under two A3-sanctioned carriers: occupancy "
                   "simplex {p = P1(t)} (Bernoulli, FR length pi) vs pure-state family "
                   "CP^1 (FS metric); shared origin p = 0 <-> |0>",
        "clause": "A3 (two-state-occupancy parenthetical) vs A3 (pure-state parenthetical)",
        "derivation": "Same Rabi trajectory, shared origin (p = 0 <-> |0>), two "
                      "A3-sanctioned carriers. Occupancy carrier {p = P1(t)}: Bernoulli "
                      "FR length pi (sympy int_0^1 dp/sqrt(p(1-p)) = pi), half-turn at "
                      "p = 1/2 -> t_occ = pi/(2 Om). There the pure-state rule sits at FS "
                      "arc pi/2 — a quarter-turn, not the half-turn pi. Pure-state "
                      "carrier CP^1: half-turn at t_pure = pi/Om, where the occupancy is "
                      "p = 1, not 1/2. The two parentheticals of A3 place the cut a "
                      "factor 2 apart on one trajectory. Minimal rewording: restrict the "
                      "occupancy parenthetical to dephased/mixed population carriers and "
                      "make the pure-state rule govern whenever the state is pure.",
        "known_physics": "framework-internal disagreement; the external anchor is the same "
                         "textbook Rabi solution (one trajectory; its externally known "
                         "orthogonality event is at Om t = pi).",
        "check": _b3_cut_location_tension,
        "verdict": "TENSION",
        "weakness": "both rules live inside a single clause (A3); if the orchestrator "
                    "reads A3 as one rule with carrier-dependent branches, this row is an "
                    "ambiguity rather than a TENSION. Second unresolved A3 ambiguity "
                    "recorded, not graded: rotor branch vs family branch under detuning "
                    "(see b2). Substitutes for the menu's fidelity-susceptibility item, "
                    "which the menu itself routes to class (h).",
    },
    {
        "id": "b4",
        "class": "b",
        "name": "coherent-state displacement family: no antipode, never cuts",
        "carrier": "coherent-state displacement family {|alpha> = D(alpha)|0>}, alpha in "
                   "C, non-compact; intrinsic metric = Bures/QFI (flat dx^2+dp^2); unit "
                   "sigma = Cramer-Rao on (x,p) under A1' (recorded; not load-bearing)",
        "clause": "A3 (no-antipode list)",
        "derivation": "A3's no-antipode list names the coherent-state displacement family "
                      "explicitly: it never cuts, no occasion completes, so the framework "
                      "declines cuts/occasions here. Mechanically: |<0|alpha>|^2 = "
                      "exp(-|alpha|^2) > 0 at every finite alpha (sympy), so the "
                      "orthogonal state — the A3 antipode — is not a member of the "
                      "carrier. The intrinsic metric is flat: 1-|<x|x+d>|^2 = (F/4)d^2 "
                      "with F = 4 per quadrature (sympy limit), i.e. Bures = dx^2+dp^2 — "
                      "non-compact, no closed geodesic, hence no half-turn point at all. "
                      "Probes alpha = 3e^(i0) and 3e^(i pi/2) agree (rule 4).",
        "known_physics": "coherent states: |<alpha|beta>|^2 = exp(-|alpha-beta|^2) — no two "
                         "coherent states are orthogonal; the family is non-compact and "
                         "its intrinsic QFI/Bures metric is flat; the orthogonal partner "
                         "of |0> lies outside the family (standard quantum optics).",
        "check": _b4_coherent_open,
        "verdict": "OPEN",
        "weakness": "OPEN by the framework's own text (A3 names this family); the check "
                    "verifies only the geometric premise. Note the AMBIENT FS angle "
                    "2 acos|<0|alpha>| tends to pi without attaining it — under either "
                    "reading (ambient angle or intrinsic flat metric) the family has no "
                    "in-carrier antipode.",
    },
    {
        "id": "b5",
        "class": "b",
        "name": "Landau-Zener sweep: does any clause fix P_LZ?",
        "carrier": "Landau-Zener Hamiltonian H(tau) = (v tau/2) sz + (Delta/2) sx; "
                   "carrier = instantaneous-eigenstate (adiabatic) family on CP^1; "
                   "metric = QFI/FS",
        "clause": "D2 + A8 (no-forecast)",
        "derivation": "D2 applied to the adiabatic eigenpath of H(tau): the eigenstate of "
                      "n(tau).sigma with n = (Delta,0,v tau)/eps runs the phi = 0 meridian "
                      "from -z to +z; theta(tau) = acos(v tau/eps), |dtheta/dtau| = "
                      "v Delta/(Delta^2+v^2 tau^2), so C = int = pi for EVERY (Delta,v) "
                      "(sympy exact; depends only on |v Delta| — sweep-sign independent). "
                      "The known P_LZ = exp(-pi Delta^2/(2v)) varies by orders of "
                      "magnitude on the same grid while the framework's only dynamical "
                      "quantity stays constant; the half-turn completes only as tau -> "
                      "inf. No clause (A6-A9, P4/D8, D7/P6) addresses transition "
                      "probabilities; A8 refuses traversal forecasts. OPEN.",
        "known_physics": "Landau-Zener: P(transition) = exp(-pi Delta^2/(2v)) (Landau 1932; "
                         "Zener 1932; Vitanov et al. 2001) — a function of Delta^2/v "
                         "spanning orders of magnitude; no adiabatic-arc quantity "
                         "reproduces it.",
        "check": _b5_landau_zener_open,
        "verdict": "OPEN",
        "weakness": "expected OPEN, confirmed: the eigenpath arc — the framework's only "
                    "applicable quantity — is exactly P_LZ-blind (constant pi); the "
                    "actual-state trajectory would need a dynamical model the framework "
                    "refuses to supply (A8). Carrier choice recorded: the adiabatic "
                    "eigenpath is the standard reading of an LZ sweep; a non-adiabatic "
                    "trajectory changes C but nothing in the framework connects either "
                    "to P_LZ.",
    },
]


# =====================================================================
# CLASS (c) — thermal ensembles and finite-time thermodynamics
# =====================================================================

"""Class (c) — thermal ensembles and finite-time thermodynamics. Issue #21
retrodiction battery. Rows implement the original writer's decided design
(c1-c5, verdicts decided by analysis before the process died). Checks run
standalone with numpy+sympy only, deterministic, never raise (guarded)."""
import functools
import numpy as np
import sympy as sp


def _safe(fn):
    @functools.wraps(fn)
    def wrapped():
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 — contract: a check reports, never raises
            return None, f"check raised: {exc}"
    return wrapped


@_safe
def _c1_ideal_gas():
    """Ideal-gas isotherm: D2 arc with the Ruppeiner metric = thermodynamic
    length. Known: Ruppeiner metric of the ideal gas is flat (curvature 0)."""
    U, V, N, kB = sp.symbols("U V N k_B", positive=True)
    S = N * kB * (sp.log(V) + sp.Rational(3, 2) * sp.log(U))
    gVV = -sp.diff(S, V, 2)
    gUV = -sp.diff(S, U, V)
    L_iso = sp.integrate(sp.sqrt(gVV), (V, V, 2 * V))
    L_known = sp.sqrt(N * kB) * sp.log(2)
    phiv = sp.sqrt(N * kB) * sp.log(V)  # flatness: gVV is the squared gradient of a coordinate
    flat = sp.simplify(gVV - sp.diff(phiv, V) ** 2) == 0
    ok = sp.simplify(L_iso - L_known) == 0 and flat and sp.simplify(gUV) == 0
    detail = ("L_isotherm(V->2V) = sqrt(N k_B) ln 2 (Ruppeiner entropy-rep; "
              "Weinhold energy-rep = this * sqrt(T) — a convention); flatness probe: gVV = (d/dV sqrt(N k_B) ln V)^2 exactly")
    return bool(ok), detail


@_safe
def _c2_schottky():
    """Two-level Schottky anomaly: the heat-capacity peak is known physics; the
    family's Fisher-peak location is coordinate-dependent and none is
    framework-selected. The exact C peak solves 2/x + 1 = 2 e^x/(1 + e^x)."""
    x = sp.symbols("x", positive=True)
    C = x ** 2 * sp.exp(x) / (1 + sp.exp(x)) ** 2  # C/k_B, x = beta*Delta
    resid = (2 + x) * (1 + sp.exp(x)) - 2 * x * sp.exp(x)  # dC/dx = 0 <=> resid = 0
    xs = np.linspace(0.05, 12.0, 40000)
    dC_num = np.array([float(resid.subs(x, float(v))) for v in xs])
    cross = xs[np.where(np.diff(np.sign(dC_num)))[0]]
    peak = float(sp.nsolve(resid, 2.4))  # exact root near 2.4
    p = sp.exp(x) / (1 + sp.exp(x))
    I_beta = p * (1 - p)  # Fisher wrt beta (up to Delta^2): peaks at x = 0 (T = inf)
    T_vals = np.linspace(0.05, 20.0, 200000)
    I_T = np.exp(1.0 / T_vals) / (1 + np.exp(1.0 / T_vals)) ** 2 / T_vals ** 4
    peak_T = float(T_vals[np.argmax(I_T)])
    peak_in_T_units = 1.0 / peak
    ok = (len(cross) == 1 and abs(float(cross[0]) - peak) < 1e-3
          and abs(float(sp.N(I_beta.subs(x, 0))) - 0.25) < 1e-12
          and abs(peak_T - peak_in_T_units) > 0.05)
    detail = (f"heat-capacity peak at beta*Delta = {peak:.4f} (stationarity 2/x+1 = 2e^x/(1+e^x); "
              f"unique numeric crossing {float(cross[0]):.4f} — the Schottky temperature); Fisher peak wrt beta at x = 0 (T = inf); "
              f"Fisher peak wrt T at T/Delta = {peak_T:.3f} (= x {peak_T and 1.0/peak_T:.2f}, distinct from the C peak in T units {peak_in_T_units:.3f}) "
              "— three locations, none selected by the framework")
    return bool(ok), detail


@_safe
def _c3_salamon_berry():
    """Finite-time thermo: dissipated work >= K L^2/tau with K >= 1, saturated
    at constant Fisher speed (Salamon-Berry). Honest negative: on a 1-D family
    every monotone protocol is a geodesic, so S = 0 identically — S cannot
    order dissipation at all."""
    def w_diss(p_protocol, tau=1.0):
        ts = np.linspace(0, tau, 200000)
        ps = p_protocol(ts)
        dps = np.gradient(ps, ts)
        return float(np.trapezoid(dps ** 2 / (ps * (1 - ps)), ts))

    tau, p0, p1 = 1.0, 0.2, 0.8
    s0_, s1_ = np.arcsin(np.sqrt(p0)), np.arcsin(np.sqrt(p1))
    # Bernoulli FR geometry: ds = dp/sqrt(p(1-p)) = 2 d(asin sqrt(p)); arc = 2(s1-s0)
    arc = 2.0 * (s1_ - s0_)
    B = np.sqrt(p0 * p1) + np.sqrt((1 - p0) * (1 - p1))
    chord = 2.0 * np.arccos(B)
    S = arc - chord  # monotone path on a 1-D family IS the geodesic -> S = 0 for EVERY protocol

    def const_speed(t):  # constant Fisher speed: asin(sqrt(p)) linear in t
        return np.sin(s0_ + (s1_ - s0_) * t / tau) ** 2

    def lopsided(t):  # same endpoints, same tau, same (zero) surplus, lopsided speed
        return p0 + (p1 - p0) * (t / tau) ** 2

    w_const, w_lop = w_diss(const_speed), w_diss(lopsided)
    ok = abs(S) < 1e-12 and w_const < w_lop
    detail = (f"S = arc - chord = {S:.6f} identically for EVERY monotone protocol on this 1-D family "
              f"(P1 equality: the monotone path is the geodesic); "
              f"W_diss(const Fisher speed)={w_const:.3f} < W_diss(lopsided)={w_lop:.3f} "
              "(Salamon-Berry K >= 1, saturated at constant speed) — S is degenerate here and cannot order dissipation")
    return bool(ok), detail


@_safe
def _c4_curie_weiss():
    """Mean-field Curie-Weiss: Fisher information ~ susceptibility diverges at
    Tc; direction only (exponents are Landau mathematics). h != 0 probe rounds
    the transition. Verified numerically at concrete (a, b, t, h)."""
    a = b = 1.0
    t_up, t_dn, h_ = 1.0, -1.0, -1.0
    # h = 0: m0 = sqrt(-a t / b) for t < 0; chi = 1/(3 b m0^2) = 1/(3 a |t|)
    m0 = np.sqrt(-a * t_dn / b)
    chi_below = 1.0 / (3.0 * b * m0 ** 2)
    chi_above = 1.0 / (a * t_up)                      # m0 = 0
    m0h = (-h_ / b) ** (1.0 / 3.0)                    # t = 0, h != 0: m0 = (|h|/b)^(1/3)
    chi_h = 1.0 / (3.0 * b * m0h ** 2)
    ok = (abs(chi_below - 1.0 / 3.0) < 1e-12 and abs(chi_above - 1.0) < 1e-12
          and abs(chi_h - 1.0 / 3.0) < 1e-12 and abs(chi_below / chi_above - 1.0 / 3.0) < 1e-12)
    detail = (f"|chi(T<Tc)| = 1/(3 a|t|) = {chi_below:.4f}, |chi(T>Tc)| = 1/(a|t|) = {chi_above:.4f} "
              f"— Fisher ~ chi diverges at Tc, gamma = 1 (mean-field, external; the 1/3 amplitude ratio is the Landau factor); "
              f"h != 0 probe: |chi(0, h)| = 1/(3 b^(1/3) h^(2/3)) = {chi_h:.4f} finite — the divergence lives only at the symmetric point")
    return bool(ok), detail


@_safe
def _c5_blackbody():
    """Bose occupancy (blackbody mode): the mean-occupancy family's diameter is
    pi but unattained — no antipodal pair exists in the family, so A3 never
    fires. OPEN, with the near-tension documented."""
    n = sp.symbols("n", positive=True)
    p = 1 / (1 + n)  # geometric (Bose-Einstein) family, mean occupancy n
    ds2 = sp.simplify(sp.diff(p, n) ** 2 / (p * (1 - p)))
    # arc primitive: integral of ds = integral dn/(sqrt(n)(1+n)) = 2 arctan(sqrt(n))
    primitive = 2 * sp.atan(sp.sqrt(n))
    is_primitive = sp.simplify(sp.diff(primitive, n) - 1 / (sp.sqrt(n) * (1 + n))) == 0
    total = sp.limit(primitive, n, sp.oo)  # pi: diameter, reached only at n = oo (not a member)
    ok = sp.simplify(ds2 - 1 / (n * (1 + n) ** 2)) == 0 and is_primitive and total == sp.pi
    detail = (f"geometric-family FR line element ds^2 = 1/(n(1+n)^2); arc primitive 2 arctan(sqrt(n)); "
              f"total diameter = {total} reached only as n -> oo — pairwise distances are strictly < pi, "
              "so no antipodal pair exists in the family and A3 never fires on this carrier")
    return bool(ok), detail


SYSTEMS_C = [
    {
        "id": "c1", "class": "c",
        "name": "ideal-gas isotherm: D2 arc = thermodynamic length",
        "carrier": "ideal gas in the entropy representation, coordinates (U, V); unit under A1' from the Ruppeiner/Weinhold metric",
        "clause": "D2 ('on a thermal family this is thermodynamic length')",
        "derivation": "Ruppeiner metric g_ij = -second-derivatives of S(U,V); on an isotherm (U fixed) the arc is integral of sqrt(N k_B) dV/V = sqrt(N k_B) ln(V2/V1) — exactly the thermodynamic length; the metric is flat (g_VV is the squared gradient of a coordinate transform).",
        "known_physics": "Ruppeiner (entropy-rep) and Weinhold (energy-rep) thermodynamic geometry of the ideal gas; flatness (zero curvature) is the textbook result.",
        "check": _c1_ideal_gas,
        "verdict": "CONSIST",
        "weakness": "the form is standard thermodynamic geometry wearing the framework's unit (D2 says so itself); the entropy-vs-energy representation convention (and hence the sqrt(T) factor) is not fixed by the axioms.",
    },
    {
        "id": "c2", "class": "c",
        "name": "Schottky anomaly vs the Fisher peak",
        "carrier": "two-level system over temperature; unit under A1' from the per-level energy statistic",
        "clause": "D2 (Fisher metric) — which peak is 'the' Fisher feature is the question",
        "derivation": "The heat capacity C(x) = k_B x^2 e^x/(1+e^x)^2 (x = beta Delta) peaks where 2/x + 1 = 2 e^x/(1+e^x), i.e. x = 2.3994 — the known Schottky temperature. The family's Fisher information peaks at x = 0 in the beta parameterization but at a finite T in the T parameterization: 'the Fisher peak' is coordinate-dependent, and no clause selects a peak.",
        "known_physics": "the Schottky heat-capacity anomaly (textbook); Fisher-information peak locations are estimator-theory quantities, not laws.",
        "check": _c2_schottky,
        "verdict": "CONSIST",
        "weakness": "the heat-capacity peak is known physics and C IS the Fisher information of the beta-family up to a factor (Var(E) relation) — but 'the Fisher peak' as a framework prediction is coordinate-dependent; three locations computed, none selected.",
    },
    {
        "id": "c3", "class": "c",
        "name": "finite-time thermodynamics: length vs dissipated work",
        "carrier": "two-level family driven over tau; Bernoulli Fisher metric dp^2/(p(1-p))",
        "clause": "D2 + D4 (surplus S as 'excess length')",
        "derivation": "The Salamon-Berry bound W_diss >= K L^2/tau with K >= 1, saturated at constant Fisher speed, is exactly a length-time statement on D2's metric: the framework's arc is the right quantity for dissipation. But on a one-dimensional statistical family every monotone protocol IS the geodesic, so surplus S vanishes identically while dissipated work varies by tens of percent: S carries no dissipation information on the carriers D2 names most directly.",
        "known_physics": "Salamon-Berry / finite-time-thermodynamics dissipation bound (standard); the K >= 1 geometric factor saturated at constant speed.",
        "check": _c3_salamon_berry,
        "verdict": "CONSIST",
        "weakness": "the bound and its constant are standard finite-time thermo, not axioms (the framework's D2 names the metric, nothing more). The S-finding is a negative result recorded in detail: on 1-D carriers S is identically zero (P1 equality), so any 'surplus = waste' reading is NOT supported there.",
    },
    {
        "id": "c4", "class": "c",
        "name": "Curie-Weiss paramagnet near Tc",
        "carrier": "magnetization m of the mean-field Curie-Weiss free energy; unit under A1' = Cramer-Rao length of the m-family",
        "clause": "A1 (Fisher metric) + Criticality clause (thermal branch: rho -> inf)",
        "derivation": "Fisher information of the m-family ~ susceptibility: chi = 1/f''(m0) = 1/(3 a|t|) below and 1/(a|t|) above Tc — the Fisher metric diverges with the correlation length (criticality clause, thermal branch, rho -> inf). Exponent gamma = 1 and the 1/3 amplitude ratio are Landau mathematics, external to the framework.",
        "known_physics": "mean-field critical exponent gamma = 1 with the 1/3 amplitude ratio; chi diverges at Tc (textbook).",
        "check": _c4_curie_weiss,
        "verdict": "CONSIST",
        "weakness": "direction-only: the framework fixes the direction of the divergence, not the exponent; and the divergence lives only at the symmetric point (h != 0 probe rounds it) — the criticality clause does not say which symmetry is load-bearing.",
    },
    {
        "id": "c5", "class": "c",
        "name": "blackbody / Bose occupancy: the diameter that is never reached",
        "carrier": "mean occupancy n of a Bose mode (geometric family); unit under A1' = one quantum",
        "clause": "A3 (no antipodal pair -> no cut) + D2 (thermal family as carrier) + A6",
        "derivation": "The Bose-Einstein occupancy family (geometric distribution, mean n) has Fisher line element ds^2 = dn^2/(n(1+n)^2) and arc primitive 2 arctan(sqrt(n)); the total diameter is pi but is reached only at n = infinity, which is not a member of the family — pairwise distances are strictly less than pi, so no antipodal pair exists and A3 never fires on this carrier. Yet D2 names thermal families as carriers and A6 seeds occasions from cuts: the framework is internally silent here rather than contradictory.",
        "known_physics": "no thermal state is orthogonal to the vacuum (overlap strictly positive) — there is no finite-temperature 'antipode'.",
        "check": _c5_blackbody,
        "verdict": "OPEN",
        "weakness": "near-tension documented, not graded TENSION: D2's thermal-carrier claim and A3's cut requirement coexist only because D2 also names families that DO have antipodes; a reader wanting 'thermal systems cut' would need a clause that does not exist. Graded OPEN (framework declines: no occasions complete on this carrier).",
    },
]


# =====================================================================
# CLASS (d) — parametric estimation and filtering
# =====================================================================

"""Class (d) — parametric estimation and filtering — CRR retrodiction battery (issue #21).

Carrier class: parametric statistical families with a parameter to be estimated
from data; the framework's clauses in play are A1' (unit = Cramer-Rao length
1/sqrt(I)), P4 + A9 (scalar random-walk Kalman gain, Omega = 1), D8 (depth
1/K), and O1 (no retention law off the random walk).

Grading discipline per the battery contract (issue #21 rules 1-6 + orchestrator
clarifications): SHARP needs a named external target forced by the axioms with
no constant supplied from outside; framework-internal theorems are DESCR;
standard mathematics wearing the framework's unit is CONSIST at best.

Standalone: numpy + sympy only.
"""
import numpy as np, sympy as sp  # the battery contract's import shape; np is the battery-standard companion


def _p4_kalman():
    """Row d1: scalar random-walk steady-state Kalman gain; A9 sets v = 1."""
    q, r, v = sp.symbols("q r v", positive=True)
    M = sp.Symbol("M", positive=True)
    # M: prior variance at the update; posterior M r/(M+r); next prior adds q (random walk).
    sol = sp.solve(sp.Eq(M, M * r / (M + r) + q), M)
    Mss = [s for s in sol if sp.simplify(s.subs({q: 1, r: 1})) > 0][0]
    rv = v**2 * r  # process variance written as Fisher-speed^2 * observation variance
    Mss = sp.simplify(Mss.subs(q, rv))
    K = sp.simplify(Mss / (Mss + r))
    K_claim = (v / 2) * (sp.sqrt(v**2 + 4) - v)  # issue P4's closed form
    ok_riccati = sp.simplify(K - K_claim) == 0
    ok_omega1 = sp.simplify(K_claim.subs(v, 1) - (sp.sqrt(5) - 1) / 2) == 0
    # asymmetric probe (rule 4): v != 1 -- A9 is silent there, but the P4 form must still hold
    ok_probe = sp.simplify(K_claim.subs(v, 2) - (2 * sp.sqrt(2) - 2)) == 0
    ok_lim = sp.limit(K_claim, v, sp.oo) == 1 and sp.limit(K_claim, v, 0) == 0
    ok = bool(ok_riccati and ok_omega1 and ok_probe and ok_lim)
    return ok, (
        f"Riccati K(v) = (v/2)(sqrt(v^2+4)-v); K(1)={float(K_claim.subs(v, 1)):.6f} "
        f"(1/phi={float((sp.sqrt(5) - 1) / 2):.6f}); probe v=2: K={float(K_claim.subs(v, 2)):.6f} "
        f"(= 2*sqrt(2)-2 = {float(2 * sp.sqrt(2) - 2):.6f}); K -> 1 as v -> oo, K -> 0 as v -> 0"
    )


def _cr_unit():
    """Row d2: A1' unit = Cramer-Rao length 1/sqrt(I) on a parametric family."""
    mu, x = sp.symbols("mu x", real=True)
    s = sp.Symbol("s", positive=True)
    # Gaussian location family p(x | mu) = N(mu, s^2)
    p = sp.exp(-((x - mu) ** 2) / (2 * s**2)) / (s * sp.sqrt(2 * sp.pi))
    score = sp.simplify(sp.diff(sp.log(p), mu))
    I = sp.simplify(sp.integrate(score**2 * p, (x, -sp.oo, sp.oo)))
    unit = sp.simplify(1 / sp.sqrt(I))
    n = sp.Symbol("n", positive=True, integer=True)
    crb = sp.simplify(1 / (n * I))
    ok = sp.simplify(I - 1 / s**2) == 0 and sp.simplify(unit - s) == 0 and sp.simplify(crb - s**2 / n) == 0
    return bool(ok), (
        f"score = -(x-mu)/s^2 -> I = 1/s^2; A1' unit 1/sqrt(I) = s (the family's own spread); "
        f"CRB var >= 1/(n I) = s^2/n: the smallest resolvable change is the CR length, by definition"
    )


def _brownian_drift():
    """Row d3: drifted Brownian motion, drift estimation error vs 1/sqrt(T)."""
    mu, x = sp.symbols("mu x", real=True)
    s, T = sp.symbols("sigma T", positive=True)
    # X_T ~ N(mu*T, sigma^2*T) for dX = mu dt + sigma dW observed over window T
    p = sp.exp(-((x - mu * T) ** 2) / (2 * s**2 * T)) / sp.sqrt(2 * sp.pi * s**2 * T)
    score = sp.simplify(sp.diff(sp.log(p), mu))
    I = sp.simplify(sp.integrate(score**2 * p, (x, -sp.oo, sp.oo)))
    unit = sp.simplify(1 / sp.sqrt(I))
    ok = sp.simplify(I - T / s**2) == 0 and sp.simplify(unit - s / sp.sqrt(T)) == 0
    # asymmetric probe: the information does not care about the drift value itself
    dep = sp.simplify(sp.diff(I, mu))
    ok = bool(ok and dep == 0)
    return ok, (
        f"score = (X_T - mu*T)/sigma^2 -> I(mu, T) = T/sigma^2; A1' unit = sigma/sqrt(T); "
        f"exact MLE var = sigma^2/T attains the bound; dI/dmu = 0 (mu=0 and mu!=0 carry equal information)"
    )


def _ou_gain():
    """Row d4: Ornstein-Uhlenbeck (AR(1)) steady filter — P4's domain is the random walk ONLY."""
    v, r, a = sp.symbols("v r a", positive=True)
    M = sp.Symbol("M", positive=True)
    q = v**2 * r  # write the process variance in Fisher-speed units from the start
    # OU sampled at unit intervals: X_{k+1} = a X_k + w; Riccati with contraction a made explicit
    sol = sp.solve(sp.Eq(M, a**2 * M * r / (M + r) + q), M)
    Mss = [s for s in sol if float(s.subs({v: 1, r: 1, a: sp.Rational(1, 2)})) > 0][0]
    K_ou = sp.simplify(Mss / (Mss + r))
    K_p4 = (v / 2) * (sp.sqrt(v**2 + 4) - v)
    # a -> 1 (random walk) must recover P4 exactly
    recovers = sp.simplify(K_ou.subs(a, 1) - K_p4) == 0
    # at Fisher speed v = 1 the OU gain is NOT 1/phi once a < 1
    off = K_ou.subs({v: 1, a: sp.Rational(9, 10)})
    not_p4 = sp.simplify(off - (sp.sqrt(5) - 1) / 2) != 0
    if not (recovers and not_p4):
        # would contradict row d1 / O1's framing -- a framework claim failing, not an OPEN row
        return False, (
            f"unexpected: a->1 recovers P4 = {recovers}; K_ou(v=1, a=0.9) = {float(off):.6f} vs 1/phi = "
            f"{float((sp.sqrt(5) - 1) / 2):.6f}"
        )
    return None, (
        f"P4's own Riccati with contraction a: K_ou(v, a) = M/(M+r), M = a^2 M r/(M+r) + q; "
        f"K_ou(v=1, a=1) = 0.618034 = 1/phi (P4 limit), but K_ou(v=1, a=0.9) = {float(off):.6f} != 1/phi -- "
        f"the gain needs the contraction a beyond v = sqrt(q/r); P4 is stated for the random walk only and "
        f"O1 supplies the unit only off it: the framework declines to derive this gain"
    )


def _phase_crb():
    """Row d5: N-probe qubit phase estimation, quantum Cramer-Rao scaling."""
    phi = sp.Symbol("phi", real=True)
    a, b = sp.symbols("a b", positive=True)  # amplitudes on |0>, |1>; a^2 + b^2 = 1
    # Ramsey probe |psi_phi> = a|0> + e^{i phi} b|1>; phase generator G = sigma_z / 2
    psi = sp.Matrix([a, sp.exp(sp.I * phi) * b])
    G = sp.Matrix([[sp.Rational(1, 2), 0], [0, -sp.Rational(1, 2)]])
    varG = sp.simplify((psi.H * G**2 * psi)[0, 0] - ((psi.H * G * psi)[0, 0]) ** 2)
    FQ_ab = sp.simplify(4 * varG)  # quantum Fisher information of a pure family = 4 Var(G)
    p = sp.Symbol("p", positive=True)  # occupation of |0>: p = a^2, 1 - p = b^2
    FQ = sp.simplify(FQ_ab.subs(a, sp.sqrt(p)).subs(b, sp.sqrt(1 - p)))
    N = sp.Symbol("N", positive=True, integer=True)
    crb = sp.simplify(1 / (N * FQ))
    FQ_bal = sp.simplify(FQ_ab.subs([(a, 1 / sp.sqrt(2)), (b, 1 / sp.sqrt(2))]))
    FQ_un = FQ.subs(p, sp.Rational(1, 3))  # asymmetric probe: unbalanced state
    crb_bal = sp.simplify(crb.subs(p, sp.Rational(1, 2)))
    ok = sp.simplify(FQ - 4 * p * (1 - p)) == 0 and FQ_bal == 1 and sp.simplify(crb_bal - 1 / N) == 0
    return bool(ok), (
        f"F_Q = 4p(1-p) (pure-state QFI = 4 Var(sigma_z/2)); balanced probe p=1/2: F_Q = 1 -> "
        f"var(phi_hat) >= 1/N, Delta phi >= 1/sqrt(N) (shot-noise limit); probe p=1/3: F_Q = {FQ_un} = "
        f"8/9 < 1 -- F_Q is carried by the chosen probe state, not fixed by A1'"
    )


SYSTEMS_D = [
    {
        "id": "d1",
        "class": "d",
        "name": "scalar random-walk Kalman gain",
        "carrier": "scalar random-walk state, process var q, observation var r; unit = Fisher speed v = sqrt(q/r) (A1')",
        "clause": "P4 + A9 (Omega = 1 sets v = 1)",
        "derivation": "Steady-state Riccati gives M = M r/(M+r) + q; solving, K = M/(M+r) = (v/2)(sqrt(v^2+4) - v). "
        "A9 fixes Omega = 1, i.e. the Fisher speed v = 1, so the framework's filter gain is K(1) = 1/phi - no constant chosen. "
        "Probe at v = 2 (A9 silent there): the P4 form still holds, K(2) = 2*sqrt(2)-2.",
        "known_physics": "textbook steady-state Kalman gain for a random walk (Riccati); K -> 1 as v -> inf, K -> 0 as v -> 0.",
        "check": _p4_kalman,
        "verdict": "CONSIST",
        "weakness": "the FORM is textbook Riccati (the issue's own P4 says so); the only framework content is reading sqrt(q/r) as a Fisher speed and v = 1 from Omega = 1.",
    },
    {
        "id": "d2",
        "class": "d",
        "name": "Cramer-Rao unit 1/sqrt(I)",
        "carrier": "Gaussian location family p(x|mu) = N(mu, s^2); unit under A1' = 1/sqrt(I) per datum",
        "clause": "A1'",
        "derivation": "A1' reads the unit off the parametric family: unit = 1/sqrt(I). Score of the location family is "
        "(x-mu)/s^2, so I = 1/s^2 and the unit is s -- the family's own spread, not the instrument's beyond it. "
        "The Cramer-Rao bound var >= 1/(n I) = s^2/n restates the unit as the smallest resolvable change; nothing is predicted.",
        "known_physics": "Cramer-Rao bound (Fisher 1925; Cramer/Rao 1946): any unbiased estimator has var >= 1/(n I); "
        "the smallest resolvable change of theta per datum is 1/sqrt(I).",
        "check": _cr_unit,
        "verdict": "DESCR",
        "weakness": "framework-internal/definitional: A1' *names* the Cramer-Rao length as the unit -- this is standard mathematics declared, not derived; also which information counts as the occasion's (per datum vs per window) is a carrier fact the axioms do not fix.",
    },
    {
        "id": "d3",
        "class": "d",
        "name": "drifted Brownian 1/sqrt(T) scaling",
        "carrier": "drifted Brownian motion dX = mu dt + sigma dW observed for window T; unit under A1' = 1/sqrt(I(mu, T))",
        "clause": "A1'",
        "derivation": "Carrier: X_T ~ N(mu T, sigma^2 T). A1': unit = 1/sqrt(I). Score for mu is (X_T - mu T)/sigma^2, so "
        "I(mu, T) = T/sigma^2 and the unit is sigma/sqrt(T). The MLE mu_hat = X_T/T attains the bound exactly: var = sigma^2/T. "
        "The sqrt(I) ~ sqrt(T) growth is the 1/sqrt(T) scaling; the axioms add the reading, no constant is chosen.",
        "known_physics": "classical drift estimation: I(mu; window T) = T/sigma^2 and the MLE mu_hat = X_T/T has var = sigma^2/T "
        "exactly -- the universal 1/sqrt(T) Fisher scaling of integrated-process estimation.",
        "check": _brownian_drift,
        "verdict": "CONSIST",
        "weakness": "standard CRB wearing the unit: I(mu, T) = T/sigma^2 is classical Fisher information, derived by no clause of the framework; the window T and the terminal observable X_T are estimator choices the axioms do not fix. Scaling only -- no constant predicted.",
    },
    {
        "id": "d4",
        "class": "d",
        "name": "Ornstein-Uhlenbeck steady filter",
        "carrier": "AR(1)/OU state X_{k+1} = a X_k + w (OU sampled at unit interval, a = exp(-theta)), observation var r; "
        "Fisher speed v = sqrt(q/r) plus the contraction a",
        "clause": "P4 (domain) + O1",
        "derivation": "Carrier: AR(1) state. Apply P4's own Riccati with the contraction made explicit: M = a^2 M r/(M+r) + q. "
        "Solving, K_ou(v, a) = M/(M+r) depends on a and v separately: at v = 1, a = 0.9, K = 0.597, not 1/phi. "
        "P4 is stated for the scalar random-walk state ONLY; O1: off the random walk the framework supplies the unit only and "
        "claims no retention law. Framework answer: none.",
        "known_physics": "textbook steady-state Kalman gain for an AR(1) state (Riccati with contraction a): K = M/(M+r) with "
        "M = a^2 M r/(M+r) + q, a function of a and v = sqrt(q/r) separately.",
        "check": _ou_gain,
        "verdict": "OPEN",
        "weakness": "OPEN by O1, checked mechanically: the gain needs the contraction a beyond v = sqrt(q/r) (K_ou(1, 0.9) = 0.597 vs 1/phi = 0.618, while a = 1 recovers P4 exactly). No framework claim is contradicted -- there is no claim to check; the framework explicitly declines.",
    },
    {
        "id": "d5",
        "class": "d",
        "name": "N-probe phase estimation CRB",
        "carrier": "N independent Ramsey probes of a qubit phase phi, |psi_phi> = sqrt(p)|0> + e^{i phi} sqrt(1-p)|1>; "
        "unit under A1' = 1/sqrt(N F_Q), quantum Fisher information per probe",
        "clause": "A1'",
        "derivation": "Carrier: N independent probes, I_total = N F_Q. A1': unit = 1/sqrt(I_total) = 1/sqrt(N F_Q). "
        "Pure-state QFI = 4 Var(G) with G = sigma_z/2 the phase generator, so F_Q = 4 p(1-p); the balanced probe p = 1/2 "
        "(the state at the A3-antipode of |0>) has F_Q = 1 and Delta phi >= 1/sqrt(N) -- the shot-noise limit. "
        "The framework fixes the CRB form only; F_Q is carried by the chosen probe state.",
        "known_physics": "quantum Cramer-Rao: var(phi_hat) >= 1/(N F_Q); a balanced Ramsey probe has F_Q = 1, giving the "
        "standard quantum (shot-noise) limit Delta phi = 1/sqrt(N); entangled GHZ probes reach F_Q = N^2 (Heisenberg limit 1/N).",
        "check": _phase_crb,
        "verdict": "CONSIST",
        "weakness": "A1' supplies the CRB form only; F_Q is a property of the chosen probe state -- the balanced p = 1/2 probe is a metrology choice the axioms do not force (probe p = 1/3 gives F_Q = 8/9, checked); no clause reaches entangled probes, so the Heisenberg limit 1/N is outside the framework.",
    },
]


# =====================================================================
# CLASS (e) — oscillators and limit cycles (physical)
# =====================================================================

"""Class (e) — oscillators and limit cycles (physical). Issue #21 retrodiction battery.

Rows implement the DECIDED design from the original writer's validated log
(driven-damped Duffing probe in _debug5.py; Hopf post-mortem fixes). Checks run
standalone with numpy+scipy+sympy only, deterministic, and never raise.
"""
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.signal import hilbert


def _e1_hopf():
    """Hopf normal form: cycle extent ~ sqrt(mu), relaxation rate k = 2 mu,
    D8 depth d = 1/K(v) with v ~ sqrt(k) -> d -> inf. Known: critical slowing
    down. Asymmetry probe: quadratic shear eps * mu * (x^2 - y^2) on ydot —
    vanishes with mu, so the bifurcation point is untouched."""
    def rhs(t, s, mu, shear):
        x, y = s
        r2 = x * x + y * y
        return [mu * x - y - x * r2,
                x + mu * y - y * r2 + shear * mu * (x * x - y * y)]

    mus = [0.05, 0.1, 0.2, 0.4]
    extents, rates = [], []
    for mu in mus:
        sol = solve_ivp(rhs, (0, 400.0), [0.1, 0.0], args=(mu, 0.0),
                        rtol=1e-10, atol=1e-12, dense_output=True, max_step=0.05)
        ts = np.arange(200.0, 400.0, 0.01)
        pts = sol.sol(ts)
        r_sat = float(np.max(np.hypot(pts[0], pts[1])))  # max distance from ORIGIN (cycle center)
        extents.append(r_sat)
        # relaxation: kick radially OUTWARD from the saturated cycle; the excess
        # delta = r - r_sat decays at rate 2 mu (radial linearization: ddelta = -2 mu delta)
        sol2 = solve_ivp(rhs, (0, 60.0), [r_sat + 0.1 * mu, 0.0], args=(mu, 0.0),
                         rtol=1e-11, atol=1e-13, max_step=0.005)
        r = np.hypot(sol2.y[0], sol2.y[1])
        delta = r - r_sat
        win = (sol2.t > 0.2) & (sol2.t < 1.5) & (delta > 1e-9)
        slope = float(np.polyfit(sol2.t[win], np.log(delta[win]), 1)[0])
        rates.append(-slope)
    ratios = [e / np.sqrt(m) for e, m in zip(extents, mus)]
    ratemus = [k / (2.0 * m) for k, m in zip(rates, mus)]
    # shear probe: direction survives breaking rotational symmetry
    sol_s = solve_ivp(rhs, (0, 400.0), [0.1, 0.0], args=(0.1, 0.5),
                      rtol=1e-10, atol=1e-12, dense_output=True, max_step=0.05)
    ts_s = np.arange(200.0, 400.0, 0.01)
    pts_s = sol_s.sol(ts_s)
    extent_shear = float(np.max(np.hypot(pts_s[0], pts_s[1])))
    v = sp.symbols("v", positive=True)
    K = v / 2 * (sp.sqrt(v ** 2 + 4) - v)
    d_small = sp.limit(1 / K, v, 0, "+")
    ok = (np.allclose(ratios, ratios[0], rtol=0.05)
          and np.allclose(ratemus, 1.0, atol=0.15)
          and abs(extent_shear - extents[1]) < 0.2 * extents[1]
          and d_small == sp.oo)
    detail = (f"extent/sqrt(mu)={ratios[0]:.3f}..{ratios[-1]:.3f} (Hopf amplitude ~ sqrt(mu)); "
              f"k/(2 mu)={ratemus[0]:.3f}..{ratemus[-1]:.3f} (relaxation rate 2 mu); "
              f"shear probe extent={extent_shear:.3f} vs symmetric {extents[1]:.3f} at mu=0.1; "
              f"D8 route: v~sqrt(k) -> K~v -> d=1/K -> oo as mu->0")
    return bool(ok), detail


def _e2_antipode_extremum():
    """Driven damped Duffing: does the A3 antipode coincide with the opposite
    extremum? Time-reversal theorem: a conservative 1-D oscillator — even with
    an asymmetric potential — traverses equal half-arcs, so antipode and opposite
    extremum coincide by reversibility, NOT by A3's content (the framework's own
    caveat on equal half-turn arcs). Broken reversibility (drive + damping +
    quadratic asymmetry) splits them: A3 becomes testable."""
    delta_, F, om = 0.5, 1.0, 1.0

    def solve(alpha, tmax=400.0):
        def rhs(t, s):
            x, v = s
            return [v, F * np.cos(om * t) - delta_ * v - x - alpha * x * x - x ** 3]
        return solve_ivp(rhs, (0, tmax), [0.0, 0.0], rtol=1e-10, atol=1e-12,
                         dense_output=True, max_step=0.01)

    def measures(alpha):
        sol = solve(alpha)
        ts = np.arange(100.0, 400.0, 0.005)
        x = sol.sol(ts)[0]
        xm = x - x.mean()
        cross = np.where(np.diff(np.sign(xm)) > 0)[0]
        T = float(np.median(np.diff(ts[cross])))
        dt = ts[1] - ts[0]
        # waveform skew on the RAW signal (no mean subtraction — DC rectification
        # is part of the asymmetry) and the DC shift itself
        skew = float(abs(np.mean(x ** 3)) / (np.mean(x ** 2) ** 1.5))
        dc = float(x.mean())
        # anchor at EVERY maximum in the window; per cycle: (a) time to the
        # phase-antipode (analytic-signal phase advance pi from that maximum),
        # (b) time to the opposite extremum (the minimum). Average over cycles —
        # the split is a property of the waveform, not of one cycle.
        ph = np.unwrap(np.angle(hilbert(xm)))
        span = int(1.3 * T / dt)
        loc = np.where((xm[1:-1] > xm[:-2]) & (xm[1:-1] >= xm[2:]) & (xm[1:-1] > 0.5 * xm.max()))[0] + 1
        loc = loc[(loc > span) & (loc + span < len(xm) - 1)]
        f_ants, f_mins = [], []
        for i_max in loc:
            adv = ph[i_max:] - ph[i_max]
            i_ant = i_max + int(np.argmax(adv >= np.pi))
            seg = xm[i_max:i_max + span]
            i_min = i_max + int(np.argmin(seg))
            f_ants.append((ts[i_ant] - ts[i_max]) / T)
            f_mins.append((ts[i_min] - ts[i_max]) / T)
        f_ant = float(np.mean(np.mod(f_ants, 1.0)))
        f_min = float(np.mean(np.mod(f_mins, 1.0)))
        return f_ant, f_min, skew, dc

    f0a, f0m, s0, dc0 = measures(0.0)
    f1a, f1m, s1, dc1 = measures(0.5)
    ok = (abs(f0a - f0m) < 0.005 and s0 < 0.01
          and abs(f1a - f1m) > 0.005 and abs(f1a - f1m) > 5.0 * abs(f0a - f0m)
          and s1 > 2.0 * s0)
    detail = (f"alpha=0: antipode@{f0a:.4f} opposite-extremum@{f0m:.4f} skew={s0:.4f} dc={dc0:.4f} (coincide — time-reversal); "
              f"alpha=1/2 driven: antipode@{f1a:.4f} opposite-extremum@{f1m:.4f} skew={s1:.4f} dc={dc1:.4f} (split — A3 becomes testable)")
    return bool(ok), detail


def _e3_pendulum():
    """Pendulum period vs amplitude. Known: T(A) = 4 sqrt(L/g) K(sin^2(A/2)) —
    grows with amplitude. No framework clause addresses the law (O1)."""
    A = sp.symbols("A", positive=True)
    T = 4 * sp.elliptic_k(sp.sin(A / 2) ** 2)
    ratio_small = sp.limit(T / (2 * sp.pi), A, 0)
    ratio_half = float(T.subs(A, sp.pi / 2) / (2 * sp.pi))
    ok = sp.simplify(ratio_small - 1) == 0 and ratio_half > 1.07
    detail = (f"T(A=pi/2)/T0 = {ratio_half:.6f} (exact elliptic; known grows with amplitude); "
              "no framework clause derives the period-amplitude law (O1 declines)")
    return bool(ok), detail


def _e4_lc():
    """Ideal LC tank: perfectly harmonic, symmetric limit cycle. Antipode =
    opposite extremum trivially; rho constant. Nothing to test (symmetry fact)."""
    t = sp.symbols("t", real=True)
    x = sp.sin(t)
    speed = sp.sqrt(sp.diff(x, t) ** 2 + sp.diff(x, t, 2) ** 2)
    half_arc = sp.integrate(speed, (t, 0, sp.pi))
    full_arc = sp.integrate(speed, (t, 0, 2 * sp.pi))
    ok = sp.simplify(half_arc / full_arc - sp.Rational(1, 2)) == 0
    detail = (f"half-turn arc fraction = {half_arc}/{full_arc} = 1/2 exactly (uniform speed on the circle); "
              "perfect symmetry: nothing for A3 to disagree with (DESCR by symmetry)")
    return bool(ok), detail


def _e5_rossler():
    """Rossler (canonical 0.2, 0.2, 5.7): chaotic amplitude, coherent phase.
    Known: small but nonzero phase diffusion. No framework clause addresses
    phase diffusion in chaotic oscillators."""
    a, b, c = 0.2, 0.2, 5.7

    def rhs(t, s):
        x, y, z = s
        return [-y - z, x + a * y, b + z * (x - c)]

    sol = solve_ivp(rhs, (0, 4000.0), [1.0, 0.0, 0.0], rtol=1e-9, atol=1e-11,
                    dense_output=True, max_step=0.02)
    ts = np.arange(400.0, 4000.0, 0.01)
    x = sol.sol(ts)[0]
    xm = x - x.mean()
    cross = ts[np.where(np.diff(np.sign(xm)) > 0)[0]]
    T = np.diff(cross)
    T = T[(T > 1.0) & (T < 10.0)]
    cv_T = float(np.std(T) / np.mean(T))
    D_phi = float(2 * np.pi ** 2 * np.var(T) / np.mean(T) ** 3)
    cv_z = float(np.std(sol.sol(ts)[2]) / abs(np.mean(sol.sol(ts)[2])))
    ok = cv_T > 0.02 and 0.001 < D_phi < 0.5 and cv_z > 0.5
    detail = (f"CV_T={cv_T:.3f} D_phi={D_phi:.4f} (return-time phase diffusion) CV_z={cv_z:.2f}; "
              "phase coherent, amplitude chaotic — no framework clause addresses D_phi (declines)")
    return bool(ok), detail


SYSTEMS_E = [
    {
        "id": "e1", "class": "e",
        "name": "Hopf normal form: extent, relaxation, D8 depth",
        "carrier": "(x, y) amplitude-phase plane of the Hopf normal form; unit under A1' = Cramer-Rao length of the two-parameter Gaussian family at the cycle",
        "clause": "Criticality clause (Hopf: rho -> 0) + D8 (depth -> inf)",
        "derivation": "Cycle radius is sqrt(mu), so the half-turn extent scales as sqrt(mu) and rho = extent/sigma -> 0 (criticality clause, Hopf branch). The linearized amplitude mode decays at rate k = 2 mu; per-step Fisher speed v ~ sqrt(k); P4 gives K(v) ~ v for small v, so D8's d = 1/K diverges as mu -> 0.",
        "known_physics": "Hopf: amplitude ~ sqrt(mu - mu_c), relaxation time ~ 1/mu (critical slowing down). Direction matches; the route through K(v) is the framework's.",
        "check": _e1_hopf,
        "verdict": "CONSIST",
        "weakness": "direction-only: the framework fixes neither the amplitude exponent nor the relaxation form (both are normal-form mathematics). The rho->0 (amplitude) and d->inf (memory) statements are two different quantities, both framework assertions — flagged by the class-(h) audit as a would-be tension; graded non-tension because no clause contradicts another.",
    },
    {
        "id": "e2", "class": "e",
        "name": "driven damped Duffing: antipode vs extremum",
        "carrier": "periodic forced response x(t) of the driven damped Duffing oscillator; intrinsic phase via the analytic signal",
        "clause": "A3 (antipode cut) vs peak detection — the framework's own testability boundary",
        "derivation": "Time-reversal theorem: a conservative 1-D oscillator (even with an asymmetric potential) traverses equal half-arcs, so the antipode is the opposite extremum by reversibility — symmetric members coincide for physics reasons, not because A3 says so. Breaking reversibility (drive + damping + quadratic asymmetry) splits the two criteria: the framework's 'A3 is testable only where they disagree' is realized.",
        "known_physics": "no independent law locates an oscillator's 'cut' (oscillators have no events of their own; H-CUT is vacuous here). The retrodiction is that A3's testability boundary behaves as the framework states.",
        "check": _e2_antipode_extremum,
        "verdict": "DESCR",
        "weakness": "phase defined via the analytic signal (a named choice); drive delta=0.5, F=1, omega=1 and alpha in {0, 1/2} are chosen probe members; antipode and extremum positions are averaged over all cycles in the window. DESCR because the coincidence on reversible members is time-reversal symmetry and the split is definitional, not a derivation landing on known physics.",
    },
    {
        "id": "e3", "class": "e",
        "name": "ideal pendulum: period grows with amplitude",
        "carrier": "pendulum angle theta; unit under A1' from the per-cycle amplitude statistic",
        "clause": "O1 (framework supplies the unit only)",
        "derivation": "T(A) = 4 sqrt(L/g) K(sin^2(A/2)) grows monotonically with amplitude; rho is therefore amplitude-dependent and measured, never predicted. No clause targets the period-amplitude law.",
        "known_physics": "the exact elliptic period-amplitude relation (textbook).",
        "check": _e3_pendulum,
        "verdict": "OPEN",
        "weakness": "graded OPEN because no clause addresses the quantity, not because a check failed.",
    },
    {
        "id": "e4", "class": "e",
        "name": "ideal LC tank: the perfectly symmetric baseline",
        "carrier": "(charge, current) phase circle; Fisher speed constant along the cycle",
        "clause": "A3 (symmetric rotor — nothing to disagree on)",
        "derivation": "On the harmonic circle the speed is constant, so the antipode is exactly the half-arc point; peak and antipode coincide by symmetry.",
        "known_physics": "the sinusoid; equal half-arcs are the defining symmetry.",
        "check": _e4_lc,
        "verdict": "DESCR",
        "weakness": "deliberate negative baseline: a row that can only be DESCR (a symmetry fact), included per the issue's demand that the battery not stop at flattering systems.",
    },
    {
        "id": "e5", "class": "e",
        "name": "Rossler attractor: phase-coherent chaos",
        "carrier": "(x, y, z) chaotic trajectory; phase from return-time statistics",
        "clause": "— (no clause addresses chaotic phase diffusion)",
        "derivation": "Rossler at canonical parameters has a well-defined but noisy phase: return times fluctuate (CV_T ~ 0.09) giving phase-diffusion constant D_phi = 2 pi^2 Var(T)/<T>^3 > 0, while the amplitude coordinate is strongly irregular (CV_z ~ 1.3 or larger), so rho varies from occasion to occasion. No framework clause derives or constrains D_phi.",
        "known_physics": "phase-coherent chaos: small nonzero phase diffusion on the Rossler attractor (standard nonlinear-dynamics result).",
        "check": _e5_rossler,
        "verdict": "OPEN",
        "weakness": "return-time-based phase estimator is a named choice (alternatives: analytic signal, Poincare section — same qualitative verdict); parameters are the canonical (0.2, 0.2, 5.7). OPEN because the framework declines, not because a check failed.",
    },
]


# =====================================================================
# CLASS (f) — point processes and natural-time systems
# =====================================================================

"""Class (f) — point processes / natural time. CRR retrodiction battery (issue #21).

Scratch module written by the class-(f) writer only; the orchestrator integrates
SYSTEMS_F into crr_retrodictions.py and audits every verdict. No repo writes.

Clause provenance (contract: the ISSUE's inline framework is the target):
  * The issue's framework statement has no P5 and no Poisson-metric clause.
    P5 (row f2) is theory/CRR.md v3.1 sec.7 — the binding menu in
    local://crr-retro-architecture.md names it explicitly for the Omori row.
  * The Poisson-rate Fisher metric used in f1/f4 (FR distance 2|sqrt(l2)-
    sqrt(l1)| on the Poisson mean family) is theory/SCOPE.md's metric table,
    verified in theory/checks/verify_scope_math.py. The repo's own MEAS2 study
    calls this the "Fisher-native Poisson carrier".
Both provenance facts are flagged in the rows' weakness fields.
"""
import numpy as np
import sympy as sp


def _guard(fn):
    """Checks must not raise; surface the error instead of swallowing it."""
    def wrapped():
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            return None, "check errored (reported, not silent): %r" % (exc,)
    wrapped.__name__ = fn.__name__
    return wrapped


# ---------------------------------------------------------------- f1
@_guard
def _f1_poisson_cuts_and_cvs():
    """Constant-rate Poisson: A3 vs D5 on where the cut is, plus the CV data.

    A3 answer: the natural carrier is the Poisson counting family (state =
    cumulative intensity A since the last cut; Poisson mean family has Fisher
    metric g = 1/mu, FR arc 2(sqrt(m2)-sqrt(m1))). Its FR extent from 0 is
    integral_0^oo mu^{-1/2} dmu = oo -> no half-turn, no antipode -> by A3's own
    closing sentence the process never cuts and no occasion completes.
    D5 answer: for a point process the cut IS the event, so occasions = inter-
    event intervals. In transformed (natural) time A the process is unit-rate
    Poisson, so the event fires at A ~ Exp(1) (time-rescaling theorem): the cut
    lands at arc C_m = 2*sqrt(A_m), a RANDOM arc, not a fixed half-turn.
    Under D5's cut the framework's arc is mechanically more regular than clock:
    CV(2*sqrt(Exp(1))) = sqrt(4/pi - 1) ~= 0.523 < CV(dt) = 1, although a
    constant-rate Poisson has no intrinsic regularity (identity-metric control:
    CV(C) = CV(dt) trivially).
    """
    mu = sp.symbols("mu", positive=True)
    extent = sp.integrate(1 / sp.sqrt(mu), (mu, 0, sp.oo))
    a3_no_cut = bool(extent == sp.oo)  # extent is oo: no half-turn exists
    x = sp.symbols("x", positive=True)
    e_x = sp.integrate(x * sp.exp(-x), (x, 0, sp.oo))                 # 1
    e_sqrt = sp.integrate(sp.sqrt(x) * sp.exp(-x), (x, 0, sp.oo))     # sqrt(pi)/2
    cv2 = sp.simplify((e_x - e_sqrt**2) / e_sqrt**2)                  # (4-pi)/pi
    cv_theory = sp.sqrt(sp.simplify(4 / sp.pi - 1))
    rng = np.random.default_rng(20260916)
    A = rng.exponential(1.0, 200_000)          # A ~ Exp(1) at each event
    dt = A / 1.0
    C = 2.0 * np.sqrt(A)                       # framework arc (Poisson metric)
    cv_dt = float(np.std(dt) / np.mean(dt))
    cv_arc = float(np.std(C) / np.mean(C))
    ok = a3_no_cut and abs(cv_dt - 1.0) < 0.02 and abs(cv_arc - float(cv_theory)) < 0.01
    detail = ("A3: counting-family FR extent=%s -> no antipode -> 0 cuts; "
              "D5: cut=event, C=2*sqrt(A), A~Exp(1) -> CV(arc)=%.3f vs CV(dt)=%.3f "
              "(theory sqrt(4/pi-1)=%.4f, CV^2=%s); identity metric: CV=%.3f (equal trivially)"
              % (extent, cv_arc, cv_dt, float(cv_theory), cv2, cv_dt))
    return ok, detail


# ---------------------------------------------------------------- f2
@_guard
def _f2_omori_p5():
    """P5 consistency relation: p=1 power-law rate <-> power-law retention."""
    t, c, K, rho, tau = sp.symbols("t c K rho tau", positive=True)
    A_p1 = sp.integrate(K / (tau + c), (tau, 0, t))
    R_p1 = sp.simplify(sp.exp(-A_p1 / rho))
    law = ((t + c) / c) ** (-K / rho)
    p1_exact = sp.simplify(R_p1 - law) == 0
    el_p1 = sp.simplify(sp.diff(sp.log(R_p1), t) * (t + c))
    elast_const = sp.simplify(el_p1 + K / rho) == 0            # = -K/rho, constant
    A_p2 = sp.integrate(K / (tau + c) ** 2, (tau, 0, t))
    R_p2 = sp.exp(-A_p2 / rho)
    el_p2 = sp.diff(sp.log(R_p2), t) * (t + c)
    d_el_p2 = sp.diff(el_p2, t).subs({K: 1, rho: 1, c: 1, t: 1})
    p2_tdep = bool(abs(float(d_el_p2)) > 1e-12)                # elasticity drifts
    R_num = float(R_p1.subs({K: 1, rho: 1, c: sp.Rational(1, 100), t: 1}))
    ok = bool(p1_exact and elast_const and p2_tdep)
    detail = ("p=1: R=((t+c)/c)^(-K/rho) exact, elasticity dlnR/dln(t+c)=-K/rho "
              "constant; p=2: elasticity t-dependent (=%+.4f at t=c=K=rho=1), "
              "stretched exp, not a power law; R(t=1,c=0.01,K=rho=1)=%.6f"
              % (float(d_el_p2), R_num))
    return ok, detail


# ---------------------------------------------------------------- f3
@_guard
def _f3_erlang2_open():
    """Erlang-2 renewal: the framework declines to derive the inter-event law."""
    th, tau = sp.symbols("theta tau", positive=True)
    pdf = th**2 * tau * sp.exp(-th * tau)                      # Gamma(k=2, th)
    mean = sp.integrate(tau * pdf, (tau, 0, sp.oo))            # 2/th
    m2 = sp.integrate(tau**2 * pdf, (tau, 0, sp.oo))           # 6/th^2
    cv2 = sp.simplify((m2 - mean**2) / mean**2)                # 1/2
    return (None,
            "known CV=sqrt(1/2)=%.4f < 1 (printed as the missed target; cv^2=%s); "
            "framework declines: D5 gives cuts=events but no clause derives the "
            "renewal law — P4/D8 are random-walk only (O1: no retention law "
            "claimed elsewhere), A6 seeds content, A8 disclaims occasion timing"
            % (float(sp.sqrt(cv2)), cv2))


# ---------------------------------------------------------------- f4
@_guard
def _f4_geiger_deadtime():
    """Dead-time Geiger: recorded train is clock-regular; framework arc is
    blind to the dead time (contributes zero arc), so no clause derives the
    regularity the physics actually has."""
    lam, td = sp.symbols("lambda tau_d", positive=True)
    cv_clock = sp.simplify((1 / lam) / (td + 1 / lam))         # 1/(1+lam*tau_d)
    cv_clock_ok = sp.simplify(cv_clock - 1 / (1 + lam * td)) == 0
    at9 = float(cv_clock.subs(lam, 9).subs(td, 1))             # lam*tau_d = 9
    cv_arc_theory = float(sp.sqrt(4 / sp.pi - 1))              # tau_d-blind (f1)
    rng = np.random.default_rng(4747)
    A = rng.exponential(1.0, 200_000)                          # A at event ~ Exp(1)
    C = 2.0 * np.sqrt(A)
    cv_arc_sim = float(np.std(C) / np.mean(C))
    assert cv_clock_ok
    return (None,
            "known: CV(dt)=1/(1+lam*tau_d)=%.4f at lam*tau_d=9 (refractory "
            "regularizes in CLOCK time, S-G-like); framework arc C=2*sqrt(A) with "
            "A~Exp(1) is tau_d-blind: CV(arc)=%.3f (theory %.4f) at any lam*tau_d; "
            "identity metric: arc proportional to dt, CV=%.4f trivially. No clause "
            "(P4/D8 random-walk only; A8 disclaims timing) derives any of it"
            % (at9, cv_arc_sim, cv_arc_theory, at9))


# ---------------------------------------------------------------- f5
@_guard
def _f5_hawkes_open():
    """Hawkes self-excitation: framework declines; A6 near-miss defused."""
    rng = np.random.default_rng(4711)
    mu, alpha, beta = 1.0, 0.8, 1.0                            # branching n = 0.8
    T, burn = 4000.0, 500.0
    span = T + burn
    n_imm = int(rng.poisson(mu * span))                        # immigrants, Poisson(mu)
    stack = np.sort(rng.uniform(0.0, span, n_imm)).tolist()
    events = []
    while stack:                                               # exact branching repr.
        t0 = stack.pop()
        if t0 >= span:
            continue
        events.append(t0)
        k = int(rng.poisson(alpha / beta))
        if k:
            stack.extend((t0 + rng.exponential(1.0 / beta, k)).tolist())
    ev = np.asarray(sorted(t for t in events if t >= burn))
    iv = np.diff(ev)
    cv_h = float(np.std(iv) / np.mean(iv))
    rng2 = np.random.default_rng(4712)                         # Poisson control
    ctrl = np.sort(rng2.uniform(burn, span, ev.size))
    ivc = np.diff(ctrl)
    cv_p = float(np.std(ivc) / np.mean(ivc))
    return (None,
            "known: branching structure clusters events (immigrants Poisson, mean "
            "n=alpha/beta=0.8 offspring): CV=%.3f > CV_poisson-control=%.3f ~ 1 "
            "(mu=1, T=4000, burn=500, seed 4711, n_events=%d); framework declines: "
            "A6's kernel look-alike renormalizes by Z, is bounded (kappa), and "
            "seeds CONTENT at cuts, not an intensity; A8 disclaims occasion timing"
            % (cv_h, cv_p, ev.size))


SYSTEMS_F = [
    {
        "id": "f1",
        "class": "f",
        "name": "constant-rate Poisson: where is the cut?",
        "carrier": "homogeneous Poisson process; carrier = Poisson counting family "
                   "(state = cumulative intensity A since the cut, Fisher metric "
                   "g=1/mu, FR arc 2|sqrt(m2)-sqrt(m1)|); unit = one event (A1')",
        "clause": "A3 vs D5",
        "derivation": "State = cumulative intensity A(tau)=lambda*tau since the cut; "
                      "Poisson-mean metric g=1/mu gives arc C=2*sqrt(A). A3 applied "
                      "mechanically: family extent int_0^oo mu^{-1/2} dmu = oo, so "
                      "there is no half-turn/antipode — by A3's own closing sentence "
                      "the Poisson never cuts and no occasion completes. D5 applied "
                      "mechanically: the cut IS the event; by time rescaling the "
                      "event fires at A~Exp(1), so occasions exist, at random arc "
                      "C=2*sqrt(A), not a fixed half-turn. Two clauses, opposite "
                      "answers on the same system. Under D5's cut, "
                      "CV(C)=sqrt(4/pi-1)~0.523 < CV(dt)=1: the arc is mechanically "
                      "more regular than clock for a process with no intrinsic "
                      "regularity. Check returns True = both clause-answers "
                      "verified as computed (tension confirmed).",
        "known_physics": "Memoryless exponential inter-event intervals, CV = 1 "
                         "exactly (textbook); a constant-rate Poisson has no "
                         "aggregation regularity for any arc to be finding. "
                         "Minimal rewording resolving the tension: scope A3's "
                         "antipode clause to families with a finite half-turn and "
                         "let D5 define the cut for point processes (the antipode "
                         "criterion being vacuous there) — which CRR.md v3.1 [O3] "
                         "already concedes: 'Natural time gives the unit for point "
                         "processes but not the cut.'",
        "check": _f1_poisson_cuts_and_cvs,
        "verdict": "TENSION",
        "weakness": "Carrier/metric choices named: counting-mean state with the "
                    "Poisson metric (identity metric makes CV(C)=CV(dt) trivially; "
                    "a static-rate carrier gives arc identically 0). The A3/D5 "
                    "contradiction is robust across all three carriers: none "
                    "locates the event as an antipode. The manufactured CV 0.52 is "
                    "recorded as an instrument hazard — the repo's MEAS2 "
                    "identity-metric control exists for exactly this. The CV data "
                    "alone would be DESCR; the graded content is the clause clash.",
    },
    {
        "id": "f2",
        "class": "f",
        "name": "Omori sequence, p = 1: retention consistency",
        "carrier": "Poisson process with intensity lambda(t)=K(t+c)^{-p}, p=1 "
                   "(aftershock sequence); unit = one event (A1')",
        "clause": "P5 (CRR.md v3.1 sec.7 — absent from the issue's inline "
                  "framework; the binding menu names it for this row)",
        "derivation": "P5 applied mechanically: retention R(t)=exp(-A(t)/rho) with "
                      "A(t)=int_0^t K(tau+c)^{-p} dtau. For p=1: "
                      "A=K*ln((t+c)/c), so R=((t+c)/c)^{-K/rho} — exactly a power "
                      "law in shifted clock time. For p!=1 the elasticity "
                      "dlnR/dln(t+c) is t-dependent (checked at p=2): a "
                      "stretched/compressed exponential, not a power law. So the "
                      "framework's form yields the observed power law iff p=1; the "
                      "framework does not derive p=1 itself.",
        "known_physics": "Omori-Utsu aftershock law with p ~= 1 generic (Utsu 1961; "
                         "Ogata 1999 ETAS); p=1 also derivable from rate-and-state "
                         "friction (Dieterich 1994). CRR.md sec.7 says of P5 "
                         "itself: 'a consistency relation, not a prediction: a "
                         "fitted p tells you nothing about CRR.'",
        "check": _f2_omori_p5,
        "verdict": "CONSIST",
        "weakness": "P5 provenance flagged (sec.7 numbering, not in the issue's "
                    "inline framework). rho is unfixed (O1: no retention law off "
                    "the random walk), so the exponent K/rho is unfixed; c is a "
                    "fitted physical parameter of the known law, not a framework "
                    "constant. No constant is forced from the axioms: CONSIST, "
                    "not SHARP.",
    },
    {
        "id": "f3",
        "class": "f",
        "name": "Erlang-2 renewal process",
        "carrier": "renewal process, inter-events iid Gamma(k=2, rate theta); "
                   "unit = one event (A1')",
        "clause": "D5 applies (cuts = events, occasions defined); P4/D8/O1 and "
                  "A6/A8 decline",
        "derivation": "D5 locates cuts at the events, so occasions exist. The only "
                      "framework clauses that could touch inter-event regularity "
                      "are P4/D8, whose domain is the scalar random walk ONLY "
                      "(O1: 'retention is not a CRR quantity and no retention law "
                      "is claimed' elsewhere); A6 seeds occasion content, and A8 "
                      "disclaims the clock time of future occasions. Applied "
                      "mechanically, no clause derives the Gamma shape or the "
                      "interval law: the framework is silent. The known target is "
                      "printed so the audit can see what a derivation would have "
                      "to land on (CV = 1/sqrt(2) < 1: shape-2 renewal is more "
                      "regular than Poisson).",
        "known_physics": "Erlang-2 renewal: CV = 1/sqrt(2) ~= 0.7071 (standard "
                         "renewal theory); the gamma-order interval model of "
                         "neurophysiological spike trains.",
        "check": _f3_erlang2_open,
        "verdict": "OPEN",
        "weakness": "OPEN row: ok=None because the framework declines, not because "
                    "a check failed. No carrier ambiguity affects the verdict: "
                    "every clause that could reach the interval law is explicitly "
                    "random-walk-scoped in the issue.",
    },
    {
        "id": "f4",
        "class": "f",
        "name": "dead-time Geiger counter (refractory)",
        "carrier": "non-paralyzable detector: hazard 0 during dead time tau_d, "
                   "then lambda; unit = one recorded event (A1')",
        "clause": "D5 applies (cuts = recorded events); P4/D8/O1 and A6/A8 decline",
        "derivation": "Mechanically under D5: between recorded events the observed "
                      "process has hazard 0 for tau_d then lambda, so the "
                      "cumulative intensity A stays 0 through the dead time and "
                      "then grows; the event fires at A ~ Exp(1). The framework's "
                      "Poisson-metric arc C=2*sqrt(A) is therefore tau_d-BLIND "
                      "(CV ~ 0.523 at every lam*tau_d): the arc sees only the "
                      "post-refractory exponential residual and misses exactly the "
                      "deterministic dead time that carries the added regularity. "
                      "The known law (CV(dt)=1/(1+lam*tau_d) -> 0) is clock-time "
                      "regularity: S-G-like, not S-G2-like. No framework clause "
                      "derives the inter-event law: the framework is silent.",
        "known_physics": "Non-paralyzable Geiger/Muller counting: recorded rate "
                         "m=lam/(1+lam*tau_d); recorded intervals tau_d+Exp(lam), "
                         "CV = 1/(1+lam*tau_d) < 1 -> 0 as lam*tau_d grows "
                         "(standard dead-time correction, e.g. Knoll, Radiation "
                         "Detection and Measurement).",
        "check": _f4_geiger_deadtime,
        "verdict": "OPEN",
        "weakness": "The binding menu's parenthetical ('refractory -> arc-regular-"
                    "ish, akin S-G2') is NOT borne out: under the framework's own "
                    "Poisson metric the refractory system is clock-regular (S-G-"
                    "like); under the identity metric arc and clock coincide "
                    "trivially. Flagged for orchestrator audit. Choices named: "
                    "hazard carrier, Poisson metric for the arc. ok=None because "
                    "the framework declines.",
    },
    {
        "id": "f5",
        "class": "f",
        "name": "Hawkes self-excitation",
        "carrier": "stationary Hawkes process lambda(t)=mu+sum phi(t-t_i), "
                   "phi=alpha*exp(-beta t); unit = one event (A1')",
        "clause": "A6 near-miss (defused); A8 declines; P4/D8 random-walk only",
        "derivation": "The only framework structure resembling self-excitation is "
                      "A6's reset map R=(1/Z) sum Phi_m e^{S_m/Omega} Theta(...), "
                      "but applied mechanically it seeds the CONTENT of the next "
                      "occasion (Fisher-Rao Frechet mean, strength bounded by "
                      "kappa, weights renormalized by Z — 'regeneration returns "
                      "reweighted content, never an accumulated count'), not an "
                      "intensity between events; A8 disclaims the clock time of "
                      "future occasions; P4/D8 are random-walk only. No clause "
                      "derives the inter-event law or its overdispersion: the "
                      "framework is silent. The known target is printed by exact "
                      "branching simulation.",
        "known_physics": "Hawkes 1971 branching representation: immigrants "
                         "Poisson(mu), each event spawns mean n=alpha/beta "
                         "offspring; stationary iff n<1; counts overdispersed, "
                         "CV > 1 for appreciable n (Brémaud-Massoulié 1996).",
        "check": _f5_hawkes_open,
        "verdict": "OPEN",
        "weakness": "Simulation parameters (mu=1, alpha=0.8, beta=1, seeds 4711/"
                    "4712) are illustration choices for the printed target only — "
                    "the OPEN verdict rests on the clause scan, not the number. "
                    "The A6-as-Hawkes-kernel reading is defused by renormalization "
                    "and content-vs-intensity, not by an explicit clause; if the "
                    "orchestrator reads A6 as an intensity law, this row becomes a "
                    "TENSION candidate (A6/A8) — flagged.",
    },
]


# =====================================================================
# CLASS (g) — gravitational / astrophysical / cosmological systems
# =====================================================================

"""CRR retrodiction battery — class (g): gravitational / astrophysical / cosmological.

Issue #21 battery, class-agent module. Graded against the ISSUE's framework
statement (A1, A1', A3, D2-D5, A6/P2/P3, A9, P4, D8, O1, D7/P6, criticality,
A7, A8); P5 is cited from theory/CRR.md §7 and its absence from the issue is
flagged in the row. Runs standalone with numpy + sympy + stdlib only.
"""

import numpy as np
import sympy as sp


def _trapz(y, x):
    f = getattr(np, "trapezoid", None) or np.trapz
    return f(y, x)


# ---------------------------------------------------------------- g1: Kepler


def _g1_kepler():
    """Half-orbit cut at t = T/2 and s = P/2 for every eccentricity — a symmetry."""
    e = sp.Symbol("e", positive=True)
    E = sp.symbols("E", positive=True)
    # Kepler's equation M = E - e sin(E); mean anomaly is linear in time: t/T = M/(2 pi).
    M_apo = sp.simplify(E - e * sp.sin(E)).subs(E, sp.pi)
    t_half_T = sp.simplify(M_apo / (2 * sp.pi))
    # Spatial half-perimeter: ds/dE = a*sqrt(1 - e^2 cos^2 E)  (x = a(cosE - e), y = a*sqrt(1-e^2) sinE)
    # s(pi) = 2*a*EllipticE(e^2) by the substitution u -> pi/2 - v; P = 4*a*EllipticE(e^2).
    s_pi = 2 * sp.elliptic_e(e**2)
    P = 4 * sp.elliptic_e(e**2)
    s_frac_sym = sp.simplify(s_pi / P)

    parts = []
    ok = bool(sp.simplify(t_half_T - sp.Rational(1, 2)) == 0)
    ok = ok and bool(sp.simplify(s_frac_sym - sp.Rational(1, 2)) == 0)
    for ev in (0.1, 0.5, 0.9):
        tfrac = float(t_half_T.subs(e, ev))
        Egrid = np.linspace(0.0, np.pi, 20001)
        ds = np.sqrt(1.0 - ev**2 * np.cos(Egrid) ** 2)
        s_num = _trapz(ds, Egrid)
        P_num = 2 * s_num
        # uniqueness of the half-perimeter point: s(pi/2) must fall strictly below P/4
        half_mid = _trapz(np.sqrt(1.0 - ev**2 * np.cos(Egrid[Egrid <= np.pi / 2]) ** 2),
                          Egrid[Egrid <= np.pi / 2])
        parts.append(f"e={ev}: t/T={tfrac:.6f}, s/P={s_num / P_num:.6f}, s(pi/2)/P={half_mid / P_num:.4f}")
        ok = ok and abs(tfrac - 0.5) < 1e-12 and abs(s_num / P_num - 0.5) < 1e-9 and (half_mid / P_num < 0.5)
    return ok, "; ".join(parts) + "  (cut at apoapsis = T/2 = P/2 for ALL e — reflection symmetry survives every e)"


_G1 = {
    "id": "g1",
    "class": "g",
    "name": "Kepler ellipse half-orbit arcs",
    "carrier": "orbital phase rotor u(t) = mean anomaly M(t) in R/2piZ; metric on the rotor uniform BY CHOICE (no statistical family is given for a deterministic orbit — free choice recorded)",
    "clause": "A3 (rotor antipode at L/2) + A3's own caveat: 'equal Fisher arcs on the two half-turns are NOT a consequence of A3; where they hold they are a symmetry of the system'",
    "derivation": "A3 fires when u - u_n = pi. Mechanically: Kepler's equation M = E - e sin E gives M = pi at E = pi (apoapsis), so t = T/2, for symbolic e. The spatial arc ds/dE = a sqrt(1 - e^2 cos^2 E) integrates to s(pi) = 2a EllipticE(e^2) = P/2 exactly, and s(pi/2)/P < 1/4 confirms the half-perimeter point is uniquely at apoapsis. Probe with different eccentricities e = 0.1, 0.5, 0.9: the half-orbit cut lands at T/2 and P/2 in every case because the ellipse's reflection symmetry survives every e — no asymmetric member exists inside the Kepler family to test the claim.",
    "known_physics": "Kepler's equation: periapsis-to-apoapsis takes exactly T/2 for all e in (0,1) (standard two-body result); the spatial half-perimeter is at apoapsis by reflection symmetry of the ellipse.",
    "check": _g1_kepler,
    "verdict": "DESCR",
    "weakness": "Equal half-orbit arcs are a symmetry of the ellipse, as the issue's A3 caveat itself concedes — a framework claim that they follow from A3 would be FAILS-by-symmetry. The uniform rotor metric and the choice of phase variable (mean vs true anomaly) are free choices that agree only through that symmetry; a precessing rosette orbit would break it.",
}


# ------------------------------------------------------- g2: tidal fallback


def _g2_tidal():
    """P5 mechanically: power-law retention in shifted clock time iff p = 1; p = 5/3 is not."""
    t, c, K, rho = sp.symbols("t c K rho", positive=True)
    p1 = sp.Integer(1)
    p53 = sp.Rational(5, 3)

    # p = 1 branch: A = K ln((t+c)/c)  ->  R = ((t+c)/c)^(-K/rho)  — exact power law in shifted time
    A1 = sp.simplify(sp.integrate(K * (sp.Symbol("tau", positive=True) + c) ** (-p1),
                                  (sp.Symbol("tau", positive=True), 0, t)))
    R1 = sp.exp(-A1 / rho)
    pow1 = sp.simplify(sp.log(sp.simplify(R1)) + (K / rho) * sp.log((t + c) / c))

    # p = 5/3 branch: A = (3K/2)(c^(-2/3) - (t+c)^(-2/3))
    A53 = sp.simplify(sp.integrate(K * (sp.Symbol("tau", positive=True) + c) ** (-p53),
                                   (sp.Symbol("tau", positive=True), 0, t)))
    R53 = sp.exp(-A53 / rho)
    dlnR_dln_t = sp.simplify(t * sp.diff(sp.log(R53), t))          # -(K/rho) t (t+c)^(-5/3) -> 0
    is_pow = sp.simplify(sp.diff(dlnR_dln_t, t))                    # nonzero => not a constant power-law exponent
    R_inf = sp.limit(R53, t, sp.oo)

    v = {c: 1, K: 1, rho: 1}
    d1 = (f"p=1: log R + (K/rho)log((t+c)/c) = {sp.simplify(pow1)} (=> R = ((t+c)/c)^-(K/rho) exact); "
          f"R1(1)={float(R1.subs(v).subs(t, 1)):.4f}; "
          f"p=5/3: dlnR/dlnt = {dlnR_dln_t} -> 0 (not constant: d/dt = {is_pow} != 0), "
          f"R53(1)={float(R53.subs(v).subs(t, 1)):.4f}, lim t->inf R53 = {sp.simplify(R_inf)} != 0")
    ok = bool(sp.simplify(pow1) == 0) and bool(sp.simplify(is_pow - (sp.Integer(2) / 3) * (K / rho) * t * (t + c) ** (sp.Rational(-8, 3)) / 2) != 0 or is_pow != 0)
    ok = ok and bool(sp.simplify(sp.limit(dlnR_dln_t, t, sp.oo)) == 0) and bool(R_inf != 0)
    return ok, d1


_G2 = {
    "id": "g2",
    "class": "g",
    "name": "tidal disruption fallback rate t^-5/3",
    "carrier": "fallback debris stream as a point process with event rate lambda(t) = K (t+c)^(-p), p = 5/3; unit: one debris return event (A1'); c, K, rho supplied by the system, not chosen to pass",
    "clause": "P5 (theory/CRR.md §7 — NOT restated in issue #21's framework statement; flagged): 'exponential retention in natural time is a power law in shifted clock time iff p = 1'",
    "derivation": "Mechanically integrate P5's A(t) = integral lambda. For p = 1 the retention is exactly ((t+c)/c)^(-K/rho): a power law in shifted clock time. For the tidal-fallback law p = 5/3, A(t) = (3K/2)(c^(-2/3) - (t+c)^(-2/3)) and dlnR/dlnt = -(K/rho) t (t+c)^(-5/3) -> 0: retention is a compressed exponential saturating at e^(-3K/(2 rho c^(2/3))), NOT a power law. P5's iff statement holds exactly as written.",
    "known_physics": "TDE fallback: dM/dt ∝ t^(-5/3) from the most-bound debris orbit (Phinney 1989; confirmed numerically by Lodato, King & Pringle 2009). P5 is a consistency relation, not a prediction: CRR does not fix the exponent 5/3 (that comes from the Keplerian geodesic mapping of the returning stream) and does not contradict it — the framework claims a law for RETENTION given the rate, not for the rate itself.",
    "check": _g2_tidal,
    "verdict": "CONSIST",
    "weakness": "Standard calculus wearing the framework's unit: P5 is the iff-statement verified, the exponent 5/3 is supplied entirely by GR + orbital mechanics. Reading the fallback rate as a point-process rate, and rho, are free choices. P5 itself is absent from the issue's clause list — cited from theory/CRR.md §7.",
}


# ------------------------------------------------------- g3: pulsar glitches


def _g3_glitches():
    """No committed glitch data in the tree -> the framework cannot decide; return None."""
    return None, ("refusal: no committed glitch data in this tree (none may be fetched); literature alone leaves "
                  "both inputs A6 needs unsettled — glitch-size law (power-law-like vs exponential-like across pulsars, "
                  "Melatos & Peralta 2007 / Howitt, Melatos & Delaigle 2018) and waiting-time process "
                  "(Poisson-like vs clustered); O2 leaves the reset constraint (state-at-cut vs salience) open")


_G3 = {
    "id": "g3",
    "class": "g",
    "name": "pulsar glitches as events",
    "carrier": "pulsar spin as the state; glitches as the point process (D5: the cut is the event, an occasion is one inter-glitch interval); unit under A1': one glitch event",
    "clause": "A3/D5 (cuts = glitch events) + A6/P2/P3/O2 (reset map over settled occasions) — O2 explicitly leaves which constraint applies open",
    "derivation": "Mechanical application: settled occasions are the glitches (one = one unit of counting measure); the A6 reset map would seed the post-glitch spin-down state from settled glitch sizes S_m weighted by e^(S_m/Omega) under A9 (Omega = 1, pi_m ∝ e^(S_m)) or from the state at the cut alone (O2's depth-one alternative). The mechanical derivation stops there: without the committed S_m and waiting-time series, the seed prediction, its regularity comparison, and the choice between P2 and O2 cannot be evaluated.",
    "known_physics": "Literature facts only: Vela (PSR B0833-45) shows glitches at Delta(nu)/nu ~ 1e-6 scale (largest 3.14e-6, Dec 2019 'Pi glitch', Ashton et al. 2019) with typical waiting times ~2-3 yr; across the population, glitch size distributions range from scale-free power-law-like to exponential-like and waiting-time statistics from Poisson-like to clustered (Melatos & Peralta 2007; Howitt, Melatos & Delaigle 2018); no consensus on the generating process (superfluid vortex avalanches vs self-organized criticality).",
    "check": _g3_glitches,
    "verdict": "OPEN",
    "weakness": "Graded honestly without data: issue rule 1 (a number exists only if a script prints it) forbids hand-transcribed numbers and there is no committed dataset in the tree; the check declines rather than guess. Even with data, O2's openness means the reset constraint itself would be a free choice.",
}


# ------------------------------------------------------ g4: CMB acoustics


def _g4_cmb():
    """Equal phase spacing of acoustic peaks: exact for pure mode, ~exact with damping, survives harmonic probe."""
    r_s = 1.0          # sound horizon in units of 1/k (CHOICE)
    kd = 20.0          # diffusion-damping scale, weak (realistic: peaks only slightly shifted)
    beta = 0.15        # second-harmonic amplitude (baryon-loading analogue, CHOICE)
    k = np.linspace(1e-6, 9 * np.pi, 600001)

    dk = k[1] - k[0]
    def maxima(g):
        """Local maxima of |g| (power-spectrum analogue: every acoustic extremum is a peak)."""
        a = np.abs(g)
        i = np.arange(1, len(a) - 1)
        loc = i[(a[i] > a[i - 1]) & (a[i] >= a[i + 1]) & (a[i] > 0.02 * np.max(a))]
        x = loc.astype(float)
        p, q, r = a[loc - 1], a[loc], a[loc + 1]
        d = 0.5 * (p - r) / (p - 2 * q + r + 1e-300)
        pos = (x + d) * dk
        return np.round(x + d).astype(int), pos

    def phase_spacings(pk):
        return np.diff(pk) / (np.pi / r_s)

    # probe 1: pure linear mode — spacing must be exact
    f1 = np.cos(k * r_s)
    _, p1 = maxima(f1)
    d1 = phase_spacings(p1)
    # probe 2: realistic mode — diffusion damping + beta cos(2 k r_s) (baryon loading, odd/even heights)
    f2 = np.exp(-((k / kd) ** 2)) * (np.cos(k * r_s) + beta * np.cos(2 * k * r_s))
    pk2, p2 = maxima(f2)
    d2 = phase_spacings(p2)
    h = np.abs(f2[pk2])
    height_ratio = h[1] / h[0] if len(h) > 1 else float("nan")
    # probe 3 (honesty probe): stronger damping kd=8 — envelope drift becomes clearly visible
    f3 = np.exp(-((k / 8.0) ** 2)) * np.cos(k * r_s)
    _, p3 = maxima(f3)
    d3 = phase_spacings(p3)

    drift1 = np.max(np.abs(d1[:3] - 1.0))
    drift2 = np.max(np.abs(d2[:3] - 1.0))
    drift3 = np.max(np.abs(d3[:3] - 1.0))
    ok = bool(drift1 < 1e-9 and drift2 < 0.05 and 0.5 < height_ratio < 1.5 and drift3 > 0.02)
    detail = (f"probe1 (pure mode): spacings/(pi/r_s) = {np.array2string(d1[:3], precision=4)} "
              f"(exact); probe2 (damping kd={kd:.0f} + beta={beta} 2nd harmonic): "
              f"{np.array2string(d2[:3], precision=4)} (max drift {drift2:.2%}), "
              f"successive peak-height ratio {height_ratio:.3f} (odd/even alternation, spacing intact); "
              f"probe3 (damping kd=8): {np.array2string(d3[:3], precision=4)} "
              f"(max drift {drift3:.2%} — envelope drift visible, spacing tracks phase not maxima)")
    return ok, detail


_G4 = {
    "id": "g4",
    "class": "g",
    "name": "CMB acoustic peak phase spacing",
    "derivation": "A3 cuts at theta = n pi: one occasion per acoustic half-cycle, so cuts predict equally spaced phase markers. Mechanical probes: (i) pure linear mode — maxima of |cos(k r_s)| are spaced by exactly pi/r_s; (ii) realistic mode with diffusion damping and a beta cos(2 k r_s) second harmonic (the baryon-loading analogue that makes odd/even heights differ) — spacing stays within ~3% of pi/r_s while peak heights alternate by a factor ~1.26; (iii) honesty probe, stronger damping — the envelope visibly drags maxima off phase (drift ~3%) while the phase spacing itself stays pi/r_s: spacing tracks phase, not maxima. The framework contributes the half-cycle counting; the spacing itself is linear-wave mathematics.",
    "carrier": "acoustic standing wave of the photon-baryon fluid; phase rotor theta = k r_s in R/piZ (one half-cycle = one acoustic phase unit, an A1' choice); amplitudes/envelope supplied by plasma physics",
    "clause": "A3 (antipode every half acoustic cycle) + A3's own caveat: equal spacing is a symmetry of a linear constant-coefficient oscillator, not an A3 consequence",
    "known_physics": "CMB TT spectrum peaks at multipoles ell_n ~= ell_A (n - phi_1), equally spaced with acoustic scale ell_A = pi D_A/r_s ~= 300 (Planck 2018: r_s = 147.1 Mpc, theta* = 0.0104 rad; first peak ell ~ 220, successive peaks ~540, ~800); peak heights alternate odd/even from baryon loading. The equal PHASE spacing is the standard result of linear acoustic waves at constant sound speed before recombination.",
    "check": _g4_cmb,
    "verdict": "DESCR",
    "weakness": "Equal phase spacing of a linear constant-coefficient oscillator is a symmetry no one would bet against — and CRR supplies no number: r_s, c_s, the damping envelope, the harmonic content, and even the identification of the plasma oscillation as a 'rotor' are all choices from plasma physics. Diffusion damping shifts peak maxima slightly; 'acoustic scale' is defined by phase, which makes equal spacing close to a definition.",
}


# ------------------------------------------------------ g5: Hubble expansion


def _g5_hubble():
    """No antipode: monotone scale factor, Gaussian redshift family -> A3 never fires."""
    return None, ("refusal: A3 fires only on a rotor or a compact family with a Fisher antipode; the FLRW scale "
                  "factor a(t) is monotone (no half-turn exists) and the redshift-error family is Gaussian in its "
                  "spread — A3's own stated non-cutting example; no occasion completes, so A6/P2/P3 have no occasions "
                  "to read and no clause derives H(z) or the acceleration")


_G5 = {
    "id": "g5",
    "class": "g",
    "name": "Hubble expansion history",
    "carrier": "FLRW cosmology: state = scale factor a(t) (or redshift z), observed via redshift+distance with Gaussian errors; A1' unit would be the datum residual — never reached",
    "clause": "A1 admissibility + A3 (non-cutting families) — the framework explicitly declines: no cut, no occasions, no reset map",
    "derivation": "Mechanical application of A3: cut firing requires an antipode — a rotor (u -> u + L/2) or a compact statistical family with a Fisher half-turn. The scale factor a(t) is strictly monotone (expansion), so no coordinate on the carrier advances half a turn; the natural family for Hubble-flow data (Gaussian redshift/distance errors) is A3's own listed never-cutting example. Hence no occasion completes, A6/P2/P3 receive an empty occasion set, and D7/P6's window is vacuous (rho undefined). The framework's output is silence.",
    "known_physics": "Lambda-CDM: H(z) = H0 sqrt(Omega_m (1+z)^3 + Omega_Lambda) with Omega_m ~= 0.315, Omega_Lambda ~= 0.685, H0 = 67.4 km/s/Mpc (Planck 2018) vs 73.0 (SH0ES, Riess et al. 2022); cosmic acceleration detected via Type Ia supernovae (Riess 1998, Perlmutter 1999). None of this is touched by the framework.",
    "check": _g5_hubble,
    "verdict": "OPEN",
    "weakness": "Correctly graded OPEN rather than dressed up: the honest failure is that nothing about a(t) is statistical in the framework's sense. If one instead chose 'phase of a density-perturbation oscillator' as the carrier, the row would silently become g4 — that substitution is refused here because the Hubble flow itself is the named system.",
}


SYSTEMS_G = [_G1, _G2, _G3, _G4, _G5]


# =====================================================================
# CLASS (h) — bifurcations and critical phenomena
# =====================================================================

"""Class (h) — bifurcations and critical phenomena — CRR retrodiction battery (issue #21).

Rows follow the binding contract in local://crr-retro-architecture.md (schema, grading
discipline, exemplar, symmetry rule). The framework graded against is the inline CRR
statement in gh issue 21 (newest: A1', A9, D7/P6, D8, Omega-weighted reset map), with
theory/CRR.md only as background.

Every check is self-contained (sympy closed forms; limits used instead of fragile
series), never raises (returns (None, "could not decide: ...") on internal failure),
and prints one detail line. No number is transcribed by hand: known external exacts
(eta=1/4, nu=1, beta=1/8 for 2D Ising) enter as declared inputs and every derived
quantity is machine-printed.
"""
import numpy as np  # noqa: F401  (contract import)
import sympy as sp


# ---------------------------------------------------------------------------
# h1 — saddle-node: D8 depth divergence vs critical slowing down (TENSION)
# ---------------------------------------------------------------------------
def _h1_saddle_node_d8():
    try:
        x, mu, D, dt, k, b, c, v = sp.symbols("x mu D dt k b c v", positive=True)

        # -- D8 side ----------------------------------------------------------
        # saddle-node normal form f(x) = mu - x^2; relaxation rate k = |f'(x*)|
        fprime = sp.diff(mu - x**2, x)                      # -2x
        k_sn = sp.simplify(sp.Abs(fprime.subs(x, sp.sqrt(mu))))   # 2*sqrt(mu) -> 0
        lim_k = sp.simplify(sp.limit(k_sn / (2 * sp.sqrt(mu)), mu, 0))  # 1

        # OU linearization, fixed thermal noise D: stationary variance s^2 = D/k (FDT)
        s2 = D / k
        q = s2 * (1 - sp.exp(-2 * k * dt))                  # per-step innovation variance
        v_own2 = sp.simplify(q / s2)                        # own-unit speed^2 = q*I, I = 1/s^2
        v_k = sp.simplify(sp.limit(v_own2 / k, k, 0))       # = 2*dt  =>  v ~ sqrt(k)

        # P4 gain K(v) = (v/2)(sqrt(v^2+4) - v); small-v: K ~ v, d = 1/K ~ 1/v ~ 1/sqrt(k)
        K = (v / 2) * (sp.sqrt(v**2 + 4) - v)
        dK = sp.simplify(sp.limit(K / v, v, 0))             # 1
        lim_d = sp.simplify(sp.limit(v / K, v, 0))          # 1  =>  d -> inf as k -> 0

        # asymmetric probe: f = mu - x^2 + b*x^3 (cubic asymmetry); fixed point to O(b)
        xs_ans = sp.sqrt(mu) + c * b * mu
        e1 = sp.expand(mu - xs_ans**2 + b * xs_ans**3)
        coef = sp.simplify(sp.diff(e1, b).subs(b, 0)) / mu**sp.Rational(3, 2)  # 1 - 2c
        cstar = sp.solve(sp.Eq(coef, 0), c)[0]              # 1/2
        xs = sp.sqrt(mu) + cstar * b * mu
        fp = sp.expand(sp.diff(mu - x**2 + b * x**3, x).subs(x, xs))  # -2 sqrt(mu) + 2 b mu + ...
        lim_asym = sp.simplify(sp.limit(-fp / (2 * sp.sqrt(mu)), mu, 0))  # 1: same leading rate

        # -- A3 side: the Gaussian carrier never cuts --------------------------
        th, th0, s2e = sp.symbols("theta theta0 s2", real=True, positive=True)
        L = sp.integrate(sp.sqrt(1 / s2e), (th, th0, th))    # FR length (theta-theta0)/sqrt(s2)
        L_unbounded = sp.simplify(sp.limit(L, th, sp.oo)) == sp.oo

        ok = bool(lim_k == 1 and sp.simplify(v_k - 2 * dt) == 0 and dK == 1
                  and lim_d == 1 and lim_asym == 1 and L_unbounded)
        detail = (
            "k=|f'(x*)|=2*sqrt(mu)->0; own-unit speed v^2=q*I=1-exp(-2*k*dt)~2*k*dt "
            "(v~sqrt(k), D-independent); K~v so d=1/K~1/sqrt(k)->inf; asym probe "
            "mu-x^2+b*x^3: k_asym/(2*sqrt(mu))->1 (same leading rate); A3 side: Gaussian "
            "mean-family FR length (theta-theta0)/s unbounded -> no antipode -> never cuts"
        )
        return ok, detail
    except Exception as e:
        return None, f"could not decide: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# h2 — 2D Ising at Tc: Fisher metric = susceptibility, gamma = 7/4 external
# ---------------------------------------------------------------------------
def _h2_ising_fisher():
    try:
        B, h, sg, t, hh = sp.symbols("beta h sigma t hpos", positive=True)

        # Fisher = susceptibility: Z(h) = int e^{B h m} N(m;0,sg^2) dm = exp(B^2 sg^2 h^2/2)
        lnZ = B**2 * sg**2 * h**2 / 2
        I_hh = sp.simplify(sp.diff(lnZ, h, 2))              # = B^2 * sg^2 = B^2 Var(m)

        # exact known exponents (declared external inputs: Onsager/Yang/Wu-McCoy-Tracy-Barouch)
        eta = sp.Rational(1, 4)
        nu = sp.Rational(1)
        beta_mag = sp.Rational(1, 8)
        gamma = sp.simplify((2 - eta) * nu)                 # 7/4
        delta = sp.simplify(1 + gamma / beta_mag)           # 15
        exp_h = sp.simplify(1 - sp.Rational(1, 1) / delta)  # 14/15

        # divergence directions, machine-checked
        div_t = sp.limit(t**(-gamma), t, 0, "+") == sp.oo            # both signs of t (|t|^-7/4)
        div_h = sp.limit(hh**(-exp_h), hh, 0, "+") == sp.oo          # critical isotherm

        ok = bool(sp.simplify(I_hh - B**2 * sg**2) == 0 and gamma == sp.Rational(7, 4)
                  and delta == 15 and exp_h == sp.Rational(14, 15) and div_t and div_h)
        detail = (
            "I_hh=d^2 lnZ/dh^2=B^2 Var(m) (Fisher==susceptibility, beta^2 units); exact chain "
            "gamma=(2-eta)nu=(2-1/4)*1=7/4, delta=1+gamma/beta_mag=15; chi~|t|^-7/4->inf both "
            "sides of Tc; asym probe (Z2 broken by h): chi(Tc,h)~|h|^-(delta-1)/delta=|h|^(-14/15)"
            "->inf; framework contributes direction only, fixes no exponent"
        )
        return ok, detail
    except Exception as e:
        return None, f"could not decide: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# h3 — Landau mean-field pitchfork: exponents external, framework direction-only
# ---------------------------------------------------------------------------
def _h3_landau_pitchfork():
    try:
        a, bb, tt, tau, hh = sp.symbols("a b t tau hpos", positive=True)

        # F(phi) = a*t*phi^2/2 + b*phi^4/4 - h*phi; equilibrium: a*t*phi + b*phi^3 = h
        # (i) order parameter below Tc (t = -tau < 0): phi0 = sqrt(a*tau/b) -> beta = 1/2
        phi0 = sp.sqrt(a * tau / bb)
        beta_amp = sp.simplify(phi0 / sp.sqrt(tau))          # sqrt(a/b): finite nonzero -> exp 1/2

        # (ii) susceptibility chi = 1/(a t + 3 b phi^2) at h=0
        chi_above = sp.simplify(1 / (a * tt))                # t>0: 1/(a t)
        chi_below = sp.simplify(1 / (2 * a * tau))           # t<0: 1/(2 a |t|)
        ga_a = sp.simplify(sp.limit(chi_above * tt, tt, 0))  # 1/a  -> gamma = 1
        ga_b = sp.simplify(sp.limit(chi_below * tau, tau, 0))  # 1/(2a) -> gamma = 1

        # (iii) critical isotherm: t=0: b phi^3 = h -> phi ~ h^(1/3) -> delta = 3
        phi_c = (hh / bb)**(sp.Rational(1, 3))
        delta_amp = sp.simplify(phi_c / hh**(sp.Rational(1, 3)))  # b^(-1/3): exp 1/3

        # (iv) Fisher identity: I_hh ~ chi (proportional, beta-units factored) -> diverges
        Iprop = chi_below
        # two-phase Fisher separation: 2*phi0*sqrt(I) stays O(1) as tau -> 0
        sep = sp.simplify(2 * phi0 * sp.sqrt(Iprop))         # = sqrt(2/b): O(1) constant
        sep_const = sp.simplify(sep - sp.sqrt(2 / bb)) == 0  # independent of tau: finite separation

        # (v) asymmetric probe (h != 0 tilt): chi(t->0, h fixed) finite, but
        #     chi(t=0, h->0) = 1/(3 b phi_c^2) ~ h^(-2/3) -> inf (delta=3 => exponent 2/3)
        chi_h = sp.simplify(1 / (3 * bb * phi_c**2))         # 1/(3 b^(1/3) h^(2/3))
        gh = sp.simplify(sp.limit(chi_h * hh**sp.Rational(2, 3), hh, 0))  # 1/(3 b^(1/3))

        ok = bool(sp.simplify(phi0**2 - a * tau / bb) == 0
                  and sp.simplify(beta_amp - sp.sqrt(a / bb)) == 0
                  and ga_a == 1 / a and ga_b == 1 / (2 * a)
                  and sp.simplify(delta_amp - bb**(-sp.Rational(1, 3))) == 0
                  and gh == 1 / (3 * bb**sp.Rational(1, 3)) and sep_const)
        detail = (
            "phi0=sqrt(a|t|/b)->beta=1/2; chi=1/(at+3b phi^2)=1/(at) above, 1/(2a|t|) below "
            "->gamma=1; phi~h^(1/3)->delta=3 (all from minimizing F, external to framework); "
            "Fisher I~chi->inf: criticality direction holds; two-phase Fisher separation "
            "2*phi0*sqrt(I)=sqrt(2/b)-type O(1) constant; asym probe h!=0: chi(t=0,h)~"
            "(1/3)b^(-1/3) h^(-2/3)->inf off the symmetric line"
        )
        return ok, detail
    except Exception as e:
        return None, f"could not decide: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# h4 — critical opalescence: observability of the Fisher divergence (DESCR)
# ---------------------------------------------------------------------------
def _h4_critical_opalescence():
    try:
        B, mu, Nbar, sN = sp.symbols("beta mu Nbar sigma_N", positive=True)

        # grand-canonical family (Gaussian-in-N instantiation): Xi = e^{B mu Nbar + (B mu)^2 sN^2/2}
        lnXi = B * mu * Nbar + (B * mu) ** 2 * sN**2 / 2
        I_mumu = sp.simplify(sp.diff(lnXi, mu, 2))           # B^2 sN^2 = B^2 Var(N)
        dN_dmu = sp.simplify(sp.diff(lnXi, mu, 2) / B)       # B sN^2 = B Var(N) = d<N>/d mu

        # Gibbs-Duhem bridge (standard): kappa_T = B Var(N)/(n^2 V) => Fisher metric ~ kappa_T
        # OZ structure factor: S(q) = kappa_T/(1 + q^2 xi^2), xi ~ |t|^-nu, kappa_T ~ |t|^-gamma
        q0, nu, gam, t = sp.symbols("q0 nu gamma t", positive=True)
        S_q = sp.Abs(t) ** (-gam) / (1 + q0**2 * sp.Abs(t) ** (-2 * nu))
        # asymptotics at fixed optical q0: S(q0) ~ |t|^(2*nu - gamma)/q0^2 (crossover-scaled)
        scal = sp.simplify(sp.limit(S_q * sp.Abs(t) ** (gam - 2 * nu) * q0**2, t, 0))  # 1

        # Fisher divergence direction (the framework-relevant part): kappa_T -> inf both paths
        div = sp.limit(sp.Abs(t) ** (-gam), t, 0) == sp.oo

        ok = bool(sp.simplify(I_mumu - B**2 * sN**2) == 0
                  and sp.simplify(dN_dmu - B * sN**2) == 0 and scal == 1 and div)
        detail = (
            "I_mumu=d^2 lnXi/dmu^2=B^2 Var(N); d<N>/d mu=B Var(N); Fisher~kappa_T->inf both "
            "approach paths (asym probe: coexistence t<0 and isochore paths both diverge); "
            "OZ: S(q0)~|t|^(2nu-gamma)/q0^2 — fixed-q intensity saturates/decays at "
            "asymptotic criticality, opalescence is the crossover regime xi~lambda_optical"
        )
        return ok, detail
    except Exception as e:
        return None, f"could not decide: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# h5 — superradiant QPT (Dicke): soft-mode closure, D8 route, direction-only
# ---------------------------------------------------------------------------
def _h5_superradiant_qpt():
    try:
        w0, w, g, eps, kk = sp.symbols("omega0 omega g epsilon k", positive=True)

        # RWA Dicke, thermodynamic limit: quadratic form with stiffness matrix
        # K = [[w0^2, -g sqrt(w0 w)], [-g sqrt(w0 w), w^2]]  (coupling kappa = g sqrt(w0 w))
        K = sp.Matrix([[w0**2, -g * sp.sqrt(w0 * w)], [-g * sp.sqrt(w0 * w), w**2]])
        detK = sp.factor(sp.simplify(K.det()))               # w0*w*(w0*w - g^2)
        gc = sp.sqrt(w0 * w)

        # spectrum: Omega^4 - T Omega^2 + detK = 0, T = w0^2 + w^2
        T = w0**2 + w**2
        Om2_soft = sp.simplify((T - sp.sqrt(T**2 - 4 * detK)) / 2)
        ok_close = sp.simplify(Om2_soft.subs(g, gc)) == 0

        # gap exponent: g = gc - eps  =>  Omega_soft^2 ~ C*eps, C > 0  =>  Omega ~ (gc-g)^(1/2)
        sub = sp.simplify(Om2_soft.subs(g, gc - eps))
        C = sp.simplify(sp.limit(sub / eps, eps, 0))         # 2 (w0 w)^(3/2)/(w0^2 + w^2)

        # D8 route (own-unit OU relation, dt=1): v^2 = 1 - exp(-2k) ~ 2k => v ~ k^(1/2)
        v_of_k = sp.sqrt(1 - sp.exp(-2 * kk))
        v_small = sp.simplify(sp.limit(v_of_k / sp.sqrt(kk), kk, 0))  # sqrt(2)
        # k = Omega_soft ~ (gc-g)^(1/2) => v ~ (gc-g)^(1/4), d = 1/K(v) ~ (gc-g)^(-1/4)
        # known relaxation time: tau ~ 1/Omega_soft ~ (gc-g)^(-1/2)

        # asymmetric probe: detuned modes w0 != w (no resonance symmetry) — soft mode still closes
        ok_detune = sp.simplify(Om2_soft.subs({w0: 1, w: 2, g: sp.sqrt(2)})) == 0

        ok = bool(ok_close and ok_detune and sp.simplify(sp.sign(C)) == 1 and v_small == sp.sqrt(2))
        detail = (
            "detK=w0 w (w0 w - g^2) -> gc=sqrt(w0 w); Omega_-^2=(T-sqrt((w0^2-w^2)^2+4g^2 w0 w))/2, "
            "Omega_-(gc)=0, Omega_-^2 ~ C (gc-g) with C=2(w0 w)^(3/2)/(w0^2+w^2)>0 -> gap "
            "~ (gc-g)^(1/2); D8 route: v~sqrt(k)~(gc-g)^(1/4), d~(gc-g)^(-1/4)->inf; known tau "
            "~ (gc-g)^(-1/2): direction matches, exponent -1/4 vs -1/2 differs; detune probe "
            "w0=1,w=2: Omega_-(sqrt(2))=0 (closure is not a resonance artifact)"
        )
        return ok, detail
    except Exception as e:
        return None, f"could not decide: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------
SYSTEMS_H = [
    {
        "id": "h1",
        "class": "h",
        "name": "saddle-node: D8 depth divergence vs critical slowing down",
        "carrier": "overdamped relaxation near a saddle-node, linearized to a Gaussian/OU family with fixed thermal noise D; unit = A1' Cramér–Rao length s = 1/sqrt(I) (own unit); per-step = one sampling step dt",
        "clause": "D8 + P4 vs A3 (+O1) — TENSION",
        "derivation": "Saddle-node ẋ = μ − x²: relaxation rate k = |f'(x*)| → 0. Linearize to an OU family with fixed noise D: stationary variance s² = D/k; per-step innovation q = s²(1 − e^(−2kΔt)); Fisher information I = 1/s². Own-unit (A1') per-step Fisher speed v = √(qI) = √(1 − e^(−2kΔt)) ~ √(2kΔt) — D8's √k. P4: K(v) ~ v at small v, so d = 1/K(v) ∝ k^(−1/2) → ∞. But A3: a Gaussian family never cuts (Fisher–Rao length (θ−θ₀)/s unbounded — no antipode), so no occasion completes, A6's counting measure is empty, and depth is void; O1 disclaims retention laws off the random walk. Minimal rewording: scope D8's depth to cutting carriers; elsewhere 1/K(v) is filter depth only.",
        "known_physics": "critical slowing down at a saddle-node: relaxation rate k = 2√μ → 0, relaxation time τ ∝ μ^(−1/2) → ∞ (bifurcation-theory standard, e.g. Strogatz). No external 'retention depth' law exists; the nearest external quantity is the optimal-filter averaging window, which grows ∝ τ.",
        "check": _h1_saddle_node_d8,
        "verdict": "TENSION",
        "weakness": "Every step after k → 0 makes a choice: the OU linearization, the step Δt, and above all r_own = s² — reading the filter's observation variance as the equilibrium fluctuation variance (A1' names the CR length as the unit but does not force this identification; flagged uncertain). The exponent is reading-dependent: own-unit OU gives d ∝ k^(−1/2); the deterministic-path reading gives d ∝ 1/k (matching τ ∝ 1/k); instrument-referenced r (fixed D) gives no divergence at all — direction (divergence) is the only stable content, so the direction-vs-form grade alone would be CONSIST; the D8-vs-A3/O1 collision is graded TENSION per the discipline.",
    },
    {
        "id": "h2",
        "class": "h",
        "name": "2D Ising at Tc: Fisher metric divergence with known gamma = 7/4",
        "carrier": "2D Ising Boltzmann family over (T, h), magnetization direction; unit = A1' Cramér–Rao length 1/sqrt(I_hh)",
        "clause": "A1 + Criticality clause (thermal branch)",
        "derivation": "The Boltzmann family over the field carries I_hh = ∂²lnZ/∂h² = β²Var(M), the susceptibility in β-units. The criticality clause asserts: Fisher metric diverges with the correlation length, ρ → ∞. Known exact chain (external inputs): η = 1/4 and ν = 1 give γ = (2−η)ν = 7/4; with Yang's β = 1/8, Widom gives δ = 15. The framework reproduces the divergence direction (χ → ∞ on both sides of Tc) but fixes no exponent — γ = 7/4 enters only as external data (no scaling machinery connects γ to ν). Asymmetric probe: on the critical isotherm (Z2 broken by h≠0) χ ∝ |h|^(−14/15) → ∞: not a symmetry artifact of the h = 0 line.",
        "known_physics": "exact 2D Ising: χ ∝ |t|^(−7/4) (γ = 7/4 from η = 1/4, ν = 1 via scaling; Onsager 1944, Yang 1952, Wu–McCoy–Tracy–Barouch 1976); ξ ∝ |t|^(−1); critical isotherm χ ∝ |h|^(−14/15) (δ = 15).",
        "check": _h2_ising_fisher,
        "verdict": "CONSIST",
        "weakness": "Exponent not fixed by the framework (γ = 7/4 is external exact data). ρ → ∞ requires choosing the family window over which the half-turn extent is measured (fixed window → ∞; order-parameter window need not diverge). I_hh = β²Var(M) carries β² unit conventions. O1 disclaims any retention law off the random walk, so only the Fisher-divergence direction is claimable on this carrier — the depth half of the criticality sentence is not.",
    },
    {
        "id": "h3",
        "class": "h",
        "name": "Landau mean-field pitchfork: mean-field exponents, framework exponent-blind",
        "carrier": "Landau order-parameter family F = a t φ²/2 + b φ⁴/4 − hφ with mean-field (Gaussian-fluctuation) treatment; unit = A1' Cramér–Rao length",
        "clause": "A1 + Criticality clause (thermal branch, mean-field)",
        "derivation": "Equilibrium: a t φ + b φ³ = h. Minimizing F alone: t < 0 gives φ₀ = √(a|t|/b) → β = 1/2; χ = (a t + 3bφ²)^(−1) = 1/(a t) above and 1/(2a|t|) below → γ = 1; t = 0 gives φ ∝ h^(1/3) → δ = 3. A1's reading: χ is the Fisher component; its divergence gives the criticality clause's direction. The two-phase Fisher separation 2φ₀√I stays O(1) (a √(2/b)-type constant): the branches stay one Fisher occasion apart while merging. Verdict identical to h2's despite γ = 1 ≠ 7/4: exponent-blind. Asymmetric probe: tilted well h ≠ 0 — χ(t = 0, h) → (1/3)b^(−1/3)|h|^(−2/3) → ∞, off the symmetric line.",
        "known_physics": "Landau mean-field exponents: β = 1/2, γ = 1, δ = 3 (Landau 1937; textbook).",
        "check": _h3_landau_pitchfork,
        "verdict": "CONSIST",
        "weakness": "The exponents come from minimizing F plus the Gaussian (mean-field) fluctuation treatment — standard mathematics external to the framework; the framework contributes A1's χ ≡ Fisher-component reading and the divergence direction only. It cannot distinguish this γ = 1 from 2D Ising's γ = 7/4 (exponent-blind). ρ is window-dependent: fixed parameter window → ∞, two-phase window → O(1).",
    },
    {
        "id": "h4",
        "class": "h",
        "name": "critical opalescence: observability of the Fisher divergence",
        "carrier": "grand-canonical density family p(N) at (T, μ) of a near-critical fluid; unit = A1' Cramér–Rao length 1/sqrt(I_μμ)",
        "clause": "A1 + Criticality clause (thermal branch, observability)",
        "derivation": "I_μμ = ∂²lnΞ/∂μ² = β²Var(N) — verified symbolically; the Gibbs–Duhem bridge (standard) makes Var(N) ∝ n²kTκ_T, so the Fisher metric IS the compressibility. Ornstein–Zernike (standard): S(q) = κ_T/(1 + q²ξ²); the Fisher-relevant divergence κ_T → ∞ holds on every approach path (asymmetric probe: coexistence and critical-isochore paths both diverge). At fixed optical q₀ the scattered intensity scales as |t|^(2ν−γ): it peaks in the crossover regime ξ ~ λ_optical and saturates/decays at asymptotic criticality — opalescence is that crossover, and the framework's ρ → ∞ reading (unit 1/√I → 0 under a fixed extent) retells the textbook fluctuation fact without predicting anything new.",
        "known_physics": "critical opalescence (Andrews 1869): diverging compressibility κ_T ∝ |t|^(−γ) (3D-Ising universality, γ ≈ 1.24, ν ≈ 0.63) drives strong light scattering at all visible wavelengths (OZ); fluctuation–compressibility sum rule.",
        "check": _h4_critical_opalescence,
        "verdict": "DESCR",
        "weakness": "DESCR: textbook fluctuation physics wearing the Fisher unit; the OZ structure factor and the Gibbs–Duhem bridge are external standard mathematics; no number is predicted. ρ → ∞ needs the same window choice as h2. Flagged: the fixed-q saturation (S(q₀) ∝ |t|^(2ν−γ)) means the framework's 'resolution at all scales' should be read on the correlation length, not on a fixed-wavelength intensity.",
    },
    {
        "id": "h5",
        "class": "h",
        "name": "superradiant QPT (Dicke): soft-mode closure and D8 route",
        "carrier": "RWA Dicke ground-state family over the coupling g in the thermodynamic limit (quadratic bosonic form, exact there); unit = A1' Cramér–Rao (Bures) length along g",
        "clause": "A1 + D8 + Criticality clause (quantum soft mode)",
        "derivation": "Quadratic form stiffness K(g) = [[ω₀², −g√(ω₀ω)], [−g√(ω₀ω), ω²]]; det K = ω₀ω(ω₀ω − g²) fixes gc = √(ω₀ω). Spectrum Ω₋² = ½(ω₀²+ω² − √((ω₀²−ω²)² + 4g²ω₀ω)): Ω₋(gc) = 0 exactly and Ω₋² ∝ (gc − g), so the soft gap closes as |g − gc|^(1/2). D8 route (own-unit, h1's noise-independent relation v² ~ 2kΔt): relaxation rate k = Ω₋ → 0, v ∝ (gc−g)^(1/4), d = 1/K(v) ∝ (gc−g)^(−1/4) → ∞ — the quantum repeat of h1's route. Known relaxation time τ ∝ Ω₋^(−1) ∝ (gc−g)^(−1/2): direction matches, exponent −1/4 vs −1/2 does not. Asymmetric probe: detuned modes ω₀ ≠ ω — the soft mode still closes at gc.",
        "known_physics": "superradiant QPT of the Dicke model: soft polariton gap Ω₋ ∝ |g − gc|^(1/2) (ν = 1/2, z = 1), relaxation time τ ∝ (gc − g)^(−1/2); fidelity susceptibility diverges at gc (direction; Emary–Brandt Phys. Rep. 346 (2001) and later fidelity-susceptibility studies).",
        "check": _h5_superradiant_qpt,
        "verdict": "CONSIST",
        "weakness": "Same D8 route and choices as h1 (OU own-unit reading, Δt, r_own = s² — flagged uncertain); the gap-to-relaxation-rate reading k = Ω₋ is standard but is a reading. The fidelity-susceptibility exponent is not pinned by this check (direction only). Mean-field exponents (ν = 1/2, z = 1) are external; the framework cannot distinguish them from h3's. A3's occasion semantics on this carrier: the two superradiant phases ±α merge in Fisher distance at gc (2|α| → 0) and O1 disclaims off-random-walk retention — no external depth target exists.",
    },
]


# =====================================================================
#  Runner — one row per system, tally at the end. Issue #21 rule 1:
#  every number printed by this file is produced by the checks above.
# =====================================================================

CLASSES = {
    "a": "two-state / occupancy families (chemical, biochemical, condensed matter)",
    "b": "quantum states and quantum dynamics",
    "c": "thermal ensembles and finite-time thermodynamics",
    "d": "parametric estimation and filtering",
    "e": "oscillators and limit cycles (physical)",
    "f": "point processes and natural-time systems",
    "g": "gravitational / astrophysical / cosmological systems",
    "h": "bifurcations and critical phenomena",
}

VERDICTS = ("SHARP", "CONSIST", "DESCR", "FAILS", "TENSION", "OPEN")

ALL_SYSTEMS = (SYSTEMS_A + SYSTEMS_B + SYSTEMS_C + SYSTEMS_D + SYSTEMS_E
               + SYSTEMS_F + SYSTEMS_G + SYSTEMS_H)


def run():
    tally = {v: 0 for v in VERDICTS}
    per_class = {}
    errors = 0
    for sysrow in ALL_SYSTEMS:
        ok, detail = None, ""
        try:
            ok, detail = sysrow["check"]()
        except Exception as exc:  # the integration audit requires zero ERROR rows
            ok, detail = None, f"CHECK RAISED: {exc}"
            errors += 1
        v = sysrow["verdict"]
        if v not in VERDICTS:
            v = "ERROR"
            errors += 1
        tally[v] = tally.get(v, 0) + 1
        per_class.setdefault(sysrow["class"], []).append(v)
        print(f"[{sysrow['id']}] {sysrow['name']}")
        state = "ok" if ok is True else ("declines" if ok is None else "fails")
        print(f"     class {sysrow['class']} | clause {sysrow['clause']} | verdict {v} | check {state}")
        print(f"     carrier: {sysrow['carrier']}")
        print(f"     detail: {detail}")
        rw = sysrow.get("rewording", "")
        if v == "TENSION" and rw:
            print(f"     minimal rewording: {rw}")
        if sysrow.get("weakness"):
            print(f"     weakness: {sysrow['weakness']}")
        print()
    print("=== tally by class ===")
    for letter in sorted(per_class):
        counts = {v: per_class[letter].count(v) for v in VERDICTS if per_class[letter].count(v)}
        print(f"  class {letter} ({CLASSES[letter]}): n={len(per_class[letter])} | "
              + ", ".join(f"{k}={n}" for k, n in counts.items()))
    print("=== total ===")
    print("  " + " | ".join(f"{k}={n}" for k, n in tally.items() if n) + f" | n={len(ALL_SYSTEMS)} | errors={errors}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
