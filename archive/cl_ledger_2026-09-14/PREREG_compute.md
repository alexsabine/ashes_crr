# Pre-registration — compute-matched test of the pitch's central claim (Stage A, small scale). 2026-09-14, before any run.

## The claim (pitch §4)
"Continual fine-tuning with an EMA teacher at CRR-scheduled rates reaches the forgetting level of 25–50 % replay
with near-zero replay" → compute falls by a third to a half.

## Two facts fixed before running
1. Every CRR-CLS number in the ledger was obtained at **100 % replay** (replay batch 10 on a stream batch of 10).
   The near-zero-replay regime has never been run. This test is the first.
2. Compute accounting (FLOP-proportional, per stream sample): student forward+backward = 3; each replayed sample = 3;
   each teacher forward = 1; EMA parameter update ≈ 0 (O(params), not O(params×batch)).
   Hence an EMA-teacher method that distils on every current sample costs ≥ 1/3 of a replayed sample → it can only
   save compute against replay fractions > ~33 %. Against 25 % replay it cannot win on compute; against 50 % the
   ceiling saving is ~(1.5−1.33)/1.5 ≈ 11 % unless the teacher is applied to a subset of batches. This is written down
   now so the result can't be re-read afterwards.

## Arms (Split-KMNIST then Split-CIFAR-10, class-IL, standard stream, seeds 0–2, repo pipeline)
- **ER(r)**: reservoir replay, replay batch ⌈r·10⌉ with fractional r by Bernoulli; r ∈ {0, 0.05, 0.1, 0.25, 0.5, 1.0}.
- **CRR-EMA(r)**: dual EMA teachers at Fisher-speed rates (kl unit, Ω at the dataset optimum found today — one scale),
  consistency loss (λ=0.2 logit MSE to the more confident teacher) on the **current** batch and any replay; r ∈ {0, 0.05, 0.25}.
- **fixed-EMA(r)**: same, teachers at the ledger's best tuned CLS-ER rates; r ∈ {0, 0.05}. (The honest baseline.)
- **CRR-EMA-sparse(0.05)**: teacher applied every 4th update only (cost 0.25 per sample) — the only configuration that
  could beat 25 % replay on compute.
Metric: final accuracy over all classes (forgetting), plotted against compute per stream sample.

## Hypotheses
- **P1 (the pitch claim at small scale):** CRR-EMA(0.05) ≥ ER(0.5) − 1.0 pt. FAIL if trails by > 2.0.
- **P2 (compute):** at equal-or-better accuracy, compute of the winning CRR arm ≤ 0.7 × compute of ER(0.5).
- **P3 (CRR vs fixed):** CRR-EMA(r) ≥ fixed-EMA(r) − 0.5 at r ∈ {0, 0.05}. FAIL if trails by > 1.0.
- **P4 (regime caveat, reported not scored):** class-IL is the harshest regime; a null here does not falsify the LLM
  claim (where forgetting is mild and regularisation-only methods are known to work), but a pass here is necessary
  before spending GPU time.
