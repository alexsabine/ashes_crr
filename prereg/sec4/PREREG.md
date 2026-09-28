# Pre-registration — SEC4: a robust SEC (the stability-clipped Laplace weight) on a third unseen family

- **Study id:** `sec4`.
- **Written:** 2026-09-28 (UTC), after the development declaration was pushed (`DEV_DECLARATION.md`, commit bde17ab) and the
  development stage ran on SEEN carriers (`dev_SEC4.txt`). Prompt-log entry 228; AGENT_LOG 169.
- **Timing.**
  - This file, the development output, the frozen scorer and the smoke output are hashed, OTS-stamped and pushed before
    any carrier below is fetched.
  - The guard was chosen on SEEN data on 2026-09-28 (R3). **No carrier below is fetched or opened before 2026-09-29
    00:00 UTC**, and not before the hash and the stamp.

## What this study is

**The owner's request.** "Work on making this more robust as planned above and repeat the tests" (prompt-log entry 228).
"Above" is SEC3's report: SEC failed by divergence on cnae-9, dionis and fabert, and the next step named there was a fresh
pre-registration of a guarded rule on a third unseen family, with its gate re-declared before the data.

**The rule under test.** SEC (the Laplace weight w = 1/2 on a secant-calibrated Fisher; SEC1, SCL3, SEC3) with the
guard G-CLIP: at each task start, every coordinate of the calibrated importance is clipped at κ / (lr · w), κ = 0.5, so the
penalty step stays at half the explicit-Euler stability edge. Below the clip the code path is SEC's, bit for bit.
It is one configuration: no sweep.

**Not a CRR hypothesis.** SEC is the textbook Laplace weight with a units calibration; the clip is a step-size safeguard.
The ledger records the rows as "not a CRR rule". The registered CRR rule (Ω = 1) is printed beside it (R7).

## The development stage (SEEN data only; `DEV_DECLARATION.md`, output `dev_SEC4.txt`)

The declaration fixed three guards (G-RAW, G-CLIP, G-SCALE), the 16 SEEN carriers, the selection rule and the development
gate before any variant ran. Its output:

| check | result |
|---|---|
| D-ID (each guard with an infinite bound equals unguarded SEC on SEC1's synthetic stream) | holds for all three, 5/5 seeds |
| not behind the tuned λ on the 16 SEEN carriers | clip 16/16, scale 16/16, raw 15/16 (unguarded SEC 13/16, pinned) |
| the three divergence carriers not behind | clip 3/3, scale 3/3, raw 2/3 |
| tie-break (fewest firings where unguarded SEC was already not behind) | clip 51, scale 51; order clip, scale, raw |
| **CHOSEN** | **clip** |
| D-COUNT 16/16 (need 12), D-ID, D-FIXES 3/3 (need 2) | **D-GATE OPEN** |

This is development, not evidence: every one of the 16 carriers was already SEEN, and three of them are where the failure
was found. Only the third family below can count. `dev_SEC4.txt` was produced before the scorer took its final form (the
test-family loader and two named constants were added after); the frozen scorer's `dev` reproduces it (the rerun is
compared byte for byte and the comparison is committed as `dev_rerun_cmp.txt`, covered by the hash).

## The third family and the carriers (`carrier_selection.txt`, from `studies/sec4/select_carriers.py`; metadata only)

**PMLB is exhausted.** `carrier_selection_pmlb.txt` (from `studies/sec4/select_carriers_pmlb.py` on PMLB's own summary
table): only two PMLB classification sets pass the rule and are not SEEN (solar_flare_2, kddcup), too few for a study.

**The family.** The pooled OpenML benchmark suites that are neither CC18 (SCL3's family) nor the AutoML Benchmark suite of
study 271 (SEC3's family): study 14 (OpenML-100, 2017), study 218 (AutoML Benchmark 2019), study 379 (TabZilla Hard) and
study 457 (TabArena v0.1). The study records and one data list (qualities) are saved in this folder; 183 distinct data ids.
OpenML-100's record first timed out on 2026-09-28 and was fetched on a retry the same day, before any selection ran on it.

**The selection.** SCL3's rule with SEC3's two additions, unchanged: active ARFF; at least 4 classes; 400 to 1,000,000
rows; at most 1001 features; not SEEN by OpenML id, by name or by shared records (aliases); K requested the largest even
number ≤ min(classes, 10). **One addition, declared here:** datasets that hold the same records under different feature
sets count once (the lowest OpenML id is kept), so that N counts independent record sets. It removes
one-hundred-plants-shape and -texture (the margin set is kept), the analogue of the mfeat rule.

| OpenML id | name | suites | rows | features | classes | K requested |
|---|---|---|---|---|---|---|
| 46906 | anneal | 457 | 898 | 39 | 5 | 4 |
| 1459 | artificial-characters | 14, 379 | 10218 | 8 | 10 | 10 |
| 1466 | cardiotocography | 14 | 2126 | 36 | 10 | 10 |
| 23380 | cjs | 14 | 2796 | 35 | 6 | 6 |
| 1476 | gas-drift | 14 | 13910 | 129 | 6 | 6 |
| 375 | JapaneseVowels | 14 | 9961 | 15 | 9 | 8 |
| 46980 | MIC | 457 | 1699 | 112 | 8 | 8 |
| 1491 | one-hundred-plants-margin | 14 | 1600 | 65 | 100 | 10 |
| 377 | synthetic_control | 14 | 600 | 61 | 6 | 6 |

**Loading.** SCL3's loader and SEC1's class-selection rule, unchanged: rows with a missing value dropped; the largest K
classes; a class floor of 40; a 5000-row stratified cap (seed 777); K lowered by two until the floor holds. cjs and MIC
carry missing values, and anneal and one-hundred-plants-margin have small classes, so the class rule may exclude them.

**Exclusions.** A carrier with K < 4 after loading is excluded and counted. The rows are scored on the N carriers that
remain, with the denominator printed. **If N < 4, SEC4-1 is NOT DECIDABLE.**

**The data step.**
1. `data/fetch_openml.py --manifest sec4 <the nine ids>`: md5 against the description; sha256 manifest.
2. `sec4_score.py check`.
3. `data/SEEN.md` gains the nine in the same commit.

## Instrument (frozen in `runs/sec4/frozen/`)

- **`sec1_score.py`, `scl2_score.py`, `scl3_score.py`, `sec3_score.py`.** Byte copies of `runs/sec3/frozen/`.
- **`sec4_score.py`.** The guard (`run_guard`), the development stage, the carriers, the scorer. `CHOSEN = "clip"`,
  `KAPPA = 0.5`, `RAW_BOUND = 1.0`, `MIN_N = 4`, `DIV_FRAC = 0.5`.
- **`select_carriers.py`, `select_carriers_pmlb.py`.** The selection scripts. `CRR.md`, the theory at hash time.

**Per carrier, at seeds 0–4:**
- every SEC1 arm through SEC1's own `run_all`, unchanged: `fixed` (the tuned λ: SEC1's two-stage grid, 17 configurations,
  tuned in-sample on the scored seeds, which favours the baseline), `fixed_sec`, `bayes` (raw Laplace), `bayes_sec`
  (unguarded SEC), `bayes_s1`, `eq` (Ω = 1), and `bayes_sec` at the window cells;
- the clipped SEC at the primary window (FS = FE = 0.1) and at SEC3's 3 retained window cells;
- G-SCALE and G-RAW at the primary window (reports).

**Timing.** Every configuration is timed (`time.process_time`) into `times_<id>.jsonl`, never into the results file (R9 cmp).

**The resolvable step.** Per carrier: max(1, 2 × SE over seeds of the tuned raw-λ arm), as in SEC1, SCL3 and SEC3.

## Checks before the hash (covered by it)

- **`dev_SEC4.txt`**: D-GATE OPEN (above).
- **SEC1's gate** (`prereg/sec3/gate_SEC3.txt`, sha256 in SEC3's hash): POS and INV hold, SHAPE fails as required. The clip
  does not change what that gate tests: below the clip SEC is unchanged (D-ID).
- **`smokefull.txt`**: the whole pipeline on SEC1's synthetic stream. Its labels are meaningless for one carrier (SEC4-1
  prints NOT DECIDABLE there, N = 1 < 4).

## Hypotheses (verdicts computed by `sec4_score.py score`; one-sided "not behind", as in SEC1, SCL3 and SEC3)

**N** is the number of scored carriers; need = ⌈0.75 N⌉ (SCL3-3's share).

| id | what is tested | criterion |
|---|---|---|
| **SEC4-1** (tuning-free; primary) | clipped SEC − tuned λ > −step | PASS on ≥ need carriers; FAIL otherwise; NOT DECIDABLE if N < 4 |
| **SEC4-2** (no divergence) | no seed of the clipped SEC below 0.5 × the tuned λ's mean accuracy | PASS if no carrier has such a seed |
| **SEC4-T** (is the saving SEC's?) | B = carriers where a transferred λ (leave-one-carrier-out log-median of the other carriers' tuned λ, snapped to the coarse grid) is behind the tuned λ by a step | DECIDABLE if \|B\| ≥ 3; PASS if the clipped SEC is not behind on ≥ ⌈0.75 \|B\|⌉ of B. If NOT DECIDABLE, the report says a reused λ would have saved the sweep without SEC |
| **SEC4-P** (against a cheap sweep) | clipped SEC − best of the 3-point sweep {1, 30, 1000} > −step (1 configuration against 3) | PASS on ≥ need carriers |
| **SEC4-S** | SEC4-1's "not behind" over the 3 retained window cells × N | more than 1 flip = FRAGILE |
| SEC4-K | configurations (full sweep, clipped SEC) and measured CPU seconds; overhead against raw Laplace | report |
| SEC4-E and beside SEC4-1 | guard firings; unguarded SEC, raw Laplace, Ω = 1, G-SCALE, G-RAW counts | report |

**Every per-carrier and per-seed value is printed (R6).** A non-finite run scores 0 and is kept. Calibration fallbacks are
counted, never excluded.

**What a PASS would be.**
- **PASS-0.** SEC4-1 passing is PASS-0 for the clipped SEC (R2–R9 as written).
- **PASS-1.** SEC4-1 is PASS-1 if also: SEC4-S is not fragile; SEC4-2 passes (no divergence, the failure the clip is for);
  the OTS anchor completes; the carriers' admissibility is as stated above.
- **PASS-2.** Not reachable in this study: the clipped rule has no earlier held-out pass. A PASS-1 here would need a
  replication on a fourth unseen family, under a fresh prereg on a later day, to become PASS-2.

**What would change the reading.**
- **SEC4-1 FAILs.** The clip does not make SEC tuning-free on a new family; the dev result was fitted to SEEN carriers.
- **SEC4-2 FAILs.** The clip does not remove divergence.
- **SEC4-T NOT DECIDABLE or FAIL.** The saving is not attributable to SEC on this family: a reused λ would do.
- **SEC4-P FAILs.** A 3-configuration sweep beats the clipped SEC.

## Anchoring

- **OpenTimestamps.** `HASH.txt` is stamped (`HASH.txt.ots`) before any fetch, and upgraded after Bitcoin confirmation.
- **The tag.** The signed tag is `prereg-sec4-2026-09-28`. If the tag push is refused, as for SCL3 and SEC3, the push
  timestamp of the commit carrying `HASH.txt` and `HASH.txt.ots` is the git-side witness.

## Reproduction (on or after 2026-09-29 00:00 UTC)

```
uv run python data/fetch_openml.py --manifest sec4 46906 1459 1466 23380 1476 375 46980 1491 377
uv run python runs/sec4/frozen/sec4_score.py check > runs/sec4/data_check.txt
for i in 46906 1459 1466 23380 1476 375 46980 1491 377; do uv run python runs/sec4/frozen/sec4_score.py all $i --out runs/sec4/results_$i.jsonl; done
uv run python runs/sec4/frozen/sec4_score.py all 377 --out runs/sec4/rerun_377.jsonl --times runs/sec4/rerun_times_377.jsonl && cmp runs/sec4/rerun_377.jsonl runs/sec4/results_377.jsonl   # R9
uv run python runs/sec4/frozen/sec4_score.py score runs/sec4/results_*.jsonl > runs/sec4/score.txt
```
