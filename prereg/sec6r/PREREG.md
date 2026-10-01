# Pre-registration: SEC6R, SEC6 run in full with a loader that reads STRING targets

**Study.**
- **Study id:** `sec6r`.
- **Written:** 2026-10-01 (UTC).
- **Why:** prompt-log entry 259 ("Yes, please run full SEC6 checks"), after SEC6 scored 0 of 12 carriers (ledger SEC6-*,
  `reports/sec6.md`, AGENT_LOG 241).

**What came before this file.**
- `DECLARATION.md` was pushed at 3d9502c, before any SEC6R code.
- The wrapper `studies/sec6r/sec6r_score.py` was then written, and D-ID-R held (`devid_r.txt`):
  - the patched loader is identical to the frozen one on all 38 SEEN carriers in SCL3, SEC3, SEC4 and SEC5's tables (the
    declaration said 30, the scored ones; the tables also hold the carriers their loaders excluded);
  - it reads a STRING target that the frozen loader drops;
  - SEC6's smoke run through the wrapper reproduces `prereg/sec6/smokefull.txt` outside its CPU-seconds line.
- `devid_r_frozen.txt` is the same check run from the frozen copy in `runs/sec6r/frozen/`.

**Timing (R3).**
- The loader change was defined on 2026-10-01 after SEC6's data.
- **No Part B carrier is fetched or opened before 2026-10-02T00:00Z.**
- This file, the declaration, the metadata, D-ID-R and the frozen scripts are hashed, OTS-stamped and pushed first.

## The one change

`_parse_rows_r` re-declares a STRING target as nominal, with its distinct non-missing field strings in sorted order as the
values, and calls SCL3's frozen `_parse_rows` on that. For every other target kind, it calls the frozen parser unchanged.

Nothing else changes:
- the arms, seeds, grids, clip (κ = 0.5; cells κ ∈ {0.25, 1.0} and SEC4's three window cells);
- the baselines SI-1, SI-1C, SI-0.1, AR1-P, AR1-B and raw Laplace;
- `fixed_clip`, `edge`, the d = 0 rule and the scorer.

All are SEC6's frozen code (`runs/sec6r/frozen/` holds byte copies of `runs/sec6/frozen/` plus the wrapper).

## Part B, the held-out test (primary)

**The carriers.** SEC7's metadata-only draw (`carrier_selection_sec7.txt`, a copy of `prereg/sec7/carrier_selection.txt`).
None is in `data/SEEN.md` today.

| OpenML id | name | K requested | target type (metadata) |
|---|---|---|---|
| 183 | abalone | 10 | nominal |
| 279 | meta_stream_intervals.arff | 10 | nominal |
| 1534 | volcanoes-b4 | 4 | nominal |
| 1538 | volcanoes-d1 | 4 | nominal |
| 1542 | volcanoes-e1 | 4 | nominal |
| 1552 | autoUniv-au7-1100 | 4 | nominal |
| 40985 | tamilnadu-electricity | 10 | nominal |
| 46608 | drug_reviews_druglib_com | 10 | string |
| 46684 | HolisticBias | 4 | string |
| 46709 | SOCC | 10 | string |
| 46745 | Advanced_IoT_Dataset | 6 | string |
| 46761 | mental_health_detection | 10 | string |

The target types come from OpenML's data-features API, fetched 2026-10-01 as metadata only (`feat_<id>.json`). Every carrier
declares at least one numeric or nominal feature.

**The hypotheses.** They are SEC6's (`prereg/sec6/PREREG.md`, the table "Hypotheses and thresholds" and the PASS-level
rules), renamed SEC6R-*:

| id | criterion (as SEC6) |
|---|---|
| SEC6R-G | instrument gate: `edge` (frozen after task 1) not behind the tuned λ on ≥ ⌈0.75 N⌉ → CLOSED; then SEC6R-1, B and P are UNINFORMATIVE and capped at PASS-0 |
| SEC6R-1 (primary) | clipped SEC (κ 0.5) − tuned λ > −step on ≥ ⌈0.75 N⌉ carriers; NOT DECIDABLE if N < 4 |
| SEC6R-1F | SEC6R-1 on carriers not floor-bound; NOT DECIDABLE if N_F < 4 |
| SEC6R-C / SEC6R-GC | clipped SEC against the tuned clipped λ, with its own instrument gate |
| SEC6R-B | clipped SEC not behind on strictly more carriers than SI-1, SI-1C, SI-0.1, AR1-P, AR1-B and raw Laplace each |
| SEC6R-T, SEC6R-2, SEC6R-P, SEC6R-S, SEC6R-K, SEC6R-E | as SEC6 |

**Added in advance (from AGENT_LOG 241).** Any line the scorer computes over 0 carriers or 0 cells is recorded as a vacuous
report with no level.

**PASS levels.** As SEC6:
- PASS-1 needs SEC6R-G OPEN, SEC6R-S not fragile, SEC6R-2 passing and the OTS anchor complete.
- PASS-2 would need SEC6R-1 PASS-1 together with SEC4-1, which itself has a failed replication (SEC5-1). Any PASS here is
  quoted beside SEC5-1 FAIL and SEC4-1-G.

## Part A, SEC6's own twelve (post hoc, seen data)

- **What it is.** The same wrapper on SEC6's twelve carriers, which have been SEEN since 2026-10-01.
- **When.** It runs only after this pre-registration is hashed and pushed.
- **Rows.** Ledger rows SEC6R-A-*, labelled "post hoc, seen data, no level" (rung R5 at most). It is never PASS-0: the loader
  change was learned on these carriers.

## Reproduction

Part A (2026-10-01, after the hash):

```
for i in 46584 46593 46597 46603 46652 46653 46676 46686 46708 46721 46737 46762; do uv run python runs/sec6r/frozen/sec6r_score.py all $i --part A --out runs/sec6r/partA/results_$i.jsonl; done
uv run python runs/sec6r/frozen/sec6r_score.py score runs/sec6r/partA/results_*.jsonl > runs/sec6r/partA/score.txt
```

Part B (on or after 2026-10-02T00:00Z):

```
uv run python data/fetch_openml.py --manifest sec6r 183 279 1534 1538 1542 1552 40985 46608 46684 46709 46745 46761
uv run python runs/sec6r/frozen/sec6r_score.py check --part B > runs/sec6r/data_check.txt
for i in 183 279 1534 1538 1542 1552 40985 46608 46684 46709 46745 46761; do uv run python runs/sec6r/frozen/sec6r_score.py all $i --part B --out runs/sec6r/results_$i.jsonl; done
uv run python runs/sec6r/frozen/sec6r_score.py all <one scored id> --part B --out runs/sec6r/rerun_<id>.jsonl && cmp runs/sec6r/rerun_<id>.jsonl runs/sec6r/results_<id>.jsonl   # R9
uv run python runs/sec6r/frozen/sec6r_score.py score runs/sec6r/results_*.jsonl > runs/sec6r/score.txt
```

The runs go three carriers at a time with `PYTHONDONTWRITEBYTECODE=1`, and every exit code is logged.

## Forecasts

These are as `DECLARATION.md`:
- SEC6R-G CLOSES on Part B;
- SEC6R-1 is not a PASS-1;
- at least 4 Part B carriers are scored.
