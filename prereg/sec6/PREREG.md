# Pre-registration: SEC6, SEC4's clipped SEC on a fifth unseen family, against the published tuning-free baselines and a tuned λ given the same clip

**Study.**
- **Study id:** `sec6`.
- **Written:** 2026-09-30 (UTC).
- **Why:** prompt-log entry 257 ("We should then run more tests on sec4"), P2 of `Applied_Suite/PROGRAMME.md`; AGENT_LOG
  214, 217, 218 and 219.

**What came before this file.**
- The development declaration was pushed at 66ff6c7 (`DEV_DECLARATION.md`).
- Its Amendment 1 (4e5f009) and Amendment 2 (e15e1ff) were pushed before their changes were coded.
- The development stage ran on SEEN carriers (`dev_SEC6.txt`).
- The carrier selection ran on metadata only (`carrier_selection.txt`).

**Timing.** This file, the development outputs, the selection, the frozen scorer and the smoke output are hashed,
OTS-stamped and pushed before any carrier below is fetched. **No carrier below is fetched or opened before 2026-10-01
00:00 UTC.** Under R3, SI-1C, the d = 0 rule and `fixed_clip` were fixed on SEEN data on 2026-09-30.

## What this study is

**Part R, the replication (primary).** SEC4's clipped SEC, unchanged:
- SEC is the Laplace weight w = 1/2 on a secant-calibrated Fisher.
- Its guard G-CLIP clips every coordinate of the calibrated importance at κ / (lr · w) at each task start, with
  κ = 0.5.
- The code is SEC4's frozen `run_guard(variant="clip")`, from byte copies of `runs/sec5/frozen/`, which are themselves byte
  copies of SEC4's.
- **SEC6-1 is SEC4-1's criterion, unchanged:** not behind the tuned λ, SEC1's two-stage grid on the raw Fisher without a
  clip.

**Part B, the published baselines** (`DEV_DECLARATION.md`, Amendment 1). Each maps its paper's penalty onto SEC1's learner:

| arm | the rule |
|---|---|
| **SI-1** | Synaptic Intelligence at the paper's principled strength c = 1, ξ = 10⁻³; as published, with no guard |
| **SI-1C** | SI-1 with Ω floored at 0 and clipped by SEC4's clip. Added after SI-1 ran away on SEEN data. |
| **SI-0.1** | the paper's permuted-MNIST pair, c = 0.1 and ξ = 0.1 |
| **AR1-P** | AR1 as published: the averaged Fisher clipped at maxF = 0.001, λ = 1/(η · maxF) |
| **AR1-B** | AR1's bound used as the strength on the raw Fisher's own maximum |
| **raw Laplace** | SEC1's `bayes` |

**Part C, the reference given the same clip** (Amendment 2).
- **`fixed_clip`** is SEC1's two-stage grid on the raw Fisher, each λ with SEC4's clip at κ / (lr · λ).
- **SEC6-C** asks whether the clipped SEC is tuning-free against this reference.
- **Why it was added.** On SEEN data the tuned clipped λ is ahead of the unclipped tuned λ by more than a step on 10/30
  carriers and behind on 2/30 (pokerhand, volcanoes-d4). Part of any clipped arm's margin over the unclipped reference
  may be the clip's.

**Part M, the P1-conditional arms.** Stated below, from `SEC_Analysis/checks/m_checks.json` by the rule fixed in
`SEC_Analysis/DECLARATION.md`.

**Not a CRR hypothesis.**
- SEC is the textbook Laplace weight with a units calibration, and the clip is a step-size safeguard (AR1's, SPA1).
- The ledger records the rows as "not a CRR rule". The registered CRR rule (Ω = 1) is printed beside them (R7).

## Part M: the P1-conditional arms (from `SEC_Analysis/checks/m_checks.json`)

PENDING: filled from the pinned P1 output before the hash, by the rule in `SEC_Analysis/DECLARATION.md`.

## The development stage (SEEN data only; `DEV_DECLARATION.md`; output `dev_SEC6.txt`)

**D-ID holds (14/14).** The clipped SEC through SEC6's harness equals SEC4's and SEC5's pinned `bayes_sec_clip`, seed 0,
bit for bit. SEC1's `bayes_sec` also matches on 2/2.

**D-MAP holds.**
- SI with c = 0 equals fine-tuning bit for bit (5/5).
- AR1-B's largest lr · 2w · imp = 1 at every task start.
- AR1-P's importance never exceeds 0.001.
- `fixed_clip` with κ = ∞ equals SEC1's `fixed` (10/10).

**D-RUN on the 30 SEEN carriers, seeds 0–4.** Not evidence; nothing chosen by count.

| arm | not behind the tuned λ | not behind the tuned clipped λ | carriers with a divergent seed |
|---|---|---|---|
| SI-1 | 0/30 | 1/30 | 29 |
| SI-1C | 28/30 | 30/30 | 2 |
| SI-0.1 | 21/30 | 15/30 | 2 |
| AR1-P | 25/30 | 20/30 | 3 |
| AR1-B | 27/30 | 19/30 | 2 |
| clipped SEC (pinned) | 26/30 | 22/30 | 2 |
| raw Laplace (pinned) | 14/30 | 11/30 | 2 |
| unguarded SEC (pinned) | 20/30 | 20/30 | 8 |

**What the development already suggests (a reading, not evidence).**
- On SEEN data the clipped SI is at least as good as the clipped SEC on every carrier count.
- The clip turns a runaway penalty (SI-1: 0/30) into the strongest arm (28/30 and 30/30).
- The tuned clipped λ sits at the top of SEC1's grid on 11/30, so the grid may not reach its optimum. The grid is kept as
  declared.
- **Every forecast of the development declaration about the baselines is wrong on SEEN data.** Forecast 2 said SI-1 would
  be the strongest baseline. The forecasts are recorded as written.

## The fifth family and the carriers (`carrier_selection.txt`, from `studies/sec6/select_carriers.py`, frozen as `sec6_select_carriers.py`; metadata only)

**The family.** OpenML study 454 (New_OpenML_Suite_2025_classification), the first suite in the declared order. It alone
held 19 eligible datasets (need ≥ 8), so study 445 was not pooled. 12 were kept by the declared seeded draw,
`default_rng(20261001)` over the sorted eligible ids. The study records and data lists of both suites are saved in this
folder.

| OpenML id | name | K requested |
|---|---|---|
| 46584 | Student_Performance_on_an_Entrance_Examination | 4 |
| 46593 | HCV_data | 4 |
| 46597 | Estimation_of_Obesity_Levels | 6 |
| 46603 | regensburg_pediatric_appendicitis | 4 |
| 46652 | news_channel | 6 |
| 46653 | wine_reviews | 10 |
| 46676 | WBCAtt | 4 |
| 46686 | DBPedia | 10 |
| 46708 | Wikipedia_Talk_Labels | 10 |
| 46721 | Mental_Health_Dataset | 4 |
| 46737 | agriculture_dataset_karnataka | 10 |
| 46762 | air-quality-and-pollution-assessment | 4 |

**What the metadata already shows (stated now, before the data).**
- **d = 0 risk.** Student_Performance, WBCAtt and Mental_Health list no numeric or symbolic feature. If SCL3's loader
  keeps no feature, the d = 0 rule excludes them. DBPedia keeps 1 numeric feature (d = 1, not excluded).
- **Missing values.** regensburg has a missing value in every row, so the missing-value rule is likely to exclude it.
- **The class rule.** HCV_data's smallest class is 7 of 615 rows, so the class rule is likely to lower K.
- **Imbalance.** Wikipedia_Talk_Labels' majority class is 715,135 of 855,514 rows.
- **Consequence.** N may fall well below 12. If N < 4, SEC6-1, SEC6-B and SEC6-C are NOT DECIDABLE.

**Loading.** SCL3's loader and SEC1's class-selection rule, unchanged (SEC4's and SEC5's):
- rows with a missing value are dropped;
- the largest K classes are kept;
- the class floor is 40;
- there is a 5000-row stratified cap (seed 777);
- K is lowered by two until the floor holds.

**Exclusions.**
- A carrier with K < 4, or with no usable feature (d = 0), after loading is excluded and counted.
- The rows are scored on the N carriers that remain, with the denominator printed.

**The data step.**
1. `data/fetch_openml.py --manifest sec6 <the twelve ids>`: md5 against the description; sha256 manifest.
2. `sec6_score.py check`.
3. `data/SEEN.md` gains the twelve in the same commit.

## Instrument (frozen in `runs/sec6/frozen/`)

- **Byte copies of `runs/sec5/frozen/`:** `sec1_score.py`, `scl2_score.py`, `scl3_score.py`, `sec3_score.py`,
  `sec4_score.py`, `sec5_score.py`, `select_carriers.py`, `select_carriers_pmlb.py` and `sec5_select_carriers.py`.
- **`sec6_score.py`:** the baseline arms (`run_b`), `fixed_clip`, the d = 0 rule and its self-test, the development stage
  and the scorer. Its registered constants are `KAPPA = 0.5`, `KAPPA_CELLS = (0.25, 1.0)`, `MIN_N = 4`,
  `DIV_FRAC = 0.5`, and SEC5's `THREE`, `SHARE` and `MIN_B`.
- **`sec6_select_carriers.py`:** this study's selection script.
- **`CRR.md`:** the theory at hash time.
- **The M-arm module,** if any P1 arm is carried (stated below).

**Per carrier, at seeds 0–4:**
- every SEC1 arm through SEC1's own `run_all`, unchanged:
  - `fixed`: the tuned λ, SEC1's two-stage grid of 17 configurations, tuned in-sample on the scored seeds, which favours
    the baseline;
  - `fixed_sec`, `bayes`, `bayes_sec`, `bayes_s1` and `eq`;
  - `bayes_sec` at the window cells;
- the clipped SEC at the primary window, at SEC4's 3 retained window cells, and at κ ∈ {0.25, 1.0};
- SI-1, SI-1C, SI-0.1, AR1-P and AR1-B at the primary window;
- `fixed_clip` on SEC1's two-stage grid;
- the carried P1 arms.

**Timing.** Every configuration is timed into `times_<id>.jsonl`, never into the results file (R9 `cmp`).

**The resolvable step.** Per carrier:
- `step` = max(1, 2 × SE over seeds) of the tuned raw-λ arm;
- `step_c` = the same for the tuned clipped λ.

## Hypotheses (verdicts computed by `sec6_score.py score`; one-sided "not behind", as in SEC1, SCL3, SEC3, SEC4 and SEC5)

N is the number of scored carriers, and need = ⌈0.75 N⌉ (SCL3-3's share).

| id | what is tested | criterion |
|---|---|---|
| **SEC6-1** (primary; the replication of SEC4-1) | clipped SEC (κ 0.5) − tuned λ > −step | PASS on ≥ need carriers; FAIL otherwise; NOT DECIDABLE if N < 4 |
| **SEC6-C** (tuning-free against the same guard) | clipped SEC − tuned clipped λ > −step_c | PASS on ≥ need; FAIL; NOT DECIDABLE if N < 4 |
| **SEC6-B** (the calibration against the published rules) | the clipped SEC is not behind the tuned λ on **strictly more** carriers than each of SI-1, SI-1C, SI-0.1, AR1-P, AR1-B, raw Laplace and every carried P1 arm | PASS only if it beats every one; FAIL otherwise; NOT DECIDABLE if N < 4 |
| **SEC6-2** (no divergence) | no seed of the clipped SEC below 0.5 × the tuned λ's mean | PASS if no carrier has such a seed |
| **SEC6-T** (is the saving SEC's?) | B = carriers where a transferred λ (leave-one-carrier-out log-median, snapped to the coarse grid) is behind the tuned λ by a step | DECIDABLE if \|B\| ≥ 3; PASS if the clipped SEC is not behind on ≥ ⌈0.75 \|B\|⌉ of B |
| **SEC6-P** (against a cheap sweep) | clipped SEC − best of the 3-point sweep {1, 30, 1000} > −step | PASS on ≥ need |
| **SEC6-S** (sensitivity) | SEC6-1's per-carrier "not behind" over 5 cells: SEC4's 3 retained window cells and κ ∈ {0.25, 1.0} | more than 1 flip in the 5 × N cells = FRAGILE |
| SEC6-K, SEC6-E | CPU seconds (including the clipped sweep's); firings, per arm | report |

**Printed beside the verdicts.**
- Every per-carrier and per-seed value (R6).
- Every baseline against both references.
- The tuned clipped λ against the tuned λ.
- The count of carriers at the top of the clipped grid.
- **The clipped SEC's family record:** SEC4-1 PASS-1, SEC5-1 FAIL, SEC6-1.

A non-finite run scores 0 and is kept. Calibration fallbacks are counted, never excluded.

## What a PASS would be

- **PASS-0.** SEC6-1 or SEC6-C passing is PASS-0 (R2–R9 as written).
- **PASS-1.** SEC6-1 is PASS-1 if also all of these hold:
  - SEC6-S is not fragile;
  - SEC6-2 passes;
  - the OTS anchor completes;
  - the carriers' admissibility is as stated.

  SEC6-C is PASS-1 under the same conditions. Its sensitivity is read on the same 5 cells against the tuned clipped λ.
- **PASS-2.** If SEC6-1 is PASS-1, SEC4-1 and SEC6-1 together are PASS-2 **by the letter of CLAUDE.md §7**: PASS-1
  replicated on a second unseen family under a fresh pre-registration on a later day, with the same frozen code.
  - **The row must print that SEC5-1 FAILED on the fourth family,** so the clipped SEC's family record is 2 of 3.
  - **If SEC6-C fails at the same time,** the row must also print "SEC6-1 rests on the clip (SEC6-C fails)".
  - The ladder prints the failures of the same kind beside it. Nothing else in this study can reach PASS-2.

## What would change the reading

| result | reading |
|---|---|
| SEC6-1 FAIL | the clipped SEC is not tuning-free on a third new family (two of three would then fail) |
| SEC6-1 PASS, SEC6-C FAIL | the pass rests on the clip: a tuned λ given the same guard beats it |
| SEC6-B FAIL | a published tuning-free rule does at least as well. On SEEN data SI-1C and AR1-B already do. The calibration is then not what makes the clipped SEC work. |
| SEC6-S FRAGILE | the pass depends on κ or on the window |
| SEC6-T NOT DECIDABLE or FAIL | a reused λ would have saved the sweep without SEC |

## Anchoring

- **OpenTimestamps.** `HASH.txt` is stamped (`HASH.txt.ots`) before any fetch, and upgraded after Bitcoin confirmation.
- **The tag.** The signed tag is `prereg-sec6-2026-09-30`. If the tag push is refused, as for SCL3, SEC3, SEC4 and SEC5, the
  push timestamp of the commit carrying `HASH.txt` and `HASH.txt.ots` is the git-side witness.

## Reproduction (on or after 2026-10-01 00:00 UTC)

```
uv run python data/fetch_openml.py --manifest sec6 46584 46593 46597 46603 46652 46653 46676 46686 46708 46721 46737 46762
uv run python runs/sec6/frozen/sec6_score.py check > runs/sec6/data_check.txt
for i in 46584 46593 46597 46603 46652 46653 46676 46686 46708 46721 46737 46762; do uv run python runs/sec6/frozen/sec6_score.py all $i --out runs/sec6/results_$i.jsonl --times runs/sec6/times_$i.jsonl; done
uv run python runs/sec6/frozen/sec6_score.py all <one scored id> --out runs/sec6/rerun_<id>.jsonl --times runs/sec6/rerun_times_<id>.jsonl && cmp runs/sec6/rerun_<id>.jsonl runs/sec6/results_<id>.jsonl   # R9
uv run python runs/sec6/frozen/sec6_score.py score runs/sec6/results_*.jsonl > runs/sec6/score.txt
```
