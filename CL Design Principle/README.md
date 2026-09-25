# CL Design Principle: a CRR safe continual learner built from what works in state-of-the-art methods

**Status.** Owner request: prompt-log entry 191. It is a note, not evidence (R8). Every number comes from a pinned output
named beside it. Findings are logged as they arrive in [FINDINGS.md](FINDINGS.md), which is append-only.

## The method (a design-principle investigation)

1. **Read the state of the art on the day (R10).** For each leading continual-learning method, record its mathematics and
   its published ablations, quoted verbatim with version and date (`docs/citations/cl_sota_*_2026-09-25.md`).
2. **Declare before grading.** Each method's mechanism is written in CRR's terms, and CRR's prediction for its ablation is
   stated: does removing the mechanism hurt, or not? The declaration is `DECLARATION_1.md`, pushed before any ablation
   reading is opened.
3. **Grade retrodictively.** A script sets each prediction against the published ablation and computes AGREES,
   DISAGREES or SILENT (R15). Every DISAGREES is examined for *why*.
4. **Design.** The CRR safe continual learner integrates:
   - the mechanisms that agree;
   - the mechanisms that disagree but work, where the reason they work can be stated in CRR's terms or honestly cannot;
   - the empty cut (Proposition 7), valued on the learner's own steps.

   The design is in `DESIGN.md`.
5. **Phase A (R4).** A declared synthetic gate, plus a synthetic comparative and ablation battery (`DECLARATION_2.md`,
   `checks/`). If the gate closes, stop (R12).
6. **Pre-register SOTA1** (`prereg/sota1/`), with the design frozen, hashed, OpenTimestamps-anchored and tagged.
7. **Data step, then the full comparative and ablation run** on online Split-CIFAR-100 (UNSEEN). Mammoth's reference
   baselines are pinned at commit e75a491. Then the ledger rows and `reports/sota1.md`.

## Schedule

The owner asked for everything by 10:00 PCT on 25 September. That is read as Pacific time (PDT, UTC−7), so 17:00 UTC on
2026-09-25.

**R3 does not allow the data step that day.** R3 forbids using a rule on a dataset on the same calendar day it was
defined. This learner is defined today (2026-09-25 UTC), and datasets were also opened today (SCL3 at 00:07Z, RLAW at
00:40Z). So its first contact with CIFAR-100 can come no earlier than 2026-09-26 00:00 UTC, which is 17:00 PDT on the 25th.
CLAUDE.md's rules override a task prompt's schedule, so the plan is:

| by | what |
|---|---|
| 2026-09-25, 17:00 UTC (10:00 PDT) | steps 1–6 done and pushed: sources, declaration, retrodictive grading, design, Phase A gate and synthetic battery, prereg hashed and anchored |
| 2026-09-26, from 00:00 UTC | step 7 begins: the data step, then all arms run on CPU in resumable chunks |
| when the runs finish (the budget is printed before the hash) | ledger rows, report, findings |
