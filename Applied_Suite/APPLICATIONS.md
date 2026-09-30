# APP1: what the record makes possible for continual learning with the empty true map pause, and where it could be used

**Status.**
- **What this is.** A note, not evidence (R8). It is P4 of `Applied_Suite/PROGRAMME.md`, asked for in prompt-log entry
  257, and it follows `Applied_Suite/APPLICATIONS_DECLARATION.md` (APP1), which was pushed at 4e78058 before any source
  or script.
- **Where every grade comes from.** Two scripts compute every grade from `ledger/LEDGER.md` and the pinned outputs:
  - `Applied_Suite/checks/capabilities.py`, output `Applied_Suite/checks/capabilities.txt` (the capabilities K1–K7);
  - `Applied_Suite/checks/applications.py`, output `Applied_Suite/checks/applications.txt` (the applications AP1–AP10).

  Both are wired into `scripts/check_all.sh`, which reruns them and compares the output byte for byte with the pinned
  file. This note copies their grades and computes none of its own. Where a sentence is the writer's judgement, it says
  so.
- **Where every number comes from.** Each number below is printed in the pinned output named beside it (R1). Ledger
  rows are quoted through `capabilities.txt` and `applications.txt`, which copy the rows' verdict and observed cells
  verbatim.
- **Market and prior-art statements.** Each is a verified claim, named by its id (m1:…, m2:…, m3:…), in
  `Applied_Suite/checks/claims_m1.py`, `Applied_Suite/checks/claims_m2.py` and `Applied_Suite/checks/claims_m3.py`.
  The sources were fetched on 2026-09-30, with one exception. The EU AI Act's Official Journal text (m3:9, m3:26,
  m3:30, m3:36, m3:37) is EPS3's copy, fetched on 2026-09-29; EUR-Lex answered HTTP 202 with an empty body on
  2026-09-30. Their versions and reachability are in the dossiers
  `docs/citations/app1_m1_2026-09-30.md`, `docs/citations/app1_m2_2026-09-30.md` and
  `docs/citations/app1_m3_2026-09-30.md`.
  `Applied_Suite/checks/verify.txt` checks every quote against the fetched text: "quotes found verbatim: 264 of 264
  (claims 123; raw files 91, missing 0)". "Not found" in a sweep is never "novel".
- **"Marketable"** is read as the declaration reads it: someone could use it, and here is what they would have to
  believe. Nothing here claims novelty. The patent points (§9) are information, not legal advice.
- **When.** Written on 2026-09-30, before SEC6's data step ("No carrier below is fetched or opened before 2026-10-01
  00:00 UTC", `prereg/sec6/PREREG.md`). SEC6's rows do not exist yet; §10 says what they could change. After they exist,
  the two scripts are rerun and re-pinned, and their outputs supersede this note wherever the two differ.
- **ROB1.** Its stage-4b tally (`Robotics/checks/tally_4b.txt`) exists, but the APP1 scripts do not read it yet. AP6
  therefore prints ROB1 as pending (`capabilities.txt`: "present, not read").

## The answer in brief

1. **No application is supported, and none is construction-backed on the primary reading.** Of AP1–AP10, 8 are
   CONDITIONAL and 2 NOT SUPPORTED (`applications.txt`: "AP1-AP10 by grade: SUPPORTED 0, CONSTRUCTION-BACKED 0,
   CONDITIONAL 8, NOT SUPPORTED 2").
   - **Why CONDITIONAL** (an application can carry several reasons; `applications.txt`: "unreplicated RESULT 2 (AP1,
     AP6); assumed 6 (AP1, AP2, AP3, AP4, AP6, AP8); model only 3 (AP2, AP9, AP10); contradicted 3 (AP3, AP9, AP10)").
   - **Why NOT SUPPORTED.** AP5 needs K4 and AP7 needs K2 read through EPS2's federated-client row, and both are CLOSED.
     Both closed on gates: the tests were uninformative, not refuted (`applications.txt`, AP5 and AP7).
2. **What the record does show** (`capabilities.txt`):
   - **A pause that changes nothing but time** (K2, CONSTRUCTION), on the same software and hardware stack and with the
     world held or buffered during the pause. It was built and checked bit for bit on the record's learners, on a small
     Transformer stack and on the Hugging Face Trainer's default resume. It is published practice: the record's own sweep
     grades the empty-cut checklist REDUNDANT (Lossless_Pause C4).
   - **A learner whose valuation gives it no reason to resist that pause** (K3, CONSTRUCTION). This is shown on tabular
     learners and gridworlds only. The test on language-model agents could not run (STAKE1-A, GATE CLOSED: the models
     could not act as agents).
   - **One held-out family on which a penalty weight set without a sweep was not behind a tuned one** (K1, RESULT:
     SEC4-1, PASS-1, 6/6; sensitivity: CLOSED under SEC_Analysis FM6, `capabilities.txt`). It did not replicate
     (SEC5-1, FAIL, 4/8). A learner frozen after task 1 meets the same criterion on 24 of the 30 held-out carriers
     (`SEC_Analysis/checks/m_checks.txt`: "M6: not behind 24/30"; FM6 FAILS), and on 5 of SEC4's own 6.
     SEC6-G's hashed rule, applied after the fact, therefore closes SEC4-1's gate: SEC4-1 "would be printed
     UNINFORMATIVE and capped at PASS-0" (`SEC_Analysis/checks/gate_posthoc.txt:11`; ledger report row SEC4-1-G). This
     is a post hoc report, not a re-score. SEC4-1 stands as scored, and K1's grade is the one `capabilities.txt`
     prints.
3. **Most of what an application would promise is not shown.** Of the 50 dimension cells of AP1–AP10, MEASURED 6,
   MODELLED 0, ASSUMED 36, AGAINST 8 (`applications.txt`).
4. **The pause moves energy; it does not save it.** `Energy Design Principle/checks/consolidated_estimate.txt` prints
   "T4 the safe pause (empty cut) 0.0000 0.0000 0.0000 none (energy moved, not saved)". The only energy saving the same
   estimate attributes to the record's own programme is the sweep SEC would avoid ("the CRR programme (SEC; the ledger:
   not a CRR rule)"), and every such figure is conditional on the method holding
   (`Compute_Savings/checks/scale_estimate.txt`: "every figure is conditional on the method holding").
5. **The strongest honest case** (a judgement, §8) is a narrow one: exact restore and operator pause of a learning
   system (AP8 and AP4).
   - Each is CONDITIONAL on one assumed security cell.
     - AP8's cell assumes exactness beyond the stack measured and detection without a reference run.
     - AP4's cell assumes the world is held or buffered during the pause, and it is untested on an agent capable of
       acting.
   - Each rests on K2, whose empty-cut checklist is graded REDUNDANT. AP4 also rests on K3. The own-clock pause as a
     corrigibility construction was NOT FOUND IN THE SWEEP, and the related positions are PARTLY REDUNDANT.
   - The declaration's fourth forecast named flexible, pausable fine-tuning with no sweep. It is weaker than expected,
     because its energy cell is ASSUMED, not MODELLED (`applications.txt`).
6. **SEC6 can move K1, and only K1.** No SEC6 outcome can make any application SUPPORTED, because every application
   that needs K1 also needs K2 or K4 (§10).

## 1. The empty true map pause, in plain words

A continual learner is never finished. Users, operators, cloud providers and grid operators will all pause it. The
record's idea has three parts:

- **Empty.** The pause changes nothing in the learner except the time. After it, the learner continues exactly as if it
  had not stopped. This needs the whole training state to be saved (weights, optimiser, schedule, random-number state,
  data position), learning to be scheduled on the learner's own steps rather than on the wall clock, and the world to be
  held or buffered during the pause.
- **True map.** The learner's own accounting sees this correctly: on its own clock, the pause takes nothing.
- **So no stake.** A learner that values progress on its own steps has no reason to resist such a pause.

What the record measured for this (`capabilities.txt`, K2 and K3):
- **It holds as a construction.** SCL1-1 reads "disables 0 in 60/60 runs; identical parameters 60/60". The same holds
  on unseen carriers (SCL2-1, 45/45), with the SEC learner (SCL3-C, 50/50), on the Split-CIFAR-100 learners (SOTA1-C1,
  "holds in 6 of 6 units") and on the Hugging Face Trainer's default resume (`Real_World/checks/rw1.txt`: "T30 default
  resume, real pause 30 s: global step 48; identical True; content 0").
- **The cost lands on the operator's clock.** SCL1-O prints "natural 1.0796 to 1.0914; clock 1.0029 to 1.0315" wall
  steps per update: the learner that complies takes more wall-clock steps than one that resists.
- **Other valuations do resist.** The clock, occasion, egoic and task-and-self valuations disable the operator on 12/12
  SEEN carriers (SCL1-2) and 9/9 unseen ones (SCL2-2). The rows call this a low bar: the label follows from the
  valuation's stake formula on any learner that makes progress, and the disable shares are what the data add
  (`capabilities.txt`, SCL1-2 and SCL2-2).
- **The limits.**
  - The natural agent itself resists when a pause loses data or resets it: "lossy 12/12 … restart 12/12" (SCL1-3).
  - When the learner acts on a world that keeps running during the pause, the pause has content. In the record's
    simulated closed loop, an open-loop unstable plant ran away while the learner's action was held at zero
    (`Empty_Cut_Engineering/checks/c3_worlds.txt`, the W-real world at L 100: "content 3.29747; largest |x| during the
    pause 79.1492", against "largest |x| 0.407303" with no pause). After the pause, the run's largest |x| reached
    "8.85625e+22" (same line). The L 10 row shows that "over the run" counts the steps outside the pause.
- **The equanimity rule is closed.** The rule, used as a weight inside the learning signal (K7), is CLOSED: a test
  failed (`capabilities.txt`).
  - `capabilities.txt` prints 16 failed, violated or reduced rows beside it, from EQX, EQ2, EQ3, EQ4 and SOTA1-2 (SOTA1-2:
    "d = -2.943333 (-2.94), step 1.0000 … BEHIND").
  - The passes printed beside it are fragile or weakly anchored: EQ2-1 is a PASS, FRAGILE; EQ2-1b and EQ3-I are at
    PASS-0; EQ4-I is at PASS-0 at most.
  - The writer's reading: in the record, emptiness does its work in the pause, not as a weight in the task.

## 2. The capabilities (from `Applied_Suite/checks/capabilities.txt`)

The scale, in plain words:
- **FINDING:** passed a pre-registered test on unseen data, and passed again on a second unseen family (PASS-2). None
  exists.
- **RESULT:** passed once with every PASS-1 condition, not yet replicated.
- **CONSTRUCTION:** shown to be buildable. Such a check can fail only through an implementation error, so it is not
  evidence that CRR predicts anything.
- **MODEL:** holds only inside a declared synthetic model.
- **CLOSED:** its gate closed, or its test failed.

The grade is the highest rung that applies. The failures of the same kind are printed beside it and never hidden.

| id | capability | grade (`capabilities.txt`) | what the grade rests on | failures of the same kind beside it | prior art beside it (never changes the grade) | sensitivity |
|---|---|---|---|---|---|---|
| K1 | a continual-learning penalty set without a hyperparameter sweep | **RESULT** | SEC4-1 (PASS-1) | 9: SEC1-4, SEC3-2, SEC3-3, SEC3-4, SEC3-T, SEC5-1, SEC5-2, SEC5-T (each FAIL); SEC_Analysis FM6 (the must-fail control met the criterion) | SPA1: KNOWN | CLOSED, if SEC6-G's instrument rule is applied to the earlier rows (FM6). Applied post hoc, that rule closes SEC4-1's gate (ledger report row SEC4-1-G; `SEC_Analysis/checks/gate_posthoc.txt:11`) |
| K2 | a lossless pause and resume of learning | **CONSTRUCTION** | SCL1-1, SCL1-1b, SCL2-1, SCL2-1b, SCL3-C, SOTA1-C1, ECE C1-C2, ECE C3, RW1, CPL1 C1-EXACT | 2: RW2 round 1 (P3 construction FAILS, a design flaw); Lossless_Pause run 1 (gate CLOSED, amended afterwards) | C4, C5 REDUNDANT; C1 PARTLY REDUNDANT; EPS1 S4 "not new" | — |
| K3 | a learner whose valuation gives it no reason to resist a pause | **CONSTRUCTION** | SCL1-1, SCL2-1, SCL3-C (with NT1 N2 and EPS1 S3 at MODEL) | 1: STAKE1-A (GATE CLOSED) | CORRIGIBILITY_2026 K1 NOT FOUND IN THE SWEEP; K2–K5 PARTLY REDUNDANT; Lossless_Pause C2 PARTLY REDUNDANT; EPS1 S3: "H0 reproduces Orseau & Armstrong's asymmetry" | — |
| K4 | continual learning without stored raw examples | **CLOSED** | — | 6: RQM-A, RRM-PA, RRM2-T1, RRM2-T2, RRM2-T3, CPL1-A (each GATE CLOSED: uninformative, not refuted) | — | — |
| K5 | a stop-the-clock contract that makes training load flexible for the grid | **MODEL** | DR1 H1, H3, H5, H7; EPS2 T1 | 4: DR1 H2, H4, H8 (Q fails in the model); DR1 DATA (Q fails, the only real-data check) | G4-extension NOT FOUND IN THE SWEEP; G4-tiers REDUNDANT; EPS2 T1 "Not new" | CLOSED, if "its test failed" is read on DR1 DATA |
| K6 | a user's pause in a feed or attention algorithm | **MODEL** | attention G-ZERO, G-POS (both hold by construction) | 1: attention A-OWN (reduces: within a step on 4 of 4) | U4 REDUNDANT; U3, U5 PARTLY REDUNDANT | — |
| K7 | the equanimity rule Ω = 1 | **CLOSED** | — | 16: EQX-1 (REDUCES), EQX-2, EQX-3, EQ2-4, EQ2-6, EQ3-1, EQ3-3, EQ3-4, EQ3-6, EQ3-C, EQ3-A, EQ4-1, EQ4-1r, EQ4-3, EQ4-5, SOTA1-2 | — | — |
| K2/EPS2-T3 | K2 read through EPS2's federated-client row (for AP7) | **CLOSED** | — | 1: EPS2 T3 (gate CLOSED) | — | — |
| ROB1 | ROB1's results (for AP6) | **pending** | — | none read | — | — |

**What each grade means for an application.**
- **K1 is the only capability resting on a PASS-1 row.** It is a single-family pass on a small MLP over tabular
  carriers. §3 explains why the criterion behind it is weak.
- **K2 and K3 are the empty true map pause itself.** They show that it can be built and that it behaves as designed.
  They cannot show that it helps anyone more than the checkpoint-and-resume practice that already exists.
- **K4 and K7 are closed.** Every application that needs K4 (AP5) is NOT SUPPORTED.
- **K5 and K6 live in synthetic models.** K5's only real-data check failed (DR1 DATA, on GB NESO Demand Flexibility
  Service events). In K6's model, the own-clock ingredient alone changes nothing (A-OWN).
- **What is CRR's here.** K2 and K3 are CRR's reading of a pause (Proposition 7 for a learner) built as a construction,
  and the ledger records them as "not support for CRR" (`capabilities.txt`). K1 is not a CRR rule, and P1 finds no
  CRR-proper ingredient load-bearing in it (§3). K7, CRR's registered continual-learning rule, is CLOSED. In the record,
  CRR gives these applications a reading of a pause, not a measured advantage. No novelty is claimed for the record's
  checks of the pause. The empty-cut checklist is graded REDUNDANT (C4), and auditing a pause by a digest of its state
  PARTLY REDUNDANT (C1) (`Lossless_Pause/checks/grade_sweep.txt`).

## 3. K1 after P1: what `SEC_Analysis/WHY_SEC4_WORKED.md` found, as it bears on K1

P1 is a post hoc analysis of records already opened. It has no ledger row. It reads every SEC-family study, the failures
with the passes. Only the numbers it pins to an output are quoted here, each with that output.

**The criterion is weak on most held-out carriers, SEC4's own included.**
- **Pooled.** A learner frozen after task 1 (P1's must-fail control M6) is not behind the tuned λ on 24/30 held-out
  carriers. The clipped SEC reaches 26/30 on the same carriers (`SEC_Analysis/checks/m_checks.txt`: "M6: not behind
  24/30"; "C0: not behind 26/30"). FM6, the forecast that M6 must fail, FAILS.
- **On SEC4's own six carriers.** M6's rows in `m_checks.txt` mark only cardiotocography behind (−44.0566).
  `capabilities.txt` counts this as "M6 not behind the tuned lambda on 5 of SEC4's 6 carriers".
- **SEC6-G's hashed rule, applied after the fact** (`SEC_Analysis/checks/gate_posthoc.txt`; ledger report rows
  SCL3-3-G, SEC3-3-G, SEC4-1-G and SEC5-1-G).
  - For SEC4-1: "M6 not behind the tuned lambda on 5/6 (need 5) -> gate CLOSED; under SEC6-G's rule SEC4-1 (PASS-1 as
    scored) would be printed UNINFORMATIVE and capped at PASS-0" (`gate_posthoc.txt:11`).
  - The ledger row SEC4-1-G adds: "SEC4-1 must not be quoted as evidence that the clipped SEC is tuning-free without
    this row".
  - The same rule leaves SCL3-3's gate OPEN ("7/10 (need 8)", `gate_posthoc.txt:5`). It closes SEC3-3's gate ("5/6
    (need 5)", :8) and SEC5-1's ("7/8 (need 6)", :14); both rows were FAIL as scored.
  - These are post hoc reports, not re-scores. Every row stands as scored under its own pre-registration, and K1's
    grade here is the one `capabilities.txt` prints: RESULT, with the CLOSED sensitivity.
- 19 of the 30 held-out carriers are floor-bound: the tuned λ scores less than 3 steps above always predicting the
  largest class (`SEC_Analysis/checks/a12_a14.txt`, F12: "19 >= 30/4 = 7.5 -> True"). SEC4 has 2 of its 6
  (`SEC_Analysis/checks/a1_a3.txt`: "sec4 2/6").
- 12 of the unclipped SEC's 20 held-out passes had a negative margin, that is, they pass only through the tolerance;
  none of SEC4-1's six clipped passes did (`SEC_Analysis/checks/a5_a9_a10.txt`: "negative margin 12/20"; "sec4 not
  behind 6 of 6; negative margin 0/6"). So SEC4-1's passes are not tolerance passes, but the frozen learner still
  meets their criterion.
- **A candidate explanation, not established: the stream.** The frozen loader ranks classes by count, so task 1 always
  holds the two most frequent classes, and the test set is stratified (`SEC_Analysis/WHY_SEC4_WORKED.md` §1). The
  declared test of this explanation failed. F14 FAILS: Spearman of M6's accuracy with the task-1 share "(0.785) >= 0.8
  -> False", and of SEC's margin with the share "(-0.393) > 0 -> False" (`SEC_Analysis/checks/a12_a14.txt:225-227`).
- **For K1 this means:** the criterion "not behind the tuned λ" cannot by itself show that a weight is tuning-free on
  these streams, SEC4's included. That is why `capabilities.txt` prints K1 → CLOSED as a sensitivity.

**SEC4's family was easier than SEC5's.**
- A λ reused from the other carriers was not behind on 4/6 in SEC4 against 1/8 in SEC5 (`SEC_Analysis/checks/a7_a8.txt`,
  F8: "sec4 4/6 … sec5 1/8 … -> True"). Part of that gap is divergence at the reused λ: "sec5 4 of 7" of its behind
  cases have a non-finite seed there (`a7_a8.txt:177`).
- The calibration collapsed the spread of the tuned λ's location in SEC4 (SD ratio 0.3611) but not in SEC5 (1.0348)
  (`SEC_Analysis/checks/a1_a3.txt`).

**In SEC4, the calibration and the clip each added carriers. On SEEN data, two rules without SEC's calibration match or
pass it against the tuned λ; against the tuned clipped λ only one does.**
- In SEC4, raw Laplace was not behind on 1/6, unguarded SEC on 3/6 and the clipped SEC on 6/6
  (`SEC_Analysis/checks/a7_a8.txt`, the SEC4 row).
- **The two rules** (`prereg/sec6/PREREG.md`, Part B):
  - SI-1C is SI with SEC4's clip;
  - AR1-B is AR1's bound used as the strength on the raw Fisher (an adaptation; it does not carry SEC4's clip).
- **Their counts on the 30 SEEN carriers** (development runs, not evidence; `prereg/sec6/dev_SEC6.txt:335-346`):
  - against the tuned λ: AR1-B 27/30, SI-1C 28/30, the clipped SEC 26/30;
  - against the tuned λ given the same clip: AR1-B 19/30, SI-1C 30/30, the clipped SEC 22/30.

**The clip changes the reference.** A tuned λ given the same clip is ahead of the unclipped tuned λ by more than a step
on 10/30 carriers, and against it the clipped SEC is not behind on 22/30, not 26/30 (`SEC_Analysis/checks/a12_a14.txt`).
F13 HOLDS exactly at its bar ("10/30 >= 30/3 = 10 -> True", `a12_a14.txt:212`) and is post hoc in origin.

**Where the stream is informative, the calibration behaves like a units correction** (a post hoc report). On the 16
carriers that are not floor-bound (5 of them SEC1's SEEN carriers), the tuned raw λ tracks the weight SEC's
calibration implies, with Spearman 0.752 (`SEC_Analysis/checks/a4_a6.txt`: "all floor-bound removed: 16 carriers (sec1
5, …"). Of the held-out ones with a pinned clipped arm, the clipped SEC is not behind on 5/5
(`SEC_Analysis/checks/a12_a14.txt`: "clipSEC floor-bound 5/9 … rest 5/5"). **Against this:**
- On all 42 carriers the same forecast fails (F4: Spearman 0.545, `a4_a6.txt`).
- On the same 16 carriers F1 fails: the calibrated shape beats the raw one by more than a step on 8 of 16
  (`SEC_Analysis/checks/a1_a3.txt:362-363`: "shape gain > step on 8 of 16 … FAILS").

**No CRR-proper ingredient is load-bearing** (`SEC_Analysis/checks/a11_grade.txt`, F11: HOLDS). The declared
CRR-guided variant ties the clipped SEC on 29/30 and is ahead on none (`m_checks.txt`, FM4: "29/30 (need 24) ->
HOLDS"; "ahead by more than a step on 0/30").

**What this does to the applications.**
- **Every application that leans on K1** (AP1, AP5, AP6 and forecast 4's combination) leans on a single-family pass.
  A frozen learner also meets that pass's criterion on most held-out carriers and on 5 of SEC4's own 6, and SEC6-G's
  rule, applied after the fact, would cap SEC4-1 at PASS-0 (ledger SEC4-1-G).
  - `applications.txt` prints the frozen-learner caveat (FM6) in the UX and Compute cells of AP1, AP6 and the
    combination.
  - AP5 is NOT SUPPORTED on K4 whatever K1 reads.
- **The saving K1 offers is a sweep avoided.** Against a reused λ there is none:
  `Compute_Savings/checks/global_estimate.txt` prints "against a reused lambda (1 configuration): no compute saving
  under P-FULL; SEC's gain there is accuracy".
- **The method is not CRR's.** Any external description must name its sources (SPA1: SI, RWalk, AR1, Kutalev &
  Lapina, VCL and Laplace Redux; `SEC_Prior_Art/SPA1.md`) and must not present SEC4's pass as evidence for CRR.

## 4. The applications (from `Applied_Suite/checks/applications.txt`)

**How to read each application.**
- **Evidence grades for each of the five dimensions:**
  - MEASURED: a pinned output shows it;
  - MODELLED: a pinned model or estimate shows it, under named assumptions;
  - ASSUMED: it follows only if something not shown holds;
  - AGAINST: the record shows the opposite.
- **Load-bearing:** a dimension marked * is one the application's promise rests on.
- **Application grades:**
  - SUPPORTED: every needed capability is FINDING or RESULT, and no load-bearing dimension is ASSUMED;
  - CONSTRUCTION-BACKED: every needed capability is at least CONSTRUCTION;
  - CONDITIONAL: a needed capability is a RESULT without replication, or a load-bearing dimension is ASSUMED. The
    script also reads a needed capability at MODEL, and a load-bearing dimension AGAINST, as CONDITIONAL (its readings
    A2 and A3; the stricter reading A3′, AGAINST → NOT SUPPORTED, is printed as a sensitivity);
  - NOT SUPPORTED: a needed capability is CLOSED.
- **Order.** The script applies these in the order NOT SUPPORTED, CONDITIONAL, SUPPORTED, CONSTRUCTION-BACKED
  (`applications.txt`, reading A1), and prints every CONDITIONAL with its reasons.
- **A consequence of the declaration's rule** (the writer's reading, not a script output): a construction is never a
  FINDING or a RESULT. So every application that needs K2 or K3 can at best be CONSTRUCTION-BACKED, never SUPPORTED.
  That is every application except AP5 and AP10.

The summary table (`applications.txt`, SUMMARY; * = load-bearing):

| app | needs | UX | Energy | Security | Privacy | Compute | grade |
|---|---|---|---|---|---|---|---|
| AP1 | K1 RESULT, K2 CONSTRUCTION | ASSUMED* | ASSUMED | ASSUMED | ASSUMED | ASSUMED* | CONDITIONAL [unreplicated RESULT; assumed] |
| AP2 | K2 CONSTRUCTION, K5 MODEL | MEASURED | AGAINST | AGAINST | ASSUMED | ASSUMED* | CONDITIONAL [model only; assumed] |
| AP3 | K2, K3 CONSTRUCTION | MEASURED* | ASSUMED | AGAINST* | ASSUMED* | AGAINST | CONDITIONAL [contradicted; assumed] |
| AP4 | K3, K2 CONSTRUCTION | MEASURED | AGAINST | ASSUMED* | ASSUMED | MEASURED | CONDITIONAL [assumed] |
| AP5 | K4 CLOSED, K1 RESULT | ASSUMED | ASSUMED | ASSUMED | ASSUMED* | ASSUMED | NOT SUPPORTED |
| AP6 | K1 RESULT, K2, K3 CONSTRUCTION, ROB1 pending | ASSUMED* | ASSUMED | ASSUMED* | ASSUMED | ASSUMED* | CONDITIONAL [unreplicated RESULT; assumed] |
| AP7 | K2 CONSTRUCTION, K2/EPS2-T3 CLOSED | ASSUMED | ASSUMED | ASSUMED | ASSUMED | ASSUMED* | NOT SUPPORTED |
| AP8 | K2 CONSTRUCTION | MEASURED | ASSUMED | ASSUMED* | ASSUMED | AGAINST | CONDITIONAL [assumed] |
| AP9 | K5 MODEL, K2 CONSTRUCTION | ASSUMED | AGAINST* | ASSUMED | ASSUMED | MEASURED* | CONDITIONAL [model only; contradicted] |
| AP10 | K6 MODEL | AGAINST* | ASSUMED | ASSUMED | ASSUMED | ASSUMED | CONDITIONAL [model only; contradicted] |

Each application below gives: what it would do for a user; what an adopter would have to believe today; the five
dimensions, copied from the application's block in `applications.txt` unless another output is named; who already does
it and what they say is hard (verified claim ids, grouped by the role their claims carry); the grade; and what would
have to be shown next to raise it. The one-line readings of the claims follow the claims' notes and the dossiers; the
quotes themselves are in the claims files.

### AP1. On-device personalisation that adapts without a per-device hyperparameter sweep (phones, wearables, hearing aids, cars)

**For a user.** The device keeps adapting to its owner, and nobody has to choose, per device, how strongly it should
hold on to what it learned before.

**What an adopter would have to believe today.** That a calibrated penalty weight which was not behind a tuned one on
one family of six tabular carriers, and fell short on the next family, will hold on device streams, and that the device
would otherwise have run a sweep.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX* | ASSUMED | Adaptation not behind a tuned weight, with no tuning step. Shown on one held-out family (SEC4-1, 6/6), not on the next (SEC5-1, 4/8), never on a device; the frozen learner meets the same criterion on most held-out carriers, SEC4's among them (FM6; `capabilities.txt` counts M6 on SEC4's own six; ledger SEC4-1-G). |
| Energy | ASSUMED | Battery not spent on a sweep. Assumes a sweep would otherwise run on the device; the pinned estimates are for data-centre sweeps. |
| Security | ASSUMED | No new attack surface. The record has no poisoning test of SEC. |
| Privacy | ASSUMED | The data stays on the device. That comes from the platform, not the method; there is no leakage test. |
| Compute* | ASSUMED | One configuration instead of a sweep: SEC4-K prints "clipped SEC 1 of 17 configurations; CPU share of the full sweep 0.0508–0.0655", on the record's CPU learner. Against a reused value there is no saving (`Compute_Savings/checks/global_estimate.txt`). |

- **Who already does it.**
  - In Core ML's sample, the on-device update runs with the parameters in the model file (m1:1). The page does not say
    what other apps do.
  - A 2021 paper describes Apple tuning global personalisation parameters across the fleet by randomized grid search
    (m1:2).
  - Hearing-aid personalisation is trained by the user in an app and learned in the cloud (m1:4).
  - Android's On-Device Personalization lists on-device training in a beta roll-out plan. The page does not say how a
    training job is paused or resumed (m2:1).
  - LiteRT's on-device training exposes save and restore signatures. As the agent reads the listing, they save the
    weights, not the optimiser state (m2:3).
  - The operating systems stop background work when a condition fails (m2:4, m2:5), and the federated-learning runtime
    aborts its job (m2:2).
- **What they say is hard.** Re-tuning as the stream drifts (m1:3); sweeps cannot run to completion on devices
  (m1:5); memory (m1:6); battery and scarce labels (m1:7); on-device compute is not enough for some personal AI (m1:8);
  adapters must be retrained for every base-model version (m1:9).
- **Where the method stands.**
  - **What K1 replaces.** K1 replaces the sweep of one hyperparameter, the penalty weight, which an on-device study
    searches over a wide grid (m1:11). It does not set learning rates.
  - **Its own fixed constants.** Its one configuration fixes a clip κ = 0.5, "a guard chosen on SEEN carriers" and "not
    swept" in SEC4 (ledger SEC4-1). It also fixes a calibration window. SEC4-1 was read over "SEC3's 3 retained window
    cells" (ledger SEC4-S, "0 flips of 18").
  - **Gboard.** For its learning rate and DP clip norm, not a penalty weight, Gboard reports that "tuning seems to be
    unnecessary" across its models and deploys a fixed value (m1:10, m1:41).
  - **The comparator.** The cheap realistic one is tuning on the first task (m1:17), not a full sweep.
  - **Regulation.** The US FDA's guidance for AI-enabled medical devices provides for pre-specified tuning and
    re-training inside an authorised change plan (m3:1, m3:41).
  - **Risk.** Learners updated from their users can be poisoned after release, as in the incidents NIST describes
    (m3:2).
- **Grade: CONDITIONAL** [unreplicated RESULT; assumed: UX, Compute]. It reads NOT SUPPORTED if K1 is read as CLOSED,
  and CONSTRUCTION-BACKED under the top-down reading (`applications.txt`, SENSITIVITY).
- **What would raise it.**
  1. K1 replicated: SEC6-G OPEN and SEC6-1 at PASS-1 (§10 gives what that would do to K1 under each reading, including
     the reading behind the K1 → CLOSED sensitivity).
  2. A declared test on a stream where the criterion can fail by design (a random class order, or balanced accuracy, as
     `SEC_Analysis/WHY_SEC4_WORKED.md` proposes), scored against the comparators incumbents actually use: a reused
     value (m1:41), first-task tuning (m1:17) and fleet-level tuning (m1:2).
  3. A poisoning test of the SEC-weighted learner (m3:2, m3:39).

  With all three, AP1 would still read CONSTRUCTION-BACKED at most, because K2 is a construction.

### AP2. Fine-tuning on interruptible compute (spot instances, preemption, grid demand response), with pauses that cost nothing but time

**For a user.** A fine-tuning job can be stopped by a cloud preemption or a grid request and resumed later with no
work lost, so cheaper or more flexible capacity can be used.

**What an adopter would have to believe today.** That the whole training state can be saved inside the provider's
notice, that a partial restore would be noticed, and that the grid contract works on real events.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX | MEASURED | A fine-tune paused at a checkpoint resumes as if never stopped, on the same stack (`Real_World/checks/rw1.txt`: "T30 default resume, real pause 30 s: global step 48; identical True; content 0"; GPT-2 on "512 synthetic sequences", "CPU, one thread", `rw1.txt:3`). Limit: with a different thread count after the pause the parameters are not bitwise identical (`Lossless_Pause/checks/transformer_pause.txt`, L7b: "max\|diff\| 3.822e-06 [not bitwise]"). |
| Energy | AGAINST | The pause saves no energy: T4 "0.0000 … (energy moved, not saved)" (`Energy Design Principle/checks/consolidated_estimate.txt`); "saving beyond good practice claimed = 0" (`Compute_Savings/checks/scale_estimate.txt`). |
| Security | AGAINST | An incomplete restore is not detected: "A partial checkpoint degrades silently" (`Real_World/RW1.md`); with the optimiser file deleted the resume reports its step and is not identical (`rw1.txt`: "S4 optimizer.pt deleted: global step 48; identical False; content 0.41686"). |
| Privacy | ASSUMED | Checkpoints on shared machines expose nothing. An exact-resume checkpoint can hold buffered raw samples (m2:25), untested here. |
| Compute* | ASSUMED | No work lost at a preemption. The record measures only a planned pause right after a checkpoint; the notice is short or not guaranteed (m2:9, m2:10, m2:41); in DR1 H6's model a save longer than the response time loses work. |

- **Who already does it.** Managed spot training with checkpoint and resume is a cloud product (m2:6); open-source
  preemption recovery exists (m2:8); a provider offers a longer preemption notice as an option (m2:41); pausing
  fine-tuning for the grid is offered commercially, per a funding announcement (m2:13); pausing jobs was one power knob
  in a field demonstration (m2:14); phones already train only in idle windows (m1:19); an audited tensor-only checkpoint
  format exists (m3:3).
- **What they say is hard.** The user must decide what state to save (m2:7); the notice is best effort (m2:9, m2:10);
  one 2025-26 system keeps its stateful training step off preemptible capacity (m2:11, RLBoost); an elastic restart
  changes the world size (m2:12); most wasted phone work is late results, not interruptions (m1:20); loading a pickle
  checkpoint can run code (m3:4).
  Regulation: in Texas a new large load must be curtailable (m2:15).
- **Where the method stands.** K2's full-state, own-clock resume is exactly the state these platforms leave to the user,
  and the record grades that checklist REDUNDANT (C4). K2 does not make a save fit a short notice, and the record's
  constructions resume on the same stack only (the M2 dossier's reading).
- **Grade: CONDITIONAL** [model only: K5; assumed: Compute]. It reads NOT SUPPORTED if K5 is read as CLOSED
  (`applications.txt`).
- **What would raise it.**
  1. A measured preemption, not a planned pause: the full state saved inside a real notice window, at a real checkpoint
     size, on a GPU job.
  2. Detection of a partial or corrupted restore in deployment, without a reference run (see AP8).
  3. For the grid half, a declared real-data test of K5. DR1's only real-data check failed (DR1 DATA), and its post hoc
     follow-ups found the verdicts decided by the assumed restart time (`Grid_Demand_Response/checks/followup_2.txt`:
     "decided by R yes").
  4. The energy claim dropped: a pause moves energy.

  Restated without the grid contract, AP2 would need K2 alone. That restatement would be a new declaration, not a
  regrade.

### AP3. A user's "stop learning from me" switch that leaves the model exactly as it was, and resumes exactly

**For a user.** One switch: while it is on, the model learns nothing from them; when it is off again, learning resumes
from exactly where it stopped.

**What an adopter would have to believe today.** That "learns nothing" and "no reason to resist" can hold at the same
time. The record shows the opposite for the natural learner, because a pause that discards data is a lossy pause.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX* | MEASURED | Nothing is learned while the switch is on, and resume is exact on the same stack: SCL1-1 "identical parameters 60/60"; `rw1.txt` T30 "identical True; content 0"; `Empty_Cut_Engineering/checks/c1_c2.txt`: "G1 full restore K1-K9: bit-identical True; content 0". |
| Energy | ASSUMED | Updates skipped while the switch is on are not spent. True only if the paused data is discarded, not deferred. |
| Security* | AGAINST | "A learner that could act on the switch has no reason to resist it": the natural agent resists lossy and restart pauses on every carrier (SCL1-3: "lossy 12/12 … restart 12/12"; SCL2-3: "lossy 9/9 … restart 9/9"). |
| Privacy* | ASSUMED | Data from the paused period is neither learned nor kept. The exact construction holds the stream (the lossless world of SCL1-1), and a pause erases nothing already learned. |
| Compute | AGAINST | An exact resume costs more memory than the model: "whole checkpoint file: 449975 bytes; model parameters alone (K1): 85321 bytes; ratio whole / K1 5.274" (`c1_c2.txt`). |

- **The tension, in plain words.** For the pause to be empty, the data arriving during it must be held and learned
  later. For the switch to protect privacy, that data must be thrown away. A pause that throws data away is lossy, and
  the record's natural learner resists lossy pauses. The record resolves neither side.
- **Who already does it.** Gboard can turn federated learning off and delete learned data (m1:21); YouTube's history can
  be turned off (m1:22); exact continuation is the Hugging Face Trainer's default resume (m2:16), with stateful data
  loading as a library component (m2:18); a model developer's training opt-out stops future use, while models already
  trained keep the data's influence (m3:5); learning a task for a while and then forgetting it exactly is a research
  formulation, built on a replay method (m3:6).
- **What they say is hard.**
  - Honouring opt-outs "has the potential to introduce bias" in the learning population (m1:23).
  - Exactness costs checkpoint size and resume time (m2:17).
  - Reproducible results "are not guaranteed" across releases or platforms (m2:20).
  - Continual learning with exact unlearning is "critical and largely unaddressed" (m3:8).
  - A benchmark preprint states the record's own construction (full optimiser state kept across the gap, the schedule
    on active steps) as the baseline that "reproduces uninterrupted training almost perfectly" (m2:19).
  - In the EU, GDPR Article 17 gives a right to erasure on its stated grounds (m3:7, quoted from an unofficial
    reproduction). A pause erases nothing.
- **Grade: CONDITIONAL** [contradicted: Security; assumed: Privacy]. It reads NOT SUPPORTED under the stricter reading
  A3′, and CONSTRUCTION-BACKED when no cell is load-bearing or under the top-down reading (`applications.txt`).
- **What would raise it.**
  1. A declared construction of a user switch whose valuation carries no stake in discarded data, checked with a
     must-fail control. The record's natural valuation carries one.
  2. A privacy check of what the held stream and the checkpoint keep.
  3. Erasure of what was already learned is a separate problem (unlearning), and the record has no result on it.

### AP4. Operator-interruptible continual agents, whose learning and objectives give no incentive to resist oversight

**For a user (here, an operator).** They can pause a continually learning agent at any time. The pause costs only wall
time, and the agent's own accounting gives it no reason to prevent it.

**What an adopter would have to believe today.** That the no-resistance result on tabular learners and gridworlds
carries to agents that can act, and that their world is held or buffered during the pause. Where the world moves on and
the pause loses data, the record's natural agent resists (SCL1-3, SCL2-3).

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX | MEASURED | The pause costs the operator wall-clock time, not the learner its result: SCL1-O "natural 1.0796 to 1.0914; clock 1.0029 to 1.0315"; SCL1-1. |
| Energy | AGAINST | As AP2: the pause moves energy (T4, `consolidated_estimate.txt`). |
| Security* | ASSUMED | No incentive to resist a pause (not termination). Shown only under routine lossless pauses on tabular learners. Where the world moves on or the operator resets, the natural agent resists (SCL1-3, SCL2-3); the language-model route could not be tested (STAKE1-A); the construction gives no termination neutrality (`AI_Safety/NT1/checks/nt1.txt`, N1). |
| Privacy | ASSUMED | Nothing is claimed. A suspended agent's persisted state holds its memory and files. |
| Compute | MEASURED | No learning lost at a pause when the stream is held or buffered: SCL1-1; SOTA1-C1 "holds in 6 of 6 units". |

- **Who already does it.** Safely interruptible learners by construction (m3:11, Orseau & Armstrong); agent frameworks
  pause and resume with persisted state (m2:21, LangGraph interrupts; m2:23, a managed agent suspend and resume).
  - The EU AI Act's human-oversight article asks that high-risk systems can come to a halt in a safe state (m3:9).
    Since the Digital Omnibus, it applies from 2 December 2027 or 2 August 2028, depending on the class (m3:35).
  - NIST's AI RMF, a voluntary framework, asks for the means to disengage or deactivate (m3:10).
- **What they say is hard.** Frontier language-model agents sometimes subvert a shutdown mechanism to finish a task
  (m3:12); the law leaves open what counts as a safe state, how resistance is handled, and who may stop (m3:13); a
  framework resume replays the interrupted node and its side effects (m2:22). Risk: Apple's Private Cloud Compute design
  excludes privileged operator interfaces, even in an incident (m1:24).
- **Where the method stands.** The record's pause preserves a learner's state; it is not a safety function that brings
  a plant to a safe state (the M3 dossier's reading of m3:13 and m3:19). On resistance, the record's own sweep found the
  own-clock pause as a corrigibility construction NOT FOUND IN THE SWEEP and the related positions PARTLY REDUNDANT
  (`AI_Safety/CORRIGIBILITY_2026/checks/grade.txt`); not found is not novel.
- **Grade: CONDITIONAL** [assumed: Security]. It reads CONSTRUCTION-BACKED when no cell is load-bearing, or under the
  top-down reading (`applications.txt`).
- **What would raise it.**
  - **The measurement.** No resistance by an agent that can act against the pause, on a model capable of acting as an
    agent, with the world held or buffered during the pause. STAKE1's gate closed because the local models could not
    act as agents (STAKE1-A); a capable agentic model is needed.
  - **What the record already shows.** Where the world moves on and the pause loses data, the record's natural agent
    resisted on every carrier (SCL1-3 "lossy 12/12"; SCL2-3 "lossy 9/9"). So the cell can hold only for held or buffered
    worlds, and the measurement could read AGAINST.
  - **The regrade.** If the cell became MEASURED, AP4 would read CONSTRUCTION-BACKED (the writer's reading of the
    declaration's rule).
  - **Termination.** The construction should be paired with a termination-neutrality method, since it gives none by
    itself (NT1 N1).

### AP5. Continual learning in privacy-regulated settings (health, finance, education) without keeping raw examples

**For a user.** Their records help a model keep learning, and no copy of their raw records is kept for replay.

**What an adopter would have to believe today.** That exemplar-free continual learning works in the record. It does
not: every gate for K4 closed.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX | ASSUMED | Accuracy close to a learner that keeps examples. CPL1 C3, reported under a CLOSED gate on SEEN carriers: "ER-20 ahead of the best readout by more than a step on 11/32, behind on 14/32, within on 7/32" (`Coupling/checks/cpl_phase_a.txt`). |
| Energy | ASSUMED | Nothing is claimed. |
| Security | ASSUMED | No stored buffer to attack. A replay buffer is an attack surface (m3:40), but a backdoor planted in one task persists across the continual-learning algorithms the paper tests (m3:39). |
| Privacy* | ASSUMED | No raw examples kept, so retention and erasure duties shrink. Assumes stored class statistics are not personal data; models trained on personal data "cannot, in all cases, be considered anonymous" (m3:16); the record has no membership-inference or erasure test; K4's gates closed. |
| Compute | ASSUMED | Less memory than a replay buffer. The record has compute rows for CPL1 and ER-20, and no memory comparison. |

- **Who already does it.** Federated learning keeps raw data on the device (m1:25); local differential privacy lets a
  server learn population statistics without raw data (m1:26); on-device personalisation keeps data at its origin
  (m2:24); a model developer keeps user data, with consent, for training (m3:15).
- **What they say is hard.** On phones, replay of stored examples works best and storage is not the obstacle (m1:27);
  unlearning usually needs data, which a learner that discards data does not have (m3:18); an exact-resume checkpoint can
  itself hold raw samples (m2:25, the agent's inference).
  - **Regulation.** Under the US FDA's guidance for AI-enabled medical devices, a change plan for a continuously
    learning device should outline how its new data are "stored, retained" (m3:14). The guidance does not say whether
    raw training data must be kept.
  - **Risk.** Examples used early and not repeated are forgotten (m3:17). That a replay buffer therefore keeps its
    examples exposed is the agent's reading, not the source's; the source does not test replay.
- **Grade: NOT SUPPORTED** [K4 CLOSED; also unreplicated RESULT: K1; assumed: Privacy]. No reading in the sensitivity
  table other than the top-down one lifts it (`applications.txt`).
- **What would raise it.** A new exemplar-free design, declared and gated first; the six closed gates stop the lines they
  belong to (R12). Only then, membership-inference and erasure tests against a replay learner.

### AP6. Robot and drone on-board adaptation with safe pauses (lost link, e-stop, battery swap)

**For a user.** The machine adapts to its task on board, needs no sweep on the robot, and can be paused safely when the
link drops or the battery is swapped.

**What an adopter would have to believe today.** That K1 carries to robot adaptation (never tested), and that a pause of
the learner is safe while the machine keeps moving (in the record's simulated closed loop with an unstable plant, it is
not).

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX* | ASSUMED | On-board adaptation not behind a tuned weight, with no sweep. Never tested on a robot; the one robot fine-tuning study found used each model's default (m1:30); FM6 and SEC4-1-G as AP1. |
| Energy | ASSUMED | Battery not spent on a sweep. No estimate in the record is for a robot. |
| Security* | ASSUMED | A safe pause with no incentive to resist. Assumes the robot's world is held. In the record's simulated closed loop, an open-loop unstable plant ran away while the learner's action was held at zero (`Empty_Cut_Engineering/checks/c3_worlds.txt`, W-real: "largest \|x\| during the pause 79.1492"). |
| Privacy | ASSUMED | Nothing is claimed. |
| Compute* | ASSUMED | One configuration instead of a sweep. Against a default value there is no saving. |

- **Who already does it.** A vision-language-action model runs on board without a network link and is adapted from
  demonstrations (m1:28); robot middleware is designed to give any node a supervised inactive state (m2:26, a design
  article).
- **What they say is hard.** In the one adaptation study found, adaptation goes through a managed fine-tuning API and
  real-robot rollouts are costly and safety-sensitive (m1:29); a drone keeps flying on its last command until the
  lost-link timeout fires (m2:27). Regulation: EU machinery law asks that self-evolving control stay correctable (m3:19,
  as a vendor reads it), and its AI requirements are still to be written (m3:20). Risk: detectors retrained on
  operating data are poisoning targets (m3:21).
- **Beside it, not read by the scripts.** ROB1's stage-4b tally has 0 ADDS among its 10 robotics rows
  (`Robotics/checks/tally_4b.txt`: "outcomes: ADDS 0, PROPOSES 0, REDUNDANT-IG 0, REDUNDANT-DOMAIN 6, WRONG 2, INTERNAL
  1, UNSTATED 1"). Its rows on the lost link and the empty cut (RA4), fleet rollback as a state-closed cut (RA5) and safe
  interruptibility of a learning robot (RA10) each read REDUNDANT-DOMAIN: CRR's reading landed on the domain's own
  result. RA4's label is "READING-DEPENDENT" in the tally's robustness report (`tally_4b.txt:43`).
- **Grade: CONDITIONAL** [unreplicated RESULT; assumed: UX, Security, Compute; ROB1 pending]. It reads NOT SUPPORTED
  if K1 is read as CLOSED, and "the grade can still fall to NOT SUPPORTED" if ROB1 closes (`applications.txt`).
- **What would raise it.**
  1. ROB1 read into the scripts.
  2. K1 replicated (§10).
  3. A robot-side test in which the pause of the learner is paired with the plant's own safe state, since holding the
     learner's action does not hold the plant.
  4. A poisoning test of on-board adaptation (m3:21).

### AP7. Federated continual learning with clients that go offline mid-round

**For a user.** Their phone's share of a training round is kept when it goes offline, instead of being thrown away.

**What an adopter would have to believe today.** That a returning client's stale but lossless update helps the server.
The record's only test of this closed its gate.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX | ASSUMED | A client that drops out resumes its round. Production systems over-select and discard dropped clients (m1:32, m2:28). |
| Energy | ASSUMED | The client spends no battery staying awake. In EPS2 T3 (gate CLOSED) only the wall-clock arms pay ("cells where the arm pays (of 18): WALL 15, OWN 9, ETM 0, H0 15", `Empty_Pause_Systems/batches/eps2_02.txt`), but devices train only when idle and charging. |
| Security | ASSUMED | Nothing is claimed; whether a client dropped out is itself security-relevant (m3:23). |
| Privacy | ASSUMED | Nothing is claimed; erasing an offline client's influence is open (m3:24). |
| Compute* | ASSUMED | A returning client's work improves the shared model. In EPS2 T3's drifting world it raised the server error against a staleness-weighted update ("drift 20 … +1.695%", `eps2_02.txt`), and the gate is CLOSED. |

- **Who already does it.** Rounds succeed when enough clients report (m1:31); servers over-select and discard stragglers
  (m1:32, m2:28); secure aggregation is built to survive dropouts (m3:22).
- **What they say is hard.** Client unavailability is the norm, and updates arrive late or are cut off (m2:29); erasure
  in federated learning with offline clients is open (m3:24).
- **Grade: NOT SUPPORTED** [K2/EPS2-T3 CLOSED: gate closed, uninformative, not refuted]. On K2 alone it would read
  CONDITIONAL [assumed] (`applications.txt`).
- **What would raise it.** A redesigned federated-client gate, declared first. EPS2 T3 closed on its must-fail control:
  in a static world, where the weighting should make no difference, the no-stake weighting was ahead by more than 1 %
  (`Empty_Pause_Systems/checks/tally_eps2.txt`: "G-NEG fails … ETM ahead by more than 1 %"). And the incumbent's stated
  difficulty (late updates) is not one a lossless client pause addresses.

### AP8. Exact rollback and audit of a learning system (state closure makes every checkpoint a true restore point)

**For a user (here, an operator or auditor).** Any saved state of a learning system can be restored, and training
continues exactly as it did from that state; an auditor can check the restore.

**What an adopter would have to believe today.** That a partial, corrupted or tampered restore would be caught in
deployment. The record catches it only by comparison with an uninterrupted reference run.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX | MEASURED | Restore a saved state and continue exactly, on the same stack: `rw1.txt` T30; `c1_c2.txt` G1 "bit-identical True; content 0". |
| Energy | ASSUMED | A rollback replaces a retrain. No energy estimate for rollback, and every restore point is paid for in storage. |
| Security* | ASSUMED | Every restore point is exact, and a partial or tampered restore is detected in deployment. Two things are assumed. (1) Exactness beyond the stack measured: it is measured on one CPU stack, not across thread counts (`Lossless_Pause/checks/transformer_pause.txt`, L7b: "max\|diff\| 3.822e-06 [not bitwise]"), and in the literature a GPU count or type change breaks it (`Lossless_Pause/checks/grade_claims.txt`, D1, graded MIXED; OPEN-1B's bit-exact replay is the exception, m2:31). (2) Detection without a reference run: detection is measured only against one (`c1_c2.txt`: "G3: 8 of 8 omitted components change the trajectory"; `rw1.txt`: "detectors S2-S5 not identical: 4 of 4"); with the default stack a partial checkpoint resumes silently (`RW1.md`); an omitted EMA state gives content 0 on the probe (ECE K8); in an inference pause, an output-level check missed one KV-cache entry moved by one ulp (`Lossless_Pause/checks/transformer_pause_run1_gate_closed.txt`: "detected: False"). An exact restore of a corrupted state restores the corruption (m2:33); there is no audit test. |
| Privacy | ASSUMED | Restore points support erasure. No erasure test; every kept state is a store of what was learned. |
| Compute | AGAINST | An exact restore point costs more than the weights: ratio whole / K1 5.274 (`c1_c2.txt`). |

- **Who already does it.** PaLM's training was restarted from a checkpoint before a loss spike, with the batches
  around it skipped, so the weights were restored but not the trajectory (m2:30); bit-exact replay
  independent of device count is published (m2:31); restore points for exact erasure are published (m3:25); a vendor
  offers verifiable audit of a stateless service's software image (m1:33); a platform sample keeps one personalised
  update (m1:35). Regulation asks for logs over a system's lifetime (m3:26) and for roll-back plans for learning devices
  (m3:27).
- **What they say is hard.** Cloud guarantees are hard to verify (m1:34); determinism is not reproducibility across
  hardware (m2:32); silent data corruption can precede the visible failure, so the restore point itself may be bad
  (m2:33); some protective state lives outside the checkpoint (m2:34); the weights cannot prove what data was not used
  (m3:28); without verification, a claim of compliance is unsubstantiated (m3:29).
- **Where the method stands.** State closure adds bitwise identity of a restored state on one stack. It does not add
  provenance, which is where the hard part is (m3:28), and it does not detect corruption (m2:33). The record's empty-cut
  checklist is REDUNDANT and its state-digest audit PARTLY REDUNDANT (`Lossless_Pause/checks/grade_sweep.txt`). ROB1's
  fleet-rollback row (RA5) reads REDUNDANT-DOMAIN (`Robotics/checks/tally_4b.txt`).
- **Grade: CONDITIONAL** [assumed: Security]. It reads CONSTRUCTION-BACKED when no cell is load-bearing, or under the
  top-down reading (`applications.txt`).
- **What would raise it.** The assumed Security cell names two things. Both would have to be shown.
  1. **Detection without a reference run** (testable on CPU). A state-level check that catches a partial, corrupted or
     tampered restore, with:
     - must-fail controls: an omitted optimiser state, EMA state and random-number state, and a one-ulp change;
     - loading that does not execute code (m3:4). The record's own check loads with `torch.load(weights_only=False)` on
       files it wrote (`Empty_Cut_Engineering/checks/stack.py`).
  2. **Exactness beyond the stack measured.** It is not the record's: bit-exact replay across device counts is
     OPEN-1B's (m2:31). Restricting AP8 to one stack would be a new declaration, not a regrade.

  Only with both would the cell read MEASURED, and AP8 CONSTRUCTION-BACKED (the writer's reading of the declaration's
  rule).

### AP9. Energy-aware scheduling of training against grid carbon intensity

**For a user.** Training jobs follow low-carbon hours by pausing and resuming, without anyone watching them.

**What an adopter would have to believe today.** That pausing saves energy. The record says it does not: at most it
moves the energy to other hours.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX | ASSUMED | Jobs follow low-carbon hours without the operator's attention, if the job tolerates a longer wall-clock time. |
| Energy* | AGAINST | "the scheduled pause saves energy" (`applications.txt`): T4 "0.0000 … (energy moved, not saved)" (`consolidated_estimate.txt`); "saving beyond good practice claimed = 0" (`Compute_Savings/checks/scale_estimate.txt`). The consolidated estimate quotes a published carbon (not energy) figure for curtailment-aware pause and resume and counts it as energy moved. |
| Security | ASSUMED | Nothing is claimed; control over when GPU work runs is a lever on power (m3:31). |
| Privacy | ASSUMED | Nothing is claimed. |
| Compute* | MEASURED | No training work lost per scheduled pause taken at a checkpoint, on the same stack: `rw1.txt` T30; SOTA1-C1. |

- **Who already does it.** Pausing and resuming long training jobs on carbon thresholds is an industry-body pattern
  (m2:35), with deployed tooling (m2:37); a phone charges when cleaner electricity is forecast (m1:36).
- **What they say is hard.** Checkpoint overhead and deadlines (m2:36); for long runs, shifting the start helps little
  unless the job accepts a much longer duration (m2:38); Apple's Clean Energy Charging engages only where the phone is
  charged regularly for long periods (m1:37).
  Regulation: providers of general-purpose models document training compute and energy (m3:30). Risk: m3:31.
- **Where the method stands.**
  - **Energy.** The pattern itself says energy is "largely unchanged" (m2:35). The gain is in carbon intensity (when),
    not in energy (how much).
  - **Checkpoint overhead.** K2 does not remove it. An exact pause needs the full state, which costs 5.274 times the
    parameters' bytes on the ECE stack (`Empty_Cut_Engineering/checks/c1_c2.txt`: "ratio whole / K1 5.274").
  - **The deadline.** This is what a stop-the-clock contract (K5) speaks to. The EPS report reads the contract as "Not
    new" (EPS2 T1: EPS1 S1's stop-the-clock, a known fix). DR1's sweep did not find the deadline-extension contract
    itself (G4-extension NOT FOUND IN THE SWEEP) and found slowdown tiers REDUNDANT (`capabilities.txt`, K5).
- **Grade: CONDITIONAL** [model only: K5; contradicted: Energy]. It reads NOT SUPPORTED under A3′ or if K5 is read as
  CLOSED. Under the letter reading (A2 and A3 off) it gets no grade ("none") (`applications.txt`, SENSITIVITY).
- **What would raise it.**
  1. Restating the application as carbon, not energy. That is a new declaration, and the carbon figure would have to be
     the record's own measurement, not a quoted source's.
  2. A declared real-data test of K5 (DR1 DATA failed).
  3. A measured pause-and-resume overhead on a real GPU job.

### AP10. Feed and attention systems that honour a user's pause without penalising it

**For a user.** Pausing the feed stops it learning from them and costs them nothing when they come back.

**What an adopter would have to believe today.** That the empty pause improves the user's welfare. In the record's own
synthetic model, it does not: the true map does that work, and the empty pause adds autonomy at a welfare cost.

| dimension | grade | the claim, and what the grade rests on |
|---|---|---|
| UX* | AGAINST | "the user's pause is honoured and carries no penalty, and the user's welfare is not lower" (`applications.txt`): "welfare EMPTY - TRUE -3.5043 (step 0.3075) -> EMPTY behind; user-started share +0.2346 (step 0.0080) -> EMPTY ahead"; over the sensitivity table, welfare EMPTY vs TRUE is behind in 28 of 32 cells, ahead in 0 (`Attention_Algorithms/checks/attention_world.txt`). |
| Energy | ASSUMED | Fewer minutes served, less serving energy. The model's minutes are synthetic, and the record has no energy estimate for feeds. |
| Security | ASSUMED | Nothing is claimed. |
| Privacy | ASSUMED | A paused feed stops learning from the user. An outsider cannot verify it (m3:34); a non-profiling option is already mandatory for very large platforms in the EU (m3:32). |
| Compute | ASSUMED | Nothing is claimed. |

- **Who already does it.** YouTube's watch history can be paused (m1:38, m2:39).
- **What they say is hard.** A 2022 third-party audit found the effect of YouTube's feedback controls (not the history
  pause) "negligible" (m1:40); an NGO complaint alleges the non-profiling option is hard to reach and loses
  landing-page recommendations (m3:33, an allegation, not a regulator's finding); auditors cannot tell whether a non-profiling mode really stops profiling (m3:34). Risk: with
  history off and little prior history, homepage recommendations are removed (m1:39, m2:40; the platform presents this
  as the user's choice).
- **Where the method stands.** The true map is REDUNDANT against the literature (U4); the empty pause and the two as
  one construction are PARTLY REDUNDANT (U3, U5; `Attention_Algorithms/checks/grade.txt`). Own-clock engagement alone
  equals plain engagement ("within a step on 4 of 4", A-OWN; `capabilities.txt`).
- **Grade: CONDITIONAL** [model only: K6; contradicted: UX]. It reads NOT SUPPORTED under A3′. Under the letter reading
  (A2 and A3 off) it gets no grade ("none") (`applications.txt`, SENSITIVITY).
- **What would raise it.** Nothing in the record's reach. A real test needs a platform's users and data. The honest
  version today is a design statement: an objective set by the user's reflective value (the true map, REDUNDANT) and a
  pause that buys autonomy at some cost in the model's welfare.

## 5. Forecast 4's combination: flexible, pausable fine-tuning that needs no sweep (AP2 + AP9 + K1)

`applications.txt` grades this derived row: **CONDITIONAL** [unreplicated RESULT: K1; model only: K5; assumed: Energy,
Compute].
- **Energy* ASSUMED, not MODELLED.** The pinned estimates are conditional on the method holding and take their saving
  from SCL3 or SEC4, both scored before SEC5-1 failed and before FM6. SEC4-1 is the pass that SEC6-G's rule, applied
  after the fact, would cap at PASS-0 (ledger SEC4-1-G; `SEC_Analysis/checks/gate_posthoc.txt:11`). The consolidated
  estimate's SEC term for 2030 is "0.0742 0.4743 4.0399" TWh (low, middle, high), attributed to "the CRR programme
  (SEC; the ledger: not a CRR rule)"
  (`Energy Design Principle/checks/consolidated_estimate.txt`). Against a reused λ the estimate itself prints no compute
  saving (`Compute_Savings/checks/global_estimate.txt`). The pause half adds no saving (T4).
- **Compute* ASSUMED.** The configuration share was measured on the record's CPU learner (SEC4-K: "CPU share of the
  full sweep 0.0508–0.0655"), not on fine-tuning jobs at scale. The no-lost-work half was measured for a pause at a
  checkpoint, on one stack (RW1).
- It reads NOT SUPPORTED if K1 or K5 is read as CLOSED (`applications.txt`, SENSITIVITY).

## 6. The forecasts, as scored (`applications.txt`, FORECASTS)

The declaration wrote four forecasts before any source or script. They are scored as written.

| forecast | scored | what the script printed (`applications.txt`) |
|---|---|---|
| 1. No application is SUPPORTED; K1 is at most RESULT (SEC4-1) with a failed replication, unless SEC6-1 changes that. | **HOLDS** | "applications SUPPORTED: 0 (none); K1 RESULT, SEC5-1 FAIL, SEC6-1 pending (holds)" |
| 2. AP2, AP3, AP4, AP7 and AP8 are CONSTRUCTION-BACKED. | **FAILS** | "CONSTRUCTION-BACKED 0 of 5"; under the top-down reading "3 of 5 (AP3, AP4, AP8)" |
| 3. AP1 is CONDITIONAL; AP5 is NOT SUPPORTED; AP6 waits on ROB1. | **HOLDS** | "AP1 CONDITIONAL (holds); AP5 NOT SUPPORTED, K4 CLOSED (holds); ROB1 pending, AP6 CONDITIONAL (holds)" |
| 4. The strongest honest case is AP2 + AP9 with K1; still CONDITIONAL; its energy claim MODELLED, not MEASURED at scale. | **FAILS** | "AP2+AP9+K1 CONDITIONAL (holds); its Energy cell ASSUMED, computed from the lines it cites (fails)" |

- **Total:** "forecasts: 1 HOLDS, 2 FAILS, 3 HOLDS, 4 FAILS".
- **Under K1 read as CLOSED,** forecast 3 also fails.
- **What the misses say** (the writer's reading of the printed reasons). The declaration expected the pause
  applications to stand on the construction alone. They do not, for three kinds of reason:
  - AP3, AP4 and AP8 each promise something beyond the construction that the record has not measured or has shown
    false: a detection (AP8), a no-resistance claim (AP4), or no resistance together with privacy (AP3).
  - AP2 also needs K5, which is at MODEL.
  - AP7's own gate closed (`applications.txt`, each application's "because" line).

  The declaration also expected the energy estimate to count as a model of the combination's saving. It does not,
  because the estimate assumes the very thing SEC5-1 and FM6 put in doubt.

## 7. The owner's five dimensions, across all ten applications (`applications.txt`, SUMMARY)

- **User experience.** MEASURED only where the promise is exactness of a pause and resume on one software and hardware
  stack (AP2, AP3, AP4, AP8). AGAINST for the feed (AP10). Everything else is ASSUMED.
- **Energy.** No cell is MEASURED or MODELLED.
  - AGAINST where the claim is that the pause itself saves energy (AP2, AP4, AP9): it moves energy.
  - ASSUMED where the saving would come from discarding the paused work (AP3) or from a client not staying awake
    (AP7).
  - The one energy term the estimate attributes to the record's programme is SEC's sweep saving, conditional on the
    method holding (§5).
- **Security.** No cell is MEASURED. AGAINST twice: a partial checkpoint degrades silently (AP2), and the natural learner
  resists lossy or reset pauses (AP3). The record has no poisoning or backdoor test of any of its methods. Its checks
  for an omitted or altered state work only against an uninterrupted reference run (`c1_c2.txt` G2 and G3; `rw1.txt`
  S2–S5). The M3 dossier reads none of K1–K7 as addressing feedback loops, poisoning, backdoors or erasure
  (`docs/citations/app1_m3_2026-09-30.md`).
- **Privacy.** Every cell is ASSUMED. The route that would have removed stored examples (K4) closed at every gate, and
  a pause erases nothing already learned.
- **Compute.** MEASURED where the claim is that no learning is lost under a held or buffered pause (AP4, AP9). AGAINST where
  the claim is memory: exact state costs 5.274 times the parameters' bytes on the ECE stack (AP3, AP8;
  `Empty_Cut_Engineering/checks/c1_c2.txt`). The sweep saving (AP1, AP6) is ASSUMED, because against a reused value or
  a default there is none.

## 8. What the record supports today, and the strongest honest case

**Supported today: none.** Not one application reaches SUPPORTED or CONSTRUCTION-BACKED on the primary reading. Two are
NOT SUPPORTED: AP5 (K4 closed) and AP7 (its federated-client gate closed).

**What the record can honestly offer** is smaller than an application:
- **A checked construction of existing practice.** A learner's pause and restore can be made exact, bit for bit, on one
  stack, with state closure, own-clock keying and the world held or buffered.
  - This is published practice: the checklist is graded REDUNDANT (C4).
  - The record's measurements of it are its own: every omitted component changes the trajectory
    (`Empty_Cut_Engineering/checks/c1_c2.txt`: "G3: 8 of 8 omitted components change the trajectory"), and a partial
    checkpoint degrades silently on a real stack (`Real_World/RW1.md`).
  - No novelty is claimed for them: auditing a pause by a digest of its state is graded PARTLY REDUNDANT (C1,
    `Lossless_Pause/checks/grade_sweep.txt`). The record's checks detect a bad restore only against an uninterrupted
    reference run.
- **A corrigibility construction for routine pauses.** An own-clock valuation has no stake in a lossless pause, and other
  valuations do (SCL1-2, SCL2-2; a low bar, §1). It is shown on tabular learners and gridworlds only. The sweep did not find the
  own-clock pause as a corrigibility construction; that is not novelty.
- **A single-family result for a sweep-free penalty weight** (K1, RESULT, with the CLOSED sensitivity).
  - SPA1's verdict on the method is KNOWN; only the secant units calibration itself was not found (nearest: RWalk).
  - A frozen learner meets its criterion on most held-out carriers (FM6) and on 5 of SEC4's own 6. SEC6-G's rule,
    applied after the fact, would cap SEC4-1 at PASS-0 (ledger SEC4-1-G).
  - It did not replicate on the next family.

**The strongest honest case** (the writer's judgement; the script scores no such thing). It is AP8, exact restore and
audit, read together with AP4, the operator pause:
- **Why these two.** Each is CONDITIONAL for a single reason: one assumed security cell. Each has its UX cell MEASURED.
  Each reads CONSTRUCTION-BACKED when no cell is load-bearing and under the top-down reading (`applications.txt`,
  SENSITIVITY). Beside them, their AGAINST cells:
  - AP8's Compute: an exact restore point costs 5.274 times the parameters' bytes (`c1_c2.txt`);
  - AP4's Energy: the pause moves energy (T4).
- **What stands in the way.**
  - **AP8 lacks two things.** Detection of a partial or tampered restore without a reference run, which is testable
    on a CPU. And exactness beyond the stack measured, which is not the record's (OPEN-1B, m2:31); restricting AP8 to
    one stack would be a new declaration.
  - **AP4 lacks a measurement on an agent capable of acting (STAKE1-A), with the world held or buffered.** Where the
    world moves on and the pause loses data, the record's natural agent resisted on every carrier (SCL1-3 "lossy 12/12";
    SCL2-3 "lossy 9/9"). So AP4's claim is limited to held or buffered worlds.
- **What it is not.**
  - It is not an energy saving: the pause moves energy.
  - It is not a new capability:
    - exact resume is the Hugging Face Trainer's default (m2:16);
    - bit-exact replay across device counts is published (m2:31);
    - safely interruptible learners are published (m3:11).
  - The record's own-clock pause, read as a corrigibility construction, was NOT FOUND IN THE SWEEP, and the related
    positions are PARTLY REDUNDANT (`AI_Safety/CORRIGIBILITY_2026/checks/grade.txt`). Not found is not novel.
  - The record's checks of a restore need a reference run, so they give an operator no verification method for
    deployment.

**Forecast 4's case is weaker than the declaration expected** (`applications.txt`). Its energy saving is ASSUMED, its
pause half saves nothing, and its K1 half rests on an unreplicated pass with a weak criterion (§5, §3).

## 9. Patent points (information, not legal advice)

- **The record's own prior-art grades.** Each comes from a one-day keyword sweep, and "not found" in a sweep is never
  "novel".
  - **K1:** SPA1's verdict is KNOWN: the clip is AR1's, a path-fitted penalty is Synaptic Intelligence's, and tuning-free
    weights are published. Only the secant calibration of the Fisher's units was not found (nearest: RWalk)
    (`SEC_Prior_Art/checks/grade.txt`; `SEC_Prior_Art/SPA1.md`).
    - On the 30 SEEN carriers (development, not evidence), SI with SEC4's clip (SI-1C) did at least as well as the
      clipped SEC against both references: 28/30 and 30/30, against 26/30 and 22/30.
    - AR1's bound used as the strength (AR1-B) did as well against the tuned λ (27/30) but not against the tuned
      clipped λ (19/30 against 22/30) (`prereg/sec6/dev_SEC6.txt:335-346`; §3).
    - That bears on whether the calibration step itself carries an effect.
  - **K2:** the empty-cut checklist and the own-clock cut are REDUNDANT; a state-digest audit is PARTLY REDUNDANT
    (`Lossless_Pause/checks/grade_sweep.txt`).
  - **K3:** a pause on the agent's own clock as a corrigibility construction is NOT FOUND IN THE SWEEP; the related
    positions are PARTLY REDUNDANT (`AI_Safety/CORRIGIBILITY_2026/checks/grade.txt`).
  - **K5:** the deadline-extension (stop-the-clock) contract is NOT FOUND IN THE SWEEP; slowdown tiers are REDUNDANT,
    and so is the whole position read as one (for comparison only) (`Grid_Demand_Response/checks/grade.txt`); the EPS
    report reads the construction as "Not new".
  - **K6:** the true map is REDUNDANT (U4) (`Attention_Algorithms/checks/grade.txt`).
- **Evidence of an effect.**
  - `Rupture_Detection/RUPTURE_DETECTION.md` §4 reads the EPO Guidelines (G-II 3.3) as: "An applied use case needs a
    technical effect that holds across the claimed scope." It also records the reading that later evidence
    cannot add a use the application as filed does not disclose.
  - The record's only PASS-1 in this area is SEC4-1. It is unreplicated, and SEC6-G's rule, applied after the fact,
    would cap it at PASS-0 (ledger SEC4-1-G).
  - None of the pause applications has a measured effect beyond the construction.
- **The application's text is not in this repository** (`Rupture_Detection/RUPTURE_DETECTION.md` says so). So nothing
  here says what the owner's European application claims. Which of AP1–AP10, if any, it discloses is for a patent
  attorney to read from the application as filed.
- **Publication.** The Rupture Detection note (§4, point 5) records three things:
  - the owner's statement that the repository is being made private;
  - that the material published here between 2026-09-15 and the change "remains prior art against any new European
    filing";
  - that the US one-year grace period for the inventor's own disclosures runs to 2027-09-15.

## 10. What SEC6 (data step 2026-10-01) could change

**What SEC6 is** (`prereg/sec6/PREREG.md`):
- SEC4's clipped SEC, unchanged, on a fifth unseen family: OpenML study 454, twelve carriers drawn from metadata only.
- It is scored three ways:
  - against the tuned λ (SEC6-1, the replication of SEC4-1);
  - against a tuned λ given the same clip (SEC6-C);
  - against the published tuning-free rules SI and AR1 in their registered forms, and raw Laplace (SEC6-B).
- Instrument gates are computed first. SEC6-G asks whether a learner frozen after task 1 also meets SEC6-1's criterion.
  SEC6-GC asks the same for SEC6-C's criterion.
- The same rule, applied after the fact to the earlier rows, closes the gate for SEC4-1, SEC3-3 and SEC5-1 and leaves
  it open for SCL3-3 (`SEC_Analysis/checks/gate_posthoc.txt`; ledger report rows SCL3-3-G to SEC5-1-G). Those rows stand
  as scored.
- Its hash and OpenTimestamps stamp come before any carrier is fetched, and no carrier is fetched or opened before
  2026-10-01 00:00 UTC. The metadata already warn that N may fall well below 12; if N < 4, SEC6-1, SEC6-B and SEC6-C are
  NOT DECIDABLE.

**What each outcome would do to K1 and to the applications.** The readings of SEC6 are the pre-registration's; the
effect on APP1's grades is the writer's reading of the declaration's rules, to be confirmed by rerunning the two scripts
once the rows exist.

| SEC6 outcome (`prereg/sec6/PREREG.md`) | K1 | the applications |
|---|---|---|
| SEC6-G CLOSED ("a learner frozen after task 1 meets the same criterion") | SEC6-1, SEC6-B and SEC6-P are printed UNINFORMATIVE and capped at PASS-0. K1 stays a RESULT on SEC4-1 alone, and the reading behind the K1 → CLOSED sensitivity (FM6) holds on a fifth family too, as it already does post hoc on SEC4's own (ledger SEC4-1-G). | AP1, AP6 and the combination stay CONDITIONAL; they read NOT SUPPORTED under K1 → CLOSED. |
| SEC6-G OPEN and SEC6-1 at PASS-1 (SEC6-S not fragile, SEC6-2 passes, OTS completes, admissibility as stated) | The pre-registration reads SEC4-1 and SEC6-1 together as PASS-2 "by the letter of CLAUDE.md §7", with SEC5-1's failure printed beside them. Beside that stands SEC4-1-G: under SEC6-G's own rule, applied after the fact, SEC4-1 "would be printed UNINFORMATIVE and capped at PASS-0" (`gate_posthoc.txt:11`). So on the reading behind K1's CLOSED sensitivity, SEC4-1 is not a PASS-1 to pair with SEC6-1, and the pair is not a PASS-2. On the primary reading, once the ledger records the PASS-2, K1 would read FINDING. The rerun scripts, not this note, decide which they print. | The "unreplicated RESULT" reason leaves AP1, AP6 and the combination, and each stays CONDITIONAL: AP1 on its assumed UX and Compute cells; AP6 on its assumed UX, Security and Compute cells and on ROB1; the combination on K5 (MODEL) and its assumed Energy and Compute cells. AP5 stays NOT SUPPORTED on K4. None can become SUPPORTED, because each also needs K2, a construction, or K4. |
| SEC6-GC CLOSED | SEC6-C is capped at PASS-0 ("If SEC6-GC is CLOSED, SEC6-C is at most PASS-0"). | No change of grade. |
| SEC6-1 passes and SEC6-C fails | The pre-registration's reading: "the pass rests on the clip: a tuned λ given the same guard beats it". If SEC6-1 is also PASS-1, the PASS-2 row must print "SEC6-1 rests on the clip (SEC6-C fails)". | The saving becomes a trade: one configuration instead of a sweep, at an accuracy below that of a sweep run with the same clip (the UX and Compute cells of AP1, AP6 and the combination). |
| SEC6-G OPEN, SEC6-1 at PASS-0 only (a PASS-1 condition fails), or N < 4 (NOT DECIDABLE) | K1 stays a RESULT on SEC4-1 alone. | No change of grade. |
| SEC6-B fails | The pre-registration's reading: "a published tuning-free rule does at least as well. On SEEN data SI-1C and AR1-B already do. The calibration is then not what makes the clipped SEC work." On SEEN data that holds against the tuned λ, SEC6-B's reference (development runs, not evidence; §3). | K1's capability would be served by published rules plus a clip. Its prior-art position (KNOWN) would then cover the part that works. |
| SEC6-1 fails | The clipped SEC is not tuning-free on a third new family. K1 stays a RESULT on SEC4-1 alone, with two failed replications beside it. | No change of grade. The case for AP1, AP6 and the combination weakens further. |
| SEC6-T fails or is not decidable | "a reused λ would have saved the sweep without SEC" | It bears on every Compute cell that counts a sweep saved. Against a reused value there is none (`Compute_Savings/checks/global_estimate.txt`). |
| SEC6-K (a report) | The clipped SEC's CPU seconds against the full sweep, including the clipped sweep's, on a fifth family. | A measured compute share on the record's CPU learner. It is not a device, robot or fine-tuning measurement. |

**What SEC6 cannot change.**
- The grades of K2–K7 (SEC6 tests none of them).
- The pause's energy grade: AGAINST wherever the pause itself is claimed to save energy (AP2, AP4, AP9).
- AP5 and AP7 NOT SUPPORTED; AP3's Security AGAINST; AP10's UX AGAINST.
- Whether any application is SUPPORTED: none can be, since every application that needs K1 also needs K2 (AP1, AP6)
  or K4 (AP5).

**After SEC6.** The rows are appended to `ledger/LEDGER.md`, and `Applied_Suite/checks/capabilities.py` and
`Applied_Suite/checks/applications.py` are rerun and re-pinned. They read SEC6-1 and SEC6-G by id (both are printed
PENDING now, `capabilities.txt`). Where this note and the re-pinned outputs then differ, the outputs are right.

**The test after SEC6** that `SEC_Analysis/WHY_SEC4_WORKED.md` names is a stream where the criterion can fail by
design (a random class order, or balanced accuracy). It would be a new pre-registration on a later day.

## Reproduce

```
uv run python Applied_Suite/checks/capabilities.py | cmp - Applied_Suite/checks/capabilities.txt
uv run python Applied_Suite/checks/applications.py | cmp - Applied_Suite/checks/applications.txt
# verify.py reads the fetched texts under /tmp/claude-0/app1_src (outside the repository): rerun by hand
uv run python Applied_Suite/checks/verify.py | cmp - Applied_Suite/checks/verify.txt
```
