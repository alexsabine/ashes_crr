# SEC4 guard development: declaration (pushed before any variant is run)

**Status.**
- **The request.** Owner request: prompt-log entry 228 (2026-09-28): "work on making this more robust as planned above and
  repeat the tests".
- **What this file covers.** The development stage of study SEC4. It uses SEEN data only. It is pushed before
  `studies/sec4/guard_dev.py` runs, and it will be covered by SEC4's pre-registration hash.

## What is being made robust

**The failure.** SEC (the Laplace weight w = 1/2 on a secant-calibrated Fisher) failed by divergence on three unseen
carriers: cnae-9 (SCL3), dionis and fabert (SEC3). One or two seeds in five fell to 0–12.5 % accuracy. On all three the
calibrated penalty crossed the explicit-Euler stability edge of the penalty step: lr · w · max_i imp_i ≥ 1, with lr = 0.05
and w = 1/2.

**SEC3's guard (G-RAW)** fell back to raw Laplace for the task. Its gate closed on cnae-9: the guarded mean was −1.9792
against a step of 1.7305. On SEC3's family it was 6/6, but only as a post hoc report.

## The three candidate guards (fixed now)

The margin is m = lr · w · max_i imp_i, computed at each task start from the calibrated importance.

| id | rule when the bound is reached | constant |
|---|---|---|
| G-RAW | m ≥ 1: use the raw Laplace importance for the task (SEC3's guard) | bound 1 |
| G-CLIP | clip every coordinate: imp_i ← min(imp_i, κ / (lr · w)) | κ = 0.5 |
| G-SCALE | if m ≥ κ, rescale the whole importance: imp ← imp · κ / m (shape kept) | κ = 0.5 |

- **When they act.** Each guard acts only at a task start. Below its bound every guard leaves SEC's code path unchanged.
- **Why κ = 0.5.** It is half the stability edge, one factor of 2 inside it. It is fixed now and not tuned.

## The development data

**The carriers.** The 16 SEEN carriers that SEC has already been scored on:
- SCL3's 10: cnae-9, eucalyptus, first-order-theorem-proving, GesturePhaseSegmentationProcessed, har, isolet, MiceProtein,
  semeion, steel-plates-fault, wall-robot-navigation;
- SEC3's 6: covertype, dionis, fabert, helena, jannis, volkert.

**The baselines.** The tuned λ and the resolvable step of each carrier are read from their pinned results
(`runs/scl3/results_*.jsonl`, `runs/sec3/results_*.jsonl`). Nothing is re-tuned.

**The runs.** Each variant runs at seeds 0–4 through the same learner, with the same data split.

## The selection rule and the development gate (fixed now)

1. **Score.** For each variant, count the carriers where the guarded mean is not behind the tuned λ by a step.
2. **Choose.** Take the variant with the largest count.
   - Ties are broken by the fewest firings on carriers where unguarded SEC was already not behind.
   - A further tie is broken in the order G-CLIP, G-SCALE, G-RAW.
3. **The development gate D-GATE opens if all three hold:**
   - **D-COUNT.** The chosen variant is not behind on at least ⌈0.75 × 16⌉ = 12 of the 16 SEEN carriers.
   - **D-ID.** On SEC1's synthetic stream, with the bound at +∞, the chosen variant equals unguarded SEC bit for bit.
   - **D-FIXES.** The chosen variant is not behind on at least 2 of the 3 divergence carriers (cnae-9, dionis, fabert).
4. **If D-GATE closes,** SEC4 stops here (R12). No unseen data are opened and the ledger records a development-gate row.

**What it means if the gate opens.** The chosen guard is then fixed. SEC4's pre-registration names it, and tests it on a
third unseen family on a later day (R3: it is chosen on SEEN data on 2026-09-28, so no unseen carrier is opened before
2026-09-29 00:00 UTC). A choice made on SEEN data is development, not evidence: only the third family can count.
