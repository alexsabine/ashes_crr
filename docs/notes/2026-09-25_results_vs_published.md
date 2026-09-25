# Our continual-learning results beside the published findings (2026-09-25)

**Status.** A note to the auditor, not evidence (R8). Owner request: prompt-log entry 177. No verdict is changed; ledger
rows are append-only.

**Where the numbers come from.**
- Every repository number here is printed by `Continuous_Learning/checks/results_vs_literature.py`. That script reads the
  pinned per-run records of EQ2, EQ3, EQ4, SEC1 and SCL3, runs nothing new, and its output is pinned beside it
  (`results_vs_literature.txt`, CI-checked).
- It reproduces the ledger's own margins and steps. Examples: EQ2-1 is +3.30, +2.10 and +2.78 with steps 1.00, 3.51 and
  3.61. EQ3-1 is +3.90 on mfeat_factors and −3.74 on fars. SCL3 cnae-9 is −21.98 with a step of 1.73.
- The published numbers are in `docs/citations/classil_benchmarks_2026-09-25.md`, fetched on the day. The Pareto and method
  literature is in the three dossiers of 2026-09-25.

## 1. Is the equanimity rule published, and do our passes do anything different?

**The rule.**
- At Ω = 1 and for two terms, the rule steps along the bisector of the unit gradients.
  - That is the direction of three published methods: Nash-MTL's two-task solution, IMTL-G, and MGDA on normalised
    gradients (`pareto_identities.txt`).
  - MEGA-II (2019/2020) takes the same bisector in continual learning, with the step fixed at the present gradient's length.
- The rule differs only in its step scale (the present gradient's length, bounded by (1 + Ω) times it), an EMA inside the
  ratio, and a cap.
- The mechanism our reports credit for its wins, the step bound, is shared by MEGA-II.

**What our studies actually compared.**
- **Published rules we did run** (EQ2–EQ4, 15 carriers): A-GEM, GradNorm and MEGA-I, each as implemented in our scorers.
  The rule is ahead of A-GEM on 13, of GradNorm on 10 and of MEGA-I on 13 of the 15. GradNorm scores 0.00 where it
  diverged.
- **The closest published equivalents were never run as arms.** These are MEGA-II and the normalised two-term sum
  (Nash-MTL/IMTL-G). So the record does not show that the rule does anything they would not. That question is untested,
  and the mathematics says to expect a tie up to step length.
- **SCL3's method (SEC)** is the textbook Laplace weight plus a secant calibration of the Fisher. The 2026-09-25 checks did
  not search for prior art on the secant calibration itself. Its novelty is therefore unknown, not established.

## 2. Our numbers beside the published class-incremental regime

**The published reference points** (split MNIST, 5 two-class tasks, class-incremental; van de Ven & Tolias, arXiv 1904.07734
v1, Table 4; Hsu et al., arXiv 1810.12488 v4, Table 2):
- EWC, online EWC, SI and MAS sit at 19.52–20.01 %. That is the "no method" lower bound (19.46–19.90), the level of a
  learner that knows only the last task.
- LwF reaches 23.85–24.17.
- Replay reaches 90.78–90.79.
- Offline training reaches 97.53–97.94.
- In van de Ven and Tolias's words, the regularisation methods "completely failed in the Class-IL scenario". Only replay
  obtained "good performance (above 90%)".

**The same reference points for every carrier we scored** (37 carrier-scorings over five studies; means over seeds, the
registered primary cell):

| what | our record |
|---|---|
| replay against the rule | ER, the best fixed replay weight, is ahead of the rule on **15 of 15** carriers that had a replay arm. Median gap **39.70 points**; DER++ **44.05** |
| LwF against EWC | LwF (best weight) is ahead of the tuned EWC λ on **14 of 15**. That is the published ordering |
| the rule and the last-task floor | the rule is within 5 points of its carrier's last-task floor on **13 of 37**, and below it on **11** |
| what tuning buys | the tuned EWC λ gains a median **5.14** points over the near-fine-tune arm (λ = 0.1), at most 25.47 |
| the rule against EWC | median **+5.03** over λ = 0.1; median **−0.60** against the tuned λ |
| SEC | a median **7.83** points above its floor (22 carrier-scorings); within 5 points of the floor on **9** |
| the tuned λ against the Bayes weight | from 0.212766 to 28300, against the Bayes weight of 1/2. That is Hsu et al.'s "wide gap between their worst and best performance", and the plasticity dossier's report of tuned weights far above Bayes (GVCL) |

**Reading (inference).** Our results reproduce the published class-incremental picture: replay ≫ LwF > the regularisers,
which sit near the last-task floor.
- On several tabular carriers the regularisers do retain real accuracy above the floor, which split MNIST does not show.
  Examples: mfeat_factors (rule 58.35 against a floor of 20.00) and isolet (SEC 62.40 against 20.00).
- Every pass we have is a comparison **inside the regularisation family**: the rule or SEC against a tuned EWC λ. That
  family trails plain replay by about 40 points on the carriers where both ran.
- The passes are real within that family, and small against the method the literature says works.

## 3. Inert carriers: where "not behind the tuned λ" is automatic

Call a carrier-scoring **inert** when the tuned EWC λ is within one resolvable step of the near-fine-tune arm (λ = 0.1).
There, tuning the weight moves nothing, so any arm is "not behind" it.
- **13 of the 37 carrier-scorings are inert:** EQ3 krkopt, led24 and led7; EQ4 satimage, sleep and wine_quality_white;
  SEC1 krkopt, satimage, sleep and wine_quality_white; SCL3 first-order-theorem-proving, wall-robot-navigation and
  GesturePhaseSegmentationProcessed.
- **What that does to the passes, read against the ledger** (no verdict changed; the criteria were scored as registered):
  - **EQ3-1**: 5 of 6 "not behind". Three of the five (krkopt, led24, led7) are inert. On the load-bearing carriers the
    rule is ahead on mfeat_factors and mfeat_morphological and behind on fars.
  - **EQ4-I** (PASS-0, satimage alone): satimage is inert (tuned − λ 0.1 = 0.20 against a step of 1.62). The invariance
    criterion "not behind the tuned λ" is therefore near-automatic there. The rule itself is 4.83 points above the tuned
    λ on satimage (27.67 against 22.84), which is not automatic.
  - **SCL3-3**: 9 of 10. Three of the nine (first-order-theorem-proving, wall-robot-navigation,
    GesturePhaseSegmentationProcessed) are inert. On first-order-theorem-proving every arm sits near 11.7, below chance
    (16.67). On the seven load-bearing carriers SEC is not behind on six (cnae-9 behind).
  - **SCL3-2** ("no harm outside M"): three of its four carriers are inert (first-order-theorem-proving, GesturePhase,
    wall-robot). Only eucalyptus is load-bearing.
  - **EQ2-1b, EQ3-I, SCL3-1 and SCL3-4** rest on load-bearing carriers. SCL3-4 is the span of tuned λ, which is not a
    per-carrier comparison.
- **Why this was missed.** EQ3's prereg had a load-bearing rule for its constraint-control cells (EQ3-4). No study applied
  one to its main "not behind" row.

## 4. What should change in any further continual-learning prereg (proposals; the owner decides)

1. **Reference arms from the published protocol:** plain fine-tuning (λ = 0), offline joint training (upper bound) and
   replay (ER-sum). Also print the last-task floor. A PASS then reads against where the method family actually stands.
2. **A pre-registered load-bearing criterion for every "not behind" row.** Inert carriers are counted and reported, not
   scored as passes.
3. **The closest published equivalents as arms:** MEGA-II, the normalised two-term sum, and the VQGAN weight. These are
   required before any claim that the rule adds anything beyond them (R7).
4. **A prior-art search on the secant calibration** before SEC is described as the repository's method.
