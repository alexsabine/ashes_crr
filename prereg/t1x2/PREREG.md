# Pre-registration — T1x2: path length against endpoint displacement as a predictor of forgetting, learning rate controlled (replacement of the void study T1x)

Study id: `t1x2`. Written, hashed and pushed 2026-09-22 (prompt-log entry 87; AGENT_LOG 69–70). Author: the agent, under
CLAUDE.md §1. Anchoring: push timestamp only. **Data step on or after 2026-09-23 UTC (R3, below).**

## Why this study exists
Study T1x (`prereg/t1x/`, ledger row T1X-VOID, `reports/t1x.md`) was voided on 2026-09-22: its frozen scorer crashed on
`215_2dplanes` (feature 0 binary, the median split left task 2 empty, a numpy bool reached `json.dumps`) and its `score`
crashed on `218_house_8L` (the split gave a 165× extrapolation; non-finite path lengths reached the fits). No row was scored;
the six T1x carriers are SEEN. This study is the same design with four corrections to the frozen scorer, on six carriers
that have never been opened.

## What changed against T1x (the R3 statement)
Four rules were learned today from the T1x carriers `215_2dplanes` and `218_house_8L` and are therefore not usable on
another dataset today (R3). The data step of this study is on or after 2026-09-23 UTC, and each rule is named here:
1. **Split feature.** The split column is the first column with at least `MIN_DISTINCT = 20` distinct values (T1x: column 0
   unconditionally). A carrier with no such column is excluded and counted (learned on `215_2dplanes`).
2. **Admissibility gate.** A carrier whose base model has task-2 test MSE above `ADMISS_FACTOR = 20` × its task-1 test MSE is
   excluded and counted: the covariate split has produced an extrapolation the learner cannot follow (learned on
   `218_house_8L`, where the ratio was 165).
3. **Type cast.** The run's `finite` flag is cast to a Python bool before serialisation (a crash fix, no scientific content).
4. **Non-finite predictors.** A run with any non-finite predictor or forgetting value is dropped from the fits and counted
   (T1x dropped only diverged runs by loss; NaN path lengths reached the least-squares fit).
Everything else (model (d), schedules, lr grid, seeds, probes, snapshot intervals, fits, splits, thresholds, rows) is T1x's
as written in `prereg/t1x/PREREG.md`, restated below. H-T1 and the instrument's path quantities are unchanged. The smoke
carriers `synthetic_binary` (split moved to column 1) and `synthetic_extreme` (excluded by the gate) exercise the new rules;
both are pinned in `smoke.txt`/`smokefull.txt`.

## Anchoring — read this first
As EQ3, EQ4, BAYES-1 and T1x: OpenTimestamps unreachable, tag pushes refused (attempts recorded in `runs/t1x2/`). The GitHub
push timestamp of the commit carrying `HASH.txt` is the only external witness; every row carries `anchor: push-timestamp only`.

## Model (d), stated as a deviation
CLAUDE.md §5 names (a) a byte-level LM, (b) a GPT-2-small class model, (c) the RL's Razor data. None is available in this
environment (no GPU, no PyTorch, paper hosts blocked). Model (d): a numpy MLP, d-64-1, ReLU, squared loss, on unseen PMLB
regression streams. Rows are labelled model (d); (a)–(c) remain to run.

## Design (frozen in `runs/t1x2/frozen/t1x2_score.py`)
- Per carrier: split feature by rule 1; task 1 = rows at or below its median, task 2 = the rest (covariate drift); 80/20
  train/test per task (seed 12345); features and targets standardised on task 1's training rows; a carrier above 5000 rows
  is subsampled once at random to 5000 (seed 777). Rows with NaN dropped and counted. Admissibility by rule 2.
- One base model θ₀ per carrier: task 1, 30 epochs, lr 0.01, batch 10, init seed 0.
- Runs: fine-tune θ₀ on task 2 under (schedule, lr, seed), lr ∈ {0.0025, 0.005, 0.01, 0.02}, seeds {0, 1, 2}, schedules
  (20 epochs unless stated): `const`; `sawtooth` (lr × a triangle wave of period T/4, mean lr); `cosine_restarts` (period T/4,
  mean lr); `noise1.0`, `noise3.0` (Gaussian gradient noise of that sd × the running gradient scale); `loop` (odd epochs
  revisit task 1, so the path returns near the start); `short` (5 epochs); `long` (40 epochs); `restart` (10 epochs, reset to
  θ₀, 10 more: the path doubles, the endpoint is a const run's). 108 runs per carrier (≥ 60). A run whose final task-2 test
  MSE exceeds 100 × the base model's task-2 test MSE, or is non-finite, is diverged: dropped from the fits and counted.
- Per run: **forgetting** F = task-1 test MSE after − before. Predictors, on fixed probes (task-1 test rows, the OLD probe;
  task-2 test rows, the NEW probe; at most 500 each), predictive means snapshotted every 5 steps: C = Σ√(2·KL_gauss) (path),
  E = KL_gauss(base → final) (endpoint), on each probe; S = C − C* on the old probe; the EWC Fisher-weighted endpoint
  distance (θ_T − θ₀)ᵀ diag(F₁) (θ_T − θ₀), F₁ the diagonal empirical Fisher of task 1 at θ₀. C is also computed at
  snapshot intervals 10 and 20 (sensitivity). Runs dropped by rule 4 are counted per carrier.
- Fits: OLS of log F (floored at 1e-6) on log predictor **with log lr as a covariate** (the learning-rate control), fitted on
  half the runs and scored by R² on the other half; the main split takes alternate runs in (schedule, lr, seed) order; two
  further splits (seeds {0, 1} fit / seed 2 score; the other parity) are the sensitivity.

## Rows (scored once by `t1x2_score.py score`)
| row | prediction | threshold | verdict rule |
|---|---|---|---|
| T1x-0 | precondition: within each lr, C_old spans ≥ 3× across schedules and seeds | 3× | else NOT DECIDABLE on that carrier |
| T1x-1 | held-out R²(best of C_new, C_old) ≥ R²(best of E_new, E_old, EWC distance) + 0.05, lr controlled | ±0.05 | PASS if ≥ +0.05; FAIL if an endpoint wins by ≥ 0.05; INCONCLUSIVE between; per carrier, and PASS overall only on every decidable carrier, FAIL overall if any carrier FAILs |
| T1x-2 | fixed-lr arm (lr 0.01, 27 runs): Spearman(C_old, F) ≥ 0.6 and Spearman(E_new, F) < Spearman(C_old, F) − 0.2 | as stated | PASS / FAIL per carrier (C_new, E_old and the EWC distance printed beside) |
| T1x-3 | the surrogate control: `gate_T1.txt` (S-H, endpoint-sufficient, must FAIL; S-H2, path-dependent by construction, must PASS) | the gate's own | pinned in this folder, GATE OPEN |
| T1x-S | sensitivity: T1x-1 over 3 splits × 3 snapshot intervals | > 1 flip | FRAGILE / not fragile |
| T1x-D | S/C* per run and whether high-S runs fall off the endpoint curve (Spearman of S with the residual of the E_old fit) | 0.3 | report only |
| T1x-X | exclusions: carriers excluded by rules 1–2 and runs dropped by rule 4 and the divergence rule, counted | — | report only; the study is decided on the carriers that remain, however many; a carrier excluded by a pre-registered gate is not a failure and not a pass |

Ledger ids will be `T1X2-*`. What the outcomes mean: T1x-1 PASS on a non-convex learner with the learning rate controlled and
the old-probe endpoint in the race would be H-T1's first held-out result; FAIL says the endpoint is sufficient on this
learner too and H-T1 retires as tested; INCONCLUSIVE says the path and the endpoint carry the same information here.

## Gate (R4)
`gate_T1.txt`: the instrument is unchanged since T1x's gate run on 2026-09-22 (copied from `prereg/t1x/gate_T1.txt`, same
`core.py`), GATE OPEN. S-H FAIL (path − endpoint −0.904; the old-probe endpoint at R² 0.997), S-H2 PASS (path − endpoint +0.231).

## Data (must be absent from data/SEEN.md — confirmed: none appears)
PMLB regression sets on the GitHub mirror (`data/fetch_pmlb.py --manifest t1x2`). Selection rule, applied to the PMLB summary
table (`all_summary_stats.tsv`, fetched 2026-09-22) and to `data/SEEN.md`: regression sets not in SEEN.md, at most 50
features, at least 3000 rows, excluding siblings of a seen set (the `cpu_small`/`cpu_act` variants of the seen `197_cpu_act`;
`574_house_16H`, the same 22784 rows and target as the seen `218_house_8L`) and the two BNG sets of a million rows
(`1191_BNG_pbc`, `1196_BNG_pharynx`; 89 MB and 19 MB LFS objects). That leaves three BNG sets, taken whole, and the Feynman
symbolic-regression sets (100000 rows each), of which the three with the most features are taken, ties broken by name:
`1199_BNG_echoMonths` (17496 rows, 9 features), `1201_BNG_breastTumor` (116640, 9), `1203_BNG_pwLinear` (177147, 10),
`feynman_I_9_18` (100000, 9), `feynman_II_36_38` (100000, 8), `feynman_test_1` (100000, 7). Row and feature counts from the
summary table, not the files; availability checked by the LFS pointers only (each pointer 132–133 bytes, HTTP 200). No
fallbacks. `1203_BNG_pwLinear` is listed with 0 continuous features: if rule 1 finds no split column it is excluded and
counted, which is the rule doing its job, not a reason to replace it.

## Seeds and determinism (R9)
Base seed 0; run seeds 0–2 (batch order, noise); split seed 12345; subsample seed 777. `smoke.txt` and `smokefull.txt` are
byte-identical on rerun and produced by the frozen copy; on the data day one run per carrier is rerun twice
(`studies/t1x2/rerun_check.py` → `runs/t1x2/rerun_check.txt`); the `uv.lock` sha256 is in every results header.

## Baselines (R7)
E_new, E_old (the sufficient statistic on a convex learner) and the EWC Fisher-weighted endpoint distance, all fitted with
the same learning-rate control and scored on the same held-out half.

## Scoring script
`runs/t1x2/frozen/t1x2_score.py` (copy of `studies/t1x2/t1x2_score.py` at hash time), with `core.py` and `CRR.md`; sha256 in
`HASH.txt`. Data-day commands (on or after 2026-09-23 UTC):
```
uv run python data/fetch_pmlb.py --manifest t1x2 1199_BNG_echoMonths 1201_BNG_breastTumor 1203_BNG_pwLinear feynman_I_9_18 feynman_II_36_38 feynman_test_1
for c in 1199_BNG_echoMonths 1201_BNG_breastTumor 1203_BNG_pwLinear feynman_I_9_18 feynman_II_36_38 feynman_test_1; do uv run python runs/t1x2/frozen/t1x2_score.py all $c > runs/t1x2/log_$c.txt 2>&1; done
uv run python runs/t1x2/frozen/t1x2_score.py score runs/t1x2/results_*.jsonl > runs/t1x2/score.txt
uv run python studies/t1x2/rerun_check.py > runs/t1x2/rerun_check.txt
```
