# A consolidated CRR lens on continual learning, AI safety and energy: what it could save, and what kind of claim that is

**Status.**
- **Owner request.** Prompt-log entry 200. It is a note, not evidence (R8).
- **How it was done.** `DECLARATION_2.md` was pushed (4b3b995) before either script existed.
- **Where the numbers come from:**
  - `checks/clock_cut.txt`: the synthetic check, rerun byte-identical, run by hand (about 2.5 minutes);
  - `checks/consolidated_estimate.txt`: the scenario and the forecasts, CI-checked.
- **Pending.** The full pipeline checks are ENERGY1 and SOTA1, still to come. This page makes the prediction they will
  score.

## 1. The synthetic check of the "own-clock cut"

**The observation (post hoc, from the literature).** Cuts on a step clock (a fixed exit layer, a forced token budget)
lost quality, while cuts on content (verified exits, stopping at the first correct answer) held.

**The world.** Four synthetic worlds of noisy evidence about a hidden class, with an exact Bayesian agent. Five stopping
rules were compared:
- run to the end;
- a fixed default budget;
- a tuned budget;
- a confidence threshold (the sequential probability ratio test's own statistic);
- the CRR arc rule: stop when the Fisher–Rao step length has settled and the belief has travelled at least half the way
  to certainty;
- answer stability.

**Results** (`clock_cut.txt`; labels in at least 4 of 5 seeds):

| check | result |
|---|---|
| gate: confidence beats a tuned budget (W1, W2); no content rule beats the budget where timing is fixed (W0) | **GATE OPEN** (cost ratios 0.5068–0.5467 in W1, 0.2883–0.3829 in W2; W0 TIE or WORSE) |
| G3: a forced 16-step budget against running to the end (W2) | TRADE-OFF: 0.0625 of the steps, 15.18–17.60 points behind, as in the literature |
| F1: the arc rule against a tuned budget | BETTER in W1 (0.5641–0.6122 of the steps) and W2 (0.3655–0.3926); TIE in W3 |
| C1: the arc rule against confidence in W1 (must not win) | holds: WORSE, 1.1109–1.1198 of the steps |
| C2: the arc rule against confidence in W2, W3 (forecast TIE) | MIXED in both, and FRAGILE (6 and 4 of 9 cells flip) |
| C3: the arc rule against answer stability | BETTER in W2 (0.5878–0.6600 of the steps), not fragile; WORSE in W3 |
| a prospective candidate (arc BETTER than confidence in W3, not W1) | **no** |

### What it means

1. **"Content beats the clock" is true, and it is not CRR's.** A tuned fixed budget loses to any sensible content rule
   wherever items differ, and it ties where they do not (the W0 null). That is Wald's sequential analysis: the sequential
   test is "later proven to be optimal by Wald and Jacob Wolfowitz" (Wikipedia, fetched 2026-09-25). The literature's
   pattern is **REDUNDANT-DOMAIN**, a correct retrodiction of a known result.
2. **The CRR-specific rule adds nothing over the known optimum.**
   - The arc rule never beats the confidence rule.
   - Where the confidence rule is provably optimal (W1), the arc rule costs 11–12 % more steps.
   - Elsewhere the comparison is MIXED and fragile.

   This is the pattern `ontology/15_grammar_to_theory.md` predicts: where a field has a sufficient statistic (here, the
   posterior's confidence, the likelihood ratio), CRR's ingredient becomes the field's or loses to it. The arc is a
   function of successive posteriors, so it carries no more information than they do, and it adds a free threshold.
3. **One real, modest property.** The arc rule beats a naïve "answer unchanged for w steps" rule where items differ in
   difficulty (W2), because the arc sees the belief still moving under a stable argmax. The stability rule wins back
   under overthinking (W3).
   - This separates two published families (confidence exits against answer-consistency stops). It is not a new
     mechanism.
4. **A design limit found by running it** (AGENT_LOG 146). In W3, where running longer hurts, the declared target (the
   run-to-the-end accuracy minus 1 point) is set by a degraded reference. The tuned rules therefore stop very early at
   about 66–67 %, while the untuned 16-step budget reaches 76.95 % (seed 0). F1's TIE and O1's labels in W3 are read with
   that caveat. The fix, a target set by the best achievable accuracy, is for a later declaration, not this run.

**Ladder rung.** R4 (declared on a synthetic world). The observation reduces to Wald. P5, the forecast that the arc cut
will beat the confidence cut on real data, stays at 0.10.

## 2. The consolidated estimate, 2030, conditional on the methods holding

Each term is energy the mechanism would save across the world's AI servers (`consolidated_estimate.txt`).

| term | low | middle | high (TWh) | attributable to |
|---|---|---|---|---|
| T1 SEC replaces sweeps of penalty weights | 0.0742 | 0.4743 | 4.0399 | the CRR programme (SEC; the ledger records it as not a CRR rule) |
| T2 continual updating replaces periodic retraining | 0.4507 | 5.1429 | 35.7058 | none (continual pre-training is published) |
| T3 content-based stopping of reasoning | 3.8403 | 23.4063 | 75.0755 | none (§1: the arc rule did not beat confidence) |
| T4 the safe pause (the empty cut) | 0 | 0 | 0 | energy moved, not saved |
| T5 horizon-free schedules for multi-horizon sweeps | 0.5209 | 2.1961 | 12.4015 | none (WSD is published) |
| **technical potential (the sum; no overlap or rebound)** | 4.8861 | **31.2195** | 127.2226 | — |
| **attributable to CRR or its programme** | 0.0742 | **0.4743** | 4.0399 | — |

**The estimate in plain terms (middle case).**
- The practices a CRR lens endorses could save about 31 TWh a year by 2030. That is 3.3 % of all data-centre electricity,
  about 10 % of AI-server electricity, or the yearly use of about 2.9 million US homes.
- **About 1.5 % of that (0.47 TWh) is attributable to the CRR programme**, all of it through SEC.
- **Weighted by an assumed adoption probability** (0.0150, `cl_patent`'s assumption), the attributable figure is about
  0.007 TWh.

### Why the terms are the size they are

- **T3 is largest because it touches the largest pool.**
  - Serving models is 60–70 % of AI electricity: 1 − f_dev in the middle and low cases.
  - Reasoning tokens are a large and compressible share of it. The assumed share is 10–50 %.
  - Published content-based stops cut 45–71 % of reasoning tokens without losing a step.
- **T2 is next.** Continual pre-training halves the tokens of a retrain (three quoted rows). Its size depends on how much
  final training is only refreshing data (assumed 10–50 %), and final training is 10–67 % of development-and-training.
- **T1 is small.** It acts on one kind of sweep, 0.1–2 % of development by assumption. It removes most of that sweep
  (82–94 %), but it cannot be larger than the sweep.
- **T4 is zero on energy.**
  - A lossless pause moves work to cleaner or cheaper hours. The quoted row saw 1.38 kgCO2 against 11.4–27.1 kgCO2 for
    single-region runs.
  - It saves carbon, not kWh. Its contribution to the economy is flexibility, and that is where CRR's own commitments
    (the contentless cut on the system's own clock) do real engineering work.

## 3. The epistemic nature of this claim

Read with `ontology/15_grammar_to_theory.md` (what CRR is), `ontology/04_falsifiability_and_metaphysics.md` and the
epistemic ladder.

1. **It is a scenario, not a CRR prediction.**
   - The 31 TWh is a product of sourced factors, three named assumptions (f_refresh, f_reason, f_scaling) and published
     cost ratios.
   - No axiom of CRR fixes any factor. In the language of ontology/15, the framework "fixes nothing" here either.
   - As a whole, the scenario is not falsifiable. It becomes testable only when broken into its parts, the forecasts
     P1–P8.
2. **The technical potential belongs to the mechanisms, not to the lens.** Every term except T1 is a published mechanism
   the lens *sorts*: continual pre-training, content stopping, WSD, the pause. That is Kitcher-style unification: one
   pattern, occasion → cut → regeneration from the settled past, fits all of them. It is also exactly what ontology/15
   warns about: "a correct abstraction of what many sciences independently had to discover; it has not yet told any of
   them something they did not know." Credit for an energy saving is counterfactual. What would not have been saved
   without CRR? For these terms, nothing.
3. **What is attributable sits at modest rungs.**
   - **T1 (SEC) is PASS-0 on ten unseen tabular carriers** (SCL3-3, R6), fragile, under SGD. The Adam_SGD record says its
     scale advantage is an SGD property. P8, survival at LLM scale under AdamW, is 0.15.
   - **T3's CRR-proper version reached only R4 and did not beat the known optimum.** It is attributed nothing.
   - **T4 is a theorem of construction** (Proposition 7; E1–E3). It is certain as mathematics, and it is zero in kWh.
4. **Where CRR could earn credit: route 5 of ontology/15**, "design rules that work by construction". The empty cut makes
   pausing lossless and safe. Cheap, safe pausing is what lets training follow clean or curtailed power.
   - Its energy value is zero. Its carbon value is potentially large.
   - It is claimable only after the literature check that route 5 requires (safe interruptibility, utility indifference,
     and checkpoint and elastic-training practice).
5. **Rebound is named, not quantified.** Cheaper compute buys more compute. Net energy could fall by less than any term,
   or rise. No source fetched today quantifies it for AI, so no figure is given.
6. **The honest one-line claim.**
   - A CRR lens points at practices that could save on the order of 3 % of data-centre electricity by 2030 (about 31 TWh,
     middle case).
   - Almost none of that is CRR's to claim.
   - The part that may be, SEC, is about 0.5 TWh if it holds at scale, and it has not yet been shown to.

## 4. The fair prediction, recorded now and scored later

These are printed by `consolidated_estimate.py`. The expected number of the eight events is 3.00.

| id | event | P |
|---|---|---|
| P1 | SEC against the tuned sweep on SOTA1's learner: accepted, saving ≥ 80 % of the sweep | 0.45 |
| P2 | a continual learner reaches ≥ 95 % of retraining accuracy at ≤ 0.5 of its compute (online Split-CIFAR-100) | 0.10 |
| P3 | a horizon-free schedule is not behind cosine in the stream | 0.60 |
| P4 | shrink-and-perturb at task boundaries saves ≥ 10 % of work to a target | 0.30 |
| P5 | the arc cut is BETTER than the confidence cut on real data | 0.10 |
| P6 | the empty cut changes energy by 0 and leaves the run bitwise identical | 0.95 |
| P7 | SOTA1-1a: CRR-SCL is AHEAD of the best baseline | 0.35 |
| P8 | SEC's saving survives at LLM scale under AdamW | 0.15 |

**Scoring.** When ENERGY1 and SOTA1 report, each event is scored 0 or 1 against its ledger row, and the Brier score of
these eight probabilities is written into FINDINGS. A forecaster who is well calibrated about this programme should see
about three of them occur.
