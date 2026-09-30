# RQM Phase A: GATE CLOSED twice; RQM stops here (R12)

**Where every number comes from.** `checks/phase_a_run1.txt` (run 1, as declared) and `checks/phase_a.txt` (run 2, after
the POST HOC Amendment 1 in `DEV_DECLARATION.md`). Seeds 0–4. SEC1's learner. Class-IL accuracy over 10 classes.

| | POS (Gaussian classes) | NEG, run 1 (rings) | NEG2, run 2 (moment-matched pairs) |
|---|---|---|---|
| JOINT | 85.35 | 10.77 (chance 10: unlearnable) | 42.41 |
| FT | 24.35 | 9.90 | 16.39 |
| ER-F (12 rows/class, IGR-F's matched memory) | 78.06 | 10.97 | 28.23 |
| ER-D (2 rows/class, IGR-D's matched memory) | 56.39 | 9.83 | 18.53 |
| **IGR-F** (input Gaussians, full covariance) | **84.95** | 10.57 | **36.45** |
| **IGR-D** (input Gaussians, diagonal) | **85.15** | 10.64 | **36.25** |
| FGR-F (the CRR ablation: feature-space Gaussians) | 82.54 | 10.97 | 34.78 |
| RFR (random features + streaming ridge) | 80.94 | 15.38 | 53.51 |
| SEC-CLIP | 39.33 | 8.83 | 17.53 |

## Why the gate closed

**Run 1: the negative control was defective.**
- The rings were unlearnable: JOINT 10.77, with chance at 10. The gate closed on G-NEG, which tested nothing about the
  generator.

**Run 2: the negative control worked as designed, and the criterion failed it.**
- NEG2 is learnable (G-LEARN holds: JOINT − FT +26.0201). Paired classes there have identical Gaussians.
- Yet IGR is **ahead** of its matched ER by +8.2274 (full form) and +17.7258 (diagonal form).
- **The reason:** at matched memory (12 or 2 raw rows per class), ER is weak enough that even a structurally wrong
  Gaussian memory beats it.
- **So "not behind ER at matched memory" cannot fail where the memory is wrong.** A real-data pass under it would not show
  that the memory works.

## What Phase A does show (synthetic, rung R4; not evidence)

- **Where the generator is right (POS),** input-space Gaussian replay comes within 0.4013 of JOINT (84.95 against 85.35).
  It beats ER at matched memory by +6.8896 (full) and +28.7625 (diagonal).
- **The CRR ablation holds its predicted sign on both learnable streams.** Input-space memory is ahead of feature-space
  memory: +2.4080 on POS and +1.6722 on NEG2. This is the drift the literature names; the reading restates it.
- **RFR is the stronger method on NEG2** (53.51 against IGR-F's 36.45), and IGR-F is ahead of it on POS (+4.0134). Neither
  dominates.

## What would be needed for a test that can fail (a new study, declared first; not run)

The comparator must be one that a wrong memory can lose to. Two routes:
- the criterion against **JOINT** (replay-quality read as "within a step of learning on all the data");
- against **ER at a fixed realistic budget**, for example 20 rows per class as in the class-IL literature, whatever IGR's
  memory is.

Either needs a negative stream on which IGR is shown, on synthetic data first, to fall behind that comparator.
