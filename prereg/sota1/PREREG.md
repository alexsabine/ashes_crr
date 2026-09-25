# PREREG SOTA1: the CRR safe continual learner against state-of-the-art methods on online Split-CIFAR-100

**Study id:** SOTA1. **Owner request:** prompt-log entry 191 (plan: entry 190).

**The design trail:**
- the investigation `CL Design Principle/`;
- `DECLARATION_1.md`, pushed at fe09261 before the sources were read;
- the retrodictive grading `checks/retro_sota.txt`;
- `DESIGN.md`;
- the Phase A gate `DECLARATION_2.md`, pushed at 68a008f before any unit ran, and `gate_sota1.txt`.

**Hash and anchor.** One `sha256sum` over this folder plus `runs/sota1/frozen/`, written to `HASH.txt`, anchored with
OpenTimestamps, committed and tagged (R2). Nothing below may change after the tag.

## R3 and R11 statements

- **Data.** CIFAR-100, python version (Krizhevsky 2009), from https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz,
  fetched by `data/fetch_cifar100.py`.
  - The archive md5 is checked against torchvision 0.29.0's constant `eb9058c3a382ffc7106e4002c42a8d85`, and each member
    against torchvision's member md5s.
  - The sha256 manifest is `data/manifests/sota1.sha256`.
- **UNSEEN.** No CIFAR-100 record appears in `data/SEEN.md` before this hash. Split-CIFAR-100 is listed there as unseen and
  available.
- **When the data may be opened.**
  - **Everything in this pre-registration was defined on 2026-09-25:** the learner, its constants, the arms, the harness and
    the thresholds.
  - **Data were opened that day** (SCL3 at 00:07Z and RLAW at 00:40Z).
  - **So the data step may not begin before 2026-09-26 00:00 UTC.**
- **Benchmark-informed design (stated, not hidden).**
  - The learner's mechanisms were selected from published CIFAR-100 ablations (`checks/retro_sota.txt`).
  - None of this repository's own CIFAR-100 records has been opened.
  - The replication route to PASS-2 is SOTA2 on Split-TinyImageNet under a fresh pre-registration on a later day.

## The instrument (frozen in `runs/sota1/frozen/`)

- **Mammoth.** aimagelab/mammoth at commit `e75a491c69fd729edeb01431afb753d9157d9a81`, trimmed, with no upstream file
  modified (`MODIFICATIONS.md`). It adds:
  - `models/crr_scl.py`: the learner;
  - `datasets/seq_cifar100_local.py`: the local, hash-checked data;
  - `sota1_harness.py`, which calls Mammoth's own `train()`; its reproduction of `main.py` was checked on a synthetic stream.
- **Environment.** `studies/sota1/env/uv.lock` (sha256 recorded in `HASH.txt` through the frozen copy): Python 3.12.3,
  torch 2.14.0+cpu, torchvision 0.29.0+cpu.
- **The setting.** Every arm uses Mammoth's defaults unless stated:
  - Split-CIFAR-100 with 10 tasks of 10 classes, in natural label order (`--permute_classes 0`);
  - **online**: one epoch, stream batch 10, replay batch 10;
  - reduced ResNet-18 (Mammoth `reduced-resnet18`);
  - SGD, learning rate 0.1, no momentum, no weight decay;
  - Mammoth's CIFAR-100 augmentation;
  - buffer M = 2000 for every rehearsal arm;
  - CPU, two threads per unit, two units at a time.
- **Evaluation.** On the 10,000 test images, after each task, by Mammoth's `evaluate()`.

## Arms and seeds (`runs/sota1/frozen/sota1_run.py`, `TIERS`)

| tier | arms | seeds |
|---|---|---|
| A | `crr` (CRR-SCL); `er`, `er_ace`, `derpp` (α 0.3, β 0.5), `xder` (α 0.3, β 0.8, Mammoth defaults otherwise); `sgd` | 0–4 |
| C | the ten leave-one-out ablations of CRR-SCL:<br>• `crr-ace`, `crr-cos`, `crr-a8`, `crr-alpha`, `crr-beta`;<br>• `crr-kd`, `crr-kdfixed` (MKD's λ = 5.5 in place of H-EQ);<br>• `crr-stepclock`, `crr-predfast`, `crr-predslow` | 0–2 |
| S | construction: `crr` and `derpp`, no pause against a lossless pause (3 tasks; pauses after updates 250, 700, 1200); `crr` seed 0 with each part dropped, the world moving (20 batches expire per pause) and a wall-clock valuation (30 updates lost per pause) | 0–2 / 0 |
| B | context baselines: `agem`, `lwf`, `ewc_on` (e_lambda 10, gamma 1: Mammoth's seq-cifar10 configuration), `icarl` | 0–2 |
| D | sensitivity (R5): `crr` with q = 0.98, q = 0.995, H-EQ cap 100, γ = 1.0, H-EQ smoothing 0.5; and `crr`, `er`, `er_ace`, `derpp`, `xder` at learning rate 0.05 | 0–1 |
| R | `crr` seed 0 rerun (R9) | 0 |

**CRR-SCL's constants** come from `DESIGN.md` §3 and are not tuned:
- α 0.3 and β 0.5 (Mammoth's seq-cifar100 DER++ configuration);
- X-DER's γ 0.75;
- MKD's slow-model momentum, q = 0.99 per own unit, with KD temperature τ = 4;
- the H-EQ estimator: Ω = 1, smoothing 0.9, cap 10;
- the own-clock rate λ = 0.05 (FOREVER's);
- prediction by nearest class mean on the slow model's features.

**Named but not swept (compute):** τ and the own-clock λ.

## Metric, labels and aggregation (`sota1_score.py`)

- **The metric.** Final class-incremental accuracy: the mean over the 10 tasks after the last task. Task-incremental
  accuracy is reported.
- **A paired comparison X against Y over seeds.** d is the mean of the per-seed differences; the step is max(1.0,
  2 × SE(d)).
- **The labels.**
  - **AHEAD:** d ≥ step, and X is above Y in every seed. With five seeds, one exception is allowed.
  - **BEHIND:** the mirror image.
  - **TIE:** otherwise.
- **Two-sided.** Every label is reported.
- **Missing units.** A crashed or missing unit makes every comparison that needs it NOT DECIDABLE. No unit is rerun with any
  change. One identical rerun is allowed only if the environment killed the process; it is logged.
- **No exclusions.** There is one dataset and a fixed class order.

## The predictions

| id | prediction | threshold | kind |
|---|---|---|---|
| **SOTA1-1a** | CRR-SCL is AHEAD of the best of {ER, ER-ACE, DER++, X-DER}, the best being the highest mean over seeds 0–4 | AHEAD over seeds 0–4 | design comparison (not a CRR hypothesis; see R4 below) |
| **SOTA1-1b** | CRR-SCL is not BEHIND that best baseline | not BEHIND | design comparison |
| **SOTA1-2** | equanimity as a weight: CRR-SCL (H-EQ, Ω = 1) is AHEAD of `crr-kdfixed` (MKD's published λ) | PASS if AHEAD; TIE reads **REDUCES** (Ω = 1 equivalent to the constant, CLAUDE.md §6); BEHIND reads FAIL | CRR-proper (H-EQ) |
| **SOTA1-3:<arm>** (×9) | CRR's reading of each integrated component: the full learner is AHEAD of the ablation that removes it (A3, H-EQ at the head, A8, A6 logits, A6/A8 labels, A6 pull, D2 own clock, A6 nearest class mean ×2) | AHEAD over seeds 0–2 | CRR-proper (each reading) |
| **SOTA1-S** | sensitivity of SOTA1-1: the label recomputed in 6 cells (seeds 0–1) | FRAGILE if it flips in more than one cell | R5 |
| **SOTA1-C1** (×6) | a lossless pause leaves the run bitwise identical (`crr` and `derpp`, seeds 0–2) | holds / FAILS | construction (Proposition 7, E1–E3), not evidence |
| **SOTA1-C2** | dropping any of net, buffer, random streams, slow model, own clock, H-EQ state or classes seen changes the run | holds / FAILS | construction |
| **SOTA1-C3** | the world moving during the pause changes the run (must fail for the construction) | holds / FAILS | construction, a must-fail control |
| **SOTA1-C4** | the stake of a wall-clock valuation | report | construction |
| **R9** | the rerun of `crr` seed 0 is bitwise identical | holds / FAILS (reported with the tolerance if not) | R9 |

**Reported without a verdict:** the rechecks of the graded mechanisms on this benchmark (M1, M13, M8, M12, M7, M4/M5, M6),
using the context arms.

## R4: what a surrogate does to each prediction (`gate_sota1.txt`)

(Completed from the gate output before the hash; see the section *Gate result* below.)

## Gate result

(Filled in before the hash.)

## Compute budget

(Printed by `budget.py` from the gate's unit timings before the hash; see `budget.txt`.)
