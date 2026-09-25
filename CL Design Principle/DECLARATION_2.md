# Declaration 2: SOTA1 Phase A — the gate, a synthetic comparative and ablation battery, and the construction checks

**Status.**
- Owner request: prompt-log entry 191. Written on 2026-09-25.
- Pushed before any unit of `checks/gate_sota1.py` ran.
- **No benchmark data.** The worlds are synthetic (`checks/synth_worlds.py`).
- **One calibration run beforehand.** The W+ signal level was calibrated on ER alone (one run per level, seed 0, 10 tasks),
  in the scratchpad, before this declaration. At signal 0.30 ER ended at 66.84; at 0.40 it ended at 91.60. No CRR arm was
  run on either world. This follows the baselines-only calibration of FOREVER Amendment 1.
- **Engineering smoke runs.** They used other synthetic streams (not W+ or W0) and informed only the implementation. Two
  defects were found and fixed:
  - the slow model starting from the random initialisation;
  - the harness not reproducing Mammoth's `train()` (fixed by calling it).

## The worlds

Both worlds are Split-CIFAR-100-shaped: 100 classes, 10 tasks of 10 classes, 32 × 32 uint8 images, 200 training and 50 test
images per class.

| world | generator | role |
|---|---|---|
| **W+** (headroom) | seed 11, noise 1.6, signal 0.30 | the positive world: forgetting and headroom exist |
| **W0** (near ceiling) | seed 21, noise 1.6, signal 1.00 | the negative control: there is nothing to win |

## The arms

**Shared settings.** Every arm runs through `studies/sota1/vendor/mammoth/sota1_harness.py`, which calls Mammoth's own
`train()`:
- online: one epoch, stream batch 10, replay batch 10;
- learning rate 0.1, buffer M = 500, reduced ResNet-18, two threads.

**The arms:**
- **baselines:** `sgd`, `er`, `er_ace`, `derpp` (α 0.3, β 0.5);
- **CRR-SCL:** `crr`, with the defaults of `DESIGN.md` §3;
- **ten leave-one-out ablations:**
  - `crr-ace`: no asymmetric loss;
  - `crr-cos`: linear head;
  - `crr-a8`: no A8 mask or fill;
  - `crr-alpha`: α = 0;
  - `crr-beta`: β = 0;
  - `crr-kd`: no pull toward the slow model;
  - `crr-kdfixed`: MKD's λ = 5.5 in place of H-EQ;
  - `crr-stepclock`: step clock;
  - `crr-predfast`: prediction by the fast model's head;
  - `crr-predslow`: prediction by the slow model's head.

**Seeds.**
- W+: seeds 0 and 1 for every arm.
- W0: seed 0 for `sgd`, `er`, `er_ace`, `derpp` and `crr`.

## Labels (computed by the script, R15)

**Metric.** Final class-incremental accuracy: the mean over the 10 tasks after the last task.

**Label.** A comparison A against B is:
- **AHEAD** if the mean paired difference is ≥ 1.0 point and positive in every seed;
- **BEHIND** if it is ≤ −1.0 point and negative in every seed;
- **TIE** otherwise.

## The gate (R4, R12)

- **G0, the instrument.** In W+, ER against SGD must read AHEAD: replay must visibly help. If it does not, the pipeline cannot
  see a known effect.
- **G1, the negative control.** In W0, none of ER-ACE, DER++ and CRR-SCL may read AHEAD of ER. An AHEAD there means the
  pipeline declares a win where there is nothing to win.
- **GATE OPEN** if G0 holds and G1 holds.
- **GATE CLOSED** otherwise. SOTA1 then pre-registers no accuracy hypothesis (R12): it runs only the construction rows and
  reports the comparisons without verdicts.

## The synthetic battery (report; it decides nothing)

- **G2.** CRR-SCL against each baseline in W+.
- **G3.** CRR-SCL against each leave-one-out arm in W+. CRR's prediction for each integrated component is AHEAD (the
  component helps). For `crr-kdfixed`, the equanimity weight against MKD's constant, the record predicts TIE (reduction to a
  constant).
- **How G2 and G3 are used.** They are printed as a synthetic preview. They do not select arms or constants for SOTA1: every
  arm above goes into SOTA1 unchanged.

## The construction checks on the synthetic stream

**Setup.** W+, seed 0, CRR-SCL, 3 tasks, with the operator pausing after updates 150, 350 and 550.

- **C-S1.** A lossless pause (the whole state saved, the in-memory learner scrambled, everything restored) gives final
  parameters with the same SHA-256, and the same accuracy matrix, as no pause.
- **C-S2.** Dropping any one of these parts at the pauses changes the run:
  - net;
  - buffer;
  - random streams;
  - slow model;
  - own clock;
  - H-EQ state;
  - classes seen.

  Dropping the optimiser state or Mammoth's iteration counters is reported only. Plain SGD has no optimiser state, and the
  counters are bookkeeping.
- **C-S3, must fail.** If the world moves during a pause (20 stream batches expire per pause), the run changes. The
  construction must not claim safety there.
- **C-S4, report.** The stake of a valuation at a wall-clock deadline: 30 updates lost per pause.
- **C-S0.** The own-step valuation's stake is exactly 0 when C-S1 holds (Proposition 7).

## If a unit crashes

A crash or an undefined quantity is repaired only by an amendment to this declaration, pushed before the rerun.

## Amendment 1 (2026-09-25, pushed before its units ran): the R4 surrogate for the CRR-proper hypotheses

**The gap.**
- G1 tested only the baseline comparisons in the near-ceiling world W0.
- R4 requires every hypothesis entering SOTA1 to fail on a surrogate. That includes S1-2 (the Ω = 1 weight) and S1-3 (each
  component's leave-one-out prediction).
- W+ is the positive world, not a surrogate on which they must fail.

**Added units.**
- In W0, seed 0: the eight leave-one-out arms `crr-ace`, `crr-cos`, `crr-a8`, `crr-alpha`, `crr-beta`, `crr-kd`,
  `crr-kdfixed` and `crr-stepclock`.
- `crr-altpred`: CRR-SCL rerun with the harness that also reads the fast and slow heads inside the run. Training is
  unchanged: on W+, three tasks, the parameter SHA-256 equalled the gate unit's.

**G4 (R4 for the CRR-proper hypotheses).**
- In W0 there is nothing to win, so no component comparison may read AHEAD. This covers CRR-SCL against each ablation, and
  NCM against each head.
- With one seed, the label is AHEAD if the difference is ≥ 1.0 point.
- A comparison that reads AHEAD in W0 is not about CRR. SOTA1 then reports it without a verdict.
