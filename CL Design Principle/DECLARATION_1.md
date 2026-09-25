# Declaration 1: CRR's predictions for the mechanisms of state-of-the-art continual-learning methods

**Status.**
- **The request.** Owner request: prompt-log entry 191. Written on 2026-09-25.
- **When it was pushed.** Before any of the three source dossiers (`docs/citations/cl_sota_*_2026-09-25.md`) was opened by
  the investigator. The dossiers are being fetched in parallel by research agents, who were told not to report any
  mechanism or ablation content back.
- **What it is.** A retrodictive battery, not a ledger study. It opens no data.

**Honesty clause.** The investigator's training exposure includes much of this literature, so the predictions below
cannot be blind. What the declaration fixes is this:
- **the CRR reading of each mechanism,** named by axiom;
- **the direction CRR implies for that mechanism's ablation;**
- **the rule that grades it.**

Every label is computed by `checks/retro_sota.py` from quoted numbers (R15), and every disagreement is examined, not
explained away. Grades are read as kind × outcome, as for the retrodiction batteries (CLAUDE.md §7).

## The CRR ingredients used

- **A1:** the Fisher metric, distance as distinguishability. It is information geometry's, not CRR's.
- **A1′:** the system's own unit.
- **D2 / D6:** the arc on the learner's own clock (natural time).
- **A3:** the cut. It has no duration and no content. It separates the settled past from the open future and orients the
  next occasion.
- **A6:** the next occasion is seeded from the settled past's *content*, as a Fréchet mean under maximum-entropy weights,
  at bounded strength (a reweighting, never an accumulated count).
- **P2 / P3:** surplus and age weights (Jaynes; CRR fixes neither β nor q).
- **A7:** nothing is fed by a future.
- **A8:** the future has no content.
- **H-EQ:** equal pull between the settled past and the present. It reduces to a constant on replay (EQX). The Adam_SGD
  finding is that it is strong where the balanced scale is an artefact and weak where the scale carries information.
- **Proposition 7:** the empty cut.

## The mechanisms and CRR's prediction for each

**Setting.** All predictions are for class-incremental accuracy with a memory buffer on CIFAR-100, or CIFAR-10 where the
paper reports no CIFAR-100 ablation.

**Prediction codes:**
- **+** removing the mechanism lowers accuracy by at least one step;
- **0** removing it changes accuracy by less than one step;
- **−** removing it raises accuracy;
- **S** CRR is silent, and the row is not graded.

| id | mechanism (where published) | CRR reading | kind | prediction |
|---|---|---|---|---|
| M1 | a replay buffer at all (ER against fine-tuning) | A7 + A6: the future is fed only by settled past content | CLASS | + |
| M2 | class-balanced storage against reservoir sampling (GDumb's greedy balancer; balanced variants) | H-EQ across the settled past's classes: each class exerts equal pull | COMPARATIVE | + |
| M3 | retrieval by interference, gradient diversity or value (MIR, GSS, ASER) against random retrieval | P2 salience weighting. The repository's SAL gate closed (no positive control), and surplus-weighted sampling tied (C7) | COMPARATIVE | 0 |
| M4 | logit replay: distilling the logits stored at insertion (DER against ER) | A6: regenerate from the settled past's own *content* (its output distribution), in the Fisher geometry of outputs (D6: KL) | CLASS | + |
| M5 | label replay added to logit replay (DER++ against DER) | A6 with the label as a second content of the same occasion | COMPARATIVE | 0 |
| M6a | updating the stored logits of classes that arrived after storage (X-DER's past-logit update) | A8: at storage those logits had no content (the future is empty). Filling them once the classes are past is A7-consistent | COMPARATIVE | + |
| M6b | preparing heads for future classes (X-DER's future preparation) | A8: the future has no content, so training for it cannot help | COMPARATIVE | 0 |
| M7 | the asymmetric loss: the incoming batch competes only among its own classes (ER-ACE; separated softmax, SS-IL) | A3: the cut orients the new occasion without writing into the settled past. The present's gradient should not push the past's heads down | CLASS | + |
| M8 | distillation on current data with no memory (LwF), against replay | A6 needs the settled past's content. LwF supplies the past model, not the past's data | COMPARATIVE | LwF far below replay (graded as: replay − LwF ≥ one step) |
| M9 | nearest-class-mean classification on stored exemplars (iCaRL NCM; prototype methods) against the trained softmax head | A6: the Fréchet mean of the settled past's contents is the regenerated state | CLASS | + |
| M10 | output bias correction (BiC; WA weight aligning; LUCIR cosine normalisation) | H-EQ at the head: equal pull between old and new classes. The recency bias in head norms is an artefact of arrival order, not information, which is where equal pull was strong (`Adam_SGD`) | COMPARATIVE | + |
| M11 | a slow model: an exponential moving average of the weights (CLS-ER's stable model; momentum distillation) | A6 + P3: regeneration from the settled past with geometric age weights | CLASS | + |
| M11b | Fisher-weighted over plain averaging (CoFiMA against uniform averaging) | A1 over Euclidean. The record: the Fisher metric made no difference (EQX) | COMPARATIVE | 0 |
| M12 | a parameter-space anchor alone (EWC, online EWC, SI, MAS) in the class-incremental setting, against fine-tuning | A6 in parameter space. The record: regularisers sit near the class-incremental floor | INHERITED | 0 (class-incremental); task-incremental S |
| M13 | gradient projection (GEM, A-GEM) against ER at equal memory | H-EQ says equal pull, not a veto on the past's side. A projection is a constraint, not a balance | COMPARATIVE | ER ≥ A-GEM by at least one step |
| M14 | retraining from scratch on the balanced buffer (GDumb) against online ER-type methods | A3 + A6: full regeneration from the settled past at each cut | COMPARATIVE | not behind ER by more than one step |
| M15 | contrastive or mutual-information representation objectives (SCR, OCM, OnPro, Co2L, GSA) | A1 names distinguishability, but prescribes no objective | — | S |
| M16 | data augmentation, repeated iterations per batch, and other "tricks" | none | — | S |
| M17 | plasticity repairs (L2 toward the initialisation, shrink-and-perturb, ReDo, continual backprop) on long streams | A6 with the first occasion as the anchor (L2-init). The settled beginning regenerates plasticity | CLASS | + (loss-of-plasticity settings) |
| M18 | replay scheduled on model time against step-based scheduling (FOREVER) | D2 / A1′: the model's own clock. This repository's miniature found a TIE (C1, C2) | COMPARATIVE | + |

## The grading rule (fixed now; applied by `checks/retro_sota.py`)

**What is graded.**
- **Every reported ablation row is graded separately.** An ablation row is a quoted pair of numbers:
  - with and without the mechanism;
  - or the two methods M1–M18 compare.
- **Effect.** The effect is the difference in class-incremental accuracy points.
- **The resolvable step.** It is max(1.0 point, twice the larger reported standard deviation of the pair). Where no
  deviation is reported, it is 1.0.

**How a row's effect is labelled.**
- **Helps:** effect ≥ step.
- **No effect:** |effect| < step.
- **Hurts:** effect ≤ −step.

**How a row's outcome is set.**
- **AGREES** when the effect label matches the prediction (+ ↔ helps, 0 ↔ no effect, − ↔ hurts; comparative predictions
  as stated in the table).
- **DISAGREES** otherwise.

**How a mechanism's outcome is set.**
- **AGREES:** every graded row agrees.
- **DISAGREES:** none agrees.
- **MIXED:** otherwise.
- **NOT REPORTED:** no quoted ablation exists.
- **S rows** are listed and not graded.

**The setting preference.** Class-incremental CIFAR-100 with a buffer. Online and offline settings are both graded, each
labelled. CIFAR-10 is used only where CIFAR-100 is absent, and is labelled.

## How the results feed the design (fixed now)

1. **AGREES, and the mechanism helps:** integrate it into the CRR safe continual learner, citing its source.
2. **DISAGREES, and the mechanism helps in the published ablation:** examine why in CRR's terms.
   - If a stated CRR reading explains it once corrected (for example, a misread axiom), record the correction as a
     finding and integrate the mechanism.
   - If no CRR reading explains it, integrate it only as **non-CRR engineering**, labelled so. This is the owner's
     "integrate what fails as appropriate".
3. **The mechanism does not help in the published ablations:** exclude it, whatever CRR predicted.
4. **S, and it helps:** include it only as labelled engineering needed for competitiveness, with its ablation arm in
   SOTA1.
5. **The empty cut** (Proposition 7; E1–E3) wraps the whole learner. Its state checklist lists every component the design
   adds.
6. **Each component integrated gets an ablation arm in SOTA1 (the leave-one-out ablation).** SOTA1 then scores CRR's
   predictions for those components on unseen data.
