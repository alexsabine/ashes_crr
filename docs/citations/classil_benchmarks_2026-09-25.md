# Class-incremental benchmark reference points, checked on the day (R10), 2026-09-25

**Status.** Owner request: prompt-log entry 177. This file is the source record for the published numbers in
`docs/notes/2026-09-25_results_vs_published.md`. Nothing here is a result.

**Access.** Both papers were fetched with `curl` on 2026-09-25:
- the arXiv abstract pages, which give the submission histories;
- the arXiv HTML full text for Hsu et al.;
- the ar5iv rendering for van de Ven and Tolias. That paper's arXiv HTML page returned no article, because arXiv has no
  HTML build for that version.

The raw files are in the session scratchpad under `lit0925/results/`, and the quotes below were matched against them.
No 404s.

| work | version and date | URL | what was read | tag |
|---|---|---|---|---|
| van de Ven GM, Tolias AS. *Three scenarios for continual learning.* | arXiv 1904.07734 v1, 15 Apr 2019 (the only version on arXiv). The 2022 Nature Machine Intelligence paper by van de Ven, Tuytelaars and Tolias is a different publication and was not read | https://arxiv.org/abs/1904.07734 ; full text https://ar5iv.labs.arxiv.org/html/1904.07734 | Table 4 (split MNIST, 20 seeds, mean ± SEM) and its discussion | [F] |
| Hsu Y-C, Liu Y-C, Ramasamy A, Kira Z. *Re-evaluating Continual Learning Scenarios: A Categorization and Case for Strong Baselines.* | arXiv 1810.12488 v4, 23 Jan 2019 (v1 30 Oct 2018) | https://arxiv.org/abs/1810.12488 ; full text https://arxiv.org/html/1810.12488v4 | Table 2 (split MNIST, 10 runs) and its discussion | [F] |

## The numbers used (split MNIST, class-incremental, 5 tasks of 2 classes, average accuracy over all classes, %)

| method | van de Ven & Tolias, Table 4 | Hsu et al., Table 2 |
|---|---|---|
| no continual-learning method ("None – lower bound"; "SGD") | 19.90 | 19.46 |
| EWC | 20.01 | 19.80 |
| online EWC | 19.96 | 19.77 |
| SI | 19.99 | 19.67 |
| MAS | — | 19.52 |
| L2 | — | 22.52 |
| LwF | 23.85 | 24.17 |
| replay (DGR; naive rehearsal) | 90.79 | 90.78 |
| offline (upper bound) | 97.94 | 97.53 |

## Quotes (verbatim from the fetched text)

- **van de Ven & Tolias (v1).** "All of the tested methods performed well in the Task-IL scenario, but LwF and especially
  the regularization-based methods (EWC, Online EWC and SI) struggled in the Domain-IL scenario and completely failed in the
  Class-IL scenario. Importantly, only methods using replay (DGR, DGR+distill and iCaRL) obtained good performance (above
  90%) in the Domain-IL and Class-IL scenarios."
- **Hsu et al. (v4), first quote.** "naive rehearsal achieves performance similar to state-of-the-art methods with the same
  space overhead, and performs much better than online EWC and SI, especially in the incremental class scenario"
- **Hsu et al. (v4), second quote.** "EWC and SI variants require significant hyper-parameter tuning, with a wide gap between
  their worst and best performance"

## Reading (inference, labelled)

In class-incremental learning with 5 two-class tasks, the regularisers sit at the "last task only" floor of 20%, which is
the lower bound. Replay sits near 91%. The ordering is replay ≫ LwF > regularisers ≈ no method.

This repository's tabular studies use the same protocol:
- class-incremental;
- two classes per task;
- one shared head;
- final accuracy over all classes.

So these numbers are the right reference points for them. The datasets and networks differ, so the absolute numbers are
not comparable. The ordering and the floor are.
