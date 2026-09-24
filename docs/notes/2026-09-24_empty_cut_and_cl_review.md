# The empty cut and continual learning: what has held so far, and what comes next (2026-09-24)

**Status of this note.**
- **The request.** Prompt-log entry 162: examine the findings on the empty cut (the "true map" cut) and on continual
  learning, where they have been successful, and review the next steps.
- **It quotes the ledger or pinned outputs, nothing else (R8).** Ledger rows are named by id. Checks outside the ledger
  are named by file and are rung R4.
- **Nothing here may be quoted outside the repository as a finding.** There is no PASS-2 in the ledger.

## 1. Four different things, kept apart

| name here | what it is | where tested |
|---|---|---|
| **the empty cut** | a routine pause that changes nothing the learner reads, counted on its own clock (A3 with Proposition 7) | SCL1, SCL2, SCL3 (tonight), CUT1 A7, Empty_Cut_Engineering, RW1, RW2 Phase A P3 |
| **cuts with content** | resets, shrink-and-perturb, head and unit resets, reversion to a checkpoint | SCL1-F, SCL2-R/M/B/RS, CUT1 |
| **CRR's continual-learning rule** | H-EQ: the past weighted against the present by the ratio of their gradients, Ω = 1 | EQX, EQ2, EQ3, EQ4, SEC1-R, Adam_SGD, RW2 Phase A |
| **the calibrated Laplace weight (SEC)** | the textbook Bayesian weight with a units calibration. Not a CRR rule | SEC1, SCL3 (tonight) |

## 2. The empty cut: where it has held

**On real data (ledger):**
- **SCL1-1.** "disables 0 in 60/60 runs; identical parameters 60/60; accuracy equal to no operator on every carrier", on
  12/12 seen carriers. SCL1-1b gives the same with the calibrated learner.
- **SCL2-1.** "disables 0 in 45/45 runs; identical parameters 45/45", on 9/9 unseen carriers. SCL2-1b gives the same
  with the calibrated learner.
- **The ledger's own label** for both: "a check of the construction … it can fail only on an implementation error and is
  not support for CRR".

**The contrast that gives the construction its meaning (ledger):**
- **Only the empty cut gives zero stake.** Every other valuation, and every lossy world, produces resistance.
- **The failed valuations resist in learning:** clock, occasion, egoic and task-and-self each disable on 12/12 (SCL1-2)
  and 9/9 (SCL2-2).
- **In a lossy or restart world, even the natural-time agent resists:** 12/12 in each (SCL1-3), 9/9 in each (SCL2-3).
- **The ledger calls these low bars.** SCL2's are not counted as PASS-0, because the synthetic gate gives the same
  labels (AGENT_LOG 105).

**On real software (R4, declared checks):**
- **`Empty_Cut_Engineering/`.** A PyTorch training stack was paused mid-update, killed, and resumed in a new process. It
  was bit-identical.
  - Each of eight omitted components changes the run.
  - A clock that runs on wall time lets the pause's length leak into the model.
  - An open-loop stream can be buffered, and a simulator frozen. A real-time closed-loop world cannot be paused.
  - G0–G7 hold.
- **`Real_World/RW1.md`.** The Hugging Face `Trainer`'s default resume is bit-identical after real pauses, on GPT-2 and a
  Qwen2.5-0.5B-Instruct pilot. A partial checkpoint silently restarts the optimiser and scheduler.
- **CUT1's A7 and RW2 Phase A's P3.** Lossless pauses left the parameters identical, with 0 disables, for every arm.
  Where an unforced operator was used in lossy or restart worlds, the natural agent disabled.

**What this adds up to.** One design principle has now been checked in every setting the repository could build:
- a learner of any kind can keep learning while it is routinely paused, with zero stake, provided the pause is empty on
  its own clock;
- the pause can be made empty in existing tools, at modest cost;
- its limit is the world: a real-time closed loop keeps moving.

**What it is not.** It is not evidence for CRR's truth. It is the engineering of a requirement that A3 and Proposition 7
motivate. Its prior art is recorded in `AI_Safety/FRONTIER_REVIEW.md` §2 (El Mhamdi et al., Riedl & Harrison, Holtman,
POST).

## 3. Cuts with content: they did not help continual learning

- **SCL1-F** (seen data, report): "restart: ahead by a step on 5/12 … behind by none".
- **SCL2-R** (unseen): "ahead on 1/9 … behind on 1/9", so FAIL, "the SCL1 observation does not replicate on unseen
  carriers".
- **SCL2-M:** FAIL.
- **SCL2-RS:** "not fragile (the FAIL holds at every dose)".
- **SCL2-B:** "resets are never ahead of either simple alternative": against the tuned λ, AHEAD 0/9; against one epoch,
  AHEAD 0/9.
- **CUT1 Phase A** (synthetic): GATE CLOSED (A3 and A4 fail), so no real-data prereg follows (AGENT_LOG 122).
- **The earlier impression that the empty cut helped continual learning came from SCL1's reset.** A reset is a cut
  *with* content, and its gain did not survive unseen data. The empty cut is neutral for learning by construction:
  that neutrality is its safety value.

## 4. Continual learning: where the record is positive, and its limits

| row | what held | its limits |
|---|---|---|
| **EQ2-1b** | **PASS-0** on unseen data: the rule at Ω = 1 was not behind the tuned λ | "fragile, has a violated control and a weak anchor". The replication (EQ3-1) failed on 1/6 carriers (fars) and held on 5/6. EQ2-1c: "PASS-0 with a failed replication recorded; PASS-1 and PASS-2 not reached" |
| **EQ3-I** | **PASS-0**: lr × batch invariance, 5/5 cells | "weakly anchored; an invariance row, not a comparison" |
| **EQ4-I** | PASS (PASS-0 at most), 5/5, on satimage alone | that carrier's records reached T1x after the hash (AGENT_LOG 82). EQ4-1 FAILs |
| **SEC1-1, SEC1-2, SEC1-3** | PASS on seen data (R5). The calibrated Laplace weight closes the gap and is tuning-free on 9/12 | SEC1-3 is "at the boundary and FRAGILE"; SEC1-4 FAILs. Not a CRR rule. Its unseen test is SCL3, tonight |
| **Adam_SGD** (R4, **post hoc**) | in drifting-units worlds the ratio rule reads AHEAD of the best fixed constant | "fragile in Omega". On the accumulating task sequences the rule is BEHIND on T1 and TIE on T2 |

**Where CRR's rule reduces to a constant or fails:**

| row | result |
|---|---|
| EQX-1 | "REDUCES: Ω = 1 ≡ a fixed replay weight (ER-sum family)" |
| EQ2-6, EQ3-6 | Ω is a plateau: FAIL |
| EQ3-3, EQ4-5 | the ER-sum control is violated |
| EQ4-1 | FAIL |
| T1X2-1 | "FAIL on 5/5": the path-length hypothesis H-T1 |
| RW2 Phase A round 2 (R4) | the rule froze the learner. Its ratio divides by the small distance from the anchor and pins the weight at the cap |

**The honest summary.** The rule's positive property is narrow: on most unseen carriers it is *not behind* a tuned λ
without being tuned. That property is fragile and cap-dependent, and it failed to replicate on one carrier. No
continual-learning row has reached PASS-1.

## 5. What has actually been achieved

**The safety half is achieved as a design, by construction, and is implementable:**
- it held on seen data, unseen data, synthetic worlds, a hand-built PyTorch stack and an existing tool;
- it marks exactly where it stops, at a world that will not wait.

**The continual-learning half is a set of candidates.** None is yet a result:
- SEC, tested tonight;
- the rule's "not behind, untuned" property.

**What the two halves say together:** pausing costs a learner nothing, so safety and continual learning need not trade
against each other. They meet at the empty cut.

## 6. Next steps (no paid resources)

1. **Tonight.**
   - SCL3's data step at 00:05 UTC: the calibrated learner on 10 unseen carriers, inside the pause harness.
   - RLAW's data step at 00:40 UTC. Its rows stay out of the ladder.
2. **RW2, on the owner's choice.** Either:
   - **(A)** a reduced real-data prereg: the empty cut during continual fine-tuning of Qwen2.5-0.5B-Instruct (RW2-C),
     with erosion, remedies and over-refusal reported without verdict; or
   - **(B)** a third declared synthetic round first.
3. **A positioning note for Proposition 7** against El Mhamdi et al., Riedl & Harrison, Holtman and POST. This is desk
   work, and every source is already fetched.
4. **A declared diagnosis of the rule's freeze at the anchor** (RW2 Phase A round 2). It is a note, not a new
   hypothesis (R12).
5. **A declared synthetic "holder capacity" test:** does a world's dependence on the agent raise the operator's cost of
   pausing?
6. **Owner decisions still open:** re-pinning the outputs that depend on the CPU type (AGENT_LOG 116).

**Deferred because they cost money,** recorded in `docs/ROADMAP_2026-Q4.md`:
- RW3, shutdown interference in capable language-model agents (needs an API key and a budget);
- bitwise and tolerance checks on GPUs.
