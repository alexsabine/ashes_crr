"""OB1 stage 1 (Open_Bottlenecks/DECLARATION.md), family H2: continual learning of large models (continual pre-training
and fine-tuning of language models, forgetting under fine-tuning, knowledge editing at scale, continual instruction
tuning). Transcribed from the dossier docs/citations/ob1_h2_2026-09-30.md (sources fetched 2026-09-30 through the session
proxy; texts extracted from the current-version arXiv PDFs by pymupdf 1.28.2 and held outside the repository under
/tmp/claude-0/ob1_src/, named in `raw_file` relative to that root). verify.py checks every quote against its text.

Roles (the declaration's Stage 1): 'a' a quote stating the problem; 'b' a 2025-26 quote stating it is open, unsolved or a
main challenge; 'c' the best result the sources report on a named benchmark against a target (joint or multi-task
training, an oracle, per-task fine-tuning, the unedited model, or a stated goal), numbers quoted as extracted (table rows
cell by cell in reading order); 'd' the method families tried and the assumption each makes.
A bottleneck is open only if it has a, b and c claims (table.py computes this). Numbers that exist but have no target
stated in the source are NOT tagged 'c'; they are kept in the quote of an 'a' claim with the reason in agent_note.
Numbers from different papers are not comparable; every gap in `gap_note` is computed by the agent within one table.
"""

ROOT_NOTE = 'raw_file is relative to /tmp/claude-0/ob1_src'
T = 'h2/txt/'

S = {
    'revive': ('Zhang, Zhang, Ye et al., "Spectral Characterization and Mitigation of Sequential Knowledge Editing '
               'Collapse" (REVIVE; arXiv:2601.11042; ACL 2026 main)', 'v2, 9 May 2026', 'https://arxiv.org/abs/2601.11042',
               T + 'pdf_2601.11042v2.txt'),
    'nas': ('Liu, Zhu, Miao et al., "Norm Anchors Make Model Edits Last" (NAS; arXiv:2602.02543)', 'v3, 6 May 2026',
            'https://arxiv.org/abs/2602.02543', T + 'pdf_2602.02543v3.txt'),
    'wbe': ('Thede, Roth, Bethge, Akata, Hartvigsen, "WikiBigEdit: Understanding the Limits of Lifelong Knowledge Editing '
            'in LLMs" (arXiv:2503.05683; ICML 2025)', 'v2, 21 Sep 2025', 'https://arxiv.org/abs/2503.05683',
            T + 'pdf_2503.05683v2.txt'),
    'horen': ('Fang, Xie, Ran, "HoReN: Normalized Hopfield Retrieval for Large-Scale Sequential Model Editing" '
              '(arXiv:2605.08143)', 'v2, 19 May 2026', 'https://arxiv.org/abs/2605.08143', T + 'pdf_2605.08143v2.txt'),
    'loki': ('Eskandar, Sirera Perello, Ioannidis, Dy, "LOKI: Memory-Free Null-Space Constrained Lifelong Knowledge '
             'Editing" (arXiv:2606.19679)', 'v1, 18 Jun 2026', 'https://arxiv.org/abs/2606.19679', T + 'pdf_2606.19679v1.txt'),
    'stable': ('Ma, Chen, Liu et al., "More Edits, More Stable: Understanding the Lifelong Normalization in Sequential '
               'Model Editing" (StableEdit; arXiv:2605.11836; ICML 2026)', 'v2, 21 Jul 2026',
               'https://arxiv.org/abs/2605.11836', T + 'pdf_2605.11836v2.txt'),
    'drift': ('Liu, Cao, Li, "RAG or Learning? Understanding the Limits of LLM Adaptation under Continuous Knowledge Drift '
              'in the Real World" (arXiv:2604.05096)', 'v2, 14 Apr 2026', 'https://arxiv.org/abs/2604.05096',
              T + 'pdf_2604.05096v2.txt'),
    'smf': ('Lin, Zettlemoyer, Ghosh et al., "Continual Learning via Sparse Memory Finetuning" (arXiv:2510.15103)',
            'v1, 16 Oct 2025', 'https://arxiv.org/abs/2510.15103', T + 'pdf_2510.15103v1.txt'),
    'cfka': ('Wang, Shang, Sun et al., "Towards Understanding Continual Factual Knowledge Acquisition of Language Models: '
             'From Theory to Algorithm" (arXiv:2605.10640; ICML 2026)', 'v1, 11 May 2026',
             'https://arxiv.org/abs/2605.10640', T + 'pdf_2605.10640v1.txt'),
    'trace': ('Wang, Zhang, Chen et al., "TRACE: A Comprehensive Benchmark for Continual Learning in Large Language '
              'Models" (arXiv:2310.06762)', 'v1, 10 Oct 2023', 'https://arxiv.org/abs/2310.06762', T + 'pdf_2310.06762v1.txt'),
    'eoupct': ('Wang, Li, Cai et al., "Estimating and Orthogonalizing Unknown Pre-training Gradients for Continual '
               'Fine-tuning of Large Language Models" (EoupCT; arXiv:2609.30935; NeurIPS 2026)', 'v1, 25 Sep 2026',
               'https://arxiv.org/abs/2609.30935', T + 'pdf_2609.30935v1.txt'),
    'opr': ('Chen, Zhu, Zhang et al., "On-Policy Replay for Continual Supervised Fine-Tuning" (OPR; arXiv:2605.29495)',
            'v1, 28 May 2026', 'https://arxiv.org/abs/2605.29495', T + 'pdf_2605.29495v1.txt'),
    'muon': ('Lu, Deng, Zhang et al., "Muon-OGD: Muon-based Spectral Orthogonal Gradient Projection for LLM Continual '
             'Learning" (arXiv:2605.08949)', 'v2, 14 May 2026', 'https://arxiv.org/abs/2605.08949', T + 'pdf_2605.08949v2.txt'),
    'survey': ('Chen, Sun, Ye et al., "Beyond Static Models: An Evolving Framework for Continual Learning in Large Language '
               'Models across Training Stages" (survey; arXiv:2603.12658)', 'v2, 9 Aug 2026',
               'https://arxiv.org/abs/2603.12658', T + 'pdf_2603.12658v2.txt'),
    'tfgn': ('Ganguli, "TFGN: Task-Free, Replay-Free Continual Pre-Training Without Catastrophic Forgetting at LLM Scale" '
             '(arXiv:2605.15053; single author, independent researcher)', 'v2, 15 May 2026',
             'https://arxiv.org/abs/2605.15053', T + 'pdf_2605.15053v2.txt'),
    'mcit': ('Guo, Zhu, Zhao et al., "MCITlib: Multimodal Continual Instruction Tuning Library and Benchmark" '
             '(arXiv:2508.07307)', 'v3, 31 Dec 2025', 'https://arxiv.org/abs/2508.07307', T + 'pdf_2508.07307v3.txt'),
    'ctb': ('Guo, Hou, Sun et al., "MLLM-CTBench: A Benchmark for Continual Instruction Tuning with Reasoning Process '
            'Diagnosis" (arXiv:2508.08275)', 'v3, 13 Feb 2026', 'https://arxiv.org/abs/2508.08275', T + 'pdf_2508.08275v3.txt'),
    'flex': ('Yi, Xu, Zhang et al., "Beyond Routing Saturation: A Long-Horizon Class-Incremental Perspective on Expert '
             'Routing in Multimodal Continual Instruction Tuning" (FLEX; arXiv:2608.01437)', 'v1, 2 Aug 2026',
             'https://arxiv.org/abs/2608.01437', T + 'pdf_2608.01437v1.txt'),
    'acl': ('Wang, Wang, Zhang et al., "ACLArena: Agent Continue Learning in Multi-stage Post-training" '
            '(arXiv:2609.23989; under review)', 'v1, 21 Sep 2026', 'https://arxiv.org/abs/2609.23989',
            T + 'pdf_2609.23989v1.txt'),
    'cpt': ('Abbes, Subbaraj, Riemer et al., "Revisiting Replay and Gradient Alignment for Continual Pre-Training of Large '
            'Language Models" (arXiv:2508.01908)', 'v1, 3 Aug 2025', 'https://arxiv.org/abs/2508.01908',
            T + 'pdf_2508.01908v1.txt'),
    'sgap': ('Guo, Fu, Zhang et al., "Efficient Continual Pre-training by Mitigating the Stability Gap" (arXiv:2406.14833)',
             'v2, 27 Jun 2024', 'https://arxiv.org/abs/2406.14833', T + 'pdf_2406.14833v2.txt'),
    'mrcl': ('Luo, Wang, Zhou et al., "RL Forgets! Towards Continual Policy Optimization" (MRCL/CPO; arXiv:2607.04364)',
             'v3, 28 Sep 2026', 'https://arxiv.org/abs/2607.04364', T + 'pdf_2607.04364v3.txt'),
}


def _c(n, b, role, key, quote, note):
    src, ver, url, raw = S[key]
    return {'id': f'h2:{n}', 'bottleneck': b, 'role': role, 'source': src, 'version': ver, 'url': url,
            'quote': quote, 'raw_file': raw, 'agent_note': note}


CLAIMS = [
    # ------------------------------------------------------------------ h2-B1 sequential / lifelong knowledge editing
    _c(0, 'h2-B1', 'a', 'revive',
       ['Sequential knowledge editing in large language models often causes catastrophic collapse of the model’s '
        'general abilities, especially for parameter-modifying methods.'],
       'Problem statement (abstract as in the PDF).'),
    _c(1, 'h2-B1', 'b', 'revive',
       ['Despite the development of several sequential knowledge editing methods, including RECT (Gu et al., 2024), '
        'PRUNE (Ma et al., 2024), and ALPHAEDIT (Fang et al., 2024), long-horizon degradation remains largely unresolved.'],
       '2026 (v2 May 2026, ACL 2026): open statement.'),
    _c(2, 'h2-B1', 'b', 'nas',
       ['Under long-stream evaluations, many existing L&E editors exhaust their usable editing lifespan within only a few '
        'thousand sequential edits, making it a central bottleneck to extend the effective horizon of in-weight editing.'],
       '2026 (v3 May 2026): names the horizon as a central bottleneck.'),
    _c(3, 'h2-B1', 'b', 'wbe',
       ['Knowledge editing is reliant on local weight modification and collapses quickly. Even methods designed for '
        'lifelong editing converge to pre-update performance early. So large-scale lifelong editing requires significantly '
        'improving existing methods.'],
       '2025 (v2 Sep 2025, ICML 2025): on real Wikidata edits (WikiBigEdit, 500K+ QA pairs).'),
    _c(4, 'h2-B1', 'c', 'revive',
       ['Performance on sequential editing over 10,000 Samples.',
        'LLaMA3 7.02 9.44 89.73 635.47 24.24 35.67 34.81 31.83',
        'AlphaEdit 62.48 56.9 52.31 505.5 4.25 90.57 85.66 30.5 +REVIVE 98.74 ↑58.0% 90.08 ↑58.4% 60.19 '
        '↑15.1%',
        'NSE 77.59 44.42 86.12 607.86 23.31 45.61 45.04 31.27 +REVIVE 98.89 ↑27.4% 92.28 ↑107.8% 65.72 '
        '↓23.6%',
        'REVIVE enhanced methods maintains an overall average 86.34% of [...] its performance across all tasks after 10, '
        '000 edits.'],
       'Table 1, CounterFact/ZsRE, LLaMA3 (8B), 10,000 edits in 100 rounds of 100. Columns (CounterFact): Eff., Para., '
       'Neigh., Flu., Consis.; then ZsRE Eff., Para., Neigh. The first row ("LLaMA3") is the unedited model: its '
       'CounterFact Neighborhood Success is 89.73. Best edited rows with Eff. above 95: AlphaEdit+REVIVE Neigh. 60.19, '
       'NSE+REVIVE Neigh. 65.72 (which the paper notes is a decrease from NSE\'s 86.12). Gap (agent): best Neigh. at high '
       'efficacy 65.72 vs unedited 89.73 = 24.01 points; general ability (GLUE) retained 86.34% of the unedited model '
       '(target 100%), a 13.66% shortfall after 10,000 edits.'),
    _c(5, 'h2-B1', 'c', 'horen',
       ['Table 6: Sequential editing on WikiBigEdit (LLaMA-3.1-8B).',
        '3000 AlphaEdit 0.799 0.651 0.169 HoReN 0.986 0.754 0.631',
        'HoReN sustains OP ≥0.93 through 50K edits, while every baseline collapses or plateaus before 10K'],
       'Columns Rel., Gen., Loc. (1.0 = every edit recalled, every paraphrase answered, every unrelated query unchanged). '
       'On the synthetic ZsRE stream the parameter-preserving codebook editor holds OP >= 0.93 to 50K edits; on real '
       'WikiBigEdit edits at 3000 edits the best editor reaches Gen. 0.754 and Loc. 0.631 (gaps 0.246 and 0.369 to 1.0; '
       'the target 1.0 is the metrics\' definition, not a number the paper states).'),
    _c(6, 'h2-B1', 'd', 'loki',
       ['One unresolved challenge is that existing methods modify a fixed set of layers for all new knowledge samples, '
        'reducing flexibility and increasing catastrophic forgetting. Another is requiring access to previous knowledge '
        'and extensive pre-processing to obtain data statistics.'],
       'Locate-and-edit / null-space family: fixed edited layers; a stored covariance of preserved knowledge.'),
    _c(7, 'h2-B1', 'd', 'stable',
       ['normalizes value gradients using running statistics',
        'performing a small number of in-domain edits before the target sequence can precondition the running statistics'],
       'Lifelong-normalization family (UltraEdit, RLEdit, StableEdit): statistics are running means/variances over all '
       'processed edits, indexed by the cumulative sample count (edit-count clock), with a warm-up.'),
    _c(8, 'h2-B1', 'd', 'nas',
       ['rescaling each solved value vector to an original-model reference norm'],
       'Norm anchoring: the original model is held fixed as the reference.'),
    _c(9, 'h2-B1', 'd', 'horen',
       ['a frozen base model with one MLP layer wrapped by a discrete key–value memory, so each edit is stored once '
        'and never re-touched',
        'HoReN’s codebook grows linearly in the number of edits',
        'The current single-key argmax routing treats edits as mutually independent and uses a fixed per-model threshold c'],
       'Parameter-preserving codebook family (GRACE, WISE, HoReN): stores every edit; fixed hand-set match threshold; '
       'edits treated as independent.'),
    _c(10, 'h2-B1', 'd', 'revive',
       ['the dominant subspace in REVIVE is identified using a singular-value energy criterion',
        'applied in 100 rounds of 100 edits each'],
       'Spectral protection family: the original weights\' dominant subspace is held fixed; the protocol batches edits '
       'in fixed rounds.'),
    # ------------------------------------------------------------------ h2-B2 parametric knowledge updating under drift
    _c(11, 'h2-B2', 'a', 'drift',
       ['Large language models (LLMs) acquire most of their knowledge during pretraining, which ties them to a fixed '
        'snapshot of the world and makes adaptation to continuously evolving knowledge challenging.'],
       'Problem statement.'),
    _c(12, 'h2-B2', 'b', 'drift',
       ['These results suggest that parameter-level updates struggle to preserve previously acquired knowledge while '
        'incorporating new information.',
        'their effectiveness remains limited when adapting to continuous knowledge drift'],
       '2026 (v2 Apr 2026).'),
    _c(13, 'h2-B2', 'b', 'smf',
       ['Continual learning has been a longstanding challenge in AI, and persists in the era of large language models'],
       '2025 (Oct 2025).'),
    _c(14, 'h2-B2', 'c', 'drift',
       ['Method Historical Contemporary Commonsense Overall C1 C2 C3',
        'Direct Generation LLaMA-3.1 45.95 11.31 1.38 1.69 45.53 21.17',
        'LoRA FTLLaMA-3.1 35.14 71.15 4.13 10.17 40.27 32.17',
        'ChronosLLaMA-3.1 50.45+3.6 92.40+12.1 63.76+16.5 61.02+28.8 50.55+2.6 63.64+24.0'],
       'Table 2, exact-match accuracy on the paper\'s time-stamped real-world event benchmark (2024 onward), '
       'LLaMA-3.1-8B-Instruct. Cells in reading order: Historical, Contemporary C1, C2, C3, Commonsense, Overall (the '
       'Overall is the mean of the five). Best parametric method (LoRA FT) Overall 32.17 vs the same backbone with the '
       'time-aware retrieval baseline Chronos 63.64: gap 31.47; LoRA FT also drops Historical from 45.95 (unupdated) to '
       '35.14 (10.81 points forgotten). The target is a non-parametric reference on the same backbone, not an upper '
       'bound on parametric learning.'),
    _c(15, 'h2-B2', 'c', 'smf',
       ['When training on a stream of TriviaQA facts, performance on NaturalQuestions drops by 89% with full finetuning '
        'and 71% with LoRA, but only 11% with sparse memory finetuning with the same level of retention.'],
       'Held-out NaturalQuestions F1 relative drop after learning TriviaQA facts; target no drop (0%). Best 11% drop, on '
       'a memory-layer model (1.3B).'),
    _c(16, 'h2-B2', 'd', 'drift',
       ['because parametric methods typically update the model either one instance at a time or in a batch-wise manner, '
        'newly acquired knowledge can overwrite both the model’s original old knowledge and earlier updates'],
       'Parametric updating (ROME, MEMIT, WISE, LoRA FT): per-instance or per-batch updates.'),
    _c(17, 'h2-B2', 'd', 'drift',
       ['a time-aware retrieval baseline, Chronos, which progressively organizes retrieved evidence into an Event '
        'Evolution Graph',
        '(subject, relation, object, timestamp)'],
       'Retrieval family: stores all evidence; every fact carries an external calendar timestamp.'),
    _c(18, 'h2-B2', 'd', 'smf',
       ['the top t memory slots that are more frequently accessed on a certain batch relative to some background corpus '
        '(e.g. pretraining data)'],
       'Sparse memory finetuning: needs a memory-layer architecture and access statistics on a background corpus.'),
    _c(19, 'h2-B2', 'd', 'cfka',
       ['While classical CPT techniques like data replay have become the standard paradigm'],
       'Replay of old data as the standard.'),
    # ------------------------------------------------------------------ h2-B3 continual fine-tuning of LLMs (TRACE)
    _c(20, 'h2-B3', 'a', 'trace',
       ['Our experiments show that after training on TRACE, aligned LLMs exhibit significant declines in both general '
        'ability and instruction-following capabilities.'],
       'Problem statement (2023 benchmark paper).'),
    _c(21, 'h2-B3', 'b', 'eoupct',
       ['the primary challenge in continual LLM fine-tuning remains catastrophic forgetting, that is, training on new '
        'tasks leads to a sustained performance decline on previously learned tasks and a degradation of the '
        'pre-training LLM’s inherent general-purpose knowledge'],
       '2026 (NeurIPS 2026).'),
    _c(22, 'h2-B3', 'b', 'opr',
       ['Continual supervised fine-tuning (SFT) is the de facto recipe for adapting large language models (LLMs) to a '
        'stream of downstream tasks, but it suffers from catastrophic forgetting of earlier capabilities.'],
       '2026 (May 2026).'),
    _c(23, 'h2-B3', 'b', 'survey',
       ['forgetting at the LLM scale is not a scaled-up version of the classical problem but a qualitatively different one'],
       '2026 survey (v2 Aug 2026), Challenges section.'),
    _c(24, 'h2-B3', 'c', 'muon',
       ['Table 2: TRACE benchmark performance with the LLaMA-2-7B-Chat backbone model.',
        'Method LLaMA-2-7B-Chat AA (%) BT (%) SeqFT 23.0 -8.3 LoRASeqFT 9.2 -24.6 O-LoRA 41.3 -6.2 OSFT 48.4 -7.1 Ours '
        '49.4±0.3 -4.7±1.2 PerTaskFT 57.6 N/A MTL 52.3 N/A'],
       'TRACE (8 tasks), LLaMA-2-7B-Chat. Best continual method (Muon-OGD) AA 49.4 vs MTL 52.3 (gap 2.9) and vs '
       'per-task fine-tuning 57.6 (gap 8.2); BT -4.7 vs 0. The MTL and PerTaskFT numbers equal TRACE\'s own 2023 Table 3 '
       '("MT w/o. Re 52.3", "SingleFT 57.6"), i.e. they are carried over, not rerun.'),
    _c(25, 'h2-B3', 'c', 'opr',
       ['A 1% Vanilla Replay budget recovers most of the degradation (Wu et al., 2024) but leaves a 3–5 pp BWT gap.',
        'OPR-RU consistently improves over Vanilla Replay. It cuts |BWT| by 42–46% across the three backbones at '
        'ρ=0.01'],
       'TRACE with 7-8B instruction-tuned models: with 1% replay the BWT gap to zero forgetting is 3-5 pp; OPR cuts it by '
       '42-46% (to roughly 1.6-2.9 pp, agent\'s arithmetic). The MTL upper bound appears only in the paper\'s Figure 1 '
       'without a number in the text.'),
    _c(26, 'h2-B3', 'c', 'eoupct',
       ['+ EOUPCT 52.9 4.4 52.1 6.0 51.5 5.7 64.7 1.4 75.9 3.0 75.5 1.4 Qwen3-4B'],
       'Table 1, SuperNI 15-task sequences (ROUGE, Fgt. per order) and MMLU STEM/Humanity/Other (Acc., Fgt.), Qwen3-8B, '
       'best method: task forgetting 4.4-6.0 ROUGE and general-knowledge (MMLU) forgetting 1.4-3.0 points against a '
       'target of 0 forgetting. General-knowledge forgetting is small here; the task-stream forgetting is the larger gap.'),
    _c(27, 'h2-B3', 'd', 'eoupct',
       ['method involves storing the gradients of previously learned tasks and projecting the training gradients of the '
        'new task onto the orthogonal subspace spanned by these stored gradients',
        'orthogonal low-rank adaptation (OLoRA) [31] allocates a distinct set of LoRA parameters [7] to each new task',
        'as the training data and gradients of off-the-shelf pre-training LLMs are typically unknown, employing '
        'techniques such as gradient orthogonalization is rendered unrealistic'],
       'Orthogonal-gradient / per-task LoRA family: known task boundaries; stored per-task gradients or adapters; needs '
       'pre-training gradients it cannot have.'),
    _c(28, 'h2-B3', 'd', 'opr',
       ['rolls out the most recent checkpoint on a small budget of historical prompts',
        '[5, 3, 7, 5, 3, 5, 5, 7] (chosen to roughly equalize the number of gradient steps across tasks). The same '
        'hyperparameters are applied to every method and every backbone'],
       'Replay family: stores past prompts (budget rho); the protocol fixes per-task epoch counts in advance, so task '
       'boundaries and schedule are given.'),
    _c(29, 'h2-B3', 'd', 'tfgn',
       ['Every published continual-learning method either retains a buffer of prior data, requires task identifiers at '
        'training or inference time, applies a regularization penalty that scales poorly with model size, or operates at '
        'sentence-classification scale'],
       'A single-author 2026 preprint\'s summary of the assumptions of the whole field (its own solution claim is not '
       'relied on here).'),
    # ------------------------------------------------------------------ h2-B4 multimodal continual instruction tuning
    _c(30, 'h2-B4', 'a', 'mcit',
       ['the rise of Multimodal Large Language Models (MLLMs) brings new challenges in Multimodal Continual Learning (MCL), '
        'where models are expected to address both catastrophic forgetting and cross-modal coordination'],
       'Problem statement.'),
    _c(31, 'h2-B4', 'b', 'mcit',
       ['current multimodal continual instruction methods partially mitigate forgetting on downstream tasks but transfer '
        'poorly to general-purpose benchmarks, often degrading the model’s original capabilities. Bridging this gap is '
        'a central direction for future work on continual learning for MLLMs.'],
       '2025 (v3 31 Dec 2025).'),
    _c(32, 'h2-B4', 'b', 'survey',
       ['multimodal continual learning (MM-CL) remains underexplored'],
       '2026 survey, Opportunities section.'),
    _c(33, 'h2-B4', 'c', 'mcit',
       ['Method Venue ImgNet-R ArxivQA VizWiz IconQA CLEVR Flickr30k MFT (↑) MFN (↑) MAA (↑) BWT (↑)',
        'Individual - 91.67 90.83 57.87 78.43 76.63 61.72 76.19 - - -',
        'DISCO ICCV-25 87.43 93.07 46.96 68.13 65.70 56.69 75.87 69.66 81.60 -7.45',
        'serves as an empirical upper bound on performance, assuming no catastrophic forgetting.'],
       'Table 3(a), UCIT benchmark (6 tasks), LLaVA-1.5. Best continual method by final accuracy (DISCO) MFN 69.66 vs '
       'per-task fine-tuning ("Individual") 76.19: gap 6.53; vs its own MFT (stated empirical upper bound) 75.87: gap '
       '6.21; BWT -7.45.'),
    _c(34, 'h2-B4', 'd', 'ctb',
       ['(2) Replay-based methods revisit stored or synthesized samples to reduce forgetting [40, 25, 26, 27], at cost of '
        'memory or compute. (3) Architecture-based methods add task-conditioned components (e.g., progressive expansion '
        'or module routing) [41, 28, 29], alleviating interference but potentially increasing inference overhead. (4) '
        'Model-fusion-based strategies merge task-specific checkpoints post hoc'],
       'Method families for continual instruction tuning of MLLMs; task-conditioned components and task-specific '
       'checkpoints presuppose known task boundaries.'),
    _c(35, 'h2-B4', 'd', 'mcit',
       ['rank = 96, expert num = 6'],
       'MCITlib Table 1 training configuration on the 6-task UCIT benchmark: the number of experts equals the number of '
       'tasks, fixed in advance.'),
    # ------------------------------------------------------------------ h2-B5 long-horizon task identification / routing
    _c(36, 'h2-B5', 'a', 'flex',
       ['Many recent methods maintain task-specific LoRA experts and route each input to one or more experts at '
        'inference. Yet the task-identification problem underlying expert routing remains under-explored.'],
       'Problem statement.'),
    _c(37, 'h2-B5', 'b', 'flex',
       ['Therefore, the transferred CIL routers remove a substantial fraction of task-identification error, but the '
        'remaining gaps leave meaningful room for stronger routers.',
        'Textual fingerprints that leak task identity and short 4–10-task sequences with few competing experts jointly '
        'obscure the long-horizon routing problem.'],
       '2026 (Aug 2026).'),
    _c(38, 'h2-B5', 'c', 'flex',
       ['Method Base Best CIL Oracle Gap Recovered (%) DISCO 50.32 54.93 (+4.61) 60.01 5.08 47.6',
        'PureLoRA 54.60 56.14 (+1.54) 60.04 3.90 28.3',
        'Oracle is a routing reference rather than a guaranteed global upper bound'],
       'Table 3, FLEX (34-task long-horizon MCIT benchmark), MacroScore. Best absolute score PureLoRA+RanPAC 56.14 vs '
       'oracle (ground-truth one-hot) routing 60.04: gap 3.90; DISCO+DDAS 54.93 vs 60.01: gap 5.08.'),
    _c(39, 'h2-B5', 'd', 'flex',
       ['each task defines an incremental routing class',
        'We denote ground-truth one-hot routing as Oracle.'],
       'Expert-routing family: one expert per task, created at a supplied task boundary; routing is a task-identity '
       'classifier whose target is the ground-truth task label.'),
    _c(40, 'h2-B5', 'd', 'acl',
       ['MLE routes to the corresponding expert using the interaction environment available in the agent execution '
        'context, without requiring benchmark identities or ground-truth task labels.'],
       'Agent setting: the environment itself reveals which expert to use (the task identity is read off the context).'),
    # ------------------------------------------------------------------ h2-B6 multi-stage post-training consolidation
    _c(41, 'h2-B6', 'a', 'acl',
       ['Building general-purpose agents for industrial deployment requires integrating multiple capabilities, each '
        'typically acquired at a distinct stage of training.'],
       'Problem statement.'),
    _c(42, 'h2-B6', 'b', 'acl',
       ['Yet there is currently no well-established recipe for Agent Continual Learning (ACL), with little understanding '
        'of the trade-offs among existing integration paradigms.',
        'these results suggest that the problem cannot be solved simply by finding a better shared checkpoint'],
       '2026 (Sep 2026, under review).'),
    _c(43, 'h2-B6', 'b', 'survey',
       ['meaning gains at one stage can be silently erased by the next—a structural challenge with no adequate '
        'solution yet.'],
       '2026 survey: cross-stage (CPT -> CFT -> alignment) interactions.'),
    _c(44, 'h2-B6', 'c', 'acl',
       ['ExpertMath 25.83 22.0±0.2 2.3±0.5 43.3±0.6',
        'ExpertSearch 9.79 49.9±1.7',
        'ExpertE-commerce 6.25 19.3±0.1 33.2±1.1',
        'ExpertIF 0.00 26.4±1.1 4.6±0.2 86.2±0.0',
        'Seq-Final 10.21 33.5±1.7 29.6±1.6 84.8±0.1',
        '+MMOPD 21.25 45.2±0.4 27.7±1.5 84.6±0.5',
        'MLE (Ours) 21.04 49.7±0.2 32.9±2.2 85.0±0.3'],
       'Table 2, Qwen3-8B-Base, four stages; in-domain columns AIME26 (math), NQ (search), tau3-Retail (e-commerce), '
       'IF-Eval. Target: the independently trained per-task oracle experts (25.83, 49.9, 33.2, 86.2). Best single shared '
       'checkpoint (+MMOPD): 21.25, 45.2, 27.7, 84.6 (gaps 4.58, 4.7, 5.5, 1.6). The parameter-isolated MLE (a routed '
       'LoRA expert per stage) reaches 21.04, 49.7, 32.9, 85.0 (gaps 4.79, 0.2, 0.3, 1.2).'),
    _c(45, 'h2-B6', 'd', 'acl',
       ['MM uniformly averages the parameters.',
        'these residuals are parameter-isolated: learning a new stage introduces a new lightweight LoRA expert',
        'Our experiments mainly focus on Qwen3-8B-Base and a fixed four-stage curriculum.'],
       'Merging (fixed uniform weights), distillation from per-stage oracles, and one expert per stage: stages are '
       'supplied from outside and fixed in number.'),
    # ------------------------------------------------------------------ h2-B7 CPT forgetting with replay available
    _c(46, 'h2-B7', 'a', 'cpt',
       ['the introduction of new data often causes distribution shifts, leading to performance degradation on previously '
        'learned tasks'],
       'Problem statement (2025).'),
    _c(47, 'h2-B7', 'c', 'cpt',
       ['The joint training baseline average is only 72.6, while 25% replay with Reptile yields 76.8, and 50% replay with '
        'Reptile achieves the best overall result of 77.1.'],
       'Downstream average (HellaSwag, PiQA, PubMedQA), 6B Llama-family model, 3 language tasks of 100B tokens each: the '
       'continual method EXCEEDS the joint-training target (77.1 vs 72.6). No 2025-26 source found stating that CPT '
       'forgetting with replay available is open; not shown open.'),
    _c(48, 'h2-B7', 'd', 'cpt',
       ['Joint Training Baseline: Model trained on the joint A+B+C dataset in an i.i.d. setting together from scratch.',
        'Our study is largely limited to three tasks in a fixed sequence.'],
       'Replay of earlier-language data at a fixed ratio; three supplied phases.'),
    # ------------------------------------------------------------------ h2-B8 replay-free, task-free CPT at LLM scale
    _c(49, 'h2-B8', 'a', 'tfgn',
       ['Continually pre-training a large language model on a sequence of heterogeneous text domains, without replay and '
        'without task labels, has remained an unsolved architectural problem at LLM scale.'],
       'Problem statement.'),
    _c(50, 'h2-B8', 'b', 'tfgn',
       ['unsolved on a ∼9 B transformer under the replay-free, task-free regime that production deployment requires'],
       '2026, single-author preprint that also claims to solve the problem (BWT -0.007 at LLaMA 3.1 8B); it reports no '
       'joint-training or replay reference, so there is no B-c: not shown open.'),
    # ------------------------------------------------------------------ h2-B9 continual RL post-training
    _c(51, 'h2-B9', 'a', 'mrcl',
       ['Experiments on MRCL show that standard reinforcement learning still suffers from catastrophic forgetting during '
        'continual post-training.',
        'GSPO (Zheng et al., 2025) 65.03 30.70 45.17 83.00 44.80 74.26 53.74 63.94',
        'CPO (Ours) 90.83 76.84 63.64 77.50 49.00 73.24 71.56 72.81',
        'CPO achieves an average score of 64.14%, compared with 49.55% for GSPO and 59.50% for the pretrained model.'],
       'Numbers kept here, not as a B-c: MRCL (5 tasks, Qwen3-VL-4B) reports MFT/MFN/MTA with no stated target; the '
       'paper\'s own CPO has MFN 71.56 against its MFT 73.24 (1.68 apart) and exceeds the pretrained model on external '
       'benchmarks (64.14 vs 59.50). Not shown open by the declaration\'s test.'),
    _c(52, 'h2-B9', 'b', 'mrcl',
       ['catastrophic forgetting in multi-modal reasoning remains underexplored, and the role of policy regularization '
        'in continual RL is still not well understood.'],
       '2026 (v3 Sep 2026).'),
    # ------------------------------------------------------------------ h2-B10 stability gap in CPT
    _c(53, 'h2-B10', 'a', 'sgap',
       ['we observed a temporary performance drop at the beginning, followed by a recovery phase, a phenomenon known as '
        'the "stability gap,"'],
       'Problem statement (2024).'),
    _c(54, 'h2-B10', 'b', 'survey',
       ['A key open direction is understanding why the “stability gap” occurs'],
       '2026 survey. No 2025-26 number against a target was found in the sweep: not shown open.'),
]

BOTTLENECKS = [
    {'id': 'h2-B1', 'name': 'long-horizon sequential knowledge editing',
     'problem': 'Editing facts into an LLM one batch after another degrades edit efficacy, locality and general ability '
                'as edits accumulate, and on real-world edits generalization and locality stay well short of ideal.',
     'open': True, 'benchmark': 'CounterFact / ZsRE, 10,000 sequential edits (LLaMA3-8B); WikiBigEdit',
     'best': 'Neigh. 65.72 (NSE+REVIVE, Eff. 98.89); general ability 86.34% of the unedited model',
     'target': 'unedited LLaMA3 Neigh. 89.73; 100% of general ability',
     'gap_note': '24.01 points of neighbourhood (locality) and 13.66% of general ability lost after 10,000 edits; on '
                 'real WikiBigEdit edits the best editor has Gen. 0.754, Loc. 0.631 at 3,000 edits.',
     'assumptions': ['a fixed set of edited layers for every edit',
                     'stored statistics of preserved knowledge (covariance) computed in advance',
                     'running normalisation statistics indexed by cumulative edit count, with a warm-up',
                     'the original model held fixed as the reference (norm anchor, dominant subspace)',
                     'every edit stored; memory grows linearly; a fixed hand-set match threshold',
                     'edits treated as mutually independent; edits arrive in fixed-size rounds'],
     'cpu_testable': False,
     'cpu_note': 'The named benchmarks use 6-8B models (GPT-J, LLaMA3) and 10,000 sequential edits; ROME/MEMIT need '
                 'covariance statistics over Wikipedia. A GPT-2-small proxy on CPU is possible but is not the benchmark.'},
    {'id': 'h2-B2', 'name': 'parametric knowledge updating under real-world drift',
     'problem': 'Learning a stream of time-stamped real-world facts into the weights forgets older knowledge and falls '
                'far behind retrieval on the same backbone.',
     'open': True, 'benchmark': 'Liu et al. 2026 continuous-knowledge-drift benchmark (LLaMA-3.1-8B); TriviaQA->NQ',
     'best': 'LoRA FT Overall 32.17 (Historical 35.14); sparse memory finetuning NQ drop 11%',
     'target': 'Chronos (retrieval, same backbone) Overall 63.64; unupdated Historical 45.95; 0% NQ drop',
     'gap_note': '31.47 points behind the non-parametric reference; 10.81 points of historical knowledge forgotten; the '
                 'best sparse method still loses 11% on held-out NQ.',
     'assumptions': ['per-instance or per-batch weight updates', 'replay of old data as the standard',
                     'an external calendar timestamp on every fact (retrieval family)',
                     'a memory-layer architecture and access statistics on a background corpus'],
     'cpu_testable': False,
     'cpu_note': '8B backbone and a 1.3B memory-layer model; the benchmark data are public but the models are not '
                 'CPU-hours scale.'},
    {'id': 'h2-B3', 'name': 'continual fine-tuning of LLMs on task streams (TRACE)',
     'problem': 'Sequential SFT of an instruction-tuned LLM on a task stream forgets earlier tasks and general ability.',
     'open': True, 'benchmark': 'TRACE (8 tasks, LLaMA-2-7B-Chat); SuperNI 15 tasks + MMLU',
     'best': 'Muon-OGD AA 49.4, BT -4.7', 'target': 'MTL 52.3; PerTaskFT 57.6',
     'gap_note': '2.9 points below multi-task training and 8.2 below per-task fine-tuning; with 1% replay a 3-5 pp BWT '
                 'gap remains (OPR cuts it by 42-46%); MMLU general-knowledge forgetting of the best method is 1.4-3.0.',
     'assumptions': ['known task boundaries and a per-task epoch schedule fixed in advance',
                     'stored per-task gradients or a new LoRA adapter per task',
                     'a replay buffer of past prompts or gold data (budget rho)',
                     'access to pre-training data or gradients (unavailable; estimated by pseudo-data)',
                     'the same hyperparameters for every method, tuned once'],
     'cpu_testable': False, 'cpu_note': '7-8B models; TRACE is public but training runs need GPUs.'},
    {'id': 'h2-B4', 'name': 'multimodal continual instruction tuning',
     'problem': 'MLLMs tuned on a sequence of instruction tasks forget earlier tasks and lose general multimodal ability.',
     'open': True, 'benchmark': 'UCIT (6 tasks, LLaVA-1.5), MCITlib',
     'best': 'DISCO MFN 69.66, BWT -7.45', 'target': 'Individual (per-task fine-tuning) 76.19; MFT 75.87',
     'gap_note': '6.53 points below per-task fine-tuning; general-purpose benchmarks degrade.',
     'assumptions': ['task-conditioned components (experts, prompts) with the number of experts equal to the number of '
                     'tasks, fixed in advance', 'replay of stored or synthesized samples',
                     'post-hoc merging of task-specific checkpoints'],
     'cpu_testable': False, 'cpu_note': 'LLaVA-1.5 (7B) and InternVL backbones; GPU only.'},
    {'id': 'h2-B5', 'name': 'long-horizon task identification for expert routing',
     'problem': 'Methods with one expert per task must infer which expert to use at inference; with many similar tasks '
                'and no textual fingerprints the router falls short of oracle task identity.',
     'open': True, 'benchmark': 'FLEX (34 tasks, MacroScore)',
     'best': 'PureLoRA + RanPAC router 56.14', 'target': 'oracle routing 60.04',
     'gap_note': '3.90 MacroScore below oracle routing (DISCO+DDAS 5.08 below); the best routers recover 28-50% of the '
                 'base-to-oracle gap.',
     'assumptions': ['one expert per task, created at a supplied task boundary',
                     'routing as classification of a ground-truth task label',
                     'task identity readable from the input or the execution context'],
     'cpu_testable': False, 'cpu_note': 'MLLM experts; the routing sub-problem could be proxied on frozen features, '
                                         'but not the benchmark.'},
    {'id': 'h2-B6', 'name': 'multi-stage post-training consolidation (agent continual learning)',
     'problem': 'Capabilities acquired in successive post-training stages interfere; no shared checkpoint recovers all '
                'of them.',
     'open': True, 'benchmark': 'ACLArena (Qwen3-8B-Base, 4 stages: math, search, e-commerce, IF)',
     'best': 'shared checkpoint +MMOPD 21.25 / 45.2 / 27.7 / 84.6',
     'target': 'per-task oracle experts 25.83 / 49.9 / 33.2 / 86.2',
     'gap_note': 'shared model 4.6-5.5 points behind the oracles on three of four stages; a routed expert per stage '
                 'closes all but math (4.79).',
     'assumptions': ['stages supplied from outside, fixed in number and order',
                     'uniform-weight merging or distillation from per-stage oracles',
                     'one parameter-isolated expert per stage, selected by the environment'],
     'cpu_testable': False, 'cpu_note': '8B model with RL stages; GPU only.'},
    {'id': 'h2-B7', 'name': 'continual pre-training forgetting with replay available',
     'problem': 'New pre-training data shift the distribution and degrade earlier data.',
     'open': False, 'benchmark': 'Abbes et al. 2025 multilingual CPT (3 x 100B tokens; HellaSwag/PiQA/PubMedQA)',
     'best': '50% replay + Reptile 77.1', 'target': 'joint training 72.6',
     'gap_note': 'target exceeded by 4.5 points; no 2025-26 open statement found for this setting.',
     'assumptions': ['earlier data kept for replay at a fixed ratio', 'three supplied phases'],
     'cpu_testable': False, 'cpu_note': '100B tokens per phase, 99M-6B models.'},
    {'id': 'h2-B8', 'name': 'replay-free, task-free continual pre-training at LLM scale',
     'problem': 'Continual pre-training across domains without a replay buffer or task labels.',
     'open': False, 'benchmark': 'none with a target (TFGN reports BWT only)', 'best': 'BWT -0.007 (claimed)',
     'target': 'none stated', 'gap_note': 'no B-c: the only 2026 source is a single-author preprint that claims the '
                                           'problem solved, without a joint or replay reference.',
     'assumptions': ['a buffer of prior data', 'task identifiers at training or inference time',
                     'a regularization penalty'],
     'cpu_testable': False, 'cpu_note': '1B tokens per phase, 0.4-9B models.'},
    {'id': 'h2-B9', 'name': 'forgetting in continual RL post-training',
     'problem': 'Sequential RL post-training of VLMs forgets earlier tasks.',
     'open': False, 'benchmark': 'MRCL (5 tasks, Qwen3-VL-4B)', 'best': 'CPO MFN 71.56 (MFT 73.24)',
     'target': 'none stated in the source',
     'gap_note': 'no stated target; the paper\'s own method is 1.68 below its own MFT and above the pretrained model on '
                 'external benchmarks.',
     'assumptions': ['current-task KL regularization (GRPO family)', 'task sequence supplied'],
     'cpu_testable': False, 'cpu_note': '2-8B VLMs with RL; GPU only.'},
    {'id': 'h2-B10', 'name': 'stability gap in continual pre-training',
     'problem': 'Performance drops at the start of continual pre-training and recovers slowly.',
     'open': False, 'benchmark': 'none with a 2025-26 number against a target', 'best': '', 'target': '',
     'gap_note': 'a 2026 survey names it open; no 2025-26 benchmark number against a target was found.',
     'assumptions': ['a fixed compute budget and data mixture chosen in advance'],
     'cpu_testable': False, 'cpu_note': 'Llama-family CPT.'},
]
