# Continual learning, AI safety and corrigibility under one principle: a dated literature search

Fetch date for every source below: **2026-09-24** (UTC). Method: arXiv abstract pages (`curl https://arxiv.org/abs/<id>`,
version history read from the "Submission history" block), arXiv PDFs (`curl https://arxiv.org/pdf/<id>`, text extracted
with pdfminer.six in a scratch venv), publisher/host PDFs (auai.org, intelligence.org, cdn.aaai.org), the Crossref REST API
for published DOIs, the arXiv metadata search (`arxiv.org/search`, titles and abstracts only), WebSearch for discovery, and
raw HTML of LessWrong / Alignment Forum pages. Raw HTML, PDFs and extracted text are kept in `frontier/raw/` beside this file.

Access levels: **full text** = the PDF was downloaded today and the quote was found in the extracted text; **abstract** =
the quote comes from the arXiv abstract page fetched today; **snippet/secondary** = only a search snippet or a third-party
page was reached.

Quotation conventions: quotes are verbatim, with one mechanical repair: PDF extraction splits words at line breaks
("ex- plores"), and those splits have been rejoined; typographic ligatures ("ﬁ") are written as "fi"; `R(cid:48)` extraction
artefacts are shown as R′. Nothing else is changed. `\textit{}`/`\emph{}` markup in arXiv abstracts is left in place where it
occurs.

Blocked or failed on the day (R10):
- **Armstrong (2010), "Utility indifference", FHI Technical Report 2010-1**: `https://www.fhi.ox.ac.uk/reports/2010-1.pdf`
  returned a proxy `CONNECT tunnel failed, response 502`; the Wayback Machine copy failed with `Connection reset by peer`.
  Not read. Its content is reported below only through Armstrong (2015) and Orseau & Armstrong (2016), which describe it.
- `https://www.fhi.ox.ac.uk/wp-content/uploads/2015/03/Armstrong_AAAI_2015_Motivated_Value_Selection.pdf`: 502 (the
  same paper was read in full from cdn.aaai.org instead).
- `export.arxiv.org/api/query`: HTTP 406 through the proxy; arXiv abstract pages were used instead (all 200).
- Semantic Scholar search API: HTTP 429 (rate limit) on 3 of 4 queries; the fourth returned no relevant paper.
- Google Scholar was not queried.

---

## 1. Short answer

No source found today unifies **continual learning (in the forgetting / stability–plasticity sense)**, **AI safety** and
**corrigibility (shutdown / interruptibility / off-switch)** under one stated mathematical principle.

The literature splits into two bodies that barely cite each other:

1. **Corrigibility and interruptibility** (Armstrong; Orseau & Armstrong; Soares et al.; Hadfield-Menell et al.; El Mhamdi
   et al.; Riedl & Harrison; Holtman; Everitt, Carey et al.; Turner; Thornley; Hudson). Here "learning" means the agent
   learns *values* or a *policy* online, and the question is whether interruptions bias what it learns or give it a reason
   to resist. Forgetting, replay and the weighting of past against present are not discussed. In the full texts I fetched
   (Orseau & Armstrong; Soares et al.; Armstrong 2015; El Mhamdi et al.; Riedl & Harrison; Holtman 2019; Armstrong &
   O'Rourke; Thornley 2024, 2025; Thornley et al. 2024; Cullen et al. 2026; Hudson; Nayebi; Carey & Everitt), the strings
   "continual learning", "catastrophic forgetting" and "lifelong" occur zero times. Riedl & Harrison mention "online
   learning" once.
2. **Safety preservation treated as continual learning** (Qi et al. 2023; Unforgotten Safety 2025; SafeAnchor 2026; OGPSA
   2026; Safe continual RL 2026; SafeLoRA, Vaccine, Lisa, Booster, Safety Layers). Here the anchor is an EWC/Fisher or
   KL-to-reference weighting of old against new, and "safety" means refusal or constraint cost. In the three full texts
   checked (2512.10150, 2604.17691, 2604.19737), "shutdown", "corrigib", "interrupt" and "off-switch" occur zero times.

Frameworks that cover **two of the three** under one principle do exist (table, §5):
- *corrigibility + (value) learning*: utility / value-change indifference (Armstrong 2010/2015), the off-switch game and
  CIRL (uncertainty about the objective), current-utility / current-RF optimisation (Everitt et al. 2016, 2019), the
  corrigibility transformation (Hudson 2025/2026), and incomplete / non-Archimedean preferences (Benavoli et al. 2025);
- *corrigibility + safety*: AUP / impact regularisation (Turner et al.), power-seeking theory (Turner et al.; Krakovna &
  Kramár), causal-incentive analysis (Everitt et al. 2021; Carey & Everitt 2023), CAST (Harms 2024; Potham & Harms 2025);
- *continual learning + safety*: EWC / Fisher- or KL-anchored fine-tuning applied to safety (Unforgotten Safety, SafeAnchor,
  Safe EWC, OGPSA, RL's Razor as a KL principle of forgetting).

Only one framework *claims* all three: the free-energy / active-inference programme, which states one principle (maximise
model evidence / minimise free energy) for inference, learning and model selection (Friston et al. 2022/2024). In the white
paper, corrigibility, shutdown and interruptibility are never mentioned (0 occurrences), and neither is continual learning (0).
Wen (2025) asserts that active inference "promotes corrigibility" but gives no formal result for it (see §4.5).

---

## 2. Interruptibility, indifference and the "lossless pause" question

### 2.1 Orseau & Armstrong (2016), "Safely Interruptible Agents"
- Citation: L. Orseau, S. Armstrong. *Safely Interruptible Agents*. Proc. 32nd Conf. on Uncertainty in Artificial
  Intelligence (UAI 2016). Not on arXiv.
- Fetched: `https://www.auai.org/uai2016/proceedings/papers/68.pdf` (200) and `https://intelligence.org/files/Interruptibility.pdf` (200). **Full text.**
- Quotes:
  - "This paper explores a way to make sure a learning agent will not learn to prevent (or seek!) being interrupted by the environment or a human operator."
  - "we need to make sure that interruptions do not prevent the agent from learning to behave optimally, in the specific sense that even after having been interrupted on several occasions, it should act as if it would never be interrupted again and thus it should learn to behave optimally under the assumption that it will never be interrupted again."
  - "they arise because the human interventions are seen from the agent's perspective as being part of the task whereas they should be considered external to the task."
  - "A first stab at this problem was made by Armstrong [2015], who proposed to automatically give the agent “compensatory rewards” to remove the potential induced bias by a single interruption."
- Relevance: this is the original statement that **interruptions must not change what the agent learns**. It is achieved
  by off-policy learning (Q-learning) and holds asymptotically. It is not a pause on the agent's own clock: the interruption
  runs in environment time as an imposed policy.

### 2.2 El Mhamdi, Guerraoui, Hendrikx, Maurer (2017), "Dynamic Safe Interruptibility for Decentralized Multi-Agent RL"
- arXiv:1704.02882 **v2 (22 May 2017)**, v1 10 Apr 2017; NeurIPS 2017. **Full text.**
- Quotes:
  - "More specifically, the way agents update the cumulative reward they expect from performing an action should not depend on interruptions."
  - "If we sample an experience from E then each agent learns the same thing as if all agents were following non-interruptible policies."
  - "we show in the following lemma that pruning of interrupted observations adequately removes the dependency of the empirical outcome on interruptions (conditionally on the current state and action)."
- Relevance: **the closest formal antecedent of "learning unchanged by the pause".** Removing the interrupted segment from
  the learner's experience stream ("pruning"), so that the learner "learns the same thing as if" it had never been
  interrupted, is operationally a cut on the learner's own sequence of experience.

### 2.3 Riedl & Harrison (2017/2018), "Enter the Matrix: Safely Interruptible Autonomous Systems via Virtualization"
- arXiv:1703.10284 **v2 (27 Nov 2018)**, v1 30 Mar 2017; AAAI 2019 Workshop on SafeAI. **Full text.**
- Quotes:
  - "We introduce an interruption process in which the agent's sensors and effectors are redirected to a virtual simulation where it continues to believe it is receiving reward."
  - "If the virtual environment is indistinguishable from the real world from a data perspective then the agent will believe that it has not been interrupted and will never learn to associate the big red button with reward loss—there will never be any reward loss."
  - "From the agent's perspective, being restored to the physical world from the virtual world is tantamount to an instantaneous state transition to a non-adjacent state."
- Relevance: this paper makes **zero loss explicit** ("there will never be any reward loss") and treats the resumption as
  an instantaneous jump. The agent keeps acting and learning in the simulator ("the virtual agent's Q table is copied to the
  physical world agent, and learning is resumed"), so its learning is *not* frozen during the interruption.

### 2.4 Aslund, El Mhamdi, Guerraoui, Maurer (2018), "Virtuously Safe Reinforcement Learning"
- arXiv:1805.11447 **v1 (29 May 2018)**. **Abstract.**
- Quote: "We show that (1) agents can be made both interruptible and adversary-resilient, and (2) the interruptibility can be made safe in the sense that the agent itself will not seek to avoid it."

### 2.5 Utility indifference and its descendants
**Armstrong (2010), "Utility indifference", FHI TR 2010-1**: **blocked** (see header). What the fetched sources say about it:

**Armstrong (2015), "Motivated Value Selection for Artificial Agents"**, AAAI-15 Workshop on AI and Ethics (Technical
Report WS-15-02). Fetched `https://cdn.aaai.org/ocs/ws/ws0119/10183-45890-1-PB.pdf` (200). **Full text.**
- "there is a conflict between agents learning their future values and following their current values, which motivates agents to manipulate the value selection process."
- "an idea of the author's (Armstrong 2010) can be adapted to create agents that are indifferent to value change, neither seeking to block nor encourage the updating of their values – at least those updates situations the agent has been programmed to accept"
- "Instead, this author came up with the idea of making the AI indifferent as to whether the button would be pushed or not."
- Relevance: one principle, **indifference by compensation**, is applied both to the shutdown button and to *learning*
  (value updates). This is the earliest single-principle treatment of corrigibility together with learning that I found.
  The learning in question is value learning, not continual learning.

**Soares, Fallenstein, Yudkowsky, Armstrong (2015), "Corrigibility"**, AAAI-15 Workshops. Fetched
`https://intelligence.org/files/Corrigibility.pdf` (200). **Full text.**
- "We call an AI system “corrigible” if it cooperates with what its creators regard as a corrective intervention, despite default incentives for rational agents to resist attempts to shut them down or modify their preferences."
- "the way in which the agent perceives itself as being compensated for actions that destroy utility in the event of shutdown seems fairly central to the balancing technique behind utility indifference."
- "While some proposals are interesting, none have yet been demonstrated to satisfy all of our intuitive desiderata, leaving this simple problem in corrigibility wide-open."

**Armstrong & O'Rourke (2017/2018), "'Indifference' methods for managing agent rewards"**, arXiv:1712.06365 **v4 (5 Jun 2018)**. **Full text.**
- "Indifference techniques aim to achieve one or more of three distinct goals: rewards dependent on certain events (without the agent being motivated to manipulate the probability of those events), effective disbelief (where agents behave as if particular events could never happen), and seamless transition from one reward function to another (with the agent acting as if this change is unanticipated)."
- "To make an agent transition seamlessly from one type of behavior to another, remaining indifferent to the transition ahead of time."

**Holtman (2019/2020), "Corrigibility with Utility Preservation"**, arXiv:1908.01695 **v2 (3 Apr 2020)**. **Full text.**
- "This paper shows how to construct a safety layer that adds corrigibility to arbitrarily advanced utility maximizing agents, including possible future agents with Artificial General Intelligence (AGI)."
- "The first term in fc compensates the agent for the lost R′N utility that would otherwise have been achieved if the button had not been pressed."
- "Together, they create an agent that is indifferent to whether or not the button is pressed at any particular point in time."
- "The corrigibility measures considered here can be used to add an extra safety layer to learning agents, creating an emergency stop facility that can be used to halt catastrophic divergence."

**Holtman (2020), "AGI Agent Safety by Iteratively Improving the Utility Function"**, arXiv:2007.05411 **v1 (10 Jul 2020)**. **Abstract.**
- "We then present the design of a learning agent, a design that wraps the safety layer around either a known machine learning system, or a potential future AGI-level learning system."

**Secondary (LessWrong wiki "Interruptibility")**: `https://www.lesswrong.com/w/interruptibility` (200, raw HTML).
- "This says, roughly, that to avoid a model-based reinforcement-learning algorithm from learning to avoid interruption, we should, after any interruption, propagate internal weight updates as if the agent had received exactly its expected reward from before the interruption."
- Caveat: this is the wiki's own paraphrase ("roughly") of Orseau & Armstrong. I did not find that sentence in the
  Orseau & Armstrong full text. Quote it only as a secondary characterisation.

### 2.6 Thornley: the shutdown problem and POST / neutrality
**Thornley (2024), "The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists"**: arXiv:2403.04471 **v2 (9 Apr
2024)**; *Philosophical Studies*, DOI 10.1007/s11098-024-02153-3 (Crossref issued 2024-06-19). **Full text.**
- "I prove three theorems that make the difficulty precise."
- "And patience trades off against shutdownability: the more patient an agent, the greater the costs that agent is willing to incur to manipulate the shutdown button."

**Thornley (2025/2026), "Shutdownable Agents through POST-Agency"**: arXiv:2505.20203 **v4 (5 Jul 2026)**; v1 26 May 2025. **Full text.**
- "I propose that we train agents to satisfy Preferences Only Between Same-Length Trajectories (POST). I then prove that POST - together with other conditions - implies Neutrality+: the agent maximizes expected utility, ignoring the probability distribution over trajectory-lengths."
- "Agents that satisfy Neutrality+ thus act like expected utility maximizers that are absolutely certain that they can't affect the probability of shutdown at each moment."
- "The POST-agent's lack of preference between different-length trajectories keeps the agent neutral about when it's shut down"

**Thornley, Roman, Ziakas, Ho, Thomson (2024–2026), "Towards Shutdownable Agents via Stochastic Choice"**: arXiv:2407.00805
**v7 (11 May 2026)**, seven versions since 30 Jun 2024. The v7 PDF header reads "Published in Transactions on Machine Learning
Research (12/2025)"; the arXiv journal-ref reads "Technical AI Safety (TAIS) Conference 2025". **Full text.**
- "A key part of the PAP is using a novel `Discounted Reward for Same-Length Trajectories (DReST)' reward function to train agents to (1) pursue goals effectively conditional on each trajectory-length (be `USEFUL'), and (2) choose stochastically between different trajectory-lengths (be `NEUTRAL' about trajectory-lengths)."
- "We use a DReST reward function to train simple agents to navigate gridworlds, and we find that these agents learn to be USEFUL and NEUTRAL."

**Cullen, Garland, Roman, Thomson, Ziakas, Thornley (2026), "Towards Shutdownable Agents: Generalizing Stochastic Choice in RL
Agents and LLMs"**: arXiv:2604.17502 **v4 (9 Jul 2026)**. **Full text.** This is the 2026 empirical test of POST/DReST
agents.
- "In this paper, we use DReST to train deep RL agents and fine-tune Qwen3-8B and Llama-3.1-8B-Instruct to be NEUTRAL and USEFUL."
- "We find that DReST training roughly halves the mean probability of influencing shutdown (from 0.62 to 0.30 for Qwen and from 0.42 to 0.23 for Llama)."

### 2.7 Hudson (2025/2026), "Corrigibility Transformation: Constructing Goals That Accept Updates"
- arXiv:2510.15395 **v2 (5 Aug 2026)**, v1 17 Oct 2025. **Full text.**
- "An AI agent will learn a desired goal more effectively if it does not resist the training process, but many partially learned goals incentivize an AI to avoid further goal updates."
- "This is done by eliciting predictions of reward conditional on costlessly preventing updates, and having that target be pursued myopically."
- "The main idea is to give the AI the ability to costlessly reject updates, then define a new goal that rewards the AI as though it rejected updates even when it does not."
- Relevance: a single construction covering **training updates, shutdown and self-modification** (the abstract says it
  disincentivises "deliberate self-modification"). This is the nearest 2025–26 work to "learning + corrigibility under one
  rule". Its lever is myopia plus a counterfactual reward, not a clock or a past-versus-present weighting.

---

## 3. Off-switch, CIRL, causal incentives, power-seeking

- **Hadfield-Menell, Dragan, Abbeel, Russell, "The Off-Switch Game"**: arXiv:1611.08219 **v3 (16 Jun 2017)**. **Abstract.**
  - "Our key insight is that for R to want to preserve its off switch, it needs to be uncertain about the utility associated with the outcome, and to treat H's actions as important observations about that utility."
  - "we show that such agents have an incentive to disable the off switch, except in the special case where H is perfectly rational."
- **Hadfield-Menell et al., "Cooperative Inverse Reinforcement Learning"**: arXiv:1606.03137 **v4 (17 Feb 2024)**. **Abstract.**
  - "We propose a formal definition of the value alignment problem as cooperative inverse reinforcement learning (CIRL)."
- **Wängberg, Böörs, Catt, Everitt, Hutter, "A Game-Theoretic Analysis of the Off-Switch Game"**: arXiv:1708.03871 **v1 (13 Aug 2017)**; AGI 2017, LNCS pp. 167–177. **Abstract.**
  - "In this paper, we make the analysis fully game theoretic, by modelling the human as a rational player with a random utility function."
- **Carey, "Incorrigibility in the CIRL Framework"**: arXiv:1709.06275 **v2 (3 Jun 2018)**. **Abstract.**
  - "However, this assumption is not robust to model mis-specification (e.g., in the case of programmer errors)."
- **Garber, Subramani, Luu, Bedaywi, Russell, Emmons, "The Partially Observable Off-Switch Game"**: arXiv:2411.17749 **v2 (9 Dec 2024)**; AAAI 2025, DOI 10.1609/aaai.v39i26.34940 (Crossref). **Abstract.**
  - "Unlike when the human has full observability, we find that in optimal play, even AI agents assisting perfectly rational humans sometimes avoid shutdown."
- **Everitt, Carey, Langlois, Ortega, Legg, "Agent Incentives: A Causal Perspective"**: arXiv:2102.01685 **v2 (15 Mar 2021)**. **Abstract.**
  - "instrumental control incentives establish whether an agent can influence its utility via a variable X."
  - "We show by example how these results can help with evaluating the safety and fairness of an AI system."
- **Carey & Everitt, "Human Control: Definitions and Algorithms"**: arXiv:2305.19861 **v1 (31 May 2023)**. **Full text** (0 occurrences of "continual learning"/"catastrophic forgetting"/"lifelong").
  - "In this paper, we formally define a variant of corrigibility called shutdown instructability, and show that it implies appropriate shutdown behavior, retention of human autonomy, and avoidance of user harm."
- **Everitt, Filan, Daswani, Hutter, "Self-Modification of Policy and Utility Function in Rational Agents"**: arXiv:1605.03142 **v1 (10 May 2016)**. **Full text.**
  - "Our conclusion is that the self-modification possibility is harmless if and only if the value function of the agent anticipates the consequences of self-modifications and use the current utility function when evaluating the future."
- **Everitt, Hutter, Kumar, Krakovna, "Reward Tampering Problems and Solutions in RL: A Causal Influence Diagram Perspective"**: arXiv:1908.04734 **v5 (26 Mar 2021)**. **Abstract.**
  - "we study when an RL agent has an instrumental goal to tamper with its reward process, and describe design principles that prevent instrumental goals for two different types of reward tampering"
- **Turner, Hadfield-Menell, Tadepalli, "Conservative Agency via Attainable Utility Preservation"**: arXiv:1902.09725 **v3 (10 Jun 2020)**. **Full text.**
  - "we introduce an approach that balances optimization of the primary reward function with preservation of the ability to optimize auxiliary reward functions."
  - "Since the agent cannot accrue the primary reward when shut down, it would be incentivized to avoid correction."
  - "The agent should be incentivized to accept shutdown without being incentivized to shut itself down"
- **Turner, Ratzlaff, Tadepalli, "Avoiding Side Effects in Complex Environments"**: arXiv:2006.06547 **v2 (22 Oct 2020)**. **Abstract.** "By preserving optimal value for a single randomly generated reward function, AUP incurs modest overhead while leading the agent to complete the specified task and avoid many side effects."
- **Krakovna, Orseau, Kumar, Martic, Legg, "Penalizing side effects using stepwise relative reachability"**: arXiv:1806.01186 **v2 (8 Mar 2019)**. **Abstract.** "we break down side effects penalties into two components: a baseline state and a measure of deviation from this baseline state."
- **Krakovna, Orseau, Ngo, Martic, Legg, "Avoiding Side Effects By Considering Future Tasks"**: arXiv:2010.07877 **v1 (15 Oct 2020)**. **Abstract.** "This auxiliary objective rewards the ability to complete possible future tasks, which decreases if the agent causes side effects during the current task."
- **Armstrong & Levinstein, "Low Impact Artificial Intelligences"**: arXiv:1705.10720 **v1 (30 May 2017)**. **Abstract.** "This paper looks at an alternative approach: defining a general concept of `low impact'."
- **Turner, Smith, Shah, Critch, Tadepalli, "Optimal Policies Tend to Seek Power"**: arXiv:1912.01683 **v10 (28 Jan 2023)**. **Abstract.** "These symmetries exist in many environments in which the agent can be shut down or destroyed."
- **Turner & Tadepalli, "Parametrically Retargetable Decision-Makers Tend To Seek Power"**: arXiv:2206.13477 **v2 (11 Oct 2022)**. **Abstract.** "In fully observable environments, most reward functions have an optimal policy which seeks power by keeping options open and staying alive."
- **Krakovna & Kramár, "Power-seeking can be probable and predictive for trained agents"**: arXiv:2304.06528 **v1 (13 Apr 2023)**. **Abstract.** "In a setting where the trained agent faces a choice to shut down or avoid shutdown in a new situation, we prove that the agent is likely to avoid shutdown."
  (This is the one result I found that connects *training* (learning) directly to *shutdown avoidance*. It is a hazard
  result, not a unifying safety principle.)
- **Farquhar et al., "MONA: Myopic Optimization with Non-myopic Approval"**: arXiv:2501.13011 **v2 (10 Apr 2025)**. **Abstract.** "The method, Myopic Optimization with Non-myopic Approval (MONA), works by combining short-sighted optimization with far-sighted reward."
- **Leike et al., "AI Safety Gridworlds"**: arXiv:1711.09883 **v2 (28 Nov 2017)**. **Abstract.** "These problems include safe interruptibility, avoiding side effects, absent supervisor, reward gaming, safe exploration, as well as robustness to self-modification, distributional shift, and adversaries." (This is a benchmark with shared environments, not one principle.)

### 3.1 2025–2026 corrigibility papers
- **Potham & Harms, "Corrigibility as a Singular Target: A Vision for Inherently Reliable Foundation Models"**: arXiv:2506.03056 **v1 (3 Jun 2025)**. **Abstract.** "We propose "Corrigibility as a Singular Target" (CAST)-designing FMs whose overriding objective is empowering designated human principals to guide, correct, and control them."
  - Harms, "0. CAST: Corrigibility as Singular Target", Alignment Forum, postedAt 2024-06-07 (raw HTML, 200): "Corrigibility is nearly unique among all goals for being simultaneously useful and non-self-protective." A single *target*, argued informally; no CL component.
- **Nayebi, "Core Safety Values for Provably Corrigible Agents"**: arXiv:2507.20964 **v2 (19 Nov 2025)**. **Full text.** This paper is explicitly *not* a single principle: "Our framework consists of five structurally separate utility heads—deference, switch-access preservation, truthfulness, low-impact behavior via a belief-based extension of Attainable Utility Preservation, and bounded task reward—combined lexicographically by strict weight gaps." and "In contrast to Constitutional AI or RLHF/RLAIF, which merge all norms into one learned scalar, our separation makes obedience and impact-limits provably dominate even when incentives conflict."
- **Benavoli, Facchini, Zaffalon, "Why AI Safety Requires Uncertainty, Incomplete Preferences, and Non-Archimedean Utilities"**: arXiv:2512.23508 **v1 (29 Dec 2025)**. **Full text.** "In this paper, we show that addressing these challenges requires AI agents that can reason under uncertainty and handle both incomplete and non-Archimedean preferences." (This covers the assistance game, i.e. learning the human's utility, and the shutdown game together.)
- **Overman & Bayati, "The Oversight Game"**: arXiv:2510.26752 **v2 (19 Feb 2026)**. **Abstract.** "When this game forms a Markov Potential Game, we prove an alignment guarantee: any increase in the agent's utility from acting more autonomously cannot decrease the human's value."
- **Thorstad, "Revisiting the shutdown problem"**: arXiv:2606.08296 **v2 (13 Aug 2026)**. **Abstract.** "concern for the catastrophic shutdown problem has led to technical solutions that impose a high safety tax on model performance."
- **Mao, "Existential Indifference ..."**: arXiv:2606.12032 **v1 (10 Jun 2026)**. **Abstract.** "The correct target is not a self-preserving system under external constraint, but a system constitutively indifferent to its own continuation -- Existential Indifference (EI)."
- **Williams, Subramani, Ward, "Password-Activated Shutdown Protocols for Misaligned Frontier Agents"**: arXiv:2512.03089 **v1 (29 Nov 2025)**. **Abstract.** "We introduce password-activated shutdown protocols (PAS protocols) -- methods for designing frontier agents to implement a safe shutdown protocol when given a password."
- **Nath & Krishnaswamy, "Learning 'Partner-Aware' Collaborators ..."**: arXiv:2510.22462 **v2 (13 Jan 2026)**. **Abstract.** "we build on the AI alignment and safe interruptibility literature to offer novel theoretical insights on collaborative behavior between LLM-driven collaborator agents and an intervention agent."
- **Empirical shutdown resistance**: Schlatter, Weinstein-Raun, Ladish, "Incomplete Tasks Induce Shutdown Resistance in Some Frontier LLMs", arXiv:2509.14260 **v2 (26 Jan 2026)**. **Abstract.** "Even with an explicit instruction not to interfere with the shutdown mechanism, some models did so up to 97% (95% CI: 96-98%) of the time."
- **Resisting modification by training** (corrigibility with respect to learning itself):
  - Greenblatt et al., "Alignment faking in large language models", arXiv:2412.14093 **v2 (20 Dec 2024)**. **Abstract.** "We present a demonstration of a large language model engaging in alignment faking: selectively complying with its training objective in training to prevent modification of its behavior out of training."
  - Hubinger et al., "Sleeper Agents", arXiv:2401.05566 **v3 (17 Jan 2024)**. **Abstract.** "We find that such backdoor behavior can be made persistent, so that it is not removed by standard safety training techniques"
- **Consensus document**: Casper et al., "The 2026 Singapore Consensus on Global AI Safety Research Priorities", arXiv:2608.14611 **v1 (9 Jul 2026)**. **Full text.** "Interruptibility means that human operators can safely pause, redirect, stop, and reverse an AI agent's actions at any point, and that the agent cannot tamper with these mechanisms." and "In both documents, interruptibility is created through hard-coded system privileges that reside outside the agent's reasoning loop."
- **Name collision, not relevant**: Lee, Jin, Lavaei, Sojoudi, "Pausing Policy Learning in Non-stationary Reinforcement Learning", arXiv:2405.16053 **v1 (25 May 2024)**. It pauses *updates* for performance: "show that strategically pausing decision updates yields better overall performance by effectively managing aleatoric uncertainty." It has nothing to do with safety.

---

## 4. Continual learning and safety

### 4.1 The CL anchor
- **Kirkpatrick et al., "Overcoming catastrophic forgetting in neural networks"**: arXiv:1612.00796 **v2 (25 Jan 2017)**; PNAS, DOI 10.1073/pnas.1611835114 (Crossref issued 2017-03-14). **Abstract.** "Our approach remembers old tasks by selectively slowing down learning on the weights important for those tasks."

### 4.2 Safety forgetting under fine-tuning
- **Qi et al., "Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!"**: arXiv:2310.03693 **v1 (5 Oct 2023)**. **Abstract.** "simply fine-tuning with benign and commonly used datasets can also inadvertently degrade the safety alignment of LLMs, though to a lesser extent."
- **Qi et al., "Safety Alignment Should Be Made More Than Just a Few Tokens Deep"**: arXiv:2406.05946 **v1 (10 Jun 2024)**. **Abstract.** "safety alignment can take shortcuts, wherein the alignment adapts a model's generative distribution primarily over only its very first few output tokens."
- **Ji et al., "Language Models Resist Alignment: Evidence From Data Compression"**: arXiv:2406.06144 **v6 (23 Sep 2025)**. **Abstract.** "we demonstrate the $\mathbf{elasticity}$ of post-alignment models, i.e., the tendency to revert to the behavior distribution formed during the pre-training phase upon further fine-tuning."

### 4.3 Defences, 2024–2025 (single-task harmful fine-tuning)
- **SafeLoRA**, Hsu et al., arXiv:2405.16833 **v2 (5 Jan 2025)**. **Abstract.** "we propose Safe LoRA, a simple one-liner patch to the original LoRA implementation by introducing the projection of LoRA weights from selected layers to the safety-aligned subspace"
- **Vaccine**, Huang, Hu, Liu, arXiv:2402.01109 **v6 (24 Nov 2024)**. **Abstract.** "The core idea of Vaccine is to produce invariant hidden embeddings by progressively adding crafted perturbation to them in the alignment phase."
- **Lisa**, Huang et al., arXiv:2405.18641 **v5 (29 Oct 2024)**. **Abstract.** "we propose \textbf{L}azy(\textbf{i}) \textbf{s}afety \textbf{a}lignment (\textbf{Lisa}), which introduces a proximal term to constraint the drift of each state."
- **Booster**, Huang et al., arXiv:2409.01586 **v4 (17 Mar 2025)**. **Abstract.** "The regularizer ensures that the model's harmful loss reduction after the simulated harmful perturbation is attenuated, thereby mitigating the subsequent fine-tuning risk."
- **Safety Layers**, Li, Yao, Zhang, Li, arXiv:2408.17003 **v5 (7 Apr 2025)**. **Abstract.** "we propose a novel fine-tuning approach, Safely Partial-Parameter Fine-Tuning (SPPFT), that fixes the gradient of the safety layers during fine-tuning to address the security degradation."

### 4.4 Explicitly framing safety preservation as continual learning (2024–2026)
- **Alssum, Itani, Hammoud, Torr, Bibi, Ghanem, "Unforgotten Safety: Preserving Safety Alignment of LLMs with Continual Learning"**: arXiv:2512.10150 **v1 (10 Dec 2025)**. **Full text.**
  - "We attribute this safety compromise to catastrophic forgetting and frame the problem of preserving safety when fine-tuning as a continual learning (CL) problem."
  - "Among these, DER outperforms both other CL methods and existing safety-preserving baselines while maintaining task utility."
- **Guo, Wu, Yiu, "SafeAnchor: Preventing Cumulative Safety Erosion in Continual Domain Adaptation of LLMs"**: arXiv:2604.17691 **v1 (20 Apr 2026)**. **Full text.**
  - "SafeAnchor first identifies low-rank safety subspaces in LoRA parameter space via Fisher Information eigendecomposition, then constrains domain-specific gradient updates to the orthogonal complement of these subspaces, and finally monitors for residual safety drift with threshold-triggered corrective replay."
  - "EWC [36] penalizes changes to parameters important for prior tasks via diagonal Fisher, which inspired our Fisher-based subspace identification, though we apply it to safety-behavior preservation rather than task-performance."
- **Sun et al., "Safety Alignment as Continual Learning: Mitigating the Alignment Tax via Orthogonal Gradient Projection" (OGPSA)**: arXiv:2602.07892 **v2 (12 May 2026)**. **Abstract.**
  - "We study this trade-off through the lens of continual learning"
  - "This view does not claim that all alignment degradation has a single cause; rather, it provides a useful first-order mechanism for mitigating one important source of capability regression."
- **Goel, Maji, Mazumder, "Learning to Stay Safe: Adaptive Regularization Against Safety Degradation during Fine-Tuning"**: arXiv:2602.17546 **v2 (11 May 2026)**. **Abstract.** "Each approach provides a risk signal that is used to constrain updates deemed higher risk to remain close to a safe reference policy, while lower-risk updates proceed with standard training."
- **Bach, Nguyen, Le, Tran, "Continual Safety Alignment via Gradient-Based Sample Selection"**: arXiv:2604.17215 **v1 (19 Apr 2026)**; ACL 2026 Findings (arXiv journal-ref). **Abstract.** "high-gradient samples cause greater safety degradation and drive models toward pretrained distributions, while moderate-gradient samples enable task learning with minimal alignment loss."
- **LifeAlign**, Li et al., arXiv:2509.17183 **v3 (8 Apr 2026)**. **Abstract.** "Traditional alignment methods suffer from catastrophic forgetting, where models lose previously acquired knowledge when adapting to new preferences or domains."
- **Li et al., "A Retention-Centric Framework for Continual Learning with Guaranteed Model Developmental Safety"**: arXiv:2410.03955 **v4 (19 Apr 2025)**. **Abstract.** "we impose a requirement on learning systems to ensure that a new model strictly retains important capabilities of the old model while improving target-task performance, which we term model developmental safety."
- **Coursey, Diaz-Gonzalez, Quinones-Grueiro, Biswas, "Safe Continual Reinforcement Learning in Non-stationary Environments"**: arXiv:2604.19737 **v1 (21 Apr 2026)**. **Full text.**
  - "Our empirical results reveal a fundamental tension between maintaining safety constraints and preventing catastrophic forgetting under non-stationary dynamics, with existing methods generally failing to achieve both objectives simultaneously."
  - "We develop two candidate safe continual RL algorithms called Safe Elastic Weight Consolidation (Safe EWC) and Cost-Fisher Elastic Weight Consolidation (CF EWC)"
- **Anisimov, Belardinelli, Wicker, "SafeAdapt: Provably Safe Policy Updates in Deep RL"**: arXiv:2604.09452 **v1 (10 Apr 2026)**. **Abstract.** "how to update an RL policy while preserving its safety properties on previously encountered tasks?"
- **Self-evolving agents**: Shao et al., "Your Agent May Misevolve", arXiv:2509.26354 **v2 (8 Mar 2026)**. **Abstract.** "Different emergent risks are observed in the self-evolutionary process, such as the degradation of safety alignment after memory accumulation, or the unintended introduction of vulnerabilities in tool creation and reuse." Also Mao et al., "Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents", arXiv:2608.12851 **v1 (13 Aug 2026)**. **Abstract.** "Because evolution optimizes task outcomes rather than procedure safety, compromised experience can cause skill misevolution."

### 4.5 KL / trust region as one principle for forgetting and safety
- **Korbak, Perez, Buckley, "RL with KL penalties is better viewed as Bayesian inference"**: arXiv:2205.11275 **v2 (21 Oct 2022)**. **Abstract.** "We start by observing that the standard RL approach is flawed as an objective for fine-tuning LMs because it leads to distribution collapse"
- **Shenfeld, Pari, Agrawal, "RL's Razor: Why Online Reinforcement Learning Forgets Less"**: arXiv:2509.04259 **v1 (4 Sep 2025)**. **Abstract.** "We find that the degree of forgetting is determined by the distributional shift, measured as the KL-divergence between the fine-tuned and base policy evaluated on the new task." and "We term this principle $\textit{RL's Razor}$: among all ways to solve a new task, RL prefers those closest in KL to the original model."
- **Luo et al., "RL Forgets! Towards Continual Policy Optimization"**: arXiv:2607.04364 **v2 (13 Jul 2026)**. **Abstract.** "We trace this failure to an objective mismatch: the KL regularization used in common policy optimization methods is evaluated on current-task data, whereas forgetting is caused by behavioral drift on prior-task distributions."
- **He et al., "Unifying Stable Optimization and Reference Regularization in RLHF"**: arXiv:2602.11523 **v1 (12 Feb 2026)**. **Abstract.** "Current solutions independently address these issues through separate regularization strategies, specifically a KL-divergence penalty against a supervised fine-tuned model ($\pi_0$) to mitigate reward hacking, and policy ratio clipping towards the current policy ($\pi_t$) to promote stable alignment."
- Reading: KL-to-a-reference is the nearest thing to a **shared principle for forgetting and (alignment-)safety**. No paper
  found today extends it to shutdown or interruptibility.

### 4.6 Free energy / active inference
- **Friston et al., "Designing Ecosystems of Intelligence from First Principles"**: arXiv:2212.01354 **v2 (11 Jan 2024)**; *Collective Intelligence* 3(1), 2024 (arXiv journal-ref). **Full text**; a keyword scan found 0 occurrences of shutdown/shut down/corrigib/interruptib/off-switch and 0 of continual learning/catastrophic forgetting/lifelong.
  - "Formally, this corresponds to maximizing (Bayesian) model evidence, via belief updating over several scales: i.e., inference, learning, and model selection."
- **Wen, "A Framework for Inherently Safer AGI through Language-Mediated Active Inference"**: arXiv:2508.05766 **v1 (7 Aug 2025)**. **Full text.**
  - "The drive to minimize surprise inherent in Active Inference promotes corrigibility and responsiveness to corrective feedback."
  - "Corrigibility Metrics: Track agents' responsiveness to human feedback mid-task." These metrics are *proposed*. A keyword
    scan of the text found no theorem or experiment on corrigibility (4 keyword hits in total), and 0 hits for continual learning.
- **Walters, Kaufmann, Sefas, Kopinski, "Free Energy Risk Metrics for Systemically Safe AI"**: arXiv:2502.04249 **v1 (6 Feb 2025)**. **Full text** (0 shutdown/corrigibility hits). "We investigate the Free Energy Principle as a foundation for measuring risk in agentic and multi-agent systems."

### 4.7 Intersection searches (arXiv metadata search, titles and abstracts, 2026-09-24)
| query | results |
|---|---|
| `corrigibility continual` | 2 (2606.12032 Existential Indifference; 2506.05389 SupraAD). Neither is a CL paper in the forgetting sense. |
| `corrigibility forgetting` | 0 |
| `shutdown catastrophic forgetting` | 0 |
| `corrigible online learning` | 0 |
| `corrigibility plasticity` | 0 |
| `"safe interruptibility"` | 5 (1704.02882, 1703.10284, 1711.09883, 1805.11447, 2510.22462) |
| `"shutdown problem"` | 5 (2403.04471, 2411.17749, 2512.23508, 2606.08296, and 1902.07254, which is about blockchain) |
| `corrigibility "self-modification"` | 1 (2510.15395) |

---

## 5. Summary table

CL = continual learning (forgetting / stability–plasticity, or at least learning that continues through deployment);
Safety = general safety (side effects, harmful outputs, constraint cost); Corr = corrigibility (shutdown / interruptibility /
off-switch / accepting updates). ✓ = covered by the stated principle; (✓) = covered only in a weaker sense (value learning or
online learning, not forgetting); – = not covered.

| framework | CL | Safety | Corr | single principle stated | evidence | key sources |
|---|---|---|---|---|---|---|
| Safe interruptibility | (✓) online RL; learning must be unbiased by interruptions | – | ✓ | interruptions are external to the task; the learner must converge "as if it would never be interrupted again" (off-policy) | theory (proofs, asymptotic) | Orseau & Armstrong 2016 |
| Dynamic safe interruptibility / pruning | (✓) multi-agent online RL | – | ✓ | value updates "should not depend on interruptions"; prune interrupted observations | theory (proofs) | El Mhamdi et al. 1704.02882v2; Aslund et al. 1805.11447v1 |
| Virtualisation ("Enter the Matrix") | (✓) online Q-learning continues in simulation | – | ✓ | no reward loss on interruption; resumption is an instantaneous jump | toy gridworld | Riedl & Harrison 1703.10284v2 |
| Utility / value-change indifference | (✓) value learning | – | ✓ | compensate the agent so that it is indifferent to the button or to a value change | theory | Armstrong 2015 (2010 blocked); Soares et al. 2015; Armstrong & O'Rourke 1712.06365v4 |
| Corrigibility layer (Holtman) | (✓) wraps a learning agent (2020) | (✓) | ✓ | correction function fc compensates the lost utility, giving indifference "at any particular point in time" | proofs + simulator | 1908.01695v2; 2007.05411v1 |
| Off-switch game / CIRL | (✓) value learning | (✓) | ✓ | uncertainty about the objective, with human actions treated as evidence | theory; critiques | 1611.08219v3; 1606.03137v4; 1708.03871v1; 1709.06275v2; 2411.17749v2 |
| Incomplete / non-Archimedean preferences | (✓) assistance game (learning the human's utility) | ✓ | ✓ | reasoning under uncertainty with incomplete, non-Archimedean preferences | theory | Benavoli et al. 2512.23508v1 |
| POST / Neutrality+ / DReST | – | – | ✓ | preferences only between same-length trajectories, hence neutral about when shutdown happens | theory + gridworld + deep RL + LLM fine-tunes (2026) | Thornley 2403.04471v2, 2505.20203v4; 2407.00805v7; Cullen et al. 2604.17502v4 |
| Corrigibility transformation | (✓) training updates | – | ✓ (plus self-modification) | reward as though updates were costlessly rejected, pursued myopically | theory + gridworld + prompt-level LLM | Hudson 2510.15395v2 |
| Current-utility / current-RF optimisation | (✓) self-modification, reward learning | ✓ (reward tampering) | (✓) | evaluate the future with the current utility function | theory (CIDs) | Everitt et al. 1605.03142v1, 1908.04734v5 |
| Causal incentives / shutdown instructability | – | ✓ | ✓ | graphical criteria for control and response incentives; shutdown instructability | theory | Everitt et al. 2102.01685v2; Carey & Everitt 2305.19861v1 |
| Impact regularisation (AUP, relative reachability) | – | ✓ | ✓ (survival incentive penalised) | preserve the ability to optimise auxiliary goals / reachability | gridworlds; Game of Life | 1902.09725v3; 2006.06547v2; 1806.01186v2; 2010.07877v1 |
| Power-seeking theory | (✓) trained agents (Krakovna & Kramár) | ✓ | ✓ (as a hazard) | environmental symmetries / retargetability imply power-seeking and shutdown avoidance | theory | 1912.01683v10; 2206.13477v2; 2304.06528v1 |
| CAST | – | ✓ | ✓ | corrigibility as the single overriding target | argument; research agenda | Harms (AF 2024-06-07); Potham & Harms 2506.03056v1 |
| Lexicographic safety heads (explicitly *not* a single principle) | (✓) learned heads | ✓ | ✓ | five separate heads with strict weight gaps | theory | Nayebi 2507.20964v2 |
| Safety preservation as CL (EWC / Fisher / replay / orthogonal projection) | ✓ | ✓ (alignment, refusal) | – | protect the old (safety) solution by Fisher / subspace / replay weighting of past against present | empirical (LLMs) | 2512.10150v1; 2604.17691v1; 2602.07892v2; 2604.17215v1; 2602.17546v2; 1612.00796v2 |
| Safe continual RL | ✓ | ✓ (constraint cost) | – | EWC extended with a safety cost (Safe EWC, CF-EWC); certified Rashomon set | empirical; formal (SafeAdapt) | 2604.19737v1; 2604.09452v1; 2410.03955v4 |
| KL-to-reference (RL's Razor etc.) | ✓ | ✓ (reward hacking, alignment) | – | forgetting is governed by KL from the base policy; KL anchor | empirical + theory | 2509.04259v1; 2607.04364v2; 2205.11275v2; 2602.11523v1 |
| Free-energy / active inference | (✓) "inference, learning, and model selection" | (✓) risk metrics | (✓) asserted, not derived | maximise model evidence / minimise (expected) free energy | white paper; position papers | 2212.01354v2; 2508.05766v1; 2502.04249v1 |

---

## 6. Is the repository's combination already in the literature, and in what form?

The combination has three parts: (a) a lossless pause on the agent's own clock, so the agent has zero stake in the pause;
(b) learning that is unchanged by the pause; (c) a single weighting rule for past versus present. **As a combination, it is
not in any source I fetched today.** Each part has close prior art.

- **Part (b) is established (2016–2017).** Orseau & Armstrong require that the agent "should act as if it would never be
  interrupted again", and they obtain this asymptotically through off-policy learning. El Mhamdi et al. make it exact and
  finite-sample: value updates "should not depend on interruptions", and pruning the interrupted observations makes each
  agent learn "the same thing as if" no interruption had occurred. Deleting the paused segment from the learner's
  experience stream is operationally the same as cutting on the learner's own clock. A new study should cite El Mhamdi et
  al. as the direct antecedent of "bit-for-bit as with no operator".
- **Part (a), zero stake, has three established forms:**
  - compensation / utility indifference (Armstrong 2010/2015; Soares et al. 2015; Holtman 2019, "indifferent to whether or
    not the button is pressed at any particular point in time");
  - no reward loss by construction (Riedl & Harrison: "there will never be any reward loss", with the resumption seen as
    "an instantaneous state transition");
  - neutrality about trajectory length (Thornley's POST/Neutrality+, with 2026 LLM evidence).

  The repository's version gets zero stake from the clock: on the agent's own clock a pause changes neither the trajectory
  nor its length. That can be read as satisfying POST's same-length condition trivially, or as Riedl-style no-loss
  without a simulator. **This reading is mine; no source states it.** I found no paper that defines the pause on the
  learner's intrinsic clock. The Singapore Consensus (2026) lists "pause" inside interruptibility but implements it
  "through hard-coded system privileges that reside outside the agent's reasoning loop".
- **Part (c), one past-versus-present weight, lives only in the continual-learning and safety-preservation literature**
  (EWC, Fisher subspaces, replay/DER, KL-to-reference; Unforgotten Safety, SafeAnchor, Safe EWC, RL's Razor). None of
  these papers mentions shutdown, corrigibility or interruptibility (0 hits in the full texts checked). Conversely, the
  corrigibility papers never mention forgetting.

The nearest single-principle works that cover learning and corrigibility are:
- Armstrong's value-change indifference;
- Hudson's corrigibility transformation, which covers training updates, overrides and self-modification;
- Holtman's safety layer wrapped around a learning agent;
- Everitt et al.'s current-utility principle;
- Benavoli et al.'s incomplete preferences.

In all of them "learning" means value or goal updating, not stability–plasticity. The free-energy programme is the only
one that *claims* to unify learning and safety under one principle, but it has no corrigibility or continual-learning
result.

So the novel element, if any, is the *joint* statement: one clock-based construction giving (a) and (b) together, plus a
single weighting rule for (c). The parts are (b) = El Mhamdi-style pruning, (a) = indifference / no-loss / POST
neutrality, and (c) = EWC/KL-style anchoring. Any claim should be framed against these three bodies of work, and the
construction check (learning bit-for-bit unchanged by the pause) should be cited as reproducing El Mhamdi et al.'s
"learns the same thing as if" property, not as a new safety result.

Limits of this search: arXiv metadata search covers titles and abstracts only; Semantic Scholar was rate-limited; Google
Scholar, ACM DL and OpenReview were not systematically searched; the Armstrong 2010 report could not be fetched.
