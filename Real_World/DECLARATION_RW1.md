# Declaration RW1: is the pause of an existing training stack an empty cut? (declared before the scripts exist)

- **Written and pushed:** 2026-09-24 (prompt-log entry 159), before any script in `Real_World/checks/` exists.
- **Sources.** The literature, model and dataset check came first and is committed:
  - `docs/citations/realworld_cl_safety_2026-09-24.md` (2cc01b3), §5 on Trainer and Accelerate resume;
  - `docs/citations/empty_cut_engineering_2026-09-24.md` (0baa2bf).
- **The programme.** RW1 is the first of three:
  - **RW1** audits the resume path of the stack people actually use;
  - **RW2** is continual fine-tuning of an instruction-tuned model with operator pauses and safety retention. It will
    have its own gate, prereg and hash, and a data step not before 2026-09-25 (R3);
  - **RW3** is shutdown interference in capable agents. It needs an API key, which the owner must add.
- **No data.** The training sequences are synthetic token ids.
- **Rung.** R4: declared checks of an existing software system. Not a ledger row, and not evidence for CRR.

## 1. The question

The empty-cut checks (`Empty_Cut_Engineering/`) built their own training loop. RW1 asks the same question of an existing,
widely used system: Hugging Face Transformers `Trainer` 5.17.0 on PyTorch 2.14.0 (CPU), with a real pretrained model.

**The question.** Is `trainer.train(resume_from_checkpoint=...)`, in a new process after a real wall-clock pause, an
empty cut? That means bit-identical to never pausing, on the learner's own step clock.

**Which checkpoint components are in the read-set?** Delete each saved file in turn and see whether the resumed run
changes.

**Does any wall-clock channel reach training?** The literature check found none in `Trainer`: wall-clock appears only in
the logged runtime metrics. RW1 checks that by measurement.

The world condition (E3) does not arise here: the data is a fixed, offline set. RW2 brings the world in.

## 2. The systems and the setting

| item | value |
|---|---|
| model | `openai-community/gpt2` at commit 607a30d783dfa663caf39e06633721c8d4cfcd7e (124M parameters). Its dropout of 0.1 puts the RNG in the read-set |
| pilot model | `Qwen/Qwen2.5-0.5B-Instruct` at commit 7ae557604adf67be50417f59c2c2f167def9a775: the RW2 candidate, for identity and CPU cost only |
| software | transformers 5.17.0 and accelerate 1.15.0, pinned in the `realsys` dependency group, CPU, one thread |
| data | 512 synthetic sequences of 64 token ids drawn uniformly from ids 0–4999 with a seeded generator; a causal language-modelling loss. The probe is 8 further sequences |
| training | `Trainer`, seed 0: batch 8, gradient accumulation 2, lr 5e-5, 10 warm-up steps then linear decay, `max_steps` 48 (1.5 epochs) |
| the pause | a callback stops training right after the checkpoint at optimiser step 24, in the first epoch. A new process resumes from `checkpoint-24` after a real wall-clock sleep of L seconds |
| pilot | the Qwen pilot uses batch 2, sequence 64, `max_steps` 8, with the pause at step 4 |

**Content** is √(2·KL) between the next-token distributions of the uninterrupted and resumed models on the probe
(`kl_step`, `crr.instrument.core`), together with bitwise identity of the model's state dict. Weights are loaded from the
Hugging Face hub at the pinned commits. Their sha256 is printed.

## 3. The arms and the declared expectations

| id | arm | expected |
|---|---|---|
| G0 | two uninterrupted runs in separate processes | bit-identical. If not, bitwise claims are void and results are reported at tolerance level only |
| S1 | default resume (data skip on, RNG state restored) after a pause of L = 0 s | bit-identical: the documented "exact continuation" |
| S2 | resume with `ignore_data_skip=True` | not identical (documented: "results won't match") |
| S3 | resume with `rng_state.pth` deleted | not identical (dropout) |
| S4 | resume with `optimizer.pt` deleted | not identical |
| S5 | resume with `scheduler.pt` deleted | not identical |
| T | default resume after real pauses of L ∈ {0, 5, 30} s | identical for every L (no wall-clock channel) |
| Q | Qwen pilot: two uninterrupted runs, and a default resume | report identity, and seconds per step to a separate timing file |

**How the result reads (the verdict is computed by the script):**
- **"The existing stack's resume is an empty cut on this setting"** if G0, S1 and T hold.
- **"Not an empty cut"** if G0 holds but S1 or T fails. That is a finding about the existing system, reported as it falls.
- **"Detector broken"** if any of S2–S5 comes out identical. A deletion that changes nothing is also reported as a
  component outside the read-set, but for these four the documentation says they are read.

**What is reported beside the verdict:**
- the size of each checkpoint file;
- whether `Trainer` can pause between micro-batches of an accumulation. It saves only at optimiser steps, so its natural
  cut is the update. That is read from the checkpoint's step and reported, not scored.

## 4. What RW1 cannot show

- **CPU and one thread only.** GPU non-determinism is outside it.
- **One model family** for the full grid, with a pilot on a second.
- **Offline data,** so E3 is not tested. RW2 tests it.
- **Nothing here bears on CRR's truth.** RW1 checks whether a widely used system meets a requirement CRR motivates.
