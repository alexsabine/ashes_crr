# Findings log (append-only; newest last)

Each entry records the date, the step, what was found, and the source that holds the number. Entries are never edited;
a correction is a new entry that references the old one.

| # | when (UTC) | step | finding | source |
|---|---|---|---|---|
| 1 | 2026-09-25T05:47Z | 0 | Starting point. The equanimity weight has been tested with the cut on tabular data (SCL1–3) and against FOREVER (C4: TIE in 6 of 7 worlds, BEHIND −11.95 in the class-incremental world). It has not been tested on any image benchmark against reference state-of-the-art code. In the class-incremental regime, replay leads the regularisers by about 40 points. | `docs/notes/2026-09-25_sota1_plan.md` §1; `docs/notes/2026-09-25_results_vs_published.md` |
| 2 | 2026-09-25T05:47Z | 0 | Two readings of equanimity: as a weight (a plateau that reduces to a constant; SEC is its best descendant, not a CRR rule) and as a valuation (zero content at the cut, which made every safety test pass). | `AI_Safety/AI_SAFETY.md` §5.6; `AI_Safety/SELF_THROUGH_TIME.md` §3 |
