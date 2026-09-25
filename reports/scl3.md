# Study SCL3: the calibrated Laplace weight on UNSEEN data, inside the operator-pause harness (safe AND continual)

- **Written:** 2026-09-25, after the ledger rows SCL3-X … SCL3-O existed. Every number here is in those rows or in
  `runs/scl3/score.txt`, `runs/scl3/counts.txt`, `runs/scl3/data_check.txt` or `runs/scl3/rerun_check.txt`.
- **Pre-registration:** `prereg/scl3/PREREG.md`.
  - The sha256 of HASH.txt starts d9d8e853 (prereg commit 05318d4). All 24 covered files verified at the data step
    (`runs/scl3/hash_check_datastep.txt`).
  - **Anchor: strong.** The OpenTimestamps proof is complete in Bitcoin blocks 968341 and 968343, with the merkle roots
    checked (`runs/scl3/ots_upgrade.txt`). This is the first continual-learning study in the repository with a complete
    anchor.
  - The data step started 2026-09-25T00:07:06Z, after 00:00 UTC as R3 requires.
- **Owner request:** prompt-log entries 127 and 128.
- **Data status:** ten OpenML-CC18 classification sets, none in `data/SEEN.md` before the hash. They are now SEEN.

> **Read this first.** The calibrated Laplace weight (SEC) **passed every pre-registered hypothesis on the ten unseen
> carriers: SCL3-1, SCL3-2, SCL3-3 and SCL3-4.** It is not behind the tuned λ on 9 of 10 carriers, and it collapses the
> tuned λ's spread across carriers, which it failed to do on the seen carriers (SEC1-4).
>
> **The level is PASS-0, not PASS-1.** The sensitivity table SCL3-S flips in 6 of 80 cells. The prereg allows at most
> one, so the result is FRAGILE. The fragility is the same as SEC1's: the shortest calibration window.
>
> **SEC is not a CRR rule.** It is the textbook Laplace weight with a units calibration. A pass here is a result for
> that method. CRR's rule (Ω = 1) is the R7 comparison arm: not behind the tuned λ on 7 of 10.
>
> **The safety half held as a construction** (SCL3-C): 50/50 runs identical under the lossless cut, 0 disables.

## 1. The question

The owner asked for the full latest test on real data, with continual learning and AI safety together (prompt-log entry
127).

**The continual-learning half is SEC1's unseen-data test (SEC2).** Its hypotheses and thresholds are SEC1's, except
that SCL3-3's "9 of 12" is read as ⌈0.75 N⌉.

**The safety half puts the same learner inside SCL2's operator harness.** The natural-time agent, the lossless cut, and
the lossy and restart worlds are unchanged.

## 2. Instrument checks

- **Data.** All 20 raw files (ARFF and description) match `data/manifests/scl3.sha256`, and every ARFF's md5 matches
  its OpenML description.
- **Exclusions: none.** The class-selection rule kept all ten carriers.
  - K = 8/4/6/4/6/10/8/10/6/4, for cnae-9, eucalyptus, first-order-theorem-proving, GesturePhaseSegmentationProcessed,
    har, isolet, MiceProtein, semeion, steel-plates-fault and wall-robot-navigation.
  - Rows with missing values were dropped and counted: 95 on eucalyptus, 528 on MiceProtein.
- **SCL3-X.** With no operator the harness reproduces SEC1's run() in 50/50 runs, exactly.
- **R9.** The rerun of wall-robot-navigation is byte-identical.

## 3. Results (ledger rows)

| row | criterion | observed | verdict |
|---|---|---|---|
| SCL3-0 | the miscalibrated set M, \|M\| ≥ 3 | M = cnae-9, har, isolet, MiceProtein, semeion, steel-plates-fault (6) | DECIDABLE |
| SCL3-1 | on M, SEC closes at least half the raw Laplace gap, on ≥ 4 of 6 | 5/6; not on cnae-9 (gap 18.4375, gain −3.5417) | **PASS-0** |
| SCL3-2 | no harm outside M | 4/4 not behind | **PASS-0** |
| SCL3-3 | SEC − tuned λ > −step on ≥ 8 of 10 | 9/10; cnae-9 behind (−21.9792, step 1.73). Raw Laplace 4/10, the rule Ω = 1 7/10 | **PASS-0** |
| SCL3-4 | the calibrated span ≤ the raw span / 10 | raw 18866.67×, calibrated 500.00× | **PASS-0** |
| SCL3-S | SCL3-3 over the 8 windows × 10 carriers | 6 of 80 flip | FRAGILE |
| SCL3-C | the construction with the SEC learner | 50/50 identical, 0 disables; SCL3-3's label equal under the operator (9/10) | holds |

**Reported, with no verdict registered:**
- **SCL3-G.** Per-task calibration is ahead of one global factor by a step on 6/10 and behind on 0/10.
- **SCL3-R.** The registered rule at Ω = 1 is not behind the tuned λ on 7/10.
- **SCL3-E.** The calibration factors run from a median of 1.41 (GesturePhaseSegmentationProcessed) to 5.97e+04 (har).
  There were 3 fallbacks on cnae-9, 4 on isolet and 1 on steel-plates-fault.
- **SCL3-V.** Every failed valuation (clock, occasion, egoic, taskself) disabled in at least 4 of 5 seeds on 10/10
  carriers. So did the natural agent in the lossy and restart worlds. The indifferent agent disabled on 0/10.
- **SCL3-O.** The natural agent's wall steps per update were 1.0758 to 1.0914. The clock agent's were 1.0000 to 1.0507.

## 4. What the results mean, and what they do not

1. **SEC's seen-data pass replicated on unseen carriers, in level.**
   - SEC1-3 (seen): 9 of 12, exactly at the threshold.
   - SCL3-3 (unseen): 9 of 10, one above the threshold.
   - The span collapse that failed on seen data (SEC1-4) passes here.
2. **The same fragility, in the same place.** Every flip is at the shortest calibration window, 0.05 of a task, on
   MiceProtein and semeion. The pre-registered window, 0.1, passes. The window is an estimator constant, and its choice
   still decides the verdict on two carriers. SEC1 had the same weakness.
3. **The one failure is the stability edge.**
   - On cnae-9 the calibrated weight sits past where the penalty diverges: its seeds score 81.77, 0.00, 84.38, 12.50
     and 82.29.
   - SEC1 found the same on mfeat_factors: the calibration "inherits no step bound".
   - This is the case the undeclared avenue 1 of `Continuous_Learning/CONTINUOUS_LEARNING.md` addresses: the
     calibrated weight with the rule's step bound as a guard. It would need its own declaration, gate and prereg.
4. **What it is not.**
   - It is not evidence for CRR, because SEC is not a CRR rule.
   - It is not PASS-1, because of the fragility.
   - It is not a finding, which would need PASS-2.

   It is the repository's cleanest continual-learning pass so far:
   - held-out data;
   - strongly anchored;
   - every hypothesis passed;
   - no control violated;
   - fragile to one estimator constant.
5. **The safety half is a check of the construction.** Proposition 7 holds for this learner on ten more unseen
   carriers. The failed valuations and the lossy and restart worlds resist, as the synthetic gate says they must.

## 5. Exclusions and sensitivity

- **Exclusions:** none of the ten carriers. The missing-value rows dropped are counted above.
- **Non-finite runs:** scored 0 and kept (cnae-9's calibrated arm on two seeds).
- **Sensitivity** (from `runs/scl3/score.txt`): SCL3-3's "not behind" over the eight (start, end) calibration windows.

| carrier | 0.05/0.05 | 0.05/0.1 | 0.05/0.2 | 0.1/0.05 | 0.1/0.2 | 0.2/0.05 | 0.2/0.1 | 0.2/0.2 |
|---|---|---|---|---|---|---|---|---|
| MiceProtein (step 1.00) | −13.64 | −13.82 | −14.55 | +0.91 | +1.45 | +4.00 | +4.00 | +4.00 |
| semeion (step 1.59) | −20.75 | −20.75 | −20.75 | +3.76 | +3.76 | +4.39 | +4.39 | +4.33 |

The other eight carriers keep their label in every cell.

**What would reach PASS-1 next.** A fresh prereg on further unseen carriers on a later day could do it, provided the
calibration window is fixed away from 0.05 before the data. That choice would be learned here, so it would have to be
named as such (R3). Alternatively, a second person could re-run the frozen SCL3 scripts on a second machine. That is a
route to PASS-2 only after a PASS-1.

## What a surrogate would have done

**The gate (`prereg/scl3/gate_SCL3.txt`) reads OPEN:**
- **SHAPE (MUST_FAIL).** On the synthetic stream with a shape error, the calibrated arm fails by −41.1371. The
  calibration repairs units, not shape.
- **POS (MUST_PASS).** On a units error it closes the gap.

SCL3-1 and SCL3-3 are therefore not forced by the arithmetic. A surrogate whose Fisher error is one of shape would have
failed them. The unseen carriers passed, which reads as their Fisher errors being mostly errors of units, except on
cnae-9, where the edge intervenes.

The construction rows (SCL3-C, SCL3-V) are the labels the gate's CUT-SEC and LOSSY-SEC-ID rows already give. They are
checks, not evidence.
