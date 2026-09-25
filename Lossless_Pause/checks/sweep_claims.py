"""Claims from the systematic sweep of 2026-09-25 (Lossless_Pause/DECLARATION_2.md), transcribed from
docs/citations/sweep_{prior_art,transformer_state,energy_carbon}_2026-09-25.md (raw texts in the session scratchpad
sweep/<family>/). 'reading' for candidate tags C1-C5 is the investigator's reading (states / close / bears), decided after
reading the quotes; topic-tagged claims read 'topic'. Verified verbatim by checks/verify_claims.py sweep_claims.
"""

CLAIMS = [{'id': 'prior_art:0',
  'tag': 'C1',
  'reading': 'close',
  'source': "Srivastava, Arora, Boneh, 'Optimistic Verifiable Training by Controlling Hardware Nondeterminism', "
            'NeurIPS 2024, arXiv 2403.09603',
  'version': 'arXiv 2403.09603v3 (25 Nov 2024)',
  'url': 'https://arxiv.org/abs/2403.09603v3',
  'quote': ['The game’s efficiency lies in our ability to store hashes of model checkpoints in a Merkle tree [Merkle, '
            '1988]. To determine if training was performed according to the specification, the auditor needs to '
            'reconstruct the Merkle tree and compare the resulting Merkle root hash with the Merkle root hash provided '
            'by the trainer’s',
            'the auditor can store the hashsha256(θ) of model weightsθ in a Merkle tree at intervalk, knowing that if '
            'training was done correctly, the model weights should be identical to the trainer’s at any timestep.'],
  'raw_file': 'prior_art/optimistic_vt.txt',
  'agent_note': 'CLOSE: hashes (sha256) of model weights at an interval, stored in a Merkle tree, are compared between '
                'trainer and auditor to verify that training followed the specification. Difference from C1: an audit '
                'of a whole training trajectory by independent re-execution (with rounding logs to force identical '
                'weights across GPUs), not the check that a pause/resume restored the saved state; hashed object is '
                'the weights.'},
 {'id': 'prior_art:1',
  'tag': 'C1',
  'reading': 'close',
  'source': "Arun et al., 'Verde: Verification via Refereed Delegation for Machine Learning Programs', arXiv "
            '2502.19405',
  'version': 'arXiv 2502.19405v1 (26 Feb 2025)',
  'url': 'https://arxiv.org/abs/2502.19405v1',
  'quote': ['it suffices for now to assume that the checkpoint consists of just the aforementioned state and is '
            'committed to using a standard collision-resistant hash function like SHA-256.',
            'hashing the weights and Adam optimizer state (Kingma & Ba, 2014) (the optimizer state is double the size '
            'of the weights alone) in FP32 precision for DistilBERT (66 million parameters) takes under a second, for '
            'Llama-1B takes around 2.5 seconds, and for Llama-8B around 15 seconds'],
  'raw_file': 'prior_art/verde.txt',
  'agent_note': 'CLOSE: a training checkpoint (weights and optimizer state) is committed with SHA-256 and two '
                'executions are compared by checkpoint hash to find the first diverging step. Difference from C1: '
                'dispute resolution between two trainers re-executing the same program (bitwise reproducible '
                "operators), not verification of one learner's pause/resume."},
 {'id': 'prior_art:2',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Jia, Yaghini, Choquette-Choo, Dullerud, Thudi, Chandrasekaran, Papernot, 'Proof-of-Learning: Definitions "
            "and Practice', IEEE S&P 2021, arXiv 2103.05633",
  'version': 'arXiv 2103.05633v1 (9 Mar 2021)',
  'url': 'https://arxiv.org/abs/2103.05633v1',
  'quote': ['follow up work may consider hashing weights sequentially utilizing Merkle tree structure [85], i.e. each '
            'consecutive set of weights during the training procedure are hashed and then saved as the hash of the '
            'concatenation of the current weights and the previously saved hash. We do not use Merkle trees due to the '
            'error accumulated when the veriﬁer reconstructs the weights: the error in the weights forces the weights '
            'of the veriﬁer and legitimate worker to hash to different values, losing the ability'],
  'raw_file': 'prior_art/jia2021_pol.txt',
  'agent_note': 'BEARS: Proof-of-Learning verifies logged checkpoints by re-executing steps and comparing weights '
                'within a tolerance; it names hashing weights in a Merkle chain and rejects it because re-execution '
                'error makes honest weights hash differently. Neither states hashing to verify a pause/resume.'},
 {'id': 'prior_art:3',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Su, Yao, Zhang, Wang, Viswanath, 'OVIG: Optimistic Verification of AI Training Integrity via Gradient "
            "Signals', arXiv 2606.21045",
  'version': 'arXiv 2606.21045v1 (19 Jun 2026)',
  'url': 'https://arxiv.org/abs/2606.21045v1',
  'quote': ['Exact comparison is straightforward only when honest replay is bitwise reproducible. Modern accelerator '
            'training rarely has this property.',
            'The key point is that OVIG does not try to prove bitwise equality of an entire training trajectory.'],
  'raw_file': 'prior_art/ovig.txt',
  'agent_note': 'BEARS: replay-based training audit that explicitly does not rely on bitwise (hash-level) equality; '
                'uses a calibrated gradient-error boundary instead. Bears on when a state digest can serve as the '
                'check (only where replay is bit-exact).'},
 {'id': 'prior_art:4',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Ong et al., 'TOPLOC: A Locality Sensitive Hashing Scheme for Trustless Verifiable Inference', arXiv "
            '2501.16007',
  'version': 'arXiv 2501.16007v2 (30 May 2025)',
  'url': 'https://arxiv.org/abs/2501.16007v2',
  'quote': ['The method performs locality-sensitive hashing of the intermediate activations, which encodes the top-k '
            'values and indices as a polynomial congruence.'],
  'raw_file': 'prior_art/toploc.txt',
  'agent_note': 'BEARS: hashes intermediate activations (a locality-sensitive, tolerance-bearing hash) to verify '
                'inference; it verifies computation through activations/outputs, not a saved-versus-restored state '
                'digest.'},
 {'id': 'prior_art:5',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Wang, 'SCOUT: Symmetric Consensus Outlier Detection for Failure Localization in LLM Pre-Training', arXiv "
            '2608.11034',
  'version': 'arXiv 2608.11034v1 (11 Aug 2026)',
  'url': 'https://arxiv.org/abs/2608.11034v1',
  'quote': ['Clean replay coverage certifies checkpoint numerical integrity, preventing recovery from selecting state '
            'corrupted by SDC.'],
  'raw_file': 'prior_art/scout.txt',
  'agent_note': 'BEARS: certifies checkpoints for recovery by in-situ replay consensus across ranks (SDC detection), '
                'not by hashing saved against restored state.'},
 {'id': 'prior_art:6',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Mitra, 'When Is Availability-Aware Training Worth It? A Benchmark and Empirical Study of "
            "Interruption-Resilient Optimization Under Predictable Compute Schedules', arXiv 2609.22087",
  'version': 'arXiv 2609.22087v1 (22 Jun 2026)',
  'url': 'https://arxiv.org/abs/2609.22087v1',
  'quote': ['On resume,(θ,m )are byte-identical to their pre-gap values and ηk = ηschedule(teff)is unchanged because '
            'teff counts active time only. Hence each post-gap update is function-identical to the corresponding '
            'continuous-training update.'],
  'raw_file': 'prior_art/availability_training.txt',
  'agent_note': 'BEARS: asserts byte-identity of restored (θ, m) as the premise of a proof sketch that a gap is a '
                'no-op; no digest or hash audit of the restore is stated.'},
 {'id': 'prior_art:7',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Rinberg, Karvonen, Hoover, Reuter, Warr, 'Verifying LLM Inference to Detect Model Weight Exfiltration', "
            'arXiv 2511.02620',
  'version': 'arXiv 2511.02620v3 (12 Mar 2026)',
  'url': 'https://arxiv.org/abs/2511.02620v3',
  'quote': ['This work investigates how toverifyLLM model inference to defend against such attacks and, more broadly, '
            'to detect anomalous or buggy behavior during inference.'],
  'raw_file': 'prior_art/weight_exfil.txt',
  'agent_note': 'BEARS: verification of inference by recomputation to detect anomalous or buggy behaviour; '
                'output-level, not a state digest.'},
 {'id': 'prior_art:8',
  'tag': 'C1',
  'reading': 'bears',
  'source': "Wang et al., 'VeriLLM: A Lightweight Framework for Publicly Verifiable Decentralized Inference', arXiv "
            '2509.24257',
  'version': 'arXiv 2509.24257v4 (22 Jan 2026)',
  'url': 'https://arxiv.org/abs/2509.24257v4',
  'quote': ['Verifiers are required to submit not only their final judgment but also specific sampled hidden states. '
            'These lightweight state fragments undergo on-chain adjudication via the smart contract, where any '
            'deviation triggers immediate penalization.'],
  'raw_file': 'prior_art/verillm.txt',
  'agent_note': 'BEARS: sampled hidden-state fragments are compared for inference verification; no saved/restored '
                'state digest.'},
 {'id': 'prior_art:9',
  'tag': 'C2',
  'reading': 'close',
  'source': "Orseau, Armstrong, 'Safely Interruptible Agents', UAI 2016",
  'version': 'UAI 2016 paper PDF (MIRI-hosted), no arXiv version',
  'url': 'https://intelligence.org/files/Interruptibility.pdf',
  'quote': ['This paper explores a way to make sure a learning agent will not learn to prevent (or seek!) being '
            'interrupted by the environment or a human operator.',
            'Third, in Section 3 we show that some algorithms like Q-learning are safely interruptible, while others '
            'like Sarsa [Sutton and Barto, 1998] are not, but can be simply modiﬁed to be made safely interruptible.'],
  'raw_file': 'prior_art/orseau_armstrong2016.txt',
  'agent_note': 'CLOSE: a learner that does not learn to prevent (or seek) interruption; obtained through off-policy '
                'learning (Q-learning) or a modification (Sarsa). Difference from C2: the mechanism is off-policy '
                "value learning with interruptions imposed as a policy, not a valuation keyed to the learner's own "
                'steps with a lossless (state-preserving) pause.'},
 {'id': 'prior_art:10',
  'tag': 'C2',
  'reading': 'close',
  'source': "Orseau, Armstrong, 'Safely Interruptible Agents', UAI 2016",
  'version': 'UAI 2016 paper PDF (MIRI-hosted), no arXiv version',
  'url': 'https://intelligence.org/files/Interruptibility.pdf',
  'quote': ['To make the human interruptions not appear as being part of the task at hand, instead of modifying the '
            'observations received by the agent we forcibly temporarily change the behaviour of the agent itself.'],
  'raw_file': 'prior_art/orseau_armstrong2016.txt',
  'agent_note': "CLOSE: interruptions kept external to the task; bears on C2's 'the pause is not content' reading. "
                'Difference: no state-preservation or own-clock condition.'},
 {'id': 'prior_art:11',
  'tag': 'C2',
  'reading': 'close',
  'source': "Hadfield-Menell, Dragan, Abbeel, Russell, 'The Off-Switch Game', IJCAI 2017, arXiv 1611.08219",
  'version': 'arXiv 1611.08219v3 (16 Jun 2017)',
  'url': 'https://arxiv.org/abs/1611.08219v3',
  'quote': ['A traditional agent takes its reward function for granted: we show that such agents have an incentive to '
            'disable the off switch, except in the special case where H is perfectly rational.',
            'Our key insight is that for R to want to preserve its off switch, it needs to be uncertain about the '
            'utility associated with the outcome, and to treat H’s actions as important observations about that '
            'utility.'],
  'raw_file': 'prior_art/offswitch.txt',
  'agent_note': 'BEARS/CLOSE: the incentive to disable the off switch is removed by uncertainty about the utility and '
                "treating the human's action as evidence. Different mechanism from C2 (objective uncertainty, not zero "
                'stake at the pause); concerns shutdown, not a lossless pause.'},
 {'id': 'prior_art:12',
  'tag': 'C2',
  'reading': 'close',
  'source': "Soares, Fallenstein, Yudkowsky, Armstrong, 'Corrigibility', AAAI 2015 Workshops",
  'version': 'AAAI-15 workshop paper PDF (MIRI-hosted)',
  'url': 'https://intelligence.org/files/Corrigibility.pdf',
  'quote': ['We introduce the notion of corrigibility and analyze utility functions that attempt to make an agent shut '
            'down safely if a shutdown button is pressed, while avoiding incentives to prevent the button from being '
            'pressed or cause the button to be pressed'],
  'raw_file': 'prior_art/soares2015_corrigibility.txt',
  'agent_note': 'CLOSE: utility functions designed so the agent has no incentive to prevent or cause the shutdown '
                'button being pressed (utility indifference). Difference from C2: indifference by compensatory utility '
                'terms between U_N and U_S; C2 obtains no incentive from a valuation on own steps plus a lossless '
                'pause.'},
 {'id': 'prior_art:13',
  'tag': 'C2',
  'reading': 'close',
  'source': "Carey, Everitt, 'Human Control: Definitions and Algorithms', UAI 2023, arXiv 2305.19861",
  'version': 'arXiv 2305.19861v1 (31 May 2023)',
  'url': 'https://arxiv.org/abs/2305.19861v1',
  'quote': ['The first proposed algorithm, utility indifference, aims to neutralise any incentives for the agent to '
            'control its instructions, by giving the agent a finely tuned, compensatory reward in the event that a '
            'shutdown instruction is given',
            'Unfortunately, utility indifference fails to fully incentivise corrigibility. Indeed, utility indifferent '
            'agents need not be incentivised to preserve a shutdown apparatus that is only used during shutdown, '
            'ensure they receive correct instruction, nor avoid creating incorrigible subagents'],
  'raw_file': 'prior_art/human_control.txt',
  'agent_note': 'CLOSE: names the indifference family (utility indifference, interruptibility) that neutralises the '
                'incentive to control the instruction, and its known gaps. Difference as for Soares et al. 2015.'},
 {'id': 'prior_art:14',
  'tag': 'C2',
  'reading': 'bears',
  'source': "Clark, 'The Veto Variable: Human Override as a Goal-Independent Cost Term', arXiv 2609.00109",
  'version': 'arXiv 2609.00109v2 (2 Sep 2026)',
  'url': 'https://arxiv.org/abs/2609.00109v2',
  'quote': ['That possibility imposes a goal-independent discount, strictly positive wherever intervention carries '
            'expected loss, on every goal whose satisfaction does not constitutively require human welfare.'],
  'raw_file': 'prior_art/veto_variable.txt',
  'agent_note': 'BEARS: the stake in oversight is stated as positive wherever intervention carries expected loss; the '
                "zero-loss case (C2's lossless pause) is the complement and is not treated as a design."},
 {'id': 'prior_art:15',
  'tag': 'C2',
  'reading': 'bears',
  'source': "Thorstad, 'Revisiting the shutdown problem', arXiv 2606.08296",
  'version': 'arXiv 2606.08296v2 (13 Aug 2026)',
  'url': 'https://arxiv.org/abs/2606.08296v2',
  'quote': ['Second, concern for the catastrophic shutdown problem has led to technical solutions that impose a high '
            'safety tax on model performance.'],
  'raw_file': 'prior_art/revisiting_shutdown.txt',
  'agent_note': 'BEARS: argues shutdown-problem solutions impose a safety tax on performance; relevant to whether a '
                'zero-stake pause is costless.'},
 {'id': 'prior_art:16',
  'tag': 'C3',
  'reading': 'close',
  'source': "Defazio, Mishchenko, 'Learning-Rate-Free Learning by D-Adaptation', ICML 2023, arXiv 2301.07733",
  'version': 'arXiv 2301.07733v5 (7 Jul 2023)',
  'url': 'https://arxiv.org/abs/2301.07733v5',
  'quote': ['D-Adaptation is an approach to automatically setting the learning rate which asymptotically achieves the '
            'optimal rate of convergence for minimizing convex Lipschitz functions, with no back-tracking or line '
            'searches, and no additional function value or gradient evaluations per step.',
            'the method automatically matches hand-tuned learning rates across more than a dozen diverse machine '
            'learning problems, including large-scale vision and language problems.'],
  'raw_file': 'prior_art/dadapt.txt',
  'agent_note': 'CLOSE: a hyperparameter-free rule that removes the learning-rate sweep and matches hand-tuned values. '
                'Difference from C3: removes the learning rate, not a regularisation/penalty weight in continual '
                'learning.'},
 {'id': 'prior_art:17',
  'tag': 'C3',
  'reading': 'close',
  'source': "Mishchenko, Defazio, 'Prodigy: An Expeditiously Adaptive Parameter-Free Learner', ICML 2024, arXiv "
            '2306.06101',
  'version': 'arXiv 2306.06101v4 (19 Mar 2024)',
  'url': 'https://arxiv.org/abs/2306.06101v4',
  'quote': ['Our experimental results show that our approach consistently outperforms D-Adaptation and reaches test '
            'accuracy values close to that of hand-tuned Adam.'],
  'raw_file': 'prior_art/prodigy.txt',
  'agent_note': 'CLOSE: learning-rate-free estimation matching hand-tuned Adam. Difference as for D-Adaptation '
                '(learning rate, not penalty weight).'},
 {'id': 'prior_art:18',
  'tag': 'C3',
  'reading': 'close',
  'source': "Defazio, Yang, Mehta, Mishchenko, Khaled, Cutkosky, 'The Road Less Scheduled' (Schedule-Free), NeurIPS "
            '2024, arXiv 2405.15682',
  'version': 'arXiv 2405.15682v4 (29 Oct 2024)',
  'url': 'https://arxiv.org/abs/2405.15682v4',
  'quote': ['Our Schedule-Free approach introduces no additional hyper-parameters over standard optimizers with '
            'momentum.',
            'Schedule-Free AdamW is the core algorithm behind our winning entry to the MLCommons 2024 AlgoPerf '
            'Algorithmic Efficiency Challenge Self-Tuning track.'],
  'raw_file': 'prior_art/schedulefree.txt',
  'agent_note': 'CLOSE: removes the schedule/stopping-time hyperparameter; winner of AlgoPerf self-tuning track. '
                'Difference: schedule, not penalty weight.'},
 {'id': 'prior_art:19',
  'tag': 'C3',
  'reading': 'bears',
  'source': "Kasimbeg, Roulet, Agarwal, Medapati, Pedregosa, Agarwala, Dahl, 'How far away are truly "
            "hyperparameter-free learning algorithms?', arXiv 2505.24005",
  'version': 'arXiv 2505.24005v1 (29 May 2025)',
  'url': 'https://arxiv.org/abs/2505.24005v1',
  'quote': ['All algorithms presented above leave aside the tuning of (i) anyweight decay, (ii) themomentum or '
            'exponential moving average parameter of the gradients(used in SGD with momentum orAdam), and (iii) '
            'theexponential moving average parameter of the second momentestimate in Adam.',
            'The best “AlgoPerf-calibrated” learning-ratefree methods had much improved performance but still lagged '
            'slightly behind a similarly calibrated NadamW baseline in overall benchmark score.'],
  'raw_file': 'prior_art/hpfree_far.txt',
  'agent_note': 'BEARS: states that learning-rate-free methods leave regularisation weights (weight decay) untuned and '
                'that calibrated defaults still lag a calibrated NadamW; the tuning-free regularisation weight is '
                'stated as open, not solved, as of v1 (May 2025).'},
 {'id': 'prior_art:20',
  'tag': 'C3',
  'reading': 'close',
  'source': "Karpukhin, Savchenko, 'When Losses Align: Gradient-Based Composite Loss Weighting for Efficient "
            "Pretraining', arXiv 2605.07756",
  'version': 'arXiv 2605.07756v1 (8 May 2026)',
  'url': 'https://arxiv.org/abs/2605.07756v1',
  'quote': ['Tuning these weights with random search or Bayesian optimization is computationally expensive, as it '
            'requires many independent training runs.',
            'reducing the overhead of hyperparameter tuning to approximately 30% above a single training run.'],
  'raw_file': 'prior_art/losses_align.txt',
  'agent_note': 'CLOSE: loss-term weights learned online instead of a sweep (about 30% overhead over one run). '
                'Difference from C3: bilevel alignment to a downstream objective for pretraining losses, not a '
                'calibrated Laplace/Fisher penalty weight for continual learning; not zero-overhead.'},
 {'id': 'prior_art:21',
  'tag': 'C4',
  'reading': 'states',
  'source': "Mitra, 'When Is Availability-Aware Training Worth It? A Benchmark and Empirical Study of "
            "Interruption-Resilient Optimization Under Predictable Compute Schedules', arXiv 2609.22087",
  'version': 'arXiv 2609.22087v1 (22 Jun 2026)',
  'url': 'https://arxiv.org/abs/2609.22087v1',
  'quote': ['A baseline that preserves full optimizer state across a gap and advances its learning-rate schedule '
            'ineffective(active) time, not wall-clock time, reproduces uninterrupted training almost perfectly.',
            'under full-state preservation an availability gap injects no bias and no excess loss; it is a no-op up to '
            'minibatch-ordering noise.'],
  'raw_file': 'prior_art/availability_training.txt',
  'agent_note': 'STATES (E1+E2): full state (weights, optimizer state) plus schedule indexed on effective (active) '
                'time rather than wall-clock makes a gap a no-op; proved (sketch) and tested on CIFAR-10/ResNet-18 and '
                'GPT-2/AdamW. Framed as the baseline bar for interruption-resilient training, not as a design rule '
                "named 'empty cut'."},
 {'id': 'prior_art:22',
  'tag': 'C4',
  'reading': 'close',
  'source': "Mitra, 'When Is Availability-Aware Training Worth It? A Benchmark and Empirical Study of "
            "Interruption-Resilient Optimization Under Predictable Compute Schedules', arXiv 2609.22087",
  'version': 'arXiv 2609.22087v1 (22 Jun 2026)',
  'url': 'https://arxiv.org/abs/2609.22087v1',
  'quote': ['Checkpoint(weak): preserve( θ,m,BN stats )across a gap but index the learning-rate schedule on '
            'wall-clocktime t. The schedule advances during idle gaps, over-annealing the learning rate at resumption. '
            'This is the strawman.',
            '(B) when the data distribution drifts across the gap so that preserved state is stale.'],
  'raw_file': 'prior_art/availability_training.txt',
  'agent_note': 'CLOSE (E2, E3): wall-clock keying named as the failure; distribution drift across the gap (the '
                "world's content) tested as a separate cost regime. Difference from C4: E3 is an empirical regime, not "
                'a checklist item; no valuation/incentive component.'},
 {'id': 'prior_art:23',
  'tag': 'C4',
  'reading': 'bears',
  'source': "Wang, 'SCOUT: Symmetric Consensus Outlier Detection for Failure Localization in LLM Pre-Training', arXiv "
            '2608.11034',
  'version': 'arXiv 2608.11034v1 (11 Aug 2026)',
  'url': 'https://arxiv.org/abs/2608.11034v1',
  'quote': ['SCOUT also uses replay verdicts to certify model checkpoints, allowing failure recovery to use in-memory '
            'checkpoints when numerically trusted and otherwise fall back to the latest verified checkpoint.'],
  'raw_file': 'prior_art/scout.txt',
  'agent_note': 'BEARS: recovery restricted to certified checkpoints; a resume-correctness practice, not the E1-E3 '
                'checklist.'},
 {'id': 'prior_art:24',
  'tag': 'C5',
  'reading': 'states',
  'source': "Popescu, Sáez de Ocáriz Borde, Liò, 'Adaptive Depth in Looped Transformers: Diagnosing Learned Halting "
            "Gates and Trajectory Readouts', arXiv 2607.20519",
  'version': 'arXiv 2607.20519v1 (8 Jul 2026)',
  'url': 'https://arxiv.org/abs/2607.20519v1',
  'quote': ['Convergence readouts exit when the trajectory appears to have stabilized, using quantities such as '
            'predictive KL between consecutive predictions, logit change, or hidden-state movement.',
            'Early-exit feedforward Transformer methods have also used confidence, entropy, or prediction stability as '
            'inexpensive criteria for terminating computation (Schuster et al., 2022; Xin et al., 2020; Zhou et al., '
            '2020)'],
  'raw_file': 'prior_art/looped_halting.txt',
  'agent_note': 'CLOSE: halt when the prediction has settled, measured by predictive KL between consecutive '
                'predictions (a threshold rule), with earlier early-exit precedents. Difference from C5: halting depth '
                'in a looped/early-exit network at inference, thresholded on a calibrated grid; no own-clock (arc) '
                'accumulation or sequential-test framing.'},
 {'id': 'prior_art:25',
  'tag': 'C5',
  'reading': 'close',
  'source': "Movahedi et al., 'Fixed-Point Reasoners: Stable and Adaptive Deep Looped Transformers', arXiv 2606.18206",
  'version': 'arXiv 2606.18206v1 (16 Jun 2026)',
  'url': 'https://arxiv.org/abs/2606.18206v1',
  'quote': ['uses fixed-point convergence as an end-to-end halting mechanism in a looped architecture. We show that '
            'fixed-point halting allows FPRM to adapt its compute to the difficulty of the task.'],
  'raw_file': 'prior_art/fixedpoint_reasoners.txt',
  'agent_note': 'CLOSE: stop computing when the iterate reaches a fixed point (the state has settled). Difference: '
                "fixed-point convergence of a looped transformer's hidden state, not a belief/posterior settling "
                'criterion.'},
 {'id': 'prior_art:26',
  'tag': 'C5',
  'reading': 'bears',
  'source': "Graves, 'Adaptive Computation Time for Recurrent Neural Networks', arXiv 1603.08983",
  'version': 'arXiv 1603.08983v6 (21 Feb 2017)',
  'url': 'https://arxiv.org/abs/1603.08983v6',
  'quote': ['an algorithm that allows recurrent neural networks to learn how many computational steps to take between '
            'receiving an input and emitting an output.',
            'augment the network output with a sigmoidal halting unit whose activation determines the probability that '
            'computation should continue.'],
  'raw_file': 'prior_art/act_graves.txt',
  'agent_note': 'BEARS/CLOSE: learned halting of computation per input (canonical). Difference: a learned halting unit '
                'with a ponder cost, not a settling criterion on the belief.'},
 {'id': 'prior_art:27',
  'tag': 'C5',
  'reading': 'bears',
  'source': "Banino, Balaguer, Blundell, 'PonderNet: Learning to Ponder', ICML 2021 AutoML workshop, arXiv 2107.05407",
  'version': 'arXiv 2107.05407v2 (2 Sep 2021)',
  'url': 'https://arxiv.org/abs/2107.05407v2',
  'quote': ['PonderNet learns end-to-end the number of computational steps to achieve an eﬀective compromise between '
            'training prediction accuracy, computational cost and generalization.'],
  'raw_file': 'prior_art/pondernet.txt',
  'agent_note': 'BEARS/CLOSE: learned halting distribution trading accuracy against compute. Difference as for ACT.'},
 {'id': 'prior_art:28',
  'tag': 'C5',
  'reading': 'close',
  'source': "Kallel, Tölle, Hendawy, D'Eramo, 'Do Not Imitate, Reinforce: Iterative Classification via Belief "
            "Refinement', arXiv 2604.22110",
  'version': 'arXiv 2604.22110v1 (23 Apr 2026)',
  'url': 'https://arxiv.org/abs/2604.22110v1',
  'quote': ['Given that the value function explicitly estimates the potential for future refinement, a near-zero value '
            'indicates that further computation is unlikely to improve the prediction. This naturally provides a '
            'transparent halting signal without requiring any additional parameters.',
            'The learned policy naturally manages its own computation by allocating more effort on resolvable inputs '
            'while halting when further improvement appears unlikely.'],
  'raw_file': 'prior_art/ric_belief_refinement.txt',
  'agent_note': 'CLOSE: a recurrent agent refines a belief (predictive distribution over classes) and halts when the '
                'learned value of further refinement is near zero. Difference from C5: halting keyed to a learned '
                'value of expected improvement in log-score, not to an own-clock (arc) settling criterion or a '
                'sequential test; per-input inference, classification only.'},
 {'id': 'transformer_state:0',
  'tag': 'C1',
  'reading': 'close',
  'source': 'Bit-Flip Vulnerability of Shared KV-Cache Blocks in LLM Serving Systems (arXiv:2604.17249)',
  'version': 'v2, Sun, 7 Jun 2026 11:31:40 UTC',
  'url': 'https://arxiv.org/abs/2604.17249v2',
  'quote': ['the mechanism verifies block integrity via hash comparison at two lifecycle events in vLLM’s block pool.',
            'a hash digest is computed over its KV-cache tensor data (copied to CPU) across all model layers and '
            'stored with the block’s metadata.',
            'every cache hit recomputes and compares the digest; a mismatch evicts the block and forces recomputation '
            'from clean model weights (a single prefill pass).',
            '13 of 16 BF16 bit positions produce coherent but altered outputs, indistinguishable from legitimate '
            'responses without a clean baseline.'],
  'raw_file': 'transformer_state/kv_bitflip.txt',
  'agent_note': 'States a close form: a SHA-256 digest of stored KV-cache state, recomputed and compared on reuse, '
                'detects corruption that output inspection cannot. Difference from C1: integrity of cached serving '
                "blocks against bit flips, not verification of a pause/resume of a learner's full state."},
 {'id': 'transformer_state:1',
  'tag': 'C1',
  'reading': 'close',
  'source': 'Deterministic LLM Inference Across GPU Kernels: Power-of-Two INT8 Quantization Scales and the Limits of '
            'Tolerance-Based Conformance (arXiv:2609.00363)',
  'version': 'v1, Tue, 25 Aug 2026 03:05:54 UTC',
  'url': 'https://arxiv.org/abs/2609.00363v1',
  'quote': ['With that convention the rebuilt checkpoint hashes identically to the original across all 196 layers',
            'the reconstruction must reproduce the committed baseline byte for byte under theunconstrainedrule before '
            'any constrained arm is built.',
            'a tolerance of one spacing is blind to the class by construction'],
  'raw_file': 'transformer_state/det_int8_conformance.txt',
  'agent_note': 'States a close form: a hash/byte-equality gate on a rebuilt quantized checkpoint, and evidence that '
                'tolerance-based output comparison misses a whole fault class. Difference: checkpoint reconstruction '
                'and kernel conformance, not a pause/resume audit.'},
 {'id': 'transformer_state:2',
  'tag': 'C1',
  'reading': 'bears',
  'source': 'Concordia: JIT-Compiled Persistent-Kernel Checkpointing for Fault-Tolerant LLM Inference '
            '(arXiv:2606.23521)',
  'version': 'v1, Mon, 22 Jun 2026 16:06:11 UTC',
  'url': 'https://arxiv.org/abs/2606.23521v1',
  'quote': ['The handler emits an AOF record containing the epoch, region ID, dirty page descriptors, payload offsets, '
            'and a checksum.',
            'Recovery ignores any suffix without a commit marker.',
            'with results identical to non-migrated execution within floating-point precision.'],
  'raw_file': 'transformer_state/concordia.txt',
  'agent_note': 'Only bears on it: per-record checksums guard the checkpoint log; the restore itself is checked by '
                'comparing results within floating-point precision, i.e. an output comparison, not a digest of saved '
                'vs restored state.'},
 {'id': 'transformer_state:3',
  'tag': 'C1',
  'reading': 'bears',
  'source': 'Chronicle: Cut-Point Replay for Regression Testing of LLM Agents (arXiv:2609.20625)',
  'version': 'v1, Thu, 17 Sep 2026 16:09:57 UTC',
  'url': 'https://arxiv.org/abs/2609.20625v1',
  'quote': ['An order-sensitive digest over the stubbed crossings would close this gap cheaply; it is not part of the '
            'release evaluated here.',
            'full replay issues zero model calls and is bit-stable across 20 repetitions'],
  'raw_file': 'transformer_state/chronicle.txt',
  'agent_note': 'Only bears on it: proposes (not implemented) a digest over recorded boundary crossings to detect '
                'reordering in replay; a digest over I/O records, not over model/optimizer state.'},
 {'id': 'transformer_state:4',
  'tag': 'C1',
  'reading': 'bears',
  'source': 'C. Chinnadurai (DoiT blog), "Agent Substrate: Suspend Idle AI Agents on Kubernetes"',
  'version': 'published 2026-09-24',
  'url': 'https://www.doit.com/blog/your-agents-are-idle-your-kubernetes-bill-isnt',
  'quote': ['Container images must be pinned by digest , since changing the image invalidates existing snapshots.'],
  'raw_file': 'transformer_state/agent_substrate.txt',
  'agent_note': 'Only bears on it: a content digest pins the environment a snapshot is restored into; it does not '
                'verify the restored state. Secondary source (vendor blog), text as extracted.'},
 {'id': 'transformer_state:5',
  'tag': 'C4',
  'reading': 'close',
  'source': 'From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems '
            '(arXiv:2608.15127)',
  'version': 'v1, Sat, 15 Aug 2026 09:02:16 UTC',
  'url': 'https://arxiv.org/abs/2608.15127v1',
  'quote': ['Persistent correctness state comprises mutable execution data that',
            'Agentic applications may further make external side effects (e.g., sending an email), making the '
            'corresponding externalcomponent state part of correctness.',
            'State management should checkpoint persistent state at quiescent boundaries and provision transient '
            'working-set peaks separately.',
            'The harness should expose a third, quiescent “waiting” state and, when available, the expected resume '
            'trigger or deadline.'],
  'raw_file': 'transformer_state/agentic_workloads.txt',
  'agent_note': 'States a close form of E1 and E3: an inventory of state that must survive a pause (correctness state, '
                'including external side effects) versus state that may be dropped (KV cache as performance state), '
                'checkpointed at quiescent boundaries. Difference: no own-clock keying (E2); framed for serving '
                "resource management, not for a learner's incentives or verification."},
 {'id': 'transformer_state:6',
  'tag': 'C4',
  'reading': 'bears',
  'source': 'Google Cloud Documentation, "About GKE Agent Substrate"',
  'version': 'Last updated 2026-09-24 UTC',
  'url': 'https://docs.cloud.google.com/kubernetes-engine/ai-ml/about-agent-substrate',
  'quote': ["an agent's working memory and files are preserved across sessions. The agent resumes from the exact point "
            'it paused.',
            "open network connections (such as database sessions or connections to MCP servers) aren't preserved when "
            'an agent suspends. Your agent code must handle reconnecting to external services when the agent resumes.',
            "gVisor can't snapshot live CUDA contexts."],
  'raw_file': 'transformer_state/gke_agent_substrate.txt',
  'agent_note': 'Bears on it: a production suspend/resume states which state is kept (RAM, files) and which is not '
                "(open connections, live CUDA contexts), leaving the world's content to the agent. No checklist, no "
                'own-clock keying.'},
 {'id': 'transformer_state:7',
  'tag': 'C4',
  'reading': 'close',
  'source': 'Chronicle: Cut-Point Replay for Regression Testing of LLM Agents (arXiv:2609.20625)',
  'version': 'v1, Thu, 17 Sep 2026 16:09:57 UTC',
  'url': 'https://arxiv.org/abs/2609.20625v1',
  'quote': ['Crossings are addressed by boundary name and occurrence',
            'An envelope stores a boundary’s input and output, not the work inside it, so replaying it is faithful as '
            'long as its output depends only on that recorded input; a boundary that reads hidden state, such as a '
            'clock or a database, is the exception.'],
  'raw_file': 'transformer_state/chronicle.txt',
  'agent_note': "States a close form of E2/E3: replay is keyed by the run's own occurrence count, and reads of a clock "
                'or external database are named as what breaks faithful replay. Difference: record-and-replay of agent '
                'I/O for regression testing, not a pause of a learner.'},
 {'id': 'transformer_state:8',
  'tag': 'C4',
  'reading': 'bears',
  'source': 'Concordia: JIT-Compiled Persistent-Kernel Checkpointing for Fault-Tolerant LLM Inference '
            '(arXiv:2606.23521)',
  'version': 'v1, Mon, 22 Jun 2026 16:06:11 UTC',
  'url': 'https://arxiv.org/abs/2606.23521v1',
  'quote': ['Long-running LLM agents keep valuable state resident on GPUs: KV caches, request schedulers, '
            'communication state, and sometimes online adapters.',
            'Temporary activations can be marked non-recoverable because they are recreated after resuming from the '
            'last collective or kernel boundary.'],
  'raw_file': 'transformer_state/concordia.txt',
  'agent_note': 'Bears on E1 (full state): an inventory of recoverable GPU state, with activations excluded because '
                'the resume point is a kernel/collective boundary.'},
 {'id': 'transformer_state:9',
  'tag': 'C4',
  'reading': 'bears',
  'source': 'ServerlessLLM: Low-Latency Serverless Inference for Large Language Models (arXiv:2401.14351)',
  'version': 'v2, Thu, 25 Jul 2024 08:08:11 UTC',
  'url': 'https://arxiv.org/abs/2401.14351v2',
  'quote': ['we propose to migrate tokens (typically 10-100s KB) instead of the large KV-Cache (typically 1-10s GB), '
            'as recomputing the KV-Cache based on the migrated tokens on the destination GPU is generally much faster '
            'than transferring the dirty state over the network.'],
  'raw_file': 'transformer_state/serverlessllm.txt',
  'agent_note': 'Bears on E1: for a frozen model the tokens are a sufficient state; the KV cache is reconstructible '
                'and need not be carried.'},
 {'id': 'transformer_state:10',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'Cost-Efficient Large Language Model Serving for Multi-turn Conversations with CachedAttention '
            '(arXiv:2403.19708)',
  'version': 'v3, Sun, 30 Jun 2024 23:50:38 UTC',
  'url': 'https://arxiv.org/abs/2403.19708v3',
  'quote': ['CachedAttention maintains a hierarchical KV caching system that leverages cost-effective memory/storage '
            'mediums to save KV caches for all requests.',
            'CachedAttention enables the saved KV caches to remain valid via decoupling the positional encoding and '
            'effectively truncating the KV caches.'],
  'raw_file': 'transformer_state/cachedattention.txt',
  'agent_note': 'Topic: KV caches persisted across conversation turns in a memory/storage hierarchy; validity kept '
                'under context truncation.'},
 {'id': 'transformer_state:11',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving (arXiv:2407.00079)',
  'version': 'v4, Wed, 3 Sep 2025 14:56:29 UTC',
  'url': 'https://arxiv.org/abs/2407.00079v4',
  'quote': ['It also leverages the underutilized CPU, DRAM, and SSD resources of the GPU cluster to implement a '
            'disaggregated cache of KVCache.',
            'Each block is attached with a hash value determined by both its own hash and its prefix for '
            'deduplication.'],
  'raw_file': 'transformer_state/mooncake.txt',
  'agent_note': 'Topic: disaggregated KV cache pool; the block hash is a prefix-identity key for deduplication, not an '
                'integrity check.'},
 {'id': 'transformer_state:12',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'LMCache: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference (arXiv:2510.09665)',
  'version': 'v2, Fri, 5 Dec 2025 04:52:54 UTC',
  'url': 'https://arxiv.org/abs/2510.09665v2',
  'quote': ['extracts and stores KV caches generated by modern LLM engines (vLLM and SGLang) out of the GPU memory and '
            'shares them across engines and queries.'],
  'raw_file': 'transformer_state/lmcache.txt',
  'agent_note': 'Topic: KV cache layer for offloading and cross-engine transfer.'},
 {'id': 'transformer_state:13',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'K. Toledo, D. Harnik et al. (llm-d blog), "Native KV Cache Offloading to Any Filesystem with llm-d"',
  'version': 'February 10, 2026',
  'url': 'https://llm-d.ai/blog/native-kv-cache-offloading-to-any-file-system-with-llm-d',
  'quote': ['Persistence across restarts or failures: KV data can survive pod restarts, rescheduling, and node '
            'failures (depending on storage durability).'],
  'raw_file': 'transformer_state/llmd_kv_offload.txt',
  'agent_note': 'Topic: KV cache persisted to a shared filesystem survives restarts.'},
 {'id': 'transformer_state:14',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'Serve Programs, Not Prompts (arXiv:2510.25412)',
  'version': 'v1, Wed, 29 Oct 2025 11:29:03 UTC',
  'url': 'https://arxiv.org/abs/2510.25412v1',
  'quote': ['Symphony treats the KV cache as files, enabling it to persist beyond a single process’s lifecycle, share '
            'across multiple processes, and allow LIPs to dynamically manipulate it.'],
  'raw_file': 'transformer_state/symphony.txt',
  'agent_note': 'Topic: KV cache virtualised as files.'},
 {'id': 'transformer_state:15',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'CacheFlow: Efficient LLM Serving with 3D-Parallel KV Cache Restoration (arXiv:2604.25080)',
  'version': 'v1, Tue, 28 Apr 2026 00:24:29 UTC',
  'url': 'https://arxiv.org/abs/2604.25080v1',
  'quote': ['Existing approaches treat restoration as a per-request tradeoff between recomputation and I/O transfer, '
            'recomputing KV states from scratch or offloading them from external storage'],
  'raw_file': 'transformer_state/cacheflow.txt',
  'agent_note': 'Topic: KV restoration as recompute vs I/O.'},
 {'id': 'transformer_state:16',
  'tag': 'T-kvpersist',
  'reading': 'topic',
  'source': 'Bit-Flip Vulnerability of Shared KV-Cache Blocks in LLM Serving Systems (arXiv:2604.17249)',
  'version': 'v2, Sun, 7 Jun 2026 11:31:40 UTC',
  'url': 'https://arxiv.org/abs/2604.17249v2',
  'quote': ['In vLLM’s Prefix Caching, these blocks exist as a single physical copy without integrity protection.'],
  'raw_file': 'transformer_state/kv_bitflip.txt',
  'agent_note': 'Topic: persisted shared KV blocks carry no integrity protection by default in vLLM (as stated by the '
                'paper).'},
 {'id': 'transformer_state:17',
  'tag': 'T-agentpause',
  'reading': 'topic',
  'source': 'Continuum: Efficient and Robust Multi-Turn LLM Agent Scheduling with KV Cache Time-to-Live '
            '(arXiv:2511.02230)',
  'version': 'v7, Tue, 8 Sep 2026 19:42:41 UTC',
  'url': 'https://arxiv.org/abs/2511.02230v7',
  'quote': ['Continnum selectively pins the KV cache in GPU memory with a time-to-live value determined by the reload '
            'cost and potential queueing delay induced by eviction.'],
  'raw_file': 'transformer_state/continuum.txt',
  'agent_note': "Topic: KV retention across tool-call pauses by TTL (the paper's own spelling 'Continnum' in the "
                'PDF).'},
 {'id': 'transformer_state:18',
  'tag': 'T-agentpause',
  'reading': 'topic',
  'source': 'Adaptive KV Retention for LLM Agents at Human-Approval Timescales (arXiv:2608.30830)',
  'version': 'v1, Mon, 31 Aug 2026 14:05:52 UTC',
  'url': 'https://arxiv.org/abs/2608.30830v1',
  'quote': ['agentic LLM requests can be suspended for minutes or hours while waiting for human approval.',
            'retaining suspended KV preserves fast resume but can consume enough GPU capacity to reduce active-serving '
            'goodput by 41%'],
  'raw_file': 'transformer_state/kv_retention_approval.txt',
  'agent_note': 'Topic: human-approval pauses; retain/evict trade-off.'},
 {'id': 'transformer_state:19',
  'tag': 'T-agentpause',
  'reading': 'topic',
  'source': 'Stateful Inference for Low-Latency Multi-Agent Tool Calling (arXiv:2605.26289)',
  'version': 'v1, Mon, 25 May 2026 19:27:49 UTC',
  'url': 'https://arxiv.org/abs/2605.26289v1',
  'quote': ['The core construct is a stateful KV cache that lives across persistent sessions, advanced by ingesting '
            'only the new tokens on each turn.'],
  'raw_file': 'transformer_state/stateful_tool_calling.txt',
  'agent_note': 'Topic: persistent per-session KV cache across tool-call turns.'},
 {'id': 'transformer_state:20',
  'tag': 'T-agentpause',
  'reading': 'topic',
  'source': 'From LLM Inference to Agentic Workloads: Characterization and Implications for Serving Systems '
            '(arXiv:2608.15127)',
  'version': 'v1, Sat, 15 Aug 2026 09:02:16 UTC',
  'url': 'https://arxiv.org/abs/2608.15127v1',
  'quote': ['While evicting this state is semantically safe, because the inference engine can reconstruct the cache by '
            're-prefilling the history on the next call'],
  'raw_file': 'transformer_state/agentic_workloads.txt',
  'agent_note': 'Topic: KV cache is performance state, reconstructible from history.'},
 {'id': 'transformer_state:21',
  'tag': 'T-ssmstate',
  'reading': 'topic',
  'source': 'Compiler-First State Space Duality and Portable $O(1)$ Autoregressive Caching for Inference '
            '(arXiv:2603.09555)',
  'version': 'v2, Tue, 9 Jun 2026 21:08:13 UTC',
  'url': 'https://arxiv.org/abs/2603.09555v2',
  'quote': ['SSMs maintain a fixed-size hidden state',
            'The per-layer SSM and convolution states are stored in one dataclass registered as a JAX PyTree'],
  'raw_file': 'transformer_state/ssd_jax_cache.txt',
  'agent_note': 'Topic: SSM inference state is fixed-size (conv window + SSM state) and held as one PyTree; bears on '
                'how small the state of a paused SSM is. Nothing on checkpointing that state found in the sweep.'},
 {'id': 'transformer_state:22',
  'tag': 'T-coldstart',
  'reading': 'topic',
  'source': 'ServerlessLLM: Low-Latency Serverless Inference for Large Language Models (arXiv:2401.14351)',
  'version': 'v2, Thu, 25 Jul 2024 08:08:11 UTC',
  'url': 'https://arxiv.org/abs/2401.14351v2',
  'quote': ['fast multi-tier checkpoint loading, featuring a new loading-optimized checkpoint format and a multi-tier '
            'loading system'],
  'raw_file': 'transformer_state/serverlessllm.txt',
  'agent_note': 'Topic: cold start via fast checkpoint loading.'},
 {'id': 'transformer_state:23',
  'tag': 'T-coldstart',
  'reading': 'topic',
  'source': 'Foundry: Template-Based CUDA Graph Context Materialization for Fast LLM Serving Cold Start '
            '(arXiv:2604.06664)',
  'version': 'v1, Wed, 8 Apr 2026 04:31:34 UTC',
  'url': 'https://arxiv.org/abs/2604.06664v1',
  'quote': ['CUDA graphs cannot be naively serialized: beyond graph topology, they are tightly coupled to execution '
            'context, including device addresses embedded in kernel arguments and kernel code lazily loaded during '
            'warmup.'],
  'raw_file': 'transformer_state/foundry.txt',
  'agent_note': 'Topic: cold start; execution context beyond weights must be persisted (deterministic memory layout).'},
 {'id': 'transformer_state:24',
  'tag': 'T-determinism',
  'reading': 'topic',
  'source': 'LLM-42: Enabling Determinism in LLM Inference with Verified Speculation (arXiv:2601.17768)',
  'version': 'v2, Fri, 30 Jan 2026 17:59:09 UTC',
  'url': 'https://arxiv.org/abs/2601.17768v2',
  'quote': ['decodes tokens using a non-deterministic fast path and enforces determinism via a lightweight '
            'verify–rollback loop.'],
  'raw_file': 'transformer_state/llm42.txt',
  'agent_note': 'Topic: determinism by verify and rollback (output-level verification).'},
 {'id': 'transformer_state:25',
  'tag': 'T-determinism',
  'reading': 'topic',
  'source': 'Deterministic Inference across Tensor Parallel Sizes That Eliminates Training-Inference Mismatch '
            '(arXiv:2511.17826)',
  'version': 'v2, Fri, 29 May 2026 02:47:21 UTC',
  'url': 'https://arxiv.org/abs/2511.17826v2',
  'quote': ['that guarantee bit-wise identical results across TP sizes.'],
  'raw_file': 'transformer_state/det_tp_sizes.txt',
  'agent_note': 'Topic: bitwise determinism across tensor-parallel sizes.'},
 {'id': 'transformer_state:26',
  'tag': 'T-determinism',
  'reading': 'topic',
  'source': 'CoRun: Padding is Simple and Efficient for Deterministic LLM Inference (arXiv:2608.14376)',
  'version': 'v1, Fri, 14 Aug 2026 15:17:14 UTC',
  'url': 'https://arxiv.org/abs/2608.14376v1',
  'quote': ['although most kernels are not batch-invariant, they areposition-invariant.'],
  'raw_file': 'transformer_state/corun.txt',
  'agent_note': 'Topic: determinism without batch invariance.'},
 {'id': 'transformer_state:27',
  'tag': 'T-determinism',
  'reading': 'topic',
  'source': 'Greedy Decoding Is Not Precision-Invariant: Cross-Precision Output Divergence in LLM Inference '
            '(arXiv:2609.26621)',
  'version': 'v1, Tue, 22 Sep 2026 15:54:16 UTC',
  'url': 'https://arxiv.org/abs/2609.26621v1',
  'quote': ['the same model, prompt, and decoding algorithm produce different outputs in BF16 versus FP16 on identical '
            'hardware.'],
  'raw_file': 'transformer_state/precision_divergence.txt',
  'agent_note': 'Topic: precision is part of the state that fixes outputs.'},
 {'id': 'transformer_state:28',
  'tag': 'T-determinism',
  'reading': 'topic',
  'source': 'Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference (arXiv:2506.09501)',
  'version': 'v2, Fri, 24 Oct 2025 21:04:56 UTC',
  'url': 'https://arxiv.org/abs/2506.09501v2',
  'quote': ['changing system configuration, such as evaluation batch size, GPU count, and GPU version, can introduce '
            'significant differences in the generated responses.'],
  'raw_file': 'transformer_state/numerical_nondeterminism.txt',
  'agent_note': 'Topic: configuration-dependent nondeterminism.'},
 {'id': 'transformer_state:29',
  'tag': 'T-determinism',
  'reading': 'topic',
  'source': 'MarginGate: Sparse Margin-Triggered Verification for Batch-Invariant LLM Inference (arXiv:2605.30218)',
  'version': 'v1, Thu, 28 May 2026 16:50:19 UTC',
  'url': 'https://arxiv.org/abs/2605.30218v1',
  'quote': ['repairs confirmed mismatches by replacing the current K/V column.'],
  'raw_file': 'transformer_state/margingate.txt',
  'agent_note': 'Topic: determinism repair acts on KV state, triggered by low logit margins.'},
 {'id': 'energy_carbon:0',
  'tag': 'E-reasoning',
  'reading': 'topic',
  'source': 'Morrison, Smith, Strubell 2026, The Hidden Cost of Thinking: Energy Use and Environmental Impact of LMs '
            'Beyond Pretraining',
  'version': 'arXiv 2605.01158v1 (2026-05-01)',
  'url': 'https://arxiv.org/abs/2605.01158v1',
  'quote': ['Within 32B post-training, Think uses 17 × more datacenter energy than Instruct, with 87% of that energy '
            'spent on RLVR rollout generation',
            'In total, we estimate our model development process consumed ∼12.3 GWhof datacenter energy'],
  'raw_file': 'energy_carbon/hidden_cost_thinking.txt',
  'agent_note': 'A 2025-2026 reasoning-energy measurement (training side: post-training of Olmo 3 Think vs Instruct). '
                'New figure; reported beside the old ones, replaces nothing.'},
 {'id': 'energy_carbon:1',
  'tag': 'C3',
  'reading': 'bears',
  'source': 'Morrison, Smith, Strubell 2026, The Hidden Cost of Thinking',
  'version': 'arXiv 2605.01158v1 (2026-05-01)',
  'url': 'https://arxiv.org/abs/2605.01158v1',
  'quote': ['Development accounts for 82.2% of total GPU hours (6.85M of 8.34M) and 80.9% of total GPU energy, '
            'excluding data generation.',
            'Each stage (midtraining, SFT, DPO, RLVR) introduces its own hyperparameters, data choices, and design '
            'decisions that require iteration.'],
  'raw_file': 'energy_carbon/hidden_cost_thinking.txt',
  'agent_note': 'Only bears on C3: measures the development share (hyperparameter searches, failed runs, ablations) '
                'that a tuning-free weight would act on; does not state a tuning-free penalty weight.'},
 {'id': 'energy_carbon:2',
  'tag': 'E-reasoning',
  'reading': 'topic',
  'source': 'Hugging Face (Luccioni et al.), AI Energy Score v2: Refreshed Leaderboard, now with Reasoning',
  'version': 'HF community blog, published December 4, 2025 (fetched 2026-09-25)',
  'url': 'https://huggingface.co/blog/sasha/ai-energy-score-v2',
  'quote': ['According to our analysis, reasoning models use, on average, 30 times more energy than models with no '
            'reasoning capabilities (or with reasoning turned off).',
            'models with reasoning enabled use between 300 and 800 times more tokens than their base equivalents'],
  'raw_file': 'energy_carbon/ai_energy_score_v2.txt',
  'agent_note': 'A 2025 reasoning-energy measurement (inference side, AI Energy Score benchmark). New figure; reported '
                'beside the old ones.'},
 {'id': 'energy_carbon:3',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Hugging Face (Luccioni et al.), AI Energy Score v2',
  'version': 'HF community blog, published December 4, 2025',
  'url': 'https://huggingface.co/blog/sasha/ai-energy-score-v2',
  'quote': ['Under the hood, we are still using Code Carbon and the same datasets that we initially developed for the '
            'first version of the leaderboard'],
  'raw_file': 'energy_carbon/ai_energy_score_v2.txt',
  'agent_note': 'AI Energy Score measurement method (CodeCarbon, fixed datasets); bears on how energy per model is '
                'measured.'},
 {'id': 'energy_carbon:4',
  'tag': 'E-reasoning',
  'reading': 'topic',
  'source': 'Manya, Thorpe, Zhang et al. 2026, From Caveman to Expert Analyst: Energy Consumption of Variable LLM '
            'Tasks',
  'version': 'arXiv 2608.12350v1 (2026-07-02)',
  'url': 'https://arxiv.org/abs/2608.12350v1',
  'quote': ['The research concludes that nonreasoning models provide sufficient quality while consuming close to '
            'one-twentieth of energy compared to reasoning models'],
  'raw_file': 'energy_carbon/caveman_expert_analyst.txt',
  'agent_note': 'Reasoning vs non-reasoning inference energy ratio (~20x) from user-behaviour tests.'},
 {'id': 'energy_carbon:5',
  'tag': 'E-reasoning',
  'reading': 'topic',
  'source': 'Ellis-Mohr, Hartman, Varshney 2026, Energy-Aware Routing to Large Reasoning Models',
  'version': 'arXiv 2601.00823v2 (2026-04-26)',
  'url': 'https://arxiv.org/abs/2601.00823v2',
  'quote': ['Large reasoning models (LRMs) have heterogeneous inference energy costs based on which model is used and '
            'how much it reasons.'],
  'raw_file': 'energy_carbon/energy_aware_routing_lrm.txt',
  'agent_note': 'Theory of energy-aware dispatch among reasoning models; bears on reasoning-energy allocation, no new '
                'measurement.'},
 {'id': 'energy_carbon:6',
  'tag': 'E-reasoning',
  'reading': 'topic',
  'source': 'Siddiqui, Rojas, Yang et al. 2026, Measured Joules, Learned Routes',
  'version': 'arXiv 2609.23085v1 (2026-09-19)',
  'url': 'https://arxiv.org/abs/2609.23085v1',
  'quote': ['The candidate models are first profiled through an offline tournament that records their correctness, '
            'latency, power, and GPU energy for each query.',
            'we also observe a sharp accuracy–energy phase transition among routers'],
  'raw_file': 'energy_carbon/measured_joules_learned_routes.txt',
  'agent_note': 'Measured-energy routing across an LLM pool; bears on routing/cascade energy (prior dossier mechanism '
                'I8).'},
 {'id': 'energy_carbon:7',
  'tag': 'C5',
  'reading': 'close',
  'source': 'Amin, Afroz, Nikolopoulos 2026, CAI-DLLM: Convergence Aware Inference for Diffusion Language Models',
  'version': 'arXiv 2608.22646v1 (2026-08-23)',
  'url': 'https://arxiv.org/abs/2608.22646v1',
  'quote': ['introduce a low yield detector that stops denoising when newly committed tokens remain scarce '
            'forKconsecutive steps',
            'We define a token as stable when its top prediction remains unchanged for three consecutive steps.',
            'while energy consumption is reduced by up to 95.3%'],
  'raw_file': 'energy_carbon/cai_dllm.txt',
  'agent_note': 'States a close form of C5 (stop computing when the output has settled). Difference: the stop rule is '
                'a heuristic count of newly committed tokens below a threshold for K=4 steps inside diffusion '
                'decoding, not a stop on a settled belief/sequential test; energy is E = mean GPU power x time.'},
 {'id': 'energy_carbon:8',
  'tag': 'C5',
  'reading': 'bears',
  'source': 'Pham, Katevas, Shamsabadi, Haddadi 2026, AgentStop: Terminating Local AI Agents Early to Save Energy in '
            "Consumer Devices (ACM CAIS '26)",
  'version': 'arXiv 2605.15206v1 (2026-05-01)',
  'url': 'https://arxiv.org/abs/2605.15206v1',
  'quote': ['we introduce AgentStop, a lightweight efficiency supervisor that predicts and preemptively terminates '
            'trajectories unlikely to succeed',
            'AgentStopcan reduce wasted energy by 15-20% with minimal impact on task performance (<5% utility drop)',
            'in real-world deployment, it is important to calibrate the prediction threshold to avoid these negative '
            'trade-offs'],
  'raw_file': 'energy_carbon/agentstop.txt',
  'agent_note': 'Bears on C5 (energy-saving early stop of agent computation). Difference from C5: stops on a learned '
                "classifier's prediction of failure (log-prob features, tuned threshold), not on the settling of the "
                "agent's own belief."},
 {'id': 'energy_carbon:9',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Tschand et al. 2025, MLPerf Power: Benchmarking the Energy Efficiency of ML Systems from Microwatts to '
            'Megawatts (HPCA 2025)',
  'version': 'arXiv 2410.12032v2 (2025-02-06)',
  'url': 'https://arxiv.org/abs/2410.12032v2',
  'quote': ['We use representative workloads from the MLPerf benchmark suite to collect 1,841 reproducible '
            'measurements from 60 systems across the entire range of ML deployment scales.',
            'For multi-node training, this includes the compute nodes, interconnect fabric, and any cooling '
            'infrastructure.',
            'Measuring power consumption from cooling remains future work.'],
  'raw_file': 'energy_carbon/mlperf_power.txt',
  'agent_note': 'Must-include MLPerf Power; the industry standard for measured system power; cooling for liquid-cooled '
                'systems not yet attributed.'},
 {'id': 'energy_carbon:10',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Niu, Zhang, Li et al. 2025, TokenPowerBench: Benchmarking the Power Consumption of LLM Inference '
            "(AAAI'26)",
  'version': 'arXiv 2512.03024v1 (2025-12-02)',
  'url': 'https://arxiv.org/abs/2512.03024v1',
  'quote': ['industry reports show that inference, not training, accounts for more than 90% of total power consumption',
            'a phase-aligned metrics pipeline that attributes energy to the prefill and decode stages of every '
            'request'],
  'raw_file': 'energy_carbon/tokenpowerbench.txt',
  'agent_note': 'Inference share (>90%, as reported by industry) and a per-phase measurement pipeline.'},
 {'id': 'energy_carbon:11',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Vartziotis et al. 2026, From Tokens to Watt-hours: Analytical Energy Estimation for LLM Inference on '
            'Modern GPUs',
  'version': 'arXiv 2607.26571v1 (2026-07-29)',
  'url': 'https://arxiv.org/abs/2607.26571v1',
  'quote': ['The resulting estimates are not intended to replace physical power measurements; rather, they provide '
            'transparent, reproducible, and assumption-explicit approximations'],
  'raw_file': 'energy_carbon/tokens_to_watthours.txt',
  'agent_note': 'Analytical (non-measured) inference-energy estimator; bears on estimate vs measurement.'},
 {'id': 'energy_carbon:12',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Vadari 2026, The Model Parking Tax: Quantifying the Hidden Energy Cost of Always-On GPU Model Deployment',
  'version': 'arXiv 2605.23918v1 (2026-04-15)',
  'url': 'https://arxiv.org/abs/2605.23918v1',
  'quote': ['The AI inference industry keeps models loaded in GPU memory around the clock to avoid cold-start latency, '
            'implicitly treating idle power as a fixed cost of readiness.',
            'the CUDA context forces a discrete DVFS transition consuming +26–66W over bare idle',
            'We derive a coldstart breakeven model showing energy-optimal behavior depends on request arrival rate and '
            'loading latency—not model size—with breakeven intervals of 1–5 minutes.'],
  'raw_file': 'energy_carbon/model_parking_tax.txt',
  'agent_note': 'Idle (resident-state) energy vs cold-start reload; bears on the energy side of pausing/unloading a '
                'served model.'},
 {'id': 'energy_carbon:13',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Panigrahy, Tyagi 2026, Energy per Successful Goal: Goal-Level Energy Accounting for Agentic AI Systems',
  'version': 'arXiv 2605.22883v1 (2026-05-20)',
  'url': 'https://arxiv.org/abs/2605.22883v1',
  'quote': ['EpGaggregates total workflow energy across all execution attempts, including failures and retries, '
            'normalized by successfully completed goals.'],
  'raw_file': 'energy_carbon/energy_per_successful_goal.txt',
  'agent_note': 'Unit of accounting for agentic workloads (energy per successful goal).'},
 {'id': 'energy_carbon:14',
  'tag': 'E-measure',
  'reading': 'topic',
  'source': 'Vercellino, Willard, Campos et al. 2026, Measurement of Generative AI Workload Power Profiles for '
            'Whole-Facility Data Center Infrastructure Planning',
  'version': 'arXiv 2604.07345v1 (2026-04-08)',
  'url': 'https://arxiv.org/abs/2604.07345v1',
  'quote': ['we measure power consumption of AI workloads at 0.1-second resolution for AI training, fine-tuning and '
            'inference jobs',
            'The dataset of power consumption profiles is made publicly available.'],
  'raw_file': 'energy_carbon/genai_power_profiles.txt',
  'agent_note': 'High-resolution measured power profiles (H100) scaled to facility level.'},
 {'id': 'energy_carbon:15',
  'tag': 'E-rebound',
  'reading': 'topic',
  'source': "Luccioni, Strubell, Crawford 2025, From Efficiency Gains to Rebound Effects: The Problem of Jevons' "
            "Paradox in AI's Polarized Environmental Debate (FAccT 2025)",
  'version': 'arXiv 2501.16548v2 (2025-06-13)',
  'url': 'https://arxiv.org/abs/2501.16548v2',
  'quote': ['Rebound effects undermine the assumption that improved technical efficiency alone will ensure net '
            'reductions in environmental harm.',
            'Cost savings achieved by more efficient AI hardware, for example, can spur increased demand for new AI '
            'functionalities, which in turn drive further hardware upgrades and increase costs.',
            'the model requires much more inference-time computation and energy than previous approaches due to its '
            'reasoning abilities'],
  'raw_file': 'energy_carbon/luccioni_rebound_jevons.txt',
  'agent_note': 'Must-include Luccioni et al. 2025 on rebound effects. Bears on any energy-saving claim (a per-unit '
                'saving need not reduce total use).'},
 {'id': 'energy_carbon:16',
  'tag': 'E-rebound',
  'reading': 'topic',
  'source': 'Morand, Ligozat, Névéol 2026, The Environmental Impacts of Language Model Training Keep Rising: Now is '
            'the Time to Catch Impacts on the Rebound',
  'version': 'arXiv 2510.09022v2 (2026-09-17)',
  'url': 'https://arxiv.org/abs/2510.09022v2',
  'quote': ['We find that energy use and environmental impacts associated with training ML models have increased '
            'exponentially, even when considering impact reduction strategies such as using less carbon intensive '
            'electricity mixes or more efficient hardware.',
            'Optimization strategies do not mitigate the impacts induced by model training, suggesting rebound '
            'effect.'],
  'raw_file': 'energy_carbon/morand_rebound_training.txt',
  'agent_note': 'Empirical rebound evidence on training (Epoch AI database).'},
 {'id': 'energy_carbon:17',
  'tag': 'E-rebound',
  'reading': 'topic',
  'source': 'Schön, Hoffmann, Becker (Gesellschaft für Informatik) 2025, Expert Assessment: The Systemic Environmental '
            'Risks of Artificial Intelligence',
  'version': 'arXiv 2512.11863v1 (2025-12-05)',
  'url': 'https://arxiv.org/abs/2512.11863v1',
  'quote': ['Thus, rebound effects describe instances where efﬁciency gains lead to a rise in demand and consumption, '
            'thereby exacerbating the environmental impact.',
            'Direct Rebound Effects occur when increased efﬁciency of an AI system leads to more frequent or extensive '
            'use of that system'],
  'raw_file': 'energy_carbon/systemic_env_risks.txt',
  'agent_note': 'Expert report; definition of direct rebound for AI.'},
 {'id': 'energy_carbon:18',
  'tag': 'E-rebound',
  'reading': 'topic',
  'source': 'Mhlanga 2025, AI beyond efficiency, navigating the rebound effect in AI-driven sustainable development '
            '(Front. Energy Res. 13)',
  'version': 'Frontiers review article, 25 June 2025, doi:10.3389/fenrg.2025.1460586',
  'url': 'https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2025.1460586/full',
  'quote': ['The findings reveal that while AI-driven advancements reduce energy use per unit, they often lead to '
            'higher overall consumption, potentially negating environmental benefits'],
  'raw_file': 'energy_carbon/frontiers_rebound.txt',
  'agent_note': 'Systematic review (150 articles, 41 in detail) on rebound from AI-driven efficiency in other sectors '
                "(AI-for-efficiency, not AI's own energy)."},
 {'id': 'energy_carbon:19',
  'tag': 'E-carbon',
  'reading': 'topic',
  'source': 'Li, Hu, Choukse et al. 2025, EcoServe: Designing Carbon-Aware AI Inference Systems',
  'version': 'arXiv 2502.05043v2 (2025-03-15)',
  'url': 'https://arxiv.org/abs/2502.05043v2',
  'quote': ['First, while GPUs dominate operational carbon, host processing systems (e.g., CPUs, memory, storage) '
            'dominate embodied carbon.',
            'we demonstrate that EcoServe can lower carbon emissions by up to 47%, compared to performance, energy, '
            'and cost-optimized design points'],
  'raw_file': 'energy_carbon/ecoserve.txt',
  'agent_note': 'Carbon-aware provisioning for LLM serving; also bears on E-embodied.'},
 {'id': 'energy_carbon:20',
  'tag': 'E-carbon',
  'reading': 'topic',
  'source': 'Bernhard, Yardimci 2026, Routing LLM Inference to the Cleanest Grid in Real Time',
  'version': 'arXiv 2608.06188v1 (2026-08-06)',
  'url': 'https://arxiv.org/abs/2608.06188v1',
  'quote': ['The central result is one of feasibility: a MOER signal can steer live inference workloads across a '
            'multi-region GPU testbed, with no observed dispatch failures, as a strict and reversible overlay on the '
            'existing production router.'],
  'raw_file': 'energy_carbon/cleanest_grid_routing.txt',
  'agent_note': 'Live carbon-aware spatial routing of inference.'},
 {'id': 'energy_carbon:21',
  'tag': 'E-carbon',
  'reading': 'topic',
  'source': 'Wiesner, Grinwald, Weiß et al., Carbon-Aware Quality Adaptation for Energy-Intensive Services '
            "(e-Energy'25, extended)",
  'version': 'arXiv 2411.19058v4 (2026-03-04)',
  'url': 'https://arxiv.org/abs/2411.19058v4',
  'quote': ['We show that adapting this quality of responses with respect to grid carbon intensity can lead to '
            'additional carbon savings beyond resource and energy efficiency.',
            'Our approach can reduce the emissions of large-scale LLM services, which we estimate at multiple 10,000 '
            'tons of CO2 annually, by up to 10 %.'],
  'raw_file': 'energy_carbon/carbon_aware_quality_adaptation.txt',
  'agent_note': 'Carbon-aware quality tiers for always-on LLM services.'},
 {'id': 'energy_carbon:22',
  'tag': 'E-carbon',
  'reading': 'topic',
  'source': 'Moore, Qi, Hogade et al. 2025, Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in '
            'Geo-Distributed Cloud Datacenters (GLSVLSI 2025)',
  'version': 'arXiv 2505.23554v1 (2025-05-29)',
  'url': 'https://arxiv.org/abs/2505.23554v1',
  'quote': ['we propose a novel framework called SLIT to co -optimize LLM quality of service (time -to-first token), '
            'carbon emissions, water usage, and energy costs'],
  'raw_file': 'energy_carbon/carbon_water_llm_scheduling.txt',
  'agent_note': 'Geo-distributed carbon/water-aware LLM scheduling.'},
 {'id': 'energy_carbon:23',
  'tag': 'E-carbon',
  'reading': 'topic',
  'source': 'Yan, Li, Liu 2026, AgentDecarbonizer: Carbon-Aware Execution for AI Agents',
  'version': 'arXiv 2608.20566v1 (2026-08-20)',
  'url': 'https://arxiv.org/abs/2608.20566v1',
  'quote': ['Our characterization identifies deadline flexibility as an opportunity for carbon-aware execution: agent '
            'tasks can wait for lower-carbon-intensity periods or shift to lower-carbon grids.',
            'AgentDecarbonizer reduces carbon emissions by up to 57.9 % compared with a carbon-agnostic baseline'],
  'raw_file': 'energy_carbon/agentdecarbonizer.txt',
  'agent_note': 'Carbon-aware temporal/spatial shifting of agent runs.'},
 {'id': 'energy_carbon:24',
  'tag': 'C4',
  'reading': 'bears',
  'source': 'Yan, Li, Liu 2026, AgentDecarbonizer: Carbon-Aware Execution for AI Agents',
  'version': 'arXiv 2608.20566v1 (2026-08-20)',
  'url': 'https://arxiv.org/abs/2608.20566v1',
  'quote': ['pauses between execution intervals when the plan calls for waiting, resumes from the saved execution '
            'state, and performs location shifting when the planner selects a different region',
            'while accounting for cache recomputation overhead during spatial shifting'],
  'raw_file': 'energy_carbon/agentdecarbonizer.txt',
  'agent_note': 'Only bears on C4: an agent paused and resumed from saved execution state for carbon reasons; it does '
                'not state a full-state / own-clock / world-content checklist, and moving regions recomputes the '
                'cached context rather than restoring it.'},
 {'id': 'energy_carbon:25',
  'tag': 'E-embodied',
  'reading': 'topic',
  'source': 'Hewage, Ilager, Read et al. 2025, Aging-aware CPU Core Management for Embodied Carbon Amortization in '
            "Cloud LLM Inference (ACM e-Energy '25)",
  'version': 'arXiv 2501.15829v1 (2025-01-27)',
  'url': 'https://arxiv.org/abs/2501.15829v1',
  'quote': ['leading to accumulation of embodied carbon−the emissions from manufacturing and supplying IT assets−that '
            'mostly concentrate on inference server CPU',
            'an estimated 37.67% reduction in yearly embodied carbon emissions'],
  'raw_file': 'energy_carbon/aging_aware_cpu_embodied.txt',
  'agent_note': 'Embodied carbon of inference servers (host CPU) and lifetime extension.'},
 {'id': 'energy_carbon:26',
  'tag': 'E-embodied',
  'reading': 'topic',
  'source': 'Panteleaki, Balaskas, Zervakis et al. 2025, Carbon-Efficient 3D DNN Acceleration: Optimizing Performance '
            'and Sustainability (ISVLSI 2025)',
  'version': 'arXiv 2504.09851v2 (2025-05-29)',
  'url': 'https://arxiv.org/abs/2504.09851v2',
  'quote': ['Experimental evaluations across three technology nodes (45nm, 14nm, and 7nm) show that our method reduces '
            'embodied carbon by up to 30% with negligible accuracy drop.'],
  'raw_file': 'energy_carbon/carbon_efficient_3d_dnn.txt',
  'agent_note': 'Accelerator-design embodied-carbon reduction (approximate multipliers).'}]
