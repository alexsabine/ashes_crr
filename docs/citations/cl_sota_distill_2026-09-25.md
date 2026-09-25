# State-of-the-art CL methods, distillation, bias-correction and dual-memory family: mechanisms and ablations, read on the day (R10), 2026-09-25

**Status.** Owner request: prompt-log entry 191. This file is the source record for `CL Design Principle/`. It is a citation
record, not evidence (R8). Nothing here is a result of this repository. Every number below is transcribed from the named
paper's own table or text as fetched on 2026-09-25. None was recomputed here, so none may appear in a ledger row (R1).

**Access.** All fetches were made with `curl` through the session proxy on 2026-09-25:
- the arXiv abstract page for each arXiv work, which gives its submission history;
- the arXiv HTML full text (`arxiv.org/html/<id>vN`). This existed for every arXiv work, and each was converted to text with
  its math alt-text kept;
- the arXiv PDF (`arxiv.org/pdf/<id>vN`), converted to text with pypdfium2 because `pdftotext` is not installed;
- for LUCIR, the CVF open-access HTML page and PDF.

The raw files and text extractions are in the session scratchpad under `lit0925/clsota/distill/`. arXiv ids were verified
by matching the `citation_title` meta tag on each abs page:
- The arXiv export API (`export.arxiv.org/api/query`) returned **HTTP 406** over HTTPS and 301 over HTTP, so the title
  searches used `arxiv.org/search/?searchtype=title` instead (HTTP 200).
- **github.com** returned **HTTP 403** from the proxy for every code link. The repositories' existence was checked instead
  through the GitHub connector's repository search on the same day (see (d) under each work, and
  `github_api_check_2026-09-25.txt` in the scratchpad).
- No arXiv or CVF link returned 404.

Quotes are verbatim from the saved text. LaTeX is kept as the arXiv HTML alt-text. Equations quoted from the HTML appear
inside backticks.

| work | version and date | URL | read |
|---|---|---|---|
| 1. LwF: Li Z, Hoiem D. *Learning without Forgetting* | arXiv 1606.09282 **v3**, 14 Feb 2017 (v1 29 Jun 2016, v2 7 Aug 2016); comments: "Conference version appears in ECCV 2016; updated with journal version" | https://arxiv.org/abs/1606.09282 ; https://arxiv.org/html/1606.09282v3 | [F] |
| 2. iCaRL: Rebuffi S-A, Kolesnikov A, Sperl G, Lampert CH. *iCaRL: Incremental Classifier and Representation Learning* | arXiv 1611.07725 **v2**, 14 Apr 2017 (v1 23 Nov 2016); CVPR 2017 | https://arxiv.org/abs/1611.07725 ; https://arxiv.org/html/1611.07725v2 | [F] |
| 3. DER / DER++: Buzzega P, Boschini M, Porrello A, Abati D, Calderara S. *Dark Experience for General Continual Learning: a Strong, Simple Baseline* | arXiv 2004.07211 **v2**, 22 Oct 2020 (v1 15 Apr 2020); NeurIPS 2020 | https://arxiv.org/abs/2004.07211 ; https://arxiv.org/html/2004.07211v2 | [F] |
| 4. X-DER: Boschini M, Bonicelli L, Buzzega P, Porrello A, Calderara S. *Class-Incremental Continual Learning into the eXtended DER-verse* | arXiv 2201.00766 **v2**, 19 Sep 2022 (v1 3 Jan 2022); IEEE TPAMI | https://arxiv.org/abs/2201.00766 ; https://arxiv.org/html/2201.00766v2 | [F] |
| 5. LUCIR: Hou S, Pan X, Loy CC, Wang Z, Lin D. *Learning a Unified Classifier Incrementally via Rebalancing* | CVPR 2019 open-access version (CVF). No arXiv version was found by title search on arXiv (two title queries, zero hits) | https://openaccess.thecvf.com/content_CVPR_2019/html/Hou_Learning_a_Unified_Classifier_Incrementally_via_Rebalancing_CVPR_2019_paper.html ; PDF .../papers/Hou_Learning_a_Unified_Classifier_Incrementally_via_Rebalancing_CVPR_2019_paper.pdf | [F] (PDF text) |
| 6. BiC: Wu Y, Chen Y, Wang L, Ye Y, Liu Z, Guo Y, Fu Y. *Large Scale Incremental Learning* | arXiv 1905.13260 **v1**, 30 May 2019 (only version) | https://arxiv.org/abs/1905.13260 ; https://arxiv.org/html/1905.13260v1 | [F] |
| 7. WA: Zhao B, Xiao X, Gan G, Zhang B, Xia S. *Maintaining Discrimination and Fairness in Class Incremental Learning* | arXiv 1911.07053 **v1**, 16 Nov 2019 (only version; the arXiv text is the pre-CVPR version) | https://arxiv.org/abs/1911.07053 ; https://arxiv.org/html/1911.07053v1 | [F] |
| 8. PODNet: Douillard A, Cord M, Ollion C, Robert T, Valle E. *PODNet: Pooled Outputs Distillation for Small-Tasks Incremental Learning* | arXiv 2004.13513 **v3**, 6 Oct 2020 (v1 28 Apr 2020, v2 21 Jul 2020); ECCV 2020 | https://arxiv.org/abs/2004.13513 ; https://arxiv.org/html/2004.13513v3 | [F] |
| 9. CLS-ER: Arani E, Sarfraz F, Zonooz B. *Learning Fast, Learning Slow: A General Continual Learning Method based on Complementary Learning System* | arXiv 2201.12604 **v2**, 10 May 2022 (v1 29 Jan 2022); ICLR 2022 camera-ready | https://arxiv.org/abs/2201.12604 ; https://arxiv.org/html/2201.12604v2 | [F] |
| 10. SS-IL: Ahn H, Kwak J, Lim S, Bang H, Kim H, Moon T. *SS-IL: Separated Softmax for Incremental Learning* | arXiv **2003.13947** (id verified by arXiv title search) **v3**, 21 Jun 2022 (v1 31 Mar 2020, v2 1 Dec 2020); ICCV 2021 | https://arxiv.org/abs/2003.13947 ; https://arxiv.org/html/2003.13947v3 | [F] |
| 11. Co2L: Cha H, Lee J, Shin J. *Co$^2$L: Contrastive Continual Learning* | arXiv **2106.14413** **v1**, 28 Jun 2021 (only version); ICCV 2021. The arXiv title search for `Co2L Contrastive Continual` found nothing because arXiv typesets the title as `Co$^2$L`. The id was confirmed from the abs-page title | https://arxiv.org/abs/2106.14413 ; https://arxiv.org/html/2106.14413v1 | [F] |
| 12a. CoFiMA: Marouf IE, Roy S, Tartaglione E, Lathuilière S. *Weighted Ensemble Models Are Strong Continual Learners* (CoMA / CoFiMA) | arXiv **2312.08977** (found by searching for `CoFiMA`; the paper's title does not contain the method name) **v4**, 11 Dec 2024 (v1 14 Dec 2023); ECCV 2024 | https://arxiv.org/abs/2312.08977 ; https://arxiv.org/html/2312.08977v4 | [F] |
| 12b. Mean Teacher (the EMA source that CLS-ER cites for its semantic memories): Tarvainen A, Valpola H. *Mean teachers are better role models: Weight-averaged consistency targets improve semi-supervised deep learning results* | arXiv 1703.01780 **v6**, 16 Apr 2018 (v1 6 Mar 2017); NIPS 2017 | https://arxiv.org/abs/1703.01780 ; https://arxiv.org/html/1703.01780v6 | [F] |

Settings vocabulary used below: *offline* means multi-epoch training on each task, and *online* means one epoch per task.
Class-IL and task-IL are as the papers state them.

---

## 1. LwF (Li & Hoiem, arXiv 1606.09282v3)

**(a) Mechanism.**
- Algorithm box (Fig. 3):
  `"\displaystyle\theta_{s}^{*},~\theta_{o}^{*},~\theta_{n}^{*}\leftarrow\argmin_{\hat{\theta}_{s},\hat{\theta}_{o},\hat{\theta}_{n}}\left(\lambda_{o}\mathcal{L}_{old}(Y_{o},\hat{Y}_{o})+\mathcal{L}_{new}(Y_{n},\hat{Y}_{n})+\mathcal{R}(\hat{\theta}_{s},\hat{\theta}_{o},\hat{\theta}_{n})\right)"`
- "For each original task, we want the output probabilities for each image to be close to the recorded output from the original network. We use the Knowledge Distillation loss, which was found by Hinton et al. [11] to work well for encouraging the outputs of one network to approximate the outputs of another."
- "We use T=2 according to a grid search on a held out set, which aligns with the authors’ recommendations." and "\lambda_{o} is a loss balance weight, set to 1 for most our experiments."

**(b) Ablations.** The setting is task-incremental with a separate output head per task, no replay, AlexNet, and offline
training. The numbers are old-task and new-task accuracy (%). The HTML numbers this table "TABLE II", while the body text
calls it "Table 7".
- Caption: "TABLE II: Performance of our method versus various alternative design choices. In most cases, these alternative choices do not provide consistent advantage or disadvantage compared to our method."
- Sub-table (a): "(a) Changing the number of task-specific layers, using network expansion, or attempting to lower \theta_{s} ’s learning rate when fine-tuning."

| variant | ImageNet→CUB old | new | ImageNet→Scenes old | new | Places365→VOC old | new |
|---|---|---|---|---|---|---|
| LwF at output layer (ours) | 54.7 | 57.7 | 55.9 | 64.5 | 50.6 | 70.2 |
| last hidden layer | 54.7 | 56.2 | 55.7 | 65.0 | 50.7 | 70.6 |
| 2nd last hidden (Fig. 6(a)) | 54.6 | 57.1 | 55.8 | 64.2 | 50.8 | 70.5 |
| network expansion | 57.0 | 54.0 | 57.0 | 62.5 | 51.7 | 67.1 |
| network expansion + LwF | 54.4 | 57.0 | 55.7 | 63.9 | 50.7 | 70.4 |
| fine-tuning (10% θs learning rate) | 52.2 | 54.9 | 54.8 | 62.7 | 49.3 | 69.5 |

- Sub-table (b): "(b) Performing LwF and fine-tuning with and without warmup. The warmup step is not crucial for LwF, but is essential for fine-tuning’s old task performance."

| variant | ImageNet→CUB old | new | ImageNet→Scenes old | new | Places365→VOC old | new |
|---|---|---|---|---|---|---|
| LwF | 54.7 | 57.7 | 55.9 | 64.5 | 50.6 | 70.2 |
| fine-tuning | 50.9 | 57.0 | 53.9 | 63.8 | 48.4 | 70.3 |
| LFL | 52.8 | 55.1 | 55.5 | 63.6 | 50.8 | 69.5 |
| LwF (no warm-up) | 53.5 | 59.9 | 55.2 | 64.9 | 50.4 | 70.0 |
| fine-tuning (no warm-up) | 42.5 | 59.8 | 49.8 | 63.9 | 42.3 | 70.0 |
| LFL (no warm-up) | 52.5 | 55.3 | 55.4 | 63.0 | 50.6 | 69.1 |

The following ablations are reported only as plots (Fig. 7), with no numbers in the text:
- Loss weight λo swept against the L2 weight penalty: "As shown in Figure 7, our method outperforms this baseline, which produces a result between feature extraction (no parameter change) and fine-tuning (free parameter change)."
- Choice of the response-preserving loss (L1, L2, cross-entropy, KD at T=2): "Results indicate our knowledge distillation loss slightly outperforms compared losses, although the advantage is not large."
- Lower learning rate on the shared layers: "A reduced learning rate does not prevent fine-tuning from significantly reducing original task performance, and it reduces new task performance."

**(c) CIFAR headline.** Not reported. The paper has no CIFAR-10 or CIFAR-100 experiment (0 mentions of `CIFAR` in the
v3 text). Its benchmarks are ImageNet or Places365 as the old task, with CUB, Scenes, VOC or MNIST as the new task.

**(d) Code.** The paper prints no code link.

---

## 2. iCaRL (Rebuffi et al., arXiv 1611.07725v2)

**(a) Mechanism.**
- "Finally, the network parameters are updated by minimizing a loss function that for each new image encourages the network to output the correct class indicator for new classes (classification loss), and for old classes, to reproduce the scores stored in the previous step (distillation loss)."
- The distillation term of the loss in Algorithm 3, which uses sigmoid/binary cross-entropy against the stored old-network outputs:
  `"\displaystyle\sum_{y=1}^{s-1}\!q^{y}_{i}\log g_{y}(x_{i})\!+\!(1\!-\!q^{y}_{i})\log(1\!-\!g_{y}(x_{i}))\Big]"`
- Classification: "iCaRL uses a nearest-mean-of-exemplars classification strategy." Exemplars are chosen by herding.

**(b) Ablations.** Section 4.2, "Differential Analysis". Setting: iCIFAR-100, class-IL, K = 2000 exemplars, 32-layer
ResNet, 70 epochs per class batch (offline). The metric is average incremental accuracy.
- The hybrids are defined as follows: "the first (hybrid1) learns a representation in the same way as iCaRL, but uses the network’s outputs directly for classification, not the mean-of-exemplar classifier. The second (hybrid2) uses the exemplars for classification, but does not use the distillation loss during training. The third (hybrid3) uses neither the distillation loss nor exemplars for classification, but it makes use of the exemplars during representation learning."
- Caption of Table 1: "Table 1: Average multi-class accuracy on iCIFAR-100 for different modifications of iCaRL."

| classes per batch | iCaRL | hybrid1 | hybrid2 | hybrid3 | LwF.MC | NCM (Table 1b) |
|---|---|---|---|---|---|---|
| 2 | 57.0 | 36.6 | 57.6 | 57.0 | 11.7 | 59.3 |
| 5 | 61.2 | 50.9 | 57.9 | 56.7 | 32.6 | 62.1 |
| 10 | 64.1 | 59.3 | 59.9 | 58.1 | 44.4 | 64.5 |
| 20 | 67.2 | 65.6 | 63.2 | 60.5 | 54.4 | 67.5 |
| 50 | 68.6 | 68.2 | 65.3 | 61.5 | 64.5 | 68.7 |

- "Comparing iCaRL and hybrid2 one sees that for very small class batch sizes, distillation can even hurt classification accuracy compared to just using prototypes. For larger batch sizes and fewer updates, the use of the distillation loss is clearly advantageous."
- Figure 4 varies the memory budget K. It is a plot, and the text gives no numbers.

**(c) CIFAR-100 headline.** The per-step curves are only in Fig. 2, a plot. The single-number results for iCaRL and its
strongest baseline, LwF.MC, are the iCaRL and LwF.MC columns of Table 1 above. The setting is class-IL with 2, 5, 10, 20
or 50 classes per batch, K = 2000, and 10 class orders. Fig. 2 caption: "Figure 2: Experimental results of class-incremental training on iCIFAR-100 and iILSVRC: reported are multi-class accuracies across all classes observed up to a certain time point."

**(d) Code.** The paper prints "Our source code and further data are available at http://www.github.com/srebuffi/iCaRL."
Through the proxy the link returned HTTP 403 (redirected to https://github.com/srebuffi/iCaRL). The GitHub API search
shows the repository exists and is not archived.

---

## 3. DER / DER++ (Buzzega et al., arXiv 2004.07211v2)

**(a) Mechanism.**
- DER objective: `"\mathcal{L}_{t_{c}}+~\alpha~\mathds{E}_{(x,z)\sim\mathcal{M}}\big[\left\lVert z-h_{\theta}(x)\right\rVert^{2}_{2}\big]."`
- DER++ objective:
  `"\mathcal{L}_{t_{c}}+~\alpha~\mathds{E}_{(x^{\prime},y^{\prime},z^{\prime})\sim\mathcal{M}}\big[\left\lVert z^{\prime}-h_{\theta}(x^{\prime})\right\rVert^{2}_{2}\big]~+~\beta~\mathds{E}_{(x^{\prime\prime},y^{\prime\prime},z^{\prime\prime})\sim\mathcal{M}}\big[\ell(y^{\prime\prime},f_{\theta}(x^{\prime\prime}))\big],"`
- Buffer and weights: "Such a strategy implies picking logits z during the optimization trajectory, so potentially different from the ones that can be observed at the task’s local optimum." and "The model is not overly sensitive to \alpha and \beta : setting them both to 0.5 yields stable performance. (DER++ collapses to DER when \beta=0 )."

**(b) Ablations.** The paper has no dedicated ablation table. The component contrasts it reports are:
- DER (β = 0) against DER++ (β > 0);
- ER, which replays labels only;
- FDR, which replays logits stored at task boundaries.

The Section 5 intent is "By so doing, we gather insights on the employment of logits sampled throughout the optimization trajectory, as opposed to ones at task boundaries and ground truth labels."
Section 5 compares flatness, calibration and buffer informativeness in Fig. 2, which is plots only.
The Table 2 rows that isolate these components are below. Setting: S-CIFAR-10, 5 tasks of 2 classes, ResNet-18, 50 epochs
per task (offline), reservoir buffer, mean ± sd over 10 runs.

| buffer | method | Class-IL | Task-IL |
|---|---|---|---|
| 200 | ER | 44.79 ± 1.86 | 91.19 ± 0.94 |
| 200 | FDR | 30.91 ± 2.74 | 91.01 ± 0.68 |
| 200 | DER | 61.93 ± 1.79 | 91.40 ± 0.92 |
| 200 | DER++ | 64.88 ± 1.17 | 91.92 ± 0.60 |
| 500 | ER | 57.74 ± 0.27 | 93.61 ± 0.27 |
| 500 | FDR | 28.71 ± 3.23 | 93.29 ± 0.59 |
| 500 | DER | 70.51 ± 1.67 | 93.40 ± 0.39 |
| 500 | DER++ | 72.70 ± 1.36 | 93.88 ± 0.50 |
| 5120 | ER | 82.47 ± 0.52 | 96.98 ± 0.17 |
| 5120 | FDR | 19.70 ± 0.07 | 94.32 ± 0.97 |
| 5120 | DER | 83.81 ± 0.33 | 95.43 ± 0.33 |
| 5120 | DER++ | 85.24 ± 0.49 | 96.12 ± 0.21 |

**(c) CIFAR headline.** The main text has no CIFAR-100 experiment. The only CIFAR-100 mention is in the appendix
discussion of single-epoch protocols. The CIFAR-10 headline is the table above, from the Table 2 caption:
"Table 2: Classification results for standard CL benchmarks, averaged across 10 runs. ‘-’ indicates experiments we were unable to run, because of compatibility issues (e.g. between PNN, iCaRL and LwF in Domain-IL) or intractable training time (e.g. GEM, HAL or GSS on Tiny ImageNet)."
- The strongest non-DER baseline on S-CIFAR-10 class-IL is ER at buffers 500 and 5120 (57.74 and 82.47). At buffer 200 it
  is iCaRL (49.02 ± 3.20).
- Also in Table 2 at buffer 200: GSS 39.07 ± 5.59, HAL 32.36 ± 2.70, GEM 25.54 ± 0.76, A-GEM 20.04 ± 0.34, LwF 19.61 ± 0.05
  and SGD 19.62 ± 0.05 (class-IL). JOINT is 92.20 ± 0.15.

**(d) Code.** The URL https://github.com/aimagelab/mammoth is given as a link in the paper. It returned HTTP 403 through
the proxy. The GitHub API search shows the repository exists and is not archived.

---

## 4. X-DER (Boschini et al., arXiv 2201.00766v2)

**(a) Mechanism.**
- Overall objective: `"\operatornamewithlimits{argmin}_{\theta}\quad\mathcal{L}_{\operatorname{X-DER}}\triangleq\mathcal{L}_{\operatorname{DER}}+\mathcal{L}_{\operatorname{S-CE}}+\mathcal{L}_{\operatorname{F}},"`
- Memory update (logits of "future past"): "we propose to implant the corresponding logits \ell_{\operatorname{fp}[c;c]} into the memory entry containing \ell^{{\scriptscriptstyle{\mathcal{M}}}} ."
  The rescaling rule is `"\ell^{\scriptscriptstyle{\mathcal{M}}}_{k}\longleftarrow\ell_{k}\cdot\operatorname{min}(\gamma\frac{\ell^{\scriptscriptstyle{\mathcal{M}}}_{\operatorname{gt}}}{\ell_{\operatorname{fpmax}}},1),\quad k\in\operatorname{fp}[c;c]"`
  with "where \gamma\in[0,1] is a hyperparameter controlling the attenuation rate (which we typically set to 0.75 )."
- Bias mitigation: "Given an example from the current task, we avoid computing the softmax activation on all logits and instead restrict it on those modeling the scores of the current task classes." A hinge term also caps past and future logits below the ground-truth logit: "where m is a hyper-parameter (we typically set it to 0.3 in our experiments) that controls the strictness of the penalty."

**(b) Ablations.** Table I. Setting:
- class-IL;
- Split CIFAR-100 with 10 tasks of 10 classes (ResNet-18), Split miniImageNet with 20 tasks of 5 classes
  (EfficientNet-B2), and Split NTU-60 with 6 tasks (EfficientGCN-B0);
- multi-epoch training (50 epochs for CIFAR-100), from scratch.

The metric is FAA, with FF in parentheses. The variants are defined in the text:
- "X-DER w/o memory update, which does not update logits through the sequence of tasks;"
- "X-DER w/o future heads, which represents the simplest way to handle new classes: namely, it simply adds a new classification head once the new task is presented;"
- "X-DER w/ CE on future heads, a baseline that devises future heads."
- "X-DER w/ RPC, an alternative to the semi-supervised strategy devised in Sec. IV-B."

Caption: "TABLE I: Class-Incremental Continual Learning Final Average Accuracy (FAA) and Final Forgetting (FF) (in parentheses)."

| method | CIFAR-100, M=500 | CIFAR-100, M=2000 | miniImageNet, M=2000 | miniImageNet, M=5000 | NTU-60, M=500 |
|---|---|---|---|---|---|
| JT (upper bound) | 70.44 | | 53.55 | | 85.75 |
| FT (lower bound) | 9.43 (89.82) | | 4.51 (77.38) | | 15.74 (92.85) |
| LwF.MC | 16.22 (54.89) | | 12.20 (23.96) | | 28.24 (46.50) |
| ER | 22.10 (73.64) | 38.58 (53.28) | 14.57 (64.49) | 21.42 (50.36) | 51.77 (48.54) |
| GDumb | 9.98 | 20.66 | 15.22 | 27.79 | 27.59 |
| ER-ACE | 38.75 (40.04) | 49.72 (25.71) | 22.60 (23.74) | 27.92 (19.72) | 52.14 (23.33) |
| RPC | 22.34 (71.94) | 38.33 (52.33) | 15.60 (61.00) | 24.69 (46.34) | 49.40 (48.10) |
| BiC | 36.02 (51.85) | 46.39 (40.49) | 12.96 (57.19) | 14.45 (56.55) | 29.20 (66.16) |
| iCaRL | 46.52 (22.06) | 49.82 (18.07) | 22.58 (16.46) | 22.78 (16.37) | 45.83 (21.48) |
| LUCIR | 40.59 (34.55) | 41.73 (25.41) | 14.97 (43.83) | 17.61 (39.01) | 58.06 (32.58) |
| DER | 36.60 (54.99) | 51.89 (34.54) | 22.96 (48.78) | 29.83 (36.38) | 49.49 (43.09) |
| DER++ | 38.25 (50.54) | 53.63 (33.66) | 23.44 (46.69) | 30.43 (37.11) | 55.32 (35.95) |
| X-DER w/o memory update | 42.67 (24.03) | 56.55 (9.24) | 25.76 (16.76) | 31.40 (13.50) | 57.66 (12.52) |
| X-DER w/o future heads | 45.61 (33.31) | 55.00 (22.94) | 21.71 (36.92) | 27.45 (18.39) | 61.02 (9.80) |
| X-DER w/ CE future heads | 47.67 (25.12) | 55.61 (10.52) | 27.18 (36.12) | 30.69 (16.80) | 61.58 (10.94) |
| X-DER w/ RPC future heads | 48.53 (26.94) | 57.00 (12.65) | 26.38 (38.33) | 29.91 (28.29) | 62.41 (8.88) |
| X-DER | 49.93 (19.90) | 59.14 (12.58) | 28.19 (20.45) | 31.70 (15.87) | 64.86 (9.95) |

JT, FT and LwF.MC need no buffer, so the table prints one value per dataset for them.
- "By omitting to update the content of the memory buffer (X-DER w/o memory update), we see a significant drop in performance – especially relevant for smaller \mathcal{M}_{\text{size}} ." and "Comparatively, the strategy adopted for preparing future logits is less influential."
- Table II (secondary information on CIFAR-100 super-classes; lower is better) reports "X-DER w/o memory update"
  SS-ERR 0.64 / 0.61 and SS-NLL 2.14 / 2.10, against X-DER 0.57 / 0.56 and 1.83 / 1.82, at M = 500 / 2000.
- The paper states that hyperparameter sensitivity is in App. F-A. That table was not transcribed.

**(c) CIFAR-100 headline.** From Table I above (Split CIFAR-100, class-IL, multi-epoch): X-DER is 49.93 at M=500 and 59.14
at M=2000. The strongest baseline is iCaRL at M=500 (46.52) and DER++ at M=2000 (53.63).

**(d) Code.** "we make the code-base available at https://github.com/aimagelab/mammoth". The link returned HTTP 403
through the proxy. The GitHub API search shows the repository exists.

---

## 5. LUCIR (Hou et al., CVPR 2019, CVF open-access PDF)

The equations in the PDF text extraction are garbled, so only prose is quoted. In the CVF PDF text, a line-break hyphen
appears as the character U+FFFE. The quote check treats U+FFFE followed by whitespace as a join; see the Quote check section below.

**(a) Mechanism.**
- "Combining the losses presented above, we reach a total loss comprised of three terms". Eq. (9) sums three terms:
  cross-entropy, λ times the feature distillation L^G_dis, and the margin-ranking loss L_mr on the reserved old samples.
- "To enforce a stronger constraint on the previous knowledges, we propose to fix the old class embeddings and compute a novel distillation loss on the features as below:" with "L G dis encourages the orientation of features extracted by current network to be similar to those by the original model."
- "where |Co| and |Cn| are the number of old and new classes in each phase, λbase is a fixed constant for each dataset. In general, λ increases when the ratio of the number of new classes to that of old classes increases." Cosine normalization handles the logits, and the margin-ranking loss "we introduce a margin ranking loss to ensure that they are well separated."

**(b) Ablations.** Section 4.4. Setting: CIFAR100 with 5 phases after a 50-class base, class-IL, 20 exemplars per class
(herding), 32-layer ResNet, 160 epochs (offline). **All ablation results are in figures only (Fig. 7(a), Fig. 8), and the
text gives no numbers.**
- "Our approach are mainly comprised of three components, i.e. cosine normalization (CN), less-forget constraint (LC), inter-class separation (IS)), When all the training is done, a class balance finetune (CBF) is further conducted on the reserved samples."
- "From the results in Figure 7(a), we can observe that, each component has its contribution to the performance achieved by our final model, while CBF has a relatively small effect on this dataset since the adverse effects of the imbalance is mitigated by the former three components."
- Adaptive weight against a fixed λbase (Fig. 8, CIFAR100 with 5 and 10 phases): "the adaptive loss weight for the distillation loss can help achieve better performance for long sequences of classes."
- The only printed numbers are in the Fig. 9 caption labels: "(a) iCaRL-CNN (51.80%) (b) iCaRL-NME (59.13%)" and
  "(c) Ours-NME (60.21%) (d) Ours-CNN (62.34%)". These are the overall top-1 on 100 classes for CIFAR100 in 1 phase.

**(c) CIFAR-100 headline.** The main results are plotted only in Fig. 5, with no numbers in the text. Caption: "Figure 5. The performance on CIFAR100. The average and standard deviations are obtained over three runs."
- Text: "Particularly, under the incremental setting of 10 phases (Figure 5(d)), the overall performance on the total 100 classes at the end of incremental learning is improved by more than 6%(Ours-CNN vs. iCaRL-NME)."
- The strongest baseline is iCaRL (CNN and NME).
- Third-party tabulations of LUCIR on CIFAR100 appear in PODNet Table 1 (§8) and X-DER Table I (§4).

**(d) Code.** The paper prints no code link. The CVF page returned HTTP 200.

---

## 6. BiC (Wu et al., arXiv 1905.13260v1)

**(a) Mechanism.**
- Stage-1 loss: `"\displaystyle L=\lambda L_{d}+(1-\lambda)L_{c},"` with "The scalar \lambda is set to \frac{n}{n+m} , where n and m are the number of old and new classes."
- Stage-2 bias layer: `"&\alpha o_{k}+\beta&n+1\leq k\leq n+m&\end{aligned}\right.,"` and "Note that the bias parameters ( \alpha , \beta ) are shared by all new classes, allowing us to estimate them with a small validation set. When optimizing the bias parameters, the convolution and fully connected layers are frozen."

**(b) Ablations.** Section 6.6. Setting: CIFAR-100, class-IL, 5 batches of 20 classes, 2,000 exemplars, 32-layer ResNet,
250 epochs per step (offline).
- Caption of Table 3: "Table 3: Incremental learning results on CIFAR-100 with a batch of 20 classes. baseline-1 uses the classification loss alone. baseline-2 uses both the distilling loss and the classification loss. BiC corrects the bias in FC layer of baseline-2. Upper bound retrains the last FC layer using all samples from both old and new classes after learning the model of baseline-2."

| variant | cls loss | distilling loss | bias removal | FC retrain | 20 | 40 | 60 | 80 | 100 |
|---|---|---|---|---|---|---|---|---|---|
| baseline-1 | ✓ | | | | 84.40 | 68.30 | 55.10 | 48.52 | 39.83 |
| baseline-2 | ✓ | ✓ | | | 85.05 | 72.22 | 59.41 | 50.43 | 40.34 |
| BiC (Ours) | ✓ | ✓ | ✓ | | 84.00 | 74.69 | 67.93 | 61.25 | 56.69 |
| upper bound | ✓ | ✓ | | ✓ | 84.39 | 76.15 | 69.51 | 64.03 | 60.93 |

- Table 4 (train_old:val_old split; same setting). At classes 20/40/60/80/100:

  | split | 20 | 40 | 60 | 80 | 100 |
  |---|---|---|---|---|---|
  | 9:1 | 84.00 | 74.69 | 67.93 | 61.25 | 56.69 |
  | 8:2 | 84.50 | 73.19 | 65.01 | 58.68 | 54.31 |
  | 7:3 | 84.70 | 71.60 | 63.68 | 58.12 | 53.74 |
  | 6:4 | 83.33 | 68.84 | 62.21 | 56.00 | 51.17 |

- Table 5 (exemplar selection): random 85.20 / 74.59 / 66.76 / 60.14 / 55.55 against iCaRL herding 84.00 / 74.69 / 67.93 /
  61.25 / 56.69.
- "With the help of the knowledge distillation, baseline-2 is slightly better than baseline-1 since it retains the classification capability on the old classes." and "The classification accuracy on the final step (100 classes) is boosted from 40.34% to 56.69%."

**(c) CIFAR-100 headline.** The comparison with the state of the art on CIFAR-100 is plotted only in Fig. 8, with no
numbers in the text. Caption: "Figure 8: Incremental learning results on CIFAR-100 with split of (a) 5 classes, (b) 10 classes, (c) 20 classes and (d) 50 classes."
Text: "Our BiC method has similar performance with iCaRL [19] and EEIL [2]. BiC is better on the split of 50 and 20 classes, but is slightly behind EEIL on the split of 10 and 5 classes. The margins are small for all splits."
The paper's large-scale headline is ImageNet-1000 and Celeb-10000 (Tables 1 and 2), which were not transcribed. A
third-party CIFAR-100 tabulation of BiC is in WA Table 4 (§7).

**(d) Code.** The paper prints no BiC code link. It links only the TensorFlow ResNet models and the iCaRL repository.

---

## 7. WA (Zhao et al., arXiv 1911.07053v1)

**(a) Mechanism.**
- `"\mathcal{L}(\mathbf{x},y)=(1-\lambda)\mathcal{L}_{CE}(\mathbf{x},y)+\lambda\mathcal{L}_{KD}(\mathbf{x}),"` with λ set to C_old/(C+C_old) "according to the recommendation in [32]".
- `"\widehat{\mathbf{W}}_{new}=\gamma\cdot\mathbf{W}_{new},"` with `"\gamma=\frac{Mean(\textit{{Norm}}_{old})}{Mean(\textit{{Norm}}_{new})},"`
- "In WA, the norms of the weight vectors of new classes are aligned to those of old classes." Also: "weight clipping [2] can be performed after each optimization step in training."

**(b) Ablations.** Section 5.2, Table 2. Setting: CIFAR-100, class-IL, 5 steps of 20 classes, 2,000 exemplars, 32-layer
ResNet, 250 epochs (offline).
- Caption: "Table 2: Class incremental learning performance (top-1 accuracy %) on CIFAR-100 with 5 incremental steps and 20 classes per step. The gains on the basis of Variation1 are also reported in parentheses."

| variant | 20 | 40 | 60 | 80 | 100 | Average |
|---|---|---|---|---|---|---|
| Variation1 (CE) | 83.5 | 70.7 | 58.2 | 49.2 | 43.3 | 55.3 |
| Variation2 (CE + WA) | 83.5 | 74.3 (+3.6) | 64.0 (+5.8) | 56.9 (+7.7) | 50.8 (+7.5) | 61.5 (+6.2) |
| Variation3 (CE + KD) | 83.5 | 72.8 (+2.1) | 60.1 (+1.9) | 49.9 (+0.7) | 42.9 (−0.4) | 56.4 (+1.1) |
| Variation4 (CE + KD + WNL) | 83.1 | 72.3 (+1.6) | 61.6 (+3.4) | 53.1 (+3.9) | 46.0 (+2.7) | 58.2 (+2.9) |
| Ours (CE + KD + WA) | 83.5 | 75.5 (+4.8) | 68.7 (+10.5) | 63.1 (+13.9) | 59.2 (+15.9) | 66.6 (+11.3) |
| Upper Bound | | | | | | 70.1 |

- "It is worth noting that the gain brought by the combination of KD and WA is greater than the sum of the gains from each component used separately, e.g., for the average results, the gain of the combination (Ours) is 11.3%, and the gains of WA (Variation2) and KD (Variation3) used separately are 6.2% and 1.1% respectively."
- Section 5.4 ablates weight clipping, 1-norm against 2-norm, the FC bias term and exemplar selection on ImageNet-100 with
  10 steps. These are plots only (Fig. 6), with no numbers in the text. Examples: "1-norm and 2-norm achieve similar results, which indicates our method is not sensitive to norm selection." and "We see that the bias term in the FC layer can only influence the performance slightly."

**(c) CIFAR-100 headline.** Caption: "Table 4: Class incremental learning performance (top-1 accuracy %) on CIFAR100 with 2, 5, 10 and 20 incremental steps. The average results over all the incremental steps except the first step are reported." Setting: class-IL with 2,000 exemplars in total.

| method | 2 steps | 5 | 10 | 20 |
|---|---|---|---|---|
| LwF.MC | 52.6 | 47.1 | 39.7 | 29.7 |
| iCaRL | 62.0 | 63.3 | 61.6 | 59.7 |
| EEIL | 60.8 | 63.7 | 63.6 | 63.4 |
| BiC | 64.9 | 65.1 | 63.5 | 62.1 |
| Ours (WA) | 65.1 | 66.6 | 64.5 | 62.6 |
| Upper Bound | 70.1 | | | |

The strongest baseline is BiC at 2, 5 and 10 steps, and EEIL at 20 steps (63.4 against WA 62.6).

**(d) Code.** The paper prints "The code will be made publicly available." and no link.

---

## 8. PODNet (Douillard et al., arXiv 2004.13513v3)

**(a) Mechanism.**
- `"\mathcal{L}_{\text{POD-final}}(\mathbf{x})=\frac{\lambda_{c}}{L-1}\sum_{\ell=1}^{L-1}\mathcal{L}_{\text{POD-spatial}}\left(f^{t-1}_{\ell}(\mathbf{x}),f^{t}_{\ell}(\mathbf{x})\right)+\\[-8.00003pt]"`
- `"\mathcal{L}_{\text{POD-spatial}}(\mathbf{h}^{t-1}_{\ell},\mathbf{h}^{t}_{\ell})=\mathcal{L}_{\text{POD-width}}(\mathbf{h}^{t-1}_{\ell},\mathbf{h}^{t}_{\ell})+\mathcal{L}_{\text{POD-height}}(\mathbf{h}^{t-1}_{\ell},\mathbf{h}^{t}_{\ell})\,."`
- "The final loss for current model g^{t}\circ f^{t} , i.e., the model trained for task t , is simply their addition \mathcal{L}_{\{f^{t};g^{t}\}}=\mathcal{L}_{\textrm{LSC}}+\mathcal{L}_{\textrm{POD-final}} ." LSC is a multi-proxy cosine classifier.

**(b) Ablations.** Setting: CIFAR100 with 50 steps of 1 class after a 50-class base, class-IL, 20 exemplars per class,
ResNet-32. The metric is average incremental accuracy.
- Caption: "Table 3: Ablation studies performed on CIFAR100 with 50 steps. We report the average incremental accuracy"
- Sub-table (a): "(a) Comparison of the performance of the model when disabling parts of the complete PODNet loss"

| classifier | POD-flat | POD-spatial | NME | CNN |
|---|---|---|---|---|
| Cosine | | | 40.76 | 37.93 |
| Cosine | ✓ | | 48.03 | 46.73 |
| Cosine | | ✓ | 54.32 | 57.27 |
| Cosine | ✓ | ✓ | 56.69 | 55.72 |
| LSC-CE | ✓ | ✓ | 59.86 | 57.45 |
| LSC | | | 41.56 | 40.76 |
| LSC | ✓ | | 53.29 | 52.98 |
| LSC | | ✓ | 61.42 | 57.64 |
| LSC | ✓ | ✓ | 61.40 | 57.98 |

- Sub-table (b): "(b) Comparison of distillation losses based on intermediary features. All losses evaluated with POD-flat". NME / CNN:
  - None 53.29 / 52.98
  - POD-pixels 49.74 / 52.34
  - POD-channels 57.21 / 54.64
  - POD-gap 58.80 / 55.95
  - POD-width 60.92 / 57.51
  - POD-height 60.64 / 57.50
  - POD-spatial 61.40 / 57.98
  - GradCam 54.13 / 52.48
  - Perceptual Style 51.01 / 52.25
- "When POD-spatial is added on top of POD-flat, we manage to increase the oldest classes performance (+7 percentage points) while the newest classes performance were barely reduced (-0.2 p.p.)."
- Tables 4 and 5 vary memory per class and the initial task size, and Table 6 (supplementary) evaluates the spatial losses
  without POD-flat. These were not transcribed.

**(c) CIFAR-100 headline.** Caption: "Table 1: Average incremental accuracy for PODNet vs. state of the art. We run experiments three times (random class orders) on CIFAR100 and report averages  \pm  standard deviations." Setting: class-IL with a 50-class base, 20 exemplars per old class, 3 class orders.

| method | 50 steps (1 class) | 25 (2) | 10 (5) | 5 (10) |
|---|---|---|---|---|
| iCaRL | 44.20 ± 0.98 | 50.60 ± 1.06 | 53.78 ± 1.16 | 58.08 ± 0.59 |
| BiC | 47.09 ± 1.48 | 48.96 ± 1.03 | 53.21 ± 1.01 | 56.86 ± 0.46 |
| UCIR (NME) | 48.57 ± 0.37 | 56.82 ± 0.19 | 60.83 ± 0.70 | 63.63 ± 0.87 |
| UCIR (CNN) | 49.30 ± 0.32 | 57.57 ± 0.23 | 61.22 ± 0.69 | 64.01 ± 0.91 |
| PODNet (NME) | 61.40 ± 0.68 | 62.71 ± 1.26 | 64.03 ± 1.30 | 64.48 ± 1.32 |
| PODNet (CNN) | 57.98 ± 0.46 | 60.72 ± 1.36 | 63.19 ± 1.16 | 64.83 ± 0.98 |

The strongest baseline is UCIR (LUCIR) CNN. The rows marked with an asterisk, copied from Hou et al., are omitted:
iCaRL* is 52.57 / 57.17 at 10 / 5 steps, UCIR (NME)* 60.12 / 63.12, and UCIR (CNN)* 60.18 / 63.42.

**(d) Code.** The paper prints "Code is available at: github.com/arthurdouillard/incremental_learning.pytorch".
https://github.com/arthurdouillard/incremental_learning.pytorch returned HTTP 403 through the proxy. The GitHub API search
shows the repository exists.

---

## 9. CLS-ER (Arani, Sarfraz, Zonooz, arXiv 2201.12604v2)

**(a) Mechanism.**
- Working-model loss: `"\mathcal{L}=\mathcal{L}_{CE}(\sigma(f(X;\theta_{W})),Y)+\lambda\mathcal{L}_{MSE}(f(X_{m};\theta_{W}),Z)"`
- Semantic memories: "The semantic memories are updated by taking an exponential moving average of the working model’s weights (Tarvainen & Valpola, 2017) with decay parameters \alpha_{P} and \alpha_{S} ," with `"\theta_{i}=\alpha_{i}\theta_{i}+(1-\alpha_{i})\theta_{W},~~~~~i\in\{P,S\}"`. Also "we stochastically update the plastic and stable models with rates r_{P} and r_{S} (note that r_{P}>r_{S} so that the plastic model is updated more frequently)."
- Replay-target selection: "For each exemplar, we select the replay logits Z based on which model has the highest softmax score for the ground-truth class (lines 5-6 in Algorithm 1)."

**(b) Ablations.** Setting: Mammoth protocol, i.e. S-CIFAR-10 with 5 tasks, ResNet-18 and 50 epochs (offline), reservoir
buffer, 10 runs.
- Appendix D, single against dual semantic memory. Caption: "Table S2: Comparison of CLS-ER with Mean-ER (single semantic memory) on Class-IL and Domain-IL settings. We report the mean and 1 std of 10 runs with different initializations."

| buffer | method | S-CIFAR-10 Class-IL | S-Tiny-ImageNet Class-IL |
|---|---|---|---|
| 200 | Mean-ER | 61.88 ± 2.43 | 17.68 ± 1.65 |
| 200 | CLS-ER | 66.19 ± 0.75 | 23.47 ± 0.80 |
| 500 | Mean-ER | 70.40 ± 1.21 | 24.97 ± 0.80 |
| 500 | CLS-ER | 75.22 ± 0.71 | 31.03 ± 0.56 |
| 5120 | Mean-ER | 84.84 ± 2.0 | 45.69 ± 0.58 |
| 5120 | CLS-ER | 86.78 ± 0.17 | 46.74 ± 0.31 |

- Appendix C.1: "Table S1: CLS-ER components performance analysis for each of the experimental setting." This is inference
  from each model of one trained CLS-ER run. S-CIFAR-10 Class-IL, stable / working / plastic:
  - buffer 200: 66.19 ± 0.75 / 50.09 ± 1.48 / 62.68 ± 1.94
  - buffer 500: 75.22 ± 0.71 / 63.09 ± 1.12 / 71.32 ± 0.89
  - buffer 5120: 86.78 ± 0.17 / 85.00 ± 0.33 / 86.77 ± 0.17
- Table S3 varies λ, r_S and r_P (S-CIFAR-10, buffer 500, 3 runs). It was not transcribed: "Table S3: The effect of different hyperparameter settings on the individual components of CLS-ER trained on S-CIFAR-10 with 500 buffer size."
- The paper has no row that switches off the consistency loss (λ = 0) or the stochastic update.

**(c) CIFAR headline.**
- CIFAR-10. Caption: "Table 1: Comparison with prior works on Class-IL and Domain-IL settings. The baseline results are from Buzzega et al. (2020a) (- indicates the experiments that the authors were unable to run)."
  S-CIFAR-10 Class-IL:
  - CLS-ER: 66.19 ± 0.75 (200), 75.22 ± 0.71 (500), 86.78 ± 0.17 (5120)
  - DER++ (strongest baseline): 64.88 ± 1.17, 72.70 ± 1.36, 85.24 ± 0.49
  - ER: 44.79 ± 1.86, 57.74 ± 0.27, 82.47 ± 0.52
- CIFAR-100 (the general-CL GCIL-CIFAR-100 protocol, recurring classes, 100 epochs). Caption: "Table 3: Comparison with prior works on GCIL-CIFAR-100 dataset."

  | method | Uniform 200 | 500 | 1000 | Longtail 200 | 500 | 1000 |
  |---|---|---|---|---|---|---|
  | ER | 16.40 ± 0.37 | 28.21 ± 0.69 | 31.98 ± 0.72 | 19.27 ± 0.77 | 20.30 ± 0.63 | 34.13 ± 0.83 |
  | DER++ | 18.84 ± 0.60 | 32.92 ± 0.74 | 38.95 ± 0.56 | 26.94 ± 1.27 | 25.82 ± 0.83 | 33.64 ± 0.88 |
  | CLS-ER | 25.06 ± 0.81 | 36.34 ± 0.59 | 39.69 ± 0.66 | 28.54 ± 0.87 | 28.63 ± 0.68 | 39.52 ± 0.91 |

  JOINT is 58.36 ± 1.02 (Uniform) and 56.94 ± 1.56 (Longtail).

**(d) Code.** The paper prints "The code is avaiable at: https://github.com/NeurAI-Lab/CLS-ER". The link returned HTTP 403
through the proxy. The GitHub API search shows the repository exists.

---

## 10. SS-IL (Ahn et al., arXiv 2003.13947v3)

**(a) Mechanism.**
- `"\displaystyle\mathcal{L}_{\text{SS-IL},t}((\bm{x},y),\bm{\theta})=\mathcal{L}_{\text{CE-SS},t}((\bm{x},y),\bm{\theta})+\mathcal{L}_{\text{TKD},t}(\bm{x},\bm{\theta}),\vskip-21.68121pt"`
- Separated softmax: "Namely, depending on whether (\bm{x},y)\in\mathcal{M} or (\bm{x},y)\in\mathcal{D}_{t} , the softmax probability is computed separately by only using the output scores for \mathcal{P}_{t} or \mathcal{N}_{t} , respectively, and the cross-entropy loss is computed separately as well."
- Task-wise KD: `"\displaystyle\mathcal{L}_{\text{TKD},t}(\bm{x},\bm{\theta})\triangleq\sum_{s=1}^{t-1}\mathcal{D}_{KL}(\bm{p}_{s}^{\tau}(\bm{x},\bm{\theta}_{t-1})\|\bm{p}_{s}^{\tau}(\bm{x},\bm{\theta})),\vskip-14.45377pt"`

**(b) Ablations.** Section 6.3. Setting: ImageNet-1K, class-IL, T = 10, |M| = 10k. **The results are figures only
(Figs. 6–8), with no numbers in the text.**
- The variants are defined as follows: "In these figures, “ \mathcal{L}_{\text{CE}} ” stands for the model that does not have both TKD and SS layer, “ \mathcal{L}_{\text{CE}}+\mathcal{L}_{\text{TKD}} ” stands for the model that does not have SS layer, “ \mathcal{L}_{\text{CE-SS}} ”, stands for the model that only has SS, and “ \mathcal{L}_{\text{CE-SS}}+\mathcal{L}_{\text{TKD}} ” stands for our SS-IL."
- "Figure 6(d) shows the Top-5 accuracy of the four models. In this figure, as we expected, “ \mathcal{L}_{\text{CE-SS}}+\mathcal{L}_{\text{TKD}} ” achieves the highest accuracy, and the models equipped with \mathcal{L}_{\text{TKD}} outperform the models trained without it."
- TKD against GKD (Fig. 8): "As shown in Figure 8, TKD achieves much higher accuracy than GKD, while the accuracy of GKD drastically declines as the task proceeds."

**(c) CIFAR headline.** Not reported. The paper has no CIFAR-10 or CIFAR-100 experiment (0 mentions in either the HTML or
the PDF text). Its own headline benchmark, from Table 1, is below. Caption: "Table 1: The results on various datasets and evaluation scenarios. The evaluation metrics are Average Top-1 and Top-5 accuracy. Accuracy is averaged over all the incremental tasks (i.e. including both initial task and incremental tasks)"

Average Top-1 on ImageNet-1K, T = 10, at |M| = 5k / 10k / 20k:

| method | 5k | 10k | 20k |
|---|---|---|---|
| SS-IL | 63.5 | 64.5 | 65.2 |
| EEIL | 57.8 | 59.4 | 60.9 |
| PODNet | 52.2 | 57.5 | 60.4 |
| BiC | 51.3 | 56.4 | 60.5 |
| LUCIR | 51.0 | 53.6 | 56.5 |
| iCaRL | 47.0 | 50.5 | 53.1 |

The strongest baseline at 5k and 10k is EEIL.

**(d) Code.** The paper prints no code link.

---

## 11. Co2L (Cha, Lee, Shin, arXiv 2106.14413v1)

**(a) Mechanism.**
- `"\displaystyle\mathcal{L}=\underbrace{\mathcal{L}^{\text{sup}}_{\text{asym}}}_{\text{(1) learning}}+\underbrace{\vphantom{\mathcal{L}^{\text{sup}}_{\text{asym}}}\lambda\cdot\mathcal{L}^{\text{IRD}}}_{\text{(2) preserving}}."`
- "In the modified version, we only use current task samples as anchors; past task samples from the memory buffer will only be used as negative samples (see Figure 2(a))."
- IRD: `"\displaystyle=\sum_{i=1}^{2N}-\mathbf{p}\left(\tilde{\mathbf{x}}_{i};\psi^{\text{past}},\kappa^{\ast}\right)\cdot\log\mathbf{p}\left(\tilde{\mathbf{x}}_{i};\psi,\kappa\right),"`
  and "the past representation is a snapshot of the model at the end of the previous task." The classifier is a linear
  head trained afterwards on the frozen representation: "we train a classifier using only the last task samples and buffered samples on top of the frozen representations learned by Co2L."

**(b) Ablations.** Setting: Seq-CIFAR-10, class-IL, ResNet-18, 10 trials.
- Caption: "Table 2: Ablation study of Instance-wise Relation Distillation (IRD). We train our model on Seq-CIFAR-10 dataset under class-IL scenario (identical to the setup in Section 5.2) with ablated Co2L. IRD brings significant gain with or without replay buffer. All results are averaged over ten independent trials."

  | variant | buffer | IRD | accuracy (%) |
  |---|---|---|---|
  | (a) w/o buffer and IRD | 0 | ✗ | 53.25 ± 1.70 |
  | (b) w/ IRD only | 0 | ✓ | 58.89 ± 2.61 |
  | (c) w/ buffer only | 200 | ✗ | 53.57 ± 1.03 |
  | (d) Co2L (ours) | 200 | ✓ | 65.57 ± 1.37 |

- The 200 auxiliary samples: "for (a,b), we use 200 auxiliary buffered samples to train the classifier (as in (c) and Co2L)."
- Caption: "Table 3: The effectiveness of asymmetric SupCon loss ( \mathcal{L}^{\text{sup}}_{\text{asym}} ) versus the original SupCon loss ( \mathcal{L}^{\text{sup}} ), combining with the IRD loss. All results are averaged over ten independent trials."

  | loss | Seq-CIFAR-10, buffer 200 | Seq-CIFAR-10, buffer 500 | Seq-Tiny-ImageNet, buffer 200 | Seq-Tiny-ImageNet, buffer 500 |
  |---|---|---|---|---|
  | L^sup | 60.49 ± 0.72 | 68.66 ± 0.68 | 13.51 ± 0.48 | 19.68 ± 0.62 |
  | L^sup_asym | 65.57 ± 1.37 | 74.26 ± 0.77 | 13.88 ± 0.40 | 20.12 ± 0.42 |

- Fig. 4 (IRD power in an infinite-buffer scenario) is a plot, with no numbers in the text.

**(c) CIFAR headline.** The paper has no CIFAR-100 experiment. CIFAR-10 caption: "Table 1: Classification accuracies for Seq-CIFAR-10, Seq-Tiny-ImageNet and R-MNIST on rehearsal-based baselines and our algorithm. We report performance of baslines of Seq-CIFAR-10 and Seq-Tiny-ImageNet from [5]." The baselines are copied from DER.

Seq-CIFAR-10, Class-IL / Task-IL:

| method | buffer 200 | buffer 500 |
|---|---|---|
| Co2L | 65.57 ± 1.37 / 93.43 ± 0.78 | 74.26 ± 0.77 / 95.90 ± 0.26 |
| DER++ | 64.88 ± 1.17 / 91.92 ± 0.60 | 72.70 ± 1.36 / 93.88 ± 0.50 |
| DER | 61.93 ± 1.79 / 91.40 ± 0.92 | 70.51 ± 1.67 / 93.40 ± 0.39 |

The strongest baseline is DER++.

**(d) Code.** The paper prints no code link.

---

## 12. Model and weight averaging in CL

### 12a. CoMA / CoFiMA (Marouf et al., arXiv 2312.08977v4)

**(a) Mechanism.**
- CoMA: `"\boldsymbol{\theta}^{*}_{t}=\lambda\boldsymbol{\theta}_{t}+(1-\lambda)\boldsymbol{\theta}^{*}_{t-1},"` and "Therefore, for each task t , we initiate finetuning from \boldsymbol{\theta}^{*}_{t-1} rather than the initial pre-trained model \boldsymbol{\theta}_{0} ."
- CoFiMA: `"\boldsymbol{\theta}_{t}^{*}=\frac{\lambda\mbox{\bf F}_{t}\boldsymbol{\theta}_{t}+(1-\lambda)\mbox{\bf F}_{t-1}\boldsymbol{\theta}^{*}_{t-1}}{\lambda\mbox{\bf F}_{t}+(1-\lambda)\mbox{\bf F}_{t-1}},"` which uses a diagonal Fisher: "this study adopts the diagonal of the Fisher information matrix for practicality [48, 62, 26]."
- "Note that, when \lambda=\frac{1}{t} , Eq. (3) is strictly equivalent to the average in Eq. (2) (see supplementary material), aligning with the maximum-likelihood solution and adhering to our initial hypothesis of isotropic Gaussian posteriors."

**(b) Ablations.** Setting: ViT-B/16 pre-trained on ImageNet-21K, class-IL, 10 tasks, SLCA training recipe, memory-free.
The metrics are Last-Acc and Inc-Acc.
- Caption: "Table 3: Experimental results comparing our methods (CoMA, and CoFiMA) to weight-averaging baselines using ViT-B/16 [27] supervised PTM." The EMA baseline is defined in the text: "Exponential Moving Average (EMA) [67], a technique for a running average of model parameters computed at every gradient descent iteration m as follows: \boldsymbol{\theta}_{m}\!=\!\beta\boldsymbol{\theta}_{m}+(1-\beta)\boldsymbol{\theta}_{m\!-\!1} with \beta=0.999 ."

  CIFAR-100 columns:

  | variant | init | λ | Last-Acc | Inc-Acc |
  |---|---|---|---|---|
  | Seq FT | – | – | 88.86 ± 0.83 | 92.01 ± 1.71 |
  | SLCA | – | – | 91.53 ± 0.28 | 94.09 ± 0.87 |
  | Weight-Ens. | θ0 | 1/t | 61.68 ± 0.14 | 70.24 ± 0.46 |
  | Weight-Ens. | θ*_{t−1} | 1/t | 91.69 ± 0.23 | 94.52 ± 0.95 |
  | EMA | – | – | 91.40 ± 0.12 | 93.89 ± 0.59 |
  | CoMA | θ*_{t−1} | λ | 92.00 ± 0.13 | 94.12 ± 0.63 |
  | CoFiMA | θ*_{t−1} | λF_t | 92.77 ± 0.24 | 94.89 ± 0.94 |

  Cars-196 Last-Acc for the same rows: Weight-Ens. (θ*_{t−1}) 71.82, EMA 65.41, CoMA 73.35, CoFiMA 76.96, SLCA 67.73.
- λ sweep on CIFAR-100 (Fig. 4, plot only): "The best performance is achieved with \lambda\!=\!0.3 , giving the best trade-off between learning new task t (i.e., plasticity) and preserving knowledge from previous tasks (i.e., stability)."
- From-scratch control (Table 4, Last-Acc on CIFAR100): ResNet18 CoFiMA 37.24 ± 0.11 from scratch against 68.31 ± 0.08
  pre-trained (Joint 69.05 / 76.12); ViT-Tiny CoFiMA 46.17 ± 0.17 from scratch against 65.90 ± 0.23 pre-trained. The paper
  comments: "We observe that CoFiMA’s performance is low when we leverage models trained from scratch."

**(c) CIFAR-100 headline.** Caption: "Table 1: State-of-the-art comparison on CUB-200, Cars-196, CIFAR-100, and ImageNet-R using ViT-B/16 [27] supervisedly pre-trained on ImageNet-21K [55]." CIFAR-100 Last-Acc / Inc-Acc:
- CoFiMA 92.77 ± 0.24 / 94.89 ± 0.94
- CoMA 92.00 ± 0.13 / 94.12 ± 0.63
- SLCA (strongest baseline) 91.53 ± 0.28 / 94.09 ± 0.87
- RanPAC 90.09 ± 0.25 / 93.31 ± 0.98
- BiC 88.45 ± 0.57 / 93.37 ± 0.32
- DER++ 84.50 ± 1.67 / 91.49 ± 0.61
- Joint-Training 93.22 ± 0.16

These are pre-trained-backbone numbers and are not comparable with the from-scratch ResNet results in §1–§11.

**(d) Code.** The paper prints "Code is available at: https://github.com/IemProg/CoFiMA." The link returned HTTP 403
through the proxy. The GitHub API search shows the repository exists.

### 12b. Mean Teacher / EMA (Tarvainen & Valpola, arXiv 1703.01780v6), the EMA source CLS-ER cites

**(a) Mechanism.**
- "After the weights of the student model have been updated with gradient descent, the teacher model weights are updated as an exponential moving average of the student weights."
- `"\displaystyle\theta^{\prime}_{t}=\alpha\theta^{\prime}_{t-1}+(1-\alpha)\theta_{t}"` and "where \alpha is a smoothing coefficient hyperparameter."
- "Note also that in the evaluation runs we used EMA decay \alpha=0.99 during the ramp-up phase, and \alpha=0.999 for the rest of the training."

**(b) Ablations.** Section 3.4. Setting: semi-supervised SVHN with 250 labels, not continual learning. **The results are
figures only (Fig. 4), with no numbers in the text.**
- Removal of noise: "We can see that either input augmentation or dropout is necessary for passable performance."
- EMA decay and consistency weight: "We can see that in each case the good values span roughly an order of magnitude and outside these ranges the performance degrades quickly." and "Note that EMA decay \alpha=0 makes the model a variation of the \Pi model, although somewhat inefficient one because the gradients are propagated through only the student path."
- Decoupling the heads, and MSE against KL: "in this setting MSE performs better than the other cost functions."

**(c) CIFAR headline.** The paper has no CIFAR-100 experiment. For CIFAR-10 (semi-supervised; error rate %, lower is
better) the caption is "Table 2: Error rate percentage on CIFAR-10 over 10 runs (4 runs when using all labels)."

| method | 1000 labels | 2000 | 4000 | all labels |
|---|---|---|---|---|
| Mean Teacher | 21.55 ± 1.48 | 15.73 ± 0.31 | 12.31 ± 0.28 | 5.94 ± 0.15 |
| Π model (their replication) | 27.36 ± 1.20 | 18.02 ± 0.60 | 13.20 ± 0.27 | 6.06 ± 0.11 |
| Supervised-only | 46.43 ± 1.21 | 33.94 ± 0.73 | 20.66 ± 0.57 | 5.82 ± 0.15 |

Also in the same table: VAT+EntMin is 10.55 at 4000 labels, and Temporal Ensembling is 12.16 ± 0.31 at 4000 labels.

**(d) Code.** The paper prints "Source code for the experiments is available at https://github.com/CuriousAI/mean-teacher."
The link returned HTTP 403 through the proxy. The GitHub API search shows the repository exists.

---

## Fetch failures and access notes

- The arXiv export API (`export.arxiv.org/api/query`) returned HTTP 406 over HTTPS and 301 over HTTP. The title searches
  therefore used `arxiv.org/search` (HTTP 200).
- github.com returned HTTP 403 through the proxy for all eight code links tried (the six printed in the papers, the iCaRL
  URL in both spellings, and Continvvm/continuum). The six paper repositories were confirmed to exist through the GitHub
  connector's repository search on 2026-09-25.
- LUCIR has no arXiv version found by title search, so the CVF open-access PDF (HTTP 200) was read.
- No 404 from arXiv or CVF.
- Tools: `pdftotext` is not installed, so the PDFs were extracted with pypdfium2 5.13.0 from the project virtual
  environment.

## Quote check

Script: `quote_check.py` in the scratchpad folder `lit0925/clsota/distill/`, run 2026-09-25. It collects every string
between straight double quotes, line by line, from all sections above this one. Both the file and the fetched texts are
normalised the same way:
- html-unescaped;
- U+FFFE (the PDF line-break hyphen in the CVF text) removed together with any whitespace after it;
- no-break spaces turned into spaces;
- runs of whitespace collapsed to one space.

Each quote is then searched as a substring of the concatenated `.txt` extractions: the arXiv HTML and PDF texts, the abs
pages and the LUCIR CVF PDF.

- Quoted strings of 20 characters or more: **131**. Found verbatim: **131**. Not found: **0**.
- One quote failed on the first run and was corrected to the source spelling: LUCIR `knowledges`, which the transcription
  had written as `knowledge`. An earlier version of the checker paired quotes across lines. After that fix, four short
  quoted words that were search terms or labels of mine, not quotes, were taken out of quotation marks.
- Quoted strings under 20 characters: 3 ("TABLE II", "Table 7", "future past"). All three were checked with the same
  normalisation and are verbatim in the LwF and X-DER texts. In the LwF HTML, "Table 7" is written with a no-break space.
