# What works in AI energy saving, read through CRR

**Status.**
- **Owner request.** Prompt-log entry 199. It is a note, not evidence (R8). It is a retrodiction on published numbers, not a
  ledger study.
- **The predictions** were pushed before the sources were fetched (`DECLARATION_1.md`, db871f6).
- **The rows** are in `checks/energy_rows.py`: 179 rows from 3 dossiers fetched on 2026-09-25, with 326 of 326 quotes
  verbatim (`checks/verify_quotes.txt`).
- **The grades** are in `checks/retro_energy.txt`, byte-identical on rerun and CI-checked. Every number below is from that
  file or the dossiers it quotes.

## Where the energy goes (quoted, not graded)

- **Developing a model costs about half as much again as training it.** In the OLMo family, model development used 459 MWh
  against 913 MWh for the final training runs: "∼50% of that of training" (Morrison et al. 2025).
- **In BLOOM, the final run was 37.24 % of the project's dynamic energy** (433,196 of 1,163,088 kWh).
- **A median Gemini Apps text prompt uses 0.24 Wh**, after a 33x reduction in one year (Google 2025).
- **No 2024–2026 source gives a new measured split between training and inference.** Recent papers re-cite Google's
  (about 3/5 inference) and Meta's (10:20:70) (dossier A17).

The development share matters for this programme. It is where SEC's saving, the sweep that is not run, falls. It is
larger than the 0.1–2 % sweep share assumed in `Compute_Savings/DECLARATION_2.md`. That assumption covered sweeps of
one kind of weight only, not all development, so the two are not in conflict. The Morrison figure bounds the whole
category from above.

## The grades

| mechanism | CRR reading | outcome (rows agreeing / graded) |
|---|---|---|
| E1 hyperparameter transfer | A1′ own unit | AGREES (2/2) |
| E2a tuning-free calibrated weight | H-EQ + A1′ | MIXED (4/6) |
| E2b adaptive balancer vs plain sum | H-EQ reduces to the sum | MIXED (2/5) |
| E3 successive halving | A7 / A3 | NOT REPORTED (no quoted numeric pair) |
| E4 curve extrapolation vs halving | A8 | NOT REPORTED |
| E5 continual pre-training vs retraining | A6 + A3 | MIXED (2/3) |
| E6a warm start vs scratch | A6 unbounded loses plasticity | AGREES (3/3) |
| E6b shrink-and-perturb | A6 as a reweighting | AGREES (2/2) |
| E7 model growth | A6 | AGREES (3/3) |
| E8 weight averaging | A6 + P3 | MIXED (3/4) |
| E9 horizon-free schedules | A8 | AGREES (4/4) |
| E10 deduplication | A1′ | DISAGREES (0/2) |
| E11 salience pruning vs random | P2 (predicted no difference) | MIXED (2/3) |
| E12 reduced-precision training | A1′ | MIXED (4/5; 4/4 without the matched-quality row) |
| E13 checkpointing | Proposition 7 | NOT REPORTED (see the correction below) |
| I1 8-bit | A1′ | AGREES (3/3) |
| I2a 4-bit | A1′ | AGREES (3/3) |
| I2b 3 bits or fewer loses quality | A1′ | MIXED (2/4) |
| I3 distillation | A6 | AGREES (7/7) |
| I4 speculative decoding (INHERITED) | A7 / A8 | MIXED (5/7) |
| I5 KV caching (INHERITED) | A6 / A7 | AGREES (3/3) |
| I6 early exit / adaptive depth | D2 own clock | MIXED (4/5) |
| I7 reasoning-length control | D2 + A3 | MIXED (4/6) |
| I8 cascades / routing | D2 / A1′ | NOT REPORTED (costs in dollars) |
| I11 carbon-aware pausing | Proposition 7 | NOT REPORTED (carbon, not energy) |

**Totals.** CRR readings, INHERITED excluded: AGREES 8, DISAGREES 1, MIXED 9, NOT REPORTED 5. 62 of 80 graded rows agree.
With the matched-quality rows set aside (a transcription rule decided after the rows were seen, AGENT_LOG 145), 55 of 70
agree.

## Why the disagreements happened, in CRR's terms

1. **Deduplication (E10) disagrees on magnitude, not direction.**
   - Both rows reach the same quality with less compute: 0.9608 and 0.9500 of the baseline. Neither clears the declared
     10 % line.
   - A1′ says a repeat adds no arc, so the saving is at most the repeated share of the corpus, which is small in C4.
   - **The reading was right, and the threshold was wrong for this mechanism.** The saving scales with the duplicate
     fraction.
2. **Adaptive loss weights (E2a, E2b) behave as in this repository's own record.**
   - Uncertainty weighting and GradNorm tie or beat a searched fixed weight in their own papers (Kendall, GradNorm).
     They are behind a 20-trial search on one CityScapes setting: AutoScale −1.39 points, uncertainty weighting −7.11.
     Each costs 0.0626 or less of the search.
   - This is the SCL3 pattern: a tuning-free weight saves about 94 % of the sweep and is sometimes behind.
   - Adam_SGD's reading covers it: equal pull is strong where the scale difference is an artefact, and weak where the
     scale carries task priority.
   - The E2b prediction, that balancing reduces to the sum, is too strong outside replay. Kurin et al. tie the sum
     (0.9093 against 0.909), but GradNorm beats equal weights in its own paper, and uncertainty weighting beats the sum on
     CityScapes. **H-EQ's reduction to a constant is a finding about replay, not a law of multi-task learning.**
3. **Continual pre-training (E5) halves the tokens, and one row falls just behind.**
   - Loss is 1.89 against 1.87, a gap of 0.020 against a step of 0.0187. The other two rows are not behind.
   - A6's regeneration from the settled past holds with a small, resolvable price on one validation set. The TiC-LM row
     (2.6x less computation) was excluded because its regret metric has no defined step.
4. **Weight averaging (E8) helps in one model and hurts in another at matched compute** (+3.26 and −2.00 points, LAWA). The
   algorithm benchmark saves 0.8987 (LAWA) and 0.8840 (EMA) of GPU-hours to target. A6 with age weights saves time to a
   target, but it is not a free quality gain at the end of training.
5. **Four-bit training formats (E12).** FP8, NVFP4 and BF16 are never behind their references. MXFP4 needs 1.36x the
   tokens of NVFP4 to match its loss.
   - **Correction.** A1′ is about the resolvable step, not the bit count. MXFP4's power-of-two block scales are coarser
     than NVFP4's, so its effective step is larger at the same four bits.
6. **Three bits or fewer (I2b).** The perplexity rows are behind, as predicted. The two Husom et al. accuracy rows print
   standard deviations of 0.32–0.41 on a 0–1 scale, so the step is 0.78–0.82 and no difference is resolvable. The
   disagreement is a failure of resolution in the benchmark, which is A1′ applied to the evidence itself.
7. **Speculative decoding (I4).** It saves time in 5 of 7 rows and costs energy in two: 1.2565 and 1.2987 of the baseline.
   - **Correction.** The '=' code assumed a speed-up is an energy saving. It is not when the drafted tokens that are
     rejected must be computed on hardware that is already busy (large batches).
   - In CRR's terms (A8), a drafted future has no content until it is verified. Drafting spends energy on proposals that
     may be discarded, and that is free only when the hardware would otherwise idle.
   - **So speculative decoding is time-lossless, not energy-lossless.**
8. **Early exit (I6) and reasoning-length control (I7): the failures are cuts on a clock, the successes cuts on content.**

   **I6: fixed exits fail and verified exits hold.**
   - A fixed early exit (LayerSkip at a set layer) is behind: ROUGE-2 0.012 against 0.079.
   - The self-speculative variant, which verifies, is not behind at 0.4902 and 0.5484 of the cost.
   - Mixture-of-depths saves half the FLOPs at loss parity.

   **I7: fixed token budgets fail and content-based cuts hold.**
   - A forced token budget of 1024 is behind by 23.4 points. A budget of 2048 is not behind, at 0.2861 of the tokens.
   - Stopping at the first correct solution is not behind at 0.5526 of the tokens, but adding reflection is behind by 3.4.
   - Removing the thinking box is ahead at matched tokens (+22.4).

   **The reading.** D2 distinguishes a cut on the system's own clock (when the content has settled) from a cut on the
   step clock (a fixed budget). The failures are step-clock cuts; the successes cut on content or verify.
   - **This is a post-hoc reading.** It is a candidate hypothesis for a declared test, not a result.

## Corrections to the declaration (for the next one)

- **E13 and I11 were coded wrongly.** Checkpointing and pausing leave the trained model unchanged by construction. They
  should have been coded '=' (graded on cost), not '+' or '0', which need a quality number the papers do not print.
  - As registered, both are NOT REPORTED.
  - The listed rows show checkpointing cutting blocking and recovery time. For example, a blocking time of 0.04 s against
    6.77 s (ByteRobust), and 13x faster recovery (GEMINI).
- **Speculative decoding** should be '=' on time and '0 or +' on energy, depending on batch size (point 7).
- **Dollar costs (I8)** were outside the declared cost kinds. Routing is therefore ungraded.

## What this says about CRR as a lens

- **Where CRR's axioms name the mechanism, the published numbers mostly agree.** The mechanisms are:
  - regenerating from the settled past (A6: warm start and its repair, model growth, distillation, continual
    pre-training);
  - the system's own unit (A1′: quantisation to 8 and 4 bits, reduced-precision training, hyperparameter transfer);
  - no future content (A8: horizon-free schedules).

  None of these readings is new. Each mechanism was invented without CRR, and the readings are at the retrodictive rungs.
- **Where CRR made a claim beyond the known result, it was wrong or too strong three times:**
  - equal pull reducing to the sum outside replay;
  - speculative decoding as energy-lossless;
  - deduplication clearing a 10 % line.

  It was right once in a way worth testing: step-clock cuts fail while content cuts hold (I6, I7). That is post hoc.
- **No energy saving here is attributable to CRR.** The lens sorts known mechanisms. It does not add one.

## What the energy tests (ENERGY1) should take up, after SOTA1

These are candidates, not predictions yet. Each needs a declaration and a Phase A gate first. They are chosen where the
published record and this repository's continual-learning record meet:

1. **Continual update against retraining from scratch (E5, A6).** In the SOTA1 setting, measure the work to reach a given
   accuracy after each task. SOTA1's arms supply the continual learners; retraining on the stored data is the reference.
2. **SEC against a sweep (E2a).** Tuning compute saved at equal accuracy, on the SOTA1 learner's penalty-like weight.
   SCL3 is the held-out precedent.
3. **A horizon-free schedule (E9, A8)** against a cosine schedule in a stream whose length is unknown. This is the natural
   continual-learning case.
4. **Shrink-and-perturb at task boundaries (E6b)** against a plain warm start, on work to a target.
5. **An own-clock cut against a step-clock cut (I6, I7, D2).** For example, the number of updates per incoming batch set
   by the arc of change against a fixed count. This is the post-hoc candidate; its gate must be able to close.
6. **The empty cut (E13, I11, Proposition 7):**
   - rework avoided and energy moved, not saved;
   - coded '=' this time.
