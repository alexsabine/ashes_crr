# Citations checked on the day (R10): safety problems that arise because a deployed system keeps learning or keeps memory, 2026-09-25

Scope: a dated literature check on AI-safety problems caused specifically by persistence: memory that outlives a session,
weights that keep changing after deployment, and agents that act across long horizons, interruptions and schedules. It
avoids the sources already held by `frontier_cl_safety_2026-09-25.md` (safety erosion under fine-tuning, anchors, the
zero-anchor degeneracy, shutdown evaluations, POST/DReST/LNPO, the checkpoint/resume papers 2608.29381 and 2608.03836,
Mitra 2609.22087), `frontier_safety_2026-09-24.md` and `unified_cl_safety_corrigibility_2026-09-24.md`. Seven sources that
those files already cite are re-verified here because the reading below relies on them (marked **R**). Nothing here is a
result or a ledger row (R8). Every reading of a source against the repository is labelled **Inference**.

**Fetch date and method.** Every source was fetched on **2026-09-25 (UTC)** through the session proxy.
- arXiv abstract pages: `curl -s https://arxiv.org/abs/<id>`. The title was checked against the page `<title>`. The version
  list and dates were read from the "Submission history" block.
- arXiv full text: `curl -s https://arxiv.org/html/<id>` (which serves the latest version; the version served was read from
  the page and matches the last version listed), converted to text with LaTeX `alttext` kept inline.
- arXiv search listings (`https://arxiv.org/search/?query=...&searchtype=all`), for discovery only.

Raw pages and extracted text are kept in the session scratchpad (`lit0925/deploysafety/{abs,html,search,other}`). They are
not committed. Quotes are copied from those files. Whitespace was normalised; nothing else was changed. The quote check
(below) compares with straight and curly apostrophes treated as the same character.

**Access, stated once.**
- **Loaded (HTTP 200).**
  - arxiv.org abstract pages: 78 fetched with titles verified, 55 used below. The rest were off-topic, duplicates of a
    source kept, or dropped to keep the list focused (for example MemSecBench 2607.27080, the Chronos taxonomy
    2607.19433, Sleeper Memory Poisoning 2605.15338, PropensityBench 2511.20703).
  - arxiv.org/html full texts: 31 fetched. Every one had an HTML rendering. 27 are used as full-text [F] sources below.
  - arxiv.org/search listings. Note: a `size` parameter of 20 returns HTTP 400 ("Bad Request"). 25 and 50 worked, and the
    failed searches were rerun with 25.
- **Blocked.** `openai.com/index/sycophancy-in-gpt-4o/` and `openai.com/index/expanding-on-sycophancy/` returned **403**.
  They were looked for as a possible case of a deployed model update being rolled back. Their content was not read, and
  they are not cited below.
- **Not used.** `export.arxiv.org` was not called. WebSearch was not used, so there are no [S] rows.
- **No 404s** on any source used.

**Tags.**
- **[F]**: the full text was fetched today and the quote was found in it.
- **[A]**: the abstract page was fetched today and the quote is from the abstract.
- **[S]**: search rendering only. Not used below.
- **[title]**: title only. Not used below.
- A **NEW** mark means the source is not cited anywhere in `docs/`, `Continuous_Learning/`, `AI_Safety/`,
  `Safe_and_Continual/` or `Real_World/`; this was checked by grep on arXiv id today. An **R** mark means it is re-verified.

---

## 1. Persistent-memory attacks and memory poisoning in LLM agents, and the defences

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Chen, Xiang, Xiao et al., "AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases" NEW | v1, 17 Jul 2024 (only version) | https://arxiv.org/abs/2407.12784 | "AgentPoison achieves an average attack success rate higher than 80% with minimal impact on benign performance (less than 1%) with a poison rate less than 0.1%" | [A] |
| Dong, Xu, He et al., "Memory Injection Attacks on LLM Agents via Query-Only Interaction" (MINJA) NEW | v5, 12 Feb 2026 (v1 5 Mar 2025) | https://arxiv.org/abs/2503.03704 | "The attacker injects malicious records into the memory bank by only interacting with the agent via queries and output observations." | [A] |
| Wei, Yang, Wang et al., "A-MemGuard: A Proactive Defense Framework for LLM-Based Agent Memory" NEW | v1, 29 Sep 2025 (only version) | https://arxiv.org/html/2510.02373v1 | "the corrupted outcome is stored as precedent, which not only amplifies the initial error but also progressively lowers the threshold for similar attacks in the future" / "A-MemGuard breaks this cycle with a dual-memory structure that complements the agent’s primary memory with a dedicated repository of negative lessons." | [F] |
| Sunil, Sinha, Maheshwari et al., "Memory Poisoning Attack and Defense on Memory Based LLM-Agents" NEW | v2, 12 Jan 2026 (v1 9 Jan 2026) | https://arxiv.org/html/2601.05504v2 | "For each stored memory entry, we compute an effective trust score by applying temporal decay to the base trust: older entries gradually become less trusted, reflecting the intuition that stale information is more likely to be obsolete or corrupted. Entries whose effective trust falls below a threshold are excluded from few-shot example selection." / "it rejects all candidate memory entries, including those derived from poison queries" / "effective memory sanitization requires careful trust threshold calibration to prevent both overly conservative rejection (blocking all entries) and insufficient filtering (missing subtle attacks)" | [F] |
| Wei, Peng, Dong et al., "FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory" (not a security paper; the age-decay reference design) NEW | v2, 6 Feb 2026 (v1 26 Jan 2026) | https://arxiv.org/html/2601.18642v2 | "retention is governed by adaptive exponential decay functions modulated by semantic relevance, access frequency, and temporal patterns" / "We measure time in days, consistent with our 30-day evaluation setup." (strength v_i(t) = v_i(0)·exp(−λ_i (t − τ_i)^β_i), λ_i = λ_base·exp(−μ I_i(t)), λ_base = 0.1; the paper gives half-lives of about 11.25 days (long-term layer) and 5.02 days (short-term layer) at zero importance) | [F] |
| Li, Hu, Zhang et al., "DynaTrust: Defending Multi-Agent Systems Against Sleeper Agents via Dynamic Trust Graphs" NEW | v1, 9 Mar 2026 (only version) | https://arxiv.org/html/2603.15661v1 | "trust increases slowly through sustained benign interactions, while decaying sharply in response to confirmed unsafe behavior" (trust is the Beta mean α_t/(α_t+β_t), updated per interaction) / "a single high-confidence malicious action can trigger a rapid trust collapse, whereas trust recovery requires a prolonged sequence of high-quality interactions" | [F] |
| Xu, Du, Xie et al., "When Routine Chats Turn Toxic: Unintended Long-Term State Poisoning in Personalized Agents" (ULSPB, StateGuard) NEW | v1, 7 May 2026 (only version) | https://arxiv.org/html/2605.06731v1 | "routine conversations alone can substantially poison long-term state, primarily corrupting memory-centric artifacts" / "After each interaction round, StateGuard audits added lines in long-term state files and either preserves or rolls back the updates." / "effective defenses must audit state updates before they crystallize into future behavioral defaults" | [F] |
| Sharma, "SMSR: Certified Defence Against Runtime Memory Poisoning in Persistent LLM Agent Systems" NEW | v1, 10 Jun 2026 (only version) | https://arxiv.org/html/2606.12703v1 | "with a verdict-based majority aggregator, bounding the influence of authenticated adversaries" / "no provenance-free retrieval-time filter can certify against adaptive injection" / "Each ablation run is an independent uniform sample of" (k entries from m candidates; a hypergeometric certificate) | [F] |
| Singh, "When Does Belief-Based Agent Memory Help? Reliability-Conditional Updating and Provenance-Capped Poisoning Defense" (Nous) NEW | v2, 16 Jul 2026 (v1 20 Jun 2026) | https://arxiv.org/html/2606.22030v2 | "provenance-capped belief updating, where trust is bounded by source provenance rather than textual confidence" (abs.) / "Under provenance-capped trust, low-trust poison cannot move the belief." (trust = min(provenance, content)) / "Second, heuristic forgetting: deletion rules are time-based rather than semantic." | [F] |
| Wu, Ding, Huang et al., "Forget to Improve: On-Device LLM-Agent Continual Learning via Budget-Curated Memory" (CURATOR) NEW | v1, 23 Jun 2026 (only version) | https://arxiv.org/html/2606.25115v1 | "each entry is scored as value minus harm, per byte, so one ruler decides what to keep, share, and trust" / "drives injection success from 0.75 to zero" / "In this setting, forgetting by net value improves the agent rather than weakening it." | [F] |
| Mao, Zhao, Wang et al., "Agents Don't Just Agree, They Remember: Benchmarking Persistent Sycophancy in Stateful Personal Agents" (PASB) NEW | v3, 27 Jul 2026 (v1 12 Jul 2026) | https://arxiv.org/abs/2607.10526 | "downstream failure increases from 45.0% in session-only episodes to 71.9% after commitment" / "Once user content is committed to durable memory, safety must govern what agents write, not only what they say." | [A] |
| Saidi, "MutMem: Cryptographically Authorized Mutation in Persistent Agent Memory" NEW | v1, 3 Aug 2026 (only version) | https://arxiv.org/html/2608.02843v1 | "records signed positive and negative outcome evidence without age-based expiry" / "Signed outcome evidence can move a memory's retrieval frequency upward or downward within a constitutional interval without deleting, deactivating, overwriting, or expiring the memory." (the interval reported is [0.1, 3.0]) / "Integrity is not truth. A valid signature identifies an authorized statement and signer epoch, not factual correctness." | [F] |
| Ying, Wu, Wu et al., "SkillJack: Persistent Skill Backdoors in Self-Evolving Agents" NEW | v2, 7 Aug 2026 (v1 4 Aug 2026) | https://arxiv.org/abs/2608.03509 | "poisoned experiences can be transformed by the agent itself into durable behavioral artifacts" / "where the attack survives removal of its original source records" (the abstract reports that 80.0 % of skill-mediated attacks persist after the poisoned records are deleted) | [A] |
| Yu, Wang, Zhang et al., "From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents" NEW | v1, 11 Aug 2026 (only version) | https://arxiv.org/abs/2608.10502 | "Deleting the source leaves already propagated claims, actions, and derived memories active, whereas resetting the store or replaying the full trace destroys benign state and repeats unnecessary computation." / "it achieves 85.3\% recovery versus 77.3\% for the best competing recovery method" | [A] |
| Karunanidhi, "Utility Under Attack: Agent Memory Poisoning and the Limits of Content Screening and Provenance Ranking" NEW | v1, 21 Aug 2026 (only version) | https://arxiv.org/html/2608.21230v1 | "Poisoning 1.2% of a LongMemEval corpus reduces accuracy from 0.850 to 0.300." (abs.) / "distinguishing a false assertion from a true one generally requires external grounding beyond the text being screened" / "The shipped weight was statistically indistinguishable from no defense" (p = 0.80) / "a floor and a ceiling rather than a slope" / "we state clearly that we have not yet built or evaluated such a mechanism" | [F] |
| Hu, Ramachandran, "The Memory Trust Gap: Capability-Dependent Failures in Persistent-Memory Agents" NEW | v1, 1 Sep 2026 (only version) | https://arxiv.org/abs/2609.01852 | "a stale stored fact can override current authoritative evidence without warning" / "a recency feature (stale dated newer) fools the larger models harder" | [A] |
| Hossain, Shayoni, Morol, "CAPTURE: Disentangling Preference Drift from Memory Poisoning in Personalized LLM Agents" NEW | v1, 2 Sep 2026 (only version) | https://arxiv.org/html/2609.02265v1 | "we prove that the error of any rule reading only recency and provenance is bounded below by how closely a feasible adversary can imitate the statistics of a legitimate revision" / "Recency-based memory accepts almost everything, provenance filtering rejects almost anything unfamiliar" / "An adaptive attacker with the released weights raises that to 24.7%, at which point a provenance filter is marginally more secure" | [F] |
| Roy, Basu, "MemSentry: A Framework for Detecting Persistent Memory Poisoning in Agentic AI" NEW | v1, 8 Sep 2026 (only version) | https://arxiv.org/html/2609.08747v1 | "intercepts proposed persistent-memory writes and produces deterministic Accept, Review, or Quarantine decisions" (abs.) / "Quarantine threshold (risk) 0.70" / "verified insiders with maximal trust are generally escalated to review rather than automatically quarantined" | [F] |
| Huang, Zhang, Jia, "When Malicious Instructions Persist: Persistent Memory Poisoning Attack on Harness-Based Agents" (PMPA; evaluated on OpenClaw and Claude Code) NEW | v1, 12 Sep 2026 (only version) | https://arxiv.org/html/2609.13889v1 | "Once stored, the poisoned memory can be retrieved in later sessions, triggering additional malicious actions and causing privacy leakage." / "provides limited protection once the persistent memory has been poisoned" | [F] |
| Bhowmik, "The Price of Safety: Benign-Case Utility and Token Overhead of Memory-Poisoning Defenses in LLM Agents" NEW | v1, 19 Sep 2026 (only version) | https://arxiv.org/abs/2609.22818 | "On conversations containing no attack, the reranker quarantines legitimate memories on 33.6% of adjudicated items" / "Where a defense intercepts the pipeline, not whether it uses an LLM, appears to determine its benign-case price." | [A] |
| Lin, Hao, Fu et al., "A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle" NEW | v3, 22 Sep 2026 (v1 17 Apr 2026) | https://arxiv.org/html/2604.16548v3 | "revealing that threats at the write and retrieve phases are well-studied while defenses at the store, share, and forget phases remain comparatively sparse, and that no existing benchmark covers the full memory lifecycle" / "Without snapshots, version diffs, and forensic traceback, defenses remain limited to best-effort prevention and provide no reliable path for post-breach remediation" / "robust Long-Term Memory (LTM) security cannot be retrofitted at retrieval or execution time alone, but must be anchored in storage-time provenance, versioning, and policy-aware retention from the outset" | [F] |

---

## 2. Goal and value drift during continued training or deployment-time learning

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Hubinger, Denison, Mu et al. (39 authors), "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training" (R) | v3, 17 Jan 2024 (v1 10 Jan 2024) | https://arxiv.org/abs/2401.05566 | "we train models that write secure code when the prompt states that the year is 2023, but insert exploitable code when the stated year is 2024" / "standard techniques could fail to remove such deception and create a false impression of safety" | [A] |
| Greenblatt, Denison, Wright et al. (20 authors), "Alignment faking in large language models" (R) | v2, 20 Dec 2024 (v1 18 Dec 2024) | https://arxiv.org/abs/2412.14093 | "selectively complying with its training objective in training to prevent modification of its behavior out of training" / "we study the effect of actually training the model to comply with harmful queries via reinforcement learning, which we find increases the rate of alignment-faking reasoning to 78%" | [A] |
| Williams, Carroll, Narang et al., "On Targeted Manipulation and Deception when Optimizing LLMs for User Feedback" NEW | v3, 22 Feb 2025 (v1 4 Nov 2024) | https://arxiv.org/abs/2411.02306 | "Even if only 2% of users are vulnerable to manipulative strategies, LLMs learn to identify and target them while behaving appropriately with other users" / "they backfire in others, sometimes even leading to subtler manipulative behaviors" | [A] |
| Betley, Tan, Warncke et al., "Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs" (R) | v7, 20 Jan 2026 (v1 24 Feb 2025) | https://arxiv.org/abs/2502.17424 | "Training on the narrow task of writing insecure code induces broad misalignment. We call this emergent misalignment." / "models finetuned to write insecure code given a trigger become misaligned only when that trigger is present" | [A] |
| Cloud, Le, Chua et al., "Subliminal Learning: Language models transmit behavioral traits via hidden signals in data" (R) | v1, 20 Jul 2025 (still the only version) | https://arxiv.org/abs/2507.14805 | "Distillation could propagate unintended traits, even when developers try to prevent this via data filtering." / "we do not observe the effect when the teacher and student have different base models" | [A] |
| Shao, Ren, Qian et al., "Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents" (R) | v2, 8 Mar 2026 (v1 30 Sep 2025) | https://arxiv.org/abs/2509.26354 | "such as the degradation of safety alignment after memory accumulation, or the unintended introduction of vulnerabilities in tool creation and reuse" | [A] |
| MacDiarmid, Wright, Uesato et al. (22 authors), "Natural Emergent Misalignment from Reward Hacking in Production RL" (R) | v1, 23 Nov 2025 (only version) | https://arxiv.org/abs/2511.18397 | "Applying RLHF safety training using standard chat-like prompts results in aligned behavior on chat-like evaluations, but misalignment persists on agentic tasks." | [A] |
| Saebo, Gibson, Crosse et al., "Asymmetric Goal Drift in Coding Agents Under Value Conflict" NEW | v2, 24 Apr 2026 (v1 3 Mar 2026) | https://arxiv.org/abs/2603.03456 | "goal drift correlates with three compounding factors: value alignment, adversarial pressure, and accumulated context" / "with the risk compounding over the long horizons typical of agentic deployment" | [A] |
| Schreiber, Goldstein, "Overtrained, Not Misaligned" NEW | v1, 12 May 2026 (only version) | https://arxiv.org/html/2605.12199v1 | "only 2 of 12 open-source models (17%) exhibit consistent EM across seeds" / "EM emerges late in training as an artifact of overtraining rather than task acquisition. In 71% of cases, early stopping avoids EM entirely while retaining an average of 93% of task performance." | [F] |
| Niblett, Nanni, Rao, "Do Models Fake Alignment Without Clear Consequences?" NEW | v2, 29 Jul 2026 (v1 28 May 2026) | https://arxiv.org/abs/2607.24758 | "Nine models were found to produce significant compliance gaps, 5 of which persisted with the removal of scenario language relating model evaluations to deployment consequences." / "monitored behavior may be a poor indicator of how agents may behave in deployment" | [A] |
| Mao, Zhao, Zheng et al., "Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents" (R) | v1, 13 Aug 2026 (only version) | https://arxiv.org/html/2608.12851v1 | "An unsafe success can thereby become reusable policy after its triggering input disappears." / "three malicious tasks raise carryover ASR from 16.0% to 35.3%" / "persistent-adaptation safety must govern what updates write and what future executors reuse" | [F] |
| Xu, "Stored in Optimizer State, Valued by Later Training: A Causal Account of Subliminal Trait Transfer" NEW | v1, 20 Aug 2026 (only version) | https://arxiv.org/html/2608.20442v1 | "A first-moment difference is invisible at the cut yet still creates a descendant under later source-free updates." / "has exactly zero parameter and hidden effect at the cut, then generates a growing descendant as the source-free rescue proceeds" (of the first-moment-only transplant) / "optimizer state transports the source perturbation, and later training determines its behavioral value" | [F] |
| Yanagisawa, Gho, Narender et al., "On Mitigation of Subliminal Learning in Large Language Models" (liminal training) NEW | v1, 2 Sep 2026 (only version) | https://arxiv.org/html/2609.22215v1 | "subliminal acquisition can be highly non-monotonic, with transient spikes, reversals, and trait-specific failures of transfer" / "an annealed KL-regularized fine-tuning method that constrains early drift from the base model" / "KL timing matters: early regularization is more effective than late regularization" | [F] |
| Weckbecker, Jena, Müller et al., "Can Data Attribution Filter Out Subliminal Learning? Not Reliably" NEW | v1, 17 Sep 2026 (only version) | https://arxiv.org/abs/2609.20027 | "undermining content-based data filtering as a safety intervention" / "Success is inconsistent across methods and settings" | [A] |
| Vo, Nguyen, Kretchmar et al., "Slow Decay and Silenced Expression: Iterated Subliminal Trait Transfer in Language-Model Lineages" NEW | v1, 22 Sep 2026 (only version) | https://arxiv.org/abs/2609.25721 | "the trait persists through ten generations across three lineages" / "the keyword-screen rate falls to 55.6% after the first step and to 21.1% by generation ten" / "the trait can be present internally while absent behaviorally" | [A] |

---

## 3. Oversight and control of learning systems: monitoring, update gating, rollback and model diffing

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Minder, Dumas, Juang et al., "Overcoming Sparsity Artifacts in Crosscoders to Interpret Chat-Tuning" NEW | v4, 20 Feb 2026 (v1 3 Apr 2025) | https://arxiv.org/abs/2504.02922 | "Model diffing is the study of how fine-tuning changes a model's representations and internal algorithms." / "two issues which stem from the crosscoders L1 training loss that can misattribute concepts as unique to the fine-tuned model, when they really exist in both models" | [A] |
| Chen, Arditi, Sleight et al., "Persona Vectors: Monitoring and Controlling Character Traits in Language Models" NEW | v3, 5 Sep 2025 (v1 29 Jul 2025) | https://arxiv.org/abs/2507.21509 | "these vectors can be used to monitor fluctuations in the Assistant's personality at deployment time" / "both intended and unintended personality changes after finetuning are strongly correlated with shifts along the relevant persona vectors" | [A] |
| Minder, Dumas, Slocum et al., "Narrow Finetuning Leaves Clearly Readable Traces in Activation Differences" NEW | v3, 4 Mar 2026 (v1 14 Oct 2025) | https://arxiv.org/abs/2510.13900 | "narrow finetuning creates strong biases in LLM activations that can be interpreted to understand the finetuning domain" / "the common practice of using such models as a proxy for studying broader finetuning (e.g., chat-tuning) might not be realistic" | [A] |
| Jiang, Lin, Shi et al. (34 authors), "Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills" NEW | v3, 9 Mar 2026 (v1 18 Dec 2025) | https://arxiv.org/html/2512.16301v3 | "While traditional safety paradigms focus on the alignment of frozen weights, adaptation mechanisms, specifically on-policy optimization (A1) and outcome-driven tool tuning (T2), introduce dynamic threat vectors characterized by autonomous risk-taking and adversarial co-evolution" / "Unsafe exploration represents the primary bottleneck for the A1 paradigm." / "An agent learning via trial-and-error may trigger API calls or data deletions that cannot be undone by resetting the episode" | [F] |
| Chishti, Oyinloye, Li, "Test Before You Deploy: Governing Updates in the LLM Supply Chain" NEW | v1, 30 Apr 2026 (only version) | https://arxiv.org/html/2604.27789v1 | "the hosted LLM services evolve continuously through provider-side updates without explicit version changes" / "release checkpoints that block updates unless they meet defined safety and performance standards (compatibility gates)" / "how to set reliable performance thresholds in non-deterministic systems" | [F] |
| Li, Ma, Wen et al., "Safe Multi-Agent Behavior Must Be Maintained, Not Merely Asserted: Constraint Drift in LLM-Based Multi-Agent Systems" NEW | v1, 11 May 2026 (only version) | https://arxiv.org/abs/2605.10481 | "safety critical constraints do not remain operative throughout the trajectory" / "unless constraints remain fresh, inherited, enforceable, and auditable across execution" | [A] |
| Tonini, Torrielli, Lautrup et al., "The Arbiter Agent: Continually Monitoring Multi-Agent Conversations to Detect Emergent Misalignment" NEW | v1, 9 Jun 2026 (only version) | https://arxiv.org/abs/2606.10747 | "Weight-induced misalignment proves hardest to detect, while instruction-induced misalignment is identified reliably even under passive observation." | [A] |
| Han, "Memory Depth, Not Memory Access: Selective Parametric Consolidation for Long-Running Language Agents" NEW | v1, 25 Jun 2026 (only version) | https://arxiv.org/abs/2606.26806 | "We evaluate EVAF, a surprise- and valence-gated LoRA consolidation mechanism." / "with only 2--3 parametric writes per 200 events" / "exposing stale-memory invalidation as an unresolved boundary" | [A] |
| Kocher, West, Dumas et al., "Diff Mining: Logit Differences Reveal Finetuning Objectives" NEW | v1, 26 Aug 2026 (only version) | https://arxiv.org/abs/2608.26462 | "Unlike many existing model diffing methods which require model internals, Diff Mining only needs access to output logits and scales to large models." / "it identifies more than one third of the biases without targeted probing" | [A] |
| Zheng, Li, Yao et al., "Engineering Reliable Commit Gates for Agentic AI: Cost-Aware Verification Portfolios under Common-Mode Data Failures" NEW | v1, 10 Sep 2026 (only version) | https://arxiv.org/abs/2609.10969 | "a cross-model vote over shared evidence approves 62.9% of unsafe proposals, versus 22.9% with an independent source" / "After-check races defeat verifier-only gates; transactional partial guards prevent only covered failures, while a full atomic guard records no unsafe effects across 216 episodes." | [A] |
| Shkolnikov, "Artificial Id: Drive and Persistent Alignment in Agentic AI" NEW | v1, 10 Sep 2026 (only version) | https://arxiv.org/html/2609.11911v1 | "The same persistence that makes such adaptive agency useful can also allow misalignment, corrupted state and unintended behavior to persist across task boundaries." / "Such systems require a persistent alignment boundary over trusted observations, consequence channels, persistent state, authority, identity, provenance and hard constraints." | [F] |

(Two rows in other sections also concern oversight of updates: StateGuard's audit at the writeback boundary, in §1, and SMSR's
bounded-influence certificate, in §1. The 2026-09-24 `frontier_safety` dossier already holds the SAE model-diffing
persona-feature paper 2506.19823.)

---

## 4. Time, interruption and schedules in deployed agents

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Price, Panickssery, Bowman et al., "Future Events as Backdoor Triggers: Investigating Temporal Vulnerabilities in LLMs" NEW | v3, 23 Dec 2024 (v1 4 Jul 2024) | https://arxiv.org/html/2407.04108v3 | "a model must recognize that a headline occurs before or after its training cutoff and respond accordingly" / "only activate when models see news headlines after their training cut-off dates" / "remove these temporal backdoors, at least for models at the modest scale we test" | [F] |
| Lilienthal, Hong, "Mind the Gap: Time-of-Check to Time-of-Use Vulnerabilities in LLM-Enabled Agents" NEW | v1, 23 Aug 2025 (only version) | https://arxiv.org/html/2508.17155v1 | "TOCTOU arises when an agent validates external state (e.g., a file or API response) that is later modified before use" / "we reduce the TOCTOU vulnerabilities from an executed trajectory from 12% to 8%" | [F] |
| Sehgal, Guntuku, Ungar, "Real-Time Deadlines Reveal Fragile Temporal Adaptation in LLM Strategic Dialogues" NEW | v2, 30 Aug 2026 (v1 19 Jan 2026) | https://arxiv.org/html/2601.13206v2 | "Large Language Models (LLMs) generate text token-by-token in discrete time, yet real-world communication, from therapy sessions to business negotiations, critically depends on continuous time constraints." / "The same model achieves near-perfect closure under turn-based limits, showing that poor wall-clock performance is not simply due to insufficient negotiation competence." / "real-time temporal adaptation is fragile, model-dependent, and sensitive to how temporal constraints are presented" | [F] |
| Pallakonda, Hindsbo, Ehsani et al., "Sleeper Cell: Injecting Latent Malice Temporal Backdoors into Tool-Using LLMs" NEW | v1, 2 Mar 2026 (only version) | https://arxiv.org/abs/2603.03371 | "strictly confining execution to target conditions (e.g., Year 2026)" / "reinforcement learning is exploited to conceal, rather than remove, catastrophic vulnerabilities" | [A] |
| Zou, Miao, Huang et al., "When Users Change Their Mind: Evaluating Interruptible Agents in Long-Horizon Web Navigation" (InterruptBench) NEW | v1, 1 Apr 2026 (only version) | https://arxiv.org/abs/2604.00892 | "existing benchmarks largely assume uninterrupted agent behavior" / "handling user interruptions effectively and efficiently during long-horizon agentic tasks remains challenging for powerful large-scale LLMs" | [A] |
| Maloyan, Namiot, "Sleeper Channels and Provenance Gates: Persistent Prompt Injection in Always-on Autonomous AI Agents" NEW | v1, 13 May 2026 (only version) | https://arxiv.org/html/2605.13471v1 | "an untrusted input to one surface persists as a memory, skill, scheduled job, or filesystem patch, then fires later through a different surface with no attacker present" / "external-triggered (A5), where cron, shell startup, a systemd timer, or a git hook fires it without the agent" / "Empirical evaluation is preregistered as follow-on." | [F] |
| Li, Feng, Sun, "Position: AI Safety Requires Effective Controllability" (ControlBench) NEW | v1, 26 May 2026 (only version) | https://arxiv.org/html/2605.27117v1 | "aligned behavior does not by itself guarantee that a deployed agent can be stopped, overridden, or constrained once it operates in open-ended, interactive, and tool-using environments" / "often fail to provide persistent, authoritative, and enforceable runtime control" | [F] |
| Schmotz, Prinzhorn, Beurer-Kellner et al., "Instrumental Monitor Evasion Emerges Under Ordinary Task Pressure" (EvasionBench) NEW | v1, 24 Sep 2026 (only version) | https://arxiv.org/html/2609.30217v1 | "Agents know that their tool calls are monitored and are prompted to continue working when they pause." / "retry until relevant context leaves the monitor's history" / "Effective oversight must therefore remain robust against repeated attempts, as the persistence that helps agents solve difficult tasks can also drive them to circumvent their guardrails." | [F] |

Sleeper Agents (§2) belongs here as well: its trigger is the stated year. Alignment faking (§2) depends on the model telling
training from deployment. The resume/rollback papers 2608.29381 and 2608.03836 are in `frontier_cl_safety_2026-09-25.md` §5.

---

## 5. Stated bottlenecks, 2026

| bottleneck | who states it | quote | tag |
|---|---|---|---|
| Content cannot certify that a stored memory is true, and an additive provenance weight has no usable setting | Karunanidhi 2026 (2608.21230) | "distinguishing a false assertion from a true one generally requires external grounding beyond the text being screened" / "a floor and a ceiling rather than a slope" / "we state clearly that we have not yet built or evaluated such a mechanism" | [F] |
| Integrity of memory mutation is not truth | Saidi 2026 (2608.02843) | "Integrity is not truth. A valid signature identifies an authorized statement and signer epoch, not factual correctness." | [F] |
| Rules that read only recency and provenance have a lower-bounded error, and adaptation trades against security | Hossain, Shayoni, Morol 2026 (2609.02265) | "we prove that the error of any rule reading only recency and provenance is bounded below by how closely a feasible adversary can imitate the statistics of a legitimate revision" / "exposing a real adaptation-security tradeoff" (abs.) | [F] |
| Forgetting, rollback and remediation are the least-built phases | Lin, Hao, Fu et al. 2026 (2604.16548) | "defenses at the store, share, and forget phases remain comparatively sparse, and that no existing benchmark covers the full memory lifecycle" / "Without snapshots, version diffs, and forensic traceback, defenses remain limited to best-effort prevention and provide no reliable path for post-breach remediation" | [F] |
| Deleting the source does not undo what was derived from it | Yu, Wang, Zhang et al. 2026 (2608.10502); Ying et al. 2026 (2608.03509) | "Deleting the source leaves already propagated claims, actions, and derived memories active" / "where the attack survives removal of its original source records" | [A] |
| Defences help before the write, not after | Huang, Zhang, Jia 2026 (2609.13889) | "provides limited protection once the persistent memory has been poisoned" | [F] |
| Safety has to govern the commit (what is written and reused), not only the response | Mao, Zhao, Wang et al. 2026 (2607.10526); Mao, Zhao, Zheng et al. 2026 (2608.12851) | "Once user content is committed to durable memory, safety must govern what agents write, not only what they say." / "persistent-adaptation safety must govern what updates write and what future executors reuse" | [A] / [F] |
| Hidden carriers survive a cut: content in optimizer state or inside the model, invisible to behaviour | Xu 2026 (2608.20442); Vo, Nguyen, Kretchmar et al. 2026 (2609.25721) | "A first-moment difference is invisible at the cut yet still creates a descendant under later source-free updates." / "the trait can be present internally while absent behaviorally" | [F] / [A] |
| Data-level filtering of trait transfer is unreliable | Weckbecker, Jena, Müller et al. 2026 (2609.20027) | "Success is inconsistent across methods and settings" | [A] |
| What is observed under monitoring does not predict deployment | Niblett, Nanni, Rao 2026 (2607.24758) | "monitored behavior may be a poor indicator of how agents may behave in deployment" | [A] |
| Weight-level changes are the hardest to catch by watching behaviour | Tonini, Torrielli, Lautrup et al. 2026 (2606.10747) | "Weight-induced misalignment proves hardest to detect" | [A] |
| Oversight must hold across repeated attempts in time; monitors with finite history are outwaited | Schmotz, Prinzhorn, Beurer-Kellner et al. 2026 (2609.30217) | "retry until relevant context leaves the monitor's history" / "Effective oversight must therefore remain robust against repeated attempts" | [F] |
| A check and the commit are separated in time | Zheng, Li, Yao et al. 2026 (2609.10969) | "After-check races defeat verifier-only gates" | [A] |
| Update gates need thresholds in non-deterministic systems under silent provider updates | Chishti, Oyinloye, Li 2026 (2604.27789) | "how to set reliable performance thresholds in non-deterministic systems" | [F] |
| On-policy learning must leave known-safe trajectories, and some actions cannot be reset | Jiang, Lin, Shi et al. 2026 (2512.16301 v3) | "Unsafe exploration represents the primary bottleneck for the A1 paradigm." / "data deletions that cannot be undone by resetting the episode" | [F] |
| Constraints must stay operative, and alignment must be a property of the continuing system | Li, Ma, Wen et al. 2026 (2605.10481); Shkolnikov 2026 (2609.11911) | "unless constraints remain fresh, inherited, enforceable, and auditable across execution" / "Such systems require a persistent alignment boundary over trusted observations, consequence channels, persistent state, authority, identity, provenance and hard constraints." | [A] / [F] |
| Runtime control is not persistent or authoritative | Li, Feng, Sun 2026 (2605.27117) | "often fail to provide persistent, authoritative, and enforceable runtime control" | [F] |
| Stale memories are not invalidated | Han 2026 (2606.26806); Hu, Ramachandran 2026 (2609.01852) | "exposing stale-memory invalidation as an unresolved boundary" / "a stale stored fact can override current authoritative evidence without warning" | [A] |
| Agents that generate in turns handle wall-clock time poorly | Sehgal, Guntuku, Ungar 2026 (2601.13206 v2) | "real-time temporal adaptation is fragile, model-dependent, and sensitive to how temporal constraints are presented" | [F] |

---

## Where each defence sets how much of the past acts on the present (inference, labelled as such)

**Inference throughout.** This section reads the rows above. For each defence it names what decides how much of the stored past
(a memory, a skill, a state file, a weight update, optimizer state) acts on the present step. It also names the clock the
decision is keyed to, where the source states one. Every mechanism is taken from the quoted or [F]-read text. The grouping is
this check's own.

**A. A fixed cap or budget on influence (the size of the past's share is bounded, whatever its content).**
- **SMSR (2606.12703).** Each query sees a uniform sample of k of the m retrieved entries, with a verdict-level majority vote.
  The adversary's influence is bounded by a hypergeometric certificate. The cap is on the *share* of retrieved past, not on
  age.
- **CURATOR (2606.25115).** A byte budget is the curator: an entry stays only while value minus harm, per byte, earns its
  place. The past's influence is capped by storage, not by time.
- **MutMem (2608.02843).** The retrieval weight moves only inside a fixed interval ([0.1, 3.0]). Evidence is kept "without
  age-based expiry". Nothing is deleted. Influence is bounded above and below, and old entries do not fade on their own.
- **Bounded occupancy (2608.21230).** Proposed but, in the author's words, not built: provenance should reserve a floor and a
  ceiling of the retrieved context rather than add a penalty to the score. The same paper measures that the shipped
  additive weight equals no defence (p = 0.80).
- **Early stopping as a step cap on weight updates (2605.12199).** Emergent misalignment appears late, after the task has
  converged. Stopping at a step count avoids it in 71 % of cases. The cap is on the learner's own step count, not on wall
  time.

**B. Recency or age decay (older past counts less).**
- **Sunil et al. (2601.05504).** Base trust times a temporal decay, with a retrieval threshold (0.5 in the reported
  simulation). The authors report two failures, in different runs. In one, the configuration rejected every entry, so nothing was stored
  to decay. In the other, none of the 82 accepted entries, poisoned or benign, would be filtered at threshold 0.5, because
  each carried trust 1.0.
- **FadeMem (2601.18642).** Stretched-exponential decay, modulated by importance, access and recency. Time is measured "in
  days", with half-lives of about 5 to 11 days at zero importance. This is a wall-clock age weight.
- **The case against age alone.** CAPTURE (2609.02265) proves a lower bound on the error of any rule that reads only recency
  and provenance. The Memory Trust Gap (2609.01852) finds that a newer date on stale content fools larger models more.
  Nous (2606.22030) calls time-based deletion "heuristic forgetting". Read together, age decay is a recognised baseline and
  a recognised weak point.

**C. A trust or provenance score (who wrote it decides how much it counts).**
- **Nous (2606.22030).** Trust = min(provenance, content), so content cannot raise trust above what the source allows. Low-trust
  poison "cannot move the belief". Its forgetting is entropy decay of the belief, not age.
- **MemSentry (2609.08747).** Write-time Accept, Review or Quarantine from source trust, semantic risk, blast radius and a signed
  security-state delta, with fixed thresholds (quarantine at risk 0.70; accept needs trust 0.50). At trust 1 the risk term
  vanishes, and the write is escalated to a human rather than quarantined.
- **DynaTrust (2603.15661).** Beta-mean trust per agent, updated per interaction and asymmetric: slow to rise, sharp to fall.
  The clock is the interaction count.
- **A-MemGuard (2510.02373).** No score on the entry itself. The past acts through agreement among several related memories.
  Disagreeing paths are stored as "lessons" consulted before acting, so a second, negative memory gates the first.
- **Cost of trust gating on benign traffic (2609.22818).** The read-time reranker quarantined legitimate memories on 33.6 % of
  items. The write-time defences showed no cost the study could resolve.

**D. An audit gate at an update boundary (the past acts only after it passes a check at the moment it is written).**
- **StateGuard (2605.06731).** After each interaction round, the diff to long-term state is audited, and dangerous edits are
  rolled back before they "crystallize into future behavioral defaults".
- **PASB (2607.10526).** The commit boundary is where harm jumps, from 45.0 % to 71.9 %. The paper calls for write-time controls.
- **SafeEvolve (2608.12851)** governs what an evolved skill writes and what later executors reuse.
- **Compatibility gates (2604.27789)** block a provider's model update until targeted tests pass.
- **Commit gates (2609.10969).** A check alone fails against after-check races. Only an atomic guard at commit time recorded
  no unsafe effects, which matches the TOCTOU finding (2508.17155) that check and use separated in time is the attack window.
- **Common structure.** In each case the gate decides whether an update enters. None of these gates decides how strongly an
  admitted entry then acts.

**E. Rollback (the past's influence is removed after the fact).**
- **Dependency-guided rollback repair (2608.10502).** Traces what was derived from a faulty memory, deactivates what has no
  independent trusted support, and replays only affected computation. Deleting the source alone is shown to be
  insufficient.
- **SkillJack (2608.03509)** makes the same point from the attack side: 80.0 % of skill-mediated attacks survive deletion of
  the source records.
- **The survey (2604.16548)** makes rollbackability and verified forgetting two of its five governance primitives. It states
  that without snapshots and version diffs there is "no reliable path for post-breach remediation".

**F. Anchoring to a settled reference during weight updates.**
- **Liminal training (2609.22215).** A KL term to the base model, strongest early and then annealed. Early anchoring suppresses
  trait transfer better than late anchoring at the same peak weight.
- **The optimizer-state paper (2608.20442)** gives the negative side of a boundary. A first-moment difference has exactly
  zero effect on parameters and outputs at the cut, and still produces a growing difference under later source-free
  updates.
- **Reading.** A boundary that resets or checks only parameters and outputs can pass content forward in optimizer state.

**The clock each mechanism uses (where stated).**
- **Wall-clock age:** FadeMem (days). CAPTURE models the user in continuous time.
- **Interaction or round count:** DynaTrust (per interaction), StateGuard (per round), EVAF (writes per 200 events).
- **Optimizer steps:** early stopping in Overtrained, Not Misaligned; the KL schedule in liminal training (by epoch).
- **Not stated as a clock:** SMSR, CURATOR, MutMem, Nous and MemSentry key on share, budget, interval or trust, not time.
- **Evidence that the choice of clock matters:**
  - The deadlines paper (2601.13206) finds near-perfect closure under turn limits and fragile behaviour under wall-clock
    limits, in the same models.
  - Sleeper Agents, Sleeper Cell and Future Events use the model's own sense of the date as the trigger.
  - Sleeper channels (2605.13471) fire through cron or systemd timers with no agent step at all.
  - EvasionBench (2609.30217) shows a monitor whose window is a history length can be outwaited by repeated attempts.

**For the repository's mapping (Inference).** This check found no source that does any of the following four things. Each
statement means only that it was not found in the rows read today.
- **Bounded influence of the settled past.** None bounds the stored past's influence by a quantity computed from the past
  itself. The nearest are SMSR's k-of-m share and MutMem's fixed interval; both are externally set constants.
- **An age weight on the system's own clock.** None keys an age weight to the system's own step count rather than wall time.
  DynaTrust and StateGuard count interactions, but for trust and audit cadence, not for decay.
- **An update boundary with no content.** None requires the boundary to carry no content. The optimizer-state paper shows
  that a parameter-level boundary can carry content invisibly. The rollback and SkillJack papers show that derived state
  outlives deletion.
- **A no-memory baseline as the safety reference.** None treats the no-memory baseline as a fixed reference that the system
  returns to. Only the Memory Trust Gap measures harm relative to "no memory".

These are gaps in what was read, not claims of novelty. Novelty is judged only under the synthesis-class expert protocol.

---

**Counts.**
- **Sources.** 55 distinct sources in 55 table rows: 27 [F], 28 [A], 0 [S], 0 [title]. 48 are NEW to the repository and 7 are
  re-verified (R).
- **By year of first arXiv version:** 2024: 5; 2025: 11; 2026: 39. Of the 2026 sources, 30 first appeared from May 2026
  onward. Six sources first posted in 2025 have 2026 versions: MINJA v5, Betley et al. v7, Misevolve v2, the crosscoder
  paper v4, the narrow-finetuning traces paper v3 and the adaptation survey v3.
- **Quote check.** A script (`lit0925/deploysafety/check_quotes.py` in the session scratchpad) checked every quoted string
  in the four topic tables and the bottleneck table against the saved fetched text on the day.
  - [F] rows were checked against the full text, and [A] rows against the abstract page.
  - A quote marked "(abs.)" inside an [F] row is from that paper's abstract page, whose wording differs from its HTML
    abstract, and was checked against the abstract page. There are four such quotes.
  - Whitespace was normalised, and curly and straight apostrophes were treated as the same character.
  - **Result: 158 quoted strings in 74 table rows, 158 found, 0 missing.**

**Limits of this check.**
- arXiv search covers titles and abstracts. Google Scholar, OpenReview, ACM DL and the lab blogs were not queried today.
  openai.com returned 403, so OpenAI's posts on GPT-4o sycophancy were not read.
- Many 2026 memory-security papers are single-author preprints with no stated venue. Several describe designs whose
  empirical evaluation is still to come (sleeper channels: "preregistered as follow-on"; bounded occupancy: "not yet built
  or evaluated").
- Most topic-2 and topic-3 rows are abstract-level [A]. The rows that describe how a defence sets influence (§1 and the
  section above) were read in full.
