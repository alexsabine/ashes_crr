# SEC7 development declaration: the clipped SEC on a stream where the criterion can fail (pushed before any SEC7 code)

**The request.** Prompt-log entry 257: "We should then run more tests on sec4". This is P2 of `Applied_Suite/PROGRAMME.md`.

**Why SEC7 exists.**
- P1 (`SEC_Analysis/WHY_SEC4_WORKED.md`) found that the SEC family's criterion is met by a must-fail control. A learner
  frozen after task 1 (M6) is not behind the tuned λ on 24 of 30 held-out carriers.
  - The cause: the frozen loader ranks the classes by count, and SEC1's tasks are consecutive label pairs. So task 1 always
    holds the two most frequent classes, and final raw accuracy on a stratified test set rewards keeping them.
  - 19 of the 30 are floor-bound.
- SEC6 (hashed at 1bb1870) replicates SEC4-1 on that stream unchanged, as a replication must, and carries the gate
  SEC6-G.
- **SEC7 asks the question SEC6 cannot:** is the clipped SEC tuning-free on a stream where a learner that stops learning
  cannot pass?
- **What SEC7 is not.** It is not a replication of SEC4-1: the stream and the metric differ. A pass here is a new
  PASS-0 or PASS-1, never a PASS-2 for SEC4-1.

## What changes, and nothing else (fixed now)

1. **Class order.** After SCL3's loader and SEC1's class rule (unchanged), the K used labels are relabelled by a seeded
   permutation, `perm = numpy.random.default_rng([20261002, openml_id]).permutation(K)`. SEC1's tasks are then consecutive
   pairs of the permuted labels, so task 1 is two classes drawn at random, not the two largest. The permutation is fixed
   per carrier: the same for every seed and every arm.
2. **The metric.**
   - The primary metric is **balanced accuracy**: the mean over the K classes of per-class recall on the test set, × 100.
     Its chance level is 100/K.
   - Raw accuracy is recorded and printed beside it.
   - The tuned λ, the tuned clipped λ, the transferred λ and the 3-point sweep's best are all chosen on balanced accuracy.
3. **The learner's loop.** It is re-implemented so that it records per-class recall.
   - **D-ID:** with the identity permutation and raw accuracy it must reproduce the pinned `bayes_sec_clip`, `bayes` and
     `fixed` records of SEC4 and SEC5 bit for bit, on seed 0 of at least 4 carriers. It must also reproduce SEC6's `si1c`,
     `ar1b`, `fixed_clip` and `edge` development records on at least 2 carriers.
   - Every arm's mechanics are SEC6's (`runs/sec6/frozen/sec6_score.py`), unchanged.

## The arms (as SEC6, at seeds 0–4)

**The references.**
- **`fixed`:** the tuned λ, on SEC1's two-stage grid, tuned on balanced accuracy.
- **`fixed_clip`:** the tuned clipped λ, on the same grid, with SEC4's clip.

**The arm under test.** `bayes_sec_clip`: the clipped SEC, κ = 0.5, at the primary window, at SEC4's 3 retained window
cells, and at κ ∈ {0.25, 1.0}.

**Beside it.** `bayes_sec` (unguarded SEC), `bayes` (raw Laplace), `eq` (Ω = 1, R7), and SI-1C and AR1-B (SEC6's
published baselines at their SEEN strength).

**The control.** `edge`: P1's M6, the learner frozen after task 1, used as the must-fail control. It is the instrument
gate.

## The development stage (the 30 SEEN carriers of SCL3, SEC3, SEC4 and SEC5; `prereg/sec7/dev_SEC7.txt`)

1. **D-ID,** as above.
2. **D-GATE-7, which decides whether SEC7 can be run at all.** Both conditions must hold on the SEEN carriers:
   - **D-FAIL:** `edge` is behind the tuned λ (balanced accuracy − tuned > −step fails) on more than half of the carriers.
     The instrument can fail.
   - **D-FLOOR:** fewer than a quarter of the carriers are floor-bound under the new metric, where a carrier is
     floor-bound if the tuned λ's balanced accuracy − 100/K < 3 steps.

   If D-GATE-7 closes, **SEC7 stops (R12):** no pre-registration. The finding is recorded: a random class order with
   balanced accuracy does not make the criterion informative on these carriers.
3. **D-RUN** (only if D-GATE-7 is open): every arm on the 30 SEEN carriers, counts printed. **Nothing is chosen from it.**
   Every constant is SEC4's, SEC6's or a paper's.

## The family (metadata only; `studies/sec7/select_carriers.py`)

- **The rule.** SEC5's selection script with SEC4's eligibility rule, unchanged. The suite is OpenML study 445 (IRT
  Diverse Dataset Benchmark), with draw seed 20261002 and a cap of 12.
- **What counts as SEEN.** The records SEEN at the hash, **and** SEC6's twelve carriers (listed in
  `prereg/sec6/PREREG.md`), so that the two families are disjoint.
- **If fewer than 6 are eligible,** SEC7 is NOT RUNNABLE on this family and stops.

## Hypotheses to be registered (if D-GATE-7 opens)

N is the number of scored carriers, and need = ⌈0.75 N⌉. A study with N < 4 is NOT DECIDABLE.

| id | criterion |
|---|---|
| **SEC7-G** (the instrument gate, computed first) | `edge` − tuned λ > −step on at least need carriers means CLOSED: every other row is printed UNINFORMATIVE and capped at PASS-0 |
| **SEC7-1** (primary) | clipped SEC − tuned λ > −step on balanced accuracy, on at least need carriers |
| **SEC7-C** | clipped SEC − tuned clipped λ > −step_c on at least need carriers (gate SEC7-GC as SEC6's) |
| **SEC7-B** | the clipped SEC is not behind the tuned λ on strictly more carriers than SI-1C, AR1-B and raw Laplace each |
| **SEC7-2, SEC7-T, SEC7-P, SEC7-S, SEC7-K** | as SEC6: no divergence; the transferred λ; the 3-point sweep; sensitivity over 5 cells (3 windows and κ ∈ {0.25, 1.0}); compute |

**PASS levels.** As SEC6: PASS-1 only if SEC7-G is OPEN, SEC7-S is not fragile, SEC7-2 passes, and the OTS anchor
completes.

**Timing.** The pre-registration is hashed on 2026-09-30 and its data step is on or after 2026-10-01T00:00Z (R3). Both
stream changes were chosen from P1's reading of SEEN data on 2026-09-30.

## Forecasts (written now)

1. **D-GATE-7 opens.** With a random task 1 and balanced accuracy, a learner frozen after task 1 scores about 2/K of the
   classes' recall and falls behind the tuned λ on most carriers.
2. **SEC7-1 FAILS.** The tuned λ chosen on balanced accuracy is a stronger reference than the old one, and SEC5's failure
   modes (the cap, noisy seeds) remain.
3. **SI-1C is not behind on at least as many carriers as the clipped SEC,** as on SEEN data.

## Amendment 1 (2026-09-30, after the metadata-only selection; no dataset record opened; pushed before any SEC7 code)

**What happened.** `prereg/sec7/carrier_selection.txt` (metadata only) finds only 2 eligible datasets in OpenML study 445
(volcanoes-b4, autoUniv-au7-1100), against the declared minimum of 6. As declared, SEC7 is NOT RUNNABLE on that family.
PMLB is no alternative: SEC4's PMLB selection (`prereg/sec4/carrier_selection_pmlb.txt`) found only 4 eligible, mostly
deprecated copies of SEEN sets.

**The change.** It was made after a metadata count, which is independent of any outcome. SEC7 does not replicate a
family-level claim; it asks a different question (a stream where the criterion can fail). So its carriers need to be
unseen and disjoint from every other study's, not drawn from a new suite.

- **The family becomes** the eligible datasets never opened from OpenML studies 445, 454 and 293, pooled in that order.
  - Eligibility is SEC4's rule, unchanged.
  - SEEN is `data/SEEN.md` today, plus SEC6's twelve, which are excluded explicitly.
  - Studies 454 and 293 contribute only their undrawn eligible datasets. SEC5's twelve and SEC6's twelve are excluded.
- **The draw.** 12, by `default_rng(20261002)` over the sorted eligible ids, as declared.
- **The metadata** of all three suites is re-fetched today into `prereg/sec7/`.
- **Nothing else changes.** The stream, the metric, the arms, D-ID, D-GATE-7, the hypotheses and the forecasts are as
  declared above.
- **D-GATE-7 runs first,** on the 30 SEEN carriers, and still stops SEC7 if it closes.
