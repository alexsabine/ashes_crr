# RQM development declaration: the candidate, the synthetic gate and the development rule (pushed before any candidate code runs)

**Follows.**
- `DECLARATION.md` (1d480cb);
- the four dossiers `docs/citations/rqm_q{1..4}_2026-09-30.md`;
- `CRR_READING.md` and `docs/citations/rqm_priorart_2026-09-30.md`. Their verdict: no CANDIDATE. The reading selects
  input-space Gaussian replay, which is the GMR/DGR family.

Prompt-log entry 245; AGENT_LOG 190.

## The arms (all on SEC1's learner, `checks/rqm_lib.py`)

**Memory is counted in float32 numbers** and matched by ER rows (one row = d numbers).

| arm | what it keeps | memory per class | label |
|---|---|---|---|
| **IGR-F** | per class, at that class's cut: the input mean μ_c and the covariance Σ_c shrunk as (1 − α)Σ_c + α·(tr Σ_c / d)·I, with α = 0.1; never refitted | d + d(d+1)/2 | the candidate, full form |
| **IGR-D** | per class, at its cut: μ_c and the diagonal variances; never refitted | 2d | the candidate, diagonal form |
| **FGR-F** | as IGR-F, but μ and Σ fitted to the hidden layer's activations (256-d) at the cut, and replayed as hidden activations into the head only | 256 + 256·257/2 | the CRR ablation (memory that depends on the learner's state) |
| **ER(m)** | a class-balanced buffer of m raw rows per class (`rqm_lib.run_er`, M = m × classes seen) | m·d | the target to match |
| **FT** | nothing | 0 | lower bound |
| **JOINT** | all data at once | — | upper bound |
| **SEC-CLIP** | SEC4's clipped SEC (frozen code of `runs/sec5/frozen/`) | parameters and importances | the regularisation family |
| **RFR** | fixed random ReLU features of the input (width 512, seed 0), with the accumulated Gram G = Σ hhᵀ and C = Σ hyᵀ; the head is (G + λI)⁻¹C, λ = 1 | 512·513/2 + 512·K (shared) | the frontier exemplar-free baseline (CIRCLE / RanPAC form; exact against joint ridge on those features) |

**The replay step (IGR and FGR).**
- During each task after the first, every SGD step concatenates the current batch of 10 with 10 pseudo-samples.
- The pseudo-samples are drawn class-balanced from the stored old-class Gaussians (equal numbers per old class, by a
  seeded rotation), exactly as ER concatenates a replay batch.
- IGR's pseudo-inputs go through the whole network. FGR's pseudo-activations enter at the head, and its gradient updates
  the head only.

**Matched memory.** For an IGR form with memory b_c numbers per class, the matched ER keeps
m = ⌈b_c / d⌉ rows per class:
- IGR-F: ⌈(d + 3)/2⌉ rows per class;
- IGR-D: 2 rows per class.

The primary comparison is IGR against its own matched ER.

## Phase A: the synthetic gate (`checks/phase_a.py`, pinned; seeds 0–4)

**Two streams, K = 10 classes, 2 classes per task, d = 20, 1500 rows:**
- **POS** — SEC1's synthetic stream (`S._synthetic`): Gaussian classes, each shifted by 3 on its own axis. A class
  Gaussian is the true generator here.
- **NEG** — concentric rings. Class c lies on a circle of radius 1 + c in the first two coordinates (angle uniform,
  radial noise sd 0.1), with 18 standard-normal nuisance coordinates. A single class Gaussian fills the disc and overlaps
  every inner ring, so Gaussian replay is the wrong generator. ER stores true points.

**Step.** max(1, 2 × SE over seeds of ER's accuracy), as in the SEC studies.

**The gate: all four must hold.**
- **G-POS:** on POS, each IGR form is not behind its matched ER by a step. If IGR cannot match ER where its generator is
  exact, there is nothing to test.
- **G-NEG:** on NEG, each IGR form is behind its matched ER by more than a step. If IGR ties ER where its generator is
  wrong, a real-data PASS would not show that its memory works.
- **G-FT:** on both streams, FT is behind ER by more than a step (forgetting exists).
- **G-ID:** with the replay batch forced empty, each IGR form equals FT bit for bit (the code path is FT's plus replay).

**Reported beside the gate, not gating:**
- FGR-F against IGR-F on POS: the CRR ablation. The prediction, from the reading: IGR-F ahead.
- RFR, SEC-CLIP and JOINT on both streams.

**If the gate closes,** RQM stops at Phase A (R12). The reason is recorded and nothing is pre-registered.

## The development stage (SEEN carriers only)

**The carriers.** The 30 SEEN carriers SEC has been scored on: SCL3's 10, SEC3's 6 (covertype, dionis, fabert, helena,
jannis, volkert; shuttle was excluded at K 2), SEC4's 6 and SEC5's 8. The development script prints the list and N_dev.

**The selection rule (fixed now).**
1. For each IGR form, count the carriers where it is not behind its matched ER by a step (step as above, over seeds 0–4).
2. Choose the form with the larger count; a tie goes to IGR-D (less memory).

**D-GATE, all must hold:**
- **D-COUNT:** the chosen form is not behind its matched ER on at least ⌈0.75 N_dev⌉ carriers.
- **D-RFR:** the chosen form is ahead of RFR by a step on at least one third of the carriers. Otherwise it is not
  distinguishable from the frontier exemplar-free baseline, and the pre-registration must say "reduces to RFR" (R7).
  This is reported, and it does not close the gate.
- **D-PHASE:** Phase A's gate was OPEN.

**If D-GATE closes,** RQM stops before any unseen data (R12) and reports why.

## If it opens: the pre-registration (fixed now; written after development, hashed before any unseen data)

**The primary row.** The chosen IGR form is not behind its matched ER by a step, on at least ⌈0.75 N⌉ unseen carriers.
It is NOT DECIDABLE if N < 4.

**The other registered rows:**
- **IGR − JOINT** (report);
- **IGR against RFR** (does it reduce to the frontier baseline?);
- **the CRR ablation, IGR − FGR** ("not behind" and "ahead" counts);
- **no collapse:** no seed below half of ER's mean accuracy;
- **sensitivity:** the shrinkage α ∈ {0.01, 0.3} for the full form, and the replay batch at 5 and 20 instead of 10. More
  than one flip is FRAGILE.

**The unseen carriers.**
- Pool OpenML study 454 (New_OpenML_Suite_2025_classification), then study 445, then the eligible study-293 datasets not
  used by SEC5, under SEC5's eligibility rule unchanged.
- The pool is built until ≥ 8 datasets are eligible and not SEEN. At most 12 are kept by the seeded draw
  `default_rng(20261001)`.
- Metadata only before the hash.

**The data step** is not before 2026-10-01 00:00 UTC (R3): the form is chosen on SEEN data on 2026-09-30.

**The label.** A pass is recorded as "not a CRR rule; the GMR/DGR family with a Gaussian generator in input space, selected
by the CRR reading" (R8).

## Amendment 1 (2026-09-30, POST HOC: written after Phase A run 1; AGENT_LOG 191)

**What run 1 found** (`checks/phase_a_run1.txt`, pinned as run): **GATE CLOSED**, on G-NEG alone.
- The concentric-rings stream was unlearnable by this learner: JOINT scored 10.77 and FT 9.90, where chance for 10 classes
  is 10.
- So no arm could be behind or ahead of another on it. The control was defective: it tested nothing about the generator.
- Run 1 stands as the declared result of the declared gate.

**The correction** (post hoc, declared here before run 2).
- **NEG is replaced by NEG2**, a stream on which a per-class Gaussian is provably the wrong generator and the learner can
  learn.
  - **The pairs.** Five pairs of classes (2k, 2k+1), each on its own two coordinates (2k, 2k+1) of d = 20; the other
    coordinates are N(0, 1).
    - Class 2k: four tight clusters (sd 0.3) at the corners (±a, ±a).
    - Class 2k+1: four tight clusters at (±√2·a, 0) and (0, ±√2·a).
    - a = 3.
  - **The trap.** Both members of a pair have the **same mean (0) and the same covariance** (a²·I on their two
    coordinates). So their Gaussians are identical, and Gaussian replay cannot keep them apart once their task has passed.
    Real stored rows can.
- **One condition is added to the gate. G-LEARN:** on NEG2, JOINT is ahead of FT by more than a step (the stream is
  learnable). If G-LEARN fails, the gate is CLOSED again and RQM stops (R12).
- **Nothing else changes:** the arms, α, the replay batch, the matched memory, G-POS, G-FT, G-ID, the development rule
  and the prereg shape.
- **What this amendment cannot do.** It cannot make run 1 open. Run 2's gate is a post hoc gate, and any pre-registration
  that follows will say so.
