# The SYNTHESIS class: does CRR add anything to a domain's own mathematics?

Written 2026-09-17 (container clock) at the owner's direction (prompt-log entry 60). The owner asked for a
new epistemic status in which CRR is allowed to relate in its fullness to the mathematics it is
investigating, and the test is whether CRR adds anything to that domain: not "not borrowing", but
whether the CRR mathematics can reveal hidden structure in an existing domain. The picture given was a
domain expert (Rovelli) with CRR to hand, an LLM, and the cognitive-security protocol. This note defines
the class, the harness that implements it (`theory/retrodictions/synthesis.py`, pinned output
`synthesis.txt`), its gate, the expert protocol that closes it, and what the first battery found. Every
number below is in the pinned output. Section 5 says the same thing in plain language.

## 1. What the class is

A **SYNTHESIS** row takes the whole of CRR v3.1 (A1–A8, D1–D6, P1–P5, O1–O3, H-CUT, H-L5, H-T1, H-EQ),
integrates it with a domain's own formalism, and states **one proposition Q about the domain, in the
domain's own terms**, built with at least one *CRR-proper* ingredient. The distinction that the earlier
kind × outcome reading (`2026-09-18_sharp_regime_review.md` §3) could not make, and this class does, is
between what CRR shares with information geometry and what is CRR's own:

- **Not CRR-proper** (shared with information geometry, Čencov–Amari): A1 the Fisher–Rao metric, D2 the
  arc, D3 the chord, D4 the surplus C − C*, P1 (S ≥ 0).
- **CRR-proper**: A3 the antipodal cut and D5 occasions; A6 regeneration by a bounded Fréchet mean of
  settled occasions, "never an accumulated count"; P2/P3 occasion weights; A1′/D1 the unit as the
  system's own resolvable step and ρ; H-L5's class claim (arc-regular vs clock-regular); D6/H-T1 path
  against endpoint; H-EQ the normalised step; A7/A8 relational tense.

A row that uses no CRR-proper ingredient can be true and checkable and still add nothing (row 6 below).

## 2. The three tests and the outcome rule (all mechanical, R15)

For each row the script prints three numbers-first tests and computes the label from them:

- **T-G, ablation against the null.** The decisive quantity is computed twice: with the CRR-proper
  ingredient, and with its information-geometric or domain replacement. If the two agree within 1 %
  (relative; `TOL_G`) the ingredient did no work: **REDUNDANT-IG**.
- **T-N, novelty against the domain.** Where the domain has its own theorem for the same target, the
  script computes it. If it gives the CRR value within 1 % (`TOL_N`) the domain already has Q:
  **REDUNDANT-DOMAIN**. Where no theorem is cited, T-N passes vacuously and the row says so.
- **T-C, the check.** Q is checked in the domain's own mathematics, numerically or in closed form.
  Holds → **ADDS**; fails → **WRONG**; unavailable here (Q is about data or an unmeasured quantity) →
  **PROPOSES**.

Two further outcomes: **INTERNAL** when two readings of the CRR ingredient give different values on
the domain (the ingredient must be fixed before Q can be checked), and **UNSTATED** when no Q could be
formed at all, with the quantities that were tried printed.

**ADDS is always a candidate.** The script can establish that the ingredient did work (T-G), that the
cited theorem does not already give the value (T-N) and that Q holds (T-C). It cannot establish that
nobody in the domain has said Q. That judgement belongs to the expert protocol in §4, and the label
reads "ADDS (candidate; novelty pending domain review)" until it has been through it.

## 3. The gate (R4 for a class)

A class whose top label is unreachable is the SHARP problem again; a class whose top label is reachable
by a framework with no content is empty. So the harness carries its own gate, printed on every run:

| control | what it is | must read | reads |
|---|---|---|---|
| positive (row 1) | a synthetic event train whose cycles have equal total variation (2.0000 σ) but random height, wiggle and duration; the domain sees a renewal process with clock CV 0.144 | ADDS | ADDS (CV(C) 1.659e-13, CV(clock) 0.144, CV(amplitude) 0.164) |
| decoy (row 1) | the same signal scored by a framework whose unit is the peak-to-peak amplitude, an outside constant | not ADDS | WRONG (CV 0.164) |
| negative (row 2) | S-G, clock-regular by construction | not ADDS | WRONG (CV(C) 0.134, CV(clock) 0.000) |

GATE OPEN. The positive control is deliberately one where excursion size does not carry the structure,
so the harness cannot be satisfied by the amplitude control that H-L5 already names.

## 4. The expert protocol (the "Rovelli with CRR to hand" step)

The class is closed by a person, not by the script. A row that reads ADDS (candidate) or PROPOSES is
handed to a named domain expert together with its Q, its T-G numbers, its cited theorem and its check,
and the expert answers three fixed questions, logged verbatim with a timestamp exactly as human prompts
are (R13):

1. Is Q already known in the domain? (cite it)
2. Is Q derivable from the domain's formalism without the CRR ingredient named in the row?
3. Would Q change any calculation, model choice or experiment in the domain?

ADDS (candidate) becomes ADDS (reviewed) only on *no, no, yes*. Any other triple is recorded as the
expert's verdict beside the script's and the row is re-labelled from it: a *yes* to (1) or (2) is
REDUNDANT-DOMAIN with the expert's citation; a *no* to (3) is "ADDS, inert". The LLM's part is to form
Q and run the three tests; it never grades its own novelty, and it never fetches the expert's answer
from the literature on the expert's behalf (R10 applies to any citation it offers).

For a PROPOSES row the same three questions are asked, and a *no, no, yes* makes it a PROSPECTIVE
CANDIDATE under the earlier note's five conditions (§3.2 there): a ticket to a prereg, not a result.

## 5. What the first battery found

`synthesis.py`, eleven rows: two gate controls and nine real domains. Real-domain tally:
**0 ADDS / 1 PROPOSES / 2 REDUNDANT-IG / 2 REDUNDANT-DOMAIN / 2 WRONG / 1 INTERNAL / 1 UNSTATED.**

| row | domain | Q (short) | ingredient | outcome |
|---|---|---|---|---|
| 3 | Bayesian estimation | the state after K evidence occasions is the Fréchet mean of the per-occasion posteriors, so its spread does not shrink | A6 | WRONG: Fréchet spread 0.3833 at K = 64 vs Bayes 0.0395 |
| 4 | quantum mechanics | the occasion boundary of a unitary evolution is the first orthogonal state, at the Mandelstam–Tamm time | A3 | INTERNAL: on levels (0,1,2) the arc half-turn is at t = 1.9238 and the antipode at 2.0944; on (0,1,3) no antipode occurs (minimum overlap 0.2024) |
| 5 | signal analysis | the A3 occasion rate of a two-tone signal is twice the stronger tone's frequency, not twice the centroid | A3 | REDUNDANT-DOMAIN: rate 1.9995 = 2 f₁, the analytic-signal literature's theorem |
| 6 | evolutionary dynamics | a replicator trajectory is a Fisher–Rao geodesic iff at most two distinct fitness values | D4 (not proper) | REDUNDANT-IG: S = 6.43e-02 vs −2.56e-09, true and information geometry's |
| 7 | evolutionary dynamics | the heteroclinic RPS epochs are arc-regular (cognitive row 8 re-read) | H-L5 | REDUNDANT-IG: mean arc 3.1416 = the edge length π; the regularity is the boundary geometry |
| 8 | cell biology | an adder whose setpoint references the age-weighted Fréchet mean of past birth sizes carries a lag-2 partial autocorrelation | A6 + P3 | PROPOSES: lag-2 coefficient 0.1290 (q = 0.3), 0.1634 (q = 0.6) vs 0.0080 for the adder; needs lineage data |
| 9 | cyclic cosmology | successive cycle maxima stay bounded (seeded from the Fréchet mean, never a count) | A6 + P3 | WRONG: Tolman growth 0.9702 in ln a_max, A6 −0.0493 |
| 10 | thermal time (Rovelli) | none could be formed | D2, A7/A8 | UNSTATED: arc rate 0 on a stationary state, thermal rate 1.0000 |
| 11 | loop quantum gravity | entropy per resolvable step of horizon area is one bit | A1′/D1 | REDUNDANT-DOMAIN: ln 2 under the j = ½ counting is that counting's definition; 1.864 bits under the all-j counting |

Three things the class did on its first run that the earlier readings could not:

- **It separated a true statement from an added one.** Row 6 is correct, checkable and interesting, and
  T-G shows CRR did not add it: every symbol is information geometry's. Row 7 does the same to one of the
  three rows the SHARP review called "dynamical CONSIST": the arc per epoch settles at π to 6.54e-06
  because the attracting cycle runs the simplex's edges and every edge is a geodesic of length π. The
  CLASS-AGREES reading stands (the system is arc-regular); the synthesis reading is that the constant is
  geometry's and CRR supplied the name. The prospective-candidate list of the earlier note should read
  the adder and the normalised step, and the heteroclinic cycle only as a class example.
- **It made A6 pay.** Read as a rule about any system with occasions, the regeneration axiom is
  contradicted twice by domains that accumulate: Bayesian evidence (row 3) and Tolman's cycles (row 9).
  The axiom's own clause ("a system that re-counts its past stops cutting") is the escape, and it is a
  scope restriction: by CLAUDE.md §10 that is a new prereg, not a repair. Where A6 is integrated with a
  domain rule that does not accumulate (the adder, row 8) it produces the battery's only PROPOSES.
- **It found A3 unfixed on the one carrier where "antipode" is a domain word.** On a projective space the
  half-turn of arc and the orthogonal state are different events, and a generic spectrum never reaches
  the second. Which reading is A3 has to be decided before any quantum row can be graded, and the
  decision is a theory change (v3.2), not an estimator choice.

Nothing in the first battery reads ADDS on a real domain. That is the honest answer to the owner's
question at this point: with the tests applied, CRR's proper ingredients either restate the domain
(rows 5, 11), restate information geometry (6, 7), contradict the domain where it accumulates (3, 9),
are unfixed (4), have no purchase (10), or propose one data test (8).

## 6. The same thing in plain language

The earlier grades asked "does CRR agree with what the field already knows?" Agreement is cheap when
you borrowed the field's geometry. The owner asked a harder question: give CRR the whole of a field's
mathematics, let it use everything it has, and see whether it can say something the field could not
say without it, something true and checkable.

We built that test. Each attempt has to state one claim about the field, in the field's own language,
using a part of CRR that is not just the borrowed geometry. Three checks then run: take the CRR part
out and see whether the number changes (if not, CRR did nothing); ask whether the field's own theorem
already gives the number (if so, the field had it); check the claim in the field's own mathematics (if
it fails, CRR is wrong there). Only a claim that survives all three is a candidate for "CRR adds
something", and even then only a candidate: whether it is *new* is for a person who knows the field to
say, answering three fixed questions on the record.

We also built the two controls every test needs: a fake domain where CRR must win by construction (it
does), and a decoy framework and a fake domain where it must not (it does not).

Then we ran nine real attempts. None survived as an addition. Two showed that a true and interesting
statement was information geometry's, not CRR's. Two showed CRR's regeneration rule is wrong wherever a
field's mathematics accumulates. One showed CRR's cut is not yet a single rule in quantum mechanics.
One could say nothing about Rovelli's thermal time. One proposes a test on bacterial lineage data that
the standard model would fail and CRR's rule would pass, and that is the one thing to hand to an
expert.

## 7. Decisions for the owner and for Daniel

1. Adopt SYNTHESIS as a fourth kind beside DEF / INHERITED / CLASS / COMPARATIVE, with the seven
   outcomes and the gate as implemented (CLAUDE.md §7 now names it).
2. Adopt the expert protocol of §4, and name the first expert and the first row (row 8, the adder with
   regeneration memory).
3. Decide the A3 reading for projective carriers (row 4): arc half-turn or antipode. Until decided,
   quantum rows are INTERNAL.
4. Decide whether A6 carries a scope clause ("regenerating systems do not accumulate") as a v3.2 change
   with its own prereg, or stands as stated and is WRONG on accumulating domains.
5. Amend the prospective-candidate list of the SHARP review: remove the heteroclinic cycle (row 7),
   keep the adder, add row 8's lag-2 test as the adder's second prediction.
