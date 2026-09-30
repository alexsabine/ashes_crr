# OB1-C3 Phase A: the result (GATE CLOSED; C3 stops)

**What was tested** (`C3_DECLARATION.md`, 38c87e3). When to consolidate (anchor and importance of an online-EWC penalty)
in a boundary-free stream. The arms were CRR's arc, TIDE's chord, a loss CUSUM, a count, random times, never, and the
oracle. Output: `checks/c3_phase_a.txt`, pinned; the rerun is byte-identical.

## The gate (BLURRY stream)

| condition | result |
|---|---|
| G-MATTER: ORACLE ahead of NONE by more than a step | **FAILS** (+0.7224, step 1.0000) |
| G-TIMING: ORACLE ahead of RAND by more than a step | **FAILS** (+0.1338, step 1.0000) |

**C3 GATE CLOSED.** The arc-against-chord contest is not scored. C3 stops (R12). Ledger row OB1-C3-A.

## Why it closed

In this stream, consolidating barely helps, so when to consolidate cannot matter.
- Final accuracy over the five domains is 28–30 % for every arm, NONE included. ORACLE's λ was the best of the declared
  grid on the calibration seed: 27.02 to 27.83 across λ.
- The one-hidden-layer MLP forgets the rotated domains almost completely, and a diagonal-Fisher penalty on a rotation
  that mixes every input coordinate does not hold them.
- The test was declared in a setting where the thing it compares has no effect. That is a design failure of the
  declaration, and it is recorded as such.

## Reported beside the closed gate (not scored; synthetic; not evidence)

- **ARC's consolidation times track the hidden domain switches, with no boundary information.** On BLURRY, ARC fired at
  steps such as 77, 148, 221, 291 and 71, 143, 218, 289, where the true switches are 72, 144, 216 and 288. On ABRUPT, the
  lag was 1–14 steps. CHORD and LOSS fired later and less regularly.
  - As a **change detector**, the learner's own accumulated arc lined up with the switches better than the chord or
    the loss surprise.
  - Change detection from the learner's own signals is published, and this does not show it improves anything
    downstream, because consolidation itself did nothing here.
- **The differences** (ARC − CHORD +0.4950 on BLURRY, +0.0401 on ABRUPT) are inside a step, and the gate is closed.

## What would be needed (a new declaration; not run)

- **A setting where consolidation matters:** a learner and stream on which ORACLE is well ahead of NONE and of RAND.
  For example, domains that share structure (permuted subsets, or input shifts that a diagonal penalty can protect), or
  a stronger consolidation action (a frozen snapshot, or a new head per consolidation).
- **The arc's alignment with switches is the one sign here worth a follow-up.** It would be tested as a boundary
  detector, against published detectors (the learned drift detectors and data-side tests in the C3 dossier), before any
  downstream claim.
