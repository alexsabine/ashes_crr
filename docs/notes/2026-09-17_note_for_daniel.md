# Note for Daniel — 17 September 2026: what the ledger says, what "equanimity" means, and what to run next

Every number here is a ledger row or a committed script output; the file names are given.
Nothing is quoted from memory or from the playground.

## 1. Findings to date (ledger/LEDGER.md)

| study | rows | verdict, in one line |
|---|---|---|
| ARC (2026-09-14 bundle, seen data) | ARC-* | every earlier "positive" was a baseline that could not win, a boundary read in the theory's favour, or a criterion moved after the data; ARC-T1b: the old-probe endpoint predicts forgetting with R² 0.99351 |
| EQX (3 unseen PMLB streams, replay) | EQX-1…5 | the rule reduces to a fixed replay weight; behind the best constant on 3/3; never ahead of ER-sum by a step; Euclidean beats Fisher |
| MEAS2 (17 English cities, measles) | MEAS2-1…3 | H-L5 FAILS 0/17 under both metrics; measles is clock-regular |
| EQ2 (3 unseen PMLB streams, online-EWC past term) | EQ2-0…8, EQ2-S | EQ2-1 PASS on 3/3 (+3.30, +2.10, +2.78 pt over the tuned λ) and the rule does **not** reduce to a constant; but FRAGILE (6/27 sensitivity cells flip, all where the cap is below the tuned λ), control EQ2-4 VIOLATED by DER++ on 2/3, SI/MAS do not miss, Ω a plateau (best 0.5 / 2.0 / 1.41) |
| CARD | prereg only | awaiting PhysioNet records 0061–0090 |

All rows are weakly anchored (OTS unreachable here; push timestamps only). Phase A now has
seven gates open (`runs/phaseA/`), including `gate_EQ2` with the nonconvex positive control
that replaced the convex one your PR #23 showed cannot open.

## 2. What the equanimity rule is doing, in plain terms

A model learning something new is a wagon pulled by two kids. The New kid pulls toward the
new task; the Old kid pulls toward what the model already knows. Every continual-learning
method adds the two pulls with a hand-set weight on the Old kid.

The rule tested in EQX and EQ2 says: at every step, make the Old kid's pull the same *length*
as the New kid's. Written out, the Old contribution is Ω × (length of the New pull) ×
(direction of the Old pull). That is the whole content: a step in the Old direction whose
length is always the New step's length. Ω = 1 means "the same length".

What the ledger says that does:

- **When the Old pull is already the same kind of thing as the New pull** (replaying old
  examples through the same loss), it does nothing: the rule computes a constant and a
  hand-set constant is at least as good (EQX; EQ2-3).
- **When the Old pull is an EWC penalty** (a spring back to the old weights, stiffness set by
  the Fisher information), it helps, and not because it picks the right stiffness once. Each
  carrier has a stiffness beyond which fixed EWC diverges; the rule runs *above* that edge
  because its step can never be longer than the New step. It is a normalised-gradient method,
  and it needs its cap: with the cap below the tuned stiffness it is just a weaker constant
  (EQ2-2, EQ2-S).
- **What it is not:** it is not the spec's equanimity law. The specification you now have in
  `theory/external/` (and the text of issue #21) defines equanimity as Ω = 1 in the *occasion
  weights* π ∝ e^{S/Ω}, "equal precision, never a ratio of pull magnitudes". The rule in the
  ledger is a ratio of pull magnitudes, and its pass lives in the regime the spec calls
  ill-posed (the past pull near zero, the ratio near its cap). Two laws share one name
  (`theory/SPEC_RECONCILIATION.md` §4; retrodiction row 16, graded TENSION).

## 3. The GPT-6 specification, absorbed

- Stored verbatim: `theory/external/CRR_test_specification_GPT6_Astra_2026-09-16.md`.
- Every [T] item verified: `theory/checks/verify_spec_math.py` → `verify_spec_math.txt`, all
  PASS, each tagged inherited / same as v3.1 / new / conflict.
- Reconciled clause by clause: `theory/SPEC_RECONCILIATION.md`. Same core as v3.1; adds
  S = 2B, the pairwise log-odds law T5, the tail law T6, the depth-one gate A4, content ≠
  surplus; removes clauses v3.1 mostly does not make (the one it does: κ in A6); one conflict
  (§2 above). Nothing in CRR.md changed; that is the owner's signature.

## 4. The retrodiction battery (issue #21), run

`theory/retrodictions/crr_retrodictions.py` → `crr_retrodictions.txt`, 32 systems, 8 classes:
**0 SHARP, 10 CONSIST, 10 DESCR, 6 FAILS, 1 TENSION, 5 OPEN.** Every row borrows its metric
from the domain; in 25 of 32 the velocity inside the coherence integral is the system's own
dynamics. The reading is in `theory/retrodictions/README.md`. Short form: on known systems
CRR reads the domain's own laws as arc lengths and forces nothing; the six FAILS are universal
claims of the older text (Bernoulli antipode, mixed states, criticality, memory depth) plus
the slogan "change has its own clock"; the gravitational class has no content; the one place
CRR could be sharp (the log-odds law) has no known system to retrodict.

## 5. Tests worth running next, in order

1. **Rename before testing.** Owner decision: "equanimity" goes to the occasion-weight law
   (T5); the gradient rule becomes "normalised penalty step" and keeps its ledger. A v3.2 that
   also drops κ from A6 and adds T4/T5/T6/A4 from the spec.
2. **EQ3 on your machine (the anchored version of EQ2).** Same prereg shape as issue #20 with
   three changes the ledger forces: the cap is the named mechanism and is swept as a primary
   axis, not a sensitivity cell; DER++ enters only where α is load-bearing (a carrier where its
   grid moves accuracy by more than a step), else it is not a control; SI/MAS are dropped from
   the mechanism statement. Mammoth EWC-online on Split-CIFAR-100, Split-TinyImageNet and a
   third stream; OTS-anchored. Outcome named: a pass there is the first strongly anchored row.
3. **T5, the first test of the spec's equanimity law.** Needs a system with several admissible
   past occasions, an independent content map, and recency fixed or cancelled by equal-age
   design. The gate first: a surrogate where log(π_i/π_j) = S_i − S_j must hold by construction
   and a Markov surrogate (depth one, A4) where it must predict nothing. Candidate carriers:
   the visuomotor-adaptation data the spec's §XV mentions, re-run under the protocol; a
   replay learner whose buffer entries are occasions with measured S and whose retrieval
   weights are observable.
4. **H-L5 on a system in the other class.** Measles and the pendulum are clock-regular. The
   claim needs a carrier that is arc-regular by its own physics (period set by threshold
   crossing under a variable charging rate: stick-slip at several normal stresses, the
   Marone-lab experiments other than p4581 named in CLAUDE.md §4), or it is retired.
5. **CARD** as pre-registered, once the PhysioNet records arrive.
6. **Not worth running:** any further test of Ω = 1 as a peak (three studies show a plateau);
   any criticality claim (the battery shows class dependence); anything on a system whose
   present state screens off its past.

## 6. Questions

1. Do you accept the rename in §5.1, or would you keep "equanimity" for the gradient rule and
   give the log-odds law a new name?
2. For EQ3, is a cap-sweep as a primary axis acceptable to you as auditor, given that the cap
   is where the mechanism lives, or does that read as tuning?
3. Which system do you trust for a first T5 test?
