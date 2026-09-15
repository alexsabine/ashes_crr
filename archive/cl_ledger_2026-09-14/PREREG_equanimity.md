# Pre-registration — equanimity replay: κ as a Fisher ratio (Ω = 1). 2026-09-14, before any run.

## Idea
A6 at bounded strength κ, stated as a ratio: the settled past and the live present contribute equal Fisher travel to
each update. Per step, g_new = gradient on the stream batch, g_past = gradient on a replay batch of fraction r.
Update with g = g_new + w·g_past, w = Ω · ‖g_new‖_F / ‖g_past‖_F, ‖g‖_F = sqrt(Σ F̂ g²) with the bench's running
diagonal Fisher (the metric cancels in the ratio, so this is estimator-invariant). Ω = 1 is the theory value; w is
capped at 20 (cap frequency reported). Compute per stream sample = 3(1 + r): the weighting is free.

## Runs (Split-KMNIST class-IL, repo pipeline, standard stream, seeds 0–2)
- EQ(r, Ω): r ∈ {0.05, 0.1, 0.25}, Ω ∈ {0.25, 0.5, 1, 2, 4}.
- ER(r) curve from today's compute test (r ∈ {0.05 … 1.0}) is the comparison.
Then the LM regime (lm_bench.py, seeds 0–2): EQ(0.05, Ω ∈ {0.5, 1, 2}) against ER(0.05/0.25/0.5).

## Hypotheses
- **Q1 (interior optimum at the theory value):** on KMNIST the Ω sweep at r = 0.05 has its best point at Ω = 1, with
  Ω = 0.25 and Ω = 4 both worse by > 1.0 pt. FAIL if Ω = 1 trails the best by > 1.0.
- **Q2 (the compute claim, restated in the working mechanism):** EQ(0.05, 1) ≥ ER(0.5) − 1.0 pt on KMNIST at
  compute 3.15 vs 4.50 (30 % less). FAIL if trails by > 2.0.
- **Q3 (LM regime):** EQ(0.05, 1) reaches ER(0.5)'s D0 forgetting within 0.03 bpb at matched plasticity (domain bpb
  within +0.05), compute 3.15 vs 4.51. FAIL if forgetting worse by > 0.06 or plasticity worse by > 0.1.
- **Q4 (recurrence):** on the recurring KMNIST stream EQ(0.05, 1) ≥ ER(1.0) − 1.0.
Outcome: Q2 ∧ Q3 pass → the 30–50 % compute claim is alive in the regeneration mechanism, parameter-free at Ω = 1;
Q1 fail with Q2 pass → adaptive weighting works but Ω is a tuned scale again; Q2 fail → κ needs a different derivation.
