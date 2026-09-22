# Pre-registration — BAYES-1: the normalised penalty step against the exact sequential Bayes posterior, on six unseen PMLB regression streams

Study id: `bayes1`. Written, hashed and pushed 2026-09-22 (prompt-log entries 75 and 84); data fetched after the push
(fetch timestamps in `data/manifests/bayes1.sha256` and `data/SEEN.md`). Author: the agent, under CLAUDE.md §1.
Anchoring: push timestamp only (below).

## What this study is
The first test of the rule against a computable Bayes optimum. On Bayesian linear regression with fixed random features the
sequential posterior is exact, so every arm can be measured by its distance from the posterior in the posterior's own metric
rather than by accuracy against a tuned baseline. The mathematics (`theory/checks/omega_sweeps.txt` [1]) says the rule reaches
the Bayes point only by coincidence; the reprocessing (`theory/checks/omega_reprocessed.txt` [1]) says the rule is invariant to
the scale of the past curvature when the term's noise scales with it and not otherwise; and the cross-verification found the
rule alone scale-robust against a fixed weight on the quadratic. This study asks which of those survive on real streams with
mini-batch noise, with the exact posterior as the referee.

## R3 statement
The registered rule and its estimator (EMA 0.9, cap 1e4, floor 1e-12, Euclidean norm) are unchanged since study EQ2
(2026-09-17). The scoring statistic (distance to the exact posterior in posterior-sd units per dimension), the model (random
tanh features whitened on the stream's training rows), the learning-rate rule and the calibration axis were defined today from
the mathematics and the synthetic gate, not from any dataset. The bounded rule EQ-B was defined today after seeing EQ3's
carriers and is **not** in this study (R3); it may enter a later study on a later day. Nothing was learned on the six carriers
below; their availability was checked by fetching each dataset's 131-byte LFS pointer only.

## Anchoring — read this first
As EQ3 and EQ4: OpenTimestamps calendars are unreachable from this environment and tag pushes are refused by the remote
(attempts recorded in `runs/bayes1/ots_attempt.txt`, `tag_attempt.txt`, `tag_push_attempt.txt`). The only external witness
to "before" is the GitHub push timestamp of the commit carrying `HASH.txt`. Every ledger row of this study carries
`anchor: push-timestamp only`; the strongest label available is PASS-0.

## The model and the referee (frozen in `runs/bayes1/frozen/bayes1_score.py`)
- Features φ(x) = [1, whitened tanh(W x + b)], W ~ N(0, 1/d) and b ~ U(−1, 1) fixed by seed 12345, 30 hidden features
  (D = 31 parameters), whitening (PCA, floor 1e-3) fitted on the training rows of the whole stream, never on a test row.
- Likelihood y ~ N(φᵀθ, σ² = 1) on targets standardised on chunk 1's training rows; prior θ ~ N(0, I/α), α = 1.
- Stream: rows sorted by feature column 0 (ties by index) into K = 5 chunks of equal size (covariate drift); a fixed 20 % test
  split per chunk (seed 12345); a carrier above 5000 rows is subsampled once at random to 5000 (seed 777) before sorting.
- The exact sequential posterior: Λ_k = Λ_{k−1} + Φ_kᵀΦ_k/σ², μ_k = Λ_k⁻¹(Λ_{k−1}μ_{k−1} + Φ_kᵀy_k/σ²), Λ_0 = αI, μ_0 = 0.
- The score of an arm: d = √((θ − μ_K)ᵀ Λ_K (θ − μ_K) / D), the arm's endpoint's distance from the final posterior mean in
  posterior standard deviations per dimension. Held-out MSE over every chunk's test rows is reported beside it, with the
  exact posterior predictive's MSE as the reference.

## The arms
Every arm is SGD on θ with g = g_present + w·g_past: present = the batch's mean squared error (batch 10); past = the exact
Laplace penalty of everything before the chunk in per-sample units, P(θ) = (c/2n_k)(θ − θ*)ᵀΛ_{k−1}(θ − θ*), anchored at the
arm's **own** endpoint after the previous chunk (chunk 1's past is the prior). 50 epochs per chunk; learning rate
= 0.5 / (K × the 95th percentile of the top eigenvalue of a batch's feature covariance), computed once per carrier from the
training features (the Bayes arm's stability edge at the last chunk with a factor-2 headroom). Seeds 0–4 permute the batches.
- Calibration c ∈ {1/16, 1, 16} multiplies the past curvature. At c = 1 the penalty is the exact Fisher.
- `fixed` λ ∈ {1/16, 1/8, 1/4, 1/2, 1, 2, 4, 8, 16} at every c. **λ = 1 at c = 1 is the Bayes arm**: run to convergence it
  reproduces the exact posterior chunk by chunk (B0 checks that it did).
- `eq` Ω ∈ {0.25, 0.35, 0.5, 0.71, 1, 1.41, 2, 2.83, 4} at every c, the registered estimator; sensitivity at Ω = 1, c = 1 over
  cap ∈ {10, 100, 1e4} × smooth ∈ {0.8, 0.9, 0.98}.
- `reduction`: fixed w at the median derived weight of the Ω = 1, c = 1 run.

## Gate (R4) — `gate_BAYES.txt`, committed here and covered by the hash
On a synthetic drifting stream (d = 6, n = 2500): GATE OPEN. The Bayes arm converges (d = 0.0650, within the B0 tolerance
0.1); B1's statistic does not fire on a second Bayes arm run twice as long (d = 0.0636, the negative control) and fires on a
fixed weight that is not the Bayes weight (λ = 4, d = 1.7672, the positive control). Informational rows the prereg relies on:
the rule at Ω = 1 sits at d = 7.1693 on the ordinary start and at 2.0024 when started at the exact posterior each chunk (it
drifts off the knife edge: the EMA estimator with mini-batch noise does not rest where the exact-norm rule would); at c = 16
the miscalibrated Bayes arm is at 3.3812 against the rule's 7.4000, at c = 1/16 at 4.6847 against 6.1273, so **the surrogate
says B2 FAILS in both directions**; the rule's d at c = 1/16, 1, 16 is 6.1273, 7.1693, 7.4000, so **the surrogate says B3
FAILS** (the invariance is to the term, not to the mini-batch noise). B2 and B3 are registered with the surrogate's verdict
as the predicted outcome: a PASS on the carriers would contradict the surrogate and is the outcome to watch for.

## Data (must be absent from data/SEEN.md — confirmed 2026-09-22: none appears)
PMLB regression sets on the GitHub mirror (LFS object, pointer oid verified, `data/fetch_pmlb.py --manifest bayes1`): six
carriers chosen from the summary table (`pmlb/all_summary_stats.tsv`) as regression sets with 3000–25000 rows, taking the six
with the largest row counts among those with at most 50 features and skipping the near-duplicate pairs (cpu_act / cpu_small,
puma8NH / puma32H) once: `503_wind` (6574 × 14), `529_pollen` (3848 × 4), `197_cpu_act` (8192 × 21), `225_puma8NH`
(8192 × 8), `537_houses` (20640 × 8), `201_pol` (15000 × 48). Row and feature counts from the summary table, not the files.
Rows with NaN dropped and counted. No fallbacks: a carrier that cannot be fetched or fails the oid check is reported as missing
and rows needing "every carrier" are scored on the carriers present with the denominator stated. A run whose parameters are
non-finite scores d = ∞ and is counted.

## Rows (scored once by `bayes1_score.py score`; per carrier and per seed values printed)
Aggregation: mean over five seeds, per-seed values beside every mean; step = max(0.05, 2 SE of the rule's d at Ω = 1, c = 1)
in posterior-sd units; "every carrier" = the carriers present.

| row | prediction | threshold | verdict rule | surrogate |
|---|---|---|---|---|
| B0 | precondition: the Bayes arm converges to the exact posterior | d(Bayes) < 0.1 on every carrier | else NOT DECIDABLE (the optimiser, not the rule, is being measured) | 0.0650 |
| B1 | the rule at Ω = 1 is not Bayes: d(rule) − d(Bayes) > step on every carrier | step | PASS / FAIL | fires (7.1693 vs 0.0650) |
| B2 | at c = 16 and at c = 1/16, the rule is closer to the exact posterior than Bayes with the miscalibrated curvature: d(rule) − d(fixed λ = 1) < −step on every carrier | step | PASS / FAIL, each c separately | **FAIL** predicted |
| B3 | the rule's own scale invariance: \|d(rule, c) − d(rule, 1)\| < step for c = 16 and 1/16 on every carrier | step | PASS / FAIL | **FAIL** predicted |
| B4 | the tuned fixed λ (in-sample on d, grid above) is the Bayes weight: d(tuned) within a step of d(Bayes) on every carrier | step | report (a check that the exact model behaves) | — |
| B5 | held-out MSE of the exact posterior predictive, the Bayes arm, the rule and the tuned λ | — | report | — |
| B6 | the Ω plateau in d | within a step of the best | report | — |
| B7 | reduction: \|d(rule) − d(fixed at the median derived w)\| < step | step | report | — |
| BS | sensitivity of B1 over the 8 cap × smooth cells per carrier | > 1 flip | FRAGILE / not fragile | — |

What the outcomes mean: B1 PASS confirms on real streams what the mathematics says (the rule is a controller, not an
inference rule); B1 FAIL would mean the rule reaches the posterior within a step on real streams, which the mathematics
does not predict and the surrogate does not show. B2 PASS in either direction would contradict the surrogate and say the
rule's robustness to miscalibration is real on data; B2 FAIL as predicted says a Bayes with the curvature wrong by 16× is
still closer to the posterior than the rule, because the rule's mini-batch bias costs more than the miscalibration. B3 FAIL
as predicted quantifies how much the mini-batch noise breaks the invariance the mathematics has for the noiseless term.

## Seeds and determinism (R9)
Run seeds 0–4 (batch order); feature seed 12345; split seed 12345; subsample seed 777. Two runs of one unit must be
byte-identical (`cmp`; checked on one arm per carrier in `runs/bayes1/rerun_*.json`); `smoke.txt`, `smokefull.txt` and
`gate_BAYES.txt` are byte-identical on rerun and produced by the frozen copy; the `uv.lock` sha256 is in every results header.

## Baselines (R7)
The exact posterior (the referee, distance 0 by definition); the Bayes arm (the same optimiser, the Bayes weight, the exact
curvature); the tuned fixed λ (in-sample on d); the miscalibrated Bayes arms; the reduction arm.

## Scoring script
`runs/bayes1/frozen/bayes1_score.py` (copy of `studies/bayes1/bayes1_score.py` at hash time), with `runs/bayes1/frozen/core.py`
and `CRR.md`; sha256 in `HASH.txt`. Data-day commands:
```
uv run python data/fetch_pmlb.py --manifest bayes1 503_wind 529_pollen 197_cpu_act 225_puma8NH 537_houses 201_pol
for c in 503_wind 529_pollen 197_cpu_act 225_puma8NH 537_houses 201_pol; do uv run python runs/bayes1/frozen/bayes1_score.py all $c > runs/bayes1/log_$c.txt 2>&1; done
uv run python runs/bayes1/frozen/bayes1_score.py score runs/bayes1/results_*.jsonl > runs/bayes1/score.txt
```
