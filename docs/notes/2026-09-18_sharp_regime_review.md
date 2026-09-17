# Review of the SHARP regime and of what a CRR PASS should mean

Written 2026-09-18 at the owner's direction (prompt-log entry 55) for Daniel Friedman's review.
Everything quoted below is in a committed, script-printed file: the retrodiction outputs under
`theory/retrodictions/*.txt` and `runs/phaseA/crr_retrodictions.txt`, the ledger `ledger/LEDGER.md`,
the gate tables `runs/phaseA/gate_*.txt`, and the notebooks. No number here comes from anywhere
else. Sections 1–4 are the full argument; section 5 says the same thing in plain language; section 6
lists what Daniel is asked to decide.

## 0. What was checked

| source | rows | SHARP | CONSIST | DESCR | FAILS | TENSION | OPEN |
|---|---|---|---|---|---|---|---|
| main battery (issue #21) | 32 | 0 | 10 | 10 | 6 | 1 | 5 |
| Daniel's battery (PR #24, pinned by verdict) | 40 | 0 | 14 | 8 | 2 | 5 | 11 |
| external "SHARP" claims re-derived | 15 | 0 | 6 | 5 | 4 | 0 | 0 |
| biological | 19 | 0 | 4 | 6 | 1 | 0 | 8 |
| E-I networks | 12 | 0 | 0 | 5 | 2 | 1 | 4 |
| driven systems | 9 | 0 | 0 | 6 | 1 | 0 | 2 |
| cognitive / collective | 9 | 0 | 2 | 5 | 1 | 1 | 0 |
| wild systems | 8 | 0 | 0 | 4 | 2 | 0 | 2 |
| twenty systems | 20 | 0 | 1 | 12 | 1 | 0 | 6 |
| emptiness (CRR at zero) | 13 | 0 | 0 | 11 | 0 | 1 | 1 |
| **all** | **177** | **0** | **37** | **72** | **20** | **9** | **39** |

The ledger holds one pre-registered PASS on unseen data, EQ2-1, and its own row says what it is:
"**PASS, FRAGILE**: the 'not behind' reading flips in 6 of 27 sensitivity cells ... the pass exists
only with cap = 1e4 (registered)", with the companion control row EQ2-4 "**VIOLATED** by DER++".
There is no SHARP row anywhere. The external document that reported 16 SHARP rows was re-derived
in `sharp_claims.py` and produced 0.

## 1. Why SHARP, as defined, cannot be reached (and why that is an unfairness, not a triumph)

SHARP is defined in the main battery as "the axioms force the known result with no outside
constant". Three features of CRR v3.1 make that unreachable by construction, not by failure:

1. **Every coherence integral has a system-supplied velocity.** Each row records FLOW: what supplies
   ẋ inside C = ∫√(ẋᵀgẋ)dt. In 177 rows the framework supplied it in none. A quantity whose
   integrand comes from the domain cannot force a domain number without an outside constant.
2. **Every unit is the system's own.** A1′ defines σ as a resolvable step of the system's own
   change, estimated from its residuals. A derived number is therefore always "in units the system
   set", which is an outside constant by the SHARP definition.
3. **The theory's content is comparative.** v3.1's four hypotheses (H-CUT, H-L5, H-T1, H-EQ) are all
   of the form "a CRR quantity beats a conventional quantity at predicting something the system
   does". A comparison cannot be a SHARP retrodiction; it is a prospective PASS or FAIL.

So the SHARP grade does not discriminate between a framework with content and one without: both
score 0. Worse, an unreachable top grade shifts the reader's attention to the next grade down, and
CONSIST then looks like the achievement. That is the epistemic unfairness in the current regime:
it cannot reward anything, and it silently promotes something that is not evidence.

## 2. What CONSIST actually contains

Of the 37 CONSIST rows, the great majority are inherited identities: thermodynamic length is the
Fisher arc on a thermal family (Crooks, Sivak–Crooks, Salamon–Nulton), the qubit's half-turn is the
orthogonal state, the Kalman gain is a function of the noise ratio, replicator dynamics is a
gradient flow in the Shahshahani metric. These agree because CRR borrowed the geometry that already
produced them. They are correct readings and they carry no risk.

Three CONSIST rows are of a different kind, and they are the only ones with prospective content:
the bacterial adder (biological row 13), the rock–paper–scissors heteroclinic cycle (cognitive row
8) and FitzHugh–Nagumo under varying drive (biological row 2). In each, the arc between the
system's own events is more regular than the clock **by the system's dynamics**, not by a threshold
that fixes the chord by construction. Each names a real-data study that could fail.

Two batteries also show CONSIST being *lost* under stricter controls: the integrate-and-fire row
went from CONSIST to OPEN when the reset jump was removed from the arc (AGENT_LOG 18), and the
diffusion-carrier theorem (cognitive row 1) shows that every arc-versus-clock tie on a noisy
one-dimensional carrier was the clock compared with itself. CONSIST is therefore not a stable
count; it falls as the pipeline tightens.

## 3. Proposed modification of the retrodiction regime

**3.1 Retire SHARP for retrodictions.** Replace the single ladder with two orthogonal labels per
row, both mechanical:

- *Kind* (what the row can be): **DEF** (a definition, symmetry or carrier fact; issue rule 3),
  **INHERITED** (the domain's law re-expressed in Fisher units; the constant is the domain's),
  **CLASS** (the framework names a class such as arc-regular / clock-regular, recency / wiping-out /
  primacy / window / power-law; the system's membership is empirical), **COMPARATIVE** (a CRR
  quantity against a conventional one on a stated target).
- *Outcome*: **AGREES**, **DISAGREES** (the present FAILS, with rule 4's "not universal" kept as the
  reason), **SILENT** (the present OPEN), **INTERNAL** (the present TENSION).

Under this scheme the present 37 CONSIST split into INHERITED-AGREES (most) and CLASS-AGREES
(the three dynamical arc-regular rows), and the reader can no longer mistake the first for the
second.

**3.2 Add one label that replaces SHARP's intended function: PROSPECTIVE CANDIDATE (PC).** A row
earns PC, and nothing more, when all five hold:

1. it is COMPARATIVE or CLASS with a named conventional baseline that can win (R7);
2. the hypothesis it would test has a gate that reads OPEN on the current instrument (R4), with a
   positive control that passes and negative controls that fail;
3. it names a real-data carrier absent from `data/SEEN.md` (R11) and, on a noisy carrier, a
   smoothing scale or a rectifiable Fisher-native carrier (the diffusion theorem) and a segmentation
   rule for reset jumps (AGENT_LOG 18);
4. its threshold is no finer than one resolvable step and is stated before the data (R5, R2);
5. its reading convention is fixed: a tie below 1e-3, a margin below 0.01 not a reading, per-unit
   scoring with the paired bootstrap (R6).

A PC is a ticket to a prereg. It is not a result and it is not evidence. Today the rows that would
earn it are the adder (single-cell growth data), the heteroclinic cycle (a population with recorded
strategy frequencies) and the normalised step on image streams (EQ3).

**3.3 Keep FAILS and TENSION exactly as they are.** They are the information the batteries produce:
every v3.1 hypothesis and the regeneration axiom A6 now has a model system on which it fails as a
universal (H-L5: measles and the diffusion theorem; H-EQ: EQX; H-T1: the old-probe endpoint;
H-CUT: phase precession; A6: variable-threshold reservoirs, counting caches), and the two laws
called "equanimity" disagree on one Gaussian update.

## 4. What a CRR PASS on a system should mean (the ledger side)

The ledger already scores PASS/FAIL per pre-registered prediction. The proposal is to grade the
PASS itself, because EQ2-1 shows a PASS can be true and still not be a result. Three levels:

**PASS-0 (provisional).** All of R2–R9 satisfied as written: hash and anchor before data; gate OPEN;
unseen data; strongest baseline and the reduction-to-constant test; per-unit criterion with the
bootstrap CI excluding zero; byte-identical rerun. EQ2-1 is a PASS-0 and no more, because it is
fragile (6 of 27 cells flip) and a pre-registered control was violated.

**PASS-1 (a result).** PASS-0 plus: the sensitivity table flips in at most one cell; no
pre-registered control violated; the rule does not reduce to a constant; the anchor is strong
(OpenTimestamps proof, or the two-person protocol in `docs/ROADMAP_2026-Q4.md` §1.2 where Daniel
stamps the hash before data); the carrier passes the admissibility rules of 3.2(3).

**PASS-2 (a replicated result).** PASS-1 plus replication on a second unseen carrier under a fresh
prereg on a later day (R3), or by a second person on a second machine with the same frozen scripts,
with both ledger rows referencing each other. Only a PASS-2 may be quoted outside the ledger as a
finding.

Two further rules follow from this session and should be added to CLAUDE.md §1 if Daniel agrees:

- **R14 (agent ledger).** Every decision that changes an instrument, a control, an operationalisation,
  a registered parameter or a verdict's wording gets an AGENT_LOG entry in the same commit
  (observed issue → decision → alternative rejected). Entries 1–24 exist; the rule does not yet.
- **R15 (numbers before words).** A verdict is computed from its numbers by the script, never
  written and then checked. Four batteries in this session had rows whose first text contradicted
  their numbers (AGENT_LOG 15, 17, 20, 21, 22, 23); in every case the model or estimator was
  corrected and the text regenerated. The rule makes that the only permitted repair.

## 5. The same thing in plain language

**What SHARP asks for.** "The theory alone predicts a number the field already measured, with no
knob to turn." CRR cannot do this, ever, because all its numbers are built from two things the
system hands it: how fast the system moves, and how big one step of that movement is. So SHARP is
a test no version of CRR could pass, which means scoring 0 on it tells us nothing. A grade that
nothing can reach is not a fair grade; it just makes the next grade look like a win.

**What CONSIST has been.** Mostly "CRR agrees with a law that the geometry it borrowed already
gave". Those rows are correct, and they are not evidence, because they could not have come out
otherwise. A few rows are different: a bacterium that divides after adding a fixed volume, and a
population cycling between three strategies, keep CRR's kind of time (distance travelled) more
steadily than clock time because of how they work, not because we built them that way. Those are
the rows worth betting on.

**What we propose instead.** Two plain labels for every check: *what kind of check is it* (a
definition, a borrowed law, a class the system may or may not belong to, or a real head-to-head
comparison), and *how did it come out* (agrees, disagrees, says nothing, or contradicts itself). No
top prize for retrodiction. A row that is a real comparison, has passed its fake-signal gate, names
untouched data, and states its threshold in advance gets a ticket called "prospective candidate".
The ticket buys a pre-registered test and nothing else.

**What a PASS should mean.** A pre-registered test that came out right on data nobody had opened is
a *provisional* pass. It becomes a *result* only if it survives its own sensitivity sweep, none of
its controls broke, it did not collapse into a constant, and the hash was anchored by a second
person before the data. It becomes a *finding* only when repeated on a second dataset or by a second
person. Our one pass so far is provisional: it is real, it is fragile, and one of its controls broke.

**Why this is fair.** It rewards the only thing CRR can actually do, which is beat a conventional
quantity at predicting something, and it stops counting agreement-by-construction as success. It
also makes the failure list, which is now long, the most informative part of the repository, which
is what it is.

## 6. Decisions for Daniel

1. Retire SHARP for retrodictions and adopt the two-label scheme of 3.1, or keep SHARP with the
   explicit note that no CRR row can reach it.
2. Adopt PROSPECTIVE CANDIDATE with the five conditions of 3.2, and confirm which three rows earn it
   today.
3. Adopt the PASS-0 / PASS-1 / PASS-2 grading of section 4 and re-label EQ2-1 as PASS-0 in a new
   ledger row referencing the old one (rows are never edited).
4. Approve R14 and R15 for CLAUDE.md §1.
5. Take the OpenTimestamps stamping role in the two-person anchoring protocol, so that any future
   PASS-1 is possible from this environment.
6. Decide whether the retrodiction batteries continue at all. Their remaining value is the class
   map and the failure list; both are now large, and each new battery has added FAILS and DESCR
   rows and no CONSIST of the dynamical kind since the heteroclinic cycle.
