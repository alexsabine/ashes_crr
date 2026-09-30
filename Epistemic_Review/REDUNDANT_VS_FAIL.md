# Redundant, consistent and descriptive against fails, and whether PRED70's fails are redundant

**Status.**
- **The request.** Owner request, prompt-log entry 235 (2026-09-29).
- **Where the numbers come from.** Every number is printed by `checks/redundant_vs_fail.py` (output `checks/redundant_vs_fail.txt`,
  CI-checked). The script reads only pinned outputs: the ladder and PRED70's tally.
- **What it is.** A note, not evidence (R8). The class readings in part 2 are the investigator's, applying one written
  rule. No label in any pinned output is changed.

## 1. The counts

| layer | consistent / descriptive / redundant | fail | ratio |
|---|---|---|---|
| retrodiction batteries (197 rows) | CONSIST 41 + DESCR 86 = 127 | FAILS 20 | 6.35 to 1 |
| synthesis re-read (164 real-domain rows) | REDUNDANT-IG 39 + REDUNDANT-DOMAIN 59 = 98 | WRONG 28 | 3.50 to 1 |
| PRED70 (70 declared predictions) | REDUNDANT-IG 19 + REDUNDANT-DOMAIN 16 = 35 | WRONG 18 | 1.94 to 1 |
| held-out ledger (pre-registered, unseen data) | PASS-0 12, PASS-1 1 (no redundant grade) | FAIL 34 (after SEC5; `checks/redundant_vs_fail.txt` re-pinned 2026-09-30) | — |

**The pattern.** The more a test demands of CRR, the smaller the ratio. Loose retrodiction gives 6.35 to 1. The synthesis
re-read, which asks whether the CRR ingredient did any work, gives 3.50. Declared prediction gives 1.94. On
pre-registered held-out data, fails outnumber passes.

**The re-read moved the batteries' positive grades.**
- The 41 CONSIST rows became: 29 redundant, 3 WRONG, 9 INTERNAL, 0 ADDS.
- The 86 DESCR rows became: 55 redundant, 14 WRONG, 12 INTERNAL, 2 ADDS.

## 2. Should PRED70's 18 fails be classed as redundant?

**No, not one.** Two reasons, both from the repository's own rules.

1. **The label rule.**
   - A row is REDUNDANT only if the CRR value agrees with the null or with the domain's own result within 1 %.
   - A row reaches WRONG only after both of those tests read "differ" (`src/crr/synthesis/harness.py`).
   - So a WRONG row is, by construction, one where CRR's ingredient changed the answer and the changed answer was wrong.
     It qualifies for REDUNDANT on 0 of 18.
   - Relabelling it would mean changing a tolerance after the result (R15), which CLAUDE.md §10 forbids: "A fail is a
     fail; the reinterpretation is a new prereg."
2. **They mean different things.**
   - A redundant row says: CRR agrees with something already known. It was consistent but took no risk, so it cannot
     falsify.
   - A fail says: CRR's ingredient made a different claim and the claim was false.
   - For a formalism meant to be falsifiable, calling its fails "redundant" would erase exactly the information the
     programme exists to collect.

**What the fails do and do not falsify.** `theory/CRR.md` §9 is precise here: only H-CUT, H-L5, H-T1 and H-EQ can fail.
"Everything else in this document is definition, standard mathematics, or open." Applied to the 18 fails:

| class | rows | reading |
|---|---|---|
| FALSIFIES | 6: P02-1, P08-4, P11-2, P11-3, P12-4, P13-2 | a §9 claim, applied inside its scope, failed: H-L5 on four carriers with their own events; H-CUT on sleep onset and a thermostat |
| SCOPE | 2: P05-1, P12-2 | CRR itself says the claim must fail or does not apply: H-T1 on a convex learner (its declared must-fail); a cut on a carrier with no rotor (O3) |
| APPLICATION | 6: P03-5, P05-3, P06-5, P07-4, P10-2, P10-4 | an axiom (A3 as a timing or control rule, A6 as a dynamical model) applied as a domain model; the consequence failed. It bounds CRR's reach but cannot falsify it under §9 |
| KNOB | 4: P05-5, P11-1, P11-4, P14-1 | the failure rests on a value CRR does not fix (A6's weight q; the occasion length), declared at one value by the investigator |

**Two things this reading does not do.**
- **It does not rescue the ten APPLICATION and KNOB fails.** They are real failures of the declared predictions. What
  they show is that CRR's axioms, used as models, often do not describe these systems.
- **It does not make them redundant.** They show that CRR's non-falsifiable parts have limited reach.

## 3. The reverse direction: passes that are fails

§9 says H-L5 fails "if CV_C ≥ CV_Δt, or a control matches it".
- **PRED70 H-L5 rows:** of the 16, 15 are §9 FAILs, 0 PASS, and 1 is undetermined (P06-3, where the amplitude control
  was not printed).
- **The harness ADDS rows among them:** 7 (P01-1, P01-2, P01-3, P01-5, P02-3, P07-5, P11-5) are §9 FAILs, because the
  amplitude control matches or beats the arc.
- **Whose error.** The declared Q omitted the control, which was the investigator's error (AGENT_LOG 175).

## 4. PRED70 read under §9 (a reading; the pinned labels stand)

- **Count against a falsifiable CRR claim: 13** (6 FALSIFIES + 7 H-L5 ADDS rows failing their control).
- **Bound CRR's reach without falsifying it: 10** (APPLICATION + KNOB).
- **Predicted by CRR itself: 2** (SCOPE).
- **Redundant: 35** (consistent but not risky).
- **Surviving candidates: 7** (A6 ADDS), pending a literature check.

**In short.** Read strictly as a falsifiable formalism, CRR's specific, risky claims fail more often than they pass.
- H-L5 failed on 15 of 16 of these systems.
- H-CUT failed wherever it could be told apart from the domain's trigger.

Where CRR agrees, it mostly restates what the domain already has. Its only surviving new content in PRED70 is the
remembered-state ingredient, and that is still unchecked against the literature.
