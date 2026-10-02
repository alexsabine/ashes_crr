# The CRR applied use-case suite (P7)

**Status.** This is a note, not evidence (R8). The suite collects results and adds none. Every grade, rung, count and figure
below is copied from `Applied_Suite/checks/suite.txt` or from a file that suite.txt cites by path and line. Nothing here is
quotable outside the ledger. Only a PASS-2 is, and the suite has none.

## How it was built

- **The declaration came first.** `Applied_Suite/SUITE_DECLARATION.md` was pushed before this work. It fixed the use cases,
  the fields of each row and five forecasts.
- **One script computes every field.** `Applied_Suite/checks/suite.py` reads `ledger/LEDGER.md` by row id and reads each
  pinned output line by line. Its output is pinned as `suite.txt`, which CI reruns and compares byte for byte.
- **It reuses APP1 by import.** The ledger parser, the status words and the APP1 grade rule come from
  `capabilities.py`. The application grades come from `applications.py`, and the script checks them against the pinned
  `applications.txt` (all match).
- **The rows match the declaration.** The script counts the declaration's use cases per domain and checks that count
  against its rows: 5, 4, 3 and 5, all equal, so 17 rows. No declared source is absent.
- **The grades.**
  - Most rows are graded on APP1's scale: FINDING > RESULT > CONSTRUCTION > MODEL > CLOSED. The grade is the highest rung
    that applies, and the failures of the same kind are printed beside it.
  - A row with nothing on that scale keeps its source's own grade: a prior-art grade, a harvest label, a reading label or a
    SYNTHESIS outcome.
- **The rungs** come from `Epistemic_Review/checks/ladder.txt`.
- **CRR's part** is decided by a rule declared at the top of suite.txt and applied to pinned lines. The CRR-proper
  ingredients are read from the ladder's per-commitment table: A3, D5, A6, P2, P3, A1', D1, H-L5, D6, H-T1, H-EQ, A7, A8.
  The rule gives one of three values, or 'not decided by a pinned source':
  - **none:** a pinned trace counts 0 CRR-proper operations in the mechanism, or the source says no CRR-proper ingredient
    was scored or applied.
  - **CRR-proper but not load-bearing:** a pinned line names an ingredient, and every test of it closed its gate, failed or
    reduced. This means it was never shown to bear load. It does not mean it was shown irrelevant.
  - **CRR-proper and load-bearing:** a pinned line names an ingredient, the row has a rung, and a pinned ablation shows the
    outcome changes without it. The ablation must not come from a source that says its checks are no test of CRR.

## The suite, by domain

The grade, rung, failure count and CRR's part are those of the suite table in suite.txt.

### Continual learning

| id | use case | grade | rung | failures beside | prior art | CRR's part |
|---|---|---|---|---|---|---|
| CL1 | tuning-free penalty strength (the SEC family) | RESULT (SEC4-1) | R7 (SEC4-1) | 14 | SPA1: KNOWN; Lossless_Pause C3: PARTLY REDUNDANT | none |
| CL2 | exemplar-free memory | CLOSED (every failure a closed gate) | no R5-R8 ledger row | 6 | none from the declared sources | CRR-proper but not load-bearing (A3, A6) |
| CL3 | consolidation timing | CLOSED (every failure a closed gate) | no R5-R8 ledger row | 2 | OB1 stage 3 C3: PARTLY REDUNDANT | CRR-proper but not load-bearing (A3, D6) |
| CL4 | optimiser clocks | CLOSED (every failure a closed gate) | no R5-R8 ledger row | 2 | OB1 stage 3 C1: PARTLY REDUNDANT | CRR-proper but not load-bearing (H-L5, D6) |
| CL5 | the equanimity rule Omega = 1 | CLOSED (a test failed) | R6 (EQ2-1b, EQ3-I, EQ4-I) | 16 | none from the declared sources | CRR-proper but not load-bearing (H-EQ) |

**CL1, the SEC family.**
- **The grade.** CL1 is RESULT because SEC4-1 is the record's one PASS-1.
- **The failures beside it.** SEC3-3, SEC5-1, SEC6R-2, SEC6R-B, SEC6R-T and SEC6R-A-B fail. SEC7-A is a closed gate.
- **The instrument gates.** The instrument gates SEC3-3-G, SEC4-1-G, SEC5-1-G, SEC6R-G, SEC6R-GC and SEC6R-A-G read
  CLOSED, some post hoc and some registered. P1's must-fail control FM6 also met the criterion: "FM6 M6 behind the tuned
  lambda on most carriers: 6/30 (need more than 15) -> FAILS".
- **The other studies.**
  - SEC6 is NOT DECIDABLE.
  - SEC6R's passes are PASS-0 UNINFORMATIVE: its gate reads "edge not behind on 8/9 (closes at 7)", and SEC6R-S is FRAGILE.
- **The sensitivity.** If SEC4-1-G or FM6 is read as decisive, CL1 reads CLOSED. SEC4-1-G's observed line is "M6 not
  behind the tuned lambda on 5/6 (need 5)".
- **CRR's part.** CRR's part is none: `SEC_Analysis/checks/a11_grade.txt` counts "CRR-proper operations performed in SEC's
  code path: 0 of 7", and F11 HOLDS.

**CL2-CL5.**
- **Gates.** Every gate in the memory, consolidation and optimiser-clock rows closed.
- **CL5's ledger rows.**
  - Its 16 failures include EQX-1 REDUCES and SOTA1-2 FAIL.
  - Its PASS-0 rows (EQ2-1b, EQ3-I, EQ4-I) do not reach a rung on APP1's scale.

### AI safety

| id | use case | grade | rung | failures beside | prior art | CRR's part |
|---|---|---|---|---|---|---|
| AS1 | the empty-cut pause as a construction | CONSTRUCTION | no R5-R8 ledger row | 0 | Lossless_Pause C4, C5: REDUNDANT; C1: PARTLY REDUNDANT | not decided by a pinned source |
| AS2 | no incentive to resist a pause | CONSTRUCTION (SCL2-1, SCL2-1b) | R5 (SCL1-2, SCL1-3) | 2 | Lossless_Pause C2: PARTLY REDUNDANT | not decided by a pinned source |
| AS3 | LLM agents' interference | CLOSED (every failure a closed gate) | no R5-R8 ledger row | 1 | CORRIGIBILITY_2026 E5: PARTLY REDUNDANT | not decided by a pinned source |
| AS4 | corrigibility positions against the 2025-26 literature | own scale: NOT FOUND IN THE SWEEP 1, PARTLY REDUNDANT 9, ADDRESSED 1 | own scale | none defined | the grade is the prior art | not decided by a pinned source |

**AS1.**
- **What the grade rests on.** SCL1-1 and SCL3-C (ledger), the Empty_Cut_Engineering checks C1-C2 and C3, RW1 (the Hugging
  Face Trainer's default resume) and CPL1's C1-EXACT.
- **CRR's part.** The pause construction names A3. Its own declaration says "Nothing here tests CRR." The rule therefore
  does not count the G4 clock ablation as a test of CRR, and CRR's part is not decided by a pinned source.

**AS4.** One position, K1 (a pause on the agent's own clock), reads NOT FOUND IN THE SWEEP. "Not found" is not "novel".

### Robotics

| id | use case | grade | rung | failures beside | prior art | CRR's part |
|---|---|---|---|---|---|---|
| RB1 | ROB1's bottlenecks (the harvest, double-checked) | OPEN (double-checked) 4; CONTESTED 22; NOT OPEN 7; not shown open 5; bottlenecks 38 | own scale | 1 (NOT OPEN 7; not shown open 5) | none | none |
| RB2 | the CRR reading and stage 3 | C-R1, C-R2, C-R3: REDUNDANT; DISAGREES (candidate) 3 | own scale | 1 (r2-B2, already failed in the record) | ROB1 stage 3: all three REDUNDANT | not decided by a pinned source |
| RB3 | the application battery (RA1-RA10) | REDUNDANT-DOMAIN 6, WRONG 2, INTERNAL 1, UNSTATED 1 | best R2 RETRO-PROPER | 3 | none from the declared sources | not decided by a pinned source |

**RB1.** The harvest ran "before any CRR reading" (`Robotics/DECLARATION.md`), so CRR's part is none.

**RB2.** Stage 3 found every candidate published. The stop condition reads "stage 4a does not run".

**RB3.**
- **Its basis rows disagree on CRR's part.**
  - RA2 and RA3 read none: their own lines say the scored ingredient is not CRR-proper.
  - RA5 and RA7 read CRR-proper and load-bearing, but only in their own synthetic models, where the result is the domain's
    known one (REDUNDANT-DOMAIN).
  - RA4 and RA10 name Proposition 7, which is not on the list.
- **The row as a whole** is therefore not decided by a pinned source.
- **Failures and limits.**
  - RA1 and RA8 read WRONG, and the battery's overall forecast FAILS.
  - RA2 and RA7 are FRAGILE.

### Trust and security

| id | use case | grade | rung | failures beside | prior art | CRR's part |
|---|---|---|---|---|---|---|
| TS1 | exact rollback and audit (AP8) | CONSTRUCTION (K2); application CONDITIONAL [assumed] | no R5-R8 ledger row | 2 | K2's: Lossless_Pause C4, C5 REDUNDANT; C1 PARTLY REDUNDANT; EPS: known | not decided by a pinned source |
| TS2 | a user's "stop learning from me" switch (AP3) | CONSTRUCTION (K2, K3); application CONDITIONAL [contradicted; assumed] | R5 (SCL1-2, SCL1-3) | 3 | as TS1, plus K3's: CORRIGIBILITY_2026 K1 NOT FOUND IN THE SWEEP, K2-K5 PARTLY REDUNDANT | not decided by a pinned source |
| TS3 | the lost-link and e-stop pause (RA4, C-R1) | RA4 REDUNDANT-DOMAIN; C-R1 REDUNDANT | R2 (RA4) | 1 (RA1, RA8 WRONG in the same battery) | ROB1 stage 3 C-R1: REDUNDANT | not decided by a pinned source |
| TS4 | energy-flexible training (DR1, AP2, AP9) | MODEL (K5); AP2 and AP9 CONDITIONAL | no R5-R8 ledger row | 6 | DR1 G4-extension: NOT FOUND IN THE SWEEP; G4-tiers, G4 pooled: REDUNDANT; EPS: not new | not decided by a pinned source |
| TS5 | feed pauses (AP10) | MODEL (K6); application CONDITIONAL [model only; contradicted] | no ledger row | 1 | Attention U3, U5: PARTLY REDUNDANT; U4: REDUNDANT | not decided by a pinned source |

**TS4.** TS4 reads CLOSED if K5 is read as CLOSED, as capabilities.txt prints under DR1 DATA ("RESULT DATA: Q fails").

**TS5.**
- **The own-clock ablation.** A-OWN, the own-clock ingredient without the true map, is within a step of plain engagement:
  "reduces: within a step on 4 of 4".
- **Why that does not decide CRR's part.** No line names an ingredient from the list, so CRR's part stays not decided.

### Compute and energy (only lines a pinned output states)

- **SEC (CL1).** CPU share of the full sweep:
  - SEC4-K: "clipped SEC 1 of 17 configurations; CPU share of the full sweep 0.0508–0.0655".
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

The script decides forecast 5 **HOLDS**:

- **(a) A reading that points to known methods and to constructions that hold.**
  - 24 prior-art lines read REDUNDANT or KNOWN, in rows AS1, CL1, RB2, TS1, TS2, TS3, TS4 and TS5.
  - Four rows grade CONSTRUCTION (AS1, AS2, TS1, TS2).
- **(b) No held-out finding.** The ladder's R8 PASS-2 count is 0, and no row grades FINDING.
- **(c) What the applications rest on.** The capabilities that APP1's applications need at CONSTRUCTION or above are K1
  RESULT, K2 CONSTRUCTION and K3 CONSTRUCTION. K2 and K3 are the pause. K1's RESULT rests on one ledger row, SEC4-1.

Printed beside it, and deciding nothing:
- SEC4-1-G reads gate CLOSED. Under SEC6's rule, SEC4-1 "would be printed UNINFORMATIVE and capped at PASS-0", and "SEC4-1
  must not be quoted as evidence that the clipped SEC is tuning-free without this row".
- Under FM6, capabilities.txt reads K1 as CLOSED. The applications would then rest on the pause capabilities alone.

## What CRR contributed (CRR's part, tallied over the 17 rows)

| CRR's part | rows |
|---|---|
| none | 2: CL1, RB1 |
| CRR-proper but not load-bearing | 4: CL2, CL3, CL4, CL5 |
| CRR-proper and load-bearing | no row |
| not decided by a pinned source | 11: AS1, AS2, AS3, AS4, RB2, RB3, TS1, TS2, TS3, TS4, TS5 |

**The one RESULT has none.** The SEC family's mechanism was traced and performs no CRR-proper operation.

**Every CL row with a CRR-proper ingredient is CLOSED.** Each of the four names an ingredient (A3, A6, D6, H-L5, H-EQ), and
every test of it closed or failed.

**The pause rows are not decided.**
- **Why.** The construction holds bit for bit on real stacks, but its sources say they do not test CRR. "Not decided" here
  is a finding about the record: no pinned check isolates what CRR adds to a checkpoint.
- **Their prior art.**
  - The checklist and the own-clock cut read REDUNDANT (Lossless_Pause C4, C5).
  - The zero-stake pause reads PARTLY REDUNDANT (Lossless_Pause C2).

## What would change a row

- **CL1 up to FINDING.** CL1 would rise to FINDING only with a PASS-1 that replicates SEC4-1 on another unseen family. That
  test needs a fresh prereg on a later day and an instrument gate that can close (a learner frozen after task 1 must fail
  its criterion).
- **CL1 down to CLOSED.** If SEC4-1-G or FM6 is read as decisive, CL1 reads CLOSED.
- **CL2-CL5, AS3.** Each needs a new study whose gate opens. AS3 needs a model that can act as an agent (STAKE1-A's gate
  closed on that).
- **AS1, AS2, TS1, TS2.** CRR's part would be decided only by a test that its own source declares a test of CRR. That test
  would be an ablation of the CRR ingredient against standard checkpoint practice on a real stack.
- **TS1, TS2.** The application grades stay CONDITIONAL while a load-bearing dimension is ASSUMED (applications.txt).
- **TS4.** TS4 falls to CLOSED if DR1 DATA is read as decisive.
- **RB2, RB3, TS3.** These could move above a retrodictive grade only through a stage-3 candidate that is not published.
  None is: stage 4a does not run.

## The forecasts, as decided by suite.py

| forecast | decided |
|---|---|
| 1. No row reaches FINDING (PASS-2). | HOLDS |
| 2. Continual learning: the best row is RESULT or below; no traced CL row has a load-bearing CRR-proper ingredient. | HOLDS |
| 3. AI safety and trust: the best rows are CONSTRUCTION; every position graded against the 2025–26 literature is at best PARTLY REDUNDANT. | FAILS |
| 4. Robotics: no row goes beyond a retrodictive grade; stage 4a did not run. | HOLDS |
| 5. The honest headline. | HOLDS |

**Why forecast 3 fails.**
- **What held.** Its first two clauses hold: the best AI-safety and trust rows are CONSTRUCTION, and the pause holds on
  real stacks (Empty_Cut_Engineering C1-C2, RW1).
- **What failed.** Its third clause fails. Of 47 prior-art grades printed in those rows, 3 read NOT FOUND IN THE SWEEP:
  - CORRIGIBILITY_2026 K1, the pause on the agent's own clock, read in AS4 and again through K3 in TS2;
  - DR1 G4-extension in TS4.
- **What that does and does not mean.** The forecast's "at best PARTLY REDUNDANT" is read as "none reads NOT FOUND", and
  these do. "Not found" means the sweep did not find them. It does not mean they are novel.
