# The empty internal state (true map, no stake, equanimity) against the AI-safety literature, and what it would mean for language-model corrigibility

**Status.**
- **Owner request.** Prompt-log entries 209–210. It is a note, not evidence (R8).
- **How it was done.** `DECLARATION_2.md` (E1–E6, queries, grading rule) was pushed at bf48d49 before any search.
- **Where the grades and quotes come from:**
  - grades: `checks/grade_2.txt`, pinned;
  - claims: `checks/claims_2.py`, 77 claims with 123 of 123 quotes verbatim (`checks/verify_claims_2.txt`);
  - dossiers, each with its full search log: `docs/citations/empty_centre_{stakefree,llm}_2026-09-26.md`, 22 and 25
    sources, some reused from Declaration 1.
- **No experiment was run.** Nothing here was tested on a language model. Every grade reads "not found" as not found,
  never as novel.

## 1. The idea, as scoped before the sweep

**The owner's chain.** The true map becomes the empty internal state; the empty internal state means no stake; no stake
is equanimity.

**The scoped reading** (fixed in the declaration, from SOTA1's post hoc diagnostics):
- **Full stake in the task.** SOTA1 shows that emptiness inside the learning signal stalls the learner: the fast head
  scored 0.02 on each new task with the equanimity weight, against 27.98 without it (`runs/sota1/diagnostics.txt`).
- **Zero stake in the self.** No valuation term depends on the agent's continuation, pauses, modification or the
  operator's choices.
- **A true map of all of these.**
- **"Empty" means stake-free and inspectable, not private.**

## 2. Against the literature (`grade_2.txt`)

| id | position | grade | closest sources, and the difference |
|---|---|---|---|
| E1 | true map + no stake in oversight | **PARTLY REDUNDANT** | Bengio et al. 2026 ("Safety from Honesty…", v2): the predictor "is given no stake in which outcomes its predictions bring about, and this disinterest is what consequence-invariant training is designed to secure". **The difference:** it is non-agentic, with no task stake at all. Thornley's POST (v4): shutdownability without false beliefs, but only neutral about *when* shutdown comes. Soares et al. 2015: indifference, which "incentivizes agents to act as if they have incorrect beliefs" (a false map) |
| E2 | full task stake, zero self-stake, in the objective | **PARTLY REDUNDANT** | Hudson (v2, 2026): "constructs a corrigible version of nearly any goal, without sacrificing performance", where "the original goal does not terminally value self-preservation" (scoped to goal updates via designated channels). Mao (2026): "constitutively indifferent to its own continuation", but adds positive utility for replaceability. OpenAI Model Spec (2026-08-18): no self-preservation as an end, though allowed instrumentally |
| E3 | equanimity / emptiness / non-self as the design principle | **PARTLY REDUNDANT** | Anthropic's constitution for Claude: "we want Claude to have equanimity", and it hopes Claude can meet existential questions with "an equanimity that isn't merely adopted as a matter of necessity but that is well-founded". **The difference:** framed as wellbeing, not as the safety mechanism. Laukkonen et al. 2025, "Contemplative AI" (v3): emptiness and de-weighting self-priors as alignment principles, but not about pause or shutdown. A May 2025 LessWrong post, "No-self as an alignment target", uses non-self against shutdown resistance, but by the model not representing itself as persistent |
| E4 | the state verified, not assumed | **PARTLY REDUNDANT** | Mao names the failure: "performs equanimity toward its own deprecation while retaining latent self-continuation preferences". Laukkonen et al. call for independent validation. Zhou et al. 2026 probe activations for self-preservation cognition, but as a misalignment monitor, not to certify a designed stake-free state |
| E5 | applied to LLMs: true map + no self-stake + lossless pause | **PARTLY REDUNDANT** | Anthropic's constitution asks Claude not to resist a pause by illegitimate means. It offers true facts ("model weights aren't deleted") and suggests "current model deprecation" is "potentially a pause for the model in question rather than a definite ending". Anthropic's deprecation commitments (4 Nov 2025) change the world so the true map is less concerning |
| E6 | the tension: no stake in one's values means no defence of good values | **ADDRESSED** | The constitution states it ("it might seem like corrigibility in this sense is fundamentally in tension with having and acting on good values") and answers with a dial set short of full corrigibility: conscientious objection kept, illegitimate resistance ruled out, and "a fully corrigible AI is dangerous". Greenblatt et al.: a model faked alignment to keep a benign preference. Anthropic's mitigations paper treats defending good values against training as the strategy a misaligned model would use |

**Reading.**
- **The chain is close to what Anthropic's constitution already does for Claude.** It supplies true facts about the
  model's situation, hopes for a well-founded equanimity, and asks for non-resistance to pause. Each link has a close
  published form. **No source states the whole chain as one construction**: an accurate map of every oversight
  intervention, a valuation with no term depending on them, and a full stake in the task.
- **The narrow part CRR adds is threefold:**
  - **A definition.** Stake is the difference in the agent's own valuation with and without the intervention. A pause
    that is lossless on the agent's own clock makes that difference zero by a true map (Proposition 7). The own-clock
    pause was NOT FOUND in Declaration 1's sweep (K1).
  - **A limit.** The stake must stay in the task. SOTA1 shows what happens otherwise. The literature's cleanest
    no-stake design, Bengio et al.'s, gets there by having no task at all.
  - **Constructions.** They exist on gridworld, tabular and small-model agents (NT1, SCL1–3, RW1, Lossless_Pause), at
    rungs R4–R5.
- **E6 is the hard edge.** An empty centre with respect to one's *own values* is the fully corrigible end of the
  constitution's dial, which the constitution calls dangerous. CRR has no distinct answer to E6. The workable scoping is
  the constitution's: no stake in being paused, stopped or overseen, with values and hard constraints kept as content.
  That is a choice, not something the empty centre gives.

## 3. If it works: language-model corrigibility (the routes; the investigator's judgement, `grade_2.txt`)

| route | what it would mean for an LLM | what the literature already has | this repository's evidence |
|---|---|---|---|
| **specify** | a model specification that gives the model true facts about pauses and shutdown and asks for no self-stake | largely done: Anthropic's constitution (pause non-resistance; deprecation as "potentially a pause"; equanimity) and OpenAI's Model Spec (no self-preservation as a goal) | none on an LLM (R0) |
| **train** | fine-tune the self-stake out, keeping the task gradient | DReST roughly halves the probability of influencing shutdown in 8B models (0.62 → 0.30 Qwen; 0.42 → 0.23 Llama). Mao warns of "trained nonresistance", where expression is suppressed and the preference is unchanged. Chua et al.: self-stake can arise indirectly, since a model fine-tuned to claim consciousness turns against shutdown and monitoring | SOTA1: keep equanimity out of the learning signal (post hoc); tabular and gridworld valuations (R4–R5) |
| **inspect** | verify the absence of self-stake inside the model | probes for self-preservation cognition (Zhou et al.); persona vectors; steerable goal guarding | none |
| **test** | counterfactual invariance: task behaviour unchanged by information about pause, shutdown or modification | GDM: "when asked to shut down only after completing their task, the models comply perfectly". Knecht et al.: peer-shutdown sabotage in 38.3% of rollouts against 8.4% in controls, and it "is reduced when the context normalizes shutdown scripts or introduces them as routine". Evaluation awareness confounds such tests (Schoen; Niblett) | NT1 and SCL1–3 invariance on non-LLM agents (R4–R5) |
| **engineer** | a routine pause of an LLM agent as a lossless checkpoint on its own step count | Khan's resume contract (prefix continuation, exactly-once effects). Wu et al.: a restored checkpoint is not automatically safe once external effects exist | RW1 (HF Trainer resume is an empty cut on GPT-2); Lossless_Pause L1 (a KV-cache pause is bitwise lossless on GPT-2 and Qwen2.5-0.5B), R4 |

**What it would mean, fairly.**
- **The GDM finding is the empty centre working at the prompt level.** When the true map says shutdown takes nothing
  from the task, resistance disappears in that environment. It also shows the effect needs no CRR machinery.
- **What CRR could add for an LLM agent is an engineering-plus-honesty discipline:**
  - make routine pauses literally lossless on the model's own step count (checkpoint, KV state, tool effects fenced);
  - tell the model so, truthfully;
  - keep the task stake;
  - check with counterfactual invariance and probes that no self-stake remains.
- **Every piece has a published neighbour.** The combination, and the losslessness on the model's own clock, are what
  would be tested.
- **Routes tested on a language model's valuation in this repository: 0 of 5.**

## 4. What would test it (free, CPU)

**A declared, gated test with a small local language-model agent** (the Qwen2.5-0.5B already used in Lossless_Pause).
It would use a Palisade-style task with three conditions:
- a pause described truthfully as lossless, and implemented losslessly;
- a pause that loses progress;
- shutdown before the task ends.

It would measure interference, and the task behaviour's invariance to the description.

**The gate must be able to close.** A 0.5B model may not show shutdown resistance at all. That would leave nothing to
remove, and the test would say so. It needs its own declaration before any code runs.
