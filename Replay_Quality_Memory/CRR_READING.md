# CRR as a heuristic on the replay-quality-memory bottlenecks (written before any candidate code)

**The procedure** is DECLARATION.md §3. For each bottleneck the four dossiers name, the investigator records what CRR says:
- **SILENT:** CRR has nothing on it.
- **RESTATES:** CRR gives the domain's own fix under another name.
- **CANDIDATE:** CRR points to a change not in the swept methods.

Every reading below is the investigator's, written on 2026-09-30 after the dossiers
(`docs/citations/rqm_q{1..4}_2026-09-30.md`) and before any candidate code. The prior-art check for the one design the
reading selects is `docs/citations/rqm_priorart_2026-09-30.md`.

## The bottlenecks and the readings

| # | bottleneck (the sources' words) | CRR ingredient | reading |
|---|---|---|---|
| B1 | **representation drift**: stored class statistics go stale as the backbone learns (LDC: "performance degradation ... is largely due to feature drift"; Wang et al. survey: "representation shift caused by sequentially updating the feature extractor") | Proposition 7, transposed as in EPS1–EPS3: a settled content keeps its meaning across later occasions only if it **does not depend on anything later learning changes** | **RESTATES** (see below) |
| B2 | **frozen features are rigid and first-task-biased** (VILA: "representation rigidity as the primary bottleneck"; RanPAC: "unlikely to be as powerful ... from scratch"; CIRCLE: the train-vs-freeze trade-off) | A6: the next occasion is seeded from the settled past, but the present occasion is free, so the learner should keep learning | **RESTATES** (learn freely, keep memory elsewhere: generative replay's design) |
| B3 | **single Gaussians are too crude; even true statistics leave a gap** (EFC++: true statistics 49.33 against joint 71.00; REMIX, PGPFR on diagonal and linear approximations) | P2/P3: an occasion's content under a fixed set of kept constraints is the MaxEnt distribution; for a mean and a covariance that is the Gaussian | **RESTATES** (MaxEnt; CRR does not say how many constraints to keep) |
| B4 | **drift estimated from current data only is biased** (LDC; ADC needs "a big enough quantity of current data") | none | **SILENT** |
| B5 | **decision or task-recency bias of the classifier** (DPCR "semantic shift and decision bias"; AdaGauss) | H-EQ read per class: settled past and present exert equal pull | **RESTATES** (class-balanced replay) |
| B6 | **generator quality, forgetting inside the generator, compute** (DGR "depends on the quality of the generator"; GUIDE "forgetting happening in the diffusion model itself") | A3 + A6: an occasion's content is settled at its cut and not re-counted; the generator for a class is fitted once at that class's cut and never retrained | **RESTATES** (one generator per class: the Generative Classifier; GMR) |
| B7 | **one linear map underfits; the Gram matrix is ill-conditioned** (DS-AL; SPARCL) | none | **SILENT** |
| B8 | **statistics cost memory** (ACIL's R is about 10× the exemplar buffer; EFC++ covariances about 100 MB) | A1′: contents are kept at the system's own resolution | **SILENT in practice** (CRR fixes no memory budget) |
| B9 | **stored aggregates leak membership, most for small classes; "no stored raw examples" is not a privacy guarantee** (Pyrgelis; Wang et al. prototypes AUC 0.6729; Tobaben et al.) | none | **SILENT** (privacy is the domain's: differential privacy) |
| B10 | **long horizons degrade drift compensation** (CIRCLE: compensation "degrades sharply" at 50–100 tasks) | as B1 | **RESTATES** |

## B1 in detail: the one design the reading selects

**The reading.**
- EPS1–EPS3 found one condition across thirteen systems. A pause is safe for an agent only if its valuation does not
  depend on anything the pause changes. Own-clock indexing alone was not enough when a state kept moving (the attention
  test's habit; EPS2 T2's resources).
- Transposed to memory: a content settled at a cut stays valid on later occasions only if it does not depend on anything
  the later occasions change.
- Class statistics stored in the backbone's feature coordinates depend on the backbone's weights. Later learning changes
  those weights, so the stored content drifts **by construction**. That is B1.

**What this prescribes.** Store the settled content in coordinates that later learning does not change. Two ways exist:
- **freeze the coordinates** (frozen or random features: the analytic family), which runs into B2;
- **keep the content in the world's coordinates, the input space**, and replay it through the learner as it is now.
  The learner then keeps learning (B2), and the memory never drifts (B1, B10).

For the repository's carriers the second way is cheap. The inputs are tabular, with few dimensions, so a class's mean and
covariance cost about (d + 3)/2 raw rows. Fitting one Gaussian per class at that class's cut and never refitting it is
A3 + A6 (B6).

**Why this is RESTATES, not CANDIDATE.**
- The design is deep generative replay with a Gaussian generator in input space.
- Gaussian Mixture Replay (Pfülb & Gepperth, arXiv 2104.09240 v1) publishes GMM pseudo-rehearsal in input space for
  class-incremental learning.
- The Generative Classifier fits one generator per class.

CRR selects this design by a principle it shares with the drift literature. It does not add a mechanism.

**What is CRR-specific and testable.** One comparison follows from the reading and is not in the swept papers as a
controlled ablation on the same learner: the **same** Gaussian replay with the memory stored in **feature** space (depends
on the learner's state) against **input** space (does not). CRR's condition predicts that input-space memory is ahead
wherever the features keep learning. The drift literature predicts the same, so this is a check of the condition's
reading, not evidence for CRR (R8).

## What goes forward

Everything below is declared in `DEV_DECLARATION.md` before any of it runs.

1. **The candidate IGR.** Per-class Gaussians in input space, fitted at each class's cut and never refitted, replayed
   class-balanced while the MLP keeps learning. Two named forms:
   - full covariance with a named shrinkage constant;
   - diagonal covariance.
2. **The CRR ablation FGR.** The same, with the Gaussians fitted in the hidden layer's feature space at the cut.
3. **Baselines (R7).**
   - ER at the candidate's matched memory;
   - fine-tuning; joint training;
   - SEC with the clip (the regularisation family);
   - the frontier exemplar-free method implementable here, analytic ridge on fixed random features (the
     CIRCLE / RanPAC form, exact against joint ridge on those features).
4. **Labels.** If IGR passes, the ledger records "not a CRR rule; the GMR/DGR family with a Gaussian generator in input
   space, selected by the CRR reading". If it ties the random-feature ridge baseline, it reduces to that (R7).
