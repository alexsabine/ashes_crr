# Pre-registration — compute-matched replay vs CRR-scheduled EMA self-distillation, LM regime (Stage A′). 2026-09-14, before any run.

## Why
Stage A (class-IL) falsified the pitch's compute claim, but class-IL is not the LLM regime. This is the smallest
honest version of the LLM regime: a byte-level transformer pretrained on general English prose, then continually
fine-tuned through four domains, forgetting measured as held-out loss on the pretraining domain.

## Setup (fixed)
- Model: byte-level (vocab 256) causal transformer, d=128, 4 layers, 4 heads, ctx 128, ~0.8 M params. AdamW lr 1e-3,
  batch 16 sequences. Same pretrained checkpoint for every arm (seed 0 pretrain; seeds vary the stream/replay only).
- D0 pretrain: Austen + Melville + Eliot (Gutenberg), 3.0 MB, one pass; held-out 64 KB of D0 for evaluation.
- Continual stream, in order: D1 Python (CPython stdlib), D2 Shakespeare, D3 German (Goethe, Mann), D4 C (Linux kernel);
  500 KB each, one pass, ~245 steps per domain. Held-out 32 KB per domain.
- Metric: bits per byte on held-out D0 at the end of the stream (**forgetting**, primary); mean bpb over held-out D1–D4
  (plasticity, secondary). Evaluated on the student and on the slow EMA where one exists; the primary comparison uses
  whichever the arm would deploy (student for ER; slow EMA for EMA arms, as CLS-ER does).
- Compute per stream sequence: student forward+backward 3; replayed sequence 3; teacher forward 1 per teacher
  (dual teachers = 2); Fisher-speed probe forward (8 sequences, every 4th step) counted at its true cost.

## Arms (seeds 0–2 for the stream)
- ER(r): replay from a reservoir over all seen sequences (D0 + earlier domains), r ∈ {0, 0.05, 0.1, 0.25, 0.5}.
- CRR-EMA(r, Ω): dual EMA teachers at Fisher-speed rates (kl unit), self-distillation KL(teacher‖student) weight λ=1 on
  the current batch (+ replay if any), teacher = more confident of the two on the batch; r ∈ {0, 0.05}; Ω ∈ {4, 16, 64}
  (one scale, small sweep, reported in full — no theory value exists for learners after today's unit test).
- fixed-EMA(r, α): same, fixed rates (α_fast, α_slow) ∈ {(0.01, 0.001), (0.03, 0.003), (0.1, 0.01)}; r ∈ {0, 0.05}.
  Same tuning budget as CRR.
- CRR-EMA-sparse(0.05, Ω*): teacher every 4th step.

## Hypotheses
- **L1 (pitch claim):** best CRR-EMA(0.05) reaches D0 forgetting ≤ ER(0.25) + 0.02 bpb. FAIL if worse than ER(0.25) by > 0.05.
- **L2 (compute):** at equal-or-better D0 bpb, compute of the qualifying CRR arm ≤ 0.8 × ER(0.5). (Ceiling is known to be
  small unless sparse; scored anyway.)
- **L3 (CRR vs fixed):** best CRR-EMA ≤ best fixed-EMA + 0.01 bpb at each r. FAIL if worse by > 0.03.
- **L4 (regime):** the gap between EMA arms and ER at r=0.05 is smaller here than in Stage A (reported, not scored).
Outcome table: L1 pass → GPU study warranted and stated in this regime. L1 fail → the compute claim is retired at
both scales tested; the schedule is kept as a quality complement to replay (Stage A) and a one-scale method.

## Amendment (2026-09-14, still before any run; cost check gave 0.6 s/step on one core)
Domains cut to 300 KB each (~150 steps per domain, ~590 stream steps). Ω and α sweeps and ER(0.1) run at seed 0 only;
the head-to-head — ER(0.05), ER(0.25), ER(0.5), best CRR-EMA(0.05), best fixed-EMA(0.05), CRR-EMA(0), sparse — at seeds 0–2.
"Best" is chosen by D0 bpb at seed 0, which is the same selection budget for CRR and fixed. Hypotheses unchanged.

## Post-hoc note (after seeing the seed-0 Ω sweep; labelled as such)
Ω=64 gives D0 bpb below the pretrained checkpoint with domain bpb 4.29 — the slow EMA simply did not learn. L1 as written
is therefore satisfiable by a degenerate arm. Scoring is amended: L1/L2 are judged at **matched plasticity** — an EMA arm
counts as reaching an ER arm's forgetting only if its domain bpb is within +0.05 of that ER arm's. Both slow-EMA and
student models are reported on both metrics. This tightens the test against CRR; it does not loosen it.
