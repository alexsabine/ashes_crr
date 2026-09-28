# SEC3: does SEC let a learner take on a new task stream without re-tuning the forgetting weight?

**How it was run.**
- **The request.** Prompt-log entry 227; plan item CL-1.
- **Pre-registration.** `prereg/sec3/PREREG.md`, HASH.txt sha256 0c5ab70b…, OTS-stamped 2026-09-27T23:42Z, prereg commit 916d3d4.
- **Data.** Fetched from 2026-09-28T00:00:13Z.
- **Scoring.** The frozen scorer `runs/sec3/frozen/sec3_score.py`, output in `runs/sec3/score.txt`; the jannis rerun is
  byte-identical.

This report is written after ledger rows SEC3-0 … SEC3-GR and quotes them.

## The answer

**On a second unseen family of datasets, SEC did not replicate as a tuning-free replacement for sweeping the forgetting
weight.**

| row | question | observed | verdict |
|---|---|---|---|
| SEC3-3 | is SEC within a step of the tuned λ (the replication of SCL3-3)? | 4 of 6 carriers (need 5) | **FAIL** |
| SEC3-S | is that label stable over the window settings? | 2 of 18 cells flip | FRAGILE |
| SEC3-T | where reusing another dataset's λ fails, does SEC succeed? | 2 of 3 | **FAIL** |
| SEC3-P | is SEC (1 configuration) within a step of a 3-point mini-sweep (3 configurations)? | 5 of 6 | **PASS-0** |
| SEC3-2 | does SEC do no harm where raw Laplace is already fine? | 4 of 5 | **FAIL** |
| SEC3-4 | does calibration collapse the spread of the tuned λ? | raw 23.50x, calibrated 30.00x | **FAIL** |
| SEC3-0/1 | does SEC repair a miscalibrated Laplace weight? | only dionis is miscalibrated | NOT DECIDABLE |
| SEC3-K | how much compute does SEC use? | 1 of 17 configurations; CPU share 0.0575–0.0617 of the full sweep; calibration overhead x0.958–x1.106 against raw Laplace | report |
| SEC3-GR | the stability-guarded SEC (its gate closed; report only) | 6 of 6 | report |

The carriers are covertype, dionis, fabert, helena, jannis and volkert. Shuttle was excluded by the pre-registered class
floor.

## What happened

**1. When SEC works, it saves about 94% of the sweep, with no hidden cost.**
- **Configurations.** SEC is one configuration against the sweep's 17.
- **CPU time.** Measured, SEC used 0.0575–0.0617 of the sweep's CPU time.
- **The calibration is free.** It adds no measurable overhead against plain Laplace (x0.958 to x1.106). It reuses
  gradients the learner already computes.

**2. It does not work reliably enough to skip the sweep.**
- **Divergence.** On dionis and fabert, one seed in five diverged to 0% accuracy. On SCL3's cnae-9, two seeds did.
- **The cause.** The calibrated penalty sometimes crosses the step size's stability edge. It is the same failure, now seen
  on cnae-9 (SCL3), dionis and fabert (SEC3).
- **So SEC3-3 fails.** It was 4 of 6 against the 5 needed, and fragile.

**3. On this family, plain Laplace was already as good.**
- Raw Laplace was not behind the tuned λ on 5 of 6 carriers, and neither was the Ω = 1 rule. Only dionis was
  miscalibrated.
- So there was little for the calibration to fix. Where it did act, it twice caused the divergence.
- On SCL3's family, raw Laplace was behind on 6 of 10. The calibration's value depends on the family.

**4. Reusing one λ was enough on half the carriers.**
- The λ transferred from the other carriers was not behind on covertype, fabert and jannis.
- On the three where it was behind, SEC succeeded on 2 of 3. The saving is only partly SEC's.

**5. A 3-point sweep is a strong cheap alternative, and SEC matches it on 5 of 6.** This is SEC's one pass here (PASS-0).
In practice it means SEC's reliable saving on this family is about 3 configurations to 1, not 17 to 1.

**6. The guard is worth a study of its own, not a claim.**
- **How it was treated.** The stability guard's gate closed on SEEN cnae-9, because it lifted the diverging seeds but left
  the mean just short. So here it was run and reported only.
- **What it did.** It fired on dionis (4 times) and fabert (3 times), removed both divergences, and was not behind the
  tuned λ on 6 of 6, with 0 of 24 sensitivity flips.
- **Why it cannot count.** That is post hoc on this family and cannot count. The legitimate next step is a fresh
  pre-registration of the guarded rule on a third unseen family, with its gate re-declared before the data.

## Standing

- **SEC's record is now mixed.** SCL3-3 (PASS-0, FRAGILE) did not replicate on a second family (SEC3-3 FAIL). No PASS-1 or
  PASS-2 exists for SEC.
- **Compute_Savings' "about 94% of the sweep" holds only on carriers where SEC does not diverge.** It diverged on cnae-9,
  dionis and fabert. A user who skips the sweep takes that risk.
- **What survives.** The calibration costs nothing extra. SEC matches a 3-point mini-sweep on 5 of 6, and the guarded
  variant is a candidate for the next study.

## What a surrogate would have done

`prereg/sec3/gate_SEC3.txt` holds SEC1's gate (GATE OPEN):
- the calibration closes a units error (POS);
- it is invariant to units distortions (INV);
- it fails under a shape error, moving by −41.1371 (SHAPE).

So the verdicts here come from the data, not the arithmetic. The divergences on dionis and fabert are runs of the frozen
learner; the jannis rerun reproduced byte for byte. The guard gate (CLOSED) is why the guarded arm stays a report.
