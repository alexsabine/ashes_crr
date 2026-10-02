# PRE-PHOENIX INTERPRETIVE AUDIT — NO VERDICTS ALTERED

## Declaration (pushed before the audit's reading begins)

**The request.** Prompt-log entry 260 (2026-10-02): "PRE-PHOENIX AUDIT — ASHES". The aims are:
- a final audit of this repository's own history;
- then a cross-audit against alexsabine/embers_CRR;
- a SALVAGE MAP, using categories A–G;
- a Phoenix inheritance table;
- an answer to the closing question on whether the adversarial architecture has been appropriate, suppressive, or both.

**Status.** This is an interpretive note, not evidence (R8).
- It changes no verdict, ledger row, report, pre-registration, pinned output or log entry.
- It is written in a new folder, `Pre_Phoenix_Audit/`, and committed separately from the historical record.
- Every committed number it quotes is cited to a ledger row (by id) or to a pinned output (by file and line).
- Any new count it makes is printed by a committed script in `Pre_Phoenix_Audit/checks/`, with its output pinned (R1).

## What the audit will not do

- Change, soften, relabel or rescue any verdict.
- Run any new confirmatory experiment, or open any held-out data.
- Import any Embers verdict into Ashes, or any Ashes verdict into Embers.
- Commit or push anything to Embers. That repository is read only, from a shallow clone of commit 7082f23 (2026-09-28).
- Promote anything beyond its current ledger rung.

## Method

1. **Ashes self-audit by lineage.** Each lineage is read in full: theory, declarations, pre-registrations, frozen code,
   ledger rows, reports, AGENT_LOG and PROMPT_LOG. Questions 1–10 of the request are answered per lineage.
   - For each observation, four things are separated:
     - the observed phenomenon;
     - the CRR interpretation;
     - the ordinary or non-CRR explanation;
     - the evidence that would distinguish the two.
   - Each line of inquiry gets one or more salvage categories, A–G, as the request defines them. Where it applies, the
     audit states core principle → operationalisation → test → failure, and the highest level actually challenged.
2. **The lineages and their stable IDs:**

   | ID | lineage |
   |---|---|
   | L-SEC | the calibrated Laplace weight (SEC1, SCL3, SEC3–SEC6R, SEC7, SPA1, P1) |
   | L-EQ | Ω = 1 / H-EQ / equanimity, Bayes and Kalman connections (EQX–EQ4, BAYES-1, SOTA1-2, Adam_SGD, omega_sweeps, cramer_rao_reading) |
   | L-L5 | H-L5, "change has its own clock" (ARC rows, MEAS, CARD, Life_Sciences CD, PRED70's H-L5 rows) |
   | L-T1 | H-T1, path length against endpoint (ARC-T1, T1x, T1x2) |
   | L-CUT | A3 / H-CUT, the antipodal cut and cut content (gates, Cut_Content, Rupture_Detection) |
   | L-SURP | the surplus S and lived surplus (SAL, the occasion-weight law) |
   | L-MEM | memory without exemplars (RQM, RRM, RRM2, HopDC, CPL1) |
   | L-CLK | own-clock optimisation and consolidation (OB1 C1/C3, FOREVER) |
   | L-PAUSE | the empty cut / Empty True Map / corrigibility (SCL1–3 C rows, NT1, STAKE1, Empty_Cut_Engineering, RW1–2, Lossless_Pause, EPS1–2, DR1, Attention, CORRIGIBILITY_2026) |
   | L-RLAW | the regeneration law, CRR 2.0 |
   | L-RETRO | the retrodictive banks (the issue-#21 battery, SYNTHESIS batches, PRED70, labs bank, FRONTIER) |
   | L-ONT | the ontology and its relation to the empirical programme |
   | L-APP | applied and compute work (Compute_Savings, Energy, the APP1 and P7 suites, Robotics ROB1) |

3. **The retrodictive-to-prospective gap.** It is counted with denominators kept apart, from `Epistemic_Review/checks/ladder.txt`
   and `redundant_vs_fail.txt`. Any recount is done by a pinned script.
4. **The process audit.** This covers the gates closed before any data, the NOT DECIDABLE, VOID and instrument failures, the
   post hoc additions, and the time each idea spent between first declaration and confirmatory test. It is read from
   AGENT_LOG and PROMPT_LOG.
5. **Embers.** It is read after the Ashes self-audit is drafted. The audit records:
   - what Embers inherited;
   - what it added (the rotor extension);
   - which of its failures bear on baseline CRR;
   - where its epistemic machinery differs from Ashes'.
   Disagreements are stated from both sides, without forcing a convergence.
6. **The Phoenix inheritance table,** with the columns the request names.
7. **Independent verification.** Before commit, a separate agent checks every citation and number against its source and
   confirms that no historical file changed.

## The auditor's expectations, written before the reading (to be checked, not defended)

1. Most held-out FAILs will turn out to reach one operationalisation, not a CRR principle stated in `theory/CRR.md`. A
   minority will reach the stated hypotheses directly (H-L5 on real carriers; H-T1 against the old-probe endpoint).
2. Several "successes" will reduce to known mathematics. Examples are SEC (the Laplace weight plus a units calibration
   plus AR1's clip), the pause (standard checkpoint and resume), and Ω = 1 (a constant or the VQGAN weight).
3. Instrument and identifiability failures will form a substantial share of the non-PASS outcomes since 2026-09-25: closed
   gates, loader defects, uninformative criteria and NOT DECIDABLE rows.
4. The retrodictive record will mainly establish expressive coverage (redescription), not unique prediction.
5. The answer to the closing question will be a mixture, with specific parts on each side.

If the reading contradicts any of these, the report says so.
