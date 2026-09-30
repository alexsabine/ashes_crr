# SEC_Analysis declaration: why SEC4 passed and SEC5 did not (P1 of `Applied_Suite/PROGRAMME.md`; pushed before any analysis code)

**The request.** Prompt-log entry 257: "Sec4 was successful so we should run a full crr analysis on it to find out
precisely why it worked."

**Status.**
- This is a post hoc analysis of records already opened. It adds no ledger row.
- Its numbers come from `checks/*.py` with pinned outputs (R1).
- Its words are computed from those numbers (R15).
- The mechanism checks M0–M4 are new runs on the 30 carriers of SCL3, SEC3, SEC4 and SEC5. Every one of those carriers is
  now SEEN, so these checks are declared checks on seen data, not a test.
- Anything P1 suggests goes into a fresh pre-registration (P2, SEC6) and is tested there on unseen carriers, on a later
  day (R3).

## What is analysed (fixed now)

**The run records.** `runs/{sec1,scl3,sec3,sec4,sec5}/results_*.jsonl`, read as they are pinned.

**The carriers.** 42 in all:

| study | carriers | data | SEC arms recorded |
|---|---|---|---|
| SEC1 | 12 | SEEN PMLB | unclipped SEC |
| SCL3 | 10 | unseen at the time | unclipped SEC |
| SEC3 | 6 scored | unseen at the time | unclipped SEC |
| SEC4 | 6 scored | unseen at the time | unclipped and clipped SEC |
| SEC5 | 8 scored | unseen at the time | unclipped and clipped SEC |

**The quantities, per carrier** (the frozen scorers' definitions, unchanged):

| symbol | definition |
|---|---|
| tuned λ\*_raw | the best mean over seeds of the `fixed` arm (the raw Fisher at weight λ, SEC1's two-stage grid) |
| step | max(1, 2 × SE over seeds) at λ\*_raw |
| λ\*_sec | the best mean of `fixed_sec` (the calibrated Fisher Σ s_j f_j at weight λ) |
| SEC | `bayes_sec` (w = 1/2 on the task-size-weighted calibrated Fisher) |
| clipped SEC | `bayes_sec_clip` (SEC4 and SEC5 only) |
| raw Laplace | `bayes` |
| one-factor SEC | `bayes_s1` (task 1's s applied to every task) |
| s_j, c_j, ρ_j | the calibration factors in each record |
| properties | d, K, n_train, per-task n, class imbalance and family, from each file's header line |

**The loader is validated first.** The shared loader (`checks/sec_lib.py`) must reproduce each study's pinned headline
counts before any analysis is read:

| study | counts to reproduce |
|---|---|
| SEC1-3 | SEC not behind 9 of 12; raw Laplace 6 of 12; the rule 8 of 12 |
| SCL3-3 | 9 of 10; raw Laplace 4 of 10; Ω = 1 7 of 10 |
| SEC3-3 | 4 of 6; raw 5 of 6 |
| SEC4-1 | 6 of 6, with its six margins |
| SEC5-1 | 4 of 8 |

**If the loader does not reproduce every pinned count, no analysis output is read** until the discrepancy is found and
logged (R14).

## The analyses (A1–A11) and forecasts, written now

The words HOLDS and FAILS against each forecast are printed by the scripts.

| id | question | the computation | forecast |
|---|---|---|---|
| **A1** | where does SEC's margin come from? | Per carrier, split SEC − tuned λ\*_raw into two parts. The **shape gain** is λ\*_sec's accuracy − λ\*_raw's: what the calibrated per-task weighting buys at the best global strength. The **location cost** is SEC − λ\*_sec's accuracy: what fixing the weight at 1/2 costs against the best multiplier of the calibrated Fisher. Both are in units of the step. | **F1.** Among the carriers where SEC is not behind, the location cost is within a step on at least 75 %. The shape gain exceeds a step on fewer than half of all carriers. SEC works mainly because 1/2 lands near the calibrated optimum, not because the calibrated shape beats the raw one. |
| **A2** | does the calibration collapse the optimum's location? | log10(λ\*_raw / 0.5) and log10(λ\*_sec / 0.5) per carrier; SD and range of each across carriers, per family and pooled | **F2.** In every family the SD of log10 λ\*_sec is at most half the SD of log10 λ\*_raw. |
| **A3** | is SEC's pass the plateau containing 1/2? | Per carrier and axis, the not-behind set: grid points within a step of the best. Report its lowest and highest grid point, its width in decades, and whether it brackets 0.5 on the calibrated axis. | **F3.** (a) The calibrated not-behind set brackets 0.5 on the carriers where SEC is not behind, and fails to bracket it where SEC is behind, on at least 90 % of the carriers. (b) The median plateau width in decades is within a factor of 2 on the two axes: the calibration moves the plateau, it does not widen it. |
| **A4** | is the calibration a units correction of the raw Fisher? | Across carriers, log10 λ\*_raw against log10(0.5 · s̄), where s̄ is the geometric mean of s over the tasks and seeds of the SEC arm. Spearman correlation and least-squares slope. Also the within-carrier SD of log10 s across tasks against the between-carrier SD. | **F4.** Spearman ≥ 0.6 and slope in [0.5, 1.5] over the 42 carriers. The median s exceeds 10 on most carriers: the empirical Fisher at a task's end understates the curvature the path showed. |
| **A5** | what kind of failure is each "behind"? | Every behind case of SEC (42 carriers) and of the clipped SEC (14) is classed in order. **D** divergence: a seed below 0.5 × the tuned mean, or non-finite. **C** cap: the clip fired and λ\*_sec lies above the not-behind set's reach at 1/2. **U** under-regularised: λ\*_sec's not-behind set lies wholly above 0.5. **O** over-regularised: it lies wholly below. **N** noise: behind by less than 2 steps with 0.5 bracketed. | **F5.** Most unclipped failures are D. Every clipped failure is C, U or N, none D. |
| **A6** | what separates divergence from stability? | Per carrier, the maximum and median s over tasks and seeds. For the clipped arms, the guard margins and firings. Diverged carriers are compared with the rest. | **F6.** The median of per-carrier max s is higher among carriers where unclipped SEC diverged than among the rest. |
| **A7** | do carrier properties predict success? | d, K, n_train, per-task n, imbalance (largest over smallest class count) and family, against SEC's and the clipped SEC's not-behind label. The best single-property threshold split and its errors. | **F7.** No single property separates: the best split misclassifies at least 3 carriers. |
| **A8** | was SEC4's family easy? | Per family: the SD of log10 λ\*_raw; a transferred λ's not-behind count (SEC4-T's leave-one-carrier-out log-median, snapped to the coarse grid), computed identically for all five studies; SEC's count; the one-factor SEC's count. | **F8.** SEC4's family has a transferred-λ not-behind share at least as high as SEC5's: part of SEC4's pass is the family's ease. |
| **A9** | why SEC4 passed and SEC5 did not, carrier by carrier | For the 14 carriers of SEC4 and SEC5: A1's parts, A5's class, s statistics, firings, guard margins and properties, side by side | **F9.** SEC5's four clipped failures have at least two distinct classes. At least one is C (volcanoes-d4) and at least one is not caused by the penalty (pokerhand's low-accuracy seeds, visible in the tuned arm too). |
| **A10** | how much of the pass count is tolerance? | Every carrier's margin (SEC − tuned λ\*_raw) in units of the step; the share of "not behind" passes with a negative margin, per family and pooled | **F10.** At least a quarter of the pooled held-out passes (unclipped SEC, 30 carriers) have a negative margin. |
| **A11** | is the explanation CRR, Bayes, optimisation or information geometry? | A code reading of `sec1_score.run()` and `sec4_score.run_guard()`. Each load-bearing ingredient is named with its published source, and whether a CRR-proper ingredient (A3/D5, A6, P2/P3, A1′/D1, H-L5, D6/H-T1, H-EQ, A7/A8; CLAUDE.md §7) is load-bearing is graded. Sources are fetched on the day with version (R10). | **F11.** No CRR-proper ingredient is load-bearing. The weight 1/2 is the Laplace (Bayes) weight. The calibration is a Barzilai–Borwein secant fixing the empirical Fisher's known scale error. The secant is a **chord** between window means, not CRR's arc. The clip is AR1's. A1′ supplies a name ("units") for the correction. Rung R1 (inherited) at best. |

## The mechanism checks (M0–M4): new runs on the 30 now-SEEN carriers, seeds 0–4

**The runner.** `checks/m_checks.py` imports the frozen `runs/sec4/frozen/sec4_score.py`, which it does not modify. Every
arm runs with SEC4's clip (κ = 0.5), so stability does not confound the comparison. Firings are reported. The carriers are
loaded by each study's own frozen loader.

| id | arm | forecast |
|---|---|---|
| **M0** | Identity. The clipped SEC reruns and must equal the pinned `bayes_sec_clip` accuracy bit for bit, on seed 0 of every SEC4 and SEC5 carrier. On SCL3 and SEC3 carriers, which have no pinned clipped record, the clipped SEC is run as the reference. | FM0: identity on 14 of 14 |
| **M1** | True-Fisher Laplace. w = 1/2 on the task-size-weighted Fisher with labels **sampled from the model** (the model Fisher: one sampled label per row, the same 50 minibatches), uncalibrated. This asks whether the known fix, "use the true Fisher, not the empirical one" (Kunstner et al.), does the calibration's job. | FM1: M1 is behind the tuned λ on more carriers than the clipped SEC |
| **M2** | Endpoint-curvature calibration. s_j = c_end / ρ_j, where c_end is the Hessian Rayleigh quotient along u = dth/‖dth‖ at the task's end: the central finite difference ⟨g(θ + εu) − g(θ − εu), u⟩ / (2ε) of the clean mean gradient over up to 1000 of the task's rows (seeded), with ε = 0.01 · ‖dth‖. This asks whether the path-averaged secant matters, or only the local curvature. | FM2: the median over tasks of c / c_end > 1; M2 is behind on more carriers than the clipped SEC |
| **M3** | One-factor SEC. Read from the pinned `bayes_s1` records, not run. It asks whether per-task factors matter or only one global scale. | FM3: `bayes_s1` is behind on more of the 42 carriers than SEC |
| **M4** | Arc secant (the one CRR-guided variant, D6-flavoured, two-sided). The task path is cut into 5 segments by 6 evenly placed windows, each of ⌈0.1 × steps⌉ steps; the first is SEC's start window and the last its end window. Then c_arc = Σ_k ⟨Δg_k, Δθ_k⟩ / Σ_k ‖Δθ_k‖² and ρ_arc = Σ_k ⟨f Δθ_k, Δθ_k⟩ / Σ_k ‖Δθ_k‖², and s = c_arc / ρ_arc. With 1 segment this is SEC exactly. SEC's fallback rule applies. | FM4: M4 is within a step of the clipped SEC on at least 80 % of carriers (a TIE: the arc adds nothing, as T1X2 found for forgetting) |

**Comparisons.** Every M arm is compared with the pinned tuned λ\*_raw and step of its carrier (not behind: arm −
tuned > −step), and with the clipped SEC run beside it.

**Words.** The words are counts and HOLDS or FAILS against the forecasts. No verdict is a PASS: these are seen carriers.

## What the results may change (fixed now)

- **Which baselines SEC6 carries.**
  - If M1 or M2 is not behind as often as the clipped SEC (at most 1 carrier fewer), SEC6 carries it as a baseline that
    could win (R7).
  - If M4 is ahead of the clipped SEC by more than a step on at least 3 carriers, SEC6 may carry M4 as a two-sided
    candidate. Otherwise M4 is recorded as a TIE or a loss and not carried.
- **What P3 and P4 may say.** They may say "SEC works because …" only in the words the pinned outputs print.

## Order

1. This declaration, `Applied_Suite/PROGRAMME.md` and AGENT_LOG 212 are pushed.
2. `checks/sec_lib.py` is written and must reproduce the pinned counts.
3. The analysis scripts are written, run and pinned, each with a byte-identical rerun.
4. The M runner is written. The M0 identity is checked before the full M run.
5. Two adversarial reviewers per analysis check each script against this declaration.
6. `WHY_SEC4_WORKED.md` is written from the pinned outputs.

## Amendment 1 (2026-09-30, after `loader_check.txt` and before any analysis output was read; pushed before A12's script exists)

**What prompted it.** The loader check prints each carrier's arm means. Several held-out carriers have a tuned-λ accuracy
near chance: for example spoken-arabic-digit 9.86 and autoUniv-au6-750 7.68 under the clipped SEC. On such a carrier,
"not behind the tuned λ" may be passing at a floor where no method learns anything. The declared analyses do not separate
this. This amendment adds one analysis. It is post hoc in origin and is labelled so in its output.

| id | question | the computation | forecast |
|---|---|---|---|
| **A12** | how much of the pass count sits at the accuracy floor? | Per carrier, the floor is the majority-class share of the loaded rows × 100 (from the header's `class_counts`). The carrier is **floor-bound** if the tuned λ\*_raw's mean accuracy − floor < 3 steps. Per study and pooled over the 30 held-out carriers: the number floor-bound; the not-behind rates of the unclipped SEC, the clipped SEC (SEC4 and SEC5), raw Laplace and the transferred λ on floor-bound carriers against the rest. Every forecast F1–F11 whose decisive count includes floor-bound carriers is also printed with them removed, as a report. | **F12.** At least a quarter of the 30 held-out carriers are floor-bound, and the unclipped SEC's not-behind rate is higher on them than on the rest. |

## Amendment 2 (2026-09-30, after SEC6's development runs of SI-1C and AR1-B on the same 30 SEEN carriers; before any M output was read; pushed before any M5/M6 code)

**What prompted it.**
- SEC6's D-RUN (`prereg/sec6/dev_SEC6.txt`) gives these not-behind counts on the 30 carriers:
  - SI-1C (SI at c = 1 with SEC4's clip and a zero floor): 28/30;
  - AR1-B (the raw Fisher scaled so its largest coordinate sits at half the stability edge): 27/30;
  - SI-1 unclipped: 0/30;
  - the pinned clipped SEC: 26/30.
- At κ = 0.5, a coordinate at the cap has lr · 2w · imp = 1. The penalty's step then returns that coordinate to its
  anchor on every update, so **the clip freezes the capped coordinates**.
- **The candidate explanation.** The clip turns a soft penalty into a hard freeze of the most important coordinates, and
  the importance measure only decides which coordinates those are.

**Added checks** (run by the P1 runner or read from SEC6's development records):

| id | what | forecast |
|---|---|---|
| **M5** | FREEZE-TOP. The clipped SEC's importance is used only to choose the coordinates at the cap. Those are frozen (snapped to the anchor on every step), and the penalty is removed everywhere else. Run on the 30 carriers, seeds 0–4, with the fraction of coordinates frozen per task recorded. | FM5: within a step of the clipped SEC on at least 80 % of the carriers where the clip fired |
| **M6** | EDGE, a must-fail control. Every coordinate is set at the cap after task 1: a uniform freeze with no Fisher at all. | FM6: behind the tuned λ on most carriers; freezing everything stops learning |
| **A13** | The development arms read as mechanism evidence: SI-1C, AR1-B, SEC6's `fixed_clip` (the tuned λ with the clip), the clipped SEC, and the fraction of capped coordinates, all against the tuned λ with and without the clip. Read from `prereg/sec6/dev/` and the M records. | **F13.** The tuned clipped λ is ahead of the unclipped tuned λ by more than a step on at least a third of the 30 carriers: part of SEC4's margins is the clip's |
