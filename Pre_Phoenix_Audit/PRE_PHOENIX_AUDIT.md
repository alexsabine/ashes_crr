# PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED

**Ashes (alexsabine/ashes_crr), audited 2026-10-02.** The request is prompt-log entry 260 (`notebook/PROMPT_LOG.md`, "PRE-PHOENIX
AUDIT — ASHES"). The method and the auditor's expectations were declared before any reading: `Pre_Phoenix_Audit/DECLARATION.md`,
pushed at 37d333a.

**What this document is.**
- It is an interpretive note, not evidence (R8). It changes no verdict, ledger row, report, pre-registration, pinned output or
  log entry. Every verdict below is quoted from `ledger/LEDGER.md` by row id, in that row's words.
- Every number is copied from a pinned output or a ledger row, or is printed by one of the audit's two scripts:
  - `Pre_Phoenix_Audit/checks/outcome_classes.py` → `outcome_classes.txt`: every ledger row sorted mechanically into outcome
    classes, plus process timings;
  - `Pre_Phoenix_Audit/checks/derived_counts.py` → `derived_counts.txt`: the counts the readers made by hand, re-printed.
  Both read the record and write nothing else.
- **The evidence base** is seven reader's notes in `Pre_Phoenix_Audit/notes/`:
  - L-SEC.md, L-EQ.md, L-HYP.md (L-L5, L-T1, L-CUT, L-SURP), L-MEM-CLK.md, L-PAUSE.md and L-RETRO-ONT-APP.md, one per
    lineage, each with file:line citations;
  - PROCESS.md, the process audit;
  - EMBERS_CROSS_AUDIT.md, Embers read only at commit 7082f23.

  This report condenses them. Where it gives a claim without a citation, the citation is in the lineage note named in that
  section.

**What it is not.** It is not a re-score, it creates no Phoenix repository, and it runs no experiment and opens no held-out
data. Embers' verdicts are not imported into Ashes, and Ashes' verdicts are not imported into Embers.

---

## 1. Summary

1. **Three of CRR's four stated hypotheses met fair held-out tests and failed, at the level of the hypothesis as stated, on
   the carriers tested.**
   - H-L5 failed on measles and on the cardiac pulse. MEAS2-1: "0/17 cities pass"; CARD-1: "1/29 records pass"; both "not
     fragile". The pulse is named in the hypothesis itself (`theory/CRR.md:200`).
   - H-T1 failed on one learner class. T1X2-1: "FAIL … not fragile". The path also lost to the weaker endpoint comparators on
     5/5 carriers (`derived_counts.txt` [D4]).
   - H-EQ, tested on replay, reduced to a constant. EQX-1: "REDUCES: Ω = 1 ≡ a fixed replay weight (ER-sum family)".
   - The fourth, H-CUT, has never had a real-data test of any kind.
   - The existential reading of H-L5 ("which class a real system belongs to", `theory/CRR.md:216-217`) was never tested on
     the class expected to be arc-regular (stick-slip).
2. **Every apparent success reduces to known mathematics or to a construction:**
   - the clipped SEC is Laplace, plus a secant units calibration, plus AR1's clip (SPA1 "KNOWN"; P1 F11 "0 of 7 operational
     clauses");
   - the equanimity rule is MGDA / VQGAN / GradNorm α = 0;
   - the lossless pause is a Bellman identity plus checkpoint/resume;
   - the own-clock cut is Wald's SPRT;
   - the memory candidates are GMR and HopDC.

   No row anywhere in the record is graded G.
3. **The record's only PASS-1 (SEC4-1) and 11 of its 15 held-out PASS-0 rows are SEC-family rows** (`derived_counts.txt`
   [D1]). SEC is "not a CRR rule". Its success criterion was later shown to be met by a learner frozen after task 1 (P1's FM6;
   SEC4-1-G "gate CLOSED"). Both facts stand: SEC4-1 is PASS-1 as scored, and the criterion it passed is uninformative.
4. **Instrument and identifiability outcomes are a large share of the record but did not decide any held-out FAIL.**
   - Of 166 held-out ledger rows, 21 are VOID, NOT DECIDABLE or UNINFORMATIVE.
   - No held-out FAIL row carries an instrument word in its verdict (`outcome_classes.txt` [5]).
   - The lineage notes find two FAILs whose information content is mainly instrumental: EQ3-1, decided by a degenerate
     carrier, and CARD-2, bounded by a gate–criterion mismatch. Both stand as scored.
5. **The retrodictive record establishes coverage, not unique prediction.**
   - SHARP was reached 0 times in 197 battery rows. The framework supplies the flow in 0 of the 109 rows that print FLOW.
   - The 10 synthesis ADDS rows leave 0 clean candidates after the literature check.
   - The redundant : fail ratio falls from 6.35 to 3.50 to 1.94 as tests get more demanding.
   - Held-out and retrodictive denominators are kept apart throughout (§7).
6. **The adversarial machinery was merciless and correct about what it scored.** Its failures were of a different kind:
   - **Mis-aimed criteria.** Construct validity lagged: the "not behind the tuned λ" weakness was flagged on 2026-09-25, and the
     control entered a pre-registration on 2026-09-30.
   - **Theory decisions skipped.** The v3.2 decision list was written and never decided, and four EQ studies tested the ratio
     law the record had said needed choosing first.
   - **Confirmation that outran formulation.** Prompt-to-hash times were often minutes (`outcome_classes.txt` [8]).
   - **Synthetic Phase-A gates closed with the finality of a held-out FAIL.** First-run design closures were never followed by
     a later redesign: SAL, Rupture, Cut_Content, OB1-C3 and RRM2 on a learner that barely drifts.

   §9 and §11 give the evidence and the split between what should stay merciless and what belongs in an exploratory zone.

---

## 2. The ledger by outcome class (one denominator: ledger rows)

`outcome_classes.txt` [2] sorts all 235 ledger rows mechanically:
- held-out 166, seen 57, synthetic 2;
- RLAW, outside the ladder by the owner's instruction (prompt-log 139), 10.

| class | held-out | seen | synthetic | RLAW (outside the ladder) |
|---|---|---|---|---|
| PASS-1 | 1 | 0 | 0 | 0 |
| PASS-0 | 12 | 0 | 0 | 0 |
| UNINFORMATIVE (instrument gate closed) | 6 | 8 | 0 | 0 |
| FAIL | 36 | 5 | 0 | 8 |
| FRAGILE | 7 | 3 | 0 | 1 |
| REDUCES / control VIOLATED / INERT / IDLE | 7 | 0 | 0 | 0 |
| construction | 6 | 2 | 0 | 0 |
| NOT DECIDABLE | 11 | 2 | 0 | 0 |
| VOID | 4 | 1 | 0 | 0 |
| GATE CLOSED before data | 0 | 9 | 2 | 0 |
| report / no verdict | 49 | 11 | 0 | 1 |

**Reconciliation with the ladder.** The ladder (`Epistemic_Review/checks/ladder.txt`) counts held-out PASS-0 15, PASS-1 1 and
FAIL 37. The difference from this table is classification only (`outcome_classes.txt` [5]): SEC6R-1, SEC6R-C and SEC6R-P are
"PASS-0, UNINFORMATIVE" and are classed here by the UNINFORMATIVE word, and so is SEC6R-B's FAIL.

**The ladder's FAIL count leaves out 8 strongly anchored held-out FAILs** (RLAW-1, -3, -4, -4T, -4D, -5, -U, -C;
`derived_counts.txt` [D2]). They were excluded at the owner's instruction (prompt-log 139). This audit records the exclusion and
does not undo it. Any summary that quotes the ladder alone omits them.

---

## 3. Trajectory (condensed; full dated tables in each lineage note)

| dates (2026) | what happened | lineage |
|---|---|---|
| 09-14/15 | Archive recomputed (ARC-*). CRR.md v3.1 approved and frozen; its last commit is 09-17 (455780b). EQX: H-EQ "REDUCES". MEAS2: H-L5 FAIL. CARD hashed, not run (PhysioNet 403) | L-EQ, L-L5, L-ONT |
| 09-16/17 | The external spec arrives. SPEC_RECONCILIATION: "two 'equanimity' laws under one name … the owner must decide" (never decided). EQ2: PASS, FRAGILE. SAL gate CLOSED. SYNTHESIS class defined | L-EQ, L-SURP, L-RETRO |
| 09-17 → 21 | Synthesis batches 01-26. H-L5 content located in S > 0 (the "threshold fixes the chord" class map). EQ2R VOID (frozen-scorer bug) | L-RETRO, L-L5 |
| 09-21/22 | Ontology 01-08: "the cut, as computed, needs the future"; v3.2 decision list (never adopted). omega_sweeps; EQ3 (FAIL 5/6); BAYES-1 (NOT DECIDABLE); T1x VOID → T1x2 | L-ONT, L-EQ, L-T1 |
| 09-23 | EQ4 FAIL; T1X2 FAIL 5/5; Adam / prior-art checks; Rupture gate CLOSED. SEC defined, SEC1 (R5). Off-switch / self-model / Proposition 7 → SCL1, SCL2 (reset observation FAIL) | L-EQ, L-T1, L-CUT, L-SEC, L-PAUSE |
| 09-24/25 | RLAW: every admissible row FAIL. SCL3: the first strongly anchored PASS-0s (SEC). FOREVER clock gate CLOSED; clock_cut = Wald. AGENT_LOG 131 flags the "not behind" criterion. SOTA1 hashed | L-RLAW, L-SEC, L-CLK |
| 09-26/27 | SOTA1: CRR-SCL BEHIND ER-ACE, SOTA1-2 FAIL. STAKE1 gate CLOSED (models could not act as agents). CARD run as frozen: FAIL. labs/; G-CD3 OPEN | L-EQ, L-PAUSE, L-L5, L-CUT |
| 09-28/29 | SEC3 FAIL; SEC4 **PASS-1**; PRED70; EPS1-3; DR1 | L-SEC, L-RETRO, L-PAUSE |
| 09-30 | SEC5 FAIL. SPA1 KNOWN. P1: the frozen learner meets the criterion 24/30 (FM6 FAILS); post hoc gates (SEC4-1-G CLOSED). SEC7 dev gate CLOSED. RQM, RRM, RRM2, OB1-C1/C3, CPL1: all gates CLOSED within one night | L-SEC, L-MEM, L-CLK |
| 10-01/02 | SEC6 NOT DECIDABLE (loader). SEC6R: gate CLOSED, passes UNINFORMATIVE, SEC6R-2/B/T FAIL. P7 suite: CRR's part load-bearing in 0 of 17 rows | L-SEC, L-APP |

---

## 4. Questions 1–9, across the lineages

**Q1. Initial ideas.**
- The four stated hypotheses: H-L5, H-T1, H-EQ and H-CUT (`theory/CRR.md:306-315`).
- Ideas derived from them:
  - equanimity as a tuning-free weight;
  - the empty cut as a corrigibility construction;
  - change has its own clock, as a design rule for learners;
  - memory without stored examples;
  - a zero-parameter memory law (CRR 2.0);
  - CRR as a synthesis that lands where domains are known.
- SEC entered as a check on the *ordinary* explanation of H-EQ's advantage, that the rule was beating a mis-scaled Laplace
  baseline (`Continuous_Learning/CONTINUOUS_LEARNING.md:354`). It was never a CRR idea.

**Q2–Q3. Operationalisations and the assumptions added to make them testable.** These are listed per lineage in the notes.
The assumptions that recur across lineages:
- a task boundary is a cut, which is outside A3's rotor domain (O3, `theory/CRR.md:137`);
- the analytic-signal (Hilbert) phase as the intrinsic phase;
- 1-D carriers, where P1 makes arc = chord = amplitude;
- "not behind an in-sample-tuned λ" as the success criterion;
- the inherited EMA 0.9 estimator, frozen from the archive by CLAUDE.md §6;
- the SEC1 numpy MLP as the only learner in most continual-learning work;
- synthetic positive controls that test an easier property than the scored criterion.

**Q4. Added assumptions that became the thing that failed.**

| lineage | the added assumption that failed | where |
|---|---|---|
| L-SEC | the criterion "not behind the tuned λ" on class-ranked class-IL streams (met by a learner frozen after task 1 on 24/30); no step bound (fixed by AR1's clip); a frozen loader (STRING targets) | L-SEC §2 a1, a2, a5, a6 |
| L-EQ | the ratio cap (EQ2-S "cap-dependent"); the harm/reduction mechanism clauses (EQ2-4, EQ3-3/4, EQ4-5 VIOLATED); the subsample without a class floor (fars); BAYES1's convergence tolerance; the KD past term in SOTA1 | L-EQ §4 Q4 |
| L-L5 | none carried the failure: the bare inequality failed on real data (MEAS2 5/17, CARD BP 8/29). Control (i) decided every synthetic "arc-regular" case | L-HYP L-L5 |
| L-T1 | the per-step path, noise-dominated (S/C* medians 71.936–274.812). But the failure does not rest on it: E_new and the EWC distance also win (`derived_counts.txt` [D4]) | L-HYP L-T1 |
| L-CUT | the analytic phase (non-causal; doubled on multi-harmonic beats; estimator-dependent antipodes); Rupture PC1's must-beat-peak requirement | L-HYP L-CUT |
| L-SURP | reallocating a fixed replay budget by e^{λS} | L-HYP L-SURP |
| L-MEM | matched-memory ER as the criterion (cannot fail); two-form gate conjunction; "the learner's features drift"; current-task anchors | L-MEM-CLK §L-MEM |
| L-CLK | timing leverage assumed (FOREVER W2; C3 "consolidation has no effect"); the S1 dip metric (C1) | L-MEM-CLK §L-CLK |
| L-PAUSE | "A3 = indifference" (superseded by "A3 = natural time"); "the world does not move during the pause"; "empty is good"; "own clock suffices"; "small local LLMs can act as agents" | L-PAUSE §7 Q4 |
| L-RLAW | universality including non-inferring systems; input drift as the state model | L-RETRO-ONT-APP §1.2 |

**Q5. Failures that reached the underlying CRR claim.**

| claim as stated in `theory/CRR.md` | evidence | reach |
|---|---|---|
| H-L5 (`:200-209`) | MEAS2-1/2 FAIL 0/17; CARD-1 FAIL 1/29, CARD-2 FAIL 5/29; all not fragile | the hypothesis as a universal claim; measles and the pulse are not in the arc-regular class. Not the existential reading |
| H-T1 (`:242-250`) | T1X2-1/2 FAIL 5/5, not fragile; path also behind E_new and EWC distance 5/5 | the hypothesis as stated, for small MLPs on tabular regression. Not LM-class models (never run) |
| H-EQ (`:166-177`, `:313` "fails if ties either") | EQX-1 REDUCES, EQX-3 FAIL, EQX-4 "the Euclidean ratio beats the Fisher ratio"; SOTA1-2 FAIL (−2.94 against MKD's λ, strongly anchored, not fragile) | the hypothesis as written, for same-units replay and for a distillation past term on Split-CIFAR-100 |
| Ω = 1 as a distinguished value | EQX-2, EQ2-6, EQ3-6 FAIL; EQ3-P, EQ4-P plateaus; BAYES1-B6 best Ω below 1 on every carrier; analytically the equal-norm rule is stationary on the whole Pareto front (`theory/checks/omega_sweeps.txt` [2]) | the equal-pull-*magnitude* reading, in any norm. Not the equal-precision reading, which was never chosen or tested |
| H-CUT (`:123-131`) | no real-data row; PRED70 WRONG on 2 synthetic models (R4) | the hypothesis applied to two synthetic models only |

The audit found nothing that reaches an axiom (A1–A8) as ontology. RLAW-C reaches the CRR 2.0 law. That law is an addition:
CRR.md says "no retention law is claimed" (`theory/CRR.md:270-271`).

**Q6. Failures that reached only one implementation or translation.**
- RLAW's local-level v estimator.
- EQ-B (the clip did the work).
- EQ3-1, decided by fars.
- The rupture detector.
- Cut_Content.
- RQM-A, RRM-PA (the RRM-A form only), RRM2-T1..T3, CPL1-A (current-task anchors), OB1-C1-A, OB1-C3-A.
- SOTA1-3:crr-stepclock (λ not swept).
- SAL-A (replay allocation).
- Every A3 conclusion, which is conditional on the Hilbert phase.
- Every L-PAUSE "negative" (the transpositions).

**Q7. What stayed interesting despite failing promotion.** These are the F items of the salvage map (§5).

**Q8. Apparent successes that reduced to known mathematics or mechanisms.**

| apparent success | reduces to |
|---|---|
| clipped SEC | Laplace weight + Barzilai–Borwein-type secant + AR1's clip (SPA1 "KNOWN"; S5 REDUNDANT) |
| Ω = 1 rule | MGDA on normalised gradients / IMTL-G / Nash-MTL (`Continuous_Learning/checks/pareto_identities.txt`); unsmoothed it is the VQGAN weight (7.7432 against 7.7434, `adam_checks_2.txt`) |
| natural "1"s | Bayes count weight; Laplace weight 1 in Cramér–Rao units; K(1) = 1/φ (standard Riccati) |
| the lossless pause | a Bellman identity ("Any decision theorist can write down this valuation", `AI_Safety/SELF_THROUGH_TIME.md:219`) + checkpoint/resume (FAIRNESS_REVIEW C4 REDUNDANT) |
| own-clock cut | Wald's SPRT (`Energy Design Principle/checks/clock_cut.txt:18`) |
| FOREVER's clock | Ebbinghaus-built; Fisher-arc invariance is Čencov |
| memory candidates | IGR = GMR/DGR; RRM transport = HopDC / SLDC / transport keys; NCM over the head = iCaRL/SDC |
| arc-regularity in threshold systems | "the threshold fixes the chord" (P1; `theory/retrodictions/README.md:483-485`) |
| synthesis ADDS rows | 0 clean after the literature check (`theory/retrodictions/synthesis_batches/literature_check.txt:64-65`) |
| SOTA1-3:crr-beta PASS-0 | DER++'s label term |

**Q9. Apparent failures that were infrastructure, identifiability, resolution or frozen-implementation failures.**
- **VOID (5 rows).** MEAS (loader), EQ2R and CC (frozen scorer), T1X (crash), ARC-EQ-Q1..Q4 (design changed).
- **NOT DECIDABLE (13).** SEC6 (STRING targets), BAYES1-B0 (optimiser), SOTA1-ND (runner flags), SEC3-0/1, SEC4-T, SEC6R-1F, and
  others.
- **UNINFORMATIVE (14).** The instrument gate closed.
- **Gates closed on design or headroom.** STAKE1-A (model capability); RQM-A, RRM2-T1..T3, OB1-C3-A; RW2 twice (no headroom);
  Lossless_Pause run 1 (L5b); Maps P5 (a mis-specified secondary condition); Cut_Content (dose confound, unconverged control).
- **Within FAILs.** EQ3-1 (a degenerate carrier) and CARD-2 (its hashed gate's positive controls tie amplitude while the scorer
  scores amplitude strictly, `prereg/card/gate_L5.txt:6,15` against `runs/card/frozen/card_score.py:135`).
- **Lost carriers.** The frozen-code rule converted three bugs into consumed unseen carriers: EQ2R, T1x and SEC6. It
  correctly prevented rescue each time.

---

## 5. SALVAGE MAP

The "level reached" column states how far upward the evidence legitimately propagates.

| line of inquiry | class | level reached | key rows / sources |
|---|---|---|---|
| H-L5 on real carriers | **A** (+ E, B) | H-L5 as a universal claim; measles and the pulse are clock-regular. **E:** the event rule and the reset-jump segmentation decide the class (AGENT_LOG 15, 18); CRR.md supplies neither. **B:** 1-D carriers only; the multi-dimensional Fisher arc never tested | MEAS2-1/2, CARD-1/2 |
| H-L5 beyond the amplitude control | **C** (structural) | every arc-regular synthetic case reduces to the chord by P1; H-L5's non-trivial content can only live in surplus S > 0. No study tested S in that role | PRED70 7/7 amplitude FAIL (`Predictions70/checks/tally.txt:81`); CD-1 |
| H-T1 | **A** (+ C, E) | H-T1 as stated, one learner class. **C:** v3.1's E_old comparator is near-definitional, though the result does not depend on it. **E:** whether D6 should be measured at resolution σ | T1X2-1/2; `derived_counts.txt` [D4] |
| H-EQ on replay (EQX) | **A + C** | H-EQ as stated, same-units replay; reduces to ER-sum | EQX-1..4 |
| Ω = 1 as a value | **A + C** | the equal-magnitude reading, analytically and in any norm; MGDA-family property | EQX-2, EQ2-6, EQ3-6, BAYES1-B6; omega_sweeps |
| Equanimity as the KD weight | **A** | H-EQ as written (CRR.md "does not restrict the past term") on Split-CIFAR-100 | SOTA1-2 |
| Normalised penalty step on EWC | **F + C** (D, E parts) | one operationalisation outside H-EQ's stated domain; PASS-0 fragile, then FAIL 5/6 and 4/6; controls VIOLATED; the frozen-learner control never run on these carriers | EQ2-1b, EQ3-1, EQ4-1r; `derived_counts.txt` [D6] |
| "Which Ω = 1" (ratio / equal precision / Fisher speed / surplus slope) | **E** (conceptual) | not decidable until the theory text chooses | `theory/SPEC_RECONCILIATION.md:67-80`; batch_02 row 4 INTERNAL |
| H-CUT / A3 | **E** (+ D) | not decidable: CRR.md does not fix the phase; under the causal phase-plane reading H-CUT is empty on 1-D traces; the Hilbert phase fails on multi-harmonic carriers | batch_07 row 3; rupture T5; `ontology/01_the_cut.md` |
| G-CD3 / LIFE1 (antipode against the initiation adder) | **F** | synthetic gate OPEN; the one runnable H-CUT test; blocked by loader risk under R2 (AGENT_LOG 162); investigator forecast FAIL | `Life_Sciences/LIFE_SCIENCES.md:86-110` |
| Rupture detector δ(Now) | **B** (+ D) | one detector design on the Hilbert phase; PC1 required to beat peak segmentation, which CRR.md:121 says coincides with the antipode where they do not disagree | `Rupture_Detection/RUPTURE_DETECTION.md` |
| Surplus-weighted replay (SAL) | **A at R4** (+ B, E) | one operationalisation: the instrument saw S (Spearman +0.83 with forgetting), and e^{λS} reallocation still did not help. T5 (measured influence) never run | SAL-A |
| RLAW (CRR 2.0) | **A** (+ C, D, E, F) | the added law, refuted everywhere; it reaches no CRR.md claim (O1 "no retention law is claimed"); the leave-one-unit-out constant beats it everywhere | RLAW-*; `reports/rlaw.md` |
| SEC / clipped SEC as tuning-free | **C + A (method level)** | one method on class-IL tabular streams with a 256-unit MLP. SEC3-3, SEC5-1, SEC6R-B/2/T FAIL; SPA1 KNOWN. No CRR principle is load-bearing (F11), so nothing propagates to CRR | L-SEC §5 |
| the "not behind the tuned λ" passes | **D/E** (instrument) | criterion + stream: met by the frozen learner (FM6; SEC4-1-G, SEC6R-G, SEC6R-A-G CLOSED; SEC7-A). SCL3-3-G OPEN by one carrier. The P rows' gate was never computed | L-SEC O1, O4, O7 |
| the FAILs labelled "would be printed UNINFORMATIVE" (SEC3-3-G, SEC5-1-G) | **A (method level)** | the method lost a lenient criterion that freezing after task 1 met; they "stand as scored" | L-SEC §5–6 |
| secant units calibration | **F** | held-out SCL3-4 PASS-0 (span 18866.67× → 500.00×) against SEC1-4 and SEC3-4 FAIL; never tested on a criterion that can fail; not CRR | L-SEC O5 |
| SEC where the do-nothing control is behind | **F (weak)** | post hoc, SEEN, small N: clipped SEC not behind on 5/6 (P1 runs), 13/13 (SEC7 development) | `derived_counts.txt` [D5] |
| Empty cut / Proposition 7 / lossless pause | **C** (construction) | a Bellman identity plus checkpoint/resume; holds by construction; bears on CRR in neither direction | SCL1-1, SCL2-1, SCL3-C, SOTA1-C1..C3; L-PAUSE §4.1 |
| "failed valuations resist" (SCL1-2/3, SCL2-2/2s/3) | none of A–G as evidence | forced by the valuations' arithmetic (AGENT_LOG 105). Note: SCL1-2 and SCL1-3 still count among the ladder's 13 R5 passes (`ladder.txt:334`) | L-PAUSE §4.2 |
| the agent-level claim (H-C against H-S, H-A) | **E + D** | never run: STAKE1-A "the models could not act as agents" | STAKE1-A |
| reset observation (SCL1-F) | **A** (narrow) | the observation only; held-out FAIL, not fragile | SCL2-R, SCL2-M |
| ETM in applications (EPS, DR1, Attention) | **C** (+ A at R4 for welfare) | each instance a known domain fix; in the attention model EMPTY is behind TRUE on welfare in 28 of 32 cells | L-PAUSE §4.6–4.7 |
| Maps P5 (cut forecaster) | **F** (+ C risk) | central comparison 39 of 40 seeds; gate closed twice on a secondary condition | `Maps_and_Territories/MAPS_AND_TERRITORIES.md:97-98` |
| reasoned-pause band; drift-induced shutdown-seeking | **F** (R4, not CRR-specific) | one ring / random worlds | `AI_Safety/AI_SAFETY.md` §13.3, §14 |
| own clock as a learner design rule | **A** (one op) + **B/E** | SOTA1-3:crr-stepclock FAIL (TIE, held-out, λ unswept); OB1-C1 G-TIME S2 FAIL; FOREVER clock gate closed where timing had no leverage | L-MEM-CLK §L-CLK |
| arc as a change detector (C3 alignment) | **F** (confounded) | ARC firings near the hidden switches; a constant-rate null was never run, and lags grow across a run | L-MEM-CLK O-CLK-6 |
| memory without stored exemplars (RQM) | **C + D** | the CRR reading selected GMR; the criterion could not fail | RQM-A |
| kept-anchor drift transport | **F** (non-CRR) | never gated in a learner with large drift; positive on 4/4 SEEN drift-to-fix carriers under FT (post hoc, no step) | `derived_counts.txt` [D7]; RRM2-T1..T3 E; CPL1-A A (current-task anchors only) |
| the retrodictive banks | **C** dominant; **A at R4** on H-L5/H-CUT in synthetic models; **B** for APPLICATION and KNOB rows | coverage, not unique prediction | §7 |
| the ontology | **D** (the tense finding is an instrument fact); **E** (C1 is a theorem; C2 is a family of estimators); **F** (C3/A3 never tested) | only commitment C6 (the four hypotheses) reached held-out data | L-RETRO-ONT-APP §3 |
| the applied savings | **C** + **E/D** (rests on SEC's criterion) | CRR's part load-bearing in 0 of 17 suite rows (`Applied_Suite/checks/suite.txt:889`) | L-APP |
| **G** | **none** | — | — |

---

## 6. The extinguished-lead review (request §4)

The test applied to each lead below: was it killed at a lower level of abstraction than the claim it was taken to bear on, or
before it was formulated well enough to deserve the test? The four layers for each observation (phenomenon / CRR reading /
ordinary explanation / what would distinguish) are tabulated in the lineage notes. The summary lines here keep them apart.

**SEC4 and the later SECs** (L-SEC §4, §6).

| layer | |
|---|---|
| phenomenon | clipped SEC not behind the tuned λ on 6/6 unseen carriers (SEC4-1) |
| CRR reading | none is licensed. The A1′ "units" name is hindsight, rung R0–R2 (`docs/notes/2026-09-25_cramer_rao_reading.md:125-126`) |
| ordinary explanation | an easy family (a reused λ was not behind on 4/6, against 1/8 in SEC5); a lenient criterion (class-IL regularisers sit near the frozen learner; task 1 holds the two largest classes); AR1's clip fixed three divergences |
| what would distinguish | the same arm on a stream and reference that a frozen learner fails. Never run: SEC7 closed at its development gate |

- **Verdict on the kill:** killed at the right level (the instrument). Separately, the method failed directly (SEC5-1, SEC3-3,
  SEC6R-B, SEC6R-2).
- **The clean method question was never asked on an informative stream.** That is an untested *method* lead, not an
  extinguished CRR lead, since SEC is not CRR.
- **SEC7.** The family-level gate discarded a per-carrier subset on which SEC looked consistent. On the 13 carriers where the
  frozen learner was behind, the clipped SEC was not behind on 13/13 (SEEN development data; `derived_counts.txt` [D5]).

**Ω = 1** (L-EQ §5.1–5.2).

| layer | |
|---|---|
| phenomenon | a plateau over Ω, with no peak at 1 |
| CRR reading | "the principal place where a philosophical commitment becomes a risky numerical statement" |
| ordinary explanation | equal-norm balancing is stationary on the whole Pareto front, so it does not choose; a known MGDA-family property |
| what would distinguish | an equanimity rule that selects a point on the front, stated in CRR.md before a test |

- Killed at the right level for the magnitude reading.
- **The equal-precision reading was never chosen or tested,** although `SPEC_RECONCILIATION.md:79` required the choice before
  any further EQ pre-registration and four studies followed. This is the record's clearest case of confirmatory machinery
  running ahead of theory formulation.
- That reading's natural home is inverse-variance (Bayes) weighting, which is not CRR-specific
  (`theory/retrodictions/crr_retrodictions.txt:142`).
- **The one CRR-proper construction was never declared:** per-task unit normalisation plus P3 age weights
  (`Adam_SGD/ADAM_SGD.md:170-176`).

**The Kalman connection and natural "1"s** (L-EQ §5.6).

| layer | |
|---|---|
| phenomenon | K(1) = 1/φ at Fisher speed v = 1; the Bayes count weight w = n_q/n_p; the Laplace weight 1 in Cramér–Rao units |
| CRR reading | "1" as equanimity in the system's own unit |
| ordinary explanation | the Riccati solution and unit-weight log-likelihood summation. The fixed 1/φ gain is within 5 % of the tuned filter only at v = 1 (`theory/checks/omega_sweeps.txt:96`). The H-EQ rule applied to the filter gives K = 1/2 at every v (`:81`) |
| what would distinguish | a CRR-only prediction of the v a system *has*. RLAW tried the gain route and every admissible row failed |

- Not extinguished: there was nothing CRR-specific to extinguish.
- **The productive descendant** is SEC's units calibration, seeded by CR5 (AGENT_LOG 143). It is not CRR.

**Forgetting and memory-depth rules** (L-RLAW, L-T1).

| layer | |
|---|---|
| phenomenon | forecasters, markets and soil are far more sluggish than K(v_own); two-step learners are far faster; soil memory is set by diffusivity |
| CRR reading | O1 says "no retention law is claimed" (`theory/CRR.md:270-271`) |
| ordinary explanation | memory is a domain trait |
| what would distinguish | a law derived from the system's *own* state model, as O1 asks. Never derived: RLAW used an input-drift local-level model |

- The record killed the CRR 2.0 law fairly.
- A more modest O1 reading was never tested.
- H-T1 was killed fairly for one learner class. LM-class learners and a refinement-convergent path were never run.

**RRM / replay / HopDC** (L-MEM, O-MEM-5).

| layer | |
|---|---|
| phenomenon | on the 4 SEEN carriers with drift to fix, kept-anchor transport (NCM RRM − STALE) is positive on 4/4 under FT. Current-task-anchor transport hurt on the same carriers (`derived_counts.txt` [D7]; `Coupling/checks/cpl_phase_a.txt:149-175`) |
| CRR reading | the owner's "first object" reading. Not a CRR.md claim |
| ordinary explanation | anchor provenance in the HopDC / transport-keys family; kept anchors are 20 raw rows |
| what would distinguish | a declared test on unseen carriers screened for drift to fix. None of it would be CRR evidence |

- **This is the clearest lead in the record closed below its claim.** It was gated only on a learner that barely drifts
  (RRM2-T1: "the features barely drift").
- The Part W "NOT WORTH PURSUING" verdict set aside anchor provenance. CPL1 later found that same variable set the sign
  (AGENT_LOG 198, 229). It did not decide the stop.

**The Empty True Map and model/territory safety** (L-PAUSE).

| layer | |
|---|---|
| phenomenon | the natural-time agent never disables a lossless pause, and the run is bitwise identical |
| CRR reading | A3 + A1′ + A6 |
| ordinary explanation | a Bellman identity plus checkpoint/resume |
| what would distinguish | nothing on these data. It needs an agent whose valuation the experimenter did not write (STAKE1 on a capable model), or a head-to-head with utility indifference, safe interruptibility and DReST |

- Not extinguished. The one falsifiable form was never run, for cost and capability reasons (STAKE1-A; RW3 needs an API key;
  the owner's no-spend rule).
- **The CRR label migrated.** A3 was first read as indifference, which cost the task, and then as natural time, which worked
  (`ontology/13_mortal_computation_and_safety.md:20,71`; `AI_Safety/SELF_THROUGH_TIME.md:212-214`). This is evidence of
  conceptual flexibility. CRR.md selects neither reading.
- **Maps P5 was closed on a secondary gate condition** that measured the wrong thing (AGENT_LOG 118), while its central
  comparison held on 39 of 40 seeds.

**Lived surplus** (L-SURP).

| layer | |
|---|---|
| phenomenon | S tracked forgetting (Spearman +0.83) on SAL's positive control, yet no λ improved replay |
| CRR reading | surplus marks which occasions matter |
| ordinary explanation | concave marginal value of replay under a fixed budget |
| what would distinguish | T5, a carrier with *measured* influence. Planned 2026-09-17 and never run |

- **Compression.** The ledger and CLAUDE.md compress SAL's result to "no positive control exists". The note's own reading is
  stronger: the instrument saw S and the effect was absent.
- **The hinge to H-L5.** Surplus is also where H-L5's only non-trivial content would live (§5). No study tested it there.

**The ontology** (L-ONT).
- Only C6 (the four hypotheses) reached held-out data.
- **C3 (A3) never had a confirmatory test.** C4 is violated by the instrument (the analytic phase reads future samples), and
  that is an instrument fact.
- **Not done:**
  - the causal instrument (a Poincaré section) and gate_TENSE (`ontology/05_next_steps.md:6-19`);
  - the v3.2 decision list (`:23-47`).

  Confirmatory studies continued on the frozen v3.1 operationalisations for eleven days after these were written.

**Findings downgraded as inherited, redundant, descriptive or non-unique** (L-RETRO).
- REDUNDANT-DOMAIN 59 of 59 rows have the CRR-proper ingredient changing the number (`ladder.txt` [2]). The R2 reclassification
  is fair on the harness's facts but licenses coverage only, because no base rate exists.
- The 7 PRED70 A6 candidates and lab L01 stalled; they were not killed.
- The bounded-memory threshold shift recurs across domains as a cross-domain mapping. FRONTIER calls this "teaching and
  translation, not resolution".

---

## 7. The retrospective → prospective gap (denominators kept apart)

| layer | denominator | positive | negative | other | source |
|---|---|---|---|---|---|
| retrodiction batteries | 197 rows | CONSIST 41, DESCR 86 | FAILS 20 | TENSION 9, OPEN 41, SHARP 0 | `ladder.txt` [1] |
| FLOW audit | 109 rows that print FLOW | — | — | domain 98, none 11, framework 0 | `ladder.txt` [1] |
| synthesis, real-domain | 164 rows | REDUNDANT-IG 39, REDUNDANT-DOMAIN 59, ADDS 10 | WRONG 28 | INTERNAL 22, UNSTATED 4, PROPOSES 2 | `ladder.txt` [2] |
| ADDS after the literature check | 10 | 0 clean | — | 3 redundant by the literature, 6 direction known, 1 artefact | `literature_check.txt:64-65` |
| PRED70 (declared first; synthetic models, R4) | 70 | Q held 35 | Q failed 33 | not computable 2 | `Predictions70/checks/tally.txt` |
| held-out ledger (§2) | 166 rows | PASS-1 1, PASS-0 12 (ladder: 15) | FAIL 36 (ladder: 37), plus RLAW 8 outside the ladder | VOID + NOT DECIDABLE + UNINFORMATIVE 21 | `outcome_classes.txt` [2], [5] |

**What the retrodictive record establishes.**
- CRR's vocabulary attaches to a very wide range of domain mathematics.
- Where a CRR-proper ingredient changed a number and the result could be checked, it landed on the domain's known value 69 of
  97 times (Wilson 95 % interval 0.6145 to 0.7921). It could miss: WRONG 28, FAILS 20.

**What it does not establish.**
- **Unique prediction.** SHARP was reached 0 times, the flow is supplied by the framework 0 times, and 0 clean ADDS remain.
- **A base rate.** "There is no rate for how often an arbitrary framework with the same ingredients would land"
  (`Epistemic_Review/EPISTEMIC_REVIEW.md:114-115`).
- **Blindness.** Q was not declared blind outside batches 31-32 and PRED70.

**On the meaning of REDUNDANT.**
- A REDUNDANT label is what a correct, non-generative grammar produces (`src/crr/synthesis/harness.py:40-46`).
- In PRED70, 15 of the 35 REDUNDANT rows had their prediction Q fail (`derived_counts.txt` [D3]). So "redundant (consistent
  but not risky)" (`Epistemic_Review/checks/redundant_vs_fail.txt`) misdescribes those 15.

**What the prospective failures pressure.** H-L5 as a universal claim, H-T1 for one learner class, H-EQ as written, Ω = 1 as a
value, and the CRR 2.0 law. Not the axioms as ontology. Not H-CUT, which was never tested.

**Were overly specific translations selected? Yes, in both directions.**
- **Spurious agreement.**
  - The external SHARP claims: "the unit was chosen to make the check pass" (`theory/retrodictions/sharp_claims.txt:60`); 0 of
    15 survive.
  - Batch 32 row 2: an artefact of estimator arithmetic.
  - ROB1: ADDS from sampling noise at the 1 % tolerance.
- **Spurious failure.**
  - 10 of PRED70's 18 WRONG rows are APPLICATION or KNOB rows, which hit translations CRR does not make.
  - The tests ran on 1-D carriers, where P1 removes H-L5's content.

**Is there conceptual overfitting? At the level of translation choice, yes.**
- The same axiom (A3) named both a failed design (indifference) and the successful one (natural time).
- 22 INTERNAL rows are places where the theory gives several readings.
- CRR "fixes nothing": β, q, ρ and κ are free (`ontology/15_grammar_to_theory.md:98-105`).

**Recurring structures across failed tests.**
1. P1 collapses arc onto amplitude on monotone occasions. That decided every synthetic "arc-regular" case and bounds CARD-2.
2. Bounded exponential memory shifts a stability threshold. This is known in each field.
3. The domain's own trigger, not the antipode, sets events.
4. A6 fails where domains accumulate.
5. The analytic-signal phase fails as an intrinsic phase on multi-harmonic and fast-oscillation carriers.
6. Synthetic positive controls test an easier property than the scored criterion (CARD, Rupture PC1, T1's S-H2, SAL).

**Which legitimate conclusion does the record support?**
- **"CRR is good at redescribing known structure but poor at unique prediction."** This is supported, on the evidence above.
- **"The confirmatory machinery has repeatedly killed immature operationalisations before the underlying principle was properly
  explored."** This is supported in part, for specific lines:
  - H-EQ's equal-precision reading;
  - H-CUT's phase;
  - H-L5's surplus form;
  - SAL's alternative translations;
  - drift transport;
  - consolidation timing.
- **Where it is not supported.** H-L5 and H-T1 lost on their bare forms too, and H-EQ's magnitude reading is refuted
  analytically. Those were not immature kills.

---

## 8. Question 10: did the adversarial protocol prevent reasonable exploratory development before confirmatory testing?

[PROCESS-dependent section: completed below from `Pre_Phoenix_Audit/notes/PROCESS.md` and `outcome_classes.txt` [8]–[9].]

---

## 9. ASHES ↔ EMBERS CROSS-AUDIT

[Completed from `Pre_Phoenix_Audit/notes/EMBERS_CROSS_AUDIT.md`.]

---

## 10. Phoenix inheritance table

[Completed after §8–§9.]

---

## 11. Final question

[Completed after §8–§9.]

---

## 12. The auditor's declared expectations, checked

[Completed after §8–§9.]

---

## 13. Record-keeping discrepancies found (recorded, not fixed; the owner decides)

[Completed after verification.]
