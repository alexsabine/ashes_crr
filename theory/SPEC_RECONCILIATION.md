# Reconciliation — the external test specification against theory/CRR.md v3.1

Written 2026-09-17 (prompt-log entry 33). The external document is
`theory/external/CRR_test_specification_GPT6_Astra_2026-09-16.md` (sha256 in
`theory/external/README.md`), uploaded by the owner and described as output of "GPT 6 Astra".
It is **not** the theory under test; `theory/CRR.md` v3.1 is. This note says, clause by clause,
whether the external spec agrees with v3.1, adds to it, or contradicts it (or contradicts the
older text the owner posted as issue #21, which carries clauses v3.1 does not). Its
mathematical claims are verified in `theory/checks/verify_spec_math.py` (output committed
beside it: every check PASS). Nothing here changes CRR.md; a change needs the owner's signature
and a version bump (v3.1 → v3.2), as for v3.1.

## 1. Where the two documents say the same thing

| spec | v3.1 | note |
|---|---|---|
| D1, A1 (Fisher–Rao carrier, positive-definite), T1 (reparameterisation invariance) | A1 | identical; the spec adds the useful corollary that changing the *model* is not a coordinate change (verified: Poisson vs Bernoulli lengths differ on the same numbers) |
| A1a (per-elementary-event unit, I_N = N I_1) | A1′ | identical in substance; the spec states the additivity argument explicitly |
| D2, D3, D4 (C, chord, S = C − D), T2, T3 | D2, D3, D4, P1 | identical; the spec renames C* as D, and both label C ≥ D as inherited geometry |
| A2a (cut at an independently specified target; C/H = 1 on a geodesic) | A3 with its consequence "the scalar condition is only the monotone reduction" | the spec's cut is more general (any canonical target or event surface); v3.1's rotor antipode is its D5 prototype |
| A5 (Fréchet barycentre with weights π) | A6 | identical, except the spec removes κ (below) and makes the argmin set-valued when non-unique |
| D9 / T5 (π ∝ e^{S/Ω}; log-odds law) | P2 (MaxEnt with ⟨S⟩ fixed gives the Gibbs form) | same law; v3.1 says "CRR does not fix β", the spec names β = 1/Ω and fixes Ω = 1 as the hypothesis (H1); T5 is the explicit prediction v3.1 never wrote down |
| O1 (independent recency kernel; geometric special case) | P3, O2 | identical; the spec's Decision 10 (recency and surplus can compensate) is new and important |
| A6 (settled-past-only) | A7, A8 | identical in content |
| T7 (scalar Kalman gain, K(1) = 1/φ) | P4 | identical, both labelled inherited |
| XIV (freeze, compare λ = 0 / λ = 1 / free λ, held-out) | CLAUDE.md R2–R7 | same protocol, stated for the salience test |

## 2. What the spec adds that v3.1 lacks (owner decision whether to sign in)

- **T4, S = 2B in one dimension.** True (verified on 2000 random paths). It gives S a plain
  reading: twice the resolved backtracking. Worth adding to D4.
- **T5, the pairwise influence-odds law** `log(π_i/π_j) = S_i − S_j` at Ω = 1 and equal
  retention. This is the cleanest numerical claim in either document and v3.1 has no test built
  on it. Every CRR study so far has tested other things (arc regularity, gradient weighting,
  path length). A study of T5 needs a system with several admissible past occasions, an
  independent content map Φ, and a way to fix or cancel recency (spec §XIV). None exists yet.
- **T6, tail exponent α = βΩ.** True (verified). Conditional on an exponential surplus tail;
  a way to test Ω without a fitted slope if a domain supplies β independently.
- **A4, the depth-one screening gate.** New and necessary: on a Markov system the salience law
  predicts nothing, and applying it would produce a false negative. The retrodiction battery's
  Hawkes row shows the case.
- **D7 / A3, content Φ is not surplus S.** New as a stated clause; v3.1's A6 uses Φ_m but never
  says S does not encode it.
- **Decision 10, surplus–recency compensation.** New; it is the identifiability warning any
  T5 prereg must carry.
- **XV, a first real-data test of λ = 1 (visuomotor adaptation), verdict MIXED.** External to
  this repository; no script, log or hash for it exists here, so under R1 it is context, not a
  ledger row. If the owner wants it in the ledger it must be re-run under the protocol.

## 3. Where the spec removes or narrows a claim

| spec removes | present in v3.1? | present in the issue-#21 text? | retrodiction row |
|---|---|---|---|
| universal `C·Ω = 1` rupture | no (A3 note already calls it a monotone reduction) | yes | verify_spec_math [XI.1] |
| Bernoulli `p = 1/2` antipode | no (A3 is rotor-only) | yes | row 1: FAILS as universal |
| "mixed quantum states never cut" | no | yes | row 8: FAILS as universal |
| universal thermal-Fisher divergence at criticality; ρ → 0 at Hopf, ρ → ∞ at thermal criticality | no (v3.1 has no §6 criticality clause) | yes (D7, P6, D8) | rows 11, 12, 29, 31: class-dependent |
| universal memory-depth divergence (D8) | no (O1 declines a retention law) | yes | row 30: FAILS at fixed q, r |
| universal coupling κ | **yes** (A6 "at a fixed strength κ") | yes | — |
| Ω inside the cut | no | no | — |

So the spec's removals mostly target the older text, not v3.1; the one v3.1 clause it removes
is κ in A6, and the spec's reason (a free strength lets the reset magnitude float after the
target is computed) is sound. Recommendation: drop κ from A6 in v3.2 and say, as the spec's O2
does, that the realised strength is the system's own dynamics.

## 4. The one genuine conflict: two "equanimity" laws under one name

- **Spec [P7]/[H1], issue-#21 text A9:** Ω = 1 is the temperature of the *occasion weights*
  π ∝ e^{S/Ω}; the issue text adds "stated as equal precision — never as a ratio of pull
  magnitudes (that form is ill-posed when either pull vanishes)".
- **v3.1 [H-EQ]:** for a learner, `w = Ω · ‖ḡ_present‖ / ‖ḡ_past‖`, a ratio of pull magnitudes.

These are different laws. The retrodiction battery grades the pair TENSION (row 16) and
`verify_spec_math.py` shows the ratio form is unbounded as the past gradient vanishes, which is
exactly the regime in which study EQ2's pass lives (ledger EQ2-1, EQ2-S: the pass needs
cap = 1e4 and vanishes at cap = 100). Read together: EQ2 did not test the spec's equanimity
hypothesis at all; it tested a normalised-gradient heuristic that shares the name. Before any
further EQ prereg the owner must decide which law carries the name. The spec's T5 is the
version with a Fisher-unit meaning; H-EQ's is the version with a ledger.

## 5. What the retrodiction battery says about the framework as a whole

`theory/retrodictions/crr_retrodictions.txt` (32 systems, 8 classes): 0 SHARP, 10 CONSIST,
10 DESCR, 6 FAILS, 1 TENSION, 5 OPEN. Every row borrows its metric or distance from the
domain, and in 25 of 32 the velocity inside the coherence integral is supplied by the system's
own dynamics (rate constants, a Hamiltonian, a protocol, a state recursion, an orbit). That is
the spec's §XIII in numbers: the inherited mathematics is not evidence, and the only clauses
with numerical bite are the occasion structure, the surplus in a fixed carrier, the exponential
weighting with Ω = 1, and settled-past-only regeneration — none of which the battery could
grade SHARP on a known system, because no known system is a multi-occasion salience test.
