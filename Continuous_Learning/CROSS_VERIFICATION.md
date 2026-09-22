# Cross-verification of the Ω = 1 rule against existing catastrophic-forgetting solutions (2026-09-22)

Owner request (prompt-log entry 73): reference 2026 papers and cross-verify the rule against existing solutions,
paper by paper. This document is a note, not evidence (R8). Every number in it is printed by a committed script
whose output is pinned: `theory/checks/omega_vs_methods.txt` (the battery of this note), `theory/checks/omega_sweeps.txt`
(the mathematics), `runs/eq3/score.txt` (study EQ3). The literature record with the access statement is
`docs/citations/continual_learning_2026-09-22.md`: every full-text host was blocked from the execution environment on
the day, so the 2026 preprints are known from search-engine renderings of their abstracts **[S]** and are unverified
against the source; the five journal records marked **[PubMed]** were read on PubMed. A paper is cross-referenced
here on what its abstract states it does; where that is not enough to decide the relation, the note says so.

## 1. The rule, and the four questions asked of every method

The rule under test (CRR H-EQ; `Continuous_Learning/CONTINUOUS_LEARNING.md` §3) multiplies a fixed past term by

$$w = \Omega \, \|\hat g_p\| / \|\hat g_q\|, \qquad \Omega = 1,$$

where ĝ_p, ĝ_q are exponential moving averages (smoothing 0.9) of the present-task and past-term gradients, w is
capped at 10⁴ and the denominator floored at 10⁻¹². The update is θ ← θ − η(g_p + w g_q). Four properties decide
how any other method relates to it, and each is answered from the pinned outputs, not from the papers' claims:

1. **What sets the past weight.** A hand-set constant, sample counts (Bayes), a target, a learned weight, a loss
   ratio, or a gradient length; or no weight at all (projection).
2. **Whether the weight carries units.** A constant λ on an EWC penalty has the units of (present loss)/(past
   penalty); when the past curvature changes scale the same λ is a different weight. The ratio of two gradient
   norms is dimensionless in that scale.
3. **Whether the step is bounded by the present step.** Under the rule, ‖g_p + w g_q‖ ≤ (1 + Ω)‖g_p‖ at the
   smoothed gradients (§4.4 of the document), so the past term cannot drive the step past a fixed weight's
   stability edge. A fixed weight has no such bound.
4. **Whether it has a natural value.** Ω = 1 is a plateau, not an optimum (EQ3-P: 9 of 9 grid points within a step
   of the best on fars, krkopt, led24 and mfeat_factors, 7 of 9 on led7 and mfeat_morphological); the Bayes weight is n_q/n_p and is 1 only at equal
   counts (`omega_sweeps.txt` [1]).

## 2. The battery: every rule on one model where each can be run exactly

`theory/checks/omega_vs_methods.py` reduces each method's rule to the two-task quadratic of the mathematics check
(five parameters; present Hessian H; past penalty with Fisher F sixteen times a second random diagonal; the learner
starts at the old-task optimum; Gaussian mini-batch noise of standard deviation 0.5 on both gradients; learning rate
0.05; 4000 steps; five seeds). Each method runs with one knob setting; then the past curvature is multiplied by 16
with the same knob (does the rule survive a change of scale without retuning?); then its own knob is multiplied by 10
(does it have a divergence edge?). Quality is the total loss L_present + L_past against the best fixed weight on the
same scale, tuned **in sample** on a ten-point grid, which favours the baseline (R7). Every label is computed from
the numbers (R15).

| method (paper's rule, reduced) | knob | L_present | L_past | total | /tuned | 16F: /tuned | knob × 10 | computed label |
|---|---|---|---|---|---|---|---|---|
| fixed weight (EWC / L2-SP / KL penalty) | λ = 1 | 3.1169 | 0.1999 | 3.3168 | 1.000 | ∞ (diverges) | DIVERGES | not scale-robust; has a divergence edge in its knob |
| **the rule** | Ω = 1 | 2.8203 | 0.6585 | 3.4789 | 1.049 | 0.660 | finite | **scale-robust**; no edge found at knob × 10 |
| learned task weights (GradNorm α = 0) | — | 2.8010 | 0.7296 | 3.5306 | 1.064 | ∞ (diverges) | n/a | not scale-robust; no knob |
| loss ratio (MEGA-I) | — | 2.6479 | 1.0830 | 3.7309 | 1.125 | ∞ (diverges) | n/a | not scale-robust; no knob |
| conflict projection (A-GEM) | — | 0.2066 | 40.1317 | 40.3382 | 12.162 | 43.384 | n/a | not scale-robust; no knob |
| soft conflict projection (PCR-style) | c = 0.5 | 0.0215 | 65.2291 | 65.2506 | 19.672 | 70.843 | finite | not scale-robust; no edge found |
| protected subspace, no past term (OGD / OGPSA / SafeAnchor-style) | k = 2 | 2.9920 | 15.7519 | 18.7439 | 5.651 | 17.313 | finite | not scale-robust; no edge found |
| target controller on the past loss (adaptive-KL-style) | target 1 | 2.6652 | 1.0382 | 3.7035 | 1.117 | ∞ (diverges) | finite | not scale-robust; no edge found |
| gradient-based sample selection at fixed λ = 1 | q = 0.8 | 3.1797 | 0.1855 | 3.3652 | 1.015 | ∞ (diverges) | n/a | not scale-robust; no knob |

Stability edge of a fixed weight: λ* = 1.2575 at F and 0.0786 at 16F; the tuned fixed weight is λ = 1
(total 3.3168) at F and λ = 0.03 (total 14.7298) at 16F. Computed summary lines (verbatim from the pinned output):

- scale-robust methods (within 10 % of the tuned fixed weight at both F and 16F with one knob setting): `['omega']`
- methods that diverge at 16F with the knob that worked at F: `['fixed', 'gradnorm', 'mega', 'klctrl', 'select']`
- methods that forget (L_past more than 10 × the tuned fixed weight's 0.1999) at F: `['agem', 'softproj', 'subspace']`
- methods with a divergence edge in their own knob: `['fixed']`

**What the battery does and does not show.** It shows that, on a model where the past term's units can be changed
at will, the one rule whose quality survives the change is the one that scales the past pull by the present pull.
It does not show that the rule is the best method: at the original scale the tuned fixed weight is better on the
total (3.3168 vs 3.4789) and much better on the past (0.1999 against the rule's 0.6585), GradNorm at α = 0 is at ratio 1.064 to the tuned
weight against the rule's 1.049, and gradient-based sample selection at λ = 1 is at ratio 1.015. The methods are the author's reductions of each paper's rule to
this model, not the papers' code; the learned-weight and controller rules start from a weight of 1, already above the edge
λ* = 0.0786 at 16F, and the loss-ratio rule's weight is a ratio of losses, which for the same displacement is sixteen
times larger at 16F; they diverge there for that reason, so "diverges at 16F"
means "carries units", not "is a bad method". The projection rules never diverge and never will: they have no past
weight; what they lose is the past wherever the two gradients do not conflict, which on this model is most of the
time. The 16F test is the gate's Fisher-scale mismatch pushed one step further and is the reason the rule was
proposed; a method whose paper says it retunes per dataset is not wrong to fail it.

> Nine different ways of deciding how hard to pull back toward the old task were tried on the same small problem.
> Then the old task's pull was secretly made sixteen times stronger without telling any of them. Most of the
> methods that use a number to set the pull blew up, because their number was now the wrong size. The methods that
> only push sideways never blew up, but they forgot most of the old task. The rule that measures the two pulls and
> keeps them the same length was the one that kept working. It was not the best on the original problem: the
> hand-tuned number beat it there, and remembered the old task three times better.

## 3. Paper by paper

For each paper: what its abstract states it does; how it sets the past weight (question 1); which battery row it
maps to and what that row says; the relation to the rule; and the fair test that would decide the relation on the
paper's own setting. "Same class" means the rule could be applied to the paper's past term as a multiplier; "orthogonal"
means the paper changes something the rule does not touch and the two compose; "competing" means the paper's
mechanism replaces the weight. Nothing below is a result about the paper.

### 3.1 Regularisation-based methods (the rule's own family)

**Liu et al., Elastic Weight Consolidation Done Right, arXiv:2603.18596, CVPR 2026 [S].** Replaces the Fisher
importance estimate (which the abstract says produces "gradient vanishing and inaccurate importance estimation in
certain scenarios") by a Logits Reversal estimate, EWC-DR. Past weight: a fixed λ on the importance-weighted
quadratic; the paper changes the importance matrix, not the weight. Battery row: fixed weight. Relation: **same
class, orthogonal change**. The rule multiplies whatever quadratic penalty is supplied; an EWC-DR penalty is a
different F with different units, which is exactly the situation the 16F test models. The fair test is the EQ3
design (Ω = 1 vs the tuned λ, per carrier, not-behind within one resolvable step) with EWC-DR's importance in
place of the empirical Fisher, under the paper's own reported λ sweep as the baseline. What the paper says about
Fisher estimation bears on the study, not the rule: `van de Ven, arXiv:2502.11756` below makes the same point,
and EQ3's Fisher is the diagonal empirical Fisher on the task's training data at the task boundary
(`runs/eq3/frozen/eq3_score.py`), one of the several implementations that paper says are reported without
description. CRR processing: none; H-EQ names the past term's Fisher as A1's metric and does not fix its estimator,
which is a registered parameter (R5) and stays one.

**Yao et al. (as displayed), Revisiting Weight Regularization for Low-Rank Continual Learning, arXiv:2602.17559,
ICLR 2026 [S].** EWC applied to a shared low-rank (LoRA) update, with importance estimated in the full space from
the low-rank representation. Past weight: fixed λ on the EWC term. Battery row: fixed weight. Relation: **same
class**; the rule applies unchanged to the low-rank parameters (the gradient norms are taken over the LoRA
factors). This is the most direct place a GPU test of the rule at LLM scale could be run: EWC-LoRA's λ sweep is the
tuned-λ baseline the EQ3 rows compare against, and the paper's stability–plasticity curve is the Pareto curve of
§4.2, on which the rule's fixed points lie at every λ. The open question the paper cannot answer from its abstract
is whether its tuned λ sits at the stability edge, which is where the rule won on tabular carriers (Figure 8 of the
document) and the only place the battery gives it an advantage.

**Sliwa, Schneider, Hennig, Hernández-Lobato, Mitigating Forgetting in Low Rank Adaptation (LaLoRA),
arXiv:2512.17720 [S].** A Laplace approximation to LoRA that constrains updates in high-curvature directions. Past
weight: the Laplace posterior precision, i.e. **the Bayes weight** (sample-count-weighted curvature) of §4.3 with
no free λ. Battery row: fixed weight at the Bayes value (λ = 1 is the Bayes weight in the battery's model; the
Laplace weight in the EQ3 scorer is 1/2). Relation: **competing on the same term**. This is the cleanest
comparison in the list because both sides claim a value with no sweep: the Laplace weight from the prior, Ω = 1
from a plateau. EQ3-B is that comparison on tabular carriers: the Bayes arm is not behind the tuned λ on 3/6
carriers and the rule at Ω = 1 is ahead of the Bayes arm on led24, led7 and the two mfeat carriers and behind on
fars and krkopt (rule − Bayes: fars −0.0200, krkopt −0.2797,
led24 +3.4429, led7 +4.0625, mfeat_factors +16.4000, mfeat_morphological +11.3000; report only, no threshold was
registered). The reason is in `omega_sweeps.txt` [1]: the Bayes weight is n_q/n_p, correct when the Fisher is
calibrated, and the empirical diagonal Fisher of a small MLP is not calibrated, so the Laplace weight under-weights
the past by an amount the rule's normalisation happens to absorb. A calibrated Laplace (which is LaLoRA's whole
contribution) removes that advantage by construction. The fair test is LaLoRA's own setting with two extra arms:
Ω = 1 on the LaLoRA penalty, and the λ sweep. CRR processing: the document's §4.3 already says the rule cannot be
Bayes-optimal except by coincidence; LaLoRA is the method that is, when its approximation holds. Nothing to change;
the claim "Ω = 1 is Bayes" must not reappear.

**Ramesh, Lewandowski, Schmidhuber, Learning to Forget: Continual Learning with Adaptive Weight Decay (FADE),
arXiv:2604.27063 [S].** Per-parameter weight-decay rates adapted online by approximate meta-gradient descent,
derived for the online linear setting. Past weight: **learned, per parameter, by a meta-gradient**, on a decay
toward zero (or a base point), i.e. an L2-SP-type past term whose weight is learned. Battery row: nearest is the
learned-weight row (GradNorm), which on the battery is at ratio 1.064 to the tuned weight at F and diverges at 16F with
the weight learning rate that worked at F. Relation: **competing, finer-grained**. FADE learns a vector of weights
where the rule sets one scalar; FADE has a target (the meta-objective, future loss) where the rule has none. The
rule's one advantage over a learned weight in the battery is the step bound: a learned weight's own learning rate
is a second knob with units. The fair test is FADE's online linear setting, where the rule's fixed-point set (the
Pareto curve) can be written down, against FADE's meta-gradient, with the past curvature rescaled between runs.
CRR processing: none; but H-EQ's "fixed strength κ" wording in the theory (prose only) is the thing FADE makes
per-parameter, and if a per-parameter Ω were ever wanted it would be a new hypothesis needing its own gate (§3.3).

**Attribution-Guided Continual Learning for Large Language Models, arXiv:2605.05285 [S].** Layer-wise Relevance
Propagation replaces the Fisher as the importance estimate; parameters critical to previous tasks receive smaller
updates. Past weight: a fixed strength on the constraint (from the abstract it is not stated whether this is a
penalty or a per-parameter learning-rate mask). Battery row: fixed weight if penalty; protected-subspace if mask.
Relation: **orthogonal** to the rule as an importance estimate; if the constraint is a mask, there is no weight for
the rule to normalise. Undecidable from the abstract; the fair test is the same as for EWC-DR once the constraint's
form is known.

**van de Ven, On the Computation of the Fisher Information in Continual Learning, arXiv:2502.11756, ICLR 2025
blogpost [S].** States that the Fisher is computed in several inconsistent ways across EWC implementations and that
many reported EWC results could improve by changing it. Not a method. Relation to the rule: **a caution that
applies with more force to the rule than to EWC**. The rule's normalisation makes w insensitive to the *scale* of F
(the 16F test) but not to its *shape*: a Fisher with the wrong diagonal profile is a wrong metric on the past, and
no scalar w repairs it. In EQ3 the Fisher is the diagonal empirical Fisher on training data at the boundary
(`runs/eq3/frozen/eq3_score.py`), which the study's report and this document state; it is one of the variants the
blogpost lists. CRR processing: the theory's A1 names the Fisher–Rao metric and its estimator is a registered
parameter; the document's claim of scale-robustness should be read as *scale*, not shape, and §5.1 of the document
now says so.

**According to PubMed: Wang J, Hu M, Li N, Al-Ali A, Suganthan PN, Randomized neural network with adaptive forward
regularization for online task-free class incremental learning, Neural Networks 2026;203:109115
([doi 10.1016/j.neunet.2026.109115](https://doi.org/10.1016/j.neunet.2026.109115)) [PubMed], and the companion
TPAMI 2026 paper ([doi 10.1109/TPAMI.2026.3652081](https://doi.org/10.1109/TPAMI.2026.3652081)).** Forward
regularisation on a randomised (fixed-feature) network, with "intervention intensity" k that the Neural Networks
paper makes self-adapting through online Bayesian learning (edRVFL-kF-Bayes), "to eliminate intractable tuning of
-kF". Past weight: **a Bayes-set regularisation strength**, in closed form because the model is linear in its
trainable weights. Battery row: fixed weight at the Bayes value. Relation: **competing on the motivation, agreeing
on the problem**. Both papers and the rule start from the same observation, that the regularisation strength is a
knob nobody wants to tune; the Bayes route sets it from the data's noise model, the rule sets it from the gradient
lengths. On a linear model with a calibrated noise model the Bayes route is exact and the rule is not (§4.3). On a
deep model the calibration fails and EQ3-B shows what happens. The fair test is theirs: an online task-free stream
on a randomised network, Bayes-set k against Ω = 1 on the same forward-regularisation term, and a k sweep. CRR
processing: none.

**According to PubMed: Liu S, Wang L, Yan R, Huo J, Li W, Gao Y, A continual learning framework with long-term and
multiple short-term memory networks, Neural Networks 2026;200:108774
([doi 10.1016/j.neunet.2026.108774](https://doi.org/10.1016/j.neunet.2026.108774)) [PubMed].** Identifies
limitations of Euclidean-distance regularisers and proposes a Gaussian-mixture regulariser "compatible with various
weight regularization based algorithms". Past weight: a fixed strength on a non-quadratic past term. Battery row:
fixed weight (the battery's past term is quadratic; a mixture term has a gradient the rule can still normalise).
Relation: **same class, orthogonal change**; the rule composes with any differentiable past term. The observation
that Euclidean regularisers are limited is A1's observation (the metric matters); the mixture regulariser is a
different metric, not a different weight.

**According to PubMed: Tzanis E, Klontzas ME, ReclAIm, Radiology: Artificial Intelligence 2026;8(4):e250923
([doi 10.1148/ryai.250923](https://doi.org/10.1148/ryai.250923)) [PubMed].** A fine-tuning workflow for medical
imaging models with a parameter-anchoring regulariser (L2-SP-type) to limit forgetting, restoring performance to
within ±2 % of baseline. Past weight: a fixed anchoring strength. Battery row: fixed weight. Relation: **same class**,
an applied instance; the anchoring strength is a knob the rule would remove. A fair test needs their pipeline; the
paper is cited to show that the fixed-anchor form is in deployed use in 2026, which is where the "saved sweeps"
value of §9 of the document would be realised if the rule held.

**According to PubMed: Zhai Z et al., Rethinking softmax in incremental learning, Neural Networks 2025;193:108017
([doi 10.1016/j.neunet.2025.108017](https://doi.org/10.1016/j.neunet.2025.108017)) [PubMed].** Identifies the
non-identifiability of the softmax cross-entropy distillation loss (a constant shift of the logits leaves it
unchanged) and proposes shift-sensitive alternatives that improve LwF, LwM and LUCIR. Past weight: not the subject.
Relation: **bears on the EQ3 LwF control, not on the rule**. EQ3-4 is VIOLATED because the rule's best Ω is ahead of
the tuned LwF weight on some carriers and behind on others with large swings in both directions (mfeat_factors/lwf
−19.3000, mfeat_morphological/lwf +12.6000, led7/lwf −7.1875). The document's §7.5 attributes this to the LwF term
being a constraint on behaviour rather than a loss on old data, so the balance of gradient lengths has no reason to
be right. Zhai et al. supply a mechanism that would add to that: a distillation gradient whose length is partly
along a direction the loss does not see (the shift) has a norm that means less than a penalty gradient's norm, and
the rule normalises by that norm. This is a hypothesis about the control, not a number; the fair test is EQ3-4
rerun with a shift-sensitive distillation loss as the LwF term, which is a new prereg. CRR processing: none required,
but it is an argument for narrowing H-EQ's scope to past terms that are losses on the past (see §4 below).

### 3.2 Projection, subspace and gradient-modification methods

**KeepLoRA, arXiv:2601.19659, ICLR 2026 [S].** Projects new-task gradients onto a subspace orthogonal to the
pre-trained model's principal subspace and the previous tasks' dominant feature directions. Past weight: **none**;
the past is protected by construction. Battery row: protected subspace (k = 2): never diverges, forgets
(L_past 15.7519 vs 0.1999). Relation: **competing mechanism, not comparable on a weight**. The rule needs a past
gradient to normalise; KeepLoRA has no past term. The two compose only if a past term is added to KeepLoRA, at which
point the rule sets its weight. What the battery says about the class (drops the past outside the protected
subspace) is the known trade-off of orthogonal projection and is not a criticism of KeepLoRA, whose subspace is
chosen to be where the past lives; the battery's k = 2 of 5 is a caricature of that choice. A fair test is not
available without the paper's code.

**Safety Alignment as Continual Learning (OGPSA), arXiv:2602.07892 [S]; SafeAnchor, arXiv:2604.17691 [S];
Muon-OGD, arXiv:2605.08949 [S].** Three orthogonal-projection methods for LLM fine-tuning: OGPSA removes from each
safety gradient its component in a low-rank general-capability subspace; SafeAnchor finds low-rank safety subspaces
by Fisher eigendecomposition in LoRA space, constrains gradients to the orthogonal complement, and adds
threshold-triggered corrective replay; Muon-OGD reformulates the projection in spectral rather than Frobenius
geometry. Past weight: none in the projection; SafeAnchor's replay is triggered by a threshold (a target, like the
adaptive-KL row). Battery row: protected subspace. Relation: **competing mechanism**. SafeAnchor is the interesting
one for CRR: it uses the Fisher's eigenstructure (A1's metric) to decide *where* the past is and a threshold to
decide *when* to pull back, where the rule uses the Fisher only through the past gradient and decides *how hard* to
pull back at every step. Muon-OGD's point that projection is usually done in the wrong geometry is A1's point made
about projection; the rule's gradients in the battery and in EQ3 are Euclidean norms of Euclidean gradients (the
EQ2 study found Fisher vs Euclidean norms made no difference on its carriers; `reports/eq2.md`), which is a choice
Muon-OGD's argument would question at LLM scale. CRR processing: H-EQ as written takes ‖·‖ in the Fisher metric
(A1); the frozen scorers' Euclidean norm is a registered deviation that the EQ2 report records. If the rule were
ever run on a transformer, the norm should be named in the prereg and both reported (as A1 requires for the
phase).

**On the Plasticity and Stability for Post-Training LLMs (Probabilistic Conflict Resolution), arXiv:2602.06453
[S].** In GRPO post-training, models the plasticity and stability gradients as random variables and arbitrates
their conflict with an uncertainty-aware soft projection. Past weight: a projection fraction set by uncertainty.
Battery row: soft conflict projection (c = 0.5): L_present 0.0215, L_past 65.2291, the worst forgetting in the
battery, because removing half the conflicting component at every step still lets the present gradient carry the
learner off the past optimum in the non-conflicting directions and the remaining half of the conflict does the rest.
Relation: **competing; the battery's c is not PCR's c.** PCR's fraction is set from gradient-variance estimates, and a
fixed 0.5 does not represent it. The battery row shows what soft projection *without* a past term does on this
model; it says nothing about PCR's variance estimate. What the comparison does isolate is a difference in kind:
the rule adds the past gradient with a weight; PCR subtracts part of the present gradient. On the quadratic model
the fixed points of the first lie on the Pareto curve; the fixed points of the second lie wherever the present
gradient is orthogonal to the past gradient, which is not a stationary point of any weighted sum.

**Hu et al., Hidden Failure Modes of Gradient Modification under Adam, arXiv:2604.22407, withdrawn by the authors
[S].** Cited only for the caution the rendering states: gradient modification applied upstream of Adam interacts with
Adam's second-moment estimate. The rule is exactly a gradient modification upstream of the optimiser (it rescales
g_q before the sum), and every study in this repository used plain SGD (`runs/eq3/frozen/eq3_score.py`). The
withdrawal removes the paper's evidence, not the question. **A fair GPU test of the rule must run SGD and Adam as
separate pre-registered arms**, and the Adam arm must decide in the prereg whether w multiplies the raw past
gradient (upstream) or the Adam-preconditioned one. This is added to the fair-test list of §5. CRR processing: none;
the theory says nothing about the optimiser.

**Continual Safety Alignment via Gradient-Based Sample Selection, arXiv:2604.17215, ACL Findings 2026 [S].**
Filters out high-gradient fine-tuning samples, which the abstract says cause the most safety degradation. Past
weight: the paper keeps whatever alignment term it uses fixed and acts on the *present* data. Battery row: sample
selection at fixed λ = 1 (q = 0.8): total 3.3652, ratio 1.015 to the tuned weight at F, diverges at 16F because its
λ is fixed. Relation: **orthogonal and composable**. Selection bounds the present gradient from above by dropping
its largest batches; the rule bounds the past pull by the present pull. Together they bound both. The battery's
selection row is the best non-tuned method at F on the total, and its L_past (0.1855) is the lowest in the table:
dropping the largest present steps is, on this model, a better way to keep the past than weighting it. This is the
paper in the list whose mechanism the rule most obviously lacks and could borrow, and it is the answer to the
poisoned-occasion failure in `ontology/07_turing_safety_ingression.md` (row 6): the rule's unbounded response to
one extreme batch is a present-gradient problem that selection addresses and normalisation does not.

**MANGO, arXiv:2605.19080 [S].** Gradient gating with meta-learned regularisation for online continual learning.
Past weight: **meta-learned**; gating on the gradient. Battery row: learned weight (GradNorm) is the nearest. Relation:
**competing, with a target**. As for FADE: a learned weight has a target the rule lacks and a second learning rate
with units the rule also lacks. Undecidable further from the abstract.

### 3.3 LLM forgetting, architecture and RLHF context

**Mechanistic Analysis of Catastrophic Forgetting in LLMs During Continual Fine-tuning, arXiv:2601.18699 [S].**
Twenty models; forgetting attributed to gradient interference in attention weights, representational drift in
intermediate layers and loss-landscape flattening; correlates with task similarity; Low-Rank Circuit Projection
mitigates. Past weight: none (projection). Relation: **context for where a past term would act**. The rule sets one
scalar for the whole parameter vector; this paper's finding that forgetting is localised (attention, middle layers)
is an argument that one scalar is the wrong granularity at LLM scale, and FADE's per-parameter weights or a
per-layer Ω are the response. A per-layer Ω is a new hypothesis (gate needed). Not runnable here.

**TFGN, arXiv:2605.15053 [S].** An architectural overlay for task-free, replay-free continual pretraining, with the
stated backward transfer of −0.007 at 8B parameters and "no Fisher penalty". The abstract's survey sentence, that
every published method "retains a buffer, requires task identifiers, applies a regularization penalty that scales
poorly with model size, or operates at sentence-classification scale", places the rule in the third clause: the
rule is a regularisation penalty's multiplier and inherits the penalty's cost (a stored Fisher and anchor of the
model's size). Relation: **competing at the level of approach**; the rule does nothing to the penalty's memory cost,
which is the objection TFGN raises. No test is possible here.

**Alssum et al., Unforgotten Safety, arXiv:2512.10150 [S].** Frames safety degradation under fine-tuning as
continual learning and reports that regularisation-, memory- and merging-based CL methods all lower attack success
rates relative to plain fine-tuning. Relation: **the setting in which the rule's "no sweep, no divergence" property
would be tested at LLM scale**; the regularisation arm of that paper is a fixed-λ arm and the rule would be an
additional arm. The document's §9 caveat stands: the rule is not itself a safety mechanism.

**Shenfeld et al., RL's Razor, arXiv:2509.04259, ICLR 2026 [S].** States that forgetting is determined by the KL
divergence between the fine-tuned and base policy evaluated on the new task, and that on-policy RL is implicitly
biased toward KL-minimal solutions. This is an **endpoint** statement: forgetting is a function of where the model
ends, not of the path it took. That is the conclusion the ledger row ARC-T1b reached on the old toy-LM runs
(R² of log forgetting on log E_old 0.99351; the path did not beat the endpoint), and the convex-learner lemma of
`theory/SCOPE.md` §4.1. Relation to the rule: the rule is a step-by-step controller, so it is a path method
applied to an endpoint problem; on a convex model its endpoint is a point on the Pareto curve, which is all that
matters, and the path is irrelevant. Relation to CRR: **H-T1 (forgetting tracks path length) is contradicted in its
framing by this paper as it is by ARC-T1b**, and study T1x's design already requires the endpoint predictors E_old
and E_new as baselines that can win. CRR processing: the paper's claim that KL on the *new* task's inputs is the
right endpoint is a specific, testable refinement of E_new vs E_old that T1x should carry as a third endpoint
predictor; noted in §4 below.

**Gauthier, Bach, Jordan, Explaining and Preventing Alignment Collapse in Iterative RLHF, arXiv:2605.04266 [S];
Rethinking KL Regularization in RLHF, arXiv:2510.01555 [S].** Context for the adaptive-KL comparison (the klctrl row):
the first identifies a parameter-steering term dropped by standard iterative RLHF; the second analyses how the KL
penalty is implemented. Neither sets the KL weight by a gradient ratio. The klctrl row of the battery (a Ziegler-style
multiplicative controller toward a target past loss) is at ratio 1.117 to the tuned weight at F and diverges at 16F
from its starting weight of 1. Relation: **competing on the same term**, the KL penalty to a reference policy; the
controller has a target the rule lacks and the rule has a step bound the controller lacks. The fair test at LLM scale
is an RLHF run with three KL arms: fixed β, Ziegler's controller at a registered target, and Ω = 1 on the KL gradient,
under SGD and Adam separately (§3.2, the Adam caution).

## 4. What the cross-verification changes, and what it asks of CRR

1. **Prior art, restated.** The rule's mechanism (equalise gradient lengths) is GradNorm at α = 0 and the
   multiple-gradient descent family (Désidéri 2012, named), applied as a scalar multiplier on one fixed past term;
   the battery's learned-weight row is at ratio 1.064 to the tuned weight at F against the rule's 1.049. The rule's distinct property is not the balance
   but the bound: with no learned weight and no target there is no second knob with units, and the step is bounded by
   the present step. That is the whole of what the battery finds in its favour, and it is a property, not a result.

2. **Scale, not shape.** The rule is robust to the *scale* of the past curvature and blind to its *shape*.
   Everything in §3.1 that improves the importance estimate (EWC-DR, attribution, the Fisher-computation caution,
   the Gaussian-mixture regulariser) composes with the rule and is untouched by it. The document's §5.1 says this.

3. **The Bayes claim stays negative.** LaLoRA and the edRVFL-kF-Bayes papers set the weight from a posterior and are
   correct where their approximation holds; the rule agrees with Bayes only at equal counts and by coincidence
   (`omega_sweeps.txt` [1]). EQ3-B's report-only advantage of the rule over the Laplace weight on four of six
   carriers is a statement about an uncalibrated empirical Fisher, not about Bayes.

4. **Scope of H-EQ (a v3.2 item for the owner's decision list, not a change made here).** The results on LwF and
   DER++ (EQ3-4 VIOLATED with both signs), the softmax non-identifiability of Zhai et al., and the composability
   argument of point 2 all point the same way: H-EQ should be stated for past terms that are losses or penalties on
   the past whose gradient length is meaningful, not for behavioural constraints (distillation) or projections. The
   theory as written (`theory/CRR.md` H-EQ) does not restrict the past term. A narrowing is a change to a hypothesis
   after seeing data and needs a fresh prereg for any later study (R3); it is recorded here as a proposal.

5. **The optimiser is unstated (a prereg item).** No study here ran Adam. The withdrawn Adam paper's caution and the
   fact that every LLM method in §3 trains under Adam mean the rule's upstream/downstream placement relative to the
   preconditioner is a registered parameter for any GPU study.

6. **H-T1 and RL's Razor.** The endpoint framing of forgetting at LLM scale in the 2026 literature is the framing
   ARC-T1b already forced on the repository. T1x, if run, should carry the new-task KL of RL's Razor as a third
   endpoint predictor (E_new in the theory's own notation, evaluated on the new task's inputs, which is how the
   frozen `path_length` companion already defines it). No change to the theory; a line in the T1x design.

7. **What the rule could borrow.** Gradient-based sample selection (the best non-tuned row at F on the past loss)
   bounds the present gradient; the rule bounds the past pull by it. The poisoned-occasion failure in the ontology
   battery is a present-gradient failure. A combined rule is a new hypothesis and needs a gate before any prereg;
   it is not proposed here beyond this sentence.

## 5. The fair tests, collected

| paper / class | test that would decide the relation | runnable here? |
|---|---|---|
| EWC-LoRA, EWC-DR, LaLoRA (fixed / Bayes weight on a penalty) | EQ3 design on the paper's penalty: Ω = 1 vs its λ sweep vs the Laplace weight, per carrier, one resolvable step; report whether the tuned λ sits at the stability edge | no (GPU, PyTorch, the papers' code) |
| FADE, MANGO (learned weights) | online linear setting; Pareto-curve fixed points vs the meta-gradient; past curvature rescaled between runs | the linear part yes, as a new gated hypothesis |
| KeepLoRA, OGPSA, SafeAnchor, Muon-OGD (projection) | not a weight comparison; compose (projection + a past term with Ω = 1) vs projection alone | no |
| PCR (soft projection with variance-set fraction) | PCR's fraction vs Ω = 1 on the same GRPO objective | no |
| adaptive KL (Ziegler-style; Gauthier et al.; Rethinking KL) | RLHF with fixed β / controller / Ω = 1 arms, SGD and Adam separately | no |
| sample selection (ACL Findings 2026) | compose: selection + Ω = 1 vs each alone, with an injected extreme batch | the quadratic part yes, as a new gated hypothesis |
| Zhai et al. (softmax non-identifiability) | EQ3-4 rerun with a shift-sensitive distillation loss as the LwF control | yes, as a new prereg on unseen carriers |
| RL's Razor (endpoint KL) | T1x with new-task KL as a third endpoint predictor | T1x is not yet built |

## 6. What a surrogate would have done

The battery's model is itself the surrogate: a convex two-task quadratic on which every rule has closed-form
equilibria. On it the rule is not the best method and is not Bayes; it is the only rule in the set that keeps its
quality under a 16-fold change of the past curvature with one knob setting, and it does so because its step is
bounded by the present step. Any rule with that bound would pass the same test; the test measures the bound, not
CRR. The gate for H-EQ (`prereg/eq3/gate_EQ.txt`) is the place where the rule had to FAIL on a convex replay
learner and PASS on a mismatched-scale learner, and it did; this note adds nothing to that gate and no row to the
ledger.
