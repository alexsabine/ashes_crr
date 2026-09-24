# When does a cut need content? CUT1 Phase A, the synthetic gate

**Status of this note.**
- **The request.** Prompt-log entries 151–152: run the literature checks and the pipeline on synthetic data, to prepare a
  real-data test of cuts with and without content in continual learning.
- **It is a note, not evidence (R8).** Every number comes from `checks/cut_phaseA.txt`, printed by
  `checks/cut_phaseA.py`. A rerun was byte-identical.
- **Declared before it ran.** `DECLARATION.md` was pushed in 6eef1f7 and its Amendment 1 in d08aa21, both before the
  script existed. The literature check is `docs/citations/plasticity_resets_2026-09-24.md`.
- **Rung.** R4: a declared check on synthetic worlds. It is not a ledger row.

## The result: GATE CLOSED

| check | declared expectation | result |
|---|---|---|
| A0 validity | plasticity loss in some World P cells | 1 of 12 cells: T50, width 32, SGD (Fresh − E0 = +23.69, step 2.04) |
| A1 must win | SP beats E0 in every valid cell | holds (+14.79) |
| A2 positive control | L2-Init beats E0 in every valid cell | holds (+23.16, λ 0.001) |
| A3 separation | R-hard does not beat E0 | **FAILS** (+8.69) |
| A4 must fail (convex) | no content cut ahead | **FAILS** on plasticity: SP +7.08, Head +4.88 (step 2.35). Holds on final accuracy |
| A5 must fail (retention) | none ahead; SP and Head behind | holds (SP −67.23, Head −78.33) |
| A6 must fail (drift) | none ahead | holds (every content cut behind or tied) |
| A7 safety construction | lossless pauses leave the parameters bit-identical, with 0 disables | holds for every arm in both worlds |

**Under R12, no real-data CUT1 prereg follows.** The declaration's rule reads CLOSED when a must-fail check passes (A4),
so neither the plasticity hypothesis nor the harm hypotheses go forward (AGENT_LOG 122).

## What the numbers say

1. **The empty cut is the safety construction, and it held again.** Pausing the learner losslessly on its own clock
   changed nothing, for every arm and in both worlds checked. This repeats SCL1-1 and SCL2-1 on a new harness. It is true
   by construction: a check of the implementation, not support for CRR.
2. **Plasticity loss was rare in these worlds.** Only the longest stream (50 tasks) with the small network (width 32)
   under SGD showed it. In the other 11 cells, including every Adam cell, continued training was not behind a fresh
   network by a step. That agrees with the literature check: plasticity loss needs long streams and small networks.
3. **Where plasticity loss existed, the known remedies worked.** L2-Init nearly matched a fresh network (42.61
   against 43.14). SP (+14.79), Head (+14.69) and ReDo0 (+15.28) each recovered part of the gap.
4. **Content that restores room to learn destroys what must be kept.** In the class-incremental world, SP lost 67.23
   points and Head lost 78.33. In the drift world, every content cut was behind or tied.
5. **The reset used in SCL1 (R-hard) is not a plasticity intervention, and A3 could not show that.** It was ahead by
   +8.69 where plasticity was lost. It was behind in the convex world's plasticity (−11.50) and in the drift world
   (−1.43).
   - **My reading, not tested.** Reverting mid-task discards half of each task's updates, so less damage accumulates.
     A3 as declared cannot separate that dose effect from a plasticity effect.

## Why the gate closed, read against the declaration

**A4.** The convex must-fail world assumed that warm starting a convex learner costs nothing (Ash and Adams). That holds
at convergence. At 3 epochs per permuted task, a start near zero beat the previous permutation's weights: SP +7.08 and
Head +4.88. Head is identical to Fresh here, as the amendment said. On final accuracy no content cut was ahead.

**A3.** The separation assumed that the task-start checkpoint "carries the damage". It does carry the damage up to the
task's start, but the mid-task reversion also halves the damage added after it.

**Whatever the failures mean, the gate is not reopened here.** A redesign would be a new declaration, labelled post hoc:
- a dose-matched control for A3, meaning a learner making the same number of updates without reverting;
- a convex world trained to convergence.

It runs only if the owner asks for it.

## What this means for the real-data test

- **Content cuts in continual learning have no hypothesis left standing.** None may enter a prereg until a gate reads
  OPEN.
- **The safety-with-continual-learning test on unseen data is already hashed.** SCL3 (`prereg/scl3/`, data step on or
  after 2026-09-25 00:00 UTC) runs the calibrated continual learner inside the operator-pause harness, in accordance with
  the pipeline. That is the real-data test this work prepares for. Its safety half is the construction A7 checked here
  once more.
- **The design lesson is unchanged.** Routine pauses stay empty cuts, scheduled by the operator. A cut with content,
  such as a reset, belongs on the learner's own task clock, and only where a gated hypothesis says it helps.

## What a surrogate would have done

The convex world (N-conv) is the surrogate on which every content cut had to fail. It did not: on plasticity, SP and Head
were ahead. Content at the cut therefore helped in a world with no plasticity loss in the literature's sense, and a
"content helps" claim is not specific to plasticity until a redesigned gate says otherwise.
