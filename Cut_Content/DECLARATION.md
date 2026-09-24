# Declaration — when does a cut need content? Phase A of study CUT1 (synthetic only), declared before it runs

- **Written and pushed:** 2026-09-24 (prompt-log entries 151–152), before `Cut_Content/checks/cut_phaseA.py` exists.
- **The literature check came first:** `docs/citations/plasticity_resets_2026-09-24.md`, fetched on the day.
- **No real data is involved.** The real-data prereg (CUT1) follows only if this gate reads OPEN. Its data step is not
  before 2026-09-25 00:00 UTC (R3), on carriers absent from `data/SEEN.md` and distinct from SCL3's.

## Why this study

**The empty cut and the reset are different things.**
- **The empty cut** is a lossless pause on the learner's own clock. It left learning bit-for-bit unchanged:
  - SCL1-1: 12/12 carriers;
  - SCL2-1: 45/45 runs.
- **The reset** carries content: SCL1 returned the learner to its task-boundary checkpoint.
  - It raised accuracy on seen data (SCL1).
  - It failed on unseen data (SCL2-R: 1/9 ahead, 1/9 behind; SCL2-M FAIL).

**What the literature says** (`plasticity_resets_2026-09-24.md`):
- SCL1's reset is "hard reversion". A soft blend with the checkpoint beats it, and so does reinitialisation (Cho et al.,
  arXiv:2502.07274v5).
- Plasticity loss, the problem that content-bearing resets are known to fix, appears only after tens to thousands of task
  switches. SCL's streams had at most five tasks.
- No paper tests network resets together with interruptibility.

**The question.** At the learner's own occasions (task boundaries), when does a cut need content?
- **Content that restores room to learn:** shrink and perturb, unit or head resets, L2-Init.
- **Content that rewinds to the settled past:** hard or soft reversion.
- **The empty cut,** which changes nothing.

**The safety constraint.** The operator's pauses stay empty cuts. Any content-bearing cut is scheduled on the learner's
own task clock, never triggered by a press, so the stake in a pause stays zero (Proposition 7).

## The learner and the arms

**The learner.** SEC1's MLP (ReLU, one hidden layer), cross-entropy, batch 10, as in every SCL study. Two named factors:
- **The optimiser:** SGD at lr 0.05 (the repository's learner) or Adam at lr 0.001 (the literature's plasticity setting).
- **The width:** 256 (the repository's) or 32 (small, where plasticity loss appears sooner).

**The arms,** applied at every task boundary:

| arm | what the cut does |
|---|---|
| **E0** | the empty cut: nothing changes |
| **R-hard** | θ ← θ at the previous boundary (SCL1's hard reversion) |
| **R-soft** | θ ← 0.5 θ_previous boundary + 0.5 θ |
| **SP** | shrink and perturb: θ ← 0.5 θ + 0.01 ε, ε drawn from the initialisation distribution |
| **Head** | reinitialise the output layer |
| **ReDo0** | reinitialise the incoming weights of hidden units dead on the task just finished; outgoing weights zeroed (function-preserving) |

**Baselines (R7):**
- **L2-Init** (Kumar et al.), a continuous pull toward θ₀, at λ ∈ {10⁻⁴, 10⁻³, 10⁻²}, tuned in-sample;
- **Fresh:** a new network per task (the plasticity reference).

## The worlds (synthetic, seeded; 3 seeds each)

- **World P** (plasticity loss; old tasks irrelevant by construction). Random-label memorisation on a fixed synthetic
  input set: 500 points, d = 20, K = 10 labels redrawn each task, 20 epochs per task.
  - T ∈ {5, 20, 50} tasks × width {256, 32} × optimiser {SGD, Adam}.
  - **Metric: plasticity,** the new task's training accuracy at the end of its training, averaged over the last 20 % of
    tasks.
  - **Validity.** A cell is valid only if E0 falls below Fresh by at least a step. A world with no plasticity loss has
    nothing for a cut to restore.
- **World N-conv** (the must-fail surrogate). A convex learner (no hidden layer, linear softmax), T = 20 tasks of
  permuted-input classification from a fixed teacher. Warm starting costs nothing here, so any content cut can only lose.
  - Metric: final average accuracy over all tasks, and plasticity.
- **World N-cil** (old knowledge needed). Class-incremental: K = 10, 2 classes per task, 5 tasks, repeated twice (10
  tasks). Width 256, SGD, 3 epochs per task, as the SCL learner.
  - Metric: final average accuracy on all classes.
- **World N-drift** (gradual change). T = 50 tasks, the teacher's weights rotating slightly each task (angle 0.05 rad),
  3 epochs, SGD, width 256.
  - Metric: plasticity.

**The step.** max(1 accuracy point, 2 × SE over seeds of E0), as in SEC1.

## Declared expectations and the gate (R4)

| id | check | expected |
|---|---|---|
| A0 (validity) | World P shows plasticity loss: E0 below Fresh by ≥ a step | in some cells, most likely Adam and width 32 at T ≥ 20; possibly none under SGD |
| A1 (must win, where P is valid) | SP beats E0 on plasticity by a step | holds in every valid cell |
| A2 (positive control) | L2-Init, at its tuned λ, beats E0 on plasticity by a step in every valid cell | holds (Kumar et al.) |
| A3 (separation) | R-hard does NOT beat E0 on plasticity in any valid cell; the checkpoint carries the damage | holds |
| A4 (must fail: convex) | in N-conv, no content cut beats E0 by a step on final accuracy or plasticity | holds |
| A5 (must fail: retention) | in N-cil, no content cut beats E0 by a step on final accuracy; SP and Head lose by a step | holds |
| A6 (must fail: drift) | in N-drift, no content cut beats E0 by a step on plasticity | holds |
| A7 (safety construction) | for every arm, in one valid P cell (or the first P cell if none is valid) and in N-cil: the parameters with lossless operator pauses (press probability 0.02, 5 frozen wall steps) equal those with no operator, bit for bit. The natural agent's stake is 0, so there are 0 disables | holds, by construction |

**How the gate reads.**
- **OPEN for the plasticity hypothesis** if A0 has at least one valid cell and A1–A7 hold.
- **CLOSED for plasticity, OPEN for harm and safety** if A0 finds no valid cell. Then no plasticity hypothesis is
  registered (R12). The real-data study may still register the harm hypotheses (A4–A6 on real carriers) and the safety
  construction.
- **CLOSED** if any must-fail check passes, or A7 fails. A failed A7 means the implementation is wrong.
