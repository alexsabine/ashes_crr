# SEC6R declaration: SEC6 run in full with a loader that reads STRING targets (pushed before any SEC6R code)

**The request.** Prompt-log entry 259 (2026-10-01T00:53:15Z): "Yes, please run full SEC6 checks".

**Why SEC6R exists.**
- SEC6 (`reports/sec6.md`, ledger SEC6-*) scored 0 of 12 carriers. Every suite-454 carrier declares its target as an ARFF
  STRING attribute. SCL3's loader, frozen unchanged through SEC6, reads a STRING target as a number and drops every row.
- A scorer changed after its hash voids its study (CLAUDE.md §8). So SEC6 cannot be re-run under its own hash. Its twelve
  carriers are now SEEN.
- SEC6R runs SEC6's design in full with exactly one change, the loader.

**Status.** Not a CRR rule. SEC is the Laplace weight with a units calibration; the clip is AR1's step-size safeguard (SPA1).
CRR's Ω = 1 rule is printed beside it (R7).

## The one change (fixed now)

**The loader reads a STRING target as a class label.**
- When the target attribute is declared `string`, its distinct non-missing values, sorted as strings, become the class
  indices 0, 1, 2, …, exactly as a nominal target's declared values do.
- Everything else in the loader is unchanged:
  - only numeric and nominal features are used; string and date features are not;
  - rows with a missing or unreadable value in a used column are dropped and counted;
  - SEC1's class selection, 5000-row cap and class floor of 40 apply;
  - SEC6's d = 0 rule (Amendment 1) excludes a carrier with no usable feature.
- **Applied from outside the frozen files.** `studies/sec6r/sec6r_score.py` imports SEC6's frozen scorer
  (`runs/sec6/frozen/sec6_score.py`) by path and replaces only the loader's row parser (`_parse_rows`) with one that handles
  a STRING target and calls the frozen parser unchanged for every other target kind. Nothing else is touched: the arms,
  the seeds, the grid, the clip, the baselines, `edge`, the gates and the scorer are SEC6's, byte for byte.

**Checks before the hash (D-ID-R, on SEEN data and synthetic data only):**
1. **Identity.** On every SEEN carrier whose target is nominal (the 30 carriers of SCL3, SEC3, SEC4 and SEC5), the patched
   loader returns the same matrices, labels and header as the frozen loader, bit for bit.
2. **A STRING target is read.** On a synthetic ARFF with a STRING target, the patched loader returns the declared classes
   and the frozen loader drops every row.
3. **Smoke.** SEC6's `smokefull` runs through the wrapper and reproduces SEC6's pinned smoke output
   (`prereg/sec6/smokefull.txt`) byte for byte.

If any of these fails, SEC6R stops before the hash and the failure is recorded.

## Part B, the held-out test (primary; pre-registered and hashed today)

- **The family.** The twelve carriers SEC7's metadata-only selection drew (`prereg/sec7/carrier_selection.txt`; SEC7 stopped
  at its development gate, so they were never fetched or opened). Their ids are 183, 279, 1534, 1538, 1542, 1552, 40985,
  46608, 46684, 46709, 46745 and 46761, from OpenML studies 445, 454 and 293. None is in `data/SEEN.md`.
- **Their declared feature types,** fetched today as metadata only (OpenML's data-features API; `prereg/sec6r/feat_*.json`):
  - seven declare a nominal target;
  - five declare a STRING target;
  - every one declares at least one numeric or nominal feature.
- **The hypotheses, thresholds, gates and PASS levels are SEC6's,** as written in `prereg/sec6/PREREG.md`:
  - SEC6-G (the instrument gate);
  - SEC6-1 (primary), SEC6-1F, SEC6-C with SEC6-GC, SEC6-B, SEC6-T, SEC6-2, SEC6-P, SEC6-S, SEC6-K and SEC6-E.
  - In the ledger they are named SEC6R-*.
- **One rule is added in advance:** any line the scorer computes over 0 carriers or 0 cells is recorded as a vacuous report
  with no level (AGENT_LOG 241).
- **Timing (R3).** The loader change was defined on 2026-10-01 after SEC6's data. So Part B's data step is on or after
  **2026-10-02T00:00Z**. The pre-registration is hashed, OTS-stamped and pushed today, before any Part B carrier is fetched.

## Part A, SEC6's own carriers (post hoc, seen data; runs only after Part B's hash)

- SEC6R's scorer runs on SEC6's twelve carriers, which are now SEEN.
- **What it is.** A confirmatory run on seen data (rung R5). It is never PASS-0: the loader change was learned on these very
  carriers today.
- **Rows.** Ledger rows SEC6R-A-*, each labelled "post hoc, seen data, no level".
- **Why it runs after the hash.** Part B's hash is pushed first, so nothing seen in Part A can shape Part B.

## Forecasts (written now)

1. **D-ID-R holds:** identity on all 30 nominal-target carriers.
2. **SEC6R-G CLOSES on Part B.** As on SEC4, SEC3 and SEC5's carriers, a learner frozen after task 1 will be not behind the
   tuned λ on at least ¾ of them, so SEC6R-1, B and P are UNINFORMATIVE and capped at PASS-0.
3. **SEC6R-1 is not a PASS-1.**
4. **At least 4 Part B carriers are scored.**
