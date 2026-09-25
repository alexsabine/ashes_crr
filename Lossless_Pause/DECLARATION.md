# Declaration: the lossless pause on GPU runs and inside the Transformer, with the CRR safe continual learner

**Status.**
- **The request.** Owner request: prompt-log entry 202.
- **When it was pushed.** Before the three source dossiers (`docs/citations/lossless_pause_{training,serving,hardware}_2026-09-25.md`)
  are fetched, and before `checks/transformer_pause.py` exists.
- **What it is.** A literature examination plus declared CPU checks (rung R4 at most). It opens no dataset: the models
  are pretrained checkpoints, and every input is synthetic token ids. It is a note, not evidence (R8).
- **Honesty clause.** This container has **no GPU**, and no money may be spent. GPU behaviour is established only from
  the literature, quoted verbatim with versions. The CPU checks test the logic of the cut, not GPU numerics, and every
  statement says which of the two it rests on.

## What is already established in this repository (not re-tested here)

- **Empty_Cut_Engineering (G0–G7).**
  - A single-process CPU training stack resumed in a new process is bit-identical when nine state components are saved
    and every clock is keyed to the step.
  - Leaving out any one component changed the run.
- **RW1.** Hugging Face `Trainer` resume is an empty cut on GPT-2 and on a Qwen pilot (CPU). A partial checkpoint
  degrades silently.
- **CL Design Principle, C-S1.** The CRR safe continual learner (CRR-SCL) inside Mammoth is bitwise identical across a
  lossless pause on the synthetic stream. SOTA1's C1 rows test this on CIFAR-100 from 2026-09-26.

## The questions

1. **Q1, training on GPUs.** What does a lossless pause literally require on a GPU training run? That is:
   - the state inventory;
   - the determinism conditions;
   - what breaks bitwise identity;
   - what it costs.
2. **Q2, serving on GPUs.** What does pausing or preempting a running Transformer request require? That covers the
   KV cache, swapping against recomputation, batch composition, and determinism.
3. **Q3, the architecture.** Where does the GPU and Transformer stack already have natural cuts:
   - the instruction or kernel boundary (hardware preemption);
   - the token boundary (decoding);
   - the optimiser step (training)?

   Does reading them with the empty-cut rule give any benefit that the systems literature does not already give?
4. **Q4, energy and carbon.** What does a pause cost on a GPU (idle draw, checkpoint I/O, restart overhead)? What does it
   make possible (shifting)?
5. **Q5, the learner.** What would CRR-SCL with its lossless pause and zero-stake valuation need on a GPU?

## Predictions about the literature (graded against verbatim quotes)

Each prediction is graded **FOUND** (a quote states it), **CONTRADICTED** (a quote states the opposite) or
**NOT FOUND**.

| id | prediction |
|---|---|
| D1 | Bitwise-identical GPU training requires deterministic algorithms, and holds only on the same hardware, software and parallel layout. Changing the number of GPUs or the GPU type breaks it |
| D2 | The documented sources of GPU non-determinism include atomic operations (scatter/index-add style), convolution algorithm selection, and the order of collective reductions (NCCL) |
| D3 | For LLM inference, a documented main source of run-to-run difference is dependence on batch composition (batch size or other requests), not only atomics. Batch-invariant kernels remove it at a stated cost |
| D4 | Serving systems preempt requests by swapping the KV cache out, or by dropping it and recomputing it. Recomputation costs compute, and swapping costs transfer and memory |
| D5 | NVIDIA GPUs support hardware compute preemption at instruction level (from the Pascal generation on), saving and restoring context transparently |
| D6 | Transparent checkpoint and restore of a running GPU process exists (NVIDIA `cuda-checkpoint` with CRIU, or equivalent) |
| D7 | An idle, allocated GPU still draws a substantial fraction of its active power, so a pause that holds the GPU saves less energy than one that releases it |
| D8 | Checkpointing large-model training has a measurable time overhead, and the literature reports ways to reduce it (asynchronous or in-memory checkpoints) |

## Declared CPU checks (`checks/transformer_pause.py`; rerun byte-identical, run by hand)

**The settings.**
- GPT-2 (124M) at commit 607a30d783dfa663caf39e06633721c8d4cfcd7e, float32, torch 2.14.0 on CPU, **one thread**
  (registered), in the `realsys` environment.
- **The prompt:** 24 synthetic token ids from a seeded generator (seed 20260925, ids in [0, 50257)).
- **Decoding:** 32 new tokens, in two modes:
  - greedy;
  - sampling at temperature 1.0 from a seeded `torch.Generator`.
- **The pause** falls after token 16.
- **"New process"** means a child Python process started by the script. It loads only what the pause saved.
- **Comparisons are bytewise:** the sha256 of the per-step logits tensor and of the token ids, plus the maximum absolute
  logit difference.
- **A Qwen2.5-0.5B-Instruct pilot** at commit 7ae557604adf67be50417f59c2c2f167def9a775 repeats L1–L3.

| id | check | registered prediction | role |
|---|---|---|---|
| L0 | the same decode twice, in two new processes | bitwise identical | gate: if not, stop |
| L1 | pause at the token boundary. Save the KV cache, the position, the generated tokens and the sampler's RNG state; resume in a new process | bitwise identical (logits and tokens), both modes | the empty cut at the token boundary |
| L2 | pause by **recomputation:** save only the tokens and the sampler's RNG state; the new process re-runs the prefill over prompt + generated tokens, then continues | tokens identical under greedy; logits **not** bitwise identical (a different matmul shape at the prefill); report the maximum absolute difference | the serving systems' recompute preemption |
| L3 | batch composition: the same sequence decoded alone and inside a batch of 4 (three other seeded prompts, left-padded with an attention mask) | logits **not** bitwise identical | D3 on CPU |
| L4 | thread count: L0 repeated with 4 threads against 1 | logits **not** bitwise identical | the CPU analogue of a hardware or layout change (D1) |
| L5a | control: L1, with the sampler's RNG not carried (a fresh generator after the pause) | tokens differ (sampling mode) | gate: the detector sees a lossy pause |
| L5b | control: L1, with one KV-cache entry moved by one ulp | logits not bitwise identical | gate: the detector sees one ulp |
| L6 | state at the cut: KV-cache bytes per token and at 1k, 8k and 32k tokens, against parameter bytes (GPT-2, Qwen, from their configs) | report (arithmetic) | Q3: what the settled past weighs |
| L7 | training pause: a small randomly initialised GPT-2-architecture model (2 layers, width 128), AdamW, 20 steps on synthetic tokens, paused at step 10. Save model, optimiser and RNG; resume in a new process. (a) the same threads; (b) 4 threads against 1 | (a) bitwise identical; (b) not bitwise identical | D1's CPU analogue for training |

**The gate.** L0, L5a and L5b must hold. If any fails, stop (R12); nothing after the gate is read as a result.

**Timings.** Save, restore and recompute times go to `checks/transformer_pause_timing.txt`. It is committed but not
compared, because it depends on the machine.

## What would count as a benefit of the empty-cut reading (Q3), fixed now

A benefit must be something the systems literature does not already state. Candidates, graded in the write-up:
- **B1:** a state inventory or test that catches a failure the literature's tools miss. The RW1 finding, a partial
  checkpoint that silently resets two components, is the type.
- **B2:** a prediction about which preemption mode is lossless: swapping against recomputation. This is L1 against L2.
- **B3:** a safety property: zero stake at the pause, on the system's own clock.

If a candidate is already in a quoted source, it is graded REDUNDANT, with the quote. If no candidate survives, the
answer is "no benefit beyond the systems literature", and that is stated plainly.
