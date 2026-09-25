# Declaration 2: a comparative investigation, CRR against FOREVER, on synthetic continual-learning worlds

**Status and timing.**
- Owner request: prompt-log entry 181: "run multiple synthetic data tests to determine what crr is and what FOREVER is and
  how CRR could potentially be able to further enhance these findings ... apply the full CRR".
- A declared synthetic battery at rung R4. It is not a ledger row and opens no data.
- Written on 2026-09-25 and pushed before `checks/comparative.py` exists.
- FOREVER is arXiv 2601.03938 v2 (`docs/citations/forever_2026-09-25.md`). Declaration 1 and its results are in
  `DECLARATION.md` and `checks/forever_checks.txt`.

## 1. What is compared

FOREVER is decomposed into its choices. Each choice is swapped, one at a time, for the choice a CRR commitment makes.
The full CRR learner makes every CRR choice at once.

| component | FOREVER (eq.) | CRR choice | CRR source |
|---|---|---|---|
| clock | Euclidean arc of the trainable weights, τ = ΣΔ (2–3), reset per task | Fisher arc of the predictions, C = Σ√(2·KL_step) on a fixed probe, reset per task | D2, D6, A3 |
| unit | τ_day = the sum of the first S Δs, i.e. S × mean (4) | S × median of the first S step lengths, a robust unit | A1′ |
| what is measured | the path | the chord √(2·KL(p_start ‖ p_t)), the displacement since the cut | D3; the record: T1X2-1 and ARC-T1b found the endpoint, not the path, predicts forgetting |
| replay weight | β_t = β_base · clip(1 + γ(r_t − 1), 0.5, 3), with γ = 1 because the paper states no value | the step-bounded weight w = Ω‖ĝ_old‖/‖ĝ_anchor‖, with Ω = 1, EMA 0.9, cap 10⁴ | H-EQ |
| anchor | Θ* = the end of the previous task (11) | the age-weighted mean of every past task's end, Σπ_k Θ*_k, with π_k ∝ q^age, normalised (Σπ = 1), q = 0.5 | A6, P3 |
| replay sampling | uniform over the buffer | past tasks sampled with normalised age weights q^age, q = 0.5 | P3, A6 |
| replay sampling, alternative | uniform | past tasks sampled with surplus weights π_k ∝ exp(S_k / mean S), S_k = C_k − C*_k of task k's training | P2 (β fixed at 1/mean S; CRR does not fix β) |

**The arms.**
- **B0 fine-tune:** no replay and no anchor.
- **B1 ER-mix:** a replay batch is mixed into every step, with summed losses. This is the standard strong baseline; it
  uses more replay compute, which is counted and reported.
- **B2 FIR:** fixed-interval replay, with the same number of events, evenly spaced in steps.
- **B3 STC:** FOREVER with step calibration, triggers at d × S steps.
- **F FOREVER:** as published, with the constants of the paper.
- **The one-swap arms:**
  - C1 is F with the Fisher clock.
  - C2 is C1 with the A1′ robust unit.
  - C3 is F with the Fisher chord clock.
  - C4 is F with the H-EQ weight.
  - C5 is F with the A6 anchor.
  - C6 is F with P3 sampling.
  - C7 is F with P2 sampling.
- **CRR-full:** C2's clock, C4's weight, C5's anchor and C6's sampling together.

**The replay budget.** Every event-based arm (B2, B3, F and C1–CRR-full) gets the same number of replay events per task
(six, one per FOREVER day d in {1, 2, 4, 7, 15, 30}). A threshold not reached by the end of the task fires at the task's
end. So the arms differ only in when replay happens and how it acts, not in how much of it there is.
- One event is R = 10 SGD steps on buffer batches with FOREVER's replay loss, L_old + β‖Θ − Θ*‖².
- Every event-based arm also runs FOREVER's end-of-task consolidation, one event.

## 2. The worlds (all synthetic; 10 seeds each, seeds 0–9)

| world | model | stream | what it probes |
|---|---|---|---|
| W1 base | LoRA-factored softmax, W = W₀ + PQ, d 20, K 4, rank 4 | 5 domain-incremental tasks with drifting class means; 300 steps per task; lr 0.05; batch 10 | FOREVER's own setting in miniature |
| W2 null movement | as W1, plus 8 input features that are always zero, whose weights take noise with sd 0.01 per step | as W1 | movement that changes no prediction (Declaration 1, F2) |
| W3 parametrisation | as W1, with P's initialisation ×4 and Q's ×1/4 (same product) | as W1 | FOREVER's clock is not invariant to the LoRA factorisation (F1) |
| W4 learning rates | as W1 | the learning rate per task ×(1, 4, 0.25, 2, 0.5) | FOREVER's premise: steps are the wrong clock |
| W5 convex (must-fail) | linear softmax, W fully trainable (convex) | as W1 | a convex learner, where forgetting is a function of the endpoint |
| W6 class-incremental | two-layer ReLU MLP, hidden 32, full-parameter | 10 classes in 5 tasks of 2 | the standard class-incremental protocol |
| W7 long | as W1 | 15 domain-incremental tasks | where A6's anchor and P3's ages have many occasions to act on |

**The fixed parts of every run.**
- **The buffer:** 50 samples per past task, fixed at the task's end.
- **The Fisher probe:** 100 current-task training inputs plus up to 100 buffer inputs, fixed at the task's start.
- **Scoring:** the final accuracy over every task's test set (OP), and BWT.
- **β_base:** tuned once for FOREVER on W1 with separate tuning seeds 100–104, on the grid {10⁻⁴, 3·10⁻⁴, …, 1, 3}, then
  held fixed in every world. That follows the paper's practice of one set of hyperparameters across datasets.

## 3. The labels (computed by the script, R15)

For each world and each arm against F:
- **The difference** d is the arm's OP minus F's OP, paired by seed.
- **The step** is max(1.0 point, 2·SE of the paired differences). That is the repository's resolvable step.
- **The label** is AHEAD if mean d > step, BEHIND if mean d < −step, and TIE otherwise.

**The gate for the clock claims** (C1, C2, C3):
- **Must fail:** no clock arm reads AHEAD in W5 (convex).
- **Must pass:** C1 reads AHEAD in W2, the world built to carry the effect.
- If either condition fails, the gate is CLOSED. No clock claim then goes to a prereg (R12), and the remaining rows are
  reported without a claim.

**The sensitivity check.**
- The C1-against-F label in W2 and W5 is recomputed at S = 12 and S = 48, the paper's own alternatives.
- If the label flips in more than one of those four cells, the result is FRAGILE.

## 4. Predictions, stated before the run (priors, honest about direction)

| # | prediction | direction for CRR |
|---|---|---|
| P1 | C1 AHEAD of F in W2 | positive control |
| P2 | C1, C2 and C3 TIE with F in W5 | negative control |
| P3 | C1 TIE or AHEAD of F in W3 | CRR-favourable |
| P4 | B3 (step clock) BEHIND F in W4 | FOREVER's premise |
| P5 | C4 TIE with F in W1 | neutral |
| P6 | C5 TIE with F in W1–W6 and not BEHIND in W7 | CRR-favourable in W7 only |
| P7 | C6 BEHIND F in at least one of W1, W6, W7: age weighting starves old tasks | **CRR-unfavourable** |
| P8 | C7 TIE with F everywhere: surplus weights have no positive control, as the SAL gate found | neutral |
| P9 | B1 (ER-mix, more replay compute) AHEAD of F in at least 5 of 7 worlds | reference |
| P10 | CRR-full not BEHIND F in at least 4 of 7 worlds | CRR-favourable; the record (H-EQ, P3) makes a FAIL plausible |

A prediction HOLDS or FAILS as computed. No threshold is changed after the run. A crash or undefined quantity is repaired
only by a pushed amendment before any rerun, as in Declaration 1.
