"""OB1 stage 1, family H4 (deployment constraints): the quoted claims and the bottleneck table.

Family H4 of `Open_Bottlenecks/DECLARATION.md`: task-free or boundary-free streams, choosing hyperparameters without
future data (tuning-free / realistic hyperparameter selection), compute-budgeted continual learning, and on-device
(resource-constrained) continual learning. The dossier is `docs/citations/ob1_h4_2026-09-30.md`.

Every quote is copied from the text that pymupdf 1.28.2 extracted from the fetched PDF (current arXiv version, fetched
2026-09-30 through the session proxy). The extracted texts are held outside the repository under
/tmp/claude-0/ob1_src/ (third-party full texts, not committed); `raw_file` is relative to that root, and the sha256 of
every fetched and extracted file is in /tmp/claude-0/ob1_src/h4/SHA256SUMS.txt. Whitespace in a quote is normalised
(one space); line-break hyphens are rejoined; table rows are quoted cell by cell in the extractor's reading order.

Roles (the declaration's Stage 1): 'a' the problem; 'b' a 2025-26 statement that it is open, unsolved or a main
challenge; 'c' the best reported number on a named benchmark and the target it is compared with; 'd' a method family
tried and the assumption it makes. The `agent_note` is the agent's reading, not evidence.

Reading rule for `open` (the agent's, for review): True only if the bottleneck has role a, b and c claims AND the
best reported result on the named benchmark falls short of the stated target by more than the reported spread.
A bottleneck with a 2025-26 statement but whose quoted numbers show the best result at (or within about one point of)
the target is recorded with open=False ("not shown open"), not dropped.
"""

CLAIMS = [
    # ---------------------------------------------------------------- h4-B1: boundary-free (task-free / GCL) streams
    {'id': 'h4:0', 'bottleneck': 'h4-B1', 'role': 'a',
     'source': 'Park, Lee & Lee, "Is Prompt Selection Necessary for Task-Free Online Continual Learning?" (CVPR Findings 2026)',
     'version': 'arXiv:2604.04420v1 (6 Apr 2026)', 'url': 'https://arxiv.org/abs/2604.04420v1',
     'quote': ['Task-free online continual learning has recently emerged as a realistic paradigm for addressing continual '
               'learning in dynamic, real-world environments, where data arrive in a non-stationary stream without clear '
               'task boundaries and can only be observed once.'],
     'raw_file': 'h4/txt/2604.04420v1.txt',
     'agent_note': 'Problem statement: no task boundaries, single pass.'},
    {'id': 'h4:1', 'bottleneck': 'h4-B1', 'role': 'b',
     'source': 'Yan et al., "FlyPrompt: Brain-Inspired Random-Expanded Routing with Temporal-Ensemble Experts for General '
               'Continual Learning" (ICLR 2026)',
     'version': 'arXiv:2602.01976v3 (24 Mar 2026)', 'url': 'https://arxiv.org/abs/2602.01976v3',
     'quote': ['We therefore identify two fundamental challenges that remain unresolved: (1) how to dynamically route inputs '
               'to appropriate experts without task labels or iterative training, and (2) how to ensure that each expert '
               'maintains strong and adaptive representations under sparse and imbalanced supervision. Both remain '
               'non-trivial'],
     'raw_file': 'h4/txt/2602.01976v3.txt',
     'agent_note': '2026 statement that boundary-free (GCL) learning has unresolved core problems.'},
    {'id': 'h4:2', 'bottleneck': 'h4-B1', 'role': 'b',
     'source': 'Sun et al., "MePo: Meta Post-Refinement for Rehearsal-Free General Continual Learning" (ICML 2026 per OpenReview)',
     'version': 'arXiv:2602.07940v3 (11 May 2026)', 'url': 'https://arxiv.org/abs/2602.07940v3',
     'quote': ['these methods remain limited in reconciling the diverse and temporally mixed information along a single pass, '
               'resulting in sub-optimal GCL performance.'],
     'raw_file': 'h4/txt/2602.07940v3.txt',
     'agent_note': 'Second 2026 statement (pretrained-model methods under blurry, single-pass streams).'},
    {'id': 'h4:3', 'bottleneck': 'h4-B1', 'role': 'c',
     'source': 'Michel, Wang, He & Yamasaki, "From Offline to Online Memory-Free and Task-Free Continual Learning via '
               'Fine-Grained Hypergradients" (under review)',
     'version': 'arXiv:2502.18762v2 (7 Jun 2025)', 'url': 'https://arxiv.org/abs/2502.18762v2',
     'quote': ['Table 1: Average Performances (%) of all considered baselines, in the Si-Blurry setting.',
               'Table 2: Average Performances (%) of all considered baselines, in the clear setting.',
               'ConvPrompt 24.55±3.8 75.01±5.16 75.01±5.16 0.64±0.23 56.27±0.84 56.27±0.84 1.18±0.02 46.75±1.8 46.75±1.8 '
               ',→+ ours 44.23±3.29 86.34±3.59 86.34±3.59 4.43±1.13 73.88±0.87 73.88±0.87 3.78±0.22 62.62±0.11 62.62±0.11',
               'ConvPrompt 33.8±0.71 73.88±3.15 73.88±3.15 2.14±0.54 65.96±2.78 65.96±2.78 3.07±0.37 59.6±0.29 59.6±0.29 '
               ',→+ ours 60.07±1.37 87.65±0.37 87.65±0.37 5.54±1.1 75.73±0.12 75.73±0.12 6.89±0.32 69.76±1.38 69.76±1.38'],
     'raw_file': 'h4/txt/2502.18762v2.txt',
     'agent_note': 'Columns: CIFAR100, CUB, Imagenet-R, each at LR 5e-5 | 5e-3 | Best HP (tuned on VTAB). The best '
                   'Si-Blurry (no boundaries) row in Table 1 is ConvPrompt + ours; the same method with clear boundaries '
                   '(Table 2) is the boundary-oracle target. Best HP: ImageNet-R 62.62 vs 69.76 (gap 7.14 points); '
                   'CUB 73.88 vs 75.73 (1.85); CIFAR100 86.34 vs 87.65 (1.31, inside the 3.59 spread). Si-Blurry also '
                   'varies task sizes and class overlap, so the gap is not boundary knowledge alone (agent caveat).'},
    {'id': 'h4:4', 'bottleneck': 'h4-B1', 'role': 'c',
     'source': 'Yan et al., FlyPrompt (ICLR 2026)',
     'version': 'arXiv:2602.01976v3 (24 Mar 2026)', 'url': 'https://arxiv.org/abs/2602.01976v3',
     'quote': ['Table 2: Comparison with prominent offline methods on three GCL benchmarks under Sup-21K.',
               'FlyPrompt (Ours) 83.24±2.23 86.76±0.73 56.58±1.47 55.27±0.91 70.64±2.85 73.40±1.88'],
     'raw_file': 'h4/txt/2602.01976v3.txt',
     'agent_note': 'State of the art on Si-Blurry (CIFAR-100, ImageNet-R, CUB-200; Aauc then Alast): ImageNet-R '
                   'Alast 55.27. The paper reports no joint or boundary-aware target, so this row fixes the level only.'},
    {'id': 'h4:5', 'bottleneck': 'h4-B1', 'role': 'd',
     'source': 'Park, Lee & Lee (CVPR Findings 2026)', 'version': 'arXiv:2604.04420v1 (6 Apr 2026)',
     'url': 'https://arxiv.org/abs/2604.04420v1',
     'quote': ['many recent approaches have employed prompt selection, an adaptive strategy that selects prompts from a pool '
               'based on input signals.',
               'we observe that such selection strategies often fail to select appropriate prompts',
               '(iii) mask logits for unexposed classes in the current minibatch.'],
     'raw_file': 'h4/txt/2604.04420v1.txt',
     'agent_note': 'Families: key-query prompt selection (assumes the input identifies its expert); the fix drops '
                   'selection and masks logits to the classes present in the current mini-batch (the batch is the unit '
                   'of "what is present now").'},
    {'id': 'h4:6', 'bottleneck': 'h4-B1', 'role': 'd',
     'source': 'Michel et al. (2025)', 'version': 'arXiv:2502.18762v2 (7 Jun 2025)',
     'url': 'https://arxiv.org/abs/2502.18762v2',
     'quote': ['Typically, most offline methods take advantage of the task boundaries knowledge',
               'the task information is used solely to freeze certain prompts in the prompt pool',
               'if learned prompts are never frozen, prompt-based approach can easily be trained in task-free onCL.'],
     'raw_file': 'h4/txt/2502.18762v2.txt',
     'agent_note': 'Boundary use in the offline families is a consolidation (freeze) trigger; the online adaptation '
                   'removes the trigger rather than replacing it.'},
    {'id': 'h4:7', 'bottleneck': 'h4-B1', 'role': 'd',
     'source': 'Han, Zhang, Zhu & Guo, "Unifying Detection and Adaptation in Task-Free Continual Learning" (Findings of EMNLP 2026)',
     'version': 'arXiv:2608.27070v1 (27 Aug 2026)', 'url': 'https://arxiv.org/abs/2608.27070v1',
     'quote': ['these methods often rely on explicit task boundaries during training, limiting their applicability to '
               'realistic task-free scenarios.',
               'matching the Fisher principal subspace of each incoming batch window with historical subspaces.'],
     'raw_file': 'h4/txt/2608.27070v1.txt',
     'agent_note': 'Self-detected boundaries: a batch window is compared with stored Fisher subspaces (the window is a '
                   'fixed count of batches, i.e. clock-indexed). Its Table 1 compares with task-aware methods and reports '
                   'no multi-task target.'},
    {'id': 'h4:8', 'bottleneck': 'h4-B1', 'role': 'd',
     'source': 'Yan et al., FlyPrompt (ICLR 2026)', 'version': 'arXiv:2602.01976v3 (24 Mar 2026)',
     'url': 'https://arxiv.org/abs/2602.01976v3',
     'quote': ['they typically rely on multiple training epochs and explicit task cues',
               'w denotes the sample budget (window size) of each expert when methods adopt a self-triggered expert '
               'allocation mechanism.'],
     'raw_file': 'h4/txt/2602.01976v3.txt',
     'agent_note': 'Self-triggered expert allocation by a fixed sample budget per expert (a count of samples, not an '
                   'event in the learner).'},
    {'id': 'h4:9', 'bottleneck': 'h4-B1', 'role': 'd',
     'source': 'Kang, Wang, Zhang & Alahari, "Advancing Prompt-Based Methods for Replay-Independent General Continual '
               'Learning" (MISA, ICLR 2025)',
     'version': 'arXiv:2503.00677v1 (2 Mar 2025)', 'url': 'https://arxiv.org/abs/2503.00677v1',
     'quote': ['It includes a forgetting-aware initial session adaption that employs pretraining data to initialize prompt '
               'parameters and improve generalizability, as well as a non-parametric logit mask of the output layers to '
               'mitigate catastrophic forgetting.'],
     'raw_file': 'h4/txt/2503.00677v1.txt',
     'agent_note': 'Assumes access to pretraining data before the stream and a frozen pretrained backbone.'},

    # ---------------------------------------------------------------- h4-B2: hyperparameters without future data
    {'id': 'h4:10', 'bottleneck': 'h4-B2', 'role': 'a',
     'source': 'Lee, Hellan, Ericsson, Crowley & Storkey, "Hyperparameter Selection in Continual Learning" (preprint)',
     'version': 'arXiv:2404.06466v2 (14 Mar 2025)', 'url': 'https://arxiv.org/abs/2404.06466v2',
     'quote': ['The most common way to fit hyperparameters for CL is end-of-training hyperparameter optimisation (HPO)',
               'This is when the hyperparameters are fit by training over the whole data stream with each hyperparameter '
               'configuration and then selecting the configuration that has the best end-of-training performance'],
     'raw_file': 'h4/txt/2404.06466v2.txt',
     'agent_note': 'Problem: the standard protocol tunes on the whole stream, i.e. with future data.'},
    {'id': 'h4:11', 'bottleneck': 'h4-B2', 'role': 'b',
     'source': 'Lee et al. (2025)', 'version': 'arXiv:2404.06466v2 (14 Mar 2025)',
     'url': 'https://arxiv.org/abs/2404.06466v2',
     'quote': ['there is an open question: what HPO framework should a practitioner use for a CL problem in reality?'],
     'raw_file': 'h4/txt/2404.06466v2.txt',
     'agent_note': '2025 statement (v2).'},
    {'id': 'h4:12', 'bottleneck': 'h4-B2', 'role': 'b',
     'source': 'Michel et al. (2025)', 'version': 'arXiv:2502.18762v2 (7 Jun 2025)',
     'url': 'https://arxiv.org/abs/2502.18762v2',
     'quote': ['In general, LR selection remains a difficult topic in Continual Learning, as, in theory, future datasets are '
               'unknown and hyperparameter search is unavailable [10]. This problem is even more pronounced in the online '
               'setting, as not even a learning rate scheduler can be used, since the length and boundaries of tasks are '
               'considered unknown.'],
     'raw_file': 'h4/txt/2502.18762v2.txt',
     'agent_note': '2025 statement; ties the schedule to the unknown length of the stream.'},
    {'id': 'h4:13', 'bottleneck': 'h4-B2', 'role': 'b',
     'source': 'Cha & Cho, "Hyperparameters in Continual Learning: A Reality Check" (TMLR 2025)',
     'version': 'arXiv:2403.09066v5 (28 Oct 2025)', 'url': 'https://arxiv.org/abs/2403.09066v5',
     'quote': ['most state-of-the-art algorithms fail to replicate their reported performance, highlighting that their CL '
               'capacity has been significantly overestimated in the conventional evaluation protocol.'],
     'raw_file': 'h4/txt/2403.09066v5.txt',
     'agent_note': '2025 statement; the evidence is rankings in bar charts plus appendix tables, not a gap to an oracle.'},
    {'id': 'h4:14', 'bottleneck': 'h4-B2', 'role': 'c',
     'source': 'Lee et al. (2025)', 'version': 'arXiv:2404.06466v2 (14 Mar 2025)',
     'url': 'https://arxiv.org/abs/2404.06466v2',
     'quote': ['Table 3: Results of using different HPO frameworks for ER, iCaRL, ER-ACE, ESMER and DER++ on the standard '
               'split-task CORe50 and Tiny ImageNet benchmarks.',
               'DER++ End-of-training HPO 51.87±0.44 63.48±0.61 39.89±0.27 70.41±0.17',
               'Current-task HPO 51.58±0.77 64.19±046 36.64±0.33 66.43±0.49',
               'Default HPs 39.26±1.15 53.98±0.27 25.66±0.16 59.14±0.51',
               'ESMER End-of-training HPO 45.08±1.06 62.05±0.45 47.33±0.30 76.18±0.22 First-task HPO 47.07±1.18 '
               '63.69±0.95 46.69±0.56 75.72±0.24',
               'Table 2: Results of using different HPO frameworks for ER, iCaRL, ER-ACE, ESMER and DER++ on the standard '
               'split-task CIFAR-10 and CIFAR-100 benchmarks.',
               'ER-ACE End-of-training HPO 82.34±0.30 96.74±0.01 55.58±0.39 85.73±0.09 First-task HPO 83.20±0.79 '
               '96.67±0.18 56.36±0.29 86.11±0.154 Current-task HPO 83.99±0.22 96.58±0.15 56.46±0.36',
               'The table shows that all HPO frameworks perform similarly; none perform consistently better than the rest.'],
     'raw_file': 'h4/txt/2404.06466v2.txt',
     'agent_note': 'Columns: CORe50 Class-IL, Task-IL, Tiny ImageNet Class-IL, Task-IL. Oracle = end-of-training HPO '
                   '(sees the whole stream). DER++ Tiny ImageNet Class-IL: 39.89 oracle vs 36.64 best realistic '
                   '(current-task) = 3.25 points; vs 25.66 with default (untuned) HPs = 14.23 points. The authors read the '
                   'table as "perform similarly": for most methods and cells the realistic frameworks are within about '
                   'one point of, or above, the oracle (e.g. ER-ACE CIFAR-100 Class-IL 56.46 current-task vs 55.58 '
                   'end-of-training in Table 2). Best across methods on Tiny ImageNet Class-IL: ESMER end-of-training 47.33 vs '
                   'first-task 46.69 (0.64 points, inside the spreads).'},
    {'id': 'h4:15', 'bottleneck': 'h4-B2', 'role': 'c',
     'source': 'Michel et al. (2025)', 'version': 'arXiv:2502.18762v2 (7 Jun 2025)',
     'url': 'https://arxiv.org/abs/2502.18762v2',
     'quote': ['Best HP refer to the best set of LR and γ found on VTAB.',
               'CODA 15.14±3.78 71.12±4.47 56.03±2.1 0.83±0.35 53.17±1.96 35.9±6.33 1.92±0.62 47.65±1.4 32.93±1.85 '
               ',→+ ours 44.21±8.04 79.47±2.23 69.04±2.56 4.5±0.63 68.64±3.19 47.49±5.25 9.95±1.79 57.16±1.17 41.68±2.32'],
     'raw_file': 'h4/txt/2502.18762v2.txt',
     'agent_note': 'Si-Blurry (Table 1). Proxy-dataset tuning (VTAB) vs the better of two fixed LRs picked with hindsight '
                   'on the stream: CODA-P + ours CIFAR100 69.04 vs 79.47 (10.43 points), CUB 47.49 vs 68.64 (21.15). '
                   'But for the best method (ConvPrompt + ours, claim h4:3) the VTAB-tuned value equals the hindsight '
                   'value (86.34), so the best realistic result is at its oracle.'},
    {'id': 'h4:16', 'bottleneck': 'h4-B2', 'role': 'd',
     'source': 'Lee et al. (2025)', 'version': 'arXiv:2404.06466v2 (14 Mar 2025)',
     'url': 'https://arxiv.org/abs/2404.06466v2',
     'quote': ['First-task HPO is a static HPO framework',
               'Seen-tasks HPO (Mem) uses a sample of data from the current memory buffer.'],
     'raw_file': 'h4/txt/2404.06466v2.txt',
     'agent_note': 'Realistic families: tune on the first task and freeze (assumes the first task is representative); '
                   're-tune per task on a validation split (assumes task boundaries to re-tune at, and repeated training '
                   'per task); tune on memory or on past validation sets (assumes stored data).'},
    {'id': 'h4:17', 'bottleneck': 'h4-B2', 'role': 'd',
     'source': 'Seo, Koh & Choi, "Budgeted Online Continual Learning by Adaptive Layer Freezing and Frequency-based '
               'Sampling" (ICLR 2025 Spotlight)',
     'version': 'arXiv:2410.15143v2 (16 Mar 2025)', 'url': 'https://arxiv.org/abs/2410.15143v2',
     'quote': ['We found the hyperparameters through a search on CIFAR-10 and applied them to other datasets and setups '
               'without further tuning.',
               'a realistic scenario is performing a hyperparameter search using a known dataset and setup in a test '
               'environment, and applying it to real-world with unknown datasets and distributions.'],
     'raw_file': 'h4/txt/2410.15143v2.txt',
     'agent_note': 'Proxy-dataset tuning: assumes hyperparameters transfer across datasets and stream shapes.'},
    {'id': 'h4:18', 'bottleneck': 'h4-B2', 'role': 'd',
     'source': 'Cha & Cho (TMLR 2025)', 'version': 'arXiv:2403.09066v5 (28 Oct 2025)',
     'url': 'https://arxiv.org/abs/2403.09066v5',
     'quote': ['Hyperparameters of CL algorithms are tuned in the first phase and applied in the second phase to evaluate '
               'the algorithms.'],
     'raw_file': 'h4/txt/2403.09066v5.txt',
     'agent_note': 'GTEP: tune on a different dataset with the same scenario shape (assumes the number of tasks is known '
                   'and shared).'},

    # ---------------------------------------------------------------- h4-B3: compute-budgeted continual learning
    {'id': 'h4:19', 'bottleneck': 'h4-B3', 'role': 'a',
     'source': 'Prabhu et al., "Computationally Budgeted Continual Learning: What Does Matter?" (CVPR 2023)',
     'version': 'arXiv:2303.11165v2 (15 Jul 2023)', 'url': 'https://arxiv.org/abs/2303.11165v2',
     'quote': ['This is unreasonable for applications in-the-wild, where systems are primarily constrained by computational '
               'and time budgets, not storage.',
               'traditional CL approaches, with no exception, fail to outperform a simple minimal baseline that samples '
               'uniformly from memory.'],
     'raw_file': 'h4/txt/2303.11165v2.txt',
     'agent_note': 'Foundational (2023). Its ERM-Naive oracle numbers are in figure boxes and are not in the extracted text.'},
    {'id': 'h4:20', 'bottleneck': 'h4-B3', 'role': 'b',
     'source': 'Seo, Koh & Choi (ICLR 2025)', 'version': 'arXiv:2410.15143v2 (16 Mar 2025)',
     'url': 'https://arxiv.org/abs/2410.15143v2',
     'quote': ['several high-performing CL methods are not competitive under a fixed computational budget, falling behind a '
               'simple baseline of training on randomly retrieved batches from memory.'],
     'raw_file': 'h4/txt/2410.15143v2.txt',
     'agent_note': '2025 statement of the state (a diagnosis, not an explicit "open problem").'},
    {'id': 'h4:21', 'bottleneck': 'h4-B3', 'role': 'b',
     'source': 'Cho, Moon, Chunara, Cho & Cha, "Forget Forgetting: Continual Learning in a World of Abundant Memory" (ICLR 2026)',
     'version': 'arXiv:2502.07274v5 (18 Feb 2026)', 'url': 'https://arxiv.org/abs/2502.07274v5',
     'quote': ['arguing that in modern deployments, GPU cost is the true constraint.',
               'practical solutions to address this gap are still underexplored.'],
     'raw_file': 'h4/txt/2502.07274v5.txt',
     'agent_note': '2026 statement.'},
    {'id': 'h4:22', 'bottleneck': 'h4-B3', 'role': 'c',
     'source': 'Cho et al. (ICLR 2026)', 'version': 'arXiv:2502.07274v5 (18 Feb 2026)',
     'url': 'https://arxiv.org/abs/2502.07274v5',
     'quote': ['Table 6: Comparison of Full Retraining from scratch and Continual Learning under a standard CL setting. '
               'Average class-IL accuracy (%) on CIFAR-100 is reported.',
               'Full Retraining 46.15 64.73 69.96 76.02 78.94 Continual (Replay) 48.63 66.11 71.60 73.29 75.71 '
               'Ours 52.16 67.25 74.49 75.97 77.71',
               'Ours 52.16±1.2 66.89±0.9 74.49±0.8 77.71±0.8'],
     'raw_file': 'h4/txt/2502.07274v5.txt',
     'agent_note': 'Columns: memory 4%, 20%, 40%, 60%, 80% of past data. Target = full retraining from scratch on the '
                   'same memory (the expensive option). Best CL vs target: 80%: 77.71 vs 78.94 (1.23 points, standard '
                   'error 0.8 in Table 2); 60%: 75.97 vs 76.02 (0.05); at 4-40% CL is ahead. On this benchmark the gap to '
                   'the compute-heavy target is about one point or less.'},
    {'id': 'h4:23', 'bottleneck': 'h4-B3', 'role': 'c',
     'source': 'Prabhu et al. (CVPR 2023)', 'version': 'arXiv:2303.11165v2 (15 Jul 2023)',
     'url': 'https://arxiv.org/abs/2303.11165v2',
     'quote': ['The final gap between MSE distillation and Naive is 11.41% for C = 40, this gap is reduced to 3.85% for C = 400.'],
     'raw_file': 'h4/txt/2303.11165v2.txt',
     'agent_note': 'CGLM: the method is behind the naive baseline, more so at the lower budget. The target here is the '
                   'naive baseline, not an oracle.'},
    {'id': 'h4:24', 'bottleneck': 'h4-B3', 'role': 'd',
     'source': 'Prabhu et al. (CVPR 2023)', 'version': 'arXiv:2303.11165v2 (15 Jul 2023)',
     'url': 'https://arxiv.org/abs/2303.11165v2',
     'quote': ['per time step, CL methods are given a fixed computational budget',
               'we state C in terms of the number of training iterations'],
     'raw_file': 'h4/txt/2303.11165v2.txt',
     'agent_note': 'The benchmark itself fixes compute per time step (clock-indexed allocation, equal across steps).'},
    {'id': 'h4:25', 'bottleneck': 'h4-B3', 'role': 'd',
     'source': 'Seo, Koh & Choi (ICLR 2025)', 'version': 'arXiv:2410.15143v2 (16 Mar 2025)',
     'url': 'https://arxiv.org/abs/2410.15143v2',
     'quote': ['adaptive layer freezing that does not update the layers for less informative batches to reduce '
               'computational costs with a negligible loss of accuracy.',
               'chooses the best layers to freeze by maximizing the Fisher Information (FI) gained by the model for each '
               'batch, given a fixed computation budget.'],
     'raw_file': 'h4/txt/2410.15143v2.txt',
     'agent_note': 'Prior art to note: compute is already allocated by the Fisher information a batch carries.'},
    {'id': 'h4:26', 'bottleneck': 'h4-B3', 'role': 'd',
     'source': 'Cho et al. (ICLR 2026)', 'version': 'arXiv:2502.07274v5 (18 Feb 2026)',
     'url': 'https://arxiv.org/abs/2502.07274v5',
     'quote': ['it assumes access to a representative subset of past data, which may not always be feasible in '
               'privacy-sensitive or streaming-only environments.',
               'our analysis primarily focuses on class-incremental learning and continual instruction tuning with '
               'relatively clean task boundaries.'],
     'raw_file': 'h4/txt/2502.07274v5.txt',
     'agent_note': 'Weight-space consolidation assumes abundant memory and clean task boundaries.'},

    # ---------------------------------------------------------------- h4-B4: on-device, memory-constrained online CL
    {'id': 'h4:27', 'bottleneck': 'h4-B4', 'role': 'a',
     'source': 'Verwimp et al., "Continual Learning: Applications and the Road Forward" (TMLR 2024)',
     'version': 'arXiv:2311.11908v3 (28 Mar 2024)', 'url': 'https://arxiv.org/abs/2311.11908v3',
     'quote': ['On such small devices, both memory and computational resources are typically constrained, and the primary '
               'goal is to maximize model efficacy under these constraints.'],
     'raw_file': 'h4/txt/2311.11908v3.txt',
     'agent_note': 'Problem statement (2024, Dagstuhl position).'},
    {'id': 'h4:28', 'bottleneck': 'h4-B4', 'role': 'a',
     'source': 'Li, Dutt & Liu, "Orion: Enabling Self-adaptive Memory Management for On-device Online Continual Learning"',
     'version': 'arXiv:2605.26473v1 (26 May 2026)', 'url': 'https://arxiv.org/abs/2605.26473v1',
     'quote': ['However, its practical deployment is hindered by memory constraints in resource-limited systems, which '
               'affect key trade-offs in training latency, plasticity, and stability.'],
     'raw_file': 'h4/txt/2605.26473v1.txt',
     'agent_note': 'Problem statement (2026).'},
    {'id': 'h4:29', 'bottleneck': 'h4-B4', 'role': 'b',
     'source': 'Li, Dutt & Liu (Orion)', 'version': 'arXiv:2605.26473v1 (26 May 2026)',
     'url': 'https://arxiv.org/abs/2605.26473v1',
     'quote': ['Yet none of these efforts jointly address runtime memory constraints, algorithmic efficacy, and system-level '
               'co-design for on-device OCL. This gap is critical'],
     'raw_file': 'h4/txt/2605.26473v1.txt',
     'agent_note': '2026 statement.'},
    {'id': 'h4:30', 'bottleneck': 'h4-B4', 'role': 'c',
     'source': 'Li, Dutt & Liu (Orion)', 'version': 'arXiv:2605.26473v1 (26 May 2026)',
     'url': 'https://arxiv.org/abs/2605.26473v1',
     'quote': ['Oracle: We conduct an offline parameter search by brute force to ensure optimized plasticity and stability.',
               'Oracle shows a more significant advantage on medium and large benchmarks, achieving an average plasticity '
               'of 0.28 and stability of 0.33, compared to Orion’s 0.22 and 0.30'],
     'raw_file': 'h4/txt/2605.26473v1.txt',
     'agent_note': 'Benchmarks: SplitCIFAR10/100 and CORe50-NI/-NC/-NIC with ER (the paper calls CORe50-NIC "large"; '
                   'the medium/large grouping is otherwise the agent\'s reading). Target = offline brute-force search over '
                   '42 batch-size x buffer-size runs (uses the future). Gap: plasticity 0.06 (21% of the oracle), '
                   'stability 0.03 (9%). No spread is reported for these averages.'},
    {'id': 'h4:31', 'bottleneck': 'h4-B4', 'role': 'd',
     'source': 'Li, Dutt & Liu (Orion)', 'version': 'arXiv:2605.26473v1 (26 May 2026)',
     'url': 'https://arxiv.org/abs/2605.26473v1',
     'quote': ['because memory pressure and workload complexity shift dynamically as the number of OCL experiences grows, '
               'any static offline configuration could be either too conservative and waste resources early, or too '
               'aggressive and cause OOM failures later.',
               'While performance metrics such as stability and plasticity are only accessible after the completion of '
               'training for one experience rather than during training',
               'we introduce a time-dependent threshold, Thrt, that decreases over time'],
     'raw_file': 'h4/txt/2605.26473v1.txt',
     'agent_note': 'Assumptions: control decisions are taken at experience (task) boundaries, and the threshold decays '
                   'with a clock/experience index t, not with the learner\'s own change.'},

    # ---------------------------------------------------------------- h4-B5: resource-constrained federated / edge CL
    {'id': 'h4:32', 'bottleneck': 'h4-B5', 'role': 'a',
     'source': 'Li et al., "Resource-Constrained Federated Continual Learning: What Does Matter?"',
     'version': 'arXiv:2501.08737v2 (14 Oct 2025)', 'url': 'https://arxiv.org/abs/2501.08737v2',
     'quote': ['This is unreasonable for FCL applications in real-world scenarios, where edge devices are primarily '
               'constrained by resources such as storage, computational budget, and label rate.'],
     'raw_file': 'h4/txt/2501.08737v2.txt',
     'agent_note': 'Problem statement (federated CL on edge devices; the paper extends Prabhu et al. 2023).'},
    {'id': 'h4:33', 'bottleneck': 'h4-B5', 'role': 'b',
     'source': 'Li et al. (2025)', 'version': 'arXiv:2501.08737v2 (14 Oct 2025)',
     'url': 'https://arxiv.org/abs/2501.08737v2',
     'quote': ['we find that, under limited resource-constrained settings, existing FCL approaches, with no exception, fail '
               'to achieve the expected performance.'],
     'raw_file': 'h4/txt/2501.08737v2.txt',
     'agent_note': '2025 statement.'},
    {'id': 'h4:34', 'bottleneck': 'h4-B5', 'role': 'b',
     'source': 'Li et al., "Unleashing the Power of Continual Learning on Non-Centralized Devices: A Survey"',
     'version': 'arXiv:2412.13840v2 (6 May 2025)', 'url': 'https://arxiv.org/abs/2412.13840v2',
     'quote': ['Unfortunately, resource constraint issues remain under-investigated.'],
     'raw_file': 'h4/txt/2412.13840v2.txt',
     'agent_note': '2025 survey statement.'},
    {'id': 'h4:35', 'bottleneck': 'h4-B5', 'role': 'c',
     'source': 'Li et al. (2025)', 'version': 'arXiv:2501.08737v2 (14 Oct 2025)',
     'url': 'https://arxiv.org/abs/2501.08737v2',
     'quote': ['Table 2: Performance comparison of various methods in two incremental scenarios w.r.t. sufficient resources.',
               'FOT [2] 43.74±1.02 58.24±0.78 28.43±1.14 38.57±0.95',
               'Table 3: Performance comparison of various methods in two incremental scenarios w.r.t. extremely limited '
               'resources.',
               'FedWeIT [62] 9.37±1.05 20.52±0.67 5.95±0.95 12.32±0.87'],
     'raw_file': 'h4/txt/2501.08737v2.txt',
     'agent_note': 'Columns: CIFAR-10 A(f), mean A, CIFAR-100 A(f), mean A (then Tiny-ImageNet, Digit-10, Office-31, '
                   'Office-Caltech-10). CIFAR-100 final accuracy: best under extremely limited resources 5.95 (FedWeIT) '
                   'vs best with sufficient resources 28.43 (FOT; FOT itself drops to 4.85): gap 22.48 points. Table 3 '
                   'restricts memory, compute and label rate together, so the gap is not compute alone.'},
    {'id': 'h4:36', 'bottleneck': 'h4-B5', 'role': 'd',
     'source': 'Li et al. (2025)', 'version': 'arXiv:2501.08737v2 (14 Oct 2025)',
     'url': 'https://arxiv.org/abs/2501.08737v2',
     'quote': ['the computational budget amount as B that denotes the gradient step during the model update'],
     'raw_file': 'h4/txt/2501.08737v2.txt',
     'agent_note': 'Budget counted in gradient steps per update round (clock-indexed).'},

    # ---------------------------------------------------------------- h4-B6: real-time streams (not shown open)
    {'id': 'h4:37', 'bottleneck': 'h4-B6', 'role': 'a',
     'source': 'Ghunaim et al., "Real-Time Evaluation in Online Continual Learning: A New Hope" (CVPR 2023)',
     'version': 'arXiv:2302.01047v3 (24 Mar 2023)', 'url': 'https://arxiv.org/abs/2302.01047v3',
     'quote': ['a practical real-time evaluation of continual learning, in which the stream does not wait for the model to '
               'complete training before revealing the next data for predictions.',
               'a simple baseline outperforms state-of-the-art CL methods under this evaluation'],
     'raw_file': 'h4/txt/2302.01047v3.txt',
     'agent_note': 'Foundational (2023). No 2025-26 statement that this is open was found in the sweep, and the numbers '
                   'compare methods with a simple baseline, not with a target.'},
    {'id': 'h4:38', 'bottleneck': 'h4-B6', 'role': 'd',
     'source': 'Ghunaim et al. (CVPR 2023)', 'version': 'arXiv:2302.01047v3 (24 Mar 2023)',
     'url': 'https://arxiv.org/abs/2302.01047v3',
     'quote': ['OCL methods are not yet suited for practical deployment.'],
     'raw_file': 'h4/txt/2302.01047v3.txt',
     'agent_note': 'The delay model charges each method by its training complexity relative to the stream rate '
                   '(a wall-clock assumption).'},

    # ---------------------------------------------------------------- h4-B7: lifetime tuning in continual RL (not shown open)
    {'id': 'h4:39', 'bottleneck': 'h4-B7', 'role': 'a',
     'source': 'Mesbahi et al., "Position: Lifetime tuning is incompatible with continual reinforcement learning" (ICML 2025)',
     'version': 'arXiv:2404.02113v4 (8 Aug 2025)', 'url': 'https://arxiv.org/abs/2404.02113v4',
     'quote': ['The standard practice in RL is to assume unfettered access to the deployment environment for the full '
               'lifetime of the agent.'],
     'raw_file': 'h4/txt/2404.02113v4.txt',
     'agent_note': 'Problem statement (the RL form of h4-B2).'},
    {'id': 'h4:40', 'bottleneck': 'h4-B7', 'role': 'b',
     'source': 'Mesbahi et al. (ICML 2025)', 'version': 'arXiv:2404.02113v4 (8 Aug 2025)',
     'url': 'https://arxiv.org/abs/2404.02113v4',
     'quote': ['This is a position paper with a call to action: stop lifetime tuning your continual RL agents. We hope and '
               'expect future work to improve upon and replace k-percent tuning.'],
     'raw_file': 'h4/txt/2404.02113v4.txt',
     'agent_note': '2025 statement. Its results are plotted only (no numbers in the text), so there is no role-c claim.'},
]

BOTTLENECKS = [
    {'id': 'h4-B1', 'name': 'boundary-free streams (task-free / general CL)',
     'problem': 'Learning from a single-pass stream with no task labels or boundaries (blurry, overlapping classes) '
                'falls short of the same learner given clear boundaries.',
     'open': True,
     'benchmark': 'Si-Blurry ImageNet-R (ViT-B/16, ImageNet-21k), Michel et al. 2025 Tables 1-2',
     'best': '62.62±0.11 (ConvPrompt + ours, Si-Blurry, VTAB-tuned)',
     'target': '69.76±1.38 (same method, clear boundaries)',
     'gap_note': '7.14 points on ImageNet-R (1.85 on CUB, 1.31 on CIFAR100 within spread); FlyPrompt (ICLR 2026) reaches '
                 'Alast 55.27 on Si-Blurry ImageNet-R with no target reported. The clear-boundary target also removes '
                 'Si-Blurry\'s varying task sizes, so the gap is an upper bound on the cost of missing boundaries.',
     'assumptions': ['expert/prompt chosen by key-query similarity of the input',
                     'logits masked to classes present in the current mini-batch',
                     'boundaries used as consolidation (prompt-freeze) triggers; online versions drop the trigger',
                     'self-detected shifts over a fixed batch window or fixed per-expert sample budget (clock/count-indexed)',
                     'frozen pretrained backbone and access to pretraining data before the stream'],
     'cpu_testable': False,
     'cpu_note': 'The named benchmarks train prompts through a ViT-B/16 on 24k-60k images per run with 5-10 seeds: not '
                 'hours on a laptop CPU. A frozen-feature variant (precomputed embeddings, prototype or linear heads on a '
                 'Si-Blurry stream) would be, but it is not the reported benchmark.'},
    {'id': 'h4-B2', 'name': 'hyperparameters without future data',
     'problem': 'Standard CL tunes hyperparameters by replaying the whole stream; a deployed learner must choose them '
                'without future data.',
     'open': False,
     'benchmark': 'split-task Tiny ImageNet Class-IL (Lee et al. 2025 Table 3); Si-Blurry CIFAR100 (Michel et al. 2025)',
     'best': 'best realistic HPO per benchmark: ESMER 46.69±0.56 (first-task) on Tiny ImageNet Class-IL; ConvPrompt + '
             'ours 86.34±3.59 (VTAB-tuned) on Si-Blurry CIFAR100',
     'target': 'end-of-training (hindsight) HPO: 47.33±0.30; hindsight best of two LRs: 86.34±3.59',
     'gap_note': 'Not shown open as a performance gap: the best realistic pipeline is within about one point of, or equal '
                 'to, its hindsight oracle. Method-specific losses are large (DER++ Tiny ImageNet 3.25 points, untuned '
                 'defaults 14.23; CODA-P + ours on Si-Blurry CIFAR100 10.43), and rankings change under GTEP (Cha & Cho). '
                 'The open part is reliability, not the best attainable number.',
     'assumptions': ['tune on the first task and freeze (first task representative)',
                     're-tune per task (task boundaries and repeated training)',
                     'tune on memory or past validation data (stored data)',
                     'tune on a proxy dataset or scenario of the same shape (transfer; number of tasks known)',
                     'no learning-rate schedule online because stream length is unknown'],
     'cpu_testable': False,
     'cpu_note': 'Lee et al. grid (up to 90 configurations x 3 runs, ResNet-18) is GPU-scale; a small synthetic analogue '
                 'is CPU-feasible but is not the named benchmark.'},
    {'id': 'h4-B3', 'name': 'compute-budgeted continual learning',
     'problem': 'When compute per step, not storage, is the binding constraint, most CL methods fall behind naive replay, '
                'and the aim is to match full retraining at a fraction of its cost.',
     'open': False,
     'benchmark': 'CIFAR-100 class-IL with 80% memory (Cho et al., ICLR 2026, Table 6)',
     'best': '77.71 (Ours, weight space consolidation; ±0.8 in Table 2)',
     'target': '78.94 (full retraining from scratch)',
     'gap_note': 'Not shown open on the quoted numbers: 1.23 points at 80% memory, 0.05 at 60%, CL ahead at 4-40%, at '
                 'replay-level cost per the paper. The large-scale evidence (Prabhu et al. 2023, ImageNet2K/CGLM, '
                 'ERM-Naive oracle) is in figures only; the quoted text gives method vs naive (11.41 and 3.85 points), '
                 'not vs an oracle.',
     'assumptions': ['fixed compute per time step, equal across steps (clock-indexed allocation)',
                     'compute counted in training iterations or FLOPs per step',
                     'layers frozen for batches with low Fisher-information gain (information-indexed; prior art)',
                     'abundant memory and clean task boundaries (weight-space consolidation)'],
     'cpu_testable': False,
     'cpu_note': 'ImageNet2K/CGLM (1500 GPU-hours) and ResNet CIFAR-100 multi-epoch runs are not laptop-CPU hours.'},
    {'id': 'h4-B4', 'name': 'on-device memory-constrained online CL (configuration without hindsight)',
     'problem': 'On-device online CL must set batch size, buffer size and optimisation online under a memory cap; an '
                'online controller falls short of an offline brute-force search.',
     'open': True,
     'benchmark': 'CORe50-NI/-NC/-NIC ("medium and large") with ER on Jetson AGX Xavier / PC (Orion, 2026)',
     'best': "Orion’s 0.22 (plasticity) and 0.30 (stability)",
     'target': 'Oracle (offline brute-force, 42 runs) 0.28 plasticity and 0.33 stability',
     'gap_note': 'Plasticity 0.06 below the oracle (21% relative), stability 0.03 (9%); no spread reported. Single 2026 '
                 'preprint (v1), so the evidence is thin.',
     'assumptions': ['configuration chosen by offline search over the whole run (the oracle; uses the future)',
                     'decisions taken only at experience (task) boundaries',
                     'control threshold decays with a clock/experience index t (Thr_t = Thr_0 e^(-delta t))',
                     'memory pressure driven by count of experiences'],
     'cpu_testable': False,
     'cpu_note': 'The result is about GPU memory on embedded boards and a 42-run oracle; a CPU replication would not test '
                 'the same constraint. SplitCIFAR10 with Avalanche on CPU is feasible but that is where the gap is small.'},
    {'id': 'h4-B5', 'name': 'resource-constrained federated / edge CL',
     'problem': 'Federated CL on edge devices with limited memory, gradient steps and labels loses most of its accuracy.',
     'open': True,
     'benchmark': 'federated class-IL CIFAR-100, final accuracy A(f) (Li et al. 2025, Tables 2-3)',
     'best': '5.95±0.95 (FedWeIT, extremely limited resources)',
     'target': '28.43±1.14 (FOT, sufficient resources)',
     'gap_note': '22.48 points; the constrained setting restricts memory, compute and label rate together, so the gap is '
                 'not attributable to compute alone. The target is the same methods with sufficient resources, not a '
                 'joint model.',
     'assumptions': ['compute budget counted in gradient steps per round (clock-indexed)',
                     'cached exemplars or generated samples for replay',
                     'methods designed for sufficient resources and truncated'],
     'cpu_testable': False,
     'cpu_note': '1000+ GPU-hours in the source; a toy federated stream is CPU-feasible but not the benchmark.'},
    {'id': 'h4-B6', 'name': 'real-time streams (the stream does not wait)',
     'problem': 'A learner whose update takes longer than the stream interval skips data; expensive methods then lose to '
                'cheap ones.',
     'open': False,
     'benchmark': 'CLOC (Ghunaim et al. 2023)',
     'best': 'not quoted (method vs simple baseline only)',
     'target': 'none stated',
     'gap_note': 'Not shown open: no 2025-26 statement found in the sweep and no target number; the 2023 source compares '
                 'with a simple baseline.',
     'assumptions': ['delay charged by training complexity relative to stream rate (wall clock)'],
     'cpu_testable': False,
     'cpu_note': 'CLOC has 39 million images.'},
    {'id': 'h4-B7', 'name': 'lifetime tuning in continual RL',
     'problem': 'Continual RL agents are tuned by running every configuration for the whole deployment, which a deployed '
                'agent cannot do.',
     'open': False,
     'benchmark': 'continuing Catch / Cartpole / Jelly Bean World (Mesbahi et al., ICML 2025)',
     'best': 'plotted only',
     'target': 'plotted only',
     'gap_note': 'Not shown open by the definition: a 2025 call to action exists but the results are in figures only, so '
                 'no B-c numbers could be quoted.',
     'assumptions': ['hyperparameters selected over the full lifetime',
                     'k-percent tuning: selected on the first fraction of the lifetime'],
     'cpu_testable': True,
     'cpu_note': 'DQN on small continuing environments runs on a laptop CPU in hours; but without quoted numbers there is '
                 'no target to test against.'},
]
