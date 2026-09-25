# State-of-the-art CL methods, replay and online family: mechanisms and ablations, read on the day (R10), 2026-09-25

**Status.** Owner request: prompt-log entry 191. This file is the source record for `CL Design Principle/`. It is a reading
record, not a result: no number here is a ledger row, and none may be quoted outside the ledger (R8). Every string in straight
double quotes is copied from the text fetched on 2026-09-25. LaTeX is kept as the arXiv HTML alt-text gives it. Everything
outside quotes (settings, which row is the strongest baseline, notes) is the reader's own wording.

**Access (2026-09-25).**
- Fetched with `curl` through the session proxy. The raw files and text extractions are in the session scratchpad under
  `lit0925/clsota/replay/`: `abs_<id>.html` + `.txt`, `html_<id>vN.html` + `.txt` + `.tables.txt`, `pdf_<id>vN.pdf` + `.txt`,
  `pdf_gdumb_eccv2020{,_supp}.pdf` + `.txt`, `pdf_ocm_guo22g.pdf` + `.txt`, `code_link_status.txt`.
- For all twelve arXiv works, arXiv served an HTML full text (arxiv.org/html/<id>vN, LaTeXML build) for the current version.
  The PDF of the same version was also fetched. PDF text was extracted with pypdfium2 5.13.0 from the repository's `.venv`,
  because `pdftotext` is not installed on this machine. Table rows below are quoted from the HTML table extraction
  (`*.tables.txt`: one row per line, cells joined by ` | `), except where a section says the PDF text was used.
- The arXiv API (`export.arxiv.org/api/query?search_query=ti:...`) returned **HTTP 406** to every query. Titles were therefore
  checked on the abs pages (`citation_title` meta tag), and missing ids were searched with `arxiv.org/search/?searchtype=title`.
- **GDumb** and **OCM** are not on arXiv. The arXiv title searches for both returned "Sorry, your query for" (followed by the query) with no hits. Both
  were read from the official proceedings: ECVA for GDumb, including the supplementary PDF, and PMLR v162 for OCM.
- **Code links:** every `github.com` URL, and also `api.github.com`, returned **HTTP 403** through the proxy (see
  `code_link_status.txt`). This is an egress block, not a 404. Whether each repository exists was then checked through the
  session's GitHub connector (repository search). The result is given per work under (d).
- No page returned 404.

| work | version and date | URL | read |
|---|---|---|---|
| 1. Chaudhry et al., *On Tiny Episodic Memories in Continual Learning* (ER) | arXiv 1902.10486 **v4**, 4 Jun 2019 (v1 27 Feb 2019) | https://arxiv.org/abs/1902.10486 ; https://arxiv.org/html/1902.10486v4 | [F] |
| 2. Aljundi et al., *Online Continual Learning with Maximally Interfered Retrieval* (MIR) | arXiv 1908.04742 **v3**, 29 Oct 2019 (v1 11 Aug 2019) | https://arxiv.org/abs/1908.04742 ; https://arxiv.org/html/1908.04742v3 | [F] |
| 3. Aljundi et al., *Gradient based sample selection for online continual learning* (GSS) | arXiv 1903.08671 **v5**, 31 Oct 2019 (v1 20 Mar 2019) | https://arxiv.org/abs/1903.08671 ; https://arxiv.org/html/1903.08671v5 | [F] |
| 4. Prabhu, Torr, Dokania, *GDumb: A Simple Approach that Questions Our Progress in Continual Learning* | ECCV 2020 (ECVA open access; DOI 10.1007/978-3-030-58536-5_31); no arXiv version found | https://www.ecva.net/papers/eccv_2020/papers_ECCV/papers/123470511.pdf (+ `-supp.pdf`) | [F] |
| 5. Caccia et al., *New Insights on Reducing Abrupt Representation Change in Online Continual Learning* (ER-ACE) | arXiv 2104.05025 **v3**, 2 May 2022 (v1 11 Apr 2021); ICLR 2022 | https://arxiv.org/abs/2104.05025 ; https://arxiv.org/html/2104.05025v3 | [F] |
| 6. Mai et al., *Supervised Contrastive Replay: Revisiting the Nearest Class Mean Classifier in Online Class-Incremental Continual Learning* (SCR) | arXiv 2103.13885 **v3**, 15 Sep 2021 (v1 22 Mar 2021); CVPR 2021 workshop | https://arxiv.org/abs/2103.13885 ; https://arxiv.org/html/2103.13885v3 | [F] |
| 7. Shim et al., *Online Class-Incremental Continual Learning with Adversarial Shapley Value* (ASER); id 2009.00093 confirmed by title | arXiv 2009.00093 **v4**, 22 Mar 2021 (v1 31 Aug 2020); AAAI-21 | https://arxiv.org/abs/2009.00093 ; https://arxiv.org/html/2009.00093v4 | [F] |
| 8. Guo, Liu, Zhao, *Online Continual Learning through Mutual Information Maximization* (OCM) | ICML 2022, PMLR 162 (guo22g); no arXiv version found | https://proceedings.mlr.press/v162/guo22g.html ; https://proceedings.mlr.press/v162/guo22g/guo22g.pdf | [F] |
| 9. Wei et al., *Online Prototype Learning for Online Continual Learning* (OnPro); id 2308.00301 confirmed by title | arXiv 2308.00301 **v1**, 1 Aug 2023; ICCV 2023 | https://arxiv.org/abs/2308.00301 ; https://arxiv.org/html/2308.00301v1 | [F] |
| 10. Guo, Liu, Zhao, *Dealing with Cross-Task Class Discrimination in Online Continual Learning* (GSA) | arXiv **2305.14657 v1**, 24 May 2023 (found by title search); CVPR 2023 | https://arxiv.org/abs/2305.14657 ; https://arxiv.org/html/2305.14657v1 | [F] |
| 11. Wang et al., *Improving Plasticity in Online Continual Learning via Collaborative Learning* (CCL-DC) | arXiv **2312.00600 v2**, 31 Mar 2024 (v1 1 Dec 2023; found by title search); CVPR 2024 | https://arxiv.org/abs/2312.00600 ; https://arxiv.org/html/2312.00600v2 | [F] |
| 12. Buzzega et al., *Rethinking Experience Replay: a Bag of Tricks for Continual Learning* | arXiv 2010.05595 **v1**, 12 Oct 2020 (only version); ICPR 2020 | https://arxiv.org/abs/2010.05595 ; https://arxiv.org/html/2010.05595v1 | [F] |
| 13. Michel et al., *Rethinking Momentum Knowledge Distillation in Online Continual Learning* (MKD) | arXiv **2309.02870 v2**, 5 Jun 2024 (v1 6 Sep 2023; found by title search); ICML 2024 | https://arxiv.org/abs/2309.02870 ; https://arxiv.org/html/2309.02870v2 | [F] |
| 14. Mai et al., *Online Continual Learning in Image Classification: An Empirical Survey* | arXiv 2101.10423 **v4**, 4 Oct 2021 (v1 25 Jan 2021); Neurocomputing | https://arxiv.org/abs/2101.10423 ; https://arxiv.org/html/2101.10423v4 | [F] |

Every arXiv id given in the request matched the title on its abs page. The ids for GSA, CCL-DC and MKD were not in the request;
they were found by title search, and each one's abs-page title matches the requested title.

---

## 1. ER: Chaudhry et al. 2019, *On Tiny Episodic Memories in Continual Learning* (arXiv 1902.10486v4)

**(a) Mechanism**
- "Second, it doubles the size of the minibatch used to compute the gradient descent parameter update by stacking the actual minibatch of examples from the current task with a minibatch of examples taken at random from the memory, line 7."
- "In ER instead, since both mini-batches are used in the optimization step, the average of g and g_{ref} is used."
- Reservoir memory update: "If ‘ n ’ is the number of points observed so far and ‘mem_sz’ is the size of the reservoir (sampling buffer), this selection strategy samples each data point with a probability \frac{\mbox{mem\_sz}}{n} ."
- Setting: "The input integer task id is used to select a task specific classifier head, and the network is trained via cross-entropy loss." and "all baselines are optimized via stochastic gradient descent with a mini-batch size equal to 10." The protocol is a single pass: "each example from a task can only be seen once". This makes it online and task-incremental (multi-head).

**(b) Ablations.** The paper varies one mechanism: the memory-writing rule (reservoir, ring buffer, k-means, mean of features) at
several memory sizes. It also runs a two-task analysis in which training on the memory and training on the new task are each
removed.
- Split CIFAR (CIFAR-100 in 20 tasks, of which 3 are used for cross-validation), online, task-IL, memory 1/3/5/13 samples per
  class. Table 4 caption: "Table 4: Split CIFAR : Performance (average accuracy (left column) and forgetting (right column)) for different number of samples per class." Columns: accuracy at 1/3/5/13 per class, then forgetting at 1/3/5/13.
  - "er-ringbuffer | 56.2 (± 1.93) | 60.9 (± 1.44) | 62.6 (± 1.77) | 64.3 (± 1.84) | 0.13 (± 0.01) | 0.09 (± 0.01) | 0.08 (± 0.02) | 0.06 (± 0.01)"
  - "er-mof | 56.6 (± 2.09) | 59.9 (± 1.25) | 61.1 (± 1.62) | 62.7 (± 0.63) | 0.12 (± 0.01 ) | 0.10 (± 0.01) | 0.08 (± 0.01) | 0.07 (± 0.01)"
  - "er-k-means | 56.6 (± 1.40) | 60.1 (± 1.41) | 62.2 (± 1.20) | 65.2 (± 1.81) | 0.13 (± 0.01) | 0.09 (± 0.01) | 0.07 (± 0.01) | 0.04 (± 0.01)"
  - "er-reservoir | 53.1 (± 2.66) | 59.7 (± 3.87) | 65.5 (± 1.99) | 68.5 (± 0.65) | 0.19 (± 0.02) | 0.12 (± 0.03) | 0.09 (± 0.02) | 0.05 (± 0.01)"
  - The authors' reading: "For instance, on CIFAR, with one example per class in the memory, ER with reservoir sampling is 3.5% worse than ER K-Means, but ER K-Means, ER Ring Buffer and ER MoF are all within 0.5% from each other"
  - The same comparison is reported for Permuted MNIST (Table 3), miniImageNet (Table 5) and CUB (Table 6).
- Hybrid writing rule (reservoir, then ring buffer): shown only in a figure (Fig. 2, CIFAR, 85 slots). No table values are given.
- Two-task analysis, MNIST Rotations, 10 memory slots: "We then verified that only training on \mathcal{M}_{1} without \mathcal{D}_{2} , yields strong overfitting to the examples in the memory and poor generalization performance, with a mere average accuracy of 40\% on T_{1} from the initial 85\% which was obtained just after training on T_{1} ." The curves are in Fig. 3. Table 7 caption: "Table 7: MNIST Rotation Performance of task 1 after training on task 2." Rows (er-ringbuffer Train/Mem/Test, then a-gem Train/Mem/Test, at 10° and then 90°):
  - "1000 | 85.6 | 1 | 86.2 | 81.5 | 86.6 | 82.5 | 68.7 | 1 | 69.4 | 51.7 | 73.3 | 52.1"
  - "20000 | 91.4 | 1 | 91.6 | 91.4 | 1 | 91.5 | 32.7 | 1 | 33.4 | 31.6 | 1 | 33.0"

**(c) Headline, CIFAR-100.** "Split CIFAR (Zenke et al., 2017) consists of splitting the original CIFAR-100 dataset (Krizhevsky and Hinton, 2009) into 20 disjoint subsets,". Setting: online (single pass), task-IL (multi-head), reduced ResNet18. Table 4 (caption above):
- method, 13 per class: "er-reservoir | 53.1 (± 2.66) | 59.7 (± 3.87) | 65.5 (± 1.99) | 68.5 (± 0.65)" (accuracy cells only; the full row is quoted in (b))
- strongest baseline, a-gem: "a-gem | 54.9 (± 2.92) | 56.9 (± 3.45) | 59.9 (± 2.64) | 63.1 (± 1.24) | 0.14 (± 0.03) | 0.13 (± 0.03) | 0.10 (± 0.02) | 0.07 (± 0.01)"
- "mer | 49.7 (± 2.97) | 57.7 (± 2.59) | 60.6 (± 2.09) | 62.6 (± 1.48) | 0.19 (± 0.03) | 0.11 (± 0.01) | 0.09 (± 0.02) | 0.07 (± 0.01)"
- "finetune | 40.6 (± 3.83) | - | - | - | 0.27 (± 0.04) | - | - |" and "multi-task | 68.3 | -"
- Main-text Table 1 (forgetting, one example per class): caption "Table 1: Forgetting when using a tiny episodic memory of single example per class." The CIFAR column reads: finetune 0.27, ewc 0.27, a-gem 0.14, mer 0.19, er-ringbuffer (ours) 0.13. That table is not in LaTeXML table form in the HTML; the values were read from the HTML text.

**(d) Code.** Printed: "Code: https://github.com/facebookresearch/agem". HTTP 403 (proxy). The connector found
`facebookresearch/agem` (archived); it is the A-GEM TensorFlow repository.

---

## 2. MIR: Aljundi et al. 2019 (arXiv 1908.04742v3)

**(a) Mechanism**
- "we estimate the would-be parameters update from the incoming batch as \theta^{v}=\theta-\alpha\nabla\mathcal{L}(f_{\theta}(\bm{X}_{t}),\bm{Y}_{t}) , with learning rate \alpha . We can now search for the top- k values x\in\mathcal{M} using the criterion s_{MI\text{-}1}(x)=l(f_{\theta^{v}}(x),y)-l(f_{\theta}(x),y) , where l is the sample loss."
- "To encourage diversity we apply a simple strategy of performing an initial random sampling of the memory, selecting C samples where C>\mathcal{B} before applying the search criterion."
- Memory update: "which is updated by the use of reservoir sampling [3, 8] as the stream of samples arrives."

**(b) Ablations**
- Retrieval rule, MIR against random (ER), with the same buffer and compute otherwise. CIFAR-10 in 5 tasks, online, shared head
  (class-IL), memories per class M = 20/50/100, 15 runs. Table 2 caption: "Table 2: CIFAR-10 results. Memories per class M , we report (a) Accuracy, (b) Forgetting (lower is better). For larger sizes of memory ER-MIR has better accuracy and improved forgetting metric. Each approach is run 15 times."
  - accuracy: "ER | 27.5\pm 1.2 | 33.1\pm 1.7 | 41.3\pm 1.9" ; "ER-MIR | 29.8 \pm 1.1 | \bm{40.0\pm 1.1} | \bm{47.6\pm 1.1}"
  - forgetting, from the PDF text (rows in table order GEM, iCarl, fine-tuning, ER, ER-MIR): ER "50.5 ± 2.4 35.4 ± 2.0 23.3 ± 2.9" ; ER-MIR "50.2 ± 2.0 30.2 ± 2.3 17.4 ± 2.1"
- Number of iterations per incoming batch, from the PDF text. Table 3 caption: "Table 3: CIFAR-10 accuracy (↑) results for increased iterations and 100 memories per class." The columns are 1 and 5 iterations: "ER 41.3 ± 1.9 42.4 ± 1.1" ; "ER-MIR 47.6 ± 1.1 49.3 ± 0.1" ; "iid online 60.8 ± 1.0 62.0 ± 0.9".
- Longer sequence, MiniImagenet in 20 tasks, 100 memories per class, 3 updates per batch. Table 4 (PDF text), columns
  accuracy then forgetting: "ER 24.7 ± 0.7 23.5 ± 1.0" ; "ER-MIR 25.2±0.6 18.0±0.8".
- Generative-replay variant, component ablation, MNIST Split. Table 6 (PDF text): "GEN-MIR 83.0" ; "ablate MIR on generator 82.7" ; "ablate MIR on classifier 81.7" ; "ablate H(ypre) 78.3" ; "ablate diversity constraint 80.7" ; "GEN 80.0". The KL-term row is "ablate DKL(ypre k yˆ) 80.7". The authors: "It seems however that the minimization of the label entropy, i.e. H(y_{pre}) , which ensures that the previous classifier is confident about the retrieved sample’s class, is most important and is essential to outperform the baseline."
- Hybrid autoencoder variant (appendix C, CIFAR-10): the "- test AE" and "- train & test AE" ablations appear only as a figure (Fig. 5). No table values are given.
- The two scoring criteria (s_MI-1 and s_MI-2) and C were chosen on validation, and no table compares them: "For MIR we select by validation at M=50 , C=50 and the s_{MI\text{-}1} criterion."

**(c) Headline.** There is no CIFAR-100 experiment. CIFAR-10 (Table 2 above), online, class-IL (shared head). ER-MIR scores 29.8 / 40.0 / 47.6
at M = 20/50/100 per class. The strongest baseline at M = 50 and 100 is ER, at 33.1 / 41.3. At M = 20 it is "iCarl (5 iter) [ 31 ] | 28.6\pm 1.2 | 33.7\pm 1.6 | 32.4\pm 2.1". GEM scores "GEM [ 27 ] | 16.8\pm 1.1 | 17.1\pm 1.0 | 17.5\pm 1.6".

**(d) Code.** Printed: "We release an implementation of our method at https://github.com/optimass/Maximally_Interfered_Retrieval." HTTP 403
(proxy). The connector found the repository.

---

## 3. GSS: Aljundi et al. 2019 (arXiv 1903.08671v5)

**(a) Mechanism**
- Surrogate objective (Eq. 7): "\displaystyle\mathrm{minimize}_{\mathcal{M}}\>\sum_{i,j\in{\mathcal{M}}}\frac{\langle{g_{i},g_{j}}\rangle}{\|g_{i}\|\|g_{j}\|}" ; "This brings up a new interpretation of the surrogate, which is maximizing the diversity of samples in the replay buffer using the parameter gradient as the feature."
- Greedy variant: "The key idea is to maintain a score for each sample in the replay buffer. The score is computed by the maximal cosine similarity of the current sample with a fixed number of other random samples in the buffer."
- "Sample i is selected as a candidate to be replaced with probability P(i)=\mathcal{C}_{i}/\sum_{j}{\mathcal{C}_{j}} . The replacement is a bernoulli event that happens with probability \mathcal{C}_{i}/(c+\mathcal{C}_{i}) where \mathcal{C}_{i} is the score of the candidate and c is the score of the new data."

**(b) Ablations.** These are buffer-selection variants: Rand, GSS-IQP, GSS-Clust, FSS-Clust, GSS-Greedy, and reservoir. The
setting is online, shared head, with no task boundaries used: "we use a fixed batch size of 10 samples and perform few iterations over a batch (1-5)".
- Disjoint MNIST (Table 1), "Table 1: Average test accuracy of sample selection methods on disjoint MNIST with different buffer sizes." Buffers 300/400/500: "Rand | 37.5\pm 1.3 | 45.9 \pm 4.8 | 57.9 \pm 4.1" ; "GSS-IQP(ours) | 75.9\pm 2.5 | 82.1 \pm 0.6 | 84.1 \pm 2.4" ; "GSS-Clust | 75.7\pm 2.2 | 81.4 \pm 4.4 | 83.9 \pm 1.6" ; "FSS-Clust | 75.8\pm 1.7 | 80.6 \pm 2.7 | 83.4 \pm 2.6" ; "GSS-Greedy(ours) | 82.6 \pm 2.9 | 84.6 \pm 0.9 | 84.8 \pm 1.8"
- Permuted MNIST (Table 2), buffer 300, average column: Rand "72.54 \pm 0.4", GSS-IQP "77.3 \pm 0.5", GSS-Clust "79.74 \pm 0.2", FSS-Clust "77.8 \pm 0.3", GSS-Greedy "77.3 \pm 0.5".
- Disjoint CIFAR-10 (Table 3), "Table 3: Comparison of different selection strategies on disjoint CIFAR10 benchmark." Columns T1..T5, Avg. The buffer size is not in the caption; the text says "for disjoint CIFAR-10 we couldn’t get sensible performance for the studied methods with buffer size smaller than 1k."
  - "Rand | 0 \pm 0.0 | 0.49 \pm 0.4 | 5.68 \pm 4.4 | 52.18 \pm 0.8 | 84.96 \pm 4.4 | 28.6 \pm 1.2"
  - "GSS-Clust | 0.35 \pm 0.5 | 15.27 \pm 8.3 | 7.96 \pm 6.3 | 9.97 \pm 2.1 | 77.83 \pm 0.7 | 22.5 \pm 0.4"
  - "FSS-Clust | 0.2 \pm 0.2 | 0.8 \pm 0.5 | 5.4 \pm 0.7 | 38.12 \pm 5.2 | 87.90 \pm 3.1 | 26.7 \pm 1.5"
  - "GSS-Greedy(ours) | 42.36 \pm 12.1 | 14.61 \pm 2.7 | 13.60 \pm 4.5 | 19.30 \pm 2.7 | 77.83 \pm 4. 2 | 33.56 \pm 1.7"
- Imbalanced streams against reservoir, disjoint MNIST, buffer 300 (Table 4): "Reservoir | 63.7 \pm 0.8 | 69.4 \pm 0.7 | 66.8 \pm 4.8 | 69.1 \pm 2.4 | 76.6 \pm 1.6 | 69.12 \pm 4.3" ; "GSS-IQP(ours) | 75.9 \pm 3.2 | 76.2 \pm 4.1 | 79.06 \pm 0.7 | 76.6 \pm 2.0 | 74.7 \pm 1.8 | 76.49 \pm 1.4" ; "GSS-Greedy(ours) | 71.2 \pm 3.6 | 78.5 \pm 2.7 | 81.5 \pm 2.3 | 79.5 \pm 0.6 | 79.1 \pm 0.7 | 77.96 \pm 3.5"
- Blurry task boundary, disjoint CIFAR-10 (Table 5), average column: Rand 29.0, GSS-IQP 29.6, GSS-Clust 25.0, FSS-Clust 26.0, GSS-Greedy 29.6 ("GSS-Greedy(ours) | 34.2 | 11.14 | 14.96 | 20.25 | 67.5 | 29.6").
- Constraint against rehearsal use of the same buffer ("a small subset of disjoint MNIST"), Tables 6 and 7: "GSS-IQP(Constrained) | 90.0 | 70.0 | 45.13 | 88.77 | 86.08 | 76.26" ; "GSS-IQP(Rehearsal) | 81.5 | 69.47 | 46.96 | 69.80 | 88.0 | 71.3" (buffer 100) ; "GSS-IQP(Constrained) | 95.0 | 83.0 | 68.7 | 87.6 | 82.4 | 83.4" ; "GSS-IQP(Rehearsal) | 94.6 | 83.89 | 50.6 | 77.0 | 88.67 | 78.9" (buffer 200).

**(c) Headline.** There is no CIFAR-100 experiment. On disjoint CIFAR-10, online and class-IL (Table 3 above), GSS-Greedy
averages 33.56, against Rand at 28.6, the best of the selection baselines. The comparison with GEM and iCaRL is shown only in a
figure: "Figure 4: Comparison with state-of-the-art task aware replay methods GEM. Figures show test accuracy."

**(d) Code.** Printed (footnote): "The code is available at https://github.com/rahafaljundi/Gradient-based-Sample-Selection". HTTP 403 (proxy). The
connector found the repository.

---

## 4. GDumb: Prabhu, Torr, Dokania, ECCV 2020 (ECVA PDF + supplementary)

**(a) Mechanism**
- "Given a memory budget, the sampler greedily stores samples from a data-stream while making sure that the classes are balanced, and, at inference, the learner (neural network) is trained from scratch (hence dumb) using all the samples stored in the memory."
- "It is greedy in the sense that whenever it encounters a new class, the sampler simply creates a new bucket for that class and starts removing samples from the old ones, in particular, from the one with a maximum number of samples."
- "GDumb uses cutmix [46] with p=0.5 and α=1.0 for regularization on all datasets except MNIST."

**(b) Ablations.** The main paper has no ablation that removes a component. The supplementary material has two tables.
- Supplementary Table 2, "Table 2. Accuracy of tweaked (NIN/DenseNet) GDumb models with number of passes." The caption continues: "accuracies in (brackets) are obtained without cutmix regularization." Header: "Passes/Form. B1-MNIST B1-SVHN A1-CIFAR10 D B2 C2". Memory k per column: "k 250 2000 500 1105 2000 9000". B2 is CIFAR-100 class-IL and D is CIFAR-100 task-IL. Rows, with values without cutmix in brackets:
  - "8 91.7 (96.0) 72.5 (81.4) 28.4 (28.4) 49.5 (50.8) 7.3 (8.8) 32.3 (33.9)"
  - "32 96.9 (97.2) 88.8 (87.3) 37.8 (36.7) 56.2 (58.3) 15.0 (18.1) 47.2 (48.4)"
  - "128 97.4 (97.2) 89.2 (88.9) 43.9 (42.9) 62.1 (61.9) 26.5 (24.1) 56.9 (56.3)"
  - "512 96.1 (97.7) 86.9 (88.4) 47.5 (45.9) 62.3 (61.5) 27.6 (25.8) 54.0 (54.7)"
  - The authors: "We also observe that cutmix regularization improves performance by 0.2% to 1.5% margins." The bolding that marks the selected pass count did not survive text extraction.
- Supplementary Table 1 varies the architecture and k (for example B2 CIFAR100-Class: "ResNet18 11.2M 2000 24.1" against "DenseNet100 800K 2000 27.5").

**(c) Headline, CIFAR-100** (main-paper tables, PDF text)
- B2, offline class-IL, CIFAR-100 in 20 tasks, k = 2000, columns Acc. (Avg) and Acc. (last). Table 5 caption: "Table 5. (CI-Offline-Disjoint) Performance on B1, B2, and B3." GDumb: "GDumb (Ours) 45.2 ± 1.70 24.1 ± 0.97". Strongest baseline: "BiC [16] 63.8 46.9" ; also "iCARL [4] 58.8 ± 1.90 42.9 ± 0.79".
- B3 (PODNet protocol), CIFAR100 column: "GDumb (CNN) 58.4 ± 0.8 62.86" against "PODNet (CNN) [21] 58.0 ± 0.5 62.08" and "PODNet (NME) [21] 61.4 ± 0.7 -".
- D, online task-IL, CIFAR-100, k = 1105, from Table 6 (right; its caption, as printed, begins "Table 6. (TI-Offline-Disjoint) Performance on C1 (left) and C2 (middle)."): "GDumb 60.3 ± 0.85" against "TinyER [34] 68.5 ± 0.65".
- Online class-IL CIFAR-10 (A1, MIR protocol), for comparison with MIR, k = 200/500/1000. Table 3, "Table 3. (CI-Online-Disjoint) Performance on formulation A1.": "GDumb (Ours) 35.0 ± 0.6 45.8 ± 0.9 61.3 ± 1.7" against "ER-MIR [11] 29.8 ± 1.1 40.0 ± 1.1 47.6 ± 1.1" and "ER-MIR5 [11] - - 49.3 ± 0.1".

**(d) Code.** Printed: "Our pytorch implementation is publicly available at: https://github.com/drimpossible/GDumb." HTTP 403 (proxy). The connector
found the repository.

---

## 5. ER-ACE: Caccia et al. 2022 (arXiv 2104.05025v3)

**(a) Mechanism**
- "\mathcal{L}_{ace}(\mathbf{X}^{bf}\cup\mathbf{X}^{in})=\mathcal{L}_{ce}(\mathbf{X}^{bf},~C_{old}\cup C_{curr})+\mathcal{L}_{ce}(\mathbf{X}^{in},C_{curr})"
- "where C_{curr} denotes the set of the classes represented in the incoming batch and C_{old} denotes previously seen classes that are not presented in the incoming batch, those that we want to preserve their representation. Note this is a straightforward procedure and induces no additional computational overhead."
- "We note that restricting the classes used in the denominator has an analogous effect to restricting the negatives in the contrastive loss."
- Buffer: "We keep buffer management constant across methods : all samples are kept or discarded according to Reservoir Sampling Vitter (1985)." Batch sizes: "leave the batch size and the rehearsal batch size fixed at 10."

**(b) Ablations**
- ER against ER-ACE: the same buffer, the same compute (17 TFLOPs each), and only the incoming-batch loss changed. Split CIFAR-10, online, single head, M = 5/20/100, 10 runs, AAA and final Acc, without and with augmentation. Table 1 caption: "Table 1: split CIFAR-10 results. {\dagger} indicates the method is leveraging a task identifier at training time. For methods whose compute depend on the buffer size, we report \min and \max values. We evaluate the models every 10 updates. Results within error margin of the best result are bolded."
  - "ER | ✗ | 40.0 \pm 0.8 | 19.7 \pm 0.3 | 45.2 \pm 1.3 | 26.7 \pm 1.0 | 55.4 \pm 1.4 | 38.7 \pm 0.8 | 17 | (4, 7)" ; with augmentation "✓ | 45.6 \pm 1.1 | 28.4 \pm 1.0 | 55.9 \pm 1.2 | 40.3 \pm 0.6 | 60.3 \pm 1.3 | 49.4 \pm 1.3"
  - "ER-ACE | ✗ | 53.1 \pm 1.0 | 35.6 \pm 1.0 | 58.0 \pm 0.7 | 42.6 \pm 0.7 | 61.9 \pm 0.9 | 52.2 \pm 0.7 | 17 | (4, 7)" ; with augmentation "(ours) | ✓ | 52.6 \pm 0.9 | 35.1 \pm 0.8 | 56.4 \pm 1.0 | 43.4 \pm 1.6 | 61.7 \pm 0.9 | 53.7 \pm 1.1"
  - The paper does not define M in the text read. The GDUMB row, "GDUMB | ✓ | 0 \pm 0.0 | 35.0 \pm 0.6 | 0 \pm 0.0 | 45.8 \pm 0.9 | 0 \pm 0.0 | 61.3 \pm 1.7", reproduces GDumb's own k = 200/500/1000 CIFAR-10 values (section 4).
- Negative selection in the metric-learning sibling ER-AML, CIFAR-10, M = 20/50. "Table 7: Ablation of ER-AML with all negative selection versus negatives selected from incoming classes. We use the CIFAR-10 dataset." Accuracy: "ER | 26.7\pm 0.3 | 36.1\pm 0.6" ; "ER-AML(all negatives) | 28.5\pm 0.3 | {41.4\pm 0.4}" ; "ER-AML(incoming negatives) | \bf 41.9\pm 0.1 | {\bf 48.3\pm 0.2}". Forgetting, in the same row order: "47.1\pm 0.8 | 37.6\pm 0.9", "56.7\pm 0.6 | 35.0\pm 0.4", "{\bf 33.6\pm 0.2} | {\bf 25.8\pm 0.3}".
- Triplet against SupCon (Table 6), CIFAR-10, M = 5/20/50/100: "ER | 19.0\pm 0.1 | 26.7\pm 0.3 | 36.1\pm 0.6 | 41.5\pm 0.6" ; "ER-AML Triplet | 33.0\pm 0.3 | 40.1\pm 0.4 | \ 46.0\pm 0.5 | {49.8\pm 0.5}" ; "ER-AML SupCon | 33.0\pm 0.2 | {\bf 41.9\pm 0.1} | {\bf 48.3\pm 0.2} | {\bf 51.9\pm 0.3}".
- Drift (Table 5, CIFAR-10, second task): "ER | (3.2\pm 1.8)\times 10^{-2}" ; "ER-AML-Triplet w. All Negs | (3.0\pm 0.6)\times 10^{-2}" ; "ER-AML-Triplet w. Incoming Negs | (2.5\pm 0.6)\times 10^{-2}".
- Blurry boundaries (Table 3, CIFAR-10): "ER | 32.1±1.5 | 42.7±2.2" ; "DER++ | 31.0±1.4 | 41.7±1.4" ; "ER-AML | 45.6 ±1.2 | 55.2 ±1.1" ; "ER-ACE | 44.5 ±0.5 | 50.2±1.1" (M = 20/100). Appendix J varies the blur level (CIFAR-10, M = 20, 1..5 unique classes per minibatch): "ER-ACE | 32.8 | 36.2 | 36.8 | 41.7 | 44.5" against "ER | 23.1 | 25.7 | 26.3 | 31.1 | 34.4".
- Limited data (Appendix K, CIFAR-10, M = 20, rehearsal batch raised to 20 to match DER++ compute): "ER-ACE | 20.5 | 25.4 | 31.2 | 36.1" against "ER | 17.3 | 22.5 | 28.0 | 33.2" and "DER++ | 17.4 | 19.9 | 24.8 | 32.8" (5/10/25/50 % of data).
- ER-ACE on top of DER++ (Appendix D, mammoth codebase) is shown only in a figure: "Figure 6: Comparison to Dark Experience Replay (DER). We obtain improved performance and we can enhance the DER method using the ER-ACE approach".

**(c) Headline, CIFAR-100.** "Split CIFAR-100 comprises 20 tasks, each containing a disjoint set of 5 labels." Setting: online, single head, M = 100. Table 2 caption: "Table 2: Split CIFAR-100 (left) and Mini-Imagenet (right) results with M=100 . For each method, we report the best result between using (or not) data augmentations." Columns AAA, Acc., Train TFLOPs, Mem. (Mb); rows as they appear in the HTML text:
- "ER-ACE (ours) 32.7 \pm 0.5 25.8 \pm 0.4 17 35"
- strongest baseline "SS-IL† 31.5 \pm 0.5 25.0 \pm 0.3 19 39" (SS-IL uses the task identifier during training)
- "ER 24.2 \pm 0.6 19.8 \pm 0.4 17 35" ; "DER++ 23.3 \pm 0.5 15.1 \pm 0.4 25 36" ; "MIR† 23.6 \pm 0.8 20.6 \pm 0.5 41 35" ; "iid++ - 28.3 \pm 0.3 17 4"

**(d) Code.** Printed: "Code to reproduce experiments is available at www.github.com/pclucas14/AML." The abs page links http://www.github.com/pclucas14/AML.
HTTP 403 after redirect to https://github.com/pclucas14/AML (proxy). The connector found `pclucas14/AML`; its default branch is
`paper_open_source`.

---

## 6. SCR: Mai et al. 2021 (arXiv 2103.13885v3)

**(a) Mechanism**
- "An input batch is created by concatenating B_{n} with another batch B_{\mathcal{M}} selected from the memory buffer \mathcal{M} . The input batch and its augmented view are encoded by a shared encoder network Enc(\cdot) and a projection network Proj(\cdot) before the representations are evaluated by the supervised contrastive loss \mathcal{L}_{\text{SCL}} ."
- "During the testing phase, Proj(\cdot) is discarded. All the buffered samples are fed into Enc(\cdot) to obtain the embeddings, which are used to compute the class means (prototypes) for the NCM classifier."
- "We use reservoir sampling [55] for memory update and random sampling for memory retrieval and use a memory batch size 100."

**(b) Ablations**
- The classifier swapped from Softmax to NCM on five replay methods. Online class-IL, CIFAR-100 in 10 tasks, M = 1k/2k/5k, 10 runs. Table 1 caption: "Table 1: Average Accuracy by the end of training. M is the memory buffer size and all numbers are the average of 10 runs. SCR considerably and consistently outperforms all the compared methods by large margins in different datasets and memory sizes." Column order: Mini-ImageNet ×3, CIFAR-100 ×3, CIFAR-10 ×3.
  - "ER | 10.3\pm 0.7 | 13.4\pm 0.7 | 16.4\pm 1.5 | 11.2\pm 0.6 | 14.6\pm 0.4 | 21.0\pm 0.9 | 22.4\pm 1.1 | 29.0\pm 2.5 | 37.7\pm 2.0"
  - "ER-NCM | 16.8\pm 0.8 | 19.7\pm 1.0 | 21.1\pm 0.8 | 16.8\pm 0.5 | 20.9\pm 0.6 | 28.3\pm 1.0 | 30.8\pm 2.0 | 40.8\pm 1.5 | 49.4\pm 0.9"
  - "MIR | 10.7\pm 0.7 | 14.7\pm 1.1 | 17.3\pm 1.6 | 11.7\pm 0.3 | 14.9\pm 0.5 | 21.6\pm 1.2 | 23.8\pm 0.9 | 33.6\pm 1.7 | 43.0\pm 1.6"
  - "MIR-NCM | 17.8\pm 0.5 | 20.5\pm 0.7 | 22.1\pm 0.9 | 16.4\pm 0.4 | 19.8\pm 0.6 | 27.9\pm 1.0 | 31.2\pm 1.5 | 40.9\pm 1.5 | 49.9\pm 1.0"
  - "GSS | 10.5\pm 0.6 | 13.5\pm 1.1 | 14.5\pm 2.2 | 10.6\pm 0.4 | 13.5\pm 0.4 | 18.0\pm 1.1 | 23.0\pm 0.9 | 28.5\pm 1.5 | 34.6\pm 2.3" ; "GSS-NCM | 15.2\pm 0.9 | 18.9\pm 0.7 | 20.9\pm 1.3 | 13.2\pm 0.7 | 18.1\pm 0.9 | 25.8\pm 0.7 | 28.5\pm 1.2 | 37.3\pm 1.6 | 46.6\pm 2.0"
  - "AGEM | 4.5\pm 0.4 | 4.6\pm 0.2 | 4.6\pm 0.2 | 5.8\pm 0.3 | 6.0\pm 0.3 | 5.9\pm 0.2 | 18.2\pm 0.3 | 18.3\pm 0.2 | 18.2\pm 0.2" ; "AGEM-NCM | 9.5\pm 0.3 | 10.6\pm 0.3 | 11.6\pm 0.5 | 11.5\pm 0.8 | 13.1\pm 0.8 | 14.3\pm 0.4 | 28.1\pm 1.8 | 29.0\pm 1.8 | 29.1\pm 0.9"
- SCR components (Section 4.4, CIFAR-100, M = 2k). These appear only as a figure: "Figure 8: Average accuracy of SCR with M=2k on CIFAR100 for ablation study." The text gives no table values:
  - memory batch size: "Nevertheless, in online CL, accuracy improvement is more obvious with the increase of B_{\mathcal{M}} when B_{\mathcal{M}} is smaller than 200. The performance drops when B_{\mathcal{M}} continues to increase."
  - memory management: "As we can see in Figure 8 (b), the random option is much better than GSS and slightly better than others."
  - temperature: "SCR with \tau ranging from 0.02 to 0.16 achieves stable results."
  - projection head: "we find that the choice of projection network is insignificant in online CL as shown in Figure 8 (d)."
- The paper has no ablation of SCR's contrastive loss against cross-entropy with NCM kept fixed, other than the X-NCM rows above.

**(c) Headline, CIFAR-100** ("Split CIFAR-100 splits the CIFAR-100 dataset [29] into 10 disjoint tasks, and each task has 10 classes."). Online class-IL, reduced ResNet18, batch 10, M = 1k/2k/5k (Table 1, caption above):
- "SCR | \mathbf{24.1\pm 0.6} | \mathbf{30.6\pm 0.5} | \mathbf{35.4\pm 0.5} | \mathbf{26.6\pm 0.5} | \mathbf{32.8\pm 0.7} | \mathbf{37.8\pm 0.3} | \mathbf{48.6\pm 1.1} | \mathbf{59.6\pm 1.2} | \mathbf{65.7\pm 0.6}"
- strongest baseline on CIFAR-100: "ASER μ -NCM | 16.6\pm 0.7 | 18.4\pm 0.5 | 21.1\pm 0.3 | 22.0\pm 0.6 | 25.2\pm 0.7 | 29.6\pm 0.4 | 34.1\pm 0.8 | 43.7\pm 0.8 | 50.3\pm 0.9"
- best Softmax baseline: "ASER μ | 12.5\pm 0.8 | 14.9\pm 0.5 | 18.2\pm 0.9 | 14.4\pm 0.6 | 17.5\pm 0.6 | 21.7\pm 1.0 | 28.5\pm 1.3 | 39.8\pm 1.7 | 46.7\pm 1.3"

**(d) Code.** The arXiv v3 PDF and HTML print no code link. OCM (section 8, Appendix) names a repository for it: "The code of ASER and SCR: https://github.com/RaptorMai/online-continual-learning." HTTP 403 (proxy). The connector found the repository; its description names ASER, SCR and the survey.

---

## 7. ASER: Shim et al. 2021 (arXiv 2009.00093v4; id confirmed by title)

**(a) Mechanism**
- Retrieval score (Eq. 5): "\displaystyle\textbf{ASV}(i)=\max_{j\in S_{\text{sub}}}s_{j}(i)-\min_{k\in B_{n}}s_{k}(i)," ; and the mean variant "\displaystyle\textbf{ASV}_{\mu}(i)=\frac{1}{|S_{\text{sub}}|}{\sum_{j\in S_{\text{sub}}}s_{j}(i)}-\frac{1}{b}{\sum_{k\in B_{n}}s_{k}(i)},"
- "Thus, we conjecture that a good data candidate i has high positive SV for memory \mathcal{M} and negative SV with large magnitude for the current input task B_{n} ."
- Update: "Then, we replace samples in \bar{\mathcal{M}} having smaller average KNN-SVs than samples in B_{n} with the input batch samples."

**(b) Ablations**
- Retrieval and update switched on and off separately. Online class-IL, CIFAR-100 in 10 tasks, M = 1k/2k/5k. Caption: "Table C.1: Ablation analysis. Average Accuracy (higher is better). Memory buffer size M." Variant definitions: "SV-upd: Use KNN-SV MemoryUpdate as described in Section 4 while randomly retrieving samples from the memory for replay." ; "ASV-ret: Use (5) scoring function for MemoryRetrieval while using reservoir sampling for MemoryUpdate." The CIFAR-100 sub-table rows carry no method labels in the extraction. They are in the order of the Mini-ImageNet sub-table (ER, SV-upd, ASV-ret, ASVμ-ret, ASER, ASERμ):
  - ER "11.2\pm 0.4 | 14.6\pm 0.4 | 20.1\pm 0.8"
  - SV-upd "\mathbf{14.0\pm 0.6} | \mathbf{17.2\pm 0.4} | 20.9\pm 0.6"
  - ASV-ret "10.1\pm 0.3 | 13.9\pm 0.3 | 20.3\pm 0.3"
  - ASVμ-ret "10.8\pm 0.3 | 14.8\pm 0.4 | \mathbf{21.7\pm 0.3}"
  - ASER "12.3\pm 0.4 | 14.7\pm 0.7 | 20.0\pm 0.6"
  - ASERμ "\mathbf{14.0\pm 0.4} | \mathbf{17.2\pm 0.5} | \mathbf{21.7\pm 0.5}"
  - The authors: "For the other two datasets, it turns out that SV-upd is a powerful MemoryUpdate method." and "In these two datasets, ASV(μ)-ret methods and ER perform comparably."
- Shapley value replaced by Euclidean distance (Dist, Distμ), Table A.1, CIFAR-100: Dist "10.3\pm.3 | 12.4\pm 0.5 | 16.7\pm 0.6" ; Distμ "10.5\pm 0.2 | 13.4\pm 0.4 | 17.2\pm 0.8".
- The trick of excluding current-task samples from retrieval (Table F.1), CIFAR-100: MIR "11.2\pm 0.3 | 14.1\pm 0.2 | 21.2\pm 0.6" ; MIR^t "11.2\pm 0.3 | 14.5\pm 0.3 | 21.9\pm 0.5" ; ASER^t "13.2\pm 0.5 | 16.1\pm 0.3 | 20.7\pm 0.5" ; ASERμ^t "13.8\pm 0.3 | \mathbf{17.3\pm 0.5} | 21.5\pm 0.7".

**(c) Headline, CIFAR-100** (10 tasks of 10 classes), online class-IL, M = 1k/2k/5k, 15 runs. Table 1 caption: "Table 1: Average Accuracy (higher is better), M is the memory buffer size. All numbers are the average of 15 runs. ASER μ has better performance when M is small and dataset is more complex." Column order: Mini-ImageNet ×3, CIFAR-100 ×3, CIFAR-10 ×3.
- "ASER μ | \mathbf{12.2\pm 0.8} | \mathbf{14.8\pm 1.1} | \mathbf{18.2\pm 1.1} | \mathbf{14.0\pm 0.4} | \mathbf{17.2\pm 0.5} | 21.7\pm 0.5 | 26.4\pm 1.5 | 36.3\pm 1.2 | 43.5\pm 1.4"
- strongest baseline on CIFAR-100: "MIR | 8.1\pm 0.3 | 11.2\pm 0.7 | 15.9\pm 1.6 | 11.2\pm 0.3 | 14.1\pm 0.2 | 21.2\pm 0.6 | 28.3\pm 1.6 | 35.6\pm 1.2 | 42.4\pm 1.5" ; also "ER | 8.7\pm 0.4 | 11.8\pm 0.9 | 16.5\pm 0.9 | 11.2\pm 0.4 | 14.6\pm 0.4 | 20.1\pm 0.8 | 26.4\pm 1.0 | 32.2\pm 1.4 | 38.4\pm 1.7"

**(d) Code.** The paper prints no URL: "The code to reproduce all results can be found in the attached zip file." OCM and the survey (section 14) point to https://github.com/RaptorMai/online-continual-learning. HTTP 403 (proxy). The connector found the repository.

---

## 8. OCM: Guo, Liu, Zhao, ICML 2022 (PMLR 162, guo22g; PDF text)

**(a) Mechanism**
- "Our final optimization goal is to optimize the sum of those three objectives, i.e., (1)+(2)+(3)."
- The three terms: "In Figure 1, maximizing (1) Lce(Xbuf) enables the model to learn a class-balanced classifier." ; "helps the model learn holistic or comprehensive feature representations for inputs." (term (2), the InfoNCE surrogate for I(X;F(X)) on X^new and X^buf separately) ; "When a new batch of data incrementally arrives, to protect the learned knowledge, the last term of the objective maximizes the MI between the current model and the frozen previous model using Xbuf." (term (3))
- Augmentation: "The combination of the global and local rotations give us 16 rotated images for each xi" ; "Our OCMfollows the memory retrieval/update strategy of ER as ER is a basic method." (the missing space is in the source)

**(b) Ablations** (CIFAR10 5 tasks; online class-IL; M = 1k; Adam; replay batch 64)
- Table 1 variants on all datasets: "OCM (no local rotation) 88.3±0.2 95.3±0.1 97.1±0.1 55.3±0.5 63.1±0.4 70.7±0.3 26.7±0.1 33.5±0.2 39.6±0.1 13.5±0.2 20.5±0.2 26.4±0.3" ; "OCM (no past) 89.5±0.1 95.0±0.1 96.0±0.1 56.2±0.4 63.2±0.2 73.1±0.2 27.0±0.4 34.0±0.1 41.0±0.3 15.0±0.4 21.0±0.3 26.0±0.2" ; full "OCM 90.7±0.1 95.7±0.3 96.7±0.1 59.4±0.2 70.0±1.3 77.2±0.5 28.1±0.3 35.0±0.4 42.4±0.5 15.7±0.2 21.2±0.4 27.0±0.3" (MNIST ×3, CIFAR10 ×3, CIFAR100 M = 1k/2k/5k, TinyImageNet ×3).
- Dropping term (2): "The results of OCM without maximizing the MI between X and fθ(X) are not listed as they are poor, e.g., 58.9% for CIFAR10, which indicates that the mechanism (i.e., (2) in Section 4.3) for learning holistic features is very important."
- Table 3, "Table 3. Ablation accuracy - average of 5 runs." Columns: Lce in all; Lce in all (no t); MI union; unsupervised InfoNCE; gray scale; horizontal flip; resized crop; λ = 1; λ = 0. Rows: "MNIST 94.8±0.1 96.1±0.1 95.8±0.1 93.6±0.1 - - 93.9±0.1 96.2±0.1 95.3±0.1" ; "CIFAR10 68.1±1.2 69.5±0.5 70.92±0.4 60.8±1.2 70.8±0.5 70.4±0.4 58.4±0.9 71.2±0.5 65.0±0.7". The authors: "Another interesting observation is that experiment “Lce to all (no t)” can be viewed as training the ER baseline by maximizing our MI objective."
- Rotation (Appendix 8, Table 6, M = 1k). Columns: different view, only local, no rotation, rotations as one class, duplicate. Rows: "MNIST 96.0±0.1 95.2±0.2 95.6±0.2 95.9±0.1 96.3±0.1" ; "CIFAR10 67.4±0.2 67.7±0.2 67.1±0.1 60.1±0.1 67.1±1.1".
- MI terms (1)+(2) added to other methods (Table 4). The values are averaged over all four datasets and memory sizes, with forgetting in brackets: "MIR MIR+MI ASER ASER+MI DER++ (DER++)+MI SCR SCR +MI OCM" / "37.5(36.3) 46.3(18.7) 32.1(51.4) 38.7(44.5) 39.01(41.1) 44.0(37.7) 48.6(18.6) 50.9(17.5) 54.9(12.9)".
- Number of pseudo classes: figure only (Fig. 2a).

**(c) Headline, CIFAR100** (10 tasks), online class-IL, M = 1k/2k/5k, full ResNet18, 15 runs. Caption: "Table 1. Accuracy on MNIST (5 tasks), CIFAR10 (5 tasks), CIFAR100 (10 tasks) and TinyImageNet (100 tasks) datasets with different memory buffer sizes M. All values are the averages of 15 runs". The OCM row is quoted above (CIFAR100 values 28.1, 35.0, 42.4). Strongest baseline: "SCR (Mai et al., 2021) 86.2±0.5 92.8±0.3 94.6±0.1 47.2±1.7 58.2±0.5 64.1±1.2 26.5±0.2 31.6±0.5 36.5±0.2 10.6±1.1 17.2±0.1 20.4±1.1". Also "GDumb (Prabhu et al., 2020) 81.2±0.5 91.0±0.2 94.5±0.1 35.9±1.1 50.7±0.7 63.5±0.5 14.1±0.3 20.1±0.2 36.0±0.5 12.6±0.1 12.7±0.3 15.7±0.2" and "ER (Chaudhry et al., 2020) 78.7±0.4 88.0±0.2 90.3±0.1 29.7±1.0 35.2±0.3 44.3±0.4 11.7±0.3 15.0±0.9 14.4±0.9 5.6±0.5 10.1±0.7 11.7±0.2".

**(d) Code.** Printed: "The code is publicly available at https://github.com/gydpku/OCM." HTTP 403 (proxy). The connector found the repository.

---

## 9. OnPro: Wei et al., ICCV 2023 (arXiv 2308.00301v1; id confirmed by title)

**(a) Mechanism**
- Online prototype: "At each time step of task t , the online prototype of each class is defined as the mean representation in a mini-batch:"
- "\displaystyle\mathcal{L}_{\mathrm{OPE}} |   \displaystyle=\mathcal{L}^{\mathrm{new}}_{\mathrm{pro}}(\mathcal{P},\widehat{\mathcal{P}})+\mathcal{L}^{\mathrm{seen}}_{\mathrm{pro}}(\mathcal{P}^{\mathrm{b}},\widehat{\mathcal{P}}^{\mathrm{b}}),"
- APF: "Specifically, APF adaptively selects more samples from easily misclassified classes in \mathcal{M} for mixup [55] according to the probability distribution P ." ; "First, we select n_{\mathrm{APF}} samples with P , and a larger P_{a,b} means more sampling from classes a and b . Here, n_{\mathrm{APF}}=\alpha\cdot m , and \alpha is the ratio of APF. Second, the remaining m-n_{\mathrm{APF}} samples are uniformly randomly selected from the entire memory bank"
- Total loss: "\displaystyle\mathcal{L}_{\mathrm{OnPro}}=\mathcal{L}_{\mathrm{OPE}}+\mathcal{L}_{\mathrm{INS}}+\mathcal{L}_{\mathrm{CE}},"

**(b) Ablations** (online class-IL)
- Table 3: "Table 3: Ablation studies on CIFAR-10 ( M=0.1k ) and CIFAR-100 ( M=0.5k ). “baseline” means \mathcal{L}_{\mathrm{INS}}+\mathcal{L}_{\mathrm{CE}} ." Accuracy with forgetting in brackets:
  - "baseline | 46.4 \pm 1.2(36.0 \pm 2.1) | 18.8 \pm 0.8(18.5 \pm 0.7)"
  - "w/o OPE | 53.1 \pm 1.4(24.7 \pm 2.0) | 19.3 \pm 0.7(15.9 \pm 0.9)"
  - "w/o APF | 52.0 \pm 1.5(34.6 \pm 2.4) | 21.5 \pm 0.5(16.3 \pm 0.8)"
  - "w/o \mathcal{L}^{\mathrm{new}}_{\mathrm{pro}} | 54.8 \pm 1.2( 22.1 \pm 3.0) | 19.6 \pm 0.8(19.9 \pm 0.7)"
  - "w/o \mathcal{L}^{\mathrm{seen}}_{\mathrm{pro}} | 55.7 \pm 1.4(25.5 \pm 1.5) | 20.1 \pm 0.4(16.2 \pm 0.6)"
  - "\mathcal{L}^{\mathrm{seen}}_{\mathrm{pro}} w/o \mathcal{C}^{\mathrm{new}} | 56.2 \pm 1.2(26.4 \pm 2.3) | 20.8 \pm 0.6(17.9 \pm 0.7)"
  - "OnPro ( ours ) | 57.8 \pm 1.1(23.2 \pm 1.3) | 22.7 \pm 0.7( 15.0 \pm 0.8)"
- APF against random mixup (Table 4, CIFAR-10, M = 0.1k/0.2k/0.5k): "Random | 53.5 \pm 2.7 | 62.9 \pm 2.5 | 70.8 \pm 2.2" ; "APF ( ours ) | 57.8 \pm 1.1 | 65.5 \pm 1.0 | 72.6 \pm 0.8".
- The APF ratio α (Table A5; CIFAR-10 M = 0.2k, CIFAR-100 M = 0.5k; α = 0, 0.10, 0.25, 0.50, 0.75, 0.9): "CIFAR-10 | 62.9 \pm 2.5 | 63.2 \pm 2.0 | 65.5 \pm 1.0 | 65.4 \pm 2.7 | 64.6 \pm 1.8 | 64.1 \pm 2.0" ; "CIFAR-100 | 22.0 \pm 1.5 | 22.7 \pm 0.7 | 22.1 \pm 1.1 | 21.7 \pm 1.2 | 21.3 \pm 1.3 | 21.1 \pm 1.1".
- CE placement (Table A3). Columns: CIFAR-10 accuracy and forgetting, then CIFAR-100 accuracy and forgetting. Rows: "\mathcal{L}_{\mathrm{CE}}(\mathrm{both}) | 48.5 \pm 2.2 | 46.6 \pm 2.4 | 20.4 \pm 0.6 | 41.0 \pm 0.6" ; "\mathcal{L}_{\mathrm{CE}}(\mathrm{sepa}) | 53.2 \pm 2.1 | 38.9 \pm 2.3 | 18.8 \pm 0.6 | 48.1 \pm 0.8" ; "OnPro ( ours ) | 57.8 \pm 1.1 | 23.2 \pm 1.3 | 22.7 \pm 0.7 | 15.0 \pm 0.8".
- Projector removed (Table A6, CIFAR-10): "no Projector | 56.1 \pm 4.7 | 63.3 \pm 1.9 | 71.0 \pm 1.5". Rotation added to baselines (Table A4, CIFAR-10): "OCM | 47.5 \pm 1.7 | 59.6 \pm 0.4 | 70.1 \pm 1.5" ; "DVC-Rot | 45.3 \pm 4.3 | 58.5 \pm 2.8 | 66.7 \pm 2.1". Knowledge distillation on ER (Table A1): "ER with KD | 17.0 \pm 2.7 | 17.3 \pm 2.1 | 17.6 \pm 0.8".

**(c) Headline, CIFAR-100** (10 tasks), online class-IL, M = 0.5k/1k/2k, 15 runs, ResNet18, Adam, replay batch 64. Caption: "Table 1: Average Accuracy (higher is better) on three benckmark datasets with different memory bank sizes M . All results are the average and standard deviation of 15 runs." Column order: CIFAR-10 ×3, CIFAR-100 ×3, TinyImageNet ×3.
- "OnPro ( ours ) | 57.8 \pm 1.1 | 65.5 \pm 1.0 | 72.6 \pm 0.8 |  | 22.7 \pm 0.7 | 30.0 \pm 0.4 | 35.9 \pm 0.6 |  | 11.9 \pm 0.3 | 16.9 \pm 0.4 | 22.1 \pm 0.4"
- strongest baseline: "OCM [ 26 ] | 47.5 \pm 1.7 | 59.6 \pm 0.4 | 70.1 \pm 1.5 |  | 19.7 \pm 0.5 | 27.4 \pm 0.3 | 34.4 \pm 0.5 |  | 10.8 \pm 0.4 | 15.4 \pm 0.4 | 20.9 \pm 0.7"
- "SCR [ 44 ] | 40.2 \pm 1.3 | 48.5 \pm 1.5 | 59.1 \pm 1.3 |  | 19.3 \pm 0.6 | 26.5 \pm 0.5 | 32.7 \pm 0.3 |  | 8.9 \pm 0.3 | 14.7 \pm 0.3 | 19.5 \pm 0.3"

**(d) Code.** Printed: "Source code is available at https://github.com/weilllllls/OnPro." The appendix of the same v1 also says: "The source code will be made publicly available upon the acceptance of this work." HTTP 403 (proxy). The connector found the repository; its description names the paper and ICCV 2023.

---

## 10. GSA: Guo, Liu, Zhao, CVPR 2023 (arXiv 2305.14657v1)

**(a) Mechanism**
- Decomposed loss for a new-class sample (Eq. 8): "\mathcal{L}_{decom}(x_{c_{n}})=-\log(\frac{e^{o_{c_{n}}}}{\sum^{m}_{s=n}e^{o_{c_{s}}}})-\log(\frac{e^{o_{c_{n}}}}{\sum^{n-1}_{s=1}e^{o_{c_{s}}}+e^{o_{c_{n}}}})"
- "The first term and second terms focus on the within-task classification goal and the last term focus on the cross-task classification goal."
- Self-adaptive weights (Eq. 13): "\small w_{y_{k}}=\frac{2}{1+e^{\textit{A-PN}(t^{\prime},t,y_{k})}},\hskip 9.24994ptv_{c_{s}}=\frac{1}{-\textit{PN}(t,c_{s})}" ; "When the model is training task t , we incrementally update the \textit{A-PN}(t^{\prime},t,y_{k}) and \textit{PN}(t,y_{k}) by adding the new gradients into the current sums of all previous gradients."
- "Like ER and many other online CL systems, GSA uses reservoir sampling for memory update."

**(b) Ablations.** Table 3: "Table 3 : Ablation accuracy - average of 5 runs. Memory size M is 1k for CIFAR100 and 2k for TinyImageNet." Columns: no new loss, no previous loss, no cross loss, no X^mix, no CL imbalance. Online class-IL.
- "CIFAR100 | 30.1 \pm 0.6 | 12.7 \pm 0.2 | 29.9 \pm 0.4 | 30.1 \pm 0.1 | 29.7 \pm 0.3"
- "TinyImageNet | 17.5 \pm 0.2 | 4.7 \pm 0.5 | 17.2 \pm 0.4 | 17.5 \pm 0.5 | 16.9 \pm 0.2"
- The column is headed "no X^{\textit{mix}}", while the text names an experiment "no balanced sampling": "In the experiments “no balanced sampling,” we replace the sampling strategy for X^{\textit{mix}} with random sampling from the memory buffer X^{\textit{buf}} ." The two labels differ as printed.
- Full GSA at the same settings (Table 1): CIFAR100 M = 1k gives 31.4 and TinyImageNet M = 2k gives 18.4 (the full row is quoted in (c)).
- OCM combined with GSA is reported in the text only: "For example, with the largest memory size for each dataset, OCM+GSA gives 96.5% on MNIST, 77.5% on CIFAR10, 53.7% on CIFAR100, and 35.7% on TinyImageNet and also outperforms OCM [16]."

**(c) Headline, CIFAR100** (10 tasks), online class-IL, M = 1k/2k/5k, 15 runs, ResNet18, Adam, X^new 10, X^mix/X^buf 64. Caption: "Table 1 : Accuracy on the four experiment datasets with different memory buffer sizes M . All values are averages of 15 runs." Column order: MNIST ×3, CIFAR10 ×3, CIFAR100 ×3, TinyImageNet ×3.
- "GSA | 91.4 \pm 0.1 | 93.2 \pm 0.1 | 96.5 \pm 0.1 | 58.0 \pm 0.4 | 64.6 \pm 0.2 | 69.1 \pm 0.3 | 31.4 \pm 0.2 | 39.7 \pm 0.6 | 49.7 \pm 0.2 | 18.4 \pm 0.4 | 26.0 \pm 0.2 | 33.2 \pm 0.4"
- strongest baselines on CIFAR100: "BiC [ 46 ] | 90.4 \pm 0.1 | 93.0 \pm 0.2 | 94.8 \pm 0.1 | 48.2 \pm 0.7 | 57.5 \pm 1.4 | 63.8 \pm 0.2 | 21.2 \pm 0.3 | 36.1 \pm 1.3 | 42.5 \pm 1.2 | 10.2 \pm 0.9 | 18.9 \pm 0.3 | 25.2 \pm 0.6" ; "SCR [ 31 ] | 86.2 \pm 0.5 | 92.8 \pm 0.3 | 94.6 \pm 0.1 | 47.2 \pm 1.7 | 58.2 \pm 0.5 | 64.1 \pm 1.2 | 26.5 \pm 0.2 | 31.6 \pm 0.5 | 36.5 \pm 0.2 | 10.6 \pm 1.1 | 17.2 \pm 0.1 | 20.4 \pm 1.1"
- OCM is not in the table: "Note that OCM is not compared in the tables as it is not a competitor of GSA."

**(d) Code.** Printed (footnote): "Code and Appendix: https://github.com/gydpku/GSA". HTTP 403 (proxy). The connector found the repository.

---

## 11. CCL-DC: Wang et al., CVPR 2024 (arXiv 2312.00600v2)

**(a) Mechanism**
- "CCL involves two peer continual learners of the same architecture and optimizer setting training in a peer-teaching manner. In the training phase, networks are supervised with both the ground truth label and the predictions of their peers."
- CCL loss (Eq. 9): "\displaystyle\lambda_{1}\cdot\mathcal{L}_{cls}(\theta^{1}(X),y)" plus "\displaystyle\lambda_{2}\cdot D_{KL}(\theta^{1}(X)/\tau,\theta^{2}(X)/\tau),"
- Distillation chain: "We take three augmentation steps and distill the logit distribution from the teacher with harder samples to the student with easier samples." ; overall "\displaystyle\mathcal{L}^{1}=\mathcal{L}_{Baseline}+\mathcal{L}_{CCL}^{1}+\mathcal{L}_{DC}^{1},"

**(b) Ablations** (CIFAR-100, 10 tasks, online class-IL, M = 2k; Acc. and LA = learning accuracy)
- Table 6: "Table 6 : Ablation studies on CIFAR-100 (M=2k). We report the ensemble performance for methods incorporating CCL."
  - "ER | 31.89 ±1.45 | 51.53 ±1.66" ; "ER + Multivew | 38.18 ±1.46 | 64.02 ±1.12" ; "ER + Ours (CCL only) | 41.05 ±1.21 | 68.76 ±0.79" ; "ER + Ours | 44.45 ±1.04 | 70.86 ±0.72"
  - "ER-ACE | 34.21 ±1.53 | 39.95 ±2.00" ; "ER-ACE + Multivew | 38.61 ±1.48 | 47.45 ±1.88" ; "ER-ACE + Ours (CCL only) | 40.90 ±1.08 | 50.91 ±1.63" ; "ER-ACE + Ours | 45.14 ±1.00 | 68.39 ±1.32"
- Distillation direction (Table 7): "ER | Easy to hard | 40.95 ±0.97 | 60.03 ±0.98" ; "ER | Same difficulty | 43.64 ±1.09 | 69.49 ±0.78" ; "ER | Hard to easy (Ours) | 44.45 ±1.04 | 70.86 ±0.72" ; "ER-ACE | Easy to hard | 38.46 ±1.51 | 39.00 ±1.03" ; "ER-ACE | Same difficulty | 43.81 ±1.28 | 55.37 ±1.54".
- Self-distillation in a single model (Table 8): "ER + SDC | Easy to hard | 35.00 ±1.31 | 56.67 ±0.84" ; "ER + SDC | Hard to easy | 41.31 ±1.25 | 68.62 ±0.60".
- Distilling from an untrained peer (Table 2, CIFAR-100 M = 1k/2k/5k): "ER + Untrained Distillation | 27.07 ±1.20 | 34.84 ±0.64 | 41.15 ±1.16" against "ER | 24.47 ±0.72 | 31.89 ±1.45 | 39.41 ±1.81".
- Ensemble against a single model (Table 9), for example "ER + Ours (Ind.) | 65.66 ±2.35 | 73.37 ±1.70 | 32.97 ±1.06 | 43.58 ±1.05 | 52.96 ±1.16 | 16.32 ±1.58 | 28.68 ±1.20 | 37.14 ±0.93 | 41.82 ±1.54". The authors: "Generally, the ensemble method provides about 1% additional accuracy compared to independent inference."
- NCM against logits (Table 11): "ER | 36.56 ±0.60 | 31.89 ±1.45" ; "ER + Ours | 44.76 ±0.55 | 44.45 ±1.04".

**(c) Headline, CIFAR-100** (10 tasks), online class-IL, M = 1000/2000/5000, full ResNet-18, stream batch 10, memory batch 64, 10 runs, ensemble of two peers. Caption: "Table 3 : Average Accuracy (%, higher is better) on four benchmark datasets with difference memory buffer size M , with and without our proposed CCL-DC scheme. The result of our method is given by the ensemble of two peer models. All values are averages of 10 runs." Columns: CIFAR10 500/1000, CIFAR100 1000/2000/5000, Tiny-ImageNet ×3, ImageNet-100.
- "GSA + Ours | 68.91 ±1.68 | 75.78 ±1.16 | 35.56 ±1.39 | 44.74 ±1.32 | 55.39 ±1.09 | 16.70 ±1.66 | 28.11 ±1.70 | 37.13 ±1.75 | 44.28 ±1.16"
- "ER-ACE + Ours | 70.08 ±1.38 | 75.56 ±1.14 | 37.20 ±1.15 | 45.14 ±1.00 | 53.92 ±0.48 | 18.32 ±1.49 | 26.22 ±2.01 | 32.23 ±1.70 | 45.15 ±1.94"
- The strongest baseline without CCL-DC on CIFAR-100 is OCM at M = 1000/2000 and GSA at M = 5000: "OCM [ 19 ] | 68.19 ±1.75 | 73.15 ±1.05 | 28.02 ±0.74 | 35.69 ±1.36 | 42.22 ±1.06 | 18.36 ±0.95 | 26.74 ±1.02 | 31.94 ±1.19 | 23.67 ±2.36" ; "GSA [ 20 ] | 60.34 ±1.97 | 66.54 ±2.28 | 27.72 ±1.57 | 35.08 ±1.37 | 41.41 ±1.65 | 12.44 ±1.17 | 19.59 ±1.30 | 25.34 ±1.43 | 41.03 ±0.99" ; "OnPro [ 44 ] | 70.47 ±2.12 | 74.70 ±1.51 | 27.22 ±0.77 | 33.33 ±0.93 | 41.59 ±1.38 | 14.32 ±1.40 | 21.13 ±2.12 | 26.38 ±2.18 | 38.75 ±1.03"
- Reader's note: the OnPro, GSA and OCM values here are CCL-DC's re-runs. They differ from each method's own paper (sections 8–10).

**(d) Code.** Printed: "The source code of our work is available at https://github.com/maorong-wang/CCL-DC." HTTP 403 (proxy). The connector found the repository.

---

## 12. Buzzega et al. 2020, *Rethinking Experience Replay: a Bag of Tricks* (arXiv 2010.05595v1)

**(a) Mechanism.** The baseline is ER with reservoir sampling; the tricks are added to it.
- "\mathcal{L}^{\prime}=\mathds{E}_{(x,y)\sim\mathcal{D}_{t}}\big[\ell(y,f_{\theta}(x))\big]+\mathds{E}_{(x,y)\sim\mathcal{B}}\big[\ell(y,f_{\theta}(x))\big]."
- IBA: "in addition to the regular augmentation performed on the input stream, we store examples not augmented in the memory buffer; this way, we can augment them independently when drawn for later replay."
- ELrD: "lr_{j}=lr_{0}\cdot{\gamma}^{N_{ex}},"
- BRS: "instead of replacing a random exemplar when a newer one is inserted (line 8 of Alg. 1), we look for the element to be removed among those belonging to the most represented class (lines 9 - 11 )."
- LARS: "we propose using the training loss value directly as a much simpler yet effective criterion for modeling the importance of examples."
- Setting: offline class-IL (multi-epoch): "iterating on each task for one epoch in Split Fashion-MNIST, 50 epochs in Split CIFAR-10 and CIFAR-100 and 15 epochs in Split CORe-50."

**(b) Ablations**
- Tricks added one at a time. "TABLE II: Accuracy values on several datasets as more tricks from Sec IV are added to the baseline, with replay buffer size 200 ." Columns: Fash-MNIST, CIFAR-10, CIFAR-100 (Split CIFAR-100 in 10 tasks). Rows: "ER | 72.54 | 24.06 | 9.66" ; "+ IBA | – | 44.78 | 13.90" ; "+ BiC | 73.43 | 49.27 | 17.73" ; "+ ElrD | 74.19 | 51.02 | 20.27" ; "+ BRS | 74.66 | 52.75 | 20.64" ; "+ LARS | 76.07 | 59.18 | 21.26".
- IBA on other rehearsal methods (Table III, buffers 200/500/1000, CIFAR-10 then CIFAR-100): "GEM [ 13 ] | 28.14 | 34.69 | 36.68 | 9.18 | 14.12 | 17.88" against "+ IBA | 22.62 | 23.01 | 20.25 | 13.69 | 16.74 | 15.21" ; "HAL [ 26 ] | 25.92 | 27.99 | 29.10 | 7.63 | 9.66 | 10.43" against "+ IBA | 32.33 | 41.77 | 49.28 | 8.19 | 11.39 | 12.91" ; "A-GEM [ 24 ] | 19.90 | 20.35 | 19.81 | 9.17 | 9.23 | 9.12" against "+ IBA | 20.23 | 19.97 | 21.15 | 9.16 | 9.34 | 9.39".
- BiC/CBiC/ElrD on non-rehearsal methods (Table IV, Split Fashion-MNIST, buffer 500): "SI | 19.91 | 24.67 | 33.15 | 35.51" ; "oEWC | 20.04 | 25.71 | 40.36 | 43.85" (No trick, BiC, CBiC, CBiC+ElrD).
- BRS against reservoir on a toy set: "The two approaches achieve a Mean Squared Error of 0.28 and 1.64 respectively."

**(c) Headline, CIFAR-100** (Split CIFAR-100, 10 tasks; offline class-IL, 50 epochs per task; ResNet18; buffers 200/500/1000; 10 runs). Caption: "TABLE I: Comparison among state-of-the-art methods in terms of average final accuracy on several datasets." The row cells run F-MNIST ×3, CIFAR-10 ×3, CIFAR-100 ×3, CORe-50 ×3.
- "ER+T (ours) | \boldsymbol{76.07} | \boldsymbol{80.11} | \boldsymbol{82.46} | \boldsymbol{59.18} | \boldsymbol{62.60} | \boldsymbol{70.99} | \boldsymbol{21.26} | \boldsymbol{24.90} | \boldsymbol{36.05} | \boldsymbol{25.63} | \boldsymbol{33.33} | \boldsymbol{37.44}"
- strongest baseline on CIFAR-100: "iCaRL [ 2 ] | 75.46 | 77.54 | 78.13 | 41.26 | 41.34 | 42.03 | 20.73 | 24.74 | 25.52 | 8.01 | 7.23 | 8.05"
- "ER [ 12 ] | 72.54 | 79.02 | 81.39 | 24.06 | 27.06 | 31.38 | 9.66 | 11.50 | 12.36 | 19.48 | 28.54 | 32.66" ; "Joint Training | 84.47 | 92.13 | 70.66 | 49.51"

**(d) Code.** Printed: "We make the code for these experiments publicly available" with footnote https://github.com/hastings24/rethinking_er. HTTP 403 (proxy). The connector's search for `repo:hastings24/rethinking_er` failed: the repository does not exist or is not visible. A search by name found `pbuzzega/rethinking_er`, which is described as the code for this paper. The printed link therefore **did not resolve** through the connector, and a repository under a different owner exists.

---

## 13. MKD: Michel et al., ICML 2024 (arXiv 2309.02870v2)

**(a) Mechanism**
- Teacher: "\theta_{\alpha}(t)=\alpha*\theta(t)+(1-\alpha)*\theta_{\alpha}(t-1),"
- Loss (Eq. 3): "\displaystyle\mathcal{L}_{MKD}(X,Y)= | \displaystyle\mathcal{L}_{CE}(\hat{X},Y) |" plus "\displaystyle\frac{\lambda_{\alpha}}{2}KL(\mathcal{T}_{\alpha}(X),S(\hat{X}))" plus "\displaystyle\frac{\lambda_{\alpha}}{2}KL(\mathcal{T}_{\alpha}(\hat{X}),S(\hat{X})),"
- Inference: "We compute the final model parameters \theta^{\star} as the average of teacher and student weights"
- Settings: "For MKD, we use \alpha=0.01 and \lambda_{\alpha}=5.5 accordingly for every method." ; "The optimal value for \lambda_{\alpha} given \alpha follows the formula \lambda_{\alpha}=a*\log_{10}(\alpha)+b , with a=9/2 and b=29/2 ."

**(b) Ablations** (CIFAR100 10 tasks, online class-IL, clear boundaries)
- Table 5: "Table 5 : Final average accuracy (%) on CIFAR100, clear boundary setting, for ER + ours and varying memory sizes." M = 1000/2000/5000: "ER + ours | 38.5 ±0.5 | 45.2 ±0.2 | 52.1 ±0.5" ; "ER + ours (student) | 37.7 ±0.7 | 44.7 ±0.5 | 51.2 ±0.6" ; "ER + ours (teacher) | 37.2 ±0.7 | 43.0 ±0.8 | 49.4 ±0.6" ; "ER + ours (student, single view) | 34.8 ±0.6 | 41.8 ±0.6 | 47.9 ±0.4".
- Teacher quality (Table 2, CIFAR100 in 2 tasks, M = 5k): "ER | 49.0 \pm 4.6" ; "ER+low qual. teach. | 50.7 \pm 4.3" ; "ER+high qual. teach. | 54.6 \pm 3.3".
- α and λ_α: grid in figures only (Fig. 4, Fig. 5); no table values.
- NCM against logits (Table 6, CIFAR100 M = 1k): "ER + ours | 38.5 ±0.5 | 31.5 ±0.5 ( \downarrow 7.0)" ; "GSA + ours | 40.1 ±1.0 | 36.2 ±0.5 ( \downarrow 3.9)".
- Backward transfer (Table 7, CIFAR100 M = 5k then ImageNet100 M = 10k): "ER | -16.7 ±1.2 | -17.5 ±1.5" ; "ER + ours | + 8.15 ±0.8 | - 1.3 ±2.3".

**(c) Headline, CIFAR100**, online class-IL, clear boundary, M = 1000/2000/5000, full ResNet18, 5 runs. Caption: "Table 3 : Final average accuracy (%) for the clear boundary setting at the end of training for considered baselines, with and without our additional MKD procedure. Results are displayed for different datasets and memory sizes. Displayed values are the mean and standard deviation computed over 5 runs." Columns: CIFAR10 200/500/1000, CIFAR100 ×3, Tiny-IN ×3, ImageNet100 ×3.
- "GSA + ours | 57.66 ±4.11 | 68.16 ±0.85 | 75.08 ±1.14 | 40.1 ±1.0 | 48.23 ±0.78 | 56.15 ±0.6 | 23.14 ±0.44 | 32.38 ±1.28 | 38.78 ±0.65 | 33.4 ±0.85 | 44.99 ±0.46 | 52.41 ±0.59"
- "ER + ours | 57.54 ±2.55 | 68.48 ±0.92 | 74.33 ±0.68 | 38.5 ±0.5 | 45.2 ±0.2 | 52.10 ±0.5 | 23.95 ±0.65 | 32.22 ±0.88 | 38.27 ±0.18 | 30.67 ±0.46 | 39.7 ±1.07 | 44.92 ±0.98"
- strongest baseline without MKD on CIFAR100: "ER + Temp. Ens. | 48.80 ±2.60 | 62.10 ±1.70 | 70.20 ±0.20 | 30.00 ±0.70 | 37.90 ±0.90 | 46.80 ±0.90 | 16.30 ±0.50 | 23.60 ±0.40 | 30.00 ±0.50 | 20.40 ±0.50 | 33.12 ±1.70 | 40.10 ±1.15" ; "GSA [CVPR‘23] | 48.9 ±3.38 | 61.45 ±1.95 | 67.63 ±1.24 | 29.68 ±1.54 | 36.96 ±0.79 | 45.86 ±1.89 | 15.77 ±0.72 | 22.48 ±0.4 | 28.46 ±1.85 | 24.29 ±0.59 | 33.47 ±1.18 | 40.18 ±0.93" ; "ER [NeurIPS‘19] | 46.33 ±2.42 | 55.73 ±2.04 | 62.99 ±2.1 | 23.0 ±0.8 | 31.55 ±1.27 | 38.05 ±1.08 | 11.39 ±0.75 | 18.97 ±1.16 | 21.52 ±3.37 | 19.06 ±0.9 | 29.74 ±1.34 | 36.72 ±1.09"

**(d) Code.** Printed: "The code is available at https://github.com/Nicolas1203/mkd_ocl." HTTP 403 (proxy). The connector found the repository.

---

## 14. Mai et al. 2022 survey, *Online Continual Learning in Image Classification: An Empirical Survey* (arXiv 2101.10423v4)

**(a) Mechanism.** This is a survey; its common frame is the generic memory-based loop.
- "For every incoming mini-batch, the algorithm retrieves another mini-batch from a memory buffer, updates the model using both the incoming and memory mini-batches and then updates the memory buffer with the incoming mini-batch."
- "What differentiate various memory-based methods are the memory retrieval strategy (line 3) [16, 87], model update (line 4) [10, 11] and memory update strategy (line 5) [62, 64, 17]."
- Tricks it tests on top of replay. Labels trick: "the outputs that do not correspond to the classes of the current mini-batch are masked out when calculating the loss." Review trick: "At the end of learning the current task, the review trick fine-tunes the model with all the samples in the memory buffer using only the cross-entropy loss." KDC*: "Hence, we suggest setting \lambda to \sqrt{\frac{\mathinner{\!\left\lvert C_{new}\right\rvert}}{\mathinner{\!\left\lvert C_{old}\right\rvert}+\mathinner{\!\left\lvert C_{new}\right\rvert}}} ."
- Setting: "The network is trained via the cross-entropy loss with a stochastic gradient descent optimizer and a mini-batch size of 10. The size of the mini-batch retrieved from the memory buffer is also set to 10, irrespective of the size of the memory buffer as in [35]."

**(b) Ablations.** The survey adds tricks to A-GEM, ER and MIR. Online class-IL, Split CIFAR-100 (20 tasks), M = 1k/5k/10k. "Table 9 : Performance of compared tricks for the OCI setting on Split CIFAR-100. We report average accuracy (end of training) for memory buffer with size 1k, 5k and 10k." Columns: A-GEM ×3, ER ×3, MIR ×3.
- "N/A | 3.7\pm 0.4 | 3.6\pm 0.2 | 3.8\pm 0.2 | 7.6\pm 0.5 | 17.0\pm 1.9 | 18.4\pm 1.4 | 7.6\pm 0.5 | 18.2\pm 0.8 | 19.3\pm 0.7"
- "LB | 5.0\pm 0.5 | 4.6\pm 0.8 | 4.9\pm 0.7 | 14.0\pm 2.0 | 19.0\pm 2.6 | 20.4\pm 1.2 | \mathbf{15.1\pm 0.6} | 21.1\pm 0.8 | 22.5\pm 0.9"
- "KDC | 8.3\pm 0.7 | 8.8\pm 0.7 | 7.7\pm 1.1 | 11.7\pm 0.8 | 10.9\pm 1.9 | 11.9\pm 2.2 | 12.0\pm 0.5 | 12.3\pm 0.7 | 11.8\pm 0.6"
- "KDC* | 5.6\pm 0.5 | 5.8\pm 0.5 | 5.8\pm 0.5 | 12.6\pm 0.5 | 21.2\pm 1.1 | 24.2\pm 1.9 | 12.4\pm 0.5 | 20.7\pm 0.8 | 23.2\pm 1.2"
- "MI | 4.0\pm 0.3 | 4.0\pm 0.3 | 4.0\pm 0.2 | 8.6\pm 0.5 | 19.7\pm 0.9 | 26.4\pm 1.2 | 8.5\pm 0.4 | 17.7\pm 1.0 | 25.9\pm 1.2"
- "SS | 5.0\pm 0.8 | 5.2\pm 0.6 | 5.1\pm 0.5 | 12.3\pm 2.1 | 20.9\pm 1.0 | 23.1\pm 1.2 | 14.0\pm 0.5 | 21.6\pm 0.7 | 24.5\pm 0.7"
- "NCM | \mathbf{9.5\pm 0.9} | 11.7\pm 0.6 | 11.5\pm 0.7 | \mathbf{14.6\pm 0.7} | \mathbf{27.6\pm 1.0} | 31.0\pm 1.0 | 13.7\pm 0.5 | 27.0\pm 0.5 | 30.0\pm 0.6"
- "RV | 4.5\pm 0.4 | \mathbf{22.5\pm 1.3} | \mathbf{30.7\pm 1.2} | 12.0\pm 0.8 | 26.9\pm 2.8 | \mathbf{32.0\pm 5.3} | 9.7\pm 0.5 | \mathbf{28.1\pm 0.6} | \mathbf{35.2\pm 0.5}"
- Running times on ER (Table 10, seconds, M = 1k/5k/10k): "NCM | 126 | 282 | 450" ; "RV | 98 | 159 | 230" ; "MI | 328 | 324 | 325" ; "N/A | 83 | 82 | 84".
- The authors: "When the memory size is small, LB and NCM are the most effective, showing around 64% relative improvement." The Section 8.4 text says instead: "LB and NCM are the most effective when M=1k and can improve the accuracy by around 100% (7.6% \rightarrow 14.5% on average)." The two figures differ as printed.

**(c) Headline, CIFAR-100.** "Split CIFAR-100 is constructed by splitting the CIFAR-100 dataset [105] into 20 tasks with disjoint classes, and each task has 5 classes." Setting: online class-IL, reduced ResNet18, M = 1k/5k/10k. "Table 7 : Average accuracy (end of training) for the OCI setting of Split CIFAR-100, Split Mini-ImageNet and CORe50-NC. Replay-based methods and a strong baseline GDumb show competitive performance across three datasets." Columns: CIFAR-100 ×3 first.
- "GDumb | 10.4\pm 1.1 | \mathbf{22.1\pm 0.9} | \mathbf{28.8\pm 0.9} | 8.8\pm 0.4 | \mathbf{21.1\pm 1.7} | \mathbf{31.0\pm 1.4} | 15.1\pm 1.2 | 28.1\pm 1.4 | 32.6\pm 1.7"
- "iCaRL | \mathbf{16.7\pm 0.8} | 19.2\pm 1.1 | 18.8\pm 0.9 | \mathbf{14.7\pm 0.4} | 17.5\pm 0.6 | 17.4\pm 1.5 | 22.1\pm 1.4 | 25.1\pm 1.6 | 22.9\pm 3.1"
- "MIR | 7.6\pm 0.5 | 18.2\pm 0.8 | 19.3\pm 0.7 | 6.4\pm 0.9 | 16.5\pm 2.1 | 21.0\pm 1.1 | \mathbf{27.0\pm 1.6} | \mathbf{32.9\pm 1.7} | \mathbf{34.5\pm 1.5}"
- "ER | 7.6\pm 0.5 | 17.0\pm 1.9 | 18.4\pm 1.4 | 6.4\pm 0.9 | 14.5\pm 2.1 | 15.9\pm 2.0 | 23.5\pm 2.4 | 27.5\pm 3.5 | 28.2\pm 3.3"
- "Offline | 49.7\pm 2.6 | 51.9\pm 0.5 | 51.7\pm 1.8"

**(d) Code.** Printed: "Our codes are available at https://github.com/RaptorMai/online-continual-learning." The abs page links the same repository. HTTP 403 (proxy). The connector found the repository.

---

## Quote check

The check was run after writing, with `lit0925/clsota/replay/quote_check.py` in the session scratchpad. For every string of 20 or more
characters in straight double quotes in this file, it tests whether the string appears in the corpus of saved texts
(`*.txt`, `*.tables.txt`, abs-page texts and `code_link_status.txt`). Before matching, both sides are HTML-unescaped, U+FFFE and
U+00AD are removed (the PDF line-break hyphenation markers, as in "in￾creased"), and every run of whitespace is collapsed to one
space. The counts are below.

- Body of this file (everything above this section): **394** strings in straight double quotes. **378** of them are 20 or more
  characters long.
- **Final run: 378 of 378 found, 0 not found.**
- First run: 375 found, 3 not found. The three were fixed by shortening them to the verbatim part:
  - an ellipsis I had placed inside the arXiv search-page quote;
  - a trailing "| ..." on the ER row in section 1(c);
  - the MKD Eq. (3) fragment in section 13(a), whose "(3)" cell sits on a separate row of the extracted text.
- The 16 shorter quoted strings (under 20 characters) are outside the check's scope. They were also looked up, and all 16 were
  found.
- What the check does not cover: text outside quotes, such as settings, row identities and "strongest baseline" labels, is the
  reader's wording. It was not checked mechanically.
