# Pre-registration — SOTA-facing CRR tests. 2026-09-14 (after the literature review), before any run.

## T1 — Path length vs endpoint (the open prediction; RL's Razor uses endpoint KL on the new task)
Setup: toy LM (lm_bench), pretrained checkpoint, fine-tune on D1 (Python) only, no replay. Vary the trajectory:
lr ∈ {2e-4, 5e-4, 1e-3, 2e-3, 5e-3}; schedule ∈ {constant, sawtooth (lr×3 every 10th step, lr/3 otherwise)}; seeds 0–1.
Fixed budget 150 steps. Log every step: KL_step(new) = KL(p_{t-1}‖p_t) on a fixed D1 probe (8 seqs);
KL_step(old) likewise on a D0 probe. Candidates for predicting forgetting F = D0 bpb(final) − D0 bpb(pretrained):
  E_new = KL(base‖final) on the D1 probe (RL's Razor's predictor)
  C_new = Σ_t sqrt(2·KL_step(new))   (CRR: arc actually travelled, new-task manifold)
  C_old = Σ_t sqrt(2·KL_step(old))   (arc travelled as seen from the settled past)
  E_old = KL(base‖final) on the D0 probe (near-tautological control; reported, not a candidate)
Prediction (CRR A2): F is better predicted by path (C_new or C_old) than by endpoint E_new, and the gap opens on the
sawtooth trajectories (surplus S = C − C* > 0). Score: Spearman ρ and R² of log F on each predictor across the 20 runs.
PASS if R²(C_new or C_old) ≥ R²(E_new) + 0.05. FAIL if E_new wins by ≥ 0.05. Also report whether the sawtooth runs
fall off the E_new curve and onto the C curve.

## T2 — Equanimity vs the published LLM recipe (Marek et al. 2026: KL-to-base on a 4×-smaller replay batch, λ=10)
lm_bench, four-domain stream, seeds 0–1. Arms: ER(0.25); KLrep(0.25, λ=10) = replay batch with KL(base‖model) loss
weight 10 (their recipe, their λ); EQ(0.1, Ω=1); EQ(0.25, Ω=1). Metrics: D0 forgetting, domain bpb, compute/seq.
PASS if EQ(0.25) is within 0.03 bpb of KLrep(0.25) on D0 at equal-or-better domain bpb (λ-free vs λ=10).

## T3 — Abundant memory suppresses plasticity (Cho et al., ICLR 2026): does equanimity avoid it?
Split-KMNIST, seeds 0–2, buffer B ∈ {500, 5000}. Arms: ER(1.0), EQ(0.2, Ω=1). Metrics: final avg acc; last-task acc
(plasticity). Prediction: ER's last-task acc drops with B=5000 (Cho); EQ's does not drop by more than 1.0 pt,
because w adapts as the past's pull saturates. FAIL if EQ's last-task acc drops by > 2.0 or ER's does not drop.
