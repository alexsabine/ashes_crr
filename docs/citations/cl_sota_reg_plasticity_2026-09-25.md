# State-of-the-art CL methods, regularisation, gradient-projection and plasticity family: mechanisms and ablations, read on the day (R10), 2026-09-25

**Status.** Owner request: prompt-log entry 191. This file is the source record for `CL Design Principle/`.
Nothing here is a result of this repository. It is a record of what the cited papers print, fetched and read on
2026-09-25. Text inside straight double quotes is copied verbatim from the saved fetches. LaTeX inside a quote is
the arXiv HTML page's math alt-text, kept as printed. Text outside quotes is the reader's note or a transcription
of table cells. Table transcriptions are labelled as such and give the table number. They are not quotes.

**Access.** Everything was fetched with `curl` through the session proxy on 2026-09-25:
- the arXiv abstract page, which gives the submission history and the title check;
- the arXiv HTML full text at `arxiv.org/html/<id>vN`;
- the arXiv PDF, with text extracted by `pypdfium2`;
- for the two Nature-family papers, the nature.com article page, the article PDF and the separate table pages.

The raw files and text extractions are in the session scratchpad under `lit0925/clsota/reg/`. Their names are
`abs_*.html`, `html_*.html/.txt`, `pdf_*.pdf/.txt`, `nature_*.html/.pdf/.txt`, `nmi_table*.html/.txt` and
`mammoth_*`. `code_status.txt` holds the code-link checks.

Every arXiv abstract page and every HTML and PDF fetch returned HTTP 200. The arXiv HTML build for SI (1703.04200v3)
contains no article body (the page is titled "Untitled Document"), so SI was read from the PDF.

The arXiv export API (`export.arxiv.org/api/query`) returned HTTP 406 through the proxy. Title searches therefore
used `arxiv.org/search/?searchtype=title`.

Every `github.com` URL returned HTTP 403 from the proxy. Each repository was then checked with `git ls-remote`,
which resolved. The HEAD commit is given per work.

| work | version and date | URL | read ([F]/[A]) |
|---|---|---|---|
| 1. Kirkpatrick et al., *Overcoming catastrophic forgetting in neural networks* (EWC) | arXiv 1612.00796 v2, 25 Jan 2017 (v1 2 Dec 2016); PNAS DOI 10.1073/pnas.1611835114 listed on abs page | https://arxiv.org/abs/1612.00796 ; https://arxiv.org/html/1612.00796v2 | [F] |
| 2. Schwarz et al., *Progress & Compress: A scalable framework for continual learning* (online EWC) | arXiv 1805.06370 v2, 2 Jul 2018; comment "Accepted at ICML 2018" | https://arxiv.org/abs/1805.06370 ; https://arxiv.org/html/1805.06370v2 | [F] |
| 3. Zenke, Poole, Ganguli, *Continual Learning Through Synaptic Intelligence* (SI) | arXiv 1703.04200 v3, 12 Jun 2017; comment "ICML 2017" | https://arxiv.org/abs/1703.04200 ; https://arxiv.org/pdf/1703.04200v3 (HTML build empty) | [F] |
| 4. Aljundi et al., *Memory Aware Synapses: Learning what (not) to forget* (MAS) | arXiv 1711.09601 v4, 5 Oct 2018; comment "ECCV 2018" | https://arxiv.org/abs/1711.09601 ; https://arxiv.org/html/1711.09601v4 | [F] |
| 5. Lopez-Paz & Ranzato, *Gradient Episodic Memory for Continual Learning* (GEM) | arXiv 1706.08840 v6, 13 Sep 2022 (v5 4 Nov 2017); comment "Published at NIPS 2017" | https://arxiv.org/abs/1706.08840 ; https://arxiv.org/html/1706.08840v6 | [F] |
| 6. Chaudhry et al., *Efficient Lifelong Learning with A-GEM* (A-GEM) | arXiv 1812.00420 v2, 9 Jan 2019; comment "Published as a conference paper at ICLR 2019" | https://arxiv.org/abs/1812.00420 ; https://arxiv.org/html/1812.00420v2 | [F] |
| 7. Ash & Adams, *On Warm-Starting Neural Network Training* (shrink and perturb) | arXiv 1910.08475 v3, 31 Dec 2020; journal ref "2020 Advances in Neural Information Processing Systems" | https://arxiv.org/abs/1910.08475 ; https://arxiv.org/html/1910.08475v3 | [F] |
| 8. Kumar, Marklund, Van Roy, *Maintaining Plasticity in Continual Learning via Regenerative Regularization* (L2 Init) | arXiv **2308.11958** v3, 24 Oct 2024 (id found by title search; title matches) | https://arxiv.org/abs/2308.11958 ; https://arxiv.org/html/2308.11958v3 | [F] |
| 9. Sokar et al., *The Dormant Neuron Phenomenon in Deep Reinforcement Learning* (ReDo) | arXiv 2302.12902 v2, 13 Jun 2023; comment "Oral at ICML 2023" | https://arxiv.org/abs/2302.12902 ; https://arxiv.org/html/2302.12902v2 | [F] |
| 10. Dohare et al., *Loss of plasticity in deep continual learning* (continual backprop) | Nature 632, published 2024-08-21, DOI 10.1038/s41586-024-07711-7. **arXiv 2306.13812 is titled differently on arXiv**: *Maintaining Plasticity in Deep Continual Learning*, v3, 9 Apr 2024. Same authors, and it is the preprint of the same work. The class-incremental CIFAR-100 experiment is in the Nature version only (see §10). | https://www.nature.com/articles/s41586-024-07711-7 ; https://arxiv.org/abs/2306.13812 ; https://arxiv.org/html/2306.13812v3 | [F] (both) |
| 11. Porrello et al., *A Second-Order Perspective on Model Compositionality and Incremental Learning* (ITA / IEL; Mammoth `models/second_order.py`) | arXiv **2405.16350** v3, 28 Feb 2025; comment "Accepted to ICLR 2025 (Spotlight)" (id found by title search) | https://arxiv.org/abs/2405.16350 ; https://arxiv.org/html/2405.16350v3 ; OpenReview https://openreview.net/forum?id=OZVTqoli2N (link as printed in Mammoth docs; not fetched) | [F] |
| 12. Wang, Zhang, Su, Zhu, *A Comprehensive Survey of Continual Learning: Theory, Method and Application* | arXiv 2302.00487 v3, 6 Feb 2024; comment "The concise version is in IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)" | https://arxiv.org/abs/2302.00487 ; https://arxiv.org/html/2302.00487v3 | [F] (sections IV-A to IV-E, Tables I–III) |
| 13. van de Ven, Tuytelaars, Tolias, *Three types of incremental learning* | Nature Machine Intelligence, published 2022-12-05, DOI 10.1038/s42256-022-00568-3. **arXiv 1904.07734 is a different title**: *Three scenarios for continual learning* (van de Ven & Tolias), v1 only, 15 Apr 2019. The NMI article's reference list cites it as one of "two preprints of this article". The 2019 preprint has no CIFAR-100 experiment. The CIFAR-100 table is read from the NMI article. | https://www.nature.com/articles/s42256-022-00568-3 ; table page https://www.nature.com/articles/s42256-022-00568-3/tables/3 ; https://arxiv.org/abs/1904.07734 | [F] (NMI Table 3 and the Methods text on the protocol; the arXiv v1 was also fetched) |
| 14. Mammoth (aimagelab): README, REPRODUCIBILITY.md and docs of the local clone | git commit e75a491c69fd729edeb01431afb753d9157d9a81 (commit date Wed May 20 22:13:32 2026 +0200). `git ls-remote` on 2026-09-25 gives the same commit as the remote HEAD. A title search found no arXiv paper named *Mammoth: an extendible (general) continual learning framework*. The README's "Citing the library" section cites Boschini et al. 2022 (TPAMI, X-DER) and Buzzega et al. 2020 (NeurIPS, DER). Neither was fetched. | local clone; https://github.com/aimagelab/mammoth (HTTP 403 via proxy; `git ls-remote` resolves) | [F] (README, REPRODUCIBILITY.md, docs files named below) |

Title check: every arXiv id given in the request matched its title on the abstract page, with two exceptions.
- 2306.13812: the arXiv title is *Maintaining Plasticity in Deep Continual Learning*. The Nature title is different.
- 1904.07734: this id is the 2019 preprint *Three scenarios for continual learning*, not the 2022 NMI article.

Two ids were not supplied and were found by title: 2308.11958 (L2 Init) and 2405.16350 (Second-Order).

---

## 1. EWC — Kirkpatrick et al. (arXiv 1612.00796 v2)

**(a) Mechanism.**
- "Given this approximation, the function {\cal L} that we minimize in EWC is:"
  "{\cal L}(\theta)={\cal L}_{B}(\theta)+\sum_{i}\frac{\lambda}{2}F_{i}(\theta_{i}-\theta^{*}_{A,i})^{2}" (Eq. 3)
- "where {\cal L_{B}}(\theta) is the loss for task B only, \lambda sets how important the old task is compared to the new one and i labels each parameter."
- "When moving to a third task, task C, EWC will try to keep the network parameters close to the learned parameters of both task A and B. This can be enforced either with two separate penalties, or as one by noting that the sum of two quadratic penalties is itself a quadratic penalty."

**(b) Ablations.** The paper prints no numeric ablation table. All comparisons below are figure-only and read from
the figure text and captions.
- L2 in place of the Fisher weighting (permuted MNIST, Fig. 2A): "This problem cannot be countered by regularizing the network with a fixed quadratic constraint for each weight (green curves, L2 regularization): here, the performance in task A degrades much less severely, but task B cannot be learned properly as the constraint protects all weights equally, leaving little spare capacity for learning on B."
- Dropout in place of EWC (permuted MNIST, Fig. 2B): "We find that stochastic gradient descent with dropout regularization alone is limited, and that it does not scale to more tasks (Figure 2B)."
- Inferred task label vs true task label (Atari, Fig. 3B): "As a control, we also considered the benefit to the agent if we explicitly provided the agent with the true task label (Figure 3B, brown), rather than relying on the learned task recognition through the FMN algorithm (red). The improvement here was only modest."
- No EWC (Atari, Fig. 3B): "If we rely on plain gradient descent methods as in (Mnih et al., 2015), the agent never learns to play more than one game and the harm inflicted by forgetting the old games means that the total human-normalized score remains below one."
- Fisher-shaped vs uniform vs nullspace weight perturbation (Breakout, Fig. 3C): "First, the agent was always more robust to parameter perturbations shaped by the inverse of the diagonal of the Fisher Information (blue), as opposed to uniform perturbations (black)." and "Empirically, however, we observe that perturbing in this space (orange) has the same effect as perturbing in the inverse Fisher space."

**(c) CIFAR-100 class-incremental.** None. The paper's experiments are permuted MNIST and Atari.

**(d) Code link.** No code link is printed in the paper or on the abstract page.

---

## 2. Online EWC — Schwarz et al., Progress & Compress (arXiv 1805.06370 v2)

**(a) Mechanism (Section 4, "Online EWC").**
- "\displaystyle-\log p(\mathcal{T}_{i}|\theta)+\frac{1}{2}\|\theta-\theta^{*}_{i-1}\|^{2}_{\gamma F^{*}_{i-1}}"
- "where \gamma<1 is a hyperparameter associated with removing the approximation term associated with the previous presentation of task" … "the overall Fisher is then updated as" "F^{*}_{i}=\gamma F^{*}_{i-1}+F_{i}"
- "We counteract this issue by normalising the Fisher information matrices F_{i} for each task."

**(b) Ablations.**
- EWC vs online EWC (Omniglot, Fig. 2(a)): "Most importantly, we do not observe a significant difference between online EWC and EWC, despite the additional memory cost of the latter."
- Table 2, "Results on sequential Omniglot. Shown is the performance on all tasks after training. Results show mean and std. dev over task permutations." Transcription of test accuracy after passes 1 to 5:

| model (as printed) | pass 1 | 2 | 3 | 4 | 5 | #params |
|---|---|---|---|---|---|---|
| EWC (λ=12.5) | 67.32 ± 4.7 | 71.92 ± 2.3 | 74.20 ± 2.8 | 74.46 ± 3.4 | 75.96 ± 3.2 | 11,100 K |
| online EWC (λ=17.5, γ=0.95) | 69.99 ± 3.2 | 73.46 ± 2.7 | 76.70 ± 1.9 | 79.26 ± 0.8 | 79.15 ± 1.9 | 446 K |
| P&C (λ=15.0, γ=0.99) | 70.32 ± 3.3 | 76.28 ± 1.3 | 78.65 ± 1.4 | 80.13 ± 1.0 | 82.84 ± 1.4 | 659 K |
| Finetuning | 26.20 ± 4.6 | 42.40 ± 7.4 | 54.24 ± 7.1 | 60.84 ± 4.1 | 60.74 ± 3.8 | 217 K |
| LwF (λ=0.1) | 62.06 ± 2.0 | 72.24 ± 2.6 | 68.44 ± 6.3 | 68.95 ± 3.0 | 66.48 ± 3.3 | 217 K |

  The same table also prints: Single model per Task 88.34 (5,680 K); Progressive Nets 86.50 ± 0.9 (108,000 K).
- Varying γ: "allowing more forgetting to happen (i.e. choosing a lower \gamma ) can lead to an overall higher performance."
  Grid: "we chose the regularisation strength \lambda and forgetting coefficient \gamma by running a grid search for \lambda =[10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0] and \gamma =[0.7, 0.8, 0.9, 0.95, 0.99]."
- Amount of training per task, EWC vs online EWC (permuted MNIST, Appendix A, Figs. 5–6): "For a small number of training steps (500 and 1000, training over minibatches of size 32), the network benefits from holding on to the memories of the earlier tasks (the accuracy of EWC, i.e. all blue dots in the plot are higher than for the online EWC, the red dots)." and "the online EWC doesn’t seem to find a good balance between the loss and penalties and the performance on older tasks is not well retained (faint red dots), although it’s still better than using no penalty at all (grey dots)."
- Re-initialising the active column (Atari), Table 1, "Positive Transfer on Atari. Shown is the relative performance after having trained on a various number of previous tasks." Transcription (% single-task performance, previous tasks 1 to 5): P&C (Active col, re-init) 127/129/125/129/128; P&C (Active col) 131/127/114/106/101; Finetuning 117/125/117/105/98; EWC 55/53/53/50/54; online EWC 53/53/49/50/57.

**(c) CIFAR-100 class-incremental.** None. The experiments are Omniglot, Atari and 3D mazes.

**(d) Code link.** None printed.

---

## 3. SI — Zenke, Poole, Ganguli (arXiv 1703.04200 v3, read from PDF)

The PDF extraction breaks words at line-end hyphens. The quote check below joins those breaks before matching (see
"Quote check"). Equations (4)–(5) are transcribed, not quoted, because the PDF text layer scrambles them:
L̃_μ = L_μ + c Σ_k Ω^μ_k (θ̃_k − θ_k)², with Ω^μ_k = Σ_{ν<μ} ω^ν_k / ((Δ^ν_k)² + ξ).

**(a) Mechanism.**
- "now have an intuitive interpretation as the parameter specific contribution to changes in the total loss" (about the ω^μ_k of Eq. 3). The next quote is about ω as well: "online as the running sum of the product of the gradient".
- "we introduced a surrogate loss which approximates the summed loss functions of previous tasks"
- "ensures that the regularization term carries the same units as the loss" … "Finally, c is a strength parameter which trades off old versus new memories." … "c typically has to be chosen smaller than one to compensate."

**(b) Ablations.** Figure-only, with no numeric table.
- Consolidation on vs off (split MNIST, multi-head, Fig. 3): "We now compare this performance between networks in which we turn consolidation dynamics on (c = 1) against cases in which consolidation was off (c = 0)." Result text: "the accuracy on the first two tasks, corresponding to the first four digits, has dropped back to chance levels in the cases without consolidation whereas the model with consolidation only shows minor degradation in performance on these tasks".
- Permuted MNIST (Fig. 4): the caption compares "Ours (c=0.1)", EWC, SGD and SGD with dropout: "SGD (green) and SGD with dropout of 0.5 on the hidden layers (red) perform far worse."
- Split CIFAR-10/100 (Fig. 6), c = 0 vs c = 0.1 vs training from scratch: "Importantly, the performance of networks trained with consolidation was always better than without consolidation, except on the last task."
- Choice of c: "To determine the best c, we performed this experiment for different values in the parameter range"
  The range printed is 1×10⁻³ < c < 0.1.

**(c) CIFAR-100 class-incremental.** None. The CIFAR-10/100 benchmark is multi-head (task-incremental): "We used the same multi-head setup as in the case of split MNIST".
Its first task is all of CIFAR-10. It is followed by "5 additional tasks each corresponding to 10 consecutive classes from the CIFAR-100 dataset".

**(d) Code link.** None printed in the PDF or on the abstract page.

---

## 4. MAS — Aljundi et al. (arXiv 1711.09601 v4)

**(a) Mechanism.**
- "\Omega_{ij}=\frac{1}{N}\sum_{k=1}^{N}\mid\mid g_{ij}(x_{k})\mid\mid" (Eq. 2)
- "As a more efficient alternative, we propose to use the gradients of the squared \ell_{2} norm of the learned function output"
- "L(\theta)=L_{n}(\theta)+{\lambda}\sum_{i,j}\Omega_{ij}(\theta_{ij}-\theta^{*}_{ij})^{2}". On the regularisation weight: "We use a regularization parameter \lambda of 1; note that no tuning of \lambda was performed as we assume no access to previous task data."

**(b) Ablations.**
- Squared ℓ2 norm vs vector output (Flower→Scenes, Flower→Birds): "We observe no significant difference on forgetting over 3 random trials where we get a mean, over 6 numbers, of 0.51\%\pm 0.18 for the drop on the first task in the vector output case compared to 0.50\%\pm 0.19 for the \ell^{2}_{2} norm case."
- Global MAS vs local Hebbian l-MAS, and Ω computed on train, test or both: "As such, l-MAS shows an average forgetting of 3\% compared to 1\% by MAS."
  Table 3, "Classification accuracies (%) for the object recognition setup - comparison between using Train and Test data (unlabeled) to compute the parameter importance \Omega_{ij} ."
  Transcription. Each cell gives accuracy on task 1 (drop in parentheses), then accuracy on task 2.

| method | Ω on | Birds→Scenes | Scenes→Birds | Flower→Bird | Flower→Scenes |
|---|---|---|---|---|---|
| MAS | Train | 53.24 (-0.4) / 55.0 | 57.61 (-1.4) / 49.62 | 77.33 (-0.7) / 50.39 | 77.24 (-0.8) / 57.38 |
| MAS | Test | 53.43 (-0.2) / 55.07 | 57.31 (-1.7) / 49.01 | 77.62 (-0.5) / 50.29 | 77.45 (-0.6) / 57.45 |
| MAS | Train + Test | 53.29 (-0.3) / 56.04 | 57.83 (-1.2) / 49.56 | 77.52 (-0.6) / 49.70 | 77.54 (-0.5) / 57.39 |
| l-MAS | Train | 51.36 (-2.3) / 55.67 | 56.79 (-2.2) / 49.08 | 73.96 (-4.1) / 50.5 | 76.20 (-1.9) / 56.68 |
| l-MAS | Test | 51.62 (-2.0) / 53.95 | 55.74 (-3.3) / 50.43 | 74.48 (-3.6) / 50.32 | 76.56 (-1.5) / 57.83 |
| l-MAS | Train + Test | 52.15 (-1.5) / 54.40 | 56.79 (-2.2) / 48.92 | 73.73 (-4.3) / 50.5 | 76.41 (-1.7) / 57.91 |

**(c) CIFAR-100 class-incremental.** None. The experiments are object-recognition task sequences (multi-head) and
fact learning on 6DS.

**(d) Code link.** None printed.

---

## 5. GEM — Lopez-Paz & Ranzato (arXiv 1706.08840 v6)

**(a) Mechanism.**
- Constraint (Eq. 7): "\left\langle g,g_{k}\right\rangle:=\left\langle\frac{\partial\ell(f_{\theta}(x,t),y)}{\partial\theta},\frac{\partial\ell(f_{\theta},\mathcal{M}_{k})}{\partial\theta}\right\rangle\geq 0,\mbox{ for all }k<t."
- "If violations occur, we propose to project the proposed gradient g to the closest gradient \tilde{g} (in squared \ell_{2} norm) satisfying all the constraints (7)."
- "GEM’s efficiency comes from optimizing over a number of variables equal to the number of tasks ( T=20 in our experiments), instead of optimizing over a number of variables equal to the number of parameters"

**(b) Ablations** (Section 4.4.1, "Importance of memory, number of passes, and order of tasks").
- Memory size (CIFAR100), Table 2, "ACC as a function of the episodic memory size for GEM and iCARL, on CIFAR100." Transcription of memory size 200 / 1,280 / 2,560 / 5,120: GEM 0.487 / 0.579 / 0.633 / 0.654; iCARL 0.436 / 0.494 / 0.500 / 0.508. Text: "the final ACC of GEM is an increasing function of the size of the episodic memory, eliminating the need to carefully tune this hyper-parameter."
- Number of passes (MNIST Rotations), Table 3, "ACC/BWT on the MNIST Rotations dataset, when varying the number of epochs per task." Transcription for 1 / 2 / 5 epochs:
  - single, shuffled data: 0.83/-0.00, 0.87/-0.00, 0.89/-0.00
  - single: 0.53/-0.08, 0.49/-0.25, 0.43/-0.40
  - independent: 0.56/-0.00, 0.64/-0.00, 0.67/-0.00
  - multimodal: 0.76/-0.02, 0.72/-0.11, 0.59/-0.28
  - EWC: 0.55/-0.19, 0.59/-0.17, 0.61/-0.11
  - GEM: 0.86/+0.05, 0.88/+0.02, 0.89/-0.02
- Compute, Table 1, "CPU Training time (s) of MNIST experiments for all methods."
  - permutations: single 11, independent 11, multimodal 14, EWC 179, GEM 77.
  - rotations: single 11, independent 16, multimodal 13, EWC 169, GEM 135.

**(c) CIFAR-100.** This setting is not class-incremental in the single-head sense. Setup quotes:
- "For all the datasets, we considered T=20 tasks." … "On the CIFAR100 dataset each task has 2500 examples from 5 different classes. The model observes the tasks in sequence, and each example once."
- "Also on CIFAR100, the network has a final linear classifier per task."

Headline: Table 2 above. The strongest baseline printed is iCARL; at memory 5,120 GEM has 0.654 and iCARL 0.508.
Grid (Appendix A) for GEM: "memory size: [5120 (rot, perm, cifar)]".

**(d) Code link.** Printed: "Our source code is available at https://github.com/facebookresearch/GradientEpisodicMemory."
HTTP 403 via proxy. `git ls-remote` resolves, HEAD 34c6b8e9a0607db7567301c48b727430d20bee7e.

---

## 6. A-GEM — Chaudhry et al. (arXiv 1812.00420 v2)

**(a) Mechanism.**
- "\displaystyle\frac{1}{2}||g-\tilde{g}||_{2}^{2}\quad\textrm{s.t.}\quad\tilde{g}^{\top}g_{ref}\geq 0" (Eq. 10)
- "In other words, a-gem replaces the t-1 constraints of gem with a single constraint, where g_{ref} is the average of the gradients from the previous tasks computed from a random subset of the episodic memory."
- "\tilde{g}=g-\frac{g^{\top}g_{ref}}{g_{ref}^{\top}g_{ref}}g_{ref}" (Eq. 11)

**(b) Ablations.**
- GEM vs S-GEM (one random constraint) vs A-GEM (averaged constraint), Table 3, "Comparison of different variations of gem on MNIST Permutations and Split CIFAR." Transcription (A_T %, F_T):

| method | Permuted MNIST | Split CIFAR |
|---|---|---|
| gem | 89.5, 0.06 | 61.2, 0.06 |
| s-gem | 88.2, 0.08 | 56.2, 0.12 |
| a-gem | 89.1, 0.06 | 62.3, 0.07 |

- Average vs worst-case forgetting, Table 2, "Comparison of average accuracy ( A_{T} ) and worst-case forgetting ( F_{wst} ) on the Episodic Memory ( \mathcal{M} ) and Test Set ( \mathcal{D}^{EV} )." Transcription (A_T, F_wst):
  - gem: MNIST memory 99.5, 0; MNIST test 89.5, 0.10; CIFAR memory 97.1, 0.05; CIFAR test 61.2, 0.14.
  - a-gem: MNIST memory 99.3, 0.008; MNIST test 89.1, 0.13; CIFAR memory 72.1, 0.15; CIFAR test 62.3, 0.15.
  Text: "gem enjoys lower worst-case task forgetting while a-gem enjoys better overall average accuracy."
- Constraint violations (Fig. 6): "As the number of tasks increase, gem violates the optimization constraints at almost each training step, whereas a-gem plateaus to a much lower value."
- Epochs and network size for EWC (Appendix F, Figs. 7–8), figure-only: "We observe that the average accuracy significantly improves with the number of epochs only when ewc is applied to the big network. In particular, in the single epoch setting, ewc peforms similarly to the baseline van on Split CIFAR which has fewer number of training examples per task."

**(c) CIFAR-100.** Split CIFAR here is task-incremental: "while on Permuted MNIST and Split CIFAR we provide integer task descriptors".
It has 20 tasks of 5 classes and a single pass: "report metrics on the remaining 17 tasks after doing a single training pass over each task in sequence".
Memory: "The amount of episodic memory per task used in icarl, gem and a-gem is set to 250 , 65 , 50 , and 100". The same sentence continues with the per-dataset list for MNIST, CIFAR, CUB and AWA, so CIFAR gets 65 per task.

Table 4, "Comparison with different baselines on Permuted MNIST and Split CIFAR." It is averaged over 5 seeds.
Transcription of the Split CIFAR columns (A_T %, F_T, LCA_10):
- van: 42.9 (± 2.07), 0.25, 0.30
- icarl: 50.1, 0.11
- ewc: 42.4 (± 3.02), 0.26, 0.33
- pi: 47.1 (± 4.41), 0.17, 0.31
- mas: 44.2 (± 2.39), 0.25, 0.33
- rwalk: 40.9 (± 3.97), 0.29, 0.32
- prog-nn: 59.2 (± 0.85), 0, 0.21
- gem: 61.2 (± 0.78), 0.06, 0.36
- a-gem (Ours): 62.3 (± 1.24), 0.07, 0.35
- multi-task: 68.3

**(d) Code link.** Printed: "The code is available at https://github.com/facebookresearch/agem."
HTTP 403 via proxy. `git ls-remote` resolves, HEAD 45421499483b28935491251e9e821c55e8b3c089.

---

## 7. Shrink and perturb — Ash & Adams (arXiv 1910.08475 v3)

**(a) Mechanism.**
- "we propose initializing the network’s parameters by shrinking the weights found in the previous round of optimization towards zero, then adding a small amount of parameter noise."
- "\theta_{i}^{t}\leftarrow\lambda\theta_{i}^{t-1}+p^{t}" with "p^{t}\sim\mathcal{N}(0,\,\sigma^{2}) and 0<\lambda<1"
- Every-step variant: "Exercising the shrink and perturb trick at every step of SGD would be very similar to applying an aggressive, noisy L_{2} regularization."

**(b) Ablations.**
- Shrink λ with noise fixed (online CIFAR-10, Fig. 7 caption text): "An online learning experiment varying \lambda and keeping the noise scale fixed at 0.01 . Note that \lambda=1 corresponds to fully-warm-started initializations and \lambda=0 corresponds to fully-random initializations. The proposed trick with \lambda=0.6 performs identically to randomly initializing in terms of validation accuracy, but trains much more quickly."
- Shrink vs perturb separately (Fig. 8 heatmap; numbers only in the figure image): "The perturbation step, adding noise after shrinking, improves both training time and generalization performance."
- Noise only, no shrink (Appendix Table 4, "Validation accuracies and warm-started model train times (minutes). Adding noise at the indicated standard deviations improves generalization, but not to the point of performing as well as randomly-initialized models. Better-generalizing warm-started models take even more time to train than their randomly-initialized peers, which on average achieve 55.2% accuracy in 34.0 minutes.").
  Transcription for noise std 1e-2 / 1e-3 / 1e-4 / 1e-5 / 0:
  - accuracy: 54.4 (0.9) / 53.5 (1.0) / 52.9 (1.0) / 49.9 (1.6) / 50.8 (1.8)
  - train time: 165.3 (3.9) / 38.0 (1.33) / 16.5 (1.3) / 14.6 (91.0) / 13.6 (0.4)
- Last layer only, and confidence regularisation: "As an alternative to shrinking all weights, we could try to increase the entropy of the output distribution by shrinking only parameters in the last layer (Appendix Figure 14), or by regularizing the model’s confidence while training (Appendix Table 3), but these are unable to resolve the warm-start problem."
- L2, adversarial and confidence regularisation: "We apply regularization in both rounds of training, and while it is helpful, regularization does not resolve the generalization gap induced by warm starting." Appendix Table 3 transcription (ResNet, CIFAR-10, penalty 1e-1 / 1e-2 / 1e-3 / 1e-4):
  - L2: RI 72.7 (4.2) / 55.4 (2.7) / 54.6 (2.4) / 55.1 (3.4); WS 63.9 (6.4) / 51.2 (2.7) / 50.5 (1.8) / 50.4 (1.3).
  - Adversarial: RI 54.8 (1.3) / 55.1 (1.5) / 55.3 (1.4) / 55.6 (0.9); WS 52.4 (1.0) / 52.6 (1.5) / 52.7 (1.2) / 50.4 (1.4).
  - Confidence: RI 53.1 (1.9) / 55.8 (1.3) / 55.4 (1.2) / 55.9 (1.4); WS 50.3 (0.7) / 50.0 (3.8) / 51.2 (1.2) / 49.3 (1.2).
- Every-step application on a static dataset (Appendix Figure 12): "Iterative application has a slight regularization effect."

**(c) CIFAR-100 class-incremental.** None. CIFAR-100 appears only in the warm-start experiment (train on 50%, then
100% of the same i.i.d. data). Table 1, "Validation percent accuracies for various optimizers and models for
warm-started and randomly initialized models on indicated datasets." Transcription of the CIFAR-100 rows, in the
order ResNet SGD / ResNet Adam / MLP SGD / MLP Adam / LR SGD / LR Adam:
- Random Init: 18.2 (0.3) / 41.4 (0.2) / 10.3 (0.2) / 11.6 (0.2) / 16.9 (0.18) / 10.2 (0.4)
- Warm Start: 15.5 (0.3) / 35.0 (1.2) / 9.4 (0.0) / 9.9 (0.1) / 16.3 (0.28) / 9.9 (0.3)

**(d) Code link.** No code link for the method is printed. The only GitHub URL, https://github.com/ej0cl6/deep-active-learning, is a reference to third-party active-learning repositories. It returned HTTP 403 via proxy and was not checked further.

---

## 8. L2 Init — Kumar, Marklund, Van Roy (arXiv 2308.11958 v3)

**(a) Mechanism.**
- "\displaystyle\mathcal{L}_{\text{reg}}(\theta)=\mathcal{L}_{\text{train}}(\theta)+\lambda||\theta-\theta_{0}||_{2}^{2},"
- "Intuitively, when the training loss \mathcal{L}_{\text{train}} becomes insensitive to particular parameters, these parameters drift toward their initial values, preparing them to adapt quickly to future tasks."
- "The initial parameters that L2 Init regresses towards are the neural network weights drawn from this distribution at the beginning of training."

**(b) Ablations** (Section 5.3 and Appendix A.2). All are figure-only; no numbers are printed in the text.
- Regularise toward a resampled random point instead of θ₀ (Fig. 4): "We find that regularizing towards the initial parameters rather than sampling a new set of parameters at each time step performs much better." Fig. 4 caption: "L2 Init + Resample performs poorly on all environments, especially on Random Label MNIST and 5+1 CIFAR where it loses plasticity."
- L1 instead of L2 distance (Fig. 4): "\displaystyle\mathcal{L}_{\text{reg}}(\theta)=\mathcal{L}_{\text{train}}(\theta)+\lambda||\theta-\theta_{0}||_{1}". Result: "L1 Init matches the performance of L2 Init on Random Label MNIST and performs slightly worse on Permuted MNIST and 5+1 CIFAR."
- Wider network (Fig. 5): "We find that L2 Init’s effectiveness is not diminished by increased network width, as shown in Figure 5." Deeper network (Fig. 9): "We find that L2 Init’s effectiveness is not diminished by increased network depth".
- Initialisation scheme (Fig. 10): "The performance of L2 Init is better with the PyTorch Default initialization relative to other initialization schemes. However, L2 Init consistently mitigates plasticity loss regardless of initialization scheme."
- Optimiser, SGD vs Adam (Fig. 6): "Unlike when using Adam, L2 Init does not outperform all methods on 5+1 CIFAR. Instead, Layer Norm performs the best on this problem."
- Against L2 toward zero: "While L2 significantly mitigates plasticity loss on Permuted MNIST, there is still large plasticity loss on Random Label MNIST, Random Label CIFAR, and 5+1 CIFAR as compared to L 2 Init."

**(c) CIFAR-100 class-incremental.** None. "5+1 CIFAR" draws from CIFAR-100 but is scored by average online task accuracy, not as class-incremental: "Data is drawn from the CIFAR 100 dataset, and a hard task is characterized by seeing (image, label) data pairs of 5 CIFAR 100 classes, whereas in an easy task, data from from only a single class arrives."
The paper describes it as follows: "Note that this is a highly synthetic environment designed to stress test methods which mitigate plasticity loss."

**(d) Code link.** None printed. The paper mentions "the implementation in the public GitHub repository" of Continual Backprop without a URL.

---

## 9. ReDo — Sokar et al. (arXiv 2302.12902 v2)

**(a) Mechanism.**
- "s^{\ell}_{i}=\frac{\mathbb{E}_{x\in D}|h^{\ell}_{i}(x)|}{\frac{1}{H^{\ell}}\sum_{k\in h}\mathbb{E}_{x\in D}|h^{\ell}_{k}(x)|}" (Eq. 1). "We say a neuron i in layer \ell is \tau -dormant if s^{\ell}_{i}\leq\tau ."
- "The main idea of ReDo, outlined in Algorithm 1, is rather simple: during regular training, periodically check in all layers whether any neurons are \tau -dormant; for these, reinitialize their incoming weights and zero out the outgoing weights."
- "For agents trained with ReDo, we use a threshold of \tau=0.1 , unless otherwise noted, as we found this gave a better performance than using a threshold of 0 or 0.025 ."

**(b) Ablations.** These are figure-only unless noted.
- Neuron selection (Fig. 15): "(1) Random: neurons are selected randomly, and (2) Inverse ReDo: neurons with the highest scores according to Equation 1 are selected." Result: "As Figure 15 shows, recycling active or random neurons hinders learning and causes performance collapse."
- Outgoing weights random vs zero (Fig. 22): "The random initialization of the outgoing connections leads to a lower performance than the zero initialization." Incoming weights rescaled vs re-drawn (Fig. 23): "We observe that this strategy has a similar performance to the random weight initialization strategy, as shown in Figure 23."
- Leaky ReLU (Fig. 21): "using leaky ReLU slightly decreases the number of dormant neurons but does not mitigate the issue."
- Batch size for the dormancy score (Fig. 24): "the identified percentage of dormant neurons is approximately the same using different batch sizes."
- ReDo score vs Continual Backprop utility (Fig. 25): "Results shown in Figure 25 show that both metrics achieve similar results."
- ReDo vs Reset and weight decay (Figs. 13–14): figure-only.
- Width (SAC, Ant-v2), Table 6, "Performance of SAC on Ant-v2 using using half and a quarter of the width of the actor and critic networks." Transcription:
  - width 0.25: SAC 2016.18 ± 102, SAC+ReDo 2114.52 ± 212
  - width 0.5: SAC 3964.04 ± 953, SAC+ReDo 4471.61 ± 648
- Hyperparameter grid: "We searched over the grids [1000, 10000, 100000] and [0, 0.01, 0.1] for the recycling period and \tau -dormant, respectively."

**(c) CIFAR-100 class-incremental.** None. The only supervised experiment is CIFAR-10 with shuffled labels (Fig. 3).

**(d) Code link.** Printed: "https://github.com/google/dopamine/tree/master/dopamine/labs/redo." HTTP 403 via proxy.
`git ls-remote https://github.com/google/dopamine` resolves, HEAD 5873f5494ee0c2d7c016d0ab2ad530354fec59d0. The
`labs/redo` subpath was not checked.

---

## 10. Continual backprop — Dohare et al. (Nature 2024; arXiv 2306.13812 v3)

**(a) Mechanism** (Nature Methods).
- "Continual backpropagation selectively reinitializes low-utility units in the network."
- Nature Eq. 1, as printed in the page's LaTeX: "{{\bf{u}}}_{l}[i]=\eta \times {{\bf{u}}}_{l}[i]+(1-\eta )\times | {{\bf{h}}}_{l,i,t}| \times \mathop{\sum }\limits_{k=1}^{{n}_{l+1}}| {{\bf{w}}}_{l,i,k,t}| ,"
- "When a hidden unit is reinitialized, its outgoing weights are initialized to zero." … "Every step, a fraction of mature units ρ, called the replacement rate, is reinitialized in every layer."

**(b) Ablations.**
- Replacement rate (class-incremental CIFAR-100, Extended Data Fig. 1b): "Test accuracy of continual backpropagation for different values of the replacement rate parameter with contribution utility and 1,000 maturity threshold."
  Figure-only. The grid is given in the text: "For continual backpropagation, we tested values for the maturity threshold in {1,000, 10,000} and for the replacement rate in {10−4, 10−5, 10−6} using the contribution utility described in equation (1). A maturity threshold of 1,000 and a replacement rate of 10−5 resulted in the best performance."
- Utility measure components (arXiv v3 Appendix D, slowly-changing regression, Fig. 12): "We also compare our utility measure with random utility and weight-magnitude-based utility." Result: "The results show that all the components of our utility measure are needed for the best performance. They also show that our utility measure performs significantly better than random utility and weight-magnitude utility."
- Running-average vs instantaneous utility (Extended Data Fig. 5d): "Comparison of two forms of utility in continual backpropagation, when using a running estimate of instantaneous utility and when using just the instantaneous utility. Both variations have similar performance."
- CBP vs ReDo (Ant-v3, Extended Data Fig. 5b): "The performance of PPO with ReDo and L2 regularization worsens over time, whereas PPO with continual backpropagation and L2 regularization keeps improving over time."
- Sensitivity (PPO): "We found that the performance of PPO with continual backpropagation and L2 regularization was sensitive to the replacement rate but not to the maturity threshold and weight decay."
- L2 and Shrink and Perturb compared with CBP (Online Permuted MNIST, Extended Data Fig. 4): "Shrink and Perturb and continual backpropagation have an extra advantage over L2 regularization: they inject randomness into the network."

**(c) CIFAR-100 class-incremental** (Nature only; this is not the standard protocol).
- "We continued training on the old classes (unlike in most work in class-incremental learning) to focus on plasticity rather than on forgetting."
- "Note that the network is trained on all data from all classes available at present." There is no replay buffer limit.
- Setup: 18-layer ResNet, classes added five at a time, "SGD with a momentum of 0.9, a weight decay of 0.0005 and a mini-batch size of 90."
- Headline, method: "The final accuracy of continual backpropagation on all 100 classes was 76.13%".
- Base system: "By the end, when all 100 classes were available, the accuracy of the incrementally trained base system was 5% lower than the retrained network".
- Strongest baseline (Shrink and Perturb): the text prints no number for it. "Loss of plasticity was less severe when Shrink and Perturb was added to the learning algorithm (in the incrementally trained network) and was eliminated altogether when continual backpropagation (see the ‘Maintaining plasticity through variability and selective preservation’ section) was added."
- Fig. 2 caption (verbatim, part): "Initially, accuracy is improved by incremental training compared with a network trained from scratch, but after 40 classes, accuracy degrades substantially in a base deep-learning system, less so for a Shrink and Perturb learning system and not at all for a learning system based on continual backpropagation." … "All results are averaged over 30 runs; the solid lines represent the mean and the shaded regions correspond to ±1 standard error."

**(d) Code link.** Printed (Nature "Code availability"): "The code is available at https://github.com/shibhansh/loss-of-plasticity."
HTTP 403 via proxy. `git ls-remote` resolves, HEAD a6b79580d85f3025bdb601566d3627c5f489f13b.

---

## 11. Mammoth `models/second_order.py` → Porrello et al., ICLR 2025 (arXiv 2405.16350 v3)

**Identification.** The file header of `models/second_order.py` at commit e75a491 has only a copyright line and cites
no paper. The file's own argument help names the two algorithms: "Tune with ITA or IEL"; "Beta parameter of IEL (Eq. 18/19)"; "Alpha parameter of ITA (Eq. 11)".

The repository's `REPRODUCIBILITY.md` maps the model to them:
- "The model is `second_order` with `use_iel=1`." (row IEL)
- "The model is `second_order` with `use_iel=0`." (row ITA)

`docs/related/our_papers.rst` lists "A Second-Order Perspective on Model Compositionality and Incremental Learning" (ICLR 2025 Spotlight). The arXiv title search gave 2405.16350, and the title matches.

**(a) Mechanism.**
- ITA (Eqs. 11–12): "\displaystyle\quad\mathop{\mathbb{E}}_{\bm{x},\bm{y}\sim p_{t}(\bm{x},\bm{y})}\left[\ell_{\operatorname{cur}}(\bm{\theta}_{t}|\bm{x},\bm{y})\right]+\frac{\alpha}{2}\operatorname{EWC}_{\bm{\theta}_{0}}(\bm{\theta}_{t})" with "\displaystyle\operatorname{EWC}_{\bm{\theta}_{0}}(\bm{\theta}_{t})={{\textstyle\sum}}_{i}^{|\theta|}\hat{\mathrm{F}}_{\bm{\theta}_{0}}^{(i)}(\bm{\theta}_{t}^{(i)}-\bm{\theta}_{0}^{(i)})^{2}."
- "In a sense, our term prevents forgetting pre-training knowledge; however, while our anchor is fixed at \bm{\theta}_{0} , the anchor of EWC instead shifts and focuses on the weights learned during the preceding task."
- "ITA builds upon Eq. 11 (i.e., the additional EWC-like term computed w.r.t. \bm{\theta}_{0} ), while IEL exploit Eqs. 18 and 19 to train the composed model."

**(b) Ablations.**
- Removing the regulariser, or applying it only on the classifier. Table 2, "For ITA, analysis of the impact of the proposed regularization loss (FA [ \uparrow ])." Transcription of final accuracy, columns IN-R / C-100 / CUB / Caltech / MIT / RESISC / CropDis.:

| row | IN-R | C-100 | CUB | Caltech | MIT | RESISC | CropDis. |
|---|---|---|---|---|---|---|---|
| ITA-FFT (reg) | 76.43 | 89.38 | 84.80 | 92.32 | 85.35 | 80.50 | 91.81 |
| without Eq. 12 reg. | 8.61 | 17.59 | 10.47 | 12.76 | 12.01 | 17.17 | 20.64 |
| Eq. 12 only on CLS | 76.00 | 87.60 | 83.54 | 91.04 | 81.45 | 75.26 | 77.00 |
| ITA-LoRA (reg) | 77.79 | 89.96 | 85.55 | 92.65 | 86.60 | 82.00 | 95.85 |
| without Eq. 12 reg. | 50.17 | 66.58 | 60.58 | 74.87 | 52.74 | 37.59 | 55.86 |
| Eq. 12 only on CLS | 77.33 | 90.03 | 85.55 | 92.59 | 84.86 | 80.64 | 96.22 |

  Text: "applying Eq. 12 is beneficial for all examined fine-tuning strategies; ii) although regularizing all layers is the most consistent approach, applying Eq. 12 only on the classification head already yields good accuracy."
- Table 6, "Ablation study for ITA-(IA)3 and IEL on several benchmarks (FA [ \uparrow ])". Transcription, same columns:

| row | IN-R | C-100 | CUB | Caltech | MIT | RESISC | CropDis. |
|---|---|---|---|---|---|---|---|
| ITA-(IA)3 (reg) | 77.04 | 90.66 | 85.67 | 92.67 | 84.74 | 83.73 | 95.41 |
| without Eq. 12 reg. | 71.82 | 88.43 | 77.61 | 90.66 | 69.14 | 69.01 | 63.72 |
| Eq. 12 only on CLS | 76.72 | 90.48 | 85.56 | 92.56 | 85.25 | 84.37 | 95.45 |
| IEL-FFT (reg) | 80.09 | 89.38 | 84.89 | 92.23 | 82.79 | 81.42 | 95.83 |
| without Eq. 19 reg. | 40.85 | 52.56 | 14.02 | 53.76 | 47.63 | 39.20 | 31.24 |
| Eq. 19 reg. only on CLS | 77.99 | 85.82 | 85.30 | 91.43 | 77.58 | 76.87 | 96.18 |
| IEL-LoRA (reg) | 79.93 | 89.53 | 84.95 | 92.19 | 84.49 | 82.53 | 95.88 |
| without Eq. 19 reg. | 51.15 | 66.01 | 60.39 | 70.71 | 55.38 | 42.72 | 45.25 |
| Eq. 19 reg. only on CLS | 76.14 | 86.11 | 84.43 | 91.77 | 82.50 | 70.05 | 95.54 |
| IEL-(IA)3 (reg) | 77.86 | 89.72 | 84.57 | 92.70 | 85.54 | 81.50 | 95.68 |
| without Eq. 19 reg. | 73.72 | 84.00 | 74.72 | 89.58 | 69.82 | 62.52 | 66.29 |
| Eq. 19 reg. only on CLS | 77.23 | 89.38 | 84.70 | 92.76 | 85.43 | 81.60 | 95.72 |

- Implementation choice: "we apply this decoupled gradient update exclusively to LoRA and (IA)3. For full fine-tuning, we refrain from using it as we observed numerical instabilities (i.e., exploding loss)."

**(c) CIFAR-100 class-incremental.**
- Setting: "Split CIFAR-100 (Krizhevsky et al., 2009) (10 tasks \times 10 classes)". All methods use "a ViT-B/16 (Dosovitskiy et al., 2021) with supervised pre-training on ImageNet21K".
- Table 1, "Comparison with SOTA (Final Accuracy [ \uparrow ]). Best results in bold, second-best underlined. EWC, LwF-MC, DER++ (buffer size of 1,000 examples), SEED, and TMC rely on full fine-tuning; L2P, CODA, and APT utilize prompt-based learning. Finally, InfLoRA adopts LoRA fine-tuning."
- Transcription of the C-100 column. Bold is not recoverable from the text extraction; underline marks survive as `\underline{}`.
  - Joint 91.74; Finetune 21.57; EWC 73.49; LWF-MC 72.16; DER++ 83.02; L2P 87.32; CODA 86.48; SEED 83.39; APT 86.19; InfLoRA 87.17; TMC 78.42.
  - ITA-FFT 89.38; ITA-LoRA 89.96 (underlined); ITA-(IA)3 90.66; IEL-FFT 89.38; IEL-LoRA 89.53; IEL-(IA)3 89.72.
  - The strongest printed non-proposed method on C-100 is L2P at 87.32. Its buffer is none; DER++ has a buffer of 1,000.
- "the results are averaged over three runs, see Sec. H.2"

**(d) Code link.** Printed in the abstract: "Code available at https://github.com/aimagelab/mammoth." HTTP 403 via proxy.
`git ls-remote` resolves, HEAD e75a491c69fd729edeb01431afb753d9157d9a81, the same commit as the local clone.

---

## 12. Wang, Zhang, Su, Zhu survey (arXiv 2302.00487 v3) — mechanism taxonomy and CIFAR-100 tables

**(a) Classification by mechanism.**
- "A number of continual learning methods have been proposed in recent years for various aspects of machine learning, which can be conceptually separated into five groups (see Fig. 1, c): adding regularization terms with reference to the old model (regularization-based approach); approximating and recovering the old data distributions (replay-based approach); explicitly manipulating the optimization programs (optimization-based approach); learning robust and well-distributed representations (representation-based approach); and constructing task-adaptive parameters with a properly-designed architecture (architecture-based approach)."
- IV-A: "The first is weight regularization, which selectively regularizes the variation of network parameters." … "The second is function regularization, which targets the intermediate or final output of the prediction function." … "Interestingly, these importance measurements have been shown to be all tantamount to an approximation of the FIM [34], although stemming from different motivations."
- IV-C: "A typical idea is to perform gradient projection. Some replay-based approaches such as GEM [281], A-GEM [66], LOGD [411] and MER [369] constrain parameter updates to align with the direction of experience replay, corresponding to preserving the previous input space and gradient space with some old training samples."
- The EWC form used by the survey: "\mathcal{L}_{{\rm{EWC}}}(\theta)=\ell_{k}(\theta)+\frac{\lambda}{2}(\theta-\mu_{k-1})^{\top}\hat{F}_{1:k-1}(\theta-\mu_{k-1})," (Eq. 12)
- IV-E: "Previous work generally separates this category into parameter isolation and dynamic architecture, depending on whether the network architecture is fixed or not."

**(b) Ablations.** Not applicable (survey). No ablation reported.

**(c) CIFAR-100 class-IL results table.** v3 contains no numeric results table. Its three tables are qualitative:
- "TABLE I: A formal comparison of typical continual learning scenarios."
- "TABLE II: Summary of representative CIL methods with the use of experience replay."
- "TABLE III: Summary of TFCL, OCL and GCL (both TFCL and OCL) methods."

**(d) Code link.** None printed.

---

## 13. van de Ven, Tuytelaars, Tolias, *Three types of incremental learning* (NMI 2022) — class-IL table

**Protocol.**
- "For the Split CIFAR-100 protocol, the CIFAR-100 dataset67 was split up into ten contexts, such that each context contained ten image classes."
- Class-IL output layer: "For the other two scenarios, single-headed output layers were used, with the number of output units equal to the number of classes per context (domain-incremental learning) or to the total number of classes (class-incremental learning)."

**Table 3, "Results on Split CIFAR-100".** Caption and footnote, verbatim:
- "Reported is the final test accuracy (as percentage, averaged over all contexts) of all compared methods on the Split CIFAR-100 protocol, which is performed according to all three scenarios."
- "The column ‘Budget’ indicates the number of examples per class that was allowed to be stored in a memory buffer."
- "Each experiment was performed 10 times with different random seeds, reported is the mean (±s.e.m.) over these runs. All compared methods used convolutional layers that were pre-trained on CIFAR-10, see Methods for full details."

Transcription of the Class-IL column (Budget, GM, value):

| strategy | method | budget | GM | Class-IL |
|---|---|---|---|---|
| Baselines | None – lower target | - | - | 7.71 (±0.18) |
| Baselines | Joint – upper target | - | - | 49.78 (±0.21) |
| Parameter regularization | EWC | - | - | 8.24 (±0.25) |
| Parameter regularization | SI | - | - | 8.10 (±0.24) |
| Functional regularization | LwF | - | - | 25.57 (±0.27) |
| Replay | DGR | - | Yes | 9.67 (±0.22) |
| Replay | BI-R | - | Yes | 25.81 (±0.41) |
| Replay | ER | 100 | - | 37.57 (±0.21) |
| Replay | A-GEM | 100 | - | 20.38 (±1.45) |
| Template-based classification | Generative Classifier | - | Yes | 46.83 (±0.18) |
| Template-based classification | iCaRL | 100 | - | 37.83 (±0.21) |

Separate Networks and XdG print "-" for Class-IL. The footnote also says: "Note that we were not able to run the method FROMP on this protocol due to its high computational costs."

**(d) Code link.** Printed: "Documented code that can be used to reproduce or build upon the reported experiments is available online under an MIT licence"
The URL is https://github.com/GMvandeVen/continual-learning. HTTP 403 via proxy. `git ls-remote` resolves, HEAD
e6d795aa81b9cef742b8de76cb71222d4d1ce00b. A Zenodo DOI, 10.5281/zenodo.7189378, is also cited; https://doi.org
returned HTTP 302 (redirect, not followed).

---

## 14. Mammoth (local clone, commit e75a491c69fd729edeb01431afb753d9157d9a81)

sha256 of the files read:
- README.md: 769f146af10f54a8588fb3ee7c086af9f8c45f40d5c7f1852ce4c512ceb9e494
- REPRODUCIBILITY.md: 18c6f953779566533b1ad778a1324a0d40f38c658cb17299d182e6379415e7c0
- models/second_order.py: fad56e69cb8f1eb6fd893cf24057e144f34c2109bb728d4cfea3df5d03bcab70

**README lines matching online / n_epochs / joint / reproducibility, verbatim.** A case-insensitive grep found no
line containing "n_epochs" or "epoch" in README.md.
- l.162: "Joint training for the General Continual setting: `joint_gcl` (_only for General Continual_)."
- l.173: "Online Continual Learning on a Contaminated Data Stream with Blurry Task Boundaries (PuriDivER): `puridiver`."
- l.174: "online Elastic Weight Consolidation (oEWC): `ewc_on`."
- l.247: "We take great pride and care in the reproducibility of the models in Mammoth and we are commited to provide the community with the most accurate results possible. To this end, we provide a _REPRODUCIBILITY.md_ file in the repository that contains the results of the models in Mammoth."
- l.249: "The performance of each model is evaluated on the same dataset used in the paper and we report in _REPRODUCIBILITY.md_ the list of models that have been verified. We also provide the exact command used to train the model (most times, it follows `python main.py --model <model-name> --dataset <dataset-name> --model_config best`)."
- l.253: "**Disclaimer**: Since there are many models in Mammoth (and some of them predate PyTorch), the process of filling the _REPRODUCIBILITY.md_ file is ongoing."
- l.257: "No! It means that we have not yet found the appropriate dataset and hyperparameters to fill the file with the results of that model."

**n_epochs, from the docs** (`docs/getting_started/validation.rst`): "This is the default option, for which training stops after a fixed number of **epochs**. The number of epochs can be set using the ``--n_epochs`` command line argument."

**REPRODUCIBILITY.md rows for the methods in this dossier, verbatim** (row text as printed; V = verified, X = not):
- "| A-GEM                     | `agem`                   | X         |       |"
- "| EwC Online                | `ewc_on`                 | X         |       |"
- "| GEM                       | `gem`                    | V         | Original work requires too much resources. We reproduced the results in `Dark Experience for General Continual Learning: a Strong, Simple Baseline`. |"
- "| SI                        | `si`                     | X         |       |"
- Row Joint (`joint`), N/A. The note cell reads "There is no single paper for the" followed by the word joint in escaped double quotes and " model." It is not quoted whole because of the embedded quote characters.

MAS, ReDo, L2 Init, shrink-and-perturb and continual backprop do not appear in the README model list or in
REPRODUCIBILITY.md at this commit. This is a grep result; the files were not read line by line for synonyms.

**Citing the library** (README): the BibTeX entries are `boschini2022class` ("Class-Incremental Continual Learning into the eXtended DER-verse", IEEE TPAMI 2022) and `buzzega2020dark` ("Dark Experience for General Continual Learning: a Strong, Simple Baseline", NeurIPS 33). Neither paper was fetched.

---

## Quote check

The check was run on 2026-09-25 with `quotecheck.py` in the scratchpad folder `lit0925/clsota/reg/`.

**Corpus.** Every saved text in that folder:
- the arXiv abstract pages, stripped to text;
- the arXiv HTML extractions, with the math alt-text inline;
- the PDF extractions;
- the Nature and NMI article, PDF and table-page extractions;
- the Mammoth README, REPRODUCIBILITY.md, `second_order.py` and the two docs files.

**Normalisation.** Each text was HTML-unescaped and its whitespace was collapsed. PDF line-end soft hyphens
(U+FFFE) were joined, with the whitespace after them removed. Nothing else was changed.

**Rule.** Every straight-double-quoted string of 20 characters or more in this file was matched as a substring
against the normalised corpus.

**Counts.**
- Quoted strings in the file: 201. Of these, 187 are 20 characters or longer and 14 are shorter.
- Found verbatim: 187 of 187.
- Not found: 0.

The first run flagged 6 strings, and these fixes were made:
- Five were abstract-page comment and journal-reference fields that had not yet been added to the corpus. They are
  verbatim once the abstract pages are included.
- One was a title given in the request, not in any source. It was taken out of quotes.

**Separate numeric check.** Every decimal number written in this file (421 distinct values) occurs in at least one
saved source text. This check finds a number that is absent from every source. It does not find a number that
appears in some source but was put in the wrong table cell.
