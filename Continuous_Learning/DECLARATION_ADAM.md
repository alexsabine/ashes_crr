# Declaration — the Adam checks and the prior-art comparison (committed and pushed before the first full run)

Owner request, prompt-log entry 104. The anchor is the push timestamp of the commit that adds this file. The script is
`Continuous_Learning/checks/adam_checks.py`. Its docstring holds the design, and every label is computed from the numbers
(R15). The model is synthetic, so this is a mechanism check at rung R4 (declared on a synthetic world). It is not a ledger
row.

**What was seen before this commit (stated so the auditor can weigh it).** Two short smoke runs (300 steps, one seed, the
module constants overridden in a scratch script) were used to check that the code runs. The first smoke run's output was not
read. The second was read, and it showed the following:
- A1, A2, A3, A5, A6a, A6b, A7 and A8 hold at 300 steps.
- A4 fails at 300 steps, at the most extreme scale (c = 256). There the SGD rule is finite but behind the SGD-tuned fixed
  weight, because 300 steps is too short for either arm to converge.

A8 (momentum) was written before the second smoke run. No criterion, threshold or constant was changed after either smoke
run. The full run (4000 steps, 5 seeds) decides every item as written.

## What is tested, what is expected, and what each outcome means

The setting is the two-task quadratic of `theory/checks/omega_sweeps.py`. The past term's curvature is scaled by c ∈
{1/16, 1, 16, 256}, which stands for the "units" of a past loss that no one chose. The score is the total loss L_p + L_q.

- **A1. Adam is invariant to rescaling the whole gradient.**
  - Expected: holds. This is Kingma and Ba's property, and a failure means a bug.
  - Meaning: it establishes the fact the rest builds on. Adam's update does not see the gradient's overall size.
- **A2. The stability edge exists under SGD and not under coupled Adam.**
  - The SGD edge is λ* = (2/η − h_max)/f_max. It moves as 1/c and crosses λ = 1 across the scales. Under coupled Adam (the
    past pull inside the preconditioner) no λ on the grid diverges.
  - Expected: holds.
  - Meaning: under SGD, a fixed weight chosen in one set of units can diverge in another. Under Adam it cannot.
- **A3. Under coupled Adam, the fixed λ tuned at c = 1 stays within 10 % of the Adam-tuned fixed weight at every c.**
  - Expected: holds. It repeats `omega_reprocessed.txt` [6] over four scales instead of two.
  - Meaning: under Adam the fixed weight is already scale-robust. The rule has no scale advantage to offer there.
- **A4. Under SGD, the rule's advantage appears exactly where the edge is below λ = 1.**
  - The rule's advantage is its total at least 10 % below the SGD-tuned fixed weight's. It must appear exactly at the scales
    whose edge is below λ = 1, and nowhere else.
  - Expected: open. The smoke run failed at c = 256.
  - If it holds: the rule's SGD advantage is the stability edge, and nothing else.
  - If it fails at c = 256: the rule survives an extreme mismatch but does not win there within 4000 steps. The rule is
    finite at every scale, but it is not a free lunch. The document must say so.
- **A5. Decoupled application (AdamW-style).**
  - The setup: the present gradient goes through Adam and the past pull is applied outside it with step 0.05.
  - The prediction: the edge returns for the fixed weight at some scale, and the decoupled rule (the ratio of the applied
    present step to the past pull) is finite at every scale.
  - Expected: holds.
  - Meaning: the rule has work to do under Adam only when the past term is applied outside the preconditioner, as AdamW
    applies weight decay (Loshchilov and Hutter). That is the one Adam configuration where a patent's technical effect could
    stand.
- **A6a. Under Adam, the poisoned rule stays within 2× of its clean total.** Five present batches are multiplied by 1000.
  - Expected: holds.
  - Meaning: Adam's second-moment estimate absorbs the poison. It does so as a single-step outlier would be absorbed, with no
    clip needed.
- **A6b. Under Adam, EQ-B and the rule are within 10 % of each other under poison.**
  - Expected: holds.
  - Meaning: EQ-B's clip, the enhancement tested in EQ4, is redundant under Adam.
- **A7. The gradient-ratio family is finite at every scale under SGD.** The family is the rule, a VQGAN-style ratio
  (instantaneous norms, additive δ = 1e-4) and a max/mean ratio with the weight smoothed.
  - Expected: holds.
  - Meaning: the step bound is a property of the gradient-ratio family, which is prior art (Esser, Rombach and Ommer's VQGAN
    adaptive weight; loss balancing in physics-informed networks). It is not a property of the rule alone. The rule's
    distinguishing choices are three: the EMA of gradient vectors, the ratio on the whole parameter vector, and the use for
    a past term in continual learning. What differs between the members is their totals, not their finiteness.
- **A8. Heavy-ball momentum** (β = 0.9, step 0.05 × (1 − β)).
  - The prediction: Polyak's quadratic edge λ* = (2(1 + β)/η_m − h_max)/f_max predicts exactly which grid points diverge,
    at every scale. Some scale has a divergent grid point, and the rule is finite at every scale.
  - Expected: holds.
  - Meaning: the rule's advantage belongs to the step-size family (plain SGD and momentum SGD), the optimisers of most
    vision training. It does not belong to the adaptive-moment family (Adam, AdamW with the past term inside), the
    optimisers of most language-model training.

## What the results change

- **If A1–A3 and A6–A7 hold**, the continual-learning write-up states the rule's scope as follows:
  - a stability guarantee for SGD-family training;
  - a candidate for decoupled application under Adam (A5);
  - nothing under coupled Adam;
  - a member of a prior-art family, distinguished by its smoothing and its use, not by its bound.
- **Any failure of A1–A3** is reported as a failure of the mathematics or the code, and investigated before any document
  uses the checks.
- **A4's outcome is reported as it falls.**

## Pipeline-level work in the same commit (not declared here, recorded for the auditor)

Study EQ4 was hashed on 2026-09-22 (`prereg/eq4/`) and its data step was taken on 2026-09-23 under R3. It is scored as
committed:
- the ledger has rows EQ4-0 to EQ4-I;
- `runs/eq4/score.txt` holds the scoring output;
- `runs/eq4/rerun_*_{a,b}.json` holds the reruns, byte-identical;
- AGENT_LOG entry 82 covers the satimage/294 overlap and the exclusions-path defect.
