# Pre-registration — EQ3: the normalised penalty step on six unseen PMLB streams, with the Bayes arm, the nine-point Ω grid and the lr × batch array

Written: 2026-09-22T01:20:36Z (container clock; the commit carries the exact time; the push timestamp is the
external witness). Hash of this folder and the frozen scripts in `HASH.txt`. Owner request: prompt-log
entry 69 ("comprehensive sweeps on the omega=1 equanimity rule on existing mathematics, then robust full
sweeps on continual learning systems ... full comprehensive tests on continual learning benchmarks / SOTA
methods"). Under the PASS levels of CLAUDE.md §7.
**No data listed below has been opened. No file named below exists under `data/raw/` at hash time.**

## What this study is
The third data study of H-EQ in its EQ2 form (the rule at Ω = 1 as a tuning-free normalised penalty step
for online EWC), and the first replication attempt since EQ2R was voided (ledger EQ2R-VOID, AGENT_LOG 40).
It runs the EQ2 design unchanged on six PMLB streams never opened in any CRR work, with the EQ2R arrays
(cap axis, empty-present diagnostic, capacity × epochs) and three additions, each named here: a Bayes arm,
the nine-point Ω grid on the EWC arm, and a learning-rate × batch invariance array. The scorer is a copy
of the frozen EQ2R scorer with the EQ2R defect fixed (the record field `hid` was rebound to an activation
array; here the width is `hidden` and the activations `act`, and every record is serialised inside
`run()`), and with the additions below. Every branch was exercised before the hash: `smoke.txt` (every
method × mode once, every array cell) and `smokefull.txt` (the whole `all` pipeline and the scorer on a
synthetic carrier), both committed here, both byte-identical on rerun, both covered by the hash.

## What the mathematics said first (theory/checks/omega_sweeps.py, PR #53, same day, no data)
With exact gradients the rule's fixed points at Ω = 1 are the whole Pareto curve of the two tasks (a
continuum of equilibria), the edge is a knife edge at Ω = 1, a fixed weight has a stability edge
lr·(h_max + λ·f_max) = 2, and smoothing plus mini-batch noise turn the knife edge into a plateau. The Bayes
weight for combining a present and a past batch is a constant fixed by the sample counts, not a norm ratio;
for a Laplace penalty on the per-sample Fisher with equal task sizes it is 1/2. None of this was learned on
a dataset (R3); it motivates the Bayes arm and the plateau row below.

## R3 statement
Two rules used here were learned on EQ2's carriers on 2026-09-17 (mfeat_fourier, mfeat_pixel, texture):
the cap-axis prediction (EQ2-S; EQ2R-C) and the narrowing of the constraint control to load-bearing
weights (reports/eq2.md §3). They are used here on different carriers five calendar days later, under this
fresh prereg, which names both. Nothing was learned on the six carriers below.

## Anchoring — read this first
OpenTimestamps calendars are unreachable from this environment and tag pushes are refused by the remote
(both attempts recorded in `runs/eq3/ots_attempt.txt` and `runs/eq3/tag_push_attempt.txt`). The only
external witness to "before" is the GitHub push timestamp of the commit carrying `HASH.txt`. Under R2 this
study is **weakly anchored**; every ledger row it produces carries `anchor: push-timestamp only`. By the
accepted levels no row of this study can be PASS-1 or PASS-2 on anchoring alone; the strongest label
available is PASS-0 with the replication noted against EQ2-1b, until Daniel stamps `HASH.txt` under the
two-person protocol (`docs/ROADMAP_2026-Q4.md` §1.2) or re-runs the frozen scripts on his machine.

## Hypothesis under test
The rule `g = g_present + w · g_past`, `w = Ω · ‖ĝ_present‖ / ‖ĝ_past‖`, Ω = 1, is useful exactly when the
past term is the past task's Fisher-curvature penalty (online EWC): on every carrier it is not behind the
tuned λ by a resolvable step, while no single λ transfers across carriers (EQ3-1). It is redundant when the
units already match (ER-sum, EQ3-3). It is harmful when the past term is a constraint that is not a loss on
the past task, **on carriers where that constraint's weight is load-bearing** (DER++, LwF; EQ3-4, narrowed
from EQ2 as reports/eq2.md §3 required). The mechanism reading from EQ2 is that the rule's value comes from
bounding the penalty step by the present step, which keeps it above a fixed weight's stability edge; that
reading predicts EQ3-C (the cap axis) and is tested by it.

## Gate (R4) — `gate_EQ2.txt` and `gate_EQ.txt`, committed here and covered by the hash
Re-run on the current instrument on 2026-09-22: GATE OPEN for both. EQ2 statistic: S-Y (softmax MLP, online
EWC, 16× Fisher-scale mismatch) PASS with the rule ahead of the tuned weight by 7.5 %; S-R, S-X and S-Y/LwF
FAIL (negative controls); the cap-100 and smooth-0.98 rows FAIL and the smooth-0.8 row passes, which is the
fragility EQ3-S measures. `gate_EQ2.txt` is byte-identical to `prereg/eq2r/gate_EQ2.txt`. The EQ2 report
asked for a gate row for a constraint whose weight is nearly inert; no such surrogate exists yet, and the
load-bearing test of EQ3-4 is the study-side answer (an inert cell is counted and excluded, never scored).

## Data (must be absent from data/SEEN.md — confirmed: none of these appears)
PMLB mirror on GitHub (LFS object via `media.githubusercontent.com`, pointer oid verified;
`data/fetch_pmlb.py --manifest eq3`), downloaded after the push; sha256 of each file in
`data/manifests/eq3.sha256`, echoed in every results file header; download date appended to `data/SEEN.md`
in the same commit. Six carriers, chosen from PMLB's summary table as classification sets with ≥ 8 classes
and ≥ 900 rows not already seen (the seen ones: optdigits, pendigits, letter, mfeat_fourier, mfeat_pixel,
texture, mfeat_karhunen, mfeat_zernike, vowel; mnist is a seen family; poker and kddcup excluded for size
and imbalance; yeast excluded for classes below the row floor).

| carrier (PMLB name) | rows | features | classes in file | classes used | class-IL stream |
|---|---|---|---|---|---|
| `mfeat_factors` | 2000 | 216 | 10 | 10 | 5 tasks × 2 classes |
| `mfeat_morphological` | 2000 | 6 | 10 | 10 | 5 × 2 |
| `led7` | 3200 | 7 | 10 | 10 | 5 × 2 |
| `led24` | 3200 | 24 | 10 | 10 | 5 × 2 |
| `krkopt` | 28056 | 6 | 18 | first 10 in remapped label order | 5 × 2 |
| `fars` | 100968 | 29 | 8 | 8 | 4 tasks × 2 classes |

**Row cap (new, named):** a carrier with more than MAX_ROWS = 5000 rows after class selection is
stratified-subsampled once to 5000 rows with seed 777, before the fixed 80/20 split (seed 12345); the
number of rows before and after is echoed in the header. Rows with NaN dropped and counted. Classes beyond
the used count dropped by the pre-registered rule and counted. No fallbacks: a carrier that cannot be
fetched or fails the oid check is reported as missing, and rows needing "every carrier" are scored on the
carriers present with the denominator stated. Quality gate as EQ2: a run whose parameters are non-finite
scores 0 and is counted in `runs/eq3/exclusions.txt`.

## Instrument (all constants named; frozen in `runs/eq3/frozen/eq3_score.py`)
As EQ2/EQ2R: numpy MLP d-256-K ReLU, SGD lr 0.05, batch 10, 3 epochs per task, seeds 0–4; online-EWC,
ER-sum, DER++, LwF, SI, MAS past terms; rule estimator EMA of gradient vectors, smooth 0.9, Euclidean norm,
cap 1e4, floor 1e-12; A-GEM, GradNorm α = 0, MEGA-I baselines; reduction arms; two-stage λ tuning (coarse
grid 0.1…1e4, √2 refinement around the coarse best); step = max(1.0 pt, 2 SE of the tuned λ); sensitivity
cap ∈ {10, 100, 1e4} × smooth ∈ {0.8, 0.9, 0.98}; x4 diagnostic regime; late-w record (LATE_FRAC 0.2);
capacity × epochs array on the array carrier. Additions:
- **Ω grid on the EWC arm:** the nine points {0.25, 0.35, 0.5, 0.71, 1, 1.41, 2, 2.83, 4} (CLAUDE.md §6);
  DER++ and LwF keep EQ2's five.
- **Bayes arm** (mode `bayes`, EWC only): past term Σ_k (N_k/N_present)·F_k·(θ − θ*) with F_k the scorer's
  per-task Fisher estimate and N_k the task's training rows, weight 1/2, no tuning. This is the Laplace
  posterior's weight in the scorer's units (omega_sweeps.py part 1; equal task sizes make it λ = 1/2 on the
  accumulated Fisher). Report only (EQ3-B).
- **lr × batch invariance array** (EQ3-I) on the array carrier `mfeat_factors`: cells (lr, batch) ∈
  {(0.0125, 10), (0.2, 10), (0.05, 5), (0.05, 20)}; the main cell (0.05, 10) completes the five. EWC coarse
  grid and the rule at Ω = 1 per cell; tuned λ, step and the rule computed per cell.
- **Array carrier:** `mfeat_factors` (216 features, the widest; chosen before any data).

## Rows (scored once by `eq3_score.py score`; per carrier and per seed values printed)
Aggregation: mean over five seeds, per-seed values beside every mean; "every carrier" = 6/6 (or the
carriers present, denominator stated). Strict/non-strict and sidedness as written (EQ3-1 one-sided by
design: the rule need only not lose; the two-sided quantity is printed).

- **EQ3-0 Precondition.** Tuned λ spans ≥ 10× across carriers; else EQ3-1 and EQ3-2 are reported without
  a verdict.
- **EQ3-1 H-EQ2.** On every carrier mean(rule Ω = 1) − mean(tuned λ) > −step, AND the best single λ (coarse
  grid, best mean over carriers) is behind the tuned λ by ≥ step on at least one carrier. PASS needs both.
- **EQ3-2 Reduction.** |rule − fixed at median derived w| < step on every carrier → "reduces"; else "does not
  reduce". Report.
- **EQ3-3 Control, same units (ER-sum).** Holds iff on every carrier rule − best fixed w < step AND
  |rule − reduction arm| < step.
- **EQ3-4 Control, constraint (DER++, LwF), narrowed.** A cell (carrier, method) is load-bearing iff the
  finite cells of its fixed-weight grid span ≥ 2 steps in mean accuracy; otherwise it is inert, counted and
  excluded from the denominator. Holds iff in every load-bearing cell the rule at its best Ω is behind the
  tuned weight by ≥ step. Not decidable if no cell is load-bearing.
- **EQ3-5 Diagnostic (SI, MAS).** Ω = 1 − tuned, report only.
- **EQ3-6 Ω plateau.** Best Ω on the EWC nine-point grid lies in {0.71, 1, 1.41} on every carrier; ties to
  the smallest Ω (works against a PASS). FAIL otherwise. Never "Ω = 1 exactly".
- **EQ3-7 Published baselines.** A-GEM, GradNorm (α = 0), MEGA-I vs the rule at Ω = 1; a baseline ahead by
  ≥ step on every carrier "dominates the rule". Report.
- **EQ3-S Sensitivity.** EQ3-1's "not behind" flips in > 1 of the 9 × n cells → fragile.
- **EQ3-8 Diagnostic regime.** Standardised features × 4, report only.
- **EQ3-C Cap axis (mechanism).** Per carrier and cap ∈ {10, 100, 1e4} at smooth 0.9: the rule at Ω = 1 is
  not behind the tuned λ by a step iff cap ≥ tuned λ. PASS iff the pattern holds in all 3n cells.
- **EQ3-D Empty-present diagnostic.** Late-w median against the whole-run median, per carrier; report.
- **EQ3-A Capacity × epochs** on `mfeat_factors`: not behind in ≥ 3 of 4 cells → PASS.
- **EQ3-I lr × batch invariance** on `mfeat_factors` (new): the rule at Ω = 1 not behind the tuned λ by
  that cell's step in ≥ 4 of 5 cells → PASS; FAIL otherwise. All five cells printed with their tuned λ.
- **EQ3-B Bayes arm** (new, report only): Bayes − tuned and rule − Bayes per carrier; the count of carriers
  where the Bayes weight is not behind the tuned λ by a step. No threshold.
- **EQ3-P Plateau width** (new, report only): per carrier, the number of the nine Ω whose mean is within a
  step of the best, and whether they are contiguous; the median width. No threshold.
- **Replication summary (not a row).** EQ3-1, fragility, controls, cap axis. The ledger row applies the
  accepted levels: PASS-0 if EQ3-1 passes; the replication is noted against EQ2-1b; PASS-1 and PASS-2 are
  unavailable here on anchoring (above).
- **Any violated control → the mechanism statement is falsified; the report says so in its first line.**

Outcomes named in advance: EQ3-1 PASS with EQ3-C PASS and controls holding → the EQ2 reading (a tuning-free
normalised penalty step whose value is the stability edge) replicates on six new carriers, at PASS-0 for
anchoring; EQ3-1 PASS with EQ3-C FAIL → the pass is real and its mechanism statement is wrong; EQ3-1 FAIL →
EQ2-1 does not replicate and stays PASS-0 with a failed replication recorded beside it; EQ3-4 violated in a
load-bearing cell → the harm clause is retired for good; EQ3-6 FAIL with EQ3-P wide → Ω is a plateau, as the
mathematics predicts, and no value of Ω is claimed; EQ3-B with the Bayes weight not behind on most carriers
→ the tuned λ is the Bayes weight and the rule's advantage is over a mis-set constant, not over Bayes; EQ3-I
FAIL → the effect is learning-rate- or batch-specific and the roadmap says so.

## Seeds and determinism (R9)
Run seeds 0–4 (network init, batch order, replay draws); split seed 12345; subsample seed 777; Fisher
estimation uses the run's generator. Two runs of one unit must be byte-identical (`cmp`; checked on one
arm per carrier in `runs/eq3/rerun_*.json`); `smoke.txt` and `smokefull.txt` are byte-identical on rerun;
the `uv.lock` sha256 is printed in every results header.

## Baselines (R7)
Tuned fixed λ (two-stage grid, tuned in-sample on the scored seeds, which favours the baseline); the
reduction arm; ER-sum with a fixed-w grid; DER++ (Buzzega et al. 2020), LwF (Li and Hoiem 2017), SI (Zenke
et al. 2017), MAS (Aljundi et al. 2018), A-GEM (Chaudhry et al. 2019), GradNorm (Chen et al. 2018), MEGA-I
(Guo et al. 2020), all hand-rolled in numpy as in EQ2 (named as context, not fetched; CLAUDE.md §6 asks for
Mammoth reference implementations on image streams, which this environment cannot run: no GPU, no PyTorch,
image datasets unreachable; that remains Daniel's anchored run); the Bayes arm.

## Sensitivity table (required in the report)
cap × smooth (9 cells per carrier) for EQ3-1; the cap axis (EQ3-C); the capacity × epochs and lr × batch
arrays on the array carrier. Fragile iff EQ3-1 flips in more than one cell.

## Scoring script
`runs/eq3/frozen/eq3_score.py` (copy of `studies/eq3/eq3_score.py` at hash time), with
`runs/eq3/frozen/core.py`, `battery.py`, `gate.py` and `CRR.md`; sha256 in `HASH.txt`.
