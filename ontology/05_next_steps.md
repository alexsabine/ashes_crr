# 05 — Next steps

Ordered by what each unblocks. Every step is a pipeline step: a script, a pinned output, a gate, a
prereg, a ledger row. None of them is a rewording. Each section ends with a fifth-grader line.

## 1. A causal instrument (unblocks everything about tense)

- Implement a second intrinsic phase in `src/crr/instrument/core.py` that uses no future sample: a
  Poincaré section on a named level, and a causal phase with a registered delay. Both must be reported
  beside the analytic signal on every row (CLAUDE.md §3.1 already says a named alternative must be).
- Implement a trailing-window unit estimator (the detrender fitted on past occasions only) as a named
  alternative to the centred Savitzky–Golay, and correct the leverage factor of the registered one in
  the same change (AGENT_LOG 30).
- Add `gate_TENSE` to the Phase-A gates: a cut located from the settled past must agree with the
  registered cut within one sample on the positive controls (S-A, S-A′, S-G2) and must not on the
  analytic reading; batch 21 row 2 gives the expected numbers (Poincaré within 1 sample; analytic
  0.146 half-turns off at d = 0). A7 becomes gateable.
- Re-run every gate and every H-L5 battery row under the causal instrument and pin the differences.
  Batch 21 predicts the symmetric signals survive and the asymmetric surrogate does not.

> Build a line-finding machine that cannot peek, and check which of our earlier answers survive.

## 2. The v3.2 decision list (unblocks every prereg)

Each is an INTERNAL row's question; each needs one sentence in CRR.md and then a gate.

1. Which intrinsic phase A3 cuts on: analytic signal, phase-plane angle, Poincaré section, or the
   system's own event (batch 07 row 3, batch 21 row 2). Proposed: the system's own event where it has
   one, a causal section elsewhere; the antipode then names nothing on one-dimensional traces and
   H-CUT is restated as "own event against extremum" or retired.
2. Which reading of A3 on projective carriers: rotor, arc half-turn, or orthogonal state (synthesis
   row 4, batch 05 row 3, batch 25 row 5). Proposed: the arc half-turn (the Mandelstam–Tamm time),
   because it always exists.
3. Which unit A1′ names on a count carrier: one event or one reporting window (batch 01 row 3).
   Proposed: one event, with the window named as an outside constant where a study uses it; the
   measles rows are then re-read, not re-scored.
4. Named or estimated unit, and with which detrender (batch 06 row 4, batch 23 rows 2–3).
5. Which Ω = 1: Fisher speed 1 or equal precisions (batch 02 row 4, batch 06 row 3).
6. P3's normalisation: finite-history MaxEnt or the infinite-horizon closed form (batch 17 row 3).
7. What a partial reset is, and which boundary jumps are arc (batch 18 row 3, batch 15 row 3):
   proposed, `segment_end="exclusive"` as the default, with the jump the cut.
8. Whether a system's law is part of its settled past (file 07 row 2, added 2026-09-22): on a deterministic
   machine the clock of the next event is open under one reading (0.0478 bits after three steps) and fixed
   under the other (0 bits), so A8 has no value until this is decided.
9. The FEP reading (file 09, added 2026-09-22): whether A3's cut is the datum's instant or the belief's occasion (batch 28 row 1: the mass lands at once, the change spreads after); whether the registered EMA estimator's oscillation above Ω = 1 (batch 28 row 2) is an estimator defect or the rule's; whether the A1′ unit's two known factors as a precision (batch 28 row 3) belong in the clause; a gate for tense on an active-inference agent (file 09 §3). The third ADDS candidate (batch 28 row 4, a bounded mean against accumulated counts) joins the expert protocol.

> CRR has seven places where it says two things at once. Pick one in each, write it down, then test.

## 3. The studies

- **H-CUT prereg** on systems with their own events (spikes, slips, R-peaks) under the causal phase,
  with its own gate. If the own event sits at the extremum, H-CUT is empty and A3 reduces to "cut at
  the event".
- **A8 with the geyser clause.** State "the content of the next occasion may be fixed by the settled
  past; its clock is not" and pre-register it on a carrier with own events absent from SEEN.md. This
  is the first version of the open-future axiom with a falsifier.
- **EQ2R2.** A new study id, the corrected scorer with its smoke mode run and committed before the
  hash, the EQ2R rows and the CC-1..3 compute rows re-registered, on carriers still unseen; and a
  decision on item 5 above before the hash.
- **L5x** on unseen data (Marone-lab experiments other than p4581; Autonomic Aging 0061–0120) under
  the causal instrument, with the amplitude control scored per unit as the batteries now do.
- **T1x** once the byte-level and GPT-2-class models are recreated and frozen; E_old is required.
- **The expert protocol** on the two candidates and the Kovacs counter-case (note
  `docs/notes/2026-09-17_synthesis_class.md` §4), with a named expert and the three questions on the
  record.

> Run the real bets again with the non-peeking machine, and ask an expert about the two guesses.

## 4. Anchoring

No PASS-1 is reachable from this environment (OpenTimestamps unreachable, tag push refused). The
two-person protocol in `docs/ROADMAP_2026-Q4.md` §1.2, with Daniel stamping the hash before data, is
the only route, and it should be in place before EQ2R2's hash.

## 5. What would count as CRR's metaphysics being found

A comparative prediction of C6, pre-registered on unseen data under the causal instrument, surviving
its sensitivity sweep with no control violated and no reduction to a constant, strongly anchored, and
replicated on a second carrier on a later day: a PASS-2. That would be evidence that a system keeps
CRR's clock rather than merely admitting its geometry. Nothing less should be quoted as a finding,
and until then the honest sentence is the one in file 04 §3.

> The only thing that would show CRR is right about the world is winning the same bet twice, in
> advance, with a machine that does not peek and a witness who sealed the envelope. We are not
> there. We now know exactly what "there" is.
