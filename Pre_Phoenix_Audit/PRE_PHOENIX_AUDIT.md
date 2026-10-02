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

   §8 and §11 give the evidence and the split between what should stay merciless and what belongs in an exploratory zone.
7. **Embers, the rotor extension, read at 7082f23.**
   - Its ledger holds no PASS. No Embers failure reaches a hypothesis stated in Ashes' CRR.md.
   - It is stricter than Ashes in four places: blame tables before data, decidability settled before held-out units are
     opened, multiplicity, and verified anchors.
   - It shares Ashes' two weaknesses: tempo, and no sanctioned way to validate a loader before the hash.
   - The two repositories converge independently on three live leads: stick-slip; indexing by the system's own events; the
     identifiability of the cut as A3's gating problem. They also converge on the main dead ends.
   - They disagree most on what the antipode's record means (D2) and on how far one FAIL propagates (D8). §9 states both
     sides.

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

Audited stage by stage, from `Pre_Phoenix_Audit/notes/PROCESS.md` (cited "PROCESS §n") and the Question-10 sections of each
lineage note.

### 8.1 The held-out scoring layer: merciless and correct

**What it did.**
- It refused to delete nulls (PL 11; AL 2).
- It refused to patch frozen code or score partial results (AL 40, 69, 153, 241).
- It refused to tune positive controls or thresholds after seeing results (AL 4, 13, 88, 118, 178, 192, 205, 238).
- It kept first-run outputs beside labelled post-run lines.
- It turned its own best pass into a caveat in the ledger (SEC4-1-G).
- **Robustness of the failures.** The large-effect failures are not fragile: MEAS2-1, CARD-1, T1X2-1, SOTA1-1a, SEC5-1.
- **Not weaponised against passes.** Post hoc additions weakened fails as well as passes: SEC3-3-G and SEC5-1-G sit beside
  FAILs (PROCESS §3(e)).

**Finding.** The record contains no case in which this layer suppressed a result that later proved real (PROCESS §7).

**One cost: held-out data consumed by infrastructure.**
- 27 held-out carriers were fetched for studies whose primary verdict became VOID or NOT DECIDABLE: EQ2R 3, T1x 6, BAYES-1 6,
  SEC6 12 (`derived_counts.txt` [D9]).
- The frozen-code rule converted each defect into lost carriers. That cost is the price of the rule's integrity, and it
  was paid correctly.

### 8.2 Before the hash: where maturity was missing

1. **Tempo.**
   - 15 of the 20 studies with a named request prompt were hashed within 25 minutes of that prompt's logged time
     (`derived_counts.txt` [D8]: EQX, MEAS, MEAS2, CARD, EQ3, BAYES-1, T1x, SEC1, SCL1, SCL2, SCL3, SEC3, SEC4, SEC5, SEC6R).
   - This is a lower bound on receipt → hash, and some designs were templated in CLAUDE.md §4–§6 beforehand (PROCESS §3(b)).
   - Within a lineage, each successor was hashed 0 to 9.07 h after the previous first score (`outcome_classes.txt` [8]).
2. **Theory decisions skipped.**
   - "Before any further EQ prereg the owner must decide which law carries the name" (`theory/SPEC_RECONCILIATION.md:79`).
     No decision is recorded, yet EQ3, EQ4, BAYES-1 and SOTA1 followed (L-EQ §4 Q6).
   - The v3.2 decision list (`ontology/05_next_steps.md` §2) has stood open since 2026-09-22. It covers which phase A3 cuts
     on, the event rule, the segmentation rule and A6's scope. CRR.md is still v3.1.
3. **Criterion construct validity lagged.**
   - The SEC criterion's weakness was flagged on 2026-09-25 (AGENT_LOG 131: 13 of 37 carrier-scorings INERT; a proposal for
     "a pre-registered load-bearing criterion").
   - SEC3, SEC4 and SEC5 were then registered without such a criterion (L-SEC §7, the reader's grep). The must-fail control
     entered a pre-registration with SEC6, on 2026-09-30, after the PASS-1 had been labelled.
   - The defect surfaced only after 30 held-out carriers had been scored (PROCESS §3(e)).
4. **Positive controls tested an easier property than the scored criterion** (L-HYP cross-lineage 4):
   - CARD: the gate_L5 positive controls tie amplitude, while CARD scores amplitude strictly;
   - Rupture PC1: its rationale beats clock windows, but it was required to beat peak segmentation;
   - T1: S-H2 builds path dependence into F by fiat;
   - SAL: "surplus tracks forgetting" is not the same as "e^{S} replay is optimal".
5. **Conceptual analysis arrived after the hashes.**
   - H-L5's real-data tests were hashed on 2026-09-15 (measles: request 21:11Z → MEAS2 hash 21:24:27Z; cardiac: 6.9 min).
   - The analysis that located H-L5's non-trivial content in S > 0, and showed that the event rule decides the class, came on
     2026-09-17 → 21.
   - CARD then ran as frozen on 2026-09-26/27 (AGENT_LOG 164 rejected a fresh prereg as rule-shopping). The protocol worked as
     designed; the cost was a second real-data test on an operationalisation chosen before the content was understood.
6. **Immature observation, immediate confirmation.** The SCL1 reset observation went to a hashed held-out replication about 15
   minutes after the owner asked (prompt 125 at 21:27:32Z; SCL2 prereg at 21:34:54Z). No exploration of mechanism, dose or task
   count came first. The FAIL (SCL2-R) is correctly scoped to the observation.

### 8.3 Phase-A and development gates: where closure became finality

**The closures.**
- 25 gates closed before any confirmatory data. Only 11 are ledger rows; the rest are in AGENT_LOG and notes
  (`derived_counts.txt` [D10]).
- By the process reader's classification (judgement, PROCESS §3(a)), the most common reasons were:
  - the hypothesis did no work, or was behind its comparator, on a gate that could have opened;
  - a positive control that was absent, could not win, or was invisible;
  - a design defect of the declared world.
- Several closures were found by the gate itself, on questions a short headroom pilot would have answered:
  - unlearnable rings (RQM run 1);
  - a criterion that cannot fail (RQM run 2, SEC7);
  - a learner whose features barely drift (RRM2-T1..T3);
  - a consolidation action with no effect (OB1-C3: G-MATTER and G-TIMING are pilot questions frozen into the gate);
  - no headroom (RW2 twice; Adam Declaration 2).

  L-MEM-CLK §L-MEM 7 notes that none of these needed held-out data to find.

**What happened next.**
- After a first closure, redesigns opened 5 times and closed again 5 times (PROCESS §3(a), judgement).
- Three of the redesigns that opened lead to the record's held-out passes: EQ2-1b, SCL3 through SEC1, and SEC4-1.
- Same-day redesign was refused each time as gate-shopping (CLAUDE.md §10). The stated route was "a new declaration, labelled
  post hoc, on a later day … only on the owner's instruction" (AL 122, 192, 209).
- 13 named follow-ups never reappear in the AGENT_LOG (`outcome_classes.txt` [9]): BAYES-1b, H-REG, LIFE1, the dose-matched
  CUT1, EQ5, the causal-phase cut, per-task normalisation, Ω scaled by settled occasions, a stronger RQM criterion, a SEC
  reference that can fail, a harder FED surrogate, the arc-triggered refresh C2, and RW3.
- The record does not separate the protocol from the owner's change of direction as the cause. After most closures the next
  prompt points elsewhere (PROCESS §3(d)).
- One R12-spirit stop was overridden by the owner: "I don't really want to give up on the continuous learning equanimity idea
  just yet" (PL 106). Declared synthetic exploration followed (Adam_SGD), then SEC (AL 96, 143). That lineage produced the
  record's only PASS-1, which a post hoc gate later emptied.

**A direct protocol block.**
- LIFE1, the one runnable real-data H-CUT test (G-CD3 OPEN), was not registered.
- A header-only check of the data's schema was ruled to be "opening data before the hash" (AL 162).
- Together with the VOID precedent of blind loaders, R2 as interpreted stopped the only ready test of CRR's most distinctive
  hypothesis.

### 8.4 Where exploration happened, and where it went

**Exploration was plentiful but unrecorded or unstructured.**
- **L-EQ:** ten synthetic batteries; an off-repository playground "permitted by the owner" whose numbers stay off the record
  (AL 3); a dev run on SEEN carriers before EQ4.
- **L-SEC:** development stages on SEEN carriers (SEC4-D on 16, SEC5-C-DEV on 22, SEC6 D-RUN on 30, SEC7 on 30). SEC itself was
  defined "in scratchpad work on synthetic quadratic worlds (… not in the repository)" (`prereg/sec1/PREREG.md:54`).
- **L-PAUSE:** an entire safety programme ran at R4, with declared batteries.
- **L-RETRO:** banks totalling 197 + 164 + 70 rows.

**What the exploration lacked.**
- It had no committed log of maturity, so the maturity of a design before its hash cannot be audited (PROCESS §7).
- It had no development loop between "declared" and "gated". A first synthetic gate run was the first test of the design
  *and* its last.
- The bank's exploration graded coverage ("does CRR agree with X?"). It never produced a revised CRR rule (L-RETRO-ONT-APP
  §2.11).

### 8.5 Answer to Question 10, from the record

**Yes, in specific places. Not at the held-out scoring layer.**

**Where it happened.** The adversarial protocol, together with the programme's tempo, prevented reasonable exploratory
development before confirmatory or gate testing in these places:
- the Phase-A gates closed on design defects and treated as final: SAL, Rupture, Cut_Content, OB1-C3, RRM2 on a non-drifting
  learner, Maps P5 on a mis-specified secondary condition, RQM's uncloseable criterion;
- the LIFE1 schema block;
- the failure to decide the theory's open readings (which equanimity, which phase, which event rule) before running four EQ
  studies and two H-L5 studies.

**Mostly not the strictness of R1–R15 as such.** The rules allowed new declarations on later days. The binding constraints
were three:
- **No exploratory stage.** There was no recognised, recorded exploratory stage between idea and gate, so exploration either
  stayed off the record or happened as a gate.
- **Tempo.** Hashes came minutes after requests.
- **Attention.** The programme moved on after closures; 13 follow-ups were never resumed.

**Also the opposite failure.** In the SEC chain and the applied valuations, confirmation and extrapolation ran *ahead* of
criterion validity: GLOBAL_ESTIMATE was re-pinned on SEC4-1 the day before SEC5-1 FAILed and SEC4-1-G closed (L-APP §4.5).

**A disagreement between readers, recorded without forcing it.**
- **L-SEC (§5, §6.2).** SEC3-3 and SEC5-1 should still be read as negative method evidence. A method that fails a lenient
  criterion, one a do-nothing learner meets, is behind where freezing was not.
- **PROCESS (§8).** A fail beside a CLOSED criterion gate must not be claimed as evidence against the method, "any more than its
  pass".
- **The ledger's own wording.** It supports the second reading for the label ("would be printed UNINFORMATIVE") and the first
  for the scoring ("FAIL as scored", "stands as scored").
- **What would decide it.** The same arms on a criterion the frozen learner fails.

---

## 9. ASHES ↔ EMBERS CROSS-AUDIT

This section summarises `notes/EMBERS_CROSS_AUDIT.md`, where every claim carries an [Embers] or [Ashes] file:line citation.
- **What was read.** Embers was read only at commit 7082f23 (2026-09-28T23:52:33Z). A `git ls-remote` on 2026-10-02 returned
  the same HEAD, so this is Embers' current published state. Nothing in Embers was modified or run.
- **Verdicts are not imported.** Each repository's verdicts are quoted in its own words and labelled with its name.

### 9.1 What Embers is, and what it inherited

**What it is.**
- "A restricted, unvalidated rotor extension of `ashes_crr`" ([Embers] `CLAUDE.md:6`).
- It was built in about 45 hours and pins Ashes at 0edbc37 for theory and rules.
- Its ledger has 12 rows and no PASS of any level.
- Its primary rows: H1CARD-1 "FAIL"; H1RESP-1 and H1GAIT-1 "NOT DECIDABLE"; STK1-1 "VOID".

**What it inherited.**
- Ashes' CLAUDE.md R1–R15 and the ladder, snapshotted verbatim and enforced by script.
- The synthesis harness, "ported verbatim in logic".
- Ashes' SEEN list.
- Ashes' verdicts, as *priors and lessons*, never as Embers rows ([Embers] `CRR_Ashes/README.md:202-222`;
  `docs/DOMAIN_PORTFOLIO.md:166-182`).

**Timing caveat.** Embers read Ashes when its ledger had 165 rows and no PASS-1. SEC4–SEC6R postdate it.

### 9.2 What Embers added: the rotor extension

It adds the following to CRR.md v3.1, which "has no equations of motion" ([Ashes] `theory/CRR.md:31-32`):
- the cut as the first passage through half of the **intrinsic Fisher arc** of an identifiable statistical circle, with the
  ordinary angular antipode as its *ablation*;
- the intrinsic, not ambient, chord;
- σ in Fisher-length units;
- constitutive laws of motion, while "not claim[ing] a universal law of motion";
- a regeneration seed separate from the phase, "an explicit revision" of A6;
- a cost bound;
- hypotheses H1 (the Fisher antipode beats the angular antipode and a fitted lag at locating an independently measured
  event), H2 (memory-coupled flow) and H3 (cost).
- Its transfer audit names exactly two structural commitments: S1 (the Fisher half-turn) and S2 (occasion-counted ageing,
  q^(n−j)).

### 9.3 Which Embers failures bear on baseline CRR, and which only on the rotor

**No Embers ledger failure reaches a hypothesis stated in [Ashes] `theory/CRR.md`.**
- H1CARD-1 tests H1, the Fisher antipode against the angular antipode, not H-CUT (antipode against extremum). Embers' own
  pre-data blame table limits it to "H1 for this (system, observation law) class" ([Embers] `prereg/h1card/PREREG.md:187`).
- H1GAIT and H1RESP are bridge outcomes: a loader issue and a resolution issue.
- STK1-1 is VOID (a file format and an HTTP 404). Had it run, it was the one Embers line that could bear on a *baseline*
  commitment: A6/P3 ageing counted in occasions, and A1′ natural time. Its successor stk2 is hashed but not run at 7082f23.
- At R4 or as wording, Embers' synthetic WRONG rows bear on baseline A6. A6 fails where a domain accumulates or needs
  several timescales, which CRR.md itself excludes. Maths_Repair MR-003 is a scope note on P3's ⟨k⟩ = q/(1−q), which holds on
  infinite support only.
- MR-002 and MR-004 bear on A3's identifiability under any Fisher-arc reading. The Fisher antipode is a property of the pair
  (rotor, observation law), and it differs from the angular antipode only through the odd harmonics of √g.

### 9.4 Where Embers' machinery is stronger, cleaner or fairer than Ashes'

1. A Bitcoin anchor is *verified* before every data step, including retrodiction declarations.
2. **A blame table in every prereg, fixed before data.** It states which conjunct a FAIL refutes and which it does not. Ashes
   had to reconstruct this level after the fact; it is most of what this audit's salvage map does.
3. **Decidability settled on training units before held-out units are opened** (the H1 calibration gate). Ashes' SEC
   instrument gates were computed after scoring, so they produced UNINFORMATIVE rows.
4. **Multiplicity:** Bonferroni within a same-day batch, with m fixed before the hash. Ashes has no family-wise rule.
5. **The adversarial code audit pinned with its defects in it** (DEFECT 11 → 0).
6. **Theory-level gaps stated as gaps** (MR-002), not left in an undecided list.
7. **Every prereg records an honest prior** ("FAIL (P ≈ 0.80)").

### 9.5 Where Embers may have become too confirmatory too early

1. **Tempo.** The first held-out data step came about 3 h 38 min after prompt 1.
2. **Data consumed without a verdict.** Three of its four scored real-data studies ended without a hypothesis verdict, for
   data-plumbing reasons that metadata-only scouting could not see. The records were consumed.
3. **A test that could not support its hypothesis.** The one FAIL (H1CARD) was run on a carrier chosen by a channel-count
   rule, with a recorded prior of "FAIL (P ≈ 0.80)". Embers' own portfolio says a PASS there "cannot validate the
   rotor-specific cut theorem".
4. **One FAIL read too broadly.** That FAIL then supported the sentence that S1 "has not survived"
   ([Embers] `docs/TRANSFER_CANDIDATES.md:89`). This is stronger than Embers' own blame table and its rule of two FAILs per
   class.
5. **The same suppressive effect as Ashes.** "No peek before the anchor" covered file formats, so exploratory contact with
   real data before the hash was effectively zero. Ashes has the same effect (LIFE1).

### 9.6 Do they identify the same live leads and the same dead ends?

**Live leads: independent convergence on three points.** Neither repository has a G.
- **Laboratory stick-slip as the right next carrier.** Ashes wants it for H-L5's existential reading; Embers wants it for S2.
  Neither ran a test that scored.
- **Indexing by the system's own events.** In Ashes this is natural time and the own clock: the one held-out learner test
  TIEd. In Embers it is occasion-counted memory, VOID or pending.
- **The identifiability of the cut** (which phase, which carrier, which event) as the problem that gates A3.

**Dead ends, mostly the same.**
- **Agreed independently, on disjoint system sets:**
  - retrodictive consistency is not evidence;
  - A6 fails where a domain accumulates;
  - at R4, the antipode loses to domain triggers and extrema.
- **Agreed because Embers read Ashes** (inherited, so not independent confirmations):
  - H-EQ's CRR-specific parts failed or reduced;
  - H-L5 fails on measles and the pulse;
  - the empty cut is a construction.

### 9.7 Disagreements: both interpretations, no convergence forced

| # | topic | Ashes reading | Embers reading | what would decide |
|---|---|---|---|---|
| D1 | What "half a turn" in A3 is measured in | intrinsic phase, unspecified in CRR.md; implemented as the analytic-signal phase + π; the choice is open (H-CUT class E) | half the intrinsic Fisher arc of a chosen observation law; the angular antipode is the ablation (an "additional modelling commitment") | a theory decision first (Ashes v3.2 item 1; Embers MR-002). Then one study scoring own events against the Fisher antipode, the angular antipode, the extremum and a fitted lag, on a carrier with large odd harmonics |
| D2 | The status of the antipodal cut | the lineage audit: "No ledger row tests H-CUT … Not extinguished", class E; R4 WRONG rows reach H-CUT only in model systems. **Ashes' ontology summary is more negative:** "found undecided and, where decided, wrong" (`ontology/02_commitments.md:149`), so part of this disagreement is inside Ashes | "Domain events sit at extrema, not antipodes"; after H1CARD, S1 "has not survived" | a held-out H-CUT test on own events with its own gate: G-CD3/LIFE1 (Ashes) or odd-harmonic carriers (Embers). Neither has run |
| D3 | What a fair cut test needs | the system's own event on the carrier, scored against the extremum | an *independent* event channel: "Never derive the tested event from the phase used to predict it" | a gate running both designs on the same surrogates, to see whether same-channel events create circular alignment |
| D4 | A6's successor state | the Fréchet mean of past occasion contents; the cut resets C | the seed is distinct from the phase: "an explicit revision" | definitional; an owner decision. A domain where the phase does not jump at the cut makes literal A6 an extra impulse |
| D5 | Laws of motion | CRR has none; the framework supplies the flow in 0 of 109 FLOW rows | adds constitutive laws but claims none universal; physics is "supplied by the domain" | the repositories' texts agree; the difference is with the owner's framing. An S2-type transfer test (fit in one condition, predict another) would show whether the laws carry content |
| D6 | The chord in D3/P1 | "the geodesic distance" on the manifold; S = 0 iff monotone in 1-D | requires the *intrinsic* chord. The ambient simplex chord gives a monotone half-turn positive surplus (1.397009 against 0.880169) | mathematical: a v3.2 wording decision. No Ashes text addresses it |
| D7 | The unit σ | 1.4826·MAD of a raw occasion statistic; renaming a constant unit cannot move an H-L5 verdict | σ must be a Fisher length; a raw residual cannot divide a Fisher arc when detectability varies with the state | a declared rerun of one SEEN study under both units, on a carrier whose metric varies along the record |
| D8 | How far one held-out FAIL propagates | H-L5: A at the universal level, not the existential one. H-T1: A for one learner class | "empirical readings of H-L5, D6/H-T1 and the regeneration law retracted for those classes", although Embers' own rule asks for two FAILs per class, and its taxonomy calls the retraction counts "a proposal for the owner" | for H-T1, Ashes' numbers already show that the FAIL does not rest only on E_old ([D4]). For H-L5, a test on a carrier with an arc-regular prior (stick-slip). For semantics, a propagation rule adopted before data |
| D9 | What RLAW reaches | the added law only; not A6/P3 ("CRR does not fix q"; "no retention law is claimed") | listed under the A6 lesson: "A6 fails where domains accumulate … RLAW-U 0/5" | textual. CRR.md supports the Ashes reading. Embers juxtaposes the two; it does not claim entailment |
| D10 | Where RLAW is counted | outside the ladder at the owner's request; a separate column here | "the ladder omits the cleanest negative in the record" | a reporting choice; both call the rows FAIL |
| D11 | What the empty-cut work is | a construction; it does not propagate to CRR.md | "R0 in substance"; prior art | no disagreement of substance; only the rung label differs |

**Reading.**
- D1–D3 are one cluster: both repositories found the same identifiability problem and answered it differently. Ashes left
  the phase open. Embers fixed one answer, tested it, and found the answer is itself relative to the instrument (MR-002).
- Ashes' implemented cut is structurally closer to Embers' *ablation* than to Embers' hypothesis. H1CARD registers no
  angular-against-lag comparison, so it gives no verdict on the angular reading.
- D2 and D8 are disagreements about the *meaning* of failures. On both, the Ashes lineage audit is more conservative about
  propagation than the lessons Embers drew from Ashes. On D2, Ashes' own ontology summary sides with Embers.

### 9.8 What Phoenix inherits from Embers' machinery

The Ashes-side recommendations in §11 already ask for a pre-hash maturity stage. Embers shows four concrete devices for it:
- a blame table before data;
- a decidability gate on training units before held-out units are opened;
- multiplicity within a batch;
- a verified anchor.

Embers also shows the same gap Ashes has. Neither repository has a sanctioned way to validate a loader or a file schema
without "opening" held-out data, and both lost held-out records to that gap.

---

## 10. Phoenix inheritance table

The rungs are the ledger's own. Nothing here is promoted. "Failure level" uses the request's scale: principle, hypothesis as
stated, one operationalisation, one implementation, or instrument only. The table is Ashes' inheritance only; Embers'
lineages are in §9 and `notes/EMBERS_CROSS_AUDIT.md`.

**What the lineages are.**
- Stated hypotheses (`theory/CRR.md` §9): L-L5, L-T1, L-EQ, L-CUT.
- CRR-derived work: L-SURP, L-RLAW, L-CLK, L-PAUSE, L-MEM, L-RETRO, L-ONT.
- Not CRR, kept for lineage: L-SEC, L-APP.

**For every lineage, Phoenix must also never claim** novelty without a literature check, or a number not printed by a script.

**Lineages that test a stated hypothesis**

| Lineage ID | Core CRR idea | Operationalisation(s) tried | Strongest supporting observation | Strongest negative evidence | Failure level | Current epistemic status | Mundane explanation | CRR-specific possibility | What Phoenix may explore | What Phoenix must never claim |
|---|---|---|---|---|---|---|---|---|---|---|
| **L-L5** | "change has its own clock": arc between own events is more regular than clock time (`CRR.md:196-219`) | CV(arc) vs CV(clock) beyond amplitude, identity-metric and peak controls; measles (1-D Poisson), cardiac BP/ECG (R-R); synthetic banks | MEAS2-3 control line 12/17 (not H-L5); CARD-2 bare inequality 19/29 (amplitude ties) | MEAS2-1 0/17, CARD-1 1/29, CARD-2 5/29, all not fragile; PRED70: 7/7 "arc-regular" rows fail the amplitude control | hypothesis as stated (the universal reading) | FAIL on both real carriers; existential reading untested | timing set by the domain's dynamics; arc = chord = amplitude on monotone occasions (P1) | arc-regularity *beyond amplitude* through S > 0 compensation on multi-hump occasions; stick-slip | which real systems have S > 0 compensation; a pre-decided event and segmentation rule; a multi-dimensional Fisher carrier; stick-slip | that H-L5 holds for measles or the pulse; threshold-system arc-regularity as CRR evidence; p4581 |
| **L-T1** | forgetting tracks the Fisher path, not the endpoint (`CRR.md:242-250`) | per-step Σ√(2KL) on probes; MLP regression, lr controlled, held-out R² | ARC-T1 (seen, lr-confounded; beaten by E_old 0.99351) | T1X2-1/2 FAIL 5/5, not fragile; path also behind E_new and EWC distance 5/5 ([D4]) | hypothesis as stated, one learner class | FAIL (held-out, weakly anchored) | loss-based forgetting is an endpoint function; the per-step path is mini-batch noise (S/C* 72–275) | a refinement-convergent path; forecasting forgetting before the endpoint exists; LM-class learners | those three | that path length predicts forgetting better than an endpoint |
| **L-EQ** | equanimity: settled past and present exert equal pull, Ω = 1 (`CRR.md:166-177`) | Fisher/Euclidean gradient-norm ratio (EMA 0.9, cap) on replay, EWC penalty, EQ-B clip, exact-posterior comparison, KD weight; Kalman; drifting-units synthetic worlds | EQ2-1b PASS-0 (fragile; replication failed); 5 of 9 load-bearing carriers ahead, 4 on one digit set ([D6]) | EQX-1 REDUCES, EQX-3 FAIL; SOTA1-2 FAIL (−2.94, strongly anchored); EQ3-1, EQ4-1r FAIL; Ω a plateau | hypothesis as stated (same-units replay; KD); the equal-*magnitude* reading analytically | REDUCES / FAIL; best rows PASS-0 at most | MGDA / VQGAN / GradNorm α = 0; the Bayes count weight; Riccati | an equanimity that *selects* a trade-off (equal precision, never chosen); per-task normalisation + P3 age weights (never declared) | decide which equanimity first; the drifting-units regime on real carriers; the knife edge as a plasticity diagnostic | that Ω = 1 is optimal, Bayes-optimal or a threshold; that the rule is new; that EQ2-1b/EQ3-I/EQ4-I are findings |
| **L-CUT** | the cut: an empty, oriented antipode of an intrinsic phase; own events sit there, not at the extremum (`CRR.md:101-131`) | Hilbert-phase antipodes; H-CUT diagnostics (CARD-3, MEAS2-3); δ(Now) rupture CUSUM; content-bearing resets; G-CD3 | G-CD3 synthetic gate OPEN | no real-data H-CUT test; Rupture gate CLOSED (PC1 behind peak; T5 190.297×); PRED70 WRONG on 2 synthetic models | instrument / one operationalisation (no stated-hypothesis test) | NOT DECIDABLE until CRR.md fixes the phase | the domain's own trigger sets events; the Hilbert phase is non-causal and harmonic-sensitive | the antipode against the initiation adder (LIFE1) | decide the phase (own event / Poincaré / analytic); LIFE1 with a declared schema-only loader check; a rupture positive control where antipode and extremum disagree | that the antipode beats peak cuts; that δ(Now) detects ruptures; that any real system's events sit at the antipode |

**CRR-derived lineages**

| Lineage ID | Core CRR idea | Operationalisation(s) tried | Strongest supporting observation | Strongest negative evidence | Failure level | Current epistemic status | Mundane explanation | CRR-specific possibility | What Phoenix may explore | What Phoenix must never claim |
|---|---|---|---|---|---|---|---|---|---|---|
| **L-SURP** | surplus S = C − C* marks what regeneration weights (D4, P2; λ = 1 from the external spec) | replay reallocation ∝ e^{λS}; S in CUSUMs and diagnostics | S tracked forgetting, Spearman +0.83 (SAL positive control) | SAL-A: no λ helps on the world built in its favour | one operationalisation (R4) | GATE CLOSED; T5 never run | concave marginal value of replay under a fixed budget; P2 is Jaynes | S > 0 as the only home of a non-trivial H-L5 | T5 (measured influence); where S > 0 occasions exist in real carriers | that surplus-weighted replay helps; that S orders dissipation |
| **L-RLAW** | CRR 2.0: memory depth α* = K(v_own), zero parameters (O1 route 1) | local-level v from input drift; five unseen domains | RLAW-4DT tracking 0.523 (FRAGILE) | RLAW-U 0/5; RLAW-C FAIL (0/112); the constant beats the law everywhere; none fragile | the added law (not a CRR.md claim: "no retention law is claimed") | FAIL, strongly anchored; outside the ladder by the owner's instruction | memory is a domain trait (diffusivity, sluggishness) | memory derived from the system's *own* state model (O1 proper, never derived) | O1 derivations on now-SEEN RLAW data, exploratory | that the law holds anywhere; that the ladder's FAIL count includes RLAW |
| **L-CLK** | index learning by own change, not steps (the slogan at `CRR.md:196`, not H-L5) | FOREVER swaps; own-clock stopping; arc-clocked Adam (C1); arc-triggered consolidation (C3); own-clock slow model (SOTA1) | C3 firings near hidden switches (confounded); C1 S1 timing effect (beaten by MECTA-M) | SOTA1-3:crr-stepclock FAIL (TIE, held-out); OB1-C1 G-TIME S2 FAIL; clock gate CLOSED; clock_cut = Wald | one operationalisation each | FAIL / GATE CLOSED; C2 never run | Wald's SPRT; Ebbinghaus; Čencov; decay distribution as a hyperparameter | the arc as a change detector with a constant-rate null | consolidation timing in a stream where consolidation matters; C1 with a β-retuned STEP control; SOTA1's arm with λ swept | that ARC detects boundaries; that FOREVER supports CRR; that own-clock rules beat step clocks |
| **L-PAUSE** | the empty cut: zero content, zero stake, on the agent's own clock (A3 + A1′ + A6; Proposition 7 lives in AI_Safety, not CRR.md) | ring MDP valuations; lossless own-step pause in learners (SCL1–3, SOTA1-C); NT1 vs DReST; STAKE1 (LLMs); EPS/DR1/Attention transpositions | constructions hold bitwise (SCL1-1, SCL2-1, SCL3-C, SOTA1-C1..C3) | STAKE1-A: the models could not act as agents (no agent-level test); Attention: EMPTY behind TRUE on welfare 28/32; A4b drift-seeking; "A3 = indifference" cost the task | transposition only (CRR.md states no safety claim) | construction (C) + untested prediction (E) | a Bellman identity; checkpoint/resume; utility indifference; POST/DReST | H-C vs H-S vs H-A on a capable agent; necessity (zero stake with nonzero content) | STAKE1 on a capable model; a head-to-head with indifference, safe interruptibility and DReST; the reasoned-pause band; Maps P5 re-declared | that constructions are CRR evidence; that SCL1-2/3 and SCL2-2/2s/3 are passes about agents; novelty of the own-clock pause; that ETM improves welfare; that A3 entails the natural-time design |
| **L-MEM** | settled content regenerated without stored examples (A3/A6 transposed; the owner's "first object") | input-space Gaussian replay (IGR); anchor-referenced transport (RRM-1/A); HopDC-type transport in a coupled learner | IGR within 0.4013 of JOINT on POS; kept-anchor transport positive on 4/4 SEEN drift-to-fix carriers ([D7], post hoc) | RQM-A (criterion cannot fail); RRM2-T1..T3 (no drift); CPL1-A (current-task anchors hurt) | instrument / one operationalisation | GATE CLOSED ×8 | GMR/DGR; HopDC / SLDC / transport keys; iCaRL/SDC | none identified (the record grades the reading RESTATES) | kept-anchor transport in a learner with real drift; anchor provenance as a variable; GMR at a fixed realistic budget | that CRR found or predicted these methods; that "the HopDC finding" is this repository's |
| **L-RETRO** | CRR as a synthesis that lands where domains are known, and sometimes adds | batteries (197 rows), SYNTHESIS (164), PRED70 (70, declared first), labs, FRONTIER | hit rate 69 of 97 (0.7113) where checkable | SHARP 0 of 197; framework flow 0 of 109; ADDS 0 clean after literature; PRED70 Q held 35, failed 33 | coverage, not prediction; R4 on H-L5/H-CUT in synthetic models | R1–R3 (R3 unreviewed: 0 named experts) | a correct non-generative grammar lands REDUNDANT by construction | the bounded-memory threshold shift as a cross-domain map; L01; 7 PRED70 A6 candidates | a decoy-framework base rate; literature check of the 7 candidates; the bank as a translation atlas | that 0.7113 is predictive; that ADDS rows are novel; that REDUNDANT means right (15 PRED70 REDUNDANT rows failed Q, [D3]); pooled denominators |
| **L-ONT** | a process ontology: occasions, empty cut, regenerating past, empty future (A1–A8) | the instrument's readings of A1′, A3, A6; tense, self-model and off-switch tests | Poincaré section within 1 sample of the registered cuts, with no future (`ontology/01_the_cut.md:55-56`) | the registered cut reads the future (instrument); only C6 reached held-out data | instrument (tense); E for C1–C2 | v3.1 frozen since 2026-09-17; v3.2 undecided | Čencov; exponential kernels; information geometry + MaxEnt | none tested beyond C6 | decide v3.2 first; implement the causal section and gate_TENSE; re-read H-L5 rows under it | that the ontology is tested beyond C6; that the tense finding refutes A8 as ontology; kinships as evidence |

**Non-CRR lineages kept for their history**

| Lineage ID | Core CRR idea | Operationalisation(s) tried | Strongest supporting observation | Strongest negative evidence | Failure level | Current epistemic status | Mundane explanation | CRR-specific possibility | What Phoenix may explore | What Phoenix must never claim |
|---|---|---|---|---|---|---|---|---|---|---|
| **L-SEC** | *none*: the Laplace weight with a secant units calibration (+ AR1 clip); it grew out of H-EQ's R7 baseline; A1′ "names" it in hindsight | SEC1 (seen), SCL3, SEC3, SEC4 (clip), SEC5, SEC6, SEC6R; P1 mechanism runs | SEC4-1 PASS-1 (6/6) as scored; SCL3-3 PASS-0 with its post hoc gate OPEN (by one carrier) | SEC4-1-G CLOSED (frozen learner 5/6); SEC5-1 FAIL (not fragile); SEC6R-B FAIL (AR1-B, SI-1C 8/9 vs 7/9); SEC6R-2 FAIL; FM6 24/30 | the method on class-IL tabular streams; the passes at instrument level | PASS-1 as scored + UNINFORMATIVE by the later gate; no PASS-2 | Laplace + Barzilai–Borwein secant + AR1; lenient class-IL criterion | none (F11: 0 of 7 operational clauses) | the calibration on a criterion a frozen learner fails; a pre-declared per-carrier informativeness rule; AR1-B and SI-1C as baselines | that SEC is CRR evidence or tuning-free; SEC4-1 without SEC4-1-G; any compute/energy/CO₂ saving |
| **L-APP** | CRR as a source of applied savings and designs | compute/energy estimates; APP1; P7 suite; ROB1 | SCL3 9/10 at 0.0588 of the sweep's compute (`Compute_Savings`) | CRR's part load-bearing in 0 of 17 suite rows; the GLOBAL_ESTIMATE premise "not currently support[ed]"; ROB1 candidates REDUNDANT | applied premise (rests on L-SEC's criterion) | notes with addenda; Energy CONSOLIDATED lacks one (§13) | known methods (SEC, checkpointing, Wald) | none shown | a tuning-cost study with a criterion that can fail, framed as engineering | any saving attributable to CRR; the Alexander Plan's figures as forecasts |

---

## 11. Final question: appropriately adversarial, excessively suppressive, or a mixture?

**A mixture, with each part located in the workflow.** The evidence is §8 and PROCESS §7.

**What was appropriately adversarial, and should remain merciless:**
1. **Numbers from scripts (R1) and the append-only ledger (R8).** Every reader could trace every verdict. No verdict needed
   reconstruction, and post hoc weakening was added as rows (SEC4-1-G), never as edits.
2. **Hash before data, strong anchoring and frozen copies (R2).** Three VOID studies cost carriers, and the rule never allowed
   a quiet rescue. Keep it.
3. **Score as committed, per unit, with sensitivity tables (R5, R6).** The held-out FAILs that carry the record's real
   information are robust because of this: MEAS2-1, CARD-1, T1X2-1, SOTA1-1a, SEC5-1, RLAW.
4. **Baselines that can win, and reduction to a constant reported as such (R7).** This is where most "successes" were
   correctly deflated: EQX-1 REDUCES, SPA1 KNOWN, Wald, GMR, HopDC.
5. **A pass on held-out data only, never on the day a rule was learned (R3, R11).** It did its job. Note that it sets no
   minimum interval (SEC3: 17.5 minutes across midnight).
6. **The prompt and decision logs (R13, R14).** They made this audit possible, including the record of where the owner pushed
   toward a pass and how the agent answered.
7. **Separate denominators, the ladder, and "construction ≠ evidence".** These stopped the retrodictive banks and the pause
   constructions from being counted as confirmation.
8. **The instrument gate on the success criterion (SEC6-G).** It arrived late. It should become merciless *earlier*: every
   "not behind" or "matches" criterion needs a must-fail control declared before any hash. Embers' two devices
   (§9.4) belong here too:
   - decidability settled on training units before held-out units are opened;
   - a pre-data blame table stating which conjunct a FAIL refutes.

**What was too final too early, and should move into an explicitly exploratory environment.** "Exploratory" here means
recorded and committed, with outputs labelled exploratory. It is never quotable as evidence, and it ends in a frozen gate.
1. **First-run synthetic Phase-A gates on a new operationalisation.**
   - Today a design-defect closure receives the same finality as a held-out FAIL: SAL, Rupture, Cut_Content, OB1-C3, RQM,
     RRM2, Maps P5.
   - In an exploratory stage, the gate's *own* preconditions are developed in a logged loop until the gate is well-formed:
     headroom, "does the action matter", "can the criterion fail", and a positive control that tests the scored property.
     Then the gate is frozen, and only the frozen gate's verdict counts.
2. **Pilot and headroom checks on SEEN or synthetic data.** Does the learner drift? Does consolidation matter? Can the
   criterion fail? Can the loader read the family's format (STRING targets)? Can the model act as an agent? Each of these was
   discovered by a gate or a held-out run. Each is a pilot question.
3. **Theory formulation.** Before a confirmatory test of an ambiguous principle, decide the reading in the theory text: which
   equanimity, which intrinsic phase, which event rule, which segmentation, A6's scope. An exploratory environment can map the
   candidate readings side by side, as SAL's three untried translations and H-EQ's four "1"s should have been. The protocol
   should forbid confirmatory hashing of a hypothesis whose reading is on an open decision list (`SPEC_RECONCILIATION.md:79`;
   `ontology/05_next_steps.md` §2).
4. **Schema-level data checks.** Reading a file's header or attribute types under a declared, hashed loader check should not
   count as opening the data. The LIFE1 block (AL 162) shows the current reading can stop the only runnable test of a
   hypothesis.
5. **Literature checks before declaration, not after.** ADDS dissolved within a day of its check. RQM and RRM were designed
   before their prior art was found. OB1 then changed the order (AL 201), and the change should be kept.
6. **Off-repository playgrounds and scratchpads become committed exploratory logs.** SEC came from scratchpad work "not in the
   repository" (`prereg/sec1/PREREG.md:54`). AL 3's playground numbers stay off the record. Under that arrangement maturity
   cannot be audited, and the audit cannot tell whether a quick hash was premature or well prepared.

**What was too loose, and should become stricter.** This is the other half of the mixture.
1. **Tempo from request to hash.** Fifteen of twenty studies were hashed within 25 minutes of the logged request
   ([D8]). A minimum maturity checklist should apply before any hash:
   - frozen-runner smoke on every arm;
   - a loader validated on the target format;
   - a must-fail control on the criterion;
   - shown headroom;
   - the theory reading decided.
2. **Applied extrapolation from PASS-0 or single-family PASS-1 rows.** GLOBAL_ESTIMATE, Energy CONSOLIDATED and the Alexander
   Plan valued results that had not replicated. Only PASS-2 may leave the ledger (CLAUDE.md §7). Valuation notes should be
   held to the same rule.
3. **Confirmatory tests of observations seen once.** SCL2 was hashed about 15 minutes after the request, on an unexplored
   observation. Such observations belong in the exploratory stage first.

**The principle behind the split.** The request asks that "things are killed for the right reason, at the right level of
abstraction, and only after they have been formulated well enough to deserve the test".
- Ashes killed for the right reason at the held-out layer.
- It mostly stated the level correctly. The notes find a few compressions: SAL's "no positive control", OB1's unscoped
  "H-T1 failed", and CRR.md's "H-EQ is retired as an adaptive rule".
- It did not reliably wait until a hypothesis was formulated well enough. The fix is not to weaken the held-out layer. It is to
  give formulation and gate design their own recorded stage, and to stop treating the first draft of a gate as the gate.

---

## 12. The auditor's declared expectations, checked

The expectations were declared at 37d333a, before any reading.

1. **"Most held-out FAILs will reach one operationalisation, not a CRR principle; a minority will reach the stated hypotheses
   directly (H-L5 on real carriers; H-T1 against the old-probe endpoint)."** Held, with two corrections.
   - H-EQ also failed at the level of the hypothesis as written (EQX-1/3, SOTA1-2). The expectation omitted it.
   - H-T1's failure does not depend on the old-probe endpoint: E_new and the EWC distance also win ([D4]).
   - Of the 36 held-out FAIL rows (`outcome_classes.txt` [7]), the stated-hypothesis rows are EQX 2, MEAS2 2, CARD 2, T1X2 2
     and SOTA1-2. The rest reach EQ operationalisations outside H-EQ's domain, the SOTA1 design and components, the SCL1
     observation, or SEC, which is not CRR.
2. **"Several 'successes' will reduce to known mathematics."** Held, more strongly than expected: every success reduced (§4
   Q8).
3. **"Instrument and identifiability failures will be a substantial share of the non-PASS outcomes since 2026-09-25."** Held.
   16 of the 21 held-out VOID / NOT DECIDABLE / UNINFORMATIVE rows belong to studies first scored on or after 2026-09-25
   ([D11]). The expectation did not foresee two things:
   - none of those touched a held-out FAIL's wording (`outcome_classes.txt` [5]);
   - the largest instrument failure, the SEC criterion, sat inside *passes*.
4. **"The retrodictive record will mainly establish expressive coverage, not unique prediction."** Held (§7).
5. **"The answer to the closing question will be a mixture."** Held. What the expectation did not foresee is that the
   suppressive part sits mostly *before* the held-out layer:
   - in Phase-A finality;
   - in skipped theory decisions;
   - in one R2 interpretation (LIFE1).

   It also did not foresee that the record shows an equally important *too-loose* part: tempo and applied extrapolation.

---

## 13. Record-keeping discrepancies found (recorded, not fixed; the owner decides)

No historical file was edited to resolve any of these.

1. **The CLAUDE.md / CRR.md Poincaré claim.**
   - `CLAUDE.md` §3.1 item 2 and `ontology/01_the_cut.md:55` say the Poincaré section is named in `theory/CRR.md` as an
     alternative intrinsic phase. AGENT_LOG 53 calls it "CRR.md's named Poincare-section alternative".
   - A search of `theory/CRR.md` finds no "Poincar". The alternative is named in `CLAUDE.md` and `src/crr/instrument/core.py:91`.
2. **SEC3's hash date.** AGENT_LOG 167 (4) says SEC3's hash follows "on 2026-09-28". The ledger's SEC3-0 cell and commit
   916d3d4 give 2026-09-27T23:42:45Z.
3. **Synthetic rows printed as "seen".** `Epistemic_Review/checks/ladder.py` prints the purely synthetic Phase-A rows (RQM-A,
   RRM-PA, OB1-C1-A, OB1-C3-A, and others) as "seen", because the dataset cell contains "(N)". SAL-A and STAKE1-A print as
   "synthetic". A labelling inconsistency; no verdict changes.
4. **Forced passes in the R5 count.** The ladder's R5 count of 13 passes on seen data includes SCL1-2 and SCL1-3. Their held-out
   twins (SCL2-2/2s/3) are allocated "forced by the construction (not R6)". AGENT_LOG 105 (a) records why they keep R5.
5. **RLAW outside the ladder.** The ladder's held-out FAIL count omits the 8 RLAW FAIL rows by the owner's instruction ([D2]).
6. **A gloss in `redundant_vs_fail.txt`.** It glosses PRED70's 35 REDUNDANT rows as "consistent but not risky". 15 of them have
   Q failing ([D3]).
7. **Missing premise addendum.** `Energy Design Principle/CONSOLIDATED.md:83` attributes "0.47 TWh … to the CRR programme, all
   of it through SEC". It has no premise addendum, while four other notes received one (AGENT_LOG 239). `Alexander Plan/` has
   no SEC4/SEC5 addendum.
8. **Stale CRR.md status lines.**
   - `theory/CRR.md:227` still says H-L5 is "Untested elsewhere" after MEAS2; CARD has since failed.
   - `theory/CRR.md:181-182` still reads "H-EQ is retired as an adaptive rule". That is broader than its replay-only evidence,
     and later rows qualified it.
   - `theory/CRR.md:190` cites "A9", which CRR.md does not define.
9. **Shared records not applied back.** The shared-records rule (mfeat, AGENT_LOG 106) was not applied back to EQ3. Two of
   EQ3-1's not-behind carriers share records with EQ2/EQ2R carriers (L-EQ §4 Q9).
10. **A compressed ledger phrase.** SAL-A's "no positive control exists for this operationalisation" (ledger; CLAUDE.md §3.3)
    is narrower than the gate's own reading (`prereg/sal/PHASE_A.md:39-46`): the instrument saw S, and the effect was absent.
