# CRR — Coherence, Rupture, Regeneration
## Canonical statement, v3 (September 2026)

This is the complete statement of the framework as it stands. It is written
in the positive: nothing here depends on earlier formulations, and nothing
here should be read alongside them. Every line carries a status tag.

| tag | meaning |
|---|---|
| **[A]** | axiom — a commitment, not derived |
| **[D]** | definition |
| **[P]** | proposition — standard mathematics, symbolically verified in `theory/checks/verify_math.py`; labelled so nobody mistakes it for a discovery |
| **[M]** | modelling step — a choice made to connect the axioms to data |
| **[H]** | hypothesis — falsifiable, and **untested** unless `ledger/LEDGER.md` has a row for it |
| **[O]** | open — the theory does not yet fix this |

**Empirical status at the time of writing: no hypothesis in this document has
a held-out PASS in this repository's ledger.** Earlier empirical work
(4–14 September 2026) was withdrawn after independent audit. It is not cited
here and must not be cited from here.

---

## 0. What CRR is, and is not

CRR is a process theory of how a finite system moves through time. It has one
state function (coherence, an arc length), one kind of event (the cut), and
one rule for what comes after a cut (regeneration from what has settled). It
is shaped like thermodynamics, not like mechanics: it supplies a unit, a
state function, an inequality that is an equality in a limiting case, and
maximum-entropy forms for what it cannot derive. It has no equations of
motion.

Consequences of that shape, which are also its testing rules:

- CRR **cannot forecast content or timing** (§7). Any test "against the future"
  is not a test of CRR.
- CRR is tested **at cuts**, and **comparatively**: a quantity CRR names must
  predict something the system does better than the conventional quantity
  (clock time, endpoint displacement) — see §4, §5.
- A prediction that a generic smooth signal would also satisfy is not a
  prediction of CRR. Every [H] below names the synthetic signal that must
  *fail* it.

---

## 1. Carrier, metric, unit

**[A1] Carrier and metric.** A finite system's state is a point x on a
statistical manifold, and its history is a curve x(t) on that manifold. The
manifold carries the Fisher–Rao metric g. (Čencov's theorem fixes g up to a
positive scale; CRR fixes the scale by A1′.)

**[A1′] The unit is the system's own resolvable step.** Lengths on the
manifold are counted in units of σ, where σ is the smallest change the system
itself resolves. Operationally:

- For a point process (events): one event = one step. Time is *natural
  time* — the event count.
- For a continuous trace: choose **one** occasion statistic before seeing the
  data (for example, "peak-to-trough amplitude of each cycle"). Compute its
  residual across occasions on training data with a named detrender, take
  σ = 1.4826·MAD(residual) with no additive floor, and reject the record if
  σ is below the instrument's quantisation step or the residual is degenerate.
  All constants (detrender, window, MAD vs std) are parameters of the study
  and appear in its pre-registration.
- The recording instrument's sample-level noise is **not** the unit.

**[D1] Resolution.** ρ := (extent of one monotone half-turn) / σ — the number
of resolvable steps in a half-turn. ρ is a measured property of a system
under an instrument. **CRR does not predict ρ** and never uses ρ inside a
threshold; ρ is reported so that a reader can judge how coarse the counting
was.

**[D2] Coherence.** Since the last cut at time t_n,

    C(t) = ∫_{t_n}^{t} √( ẋ(τ)ᵀ g(x(τ)) ẋ(τ) ) dτ

the Fisher–Rao arc length travelled, measured in units of σ. C is
real-valued. **An integer step counter is not an admissible estimator of C**:
it floors C on monotone segments and makes the surplus of §2 negative by
construction.

**[D3] Chord.** C*(t) = d_FR( x(t_n), x(t) ), the geodesic distance from the
last cut to the present state, in units of σ.

**[P1] Arc dominates chord.** C ≥ C*, with equality iff the path is a
geodesic (in one dimension: iff the segment is monotone). *This is the
triangle inequality for a length metric and holds in every metric space; it
is not a result of CRR.*

**[D4] Lived surplus.** S := C − C* ≥ 0 (by P1). S = 0 iff the occasion was
traversed without backtracking at resolution σ. Everything a system does
beyond the shortest route between where it was and where it is, is S.

---

## 2. The cut

**[A3] The cut is the oriented antipode on the carrier.** Where the system is
cyclic, its carrier is a rotor u ∈ ℝ/Lℤ (intrinsic phase, a circle of
circumference L). The cut fires when the phase has advanced half a turn from
the last cut:

    δ(Now) = δ( u(t) − u(t_n) − L/2 )

The cut has no duration and no content. It does four things: partitions the
history into settled past and open future; settles the occasion just
completed, with its C_m, C*_m and S_m; resets C to zero; orients the next
half-turn.

Consequences that matter for testing:

- The scalar condition "cut when C = C*·(something)" coincides with A3 only on
  monotone traversals. It is not the axiom.
- **Peak detection is not the cut.** A pipeline that locates cuts with a peak
  finder is measuring waveform extrema, and its results say nothing about
  A3. The cut must be implemented as an oriented phase criterion
  (`instrument/core.py: antipodal_cuts`).
- A3 is testable only where the antipodal cut and the peak cut **disagree**:

**[H-CUT]** On carriers where phase-antipode and extremum differ (asymmetric
waveforms; systems with events of their own such as slip, firing, R-peak),
the system's own event aligns with the antipode more often than with the
extremum. *Negative controls (nothing testable, gate must read FAIL):*
symmetric limit cycles (sine, van der Pol) — antipode and extremum coincide.
*Positive control (gate must read PASS):* an asymmetric multi-harmonic
waveform. *Caution established by the gate:* additive noise alone displaces
detected extrema from antipodes, so H-CUT is scored against the system's own
events, never against the disagreement itself.

**[D5] Occasion.** The interval between consecutive cuts. Each completed
occasion m carries (C_m, C*_m, S_m). [M] For a point process, the cut is
the event itself and an occasion is one inter-event interval.

**[O3] Cut without a rotor.** For non-cyclic becoming nothing yet sets L.
Natural time gives the unit for point processes but not the cut.

---

## 3. Regeneration

**[A6] The next occasion is seeded from the settled past at bounded strength.**
The successor state is the Fisher–Rao Fréchet mean of past occasion contents
Φ_m under weights π_m, at a fixed strength κ:

    X_{n+1} = argmin_y Σ_m π_m · d²_FR( y, Φ_m )

The weights are a maximum-entropy distribution over occasions subject to
**one** history constraint. The strength is bounded: regeneration returns a
reweighted content, never an accumulated count (a system that re-counts its
past stops cutting).

**[P2] Surplus weights.** MaxEnt over occasions with ⟨S⟩ fixed gives the
Gibbs form π_m ∝ exp(β S_m), β set by the constraint value. *Standard
(Jaynes). CRR does not fix β.*

**[P3] Age weights.** MaxEnt with mean age fixed gives geometric weights
π_k ∝ q^k over age k, with ⟨k⟩ = q/(1−q). *Standard. CRR does not fix q.*

**[O2] Which constraint.** Surplus (P2) and age (P3) do not coarse-grain into
each other. Deciding between them needs a carrier whose occasions differ
in-family **and** recur. Untested.

**[H-EQ] Equanimity (learners).** When a learner updates from a present batch
and a replayed past batch, weight the past gradient so that settled past and
present exert equal pull in the Fisher norm:

    g = g_present + w · g_past,   w = Ω · ‖ḡ_present‖_F / ‖ḡ_past‖_F,   Ω = 1

with ḡ smoothed mean gradients and a named smoothing constant. **Status:** in
the one comparison made, this was within seed noise of a *fixed* w = 1, and
the Fisher metric made no difference. It counts as a result only if it beats
experience replay with the two losses summed (the standard baseline) and the
best fixed w, on data not used to choose the estimator. *Must fail on:* a
convex learner with no forgetting to trade off.

---

## 4. Regularity — "change has its own clock"

This is the shape of test CRR is built for: a CRR quantity against a clock.

**[H-L5]** For a system with its own boundary events (slips of a fault, beats
of a heart, firings), the coherence C accumulated between consecutive events
is a **more regular** quantity than the clock time between them:

    CV( C_m ) < CV( Δt_m )   across occasions m,

and this holds beyond three controls: (i) the amplitude of the excursion
alone, (ii) arc computed with the identity metric instead of g, (iii) arc
between *peak-detected* boundaries instead of antipodal ones. Scored per
level/subject with a paired bootstrap on the CV difference.
*Negative controls (gate must read FAIL):* a pure sine (nothing varies), an
amplitude-modulated sine with constant period (clock is the regular one), and
a relaxation oscillator whose firing time is fixed while its threshold
varies (clock-regular by construction). *Positive controls (gate must read
PASS):* a frequency-modulated sine with constant amplitude and a relaxation
oscillator with fixed threshold and variable charging rate — systems in
which "change has its own clock" is true by construction. H-L5 is therefore
an empirical claim about which class a real system belongs to; it is not
tautological, and the gate (`surrogates/gate.py L5`) shows the instrument
separates the two classes.

---

## 5. Path length in learners

**[D6] Arc for a parametric model.** For a model with predictive distribution
p_θ(y|x) and a fixed probe set, the Fisher–Rao length of one update is, to
second order, √(2·KL(p_{θ_{t−1}} ‖ p_{θ_t})) averaged over the probe. So

    C_new = Σ_t √( 2·KL_t )  on a new-task probe,
    C_old = Σ_t √( 2·KL_t )  on an old-task probe,
    E     = KL( p_{θ_0} ‖ p_{θ_T} )  (endpoint displacement),
    C*    = √(2E),   S = C − C*.

**[H-T1] Forgetting tracks the path, not the endpoint.** For fine-tuning on a
new task, the forgetting F of an old task (rise in old-task loss) is
predicted better by C_new or C_old than by E on the new task, **with learning
rate controlled** (path length varied at fixed lr by schedule) and scored on
held-out runs. *Must fail on:* a convex learner (linear model, convex loss),
where forgetting is a function of the endpoint alone.

---

## 6. Retention

CRR supplies the unit; the amount of past a system carries is a property of
the system's own dynamics.

**[P4] Kalman identity.** For a scalar random-walk state with process
variance q and observation variance r, the steady-state Kalman gain depends
on the data only through the Fisher speed v = √(q/r):

    K(v) = (v/2)·( √(v² + 4) − v ),   K(1) = 1/φ = (√5 − 1)/2,   K → 1 as v → ∞.

*Standard (textbook steady-state Riccati). CRR's reading is that √(q/r) is
a speed in Fisher units; the formula itself is not CRR's.*

**[O1] Retention depth.** Whether the memory depth of a system follows from
its own state model at Ω = 1, with no other parameter, is open. Until it is
derived for a mean-reverting or oscillatory state model and checked,
retention is **not** a CRR quantity and no retention law is claimed.

---

## 7. Natural time and consistency relations

**[P5] Exponential retention in natural time is a power law in shifted clock
time iff p = 1.** If events arrive at rate λ(t) = K·(t + c)^{−p} and the
system retains with e^{−A(t)/ρ}, A(t) = ∫λ, then retention is
((t + c)/c)^{−K/ρ} exactly when p = 1, and a stretched/compressed exponential
otherwise. *Standard calculus.* This is a **consistency relation**, not a
prediction: p ≈ 1 is the generic empirical value for aftershock sequences and
is derived independently by rate-and-state friction. A fitted p tells you
nothing about CRR, and a "memory depth" defined as 1/p from the same fit is a
reparameterisation, not a measurement.

---

## 8. Prohibitions

**[A7] Relational tense.** What is future for a system can only be fed by
what is already past for something. Nothing is fed by a future.

**[A8] No valence, no forecast.** Persistence proves regeneratability, not
truth. CRR forbids itself any prediction of the *content* or *clock time* of
a future occasion. Its predictions are relations that hold at cuts,
inequalities, and comparisons of regularity.

---

## 9. Summary of what could fail

| id | claim (one line) | fails if | must fail on (surrogate) |
|---|---|---|---|
| H-CUT | own events sit at the phase antipode, not the extremum | extremum wins where they differ | symmetric cycles (nothing to test); scored on events, not on noise-induced disagreement |
| H-L5 | C between events more regular than clock, beyond controls | CV_C ≥ CV_Δt, or a control matches it | pure sine, AM sine, clock-regular relaxation oscillator (must pass on FM sine and arc-regular oscillator) |
| H-T1 | forgetting tracks path length, lr controlled | endpoint predicts as well | convex learner |
| H-EQ | Ω = 1 gradient balance beats ER-sum and best fixed w | ties either | convex learner |

Everything else in this document is definition, standard mathematics, or open.
