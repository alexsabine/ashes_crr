# Pre-Phoenix audit notes: L-MEM and L-CLK

PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED. These are a reader's notes. They are not evidence (R8).

**Scope.**
- **L-MEM**, memory without stored exemplars and replay:
  - `Replay_Quality_Memory/` (RQM);
  - `Relational_Reference_Memory/` (RRM, RRM2, including the HopDC comparisons);
  - `Coupling/` (CPL1).
- **L-CLK**, own-clock (arc-clocked) optimisation and consolidation:
  - `Open_Bottlenecks/` (OB1: C1, C3, and C2, which was never run);
  - `Continuous_Learning/FOREVER/`;
  - `Energy Design Principle/checks/clock_cut`.
  - Also the one held-out own-clock row, `SOTA1-3:crr-stepclock`. The study belongs to L-EQ/SOTA1, but the row bears
    directly on L-CLK.

**Conventions.**
- Ledger rows are cited by id from `ledger/LEDGER.md`. Files are cited as `path:line`.
- Every number is copied from the cited source. Where I derived something myself (a count, a difference, a time span), it
  is marked **auditor's count (derived)** and the method is stated.
- Times come from commit timestamps (`git log --format=%cI`). AGENT_LOG 146 records that some PROMPT_LOG timestamps were
  typed by hand, so the commit times are used for spans.

**Theory anchor.**
- `theory/CRR.md:306-315` lists the only falsifiable claims: H-CUT, H-L5, H-T1 and H-EQ. "Everything else in this document
  is definition, standard mathematics, or open" (`theory/CRR.md:315`).
- None of the four is a claim about memory, transport, optimiser moments or consolidation triggers.
- The ingredients the two lineages used are of three kinds:
  - **axioms and definitions:** A3 (`:101`), A6 (`:144`), D2 (`:76`), D6 (`:233`), A1′ (`:55`);
  - **an open item:** O3, the cut without a rotor (`:137`);
  - **a slogan:** "change has its own clock", the §4 heading at `:196`, whose falsifiable form is H-L5 (`:200`), a
    regularity claim about a system's own boundary events.
- `Proposition 7` (the empty cut) does not appear in `theory/CRR.md`. It lives in `AI_Safety/`.
- A3 is defined on a rotor. Reading a task boundary as a cut is therefore already outside A3's stated domain. O3
  (`theory/CRR.md:137`) says nothing yet sets the cut for non-cyclic becoming. `Continuous_Learning/FOREVER/FOREVER_AND_CRR.md:21`
  says the same about FOREVER's triggers ("not an A3 cut").

---

## L-MEM — memory without stored exemplars

### 1. Trajectory (dated, cited)

All of L-MEM ran on **2026-09-30**, between 01:55 and 10:59 UTC, mostly while the owner slept.
- PROMPT_LOG 250 (03:46Z): "I am going to bed now so please keep working overnight on testing the idea repeatedly in
  different ways".

| when (commit, UTC) | step | source |
|---|---|---|
| 01:49Z (prompt) | Owner asks what "Replay keeps a notebook, SEC doesn't need one" means | PROMPT_LOG 244 |
| 01:54Z (prompt) | "Apply CRR to solving this 'replay-quality memory' problem ... try to achieve a Pass-1" | PROMPT_LOG 245 |
| 01:55:54 `1d480cb` | RQM DECLARATION: target, M1–M7, the CRR heuristic procedure, route to PASS-1 | `Replay_Quality_Memory/DECLARATION.md`; AGENT_LOG 189 |
| 02:14:49 `59156d8` | CRR_READING: RESTATES 6, SILENT 4, no CANDIDATE. The reading selects input-space Gaussian replay (= GMR/DGR) | `Replay_Quality_Memory/CRR_READING.md:14-53`; AGENT_LOG 190 |
| 02:15:47 `5d46fcb` | DEV_DECLARATION: IGR-F/IGR-D, the FGR ablation, ER at matched memory, RFR; Phase A gate | `DEV_DECLARATION.md:11-63` |
| 02:19:47 `b4ee36c` | Phase A run 1: GATE CLOSED (the rings control was unlearnable); post hoc Amendment 1 (NEG2, G-LEARN) | `phase_a_run1.txt:25-32`; `DEV_DECLARATION.md:108-132`; AGENT_LOG 191 |
| 02:21:38 `76e87b3` | Phase A run 2: GATE CLOSED again (criterion cannot fail). RQM stops (R12) | `phase_a.txt:27-33` (file lines); ledger **RQM-A**; AGENT_LOG 192 |
| 02:55Z (prompt) | Owner's object-relations reading: "the relationality between the schematic representations is what matters ... each object (person) is a different reflection of the first object" | PROMPT_LOG 248 |
| 03:00:55 `3a740f1` | RRM DECLARATION: anchor-referenced transport, forms RRM-1 and RRM-A, ER-20 comparator, DECOY must-fail | `Relational_Reference_Memory/DECLARATION.md`; AGENT_LOG 194 |
| 03:05:08 `e75f239` | RRM Phase A part 1: GATE CLOSED on 1 of 8 conditions (RRM-A under ROT). RRM stops (R12) | `worlds.txt:40-48`; ledger **RRM-PA**; AGENT_LOG 195 |
| 03:25:27 `be40f23` | RRM literature grade N1–N6 (N5 PARTLY REDUNDANT: transport not found) | `PHASE_A.md:53-79`; AGENT_LOG 196 |
| 03:48:26 `a2719f0` | RRM DECLARATION_2: Part W worth rule, then T1–T6 | `DECLARATION_2.md`; AGENT_LOG 197 |
| 04:18:02 `3fb8b02` | Part W verdict: NOT WORTH PURSUING (P5 REDUNDANT on the investigator's review of HopDC) | `DECLARATION_2.md:111-133`; AGENT_LOG 198 |
| 04:23–04:24 | T1, T2, T3: all GATE CLOSED | ledger **RRM2-T1**, **RRM2-T2**, **RRM2-T3**; AGENT_LOG 199 |
| 04:25:22 `33d332f` | DECLARATION_3 (POST HOC, report only): T7, the drift-rich regime | `DECLARATION_3.md`; AGENT_LOG 199 |
| 04:41 → 06:27 | T1 and T7 on the 30 SEEN carriers (report only) | `t1_seen.txt`, `t7_seen.txt`; AGENT_LOG 226 |
| 04:57Z (prompt) | "Can you give me a quick summary on the last output from the hop dc comparison and what this means for CRR?" | PROMPT_LOG 251 |
| 07:11Z (prompt) | "explore the potential of using crr to couple the sec4 finding with the hop finding together, and the AI safety cut" | PROMPT_LOG 257 |
| 07:29:18 `440e185` | CPL1 DECLARATION | `Coupling/DECLARATION.md`; AGENT_LOG 215 |
| 10:59:11 `1a76ef4` | CPL1 closed: GATE CLOSED | ledger **CPL1-A**; AGENT_LOG 229, 230 |

**Auditor's count (derived) from those commit times.**
- Declaration to final gate closure:
  - RQM: ≈ 26 min (01:55:54 → 02:21:38);
  - RRM part 1: ≈ 4 min (03:00:55 → 03:05:08);
  - RRM2 T1–T3: ≈ 36 min from DECLARATION_2 (03:48:26 → 04:24:00);
  - CPL1: ≈ 3.5 h (07:29:18 → 10:59:11).
- Pre-registrations: none. Unseen carriers opened: none.

### 2. Operationalisations and added assumptions

**The initial idea** (PROMPT_LOG 244–245; `DECLARATION.md:8-13`). Get replay-quality class-incremental memory without
storing raw examples. The quoted gap is class-IL split-MNIST at "19.52–20.01 % against replay's 90.78–90.79 %"
(`DECLARATION.md:11-12`).
- AGENT_LOG 190 (2) later found that 90.79 was *generative* replay. An erratum was appended to the source note.

The work used five operationalisations, each with assumptions added to make it testable.

**(a) RQM: the CRR reading as a heuristic** (`CRR_READING.md:14-26`).
- Ingredients: A3/D5, A6, P2/P3, A1′, and Proposition 7 "transposed as in EPS1–EPS3" (`:16`).
- Added assumption 1: a task boundary is a cut. A3 itself is defined on a rotor (`theory/CRR.md:101`).
- Added assumption 2, the one that did the work: the EPS condition, "a settled content stays valid only if it does not
  depend on what later learning changes" (`CRR_READING.md:30-36`).
  - This prescribes storing the memory in coordinates that learning does not change: input space (`:38-41`).
  - That is the drift literature's own diagnosis (B1, RESTATES, `:16`).
- Result: RESTATES 6, SILENT 4, no CANDIDATE (AGENT_LOG 190). The reading selects Gaussian Mixture Replay (GMR,
  arXiv 2104.09240 v1) (`CRR_READING.md:47-53`).

**(b) RQM: the candidate and its test** (`DEV_DECLARATION.md:15-63`).
- The candidate: IGR, per-class input Gaussians fitted at each class's cut and never refitted.
- The CRR ablation: FGR, the same Gaussians fitted in feature space.
- Added assumption: the criterion "not behind ER **at matched memory**" (ER keeps ⌈b_c/d⌉ rows per class: 12 for IGR-F, 2
  for IGR-D; `DEV_DECLARATION.md:33-36`).
  - **This added assumption is what failed.**
- Added assumption: the negative control. Run 1's rings were unlearnable. Run 2's NEG2 uses moment-matched class pairs
  (`DEV_DECLARATION.md:117-128`).

**(c) RRM: the owner's object-relations reading** (`Relational_Reference_Memory/DECLARATION.md:15-52`).
- Each settled content is stored as a relation to kept anchors, h′ = h + (H_A(now) − H_A(cut))ᵀ R h.
- Added assumptions:
  - drift is **shared and linear** on the anchors' span (`:24-25`, `:37-38`);
  - **M raw rows are kept**, which relaxes RQM's "no stored raw rows" (`:42-43`);
  - the gate required **both** forms, RRM-1 and RRM-A, to clear every condition (`:99`).
    - **This conjunction is what closed the gate.**
- The literature sweep graded N5 (the transport itself) PARTLY REDUNDANT, "not found published" (`PHASE_A.md:68-75`).

**(d) RRM2: the same mechanism inside the SEC1 MLP learner** (`DECLARATION_2.md:53-110`).
- Added assumption: the SEC1 one-hidden-layer MLP on POS/NEG2 is "a learner whose features actually drift"
  (`DECLARATION.md:108-109`).
  - **This added assumption failed.** "the learner's features barely drift" (ledger RRM2-T1).
- Added assumption: a worth rule on the literature that gates the pre-registration (`DECLARATION_2.md:41-48`).
- Amendment 1 adds a HOPDC arm on the same kept anchors (`DECLARATION_2.md:125-133`).

**(e) CPL1: SEC4's clipped SEC + HopDC-type transport + the empty-cut pause** (`Coupling/DECLARATION.md:24-45`).
- Added assumption: the anchors are **current-task rows** ("No old-class rows are kept", `:30-32`), to keep the
  exemplar-free rule.
  - **This added assumption is what failed**: "current-task anchors drift about twice the old-class shift" (AGENT_LOG 229).
- Added assumption: the drift world is a rotated synthetic stream plus Kuzushiji-MNIST (`:71-73`).
  - The rotated stream "barely drifts" (`cpl_phase_a.txt:195`).

### 3. Results (verbatim verdicts, by row id)

- **RQM-A**: "GATE CLOSED twice; RQM stops at Phase A (R12): the criterion 'not behind ER at matched memory' cannot fail
  where the memory is wrong."
  - Run 1: "G-NEG FAILS (the rings unlearnable: JOINT 10.77, chance 10)".
  - Run 2: "G-NEG FAILS (IGR ahead of matched ER on NEG2 by +8.2274 and +17.7258 where its Gaussians are provably wrong),
    G-POS, G-FT, G-ID, G-LEARN hold".
- **RRM-PA**: "GATE CLOSED at part 1 (the declared gate required both forms); RRM stops at Phase A part 1 (R12); part 2
  (the learner) not run". "RRM-1: all hold"; "RRM-A: G-SHARED on ROT FAILS (ORACLE - RRM +1.8060 against step 1.1072)".
- **RRM2-T1**: "GATE CLOSED (T1)". "stale errors 0.1197-0.2550 against decoy errors 3.1345-6.7996 (the features barely
  drift)". On the 30 SEEN carriers (report only): "drift explained > 0 on 29/22/28 of 30 (FT/ANCH1/ER20), more than HOPDC on
  30/30 each, NCM RRM - STALE split".
- **RRM2-T2**: "GATE CLOSED (T2); T5 development not run". "G-REL FAILS (+0.4682, step 1.2936)"; "G-CANFAIL holds on POS
  (-2.3411, step 1.5399), FAILS on NEG2 (-1.4047, step 2.2023)"; "RRM-1 - HOPDC-1 +0.1338 on both streams".
- **RRM2-T3**: "GATE CLOSED (T3)". "NCM-RRM - NCM-STALE -0.2007 (step 1.1272) FAILS"; "NCM with stale prototypes 85.35
  against the softmax head 43.88 (the forgetting is in the head)".
- **CPL1-A**: "GATE CLOSED (the coupling stops, R12): transport with current-task anchors makes the stored means worse in
  this learner, so the coupling adds nothing; the pause construction holds on the whole coupled state (a check of the
  construction, not support for CRR)".
  - "G-DRIFT FAILS on both drift worlds (rotated I_NCM -0.2007, FT+T - FT NCM within a step, stale relative error 0.0191;
    Kuzushiji-MNIST FT+T - FT NCM -8.840, step 1.47, while ORACLE - STALE +2.480, step 1.11: drift to fix, and this
    exemplar-free transport does not fix it)".
  - "C1-EXACT bit-identical on 160/160 stream-seeds".
  - "C3 ER-20 ahead of the coupled best on 11/32, behind on 14/32; forecasts 1-4 FAIL".
- **Non-ledger results** (all labelled report or post hoc in the source):
  - RRM2 Part W: "NOT WORTH PURSUING; failing: P5 (the transport is published)" (`DECLARATION_2.md:113-114`).
  - RRM2 T7 forecasts: "F1 ... held", "F2 ... held", "F3 ... not held", "F4 ... not held" (`t7_drift.txt:40-43`).

### 4. Four-layer tables for the key observations

**O-MEM-1. Input-space Gaussian replay matched joint training on its own stream and beat matched ER**
(`Replay_Quality_Memory/PHASE_A.md:34-36`; `phase_a.txt` file lines 4-12 and 14-22).

| layer | content |
|---|---|
| observed | On POS, IGR-F 84.95 against JOINT 85.35; ahead of matched ER by +6.8896 (IGR-F) and +28.7625 (IGR-D). On NEG2, IGR-F 36.45 against ER-F 28.23 and JOINT 42.41. In RRM2 T2 (report), IGR-F was 84.95 on POS and 36.45 on NEG2 against ER-20's 79.93 and 32.04 (`t2_learner.txt:7-8, 18-19`) |
| CRR interpretation | A3 + A6: a content settled at the cut and regenerated is a sufficient memory where it does not depend on later learning (`CRR_READING.md:38-45`) |
| ordinary explanation | Gaussian Mixture Replay / deep generative replay with a Gaussian generator (`CRR_READING.md:47-53`). On POS the Gaussian is the true generator. At 12 or 2 rows per class, ER is weak. On NEG2 each pair sits on its own two coordinates (`DEV_DECLARATION.md:119-121`), so a Gaussian memory still separates the five pairs; it is wrong only within a pair (auditor's reading of the stream definition, not a printed number) |
| what would distinguish | Nothing CRR-specific: the record grades the design RESTATES. The useful test is engineering: IGR against JOINT or ER at a fixed realistic budget, on a stream where Gaussians are wrong in every direction (`PHASE_A.md:41-48`) |

**O-MEM-2. Input-space memory ahead of feature-space memory (the "CRR ablation")** (`PHASE_A.md:37`).

| layer | content |
|---|---|
| observed | IGR-F − FGR-F +2.4080 on POS and +1.6722 on NEG2 (`phase_a.txt` file lines 36-37). Reported, not gated |
| CRR interpretation | The EPS condition: memory that depends on the learner's state goes stale |
| ordinary explanation | Representation drift, the frontier's own named bottleneck (B1, `CRR_READING.md:16`). FGR also updates only the head (`DEV_DECLARATION.md:30-31`), a second difference between the arms |
| what would distinguish | Nothing. Both predict the same sign; the record says "a check of the condition's reading, not evidence for CRR (R8)" (`CRR_READING.md:58-59`) |

**O-MEM-3. Relational transport recovers shared drift, and partly survives unshared change** (`worlds.txt`; `t4_sens.txt`).

| layer | content |
|---|---|
| observed | RRM-1, SHARED: RRM − STALE +3.0769, ORACLE − RRM +0.9365 (`worlds.txt:40`). UNSHARED: STALE 10.84, RRM 52.64 (RRM-1) and 51.91 (RRM-A) (`worlds.txt:17-18, 35-36`; `PHASE_A.md:37-41`). T4, ε = 0.1, ROT: RRM − STALE up to +27.63 (`t4_sens.txt:78`) |
| CRR interpretation | The owner's reading: content as a relation to a "first object" (PROMPT_LOG 248). It is not a CRR.md ingredient. DECLARATION.md:27 calls it "the machine translation" |
| ordinary explanation | Under a linear change on the anchors' span the transport is exact by construction (`DECLARATION.md:37-38`). This is ridge regression on anchor features, in the HopDC / SLDC / relative-representation family (N1, N3 REDUNDANT; `PHASE_A.md:60-62`). The UNSHARED result is "reported only" (`PHASE_A.md:41`). One possible reason: the transported prototype is re-expressed in the anchors' new features (`PHASE_A.md:39-40`) |
| what would distinguish | Nothing CRR-specific. Exactness under shared linear drift is a property of the construction |

**O-MEM-4. The SEC1 learner's features barely drift, and the forgetting lives in the head** (RRM2-T1, RRM2-T3; `DECLARATION_3.md:3-9`).

| layer | content |
|---|---|
| observed | On POS (E = 3), relative drift is 0.0113 (FT), 0.0147 (ANCH1) and 0.0180 (ER20) (`t7_drift.txt:3-5`). Raising E to 30 reaches only 0.0425 (`t7_drift.txt:17`). NCM with stale prototypes 85.35 against the softmax head 43.88 (`t3_ncm.txt` file lines 4, 6). Held-out echo, in another study: SOTA1-3:pred-fast, nearest class mean against the fast head, d = +7.958000, "5/5 seeds ahead", "report (no verdict)" |
| CRR interpretation | None offered. The record treats it as "no headroom" for the mechanism |
| ordinary explanation | Task-recency or classifier bias of the softmax head, and the reason NCM / prototype classifiers are used in class-IL (iCaRL / SDC). The T3 design names "the use SDC makes of drift compensation" (`DECLARATION_2.md:84`) |
| what would distinguish | Not a CRR question. It is a fact about the learner that removed the mechanism's leverage |

**O-MEM-5. Conditional on drift to fix, kept-anchor transport helps; current-task-anchor transport hurts.**
This is a cross-study observation. The record never puts the two diagnostics side by side; the juxtaposition is the
auditor's.

| layer | content |
|---|---|
| observed | (i) CPL1's post hoc ORACLE-means diagnostic: "ORACLE ahead of STALE by more than a step on 4/32 streams ['har', 'isolet', 'Indian_pines', 'Kuzushiji-MNIST']" (`cpl_phase_a.txt:175`). There, current-task-anchor transport T − STALE under FT: har −1.279 (WITHIN), isolet −10.533 (NEGATIVE), Indian_pines −7.173 (WITHIN), K-MNIST −8.840 (NEGATIVE) (`cpl_phase_a.txt:149-150, 173-174`). (ii) On the same four carriers, RRM2 T1 SEEN (report only, no step printed), with 20 kept first-task anchors, NCM RRM − STALE under FT: har +6.7333, isolet +2.6667, Indian_pines +13.6464, K-MNIST +1.7400 (`t1_seen.txt:984, 987, 1056, 1059`). **Auditor's count (derived): positive on 4/4 under FT, by reading the sign in column 4 of those lines.** Under ANCH1: +2.9570, +0.7667, +7.3726, −1.6400 (`t1_seen.txt:985, 988, 1057, 1060`). Over all 30 carriers the record reports only the aggregate "NCM RRM ahead of STALE on 14, behind on 15" (FT) (`t1_seen.txt:1062`). In T7, on har (ANCH1, E = 3): ORACLE 86.07, STALE 72.13, RRM 75.08, HOPDC 74.35 (`t7_seen.txt:66`); on Indian_pines: ORACLE 63.00, STALE 53.45, RRM 60.82, HOPDC 63.74 (`t7_seen.txt:426`) |
| CRR interpretation | The owner's: relate content to a stable "first object", not to a moving present. Not a CRR.md claim |
| ordinary explanation | Anchor provenance. Anchors that do not drift with the current task track old-class drift; current-task anchors "drift about twice the old-class shift" (AGENT_LOG 229). This is the HopDC family (AGENT_LOG 198) plus "transport keys" (arXiv 2606.02860, kept earlier-task anchors; `docs/citations/rrm2_f2_2026-09-30.md:554-566`). Kept anchors are also 20 raw rows, which breaks exemplar-free |
| caveats | Post hoc, SEEN, report only, no step on the T1 SEEN summary lines. The four carriers were selected by a later, separate diagnostic. The learners differ: T1's FT learner against CPL1's FT arm. The review's figure for "T7-style anchors" in CPL1's learner on K-MNIST is "+0.50 within a step" (AGENT_LOG 229), which does not match t1_seen's +1.7400; the record does not reconcile the two (different transport form and run) |
| what would distinguish | A declared test, on unseen carriers screened by a pre-registered drift-to-fix criterion (ORACLE − STALE > step), comparing kept-anchor ridge transport, kept-anchor HopDC, current-task HopDC, STALE and ORACLE. None of it would be CRR evidence |

**O-MEM-6. Exemplar-free NCM on stored statistics is level with ER-20 on the SEEN carriers** (CPL1 C3).

| layer | content |
|---|---|
| observed | "REPORT ER-20 against the SEC-only NCM (no transport): ahead by more than a step on 11/32, behind on 15/32, within on 6/32" (`cpl_phase_a.txt:241`) |
| CRR interpretation | None |
| ordinary explanation | Streaming class statistics with an NCM readout (M1 REDUNDANT; `Replay_Quality_Memory/PHASE_A.md:58`). This bears on RQM's original target ("replay-quality ... without stored data") through a known method |
| what would distinguish | Not a CRR question. It is an applied benchmark question |

### 5. Salvage classification (A–G, with the level the evidence reaches)

| item | categories | highest level the negative evidence legitimately reaches |
|---|---|---|
| RQM's CRR reading (RESTATES 6, SILENT 4, no CANDIDATE) | **C** (reduction at the design level: the reading picks GMR) | CRR as a **design heuristic** for exemplar-free memory: it produced restatements only, in one sweep, on one day. It does not reach any CRR.md claim: none is about memory (`theory/CRR.md:306-315`), and retention depth is explicitly open (O1, `:268`) |
| RQM-A (gate closure) | **D** (instrument: the criterion cannot fail), plus D for run 1's unlearnable control | **Instrument only.** The candidate was not shown to fail. On POS it came within 0.4013 of JOINT (`PHASE_A.md:34`) |
| RRM-PA | **D** (gate conjunction across forms) + a narrow **A/B** for the RRM-A form | The RRM-A form under ROT (thin early anchor span, untested reason; `PHASE_A.md:32-36`). **Not** the owner's form RRM-1, which "cleared every condition" (`PHASE_A.md:26`) |
| RRM2-T1, T2, T3 | **E** (no headroom: nothing to fix) + **D** (G-CANFAIL fails on NEG2) | **One learner, two synthetic streams.** "the features barely drift" (RRM2-T1), so transport and stale cannot be told apart there. Not evidence against transport where drift exists |
| Part W "NOT WORTH PURSUING" | **C** (reduction to HopDC by the investigator's reading) | One judgement. The grading agent read HopDC "close" (which gives WORTH); the investigator read it "states" because "anchor provenance and the relation's form are not predicates of P5" (`DECLARATION_2.md:119-122`; AGENT_LOG 198). Not decisive for the stop: T6 also needed T5, and T5 needed T2's gate, which closed (`DECLARATION_2.md:96-101`) |
| T7 (post hoc) + T1 SEEN | **F** (unresolved structure, non-CRR): O-MEM-5 | Report-only on SEEN data; no level |
| CPL1-A | **A** for one operationalisation (current-task-anchor, exemplar-free transport in this learner), **D** for the rotated world ("barely drifts"), **C** for the pause (a construction) | **One operationalisation and implementation**: HopDC-type transport with current-task anchors, SEC1 MLP, SEEN carriers, R4/R5. It does not reach kept-anchor transport, and it does not reach CRR. The pause half is "a check of the construction, not support for CRR" |
| CPL1 C3 / O-MEM-6 | **C/F** (a known method level with ER-20 on about half the carriers) | Not CRR |

**Is any of L-MEM a G?** No. Nothing in L-MEM is above R4/R5. Every ledger row is a closed gate (`Epistemic_Review/checks/ladder.txt:252-259`).

### 6. Extinguished-lead check

1. **RQM: a candidate stopped by its criterion, not by itself.**
   - The gate closed because matched-memory ER is too weak to lose to (RQM-A). That is a comparator design defect.
   - The candidate never reached the SEEN carriers: D-PHASE required Phase A open (`DEV_DECLARATION.md:79`).
   - The repair, a criterion against JOINT or ER at a fixed budget, was named (`PHASE_A.md:41-48`) and not declared.
     AGENT_LOG 192: "a new study, to be declared first and put to the owner".
   - **What was extinguished is an applied lead for a published method (GMR), not a CRR idea.** The lesson about
     comparators was carried forward: RRM adopted ER-20 and a DECOY must-fail (AGENT_LOG 194 (3)).
2. **RRM-PA: killed at a lower level than the claim it seemed to bear on.**
   - The owner's form passed all four of its conditions. The gate closed on the other form (`worlds.txt:41-47`).
   - Not extinguished: RRM2 re-declared RRM-1 alone 43 minutes later (`a2719f0`), with part 1 disclosed as not blind
     (`DECLARATION_2.md:75`).
3. **RRM2 T1–T3: the transport idea was gated in a regime where it could not act.**
   - The claim is about drift. The learner barely drifted (stale error 0.1197 against decoy 6.6796 on POS FT;
     `t1_diag.txt:3-5`).
   - T7 (post hoc) tried to raise drift through epochs per task, which gave little: 0.0113 → 0.0208 (FT, POS;
     `t7_drift.txt:40`). No other learner (deeper, convolutional, image data) was tried; the SEC1 MLP was the only learner
     in the lineage.
   - **Was transport ever tested where drift is large?** Only in three places:
     - (i) synthetic worlds with no learner (T4, ε = 0.1: gains up to +27.63);
     - (ii) post hoc SEEN report lines (T1 SEEN, T7 SEEN: relative drift up to 0.8747 on har FT, `t7_seen.txt:63`);
     - (iii) CPL1 with **current-task** anchors, where it hurt.
   - **Kept-anchor transport was never gated in a learner with large drift.** The per-carrier SEEN structure (O-MEM-5)
     sits under a 30-carrier aggregate ("split"). That aggregate is dominated by carriers with nothing to fix: ORACLE
     beats STALE by a step on only 4/32 (`cpl_phase_a.txt:175`).
   - This is the clearest case in these lineages of a lead closed below the level of its claim. It is a non-CRR
     engineering lead.
4. **Part W override.**
   - The investigator discarded anchor provenance as "not a predicate of P5" (`DECLARATION_2.md:120`).
   - CPL1's review later found anchor provenance to be the variable that set the sign (AGENT_LOG 229).
   - Both facts stand. The override did not decide the stop (see the table above).
5. **CPL1.**
   - Not extinguished below its level: the declared exemplar-free rule forced current-task anchors, and the review
     checked the alternative.
   - "T7-style anchors would not flip G-DRIFT (K-MNIST +0.50 within a step) and would break the exemplar-free rule"
     (AGENT_LOG 229).

### 7. Question-10 evidence (L-MEM)

**Speed.** Seven gate evaluations across five declarations ran inside about 9 hours on one day.
- **Auditor's count (derived):** RQM runs 1 and 2, RRM part 1, RRM2 T1, T2 and T3, and CPL1; from the commit table above.
- The time from declaration to closure was 4–36 minutes for all but CPL1.

**No exploratory or pilot stage between the idea and the gate.** Each defect was found by the gate itself:
- the unlearnable rings (AGENT_LOG 191);
- the uncloseable matched-ER criterion (AGENT_LOG 192);
- the no-drift learner (AGENT_LOG 199);
- the rotated world that "barely drifts" (`cpl_phase_a.txt:195`).

None of these needed held-out data to find. A short headroom pilot on SEEN or synthetic data, logged before the gate was
frozen, would have found each one.

**The protocol's own rules were cited to stop development:**
- "Rejected: a third negative stream tuned until IGR loses (gate-shopping, CLAUDE.md section 10)" (AGENT_LOG 192);
- "Rejected: continuing with RRM-1 alone under this declaration (a declared gate changed after its result, CLAUDE.md
  section 10)" (AGENT_LOG 195);
- "Rejected: re-running T2 at a larger E and calling it the gate" (AGENT_LOG 199).

R12 (`CLAUDE.md:161-163`) was written for Phase-A gates on CRR hypotheses. Here it was applied to engineering candidates
that the record itself labels "not a CRR rule" (`DEV_DECLARATION.md:105-106`; `Relational_Reference_Memory/DECLARATION.md:166-167`).

**But the protocol also permitted re-declaration quickly**, and that was used:
- RRM2 came 43 minutes after RRM-PA;
- T7 was a declared post hoc report-only exploration (`DECLARATION_3.md:10-13`);
- RQM run 2 followed a declared post hoc amendment.

So exploration was not forbidden. It was confined to report-only lines with no development loop, on one learner, and
never reached the regime where the idea had leverage.

**Design iterations on SEEN data before any hash: zero toward a prereg.** No L-MEM idea reached a development gate. The
SEEN work was T1 SEEN and T7 SEEN, reports only (AGENT_LOG 226).

**What the gates caught that mattered.**
- RQM-A caught a criterion that would have made any real-data PASS uninformative (`PHASE_A.md:29-30`).
- T2's G-CANFAIL caught a weak DECOY on NEG2.

These are the merciless parts working as intended.

### 8. Open questions for Phoenix (L-MEM)

**May explore** (exploratory, labelled as the published family, never as CRR):
- **A learner with real feature drift.**
  - A deeper or convolutional backbone on image streams, or the four SEEN carriers where ORACLE beats STALE by a step
    (har, isolet, Indian_pines, Kuzushiji-MNIST).
  - On it: kept-anchor versus current-task-anchor transport, ridge versus HopDC kernel, against STALE, ORACLE and ER-20.
  - First establish headroom (ORACLE − STALE) as a pilot.
- **IGR (GMR) against JOINT and against ER at a fixed realistic budget** on SEEN carriers, with a negative stream on which
  Gaussians are wrong in every direction.
- **Exemplar-free NCM on stored statistics against ER-20** as an applied privacy benchmark (O-MEM-6).
- **Anchor provenance** as a measured variable (O-MEM-5).

**Must never claim:**
- That CRR found, predicted or is evidenced by:
  - input-space generative replay (GMR/DGR);
  - anchor-drift transport (HopDC, SLDC, transport keys);
  - NCM over a softmax head (iCaRL/SDC);
  - the "input beats feature space" sign (drift literature).
- That RRM-1's part-1 pass is evidence. It is exact by construction on SHARED/ROT, synthetic, no learner.
- That any L-MEM result reached a rung above R4/R5, or that "the HopDC finding" (PROMPT_LOG 257) is a finding of this
  repository. HopDC is a published method (arXiv 2602.00144 v1). The repository's comparisons with it are report lines.
- That a closed L-MEM gate falsifies a CRR principle. No CRR.md hypothesis was under test.

---

## L-CLK — own-clock (arc-clocked) optimisation and consolidation

### 1. Trajectory (dated, cited)

| when (commit, UTC) | step | source |
|---|---|---|
| 2026-09-25 02:48Z (prompt) | "Treat crr as falsifiable metaphysics and run the mathematical principles through the forever paper mathematics" | PROMPT_LOG 180 |
| 2026-09-25 02:51:29 `7760b88` → 02:56:06 `37d3616` | FOREVER × CRR declaration F1–F6; Amendment 1 after a crash; 11 labels hold, 5 fail | `FOREVER_AND_CRR.md:39-58`; AGENT_LOG 133 |
| 2026-09-25 03:01Z (prompt) → 03:01:52 `359d850` | Comparative battery declared (7 worlds, 13 arms, a clock gate) | PROMPT_LOG 181; `DECLARATION_2.md`; AGENT_LOG 134 |
| 03:05:39 `1d61614` | Amendment 1 (headroom), calibrated on unscored seed 999 with baselines only | AGENT_LOG 134 |
| 03:12:17 `37f6655` | Clock gate **CLOSED**; "ARC-R is not licensed" | `COMPARATIVE.md:68-71`; `comparative.txt:134` |
| 2026-09-25 19:10:26 `4b3b995` → 19:17:21 `9e9b5be` | clock_cut: the own-clock cut against Wald. Gate open; F1 REDUNDANT-DOMAIN; C2 MIXED, fragile; no candidate | `clock_cut.txt:5-27, 54-55`; AGENT_LOG 146 |
| 2026-09-25/26 (SOTA1, L-EQ's study) | SOTA1-3:crr-stepclock, held-out: **FAIL** (TIE) | ledger SOTA1-3:crr-stepclock |
| 2026-09-30 05:02Z (prompt) | "find the actual big bottlenecks so we can put crr to the proper test on things that are not currently possible" | PROMPT_LOG 252 |
| 05:03:55 `a7fa3fe` | OB1 declaration: open first, disagreement not restatement, prior art before code | `Open_Bottlenecks/DECLARATION.md`; AGENT_LOG 201 |
| 05:24:24 `1e4a630` | Stage 2: DISAGREES 7 ("the clock"), RESTATES 6, SILENT 2, set aside 4 | `CRR_READING.md:47-54`; AGENT_LOG 202 |
| 05:48:05 `c4da07e` | Stage 3: C1, C2, C3 each PARTLY REDUNDANT; the missing part in each is the arc as the index | `CRR_READING.md:103-105`; AGENT_LOG 203 |
| 05:49:06 `39e86ce` → 05:54:58 `0214108` | C1 declared → **GATE CLOSED** on G-TIME S2 | `C1_DECLARATION.md`; ledger **OB1-C1-A**; AGENT_LOG 204, 205 |
| 06:02Z (prompt) | "We should run a consolidation" | PROMPT_LOG 254 |
| 06:05:22 `38c87e3` → 06:19:47 `e3f4ca5` | C3 declared → **GATE CLOSED** (G-MATTER and G-TIMING fail) | `C3_DECLARATION.md`; ledger **OB1-C3-A**; AGENT_LOG 208, 209 |
| — | C2 (arc-triggered refresh): declared "next in the declared order" (AGENT_LOG 205). No later declaration, run or recorded drop decision was found (auditor's grep of `notebook/AGENT_LOG.md` and `Open_Bottlenecks/` for C2) | — |

**Auditor's count (derived) from commit times:**
- C1: ≈ 6 min from declaration to closure.
- C3: ≈ 14 min.
- The FOREVER comparative battery: ≈ 10 min from declaration to the closed gate.
- No L-CLK idea except SOTA1's own-clock slow-model arm reached a pre-registration.

### 2. Operationalisations and added assumptions

**Core principle.** "change has its own clock" (`theory/CRR.md:196`), with:
- D2, coherence as the arc since the last cut (`:76`);
- D6, the arc for a parametric model (`:233`);
- A1′, the own unit (`:55`).

Its only falsifiable statement in CRR.md is **H-L5** (`:200`): the arc between a system's own boundary events is more
regular than clock time. OB1 says plainly that its use is "a different use from H-L5's regularity claim"
(`Open_Bottlenecks/CRR_READING.md:20-21`).

**Added assumption common to all of L-CLK:** an arc-indexed *design rule* (a trigger, a decay or a schedule) should beat a
step-indexed one. CRR.md does not state this. It is an extension of the slogan, and A3's cut has no rotor here (O3).

The operationalisations, with the added assumptions specific to each:

**(a) FOREVER F1–F6** (`FOREVER_AND_CRR.md:16-26`). FOREVER's τ is D2's arc with a Euclidean metric, reset at the cut.
- Tested as mathematical properties (Fisher invariance F1; blindness to null movement F2; the step bound F4b), not
  accuracy (`:69`: "These are properties, not gains in accuracy").

**(b) The comparative battery** (`COMPARATIVE.md`). The Fisher arc (C1), A1′'s robust unit (C2), the chord (C3) and others
are swapped into FOREVER.
- Added assumption: at a fixed replay budget, *when* replay fires has leverage on accuracy in these miniatures.
- Added assumption: the "positive control" is P1 itself, "C1 reads AHEAD in W2, the world built to carry the effect"
  (`DECLARATION_2.md:77, 89`).

**(c) clock_cut** (`Energy Design Principle/DECLARATION_2.md:10-22, 94-107`). The own-clock stopping rule (S3), measured
against Wald's SPRT (S2) and step budgets.
- Added assumption: the CRR-proper part is S3 against S2 (C2), separated from the inherited "content beats the clock"
  (F1, REDUNDANT-DOMAIN by construction).

**(d) OB1-C1** (`C1_DECLARATION.md:44-50`). Adam's β^(r_t), with r_t = a_t/ā_t and a_t = √(2·KL̄) on the previous and
current batch.
- Added assumption: the stability gap is measured by a 30-step minimum after a switch, including on S1, which has no
  replay (`:32-37`).
  - **This failed as a design**: "S1's metric is a design defect of the declaration" (`C1_PHASE_A.md`, file lines 36-38).
- Added assumption: timing must beat a shuffled decoy (G-TIME, `C1_DECLARATION.md:66`).
  - **This failed on S2.**

**(e) OB1-C3** (`C3_DECLARATION.md:23-58`). Consolidation (online-EWC anchor plus diagonal window Fisher) is triggered by
the accumulated arc, against the chord (TIDE's quantity), loss CUSUM, count, random, none and oracle.
- Added assumptions:
  - an MLP, a rotated-domain blurry stream, a diagonal-Fisher penalty, and **SEC4's clip at κ/(lr·λ), κ = 0.5**
    (`C3_DECLARATION.md:41`);
  - λ calibrated on one seed (`:55-58`).
- **The failure:** consolidation itself had no effect. Every arm scored 28–30 % (`C3_PHASE_A.md`, file lines 16-24).

**(f) SOTA1-3:crr-stepclock** (prereg/sota1). The slow model runs on the own clock at "the own-clock rate λ = 0.05
(FOREVER's)" (`prereg/sota1/PREREG.md:69`).
- "Named but not swept (compute): τ and the own-clock λ" (`:72`).
- The surrogate already read TIE: "stepclock −0.12: all TIE ... retained" (`:117`).

### 3. Results (verbatim verdicts, by row id)

- **OB1-C1-A**: "GATE CLOSED (C1 stops, R12); on S2 the gain is the distribution of the decays, not their timing; on S1 a
  published signal (MECTA-M) is ahead, and S1's metric measures forgetting onset (no replay), a declared-design defect".
  - "G-POS holds (S1 -61.4949, S2 -3.6288); G-TIME holds on S1 (-44.7388) and FAILS on S2 (ARC - SHUF -0.8528, step
    1.0000); G-DISC holds on S2 (KOURK -4.0970, MECTA-M -7.1405), not on S1 (MECTA-M ahead by 8.4452); G-HARM holds
    (+0.5351); G-FAIL holds (ORACLE - STEP -58.1425)".
- **OB1-C3-A**: "GATE CLOSED (C3 stops, R12): consolidation has no effect in the declared stream, so the arc-against-chord
  contest is not scored; a design failure of the declaration".
  - "G-MATTER FAILS (ORACLE - NONE +0.7224, step 1.0000); G-TIMING FAILS (ORACLE - RAND +0.1338, step 1.0000)"; reported:
    "ARC's consolidation times align with the hidden switches (e.g. 77/148/221/291 against 72/144/216/288), ARC - CHORD
    +0.4950 (inside a step)".
- **SOTA1-3:crr-stepclock** (held-out, strongly anchored): "D2/A1' reading: full AHEAD of the arm whose slow model runs on
  the step clock". Observed "d = +0.126667 (+0.13), step 1.0000; per seed +0.22 / +0.03 / +0.13 -> TIE", "3/3 seeds
  ahead", verdict "**FAIL**".
- **Non-ledger (R4):**
  - FOREVER clock gate: "CLOSED" (`COMPARATIVE.md:68`); "C1 Fisher arc ... TIE" in 7 of 7 (`:57`).
  - F1–F6: "11 labels hold ... 5 fail" (`FOREVER_AND_CRR.md:55-57`).
  - clock_cut: "GATE OPEN" (`clock_cut.txt:11`); "F1 ... REDUNDANT-DOMAIN (Wald's sequential test) whatever the outcome"
    (`:18`); "C2 forecast was TIE: W2 MIXED, W3 MIXED; PROSPECTIVE CANDIDATE ... : no" (`:27`); "FRAGILE (> 1 flip)"
    (`:55`).

### 4. Four-layer tables for the key observations

**O-CLK-1. FOREVER's scheduler has CRR's shape** (`FOREVER_AND_CRR.md:13-26, 61-63`).

| layer | content |
|---|---|
| observed | τ_t = Σ‖Θ_t − Θ_{t−1}‖₂, reset at each task; τ_day an own unit. FOREVER's paper reports model time ahead of step calibration "by 1.2 OP and 1.1 BWT" (the paper's numbers, `:22, 84`) |
| CRR interpretation | "the first external support in continual learning for 'change has its own clock'" (`:33-34`) |
| ordinary explanation | FOREVER "was built from Ebbinghaus's forgetting curve, not from CRR" (`:13`). Spaced repetition indexed by update magnitude is an independent design. In the miniatures, "Its gain here comes from the anchored replay, not from its clock" and "The model-time clock did not help where it was built to" (`COMPARATIVE.md:84-92`) |
| what would distinguish | ARC-R as designed (`FOREVER_AND_CRR.md:87-95`). Under R12 it is "not licensed" after the synthetic gate closed (`:97-100`) |

**O-CLK-2. Fisher-clock properties: invariance and blindness to null movement** (F1, F2).

| layer | content |
|---|---|
| observed | Fisher arc invariant to the LoRA rescaling (relative 9.554e-14). Euclidean arc 4.989435 → 10.113847; noise on null weights moves FOREVER's second trigger from 208 to 65 while the Fisher triggers are unchanged (`FOREVER_AND_CRR.md:41-44`) |
| CRR interpretation | D2's metric is "change in what the system says" |
| ordinary explanation | "standard (Čencov)" (`:41`). An information-geometry property, not CRR's (CLAUDE.md §7: "the Fisher–Rao metric, arc, chord and surplus are information geometry's, not CRR's") |
| what would distinguish | An accuracy consequence. The comparative found none: "The Fisher metric's properties are real mathematics (F1, F2) with no accuracy consequence at a fixed replay budget" (`COMPARATIVE.md:115-116`) |

**O-CLK-3. The clock gate's positive control and replay-timing leverage** (`comparative.txt:21-36, 134`).

| layer | content |
|---|---|
| observed | In W2 (null movement), C1 Fisher arc −0.71 TIE. Fixed-interval replay B2 −0.19 TIE and step clock B3 +0.23 TIE against FOREVER (`comparative.txt:25-26, 28`). Gate: "C1 AHEAD in W2 (must pass): False -> GATE CLOSED" (`:134`) |
| CRR interpretation | Under the protocol: the clock claim failed its positive control |
| ordinary explanation | **Auditor's reading:** in W2, replay timing had no measurable leverage. Fixed-interval, step and Euclidean schedules all tie. A better clock could not show, whatever its merit. The "positive control" was the CRR prediction itself (P1, `DECLARATION_2.md:89`), not an independent check that timing matters |
| what would distinguish | A world in which a known-correct schedule (an oracle at the true switches) beats a fixed-interval schedule by more than a step, so that timing has leverage. Only then does Fisher arc against Euclidean arc mean anything. C3 later built exactly such a gate (G-TIMING) and it closed too (OB1-C3-A) |

**O-CLK-4. The own-clock cut is Wald** (`clock_cut.txt`).

| layer | content |
|---|---|
| observed | Gate OPEN; F1 (S3 against S1b) BETTER in W1 and W2, TIE in W3: "does not hold in every world -> REDUNDANT-DOMAIN" (`:15-18`). C1 (must-fail) holds; C2 MIXED in W2 and W3; four comparisons FRAGILE (`:19-27, 54-55`) |
| CRR interpretation | An own-clock cut stops when the belief has settled (D2) |
| ordinary explanation | Wald's sequential probability ratio test (`DECLARATION_2.md:15-22`). The arc rule is "a function of successive posteriors, as the confidence rule is" (`:103`) |
| what would distinguish | S3 BETTER than S2 in W3 but not W1. It did not occur: "PROSPECTIVE CANDIDATE ... : no" (`clock_cut.txt:27`) |

**O-CLK-5. C1: arc-clocked Adam reduces the dip, but timing does not carry it on S2** (`c1_phase_a.txt`).

| layer | content |
|---|---|
| observed | S2: avg-SG STEP 3.06, ARC −0.57, SHUF 0.28 (`:18-20`). ARC's median r 0.628 (`:25`). S1: ARC 8.70, SHUF 53.44, STEP 70.20, MECTA-M 0.26, with final accuracy MECTA-M 43.96 against ARC 27.35 (`:7-11`) |
| CRR interpretation | Index the optimiser by the learner's own change: the arc jumps at a switch and flushes stale moments |
| ordinary explanation | On S2, the gain is a lower effective β (median r < 1 means longer memory on most steps): "the gain comes from the **distribution** of ARC's decays, not from their **timing**" (`C1_PHASE_A.md`, file lines 30-32). That is a hyperparameter effect. On S1, a published hidden-statistics signal (MECTA) does better, and the metric measures forgetting onset, not the transient gap |
| what would distinguish | A stability-gap protocol with replay (as h1-B6 uses), ARC against SHUF **and** against STEP with β retuned to ARC's mean effective decay. Only a timing effect beyond both would be CRR-specific. Not run |

**O-CLK-6. C3: the arc's consolidation times line up with the hidden switches** (`c3_phase_a.txt`, file lines 19, 34).

| layer | content |
|---|---|
| observed | BLURRY: ARC fired at "77,148,221,291 \| 71,143,218,289 \| 75,144,213,281,354 \| 68,139,215,286 \| 74,143,219,290" against switches 72/144/216/288. ABRUPT: "80,155,231,302 \| 75,141,217,293 \| 82,157,231,306 \| 73,141,213,291 \| 75,144,220,295". CHORD and LOSS fired "later and less regularly" (`C3_PHASE_A.md`, file lines 28-31) |
| CRR interpretation | The own arc as a change detector: "The arc's alignment with switches is the one sign here worth a follow-up" (`C3_PHASE_A.md`, file line 42) |
| ordinary explanation | **Auditor's reading; not tested in the record.** The ARC threshold was calibrated to fire 4 times on seed 100 (`c3_phase_a.txt`, file line 6), on a 360-step stream with five equally spaced domains. A near-constant arc rate would then also fire at roughly 72–90-step spacing. In ABRUPT, seed 0's lags behind the switches are 8, 11, 15, 14 and seed 2's are 10, 13, 15, 18 (**auditor's count (derived)**: firing step minus 72/144/216/288). The lag grows across a run, which is what a slightly slow constant rate would produce. Seed 3 (1, −3, −3, 3) fits switch-tracking better. Published change detectors from the learner's own signals also exist (`C3_PHASE_A.md`, file lines 33-34) |
| what would distinguish | A constant-rate null: ARC's own per-step arcs shuffled in time (C1's SHUF design), or domains of unequal length, so that regular spacing and switch-tracking predict different firing times. Then the published detectors, as `C3_PHASE_A.md` (file lines 42-44) already proposes |

**O-CLK-7. Own clock against step clock for a slow model, held out** (SOTA1-3:crr-stepclock).

| layer | content |
|---|---|
| observed | d = +0.126667, step 1.0000, TIE → FAIL; the surrogate also TIE (−0.12) (`prereg/sota1/PREREG.md:117`) |
| CRR interpretation | D2/A1′: the slow model should follow the learner's own change |
| ordinary explanation | The EMA slow model is insensitive to whether its rate is indexed by steps or by own change, at λ = 0.05 (FOREVER's value, not swept) |
| what would distinguish | A world in which the per-step arc varies widely, so the two clocks diverge, with λ swept. The record has no measure of how far the two clocks diverged in SOTA1 (not found by the auditor) |

### 5. Salvage classification (A–G)

| item | categories | core principle → operationalisation → test → failure; the highest level reached |
|---|---|---|
| FOREVER F1–F6 | **C** (properties are standard information geometry; F4c: FOREVER's weight reduces to a constant; F4d: the rule is behind a tuned constant) + **D** (F3a: the declaration's approximation was wrong; F5c: the clip masks a channel) | Mathematical properties at R4; no accuracy claim. F4d reaches H-EQ's "equal pull is at least as good" in one quadratic world (L-EQ's territory) |
| Comparative clock gate | **B + E** | "change has its own clock" (`CRR.md:196`) → Fisher-arc replay scheduler in FOREVER (D2/D6) → W2 positive control → TIE. The highest level reached is **one operationalisation in miniatures where timing showed no leverage** (O-CLK-3). It does not reach H-L5 |
| A1′ robust unit lead (comparative C2, +1.74 in W6) | **F** (a near-win in one cell, just over the step) | One world; "not gated" (`COMPARATIVE.md:104`). It was later folded into SOTA1's own-clock arm, which tied (O-CLK-7) |
| clock_cut | **C** (reduces to Wald) | The CRR-proper comparison (C2) is MIXED and FRAGILE; no candidate (`clock_cut.txt:27, 55`) |
| OB1-C1-A | **B** (the operationalisation's timing claim failed on S2) + **C** (a published signal ahead on S1; the S2 gain reduces to the decay distribution, a hyperparameter) + **D** (S1 metric defect) | own clock (D6) → Adam β^(a_t/ā), arc on the batch → G-TIME S2 → FAIL. The highest level is **one operationalisation on synthetic streams (R4)**. Within that operationalisation the timing claim was tested fairly and lost. That is genuine pressure on "own-change timing of optimiser moments", not on CRR.md |
| OB1-C3-A | **D** (design: "consolidation has no effect"); **E** for the arc-against-chord question (not decided); **F** for the alignment observation, weakened by O-CLK-6's confound | own arc (D2/D6) as a consolidation clock → arc-triggered online EWC → G-MATTER / G-TIMING → both FAIL. **Instrument only.** Nothing about the arc was tested. The ledger's wording "a design failure of the declaration" is accurate. The record names one cause: a diagonal penalty under input rotations (`C3_PHASE_A.md`, file lines 21-22). **Untested alternative (auditor's reading):** the declared clip, Ω ≤ κ/(lr·λ) (`C3_DECLARATION.md:41`), bounds how strongly any consolidation can hold. The record does not examine it |
| OB1-C2 | none: never run, and no stop decision recorded | — |
| SOTA1-3:crr-stepclock | **A** (a fair held-out test; FAIL as TIE) | own clock → slow-model EMA at λ = 0.05 → held-out Split-CIFAR-100 → TIE. The highest level is **one operationalisation and implementation (λ not swept)**. It is the strongest negative evidence in L-CLK, and it is still not H-L5 |
| Connection to H-L5 | — | H-L5 itself fails on real carriers (MEAS2, CARD; `Open_Bottlenecks/CRR_READING.md:16-18`, L-L5's lineage). OB1 took that as a low prior. L-CLK's results add no evidence for or against H-L5 as stated |

**Is any of L-CLK a G?** No.

### 6. Extinguished-lead check (L-CLK)

1. **OB1-C3: stopped by R12 before a developed variant existed.**
   - The gate was declared without first checking that consolidation does anything in this stream.
   - When it did not, the contest was not scored, and "an amended stream run now to reopen the gate" was rejected as "a
     post hoc redesign after the result; it needs its own declaration and the owner's go-ahead" (AGENT_LOG 209).
   - No new declaration followed. **The arc-against-chord question is open, not answered.** It was closed at the
     instrument level, below the claim.
2. **C2: never run, never formally dropped.** An undeveloped candidate left without a record.
3. **The comparative clock gate (ARC-R).** The positive control coincided with the prediction, and replay timing showed
   no leverage (O-CLK-3), so "not licensed" rests partly on an instrument limit. But the own-clock idea did later get a
   held-out test in SOTA1 (O-CLK-7), and it failed. **Net: not extinguished prematurely overall.** It was tested again, in
   another form, and lost.
4. **C1** was answered within its operationalisation. "A corrected S1 is not run, because it could not reopen the gate"
   (AGENT_LOG 205) is logically correct: G-TIME S2 is independent of S1. Not extinguished below its level. The obvious
   development step was never declared: replay-based S1 plus a β-retuned STEP control.

### 7. Question-10 evidence (L-CLK)

**OB1 changed the process deliberately.** "Observed issue: in RQM and RRM the design was derived first and the prior art
searched after, and each design was published" (AGENT_LOG 201).
- The new order: open bottleneck first, then disagreement, then prior art, then code (`Open_Bottlenecks/DECLARATION.md:6-25`).
- This is a protocol improvement that came out of the L-MEM failures. It aims at *novelty*, not development.

**Gates were declared and evaluated within minutes,** with no pilot (≈ 6 min for C1, ≈ 14 min for C3). In C3 the gate's
own first conditions, G-MATTER and G-TIMING, are pilot questions: does the action matter, and does timing matter? They were
frozen into the gate instead of being checked before the contest was designed. Both failed, and R12 then stopped the line.

**The FOREVER battery shows the protocol allowing a headroom repair.**
- The declared generator gave "99.3-100 with no forgetting"; a calibration "on unscored seed 999 with baselines only"
  fixed it before scoring (AGENT_LOG 134).
- So a pilot-like step *was* permitted when it was declared as an amendment before scoring. The same move was not taken
  for C3 or for the RRM2 learner.

**R12 and CLAUDE.md §10 were cited to stop:**
- C1: "Rejected: dropping G-TIME S2 or re-running with a changed S1 to open the gate (gate-shopping, CLAUDE.md section 10)"
  (AGENT_LOG 205);
- C3: AGENT_LOG 209, quoted above.

**Pace and supervision.** OB1 ran overnight, with the owner asleep (PROMPT_LOG 250). Prompts 252 and 254 set direction.
Each candidate had one shot at a synthetic gate built in the same session.

**Counter-evidence: the protocol did not stop the own-clock idea from reaching a held-out test.** SOTA1 pre-registered it,
and it failed fairly (O-CLK-7). The clock_cut check was also designed with an inherited/proper split and a must-fail
control, and it gave an informative reduction (Wald).

### 8. Open questions for Phoenix (L-CLK)

**May explore** (exploratory):
- **The arc as a change detector**, with a constant-rate null (shuffled per-step arcs, unequal domain lengths) and against
  published detectors, before any downstream claim (`C3_PHASE_A.md`, file lines 42-44).
- **Consolidation timing in a stream where consolidation demonstrably matters.** Pilot G-MATTER and G-TIMING first, then
  freeze the arc-against-chord contest. Report the clip's effect on penalty strength.
- **C1 on a replay-based stability-gap protocol,** with STEP retuned to ARC's effective decay as the control that isolates
  timing.
- **C2** (arc-triggered refresh), if anyone still wants it. The prior is low (AGENT_LOG 202).
- **The SOTA1 own-clock arm with λ swept,** in a regime where per-step arc varies widely, recording how far the two clocks
  diverge.

**Must never claim:**
- That FOREVER is evidence for CRR. It was built independently from Ebbinghaus (`FOREVER_AND_CRR.md:13`), and its clock
  did not help in the miniatures (`COMPARATIVE.md:89-92`).
- That the Fisher clock's invariance or null-movement blindness is a CRR result (Čencov; `FOREVER_AND_CRR.md:41`).
- That "content beats the clock" or the own-clock cut is CRR's. It is Wald (`clock_cut.txt:18`).
- That ARC "detects boundaries" (O-CLK-6 has an unexcluded constant-rate confound).
- That any own-clock design rule beat a step clock anywhere above R4. The only held-out row is SOTA1-3:crr-stepclock,
  **FAIL**.
- That these results bear on H-L5 in either direction. They are different claims (`Open_Bottlenecks/CRR_READING.md:20-21`).

---

## Answers to request questions 1–9 (both lineages)

1. **Initial ideas.**
   - L-MEM: replay-quality class-IL memory without stored data (PROMPT_LOG 245). Then the owner's relational
     "first object" memory (PROMPT_LOG 248). Then coupling with SEC4 and the pause (PROMPT_LOG 257).
   - L-CLK: "change has its own clock" carried into learners. First through FOREVER (PROMPT_LOG 180–181), then as the one
     repeated point of disagreement with the frontier (`Open_Bottlenecks/CRR_READING.md:14-21`).
2. **Operationalisations.** L-MEM: IGR/FGR; RRM-1/RRM-A ridge transport; HopDC-type current-task transport. L-CLK:
   FOREVER swaps; the own-clock stopping rule; arc-clocked Adam; arc-triggered online-EWC consolidation; an own-clock
   slow-model EMA (§2 of each lineage).
3. **Assumptions added to make them testable:**
   - a task boundary is a cut (outside A3's rotor domain; O3 open);
   - the EPS / Proposition 7 transposition to memory;
   - the matched-memory ER criterion;
   - conjunctive gates across two forms;
   - the SEC1 MLP as a learner whose features drift;
   - the exemplar-free rule forcing current-task anchors;
   - a positive control equal to the prediction (FOREVER P1);
   - a 30-step dip metric without replay (C1 S1);
   - a consolidation action with leverage (C3);
   - λ = 0.05 unswept (SOTA1).
4. **Which added assumptions became the thing that failed:**
   - the matched-memory criterion (RQM-A);
   - the two-form conjunction (RRM-PA);
   - "the learner's features drift" (RRM2-T1..T3);
   - current-task anchors (CPL1-A);
   - consolidation having an effect (OB1-C3-A);
   - the S1 dip metric (OB1-C1-A, partly);
   - timing leverage in W2 (comparative clock gate; auditor's reading, O-CLK-3).
5. **Failures that reached the underlying CRR claim:** none in these lineages reach a CRR.md hypothesis. The closest are
   SOTA1-3:crr-stepclock (held-out, one operationalisation of the own clock) and OB1-C1-A's G-TIME S2 (synthetic, one
   operationalisation). Both are pressure on "own-change indexing as a design rule in learners". That rule is an
   extension of the slogan at `theory/CRR.md:196`, not a stated hypothesis.
6. **Failures that reached only an implementation, an instrument or a translation:** RQM-A, RRM-PA, RRM2-T1/T2/T3,
   OB1-C3-A, the C1 S1 defect, and the comparative clock gate (partly).
   - **Auditor's count (derived), reading the eight ledger verdict texts** (RQM-A, RRM-PA, RRM2-T1, RRM2-T2, RRM2-T3,
     OB1-C1-A, OB1-C3-A, CPL1-A):
     - 5 of 8 close mainly on instrument, design or no-headroom grounds: RQM-A, RRM2-T1, RRM2-T2, RRM2-T3, OB1-C3-A;
     - 3 of 8 carry substantive negative content for one operationalisation: OB1-C1-A, CPL1-A, and RRM-PA for the RRM-A
       form only.
7. **Interesting despite failing promotion:**
   - O-MEM-5, anchor provenance on the drift-rich SEEN carriers;
   - O-MEM-1, IGR within 0.4013 of JOINT on POS;
   - O-MEM-3's UNSHARED residual (52.64 against stale 10.84);
   - O-MEM-6, exemplar-free NCM level with ER-20;
   - O-MEM-4, the recurring "forgetting is in the head" (also SOTA1 pred-fast);
   - O-CLK-5, the large S1 timing effect (ARC 8.70 against SHUF 53.44), beaten by MECTA-M;
   - O-CLK-6, ARC alignment, with its confound;
   - the comparative's A1′ cell (+1.74).
8. **Apparent successes that reduced to known mathematics:**
   - IGR → GMR/DGR;
   - RRM transport → HopDC / SLDC / transport keys;
   - FOREVER's τ → D2 with a Euclidean metric (and FOREVER predates its CRR reading);
   - Fisher-clock invariance → Čencov;
   - the own-clock cut → Wald's SPRT;
   - C1's S2 gain → a longer effective moment memory (decay distribution);
   - the CPL1 pause → checkpoint/resume state closure;
   - NCM over the head → iCaRL/SDC;
   - input-beats-feature-space → the drift literature.
9. **Apparent failures that were infrastructure, identifiability or design:**
   - the RQM rings (unlearnable), and the matched-ER criterion (uncloseable);
   - RRM2's no-drift learner (unidentifiable: stale error ≈ 0.12–0.26 against decoy ≈ 3–7);
   - T2's G-CANFAIL on NEG2;
   - CPL1's rotated world (0.0191 against a SEEN median of 0.0567);
   - C3's null consolidation;
   - C1's S1 metric;
   - FOREVER's original generator with no headroom (repaired), F3a (an approximation error) and F5c (masked by the clip).
   - Also a record-keeping point:
     - `Epistemic_Review/checks/ladder.py:197-198` tests for "(N)" before "synthetic", so purely synthetic Phase-A rows
       (RQM-A, RRM-PA, OB1-C1-A, OB1-C3-A) print as "seen" in `ladder.txt:252-259`, while SAL-A and STAKE1-A print as
       "synthetic" (`:102, :222`).
     - A labelling inconsistency only. It changes no verdict.
