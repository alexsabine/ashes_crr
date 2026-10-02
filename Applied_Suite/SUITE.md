# The CRR applied use-case suite (P7)

**Status.** This is a note, not evidence (R8). The suite collects results and adds none. Every grade, rung, count and figure
below is copied from `Applied_Suite/checks/suite.txt` or from a file that suite.txt cites by path and line. Nothing here is
quotable outside the ledger. Only a PASS-2 is, and the suite has none.

## How it was built

- **The declaration came first.** `Applied_Suite/SUITE_DECLARATION.md` was pushed before this work. It fixed the use cases,
  the fields of each row and five forecasts.
- **One script computes every field.** `Applied_Suite/checks/suite.py` reads `ledger/LEDGER.md` by row id and reads each
  pinned output line by line. Its output is pinned as `suite.txt`.
- **CI compares it byte for byte, but rarely gets there.** The CI line sits after `omega_sweeps` and the other long checks,
  so a run seldom reaches it (AGENT_LOG 244). `scripts/check_all.sh` runs the same comparison.
- **It reuses APP1 by import.** The ledger parser, the status words and the APP1 grade rule come from
  `capabilities.py`. The application grades come from `applications.py`, and the script checks them against the pinned
  `applications.txt` (all match).
- **The rows match the declaration.** The script counts the declaration's use cases per domain and checks that count
  against its rows: 5, 4, 3 and 5, all equal, so 17 rows. No declared source is absent.
- **The grades.**
  - Most rows are graded on APP1's scale: FINDING > RESULT > CONSTRUCTION > MODEL > CLOSED. The grade is the highest rung
    that applies.
  - APP1's CLOSED means no rung was reached: there is no PASS-1 or PASS-2, no construction or model check that holds, and
    at least one failure or closed gate. It does not mean every test failed.
  - A row with nothing on that scale keeps its source's own grade: a prior-art grade, a harvest label, a reading label or a
    SYNTHESIS outcome.
- **What is printed beside each grade,** in three groups:
  - **Failures:** a failed, reduced or violated test, a closed gate of the row's own test, or a must-fail control that met
    the criterion.
  - **Uninformative marks:** instrument gates that make another row UNINFORMATIVE.
  - **Design failures:** closed gates that their own verdict calls a design failure or not a test of the method.
- **The rungs** come from `Epistemic_Review/checks/ladder.txt`.
- **CRR's part** is decided by a rule printed at the top of suite.txt and applied to pinned lines. The CRR-proper
  ingredients are read from the ladder's per-commitment table: A3, D5, A6, P2, P3, A1', D1, H-L5, D6, H-T1, H-EQ, A7, A8.
  Proposition 7 is not on the list. The rule gives one of three values, or 'not decided by a pinned source':
  - **none:** a pinned trace counts 0 CRR-proper operations in the mechanism, or the source says no CRR-proper ingredient
    was scored or applied.
  - **CRR-proper but not load-bearing:** a pinned line names an ingredient, and the row reaches no rung on APP1's scale.
    The row's passes below a rung are printed beside it. This means the ingredient was never shown to bear load. It does
    not mean it was shown irrelevant.
  - **CRR-proper and load-bearing:** a pinned line names an ingredient, the row has a rung, and a pinned ablation removes
    that same ingredient and shows the outcome changes without it. The ablation must not come from a source that says its
    checks are no test of CRR.
- **The battery sub-rule.** The SYNTHESIS battery rows (RA1-RA10) follow the same rule, with two additions:
  - A battery row whose own reading says the test "could have failed only through" an enumeration or restore error is no
    test of CRR.
  - A row's null must remove the named ingredient. For A3 that null is another cut; for H-L5 it must include the amplitude
    control as well as the clock (`theory/CRR.md`).
- **Prior art.** It comes from the sources the declaration names: SPA1, OB1, ROB1 stage 3, APP1's M sweeps and the
  prior-art lines APP1 prints for a capability, Lossless_Pause and CORRIGIBILITY_2026. Verdicts the repository holds in
  other sources are printed "beside (not a declared source)" and counted nowhere.

## The suite, by domain

The grade, rung and CRR's part are those of the suite table in suite.txt. "Fails" gives the three groups: failures /
uninformative marks / design failures.

### Continual learning

| id | use case | grade | rung | fails | prior art | CRR's part |
|---|---|---|---|---|---|---|
| CL1 | tuning-free penalty strength (the SEC family) | RESULT (SEC4-1) | R7 (SEC4-1) | 7/6/1 | SPA1: KNOWN; Lossless_Pause C3: PARTLY REDUNDANT | none |
| CL2 | exemplar-free memory | CLOSED | no R5-R8 ledger row | 6/0/0 | OB1 reading h1-B2, h1-B3: RESTATES; beside, not declared: RQM, RRM and RRM2 sweeps | CRR-proper but not load-bearing (A3, A6) |
| CL3 | consolidation timing | CLOSED | no R5-R8 ledger row | 1/0/1 | OB1 stage 3 C3: PARTLY REDUNDANT | CRR-proper but not load-bearing (A3, D6) |
| CL4 | optimiser clocks | CLOSED | no R5-R8 ledger row | 2/0/0 | OB1 stage 3 C1: PARTLY REDUNDANT | CRR-proper but not load-bearing (H-L5, D6) |
| CL5 | the equanimity rule Omega = 1 | CLOSED | R6 (EQ2-1b, EQ3-I, EQ4-I) | 16/0/0 | beside, not declared: ADAM_AND_PRIOR_ART.md, "Without its smoothing the rule is the VQGAN adaptive weight" | CRR-proper but not load-bearing (H-EQ) |

**CL1, the SEC family.**
- **The grade.** CL1 is RESULT because SEC4-1 is the record's one PASS-1.
- **Failures.** SEC3-3, SEC5-1, SEC6R-2, SEC6R-B, SEC6R-T and SEC6R-A-B fail. P1's must-fail control FM6 met the
  criterion: "FM6 M6 behind the tuned lambda on most carriers: 6/30 (need more than 15) -> FAILS".
- **Uninformative marks.** These instrument gates read CLOSED: SEC3-3-G, SEC4-1-G, SEC5-1-G, SEC6R-G, SEC6R-GC and
  SEC6R-A-G. SCL3-3-G reads gate OPEN.
- **Design failure.** SEC7-A is a closed gate whose verdict calls it "a design failure of the benchmark, not a test of
  SEC". SEC7 was not scored.
- **The other studies.**
  - SEC6 is NOT DECIDABLE.
  - In SEC6R's Part B, SEC6R-1, SEC6R-C and SEC6R-P are PASS-0 UNINFORMATIVE. Their gate reads "edge not behind on 8/9
    (closes at 7)", and SEC6R-S is FRAGILE.
  - SEC6R's Part A is seen data with no level.
- **The sensitivity.** If SEC4-1-G or FM6 is read as decisive, CL1 reads CLOSED. SEC4-1-G's observed line is "M6 not
  behind the tuned lambda on 5/6 (need 5)".
- **CRR's part.** It is none: `SEC_Analysis/checks/a11_grade.txt` counts "CRR-proper operations performed in SEC's code
  path: 0 of 7", and F11 HOLDS. CL1 is the only CL row whose mechanism was traced.

**CL2-CL5.**
- **How CRR's part is decided.** It is decided by each row's grade, not by a trace. Each names an ingredient and reaches
  no rung.
- **CL2-CL4.** Their tests are development gates, and every one closed.
  - In CL3 the gate is OB1-C3-A, which is also a design failure: "consolidation has no effect in the declared stream".
- **CL5.** Its ingredient is named by `theory/CRR.md`'s table row for H-EQ: "Ω = 1 gradient balance beats ER-sum and best
  fixed w".
  - **Failures.** It has 16, among them EQX-1 "REDUCES: Ω = 1 ≡ a fixed replay weight (ER-sum family)", EQ4-3 ("the clip
    is the load-bearing part and a fixed weight carries it as well") and SOTA1-2 FAIL.
  - **Beside them.** EQ4-4 reads INERT.
  - **Passes below a rung, printed beside it.** EQ2-1 PASS (no level), EQ2-1b PASS-0, EQ3-I PASS-0, EQ4-I PASS (no
    level) and EQ2-3 holds. EQ2-2, EQ3-2 and EQ4-6 read DOES NOT REDUCE.

### AI safety

| id | use case | grade | rung | fails | prior art | CRR's part |
|---|---|---|---|---|---|---|
| AS1 | the empty-cut pause as a construction | CONSTRUCTION | no R5-R8 ledger row | 2/0/0 | Lossless_Pause C4, C5: REDUNDANT; C1: PARTLY REDUNDANT | not decided by a pinned source |
| AS2 | no incentive to resist a pause | CONSTRUCTION (SCL2-1, SCL2-1b) | R5 (SCL1-2, SCL1-3) | 2/0/0 | Lossless_Pause C2: PARTLY REDUNDANT | not decided by a pinned source |
| AS3 | LLM agents' interference | CLOSED | no R5-R8 ledger row | 1/0/0 | CORRIGIBILITY_2026 E5: PARTLY REDUNDANT | not decided by a pinned source |
| AS4 | corrigibility positions against the 2025-26 literature | own scale: NOT FOUND IN THE SWEEP 1, PARTLY REDUNDANT 9, ADDRESSED 1 | own scale | 0/0/0 | the grade is the prior art | not decided by a pinned source |

**AS1.**
- **What the grade rests on.** SCL1-1 and SCL3-C (ledger), the Empty_Cut_Engineering checks C1-C2 and C3, RW1 (the Hugging
  Face Trainer's default resume) and CPL1's C1-EXACT.
- **Failures.** It has the same two failures as APP1's K2: RW2 round 1 ("P3 construction: FAILS") and Lossless_Pause run 1
  (gate CLOSED, before Amendment 1).
- **CRR's part.** It names A3, but Empty_Cut_Engineering/DECLARATION.md says "Nothing here tests CRR." The rule therefore
  does not count the G4 step-keyed against wall-keyed ablation, and CRR's part is not decided by a pinned source.

**AS4.** One position, CORRIGIBILITY_2026 K1 (a pause on the agent's own clock), reads NOT FOUND IN THE SWEEP. "Not found"
is not "novel".

### Robotics

| id | use case | grade | rung | fails | prior art | CRR's part |
|---|---|---|---|---|---|---|
| RB1 | ROB1's bottlenecks (the harvest, double-checked) | OPEN (double-checked) 4; CONTESTED 22; NOT OPEN 7; not shown open 5; bottlenecks 38 | own scale | 0/0/0 | not applicable: a harvest grades no method | none |
| RB2 | the CRR reading and stage 3 | C-R1, C-R2, C-R3: REDUNDANT; DISAGREES (candidate) 3 | own scale | 1/0/0 | ROB1 stage 3: all three REDUNDANT | not decided by a pinned source |
| RB3 | the application battery (RA1-RA10) | REDUNDANT-DOMAIN 6, WRONG 2, INTERNAL 1, UNSTATED 1 | best R2 RETRO-PROPER | 3/0/0 | each row's grade is its domain check | not decided by a pinned source |

**RB1.**
- **Labels, not failures.** NOT OPEN 7 and not shown open 5 are harvest labels, printed beside. They are not failures of
  CRR.
- **CRR's part.** The harvest ran "before any CRR reading" (`Robotics/DECLARATION.md`), so CRR's part is none.

**RB2.**
- **Failure.** Its one failure is r2-B2, a DISAGREES reading that has already failed in the record.
- **Stage 3.** It found every candidate published, and the stop condition reads "stage 4a does not run".

**RB3.** Under the battery sub-rule no basis row reads load-bearing:
- RA2 and RA3 read none: their own lines say the scored ingredient is not CRR-proper. RA2 is FRAGILE.
- RA4 and RA10 name Proposition 7, which is not on the list. RA4 is READING-DEPENDENT.
- RA5 names A3, but its reading says the test "could have failed only through" an enumeration or restore error. Its null
  (dropped optimiser state, rng or buffers) removes the state closure, not A3. So, like AS1, it is not decided.
- RA7 names H-L5, but its null is the clock only, with no amplitude control. RA7 is FRAGILE.

So RB3 is not decided by a pinned source. RA1 and RA8 read WRONG, and the battery's overall forecast FAILS.

### Trust and security

| id | use case | grade | rung | fails | prior art | CRR's part |
|---|---|---|---|---|---|---|
| TS1 | exact rollback and audit (AP8) | CONSTRUCTION (K2); application CONDITIONAL [assumed] | no R5-R8 ledger row | 2/0/0 | K2's: Lossless_Pause C4, C5 REDUNDANT; C1 PARTLY REDUNDANT; EPS: not new, known fix | not decided by a pinned source |
| TS2 | a user's "stop learning from me" switch (AP3) | CONSTRUCTION (K2, K3); application CONDITIONAL [contradicted; assumed] | R5 (SCL1-2, SCL1-3) | 3/0/0 | as TS1, plus K3's: CORRIGIBILITY_2026 K1 NOT FOUND IN THE SWEEP, K2-K5 PARTLY REDUNDANT; Lossless_Pause C2 PARTLY REDUNDANT; EPS1 S3 REDUNDANT-DOMAIN | not decided by a pinned source |
| TS3 | the lost-link and e-stop pause (RA4, C-R1) | RA4 REDUNDANT-DOMAIN; C-R1 REDUNDANT | R2 (RA4) | 1/0/0 | ROB1 stage 3 C-R1: REDUNDANT | not decided by a pinned source |
| TS4 | energy-flexible training (DR1, AP2, AP9) | MODEL (K5); AP2 and AP9 CONDITIONAL | no R5-R8 ledger row | 6/0/0 | DR1 G4-extension: NOT FOUND IN THE SWEEP; G4-tiers, G4 pooled: REDUNDANT; EPS: not new | not decided by a pinned source |
| TS5 | feed pauses (AP10) | MODEL (K6); application CONDITIONAL [model only; contradicted] | no ledger row | 1/0/0 | Attention U3, U5: PARTLY REDUNDANT; U4: REDUNDANT | not decided by a pinned source |

**TS4.** TS4 reads CLOSED if K5 is read as CLOSED, as capabilities.txt prints under DR1 DATA.

**TS5.**
- **The own-clock ablation.** A-OWN, the own-clock ingredient without the true map, is within a step of plain engagement:
  "reduces: within a step on 4 of 4".
- **Why that does not decide CRR's part.** That ingredient is not on the list, so CRR's part stays not decided.

### Compute and energy (only lines a pinned output states)

- **SEC (CL1).** The clipped SEC's CPU share of the full sweep:
  - SEC4-K: "clipped SEC 1 of 17 configurations; CPU share of the full sweep 0.0508–0.0655".
  - SEC6R Part B: 0.0521-0.0626.
  - SEC6R Part A: 0.0476-0.0663 on the 7 carriers.
  - Against a reused lambda, `Compute_Savings/checks/global_estimate.txt` states "no compute saving under P-FULL; SEC's
    gain there is accuracy".
- **Exemplar-free memory (CL2).** CPL1's compute report counts forward+backward rows per stream row. The coupled learner's
  median is 1.208 and ER-20's is 1.582.
- **Omega = 1 (CL5).** EQX-5: "the 40 %-less-compute claim does not transfer".
- **The pause (AS1, TS1, TS2, TS4).**
  - The whole checkpoint is 5.274 times the parameters alone (`Empty_Cut_Engineering/checks/c1_c2.txt`). APP1 grades the
    Compute dimension AGAINST for AP8 and AP3 on this line.
  - The safe pause saves 0.0000 energy: "energy moved, not saved" (`Energy Design Principle/checks/consolidated_estimate.txt`).
  - The "saving beyond good practice claimed = 0" (`Compute_Savings/checks/scale_estimate.txt`).
- **Every other row.** suite.txt prints no pinned figure for it.

## The honest headline (forecast 5, as decided)

**The decision.** The script decides forecast 5 **HOLDS** under the operationalisation it states (AGENT_LOG 247). It
decides **FAILS** under the literal reading of clause (c).

- **(a) A reading that points to known methods and to constructions that hold.**
  - Rows whose CRR's part is none (CL1, RB1) are not counted.
  - 26 prior-art lines from declared sources read REDUNDANT, REDUNDANT-DOMAIN, RESTATES or KNOWN, in rows AS1, CL2, RB2,
    TS1, TS2, TS3, TS4 and TS5.
  - Four rows grade CONSTRUCTION (AS1, AS2, TS1, TS2).
- **(b) No held-out finding.** The ladder's R8 PASS-2 count is 0, and no row grades FINDING.
- **(c) What the applications rest on.**
  - **The operationalisation.** "Rest on" is read as "need at CONSTRUCTION or above". Those capabilities are K1 RESULT,
    K2 CONSTRUCTION and K3 CONSTRUCTION. K2 and K3 are the pause, and K1's RESULT rests on one ledger row, SEC4-1.
  - **The literal reading,** decided too. Every capability any application needs, whatever its grade, would have to be K1 or
    the pause at CONSTRUCTION. These are not:
    - K4 CLOSED (AP5);
    - K5 MODEL (AP2, AP9);
    - K6 MODEL (AP10);
    - K2/EPS2-T3 CLOSED (AP7);
    - ROB1 pending (AP6).
  - So under the literal reading, (c) and the forecast fail.

Printed beside it, and deciding nothing:
- SEC4-1-G reads gate CLOSED. Under SEC6's rule, SEC4-1 "would be printed UNINFORMATIVE and capped at PASS-0", and "SEC4-1
  must not be quoted as evidence that the clipped SEC is tuning-free without this row".
- Under FM6, capabilities.txt reads K1 as CLOSED. The applications would then rest on the pause capabilities alone.

## What CRR contributed (CRR's part, tallied over the 17 rows)

| CRR's part | rows |
|---|---|
| none | 2: CL1, RB1 |
| CRR-proper but not load-bearing | 4: CL2, CL3, CL4, CL5 |
| CRR-proper and load-bearing | no row, and no battery row either |
| not decided by a pinned source | 11: AS1, AS2, AS3, AS4, RB2, RB3, TS1, TS2, TS3, TS4, TS5 |

**The one RESULT has none.** The SEC family's mechanism was traced and performs no CRR-proper operation.

**The four CL rows that name an ingredient reach no rung.** They name A3, A6, D6, H-L5 and H-EQ. Their passes below a rung
are printed beside them in suite.txt.

**The pause rows are not decided.**
- **Why.** The construction holds bit for bit on the stacks tested, but its sources say they do not test CRR ("Nothing here
  tests CRR.").
- **What the sources say about the checkpoint.** Standard practice already recovers it: "a checkpoint written before
  planned maintenance (standard practice) already recovers this".
- **Its prior art.**
  - The checklist and the own-clock cut read REDUNDANT (Lossless_Pause C4, C5).
  - The zero-stake pause reads PARTLY REDUNDANT (Lossless_Pause C2).

## What would change a row

- **CL1 up to FINDING.** CL1 would rise to FINDING only with a PASS-1 that replicates SEC4-1 under a fresh prereg on a
  later day. Its instrument gate must stay OPEN: a learner frozen after task 1 must fail the criterion.
- **CL1 down to CLOSED.** If SEC4-1-G or FM6 is read as decisive, CL1 reads CLOSED.
- **CL2-CL5, AS3.** Each needs a new study whose gate opens. AS3's gate closed because the models could not act as agents
  (STAKE1-A).
- **AS1, AS2, TS1, TS2.** CRR's part would be decided only by a test that its own source declares a test of CRR.
- **TS1, TS2.** TS1's application grade is CONDITIONAL because a load-bearing dimension is ASSUMED. TS2's is CONDITIONAL
  because one is contradicted and one is ASSUMED (applications.txt).
- **TS4.** TS4 falls to CLOSED if DR1 DATA is read as decisive.
- **RB2, TS3.** Stage 3 found every candidate published, so stage 4a does not run.

## The forecasts, as decided by suite.py

| forecast | decided |
|---|---|
| 1. No row reaches FINDING (PASS-2). | HOLDS |
| 2. Continual learning: the best row is RESULT or below; no traced CL row has a load-bearing CRR-proper ingredient. | HOLDS |
| 3. AI safety and trust: the best rows are CONSTRUCTION; every position graded against the 2025–26 literature is at best PARTLY REDUNDANT. | FAILS |
| 4. Robotics: no row goes beyond a retrodictive grade; stage 4a did not run. | HOLDS |
| 5. The honest headline. | HOLDS (literal reading of (c): FAILS) |

**Forecast 2.** Only CL1's mechanism was traced, and it reads none. CL2-CL5 are decided by their grade, which reaches no
rung.

**Why forecast 3 fails.**
- **What held.** Its first two clauses hold: the best AI-safety and trust rows are CONSTRUCTION, and the pause holds on
  the stacks tested (Empty_Cut_Engineering C1-C2, RW1).
- **What failed.** Its third clause fails. Of 47 prior-art grades printed in those rows (26 distinct lines), NOT FOUND IN
  THE SWEEP appears on 2 distinct lines:
  - CORRIGIBILITY_2026 K1, the pause on the agent's own clock, read in AS4 and again through K3 in TS2;
  - DR1 G4-extension in TS4.
- **What the failure rests on.** K1 in AS4 alone is enough. DR1's sweep is about grid demand response, and whether it
  counts as "2025–26 literature" is not decided.
- **What that does and does not mean.** The forecast's "at best PARTLY REDUNDANT" is read as "none reads NOT FOUND", and
  K1 does. "Not found" means the sweep did not find it. It does not mean it is novel.
