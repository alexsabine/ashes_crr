# CRR against FOREVER: a comparative investigation on synthetic continual-learning worlds

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 181. The work is a declared synthetic battery (rung
R4).
- **Declaration.** `DECLARATION_2.md` was pushed at 359d850 before the script existed. Amendment 1 (headroom) was pushed
  at 1d61614 before any scored run.
- **Numbers.** Every number is from `checks/comparative.txt`, which is byte-identical on rerun. The headroom calibration
  is `checks/comparative_calibration.txt`.

## 1. What was run

**FOREVER's choices.** FOREVER (arXiv 2601.03938 v2) was broken into six choices:
- the clock;
- the unit;
- what is measured;
- the replay weight;
- the anchor;
- replay sampling.

**The CRR swaps.** Each choice was swapped, one at a time, for the one a CRR commitment makes:
- the Fisher arc (D2/D6);
- A1′'s robust unit;
- the Fisher chord (D3);
- the step-bounded weight (H-EQ);
- the normalised age-weighted anchor (A6 + P3);
- age-weighted sampling (P3);
- surplus-weighted sampling (P2).

**The full learner.** CRR-full makes all the CRR choices at once.

**Every run was controlled the same way.**
- **Replay budget.** Every event-based arm gets exactly the same budget, so the arms differ only in when and how replay
  acts.
- **Pairing.** Data, initialisation and batch order are identical across arms, so each comparison is paired by seed.
- **Worlds and seeds.** Seven worlds, 10 seeds each.
- **Labels.** Each arm is compared with FOREVER by the paired mean difference in final accuracy (OP), against a step of
  max(1.0, 2 SE).

**The headroom repair (Amendment 1).**
- The declared generator gave near-100 % accuracy with no forgetting, so every arm would have tied by construction.
- The generator was recalibrated on an unscored seed, using baselines only.
- All seven worlds then pass the headroom precondition. For example, fine-tune BWT is −28.32 in W1 and −89.80 in W6.

**FOREVER's β_base.** It was tuned once on W1 with separate tuning seeds, giving 1, and held fixed everywhere.

## 2. Results

Paired mean difference against FOREVER, in accuracy points, with the label:

| arm | W1 base | W2 null movement | W3 parametrisation | W4 learning rates | W5 convex | W6 class-incremental | W7 long (15 tasks) |
|---|---|---|---|---|---|---|---|
| FOREVER (OP) | 78.97 | 78.93 | 78.02 | 79.10 | 79.78 | 39.25 | 74.72 |
| B0 fine-tune | −9.81 B | −9.85 B | −7.03 B | −6.39 B | −10.04 B | −21.08 B | −9.09 B |
| B1 ER-mix (8.6× the replay batches) | −5.13 B | −5.14 B | −3.90 B | −3.58 B | −5.66 B | −2.20 B | −1.93 B |
| B2 fixed-interval replay | −0.82 T | −0.19 T | +0.78 T | −0.90 T | −0.73 T | **+10.25 A** | −1.56 B |
| B3 step clock | +0.15 T | +0.23 T | +0.56 T | −0.29 T | −0.07 T | **+2.83 A** | −0.08 T |
| C1 Fisher arc | −0.10 T | −0.71 T | −0.29 T | −0.15 T | −0.17 T | +0.13 T | −0.17 T |
| C2 Fisher arc + A1′ robust unit | +0.12 T | −0.23 T | +0.12 T | +0.05 T | −0.03 T | **+1.74 A** | +0.05 T |
| C3 Fisher chord | −1.87 B | −3.08 B | −2.90 B | −0.62 T | −1.90 B | −3.54 B | −0.90 T |
| C4 H-EQ weight | −0.70 T | −0.03 T | +0.51 T | −0.27 T | −0.47 T | −11.95 B | −0.66 T |
| C5 A6 anchor | −0.54 T | −0.80 T | −1.50 B | −0.40 T | −0.73 T | −3.41 B | +0.54 T |
| C6 P3 sampling | −0.10 T | −0.02 T | +0.37 T | −0.53 T | −0.26 T | +0.17 T | −1.73 B |
| C7 P2 sampling | −0.05 T | +0.08 T | +0.21 T | −0.34 T | −0.11 T | −0.43 T | +0.11 T |
| CRR-full | −1.51 B | −0.77 T | −0.68 T | −0.56 T | −0.60 T | −13.58 B | +0.65 T |

A = AHEAD, T = TIE, B = BEHIND.

**The gate for the clock claims** (declared): **CLOSED.**
- The negative control held: no clock arm read AHEAD in the convex world.
- The positive control failed: the Fisher arc did not read AHEAD in the null-movement world (−0.71, TIE).
- The sensitivity check (S = 12 and 48) flips in 0 of 4 cells.

**The predictions** (declared):
- **Hold:** P3, P5, P7, P8 and P10.
- **Fail:** P1, P2, P4, P6 and P9.
  - P1 is the gate's positive control.
  - P2 failed because the chord is BEHIND in the convex world.
  - P4: the step clock is not behind FOREVER in the learning-rate world.
  - P6: the A6 anchor is BEHIND in W3 and W6.
  - P9: ER-mix is BEHIND everywhere.

## 3. What FOREVER is, on this evidence

1. **Its gain here comes from the anchored replay, not from its clock.**
   - Fixed-interval replay and step-calibrated replay, with FOREVER's weight and anchor, tie FOREVER in all five
     domain-incremental worlds of 5 tasks.
   - Plain replay mixed into every step, with no anchor, is behind FOREVER in every world. That holds despite 8.6 times
     as many replay batches.
2. **The model-time clock did not help where it was built to.**
   - In the world with learning rates varied ×(1, 4, 0.25, 2, 0.5), the step clock is −0.29, a TIE.
   - The paper reports model time ahead of step calibration by 1.2 OP on its LLM benchmarks. That did not reproduce in
     these miniatures.
3. **In class-incremental learning, FOREVER's increasing spacing was the wrong shape.**
   - Evenly spaced replay is +10.25 and step spacing +2.83 against FOREVER's τ schedule.
   - A likely reason, not tested here: FOREVER's early replays fire while the new task's classes are still being learned.
   - Two readings of FOREVER's BWT in W6 need care. It is positive (+23.10) because accuracy right after each task is
     measured after that task's end-of-task replay events. And plain fine-tuning forgets almost everything (−89.80).

## 4. What CRR is, on this evidence, and whether it enhances FOREVER

| CRR commitment | swap | result | reading |
|---|---|---|---|
| D2/D6: the Fisher metric for the clock | C1 | TIE in 7 of 7 | Declaration 1 showed the Fisher clock is invariant and blind to null movement (F1, F2). With a fixed replay budget, that property **did not change accuracy** in any world. The gate is closed (R12): **no clock claim goes to a prereg**, and ARC-R as designed is not licensed |
| A1′: a robust unit | C2 | AHEAD in class-incremental (+1.74, step 1.00); TIE in 6 | the one swap that improved FOREVER anywhere, in one world. It is a candidate only: one cell, just over the step, and not gated |
| D3: the chord (the endpoint, which the ledger found predicts forgetting) | C3 | BEHIND in 5 of 7 | as a replay clock the chord is worse. Predicting forgetting (T1X2) is not the same as scheduling replay |
| H-EQ: the step-bounded weight | C4 | TIE in 6; BEHIND by 11.95 in class-incremental | no gain where FOREVER's β_base is well tuned, and a large loss where the anchor must give way |
| A6 + P3: the anchor | C5 | TIE in 5; BEHIND in W3 and W6 | the normalised average of past task ends is a worse anchor than the last task's end here |
| P3: age-weighted sampling | C6 | BEHIND in the 15-task stream (−1.73) | as predicted (P7): weighting by age starves old tasks |
| P2: surplus weights | C7 | TIE in 7 of 7 | inert, as the SAL gate found |
| all of them | CRR-full | TIE in 5; BEHIND in W1 (−1.51) and W6 (−13.58) | the combination does not enhance FOREVER. It inherits H-EQ's and A6's losses in class-incremental learning |

**The answer to the question asked.**
- **FOREVER is CRR-shaped.** It is an own-clock arc reset at the cut (Declaration 1).
- **Its measured value here lies in the anchored replay,** with a tuned weight, not in the clock.
- **None of the CRR swaps enhances FOREVER in a way that survives these worlds.** The Fisher metric's properties are real
  mathematics (F1, F2) with no accuracy consequence at a fixed replay budget.
- **One lead remains:** A1′'s robust unit in class-incremental learning (+1.74). It is a single world, just over the step,
  and it would need its own declaration and gate before it could mean anything.
- **The schedule's shape mattered more than its clock.** In the class-incremental world, evenly spaced replay beat
  FOREVER's forgetting-curve spacing by 10.25 points. CRR says nothing about spacing.

## 5. Limits

- Small numpy models, not LoRA-adapted language models.
- Seven synthetic worlds, with a generator chosen after a headroom failure (Amendment 1, calibrated on an unscored seed).
- γ in FOREVER's weight is not stated in the paper; γ = 1 was used.
- One tuned β_base, held across worlds.
- These are R4 results. They can close a gate but cannot establish a finding.
