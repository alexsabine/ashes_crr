# Declaration 2: a coverage audit and a systematic gap sweep for prior art on CRR's candidate offers

**Status.**
- **The request.** Owner request: prompt-log entry 203. The question is: did we check all the latest papers, and what, if
  anything, does CRR offer? The owner cannot spend money, so everything here is literature and CPU.
- **When it was pushed.** Before the sweep's searches run and before `checks/coverage.py` exists.
- **What it is.** A note, not evidence (R8).

## The honest answer to "did you check all the latest papers?"

**No.** No sweep checks all papers. The dossiers of 2026-09-25 are targeted: the investigator named the canonical and
recent sources for each declared mechanism. They are not systematic searches, and they carry three biases:
- **Selection.** The investigator chose what to fetch.
- **Access.** iea.org, github.com and some ACM pages refused the proxy.
- **Recency.** Work after the models' training exposure is found only by search.

`checks/coverage.py` prints what was covered (sources per dossier, share from 2024–2026). This declaration fixes a
systematic sweep for the gaps that bear on the fairness question.

## What CRR might offer: the candidates to be checked for prior art

| id | candidate offer | where it came from |
|---|---|---|
| C1 | **the state-digest audit:** verify a pause or resume by hashing the saved and restored state, not by comparing outputs (B1) | Lossless_Pause L5b |
| C2 | **the zero-stake pause:** a learner whose valuation is on its own steps has no incentive to resist a lossless pause (B3) | SCL1–3, NT1, AI_Safety |
| C3 | **SEC:** a tuning-free, calibrated penalty weight that removes a hyperparameter sweep (not a CRR rule; a product of the programme) | SCL3-3 PASS-0 |
| C4 | **the empty-cut checklist:** full state, own-clock keying, the world's content (E1–E3) as a design rule for pausable learners | Empty_Cut_Engineering, RW1 |
| C5 | **the own-clock cut:** stop computing when the belief has settled | Energy DECLARATION_2 (it already reduced to Wald on a synthetic world) |

**The grading of each candidate, from quotes:**
- **REDUNDANT:** a fetched source states it.
- **PARTLY REDUNDANT:** a source states a close form. The difference is named.
- **NOT FOUND IN THE SWEEP.**

"Not found" is never read as "novel". Novelty is judged only by a named domain expert (CLAUDE.md §7).

## The sweep protocol (fixed now)

**Window and sources.**
- **Window:** 2024-01-01 to 2026-09-25, plus any canonical earlier work a hit cites for the same idea.
- **Search services:**
  - the arXiv API (`export.arxiv.org/api/query`, search_query over all fields, sorted by relevance, first 25 hits per
    query);
  - one WebSearch per query for non-arXiv venues.

  Each query and its hit list (id, title, date) are recorded in the family's search log. Every hit is screened by title
  and abstract, with the inclusion decision recorded.

**Inclusion.** A primary source on the query's topic, fetched in full text, with quotes verbatim. The same verification
rule as before applies: at least 20 characters, and a substring of the saved text after normalisation.

**Three families, each run by one research agent:**

1. **P, prior art for C1–C5.**
   - Queries: "proof of learning checkpoint hash verification"; "verifiable training replay hash"; "verification of
     inference activations hashing"; "safe interruptibility reinforcement learning"; "utility indifference shutdown";
     "corrigibility pause incentive"; "hyperparameter-free regularization weight"; "tuning-free loss weighting";
     "learning-rate-free optimizer"; "checkpoint resume correctness bug"; "silent data corruption checkpoint";
     "adaptive computation halting".
   - Must include if found: Proof-of-Learning (Jia et al. 2021), TOPLOC (2025), Verde (2025), Orseau & Armstrong
     (2016), the off-switch game (Hadfield-Menell et al. 2017), D-Adaptation or Prodigy, and schedule-free.
2. **T, Transformer and serving state, 2024–2026.**
   - Queries: "KV cache persistence serving"; "stateful LLM serving suspend resume"; "LLM agent pause resume tool call KV
     cache"; "state space model inference state checkpoint"; "LLM serving cold start snapshot restore"; "deterministic
     LLM inference 2026".
   - Must include if found: CachedAttention / AttentionStore, Mooncake, LMCache, ServerlessLLM.
3. **E, energy and carbon, 2025–2026.**
   - Queries: "energy consumption reasoning models"; "AI inference energy measurement 2026"; "rebound effect AI energy
     efficiency"; "carbon-aware LLM inference serving"; "carbon-aware training scheduling 2025"; "embodied carbon GPU AI
     accelerators"; "MLPerf power"; "AI Energy Score".
   - Must include if found: Luccioni et al. 2025 on rebound effects, MLPerf Power, and a 2025–2026 reasoning-energy
     measurement.

**The outputs:**
- the dossiers `docs/citations/sweep_{prior_art,transformer_state,energy_carbon}_2026-09-25.md`, each with its search log;
- claims files, tagged C1–C5 or with an energy or carbon topic tag;
- `checks/sweep_claims.py` and `checks/grade_sweep.py` (+ `.txt`).

The grading for C1–C5 is computed from the investigator's per-claim reading (states / close / bears), recorded per claim
as before.

**What would change the record.**
- **C1 or C4 graded REDUNDANT:** LOSSLESS_PAUSE §5's B1 row is corrected in a new entry, and the empty-cut discipline is
  reported as existing practice.
- **C3 graded REDUNDANT, or dominated by a published tuning-free method:** SEC's attributable saving in
  `Energy Design Principle/CONSOLIDATED.md` is corrected to the counterfactual beyond that method.
- **New energy or carbon figures:** reported beside the old ones. They replace nothing silently.
