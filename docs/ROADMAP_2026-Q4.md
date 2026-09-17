# Roadmap, 2026 Q4 — broadening CRR under the protocol

Written 2026-09-17 at the owner's direction (prompt-log entry 38) after the owner's conversation
with Daniel Friedman. Purpose: make the repository ready for HumLab and for Daniel's cognitive-
security audit while broadening the framework across systems. Nothing here is a result. Every
item below ends in a ledger row or in a gate table, or it does not happen.

## 0. Terminology, fixed now

- **Confirmatory** is reserved by R11 for a study on *seen* data. Cross-system checks are
  **retrodictive** and are graded (SHARP / CONSIST / DESCR / FAILS / TENSION / OPEN), never
  called confirmations. Three batteries agree there is no SHARP row; the useful product of
  retrodiction is the CONSIST rows (what CRR *reads* correctly) and the FAILS rows (what it must
  stop claiming), not a count of agreements.
- **Implication** means a statement of the form "if CRR's reading of system X is adopted, the
  quantity Y becomes a prospective, comparative prediction with an error distribution" (v3.1 A8).
  An implication is worth writing only if it names the study that would score it.
- **Applied use case** means a carrier where a CRR quantity would be *used* (to schedule, to
  weight, to forecast) and where the comparison against the conventional quantity can be
  pre-registered.

## 1. Repository readiness for HumLab (audit-proof first)

1. **Theory v3.2, owner-signed.** Carry the external specification's additions (T4 `S = 2B`,
   T5 log-odds law, T6 tail law, A4 depth-one gate, content ≠ surplus), drop κ from A6, and
   resolve the naming collision: "equanimity" for the occasion-weight law, "normalised penalty
   step" for the gradient rule (`theory/SPEC_RECONCILIATION.md` §2–§4). Until v3.2 is signed,
   every prereg that tests a spec clause names its source, as EQ2 and SAL did.
2. **Anchoring by a second person.** This environment cannot reach OpenTimestamps and cannot
   push tags. Proposed two-person protocol: the agent hashes and pushes `HASH.txt`; Daniel runs
   `ots stamp` on it from his machine and commits the `.ots`; only then does the agent fetch
   data. That makes future rows *strongly* anchored. For the five existing studies Daniel's
   stamp would be a later time and the rows stay "weakly anchored"; say so.
3. **Both sides of the notebook.** `notebook/PROMPT_LOG.md` (human, R13) and
   `notebook/AGENT_LOG.md` (agent decisions: observed issue, decision, alternative rejected)
   are the chain of thought the audit reads the curated layer against. Proposed rule for the
   owner to add to CLAUDE.md §1 as R14: every decision that changes an instrument, a control,
   an operationalisation or a study's scope gets an entry in the same commit.
4. **Reproduction on the day.** CI runs tests, both math-check scripts, seven gates and pins
   three battery outputs. Add: a nightly re-run of every `runs/<study>/frozen/*_score.py score`
   against the committed results (byte-identical), and a runbook line per study saying which
   Python patch version produced it.
5. **HumLab entry points.** A top-level reading order for a new auditor: CLAUDE.md → CRR.md →
   ledger → reports → gate tables → notebooks. `docs/README.md` carries it; nothing else is
   needed, and no summary of "findings" is written (§9).

## 2. Retrodiction across more systems: what is worth adding

The batteries cover 32 + 40 systems, 15 re-derived external claims, 19 biological, 12 E-I and 9
driven-system rows. Adding rows has value only where a class is thin or a claim is untested:

- **Point processes with events the system owns** (neuronal spike trains, stick-slip, glitches,
  epidemics): the one class where A3/D5 and H-L5 have content. Each new row should compute the
  L5 statistic on a published record and grade it, so the battery becomes a map of which
  systems are clock-regular and which are arc-regular. Measles and the pendulum are the first
  two entries in the clock-regular column; none is yet in the other.
- **Thermal systems with a measured protocol**: answered on a model (driven-systems battery row
  9): on a two-parameter trap protocol S does not order the excess work, the speed profile in the
  friction metric does, and the friction metric is not the Fisher metric up to a scalar. No
  real-data row is needed for this question.
- **Multi-occasion systems where influence is measured, not imposed**: this is the only place
  the spec's T5 can be tested. The first such row (driven-systems battery row 5, a Preisach
  hysteresis ensemble) FAILS the law: influence is 1 or 0 by wiping-out, not e^{S}. A T5 prereg
  must first state the memory class the law excludes. Candidates: human motor adaptation
  with block-wise interference measured (the spec's §XV, re-run under the protocol),
  ecological or epidemiological systems with recorded successive outbreaks and a measurable
  effect of each on the next.

- **E-I networks**: closed as a retrodiction target (0 of 11 rows reach a known result;
  `theory/retrodictions/README.md`). The only prospective item is the T5-type experiment on
  block-wise interference; Tucker and Luu's full texts are still to be read (abstracts only here).

Not worth adding: more occupancy, quantum or gravitational rows (the batteries have shown
their content is definitional), and anything Markov in its present state (A4).

## 3. Studies, in order of value per unit of protocol cost

| # | study | question | carrier | gate | who |
|---|---|---|---|---|---|
| 1 | **EQ3** | does the normalised penalty step survive on image streams with the cap as a primary axis, DER++ only where load-bearing | Mammoth EWC-online, Split-CIFAR-100, Split-TinyImageNet, a third stream | `gate_EQ2` (open) | Daniel (GPU, anchored) |
| 2 | **L5x** | is any system arc-regular by its own physics | Marone-lab stick-slip other than p4581; Autonomic Aging 0061–0120 (CARD) | `gate_L5`, `gate_L5R` (open) | agent (data download blocked for PhysioNet; owner upload) |
| 3 | **T1x** | does path length beat the *old-probe* endpoint with lr controlled | recreate `lm_bench.py`; GPT-2-small class model | `gate_T1` (open) | Daniel (GPU) |
| 4 | **F1** | comparative forecasting: quota-forecaster error vs clock forecaster (A8 v3.1) | S-A′/S-G2 positive, S-A″/S-G negative; then stick-slip | `gate_F` (to build) | agent |
| 5 | **T5** | the occasion-weight law on a carrier where influence is measured | to be chosen with Daniel (§2, third bullet) | new gate: log-odds slope 1 by construction (must pass) and a Markov surrogate (must predict nothing) | owner + Daniel |

Retired unless re-opened by a new gate: Ω = 1 as a peak (three studies show a plateau);
criticality claims (class-dependent, batteries); salience-weighted replay (SAL-A).

## 4. Applied use cases to write up as implications (each names its study)

- **Continual learning.** A tuning-free way of running a Fisher penalty above the fixed-λ
  stability edge (EQ2-1, fragile). Use case: replacing EWC's λ. Study that scores it: EQ3.
- **Natural-time monitoring.** Where a system is arc-regular, arc since the last event is a
  better clock than time for scheduling the next observation. Use case: adaptive sampling of
  slow-slip or stick-slip records. Study: L5x, then F1.
- **Protocol design.** Constant-Fisher-speed protocols minimise dissipation (CONSIST,
  inherited). Use case: none that is CRR's rather than Crooks's; say so.
- **Memory weighting.** The occasion-weight law, if it survives T5, gives a hyperparameter-free
  salience for reweighting settled records (replay buffers, case libraries, retrieval). Study:
  T5. Until then it is not a use case.

## 5. What "careful" means operationally, restated

Gate before prereg; prereg, hash and anchor before data; one run, one rerun, `cmp`; per-unit
rows, never medians; every control violated is the first line of the report; every number in a
report exists in `runs/`; every prompt and every decision in the notebook; nothing on GitHub
that quotes anything but the ledger. Daniel's audit re-runs all of it, and the repository should
make that a single command (`scripts/check_all.sh`).
