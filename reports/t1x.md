# Study T1x — VOID (2026-09-22)

Ledger row T1X-VOID. Prereg `prereg/t1x/PREREG.md`, hash `872d083a`, anchor push-timestamp only (prereg commit ce825dd
pushed 2026-09-22T16:23:24Z; data fetched 16:23:30Z). Frozen scorer `runs/t1x/frozen/t1x_score.py`.

## What happened

The six unseen regression carriers were fetched after the push and the frozen scorer was run on each. It could not
run or score the study as pre-registered:

- On `215_2dplanes` the scorer crashed at its first run. Feature 0 of that carrier takes two values, so the pre-registered
  split ("task 1 = rows with feature 0 at or below its median") left task 2 empty; the task-2 base loss was NaN and the
  run's finiteness flag became a numpy boolean that the JSON writer refuses (`runs/t1x/log_215_2dplanes.txt`).
- On `218_house_8L` the runs completed but `score` crashed. The same split produced a task 2 whose base test MSE was
  95.0061 against 0.5772 on task 1; 54 of 108 runs were dropped by the divergence rule, the rest carried non-finite path
  lengths, and the held-out fit raised a LinAlgError after printing that carrier's lines (`runs/t1x/score.txt`, 20 lines).

Under CLAUDE.md §8 a frozen script that must be changed after the hash voids the study. The four other carriers
(`344_mv`, `564_fried`, `1193_BNG_lowbwt`, `294_satellite_image`) completed 108 runs each and are pinned unscored in
`runs/t1x/results_*.jsonl`. They are not scored separately: leaving a carrier out is a post-hoc exemption (R6). All six
carriers are now in `data/SEEN.md`. This is the second void study of the repository (EQ2R, 2026-09-21).

## What the frozen scorer printed before it crashed

The 20 lines in `runs/t1x/score.txt` are the scorer's own output for `1193_BNG_lowbwt` and the first lines for
`218_house_8L`. They carry no verdict; they are quoted here only as the record of what ran. For `1193_BNG_lowbwt` the
precondition read decidable (path spans 6.49× to 39.81× within each learning rate), the held-out R² with the learning
rate controlled read C_new 0.024, C_old 0.026, E_new −1.556, E_old 0.776, EWC distance 0.139, and the S/C* median was
51.137 (the per-step path is fifty times the chord: mini-batch wiggle). Whether that pattern holds on unseen carriers is
the question T1x2 asks; this study cannot answer it.

## The replacement

T1x2 (`prereg/t1x2/`, hashed 2026-09-22, data on or after 2026-09-23 under R3) carries four corrections learned on
today's carriers and named there: the finiteness flag cast to a Python boolean; the split feature taken as the first
column with at least twenty distinct values, a carrier with none excluded and counted; a carrier admissibility gate (base
task-2 test MSE at most 20 × task-1's, else excluded and counted); runs with any non-finite predictor or forgetting
dropped from the fits and counted. Its synthetic smoke exercises both exclusions before the hash. Six unseen regression
carriers remain on the mirror for it.

## Sensitivity table, exclusions, what a surrogate would have done

No sensitivity table (no row scored). Exclusions: two carriers on which the frozen scorer failed, four unscored. The
surrogate gate (`prereg/t1x/gate_T1.txt`) read OPEN and the synthetic end-to-end smoke read FAIL for H-T1 with the
old-probe endpoint at R² 0.999; neither could see a binary split feature or a 165× extrapolation, because the synthetic
carrier had neither. T1x2's smoke has both.
