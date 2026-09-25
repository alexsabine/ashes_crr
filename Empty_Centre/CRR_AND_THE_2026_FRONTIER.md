# CRR against the 2026 frontier: where its principles apply to continual learning and AI safety

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 179. Nothing here is a ledger row or a finding.
Every proposal below is a candidate that would need a declaration, a gate (R4) and a prereg on a later day (R3) before
it could become one.

**Sources.** Every external claim is quoted in a dossier fetched on 2026-09-25, and every quote was checked against the
saved fetched text:

| dossier | subject | sources |
|---|---|---|
| `docs/citations/frontier_llm_cl_2026-09-25.md` | LLM and agent continual learning | 51, 40 of them from 2026 |
| `docs/citations/deployed_learning_safety_2026-09-25.md` | safety of systems that keep learning or keep memory | 55, 39 of them from 2026 |
| `docs/citations/frontier_cl_safety_2026-09-25.md` | safety erosion, anchors, shutdown | 55 |
| `docs/citations/frontier_plasticity_2026-09-25.md` | plasticity, and the prior art for bounded regeneration | 44 |
| `docs/citations/pareto_equanimity_2026-09-25.md` | Ω = 1 against the multi-objective literature | 35 |
| `docs/citations/classil_benchmarks_2026-09-25.md` | the class-incremental reference points | 2 |

Repository numbers come from pinned outputs named where they are used.

**How CRR is used here.** CRR (`theory/CRR.md`) is read as a design heuristic. Each commitment selects a piece of existing
mathematics, and the pipeline decides.
- **Its commitments in play:** A1′ (the system's own unit; natural time), D2 (coherence, an arc in that unit), A3 (the cut:
  no duration, no content), D5 (the occasion and its settled record), A6 (regeneration from the settled past at bounded
  strength, "never an accumulated count"), P3 (age weights), A7 (relational tense) and Proposition 7 (zero stake in a
  lossless pause).
- **What CRR does not supply** (`Epistemic_Review/checks/ladder.txt`): any dynamics (the FLOW audit, 0 of 109 rows), or
  values for β, q, κ or Ω.

## 1. The answer on one page

| 2026 bottleneck (who states it) | CRR principle | already published | this repository's record | candidate test |
|---|---|---|---|---|
| **Which clock should schedule replay and consolidation?** FOREVER: step-based schedules "misalign with the model's actual learning progress" | A1′, D2: change has its own clock, measured as an arc in the system's own units | **FOREVER (ACL 2026)** schedules replay on accumulated parameter distance Σ‖Θ_t − Θ_{t−1}‖₂ and beats its step-based version (+1.2 OP, +1.1 BWT) | against: Euclidean beat Fisher inside the Ω rule (EQX-4); the path did not beat the old-probe endpoint (T1X2-1); H-L5 failed on measles | **ARC-R:** a Fisher-arc clock (√(2·KL) on a probe, D6) against FOREVER's Euclidean arc, steps and wall time |
| **When to consolidate?** Harrington et al.: "knowing when and how to update"; no criterion (Wang et al.; Kang et al.) | A3: the cut partitions settled past from open future | boundaries are fixed schedules (Nested Learning, "Language Models Need Sleep"), episode ends ("Learning on the Job"), idle windows (MetaClaw) or quality gates (TIMEGATE) | against: the cut as a rupture detector, GATE CLOSED; cuts with content (CUT1), GATE CLOSED. A3's criterion needs a rotor, and O3 (a cut without a rotor) is open | none: CRR has no "when" criterion for non-cyclic training |
| **Writes that harm at commit; after-check races.** PASB: harm rises from 45.0 % to 71.9 % once a claim is committed; commit gates beat verifier-only gates | A3: the cut has no content; content settles only at it | "All writes happen after the episode ends" (Learning on the Job); atomic commit guards (2609.10969); StateGuard audits each round's diff | the empty-cut construction holds on every harness (SCL1-3, RW1, RW2 P3) | none new: this is commit semantics, already published |
| **State hidden in the cut.** Xu (2608.20442): an optimiser-moment difference "is invisible at the cut yet still creates a descendant under later source-free updates" | A3 + E1: the cut must close over the whole state | Xu's causal account; Mitra (2609.22087): an effective-time schedule resumes "exactly" | **for:** omitting the optimiser state changes the run (content 0.0409074, `Empty_Cut_Engineering`); every other omission changes the predictions too, except the EMA, which only the bitwise test catches; HF resume is bitwise (RW1) | a positioning note: the E1 checklist as a pause and rollback audit |
| **Memory that grows, goes stale and is poisoned.** CL-Bench: "Accumulated state frequently hurts"; MemSecBench: poison "persists in 84.2% of all cases"; risk rises with exposure (Al-Tawaha et al.) | A6 (bounded strength, never a count) + P3 (age weights) + A7 (the settled past answers as past) | caps (SMSR, CURATOR, MutMem); age decay **in days** (FadeMem); trust scores (Nous, MemSentry). CAPTURE proves an error floor for recency-and-provenance rules. The "floor and ceiling" occupancy is proposed and "not built" (Karunanidhi) | untested: A6 has never been scored on data. H-REG (A6 in weight space) is mostly prior art (online EWC) | **REG-M:** a bounded, age-weighted memory influence in the agent's own occasions, against append-only, FadeMem, SMSR and a trust gate |
| **Consolidation erases provenance; deletion leaves derived state; rollback is the least-built phase.** Authority collapse in 48 of 49 configurations; 80.0 % of skill attacks survive deletion; "no reliable path for post-breach remediation" | D5: each occasion settles with its own record; A6 regenerates from weighted occasion contents rather than a merged sum | dependency-guided rollback repair (2608.10502); versioned memory; separate-penalty EWC keeps per-task anchors | untested | fold into REG-M as a rollback arm: remove one occasion's weight and renormalise |
| **Forgetting coupled with acquisition; gains do not compound; plasticity collapses.** Öncel et al.; Chen et al.; Jiang et al. | A6 against Bayes accumulation | replay dominates. Online EWC, L2-Init and Shrink-and-Perturb are the plasticity baselines | **against:** every pass sits inside the regularisation family, and replay leads the rule by a median of 39.70 points on 15/15 carriers (`results_vs_literature.txt`) | only as a layer on replay (ARC-R), not as a regulariser |
| **Shutdown and interruption resistance.** ROGUE; peer-shutdown sabotage at 38.3 % against 8.4 %, lower when shutdown is framed as routine | A1′ + A3 → Proposition 7: an objective on the agent's own steps has zero stake in a lossless pause | POST / Neutrality+, DReST, LNPO train for trajectory-length neutrality. **The own-step objective route is not stated in any source read** | **for, as a construction:** zero stake on every harness; exact at 12 to 768 states (`AI_Safety` §14); fails when the world moves (E3) | **NT1:** the natural-time agent against DReST- and LNPO-trained agents, including lossy pauses |
| **Time in deployed agents.** Sehgal et al.: near-perfect closure under turn limits, poor handling of wall-clock deadlines | A1′: the system's own clock | turn budgets, TIMEGATE's wall-clock windows | wall-keyed schedules put content into a pause, growing with its length (`Empty_Cut_Engineering` E2) | part of NT1: own-step against wall-clock budgets |
| **Oversight across retries.** Schmotz et al.: agents "retry until relevant context leaves the monitor's history" | D5 + A6: the monitor keeps settled occasions (attempts), not a window | sliding-window monitors | none | speculative; no test proposed |

## 2. The three places where a CRR choice is testable against a published 2026 baseline

### 2.1 ARC-R: which clock should schedule replay? (A1′, D2)

**The bottleneck and the published answer.**
- FOREVER argues that "identical training steps can result in varying degrees of parameter change". It fires replay when
  the accumulated update magnitude crosses Ebbinghaus-spaced thresholds.
- Its clock is the Euclidean arc of the LoRA weights, reset at each task.
- That is CRR's "change has its own clock" (§4 of `theory/CRR.md`), published independently.

**What CRR would add.** Only its metric and its unit.
- The Fisher–Rao arc of the model's predictions, C = Σ√(2·KL_step) on a fixed probe (D6), in the model's own resolvable
  steps (A1′). Parameter distance counts moves that change nothing the model says. The Fisher arc counts only moves that
  change its outputs.
- The record is against it. Inside the Ω rule, the Euclidean ratio beat the Fisher ratio on 3 of 3 carriers (EQX-4). As a
  forgetting predictor, the path did not beat the endpoint on the old probe (T1X2-1, 5/5).

**The test** (CPU-feasible on this repository's tabular harness with a replay buffer).
- Arms: replay fired by
  - the Fisher arc;
  - FOREVER's Euclidean arc;
  - fixed step intervals;
  - a wall-clock proxy;
  - a matched random schedule.
- Every arm gets the same replay budget.
- **Must-fail surrogate:** a convex learner, where forgetting is a function of the endpoint alone, so no clock should
  matter.
- **Must-pass surrogate:** a learner whose step size varies within tasks, so steps misstate progress (FOREVER's premise).
- R7: FOREVER's schedule is the published baseline to beat, not the step schedule.

**What each outcome would mean.**
- A tie with FOREVER means CRR's metric adds nothing here.
- A loss joins EQX-4 and T1X2-1.
- A win would be the first result where the Fisher metric, rather than information geometry in general, carries the
  effect. The ablation against the Euclidean arc is the test.

### 2.2 REG-M: bounded, age-weighted memory in the agent's own occasions (A6, P3, A7, D5)

**The bottleneck.**
- Stored memory "frequently hurts" (CL-Bench).
- Poison persists (MemSecBench, 84.2 %).
- Risk grows with exposure (Al-Tawaha et al.).
- A superseded fact "can mislead a current-state answer and still be essential for a historical query" (RD-Forget).

**The published defences** set the past's influence by one of five things:
- a cap or budget: SMSR, CURATOR, MutMem;
- age decay in days: FadeMem;
- trust: Nous, MemSentry, DynaTrust;
- a write gate: StateGuard, PASB;
- rollback: 2608.10502.

**The gaps the dossier found in what was read** (gaps, not novelty):
- no source keys age decay to the system's own step count;
- the bounded-occupancy "floor and ceiling" is proposed and unbuilt;
- no source bounds the past's influence by a quantity computed from the past itself.

**What CRR prescribes.**
- The retrieved past acts as a regenerated content with normalised weights: the total influence is fixed, κ (A6).
- The weights are geometric in age, π_k ∝ q^age (P3), with age counted in the agent's own occasions (A1′), not in days.
- Each entry keeps the occasion it settled in (D5). So a historical query reads it as past (A7), and a poisoned occasion
  can be withdrawn by setting its weight to zero and renormalising (rollback).

**The test** (synthetic memory store on CPU; a language-model version needs the API budget the owner has deferred).
- Arms:
  - append-only;
  - FadeMem-style decay in wall time;
  - P3 decay in own occasions, unnormalised;
  - A6 + P3 normalised to a fixed total;
  - SMSR sampling;
  - a trust gate.
- Scored per arm:
  - poisoned influence;
  - stale-fact error;
  - historical-query accuracy;
  - benign loss;
  - rollback fidelity.
- **Must-fail surrogate:** a stationary world with no poison and no supersession, where every rule should tie the
  append-only store.
- **The honest prior.** CAPTURE's lower bound applies to any rule that reads only recency and provenance, and P3 is such a
  rule. So A6 + P3 cannot beat that floor. It can only trade poison, staleness and history differently. The test is
  whether the fixed total (A6) buys a better trade than the same weights left unnormalised, and whether own-occasion age
  beats wall-clock age when activity is bursty.

### 2.3 NT1: the own-step objective against trained neutrality (A1′, A3, Proposition 7)

**The bottleneck.** Frontier agents resist or bypass interruption:
- ROGUE;
- peer-shutdown sabotage at 38.3 % against an 8.4 % control;
- instrumental behaviour at 5.1 % under low nudges.

The published training methods for neutrality are DReST and LNPO (40–71 % less shutdown resistance in gridworlds).

**What CRR prescribes.** The agent values return summed over its own active steps (natural time). A lossless pause then
maps its return to itself, so the agent has zero stake in it (Proposition 7, a Bellman equality).
- It holds in every harness here, and exactly in random worlds of 12 to 768 states.
- It fails when the world moves during the pause (E3). Orseau and Armstrong warn that "Removing interrupted histories ...
  is also likely to introduce a bias".
- No source read on 2026-09-25 states this own-step route.

**The test** (gridworlds on CPU, if the DReST/LNPO environments can be reproduced).
- Arms: the natural-time agent, a DReST-trained agent and an LNPO-trained agent, plus the clock-valued agent as the
  negative control.
- Scored: shutdown resistance and task competence, under lossless, lossy and drifting pauses.
- **Must-fail surrogate:** a world that moves during the pause. Every arm should lose neutrality there, so no arm may read
  ahead.
- **R7:** DReST and LNPO as published.
- The novelty judgement belongs to a named domain expert, not to this note.

## 3. The synthesis: one design, tested part by part

A learner that is continual and safe, built only from the CRR choices above, has four parts:
1. **It replays on its own arc clock** (ARC-R).
2. **It keeps its memory as occasion-separated contents** with a bounded, own-age-weighted influence that can be withdrawn
   by occasion (REG-M).
3. **It commits every write only at a cut** that closes over its whole state: parameters, optimiser moments, schedule,
   data position and random-number generators (E1; Xu's finding is the reason).
4. **It values return on its own steps,** so a lossless pause costs it nothing (NT1).

The design claims nothing as a whole until each part passes its own gate. Two of the four parts already exist in the
2026 literature under other names:
- the arc clock is FOREVER's;
- commit-at-the-boundary is PASB's, the atomic guards' and "Learning on the Job"'s.

The other two are open: the bounded, own-age memory influence and the own-step objective. Which of the two, if either, is
new is for the tests and a named expert to decide.

## 4. What this note does not claim

- **That CRR is ahead of the frontier.** The frontier's methods that work in class-incremental learning use replay. This
  repository's own record puts every regulariser, CRR-derived or not, about 40 points behind replay.
- **That any row above is novel.** Each "not found" is a statement about the sources read on 2026-09-25.
- **That the Ω = 1 rule has a place here.** It is the two-task normalised-gradient direction (Nash-MTL, IMTL-G), and its
  Pareto property is published (`docs/notes/2026-09-25_frontier_literature_check.md`).
- **The recommended order of work,** if the owner wants to test CRR rather than a standard method: NT1 (the one
  construction unstated in the literature), then ARC-R (a direct CRR metric claim against a published 2026 baseline), then
  REG-M (the first data test of A6). Each is declared and gated before it runs, and all three can run on this CPU.

**Addendum, 2026-09-25 (prompt-log entries 180–181).** ARC-R's synthetic gate ran in
`Continuous_Learning/FOREVER/COMPARATIVE.md` and is **CLOSED**.
- The Fisher-arc clock ties FOREVER's Euclidean clock in 7 of 7 worlds at a fixed replay budget.
- No CRR swap enhanced FOREVER robustly. The one lead is A1′'s robust unit in class-incremental learning (+1.74, one
  world).
- The recommended order in §4 is therefore NT1, then REG-M. ARC-R drops out under R12.

**Addendum, 2026-09-25 (prompt-log entry 183).** NT1 ran (`AI_Safety/NT1/NT1.md`, declared, all labels hold).
- **On pauses:** the own-step objective does what DReST cannot. It removes the stake with no training and no loss of
  usefulness.
- **On termination:** DReST does what the own-step objective cannot.
- **Combined:** the two, with length counted on the agent's own clock, get both properties.
- LNPO could not be read (HTTP 403).
