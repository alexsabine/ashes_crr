# Energy literature, family "training" (fetched 2026-09-25)

Scope: mechanisms that reduce the compute or energy of training and model development (E1-E12 extracted; E14, E15 silent rows, recorded only). Every source was fetched in full text on 2026-09-25 and its text extracted with pypdf; the raw texts are in the agent scratchpad under `energy_lit/training/<id>.txt` and the rows in `energy_lit/training_rows.json` (81 rows). This file records what each source says; it grades nothing and quotes no number that is not in a quote below (R1, R8: a note, not evidence; nothing here is a ledger row).

**Quote check.** Every quote was checked as a verbatim substring of its raw text after html-unescape, removal of U+FFFE, U+00AD and "-\n" hyphenation joins, and whitespace collapsing: see the count at the end of this file. Table lines are quoted exactly as pypdf extracted them, including its artefacts (for example "76 .14" for 76.14, "1023" for 10^23, "/tildelow" for ~, and missing spaces such as "a1.32×speed-up").

**Fetch notes.** All arXiv PDFs (45) returned HTTP 200 from arxiv.org/pdf/<id>. Versions and dates were read from export.arxiv.org/abs/<id>; for seven ids (2202.09774, 2404.16795, 2508.01908, 1910.08475, 2305.02869, 2306.03241, 2405.20541) export.arxiv.org returned HTTP 406, and the version history was read from arxiv.org/abs/<id> instead. No github.com link was needed. Extraction limits: the shrink-and-perturb grids of Ash & Adams (Figures 15-21) are heatmaps whose numbers pypdf does not extract; Everett et al. and u-muP report most sweep comparisons in figures only; in Lee et al. Table 6 the column headers are garbled by extraction, so the energy row uses the Appendix D sentence instead of the table.

## Sources

### Tensor Programs V: Tuning Large Neural Networks via Zero-Shot Hyperparameter Transfer

- Authors: Yang, Greg; Hu, Edward J.; Babuschkin, Igor; Sidor, Szymon et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2203.03466v2, Mon, 28 Mar 2022 08:12:14 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2203.03466 ; https://arxiv.org/pdf/2203.03466
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2203.03466.txt`
- Rows: E1

Quotes:

> Task Metric 6.7B+ µP 6.7B re-run 6.7B [7] 13B [7] Validation loss cross-entropy 1.98 2.03

> The total tuning cost was only 7% of total pretraining cost.

> BERT large Megatron Default 1x 1x 1.731 86.3/86.2 90.9 BERT large Naive Transfer 22x 220x training diverged BERT large µTransfer (Ours) 22x 220x 1.683 87.0/86.5 91.4

> The total tuning cost = the cost of pretraining a single BERT-large.

### u-$\mu$P: The Unit-Scaled Maximal Update Parametrization

- Authors: Blake, Charlie; Eichenberg, Constantin; Dean, Josef; Balles, Lukas et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2407.17465v3, Fri, 10 Jan 2025 14:22:02 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2407.17465 ; https://arxiv.org/pdf/2407.17465
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2407.17465.txt`
- Rows: E1, E12

Quotes:

> Table 4: 0-shot benchmark results at 7B scale. Scheme Format MMLU HellaSwag OpenBook QA PIQA TriviaQA WinoGr SP BF16 29.6 52.4 27.8 76.5 22.2 63.3 u-µP BF16 29.0 53.4 31.6 77.1 23.4 63.7

> SP BF16 29.6 52.4 27.8 76.5 22.2 63.3 u-µP BF16 29.0 53.4 31.6 77.1 23.4 63.7

> u-µP BF16 29.0 53.4 31.6 77.1 23.4 63.7 u-µP FP8 31.2 53.4 29.6 77.6 21.3 65.7

### Scaling Exponents Across Parameterizations and Optimizers

- Authors: Everett, Katie; Xiao, Lechao; Wortsman, Mitchell; Alemi, Alexander A. et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2407.05872v2, Tue, 16 Jul 2024 17:40:09 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2407.05872 ; https://arxiv.org/pdf/2407.05872
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2407.05872.txt`
- Rows: E1

Quotes:

> Our results show that all parameterizations, not just maximal update parameterization (muP), can achieve hyperparameter transfer; moreover, our novel per-layer learning rate prescription for standard parameterization outperforms muP.

### Completed Hyperparameter Transfer across Modules, Width, Depth, Batch and Duration

- Authors: Mlodozeniec, Bruno; Ablin, Pierre; Béthune, Louis; Busbridge, Dan et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2512.22382v1, Fri, 26 Dec 2025 20:56:04 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2512.22382 ; https://arxiv.org/pdf/2512.22382
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2512.22382.txt`
- Rows: E1

Quotes:

> which at large scale result in a1.32×speed-up and improved benchmark performance (see Figure 9).

> The hyperparameter search at small scale in Figure 1 took 6730 GPU-hours on NVIDIA A100s, although 99% of the loss gains over the optimal global hyperparameters were realised within the first 3168 GPU-hours.

> 1.32× speedup 7.2B training run

### Multi-Task Learning Using Uncertainty to Weigh Losses for Scene Geometry and Semantics

- Authors: Kendall, Alex; Gal, Yarin; Cipolla, Roberto
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 1705.07115v3, Tue, 24 Apr 2018 06:42:35 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1705.07115 ; https://arxiv.org/pdf/1705.07115
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/1705.07115.txt`
- Rows: E2a

Quotes:

> Approx. optimal weights 0.89 0.01 0.1 62.8% 3.61 0.549

> 3 task uncertainty weighting ✓ ✓ ✓ 63.4% 3.50 0.522

> Tuning these weights by hand is a difﬁcult and expensive process, making multi-task learning prohibitive in practice.

> Unweighted sum of losses 0.333 0.333 0.333 50.1% 3.79 0.592

### GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks

- Authors: Chen, Zhao; Badrinarayanan, Vijay; Lee, Chen-Yu; Rabinovich, Andrew et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 1711.02257v4, Tue, 12 Jun 2018 06:45:49 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1711.02257 ; https://arxiv.org/pdf/1711.02257
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/1711.02257.txt`
- Rows: E2a, E2b

Quotes:

> Even after 100 networks trained, grid search still falls short of our GradNorm network.

> GradNorm has therefore found the optimal grid search weights in one single training run.

> Equal Weights 0.697 7.80 0.172 (Kendall et al., 2017) 0.702 7.96 0.182 GradNorm Static 0.695 7.63 0.156 GradNormα = 1.5 0.663 7.32 0.155

### AutoScale: Linear Scalarization Guided by Multi-Task Optimization Metrics

- Authors: Yang, Yi; Ikemura, Kei; Zhang, Qingwen; Zhu, Xiaomeng et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2508.13979v1, Tue, 19 Aug 2025 16:14:00 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2508.13979 ; https://arxiv.org/pdf/2508.13979
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2508.13979.txt`
- Rows: E2a, E2b

Quotes:

> Searched weights⋆ 0.695 0.725 0.706 3.0 0.00 -0.44 0.453×n 66.27 10.36 0.320 3.67 0.69 -1.42 0.195×n

> Low Cond. 0.697 0.727 0.703 2.0 0.00 -0.37 0.535 66.07 10.62 0.32 6.00 0.82 -0.03 0.244

> The searched weights are from 20 trials, but only one trial’s time is plotted; actual time is 20 times longer.

> Searched weights⋆ 0.695 0.725 0.706 3.0 0.00 -0.44 0.453×n

> Low Cond. 0.697 0.727 0.703 2.0 0.00 -0.37 0.535

> UM [18] 0.681 0.716 0.698 8.0 0.95 0.95 0.455 57.96 9.99 0.361 8.00 11.20 5.69 0.199

> Unitary 0.699 0.729 0.680 6.0 2.98 1.14 0.453 54.16 9.96 0.392 9.00 18.74 10.62 0.195

> Gradnorm [5] 0.677 0.714 0.700 7.0 1.07 1.07 1.130 52.53 10.06 0.395 11.00 20.49 12.11 0.572

### In Defense of the Unitary Scalarization for Deep Multi-Task Learning

- Authors: Kurin, Vitaly; De Palma, Alessandro; Kostrikov, Ilya; Whiteson, Shimon et al.
- Venue: NeurIPS 2022 (per PDF footer)
- Version: arXiv 2201.04122v4, Wed, 8 Mar 2023 22:29:41 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2201.04122 ; https://arxiv.org/pdf/2201.04122
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2201.04122.txt`
- Rows: E2b

Quotes:

> Unit. Scal. 9.090e-01 ± 7.568e-04 [2.869e+02, 2.878e+02]

> PCGrad 9.093e-01 ± 1.108e-03 [1.015e+04, 1.016e+04]

> IMTL 9.093e-01 ± 7.631e-04 [3.600e+02, 3.621e+02]

> MGDA 9.022e-01 ± 9.687e-04 [6.859e+02, 7.194e+02]

### Do Current Multi-Task Optimization Methods in Deep Learning Even Help?

- Authors: Derrick Xin; Behrooz Ghorbani; Ankush Garg; Orhan Firat; Justin Gilmer
- Venue: NeurIPS 2022 (Advances in Neural Information Processing Systems 35), main conference track
- Version: No arXiv version; publisher version as served on the day by proceedings.neurips.cc
- Fetched: https://proceedings.neurips.cc/paper_files/paper/2022/hash/580c4ec4738ff61d5862a122cdf139b6-Abstract-Conference.html ; https://proceedings.neurips.cc/paper_files/paper/2022/file/580c4ec4738ff61d5862a122cdf139b6-Paper-Conference.pdf
- Status: HTTP 200 (abstract page and PDF, 4,098,705 bytes)
- Raw text: `energy_lit/training/xin2022.txt`
- Rows: E2b

Quotes:

> We show that, despite the added design and computational complexity of these algorithms, MTO methods do not yield any performance improvements beyond what is achievable via traditional optimization approaches.

> led to a significant reduction in the number of training steps per second (from≈ 12 to≈ 5).

### Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization

- Authors: Li, Lisha; Jamieson, Kevin; DeSalvo, Giulia; Rostamizadeh, Afshin et al.
- Venue: Journal of Machine Learning Research 18 (per PDF header)
- Version: arXiv 1603.06560v4, Mon, 18 Jun 2018 23:01:43 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1603.06560 ; https://arxiv.org/pdf/1603.06560
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/1603.06560.txt`
- Rows: E3, E4

Quotes:

> On these data sets, Hyperband is over 20× faster than random search while SMAC (early) is ≤ 7× faster than random search within the evaluation window.

> In addition, Hyperband is 5× to 30× faster than popular Bayesian optimization algorithms on a variety of deep-learning and kernel-based learning problems.

> magnitude faster than standard conﬁguration selection approaches and 5 × faster than SMAC (early). For SVHN, while Hyperband ﬁnds a good conﬁguration faster, Bayesian optimization methods are competitive and SMAC (early) outperforms Hyperband.

> Hyperband is over 20× faster than random search while SMAC (early) is ≤ 7× faster than random search within the evaluation window.

### BOHB: Robust and Efficient Hyperparameter Optimization at Scale

- Authors: Falkner, Stefan; Klein, Aaron; Hutter, Frank
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 1807.01774v1, Wed, 4 Jul 2018 20:59:35 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1807.01774 ; https://arxiv.org/pdf/1807.01774
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/1807.01774.txt`
- Rows: E3, E4

Quotes:

> We note that HB initially performed much better than the vanilla BO methods and achieved a roughly three-fold speedup over RS. However, for large enough budgets TPE and GP-BO caught up in all cases, and in the end found better conﬁgurations than HB and RS.

> All model-based methods substantially outperformed RS at the end of their budget, whereas HB approached the same performance.

> HB and BOHB started out identically, but BOHB achieved the same ﬁnal performance as HB 100 times faster

> Finally, HB-LCNet performed somewhat better than HB alone, but consistently worse than BOHB, even when tuning HBLCNet.

### A System for Massively Parallel Hyperparameter Tuning

- Authors: Li, Liam; Jamieson, Kevin; Rostamizadeh, Afshin; Gonina, Ekaterina et al.
- Venue: MLSys 2020 (arXiv v5 of the MLSys paper; venue string in the PDF)
- Version: arXiv 1810.05934v5, Mon, 16 Mar 2020 01:28:21 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1810.05934 ; https://arxiv.org/pdf/1810.05934
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/1810.05934.txt`
- Rows: E3

Quotes:

> Additionally, ASHA and asynchronous Hyperband are both about 3× faster than Vizier at ﬁnding a conﬁguration with test perplexity below 80, despite being much simpler and easier to implement. Furthermore, the best model found by ASHA achieved a test perplexity of 76.6, which is signiﬁcantly better than 78.4 reported for the large LSTM in Zaremba et al. (2014).

### Speeding Up Automatic Hyperparameter Optimization of Deep Neural Networks by Extrapolation of Learning Curves

- Authors: Tobias Domhan; Jost Tobias Springenberg; Frank Hutter
- Venue: IJCAI 2015 (Proceedings of the 24th International Joint Conference on Artificial Intelligence)
- Version: No arXiv version; IJCAI proceedings PDF as served on the day
- Fetched: https://www.ijcai.org/Proceedings/15/Papers/487.pdf
- Status: HTTP 200 (PDF, 2,765,547 bytes)
- Raw text: `energy_lit/training/domhan2015.txt`
- Rows: E4

Quotes:

> our predictive termination criterion sped up both SMAC and TPE by at least a factor of two for reaching the same validation error as without it. Overall, the average time needed per hyperparamter optimization run was reduced from 40 to 18 hours.

### Efficient Bayesian Learning Curve Extrapolation using Prior-Data Fitted Networks

- Authors: Adriaensen, Steven; Rakotoarison, Herilalaina; Müller, Samuel; Hutter, Frank et al.
- Venue: NeurIPS 2023 (per PDF footer)
- Version: arXiv 2310.20447v1, Tue, 31 Oct 2023 13:30:30 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2310.20447 ; https://arxiv.org/pdf/2310.20447
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2310.20447.txt`
- Rows: E4

Quotes:

> this LC-PFN variant obtains an expected regret lower than that obtained by no-stop, approximately 3.3× faster on LCBench and Taskset. Looking at individual tasks, we note 2 - 6× speed-ups on all 3 PD1 tasks, all 12 Taskset tasks, and 30 of the 35LCBench tasks (we obtain 1 - 2× speed-ups on the remaining 5).

> On NAS-Bench-201, we find that all termination criteria considered, including 9 standard Patience heuristics, fail on all 3 tasks

### In-Context Freeze-Thaw Bayesian Optimization for Hyperparameter Optimization

- Authors: Rakotoarison, Herilalaina; Adriaensen, Steven; Mallik, Neeratyoy; Garibov, Samir et al.
- Venue: ICML 2024 (per PDF footer)
- Version: arXiv 2404.16795v3, Mon, 12 Aug 2024 12:24:45 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2404.16795 ; https://arxiv.org/pdf/2404.16795
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/2404.16795.txt`
- Rows: E4

Quotes:

> The results validate the superiority of freeze-thaw approaches (ifBO, DyHPO, and DPL) compared to standard approaches (Hyperband, ASHA, and random search) for low-budget settings.

### Supervising the Multi-Fidelity Race of Hyperparameter Configurations

- Authors: Wistuba, Martin; Kadra, Arlind; Grabocka, Josif
- Venue: NeurIPS 2022 (per PDF footer)
- Version: arXiv 2202.09774v2, Thu, 1 Jun 2023 08:55:35 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2202.09774 ; https://arxiv.org/pdf/2202.09774
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/2202.09774.txt`
- Rows: E4

Quotes:

> We present the results of our second experiment in Figure 5 (left), where, as it can be seen, DYHPO still outperforms the other methods when its overhead is considered.

### Simple and Scalable Strategies to Continually Pre-train Large Language Models

- Authors: Ibrahim, Adam; Thérien, Benjamin; Gupta, Kshitij; Richter, Mats L. et al.
- Venue: TMLR (06/2024) (per PDF header)
- Version: arXiv 2403.08763v4, Wed, 4 Sep 2024 16:13:18 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2403.08763 ; https://arxiv.org/pdf/2403.08763
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2403.08763.txt`
- Rows: E5

Quotes:

> 300B Pile → 300B SP (5% Replay) 1.79 2 .00 1.89 600B Pile ∪ SP 1.72 2 .02 1.87

> The standard error for these measurements was computed but is not reported as it was< 0.001 for all models.

> 300B Pile → 300B SP (5% Replay) 2.23 2 .51 2.37 600B Pile ∪ SP 2.17 2 .53 2.35

> 300B Pile→ 300B SP (5% Replay) 73.24 39 .42 74 .24 70 .80 26 .83 28 .79 30 .60 78 .02 68 .67 23 .01 35 .02 13 .32 57 .86 47.68 600B Pile∪ SP 73.39 39 .25 73 .57 72 .05 26 .83 37 .78 27 .80 77 .58 67 .32 23 .13 36 .16 12 .41 56 .73 48.00

> 300B Pile→ 300B SP (5% Replay) 46.55 23 .55 55 .01 57 .92 24 .22 25 .94 20 .60 69 .37 54 .22 23 .38 38 .35 1 .99 15 .70 35.14 600B Pile∪ SP 45.06 23 .55 52 .99 55 .57 23 .12 26 .65 18 .20 69 .37 52 .72 23 .50 38 .81 1 .72 14 .63 34.30

### Continual Pre-Training of Large Language Models: How to (re)warm your model?

- Authors: Gupta, Kshitij; Thérien, Benjamin; Ibrahim, Adam; Richter, Mats L. et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2308.04014v2, Wed, 6 Sep 2023 23:13:07 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2308.04014 ; https://arxiv.org/pdf/2308.04014
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2308.04014.txt`
- Rows: E5

Quotes:

> Our results show that while rewarming models first increases the loss on upstream and downstream data, in the longer run it improves the downstream performance, outperforming models trained from scratch—even for a large downstream dataset.

### TiC-LM: A Web-Scale Benchmark for Time-Continual LLM Pretraining

- Authors: Li, Jeffrey; Armandpour, Mohammadreza; Mirzadeh, Iman; Mehta, Sachin et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2504.02107v3, Fri, 6 Jun 2025 06:49:43 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2504.02107 ; https://arxiv.org/pdf/2504.02107
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2504.02107.txt`
- Rows: E5

Quotes:

> Replay (α = 1/2) + AR 440B 3B -0.002 0.016 0.154

> Oracle Series 1.16T 3B -0.003 0.037 0.163

> can achieve comparable heldout loss to re-training from scratch, while requiring significantly less computation (2.6×).

### Revisiting Replay and Gradient Alignment for Continual Pre-Training of Large Language Models

- Authors: Abbes, Istabrak; Subbaraj, Gopeshh; Riemer, Matthew; Islah, Nizar et al.
- Venue: CoLLAs 2025 (per PDF header)
- Version: arXiv 2508.01908v1, Sun, 3 Aug 2025 20:07:15 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2508.01908 ; https://arxiv.org/pdf/2508.01908
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/2508.01908.txt`
- Rows: E5

Quotes:

> Our scaling analysis across model sizes and replay rates indicates that small rates of replaying old examples are definitely a more valuable use of compute than investing in model size, but that it is more compute efficient to scale the size of the model than invest in high rates of replaying old examples.

### On Warm-Starting Neural Network Training

- Authors: Ash, Jordan T.; Adams, Ryan P.
- Venue: NeurIPS 2020 (per PDF footer)
- Version: arXiv 1910.08475v3, Thu, 31 Dec 2020 07:58:30 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1910.08475 ; https://arxiv.org/pdf/1910.08475
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/1910.08475.txt`
- Rows: E6a, E6b

Quotes:

> CIFAR-10 SGD A DAM SGD A DAM SGD A DAM RANDOM INIT 56.2 (1.0) 78.0 (0.6) 39.0 (0.2) 39.4 (0.1) 40.5 (0.6) 33.8 (0.6) WARM START 51.7 (0.9) 74.4 (0.9)

> Means and standard deviations across ﬁve runs are shown.

> Better-generalizing warm-started models take even more time to train than their randomly-initialized peers, which on average achieve 55.2% accuracy in 34.0 minutes.

> Accuracy 54.4 (0.9) 53.5 (1.0) 52.9 (1.0) 49.9 (1.6) 50.8 (1.8) Train Time 165.3 (3.9) 38.0 (1.33) 16.5 (1.3) 14.6 (91.0) 13.6 (0.4)

> The proposed trick with λ = 0.6 performs identically to randomly initializing in terms of validation accuracy, but trains much more quickly.

> As expected, we see that warm-started models train faster but generalize worse. However, if we instead initialize parameters using the shrink and perturb trick, we are able to both close this generalization gap and signiﬁcantly speed up training.

### DASH: Warm-Starting Neural Network Training in Stationary Settings without Loss of Plasticity

- Authors: Shin, Baekrok; Oh, Junsoo; Cho, Hanseul; Yun, Chulhee et al.
- Venue: NeurIPS 2024 (per PDF footer)
- Version: arXiv 2410.23495v2, Fri, 1 Nov 2024 09:49:24 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2410.23495 ; https://arxiv.org/pdf/2410.23495
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2410.23495.txt`
- Rows: E6a, E6b

Quotes:

> CIFAR-10 Random Init 67.32 (0.51) 75.68 (0.39) 5161 (156) 17125 (292) 57.66 (0.11) 66.27 (0.13) 2916 (37) 8121 (26) Warm Init 63.53 (0.56) 70.99 (0.59) 1173 (0) 3910 (247)

> Standard deviations are provided in parentheses.

> Warm Init 63.53 (0.56) 70.99 (0.59) 1173 (0) 3910 (247) 54.87 (0.18) 63.27 (0.55) 665 (11) 2153 (23) S&P 81.25 (0.14) 85.53 (0.22) 5395 (625)

> CIFAR-10 Random Init 67.32 (0.51) 75.68 (0.39) 5161 (156)

> DASH 84.08 (0.52) 86.75 (0.53) 6490 (399)

> Random Init 25.69 (0.13) 31.30 (0.09) 30237 (368) 40142 (368) 17.37 (0.06) 21.95 (0.11) 17503 (53) 22513 (74) Warm Init 9.57 (0.24) 13.94 (0.37) 3388 (368) 5474 (0) 6.70 (0.04) 9.88 (0.21) 1785 (5) 2773 (7) S&P 34.34 (0.48) 37.39 (0.18) 13815 (368)

### bert2BERT: Towards Reusable Pretrained Language Models

- Authors: Chen, Cheng; Yin, Yichun; Shang, Lifeng; Jiang, Xin et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2110.07143v1, Thu, 14 Oct 2021 04:05:25 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2110.07143 ; https://arxiv.org/pdf/2110.07143
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2110.07143.txt`
- Rows: E7

Quotes:

> BERTBASE† (Ours) 7.3 0% 89.6(0.1) 92.7(0.2) 84.6(0.2) 88.6(0.5) 57.3(4.0) 90.6(0.7) 90.6(0.1) 89.9(0.3) 85.5(0.5)

> bert2BER T 4.0 45 .2% 90.0(0.2) 92.9(0.1) 85.1(0.1) 87.7(0.7) 60.0(1.2) 90.5(0.8) 90.4(0.1) 89.2(0.2) 85.7(0.4)

> We report mean (and standard deviation) performance over 3 runs on the dev set.

> GPT 4.9 133.8 47.0 53.5 bert2BERT 2.6 (47%↓) 132.1 47.9 53.0

### Learning to Grow Pretrained Models for Efficient Transformer Training

- Authors: Wang, Peihao; Panda, Rameswar; Hennigen, Lucas Torroba; Greengard, Philip et al.
- Venue: ICLR 2023 (per PDF header)
- Version: arXiv 2303.00980v1, Thu, 2 Mar 2023 05:21:18 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2303.00980 ; https://arxiv.org/pdf/2303.00980
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2303.00980.txt`
- Rows: E7

Quotes:

> For instance, LiGO saves 44.7% and 22.5% FLOPs for training BERT-Base and GPT2-Medium from scratch by reusing pretrained smaller models that are half as big. Similarly, for vision transformers, when using DeiT-S (Touvron et al., 2021a) for initialization, LiGO yields 55% savings in FLOPs with no performance drop on ImageNet

### Stacking Your Transformers: A Closer Look at Model Growth for Efficient LLM Pre-Training

- Authors: Du, Wenyu; Luo, Tongxu; Qiu, Zihan; Huang, Zeyu et al.
- Venue: NeurIPS 2024 (per PDF footer)
- Version: arXiv 2405.15319v2, Tue, 22 Oct 2024 10:31:59 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2405.15319 ; https://arxiv.org/pdf/2405.15319
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2405.15319.txt`
- Rows: E7

Quotes:

> For example, compared to a conventionally trained 7B model using 300B tokens, ourGstack model converges to the same loss with 194B tokens, resulting in a 54.6% speedup.

### Masked Structural Growth for 2x Faster Language Model Pre-training

- Authors: Yao, Yiqun; Zhang, Zheng; Li, Jing; Wang, Yequan et al.
- Venue: ICLR 2024 (per PDF header)
- Version: arXiv 2305.02869v3, Sat, 6 Apr 2024 06:18:26 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2305.02869 ; https://arxiv.org/pdf/2305.02869
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/2305.02869.txt`
- Rows: E7

Quotes:

> Wall time 70h, 48min 32h, 10min 29h, 20min Operator - Bert2BERT MSG No Mask MSG No Mask Glue Avg. 82.2(0.2) 82.1(0.3) 83.2(0.2) 82.2(0.2) 79.1(0.4) 77.9(0.3)

> The numbers are mean (standard deviation) computed across 3 runs.

> Wall time 53h, 1min 37h, 59min

> PPL-zs 41.31 42.24 41.20

### Early Weight Averaging meets High Learning Rates for LLM Pre-training

- Authors: Sanyal, Sunny; Neerkaje, Atula; Kaddour, Jean; Kumar, Abhishek et al.
- Venue: WANT@NeurIPS 2023 workshop (per PDF footer)
- Version: arXiv 2306.03241v2, Mon, 11 Dec 2023 22:31:12 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2306.03241 ; https://arxiv.org/pdf/2306.03241
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/2306.03241.txt`
- Rows: E8

Quotes:

> nanoGPT-2(125M) 50 K 33.77 27.65 44.65 44.07 74.10 71.60 52.08 48.26 51.15 47.89

> nanoGPT-2(335M) 50 K 35.88 30.95 44.74 44.28 75.8 72.9 50.76 50.49 49.72 51.72

### Stop Wasting My Time! Saving Days of ImageNet and BERT Training with Latest Weight Averaging

- Authors: Kaddour, Jean
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2209.14981v2, Thu, 6 Oct 2022 17:57:36 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2209.14981 ; https://arxiv.org/pdf/2209.14981
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2209.14981.txt`
- Rows: E8

Quotes:

> corresponding to time savings up to /tildelow68 and /tildelow30 GPU hours when training a ResNet50 on ImageNet and RoBERTa-Base model on WikiText-103, respectively.

### Exponential Moving Average of Weights in Deep Learning: Dynamics and Benefits

- Authors: Morales-Brotons, Daniel; Vogels, Thijs; Hendrikx, Hadrien
- Venue: TMLR (04/2024) (per PDF header)
- Version: arXiv 2411.18704v1, Wed, 27 Nov 2024 19:14:27 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2411.18704 ; https://arxiv.org/pdf/2411.18704
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2411.18704.txt`
- Rows: E8

Quotes:

> Val Acc. 75.83 ± 0.05 76 .14 ± 0.21 75 .95 ± 0.29 76 .75 ± 0.31 76 .31 ± 0.28

> epochs [200, 197, 199] [143 , 139, 156] [133 , 112, 129]

> Other than the mean and standard deviation of the results over 3 independent runs

### When, Where and Why to Average Weights?

- Authors: Ajroldi, Niccolò; Orvieto, Antonio; Geiping, Jonas
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2502.06761v3, Mon, 24 Nov 2025 10:35:14 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2502.06761 ; https://arxiv.org/pdf/2502.06761
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2502.06761.txt`
- Rows: E8

Quotes:

> NadamW +LAW A +EMA GPU-Hours 612 550 541

> estimate a 12% reduction in GPU-hours to train the entire AlgoPerf suite up to the validation target compared to our baseline.

> This result suggests that averaging schemes which do not use the average to compute optimization updates cannot fully replace a learning rate annealing

### Scaling Laws and Compute-Optimal Training Beyond Fixed Training Durations

- Authors: Hägele, Alexander; Bakouch, Elie; Kosson, Atli; Allal, Loubna Ben et al.
- Venue: NeurIPS 2024 (per PDF footer)
- Version: arXiv 2405.18392v3, Thu, 17 Oct 2024 12:01:15 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2405.18392 ; https://arxiv.org/pdf/2405.18392
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2405.18392.txt`
- Rows: E9

Quotes:

> Metric Cosine to 0 1-Sqrt 5% Linear 5% Linear 10% Linear 20% Aggregated Score 48.03 47.91 47.84 47.98 47.92

> FLOPs Chinchilla 5.59× 1023 w/ Cooldown 2.36× 1023

> The reliable behavior of both the cooldown schedule and SW A allows scaling experiments with a drastic reduce in both compute and GPU hours

### MiniCPM: Unveiling the Potential of Small Language Models with Scalable Training Strategies

- Authors: Hu, Shengding; Tu, Yuge; Han, Xu; He, Chaoqun et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2404.06395v3, Mon, 3 Jun 2024 08:54:38 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2404.06395 ; https://arxiv.org/pdf/2404.06395
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2404.06395.txt`
- Rows: E9

Quotes:

> in the decay stage, as the learning rate begins to decrease, the loss experiences a significant rapid decline and quickly decreases to be equal to or lower than the Cosine LRS at step T = S. At the same time, we can reuse the model before decay and continue training with the previous high learning rate.

### The Road Less Scheduled

- Authors: Defazio, Aaron; Yang, Xingyu Alice; Mehta, Harsh; Mishchenko, Konstantin et al.
- Venue: NeurIPS 2024 (per PDF footer)
- Version: arXiv 2405.15682v4, Tue, 29 Oct 2024 22:40:23 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2405.15682 ; https://arxiv.org/pdf/2405.15682
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2405.15682.txt`
- Rows: E9

Quotes:

> ILSVRC 2012 ImageNet (ResNet-50) Schedule-Free (76.90% SE 0.03) Cosine Schedule (76.90% SE 0.06)

> OpenWebText (GPT-2 124M) Cosine Schedule (2.853 SE 0.004) Schedule-Free (2.831 SE 0.008)

### Straight to Zero: Why Linearly Decaying the Learning Rate to Zero Works Best for LLMs

- Authors: Bergsma, Shane; Dey, Nolan; Gosal, Gurpreet; Gray, Gavia et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2502.15938v2, Sun, 23 Nov 2025 19:25:46 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2502.15938 ; https://arxiv.org/pdf/2502.15938
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2502.15938.txt`
- Rows: E9

Quotes:

> a 610M-parameter model trained for 80 tokens-per-parameter (TPP) using D2Z achieveslowerloss than when trained for 200 TPP using 10×decay, corresponding to an astonishing 60% compute savings.

> Comparison to continuous (610M, 80 TPP): D2Z surpassesCyclicand WSDschedules.

### Deduplicating Training Data Makes Language Models Better

- Authors: Lee, Katherine; Ippolito, Daphne; Nystrom, Andrew; Zhang, Chiyuan et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2107.06499v2, Thu, 24 Mar 2022 19:29:45 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2107.06499 ; https://arxiv.org/pdf/2107.06499
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2107.06499.txt`
- Rows: E10

Quotes:

> We estimate training 2 epochs of XL-ORIGINAL and XLEXACT SUBSTR uses 5.86MWh . XL-NEAR DUP is trained for fewer steps and we estimate uses 5.63MWh .

> models trained on deduplicated datasets have no worse perplexity compared to baseline models trained on the original datasets. In some cases deduplication reduces perplexity by up to 10%.

> XL-ORIGINAL 1.926% 1.571% XL-NEAR DUP 0.189% 0.264%

### SemDeDup: Data-efficient learning at web-scale through semantic deduplication

- Authors: Abbas, Amro; Tirumala, Kushal; Simig, Dániel; Ganguli, Surya et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2303.09540v3, Wed, 22 Mar 2023 17:22:35 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2303.09540 ; https://arxiv.org/pdf/2303.09540
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2303.09540.txt`
- Rows: E10

Quotes:

> Down to using only 50% of LAION-440M for pre-training CLIP, we are able to match the zero-shot ImageNet accuracy of the baseline model trained on 100% of the data (black dashed line) with a small drop of 0.47% only, while we outperform the baseline model with only 63% of data.

> Average performance improves across 24 tasks down to 63% of the pre-training data, yielding better performance with almost 1.6× faster pre-training.

> For example, training on the 80% pruned dataset reaches baseline model perplexity on prompts_with_answer in 95.0% of the baseline training, saving 5.0% compute.

### D4: Improving LLM Pretraining via Document De-Duplication and Diversification

- Authors: Tirumala, Kushal; Simig, Daniel; Aghajanyan, Armen; Morcos, Ari S. et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2308.12284v1, Wed, 23 Aug 2023 17:58:14 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2308.12284 ; https://arxiv.org/pdf/2308.12284
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2308.12284.txt`
- Rows: E10

Quotes:

> D4 significantly outperforms baseline training, getting between 18-20% efficiency gains on validation perplexity and 2% increase in average 0-shot downstream accuracy across 16 NLP tasks.

### Perplexed by Perplexity: Perplexity-Based Data Pruning With Small Reference Models

- Authors: Ankner, Zachary; Blakeney, Cody; Sreenivasan, Kartik; Marion, Max et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2405.20541v1, Thu, 30 May 2024 23:50:20 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2405.20541 ; https://arxiv.org/pdf/2405.20541
- Status: HTTP 200 (PDF); version page via arxiv.org/abs (export.arxiv.org returned 406)
- Raw text: `energy_lit/training/2405.20541.txt`
- Rows: E11

Quotes:

> 3B Parameters Trained on Pile No Pruning (Baseline) 21.82 13.09 39.08 4.88 14.28 18.63 High Perplexity Selected 25.8 16.24 43.32 2.91 15.07 20.67

> achieves up to a 1.45× reduction in pretraining steps to reach commensurate baseline performance.

> 3B Parameters Trained on Dolma No Pruning (Baseline) 23.56 14.29 39.57 4.4 14.2 19.2 Medium Perplexity Selected 24.19 16.48 41.8 3.3 13.19 19.79

### When Less is More: Investigating Data Pruning for Pretraining LLMs at Scale

- Authors: Marion, Max; Üstün, Ahmet; Pozzobon, Luiza; Wang, Alex et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2309.04564v1, Fri, 8 Sep 2023 19:34:05 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2309.04564 ; https://arxiv.org/pdf/2309.04564
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2309.04564.txt`
- Rows: E11

Quotes:

> Compared with the no-pruning baseline, pruning to themiddle 50% of the perplexity distribution leads to a 0.97% improvement in perplexity. Using only themiddle 30% of the data achieves nearly the same performance, with a 0.80% improvement over the no-pruning baseline.

> Compared with random selection, pruning usingPerplexity results in significantly higher model performance than random pruning across all data ratios (Figure 4). Formemorizationand EL2N pruning metrics, both achieve similar performances to random pruning despite being far more computationally expensive.

> 30% 77.29 0.007 66.040.017

> 30% 77.34 0.005 64.840.023

> No Pruning 100% 78.15 0.002

### Beyond neural scaling laws: beating power law scaling via data pruning

- Authors: Sorscher, Ben; Geirhos, Robert; Shekhar, Shashank; Ganguli, Surya et al.
- Venue: NeurIPS 2022 (per PDF footer)
- Version: arXiv 2206.14486v6, Fri, 21 Apr 2023 20:14:07 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2206.14486 ; https://arxiv.org/pdf/2206.14486
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2206.14486.txt`
- Rows: E11

Quotes:

> only a 8 few still match performance obtained by training on the full dataset, when selecting a signiﬁcantly smaller training subset (i.e. about 80% of ImageNet). Nonetheless, most metrics continue to beat random pruning, with memorization in particular demonstrating strong performance (Fig. 5C).

### Mixed Precision Training

- Authors: Micikevicius, Paulius; Narang, Sharan; Alben, Jonah; Diamos, Gregory et al.
- Venue: ICLR 2018 (per PDF header)
- Version: arXiv 1710.03740v3, Thu, 15 Feb 2018 20:04:02 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/1710.03740 ; https://arxiv.org/pdf/1710.03740
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/1710.03740.txt`
- Rows: E12

Quotes:

> Resnet50 75.92% 76.04%

> This nearly halves memory requirements and, on recent GPUs, speeds up arithmetic.

### FP8 Formats for Deep Learning

- Authors: Micikevicius, Paulius; Stosic, Dusan; Burgess, Neil; Cornea, Marius et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2209.05433v2, Thu, 29 Sep 2022 20:47:07 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2209.05433 ; https://arxiv.org/pdf/2209.05433
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2209.05433.txt`
- Rows: E12

Quotes:

> GPT 22B 7.21 7 .24 GPT 175B 6.65 6 .68

> Thus, unless otherwise speciﬁed, we clip to FP8-representable values the activation, weight, and activation gradient tensors that are inputs to GEMMs.

### DeepSeek-V3 Technical Report

- Authors: DeepSeek-AI; Liu, Aixin; Feng, Bei; Xue, Bing et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2412.19437v2, Tue, 18 Feb 2025 17:26:38 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2412.19437 ; https://arxiv.org/pdf/2412.19437
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2412.19437.txt`
- Rows: E12

Quotes:

> Notably, compared with the BF16 baseline, the relative loss error of our FP8-training model remains consistently below 0.25%, a level well within the acceptable range of training randomness.

> This design theoretically doubles the computational speed compared with the original BF16 method.

> DeepSeek-V3 requires only 2.788M H800 GPU hours for its full training.

### Pretraining Large Language Models with NVFP4

- Authors: NVIDIA; Abecassis, Felix; Agrusa, Anjulie; Ahn, Dong et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2509.25149v2, Wed, 4 Mar 2026 23:43:57 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2509.25149 ; https://arxiv.org/pdf/2509.25149
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2509.25149.txt`
- Rows: E12

Quotes:

> For instance, the model attains an MMLU-pro accuracy of 62.58%, nearly matching the 62.62% accuracy achieved through FP8 pretraining.

> Tensor Cores deliver FP4 computations at 2× (on GB200 chips) and 3× (on GB300 chips) higher math throughput rates compared to FP8.

> the relative loss error of NVFP4 remains consistently below1%, and widens to slightly above1.5%as the learning rate is decayed towards the end of training.

> We observe that MXFP4 matches NVFP4 loss when trained on36%more tokens (i.e., using 1.36T instead of 1T tokens).

### Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity

- Authors: Fedus, William; Zoph, Barret; Shazeer, Noam
- Venue: Journal of Machine Learning Research 23 (per PDF header)
- Version: arXiv 2101.03961v3, Thu, 16 Jun 2022 20:36:07 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2101.03961 ; https://arxiv.org/pdf/2101.03961
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2101.03961.txt`
- Rows: E14

Quotes:

> We design models based oﬀ T5-Base and T5-Large (Raﬀel et al., 2019) to obtain up to 7x increases in pre-training speed with the same computational resources.

### DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models

- Authors: Dai, Damai; Deng, Chengqi; Zhao, Chenggang; Xu, R. X. et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2401.06066v1, Thu, 11 Jan 2024 17:31:42 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2401.06066 ; https://arxiv.org/pdf/2401.06066
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2401.06066.txt`
- Rows: E14

Quotes:

> Evaluation results reveal that with only about 40% of computations, DeepSeekMoE 16B achieves comparable performance with DeepSeek 7B (DeepSeek-AI, 2024), a dense model trained on the same 2T corpus.

### Training Compute-Optimal Large Language Models

- Authors: Hoffmann, Jordan; Borgeaud, Sebastian; Mensch, Arthur; Buchatskaya, Elena et al.
- Venue: venue not stated in the fetched PDF header or footer; arXiv version cited
- Version: arXiv 2203.15556v1, Tue, 29 Mar 2022 13:38:03 UTC (current version on the day)
- Fetched: https://arxiv.org/abs/2203.15556 ; https://arxiv.org/pdf/2203.15556
- Status: HTTP 200 (PDF)
- Raw text: `energy_lit/training/2203.15556.txt`
- Rows: E15

Quotes:

> We test this hypothesis by training a predicted computeoptimal model,Chinchilla, that uses the same compute budget asGopher but with 70B parameters and 4

> more more data.Chinchilla uniformly and signiﬁcantly outperformsGopher (280B)

> As a highlight,Chinchilla reaches a state-of-the-art average accuracy of 67.5% on the MMLU benchmark, greater than a 7% improvement overGopher.

## Rows by mechanism

Each row: X vs Y, quality (X / Y), cost (X / Y), matched compute, location. "n.r." = not reported as a number in the quoted text. Full rows with quotes are in `training_rows.json`.

### E1: hyperparameter transfer from a small proxy (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| muTransfer (HPs tuned on 40M-parameter proxy, transferred zero-shot) | 6.7B re-run with the original GPT-3 HPs | validation loss (cross-entropy) (higher_is_better false) | 1.98 | 2.03 | HP tuning cost, % of total pretraining cost | 7 | n.r. | no | Yang et al. 2022 (Tensor Programs V), arXiv 2203.03466v2, Section 7.4, Table 7 |
| muTransfer (proxy-tuned HPs) | Megatron default HPs (BERT-large) | test loss (higher_is_better false) | 1.683 | 1.731 | HP tuning FLOPs (in units of one BERT-large pretraining) | n.r. | n.r. | no | Yang et al. 2022 (Tensor Programs V), arXiv 2203.03466v2, Section 7.3, Table 6 |
| u-muP (HPs swept on proxy, transferred) | SP (Pythia init + Llama 3 LR scheme) | MMLU accuracy (%) (higher_is_better true) | 29 | 29.6 | tokens | n.r. | n.r. | yes | Blake et al. 2024 (u-muP), arXiv 2407.17465v3, Table 4 |
| u-muP (HPs swept on proxy, transferred) | SP (Pythia init + Llama 3 LR scheme) | HellaSwag accuracy (%) (higher_is_better true) | 53.4 | 52.4 | tokens | n.r. | n.r. | yes | Blake et al. 2024 (u-muP), arXiv 2407.17465v3, Table 4 |
| per-layer LR prescription for standard parameterization | muP | eval loss (qualitative only in quoted text) (higher_is_better false) | n.r. | n.r. | none reported | n.r. | n.r. | yes | Everett et al. 2024, arXiv 2407.05872v2, Abstract |
| optimal per-module HPs (transferred) | optimal global HPs (transferred) | loss (speed-up to equal loss) | n.r. | n.r. | tokens to reach equal loss (speed-up factor); proxy search GPU-hours | n.r. | n.r. | no | Mlodozeniec et al. 2025 (Complete(d)P), arXiv 2512.22382v1, Figure 1 caption; Appendix D |

- Yang et al. 2022 (Tensor Programs V), arXiv 2203.03466v2 (Section 7.4, Table 7): Tuning cost of the baseline HPs not reported (taken from the GPT-3 paper). The paper notes the re-run baseline mistakenly used absolute attention.
- Yang et al. 2022 (Tensor Programs V), arXiv 2203.03466v2 (Section 7.3, Table 6): Tuning cost of muTransfer = one BERT-large pretraining; the default HPs were not re-tuned at target scale in this paper. Naive transfer (standard parameterisation) diverged.
- Blake et al. 2024 (u-muP), arXiv 2407.17465v3 (Table 4): Same architecture and token budget per Section 5; HP search cost at target scale not reported for SP.
- Everett et al. 2024, arXiv 2407.05872v2 (Abstract): Numeric comparisons are in figures only.
- Mlodozeniec et al. 2025 (Complete(d)P), arXiv 2512.22382v1 (Figure 1 caption; Appendix D): Speed-up 1.32x at 7.2B (text as extracted lacks spaces). Proxy search cost 6730 A100 GPU-hours (99% of gains within 3168). Both arms use transfer; neither is direct tuning at target scale.

### E2a: calibrated / tuning-free loss weights vs a tuned constant (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| 3-task homoscedastic-uncertainty weighting | approx. optimal fixed weights (0.89, 0.01, 0.1) | segmentation IoU (%) (higher_is_better true) | 63.4 | 62.8 | none reported | n.r. | n.r. | yes | Kendall et al. 2018, arXiv 1705.07115v3, Table 1 |
| 3-task homoscedastic-uncertainty weighting | approx. optimal fixed weights (0.89, 0.01, 0.1) | inverse depth mean error (px) (higher_is_better false) | 0.522 | 0.549 | none reported | n.r. | n.r. | yes | Kendall et al. 2018, arXiv 1705.07115v3, Table 1 |
| GradNorm (alpha = 1.5), one training run | grid search over static task weights (100 networks) | average change in per-task performance (qualitative in text) | n.r. | n.r. | number of training runs | n.r. | 100 | no | Chen et al. 2018 (GradNorm), arXiv 1711.02257v4, Section 5.3, Figure 4 |
| AutoScale (Low Cond.) | linear scalarization with searched weights (best of 20 trials) | Delta_m % (lower is better) (higher_is_better false) | -0.03 | -1.42 | seconds per training iteration (searched weights: x n trials, n = 20) | 0.244 | n.r. | no | Yang et al. 2025 (AutoScale), arXiv 2508.13979v1, Table 1 (CityScapes) |
| AutoScale (Low Cond.) | linear scalarization with searched weights (best of 20 trials) | Delta_m % (lower is better) (higher_is_better false) | -0.37 | -0.44 | seconds per training iteration (searched weights: x n trials) | 0.535 | n.r. | no | Yang et al. 2025 (AutoScale), arXiv 2508.13979v1, Table 1 (NuScenes) |
| uncertainty weighting (UM, Kendall et al.) | linear scalarization with searched weights (best of 20 trials) | Delta_m % (lower is better) (higher_is_better false) | 5.69 | -1.42 | seconds per training iteration (searched weights: x n trials) | 0.199 | n.r. | no | Yang et al. 2025 (AutoScale), arXiv 2508.13979v1, Table 1 (CityScapes) |

- Kendall et al. 2018, arXiv 1705.07115v3 (Table 1): Cost of finding the approx. optimal weights not quantified.
- Kendall et al. 2018, arXiv 1705.07115v3 (Table 1): Unweighted sum of losses in the same table: 50.1% IoU, 0.592 depth error.
- Chen et al. 2018 (GradNorm), arXiv 1711.02257v4 (Section 5.3, Figure 4): Quality numbers are in Figure 4 only.
- Yang et al. 2025 (AutoScale), arXiv 2508.13979v1 (Table 1 (CityScapes)): Searched-weight cost 0.195 s/iter per trial x 20 trials.
- Yang et al. 2025 (AutoScale), arXiv 2508.13979v1 (Table 1 (NuScenes)): Searched-weight cost 0.453 s/iter per trial x n trials.

### E2b: adaptive multi-task balancers vs the plain sum of losses (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| PCGrad | unitary scalarization (sum of losses) with standard regularization | average task test accuracy (mean, 95% CI) (higher_is_better true) | 0.9093 | 0.909 | epoch runtime [s], interquartile range lower bound | 10150 | 286.9 | no | Kurin et al. 2022, arXiv 2201.04122v4, Appendix D, Figure 8(c) |
| IMTL | unitary scalarization | average task test accuracy (mean, 95% CI) (higher_is_better true) | 0.9093 | 0.909 | epoch runtime [s], interquartile range lower bound | 360 | 286.9 | no | Kurin et al. 2022, arXiv 2201.04122v4, Appendix D, Figure 8(c) |
| MTO methods requiring per-task gradients | scalarization (weighted sum of losses) | Pareto front of task performance (qualitative) | n.r. | n.r. | training steps per second | 5 | 12 | no | Xin et al. 2022, NeurIPS 2022 proceedings (no arXiv), Section 5 (compute) |
| GradNorm (alpha = 1.5) | equal weights (sum of losses) | depth RMS error (m) (higher_is_better false) | 0.663 | 0.697 | none reported | n.r. | n.r. | yes | Chen et al. 2018 (GradNorm), arXiv 1711.02257v4, Table 2 (ResNet backbone) |
| GradNorm | linear scalarization, unitary weights | Delta_m % (lower is better) (higher_is_better false) | 12.11 | 10.62 | seconds per training iteration | 0.572 | 0.195 | no | Yang et al. 2025 (AutoScale), arXiv 2508.13979v1, Table 1 (CityScapes) |
| uncertainty weighting (UM) | linear scalarization, unitary weights | Delta_m % (lower is better) (higher_is_better false) | 5.69 | 10.62 | seconds per training iteration | 0.199 | 0.195 | no | Yang et al. 2025 (AutoScale), arXiv 2508.13979v1, Table 1 (CityScapes) |

- Kurin et al. 2022, arXiv 2201.04122v4 (Appendix D, Figure 8(c)): Values printed in scientific notation (9.093e-01 etc.). ± is a 95% confidence interval, not SD; runtime given as IQR [1.015e+04, 1.016e+04] vs [2.869e+02, 2.878e+02] s/epoch.
- Kurin et al. 2022, arXiv 2201.04122v4 (Appendix D, Figure 8(c)): Values printed in scientific notation. ± is a 95% CI. MGDA in the same table: 0.9022 at [685.9, 719.4] s/epoch.
- Xin et al. 2022, NeurIPS 2022 proceedings (no arXiv) (Section 5 (compute)): Throughput: approximately 5 (MTO) vs approximately 12 (scalarization) steps/s; higher is cheaper.
- Chen et al. 2018 (GradNorm), arXiv 1711.02257v4 (Table 2 (ResNet backbone)): Uncertainty weighting (Kendall et al.) in the same table: 0.702.

### E3: successive halving / Hyperband / ASHA (5 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| Hyperband | random search | test error (qualitative in text) (higher_is_better false) | n.r. | n.r. | budget to reach a given error (speed-up factor) | n.r. | n.r. | no | Li et al. 2018 (Hyperband, JMLR), arXiv 1603.06560v4, Section 4.1 (Figure 4) |
| Hyperband | Bayesian optimization (SMAC, TPE, Spearmint) | validation/test error (qualitative) (higher_is_better false) | n.r. | n.r. | time to reach a given error (speed-up factor) | n.r. | n.r. | no | Li et al. 2018 (Hyperband, JMLR), arXiv 1603.06560v4, Abstract |
| Hyperband | random search | regret (qualitative) (higher_is_better false) | n.r. | n.r. | time to reach a given regret (speed-up factor) | n.r. | n.r. | no | Falkner et al. 2018 (BOHB), arXiv 1807.01774v1, Section 5 (Figure 5) |
| BOHB | Hyperband | final performance (qualitative) | n.r. | n.r. | time to same final performance (speed-up factor) | n.r. | n.r. | no | Falkner et al. 2018 (BOHB), arXiv 1807.01774v1, Section 5 (Figure 5) |
| ASHA | Vizier (Google black-box optimization) | test perplexity of best configuration (higher_is_better false) | 76.6 | 78.4 | time (units of time(R)) to perplexity below 80 (speed-up factor) | n.r. | n.r. | no | Li et al. 2020 (ASHA, MLSys), arXiv 1810.05934v5, Section 4.4 (Figure 5) |

- Li et al. 2018 (Hyperband, JMLR), arXiv 1603.06560v4 (Section 4.1 (Figure 4)): Speed-up >20x over random search (budget measured in multiples of R).
- Li et al. 2020 (ASHA, MLSys), arXiv 1810.05934v5 (Section 4.4 (Figure 5)): The 78.4 reference is the published hand-tuned result (Zaremba et al.), not Vizier.

### E4: learning-curve extrapolation (7 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| HPO with predictive termination (learning-curve extrapolation) | same HPO without early termination (full-length runs) | validation error reached (same) (higher_is_better false) | n.r. | n.r. | wall time per HPO run (hours) | 18 | 40 | no | Domhan et al. 2015, IJCAI 2015 proceedings (no arXiv), Section 4 (CIFAR-10 fully connected nets) |
| SMAC (early): SMAC with the Domhan et al. (2015) extrapolation-based early stopping | Hyperband | average test error (qualitative) (higher_is_better false) | n.r. | n.r. | budget to reach a given error (speed-up factor) | n.r. | n.r. | no | Li et al. 2018 (Hyperband, JMLR), arXiv 1603.06560v4, Section 4.1 (Figure 4) |
| HB-LCNet (Hyperband with learning-curve prediction) | Hyperband alone | regret (qualitative) (higher_is_better false) | n.r. | n.r. | none reported | n.r. | n.r. | no | Falkner et al. 2018 (BOHB), arXiv 1807.01774v1, Section 5 |
| LC-PFN predictive early-stopping criterion | no-stop (train every run to the end) | anytime regret (same or lower) (higher_is_better false) | n.r. | n.r. | training time to equal regret (speed-up factor) | n.r. | n.r. | no | Adriaensen et al. 2023 (LC-PFN), arXiv 2310.20447v1, Section 5 |
| LC-PFN predictive early-stopping criterion (and 9 Patience heuristics) | no-stop | anytime regret (higher_is_better false) | n.r. | n.r. | none | n.r. | n.r. | no | Adriaensen et al. 2023 (LC-PFN), arXiv 2310.20447v1, Section 5 |
| freeze-thaw BO with learning-curve surrogates (ifBO, DyHPO, DPL) | Hyperband, ASHA, random search | normalized regret (qualitative) (higher_is_better false) | n.r. | n.r. | total epochs spent | n.r. | n.r. | yes | Rakotoarison et al. 2024 (ifBO), arXiv 2404.16795v3, Section 5, Figure 3 |
| DyHPO (deep-kernel GP over learning curves) | Hyperband, ASHA, BOHB, DEHB, random search | mean regret (qualitative) (higher_is_better false) | n.r. | n.r. | wall-clock time including optimizer overhead | n.r. | n.r. | yes | Wistuba et al. 2022 (DyHPO), arXiv 2202.09774v2, Section 5, Figure 5 |

- Domhan et al. 2015, IJCAI 2015 proceedings (no arXiv) (Section 4 (CIFAR-10 fully connected nets)): Reference arm is HPO without early stopping, not successive halving.
- Li et al. 2018 (Hyperband, JMLR), arXiv 1603.06560v4 (Section 4.1 (Figure 4)): On MRBI Hyperband was 5x faster than SMAC (early); on SVHN SMAC (early) outperformed Hyperband.
- Adriaensen et al. 2023 (LC-PFN), arXiv 2310.20447v1 (Section 5): Reference arm is no early stopping, not successive halving.
- Adriaensen et al. 2023 (LC-PFN), arXiv 2310.20447v1 (Section 5): Failure case.
- Rakotoarison et al. 2024 (ifBO), arXiv 2404.16795v3 (Section 5, Figure 3): Comparison at equal epoch budget; numbers in figures only.
- Wistuba et al. 2022 (DyHPO), arXiv 2202.09774v2 (Section 5, Figure 5): Numbers in figures only.

### E5: continual pre-training vs re-training on the union (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| continual pre-training with LR re-warming/re-decay + 5% replay (300B Pile -> 300B SP) | re-training from scratch on the union (600B Pile U SP) | average validation loss (Pile, SP) (higher_is_better false) | 1.89 | 1.87 | tokens (billions) trained after the Pile checkpoint vs from scratch | 300 | 600 | no | Ibrahim et al. 2024, arXiv 2403.08763v4, Table 4 |
| continual pre-training with re-warming + 5% replay | re-training on the union (600B) | average validation loss (higher_is_better false) | 2.37 | 2.35 | tokens (billions) | 300 | 600 | no | Ibrahim et al. 2024, arXiv 2403.08763v4, Table 4 |
| continual pre-training with re-warming + 5% replay | re-training on the union (600B) | average benchmark accuracy (%) (higher_is_better true) | 47.68 | 48 | tokens (billions) | 300 | 600 | no | Ibrahim et al. 2024, arXiv 2403.08763v4, Table 5 |
| continual pre-training with LR re-warming | training from scratch on the downstream data | downstream (SlimPajama) validation loss (qualitative) (higher_is_better false) | n.r. | n.r. | tokens | n.r. | n.r. | no | Gupta et al. 2023, arXiv 2308.04014v2, Abstract |
| Replay (alpha = 1/2) + AR meta-schedule, 440B tokens | Oracle series (re-train from scratch roughly every two years), 1.16T tokens | in-distribution log-perplexity regret vs Oracle-2024-07 (ID) (higher_is_better false) | 0.016 | 0.037 | total training tokens (billions; Oracle printed as 1.16T) | 440 | 1160 | no | Li et al. 2025 (TiC-LM), arXiv 2504.02107v3, Table 2 (3B, TiC-CC) |
| small replay rates | spending the same compute on model size | loss (qualitative) | n.r. | n.r. | FLOPs | n.r. | n.r. | yes | Abbes et al. 2025, arXiv 2508.01908v1, Abstract |

- Ibrahim et al. 2024, arXiv 2403.08763v4 (Table 4): Continual arm starts from a model already trained on 300B Pile tokens; union arm trains 600B tokens from scratch. Standard error < 0.001 (not reported).
- Ibrahim et al. 2024, arXiv 2403.08763v4 (Table 5): At 405M the continual arm is higher (35.14 vs 34.30) in the same table.
- Li et al. 2025 (TiC-LM), arXiv 2504.02107v3 (Table 2 (3B, TiC-CC)): Backward-transfer regret in the same rows: -0.002 (continual) vs -0.003 (Oracle).
- Abbes et al. 2025, arXiv 2508.01908v1 (Abstract): Not a comparison against re-training from scratch.

### E6a: warm start vs from scratch (3 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| warm start | random initialisation | validation accuracy (%) (higher_is_better true) | 51.7 | 56.2 | none reported | n.r. | n.r. | no | Ash & Adams 2020, arXiv 1910.08475v3, Table 1 |
| warm start (noise 0) | random initialisation | validation accuracy (%) (higher_is_better true) | 50.8 | 55.2 | wall time (minutes) | 13.6 | 34 | no | Ash & Adams 2020, arXiv 1910.08475v3, Appendix Table 4 |
| warm initialisation | random initialisation (cold start) | test accuracy (%) (higher_is_better true) | 63.53 | 67.32 | training steps | 1173 | 5161 | no | Shin et al. 2024 (DASH), arXiv 2410.23495v2, Table 1 |

- Ash & Adams 2020, arXiv 1910.08475v3 (Table 1): Parentheses are standard deviations over 5 runs.
- Ash & Adams 2020, arXiv 1910.08475v3 (Appendix Table 4): Last column (noise 0) is plain warm start; other columns add parameter noise.
- Shin et al. 2024 (DASH), arXiv 2410.23495v2 (Table 1): 5 seeds.

### E6b: shrink-and-perturb vs plain warm start (3 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| shrink & perturb (S&P) | warm initialisation | test accuracy (%) (higher_is_better true) | 81.25 | 63.53 | training steps | 5395 | 1173 | no | Shin et al. 2024 (DASH), arXiv 2410.23495v2, Table 1 |
| shrink & perturb (S&P) | warm initialisation | test accuracy (%) (higher_is_better true) | 34.34 | 9.57 | training steps | 13815 | 3388 | no | Shin et al. 2024 (DASH), arXiv 2410.23495v2, Table 1 |
| shrink & perturb (lambda = 0.6) | fully warm-started (lambda = 1) and fully random (lambda = 0) initialisations | validation accuracy (qualitative) (higher_is_better true) | n.r. | n.r. | training time (qualitative) | n.r. | n.r. | no | Ash & Adams 2020, arXiv 1910.08475v3, Figure 7 |

- Shin et al. 2024 (DASH), arXiv 2410.23495v2 (Table 1): Random init in the same table: 67.32 at 5161 steps; DASH: 84.08 at 6490 steps.
- Shin et al. 2024 (DASH), arXiv 2410.23495v2 (Table 1): 3 seeds; random init 25.69 at 30237 steps.

### E7: model growth vs training the large model from scratch (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| bert2BERT (AKI + two-stage pre-training) | BERT-base trained from scratch (re-implementation) | GLUE+SQuAD average (higher_is_better true) | 85.7 | 85.5 | pre-training FLOPs (x 1e19) | 4 | 7.3 | no | Chen et al. 2022 (bert2BERT), arXiv 2110.07143v1, Table 2 |
| bert2BERT | GPT trained from scratch | PTB perplexity without fine-tuning (higher_is_better false) | 132.1 | 133.8 | pre-training FLOPs (x 1e19) | 2.6 | 4.9 | no | Chen et al. 2022 (bert2BERT), arXiv 2110.07143v1, Table 5 |
| LiGO (learned linear growth operator) | training from scratch | loss/accuracy at equal level (qualitative) | n.r. | n.r. | FLOPs saved (%) | n.r. | n.r. | no | Wang et al. 2023 (LiGO), arXiv 2303.00980v1, Section 1 / Figure 2 |
| G_stack model growth | 7B trained from scratch | training loss (equal) (higher_is_better false) | n.r. | n.r. | tokens (billions) to the same loss | 194 | 300 | no | Du et al. 2024 (Stacking Your Transformers), arXiv 2405.15319v2, Abstract / Figure 1 |
| MSG (masked structural growth) | full-size training from scratch | GLUE average (higher_is_better true) | 83.2 | 82.2 | wall time | n.r. | n.r. | no | Yao et al. 2024 (MSG), arXiv 2305.02869v3, Table 4 |
| MSG | full-size training from scratch | WikiText2 zero-shot perplexity (higher_is_better false) | 41.2 | 41.31 | wall time | n.r. | n.r. | no | Yao et al. 2024 (MSG), arXiv 2305.02869v3, Table 5 |

- Chen et al. 2022 (bert2BERT), arXiv 2110.07143v1 (Table 2): Whether the small model's training FLOPs are included is not stated in the quoted passages.
- Chen et al. 2022 (bert2BERT), arXiv 2110.07143v1 (Table 5): WikiText-2: 47.9 vs 47.0 (grown model worse).
- Wang et al. 2023 (LiGO), arXiv 2303.00980v1 (Section 1 / Figure 2): Savings 44.7% (BERT-Base), 22.5% (GPT2-Medium), 55% (DeiT).
- Du et al. 2024 (Stacking Your Transformers), arXiv 2405.15319v2 (Abstract / Figure 1): Accounting of small-model tokens (growth timing d) described separately in the paper.
- Yao et al. 2024 (MSG), arXiv 2305.02869v3 (Table 4): Wall time 32h, 10min (growth) vs 70h, 48min (full).
- Yao et al. 2024 (MSG), arXiv 2305.02869v3 (Table 5): Wall time 37h, 59min (growth) vs 53h, 1min (full).

### E8: weight averaging vs last iterate (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| LAWA (latest-weight averaging) | original training (last iterate) | zero-shot average accuracy (%) (higher_is_better true) | 51.15 | 47.89 | training steps (thousands) | 50 | 50 | yes | Sanyal et al. 2023 (LAWA), arXiv 2306.03241v2, Table 2 |
| LAWA | original training (last iterate) | zero-shot average accuracy (%) (higher_is_better true) | 49.72 | 51.72 | training steps (thousands) | 50 | 50 | yes | Sanyal et al. 2023 (LAWA), arXiv 2306.03241v2, Table 2 |
| LAWA (average of k latest epoch checkpoints) | baseline optimizer (SGD or Adam), last iterate | loss/accuracy (matched) | n.r. | n.r. | GPU hours saved | n.r. | n.r. | no | Kaddour 2022, arXiv 2209.14981v2, Abstract, Figure 1 |
| EMA of weights (early-stopped at best accuracy) | momentum SGD last iterate | validation accuracy (%) (higher_is_better true) | 76.14 | 75.83 | epochs to the early-stopping point | n.r. | n.r. | no | Morales-Brotons et al. 2024, arXiv 2411.18704v1, Appendix Table 6 |
| NadamW + LAWA | NadamW (no averaging) | reach the AlgoPerf validation target (matched) | n.r. | n.r. | GPU-hours for one run of the suite | 550 | 612 | no | Ajroldi et al. 2025, arXiv 2502.06761v3, Table 1 |
| NadamW + EMA | NadamW (no averaging) | reach the AlgoPerf validation target (matched) | n.r. | n.r. | GPU-hours for one run of the suite | 541 | 612 | no | Ajroldi et al. 2025, arXiv 2502.06761v3, Table 1 |

- Sanyal et al. 2023 (LAWA), arXiv 2306.03241v2 (Table 2): Same step count (50 K).
- Sanyal et al. 2023 (LAWA), arXiv 2306.03241v2 (Table 2): Here LAWA is lower on the average.
- Kaddour 2022, arXiv 2209.14981v2 (Abstract, Figure 1): Up to ~68 (ImageNet) and ~30 (RoBERTa) GPU hours saved; '/tildelow' is the PDF extraction of '~'.
- Morales-Brotons et al. 2024, arXiv 2411.18704v1 (Appendix Table 6): Extraction splits '76.14' as '76 .14'. Early-stopping epochs per run: SGD [200, 197, 199], EMA (acc.) [143, 139, 156].

### E9: horizon-free LR schedules vs cosine (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| constant LR + 20% linear cooldown (WSD-type) | cosine to 0 | aggregated downstream score (higher_is_better true) | 47.92 | 48.03 | tokens | n.r. | n.r. | yes | Hagele et al. 2024, arXiv 2405.18392v3, Appendix Table 4 |
| constant LR + cooldowns (reusable runs) | cosine (one run per length) | same scaling-law fit (qualitative) | n.r. | n.r. | estimated training FLOPs for the suite | 2.36e+23 | 5.59e+23 | no | Hagele et al. 2024, arXiv 2405.18392v3, Figure 13(b) |
| WSD schedule (decay ~10% of tokens) | cosine schedule with T = S | C4 loss (qualitative) (higher_is_better false) | n.r. | n.r. | tokens | n.r. | n.r. | yes | Hu et al. 2024 (MiniCPM), arXiv 2404.06395v3, Section 4.3 |
| Schedule-Free SGD | cosine schedule | test accuracy (%) (higher_is_better true) | 76.9 | 76.9 | epochs | n.r. | n.r. | yes | Defazio et al. 2024 (Schedule-Free), arXiv 2405.15682v4, Figure 5 |
| Schedule-Free AdamW | cosine schedule | test loss (higher_is_better false) | 2.831 | 2.853 | steps | n.r. | n.r. | yes | Defazio et al. 2024 (Schedule-Free), arXiv 2405.15682v4, Figure 5 |
| linear decay-to-zero (D2Z) at 80 tokens-per-parameter | linear 10x decay at 200 tokens-per-parameter | training/validation loss (higher_is_better false) | n.r. | n.r. | training FLOPs | n.r. | n.r. | no | Bergsma et al. 2025 (Straight to Zero), arXiv 2502.15938v2, Abstract / Figure 1 |

- Hagele et al. 2024, arXiv 2405.18392v3 (Figure 13(b)): '1023' is the extraction of 10^23.
- Defazio et al. 2024 (Schedule-Free), arXiv 2405.15682v4 (Figure 5): Printed spread is a standard error (SE), not SD.
- Defazio et al. 2024 (Schedule-Free), arXiv 2405.15682v4 (Figure 5): SE, not SD.
- Bergsma et al. 2025 (Straight to Zero), arXiv 2502.15938v2 (Abstract / Figure 1): 60% fewer FLOPs for lower loss. Figure 8 of the same paper: 'D2Z surpassesCyclicand WSDschedules' (610M, 80 TPP).

### E10: training-data deduplication (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| NearDup-deduplicated C4 | original C4 | perplexity (no worse; qualitative) (higher_is_better false) | n.r. | n.r. | estimated training energy (MWh) | 5.63 | 5.86 | no | Lee et al. 2022, arXiv 2107.06499v2, Appendix D, Table 6 |
| NearDup-deduplicated C4 | original C4 | % of emitted tokens memorised (1 epoch) (higher_is_better false) | 0.189 | 1.926 | none | n.r. | n.r. | no | Lee et al. 2022, arXiv 2107.06499v2, Table 4 |
| SemDeDup keeping 50% of data | baseline trained on 100% of data | zero-shot ImageNet accuracy (higher_is_better true) | n.r. | n.r. | fraction of data / training | n.r. | n.r. | no | Abbas et al. 2023 (SemDeDup), arXiv 2303.09540v3, Figure 4 caption |
| SemDeDup keeping 63% of data | baseline trained on 100% of data | average zero-shot performance (qualitative) (higher_is_better true) | n.r. | n.r. | pre-training time (speed-up) | n.r. | n.r. | no | Abbas et al. 2023 (SemDeDup), arXiv 2303.09540v3, Figure 4 caption |
| SemDeDup-pruned C4 (80% kept), trained past one epoch | baseline C4 | perplexity on prompts_with_answer (matched) (higher_is_better false) | n.r. | n.r. | % of baseline training FLOPs | 95 | n.r. | no | Abbas et al. 2023 (SemDeDup), arXiv 2303.09540v3, Figure 8 |
| D4 (dedup + embedding-based diversification) | randomly selected (MinHash-deduplicated) data | average 0-shot accuracy on 16 NLP tasks; validation perplexity (higher_is_better true) | n.r. | n.r. | tokens to equal perplexity (efficiency gain %) | n.r. | n.r. | no | Tirumala et al. 2023 (D4), arXiv 2308.12284v1, Abstract / Figure 1 |

- Lee et al. 2022, arXiv 2107.06499v2 (Appendix D, Table 6): Energy is an estimate from Patterson et al. (2021) per-core rates.
- Abbas et al. 2023 (SemDeDup), arXiv 2303.09540v3 (Figure 4 caption): 0.47% drop at 50% data.

### E11: salience / difficulty-scored data pruning (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| high-perplexity-selected data (50% rate) | no pruning (baseline) | average normalized accuracy (higher_is_better true) | 20.67 | 18.63 | tokens | n.r. | n.r. | yes | Ankner et al. 2024, arXiv 2405.20541v1, Table 1 |
| medium-perplexity-selected data (50% rate) | no pruning (baseline) | average normalized accuracy (higher_is_better true) | 19.79 | 19.2 | tokens | n.r. | n.r. | yes | Ankner et al. 2024, arXiv 2405.20541v1, Table 1 |
| perplexity pruning (middle 50%) | no pruning | test perplexity (relative improvement %) | n.r. | n.r. | data fraction | n.r. | n.r. | no | Marion et al. 2023, arXiv 2309.04564v1, Section 4.2 |
| perplexity-based pruning (EL2N and memorization also listed) | random pruning | test perplexity (qualitative) (higher_is_better false) | n.r. | n.r. | data fraction (matched) | n.r. | n.r. | yes | Marion et al. 2023, arXiv 2309.04564v1, Section 4.2 / Figure 4 |
| perplexity (52B reference) middle subset, 30% | random pruning, 30% | SST2 accuracy (higher_is_better true) | 77.34 | 77.29 | data fraction (matched) | n.r. | n.r. | yes | Marion et al. 2023, arXiv 2309.04564v1, Table 2 (SST2 column) |
| score-based pruning metrics | random pruning / full dataset | top-1 accuracy (qualitative) (higher_is_better true) | n.r. | n.r. | fraction of data kept | n.r. | n.r. | yes | Sorscher et al. 2022, arXiv 2206.14486v6, Section 6 (ImageNet benchmark) |

- Ankner et al. 2024, arXiv 2405.20541v1 (Table 1): Cost of the 125M reference model not included in the comparison.
- Marion et al. 2023, arXiv 2309.04564v1 (Section 4.2): Data fractions 50% and 30%.
- Marion et al. 2023, arXiv 2309.04564v1 (Table 2 (SST2 column)): Printed spreads labelled standard deviation (0.005, 0.007) appear to be on a fraction scale; left null here. No pruning: 78.15.

### E12: reduced-precision training (6 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| mixed precision (FP16 with FP32 master weights, loss scaling) | FP32 baseline | top-1 accuracy (%) (higher_is_better true) | 76.04 | 75.92 | memory (qualitative) | n.r. | n.r. | yes | Micikevicius et al. 2018, arXiv 1710.03740v3, Table 1 |
| FP8 (GEMM inputs clipped to FP8) | 16-bit baseline (FP16 or bfloat16) | perplexity (higher_is_better false) | 6.68 | 6.65 | none reported | n.r. | n.r. | yes | Micikevicius et al. 2022 (FP8 formats), arXiv 2209.05433v2, Table 4 |
| FP8 mixed-precision training | BF16 baseline | relative loss error (%) (higher_is_better false) | n.r. | n.r. | GEMM compute speed (theoretical) | n.r. | n.r. | yes | DeepSeek-AI 2024 (DeepSeek-V3), arXiv 2412.19437v2, Section 3.3; Appendix B.1 |
| NVFP4 pretraining | FP8 pretraining | MMLU-Pro 5-shot accuracy (%) (higher_is_better true) | 62.58 | 62.62 | math throughput relative to FP8 | n.r. | n.r. | yes | NVIDIA 2025 (NVFP4 pretraining), arXiv 2509.25149v2, Abstract; Table 2 |
| MXFP4 | NVFP4 | final training loss (matched) (higher_is_better false) | n.r. | n.r. | tokens (trillions) | 1.36 | 1 | no | NVIDIA 2025 (NVFP4 pretraining), arXiv 2509.25149v2, Section 5 (Figure 6b) |
| u-muP FP8 | u-muP BF16 | MMLU accuracy (%) (higher_is_better true) | 31.2 | 29 | tokens | n.r. | n.r. | yes | Blake et al. 2024 (u-muP), arXiv 2407.17465v3, Table 4 |

- Micikevicius et al. 2022 (FP8 formats), arXiv 2209.05433v2 (Table 4): Extraction shows '6 .68'. Paper reports quality only; no speed or energy measured.
- DeepSeek-AI 2024 (DeepSeek-V3), arXiv 2412.19437v2 (Section 3.3; Appendix B.1): Relative loss error < 0.25%; speed doubling is theoretical for GEMMs. Full DeepSeek-V3 training: 2.788M H800 GPU hours.
- NVIDIA 2025 (NVFP4 pretraining), arXiv 2509.25149v2 (Abstract; Table 2): Throughput figures are hardware peak rates, not measured end-to-end training speed. Relative loss error < 1% in the stable phase, slightly above 1.5% during decay.
- Blake et al. 2024 (u-muP), arXiv 2407.17465v3 (Table 4): HellaSwag equal (53.4); OpenBookQA lower in FP8 (29.6 vs 31.6).

### E14: mixture-of-experts vs dense (silent) (2 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| Switch Transformer (sparse MoE) | dense T5 at the same FLOPs per token | pre-training quality (speed to equal loss) | n.r. | n.r. | pre-training time (speed-up) | n.r. | n.r. | yes | Fedus et al. 2022 (Switch Transformer), arXiv 2101.03961v3, Abstract |
| DeepSeekMoE 16B | DeepSeek 7B dense (same 2T corpus) | benchmark performance (comparable) | n.r. | n.r. | training computation (relative) | n.r. | n.r. | no | Dai et al. 2024 (DeepSeekMoE), arXiv 2401.06066v1, Abstract / Section 1 |

- Fedus et al. 2022 (Switch Transformer), arXiv 2101.03961v3 (Abstract): Silent row, recorded only.
- Dai et al. 2024 (DeepSeekMoE), arXiv 2401.06066v1 (Abstract / Section 1): Silent row.

### E15: compute-optimal allocation (silent) (1 rows)

| X | Y | quality metric | X | Y | cost metric | X | Y | matched | source, location |
|---|---|---|---|---|---|---|---|---|---|
| compute-optimal allocation (70B params, 4x more data) | Gopher 280B at the same compute | MMLU accuracy (%) (higher_is_better true) | 67.5 | n.r. | training FLOPs (same budget) | n.r. | n.r. | yes | Hoffmann et al. 2022 (Chinchilla), arXiv 2203.15556v1, Abstract |

- Hoffmann et al. 2022 (Chinchilla), arXiv 2203.15556v1 (Abstract): Silent row. The extracted text has a control character where the PDF prints 4x (more data), so the quote is split there. Gopher's MMLU not printed in the quoted text (stated as >7% lower).


## Quote check

Run on 2026-09-25 over `training_rows.json` against the saved raw texts (normalisation as stated at the top): 135/135 quotes found. Sources fetched: 47 (45 arXiv, 2 proceedings PDFs); rows: 81.
