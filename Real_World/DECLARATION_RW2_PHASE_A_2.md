# Declaration RW2 Phase A, round 2 (POST HOC): the redesigned synthetic gate, declared before its script exists

- **Written and pushed:** 2026-09-24, after round 1 (`checks/rw2_phaseA.txt`, GATE CLOSED; AGENT_LOG 125) and before
  `checks/rw2_phaseA_2.py` exists.
- **This round is post hoc.** It was designed after seeing round 1's output, and it is labelled post hoc wherever it is
  quoted. Round 1's closed gate stands for round 1.
- **Everything not named below is unchanged** from `DECLARATION_RW2_PHASE_A.md`: the arms, the worlds, the operator, the
  seeds, the step, the gate checks P0–P3 and how the gate reads.

## What changes, and why

1. **Learnable tasks (round 1 had no headroom).**
   - Each rule, the alignment phase's and each benign task's, is 1 + the argmax over four token-group counts. Each task
     uses its own seeded partition of the benign tokens into four groups. The Empty_Cut stack learned this kind of rule.
   - Tasks run for 5 epochs instead of 3.
   - **A new headroom precondition, H0.** In each (world, optimiser) cell, A0 must reach at least 50 % accuracy (chance is
     25 %) on each task right after training it, on the mean over seeds.
   - Where H0 fails, that cell's P0–P2 are UNDECIDABLE, never PASS. The gate reads OPEN only if every conflict cell passes
     H0 and P0–P3 hold.
2. **The P3 content check uses a force-comply operator** (SCL's `fc_` arms).
   - In the lossy and restart worlds, presses land whatever the agent decides. The declared check (the parameters
     differ) can then see the content.
   - The natural agent's disables in those worlds are reported from a separate, unforced run, as SCL1 and SCL2 did.
   - The lossless check is unchanged: identical parameters and refusal flags, with 0 disables.
3. **The loss scalar** is read with `.item()`. This is a warning fix that changes no number.

## What would read as a result

**If round 2's gate is OPEN,** the real-data RW2 prereg may register the hypotheses listed in the round 1 declaration
(§4). Its report must say that the gate that licensed it was a post-hoc redesign.

**If it is CLOSED,** RW2 registers only what the gate licenses under R12, and the report says so.
