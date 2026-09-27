# Pre-registration — SEC3: can a learner take on a new task stream without paying to rediscover the forgetting weight?

- **Study id:** `sec3`.
- **Written:** 2026-09-27 (UTC), after the rules were committed at 373af46 (prompt-log entry 227; AGENT_LOG 167).
- **Plan item.** CL-1 of `Empty_Centre/REVIEW_AND_NEXT_STEPS.md`: replicate SEC toward PASS-1 and PASS-2, with the compute
  accounting (ENERGY1) inside it.
- **Timing.**
  - This file, the frozen scorer and every gate and smoke output are hashed, OTS-stamped and pushed before any carrier
    below is fetched.
  - Every scoring rule dates from 2026-09-27, the day the guard gate ran on SEEN carriers (R3).
  - **No carrier below is fetched or opened before 2026-09-28 00:00 UTC**, and not before the hash and the stamp.

## What this study is

**The owner's question.** "To what extent does the SEC method enable learning new tasks without paying to rediscover the
forgetting weight for every task stream?"

**What is being tested.** The online-EWC learner of SEC1, SCL3 and EQ3/EQ4 (numpy MLP; five seeds; tasks of two classes)
needs a penalty weight λ.
- **The conventional practice.** Sweep λ: SEC1's two-stage grid, 17 configurations per carrier, each run at five seeds.
- **SEC.** The Laplace weight w = 1/2 on a secant-calibrated Fisher. It is one configuration, with no sweep.

**What is already known (SCL3, `reports/scl3.md`, PASS-0, FRAGILE).**
- On 10 unseen OpenML-CC18 carriers, SEC was not behind the tuned λ on 9, at one configuration.
- It failed large on cnae-9, where two of five seeds diverged.

**What SEC3 asks, on a second unseen family:**
1. Does SCL3's result replicate, exactly as SCL3 ran it? Rows SEC3-0..4 and S.
2. Is the saving SEC's, or would a reused λ have done as well? Rows SEC3-T and P.
3. How much compute does it save, measured? Row SEC3-K.

**Not a CRR hypothesis.** SEC is the textbook Laplace weight plus a units calibration. The ledger records it as "not a CRR
rule". The registered CRR rule (Ω = 1) is printed beside it as an R7 comparison.

## R3 statement

**Defined on 2026-09-23 to 2026-09-24, and unchanged:**
- SEC1's learner, calibration, arms, grids, windows and thresholds;
- SCL3's ARFF reader, OpenML loader, class-selection rule and carrier-selection rule.

**Defined on 2026-09-27** (commit 373af46; no unseen record read):
- the second family and two selection additions;
- the saving rows;
- the timing;
- the guard and its gate. The gate ran on SEEN carriers and closed.
- the change that makes the guarded arm report-only, after the gate.

**The consequence.** None of these may be used on another dataset on 2026-09-27, so the data step is on or after
2026-09-28 00:00 UTC.

## Anchoring

- **OpenTimestamps.** `HASH.txt` is stamped (`HASH.txt.ots`) before any fetch, and upgraded after Bitcoin confirmation.
- **The tag.** The signed tag is `prereg-sec3-2026-09-27`. If the tag push is refused, as for SCL3, the push timestamp of
  the commit carrying `HASH.txt` and `HASH.txt.ots` is the git-side witness.

## Carriers (`carrier_selection.txt`, from `studies/sec3/select_carriers.py`; metadata only)

**The source.** The OpenML AutoML Benchmark classification suite, OpenML study 271. The study record and the data list are
saved in this folder.

**The selection.** SCL3's rule, unchanged:
- active ARFF;
- at least 4 classes and at least 400 rows;
- at most 1001 features;
- not SEEN by name or by shared records;
- K requested is the largest even number ≤ min(classes, 10).

**Two declared additions.**
- An OpenML id listed in `data/SEEN.md` is SEEN. SCL3's ten are listed by id, and the name match missed them.
- At most 1,000,000 rows, the pure-Python ARFF reader's cost. This excludes KDDCup99.

| OpenML id | name | rows | features | classes | K requested |
|---|---|---|---|---|---|
| 1596 | covertype | 581012 | 55 | 7 | 6 |
| 41167 | dionis | 416188 | 61 | 355 | 10 |
| 41164 | fabert | 8237 | 801 | 7 | 6 |
| 41169 | helena | 65196 | 28 | 100 | 10 |
| 41168 | jannis | 83733 | 55 | 4 | 4 |
| 40685 | shuttle | 58000 | 10 | 7 | 6 |
| 41166 | volkert | 58310 | 181 | 10 | 10 |

**Loading.** SCL3's loader and SEC1's class-selection rule are applied unchanged:
- the largest K classes;
- a class floor of 40;
- a 5000-row stratified cap (seed 777);
- K lowered by two until the floor holds.

**Exclusions.** A carrier with K < 4 is excluded and counted (shuttle's class sizes may exclude it). The rows are scored
on the N carriers that remain, with the denominator printed.

**The data step.**
1. `data/fetch_openml.py --manifest sec3 <the seven ids>`: md5 against the description; sha256 manifest.
2. `sec3_score.py check`.
3. `data/SEEN.md` gains the seven in the same commit.

## Instrument (frozen in `runs/sec3/frozen/`)

- **`sec1_score.py`, `scl2_score.py`, `scl3_score.py`.** Byte copies of `runs/scl3/frozen/`.
- **`sec3_score.py`.** It adds the carriers, the guarded arm, the timing, the scorer and the gate.

**Per carrier, at seeds 0–4:**
- **every SEC1 arm through SEC1's own `run_all`, unchanged:**
  - `fixed` (the tuned λ: two-stage grid, tuned in-sample on the scored seeds, which favours the baseline);
  - `fixed_sec`, `bayes`, `bayes_sec` (the arm under test), `bayes_s1`, `eq` (Ω = 1);
  - `bayes_sec` at the 8 window cells;
- **the guarded arm, `bayes_sec_g`** (report only), at:
  - the primary window;
  - the 3 retained window cells;
  - a stricter bound of 0.5.

**Timing.** Every configuration is timed (`time.process_time`) into `times_<id>.jsonl`, never into the results file.

**The resolvable step.** Per carrier: max(1, 2 × SE over seeds of the tuned raw-λ arm), as in SEC1 and SCL3.

## Checks before the hash (covered by it)

**`gate_SEC3.txt`, SEC1's gate: GATE OPEN.**
- POS holds: the calibration closes the gap on a units error.
- INV holds: invariance to units distortions.
- SHAPE fails as required: the calibration fixes units, not shape, and moves the arm by −41.1371 under a shape error.

So SEC3-3 is not forced by the arithmetic: the data decide whether a carrier's Fisher error is one of units.

**`gate_SEC3.txt`, the guard gate: CLOSED.**

| check | carrier | result |
|---|---|---|
| G-ID | synthetic | holds: at +inf the guard equals `bayes_sec` bit for bit |
| G-QUIET | wall-robot-navigation (SEEN) | holds: the guard never fires |
| G-RESCUE | cnae-9 (SEEN) | **fails** |

On cnae-9 the guard fired and lifted the two diverging seeds (0.00 → 52.60, 12.50 → 59.90). The guarded mean is still
behind SCL3's tuned λ by −1.9792, against a step of 1.7305. The guarded arm therefore enters no hypothesis. It is run and
printed as the `*-GR` report rows only.

**`smokefull.txt`.** The whole pipeline on SEC1's synthetic stream. Its labels are meaningless for one carrier.

## Hypotheses (verdicts computed by `sec3_score.py score`; one-sided "not behind", as in SEC1 and SCL3)

**N** is the number of scored carriers, and need = ⌈0.75 N⌉, SCL3-3's share.

| id | what is tested | criterion |
|---|---|---|
| **SEC3-0** (precondition) | the miscalibrated set M: carriers where `bayes` − tuned ≤ −step | DECIDABLE if \|M\| ≥ 3; otherwise SEC3-1 is NOT DECIDABLE |
| **SEC3-1** | on M, SEC closes at least half the raw gap | PASS on ≥ ⌈2/3 × \|M\|⌉ carriers of M |
| **SEC3-2** (no harm) | outside M, `bayes_sec` − `bayes` > −step | PASS on every such carrier; NOT DECIDABLE if there is none |
| **SEC3-3** (tuning-free, the replication of SCL3-3) | `bayes_sec` − tuned > −step | PASS on ≥ need carriers, otherwise FAIL |
| **SEC3-4** (the spread collapses) | span of the calibrated tuned λ against the raw span | PASS if the calibrated span ≤ the raw span / 10 |
| **SEC3-T** (is the saving SEC's?) | B = carriers where a transferred λ is behind the tuned λ by a step. The transferred λ is the leave-one-carrier-out median, on a log scale, of the other carriers' tuned raw λ, snapped to the coarse grid; its accuracy is read from the grid runs. | DECIDABLE if \|B\| ≥ 3; PASS if SEC is not behind the tuned λ on ≥ ⌈0.75 \|B\|⌉ of B. If NOT DECIDABLE, the report says a reused λ would have saved the sweep without SEC |
| **SEC3-P** (against a cheap sweep) | `bayes_sec` − best of the 3-point sweep {1, 30, 1000} > −step. The sweep costs 3 configurations; SEC costs 1. | PASS on ≥ need carriers |
| **SEC3-S** | SEC3-3's "not behind" over the 3 retained window cells × N. The declared change: SCL3's cells with a 0.05 window, where SCL3-S flipped, are dropped. | more than 1 flip = FRAGILE |
| SEC3-K | configurations (full sweep, 3-point sweep, SEC) and measured CPU seconds; SEC's calibration overhead against raw Laplace | report |
| SEC3-*-GR, E | the guarded arm; the raw-Laplace and Ω = 1 counts; the guard firings | report |

**Every per-carrier and per-seed value is printed (R6).**
- A non-finite run scores 0 and is kept.
- Calibration fallbacks are counted, never excluded.

**What a PASS would be.**
- **PASS-0.** SEC3-3 passing is PASS-0 for SEC as run in SCL3 (R2–R9 as written).
- **PASS-1.** It is PASS-1 if SEC3-S is not fragile, the OTS anchor completes, and no control is violated.
- **PASS-2.** With SCL3-3, a PASS-1 here would make the pair the route to PASS-2. SCL3-3 itself was fragile, so the ladder
  decides.

**What would change the reading.**
- **SEC3-3 FAILs.** SEC is not tuning-free on this family, and SCL3's pass does not replicate.
- **SEC3-T is NOT DECIDABLE or FAILs.** The saving is not attributable to SEC on this family: a reused λ, or nothing,
  would do.
- **SEC3-P FAILs.** A 3-configuration sweep beats SEC, so SEC's saving is at most 3 configurations to 1, not the full
  sweep.

## Reproduction (on or after 2026-09-28 00:00 UTC)

```
uv run python data/fetch_openml.py --manifest sec3 1596 41167 41164 41169 41168 40685 41166
uv run python runs/sec3/frozen/sec3_score.py check > runs/sec3/data_check.txt
for i in 1596 41167 41164 41169 41168 40685 41166; do uv run python runs/sec3/frozen/sec3_score.py all $i --out runs/sec3/results_$i.jsonl; done
uv run python runs/sec3/frozen/sec3_score.py all 41168 --out runs/sec3/rerun_41168.jsonl --times runs/sec3/rerun_times_41168.jsonl && cmp runs/sec3/rerun_41168.jsonl runs/sec3/results_41168.jsonl   # R9
uv run python runs/sec3/frozen/sec3_score.py score runs/sec3/results_*.jsonl > runs/sec3/score.txt
```
