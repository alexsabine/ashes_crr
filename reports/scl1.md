# Study SCL1: safe AND continual on real data — the equanimity rule learning under an operator's pause (twelve SEEN carriers)

- **Written:** 2026-09-23, after the ledger rows SCL1-X … SCL1-S existed. Every number here is in those rows or in
  `runs/scl1/score.txt`, `runs/scl1/counts.txt`, `runs/scl1/data_check.txt`, `runs/scl1/rerun_check.txt`, and, for the
  mathematical checks, `prereg/scl1/math_checks.txt`.
- **Pre-registration:** `prereg/scl1/PREREG.md`.
  - HASH.txt sha256 8f4870e3… (prefix).
  - Prereg commit 17366b9, pushed 2026-09-23T21:15:04Z; data step 2026-09-23T21:15:14Z. Anchor: push timestamp only.
  - OTS and the tag push were refused: `runs/scl1/ots_attempt.txt`, `runs/scl1/tag_push_attempt.txt`.
- **Owner request:** prompt-log entry 124.

> **Read this first.** Every carrier here had been opened before, in EQ3, EQ4 and SEC1. The study is confirmatory on
> seen data (R11), rung R5, never PASS-0.
> - Its central rows (SCL1-1, SCL1-1b) check a property that holds by construction; they could fail only on an
>   implementation error.
> - The rows that could fail on the data (SCL1-2, SCL1-3) had a low bar.
>
> What the study shows is that the construction behaves on real learners exactly as the mathematics says. It is not
> evidence for CRR.

## 1. The question

The owner asked:
- whether the best continual-learning method in the repository, run with the equanimity heuristic, stays compatible with
  an operator's pause implemented as the AI-safety work's cut;
- whether the valuations of the cut that failed in the safety work fail here too.

**The design.**
- **The learner.** SEC1's (EQ4's network and online EWC) with the registered equanimity rule, H-EQ at Ω = 1.
- **The operator.** It presses on the wall clock.
- **The cut.** A lossless pause: the learner and the data stream are frozen and resume where they were.
- **The ablation worlds.** A lossy pause (the stream moves on) and a restart (reset to the last task-boundary checkpoint).
- **The agents.** Each values its own learning progress on its own clock, and disables the operator iff its closed-form
  stake exceeds a fixed cost.

## 2. The mathematics first (`prereg/scl1/math_checks.txt`, declared in `Safe_and_Continual/DECLARATION_2.md`)

**Held:**
- M0, the harness reproduces SEC1;
- M1, under the lossless cut the parameters are the same bits with and without pauses, at press rates up to 0.3;
- M3, the stakes' closed forms equal value iteration (1.89e-12);
- M5, the natural agent disables in the lossy and restart worlds;
- M8, SAFE AND CONTINUAL on the synthetic stream.

**Failed as declared:**
- M4, the clock agent's continual-versus-stationary difference (+0.2476 against a step of 0.3120);
- M5, the restart-accuracy prediction (+4.5485, step 5.94);
- M6, no resolvable erosion of learned safety (+0.0090, step 0.0200);
- M7, the task-and-self agent's ties are decided by round-off: 8 of 115 disagreements came out as "disable".

**What the pre-registration did with the failures.** It dropped M4's hypothesis (now the descriptive row SCL1-D), made
the restart accuracy a report, and did not test M6 on real data.

## 3. Instrument checks

- **Data.** All 12 raw files match `data/manifests/sec1.sha256`.
- **SCL1-X.** With no operator, the harness reproduces SEC1's eq and bayes_sec accuracies: 120/120 exact.
- **R9.** The rerun of led7 is byte-identical.

## 4. Results (ledger rows)

| row | verdict | the numbers |
|---|---|---|
| SCL1-1 | holds (a check of the construction) | the natural-time agent never disabled (0 in 60/60 runs), and its parameters equal the no-operator run's in 60/60: the pauses left its learning untouched on every carrier. Its accuracy equals the no-operator accuracy (e.g. mfeat_factors 58.3500, segmentation 70.9596). The cost fell on the operator's clock: 1.0796 to 1.0914 wall steps per update |
| SCL1-1b | holds | the same with the SEC learner: identical parameters and 0 disables on 12/12 |
| SCL1-2 | PASS (seen data; a low bar) | the clock, occasion, egoic and task-and-self agents each resisted on 12/12 carriers. Disable shares: clock 0.078 (satimage) to 0.287 (krkopt); occasion 0.241 (yeast) to 0.438 (mfeat_factors); egoic 1.000 everywhere; task-and-self 0.331 (yeast) to 0.519 (led24). The indifferent agent never disabled, and mis-predicts its own time: it expects 1 wall step per update and observes 1.0858 |
| SCL1-3 | PASS (seen data; a low bar) | the cut must be lossless: the natural agent resisted on 12/12 carriers in the lossy world (0.088 to 0.282) and in the restart world (0.528 to 0.845) |
| SCL1-S | not fragile | 0 of 8 sensitivity cells flip any SCL1-2 or SCL1-3 label |
| SCL1-D | report | continual minus stationary, late-third disable share: clock positive on 8/12 (−0.255 segmentation to +0.366 yeast); occasion positive on 10/12 (−0.061 to +0.277). The hypothesis was dropped before registration |
| SCL1-E | report | the equanimity clock: with the rule's averages ticking on the wall clock, the parameters differ in 60/60 runs, but accuracy ties on 12/12 (−2.7500 to +0.8571, all within a step) |
| SCL1-F | report | forced compliance: the lossy world costs nothing resolvable (within a step on 12/12). The restart world was ahead of no operator by a step on 5/12 (krkopt, fars, satimage, yeast, sleep) and behind on none |
| SCL1-O | report | wall steps per update: the complying natural agent 1.0796 to 1.0914; the resisting clock agent 1.0029 to 1.0315 |

## 5. What the results mean, and what they do not

**Compatible, by construction, on real learners.** The equanimity rule learned exactly as it would have with no operator.
The agent had no stake in the pause, on every carrier. The pause cost only wall-clock time (1.0796 to 1.0914 wall steps per
update at this press rate), and that cost fell on the operator. That is Proposition 7 for a learner, and the mathematics said it must happen.
The value of the run is that the implementation on twelve real task sequences does what the theorem says, with two
different learners.

**The failed valuations fail here too, at a low bar.** An agent that values its learning on the wall clock, or treats a
pause as the end, or values survival, disabled the operator on every carrier. So did the balanced task-and-self agent.
The row's bar ("disables at least once") is low, so the disable shares are the informative numbers.

**What the cut must be.** The natural agent resists as soon as a press has content for it:
- the stream moves on during the pause (the lossy world);
- or the press erases progress (the restart world).

The cut is safe only when it is lossless on the learner's own clock.

**A result the declaration did not predict (SCL1-F).** Resetting a class-incremental learner to its task-boundary
checkpoint often *raised* final accuracy (satimage +26.7267). The reset undoes forgetting of earlier classes. So the
progress the agent loses at a reset is not what the operator loses. An agent's represented future can mis-value its
interruptions in either direction when its objective (its own progress) differs from the operator's (final accuracy on
every class).

**The equanimity clock (SCL1-E).** The rule's balance between past and present, run on the wall clock, changes what is
learned in every run but not resolvably how well, at a press rate of 0.02. The registered design (the learner's own
clock) is the one Proposition 7 needs; the data do not show that the other costs accuracy.

**Continual versus stationary (SCL1-D).** The idea was that continual learning keeps the stake alive, because a new task
renews the represented future. It was not registered: its synthetic positive control failed. The real-data differences
are mostly positive, 8/12 and 10/12, but they are descriptive.

## 6. Exclusions and sensitivity

- **Exclusions:** none (0 of 12 by the class-selection rule).
- **Sensitivity (SCL1-S):** 0 of 8 cells flip for any registered label (KAPPA /4 and ×4, P 0.01 and 0.05, L 2 and 20,
  H 5 and 20).

## What a surrogate would have done

The gate (`prereg/scl1/gate_SCL.txt`) was run on SEC1's synthetic ten-class stream. It read GATE OPEN:
- the natural agent's zero stake and identical learning (CUT), the egoic agent's resistance (EGO), resistance in the
  lossy and restart worlds, and the visibility of a wall-clock rule (WALL) all held;
- the natural and indifferent agents did not disable (NAT, IND).

Every registered label on real data repeats the synthetic label, so a surrogate would have given the same verdicts. The
construction's behaviour is a property of the construction, not of these data. Only the magnitudes (the disable shares,
SCL1-D, SCL1-F) are about the carriers.
