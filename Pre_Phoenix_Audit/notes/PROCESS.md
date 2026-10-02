# PROCESS — the research process and the counting (Pre-Phoenix audit, process reader)

PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED. An interpretive note, not evidence (R8). Scope: the process
across all lineages (prompt-log entry 260, question 10, and the denominator table for section 5 of the request).
Nothing in the ledger, reports, preregs, runs, notebook or any pinned output was edited.

## 0. Sources, conventions and what was counted

- **Script.** `Pre_Phoenix_Audit/checks/outcome_classes.py`, output `Pre_Phoenix_Audit/checks/outcome_classes.txt`
  (run twice, `cmp` byte-identical). It imports `Epistemic_Review/checks/ladder.py` unchanged for its parser and its
  data-status rule, and prints the ledger and ladder sha256 (OC:3-4). Citations `OC:n` are lines of that output.
- **Other citations.**
  - `AL n` is entry n of `notebook/AGENT_LOG.md`. Entry n sits on line n+12 for n ≤ 20, n+13 for 21 ≤ n ≤ 233 (233 is
    used twice, lines 246-247), and n+14 for n ≥ 234.
  - `PL n (:L)` is prompt-log entry n at line L of `notebook/PROMPT_LOG.md`.
  - `LT:n` is a line of `Epistemic_Review/checks/ladder.txt`; `RVF:n` is a line of
    `Epistemic_Review/checks/redundant_vs_fail.txt`.
  - Ledger rows are cited by id, from `ledger/LEDGER.md`.
- **Reading done.**
  - AGENT_LOG: entries 1-248, in full.
  - PROMPT_LOG: every entry header, plus the full text of each entry cited here.
  - The ledger: every row's verdict, plus the hash/anchor cell of each study's first row.
  - `git log`: commit times of the prereg, data-step and scoring commits named in OC [8].
- **Derived counts.** Any count not printed by the script, or by a pinned output, is marked **auditor's count
  (derived)**, and the method is stated with it.

## 1. Trajectory of the process (dated, cited)

**Phase 1 (2026-09-15).** The audit protocol landed, and three held-out tests followed within hours. EQX was hashed
14.8 min after PL 3 (:53). MEAS took 10.5 min from PL 7 (:100) and was VOID through its loader. MEAS2 was re-hashed
with a corrected loader. CARD was hashed 6.9 min after PL 9 (:121), but its data were unreachable until 2026-09-26
(OC:427-430; AL 164). The owner asked for the nulls to be deleted. The agent refused under R8/R12 (PL 11 :142-157;
AL 2).

**Phase 2 (2026-09-15/17): EQ2.** The design ran through owner prompts PL 17-31. A playground outside the repository
(AL 3) showed the rule helping EWC-type penalties and harming distillation constraints; its numbers were kept off the
record. A first gate with a convex positive control closed: "a fixed
weight is metric-optimal on a quadratic" (AL 4). A second positive control opened, and EQ2 was hashed (OC:431). It is
the only study with a long design phase before its hash: 1492.8 min from PL 17 (OC:431).

**Phase 3 (2026-09-17/21): breadth.** On the owner's and Daniel's direction (PL 38 :561), the agent built the
retrodictive programme. It kept "confirmatory" for seen data (AL 14). The prompts asked for battery after battery
(PL 39-61). The held-out replication EQ2R was hashed the same day as EQ2's data and held for R3 (AL 25). It went VOID
on 2026-09-21 through an untested branch of its frozen scorer (AL 40).

**Phase 4 (2026-09-22/23): the continual-learning tests, fast.** One test followed another:

- EQ3, 22.0 min from request to hash;
- EQ4, 39.5 min, with the rule EQ-B defined that morning;
- BAYES-1, 12.5 min;
- T1x, 6.2 min, VOID;
- T1x2, hashed 17 min after T1x's data (OC:434-438).

Then came Adam/SGD exploration on synthetic data (AL 90-94). SEC was defined on synthetic worlds and run the same day
on SEEN carriers as SEC1 (AL 96; OC:439). The safety harness followed: SCL1 on seen data, SCL2 on unseen (OC:440-441).

**Phase 5 (2026-09-24/27): first strong anchors.** OpenTimestamps became reachable (AL 107, 111). SCL3 gave the first
strongly anchored PASS-0 rows (AL 128). RLAW and SOTA1 failed (OC:443-444). CARD finally ran and failed (AL 165). Many
declared synthetic batteries and literature sweeps ran beside them (AL 113-166).

**Phase 6 (2026-09-27/10-02): the SEC chain.** The studies ran SEC3 → SEC4 (PASS-1) → SEC5 (FAIL) → SEC6 (NOT
DECIDABLE, loader) → SEC6R (gate CLOSED, UNINFORMATIVE). Each was hashed 0.45 to 9.07 h after the previous scoring
commit (OC:445-449). Interleaved with them were the Phase-A programmes RQM, RRM/RRM2, OB1, CPL1 and SEC7, each of which
closed its gate (AL 189-238). A post hoc mechanism analysis (P1) then found that the SEC family's criterion is met by a
learner frozen after task 1 (AL 222). That finding was applied to the record's only PASS-1 (AL 236; ledger SEC4-1-G).

## 2. The denominator table (ledger rows only)

### 2.1 Totals

- The ledger has 235 rows. `ladder.py` allocates 225 of them and skips the 10 RLAW rows at the owner's instruction
  (OC:48; PL 139; AL 114).
- Mechanical outcome class (first matching rule on the verdict text; the rules are printed at OC:6-46) against data
  status (OC:286-307):

| class | held-out | seen | synthetic | RLAW (outside ladder) | all |
|---|---|---|---|---|---|
| VOID | 4 | 1 | 0 | 0 | 5 |
| GATE CLOSED (before data) | 0 | 9 | 2 | 0 | 11 |
| UNINFORMATIVE | 6 | 8 | 0 | 0 | 14 |
| NOT DECIDABLE | 11 | 2 | 0 | 0 | 13 |
| PASS-1 | 1 | 0 | 0 | 0 | 1 |
| PASS-0 | 12 | 0 | 0 | 0 | 12 |
| FRAGILE | 7 | 3 | 0 | 1 | 11 |
| REDUCES / control violated / INERT (+IDLE) | 7 | 0 | 0 | 0 | 7 |
| construction | 6 | 2 | 0 | 0 | 8 |
| PASS-other | 5 | 9 | 0 | 0 | 14 |
| report / no verdict | 49 | 11 | 0 | 1 | 61 |
| FAIL | 36 | 5 | 0 | 8 | 49 |
| other (holds 7, not fragile 9, does not reduce 3, DECIDABLE 6, UNVERIFIABLE 1, numbers 3) | 22 | 7 | 0 | 0 | 29 |
| total | 166 | 57 | 2 | 10 | 235 |

### 2.2 Where this table and `ladder.py` disagree (OC:394-395, printed, not reconciled)

- `ladder.py` counts 15 PASS-0 rows; this script counts 12. The difference is SEC6R-1, SEC6R-C and SEC6R-P. Their
  verdicts read "PASS-0 (UNINFORMATIVE: ...)" (ledger), and the UNINFORMATIVE rule matches first here.
- `ladder.py` counts 37 held-out FAIL rows; this script counts 36. SEC6R-B reads "FAIL (UNINFORMATIVE: SEC6R-G CLOSED
  ...)".
- Both facts stand. The ledger registers those rows as PASS-0 and FAIL (AL 245 (1)). The gate row beside them says they
  cannot discriminate.

### 2.3 Held-out rows, summarised (OC:396)

- There are 166 held-out rows:
  - PASS-1 or PASS-0: 13;
  - FAIL: 36;
  - VOID + NOT DECIDABLE + UNINFORMATIVE: 21.
- The held-out FAIL rows by study prefix are auditor's sums (derived) from OC:403-424. The H-EQ family accounts for 10:

| study | held-out FAIL rows | what the rows test |
|---|---|---|
| EQX | 2 | H-EQ (`theory/CRR.md:313`) |
| EQ2 | 1 | H-EQ |
| EQ3 | 4 | H-EQ |
| EQ4 | 3 | H-EQ (bounded rule EQ-B) |
| MEAS2 | 2 | H-L5 (`theory/CRR.md:311`) |
| CARD | 2 | H-L5 |
| T1X2 | 2 | H-T1 (`theory/CRR.md:312`) |
| SCL2 | 2 | an unpredicted observation from SCL1 (AL 104 (b)) |
| SOTA1 | 9 | the CRR safe continual learner and its components |
| SEC3 | 4 | SEC, which the ledger labels "not a CRR rule" (SEC4-1's verdict) |
| SEC5 | 3 | SEC |
| SEC6R | 2 | SEC |

### 2.4 The INSTR flag and what it misses

- **What the flag found.** The INSTR flag (the brief's word list, OC:30-39) is set on 16 rows (OC:373), all of them
  VOID, NOT DECIDABLE, GATE CLOSED or one UNINFORMATIVE row (OC:374-379).
- **Its blind spot.** It is set on **0 held-out FAIL rows** (OC:397). That understates infrastructure involvement in
  the FAILs, because the words are not in those verdicts:
  - EQ3-1. The verdict says fars's "class 0 is empty after the pre-registered subsample and [its] EWC family is at
    chance". The AGENT_LOG later calls this "a pipeline sampling defect" (AL 81 (a); AL 60).
  - SEC5-2. Its verdict reads "on pokerhand not a stability-edge crossing" (AL 188 (2)).
  - SEC3-3 and SEC5-1. Both are FAIL as scored, but the post hoc gate rows SEC3-3-G and SEC5-1-G say they "would be
    printed UNINFORMATIVE". The criterion could not discriminate on those carriers (AL 236).
- **Mechanical classes are not salvage categories.** Section 5 maps one to the other only as a starting point.

### 2.5 The 23 hashed pre-registrations at study level

- **Source.** Auditor's reading (derived) of each study's primary row. Count method: the `prereg/*/HASH.txt` files
  (23; SAL and SEC7 have none).
- **Outcomes:**
  - **VOID, 4 studies:** MEAS, EQ2R, EQ2R-CC, T1x (ledger MEAS-1..3, EQ2R-VOID, CC-VOID, T1X-VOID).
  - **NOT DECIDABLE on the primary, 2:** BAYES-1 (BAYES1-B0) and SEC6 (SEC6-1).
  - **FAIL or REDUCES on the primary, 11:** EQX (EQX-1 REDUCES, EQX-3), MEAS2, CARD, EQ3 (EQ3-1), EQ4 (EQ4-1), T1x2,
    SCL2 (SCL2-R and SCL2-M FAIL; SCL2-2, SCL2-2s and SCL2-3 are "PASS as scored ... not counted as
    PASS-0"), RLAW, SOTA1, SEC3, SEC5.
  - **PASS on seen data, rung R5, 2:** SEC1 and SCL1.
  - **Held-out PASS-0 or PASS-1, 4:**
    - EQ2: EQ2-1 "PASS, FRAGILE", then EQ2-1b PASS-0, then EQ2-1c "failed replication recorded".
    - SCL3: four PASS-0 rows. FRAGILE (SCL3-S). Gate OPEN post hoc (SCL3-3-G).
    - SEC4: PASS-1, with SEC4-1-G "would be printed UNINFORMATIVE and capped at PASS-0".
    - SEC6R: PASS-0 "UNINFORMATIVE".

### 2.6 Retrodictive banks: separate denominators, quoted only

These never enter the table above.

- **Retrodiction batteries.** 197 rows: SHARP 0, CONSIST 41, DESCR 86, FAILS 20, TENSION 9, OPEN 41 (LT:15). FLOW is
  supplied by the framework in "0 of 109 rows that print FLOW" (LT:20).
- **Synthesis re-reads.** 164 real-domain rows: ADDS 10, PROPOSES 2, REDUNDANT-IG 39, REDUNDANT-DOMAIN 59, WRONG 28,
  INTERNAL 22, UNSTATED 4 (LT:28).
  - Retrodictive hit rate: "69 of 97 = 0.7113". Novelty rate: "10 of 97 = 0.1031" (LT:41-42).
  - After the literature check: "3 of 10 ADDS rows are REDUNDANT-DOMAIN by the literature, 6 keep R3 with the direction
    known, 0 keep R3 as clean candidates, 1 removed" (LT:68).
- **Ratios layer by layer.**
  - Consistent/descriptive to fail: 127:20 (RVF:4).
  - Redundant to fail: 98:28 (RVF:5).
  - PRED70: 35:18 (RVF:8).
  - The held-out ledger: "PASS-0 15, PASS-1 1, FAIL 37" (RVF:9).
- **PRED70 under CRR.md section 9.** 13 fails count against a falsifiable CRR claim. 10 fails bound reach. 7 A6 ADDS
  candidates survive (RVF:43-45).
- **Why the banks stay apart.** The ratios fall from the batteries to PRED70 to the held-out ledger (RVF:4-9). That is
  a different denominator at each layer. No single "rate" across them is meaningful (RVF:10 says the combination
  "double-counts by design").

## 3. Process audit, items (a) to (g)

### 3(a) Gates closed before confirmatory data, and why

Every closure below happened before any held-out data were opened for that hypothesis. The reason column is the
auditor's classification (judgement); the quoted reasons let a reader reclassify.

| # | gate | AL | quoted reason (abridged from the entry or ledger row) | auditor's reason class | what happened next |
|---|---|---|---|---|---|
| 1 | EQ2 attempt 1 | 4 | convex positive control "cannot open (a fixed weight is metric-optimal on a quadratic)" | positive control could not win | redesigned (S-Y), OPEN; EQ2 ran |
| 2 | SAL-A | 12-13 | "the law's own value λ = 1 loses on the surrogate built in its favour"; ledger "no positive control exists for this operationalisation" | no positive control | stopped (R4, R12); "trying other operationalisations until one opened" rejected |
| 3 | FED v1, v2 | 71 | v1 "two design defects"; v2 "the global knob is never a step behind"; "knob+clip holds as well as EQ-B" | v1 design defect; v2 the rule has nothing to win | no prereg (R4, R12) |
| 4 | SEC1 gate v1 | 96 | "its units-distortion rows were not load-bearing" | positive control not load-bearing | redesigned before any carrier, OPEN; SEC1 ran |
| 5 | Rupture detector | 88 | "the positive control PC1 (speed-jittered sine) is BEHIND" | positive control could not win | stopped; "re-running with a causal phase, a Poincaré section ..." rejected |
| 6 | Adam drift battery, Declaration 2 | 92 | "two instrument defects, not a verdict on the rule: (a) no headroom ... (b) grid edges" | no headroom | post hoc Declaration 3 "GATE OPEN, narrowly" (AL 93); mechanism check (AL 94) |
| 7 | Maps P5 | 117-118 | "one declared G+ condition was wrong"; post hoc Declaration 2 also CLOSED | declared condition wrong | "no third round, which would be fishing" |
| 8 | CUT1 | 122 | A3 "cannot separate a plasticity effect from a dose effect"; the convex premise "holds at convergence, and 3 epochs ... is short of it" | design defect (dose confound; must-fail premise unmet) | no real-data CUT1 (R12); redesign "only on the owner's instruction" |
| 9 | RW2 Phase A, two rounds | 125-126 | round 1 "no headroom ... the stream never moved the model"; round 2 "H0 FAILS" | no headroom | only the construction may be registered |
| 10 | Lossless pause, run 1 | 147 | "the declared control L5b ... left every logit byte identical" | control invisible at the declared level | post hoc Amendment 1, run 2 OPEN |
| 11 | FOREVER comparative clock gate | 134 | "positive control failed: C1 -0.71 TIE in W2" | positive control could not win | "ARC-R is not licensed" |
| 12 | STAKE1-A | 160 | "the models could not act as agents" (ledger) | precondition unmet (the model) | stopped (R12); a capable model (RW3) needs money (AL 158) |
| 13 | Life Sciences G-DS2 | 162 | "the better arc detector not ahead of even that stand-in by a step" | hypothesis behind the domain stand-in | G-CD3 OPEN, but LIFE1 was not registered (loader risk, R2/R3) |
| 14 | SEC3 guard gate | 167 | "G-RESCUE FAILS ... GUARD GATE CLOSED" | behind the comparator | guarded arm report-only; a guard re-developed in SEC4 (AL 169) |
| 15 | SEC5 D-GATE-C | 178 | A6-MEAN-CLIP "-0.2021 below the clip, so D-ADDS fails" | adds nothing over the existing arm | no A6 arm on unseen data (R12) |
| 16 | EPS2 T3 | 184 | "G-NEG fails ... the advantage is partly built in" | negative control failed | not counted |
| 17 | RQM-A, two runs | 191-192 | run 1 "a defective control"; run 2 "the declared criterion cannot fail where the memory is wrong" | criterion cannot fail | stopped (R12); "a third negative stream tuned until IGR loses" rejected |
| 18 | RRM-PA | 195 | "GATE CLOSED on 1 of 8 conditions: RRM-A under ROT"; "RRM-1 ... held every condition" | one of two declared forms failed | RRM2 (AL 197-199) |
| 19 | RRM2 Part W | 198 | "NOT WORTH PURSUING (P5 REDUNDANT)" via HopDC | prior art | T6 (unseen data) off |
| 20 | RRM2-T1..T3 | 199 | "the learner's features barely drift"; "the forgetting lives in the head" | mechanism has no work to do in this learner | stopped |
| 21 | OB1-C1-A | 205 | "on S2 the gain is the distribution of the decays, not their timing"; "S1's metric measures forgetting onset ... a declared-design defect" (ledger) | timing not load-bearing; plus a design defect | stopped (R12); corrected S1 not run |
| 22 | OB1-C3-A | 209 | "consolidation has no effect in the declared stream ... a design failure of the declaration" (ledger) | design failure (the compared thing has no effect) | stopped (R12); amended stream not run |
| 23 | CPL1-A | 229-230 | "transport with current-task anchors makes the stored means worse in this learner" (ledger) | mechanism harmful in this learner | stopped (R12) |
| 24 | ROB1 stage 3 | 231 | C-R1, C-R2, C-R3 "REDUNDANT" | prior art | stage 4a not run (R12) |
| 25 | SEC7-A | 238 | "'not behind the tuned lambda' cannot fail ... a design failure of the benchmark, not a test of SEC" (ledger) | criterion cannot fail | stopped (R12) |

The ledger's own GATE CLOSED rows are SAL-A, STAKE1-A, RQM-A, RRM-PA, RRM2-T1..T3, OB1-C1-A, OB1-C3-A, CPL1-A and SEC7-A
(OC:313-315). Items 1, 3-11 and 13-16 are recorded only in the AGENT_LOG and the notes folders, not in the ledger.

**Reason classes (auditor's count, derived by hand from the table, judgement-dependent).** These tally the 25 gates by
the reason class assigned in the table. Two gates (FED, OB1-C1) carry two reasons each, so the classes overlap.

- Positive control absent, unable to win or invisible: 6 (rows 1, 2, 4, 5, 10, 11).
- No headroom, or the agent unable to act: 3 (rows 6, 9, 12).
- Criterion cannot fail: 2 (rows 17, 25).
- Design defect of the declared world or condition: 5 (rows 3 v1, 7, 8, 21, 22).
- The hypothesis or mechanism did no work, or was behind its comparator, on a gate that could have opened: 8 (rows 3
  v2, 13, 14, 15, 16, 18, 20, 23).
- Prior art: 2 (rows 19, 24).

**Redesigns after a first closure (auditor's count, derived from the entries cited):**

- **5 opened:** EQ2 (AL 4), SEC1 (AL 96), Adam Declaration 3 (AL 93, post hoc, "narrowly"), Lossless run 2 (AL 147,
  post hoc), and the SEC3 guard re-developed as SEC4's clip (AL 169, D-GATE OPEN).
- **5 closed again:** FED v2 (AL 71), RW2 round 2 (AL 126), Maps Declaration 2 (AL 118), RQM run 2 (AL 192), and
  RRM → RRM2-T2 (AL 199).
- **Where the opened ones led.** Three of them lead to the record's held-out passes:
  - EQ2 led to EQ2-1b PASS-0;
  - SEC1 led to SCL3's PASS-0 rows, through SEC;
  - the re-developed guard led to SEC4-1 PASS-1.

### 3(b) Time from declaration to hash, and development before the hash

**Timing (OC:425-453).** Commit times are authoritative. From entry 57 on, prompt header times are logging times
(prompt-log correction note after entry 56), so "prompt→hash" is a lower bound on receipt→hash. It also excludes
design work done before the request.

**Auditor's count (derived from OC:427-449):**

- Of the 20 studies with a named request prompt, 15 were hashed within 25 min of that prompt's header time: EQX, MEAS,
  MEAS2, CARD, EQ3, BAYES-1, T1x, SEC1, SCL1, SCL2, SCL3, SEC3, SEC4, SEC5, SEC6R.
- The other five took longer:
  - EQ2: 1492.8 min;
  - EQ4: 39.5 min;
  - RLAW: 84.1 min;
  - SOTA1: 383.5 min;
  - SEC6: 160.8 min.

**Where the design came from.** The short gaps do not mean the design was invented in those minutes:

- The L5x, T1x and EQ designs were templated in `CLAUDE.md` §4-§6 (CLAUDE.md:535, 574, 611).
- SEC3 is plan item CL-1 of the 2026-09-26 next-steps plan (AL 161, 167).
- SEC4-SEC6 had development declarations: AL 169, 177-178, 214-224.

**What each study had before its hash** (from the AGENT_LOG; "SEEN" means development on seen carriers):

| study | development or exploration before the hash | AL |
|---|---|---|
| EQX | none logged (the AGENT_LOG starts 2026-09-17; the design came from the archived seen bundle, ledger ARC-*) | 1 (r) |
| MEAS / MEAS2 | none; MEAS2 was re-hashed 2.9 min after MEAS with the loader corrected (OC:428-429) | — |
| CARD | none | 164 |
| EQ2 | an owner-permitted playground on synthetic data (numbers kept off the record); two gate attempts | 3, 4 |
| SAL | one operationalisation change (shadow-pass surplus), then the gate | 12, 13 |
| EQ2R | none; the smoke mode was "not run on the EQ2R copy before the hash" | 40 |
| EQ3 | `omega_sweeps` on existing mathematics; two smoke modes | 58, 59 |
| EQ4 | EQ-B v1 (median) behind on the gate; v2 (largest kept length), κ chosen on synthetic rows and confirmed on six SEEN carriers | 63 |
| BAYES-1 | four defects fixed on the surrogate; B2/B3 registered with the surrogate's predicted FAIL | 66 |
| T1x | one synthetic smoke; schedules added for the precondition | 68 |
| T1x2 | the T1x VOID's corrections; smoke extended to binary and extreme-drift carriers | 69, 70 |
| SEC1 | gate v1 CLOSED and redesigned; a one-factor arm added | 96 |
| SCL1 | a declared mathematics run; M4, M5, M7 failed; consequences applied; KAPPA and R set after smoke | 102 |
| SCL2 | gate on synthetic data; positive-control dose P 0.05 | 104 |
| SCL3 | loader checked on 12 SEEN datasets "to avoid the T1x failure" | 107 |
| RLAW | Declarations 1-2 with checks; row definitions changed once after the first gate run, before the hash | 113-115 |
| SOTA1 | Phase A gate with Amendment 1; ER-only calibration | 139-142 |
| SEC3 | a guard built and gated on SEEN carriers (CLOSED) | 167 |
| SEC4 | three guards on 16 SEEN carriers, D-GATE OPEN | 169 |
| SEC5 | two A6 candidates on 22 SEEN carriers, D-GATE-C CLOSED | 177-178 |
| SEC6 | D-RUN on 30 SEEN carriers; Amendments 1-3, the last after P1's FM6 | 217-224 |
| SEC6R | D-ID-R identity on 38 SEEN carriers | 242 |

**A discrepancy recorded for the verifier.** AL 167 (4) says SEC3's "PREREG.md, the freeze and the hash follow on
2026-09-28". The ledger's SEC3-0 anchor cell and commit 916d3d4 give "pushed 2026-09-27T23:42:45Z" (OC:445). PL 227
and AL 167 were committed together at 23:41:24Z (commit 373af46). The timing of SEC3's development gate inside that
window is not reconstructible from the record.

### 3(c) Where R3 or R12 forced a stop

**R3** ("a rule ... defined or changed after seeing any dataset may not be used on another dataset the same calendar
day", CLAUDE.md:100-104). In most cases it delayed a data step to the next UTC day:

- AL 25 (EQ2R), 63 (EQ4), 70 (T1x2), 104 (SCL2), 106 (d) (SCL3), 139 (1) (SOTA1), 169 (SEC4), 177 (SEC5), 214 (SEC6),
  242 (2) (SEC6R).

In four cases it changed the design:

- SEC1 ran on SEEN carriers at rung R5, "never PASS-0", rather than on unseen data that day (AL 96).
- BAYES-1 excluded EQ-B, defined that day (AL 66).
- SOTA1's diagnostics could not become a new arm the same day (AL 156).
- The registered smoothing was not tuned (AL 91).

The calendar-day rule sets no minimum interval. SEC3 was hashed at 2026-09-27T23:42:45Z, and its data were fetched
"from 2026-09-28T00:00:13Z" (ledger SEC3-0). That is 17.5 min apart (auditor's count, derived from those two times).

**R12** ("If Phase A leaves no hypothesis standing, stop ... Do not invent a weaker hypothesis", CLAUDE.md:161-163). It
is invoked by name or in spirit at:

- SAL (AL 13);
- FED (AL 71);
- the rupture detector (AL 88);
- the Ω accuracy programme ("proposes no further accuracy study ... R12's spirit", AL 85);
- Maps P5 (AL 118);
- CUT1 (AL 122);
- RW2 (AL 126);
- ARC-R (AL 134);
- STAKE1 (AL 160);
- SEC5 Part C (AL 178);
- RQM (AL 192);
- RRM (AL 195);
- RRM2 T6 (AL 198-199);
- OB1-C1 (AL 205) and OB1-C3 (AL 209);
- CPL1 (AL 230);
- ROB1 stage 4a (AL 231);
- SEC7 (AL 238);
- RLAW, as "CRR stays a grammar on this route, R12" (ledger RLAW-C).

One R12-spirit stop was overridden by the owner.

1. After AL 85, the owner wrote "I don't really want to give up on the continuous learning equanimity idea just yet"
   (PL 106 :997).
2. Declared synthetic exploration followed (Adam_SGD, AL 90-94).
3. SEC was then defined (AL 96). AL 143 records that SEC "grew out of the H-EQ programme ... the Adam_SGD scale-freeness
   result".
4. SEC is the lineage of the record's one PASS-1 (SEC4-1).

### 3(d) Exploratory variants rejected to avoid gate-shopping, and whether the rejection stopped development

The AGENT_LOG's "alternative rejected" column refuses post-result variants many times:

- tuning the convex surrogate (AL 4);
- "trying other operationalisations until one opened (forking path)" (AL 13);
- "re-running with a causal phase, a Poincaré section or other statistics until a carrier reads AHEAD" (AL 88);
- "changing the phase estimator or the event definition after the run" (AL 109);
- "no third round, which would be fishing" (AL 118);
- "running a redesign today and treating it as the declared gate" (AL 122);
- "simplifying the environment to suit a small model" (AL 160);
- "trying a third candidate" (AL 178);
- "a third negative stream tuned until IGR loses (gate-shopping)" (AL 192);
- "continuing with RRM-1 alone under this declaration" (AL 195);
- "re-running T2 at a larger E and calling it the gate" (AL 199);
- "dropping G-TIME S2 or re-running with a changed S1 to open the gate" (AL 205);
- "an amended stream run now to reopen the gate" (AL 209);
- "relaxing D-FAIL's bar (gate-shopping ...)" (AL 238).

Each refusal is of a variant under the same declaration or on the same day, not a permanent ban. Most entries name the
route: a new declaration, labelled post hoc, on a later day, often "only on the owner's instruction" (AL 122, 192, 209).

**Taken up later, under a new or post hoc declaration:**

- equal exploration (AL 73 → applied in AL 74; OC:470);
- Adam Declarations 3-4 (AL 92-94);
- RW2 round 2 (AL 125-126);
- RQM run 2 (AL 191-192);
- RRM → RRM2 (AL 195-199);
- the SEC3 guard → SEC4's clip (AL 167-169);
- Maps Declaration 2 (AL 117-118);
- the Lossless pause's Amendment 1 (AL 147);
- T1x → T1x2 (AL 69-70);
- EQ2R → EQ3's replication arm (AL 40, 59).

**Named as a next step but never mentioned again in the AGENT_LOG** (OC:456-470; a grep, so a follow-up done under
another name would be missed). These are lineage-level follow-ups the protocol allowed but nobody ran:

- BAYES-1b, "a convergence-scaled budget" (AL 67);
- H-REG (AL 130);
- LIFE1 (AL 162);
- a dose-matched CUT1 redesign (AL 122);
- EQ5, explicitly "not proposed" (AL 85);
- a causal-phase or Poincaré cut detector (AL 88);
- per-task normalisation of online EWC (AL 95);
- "Omega scaled by the number of settled occasions; balancing signal rather than noise" (AL 94);
- a stronger RQM criterion (AL 192);
- a SEC test against "a different reference" (AL 238);
- a harder FED surrogate (AL 71);
- the OB1 arc-triggered refresh, C2 (AL 202-203);
- STAKE1 on a capable model, RW3 (AL 158).

ARC-R was named in AL 132 and closed in AL 134.

**What the record shows about why these were not resumed.** The record does not say it was the protocol. After most
closures the next owner prompt points elsewhere, for example:

- after CUT1 (2026-09-24), PL 153-159 turned to the empty-cut engineering and real-world checks;
- after OB1-C1, PL 254 asked for "a consolidation" and the SEC4 literature sweep, and the agent declared C3 rather
  than C2 (AL 207-208).

The R12 entries themselves leave redesign to "the owner's decision" (AL 192, 195, 209). The proximate cause of
non-continuation is therefore split between R12, which forbids a same-declaration rescue, and the direction set by
the owner's prompts. The record does not separate the two.

### 3(e) Post hoc additions, and whether they weakened earlier passes, or fails

None of these edited a ledger verdict; they are append-only rows, labelled post-run lines, addenda or notes.

**Weakening passes:**

- EQ2-1 "PASS, FRAGILE" was relabelled into EQ2-1b "PASS-0 (provisional)". EQ2-1c then records "a failed replication"
  (ledger).
- SCL2-2, SCL2-2s and SCL2-3 are "PASS as scored (... not counted as PASS-0: the synthetic gate gives the same label)"
  (AL 105). The same caveat applies to SCL1-2 and SCL1-3, which keep R5 (AL 105 (a)).
- Adam B4-B5: the rule's earlier SGD advantage "was measured against the 10-point tuning grid" (AL 85).
- Synthesis batch 32 row 2's ADDS was shown, by a post hoc surrogate, to be "forced by the arithmetic" (AL 109).
- The literature check of the ADDS rows: "0 clean candidates" (AL 110; LT:68).
- "13 of 37 carrier-scorings are inert ... so 'not behind' is automatic there", touching EQ3-1, EQ4-I, SCL3-3 and
  SCL3-2 (AL 131). It is not re-scored.
- PRED70's post hoc amplitude column: the 7 H-L5 ADDS rows fail their own control (AL 175; RVF:40).
- P1's FM6: "EDGE, a uniform cap after task 1 with no Fisher, NOT behind the tuned lambda on 24/30" (AL 222).
- `gate_posthoc` (AL 236; ledger rows *-G):
  - SEC4-1 "would be printed UNINFORMATIVE and capped at PASS-0";
  - SCL3-3's gate is OPEN, "not affected".
- SPA1: SEC4's method is "KNOWN" by its declared rule (AL 210).

**Weakening fails, or the earlier negative verdicts:**

- SEC3-3-G and SEC5-1-G: those FAILs "would be printed UNINFORMATIVE" (AL 236).
- AL 81 (a) calls the one EWC-arm miss in EQ3-1, fars, "a pipeline sampling defect" (not a verdict).
- Adam Declarations 3-4 made the earlier "behind a finely tuned constant" verdict "conditional", post hoc and labelled
  (AL 93-94).
- AL 65 read synthesis row 28-1's WRONG as "a verdict on the FEP's object, not on A3".
- RLAW's K(inf) diagnostic: "no verdict changes" (AL 129).

**Net reading.** The post hoc layer cuts in both directions and changes no ledger verdict. Its largest single effect is
on the SEC family's criterion:

- It removes the discriminating power of SEC4-1's pass.
- It does the same to SEC3-3's and SEC5-1's fails.
- That criterion defect was found after 30 held-out carriers had been used. P1's "24/30" is over "the 30 now-SEEN
  held-out carriers" (AL 212).

### 3(f) Instrument and pipeline failures over time (chronological)

| date | failure | effect on a verdict | AL / ledger |
|---|---|---|---|
| 09-15 | OpenTimestamps unreachable; tag push refused | every row before SCL3 weakly anchored, so no PASS-1 was possible | AL 1 |
| 09-15 | MEAS loader read 0 series (`rdata` TypeError) | VOID; MEAS2 re-run with the values unread | MEAS-1..3 |
| 09-15 | PhysioNet 403 | CARD unrun until 09-26 (266.72 h hash→score, OC:430) | AL 164 |
| 09-17 | HASH.txt hashes itself | recorded; future preregs exclude it | AL 7, 111 |
| 09-17 | `unit_sigma` leverage bias (×1.1589 on ρ) | none: ρ is never thresholded (R5) | AL 30 |
| 09-21 | EQ2R frozen scorer crash (`hid` rebound to an array) | VOID; 3 carriers now SEEN | AL 40; EQ2R-VOID |
| 09-22 | EQ3 fars class emptied by the registered subsample | EQ3-1 FAIL on 1/6 scored as committed | AL 60, 81 |
| 09-22 | BAYES-1 optimiser does not reach the posterior | B0 NOT DECIDABLE; B1-B3 without verdict | AL 67 |
| 09-22 | T1x crash on a binary split feature, then a non-finite path | VOID; 6 carriers now SEEN | AL 69; T1X-VOID |
| 09-23 | EQ4 exclusions script path bug; satimage overlap with T1x | none (the scorer was unaffected; satimage kept) | AL 82 |
| 09-23 | ladder parser misread cells containing '\|' | allocations corrected | AL 86 |
| 09-23 | ratio guard divided by round-off | exact Ω = 1 task 0.1205 → 0.1887 (notes) | AL 100 |
| 09-24 | CI red: PDF dependency; CPU-feature dependence of pinned outputs | labels on Ω > 1 arms differ by CPU | AL 116 |
| 09-25 | RLAW K(∞) NaN in sensitivity cells | "no verdict changes in any cell" | AL 129 |
| 09-26 | SOTA1 start-up race; two container losses | identical reruns allowed | AL 151, 152, 154 |
| 09-26 | SOTA1 frozen runner passes rehearsal flags to lwf/ewc_on | SOTA1-ND NOT DECIDABLE (context arms only) | AL 153 |
| 09-29 | OpenBLAS kernel choice breaks `omega_sweeps` in CI | most CI runs stop early | AL 174, 244 |
| 09-30 | `m_checks` printed the full Python version | re-pinned | AL 240 |
| 09-30 | SEC family criterion met by a frozen learner | the post hoc gates (§3(e)) | AL 222, 236, 238 |
| 10-01 | SEC6 STRING targets read as numbers | all 12 carriers excluded, NOT DECIDABLE; 12 carriers now SEEN | AL 241; SEC6-1 |

**Held-out carriers opened without a decided primary verdict** (auditor's count, derived from the ledger dataset
cells): 27 in total.

- EQ2R: 3 (EQ2R-VOID).
- T1x: 6 (T1X-VOID).
- BAYES-1: 6 (BAYES1-B0).
- SEC6: 12 (SEC6-1).
- Not counted: MEAS's 20 cities. MEAS2's dataset cell says the file's "values [were] unread before the hash".

**Recurring cause.** EQ2R, T1x, SOTA1-ND and SEC6 all failed through a frozen path that the pre-hash smoke or loader
check did not exercise. The AGENT_LOG draws this lesson itself:

- "the Phase A smoke must run one task of every arm through the frozen runner itself" (AL 153);
- "selection (metadata only) ... could not see it" (AL 241).

### 3(g) The owner's prompts that steered direction

**Direction-setting prompts:**

- PL 2 (the prompt-log rule).
- PL 11 (:142): delete the nulls. Refused.
- PL 38 (:561): "broadening out with CRR, showing its implications, potential applied use cases".
- PL 60 (:673): the SYNTHESIS class.
- PL 102: what a PASS means.
- PL 106 (:997): "I don't really want to give up on the continuous learning equanimity idea".
- PL 139: RLAW kept out of the ladder.
- PL 150 (:1255): the focus becomes continual learning plus AI safety.
- PL 216 (:1585): the next-steps plan.
- PL 220 (:1611): labs.
- PL 252 (:1765): "find the actual big bottlenecks".
- PL 257 (:1787): "Sec4 was successful", a week-long applied programme.

**Framing that pushes toward a pass.** These are verbatim, each with the agent's handling:

- PL 13 (:167): "I agree with 1. especially if it makes the tests easier to pass, of course". The logged context
  records the change was "adopted on Daniel Friedman's technical grounds, not because it is easier to pass; the agent
  flagged in chat that the latter is a §10 temptation" (:175-178).
- PL 31 (:310): "Something that will actually work?". The context: hand over the control "only if the gate opens; if it
  does not open, report that instead" (:312).
- PL 196 (:1485): "Crr helped to arrive at the SEC tuning. It must have done because it happened in this repo". AL 143
  records the lineage and the ledger's "not a CRR rule".
- PL 238 (:1701): "Use the CRR to fine-tune the approach as required". AL 177 keeps the primary arm unchanged, "it would
  forfeit the replication", and reads the request as two A6 candidates behind a development gate, which closed (AL 178).
- PL 256 (:1785): "This is silly because we calculated the energy saving costs as high value and then thought it might
  not catch on".
- PL 257 (:1789): "Sec4 was successful". AL 212: "an analysis of SEC4's pass alone would select on the outcome",
  rejected.

**Breadth prompts.** Prompts requesting new batteries or domains, often back to back, include PL 42, 48, 51, 52, 54,
58, 59, 66, 67, 116, 130, 131, 217, 226, 234 (70 systems), 240 and 241. Their products are the retrodictive and R4
banks (§2.6), not ledger rows.

**Cadence of consecutive pre-registrations (OC:427-449; auditor's count, derived).**

- Within a lineage, the next study was hashed after the previous first-score commit by:
  - MEAS → MEAS2: 0.00 h (same commit);
  - T1x → T1x2: 0.00 h;
  - EQ3 → EQ4: 4.12 h;
  - SEC1 → SCL1: 5.83 h;
  - SCL1 → SCL2: 0.19 h;
  - SCL2 → SCL3: 1.70 h;
  - SEC3 → SEC4: 3.65 h;
  - SEC4 → SEC5: 2.92 h;
  - SEC5 → SEC6: 9.07 h;
  - SEC6 → SEC6R: 0.45 h.
- Every within-lineage successor in that list came within 10 h.
- Across the whole table, 17 of the 18 rows with a defined "prev score→hash" are under 24 h. The exception is SEC3, at
  30.40 h.

**Effect on the timing of the next design.** Each new prereg was designed after the previous result and before the
next calendar day:

- SEC4's guard was chosen on SEEN carriers 2026-09-28 (AL 169);
- SEC5's design 2026-09-29 (AL 177);
- SEC6's amendments 2026-09-30 (AL 217-222);
- SEC6R 2026-10-01 (AL 242).

## 4. Four-layer table (process-level observations)

| # | (1) observed phenomenon | (2) CRR interpretation | (3) ordinary / non-CRR explanation | (4) evidence that would distinguish |
|---|---|---|---|---|
| P1 | 25 gates closed before confirmatory data (§3(a)). The ledger holds 11 GATE CLOSED rows (OC:289) | the operationalisations of CRR ingredients do not survive their own positive and negative controls | many closures are design-level: no headroom, an invisible control, a criterion that cannot fail, a declared world where the mechanism has no work (e.g. §3(a) rows 3 v1, 6-10, 12, 17, 22, 25) | a redesigned gate on the same hypothesis, declared before running. Where that happened, 5 opened and 5 closed again (§3(a)) |
| P2 | 36 held-out FAIL rows, none carrying instrument words (OC:395-397) | genuine falsification pressure on H-EQ, H-L5, H-T1, the CRR learner, SEC | some FAIL rows include pipeline components (EQ3-1's fars, AL 81) or a criterion that cannot discriminate (SEC3-3-G, SEC5-1-G) | per-row re-reading by lineage (other readers); rows marked not fragile with a gate OPEN carry the most weight: MEAS2-1, CARD-1 (0/26 cells), T1X2-1 (5/5, not fragile), SOTA1-1a (5/5 seeds) |
| P3 | 27 held-out carriers opened without a decided primary verdict (§3(f)) | none: these say nothing about CRR | frozen-code paths not exercised before the hash; loader formats not checked on the target family | none needed; the record already classes them VOID / NOT DECIDABLE |
| P4 | request→hash ≤ 25 min for 15 of 20 studies (§3(b)) | — | a fast cadence set by the prompts; templated designs (CLAUDE.md §4-§6); development compressed into the session | not separable from the record: scratchpad and playground work is kept off the record by rule (AL 3; PL 19-27 contexts) |
| P5 | the SEC criterion's defect was found after the held-out runs (AL 222, 236, 238) | — | no must-fail control on the criterion was declared before SCL3/SEC3/SEC4/SEC5 | the SEC6/SEC6R design shows what a pre-registered instrument gate does: SEC6R-G CLOSED, "edge 8/9" (AL 245) |
| P6 | post hoc analyses weakened passes and fails alike (§3(e)) | — | append-only rules route every second reading into a labelled row or note | none: both directions are recorded |
| P7 | the owner's override of an R12-spirit stop (PL 106) led to SEC and the only PASS-1 (AL 85 → 90-96 → 169-172) | exploration guided by the H-EQ programme found a usable calibration | SEC's parts are published (SPA1 "KNOWN", AL 210); P1 found no CRR-proper ingredient load-bearing (CLAUDE.md §0, P1 summary; F11) | a test where a CRR-proper ingredient is ablated inside SEC. P1's M4 (arc secant) "adds nothing" (AL 222) |

## 5. Salvage classification at the process level (a mapping of mechanical classes, not a verdict on lineages)

The A-G categories belong to lines of inquiry (other readers' notes). This table only says which category each
mechanical class most often feeds. Every row still needs reading.

| mechanical class (OC:288-305) | usual category | where the default fails (examples) |
|---|---|---|
| VOID (5) | D | — |
| NOT DECIDABLE (13) | D or E | SEC6-* is D (loader, AL 241). BAYES1-B0 is E/D (optimiser error 0.18-0.89 sd against 0.1; CLAUDE.md §0). SEC3-0/1, SEC4-T, SEC6R-1F and SEC6R-A-* are E (too few carriers in the decidable set) |
| UNINFORMATIVE (14) | E, at the level of the criterion | rows the criterion cannot discriminate, in either direction |
| GATE CLOSED (11, plus the gates in §3(a) outside the ledger) | B or D, sometimes C (prior art) | B where the hypothesis did no work on a gate that could open (§3(a) rows 13-16, 18, 20, 23); D where headroom or controls failed |
| REDUCES / control violated / INERT (7) | C, plus A for violated mechanism statements | EQ2-4: "the mechanism statement ... is falsified as written" is A |
| FAIL, held-out (36) | A or C | lower where a pipeline component or criterion defect is recorded (§2.4) |
| FRAGILE (11) | F where a pass exists | ARC-A1 and SEC1-3 are seen-data |
| construction (8) | none (R0-like; "not support for CRR", ledger SCL1-1) | — |
| PASS-0 / PASS-1 (13) | F or G | SEC4-1's PASS-1 sits beside SEC4-1-G; no row is G at the process level |

## 6. Extinguished-lead check (process level)

Stops recorded at a lower level of abstraction than the claim they are sometimes taken to bear on:

1. **OB1-C3.** "Consolidation has no effect in the declared stream, so the arc-against-chord contest is not scored" (AL
   209). The arc-against-chord question was never scored. AL 206 notes that the record (T1X2-1) already disfavours the
   arc side. This stop is at the level of the stream (D/B), not the idea.
2. **CUT1.** A3 failed by "a dose effect" confound and A4 by an unmet must-fail premise (AL 122). The dose-matched
   redesign was never run (OC:459). Cut content was stopped at the level of design.
3. **The rupture detector.** Only the analytic-signal phase was tested (AL 88). CLAUDE.md:442 says a Poincaré section
   is a named alternative in `theory/CRR.md`, but an auditor's grep finds no "Poincar" in `theory/CRR.md` (derived). AL
   53 also calls it "CRR.md's named Poincare-section alternative". Whichever text holds, the alternative phase was never
   run (OC:462). This is a one-operationalisation stop.
4. **RQM.** It stopped because "the declared criterion cannot fail" (AL 192). The stronger criterion named there was
   never declared (OC:465). Instrument-level.
5. **The SEC family after P1.** "A SEC test that can fail needs a different reference ... declared from scratch" (AL
   238). It was never declared (OC:466). SEC6R reused SEC6's design (AL 242).
6. **BAYES-1.** B0 was NOT DECIDABLE through optimiser error (AL 67). BAYES-1b was never run (OC:456). The Bayes
   question for the rule (B1-B3) has no verdict.
7. **LIFE1 / G-CD3.** The gate is OPEN (AL 162), but it was not pre-registered because the only public data could not be
   loaded blind. This lead stopped at data access, not at the gate.
8. **STAKE1.** "The models could not act as agents" (ledger STAKE1-A). A real test needs a capable model (AL 158, 160).
   Stopped at the level of the instrument (model capability).

Stops at the level of the stated hypothesis (`theory/CRR.md` §9), with the sensitivity table not fragile:

- H-L5 on measles (MEAS2-1, "not fragile (0/26 ...)") and on the pulse (CARD-1, "not fragile (0/26 ...)");
- H-T1 (T1X2-1, "the path does not beat it on any carrier; not fragile");
- RLAW ("every admissible row FAILs, none fragile", CLAUDE.md §0);
- SOTA1-1 ("not fragile, 0 of 6 cells", CLAUDE.md §0).

SEC5-1 is also "not fragile: 0 of 40 sensitivity cells flip", but it sits beside SEC5-1-G ("would be printed
UNINFORMATIVE").

## 7. Question-10 evidence, both sides

**Evidence that the protocol was appropriately merciless:**

- **Nulls kept.** It refused to delete nulls when asked (PL 11; AL 2). It refused to patch frozen code and score
  partial results (AL 40, 69, 153, 241).
- **No control tuning.** It refused to tune positive controls or thresholds after seeing results (AL 4, 13, 76, 88, 118,
  178, 192, 205, 238).
- **First runs pinned.** First-run outputs were kept beside labelled post-run lines (AL 75, 98, 100, 117, 147).
- **Its own best pass examined.** It turned its own best pass into a post hoc caveat in the ledger (AL 236; SEC4-1-G),
  and recorded that SEC5-1 FAIL "stands as its replication" (SEC6-1).
- **Artefacts caught.** It caught a harness ADDS forced by arithmetic (AL 109), an omitted amplitude control in its own
  declaration (AL 175), and 13 inert carrier-scorings (AL 131). None of these was rescued.
- **Large-effect failures robust.** The large-effect held-out failures are not fragile (§6), so they do not hang on a
  window or a seed.

**Evidence that it killed immature operationalisations before they were explored:**

- **Little time before the hash.** Request-to-hash was 25 min or less for 15 of 20 studies (§3(b)). Exploration was
  kept off the record (AL 3) and so cannot be audited.
- **Design-level closures stopped by R12.** Ten of the 25 pre-data closures are classed above as design-level
  (headroom, an invisible control, a criterion that cannot fail, a mechanism with no work in the declared world:
  §3(a) rows 3 v1, 6-10, 12, 17, 22, 25; auditor's classification). Each became an R12 stop rather than a redesign.
  Only 10 redesigns are recorded (§3(a)).
- **Follow-ups never run.** Thirteen named follow-ups never reappear (§3(d); OC:456-470).
- **Infrastructure consumed held-out data.** It used up 27 held-out carriers without a decided primary verdict (§3(f)).
  The SEC criterion defect surfaced only after 30 held-out carriers had been scored (§3(e)), which suggests the
  pre-confirmatory stage did not test the criteria hard enough.
- **The R3 rule shaped timing more than maturity.** It allowed a 17.5-min hash-to-data interval across midnight (SEC3).
  It forced 20 h waits in other cases, and moved SEC1 onto seen data (§3(c)).
- **The override that paid off.** The one recorded override of an R12-spirit stop (PL 106) led to SEC and the record's
  only PASS-1 (§3(c); P7).

**Facts that bear on both sides:**

- Of the redesigns permitted after a first gate closure, 5 opened and 5 closed again (§3(a)). Three of those that
  opened lead to the record's held-out passes.
- Most non-continuations coincide with the owner moving the programme elsewhere (§3(d)), so they cannot be attributed to
  the protocol alone.
- The post hoc layer weakened fails as well as passes (§3(e)).

**What the record supports, by stage (stated as findings, not as a single adjective):**

- **Held-out scoring.** Append-only rows, no exemptions, frozen scorers, sensitivity tables: the record shows these
  catching real defects in both directions, and no case where they suppressed a result that later proved real.
- **Phase A and development gates.** Most closures here were about the gate's own construction. The rule then stopped
  the line, unless the owner re-opened it. Whether the underlying ideas were ready to test is not shown, either way.
- **Pre-hash infrastructure checks.** The checks on frozen-path smoke, loaders and criterion must-fail controls were
  repeatedly insufficient. That cost held-out data (AL 40, 69, 153, 222, 241).
- **The tempo of request → hash → next prereg.** Hours, set by prompts (§3(g)). Exploration on synthetic or seen data
  happened, but inside those windows and off the record.

## 8. Open questions for Phoenix (process)

**What may be explored:**

- An explicitly exploratory environment whose runs are logged and committed. Today they are kept off the record (AL 3),
  so maturity cannot be audited.
- A redesign path after a gate closes for a design reason, declared and labelled, without requiring the owner to
  restart the line (§3(a) rows 6-10, 17, 22, 25).
- A maturity checklist before any hash:
  - the frozen runner smoke-run on every arm (AL 153);
  - the loader validated on the target family's format (AL 241);
  - a must-fail control on the criterion itself (AL 222, 238);
  - headroom shown (AL 92, 125).
- Re-opening the thirteen unrun follow-ups (§3(d)) under fresh declarations, each with its gate.

**What must never be claimed:**

- Any count that mixes the retrodictive banks with ledger rows (§2.6; RVF:10).
- A held-out pass without its post hoc gate row beside it (SEC4-1-G; SEC6R-G).
- A post hoc OPEN gate (AL 93, 147) as a result.
- A fail that sits beside a CLOSED criterion gate (SEC3-3-G, SEC5-1-G) as evidence against the method, any more than
  its pass.
- That the 27 carriers consumed by VOID or NOT DECIDABLE outcomes tested anything.
- That a fast request→hash interval measures how mature a design was, in either direction (OC:451-453).
