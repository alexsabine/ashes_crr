# Findings log (append-only; newest last)

Each entry records the date, the step, what was found, and the source that holds the number. Entries are never edited;
a correction is a new entry that references the old one.

| # | when (UTC) | step | finding | source |
|---|---|---|---|---|
| 1 | 2026-09-25T18:20Z | 1 | Declaration pushed before the dossiers: 30 mechanism rows (17 training and development, 13 execution): 23 graded CRR readings, 2 INHERITED (speculative decoding, KV caching), 5 S rows. | `DECLARATION_1.md` |
| 2 | 2026-09-25T20:40Z | 2 | Sources read on the day by three research agents: 179 comparison rows and 3 accounting figures, 326 of 326 quotes verbatim. The IEA's own pages refused the proxy (HTTP 403); IEA figures are quoted as reported. No 2024-2026 source gives a new measured training/inference split. | `docs/citations/energy_{accounting,training,inference}_2026-09-25.md`; `checks/verify_quotes.txt` |
| 3 | 2026-09-25T20:40Z | 2 | Development is a large target. OLMo's model development used 459 MWh against 913 MWh for the final runs (~50 %); the final BLOOM run was 37.24 % of its project's dynamic energy. | `checks/retro_energy.txt` (accounting) |
| 4 | 2026-09-25T20:40Z | 3 | Retrodictive grading: CRR readings (INHERITED excluded) AGREES 8, DISAGREES 1, MIXED 9, NOT REPORTED 5; 62 of 80 graded rows agree (55 of 70 with matched-quality rows set aside). Agreeing: hyperparameter transfer, warm-start gap and its repair, model growth, horizon-free schedules, 8- and 4-bit quantisation, distillation (7/7), KV caching. | `checks/retro_energy.txt` |
| 5 | 2026-09-25T20:40Z | 3 | Corrections: equal pull reduces to the sum in replay, not in multi-task learning (E2b MIXED); speculative decoding is time-lossless, not energy-lossless (1.2565 and 1.2987 of baseline energy at large batch); deduplication's saving is real but below 10 % (0.9608, 0.9500); MXFP4 needs 1.36x the tokens of NVFP4 (the resolvable step, not the bit count); E13 and I11 were mis-coded and are NOT REPORTED. | `RETRODICTION.md` |
| 6 | 2026-09-25T20:40Z | 3 | Post-hoc candidate: cuts on a step clock fail while cuts on content hold (a fixed early exit is behind, ROUGE-2 0.012 against 0.079; a forced 1024-token budget is behind by 23.4; a verified exit and first-correct stopping are not behind). To be declared and gated before any test. | `RETRODICTION.md` point 8 |
| 7 | 2026-09-25T20:40Z | 3 | No energy saving in the literature is attributable to CRR: the lens sorts known mechanisms. ENERGY1 candidates, after SOTA1: continual update vs retraining, SEC vs a sweep, a horizon-free schedule, shrink-and-perturb, an own-clock vs step-clock cut, the empty cut (coded '='). | `RETRODICTION.md` |
