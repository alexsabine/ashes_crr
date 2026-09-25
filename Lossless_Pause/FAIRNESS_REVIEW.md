# Did we check the latest papers, and what does CRR offer? A fairness review

**Status.**
- **Owner request.** Prompt-log entry 203. It is a note, not evidence (R8).
- **How it was done.** `DECLARATION_2.md` was pushed (41354b6) before any search ran.
- **Where the numbers come from:**
  - `checks/coverage.txt`, the coverage audit;
  - `checks/grade_sweep.txt`, the grades of C1–C5 and the new figures;
  - `checks/sweep_claims.py`: 86 claims, 143 of 143 quotes verbatim (`checks/verify_sweep_claims.txt`).

  All three are CI-checked except the quote check, which is run by hand because the raw texts are not committed.
- **The dossiers:** `docs/citations/sweep_{prior_art,transformer_state,energy_carbon}_2026-09-25.md`. Each carries its full
  search log.

## 1. Did we check all the latest papers?

**No.** No search checks all papers, and before this sweep the dossiers were targeted, not systematic.

**The coverage audit** (`coverage.txt`, distinct arXiv ids named in the dossiers of 2026-09-23 to 2026-09-25):
- Across all groups, 884 ids. The sweep's count includes hits that were screened and excluded.
- **Energy (prompt 199):** 111 ids, 58 from 2024–2026.
- **Lossless pause (prompt 202):** 38 ids, 26 from 2024–2026.
- **The gap the audit exposed: the continual-learning state-of-the-art dossiers (prompt 191) name only 1 id from
  2024–2026.** The recent continual-learning work is in the frontier dossiers (120 ids, 107 from 2024–2026). The
  retrodictive grading of CL mechanisms used the older ablation literature. That is a recency limit of the CL grading,
  and it is stated here.

**The sweep's own limits** (from its search logs):
1. **The arXiv API was unusable.** It returned HTTP 406 through the proxy for every query in all three families.
   - The fallback was arxiv.org/search, which requires every term to match. Some queries returned no hits, and recall
     is lower than a relevance-ranked search.
   - One WebSearch per query supplemented it.
2. **At most 25 sources were included per family.** The qualifying but unfetched hits are listed in each log.
3. **Some sources were refused:** github.com (for example, two pull requests on topic for C4) and one OCP
   silent-data-corruption whitepaper.

## 2. What CRR might offer, against prior art (`grade_sweep.txt`)

| id | candidate | grade | the closest sources, and the difference |
|---|---|---|---|
| C1 | a state-digest audit of a pause (hash the state, not the outputs) | **PARTLY REDUNDANT** (4 close) | SHA-256 or Merkle hashes of weights and optimizer state, used to verify training (Srivastava et al. 2403.09603v3; Verde 2502.19405v1). A SHA-256 digest of stored KV-cache blocks, compared on reuse, catches bit flips that yield "coherent but altered outputs, indistinguishable from legitimate responses" (the Bit-Flip KV-cache paper, 2026). **The difference:** these verify training or cached serving, not a pause and resume specifically. The step to a pause is small |
| C2 | a zero-stake pause | **PARTLY REDUNDANT** (5 close) | safe interruptibility (Orseau & Armstrong 2016); utility indifference (Soares et al. 2015; Carey & Everitt 2023); the off-switch game (Hadfield-Menell et al. 2017). **The difference:** CRR obtains no incentive from a valuation on the learner's own steps plus a lossless pause, rather than from off-policy learning, compensatory utility or uncertainty |
| C3 | SEC, a tuning-free penalty weight | **PARTLY REDUNDANT** (4 close) | learning-rate-free and schedule-free methods (D-Adaptation, Prodigy, Schedule-Free); online loss-weight learning at about 30 % above one run (2605.07756v1). A 2025 AlgoPerf paper states that these methods leave regularisation weights untuned. **So no quoted method sets a continual-learning penalty weight, and SEC's niche is open but narrow** |
| C4 | the empty-cut checklist | **REDUNDANT** | Mitra (2609.22087v1, submitted 22 Jun 2026) states it: "under full-state preservation an availability gap injects no bias and no excess loss". The schedule must be indexed on active, not wall-clock, time, and wall-clock keying is named as the failure. The world's content across the gap is treated as a separate cost regime |
| C5 | the own-clock cut | **REDUNDANT** | Popescu et al. (2607.20519v1) name exit rules that "exit when the trajectory appears to have stabilized, using quantities such as predictive KL between consecutive predictions". The Fisher–Rao step is √(2·KL), so this is the arc rule. It was already REDUNDANT-DOMAIN to Wald on the synthetic world (Energy DECLARATION_2) |

**Nothing was NOT FOUND.** Every candidate has at least a close form in the literature.

## 3. Corrections this makes to earlier notes (appended, not edited over)

1. **`LOSSLESS_PAUSE.md` §5, B1.** It said "supported by L5b; close to Lorup's quoted statement, so a candidate at most".
   **It now reads PARTLY REDUNDANT.** State-hash verification is established practice in verifiable training and
   cached serving.
2. **The empty-cut checklist (`Empty_Cut_Engineering/`, RW1) is existing practice.** Full-state preservation with
   active-time scheduling is published as the baseline for interruption-resilient training (Mitra 2026). The repository's
   checks remain valid replications. They are not an offer of CRR's.
3. **The own-clock cut (Energy FINDINGS 6, 9) is REDUNDANT twice over:** to Wald's sequential test, and to published
   early-exit rules keyed to predictive KL between consecutive predictions.
4. **SEC's attributable energy saving** (`Energy Design Principle/CONSOLIDATED.md` T1) assumed a full sweep as the
   counterfactual.
   - If an online loss-weighting method at about 1.30 runs transferred to continual-learning penalty weights (not
     shown), SEC would save 0.0176 of the sweep-equivalent instead of 0.9412.
   - T1's middle case would then fall from 0.4743 to 0.0095 TWh.
   - This is a sensitivity, not a correction. No quoted method sets such a weight today.

## 4. New energy and carbon figures (reported beside the old ones; they replace nothing)

- **Development is a larger share of a model project than the scenario assumed.** In Olmo 3 (Morrison et al. 2026),
  development was 80.9 % of GPU energy. In OLMo 2, the source the scenario used, it was 0.3345 of development plus final
  runs.
- **Reasoning multiplies energy.**
  - Reasoning models use on average 30× more inference energy (AI Energy Score v2).
  - Olmo 3 Think used 17× more post-training energy than Instruct.
- **The inference share may be larger than the scenario's.** "More than 90%" of power, from industry reports as cited
  by TokenPowerBench. It is secondhand, and it compares with the scenario's 0.60 middle.
- **Rebound is stated and measured.** Luccioni, Strubell & Crawford (2025) state that rebound effects undermine
  efficiency-only assumptions. Morand et al. (2026) find that training impacts rose exponentially despite optimisation
  strategies, "suggesting rebound effect".
- **Carbon-aware serving and agents** report cuts of up to 47 % (EcoServe) and up to 57.9 % (AgentDecarbonizer), by
  shifting load, adapting quality or re-provisioning. That is the same family of mechanism as the pause-and-shift
  results already on record.

## 5. So what does CRR offer, if anything? (fairly, under the pipeline)

1. **As a technical offer, almost nothing new.**
   - Two candidates (the checklist, the own-clock cut) are REDUNDANT.
   - Three (state-digest audit, zero-stake pause, SEC) are PARTLY REDUNDANT, with a narrow stated difference each.
   - None survives as "not found".
2. **The narrow differences worth keeping:**
   - **SEC** targets a continual-learning penalty weight that published tuning-free methods leave untuned. It holds at
     PASS-0 on ten unseen tabular carriers.
   - **The zero-stake pause** reaches non-resistance by a different mechanism: the valuation on own steps plus a
     lossless cut. It needs its own comparison against safe interruptibility and utility indifference in a shared
     environment. NT1 compared it with DReST only.
3. **As a lens, CRR's contribution is organisational.** One vocabulary (occasion, cut, settled past, own clock) sorts
   continual learning, pausing, safety and energy together. That matches ontology/15's description: a grammar that
   correctly abstracts what fields found independently. It is useful for design and teaching, and not evidence.
4. **What would change this.** A PASS-2 for SEC, or a head-to-head in which the zero-stake pause beats safe
   interruptibility and utility indifference on a declared task. Both can be done on CPU, at no cost.
