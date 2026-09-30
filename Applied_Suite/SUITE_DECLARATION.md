# Declaration: the CRR applied use-case suite (P7 of `Applied_Suite/PROGRAMME.md`; pushed before it is assembled)

**The request.** Prompt-log entry 257: "The goal is to produce a full crr suite of applied use cases in the context of
continuous learning, AI safety, robotics and trust/security."

**Status.** A note, not evidence (R8). The suite collects results; it adds none. Every row is computed by
`Applied_Suite/checks/suite.py` from pinned outputs and ledger rows. The prose (`Applied_Suite/SUITE.md`) quotes only
that table and the files it names.

## The rows (fixed now)

There is one row per use case, in four domains.

| domain | use cases (the source of each row's grade) |
|---|---|
| **Continual learning** | tuning-free penalty strength (SEC family: SCL3-3, SEC3-3, SEC4-1, SEC5-1, SEC6-*, SEC7-* when scored; P1's `SEC_Analysis`); exemplar-free memory (RQM-A, RRM-PA, RRM2-T*, CPL1-A); consolidation timing (OB1-C3-A); optimiser clocks (OB1-C1-A); the equanimity rule Ω = 1 (EQ\*, SOTA1-2) |
| **AI safety** | the empty-cut pause as a construction (SCL1-1, SCL3-C, `Empty_Cut_Engineering/`, `Real_World/RW1.md`, CPL1's C1); no incentive to resist a pause (SCL1-2/3, SCL2, `AI_Safety/NT1/`); LLM agents' interference (STAKE1-A); corrigibility positions (`AI_Safety/CORRIGIBILITY_2026/`) |
| **Robotics** | ROB1's bottlenecks (`Robotics/checks/table.txt`), the CRR reading and stage 3 (`reading_tally.txt`, `grade_s3.txt`), and the application battery (`tally_4b.txt`) |
| **Trust and security** | exact rollback and audit (APP1 AP8); a user's "stop learning from me" switch (AP3); the lost-link and e-stop pause (RA4, C-R1); energy-flexible training (DR1, AP2, AP9); feed pauses (`Attention_Algorithms/`, AP10) |

**The fields of each row:**
- the capability grade (APP1's scale: FINDING, RESULT, CONSTRUCTION, MODEL, CLOSED), or the ledger verdict;
- the rung (`Epistemic_Review/checks/ladder.py`);
- the failures of the same kind, printed beside it;
- the prior-art verdict where one exists (SPA1, OB1, ROB1 stage 3, APP1's M sweeps, `Lossless_Pause/`);
- CRR's part: CRR-proper and load-bearing, CRR-proper but not load-bearing, or none;
- the compute or energy figure, only if a pinned output states it.

## Forecasts (written now, before SEC6's and SEC7's data steps)

1. **No row reaches FINDING** (PASS-2).
2. **Continual learning.** The best row is RESULT or below. Every CL row whose mechanism was traced has no load-bearing
   CRR-proper ingredient (P1's F11; ROB1 stage 3; OB1).
3. **AI safety and trust.** The best rows are CONSTRUCTION: the pause holds bit for bit on real stacks. Every position
   graded against the 2025–26 literature is at best PARTLY REDUNDANT.
4. **Robotics.** No row goes beyond a retrodictive grade. Stage 4a did not run.
5. **The suite's honest headline:**
   - CRR has been useful as a **reading** that points to known methods and to constructions that hold;
   - it has not produced a held-out finding;
   - its applications rest on the pause construction and on one unreplicated continual-learning result.

## Order

1. SEC6 (data step 2026-10-01) and SEC7 (if its gate opens) are scored.
2. `suite.py` is written and pinned, with a CI check.
3. `SUITE.md` is written from it.
4. An independent verifier checks it number by number.
5. It is merged.
