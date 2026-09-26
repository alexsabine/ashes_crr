# Study SOTA1: the CRR safe continual learner against state-of-the-art methods on online Split-CIFAR-100

- **Written:** 2026-09-26, after the ledger rows SOTA1-1a … SOTA1-ND existed. Every number here is in those rows, in
  `runs/sota1/score.txt` (the frozen scorer's output, byte-identical on a second run) or in `runs/sota1/ledger_rows.txt`.
- **Pre-registration:** `prereg/sota1/PREREG.md`.
  - The sha256 of HASH.txt starts 4986bbee (prereg commit de95c63, 2026-09-25T11:51:16Z).
  - **Anchor: strong.** The OpenTimestamps proof is complete in Bitcoin blocks 968549, 968554, 968555 and 968581, the
    earliest at 2026-09-25T13:06:00Z. Every merkle root was matched against a public explorer (`runs/sota1/ots_upgrade.txt`).
    The signed tag could not be pushed (HTTP 403, `runs/sota1/tag_attempt.txt`), so the anchor is the proof.
  - **Hash after the run.** All 197 hashed files are unchanged (`runs/sota1/hash_check.txt`). The files the run added
    inside the frozen folder (bytecode caches, Mammoth's results logs, two pause checkpoints) are listed there. None is
    read as input.
  - **Data step.** It started 2026-09-26T00:07:26Z, after 00:00 UTC as R3 requires. The archive and member md5s
    matched torchvision's constants (`data/manifests/sota1.sha256`).
- **Owner request:** prompt-log entries 190 and 191; the design is in `CL Design Principle/`.
- **Data status:** CIFAR-100 was absent from `data/SEEN.md` before the hash. It is now SEEN.

> **Read this first.** **The CRR safe continual learner (CRR-SCL) does not beat the state of the art.**
>
> - **SOTA1-1a and SOTA1-1b FAIL.** CRR-SCL is BEHIND ER-ACE, the best baseline, by d = −3.30 class-incremental
>   points, on all five seeds. It ties ER, is BEHIND X-DER, and is AHEAD only of DER++ (which does badly in this online
>   setting) and of fine-tuning.
> - **The failure is not fragile.** SOTA1-S has 0 of 6 cells flipping: every sensitivity cell, including learning rate
>   0.05, reads BEHIND.
> - **SOTA1-2 FAILS.** Equanimity as a weight, H-EQ at Ω = 1, is BEHIND MKD's published constant λ = 5.5 by −2.94. It
>   does not even reduce to the constant; the constant beats it.
> - **SOTA1-3: 1 of 7 CRR component readings passes,** label replay (+5.18, PASS-0). That is DER++'s β term, a published
>   mechanism CRR names but did not invent.
>   - Four are TIE: A3's asymmetric loss, the cosine head, logit replay, and the own clock.
>   - Two are BEHIND: the A8 fill (−1.26) and the pull toward the slow model (−4.30). Removing either *improves* the
>     learner.
> - **The safety half holds as a construction.** A lossless pause is bitwise identical in 6 of 6 units (SOTA1-C1). Every
>   declared part of the pause state matters (C2). The must-fail control fails as it must (C3). The rerun is bitwise
>   identical (R9).

## 1. The question

**Can a continual learner built from CRR's readings of what works in state-of-the-art methods beat those methods on a
real benchmark?** This is SOTA1-1. **Does each CRR-proper component pull its weight?** This is SOTA1-2 and SOTA1-3.
The learner was assembled from published CIFAR-100 ablations (`CL Design Principle/checks/retro_sota.txt`, `DESIGN.md`):
- the empty cut and the own clock (CRR);
- H-EQ as the knowledge-distillation weight;
- logit and label replay, an asymmetric loss and X-DER's fill;
- a slow model, and nearest class mean.

**What SOTA1-1 is and is not.** It is a design comparison, not a test of a CRR hypothesis (PREREG R4 note). SOTA1-2 and
SOTA1-3 are the CRR-proper rows.

## 2. Instrument and run checks

- **Determinism.** SOTA1-R9 holds: the rerun of `crr` seed 0 reproduces the parameter sha256 and the per-task accuracy
  matrix bitwise.
- **Exclusions.** 6 of 110 declared units are NOT DECIDABLE (SOTA1-ND).
  - The `lwf` and `ewc_on` context baselines, seeds 0–2, failed at argument parsing before training. The frozen runner
    passes the rehearsal flags to every arm except `sgd` (AGENT_LOG 153).
  - Repairing the runner after the hash would have voided the study. No registered verdict needs these arms. The two
    rechecks that do (M8 and M12, report only) print NOT DECIDABLE.
- **Environment losses.** There were two container losses, at about 00:32Z and 15:26Z (AGENT_LOG 152 and 154,
  `runs/sota1/run_log.txt`).
  - The units running at the time (`er` and `er_ace` seed 0; `xder` at lr 0.05, seeds 0 and 1) were killed before
    writing any record. They were rerun with the identical command, and their killed logs are kept.
  - One startup race killed `crr` seed 0 at import (AGENT_LOG 151). It was rerun identically.
  - Every rerun is identical by construction, and R9 shows the pipeline is bitwise deterministic.
- **The four state-of-the-art baselines ran:** ER, ER-ACE, DER++ and X-DER, from Mammoth's reference implementations
  (commit e75a491), plus A-GEM and iCaRL as context.

## 3. Results

**Final class-incremental accuracy, mean over seeds** (`score.txt` gives every seed, with task-incremental in brackets):

| arm | mean | seeds |
|---|---|---|
| ER-ACE | 21.90 | 0–4 |
| X-DER | 20.44 | 0–4 |
| ER | 19.32 | 0–4 |
| **CRR-SCL** | **18.60** | 0–4 |
| DER++ | 10.87 | 0–4 |
| iCaRL | 8.82 | 0–2 |
| A-GEM | 5.80 | 0–2 |
| fine-tuning (SGD) | 5.57 | 0–4 |

**The pre-registered rows** (ledger SOTA1-*; d is CRR-SCL minus the comparator, with step max(1.0, 2·SE)):

| row | observed | verdict |
|---|---|---|
| SOTA1-1a / 1b | against ER-ACE: d = −3.30, step 1.07; per seed −2.11 / −4.51 / −3.00 / −4.60 / −2.28 | **FAIL / FAIL** |
| SOTA1-2 | against `crr-kdfixed` (λ = 5.5): d = −2.94; per seed −3.47 / −2.93 / −2.43 | **FAIL** (BEHIND, not REDUCES) |
| SOTA1-3 A3, asymmetric loss | +0.37, TIE | FAIL |
| SOTA1-3 H-EQ at the head, cosine | +0.80, TIE | FAIL |
| SOTA1-3 A8, mask and fill | −1.26, BEHIND | FAIL |
| SOTA1-3 A6, logit replay | +0.13, TIE | FAIL |
| SOTA1-3 A6/A8, label replay | +5.18, AHEAD | **PASS-0** |
| SOTA1-3 A6, pull to the slow model | −4.30, BEHIND | FAIL |
| SOTA1-3 D2/A1′, own clock against step clock | +0.13, TIE | FAIL |
| SOTA1-3 prediction rules (nearest class mean against the fast / slow head) | +7.96 / +7.97, AHEAD | report only: AHEAD on the R4 surrogate too |
| SOTA1-S | 0 of 6 cells flip | not fragile |
| SOTA1-C1 | 6/6 units bitwise identical under a lossless pause | holds (construction) |
| SOTA1-C2 | drop net −15.57, buffer −11.43, rng −2.10, slow model +0.03, own clock −0.20, H-EQ state −0.17 (all change the parameters) | holds |
| SOTA1-C3 | the world moving: stake +0.83 | holds (the must-fail control) |
| SOTA1-C4 | wall-clock valuation stake +0.77 | report |
| SOTA1-R9 | bitwise identical | holds |

**Against the other baselines,** CRR-SCL is:
- TIE with ER (−0.72);
- BEHIND X-DER (−1.84);
- AHEAD of DER++ (+7.73) and of fine-tuning (+13.03).

**Rechecks of the graded mechanisms on this benchmark** (report only, seeds 0–2; `score.txt`):

| mechanism | comparison | label |
|---|---|---|
| M1 replay | ER against fine-tuning | AHEAD (+12.93) |
| M13 | ER against A-GEM | AHEAD (+12.66) |
| M7 asymmetric loss | ER-ACE against ER | AHEAD (+2.93) |
| M4/M5 logit + label replay | DER++ against ER | **BEHIND (−7.34)** |
| M6 | X-DER against DER++ | AHEAD (+9.23) |
| M8, M12 | against LwF / online EWC | NOT DECIDABLE |

## 4. Sensitivity table (SOTA1-S, seeds 0–1)

| cell | d against ER-ACE | label |
|---|---|---|
| default | −3.31 | BEHIND |
| q = 0.98 | −2.80 | BEHIND |
| q = 0.995 | −3.54 | BEHIND |
| H-EQ cap 100 | −4.11 | BEHIND |
| γ = 1 | −3.31 | BEHIND |
| H-EQ smoothing 0.5 | −3.17 | BEHIND |
| lr 0.05 (all five arms) | −4.08 | BEHIND |

Flips: 0 of 6. **The FAIL does not depend on any named constant.**

## 5. Reading

1. **CRR as a design lens did not produce a better learner on this benchmark.** The integrated learner is 3.30 points
   behind a single published method, ER-ACE. It is ahead only of the methods that collapse in this online setting.
2. **The equanimity weight lost to a constant again.** Earlier real-data H-EQ rows found the rule reducing to a fixed
   weight (EQX-1) or behind the tuned λ (EQ4-1 FAIL). Here it is BEHIND the published constant, not tied with it.
3. **The CRR-proper component readings mostly failed.**
   - The own clock (D2/A1′) is a TIE with the step clock, as the energy check predicted
     (`Energy Design Principle/checks/clock_cut.txt`: the own-clock cut reduces to Wald).
   - Two readings are counter-productive: the A8 fill and the pull toward the slow model.
   - The one pass, label replay, is a published mechanism.
4. **What held is the construction.** The lossless pause is bitwise identical on a real CIFAR-100 learner, and the
   declared state is the state that matters. This is Proposition 7 on a real benchmark: engineering, not evidence for
   CRR (SOTA1-C1–C3; the same status as SCL1–3 and Empty_Cut_Engineering).
5. **Observations with no verdict (post hoc; R3 forbids acting on them without a new prereg on a new dataset on a later
   day):**
   - `crr-kd`, the learner without the pull toward the slow model, reaches a mean of 22.49 over seeds 0–2. That is the
     highest arm in the table. It is an ablation, not a registered comparison against ER-ACE.
   - The fast and slow heads collapse in class-incremental prediction; nearest class mean carries the learner (+7.96),
     as the Phase A gate had already shown.

## 6. What a surrogate would have done (`prereg/sota1/gate_sota1.txt`)

On the near-ceiling surrogate W0, where there is nothing to win:
- SOTA1-1a and 1b were BEHIND (−1.14 against ER);
- SOTA1-2 was a TIE (−0.10);
- every arm component was a TIE;
- the prediction-rule rows were AHEAD, so they were reported without a verdict.

On the real benchmark:
- SOTA1-1 and SOTA1-2 fail as they failed on the surrogate;
- the component readings split between TIE and BEHIND, with one AHEAD;
- the prediction rules are AHEAD, as on the surrogate, which is why they carry no verdict.

**Every CRR-proper row that failed would have failed on a signal with no CRR content.** The one pass (label replay)
failed on the surrogate (+0.20, TIE) and passed here. It is a real effect, and it belongs to DER++'s β term.

## 7. Rung and next steps

- **Rungs.**
  - SOTA1-3 label replay is PASS-0 (R6) on unseen, strongly anchored data, for a published mechanism.
  - Every CRR-proper hypothesis in SOTA1 is FAIL.
  - The construction rows are checks of the build, not rungs of evidence.
- **SOTA2 (Split-TinyImageNet), the pre-registered replication route to PASS-2, has nothing CRR-proper to replicate.**
  Under R12 no weaker hypothesis is invented to have something to run. A SOTA2 prereg would be a replication of the
  label-replay component and of the construction only, and it needs the runner defect of AGENT_LOG 153 fixed before a
  new hash.
- **ENERGY1 depends on SOTA1** (`Energy Design Principle/FINDINGS.md`). With the learner BEHIND the state of the art,
  ENERGY1's CRR-learner arm has no accuracy parity to trade against compute. What remains testable for energy is the
  lossless pause (C1 holds) and SEC (SCL3, PASS-0).
