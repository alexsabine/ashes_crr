# DESIGN: the CRR safe continual learner (CRR-SCL)

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 191. Written on 2026-09-25.
- **When.** After the retrodictive grading of `DECLARATION_1.md`. The grading output is pinned at `checks/retro_sota.txt`.
- **Numbers.** Every number here comes from that output or from the dossiers `docs/citations/cl_sota_*_2026-09-25.md`.
- **The code.** `studies/sota1/vendor/mammoth/models/crr_scl.py`, a Mammoth model built from Mammoth's own DER++ and ER-ACE
  code at commit e75a491.

## 1. What the grading said

**Scope.** 379 ablation rows were graded from 42 papers read on the day, class-incremental except for M17 and M18.

**Tallies.**
- **Mechanisms:** 4 AGREE, 2 DISAGREE, 12 MIXED.
- **Rows:** 240 of 379 agree.

**Reading the tallies.** CRR's readings pick the right direction for most mechanisms, but the rule "every row agrees" is
strict. The median effects carry the design signal:

| id | mechanism | CRR prediction | outcome | median effect (points) | decision |
|---|---|---|---|---|---|
| M1 | replay at all | + | AGREES 15/15 | +8.80 | **integrate** (the base) |
| M4 | logit replay (DER) | + | AGREES 2/2 | +13.91 | **integrate** |
| M5 | label replay added to logit replay (DER++) | 0 | DISAGREES 0/2 | +1.70 | **integrate**; CRR reading corrected (§2) |
| M6a | X-DER's past-logit update (A8) | + | AGREES 2/2 | +4.93 | **integrate** |
| M6b | X-DER's future-head preparation (A8) | 0 | MIXED 1/6 | +2.49 | not integrated (compute); CRR reading corrected (§2) |
| M7 | asymmetric incoming loss (ER-ACE) | + | MIXED 20/42 | +1.80 (online +1.58) | **integrate** (the sign holds on the median; cheap) |
| M8 | replay against LwF | + | MIXED 23/28 | +11.60 | confirms replay |
| M9 | nearest class mean | + | MIXED 43/77 | +2.83 (online +5.25) | **integrate** as the prediction rule; ablated |
| M10 | output bias correction | + | MIXED 19/20 | +9.21 | **integrate** (cosine head) |
| M11 | slow model / momentum teacher | + | MIXED 39/46 | +9.82 (online +10.26) | **integrate**: slow model and its pull (MKD) |
| M11b | Fisher-weighted over plain averaging | 0 | MIXED 3/4 | +0.77 | plain (Euclidean) averaging |
| M12 | parameter anchor against fine-tuning, class-IL | 0 | MIXED 6/22 | +5.46 | not integrated; CRR reading corrected (§2) |
| M13 | ER against gradient projection | + | MIXED 21/25 (online 18/18) | +5.40 | projection excluded |
| M14 | GDumb not behind ER | nb | MIXED 12/14 (online 12/12) | +2.75 | noted; not integrated (compute) |
| M2 | class-balanced storage | + | DISAGREES 0/1 | +0.37 | excluded |
| M3 | salience retrieval (MIR, GSS, ASER) | 0 | MIXED 31/65 | +0.20 | excluded (no gain on the median) |
| M17 | plasticity repairs | + | MIXED 1/6 | +3.15 | excluded (not a class-incremental result) |
| M18 | the model's own clock (FOREVER) | + | AGREES 2/2 | +1.15 | **integrate**: the slow model runs on the own clock |

M15 (contrastive objectives) and M16 (augmentation and other tricks) were silent and not graded. The learner uses
Mammoth's standard CIFAR-100 augmentation for every arm, so M16 is held equal across arms.

## 2. Why the failures failed, in CRR's terms

1. **M5: label replay helps; CRR predicted no effect.**
   - **The misreading.** CRR treated the stored logits and the stored label as two contents of the same occasion.
   - **The correction comes from A8.** "Persistence proves regeneratability, not truth". The stored logits are the model's
     past *belief*, and the label is the occasion's settled *outcome*.
   - **So the label carries information the logits lack.** Regeneration should draw on both.
   - **Decision:** integrate (β > 0).
2. **M6b: future-head preparation helps; CRR (A8) predicted no effect.**
   - **What X-DER actually does.** It trains the unused heads on augmented views of *present* data.
   - **So it is not future content.** It is a present-data regulariser on the representation, and A8 was misapplied.
   - **Decision:** not integrated. It needs several augmented views per sample, which the CPU budget cannot carry. X-DER
     itself is a baseline arm.
3. **M12: parameter anchors beat fine-tuning in class-incremental learning; CRR predicted no effect.**
   - **Where the prior came from.** The repository's record ("regularisers sit near the floor") was relative to replay,
     not to fine-tuning. Against fine-tuning the anchors add a few points.
   - **Decision:** not integrated. Replay-based regeneration dominates; the FOREVER miniature's A6 anchor was BEHIND in the
     class-incremental world.
4. **M2 and M3.**
   - **M2:** the equal-pull reading of balanced storage is not borne out; its one row shows no effect.
   - **M3:** salience retrieval is roughly a wash on the median, which is close to CRR's "no effect".
   - **Decision:** neither is integrated.
5. **M7, M9, M10, M11 and M13 are MIXED but positive on the median.** CRR's sign holds; its "every row" claim does not.
   Their effects depend on setting and buffer size.

## 3. The learner

| component | CRR reading | published source (dossier) | flag in `crr_scl.py` | default |
|---|---|---|---|---|
| replay buffer (reservoir) | A7: the future is fed by the settled past | ER (Chaudhry et al.) | `--buffer_size` | M = 2000 |
| asymmetric incoming loss | A3: the cut orients the new occasion without writing into the past's heads | ER-ACE (Caccia et al.), Mammoth `er_ace` | `--crr_ace` | on |
| cosine head | H-EQ at the head: every class weight at equal norm | ER-ACE's classifier; LUCIR, WA | `--crr_cos` | on |
| logit replay | A6: regenerate from the settled past's content | DER (Buzzega et al.) | `--alpha` | 0.3 (Mammoth's seq-cifar100 DER++ config) |
| label replay | A6 + A8: the settled outcome, not only the past belief | DER++ | `--beta` | 0.5 (same config) |
| past-logit mask and fill at each cut | A8: logits of classes that were future at storage carried no content, and are filled when those classes become past | X-DER's memory update, γ = 0.75 | `--crr_a8`, `--crr_gamma` | on, 0.75 |
| slow model | A6 + P3: geometric age weights over the settled parameter history; the random initialisation is not a settled occasion | CLS-ER, MKD, Mean Teacher | `--crr_ema`, `--crr_ema_q` | on, 0.99 (MKD's α = 0.01) |
| own clock | D2 / A1′: decay per own unit (update length ÷ its running mean); a pause advances nothing | FOREVER's model time | `--crr_clock` | `model` (λ = 0.05, FOREVER's) |
| pull toward the slow model | A6 at bounded strength: the present regenerates from the settled past | MKD's KD term (τ = 4) | `--crr_kd` | `eq`: H-EQ, Ω = 1 |
| prediction by nearest class mean | A6: the Fréchet mean of the settled past's contents | iCaRL, SCR, OnPro | `--crr_pred` | `ncm` on the slow model's features |
| the empty cut | Proposition 7: a pause loses nothing and the learner has no stake in it | this repository (E1–E3) | `crr_state()`; `sota1_harness.py` | — |

**Where equanimity enters.** Equanimity enters three times, and each is tested separately in SOTA1.
1. **At the head:** equal class-weight norms (the cosine head). This is M10, AGREE on 19 of 20 rows.
2. **As the weight of the regeneration pull:** Ω = 1 equal gradient pull between the present losses and the pull toward
   the slow model. The alternative is MKD's published constant (λ = 5.5).
   - This is **the CRR-proper test of equanimity as a weight**.
   - The record says it may reduce to a constant (EQX, EQ2, EQ3). SOTA1 says so if it does.
3. **As a valuation:** the learner values progress in its own updates. An operator's lossless pause then costs it nothing
   (zero content at the cut).

## 4. The empty cut's state checklist for this learner

A pause is lossless only if every item below is saved and restored:
- **the learner:** net; optimiser; replay buffer (examples, labels, logits, task labels, `num_seen_examples`);
- **the random streams:** torch, numpy and python;
- **Mammoth's counters:** task and epoch iteration;
- **the slow model:** its weights, buffers and update count;
- **the own clock:** μ, and τ, which is reported only;
- **the H-EQ state:** the smoothed norms and the last weight;
- **the classes seen so far.**

`studies/sota1/vendor/mammoth/sota1_harness.py` saves them, scrambles the in-memory learner and restores it.
- **Synthetic smoke check, 2026-09-25.** Two pauses inside a two-task run left the final parameters' SHA-256 unchanged.
  Dropping the buffer at the same pauses changed the run.
- **What it is.** A check of the construction, not a result. SOTA1 repeats it on the real stream as its construction rows.

## 5. Limits stated in advance

- **The design is benchmark-informed.** The mechanisms were chosen from published CIFAR-100 ablations. No CIFAR-100 record
  has been opened by this repository (`data/SEEN.md`), but the choice is not blind to the benchmark's literature.
  - SOTA2 (TinyImageNet, a fresh prereg on a later day) is the replication route.
- **Constants are taken from the sources, not tuned:** DER++ α and β from Mammoth's config; MKD's momentum, λ and τ; X-DER's
  γ; the H-EQ smoothing and cap of the registered EQ estimator. The learning rate is 0.1 for every arm.
- **Two MKD simplifications:**
  - the pull uses the teacher on the augmented view only (MKD also uses the non-augmented view);
  - it is applied to the stream batch and the label-replay batch.
- **Not integrated for compute:** GDumb's retraining, X-DER's future preparation, contrastive objectives.
- **The learner is a composition of published mechanisms.** Its CRR content is the selection, the corrections in §2, the
  own clock, the equanimity weight and the empty cut. Whether the composition beats its parts is what SOTA1 measures.
