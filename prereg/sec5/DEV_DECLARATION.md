# SEC5: declaration (pushed before any SEC5 code runs, before any suite metadata is fetched, before any data)

**Status.**
- **The request.** Owner request, prompt-log entry 238 (2026-09-29): "Yes, please run a new SEC test in full. Thank you.
  Ensure you record every decision carefully and provide a full output of findings. Use the CRR to fine-tune the approach
  as required."
- **What came before.** SEC4 (`reports/sec4.md`): the clipped SEC (κ = 0.5) was not behind the tuned λ on 6/6 carriers of a
  third unseen family, with no divergence and no flips: SEC4-1 PASS-1, the record's first. The report named why it is not
  PASS-2: one family, and κ never swept.
- **This file** fixes the design of SEC5, the CRR-guided development stage and its gate, and the rule that picks the
  fourth family. It is covered by SEC5's pre-registration hash.

## Two parts, kept apart (decision; AGENT_LOG 177)

**Part R: the replication (primary).** SEC4's clipped SEC, **unchanged**: the frozen code of `runs/sec4/frozen/`
(byte copies), κ = 0.5, the same learner, windows, grid, step and thresholds, on a **fourth unseen family**, under a fresh
pre-registration on a later day. If its primary row is PASS-1 here, SEC4-1 and SEC5-1 together are the ledger's first
PASS-2 (CLAUDE.md §7), each row referencing the other.

**Part C: the CRR-guided refinement (secondary).** The owner asked that CRR be used to fine-tune the approach. Any change
to the rule is a new method: it cannot be the replication, and a method chosen on SEEN data cannot reach PASS-2 in the
study that first tests it. So the refinement is developed on SEEN carriers today, gated, and, only if its gate opens,
tested beside Part R on the same unseen family as a separately scored arm.

- **Rejected: fine-tuning the primary arm.** It would forfeit the replication (the only route to PASS-2), and a variant
  chosen on SEEN data the same day as its test would break R3.
- **Rejected: tuning κ with CRR.** CRR fixes no value of κ (A6's strength is bounded but not fixed); choosing κ on SEEN
  data is tuning, and the claim under test is that SEC needs none. κ is swept as sensitivity instead (below).

## Part R: what is added to SEC4's design

**The κ sweep (the missing sensitivity; R5).** The clip at κ ∈ {0.25, 1.0}, one factor of 2 either side of 0.5, at the
primary window. κ = 1 is the explicit-Euler stability edge itself. These cells join SEC4's three retained window cells:
**five sensitivity cells per carrier.** More than one flip of SEC5-1's per-carrier "not behind" across all of them
reads FRAGILE, as in SEC4.

Nothing else in Part R changes: the tuned λ (SEC1's 17-configuration two-stage grid, tuned in-sample on the scored
seeds), the resolvable step max(1, 2 × SE), seeds 0–4, need = ⌈0.75 N⌉, MIN_N = 4, DIV_FRAC = 0.5, the 3-point sweep
{1, 30, 1000}, the transferred λ (leave-one-carrier-out, snapped to the coarse grid), the loader, the class rule (floor 40,
5000-row cap, seed 777, K lowered by two until the floor holds), the exclusion rule (K < 4).

## Part C: what CRR says, and the candidates (fixed now)

**The reading.** SEC's past importance is a **sum** over settled tasks: imp ← imp + n_task · s · F_task. On the six
carriers where unguarded SEC diverged (cnae-9, dionis, fabert; anneal, cardiotocography, synthetic_control) the summed,
calibrated importance crossed the stability edge lr · w · max imp ≥ 1. `theory/CRR.md` A6: "The strength is bounded:
regeneration returns a reweighted content, never an accumulated count (a system that re-counts its past stops cutting)",
with MaxEnt weights over occasions normalised to one. Read on SEC: the past term should be a **weighted mean** of the
settled tasks' importances, not their sum. With no history constraint the MaxEnt weights are uniform (P2 at β = 0, P3 at
q → 1); CRR does not fix β or q, so uniform weights are the zero-knob choice, not a CRR prediction.

**Prior art (R7, R10; `docs/citations/sec5_2026-09-29.md`).** Online EWC (Schwarz et al., arXiv:1805.06370 v2) names the
same problem ("the accumulation of Fisher regularisers can over-constrain the network parameters") and decays the running
Fisher by a hyperparameter γ < 1. The candidate below is a tuning-free member of that family, not a new idea.

| id | the past importance at a task start | guard |
|---|---|---|
| **A6-MEAN** | (Σ over settled tasks of n_m · s_m · F_m) / (number of settled tasks), then / n_task as in SEC | none |
| **A6-MEAN-CLIP** | as A6-MEAN | SEC4's clip at κ = 0.5 |

- **Identity (D-ID).** With one settled task the mean is the sum, so both candidates equal SEC (and the clip equals SEC4's)
  on a two-task stream. Checked in code: with the divisor forced to 1, A6-MEAN equals SEC1's `bayes_sec` bit for bit and
  A6-MEAN-CLIP equals SEC4's clip bit for bit, on SEC1's synthetic stream, seeds 0–4.
- **No new constant.** The divisor is the count of settled tasks. Nothing is tuned.

**The development data (SEEN only).** The 22 carriers SEC has been scored on: SCL3's 10, SEC3's 6, SEC4's 6 (JapaneseVowels,
anneal, artificial-characters, cardiotocography, gas-drift, synthetic_control). Tuned λ, its accuracy and the step are read
from the pinned results (`runs/scl3`, `runs/sec3`, `runs/sec4`); nothing is re-tuned. SEC4's clip is re-run beside the
candidates on the same splits and seeds, as the reference.

**The selection rule.** For each candidate, count the carriers not behind the tuned λ by a step. The chosen candidate has
the largest count; ties go to fewer guard firings, then to the order A6-MEAN, A6-MEAN-CLIP (the one without an ad hoc
guard first).

**The development gate D-GATE-C (all must hold).**
- **D-COUNT.** Not behind on at least ⌈0.75 × 22⌉ = 17 of the 22.
- **D-ID.** As above, bit for bit.
- **D-FIXES.** Not behind on at least 4 of the 6 divergence carriers.
- **D-ADDS.** Not behind on at least as many of the 22 as SEC4's clip, **and** the mean over the 22 of (candidate − clip)
  is ≥ 0. A candidate that does worse than the clip on SEEN data adds nothing to test.

**If D-GATE-C closes,** Part C stops (R12): no A6 arm is run on the unseen family, and the ledger gets one development row.
**If it opens,** the chosen candidate is pre-registered as SEC5-C (its own row, "not behind the tuned λ on ≥ ⌈0.75 N⌉",
with its own sensitivity over the three window cells) and SEC5-CR (head to head with the clip, report). It is PASS-0 at
best here; never PASS-2 in this study.

## The fourth family (the rule, fixed before any suite metadata is fetched)

**Suites, in order:** OpenML study 293 (AutoML Benchmark Training Datasets, 2022), then study 454
(New_OpenML_Suite_2025_classification), then study 445 (IRT Diverse Dataset Benchmark). None has been used by a CRR study.

**Eligibility:** SEC4's rule unchanged (active; ARFF; ≥ 4 classes; 400 to 1,000,000 rows; ≤ 1001 features; not SEEN by
OpenML id, name or shared records, SEC4's nine now included; one carrier per shared record set, lowest OpenML id kept;
K requested the largest even number ≤ min(classes, 10)).

**Pooling:** suites are added in the order above until at least **8** datasets are eligible. If the pool then holds more
than **12**, 12 are kept by a seeded draw (the sorted eligible OpenML ids, permuted by numpy `default_rng(20260930)`,
first 12). A suite whose record cannot be fetched is skipped and the skip printed. Metadata only: no dataset record is
read before the hash.

## Timing (R2, R3)

- Part C's candidates are chosen on SEEN data on 2026-09-29. **No carrier of the fourth family is fetched or opened before
  2026-09-30 00:00 UTC**, and not before SEC5's hash is OpenTimestamps-stamped and pushed.
- The pre-registration (`PREREG.md`) is written after the development output and the carrier selection exist, and is
  hashed with them and with the frozen scripts.
