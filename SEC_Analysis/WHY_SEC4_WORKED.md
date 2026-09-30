# Why SEC4 passed and SEC5 did not (P1 of `Applied_Suite/PROGRAMME.md`)

**Status.**
- A post hoc analysis of records already opened, declared before any analysis ran (`DECLARATION.md` at 5f64b5f,
  Amendments 1–3). No ledger row. A note, not evidence (R8).
- **Every number below is printed by a script in `checks/`** whose output is pinned beside it, with a byte-identical rerun.
  Each script was attacked by two adversarial reviewers, and the real defects they found were fixed before this was
  written (AGENT_LOG 220).
- **The loader reproduces all 122 pinned SEC-family counts** (`checks/loader_check.txt`: REPRODUCED 122, DIFFERS 0).
  Nothing here disagrees with a ledger row. It explains the rows.
- **"Floor-bound"** (Amendment 1): a carrier whose tuned-λ accuracy is less than 3 steps above the majority-class share.
  There, no method is learning much beyond the largest class.

## The answer in five sentences

1. **SEC4's criterion was weak on most of the carriers it is read on.**
   - 19 of the 30 held-out carriers are floor-bound (`checks/a12_a14.txt`, F12).
   - A learner frozen after task 1 (P1's must-fail control M6) is not behind the tuned λ on 24/30
     (`checks/m_checks.txt`, FM6 FAILS).
   - 12 of 20 held-out passes had a negative margin, passing on the tolerance (`checks/a5_a9_a10.txt`, F10).
2. **SEC4's family was easier than SEC5's.**
   - A λ reused from the other carriers was not behind on 4/6 in SEC4 against 1/8 in SEC5 (`checks/a7_a8.txt`, F8).
   - The calibration collapsed the spread of the optimum's location in SEC4 (SD ratio 0.361) but not in SEC5 (1.035)
     (`checks/a1_a3.txt`, F2).
3. **The clip, not the calibration, did the rest.**
   - Unguarded SEC was not behind on 3/6 in SEC4, the clipped SEC on 6/6 (`checks/a7_a8.txt`, A8 table).
   - Divergence goes with a large calibration factor: the median of per-carrier max s is 28599 where unguarded SEC
     diverged, against 212 elsewhere (`checks/a4_a6.txt`, F6).
   - On SEEN data, a published rule given the same clip does at least as well (SI-1C 28/30; `prereg/sec6/dev_SEC6.txt`).
4. **Where the stream is informative, the calibration really is a units correction of the Fisher.**
   - On the 16 carriers that are not floor-bound, the tuned raw λ tracks 0.5 · s̄: Spearman 0.752, slope 1.224, s̄ > 10
     on 16/16.
   - The spread of the optimum shrinks 4–5× (SD ratios 0.191, 0.246, 0.258).
   - The clipped SEC is not behind on 5/5 there.
   - This is post hoc, on few carriers (`checks/a4_a6.txt`, `checks/a1_a3.txt`, `checks/a7_a8.txt`: the Amendment 1
     reports).
5. **No CRR-proper ingredient is load-bearing** (`checks/a11_grade.txt`, F11 HOLDS).
   - The weight 1/2 is the Laplace weight. The calibration is a Barzilai–Borwein secant fixing the empirical Fisher's
     scale, and the clip is AR1's.
   - The one CRR-guided variant, an arc secant in place of SEC's chord secant, is within a step of SEC on 29/30 and ahead
     on none (`checks/m_checks.txt`, FM4).

## 1. The criterion, and why most passes could not have failed

**The stream's structure.**
- The frozen loader ranks the classes by count, and SEC1's tasks are consecutive label pairs. Task 1 always holds the
  two most frequent classes (`DECLARATION.md` Amendment 3; checked on all 42 headers in `checks/a12_a14.txt`).
- The test set is stratified. Keeping task 1 is therefore worth a lot of accuracy on imbalanced carriers.

**The must-fail control met the criterion.** P1's M6 puts every coordinate at SEC4's cap after task 1, with no Fisher.
It is not behind the tuned λ on 24/30 carriers, with margins over the tuned λ up to +43.7237 (wall-robot-navigation;
`checks/m_checks.txt`). The clipped SEC (C0) reaches 26/30 on the same carriers.

**The task-1 share does not explain SEC's margins.**
- The share tracks M6's accuracy only just below the declared bar: Spearman 0.785 against 0.8.
- The share correlates **negatively** with SEC's margin: −0.393 over 42 carriers (−0.604 for C0 over 30).
- So F14 FAILS (`checks/a12_a14.txt`). The class order explains why the control passes; it does not explain SEC's
  margins.

**Floor effects.**
- 19 of the 30 held-out carriers are floor-bound (per study: SCL3 5/10, SEC3 5/6, SEC4 2/6, SEC5 7/8).
- The unclipped SEC is not behind on 13/19 of them, against 7/11 elsewhere (F12 HOLDS).

**Tolerance.** Of 20 held-out passes, 12 had a negative margin (F10 HOLDS).

**What follows.** "Not behind the tuned λ" is met on these streams by a learner that stops learning after task 1. Without
a gate on that, SEC4-1's PASS-1 shows less than its label says. The rows stand as scored. SEC6 now carries the gate
(SEC6-G, below).

## 2. Why SEC4's family, and not SEC5's

Per family, from `checks/a7_a8.txt` (A8 table) and `checks/a1_a3.txt` (F2):

| family | SD of log10 λ\*_raw | reused λ not behind | SD ratio after calibration | unguarded SEC | clipped SEC | raw Laplace |
|---|---|---|---|---|---|---|
| SEC4 | 1.2768 | 4/6 | 0.361 | 3/6 | 6/6 | 1/6 |
| SEC5 | 1.6679 | 1/8 | 1.035 | 4/8 | 4/8 | 4/8 |

**The contrast.**
- In SEC4 the calibration moved the carriers' optima together, and a reused λ already did well. In SEC5 neither held.
- SEC5's four clipped failures are classes U, D, D and X (`checks/a5_a9_a10.txt`, F5): one under-regularised, two
  divergent seeds (pokerhand, volcanoes-d4) and one unclassified.
- The clipped SEC's label is split by class imbalance at 18.0927 with one error in 14 (`checks/a7_a8.txt`, F7). An
  undeclared label-permutation null reaches one error or fewer in 449/5000 = 0.0898 of permutations. It is a report,
  not a test.
- 7 of SEC5's 8 carriers are floor-bound.

## 3. What the calibration does, and what it does not

- **It does not work by the shape.** Where SEC is not behind, fixing the weight at 1/2 costs less than a step against
  the best multiplier of the calibrated Fisher on 29/29. The calibrated shape beats the raw shape by more than a step on
  only 9/42 (F1 HOLDS).
- **It moves the plateau, it does not widen it.** The median plateau width is about the same on both axes (F3(b)
  HOLDS). Whether 0.5 lies inside the calibrated plateau agrees with SEC's label on 35/42, below the declared 0.9
  (F3(a) FAILS).
- **It is a partial units correction on all 42, and a strong one where the stream is informative.**
  - F4 FAILS on all 42: Spearman 0.545, slope 0.718.
  - It HOLDS on the 16 carriers that are not floor-bound (Spearman 0.752, slope 1.224).
  - s > 1 on 41/42 (`checks/a11_grade.txt`), so the empirical Fisher at a task's end understates the curvature the path
    showed.
- **The known alternatives do not do its job.**

  | arm | not behind (of 30) | source |
  |---|---|---|
  | Laplace on the model Fisher (M1) | 13 | FM1 HOLDS |
  | calibration to the endpoint curvature (M2) | 21 | FM2 HOLDS; the path secant exceeds the endpoint curvature by a median factor of 5.859 |
  | clipped SEC (C0) | 26 | |

  One global factor (`bayes_s1`) is not behind on 18/42, against 29/42 for per-task factors (FM3 HOLDS).
- **But a published path-fitted importance does at least as well once it is given the same clip.** SI with c = 1, a
  zero floor and SEC4's clip (SI-1C) is not behind the tuned λ on 28/30 SEEN carriers, and not behind the tuned clipped λ
  on 30/30 (`prereg/sec6/dev_SEC6.txt`). SEC's calibration is one good units correction, not the only one.

## 4. What the clip does, and what it does not

- **It removes most divergence.**
  - Unguarded SEC diverged on 8 of the 30 SEEN carriers (`prereg/sec6/dev_SEC6.txt`).
  - Divergence goes with a very large calibration factor (F6 HOLDS; also with the floor-bound carriers removed).
  - The clip leaves two divergent carriers: pokerhand and volcanoes-d4, both in SEC5.
- **It is not a hard freeze.** Freezing only the coordinates at the cap, with no penalty elsewhere (M5), is within a step
  of the clipped SEC on 1 of 13 carriers where the clip fired (FM5 FAILS). The soft penalty below the cap matters.
- **It fires rarely and touches very few coordinates.** It fired on 13/30 carriers, and the median of the per-carrier mean
  fraction of capped coordinates is 6.889e-05 (`checks/a12_a14.txt`, A13).
- **It changes the reference.** A tuned λ given the same clip is ahead of the unclipped tuned λ by more than a step on
  10/30 (F13 HOLDS at its bar). Against it, the clipped SEC is not behind on 22/30, not 26/30.

## 5. CRR's part

**A11** (`A11_CRR_READING.md`, `checks/a11_grade.txt`; every source quote verified in `checks/verify_a11.txt`):
- none of CRR's operational clauses is performed on SEC's code path;
- the ingredients are published (Laplace weight; Barzilai–Borwein secant; the empirical Fisher's scale error; AR1's
  clip);
- the rung is R1 at most.

**The one place CRR could have changed the method did nothing.** Replacing SEC's chord (start-window to end-window) with
an arc of 5 segments gives the same result on 29/30 (FM4). This agrees with T1X2: the path did not beat the endpoint.

**So SEC4's pass is not evidence for CRR,** and the programme's documents must not present it as such (R8).

## 6. What this changed before SEC6 was hashed (`prereg/sec6/PREREG.md`, hashed 69c37965 at 1bb1870)

1. **SEC6-G,** the instrument gate. If a learner frozen after task 1 meets the criterion on the fifth family, SEC6-1,
   SEC6-B and SEC6-P are printed UNINFORMATIVE and capped at PASS-0.
2. **SEC6-C.** The clipped SEC against a tuned λ given the same clip.
3. **SEC6-1F.** The criterion on the carriers that are not floor-bound.
4. **SEC6-B.** The calibration against the published tuning-free rules, SI (c = 1, as published and clipped; c = 0.1) and
   AR1 (as published; its bound as the strength).
5. **What was not carried.** P1's M1, M2 and M4 are not carried: each failed the declared carry rule.

## The forecasts, as scored

| forecast | word | where |
|---|---|---|
| F1 (the location, not the shape) | HOLDS | `checks/a1_a3.txt` |
| F2 (the calibration collapses the spread in every family) | FAILS (only SCL3 and SEC4) | `checks/a1_a3.txt` |
| F3(a) / F3(b) | FAILS / HOLDS | `checks/a1_a3.txt` |
| F4 (units correction on all 42) | FAILS (HOLDS with the floor-bound carriers removed, report) | `checks/a4_a6.txt` |
| F5 (failure classes) | FAILS | `checks/a5_a9_a10.txt` |
| F6 (divergence goes with large s) | HOLDS | `checks/a4_a6.txt` |
| F7 (no single property separates) | FAILS (imbalance separates the clipped label with one error; the permutation share 0.0898 is a report, not a test) | `checks/a7_a8.txt` |
| F8 (SEC4's family was easy) | HOLDS | `checks/a7_a8.txt` |
| F9 (SEC5's failure classes) | FAILS | `checks/a5_a9_a10.txt` |
| F10 (tolerance passes) | HOLDS | `checks/a5_a9_a10.txt` |
| F11 (no CRR ingredient load-bearing) | HOLDS | `checks/a11_grade.txt` |
| F12 (floor-bound carriers) | HOLDS | `checks/a12_a14.txt` |
| F13 (the clip changes the reference) | HOLDS (at its bar) | `checks/a12_a14.txt` |
| F14 (the class order explains the margins) | FAILS | `checks/a12_a14.txt` |
| FM0–FM4 | HOLD | `checks/m_checks.txt` |
| FM5 (the clip is a hard freeze) | FAILS | `checks/m_checks.txt` |
| FM6 (the frozen learner must fail) | FAILS | `checks/m_checks.txt` |

## What would change this reading

- **SEC6 decides whether any of this holds on unseen data.**
  - If SEC6-G is OPEN and SEC6-1 and SEC6-C pass, the clipped SEC is tuning-free on a family where the criterion can fail.
  - If SEC6-G is CLOSED, the family's criterion is shown to be uninformative on a fifth family too.
- **Every "floor-bound removed" result above is post hoc** (Amendment 1), on 16 carriers of which 5 have a clipped arm.
  The next test of SEC is a stream where the criterion can fail by design: random class order, or balanced accuracy.
  That test is a new pre-registration on a later day.
