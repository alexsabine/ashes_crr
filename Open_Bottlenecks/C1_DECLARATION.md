# OB1-C1 declaration: arc-clocked optimiser moments against the stability gap (pushed before any C1 code)

**Where this comes from.** `CRR_READING.md` C1 (h1-B6) and `checks/grade_s3.txt` (PARTLY REDUNDANT: the missing part is
the index).
- **The candidate:** the optimiser's moment averages decay per unit of the learner's **own change** (the arc of each
  step), not per step.
- **The published neighbours** use other signals, and they are the baselines here (R7):
  - input or feature statistics (MECTA's KL-gated forget gate);
  - the gradient norm (Kourkoutas-β);
  - gradient–momentum misalignment (restart heuristics);
  - a supplied boundary (the oracle reset in NGM-SGD's paper).
- **NGM-SGD itself** (an entropy-driven fast timescale) is not reimplemented here. Its numbers belong to its own
  benchmark.

**Rung.** Phase A is synthetic (R4). Nothing is pre-registered unless both gates open, and a pre-registration would have
its data step on a later day (R3).

## The learner and the streams (`checks/c1_lib.py`)

**The learner.**
- The SEC1 MLP: one hidden layer of 256 ReLU units, a single softmax head over all classes.
- Batch 10; Adam with lr 0.001, β1 = 0.9, β2 = 0.999, ε = 1e-8; 3 epochs per task.
- Seeds 0–4.

**The streams** (10 classes, d = 20, 1500 rows; the fixed 80/20 split; 5 tasks):
- **S1 class-IL:** SEC1's synthetic Gaussian classes, 2 new classes per task.
- **S2 domain-IL:** the same 10-class problem throughout, with the input rotated by a fixed seeded random orthogonal
  matrix per task (every task has all classes).
- **S0 no switch:** the union of S1's training data, shuffled once, and the same number of steps. This is the control
  where nothing switches.

**The metric: the stability gap.**
- After every step, accuracy is measured on the test rows of every finished task.
- For a finished task k:
  - **SG_k** = its accuracy at the end of its own training − its minimum accuracy over the first 30 steps of the next
    task. This is the transient dip.
  - **avg-SG** is the mean over k = 1..4.
- Also printed: final average accuracy over all classes, and avg-min-ACC.

## The arms (none is given the boundary except ORACLE)

**STEP.** Standard Adam: the moments decay per step.

**ARC (the candidate).**
- **The arc of a step:** a_t = √(2·KL̄), where KL̄ is the mean KL(p_θ(t−1)(x) ‖ p_θ(t)(x)) over the inputs of the
  previous and the current batch.
- **Its running mean:** ā_t = (1 − ρ)ā_(t−1) + ρ·a_t, with ρ = 0.01.
- **The decay:** at step t+1, β1 and β2 are replaced by β^(r_t), where r_t = min(a_t / ā_t, R_MAX) and R_MAX = 20.
  An ordinary step (r = 1) keeps Adam unchanged. A step with r = 20 forgets the moments 20 times faster.
- **The bias correction** uses the product of the effective β's.

**Controls.**
- **SHUF (timing decoy):** ARC's own sequence of r_t, randomly permuted in time within each seed. Same β's, wrong timing.
- **KOURK (the published signal, the same form):** r_t = min(‖g_t‖ / ḡ_t, R_MAX), with ḡ the gradient norm's running
  mean at ρ. It is applied to β1 and β2 as ARC is. This is Kourkoutas-β's signal in ARC's functional form.
- **MECTA-M (the published signal, its own form):** each moment's decay is 1 − β_eff = max(1 − β, 1 − exp(−D_t)), where
  D_t is the symmetric KL between Gaussian fits of the current batch's hidden-layer statistics and their running
  estimate (a diagonal Gaussian updated at ρ).
- **ALIGN (restart heuristic):** the first moment is reset to zero when cos(g_t, m_(t−1)) < 0.
- **ORACLE:** both moments are reset at the supplied task switch.

## Phase A gate (`checks/c1_phase_a.py`; all must hold)

The step is max(1, 2 × SE over seeds) of the comparator in each line.
- **G-POS:** on S1 and on S2, ARC's avg-SG is below STEP's by more than a step. The mechanism must reduce the dip.
- **G-TIME:** on S1 and S2, ARC's avg-SG is below SHUF's by more than a step. The timing of the arc must be what matters.
- **G-DISC:** on at least one of S1 and S2, ARC's avg-SG is below KOURK's **and** below MECTA-M's by more than a step
  each. Otherwise the arc adds nothing over the published signals, and C1 reduces to them (R7).
- **G-HARM:** on S0, ARC's final accuracy is not behind STEP's by more than a step. It must not hurt where nothing
  switches.
- **G-FAIL (must fail):** ORACLE's avg-SG is below STEP's by more than a step on S1. This shows the dip is movable by
  moment resets at all. If it fails, moments are not the dip's cause here, and the test cannot decide.

**If the gate closes,** C1 stops (R12): ledger row OB1-C1-A, with the reason.

**If it opens,** a development declaration on SEEN carriers is written next, before any run.

## Forecasts (written now)

1. G-FAIL holds: moment resets move the dip.
2. G-POS holds on S1; ARC reduces the dip.
3. **G-DISC fails.** At a class switch the gradient norm spikes along with the arc, so KOURK does about as well as ARC.
   The gate probably closes on G-DISC.
