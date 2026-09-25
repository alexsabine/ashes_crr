# Citations checked on the day (R10): continual learning for large language models and agents, approaches and stated bottlenecks, 2026-09-25

Scope: a dated literature check of the 2025–2026 frontier of continual learning (CL) for large language models (LLMs) and
LLM agents. It covers the approaches being proposed, the bottlenecks their authors state, and the quantity each approach
uses to decide when, and how much, the past is kept. It adds to, and does not repeat, four dossiers:
`frontier_cl_2026-09-23.md` (lab leaders' statements, mostly [S]), `frontier_plasticity_2026-09-25.md`,
`frontier_cl_safety_2026-09-25.md` and `pareto_equanimity_2026-09-25.md`. Four sources that were [S] in
`frontier_cl_2026-09-23.md` are re-read here at [A] or [F]: Lin et al. (sparse memory finetuning), Behrouz et al.
(Nested Learning; "Language Models Need Sleep") and Continual Learning Bench. RL's Razor is re-verified because §1 leans on it.
Nothing here is a result or a ledger row (R8). Every reading of a source against the repository is labelled **Inference**.

**Fetch date and method.** Every source was fetched on **2026-09-25 (UTC)**, between 02:24 and 02:31 UTC, in this session,
through the session proxy.
- arXiv abstract pages: `curl -s https://arxiv.org/abs/<id>`. The title on the page was checked against the id before the
  source was used, and the version list and dates were read from the "Submission history" block. 61 abstract pages were
  fetched and all titles matched; 50 are used below.
- arXiv full text: `https://arxiv.org/html/<id>vN` (the current version named in the table), converted to text with a
  stdlib HTML parser. LaTeX `alttext` was kept inline, so a few quotes show a LaTeX fragment. 20 full texts were fetched.
- arXiv search listings (`https://arxiv.org/search/?query=...&searchtype=all&order=-announced_date_first`) were used for
  discovery.
- One blog page (letta.com) was fetched with curl and converted the same way.
- WebSearch was used twice for discovery only. No quote below rests on a search rendering.

Raw pages and extracted text are kept in the session scratchpad (`lit0925/llmcl/{abs,html,search,other}`). They are not
committed. Quotes are copied from those files; whitespace was normalised, nothing else was changed. The quote check at the
end of this file was run against the same files.

**Access, stated once.**
- **Loaded (HTTP 200).** arxiv.org abstract pages (61), arxiv.org/html full texts (20; every requested version had an HTML
  rendering), arxiv.org/search listings, and www.letta.com (one blog page).
- **Not used.** `export.arxiv.org` was not called (it returned 406 on 2026-09-24). OpenReview, conference proceedings pages
  and lab blogs other than Letta were not needed and were not fetched.
- **No 404s. Nothing blocked** among the pages requested today.
- **Searched for and not found.** An arXiv listing search for "stability gap" with "language model" returned no 2026 LLM
  paper on the stability gap. A WebSearch rendering pointed only to the 2024 paper (arXiv 2406.14833, already in
  `frontier_plasticity_2026-09-25.md`) and to 2025 work. The stability gap therefore appears below only as stated
  indirectly (acquisition and forgetting coupled; representation or capability collapse), not as a 2026 row.

**Tags.**
- **[F]**: the arXiv HTML full text (or the blog page) was read and the quote copied from it.
- **[A]**: the arXiv abstract page was read and the quote copied from its abstract.
- **[S]**: a search-engine rendering only; unverified. None is used for a quote here.
- **[title]**: the title was seen, not the content.

Version and date are those on the arXiv abstract page today. `vN, date` is the current version; v1's date is given where
the paper was first posted in an earlier year.

---

## 1. Parametric continual learning for LLMs

### 1a. Sparse or localised updates, memory layers, fast weights, self-editing

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Lin, Zettlemoyer, Ghosh, Yih, Markosyan, Berges, Oğuz, "Continual Learning via Sparse Memory Finetuning" (Meta FAIR) | v1, 16 Oct 2025 (only version) | https://arxiv.org/abs/2510.15103 | "By updating only the memory slots that are highly activated by a new piece of knowledge relative to usage on pretraining data, we reduce interference between new knowledge and the model's existing capabilities." / "while NaturalQuestions F1 drops by 89% after full finetuning on new facts and 71% with LoRA, sparse memory finetuning yields only an 11% drop with the same level of new knowledge acquisition" | [A] |
| same | same | https://arxiv.org/html/2510.15103v1 | "We use TF-IDF as a ranking score, identifying a set of indices to update with each gradient step that minimally interferes with the model’s existing knowledge." / "this strategy is data-inefficient and not scalable as we grow the amount of experience" (on replay) | [F] |
| Goyal, Kanchi, Shah, Gupta, "Improving Sparse Memory Finetuning" | v1, 6 Apr 2026 | https://arxiv.org/abs/2604.05248 | "a theoretically grounded slot-selection mechanism based on Kullback-Leibler (KL) divergence" | [A] |
| Behrouz, Zhong, Mirrokni, "Titans: Learning to Memorize at Test Time" (Google) | v1, 31 Dec 2024 (only version) | https://arxiv.org/html/2501.00663v1 | "we design this memory module so an event that violates the expectations (being surprising) is more memorable" / "we use an adaptive forgetting mechanism that allows the memory to forget the information that is not needed anymore, resulting in better managing the memory’s limited capacity" | [F] |
| Behrouz, Razaviyayn, Zhong, Mirrokni, "Nested Learning: The Illusion of Deep Learning Architectures" (Google; NeurIPS 2025 per the page) | v1, 31 Dec 2025 (only version) | https://arxiv.org/html/2512.24695v1 | "as its number of updates per unit of time" (Definition 2, update frequency) / "In this design, higher-frequency neurons are responsible for fast adaption but store memories/knowledge for a short period of time" / "catastrophic forgetting is a natural consequence of compression, where the limited capacity of the network forces the model to forget so that it retains capacity for new information" | [F] |
| Feng, Luo, Hua, Zhang, He, Huang, Cai, "In-Place Test-Time Training" (ICLR 2026 Oral per the page) | v1, 7 Apr 2026 | https://arxiv.org/abs/2604.06169 | "In-Place TTT treats the final projection matrix of the ubiquitous MLP blocks as its adaptable fast weights" / "combined with an efficient chunk-wise update mechanism" | [A] |
| Wang, Dang, Zhu, Wen, Fu, Chai, Lee, "Learning What to Remember: Test-Time Training via Context Distillation" | v1, 3 Aug 2026 | https://arxiv.org/abs/2608.01672 | "existing TTT methods only optimize either reconstruction or online adaptation objectives without considering the future utility of retained information" | [A] |
| Zweiger, Pari, Guo, Akyürek, Kim, Agrawal, "Self-Adapting Language Models" (SEAL) | v2, 18 Sep 2025 (v1 12 Jun 2025) | https://arxiv.org/html/2506.10943v2 | "performance on earlier tasks gradually declines as the number of edits increases, suggesting that SEAL is still susceptible to catastrophic forgetting" / "each self-edit evaluation takes approximately 30–45 seconds, introducing substantial overhead" | [F] |
| Wang, Gupta, Dong, MacLellan, "Self-Consolidating Language Models: Continual Knowledge Incorporation from Context" (SCoL) | v2, 12 May 2026 | https://arxiv.org/abs/2605.07076 | "We study continual context consolidation: writing current context into model weights while limiting interference with previously consolidated information." / "SCoL encourages the LLM to generate sparse update locations that align with layers of high Fisher information" | [A] |
| Behrouz, Hashemi, Javanmard, Mirrokni, "Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories" (Google; the page says a version was on OpenReview from September 2025) | v2, 10 Jul 2026 (v1 2 Jun 2026) | https://arxiv.org/abs/2606.03979 | "existing models lack the ability to continually learn and effectively transfer their temporal in-context knowledge to their long-term parameters" | [A] |
| same | same | https://arxiv.org/html/2606.03979v2 | "In offline consolidation phase, the model enters the sleep phase, where it stops processing new data, but uses self-generated data to consolidate the recent memories." / "Since sleep is triggered when the number of past steps is divisible by" | [F] |

### 1b. Replay, schedules and continual pretraining recipes

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Öncel, Ali, Ravanelli, Subakan, Yıldız, "Time-Incremental Continued Pretraining of LLMs: Knowledge Updates Without Catastrophic Forgetting" | v1, 20 Sep 2026 | https://arxiv.org/abs/2609.23916 | "Large language models (LLMs) drift out of date the moment their pretraining ends, yet retraining from scratch is prohibitively expensive." / "the optima for knowledge acquisition and general capability are separated by roughly an order of magnitude in learning rate" | [A] |
| same | same | https://arxiv.org/html/2609.23916v1 | "Acquisition and forgetting are always coupled." / "The disjoint-stream assumption that shaped earlier continual learning work is thus not a property that survives at web scale." | [F] |
| Atreya, Batra, Mantri, Bantug, Cowan, Khraishi, "When to Review: Spaced Repetition for Continual Pre-Training of Language Models" (SRT) | v1, 18 Aug 2026 | https://arxiv.org/abs/2608.17530 | "Existing replay methods often choose a global old/new mixture and sample uniformly, ignoring that examples differ in how quickly they are forgotten." | [A] |
| same | same | https://arxiv.org/html/2608.17530v1 | "is the current inter-review interval measured in training steps" / "Replay assumes access to historical examples, so buffers and SRT state must respect retention limits, deletion requests, and data-governance obligations." | [F] |
| Feng, Wang, Li, Chu, Kang, Liu, Wang, Yu, Wu, "FOREVER: Forgetting Curve-Inspired Memory Replay for Language Model Continual Learning" (ACL 2026 camera-ready per the page) | v2, 20 Apr 2026 (v1 7 Jan 2026) | https://arxiv.org/abs/2601.03938 | "most rely on fixed, step-based heuristics that often misalign with the model's actual learning progress, since identical training steps can result in varying degrees of parameter change" | [A] |
| same | same | https://arxiv.org/html/2601.03938v2 | "which represents the total distance the model has traveled in parameter space." / "replay should impose stronger constraints when the model is changing rapidly and remain gentle once learning stabilizes" / "Model-centric calibration consistently outperforms step-based calibration, yielding an average improvement of 1.2% in OP and 1.1% in BWT." / "they do not directly reflect task-level performance degradation or semantic forgetting" (limitations) | [F] |
| Chen, Zhu, Zhang, Chen, Huang, Xu, Wang, "On-Policy Replay for Continual Supervised Fine-Tuning" (OPR) | v1, 28 May 2026 | https://arxiv.org/abs/2605.29495 | "OPR lifts BWT to -0.65 at a 10% replay budget and to -2.29 at a 1% budget" / "the active ingredient in OPR is the on-policy distribution, not the response quality" | [A] |
| Shenfeld, Pari, Agrawal, "RL's Razor: Why Online Reinforcement Learning Forgets Less" (re-verified) | v1, 4 Sep 2025 (still the only version) | https://arxiv.org/abs/2509.04259 | "the degree of forgetting is determined by the distributional shift, measured as the KL-divergence between the fine-tuned and base policy evaluated on the new task" / "among all ways to solve a new task, RL prefers those closest in KL to the original model" | [A] |
| Meterez, Nair, Morwani, Pehlevan, Kakade, "Anytime Pretraining: Horizon-Free Learning-Rate Schedules with Weight Averaging" | v2, 25 Aug 2026 (v1 3 Feb 2026) | https://arxiv.org/abs/2602.03702 | "most existing pretraining recipes are not anytime: they rely on horizon-dependent learning rate schedules and extensive tuning under a fixed compute budget" / "weight averaging combined with simple, horizon-free step sizes offers a practical and effective anytime alternative to cosine learning rate schedules" | [A] |

### 1c. LoRA-based continual learning and model merging

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Wang et al., "Orthogonal Subspace Learning for Language Model Continual Learning" (O-LoRA; EMNLP 2023 Findings) — lineage | v1, 22 Oct 2023 | https://arxiv.org/abs/2310.14152 | "learns tasks in different (low-rank) vector subspaces that are kept orthogonal to each other in order to minimize interference" / "requires no user data storage for replay" | [A] |
| Das Biswas, Zhang, Pal, Bhargava, Roy, "ELLA: Efficient Lifelong Learning for Adapters in Large Language Models" (EACL 2026 per the page) | v2, 7 Jan 2026 | https://arxiv.org/abs/2601.02232 | "replay-based methods are impractical and privacy-violating, while strict orthogonality-based methods collapse under scale" / "penalizes alignments along their high-energy, task-specific directions, while preserving freedom in the low-energy residual subspaces" | [A] |
| Sincari, Gheorghe, Barbalau, "Muon Can Outperform Dedicated Continual Learning Methods" (CoLLAs 2026 work-in-progress track per the page) | v1, 21 Sep 2026 | https://arxiv.org/abs/2609.24678 | "One update-constraining mechanism is enough, whether it comes from the loss or from the optimizer" / "Part of the advantage usually attributed to dedicated CL methods may therefore be explained by the geometry of the optimizer's updates." | [A] |
| Qiao, Mahdavi, "Merge before Forget: A Single LoRA Continual Learning via Continual Merging" (SLAO) | v1, 28 Dec 2025 | https://arxiv.org/abs/2512.23017 | "using a time-aware scaling mechanism to balance new and old knowledge during continual merging" | [A] |
| same | same | https://arxiv.org/html/2512.23017v1 | "the scaling factor can be set to" (followed in the text by λ(i) = 1/√i, "which follows the continual merging method proposed in Tang et al. (2025)") | [F] |
| Wang et al., "Geometry Conflict: Explaining and Controlling Forgetting in LLM Continual Post-Training" (GCWM) | v1, 10 May 2026 | https://arxiv.org/abs/2605.09608 | "offer limited criteria for determining when incorporating new updates is beneficial or harmful" / "forgetting can be considered as a state-relative update-integration failure" | [A] |
| Fallah, Naihin, Widawsky, Mao, "CLaaS: Continual learning as a service for sample efficient online learning" | v1, 4 Jun 2026 | https://arxiv.org/abs/2606.05559 | "agent actions and environmental transitions can only be sampled once per scenario, as real-world environments cannot be trivially reset" / "parametric updates lead to superior forward transfer and less forgetting than in-context learning, with replay being a critical choice for sample efficiency" | [A] |

---

## 2. Non-parametric and memory continual learning for agents

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Packer, Wooders, Lin, Fang, Patil, Stoica, Gonzalez, "MemGPT: Towards LLMs as Operating Systems" — lineage | v2, 12 Feb 2024 (v1 12 Oct 2023) | https://arxiv.org/abs/2310.08560 | "a system that intelligently manages different memory tiers in order to effectively provide extended context within the LLM's limited context window" | [A] |
| Lin, Snell, Wang, Packer, Wooders, Stoica, Gonzalez, "Sleep-time Compute: Beyond Inference Scaling at Test-time" (Letta / Berkeley) | v1, 17 Apr 2025 (only version) | https://arxiv.org/abs/2504.13171 | "by anticipating what queries users might ask and pre-computing useful quantities, we can significantly reduce the compute requirements at test-time" / "finding the predictability of the user query to be well correlated with the efficacy of sleep-time compute" | [A] |
| Letta, "Continual Learning in Token Space" (blog) | dated on the page "DEC 11, 2025" | https://www.letta.com/blog/continual-learning/ | "updates to learned context, not weights, should be the primary mechanism for LLM agents to learn from experience." / "how to weigh recent information against older knowledge" / "whose data do you learn from when you have millions of users?" / "agents could process and restructure learned context between active sessions" | [F] |
| Zhang et al., "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models" (ACE; ICLR 2026 per the page) | v3, 29 Mar 2026 (v1 6 Oct 2025) | https://arxiv.org/abs/2510.04618 | "context collapse, where iterative rewriting erodes details over time" | [A] |
| Li, Lin, Deng, Zhang, He, Ji, Cao, Hooi, "Just-In-Time Reinforcement Learning: Continual Learning in LLM Agents Without Gradient Updates" (JitRL) | v3, 8 Jun 2026 (v1 26 Jan 2026) | https://arxiv.org/abs/2601.18510 | "JitRL maintains a dynamic, non-parametric memory of experiences and retrieves relevant trajectories to estimate action advantages on-the-fly." / "this additive update rule is the exact closed-form solution to the KL-constrained policy optimization objective" | [A] |
| Tablan, Taylor, Bernhem, "Learning on the Job: Continual Learning from Deployment Feedback for Frozen-Weights Agents" | v1, 24 Jul 2026 | https://arxiv.org/abs/2607.22157 | "the underlying models are frozen at deployment, so an agent that resolves a difficult request today starts from zero when it recurs tomorrow" | [A] |
| same | same | https://arxiv.org/html/2607.22157v1 | "All writes happen after the episode ends, in a dedicated reflection turn carried out by the same agent with the feedback in hand" / "writes attempted mid-conversation are acknowledged but not committed, which prevents the store from being poisoned by confident mistakes" | [F] |
| Xia et al., "MetaClaw: Just Talk -- An Agent That Meta-Learns and Evolves in the Wild" | v1, 17 Mar 2026 | https://arxiv.org/html/2603.17187v1 | "a background daemon that defers policy optimization to periods when the user is not actively interacting with the agent" / "The user configures a sleep schedule (e.g., 23:00–07:00)." / "training is initiated only after the query buffer" | [F] |
| Li et al., "Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation" | v2, 31 Aug 2026 (v1 23 Aug 2026) | https://arxiv.org/abs/2608.22215 | "Existing memory systems typically treat external memory as a monotonically growing repository, inevitably leading to retrieval degradation and increasing computational costs over time." | [A] |
| same | same | https://arxiv.org/html/2608.22215v2 | "Retained external memories are periodically internalized via supervised fine-tuning (Slow Consolidation)." / "A fact is removed from external memory only if consolidation is validated" / "lacks a principled mechanism to resolve temporally conflicting updates accumulated between cycles" | [F] |
| Kang et al., "Retain or Consolidate? Budget-Dependent Operator Selection for Language Agent Memory" | v2, 21 Jul 2026 | https://arxiv.org/abs/2607.17545 | "when should consolidation replace retention" / "consolidation improves absolute accuracy by up to 48% under tight budgets, whereas retention is preferable under loose budgets" | [A] |
| Chen et al., "Rethinking Continual Experience Internalization for Self-Evolving LLM Agents" | v1, 3 Jun 2026 | https://arxiv.org/abs/2606.04703 | "under multi-iteration experience learning, existing methods suffer from a progressive capability collapse rather than compounding improvement" | [A] |
| Li, Ding, Hu, "Understanding Generalization and Forgetting in In-Context Continual Learning" (ICML 2026 per the page) | v1, 27 May 2026 | https://arxiv.org/abs/2605.28705 | "standard attention mechanisms inevitably induce intertask interference by uniformly or causally aggregating historical contexts" | [A] |
| Li, Li, "What Should an Agent Forget? Separating What Is Stored from What Is Used" (RD-Forget) | v1, 9 Sep 2026 | https://arxiv.org/abs/2609.10263 | "A superseded fact can mislead a current-state answer and still be essential for a historical query." | [A] |
| Kyrkewood, "The Sleeping Agent: What Gist-Based Context Compression Loses and Why" | v1, 12 Aug 2026 | https://arxiv.org/abs/2608.11775 | "the gist abstraction prompt preserves relational and event structure while discarding dates and times" | [A] |
| Fan, Liu, Yang, Ouyang, Han, "Can Agent Memory Systems Track Evolving State?" (StateMemBench) | v1, 20 Aug 2026 | https://arxiv.org/abs/2608.19652 | "an effective memory system must track the evolving state of the world" | [A] |
| Zhan, Zhang, Guo, Zhao, Liu, "When Memory Becomes Authority: Benchmarking Authority Collapse at the Memory Consolidation Boundary" | v2, 4 Aug 2026 | https://arxiv.org/abs/2608.01679 | "consolidation also imposes an implicit authorization boundary" / "we observe authority collapse in 48 of 49 evaluated configurations" | [A] |
| Chen et al., "MemSecBench: Tracking Agent Memory Poisoning from Persistence to Consequence and Repair" | v1, 29 Jul 2026 | https://arxiv.org/abs/2607.27080 | "malicious memory persists in 84.2% of all cases, and the full Write--Execute chain succeeds in 50.3%" | [A] |
| Al-Tawaha, Gu, Niu, Jia, Jin, "Remembering More, Risking More: Longitudinal Safety Risks in Memory-Equipped LLM Agents" | v1, 18 May 2026 | https://arxiv.org/abs/2605.17830 | "memory-induced violation rates show a robust upward trend with exposure length on both agent classes" / "treating memory safety as a longitudinal property" | [A] |

---

## 3. Evaluation, benchmarks, time and deployment constraints

| work | version and date | URL | quote (verbatim from fetched text) | tag |
|---|---|---|---|---|
| Asawa et al. (incl. Zaharia, Gonzalez), "Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments" (CL-Bench) | v1, 4 Jun 2026 | https://arxiv.org/abs/2606.05661 | "no high-quality benchmark exists to evaluate it" | [A] |
| same | same | https://arxiv.org/html/2606.05661v1 | "Accumulated state frequently hurts rather than helps: memory modules introduce spurious generalizations and stale beliefs, while more expensive systems fail to translate cost into performance." | [F] |
| Shu, Jiménez Gutiérrez, Jonnalagedda, Yao, Sun, Su, "AgentCL: Toward Rigorous Evaluation of Continual Learning in Language Agents" | v2, 2 Jun 2026 | https://arxiv.org/abs/2606.02461 | "naive and held-out settings often yield limited gains and can expose memory-induced degradation" | [A] |
| Cheng et al., "AhaBench: Do Agents Turn Experience into Reusable Insights? A Long-Horizon Benchmark for Continual Learning" | v2, 21 Sep 2026 (v1 30 Jun 2026) | https://arxiv.org/abs/2609.05435 | "using explicit guidance is more reliable than generalizing beyond it or sustaining useful behavior" | [A] |
| Wang, Kattakinda, Feizi, "Do Agent Optimizers Compound? A Continual-Learning Evaluation on Terminal-Bench 2.0" | v1, 15 Jul 2026 | https://arxiv.org/abs/2607.14004 | "optimization gains compounded only when regression control was built into the optimization loop" | [A] |
| Harrington et al. (incl. Darrell, Malik, Bai), "When Does Continual Learning Require Learning" | v1, 8 Jul 2026 | https://arxiv.org/abs/2607.07847 | "Distillation-based methods accumulate knowledge stably but struggle to update outdated facts." / "continual learning is not a single capability" | [A] |
| same | same | https://arxiv.org/html/2607.07847v1 | "Avoiding catastrophic forgetting is necessary, but so is knowing when and how to update." | [F] |
| Shihab, Akter, Sharma, "Continual Calibration: Coverage Can Collapse Before Accuracy in Lifelong LLM Fine-Tuning" | v1, 27 Apr 2026 | https://arxiv.org/abs/2604.23987 | "uncertainty reliability can degrade earlier and more sharply than top-1 performance" | [A] |
| Dong et al., "Is One Score Enough? Rethinking the Evaluation of Sequentially Evolving LLM Memory" (SeqMem-Eval) | v1, 14 May 2026 | https://arxiv.org/abs/2605.15384 | "higher final or cumulative accuracy does not necessarily imply better memory quality" | [A] |
| Guan et al., "ContinualSkillBench: Can LLM Agents Truly Evolve Their Capabilities?" | v1, 4 Aug 2026 | https://arxiv.org/abs/2608.03874 | "still struggle to consistently consolidate experience into robust and transferable skills" | [A] |
| Murtaza, Nie, Soni, Wen, Frydenlund, "When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents" (EMNLP 2026 Industry per the page) | v1, 9 Sep 2026 | https://arxiv.org/abs/2609.10750 | "the synthetic-data fine-tuning improves in-distribution retrieval but it causes catastrophic forgetting on real and out-of-distribution (OOD) data" | [A] |
| Pilchen, Fabre, Signe Talla, Perez, Grave, "Understanding Data Temporality Impact on Large Language Models Pre-training" | v2, 25 May 2026 | https://arxiv.org/abs/2605.22769 | "Large language models (LLMs) are typically trained on shuffled corpora, yielding models whose knowledge is frozen at train time" / "Temporally ordered pre-training yields improved factual freshness" | [A] |
| Jiang et al., "LLM Evolution as an Industry-Scale Ecosystem: A Lifecycle Perspective on Continual Learning" (survey) | v1, 12 Jun 2026 | https://arxiv.org/abs/2606.24901 | "repeated adaptation erodes model plasticity, foundation-model upgrades break capability inheritance, and long-term sustainability is constrained by deployment requirements" | [A] |
| Chakraborty, Das, Shah, Gupta, Gary, "TIMEGATE: Sustainable Time-Boxed Promotion Gates for Continual ML Adaptation Under Resource Constraints" | v2, 31 May 2026 | https://arxiv.org/abs/2605.29183 | "each re-training cycle uses compute, annotation, and energy" | [A] |
| same | same | https://arxiv.org/html/2605.29183v2 | "bounds wall-clock time for labeling, training, and evaluation in cycle" | [F] |
| Shihab, Al Ahsan, Sharma, "Canonicalized Stable-List Replay for Private Federated Continual Learning over Language-Model Embeddings" | v1, 29 May 2026 | https://arxiv.org/abs/2606.00426 | "Under user-level differential privacy (DP), replay-based continual learning faces a structural obstacle" | [A] |

**Counts.** 51 distinct sources: 50 arXiv papers (RL's Razor, re-verified, among them) and 1 blog page. By tag of the
strongest quote: [F] 16 sources (15 arXiv full texts plus the Letta page); [A] 35; [S] 0; [title] 0. By year of first
posting: 2023: 2 (O-LoRA, MemGPT); 2024: 1 (Titans, 31 Dec 2024); 2025: 8 (sleep-time compute, SEAL, RL's Razor, ACE,
sparse memory finetuning, SLAO, Nested Learning, the Letta blog); 2026: 40. The count exceeds the 25–40 aimed for because
the 2026 agent-memory and evaluation literature is large; every row was fetched and read today.

---

## 4. Stated bottlenecks, 2026

Each row is a bottleneck as stated by the source, in its words. Sources first posted before 2026 are marked (2025).

| bottleneck | who states it | quote | tag |
|---|---|---|---|
| Catastrophic forgetting remains under every weight-update route | SEAL (2025) | "performance on earlier tasks gradually declines as the number of edits increases, suggesting that SEAL is still susceptible to catastrophic forgetting" | [F] |
| same, framed as a capacity limit | Nested Learning (2025) | "catastrophic forgetting is a natural consequence of compression, where the limited capacity of the network forces the model to forget so that it retains capacity for new information" | [F] |
| Acquisition and forgetting cannot be separated by a learning-rate choice | Öncel et al. 2609.23916 | "Acquisition and forgetting are always coupled." | [F] |
| Collapse under repeated self-improvement (a plasticity / compounding failure) | Chen et al. 2606.04703 | "under multi-iteration experience learning, existing methods suffer from a progressive capability collapse rather than compounding improvement" | [A] |
| same, at industrial scale | Jiang et al. 2606.24901 | "repeated adaptation erodes model plasticity, foundation-model upgrades break capability inheritance, and long-term sustainability is constrained by deployment requirements" | [A] |
| Gains do not compound without regression control | Wang, Kattakinda, Feizi 2607.14004 | "optimization gains compounded only when regression control was built into the optimization loop" | [A] |
| No trustworthy benchmark; dedicated memory does not beat plain in-context learning | CL-Bench 2606.05661 | "no high-quality benchmark exists to evaluate it" / "Accumulated state frequently hurts rather than helps: memory modules introduce spurious generalizations and stale beliefs, while more expensive systems fail to translate cost into performance." | [A] / [F] |
| Aggregate scores hide forgetting | SeqMem-Eval 2605.15384 | "higher final or cumulative accuracy does not necessarily imply better memory quality" | [A] |
| Accuracy retention hides a loss of calibration | Shihab, Akter, Sharma 2604.23987 | "uncertainty reliability can degrade earlier and more sharply than top-1 performance" | [A] |
| Benchmarks built on naive streams cannot tell memory designs apart | AgentCL 2606.02461 | "naive and held-out settings often yield limited gains and can expose memory-induced degradation" | [A] |
| When to update weights, and how (the consolidation decision) | Harrington et al. 2607.07847 | "Avoiding catastrophic forgetting is necessary, but so is knowing when and how to update." | [F] |
| same, as a missing criterion | Wang et al. 2605.09608 | "offer limited criteria for determining when incorporating new updates is beneficial or harmful" | [A] |
| same, for agent memory | Kang et al. 2607.17545 | "when should consolidation replace retention" | [A] |
| How to weigh recent against old (the weight on the past) | Letta (2025) | "how to weigh recent information against older knowledge" | [F] |
| Stale facts and updates in time | Öncel et al. 2609.23916 | "Large language models (LLMs) drift out of date the moment their pretraining ends, yet retraining from scratch is prohibitively expensive." | [A] |
| same | Harrington et al. 2607.07847 | "Distillation-based methods accumulate knowledge stably but struggle to update outdated facts." | [A] |
| same, in agent memory | StateMemBench 2608.19652; RD-Forget 2609.10263 | "an effective memory system must track the evolving state of the world" / "A superseded fact can mislead a current-state answer and still be essential for a historical query." | [A] |
| Compression loses time stamps | Kyrkewood 2608.11775 | "the gist abstraction prompt preserves relational and event structure while discarding dates and times" | [A] |
| Consolidation leaves conflicts accumulated between cycles unresolved | Li et al. 2608.22215 | "lacks a principled mechanism to resolve temporally conflicting updates accumulated between cycles" | [F] |
| Memory growth | Li et al. 2608.22215 | "Existing memory systems typically treat external memory as a monotonically growing repository, inevitably leading to retrieval degradation and increasing computational costs over time." | [A] |
| Context collapse under repeated rewriting | ACE (v1 2025; v3 2026) | "context collapse, where iterative rewriting erodes details over time" | [A] |
| In-context CL has its own interference | Li, Ding, Hu 2605.28705 | "standard attention mechanisms inevitably induce intertask interference by uniformly or causally aggregating historical contexts" | [A] |
| Memory poisoning persists | MemSecBench 2607.27080 | "malicious memory persists in 84.2% of all cases, and the full Write--Execute chain succeeds in 50.3%" | [A] |
| Consolidation erases provenance and authority | Zhan et al. 2608.01679 | "we observe authority collapse in 48 of 49 evaluated configurations" | [A] |
| Risk grows with accumulated memory | Al-Tawaha et al. 2605.17830 | "memory-induced violation rates show a robust upward trend with exposure length on both agent classes" | [A] |
| Replay cost and scalability | Lin et al. (2025) | "this strategy is data-inefficient and not scalable as we grow the amount of experience" | [F] |
| Cost of a weight-update loop | SEAL (2025) | "each self-edit evaluation takes approximately 30–45 seconds, introducing substantial overhead" | [F] |
| Cost of each retraining cycle | TIMEGATE 2605.29183 | "each re-training cycle uses compute, annotation, and energy" | [A] |
| Privacy, retention and licensing limits on replay | SRT 2608.17530 | "Replay assumes access to historical examples, so buffers and SRT state must respect retention limits, deletion requests, and data-governance obligations." | [F] |
| same | ELLA 2601.02232 | "replay-based methods are impractical and privacy-violating, while strict orthogonality-based methods collapse under scale" | [A] |
| same, under differential privacy | CSLR 2606.00426 | "Under user-level differential privacy (DP), replay-based continual learning faces a structural obstacle" | [A] |
| same, across users | Letta (2025) | "whose data do you learn from when you have millions of users?" | [F] |
| No reset: the world is sampled once | CLaaS 2606.05559 | "agent actions and environmental transitions can only be sampled once per scenario, as real-world environments cannot be trivially reset" | [A] |
| Horizon-dependent schedules do not fit open-ended training | Meterez et al. 2602.03702 | "most existing pretraining recipes are not anytime: they rely on horizon-dependent learning rate schedules and extensive tuning under a fixed compute budget" | [A] |
| Step counts are the wrong clock for replay | FOREVER 2601.03938 | "most rely on fixed, step-based heuristics that often misalign with the model's actual learning progress, since identical training steps can result in varying degrees of parameter change" | [A] |

**Not found as a 2026 statement today:** the stability gap for LLMs (see the access note). The nearest 2026 statements
are the acquisition–forgetting coupling (2609.23916) and the collapse under repeated internalization (2606.04703).

---

## 5. Where the approaches set a schedule, a weight or a boundary (inference, labelled as such)

**Inference.** This section reads each approach for the quantity that decides **when** the past is revisited or
consolidated, and **how much** weight the past carries. The quantities are taken from the texts quoted above. The
classification is this repository's reading, not the authors'. The column "clock" records what time is measured in:
the model's own steps, the model's own movement, experience or episode count, or wall-clock / user time.

| approach | when (schedule or boundary) | how much (weight on the past) | clock | kind |
|---|---|---|---|---|
| Sparse memory finetuning (2510.15103; 2604.05248) | every gradient step | only the top-t memory slots ranked by TF-IDF against a background corpus are updated; the variant ranks by a KL "surprise" score | own steps | **gate** (which parameters may move); no replay |
| Titans (2501.00663) | every token / chunk | gate α_t ∈ [0,1] decides how much is forgotten; surprise decay η_t is data-dependent | own tokens | **learned** decay |
| Nested Learning / Hope, CMS (2512.24695) | block ℓ is updated every C^(ℓ) steps; frequency = "number of updates per unit of time" | a spectrum of fixed update frequencies; slow blocks keep what fast blocks forget | own steps | **fixed schedule** by level |
| Language Models Need Sleep (2606.03979) | "sleep is triggered when the number of past steps is divisible by" the block's chunk size; offline phase stops processing new data | distillation into added capacity plus self-generated rehearsal | own steps; **discrete boundary** | fixed schedule + boundary |
| In-Place TTT; TTCD (2604.06169; 2608.01672) | chunk-wise fast-weight update at inference | fast weights overwrite within the context; TTCD adds a teacher signal for future utility | own tokens | fixed chunk schedule |
| SEAL (2506.10943) | per new input (self-edit), RL-trained | the self-edit may specify hyperparameters; no retention term, and forgetting is measured | experience count | **learned** (by the model) |
| SCoL (2605.07076) | per context in the stream | model chooses which layers to update; chosen layers align with high-Fisher layers | experience count | **learned gate** |
| RL's Razor; OPR (2509.04259; 2605.29495) | continuous (RL); OPR replays at each stage | implicit KL-to-base minimisation (RL); OPR uses a fixed replay budget (1 % or 10 %) of on-policy samples | own steps | implicit (RL) / **replay ratio** (OPR) |
| Time-incremental CPT (2609.23916) | per new crawl snapshot | learning rate, with acquisition and general-capability optima an order of magnitude apart; replay is implicit through URL overlap | data snapshots (calendar-dated) | **fixed LR**, implicit replay |
| SRT spaced repetition (2608.17530) | per-example due step; interval "measured in training steps", grown by the SM-2 ease factor from a perplexity-derived recall score | old-exposure fraction ρ of each batch (fixed cap); which old items is scheduled | own steps | **replay ratio** + per-item schedule |
| FOREVER (2601.03938) | replay fires when accumulated update magnitude τ_t = Σ‖Θ_t − Θ_{t−1}‖₂ crosses Ebbinghaus-spaced thresholds, calibrated as virtual model days on the first S steps | regulariser weight β_t = β_base · clip(1 + γ(r_t − 1)), with r_t the ratio of an EMA of recent update size to the warm-up mean | **model's own movement** (Euclidean arc in parameter space, reset per task) | schedule by arc + **clipped ratio weight** |
| Anytime pretraining (2602.03702) | no horizon: constant or 1/√t step size with weight averaging | the averaging weight on past iterates | own steps | fixed decay |
| O-LoRA; ELLA; Muon IncLoRA (2310.14152; 2601.02232; 2609.24678) | per task boundary | a subspace constraint: strict orthogonality (O-LoRA), an anisotropic penalty on high-energy past directions (ELLA), or the optimiser's orthogonalised update alone (Muon) | task count; **discrete boundary** | **fixed penalty weight** or constraint |
| SLAO merging (2512.23017) | at each task boundary | merge coefficient λ(i) = 1/√i on the new task's update | task count | **fixed decay** in task index |
| GCWM (2605.09608) | at each update integration | a geometry-conflict score gates the correction | task count | **gate** |
| CLaaS (2606.05559) | asynchronous training on an experience replay buffer | replay reuse of gradients | experience count | replay |
| MemGPT; sleep-time compute; Letta token-space CL (2310.08560; 2504.13171; blog) | data moved between memory tiers; offline sleep-time processing before queries arrive (paper) or between active sessions (blog) | what is kept in context is chosen by the agent | context size; **between sessions** | learned (by prompt) |
| ACE (2510.04618) | per execution, incremental updates to a playbook | structured, incremental context edits instead of rewrites | experience count | rule-based |
| JitRL (2601.18510) | per decision, no weight update | retrieved advantages added to logits; closed form of a KL-constrained objective | experience count | KL-regularised weight |
| Learning on the Job (2607.22157) | "All writes happen after the episode ends"; mid-episode writes are not committed | one WHEN–THEN rule per episode; verified rules never weakened | **episode boundary** | discrete boundary + write contract |
| MetaClaw (2603.17187) | skills: immediately after failures; weights: only in idle windows (a user-set sleep schedule, input-idle for δ minutes, calendar meetings) and only once the buffer is large enough | buffer flushed at each skill-generation change | skills: experience count; weights: **wall-clock and user time** | wall-clock gate |
| Dual-Layer Agentic Memory (2608.22215) | periodic write-back cycles; a fact leaves external memory only when a probe check passes | router decides write / update / discard; consolidation is SFT | cycles (period not tied to the model's state) | periodic + **validation gate** |
| Retain or Consolidate (2607.17545) | when context-budget pressure is high | learned choice among merge / abstract / rewrite | token budget | **learned gate** |
| TIMEGATE (2605.29183) | each cycle has a wall-clock decision window Δτ; promotion only if the quality gate passes within it | promote or hold | **wall-clock** | time-boxed gate |

**Reading across the table (inference).**
- **Three clocks are in use.**
  - *The model's own step or token count* (Nested Learning, Sleep, SRT, TTT). This is the common default.
  - *The model's own movement.* FOREVER is the only 2026 source found that sets the replay schedule on distance travelled
    in parameter space. It argues explicitly that step counts are the wrong clock, and its ablation against step-based
    calibration is +1.2 OP / +1.1 BWT. Its distance is the Euclidean norm of LoRA updates, not a Fisher–Rao arc. It is
    reset at each task and calibrated on the first S = 24 steps.
  - *Wall-clock or user time* (MetaClaw's idle and calendar windows; TIMEGATE's decision window). This is a systems
    choice, justified by service availability and budget, not by the model's state.
- **Discrete boundaries are explicit** in several designs: episode end (Learning on the Job), sleep phases (Sleep;
  MetaClaw), task boundaries (O-LoRA, ELLA, SLAO, FOREVER's per-task reset), and write-back cycles (Dual-Layer). None of
  these sources derives the boundary from a phase of the process. Each boundary is a fixed period, a task or episode end,
  a divisibility rule on the step count, or a user-idle signal.
- **The weight on the past is mostly fixed.** It is a replay ratio (OPR's 1 % or 10 %; SRT's ρ), a merge schedule
  (SLAO's 1/√i), a penalty coefficient (ELLA), or a learning rate (time-incremental CPT). Where it adapts, it is learned
  (Titans' gates, SCoL, Retain or Consolidate), or it is **a clipped ratio of recent to baseline update size** (FOREVER's
  β_t). The last form is structurally close to the repository's bounded ratio rule EQ-B: a ratio of present to past
  magnitudes, then a clip. It differs in two ways. FOREVER's ratio is recent against warm-up update size, not present
  gradient against past gradient. And it scales a regulariser at replay time only.
- **The consolidation decision is named as open** (when to move context into weights) by 2607.07847, 2605.09608,
  2607.17545 and Letta. The implemented answers are periodic cycles, idle windows, budget pressure or a validation probe.
  No source found today sets it on accumulated information-geometric change.
- **For the repository (inference).** The nearest prior art to an arc-length clock for replay is FOREVER (ACL 2026).
  Any claim that CRR's arc clock is new for LLM replay scheduling must cite it and beat its step-based ablation baseline
  as well as FOREVER itself (R7). For consolidation at discrete boundaries, the baselines that can win are a fixed period
  (Dual-Layer, Sleep), an episode-end boundary (Learning on the Job) and a user-idle window (MetaClaw).

---

## Quote check

Run at 02:35 UTC on 2026-09-25: `scratchpad/lit0925/llmcl/check_quotes.py` (session scratchpad, not committed). The
script splits each line of this file on straight double quotes and takes every quoted string of 20 or more characters.
It checks each one, after whitespace normalisation, against the concatenated saved text of every fetched page
(61 abstract pages, 20 full texts and the Letta page).

- **Result: 194 quoted strings checked, 194 found, 0 missing.**
- With the length threshold lowered to 4 characters: 200 checked, 200 found.
- The raw files are listed with their sha256 in `scratchpad/lit0925/llmcl/MANIFEST.sha256` (185 files, including search
  listings).
- This file states no number computed by the repository. Every number in it is printed in a cited source (R1).
