# Why SEC4 passed and SEC5 did not (P1 of `Applied_Suite/PROGRAMME.md`)

**Status.**
- **What this is.** A post hoc analysis of records already opened. No ledger row. A note, not evidence (R8).
- **When each part was fixed.**
  - The declaration (`DECLARATION.md`, 5f64b5f) was pushed before any analysis ran.
  - Amendment 1 (A12) came after the loader check.
  - Amendment 2 (M5, M6, A13) came after SEC6's development runs.
  - Amendment 3 (A14) came after `m_checks.txt` was read.
  - So **A12–A14 (F12–F14) are post hoc in origin**, and are labelled so below.
- **Where the numbers come from.** Every number below is printed in a pinned output named beside it:
  - `checks/*.txt`, each of which reruns byte-identically;
  - or `prereg/sec6/dev_SEC6.txt`, SEC6's development report, for which no rerun is recorded.

  The one exception is SEC6's hash 69c37965…, which is the sha256 of `prereg/sec6/HASH.txt` (commit 1bb1870,
  AGENT_LOG 224).
- **Review.**
  - The A1–A11 scripts and the M runner were each attacked by two adversarial reviewers, and the real defects were fixed
    before this was written (AGENT_LOG 220).
  - `checks/a12_a14.py` was not reviewed that way.
  - This document was checked number by number by an independent verifier (AGENT_LOG 227).
- **The loader.** It reproduces every pinned SEC-family result it checks (`checks/loader_check.txt`: REPRODUCED 122, DIFFERS
  0).
- **The ledger rows stand as scored.** This note reads them; it does not re-score them.
- **"Floor-bound"** (Amendment 1): the tuned λ scores less than 3 steps above always predicting the largest class, and
  often below it. Other arms can score well above the floor on such a carrier. P1's M6 does on wall-robot-navigation:
  68.4885 against a floor of 40.4119 (`checks/a12_a14.txt`).

## The answer in five sentences

1. **The criterion the SEC family shares was weak on most of the 30 held-out carriers. It was not weak on SEC4-1's own
   passes.**
   - **Pooled over the held-out carriers:**
     - 19 of the 30 are floor-bound (`checks/a12_a14.txt`; F12, post hoc in origin).
     - A learner frozen after task 1 (P1's must-fail control M6, Amendment 2) is not behind the tuned λ on 24/30
       (`checks/m_checks.txt`, FM6 FAILS).
     - 12 of the unclipped SEC's 20 held-out passes had a negative margin (`checks/a5_a9_a10.txt`; F10, declared).
   - **On SEC4's own six carriers:**
     - 2 are floor-bound (`checks/a12_a14.txt`);
     - none of SEC4-1's six clipped passes rests on the tolerance (0/6 negative margins; `checks/a5_a9_a10.txt`);
     - M6's rows in `checks/m_checks.txt` mark only cardiotocography behind (−44.0566). The others print JapaneseVowels
       +18.2583, anneal +0.6742, artificial-characters +9.4905, gas-drift −1.7618 and synthetic_control −1.6667.
2. **SEC4's family was easier than SEC5's.**
   - A λ reused from the other carriers was not behind on 4/6 in SEC4 against 1/8 in SEC5 (`checks/a7_a8.txt`, F8).
     Part of that gap is divergence at the reused λ: 4 of SEC5's 7 behind cases have a non-finite seed there.
   - The calibration collapsed the spread of the optimum's location in SEC4 (SD ratio 0.3611) but not in SEC5 (1.0348)
     (`checks/a1_a3.txt`, F2).
3. **Both the calibration and the clip added carriers in SEC4. On SEEN data the calibration is replaceable.**
   - In SEC4 (`checks/a7_a8.txt`):
     - raw Laplace was not behind on 1/6;
     - unguarded SEC (with the calibration) on 3/6;
     - the clipped SEC on 6/6.
   - On the 30 SEEN carriers (`prereg/sec6/dev_SEC6.txt`), two rules without SEC's calibration match or pass the clipped
     SEC's 26/30 against the tuned λ (against the tuned clipped λ, AR1-B falls to 19/30, below the clipped SEC's 22/30):
     - the raw Fisher scaled to half the stability edge (AR1-B): 27/30;
     - SI at c = 1 with a zero floor and SEC4's clip (SI-1C): 28/30.
4. **Where the stream is informative, the calibration behaves like a units correction. This is a post hoc report on few
   carriers.**
   - On the 16 carriers that are not floor-bound, the tuned raw λ tracks 0.5 · s̄: Spearman 0.752, slope 1.224, and the
     median s > 10 on 16/16 (`checks/a4_a6.txt`).
   - The optimum's spread falls to 0.191, 0.246 and 0.258 of the raw spread in SEC1, SCL3 and SEC4
     (`checks/a1_a3.txt`). SEC3 and SEC5 keep one carrier each, so F2 on this subset is NOT DECIDABLE, although all three
     families with a defined SD meet the bar.
   - Where a pinned clipped arm exists (SEC4 and SEC5), the clipped SEC is not behind on 5/5 of those carriers
     (`checks/a12_a14.txt`).
   - **Against this:** on the same 16 carriers F1 FAILS: the calibrated shape beats the raw one by more than a step on 8.
5. **No CRR-proper ingredient is load-bearing** (`checks/a11_grade.txt`, F11 HOLDS).
   - The weight 1/2 is the Laplace weight. The calibration is a Barzilai–Borwein secant that rescales the empirical Fisher, and the
     clip is AR1's bound.
   - The declared CRR-guided variant was a 5-segment least-squares secant. As implemented it is not CRR's arc, and it
     performs no CRR-proper operation (`checks/a11_grade.txt`). It is within a step of the clipped SEC on 29/30 and ahead
     on 0/30 (`checks/m_checks.txt`, FM4).

## 1. The criterion

**The stream's structure.**
- The frozen loader ranks the classes by count, and SEC1's tasks are consecutive label pairs. Task 1 therefore holds the
  two most frequent classes. This is checked on all 42 headers (`checks/a12_a14.txt`).
- The test set is stratified.

**The must-fail control met the criterion.** P1's M6 puts every coordinate at SEC4's cap after task 1, with no Fisher.
It is not behind the tuned λ on 24/30, with margins over the tuned λ up to +43.7237 (wall-robot-navigation;
`checks/m_checks.txt`). The clipped SEC (C0) reaches 26/30 on the same carriers.

**The class order is a candidate explanation of the control's pass whose declared test fell just short** (post hoc in
origin, F14 FAILS;
`checks/a12_a14.txt`):
- The task-1 share correlates with M6's accuracy at Spearman 0.785, just under the declared 0.8.
- With M6's margin in steps it correlates at +0.271, a report.
- The majority-class floor alone correlates with M6's accuracy at 0.751, a report.
- The share correlates **negatively** with SEC's margin: −0.393 over 42 carriers, −0.543 for the clipped SEC over 14, and
  −0.604 for C0 over 30.

**Floor effects** (post hoc in origin, F12; `checks/a12_a14.txt`).
- 19 of the 30 held-out carriers are floor-bound. Per study: SCL3 5/10, SEC3 5/6, SEC4 2/6, SEC5 7/8.
- The unclipped SEC is not behind on 13/19 of them, against 7/11 on the rest.
  - That difference rests on one carrier: with one fewer floor-bound pass, 12/19 = 0.632 < 0.636.
  - It holds at every floor-bound bar from 1 to 5 steps.
  - The nearest floor-bound pass (covertype) is 0.300 steps above the line.
  - These are REPORT lines in `checks/a12_a14.txt`.
- The clipped SEC runs the other way: 5/9 on floor-bound carriers against 5/5 on the rest (the pinned arm, SEC4 and SEC5
  only: 14 carriers).

**Tolerance.** 12 of the unclipped SEC's 20 held-out passes had a negative margin (F10 HOLDS). None of SEC4-1's six
clipped passes did.

**What follows.**
- The family's criterion ("not behind the tuned λ") is met on most of these carriers by a learner that stops learning
  after task 1, so the criterion alone cannot show that a method is tuning-free.
- SEC4-1's own passes are not the weak ones: no tolerance passes, and 2 of 6 floor-bound. But M6 is not behind on five of
  SEC4's six carriers too.
- **Applied after the fact, SEC6-G's rule (hashed in SEC6) closes the gate for SEC4-1.** M6 is not behind the tuned λ on
  5/6 of SEC4's carriers, and SEC4-1 needed 5, so the rule would print SEC4-1 UNINFORMATIVE and cap it at PASS-0
  (`checks/gate_posthoc.txt`; ledger report row SEC4-1-G).
  - The same rule leaves SCL3-3's PASS-0 standing (7/10, need 8).
  - It closes the gate for SEC3-3 (5/6) and SEC5-1 (7/8), both FAIL as scored.
  - The rows stand as scored under their own pre-registrations. This is a post hoc report, not a re-score.
- SEC6 now carries a gate for this (SEC6-G, below).

## 2. Why SEC4's family, and not SEC5's

From `checks/a7_a8.txt` (A8 table; the clip and raw-Laplace columns are REPORT columns) and `checks/a1_a3.txt` (F2):

| family | SD of log10 λ\*_raw | reused λ not behind | SD ratio after calibration | unguarded SEC | clipped SEC | raw Laplace |
|---|---|---|---|---|---|---|
| SEC4 | 1.2768 | 4/6 | 0.3611 | 3/6 | 6/6 | 1/6 |
| SEC5 | 1.6679 | 1/8 | 1.0348 | 4/8 | 4/8 | 4/8 |

**SEC5's four clipped failures** (`checks/a5_a9_a10.txt`, F5):
- They are classed U, D, D and X: one under-regularised, two classed D (pokerhand and volcanoes-d4: seeds below half the
  tuned accuracy) and one unclassified.
- On pokerhand the clip never fired. Ledger row SEC5-2 reads its low seeds as not a stability-edge crossing.
- On volcanoes-d4 the clip fired on every seed and lowered accuracy: 6.0861 against the unclipped 16.2763
  (`checks/loader_check.txt`).

**Imbalance.** The clipped SEC's label is split by class imbalance at 18.0927, with one error in 14 (`checks/a7_a8.txt`,
F7). An undeclared label-permutation null reaches one error or fewer in 449/5000 = 0.0898 of permutations. That is a
report, not a test.

**Floor.** 7 of SEC5's 8 carriers are floor-bound.

## 3. What the calibration does, and what it does not

- **On all 42 carriers it mostly moves the location, not the shape.**
  - Where SEC is not behind, fixing the weight at 1/2 costs less than a step against the best calibrated multiplier on
    29/29.
  - The calibrated shape beats the raw one by more than a step on only 9/42 (F1 HOLDS).
  - Two qualifiers are printed with it (`checks/a1_a3.txt`):
    - the lower half of F1(i) is forced by "not behind" on 10 of the 29;
    - SEC's effective weight is 0.5 · n_j / n_t, which is exactly 0.5 on only 7 of 42 carriers, so the "location cost"
      includes a task-size reweighting.
  - On the 16 carriers that are not floor-bound, the shape gain exceeds a step on 8 (F1 FAILS there, a post hoc report).
- **It moves the plateau, it does not widen it.** The median plateau width is about the same on both axes (F3(b)
  HOLDS). Whether 0.5 lies inside the calibrated plateau agrees with SEC's label on 35/42, below the declared 0.9
  (F3(a) FAILS).
- **As a units correction:**
  - F4 FAILS on all 42: Spearman 0.545 < 0.6, slope 0.718.
  - It HOLDS on the 16 that are not floor-bound (post hoc report).
  - The geometric-mean s > 1 on 41/42 carriers (`checks/a11_grade.txt`). The same output notes that the direction does
    not single out the empirical Fisher's error: a diagonal-against-full curvature gap would also give s > 1.
- **The known Fisher-based alternatives, each run with SEC4's clip, do worse** (`checks/m_checks.txt`):

  | arm | not behind (of 30) | note |
  |---|---|---|
  | Laplace on the model Fisher (M1) | 13 | FM1 HOLDS |
  | calibration to the endpoint curvature (M2) | 21 | FM2 HOLDS; the path secant exceeds the endpoint curvature by a median factor of 5.859 |
  | clipped SEC (C0) | 26 | |

  One global factor (`bayes_s1`, unclipped) is not behind on 18/42, against 29/42 for per-task factors (FM3 HOLDS).
- **Two rules without SEC's calibration match or pass it on SEEN data** (`prereg/sec6/dev_SEC6.txt`; development runs,
  not evidence):
  - AR1-B, the raw Fisher at half the stability edge: 27/30 against the tuned λ, 19/30 against the tuned clipped λ;
  - SI-1C: 28/30 against the tuned λ and 30/30 against the tuned clipped λ;
  - the clipped SEC: 26/30 and 22/30.

  "Match or pass" holds against the tuned λ; against the tuned clipped λ only SI-1C passes the clipped SEC.

## 4. What the clip does, and what it does not

- **Divergence.** Here "diverged" means a seed below half the tuned accuracy.
  - Over the 42 carriers, the 10 where unguarded SEC diverged have a median of per-carrier max s of 28599.49, against
    212.25 for the other 32 (`checks/a4_a6.txt`, F6 HOLDS; it also holds with the floor-bound carriers removed).
  - On the 30 SEEN carriers of SEC6's development stage, unguarded SEC diverged on 8 (`prereg/sec6/dev_SEC6.txt`).
  - The clipped SEC still meets that rule on pokerhand and volcanoes-d4, as do raw Laplace, SI-0.1, AR1-P, AR1-B and
    SI-1C (`prereg/sec6/dev_SEC6.txt`). SI-1 meets it on pokerhand but not on volcanoes-d4, where it scores 80.2803.
    What happens on each is in §2.
- **It is not only a freeze.** At the cap, each step returns a capped coordinate to its anchor minus one gradient step
  (`checks/a11_grade.txt`).
  But freezing the capped coordinates with no penalty elsewhere (M5) is within a step of the clipped SEC on only 1/13 of
  the carriers where the clip fired (`checks/m_checks.txt`, FM5 FAILS). The penalty below the cap matters.
- **Where it fires** (`checks/m_checks.txt`, `checks/a12_a14.txt`):
  - it fired on 13/30 carriers;
  - 115 firings over seeds and tasks;
  - over those 13 carriers, the median of the per-carrier mean fraction of capped coordinates is 6.889e-05.
- **It changes the reference** (post hoc, F13 HOLDS at its bar).
  - A tuned λ given the same clip is ahead of the unclipped tuned λ by more than a step on 10/30.
  - Against it, the clipped SEC is not behind on 22/30, not 26/30 (`checks/a12_a14.txt`).
  - The count is 10/30 whichever step is read: the unclipped step, step_c, or their maximum.
  - "Ahead" partly reflects λ values the raw refinement never visits. The two grids coincide on 11/30 carriers, none of
    them among the 10 ahead. On 8 of the 10, the tuned clipped λ is not a value of the raw grid.
  - These are REPORT lines in `checks/a12_a14.txt`.

## 5. CRR's part

**A11** (`A11_CRR_READING.md`, `checks/a11_grade.txt`; the sources' quotes verified in `checks/verify_a11.txt`):
- none of CRR's operational clauses is performed on SEC's code path;
- the ingredients are published: the Laplace weight, the Barzilai–Borwein secant, the empirical Fisher's scale error and
  AR1's bound;
- CRR's rung for the explanation is at most R1.

**The declared CRR-guided variant (M4) ties the chord** on 29/30 and is ahead on none. As implemented it is a 5-segment
least-squares secant, not CRR's arc, so it is not a path-length test. It echoes T1X2's finding on a different question.

**SEC4's pass is not evidence for CRR,** and the programme's documents must not present it as such (R8).

## 6. What this changed before SEC6 was hashed (`prereg/sec6/PREREG.md`; sha256 of HASH.txt 69c37965…, commit 1bb1870)

1. **SEC6-G and SEC6-GC,** the instrument gates. If a learner frozen after task 1 meets the criterion on the fifth
   family, SEC6-1, SEC6-B and SEC6-P (or SEC6-C, for SEC6-GC) are printed UNINFORMATIVE and capped at PASS-0.
2. **SEC6-C.** The clipped SEC against a tuned λ given the same clip.
3. **SEC6-1F.** The criterion on the carriers that are not floor-bound.
4. **SEC6-B.** The calibration against the published tuning-free rules, SI (c = 1, as published and clipped; c = 0.1) and
   AR1 (as published; its bound as the strength).
5. **What was not carried.** P1's M1, M2 and M4 are not carried: each failed the declared carry rule
   (`checks/m_checks.txt`).

## The forecasts, as scored

| forecast | word (all carriers) | floor-bound removed (post hoc report) | where |
|---|---|---|---|
| F1 (the location, not the shape) | HOLDS | FAILS | `checks/a1_a3.txt` |
| F2 (the spread collapses in every family) | FAILS (meets the bar in SCL3 and SEC4 only; SCL3 under the scorers' tie rule) | NOT DECIDABLE | `checks/a1_a3.txt` |
| F3(a) / F3(b) | FAILS / HOLDS | FAILS / HOLDS | `checks/a1_a3.txt` |
| F4 (units correction) | FAILS | HOLDS | `checks/a4_a6.txt` |
| F5 (failure classes) | FAILS | HOLDS ((ii) vacuous) | `checks/a5_a9_a10.txt` |
| F6 (divergence goes with large s) | HOLDS | HOLDS | `checks/a4_a6.txt` |
| F7 (no single property separates) | FAILS (imbalance separates the clipped label with one error) | UNDEFINED | `checks/a7_a8.txt` |
| F8 (SEC4's family was easy) | HOLDS | HOLDS | `checks/a7_a8.txt` |
| F9 (SEC5's failure classes) | FAILS | FAILS (vacuous) | `checks/a5_a9_a10.txt` |
| F10 (tolerance passes) | HOLDS | HOLDS | `checks/a5_a9_a10.txt` |
| F11 (no CRR ingredient load-bearing) | HOLDS | part (b-iv) true on 16/16 | `checks/a11_grade.txt` |
| F12 (floor-bound carriers; post hoc in origin) | HOLDS | — | `checks/a12_a14.txt` |
| F13 (the clip changes the reference; post hoc in origin) | HOLDS (at its bar) | — | `checks/a12_a14.txt` |
| F14 (the class order explains the margins; post hoc in origin) | FAILS | — | `checks/a12_a14.txt` |
| FM0–FM4 | HOLD | — | `checks/m_checks.txt` |
| FM5 (the clip acts as a freeze) | FAILS | — | `checks/m_checks.txt` |
| FM6 (the frozen learner must fail) | FAILS | — | `checks/m_checks.txt` |

## What would change this reading

- **SEC6 decides whether any of this holds on unseen data.**
  - If SEC6-G and SEC6-GC are OPEN and SEC6-1 and SEC6-C pass, the clipped SEC is tuning-free on a family where the
    criterion can fail: PASS-0, or PASS-1 if the pre-registration's PASS-1 conditions also hold.
  - If SEC6-G is CLOSED, the family's criterion is shown to be uninformative on a fifth family too.
- **Every "floor-bound removed" result is post hoc**, on 16 carriers of which 5 have a pinned clipped arm.
- **The test after SEC6** should use a stream where the criterion can fail by design: random class order, or balanced
  accuracy. That test is a new pre-registration on a later day.

## Addendum (2026-09-30, after SEC7's development gate; appended, nothing above changed)

The redesign proposed above was tried on the 30 SEEN carriers: a seeded random class order, with balanced accuracy as the
metric (`prereg/sec7/DEV_DECLARATION.md`, Amendment 1; `prereg/sec7/dev/gate7.txt`; ledger row SEC7-A).

- **It does not make the criterion informative.**
  - The learner frozen after task 1 is behind the tuned λ on only 13/30. The gate needed more than 15, so D-GATE-7 is
    CLOSED and SEC7 stopped (R12).
  - The clipped SEC is not behind on 29/30, and the frozen learner on 17/30.
- **What that means.** On these class-incremental tabular streams, the tuned EWC-type λ is often no better than freezing
  after the first task, whatever the class order or metric. "Not behind the tuned λ" therefore cannot show that a
  method is tuning-free here.
- **What would be needed.** A SEC test that can fail needs a reference that must beat freezing (or task-incremental
  heads). That is a new design, declared from scratch on a later day.
