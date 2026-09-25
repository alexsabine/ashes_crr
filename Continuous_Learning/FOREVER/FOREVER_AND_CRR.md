# CRR run through FOREVER's mathematics

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 180. The work is a declared synthetic check (rung
R4).
- **Declaration.** `DECLARATION.md` was pushed at 7760b88 before the script existed. Amendment 1 was pushed at a54184b
  before the rerun.
- **Numbers.** Every number is from `checks/forever_checks.txt`, which is pinned and byte-identical on rerun.
- **The paper.** FOREVER, arXiv 2601.03938 v2, 20 Apr 2026, read in full on the day
  (`docs/citations/forever_2026-09-25.md`).

## 1. CRR read as falsifiable metaphysics, and where FOREVER already is CRR

FOREVER was built from Ebbinghaus's forgetting curve, not from CRR. Its scheduler is nevertheless CRR's coherence clock
almost term for term:

| FOREVER | CRR (`theory/CRR.md`) | same or different |
|---|---|---|
| τ_t = Σ‖Θ_t − Θ_{t−1}‖₂, "the total distance the model has traveled in parameter space" | **D2**: coherence C is the arc travelled since the last cut | the same construction; the **metric** differs (Euclidean on LoRA weights, against Fisher–Rao on predictions) |
| "τ_t is reset at the beginning of each new task" | **A3**: the cut "resets C to zero" | the same. The task boundary is the cut |
| τ_day = the arc of the first S = 24 steps: "a model-specific unit of time" | **A1′**: lengths are counted in the system's own resolvable step | the same idea, with a different statistic: FOREVER uses the arc of a warm-up window; A1′ uses a robust scale of occasion residuals |
| replay fires when τ ≥ d·τ_day, d = 1, 2, 4, 7, 15, 30 | occasions within a task, marked by arc thresholds | **not an A3 cut.** CRR.md says a scalar arc condition "is not the axiom", and a cut without a rotor is open (O3). FOREVER is an empirical answer to O3 that CRR has not given |
| "Unlike raw step counts, τ_t directly reflects model evolution" | "change has its own clock" (§4) | the same claim. FOREVER's ablation supports it: model-centric calibration beats step calibration by 1.2 OP and 1.1 BWT (the paper's numbers) |
| β_t = β_base·clip(1 + γ(r_t − 1), 0.5, 3), r_t the recent update size against the warm-up size | **H-EQ**: the past's weight set by the present's pull, w = Ω‖ĝ_p‖/‖ĝ_q‖ | related: both raise the past's weight when the present moves fast. FOREVER divides by a warm-up constant, where H-EQ divides by the past's own length |
| the anchor Θ* is the end of the previous task, with a weight bounded by g_max·β_base | **A6** with P3's q → 0: regeneration from the latest settled occasion, at bounded strength, never an accumulated count | consistent with A6. Online EWC, which accumulates, is not |
| τ advances only with updates; the EMA (8) advances per update in Algorithm 1 | **E2**, Proposition 7: the learner's own clock, so a pause carries no content | consistent: FOREVER's schedule is pause-neutral as specified (F5a) |

**The metaphysical reading, stated so it can fail.** CRR claims that a system's change should be measured:
- on its own clock;
- in its own unit;
- as an arc that restarts at each cut;
- in the Fisher–Rao metric, the only metric invariant to how the system is parametrised (Čencov).

FOREVER independently found the first three useful, which is the first external support in continual learning for
"change has its own clock". It used a Euclidean metric. The checks below ask what the fourth commitment, and CRR's
weighting rule, change on FOREVER's own quantities.

## 2. The checks (declared; labels computed by the script)

| check | CRR commitment | result | reading |
|---|---|---|---|
| F1a, F1b | the Fisher arc is invariant to parametrisation | **HOLD.** Under a LoRA rescaling P → PD, Q → D⁻¹Q the predictions differ by at most 6.661e-16 and the Fisher arc by at most 9.554e-14 (relative) | standard (Čencov) |
| F1c | FOREVER's Euclidean clock is not invariant | **HOLDS.** The same function path gives a Euclidean arc of 4.989435 before and 10.113847 after; FOREVER's second trigger moves from update 257 to 288 | LoRA's factor symmetry makes τ a property of the parametrisation, not of the model. In FOREVER's own setting it is the LoRA weights that are measured |
| F1d | A1′'s own unit removes a global change of units | **HOLDS.** Δ × 7 leaves every trigger unchanged | FOREVER's τ_day calibration does A1′'s work for a global scale; it cannot for a per-direction scale (F1c) |
| F2a, F2b | D2's "change" is change in what the system says | **HOLD.** Noise on weights that affect no prediction leaves the Fisher triggers unchanged, while FOREVER's Euclidean triggers move earlier in 3 of 6 (second trigger 208 → 65) | FOREVER's clock counts movement that changes nothing; the Fisher clock does not |
| F3b | the human schedule in steps with constant Δ | **HOLDS.** Triggers at 24, 48, 96, 168, 360, 720 | trivial |
| F3a | P5, the consistency relation | **FAILS** as declared. With Δ ∝ 1/(t + 50) the triggers are 24, 60, 189, 718, 17177 and 5876606; the declared continuous formula misses by up to 532804.4 steps | **an error in the declaration's approximation, not in P5.** A half-step correction, post hoc, is within 1460.4 steps. The qualitative point stands: when updates shrink like 1/t, FOREVER's schedule in model time becomes geometric spacing in steps |
| F4a | the zero-anchor freeze of H-EQ | **FAILS.** In this quadratic world the rule's weight is at its cap on only 0.02 of the first 50 steps | RW2's freeze is world-dependent, not general. The record's warning stands for RW2's setting only |
| F4b | the step bound: the past step is at most Ω times the present, whatever the anchor's scale | **HOLDS.** FOREVER, with β_base tuned at c = 1 (β_base = 3), diverges at c = 16 and 256 for every γ. The rule is finite at every c (totals 3.218950, 3.308091, 4.734344). The tuned fixed w = 1 survives c = 16 (3.305829) and diverges at 256 | FOREVER's β_base carries the anchor's units. The paper says "This calibration is critical". The rule's weight does not carry them |
| F4c | where FOREVER stops | **HOLDS.** As movement stops, β_t → β_base·max(g_min, 1 − γ) exactly: 1.5 for every γ | **FOREVER's adaptive weight reduces to a constant** when training converges. Here every γ gave the same total, 2.210193. It picks one fixed-λ point on the Pareto curve, where Ω = 1 picks none |
| F4d | H-EQ's own claim: equal pull is at least as good | **FAILS,** as the record predicted. The rule's total at c = 1 is 3.218950, against FOREVER's 2.210193 and the tuned fixed w = 1's 2.140476 | the same trade as the Adam checks: robust to scale, worse where the scale is right |
| F5a, F5b | E2: a clock keyed to the learner's own updates makes a pause empty | **HOLD.** FOREVER's triggers are identical for pauses of 0, 50 and 500 ticks. Wall-keyed thresholds move: the fourth trigger falls at update 168, 118 and 101 | FOREVER's scheduler is pause-neutral as specified. MetaClaw's and TIMEGATE's wall-clock windows are the kind that are not |
| F5c | the EMA (8) advanced per wall tick puts content into a pause | **FAILS** as declared. β at the first replay after the pause is 0.5·β_base under both EMAs | the channel exists but is hidden by the clip floor. The unclipped ratio is 3.536304e-02 per update, against 3.532905e-02 and 3.532622e-02 per tick for L = 50 and 500 (a post-hoc report line). A clip can mask an E2 violation, so any audit must read the unclipped quantity |
| F6a | D3/D4: the arc overstates change when the path comes back | **FAILS** as declared. The arc clocks fired 2 and 1 triggers, the chords 1 and 1 | the path did go out and back: old-task loss 0.008658 at the start, 0.180147 after task B, 0.007899 at the end, with Fisher arc 4.035926 against Fisher chord 1.673135. But the trigger counts barely differ, because most of the arc is travelled early |

**The script's summary line:**
- 11 labels hold: F1a, F1b, F1c, F1d, F2a, F2b, F3b, F4b, F4c, F5a, F5b.
- 5 fail: F3a, F4a, F4d, F5c, F6a.

## 3. What this says about CRR, and what it does not

**What held, as mathematics.**
- FOREVER is CRR's coherence clock with a Euclidean metric: the arc since the last cut, in an own unit, on the learner's
  own clock.
- Two of CRR's further commitments change FOREVER's quantities in the direction CRR says:
  - **The Fisher metric** makes the clock independent of the LoRA parametrisation (F1) and blind to movement that
    changes no prediction (F2).
  - **The step bound** keeps a past weight finite when the anchor's scale changes, where FOREVER's β_base, a constant
    with units, diverges (F4b).
- These are properties, not gains in accuracy. Whether either improves forgetting is exactly what ARC-R would test.

**What failed.**
- **H-EQ's claim that equal pull is at least as good** (F4d). FOREVER's weight reduces to a constant at convergence
  (F4c), and a tuned constant is better still in this world.
- **Three declared checks** failed for reasons worth keeping:
  - F3a: my continuous approximation was wrong.
  - F5c: a clip hides a pause channel.
  - F6a: the arc and the chord fire alike when most of the arc is early.
- **The zero-anchor freeze did not appear in this world** (F4a). It is not a general property of the rule.

**What FOREVER's own evidence says** (the paper's numbers, not this repository's):
- the own clock beats the step clock by 1.2 OP and 1.1 BWT;
- increasing spacing beats uniform and decreasing spacing under the same replay budget;
- forgetting is about 7 times faster early than late.

The first supports "change has its own clock" as a design principle for replay. The paper is silent on the metric.

**The falsifiable next step.** ARC-R, declared and gated before any data:
- **Arms:** replay scheduled on the Fisher arc; on FOREVER's Euclidean arc; on steps; on wall time.
- **The world:** a LoRA-factored learner, where F1 and F2 say the two arcs differ.
- **R7:** FOREVER as the published baseline.
- **Must-fail surrogate:** a convex learner, where no clock should matter.
- **Must-pass surrogate:** a learner with movement that changes nothing (F2's world). There the Fisher clock must not
  fire spuriously, and FOREVER's does.

If the Fisher arc ties FOREVER on real data, CRR's metric adds nothing to FOREVER's clock, and the ledger will say so.

**Addendum, 2026-09-25 (prompt-log entry 181).** The comparative battery (`COMPARATIVE.md`, Declaration 2) ran the gate
that ARC-R would have needed, and the gate is **CLOSED**.
- The Fisher-arc clock ties FOREVER in 7 of 7 worlds, including the null-movement world built to carry the effect.
- Under R12, no clock claim goes to a prereg, and ARC-R as described above is not licensed.
