# Pre-registration — SEC1: the Laplace (Bayes) weight on a secant-calibrated Fisher, on the twelve SEEN carriers of EQ3 and EQ4

- **Study id:** `sec1`.
- **Written:** 2026-09-23 (prompt-log entry 120, after entries 111–119).
- **Timing:** hashed and pushed before any of the carriers below is opened for this study.
- **Author:** the agent, under CLAUDE.md §1.
- **Anchoring:** push timestamp only (see below).

## What this study is, and what it cannot be

**The owner's decision** (prompt-log entry 120): "today we will run the pre registered checks on existing actual data."
Every carrier here was opened before, in EQ3 (2026-09-22) or EQ4 (2026-09-23), and is listed in `data/SEEN.md`.

**What the study therefore is:**
- **A confirmatory study on seen data (R11).** It is not held-out, and no row may be described as held-out.
- **On the epistemic ladder** (`Epistemic_Review/`) its rungs are:
  - R5, pre-registered on seen data;
  - never PASS-0 or above, because PASS-0 requires R2–R9 on data held out under R11.

**What a PASS here would license:** the unseen-data test named in the scratchpad reading (prompt-log entry 118), under
a fresh pre-registration on a later calendar day. Nothing more.

## The question

The continual-learning paper (`Continuous_Learning/CONTINUOUS_LEARNING.md` §7.4) found the Laplace weight (EQ3's Bayes arm,
w = 1/2 on the task-size-weighted empirical Fisher):
- equal to the in-sample-tuned λ where the tuned λ was small;
- 7.6 to 12.5 points behind where the tuned λ was in the hundreds.

The paper read the rule's advantage there as "an advantage over a mis-calibrated Laplace approximation with a diagonal
empirical Fisher". The scratchpad work of 2026-09-23 split the tuned λ's job into three:
1. fixing the Fisher's units;
2. keeping the task count;
3. staying below the stability edge.

It then proposed a direct correction of (1) that leaves (2) intact.

**The correction (SEC).** At the end of each task j, rescale the empirical Fisher f_j by s_j = c_j / ρ_j:
- c_j is the curvature the present loss showed along the path the learner actually travelled during task j. It is a
  secant: the change of the mean clean present gradient between the task's first and last 10 % of steps, projected on
  the change of the mean parameters, divided by the squared length of that change.
- ρ_j is the curvature the Fisher claims along the same path.

The scorer's docstring gives the formulae and the fallback: s_j = 1, counted and never excluded, when the path is too
short or either curvature is not positive.

**The claim under test.** With the units fixed this way, the textbook Laplace weight (w = 1/2) needs no per-dataset
tuning.

## R3 statement

**What was defined, and when.** The calibration, its windows (FS = FE = 0.1), its fallback and the one-factor
alternative were defined on 2026-09-23:
- in scratchpad work on synthetic quadratic worlds (prompt-log entries 111–118; not in the repository);
- in this study's gate, on a synthetic ten-class stream.

The motivation came from the rows EQ3-B and EQ4-0 on these carriers.

**The R3 consequence.** R3 forbids using a rule defined after seeing a dataset on *another* dataset the same day. This
study uses the rule only on the datasets whose rows motivated it, which is exactly why it is confirmatory-on-seen and
nothing more. **The unseen-data test may not be run before 2026-09-24 00:00 UTC.**

## Anchoring — read this first

As EQ3 and EQ4: OpenTimestamps calendars and tag pushes have been unreachable from this environment. The attempts are
recorded in `runs/sec1/ots_attempt.txt` and `runs/sec1/tag_attempt.txt`. The only external witness to "before" is the
GitHub push timestamp of the commit carrying `HASH.txt`. Every ledger row carries `anchor: push-timestamp only`.

## Carriers (all SEEN; the raw files are those of the EQ3 and EQ4 manifests)

| group | carriers | file hashes | K requested |
|---|---|---|---|
| EQ3's six | mfeat_factors, mfeat_morphological, led7, led24, krkopt, fars | `data/manifests/eq3.sha256` | 10, 10, 10, 10, 10, 8 (as EQ3) |
| EQ4's six | satimage, segmentation, yeast, wine_quality_white, sleep, page_blocks | `data/manifests/eq4.sha256` | 6, 6, 6, 4, 4, 4 (as EQ4) |

- Every carrier goes through **EQ4's class-selection rule**: the largest K classes, a class floor of 40, and a 5000-row
  stratified cap (seed 777). This changes EQ3's led7, led24, krkopt and fars class sets from EQ3's first-K-by-label rule.
- Two classes per task.
- A carrier with K < 4 after the rule is excluded and counted.
- Before any run, the data step verifies each raw file's sha256 against its manifest. A mismatch stops the study.

## Design

**Unchanged from EQ4.** Network, optimiser, data handling and Fisher estimator: a numpy MLP with 256 hidden units,
SGD at lr 0.05, batch 10, 3 epochs per task, class-incremental accuracy (%) on a fixed 20 % stratified test split, 50
mini-batches for the Fisher, seeds 0–4.

**Arms (online EWC):**
- `fixed`, λ tuned on the raw Fisher, two-stage:
  - coarse grid 0.1 … 1e4 (11 points);
  - √2 refinement around the coarse best;
  - in-sample on the scored seeds, as in EQ3 and EQ4, which favours the baseline.
- `fixed_sec`, λ tuned the same way on the calibrated Fisher, coarse grid 0.01 … 1e4 (13 points).
- `bayes`, the Laplace weight 1/2 on the raw Fisher.
- `bayes_sec`, the Laplace weight 1/2 on the calibrated Fisher (**the arm under test**).
- `bayes_s1`, the Laplace weight 1/2 with one factor for every task (task 1's s). This is the R7 strongest simple
  alternative: "fix the units once".
- `eq`, the registered rule at Ω = 1. This is the R7 comparison: it is the paper's method.

**Sensitivity.** `bayes_sec` at start × end window fractions {0.05, 0.1, 0.2}²: 8 cells besides the main one.

**The resolvable step** per carrier: max(1, 2 × SE over seeds of the tuned raw-λ arm), as in EQ4.

## Hypotheses (verdicts computed by `score`; one-sided "not behind", as in EQ3 and EQ4, because the claim is that a tuning-free weight is at least as good as the tuned one)

| id | what is tested | criterion |
|---|---|---|
| **SEC1-0** (precondition) | the miscalibrated set M: carriers where `bayes` − tuned ≤ −step | DECIDABLE if \|M\| ≥ 3; otherwise SEC1-1 is NOT DECIDABLE |
| **SEC1-1** (the paper's reading) | on M, the calibrated Laplace closes at least half of the raw gap: `bayes_sec` − `bayes` ≥ 0.5 × (tuned − `bayes`) | PASS if on at least ⌈2/3 × \|M\|⌉ carriers of M; else FAIL |
| **SEC1-2** (no harm) | on the other carriers, `bayes_sec` − `bayes` > −step | PASS if on every such carrier |
| **SEC1-3** (tuning-free) | `bayes_sec` − tuned > −step | PASS if on at least 9 of the 12 carriers. Raw Bayes's and the rule's counts are printed beside it |
| **SEC1-4** (the λ spread collapses) | the across-carrier span (max/min) of the calibrated tuned λ against the raw tuned λ | PASS if calibrated span ≤ raw span / 10 |

**Reported without verdict:**
- **SEC1-G:** `bayes_sec` − `bayes_s1` per carrier. Does per-task calibration beat one global factor?
- **SEC1-R:** the rule against tuned, and `bayes_sec` against the rule.
- **SEC1-S:** SEC1-3 flips over the 8 window cells × 12 carriers. More than one flip is FRAGILE.
- **SEC1-E:** the calibration factors s_j (median, range) and fallback counts, per carrier.

**Instrument check SEC1-X** (pre-registered; run in the data step before scoring). On the six EQ4 carriers, SEC1's
`fixed` (coarse grid), `bayes` and `eq` arms must reproduce `runs/eq4/results_*.jsonl` exactly, per seed. They are the same
code path and the same random draws. A mismatch is reported and stops scoring until it is explained in AGENT_LOG.

**Reproducibility (R9).** One carrier, `led7`, is run twice with `all`, and the two JSONL files must be byte-identical
(`cmp`).

**Exclusions and non-finite runs.** A run that ends non-finite scores 0 and is kept (as EQ3 and EQ4). Calibration
fallbacks are counted per carrier and mode (`exclusions.py`). A carrier excluded by the class-selection rule is counted
and not scored.

## Gate (R4) — committed here and covered by the hash

`gate_SEC_v1_closed.txt`, **the first gate: CLOSED.**
- Its units-distortion rows were not load-bearing on the synthetic stream: the raw Laplace arm is about 500× under-scaled
  there, so a 16× distortion barely moves it.
- The calibrated arm's invariance to a units change is an algebraic identity, not evidence.

Redesigned before any carrier was opened (AGENT_LOG 96).

`gate_SEC.txt`, **the gate this study stands on: OPEN.**

| row | role | result |
|---|---|---|
| POS | MUST_PASS | the calibrated Laplace closes 15.9197 of the raw 16.9231 gap on the synthetic ten-class stream (tuned λ 100: 42.1405; raw Laplace 25.2174; calibrated 41.1371) |
| INV | MUST_PASS, implementation check | unchanged under per-task and global units distortions: max change 0.00e+00 |
| SHAPE | MUST_FAIL | under a shape-only distortion the calibrated arm moves by −41.1371 (it diverges): it corrects scale, not shape, as required |

On the synthetic stream the one-factor alternative scored 33.8462 and the rule 42.2742.

**What a surrogate would do.** On a stream with a shape error rather than a units error, the calibration cannot help.
SHAPE shows it can hurt badly: the stiffened penalty crosses the stability edge. SEC1 inherits no step bound.

## Commands (in order)

```
uv run python runs/sec1/frozen/sec1_score.py smoke        | cmp - prereg/sec1/smoke.txt
uv run python runs/sec1/frozen/sec1_score.py gate         | cmp - prereg/sec1/gate_SEC.txt
# after the push of this commit: verify raw sha256 against the manifests, then
uv run python runs/sec1/frozen/sec1_score.py all <carrier> --out runs/sec1/results_<carrier>.jsonl   (x12)
uv run python runs/sec1/frozen/sec1_score.py all led7 --out runs/sec1/rerun_led7.jsonl && cmp runs/sec1/results_led7.jsonl runs/sec1/rerun_led7.jsonl
uv run python runs/sec1/frozen/repro_eq4.py > runs/sec1/repro_eq4.txt                           # SEC1-X
uv run python runs/sec1/frozen/sec1_score.py score runs/sec1/results_*.jsonl > runs/sec1/score.txt
uv run python runs/sec1/frozen/exclusions.py > runs/sec1/exclusions.txt
```
