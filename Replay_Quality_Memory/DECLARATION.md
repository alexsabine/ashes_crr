# Declaration: RQM, replay-quality memory without stored data, with CRR as the heuristic (pushed before any source, code or data)

**Status.**
- **The request.** Owner request, prompt-log entry 245 (2026-09-30): "Apply CRR to solving this 'replay-quality memory'
  problem. You are at liberty to search online for the frontier methods, using CRR as a heuristic to determine the
  bottlenecks. Find ways to use CRR to resolve these bottlenecks then we continue the pipeline testing to try to achieve a
  Pass-1."
- **The problem, as stated in the conversation** (prompt-log entry 244 and the answer to it):
  - Replay (keeping real past examples) remembers well in class-incremental learning.
  - The regularisation family (EWC, SEC: keeping only a summary of what mattered) keeps no data but fails there. The
    published split-MNIST class-IL numbers quoted in `docs/notes/2026-09-25_results_vs_published.md` are 19.52–20.01 %
    against replay's 90.78–90.79 %.
  - The target is **replay-quality memory without storing raw past examples.**
- **What this file fixes before anything runs:** the definition of the target; the positions to be graded from the
  frontier literature; the procedure by which CRR is used as a heuristic; the rules for turning a candidate into a
  pre-registered test; and what a PASS-1 would require. The candidate method itself is **not** fixed here. It is chosen
  after the sweep, by the procedure below, on SEEN data only, and pre-registered before any unseen carrier is opened.
- **Rung.** The sweep and the design are notes (R8). Only the eventual pre-registered study can produce ledger rows.

## 1. The target, defined now

**Class-incremental learning (class-IL).**
- A learner sees a stream of tasks, each introducing new classes.
- At test time it must classify among **all** classes seen so far, with no task label.
- **The score:** the final average accuracy over all classes, after the last task.

**Replay-quality.** The candidate's final class-IL accuracy is within one resolvable step of **experience replay (ER) with
a buffer of raw examples**. The buffer size is fixed in the pre-registration at a memory budget comparable to the
candidate's stored state in bytes.

**Without stored data.** The candidate keeps no raw past example, and no one-to-one transform of one:
- permitted: aggregates (counts, means, covariances, statistics over many examples), model parameters, and parameters of
  generators;
- not permitted: stored inputs, stored per-example features, or per-example logits.

## 2. The frontier sweep and the positions graded (rule as in `AI_Safety/CORRIGIBILITY_2026`)

**Families** (one dossier each, `docs/citations/rqm_<family>_2026-09-30.md`, every quote verified against its fetched text,
unreached sources marked NOT REACHED, current arXiv versions noted, R10):
- **Q1:** exemplar-free class-IL with prototypes and feature statistics: class means and covariances, prototype
  augmentation, feature translation, and drift compensation of stored statistics. Examples: PASS, SSRE, FeTrIL, FeCAM,
  EFC, SDC and its successors, LDC, ADC.
- **Q2:** generative and model-inversion replay: deep generative replay, data-free class-IL with model inversion
  (ABD, R-DFCIL), and diffusion-based replay.
- **Q3:** closed-form and analytic learning (ACIL, GKEAL, DS-AL and successors; streaming LDA), and pretrained-model
  class-IL (SimpleCIL, RanPAC, EASE, prompt-based methods). This includes what these methods assume (a frozen or
  pretrained backbone).
- **Q4:** privacy of stored statistics and generators: membership inference and reconstruction from class statistics or
  model inversion, and differential privacy for continual learning.

| id | position | expected grade |
|---|---|---|
| M1 | exemplar-free methods that store class statistics can approach replay-quality class-IL when the feature extractor is fixed or pretrained | REDUNDANT |
| M2 | the main bottleneck of statistics-based memory is representation drift: stored statistics go stale as the backbone learns | REDUNDANT |
| M3 | drift can be compensated by estimating how old statistics move, from current data only | REDUNDANT |
| M4 | closed-form (analytic) learning on fixed features equals joint training exactly, with no stored examples | REDUNDANT |
| M5 | generative or inversion replay recovers much of replay's accuracy but costs compute and has its own drift and quality limits | PARTLY REDUNDANT |
| M6 | class statistics and generators can leak information about training data; formal privacy needs extra mechanisms | REDUNDANT |
| M7 | on small models trained from scratch (no pretraining), exemplar-free methods stay well below replay | MIXED |

## 3. How CRR is used as the heuristic (the procedure, fixed now)

The investigator reads each bottleneck the sweep finds through CRR's commitments (`theory/CRR.md`) and writes down, before
any design code, what CRR says about it. The ingredients permitted:

- **A3/D5, the cut and the occasion.** A task boundary is a cut that settles an occasion. What is kept at the cut is that
  occasion's content, Φ_m.
- **A6, regeneration.** The next occasion is seeded from the settled past as a Fréchet mean of past contents under MaxEnt
  weights, at bounded strength. So the memory is a set of settled contents, not a record of the path.
- **P2/P3, MaxEnt weights.** Which occasions count, and how much.
- **A1′/D1, the unit.** Contents are compared in the system's own resolvable unit (the Fisher–Rao metric), not in raw
  coordinates.
- **The empty cut (Proposition 7) and the lossless pause.** Where relevant to what must be kept at a cut.

**Reading rule.**
- For each bottleneck the investigator records one of:
  - CRR **says nothing** (SILENT);
  - CRR **restates** the domain's own fix (RESTATES);
  - CRR **points to a specific change** not in the swept methods (CANDIDATE).
- Each CANDIDATE is checked against the dossiers for prior art before it goes further. "Not found" is never "novel".

## 4. From candidate to test (rules fixed now)

1. **Phase A, synthetic gate.** Each candidate, the baselines and at least one positive and one negative control run on
   synthetic class-IL streams. The gate must be able to close. If no candidate opens its gate, the work stops here (R12)
   and is reported.
2. **Development on SEEN carriers.** Candidates are compared on SEEN OpenML carriers (the 22 SEC carriers, and SEC5's 8).
   The selection rule and a development gate are declared in a development declaration pushed before any candidate runs.
3. **Pre-registration.** One candidate (or none) is pre-registered, with the unseen carriers, the exact criterion, the
   baselines, the sensitivity table and the exclusion rules. It is hashed, OpenTimestamps-stamped and pushed before any
   unseen carrier is opened.
4. **The data step** is on a later calendar day than any development choice (R3).

**Baselines required (R7).**
- ER with a raw-example buffer at matched memory;
- fine-tuning (the lower bound);
- joint training on all data (the upper bound);
- EWC or SEC (the regularisation family);
- the strongest frontier exemplar-free method implementable on CPU in the repository's learner (named after the sweep).

**What a PASS-1 would require** (CLAUDE.md §7):
- PASS-0 on the pre-registered criterion ("not behind ER at matched memory, by a step, on ⌈0.75 N⌉ carriers").
- A sensitivity table flipping in at most one cell.
- No pre-registered control violated.
- No reduction to a published method: the candidate must not merely tie the strongest frontier exemplar-free baseline;
  if it does, the row says so.
- An OpenTimestamps anchor and stated carrier admissibility.

**What would not be a result.**
- A candidate that equals a swept method gets a row that names that method (R7).
- A PASS on carriers where every method ties.

## 5. Expectations, written now

1. The sweep will grade M1–M6 REDUNDANT or PARTLY REDUNDANT. The frontier already knows the bottleneck (drift) and has
   several fixes.
2. CRR will mostly RESTATE. A3 (keep settled class contents at the cut) and A6 (regenerate from them) describe prototype
   and statistics replay. A CANDIDATE, if any, is most likely in how stale contents are carried into the present metric
   (A1′).
3. **On the repository's small from-scratch MLP learner** (no pretraining), a statistics-based candidate that must also keep
   learning its features will stay behind ER. A candidate that freezes features after the first task will be limited by
   first-task features. A PASS-1 is possible, but it is not the expected outcome.
4. Whatever passes will likely be a known method (M4, analytic learning on fixed features) rather than a CRR-specific one,
   and the report will say so.

## Outputs

- `Replay_Quality_Memory/DECLARATION.md` (this file);
- `docs/citations/rqm_q{1..4}_2026-09-30.md`;
- `checks/claims.py`, `grade.py` and `grade.txt` (M1–M7);
- `Replay_Quality_Memory/CRR_READING.md` (the heuristic reading, per bottleneck, written before any design code);
- `checks/phase_a.py` and `.txt` (the gate);
- `DEV_DECLARATION.md` and the development outputs;
- then `prereg/rqm1/` and the study.
