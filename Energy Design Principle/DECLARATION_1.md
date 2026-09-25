# Declaration 1: CRR's predictions for the mechanisms that save energy in AI training and execution

**Status.**
- **The request.** Owner request: prompt-log entry 199. Written on 2026-09-25.
- **When it was pushed.** Before any of the three source dossiers (`docs/citations/energy_*_2026-09-25.md`) exists. The
  dossiers will be fetched afterwards by research agents.
- **What it is.** A retrodictive battery, as for `CL Design Principle/DECLARATION_1.md`. It is not a ledger study, and it
  opens no data.

**Honesty clause.**
- **The predictions cannot be blind.** The investigator's training exposure includes much of this literature.
- **Seven sources were already read today** for prompt-log entry 198 (`docs/citations/compute_scale_2026-09-25.md`):
  - the IEA figures, as reported;
  - Patterson et al. 2022;
  - Wu et al. 2022;
  - Strubell et al. 2019;
  - Llama 3;
  - μTransfer's abstract, which bears on E1: tuning cost 7 % of pretraining;
  - the EIA household figure.
- **What the declaration fixes:**
  - the CRR reading of each mechanism, named by axiom;
  - the direction CRR implies;
  - the rule that grades it.
- **How labels are computed.** Every label is computed by `checks/retro_energy.py` from quoted numbers (R15). Every
  disagreement is examined, not explained away.

## The CRR ingredients used

The same list as the CL declaration:
- **A1**, the Fisher metric (information geometry's, not CRR's);
- **A1′**, the system's own resolvable step: lengths and settings are measured in the system's own unit, and nothing below
  one step carries distinguishable content;
- **D2 / D6**, the arc on the system's own clock: "change has its own clock";
- **A3**, the cut: no duration and no content, separating the settled past from the open future;
- **A6**, regeneration of the next occasion from the settled past's *content*, at bounded strength;
- **P2 / P3**, surplus and age weights;
- **A7**, nothing is fed by a future;
- **A8**, the future has no content;
- **H-EQ**, equal pull. It reduces to a constant on replay (EQX). SEC, its calibrated descendant, is not a CRR rule;
- **Proposition 7**, the empty cut.

## What an energy row compares

- **What a row is.** A mechanism X against its reference Y, with two quantities from the paper:
  - **quality Q:** accuracy, a score, perplexity or loss;
  - **cost C:** energy, FLOPs, accelerator-hours, wall time or generated tokens.

  Energy is preferred, then FLOPs, then time, then tokens. The kind of cost is recorded on the row.
- **The cost label.**
  - **SAVES:** C_X / C_Y ≤ 0.90.
  - **COSTS:** C_X / C_Y ≥ 1.10.
  - **SAME:** otherwise.
- **The quality step.**
  - On a 0–100 scale, the step is max(1.0 point, twice the larger reported standard deviation).
  - On a lower-is-better metric (perplexity, loss), the step is max(1 % of Y's value, twice the larger deviation).
- **The quality label.**
  - **AHEAD:** X better by at least a step.
  - **BEHIND:** X worse by at least a step.
  - **NOT BEHIND:** otherwise.
- **Matched-compute rows.** Where a paper compares at matched compute (cost SAME by design), only the quality label is
  graded, and the row is marked so.

## Prediction codes

| code | meaning | graded as AGREES when |
|---|---|---|
| **+** | a free saving | SAVES and quality NOT BEHIND or AHEAD. On a matched-compute row: quality NOT BEHIND or AHEAD |
| **0** | no free saving | SAME or COSTS; or SAVES with quality BEHIND |
| **q+** | a quality claim at matched cost | quality AHEAD |
| **q−** | X is worse at matched cost | quality BEHIND |
| **=** | lossless by construction: the output is identical by a theorem of the method, and it saves | SAVES. The kind is INHERITED: the mathematics guarantees it, and CRR's reading adds nothing testable |
| **S** | CRR is silent | not graded; listed |

## The mechanisms and CRR's prediction for each

### Training and development

| id | mechanism X against reference Y | CRR reading | kind | prediction |
|---|---|---|---|---|
| E1 | hyperparameter transfer from a small proxy (μP / μTransfer and successors) against tuning the target model directly | A1′: settings expressed in the system's own unit are scale-free, so they transfer | CLASS | + |
| E2a | a calibrated tuning-free weight (SEC in this repository; published analogues: uncertainty weighting, GradNorm) against a tuned constant | H-EQ corrected by A1′ (a units calibration) | COMPARATIVE | + |
| E2b | adaptive multi-task loss balancers against the plain sum of losses (unitary scalarisation) at matched compute | H-EQ reduces to a constant: equal pull *is* the sum (EQX), so a balancer adds nothing | COMPARATIVE | q− is not predicted; **0 difference**: graded AGREES when quality NOT BEHIND in both directions, that is \|ΔQ\| < step |
| E3 | successive halving / Hyperband / ASHA against full-budget random search | A7: rank on the settled past only. A3: cut the runs that the settled past already ranks low | CLASS | + |
| E4 | learning-curve extrapolation (predicting a run's final score from its partial curve) against successive halving alone | A8: an extrapolated future adds no content beyond the settled past it is computed from | COMPARATIVE | 0 |
| E5 | continual pre-training (warm start, learning-rate re-warming, replay) against retraining from scratch on the union of data | A6 + A3: regenerate from the settled past at the cut, not from nothing | CLASS | + |
| E6a | a warm start without repair against training from scratch, at matched final data | A6 at *bounded* strength: accumulated past weight without reweighting loses plasticity | COMPARATIVE | q− (warm start BEHIND in generalisation) |
| E6b | shrink-and-perturb (or another plasticity repair) on a warm start against the plain warm start | A6 as a reweighting: shrink the past's pull, keep its content | COMPARATIVE | q+ |
| E7 | model growth (initialising a larger model from a trained smaller one: stacking, bert2BERT, LiGO, MSG) against training the larger model from scratch | A6: seed the next occasion from the settled past's content | CLASS | + |
| E8 | weight averaging (EMA, LAWA, SWA, checkpoint averaging) against the last iterate, reaching a target quality | A6 + P3: regeneration with geometric age weights | CLASS | + |
| E9 | a horizon-free learning-rate schedule (warmup-stable-decay, schedule-free) against cosine with a fixed horizon | A8: a cosine schedule writes the future horizon into the present, and a horizon-free schedule does not. The cool-down is a cut (A3) | COMPARATIVE | + (NOT BEHIND at matched compute, and saves when several horizons are needed) |
| E10 | deduplication of training data against none | A1′: an indistinguishable repeat adds no arc | CLASS | + |
| E11 | salience or difficulty-scored data pruning against random selection at matched compute | P2 salience weighting. This repository's SAL gate closed, and the CL analogue M3 was predicted 0 | COMPARATIVE | 0 difference (\|ΔQ\| < step) |
| E12 | reduced-precision training (BF16, FP8) against higher precision | A1′: bits below one resolvable step carry no distinguishable content | CLASS | + |
| E13 | frequent, fast or in-memory checkpointing against slower or rarer checkpointing, on goodput | Proposition 7: a complete checkpoint is an empty cut; lost work falls with the cut's cost and interval | CLASS | + (cost = lost or wasted time) |
| E14 | mixture-of-experts (sparse activation) against dense at matched quality | none | — | S |
| E15 | compute-optimal allocation of parameters and tokens (Chinchilla) | none | — | S |

### Execution (inference and serving)

| id | mechanism X against reference Y | CRR reading | kind | prediction |
|---|---|---|---|---|
| I1 | 8-bit weight (or weight-activation) quantisation against 16-bit | A1′: the resolvable step is coarser than 16 bits | CLASS | + |
| I2a | 4-bit weight-only quantisation against 16-bit | A1′ | CLASS | + |
| I2b | quantisation at 3 bits or fewer against 16-bit | A1′: below the resolvable step, content is lost | COMPARATIVE | 0 (quality BEHIND) |
| I3 | distillation: a small student trained on the teacher's outputs, against the same student trained on labels only | A6: regenerate from the settled past's own content (its output distribution), as for logit replay (CL M4) | CLASS | q+ |
| I4 | speculative decoding against plain autoregressive decoding | A7/A8: proposals about the future are accepted only once verified, that is, settled | INHERITED | = |
| I5 | KV or prefix caching against recomputation | A6/A7: reuse the settled past; do not regenerate it | INHERITED | = |
| I6 | early exit or adaptive depth (CALM, LayerSkip, mixture-of-depths) against full depth | D2: compute follows the arc of change, not the count of tokens | CLASS | + |
| I7 | controlling reasoning length (budgets, early stopping of a chain of thought, penalties on overthinking) against unrestricted reasoning | D2 + A3: end the occasion when its arc has settled | CLASS | + (cost = tokens) |
| I8 | model cascades or routing (a small model first, a large one when needed) against always the large model | D2 / A1′: spend in proportion to the content of the query | CLASS | + |
| I9 | serving systems: continuous batching, paged attention | none (systems engineering) | — | S |
| I10 | GPU power capping or frequency scaling | none (hardware physics) | — | S |
| I11 | carbon- or price-aware shifting and pausing of training jobs, on energy | Proposition 7: a lossless pause moves energy in time and does not reduce it | COMPARATIVE | 0 on energy (carbon is reported, not graded) |
| I12 | pruning to 50 % sparsity (SparseGPT, Wanda) against dense | none specific | — | S |

## The grading rule (fixed now; applied by `checks/retro_energy.py`)

**What a row is.**
- A quoted pair (X, Y), with quality and cost where the paper reports both, and the setting named.
- Rows come from the dossiers. Each number must appear in a verbatim quote (the CL battery's convention,
  `CL Design Principle/checks/ablation_rows.py`).

**How a mechanism is graded.**
- **AGREES:** every graded row agrees.
- **DISAGREES:** no row agrees.
- **MIXED:** otherwise.
- **NOT REPORTED:** no quoted row exists.

**Rows that are not graded.**
- A row with only one of quality or cost is recorded. It is graded only for the codes that need only that quantity
  (q+, q−, 0-difference).
- A cost-only row is listed, not graded.

**The kinds.** Grades are read as kind × outcome (CLAUDE.md §7). An AGREES on an INHERITED row says that the method's own
theorem holds, not that CRR adds anything.

## How the results feed the design (fixed now)

1. **AGREES, and the mechanism saves energy:** it is a candidate for the energy tests (ENERGY1), where it can be run on
   this repository's CPU setting.
2. **DISAGREES, and the mechanism saves in the published rows:** examine why in CRR's terms. Record the correction, or
   label the mechanism non-CRR engineering.
3. **It does not save in the published rows:** exclude it, whatever CRR predicted.
4. **Candidates that meet the continual-learning record are tested first:**
   - E2a (SEC against a sweep);
   - E5 (continual update against retraining from scratch);
   - E8 (the slow model);
   - E13 and I11 (the empty cut);
   - E9 (a horizon-free schedule).

   They are tested in the SOTA1 setting (Split-CIFAR-100, reduced ResNet-18, CPU) after SOTA1 has run.
5. **The measurement is honest about the machine.**
   - This container exposes no energy counter (no RAPL), so ENERGY1 measures counted work: forward and backward passes,
     multiply-accumulates, and wall time at fixed threads.
   - Any conversion to joules uses a named power assumption, stated beside the figure.
