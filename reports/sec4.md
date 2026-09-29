# SEC4: a robust SEC (the stability-clipped Laplace weight) on a third unseen family

**How it was run.**
- **The request.** Prompt-log entry 228: make SEC robust and repeat the tests.
- **The development stage.** `prereg/sec4/DEV_DECLARATION.md` was pushed at bde17ab before any guard ran. The guard was
  chosen on 16 SEEN carriers (`dev_SEC4.txt`).
- **The pre-registration.** `prereg/sec4/PREREG.md`, HASH.txt sha256 cf702c31…, prereg commit 278d0b4 pushed
  2026-09-28T04:13Z.
- **The anchor.** OpenTimestamps is complete in Bitcoin block 968935 (`runs/sec4/hash_check_datastep.txt`). The signed tag
  was created, but its push was refused, as for SCL3 and SEC3.
- **The data step.** 2026-09-29, from 00:05:59Z (R3: the guard was chosen the day before). The hash was unchanged, and all
  18 raw files matched the manifest.
- **Scoring.** The frozen scorer, output in `runs/sec4/score.txt`. The synthetic_control rerun is byte-identical.

This report is written after ledger rows SEC4-D … SEC4-E and quotes them.

## The answer

**The clipped SEC is tuning-free on the third unseen family, with no divergence and no fragility. It is the record's
first PASS-1. It is not a CRR rule.**

| row | question | observed | verdict |
|---|---|---|---|
| SEC4-1 | is the clipped SEC within a step of the tuned λ? | 6 of 6 (need 5) | **PASS-1** |
| SEC4-2 | does any seed diverge? | none (unguarded SEC: anneal, cardiotocography, synthetic_control) | **PASS-0** |
| SEC4-S | is SEC4-1's label stable over the window settings? | 0 of 18 cells flip | not fragile |
| SEC4-P | is it within a step of a 3-point mini-sweep? | 6 of 6 | **PASS-0** |
| SEC4-T | where a reused λ fails, does SEC succeed? | the reused λ fails on only 2 (cardiotocography, synthetic_control); SEC is not behind on both | NOT DECIDABLE |
| SEC4-K | compute | 1 of 17 configurations; CPU share of the full sweep 0.0508–0.0655; overhead against raw Laplace x0.891–x1.189 | report |
| SEC4-D | development (SEEN) | clip 16/16, D-GATE OPEN | report |

**The carriers.**
- **Scored (6):** JapaneseVowels, anneal, artificial-characters, cardiotocography, gas-drift and synthetic_control.
- **Excluded (3), by the registered loader:**
  - cjs and MIC lost every row to the missing-value rule;
  - one-hundred-plants-margin has no class with 40 rows.
- The pre-registration had named these risks.

## What happened

**1. The clip did exactly what it was built for.** Unguarded SEC diverged on half the carriers:

| carrier | lowest seed, unguarded | guard firings (clipped) | clipped mean − tuned λ |
|---|---|---|---|
| anneal | 18.54 | 5 | +5.5056 |
| cardiotocography | 18.16 | 11 | +1.0377 |
| synthetic_control | 0.00 | 10 | +3.5000 |

- **Where it fired.** The clip fired on these three carriers and nowhere else. On the other three it never fired, so the
  code path there is SEC's own.
- **Without the clip.** Unguarded SEC was not behind the tuned λ on only 3 of 6. This is the same failure seen on cnae-9,
  dionis and fabert, and now it is fixed on a family the guard never saw.

**2. It did as well as the full sweep everywhere, at 1 configuration of 17.**
- **Margins.** Every margin is positive, from +0.5594 (artificial-characters) to +5.5056 (anneal).
- **Sensitivity.** The window sensitivity flips no cell.
- **Against the 3-point mini-sweep.** It beats the mini-sweep on all 6.

**3. Would a reused λ have done as well?** On 4 of 6, yes.
- **Where it held.** The λ transferred from the other carriers (30) was not behind on JapaneseVowels, anneal,
  artificial-characters and gas-drift.
- **Where it failed.** It failed on cardiotocography (−10.0000) and synthetic_control (−6.3333), whose tuned λ are 7092.2
  and 4230, far from the others. SEC was not behind on both.
- **The consequence.** SEC4-T is NOT DECIDABLE (two carriers, not three). A reused λ reaches only 4 of 6, below the 5 that
  SEC4-1 needs, so the result does not reduce to a constant.

**4. Beside it:**
- raw Laplace: 1 of 6;
- the CRR rule Ω = 1: 5 of 6;
- the other guards: G-SCALE 6 of 6; G-RAW behind on cardiotocography.

## Standing

- **What PASS-1 means here.** Every PASS-1 condition in the pre-registration holds:
  - held-out and anchored in Bitcoin;
  - not fragile;
  - no divergence;
  - carriers' admissibility stated;
  - no reduction to a constant at the study's threshold.
- **Its limits:**
  - N is 6, after 3 exclusions.
  - κ itself was not swept, although two other guard forms are reported beside it.
  - The guard was chosen on SEEN carriers, three of them where the failure was found.
  - It is a single family.
- **It is not PASS-2.** The clipped rule has no earlier held-out pass. SCL3-3 was unguarded SEC, a different rule. PASS-2
  needs the same frozen rule on a fourth unseen family, under a fresh pre-registration on a later day.
- **It is not a CRR result.** SEC is the textbook Laplace weight with a units calibration, and the clip is a step-size
  safeguard (R8). CRR's own rule, Ω = 1, reached 5 of 6 as a report beside it.
- **Compute_Savings is re-pinned.** With no divergence, the realistic protocol saves s = 0.9412 of a sweep, against 0.7537
  on unguarded SEC's record (`Compute_Savings/GLOBAL_ESTIMATE.md`).

## What a surrogate would have done

- **D-ID** (`prereg/sec4/dev_SEC4.txt`). On SEC1's synthetic stream, with the bound at +∞, the clip equals unguarded SEC
  bit for bit (5/5). Below the clip, the code path is SEC's. SEC1's gate (`prereg/sec3/gate_SEC3.txt`) still applies:
  - the calibration closes a units error (POS) and is invariant to units distortions (INV);
  - it fails under a shape error (SHAPE).
- **The smoke run** (`prereg/sec4/smokefull.txt`). One synthetic carrier prints SEC4-1 NOT DECIDABLE (N = 1 < 4), so the
  verdict comes from the carriers, not the arithmetic.
- **Where the verdicts come from.** The divergences the clip removed are seeds of the frozen learner on real data, and the
  rerun reproduced byte for byte.
