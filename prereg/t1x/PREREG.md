# Pre-registration — T1x: path length against endpoint displacement as a predictor of forgetting, learning rate controlled

Study id: `t1x`. Written, hashed and pushed 2026-09-22 (prompt-log entries 86–87); data fetched after the push (timestamps in
`data/manifests/t1x.sha256` and `data/SEEN.md`). Author: the agent, under CLAUDE.md §1. Anchoring: push timestamp only.

## What this study is
The held-out test of H-T1 (CLAUDE.md §5; `theory/CRR.md` D6/H-T1): does forgetting of an old task track the Fisher path
length travelled during fine-tuning rather than the endpoint displacement, once the learning rate is controlled? The two
prior facts: the convex-learner lemma (`theory/SCOPE.md` §4.1) makes the old-probe endpoint a sufficient statistic for
forgetting on any convex learner, and ledger row ARC-T1b found the old-probe endpoint at R² 0.99 on the original toy-LM runs
(the path beat the wrong endpoint). This study is on a non-convex learner, the only place the path could still win, with
the endpoint baselines that can win (R7) and no in-sample R².

## R3 statement
H-T1 and the instrument's path quantities (`path_length`, `kl_gauss`) are unchanged. The design is CLAUDE.md §5 as written
on 2026-09-15; the model, the schedules, the split rule and the thresholds below were fixed today from that design and the
synthetic smoke, not from any dataset. Nothing was learned on the six carriers, whose availability was checked by their
131-byte LFS pointers only. Nothing learned today on EQ3's, EQ4's or BAYES-1's carriers enters this study.

## Anchoring — read this first
As EQ3, EQ4 and BAYES-1: OpenTimestamps unreachable, tag pushes refused (attempts in `runs/t1x/`). The GitHub push timestamp
of the commit carrying `HASH.txt` is the only external witness; every row carries `anchor: push-timestamp only`.

## Model (d), stated as a deviation
CLAUDE.md §5 names (a) a byte-level LM, (b) a GPT-2-small class model, (c) the RL's Razor data. None is available in this
environment (no GPU, no PyTorch, paper hosts blocked). Model (d): a numpy MLP, d-64-1, ReLU, squared loss, on unseen PMLB
regression streams. Rows are labelled model (d); (a)–(c) remain to run.

## Design (frozen in `runs/t1x/frozen/t1x_score.py`)
- Per carrier: task 1 = rows with feature 0 at or below its median, task 2 = the rest (covariate drift); 80/20 train/test
  per task (seed 12345); features and targets standardised on task 1's training rows; a carrier above 5000 rows is
  subsampled once at random to 5000 (seed 777). Rows with NaN dropped and counted.
- One base model θ₀ per carrier: task 1, 30 epochs, lr 0.01, batch 10, init seed 0.
- Runs: fine-tune θ₀ on task 2 under (schedule, lr, seed), lr ∈ {0.0025, 0.005, 0.01, 0.02}, seeds {0, 1, 2}, schedules
  (20 epochs unless stated): `const`; `sawtooth` (lr × a triangle wave of period T/4, mean lr); `cosine_restarts` (period T/4,
  mean lr); `noise1.0`, `noise3.0` (Gaussian gradient noise of that sd × the running gradient scale); `loop` (odd epochs
  revisit task 1, so the path returns near the start); `short` (5 epochs); `long` (40 epochs); `restart` (10 epochs, reset to
  θ₀, 10 more: the path doubles, the endpoint is a const run's). Training length is a schedule parameter, named as such.
  108 runs per carrier (≥ 60). A run whose final task-2 test MSE exceeds 100 × the base model's task-2 test MSE, or is
  non-finite, is diverged: dropped from the fits and counted. The synthetic smoke needed the wider set: with the first six
  schedules the path spanned only 1.16× at the smallest lr (AGENT_LOG 68).
- Per run: **forgetting** F = task-1 test MSE after − before. Predictors, on fixed probes (task-1 test rows, the OLD probe;
  task-2 test rows, the NEW probe; at most 500 each), predictive means snapshotted every 5 steps: C = Σ√(2·KL_gauss) (path),
  E = KL_gauss(base → final) (endpoint), on each probe; S = C − C* on the old probe; the EWC Fisher-weighted endpoint
  distance (θ_T − θ₀)ᵀ diag(F₁) (θ_T − θ₀), F₁ the diagonal empirical Fisher of task 1 at θ₀. C is also computed at
  snapshot intervals 10 and 20 (sensitivity).
- Fits: OLS of log F (floored at 1e-6) on log predictor **with log lr as a covariate** (the learning-rate control), fitted on
  half the runs and scored by R² on the other half; the main split takes alternate runs in (schedule, lr, seed) order; two
  further splits (seeds {0, 1} fit / seed 2 score; the other parity) are the sensitivity.

## Rows (scored once by `t1x_score.py score`)
| row | prediction | threshold | verdict rule |
|---|---|---|---|
| T1x-0 | precondition: within each lr, C_old spans ≥ 3× across schedules and seeds | 3× | else NOT DECIDABLE on that carrier |
| T1x-1 | held-out R²(best of C_new, C_old) ≥ R²(best of E_new, E_old, EWC distance) + 0.05, lr controlled | ±0.05 | PASS if ≥ +0.05; FAIL if an endpoint wins by ≥ 0.05; INCONCLUSIVE between; per carrier, and PASS overall only on every decidable carrier, FAIL overall if any carrier FAILs |
| T1x-2 | fixed-lr arm (lr 0.01, 27 runs): Spearman(C_old, F) ≥ 0.6 and Spearman(E_new, F) < Spearman(C_old, F) − 0.2 | as stated | PASS / FAIL per carrier (C_new, E_old and the EWC distance printed beside) |
| T1x-3 | the surrogate control: `gate_T1.txt` (S-H, endpoint-sufficient, must FAIL; S-H2, path-dependent by construction, must PASS) | the gate's own | pinned in this folder, GATE OPEN |
| T1x-S | sensitivity: T1x-1 over 3 splits × 3 snapshot intervals | > 1 flip | FRAGILE / not fragile |
| T1x-D | S/C* per run and whether high-S runs fall off the endpoint curve (Spearman of S with the residual of the E_old fit) | 0.3 | report only |

What the outcomes mean: T1x-1 PASS on a non-convex learner with the learning rate controlled and the old-probe endpoint
in the race would be H-T1's first held-out result; FAIL says the endpoint is sufficient on this learner too and H-T1 retires
as tested; INCONCLUSIVE says the path and the endpoint carry the same information here.

## Gate (R4)
`gate_T1.txt`: re-run on the current instrument on 2026-09-22, GATE OPEN. S-H FAIL (path − endpoint −0.904; the old-probe
endpoint at R² 0.997), S-H2 PASS (path − endpoint +0.231).

## Data (must be absent from data/SEEN.md — confirmed: none appears)
PMLB regression sets on the GitHub mirror (`data/fetch_pmlb.py --manifest t1x`): six carriers from the summary table with
3000–60000 rows and at most 50 features, not used by BAYES-1 and not near-duplicates of its sets: `218_house_8L`,
`344_mv`, `564_fried`, `215_2dplanes`, `1193_BNG_lowbwt`, `294_satellite_image`. Row counts from the summary table, not the
files. No fallbacks. A run whose parameters are non-finite is dropped from the fits and counted.

## Seeds and determinism (R9)
Base seed 0; run seeds 0–2 (batch order, noise); split seed 12345; subsample seed 777. `smoke.txt` and `smokefull.txt` are
byte-identical on rerun and produced by the frozen copy; one run per carrier rerun twice (`runs/t1x/rerun_check.txt`); the
`uv.lock` sha256 is in every results header.

## Baselines (R7)
E_new, E_old (the sufficient statistic on a convex learner) and the EWC Fisher-weighted endpoint distance, all fitted with
the same learning-rate control and scored on the same held-out half.

## Scoring script
`runs/t1x/frozen/t1x_score.py` (copy of `studies/t1x/t1x_score.py` at hash time), with `core.py` and `CRR.md`; sha256 in
`HASH.txt`. Data-day commands:
```
uv run python data/fetch_pmlb.py --manifest t1x 218_house_8L 344_mv 564_fried 215_2dplanes 1193_BNG_lowbwt 294_satellite_image
for c in 218_house_8L 344_mv 564_fried 215_2dplanes 1193_BNG_lowbwt 294_satellite_image; do uv run python runs/t1x/frozen/t1x_score.py all $c > runs/t1x/log_$c.txt 2>&1; done
uv run python runs/t1x/frozen/t1x_score.py score runs/t1x/results_*.jsonl > runs/t1x/score.txt
```
