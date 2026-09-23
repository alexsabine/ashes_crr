# Study SEC1: the Laplace weight on a secant-calibrated Fisher (twelve SEEN carriers)

- **Written:** 2026-09-23, after the ledger rows SEC1-0 … SEC1-X existed. Every number here is in those rows or in
  `runs/sec1/score.txt`, `runs/sec1/exclusions.txt`, `runs/sec1/repro_eq4.txt`, `runs/sec1/rerun_check.txt`.
- **Pre-registration:** `prereg/sec1/PREREG.md`.
  - HASH.txt sha256 775eb1a8… (prefix, as for the earlier studies).
  - Prereg commit 0f67f2d, pushed 2026-09-23T15:18:10Z. Anchor: push timestamp only.
  - OTS and the tag push were refused: `runs/sec1/ots_attempt.txt`, `runs/sec1/tag_push_attempt.txt`.

> **Read this first.** Every carrier in this study had been opened before, in EQ3 or EQ4. The study is confirmatory on
> seen data (R11), rung R5 of the epistemic ladder. None of its passes is PASS-0, and none may be quoted as a result.
> What it licenses is a fresh pre-registration on unseen carriers on a later calendar day (R3: not before 2026-09-24).

## 1. The question

The Laplace (Bayes) weight is w = 1/2 on the task-size-weighted empirical Fisher. In EQ3 it matched the tuned λ only
where the tuned λ was small. The continual-learning paper read this as a mis-calibrated Fisher (§7.4).

**The arm under test.** SEC rescales each task's Fisher, once, at the task's end. The factor is s_j = c_j / ρ_j:
- c_j is the curvature the present loss showed along the path travelled (a secant);
- ρ_j is the curvature the Fisher claims along the same path.

**The question.** Does the textbook Laplace weight then need no per-dataset tuning?

## 2. Instrument checks (before scoring)

- **Data.** All 12 raw files match the EQ3 and EQ4 manifests (`runs/sec1/data_check.txt`).
- **SEC1-X.** SEC1's `fixed`, `bayes` and `eq` arms reproduce EQ4's results exactly: 390 runs, 0 mismatches.
- **R9.** The rerun of led7 is byte-identical.

## 3. Results (ledger rows)

| row | verdict | the numbers |
|---|---|---|
| SEC1-0 | DECIDABLE | raw Laplace trails the tuned λ by a step on 6 of 12 carriers |
| SEC1-1 | **PASS (seen data), exactly at the threshold** | the calibrated Laplace closes at least half of the raw gap on 4 of the 6 (needs 4): mfeat_factors (+7.45 of 12.50), mfeat_morphological (+10.30 of 7.60), led7 (+4.09 of 4.03), segmentation (+3.79 of 4.39). Not on fars (+0.12 of 3.52); on yeast it is worse (−3.64) |
| SEC1-2 | **PASS (seen data)** | where raw Laplace was already close, calibration did no harm: 6/6 |
| SEC1-3 | **PASS (seen data), at the boundary, FRAGILE** | not behind the tuned λ on 9 of 12 (needs 9); raw Laplace 6/12, the registered rule Ω = 1 8/12. wine_quality_white counts as not behind by 0.029497893800771 points |
| SEC1-4 | **FAIL** | the calibrated tuned λ does not collapse across carriers: span 849.00× against 423.00× raw. 8 of 12 calibrated optima lie in 0.423–1.41, around the Laplace value; fars (0.01, the grid's lower edge), satimage (0.1), wine_quality_white (2.13) and page_blocks (8.49) do not |
| SEC1-S | **FRAGILE** | 8 of 96 window cells flip SEC1-3 |
| SEC1-G | report | per-task calibration beats one global factor (task 1's) by a step on 5/12 and is never behind by a step; the one-factor arm diverges on every seed of mfeat_factors and mfeat_morphological |
| SEC1-R | report | against the paper's rule: calibrated Laplace ahead by a step only on led7 (+1.2812, step 1.00) and behind by a step only on mfeat_factors (−8.9500, step 4.54) |
| SEC1-E | report | median calibration factors range from 0.869 (wine_quality_white) to 4.43e+03 (mfeat_factors). On mfeat_factors 18 of 45 calibrated runs are non-finite |

## 4. The sensitivity table (calibrated Laplace − tuned λ, by start/end window fraction; the main cell is 0.1/0.1)

| carrier | 0.05/0.05 | 0.05/0.1 | 0.05/0.2 | 0.1/0.05 | **0.1/0.1** | 0.1/0.2 | 0.2/0.05 | 0.2/0.1 | 0.2/0.2 |
|---|---|---|---|---|---|---|---|---|---|
| mfeat_factors | −54.45 | −54.45 | −54.45 | −4.95 | −5.05 | −5.10 | +6.15 | +6.30 | +6.40 |
| mfeat_morphological | +3.25 | +3.30 | +3.40 | +2.70 | +2.70 | +2.90 | +1.95 | +2.10 | +2.30 |
| led7 | −0.03 | −0.03 | −0.03 | +0.06 | +0.06 | +0.12 | +1.03 | −0.12 | +0.00 |
| led24 | +3.10 | +3.10 | +3.10 | +3.04 | +3.07 | +3.00 | +3.13 | +3.13 | +3.19 |
| krkopt | −0.74 | −0.72 | −0.74 | −0.50 | −0.54 | −0.56 | −0.28 | −0.28 | −0.30 |
| fars | −3.48 | −3.48 | −3.48 | −3.32 | −3.40 | −3.32 | −3.18 | −3.18 | −3.20 |
| satimage | +5.53 | +5.51 | +5.49 | +5.65 | +5.57 | +5.55 | +5.63 | +5.49 | +5.43 |
| segmentation | −0.56 | −0.51 | −0.56 | −0.61 | −0.61 | −0.61 | −0.76 | −0.76 | −0.71 |
| yeast | −9.43 | −11.64 | −8.71 | −13.43 | −11.43 | −12.07 | −4.50 | −3.86 | −4.14 |
| wine_quality_white | −6.69 | −6.69 | −6.69 | −6.71 | −6.71 | −6.71 | −6.71 | −6.71 | −6.71 |
| sleep | −0.30 | −0.34 | −0.34 | −0.26 | −0.28 | −0.30 | −0.26 | −0.28 | −0.30 |
| page_blocks | −17.24 | −16.48 | −7.13 | −4.28 | +0.54 | −2.86 | +6.73 | +6.49 | +6.53 |

The steps are those of SEC1-3. The 8 flips come from three carriers:
- mfeat_factors: 3 flips. The 0.2 start windows pass where the main cell is behind; the 0.05 windows diverge.
- yeast: 3 flips. The 0.2 start windows are within its step (6.04).
- page_blocks: 2 flips. The 0.05/0.05 and 0.05/0.1 cells are behind by more than its step (10.90).

Any window preference read from this table is an observation after the fact. It is not a rule for the next study
unless a fresh pre-registration names it (R3).

## 5. Exclusions

- **Carriers:** none excluded by the class-selection rule.
- **Non-finite runs:** 707 of 2880, kept and scored 0 as pre-registered. By arm:

  | arm | non-finite |
  |---|---|
  | tuned-λ grids, raw | 270 of 1020 |
  | tuned-λ grids, calibrated | 406 of 1140 |
  | one-factor Laplace | 13 of 60 |
  | calibrated Laplace | 18 of 540, all on mfeat_factors |
  | raw Laplace | 0 of 60 |
  | rule | 0 of 60 |
- **Calibration fallbacks** (s = 1): 2081 of 10320 task ends over all arms. For the arm under test: 60 on mfeat_factors,
  11 on page_blocks, 12 on yeast, 0 elsewhere (`runs/sec1/exclusions.txt`).

## 6. Reading

**Where it worked.** On the seen carriers, calibrating the Fisher by the path travelled moved the textbook Laplace weight
from not behind on 6 of 12 carriers to not behind on 9 of 12. It closed at least half of the raw gap on mfeat_factors,
mfeat_morphological, led7 and segmentation.

**What it did not deliver:**
- It did not collapse the tuned λ's spread (SEC1-4 FAIL).
- It hurt on yeast.
- It did nothing on fars.
- It is fragile to its window.

**Where it failed, the mechanism is visible.** On mfeat_factors the calibration factor reaches about 4400, and with no
step bound the penalty crosses the stability edge. That is the risk the gate's SHAPE row and the prereg named: the
calibration does not inherit the rule's step bound.

**Against the paper's rule,** the calibrated Laplace is about level: 9 against 8 carriers not behind the tuned λ. It is
ahead of the rule by a step on one carrier and behind by a step on one.

**What a real test needs.** A fresh study on unseen carriers, on a later day. It would pre-register a step safeguard and
the window choice before seeing them.

## 7. What a surrogate would have done

See `prereg/sec1/gate_SEC.txt`:
- On a stream whose Fisher error is one of *shape*, not scale, the calibration cannot help, and it diverged (SHAPE row:
  −41.1371).
- Its invariance to a units change is exact by construction (INV row). The first gate showed that this, on its own, is no
  evidence (`gate_SEC_v1_closed.txt`).
- The positive control (POS) shows that on a synthetic stream the calibration closes most of a real gap (15.9197 of
  16.9231).

On these carriers a pass is consistent with a Fisher error that was largely one of scale. The two failures (yeast, fars)
are not explained by this study: yeast had 12 calibration fallbacks, fars none.
