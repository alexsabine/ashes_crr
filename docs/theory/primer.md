# CRR in brief — a primer for newcomers

> Explanatory primer. The canonical statement is
> [`theory/CRR.md`](../../theory/CRR.md); on any conflict, CRR.md wins.
> Nothing here adds a claim; every section links the CRR.md section it
> paraphrases and the code that implements it.

---

## 0. What CRR is — and is not

CRR (Coherence–Rupture–Regeneration) is a **process theory of how a finite
system moves through time** ([CRR.md §0](../../theory/CRR.md)). It has
exactly three moving parts:

- one **state function** — coherence, an arc length on a statistical
  manifold ([D2](../../theory/CRR.md));
- one kind of **event** — the cut ([A3](../../theory/CRR.md));
- one rule for what comes after a cut — **regeneration from what has
  settled** ([A6](../../theory/CRR.md)).

It is **shaped like thermodynamics, not like mechanics** (CRR.md §0): it
supplies a unit, a state function, an inequality that is an equality in a
limiting case, and maximum-entropy forms for what it cannot derive. It has
**no equations of motion**.

Three consequences of that shape are also its testing rules (CRR.md §0):

1. CRR **cannot forecast content or timing** ([A8](../../theory/CRR.md));
   any test "against the future" is not a test of CRR.
2. CRR is tested **at cuts**, and **comparatively**: a quantity CRR names
   must predict something the system does better than the conventional
   quantity (clock time, endpoint displacement).
3. A prediction a generic smooth signal would also satisfy is not a
   prediction of CRR: every hypothesis names the synthetic signal that
   must *fail* it (the [surrogate gate](../modules/surrogates.md)).

## 1. Carrier, metric, unit — A1, A1′, D1

A finite system's state is a point on a statistical manifold and its
history a curve on it; the manifold carries the **Fisher–Rao metric**
([A1](../../theory/CRR.md), CRR.md §1).

**[A1′] The unit is the system's own resolvable step.** Lengths are
counted in units of σ: choose **one** occasion statistic *before seeing
the data*, compute its residual across occasions, take
σ = 1.4826·MAD(residual) with **no additive floor**. The recording
instrument's sample-level noise is not the unit.

**[D1] Resolution.** ρ := (extent of one monotone half-turn)/σ. ρ is a
**measured** property of a system under an instrument: CRR does not
predict it and never uses it inside a threshold; it is reported so a
reader can judge how coarse the counting was.

Code: `unit_sigma()` in
[`src/crr/instrument/core.py`](../../src/crr/instrument/core.py);
ρ is reported by the `rho()` helper of the same module.

## 2. Coherence, chord, surplus — D2–D4, P1

Since the last cut at time t_n ([D2](../../theory/CRR.md), CRR.md §1):

- **Coherence** C(t) = the Fisher–Rao arc length travelled since the cut,
  in units of σ. Real-valued — **an integer step counter is not an
  admissible estimator**: it floors C on monotone segments and makes S
  negative by construction (demonstrated symbolically in
  [`theory/checks/verify_math.py`](../modules/theory-checks.md)).
- **Chord** C*(t) = the geodesic distance from the last cut to the
  present state ([D3](../../theory/CRR.md)).
- **Lived surplus** S := C − C* ≥ 0 ([D4](../../theory/CRR.md)), by
  [P1](../../theory/CRR.md) — arc dominates chord, with equality iff the
  path is a geodesic (in 1-D: iff the segment is monotone). P1 is the
  triangle inequality for a length metric; **it is not a result of CRR**.
  S = 0 iff the occasion was traversed without backtracking at resolution
  σ. Everything a system does beyond the shortest route between where it
  was and where it is, is S.

Code: `arc_length()`, `chord()`, `surplus()` in
[`src/crr/instrument/core.py`](../../src/crr/instrument/core.py).

## 3. The cut — A3, D5, H-CUT

**[A3] The cut is the oriented antipode on the carrier** (CRR.md §2).
Where the system is cyclic, its carrier is a rotor — the intrinsic phase,
a circle — and **the cut fires when the phase has advanced half a turn
from the last cut**. The cut has no duration and no content. It does four
things: partitions history into settled past and open future; settles the
occasion just completed, with its C_m, C*_m and S_m; resets C to zero;
orients the next half-turn ([D5](../../theory/CRR.md)).

Two consequences that matter for testing:

- **Peak detection is not the cut.** A pipeline that locates cuts with a
  peak finder is measuring waveform extrema, and its results say nothing
  about A3.
- A3 is **testable only where the antipodal cut and the peak cut
  disagree** — asymmetric waveforms, systems with events of their own
  (slip, firing, R-peak). That is
  [H-CUT](../../theory/CRR.md): the system's own event aligns with the
  antipode more often than with the extremum. On symmetric limit cycles
  (sine, van der Pol) the two coincide — nothing to test, the gate must
  read FAIL. Additive noise alone displaces detected extrema from
  antipodes, so H-CUT is **scored against the system's own events, never
  against the disagreement itself**.

Code: `intrinsic_phase()` and `antipodal_cuts()` (this IS the cut of A3,
oriented — only forward crossings count) in
[`src/crr/instrument/core.py`](../../src/crr/instrument/core.py);
`peak_cuts()` exists only so studies can show where it disagrees.
Gate: [`crr.surrogates.gate CUT`](../modules/surrogates.md).

## 4. Regeneration — A6, P2, P3, O2

**[A6] The next occasion is seeded from the settled past at bounded
strength** (CRR.md §3). The successor state is the Fisher–Rao Fréchet
mean of past occasion contents Φ_m under weights π_m, at a fixed strength
κ. The weights are a maximum-entropy distribution over occasions subject
to **one** history constraint; two candidates are proved standard
mathematics:

- **Surplus weights** ([P2](../../theory/CRR.md)): Gibbs form
  π_m ∝ exp(β S_m).
- **Age weights** ([P3](../../theory/CRR.md)): geometric weights
  π_k ∝ q^k, with ⟨k⟩ = q/(1−q).

CRR does not fix β or q, and **which constraint applies is open**
([O2](../../theory/CRR.md)) — deciding needs a carrier whose occasions
differ in-family *and* recur. "Bounded strength" means regeneration
returns a reweighted content, never an accumulated count: a system that
re-counts its past stops cutting.

No regeneration estimator exists in the instrument; regeneration is
definition and standard mathematics, untested.

## 5. Regularity — "change has its own clock" — H-L5

**[H-L5]** (CRR.md §4) For a system with its own boundary events (slips
of a fault, beats of a heart, firings), the coherence C accumulated
between consecutive events is a **more regular** quantity than the clock
time between them:

> CV(C_m) < CV(Δt_m) across occasions m,

scored per level/subject with a paired bootstrap on the CV difference,
and required to hold **beyond three controls**: (i) the amplitude of the
excursion alone, (ii) arc computed with the identity metric instead of g,
(iii) arc between peak-detected boundaries instead of antipodal ones.

The gate fixes the two classes the claim separates:

- **Negative controls (gate must read FAIL):** a pure sine (nothing
  varies), an amplitude-modulated sine with constant period (clock is the
  regular one), a relaxation oscillator whose firing time is fixed while
  its threshold varies (clock-regular by construction).
- **Positive controls (gate must read PASS):** a frequency-modulated sine
  with constant amplitude, a relaxation oscillator with fixed threshold
  and variable charging rate (arc-regular by construction).

H-L5 is therefore an empirical claim about *which class a real system
belongs to* — it is not tautological, and the gate shows the instrument
separates the two classes.

Code: `cv()`, `regularity()` (paired bootstrap included) and the
per-unit `sign_test_units()` helper in
[`src/crr/instrument/core.py`](../../src/crr/instrument/core.py).
Gate: [`crr.surrogates.gate L5`](../modules/surrogates.md).

## 6. Path length in learners — D6, H-T1

**[D6]** (CRR.md §5) For a parametric model with predictive distribution
p_θ(y|x) and a fixed probe set, the Fisher–Rao length of one update is,
to second order, √(2·KL(p_{θ_{t−1}} ‖ p_{θ_t})) averaged over the probe.
So:

- C_new, C_old = Σ_t √(2·KL_t) on a new-task / old-task probe,
- E = KL(p_{θ_0} ‖ p_{θ_T}) — the endpoint displacement,
- C* = √(2E), and S = C − C*.

**[H-T1] Forgetting tracks the path, not the endpoint.** For fine-tuning
on a new task, the forgetting F of an old task is predicted better by
C_new or C_old than by E, **with learning rate controlled** (path length
varied at fixed lr by schedule) and scored on held-out runs.

It **must fail on a convex learner** (linear model, convex loss), where
forgetting is a function of the endpoint alone — in fact exactly
F = 2σ²·E_old on the old probe (lemma verified in
[`theory/checks/verify_scope_math.py`](../modules/theory-checks.md)),
which is why the endpoint on the *old* probe, not only the new one, is a
required baseline in the gate.

Code: `kl_step()`, `kl_gauss()`, `path_length()` in
[`src/crr/instrument/core.py`](../../src/crr/instrument/core.py).
Gate: [`crr.surrogates.gate T1`](../modules/surrogates.md).

## 7. Prohibitions — A7, A8

- **[A7] Relational tense.** What is future for a system can only be fed
  by what is already past for something. Nothing is fed by a future.
- **[A8] No valence, no forecast.** Persistence proves regeneratability,
  not truth. CRR forbids itself any prediction of the *content* or
  *clock time* of a future occasion. Its predictions are relations that
  hold at cuts, inequalities, and comparisons of regularity.

## 8. What could fail

The theory contains four falsifiable hypotheses and nothing else that can
be tested (CRR.md §0, §9). In substance, from the CRR.md §9 table:

| id | claim (one line) | fails if | must fail on (surrogate) |
|---|---|---|---|
| H-CUT | own events sit at the phase antipode, not the extremum | extremum wins where they differ | symmetric cycles (nothing to test); scored on events, not noise-induced disagreement |
| H-L5 | C between events more regular than clock, beyond controls | CV_C ≥ CV_Δt, or a control matches it | pure sine, AM sine, clock-regular relaxation oscillator (must pass on FM sine and arc-regular oscillator) |
| H-T1 | forgetting tracks path length, lr controlled | endpoint predicts as well | convex learner |
| H-EQ | Ω = 1 gradient balance beats ER-sum and best fixed w | ties either | convex learner |

Everything else in CRR.md is definition, standard mathematics, or open.
H-EQ has no gate yet (`gate_EQ`, [SCOPE.md §4.3](../../theory/SCOPE.md));
until it exists, EQ cannot enter a prereg — see
[audit finding #12](../audit/2026-09-15-audit.md). **No hypothesis has a
held-out PASS**: the ledger is empty.
