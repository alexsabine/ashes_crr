# SEC6R: SEC6 run in full with a loader that reads STRING targets

**How it was set up.**
- **The request.** Prompt-log entry 259 ("Yes, please run full SEC6 checks"), after SEC6 scored 0 of 12 carriers
  (`reports/sec6.md`).
- **The declaration.** `prereg/sec6r/DECLARATION.md` was pushed at 3d9502c before any SEC6R code.
- **The one change.** The loader reads an ARFF STRING target as a class label. Its sorted distinct values are re-declared
  nominal, and SCL3's frozen parser then runs on them. Everything else is SEC6's frozen code, imported by path
  (`runs/sec6r/frozen/sec6r_score.py`).
- **D-ID-R held** (`prereg/sec6r/devid_r.txt`, and the same from the frozen copy):
  - identity on 38/38 SEEN carriers;
  - a synthetic STRING target read (240 rows kept, where the frozen loader drops all 240);
  - SEC6's smoke run reproduced outside its CPU-seconds line.
- **The pre-registration.** `prereg/sec6r/PREREG.md`, HASH.txt sha256 dc9c64d7…, prereg commit 20f7d06 pushed
  2026-10-01T01:08:02Z.
  - OpenTimestamps was stamped at 01:08Z; completion is pending.
  - The signed tag was created, but its push was refused (`runs/sec6r/tag_attempt.txt`).
- **Two parts.**
  - **Part B** is the held-out test on SEC7's metadata-only draw of 12. Its data step is on or after 2026-10-02T00:00Z.
  - **Part A** is SEC6's own twelve carriers, SEEN, post hoc. It ran only after Part B's hash was pushed.

## Part A: SEC6's own carriers (post hoc, seen data, no level)

This section is written after ledger rows SEC6R-A-G … SEC6R-A-K and quotes them.
- **The scoring.** `runs/sec6r/partA/score.txt`. The rerun of Estimation_of_Obesity_Levels is byte-identical
  (`runs/sec6r/partA/rerun_cmp.txt`).
- **The runs.** All twelve exited 0 (`runs/sec6r/partA/exits.txt`).
- **Seven carriers scored:** DBPedia, Estimation_of_Obesity_Levels, Wikipedia_Talk_Labels, agriculture_dataset_karnataka,
  air-quality-and-pollution-assessment, news_channel and wine_reviews.
- **Five were excluded by the registered loader:**
  - Student_Performance_on_an_Entrance_Examination, WBCAtt and Mental_Health_Dataset have no usable feature (the d = 0 rule);
  - HCV_data falls below the class floor;
  - regensburg_pediatric_appendicitis has a missing feature in every row.

**The answer. The gate closes, so the passes say nothing.** A learner frozen after task 1 is not behind the tuned λ on 7/7.
On six of the seven it is ahead by more than a step, by up to +49.6200 points (Wikipedia_Talk_Labels). On these carriers the
criterion "not behind the tuned λ" cannot fail. So the clipped SEC's 6/7 is UNINFORMATIVE. It is also post hoc on seen data,
so it carries no level.

| row | question | observed | verdict |
|---|---|---|---|
| SEC6R-A-G | is the criterion failed by the frozen learner? | edge not behind 7/7 (closes at 6) | gate CLOSED (report) |
| SEC6R-A-1 | clipped SEC not behind the tuned λ | 6/7 (need 6); behind on air-quality (−2.9400, step 1.00) | PASS as printed; seen, post hoc, no level, UNINFORMATIVE |
| SEC6R-A-1F | the same, on carriers not floor-bound | N_F = 2 of 7; 1/2 | NOT DECIDABLE |
| SEC6R-A-C | clipped SEC against the tuned clipped λ | 6/7; its gate GC CLOSED (edge 7/7) | PASS as printed; UNINFORMATIVE |
| SEC6R-A-B | does the clipped SEC beat every published baseline? | clipped SEC 6/7; SI-1 0/7, SI-0.1 7/7, AR1-P 6/7, AR1-B 6/7, SI-1C 7/7, raw Laplace 7/7 | FAIL |
| SEC6R-A-T | is the saving SEC's? | a transferred λ behind on 0 carriers | NOT DECIDABLE |
| SEC6R-A-2 | no divergence | 0 carriers | PASS as printed; no level |
| SEC6R-A-P | against the 3-point mini-sweep | 6/7 | PASS as printed; UNINFORMATIVE |
| SEC6R-A-S | sensitivity (3 windows, κ 0.25 and 1.0) | 0 of 35 flips | not fragile |
| SEC6R-A-K | compute | CPU share of the full sweep 0.0476–0.0663; clip firings 2 | report |

**What the numbers show beyond the verdicts** (all from `runs/sec6r/partA/score.txt`):
- **The tuned λ's final accuracies are near the floor on most carriers.** For example, 2.8600 on Wikipedia_Talk_Labels and
  5.1877 on agriculture_dataset_karnataka. Only 2 of 7 carriers are not floor-bound.
- **The criterion rewards keeping the first task.** On these class-incremental streams, the frozen learner's accuracies are far
  above every penalty arm. For example, it scores 52.4800 on Wikipedia_Talk_Labels, where the first task holds 77.04 % of the
  test set.
- **SI-1C is far ahead of the tuned λ on four carriers** (+20.4905 Obesity, +12.2800 air-quality, +9.3200 news_channel,
  +2.2600 Wikipedia). It caps its own penalty at SEC4's clip, which pins the first tasks.
- **SI-1, SI's published strength without a guard, diverges on every seed of every carrier.**
- **The rule Ω = 1 sits within a step of the tuned λ on 6/7,** exactly as the clipped SEC does.

**What Part A does not show.** It does not show that the clipped SEC is tuning-free, and it does not replicate SEC4-1. The
SEC family's record is unchanged:
- SEC4-1: PASS-1 on one family;
- SEC5-1: FAIL;
- SEC6: NOT DECIDABLE;
- SEC4-1-G: the same gate, post hoc, CLOSED.

(The scorer's own family line reads "PASS on 2 of 3 families". It counts this post hoc, seen, uninformative 6/7 as SEC6-1. The
ledger does not.)

## Part B: the held-out test

Pending. The data step is on or after 2026-10-02T00:00Z, and this section is written after its rows.

## What a surrogate would have done

No surrogate entered the scoring. The instrument gate SEC6-G plays the surrogate's part here: a learner that stops learning
after task 1 is the must-fail control, and on Part A it passes the criterion on every carrier. Its earlier readings are in
`SEC_Analysis/checks/gate_posthoc.txt` (SEC4-1-G CLOSED, only SCL3's carriers OPEN) and in ledger SEC7-A. A random class
order with balanced accuracy did not make it fail.
