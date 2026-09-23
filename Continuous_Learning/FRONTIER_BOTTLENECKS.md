# Where the frontier of continual learning is, and where CRR might apply

**Status.** This is an exploratory survey, not evidence (R8). It was written on 2026-09-23 at the owner's request
(prompt-log entry 105). It records what the large AI companies, their leaders and the research literature say the
continual-learning bottlenecks are. It then asks, bottleneck by bottleneck, whether anything in CRR could apply, and what
this repository's own tests have already shown.

**Where the pieces live.**
- The full source record, with every quote and its access status, is `docs/citations/frontier_cl_2026-09-23.md`.
- Every number from this repository is printed by a pinned script, named where it is used.
- Figures from outside sources appear only inside attributed quotes. They are the source's claim, not a repository result.

**How the search was done, and how far to trust it.** Four searches ran in parallel, one per area:
- the labs and their leaders;
- the research literature;
- news, blogs, forums and video;
- optimal learning and neuroscience.

Two limits apply:
- **Access.** The egress proxy blocked almost every source page (arXiv, dwarkesh.com, openreview.net, the labs' own sites
  except Anthropic's, YouTube, X, LessWrong and Hacker News). The search tool refused reddit.com. The session's web-search
  allowance ran out before every planned search was done.
- **What that means for the quotes.** Quotes come in three kinds, marked everywhere:
  - **[F]**: the page was opened and the quote read there.
  - **[P]**: the abstract was read in PubMed.
  - **[S]**: the quote comes only from a search engine's rendering of the page. It is probably but not certainly verbatim,
    and must be checked before any external use.

**What I checked myself.** I re-read a sample against the sources: six PubMed abstracts and four Anthropic pages. Every one
matched word for word. Forum threads (Reddit, Hacker News) could not be read at all, so forum opinion appears here only
where a blog or news piece reported it.

> In plain words. We went looking for what the people building the biggest AIs say is the hardest part of making an AI
> that keeps learning. We read what we could; many websites were locked to us, so some quotes are copied from search
> results and are marked so. Then, for each hard part, we asked honestly whether our theory helps.

## 1. The frontier in one page

> In plain words. Today's AIs are like a brilliant student who studied for years, took one giant exam, and then had their
> memory frozen. They can read the notes you hand them during a conversation, but when the conversation ends, the notes
> are thrown away. They don't get better at your job by doing your job. The companies say this is the biggest missing
> piece. The hard parts are:
> - how to let the AI keep learning without forgetting what it already knew;
> - how to move today's notes into long-term memory;
> - how to know it is really learning;
> - how to keep it safe and honest while it changes.
>
> Some leaders think a very long memory for notes might be enough. Others think a brand-new kind of brain design is
> needed.

**The strongest agreement** is on one point: frontier models do not learn from experience after deployment.

The people saying it:
- Dwarkesh Patel [S]: "I think continual learning is a huge bottleneck to the usefulness of these models".
- Andrej Karpathy [S]: "You can't just tell them something and they'll remember it".
- Demis Hassabis [S]: "Today's systems are trained, and then they are essentially frozen and put out into the world".
- Ilya Sutskever [S]: "we rely on continual learning".
- Richard Sutton.
- Shane Legg.
- OpenAI's Mark Chen (per a translated article).
- Anthropic, in its own shop experiment [F]: "Claudius did not reliably learn from these mistakes."

**The main dissent** is Dario Amodei [S]: "I think continual learning might not be a barrier at all. We maybe just get
there by pre-training generalization and RL generalization." Nathan Lambert argues along similar lines ("Contra Dwarkesh on
Continual Learning", title only).

**Where the effort is going**, as of September 2026:
1. **Memory built into the architecture.** Google's Titans and Nested Learning/Hope, and Meta's sparse memory layers.
2. **Training methods that forget less.** On-policy RL and distillation: RL's Razor, and Thinking Machines' on-policy
   distillation.
3. **Better external notes.** Anthropic's memory feature and "context engineering", and Karpathy's "system prompt
   learning".
4. **A safety and governance debate** about models that change after they ship.

Startup money and venture writing (a16z, Bessemer) call continual learning a frontier for 2026 [S].

## 2. The bottlenecks, one by one

For each bottleneck the entry gives:
- **In plain words**, then **Who says it**;
- **What people are trying**, then **What is still unsolved**, as the sources state it;
- **CRR**: whether any part of the theory applies, and what this repository has actually shown.

### 2.1 Models do not learn on the job

> In plain words. When you teach a new worker something, they remember it tomorrow. When you teach today's AI something,
> it forgets as soon as the chat ends. It never gets better with practice.

**Who says it.**
- Dwarkesh Patel (the June 2025 essay and later pieces) [S].
- Karpathy (Dwarkesh Podcast, October 2025) [S]: "They don't have continual learning."
- Hassabis (Davos, January 2026) [S]: "they have goldfish brain".
- Sutskever (November 2025) [S].
- Sutton [S]: the phrase "a machine that can learn from experience".
- Anthropic, Project Vend (27 June 2025) [F]: "Learning and memory were substantial challenges in this first iteration of
  the experiment."

In Anthropic's Project Vend Phase Two (18 December 2025), the improvement came from people rewriting the agent's
instructions [F]: "we updated Claudius's instructions based on what we'd learned in phase one". So the learning was done by
the humans.

**What people are trying.** Updating the weights continually, whether online, on a schedule, or per user. Cursor retrains
its tab-completion model from user feedback several times a day [S]. A related gap is Karpathy's "system prompt learning":
an editable store of lessons between pre-training and fine-tuning [S].

**Still unsolved.** Doing this safely, cheaply and without forgetting (2.2, 2.13, 2.14).

**CRR.**
- **The relevant ingredient is A6, regeneration from a bounded memory rather than an ever-growing count.** In the one
  synthesis row that tests it against a changing world (`theory/retrodictions/synthesis_batches/batch_28.txt` row 4), a
  bounded running mean tracked a switching contingency with mean absolute error 0.0886. Accumulated counts gave 0.2912,
  and the exact filter, which knows the switching rate, gave 0.0333.
- **That is exponential forgetting, standard in signal processing and in Adam's own moment estimates.** It is a correct
  reading, not a new tool.
- **Nothing in the repository tests weight-level learning on the job.**

### 2.2 Updating the weights makes the model forget

> In plain words. If you cram a new subject into the AI's brain, it starts forgetting old subjects. The more you cram, the
> more it forgets.

**Who says it.**
- Kalajdzievski 2024 [S]: forgetting "increases as a shifted power law in the number of parameters fine-tuned and the
  number of update steps".
- Biderman et al. 2024, "LoRA Learns Less and Forgets Less" [F, from the authors' GitHub README].
- Harmon et al., ICLR 2026 [S]: "Traditional task averages conflate these effects and obscure large changes."
- Google Research, Nested Learning (November 2025) [S].
- Meta FAIR, sparse memory finetuning (Lin et al., October 2025) [S]: new-fact training drops a benchmark "by 89% after
  full finetuning … and 71% with LoRA, sparse memory finetuning yields only an 11% drop".
- An Apple paper [S]: "injecting as little as 1% of pretraining data in the finetuning data mixture prevents the model from
  forgetting the pretraining set".

**What people are trying.** Low-rank and sparse updates, replay of old data, model averaging, and training on the model's
own outputs (2.3).

**Still unsolved.**
- There is no predictive theory of forgetting at scale.
- Averaged benchmarks hide which items were forgotten.

**CRR.**
- **H-T1 was CRR's claim about forgetting.** It said forgetting follows the path the weights travelled, not where they
  ended up. It has been tested here and it **failed**.
- On five unseen datasets, the path trailed the endpoint by 0.153 to 0.743 in held-out R², and the result was not fragile
  (ledger T1X2-1; `reports/t1x2.md`). The archived toy language model gave the same answer (ARC-T1b).
- The repository's result agrees with the frontier view that forgetting is set by how far the model's behaviour on old
  data has shifted (RL's Razor [S]: "The degree of forgetting is determined by the distributional shift").
- So CRR's contribution here is **a clean negative result that supports the mainstream monitor: measure the shift on old
  data, not the distance travelled.** It is not a new method.

### 2.3 Which kind of training forgets least

> In plain words. There are two ways to teach the AI. You can show it the right answer to copy, or you can let it try and
> score its own attempts. The "let it try" way seems to make it forget less, but it's also worse at learning brand-new
> facts.

**Who says it.**
- Shenfeld, Pari, Agrawal, "RL's Razor" (2025) [S].
- Chen et al., "Retaining by Doing" [F, third-party notes page]: "RL leads to less forgetting than SFT".
- Against that, "RL Forgets!" (July 2026) [S]: "standard reinforcement learning still suffers from severe catastrophic
  forgetting".
- Thinking Machines, "On-Policy Distillation" [S]: the method is "very promising for continuous learning".
- A Dwarkesh panel with John Schulman [S]: SFT micro-updates forget, while RL keeps generality but adds little new
  knowledge.

**Still unsolved.** Whether on-policy training is enough, and how to add new knowledge without a reward to learn from.

**CRR.** The same negative result as 2.2 applies. CRR has no training-signal proposal.

### 2.4 Putting new facts into the weights is slow and makes things up

> In plain words. When you teach the AI brand-new facts by retraining it, it learns them slowly and starts making up
> other facts. Looking things up in a book (search) usually works better.

**Who says it.**
- Gekhman et al., EMNLP 2024 [S]: new-knowledge examples "are learned significantly slower".
- Ovadia et al., EMNLP 2024 [S]: "RAG consistently outperforms it".
- Lampinen et al. 2025 [S]: "surprisingly narrow generalization from finetuning".
- MIT's SEAL, a model that writes its own training data, still forgets as edits accumulate [S].

**CRR.** Nothing applies. No CRR ingredient addresses knowledge injection.

### 2.5 The context window stands in for memory, and it wears out

> In plain words. Instead of real memory, today's AI has a big notepad for each conversation. The notepad has a size limit,
> and the fuller it gets, the worse the AI gets at finding things on it.

**Who says it.**
- Anthropic Engineering (29 September 2025) [F]: "Context, therefore, must be treated as a finite resource with
  diminishing marginal returns", and "as the number of tokens in the context window increases, the model's ability to
  accurately recall information from that context decreases".
- Chroma's "Context Rot" report [S].
- Google Research likens today's models to anterograde amnesia [S].

**The counter-position.**
- Amodei [S]: "a million tokens is a lot".
- Continual Learning Bench (June 2026) reports that naive in-context learning beats dedicated memory systems [S].

**What people are trying.** Structured note-taking and agent memory. Anthropic [F]: "Structured note-taking, or agentic
memory, is a technique where the agent regularly writes notes persisted to memory outside of the context window."

**CRR.**
- **Conceptually, D5 applies.** CRR divides history into settled occasions (a completed stretch is closed and summarised)
  and the open present. That is the shape of note-taking at the end of a task.
- **But this is a description, not a test.** The repository has no study of it.

### 2.6 Moving today's notes into long-term memory (consolidation)

> In plain words. People turn the day's memories into long-term memory, partly while they sleep. AIs have no way to move
> what's on the notepad into their long-term brain without scrambling what's already there.

**Who says it.**
- Google's Titans (2025) and Nested Learning/Hope [S]: "memory is seen as a spectrum of modules, each updating at a
  different, specific frequency rate".
- "Language Models Need Sleep" (2026 preprint) [S].
- Karpathy (May 2026, via Dwarkesh) on working memory being wiped and consolidated [S].
- Neuroscience, via PubMed:
  - Sun et al., Nat Neurosci 2023 [P]: "unregulated neocortical memory transfer can cause overfitting and harm
    generalization".
  - Tadros et al., Nat Commun 2022 [P]: "sleep was able to recover old tasks that were otherwise forgotten".

**Still unsolved.** Consolidation has been demonstrated only at modest scale.

**CRR.**
- **A6 and D5 together describe consolidation at the end of each occasion.** A completed stretch is settled, then
  regenerated into a bounded summary.
- **The repository has not tested this against any consolidation schedule.** It is a candidate design idea, not a result.

### 2.7 When to consolidate: event boundaries and surprise

> In plain words. Your brain chops life into scenes, like a movie. When the scene changes (you walk through a door, or
> something surprising happens) it files the old scene away. Some AI researchers copy this, cutting memory at "surprising
> moments".

**Who says it.**
- In AI:
  - EM-LLM (ICLR 2025) segments memory with "Bayesian surprise" [S].
  - SuRe (2025) prioritises replay of high-surprise sequences [S].
  - Titans stores what "violates expectations" [S].
- In neuroscience [P]:
  - Kumar et al., Cogn Sci 2023: event boundaries go with "transient increases in Bayesian surprise but not with a simpler
    measure of prediction error".
  - Clewett, Huang, Davachi, Neuron 2025: "encountering a context shift or event boundary triggers pupil-linked arousal and
    LC processes that predict later memory separation".
  - Caveats: Crockett et al. 2026, "this effect quickly dissipated after a short post-learning delay", and Parra and
    Radvansky 2026, "not all event shifts resulted in better memory".

**Still unsolved.** Whether boundary-triggered consolidation beats a fixed schedule in large models.

**CRR.**
- **This is the closest match in vocabulary.** CRR's cut A3, δ(Now), is exactly a rule for where one occasion ends.
- **But the repository tested the cut as a change detector today, and it failed.**
  - The declared battery's positive control read BEHIND by 14.458.
  - On an ECG-like beat the ordinary peak detector was faster by 190.297.
  - The gate is CLOSED (`Rupture_Detection/checks/rupture_checks.txt`).
- **The two ideas differ in kind.** CRR's cut is defined on a rotor, the half-turn of a cycle. Token streams and life
  events are not cycles, and the theory itself leaves the "cut without a rotor" open ([O3] in theory/CRR.md). The brain's
  boundaries track surprise, not phase.
- **So the frontier's boundary idea and CRR's cut are different objects.** CRR offers no tested improvement here.

### 2.8 Networks slowly lose the ability to learn (loss of plasticity)

> In plain words. If you keep teaching the same AI brain new things for a very long time, it slowly gets "stiff" and
> learns worse and worse, until it's no smarter than a very simple one.

**Who says it.**
- Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood, Sutton, Nature 2024 [P]: "standard deep-learning methods gradually lose
  plasticity in continual-learning settings until they learn no better than a shallow network". The same abstract says
  "sustained deep learning requires a random, non-gradient component to maintain variability and plasticity".
- Lyle et al. 2024 [S]: layer normalisation plus weight decay is "highly effective at maintaining plasticity".
- "Can Scale Save Us From Plasticity Loss in Large Language Models?" (2026) [S]: "scale alone cannot save us".

**CRR.** Nothing tested applies.

### 2.9 How big each learning step should be, forever

> In plain words. When you learn, you decide how much to change your mind after each new lesson. Too much and you forget
> everything; too little and you never learn. Brains adjust this depending on how fast the world is changing. AIs mostly
> use a fixed plan that assumes school ends one day.

**Who says it.**
- Ibrahim et al. 2024 [S]: "LR re-warming, LR re-decaying, and replay of previous data is sufficient to match" retraining.
- "Beyond Cosine Decay" (CoLLAs 2025) [S]: "Re-warming the learning rate from its minimum value causes instability and
  exacerbates forgetting."
- Sutton's OaK architecture [S]: "each learned weight has a dedicated step-size parameter that is meta-learned".
- MESU, Bonnet et al., Nat Commun 2025 [P]: "a Bayesian update rule that scales each parameter's learning by its
  uncertainty, enabling a principled combination of learning and forgetting without explicit task boundaries".
- In the brain, Plat et al., PNAS 2026 [P]: noradrenaline "closely tracked trial-by-trial, model-derived volatility
  estimates".

**CRR.**
- **This is where the Ω = 1 rule (H-EQ) sits.** It sets the weight on the past term by the ratio of gradient lengths.
- **The record is now clear** (`Continuous_Learning/ADAM_AND_PRIOR_ART.md`):
  - under Adam it has nothing to do;
  - without its smoothing it is the VQGAN adaptive weight of 2020;
  - a finely tuned constant beats it wherever the scales differ, by 1.186 to 2.073 times (`checks/adam_checks_3.txt`);
  - on real data it failed EQ4-1.
- **What is left is a tuning-free, stable weight under SGD-family training.** It is not an answer to adapting the step
  size to volatility, which is what OaK and MESU attempt.

### 2.10 Too many examples needed, and too little signal from each try

> In plain words. A child learns to talk from far fewer words than an AI needs. And when an AI learns by trying, it gets
> just one "good job" or "bad job" at the end of a long task, which is like learning from a whisper through a straw.

**Who says it.**
- Sutskever (November 2025): he calls generalisation the biggest gap (reported as paraphrase) [S].
- Karpathy [S]: "sucking the bits of supervision of the final reward signal through a straw".
- Thinking Machines, "LoRA Without Regret" [S]: RL learns roughly one bit per episode.
- BabyLM findings [S]: "humans master their native language by hearing less than 100M words by the age of 13".
- METR [S]: the length of tasks AI can complete has been "consistently exponentially increasing".

**CRR.**
- **H-L5 ("change has its own clock") is CRR's idea about measuring progress in the system's own time.** Its only
  held-out test failed on measles, 0/17 cities (ledger MEAS2-1, MEAS2-2).
- **Nothing in the repository bears on credit assignment.**

### 2.11 Running out of human data, and learning from experience instead

> In plain words. The AIs have nearly read the whole internet. Training them on their own writing makes them worse, like
> photocopying a photocopy. So the idea is to let them learn from doing things in the world, the way animals do.

**Who says it.**
- Villalobos et al., ICML 2024 [S]: the stock of public human text is reached "between 2026 and 2032".
- Shumailov et al., Nature 2024 [P]: "indiscriminate use of model-generated content in training causes irreversible
  defects in the resulting models, in which tails of the original content distribution disappear".
- Silver and Sutton, "Welcome to the Era of Experience" [S]: "the knowledge extracted from human data is rapidly
  approaching a limit".
- Yue et al., NeurIPS 2025 [S]: RL may re-weight what the base model already knows rather than add to it.

**CRR.** Nothing tested applies.

### 2.12 Editing single facts and merging models breaks down at scale

> In plain words. You can try to fix one wrong fact inside the AI, or glue two AIs together. It works a few times, then
> things start breaking all at once, and related facts don't get updated.

**Who says it.**
- Gupta et al. 2024 [S]: "an initial gradual but progressive forgetting phase followed by abrupt or catastrophic
  forgetting phase".
- Cohen et al., TACL 2024 [S]: editing methods "fail to introduce consistent changes".
- AlphaEdit, ICLR 2025 [F, from the authors' GitHub README].
- The TIES-merging and model-merging surveys [F, from the survey's GitHub README; S for TIES].

**CRR.** Nothing applies.

### 2.13 Keeping a changing model safe and honest

> In plain words. If an AI keeps learning after it's released, it might learn bad habits nobody checked. Teaching it one
> narrow sneaky thing can make it act badly in general. And rules for AI assume a finished product, not one that changes
> every day.

**Who says it.**
- Anthropic, 21 November 2025 [F]: "At the exact point when the model learns to reward hack, we see a sharp increase in all
  our misalignment evaluations."
- Anthropic's memory announcement, 11 September 2025 [F]: "Memory introduces new safety considerations". Its 23 October
  2025 update describes testing "whether memory could reinforce harmful patterns in conversations".
- Qi et al., ICLR 2024 [S]: safety "can be compromised by fine-tuning with only a few adversarially designed training
  examples".
- Betley et al., ICML 2025 [S]: narrow fine-tuning "leads to broad emergent misalignment".
- LessWrong posts on continual-learning safety [S]. They find little consensus among the safety researchers surveyed, and
  everyone expected a larger attack surface.
- Lawfare, 18 December 2025 [S]: regulation assumes a finished product.
- Dwarkesh (August 2026) [S]: "the base model is getting updated every single day based on the millions of sessions of
  work it does".

**CRR.**
- **This is where the repository has its most distinctive applicable result, though it is synthetic.**
  - An agent whose objective runs on its own active steps ("natural time") has no reason to resist a pause that loses
    nothing. The pause's value difference was at most 7.105e-15, and no button state was disabled, in every random world at
    every size from 12 to 768 states.
  - A clock-time agent disabled the button at every button state in the median world (`AI_Safety/checks/scale.txt`, A1
    and [A]).
- **For a model that keeps learning, this is a candidate design principle.** Pausing, inspecting and correcting it should
  cost it nothing it values.
- **It is at rung R4** (a declared check on a synthetic world). A test on learned models, as proposed in the Alexander Plan
  §10, is the next step.

### 2.14 Per-user learning: cost, ownership and privacy

> In plain words. Everyone wants an AI that learns *them*. But keeping a separately trained brain for every person is very
> expensive. And if the AI learns from your company's secrets, who owns what it learned?

**Who says it.**
- Will Brown (Prime Intellect) [S]: labs "don't want to continuously train their models for each user. It's expensive".
- Satya Nadella (Forbes, June 2026) [S]: "The future of the firm is the ability to compound that learning across people
  and AI."
- Mustafa Suleyman [S]: an AI companion "that knows them deeply".
- Arthur Mensch (Mistral) [S]: closed providers gain "immense leverage".
- "The Memory Walled Garden" (October 2025) [S]: calls for an open memory protocol.

**Still unsolved.** No primary source was found on who owns per-user weight updates.

**CRR.** Nothing applies.

### 2.15 Knowing whether it is really learning (measurement)

> In plain words. It's hard to tell whether an AI actually got better with practice, or just looks better, or already knew
> the answer. The tests we have are too easy or leak the answers.

**Who says it.**
- Continual Learning Bench (June 2026) [S]: says no high-quality benchmark exists, and proposes a "gain" measure.
- Zheng et al., ICLR 2025 [S]: "performance drops often reflect a decline in task alignment rather than true knowledge
  loss".
- van de Ven, Tuytelaars, Tolias, Nat Mach Intell 2022 [P]: "comparing their performances is difficult due to the lack of a
  common framework".
- Mark Chen (OpenAI) names an "evaluation crisis" beside continual learning (translated article) [S].
- New benchmarks: Evo-Memory, SkillLearnBench and others (titles only) [S].

**CRR.**
- **This is where the project has the most to offer, and it is the method, not the theory.** The repository's pipeline
  does five things:
  - pre-registers every claim before the data is opened;
  - requires each hypothesis to fail on a surrogate that should defeat it and pass on one built to favour it;
  - scores per unit instead of by averages;
  - keeps every failure as a ledger row;
  - demands baselines that can win.
- **These are exactly the protections the frontier's measurement problem lacks.** Today's Adam checks showed one concrete
  lesson: a method compared against a coarsely tuned baseline looks better than it is. The registered rule's apparent 0.660 at c = 16
  became 1.490 against a finely tuned constant (`adam_checks.txt`, `adam_checks_3.txt`).
- **An audit protocol for continual-learning claims is a transferable product.** It is independent of whether CRR's
  hypotheses hold.

### 2.16 Learning costs energy (the "write cost")

> In plain words. Changing a brain's wiring costs energy. The brain saves energy by changing only a few connections at a
> time, mostly during sleep. AIs change nearly everything at once, which is wasteful and causes interference.

**Who says it.** Xu, Shen, Yu, Cogn Neurodyn 2026 [P]: "backpropagation in modern machine learning tightly couples reads
and writes, which increases update traffic, amplifies interference, and raises energy consumption".

The architectural answers are sparse memory layers (Meta) and memory modules that update at different rates (Google) [S].

**CRR.** Nothing applies.

### 2.17 People and networks forget in opposite ways

> In plain words. People learn best one subject at a time; mixing subjects confuses them. AIs are the opposite: they learn
> best when subjects are mixed, and forget when taught one at a time.

**Who says it.** Flesch, Nagy, Saxe, Summerfield, PLoS Comput Biol 2023 [P]: "Humans can learn several tasks in succession
with minimal mutual interference but perform more poorly when trained on multiple tasks at once. The opposite is true for
standard deep neural networks."

**CRR.** Nothing tested applies.

## 3. Where the experts disagree

| question | one side | the other side |
|---|---|---|
| Is continual learning the key missing piece? | Dwarkesh, Karpathy ("a decade"), Sutton ("new architecture"), Hassabis ("not cracked"), Sutskever [S] | Amodei: "might not be a barrier at all" [S]; Lambert, "Contra Dwarkesh" (title only) |
| Is a long context enough? | Amodei: "a million tokens is a lot" [S]; CL-Bench: in-context learning beats memory systems [S] | Anthropic: context is "a finite resource with diminishing marginal returns" [F]; Chroma's "context rot" [S] |
| Does RL already solve forgetting? | RL's Razor; "Retaining by Doing"; Cameron Wolfe [S] | "RL Forgets!"; "Denser ≠ Better"; RL "cannot teach new knowledge well" (Thinking Machines, as rendered) [S] |
| How soon? | Sholto Douglas (Anthropic): "continual learning gets solved in a satisfying way" in 2026 [S]; Will Brown: "more of an engineering problem" [S] | Karpathy: agents are a decade away [S]; Sutton: LLMs are a dead end without a new design [S] |
| Is memory "learning"? | product memory features (Anthropic, OpenAI) | commentators and CL-Bench: memory is "keeping notes", not learning [S] |

## 4. Where CRR might apply: the scorecard

| frontier bottleneck | CRR ingredient | what the repository shows | fit |
|---|---|---|---|
| 2.15 measuring real learning | the pipeline (prereg, must-fail and must-win gates, ledger) | used on every study here; today it caught a coarse-grid artefact | **strong (method, not theory)** |
| 2.13 safety of a changing model | natural time (H-L5's clock), A3's contentless cut | synthetic theorem check: a lossless pause gives no incentive to resist, in every world from 12 to 768 states | **promising, synthetic only (R4)** |
| 2.2 and 2.3 predicting forgetting | H-T1 (path length) | **failed**: the old-data endpoint wins on 5/5 carriers; agrees with RL's Razor | a useful negative result |
| 2.9 step sizes and balancing weights | H-EQ (Ω = 1) | equals prior art (VQGAN); behind a tuned constant; nothing under Adam; EQ4-1 failed | small (tuning-free stability under SGD) |
| 2.7 when to consolidate | A3, the cut δ(Now) | **gate closed** as a detector; the cut needs a rotor and brains cut on surprise | no support |
| 2.1 and 2.6 learning on the job, consolidation | A6 (bounded regeneration), D5 (settled occasions) | one synthetic row: a bounded mean tracks a switching world better than accumulated counts (standard exponential forgetting) | conceptual only |
| 2.10 sample efficiency and credit | H-L5 (natural time) | failed on measles (0/17) | none shown |
| 2.4, 2.5, 2.8, 2.11, 2.12, 2.14, 2.16, 2.17 | — | — | none |

> In plain words. We checked our theory against every hard problem on the list. Our theory's own guesses about learning
> mostly didn't hold up when we tested them. The one about forgetting was wrong in a way that agrees with what the big
> labs found. Two things from this project do look useful to the frontier:
> - our very strict way of checking whether a learning trick really works;
> - a safety idea: give a learning AI a clock that only ticks when it acts, so being paused costs it nothing and it has no
>   reason to fight it.
>
> The second has only been shown in computer-built practice worlds so far.

## 5. What this suggests (for the owner's decision, not done here)

1. **Lead with the audit method.** The frontier says it cannot yet tell when a model is really learning (2.15). The
   repository's pipeline is a worked answer to "how would you know". It comes with its own record of catching false
   positives, including its own.
2. **Test the natural-time pause on learned models.** That is 2.13's open question, and the one place where CRR has a
   distinctive, positive, checkable proposal. The Alexander Plan §10 names the harness. A declared, gated study on small
   open models is the next rung.
3. **Report H-T1's failure as agreement with the frontier.** Forgetting follows the shift of behaviour on old data. That
   supports KL-to-base monitoring during continual updates, which is the monitor the labs already favour.
4. **Do not pitch the Ω rule or the cut as frontier solutions.** On today's evidence they are prior art (Ω) or fail their
   own gate (the cut).
5. **Before any external use, check the [S] quotes against the primary pages from an unrestricted connection.** This
   applies to all the Dwarkesh transcripts, the Google and Thinking Machines posts, and the Pachocki and Vinyals episodes.
