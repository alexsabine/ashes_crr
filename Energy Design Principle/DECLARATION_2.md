# Declaration 2: a synthetic check of the own-clock cut, and a consolidated estimate with fair forecasts

**Status.**
- **The request.** Owner request: prompt-log entry 200.
- **When it was pushed.** Before `checks/clock_cut.py` and `checks/consolidated_estimate.py` exist.
- **What it is.** A declared synthetic battery (rung R4 at most) and a scenario model. It opens no data, and it is a note,
  not evidence (R8).
- **The labels are computed by the scripts** (R15).

## Part A — the check: does a cut on content beat a cut on the clock?

**The observation being checked.** It is post hoc: `RETRODICTION.md` point 8, FINDINGS 6.
- Fixed exits and forced token budgets were behind.
- Exits that verify, and stops at the first correct answer, held.
- D2 reads this as a cut on the system's own clock (when the belief has settled) against a cut on the step clock (after
  a fixed number of steps).

**The known result it must be separated from.** A sequential test that stops on the evidence needs fewer samples than a
fixed-sample test at the same error rates. The sequential probability ratio test (SPRT) is "later proven to be optimal by
Wald and Jacob Wolfowitz". This is quoted from the Wikipedia article *Sequential probability ratio test*, fetched
2026-09-25; the Project Euclid page of Wald & Wolfowitz 1948 returned no text to the proxy.
- **So "content beats the clock" is inherited from sequential analysis.** On this check it can be at most
  REDUNDANT-DOMAIN.
- **The CRR-proper question is narrower.** Does stopping when the *arc* has settled (D2 + A3 + A1′) beat stopping on
  confidence (the SPRT's own statistic) and stopping on answer stability (the "first correct" and consistency methods of
  the literature)?

### The world

**Items.** Each item is a sequence of observations about a hidden class c ∈ {0, 1, 2, 3}.
- **Class means:** μ_k = k.
- **Observations:** x_t = μ_c + σ_i ε_t, with ε_t standard normal.
- **The agent** updates an exact Bayesian posterior over the four classes, using the item's true σ_i (except where a world
  says otherwise).
- **T_max = 256** steps.

**Worlds.**
- **W0, the null: fixed timing.** Every item is uninformative until step 32 (σ = 10⁶) and then fully informative from step
  32 on (σ = 0.05). The evidence arrives at the same step for every item, so a fixed budget of 32 is as good as any
  content rule. **No content rule may be BETTER than the tuned budget here.**
- **W1, homogeneous:** σ_i = 2 for every item. The SPRT is optimal. Content rules should beat the tuned budget (Wald), and
  the confidence rule should be best.
- **W2, heterogeneous:** σ_i log-uniform on [0.5, 4]. Items differ in how long they need.
- **W3, overthinking:** as W2, but evidence goes bad after each item's settle step τ_i, drawn geometric with mean 24.
  After τ_i, each observation is, with probability 0.3, drawn from a random wrong class's mean; the agent's model does not
  know this. Running to T_max can lower accuracy.

**Sizes.** Per world and seed: 4000 calibration items and 4000 test items, independent. Seeds are 0–4.

### The stopping rules (arms)

At the stop, the decision is the argmax of the posterior.

| arm | rule | tuned on calibration |
|---|---|---|
| S0 | run to T_max | — |
| S1a | a fixed default budget, T = 16 steps (the "forced budget") | no |
| S1b | a fixed budget, the cheapest T ∈ {1, …, 256} meeting the target | T |
| S2 | confidence: stop when max posterior ≥ c (the SPRT's statistic) | c |
| S3 | **the own-clock cut (CRR):** stop at the first step where two conditions hold. The Fisher–Rao length of the last w posterior steps is each below θ (step length 2·arccos Σ√(p_t p_{t−1})), **and** the arc travelled since the start is at least a_min | θ |
| S4 | answer stability: stop when the argmax has been unchanged for w_s steps | w_s |

**Named constants.**
- S3 uses w = 4 and a_min = 1.0472, half the Fisher–Rao distance from the uniform belief to a vertex, 2·arccos(1/2) / 2.
  a_min is CRR's A1′ reading: a settled past must have content, not merely stillness.
- **The sensitivity table** re-runs W2 and W3 with w ∈ {2, 4, 8} × a_min ∈ {0, 0.5236, 1.0472}. Nine cells; a label that
  flips in more than one cell is FRAGILE.

**Tuning (the same for every tuned arm).**
- **The target** is S0's calibration accuracy minus 1.0 point.
- **The chosen parameter** is the cheapest (lowest mean steps) that meets the target on calibration. If none meets it,
  the most accurate is chosen.
- **Grids:**
  - c ∈ {0.5, 0.55, …, 0.95} ∪ {0.97, 0.98, 0.99, 0.995, 0.999, 0.9999};
  - θ ∈ 30 values log-spaced from 10⁻⁴ to 1;
  - w_s ∈ {1, …, 64};
  - T ∈ {1, …, 256}.

### Labels (per seed, on test items, paired)

**The two quantities.**
- **Cost:** the ratio of mean steps, X / Y. SAVES ≤ 0.90, COSTS ≥ 1.10, SAME otherwise (DECLARATION_1).
- **Quality:** the accuracy difference, X − Y. The step is max(1.0 point, 2 × the paired standard error). AHEAD, BEHIND
  or NOT BEHIND by the step.

**X against Y:**
- **BETTER:** (SAVES and not BEHIND) or (not COSTS and AHEAD);
- **WORSE:** (COSTS and not AHEAD) or (not SAVES and BEHIND);
- **TRADE-OFF:** SAVES and BEHIND, or COSTS and AHEAD;
- **TIE:** otherwise.

**Across seeds.** The label that occurs in at least 4 of 5 seeds; otherwise MIXED.

### The gate and the predictions (fixed now)

| id | comparison | world | required / predicted | role |
|---|---|---|---|---|
| G1 | S2 against S1b | W1 and W2 | BETTER in both | positive control (Wald): if not, the instrument cannot see content stopping; **gate closed** |
| G2 | each of S2, S3, S4 against S1b | W0 | none BETTER | null control: a content rule BETTER where timing is fixed is an artefact; **gate closed** |
| G3 | S1a against S0 | W2 | TRADE-OFF (saves, behind) | the literature's failing rows: a forced budget loses quality |
| F1 | S3 against S1b | W1, W2, W3 | BETTER | the post-hoc observation (content beats the clock); if it holds, it is **REDUNDANT-DOMAIN** (Wald) |
| C1 | S3 against S2 | W1 | not BETTER | must-fail for the CRR-proper claim: nothing beats the optimal SPRT in its own world; if S3 is BETTER, it is an artefact |
| C2 | S3 against S2 | W2, W3 | **forecast: TIE** (the arc is a function of successive posteriors, as the confidence rule is) | CRR-proper: BETTER in W3 but not W1 would be a PROSPECTIVE CANDIDATE, to be declared on real data |
| C3 | S3 against S4 | W2, W3 | forecast: TIE or BETTER | CRR-proper, report |
| O1 | S3, S2 and S4 against S0 | W3 | forecast: BETTER (stopping before the evidence goes bad) | report: the "overthinking" rows |

If G1 or G2 fails, stop (R12). The gate is written first in the output, and nothing after it is read as a result.

## Part B — the consolidated estimate (a scenario, conditional on the method holding)

**The question.** What would a CRR-informed economy of continual learning, AI safety and compute save in energy?

**The answer's form.** Five terms for 2030, each factor sourced or named as an assumption:
- the **technical potential** of the mechanisms the lens endorses;
- the part **attributable to CRR** (or to the CRR programme);
- a probability-weighted figure.

**Inputs pinned elsewhere:**
- E_AI(2030) = 300.47 TWh, and f_dev (0.30 / 0.40 / 0.7143), from `Compute_Savings/checks/scale_estimate.txt`;
- the SEC term's low, middle and high values, from the same file;
- the cost ratios of the graded rows, from `checks/retro_energy.txt`.

| term | model | factors | attributable to |
|---|---|---|---|
| T1 SEC on penalty-weight sweeps | from `scale_estimate.txt` | as pinned | the CRR programme (SEC is a product of it; the ledger says "not a CRR rule") |
| T2 continual updating instead of periodic retraining | E_AI × f_dev × f_final × f_refresh × s_cl | f_final, the share of development-and-training energy that is final runs: 0.10 (Epoch, 0.5 of 5) to 0.6655 (Morrison, 913 of 1,372 MWh). f_refresh ASSUMED 0.1–0.5. s_cl = 1 − 0.5000 (the continual pre-training rows) | none: continual pre-training is published (Ibrahim et al.) |
| T3 content-based stopping of reasoning | E_AI × (1 − f_dev) × f_reason × s_stop | f_reason, the share of inference energy spent on reasoning tokens: ASSUMED 0.1–0.5. s_stop from the not-behind I7 rows: 1 − 0.5526 to 1 − 0.2861 | CRR only if C2 finds the arc rule BETTER than confidence; otherwise none (Wald; the published methods) |
| T4 the safe pause (the empty cut) | 0 TWh | energy is moved, not saved. Carbon is reported from the quoted row (1.38 against 11.4 kgCO2) | — |
| T5 horizon-free schedules for multi-horizon sweeps | E_AI × f_dev × f_scaling × s_wsd | f_scaling ASSUMED 0.01–0.1; s_wsd = 1 − 0.4222 | none: WSD is published |

**Cases.** Low, middle and high as in `scale_estimate.py`: ends of every band, or the middle f_dev with the geometric means
of assumed bands.

**Not modelled.** Overlaps between terms, and rebound: cheaper compute buys more compute.
- The printed sum is an **upper bound on the sum of the terms**, not a forecast of net energy.
- Rebound is named and not quantified. No source fetched on the day quantifies it for AI.

## Part C — fair forecasts, recorded now, scored later by ENERGY1 and SOTA1

These are the investigator's own probabilities. They are printed by `consolidated_estimate.py` so that they exist as
numbers (R1). They are **forecasts, not results**, and they will be scored against ENERGY1's and SOTA1's rows when those
exist.

| id | event (in the SOTA1 setting unless stated) | P |
|---|---|---|
| P1 | SEC against the tuned sweep on SOTA1's learner: accepted without losing a step, saving ≥ 80 % of the sweep | 0.45 |
| P2 | a continual learner reaches ≥ 95 % of retraining-from-scratch accuracy at ≤ 0.5 of its compute on online Split-CIFAR-100 | 0.10 |
| P3 | a horizon-free schedule is not behind cosine in the stream | 0.60 |
| P4 | shrink-and-perturb at task boundaries saves ≥ 10 % of work to a target | 0.30 |
| P5 | the arc cut is BETTER than the confidence cut on real data | 0.10 |
| P6 | the empty cut changes energy by 0 and leaves the run bitwise identical | 0.95 |
| P7 | SOTA1-1a: CRR-SCL is AHEAD of the best baseline | 0.35 |
| P8 | SEC's saving survives at LLM scale under AdamW (not testable here without money) | 0.15 |
