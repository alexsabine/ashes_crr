# Study SAL — Phase A stops at the gate (2026-09-17)

**Study id `sal` was not pre-registered, hashed or run. Its gate reads GATE CLOSED and no
positive control could be built.** This note records why, quoting only `gate_SAL.txt` (the
committed output of `uv run python -m crr.surrogates.gate SAL`). Per CLAUDE.md R4 and R12 the
study stops here; a ledger row (`SAL-A`) records the closure.

## What was to be tested

The occasion-weight law of the external specification ([D9]/[H1]/[T5],
`theory/external/CRR_test_specification_GPT6_Astra_2026-09-16.md`; v3.1 [P2] with β fixed):
settled occasions enter regeneration with weights π_m ∝ e^{λ S_m}, λ = 1 in the per-elementary-
event Fisher unit, equal retention. Operationalised on a continual learner
(`src/crr/instrument/replay.py`): one occasion = one task; S_m = the model's own Fisher-path
surplus (D6, categorical predictives on a fixed probe, per-update unit) measured on a
replay-free shadow pass over task m from the weights at its start; replay draws a past task with
probability π_m, then a sample from that task's buffer entries; loss = CE(present) + CE(replay).
λ = 0 is uniform replay, λ = 1 the prediction, λ < 0 the anti-salience control; the spec's
three-way protocol (λ = 0 / λ = 1 / free λ on training seeds) was to be the study.

## The gate

Statistic (instrument sensitivity): some λ on the pre-registered grid {−1, −0.5, −0.25, 0, 0.1,
0.25, 0.5, 1, 2} beats λ = 0 by ≥ 1.0 accuracy point on the seed mean, positive in ≥ 4 of 5
seeds. Surrogates (all in `src/crr/surrogates/battery.py`, deterministic):

- **S-SAL-P** (MUST PASS): five tasks of unequal difficulty; surplus tracks forgetting
  (Spearman +0.83; S per task 0.15, 1.7, 0.1, 2.3, −0.07). Best λ on the grid gains +0.03
  (λ = −0.25); λ = 1 gains −0.67; λ = 2 gains −10.57. **FAIL: violates its positive-control role.**
- **S-SAL-F** (MUST FAIL): equal difficulty, flat surplus (0.19–0.37). Every λ within ±0.15 of
  λ = 0. FAIL, as required.
- **S-SAL-D** (MUST FAIL): surplus inflated by gradient noise on two tasks (5.25, 4.84 against
  0.34–0.65), decoupled from forgetting (Spearman −0.24). λ = 1 gains −15.54. FAIL, as required.

GATE CLOSED (1 violation).

## Reading

1. **The instrument sees the surplus** (the positive control's S tracks its forgetting at
   +0.83) **and the law does what it says**: at λ = 1 one Fisher unit of surplus multiplies a
   task's replay share by e, and the weights concentrate on the high-surplus tasks. What does
   not follow is a benefit: reallocating a fixed replay budget by e^{λS} never beats uniform
   replay by a resolvable step on a stream built in its favour, because starving the low-surplus
   tasks costs more than over-replaying the high-surplus ones gains. At λ = 1 the loss is
   already visible; at λ = 2 it is large. The negative controls behave, so this is not an
   instrument fault: it is the absence of an effect for the instrument to see.
2. **A first operationalisation was rejected before this one.** Measuring S_m on the live pass
   (replay included) gives a surplus that grows with the task index, so e^{S} became a recency
   kernel in disguise, which is the surplus–recency compensation the spec's Decision 10 warns
   about. The shadow measurement removes the trend; the row above uses it.
3. **What would be a different study, not a repair of this one.** The law could be
   operationalised as a weight on a per-task regulariser instead of on replay allocation, or
   with S measured on a task-specific probe, or with a smaller unit. Each of those is a new
   instrument and needs its own gate; trying them in sequence until one opens is the forking
   path the protocol exists to stop. None was tried.
4. **What the closure does and does not say.** It says that on continual learners of this
   kind, weighting replay by e^{S} does not help; it does not test the law on a system whose
   past occasions carry content that regeneration must reweight (the spec's intended domain),
   because the learner supplies no such observable. A test there needs a carrier where
   influence is measured, not imposed.

## Files

`gate_SAL.txt` (this folder), `src/crr/instrument/replay.py`, `src/crr/surrogates/battery.py`
(S-SAL-P/F/D), `src/crr/surrogates/gate.py` (`gate_SAL`), ledger row `SAL-A`.
