# SEC5: SEC4's clipped SEC replicated on a fourth unseen family, with κ swept — it does not replicate

**How it was run.**
- **The request.** Prompt-log entry 238: run a new SEC test in full, record every decision, give a full output of the
  findings, and use CRR to fine-tune the approach as required.
- **The declaration.** `prereg/sec5/DEV_DECLARATION.md` was pushed at 2c07fcc before any run and before any suite
  metadata was fetched. AGENT_LOG 177.
- **The CRR-guided development.** It ran on the 22 SEEN carriers (`prereg/sec5/dev_SEC5.txt`; AGENT_LOG 178).
- **The pre-registration.** `prereg/sec5/PREREG.md`, HASH.txt sha256 2556b65e…, prereg commit 576a092 pushed
  2026-09-29T03:12Z.
- **The anchor.** OpenTimestamps is complete in Bitcoin blocks 969093 and 969098 (`runs/sec5/ots_upgrade.txt`). The
  signed tag was created, but its push was refused, as for SCL3, SEC3 and SEC4 (`runs/sec5/tag_attempt.txt`).
- **The data step.** 2026-09-30, from 00:04:37Z (R3: the CRR candidates and κ cells were fixed the day before).
  - The hash was unchanged (`runs/sec5/hash_check_datastep.txt`).
  - All 24 raw files matched the manifest (`runs/sec5/data_check.txt`).
- **The scoring.** The frozen scorer's output is `runs/sec5/score.txt`. The rerun of autoUniv-au6-750 is byte-identical
  (`runs/sec5/rerun_check.txt`).

This report is written after ledger rows SEC5-C-DEV … SEC5-E and quotes them.

## The answer

**SEC4's PASS-1 does not replicate on a fourth family. The clipped SEC was not behind the tuned λ on 4 of 8 carriers,
where 6 were needed. The FAIL is robust: 0 of 40 sensitivity cells flip, κ included. There is no PASS-2. SEC4-1 stands
as a single-family PASS-1.**

| row | question | observed | verdict |
|---|---|---|---|
| SEC5-C-DEV | does the CRR-guided refinement (A6: past importance averaged, not summed) earn a test? | A6-MEAN 18/22, fixes 2/6; A6-MEAN-CLIP 22/22 but −0.2021 against the clip on average | D-GATE-C CLOSED (not run on unseen data, R12) |
| SEC5-1 | is the clipped SEC within a step of the tuned λ? | 4 of 8 (need 6) | **FAIL** |
| SEC5-2 | no seed below half the tuned accuracy? | 2 carriers with such seeds (pokerhand, volcanoes-d4) | **FAIL** |
| SEC5-T | is the saving SEC's, where a reused λ fails? | 3 of 7 (need 6) | **FAIL** |
| SEC5-P | one configuration against the 3-point sweep {1, 30, 1000}? | 6 of 8 (need 6) | PASS-0 |
| SEC5-S | sensitivity over 3 window cells and κ ∈ {0.25, 1.0} | 0 of 40 flips | not fragile |
| SEC5-K | CPU share against the 17-configuration sweep | 0.0563–0.0623; overhead ×0.968–×1.108 against raw Laplace | report |
| SEC5-E | guard firings | Kuzushiji-MNIST 4, volcanoes-d4 5, the other six 0 | report |

## The carriers

**Chosen by the declared rule.** OpenML study 293 (AutoML Benchmark Training Datasets) held 27 eligible datasets; the
seeded draw kept 12 (`prereg/sec5/carrier_selection.txt`).

**Four were excluded by the registered loader:**
- hypothyroid: every row carries a missing value;
- volcanoes-a3, volcanoes-a4 and volcanoes-b2: K falls to 2 under the 40-row class floor.

With only one volcano set scored, the pre-registered report line "the volcanoes counted once" does not arise.

**Scored (N = 8):**

| carrier | tuned λ | tuned acc. | step | clipped SEC − tuned | fired | unguarded SEC | raw Laplace | Ω = 1 |
|---|---|---|---|---|---|---|---|---|
| Indian_pines | 20 | 55.0649 | 5.2111 | −6.7932 | 0 | −6.7932 | −10.5694 | −44.3756 |
| Kuzushiji-MNIST | 300 | 25.6800 | 1.3303 | +5.2000 | 4 | +5.2000 | −3.2400 | +3.3000 |
| autoUniv-au6-750 | 0.035336 | 8.0795 | 1.6437 | −0.3974 | 0 | −0.3974 | +0.0000 | −0.5298 |
| microaggregation2 | 60 | 17.6024 | 15.5216 | −4.1159 | 0 | −4.1159 | −4.1159 | −4.1359 |
| pokerhand | 100 | 43.4600 | 1.8216 | −28.2400 | 0 | −28.2400 | −32.1400 | −35.0200 |
| spoken-arabic-digit | 0.212766 | 9.8800 | 1.0000 | −0.0200 | 0 | −0.0200 | −0.0400 | −0.1200 |
| volcanoes-d4 | 1000 | 94.9950 | 1.0000 | −88.9089 | 5 | −78.7187 | −89.6897 | −89.6296 |
| walking-activity | 0.212766 | 13.6000 | 1.1367 | −2.5600 | 0 | −2.5600 | −0.9800 | −2.2800 |

- **Not behind (within a step):** Kuzushiji-MNIST, autoUniv-au6-750, microaggregation2, spoken-arabic-digit.
- **Behind:** Indian_pines, pokerhand, volcanoes-d4, walking-activity.
- **Beside it (report):** unguarded SEC 4/8, raw Laplace 4/8, the CRR rule Ω = 1 4/8.

## Why it failed (readings of the printed numbers, not new claims)

- **Where the clip fired, it did not decide the verdict.** It fired on only two carriers:
  - on Kuzushiji-MNIST SEC was far ahead (+5.2000);
  - on volcanoes-d4 SEC was far behind.

  Everywhere else the clipped SEC equals unguarded SEC. So SEC5 is mostly a test of SEC itself on this family, and SEC
  itself is not tuning-free here.
- **pokerhand: under-regularised, not diverged.**
  - The runs are finite, and the clip never fired (largest margin 0.157719).
  - The calibration scale at the first penalised task was small (0.078–0.289 across seeds), and the learner forgot.
  - So SEC5-2's low seeds are not stability-edge crossings. As registered, a seed below half the tuned accuracy counts
    as a failure.
- **volcanoes-d4: the clip caps what the carrier needs.**
  - The tuned λ sits on a plateau from 1000 to 10000 (94.99 at every value).
  - The calibrated penalty crossed the stability edge on every seed, and the clip held it below.
  - Unguarded SEC was also far behind (−78.7187). The explicit-Euler edge that the clip protects is below the strength
    this carrier rewards.
- **Indian_pines and walking-activity: moderately behind at every κ and window.** On walking-activity, raw Laplace
  (−0.9800) was closer than SEC.

## The κ sweep (the reason SEC4 was not PASS-2)

κ = 0.25 and κ = 1.0 each give 4 of 8, the same carriers as κ = 0.5; 0 of 16 κ cells flip. κ is not what decides this
family. The failure is SEC's calibration on carriers whose tuned λ lies far from where the calibration lands.

## The CRR-guided refinement

- **The result.** The owner asked that CRR be used to fine-tune the approach. A6's bounded strength ("never an
  accumulated count") gave two candidates, developed on the 22 SEEN carriers under a gate declared before any run.
  D-GATE-C CLOSED:
  - averaging without the clip left 5 of the 6 divergence carriers diverging;
  - with the clip, it was 0.2021 below the clip on average.
- **What the development showed.** On anneal (one settled task), averaging equals summing, and divergence still
  occurred. The diverging scale is the calibration's, not the accumulation's. CRR's A6 reading pointed at the wrong cause.

## Standing

- **SEC4-1 remains a PASS-1 on one family.** SEC5-1 is the declared replication, and it fails, so there is no PASS-2.
  Per CLAUDE.md §7, only a PASS-2 may be quoted outside the ledger as a finding. **The clipped SEC has no finding.**
- **The ledger now holds**, for SEC, on unseen data:
  - SCL3-3 PASS-0 (unguarded SEC, 9/10);
  - SEC3-3 FAIL (4/6);
  - SEC4-1 PASS-1 (clipped, 6/6);
  - SEC5-1 FAIL (clipped, 4/8).

- **What still holds.**
  - One configuration is not behind a 3-point sweep on 6 of 8 (SEC5-P, PASS-0), and costs 0.0563–0.0623 of the full sweep's CPU time (SEC5-K).
  - That is a cheap-sweep replacement on most carriers, not a tuning-free method.
- **Compute_Savings.** `Compute_Savings/GLOBAL_ESTIMATE.md` was declared on SCL3, SEC3 and SEC4. SEC5 is not among its
  inputs, so its pinned numbers are unchanged. Its premise — that SEC saves the sweep at the rate those studies showed —
  is weakened by SEC5. A re-estimate that includes SEC5 would need its own declaration.
- **It is not a CRR result either way.** SEC is the textbook Laplace weight with a units calibration; the clip is a
  step-size safeguard (R8). CRR's rule Ω = 1 reached 4 of 8 as a report beside it.

## What a surrogate would have done

- **D-ID** (`prereg/sec5/dev/devid.txt`). With the divisor forced to 1, both A6 candidates equal SEC and SEC4's clip bit
  for bit on SEC1's synthetic stream (5/5). The primary arm is SEC4's frozen code unchanged. SEC4's D-ID and SEC1's gate
  (`prereg/sec3/gate_SEC3.txt`) apply: the calibration closes a units error and fails under a shape error.
- **The smoke run** (`prereg/sec5/smokefull.txt`). One synthetic carrier prints SEC5-1 NOT DECIDABLE (N = 1 < 4), so the
  verdict comes from the carriers, not the arithmetic.
- **Where the verdicts come from.** The failures are the frozen learner's runs on real data, and the rerun reproduced
  byte for byte.
