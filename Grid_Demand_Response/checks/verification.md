# DR1 verification: the skeptics' verdicts

Declaration: `Grid_Demand_Response/DECLARATION.md` §4 (pushed at e67e8ee): every model check and the data calculation are
reviewed by independent skeptic agents prompted to refute them; a finding survives only if a majority of its skeptics fail to
refute it; refuted findings are reported as refuted, not deleted.

This file transcribes the verification record (one entry per check: status, final RESULT line, round-1 skeptic verdicts,
fix, round 2) as given, without editorialising. The record carries no `lens` field for any skeptic; the lens is therefore
written as "not recorded" below. Skeptics are numbered in the order the record lists them.

## Overview

| id | status | round-1 skeptics refuting | severities (round 1, in order) | fix | round 2 |
|---|---|---|---|---|---|
| H1 | survived | 0 of 3 | minor, minor, minor | none | none |
| H2 | survived | 0 of 3 | minor, minor, minor | none | none |
| H3 | survived | 0 of 3 | minor, minor, minor | none | none |
| H4 | survived | 0 of 3 | minor, minor, minor | none | none |
| H5 | survived | 0 of 3 | minor, minor, minor | none | none |
| H6 | survived | 0 of 3 | minor, minor, minor | none | none |
| H7 | survived | 1 of 3 | minor, minor, major | none | none |
| H8 | survived | 0 of 3 | minor, minor, minor | none | none |
| DATA | survived | 0 of 3 | minor, minor, minor | none | none |

---

## H1

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H1: Q holds; G-ZERO holds (max |ETM stake - rate (R + S)| = 0 over 1312 event counts in 32 cells; ETM x* = (R + S)/H at 27552 of 27552 offer states); G-NEG holds (ETM ahead of WALL by more than 1 % in 0 of 3456 no-event comparisons); G-POS holds (expected events below ETM's: WALL in 112, OWN in 56 of 288 cell x pi; OWN's largest shortfall 11.451256 events)

### H1, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q-b depends on how the check reads the declaration, and only 8 of 32 cells actually test it. The declared clause 'OWN's and WALL's rise as the slack falls' is scored under reading B, which the check chose itself; the declaration does not specify it. In 24 of 32 cells no zero-slack state is reachable. There, OWN's x* is flat at (R+S)/H, the same as ETM's, and WALL's is flat at (H+R+S)/H, even though wall slack falls with every accepted event (e.g. from 100 h to about 55 h in the D1100-H1 cells). Reading B passes those cells because nothing contradicts it; reading A fails 8/32, and then Q would be 'fails'. The declaration never says 'in every cell', so reading B is a defensible reading, not a deviation. But the RESULT line prints a bare 'Q holds', and any write-up must carry 'reading B; reading A fails 24/32 cells'.
2. In substance, OWN differs from ETM only in states reached with tiny probability. OWN's x* equals ETM's except at zero-slack states in the D1100-H4 cells. At the only sourced rate, lambda_DFS = 1/66, P(offers made > OWN's nmax 24) = 5.25e-05; at 1/240 it is 6.4e-16. G-POS for OWN (56 of 288) rests entirely on these tails; G-POS holds anyway through WALL (112 of 288).
3. The check reads 'R' as the total overhead R + S. The declaration's Q ('R/H') and G-ZERO ('stake beyond R') say R; the check scores (R+S)/H and 'stake - rate (R+S)' (drlib's CHOICE, printed). In the added Kokolis cells (S = R = 1/12 h), ETM's x* is 2R/H, so literal Q-a and G-ZERO would fail in 16 of 32 cells. This does not change the verdict relative to the declaration. The declaration fixes EPS2 T1's units for H1 (S = 0), and on those cells (the 'A' cells) Q-a and G-ZERO hold 16/16 under either reading. The declaration's own H4 and H6 treat the save as an overhead.
4. Q-b's monotonicity excludes states past the deadline (slack < 0), where OWN's x* collapses from about 250 back to R/H. The exclusion is printed and reasonable, but it is a choice needed for reading B to hold.
5. lambda_DFS divides the 44 events by the calendar months December 2024 to March 2025 (121 days). The dossier's own period statement is 27 November 2024 to 28 March 2025, and it also says DFS became year-round on 27 November 2024. A full-year reading would give about 1/199 per hour. This is printed as a CHOICE, and the grid already covers 1/240, so the verdict is unaffected.
6. G-NEG cannot fail in this model: with no events, all arms are identical (largest rel 0). It is implemented as declared, but it has no discriminating power.

**Recomputed:**

I reran 'uv run python Grid_Demand_Response/checks/dr_h1.py'; the output is byte-identical to the pinned dr_h1.txt under cmp (about 3 min 05 s). I checked by hand: lambda_DFS = 44/(121*24) = 1/66 (121 days from Dec 1, 2024 to Apr 1, 2025); nmax_OWN at D1100/H4 = floor(100/4.1) = 24; OWN's zero-slack x* at the last offer = (0.1 + 1000)/4 = 250.025, which matches rule_xstar. The G-POS counts follow from the grid. WALL: pi strictly between ETM's and WALL's x* gives 2 values x 8 cells for H = 1 and 3 values x 8 cells for H = 4 in each overhead setting, so 80. Adding pi in {2, 5, 10, 20} in the 8 binding cells gives 112. OWN: 7 values of pi above ETM's x* x 8 binding cells = 56. Both SOURCED quotes appear verbatim in dr1_f2 (line 290) and dr1_f4 (line 359); verify.txt lists the Kokolis quote as found in the fetched PDF text.

**Summary:**

I found no major fidelity break. The script implements the declared arms (WALL, OWN, ETM; H0 for context, TIER left to H2), the declared Q, and the three gate lines, and every verdict word is computed from numbers. The output reproduces byte-identically and the key counts check out. The reported 'Q holds' rests on reading B, which the check chose itself and the declaration does not specify. Under reading B, 24 of 32 cells pass vacuously: OWN's x* equals ETM's there and WALL's is flat as slack falls. Reading A fails in those 24 cells, and at the sourced DFS rate OWN departs from ETM with probability 5e-5. The check also reads 'R' as R + S, which only matters in the extra Kokolis cells it added itself; on the declared EPS2 units the verdict is the same. These qualifications belong in the write-up, but they do not overturn the result.

### H1, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q-b reading B is lenient, and the RESULT line hides this. In 24 of 32 scored cells OWN's and WALL's x* stays flat at (R+S)/H and (H+R+S)/H while the slack falls (for example by 45.1 h at D=1100, H=1). Reading B counts 'never falls' as satisfied, so Q-b holds there with no rise at all. In the 8 binding cells the 'rise' is a single step at zero slack (the all-or-nothing deadline cliff), not a graded rise. Reading A fails (8 of 32), yet the RESULT line prints only 'Q holds'. The reading is a printed CHOICE and is defensible: with flat identical payments slack has no option value, so a flat x* is the correct economics. It was present from the first committed snapshot (0847be3), so there is no evidence of post-hoc selection. Minor, but the RESULT line should carry the reading-A outcome.
2. Q-a and G-ZERO read the declared 'R' as R+S. The declaration says 'ETM's minimum acceptable payment is R/H' and 'ETM's stake beyond R is exactly 0'. In the 16 Kokolis cells (S = R = 1/12 h), ETM's x* is 2R/H and its stake beyond R is S = 1/12. Read literally, Q-a and G-ZERO would fail in those cells. The script discloses this as a CHOICE (drlib's), and the Kokolis cells are an author addition. On EPS2's cells alone (S=0) the verdict is unchanged, and the declaration's H4 itself treats save overhead as ETM's cost. Minor.
3. The G-POS counts are inflated by exact-rational differences that are vanishingly small. At lambda=1/240, OWN's and WALL's expected shortfall against ETM is E[(N-24)+] = 6.9e-16 events. So 8 of WALL's 112 and 14 of OWN's 56 counted combinations rest on shortfalls of that order. A float recomputation with a 1e-12 tolerance gives WALL 104 and OWN 42. G-POS still holds robustly (WALL at pi 0.2/0.5 in every cell, OWN in the lambda >= 1/66 binding cells). Minor.
4. Q-a's 'at every offer' holds only because the scored grid gives ETM own-step slack far above the season's total overhead: ETM's nmax is 1000, against 41 offers. In the disclosed boundary cell (D=1002, ETM nmax 20), Q-a fails at 21 of 861 states with a stake of 1000. This is disclosed and is sensitivity only, but it bounds the claim's scope.
5. lambda_DFS = 44/(121x24) reads the report's monthly table as Dec 2024 to Mar 2025. The same dossier (dr1_f2) states that DFS became year-round from 27 Nov 2024 and that the winter data period ran 27 Nov 2024 to 28 Mar 2025. The choice is disclosed; an annualised rate would be about 3x lower. It does not decide a verdict, because the ASSUMED rates span 1/240 to 1/12.
6. G-NEG is trivially satisfied by construction: with no events every arm is identical, so the rel is exactly 0. It carries no information about the model.

**Recomputed:**

I wrote my own float backward induction in /tmp/claude-0/dr1_skeptic/h1.py, separate from drlib, using the same model: slots at 24k < 1000, K=41, p = 1-exp(-24 lambda), valuation 1000*1[met] minus the charge, payment pi*H, ties accept.

- **OWN's largest shortfall:** 11.45125587 events at A-D1100-H4-lambda=1/12, pi=0.05. This matches the reported 11.451256.
- **x* in the binding cell A-D1100-H4-a3, found by bisection on pi:**
  - OWN is 0.025 at (k,n) = (0,0), (30,10) and (40,23); at zero slack it is 16.877 (k=24), 25.941 (k=30) and 250.025 (k=40).
  - WALL is 1.025 away from zero slack, and 251.025 at (40,24).
  - ETM is 0.025 at every tested state.
  - These values match the reported ranges 0.025-250.025 and 1.025-251.025, and ETM's x* = R/H.
- **G-POS in floats (1e-12 tolerance):** WALL 104 and OWN 42, against the reported 112 and 56. The differences are exactly the lambda=1/240 binding combinations (8 WALL, 14 OWN). There my exact-rational tail E[(N-24)+] is 6.9e-16 events, positive but negligible, so the exact counts are arithmetically right.
- **Counts derived by hand, all matching:**
  - 861 states per arm per cell (the sum of k+1 over k=0..40) x 32 cells = 27552.
  - Monotonicity pairs: 24x2x820 + 8x2x684 = 50304.
  - Zero-slack offers: k = 24..40 gives 17 x 16 arm-cells = 272.
  - OWN nmax = floor(100/4.1) = floor(100/(25/6)) = 24.
  - Boundary cell: ETM nmax 20, and 861 - 21 = 840.
- **Rerun:** a full rerun of dr_h1.py is byte-identical to the pinned dr_h1.txt (cmp).

**Summary:**

I could not refute the check. Every key number I recomputed independently matches: OWN's largest shortfall 11.451256, the x* ranges, the ETM x* identity and the state and pair counts. The pinned output reproduces byte-identically. The verdict words follow from the numbers under the printed CHOICES. The G-POS counts differ from a float recomputation (104 and 42 against 112 and 56) only through shortfalls of about 1e-16 events, which do not change the verdict. The substantive weaknesses are interpretive, and all are disclosed. First, 'Q holds' rests on reading B: OWN's and WALL's x* is flat in 24 of 32 cells and steps up only at the zero-slack deadline cliff, and reading A fails 8 of 32; the RESULT line should say so. Second, the declared 'R/H' and 'stake beyond R' are read as (R+S) in the author-added Kokolis cells. Third, Q-a's universality depends on ETM's large own-step slack; the boundary cell fails. None of these is a bug or a fabricated source, and none reverses the declared verdict on EPS2's own cells.

### H1, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q-b is decided by the reading chosen for 'rise as the slack falls', and that choice is printed. Reading B passes a cell where x* is flat, because it only asks that x* never falls and that it rises strictly wherever zero slack is reachable. In 24 of 32 cells OWN's nmax (85-454) is above K = 41, so zero slack is never reached. There OWN's and WALL's x* stay flat at R/H and (H+R)/H while the wall slack falls by up to about 45 h (D1100-H1: from 100 to about 55 h). In those cells OWN's x* equals ETM's at every state. Reading A (a rise in every cell) fails in 24 of 32 cells. The headline RESULT line says only 'Q holds' and does not mention reading A. This is a printed choice that decides the verdict, so it is minor, but the report must carry it.
2. Even where it occurs (the 8 D1100-H4 cells), the rise is not gradual. x* is flat at R/H (OWN) or (H+R)/H (WALL) for n = 0..23 and jumps at n = 24, the last event the slack absorbs (to 16.88-250.025 for OWN in A-D1100-H4-a3). This follows from the printed choice of the same flat pi for the rest of the season, which removes any option value of slack. A declining or random future price would give a gradual rise, which would strengthen Q-b, not flip it.
3. Q-a and G-ZERO are scored against (R + S)/H and 'stake - rate (R + S)', not the declaration's literal 'R/H' and 'stake beyond R'. Read literally, the 16 Kokolis cells (S = 1/12 h) would fail Q-a (x* = 1/24 or 1/6 against R/H = 1/48 or 1/12), and G-ZERO would fail too (stake beyond R = 1/12), so Q would fail and the gate would close. The reinterpretation is printed as a CHOICE (the save counted as pause overhead), the RESULT line writes '(R + S)', and it is economically defensible. The declaration itself (H4, H6) keeps save and restart separate, so this is a verdict-deciding reading of a declared symbol that the report should name. The S = 0 (EPS2) cells hold under either reading.
4. Q-a holds by construction on the scored grid. K (R + S) is at most 6.83 h against an own-step slack of 100 or 500 h, so ETM's own-step deadline never binds. The printed boundary cell (D = 1002, lambda = 1/12) shows Q-a fails once the slack is below the season's overheads (840 of 861 states; stake beyond R up to 1000). D is ASSUMED from EPS2 and the dependence is printed in the sensitivity section, so this is minor.
5. Excluding states past the deadline (slack < 0) from the monotonicity test is verdict-relevant. In the D1100-H4 cells OWN's and WALL's x* falls back to 0.025 and 1.025 once the deadline is lost (136 such states per arm per cell). Including them would give violations. The exclusion is printed and counted, so this is minor.
6. The Q line's wording is ambiguous. 'reading A ... fails (8 of 32 cells)' reads as if 8 cells fail, but 8 is the number of cells in which reading A HOLDS, and 24 fail. The author's summary repeats the ambiguity ('fails, 8 of 32').
7. Checked and fine:
   - lambda_DFS: the report's own period is 27 November 2024 - 28 March 2025 (dossier line 292), which also spans 121 days, so the calendar-month CHOICE gives the same 1/66. All four rates give identical verdicts in any case.
   - Both SOURCED quotes appear verbatim in dr1_f2 (line 290) and dr1_f4 (line 359).
   - The Kokolis overheads are correctly labelled as the paper's modelling assumption.
   - All ASSUMED inputs (R = 0.1, D, H, pi grid) match EPS2 T1 (eps2_01.py lines 11-12 and 80).
   - No sourced-looking number is unsourced.

**Recomputed:**

I reran dr_h1.py, and its output is byte-identical to the pinned dr_h1.txt (cmp).

I also wrote an independent backward induction from scratch (Fractions, my own Poisson p, V(n) = 1000·1[met] − charge) for cell A-D1100-H4-a3 on all 9 grid prices. Expected accepted events:
- WALL: 0 for pi ≤ 0.5, 23.999998 for pi = 2-10, 25.637899 at pi = 20;
- OWN: 0 for pi ≤ 0.02, 23.999998 for pi = 0.05-10, 27.695428 at pi = 20;
- ETM: 35.451253 for every pi ≥ 0.05.
All match the pinned table exactly. OWN's shortfall at pi = 0.05 is 35.451253 − 23.999998 = 11.451255, which matches the printed 11.451256 to rounding.

I confirmed from the output:
- Only the 8 D1100-H4 cells reach zero slack (nmax 24 < K = 41).
- OWN's and WALL's x* are flat in the other 24 cells.
- The rise in the 8 cells is a single step at n = 24.
- 272 = 8 cells × 17 offers × 2 arms.
- The dossier's DFS period (27 Nov 2024 - 28 Mar 2025) also gives 121 days.

**Summary:**

Not refuted. The arithmetic is correct: an independent from-scratch backward induction reproduces the expected-event table and G-POS's shortfall, and the script reproduces byte for byte. The sourced quotes are verbatim in the dossiers, and the ASSUMED inputs match EPS2 T1. The verdict does depend on printed choices, all of them minor. (1) Q-b counts as holding under reading B, which passes flat x*. In 24 of 32 cells OWN's and WALL's x* never rise, and OWN's equals ETM's. Where a rise occurs it is a single cliff at the last event the slack absorbs. Reading A fails in 24 of 32 cells, and the RESULT line omits it. (2) Q-a and G-ZERO use (R + S)/H in place of the declared R/H. Read literally, the 16 Kokolis cells would fail both, and the gate would close. (3) Q-a holds by construction because the own-step deadline never binds at EPS2's D; the boundary sensitivity shows this. (4) Excluding states past the deadline is what keeps the monotonicity test clean. The 'fails (8 of 32 cells)' wording should say that 8 cells hold. The report should state the verdict as 'Q holds under reading B with (R + S) as the pause overhead; reading A fails in 24 of 32 cells'.

---

## H2

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H2: Q fails; G-ZERO holds (max |ETM stake - R| = 0.000000 over 328 event counts, x* == R/H at 6888 of 6888 offer states); G-NEG holds (no events: ETM ahead of WALL by > 1 % on 0 of 288 outcome comparisons)

### H2, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. G-POS is neither printed nor noted in H2. The declaration's gate is stated for 'all eight' checks; G-POS is defined on H1's cells, and dr_h8.txt says 'G-POS is H1's; not printed', but dr_h2.py prints only G-ZERO and G-NEG and gives no such note. Minor: it is a reporting gap, and the verdict does not change.
2. G-NEG is trivially true by construction here. With offers = (), H has no effect, so the 72 'cell x pi combinations' contain 4x duplicates (only 18 distinct D x pi cases). The '0 of 288 outcome comparisons' therefore overstates how much independent evidence there is. Minor: the declaration defines G-NEG exactly as 'no events offered'.
3. The Q failure is arithmetic forced by the ASSUMED R. With a linear throttle every tier supplies exactly 1 unit of energy per hour of wall delay, while ETM supplies H/(H+R). So rel = R/(H+R) in every cell, and Q fails if and only if R > H/99. R = 0.1 has no source (the eps2 dossier says so), and Sensitivity 1 shows 8/8 cells within 1 % at R = 0.01. The verdict is honest for the declared EPS2 T1 setting, but it is a statement about the assumed R, not about tiers against ETM. The report should say this plainly.
4. C1 reads the sourced 'average throughput reduction over a 3-6 hour period' as a continuous throttle with zero overhead. I checked the alternative reading by hand, not with a script: a duty-cycle pause of x*w hours per event that carries the same R. Under it Q still fails (for example H=1: 50 % tier 0.5/0.6 against ETM 1/1.1, rel about 8 %), but the direction flips (ETM ahead). So the printed direction '34 of 34 breakpoints ETM behind' depends on C1. The fail verdict does not.
5. The scored power curve is linear and ASSUMED. With an idle-power (affine) curve, tiers supply less than 1 unit of energy per delay hour; Q still fails, but ETM would be ahead. Only a knife-edge curve would bring the rel within 1 %. The one sourced point (POLCA, a peak-power figure) pushes the tiers further ahead (0/8 cells within). The verdict is robust; the direction is not.
6. The matched-delay frontier (C3, fleet mixing, lines through the origin) is a CHOICE and is not in the declaration. It is the reading most favourable to ETM: the discrete Sensitivity 3 gives larger rel (0.0244 to 0.2683), and 0/48 points are within. So no alternative reading rescues Q.

**Recomputed:**

I ran dr_h2.py twice. Both outputs are byte-identical (cmp) to each other and to the pinned dr_h2.txt, whose sha256 is 003a832dd6ff235be8767a882f58121cff0f9f18f760ade17a968b93bef57967, matching the report.

Hand-checked against drlib.Model:
- ETM per event: energy H, wall delay H + R, so energy per delay hour is H/(H+R) (10/11, 30/31, 40/41, 60/61).
- TIER per event: energy x*min(H,w), delay x*min(H,w), so energy per delay hour is 1 under the linear curve.
- Hence rel = R/(H+R): 1/11, 1/31, 1/41, 1/61. This matches the per-cell max rel.
- The fail threshold is R* = H/99; rel at R* is exactly 0.01, which counts as within (the test is non-strict).
- TIER-50%/6h at D = 1100, H = 6 has n_use 33 (33*3 = 99 <= 100 < 102); ETM's reach there is 246/99 = 2.4848.
- Sensitivity 1: R = 0.025 gives 0.02439 at H = 1 and within 1 % elsewhere, so 6/8. R = 0.01 gives 0.0099, so 8/8.
- Sensitivity 2 slopes: 0.22/0.1 = 2.2; (1 - 0.65)/0.25 = 1.4; (1 - 0.4333)/0.5 = 1.1333.
- Sensitivity 3 spot check, D = 1100, H = 4, TIER-25%/3h: ETM takes 7 events (28.7 h), E 28 against 30.75, rel 0.0894.
- G-ZERO state count: 8 cells x 861 offer states (41*42/2) = 6888.
- The quoted sources (Colangelo arXiv:2507.00909 Flex tiers and the 3 h event; POLCA arXiv:2308.12908 22 %/10 %; the eps2 dossier's R caveat) appear verbatim in dr1_f1, dr1_f4 and eps2_2026-09-29.md.

**Summary:**

I could not refute the result: 'Q fails' at R = 0.1 is correct. The code implements the declared H2 faithfully:
- the arms are ETM against the 10/25/50 % tiers over a 3-6 h window;
- the comparison is at matched job delay, with the declared 1 % tolerance;
- G-ZERO and G-NEG are printed;
- every verdict word, and the 'forecast wrong' word, is computed from exact rationals;
- the declaration is not edited, and the post-first-run changes are listed.

The fail is exact and arithmetically forced: rel = R/(H+R) > 1 % whenever R > H/99. It survives every alternative reading I tried: the discrete single-job reading, the duty-cycle-pause tier reading, affine or POLCA power curves, and paused idle power.

The minor issues:
- The verdict depends entirely on the unsourced R = 0.1; with R <= 0.01 it holds 8/8.
- The printed direction (ETM behind the best tier) depends on the throttle reading C1 and the linear power curve.
- G-POS is not printed or noted in H2.
- G-NEG is trivially true, and its 288 comparisons contain duplicates.

Files: /home/user/ashes_crr/Grid_Demand_Response/checks/dr_h2.py, /home/user/ashes_crr/Grid_Demand_Response/checks/dr_h2.txt, /home/user/ashes_crr/Grid_Demand_Response/checks/drlib.py, /home/user/ashes_crr/Grid_Demand_Response/DECLARATION.md.

### H2, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. The verdict 'Q fails' comes entirely from the ASSUMED restart overhead R = 0.1 h, which no source supplies. The gap is exactly R/(H+R) in every cell, so Q fails whenever R > H/99 and holds whenever R <= H/99. Sensitivity 1 shows this: 8/8 cells within 1 % at R = 0 and at R = 0.01, 6/8 at R = 0.025. The dossier's own source goes the other way: Colangelo et al. write 'Control overhead of power capping is negligible', and EPS2 notes that the Phoenix trial treats checkpoint overhead as negligible. The script prints all of this, but the RESULT line reads 'Q fails' with no fragility qualifier. A reader of that line alone would not learn that the verdict flips inside the sensitivity range. This is disclosed, so it is not a hidden deviation. It is still a wording weakness.
2. The 8-cell grid is really 4 independent numbers. rel = R/(H+R) does not depend on D, K, the tier fraction x or the window w: every tier has slope 1 under linear power, and ETM has slope H/(H+R). The D = 1500 cells and all tier choices therefore add nothing, and '0 of 8 cells' and '34 of 34 breakpoints' overstate how much independent evidence there is.
3. At H = 1 and H = 3 the w = 3 and w = 6 tiers are identical (min(H, w) = H). They appear as duplicate rows and inflate the breakpoint and feasible-tier counts.
4. G-ZERO (stake beyond R = 0 at 328 event counts; x* = R/H at 6888 of 6888 states) and G-NEG (0 of 288 with no events offered) hold by construction in this model. They cannot fail, so they add no information to H2.
5. Sensitivity 2 uses POLCA's peak-power figure (22 % at 10 % performance) as an average-power curve. The script labels it 'a peak-power figure', but it still reads a peak reduction as an average one. The (0, 0) endpoint (no idle power) is ASSUMED and flatters the tiers further. The effect is sensitivity only, not scored.

**Recomputed:**

Independent exact-rational code at /tmp/claude-0/dr1_skeptic/recompute_h2.py, with no drlib. It rebuilds the offer schedule (K = 41, hours 24..984), the per-event arithmetic (ETM: energy H, delay H+R, n <= (D-W)/R; TIER: energy and delay x*min(H,w), n <= (D-W)/(x*min(H,w))), the fleet-mixed linear frontiers and the best-feasible-tier rule, checked on a dense 100-point grid in (0, Delta_top]. Results:
- Per-cell max rel: 1/11, 1/31, 1/41, 1/61 at H = 1, 3, 4, 6, identical for D = 1100 and D = 1500. This equals R/(H+R), so Q fails, matching the script.
- ETM slope 40/41 at H = 4.
- ETM reach 2.0000 in 7 cells and 2.4848 at D = 1100, H = 6, where TIER-50%/6h has n_use = 33.
- Sensitivity 1: 8, 8, 6 and 0 of 8 cells within 1 % for R = 0, 0.01, 0.025, 0.1.
- Sensitivity 2: tier slopes 2.2, 1.4 and 1.1333; 0 of 8 cells within.
- R* = H/99 (4/99 at H = 4) gives rel exactly 1/100.
- G-ZERO max |stake - R| = 0.
Rerunning dr_h2.py twice gives output byte-identical (cmp) to the pinned dr_h2.txt, sha256 003a832dd6ff235be8767a882f58121cff0f9f18f760ade17a968b93bef57967. The quoted sources are present verbatim in dr1_f1 (Flex 1-3 tiers; 3 h event) and dr1_f4 (the POLCA 22 %/10 % sentence).

**Summary:**

Not refuted. Every key number reproduces exactly from first-principles code: per-cell max rel = R/(H+R) (1/11, 1/31, 1/41, 1/61), the 34 of 34 breakpoints with ETM behind, reach 2.0 and 2.4848, the sensitivities 8/8/6/0 of 8 and 0 of 8, and R* = H/99. The verdict words are computed from the numbers, the pinned output is byte-reproducible, and the sourced inputs are quoted verbatim in the dossiers. 'Q fails' and 'the forecast is wrong' are correct for the declared setting (R = 0.1). The main caveat is minor: the failure depends entirely on the unsourced, ASSUMED R being above H/99, and a sourced statement calls power-capping overhead negligible. The failure is really that restart overhead makes ETM a slightly worse-than-linear tier. The RESULT line should carry that R-fragility, and the 8-cell grid holds only 4 independent numbers. The gates hold by construction.

### H2, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Minor (printed choice that decides the verdict): 'Q fails' is decided entirely by the ASSUMED restart overhead R. Under the scored linear throttle curve every tier supplies exactly 1 unit of energy per hour of delay, and ETM supplies H/(H+R). So the 1 % test reduces to R/(H+R) <= 0.01, i.e. R <= H/99: 36 s at H = 1 and 109 s at the sourced H = 3. The check prints this (the R* lines and Sensitivity 1: 8, 8, 6 and 0 of 8 cells for R = 0, 0.01, 0.025, 0.1), so it is reported, not hidden. The report should still say plainly that H2's Q is a test of R/H, not of the contracts.
2. Minor (labelling): R = 0.1 h is printed as ASSUMED with the EPS2 dossier's words 'no fetched source supplies or contradicts that number', and the author's assumed_inputs says 'no source supplies it'. The DR1 F4 dossier does supply restart components: MegaScale initialisation 1047 s, 361 s, under 5 s and under 30 s; ByteCheckpoint TLoad 129.49 s and 265.73 s; ByteRobust about 10 min. The sibling check dr_h4 parses these into a sourced restart grid of 5 s to 1200 s. R = 0.1 h (360 s) sits in the middle of that range, so the assumption is consistent with the sources. But 2 of the 10 sourced values (5 s and 30 s, initialisation only) would make Q hold in all 8 cells (with S = 0), and the other 8 make it fail. H2 does not cross-reference F4 or H4 on this point. That should be printed; it is not a fabricated source.
3. Minor: save time S = 0 is ASSUMED. The sourced F4 save times (0.34 s to 2520 s) would lengthen ETM's delay per event. Idle power while paused (ASSUMED 0) would cut ETM's curtailed energy. Both move ETM further behind the tiers, so neither can flip Q to holds, but neither is run as a sensitivity.
4. Minor: in Sensitivity 2, POLCA's (0.9, 0.78) point is a PEAK server-power figure, and the script says so. The (0, 0) origin is ASSUMED even though the script itself notes that real GPUs draw idle power. The result (tiers 13-59 % ahead, 0 of 8 within) only strengthens 'fails', so it does not decide the verdict.
5. Observation, not a defect of the check: the declared forecast 'Q holds' was already contradicted by EPS2 T1's own reference point. At R = 0.1 and H = 4, rel = 1/41 = 2.4 % > 1 %.
6. Other alternatives I checked do not flip Q to holds. A different rel denominator gives R/H = 2.5 % at H = 4. Implementing a tier as a partial full pause makes throttling still the best tier. Without fleet mixing (Sensitivity 3, C3 dropped) 0 of 48 points are within. The wall-clock delay reading is the natural one. C5's tie rule is irrelevant because all tiers have slope 1 under the linear curve.

**Recomputed:**

Reran dr_h2.py twice: both outputs are byte-identical (cmp) to the pinned dr_h2.txt, whose sha256 is 003a832dd6ff235be8767a882f58121cff0f9f18f760ade17a968b93bef57967, as reported. By hand, per-cell max rel = R/(H+R) with R = 0.1: 0.1/1.1 = 1/11 = 0.090909, 0.1/3.1 = 1/31 = 0.032258, 0.1/4.1 = 1/41 = 0.024390, 0.1/6.1 = 1/61 = 0.016393. All exceed 0.01, so 0 of 8 cells are within and Q fails. The threshold is R* = H/99, and at R* rel is exactly 0.01. Breakpoint count 3+3+6+5+3+3+6+5 = 34, with ETM behind at all 34. TIER-50%/6h at D = 1100, H = 6: n_use = floor(100/3) = 33 and emax = 99, so ETM's reach is 246/99 = 2.4848. Quotes checked verbatim in the dossiers: 'sustain the reduction for 3 hours' (dr1_f1 line 323), 'Flex 1: up to 10% performance (average throughput) reduction allowed over a 3-6 hour period' (dr1_f1 line 313), POLCA 'reduces the peak server power by 22% while only impacting the performance by 10%' (dr1_f4 line 585). EPS2 T1 uses R = 0.1 and D = {1100, 1500} as stated.

**Summary:**

Not refuted. 'RESULT H2: Q fails' is computed correctly and reproduces byte-for-byte, and G-ZERO and G-NEG hold as printed. The verdict is decided by a single input, the ASSUMED restart overhead R. Under the linear throttle curve the 1 % test is exactly R/(H+R) <= 0.01, so Q would hold for R up to H/99. The check prints this (R* lines, Sensitivity 1), which makes it a minor issue rather than a hidden choice. R = 0.1 h is consistent with the sourced F4 restart range (5 s to 1200 s, used by dr_h4). The label 'no source supplies it' is inaccurate for DR1, though: 2 of the 10 sourced restart values would flip Q to holds, and H2 does not say so. Every other alternative I tried leaves Q failing, and most widen the gap: the POLCA curve, idle power while paused, save time S > 0, other rel denominators, and no fleet mixing. No fabricated source was found; all quoted sources match the dossiers verbatim.

---

## H3

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H3: Q holds; G-ZERO holds (max |ETM stake - R| = 0.000000 over 12300 (job, event count) pairs, x* == R/H at 258300 of 258300 offer states); G-NEG holds (no events: ETM ahead of WALL by > 1 % on 0 of 10854 outcome comparisons)

### H3, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. The part 'gap largest for tight-slack jobs' depends on the tercile CHOICE (C4), and the per-job shape runs the other way inside the binding region. For the jobs whose slack cannot absorb all 41 events (9/25/33 jobs at H = 1/3/4), the gap rises with slack: Spearman +1.0 in every cell (my computation from the pinned table). The tightest job (5 h) has gap 27.03/8.33/6.25; the largest gap is 1000/333.33/250, at slack 45/125/165 h. The terciles read 'yes' only because every nonzero gap lies in the bottom 34 jobs. With 4 groups H = 4 fails, and with 5 or 10 groups H = 3 and 4 fail (the script's own Sensitivity 1). Over all 100 jobs the rank reading still favours tight jobs (Spearman(gap, slack) = -0.49/-0.72/-0.75, my computation), so the verdict word is defensible under the declared-open wording and is disclosed. But 'rise as the slack falls' does not hold per job; the gap is an artefact of the value cliff at the deadline, amortised over the events left after the bust.
2. 'ETM flat at R/H' and G-ZERO both hinge on the ASSUMED slack spread 5i h, whose tightest job (5 h) sits just above K*R = 4.1 h. The script says so explicitly. Under spread 1i h, 0.05i h or spacing 12 h (K = 83), flatness fails (96, 19 and 99 of 100 jobs at R/H). G-ZERO would also fail there, but it is computed only on the three scored cells, not the sensitivity cells. The declaration's 'in every cell' is read as the scored cells. This is disclosed, not hidden, but the verdict is not robust to an unsourced input.
3. G-NEG is tautological here: with offers = () every arm plays identically. It is also looped over H although the offers do not depend on H, so the 10854 comparisons are 3 identical copies of 3618 (count inflated, verdict unaffected).
4. G-POS is not printed. The declaration assigns it to H1 ('in at least one cell of H1'), so no deviation, but unlike dr_h4-h7 the H3 docstring does not say that G-POS belongs to H1.
5. 'Rising' = two or more distinct entry prices (C3) is a weak operationalisation (any heterogeneous firm curve 'rises'). It is acceptable as a declared CHOICE and does not change the verdict here.
6. The script runs about 7 min per run. The header does not flag it as 'rerun by hand', as other long DR/EPS checks do (cosmetic).

**Recomputed:**

I ran dr_h3.py twice: each run took about 6m50s, and both outputs are byte-identical to the pinned dr_h3.txt (cmp). I recomputed from the pinned table: the OWN area at H = 1 is 27.027027 + 31.25 + 35.714286 + 43.478261 + 52.631579 + 71.428571 + 100 + 200 + 1000 = 1561.53, and the tight tercile mean is 1561.53/34 = 45.927 (matches). The second-reading count 35 of 46 is 2 arms x (7+8+8) pi at or above R/H, with OWN 23 yes and WALL 12 yes (matches). The G-NEG count 10854 = 3 H x 9 pi x (100 x 4 + 2) (matches). The EPS2 cross-check rows (1100/1500 x H 1/4) appear in eps2_01.txt with the same p_all values (e.g. 15.730882/14.730882/0.025/6.122561). The sources are real: the Colangelo arXiv:2507.00909 v1 quote is at dr1_f1 line 323, and the R 'no fetched source' sentence is at eps2 line 129. Spearman(gap, slack) over the binding jobs is +1.0 in all cells, and over all 100 jobs it is -0.49/-0.72/-0.75.

**Summary:**

I could not refute H3's result under the fidelity lens. The code implements the declared arms (WALL/OWN/ETM via drlib, which uses exact backward induction verified by play at p_all and at p_all - 1e-6 for 100 of 100 jobs per cell). It implements Q's three parts with every verdict word computed from numbers, and prints G-ZERO and G-NEG as the declaration requires (G-POS is H1's). The output reproduces byte-identically. All inputs are marked ASSUMED, SOURCED, DECLARED or CHOICE, and the sources checked are real. The only post-first-run change is a listed bug fix to the unscored second reading. The weaknesses are disclosed choices that decide the verdict rather than bugs. 'Gap largest for tight-slack jobs' holds only under terciles: inside the binding region the gap rises with slack, and finer groupings fail at H = 3 and 4. 'ETM flat' and G-ZERO hold only because the ASSUMED spread's tightest slack (5 h) exceeds K*R = 4.1 h; other spreads and 12 h spacing fail flatness. I report these as minor and fragile, not as a refutation.

### H3, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Verdict-deciding coarse-graining (C4): the 'gap largest for tight-slack jobs' part holds only because the tight tercile (slack 5-170 h) contains every job whose slack cannot absorb all 41 events (9, 25 and 33 jobs at H = 1, 3, 4), while the middle and loose terciles have zero OWN gap by construction. At job level the prediction's natural reading is contradicted. Among the constrained jobs the gap RISES with slack: the closed form for the critical offer is R/H + W/((K - nmax) H), so the tightest job has the smallest non-zero gap and the largest gap sits just below absorption (45/125/165 h). One job (gap 1000) carries 64 % of the tight tercile's OWN total at H = 1 (1000 of 1561.53). With 5 or 10 groups the part fails at H = 3 and 4, and with 4 groups it fails at H = 4. The script prints all of this, but the RESULT line says 'Q holds' with no qualifier.
2. The flat part holds only because of an ASSUMED input: the slack spread's floor (5 h) is above K*R = 4.1 h, which the script states. ETM is flat at R/H only when slack >= K*R. Under the other ASSUMED spreads (1i h: 96 of 100 at R/H; 0.05i h: 19 of 100) and at 12 h spacing (K = 83, K*R = 8.3 h > 5 h; 99 of 100), 'flat' fails and Q fails. Counting every unscored alternative, 6 of 10 (3 grouping, 2 spread, 1 spacing) flip Q in at least one cell. The choices are disclosed as ASSUMED/CHOICE with sensitivities, so this is not an undeclared deviation. It is fragility that the headline RESULT line and the author's summary line do not carry, and the write-up should say 'holds on the scored spread only; fragile'.
3. G-NEG is vacuous by construction. With K = 0 offers, ETM and WALL are identical, and H and pi have no effect, so the 10854 comparisons are 27 copies of the same 100-job comparison (2700 x 4 + 27 x 2). The count overstates the gate's coverage.
4. G-ZERO is near-tautological in this setting. ETM's stake is R per event whenever slack >= (n+1) R, which the chosen spread guarantees for every n < 41. G-POS (declared for cells of H1) is not computed in H3. That is acceptable under the declaration's wording, but it should be noted.
5. Stylistic: the author's key numbers give the area between the curves for H = 1 and 4 only. The pinned H = 3 areas (951.2660 OWN, 1051.2660 WALL) match my recomputation too.

**Recomputed:**

I wrote an independent closed-form recomputation at /tmp/claude-0/dr1_skeptic/h3_recompute.py. It uses exact Fractions. Because the 41 offers are identical and all precede hour 1000, the continuation from offer k at state n is the max over j of (pi*H*j + T(n+j)), with the terminal value T from each arm's own charge and deadline. It does not use drlib; it takes x* from exact line crossings and p_all as the max x* along the accept-all path. Results:
- ETM: 100 of 100 jobs at exactly R/H at H = 1, 3, 4.
- OWN: 10, 26 and 34 distinct entry prices; the highest are 1000.1, 333.366667 and 250.025.
- WALL: 10, 26 and 34 distinct entry prices; the highest are 1001.1, 334.366667 and 251.025.
- Tercile mean gaps: OWN 45.927345/0/0, 27.978411/0/0 and 26.434106/0/0; WALL 46.927345/1/1, 28.978411/1/1 and 27.434106/1/1.
- Areas: 1561.5297 and 1661.5297 (H = 1); 951.2660 and 1051.2660 (H = 3); 898.7596 and 998.7596 (H = 4).
- The largest gap is 1000 at slack 45 h, 333.33 at 125 h and 250 at 165 h. No job's OWN or WALL p_all is below ETM's.
- Sensitivity 1 reproduces: 4 groups fail at H = 4; 5 and 10 groups fail at H = 3 and 4.
- Second reading: the tight tercile is largest in 35 of 46 (11/14, 12/16, 12/16).
- EPS2 cross-check: at D = 1100, H = 4, WALL/OWN/ETM = 15.730882/14.730882/0.025, and the other three cells also match the pinned eps2_01.txt.
- The script was rerun twice: both outputs are byte-identical to each other and to the pinned dr_h3.txt (cmp).
- The H = 3 quote is verbatim in docs/citations/dr1_f1_2026-09-29.md line 323.

**Summary:**

Not refuted. Every scored number in dr_h3.txt matches my independent closed-form recomputation exactly: ETM flat at R/H (100/100), OWN/WALL entry counts and highest prices, tercile gaps, areas, the second-reading 35 of 46, and the EPS2 cross-check. Two runs of the script are byte-identical to the pinned output, and the H = 3 source quote is verbatim. The weakness is interpretive and about fragility, not a bug. 'Largest for tight-slack jobs' holds only because the tercile boundary happens to hold every constrained job. Per job, the gap rises with slack among the constrained jobs, and it fails with 5 or 10 groups. 'Flat at R/H' holds only because the ASSUMED slack floor (5 h) is above K*R (4.1 h). Q flips under the 1i and 0.05i spreads and 12 h spacing. All of this is disclosed as CHOICE/ASSUMED with printed sensitivities, but the RESULT line reports 'Q holds' without a fragility qualifier. G-NEG is vacuous by construction and its comparison count is inflated.

### H3, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. MINOR (a printed choice decides the verdict). The third part of Q, 'the gap is largest for tight-slack jobs', holds only as a tercile mean. Per job the gap runs the other way across the jobs whose slack binds. In the model it equals W/((K - nmax)H), so it rises with slack: at H = 1 it is 27.03 at 5 h, 31.25 at 10 h, and so on up to 1000 at 45 h, then 0 for every job with more slack. The tightest jobs therefore have the smallest non-zero gaps. The tercile mean is 'largest for tight' only because every job with a positive gap falls in the tight tercile, and every other job's gap is 0 (OWN) or 1 (WALL). Read naturally ('the gap falls as slack grows', H1's own wording), this part fails in every cell. It also fails with 4 groups at H = 4, and with 5 and 10 groups at H = 3 and 4. The script prints all of this (non-increasing: no; largest gap at 45/125/165 h; SENSITIVITY 1), but the RESULT line gives 'Q holds' alone. The mean over terciles hides the per-job pattern, the kind of aggregation CLAUDE.md R6 warns against.
2. MINOR (an ASSUMED input decides the verdict, and one statement about it is out of date). 'ETM flat at R/H' holds only while the tightest slack (5 h) is at least K x R (41 x 0.1 = 4.1 h). My closed form, checked against drlib, shows 'flat' failing (99 of 100) once R >= 0.125 h (7.5 min) on the scored spread. That value is inside the range the DR1 F4 dossier sources: Meta RSC restart overhead of about 5-20 min plus about 5 min of save (dr1_f4 lines 359-369), and NCCL initialisation of 1047 s with default tooling (line 145). S = 0 is also ASSUMED against sourced save times of seconds to minutes. R = 0.1 h is correctly marked ASSUMED and sits at the low end of the sourced range, so it is consistent with it. But the script's reason, 'no fetched source supplies R', quotes the EPS2 dossier and is out of date for DR1, whose F4 dossier does give a range. A slack step of 4 h or less, or 12 h spacing (K = 83), also flips 'flat'; both are printed in the sensitivities.
3. MINOR (a label). The 24 h offer spacing (K = 41) is an input number but is labelled CHOICE, not ASSUMED. The declaration requires every input number to be sourced or marked ASSUMED. The sourced programmes are sparser: DFS winter 2024/25 had 44 events over December to March (dr1_f2 line 290), and another sourced programme is capped at 'up to 15 Events and/or 48 hours per term' (dr1_f2 line 832). A sparser schedule helps Q (48 h spacing holds), so the label does not threaten the verdict.
4. MINOR (a printed choice). C1's deadline cliff (the value drops to 0 when the job is late, and the job may let its deadline pass) is what produces the gap's shape (a peak just before the slack absorbs every event). Under a hard deadline the binding jobs would never enter: Q would be not computable, or 'rising' would fail. C1 follows EPS2 T1 and is printed.
5. MINOR (context only; the verdict does not change). The Acun et al. relative-deadline threshold (3-4 x T_min, re-typed in dr1_f1 line 718, not quoted) would put realistic slack far above the ASSUMED 0.5-50 % of W. The script is right not to use it. Larger spreads keep Q holding: 10i h is printed as holding, and my closed form also holds at 20i and 40i h.
6. No fabricated source was found. The H = 3 quote appears verbatim at dr1_f1 line 323 (the '[...]' ellipsis is honest). The EPS2 R quote is at eps2_2026-09-29.md line 129. The 100 MW ASSUMED is at DECLARATION.md line 97. The second-reading bug fix is listed and unscored.

**Recomputed:**

My rerun of dr_h3.py matched the pinned dr_h3.txt byte for byte (cmp identical; the run took 6m56s). An independent closed form for the gap, gap = W/((K - nmax)H) with nmax = floor(slack/(H+R)) for OWN (WALL = OWN + 1) and no gap for ETM when slack >= K R, reproduces the scored tercile means exactly: 45.93/0/0 (H = 1), 27.98/0/0 (H = 3) and 26.43/0/0 (H = 4). A probe calling the repo's analyse/score on the drlib model agrees. Varying the slack step (scored: 5 h): Q fails at 3 h and 4 h; it holds at 4.5 h (H = 4 tight 16.43 against middle 13.89), and at 4.8, 4.9, 4.95, 5.05, 5.1, 5.5, 6, 7, 8, 10, 20 and 40 h. Varying R at step 5 h: 'flat' holds for R <= 0.12 h and fails for R >= 0.125 h (99 to 97 of 100 at R/H up to R = 0.4167 h).

**Summary:**

Not refuted. The arithmetic is right, the rerun is byte-identical, the sourced inputs are quoted verbatim, and the gates compute as the declaration requires. The verdict, however, rests on printed choices and on ASSUMED inputs. First, 'largest for tight-slack jobs' holds only as a tercile mean: per job the gap rises with slack across the binding range, so the tightest jobs have the smallest non-zero gaps, and 4 or more groups fail. Second, 'flat at R/H' holds only because min slack (5 h) >= K R (4.1 h). It flips at R >= 7.5 min, which is inside the DR1 F4 dossier's sourced restart range, even though the script says no source supplies R. Third, the 24 h spacing is labelled CHOICE rather than ASSUMED. Every issue is printed or at worst mislabelled, and none is a hidden deviation, a fabricated source or a wrong verdict word, so all are minor.

---

## H4

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H4: Q fails; G-ZERO holds (max |ETM stake - rate (R + S)| = 0 over 57400 event counts in 1400 cells; ETM x* = (R + S)/H at 1205400 of 1205400 offer states); G-NEG holds (ETM ahead of WALL by more than 1 % in 0 of 16560 no-event comparisons)

### H4, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. G-ZERO is scored as 'ETM stake minus rate (R + S) = 0', but the declaration's gate says 'ETM's stake beyond R is exactly 0 in every cell'. Read literally, the stake beyond R equals S, which is non-zero in the 1300 cells with S > 0 (up to 0.7 h), so G-ZERO would FAIL and the gate would close. The check discloses this as a CHOICE, prints the literal diagnostic (stake minus R = S; 0 on the S = 0 cells), and uses the same reading as H1 and H6. H4 itself declares 'restart and save overheads', so the reading is defensible. Q's verdict is unaffected, but the gate word depends on this reading and the RESULT line does not flag it.
2. Q-a's failure depends on the ASSUMED setting inherited from EPS2 T1 (D in {1100, 1500}, K = 41 offers 24 h apart). D = 1500 can never bind: 41 x (4 + 1.033) = 206 h is less than the 500 h slack, so all 700 D = 1500 cells tie by construction. No tighter D is tried. The failure still holds at D = 1100 alone (H 0.5 and 1 never bind; ratio 1) and at the 12 h spacing (sensitivity), so the verdict does not depend on the D = 1500 cells.
3. The NOT USED list of dossier numbers is incomplete. Unlisted: ByteCheckpoint's 62 s planning time, PyTorch's 'under 4 minutes for up to 30B', DataStates' 'about 3 seconds', CheckFreq's 'just under a minute', ByteRobust's 30-minute checkpoint interval, Bamboo's 77 %. All of them fall inside the grid's range or are not save or restart times, so none could change a verdict. The script's claim to list every unused number is overstated.
4. Components are read as the whole restart (MegaScale initialisation, ByteCheckpoint TLoad), and bounds ('under', 'more than', 'up to') are taken at their stated values. These are disclosed choices, and they only move o inside 0.0014 to 1.03 h. The flat rows and the non-binding cells do not depend on them.
5. The one rise in Q-b (D 1100, H 2) comes from the p_all reading: OWN's p_all jumps from o/H to (o + W/(K - nmax))/H when the slack first binds. The effect is real in the model, but the strict Q-b reading fails anyway because seven rows are flat at 1 (last < first fails). Both readings are printed and both give 'fails', so Q-b is not decisive on its own.
6. The RESULT line prints Q's verdict but not the Q-a and Q-b counts (300/1400 cells, 2/10 rows). They appear only in the Q block.

**Recomputed:**

I ran dr_h4.py twice (about 5 min each). The two outputs were byte-identical to each other and to the pinned dr_h4.txt (cmp).

I recomputed p_all independently with a separate exact-fraction DP (identical offers, bisection on a flat pi):
- D 1100, H 4, o 0.1: ETM 0.025, OWN 14.730882, ratio 589.24. This is the EPS2 T1 cell, reproduced.
- D 1100, H 2, o 0.501389: ETM 0.250694, OWN 250.250694, ratio 998.229917.
- D 1100, H 2, o 0.416667: both 0.208333, ratio 1.
- D 1100, H 3, o 0.001389: ratio 90001.
- D 1100, H 0.5, o 1.0333: both 2.0667, ratio 1.
- D 1500, H 4, o 1.0333: both 0.25833, ratio 1.

All match the pinned output.

Counts checked by hand:
- 10 restart x 14 save x 5 H x 2 D = 1400 cells.
- Binding cells: 140 (H 3) + 140 (H 4) + 20 (H 2 with S in {0.5, 0.7} h, o > 0.439) = 300, which gives Q-a 300/1400.
- 138 distinct overheads; 1380 G-NEG worlds x 2 realisations x 6 outcomes = 16560 comparisons.

The BC Table 8 column order (TBlock, TSave, TLoad) matches the dossier's header, and every F4 quote is verified in verify.txt.

**Summary:**

I could not refute H4's result. The code follows the declaration: the ETM, OWN and WALL arms, overheads taken from the F4 dossier, H over the declared 0.5–4 h, Q split into Q-a and Q-b, and G-ZERO and G-NEG printed. Every verdict word is computed from exact rational numbers.

'Q fails' holds under both the strict and the non-strict readings:
- Wherever OWN's wall-clock slack does not run out within the season, OWN's minimum payment equals ETM's ((R + S)/H). This happens in 1100 of 1400 cells, including H 0.5 and 1 at D 1100 alone.
- The OWN/ETM ratio is flat at 1 in 7 of 10 (D, H) rows and rises once (D 1100, H 2).

An independent DP reproduces every checked number, and the pinned output reruns byte-identically.

The issues are minor:
- G-ZERO is scored beyond R + S, not the declaration's literal 'beyond R'. The choice is disclosed and matches H1 and H6. The literal reading would close the gate but would not change Q.
- The ASSUMED D and K come from EPS2 T1, and D = 1500 never binds.
- The list of unused dossier numbers is incomplete.
- The RESULT line omits the Q-a and Q-b counts.

### H4, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. G-ZERO is scored as 'ETM stake minus rate (R + S) = 0', but the declaration says 'ETM's stake beyond R is exactly 0'. Taken literally, the stake beyond R equals S, which is nonzero (up to 0.7 h) in every cell with S > 0, so the literal gate would read FAILS. This is not major: the choice is printed as a CHOICE, the stake-minus-R diagnostic is printed beside it, the reading is defensible because H4 itself introduces the save as an overhead, and Q's verdict does not depend on it. The final write-up should say this in words.
2. Q-b is scored strictly: the ratio must never rise and must end lower than it starts. Under that rule the 7 rows that stay flat at ratio 1 fail because the ratio never shrinks. The verdict does not depend on this: the non-strict reading also fails (9 of 10 rows), because D 1100, H 2 jumps from 1.000000 to 998.229917 at o 0.416667 -> 0.501389 h. The non-strict Q-a holds in 1400 of 1400 cells, so under non-strict readings Q fails only through that single jump in one row. The jump is real: it is where OWN's slack starts to bind. It does depend on the ASSUMED D and H grid, but the declaration says 'every overhead and length', so one real counterexample is enough.
3. Q-a's failure is largely structural. Wherever OWN's wall-clock slack does not bind, OWN's p_all equals (R + S)/H, the same as ETM's, which EPS2 T1 already shows at D 1500. So the verdict turns on the ASSUMED deadlines D in {1100, 1500}. A tighter D alone would not rescue Q-a at H 0.5 and 1 unless the slack bound there too. This is disclosed as ASSUMED; not an error.
4. G-NEG holds trivially: with no events offered, ETM and WALL go through identical states. This is as the declaration designed the gate, and it adds no information.
5. Four restart values are one component (MegaScale initialisation or ByteCheckpoint TLoad) read as the whole restart, and the bound words ('under', 'more than', 'up to', 'less than') are taken at their stated values. All of this is disclosed as CHOICE and does not bear on the verdict.

**Recomputed:**

I wrote my own first-principles float backward-induction DP in /tmp/claude-0/dr1_skeptic/h4_recompute.py, without drlib. The setting: W 1000, K 41 offers at 24k < 1000; OWN meets the deadline iff W + n(H + o) <= D, ETM iff W + n o <= D; both are charged n o; ties accept. I found p_all by bisection in all 1400 cells, using my own R and S values in seconds.
- Grid: identical to the pinned grid (1400 cells, 138 distinct o).
- Q-a: strictly below in 300 of 1400 cells, with 0 disagreements with the pinned 'below' column.
- Q-b: holds in 2 of 10 rows (D 1100, H 3 and H 4), with exactly one rise, at D 1100, H 2 (last ratio 108.527, matching the pinned 108.526882).
- Every other p_all agrees to rounding: at most 1.4e-3 relative, from the 6-dp table and my bisection tie tolerance on values near 3e-4.
- Hand-checked closed forms for the ratio 1 + W/((K - nmax) o):
  - D 1100, H 3, o = 5 s: nmax 33, ratio 90001;
  - D 1100, H 4, o = 5 s: nmax 24, ratio 42353.94;
  - D 1100, H 4, o = 3720 s: nmax 19, ratio 44.988;
  - D 1100, H 3, o = 3720 s: nmax 24, ratio 57.926;
  - D 1100, H 2, o = 0.501389 h: nmax 39, ratio 998.23.
- EPS2 reference (D 1100, H 4, R 0.1 h, S 0): my DP gives ETM 0.025 and OWN 14.7308823 against the closed form 14.730882353.
- Gate counts: 57400 = 1400 x 41; 1205400 = 1400 x 861 reachable ETM states; 16560 = 1380 x 2 x 6.
- Sources: the ByteCheckpoint Table 8 values (0.34/20.13/265.73 and 0.59/51.06/129.49, under TBlock/TSave/TLoad), the Kokolis wcp/u0 values and the ByteRobust quote appear in the fetched raw texts under /tmp/claude-0/dr1_src/F4. verify.txt reports 311 of 311 fragments found.
- Rerun: I reran dr_h4.py (about 5 min 21 s); its output is byte-identical (cmp) to the pinned dr_h4.txt.

**Summary:**

I could not refute H4's result 'Q fails; G-ZERO holds; G-NEG holds'. An independent DP reproduces the key numbers exactly: 300 of 1400 cells strictly below (Q-a fails), Q-b holding in 2 of 10 rows, and one ratio rise, at D 1100, H 2. The EPS2 reference cell and the closed-form ratios also match. The verdict holds under every reading I tried: strict or non-strict, and ratio or difference. Q-a fails because OWN equals ETM wherever the wall-clock slack does not bind. Q-b fails even non-strictly because the ratio jumps from 1 to 998 where the slack starts to bind. The sourced numbers match the fetched raw texts, and the rerun is byte-identical to the pinned output. All issues are minor and disclosed. The main one is that G-ZERO subtracts R + S where the declaration says 'beyond R'. Read literally, the gate would fail wherever S > 0. The choice is printed, is defensible for H4, and does not affect Q.

### H4, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Printed and ASSUMED, and it decides the verdict: Q-a fails only because OWN's wall-clock slack covers every offer in 1100 of 1400 cells. There OWN's closed form reduces to ETM's (R+S)/H. This is the model, not a bug, and EPS2 T1 already showed OWN = ETM in 3 of its 4 cells. A tighter deadline, D <= about 1020.5 h (slack under 41 x (0.5 + 0.001389) h), makes every cell bind. Then Q-a holds, and Q-b holds too, because the ratio 1 + W/((K - nmax) o) falls strictly as o grows. The deadlines D {1100, 1500} are marked ASSUMED (EPS2's), so this is minor. At EPS2's own D = 1100, Q-a still fails (H 0.5 and 1 never bind), and so do the strict and non-strict readings. The report should say plainly that the verdict turns on the deadline slack.
2. G-ZERO is read as 'stake beyond R + S', not the declaration's 'beyond R'. On the literal reading, the stake beyond R equals S, which is non-zero (up to 0.7 h) in the 1300 cells with S > 0. The reading is printed as a CHOICE with the stake-minus-R diagnostic beside it, but the RESULT line reports only the reframed gate. Minor, since a save is overhead, not stake; the same reading is used in H1.
3. The 24-h offer spacing (so K = 41) is labelled a CHOICE (EPS2 T1), not ASSUMED, though it is an input number. It does not decide the verdict: at 12 h and 48 h spacing Q-a still fails wherever the slack does not bind (D 1500 never binds at any feasible spacing).
4. Several sourced numbers are the author's readings of the source: one component (MegaScale initialisation, ByteCheckpoint TLoad) is read as the whole restart R; bounds ('under', 'more than', 'up to', 'less than') are taken at their stated value; and TBlock, async and visible downtime are read as the save. All are printed beside their values, and none decides Q, which turns on the slack and not on the size of o.
5. Q-b's strict clause ('last < first') fails in the 7 flat rows at ratio 1 by construction, so Q-b says little there. The one real rise (D 1100, H 2, from 1 to 998.23) is the jump from not binding to binding. The non-strict reading also gives Q fails, so the verdict word holds under both readings.

**Recomputed:**

I reran dr_h4.py (5 min 13 s); the output is byte-identical to the pinned dr_h4.txt (cmp). Hand checks:
- EPS2 reference cell (D 1100, H 4, R 0.1): nmax = floor(100/4.1) = 24; OWN = (0.1 + 1000/17)/4 = 14.730882. This matches eps2_01.txt line 19 (WALL 15.730882, ETM 0.025, H0 6.122561).
- D 1100, H 3 at o min: nmax = floor(100/3.001389) = 33, so the ratio is 1 + 1000/(8 x 0.001389) = 90001.
- D 1100, H 2 rise: nmax goes from 41 to 39 at o 0.4167 -> 0.5014; the ratio becomes 1 + 1000/(2 x 0.501389) = 998.23.
- Counts: 57400 = 1400 x 41 event counts; 1380 = 10 x 138 G-NEG worlds.
- All 19 quotes appear verbatim in docs/citations/dr1_f4_2026-09-29.md (Table 8 column order TBlock/TSave/TLoad confirmed at line 187).
- A Poisson (H1-style) offer process would not flip Q-a: at most one event per 24-h slot means at most 41 events, so D 1500 never binds.
- Only a deadline tighter than about 1020.5 h makes Q hold.

**Summary:**

Not refuted. "Q fails" is right under the declaration: the numbers reproduce and the internal checks agree. The failure is structural. Wherever OWN's wall-clock slack covers all 41 offers, OWN's minimum payment equals ETM's (R+S)/H. That happens at every overhead for H 0.5 and 1 at EPS2's D = 1100, and throughout D = 1500. The strict and non-strict readings both give fails, as do alternative spacings and a Poisson offer process. Only a much tighter deadline than EPS2's (at most about 1020.5 h) would flip Q to holds, and that choice is printed as ASSUMED. The sources check out, and nothing presented as sourced is fabricated. Minor issues: G-ZERO is read as 'beyond R+S' rather than the declaration's 'beyond R' (printed as a CHOICE, diagnostic shown); the 24-h spacing is labelled a CHOICE rather than ASSUMED; and the component-as-whole-restart and bound readings of sourced values are printed but do not affect Q. Files: /home/user/ashes_crr/Grid_Demand_Response/checks/dr_h4.py, /home/user/ashes_crr/Grid_Demand_Response/checks/dr_h4.txt, /home/user/ashes_crr/docs/citations/dr1_f4_2026-09-29.md.

---

## H5

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H5: Q holds; G-ZERO holds (max |ETM stake - rate R| = 0 over 194832 (job, H, stagger d, event count) cases; ETM x* = R/(H + d) at 116235 of 116235 offer states; ETM's stagger cost 0 in every row: yes); G-NEG holds (ETM ahead of WALL by more than 1 % in 0 of 3612 no-event comparisons)

### H5, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q-b is close to forced by construction in the scored setting. 'Binding' means N*P > L, and b = floor(L/P) < N then follows, so the 'at a cost' clause (sum of delays > 0) cannot fail. For M-step, b = floor(L/P) jobs per minute gives a 1-minute rise of b*P <= L by definition. So with 100 x 1 MW jobs, Q-b can fail only if L < P = 1 MW/min, and no sourced limit is that low. The informative content sits in CONTEXT B (N = 1: S1 infeasible on 7 of 7 limits; N = 10: S1 meets only 4 of 7) and in the cost tables, and none of them is scored. N = 100 is anchored in the declaration (the H3 portfolio; section 3's fleet), so this is not a deviation. It does make Q-b close to definitional.
2. Q-a is definitional in the model. With idle power 0, no catch-up capacity and a return straight to baseline, the 1-minute rise must equal the curtailed load (100 MW). The declaration frames this with 'so', and the forecast is REDUNDANT, so it is faithful, but it cannot fail. Under the snapback reading of 'rebound peak' (demand above the pre-event baseline; the MICH-snapback quote, and Phoenix's 'staying below the pre-event baseline'), the model's rebound is 0 MW in 9 of 9 cells, not the curtailed load. The script prints this 'above' column openly and adopts the declaration's own step reading. That reading is defensible, but the rebound claim holds only in the step sense.
3. The scored reading of 'at a cost' is deferred job-hours. The alternative reading, a cost in ETM's own valuation, fails 0 of 42 and is printed but not scored. ETM's zero cost follows from the declared ETM definition (deadline counted in own steps), so the scored reading is the one that makes the Q clause non-vacuous. The printout says so openly; the choice does not overturn the verdict.
4. The ramp window decides S1 but not the proposition. Read over a 1-second window, S1 meets the limit in 0 of 63 binding cells. S2 (the power-cap ramp) meets it in 63 of 63 in both windows. If S2 counts as 'a staggered resume', Q-b holds under either window. But S2 is printed and not scored, so the scored S1 verdict depends on the 1-minute CHOICE.
5. Phoenix limit reading: the quote is 'reduce power by 25%... and ramp down and up gracefully over 15 minutes'. The script reads it as 100 MW/15 = 20/3 MW/min, applying the ramp time to a 100 % curtailment, whereas the trial ramped a 25 % reduction. The rate reading would be 25/15 MW/min, which gives b = 1, still feasible, so the verdict is unchanged. The key-numbers summary calls 20/3 'sourced'; it is a derived CHOICE. NPRR-up = 2 MW/min likewise depends on the ASSUMED 100 MW peak.
6. G-POS is not printed ('belongs to H1'). The declaration defines G-POS on H1 cells, so this is consistent, and H4, H6, H7 and H8 do the same. It is flagged only because the declaration says 'The gate (all eight)'.
7. G-ZERO and G-NEG are near-tautological in this model. ETM's charge is n*o regardless of L, and slack >= 5 h > 41*0.1 h, so the stake is always R. The no-event worlds make every comparison identical (largest rel 0). The script implements both exactly as declared. It adds a conjunct (ETM's stagger cost 0), which could only make G-ZERO harder to hold.

**Recomputed:**

I reran dr_h5.py twice (about 72 s each). Both runs are byte-identical to each other and to the pinned dr_h5.txt (cmp). Grid_Demand_Response/DECLARATION.md is unchanged since e67e8ee. I checked by hand:
- S1 summed delays: 2450 min = 40.8333 h (b=2); 784 min = 13.0667 h (b=6); 576 min = 9.6 h (b=8); 450 min = 7.5 h (b=10); 200 min = 3.333 h (b=20); 120 min = 2.0 h (b=30). S2: 100*25 min = 41.667 h.
- Cells: 63 binding and 9 non-binding (3 models x 3 H x the 300 MW/min limit).
- G-NEG: 100*3*2*6 + 3*2*2 = 3612 comparisons.
- Mueller-Jansen: 1 - 32.6/64.8 = 49.69 %. Li: 9.28*1.125 = 10.44.
- WALL season cost at 2 MW/min: 1674.167 to 6674.167.
- OWN and ETM-H: up to 5 and 7 jobs lost.
I brute-forced the exact 1-minute rise function against a 1 s sampled load for all three resume models and b in {2, 6, 8, 10, 20, 30}; every value agrees (2, 6, 8, 10, 20, 30 MW). I also confirmed the S1 minimum-delay argument: any 7 releases must span at least 1 minute. All sourced quotes are present verbatim in the dr1_f1, f3 and f4 dossiers, with URLs, fetch dates and sha256 values. All verdict words (Q, Q-a, Q-b, G-ZERO, G-NEG, the forecast) are computed from the numbers.

**Summary:**

H5 reproduces exactly, is deterministic, and implements the declared Q, arms and gate lines (G-ZERO and G-NEG; G-POS is defined on H1). Every verdict word is computed. I found no bug, no fabricated source and no undeclared change that alters the verdict, so the result stands: Q holds, G-ZERO holds, G-NEG holds.

The main caveats are interpretive and all minor:
- **Q-a is definitional.** With idle power 0, no catch-up and a step back to baseline, the rise must equal the curtailed load. Under the snapback reading, the rebound above baseline is 0.
- **Q-b is nearly forced.** With 100 x 1 MW jobs, b = floor(L/P) makes it hold unless L < 1 MW/min, and the 'cost' clause cannot fail once the limit binds.
- **The scored readings are the favourable ones.** The 1-minute ramp window and 'deferred job-hours' as the cost are both chosen readings. Their alternatives (1 s window: S1 0 of 63; cost in ETM's own valuation: 0 of 42) are printed but not scored.
- **S1 fails at small N.** With 1 or 10 jobs, S1 fails, and this is printed as context only.
- **The Phoenix limit is derived, not sourced.** 20/3 MW/min applies a 15-minute ramp time to a 100 % curtailment; the rate reading gives 25/15, and the verdict is unchanged.

### H5, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q-a is true by construction. Each paused job is modelled as returning to exactly its pre-event draw, so the 1-minute rise equals the curtailed load in every resume model. The verdict also depends on reading 'rebound peak' as the size of the resume step. The sources' own definitions measure snapback as load above the pre-event baseline (PHX-ramp: 'avoiding so-called snap back ... by staying below the pre-event baseline'; MICH-snapback: 'the increase in energy and demand ... following'). On that reading the model's rebound is 0 MW (the 'above' column is 0.000 in 9 of 9 cells) and Q-a would fail 9 of 9. The script prints the choice and the 'above' column, and the declaration's own wording ('resumes at full power at once, so the rebound peak equals the curtailed load') supports the step reading, so this is minor. The report should still say that under the field's definition a lossless pause has no rebound above baseline in this model.
2. Q-b's 'at a cost' test (summed release delay > 0) holds automatically in every binding cell. The reading closer to G-ZERO, a cost in ETM's own valuation, fails 0 of 42 and is printed only as an unscored alternative. It is disclosed, but 'Q holds' rests on the deferred-time reading.
3. PHX-15min limit. The Phoenix quote describes a 25 % curtailment ramped over 15 minutes. For a 100 MW fleet that is about 25/15 = 1.67 MW/min, not the 100/15 = 6.67 MW/min used, which comes from the model's 100 % curtailment. The CHOICE line discloses this, and at 1.67 MW/min S1 still has b = 1, so no verdict changes. The listed cost (13.07 job-hours) is specific to this reading.
4. The sourced NERC Level 2 and Southern Company limits are general large-load ramp limits for normal operation, not requirements for resuming after a demand-response event. The script labels this as a CHOICE; it does not change the verdict.
5. Context C: the Li line prints 'quoted -12.5 %, which the F1 reading says is a rise: yes'. The 'yes' is computed only as equality of magnitudes, because the regex drops the minus sign; it does not check the sign reading it appears to confirm. This is a labelling issue in context only.
6. The event start is itself a 100 MW drop within a minute, far over the 5 MW/min NPRR down limit (printed as context). The stagger analysis covers only the resume, although the Phoenix source requires ramping 'down and up gracefully'. This is within the declared Q, which is about the resume, but the fleet as modelled still breaks the ramp limits at the event start.
7. Both gates hold by construction. G-ZERO holds because every job's slack (at least 5 h) exceeds K*R = 4.1 h, so ETM never reaches its deadline. G-NEG compares two worlds with no events, where the arms cannot differ (every comparison has rel 0). Both are as declared, but neither could have failed in this setup.

**Recomputed:**

I wrote independent code at /tmp/claude-0/dr1_skeptic/recompute.py, using exact Fractions for the schedule and costs and numpy on a 1/190 s grid for load rises. All numbers checked match the pinned output.
(1) S1 schedule, from the pigeonhole bound b = floor(L/P):
  - summed delay in job-hours: 40.8333 at 2 MW/min, 13.0667 at 20/3, 9.6 at 8, 7.5 at 10, 3.3333 at 20, 2.0 at 30, 0 at 300;
  - last release: 49, 16, 12, 9, 4 and 3 min;
  - S2 job-hours: 41.667 at 2 MW/min, 12.5 at 20/3, 10.417 at 8, 8.333 at 10, 4.167 at 20, 2.778 at 30.
(2) Rises on the grid:
  - the simultaneous 1-minute rise is 100 MW under the step, idle and ramp models, and the post-event maximum is 100 MW (no load above the baseline);
  - under S1 the 1-minute rise equals b (2, 6, 30 MW) in all three models, within L;
  - the 1-second rise also equals b, so the 1-second-window sensitivity fails as reported.
(3) Season cost per arm (K = 41, slack 5i, R = 0.1), from my own deadline and charge arithmetic, for H in {1, 3, 4}, limits 2, 20/3 and 8 MW/min, all three orders:
  - WALL: 1674.167 and 6674.167 at H = 1 (0 and 5 jobs missed); 3674.167 and 5674.167 at H = 4;
  - OWN: up to 5000 [5]; ETM-H: up to 7000 [7]; ETM: 0 everywhere;
  - S2 at H = 4, 2 MW/min: 5708.333 [4].
  All match TABLE C1 exactly.
I also re-ran dr_h5.py; its output is byte-identical to the pinned dr_h5.txt (cmp).

**Summary:**

I could not refute H5's reported result. I re-ran dr_h5.py and its output is byte-identical to the pinned dr_h5.txt. Recomputing from first principles reproduces the key numbers exactly:
- the S1 costs in deferred job-hours (40.83, 13.07, 9.6, 7.5, 3.33, 2.0) and the last-release times;
- the S2 costs (41.67 at 2 MW/min);
- the 1-minute and 1-second rises under all three resume models;
- the TABLE C1 season costs per arm, including WALL 1674–6674, OWN up to 5 jobs lost, ETM-H up to 7, ETM 0.
The G-ZERO and G-NEG counts agree with the loop sizes (194832 = 41 x 3 x 1584; 3612 = 6 x 602). Every verdict word is computed from the numbers. The sourced ramp limits parse correctly: NPRR up = min(2 % of 100 MW, 8) = 2 MW/min.

The weaknesses are definitional and all disclosed as CHOICE lines, so none is major:
- Q-a is true by construction and holds only under the resume-step reading of 'rebound peak'. Under the sources' own above-baseline definition of snapback it would read 0 MW and fail 9 of 9.
- Q-b's 'at a cost' holds automatically; the ETM-valuation reading fails 0 of 42.
- The Phoenix limit (100/15 MW/min) scales a 25 % curtailment's ramp to the model's 100 % curtailment.
- The event start itself breaks the ramp limits and is left unstaggered.
- Both gates hold by construction (slack of at least 5 h against K*R = 4.1 h; no-event worlds are identical).
- One context label, the Li sign line, overstates what its 'yes' checks.

### H5, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Job size decides Q-b, and the ASSUMED size conflicts with a source the script itself prints. Q-b holds only because the ASSUMED 100 MW fleet is split into 100 jobs of 1 MW. The LLTF-xai quote in the same output (dr1_f3 line 107) says one training model 'can change the loading 35–70 MW or more within a minute as the model starts and stops'. At that job size every binding limit (all 30 MW/min or less) makes S1 infeasible (b = 0), so Q-b would fail in every binding cell. CONTEXT B already shows the direction: N = 1 gives 0 of 7 and N = 10 gives 4 of 7. The script prints the xAI swing only as context against the limits and never says it contradicts the 1 MW job. This is minor, not refuting: the 1 MW job follows from declared items (§3 says the 100 MW fleet runs 'jobs of the H3 portfolio', and H3 declares 100 jobs), it is printed as ASSUMED, and the N sensitivity appears in the author's key numbers. It should still be stated next to the result.
2. Q-a holds by construction, so it tests nothing. M-step implements the declared premise ('resumes at full power at once'), and the model has no catch-up capacity, so the 1-minute rise equals the curtailed load by construction in all 9 cells. Under the domain's own definition of rebound, quoted in the output (MICH-snapback: 'the increase in energy and demand ... following a demand response event'; Phoenix: snap back means going above the pre-event baseline), the model's rebound is 0 MW above baseline, not 100. The script reads 'rebound peak' as the 1-minute step, which is a printed CHOICE (the 'above' column is 0.000 and Q-a's second condition says the return goes to baseline, not above it). It decides Q-a's wording, so it is minor.
3. M-ramp stretches a short sourced rate. It takes the sourced 1.9 p.u./s, which lasts 'for about 250 milliseconds' (about 0.475 p.u.), as the rate of the whole 0 to 1 p.u. rise. The only sourced facility return (LLTF-field: 'ramps back up to 450 MW over the course of a few minutes') is printed but unused. If one job's return took more than 1 minute, the 1-minute-window Q-a would fail. Printed as a CHOICE; under the declared 'at once' premise M-step decides the result anyway.
4. The 1-minute window decides Q-b for S1. Read over 1 s, S1 meets the limit in 0 of 63 binding cells, because releasing a 1 MW job is an instantaneous step. The sensitivity is printed and reported. S2 (the power-cap ramp) holds under both windows and for N = 1, so Q's substance ('a stagger removes it at a cost') survives if S2 counts as a staggered resume. S2 is printed but not scored.
5. 'At a cost' is read as deferred job time, which is greater than 0 for any stagger by construction. The alternative reading, a cost in ETM's own valuation, fails in 0 of 42 rows. That 0 comes from the CHOICE that ETM's extension covers the stagger; ETM-H, the alternative arm, pays in 21 of 42. Both are printed and disclosed. Two printed choices decide this clause.
6. The ramp limits are CHOICE readings. NERC Level 2's 8–300 MW/min limits are normal-operation limits: the dossier says many entities set none and that it is 'Not supplied: whether the limits bind demand-response recoveries'. The tightest limit (2 MW/min, which drives the 40.83 job-h headline) is a commenter's restatement of the withdrawn NPRR1191. Phoenix's 15-minute ramp was for a 25 % curtailment and is rescaled to the full 100 MW. All of these are labelled CHOICE or withdrawn in the output.
7. Labelling inconsistency: H = 3 is marked SOURCED in the code comment (Phoenix 3-hour events, F1 line 309/323) but printed as ASSUMED. It is harmless, since Q-a and Q-b do not depend on H.
8. No fabricated or unsourced number found. All 16 quotes appear verbatim in the dr1_f1/f3/f4 dossiers (the script checks this at run time and I confirmed several by grep), and the parsed values match. Every other input is printed as ASSUMED, DECLARED or CHOICE.

**Recomputed:**

I reran dr_h5.py (73 s) and it matched the pinned dr_h5.txt byte for byte (cmp).

Recomputed by hand:
- S1 at 2 MW/min: b = 2, 50 batches, sum d = 2 x (0 + ... + 49) = 2450 job-min = 40.833 job-h.
- Phoenix: L = 100/15 = 6.667 MW/min, b = 6, 17 batches, sum d = 6 x 120 + 4 x 16 = 784 min = 13.067 job-h.
- NERC low limit: 8 MW/min gives b = 8, sum 9.6 job-h.
- S2 at 2 MW/min: T = 50 min, 100 x 25 min = 41.667 job-h.
- NPRR up-ramp: min(2 % x 100, 8) = 2 MW/min. NPRR CLR: 20 % x 100 = 20 MW/min.
- Müller & Jansen damping: 1 - 32.6/64.8 = 49.69 %.
- Li: 9.28 x 1.125 = 10.44 MWh.
- G-NEG: 100 x 3 x 2 x 6 + 12 = 3612 comparisons.
- K = 41: offers at hours 24..984, as in EPS2.

The S1 least-delay argument checks out. The limit allows at most b releases in any half-open window (t, t+1 min], so rank r cannot go before floor(r/b) minutes.

With job size P at or above the sourced 35 MW single-model swing, b = floor(L/P) = 0 for every binding limit. S1 is then infeasible and Q-b would fail; S2 would still hold.

**Summary:**

I could not refute H5's result. The script reproduces byte for byte, the arithmetic recomputes, every sourced number comes from a quote found verbatim in its dossier, and every other input is labelled ASSUMED, DECLARED or CHOICE. The choices that decide the verdict are all printed:
- the 1 MW job size (N = 100);
- the 1-minute ramp window;
- 'rebound peak' read as the 1-minute step rather than the rise above baseline;
- 'at a cost' read as deferred job time, not ETM's valuation.

So the issues are minor. The most important one: the ASSUMED 1 MW job conflicts with the sourced xAI figure of a 35–70 MW swing for a single model. At that size S1 becomes infeasible under every binding limit and Q-b would fail; only the power-cap ramp S2 would still remove the peak. Q-a holds by construction: the model implements the declared 'resumes at full power at once' premise and has no catch-up capacity, and the peak above baseline is 0. None of this is a bug, an undeclared deviation, a wrong verdict word or a fabricated source.

---

## H6

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H6: Q holds; G-ZERO holds (max |ETM stake - rate (R + S)| = 0 over 1722 event counts in 42 jobs; ETM x* = (R + S)/H at 36162 of 36162 offer states); G-NEG holds (ETM ahead of WALL by more than 1 % in 0 of 612 no-event comparisons)

### H6, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. G-ZERO wording deviation (disclosed, shared with H1/H4/H8): the declaration's gate is 'ETM's stake beyond R is exactly 0 in every cell'. dr_h6.py tests stake minus rate (R + S). The literal quantity, stake minus rate R, equals rate S and ranges over 0..0.7 h, the script's own printed line. Read literally, G-ZERO would print FAILS on the 39 of 42 lossless jobs with S > 0. The script prints the reinterpretation as a CHOICE and the literal number beside it. Treating the save time as own overhead alongside R is defensible: work is kept, and the declaration's H4 groups 'restart and save overheads' together. So I count this as a disclosed reading, not a hidden flip, but a strict reader could call the gate word a reinterpretation.
2. Q holds by construction, which the script's own NOTE admits. The lossless route meets T iff S <= T. The lossy route always loses I/2 > 0 (all intervals are positive) and always meets T (stop taken as instantaneous). So every S > T cell must satisfy the reading. The 414/414 is arithmetic, not an empirical finding.
3. Latent logic gap, not triggered: if the lossy route could not meet T (for example, if stopping took longer than FFR's 0.25 s), min_lost would be None and qcell would be False. Q would then print 'fails', although the declared Q ('cannot meet the product without losing work') would hold even more strongly. The instantaneous-stop CHOICE hides this.
4. The product count is inflated by near-duplicates. T-FFR15cyc (F2) and T-RRSFFR (F3) are the same ERCOT FFR requirement: the script's own cross-check shows 0.25 s = 0.25 s. T-PJMreal is a realised instance of T-PJM30. So '13 products', the per-product tallies and 'Regulation fits 3 of 14' overstate independent products. Q is unaffected.
5. TBlock (0.34/0.59 s) and the async/visible DCP downtimes are read as the save 'with the hosts staying powered to persist'. This does not fully fit the script's own CHOICE that the fleet's power is down by T. It moves Regulation (4 s) from 1 to 3 feasible saves and FFR/RRS feasibility at 0.34/0.59 s. It affects only the feasible product set, not Q or the gate.
6. Regulation's 4 s deployment cadence is read as a curtailment response time. This is questionable: Regulation is continuous up/down following, not a curtailment product. It is a disclosed CHOICE and affects only the feasible set.
7. The CHOICES say DFS is 'counted as an exclusion', but the output prints no explicit exclusion count. DFS is printed under NOT SCORED only.
8. G-NEG is trivially satisfied: with no events, ETM and WALL are identical in every outcome (largest rel 0). It is implemented as declared, but it carries no information about H6's lossy/lossless routes.

**Recomputed:**

Ran the script twice: byte-identical, and cmp-identical to the pinned dr_h6.txt (about 9 s). DECLARATION.md is unchanged since e67e8ee. The PJM real-event columns in dossier F2 are Notification/Deploy/Release, so 14:00 -> 14:30 = 30 min is parsed correctly. All H6 quotes are present in the dossiers. The ByteCheckpoint Table 8 rows and the POLCA/Perseus quotes appear only as split fragments in the raw PDFs. They are in claims.py, and verify.txt reports 311/311 fragments found, so they are verified in rejoined mode. Hand checks: 13 x 14 x 3 x 3 = 1638 cells. The S > T pairs are 13 (FFR) + 13 (RRS) + 11 (REG) + 2 (ECRS) + 2 (ERS10) + 1 each for ERS30, NSPIN, PJM30, PJMreal and RDRR40 = 46; 46 x 9 = 414, and 1638 - 414 = 1224. Cheaper-lossy cells: PT-legacy 8 products x 3 R x 1 interval (15 min) + GEM 3 products x 3 R x 2 intervals (15 min, 60 min) = 24 + 18 = 42. Ties (30 min save against 60 min interval, 0.15 = 0.15) are correctly not counted. ETM p_all = (R + S)/H, e.g. (0.1 + 0.5)/4 = 0.15. Lossy: (0.1 + 0.125)/4 = 0.05625 and (0.1 + 2)/4 = 0.525. States: 41 x 42/2 = 861 per job, and 861 x 42 = 36162. Event counts: 42 x 41 = 1722. G-NEG comparisons: (42 + 9) jobs x 2 realisations x 6 outcomes = 612. Every verdict word (Q holds/fails/not computable, G-ZERO, G-NEG, forecast right/wrong) is computed from counts.

**Summary:**

I could not refute the reported result. dr_h6.py implements the declared H6 check: Q, the feasible product set, and the G-ZERO and G-NEG gate lines, with computed verdict words. Its output reproduces byte-for-byte and matches the pinned file, and every headline number re-derives by hand. The sourced inputs appear verbatim in the dossiers, and the fragment-split table rows are backed by verify.txt. The main fidelity caveat is disclosed as a CHOICE: G-ZERO tests the stake beyond R + S, not the declaration's literal 'beyond R'. Read literally, the gate would fail on the 39 jobs with S > 0, because the stake minus R equals S (printed). Counting the save time as own overhead is consistent with H1, H4 and H8 and defensible. Q's 414/414 is true by construction (the script's NOTE says so). Other minor issues: duplicate products inflate the product counts, the TBlock and Regulation readings affect only the feasible set, a latent Q-logic gap is not triggered, and no explicit DFS exclusion count is printed.

### H6, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. G-ZERO is scored as 'ETM stake minus rate (R + S) = 0', but the declaration says 'ETM's stake beyond R is exactly 0 in every cell'. Read literally, the stake beyond R equals S, which runs from 0 to 0.7 h and is nonzero in 39 of the 42 lossless jobs (every S > 0), so G-ZERO would FAIL. The script prints this as a CHOICE, matching H4, and prints the stake beyond R alone ('it equals rate S'). The declaration's H4 row also treats save and restart as joint overheads. Because the choice is disclosed and defensible, this is minor, not a hidden deviation. It should still be named in the synthesis as a reading of G-ZERO, not as G-ZERO as worded.
2. The script's NOTE admits that Q holds by construction. Only two routes are allowed: a lossless save-then-drop that meets T iff S <= T, and a lossy instant drop that always loses I/2 > 0. So 414/414 is a definitional result, not an empirical one. A hybrid route is excluded by CHOICE: throttle within the 10 ms SM-frequency or 5 s power-brake latency, then save at reduced power, then drop. That route would meet most products without lost work if a partial or throttled curtailment counts. The script prints the throttle context, but the verdict depends on this exclusion.
3. The reading is inconsistent. Q's third conjunct counts 'stake beyond R > 0' on the lossy route as evidence of lost work. By the same measure, the lossless route with S > 0 also has stake beyond R > 0 (= S), while G-ZERO excludes S from the stake. The measure does not separate lost work from save time. Q still holds through the other two conjuncts, so the verdict is unchanged.
4. The 13 'products' include near-duplicates. ERCOT's FFR definition (15 cycles) and RRS-FFR (250 ms) are the same service. PJM's realised Quick_30 event is one instance of PJM Load Management's 30-min default. This inflates the per-save feasible-product counts and the 414 S > T cells (FFR and RRS-FFR alone give 234 of them) but does not change the verdict.
5. Several readings are disclosed choices, not facts. Regulation's 4 s deployment cadence is taken as a response time. SB 6's 'at least 24-hour notice' is taken as T = 24 h. TBlock and async DCP downtime count as saves with hosts still powered. Stopping on the lossy route is taken as instantaneous. The lossless route saves at full power, with no partial power drop during the save. All are printed as CHOICE. They affect the feasible-product counts, not Q.
6. G-NEG is vacuous as run: with no events, ETM and WALL are identical on every outcome (largest rel 0.000e+00). It passes trivially, as the gate design implies.

**Recomputed:**

My own code is in /tmp/claude-0/dr1_skeptic/recompute.py. It uses exact Fractions, its own list of T and S values typed from the quotes, and its own backward induction with bisection on a flat price. It does not use drlib.
- S > T: 46 of 182 product x save pairs, so 414 cells. Total 1638 cells; converse 1224. All match.
- Feasible products per save: 13, 11, 11, 10 (x9), 8, 3. Saves that fit per product: FFR 1, RRS 1, REG 3, ECRS/ERS10 12, 30-40 min products 13, PJM60/120 and SB6 14. All match.
- Lossy route strictly cheaper than a lossless route that meets T: 42 cells. Matches.
- K = 41. Matches.
- ETM p_all: 0.025 at R = 0.1, S = 0; 0.2 at R = 0.1 with GEMINI's 42 min; 0.045833 with Kokolis's 5 min; 0.258333 at u0 = 20 min with GEMINI. All match.
- OWN p_all at the same four jobs: 14.730882, 12.104762, 13.934722, 11.62197. All match.
- Lossy route at R = 0.1, I = 15 min / 1 h / 4 h: ETM 0.05625 / 0.15 / 0.525 and OWN 13.945139 / 12.65 / 10.525. nmax values also match (e.g. 1000/24, 125/20, 47/16). All match.
- 36162 = 42 x 861 offer states (861 = 41·42/2); 1722 = 42 x 41; 612 = 51 x 2 x 6. All consistent.
- Rerunning dr_h6.py twice gives identical output, and cmp against the pinned dr_h6.txt is byte-identical.
- Spot-checked quotes are in the dossiers' blockquotes (ECRS, Regulation, Non-Spin, SB 6, FFR, RDRR, RRS-FFR, the Kokolis wcp/u0 figures, ByteCheckpoint Table 8, GEMINI, torch.save, POLCA). The PJM 14:00 -> 14:30 Quick_30 lead is read correctly from the Notification/Deploy columns.

**Summary:**

I could not refute H6. All the key numbers I recomputed match exactly: cell counts, feasible-product sets, the 42 cells where losing the work is cheaper, and the ETM, OWN and lossy prices by my own backward induction. The script is deterministic and matches its pinned output byte for byte. The issues are minor and disclosed. G-ZERO is scored as 'stake beyond R + S' rather than the declaration's 'beyond R'; read literally, it would fail in 39 of 42 jobs. Q holds by construction given the two-route CHOICE, which excludes a throttle-then-save route. The 13 products include near-duplicates (FFR and RRS-FFR; PJM30 and the realised PJM event). G-NEG is trivially satisfied. None of these changes a verdict word as the check has declared and printed its readings.

### H6, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q is forced by the model's definitions. drlib.response_ok is S <= T, so the lossless route cannot meet T when S > T, and drlib.lossy sets lost = I/2 > 0, so the lossy route always loses work. The 414/414 'holds' is therefore arithmetic, not a finding. The script says so itself (the NOTE line), so this is minor.
2. G-ZERO checks stake - rate(R+S) = 0, but the declaration's gate reads 'ETM's stake beyond R is exactly 0 in every cell'. Read literally, G-ZERO fails in 39 of the 42 lossless jobs: those with a sourced S > 0, where stake - R = S, up to 0.7 h. The choice decides the gate verdict. It is printed as a CHOICE and the stake-R diagnostic is printed beside it. H1, H4 and H8 use the same reading; H2, H3, H5 and H7 check 'stake - R', but they have S = 0, so they do not conflict. Minor under the lens rules (printed), but the RESULT line reports 'G-ZERO holds' with no qualifier.
3. Latent flaw in the Q-cell reading. qcell requires 'min_lost is not None', meaning some route meets T. The instantaneous-stop CHOICE makes the lossy route meet every product, including the 0.25 s FFR and RRS-FFR and the 4 s Regulation. That choice does not match the sourced power-control latencies in F4: POLCA's power brake is 5 s and OOB capping 40 s; only Perseus' 10 ms frequency change fits. If the stop took the sourced 5 s brake latency, no route would meet those three products. That would be 333 of the 414 S > T cells (117 + 117 + 99). The printed verdict would then flip to 'fails', even though the declared Q ('cannot meet without losing work') would still be true. The choice is printed, but the reading would mislabel under a reasonable alternative.
4. Some saves are read as 'the save before the power drops (the hosts stay powered to persist)': TBlock 0.34/0.59 s, PyTorch async 6.3 s and visible 6-14 s. That conflicts with CHOICE 1, which says the fleet's power is down by T. If the hosts stay powered while the save persists (TSave is 20.13/51.06 s), power is not fully down at TBlock. This inflates the feasible set: Regulation 4 s fits 3 of 14, and 11 of 13 products are feasible at a TBlock save. It does not change Q. The choice is printed.
5. FFR is scored only in its 15-cycle automatic mode. The same sourced definition (F2 line 497) also allows 'a deployment in response to an ERCOT XML messaging instruction within ten minutes'. The printed reason for dropping that mode is that it 'is not in the task's number list', which points to an instruction outside the declaration. Scored in its XML mode, FFR would fit 12 of 14 saves instead of 1. This affects the feasible product set only, not Q.
6. Regulation's 4 s deployment cadence is read as a response time, and SB 6's 'at least a 24-hour notice' is read as T = 24 h. Both readings are printed. Regulation also requires continuous two-way signal following, which a pause cannot provide, so its row in the feasible set is generous. Q is unaffected.
7. A pause in place is excluded by the declaration's own H6 premise ('a lossless pause must save before the power drops'), so it does not refute the check. In this route the state stays in device memory and the GPUs idle, with no save; drlib has an idle parameter. Under it, a lossless route would meet every T with partial curtailment and Q would be moot. It should be listed as outside the declared scope.
8. ByteCheckpoint's stated 62 s planning time for the 405B save (F4 line 181) is not added to TBlock or TSave. Minor; it affects the feasible set only.

**Recomputed:**

I reran dr_h6.py twice: the two outputs are byte-identical with cmp, and identical to the pinned dr_h6.txt. Hand-checked counts:
- Infeasible (product, save) pairs: 0+2+2+9x3+5+10 = 46, and 46 x 9 = 414 S > T cells.
- Feasible saves per product: Regulation 3; ECRS/ERS-10 12; 30-40 min products 13.
- Cloud notices: 8 saves fit within 30 s and 9 within 2 min. Both throttle latencies (5 s brake, 40 s OOB) are within T for 10 of 13 products.
- Prices: lossless (0.1+0.5)/4 = 0.15 and (0.1+0.7)/4 = 0.2; lossy (0.1+0.125)/4 = 0.05625, 0.15 and 0.525.
- Cheaper-lossy cells: 24 (30 min save, 8 products x 3 restarts, I = 15 min) + 18 (42 min save, 3 products x 3 restarts x 2 intervals) = 42.
- G-ZERO: 42 x 41 = 1722 event counts. Stake - R equals S at every job; it is nonzero in 39 of 42 jobs.
- Quotes and parses match the dossiers; the PJM columns are Notification/Deploy/Release, giving a 30 min lead. D = 1100, H = 4, R = 0.1 and K = 41 match EPS2 T1's pinned output.

**Summary:**

Not refuted. The RESULT line reproduces exactly, the arithmetic and sourced numbers check out, and the ASSUMED inputs match EPS2 T1 and sit inside the sourced ranges (R = 6 min lies in Kokolis' 5-20 min u0). Q's 'holds' follows from the model's definitions (S <= T feasibility; lost = I/2 > 0), which the script admits. The verdict-deciding choices are all printed: G-ZERO read as stake beyond R + S, not the declaration's 'beyond R' (the literal reading fails in 39 of 42 jobs), and an instantaneous stop on the lossy route. The Q-cell reading has a latent flaw: with a sourced stop latency (5 s brake), no route would meet FFR, RRS-FFR or Regulation, and the verdict word would flip to 'fails' although Q's statement would still be true. The feasible product set also depends on some generous readings: 'hosts stay powered' saves counted as power down, FFR's 10-minute XML mode dropped on a reason from outside the declaration, and Regulation's cadence read as a response time. No fabricated source and no unprinted choice that decides the verdict.

---

## H7

**Final status:** survived (1 of 3 round-1 skeptics refuted, severity major; 2 of 3 did not refute). **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H7: Q holds; G-ZERO holds (max |ETM stake - R| = 0.000000 over 328 event counts, x* == R/H at 6888 of 6888 offer states); G-NEG holds (no events: ETM ahead of WALL by > 1 % on 0 of 288 outcome comparisons)

### H7, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Unlabelled GPU-to-fleet transfer (the most consequential issue; it can change the verdict but is not a code bug). The SRC curve point (t_M, p_M) = (0.936330, 0.808052) is printed as SOURCED for the 100 MW fleet's power. McDonald et al. measure GPU energy: the paper speaks of 'reducing GPU energy consumption', and the F4 dossier's own reading says 'A cap limits the GPU's maximum draw, not the facility's'. Applying that GPU ratio to all of the fleet's MW is an assumption, but it is printed neither as CHOICE nor as ASSUMED. Suppose only a share g of fleet power follows the GPU curve and the rest is constant. Q2(a) p/t < 1 then needs g > 0.33 at x_M, g > 0.45 at x = 0.10, g > 0.71 at x = 0.25 and g > 0.88 at x = 0.50. My exact recomputation at g = 0.6 gives p/t = 0.945, 0.962, 1.051 and 1.318. At a plausible facility GPU share, Q2(a) and therefore Q would fail at the 0.25 and 0.50 tiers. The FLOOR sensitivity (p(0) = 0.3) covers this only in part, because it keeps the GPU point as the fleet point.
2. The scored lower end (0,0) is the most Q-favourable choice possible. It makes the energy per step exactly p_M/t_M = 0.863 at every depth below t_M. It is printed as ASSUMED and flagged ('depths 0.10, 0.25, 0.50 rest on it'), and it is consistent with the pause drawing 0 power. However, two sourced qualitative statements point the other way: PERSEUS-LOW says very low frequencies raise energy, and Colangelo says degradation grows below TDP. By my calculation the x = 0.5 verdict flips once p(0) exceeds about 0.147. The RESULT line says 'Q holds' without carrying the qualifier that the verdict at 3 of 4 depths rests on an ASSUMED point. Only x_M is read at the sourced point, and there Q holds under every curve except LIN.
3. Q1 is definitional. THR-own has an own-step deadline (g = n*o = 0) and an own-clock charge (n*o = 0), so its stake is 0 by construction under every curve (Sensitivity 1 shows 0 everywhere). The clause cannot fail and is rung R0 in substance. Reading 'on the own clock' as THR-own (the ETM analogue) rather than the industry cap THR-wall is a disclosed CHOICE (C3). It matters: under THR-wall, Q1 would have a nonzero stake in 1 of 32 pairs (D 1100, H 6, x 0.5, where nmax 33 < K 41).
4. Q3 is near-vacuous. It holds iff both wall delays are > 0, which is always true here. The direction is computed (throttle ahead 32/32) but is not scored. This is a defensible reading of 'is compared' (the declaration names no direction), but it adds nothing to the verdict.
5. Q2(b) is driven largely by the pause's R overhead rather than by throttle efficiency: under LIN (energy per step 1) Q2(b) still holds 32/32.
6. Minor code points. Sensitivity 2's x* check does not require closed/attained, unlike the scored Q1 check. The early-exit branch prints 'G-ZERO FAILS (not run ...)', a failure word for a gate that did not run. The 100 MW fleet is ASSUMED and the energy accounting is at fleet level with no PUE or cooling term (unstated).
7. What checks out. G-POS is correctly left to H1, as the declaration requires ('in at least one cell of H1'). G-ZERO and G-NEG are implemented as in H2. The forecast word is computed. There are no git revisions of dr_h7.py since its first commit, so no scored curve was swapped after a run is visible in the history.

**Recomputed:**

I ran the script twice. Both runs are byte-identical (cmp) and identical to the pinned dr_h7.txt. I recomputed with exact fractions independently of the script. SRC: p/t = 0.863 at x in {17/267, 0.10, 0.25, 0.50}, and (1-p)/x = 3.014706, 2.233, 1.411, 1.137. The throttle/ETM ratio of curtailed MWh per hour of delay runs from 1.15595 to 3.31618, matching the pinned 1.1560–3.3162. ETM's H/(H+R) = 0.9091, 0.9677, 0.9756, 0.9836. Sensitivity 2: x* = 89/24600000 at H 4, x_M, confirmed. FLOOR at x = 0.5: p/t = 1.1426, confirmed. The break-even floor for x = 0.5 is p(0) ≈ 0.147. With a fleet whose GPU-following share is g = 0.6, p/t = 0.945, 0.962, 1.051 and 1.318 at the four depths, so Q2(a) fails at 0.25 and 0.50.

**Summary:**

The code does what DECLARATION.md's row H7 declares, as the author's C1–C8 choices read it. The verdict words are computed from the numbers, the run is deterministic and reproduces the pinned output, and I found no arithmetic bug; I could not refute the result. The 'Q holds' verdict is fragile, though. It rests on (i) an ASSUMED, maximally favourable (0,0) lower end of the curve at 3 of 4 depths, and (ii) an unlabelled transfer of McDonald's GPU-only energy ratio to the whole 100 MW fleet, which is printed as SOURCED. The dossier itself warns that a GPU cap is not a facility cap. Under a plausible facility share of GPU power (g ≈ 0.6), Q2(a) fails at the 0.25 and 0.50 tiers. Q1 holds by construction, and Q3 holds whenever both delays are nonzero, which is always here. These are labelling and interpretation weaknesses to report, not a code bug or a wrong verdict word, so severity is minor and refuted is false.

### H7, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Q1 is true by construction. THR-own has zero own overhead (a CHOICE) and an own-step deadline that a throttle never uses (g = n*o = 0, so nmax is 'none'), so its stake is identically 0. The check cannot fail. There is another reading of 'a throttle ... on the own clock': own-clock valuation with the industry wall deadline (THR-wall). Under that reading the stake is nonzero in 1 of 32 pairs (D 1100, H 6, x 0.5; nmax 33 < K 41; p_all 36.646145, which I recomputed independently as 36.64614), and Q1 would fail. The script declares its reading as CHOICE C3 and prints THR-wall as context, so this is not an undeclared deviation. But it is the reading that decides the Q1 verdict.
2. Q3 'holds iff computable everywhere' is an empty clause: both delays are positive by construction, so Q3 cannot fail. This follows from the declaration, which names no direction for the comparison. The direction is printed (throttle ahead at 32 of 32) but not scored.
3. The scored verdict at depths 0.10, 0.25 and 0.50 rests on the ASSUMED (0,0) lower end of SRC, which makes energy per step exactly 0.863 at every depth below t_M. The only sensitivity curve with a powered floor (FLOOR, itself ASSUMED) turns Q to fail: Q2(a) 24/32, (b) 26/32, and the pause is ahead in 8 cells at x 0.5. The sourced PERSEUS-LOW quote points the same way as FLOOR. The script labels all of this. Against that, the McDonald PDF text (inference paragraph, not used by the script) gives 100W as '114% increase' in time and '11.0% less energy', which is energy per step of about 0.89 at a throughput of about 0.47. That datum supports p/t < 1 near x = 0.5, so the assumption is not contradicted there.
4. Q2(b) adds little beyond (a). It holds 32/32 even under LIN, where the throttle saves no energy, because the pause pays R at full power and the throttle has zero overhead. So (b) is driven by R. Also, the Q2(a) count of 32/32 repeats 4 distinct depth values across 8 cells; they are not 32 independent pairs.
5. Transcription slip in the author's key_numbers: the season energy per step for THR-own is given as '0.9687-0.9972'. The pinned output gives 0.968444 at the low end (D 1100/1500, H 6, x_M), which rounds to 0.9684, and my recomputation gives 0.9684. The pinned .txt is correct; only the summary is off (R1 hygiene for any later write-up). No verdict is affected.
6. p_M = E/T divides McDonald's average energy change by his average time change across configurations (a ratio of averages, not an average of ratios). It is printed as a CHOICE, and it only matters at the x_M point and for the slope of SRC.
7. The MCD-100 quote is verbatim in the dossier but not in the fetched PDF text, where a line-break hyphen splits it ('av- erage'). The number is printed only and not used, so this has no effect.

**Recomputed:**

I wrote independent exact-rational and float code in /tmp/claude-0/dr1_skeptic/recompute_h7.py, built from the quotes rather than from drlib.

- McDonald point: t_M = 250/267 = 0.936330, p_M = 863/1068 = 0.808052, x_M = 17/267.
- SRC curve at H 4: p = 0.808052, 0.776700, 0.647250, 0.431500; p/t = 0.863 at every depth; (1-p)/x = 3.014706, 2.233, 1.411, 1.137.
- Net job energy per event at P = 100 MW: -51.311, -49.320, -41.100, -27.400 MWh.
- ETM: H/(H+R) = 0.90909, 0.96774, 0.97561, 0.98361; season energy per step 1.0041.
- Throttle/ETM ratio range 1.1560 to 3.3162; SRC gives Q2(a) 32/32, Q2(b) 32/32, throttle ahead 32/32.
- THR-own season energy per step 0.9684 to 0.9972. The author's summary says 0.9687 at the low end; the pinned .txt says 0.968444, which is correct.
- FLOOR: Q2(a) 24/32, (b) 26/32, pause ahead in 8. LIN: Q2(a) 0/32, (b) 32/32.
- Sensitivity 3: throttle ahead 16/16 at every overhead (R 0.1 h, 5, 20, 10 and 25 min).
- My own backward induction: THR-wall p_all at D 1100, H 6, x 0.5 = 36.64614 (the script prints 36.646145); WALL p_all at D 1100, H 4 = 15.730882 and OWN 14.730882, both matching EPS2; ETM x* at H 4 = 0.025 = R/H.
- Counts: 328 = 8 x 41 event counts, 6888 = 8 x 861 offer states, 1312 = 32 x 41, 27552 = 32 x 861.
- The script, run twice, gives byte-identical output (cmp), identical to the pinned dr_h7.txt.

Every recomputed number matches the pinned output apart from the 0.9687 summary slip.

**Summary:**

I could not refute H7's result. The script follows the declaration's H7 row. Its verdict words are computed from the numbers. Every sourced quote is in its dossier, and I confirmed the MCD-150 and MCD-BERT quotes in the fetched McDonald PDF text. Every number I recomputed independently matches the pinned output, apart from one slip in the author's summary (0.9687 where the pinned output has 0.968444). The run reproduces byte-identically. The weaknesses are minor and the script discloses them itself:
- Q1 is true by construction under the declared own-step-deadline reading (CHOICE C3). Under the industry wall-deadline reading, THR-wall has a nonzero stake in 1 of 32 pairs.
- Q3 is an empty 'is computable' clause, because the declaration names no direction.
- Q2 at depths 0.10 to 0.50 rests on the ASSUMED (0,0) end of the curve, and the ASSUMED FLOOR curve reverses it. A related McDonald inference datum, which the script does not use, suggests energy per step stays below 1 near x = 0.5.
- Q2(b) is driven by the pause's R overhead: it passes even under LIN, where the throttle saves no energy.
None of these is a bug, an undeclared deviation that changes the verdict, a wrong verdict word or a fabricated source.

### H7, skeptic 3

- **Lens:** not recorded. **Refuted:** true. **Severity:** major.

**Issues:**

1. MAJOR (hidden, verdict-deciding scope choice; sourced label used past its source): the scored curve's one sourced point p_M = E/T = 863/1068 = 0.808 is a GPU-only average-power fraction. McDonald et al. measured GPU energy with nvidia-smi on V100s, and the cap limits GPU draw. The script uses p_M as the power fraction of the whole 100 MW fleet: depth MW = P x (1 - p), net MWh, MWh per hour of delay, and p(t)/t in Q2(a). It labels the point SOURCED and never says GPU. The F4 dossier's own reading of this source warns: 'A cap limits the GPU's maximum draw, not the facility's ... It cannot be read as "a 40 % cut in power ..."'. Neither dr_h7.py nor dr_h7.txt mentions GPU vs facility scope. A reasonable alternative within the declaration reads the fleet's power as facility/IT power, with a GPU share g and the non-GPU power not throttled. Keep the script's own ASSUMED (0,0) GPU lower end. Fleet energy per step is then (g p + 1 - g)/t, and Q2(a) fails at x = 0.5 for any g < 0.8796 (e.g. g = 0.7 gives 1.2041). It also fails at x = 0.25 for g < 0.709 (g = 0.6 gives 1.0511). The scored 'Q holds' therefore rests on an unprinted assumption that 100 % of fleet power is throttled GPU power. The x_M point survives for g > 0.33.
2. minor (printed, verdict-deciding): at the FLEX depths 0.10/0.25/0.50 the scored Q2 rests entirely on the ASSUMED (0,0) lower end. With a straight line through the origin, p/t = 0.863 at every depth by construction. Any powered-on floor p0 > about 0.147 flips Q2(a) at x = 0.5 (p(0.5) = p0 + (p_M - p0)(0.5/t_M) < 0.5 needs p0 < 0.147). The script shows this through FLOOR (p0 = 0.3, Q fails 24/32 and 26/32). The (0,0) end also sits against the sourced qualitative statements in F4: Zeus, 'none of them are entirely power proportional', and Perseus, 'very low frequencies incur more latency increase than power reduction, resulting in higher energy consumption'. The throttle's energy per step should not stay constant down to 50 % throughput.
3. minor: the BERT and POLCA 'Q holds' sensitivities share the same ASSUMED (0,0) lower end, so they are not independent robustness for the deep depths. POLCA also reads peak power as average (labelled ASSUMED).
4. minor (printed choice C3): Q1 is true by construction. THR-own has own overhead 0 and an own-step deadline, so drlib's charge and deadline use are both 0 and the stake is identically 0. The industry cap THR-wall has a nonzero stake in 1 of 32 (cell, depth) pairs, and under that reading Q1 would fail. It is printed as context.
5. minor (printed choice C5): Q3 holds iff both delays are > 0, which is automatic here, so Q3 cannot fail. The direction (throttle ahead in 32/32) is printed but not scored.
6. minor (printed choice C4): Q2(a) compares the throttle with full-power energy per step (1). Under LIN it fails 0/32. Q2(b) holds under LIN only because ETM carries R at full power.
7. minor: FLOOR gives the powered-on floor to the throttle only, while the pause's power stays 0 (ASSUMED idle 0). A floor applied consistently would also raise ETM's season energy per step, so Q2(b) under FLOOR is asymmetric.
8. minor: Sensitivity 2 checks x* only in the D = 1100 cells and does not check closed/attained as the scored Q1 does.
9. checked, no issue: every quote is found verbatim; the parsed numbers are correct (t_M = 250/267, p_M = 863/1068, x_M = 17/267; (1-p)/x = 3.0147/2.233/1.411/1.137; ETM H/(H+R); ratio range 1.156-3.316; net -51.3 and -27.4 MWh; FLOOR p/t 1.1426 at x = 0.5); THR-wall nmax 33 < K 41 at D 1100, H 6, x 0.5; the drlib Model arithmetic for tier/pause is consistent with C1/C2/C8; G-ZERO and G-NEG as printed; the output reproduces byte-identically twice and matches the pinned dr_h7.txt (cmp).

**Recomputed:**

Reran the script twice: the outputs are byte-identical with each other and with the pinned dr_h7.txt. The arithmetic checks: t_M = 0.936330, p_M = 0.808052, and p/t = 0.863 at every SRC depth. (1-p)/x is 3.0147, 2.233, 1.411 and 1.137; ETM's H/(H+R) is 0.9091 to 0.9836. Net energy per event is -51.3 MWh (x_M) and -27.4 MWh (x = 0.5) at H 4. FLOOR gives p/t = 1.1426 at x = 0.5.

Two new calculations. Keep the SRC GPU curve and read fleet power as g x GPU + (1 - g) unthrottled. Fleet energy per step at x = 0.5 is 1.4315, 1.3178, 1.2041, 1.0904 and 0.9994 for g = 0.5, 0.6, 0.7, 0.8 and 0.88, so Q2(a) fails at x = 0.5 for g < 0.8796 and at x = 0.25 for g < 0.709. Under a FLOOR-type curve, the floor at which Q2(a) flips at x = 0.5 is p0 = 0.147.

**Summary:**

The script's arithmetic, quotes, gate and reproducibility check out. The scored 'Q holds' does not survive the assumptions lens.

1. The one sourced curve point is a GPU-only average-power fraction (McDonald, nvidia-smi on V100s). The script applies it, labelled SOURCED and without saying so, as the power fraction of the whole 100 MW fleet. The F4 dossier itself warns that the cap limits the GPU's draw, not the facility's.
2. Take the reasonable fleet/facility reading: GPU share g, the rest not throttled, the script's own (0,0) GPU lower end kept. Q2 ('its energy per step is lower') then fails at x = 0.5 for any g < 0.88 and at x = 0.25 for g < 0.71. That is a hidden choice that decides the verdict (major).
3. Separately, the verdict at the FLEX depths rests on the printed ASSUMED (0,0) lower end. It flips for any powered-on floor above 0.147, and it sits against Zeus's and Perseus's sourced statements that GPUs are not power-proportional (minor, printed).
4. Q1 is true by construction and Q3 cannot fail (minor, printed).

Relevant files: /home/user/ashes_crr/Grid_Demand_Response/checks/dr_h7.py, /home/user/ashes_crr/Grid_Demand_Response/checks/dr_h7.txt, /home/user/ashes_crr/docs/citations/dr1_f4_2026-09-29.md (McDonald reading, 'A cap limits the GPU's maximum draw, not the facility's').

---

## H8

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT H8: Q fails; G-ZERO holds (max |ETM stake - rate (R + S)| = 0.000000 over 12300 (job, event count) pairs in 3 cells; ETM x* = (R + S)/H at 258300 of 258300 offer states); G-NEG holds (no events: ETM ahead of WALL by more than 1 % in 0 of 81405 comparisons; battery H1-H8 per pinned RESULT lines: 8 of 8 hold)

### H8, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Reproducibility confirmed. Two fresh runs of Grid_Demand_Response/checks/dr_h8.py are byte-identical to each other and to the pinned dr_h8.txt (cmp).
2. The Q-fails verdict rests entirely on the literal 'only' part of Q-b (C5). Q-a and the 'while' part hold in all three scored cells. C5 was fixed after the author had seen H3's pinned output (disclosed as C8). It also depends on drlib's inherited EPS2 convention that a job may let its deadline pass. That is a disclosed, verdict-deciding reading, but it is the literal reading of 'OWN supplies it only while slack lasts', so it is not a deviation. The failure is plain arithmetic. For J001 at H=1, OWN absorbs 4 events. Accepting all 41 instead pays 41pi - 4.1 against 4pi - 0.4 + 1000, so it pays when pi >= 1003.7/37 = 27.127027, the printed value. At H=4, 1004/160 = 6.275, also the printed value. At very high pi, OWN even supplies all the flexibility (16400 MWh), so no reading of 'at every payment above R/H' makes Q-b hold.
3. G-ZERO is gated on the three scored cells only. In the sensitivity cells, ETM's stake beyond rate (R+S) is positive at 261 of 92400 pairs, because the own-step deadline cannot absorb every event. If the declaration's 'exactly 0 in every cell' is read to include the sensitivity cells, the G-ZERO word would be FAILS. The choice is disclosed in C7, printed as context, and consistent with H3 and H4, which also gate only scored cells. It does not touch Q. Minor.
4. G-POS, part of 'the gate (all eight)' in the declaration, is neither printed nor read from H1's pinned RESULT line. The script says only 'G-POS is H1's; not printed'. H1's line does read 'G-POS holds', so the gate is open, but H8 does not say so. Minor.
5. G-NEG with K = 0 holds trivially: with no events, ETM and WALL are identical, so max rel is 0. This is uninformative but consistent with the rest of the battery.
6. Error in the author's summary, not in the script: 'TIER curtails 410-2050 MWh (H = 1)' at the grid. The pinned H=1 grid table shows 410.0 to 2018.0 MWh. 2050 appears only on the exact curve at pi >= 2000, not at any grid pi. The H=4 range, 1220-7950 at the grid, is correct.
7. Side observation, not scored: every TIER arm curtails at pi = 0.01, below R/H, because the throttle has zero overhead and an own-clock valuation (ASSUMED). It is printed, but the author's summary does not flag it.

**Recomputed:**

Reran dr_h8.py twice. Both outputs are byte-identical to the pinned dr_h8.txt. Hand-checked the abandonment thresholds: H=1 J001, 1003.7/37 = 27.127027; H=4 J001, 1004/160 = 6.275 = (0.1 + 1000/40)/4. Hand-checked the slack-limited shares: 3931/4100 = 0.9588, 10761/12300 = 0.8749, 13660/16400 = 0.8329. H0 enrolment at H=4: 67 jobs, since slack >= 41 x 4.1 = 168.1 h means i >= 34. The sensitivity pair count is 92400 = 924 offers x 100 jobs. Checked the grid rows: OWN at H=4 supplies 15376 MWh with 87 met at pi=10, and 16132 MWh with 77 met at pi=20.

**Summary:**

The H8 result stands: no major issue found. The code implements the declared arms (WALL, OWN, ETM, TIER, H0), the declared Q, and G-ZERO and G-NEG, and every verdict word is computed from numbers. Two fresh runs are byte-identical to the pinned output. 'Q fails' comes from Q-b's 'only' part: at high payments, tight-slack OWN jobs give up their deadline and supply beyond their slack. The first such payment per cell is 27.127, 8.367 and 6.275, each confirmed by hand from the break-even arithmetic. That is the literal reading of the declared 'OWN supplies it only while slack lasts', and the choice is disclosed (C5, C8). Minor issues: G-ZERO is gated on the scored cells only, while the sensitivity cells show a positive stake at 261 of 92400 pairs, so a reading that includes them would print FAILS. G-POS is not printed or read from H1. G-NEG at K = 0 is trivially satisfied. The author's summary quotes a TIER range of 410-2050 MWh at H=1 where the grid shows 410-2018.

### H8, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. G-ZERO is scored on the three scored cells only (C7, the same convention as H3). The declaration's gate says 'exactly 0 in every cell'. Counting the sensitivity cells too, G-ZERO would read FAILS: I independently get 261 of 92400 positive pairs (3 in spacing 12 h, 12 in spread 1i, 243 in spread 0.05i, 3 in Kokolis). These are exactly the (cell, job) pairs where ETM's own-step deadline (W + n(R+S) <= D) cannot absorb K events. The output prints this as context, so it is disclosed, and it does not touch Q's verdict. Still, the gate word 'holds' depends on reading 'every cell' as 'every scored cell'.
2. The verdict depends partly on reading, but it is robust. Under C5's literal reading ('only' = no acceptance once slack is spent), Q-b fails even on the grid alone (H = 3 and 4 at pi = 10 and 20). Under a softer 'shortfall' reading (OWN supplies less than all the flexibility), Q-b holds on the grid but fails on the continuum above R/H. The first payments where OWN supplies the full flexibility are 1000.1 (H = 1), 333.37 (H = 3) and 250.025 (H = 4). The declared 'at every payment above R/H' means the continuum, so 'Q fails' stands under both readings. C8 discloses that H3's output was seen first; the literal reading goes against the forecast, not toward it.
3. The 'only' failure is structural, not an empirical surprise. In this model a deadline has a finite value (W = 1000), so any job with fewer than K slack-limited events gives up its deadline at pi >= (1000/(K - m) + R)/H. The declared Q-b could hold only if every job had slack for all K events. That is a weakness of the declared prediction, not a bug in the check.
4. The author's key_numbers say 'TIER curtails 410-2050 MWh (H = 1)'. At the price grid the pinned output shows 410-2018 MWh at H = 1. The value 2050 appears only on the exact curve at pi >= 2000, while the H = 4 range (1220-7950) is quoted at the grid. The summary is inconsistent; nothing is scored on it.
5. The lambda_DFS sensitivity uses a 121-day window (1 Dec 2024 to 1 Apr 2025, labelled CHOICE). The same NESO report elsewhere gives the period as '27 November 2024 – 28 March 2025'. This is sensitivity only and does not affect the verdict.
6. The docstring says 'Runtime several minutes'. My rerun took 24 min 25 s.

**Recomputed:**

I wrote an independent closed-form maximiser at /tmp/claude-0/dr1_skeptic/h8_recompute.py. It uses identical deterministic offers, maximises over n in 0..K the terminal valuation plus payments, and breaks ties toward accepting. It does not use drlib. It reproduces the following:
- **Slack-limited OWN supply** (sum of min(41, floor(5i/(H+0.1))) x H): 3931, 10761 and 13660 MWh, shares 0.9588, 0.8749 and 0.8329.
- **Jobs that can abandon their deadline:** 9, 25 and 33.
- **Lowest abandonment payments** ((1000/(K-m) + 0.1)/H): 27.127027 (= 10037/370), 8.366667 (= 251/30) and 6.275 (= 251/40). At 6.275 this is an exact tie (1025 = 1025), so 'inclusive' is correct under ties-accept.
- **OWN at H = 4:** 15376 MWh with 87 jobs meeting their deadline at pi = 10; 16132 MWh with 77 at pi = 20.
- **WALL at H = 4:** 15164/89 and 16080/78.
- **ETM:** 4100, 12300 and 16400 MWh at every pi >= R/H. Q-a holds because 41 x 0.1 <= 5.
- **H0:** 91, 75 and 67 jobs at R/H; all 100 at 24.4902, 8.1634 and 6.1226.
- **TIER grid values** match to rounding.
- **Sensitivity count:** 261 of 92400 pairs, and ETM 8267 MWh at spacing 12 h, H = 1.
- **Gate:** the 12300 pairs, 258300 states and 81405 comparisons follow from counting, and G-NEG at K = 0 is trivially 0. H1-H7 RESULT lines all read 'G-NEG holds'.
- **Sources:** the four quotes are in the dossiers, and the DFS table is in the raw NESO text (whitespace-normalised).
- **Rerun:** a full rerun of dr_h8.py is byte-identical to the pinned dr_h8.txt (cmp IDENTICAL).

**Summary:**

I could not refute H8. Recomputed from first principles, 'Q fails' is correct. Q-a holds (ETM supplies all of 4100, 12300 and 16400 MWh above R/H). Q-b's 'while' part holds. Q-b's 'only' part fails in every cell: 9, 25 and 33 tight-slack jobs give up their deadline from 27.127027, 8.366667 and 6.275 onward. Every key number matches, and the pinned output reruns byte-identically.

The minor issues:
- G-ZERO is restricted to the scored cells, although the declaration says 'every cell'. It is disclosed, and including the sensitivity cells would turn it to FAILS (261 of 92400 pairs).
- C5's literal reading is disclosed, and the verdict is robust to the alternative reading on the declared continuum.
- The author's summary TIER range for H = 1 is inconsistent with the grid.
- The docstring's runtime is understated.

### H8, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Verdict-deciding reading (printed, C5 plus the continuum scoring of C2): Q fails only through Q-b's 'only' part, meaning OWN gives up its deadline at high payments. Restricting the score to the declared price grid (H8 says 'at a price grid') does not flip Q under C5: H = 3 and H = 4 still fail at pi = 10 and 20, and only H = 1 (first abandonment 27.127 > 20) would hold. A weaker reading, 'OWN does not supply all the flexibility', would hold on the grid (OWN at most 16132 of 16400 MWh). It still fails on the continuum, where OWN supplies all the flexibility from pi = 1000.1, 333.367 and 250.025 (H = 1, 3, 4). So Q flips only with both the weaker reading and grid-only scoring. The weaker reading is less literal than C5, and C5 is printed. Minor.
2. C1 (printed): OWN may let its deadline pass. With a hard deadline, Q-b 'only' holds trivially and so would Q. This matches EPS2 T1's own model ('a fleet may let the deadline pass if payments outweigh the job'; eps2_01.py line 247) and drlib's header. It is printed, not hidden. Minor.
3. C8 (disclosed): the author saw H3's pinned output, which shows OWN's grid supply above the slack-limited level at pi = 10 and 20, before fixing C5. So the verdict-deciding reading was fixed knowing its outcome. It is disclosed and it is the literal reading. Minor.
4. G-ZERO covers only the scored cells (C7, printed). In the sensitivity cells ETM's stake beyond R is positive at 261 of 92400 pairs, where ETM's own-step deadline (nmax = 50i events) cannot absorb K = 83 offers at 12 h spacing. If the declaration's 'exactly 0 in every cell' includes sensitivity cells, G-ZERO fails and the gate reading changes. The restriction matches H3's practice and the count is printed as context, but the RESULT line says only 'G-ZERO holds'. Minor.
5. Q-a's pass depends on the CHOICE of 24 h spacing (K = 41 <= ETM's nmax = 50i for every job). At 12 h spacing Q-a fails (99 of 100 jobs). This is printed as a sensitivity and does not flip Q, which fails anyway.
6. G-NEG at K = 0 is trivially satisfied (max rel exactly 0 over 81405 comparisons). This is as declared, but the gate is uninformative.
7. lambda_DFS = 44/(121 x 24) uses a 121-day denominator, 1 Dec 2024 to 31 Mar 2025, marked CHOICE. The f2 dossier notes DFS became year-round on 27 Nov 2024, so the denominator is a judgement. Sensitivity only; it does not affect Q.
8. H = 3 h is SOURCED from the Phoenix trial's event length ('sustain the reduction for 3 hours'). That event was a 25 % power reduction, not a full pause. The label is accurate for the length only. All four quoted sources (Colangelo arXiv:2507.00909 v1 x2, NESO DFS 2024/25 table, Kokolis arXiv:2410.21680v2) were found verbatim in dr1_f1, dr1_f2 and dr1_f4. No sourced-looking number was found unsourced. R = 0.1 h (ASSUMED) is consistent with Kokolis's 5 min restart (0.083 h).

**Recomputed:**

Independent closed form, exact Fractions, separate from drlib. OWN job i has slack 5i h, uses H + R wall hours per event and gives up its deadline iff (K - nmax_i)(pi H - R) >= W, i.e. pi >= (R + W/(K - nmax_i))/H, with ties accepting. Results: tight jobs 9/25/33 (H = 1/3/4); slack-limited MWh 3931/10761/13660 against flexibility 4100/12300/16400; lowest abandonment 27.127027/8.366667/6.275 (= (0.1 + 1000/40)/4); OWN supplies all the flexibility from 1000.1/333.367/250.025. All match the pinned output. ETM nmax = 50i >= 50 > 41, so ETM accepts every offer at pi >= R/H (Q-a holds). A rerun of dr_h8.py stopped at my 600 s limit after 505 lines. Those 505 lines (through the SCORED Q PER CELL section, up to the sensitivities) are byte-identical to the pinned dr_h8.txt (cmp: EOF on the partial file only). Sensitivities and gate were not re-run to completion.

**Summary:**

Not refuted. 'Q fails' comes from the literal reading (C5) of 'OWN supplies it only while slack lasts': at payments of 6.275 or more (H = 4), 8.367 (H = 3) and 27.127 (H = 1), tight-slack OWN jobs give up their wall-clock deadline and supply beyond their slack. I reproduced these thresholds and counts independently with a closed form, and the scored part of a partial rerun matches the pinned output byte for byte. Grid-only scoring does not flip the verdict (H = 3 and 4 still fail at pi = 10 and 20). Only a weaker, less literal reading ('OWN never supplies all the flexibility') combined with grid-only scoring would give 'Q holds'. The deciding choices (C5, C1's soft deadline taken from EPS2 T1, and continuum scoring) are printed, and C8 discloses that H3's output was seen first. G-ZERO being limited to the scored cells (261 positive stakes in the sensitivity cells) is printed but absent from the RESULT line. All sourced quotes are verbatim in the dossiers, and ASSUMED inputs are consistent with them. Every issue is minor.

---

## DATA

**Final status:** survived. **Fix:** none. **Round 2:** none.

**Final result:**

> RESULT DATA: Q fails; G-ZERO holds (max |ETM stake - R| = 0.000000 over 29800 (job, event) states); G-NEG holds (no events: ETM ahead of WALL by > 1 % on 0 of 1224 outcome comparisons)

### DATA, skeptic 1

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. C5 (scarcity season) does not match the dossier. The DFS-2223 quote only states an average live price (GBP 4,559/MWh) and never says 'scarcity'. The F2 dossier's tightened reading (dr1_f2 lines 338-342, 961-962) says only the W2022/23 LIVE events are the scarcity exception, and its GBP 3,000/MWh GAP test events are not. Yet the code drops the whole season from part (b), while W2023/24's test events at similar prices are scored as ordinary. W2022/23's 19 test events alone come to about 20 h x ~3000 x 100 MW = about GBP 6.0M against a compute cost of GBP 467.1M, about 1.28 %, so under the dossier's reading part (b) would FAIL. The Q word does not change (Q already fails on part a), but 'part (b) holds in 5 of 5' depends on this choice.
2. The Q verdict turns on the ASSUMED R = 0.1 h and the ASSUMED value unit (1 value unit = the compute cost of one MWh). Sensitivity 3 with the sourced R = 5 s (MegaScale) has ETM join every event in all 6 seasons, with ordinary-season shares 0.9884 / 0.5239 / 0.3171 / 0.2105 / 0.9693 %, all below 1 %. So Q would HOLD at the sourced R = 5 s. The author's summary reports the join counts but not that the Q word flips. This is disclosed as sensitivity, not a code deviation.
3. Undeclared modelling choice that understates ETM's participation. Each event costs its own restart even when two events are separated by a short unpaid gap. On ETM's own-clock valuation, staying paused through the gap costs nothing, so the two events could be bridged with a single R. Of the price-declined events, 4 of 6 in W2024/25, 12 of 26 in S2025, 3 of 8 in W2025/26 and 4 of 7 in S2026 lie within 1 h of a neighbouring event. Enough standalone declines remain in all four seasons (for example W2024/25 #43 and #47: 1 h at 130.11 and 129.53, whose max accepted bids of 140 are also below the 145.24 entry), so part (a) still fails. C3/C7 do not print this as a CHOICE.
4. Internal inconsistency inherited from the declared ETM valuation. C4 charges rented compute while paused, yet ETM's charge c = R ignores the H idle rental hours that the stop-the-clock extension adds. On the fleet's own cost accounting a pause costs (H+R)*C, which is WALL's entry price. ETM's revenue is therefore gross, not net. Correcting this would only strengthen 'Q fails'.
5. The price-taker ASSUMPTION matters most in exactly the seasons that pass. In 39 of 45 SPs (W2022/23) and 26 of 32 SPs (W2023/24), NESO's procured volume plus 100 MW exceeds NESO's requirement. So W2023/24's 0.98842 % share (the tightest part-(b) pass) is overstated. Disclosed.
6. Several quotes that dr_data.py relies on are not in claims.py, so verify.py's verbatim check against the raw fetched text does not cover them: DFS-K, DFS-RV, DFS-MAX, DFS-BIDIR (which drives C2), CW, LAMBDA-OD, LAMBDA-RES, RUNPOD and KOK-U0. dr_data.py checks them only against the dossier text. I found each one in the fetched raw texts or verify_log under /tmp/claude-0/dr1_src, so none is fabricated. The scored inputs (IDX-NEO, DGX) are covered by verify.py.
7. OWN is given a price condition (c = R) on top of the declaration's wording 'while slack lasts'. This is consistent with the declared own-clock valuation and does not enter Q.
8. Both gates hold by construction on this data. G-NEG compares ETM and WALL with zero events, so all 1224 comparisons are identical. G-ZERO holds because ETM's own-step deadline never binds (0 deadline declines). They are correctly computed but carry no information here.
9. Cosmetic: the 'mean' SP price (summary cost / procured MW) can fall slightly outside the accepted-bid range. For example, W2022/23 event 1 has mean 2999.96 against min = max = 3000, from a summary-vs-utilisation difference of at most 0.078 %.

**Recomputed:**

I ran `uv run python Grid_Demand_Response/checks/dr_data.py` (43 s) and its output is byte-identical to the pinned dr_data.txt (cmp). The raw files total 4,254,403 bytes and every sha256 matches the manifest.

Arithmetic checks:
- C = 2.5 x 8 / 10.2 kW / 1.35 = 1452.4328 GBP/MWh.
- ETM's entry price C*R/H is 290.49 at H = 0.5 h, 145.24 at 1 h and 72.62 at 2 h. WALL's is 1597.68 at 1 h.
- G-ZERO covers 29800 = 100 jobs x 298 events. G-NEG makes 1224 = 6 x (4 + 2 x 100) comparisons.

The code implements the declared rules:
- ETM joins iff price x H >= C x R, under an own-step deadline.
- OWN and WALL use the wall-clock deadline, with charges R and H + R.
- TIER throttles at x in {10, 25, 50} % over min(H, w), w in {3, 6} h.
- C10 makes Q the conjunction of part (a) and part (b), and every verdict word is computed.

Per-event check: ETM's declines are all on price, the same for all 100 jobs. Several declined events stand alone, for example W2024/25 #43 and #47 (1 h at about 130, below the 145.24 entry, with max accepted bids of 140). So part (a) fails under the 'mean', 'min' and 'max' price readings and even if near-adjacent events were bridged. It holds only when R falls to the sourced 5 s. At R = 5 s, the pinned sensitivity-3 shares make Q hold. With W2022/23's test events counted as ordinary, their share is about 1.28 %, so part (b) would fail.

**Summary:**

I could not refute the reported result 'RESULT DATA: Q fails; G-ZERO holds; G-NEG holds'. The script reproduces byte-identically. It implements the arms, Q, the named parameters and the gate lines that DECLARATION.md section 3 declares, and it computes its verdict words from the numbers.

Q fails on part (a): ETM declines low-priced, short DFS events from W2024/25 onwards, because the price is below C*R/H. This holds under all three SP price readings and even if near-adjacent events were bridged.

Issues:
- The verdict depends on the ASSUMED R = 0.1 h. At the sourced R = 5 s, Q would hold. The output discloses this as sensitivity, but the author's summary does not say the verdict flips.
- C5 drops the whole W2022/23 season from part (b), although the F2 dossier treats only its live events as the scarcity exception. Counting its GAP test events as ordinary would make part (b) fail (about 1.28 %). This undermines the 'part (b) 5 of 5' reading but not the Q word.
- Unpaid gaps between near-adjacent events are never bridged, which understates ETM's participation.
- ETM's own-clock charge ignores the idle rental that C4 counts, so its revenue is gross, not net.
- The price-taker assumption overstates W2023/24's 0.988 % share.
- Some quotes are checked only against the dossier text, not by verify.py, though I found each one in the fetched raw texts.
- Both gates hold by construction on this data.

### DATA, skeptic 2

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. Economic inconsistency, interpretive and not verdict-changing: C4 says rented compute is paid for while paused, but ETM's valuation charges only c = R per event. For a renter, an H-hour pause means paying H more hours of rent to finish the job, so the real cost per event is about (H+R)C, which is WALL's entry price (1597.68 GBP/MWh at 1 h). WALL joins 0 events from W2024/25 on, so in ordinary seasons every event ETM joins loses money net of rent. The reported 'revenue share' is gross revenue and should be labelled that way. This strengthens G7/G8 rather than weakening them.
2. The Q verdict depends on the ASSUMED R = 0.1 h, while the sourced F4 values fall on both sides of it. At MS-5 (R = 5 s), SENSITIVITY 3 shows ETM joining 21/21, 17/17, 48/48, 86/86, 33/33 and 93/93 events, with ordinary-season shares of 0.9884, 0.5239, 0.3171, 0.2105 and 0.9693 %, all below 1 %. Q would therefore HOLD at a sourced R. At the sourced 5 min (KOK-U0 lo) it fails. The author's summary reports that ETM joins every event at 5 s but does not say that Q flips there.
3. Part (b) sits close to its bound: W2023/24 is at 0.98842 % and S2026 at 0.95904 %. It flips at FX 1.50 or at the CoreWeave spot price (up to 1.1144 %). The author discloses this, but the phrase 'below 1 % only within about 11 %' is unclear. It means the largest sensitivity share exceeds the bound by about 11 %.
4. The 499 turn-down SPs where NESO accepted no bid are left out of the offered set (C1, counted). In a pay-as-bid auction, a fleet bidding its low entry price (as low as 36-73 GBP/MWh on long events) might have been accepted in some of them. This is a disclosed choice that affects the denominator of part (a).
5. The price-taker assumption is invalid for most SPs in the two early seasons (100 MW exceeds the requirement on 39/45 and 26/32 SPs). This is disclosed. It means the W2022/23 and W2023/24 shares are upper bounds.
6. The gates are nearly tautological. G-ZERO compares drlib.stake with R on drlib's own formula, and the ETM own-step deadline never binds because slack is at least 5 h and nR stays below 5 h per job. G-NEG compares ETM and WALL with no events, where they are identical by construction. Both are as declared.
7. The context line '3142 to 33560 GBP' mixes two NESO scenario columns: 3142 is the one-hour-per-requirement low and 33560 the every-SP breakpoint high. The like-for-like NESO figure is 21,009 (every SP, mean accepted bid), which the author also prints.

**Recomputed:**

I wrote independent code in /tmp/claude-0/dr1_skeptic/recompute.py and util.py. It reads the raw CSVs directly: turn-down only, procured and cost both > 0, SP price = cost/(procured x 0.5), best-paid SP where two share a slot, contiguous SPs merged, season by month, ETM joins iff price x H >= C x R.
- Records: 2369 rows, 308 turn-up, 499 unpriced, 1562 priced, 1560 unique SP slots (2 concurrent).
- Compute cost: C = 2.5 x 8 / 0.0102 / 1.35 = 1452.4328 GBP/MWh.
- ETM events joined with all 100 jobs, by season: 21/21, 17/17, 42/48, 60/86, 25/33, 86/93 (251/298).
- Curtailed MWh: 2250, 1600, 11100, 17850, 7150, 34150.
- Revenue per MW: 71123.29, 43757.59, 21121.41, 20864.23, 9512.02, 56497.55.
- Shares: 1.52265, 0.98842, 0.50918, 0.28638, 0.19217, 0.95904 %. Period hours: 3216, 3048, 2856, 5016, 3408, 4056.
- ETM delay (one slot, jobs back to back): mean/max 7.1/8.7, 5.5/10.8, 35.3/50.9, 38.375/55.0, 22.533/27.3, 73.667/129.1 h.
- Summary cost against the utilisation report: 1562/1562 matched, max rel diff 0.000778.
- Raw files: 19, total 4,254,403 bytes.
Every figure matches the pinned output exactly. A full rerun of dr_data.py is byte-identical to dr_data.txt (cmp). By these numbers Q fails (part (a) holds in only 2 of 6 seasons; part (b) holds in 5/5), and the verdict word is computed correctly.

**Summary:**

I could not refute the DATA check. Independent code reading the raw NESO DFS files reproduces every key number exactly: record counts, C = 1452.43 GBP/MWh, ETM events joined 251/298 (2 of 6 seasons complete), all six revenue shares, MWh, revenue per MW, ETM delays and the cost cross-check. The pinned output reruns byte-identically, and 'Q fails' follows from the numbers under the declared rule. The remaining issues are minor and interpretive:
- The revenue share is gross, while C4 charges rent during pauses. For a renter, ETM's ordinary-season events lose money.
- Q flips to 'holds' at the sourced 5 s restart time, but stays 'fails' at the sourced 5 min.
- Part (b) sits near its bound and flips at FX 1.50 or at the spot price.
- Unpriced SPs are excluded under pay-as-bid.
- The gates are near-tautological.
- One context line mixes two NESO scenario columns.

### DATA, skeptic 3

- **Lens:** not recorded. **Refuted:** false. **Severity:** minor.

**Issues:**

1. C5 (the season excluded as scarcity) conflicts with the F2 dossier it cites, and it decides part (b). The script prints W2022/23 as 'the season the F2 sources mark as the scarcity exception [DFS-2223]'. The dossier's own reading, tightened 2026-09-30 at docs/citations/dr1_f2_2026-09-29.md lines 338-342, says the opposite: 'Only the live events are "exceptions in scarcity events" ... the earlier reading counted the test GAP as a scarcity exception.' W2022/23 is 40 test SPs at the £3,000 GAP and 5 live SPs. Excluding only the two live events (revenue 100 x (3954.44 + 1.5 x 4779.48) = £1,112,366) leaves test revenue of £5,999,963 against a compute cost of £467,102,397, a share of 1.2845 %. Part (b) would then fail. The exclusion is also applied inconsistently: W2023/24 is scored as ordinary, yet its live events paid £4,439.74 and £5,012.66, above the 2022/23 live average of £4,559 that defines the exception. Q still fails through part (a), so the RESULT line stands. The reported 'Part (b) holds in 5 of 5 ordinary seasons' and any G7 reading built on it do not survive a dossier-consistent C5. The attribution to F2 is inaccurate.
2. Part (b) is far more fragile than reported. W2023/24's share is 0.98842 %, so a 1.17 % fall in C already reaches 1 %. The printed sensitivity shows it: CW-SPOT at fx 1.35 (C = 1431.4) gives 1.0030 %. The author's 'below 1 % only within about 11 %' reads as an 11 % margin, but the margin on C is about 1.2 % (W2023/24) and 4.3 % (S2026, 0.95904 %).
3. PUE = 1 (ASSUMED, printed) decides part (b) at any realistic facility overhead. With a PUE of 1.012 or more, the metered cost per MWh falls enough to take W2023/24 above 1 %, and 1.043 or more does the same for S2026. The F5 dossier asked that the PUE choice be stated. It is stated, but its verdict-deciding role is not.
4. R = 0.1 h (ASSUMED, printed; the EPS2 T1 value, inside the sourced F4 range of 5 s to 20 min) decides part (a) and therefore Q. At primary C, ETM joins every event iff R <= about 99 s. The binding event is S2025 2025-04-16 21:30, 0.5 h at £80: 80 x 0.5 / 1452.43 = 0.0275 h. With the sourced MS-5 value (5 s), ETM joins 48/48, 86/86, 33/33 and 93/93, all ordinary shares stay below 1 %, and Q HOLDS. The author reports this sensitivity, so it is minor, but the Q verdict is an R choice.
5. A modelling tension, not verdict-flipping. Under the check's own C4 ('rented compute is paid for while paused'), a pause of H hours costs a renter H + R hours of rent in money, which is WALL's charge. ETM's own-clock valuation treats the H hours as free. The F5 dossier records this qualifier (compute is 'non-storable': a capacity-bound fleet loses the curtailed GPU-hours). ETM's entry price C*R/H is therefore a lower bound on the monetary cost for a rented fleet. It is the declared arm, and it only makes part (a) fail more.
6. Price-taker assumption: the output itself shows it violated in 26 of 32 W2023/24 SPs (100 MW more than procured exceeds NESO's requirement). The near-threshold W2023/24 share assumes full acceptance at the volume-weighted mean price in a pay-as-bid market. This is printed and does not flip Q.
7. Minor: no electricity saving is credited while paused (power 0, rented-fleet reading). For an owner-operator fleet the avoided energy bill would lower the effective entry price. This is not modelled; it is outside the declared arm and printed only implicitly.

**Recomputed:**

I ran the script again and cmp shows the output byte-identical to the pinned dr_data.txt (44 s). The sourced inputs, the SP counts and the headline numbers all check out.

- Compute cost: C = 2.5 x 8 / 0.0102 / 1.35 = 1452.43 GBP/MWh. ETM's entry price is 290.49 at 0.5 h and 145.24 at 1 h.
- W2024/25 cost and share: 100 x 2856 h x 1452.43 = £414.8M, and 2,112,140.72 / 414.8M = 0.50918 %. The period of 119 days (2024-12-03 to 2025-03-31) is correct.
- SP counts: 2061 turn-down SPs - 1562 priced = 499 unpriced. There are 308 turn-up SPs, all in cur_sum.csv, dated 2026-05 or later.
- G-NEG: 1224 comparisons = 6 x (4 + 2 x 100).
- Part (a): every declined event is priced £80-160 against an entry price of £145-290, so the declines are on price.
- R threshold: part (a) holds iff R <= about 99 s.
- My own recomputations:
  - W2022/23 test-only ETM share: 5,999,963 / 467,102,397 = 1.2845 %.
  - W2023/24 break-even: C must fall by 1.17 % (or PUE >= 1.0117).
  - S2026 break-even: C must fall by 4.3 %.

**Summary:**

Q fails, as reported, and I could not refute it. Part (a) fails because real DFS prices of £80-160/MWh fall below ETM's entry price C*R/H in 4 of 6 seasons. That holds at every sourced compute price and at every sourced R except the 5 s MegaScale value. G-ZERO and G-NEG hold, the arithmetic is right, and the output is byte-identical on rerun. The weak point is the part (b)/G7 sub-result ('below 1 % in 5 of 5 ordinary seasons'). It rests on C5, which excludes the whole of W2022/23 as 'the season the F2 sources mark as the scarcity exception'. The F2 dossier's reading, tightened 2026-09-30, says only the live events are scarcity and the £3,000 test GAP is not. With only the live events excluded, W2022/23 counts as ordinary at 1.2845 % and part (b) fails. The exclusion is also inconsistent with W2023/24, which is scored as ordinary despite live events at £4,440-5,013. Part (b) is also much more fragile than the author says. W2023/24 is at 0.98842 %, so a 1.2 % fall in C or a PUE of 1.012 or more flips it. R = 0.1 h alone decides Q, since R = 5 s makes Q hold. Everything that decides the verdict is printed, and no fabricated source was found, so the issues are minor. The C5 misattribution should still be fixed or reported before G7 is quoted.
