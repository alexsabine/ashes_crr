"""Claims for Open_Bottlenecks/DECLARATION.md Stage 1, family H3 (loss of plasticity, long-horizon streams, continual
reinforcement learning, non-stationary optimisation), transcribed from the dossier docs/citations/ob1_h3_2026-09-30.md
(sources fetched 2026-09-30 through the session proxy; the extracted texts are held outside the repository under
/tmp/claude-0/ob1_src/, named in `raw_file` relative to that root; sha256 of every fetched file in
/tmp/claude-0/ob1_src/h3/SHA256SUMS.txt and in the dossier). Every quote is copied from the text that pymupdf 1.28.2
extracted from the fetched PDF; whitespace is normalised and line-break hyphens may be rejoined (the verifier's rule);
table rows are quoted cell by cell in the extractor's reading order. Nothing else is changed.

Roles (DECLARATION.md, Stage 1):
  a  a quote stating the problem;
  b  a 2025-26 quote stating that it is open, unsolved or a main challenge;
  c  the best reported result on a named benchmark, and the target (joint/offline training, an oracle, a human or batch
     reference, or a stated goal), with the numbers quoted; the gap is computed in the agent_note;
  d  a method family tried and the assumption it makes (about time or clock, task boundaries, memory, tuning, what is
     stored, what is held fixed).
A bottleneck is marked open=True only if it has at least one claim of each role a, b and c, the b claim is from a
2025-26 source, and the c numbers show the best reported result short of the stated target. The notes, the gap
arithmetic and the reading of each table are the harvesting agent's, for the investigator's review; numbers from
different papers are not comparable.
"""

AG = 'harvesting agent (H3), 2026-09-30; for the investigator\'s review'

# --------------------------------------------------------------------------------------------------------------------
# Sources (short keys used below)
KLEIN = ('Klein, Luther, McAuliffe, Miklautz, Plant, Tschiatschek, "Plasticity Loss in Deep Reinforcement Learning: '
         'A Survey" (arXiv:2411.04832)', 'v3, 18 Apr 2026', 'https://arxiv.org/abs/2411.04832',
         'h3/src/pdf_2411.04832v3.txt')
CCHAIN = ('Tang, Obando-Ceron, Castro, Courville, Berseth, "Mitigating Plasticity Loss in Continual Reinforcement '
          'Learning by Reducing Churn" (arXiv:2506.00592; ICML 2025)', 'v1, 31 May 2025',
          'https://arxiv.org/abs/2506.00592', 'h3/src/pdf_2506.00592v1.txt')
CPR = ('McCutcheon, Chatzaroulas, Fallah, "Calibrated Partial Resets: Preventing Policy Collapse in Continual '
       'Reinforcement Learning" (arXiv:2607.24996; RLC Continual RL Workshop, oral)', 'v1, 27 Jul 2026',
       'https://arxiv.org/abs/2607.24996', 'h3/src/pdf_2607.24996v1.txt')
PLASTICINE = ('Yuan, Wang, Ma, Sun, Li, Jin et al., "Plasticine: Accelerating Research in Plasticity-Motivated Deep '
              'Reinforcement Learning" (arXiv:2504.17490)', 'v2, 10 Feb 2026', 'https://arxiv.org/abs/2504.17490',
              'h3/src/pdf_2504.17490v2.txt')
STREAMX = ('Elsayed, Lupu, Vasan, Mahmood, "Streaming Deep Reinforcement Learning Finally Works" (arXiv:2410.14606)',
           'v3, 21 Sep 2026', 'https://arxiv.org/abs/2410.14606', 'h3/src/pdf_2410.14606v3.txt')
SQUEEZE = ('Nilaksh, Clavaud, Reymond, Rivest, Chandar, "Squeezing More from the Stream: Learning Representation '
           'Online for Streaming Reinforcement Learning" (arXiv:2602.09396; ICML 2026 per OpenReview listing)',
           'v1, 10 Feb 2026', 'https://arxiv.org/abs/2602.09396', 'h3/src/pdf_2602.09396v1.txt')
INTENT = ('Sharifnassab, Elsayed, De Asis, Mahmood, Sutton, "Intentional Updates for Streaming Reinforcement '
          'Learning" (arXiv:2604.19033; ICML 2026 per OpenReview listing)', 'v1, 21 Apr 2026',
          'https://arxiv.org/abs/2604.19033', 'h3/src/pdf_2604.19033v1.txt')
AGAR = ('Mohamed, Nekhomiazh, Vyas, Jose, Patterson, Machado, "The Cell Must Go On: Agar.io for Continual '
        'Reinforcement Learning" (arXiv:2505.18347; Reinforcement Learning Journal 2026)', 'v3, 8 Aug 2026',
        'https://arxiv.org/abs/2505.18347', 'h3/src/pdf_2505.18347v3.txt')
COOBS = ('Hess, Jha, van de Ven, Tuytelaars, "Forgetting, plasticity, and co-observation: a third facet of continual '
         'learning" (arXiv:2608.18803; CoLLAs 2026)', 'v1, 19 Aug 2026', 'https://arxiv.org/abs/2608.18803',
         'h3/src/pdf_2608.18803v1.txt')
DASH = ('Shin, Oh, Cho, Yun, "DASH: Warm-Starting Neural Network Training in Stationary Settings without Loss of '
        'Plasticity" (arXiv:2410.23495; NeurIPS 2024)', 'v2, 1 Nov 2024', 'https://arxiv.org/abs/2410.23495',
        'h3/src/pdf_2410.23495v2.txt')
LIFETIME = ('Mesbahi, Panahi, Mastikhina, Tang, White, White, "Position: Lifetime tuning is incompatible with '
            'continual reinforcement learning" (arXiv:2404.02113; ICML 2025 position track)', 'v4, 8 Aug 2025',
            'https://arxiv.org/abs/2404.02113', 'h3/src/pdf_2404.02113v4.txt')
DEPLOY = ('Behdin, Roice, Mesbahi, "Position: Deployed Reinforcement Learning should be Continual" '
          '(arXiv:2606.04029; ICML 2026 position track)', 'v2, 6 Jun 2026', 'https://arxiv.org/abs/2606.04029',
          'h3/src/pdf_2606.04029v2.txt')
NATURE = ('Dohare, Hernandez-Garcia, Lan, Rahman, Mahmood, Sutton, "Loss of plasticity in deep continual learning", '
          'Nature 632, 768-774 (2024)', 'published version (Nature, 22 Aug 2024), open-access PDF',
          'https://www.nature.com/articles/s41586-024-07711-7', 'h3/src/nature_s41586-024-07711-7.txt')
ACTFN = ('Lillo, Cheney, "Activation Function Design Sustains Plasticity in Continual Learning" (arXiv:2509.22562; '
         'ICLR 2026)', 'v4, 30 Apr 2026', 'https://arxiv.org/abs/2509.22562', 'h3/src/pdf_2509.22562v4.txt')
BARRIERS = ('Joudaki, Lanzillotta, Razlighi, Mirzadeh, Alizadeh, Hofmann et al., "Barriers for Learning in an '
            'Evolving World: Mathematical Understanding of Loss of Plasticity" (arXiv:2510.00304)', 'v3, 17 May 2026',
            'https://arxiv.org/abs/2510.00304', 'h3/src/pdf_2510.00304v3.txt')
SPECTRAL = ('Prakash, He, Guo, Tiwari, Tao, Serapio et al., "Spectral Collapse Drives Loss of Plasticity in Deep '
            'Continual Learning" (arXiv:2509.22335)', 'v3, 29 May 2026', 'https://arxiv.org/abs/2509.22335',
            'h3/src/pdf_2509.22335v3.txt')
GRADUAL = ('Liu, Mou, "Do Neural Networks Lose Plasticity in a Gradually Changing World?" (arXiv:2602.09234)',
           'v2, 16 Jun 2026', 'https://arxiv.org/abs/2602.09234', 'h3/src/pdf_2602.09234v2.txt')
CRLSURV = ('Pan, Yang, Li, Wei, Li, An et al., "A Survey of Continual Reinforcement Learning" (arXiv:2506.21872)',
           'v2, 7 Apr 2026', 'https://arxiv.org/abs/2506.21872', 'h3/src/pdf_2506.21872v2.txt')
SSDE = ('Zheng, Yin, Chen, Ng, Ong, Tsang, "Mastering Continual Reinforcement Learning through Fine-Grained Sparse '
        'Network Allocation and Dormant Neuron Exploration" (arXiv:2503.05246)', 'v2, 10 Mar 2025',
        'https://arxiv.org/abs/2503.05246', 'h3/src/pdf_2503.05246v2.txt')
LLMSCALE = ('Hernandez-Garcia, Figliolia, Millidge, "Can Scale Save Us From Plasticity Loss in Large Language '
            'Models?" (arXiv:2606.24752)', 'v1, 23 Jun 2026', 'https://arxiv.org/abs/2606.24752',
            'h3/src/pdf_2606.24752v1.txt')


def C(cid, bottleneck, role, src, quote, note):
    source, version, url, raw = src
    return {'id': cid, 'bottleneck': bottleneck, 'role': role, 'source': source, 'version': version, 'url': url,
            'quote': quote, 'raw_file': raw, 'agent_note': note, 'note_by': AG}


CLAIMS = [
    # ================================================================================================================
    # h3-B1  Loss of plasticity in deep RL under task switches (continual RL with a single network)
    C('h3:1', 'h3-B1', 'a', KLEIN,
      ['Plasticity loss represents a fundamental challenge in deep RL, where networks progressively lose their ability '
       'to learn despite remaining capacity.'],
      'Problem statement (the survey\'s conclusion).'),
    C('h3:2', 'h3-B1', 'b', KLEIN,
      ['This variability highlights a critical gap: We cannot yet predict which environment properties will cause '
       'severe plasticity loss and which interventions will prove effective for a given task.',
       'However, fundamental understanding remains limited despite empirical progress.'],
      '2026 (v3, 18 Apr 2026): states the problem open, both in prediction and in mechanism.'),
    C('h3:3', 'h3-B1', 'b', PLASTICINE,
      ['Despite its significance, this field lacks unified benchmarks and evaluation protocols.',
       'Accurately quantifying neural network plasticity remains an open research question'],
      '2026 (v2, 10 Feb 2026): the field lacks a benchmark and a measure; no table of numbers (figures only).'),
    C('h3:4', 'h3-B1', 'c', CCHAIN,
      ['Table 1. Performance comparison on continual Gym Control.',
       'Oracle Vanilla TRAC Weight Clipping L2 Init C-CHAIN',
       'C-CartPole 299.925 ± 5.986 61.766 ± 6.927 217.376 ± 26.307 154.306 ± 16.047 266.114 ± 5.345 160.396 ± 14.643',
       'C-LunarLander 1.118 ± 2.002 -499.396 ± 19.571 -58.059 ± 17.474 -58.575 ± 2.896 −6.666 ± 5.903 '
       '-16.659 ± 8.369',
       'Agg. Score -147.302 -1156.958 -407.256 -290.99 -243.985 −221.22',
       'we use a PPO agent that gets fully re-initialized every time the task is switched to be the oracle baseline.'],
      'Benchmark: continual Gym Control (CartPole, Acrobot, LunarLander, MountainCar, each chained k times with a fixed '
      'Gaussian observation noise per instance). Target: the Oracle (PPO re-initialised at every task switch). Best '
      'single method on the aggregate: C-CHAIN -221.22 against Oracle -147.302, short by 73.92 return units (summed '
      'over 4 envs). Per env the best non-oracle method trails the Oracle on C-CartPole (L2 Init 266.114 vs 299.925, '
      '-33.81) and C-LunarLander (L2 Init -6.666 vs 1.118, -7.78) but is ahead on C-Acrobot (Weight Clipping -118.821 '
      'vs -125.736) and C-MountainCar (C-CHAIN -245.746 vs -322.608). MIXED: see h3:5, the same paper\'s ProcGen table '
      'has methods above the Oracle.'),
    C('h3:5', 'h3-B1', 'c', CCHAIN,
      ['One may note that TRAC, L2 Init and C-CHAIN outperform Oracle in ProcGen.',
       'Oracle still suffers from plasticity loss due to the change of sampling and policy'],
      'Counter-evidence to the gap: on continual ProcGen the per-task re-initialised Oracle is exceeded, so the Oracle '
      'is not an upper bound there. The gap in h3:4 holds on Gym Control only (2 of 4 envs, and the aggregate).'),
    C('h3:6', 'h3-B1', 'c', CPR,
      ['Table 2: Continual MinAtar IQM of return over training steps and final performance using 5 seeds with IQR',
       'Method Avg Final CPR 75.6 ± 14.3 52.3 ± 25.0 CBP 65.6 ± 3.2 5.8 ± 14.9'],
      'Context, no external target: on Continual MinAtar the best method (CPR) ends at 52.3 final IQM return against '
      'its own 75.6 average over training (every method\'s final is below its average). Shows decline within the '
      'stream, not a gap to a stated target; not used for the open flag.'),
    C('h3:7', 'h3-B1', 'd', KLEIN,
      ['Non-targeted weight resets periodically reinitialize network layers to restore plasticity and were initially '
       'proposed to mitigate early overfitting',
       'Such quantification is necessary for principled regularization selection: stronger non-stationarity should '
       'require stronger regularization, but without measurement tools, this principle cannot be implemented.',
       'we recommend that practitioners encountering plasticity loss should start with general regularization '
       'techniques such as LayerNorm and SpectralNorm.'],
      'Assumptions: resets are scheduled on the clock (periodic); regularisation strength is a fixed hyperparameter '
      'because the degree of non-stationarity is not measured; general regularisers (LayerNorm, SpectralNorm, L2) are '
      'held fixed through the stream.'),
    C('h3:8', 'h3-B1', 'd', CCHAIN,
      ['Adam with Relative Timesteps (AdamRel)',
       'The oracle baseline learns each task from ran-dom initialization, thus free of the influence of task change.'],
      'Assumptions: AdamRel resets Adam\'s timestep at each task switch and the Oracle re-initialises at each switch; '
      'both need the task boundary supplied from outside the learner.'),
    C('h3:9', 'h3-B1', 'd', CPR,
      ['an optimizer that periodically pulls low-utility neurons toward their initialization, with pull strength '
       'scaled by each neuron’s utility.',
       'Ablations reveal a tunable trade-off between plasticity and peak performance'],
      'Assumption: the refresh is periodic (clock-scheduled) and its strength is a tuned constant.'),

    # ================================================================================================================
    # h3-B2  Streaming deep RL (no replay, batch size 1): the gap to batch/replay methods
    C('h3:10', 'h3-B2', 'a', STREAMX,
      ['However, reliable streaming learning has remained a persistent challenge in modern deep reinforcement learning '
       '(RL).',
       'We call this phenomenon stream barrier; overcoming it remains an open problem, which we address in this work.'],
      'Problem statement (v3 is dated 21 Sep 2026; the paper claims to address it).'),
    C('h3:11', 'h3-B2', 'b', SQUEEZE,
      ['As a result, streaming RL is severely sample-inefficient: each transition is expensive to obtain, and its '
       'informational content is only weakly exploited before being discarded.',
       'Not many works study representation learning in a streaming fashion (Han et al., 2025), and none do for '
       'streaming RL, making this an open challenge.'],
      '2026 (10 Feb 2026): states sample efficiency of streaming RL as unsolved.'),
    C('h3:12', 'h3-B2', 'b', INTENT,
      ['In several environments, Intentional AC closes most of the gap between streaming learning and replay-based '
       'training.',
       'There remain several open problems and natural next steps.'],
      '2026 (21 Apr 2026): "most of the gap", in "several environments", i.e. not all of it everywhere. Its abstract '
      'also says "frequently performing on par with batch and replay-buffer approaches"; its numbers are in figures.'),
    C('h3:13', 'h3-B2', 'c', STREAMX,
      ['SAC1 PPO1 IAC Stream-AC Best(PPO, SAC): 1.00 0.04 0.07 0.00 0.73 Continuous control 50 tasks',
       'DQN1 Q-learning Stream-Q DQN: 0.67 0.00 0.15 0.99 Atari 58 games',
       'One denotes the best average return among all methods including buffer settings.'],
      'Benchmark: 50 continuous-control tasks (MuJoCo Gym + DM Control; 5M steps each), median normalised score. Best '
      'streaming: Stream-AC 0.73; target: per-task best of batch SAC (1e6 replay) or PPO (2048 rollout) = 1.00. Gap '
      '0.27 (streaming reaches 73% of the batch reference on the median task). On 58 Atari games (200M frames) '
      'Stream-Q 0.99 is ABOVE batch DQN 0.67: no gap there. Figure-panel text as extracted from the PDF.'),
    C('h3:14', 'h3-B2', 'd', STREAMX,
      ['Instead, most deep RL algorithms learn from old experience by storing past interactions in a buffer—an '
       'approach that can be restrictive in resource-constrained and privacy-sensitive applications.',
       'Using one prescribed hyperparameter configuration per algorithm across tasks, Stream-X substantially improves '
       'aggregate performance, often on par with batch RL algorithms.'],
      'Assumptions: batch methods store the past (replay buffer, rollouts); Stream-X holds one step size and trace '
      'parameter fixed for the whole stream and all tasks.'),
    C('h3:15', 'h3-B2', 'd', INTENT,
      ['In gradient-based learning, a step size chosen in parameter units does not produce a predictable per-step '
       'change in function output.',
       'We deliberately avoided learning-rate schedules and decay to respect the continual nature of RL.',
       'Intentional updates still use a global scale η'],
      'Assumption named and partly denied by the frontier itself: the step size is set in parameter units; Intentional '
      'updates instead fix the intended change in output (TD-error fraction, policy KL) but keep a global scale eta '
      'fixed. Relevant to any CRR reading that indexes updates by the learner\'s own change (stage 2).'),

    # ================================================================================================================
    # h3-B3  Continual RL in a non-episodic world with endogenous non-stationarity (AgarCL)
    C('h3:16', 'h3-B3', 'a', AGAR,
      ['However, transforming episodic problems into continual ones primarily captures scenarios involving abrupt '
       'changes in the data stream and still relies on episodic structure.'],
      'Problem statement: the usual continual-RL benchmarks are episodic tasks with abrupt switches.'),
    C('h3:17', 'h3-B3', 'b', AGAR,
      ['Finally, our empirical study exposes persistent challenges in continual RL research, particularly regarding '
       'evaluation methodology and hyperparameter sensitivity,',
       'The transition from episodic to continual variants further amplifies these difficulties, revealing sharp '
       'degradation once resets are removed.',
       'More complex interactions, such as competition and virus-based strategies, remain entirely unsolved.'],
      '2026 (v3, 8 Aug 2026; Reinforcement Learning Journal 2026).'),
    C('h3:18', 'h3-B3', 'c', AGAR,
      ['Category Mini-game Scenarios DQN PPO SAC Human Random',
       'Pellet Collection (Continual) 1 — 619 (7.9) 335 (3.0) 419 (0.2) 700 (0) 0.01 (0.1) 2 — 0 (0) 0 (0) 2 (1.7) '
       '682 (0) 0 (0)',
       'Dense −828 (10.5) 5064.4 (113.6) −968 (0.01) 7215 (0) −973 (1.1)',
       'Full Game (Grand Arena) — — 4 (3.1) 8 (8.3) 22 (11.1) — 0.06 (0.18)'],
      'Benchmark: AgarCL (Table 9; continual pellet-collection mini-games, final 100 steps, 10 runs). Target: the '
      'Human column. Best agent vs Human: continual mini-game 1, DQN 619 vs 700 (88.4%); mini-game 2, SAC 2 vs 682 '
      '(0.3%); mini-game 6 Dense, PPO 5064.4 vs 7215 (70.2%). Full game: best SAC 22 against random 0.06, no human '
      'reference. Column reading of the extracted row is the agent\'s (Scenarios cell "—" precedes DQN).'),
    C('h3:19', 'h3-B3', 'd', AGAR,
      ['Results for the continual learning baselines were obtained with standard hyperparameters.',
       'Despite their strong performance in many established benchmarks, none of these methods achieves sustained '
       'competence in the full game.',
       'We therefore reuse the best hyperparameters identified for AgarCL’s continual MINI-GAME 4, the setting most '
       'similar to the full game but considerably shorter.'],
      'Assumptions: the plasticity methods (Shrink & Perturb, ReDo, Continual Backprop) were designed and tuned on '
      'episodic benchmarks with abrupt switches; hyperparameters are carried over from a shorter horizon.'),

    # ================================================================================================================
    # h3-B4  Warm-started / data-incremental training falls short of offline joint training
    C('h3:20', 'h3-B4', 'a', DASH,
      ['However, it often leads to loss of plasticity, where the network loses its ability to learn new information, '
       'resulting in worse generalization than training from scratch.'],
      'Problem statement for warm-starting (2024).'),
    C('h3:21', 'h3-B4', 'a', COOBS,
      ['we show that these two issues cannot fully explain the performance gap between naive sequential training and '
       'offline joint training.',
       'the gap between the incremental joint model and the (offline) joint target highlights the loss of plasticity.'],
      'Problem statement (2026): the gap to offline joint training has a plasticity part and a co-observation part.'),
    C('h3:22', 'h3-B4', 'b', COOBS,
      ['Efficient continual learning remains a fundamental challenge for deep neural networks.',
       'How to best facilitate such synergies, especially in compute-bounded settings, needs to be the subject of '
       'further research.'],
      '2026 (19 Aug 2026; CoLLAs 2026).'),
    C('h3:23', 'h3-B4', 'c', COOBS,
      ['Table 2: SL-IN-100 - LP-accuracy[%] IN-100',
       'Incremental Joint 73.24±0.48 79.58±0.12 81.85±0.10 82.75±0.15 Joint (offline) – – – 83.68±0.11',
       'Replay (mt =12500) 73.25±0.07 78.05±0.07 80.68±0.15 81.27±0.24 LwF 73.35±0.23 77.41±0.15 79.44±0.22 '
       '79.93±0.25'],
      'Benchmark: ImageNet-100, 4 i.i.d. chunks, ResNet-18 from scratch, linear-probe accuracy after chunk 4. Target: '
      'Joint (offline) 83.68. Warm-started incremental joint (all data so far, continued from the previous chunk) '
      '82.75: short by 0.93 pt (the paper\'s plasticity gap). Best continual method (Replay, 12500 per chunk, ~30%) '
      '81.27: short by 2.41 pt. LwF 79.93: short by 3.75 pt.'),
    C('h3:24', 'h3-B4', 'c', DASH,
      ['Random Init 25.69 (0.13) 31.30 (0.09)',
       'DASH 46.11 (0.34) 49.57 (0.36)'],
      'Counter-evidence (2024, own protocol): on Tiny-ImageNet (ResNet-18, data added in stages from a stationary '
      'distribution) DASH\'s last-experiment test accuracy (46.11 SGD / 49.57 SAM) is above cold-start random init '
      '(25.69 / 31.30). The warm-start gap is closed there; not tested in h3:23\'s protocol.'),
    C('h3:25', 'h3-B4', 'd', COOBS,
      ['For fair comparison, all training is constrained to an identical, fixed iteration budget per chunk.',
       'Storing approximately 15% of the data appears sufficient for the replay mechanism to effectively match the '
       'performance of the ensemble.',
       'the linear probing accuracy pushes past the ensemble baseline, closing half the gap to incremental joint '
       'training.'],
      'Assumptions: the chunk boundaries are given; a fixed step budget per chunk; replay must store 15-30% of the '
      'data to recover co-observation.'),
    C('h3:26', 'h3-B4', 'd', DASH,
      ['a method aiming to mitigate plasticity loss by selectively forgetting memorized noise while preserving learned '
       'features.'],
      'Assumption: the data distribution is stationary (the title\'s "Stationary Settings"); shrinking is applied at '
      'each new data arrival (given boundaries).'),

    # ================================================================================================================
    # h3-B5  Hyperparameters without a natural horizon (lifetime tuning)  -- NOT SHOWN OPEN (no numbers in text)
    C('h3:27', 'h3-B5', 'a', LIFETIME,
      ['The standard practice in RL is to assume unfettered access to the deployment environment for the full lifetime '
       'of the agent.',
       'lifetime tuning does not allow us to identify algorithms that work well for continual learning—all algorithms '
       'equally succeed;'],
      'Problem statement (ICML 2025 position).'),
    C('h3:28', 'h3-B5', 'b', AGAR,
      ['Hyperparameter tuning is a central yet often overlooked challenge in continual RL.',
       'This pragmatic choice reflects a broader open question in continual RL: how should hyperparameters be selected '
       'when no natural training horizon exists?'],
      '2026 (v3, 8 Aug 2026).'),
    C('h3:29', 'h3-B5', 'b', DEPLOY,
      ['CRL research should treat hyperparameter tuning as part of online deployment, not a hidden offline phase',
       'Degris et al. (2024) showed that two commonly used optimizers, RMSProp (Hinton et al., 2012) and Adam (Kingma '
       '& Ba, 2015), were unsuitable for step-size adaptation in a simple continual learning scenario.'],
      '2026 (ICML 2026 position track). Also a d-type statement: Adam/RMSProp step-size adaptation assumes a stationary '
      'gradient scale.'),
    C('h3:30', 'h3-B5', 'd', LIFETIME,
      ['Instead, we suggest a limited tuning phase: a small percent of the total lifetime.',
       'The learning rate is particularity sensitive to lifetime.',
       'Tuning on one-percent of a lifetime leads to poor performance in Continuing Cartpole, whereas lifetime tuning '
       'allows DQN to achieve nearly optimal performance.'],
      'Assumptions: a fixed hyperparameter vector chosen once (on 1% or on 100% of the lifetime) and held fixed. The '
      'results are in figures only (no numbers in the text): no role-c claim, so NOT SHOWN OPEN by the declaration\'s '
      'rule. ("particularity" is the source\'s spelling.)'),

    # ================================================================================================================
    # h3-B6  Loss of plasticity in supervised learning on standard long task sequences  -- NOT SHOWN OPEN
    C('h3:31', 'h3-B6', 'a', NATURE,
      ['Here we show that they do not—that standard deep-learning methods gradually lose plasticity in continual-learning '
       'settings until they learn no better than a shallow network.',
       'Although these networks learned up to 88% correct on the test set of the early tasks'],
      'Problem statement (2024) with the magnitude on Continual ImageNet (88% early, falling toward the linear '
      'baseline by the 2,000th task; the later numbers are in figures).'),
    C('h3:32', 'h3-B6', 'b', ACTFN,
      ['Despite growing interest, loss of plasticity remains less understood and underexplored,'],
      '2026 (ICLR 2026): open as understanding, not as a benchmark gap.'),
    C('h3:33', 'h3-B6', 'b', BARRIERS,
      ['Several questions remain open.'],
      '2026 (v3, 17 May 2026): open questions are theoretical (non-linear LoP manifolds, stability conditions).'),
    C('h3:34', 'h3-B6', 'c', SPECTRAL,
      ['a RESET baseline that reinitializes parameters at each task change; algorithms outperforming RESET are '
       'considered to maintain plasticity.',
       'L2-ER maintains plasticity in all, and provides an early performance boost on Permuted MNIST before plasticity '
       'loss would typically occur.'],
      'Frontier reports the target reached: on Permuted MNIST, Continual ImageNet, Incremental CIFAR and Slippery Ant '
      'the paper\'s method is above its RESET target in all four (numbers in figures only). With no quoted number '
      'short of a target, NOT SHOWN OPEN on these benchmarks.'),
    C('h3:35', 'h3-B6', 'd', GRADUAL,
      ['A common thread across these studies is the use of benchmarks with abrupt task transitions;',
       'showing that the severity of plasticity loss is closely tied to the abruptness of task transitions, and can be '
       'substantially reduced when the environment changes gradually.'],
      'Assumption of the benchmarks: abrupt, externally scheduled task switches.'),
    C('h3:36', 'h3-B6', 'd', NATURE,
      ['a variation of backpropagation in which a small fraction of less-used units are continually and randomly '
       'reinitialized.'],
      'Continual backprop: a fixed replacement rate per step (clock-indexed) and a fixed maturity threshold.'),

    # ================================================================================================================
    # h3-B7  Predicting plasticity loss / measuring non-stationarity  -- NOT SHOWN OPEN (no numbers)
    C('h3:37', 'h3-B7', 'b', KLEIN,
      ['More fundamentally, the field lacks methods to quantify the degree of non-stationarity in a given learning '
       'problem.',
       'Despite substantial empirical progress, we lack theoretical frameworks to predict when plasticity loss will '
       'occur or which interventions will work for a given problem.'],
      '2026. Problem and open statement in one source; no benchmark with a target number exists, so NOT SHOWN OPEN.'),

    # ================================================================================================================
    # h3-B8  Task-free continual RL (no task boundaries supplied)  -- NOT SHOWN OPEN (no numbers)
    C('h3:38', 'h3-B8', 'a', CRLSURV,
      ['Most CRL methods assume that tasks are given in advance, the boundaries between tasks are clear, and the '
       'environment is stationary within a task.'],
      'Problem statement and the assumption (d-type) in one sentence.'),
    C('h3:39', 'h3-B8', 'b', CRLSURV,
      ['Task-free CRL is a challenging problem that requires agents to learn from the environment without any explicit '
       'tasks.'],
      '2026 (v2, 7 Apr 2026).'),
    C('h3:40', 'h3-B8', 'c', SSDE,
      ['TABLE I: Benchmark evaluation results on Continual World (v1).',
       'MTL+PopArt [36] 0.66 ±0.04 − − 0.65 ±0.03 − − SSDE (Ours) 0.95 ±0.02 0.00 ±0.00 0.30 ±0.02'],
      'Task-LABELLED setting only: on CW10 SSDE\'s average success 0.95 is above the multi-task reference MTL+PopArt '
      '0.66, so the task-given benchmark does not show a gap. No task-free benchmark with numbers and a target was '
      'found: NOT SHOWN OPEN.'),

    # ================================================================================================================
    # h3-B9  Plasticity loss at LLM scale  -- NOT SHOWN OPEN (no target; overlaps H2)
    C('h3:41', 'h3-B9', 'a', LLMSCALE,
      ['These results suggest that larger models may delay the measurable effects of plasticity loss, but that '
       'increasing parameter count alone is likely to be insufficient to completely prevent it.'],
      '2026. No mitigation method and no target number; overlaps family H2.'),
]


BOTTLENECKS = [
    {'id': 'h3-B1', 'name': 'plasticity loss in deep RL under task switches',
     'problem': 'A single deep RL network trained through a sequence of task switches learns later tasks worse than a '
                'network re-initialised at each switch.',
     'open': True,
     'benchmark': 'continual Gym Control (C-CHAIN, ICML 2025; 4 envs chained with observation noise)',
     'best': 'Agg. Score −221.22 (C-CHAIN)',
     'target': 'Agg. Score -147.302 (Oracle: PPO re-initialised at every task switch)',
     'gap_note': 'Aggregate short by 73.92 return units; per env the Oracle leads on CartPole (by 33.81) and LunarLander '
                 '(by 7.78) but trails on Acrobot and MountainCar; on continual ProcGen methods exceed the Oracle. '
                 'Open, but mixed: the target is not an upper bound everywhere.',
     'assumptions': ['resets and refreshes scheduled on the clock (periodic)',
                     'task boundary supplied from outside (Oracle re-init, AdamRel timestep reset)',
                     'regularisation strength a fixed tuned constant, because non-stationarity is not measured',
                     'general regularisers (LayerNorm, SpectralNorm, L2) held fixed through the stream'],
     'cpu_testable': True,
     'cpu_note': 'Gym Control envs with small MLP PPO agents run on a laptop CPU; a reduced chain (fewer seeds or tasks) '
                 'fits in hours with public simulators (gymnasium). ProcGen/MinAtar variants are heavier.'},
    {'id': 'h3-B2', 'name': 'streaming deep RL vs batch/replay',
     'problem': 'Learning from each transition once, without a replay buffer or batches, still reaches less return than '
                'batch methods on continuous control.',
     'open': True,
     'benchmark': '50 continuous-control tasks (MuJoCo Gym + DM Control), median normalised score, Stream-X v3',
     'best': 'Stream-AC 0.73',
     'target': 'Best(PPO, SAC): 1.00',
     'gap_note': 'Streaming reaches 73% of the batch reference on the median task (gap 0.27). On 58 Atari games '
                 'Stream-Q 0.99 exceeds batch DQN 0.67, so the gap is specific to continuous control. A 2026 successor '
                 '(Intentional AC) reports closing "most of the gap" in several environments, figures only.',
     'assumptions': ['batch methods store the past (replay buffer, rollouts)',
                     'one prescribed step size and trace parameter held fixed for the whole stream and all tasks',
                     'step size set in parameter units (Intentional updates move to output units but keep a global '
                     'scale fixed)',
                     'no learning-rate schedule (clock-indexed decay rejected as non-continual)'],
     'cpu_testable': True,
     'cpu_note': 'Streaming updates are batch size 1 and CPU-friendly (Stream-Q even runs on a microcontroller); a subset '
                 'of MuJoCo tasks at reduced step counts fits in hours; the full 50 tasks x 5M steps x 30 seeds does not.'},
    {'id': 'h3-B3', 'name': 'non-episodic continual RL with endogenous drift (AgarCL)',
     'problem': 'In a non-episodic world whose dynamics change with the agent\'s own play, deep RL and plasticity methods '
                'fail to reach human-level or sustained competence.',
     'open': True,
     'benchmark': 'AgarCL continual pellet-collection mini-games (Table 9)',
     'best': 'mini-game 6 Dense: PPO 5064.4; mini-game 2: SAC 2; mini-game 1: DQN 619',
     'target': 'Human 7215 (mini-game 6), 682 (mini-game 2), 700 (mini-game 1)',
     'gap_note': 'Best agent at 70.2%, 0.3% and 88.4% of the human reference on three continual mini-games; full game '
                 'has no human reference (best SAC 22, random 0.06).',
     'assumptions': ['plasticity methods designed and tuned on episodic benchmarks with abrupt switches',
                     'hyperparameters carried over from a shorter horizon (mini-game 4)',
                     'standard (untuned) hyperparameters for the continual baselines'],
     'cpu_testable': False,
     'cpu_note': 'The source reports more than seven days on a single machine for SAC on the full game; mini-games are '
                 'millions of frames with pixel observations. Not laptop-CPU hours.'},
    {'id': 'h3-B4', 'name': 'warm-started / data-incremental training short of offline joint',
     'problem': 'Training that continues from the previous model as data arrives in chunks ends below a model trained '
                'once on all the data, even without distribution shift.',
     'open': True,
     'benchmark': 'ImageNet-100 in 4 i.i.d. chunks, ResNet-18 from scratch, linear-probe accuracy (Hess et al. 2026)',
     'best': 'Incremental Joint 82.75±0.15 (warm-started, all data); Replay (mt =12500) 81.27±0.24 (best continual)',
     'target': 'Joint (offline) 83.68±0.11',
     'gap_note': 'Warm-started on all data: 0.93 pt short (plasticity part). Best continual method: 2.41 pt short. DASH '
                 '(2024) closes the warm-start gap on its own protocol, untested here.',
     'assumptions': ['chunk boundaries given', 'fixed iteration budget per chunk',
                     'replay stores 15-30% of the data to recover co-observation',
                     'stationary data (DASH)'],
     'cpu_testable': False,
     'cpu_note': 'The named benchmark is ResNet-18 on ImageNet-100/CIFAR-100 for about 100 epoch-equivalents: GPU-days, '
                 'not CPU-hours. A small-MLP analogue would run on CPU but is not the named benchmark.'},
    {'id': 'h3-B5', 'name': 'hyperparameters without a natural horizon (lifetime tuning)',
     'problem': 'Continual-RL agents are tuned over their full evaluation lifetime; tuned on a fraction, several '
                'algorithms collapse, and no rule says what horizon to tune for.',
     'open': False,
     'benchmark': 'Continuing Cartpole, Non-stationary Catch, quadruped walk-to-run (Mesbahi et al.); AgarCL',
     'best': 'not quoted (figures only)', 'target': 'not quoted (lifetime-tuned DQN "nearly optimal")',
     'gap_note': 'Open by 2026 statements (AgarCL, ICML 2026 position), but no number in any text: NOT SHOWN OPEN.',
     'assumptions': ['one hyperparameter vector chosen before deployment and held fixed',
                     'tuning horizon = the evaluation lifetime (or k% of it)',
                     'Adam/RMSProp step-size adaptation assumes a stationary gradient scale'],
     'cpu_testable': True,
     'cpu_note': 'Continuing Cartpole and Non-stationary Catch with DQN run on CPU in hours.'},
    {'id': 'h3-B6', 'name': 'supervised loss of plasticity on long task sequences',
     'problem': 'Networks trained by backpropagation through thousands of tasks lose the ability to learn new ones.',
     'open': False,
     'benchmark': 'Continual ImageNet, Permuted MNIST, Incremental CIFAR-100, Slippery Ant',
     'best': 'L2-ER above RESET on all four (figures)', 'target': 'RESET (re-initialise at each task change)',
     'gap_note': 'The 2026 frontier reports the target reached on these benchmarks; open statements concern mechanism '
                 'and theory, not a benchmark gap. NOT SHOWN OPEN.',
     'assumptions': ['abrupt, externally scheduled task switches in the benchmarks',
                     'fixed replacement rate per step (continual backprop)',
                     'fixed regularisation strength'],
     'cpu_testable': True,
     'cpu_note': 'Permuted MNIST and slowly-changing regression run on CPU in hours.'},
    {'id': 'h3-B7', 'name': 'predicting plasticity loss / measuring non-stationarity',
     'problem': 'There is no measure of a problem\'s non-stationarity that predicts plasticity loss or sets '
                'regularisation strength.',
     'open': False, 'benchmark': 'none named', 'best': 'none', 'target': 'none',
     'gap_note': 'Stated open (Klein et al. 2026) but no benchmark or number: NOT SHOWN OPEN.',
     'assumptions': ['regularisation strength fixed because non-stationarity is unmeasured'],
     'cpu_testable': True, 'cpu_note': 'Synthetic streams would suffice, but there is no benchmark to test against.'},
    {'id': 'h3-B8', 'name': 'task-free continual RL',
     'problem': 'Most continual-RL methods need task boundaries supplied; learning without them is a named challenge.',
     'open': False, 'benchmark': 'none task-free with numbers; Continual World CW10 (task-labelled)',
     'best': 'SSDE 0.95 (CW10, task-labelled)', 'target': 'MTL+PopArt 0.66 (multi-task reference)',
     'gap_note': 'The task-labelled benchmark is above its multi-task reference; no task-free benchmark with a target '
                 'was found. NOT SHOWN OPEN.',
     'assumptions': ['tasks given in advance, boundaries clear, stationary within a task'],
     'cpu_testable': False, 'cpu_note': 'Continual World (MetaWorld, SAC, 1M steps per task) is GPU-scale; no task-free '
                                         'benchmark named.'},
    {'id': 'h3-B9', 'name': 'plasticity loss at LLM scale',
     'problem': 'GPT-style models from 5M to 314M parameters lose plasticity on a multilingual continual problem; scale '
                'delays but does not prevent it.',
     'open': False, 'benchmark': 'Multilingual Continual Learning Problem (Hernandez-Garcia et al. 2026)',
     'best': 'none (no mitigation reported)', 'target': 'none stated',
     'gap_note': 'No target and no mitigation: NOT SHOWN OPEN here (overlaps H2).',
     'assumptions': ['fixed training budget per cycle'],
     'cpu_testable': False, 'cpu_note': 'Transformer pre-training at 5M-314M parameters is GPU-scale.'},
]
