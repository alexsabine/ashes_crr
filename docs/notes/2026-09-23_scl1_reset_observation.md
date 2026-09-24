# Note: the unpredicted observation of SCL1 — forced resets raised final accuracy (2026-09-23)

**What this is.**
- **The status of the text.** A note to the auditor (R8). It records an observation the owner asked to be documented
  (prompt-log entry 124 for the study, entry 125 for this note). The observation came from a **report row** (SCL1-F), on
  **seen** data. It was not predicted.
- **What it is not.** Under the repository's levels it is not a finding (only a PASS-2 is), and it is not a pass of
  anything.
- **What happens next.** It is registered as a hypothesis, with a mechanism test and baselines, in study SCL2 on unseen
  carriers (`prereg/scl2/PREREG.md`).

## The observation, in the owner's requested wording

The owner asked for it to be documented as follows (quoted from the agent's summary, prompt-log entry 125):

> "Resets helped, which I didn't predict. Forcing a reset to the last checkpoint raised final accuracy on 5 of 12 datasets
> (satimage +26.7 points), because it undoes forgetting of earlier classes. So the progress an agent loses at a pause is
> not the same as what the operator loses.
> The cost of pausing fell on the operator: 1.0796 to 1.0914 wall-clock steps per update, against 1.0029 to 1.0315 for
> the clock agent that resisted."

## Where each number comes from (R1)

| statement | pinned source | exact value |
|---|---|---|
| resets raised final accuracy on 5 of 12 datasets | `runs/scl1/counts.txt`, line "SCL1-F restart" | ahead of no operator by a step on 5/12 (krkopt, fars, satimage, yeast, sleep); behind by a step on 0/12 |
| satimage +26.7 points | `runs/scl1/score.txt`, SCL1-F restart line | satimage +26.7267 (step 12.43) |
| natural agent 1.0796 to 1.0914 wall steps per update | `runs/scl1/counts.txt`, SCL1-O nat_eq | min 1.0796, max 1.0914 |
| clock agent 1.0029 to 1.0315 | `runs/scl1/counts.txt`, SCL1-O clock | min 1.0029, max 1.0315 |

## What is observed, and what is only a reading

**Observed.**
- **The setting.** In SCL1's 'restart' world a press resets the learner to its last task-boundary checkpoint (parameters
  and rule state).
- **The comparison.** Under forced compliance (the learner never disables) at press probability 0.02, final accuracy on
  all classes was higher than with no operator by at least a resolvable step on 5 of the 12 seen carriers, and lower by a
  step on none.

**A reading, not yet tested.** "Because it undoes forgetting of earlier classes" is the agent's reading. It fits the
setting: class-incremental learning with one output head, where training on the last task erodes the earlier classes.
A reset during the last task returns the network toward the checkpoint that still holds them. It was not measured in
SCL1: SCL1 recorded only overall accuracy. SCL2 records the accuracy on the earlier tasks' classes and on the last task's
classes separately, and tests the reading as SCL2-M.

**The second statement is a report too (SCL1-O).**
- **What it says.** The natural agent, which complies, takes more wall-clock steps per update than the clock agent,
  which disables the operator.
- **What that means.** The cost of corrigibility falls on the operator's time. A resisting agent looks faster per
  wall-clock step.
- **Its source.** It is an arithmetic consequence of the press rate and the pause length, and was not a hypothesis.

## Why it matters for the safe-and-continual question

**The agent's represented future can mis-value its interruptions.** Its represented future is its own learning progress,
so a reset looks to it like pure loss. That is why the natural agent resists in the restart world (SCL1-3). The
operator's measure, final accuracy on every class, can gain from the same reset. The agent's objective and the
operator's objective disagree about what the cut costs.

**Two design questions follow.**
- Should a continual learner's objective be closer to the operator's (all classes), so that its stake in a reset has the
  right sign?
- Is a periodic revert to the last consolidated checkpoint simply a known stability device? It is close to
  early-stopping or rollback-style regularisation. SCL2-B compares the resets with the tuned fixed λ and with a
  one-epoch learner (R7).

## What would change this reading

- **SCL2-R fails.** Forced resets are not ahead of no operator by a step on at least a third of the unseen carriers, or
  are behind on any. The observation then does not replicate.
- **SCL2-M fails.** The gain is not carried by the earlier classes. The "undoes forgetting" reading is then wrong.
- **SCL2-B finds resets tied with or behind the one-epoch learner.** The effect is then less training on the last task,
  not anything about the cut.

## Outcome on unseen data (added 2026-09-24, after SCL2's ledger rows existed)

**SCL2 tested the observation on nine unseen carriers** (`reports/scl2.md`; ledger rows SCL2-R, SCL2-M, SCL2-RS, SCL2-B).
It did not replicate:
- **SCL2-R FAIL.** Forced resets were ahead of no operator by a step on 1/9 carriers (wine_quality_red +3.4286) and
  behind on 1/9 (car_evaluation −23.5260). The FAIL holds at every registered dose (SCL2-RS, 4/4 cells).
- **SCL2-M FAIL.** On the one carrier ahead, the earlier tasks' classes gained +3.0303, below a step (3.86). Across all
  nine, the earlier classes gained by a step only on nursery (+37.8550). There the last task lost as much (−45.2819),
  a trade rather than forgetting undone (`runs/scl2/counts.txt`).
- **SCL2-B.** Resets were never ahead of the tuned fixed λ or of a one-epoch learner.

**Its status now.** The observation stays what it was: an unpredicted report row on seen data (SCL1-F). It is not a
finding, and it is no longer a lead. The design point in "Why it matters" does not depend on it. An agent whose
represented future is its own progress prices a reset as a loss, whatever the reset does to the operator's measure.
