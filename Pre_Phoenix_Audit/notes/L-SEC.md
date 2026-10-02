# L-SEC: the calibrated Laplace weight (SEC1, SCL3, SEC3, SEC4, SEC5, SEC6, SEC6R, SEC7, SPA1, P1)

Reader's notes for the Pre-Phoenix audit (`Pre_Phoenix_Audit/DECLARATION.md`; prompt-log entry 260). These are interpretive
notes, not evidence (R8). No verdict is changed. Verdicts are quoted from `ledger/LEDGER.md` by row id. Where I derive a
count myself it is marked **auditor's count (derived)** with the method; such counts must be re-printed by a pinned script
in `Pre_Phoenix_Audit/checks/` before they enter the final report (DECLARATION.md, "Status").

---

## 0. One-paragraph summary

SEC is the textbook Laplace (Bayes) weight w = 1/2 on an empirical Fisher. Each task's Fisher is rescaled once by a
per-task secant ratio. In SEC4 onwards an AR1-type stability clip is added. It is **not a CRR rule**, and the record says
so throughout:
- `reports/scl3.md:22`, `reports/sec4.md:87-88`, `prereg/scl3/PREREG.md:20`;
- P1's F11 HOLDS: "CRR-proper operations performed in SEC's code path: 0 of 7 operational clauses"
  (`SEC_Analysis/checks/a11_grade.txt:125`, `:242`).

It grew out of the H-EQ programme, as a test of the *ordinary* explanation of the Ω = 1 rule's advantage: that the rule
was beating a miscalibrated Laplace baseline (`Continuous_Learning/CONTINUOUS_LEARNING.md:354`).

The lineage holds the record's only PASS-1 (SEC4-1) and most of its held-out PASS-0 rows. Every one of those "not behind
the tuned λ" passes was later shown, or registered, to rest on a criterion that a learner frozen after task 1 also meets.
The failures (SEC3-3, SEC5-1, SEC6R-B, SEC6R-2) reach the *method* as a tuning-free replacement for a λ sweep on
class-incremental tabular streams. Nothing here reaches a CRR principle, because no CRR principle is load-bearing in SEC.

Two things survive as candidate phenomena (F), not passes:
- the secant units calibration, the one part SPA1 did not find in the literature;
- a tendency, on the few carriers where the criterion *can* discriminate, for the clipped SEC to hold.

The decisive confirmatory test, a stream and reference that a frozen learner fails, was never run. SEC7 stopped at its
development gate.

---

## 1. Trajectory (dated, cited)

| date (UTC) | event | source |
|---|---|---|
| 2026-09-22 | The H-EQ programme's required R7 Bayes arm (Laplace 1/2 on the task-size-weighted Fisher; derived in `Continuous_Learning/CONTINUOUS_LEARNING.md:148-152`). EQ3-B reads it "the tuned weight on led7 … and krkopt, and 7.6 to 12.5 points behind where the tuned λ is in the hundreds". The paper reads the rule's advantage as "an advantage over a mis-calibrated Laplace approximation with a diagonal empirical Fisher" | ledger EQ3-B; `CONTINUOUS_LEARNING.md:354` |
| 2026-09-23 07:07–15:06 | Owner scratchpad prompts on "what determines a learning unit" (entry 111). Entry 118 quotes "Bayes λ = 1 simply assumes F is already right … The new step stayed at 1.000 of the best achievable score at every hidden scale from 1/256 to 256" | PROMPT_LOG 111–119 |
| 2026-09-23 15:14:52 | Owner: "today we will run the pre registered checks on existing actual data" | PROMPT_LOG 120 |
| 2026-09-23 | SEC defined "in scratchpad work on synthetic quadratic worlds (prompt-log entries 111–118; not in the repository)". First gate CLOSED (units rows not load-bearing), redesigned before any carrier (POS/INV/SHAPE), OPEN. One-factor arm added as the R7 alternative | `prereg/sec1/PREREG.md:52-56, 131-151`; AGENT_LOG 96 |
| 2026-09-23 15:18:10 / 15:18:27 | SEC1 prereg pushed; data step 17 s later, on the twelve SEEN EQ3+EQ4 carriers (rung R5, push-timestamp anchor only) | ledger SEC1-1 col. 2 |
| 2026-09-24 → 25 | SCL3 hashed 2026-09-24 (OpenTimestamps complete). Data step 2026-09-25T00:07:06Z on ten unseen OpenML-CC18 carriers ("SEC2" inside the operator harness) | ledger SCL3-3; `reports/scl3.md:3-13, 32`; AGENT_LOG 128 |
| 2026-09-25 | **The criterion weakness is first flagged.** Every pass is "inside the regularisation family". 13 of 37 carrier-scorings are INERT (three of SCL3-3's nine). Proposed: "a pre-registered load-bearing criterion for every 'not behind' row", plus fine-tune/offline/replay reference arms (owner decides). No row edited | AGENT_LOG 131; `docs/notes/2026-09-25_results_vs_published.md:76-100`; `Continuous_Learning/checks/results_vs_literature.txt:95`; `docs/citations/classil_benchmarks_2026-09-25.md` |
| 2026-09-25 | Compute_Savings: "SEC is a product of this repository's CRR programme … CRR's role was the path to it, not its equations" | `Compute_Savings/COMPUTE_SAVINGS.md:8-17`; AGENT_LOG 143 |
| 2026-09-25 | Cramér–Rao reading: "SEC is a repair of the Cramér–Rao unit … Stated in advance, it might have pointed at unit calibration sooner. That is hindsight, and it is not counted as a prediction". Rung R0–R2 | `docs/notes/2026-09-25_cramer_rao_reading.md:90-135` |
| 2026-09-27 → 28 | SEC3 (plan CL-1). The guard (fall back to raw Laplace at the stability edge) gate CLOSED on SEEN cnae-9 by one carrier: guarded −1.9792 against step 1.7305. The guarded arm becomes report-only. Data 2026-09-28 | `prereg/sec3/gate_SEC3.txt:11-21`; AGENT_LOG 167, 168 |
| 2026-09-28 → 29 | SEC4. Guard chosen on 16 SEEN carriers (D-GATE OPEN, clip chosen), "three of them where the failure was found". Hashed 2026-09-28; data 2026-09-29. **PASS-1** | ledger SEC4-D, SEC4-1; AGENT_LOG 169, 172 |
| 2026-09-29 → 30 | SEC5. Owner: "Use the CRR to fine-tune". The A6 candidates closed D-GATE-C on 22 SEEN carriers. SEC4's clipped SEC unchanged on a fourth family; data 2026-09-30. FAIL | PROMPT_LOG 238; AGENT_LOG 177, 178, 188; ledger SEC5-C-DEV, SEC5-1 |
| 2026-09-30 | SPA1 (prior art: KNOWN); COMPARISON (owner prompts 254–256) | AGENT_LOG 210, 211 |
| 2026-09-30 | Owner: "Sec4 was successful so we should run a full crr analysis on it". The agent records that analysing SEC4 alone "would select on the outcome" and declares P1 over all five families | PROMPT_LOG 257; AGENT_LOG 212 |
| 2026-09-30 | P1 mechanism checks: **FM6 FAILS**, M6 (a learner frozen after task 1) "NOT behind the tuned lambda on 24/30". Cause traced to the loader's class ranking. SEC6 Amendment 3 adds the instrument gate SEC6-G before the hash | AGENT_LOG 222, 224; `SEC_Analysis/checks/m_checks.txt:118, 186` |
| 2026-09-30 | Post hoc gate rows SCL3-3-G (OPEN), SEC3-3-G, SEC4-1-G, SEC5-1-G (CLOSED). Addenda appended to Compute_Savings, SPA1, COMPARISON | AGENT_LOG 236, 239 |
| 2026-09-30 | SEC7 (random class order, balanced accuracy) development gate CLOSED. SEC7 stops (R12) | ledger SEC7-A; AGENT_LOG 234, 235, 238 |
| 2026-10-01 | SEC6 data step: 0 of 12 carriers readable (ARFF STRING targets). NOT DECIDABLE | ledger SEC6-1; AGENT_LOG 241 |
| 2026-10-01 → 02 | SEC6R: one change (a STRING-target loader). Part A post hoc on SEC6's twelve; Part B held-out, data 2026-10-02T00:07:24Z. Gate CLOSED, passes UNINFORMATIVE | ledger SEC6R-*; AGENT_LOG 242, 243, 245 |

**Tempo.**
- **Auditor's count (derived, from the dates above):** eight SEC-family stages in ten days (2026-09-23 to 2026-10-02):
  - six hashed confirmatory studies with a data step: SEC1, SCL3, SEC3, SEC4, SEC5, SEC6R;
  - one hashed study whose data step scored no carrier: SEC6;
  - one development-only study: SEC7.
- The first held-out test came two days after SEC was first written down.

---

## 2. Operationalisations and added assumptions (Q1–Q4)

**Q1. The initial idea.** It was not a CRR idea.
- The idea was a check on an ordinary explanation of the H-EQ result: the rule's advantage over Bayes is an advantage over
  a mis-scaled Fisher (`CONTINUOUS_LEARNING.md:354`).
- SEC1's question: "With the units fixed this way, the textbook Laplace weight (w = 1/2) needs no per-dataset tuning"
  (`prereg/sec1/PREREG.md:47-48`).
- The CRR vocabulary attached to it (A1′, "the system's own resolvable step", `theory/CRR.md:55`) supplies a *name* for
  the correction: P1 graded "(e) A1' supplies a name ('units') for the correction: holds" (`a11_grade.txt:233`).
- `theory/CRR.md` contains no Laplace weight, no calibration and no clip. The only CRR learner hypothesis is H-EQ
  (`theory/CRR.md:166-191`). SEC was carried beside it as its R7 comparison (`prereg/sec1/PREREG.md:98`).

**Q2. How it was operationalised.**
- s_j = c_j / ρ_j, at the end of each task j:
  - c_j is the change of the mean clean present gradient between the task's first and last 10 % of steps, projected on
    the parameter change, divided by its squared length (a secant);
  - ρ_j is the Fisher's claimed curvature on the same path.
- The Fisher is rescaled by s_j and used at w = 1/2. The windows FS = FE = 0.1 are named estimator constants; there is a
  fallback s = 1 (`prereg/sec1/PREREG.md:38-45, 52`).
- From SEC4: a stability clip at κ = 0.5 of the explicit-Euler edge (ledger SEC4-1; SPA1: "AR1's clip … with κ = 0.5 in
  place of 1", `SEC_Prior_Art/SPA1.md:28`).
- Learner: "a numpy MLP with 256 hidden units, SGD at lr 0.05, batch 10, 3 epochs per task, class-incremental accuracy
  (%)", two classes per task (`prereg/sec1/PREREG.md:77, 84-86`).

**Q3. Assumptions added to make it testable.**

| # | added assumption | where | later fate |
|---|---|---|---|
| a1 | "Tuning-free" ≙ "not behind the in-sample-tuned EWC λ by a resolvable step" (one-sided). The tuned λ is tuned "in-sample on the scored seeds … which favours the baseline" | `prereg/sec1/PREREG.md:92, 104` | **Failed as an instrument.** M6 meets it on 24/30 held-out carriers (FM6 FAILS); SEC4-1-G, SEC6R-G, SEC6R-A-G CLOSED; SEC7-A CLOSED |
| a2 | The stream: class-incremental, consecutive label pairs, classes ranked by count, stratified test set (inherited from EQ4's class-selection rule) | `prereg/sec1/PREREG.md:76-78`; `WHY_SEC4_WORKED.md:76-79` | **The structural cause of a1's failure:** "task 1 always holds the two most frequent classes and the stratified test set rewards keeping them" (AGENT_LOG 222) |
| a3 | Resolvable step = max(1, 2 × SE over seeds of the tuned arm). Pass bar ⌈0.75 N⌉ with N ≥ 4 | `prereg/sec1/PREREG.md:102`; ledger SEC4-1 threshold | Coarse at the N reached (6, 8, 9). SEC6R-1 and SEC6R-C pass at exactly 7/9, need 7 (ledger) |
| a4 | The Fisher's error is one of scale, not shape (the R4 gate's MUST_FAIL row SHAPE) | `prereg/sec1/PREREG.md:146, 150-151` | Partly supported, post hoc and only on informative carriers (F4 HOLDS on 16 non-floor-bound; FAILS on all 42: `a4_a6.txt:100-101, 262-263`). The same output notes that a "diagonal-against-full curvature gap would also give s > 1" (`a11_grade.txt:185`) |
| a5 | No step bound is needed (SEC1/SCL3/SEC3), then a clip at κ = 0.5 (SEC4 onwards) | AGENT_LOG 96 ("SEC inherits no step bound"); ledger SEC4-1 | The no-bound assumption failed: divergence on mfeat_factors, cnae-9, dionis, fabert, anneal, cardiotocography, synthetic_control. The clip fixed those (SEC4-2 PASS-0). It fails where it "caps what the carrier needs" (SEC5-2, SEC6R-2) |
| a6 | The OpenML/ARFF loader of SCL3, frozen unchanged | ledger SEC6-1 | **Failed as an implementation** on STRING targets (SEC6: N = 0) |
| a7 | Held-out families exist in sufficient number | AGENT_LOG 169 (3), 235 | PMLB "exhausted"; study 445 "only 2 eligible"; the families were pooled |

**Q4. Which added assumption became the thing that failed.**
- Mainly a1 + a2: the criterion and the stream. These are not part of SEC, and not part of CRR.
- a5 (no step bound) failed as a method assumption and was repaired by a known device (AR1).
- a6 failed as infrastructure.
- a4 (units, not shape) is the one assumption about the method's *mechanism*. It was never tested on a criterion that can
  fail. Its post hoc support is limited to informative carriers.

---

## 3. Results (verbatim verdicts, by row id)

**SEC1** (SEEN, rung R5)
- SEC1-0 DECIDABLE.
- SEC1-1 "PASS (seen data; rung R5, not PASS-0), exactly at the threshold; fars does not close and on yeast the calibrated
  arm is worse than raw".
- SEC1-2 "PASS (seen data; rung R5, not PASS-0)".
- SEC1-3 "PASS (seen data; rung R5, not PASS-0), at the boundary and FRAGILE (SEC1-S): 9 is the threshold, and
  wine_quality_white counts as not behind by 0.029497893800771".
- SEC1-4 FAIL (calibrated span 849.00× against raw 423.00×).
- SEC1-S "FRAGILE (8 of 96 cells flip)".
- SEC1-X "holds (reproduced exactly)".

**SCL3** (held-out, OpenTimestamps complete)
- SCL3-1 "**PASS-0** (held-out; PASS-1 not reached: SCL3-S FRAGILE)" (5/6).
- SCL3-2 "**PASS-0** (held-out)" (4/4).
- SCL3-3 "**PASS-0** (held-out; PASS-1 not reached: SCL3-S FRAGILE; cnae-9 behind, its calibrated arm scoring 0.00 and
  12.50 on two seeds)" (9/10; raw Bayes 4/10, the rule Ω = 1 7/10).
- SCL3-4 "**PASS-0** (held-out; SEC1-4 had FAILED on the seen carriers)" (raw 18866.67×, calibrated 500.00×).
- SCL3-S FRAGILE (6 of 80).
- SCL3-C "holds (a check of the construction, Proposition 7 for a learner; not support for CRR)".

**SEC3** (held-out)
- SEC3-0 "M = dionis (1)"; SEC3-1 NOT DECIDABLE.
- SEC3-2 FAIL (4/5).
- SEC3-3 "FAIL (SCL3-3's PASS-0 does not replicate on the second family; beside it raw Laplace 5/6 and the rule Ω=1 5/6)"
  (4/6).
- SEC3-4 FAIL (raw 23.50x, calibrated 30.00x).
- SEC3-T FAIL (2/3).
- SEC3-P "**PASS-0** (held-out; not PASS-1: OTS confirmation pending at scoring, no sensitivity row registered for it, and
  the arm's SEC3-S is FRAGILE)" (5/6).
- SEC3-S FRAGILE.
- SEC3-GR "report (no verdict registered; post hoc, a hypothesis for a new study, not a result)" (not behind 6/6).

**SEC4** (held-out, OpenTimestamps complete)
- SEC4-D report (development on SEEN, D-GATE OPEN).
- SEC4-1 "PASS-1 (held-out, the third family; the prereg's PASS-1 conditions all hold: SEC4-S not fragile 0/18, SEC4-2 no
  divergence, OTS complete, carriers' admissibility stated; no reduction to a constant: the transferred λ is behind on 2 of
  6, below the 5 needed; limits: N = 6 after 3 exclusions, κ itself not swept (the scale and raw guards reported beside
  it), a guard chosen on SEEN carriers, not a CRR rule; not PASS-2: no earlier held-out pass of the clipped rule)" (6/6;
  unguarded SEC 3/6, raw Laplace 1/6, the rule Ω=1 5/6).
- SEC4-2 "PASS-0 (held-out; the failure the clip is for does not occur)".
- SEC4-T "NOT DECIDABLE (a reused λ would have saved the sweep on 4 of 6 without SEC; on the 2 where it fails, the clipped
  SEC is not behind)".
- SEC4-P "PASS-0 (held-out; no sensitivity row registered for it)" (6/6).
- SEC4-S "not fragile".

**SEC5** (held-out, OpenTimestamps complete)
- SEC5-C-DEV "report (development on SEEN carriers, not evidence; D-GATE-C CLOSED: D-ADDS fails; no A6 arm run on the
  unseen family, R12 …)".
- SEC5-1 "FAIL (held-out, the fourth family; not fragile: 0 of 40 sensitivity cells flip, kappa included; SEC4-1's PASS-1
  does not replicate, so no PASS-2; SEC4-1 stands as a single-family PASS-1)" (4/8; unguarded 4/8, raw Laplace 4/8,
  Ω = 1 4/8).
- SEC5-2 "FAIL (as registered: low-accuracy seeds; on pokerhand not a stability-edge crossing)".
- SEC5-T FAIL (3/7).
- SEC5-P "PASS-0 (held-out; one configuration not behind a 3-point sweep on 6 of 8)".
- SEC5-S "not fragile (the FAIL is robust to kappa and the window)".

**Post hoc gate rows** (SEC6-G's rule applied after the fact; "not a re-score")
- SCL3-3-G "gate OPEN: the criterion could fail on SCL3's carriers" (M6 7/10, need 8).
- SEC3-3-G "gate CLOSED: SEC3-3 (FAIL as scored) would be printed UNINFORMATIVE" (5/6).
- SEC4-1-G "gate CLOSED: SEC4-1 (PASS-1 as scored under its own pre-registration) would be printed UNINFORMATIVE and capped
  at PASS-0 … SEC4-1 must not be quoted as evidence that the clipped SEC is tuning-free without this row" (5/6, need 5).
- SEC5-1-G "gate CLOSED: SEC5-1 (FAIL as scored) would be printed UNINFORMATIVE" (7/8).

**SEC7**
- SEC7-A "GATE CLOSED (SEC7 stops, R12): even with a random task 1 and balanced accuracy the tuned lambda is often no better
  than a learner frozen after task 1, so 'not behind the tuned lambda' cannot fail on these class-incremental tabular
  streams; a design failure of the benchmark, not a test of SEC" (frozen learner behind on 13/30, need more than 15).

**SEC6** (held-out family, 0 scored)
- SEC6-1, SEC6-1F, SEC6-C, SEC6-B, SEC6-T: NOT DECIDABLE (N = 0).
- SEC6-G, SEC6-2, SEC6-P, SEC6-S: "report (vacuous …)". The cause: "every SEC6 carrier declares its target as an ARFF
  STRING attribute … which the frozen loader … reads as a number".

**SEC6R Part A** (SEEN, post hoc, no level)
- SEC6R-A-G gate CLOSED (edge 7/7).
- SEC6R-A-1 "PASS as printed (seen data, post hoc; no level; UNINFORMATIVE …)" (6/7).
- SEC6R-A-B "FAIL (… UNINFORMATIVE …): SI-0.1, SI-1C and raw Laplace are not behind on more carriers than the clipped
  SEC".

**SEC6R Part B** (held-out, OpenTimestamps complete)
- SEC6R-G "gate CLOSED: SEC6R-1, SEC6R-B and SEC6R-P are UNINFORMATIVE and capped at PASS-0 (as registered)" (edge 8/9).
- SEC6R-1 "PASS-0 (UNINFORMATIVE: SEC6R-G CLOSED, a learner frozen after task 1 meets the same criterion; also FRAGILE
  (SEC6R-S) and SEC6R-2 FAIL, so not PASS-1; it does not raise SEC4-1 to PASS-2)" (7/9, need 7).
- SEC6R-1F NOT DECIDABLE (N_F 1).
- SEC6R-C "PASS-0 (UNINFORMATIVE: SEC6R-GC CLOSED)".
- SEC6R-B "FAIL (UNINFORMATIVE …): AR1-B and SI-1C are each not behind on 8/9, more than the clipped SEC".
- SEC6R-T FAIL (5/7).
- SEC6R-2 FAIL (volcanoes-d1).
- SEC6R-P "PASS-0 (UNINFORMATIVE …)".
- SEC6R-S FRAGILE (2 of 45).

**Share of the record's passes (auditor's count, derived).** `Epistemic_Review/checks/ladder.txt:335` lists 15 rung-R6
held-out PASS-0 rows. Counting those with an `SCL3-` or `SEC` prefix gives 11: SCL3-1, SCL3-2, SCL3-3, SCL3-4, SEC3-P,
SEC4-2, SEC4-P, SEC5-P, SEC6R-1, SEC6R-C, SEC6R-P. The record's only R7 PASS-1 is SEC4-1. None is a CRR rule.

---

## 4. Four-layer tables for the key observations

### O1. SEC4-1 PASS-1 (6/6) and SEC4-1-G (frozen learner 5/6)

| layer | content |
|---|---|
| observed | Clipped SEC not behind the tuned λ on 6/6 unseen carriers. Margins +0.5594 to +5.5056. 0/18 sensitivity flips; no divergence (ledger SEC4-1, SEC4-2, SEC4-S; `reports/sec4.md:43-57`). P1's M6 (no Fisher, every coordinate at the cap after task 1) is not behind on 5/6 (SEC4-1-G; `gate_posthoc.txt:11-12`) |
| CRR interpretation | None is licensed. SEC is "not a CRR rule" (SEC4-1 verdict text). A posteriori, A1′ "supplies a name ('units')" (`a11_grade.txt:233`). The Cramér–Rao reading calls this hindsight (`2026-09-25_cramer_rao_reading.md:125-126`) |
| ordinary explanation | (i) An easy family: a reused λ was not behind on 4/6 against 1/8 in SEC5; SD ratio 0.3611 against 1.0348 (`WHY_SEC4_WORKED.md:43-47, 124-127`). (ii) A lenient criterion: regularisers on class-IL streams sit near the no-method lower bound ("completely failed in the Class-IL scenario", van de Ven & Tolias, quoted in `docs/citations/classil_benchmarks_2026-09-25.md`). Task 1 holds the two largest classes (AGENT_LOG 222). (iii) The clip is AR1's (SPA1) and fixed the three divergences (`reports/sec4.md:41-52`) |
| what would distinguish | The same arm on a stream and reference that M6 fails: task-incremental heads, or a reference that must beat freezing (SEC7-A verdict; AGENT_LOG 238; `WHY_SEC4_WORKED.md:271-272`). Also: the calibration's units claim tested by a criterion that does not involve "not behind" (see O5) |

### O2. SCL3-3 PASS-0 (9/10) with its post hoc gate OPEN (SCL3-3-G: 7/10, need 8)

| layer | content |
|---|---|
| observed | The only SEC "not behind" pass whose post hoc gate is OPEN, and it is open by one carrier (M6 7/10 against a need of 8, `gate_posthoc.txt:5`). FRAGILE (SCL3-S 6 of 80). Three of its nine passes are INERT (`results_vs_literature.txt:95`; `2026-09-25_results_vs_published.md:82-84`): "On the seven load-bearing carriers SEC is not behind on six (cnae-9 behind)" |
| CRR interpretation | None (`reports/scl3.md:22-23`) |
| ordinary explanation | A units correction of the empirical Fisher. SCL3's family was the one where raw Laplace was most miscalibrated: M had 6 carriers (SCL3-0), against 1 in SEC3 (SEC3-0) |
| what would distinguish | Replication on a family where M is large *and* M6 fails. Not achieved: SEC3-3 FAIL; SEC4/SEC5/SEC6R gates CLOSED |

### O3. The method-level failures: SEC3-3, SEC5-1, SEC6R-B, SEC6R-2, SEC5-2

| layer | content |
|---|---|
| observed | SEC3-3 4/6 FAIL (dionis and fabert each with one seed at 0.00). SEC5-1 4/8 FAIL, not fragile over κ and the window. SEC6R-B FAIL: AR1-B and SI-1C 8/9 against clipped SEC 7/9. SEC6R-2 and SEC5-2 FAIL (volcanoes-d1, volcanoes-d4: "the clip caps the strength the carrier needs"; pokerhand under-regularised, `reports/sec5.md:74-82`) |
| CRR interpretation | None. SEC5's one CRR-guided refinement (A6 averaging) was closed in development. "CRR's A6 reading pointed at the wrong cause" (`reports/sec5.md:92-100`) |
| ordinary explanation | The calibration lands far from the tuned λ on families with a wide optimum spread (SD ratio 1.0348 in SEC5). A fixed clip cannot supply strength above the explicit-Euler edge. Two simpler published-style rules without units calibration do as well or better (SEC6R-B) |
| what would distinguish | Nothing further needed for the *method claim* at this rung. Negative evidence on "SEC is tuning-free on these streams" is already direct. See §5 on the post hoc "UNINFORMATIVE" label attached to these FAILs |

### O4. The must-fail control meets the criterion (M6 24/30; SEC7-A 13/30 behind)

| layer | content |
|---|---|
| observed | M6 "not behind 24/30, behind 6/30" over the 30 held-out carriers (`m_checks.txt:118`; FM6 FAILS, `:186`). Under a random class order with balanced accuracy, on SEEN carriers, edge is behind on 13/30 against a need of more than 15 (SEC7-A; `prereg/sec7/dev/gate7.txt`, the D-FAIL line) |
| CRR interpretation | Not applicable |
| ordinary explanation | Class-incremental regularisation baselines fail (van de Ven & Tolias, in `docs/citations/classil_benchmarks_2026-09-25.md`), so the tuned λ is weak. Keeping task 1 is rewarded under the loader's class ranking and a stratified test set (AGENT_LOG 222). The class-order explanation's own declared test "fell just short" (F14 FAILS; Spearman 0.785 against 0.8, `WHY_SEC4_WORKED.md:85-92`) |
| what would distinguish | A benchmark redesign (task-IL heads, replay, or a reference that must beat freezing), declared from scratch (AGENT_LOG 238). Never run |

### O5. The secant units calibration as a units correction (the one part not found by SPA1)

| layer | content |
|---|---|
| observed | **Held-out, a criterion independent of "not behind":** SCL3-4 PASS-0, the tuned λ's span collapses from 18866.67× to 500.00×. **Against it:** SEC1-4 FAIL (849.00× against 423.00×); SEC3-4 FAIL (30.00x against 23.50x); F2 FAILS, the SD ratio meets the bar in 2 of 5 families (`a1_a3.txt:153-158`). **Post hoc on 16 non-floor-bound carriers:** the tuned raw λ tracks 0.5·s̄, Spearman 0.752, slope 1.224 (`a4_a6.txt:262`). On all 42 it is 0.545 and F4 FAILS (`a4_a6.txt:100-101`). Per-task factors beat one global factor: `bayes_s1` 18/42 against 29/42 (FM3; `WHY_SEC4_WORKED.md:169`). The path secant exceeds the endpoint curvature by a median factor of 5.859; endpoint calibration gives 21/30 against 26/30 (FM2) |
| CRR interpretation | A1′ "names" the unit. The Cramér–Rao note reads SEC as "a repair of the Cramér–Rao unit", rung R0–R2, hindsight (`2026-09-25_cramer_rao_reading.md:103-104, 125-135`). No CRR operation is performed (F11) |
| ordinary explanation | Numerical analysis: a Barzilai–Borwein / self-scaling secant (`WHY_SEC4_WORKED.md:68-69`). The empirical-Fisher scale error is known (SPA1 S1 MIXED: Ritter, van de Ven, Progress & Compress). RWalk "takes the same ratio and then discards its scale" (`SPA1.md:31-33`). The direction s > 1 is also produced by a diagonal-against-full curvature gap (`a11_grade.txt:185`) |
| what would distinguish | COMPARISON.md's proposal: do the calibration factors land the effective weight on the *published* tuned λ on the published benchmarks? (`SEC_Prior_Art/COMPARISON.md:64-73`; there SEEN, so R5.) The criterion must be one the frozen learner fails (`COMPARISON.md:88`). Also a pre-declared location test (calibrated weight against tuned λ, log-scale error) on informative carriers |

### O6. The clip and divergence

| layer | content |
|---|---|
| observed | Unguarded SEC diverged on 10 of 42 carriers, with a median per-carrier max s of 28599.49 against 212.25 on the rest (F6 HOLDS; `WHY_SEC4_WORKED.md:181-182`). The clip removed SEC4's divergences (SEC4-2 PASS-0). Freezing the capped coordinates alone (M5) is within a step on only 1/13 (FM5 FAILS: "the penalty below the cap matters") |
| CRR interpretation | SEC5's A6 reading ("never an accumulated count", `theory/CRR.md:151-152`) was tried as the cause and closed in development. Divergence occurs with one settled task (anneal), so "the calibrated scale, not accumulation, crosses the edge" (AGENT_LOG 178) |
| ordinary explanation | AR1's explicit-Euler bound η·λ·F ≤ 1 (SPA1 S5 REDUNDANT) |
| what would distinguish | Nothing CRR-specific is on the table |

### O7. One configuration against a 3-point mini-sweep (the P rows)

| layer | content |
|---|---|
| observed | SEC3-P 5/6, SEC4-P 6/6 and SEC5-P 6/8, each PASS-0. SEC6R-P 7/9, PASS-0 UNINFORMATIVE. CPU share of the full sweep about 0.05–0.066 (SEC3-K, SEC4-K, SEC5-K, SEC6R-K) |
| CRR interpretation | None |
| ordinary explanation | The mini-sweep {1, 30, 1000} is itself EWC λ values, so the same class-IL leniency is likely to apply. **Not computed:** `gate_posthoc.py` applied SEC6-G's rule to SCL3-3, SEC3-3, SEC4-1 and SEC5-1 only (`gate_posthoc.txt:5-15`). Whether M6 meets the P criterion on SEC3–SEC5 is not printed anywhere I found |
| what would distinguish | Apply the same post hoc gate to SEC3-P, SEC4-P and SEC5-P (a report, not a re-score), and declare a P-type row with its own gate in any successor |

### O8. Infrastructure: SEC6 (and the loader exclusions throughout)

| layer | content |
|---|---|
| observed | 0 of 12 carriers scored (STRING targets). Loader exclusions elsewhere: 3 of 9 (SEC4), 4 of 12 (SEC5), 3 of 12 (SEC6R Part B), 5 of 12 (SEC6R Part A) (ledger column 3) |
| CRR interpretation | Not applicable |
| ordinary explanation | Frozen parser; selection by metadata could not see the attribute type (`reports/sec6.md:45-62`) |
| what would distinguish | Not needed. Pure D. Its cost was 12 carriers made SEEN (`reports/sec6.md:67`) and a day |

### O9. The discriminating-subset tendency (candidate F; all counts derived, mostly post hoc or SEEN)

| layer | content |
|---|---|
| observed | **(a) Auditor's count (derived), P1's C0 runs (post hoc, now SEEN).** On the 6 held-out carriers where M6 is behind (`gate_posthoc.txt`, marked *), I computed C0 − tuned = (M6−tuned) − (M6−C0) from the `m_checks.txt` per-carrier table (lines 77-108): cnae-9 +7.9167, isolet −0.1667 (step 3.470), semeion +3.7618, dionis +9.8102, cardiotocography +1.0377, volcanoes-d4 −88.9089. The clipped SEC is not behind on 5/6. **(b) Auditor's count (derived), SEC7 development (SEEN, random order, balanced accuracy).** Reading the per-carrier lines of `prereg/sec7/dev/gate7.txt`: on the 13 carriers where edge is BEHIND, the clipped SEC is "not behind" on 13/13, and ahead by more than its step on 4/13 (cnae-9, isolet, semeion, dionis). **(c) Auditor's count (derived), held-out clipped scorings only, on carriers where the frozen learner is behind:** cardiotocography (SEC4-1 +1.0377, not behind), volcanoes-d4 (SEC5-1 −88.9089, behind), Advanced_IoT_Dataset (SEC6R-1 −2.0559, step 2.90, not behind; SEC6R-G edge −24.9501). That is 2/3 |
| CRR interpretation | None |
| ordinary explanation | A calibrated EWC penalty that does not diverge is a reasonable regulariser. The κ clip was chosen on 16 SEEN carriers that overlap (a) and (b) (SEC4-D; AGENT_LOG 169). (b) is SEEN data and development, "not evidence". The subset is selected on the reference's own failure (post hoc). Mixed arms; tiny N |
| what would distinguish | A pre-registered per-carrier conditional criterion (score only carriers where the do-nothing control is behind), with N large enough to decide, on unseen carriers |

---

## 5. Salvage classification (A–G) and propagation level

**Is SEC a CRR idea?** No, by every source in the record.
- It is the Laplace weight + a secant units correction + AR1's clip. F11 HOLDS: 0 of 7 operational clauses
  (`a11_grade.txt:125, 213, 242`).
- Its *provenance* is the CRR programme. It came from H-EQ's mandatory R7 Bayes baseline and EQ3-B's miscalibration
  finding (AGENT_LOG 143; `COMPUTE_SAVINGS.md:8-17`).
- A1′ was read onto it afterwards as a name, explicitly hindsight (`2026-09-25_cramer_rao_reading.md:125-126`).
- The two CRR-guided variants added nothing:
  - A6-MEAN: SEC5-C-DEV, D-GATE-C CLOSED;
  - the M4 "arc secant": FM4 ties C0 on 29/30 and is ahead on 0/30. "As implemented it is a 5-segment least-squares secant,
    not CRR's arc" (`WHY_SEC4_WORKED.md:211-212`).

So **no negative or positive result in this lineage propagates to a CRR principle in `theory/CRR.md`**. The highest level
reached is the method (SEC, clipped SEC) as a tuning-free weight on class-IL tabular streams with this MLP.

| line of inquiry | class | core → operationalisation → test → failure; highest level reached |
|---|---|---|
| SEC/clipped SEC as a tuning-free replacement for the λ sweep | **C** + **A (method level only)** | Laplace-weight principle (not CRR) → secant calibration (+ clip) → "not behind the tuned λ" on unseen families → SEC3-3 FAIL, SEC5-1 FAIL (not fragile), SEC6R-B FAIL (AR1-B, SI-1C 8/9 against 7/9), SEC6R-2 FAIL. **Highest level: one method on one benchmark type** (class-IL tabular, 256-unit MLP, SGD). SPA1 verdict KNOWN for the parts (`SPA1.md:9-12`) |
| The "not behind the tuned λ" passes (SCL3-3, SEC4-1, SEC6R-1/C/P, SEC3-P/SEC4-P/SEC5-P) | **D/E (instrument / identifiability)** | Criterion a1 on stream a2 → met by M6 on 24/30 (FM6 FAILS) → SEC4-1-G, SEC6R-G, SEC6R-A-G CLOSED; SEC7-A CLOSED. **Level: instrument only.** It says nothing for or against SEC's mechanism. SCL3-3 is the exception (gate OPEN, by one carrier). The P rows' gate was never computed |
| The FAILs labelled "would be printed UNINFORMATIVE" (SEC3-3-G, SEC5-1-G) | **A (method level), with a labelling caveat** | My reading, interpretation only, verdicts unchanged. A criterion that a do-nothing learner meets is *lenient*. A method that fails it is behind the tuned λ by a step where freezing after task 1 was not (M6 not behind on 7/8 in SEC5: SEC5-1-G). The symmetric "UNINFORMATIVE" label understates the negative evidence for the FAILs, while correctly emptying the PASSes |
| Secant units calibration (the step SPA1 "did not find") | **F** | Units correction → s_j = c_j/ρ_j → span collapse (SCL3-4 PASS-0 held-out; SEC1-4 FAIL seen, SEC3-4 FAIL held-out); F2 FAILS 2/5; F4 FAILS on 42, HOLDS post hoc on 16. Unresolved, mixed, never tested on an informative criterion. Not CRR |
| Stability clip | **C** | AR1 (SPA1 S5 REDUNDANT). SEC4-2 PASS-0; SEC5-2/SEC6R-2 FAIL where the carrier needs strength above the edge |
| SEC3 guard (raw-Laplace fallback) | **F (delayed, not killed)**, then superseded | G-RESCUE FAILS by −1.9792 against step 1.7305 on a single SEEN carrier (`gate_SEC3.txt:13-15`). Report-only 6/6 (SEC3-GR). A different guard (the clip) passed the next day (SEC4-1) |
| SEC6 | **D** | Loader defect, N = 0, NOT DECIDABLE. No bearing on SEC or CRR |
| SEC7 | **E / D (benchmark design)** | "a design failure of the benchmark, not a test of SEC" (SEC7-A). R12 stop |
| CRR-guided A6 variant (SEC5) | **B (one operationalisation; development level)** | A6 bounded strength (`theory/CRR.md:144-152`) → "past importance averaged over settled tasks" → D-GATE-C on 22 SEEN → CLOSED (D-ADDS: −0.2021). **Level: one development operationalisation.** It does not reach A6. The reading "accumulation causes divergence" was refuted on anneal (AGENT_LOG 178) |
| CRR-guided M4 "arc secant" (P1) | **C (tie) at one implementation** | Not CRR's arc as implemented; FM4 ties. Says nothing about D2/H-T1 |
| One configuration against the 3-point sweep | **F, with E unexamined** | PASS-0 three times. Possibly lenient for the same class-IL reason; not gated |
| Discriminating-subset tendency (O9) | **F (weak)** | Derived, post hoc / SEEN / small N. The most specific candidate phenomenon in the lineage |
| G (strong surviving lead) | **none** | No row survives at PASS-1 without a closed instrument gate beside it. SCL3-3 (gate OPEN) is FRAGILE PASS-0, did not replicate (SEC3-3), and is not a CRR rule |

---

## 6. Extinguished-lead check

1. **SEC4-1 was "killed" at the correct level, but the question it was meant to answer was never answered.**
   - SEC4-1-G removes the evidential value of the PASS at the level of the instrument (criterion + stream), not the method.
   - The method-level negatives are separate and direct: SEC5-1, SEC3-3, SEC6R-B, SEC6R-2.
   - The clean question — does the units-calibrated, clipped Laplace weight match a tuned λ where matching is hard — was
     closed at the benchmark level (SEC7-A) without being asked on any informative stream. This is not an extinguished
     *CRR* lead, because SEC is not CRR. It is an **untested method lead** whose only tests used a lenient instrument.
2. **The "UNINFORMATIVE" label on FAILs (SEC3-3-G, SEC5-1-G) risks the opposite error:** reading real method failures as
   non-evidence. The rows themselves say "not a re-score … stands as scored". Phoenix should keep SEC3-3 and SEC5-1 as
   FAILs of the method.
3. **SEC7's stop was a whole-family gate (D-FAIL more than 15/30).**
   - It closed at 13/30 (SEC7-A).
   - On the 13 carriers where the frozen learner *was* behind, the clipped SEC was not behind on 13/13 (auditor's count,
     derived; SEEN development data, not evidence; §4 O9).
   - The design had no per-carrier informative-subset branch, so a possibly discriminating subset was discarded with the
     family. Under R12 that is the correct procedural outcome. It is also an example of a gate stopping at a level
     (family-wide informativeness) lower than the question (does SEC hold where the test can fail).
4. **The A6 variant closed on D-ADDS by −0.2021 mean, while matching the clip on 22/22 and 6/6** (SEC5-C-DEV).
   - It was closed for not *adding* over the clip, which is the right reason.
   - The conclusion "CRR's A6 reading pointed at the wrong cause" (`reports/sec5.md:100`) is evidence against one causal
     story (accumulation causes divergence). It is not against A6.
5. **No evidence of a CRR principle killed via SEC.** The danger runs the other way: external documents crediting CRR with
   SEC's passes. Compute_Savings states "SEC is a product of this repository's CRR programme" (`COMPUTE_SAVINGS.md:10`)
   beside "the ledger records SEC as 'not a CRR rule'" (`:16`).

---

## 7. Question-10 evidence (did the protocol prevent reasonable exploratory development?)

**Evidence that it did not prevent exploration (tempo and iteration were high):**
- **SEC went from idea to first test in hours, then to held-out in two days.**
  - It was defined on 2026-09-23 in scratchpad synthetic work "not in the repository" (`prereg/sec1/PREREG.md:54`).
  - The R5 test on SEEN carriers ran the same afternoon: prereg pushed 15:18:10Z, data 15:18:27Z (ledger SEC1-1).
  - The held-out test followed on 2026-09-25 (SCL3).
  - R3 cost exactly one calendar day per variant.
- **Each failure produced a new variant tested on a fresh family the next day.**
  - SEC3 FAIL (09-28) → clip chosen on SEEN (09-28) → SEC4 PASS-1 (09-29).
  - SEC5 FAIL (09-30) → SEC6 (10-01) → SEC6R (10-02).
- **Development stages on SEEN carriers were used repeatedly before hashes:**
  - SEC4-D (16 carriers), SEC5-C-DEV (22), SEC6 development (30, Amendments 1–3, AGENT_LOG 217–222), SEC7 (30);
  - SEC1's gate was redesigned before any carrier (AGENT_LOG 96).
- **The SEC3 guard gate closed narrowly** (−1.9792 against step 1.7305, one SEEN carrier). The guard was still run as a
  report (SEC3-GR 6/6). A successor guard was pre-registered the next day. That is a delay, not a suppression.

**Evidence that it constrained or misdirected:**
- **R12 stops** ended two lines without an exploratory alternative:
  - SEC5's A6 candidates (D-GATE-C) — fair, since they added nothing;
  - SEC7 (D-GATE-7) — a whole-family gate; see §6.3.
- **Supply of unseen carriers became a binding constraint.**
  - "PMLB … is exhausted" (AGENT_LOG 169 (3)); study 445 had "only 2 eligible datasets" (AGENT_LOG 235).
  - SEC6's loader defect consumed 12 carriers (ledger SEC6-1).
  - The one-prereg-per-dataset rule plus daily tempo spent held-out families quickly.
- **The adversarial strength was misdirected rather than excessive.**
  - The R4 gate for SEC (POS/INV/SHAPE, `prereg/sec1/PREREG.md:140-151`) tested the *method's arithmetic*, not whether
    the *criterion* could fail.
  - The criterion weakness was identified on 2026-09-25 (AGENT_LOG 131: 13 of 37 inert; proposals including "a
    pre-registered load-bearing criterion for every 'not behind' row"). The class-IL literature result was fetched the
    same day (`docs/citations/classil_benchmarks_2026-09-25.md`).
  - SEC3 (hashed 09-27), SEC4 (09-28) and SEC5 (09-29) were registered without such a criterion. A grep of
    `prereg/sec3`, `prereg/sec4`, `prereg/sec5`, `studies/sec3`, `studies/sec4`, `studies/sec5` for
    "inert|load-bearing|results_vs_published|last-task floor" returns nothing (auditor's search, derived).
  - The control entered a prereg only with SEC6 (09-30, AGENT_LOG 222, 224), after the PASS-1 had been labelled.
  - So the protocol's hashing, anchoring and sensitivity machinery was strict, while construct validity of the success
    criterion lagged by five days and three studies.
- **Owner pressure toward a positive narrative was resisted in the record:**
  - "Sec4 was successful" (PROMPT_LOG 257) → P1 over all families "rejected: analysing SEC4's six carriers alone
    (selection on the outcome)" (AGENT_LOG 212);
  - "Use the CRR to fine-tune" (PROMPT_LOG 238) → a gated development stage (AGENT_LOG 177).

**Net, for L-SEC.** The protocol did not prevent exploratory development. Iteration was fast, and development stages
existed. Its failure mode here was the opposite of over-suppression:
- a lenient criterion passed four studies before the do-nothing control was required;
- after that, the family-level gate (SEC7) stopped the one redesign that could have tested the method fairly.

---

## 8. Open questions for Phoenix

**May be explored (as method research, not CRR evidence):**
1. **The secant units calibration on a criterion a do-nothing learner fails.**
   - Options: task-incremental heads; a replay learner where the penalty is one term; a reference that must beat freezing
     (AGENT_LOG 238; `WHY_SEC4_WORKED.md:271-272`).
   - Declare the frozen-after-task-1 and fine-tune (λ = 0) controls as must-fail rows *before* any data
     (`2026-09-25_results_vs_published.md:94-97`).
2. **A per-carrier informativeness rule, declared in advance:** score only carriers where the do-nothing control is behind
   the reference, with an N rule that can decide (motivated by §4 O9; derived counts, not evidence).
3. **A location test of the calibration:** does 0.5·s̄ predict the tuned λ (log error) on informative carriers? Post hoc
   Spearman 0.752 on 16 (`a4_a6.txt:262`); 0.545 on 42.
4. **Against the published targets:** COMPARISON.md's proposal (calibration factor against the tuned λ published on
   Ritter/NCL/GVCL benchmarks), with a criterion M6 fails (`COMPARISON.md:64-73, 88`). It is SEEN in this repository, so
   R5 unless an unseen benchmark is found.
5. **Run the post hoc gate on SEC3-P, SEC4-P and SEC5-P,** so that the "one configuration against a 3-point sweep" PASS-0s
   carry their gate status (O7). This is a report only.
6. **AR1-B and SI-1C as the baselines to beat.** They matched or beat the clipped SEC on SEC6R-B and on SEEN development
   (`WHY_SEC4_WORKED.md:170-176`).

**Must never be claimed:**
- That SEC, the clipped SEC, or any SEC pass is evidence for CRR, or that CRR "predicted" SEC.
  - F11 HOLDS (`a11_grade.txt:242`).
  - The A1′ / Cramér–Rao reading is hindsight, R0–R2 (`2026-09-25_cramer_rao_reading.md:125-135`).
- That SEC is tuning-free, or a "finding". There is no PASS-2 (`reports/sec5.md:104-105`).
- SEC4-1's PASS-1 without SEC4-1-G beside it (the SEC4-1-G verdict text).
- Any compute, energy or CO₂ saving from `Compute_Savings/GLOBAL_ESTIMATE.md`: "an arithmetic on an unsupported premise,
  not an estimate of a saving" (`GLOBAL_ESTIMATE.md:131-133`).
- Novelty of the clip, of a path-fitted penalty, or of tuning-free weighting. SPA1 is KNOWN; only the units step was "not
  found", and "A one-day keyword sweep cannot show that it is new" (`SPA1.md:28-33`).
- The pooled 23/30 as a result. It is "a report, not a registered test" (`COMPARISON.md:57`), and M6 reaches 24/30 on the
  same carriers (`COMPARISON.md:78-79`).
- That SEC3-3-G or SEC5-1-G turn those FAILs into non-results. They "stand as scored".
