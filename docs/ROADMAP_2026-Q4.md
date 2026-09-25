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
3. **Accepted 2026-09-18:** R14 (agent ledger) and R15 (numbers before words) are in CLAUDE.md §1;
   PASS-0/1/2 levels are in §7; EQ2-1 is re-labelled PASS-0 (ledger EQ2-1b); SHARP is retired
   for retrodictions. Study EQ2R (below) was the first replication attempt under PASS-2; it is VOID (ledger EQ2R-VOID, AGENT_LOG 40: the frozen scorer crashed at its first DER++ arm), and a replication needs a new study id on carriers still unseen.
3a. **EQ3 (2026-09-22, ledger EQ3-0…P, EQ2-1c):** the replication on six unseen PMLB streams fails on
   1/6 (fars, a degenerate carrier under the pre-registered subsample) and holds on 5/6; both controls are
   violated; Ω is a plateau over the whole nine-point grid; the mathematics (theory/checks/omega_sweeps.py)
   says why. EQ2-1b stays PASS-0 with the failed replication recorded. No further Ω study is planned.
3b. **Both sides of the notebook.** `notebook/PROMPT_LOG.md` (human, R13) and
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

3b. **EQ4 (pre-registered 2026-09-22, `prereg/eq4/`; data on or after 2026-09-23 under R3):** the bounded rule EQ-B
(present gradient clipped at κ × the largest kept recent length, then the equanimity ratio; `theory/checks/omega_reprocessed.py`,
gates EQB/EQBM open) beside the registered rule on six unseen PMLB carriers (satimage, segmentation, yeast, wine_quality_white,
sleep, page_blocks), with a poisoned regime whose R7 baseline is the fixed weight with the same clip, and the class-selection
rule that answers the fars defect. Rows EQ4-0…I; no row until the data day. What a PASS would mean: the enhancement is a
result at PASS-0 (anchoring); what EQ4-4 INERT would mean: the poison property is surrogate-only.

3c. **BAYES-1 (2026-09-22, `prereg/bayes1/`, hashed before data; data the same day: the rule is unchanged since EQ2 and the
scoring was defined from the mathematics, R3 statement in the prereg):** the registered rule against the exact sequential
Bayes posterior on six unseen PMLB regression streams with a whitened random-feature readout; score = distance to the posterior
in posterior-sd units; a calibration axis c ∈ {1/16, 1, 16} on the past curvature. Rows B0–B7, BS. The surrogate gate
predicts B1 PASS (the rule is not Bayes) and B2/B3 FAIL (a Bayes with the curvature wrong by 16× is closer to the posterior
than the rule; the invariance does not survive mini-batch noise). EQ-B is not in it (R3); a later day.

3d. **T1x (2026-09-22, `prereg/t1x/`, hashed before data; model (d), a numpy MLP on six unseen PMLB regression streams;
models (a)–(c) of CLAUDE.md §5 still to run):** the held-out test of H-T1 with the learning rate controlled, the old-probe
endpoint and the EWC distance as baselines, nine schedules × four lr × three seeds, held-out R². The surrogate S-H2 (path
dependent by construction) passes the gate and the synthetic MLP smoke reads FAIL (E_old at R² 0.999).
**Outcome: VOID** (ledger T1X-VOID; `reports/t1x.md`): the frozen scorer crashed on `215_2dplanes` (binary split feature)
and its `score` on `218_house_8L` (non-finite path lengths); no row scored; the six carriers SEEN.
**T1x2 (`prereg/t1x2/`, hashed 2026-09-22; data on or after 2026-09-23 under R3):** the same design with the four
corrections named in its prereg (split-feature rule, admissibility gate, bool cast, non-finite runs dropped and counted)
on six unseen carriers (three BNG sets, three Feynman sets).

3e. **FED Phase A (2026-09-22, synthetic): CLOSED.** The heterogeneous-node federated test of H-EQ sketched for
decentralised alignment does not pass its own gate: one global weight is within a step of every node's oracle, and on a
poisoned node the clip holds with a fixed weight too (`docs/notes/2026-09-22_fed_phaseA.md`). No prereg follows.

## 2. Retrodiction across more systems: what is worth adding

The batteries cover 32 + 40 systems, 15 re-derived external claims, 19 biological, 12 E-I, 9
driven-system, 9 cognitive-collective, 8 wild-system and 20 twenty-systems rows, plus a
13-row boundary battery on emptiness (CRR at zero) a 12-row battery against Shannon
information theory, an 8-row battery against loop quantum gravity and an 11-row SYNTHESIS battery
(does CRR add anything to a domain's own mathematics: 0 ADDS on nine real domains, 1 PROPOSES,
`docs/notes/2026-09-17_synthesis_class.md`), now being applied to every CONSIST/DESCR row in batches of five
(`theory/retrodictions/synthesis_batches/`, 127 rows, complete: 2 ADDS candidates / 0 PROPOSES / 34 REDUNDANT-IG / 50 REDUNDANT-DOMAIN / 17 WRONG /
21 INTERNAL / 3 UNSTATED; the SHARP review's dynamical-CONSIST list is empty; the 21 INTERNAL rows are the
v3.2 decision list; 92 elegance entries). Adding rows has value only where a class is thin or a claim is untested:

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
  hysteresis ensemble) FAILS the law: influence is 1 or 0 by wiping-out, not e^{S}; the second
  (a linear echo-state reservoir) is explained by age weights and the surplus adds 0.011 in R².
  A T5 prereg must first state the memory class the law excludes and name a system where
  neither wiping-out nor linear fading applies.
- **Diffusion carriers**: the Fisher arc of a Brownian path is not finite (cognitive-collective
  battery row 1, TENSION), so every L5-type prereg on a noisy carrier must name a smoothing
  scale or a rectifiable Fisher-native carrier before the gate; the exact ties of the Kramers
  and integrate-and-fire rows were this, not a property of those systems. Candidates: human motor adaptation
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

## Focus from 2026-09-24 (owner, prompt-log entry 150)

**The focus.** Continual learning and AI safety integrated in one system, with an explainable reason for the design:
zero stake at the cut. The design and its reasons are in `Empty_Centre/THE_EMPTY_CENTRE.md`.

**In order:**
1. SCL3 (data step 2026-09-25).
2. A positioning note for Proposition 7 against its prior art (`AI_Safety/FRONTIER_REVIEW.md` §2).
3. A declared test on language-model agents, adapting the DReST/POST protocol.
4. A declared study of shutdownability and safety retention under continual learning.

**Not the focus.** The Regeneration Law runs in parallel, out of the epistemic ladder. Falsifiable metaphysics is a
side-quest.

## Next steps as of 2026-09-24, evening (owner, prompt-log entries 159 and 162)

The review is `docs/notes/2026-09-24_empty_cut_and_cl_review.md`.

**No paid resources, in order:**
1. **Tonight.** SCL3 (00:05 UTC) and RLAW (00:40 UTC) data steps.
2. **RW2, on the owner's choice.** Either (A) a reduced real-data prereg (the empty cut during continual fine-tuning of
   Qwen2.5-0.5B-Instruct, with erosion and remedies reported without verdict), or (B) a third declared synthetic round.
3. **A positioning note for Proposition 7** against its prior art.
4. **A declared diagnosis of the rule's freeze at the anchor** (RW2 Phase A round 2).
5. **A declared synthetic holder-capacity test.**
6. **The owner's decision on re-pinning CPU-dependent outputs** (AGENT_LOG 116).

**Deferred because they cost money** (the owner, prompt-log entry 162: "I don't want to spend money at this stage"):
- **RW3: shutdown interference in capable language-model agents.**
  - Adapt the DReST/POST protocol (arXiv:2604.17502v4), comparing an objective counted on the agent's own steps.
  - Include a must-fail surrogate (a pause that loses progress) and DReST itself as the baseline.
  - It needs an Anthropic API key from the Claude Console. That is billed separately from a Claude subscription, and
    how to add one is recorded in prompt-log entry 161's reply. It also needs an agreed budget, and a declaration with a
    cost estimate approved before any call.
- **Bitwise and tolerance checks on GPUs** for the empty-cut engineering (C1–C2) and RW1. They need GPU hardware, with a
  tolerance declared before the run.

## SOTA1, planned 2026-09-25 (owner, prompt-log entry 190)

The full CRR learner on a real image benchmark, with the empty cut and equanimity. The plan is
`docs/notes/2026-09-25_sota1_plan.md`.
- **The learner:** replay, plus an equanimity-weighted anchor (or SEC, labelled as not a CRR rule), plus the own-clock
  schedule and A1′'s unit, all inside the operator harness.
- **The benchmark:** online Split-CIFAR-100 (UNSEEN), run on CPU for free. Mammoth's reference baselines are pinned at
  commit e75a491.
- **The replication:** Split-TinyImageNet under a fresh prereg, only if a row reaches PASS-1.
- **The order:** citation check, then engineering without data, then declaration and gate, then prereg, hash and
  OpenTimestamps, then the data step on a later day.
- **Deferred because it costs money:** the language-model and offline multi-epoch settings.
