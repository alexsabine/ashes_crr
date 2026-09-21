# 03 — A fair review of everything the repository has found

Sources: `ledger/LEDGER.md` (the curated table), the pinned battery outputs under
`theory/retrodictions/`, the gate outputs under `runs/phaseA/`, `notebook/AGENT_LOG.md`, and
`docs/pedagogy/ELEGANCE_LEDGER.md`. Counts of rows and grades were tallied from those files in the
scratchpad and are stated as counts, not as results. Each section ends with a fifth-grader line.

## 1. The ledger: pre-registered predictions on data

| study | data | what it asked | what it found |
|---|---|---|---|
| ARC | seen bundle, recomputed | H-T1: forgetting tracks path, not endpoint | the old-probe endpoint predicts forgetting with R² 0.99351 (ARC-T1b): the path beat the wrong endpoint |
| EQX | three unseen PMLB streams, replay | H-EQ: Ω = 1 beats ER-sum and the best fixed weight | reduces to a fixed replay weight on 3/3 (EQX-1); never ahead of ER-sum by a step (EQX-3); the Euclidean ratio beats the Fisher ratio on 3/3 (EQX-4) |
| MEAS, MEAS2 | 17 English cities, measles | H-L5 on a Poisson-rate carrier | 0/17 cities pass under either metric (MEAS2-1, MEAS2-2); not fragile |
| EQ2 | three unseen PMLB streams, online-EWC penalty | H-EQ2: Ω = 1 not behind the tuned λ, no single λ transfers | ahead on 3/3 (+3.30, +2.10, +2.78); **PASS-0**: flips in 6/27 sensitivity cells, DER++ control violated (EQ2-4), Ω a plateau over 0.5–1.41 (EQ2-6), weak anchor (EQ2-1b) |
| SAL-A | surrogates only | the surplus-weight law as salience-weighted replay | gate CLOSED: no λ on the grid helps the positive control |
| EQ2R, EQ2R-CC | three unseen PMLB carriers | replication of EQ2-1b; compute-cost rows | **VOID**: the frozen scorer crashed at the first DER++ arm on every carrier; no row scored; carriers now seen (EQ2R-VOID, CC-VOID) |

No hypothesis has a PASS above provisional. The one PASS-0 is a normaliser for a penalty weight,
useful and fragile, with the value of Ω undetermined by the data.

> We made six real bets in advance on data nobody had opened. Five lost or were called off; one
> half-won, and even that one we cannot yet repeat.

## 2. The gates: can the instrument see the effect at all?

L5, CUT, T1, EQ2 and the A3 diagnostic read GATE OPEN on the standing outputs: the instrument
separates a signal built to have the effect from one built not to. SAL is CLOSED. The synthesis
class carries its own gate (positive control ADDS, decoy WRONG, negative WRONG; synthesis rows 1–2).
Two instrument findings were recorded and not repaired, because the constants are registered in
frozen preregs: the unit estimator's detrender leverage lowers the unit by 0.8629 at the registered
window, inflating every reported ρ by 1.1589 (AGENT_LOG 30); and both the cut and the unit are
two-sided operators (file 01).

> The measuring tools work on practice signals, but two of them peek at the future and one reads
> a little small. We wrote that down instead of quietly fixing it, because the tools were sealed.

## 3. The retrodiction batteries: 197 rows

Eleven standard batteries (157 rows) plus Daniel's battery (40 rows), across the fields listed in
`theory/retrodictions/README.md`. Grades summed: 41 CONSIST, 86 DESCR, 20 FAILS, 9 TENSION, 41 OPEN.
No SHARP anywhere, and the review of 2026-09-18 retired SHARP for retrodictions because every
coherence integral has a system-supplied velocity and every unit is the system's own. Three rows
were then thought to be "dynamical" CONSIST (the heteroclinic cycle, FitzHugh–Nagumo, the adder); the
synthesis re-reads found all three to be geometry (synthesis row 7; batch 11 row 4; batch 13 row 1).

Corrections to the batteries recorded in the agent log, with pinned outputs never edited:
the forced-SIR event rule (15), the E-I models (17), the reset-jump segmentation (18), the driven,
cognitive, wild and twenty-systems first runs (20–23), the trap-protocol known line (31), the AIMD
and OFC class verdicts (41, 45), the circadian typed zero (46), the Elo comparison across realisations
(51), the Clarke–Barron unit (52), the area-spectrum asymptote (48), Daniel's rows h2 and h3 (37).

> We checked CRR's arithmetic against about two hundred known results. It agreed a lot, disagreed
> sometimes, and we found and wrote down fourteen places where our own earlier checks had been
> sloppy.

## 4. The synthesis class: 138 runs

Eleven rows in the first battery (0 ADDS on nine real domains, 1 PROPOSES) and 127 re-reads of every
CONSIST and DESCR row:

**2 ADDS (candidates) / 0 PROPOSES / 34 REDUNDANT-IG / 50 REDUNDANT-DOMAIN / 17 WRONG / 21 INTERNAL /
3 UNSTATED.**

- The 84 redundant rows say the breadth of CRR's agreement is the breadth of information geometry
  (34 rows) and of the domains' own theorems (50).
- The 17 WRONG rows cluster on A6 read as a rule, H-CUT's antipode where the domain has an extremum,
  the constant-Fisher-speed protocol wherever friction is not Fisher times a scalar, H-L5 where the
  amplitude control is the arc, and path-versus-endpoint wherever the domain's state variable is the
  endpoint.
- The 21 INTERNAL rows are the v3.2 decision list (file 05).
- The 2 candidates (alternans, batch 12 row 2; Bass, batch 17 row 1) share one shape, an exponential
  memory kernel inside a domain's own map; the Kovacs row (batch 19 row 3) is the counter-case; both
  await the expert protocol.
- The 3 UNSTATED rows (the empty occasion, the sparse count carrier, the binary symmetric channel)
  are honest silences.

> We then asked a harder question of every place CRR agreed: did CRR add anything the field did not
> have? In 84 places, no. In 17 it was wrong. In 21 CRR had not decided what it meant. In 2 it made a
> guess worth showing an expert.

## 5. What is genuinely to CRR's credit

A fair review lists these plainly.

- It produced 17 definite falsifications and 21 decision points from a metaphysics. Most process
  metaphysics produces neither.
- Its one provisional pass (EQ2-1) is a real engineering observation: a gradient-normalised penalty
  weight that transfers across carriers whose tuned weights differ 47-fold, at a computed fraction
  0.0588 of the tuning compute on seen data (EQ2R-CC dry run, context only).
- The class map is real: which systems are arc-regular, and why (geometry of monotone occasions;
  the refill rate; the drive), is now a computed table rather than a slogan.
- The elegance ledger's 92 entries show the pictures carry, which is the pedagogical claim the owner
  made; the ledger also says, on each, whose picture it is.
- The pipeline held. Every number quoted anywhere reproduces byte for byte; every correction is on
  the record; the void study is a void study.

> CRR has not won a bet yet, but it has been an unusually honest player: it said things clear
> enough to be wrong, and we wrote down every time it was.

## 6. What is not to its credit, said once

- The two motivating results (L5 on p4581, T1 on the toy LM) are context, not evidence, and the T1
  recomputation showed the path beat the wrong endpoint.
- "Consistent in fifty fields" is the consistency of a borrowed geometry.
- The tensed axioms were operationalised with tenseless tools.
- The value Ω = 1 has done no work that 0.7 or 1.4 would not.
- The one replication attempted was voided by an untested script edit.
