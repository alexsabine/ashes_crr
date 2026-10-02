# Pre-Phoenix audit notes: L-RLAW, L-RETRO, L-ONT, L-APP

- **Reader:** one subagent of the Pre-Phoenix interpretive audit (`Pre_Phoenix_Audit/DECLARATION.md`; prompt-log entry 260,
  `notebook/PROMPT_LOG.md:1817`).
- **Status:** an interpretive note, not evidence (R8). It changes no verdict, row, pinned output or log entry.
- **Citations:** every number is copied from the file and line, or the ledger row, cited next to it.
- **Derived counts:** any count I made myself is marked **auditor's count (derived)**, and the method is stated.
- **Readings:** sentences marked *auditor's reading* are interpretation. They are not record.

---

## 0. Cross-lineage conclusions (short form)

1. **RLAW is a genuine falsification, but of a conjecture added on top of CRR.md, not of anything CRR.md claims.**
   - `theory/CRR.md:268-271` (O1) says retention depth is open and "no retention law is claimed".
   - CRR.md §6 opens with "the amount of past a system carries is a property of the system's own dynamics"
     (`theory/CRR.md:256-257`). RLAW-C's soil failure (memory "set by its thermal diffusivity and depth",
     `reports/rlaw.md:107-108`) matches that sentence. It contradicts only the CRR 2.0 law.
2. **What the retrodictive record establishes:** broad expressive coverage, which is redescription. It does not establish
   unique prediction.
   - SHARP 0 of 197; the framework supplies the flow in 0 of 109 rows (`Epistemic_Review/checks/ladder.txt:15-20`).
   - ADDS: 10, then 0 clean candidates after the literature check (`theory/retrodictions/synthesis_batches/literature_check.txt:64-65`).
   - The SYNTHESIS outcome rule makes REDUNDANT the expected label for a correct grammar. ADDS is reachable mainly by
     extending a domain model (adding an A6 memory). Its T-C check then verifies the extended model's own mathematics,
     not the world.
3. **The redundant:fail ratios fall as tests get more demanding:** 6.35, then 3.50, then 1.94
   (`Epistemic_Review/checks/redundant_vs_fail.txt:4-8`).
   - The PRED70 "redundant" count includes 15 rows whose prediction Q failed: auditor's count (derived), §2.3.
   - So the PRED70 layer is better read by its own Q line: held 35, failed 33 (`Predictions70/checks/tally.txt:79`).
4. **Conceptual overfitting is visible in both directions.**
   - *Spurious agreement:* the unit "chosen to make the check pass", and 0 of 15 external SHARP claims surviving.
   - *Spurious failure:* 10 of PRED70's 18 WRONG rows rest on translations CRR does not make (APPLICATION, KNOB).
4b. **The ontology's testable commitments were mostly not tested on held-out data.**
   - Only C6, the four hypotheses of `theory/CRR.md` §9, reached the ledger.
   - A3/H-CUT has no held-out ledger row.
   - The ontology's own prerequisites were never carried out, although confirmatory studies continued:
     - the causal instrument and the v3.2 decision list (`ontology/05_next_steps.md:6-47`);
     - `theory/CRR.md` was last changed 2026-09-17 (commit 455780b);
     - `src/crr/instrument/core.py` was last changed 2026-09-17 (commit 33faec5).
5. **The applied suite finds no row in which a CRR-proper ingredient is shown to be load-bearing.**
   - The 17 rows read: "CRR-proper but not load-bearing 4 ... none 2 ... not decided by a pinned source 11"
     (`Applied_Suite/checks/suite.txt:889`).
   - "not load-bearing" means "not shown to bear load by any pinned test; it does not mean shown irrelevant"
     (`suite.txt:48`).
   - The pause rows are "not decided" partly by definition: Proposition 7 is excluded from the CRR-proper list
     (`suite.txt:13-14`).
6. **On question 10 for these lineages, the protocol was not what stopped exploration.**
   - RLAW went from request to hash in 1 h 24 min, a pace the owner set.
   - The exploratory layer (the retrodictive bank, PRED70, labs) was large and unconstrained.
   - Where leads stalled, the cause was:
     - direction: L01 was never preregistered, and the 7 PRED70 A6 candidates were never literature-checked;
     - resources: D3 experiments are excluded by the owner's no-spend rule (`labs/README.md`, D3 row);
     - a frozen theory text: v3.2 was never decided.
   - The rules did not cause the stalls.

---

## 1. L-RLAW: the regeneration law α* = K(v_own) ("CRR 2.0")

### 1.1 Trajectory (dated, cited)

| when (UTC) | event | source |
|---|---|---|
| 2026-09-24 04:21:19 | Prompt 136: write the scratchpad answers (entries 134-135, "how could we realistically turn CRR from a Grammar into a Theory?") into the ontology folder | `notebook/PROMPT_LOG.md:1187`, `:1169-1183` |
| 2026-09-24 04:22:13 | `ontology/15_grammar_to_theory.md` committed; route 1, "The regeneration law: fix the memory depth. The recommended empirical route" | commit 35d32c8; `ontology/15_grammar_to_theory.md:117-134` |
| 2026-09-24 04:26:27 | Prompt 137: "Please test the following version of CRR (CRR 2.0) on five different domains where it can fail. Full pipeline as usual. Ensure the mathematics is internally sound first." The law is stated as q = 1 − K(v), claimed "for every system that regenerates from its past, including ones that do no inference at all" | `notebook/PROMPT_LOG.md:1191-1199` |
| 2026-09-24 04:27:31 | Declaration 1 (checks M1-M10) pushed before its script | commit f5f3647; `Regeneration_Law/DECLARATION_1.md:1-30` |
| 2026-09-24 04:45:36 | Literature check committed | commit 58d2358 (`docs/citations/rlaw_literature_2026-09-24.md`) |
| 2026-09-24 (morning) | Declaration 2 (M11-M14) and the gate design. The first gate run showed the constant-comparison row alone passing on must-fail surrogates, so the rows were redefined before the hash | AGENT_LOG 113, 114 (`notebook/AGENT_LOG.md:126-127`) |
| 2026-09-24 05:23:12 | Prompt 139: keep CRR 2.0 out of the epistemic ladder, "because it is a different form of CRR which was not in the initial conditions of this repo" | `notebook/PROMPT_LOG.md:1205-1207`; AGENT_LOG 114 |
| 2026-09-24 05:50:35 | Prereg hashed: dc8a7101, commit be82a3f; OTS later complete in Bitcoin block 968363 onward | ledger RLAW-1 (`ledger/LEDGER.md:142`); `reports/rlaw.md:6-9` |
| 2026-09-25 00:40:40 | Data step; scored once and rerun byte-identical | AGENT_LOG 129 (`notebook/AGENT_LOG.md:142`) |
| 2026-09-25 | Ledger rows RLAW-1 … RLAW-C; `reports/rlaw.md` | `ledger/LEDGER.md:142-151` |

**Elapsed time (auditor's count, derived from the timestamps above):**
- prompt 137 to prereg commit: 1 h 24 min 08 s;
- prompt 137 to data step: 20 h 14 min 13 s.

### 1.2 Operationalisations and added assumptions

The **core idea** comes from CRR.md O1: "Whether the memory depth of a system follows from its own state model at Ω = 1,
with no other parameter, is open. Until it is derived for a mean-reverting or oscillatory state model and checked,
retention is **not** a CRR quantity and no retention law is claimed" (`theory/CRR.md:268-271`). It also uses P4, whose
formula "is not CRR's" (`theory/CRR.md:259-266`).

Assumptions added to make it testable:

1. **One universal zero-parameter law.**
   - α* = K(v_own), with v_own = σ_η/√(σ_ε² + δ²/12) (`prereg/rlaw/PREREG.md:25-29`).
   - This is the owner's formulation (prompt 137) and route 1 of `ontology/15_grammar_to_theory.md:117-125`.
2. **Ω = 1 dropped.**
   - M7 showed equal pull only at v = 0.7071 (`Regeneration_Law/checks/math_checks.txt`, line M7).
   - "CRR 2.0 drops 'at Ω = 1'" (`prereg/rlaw/PREREG.md:30-32`).
   - So the tested law already departs from O1's own wording.
3. **v from a random-walk-plus-noise model of the input, not from the system's own state model.**
   - M8: for an AR(1) environment the approximation is 2 % off (`math_checks.txt`, M8: "relative difference 0.020").
   - O1 asks for a derivation "for a mean-reverting or oscillatory state model" (`theory/CRR.md:269-270`). No such
     derivation was made.
4. **The input's drift sets memory, including in systems that do no inference.**
   - This is the "CRR-only" content (`prereg/rlaw/PREREG.md:53`).
   - The literature check found the contrary stated for heat conduction (`Regeneration_Law/DECLARATION_2.md:23-26`).
5. **Domain-specific substitutions.**
   - Two-step domain: the law's prediction is replaced by "the numerically optimal constant rate". M13 was "OFF by more
     than 25 % at every mean gap" because the arm is mean-reverting (AGENT_LOG 113).
   - SPF: units are whole-sample because of M12 (AGENT_LOG 113).
   - Each domain row is "level AND beats-the-constant" after the first gate run (AGENT_LOG 114).

**Which added assumption later failed.**
- Assumption 4 failed outright: soil 5 cm, 0/112 within ×2 (RLAW-4); tracking Spearman −0.065 (RLAW-4T).
- Assumption 1 failed in every domain: RLAW-U 0/5.
- Assumption 3 is implicated as a resolution problem on soil, as a reading:
  - the moments estimator "finds no noise component at all on 366 of 369 deeper-soil units" (`reports/rlaw.md:63-64`);
  - the ML v sits "at the grid edge" for 64/112 soil 5 cm units and 366/369 deeper units (`reports/rlaw.md:48-49`);
  - so α* collapsed towards 1: median α* 0.9997 for soil 5 cm (RLAW-4) and 0.9982 for deeper soil (RLAW-4D).

### 1.3 Results (verbatim verdicts)

- RLAW-1 **FAIL** (not fragile): 1/8 within ×2; law median |log err| 2.662 vs constant 0.682 (`ledger/LEDGER.md:142`).
- RLAW-2 "FAIL as computed; **no counted verdict** (not admissible)": G+ power 0.600 (`:143`).
- RLAW-3 **FAIL** (not fragile): 1/5 (`:144`).
- RLAW-4 **FAIL** (not fragile): 0/112 (`:145`).
- RLAW-4T **FAIL** (not fragile): Spearman −0.065398, CI −0.248 to 0.134 (`:146`).
- RLAW-4D **FAIL** (not fragile): 140/369 (`:147`).
- RLAW-4DT "PASS as computed; **FRAGILE** (8 flips > 1); not PASS-0; RLAW-C does not read it": Spearman 0.522909, CI
  0.439 to 0.600, every own:off cell flips (`:148`).
- RLAW-5 **FAIL** (not fragile): 6/197 (`:149`).
- RLAW-U **FAIL**: 0/5 (`:150`).
- RLAW-C **FAIL** "(as the prereg said physics expects; CRR stays a grammar on this route, R12)" (`:151`).
- **Out of the ladder.** These rows are excluded from the epistemic ladder at the owner's instruction:
  "excluded, CRR 2.0 (owner's instruction, prompt-log entry 139): 10 rows" (`Epistemic_Review/checks/ladder.txt:70`).
  - Of the 10, 8 carry a FAIL verdict (RLAW-1, -3, -4, -4T, -4D, -5, -U, -C). **Auditor's count (derived)** from
    `ledger/LEDGER.md:142-151`.
  - So the ladder's "held-out FAIL 37" (`ladder.txt:297`) does not include them. Any summary that quotes the ladder
    alone omits 8 strongly anchored held-out FAILs. The exclusion is a stated owner choice, recorded here, not undone.
- **Instrument defect.** The frozen K(∞) evaluates to NaN in the four `v:mom own:off` sensitivity cells. A post hoc
  diagnostic shows "no verdict changes in any cell of any domain" (`reports/rlaw.md:51-65`; AGENT_LOG 129).

### 1.4 Four-layer table

| # | observed phenomenon | CRR interpretation | ordinary / non-CRR explanation | evidence that would distinguish |
|---|---|---|---|---|
| R-a | Forecasters, households, option markets and soil weight the newest input far less than K(v_own); two-step learners far more (`reports/rlaw.md:96-103`: SPF median α̂ 0.0583 vs α\* 0.7478; two-step 0.3938 vs 0.0420) | the zero-parameter law is refuted (`reports/rlaw.md:127-130`) | soil: "memory ... set by its thermal diffusivity and depth" (`reports/rlaw.md:107-108`; heat conduction is linear, `DECLARATION_2.md:23-26`). Two-step: high fitted rates are known (`PREREG.md:56-58`, Daw 2011 via the literature agent). Forecasters and markets: "This study cites no source on why they do not" (`reports/rlaw.md:133-135`) | already decided for the law as stated. Whether *any* system-state-derived memory law holds (O1 proper) would need a derivation for the system's own state model, which O1 asks for and RLAW did not make |
| R-b | Deeper-soil tracking: Spearman 0.523 with the own unit, failing in every own:off cell (RLAW-4DT) | the own unit (A1′) carries the tracking | *auditor's reading, untested:* α̂ and α\* may both covary with probe depth or probe-specific quantisation, giving a cross-unit correlation with no law behind it | a within-depth (stratified) partial correlation, or a fresh preregistered soil network |
| R-c | α\* compressed near 1 for soil (median 0.9997, v at the grid edge 64/112) | — | the local-level model is mis-specified for a smooth daily air series ("almost noiseless random walk", `reports/rlaw.md:105-106`) | *auditor's reading:* RLAW-4T's tracking FAIL may be low-powered because α\* barely varies. RLAW-4's level FAIL does not depend on this (α̂ median 0.1901 against roughly 1) |
| R-d | The law loses to a leave-one-unit-out constant in every domain (`reports/rlaw.md:23-24`) | the law adds nothing over the domain's typical memory | memory is a domain trait (sluggishness, diffusivity), not a function of drift | — (a comparator defeat) |

### 1.5 Salvage classification

- **A (genuine falsification pressure), on the CRR 2.0 conjecture.**
  - *Chain:* `theory/CRR.md:256-257` + O1 (`:268-271`) + P4 (`:259-266`) + A1′ (`:55-68`) → α* = K(v_own), universal,
    zero-parameter, v from a local-level fit → five unseen domains → RLAW-U 0/5, RLAW-C FAIL, none fragile.
  - *Highest level reached:* the stated law (a hypothesis *added* to CRR, outside CRR.md's four §9 hypotheses). It does
    not reach a principle stated in CRR.md: CRR.md says "no retention law is claimed" (`:270-271`). Nor does it reach
    A6/P3, since "CRR does not fix q" (`:160`).
  - It does refute the strongest universality reading: that a non-inferring system's memory follows its input's drift.
- **B (operationalisation).**
  - The input-drift local-level operationalisation of "own state model" is one translation of O1.
  - On soil it degenerated (R-c), and on two-step it was replaced by a numerical optimum (M13).
- **C (comparator defeat).** The constant beats the law everywhere (R-d).
- **D (instrument).** The K(∞) NaN, confined to sensitivity cells; no verdict changed.
- **E (identifiability).**
  - RLAW-2 is not admissible: G+ power 0.600 < 0.8 (AGENT_LOG 115).
  - RLAW-4T is possibly underpowered because α* is compressed (*auditor's reading*).
- **F (near-win).** RLAW-4DT tracking, FRAGILE. This is a pattern only, not a pass.

### 1.6 Extinguished-lead check

Was something killed at a lower level than the claim it was taken to bear on? Partly. The record itself is careful: "It
does not bear on H-L5, H-T1, H-EQ or H-CUT, or on the empty-cut construction" (`reports/rlaw.md:137-138`). Two
framings deserve note.

1. **"CRR stays a grammar on this route (R12)"** (RLAW-C).
   - What failed is one maximally risky translation of an *open* item.
   - O1's own condition was not met: "until it is derived for a mean-reverting or oscillatory state model"
     (`theory/CRR.md:269-270`). M8 and M13 show mean reversion was present in at least one domain.
   - So a more modest O1 reading was never tested. Neither was "memory depth follows from the system's *own* dynamics" in
     the sense of `theory/CRR.md:256-257`.
   - *Auditor's reading:* RLAW-C's result is consistent with CRR.md §6's sentence that memory "is a property of the
     system's own dynamics". The refuted part is the added claim that the *environment's* drift sets it.
2. **The domain choice made the CRR-only test a foreseen loss.**
   - The prereg said: "The foreseeable result of domain 4 is FAIL" (`prereg/rlaw/PREREG.md:55`).
   - Four of five domains could only test Muth-optimality, "not CRR's" (`PREREG.md:51`).
   - This is honest. It also means the study had low prior information value for CRR beyond confirming known physics.

### 1.7 Answers to questions 1-9 (RLAW)

1. **Initial idea:** fix memory depth with a zero-parameter law (O1, route 1).
2. **Operationalisation:** α* = K(v_own), with v from an ML local-level fit; five domains.
3. **Added assumptions:** universality including non-inferring systems; input drift as the state model; Ω = 1 dropped;
   the reporting quantum as the own unit; domain substitutions (two-step optimum; whole-sample SPF).
4. **Added assumptions that failed:** universality (RLAW-U); non-inferring systems (RLAW-C); the local-level v
   degenerated on soil (R-c).
5. **Reached the CRR claim?** None reached a CRR.md hypothesis. The added CRR 2.0 law is refuted.
6. **Reached only an implementation or translation:** the specific v estimator; the two-step substitution; the K(∞)
   defect.
7. **Interesting despite failing:**
   - the robust *direction* of the misfit (sluggish versus over-reactive, none fragile);
   - RLAW-4DT's own-unit-dependent tracking (fragile).
8. **Successes reduced to known mathematics:** the inferring-domain law *is* Muth/Kalman (`PREREG.md:51`), so a pass
   there would not have been CRR's.
9. **Infrastructure or identifiability:** RLAW-2's power; the K(∞) NaN (no verdict changed); the α* compression on soil
   (reading).

### 1.8 Question-10 evidence (RLAW)

- **Pace.** The idea went from the owner's request to a hashed, gated prereg in 1 h 24 min (auditor's count, §1.1).
  In that time it had:
  - 14 synthetic checks (M1-M14);
  - one literature check;
  - one gate redesign before the hash (AGENT_LOG 114).
- **Compression of the route-1 plan.** The note recommended:
  - a literature check first;
  - "derive the law formally";
  - a gate;
  - "three blind, anchored preregistrations on three unrelated unseen fields, each with the domain's fitted memory as a
    baseline that can win, then replication" (`ontology/15_grammar_to_theory.md:182-190`).

  All of it ran as one prereg over five domains, on the same morning.
- **What the protocol did not do.** R2 and R3 did not stop exploratory development here. No real-data exploration
  happened because none was asked for, and the literature already predicted the CRR-only failure. The derivation O1 asks
  for (a mean-reverting state model) was skipped in favour of a random-walk approximation that M8 quantified.
- **Reading.** The owner-set pace moved straight to confirmation, which is the opposite of suppression. The protocol's
  part was to make the outcome clean and unambiguous.

### 1.9 Open questions for Phoenix (RLAW)

- **May explore.**
  - Derive memory depth from a *system's own* state model (diffusion for soil; mean-reverting arms for bandits) and ask
    whether any CRR-specific quantity (the own unit) adds to the domain's model. Start in an explicitly exploratory space
    on the now-SEEN RLAW data.
  - The RLAW-4DT pattern, as an exploratory question with a depth-stratified analysis.
- **Must never claim.**
  - That the Regeneration Law holds anywhere.
  - That RLAW's failure refutes a CRR.md hypothesis.
  - That the ladder's FAIL count is the full held-out failure record: it excludes 8 RLAW FAILs by owner instruction.

---

## 2. L-RETRO: the retrodictive banks

### 2.1 Trajectory (dated, cited)

| when | event | source |
|---|---|---|
| 2026-09-17 | Issue-#21 battery and the sister batteries: 197 graded rows across all batteries | `Epistemic_Review/checks/ladder.txt:3-15` |
| 2026-09-17 | External SHARP claims, made by another instance of the model, re-derived: "TALLY over the 15 unique systems ... SHARP=0 CONSIST=6 DESCR=5 FAILS=4" | `theory/retrodictions/sharp_claims.txt:67-69`; AGENT_LOG 11 |
| 2026-09-17 | SYNTHESIS class defined (owner prompt 60). Its rule: T-G ablation (1 %), T-N domain theorem (1 %), T-C check | `docs/notes/2026-09-17_synthesis_class.md:29-46`; `src/crr/synthesis/harness.py:34-46`; AGENT_LOG 29 |
| 2026-09-17 to 21 | Batches 01-26: re-reads of the battery rows, with estimator decisions taken at the prototype stage from prototype numbers | AGENT_LOG 30-54 (e.g. 32, 50) |
| 2026-09-18 | SHARP retired for retrodictions | `theory/retrodictions/README.md` ("Grade reading, accepted 2026-09-18") |
| 2026-09-22/23 | FEP batches 27-28 | `ladder.txt:25` |
| 2026-09-23 | Epistemic Review: the ladder, the FLOW audit, and R2 counted as "a pass at the retrodictive level" | `Epistemic_Review/EPISTEMIC_REVIEW.md:31-39`; AGENT_LOG 80 |
| 2026-09-24 | Batches 29-30 (Rovelli, Smolin); batches 31-32 declared blind and OTS-stamped before code | AGENT_LOG 108, 109 |
| 2026-09-24 | Literature check of every ADDS row (prompt 132). The rule was pushed before the findings (a5d9418) | AGENT_LOG 110 |
| 2026-09-26 | labs/ (prompt 220): entry rule; bank index of 166 rows; CANDIDATES.md (L03 first; L01 + L02; L04-L06 need a sharper H1) | AGENT_LOG 163; `labs/README.md`; `labs/CANDIDATES.md` |
| 2026-09-27 | L03 = study CARD: CARD-1 **FAIL** | `labs/CANDIDATES.md:76-77` |
| 2026-09-27 | FRONTIER: RESTATES 10, GUIDES 1 (F2a = L01), AVOID 2 | `labs/frontier/FRONTIER.md:15-32`; AGENT_LOG 166 |
| 2026-09-29 | PRED70: 70 declared predictions (pushed at 8397478 before any model) | `Predictions70/PREDICTIONS70.md:5-11`; AGENT_LOG 175 |
| 2026-09-29 | Redundant against fail (prompt 235) | `Epistemic_Review/REDUNDANT_VS_FAIL.md`; AGENT_LOG 176 |

### 2.2 What the retrodictive record establishes, with denominators kept apart

| layer | denominator | positive | negative | other | source |
|---|---|---|---|---|---|
| batteries | 197 rows | CONSIST 41, DESCR 86 | FAILS 20 | TENSION 9, OPEN 41, SHARP 0 | `ladder.txt:15` |
| FLOW audit | 109 rows printing FLOW | — | — | domain 98, none 11, framework 0 | `ladder.txt:16-20` |
| synthesis, real-domain | 164 rows | REDUNDANT-IG 39, REDUNDANT-DOMAIN 59, ADDS 10 | WRONG 28 | INTERNAL 22, UNSTATED 4, PROPOSES 2 | `ladder.txt:28` |
| hit rate of CRR-proper ingredients where checkable | 97 rows (R2 + R3 + WRONG) | 69 | 28 | — | "69 of 97 = 0.7113 (Wilson 95 % interval 0.6145 to 0.7921)" `ladder.txt:41` |
| ADDS after the literature check | 10 | 0 clean candidates | — | "3 ... REDUNDANT-DOMAIN by the literature, 6 keep R3 with the direction known ... 1 removed" | `literature_check.txt:64-65` |
| expert review of ADDS | — | — | — | "reviewed by a named expert 0" | `ladder.txt:397` |
| PRED70, declared on synthetic models (R4) | 70 | Q held 35; ADDS 14, of which 7 survive the amplitude control | Q failed 33; WRONG 18 | Q not computable 2 | `Predictions70/checks/tally.txt:77-82` |
| PRED70 investigator's forecast | 70 | right on 33 (0.4714) | — | — | `tally.txt:84` |
| held-out ledger, a *different denominator* | ladder rows | PASS-0 15, PASS-1 1, PASS-2 0 | FAIL 37 | NOT DECIDABLE 11, VOID 4, and others | `ladder.txt:297-303, 335` |

**What it establishes.**
- CRR's vocabulary can be attached to a very wide range of domain mathematics.
- Where a CRR-proper ingredient changed a number and the result could be checked, it landed on the domain's known value
  69 of 97 times (`ladder.txt:41`).
- The procedure could miss: WRONG 28, FAILS 20.

**What it does not establish.**
- **No unique prediction.** SHARP was reached 0 times, and the flow is supplied by the framework 0 times
  (`ladder.txt:20`). There are 0 clean ADDS after the literature check.
- **No base rate.** "There is no rate for how often an arbitrary framework with the same ingredients would land"
  (`EPISTEMIC_REVIEW.md:114-115`). So 0.7113 cannot be compared with a null.
- **Q was not blind in the re-reads.** "A tester who knows the answer can pick which proposition to state ... No
  pre-registration of Q exists for any synthesis row" (`EPISTEMIC_REVIEW.md:111-113`). Batches 31-32 and PRED70 are the
  exceptions: there Q was declared first.
- **No real-world data.** All of it is known results or the domains' own synthetic models (R1-R4).

### 2.3 Redundant:fail ratios per layer, and a caveat on what "redundant" contains

- The ratios: batteries 127:20 (6.35); synthesis 98:28 (3.50); PRED70 35:18 (1.94)
  (`Epistemic_Review/checks/redundant_vs_fail.txt:4-8`). The record's reading: "The more a test demands of CRR, the
  smaller the ratio" (`REDUNDANT_VS_FAIL.md:19-21`).
- **Caveat (auditor's count, derived).** In PRED70, "redundant (IG or DOMAIN): 35 of 70, of which Q held 20"
  (`tally.txt:83`). So **15 redundant rows had Q fail**: P02-2, P02-5, P04-1, P04-2, P04-4, P06-1, P07-3, P09-1, P09-3,
  P09-5, P10-3, P12-1, P12-3, P12-5, P13-4.
  - *Method:* I listed every row in `tally.txt:5-74` whose outcome is REDUNDANT-IG or REDUNDANT-DOMAIN and whose Q column
    reads "fails". There are 15, matching 35 − 20.
  - The harness assigns REDUNDANT before it consults T-C (`harness.py:40-46`).
  - So `redundant_vs_fail.txt:45`'s gloss "redundant (consistent but not risky): 35" is not accurate for those 15. They
    are rows where CRR's ingredient did nothing *and* the prediction failed.
  - The informative PRED70 ratio is the Q line: held 35, failed 33, not computable 2 (`tally.txt:79`).
- **Is REDUNDANT the expected outcome for a correct grammar? Yes (auditor's reading of the rule).**
  - The outcome function returns REDUNDANT-DOMAIN whenever the CRR value agrees with the domain's own theorem within 1 %
    (`harness.py:42-43`). A correct re-expression of a domain's mathematics must land there.
  - ADDS requires three things: T-N to miss (no domain theorem cited, in which case "T-N passes vacuously",
    `synthesis_class.md:38`, or the theorem gives a different value), T-C to hold, and T-G to differ.
  - When CRR modifies the domain's model, T-C is checked "in the domain's own mathematics" (`synthesis_class.md:39-41`)
    *for the modified model*. So ADDS certifies that an extended model has a property. It does not certify that nature
    uses the extension.
  - **Auditor's count (derived)** from the descriptions at `ladder.txt:55-65`: 9 of the 10 real-domain ADDS rows insert an
    A6/P3 remembered state into a domain model. The tenth, batch 32 row 2, is the A3 row later found to be an artefact.
    The literature check found that shape known (3 redundant, 6 direction known).
  - **A second route to ADDS is noise.** ROB1's report: "a stochastic row's T-N at the harness's 1 % relative tolerance
    can miss on sampling noise alone ... Such an ADDS is a tolerance artefact, not a CRR addition"
    (`Robotics/checks/tally_4b.txt`, REPORT section; RA2 "29 of 40 differ", RA7 "34 of 40").
  - **Epistemic meaning.** A high REDUNDANT share is what a correct, non-generative grammar produces. It shows coverage,
    not novelty, and cannot discriminate a correct abstraction from investigator choice of reading. WRONG, by contrast,
    is informative: "a WRONG row is, by construction, one where CRR's ingredient changed the answer and the changed
    answer was wrong" (`REDUNDANT_VS_FAIL.md:34-35`).

### 2.4 Did the ADDS rows survive the literature check? No clean one did.

- The tally: "1 FOUND-EXACT / 2 FOUND-THEOREM / 6 PARTIAL / 0 NOT FOUND / 1 ARTEFACT"
  (`literature_check.txt:64`). Under the pre-pushed rule, PARTIAL means "direction known" (AGENT_LOG 110).
- The rule was fixed before the findings, and a looser reading was rejected. The note states that for the
  switching-contingency and SIR rows "the claim itself is published and only the numbers are not" (AGENT_LOG 110).
- **PRED70's 7 A6 ADDS candidates were never literature-checked.**
  - "They are not claims until a literature check of each one is done" (`PREDICTIONS70.md:77-78`); "pending a literature
    check" (`REDUNDANT_VS_FAIL.md:75`).
  - A grep for those row ids outside `Predictions70/` finds no follow-up (auditor's search, 2026-10-02). This is an open
    item, not an extinguished lead.
  - P14-4 already "holds only against the fixed-rate form" of FedAvgM (AGENT_LOG 175).

### 2.5 Did PRED70's WRONG rows reach CRR principles?

The reading of `CRR.md` §9 (`redundant_vs_fail.txt:33-36`; `REDUNDANT_VS_FAIL.md:48-53`) sorts the 18 WRONG rows:

| class | count | rows | what they reach |
|---|---|---|---|
| FALSIFIES | 6 | P02-1, P08-4, P11-2, P11-3, P12-4, P13-2 | H-L5 (4) and H-CUT (2) as stated in `theory/CRR.md:123-131, 200-209`, but only on the domains' *standard synthetic models* (R4). Hypothesis level, not real systems |
| SCOPE | 2 | P05-1, P12-2 | outcomes CRR itself predicts: the convex learner is H-T1's must-fail; no rotor means O3 |
| APPLICATION | 6 | P03-5, P05-3, P06-5, P07-4, P10-2, P10-4 | an axiom used as a control or dynamical model CRR does not claim. A translation only |
| KNOB | 4 | P05-5, P11-1, P11-4, P14-1 | a value CRR does not fix (q = 0.5 fixed by the declaration, AGENT_LOG 175). A translation only |

- In addition, "harness ADDS rows that are section-9 H-L5 FAILs (the amplitude control matches): 7"
  (`redundant_vs_fail.txt:40`). The cause was the investigator's declaration omitting the control (AGENT_LOG 175).
- Total "against a falsifiable CRR claim: 13" (`redundant_vs_fail.txt:43`), all at R4 on synthetic domain models.

### 2.6 Evidence of conceptual overfitting

**Over-specific translations producing spurious agreement:**
- External SHARP claims: "rule 2: the unit was chosen to make the check pass" (`sharp_claims.txt:60`). Others hold "on
  the symmetric (logistic) member" only (`:12`, `:40`), or reproduce a definition (`:16`, `:32`). SHARP survives on 0 of
  15 (`:69`).
- Batch 32 row 2 read ADDS through estimator arithmetic. "The analytic signal writes x = A cos(phi) exactly, so zero
  crossings sit a half-turn apart" (AGENT_LOG 109; `literature_check.txt:52-56`).
- ROB1 ADDS-by-noise (above).

**Over-specific translations producing spurious failure:**
- 10 of 18 PRED70 WRONG rows are APPLICATION or KNOB (§2.5).
- "Model choices that decided a label": 12 named, and "deviations flagged 22" (`PREDICTIONS70.md:107-122`;
  `tally.txt:76`).

**Choice of ingredient per domain:**
- "The author chose which CRR ingredient to apply per domain, and 28 rows were still WRONG"
  (`ontology/15_grammar_to_theory.md:64-67`).
- Prototype-stage estimator choices were made from prototype numbers: AGENT_LOG 32, and 50 ("the uncontrolled
  path-vs-endpoint fit let the path win (0.8319 vs 0.1038)"). The controlled check reversed it.

**Under-determination.** INTERNAL 22 rows: the theory gives two or more readings that disagree on the domain
(`ladder.txt:28`). These are the "v3.2 decision list" (`ontology/05_next_steps.md:23-47`), never decided (§3).

**Reading.** There is conceptual overfitting at the level of *translation choice*, in both directions. It is
consistent with a theory that under-determines its own operationalisations.

### 2.7 Recurring structures across otherwise failed tests

1. **H-L5's arc collapses onto amplitude on monotone 1-D occasions.**
   - "Every 'arc-regular' system in the batteries turned out arc-regular by the geometry of a monotone occasion, with the
     amplitude control equal to the arc" (`ontology/02_commitments.md:127-128`).
   - PRED70: 7/7 H-L5 ADDS rows fail the amplitude control (`tally.txt:81`).
   - Labs: "P1: the arc is the added size; H-L5's control can never be beaten" (`labs/CANDIDATES.md:56`).
   - *Category E (identifiability):* on such carriers H-L5 and its control are not separable.
2. **A bounded exponential memory shifts a stability threshold or a speed.**
   - Alternans gives (1 + q)/(1 − q) (`literature_check.txt:6-8`). The same shape recurs in Bass, SIR, OV traffic,
     Samuelson and Lotka-Volterra, and in PRED70's 7 A6 candidates (`PREDICTIONS70.md:59-69`).
   - It is known as the distributed-delay or weak-kernel effect (`literature_check.txt:42, 60`).
   - What it offers is a cross-domain mapping. FRONTIER calls this "teaching and translation, not resolution"
     (`labs/frontier/FRONTIER.md:88-92`).
3. **A3's antipode loses to domain triggers wherever the two differ.**
   - "In each the domain's own trigger ... sets the event, not half a turn of a phase" (`PREDICTIONS70.md:82-86`).
4. **A6 is wrong wherever a domain accumulates.** Bayesian evidence and Tolman cycles
   (`docs/notes/2026-09-17_synthesis_class.md:112-116`).

### 2.8 Salvage classification (L-RETRO)

- **C (reduction), dominant.**
  - REDUNDANT-IG 39 and REDUNDANT-DOMAIN 59 (`ladder.txt:28`).
  - 0 clean ADDS after the literature check.
  - SHARP claims re-graded to 0 of 15.
  - FRONTIER RESTATES 10 of 12 (`FRONTIER.md:32`).
- **A, at R4 only, on H-L5 and H-CUT as stated in CRR.md.**
  - Chain: H-L5 (`theory/CRR.md:200-209`) → the arc-vs-clock CV on the domains' own synthetic models → PRED70 →
    6 FALSIFIES and 7 control fails.
  - Highest level: the hypothesis as stated, but on synthetic models, not real systems.
- **B: APPLICATION and KNOB WRONG rows (10).**
  - Chain: A3/A6 (`theory/CRR.md:101-111, 144-153`) → a restart schedule, a ratchet rule, a q = 0.5 memory → WRONG.
  - Highest level: one translation.
- **E.** H-L5 against its amplitude control on monotone 1-D occasions; INTERNAL 22.
- **F (unresolved structure).**
  - L01 / F2a: G-CD3 OPEN; "the only place in these twelve fields where CRR makes a claim the field does not already
    make" (`FRONTIER.md:68-75` (section 4)). Never preregistered: "LIFE1 (real lineages) not yet preregistered" (`CLAUDE.md:325`).
    The investigator forecast FAIL (`FRONTIER.md:72-73`).
  - The 7 PRED70 A6 candidates, not literature-checked.
- **No G.**

### 2.9 Extinguished-lead check (L-RETRO)

1. **SHARP's retirement cuts both ways.**
   - The record treats the zero as "a fact about the grade, not about CRR" (`EPISTEMIC_REVIEW.md:143`).
   - Also legitimate: the 0-of-109 FLOW result *is* the core epistemic fact, since a framework that supplies no dynamics
     cannot predict unique numbers. ontology/15 says the same: "CRR fixes nothing" (`ontology/15_grammar_to_theory.md:98-105`).
   - Both readings should travel together. The retirement did not extinguish a lead. It relabelled an absence.
2. **The R2 reclassification.**
   - REDUNDANT-DOMAIN rows were moved from "nothing did [the work]" to "a real, if modest, success"
     (`EPISTEMIC_REVIEW.md:219-229`).
   - The correction is fair on the harness's facts (T-G "differ" on 59 of 59, `ladder.txt:29`).
   - Without a base rate it still licenses only coverage.
3. **Leads stalled but not killed:**
   - L01 (G-CD3 OPEN since 2026-09-26);
   - PRED70's A6 candidates (since 2026-09-29);
   - the expert protocol (0 experts named, `ladder.txt:397`).
4. **A lead the literature killed, not the protocol.**
   - L02, the grandmother term (synthesis row 8 PROPOSES), is FRONTIER F2b: "yes, and tested: it did not improve the
     E. coli fit" (`FRONTIER.md:20`).
   - It was killed by the literature, not by the protocol.

### 2.10 Answers to questions 1-9 (L-RETRO)

1. **Initial idea.** CRR as a synthesis lands where domains are known. Then: does CRR "add hidden structure" (prompt 60)?
2. **Operationalisation.** Graded battery rows; then SYNTHESIS with T-G, T-N and T-C at 1 %; then declared-blind batches;
   then PRED70.
3. **Added assumptions.** The 1 % tolerances; the choice of null per row; the choice of ingredient per domain; q = 0.5
   fixed (PRED70); bare H-L5 without its control (PRED70, an error).
4. **Which of them failed.** The bare H-L5 Q (7 ADDS fail the control); the q = 0.5 knob (4 KNOB WRONG); the 1 %
   tolerance on stochastic rows (ROB1 report).
5. **Reached the CRR claim.** H-L5 and H-CUT as stated, at R4 on synthetic models (6 FALSIFIES + 7). A6 as an
   unrestricted rule (accumulating domains).
6. **Reached only a translation.** APPLICATION 6, KNOB 4; the INTERNAL rows.
7. **Interesting despite failing.** The memory-threshold lemma family as a cross-domain mapping; L01; the 7 A6
   candidates.
8. **Successes reduced to known mathematics.** All 10 ADDS; the 15 external SHARP claims; REDUNDANT-DOMAIN 59 by
   construction.
9. **Infrastructure, identifiability or resolution.** Batch 32 row 2 (the estimator forced the pass); the ROB1 tolerance
   artefact; H-L5's control identity on monotone carriers.

### 2.11 Question-10 evidence (L-RETRO)

- **The bank was the exploratory environment, and it was large.** 197 battery rows, 164 synthesis rows, 70 PRED70 rows,
  10 ROB1 rows (`ladder.txt:15, 28`; `tally.txt:76`; `tally_4b.txt`). It ran without R2/R3: rows were prototyped and
  repaired after first runs (AGENT_LOG 30-54).
- **Its exploration was aimed at grading coverage ("does CRR agree with X?"), not at developing a better model.** No
  bank output produced a revised CRR rule, and `theory/CRR.md` stayed at v3.1.
- **The route from bank to confirmation was narrow but open.**
  - The labs entry rule requires H1 ≠ H0 on a synthetic gate (`labs/README.md`, "The entry rule").
  - L03 ran within a day (CARD).
  - L01, with an open gate, waited for "a loader VOID rule and an owner decision on the D2 risk"
    (`labs/CANDIDATES.md:82`). D3 work is excluded by the owner's no-spend constraint (AGENT_LOG 163).
- **The literature check came after declaration.** It dissolved ADDS within a day (prompt 132, AGENT_LOG 110).
  ontology/15 drew the lesson: "Check the literature before declaring anything, not after" (`ontology/15_grammar_to_theory.md:162-163`).

### 2.12 Open questions for Phoenix (L-RETRO)

- **May explore.**
  - Run the literature check of PRED70's 7 A6 candidates.
  - L01 (an H-CUT antipode against the initiation adder) on Witz et al. 2019, under a VOID-capable loader.
  - A *base rate* for the synthesis hit rate: a decoy framework with the same ingredients over the same rows.
  - Use the bank as a translation atlas: mappings between fields.
- **Must never claim.**
  - That the 0.7113 hit rate is predictive evidence.
  - That any ADDS row is novel.
  - That REDUNDANT means "CRR was right" (15 PRED70 redundant rows failed Q).
  - That the retrodictive and ledger denominators can be pooled.

---

## 3. L-ONT: the ontology and its link to the empirical programme

### 3.1 Trajectory

| when | event | source |
|---|---|---|
| 2026-09-15 | CRR.md v3.1, owner-approved: A8 amended "no forecast" → "no certainty"; H-T1 tightened | `theory/CRR.md:319-327` |
| 2026-09-17 | Last commit to `theory/CRR.md` (status lines only) | commit 455780b |
| 2026-09-17 | Last commit to `src/crr/instrument/core.py` | commit 33faec5 |
| 2026-09-21/22 | ontology 01-08: "the cut, as computed, needs the future"; six commitments sorted; next steps (causal instrument, v3.2 list) | `ontology/README.md:3`; `ontology/01_the_cut.md`; `ontology/05_next_steps.md` |
| 2026-09-22 | Epistemic status note | `docs/notes/2026-09-22_epistemic_status.md` |
| 2026-09-22/23 | 09-13: FEP, tense test, self-model, off switch (synthetic) | `ontology/README.md:23-31`; AGENT_LOG 72-74 |
| 2026-09-24 | 14 (Smolin, Rovelli, Gough); 15 (grammar to theory; route 1 = RLAW) | AGENT_LOG 108, 112 |

### 3.2 The commitments and whether the empirical programme tested them

This uses the ontology's own sorting (`ontology/02_commitments.md:143-156`).

| commitment | CRR.md lines | testable form | tested on held-out data? | result |
|---|---|---|---|---|
| C1 distinguishability (A1) | 50-53 | none: "a theorem" (`ontology/02_commitments.md:23-25`) | n/a | REDUNDANT-IG rows agree by Čencov |
| C2 own unit (A1′, D1) | 55-74 | which estimator | only as a sensitivity factor (RLAW own:on/off) | "a family of estimators until a rule picks one" (`ontology/02_commitments.md:40-41`); RLAW: "The own unit does not rescue any domain row" (`reports/rlaw.md:122`) |
| C3 occasioned time (A3, H-CUT) | 101-131 | H-CUT | **no ledger row tests H-CUT** (auditor's search of `ledger/LEDGER.md` for H-CUT: only CARD-3, a "DIAGNOSTIC ONLY" row, `LEDGER.md:174`) | synthetic only: PRED70 WRONG 6 on A3/H-CUT; G-CD3 OPEN, never run |
| C4 empty future (A7, A8) | 291-302 | an operational demand on the instrument | no | the instrument violates it: "every antipodal cut in every H-L5 row of this repository was located with samples after the cut" (`ontology/01_the_cut.md:32-33`); tense test synthetic (`ontology/11`) |
| C5 re-weighting (A6, P2, P3) | 144-164 | domain by domain | no held-out test (RLAW tested O1/P4, not A6) | "false where the domain accumulates" (`ontology/02_commitments.md:151`) |
| C6 own clock (H-L5, H-T1, H-EQ, H-CUT) | 196-250, 166-192 | comparative hypotheses | **yes**, for H-L5, H-T1 and H-EQ | H-L5: MEAS2-1/2 FAIL, CARD-1/2 FAIL. H-T1: T1X2-1 FAIL on 5/5. H-EQ: EQX-1 "reduces to a constant"; EQ2-1b PASS-0, fragile (ladder.txt rows) |

**The answer.** The only ontological commitment the empirical programme put to held-out test is C6. The rest stayed
synthetic or retrodictive:
- C3, the antipodal cut, CRR's most distinctive axiom, never had a confirmatory test;
- C4 was found to be violated by the instrument, which is an instrument fact.

ontology/15 names "A3, A6, A7/A8, H-L5 and H-EQ" as the Lakatosian hard core (`ontology/15_grammar_to_theory.md:37`). Of these, only H-L5
and H-EQ reached held-out tests.

### 3.3 The prerequisites the ontology set, and what happened to them

1. **The causal instrument.** "Implement a second intrinsic phase ... that uses no future sample: a Poincaré section
   ..." and "Add `gate_TENSE`" (`ontology/05_next_steps.md:6-19`).
   - Not done. `core.py` has only the analytic-signal `intrinsic_phase` (`core.py:89`). Its docstring mentions the
     Poincaré section as an option a prereg may name (`core.py:91`). There is no gate_TENSE in `runs/phaseA/`
     (directory listing).
2. **The v3.2 decision list** (`ontology/05_next_steps.md:23-47`).
   - None decided. `theory/CRR.md` has had no commit since 2026-09-17.
3. **A documentary discrepancy (auditor's finding).**
   - CLAUDE.md:442 and `ontology/01_the_cut.md:55` say that `theory/CRR.md` names a Poincaré section as the alternative
     intrinsic phase.
   - `grep -i poincar theory/CRR.md` returns nothing, and CRR.md v3.1 (read in full, 327 lines) contains no such text.
   - The alternative is named in CLAUDE.md and `core.py:91`, not in CRR.md.
4. **The demonstration that a causal repair exists.**
   - "The Poincaré section ... places the cuts within 1 sample of the registered ones with no future at all"
     (`ontology/01_the_cut.md:55-56`).
   - With the future removed the section's phase change is 0.0000 at every lag (`ontology/checks/cut_on_a_machine.txt:29`).
   - The analytic phase changes by 0.1600 half-turns one sample before (`:25`).

### 3.4 Four-layer table (ontology)

| # | observed phenomenon | CRR interpretation | ordinary explanation | distinguishing evidence |
|---|---|---|---|---|
| O-a | The registered cut needs about two half-turns of future (`ontology/01_the_cut.md:38-53`) | "the cut, the very thing the theory says is empty, is computed from the future and carries a measurable content" (`ontology/README.md:45-47`): a tension for A3/A7 | the Hilbert transform is non-causal (`ontology/01_the_cut.md:26-28`): an instrument property, as the Poincaré result shows | re-run the gates and the H-L5 rows under a causal section (the plan of `ontology/05_next_steps.md:18-19`); never done |
| O-b | A6 is wrong in accumulating domains (synthesis rows 3 and 9) | a scope restriction ("a system that re-counts its past stops cutting", `CRR.md:152-153`) | Bayesian evidence and Tolman cycles genuinely accumulate | a pre-declared scope clause (`synthesis_class.md:160`); a v3.2 decision, never made |
| O-c | CRR "fixes nothing": β, q, ρ and κ are free (`ontology/15_grammar_to_theory.md:98-105`) | a grammar or framework theory | the shared mathematics is information geometry plus MaxEnt (`ontology/15_grammar_to_theory.md:41-47`) | a fixed constant that is CRR-only and confirmed (route 1 failed: RLAW) |

### 3.5 Salvage classification (L-ONT)

- **D (instrument), for the tense finding.** It bears on the instrument's compliance with A7/A8, not on A8 as ontology.
  The ontology says so: "Not as ontology. As an operational demand on an instrument, yes" (`ontology/02_commitments.md:83-84`).
- **E (identifiability) for C1-C2, as the ontology itself states:**
  - C1 is a theorem (`ontology/02_commitments.md:23-25`);
  - C2 is "a family of estimators until a rule picks one" (`ontology/02_commitments.md:40-41`).
- **A, at hypothesis level, for C6 (ledger FAILs).** Those belong to the lineages L-L5, L-T1 and L-EQ. They are not
  re-assessed here.
- **F, for C3.** A3/H-CUT was never confirmatorily tested. G-CD3 OPEN is the one standing route.

### 3.6 Extinguished-lead check (L-ONT)

- **No ontological commitment was killed by a held-out test that it alone entailed.**
- **The risk runs the other way.**
  - Confirmatory studies ran on frozen v3 and v3.1 operationalisations while the ontology's own audit had flagged them as
    under-determined (22 INTERNAL rows) and the instrument as acausal.
  - Example: CARD's prereg was hashed 2026-09-15 and run 2026-09-27 (`ledger/LEDGER.md:174`), after the ontology's
    finding of 2026-09-21. That is in keeping with frozen-copy semantics (CLAUDE.md §2).
  - Consequence: failures in that period reach the frozen operationalisation. Whether the causal or own-event reading
    would differ was never checked.

### 3.7 Answers to questions 1-9 (L-ONT)

1. **Initial idea.** CRR as a process ontology: occasions, an empty cut, a regenerating past, an empty future.
2. **Operationalisation.** A1′ as `unit_sigma`; A3 as `antipodal_cuts` on the analytic phase; A6 as a Fréchet mean
   with P3 weights.
3. **Added assumptions.** The analytic-signal phase (non-causal); the Savitzky-Golay centred detrender
   (`ontology/01_the_cut.md:29-31`).
4. **Which of them failed.** The causal reading of the cut (O-a); A6 without a scope clause.
5. **Reached the CRR claim.** H-L5 and H-T1 at held-out level (other lineages).
6. **Reached only an implementation.** The tense violation (instrument).
7. **Interesting despite failing.** The Poincaré section as a causal cut that agrees with the registered one within
   1 sample.
8. **Reduced to known.** C1 is Čencov. P3 weights are the exponential kernel each field rediscovered (`ontology/15_grammar_to_theory.md:46-53`).
9. **Instrument.** The acausal phase and detrender.

### 3.8 Question-10 evidence (L-ONT)

- **Development was not blocked by R2/R3. It was not carried out.**
  - The ontology wrote a precise exploratory programme on 2026-09-21/22: a causal instrument, the v3.2 decisions,
    gate_TENSE (`ontology/05`).
  - Eleven days later none of it is implemented (§3.3).
  - In the same period the repository ran the RLAW, SCL, SOTA1, CARD and SEC3-SEC6R studies (CLAUDE.md §0).
- **One structural factor.** CRR.md changes need the owner: v3.1 was "owner-approved, issue #13" (`CRR.md:321`), and
  AGENT_LOG 9 records "change nothing in CRR.md" for an external spec.
- **Reading.** The programme kept producing operationalisations of a theory text it never revised. That is a direction
  and workflow choice. The confirmatory rules did not force it.

### 3.9 Open questions for Phoenix (L-ONT)

- **May explore.**
  - Decide v3.2 before any new confirmatory work: which phase; which A3 reading on projective carriers; A6's scope
    clause; which Ω.
  - Implement the causal section and gate_TENSE.
  - Re-read H-L5 rows under it, explicitly as exploration.
- **Must never claim.**
  - That the ontology has been tested beyond C6.
  - That the tense finding refutes A8 as ontology.
  - That contemplative kinships are evidence (`ontology/02_commitments.md:140-141`: "kinships of picture, not of doctrine").

---

## 4. L-APP: applied and compute work

### 4.1 Trajectory

| when | event | source |
|---|---|---|
| 2026-09-23 | Alexander Plan, with §11 adding the EPO application in money terms; addenda §11.6-11.7 the same day | `Alexander Plan/ALEXANDER_PLAN.md:547-793` |
| 2026-09-25 | Compute_Savings (prompt 196); scale estimate (198); Energy Design Principle (199) | AGENT_LOG 143-145 |
| 2026-09-28/29 | GLOBAL_ESTIMATE (prompt 228); "Re-pinned 2026-09-29 on SEC4's evidence" | `Compute_Savings/GLOBAL_ESTIMATE.md:1-15` |
| 2026-09-30 | SEC5-1 FAIL; SEC4-1-G post hoc gate CLOSED; addenda to four notes | AGENT_LOG 236, 239 |
| 2026-09-30 | APP1 (applications); ROB1 stages 1-4b | AGENT_LOG 212-234 |
| 2026-10-02 | P7 suite: 17 rows | AGENT_LOG 246, 247; `Applied_Suite/checks/suite.txt` |

### 4.2 Results (verbatim)

- **The suite's verdict on CRR's part.** "CRR's part over the 17 rows: CRR-proper but not load-bearing 4 (CL2, CL3,
  CL4, CL5); none 2 (CL1, RB1); not decided by a pinned source 11 (AS1, AS2, AS3, AS4, RB2, RB3, TS1, TS2, TS3, TS4,
  TS5)" (`suite.txt:889`). No row reads "CRR-proper and load-bearing".
- **CL1 (SEC):**
  - GRADE RESULT, resting on SEC4-1 (`suite.txt:76-78`);
  - "SENSITIVITY ... CLOSED if SEC4-1-G is read as decisive" (`:79`);
  - CRR's part is "none (the pinned trace counts 0 CRR-proper operations in the mechanism ...)" (`:191`), from
    "CRR-proper operations performed in SEC's code path: 0 of 7 operational clauses" (`:192`).
- **Forecasts:** "1 HOLDS, 2 HOLDS, 3 FAILS, 4 HOLDS, 5 HOLDS (forecast 5 under the literal reading of (c): FAILS)"
  (`suite.txt`, forecasts block).
- **Compute_Savings:**
  - "SEC, no tuning | 0.0588 (a saving of 0.9412) | 9/10" (`COMPUTE_SAVINGS.md`, table);
  - addendum: "'not behind the tuned λ' is a weak mark of success" (`COMPUTE_SAVINGS.md:138`).
- **GLOBAL_ESTIMATE addendum:** "the figures above are an arithmetic on an unsupported premise, not an estimate of a
  saving" (`GLOBAL_ESTIMATE.md:132-133`).
- **Energy:**
  - "No energy saving here is attributable to CRR. The lens sorts known mechanisms" (`RETRODICTION.md:139`);
  - the own-clock cut "reduces to Wald's sequential test and does not beat the confidence rule" (`Energy Design
    Principle/README.md`, "Where it stands");
  - **but** CONSOLIDATED says "About 1.5 % of that (0.47 TWh) is attributable to the CRR programme, all of it through
    SEC" (`Energy Design Principle/CONSOLIDATED.md:83`).
  - The note was last committed 2026-09-25 (9e9b5be). A grep of the folder's .md files finds no addendum and no mention
    of SEC4-1-G or the frozen learner's 24/30 (auditor's search). AGENT_LOG 239 added premise addenda to four other notes
    but not to this one.
- **ROB1:**
  - stage 3: "C-R1: REDUNDANT ... C-R2: REDUNDANT ... C-R3: REDUNDANT" (`Robotics/checks/grade_s3.txt:199-201`);
  - stage 4b: "ADDS 0, PROPOSES 0, REDUNDANT-IG 0, REDUNDANT-DOMAIN 6, WRONG 2, INTERNAL 1, UNSTATED 1"
    (`tally_4b.txt`, outcomes line);
  - overall forecast "FAILS (failed: F1)";
  - reading: "DISAGREES (candidate) 3 ... RESTATES 9 ... SILENT 13" (`reading_tally.txt`).
- **Alexander Plan:** "No continual-learning row is PASS-1" (`ALEXANDER_PLAN.md:164`, written before SEC4). Its value
  figures are, by its own addendum, "a ceiling on a scenario the evidence does not support, not as a forecast"
  (`:771`). The rupture-detector use case: "the repository offers no evidence of a technical effect for that use"
  (§11.6). There is no SEC4/SEC5 addendum in the file (auditor's grep for "SEC4": none).

### 4.3 Four-layer table (applied)

| # | observed phenomenon | CRR interpretation | ordinary explanation | distinguishing evidence |
|---|---|---|---|---|
| P-a | One SEC configuration matched the tuned λ on 9/10 SCL3 carriers at 0.0588 of the sweep's compute | "SEC is a product of this repository's CRR programme ... CRR's role was the path to it, not its equations" (`COMPUTE_SAVINGS.md:10-17`) | SEC = Laplace + a secant units calibration + AR1's clip (SPA1 "KNOWN"); 0 CRR-proper operations (`suite.txt:192`); the frozen learner is not behind on 24/30 (`GLOBAL_ESTIMATE.md:122`) | a criterion that can fail (an open instrument gate) on unseen data. SCL3-3-G reads OPEN (7/10, need 8) and SCL3-3 stands (`COMPUTE_SAVINGS.md:129-131`) |
| P-b | The pause is bit-for-bit lossless on real stacks (AS1 CONSTRUCTION) | the empty cut (A3) / Proposition 7 | standard checkpoint-resume determinism. "Nothing here tests CRR." (`Empty_Cut_Engineering/DECLARATION.md:153`) | a world where own-clock keying changes an outcome standard practice would not (lineage L-PAUSE) |
| P-c | The robotics reading found 3 DISAGREES candidates | CRR points at open bottlenecks | all three are published (C-R1..3 REDUNDANT) | — (dissolved by prior art) |

### 4.4 Salvage classification (L-APP)

- **C (reduction) dominant.** SEC is known (SPA1); the clock cut is Wald; ROB1's candidates are published.
- **E/D (criterion weakness) on SEC's saving premise.** This belongs to L-SEC: the "not behind tuned λ" criterion is met
  by a frozen learner.
- **F.** The SCL3-3 PASS-0 stands with an open gate (narrow: 7/10 against a need of 8). A tuning-cost saving is a real
  engineering question, unattributed to CRR.
- **No G.**

### 4.5 Extinguished-lead check (L-APP)

None was killed too early. The opposite risk is documented:
- Applied valuations outran the evidence. GLOBAL_ESTIMATE was re-pinned on SEC4-1 on 2026-09-29; SEC5-1 FAILed and
  SEC4-1-G closed on 2026-09-30.
- Then came addenda: premise "not currently support[ed]" (`GLOBAL_ESTIMATE.md:130-133`).
- Energy CONSOLIDATED still carries the attribution without an addendum (§4.2).

### 4.6 Answers to questions 1-9 (L-APP)

1. **Initial idea.** CRR as a source of compute and energy savings, safe-pause applications, and robotics guidance.
2. **Operationalisation.** Configurations counted; scenario models; APP1 grades; suite rules.
3. **Added assumptions.**
   - "one SEC configuration replaces the 17-point sweep without loss" (`GLOBAL_ESTIMATE.md:129-130`);
   - adoption probabilities ("cl_patent's assumption", `CONSOLIDATED.md:84`).
4. **Which failed.** The "without loss" premise (SEC5-1, SEC4-1-G, 24/30).
5. **Reached the CRR claim.** None. There is no CRR-proper load-bearing row.
6. **Reached only an implementation.** n/a.
7. **Interesting.** The tuning-free calibration as engineering (L-SEC); the pause as an engineering construction
   (L-PAUSE).
8. **Reduced to known.** SEC (Laplace + AR1 clip); the pause (checkpoint/resume); the clock cut (Wald); the ROB1
   candidates.
9. **Infrastructure.** The SEC criterion's identifiability (L-SEC).

### 4.7 Question-10 evidence (L-APP)

Here the record shows over-extension, not suppression. Monetary and energy extrapolations (`ALEXANDER_PLAN.md:70`;
`GLOBAL_ESTIMATE.md`, the "short answer" table) were produced from PASS-0 and single-family PASS-1 results before any
replication, and then had to be qualified by addenda.

### 4.8 Open questions for Phoenix (L-APP)

- **May explore.** A tuning-cost study with a criterion that can fail, framed as engineering, not as CRR.
- **Must never claim.**
  - That any applied saving is attributable to CRR. The Energy CONSOLIDATED attribution needs the same premise addendum
    as GLOBAL_ESTIMATE.
  - That the pause is a CRR result.
  - The Alexander Plan's dollar figures as forecasts.

---

## 5. Note on stale snapshots (for the verifier)

Several notes quote counts that later changed. Each is dated and correct for its own date:
- `EPISTEMIC_REVIEW.md:31-35`: 146 rows, 56 of 80. Current: 164 rows, 69 of 97 (`ladder.txt:28, 41`).
- `docs/notes/2026-09-22_epistemic_status.md:9-21`: two held-out PASS-0, "Anchoring is push-timestamp only".
- `ALEXANDER_PLAN.md:164`: "No continual-learning row is PASS-1".

Phoenix should quote `ladder.txt` (current) and the ledger, never these snapshots.
