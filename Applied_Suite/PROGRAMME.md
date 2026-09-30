# The applied-suite programme (prompt-log entry 257): declared before any of its work

**The request.** Prompt-log entry 257 (2026-09-30T07:11:08Z). The owner asked for seven pieces of work:
1. a full CRR analysis of SEC4, to find precisely why it worked;
2. more tests of SEC4;
3. an exploration of coupling SEC4 with the HopDC finding and the AI-safety cut;
4. a full analysis of what CRR makes possible for continual learning, and of marketable applications with the empty true
   map pause (user experience, energy, data security, privacy, compute);
5. frontier robotics bottlenecks, double-checked before CRR is applied (ARIA, arXiv, news feeds, drones);
6. CRR checks on robotics applications;
7. a full CRR suite of applied use cases (continual learning, AI safety, robotics, trust and security), split across the
   week.

This file is a note, not evidence (R8). It fixes the order of the work, its gates and what each part may claim.

## What "SEC4 was successful" means in the record (fixed now, from the ledger)

**The SEC family's record.**
- **SEC4-1 is the record's only PASS-1.** The clipped SEC was not behind the tuned λ on 6 of 6 carriers of the third
  unseen family (`reports/sec4.md`).
- **It did not replicate.** SEC5-1 FAILs at 4 of 8 on the fourth family (`reports/sec5.md`), so there is no PASS-2 and
  nothing in the SEC family may be quoted outside the ledger as a finding.
- **Its parts are known.** SPA1 finds SEC4's method KNOWN by its declared rule: the clip is AR1's, a path-fitted penalty
  is Synaptic Intelligence's, and tuning-free weights are published. Only the secant units calibration of the Fisher
  itself was not found (`SEC_Prior_Art/SPA1.md`).
- **The pooled count.** Across the four held-out families the calibrated weight is not behind the tuned λ on 23 of 30,
  and raw Laplace on 14 of 30 (`SEC_Prior_Art/checks/compare.txt`).

**Consequence for P1.** "Why SEC4 worked" is only answerable together with "why SEC5 failed". An analysis of the passes
alone would be selection on the outcome. P1 therefore reads all five SEC-family studies: SEC1 on SEEN data, then SCL3,
SEC3, SEC4 and SEC5.

## The parts, in order (each is declared in its own folder before it runs)

| part | what | where | rung it can reach | depends on |
|---|---|---|---|---|
| **P1** | why SEC4 worked and SEC5 did not: analyses A1–A11 over the pinned run records; mechanism checks M1–M4 on the 30 now-SEEN held-out carriers | `SEC_Analysis/` | post hoc on seen records (no ledger row); the M checks are declared checks on SEEN data | — |
| **P2** | SEC6: SEC4's frozen method on a fifth unseen family, with the prior-art baselines SPA1 named and P1's mechanism baselines | `prereg/sec6/`, `studies/sec6/`, `runs/sec6/` | PASS-0/1; a PASS-2 only if SEC6-1 replicates SEC4-1 | P1's M results (the baselines); hash on 2026-09-30, data step on or after 2026-10-01T00:00Z (R3) |
| **P3** | coupling: SEC (the head's penalty), anchor-drift transport of stored class statistics (HopDC's family) and the empty-cut pause (SCL's construction), in one learner | `Coupling/` | R4 (declared, synthetic), then R5 on SEEN carriers if its gate opens | P1; RRM2's finding that the SEC1 learner's features barely drift decides which world can open the gate |
| **P4** | applications: what the record supports for continual learning plus the empty true map pause, graded for user experience, energy, security, privacy and compute | `Applied_Suite/APPLICATIONS.md` | a note: quotes the ledger or nothing (R8) | P1, P2's rows when they exist |
| **P5** | robotics and drone bottlenecks: harvest (ARIA, arXiv, news and industry feeds), double-checked; then the CRR reading, targeted prior art before any code, and CPU gates | `Robotics/` | harvest and grades are notes; gates are R4 | — (runs in parallel with P1–P2) |
| **P6** | robotics application checks: CPU simulations of the P5 candidates that survive prior art, each with a published baseline and a must-fail control | `Robotics/` | R4; a prereg only if a gate opens, with its data step on a later day | P5 |
| **P7** | the applied suite: every use case with its rung, the failures of the same kind beside it, its prior art and its compute | `Applied_Suite/SUITE.md` | a note (R8) | P1–P6 |

## Schedule (UTC)

- **2026-09-30.**
  - P1 declared, run, skeptic-checked and written up.
  - P2: development declaration, baselines built on SEEN carriers, carrier selection from metadata, prereg, hash,
    OpenTimestamps and push, all before the day ends.
  - P5: declaration and harvest, in parallel with P1–P2.
- **2026-10-01.**
  - P2 data step (on or after 00:00Z), scoring, ledger rows and report.
  - P5: CRR reading and targeted prior art.
  - P3: declaration and Phase A.
- **2026-10-02.** P6 gates; P4.
- **2026-10-03 onward.** P7. Any pre-registration whose gate opened, with its data step on a later day than its hash.

## Standing rules this programme adds nothing to and removes nothing from

- **Declarations come first.** Every declaration is pushed before the search, code or run it declares.
- **Hash before data.** Every held-out test is hashed and anchored before any data (R2), with its data step on a later
  day (R3).
- **Every number is printed by a committed script** (R1).
- **Negative results count.**
  - A closed gate stops its line (R12). A fail is a row.
  - "Not found" in a literature sweep is never "novel".
- **What is quotable.**
  - Applications are stated at the rung the record reaches, never above it.
  - Nothing is quotable outside the ledger except a PASS-2.
- **Money.** The owner cannot spend money on these tests at this stage: every run is CPU-only on this container, and every
  source is free to read.
