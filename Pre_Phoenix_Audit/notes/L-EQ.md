# L-EQ — Ω = 1, H-EQ, the equanimity rule, and its Bayes / Kalman / Cramér–Rao connections (with SOTA1)

PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED. Reader's notes for lineage L-EQ (`Pre_Phoenix_Audit/DECLARATION.md`,
prompt-log entry 260). This is an interpretive note, not evidence (R8). Every verdict is quoted from `ledger/LEDGER.md` by row id;
every number is copied from the cited file. Counts the auditor made are marked **auditor's count (derived)**, with the method.
Citations of the form `file:N` give line numbers as the files stood when this note was written (HEAD of the working tree,
2026-10-02).

---

## 0. One-paragraph summary

Equanimity entered the record as a gradient-norm ratio, w = Ω·‖ḡ_present‖/‖ḡ_past‖ with Ω = 1 (`theory/CRR.md:166-177`). As
H-EQ is stated (replay, against ER-sum and the best fixed w), it met a direct, fair-by-its-own-terms test and lost: it REDUCES to
a fixed replay weight and is behind it (EQX-1, EQX-3). The value Ω = 1 was never singled out on data (EQX-2, EQ2-6, EQ3-6;
BAYES1-B6 has the best Ω below 1 on every carrier). The mathematics accounts for both results (`theory/checks/omega_sweeps.txt` [1]-[2],
`theory/checks/cramer_rao_reading.txt` [CR6], `Continuous_Learning/checks/pareto_identities.txt` [1]-[4]). At Ω = 1, any rule that
equalises pull magnitudes is stationary on the whole Pareto front, so it selects no trade-off point. That result is published
for the MGDA family. Outside H-EQ's stated domain, the rule run as a normalised penalty step on online EWC showed a repeatable
but weak non-inferiority against an in-sample-tuned λ:
- EQ2-1 "**PASS, FRAGILE**", relabelled EQ2-1b "**PASS-0 (provisional)**";
- EQ3-1 "**FAIL**" (5/6);
- EQ4-1r "**FAIL**" (4/6).

That effect is cap-dependent, needs SGD, reduces to prior art (VQGAN's adaptive weight, GradNorm α = 0, MGDA / Nash-MTL), and
lives largely on one underlying digit set. On the real image benchmark, strongly anchored, equanimity as a distillation weight
lost to a published constant (SOTA1-2 "**FAIL**"), through a "stalemate" mechanism that is the knife edge the mathematics
predicts (`CL Design Principle/FINDINGS.md:28`).

The places where a "1" arises *naturally* are all standard mathematics:
- the Bayes count weight (`omega_sweeps.txt:6`);
- the Laplace weight 1 in correct Cramér–Rao units (`cramer_rao_reading.txt:43`);
- the Kalman gain K(1) = 1/φ at Fisher speed v = 1 (`omega_sweeps.txt:80`).

The productive descendant of this lineage (unit calibration of the Laplace weight, SEC) is not a CRR rule (L-SEC; P1's F11).
**No G.** The strongest negative evidence reaches **the hypothesis as stated in CRR.md** (H-EQ, replay) and the claim that
Ω = 1 is a distinguished value. It also reaches the "equal pull *magnitude*" reading of equanimity, analytically and in any
norm. It does **not** reach the rival reading the record itself flagged (equal *precision*, the external spec's A9) and
never adopted or tested as such. Nor does it reach equanimity-as-valuation (zero stake at the cut; that is L-PAUSE).

---

## 1. Trajectory (dated, cited)

| date (UTC) | event | source |
|---|---|---|
| ≤ 2026-09-14 | Archive bundle (seen MNIST-family data) used the Ω rule on replay. Recomputed rows: ARC-EQ-LAND "as claimed (seen); Ω relabels the effective replay weight (median w at Ω=1 ≈ 0.7–2.2)"; ARC-A1 "FRAGILE at boundary — not a PASS"; ARC-A2 "PASS (seen)"; ARC-A3 "PASS (seen), one cell inside seed noise"; ARC-METRIC "immaterial (seen)"; ARC-COMPUTE "FAIL on Fashion; where it holds, fixed w = 1 holds too"; ARC-T3 "FAIL (seen)"; ARC-T2 "FAIL as pre-registered"; ARC-EQ-Q1..Q4 "VOID (design changed after prereg)" | ledger ARC-* (LEDGER.md:10-20) |
| 2026-09-15 17:50:15 | Repository imported (commit 02d4292) | `git log` |
| 2026-09-15 18:14:48 | EQX pre-registered (231f75b), 24 min after import: the reduction test CLAUDE.md §6 mandates, with the estimator frozen from the archive | `git log`; `reports/eqx.md:24-31` |
| 2026-09-15 | EQX scored: EQX-1 "REDUCES", EQX-2/3 "FAIL", EQX-4 "Euclidean ratio beats the Fisher ratio". CRR.md's status line: "H-EQ is retired as an adaptive rule" | LEDGER.md:22-26; `theory/CRR.md:178-183` |
| 2026-09-16 | Exploratory "playground" outside the repo (owner-permitted) suggests the rule helps EWC-type penalties and harms distillation constraints. No playground number is quoted | AGENT_LOG 3 |
| 2026-09-16 23:10:55 | gate_EQ2, attempt 1 (convex positive control) CLOSED, "R12 stop" | `git log` dbef54f; AGENT_LOG 4 |
| 2026-09-17 00:04:02 | Attempt 2, with a nonconvex S-Y positive control, opens gate_EQ2 | `git log` 4f1c0f2; AGENT_LOG 4 |
| 2026-09-17 00:10:49 | EQ2 pre-registered (4ba6035). Data opened 00:11Z | `git log`; AGENT_LOG 25 |
| 2026-09-17 00:34 | SPEC_RECONCILIATION §4: "two 'equanimity' laws under one name"; "Before any further EQ prereg the owner must decide which law carries the name" | `theory/SPEC_RECONCILIATION.md:67-80`; `git log` 89de971 |
| 2026-09-17 | EQ2 scored (EQ2-0..8, EQ2-S). CRR.md H-EQ status amended | LEDGER.md:31-40; `theory/CRR.md:184-192` |
| 2026-09-18 | EQ2-1 relabelled EQ2-1b "PASS-0 (provisional)" under the new PASS levels | LEDGER.md:42 |
| 2026-09-17 → 09-21 | EQ2R held to the next calendar day under R3. The session was down when the trigger fired. On resuming, the frozen scorer crashed at the first DER++ arm: EQ2R-VOID, CC-VOID, three carriers now SEEN | AGENT_LOG 25, 26, 40; LEDGER.md:43-44 |
| 2026-09-22 00:59:34 | Owner: sweeps of Ω = 1 on existing mathematics ("I hear there is a threshold either side of 1, but 1 is also bayes optimum"), Kalman tuned vs fixed, then full CL tests | PROMPT_LOG 69 |
| 2026-09-22 01:14:35 | `theory/checks/omega_sweeps.py` committed: Bayes, knife edge, plateau, Kalman | `git log` 62a9512; AGENT_LOG 58 |
| 2026-09-22 01:21:32 | EQ3 pre-registered (daf50e7), 22 min after the prompt. Data fetched 01:23Z | `git log`; LEDGER.md:45 |
| 2026-09-22 | EQ3 scored: EQ3-1 "FAIL" (fars); EQ3-3, EQ3-4 "VIOLATED"; EQ3-6 "FAIL" (plateau); EQ3-I "PASS-0"; EQ2-1c records the failed replication | LEDGER.md:45-61; AGENT_LOG 60 |
| 2026-09-22 | Cross-verification against the literature: GradNorm α = 0 / MGDA; scale not shape | `Continuous_Learning/CROSS_VERIFICATION.md:331-367`; AGENT_LOG 62 |
| 2026-09-22 04:59:33 → 05:39:00 | Owner asks to reprocess the mathematics. `omega_reprocessed.py` written; EQ-B designed (median → window-max iteration on the surrogate; dev run on six SEEN EQ3 carriers); EQ4 pre-registered (a55be4d), about 40 min after the prompt | PROMPT_LOG 74; AGENT_LOG 63; `git log` |
| 2026-09-22 15:52 | BAYES-1 pre-registered (49072aa, 15:52:37Z); data fetched 15:52:56Z | LEDGER.md:62 |
| 2026-09-22 | BAYES-1 scored: B0 "NOT DECIDABLE"; B1-B3 without verdict | LEDGER.md:62-71; AGENT_LOG 67 |
| 2026-09-22 | FED Phase-A gate CLOSED twice ("one global weight is never a step behind"; "the clip does the work") | AGENT_LOG 71; `docs/notes/2026-09-22_fed_phaseA.md` |
| 2026-09-23 04:45:13 | EQ4 data step (R3 hold). EQ4-1 "FAIL"; EQ4-3 "FAIL"; EQ4-4 "INERT"; EQ4-5 "VIOLATED"; EQ4-S "FRAGILE"; EQ4-I "PASS (PASS-0 at most …)" | LEDGER.md:73-86; AGENT_LOG 82 |
| 2026-09-23 | Adam / prior-art checks: under Adam the rule is unnecessary; unsmoothed it is VQGAN's weight; it is behind a finely tuned constant (R4). "EQ5" declined | `Continuous_Learning/ADAM_AND_PRIOR_ART.md:24-50`; AGENT_LOG 85 |
| 2026-09-23 | Adam_SGD assumption audit and drift batteries: the unsmoothed rule beats every fixed constant in drifting-units worlds, post hoc and FRAGILE in Ω; it loses on accumulating tasks; the noise-ratio mechanism is "not confirmed as declared" | `Adam_SGD/ADAM_SGD.md`; AGENT_LOG 90, 93, 94 |
| 2026-09-23 | "Let Ω grow" refuted analytically (any Ω > 1 slides to the old optimum). A coherent CRR-proper alternative (per-task normalisation + P3 age weights) is named, not run | AGENT_LOG 95; `Adam_SGD/ADAM_SGD.md:152-176` |
| 2026-09-23 → | The lineage hands off to SEC (SEC1 on the 12 SEEN EQ3+EQ4 carriers; SEC1-R reports the rule) | AGENT_LOG 96, 143; LEDGER.md:94-103 |
| 2026-09-23/24 | SCL1/SCL2 use the Ω rule as the learner inside the pause harness (construction rows; SCL1-E/SCL2-E "equanimity clock" TIE) | LEDGER.md:104-128 |
| 2026-09-24 | RW2 Phase A round 2: the rule freezes the learner on anchors that start at zero ("ill-posed for anchors that start at the reference") | AGENT_LOG 126, 127; `Continuous_Learning/CONTINUOUS_LEARNING.md:445` |
| 2026-09-24 | RLAW: "is not H-EQ (equal pull only at v = 1/sqrt 2, M7), so O1's 'at Omega = 1' is dropped" | AGENT_LOG 113 |
| 2026-09-25 | Pareto literature check: the rule's direction is MGDA on normalised gradients / IMTL-G / Nash-MTL; MEGA-II takes the bisector. Results vs published benchmarks: ER is ahead of the rule 15/15 | CL doc addenda (`CONTINUOUS_LEARNING.md:469-512`); AGENT_LOG 130, 131 |
| 2026-09-25 | Cramér–Rao reading: "It gives H-EQ's Ω = 1 no meaning (CR6)"; weight 1 is correct "exactly when the unit is correct" (CR5) | `docs/notes/2026-09-25_cramer_rao_reading.md:77-95,121` |
| 2026-09-25 05:27:48 → 11:51:16 | SOTA1: owner prompt, then declaration (05:50:35), Phase A gate, prereg (de95c63), strongly anchored (OTS) | PROMPT_LOG 190; `git log`; AGENT_LOG 138-142 |
| 2026-09-26 | SOTA1 scored: SOTA1-1a/1b "FAIL"; SOTA1-2 "FAIL"; SOTA1-3: one "PASS-0" (label replay), six "FAIL"; SOTA1-ND "NOT DECIDABLE". Post hoc diagnostics: dose-response and stalemate | LEDGER.md:152-170; AGENT_LOG 155, 156; `CL Design Principle/FINDINGS.md:27-29` |

---

## 2. Operationalisations and added assumptions

**Core principle as stated** (`theory/CRR.md:166-177`). "When a learner updates from a present batch and a replayed past batch,
weight the past gradient so that settled past and present exert equal pull in the Fisher norm", with
w = Ω·‖ḡ_present‖_F/‖ḡ_past‖_F, Ω = 1. The test: "It counts as a result only if it beats experience replay with the two losses
summed … and the best fixed w". *Must fail on:* a convex learner. The summary row reads "fails if ties either" (`CRR.md:313`).

**Rival statements of "equanimity" in the record:**
- **The external spec** (issue-#21 text A9; spec [P7]/[H1]). Ω = 1 is the temperature of the occasion weights (surplus slope
  λ = 1), "stated as equal precision — never as a ratio of pull magnitudes" (`theory/SPEC_RECONCILIATION.md:69-71`;
  `theory/external/CRR_test_specification_GPT6_Astra_2026-09-16.md:63-68, 471-492`). The retrodiction battery grades the pair
  TENSION (`theory/retrodictions/crr_retrodictions.txt:138-146`).
- **CRR.md's dangling reference.** `CRR.md:190` cites "A9", which is not defined in CRR.md (auditor's search of `theory/CRR.md`);
  it exists only in the issue text.
- **The two readings on the Kalman filter.** "Fisher speed 1" gives K = 1/φ; "equal pull / equal precision" gives K = 1/2
  (`theory/retrodictions/synthesis_batches/batch_02.txt:50-61`, OUTCOME "INTERNAL"; `batch_06.txt:38-47`).
- **Equanimity-as-valuation.** Zero stake at the cut, the natural-time agent (AGENT_LOG 138 separates the two). That reading
  belongs to L-PAUSE and is not audited here.

**Operationalisations tried:**

| op | past term | comparator | where |
|---|---|---|---|
| O1 ratio rule, Fisher norm, EMA 0.9 | replay batch | ER-sum, fixed w grid | EQX |
| O1′ ratio rule, Euclidean norm, EMA 0.9, cap 1e4, floor 1e-12 | online-EWC Fisher penalty (also DER++, LwF, SI, MAS as controls) | in-sample-tuned λ on a √2-refined grid | EQ2, EQ3, EQ4 (rule arm), SEC1-R, SCL3, SEC3 |
| O2 EQ-B (present gradient clipped at κ × the window maximum, then the ratio) | online EWC, clean and poisoned | tuned λ; fixed+clip | EQ4 |
| O3 ratio rule against the exact posterior | exact Laplace penalty on a Bayesian linear readout | the exact sequential posterior | BAYES1 |
| O4 ratio rule as KD weight (cap 10); "H-EQ at the head" = cosine head | MKD slow-model distillation | MKD's published λ = 5.5; leave-one-out ablation | SOTA1-2, SOTA1-3:crr-cos |
| O5 the rule applied to the Kalman update | prior vs innovation | tuned Riccati gain | `omega_sweeps.txt:78-107` |
| O6 unsmoothed rule (= VQGAN ratio) in drifting-units worlds; under SGD / momentum / Adam / decoupled Adam | synthetic quadratics | finely tuned constant; oracle | `Adam_SGD/`, `Continuous_Learning/checks/adam_checks*.txt` (R4) |
| O7 rule as the weight on heterogeneous nodes | shared-anchor Fisher | one global knob | FED gate (CLOSED) |

**Assumptions added to make H-EQ testable** (each with where it entered):
1. **EMA smoothing 0.9 of gradient vectors, frozen at the archive's value.** CLAUDE.md §6 "Estimator frozen at hash time:
   ratio=ema, smooth=0.9, Fisher metric". It was carried unchanged through EQX → SOTA1 (`prereg/eq2/PREREG.md:74-76`;
   `prereg/sota1/PREREG.md:68`).
2. **A ratio cap** (1e4 in EQ2-EQ4 and BAYES1; 10 in SOTA1) and a denominator floor 1e-12 (`prereg/eq2/PREREG.md:75-76`;
   `prereg/sota1/PREREG.md:68`).
3. **Euclidean in place of the Fisher norm from EQ2 on.** "EMA of the gradient **vectors**, smooth = 0.9, Euclidean norm"
   (`prereg/eq2/PREREG.md:75-76`), after EQX-4 found Euclid better. This departs from CRR.md's "in the Fisher norm" (`CRR.md:168`).
4. **The past term generalised from "a replayed past batch"** (`CRR.md:167`) to penalties and constraints. It came with a
   mechanism statement: "useful exactly when the past term is the past task's loss or its Fisher-curvature (Laplace)
   approximation …, redundant when the units already match (ER-sum), and harmful when the past term is a constraint"
   (`prereg/eq2/PREREG.md:20-24`).
5. **The comparator.** An in-sample-tuned λ "which favours the baseline" (`prereg/eq2/PREREG.md:81-85`). The criterion is "not
   behind by a step" (step = max(1.0 pt, 2·SE)), a non-inferiority criterion, not "beats".
6. **The instrument.** A numpy MLP d-256-K, one head, tasks of two classes, 3 epochs per task, plain SGD lr 0.05, batch 10
   (`reports/eq3.md:17-18`; `reports/eq4.md:32-35`). Tabular PMLB carriers, standardised features, replacing the
   Mammoth/CIFAR design of CLAUDE.md §6 (AGENT_LOG 5, 59).
7. **Carrier construction.** A 5000-row stratified subsample without a class floor (EQ3); class ranking by count with floor 40
   (EQ4: `runs/eq4/frozen/eq4_score.py:114-115`); label order (EQ3: `runs/eq3/frozen/eq3_score.py:103-104`).
8. **BAYES1.** A convergence tolerance of 0.1 posterior sd, set on the synthetic gate (`reports/bayes1.md:11-15`).
9. **SOTA1.** H-EQ as the weight of a distillation (KD) past term, cap 10. The past-term type is the one the playground and
   the EQ2 mechanism statement had flagged as harmful (AGENT_LOG 3; `prereg/eq2/PREREG.md:23-24`).

---

## 3. Results (verdicts verbatim, by row id)

**H-EQ as stated (replay), EQX** (anchor: push-timestamp only):
- EQX-1 "**REDUCES: Ω = 1 ≡ a fixed replay weight (ER-sum family)**", observed −1.63700 / −0.46383 / −1.74914;
- EQX-2 "FAIL";
- EQX-3 "FAIL — the rule never beats ER-sum by a resolvable step; on two datasets it is behind it";
- EQX-4 "metric matters, in the direction against the theory: the Euclidean ratio beats the Fisher ratio";
- EQX-5 "report: the 40 %-less-compute claim does not transfer".

The report names the outcome: "Ω = 1 is ER-sum with a replay weight near 1 … median effective weight was 1.04, 1.12 and 1.10"
(`reports/eqx.md:17-21`).

**Normalised penalty step on online EWC:**
- **EQ2.** EQ2-0 "DECIDABLE"; EQ2-1 "**PASS, FRAGILE**"; EQ2-2 "DOES NOT REDUCE: normalised-gradient method"; EQ2-3 "holds";
  EQ2-4 "**VIOLATED** by DER++"; EQ2-5 "report: the expected miss does not appear"; EQ2-6 "FAIL: a broad plateau over
  0.5–1.41 with no resolvable peak at 1"; EQ2-7 "report: no published baseline is ahead of the rule"; EQ2-S "FRAGILE
  (cap-dependent …)"; EQ2-8 "report: … the pass in EQ2-1 is not explained by input scale". EQ2-1b "**PASS-0 (provisional)**".
- **EQ2R.** EQ2R-VOID "**VOID**"; CC-VOID "**VOID** with EQ2R".
- **EQ3.** EQ3-0 "decidable"; EQ3-1 "**FAIL** (fars behind by 3.7400 > step …)"; EQ3-2 "does not reduce"; EQ3-3
  "**VIOLATED**"; EQ3-4 "**VIOLATED** (… the harm clause is retired)"; EQ3-5 "report: no systematic miss"; EQ3-6 "**FAIL**
  (a plateau, no peak at 1 …)"; EQ3-7 "no published baseline is ahead by a step on every carrier"; EQ3-S "fragile"; EQ3-8
  "report"; EQ3-C "**FAIL**"; EQ3-D "report"; EQ3-A "**FAIL** (the pass is specific to the wide network)"; EQ3-I "**PASS-0**
  (weakly anchored; an invariance row, not a comparative win …)"; EQ3-B "report"; EQ3-P "report: Ω is a plateau over the
  whole grid on 4/6 carriers …". EQ2-1c: "EQ2-1b stays **PASS-0 with a failed replication recorded**".
- **EQ4.** EQ4-0 "DECIDABLE"; EQ4-1 "**FAIL**"; EQ4-1r "**FAIL** (… EQ3-1's 5/6 does not replicate as 6/6)"; EQ4-2 "IDLE";
  EQ4-3 "**FAIL** (…); the clip is the load-bearing part and a fixed weight carries it as well"; EQ4-4 "INERT"; EQ4-5
  "**VIOLATED**"; EQ4-6 "DOES NOT REDUCE: normalised-gradient method"; EQ4-7 "report"; EQ4-S "FRAGILE"; EQ4-P "report: a
  plateau, as EQ3"; EQ4-B "report"; EQ4-D "report only"; EQ4-I "PASS (PASS-0 at most: weakly anchored, on the one carrier
  whose records reached T1x after the hash; not quotable as a result)".

**BAYES-1:**
- BAYES1-B0 "**NOT DECIDABLE**";
- B1 "reported without verdict (B0 not decidable); the script's own line reads PASS on 6/6", with margins +18.1162 … +5.2082
  posterior sd;
- B2-16, B2-1/16, B3: "reported without verdict"; each script line "reads FAIL on 6/6, as the surrogate predicted";
- B4 "report: … the Bayes weight is the tuned weight on every carrier";
- B6 "report: no plateau in the posterior metric; the best Ω is below 1 on every carrier";
- B7 "report: does not reduce …";
- BS "not fragile".

**SOTA1** (OpenTimestamps complete):
- SOTA1-1a / 1b "**FAIL**" (d = −3.300000 against ER-ACE, 5/5 seeds behind); SOTA1-S "**not fragile**".
- SOTA1-2 "**FAIL**" (d = −2.943333 against MKD's λ; "BEHIND, not REDUCES", `reports/sota1.md:87`).
- SOTA1-3:
  - crr-cos (H-EQ at the head) "**FAIL**" (+0.80, TIE);
  - crr-beta "**PASS-0** (… the component is DER++'s label term, M4/M5)";
  - crr-ace, crr-alpha, crr-stepclock (TIE) and crr-a8, crr-kd (BEHIND) "**FAIL**".
- SOTA1-ND "NOT DECIDABLE (no registered verdict needs them)".
- SOTA1-C1..C3 "holds (construction …)".

**Other ledger rows using the rule:**
- SEC1-R (report): "rule − tuned: +3.9000, +3.7000, −1.2188, +3.5994, −0.6012, −3.5000, +4.8248, −2.2727, −6.7857, −6.7304,
  −0.4995, −7.8278"; SEC1-3 notes "the registered rule Ω = 1 on 8/12" (seen, R5).
- SCL3-3: "the rule Ω = 1 7/10" (beside SEC's PASS-0).
- SEC3-3: "the rule Ω=1 5/6".
- SCL1-E: "accuracy TIE on 12/12"; SCL2-E: "accuracy TIE on 9/9" (the wall clock against the own clock for the rule's averages).
- SCL1-1, SCL2-1: "holds (a check of the construction …)".

**Synthetic, not ledger (R4 rung):**
- `omega_sweeps.txt` [1]-[3];
- `omega_vs_methods.txt`: "scale-robust methods … ['omega']" (`:25`);
- `omega_reprocessed.txt` [1]-[7];
- `adam_checks*.txt` A1-A8, B1-B5;
- `Adam_SGD/checks/*.txt`: the drift gate "GATE OPEN" on a post hoc redesign (`drift_battery_2.txt:57`); T0′ "FRAGILE"
  (`:61`); mechanism "M1 FAILS, M2 holds; the noise-ratio explanation is not confirmed as declared" (`mechanism.txt:11`);
- FED gate CLOSED (`docs/notes/2026-09-22_fed_phaseA.md:1, 36-46`).

---

## 4. Answers to questions 1–9 for L-EQ

**Q1. What idea was initially investigated?** Equanimity: settled past and present should "exert equal pull" (`CRR.md:166-168`).
The idea comes with a theory value Ω = 1 that the external spec calls "the principal place where a philosophical commitment
becomes a risky numerical statement" (`CRR_test_specification…md:69`). The owner's working beliefs were "a threshold either
side of 1" and "1 is also bayes optimum" (PROMPT_LOG 69).

**Q2. How was it operationalised?** As a scalar weight on a past-term gradient, set by the ratio of smoothed gradient norms
(O1-O7, §2). It was never operationalised as precision weighting of occasions (the spec's A9/T5). That version belongs to the
surplus-weight law, gated CLOSED in SAL (AGENT_LOG 13; L-SURP).

**Q3. Which assumptions were added?** §2 items 1–9. The ones that do real work:
- the EMA and the cap (the cap is load-bearing: EQ2-S);
- the switch to the Euclidean norm (EQ2 onward);
- the extension beyond replay to penalty past terms;
- the in-sample-tuned non-inferiority comparator;
- plain SGD;
- the narrow tabular MLP instrument and its carrier-construction rules.

**Q4. Which added assumptions later became the thing that failed?**
- **The cap.** The EQ2/EQ3 passes "vanish when the ratio cap is below the tuned λ" (EQ2-S, EQ3-S; EQ3-C "FAIL" showed the cap
  is "not the whole story").
- **The mechanism statement** (harm on constraints; reduction on same-units replay). EQ2-4, EQ3-4 and EQ3-3, EQ4-5 are
  "VIOLATED". `reports/eq3.md:66-67` reads "falsified as written, for the second time".
- **The smoothing.** "The registered smoothing (EMA 0.9) costs at every scale … and at every noise level tried"
  (`ADAM_AND_PRIOR_ART.md:43-44`). Synthetic only; every real-data verdict is about the smoothed estimator.
- **Network width.** EQ3-A "the pass is specific to the wide network".
- **The row cap without a class floor.** It produced the degenerate fars carrier that decided EQ3-1 (`reports/eq3.md:20-28`).
- **BAYES1's convergence tolerance, set on a faster-converging surrogate.** B0 "NOT DECIDABLE" (`reports/bayes1.md:11-15`).
- **The Mammoth runner's argument passing.** SOTA1-ND.
- **The reported comparator gaps.** The coarse 10-point tuning grid overstated the rule in the synthetic checks
  (`ADAM_AND_PRIOR_ART.md:36-39`; AGENT_LOG 85). The comparison used a fixed lr (`Adam_SGD/ADAM_SGD.md:39-41`: "With the
  learning rate tuned for every arm, the rule and λ = 1 tied exactly").
- **The KD past term in SOTA1.** "Equalising the two gradient norms asked for a pull larger than the cap allowed, and the more
  pull, the lower the accuracy" (`CL Design Principle/FINDINGS.md:27`).

**Q5. Which failures reached the underlying CRR claim?**
- **H-EQ as stated.** EQX-1, EQX-3: H-EQ ties or trails ER-sum and the best fixed w, which is CRR.md's own failure condition
  ("fails if ties either", `CRR.md:313`).
- **"In the Fisher norm".** EQX-4 runs against it; and analytically "the metric moves the stopping point along the curve, it
  does not change the set" (`omega_reprocessed.txt:41`).
- **Ω = 1 as a distinguished value.** EQX-2, EQ2-6, EQ3-6 "FAIL"; EQ3-P and EQ4-P plateaus; BAYES1-B6 best Ω < 1 (report).
  Analytically the equal-norm rule has "a continuum of equilibria" on the Pareto curve, so "it does not choose a point on the
  front, it stops wherever it first reaches it" (`docs/notes/2026-09-22_omega_sweeps.md:33-38`). This holds in any norm. It is
  pressure at the level of "equal pull *magnitude*" as a trade-off principle, and it is the MGDA family's known property
  (`CONTINUOUS_LEARNING.md:475-480`).
- **The "Bayes optimum" belief.** Refuted: "Ω = 1 coincides with the Bayes optimum only when the trajectory happens to stop at
  the posterior mode" (`omega_sweeps.md:22-25`); CR6 "OFF THE MODE" (`cramer_rao_reading.txt:45`).
- **SOTA1-2.** It reaches H-EQ as written, because CRR.md "does not restrict the past term" (`CROSS_VERIFICATION.md:348-353`).
  It is strongly anchored and not fragile (SOTA1-S), with a mechanism that matches the knife edge (`FINDINGS.md:28`).

**Q6. Which failures reached only one implementation or mathematical translation?**
- **Instrument and frozen-code failures.** EQ2R-VOID / CC-VOID (a frozen-scorer bug), BAYES1-B0 (optimiser convergence),
  SOTA1-ND (runner flags).
- **Carrier defects.** EQ3-1's single failing carrier was a subsample defect (fars, class 0 empty).
- **EQ-B.** EQ4-3 and EQ4-4 reach the bounded variant EQ-B only. The clip is AutoClip-type prior art (`reports/eq4.md:76-84`).
- **The harm/reduction mechanism clauses.** These belong to EQ2's mechanism statement, not to CRR.md.
- **EQ3-A (width), EQ2-S / EQ3-S / EQ4-S (estimator constants).**
- **The zero-start freeze.** It reaches the literal ratio when the past term starts at zero (AGENT_LOG 126).
- **The "equal precision" reading (A9).** It was never chosen. The auditor's grep of AGENT_LOG, PROMPT_LOG and the EQ3, EQ4,
  BAYES1 and SOTA1 preregs for "which law carries", "which Ω = 1" and "item 5" found no record of the decision that
  `SPEC_RECONCILIATION.md:79` and `ontology/05_next_steps.md:38,58-59` required before further EQ preregs. Every failure
  after EQX therefore reaches the ratio law, not A9.

**Q7. What stayed numerically or structurally interesting despite failing promotion?**
1. **Non-inferiority of the normalised penalty step on online EWC**, with a named mechanism: the rule runs at or above the
   fixed-λ stability edge because "its step is bounded by the present step" (`reports/eq2.md:36-43`). The reduction arm at
   the rule's median w diverges (EQ2-2, EQ3-2, BAYES1-B7).
   - Margins on the 9 "load-bearing" carriers of EQ2–EQ4, from `results_vs_literature.txt:5-38` and rows EQ2-1, EQ3-1,
     EQ4-1r: positive on 5 (mfeat_fourier +3.3000, mfeat_pixel +2.1000, texture +2.7800, mfeat_factors +3.9000,
     mfeat_morphological +3.7000), negative on 4 (fars −3.7400, page_blocks −7.8278, segmentation −2.2727, yeast −6.7857).
     **Auditor's count (derived).** Four of the five positive carriers are feature sets of the same 2000 digits
     (`prereg/scl3/PREREG.md:69-70`).
   - Ahead by at least a step on 3 of 15 carrier-scorings (mfeat_fourier, led7, satimage). **Auditor's count (derived)** from
     the observed margins and steps in rows EQ2-1, EQ3-1 and EQ4-1r.
2. **Learning-rate × batch invariance on one carrier** (EQ3-I "PASS-0"; the tuned λ "moves 300 → 300 / 3000 / 3000 / 300").
3. **Drifting units (synthetic, post hoc, FRAGILE).** The unsmoothed ratio beat every fixed constant on 10 of 10 held-out
   seeds (`Adam_SGD/ADAM_SGD.md:61-73`). Part of the effect is built in: "the rule's effective weight is 1, the oracle's value,
   by the design of the world" (AGENT_LOG 93). The declared mechanism check "M1 FAILS" (`mechanism.txt:8,11`).
4. **The SOTA1 dose-response and stalemate** (post hoc). Accuracy falls with pull weight: "weight 0 (crr-kd) 22.49; MKD's
   fixed 2.75 … 21.13; H-EQ, median 10.000, at its cap in 217 of 270 samples, 18.19; H-EQ uncapped … 17.41". With H-EQ "the
   head keeps the first task and never takes in a new one" (`FINDINGS.md:27-28`). This is a clean real-benchmark
   demonstration of the equal-norm knife edge.
5. **The clip is load-bearing under poison.** "fixed without clip − fixed+clip: −16.2162 / −17.8979 / −32.3737 / −4.5355 /
   −4.2251 / +0.7857" (EQ4-3).
6. **The Laplace "1" in correct units** (CR5). This seeded SEC (AGENT_LOG 143).

**Q8. Which apparent successes reduced to ordinary mathematics or known mechanisms?**
- **The archive's "Ω = 1 best grid point 6/6"** (ARC-EQ-LAND): "Ω relabels the effective replay weight". On unseen data, EQX-1
  REDUCES.
- **The rule's direction.** It is MGDA on normalised gradients and the IMTL-G / Nash-MTL two-task solution, with a "max
  relative deviation over 1000 random pairs … 5.164e-15" (`pareto_identities.txt:2-4,18`). MEGA-II takes the bisector
  (`CONTINUOUS_LEARNING.md:477-478`).
- **The unsmoothed weight.** It is "the VQGAN adaptive weight (Esser, Rombach and Ommer, 2020)": 7.7432 against 7.7434
  (`adam_checks_2.txt:3,7`). It is also GradNorm at α = 0 without the learning (`CROSS_VERIFICATION.md:333-337`).
- **The scale-robustness "win" of `omega_vs_methods.txt:25`.** "The test measures the bound, not CRR"
  (`CROSS_VERIFICATION.md:386-388`). Against a finely tuned constant the rule is BEHIND: "rule / finely tuned 1.186"
  (`adam_checks_3.txt:9`).
- **Under Adam.** "the rule has no scale advantage under Adam in this model, its property is an SGD property"
  (`omega_reprocessed.txt:49`).
- **The Bayes count weight w = n_q/n_p** (`omega_sweeps.txt:6`). This is standard Bayes, and at equal counts it is ER-sum.
- **The Laplace weight 1 in Cramér–Rao units** (CR5). Rung "R0–R2: Fisher, Cramér and Rao's mathematics"
  (`cramer_rao_reading.md:127`).
- **K(1) = 1/φ.** "Standard (textbook steady-state Riccati)" (`CRR.md:265-266`). The fixed 1/φ gain is within 5 % of the tuned
  filter only at v = 1 (`omega_sweeps.txt:96`). "The normalised-gradient rule applied to the filter update is K = 1/2 at
  every v" (`:81`).
- **EQ-B under poison.** The fixed weight with the same clip does as well (EQ4-3), and the clip is AutoClip-type prior art.
- **SOTA1-3:crr-beta "PASS-0".** This is DER++'s label term. The NCM rows (+7.96 / +7.97) pass on the surrogate too
  ("report (no verdict)").
- **The pause construction rows** (SOTA1-C1..C3, SCL1-1, SCL2-1). These are construction checks, not evidence.

**Q9. Which apparent failures were infrastructure, identifiability, resolution or frozen-implementation failures?**
- **EQ2R-VOID and CC-VOID.** A frozen scorer rebinding `hid` (AGENT_LOG 40). Three unseen carriers were consumed and are now
  SEEN.
- **BAYES1-B0 "NOT DECIDABLE".** "The optimiser, not the rule, was being measured at that tolerance" (`reports/bayes1.md:13-14`).
- **SOTA1-ND.** Runner flags (AGENT_LOG 153).
- **EQ3-1's FAIL.** It is decided by fars, where the EWC family sits at chance and "the tuned λ = 283 reaches 13.0000 only with
  per-seed values 18.00, 15.70, 9.20, 12.00, 10.10" (`reports/eq3.md:24-27`). The FAIL stands under R6. Its information
  content about the rule is that of a carrier-construction defect.
- **EQ4.** The exclusions command read nothing (AGENT_LOG 82(b)); satimage overlapped with T1x after the hash (AGENT_LOG 82(a)).
- **Weak anchoring.** EQX, EQ2, EQ3, EQ4 and BAYES1 are all weakly anchored, because OTS was unreachable and tag pushes were
  refused (AGENT_LOG 1). This caps them at PASS-0 whatever they showed.
- **Resolution and identifiability of the "not behind" criterion:**
  - On 13 of 37 carrier-scorings the tuned λ is within a step of λ = 0.1. That covers "three of EQ3-1's five, EQ4-I's one
    carrier" (`CONTINUOUS_LEARNING.md:508-511`; `results_vs_literature.txt:95`), so EQ4-I's PASS-0 is on an INERT carrier.
  - A learner frozen after task 1 meets the same criterion on SCL3 (SCL3-3-G: "M6 not behind the tuned lambda on 7/10") and
    on SEC3 (SEC3-3-G: "5/6"). The ledger lists the rule at Ω = 1 at 7/10 and 5/6 on those same families (SCL3-3, SEC3-3).
    **Auditor's juxtaposition** of two ledger figures, not a new count.
  - No frozen-learner control was run on the EQ2/EQ3/EQ4 carriers. M6 covers the 30 held-out SEC-family carriers only
    (`SEC_Analysis/checks/m_checks.txt:77-118`). EQ4's loader ranks classes by count (`eq4_score.py:114-115`), the property P1
    links to the frozen learner's pass (`SEC_Analysis/WHY_SEC4_WORKED.md:77-80`). Whether the EQ-family passes would
    survive that gate is **not decidable from the record**.
- **Carrier non-independence.** mfeat_fourier and mfeat_pixel (EQ2), mfeat_karhunen and mfeat_zernike (EQ2R), and
  mfeat_factors and mfeat_morphological (EQ3) share the same 2000 digits (`prereg/scl3/PREREG.md:69-70`; the rule was written
  2026-09-24, AGENT_LOG 106). EQ3 recorded its mfeat carriers as "unseen before the push" (`reports/eq3.md:16-17`), because
  SEEN.md was keyed by name (`data/SEEN.md:27-34`). The auditor found no AGENT_LOG entry applying the shared-records rule
  back to EQ3 (grep for "mfeat" in `notebook/AGENT_LOG.md` returns entries 106 and 169 only). EQ3-I and EQ3-A stand on
  mfeat_factors. Under the later rule, two of EQ3-1's five not-behind carriers held records already opened in EQ2/EQ2R.

---

## 5. Four-layer tables for the key observations

### 5.1 EQX: the ratio rule on replay reduces to a constant (EQX-1, EQX-3)

| layer | content |
|---|---|
| (1) observed | Behind the best fixed replay weight on 3/3; median derived w 1.04–1.12; not ahead of ER-sum by a step (EQX-1, EQX-3; `reports/eqx.md:17-21`) |
| (2) CRR interpretation | Equanimity at Ω = 1 *is* summing the two losses: "a reasonable default" (`CRR.md:182-183`) |
| (3) ordinary explanation | With standardised class-IL features the two gradient scales do not swing, so the ratio "has nothing to adapt to and becomes a noisy constant" (`reports/eqx.md:56-61`). With equal counts the Bayes weight is w = 1 (`omega_sweeps.txt:20`) |
| (4) what would distinguish | A carrier where the units drift during the stream, chosen by a metadata rule before any data is opened, with the unsmoothed ratio, VQGAN, MEGA-II and a retuned constant as arms (`CONTINUOUS_LEARNING.md:451`). Even a win there "would be applied value, not CRR novelty" (same line) |

### 5.2 Ω = 1 is a plateau, not a value (EQX-2, EQ2-6, EQ3-6, EQ3-P, EQ4-P, BAYES1-B6)

| layer | content |
|---|---|
| (1) observed | Best Ω = 0.5 / 2.0 / 1.41 (EQ2-6); 2.0 / 4.0 / 2.0 / 2.83 / 1.0 / 2.83 (EQ3-6); plateau width 9/9 on 4/6 (EQ3-P); best Ω 0.71 / 0.5 / 0.5 / 0.71 / 0.5 / 0.71 with no plateau in the posterior metric (BAYES1-B6) |
| (2) CRR interpretation | Ω = 1 is "the principal place where a philosophical commitment becomes a risky numerical statement" (spec [P7]) |
| (3) ordinary explanation | At Ω = 1 every point of the Pareto curve is stationary; with exact gradients there is a knife edge at 1; "smoothing and mini-batch noise" widen it into a plateau (`omega_sweeps.md:33-55`). This is a published MGDA-family property (`CONTINUOUS_LEARNING.md:475-476`) |
| (4) what would distinguish | A version of equanimity that selects a point on the front (e.g. equal *precision* / count weighting), stated in CRR.md before a test. The record's selecting principles are "not CRR's" (`CONTINUOUS_LEARNING.md:481-482`) |

### 5.3 Non-inferiority of the normalised penalty step on online EWC (EQ2-1b, EQ3-1, EQ4-1r)

| layer | content |
|---|---|
| (1) observed | Not behind the in-sample-tuned λ on 3/3 (EQ2-1), 5/6 (EQ3-1), 4/6 (EQ4-1r). Fragile in the cap (EQ2-S 6/27; EQ3-S 6/54; EQ4-S 16 of 96). Rule − EWC tuned has a "median -0.60" over 37 carrier-scorings (`results_vs_literature.txt:92`). ER is ahead of the rule on 15 of 15 carriers with a replay arm, median 39.70 (`:89`) |
| (2) CRR interpretation | Equanimity as a tuning-free balance of settled past and present in one family of past terms (`CONTINUOUS_LEARNING.md:400`) |
| (3) ordinary explanation | The step bound lets the penalty run above the fixed-λ stability edge (`reports/eq2.md:36-43`). This is the bound of the normalised-gradient family (VQGAN, GradNorm α = 0, MEGA-II). An in-sample λ found on a grid near a stability edge is a coarse comparator. "Not behind" is automatic on inert carriers and was met by a frozen learner on two later families. Positive margins concentrate on one digit set (§4 Q7, derived) |
| (4) what would distinguish | MEGA-II and the normalised two-term sum as arms (never run, `CONTINUOUS_LEARNING.md:512`); a frozen-learner gate and a load-bearing criterion pre-registered (AGENT_LOG 131 proposals); a finely tuned λ grid with and without a clip; independent carriers (shared-records rule) |

### 5.4 BAYES-1: the rule far from the posterior (B1, reported without verdict)

| layer | content |
|---|---|
| (1) observed | d(rule) − d(Bayes) +18.1162 … +5.2082 posterior sd. The Bayes arm's own error is 0.18–0.89, so B0 is "NOT DECIDABLE". Rule MSE 1.5 to 4.2 times the Bayes arm's (`reports/bayes1.md:35-36`) |
| (2) CRR interpretation | None that survives. The rule was not claimed to be Bayes after `omega_sweeps.txt` [1] |
| (3) ordinary explanation | "The present batch gradient is mostly noise … their length ratio is therefore a noise ratio, and the rule read it as an instruction to hold the past fifty to a hundred times harder than Bayes does" (`reports/bayes1.md:33-36`) |
| (4) what would distinguish | BAYES-1b with a convergence-scaled epoch budget registered in advance (`reports/bayes1.md:63-65`). The B1 margins exceed the precondition's error by an order of magnitude, so a decidable rerun would probably confirm B1. That expectation is not a verdict |

### 5.5 SOTA1-2: equanimity as the KD weight on Split-CIFAR-100

| layer | content |
|---|---|
| (1) observed | BEHIND MKD's λ by −2.94 on 3/3 seeds (SOTA1-2), strongly anchored; not fragile in its sensitivity cells (SOTA1-S, including cap 100 and smoothing 0.5). Post hoc: the H-EQ weight sat at the cap 10 in 217 of 270 samples; the uncapped median was 11.457; the fast head's newest-task class-IL accuracy was 0.02 with H-EQ against 27.98 without the pull (`FINDINGS.md:27-28`) |
| (2) CRR interpretation | Equal pull between the settled past (slow model) and the present |
| (3) ordinary explanation | Distillation is a constraint whose gradient length is not a distance-from-past measure (`CROSS_VERIFICATION.md:348-353`). Equal-norm balancing at a knife edge yields stasis. A smaller KD weight (including 0) was better in this setting (post hoc) |
| (4) what would distinguish | An equanimity rule that is not an equal-norm ratio, declared before a test. The synthetic preview already showed "MKD's constant was AHEAD of Ω = 1 (−4.11)" (`prereg/sota1/PREREG.md:129`), and AGENT_LOG 140(4) records that it was deliberately not used to change arms |

### 5.6 Where a "1" arises naturally (Bayes, Laplace, Kalman, Cramér–Rao)

| layer | content |
|---|---|
| (1) observed | Bayes MAP iff w = n_q/n_p (`omega_sweeps.txt:6`). The Laplace penalty in Cramér–Rao units at weight 1 is the exact sequential-Bayes mode; with Fisher scaled by c the right weight is 1/c (`cramer_rao_reading.txt:38-43`). K(1) = 1/φ at v = 1 only (`omega_sweeps.txt:80, 96`). Equal precision gives K = 1/2 at v = 0.707107 (`:80`) |
| (2) CRR interpretation | "1" as equanimity in the system's own (A1′) unit; √(q/r) as a Fisher speed (`CRR.md:265-266`) |
| (3) ordinary explanation | Unit-weight log-likelihood summation (Bayes) and the Riccati solution. The "1" is a units identity, not a law about which v systems have. The H-EQ ratio "gives H-EQ's Ω = 1 no meaning (CR6)" |
| (4) what would distinguish | A prediction of v (or of the unit) that a system *has*, from CRR alone. RLAW tried the gain route and "every admissible row FAILs" (L-RLAW). O1 remains open (`CRR.md:268-271`) |

### 5.7 Drifting units (synthetic, Adam_SGD)

| layer | content |
|---|---|
| (1) observed | Unsmoothed ratio AHEAD in G-DRIFT2 (0.898) and in T0′ under SGD, momentum and coupled Adam, 10/10 seeds. BEHIND in T1 (1.137). FRAGILE in Ω (`drift_battery_2.txt:10,15,32,57,61`) |
| (2) CRR interpretation | Equanimity strips units the learner cannot see; "Cancelling the units is its real strength" (`ADAM_SGD.md:167`) |
| (3) ordinary explanation | The VQGAN-style ratio. At equilibrium the signal cancels, so the ratio reads relative noise, which the world made equal (AGENT_LOG 93). The declared mechanism test "M1 FAILS" |
| (4) what would distinguish | Real carriers with drifting units chosen by rule; arms with unequal present/past noise; the VQGAN weight and MEGA-II as baselines |

---

## 6. Salvage classification (A–G), with propagation level

| sub-line | class | core principle → operationalisation → test → failure | highest level legitimately reached |
|---|---|---|---|
| H-EQ on replay (EQX) | **A + C** | equal pull (`CRR.md:166-168`) → Fisher-norm ratio, EMA 0.9, replay → EQX on 3 unseen PMLB streams vs ER-sum / fixed w → EQX-1 REDUCES, EQX-3 FAIL, EQX-4 Fisher worse | **The hypothesis as stated in CRR.md**, for same-units replay on tabular class-IL. It does not reach a drifting-units regime (not tested). Weakly anchored, but every line is negative (`reports/eqx.md:28-30`) |
| Ω = 1 as a distinguished value | **A** (empirical) **+ C** (analytic, MGDA-known) | "Ω = 1" → nine-point Ω grid → EQX-2, EQ2-6, EQ3-6 FAIL; EQ3-P, EQ4-P plateau; BAYES1-B6 best Ω < 1 | **The equal-pull-magnitude reading** of the principle, in any norm (`omega_reprocessed.txt:41`; `omega_sweeps.md:33-38`). Not the equal-precision reading (§4 Q6) |
| Normalised penalty step on online EWC (EQ2-EQ4, SEC1-R, SCL3/SEC3 rule columns) | **F + C** (and D, E components) | equal pull → Euclidean ratio on an EWC penalty, cap 1e4 → non-inferiority vs in-sample λ → PASS-0 fragile / FAIL 5/6 / FAIL 4/6; controls VIOLATED | One operationalisation **outside CRR.md's stated domain** (a penalty, not a replayed batch). The negative evidence (controls, fragility, replication 4/6) reaches that operationalisation. The positive evidence is capped at PASS-0 and reduces to prior art |
| EQ-B (bounded rule) | **C** | equal pull + present-step clip → EQ4 clean and poisoned → EQ4-1 FAIL, EQ4-3 FAIL, EQ4-4 INERT | **One implementation enhancement**: "the clip is the load-bearing part and a fixed weight carries it as well" (EQ4-3) |
| BAYES-1 | **E + D** (with report-level negative structure) | equal pull → rule vs exact posterior → B0 NOT DECIDABLE | **Instrument only** for the verdict. The report-level margins point against the rule being near-Bayes, which the mathematics already says (`omega_sweeps.txt` [1]) |
| SOTA1-2 (KD weight) | **A** | equal pull → ratio as the KD weight, cap 10 → online Split-CIFAR-100 vs MKD λ → BEHIND −2.94 | **The hypothesis as written in CRR.md** ("does not restrict the past term", `CROSS_VERIFICATION.md:348-353`), for distillation past terms on one benchmark. Strongly anchored; not fragile. The record had already proposed excluding such terms (v3.2 proposal, not adopted) |
| SOTA1-3:crr-cos ("H-EQ at the head") | **A** at operationalisation level (TIE → FAIL) | equal class-weight norms → cosine head ablation → +0.80 TIE | One operationalisation (the cosine head). Its retrodictive grade was MIXED 19/20 on published ablations (`CL Design Principle/checks/retro_sota.txt:17`), a retro→prospective gap |
| SOTA1-1 (integrated learner) | **C** (design comparison, "not a CRR hypothesis", `reports/sota1.md:46-47`) | — | The design, not CRR |
| SOTA1-3:crr-beta | **C** | — | DER++'s β term; PASS-0 for a published mechanism |
| SOTA1-ND, EQ2R-VOID, CC-VOID | **D** | — | Instrument / frozen code only |
| Kalman K(1) = 1/φ; Bayes count weight; Laplace weight 1 (CR5) | **C** (R0–R2) | — | Standard mathematics. "1" arises naturally only as a units identity (Bayes) or at one Fisher speed (Kalman) |
| "Which Ω = 1" (ratio vs equal precision vs Fisher speed) | **E** (conceptual identifiability) | — | The theory says two things (batch_02 row 4 "INTERNAL"; SPEC_RECONCILIATION §4). Not decidable until CRR.md fixes one |
| Drifting-units niche | **F** (rung R4, post hoc, fragile) + **C** (VQGAN) | — | Synthetic only; never tested on real carriers |
| FED | **E/B** (gate CLOSED: "nothing to win") | — | One surrogate design after one correction round (AGENT_LOG 71) |
| Zero-start anchors (RW2) | **B** | equal pull → ratio with a past term that starts at zero → freeze | The literal ratio's domain of definition (`CONTINUOUS_LEARNING.md:445`) |
| Equanimity clock in SCL1/SCL2 | **C/E** (TIE, report) | — | The clock of the rule's averages is immaterial at these pause rates |

**G: none.** The best-placed row is EQ2-1b "PASS-0 (provisional)" (rung R6) with a failed replication recorded (EQ2-1c) and
two violated controls. EQ3-I (R6) is an invariance row on a carrier sharing records with EQ2's. EQ4-I (R6) is on an INERT
carrier whose records reached T1x after the hash.

---

## 7. Extinguished-lead check (was anything killed at a lower level than the claim it was taken to bear on?)

1. **CRR.md's EQX status line over-propagated, then partly corrected.** "H-EQ is retired as an adaptive rule"
   (`CRR.md:181-182`) was written from three same-units replay streams. That is the regime the EQX gate itself predicted
   would reduce (`reports/eqx.md:56-61`; `prereg/eqx/gate_EQ.txt`: S-R "FAIL", S-V "PASS"). Two days later EQ2-2 "DOES NOT
   REDUCE". The EQ2 status line (`CRR.md:184-192`) corrects the record by adding to it, but "retired as an adaptive rule"
   still stands in the canonical text. The retirement was **broader** than the evidence (replay, same units). This is the
   opposite of an extinguished lead: an over-reaching kill that was walked back.
2. **ADAM_AND_PRIOR_ART over-propagated a negative too**, then Adam_SGD corrected it. "A finely tuned constant beats the rule
   wherever the scales differ" was found to hold "only in a narrow setting: the 'imp' reading, at a fixed learning rate, with
   a constant tuned on the seeds it was scored on" (`ADAM_SGD.md:132-140`). The correction was made by addendum, and the
   protocol caught its own overstatement.
3. **The drifting-units niche was never tested on real data.** It is the only regime where the gate's positive control (S-V)
   and the synthetic batteries predict an advantage. Every real-data carrier (EQX-EQ4) was a standardised class-IL stream.
   The "EQ5" accuracy study was declined (AGENT_LOG 85: "pre-registering an 'EQ5' accuracy study to have something to run" is
   listed as the rejected alternative). Avenue 3 is "none yet declared" (`CONTINUOUS_LEARNING.md:448,451`). **Not killed;
   untested.** The record itself caps its value: a win would be the VQGAN weight's (`:451`).
4. **The registered smoothing persisted through every real-data test.** EMA 0.9 was frozen from the archive by CLAUDE.md §6
   and used in EQX through SOTA1 (`prereg/sota1/PREREG.md:68`), although the synthetic record later found that it "costs at
   every scale". The unsmoothed rule never had a real-data test under the H-EQ name. The real-data FAILs therefore reach
   **one estimator**. That matters little for CRR, because the unsmoothed form is prior art.
5. **The equal-precision reading (A9) was never chosen or tested as such.** The decision required "before any further EQ
   prereg" (`SPEC_RECONCILIATION.md:79`) was not taken (§4 Q6). Four studies then tested the ratio law. This is the clearest
   case in L-EQ of **confirmatory machinery running ahead of theory formulation**. The untested reading is not obviously
   CRR-specific either: "equal-precision weight is Bayes-optimal iff the precisions are equal"
   (`crr_retrodictions.txt:142`). Its natural home is inverse-variance (Bayes) weighting, which the SEC lineage effectively
   pursued.
6. **The one CRR-proper avenue was never declared.** Per-task unit normalisation plus P3 age-weighted bounded accumulation
   (`ADAM_SGD.md:170-176`; `CONTINUOUS_LEARNING.md:450`: "the only avenue built from CRR-proper ingredients (P3, A6), so it
   could say something about CRR") was named on 2026-09-23 and is listed as a candidate. It is not run or declared anywhere
   in the record the auditor read. The programme moved to SEC (Laplace weight 1/2 plus calibration), which drops the P3
   ingredient. **An unexplored lead, not an extinguished one.**
7. **The closest published comparators were never run.** MEGA-II and the normalised two-term sum (`CONTINUOUS_LEARNING.md:512`)
   were not arms. The reduction to them is analytic (`pareto_identities.txt`), not empirical. GradNorm "as implemented
   (weights summing to 2) starves the present term and diverges" (EQ2-7), which the report flags as "not of GradNorm at its
   best" (`reports/eq2.md:61-63`). This is comparator weakness in the rule's favour.
8. **SOTA1-2 was not killed below its level.** The cap bound most samples, but the uncapped sensitivity cell is also BEHIND
   (SOTA1-S "H-EQ cap 100 … −4.11"; `FINDINGS.md:27` uncapped 17.41). The failure reaches the equal-norm KD weight on this
   benchmark, which is the level claimed.
9. **EQ3-1 was killed by a carrier defect.** The FAIL is decided by fars, a degenerate carrier the pre-registered subsample
   produced (§4 Q9). The verdict stands under R6. As evidence against the rule it is **D-level**; EQ4-1 / EQ4-1r then
   supplied genuine 4/6 evidence on non-degenerate carriers.
10. **"Let Ω grow" was refuted analytically** (AGENT_LOG 95). The kill was made at the right level, by mathematics.

**Net judgment for L-EQ.** The equal-*magnitude* reading of equanimity was tested fairly enough to say it does not select a
trade-off and does not beat the constants it reduces to. That conclusion holds at the level of the hypothesis as written,
backed by an analytic argument. What remains untested is whether any *other* formalisation of equanimity says something not
already said by Bayes or Kalman. The record leaves that open (decision list item 5) and did not try it. That gap is a
formulation gap, not a protocol kill.

---

## 8. Question-10 evidence (did the protocol prevent reasonable exploratory development?)

**Time from owner request or first declaration to confirmatory hash, and from hash to data:**

| study | from | to hash | hash → data | source |
|---|---|---|---|---|
| EQX | repository import 2026-09-15 17:50:15Z | 18:14:48Z (24 min) | same day | `git log` |
| EQ2 | gate re-opened 2026-09-17 00:04:02Z | 00:10:49Z (7 min) | 00:11Z (< 1 min) | `git log`; AGENT_LOG 25 |
| EQ3 | prompt 69, 00:59:34Z | 01:21:32Z (22 min); the omega_sweeps mathematics was committed 01:14:35Z, 7 min before the hash | 01:23Z | PROMPT_LOG 69; `git log`; LEDGER.md:45 |
| EQ4 | prompt 74, 04:59:33Z | 05:39:00Z (about 40 min), including the EQ-B design iteration and the dev run on SEEN carriers | about 23 h (R3) | AGENT_LOG 63; LEDGER.md:73 |
| BAYES1 | — | 15:52:37Z | 15:52:56Z (19 s) | LEDGER.md:62 |
| SOTA1 | prompt 190, 2026-09-25 05:27:48Z | 11:51:16Z (about 6.4 h, including Phase A) | 2026-09-26T00:07:26Z (R3) | `git log`; LEDGER.md:152 |

**Exploration that the protocol allowed, and that took place:**
- an off-repo playground before EQ2 (AGENT_LOG 3);
- ten synthetic batteries at rung R4: `omega_sweeps`, `omega_vs_methods`, `omega_reprocessed`, `pareto_identities`,
  `adam_checks` 1-3, `Adam_SGD` 1-4 and FED;
- a post hoc redesign permitted and labelled (Adam_SGD Declaration 3, AGENT_LOG 93);
- a dev run on SEEN carriers before EQ4 (`runs/eq4_dev/summary.txt`, AGENT_LOG 63);
- confirmatory-on-seen tests permitted (SEC1, SCL1 at rung R5).

The gates were redesigned when a positive control was mathematically impossible: gate_EQ2 attempt 1 was CLOSED and replaced
within an hour (AGENT_LOG 4).

**Where the protocol, or the pace around it, cut development short:**
- **Theory-level choices were not made before testing.** The "which Ω = 1" decision was required by
  `SPEC_RECONCILIATION.md:79` and `ontology/05_next_steps.md:58-59`, but was never recorded. EQ3, EQ4, BAYES1 and SOTA1 still
  ran (§7.5). This is not the protocol suppressing exploration. It is the confirmatory machinery being invoked on an
  operationalisation the theory had not chosen over its rival.
- **Early freezing of an inherited estimator.** CLAUDE.md §6 fixed "ratio=ema, smooth=0.9" at the first prereg. Later
  synthetic work found that this choice costs, but no real-data revision followed (§7.4). Under R3 a revision is a new
  hypothesis needing a new study; the protocol makes that costly but does not forbid it. The decision not to run "EQ5" was a
  judgement (AGENT_LOG 85), not a rule.
- **Frozen-code strictness converted bugs into lost data.** EQ2R crashed on an untested branch after an R3 hold and a session
  outage. Three unseen carriers were consumed (AGENT_LOG 25, 40). SOTA1-ND lost the LwF / online-EWC context arms
  (AGENT_LOG 153). In both cases the rule ("a script that must change after the tag voids the study") correctly prevented
  rescue. The lesson the record draws is to run smoke modes before the hash (AGENT_LOG 59), which is an engineering fix, not a
  loosening.
- **Preconditions tuned on surrogates were too tight for real data.** BAYES1's B0 tolerance came from a surrogate that
  "converged faster than the carriers" (`reports/bayes1.md:14-15`), producing NOT DECIDABLE. The 19-second hash-to-data gap
  left no room to measure convergence on the carriers first. A registered "convergence-scaled budget" is named only for a
  later day.
- **One correction round, then stop.** FED stopped after one correction ("Tuning this surrogate until it passes is exactly
  what the protocol forbids in spirit", `fed_phaseA.md:45-47`). SAL was CLOSED with alternative operationalisations rejected
  as a "forking path" (AGENT_LOG 13). In L-EQ these stops seem justified by the gates' own content (nothing to win).
- **Synthetic previews were not allowed to steer SOTA1's design.** AGENT_LOG 140(4): "switching the headline learner to
  crr-kdfixed or dropping the cosine head / A8 / KD after seeing synthetic results" was rejected as tuning on the gate. The
  registered test therefore included a component the preview had already shown losing. That kept the test clean. It also
  meant the strongly anchored benchmark was spent on a design the exploratory evidence disfavoured. Post hoc diagnostics
  (`FINDINGS.md:27-29`) may only be used "with a fresh prereg on a new dataset on a later day".

**Reading for L-EQ.** The record does not show the protocol preventing exploratory development of the equanimity rule. Much
synthetic exploration happened and was labelled. What it shows is:
- confirmatory tests launched within minutes of the owner's requests, while the mathematics of the rule was being worked out
  the same hour (EQ3's hash came 7 min after omega_sweeps);
- an inherited estimator frozen before its costs were known;
- a theory-level ambiguity left unresolved across four studies.

The machinery was merciless and correct about what it scored. Where it went wrong, it went wrong by being invoked too early
on an under-formulated operationalisation, not by forbidding development.

---

## 9. Open questions for Phoenix

**What Phoenix may explore** (exploratory, labelled, none of it evidence until pre-registered):
1. **Formulation first.** Decide in the theory text which "equanimity" is meant, before any test:
   - (a) equal pull *magnitude* (the ratio; analytically non-selecting; reduces to MGDA / VQGAN);
   - (b) equal *precision* / Bayes count weighting (selecting, but standard);
   - (c) Fisher speed v = 1 (K = 1/φ; a statement about systems, untested);
   - (d) the surplus-slope λ = 1 of the occasion weights (L-SURP; SAL gate CLOSED).
   The record's numbers on both sides are in `omega_sweeps.txt` [3] and `batch_02.txt:50-61`.
2. **The drifting-units regime on real carriers.** Exploratory first. The unsmoothed ratio, VQGAN, MEGA-II, a finely tuned
   constant (with lr tuned per arm, `ADAM_SGD.md:39-41`) and unequal present/past noise are the required comparators. Expect
   no CRR novelty even if it wins.
3. **Per-task unit normalisation with P3 age-weighted bounded accumulation** (`ADAM_SGD.md:170-176`), the only CRR-proper
   continual-learning construction the lineage produced. It must be compared against SEC, raw Laplace and Bayes counting
   (q → 1).
4. **The equal-norm knife edge as a diagnostic of plasticity loss.** SOTA1's stalemate (`FINDINGS.md:28`) is a clean
   mechanism; a descriptive study of when equal-norm balancing freezes a head is legitimate exploratory work.
5. **Any reopening of the EWC non-inferiority** must carry, pre-registered:
   - a frozen-learner gate (SEC6-G style);
   - a load-bearing-carrier criterion;
   - a shared-records independence rule (mfeat);
   - MEGA-II and the normalised sum as arms;
   - a finely tuned λ with and without a clip.
6. **BAYES-1b** with a convergence-scaled budget, if the Bayes comparison is still wanted (`reports/bayes1.md:63-65`).

**What Phoenix must never claim:**
- That Ω = 1 is optimal, Bayes-optimal, a threshold, or a distinguished value of the ratio rule (EQX-2, EQ2-6, EQ3-6,
  BAYES1-B6; `omega_sweeps.txt` [1]-[2]).
- That H-EQ beats ER-sum or the best fixed weight (EQX-1, EQX-3), or that it beats a published distillation constant
  (SOTA1-2).
- That the ratio rule is new. It is the VQGAN adaptive weight without smoothing, GradNorm at α = 0, and MGDA / IMTL-G /
  Nash-MTL for two terms (`ADAM_AND_PRIOR_ART.md:40-44, 111-128`; `pareto_identities.txt:18`).
- That EQ2-1b, EQ3-I, EQ4-I or SOTA1-3:crr-beta are CRR findings. They are PASS-0 at most, with recorded failed
  replication, violated controls, inert or shared-record carriers, or a published mechanism.
- That K(1) = 1/φ, the Bayes count weight or the Laplace weight 1 is evidence for CRR (standard; R0–R2).
- That the drifting-units result is evidence. It is post hoc, R4, FRAGILE, and partly built into the world's design
  (AGENT_LOG 93).
- That SEC is H-EQ or a CRR rule (P1 F11; L-SEC). Nor that the rule "helped arrive at" SEC as anything more than historical
  lineage (AGENT_LOG 143 states both).
- That the rule is well-posed for past terms that start at zero (KL-to-reference, L2-SP anchors) (`CONTINUOUS_LEARNING.md:445`).
- That the H-EQ failures falsify "equanimity" in the ontological or valuation sense (zero stake at the cut). They reach the
  gradient-norm operationalisation and the hypothesis as written in CRR.md, not L-PAUSE's construction or the
  contemplative reading.
