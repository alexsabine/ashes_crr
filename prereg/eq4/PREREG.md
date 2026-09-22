# Pre-registration — EQ4: the bounded normalised penalty step (EQ-B) on six unseen PMLB streams, beside the registered rule, with a poisoned regime

Study id: `eq4`. Written 2026-09-22 (prompt-log entry 74), hashed and pushed the same day; **the data step is on or
after 2026-09-23 UTC** (R3, below). Author: the agent, under CLAUDE.md §1. Anchoring: push timestamp only (below).

## What this study is
The replication test of the EQ3 design with the rule enhanced by what the cross-verification and the reprocessed
mathematics taught (`Continuous_Learning/CROSS_VERIFICATION.md` §4; `theory/checks/omega_reprocessed.txt`;
`docs/notes/2026-09-22_h_eq_reprocessed.md`). The enhancement, **EQ-B**, bounds the present gradient before the
equanimity ratio is taken; on clean streams it must be idle (EQ4-2), and on a poisoned stream, where the registered rule
amplifies the past pull in proportion to an extreme present batch, it must be load-bearing (EQ4-3, EQ4-4). The
registered rule runs beside it on every arm, so EQ3-1 is replicated on fresh carriers at the same time (EQ4-1r).

## What the mathematics and the surrogates said first (same day, no unseen data)
- `theory/checks/omega_reprocessed.txt` [4]: on the two-task quadratic, the registered rule's total exceeds twice its
  clean value under a poison of (×100, 5 steps) and diverges at (×1000, 5); the tuned fixed weight diverges at (×1000, 5);
  EQ-B survives the whole sweep and equals the rule on the clean stream (3.4789 vs 3.4789).
- `gate_EQB.txt` (this folder): GATE OPEN. EQ-B at Ω = 1 is not behind the tuned weight on the S-Y positive control
  (0.1745 vs 0.1977) and on the poisoned S-Y row (0.6287 vs 0.7289); behind on S-R, S-X and S-Y/LwF (negative controls).
- `gate_EQBM.txt`: GATE OPEN. EQ-B is ahead of the registered rule only on the poisoned row (+0.223 relative, 5/5 seeds);
  on the clean S-Y row the two agree (−0.002).
- `runs/eq4_dev/summary.txt` (six SEEN EQ3 carriers, exploratory): clean EQ-B equals the rule on every carrier (clip
  fraction ≤ 0.001); poisoned EQ-B is ahead of the rule on 6/6 (2.64 to 20.75 points) and ahead of the fixed weight
  with the same clip on 5/6 (behind on led7 by 1.72 with step 1.00).

## R3 statement
EQ-B (the clip, its reference statistic, κ = 2, N = 50, N_MIN = 10, the history of kept lengths, the reset at task
boundaries), the poisoned regime's placement rule, the class-selection rule and the seed-mean gate statistic were all
defined on 2026-09-22 after seeing (i) the S-Y surrogate rows, (ii) the six EQ3 carriers (mfeat_factors,
mfeat_morphological, led7, led24, krkopt, fars; `runs/eq4_dev/`), and (iii) EQ3's class-count headers (fars). The first
EQ-B (median reference) was rejected on the S-Y rows (AGENT_LOG 63). None of it may be used on another dataset the same
calendar day: **no carrier below is fetched or opened before 2026-09-23 00:00 UTC**, and the fetch timestamp in
`data/manifests/eq4.sha256` and `data/SEEN.md` is the record.

## Anchoring — read this first
As EQ3: OpenTimestamps calendars are unreachable from this environment and tag pushes are refused by the remote (the
attempts are recorded in `runs/eq4/ots_attempt.txt`, `runs/eq4/tag_attempt.txt`, `runs/eq4/tag_push_attempt.txt`). The
only external witness to "before" is the GitHub push timestamp of the commit carrying `HASH.txt`. Every ledger row of
this study carries `anchor: push-timestamp only`; the strongest label available is PASS-0 until Daniel stamps
`HASH.txt` under the two-person protocol or re-runs the frozen scripts on his machine.

## Hypothesis under test (H-EQ-B)
The rule `g = g̃_present + w · g_past`, `w = Ω · ‖ĝ̃_present‖ / ‖ĝ_past‖`, Ω = 1, where `g̃_present` is the present
gradient clipped to κ × the largest kept length among the last N present batches (κ = 2, N = 50; no clip until N_MIN = 10
lengths are known; the history holds the kept lengths and restarts at every task boundary), is (i) not behind the tuned
λ by a resolvable step on every carrier when the past term is the online-EWC penalty (EQ4-1, the EQ3-1 claim carried by
the bounded rule); (ii) within a step of the registered rule on every clean carrier (EQ4-2: the bound is idle where
nothing is extreme); (iii) not behind the tuned fixed weight **with the same clip** on every poisoned carrier (EQ4-3);
and (iv) ahead of the registered rule by a step on at least half of the poisoned carriers (EQ4-4: the enhancement is
load-bearing exactly where the mathematics says the rule amplifies). The scope of H-EQ is narrowed, as the reprocessing
proposes, to past terms that are losses or curvature penalties on the past: DER++ and LwF are run and reported (EQ4-D),
not scored, and the ER-sum reduction control stays (EQ4-5).

## Gate (R4) — `gate_EQB.txt`, `gate_EQBM.txt`, committed here and covered by the hash
Run on 2026-09-22 on the instrument frozen in `runs/eq4/frozen/`. EQB: must fail on S-R, S-X, S-Y/LwF (it does: behind
by +0.177, +0.070, +2.468 on the seed means); must pass on S-Y (online EWC, 16× mismatch) and on the poisoned S-Y (it
does: −0.117, −0.137). EQBM: must pass only on the poisoned row (+0.223, 5/5 seeds) and fail on the clean S-Y (−0.002)
and S-R (+0.000): OPEN. The gate statistic for EQB is on the seed means (the study's criterion), not gate_EQ2's mean of
per-seed ratios (AGENT_LOG 63 (c)); gate_EQ2 is untouched and `prereg/eq3/gate_EQ2.txt` still stands for the registered
rule.

## Data (must be absent from data/SEEN.md — confirmed on 2026-09-22: none of these appears as opened)
PMLB mirror on GitHub (LFS object via `media.githubusercontent.com`, pointer oid verified; `data/fetch_pmlb.py
--manifest eq4`), downloaded on or after 2026-09-23 UTC; sha256 of each file in `data/manifests/eq4.sha256`, echoed in
every results header; download date appended to `data/SEEN.md` in the same commit. Availability was checked on
2026-09-22 by fetching each dataset's 131-byte LFS pointer only (HTTP 200 for all six; `usps` 404), which contains no
data rows. Six carriers chosen from PMLB's summary table (`pmlb/all_summary_stats.tsv`, read 2026-09-22) as
classification sets with ≥ 5 classes and ≥ 900 rows not already seen; poker and kddcup excluded for extreme imbalance
(their tail classes vanish under the row cap); shuttle excluded for the same reason (three classes survive the cap);
wine_quality_red excluded (four classes above the floor, 1599 rows).

| carrier (PMLB name) | rows in file | features | classes in file | K requested | expected stream |
|---|---|---|---|---|---|
| `satimage` | 6435 | 36 | 6 | 6 | 3 tasks × 2 classes (row cap applies) |
| `segmentation` | 2310 | 19 | 7 | 6 | 3 × 2 (the six largest classes; ties by label) |
| `yeast` | 1479 | 8 | 10 | 6 | 3 × 2 if six classes clear the floor, else lowered by the rule |
| `wine_quality_white` | 4898 | 11 | 7 | 4 | 2 × 2 |
| `sleep` | 105908 | 13 | 5 | 4 | 2 × 2 (row cap applies) |
| `page_blocks` | 5473 | 10 | 5 | 4 | 2 × 2 (row cap applies) |

Row counts and class counts above are from the summary table, not from the files. **Class-selection rule (new,
named):** classes are ranked by row count (ties by remapped label); the K requested largest are taken; the row cap
(MAX_ROWS = 5000, stratified, seed 777) is applied; if the smallest used class has fewer than CLASS_FLOOR = 40 rows, K
is lowered by two and the selection repeated; a carrier that ends with K < 4 is **excluded and counted**
(`runs/eq4/exclusions.txt`), and rows needing "every carrier" are scored on the carriers present with the denominator
stated. This rule answers the fars defect of EQ3 (AGENT_LOG 60: a class emptied by the cap). NaN rows dropped and
counted. Fixed 80/20 stratified split (seed 12345), standardised on the training part. Quality gate as EQ3: a run whose
parameters are non-finite scores 0 and is counted.

## Instrument (all constants named; frozen in `runs/eq4/frozen/eq4_score.py`)
As EQ3: numpy MLP d-256-K ReLU, SGD lr 0.05, batch 10, 3 epochs per task, seeds 0–4; online-EWC, ER-sum, DER++, LwF,
SI, MAS past terms; rule estimator EMA of gradient vectors, smooth 0.9, Euclidean norm, cap 1e4, floor 1e-12; A-GEM,
GradNorm α = 0, MEGA-I baselines; the Bayes arm (weight 1/2); reduction arms (fixed w at the median derived weight of
the EQ-B Ω = 1 run); two-stage λ tuning (coarse grid 0.1…1e4, √2 refinement around the coarse best, for the clean fixed
weight and for the poisoned fixed+clip weight); step = max(1.0 pt, 2 SE of the tuned arm); nine-point Ω grid on the
EWC arm for both rules; the lr × batch array on the array carrier `satimage` (chosen before any data: the most rows
above the cap with balanced classes). Dropped from EQ3: the capacity × epochs array and the x4 diagnostic regime.
Additions:
- **mode `eqb`** (EQ-B): `g̃_p = g_p · min(1, τ/‖g_p‖)`, `τ = κ · max(kept lengths of the last N batches)`, κ = 2,
  N = 50, N_MIN = 10, history of kept lengths, reset at every task boundary; then the registered ratio on `g̃_p`.
- **mode `fixedclip`**: the fixed weight with the same clip (the R7 baseline of the poisoned regime).
- **regime `poison`**: in the first epoch of every task after the first, from batch
  `min(max(N_MIN, floor(0.25 · n_batches)), n_batches − run)`, `run = max(1, min(5, floor(0.05 · n_batches)))`
  consecutive batches have their present gradient multiplied by 1000 before any clip. Arms in this regime: EWC fixed
  coarse grid, EWC fixed+clip coarse grid with √2 refinement, the registered rule at Ω = 1, EQ-B at Ω = 1.
- **sensitivity of EQ-B at Ω = 1:** cap ∈ {10, 100, 1e4} × smooth ∈ {0.8, 0.9, 0.98} (8 cells beyond the main) and
  κ ∈ {1.5, 2, 4} × N ∈ {20, 50, 200} (8 cells beyond the main): 16 cells per carrier.
- The clip fraction, the maximum derived weight and the number of poisoned batches are recorded per run.

## Rows (scored once by `eq4_score.py score`; per carrier and per seed values printed)
Aggregation: mean over five seeds, per-seed values beside every mean; "every carrier" = the carriers present, denominator
stated (6/6 if none is excluded). One-sided where the rule need only not lose (EQ4-1, EQ4-1r, EQ4-3); the two-sided
quantity is printed everywhere.

| row | prediction | threshold | verdict rule |
|---|---|---|---|
| EQ4-0 | precondition: the tuned λ moves across carriers | span of tuned λ ≥ 10× | else EQ4-1/1r reported without verdict |
| EQ4-1 | EQ-B(Ω = 1) − tuned λ > −step on every carrier, and the best single λ loses ≥ a step on some carrier | step = max(1, 2 SE) | PASS / FAIL |
| EQ4-1r | the registered rule, same criterion (EQ3-1 on fresh carriers) | as above | PASS / FAIL |
| EQ4-2 | \|EQ-B(Ω = 1) − rule(Ω = 1)\| < step on every clean carrier | step | IDLE / NOT IDLE |
| EQ4-3 | poisoned: EQ-B(Ω = 1) − tuned fixed+clip > −step_p on every carrier | step_p = max(1, 2 SE of the tuned fixed+clip arm) | PASS / FAIL |
| EQ4-4 | poisoned: rule(Ω = 1) − EQ-B(Ω = 1) ≤ −step_p on ≥ ⌈n/2⌉ carriers | step_p | LOAD-BEARING / INERT |
| EQ4-5 | control ER-sum: EQ-B on replay within a step of its reduction arm and not ahead of the best fixed w by a step | step | holds / VIOLATED |
| EQ4-6 | reduction: \|EQ-B(Ω = 1) − fixed@median\| < step on every carrier | step | REDUCES / DOES NOT REDUCE |
| EQ4-7 | published baselines (A-GEM, GradNorm, MEGA-I) vs EQ-B | a baseline ahead by ≥ step on every carrier dominates | report |
| EQ4-S | EQ4-1 flips over the 16 sensitivity cells per carrier | > 1 flip | FRAGILE / not fragile |
| EQ4-P | plateau width of EQ-B over the nine-point Ω grid | within a step of the best | report |
| EQ4-B | the Bayes arm vs tuned λ and vs EQ-B | step | report |
| EQ4-D | DER++, LwF (load-bearing cells marked), SI, MAS with EQ-B | — | report only (outside the narrowed H-EQ) |
| EQ4-I | lr × batch on `satimage`: EQ-B not behind the tuned λ per cell | ≥ 4/5 cells | PASS / FAIL |

What the outcomes mean: EQ4-1 PASS and EQ4-2 IDLE and EQ4-1r PASS → the bounded rule carries EQ3's claim on fresh
carriers at no cost; EQ4-1 PASS with EQ4-1r FAIL → the bound is doing work on a clean carrier and EQ4-2 must show where;
EQ4-3 PASS and EQ4-4 LOAD-BEARING → the enhancement is a result at the PASS-0 level (anchoring); EQ4-4 INERT → the
poison does not separate the rules on real carriers and the enhancement is a surrogate-only property; EQ4-3 FAIL →
the fixed weight with the same clip is enough, and the rule adds nothing under poison; EQ4-5 VIOLATED → the reduction
premise fails and the mechanism statement is falsified as in EQ3-3.

## Seeds and determinism (R9)
Run seeds 0–4; split seed 12345; subsample seed 777. Two runs of one unit must be byte-identical (`cmp`; checked on one
arm per carrier in `runs/eq4/rerun_*.json`); `smoke.txt` and `smokefull.txt` are byte-identical on rerun and produced
by the frozen copy; the `uv.lock` sha256 is printed in every results header.

## Baselines (R7)
Tuned fixed λ (two-stage, in-sample on the scored seeds); the fixed weight with the same clip under poison (tuned the same
way); the reduction arms; ER-sum with a fixed-w grid; DER++, LwF, SI, MAS, A-GEM, GradNorm, MEGA-I (hand-rolled in
numpy as in EQ2/EQ3; named as context, not fetched); the Bayes arm; the registered rule itself.

## Sensitivity table (required in the report)
cap × smooth and κ × N for EQ4-1 (16 cells per carrier); the lr × batch array on `satimage`. Fragile iff EQ4-1 flips
in more than one cell.

## Scoring script
`runs/eq4/frozen/eq4_score.py` (copy of `studies/eq4/eq4_score.py` at hash time), with `runs/eq4/frozen/exclusions.py`,
`core.py`, `battery.py`, `gate.py` and `CRR.md`; sha256 in `HASH.txt`. Command sequence on the data day:
```
uv run python data/fetch_pmlb.py --manifest eq4 satimage segmentation yeast wine_quality_white sleep page_blocks
for c in satimage segmentation yeast wine_quality_white sleep page_blocks; do uv run python runs/eq4/frozen/eq4_score.py all $c > runs/eq4/log_$c.txt 2>&1; done
uv run python runs/eq4/frozen/eq4_score.py score runs/eq4/results_*.jsonl > runs/eq4/score.txt
uv run python runs/eq4/frozen/exclusions.py > runs/eq4/exclusions.txt
```
