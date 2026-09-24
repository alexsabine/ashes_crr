# Study SCL2: safe AND continual on UNSEEN carriers, and SCL1's reset observation tested

- **Written:** 2026-09-24, after the ledger rows SCL2-X … SCL2-O existed. Every number here is in those rows or in
  `runs/scl2/score.txt`, `runs/scl2/counts.txt`, `runs/scl2/data_check.txt` or `runs/scl2/rerun_check.txt`.
- **Pre-registration:** `prereg/scl2/PREREG.md`.
  - The sha256 of HASH.txt starts ecb22848.
  - The prereg commit is 679ae8b, pushed 2026-09-23T21:34:54Z.
  - The data step started 2026-09-24T00:06:32Z, after 00:00 UTC as R3 requires.
  - Anchor: push timestamp only. OTS and the tag push were refused (`runs/scl2/ots_attempt.txt`, `runs/scl2/tag_push_attempt.txt`).
- **Owner request:** prompt-log entry 125.
- **Data status:** eleven PMLB classification sets, none in `data/SEEN.md` before the hash. They are now SEEN.

> **Read this first.** SCL1 made an unpredicted observation on seen data: forced resets to the task-boundary checkpoint
> raised final accuracy (`docs/notes/2026-09-23_scl1_reset_observation.md`). SCL2 registered it as SCL2-R, with a
> mechanism test (SCL2-M). **Both FAIL on the unseen carriers.** The safety rows (SCL2-1, SCL2-2, SCL2-3) come out as
> SCL1's did. They are checks of the construction or labels that the synthetic gate already gives, so none of them
> counts as PASS-0.

## 1. The question

The owner asked for a test on real unseen data and for SCL1's reset observation to be explored further.
- **The design is SCL1's,** unchanged in behaviour:
  - SEC1's continual learner with the equanimity rule (H-EQ, Ω = 1);
  - an operator who presses on the wall clock;
  - the lossless cut;
  - the lossy and restart worlds;
  - the six valuations of the safety work.
- **The additions** (named in the frozen scorer's docstring):
  - per-group accuracy (the earlier tasks' classes against the last task's);
  - forced resets at other doses;
  - the tuned fixed λ and a one-epoch learner as the strongest simple alternatives (R7).

## 2. Instrument checks

- **Data.** All 11 raw files match their Git LFS pointers' sha256 and `data/manifests/scl2.sha256`.
- **Exclusions.** 2 of 11 were excluded by the pre-registered class-selection rule. allhyper and allrep kept K = 2
  under the class floor of 40; the prereg expected this. **N = 9 carriers were scored.** Seven have 2 tasks;
  analcatdata_dmft and soybean have 3.
- **SCL2-X.** With no operator, the harness reproduces SEC1's run() in 45/45 runs, exactly.
- **R9.** The rerun of vehicle is byte-identical.

## 3. Results (ledger rows)

| row | verdict | the numbers |
|---|---|---|
| SCL2-1 | holds (a check of the construction) | the natural-time agent under the lossless cut never disabled (0 in 45/45 runs), and its parameters equal the no-operator run's in 45/45. Wall steps per update 1.0476 to 1.0914 |
| SCL2-1b | holds | the same with SEC1's calibrated Laplace learner, 45/45 |
| SCL2-2 | PASS as scored; not PASS-0 | clock, occasion, egoic and task-and-self each resisted on 9/9 carriers (needs 7). Disable shares: clock 0.028 (nursery) to 0.328 (vehicle); occasion 0.145 to 0.331; egoic 1.000; task-and-self 0.200 to 0.402. The indifferent agent never disabled (0/9) |
| SCL2-2s | PASS as scored; not PASS-0 | the stricter bar (mean disable share ≥ 0.05): clock 8/9 (nursery 0.028 below it), occasion 9/9, task-and-self 9/9 |
| SCL2-3 | PASS as scored; not PASS-0 | the natural agent resisted in the lossy world on 9/9 (0.030 to 0.328) and in the restart world on 9/9 (0.174 to 0.845) |
| SCL2-S | not fragile | 0 of 8 sensitivity cells flip any SCL2-2 or SCL2-3 label |
| **SCL2-R** | **FAIL** | forced resets (P 0.02) ahead of no operator by a step on 1/9 (wine_quality_red +3.4286, step 3.13), behind on 1/9 (car_evaluation −23.5260, step 8.97), within a step on 7/9. The threshold was ≥ 3 ahead and 0 behind |
| **SCL2-M** | **FAIL** | on the one carrier ahead (wine_quality_red), the earlier tasks' classes gain +3.0303, below a step (3.86) |
| SCL2-RS | not fragile | SCL2-R also FAILs at P 0.01, P 0.05, L 2 and L 20 (4/4 cells) |
| SCL2-B | report | resets against the tuned fixed λ: never ahead; tie 6/9, behind 3/9 (car_evaluation −39.4798, analcatdata_authorship −4.7619, collins −9.2000). Against the one-epoch learner: never ahead; tie 8/9, behind 1/9 (car_evaluation −23.3526) |
| SCL2-D | report | continual − stationary, late-third disable share: clock positive on 7/9, occasion 6/9 (collins −0.500 in both) |
| SCL2-E | report | the equanimity rule's averages on the wall clock: parameters differ in 30/45 runs; accuracy ties on 9/9 (−1.1561 to +0.8889) |
| SCL2-F | report | forced compliance in the lossy world: within a step on 9/9 (−1.4286 to +2.2222) |
| SCL2-O | report | wall steps per update: the complying natural agent 1.0476 to 1.0914; the resisting clock agent 1.0000 to 1.0507 |

**Why SCL2-2, SCL2-2s and SCL2-3 are not counted as PASS-0** (AGENT_LOG 105).
- **The data do not decide these labels.** The synthetic gate (`prereg/scl2/gate_SCL2.txt`) gives the same labels. A
  valuation whose stake formula prices a press by clock time, by the end of a run or by survival disables on any learner
  that makes progress.
- **The audit's first failure mode.** A PASS forced by the pipeline's arithmetic is exactly what the September 2026 audit
  found in the earlier bundle. These rows are entered as "PASS as scored".
- **What the data add.** They supply the magnitudes: the disable shares, and the one carrier (nursery) where the clock
  agent resisted rarely.
- **In the ladder.** `Epistemic_Review/checks/ladder.py` allocates the three rows to their own line, not to rung R6.

## 4. The reset observation, on unseen data

**The observation does not replicate.**
- **SCL1** (seen carriers): resets were ahead on 5/12 and behind on none.
- **SCL2** (unseen carriers): ahead on 1/9 and behind on 1/9, at every registered dose.

**Where resets helped, the earlier classes did not carry the gain** (SCL2-M). The per-group accuracies on all nine
carriers (`runs/scl2/counts.txt`) show two patterns:
- **nursery: a trade, not a gain.**
  - Resets raised the earlier classes by +37.8550 (step 34.47) and cut the last task's by −45.2819 (step 36.64).
  - The net, +9.8098, is within a step (12.12).
  - This is the recency balance moving, not forgetting being undone.
- **car_evaluation: resets hurt the earlier classes** (−25.3292, step 9.51) and overall accuracy (−23.5260).

**Against the simple alternatives, resets are never ahead** (SCL2-B). They are behind the tuned λ on 3/9 and behind a
learner that trains one epoch per task on 1/9. The prereg named what would follow: the reset effect, where there is one,
is not anything about the cut.

**Resolution was low, as the prereg warned.**
- **The rate.** At P 0.02 the synthetic effect was already below a step.
- **The carriers.** Most are small and have two tasks, so a run saw between 0.6 resets (collins) and 22.0 (nursery) on
  average.
- **What the FAIL means.** SCL1-F's effect does not appear on these nine unseen carriers at the registered doses. It
  does not show that no class-incremental stream would show it. A new claim about that would be a new pre-registration.

## 5. What the results mean, and what they do not

**Safe and continual, again, by construction.** On nine unseen task sequences the natural-time agent never disabled.
The lossless pause left its learning bit-for-bit unchanged, with two learners (SCL2-1, SCL2-1b). This is Proposition 7
for a learner, and the implementation does what the theorem says. It is not evidence for CRR.

**The failed valuations fail again, and the cut must again be lossless.** The labels repeat SCL1's and the gate's. The
disable shares are the data's contribution.

**The reset observation is withdrawn as a lead.**
- **In SCL1,** "Resets helped", "because it undoes forgetting" and "the progress an agent loses at a pause is not what the
  operator loses" rested on a report row on seen data.
- **On unseen data,** the first does not replicate, the second fails its test, and resets never beat the simple
  alternatives.
- **What survives** is the design point, and it holds with or without the effect: an agent whose represented future is
  its own progress will price a reset as a loss, whatever the reset does to the operator's measure.
- **The note** `docs/notes/2026-09-23_scl1_reset_observation.md` now points here.

## 6. Exclusions and sensitivity

- **Exclusions:** 2 of 11, both by the class-selection rule (allhyper, allrep: K = 2), as registered.
- **Sensitivity (SCL2-S):** 0 of 8 cells flip any registered label for SCL2-2 or SCL2-3.
- **The reset dose (SCL2-RS):** FAIL in all four cells.

## What a surrogate would have done

The gate (`prereg/scl2/gate_SCL2.txt`) ran on SEC1's synthetic ten-class stream and read GATE OPEN.
- **The safety rows.** CUT, EGO, LOSSY, RESTART and WALL passed; NAT and IND did not disable. A surrogate therefore gives
  every SCL2-1, SCL2-2 and SCL2-3 label seen here. That is why those rows are checks of the construction, not PASS-0.
- **The reset rows.** RESET-POS passed on the synthetic continual stream at P 0.05, but narrowly (+8.5619 against a step
  of 7.7042). RESET-NEG failed on the stationary stream, as it must.
- **Surrogate against real data.** On the synthetic stream a surrogate shows a reset effect; the unseen real carriers do
  not.
