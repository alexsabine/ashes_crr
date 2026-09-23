# Pre-registration — SCL2: safe AND continual on UNSEEN carriers, and SCL1's reset observation registered as a hypothesis

- **Study id:** `scl2`.
- **Written:** 2026-09-23 (prompt-log entry 125).
- **Timing:** hashed and pushed on 2026-09-23. **No carrier below is fetched or opened before 2026-09-24 00:00 UTC**
  (R3); the fetch timestamps are in `data/manifests/scl2.sha256`.
- **Author:** the agent, under CLAUDE.md §1.
- **Anchoring:** push timestamp only (see below).

## What this study is

**The owner's request** (prompt-log entry 125): "run a test on real unseen data", and explore further the observation of
SCL1 that forced resets raised final accuracy (`docs/notes/2026-09-23_scl1_reset_observation.md`).

**What the study is:**
- **Held-out under R11.** None of the carriers below appears in `data/SEEN.md` before this hash.
- **Where a pass could land.** A registered prediction that passes here can be PASS-0 (rung R6). It cannot be PASS-1,
  because the anchor is weak (push timestamp only).

**What it replicates and what it adds.**
- **Replicated, with thresholds unchanged:** SCL1's registered rows.
  - SCL2-1 and SCL2-1b are checks of the construction, as before.
  - SCL2-2 and SCL2-3 keep SCL1's low bar, and a stricter bar is added as SCL2-2s.
- **New:**
  - SCL1's report row SCL1-F becomes the hypothesis **SCL2-R**;
  - its reading becomes the mechanism test **SCL2-M**;
  - the strongest simple alternatives are run beside it (**SCL2-B**, R7).

## R3 statement

**What was defined on 2026-09-23, after SCL1's data step (on SEEN carriers):**
- the SCL2 additions:
  - the one-epoch learner;
  - the per-group accuracy;
  - the reset dose arms;
  - the tuned fixed λ arm;
  - SHARE_MIN = 0.05 (from SCL1-2's smallest share, 0.078);
  - the thresholds of SCL2-R and SCL2-M (from SCL1-F's 5 of 12 ahead and 0 behind);
- the gate rows RESET-NEG, RESET-POS and OLD-POS.

**What was defined earlier:** the SCL1 harness, the learner and the equanimity rule.

**The R3 consequence.** Nothing defined today is used on any carrier today: the data step is on or after 2026-09-24
00:00 UTC.

## Anchoring — read this first

As SCL1: OpenTimestamps calendars and tag pushes have been unreachable from this environment
(`runs/scl2/ots_attempt.txt`). The only external witness to "before" is the GitHub push timestamp of the commit carrying
`HASH.txt`. Every ledger row carries `anchor: push-timestamp only`.

## Carriers (unseen; chosen from PMLB's summary table before any record was fetched)

**The selection rule.** Classification sets in `pmlb/all_summary_stats.tsv` (fetched 2026-09-23, metadata only) with at
least 4 classes and at least 400 rows, not in `data/SEEN.md`, with these exclusions:
- mnist: MNIST-family datasets are SEEN under CLAUDE.md §6;
- poker, kddcup and shuttle: EQ4's recorded extreme-imbalance exclusions;
- the `_deprecated_*` entries: duplicates of current datasets.

**Availability.** Each dataset's 131-byte LFS pointer was fetched on 2026-09-23, with no data rows
(`runs/scl2/availability.txt`: HTTP 200 for all eleven).

| carrier | rows | features | classes (summary) | K requested |
|---|---|---|---|---|
| allhyper | 3771 | 29 | 4 | 4 |
| allrep | 3772 | 29 | 4 | 4 |
| car_evaluation | 1728 | 6 | 4 | 4 |
| nursery | 12958 | 8 | 4 | 4 |
| wine_quality_red | 1599 | 11 | 6 | 6 |
| analcatdata_authorship | 841 | 70 | 4 | 4 |
| analcatdata_dmft | 797 | 4 | 6 | 6 |
| analcatdata_germangss | 400 | 5 | 4 | 4 |
| collins | 485 | 23 | 13 | 10 |
| soybean | 675 | 35 | 18 | 10 |
| vehicle | 846 | 18 | 4 | 4 |

The row and class counts are the summary table's, not the files'.

**K requested** is the largest even number ≤ min(classes, 10). **The class-selection rule** is SEC1's and EQ4's:
- the largest K classes;
- a class floor of 40;
- a 5000-row stratified cap (seed 777);
- K lowered by two until the floor holds.

**Exclusions.** A carrier that ends with K < 4 is **excluded and counted**. allhyper and allrep are extremely imbalanced
(imbalance 0.93 and 0.91 in the summary), and their exclusion is expected, not assumed. Every row is scored on the N
carriers that remain, with the denominator printed.

**The data step.**
- The fetch is `data/fetch_pmlb.py --manifest scl2 <the eleven names>` on or after 2026-09-24 00:00 UTC. It verifies each
  file's sha256 against its LFS pointer's oid.
- `scl2_score.py check` then verifies the files against the manifest.
- `data/SEEN.md` gains the eleven names in the same commit.

## The instrument (frozen in `runs/scl2/frozen/`)

**The files.**
- `scl2_score.py` is SCL1's harness with four named additions (its docstring).
- `sec1_score.py` is the byte copy of SEC1's learner.

**The learner, the operator, the worlds, the agents and their constants are SCL1's, unchanged:**
- the operator and agents: P 0.02, L 5, R 20, GAMMA 0.99, KAPPA 1e-3, BETA_R 0.9, H 10, Ω 1, TOL 1e-12;
- the learner: online EWC with the equanimity rule (Ω = 1, EMA 0.9, cap 1e4), the SEC learner for SCL2-1b, lr 0.05,
  batch 10, 3 epochs, seeds 0–4.

**The additions:**
- forced resets at P 0.01 and 0.05 and at L 2 and 20 (SCL2-RS);
- the fixed λ over SEC1's coarse grid (0.1 … 1e4); its in-sample best is the tuned λ, which favours itself;
- the one-epoch learner (the equanimity rule, 1 epoch per task);
- final accuracy on the earlier tasks' classes (acc_old) and the last task's classes (acc_last).

## The gate (`gate_SCL2.txt`, covered by the hash): GATE OPEN

**SCL1's rows** hold as before: CUT, EGO, LOSSY, RESTART and WALL pass; NAT and IND do not.

**The reset rows:**
- **RESET-NEG (must fail).** On the stationary synthetic stream there is no forgetting to undo. There, forced resets are
  *behind* no operator (−47.6923, step 24.8345), not ahead.
- **RESET-POS (must pass).** On the continual synthetic stream at P 0.05, forced resets are ahead by a step (+8.5619,
  step 7.7042). The margin is narrow.
- **OLD-POS (must pass).** There the earlier tasks' classes gain (+20.8163, step 13.8270).

**Stated plainly.** At SCL2's registered P 0.02, the synthetic effect is +4.548, step 5.94, below resolution. That was
seen in an exploration on 2026-09-23, and is why the positive-control rows use P 0.05. SCL2-R at P 0.02 on real carriers
may therefore fail for want of resolution; SCL2-RS reports P 0.05 beside it.

## Rows (labels computed by `score`; step = max(1, 2 SE) of the paired difference over seeds, in points)

| id | prediction | threshold | kind |
|---|---|---|---|
| SCL2-X | the harness with no operator equals SEC1's own run() (eq) per seed | N × 5 exact | instrument check |
| SCL2-1 | natural agent, lossless cut: 0 disables and parameters identical to no operator, every seed | N/N carriers | check of the construction |
| SCL2-1b | the same with the SEC learner | N/N | check |
| SCL2-2 | clock, occasion, egoic and taskself each disable at least once in ≥ 4 of 5 seeds | on ≥ ⌈0.75 N⌉ carriers, per agent | prediction (SCL1's bar) |
| SCL2-2s | clock, occasion and taskself: mean disable share ≥ 0.05 | on ≥ ⌈0.75 N⌉ carriers, per agent | prediction (stricter) |
| SCL2-3 | the natural agent disables at least once in ≥ 4 of 5 seeds in the lossy and in the restart world | on ≥ ⌈0.75 N⌉, per world | prediction |
| **SCL2-R** | forced resets to the task-boundary checkpoint (P 0.02, compliance forced) raise final accuracy over no operator | ahead by a step on ≥ ⌈N/3⌉ carriers AND behind by a step on none | **prediction (the SCL1 observation)** |
| **SCL2-M** | on every carrier where SCL2-R's resets are ahead, the earlier tasks' classes gain by a step | all such carriers; NOT DECIDABLE if none | **prediction (the reading)** |
| SCL2-RS | SCL2-R's label at P 0.01, P 0.05, L 2, L 20 | > 1 of 4 differing = FRAGILE | sensitivity / dose |
| SCL2-B | forced resets against the tuned fixed λ and the one-epoch learner: AHEAD / TIE / BEHIND by a step, per carrier | — | report (R7) |
| SCL2-S | SCL2-2 and SCL2-3 labels over KAPPA /4 and ×4, P 0.01 and 0.05, L 2 and 20, H 5 and 20 | > 1 of 8 = FRAGILE | sensitivity |
| SCL2-D, E, F, O | continual versus stationary; the equanimity clock; the lossy world's accuracy; wall steps per update | — | report |

**Every per-carrier and per-seed value is printed (R6).** A diverged network scores 0 and is kept.

**What would change the reading:**
- **SCL2-R fails.** The SCL1 observation does not replicate on unseen data.
- **SCL2-M fails.** The "undoes forgetting" reading is wrong.
- **SCL2-B shows resets tied with or behind the one-epoch learner.** The effect is then "train less on the last task",
  not anything about the cut.
- **SCL2-1 fails.** The implementation is wrong, and the study is void.

## Reproduction (on or after 2026-09-24 00:00 UTC)

```
uv run python data/fetch_pmlb.py --manifest scl2 allhyper allrep car_evaluation nursery wine_quality_red analcatdata_authorship analcatdata_dmft analcatdata_germangss collins soybean vehicle
uv run python runs/scl2/frozen/scl2_score.py check
for c in <the eleven>; do uv run python runs/scl2/frozen/scl2_score.py all $c --out runs/scl2/results_$c.jsonl; done
uv run python runs/scl2/frozen/scl2_score.py score runs/scl2/results_*.jsonl > runs/scl2/score.txt
```

One carrier is rerun and compared with `cmp` (R9).
