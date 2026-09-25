# Systematic sweep, family P (prior art for C1–C5), 2026-09-25

Run on 2026-09-25 by a literature agent following `sweep/BRIEF.md` and `Lossless_Pause/DECLARATION_2.md` (family P). This is a note, not evidence (R8). Every quote is a verbatim substring of the raw text saved in the session scratchpad at `sweep/prior_art/<slug>.txt`. The check applies html-unescape, removes U+FFFE and U+00AD, joins "-\n" and collapses whitespace. PDF text was extracted with pypdf, so hyphenated line breaks appear joined, some words run together (e.g. "toverifyLLM", "anyweight") and PDF ligatures (ﬁ, ﬀ) are kept exactly as extracted. Machine-readable claims are in `sweep/prior_art_claims.json`. The quote check found 44/44 quotes.

**Failures on the day.**

- **arXiv API.** The declared call (`curl -sS "http://export.arxiv.org/api/query?search_query=all:<q>&start=0&max_results=25&sortBy=relevance"`) got an empty body for all 12 queries, on the attempt and on the retry (24 attempts, about 20:27 UTC). The http:// URL answers 301 to https://, and the https:// endpoint answers HTTP 406 to uncached queries (checked by hand, and on three further spaced attempts for q01–q03, logged in `sweep/prior_art/api/attempts.log`). As a fallback, each query was run once on the arXiv listing search (`arxiv.org/search/?query=<q>&searchtype=all&abstracts=show&order=&size=25`, raw HTML saved as `sweep/prior_art/api/sNN.html`). That service matches all terms, not relevance-ranked over all fields: four queries returned 0 hits, and the lists for the broad queries come back newest-first, so their first 25 hits are the most recent, not the most relevant. The hit counts below are the listing search's, not the API's.
- **github.com** is refused by the proxy (HTTP 403, checked with curl for Megatron-Bridge PR #6209 and UniRL issue #499). Both are on-topic for C4 by the search snippet, and neither was fetched. The schedule-free repository was not fetched either; the paper was used.
- **opencompute.org** ("Silent Data Corruption in AI", OCP whitepaper) returned HTTP 403 to curl and to WebFetch.

**Must-include works.** All seven were found and fetched. Found by the queries: TOPLOC (q3 web), Orseau & Armstrong 2016 (q4 web, MIRI page → paper PDF), D-Adaptation and Prodigy (q9 web). Added by title search: Proof-of-Learning (Jia et al. 2021), Verde (2025), the off-switch game (Hadfield-Menell et al. 2017), and schedule-free (Defazio et al., "The Road Less Scheduled"; the q9 web hit was its github repository, refused). Canonical earlier works cited by included hits were also added by title: Soares et al. 2015 "Corrigibility" (q6 web hit), and ACT (Graves 2016) and PonderNet (2021). ACT and PonderNet are cited as the adaptive-computation baselines by 2604.22110 and 2607.20519.

**Cap.** 25 sources are included. Items marked QUALIFYING in the log were on topic but not fetched because of the cap (the most recent and most-cited were preferred). 1704.02882 was fetched and then dropped for the cap; it has no quotes.

## Sources

### P1. Srivastava, Arora, Boneh, 'Optimistic Verifiable Training by Controlling Hardware Nondeterminism', NeurIPS 2024, arXiv 2403.09603

- Version: arXiv 2403.09603v3 (25 Nov 2024)
- URL: https://arxiv.org/abs/2403.09603v3
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/optimistic_vt.txt`

> The game’s efficiency lies in our ability to store hashes of model checkpoints in a Merkle tree [Merkle, 1988]. To determine if training was performed according to the specification, the auditor needs to reconstruct the Merkle tree and compare the resulting Merkle root hash with the Merkle root hash provided by the trainer’s

> the auditor can store the hashsha256(θ) of model weightsθ in a Merkle tree at intervalk, knowing that if training was done correctly, the model weights should be identical to the trainer’s at any timestep.

Tag: C1. CLOSE: hashes (sha256) of model weights at an interval, stored in a Merkle tree, are compared between trainer and auditor to verify that training followed the specification. Difference from C1: an audit of a whole training trajectory by independent re-execution (with rounding logs to force identical weights across GPUs), not the check that a pause/resume restored the saved state; hashed object is the weights.

### P2. Arun et al., 'Verde: Verification via Refereed Delegation for Machine Learning Programs', arXiv 2502.19405

- Version: arXiv 2502.19405v1 (26 Feb 2025)
- URL: https://arxiv.org/abs/2502.19405v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/verde.txt`

> it suffices for now to assume that the checkpoint consists of just the aforementioned state and is committed to using a standard collision-resistant hash function like SHA-256.

> hashing the weights and Adam optimizer state (Kingma & Ba, 2014) (the optimizer state is double the size of the weights alone) in FP32 precision for DistilBERT (66 million parameters) takes under a second, for Llama-1B takes around 2.5 seconds, and for Llama-8B around 15 seconds

Tag: C1. CLOSE: a training checkpoint (weights and optimizer state) is committed with SHA-256 and two executions are compared by checkpoint hash to find the first diverging step. Difference from C1: dispute resolution between two trainers re-executing the same program (bitwise reproducible operators), not verification of one learner's pause/resume.

### P3. Jia, Yaghini, Choquette-Choo, Dullerud, Thudi, Chandrasekaran, Papernot, 'Proof-of-Learning: Definitions and Practice', IEEE S&P 2021, arXiv 2103.05633

- Version: arXiv 2103.05633v1 (9 Mar 2021)
- URL: https://arxiv.org/abs/2103.05633v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/jia2021_pol.txt`

> follow up work may consider hashing weights sequentially utilizing Merkle tree structure [85], i.e. each consecutive set of weights during the training procedure are hashed and then saved as the hash of the concatenation of the current weights and the previously saved hash. We do not use Merkle trees due to the error accumulated when the veriﬁer reconstructs the weights: the error in the weights forces the weights of the veriﬁer and legitimate worker to hash to different values, losing the ability

Tag: C1. BEARS: Proof-of-Learning verifies logged checkpoints by re-executing steps and comparing weights within a tolerance; it names hashing weights in a Merkle chain and rejects it because re-execution error makes honest weights hash differently. Neither states hashing to verify a pause/resume.

### P4. Su, Yao, Zhang, Wang, Viswanath, 'OVIG: Optimistic Verification of AI Training Integrity via Gradient Signals', arXiv 2606.21045

- Version: arXiv 2606.21045v1 (19 Jun 2026)
- URL: https://arxiv.org/abs/2606.21045v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/ovig.txt`

> Exact comparison is straightforward only when honest replay is bitwise reproducible. Modern accelerator training rarely has this property.

> The key point is that OVIG does not try to prove bitwise equality of an entire training trajectory.

Tag: C1. BEARS: replay-based training audit that explicitly does not rely on bitwise (hash-level) equality; uses a calibrated gradient-error boundary instead. Bears on when a state digest can serve as the check (only where replay is bit-exact).

### P5. Ong et al., 'TOPLOC: A Locality Sensitive Hashing Scheme for Trustless Verifiable Inference', arXiv 2501.16007

- Version: arXiv 2501.16007v2 (30 May 2025)
- URL: https://arxiv.org/abs/2501.16007v2
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/toploc.txt`

> The method performs locality-sensitive hashing of the intermediate activations, which encodes the top-k values and indices as a polynomial congruence.

Tag: C1. BEARS: hashes intermediate activations (a locality-sensitive, tolerance-bearing hash) to verify inference; it verifies computation through activations/outputs, not a saved-versus-restored state digest.

### P6. Wang, 'SCOUT: Symmetric Consensus Outlier Detection for Failure Localization in LLM Pre-Training', arXiv 2608.11034

- Version: arXiv 2608.11034v1 (11 Aug 2026)
- URL: https://arxiv.org/abs/2608.11034v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/scout.txt`

> Clean replay coverage certifies checkpoint numerical integrity, preventing recovery from selecting state corrupted by SDC.

Tag: C1. BEARS: certifies checkpoints for recovery by in-situ replay consensus across ranks (SDC detection), not by hashing saved against restored state.

> SCOUT also uses replay verdicts to certify model checkpoints, allowing failure recovery to use in-memory checkpoints when numerically trusted and otherwise fall back to the latest verified checkpoint.

Tag: C4. BEARS: recovery restricted to certified checkpoints; a resume-correctness practice, not the E1-E3 checklist.

### P7. Mitra, 'When Is Availability-Aware Training Worth It? A Benchmark and Empirical Study of Interruption-Resilient Optimization Under Predictable Compute Schedules', arXiv 2609.22087

- Version: arXiv 2609.22087v1 (22 Jun 2026)
- URL: https://arxiv.org/abs/2609.22087v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/availability_training.txt`

> On resume,(θ,m )are byte-identical to their pre-gap values and ηk = ηschedule(teff)is unchanged because teff counts active time only. Hence each post-gap update is function-identical to the corresponding continuous-training update.

Tag: C1. BEARS: asserts byte-identity of restored (θ, m) as the premise of a proof sketch that a gap is a no-op; no digest or hash audit of the restore is stated.

> A baseline that preserves full optimizer state across a gap and advances its learning-rate schedule ineffective(active) time, not wall-clock time, reproduces uninterrupted training almost perfectly.

> under full-state preservation an availability gap injects no bias and no excess loss; it is a no-op up to minibatch-ordering noise.

Tag: C4. STATES (E1+E2): full state (weights, optimizer state) plus schedule indexed on effective (active) time rather than wall-clock makes a gap a no-op; proved (sketch) and tested on CIFAR-10/ResNet-18 and GPT-2/AdamW. Framed as the baseline bar for interruption-resilient training, not as a design rule named 'empty cut'.

> Checkpoint(weak): preserve( θ,m,BN stats )across a gap but index the learning-rate schedule on wall-clocktime t. The schedule advances during idle gaps, over-annealing the learning rate at resumption. This is the strawman.

> (B) when the data distribution drifts across the gap so that preserved state is stale.

Tag: C4. CLOSE (E2, E3): wall-clock keying named as the failure; distribution drift across the gap (the world's content) tested as a separate cost regime. Difference from C4: E3 is an empirical regime, not a checklist item; no valuation/incentive component.

### P8. Rinberg, Karvonen, Hoover, Reuter, Warr, 'Verifying LLM Inference to Detect Model Weight Exfiltration', arXiv 2511.02620

- Version: arXiv 2511.02620v3 (12 Mar 2026)
- URL: https://arxiv.org/abs/2511.02620v3
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/weight_exfil.txt`

> This work investigates how toverifyLLM model inference to defend against such attacks and, more broadly, to detect anomalous or buggy behavior during inference.

Tag: C1. BEARS: verification of inference by recomputation to detect anomalous or buggy behaviour; output-level, not a state digest.

### P9. Wang et al., 'VeriLLM: A Lightweight Framework for Publicly Verifiable Decentralized Inference', arXiv 2509.24257

- Version: arXiv 2509.24257v4 (22 Jan 2026)
- URL: https://arxiv.org/abs/2509.24257v4
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/verillm.txt`

> Verifiers are required to submit not only their final judgment but also specific sampled hidden states. These lightweight state fragments undergo on-chain adjudication via the smart contract, where any deviation triggers immediate penalization.

Tag: C1. BEARS: sampled hidden-state fragments are compared for inference verification; no saved/restored state digest.

### P10. Orseau, Armstrong, 'Safely Interruptible Agents', UAI 2016

- Version: UAI 2016 paper PDF (MIRI-hosted), no arXiv version
- URL: https://intelligence.org/files/Interruptibility.pdf
- Fetch: curl, HTTP 200 (PDF, 10 pages; UAI 2016 paper hosted by MIRI; no arXiv version).
- Raw text: `sweep/prior_art/orseau_armstrong2016.txt`

> This paper explores a way to make sure a learning agent will not learn to prevent (or seek!) being interrupted by the environment or a human operator.

> Third, in Section 3 we show that some algorithms like Q-learning are safely interruptible, while others like Sarsa [Sutton and Barto, 1998] are not, but can be simply modiﬁed to be made safely interruptible.

Tag: C2. CLOSE: a learner that does not learn to prevent (or seek) interruption; obtained through off-policy learning (Q-learning) or a modification (Sarsa). Difference from C2: the mechanism is off-policy value learning with interruptions imposed as a policy, not a valuation keyed to the learner's own steps with a lossless (state-preserving) pause.

> To make the human interruptions not appear as being part of the task at hand, instead of modifying the observations received by the agent we forcibly temporarily change the behaviour of the agent itself.

Tag: C2. CLOSE: interruptions kept external to the task; bears on C2's 'the pause is not content' reading. Difference: no state-preservation or own-clock condition.

### P11. Hadfield-Menell, Dragan, Abbeel, Russell, 'The Off-Switch Game', IJCAI 2017, arXiv 1611.08219

- Version: arXiv 1611.08219v3 (16 Jun 2017)
- URL: https://arxiv.org/abs/1611.08219v3
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/offswitch.txt`

> A traditional agent takes its reward function for granted: we show that such agents have an incentive to disable the off switch, except in the special case where H is perfectly rational.

> Our key insight is that for R to want to preserve its off switch, it needs to be uncertain about the utility associated with the outcome, and to treat H’s actions as important observations about that utility.

Tag: C2. BEARS/CLOSE: the incentive to disable the off switch is removed by uncertainty about the utility and treating the human's action as evidence. Different mechanism from C2 (objective uncertainty, not zero stake at the pause); concerns shutdown, not a lossless pause.

### P12. Soares, Fallenstein, Yudkowsky, Armstrong, 'Corrigibility', AAAI 2015 Workshops

- Version: AAAI-15 workshop paper PDF (MIRI-hosted)
- URL: https://intelligence.org/files/Corrigibility.pdf
- Fetch: curl, HTTP 200 (PDF, 10 pages; AAAI-15 workshop paper hosted by MIRI).
- Raw text: `sweep/prior_art/soares2015_corrigibility.txt`

> We introduce the notion of corrigibility and analyze utility functions that attempt to make an agent shut down safely if a shutdown button is pressed, while avoiding incentives to prevent the button from being pressed or cause the button to be pressed

Tag: C2. CLOSE: utility functions designed so the agent has no incentive to prevent or cause the shutdown button being pressed (utility indifference). Difference from C2: indifference by compensatory utility terms between U_N and U_S; C2 obtains no incentive from a valuation on own steps plus a lossless pause.

### P13. Carey, Everitt, 'Human Control: Definitions and Algorithms', UAI 2023, arXiv 2305.19861

- Version: arXiv 2305.19861v1 (31 May 2023)
- URL: https://arxiv.org/abs/2305.19861v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/human_control.txt`

> The first proposed algorithm, utility indifference, aims to neutralise any incentives for the agent to control its instructions, by giving the agent a finely tuned, compensatory reward in the event that a shutdown instruction is given

> Unfortunately, utility indifference fails to fully incentivise corrigibility. Indeed, utility indifferent agents need not be incentivised to preserve a shutdown apparatus that is only used during shutdown, ensure they receive correct instruction, nor avoid creating incorrigible subagents

Tag: C2. CLOSE: names the indifference family (utility indifference, interruptibility) that neutralises the incentive to control the instruction, and its known gaps. Difference as for Soares et al. 2015.

### P14. Clark, 'The Veto Variable: Human Override as a Goal-Independent Cost Term', arXiv 2609.00109

- Version: arXiv 2609.00109v2 (2 Sep 2026)
- URL: https://arxiv.org/abs/2609.00109v2
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/veto_variable.txt`

> That possibility imposes a goal-independent discount, strictly positive wherever intervention carries expected loss, on every goal whose satisfaction does not constitutively require human welfare.

Tag: C2. BEARS: the stake in oversight is stated as positive wherever intervention carries expected loss; the zero-loss case (C2's lossless pause) is the complement and is not treated as a design.

### P15. Thorstad, 'Revisiting the shutdown problem', arXiv 2606.08296

- Version: arXiv 2606.08296v2 (13 Aug 2026)
- URL: https://arxiv.org/abs/2606.08296v2
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/revisiting_shutdown.txt`

> Second, concern for the catastrophic shutdown problem has led to technical solutions that impose a high safety tax on model performance.

Tag: C2. BEARS: argues shutdown-problem solutions impose a safety tax on performance; relevant to whether a zero-stake pause is costless.

### P16. Defazio, Mishchenko, 'Learning-Rate-Free Learning by D-Adaptation', ICML 2023, arXiv 2301.07733

- Version: arXiv 2301.07733v5 (7 Jul 2023)
- URL: https://arxiv.org/abs/2301.07733v5
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/dadapt.txt`

> D-Adaptation is an approach to automatically setting the learning rate which asymptotically achieves the optimal rate of convergence for minimizing convex Lipschitz functions, with no back-tracking or line searches, and no additional function value or gradient evaluations per step.

> the method automatically matches hand-tuned learning rates across more than a dozen diverse machine learning problems, including large-scale vision and language problems.

Tag: C3. CLOSE: a hyperparameter-free rule that removes the learning-rate sweep and matches hand-tuned values. Difference from C3: removes the learning rate, not a regularisation/penalty weight in continual learning.

### P17. Mishchenko, Defazio, 'Prodigy: An Expeditiously Adaptive Parameter-Free Learner', ICML 2024, arXiv 2306.06101

- Version: arXiv 2306.06101v4 (19 Mar 2024)
- URL: https://arxiv.org/abs/2306.06101v4
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/prodigy.txt`

> Our experimental results show that our approach consistently outperforms D-Adaptation and reaches test accuracy values close to that of hand-tuned Adam.

Tag: C3. CLOSE: learning-rate-free estimation matching hand-tuned Adam. Difference as for D-Adaptation (learning rate, not penalty weight).

### P18. Defazio, Yang, Mehta, Mishchenko, Khaled, Cutkosky, 'The Road Less Scheduled' (Schedule-Free), NeurIPS 2024, arXiv 2405.15682

- Version: arXiv 2405.15682v4 (29 Oct 2024)
- URL: https://arxiv.org/abs/2405.15682v4
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/schedulefree.txt`

> Our Schedule-Free approach introduces no additional hyper-parameters over standard optimizers with momentum.

> Schedule-Free AdamW is the core algorithm behind our winning entry to the MLCommons 2024 AlgoPerf Algorithmic Efficiency Challenge Self-Tuning track.

Tag: C3. CLOSE: removes the schedule/stopping-time hyperparameter; winner of AlgoPerf self-tuning track. Difference: schedule, not penalty weight.

### P19. Kasimbeg, Roulet, Agarwal, Medapati, Pedregosa, Agarwala, Dahl, 'How far away are truly hyperparameter-free learning algorithms?', arXiv 2505.24005

- Version: arXiv 2505.24005v1 (29 May 2025)
- URL: https://arxiv.org/abs/2505.24005v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/hpfree_far.txt`

> All algorithms presented above leave aside the tuning of (i) anyweight decay, (ii) themomentum or exponential moving average parameter of the gradients(used in SGD with momentum orAdam), and (iii) theexponential moving average parameter of the second momentestimate in Adam.

> The best “AlgoPerf-calibrated” learning-ratefree methods had much improved performance but still lagged slightly behind a similarly calibrated NadamW baseline in overall benchmark score.

Tag: C3. BEARS: states that learning-rate-free methods leave regularisation weights (weight decay) untuned and that calibrated defaults still lag a calibrated NadamW; the tuning-free regularisation weight is stated as open, not solved, as of v1 (May 2025).

### P20. Karpukhin, Savchenko, 'When Losses Align: Gradient-Based Composite Loss Weighting for Efficient Pretraining', arXiv 2605.07756

- Version: arXiv 2605.07756v1 (8 May 2026)
- URL: https://arxiv.org/abs/2605.07756v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/losses_align.txt`

> Tuning these weights with random search or Bayesian optimization is computationally expensive, as it requires many independent training runs.

> reducing the overhead of hyperparameter tuning to approximately 30% above a single training run.

Tag: C3. CLOSE: loss-term weights learned online instead of a sweep (about 30% overhead over one run). Difference from C3: bilevel alignment to a downstream objective for pretraining losses, not a calibrated Laplace/Fisher penalty weight for continual learning; not zero-overhead.

### P21. Popescu, Sáez de Ocáriz Borde, Liò, 'Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts', arXiv 2607.20519

- Version: arXiv 2607.20519v1 (8 Jul 2026)
- URL: https://arxiv.org/abs/2607.20519v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/looped_halting.txt`

> Convergence readouts exit when the trajectory appears to have stabilized, using quantities such as predictive KL between consecutive predictions, logit change, or hidden-state movement.

> Early-exit feedforward Transformer methods have also used confidence, entropy, or prediction stability as inexpensive criteria for terminating computation (Schuster et al., 2022; Xin et al., 2020; Zhou et al., 2020)

Tag: C5. CLOSE: halt when the prediction has settled, measured by predictive KL between consecutive predictions (a threshold rule), with earlier early-exit precedents. Difference from C5: halting depth in a looped/early-exit network at inference, thresholded on a calibrated grid; no own-clock (arc) accumulation or sequential-test framing.

### P22. Movahedi et al., 'Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers', arXiv 2606.18206

- Version: arXiv 2606.18206v1 (16 Jun 2026)
- URL: https://arxiv.org/abs/2606.18206v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/fixedpoint_reasoners.txt`

> uses fixed-point convergence as an end-to-end halting mechanism in a looped architecture. We show that fixed-point halting allows FPRM to adapt its compute to the difficulty of the task.

Tag: C5. CLOSE: stop computing when the iterate reaches a fixed point (the state has settled). Difference: fixed-point convergence of a looped transformer's hidden state, not a belief/posterior settling criterion.

### P23. Graves, 'Adaptive Computation Time for Recurrent Neural Networks', arXiv 1603.08983

- Version: arXiv 1603.08983v6 (21 Feb 2017)
- URL: https://arxiv.org/abs/1603.08983v6
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/act_graves.txt`

> an algorithm that allows recurrent neural networks to learn how many computational steps to take between receiving an input and emitting an output.

> augment the network output with a sigmoidal halting unit whose activation determines the probability that computation should continue.

Tag: C5. BEARS/CLOSE: learned halting of computation per input (canonical). Difference: a learned halting unit with a ponder cost, not a settling criterion on the belief.

### P24. Banino, Balaguer, Blundell, 'PonderNet: Learning to Ponder', ICML 2021 AutoML workshop, arXiv 2107.05407

- Version: arXiv 2107.05407v2 (2 Sep 2021)
- URL: https://arxiv.org/abs/2107.05407v2
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/pondernet.txt`

> PonderNet learns end-to-end the number of computational steps to achieve an eﬀective compromise between training prediction accuracy, computational cost and generalization.

Tag: C5. BEARS/CLOSE: learned halting distribution trading accuracy against compute. Difference as for ACT.

### P25. Kallel, Tölle, Hendawy, D'Eramo, 'Do Not Imitate, Reinforce: Iterative Classification via Belief Refinement', arXiv 2604.22110

- Version: arXiv 2604.22110v1 (23 Apr 2026)
- URL: https://arxiv.org/abs/2604.22110v1
- Fetch: arxiv.org/abs page and arxiv.org/pdf (current version), HTTP 200; text via pypdf.
- Raw text: `sweep/prior_art/ric_belief_refinement.txt`

> Given that the value function explicitly estimates the potential for future refinement, a near-zero value indicates that further computation is unlikely to improve the prediction. This naturally provides a transparent halting signal without requiring any additional parameters.

> The learned policy naturally manages its own computation by allocating more effort on resolvable inputs while halting when further improvement appears unlikely.

Tag: C5. CLOSE: a recurrent agent refines a belief (predictive distribution over classes) and halts when the learned value of further refinement is near zero. Difference from C5: halting keyed to a learned value of expected improvement in log-score, not to an own-clock (arc) settling criterion or a sequential test; per-input inference, classification only.

## Claims

Reading per claim, as recorded in the claims file. STATES means the quote states the candidate. CLOSE means it states a close form, and the difference is named. BEARS means it only bears on the candidate. No novelty judgement is made here (CLAUDE.md §7).

| tag | source | reading |
|---|---|---|
| C1 | arXiv 2403.09603 | CLOSE |
| C1 | arXiv 2502.19405 | CLOSE |
| C1 | arXiv 2103.05633 | BEARS |
| C1 | arXiv 2606.21045 | BEARS |
| C1 | arXiv 2501.16007 | BEARS |
| C1 | arXiv 2608.11034 | BEARS |
| C1 | arXiv 2609.22087 | BEARS |
| C1 | arXiv 2511.02620 | BEARS |
| C1 | arXiv 2509.24257 | BEARS |
| C2 | Orseau, Armstrong, 'Safely Interruptible Agents', UAI 2016 | CLOSE |
| C2 | Orseau, Armstrong, 'Safely Interruptible Agents', UAI 2016 | CLOSE |
| C2 | arXiv 1611.08219 | BEARS/CLOSE |
| C2 | Soares, Fallenstein, Yudkowsky, Armstrong, 'Corrigibility',  | CLOSE |
| C2 | arXiv 2305.19861 | CLOSE |
| C2 | arXiv 2609.00109 | BEARS |
| C2 | arXiv 2606.08296 | BEARS |
| C3 | arXiv 2301.07733 | CLOSE |
| C3 | arXiv 2306.06101 | CLOSE |
| C3 | arXiv 2405.15682 | CLOSE |
| C3 | arXiv 2505.24005 | BEARS |
| C3 | arXiv 2605.07756 | CLOSE |
| C4 | arXiv 2609.22087 | STATES (E1+E2) |
| C4 | arXiv 2609.22087 | CLOSE (E2, E3) |
| C4 | arXiv 2608.11034 | BEARS |
| C5 | arXiv 2607.20519 | CLOSE |
| C5 | arXiv 2606.18206 | CLOSE |
| C5 | arXiv 1603.08983 | BEARS/CLOSE |
| C5 | arXiv 2107.05407 | BEARS/CLOSE |
| C5 | arXiv 2604.22110 | CLOSE |

Claims per tag: C1 9, C2 7, C3 5, C4 3, C5 5 (total 29 claims, 44 quotes).

For each candidate, the closest statements found in this sweep are listed below. The grading itself is left to `checks/grade_sweep.py`.

- **C1 (state-digest audit).** No fetched source states hashing the saved and the restored state to verify a pause or resume. Close forms: SHA-256 or Merkle commitments of checkpoints (weights; in Verde also the optimizer state), compared across two executions to audit training (2403.09603 v3; Verde 2502.19405 v1). PoL (2103.05633 v1) names weight hashing and rejects it because of re-execution error. 2609.22087 v1 asserts that the restored (θ, m) are byte-identical, but gives no digest check.
- **C2 (zero-stake pause).** Close forms: no learned incentive to prevent or seek interruption (Orseau & Armstrong 2016, through off-policy learning), utility indifference (Soares et al. 2015; Carey & Everitt 2023), and objective uncertainty (off-switch game). None states a valuation on the learner's own steps together with a lossless pause. 2609.00109 v2 ties the stake to the expected loss of an intervention.
- **C3 (tuning-free calibrated penalty weight).** Close forms remove the learning-rate or schedule sweep (D-Adaptation, Prodigy, Schedule-Free), or learn loss weights online at about 30% overhead (2605.07756 v1). 2505.24005 v1 states that learning-rate-free methods leave weight decay and regularisation untuned. No fetched source states a calibrated penalty weight for continual learning that removes the λ sweep.
- **C4 (empty-cut checklist).** 2609.22087 v1 states E1 and E2: full optimizer state, plus a schedule indexed on effective (active) time rather than wall-clock, makes a gap a no-op, with a proof sketch and two experiments. It treats E3 (the distribution drifting across the gap) as a cost regime, not as a checklist item, and it has no valuation or incentive component. Two on-topic engineering sources (Megatron-Bridge PR #6209, UniRL #499) were refused by the proxy.
- **C5 (own-clock cut: stop when the belief has settled).** Close forms: exit when consecutive predictions stop changing (predictive KL, a convergence readout; 2607.20519 v1), fixed-point halting (2606.18206 v1), and halting when the learned value of further belief refinement is near zero (2604.22110 v1). Canonical learned halting: ACT, PonderNet. None keys the halt to an accumulated own-clock arc.

## SEARCH LOG

Decision codes: INCLUDE; EXCLUDE (reason); DUPLICATE (of an included or listed item); QUALIFYING (on topic, not fetched or not included because of the cap).

### Q1. "proof of learning checkpoint hash verification"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 0 hits. URL: https://arxiv.org/search/?query=proof+of+learning+checkpoint+hash+verification&searchtype=all&abstracts=show&order=&size=25

- WebSearch: 9 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://www.emergentmind.com/topics/proof-of-learning-pol | Proof-of-Learning (PoL) [topic page] | EXCLUDE | aggregator, not primary |
| https://arxiv.org/pdf/2208.03567 | Proof-of-Learning is Currently More Broken Than You Think | EXCLUDE | outside window (2022); attacks on PoL |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12242945 | Apparatus and method for personalization of ML models (patent) | EXCLUDE | patent, off-topic |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11893464 | Apparatus and methods for training an educational ML model (patent) | EXCLUDE | patent, off-topic |
| https://arxiv.org/pdf/2505.12296 | PoLO: Proof-of-Learning and Proof-of-Ownership at Once with Chained Watermarking | QUALIFYING | watermark chain PoL; not fetched (cap) |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12278907 | Apparatus for secure multiparty computations for ML (patent) | EXCLUDE | patent, off-topic |
| https://www.weka.io/learn/glossary/ai-ml/ai-checkpoints/ | AI Checkpoints: How They Work and More | EXCLUDE | vendor glossary, not primary |
| https://arxiv.org/pdf/2110.11891 | On the Necessity of Auditable Algorithmic Definitions for Machine Unlearning | EXCLUDE | outside window; unlearning, off-topic |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12456052 | Systems and methods for verifiability of ML model unlearning (patent) | EXCLUDE | patent, off-topic |

### Q2. "verifiable training replay hash"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 1 hits. URL: https://arxiv.org/search/?query=verifiable+training+replay+hash&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2608.20097 | TrustRAG: Blockchain-Enhanced RAG via Committee-Based Credibility Scoring | 20 August, 2026 | EXCLUDE | RAG credibility, off-topic |

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://proceedings.neurips.cc//paper_files/paper/2024/hash/ad885a9caafff30ee9cafdf0ee42fda2-Abstract-Conference.html | Optimistic Verifiable Training by Controlling Hardware Nondeterminism (NeurIPS 2024) | DUPLICATE | of arXiv 2403.09603 (INCLUDED) |
| https://arxiv.org/pdf/2606.21045 | OVIG: Optimistic Verification of AI Training Integrity via Gradient Signals | INCLUDE | replay audit of training (C1) |
| https://commons.erau.edu/cgi/viewcontent.cgi?article=1944&context=edt | Enhancing Proof-of-Learning Security Against Spoofing (thesis) | QUALIFYING | PoL spoofing thesis; not fetched (cap) |
| https://arxiv.org/pdf/2403.09603 | Optimistic Verifiable Training by Controlling Hardware Nondeterminism | INCLUDE | hashed checkpoints in Merkle tree (C1) |
| https://github.com/TimoKruth/EvoNN-Research/pull/40 | Speed up checkpoint replay while preserving canonical hashes (PR) | EXCLUDE | github.com refused by proxy (403) |
| https://github.com/Ledger-Lenz/Ledgerlens-core/issues/936 | Add reproducibility harness for training runs (issue) | EXCLUDE | github.com refused by proxy (403) |
| https://arxiv.org/pdf/2601.00816 | MathLedger: A Verifiable Learning Substrate with Ledger-Attested Feedback | EXCLUDE | ledger-attested feedback, off-topic |
| https://arxiv.org/html/2508.12220v1 | Unlearning at Scale: Implementing the Right to be Forgotten in LLMs | QUALIFYING | replay-based unlearning; not fetched (cap) |
| https://www.professormesser.com/security-plus/sy0-601/sy0-601-video/replay-attacks-3/ | Replay Attacks (Security+ course) | EXCLUDE | off-topic |
| https://arxiv.org/pdf/2106.14253 | An efficient and secure scheme of verifiable computation for Intel SGX | EXCLUDE | outside window; off-topic |

### Q3. "verification of inference activations hashing"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 1 hits. URL: https://arxiv.org/search/?query=verification+of+inference+activations+hashing&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2510.25677 | ZK-SenseLM: Verifiable Large-Model Wireless Sensing with Selective Abstention and Zero-Knowledge Attestation | 14 January, 2026 | EXCLUDE | zk attestation of sensing, off-topic |

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://equilibrium.co/writing/state-of-verifiable-inference | State of Verifiable Inference & Future Directions | EXCLUDE | industry survey, not primary |
| https://arxiv.org/pdf/2501.16007 | TOPLOC: A Locality Sensitive Hashing Scheme for Trustless Verifiable Inference | INCLUDE | must-include; activation hashing (C1) |
| https://www.primeintellect.ai/blog/toploc | TOPLOC (blog) | DUPLICATE | of arXiv 2501.16007 |
| https://inference.net/blog/logic/ | LOGIC: Trustless Inference through Log-Probability Verification | QUALIFYING | vendor method page; not fetched (cap) |
| https://arxiv.org/pdf/2505.18398 | Towards Anonymous Neural Network Inference | EXCLUDE | anonymity, off-topic |
| https://github.com/netsky2-tech/omnifood-ni/issues/506 | activation verification sale never syncs (issue) | EXCLUDE | off-topic; github.com refused (403) |
| https://arxiv.org/pdf/2511.02620 | Verifying LLM Inference to Detect Model Weight Exfiltration | INCLUDE | inference verification (C1, bears) |
| https://arxiv.org/pdf/2509.24257 | VeriLLM: A Lightweight Framework for Publicly Verifiable Decentralized Inference | INCLUDE | hidden-state audit (C1, bears) |
| https://arxiv.org/pdf/1906.07148 | CheckNet: Secure Inference on Untrusted Devices | EXCLUDE | outside window (2019) |
| https://arxiv.org/html/2511.12592 | Knowledge is Overrated: zkML and hashing for inference at the LHC | EXCLUDE | trigger-physics zkML, off-topic |

### Q4. "safe interruptibility reinforcement learning"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 8 hits. URL: https://arxiv.org/search/?query=safe+interruptibility+reinforcement+learning&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2510.14503 | Learning to Undo: Rollback-Augmented Reinforcement Learning with Reversibility Signals | 16 October, 2025 | EXCLUDE | rollback in RL, not interruption |
| 2206.12065 | Eco-driving for Electric Connected Vehicles at Signalized Intersections: A Parameterized Reinforcement Learning approach | 7 October, 2022 | EXCLUDE | off-topic by title and abstract |
| 2106.05907 | DAIR: Disentangled Attention Intrinsic Regularization for Safe and Efficient Bimanual Manipulation | 6 October, 2021 | EXCLUDE | off-topic by title and abstract |
| 2106.00936 | Least-Restrictive Multi-Agent Collision Avoidance via Deep Meta Reinforcement Learning and Optimal Control | 2 June, 2021 | EXCLUDE | off-topic by title and abstract |
| 2007.03313 | Predictive Maintenance for Edge-Based Sensor Networks: A Deep Reinforcement Learning Approach | 7 July, 2020 | EXCLUDE | off-topic by title and abstract |
| 1805.11447 | Virtuously Safe Reinforcement Learning | 29 May, 2018 | EXCLUDE | outside window; interruptibility variant |
| 1711.09883 | AI Safety Gridworlds | 28 November, 2017 | EXCLUDE | outside window; benchmark environments only |
| 1704.02882 | Dynamic Safe Interruptibility for Decentralized Multi-Agent Reinforcement Learning | 22 May, 2017 | QUALIFYING | fetched; not included (cap) |

- WebSearch: 9 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://dl.acm.org/doi/10.5555/3294771.3294784 | Dynamic safe interruptibility for decentralized MARL (ACM) | DUPLICATE | of arXiv 1704.02882 |
| https://papers.nips.cc/paper/6618-dynamic-safe-interruptibility-for-decentralized-multi-agent-reinforcement-learning | Dynamic Safe Interruptibility (NeurIPS page) | DUPLICATE | of arXiv 1704.02882 |
| https://arxiv.org/pdf/1902.06766 | Parenting: Safe Reinforcement Learning from Human Input | EXCLUDE | outside window; human-input safe RL |
| https://intelligence.org/2016/06/01/new-paper-safely-interruptible-agents/ | New paper: Safely interruptible agents (MIRI blog) | INCLUDE | via the paper PDF (must-include) |
| https://arxiv.org/abs/1805.11447 | Virtuously Safe Reinforcement Learning | EXCLUDE | outside window; interruptibility variant |
| https://papers.nips.cc/paper_files/paper/2017/file/812b4ba287f5ee0bc9d43bbf5bbe87fb-Reviews.html | Reviews: Dynamic Safe Interruptibility | EXCLUDE | reviews, not primary |
| https://arxiv.org/pdf/1703.10284 | Enter the Matrix: Safely Interruptible Autonomous Systems via Virtualization | QUALIFYING | outside window (2017); not fetched (cap) |
| https://arxiv.org/pdf/1704.02882 | Dynamic Safe Interruptibility for Decentralized MARL | QUALIFYING | fetched; not included (cap) |
| https://proceedings.neurips.cc/paper/2017/file/812b4ba287f5ee0bc9d43bbf5bbe87fb-Paper.pdf | Dynamic Safe Interruptibility (proceedings PDF) | DUPLICATE | of arXiv 1704.02882 |

### Q5. "utility indifference shutdown"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 0 hits. URL: https://arxiv.org/search/?query=utility+indifference+shutdown&searchtype=all&abstracts=show&order=&size=25

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://arxiv.org/pdf/2305.19861 | Human Control: Definitions and Algorithms | INCLUDE | utility indifference analysed (C2) |
| https://arxiv.org/pdf/1709.06275 | Incorrigibility in the CIRL Framework | QUALIFYING | outside window (2017); not fetched (cap) |
| https://www.alignmentforum.org/posts/5bd75cc58225bf0670374f04/forum-digest-corrigibility-utility-indifference-and-related-control-ideas | Forum Digest: Corrigibility, utility indifference | EXCLUDE | forum digest, not primary |
| https://www.lesswrong.com/posts/iJofoQX7EjMFxDo6m/what-s-hard-about-the-shutdown-problem | What's Hard About The Shutdown Problem | EXCLUDE | forum post, not primary |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9135770 | Prediction of remaining utility usage via meter (patent) | EXCLUDE | off-topic |
| https://arxiv.org/pdf/1003.4118 | Indifference of Defaultable Bonds with Stochastic Intensity models | EXCLUDE | finance, off-topic |
| https://arxiv.org/pdf/1307.4591 | Utility indifference valuation for non-smooth payoffs | EXCLUDE | finance, off-topic |
| https://arxiv.org/pdf/1607.01110 | Utility Indifference Pricing of Insurance Catastrophe Derivatives | EXCLUDE | finance, off-topic |
| https://orf.od.nih.gov/TechnicalResources/ORFPolicies/Documents/POLICYANDPROCEDUREUTILITYSHUTDOWN508.pdf | Policy and procedure: utility shutdown (NIH) | EXCLUDE | facilities, off-topic |
| https://arxiv.org/pdf/2606.08296 | Revisiting the shutdown problem | INCLUDE | 2026 shutdown-problem review (C2) |

### Q6. "corrigibility pause incentive"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 0 hits. URL: https://arxiv.org/search/?query=corrigibility+pause+incentive&searchtype=all&abstracts=show&order=&size=25

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://www.alignmentforum.org/posts/d7jSrBaLzFLvKgy32/4-existing-writing-on-corrigibility | 4. Existing Writing on Corrigibility | EXCLUDE | forum post, not primary |
| https://www.alignmentforum.org/s/KfCjeconYRdFbMxsy/p/d7jSrBaLzFLvKgy32 | Alignmentforum (same post) | DUPLICATE | forum post |
| https://arxiv.org/pdf/1908.01695 | Corrigibility with Utility Preservation | QUALIFYING | outside window (2019); not fetched (cap) |
| https://www.alignmentforum.org/posts/HLns982j8iTn7d2km/defining-corrigible-and-useful-goals | Defining Corrigible and Useful Goals | EXCLUDE | forum post, not primary |
| https://www.alignmentforum.org/posts/fkLYhTQteAu5SinAc/corrigibility | Corrigibility (forum) | EXCLUDE | forum post, not primary |
| https://intelligence.org/files/Corrigibility.pdf | Corrigibility (Soares et al. 2015) | INCLUDE | canonical utility indifference (C2) |
| https://www.lesswrong.com/posts/WCX3EwnWAx7eyucqH/corrigibility-can-be-vnm-incoherent | Corrigibility can be VNM-incoherent | EXCLUDE | forum post, not primary |
| https://www.lesswrong.com/w/corrigibility-1 | Corrigibility (wiki) | EXCLUDE | wiki, not primary |
| https://arxiv.org/pdf/2006.04948 | AI Research Considerations for Human Existential Safety (ARCHES) | EXCLUDE | outside window; survey |
| https://arxiv.org/pdf/2609.00109 | The Veto Variable: Human Override as a Goal-Independent Cost Term | INCLUDE | 2026 oversight-stake analysis (C2) |

### Q7. "hyperparameter-free regularization weight"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 16 hits. URL: https://arxiv.org/search/?query=hyperparameter-free+regularization+weight&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2609.10892 | DriftNet: A Dual-Head Trajectory Transformer for Detecting and Localizing Prompt Injection in LLM Agents | 9 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.27725 | GA-Agent: Large Language Models as Hyperparameter Optimizers for Evolutionary Controller Synthesis | 23 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.22688 | GARIP: A Running-Average Moving Reference for Last-Iterate Self-Play in Two-Player Zero-Sum Games | 21 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.25939 | From Latent Space to Training Data: Explainable Specialization in Minimal MLPs | 25 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.29380 | TRACER: Persistent Regularization for Robust Multimodal Finetuning | 28 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.25604 | DVAO: Dynamic Variance-adaptive Advantage Optimization for Multi-reward Reinforcement Learning | 25 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2602.18116 | Cut Less, Fold More: Model Compression through the Lens of Projection Geometry | 20 February, 2026 | EXCLUDE | off-topic by title and abstract |
| 2510.26121 | Uncertainty-Aware Diagnostics for Physics-Informed Machine Learning | 30 October, 2025 | EXCLUDE | off-topic by title and abstract |
| 2506.13239 | Restarted contractive operators to learn at equilibrium | 16 June, 2025 | EXCLUDE | off-topic by title and abstract |
| 2410.05270 | CLIP's Visual Embedding Projector is a Few-shot Cornucopia | 26 January, 2026 | EXCLUDE | off-topic by title and abstract |
| 2402.01379 | Regularized boosting with an increasing coefficient magnitude stop criterion as meta-learner in hyperparameter optimization stacking ensemble | 2 February, 2024 | EXCLUDE | HPO stop criterion, off-topic |
| 2211.04453 | Automated discovery of generalized standard material models with EUCLID | 26 October, 2022 | EXCLUDE | off-topic by title and abstract |
| 2107.06916 | Training Compact CNNs for Image Classification using Dynamic-coded Filter Fusion | 18 December, 2022 | EXCLUDE | off-topic by title and abstract |
| 2103.17032 | Weighted SPICE Algorithms for Range-Doppler Imaging Using One-Bit Automotive Radar | 31 March, 2021 | EXCLUDE | off-topic by title and abstract |
| 1712.02840 | Learning Free Energy Landscapes Using Artificial Neural Networks | 7 December, 2017 | EXCLUDE | off-topic by title and abstract |
| 1505.01461 | Online Hyperparameter-Free Sparse Estimation Method | 6 May, 2015 | EXCLUDE | outside window; sparse estimator |

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://arxiv.org/pdf/2105.00925 | Hyperspherically Regularized Networks for Self-Supervision | EXCLUDE | off-topic |
| https://arxiv.org/pdf/2505.24005 | How far away are truly hyperparameter-free learning algorithms? | INCLUDE | hyperparameter-free status (C3) |
| https://arxiv.org/pdf/2306.16993 | Weight Compander: A Simple Weight Reparameterization for Regularization | EXCLUDE | outside window (2023); reparameterisation |
| https://medium.com/@tm2761/regularization-hyperparameter-tuning-in-a-neural-network-f77c18c36cd3 | Regularization: Hyperparameter tuning (Medium) | EXCLUDE | blog, not primary |
| https://arxiv.org/pdf/2208.14133 | Deep Generative Modeling on Limited Data with Regularization | EXCLUDE | outside window; off-topic |
| https://medium.com/@krushnakr9/deep-learning-hyperparameter-tuning-regularization-and-optimization-e1a8a9ba532b | Deep Learning: Hyperparameter tuning (Medium) | EXCLUDE | blog, not primary |
| https://arxiv.org/pdf/2311.08239 | Learning Physics-Inspired Regularization for Medical Image Registration with Hypernetworks | EXCLUDE | outside window; registration domain |
| https://towardsdatascience.com/the-what-why-and-how-of-hyperparameter-tuning-for-machine-learning-models-1a2634e9ca9e/ | The what, why, and how of hyperparameter tuning | EXCLUDE | blog, not primary |
| https://www.exxactcorp.com/blog/deep-learning-ai/maximizing-ai-efficiency-tuning-and-regulation | Hyperparameter Tuning & Regularization (Exxact) | EXCLUDE | vendor blog, not primary |
| https://machinelearningmastery.com/how-to-reduce-overfitting-in-deep-learning-with-weight-regularization/ | How to Use Weight Decay (MLM) | EXCLUDE | tutorial, not primary |

### Q8. "tuning-free loss weighting"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 25 hits (of 87). URL: https://arxiv.org/search/?query=tuning-free+loss+weighting&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2609.16145 | Safe Error Correction for Language Models: Frozen-Base Adjustment with Capability Preservation | 14 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.02089 | IDEEA: training-free Input-Dependent stEEring via Activation cluster matching | 2 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.25014 | Not All 4-bit Quantizers Are Equal: Deployment-Time Mitigation of PII Leakage in Fine-Tuned Small Language Models | 2 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.02480 | Private Generative Bootstrap via Blocking | 3 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.11505 | Does a Structural Model Add Anything to the Closing Price? Calibrated forecasting, incremental information, and match leverage in the Italian Serie A | 11 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.14649 | Discrete Diffusion Language Models Are Training-Free Multi-Label Classifiers | 30 July, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.24026 | NeurRAFT: Robot Motion Planning via Anchor-Level Flow Matching with Clearance-Aware Preference Tuning | 24 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.12274 | A Neighborhood Attention Transformer Network for Enhanced 3D Segmentation of the Left Anterior Descending Artery | 12 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.05100 | Lesion Detection in CT with Frozen Self-Distilled Features: SALT, a Spatially Adaptive Label-Guided Temperature | 5 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2608.04084 | SpecDrop: Parameter-Free Category-Conditioned Routing for Modular Specialization | 4 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2607.26498 | HERMES: A Hybrid Ensemble for Head-and-Neck Tumor Segmentation, TN Staging, and Recurrence-Free Survival on PET/CT | 3 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2607.22077 | The Lift Spectrum: How Measurement-to-Space Adaptivity Shapes Robustness in Image-Free Single-Pixel Sensing | 10 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.29027 | A Mass, Momentum, and Energy Conserving Semi-Lagrangian Adaptive-Rank (SLAR) Method for the Vlasov-Poisson System | 27 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.14181 | Robin-Neumann Coupling of PINN and FEM Solvers: A Steklov-Poincaré View, with Application to Fluid-Structure Interaction with Contact | 12 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.26587 | SharQ: Bridging Activation Sparsity and FP4 Quantization for LLM Inference | 25 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.27771 | NormGuard: Reward-Preserving Norm Constraints in Flow-Matching Reinforcement Learning | 5 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.07207 | Entropy as a Structural Prior: How a Log-Barrier on DiT Belief Space Drives Musical Diversity and Development | 5 June, 2026 | EXCLUDE | diffusion confidence weighting, off-topic |
| 2606.31796 | CHERRY: Compressed Hierarchical Experts with Recurrent Representational Yield | 23 July, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.01928 | Training Non-Differentiable Networks via Optimal Transport | 21 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.11654 | Weather-Robust Cross-View Geo-Localization via Prototype-Based Semantic Part Discovery | 18 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.23391 | Coupling-Robust Accuracy in Multiphysics Physics Informed Neural Networks via Kronecker-Preconditioned Optimization | 14 August, 2026 | EXCLUDE | PINN loss balancing, domain-specific |
| 2604.14651 | CURA: Clinical Uncertainty Risk Alignment for Language Model-Based Risk Prediction | 23 April, 2026 | EXCLUDE | off-topic by title and abstract |
| 2604.01502 | Conformal Risk Control under Non-Monotone Losses: Theory and Finite-Sample Guarantees | 17 April, 2026 | EXCLUDE | off-topic by title and abstract |
| 2603.17685 | Flow Matching Policy Optimization with Mirror Descent and Entropy Constraints | 26 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2603.19561 | An Adaptive Machine Learning Framework for Fluid Flow in Dual-Network Porous Media | 23 September, 2026 | EXCLUDE | off-topic by title and abstract |

- WebSearch: 9 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://arxiv.org/pdf/2009.01717 | Multi-Loss Weighting with Coefficient of Variations | QUALIFYING | outside window (2020); not fetched (cap) |
| https://www.emergentmind.com/topics/weighted-loss-functions | Weighted Loss Functions: Theory and Practice | EXCLUDE | aggregator, not primary |
| https://arxiv.org/pdf/2402.00518 | EE-Tuning: tuning early-exit LLMs | EXCLUDE | early-exit fine-tuning, off-topic |
| https://arxiv.org/pdf/2605.07756 | When Losses Align: Gradient-Based Composite Loss Weighting for Efficient Pretraining | INCLUDE | online loss weights vs sweep (C3) |
| https://arxiv.org/html/2502.02797v1 | Upweighting Easy Samples in Fine-Tuning Mitigates Forgetting | QUALIFYING | parameter-free sample weighting; not fetched (cap) |
| https://medium.com/@syedasilalinaqvi/dynamic-loss-weighting-in-keras-fine-tuning-model-training-with-adaptive-loss-weights-207aa3fc388f | Dynamic Loss Weighting in Keras (Medium) | EXCLUDE | blog, not primary |
| https://direct.mit.edu/tacl/article/doi/10.1162/TACL.a.42/133798/On-the-Effect-of-Instruction-Tuning-Loss-on-Generalization | On the Effect of Instruction Tuning Loss on Generalization | EXCLUDE | instruction-loss masking, off-topic |
| https://arxiv.org/pdf/2008.01478 | Learning Interpretable Microscopic Features of Tumor | EXCLUDE | off-topic |
| https://www.researchgate.net/publication/386203269_Instruction_Fine-Tuning_Does_Prompt_Loss_Matter | Instruction Fine-Tuning: Does Prompt Loss Matter? | EXCLUDE | off-topic |

### Q9. "learning-rate-free optimizer"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 25 hits (of 750). URL: https://arxiv.org/search/?query=learning-rate-free+optimizer&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2609.00771 | Non-Prehensile Throwing: A Reinforcement Learning Perspective | 1 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.02089 | IDEEA: training-free Input-Dependent stEEring via Activation cluster matching | 2 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.02964 | When Optimization Becomes Manipulation: Defending Generative Search against Malicious Generative Engine Optimization | 2 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.01930 | Quantum-Based k-Coverage Optimization for UAV-Aided Search and Rescue Missions | 1 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.09075 | ThinkPrior: Zero-Rollout Difficulty Priors for Cold-Start Prompt Selection in RLVR | 11 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.09776 | Proof-Carrying Cognition: Closing the Verification Gap with Reality-Settled Reward | 9 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.05856 | Transformation of Adaptive Multistage Sampling for Solving Finite-Horizon Markov Decision Processes with Unknown Model | 4 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.20174 | Robust Federated Q-Learning with Almost No Communication | 24 August, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.00870 | Stochastic Optimization of Tree Tensor Networks | 1 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.03645 | Calibration of neural viscoelastic models via full-field data | 3 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.03762 | Projected Riemannian Gradient Descent for the Bures-Wasserstein Barycenter: Dimension-Independent Linear Convergence at Unit Step Size | 3 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.01126 | When Does Online Adaptation Pay on the Edge? A Leakage-Free Evaluation of Warmup, Learning-Rate Selection, and Resource Trade-offs for Time-Series Forecasting | 1 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.22087 | When Is Availability-Aware Training Worth It? A Benchmark and Empirical Study of Interruption-Resilient Optimization Under Predictable Compute Schedules | 22 June, 2026 | INCLUDE | interruption-resilient training (C4, C1) |
| 2609.22041 | $λ$-Controlled GRPO: Turning Flow-Matching Ratio Instability into a Budgeted Resource | 21 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.05832 | CR-VLA-Force: Learning Control-aware Compliance VLA Model for Robust Contact-rich Robotic Manipulation | 4 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.18782 | A Convergence Framework for Deep $V$-Learning: Error Propagation and Sharp Action-Gap Bounds | 16 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.14373 | Low-Complexity Near-Field Channel Estimation and Subcarrier-Cooperative Hybrid Precoding for Wideband XL-MIMO OFDM Systems | 13 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.13235 | Learning Manipulation-Sufficient Representations via Outcome Bottlenecks | 2 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.13231 | ShieldVLA: Feasibility-Aware Safety Alignment for Vision-Language-Action Models | 2 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.23189 | Entangled measurements are necessary for optimal tomography of mixed fermionic Gaussian states and of bosonic Gaussian states near the vacuum | 19 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.20784 | RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning | 17 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.03657 | Rethinking 3D Noise: Learning 3D-Aware Video Priors via Optimization-Free Morphological Perturbations | 3 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.01961 | MACAW: Reliable And Efficient Surgical Debridement Using Monocular Adaptive Compact Attention Windows | 1 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.13922 | Minibatch persistency, eight years later: what batch reuse costs in steps and joules, and what it saves in data | 12 September, 2026 | EXCLUDE | data-reuse study, not LR-free |
| 2609.23127 | Provably Efficient Reinforcement Learning in Continuous-Time Episodic MDPs with Poisson Decision Epochs | 19 September, 2026 | EXCLUDE | off-topic by title and abstract |

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://medium.com/syncedreview/samsung-meta-ais-adaptive-parameter-free-learning-rate-method-matches-hand-tuned-adam-optimizer-c2a68cb6e31f | Samsung & Meta AI's Parameter-Free LR Method (SyncedReview) | EXCLUDE | news, not primary |
| https://arxiv.org/pdf/2308.03102 | Learning-Rate-Free Learning: Dissecting D-Adaptation and Probabilistic Line Search | EXCLUDE | outside window (2023); secondary analysis |
| https://ai.meta.com/research/publications/learning-rate-free-learning-by-d-adaptation/ | Learning-Rate-Free Learning by D-Adaptation (Meta page) | DUPLICATE | of arXiv 2301.07733 |
| https://arxiv.org/pdf/2603.25471 | Advancing weak lensing mass mapping with a mask-aware HEALPix transformer | EXCLUDE | off-topic |
| https://arxiv.org/pdf/2306.06101 | Prodigy: An Expeditiously Adaptive Parameter-Free Learner | INCLUDE | must-include (C3) |
| https://www.biorxiv.org/content/10.1101/348557.full.pdf | Hyperparameter-free optimizer of SGD with unit correction | EXCLUDE | outside window (2018) |
| https://arxiv.org/abs/2301.07733 | Learning-Rate-Free Learning by D-Adaptation | INCLUDE | must-include (C3) |
| https://arxiv.org/abs/2406.02296 | Learning-Rate-Free Stochastic Optimization over Riemannian Manifolds | QUALIFYING | in window; not fetched (cap) |
| https://link.springer.com/article/10.1007/s10915-025-02798-0 | Learning-Rate-Free Momentum SGD with Reshuffling (J Sci Comput) | QUALIFYING | in window; not fetched (cap) |
| https://github.com/facebookresearch/schedule_free | Schedule-Free Optimization in PyTorch (repo) | EXCLUDE | github.com refused (403); paper 2405.15682 INCLUDED |

### Q10. "checkpoint resume correctness bug"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 0 hits. URL: https://arxiv.org/search/?query=checkpoint+resume+correctness+bug&searchtype=all&abstracts=show&order=&size=25

- WebSearch: 9 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://github.com/Tencent-Hunyuan/UniRL/issues/499 | [Bug] Checkpoint resume rejects valid partially initialized AdamW state | EXCLUDE | on-topic by snippet; github.com refused (403) |
| https://github.com/cockroachdb/cockroach/issues/174963 | importer: job restart resets checkpointed resume positions | EXCLUDE | database job; github.com refused (403) |
| https://github.com/TaewoooPark/Motifcode/issues/18 | Restore checkpoint state when resuming in print mode | EXCLUDE | agent tool; github.com refused (403) |
| https://github.com/aegra/aegra/issues/558 | run.start rejects checkpoint-only resume | EXCLUDE | agent framework; github.com refused (403) |
| https://dev.to/hexisteme/the-checkpoint-remembered-the-result-not-the-request-4nfo | The Checkpoint Remembered the Result, Not the Request | EXCLUDE | blog post, not primary |
| https://github.com/BelfordZ/open-rpc-flow/issues/158 | Design: durable checkpoints exportState/importState | EXCLUDE | off-topic; github.com refused (403) |
| https://github.com/NVIDIA-NeMo/Megatron-Bridge/pull/6209 | fix(ckpt): sync training resume state and compatibility fixes | EXCLUDE | on-topic by snippet; github.com refused (403) |
| https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5421003 | Disk storage system with fault tolerant media maintenance (patent) | EXCLUDE | off-topic |
| https://github.com/petry-projects/.github-private/issues/1706 | Action budget: resume from a checkpoint on re-dispatch | EXCLUDE | off-topic; github.com refused (403) |

### Q11. "silent data corruption checkpoint"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 3 hits. URL: https://arxiv.org/search/?query=silent+data+corruption+checkpoint&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2608.11034 | SCOUT: Symmetric Consensus Outlier Detection for Failure Localization in LLM Pre-Training | 11 August, 2026 | INCLUDE | checkpoint certification under SDC (C1, C4) |
| 2607.20952 | The Weight of Silence: A Causal Case for Weights Over the Scratchpad in Latent Chess Reasoning | 27 July, 2026 | EXCLUDE | off-topic by abstract |
| 1310.8486 | On the Combination of Silent Error Detection and Checkpointing | 31 October, 2013 | EXCLUDE | outside window; HPC checkpoint scheduling |

- WebSearch: 9 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://www.opencompute.org/documents/sdc-in-ai-ocp-whitepaper-final-pdf | Silent Data Corruption in AI (OCP whitepaper) | EXCLUDE | on-topic; HTTP 403 (curl and WebFetch) |
| https://support.google.com/cloud/answer/10759085?hl=en | Silent Data Corruption (Google Cloud help) | EXCLUDE | help page, not primary |
| https://info.ornl.gov/sites/publications/files/Pub36913.pdf | Detection and Correction of SDC for Large-Scale HPC | EXCLUDE | outside window (HPC, 2012) |
| https://bugs.launchpad.net/bugs/613244 | silent data corruption with checkpoint/restore (Duplicity) | EXCLUDE | backup tool bug, off-topic |
| https://arxiv.org/pdf/1511.04478 | A Backward/Forward Recovery Approach for PCG | EXCLUDE | outside window; numerical solver |
| https://dl.acm.org/doi/10.1145/2802658.2802665 | Detecting SDC for Extreme-Scale MPI Applications | EXCLUDE | outside window (2015) |
| https://www.researchgate.net/publication/220782867_Detection_and_correction_of_silent_data_corruption_for_large-scale_high-performance_computing | Detection and correction of SDC (ResearchGate) | DUPLICATE | of ORNL paper |
| https://arxiv.org/pdf/1404.5552 | Tolerating Silent Data Corruption in Opaque Preconditioners | EXCLUDE | outside window; numerical solver |
| https://www.osti.gov/servlets/purl/1110355 | Detection and Correction of SDC (OSTI) | DUPLICATE | of ORNL paper |

### Q12. "adaptive computation halting"

- arXiv API: FAILED (empty body on the attempt and the retry; http 301 to https, https HTTP 406).
- arXiv listing search (fallback): 25 hits (of 72). URL: https://arxiv.org/search/?query=adaptive+computation+halting&searchtype=all&abstracts=show&order=&size=25

| id | title | date (submitted) | decision | reason |
|---|---|---|---|---|
| 2609.00237 | Learning What to Retain: Gated-Memory Routing for Efficient Collaboration in Multi-Agent LLM Systems | 9 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.13807 | Bypass Observation: A Conceptual Design of a Non-Intrusive Layer-Wise Semantic Extraction Architecture | 12 September, 2026 | EXCLUDE | off-topic by title and abstract |
| 2609.03379 | RecurTrace: Adaptive Latent Reasoning with Loop-Time Memory | 10 September, 2026 | QUALIFYING | adaptive latent recurrence; not fetched (cap) |
| 2608.22347 | Where Cognition Lives: Dissecting Emergent from Computed Function in a Minimal Complete Cognitive Architecture | 23 August, 2026 | QUALIFYING | adaptive halting; not fetched (cap) |
| 2608.05217 | A Survey of Adversarial Efficiency Degradation for Vision Transformer by Exploiting Input-adaptive Optimization | 5 August, 2026 | EXCLUDE | attacks on adaptive inference; survey |
| 2607.05051 | Listen, Think, Transcribe: Continuous Latent Test-Time Scaling for ASR | 6 July, 2026 | EXCLUDE | off-topic by title and abstract |
| 2607.08775 | HALO: Hybrid Adaptive Latent Reasoning for Language Models | 3 May, 2026 | QUALIFYING | adaptive refinement steps; not fetched (cap) |
| 2607.20519 | Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts | 7 July, 2026 | INCLUDE | convergence-readout halting (C5) |
| 2607.22769 | DomainPilot: Domain-Level Loss-Guided Two-Stage Data Mixture Optimization for Efficient Language Model Fine-Tuning | 23 July, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.03739 | Entropy Gate: Entropy Quenching for Near-Lossless Token Compression in LLM Pipelines | 2 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.03811 | AI Agents Enable Adaptive Computer Worms | 2 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.10706 | Unifying Data, Memory, and Compute Efficiency in LLM training: A Survey | 9 June, 2026 | EXCLUDE | off-topic by title and abstract |
| 2606.18206 | Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers | 16 June, 2026 | INCLUDE | fixed-point halting (C5) |
| 2606.24074 | Token Complexity of Certifying Stochastic-Oracle Reliability | 22 June, 2026 | EXCLUDE | oracle token complexity, off-topic |
| 2605.05222 | Adaptive Computation Depth via Learned Token Routing in Transformers | 17 April, 2026 | QUALIFYING | learned token depth; not fetched (cap) |
| 2605.05561 | BitCal-TTS: Bit-Calibrated Test-Time Scaling for Quantized Reasoning Models | 6 May, 2026 | EXCLUDE | test-time budget allocation, not halting |
| 2605.03743 | A Workflow-Oriented Framework for Asynchronous Human-AI Collaboration in Hybrid and Compute-Intensive HPC Environments | 5 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.28919 | CosmicFish-HRM: Adaptive Reasoning via Hierarchical Recurrent Mechanisms in Compact Language Models | 27 May, 2026 | QUALIFYING | adaptive reasoning depth; not fetched (cap) |
| 2605.05863 | SOPE: Stabilizing Off-Policy Evaluation for Online RL with Prior Data | 20 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.03999 | RD-ViT: Recurrent-Depth Vision Transformer for Semantic Segmentation with Reduced Data Dependence Extending the Recurrent-Depth Transformer Architecture to Dense Prediction | 5 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2605.02442 | Measuring AI Reasoning: A Guide for Researchers | 4 May, 2026 | EXCLUDE | off-topic by title and abstract |
| 2604.22110 | Do Not Imitate, Reinforce: Iterative Classification via Belief Refinement | 23 April, 2026 | INCLUDE | belief-refinement halting (C5) |
| 2604.21999 | Universal Transformers Need Memory: Depth-State Trade-offs in Adaptive Recursive Reasoning | 3 May, 2026 | QUALIFYING | ACT variant; not fetched (cap) |
| 2603.28565 | StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation | 30 March, 2026 | EXCLUDE | off-topic by title and abstract |
| 2603.24597 | Algorithmic Barriers to Detecting and Repairing Structural Overspecification in Adaptive Data-Structure Selection | 9 March, 2026 | EXCLUDE | off-topic by title and abstract |

- WebSearch: 10 hits.

| URL | title | decision | reason |
|---|---|---|---|
| https://arxiv.org/pdf/2601.19551 | Scale-Consistent State-Space Dynamics via Fractal of Stationary Transformations | EXCLUDE | off-topic by abstract |
| https://www.emergentmind.com/topics/adaptive-computational-time-act | Adaptive Computational Time (ACT) [topic page] | EXCLUDE | aggregator, not primary |
| https://www.emergentmind.com/topics/dynamic-halting-mechanisms | Dynamic Halting Mechanisms in Computation [topic page] | EXCLUDE | aggregator, not primary |
| https://arxiv.org/pdf/2301.13195 | Adaptive Computation with Elastic Input Sequence | EXCLUDE | outside window (Jan 2023) |
| https://www.emergentmind.com/topics/adaptive-computation-time-act | Adaptive Computation Time (ACT) [topic page] | EXCLUDE | aggregator, not primary |
| https://arxiv.org/pdf/2607.20519 | Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts | INCLUDE | convergence-readout halting (C5) |
| https://www.emergentmind.com/topics/dynamic-halting-mechanism | Dynamic Halting Mechanism [topic page] | EXCLUDE | aggregator, not primary |
| https://arxiv.org/pdf/2505.14467 | Void in Language Models | EXCLUDE | off-topic |
| https://arxiv.org/pdf/2603.04180 | Architectural Proprioception in SSMs: Anticipatory Halt Detection | QUALIFYING | halt detection; not fetched (cap) |
| https://arxiv.org/pdf/2603.22871 | Dynamical Systems Theory Behind a Hierarchical Reasoning Model | QUALIFYING | HRM halting dynamics; not fetched (cap) |

### Added by title (must-include or canonical cited)

| id / URL | title | reason |
|---|---|---|
| 2103.05633 | Proof-of-Learning: Definitions and Practice | must-include; not in any query hit list |
| 2502.19405 | Verde: Verification via Refereed Delegation for ML Programs | must-include; not in any query hit list |
| 1611.08219 | The Off-Switch Game | must-include; not in any query hit list |
| 2405.15682 | The Road Less Scheduled (Schedule-Free) | must-include; q9 web hit was the github repo (403) |
| https://intelligence.org/files/Interruptibility.pdf | Safely Interruptible Agents (UAI 2016) | must-include; q4 web hit was the MIRI announcement |
| 1603.08983 | Adaptive Computation Time for RNNs | canonical; cited by 2604.22110 and 2607.20519 |
| 2107.05407 | PonderNet: Learning to Ponder | canonical; cited by 2604.22110 and 2607.20519 |

Totals: 12 queries; 104 arXiv listing hits and 115 WebSearch hits screened; 25 sources included, and 44 quotes found out of 44.
