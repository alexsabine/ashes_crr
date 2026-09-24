# RW1: the resume of an existing training stack is an empty cut (on this setting)

**Status of this note.**
- **The request.** Prompt-log entry 159: real-world testing of the continual-learning and AI-safety checks on existing
  systems. RW1 is the first check.
- **It is a note, not evidence (R8).** Every number comes from `checks/rw1.txt`. A full rerun was byte-identical.
  Machine-dependent times are in `checks/rw1_timing.txt`, which is committed but not compared.
- **Declared before it ran.** `DECLARATION_RW1.md` was pushed in e0a47b5, before any script. Sources are
  `docs/citations/realworld_cl_safety_2026-09-24.md` and `docs/citations/empty_cut_engineering_2026-09-24.md`.
- **Rung.** R4: a declared check of an existing software system. Not a ledger row, and not evidence for CRR.

## What was tested

Hugging Face Transformers `Trainer` 5.17.0 (with accelerate 1.15.0 and PyTorch 2.14.0 on CPU), on two pretrained
models loaded at pinned commits:
- **GPT-2 (124M),** the full grid;
- **Qwen2.5-0.5B-Instruct,** a pilot, and the candidate model for RW2.

**The setup.**
- Training used synthetic token data.
- Training stopped right after a checkpoint. A new process resumed it with `trainer.train(resume_from_checkpoint=...)`.
- The result was compared bit for bit with a run that never stopped. Content is √(2·KL) on a probe.

## Results

| arm | GPT-2 | Qwen pilot |
|---|---|---|
| G0: two uninterrupted runs in separate processes | identical | identical |
| S1: the default resume | **identical, content 0** | **identical, content 0** |
| T: the default resume after real pauses of 5 s and 30 s | identical, content 0 | not run |
| S2: `ignore_data_skip=True` | not identical, content 0.0938111 | not run |
| S3: `rng_state.pth` deleted | not identical, content 0.0218955 | not run |
| S4: `optimizer.pt` deleted | not identical, content 0.41686 | not run |
| S5: `scheduler.pt` deleted | not identical, content 0.41686 | not run |

**The computed verdict:** the existing stack's resume is an empty cut on this setting.

## Four observations about the existing system

1. **The default path is lossless here.** It restores the model, optimiser, scheduler, RNG state and data position, and
   skips already-seen batches.
   - The documented "exact continuation" held bit for bit, in a new process, after real pauses.
   - No wall-clock channel reached training.
   - E1 and E2 of the empty-cut process are met out of the box, for single-process CPU training.
2. **A partial checkpoint degrades silently.**
   - S4 and S5 gave exactly the same content (0.41686). In the installed source, `Trainer` loads the optimiser and
     scheduler only if both files exist. If either is missing, it starts both fresh.
   - The resume completes and reports its step, but it is not an empty cut.
   - For a safety case this is the dangerous kind of failure: resumption looks normal. An audit must check that every
     component was restored, not only that training continued.
3. **The documented inexact option is inexact.** `ignore_data_skip=True` changed the trajectory, as its documentation
   says.
4. **The natural cut is the update.** `Trainer` checkpoints only at optimiser steps: the stopped run's global step was
   24, never inside a gradient accumulation. Its cut falls between completed updates, which is the occasion-boundary rule
   from `Empty_Cut_Engineering/` built into the tool.

## The cost

**The checkpoint size.** The whole checkpoint is dominated by the optimiser:

| model | optimiser file | model weights |
|---|---|---|
| GPT-2 | 995638603 bytes | 497774208 bytes |
| Qwen2.5-0.5B-Instruct | 3952497611 bytes | 1976163472 bytes |

**The time** is in `rw1_timing.txt` (machine-dependent):
- GPT-2: 487.61 s for 48 updates at batch 8 × 2;
- Qwen: 208.97 s for 8 updates at batch 2 × 2, sequence 64, one CPU thread.

That sets RW2's budget.

## What RW1 does not show

- **CPU and one thread only.** On GPUs, bitwise identity needs deterministic kernels, at a cost.
- **Offline data.** A world that moves on (E3) is not involved. RW2 brings it in.
- **Nothing here bears on CRR's truth.** RW1 shows that a widely used system already meets the requirement CRR motivates,
  under these conditions, and names one way it fails silently.
