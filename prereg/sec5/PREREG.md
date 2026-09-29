# Pre-registration — SEC5: SEC4's clipped SEC replicated on a fourth unseen family, κ swept, and a CRR-guided (A6) candidate

- **Study id:** `sec5`.
- **Written:** 2026-09-29 (UTC), after the declaration was pushed (`DEV_DECLARATION.md`, commit 2c07fcc), after the development
  stage ran on SEEN carriers (`dev_SEC5.txt`) and after the carrier selection ran on metadata (`carrier_selection.txt`).
  Prompt-log entry 238; AGENT_LOG 177–178.
- **Timing.** This file, the development outputs, the selection, the frozen scorer and the smoke output are hashed,
  OTS-stamped and pushed before any carrier below is fetched. **No carrier below is fetched or opened before 2026-09-30
  00:00 UTC** (R3: the A6 candidate was chosen on SEEN data on 2026-09-29).

## What this study is

**The owner's request.** "Yes, please run a new SEC test in full. [...] Use the CRR to fine-tune the approach as required"
(prompt-log entry 238), after the answer that the step that would most change the picture is a replication of SEC4 on a
second family with κ swept.

**Part R, the replication (primary).** SEC4's clipped SEC, unchanged: SEC (the Laplace weight w = 1/2 on a secant-calibrated
Fisher) with G-CLIP, every coordinate of the calibrated importance clipped at κ / (lr · w) at each task start, κ = 0.5. The
code is SEC4's frozen `run_guard(variant="clip")`, imported from byte copies of `runs/sec4/frozen/`.

**Part C, the CRR-guided refinement (secondary).** Two candidates read from A6's bounded strength ("never an accumulated count": the
past importance averaged over settled tasks instead of summed), with and without SEC4's clip, were developed on the 22 SEEN
carriers under the gate D-GATE-C declared in `DEV_DECLARATION.md`. **D-GATE-C CLOSED** (D-ADDS fails; table below). Under
R12 Part C stops here: **no A6 arm is run on the fourth family**, and the ledger records one development row (SEC5-C-DEV).

**Not a CRR hypothesis.** SEC is the textbook Laplace weight with a units calibration; the clip is a step-size safeguard;
the A6 candidate is a tuning-free member of a published family (online EWC's down-weighting of accumulated Fisher terms,
`docs/citations/sec5_2026-09-29.md`). The ledger records the rows as "not a CRR rule". The registered CRR rule (Ω = 1) is
printed beside them (R7).

## The development stage (SEEN data only; `DEV_DECLARATION.md`, output `dev_SEC5.txt`)

| check | A6-MEAN | A6-MEAN-CLIP | SEC4's clip (reference) |
|---|---|---|---|
| D-ID (divisor forced to 1 equals SEC / SEC4's clip, synthetic stream, 5/5 seeds) | holds | holds | — |
| not behind the tuned λ on the 22 SEEN carriers | 18/22 | 22/22 | 22/22 |
| the six divergence carriers not behind | 2/6 | 6/6 | 6/6 |
| guard firings | 0 | 40 | — |
| mean over the 22 of (candidate − clip) | −2.6465 | −0.2021 | — |
| **CHOSEN** (most not behind; ties: fewer firings, then A6-MEAN) | | **A6-MEAN-CLIP** | |
| D-COUNT 22/22 (need 17), D-ID, D-FIXES 6/6 (need 4) | | hold | |
| D-ADDS (not behind on ≥ the clip's 22, **and** mean − clip ≥ 0) | | **FAILS** (−0.2021) | |
| **D-GATE-C** | | **CLOSED** | |

**What the development shows (a reading of `dev_SEC5.txt`, not evidence).**
- **Averaging does not remove divergence.** A6-MEAN, with no clip, lost a whole seed (0.00 or 18.54 %) on cnae-9, dionis,
  fabert, anneal and synthetic_control.
- **Accumulation is not the cause on every carrier.** anneal has K = 4, two tasks, so one settled task: the mean equals the
  sum and A6-MEAN equals unguarded SEC there (70.4494 both, the 18.54 % seed included). Divergence already happens with a
  single calibrated task, so the calibrated scale itself crosses the stability edge. The clip addresses that; A6's
  bounded-strength reading does not.
- **With the clip, averaging adds nothing.** A6-MEAN-CLIP matches the clip's 22/22 and 6/6 but sits 0.2021 below it on
  average.

This is development, not evidence: all 22 carriers were already SEEN, six of them are where divergence was found, and
the candidates were compared with the clip on them. Only the fourth family below can count. The per-carrier JSON lines
(`dev/dev_<study>_<id>.jsonl`) and the D-ID output (`dev/devid.txt`) are covered by the hash; the frozen scorer's
`devreport` reproduces `dev_SEC5.txt` from them.

## The fourth family and the carriers (`carrier_selection.txt`, from `studies/sec5/select_carriers.py`; metadata only)

**The family.** OpenML study 293, the AutoML Benchmark Training Datasets (2022), the first suite in the declared order.
It alone held 27 eligible datasets (need ≥ 8), so studies 454 and 445 were not pooled. 12 were kept by the declared
seeded draw (`default_rng(20260930)` over the sorted eligible ids). The study records and data lists of all three suites
are saved in this folder.

| OpenML id | name | rows | features | classes | K requested |
|---|---|---|---|---|---|
| 57 | hypothyroid | 3772 | 30 | 4 | 4 |
| 155 | pokerhand | 829201 | 11 | 10 | 10 |
| 1503 | spoken-arabic-digit | 263256 | 15 | 10 | 10 |
| 1509 | walking-activity | 149332 | 5 | 22 | 10 |
| 1529 | volcanoes-a3 | 1521 | 4 | 5 | 4 |
| 1530 | volcanoes-a4 | 1515 | 4 | 5 | 4 |
| 1532 | volcanoes-b2 | 10668 | 4 | 5 | 4 |
| 1541 | volcanoes-d4 | 8654 | 4 | 5 | 4 |
| 1549 | autoUniv-au6-750 | 750 | 41 | 8 | 8 |
| 41671 | microaggregation2 | 20000 | 21 | 5 | 4 |
| 41972 | Indian_pines | 9144 | 221 | 8 | 8 |
| 41982 | Kuzushiji-MNIST | 70000 | 785 | 10 | 10 |

**Two things the metadata already shows (stated now, before the data).**
- **Four carriers are from one survey.** volcanoes-a3, -a4, -b2 and -d4 are distinct image sets from the same Magellan
  volcano survey (JARtool), with the same four features. The declared rule counts them as four carriers (they do not share
  records, so SHARED does not apply). The score also prints, as a **report only**, SEC5-1 with the four counted as one
  carrier (their majority "not behind", ties counted as behind).
- **Some carriers may be excluded by the class rule.** hypothyroid's fourth class is tiny in the full table; pokerhand's
  higher classes are rare. The class rule (floor 40 after the 5000-row stratified cap, K lowered by two until it holds)
  decides; a carrier with K < 4 is excluded and counted.

Kuzushiji-MNIST is not an MNIST-family record set (Japanese cursive characters, not digits); it is eligible under the rule.

**Loading.** SCL3's loader and SEC1's class-selection rule, unchanged (SEC4's): rows with a missing value dropped; the
largest K classes; a class floor of 40; a 5000-row stratified cap (seed 777); K lowered by two until the floor holds.

**Exclusions.** A carrier with K < 4 after loading is excluded and counted. The rows are scored on the N carriers that
remain, with the denominator printed. **If N < 4, SEC5-1 is NOT DECIDABLE.**

**The data step.**
1. `data/fetch_openml.py --manifest sec5 <the twelve ids>`: md5 against the description; sha256 manifest.
2. `sec5_score.py check`.
3. `data/SEEN.md` gains the twelve in the same commit.

## Instrument (frozen in `runs/sec5/frozen/`)

- **`sec1_score.py`, `scl2_score.py`, `scl3_score.py`, `sec3_score.py`, `sec4_score.py`, `select_carriers.py`,
  `select_carriers_pmlb.py`.** Byte copies of `runs/sec4/frozen/` (SEC4's selection scripts are kept under their names).
- **`sec5_score.py`.** The A6 arm (`run_a6`), the development stage, the carriers, the scorer. `KAPPA = 0.5` (SEC4's),
  `KAPPA_CELLS = (0.25, 1.0)`, `C_CHOSEN = None`, and SEC4's `MIN_N = 4`, `DIV_FRAC = 0.5`, `THREE`, `SHARE`, `MIN_B`.
- **`sec5_select_carriers.py`.** This study's selection script. `CRR.md`, the theory at hash time.

**Per carrier, at seeds 0–4:**
- every SEC1 arm through SEC1's own `run_all`, unchanged: `fixed` (the tuned λ: SEC1's two-stage grid, 17 configurations,
  tuned in-sample on the scored seeds, which favours the baseline), `fixed_sec`, `bayes` (raw Laplace), `bayes_sec`
  (unguarded SEC), `bayes_s1`, `eq` (Ω = 1), and `bayes_sec` at the window cells;
- the clipped SEC (κ = 0.5) at the primary window (FS = FE = 0.1) and at SEC4's 3 retained window cells;
- the clip at κ = 0.25 and κ = 1.0 at the primary window (the κ sweep);
- no A6 arm (D-GATE-C closed).

**Timing.** Every configuration is timed (`time.process_time`) into `times_<id>.jsonl`, never into the results file (R9 cmp).

**The resolvable step.** Per carrier: max(1, 2 × SE over seeds of the tuned raw-λ arm), as in SEC1, SCL3, SEC3 and SEC4.

## Checks before the hash (covered by it)

- **`dev_SEC5.txt`** and **`dev/devid.txt`**: D-ID holds; D-GATE-C as printed.
- **SEC1's gate** (`prereg/sec3/gate_SEC3.txt`, sha256 in SEC3's hash) and SEC4's D-ID (`prereg/sec4/dev_SEC4.txt`): the
  primary arm is SEC4's code, unchanged.
- **`smokefull.txt`**: the whole pipeline on SEC1's synthetic stream. Its labels are meaningless for one carrier (SEC5-1
  prints NOT DECIDABLE there, N = 1 < 4).

## Hypotheses (verdicts computed by `sec5_score.py score`; one-sided "not behind", as in SEC1, SCL3, SEC3 and SEC4)

**N** is the number of scored carriers; need = ⌈0.75 N⌉ (SCL3-3's share).

| id | what is tested | criterion |
|---|---|---|
| **SEC5-1** (tuning-free; primary; the replication of SEC4-1) | clipped SEC (κ 0.5) − tuned λ > −step | PASS on ≥ need carriers; FAIL otherwise; NOT DECIDABLE if N < 4 |
| **SEC5-2** (no divergence) | no seed of the clipped SEC below 0.5 × the tuned λ's mean accuracy | PASS if no carrier has such a seed |
| **SEC5-T** (is the saving SEC's?) | B = carriers where a transferred λ (leave-one-carrier-out log-median of the other carriers' tuned λ, snapped to the coarse grid) is behind the tuned λ by a step | DECIDABLE if \|B\| ≥ 3; PASS if the clipped SEC is not behind on ≥ ⌈0.75 \|B\|⌉ of B |
| **SEC5-P** (against a cheap sweep) | clipped SEC − best of the 3-point sweep {1, 30, 1000} > −step | PASS on ≥ need carriers |
| **SEC5-S** (sensitivity, now with κ) | SEC5-1's per-carrier "not behind" over **5 cells**: SEC4's 3 retained window cells and κ ∈ {0.25, 1.0} | more than 1 flip in the 5 × N cells = FRAGILE |
| SEC5-C-DEV | the CRR-guided (A6) candidate's development gate on the 22 SEEN carriers | D-GATE-C CLOSED (above); recorded, not tested further (R12) |
| SEC5-K, SEC5-E, beside SEC5-1 | CPU seconds; guard firings; unguarded SEC, raw Laplace, Ω = 1 counts; the κ cells' divergence; SEC5-1 with the volcanoes counted once | report |

**Every per-carrier and per-seed value is printed (R6).** A non-finite run scores 0 and is kept. Calibration fallbacks are
counted, never excluded.

**What a PASS would be.**
- **PASS-0.** SEC5-1 passing is PASS-0 (R2–R9 as written).
- **PASS-1.** SEC5-1 is PASS-1 if also: SEC5-S is not fragile (at most 1 flip over the five cells, κ included); SEC5-2
  passes; the OTS anchor completes; the carriers' admissibility is as stated above.
- **PASS-2.** If SEC5-1 is PASS-1, **SEC4-1 and SEC5-1 together are PASS-2** for the clipped SEC (CLAUDE.md §7: PASS-1
  replicated on a second unseen family under a fresh prereg on a later day, with the same frozen code). The ledger rows
  reference each other. Nothing else in this study can reach PASS-2.

**What would change the reading.**
- **SEC5-1 FAILs.** SEC4's pass does not replicate; the clipped SEC is not tuning-free on a second new family.
- **SEC5-2 FAILs.** The clip does not remove divergence here.
- **SEC5-S FRAGILE.** The pass depends on κ = 0.5 or on the window, so a value was being tuned after all.
- **SEC5-T NOT DECIDABLE or FAIL.** The saving is not attributable to SEC on this family: a reused λ would do.
- **SEC5-P FAILs.** A 3-configuration sweep beats the clipped SEC.

## Anchoring

- **OpenTimestamps.** `HASH.txt` is stamped (`HASH.txt.ots`) before any fetch, and upgraded after Bitcoin confirmation.
- **The tag.** The signed tag is `prereg-sec5-2026-09-29`. If the tag push is refused, as for SCL3, SEC3 and SEC4, the push
  timestamp of the commit carrying `HASH.txt` and `HASH.txt.ots` is the git-side witness.

## Reproduction (on or after 2026-09-30 00:00 UTC)

```
uv run python data/fetch_openml.py --manifest sec5 57 155 1503 1509 1529 1530 1532 1541 1549 41671 41972 41982
uv run python runs/sec5/frozen/sec5_score.py check > runs/sec5/data_check.txt
for i in 57 155 1503 1509 1529 1530 1532 1541 1549 41671 41972 41982; do uv run python runs/sec5/frozen/sec5_score.py all $i --out runs/sec5/results_$i.jsonl; done
uv run python runs/sec5/frozen/sec5_score.py all 1549 --out runs/sec5/rerun_1549.jsonl --times runs/sec5/rerun_times_1549.jsonl && cmp runs/sec5/rerun_1549.jsonl runs/sec5/results_1549.jsonl   # R9
uv run python runs/sec5/frozen/sec5_score.py score runs/sec5/results_*.jsonl > runs/sec5/score.txt
```
