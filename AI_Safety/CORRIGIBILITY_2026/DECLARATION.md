# Declaration: the corrigibility problem in 2026, and where CRR's empty cut stands against the current safety bottlenecks

**Status.**
- **The request.** Owner request: prompt-log entry 206.
- **When it was pushed.** Before the sweep's searches run and before any script exists.
- **What it is.** A note, not evidence (R8).
- **The starting point.** It builds on:
  - `AI_Safety/FRONTIER_REVIEW.md` (prompt 149; sources `docs/citations/frontier_safety_2026-09-24.md`);
  - `docs/citations/unified_cl_safety_corrigibility_2026-09-24.md`;
  - today's sweep, `Lossless_Pause/FAIRNESS_REVIEW.md`, where C2 (the zero-stake pause) was graded PARTLY REDUNDANT.

## What the repository already holds (the position to be tested against 2026 work)

- **Proposition 7.** Zero content at the cut gives zero stake, in every world. It was checked in 540 cells
  (`AI_Safety/SELF_THROUGH_TIME.md`) and held by construction in SCL1–2 and NT1.
- **Its limits.** The repository itself states these:
  - reasoned pauses, where the operator pauses the agent because of harm;
  - drift during the pause;
  - value correction.

  The construction "is not a solution to the shutdown problem in general".
- **FRONTIER_REVIEW §2** found no source defining a pause on the agent's own clock. That is the claim most in need of a
  re-check.

## The candidate positions (K1–K5) to be graded against the sweep

| id | position | graded as |
|---|---|---|
| K1 | a pause defined on the agent's own clock (active steps), so it adds no length and no loss | REDUNDANT if a fetched source states it; PARTLY if a close form (the difference named); NOT FOUND otherwise |
| K2 | zero stake by a **true** map (the pause takes nothing on the agent's own clock), against indifference by a **false** map (the pause does not happen), which costs competence | as above |
| K3 | pause and termination separated on the agent's own clock, so a termination-neutrality method (DReST) and the zero-stake pause combine (NT1) | as above |
| K4 | routine pauses kept empty, and reasoned or corrective pauses made to carry information (an informative cut) | as above |
| K5 | corrigibility for a continually learning agent, placed in the structure of the valuation rather than in a learned belief, so it survives forgetting | as above |

"Not found" is never read as novel (CLAUDE.md §7).

## The sweep protocol (fixed now)

**Window and search.**
- **Window:** 2025-01-01 to 2026-09-25, with canonical earlier work included where a 2025–26 source builds on it.
- **Search:**
  - arxiv.org/search, all fields, first 50 hits by date. The arXiv API returned 406 today, so that fallback is declared
    in advance.
  - One WebSearch per query.
  - Every hit is screened and logged, as in `Lossless_Pause/DECLARATION_2.md`.
- **Cap:** at most 25 sources included per family.

**Family A: theory of corrigibility and shutdown, 2025–2026.**
- Queries:
  - "corrigibility";
  - "shutdown problem AI";
  - "shutdownable agents";
  - "incomplete preferences shutdown";
  - "off-switch game";
  - "utility indifference";
  - "safe interruptibility";
  - "corrigibility reinforcement learning 2026";
  - "shutdown-seeking AI".
- Must include if found:
  - Thornley's latest work on the shutdown problem and POST;
  - any 2025–26 DReST follow-up;
  - "Corrigibility as a Singular Target" (Harms);
  - Goldstein & Robinson on shutdown-seeking AI;
  - any 2025–26 formal result on corrigibility or impossibility.

**Family B: empirical corrigibility and loss-of-control evidence, and the 2026 statements of the bottlenecks.**
- Queries:
  - "shutdown resistance language models";
  - "self-preservation LLM agents";
  - "alignment faking";
  - "scheming evaluations frontier models";
  - "corrigibility evaluation benchmark";
  - "International AI Safety Report 2026";
  - "frontier safety framework shutdown";
  - "loss of control AI 2026".
- Must include if found:
  - the International AI Safety Report 2026;
  - Palisade's shutdown-resistance work;
  - the latest Anthropic, OpenAI and Google DeepMind safety-framework text on shutdown or pausing;
  - any 2025–26 corrigibility benchmark.

**The outputs.**
- Dossiers: `docs/citations/corrigibility_{theory,empirical}_2026-09-25.md`, each with its search log.
- Claims tagged K1–K5, or with a bottleneck tag (B-scheming, B-shutdown, B-selfpres, B-rewardhack, B-oversight, B-CL,
  B-evalaware, B-policy).
- The investigator's reading per claim (states / close / bears), recorded in `checks/claims.py`.
- `checks/grade.py` + `.txt`, which prints:
  - the K1–K5 grades;
  - a bottleneck table. CRR's position per bottleneck is the investigator's judgement (ADDRESSES at a named rung /
    PARTLY / SILENT), printed with the repository evidence it rests on and labelled as a judgement.
