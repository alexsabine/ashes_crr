# Reader notes: L-L5, L-T1, L-CUT, L-SURP (the stated hypotheses, and the cut/surplus ideas)

PRE-PHOENIX INTERPRETIVE AUDIT. NO VERDICTS ALTERED. These are a reader's notes, not evidence (R8). Every number is copied
verbatim from the cited file:line or ledger row. A count or difference the reader derived is marked **auditor's count
(derived)** or **auditor's reading**, and the method is stated. Line numbers refer to the files as they stand at the time of
reading (2026-10-02).

Which of these lineages are hypotheses `theory/CRR.md` itself states. Section 9 of `theory/CRR.md` (lines 306-315) lists
exactly four falsifiable claims: H-CUT, H-L5, H-T1 and H-EQ. "Everything else in this document is definition, standard
mathematics, or open" (`theory/CRR.md:315`). So:
- **L-L5 (H-L5) and L-T1 (H-T1)** are stated hypotheses. Negative evidence on them can reach the hypothesis as stated.
- **L-CUT** mixes three things: the axiom A3 (`theory/CRR.md:101-111`); the stated hypothesis H-CUT (`:123-131`); and
  uses of the cut that CRR.md does not state (a change detector, plasticity resets).
- **L-SURP** is mostly not a hypothesis. D4 is a definition (`:93-95`). P2 is "Standard (Jaynes). CRR does not fix β"
  (`:155-157`). O2 is open (`:162-164`). The law π ∝ e^{λS} with λ = 1 came from the external specification
  (`prereg/sal/PHASE_A.md:10-12`), not from CRR.md v3.1.

---

## L-L5: H-L5, "change has its own clock"

### Trajectory (dated, cited)

| date | event | source |
|---|---|---|
| before 2026-09-15 | Motivating result: arc beats clock at 11/12 stress levels on Marone p4581. It was withdrawn by the September audit and may be held as "context, not evidence" only. | CLAUDE.md §0 ("L5 (p4581 stick-slip)"); `data/SEEN.md:18` |
| 2026-09-15 | CRR.md v3/v3.1 states H-L5. It has three controls: (i) amplitude, (ii) identity metric, (iii) peak-detected boundaries. It is framed as "an empirical claim about which class a real system belongs to". | `theory/CRR.md:200-219` |
| 2026-09-15 | SCOPE domain review. Stick-slip and cardiac are "Tier 1 (planned L5x)". Measles is "Tier 2", planned on the "(S, I, R) fractions on the simplex", "native (P7)". | `theory/SCOPE.md:119,121,132-137` |
| 2026-09-15T21:11Z | Owner asks for the measles run. | `notebook/PROMPT_LOG.md:100-113` (entry 7) |
| 2026-09-15, same hour | Built: the instrument extension, the S-P rate battery and gate_L5R (GATE OPEN). MEAS was preregistered, then VOID by its format rule (loader read 0 series). MEAS2 was hashed at 21:26Z, run and reported. | ledger MEAS-1..3, MEAS2-1..3; `prereg/meas2/PREREG.md:3,7-22` |
| 2026-09-15T21:40Z → 21:46Z | "Okay, run on cardiac". The CARD prereg was written 6 minutes later. PhysioNet returned 403, so CARD was hashed and not run. | `notebook/PROMPT_LOG.md:121-134`; `prereg/card/PREREG.md:3-18` |
| 2026-09-15 ~22:25Z | PR #15 adopted: the amplitude control is scored by paired bootstrap. "leaves MEAS2 at 0/17 either way". | `notebook/PROMPT_LOG.md:149-155,167-180` |
| 2026-09-17 | Bio battery. The forced-SIR row showed that the event rule decides the class (AGENT_LOG 15). The reset-jump segmentation bias was found and `segment_end` was added (AGENT_LOG 18). | `notebook/AGENT_LOG.md:27,30`; `theory/retrodictions/README.md:181-206` |
| 2026-09-17 → 09-21 | Synthesis batches. H-L5 rows repeatedly found "the arc is the amplitude" on monotone occasions (e.g. batch 17, 18, 19 readings). The class-map conclusion: "The arc-regular class needs a fixed chord *and* a fixed reset". | `theory/retrodictions/README.md:473,483-485`; `theory/retrodictions/synthesis_batches/batch_17.txt:77`, `batch_19.txt:68,77` |
| 2026-09-17 | Note for Daniel: H-L5 "needs a carrier that is arc-regular by its own physics … stick-slip … or it is retired". | `docs/notes/2026-09-17_note_for_daniel.md:86-91` |
| 2026-09-26 | Life_Sciences CD-1: on cell size (adder, sizer, timer) "control (i) can never be beaten … H-L5 is empty here". | `Life_Sciences/LIFE_SCIENCES.md:26,55-68` |
| 2026-09-26/27 | Lab L03 runs CARD as committed. Investigator's forecast, written before the data: "CARD-1 FAIL". | `labs/L03_pulse/LAB.md:30-32`; AGENT_LOG 164-165 (`notebook/AGENT_LOG.md:177-178`) |
| 2026-09-29 | PRED70: 7 H-L5 ADDS rows. "None of them survives H-L5's own amplitude control" (post hoc). | `Predictions70/PREDICTIONS70.md:43-56`; `Predictions70/checks/tally.txt:81-82` |
| never | L5x on stick-slip (Marone experiments ≠ p4581) was never preregistered or fetched. There is no fetch script in `data/`. | `ls data/` (fetch scripts: autonomic_aging, cifar100, measles, openml, pmlb, rlaw) |

### Operationalisations and added assumptions

1. **The stated form.** `CV(C_m) < CV(Δt_m)`, beyond controls (i)-(iii), scored per unit with a paired bootstrap
   (`theory/CRR.md:204-209`).
2. **Measles (MEAS2).** Added assumptions:
   - **(a) The carrier is 1-D** reported biweekly cases under a Poisson transform y = 2√λ (`prereg/meas2/PREREG.md:40-45`).
     It is not the SIR simplex that SCOPE named (`theory/SCOPE.md:121`). The "Fisher-native" metric is therefore a concave
     reparametrisation of one count series.
   - **(b) "Own events" are threshold onsets** from a detector with four constants (`prereg/meas2/PREREG.md:47-52,91-96`).
     CRR.md supplies no event rule (O3, `theory/CRR.md:137-138`).
   - **(c) Control (i) is decisive and scored by CI.** It is the gate's "concavity trap" defence (`prereg/meas2/PREREG.md:62-67`).
   - **(d) ≥ 8 onsets**, so 3 cities were excluded.
3. **Cardiac (CARD).** Added assumptions:
   - **(a) Events are ECG R-peaks** (Pan–Tompkins), not the "pressure upstroke onset / arc from the dicrotic notch" of
     CLAUDE.md §4.
   - **(b) The identity metric.** "the Fisher metric plays no role in this study", so control (ii) is void
     (`prereg/card/PREREG.md:27-30`).
   - **(c) The arc is the BP (or ECG) total variation per R-R interval**, against the RR interval.
   - **(d) Control (i) is scored strictly**: the CI of (cv_arc − cv_amp) must lie below 0 (`runs/card/frozen/card_score.py:135`).
4. **Synthetic banks (PRED70, synthesis).** The declared Q was the bare inequality, which omitted control (i)
   (`Predictions70/PREDICTIONS70.md:50-51`, "That is the investigator's error in the declaration").

**Which added assumption later became the thing that failed (Q4).**
- On real data the bare inequality itself mostly failed:
  - MEAS2: 5/17 Poisson and 1/17 identity (MEAS2-1, MEAS2-2);
  - CARD BP: 8/29 (CARD-1).

  So the failure is not mainly an artefact of an added assumption.
- Control (i) is the assumption that defeats every "arc-regular" synthetic case. That covers 7/7 PRED70 ADDS rows
  (`Predictions70/checks/tally.txt:81`), the adder, sizer and timer worlds (CD-1), and the slider (PRED70 P02-1:
  CV(arc) = CV(amplitude) = 0.732026, and 0.499621 with the slip included; `Predictions70/batches/pred_02.txt:10`). It also
  defeats the ECG on real data, where the bare inequality held in 19/29 but only 5/29 passed (CARD-2).
- **Auditor's reading (structural).** By P1 (`theory/CRR.md:88-91`), on an occasion traversed monotonically at resolution σ
  the arc equals the chord, which equals the excursion. So control (i) can only be beaten when occasions carry surplus
  S > 0 whose arc compensates amplitude variation.
  - That is exactly the positive control the measles gate needed: "S-P FM two-hump compensating (arc constant, amplitude
    variable)" (`src/crr/surrogates/gate.py:75,332-334`; `prereg/meas2/gate_L5R.txt:9`).
  - So H-L5 "beyond control (i)" is in substance a claim about lived surplus (L-SURP). Where the arc is regular because a
    threshold fixes the chord, the result is "how ordinary the arc-regular class is when a threshold fixes the chord …
    the practice (mileage-based maintenance) predates the framework" (`theory/retrodictions/README.md:483-485`).
- **Auditor's reading (gate mismatch, CARD).** CARD's hashed gate (`prereg/card/gate_L5.txt:6,15`) has positive controls
  S-A′ and S-G2 with cv_amp equal to cv_arc at printed precision (0.000/0.000 and 0.001/0.001). It prints no amplitude CI.
  - The repository's own gate_L5R docstring says such a one-hump row "is not a positive control for 'beyond control (i)'"
    (`src/crr/surrogates/gate.py:332-334`).
  - The standing gate_L5 scores amplitude only as a veto (`gate.py:80-95,98-99`), but CARD scores it strictly
    (`card_score.py:135`).
  - So CARD's hashed gate showed that the instrument can see arc against clock. It did not show that it can see arc beyond
    amplitude on a one-hump trace.
  - This does not change CARD-1, where the bare inequality held in only 8/29. It bounds what CARD-2's failure (19/29 bare,
    5/29 strict) says.

### Results (verbatim, by row id)

- **MEAS-1..3.** "VOID (format rule, as pre-registered)"; "loader returned 0 series" (ledger).
- **MEAS2-1.** "0/17 cities pass (0.0000; binomial p 0.0000); plain cv_arc < cv_clock in 5/17; 3 cities excluded" →
  "**FAIL**; not fragile (0/26 sensitivity cells differ)".
- **MEAS2-2** (identity, control ii). "0/17 pass; plain inequality in 1/17" → "**FAIL**; not fragile (0/26)".
- **MEAS2-3** (control iii). "12/17 = 0.70588 (0.71)" against threshold 0.70 → "PASS on a control line only — a comparison of
  two boundary rules, not evidence for H-L5 (which fails on both)".
- **CARD-1** (BP). "1/29 records pass (0.034; binomial p 0.0000); plain cv_arc < cv_clock in 8/29; 1 excluded (0065, flat
  channel)" → "**FAIL**; not fragile (0/26 sensitivity cells differ)".
- **CARD-2** (ECG). "5/29 records pass (0.172; binomial p 0.0005); plain cv_arc < cv_clock in 19/29" → "**FAIL**; not fragile
  (0/26 sensitivity cells differ)".
- **CARD-3** (diagnostic, antipodal against peak cut). "5/28 records" → "report (no verdict registered; diagnostic)".
- **Context only, not ledger.**
  - Life_Sciences CD-1: "control (i) can never be beaten: **HOLDS** as predicted; H-L5 is empty here"
    (`Life_Sciences/LIFE_SCIENCES.md:26`).
  - PRED70: "H-L5 rows 16: section-9 FAIL 15, PASS 0, undetermined 1 (P06-3)" (`Epistemic_Review/checks/redundant_vs_fail.txt:39`).
  - Rows read as FALSIFIES at R4: P02-1 (slider), P08-4 (Red Queen), P11-3 (breathing), P12-4 (glacial)
    (`redundant_vs_fail.txt:15,22,27,30`).
  - Ladder per-commitment line: "H-L5 natural time 10 | 0 | 6 | 3 | 20 | 2 | 0 | 10 of 16 = 0.6250"
    (`Epistemic_Review/checks/ladder.txt:48`; R1 count 20, i.e. inherited).

### Four-layer table

| observation | (1) phenomenon | (2) CRR interpretation | (3) ordinary explanation | (4) what would distinguish |
|---|---|---|---|---|
| Measles, MEAS2-1/2 | Inter-onset clock CV 0.20–0.48 against arc CV 0.26–0.52 (Poisson). In Birmingham, Leeds and Dalton the arc is significantly *less* regular (`reports/meas2.md:26-30`). | Measles belongs to the clock-regular class (`theory/CRR.md:225-226`). | The textbook biennial oscillator: timing is set by susceptible build-up and seasonal forcing, and epidemic size varies. TSIR predicts timing (`prereg/meas2/PREREG.md:106-114`). | Nothing here separates the two. Both say clock-regular. The prior for measles was clock-regular (`reports/meas2.md:30-33`). |
| Cardiac, CARD-1/2 | The RR clock is regular. The BP arc per beat is less regular in 21/29 (auditor's count (derived): 29 − 8). In the ECG the bare arc beats RR in 19/29, but the QRS amplitude ties. | The pulse is clock-regular (`reports/card.md:50-52`). | Autonomic control of RR. The pressure excursion varies with breathing and vascular tone (`labs/L03_pulse/LAB.md:30-32`). ECG arc per beat ≈ a stereotyped waveform's total variation. | A carrier where the excursion varies but its arc does not. None was found. |
| PRED70's 7 H-L5 ADDS rows (HH, Morris-Lecar, Stuart-Landau, Lorenz, faucet, Dupont Ca, menstrual) | The bare CV(arc) < CV(clock) held. | "Change has its own clock" in excitable systems. | "Where a spike or cycle has a nearly fixed height, the arc per cycle is nearly fixed by arithmetic" (`Predictions70/PREDICTIONS70.md:54-55`). An all-or-none, stereotyped amplitude. | Control (i) itself. It failed 7/7 (`tally.txt:81`). |
| Adder / threshold systems (CD-1, odometer, Tate drops) | Arc-regular with the clock irregular. | Arc is the system's clock. | The threshold fixes the chord. The arc equals the amplitude by P1. This is mileage-based maintenance and the adder (`theory/retrodictions/README.md:483-485`; `Life_Sciences/LIFE_SCIENCES.md:57-68`). | Only S > 0 compensation, as in the two-hump gate row, could separate them. |
| Slider P02-1 | The class flips with segmentation: slip excluded, CI includes 0; slip included, "arc-regular (CI below 0)". | A slip is the cut (A3: no content). | A constant jump at each event lowers CV(arc) by arithmetic (AGENT_LOG 18; `ontology/06_cut_as_content.md` R4). | A pre-registered segmentation rule. v3.2 item 7 proposes `segment_end="exclusive"` (`ontology/05_next_steps.md` §2 item 7), but it was not adopted into CRR.md. |
| MEAS2-3 (12/17, at the 0.70 threshold) | Onset-bounded arc is more regular than peak-bounded arc. | Own events are better boundaries than extrema. | `find_peaks` on Poisson-noisy counts segments inconsistently. gate_A3 shows such comparisons pass on surrogates with no CRR content (`prereg/card/PREREG.md:45-54`). | An H-CUT test on own events with its own gate. It was never built. |

### Salvage classification

- **A (genuine falsification pressure), on the hypothesis as stated.**
  - **Core principle.** "This is the shape of test CRR is built for: a CRR quantity against a clock"
    (`theory/CRR.md:198`).
  - **→ Operationalisation.** H-L5 (`:200-209`).
  - **→ Tests.** MEAS2 on a 1-D Poisson count carrier with detector onsets; CARD on BP and ECG total variation per R-R
    interval, identity metric.
  - **→ Failure.** 0/17; 1/29 and 5/29; not fragile.
  - **Highest level reached.** H-L5 *as a universal claim over systems with own events*: CRR.md names "beats of a heart" in
    the hypothesis (`:200`), and the pulse failed. It also reaches the claim that measles and the pulse are in the
    arc-regular class.
  - **What it does not reach.** It does not reach the existential reading CRR.md also gives ("an empirical claim about which
    class a real system belongs to", `:216-217`). On that reading, two clock-regular assignments leave open whether any real
    system is arc-regular beyond control (i). The class named as the candidate (stick-slip, threshold with variable charging
    rate) was never tested on real data.
  - It does not reach the Fisher metric (A1) either way. Control (ii) did not change a verdict in MEAS2
    (`reports/meas2.md:35-37`) and was void in CARD.
- **B (operationalisation).**
  - Measles was tested on a 1-D Poisson transform of cases, not on the SIR simplex SCOPE planned (`theory/SCOPE.md:121`).
    So the "first Fisher-native carrier" claim (`theory/CRR.md:220-222`) is native only in the 1-D sense, where the arc is a
    reparametrised total variation (SCOPE §7 item 2, `theory/SCOPE.md:261-263`).
  - CARD deviated from CLAUDE.md §4's pressure-onset / dicrotic-notch boundary.

  Neither changes the verdicts' direction, because the bare inequality failed too. But the multi-dimensional Fisher arc,
  where A1 could matter, was never tested in a real H-L5 study.
- **C (reduction).** The bare "arc-regular" result reduces in every synthetic case on the record to "the threshold fixes the
  chord", which is the amplitude (P1). Examples: CD-1, PRED70's 7, and the README class map. This is not CRR evidence.

  Useful by-product: a clear statement that H-L5's non-trivial content must live in S > 0.
- **D (instrument).**
  - MEAS VOID (loader).
  - CARD's 12-day delay (PhysioNet 403; `prereg/card/PREREG.md:13-18`).
  - Three CARD BP channels with ρ 670.9, 619.6 and 316.9 and a fast oscillation dominating the analytic phase, kept under R6
    (`reports/card.md:40-46`).
  - The CARD gate mismatch described above.

  None reverses a verdict.
- **E (identifiability).**
  - "The event rule, which the framework does not supply (v3.1 O3), decides the class" (`theory/retrodictions/README.md:204-207`;
    AGENT_LOG 15).
  - Whether a reset jump is arc or cut decides the class on threshold-reset carriers (AGENT_LOG 18; P02-1).
  - Needed: a CRR.md v3.2 decision on the event rule and on segmentation, fixed before any data (`ontology/05_next_steps.md`
    §2 items 3 and 7).
- **F (near-win).**
  - Weak. The ECG bare inequality held in 19/29 (CARD-2), but the ordinary explanation (QRS stereotypy) is the obvious one.
  - MEAS2-3 at 12/17 against a 0.70 threshold is a control line with a known noise explanation.
  - Neither is a candidate phenomenon in the request's sense.
- **G.** None.

### Extinguished-lead check

- **No verdict was overstated.** "H-L5 fails on its second real carrier" (`reports/card.md:22`) and "false for this system
  under this carrier and metric" (`reports/card.md:50-52`) are scoped correctly.
- **The existential lead was never tested, rather than killed.** Both real carriers were ones where a domain expert (and,
  for CARD, the investigator in writing) expected clock-regularity:
  - `reports/meas2.md:30-33`, "the textbook biennial oscillator";
  - `labs/L03_pulse/LAB.md:30`.

  The Tier-1 candidate expected to be arc-regular (stick-slip) never ran. `reports/meas2.md:66-68` says so explicitly:
  "H-L5 on carriers with genuinely arc-regular events (stick-slip, cardiac — the planned L5x), which this result does not
  touch."
- **One transfer of prior.** OB1 uses MEAS2/CARD/T1X2 to set a low prior for "index by own change" in learners
  (`Open_Bottlenecks/CRR_READING.md:14-21`). It notes in the same place: "That is a different use from H-L5's regularity
  claim." This is not a kill, but a regularity failure was carried into a different use as a prior.
- **CRR.md was not updated after CARD.** It still says "Untested elsewhere" after MEAS2 (`theory/CRR.md:227`).

### Question-10 evidence (L-L5)

- **Time from request to confirmatory test.**
  - Measles: under an hour, from 21:11Z to the MEAS2 hash at 21:26Z (`notebook/PROMPT_LOG.md:100-113`;
    `prereg/meas2/PREREG.md:3`).
  - Cardiac: request to hash in 6 minutes (21:40Z → 21:46Z).
  - No exploratory phase on any real carrier preceded either. The only prior exploratory result (p4581) was ruled
    inadmissible (CLAUDE.md §0).
- **The conceptual clarification came after both preregs were hashed.** Two results arrived 2026-09-17 → 09-21 (AGENT_LOG
  15 and 18; synthesis batches; README class map):
  - H-L5 beyond control (i) needs S > 0;
  - the event rule and the jump segmentation decide the class.

  CARD then ran on 2026-09-27 as frozen on 2026-09-15. A fresh prereg on the same records was rejected as "rule-shopping"
  (AGENT_LOG 164, `notebook/AGENT_LOG.md:177`).
  - The protocol worked as designed here, preventing rule-shopping.
  - Its cost is that the second real-data test of H-L5 used an operationalisation chosen before the repository understood
    where H-L5's content lies.
- **Carrier selection followed availability and metric nativeness** (`theory/SCOPE.md:132-137`), not prior plausibility of
  arc-regularity. The protocol did not cause this; the order of prompts did (`notebook/PROMPT_LOG.md:102,123`).
- **R12/R3 did not stop L5x on stick-slip.** No record shows it was attempted. The roadmap left it "agent (data download
  blocked for PhysioNet; owner upload)" (`docs/ROADMAP_2026-Q4.md:129`).

### Open questions for Phoenix (L-L5)

- **May explore** (explicitly exploratory, on SEEN or synthetic data first):
  - Which real systems have multi-hump occasions where the arc stays regular while the amplitude varies (S > 0
    compensation)? This is the only form in which H-L5 can beat control (i).
  - A pre-decided event rule and segmentation rule (v3.2 items 3 and 7).
  - A multi-dimensional Fisher carrier (the SIR simplex with reconstructed susceptibles) where control (ii) has content.
  - Stick-slip at several normal stresses as the intended arc-regular class.
- **Must never claim:**
  - that H-L5 holds for measles or the cardiac pulse;
  - that the bare arc-regularity of excitable or threshold systems (PRED70's 7, the adder, faucet, geyser) is CRR evidence.
    It is the chord, by P1;
  - the p4581 result, or any arc-regularity claim that counts a reset jump inside the arc;
  - MEAS2-3 or CARD-3 as support for A3.

### Q1-9 summary (L-L5)

1. **Initial idea.** Change has its own clock (p4581 context).
2. **Operationalisation.** The CV of arc against clock, beyond three controls, on measles and cardiac.
3. **Added assumptions.** Detector events; 1-D carriers; identity metric on the pulse; control (i) scored by CI; ≥ 8 onsets.
4. **Assumption that failed.** On real data the bare inequality failed, so no single added assumption carried it. Control (i)
   decided every synthetic "arc-regular" case and CARD-2.
5. **Reached the claim.** MEAS2-1/2 and CARD-1/2 reach H-L5 as stated, for measles and the pulse. Together they falsify the
   universal reading.
6. **Reached only an implementation.** The 1-D Poisson carrier stands in for the SIR simplex, and CARD's events stand in for
   the CLAUDE.md §4 boundary.
7. **Interesting despite failing.** The structural fact that H-L5 beyond amplitude requires S > 0. The event-rule and
   segmentation sensitivity.
8. **Successes that reduced.** Every synthetic arc-regular case reduced to "the threshold fixes the chord".
9. **Infrastructure failures.** MEAS VOID (loader); the CARD 403 delay; CARD gate–rule mismatch (auditor's reading); three
   CARD BP channels with an anomalous analytic phase.

---

## L-T1: H-T1, path length against endpoint

### Trajectory

| date | event | source |
|---|---|---|
| before 2026-09-15 | Motivating result on a toy LM: R² 0.89 for the path against 0.76 for E_new, n = 20, confounded by learning rate. | CLAUDE.md §0 ("T1 (toy LM)") |
| 2026-09-14/15 | Recompute. ARC-T1: "PASS as pre-registered (seen, in-sample, lr not controlled)", C_new 0.88752, C_old 0.90058, E_new 0.75641. ARC-T1b: "R²(log F ~ log E_old) = 0.99351 → C − E = −0.093" → "FAIL: the old-probe endpoint predicts forgetting better than any path quantity". | ledger ARC-T1, ARC-T1b |
| 2026-09-15 | SCOPE lemma: on a linear model at its task-A optimum, "forgetting is exactly 2σ²·E_old … Path length can only lose to it". E_old made a required baseline. | `theory/SCOPE.md:143-169,258-262` |
| 2026-09-15 | v3.1 tightens H-T1 to "either probe" (owner approval). | `theory/CRR.md:242-250,321-327`; `notebook/PROMPT_LOG.md:167-180` |
| 2026-09-22 | T1x design iteration on synthetic smoke: precondition NOT DECIDABLE (path span 1.16×); schedules added; the per-step path definition kept. | AGENT_LOG 68 (`notebook/AGENT_LOG.md:81`) |
| 2026-09-22T16:23Z | T1x prereg pushed; data fetched 16:23:30Z; scorer crashed → VOID. | ledger T1X-VOID; AGENT_LOG 69 |
| 2026-09-22T16:40Z | T1x2 prereg (17 minutes later), four named corrections, data step held to 2026-09-23 (R3). | `prereg/t1x2/PREREG.md:1-31`; AGENT_LOG 70 |
| 2026-09-23T05:06Z | T1x2 data step and run. FAIL 5/5. | ledger T1X2-* |
| never | Models (a) byte-level LM, (b) GPT-2-small and (c) RL's Razor logs: "None is available in this environment (no GPU, no PyTorch, paper hosts blocked)". | `prereg/t1x2/PREREG.md:33-36` |

### Operationalisations and added assumptions

- **Path.** D6 as written (`theory/CRR.md:233-240`): C = Σ√(2·KL_gauss) between predictive means snapshotted every 5 steps
  (sensitivity at 10 and 20) on fixed probes (`prereg/t1x2/PREREG.md:49-53`).
- **The learner.** Model (d): a numpy MLP d-64-1 on PMLB regression, split by a median covariate (`:33-48`). Added
  assumptions:
  - forgetting means covariate-split fine-tuning on tabular regression;
  - learning rate is controlled as a log-lr covariate;
  - nine schedules vary the path at fixed lr, including noise injection, `restart` and training length.
- **The kept assumption that matters most (AGENT_LOG 68).**
  - The agent recorded: "the mini-batch dominance of the per-step path (C at snapshot interval 5 is about twice C at
    interval 10) kept as the instrument's own definition (path_length is per-step)".
  - The agent rejected: "changing the path definition to a coarse-grained one (the theory's D6 is per-step)".
  - The data show the size of the domination. On the old probe the S/C* medians are 222.195, 274.812, 86.158, 97.831 and
    71.936 (`runs/t1x2/score.txt:8,17,26,35,44`). The path is two orders of magnitude longer than the chord.
  - So the operationalised C mostly measures mini-batch wiggle. The A1′ unit ("the smallest change the system itself
    resolves", `theory/CRR.md:55-57`) is not applied in D6.

**Auditor's reading (comparator structure).**
- F is "task-1 test MSE after − before", and the old probe is "task-1 test rows" (at most 500)
  (`runs/t1x2/frozen/t1x2_score.py:13-15,151,171`). E_old is KL_gauss between the base and final predictive means on those
  rows.
- Algebra: ΔMSE = mean(Δμ²) + 2·mean(Δμ·(μ_old − y)). E_old = mean(Δμ²)/(2·var) with var = 1, so E_old is (up to a factor) a
  term of F's own definition on overlapping rows.
- More generally, F as measured is a function of the endpoint θ_T only. A path statistic can predict F only through its
  correlation with the endpoint. So the v3.1 "either probe" form of H-T1 is close to unwinnable on any learner where E_old is
  measured on the rows that define F.
- The gate's positive control S-H2 passes because it defines forgetting differently: F "additionally accumulates gamma *
  ||delta theta|| per step" (`src/crr/surrogates/battery.py:185-187,216-222`). That is a path term by fiat, with no
  loss-based analogue.

**But the failure does not depend on that.** The path also lost to the weaker comparators on every carrier.
- Held-out R² from `runs/t1x2/score.txt:9,18,27,36,45`:
  - best path 0.030, 0.352, −0.004, 0.001, 0.073;
  - E_new 0.085, 0.404, 0.217, 0.433, 0.756;
  - EWC distance 0.452, 0.490, 0.355, 0.390, 0.184.
- Path − E_new = −0.055, −0.052, −0.221, −0.432, −0.683. **Auditor's count (derived):** best path minus E_new, per carrier,
  from those lines; all ≤ −0.05.
- So the pre-v3.1 form (path against E_new) also fails 5/5 by the ±0.05 band, and the path loses to the parameter-space EWC
  distance on 5/5. **Auditor's count (derived)**, same lines.

### Results (verbatim)

- **ARC-T1.** "PASS as pre-registered (seen, in-sample, lr not controlled)". **ARC-T1b.** "FAIL: the old-probe endpoint predicts
  forgetting better than any path quantity, as the convex-learner lemma predicts".
- **T1X-VOID.** "**VOID**: a frozen script that cannot run or score the study as pre-registered voids it … the carriers are now
  SEEN". Cause: a binary split feature left task 2 empty, then a numpy bool reached json.dumps. On 218_house_8L a "165×
  extrapolation" carried non-finite path lengths into the fit (ledger; `reports/t1x.md:11-16`).
- **T1X2-0.** "DECIDABLE on 5/5" (smallest span 7.33× / 7.23× / 5.04× / 6.15× / 7.36×).
- **T1X2-1.** "**FAIL** (the old-probe endpoint predicts forgetting; the path does not beat it on any carrier; not fragile)".
  Path − endpoint "−0.663 / −0.153 / −0.628 / −0.685 / −0.743".
- **T1X2-2.** "**FAIL**". Spearman C_old "+0.349 / +0.582 / +0.003 / +0.118 / +0.112"; E_old "+0.915 / +0.983 / +0.948 / +0.946 /
  +0.970".
- **T1X2-3.** "holds (GATE OPEN)".
- **T1X2-S.** "0 flips in 45 cells" → "not fragile".
- **T1X2-D** (S against the residual of the E_old fit). "−0.029 / −0.522 / +0.485 / +0.659 / +0.132" → "report: high-S runs fall off
  the endpoint curve on feynman_II_36_38 and feynman_I_9_18 only".
- **T1X2-X.** "1 carrier excluded by rule 1 (1203_BNG_pwLinear …); 0 runs dropped".

### Four-layer table

| observation | (1) phenomenon | (2) CRR interpretation | (3) ordinary explanation | (4) distinguishing evidence |
|---|---|---|---|---|
| E_old dominates (T1X2-1/2, ARC-T1b) | Held-out R² 0.505–0.815 for E_old against ≤ 0.352 for the path. | Forgetting does not track the path on this learner. H-T1 "retires as tested" (`reports/t1x2.md:47-49`). | F is an endpoint function. E_old is close to F's own definition on the probe rows. The mainstream reading is "bound the old-probe endpoint" (`reports/t1x2.md:58-61`). | None needed for E_old. The informative comparison is path against E_new and EWC distance, and it was lost too (auditor's count above). |
| Path ≈ noise (S/C* 72–275) | The per-step arc is dominated by mini-batch wiggle; C roughly doubles when the snapshot interval halves (AGENT_LOG 68). | None stated. | The arc length of a noisy path does not converge under refinement. | A path coarse-grained at a resolvable step (A1′) against E_new. Never run: rejected as unfaithful to D6 (AGENT_LOG 68). |
| T1X2-D | High-S runs sit off the E_old fit on 2 carriers (+0.485, +0.659) and on the opposite side on 1 (−0.522). | Surplus carries path information the endpoint misses. | Sign-inconsistent across carriers; consistent with noise in a report-only diagnostic. | A pre-registered sign prediction across fresh carriers. Mixed signs make it a weak candidate. |
| ARC-T1 (path beats E_new, seen) | R² 0.88752 / 0.90058 against 0.75641. | The path beats the new-probe endpoint. | Learning-rate confound (lr not controlled). The old-probe endpoint reaches 0.99351 (ARC-T1b). | lr control. T1X2 did it, and the path lost to E_new there. |

### Salvage classification

- **A, at the level of the hypothesis as stated, for one learner class.**
  - **Core idea.** "Forgetting tracks the path, not the endpoint" (`theory/CRR.md:242`).
  - **→ Operationalisation.** D6 per-step √(2KL) sums against E on either probe, lr-controlled, held-out R² (`:242-250`).
  - **→ Test.** T1X2 (model (d), weak anchor).
  - **→ Failure.** 5/5, not fragile. The path also loses to E_new and to the EWC distance (auditor's count).
  - **Highest level reached.** H-T1 as stated in CRR.md, for small MLPs on tabular regression under covariate drift. It does
    not reach LM-scale fine-tuning (models (a)-(c) never ran), and it does not reach a resolution-coarse-grained path.
- **C, for the v3.1 comparator.** H-T1 v3.1 asks a path to beat a near-measurement of the outcome. That reduces the test to "is
  F an endpoint function", which it is by definition for loss-based forgetting (auditor's reading).

  Useful by-product: the theory's own E_old lemma (SCOPE §4.1) and the mainstream "bound the old-probe endpoint" reading.
- **D.** T1X-VOID: a binary split feature, a numpy bool, and non-finite paths. This is an instrument failure, not evidence.
- **E.** The theory leaves open whether D6's per-update arc should be measured at resolution σ. The record shows the
  per-step quantity is noise-dominated.

  Decidable with: a path estimator converged under refinement (or coarse-grained at A1′'s σ), fixed before the data, with
  E_new and EWC distance as the comparators that are not near-definitional.
- **F.** T1X2-D on 2/5 with a sign reversal on a third. Too weak to list as a candidate phenomenon. Recorded only.
- **G.** None.

### Extinguished-lead check

- `reports/t1x2.md:47` scopes the result properly: "H-T1 is retired as tested on this learner."
- OB1 restates it unscoped: "H-T1 failed (T1X2-1, 5/5 …)" (`Open_Bottlenecks/CRR_READING.md:18`). This is a mild loss of
  scope, used only as a prior.
- **Not extinguished:** H-T1 for LM-class models, and the coarse-grained path. These were never run because of infrastructure
  (no GPU, no PyTorch) and fidelity to D6. Neither was falsified.
- **Was it killed at too low a level?** No. The failure is broad within its learner class: the path lost to every endpoint
  comparator, not only to E_old.

### Question-10 evidence (L-T1)

- **About 7 days from v3.1 (2026-09-15) to the first held-out test (2026-09-22).** Synthetic iteration before the hash was
  allowed and used. AGENT_LOG 68 recorded schedule redesign, a divergence rule and a lowered lr grid.
- **The protocol did not suppress development.** Two things did:
  - the theory text (D6 per-step), which the agent declined to reinterpret;
  - infrastructure (no LM-class models).
- **The VOID cost a set of six unseen carriers.** The replacement was hashed 17 minutes after the T1x push
  (`prereg/t1x2/PREREG.md:3`; ledger T1X-VOID).
  - The R3 hold pushed the data step to the next day, as designed.
  - The fast turnaround did not reintroduce a defect: T1x2 ran cleanly, with 0 runs dropped.

### Open questions for Phoenix (L-T1)

- **May explore.**
  - A forgetting quantity that is not an endpoint function by construction. For example, *anticipating* forgetting from the
    new-probe path during training, before the old-probe endpoint exists. That is a forecasting form (A8 v3.1,
    `theory/CRR.md:294-302`).
  - A refinement-convergent path estimator.
  - LM-class learners.
- **Must never claim:**
  - that path length predicts forgetting better than an endpoint;
  - that ARC-T1 (seen, lr-confounded, beaten by E_old at 0.99351) is support;
  - that T1X2-D shows surplus carrying forgetting information.

### Q1-9 summary (L-T1)

1. **Initial idea.** Forgetting tracks the Fisher path.
2. **Operationalisation.** The D6 per-step √(2KL) sum against E_new, E_old and the EWC distance, lr-controlled, held-out R².
3. **Added assumptions.** Model (d) on tabular regression; a covariate split; the per-step snapshot; the noise and loop
   schedules; v3.1's "either probe".
4. **Assumption that failed.** The per-step path proved noise-dominated (S/C* 72–275). The E_old comparator is
   near-definitional. But the result does not rest on either, because E_new and EWC also win.
5. **Reached the claim.** T1X2-1/2 reach H-T1 as stated, for this learner class.
6. **Reached only an implementation.** None of the verdicts. The VOID was implementation only.
7. **Interesting despite failing.** T1X2-D, weakly. Also the noise domination of per-step arcs, which matters for any
   arc-based CRR quantity in SGD learners (it bears on L-CLK).
8. **Successes that reduced.** ARC-T1: "the path beat the wrong endpoint" (CLAUDE.md §0, ARC-T1b).
9. **Infrastructure failures.** T1X-VOID; models (a)-(c) unavailable.

---

## L-CUT: A3, H-CUT, the antipodal cut and its uses

### Trajectory

| date | event | source |
|---|---|---|
| 2026-09-15 | A3: the cut is the oriented antipode on an intrinsic phase. H-CUT: own events align with the antipode, not the extremum, where the two differ. The positive control is "an asymmetric multi-harmonic waveform". | `theory/CRR.md:101-131` |
| 2026-09-15 | gate_CUT: a testability gate (the antipode and extremum disagree on S-E but not on symmetric cycles). GATE OPEN. It does not score own events. | `runs/phaseA/gate_CUT.txt` |
| 2026-09-15 | gate_A3 (the L5x-3 comparison) passes on S-C λ = 1 and S-E, "jittered asymmetric waveforms with no CRR content", so it becomes a diagnostic. MUST_PASS is empty for A3. | `prereg/card/PREREG.md:45-54`; `src/crr/surrogates/gate.py:76`; `runs/phaseA/gate_A3.txt` |
| 2026-09-17 → 09-22 | Synthesis batch 07 row 3: under the oscillator's own phase-plane angle, "A3 is the peak cut for every 1-D trace and H-CUT is empty". The analytic phase is non-causal (batch 21 row 2: 0.146 half-turns off with no future). | `theory/retrodictions/synthesis_batches/batch_07.txt:36-45`; `ontology/01_the_cut.md:24-61,110-118` |
| 2026-09-22 | v3.2 decision list item 1 ("which intrinsic phase A3 cuts on") is proposed. It was not adopted: CRR.md is still v3.1. | `ontology/05_next_steps.md` §2; `theory/CRR.md:2,319-327` |
| 2026-09-23 | Rupture detector (δ(Now) feeding a CUSUM on occasion arc and surplus) declared at 05:01:47Z and run the same day. GATE CLOSED. | `Rupture_Detection/RUPTURE_DETECTION.md:1-50`; AGENT_LOG 84, 88 |
| 2026-09-24 | Cut_Content (content-bearing resets at task boundaries) declared and closed the same day. | `Cut_Content/CUT_CONTENT.md`; AGENT_LOG 121-122 |
| 2026-09-26 | Life_Sciences G-CD3: H-CUT on DNA replication initiation against the initiation adder. Synthetic gate OPEN. LIFE1 was not preregistered. | `Life_Sciences/LIFE_SCIENCES.md:28,70-128`; AGENT_LOG 162 |
| 2026-09-27 | CARD-3 diagnostic: 5/28. | ledger CARD-3 |
| 2026-09-29 | PRED70: A3/H-CUT rows WRONG where a domain trigger sets the event. | `Predictions70/PREDICTIONS70.md:79-84`; `Epistemic_Review/checks/redundant_vs_fail.txt:26,31` |

### Operationalisations and added assumptions

- **The intrinsic phase.** It is the unwrapped analytic-signal (Hilbert) phase of the trace (`src/crr/instrument/core.py`
  `intrinsic_phase`). The core docstring says "a prereg may name another (Poincaré section) — both must be reported"
  (`core.py:91`), but no study implemented the Poincaré alternative.
  - This added assumption is the one that later failed in four ways:
    - **(a)** it is non-causal (`ontology/01_the_cut.md:24-32`);
    - **(b)** on an ECG-like beat it "advances about twice per true half-turn (1.9997), so the cut falls four times per beat"
      (`Rupture_Detection/RUPTURE_DETECTION.md:38-39`);
    - **(c)** on three CARD BP channels a fast oscillation dominates it (`reports/card.md:40-46`);
    - **(d)** on Duffing, three phase readings give three antipodes, and "the split … is a property of the analytic-signal
      phase, not of the waveform" (batch 07 row 3).
- **The rupture detector.** CUSUM on per-occasion arc and surplus, at a matched 5 % false-alarm rate. Baselines: clock
  windows, peak occasions, and early-warning signals (AGENT_LOG 84).
  - The added assumption that failed is in the positive control. PC1 ("NC1 with speed jitter") must read AHEAD of the best
    baseline because "an occasion holds one half-turn whatever the speed; a clock window does not"
    (`Rupture_Detection/DECLARATION.md:45`).
  - **Auditor's reading.** That rationale distinguishes δ occasions from *clock* windows only. The peak baseline also holds
    one occasion per half-turn ("peak cuts per delta cut 0.9981", `Rupture_Detection/checks/rupture_checks.txt:25`).
    CRR.md itself says A3 "is testable only where the antipodal cut and the peak cut disagree" (`theory/CRR.md:121`).
  - So PC1's "must beat peak" requirement was not a property true by construction of the CRR ingredient. On PC1 the δ
    detector was ahead of clock where either detected (secondary cell k 0.25: "delta med 25.280 det 36/40 … clock med
    104.167 det 2/40", `rupture_checks.txt:26`), and behind peak.
- **Cut_Content.** Its "content" arms (SP, Head, ReDo0, R-hard, R-soft) are plasticity interventions. They are not A3, which
  says the cut "has no content" (`theory/CRR.md:108`).
  - The assumptions that failed were the gate's own:
    - "warm starting costs nothing" in the convex must-fail world, which holds only at convergence;
    - "the task-start checkpoint carries the damage" (`Cut_Content/CUT_CONTENT.md:46-53`).
- **G-CD3.** The antipode is on the log-volume trace's analytic phase, with events = replication initiations. The domain
  baselines are a fitted cycle fraction and the initiation adder (`Life_Sciences/LIFE_SCIENCES.md:76-93`).

### Results (verbatim)

- **No ledger row tests H-CUT.** The only cut rows are CARD-3 ("5/28 records", "report (no verdict registered; diagnostic)")
  and MEAS2-3 (control iii, "PASS on a control line only"). The prereg notes MEAS2-3 "tests 'own events vs extrema', not A3
  itself" (`prereg/meas2/PREREG.md:127-130`).
- **Rupture (R4, note).**
  - "The gate is CLOSED" (`RUPTURE_DETECTION.md:19`).
  - PC1 "BEHIND … 14.458"; T5 ECG-like "BEHIND … 190.297"; chaotic carriers "TIE" in the main cell.
  - The Lorenz secondary-cell wins are "not a result" (`:75-79`).
  - The one AHEAD main-size cell (T1 k 0.25, δ/best 0.795; `rupture_checks.txt:36`) "becomes TIE 1.000" on a CPU without
    AVX-512 (AGENT_LOG 116, `notebook/AGENT_LOG.md:129`).
- **Cut_Content (R4, note).** "GATE CLOSED": A3 FAILS (+8.69), A4 FAILS (SP +7.08, Head +4.88), A7 "holds for every arm in both
  worlds" (`Cut_Content/CUT_CONTENT.md:12-26`).
- **G-CD3.** "**G-CD3 OPEN.**" The pass fractions in the domain world W− are 0.00 at all three growth rates; W+ gives
  0.90 / 1.00 / 1.00 (`Life_Sciences/LIFE_SCIENCES.md:86-94`). The investigator's forecast for real cells is FAIL (`:108-110`).
- **PRED70 (R4).** By ingredient: "A3: INTERNAL 1, REDUNDANT-IG 1, WRONG 4 … H-CUT (A3): INTERNAL 1, REDUNDANT-IG 2, WRONG 2"
  (`Predictions70/checks/tally.txt:85`). FALSIFIES rows: P11-2 sleep onset and P13-2 relay thermostat
  (`redundant_vs_fail.txt:26,31`).

### Four-layer table

| observation | (1) phenomenon | (2) CRR interpretation | (3) ordinary explanation | (4) distinguishing evidence |
|---|---|---|---|---|
| The antipode–extremum split depends on the phase estimator | Duffing: offsets −0.0066 (analytic), 0.0000 (plane angle), −0.0148 (drive) cycles from the minimum (batch 07 row 3). | A3 locates the cut at a half-turn of the intrinsic phase. | The split is an estimator property. On a causal plane-angle phase the half-turn from a maximum is the next minimum identically. | A v3.2 decision naming A3's phase, then an H-CUT test on own events. ontology/05 proposes "own event where it has one, causal section elsewhere; H-CUT … restated … or retired". |
| ECG-like beat (rupture T5) | The analytic phase advances 1.9997× per true half-turn, so the δ detector is 190.297× slower than peak. | None. | Hilbert phase on a multi-harmonic waveform tracks the dominant harmonic. This is an instrument failure for that carrier class. | A Poincaré or own-event phase on the same carriers. |
| PC1 (speed-jittered asymmetric sine) | δ is behind peak and ahead of clock in the cells where clock detects at all. | Sampling at the cut removes speed jitter. | So does any phase-locked segmentation, including peak detection (0.9981 peak cuts per δ cut). | A positive control where the antipode and extremum disagree and the change is phase-referenced. It was not built. |
| G-CD3 synthetic | Antipode-timed initiations separate from adder-timed initiations at 3 growth rates. | Replication initiation sits at A3's antipode. | The initiation adder (Si et al. 2019; Witz et al. 2019) predicts within 0.0312–0.0631 of a cycle in its own world. | Real lineages (Witz et al. 2019 tables) under LIFE1 as specified (`LIFE_SCIENCES.md:117-128`). Never run. |
| Arc-triggered consolidation times (OB1 C3, cross-reference; L-CLK) | "ARC's consolidation times align with the hidden switches (e.g. 77/148/221/291 against 72/144/216/288)". The gate closed because consolidation had no effect (ledger OB1-C3-A). | The learner's own change marks its boundaries (a cut by own change). | A KL jump at a distribution shift is standard change-point detection. | The arc against a chord and a CUSUM on loss in a stream where consolidation matters. The declared stream could not show it. |

### Salvage classification

- **E (dominant).** H-CUT is not decidable until CRR.md fixes which intrinsic phase A3 uses. Under the causal phase-plane
  reading H-CUT is empty on 1-D traces (batch 07 row 3). Under the analytic reading the split is estimator-dependent and
  non-causal.
  - **Needed:** a CRR.md decision (ontology/05 §2 item 1). Then an H-CUT gate on own events, with a positive control where
    own events sit at the antipode by construction (G-CD3 is one), before any real data.
- **D.**
  - Hilbert-phase failures on multi-harmonic and fast-oscillation carriers (rupture T5; CARD 0069/0085/0088).
  - The rupture AHEAD cell depends on the CPU (AGENT_LOG 116).
  - LIFE1 is blocked: a loader for 2019 pandas pickles cannot be verified without opening them (R2), and a blind loader had
    voided EQ2R and T1x (AGENT_LOG 162).
- **B.** The rupture detector is one operationalisation of the cut as a change detector. That use is not stated in CRR.md.
  - **Chain.** A3 → CUSUM on occasion arc and surplus at Hilbert-phase half-turns → synthetic battery → PC1 behind the peak
    baseline.
  - **Highest level reached:** that one detector design, with the analytic phase. The closure partly reflects a positive
    control whose "must beat peak" requirement the declared mechanism does not supply (auditor's reading).
- **A, at R4 only (synthetic).** In PRED70's sleep-onset and thermostat models the domain's own trigger, not the antipode, set
  the event (P11-2, P13-2). Synthesis WRONG rows add more: the travelling-wave break at the antipode (batch_14 row 2) and the
  fibre-bundle collapse at the antipode (batch_19 row 1), both in the WRONG section of `labs/checks/bank.txt:63-181`.
  - **Highest level reached:** H-CUT as applied to those model systems. There is no real-data test.
- **C.**
  - The empty cut's construction (Cut_Content A7) holds "by construction: a check of the implementation, not support for
    CRR" (`Cut_Content/CUT_CONTENT.md:30-32`). It is a lossless checkpoint.
  - Content-bearing cuts are known plasticity remedies. Where plasticity loss existed, "the known remedies worked"
    (`:36-37`).
- **F.**
  - G-CD3, as a real-data candidate: separable from the domain rule on synthetic data, with an open gate. It is the one H-CUT
    test that can be run.
  - The OB1-C3 alignment of arc-triggered cuts with hidden switches, which belongs to L-CLK.
- **G.** None.

### Extinguished-lead check

- **Rupture detector.**
  - The closure is stated at the right level ("no applied use case may rest on this operationalisation",
    `RUPTURE_DETECTION.md:59`).
  - The failed positive control was not diagnosed: "A diagnosis would be a new declared check" (`:65-69`). R12 forbade a
    same-day redesign, and no later declaration was made.
  - **Auditor's reading.** The gate may have closed partly on a positive control that CRR.md's own testability rule
    (`theory/CRR.md:121`) says cannot separate the antipode from the extremum. That is a lead closed at the gate-design level
    and never reopened. It is not a falsification of A3.
- **Cut_Content.**
  - Closed on two must-fail design defects that the note itself identifies. The convex world was not at convergence, and A3
    was confounded with dose (`CUT_CONTENT.md:46-59`).
  - The redesign "runs only if the owner asks for it". It is not a CRR claim, so nothing of CRR's was extinguished.
- **H-CUT.** Not extinguished. It was never brought to a test, because the theory has not decided its phase and LIFE1 was
  blocked by loader risk.
- **No ledger row or report claims H-CUT failed.** CARD-3 and MEAS2-3 are correctly labelled diagnostics.

### Question-10 evidence (L-CUT)

- **Rupture.** Declared and closed on the same day, 2026-09-23 (AGENT_LOG 84, 88).
  - The R12 stop was applied to a Phase-A synthetic gate whose positive control had failed. AGENT_LOG 88 rejected
    "re-running with a causal phase, a Poincaré section or other statistics until a carrier reads AHEAD (a post-hoc
    search)".
  - That guards against forking paths. But it also treated the first design of a synthetic gate with confirmatory finality,
    and no mechanism scheduled the declared-on-a-later-day redesign.
- **Cut_Content.** The same pattern: declared, run and closed on 2026-09-24 (AGENT_LOG 121-122). An amendment before the run
  fixed one arm (AGENT_LOG 121); defects found by the run closed the gate.
- **LIFE1 (H-CUT's one open gate).** The interaction of R2 and the VOID precedent prevented a preregistration. A schema check
  counts as opening data (AGENT_LOG 162: "rejected: a header-only peek (opening data before the hash)"). This is a direct
  case of the protocol blocking the only real-data H-CUT test that was ready.
- **The v3.2 decision list** (ontology/05 §2) was written on 2026-09-22 and never adopted into CRR.md, so H-CUT has had no
  stated phase to test against for the whole programme. That is a theory-formulation gap, not protocol suppression.

### Open questions for Phoenix (L-CUT)

- **May explore.**
  - Which intrinsic phase A3 means: own event, Poincaré section, or analytic signal. Check whether any reading leaves H-CUT
    non-empty on 1-D traces.
  - The G-CD3/LIFE1 design, with a loader-validation protocol that does not count as "opening" (for example, a schema-only
    read under a declared hash of the loader).
  - A rupture positive control in which the antipode and extremum genuinely disagree.
- **Must never claim:**
  - that δ(Now) detects ruptures better than conventional segmentation;
  - that the antipodal cut beats peak cuts (gate_A3 passes on content-free surrogates);
  - that A7's lossless pause is evidence for CRR;
  - that any real system's own events sit at the antipode.

### Q1-9 summary (L-CUT)

1. **Initial idea.** The Now is a contentless cut at the phase antipode.
2. **Operationalisation.** Hilbert-phase half-turns, antipode against extremum; δ-sampled CUSUM; resets as "content cuts";
   replication initiation at the antipode.
3. **Added assumptions.** The analytic phase; PC1's must-beat-peak requirement; convergence in the convex world.
4. **Assumption that failed.** The analytic phase (non-causal; doubled on multi-harmonic beats); PC1's construction; the
   Cut_Content must-fail world.
5. **Reached the claim.** No real-data result reaches H-CUT. Synthetic WRONG rows reach H-CUT applied to specific models (R4).
6. **Reached only an implementation.** The rupture closure and the Cut_Content closure.
7. **Interesting despite failing.** G-CD3's separability; arc-cut alignment with hidden switches (OB1-C3, L-CLK).
8. **Successes that reduced.** The empty cut reduced to lossless checkpointing (A7 "by construction").
9. **Infrastructure failures.** Hilbert-phase failures, the CPU-dependent AHEAD cell, and the LIFE1 loader block.

---

## L-SURP: surplus S, "lived surplus", π ∝ e^{λS}, SAL

### Trajectory

| date | event | source |
|---|---|---|
| 2026-09-15 | D4 defines S = C − C* ≥ 0. P2 gives the Gibbs weights π ∝ exp(βS) with β unfixed. O2 (surplus or age constraint) is "Untested". | `theory/CRR.md:93-95,155-164` |
| 2026-09-16/17 | An external spec (GPT-6) sets λ = 1 in the per-event Fisher unit (spec H1/T5). Logged as owner-uploaded, newer than v3.1 and not signed. | `prereg/sal/PHASE_A.md:10-12`; AGENT_LOG 9(r); `notebook/PROMPT_LOG.md:462,486` |
| 2026-09-17T00:54Z | Owner asks for a "new suite of continual learning benchmark checks", and SAL is chosen. "The hypothesis is not in theory/CRR.md v3.1". | `notebook/PROMPT_LOG.md:555-559` |
| 2026-09-17 | First operationalisation (live-pass S) rejected before the gate: "e^{S} became a recency kernel" (AGENT_LOG 12(r)). The shadow-pass S is used. gate_SAL is CLOSED on its first run (AGENT_LOG 13(r)). | `notebook/AGENT_LOG.md:24-25`; `prereg/sal/gate_SAL.txt` |
| 2026-09-17 | Roadmap: "T5 … on a carrier where influence is measured … new gate: log-odds slope 1 by construction (must pass) and a Markov surrogate". It was never run. | `docs/ROADMAP_2026-Q4.md:132`; `docs/notes/2026-09-17_note_for_daniel.md:81-86` |
| 2026-09-17 → 09-21 | Synthesis rows using S. In the WRONG section of `labs/checks/bank.txt` (`:63-181`): batch_02 row 2 (S = 0 minimum-dissipation geodesic), batch_10 row 5 (excess work ≥ S²/τ), batch_15 row 4 ("S of a protocol orders its excess work") and batch_03 row 1 (surplus-weighted seed against the posterior mean). batch_24 row 5 (P2 weights as recall frequencies) is REDUNDANT-DOMAIN (`:478-481`). | `labs/checks/bank.txt:75-83,96-99,120-123` |
| 2026-09-22/23 | T1X2-D reports S against the E_old residual. The rupture CUSUM monitors S. | ledger T1X2-D; `Rupture_Detection/DECLARATION.md:15` |

### Operationalisations and added assumptions

- **SAL.**
  - **The learner.** One occasion is one task. S_m is measured on "a replay-free shadow pass over task m from the weights at
    its start" (D6 categorical, per-update unit). Replay draws a past task with probability π_m. The grid is
    λ ∈ {−1, …, 2} (`prereg/sal/PHASE_A.md:13-19,23-25`).
  - **Added assumptions:**
    - **(a)** P2's weights act by *reallocating a fixed replay budget*;
    - **(b)** S is the D6 per-update path surplus on a probe;
    - **(c)** the positive control is a world where "surplus tracks forgetting" (Spearman +0.83), not a world where
      e^{λS}-weighted replay is optimal by construction.
  - **The assumption that failed is (a) with (c).** "Reallocating a fixed replay budget by e^{λS} never beats uniform replay
    by a resolvable step on a stream built in its favour, because starving the low-surplus tasks costs more than
    over-replaying the high-surplus ones gains" (`prereg/sal/PHASE_A.md:39-46`).
- **Minor instrument fact.** SAL's positive control printed S per task "[0.15, 1.7, 0.1, 2.3, -0.07]" (`gate_SAL.txt`). That is
  one negative surplus, which D4 forbids up to round-off (`theory/CRR.md:93`). D6's C = Σ√(2KL) and C* = √(2E) are
  second-order quantities, so P1 is not guaranteed for them. T1X2's old-probe S was never negative: "S < 0 in 0/108 runs"
  (`runs/t1x2/score.txt:8`). Not load-bearing.
- **Structural link to L-L5 (auditor's reading, above).** H-L5 beyond the amplitude control needs S > 0 occasions whose arc
  compensates amplitude. The surplus is therefore where H-L5's non-trivial content would have to live. No real-data study
  isolated it.

### Results (verbatim)

- **SAL-A.**
  - Observed: "S-SAL-P: best λ = −0.25 gains +0.03; λ = 1 gains −0.67; λ = 2 gains −10.57 … Spearman(S, forgetting) +0.83.
    S-SAL-F: all λ within ±0.15. S-SAL-D: λ = 1 gains −15.54".
  - Pass fraction: "positive control 0/1; negative controls 2/2 behave".
  - Verdict: "**GATE CLOSED: no positive control exists for this operationalisation; study not run (R4, R12)**".
- **T1X2-D.** "report: high-S runs fall off the endpoint curve on feynman_II_36_38 and feynman_I_9_18 only" (values
  −0.029 / −0.522 / +0.485 / +0.659 / +0.132).
- **Rupture.** The arc-and-surplus CUSUM gate is CLOSED (see L-CUT).

### Four-layer table

| observation | (1) phenomenon | (2) CRR interpretation | (3) ordinary explanation | (4) distinguishing evidence |
|---|---|---|---|---|
| SAL S-SAL-P | S tracks forgetting (+0.83), yet no λ improves replay by ≥ 1.0. | Surplus marks which past occasions matter; regeneration should weight them. | Under a fixed budget, the marginal value of replay is concave across tasks. Starving the easy tasks costs more. Standard allocation reasoning. | A carrier where influence is *measured*, not imposed (`PHASE_A.md:56-60`). The T5 design: a log-odds slope of 1 by construction, and a Markov surrogate must predict nothing. Never run. |
| Live-pass S grows with task index | e^{S} becomes recency weighting. | — | Surplus–recency compensation (spec Decision 10). | The shadow pass was used. This was a design fix, not a finding. |
| Protocol surplus rows (WRONG) | S does not order excess work where friction is not Fisher times a scalar. The S = 0 protocol is not the minimum. | S = 0 is the efficient route. | Thermodynamic length uses the friction tensor, not the Fisher metric. The minimum is the friction geodesic. | Already decided in the domain: WRONG. |
| T1X2-D | Mixed-sign association of S with the residual of the endpoint fit. | Surplus carries path information. | Noise in a report-only statistic over 5 carriers. | A fresh, pre-registered sign test. Low prior. |

### Salvage classification

- **A, at R4 (synthetic), for one operationalisation.**
  - **Chain.** P2 (`theory/CRR.md:155-157`, β free) → the external spec's λ = 1 → surplus-weighted allocation of a fixed
    replay budget on a small learner → gate → no λ on the grid helps the world built in its favour.
  - **Highest level reached:** "weighting replay by e^{S} does not help" on "continual learners of this kind"
    (`PHASE_A.md:56-58`). It does not reach P2 or A6 in general. It explicitly does not reach "the spec's intended domain".
- **B.** Replay allocation is one translation of "regeneration weights occasions by surplus". Other translations were named and
  not tried: "a weight on a per-task regulariser … S measured on a task-specific probe, or … a smaller unit"
  (`PHASE_A.md:51-55`).
- **E.**
  - O2 (surplus or age) needs "a carrier whose occasions differ in-family **and** recur" (`theory/CRR.md:162-164`).
  - T5 needs a system whose influence of past occasions is observable. "The learner supplies no such observable"
    (`PHASE_A.md:58-60`).
  - Decidable with: the roadmap's T5 gate and a carrier with measured retrieval weights (`docs/ROADMAP_2026-Q4.md:132`).
- **C.**
  - P2 itself is Jaynes (`theory/CRR.md:155-157`).
  - The P2-as-recall-frequency row is REDUNDANT-DOMAIN (batch_24 row 5).
  - The S = 0 / geodesic rows reduce to thermodynamic length where they hold, and are WRONG where friction is not Fisher.
- **D.** The S < 0 print in the SAL gate (D6 approximation). Minor.
- **F.** T1X2-D, weak and sign-inconsistent. The structural observation that H-L5's content beyond amplitude is surplus is a
  conceptual link, not an empirical near-win.
- **G.** None.

### Extinguished-lead check

- **SAL was closed by the right rule, at the scope its own note states.**
- **Two places compress the closure.**
  - The CLAUDE.md summary "no positive control exists" and the roadmap's "Retired unless re-opened by a new gate: …
    salience-weighted replay (SAL-A)" (`docs/ROADMAP_2026-Q4.md:134-135`) both say less than the note. The note's own reading
    is stronger and more precise: the instrument saw S, and the effect was absent.
  - The phrase "no positive control exists" could be misread as an instrument failure (D). The record supports A at R4 for
    one operationalisation.
- **"Lived surplus" as a regeneration weight in the spec's intended domain (T5) was never tested.** It was deferred, not
  extinguished: "None was tried", deliberately, to avoid a forking path (`PHASE_A.md:55`).

### Question-10 evidence (L-SURP)

- **SAL went from request (2026-09-17T00:54Z) to gate closure on the same day.** One operationalisation iteration
  (live → shadow pass) happened before the gate. After closure, R12 forbade trying named alternatives in sequence.
- **No exploratory environment existed** in which the three named alternative translations could have been explored on
  synthetic worlds without counting as forking. The protocol treats each as a new study needing its own gate. None was ever
  declared.
- **T5, the stated-domain test, needed a different carrier class and a new gate.** It was planned on 2026-09-17 and never
  started. Nothing in the record shows the protocol blocked it; it was not prioritised.

### Open questions for Phoenix (L-SURP)

- **May explore.**
  - Whether S has any role at all once P1's arithmetic is removed. Check where S > 0 occasions exist in real carriers and
    whether S compensates amplitude (the H-L5 link).
  - T5 on a carrier with measured influence.
  - Alternative P2 translations, declared as exploratory.
- **Must never claim:**
  - that surplus-weighted replay helps;
  - that S orders dissipation or excess work;
  - that "lived surplus" has an empirical signature on the record (T1X2-D is mixed-sign and report-only).

### Q1-9 summary (L-SURP)

1. **Initial idea.** What a system does beyond the shortest route (S) is what regeneration weights.
2. **Operationalisation.** Replay allocation ∝ e^{λS} on a continual learner; S in CUSUMs and diagnostics.
3. **Added assumptions.** A fixed replay budget; D6 per-update S on a shadow pass; λ = 1 from the external spec.
4. **Assumption that failed.** Budget reallocation (a, with c).
5. **Reached the claim.** None of CRR.md's stated hypotheses. P2 is standard and β is free.
6. **Reached only an implementation.** SAL-A.
7. **Interesting despite failing.** S tracked forgetting at +0.83 on the positive control. The structural role of S in H-L5.
8. **Successes that reduced.** P2 is Jaynes. The S = 0 geodesic reduces to thermodynamic length.
9. **Infrastructure failures.** None of substance. One S < 0 print.

---

## Cross-lineage observations (for the synthesis)

1. **Two stated hypotheses received fair real-data FAILs that reach the hypothesis as stated.**
   - H-L5: on measles and the pulse; the pulse is named in CRR.md.
   - H-T1: on one learner class, losing to every endpoint comparator.

   This matches the declaration's expectation 1 (`Pre_Phoenix_Audit/DECLARATION.md`): "A minority will reach the stated
   hypotheses directly (H-L5 on real carriers; H-T1 against the old-probe endpoint)". One refinement: H-T1's failure does not
   depend on the old-probe endpoint, since E_new and EWC distance also win.

   H-CUT never received a real-data test of any kind.
2. **The surplus is the hinge between L-L5 and L-SURP.** P1 makes arc = chord = amplitude on monotone occasions. So every
   "arc-regular" success on the record reduces to the chord, and the only remaining form of H-L5 is a claim about S > 0
   compensation. SAL tested S in a different role (replay weights), and no study tested S in this role.

   This is the clearest case in these lineages of a single conceptual point appearing in several failed tests
   (MEAS2, CARD-2, CD-1, PRED70's 7, P02-1).
3. **Recurring operationalisation failure: the analytic-signal phase.**
   - Non-causal (`ontology/01_the_cut.md`).
   - Doubled on multi-harmonic beats (rupture T5).
   - Dominated by fast oscillations (CARD BP channels).
   - Estimator-dependent antipodes (batch 07 row 3).

   CRR.md leaves the phase unnamed. The named alternative (Poincaré) was never implemented in `core.py`. Every A3 and H-CUT
   conclusion on the record is conditional on this one estimator.
4. **Recurring structural issue: the positive control does not match the scored criterion.**
   - CARD: gate_L5's one-hump positive controls tie amplitude, while CARD scores amplitude strictly.
   - Rupture PC1: its rationale beats clock windows, but it was required to beat peak segmentation.
   - T1: S-H2 builds path dependence into the definition of F.
   - SAL: a "surplus tracks forgetting" world, not an "e^{S} replay is optimal" world.

   In each case the gate's positive control tested an easier or different property than the decisive criterion. Only the
   measles gate (L5R) was built to match its criterion: its two-hump row and its docstring.
5. **Question 10 in these lineages.**
   - Confirmatory real-data tests of H-L5 came within an hour of the request, before the conceptual analysis (2026-09-17 to
     09-21) that located H-L5's content in S.
   - Synthetic gates (SAL, Rupture, Cut_Content) were declared, run and closed on the same day. R12 then forbade same-day
     redesign, and no later redesign was ever declared.
   - The one ready real-data H-CUT test (LIFE1) was blocked by R2's treatment of a schema check as opening data.
   - Exploratory development did happen where it was synthetic and before the first gate run (T1x smoke, AGENT_LOG 68; SAL's
     live → shadow fix).

   The pattern: exploration was permitted *before* a first gate run and effectively ended *at* it. A first-run gate closure
   (Phase A, synthetic) received the same finality as a held-out FAIL.
