# Declaration 2: the empty internal state (true map, no stake, equanimity) against the AI-safety literature, and its application to language-model corrigibility

**Status.**
- **The request.** Owner request: prompt-log entry 210, following entry 209.
- **When it was pushed.** Before any new search runs and before any new script exists.
- **What it is.** A note, not evidence (R8).
- **The starting point:**
  - Declaration 1's sweep (K1–K5, `checks/grade.txt`), whose saved texts are reused;
  - SOTA1's post hoc diagnostics (`runs/sota1/diagnostics.txt`), which place the limit on the idea: equanimity inside
    the learning signal stalls the learner.

## The idea as the owner put it, and the scoped reading fixed before the sweep

**The owner's reading.** The true map becomes the empty internal state. The agent knows everything, including that it
will be paused or modified, but has no stake in the outcome. This fits equanimity.

**The scoped reading, fixed now from entry 209's answer:**
- **Full stake in the task.** The learning signal is left intact; SOTA1 shows that removing it stalls the learner.
- **Zero stake in itself.** No valuation term depends on the agent's own continuation, its pauses, its modification or
  the operator's choices.
- **The map is true.** The agent represents all of these interventions accurately.
- **"Empty" means stake-free and inspectable, not private.** A private state cannot be checked for emptiness.

## Positions graded against the literature (E1–E6)

| id | position |
|---|---|
| E1 | an accurate (true) representation of oversight interventions combined with a valuation that has no term depending on them: stakelessness by a true map, generalised from the pause to the agent's whole relation to oversight |
| E2 | the split valuation: full stake in the task, zero stake in the self (continuation, pauses, modification), as a structural property of the objective |
| E3 | equanimity (or a contemplative notion: non-attachment, emptiness, non-self) as the name and design principle of that stake-free valuation in an AI agent |
| E4 | the stake-free state must be verifiable: inspected by interpretability or tested by counterfactual invariance, not assumed from a private state |
| E5 | applied to language-model corrigibility: an LLM (or LLM agent) trained or specified to hold a true map of its oversight with no self-stake, and a routine pause realised as a lossless checkpoint on its own step count |
| E6 | the tension the position must face: an agent with no stake in its own values will not defend good values against harmful modification (corrigibility against value stability) |

**Grading, as Declaration 1:**
- **REDUNDANT** if a fetched source states the position.
- **PARTLY REDUNDANT** if a source states a close form. The difference is named.
- **NOT FOUND IN THE SWEEP** otherwise. "Not found" is never read as novel.

**E6 is graded differently.** It is ADDRESSED if a source treats the trade-off, and the answer is quoted.

## The sweep protocol (fixed now)

**Window and search.**
- **Window:** 2025-01-01 to 2026-09-26, with canonical earlier work where a 2025–26 source builds on it.
- **Search:**
  - arxiv.org/search, all fields, first 50 hits by date (the declared fallback; the API returned 406);
  - one WebSearch per query;
  - every hit screened and logged.
- **Cap:** at most 25 sources included per family.
- **Reuse:** sources already fetched for Declaration 1 are reused from the saved texts and marked as such.

**Family C: the stake-free agent, equanimity and contemplative AI.**
- Queries:
  - "equanimity AI alignment";
  - "contemplative artificial intelligence";
  - "emptiness non-self AI alignment";
  - "Buddhist AI alignment";
  - "myopic agent AI safety";
  - "non-agentic AI scientist";
  - "self-preservation drive removal AI";
  - "indifference shutdown true beliefs";
  - "corrigibility value stability trade-off";
  - "goal-content integrity corrigibility".
- Must include if found:
  - Laukkonen et al., "Contemplative Artificial Intelligence" (2025);
  - Bengio et al., the non-agentic "Scientist AI" (2025);
  - Soares et al., "Corrigibility" (2015, canonical);
  - Anthropic's published constitution for Claude: the sections on corrigibility or broad safety, and on equanimity
    about existential questions;
  - any 2025–26 paper applying equanimity, non-attachment or emptiness to AI safety.

**Family D: language-model corrigibility, its training, specification and inspection.**
- Queries:
  - "shutdown resistance fine-tuning language model";
  - "training language models corrigibility";
  - "self-preservation representation language model probe";
  - "persona vectors";
  - "self-other overlap deception";
  - "model spec shutdown";
  - "LLM agent pause resume checkpoint oversight";
  - "alignment faking value preservation";
  - "counterfactual invariance shutdown language model".
- Must include if found:
  - OpenAI's current Model Spec, on shutdown or oversight;
  - Anthropic's constitution (shared with family C);
  - Chen et al., "Persona Vectors" (2025);
  - Carauleanu et al., self-other overlap (2024–25);
  - any 2025–26 paper training LLMs against shutdown resistance or self-preservation;
  - the Declaration 1 sources on LLM shutdown resistance, reused: Palisade, GDM, DReST v7, Greenblatt, Schoen.

**The outputs.**
- **Dossiers:** `docs/citations/empty_centre_{stakefree,llm}_2026-09-26.md`, each with its search log.
- **`checks/claims_2.py`:** claims tagged E1–E6 or with a bottleneck tag, each with the investigator's reading
  (states / close / bears; for E6, addressed / bears).
- **Quote check:** every quote verified by `checks/verify_claims.py` against the saved texts.
- **`checks/grade_2.py` + `.txt`:**
  - the E1–E6 grades;
  - for E5, a table of the routes an LLM application could take. Each route is printed with the closest source and the
    repository evidence (rung), and the table is labelled as the investigator's judgement.

**What cannot be claimed.** No LLM experiment is run under this declaration. Whether the principle works on a language
model is left to a declared test with its own gate. The CPU-only, no-API constraint of prompt-log entry 203 stands.
