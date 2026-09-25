# Energy Design Principle: CRR as a lens on what saves energy in AI training and execution

**Status.** Owner request: prompt-log entry 199. It is a note, not evidence (R8). Every number comes from a pinned output
named beside it. Findings are logged as they arrive in [FINDINGS.md](FINDINGS.md), which is append-only.

## The method (the same as `CL Design Principle/`)

1. **Declare before reading.** `DECLARATION_1.md` gives CRR's reading of each energy-saving mechanism and the direction it
   implies. It was pushed before the sources were fetched.
2. **Read the literature on the day (R10).** Three dossiers:
   - how AI energy is measured and where it goes;
   - training and development efficiency;
   - execution (inference and serving) efficiency.

   They are `docs/citations/energy_{accounting,training,inference}_2026-09-25.md`, with quotes verbatim, versions and
   dates.
3. **Grade retrodictively.** `checks/energy_rows.py` holds the quoted rows, and `checks/retro_energy.py` computes AGREES,
   DISAGREES or SILENT (R15). Every DISAGREES is examined for *why*.
4. **Design the energy tests (ENERGY1)** from what agrees and what works. This happens after the continual-learning and
   AI-safety pipeline (SOTA1) has run, so the energy tests can use its learner, its baselines and its measured costs.
5. **Phase A (R4), then the pre-registration.** A declared synthetic gate first, then `prereg/energy1/` hashed,
   OpenTimestamps-anchored and pushed. The data step comes on a later UTC day than any rule defined (R3).
6. **The prospectus.** One document comparing CRR's methods with the state of the art on continual learning, AI safety and
   energy. It quotes the ledger or nothing (R8).

## Schedule (UTC)

| when | what |
|---|---|
| 2026-09-25 | steps 1–3: declaration, dossiers, retrodictive grading, findings |
| 2026-09-26 from 00:05 | SOTA1 data step and full run (about 20 hours of CPU) |
| when SOTA1 finishes | SOTA1 ledger rows and report; then step 4, ENERGY1 design, and step 5, Phase A gate and pre-registration |
| the next UTC day after the ENERGY1 hash | the ENERGY1 data step and run |
| after ENERGY1's rows | step 6, the prospectus |

## The measurement limit

- **This container has no energy counter** (no RAPL, no GPU). The energy tests measure counted work: passes,
  multiply-accumulates, and wall time at fixed threads.
- **Joules come only from a named power assumption.** Any figure in joules says so beside it.
- **No money is spent.** Per the owner's instruction, there is no paid GPU or API.
