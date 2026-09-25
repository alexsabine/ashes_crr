# The lossless pause on GPU runs and inside the Transformer

**Status.**
- **The request.** Owner request: prompt-log entry 202. It is a note, not evidence (R8), at rung R4 at most.
- **How it was done.** `DECLARATION.md` was pushed (d933519) before the sources and before the script.
  - Amendment 1 (eac338f) was pushed after the first run's gate closed and before the rerun.
  - Decisions are in AGENT_LOG 147.
- **Where the numbers come from:**
  - `checks/transformer_pause.txt`, the CPU checks. The rerun is byte-identical and run by hand. The closed first run is
    kept as `checks/transformer_pause_run1_gate_closed.txt`.
  - `checks/grade_claims.txt`, the literature predictions, CI-checked.
  - `checks/claims.py`: 122 claims and 238 quotes, all verbatim (`checks/verify_claims.txt`), from
    `docs/citations/lossless_pause_{training,serving,hardware}_2026-09-25.md`.
- **The limit.** This container has no GPU. Everything said here about GPUs is the literature's; the CPU checks test the
  logic of the cut, not GPU numerics.

## 1. The answer in brief

- **A lossless pause is achievable on GPUs, but only under stated conditions**, and the literature already states them
  (D1–D8):
  - deterministic kernels;
  - the same GPU type, the same number of GPUs and the same software;
  - batch-invariant kernels for serving;
  - the full state saved.
- **Each condition has a price:**
  - determinism slows training and serving;
  - holding the GPU through a pause keeps it drawing power;
  - releasing it costs checkpoint and restore time.
- **The Transformer has natural empty cuts.** The token boundary in decoding and the optimiser step in training each
  carry a finite, explicit state. On CPU, pausing at the token boundary with the KV cache carried was **bitwise
  lossless** for GPT-2 and Qwen2.5-0.5B.
- **The serving systems' default recompute preemption is not lossless at the level of state.** It regenerates the past
  instead of carrying it. The tokens came out the same here, but the logits and the KV cache did not. The literature
  reports token flips in FP16 and BF16.
- **An output-level check cannot prove a pause lossless.** A one-ulp corruption of the saved state left every output
  byte identical. The audit must compare the state itself.
- **Does the empty-cut reading add anything beyond the systems literature?**
  - Almost nothing technical. The one candidate is an audit discipline: compare state digests, not only outputs.
  - Even that is close to a quoted 2026 statement.
  - The safety property (zero stake at the pause) is a property of the learner's valuation, not of the GPU or the
    Transformer.

## 2. What the literature says (graded; `grade_claims.txt`)

| id | prediction | grade | what the quotes say |
|---|---|---|---|
| D1 | bitwise GPU training needs deterministic kernels and holds only on the same hardware, software and layout | **MIXED** (7 state it, 1 states the opposite) | "same architecture and the same number of SMs" (cuBLAS 13.4); "Across different architectures, no cuDNN routines guarantee bitwise reproducibility" (cuDNN 9.26.0); "the same HW and SW environment" (Megatron). **The exception:** OPEN-1B (arXiv 2609.17380v1) makes a run "bit-exact under replay, independent of device count and topology", with custom reproducible kernels, trading "compute performance for reproducibility" |
| D2 | non-determinism comes from atomics, algorithm selection and the collective reduction order | FOUND (9) | the PyTorch 2.14 list of non-deterministic CUDA ops; cuBLAS and cuDNN atomics; Megatron: the NCCL ring's reduction order is "fixed by topology", and tree "cannot be vouched for as bit-exact" |
| D3 | LLM inference differs mainly with batch composition; batch-invariant kernels fix it at a cost | FOUND (10) | "the primary reason nearly all LLM inference endpoints are nondeterministic is that the load (and thus batch-size) nondeterministically varies" (Thinking Machines, 2025-09-10); SGLang's deterministic mode has "most slowdowns ranging from 25% to 45%"; a bitwise RL run was "2.4x slower" (vLLM/TorchTitan) |
| D4 | serving preempts by swap or by recompute; recompute costs compute, swap costs transfer | FOUND (12) | vLLM V1's default is RECOMPUTE; recomputing an 8k sequence for LLaMA-30B "takes 3.5s", against 20–30 ms for live migration (Llumnix); recomputation took "37-40% of total model forwarding time" in tool-call pauses (InferCept); "up to 69% of GPU time" was wasted on recomputation or swapping under memory pressure (ConServe) |
| D5 | instruction-level hardware preemption from Pascal on | FOUND (2) | the Pascal whitepaper and the CUDA 12.4 guide state it. REEF (OSDI 2022) and GPreempt (ATC 2025) add that there is no user-facing interface, and that the context is about 44 MB on an A100 |
| D6 | transparent checkpoint and restore of a GPU process | FOUND (3) | NVIDIA `cuda-checkpoint` with CRIU (2024 blog; Driver API v13.4). Restore onto a different GPU needs "the same chip type". CRIUgpu reports 77.40–146.43 s to checkpoint and 38.83–145.14 s to restore 54–58 GB on one H100, and no NCCL support at the time of writing |
| D7 | an idle but allocated GPU draws substantial power | FOUND (2) | with a CUDA context, an idle H100 drew 121.7 W against 71.8 W bare (the Model Parking Tax, 2026). An "execution-idle" GPU draws around 110 W against a 35 W deep idle, "48% of energy in long-lived, academic serving workloads" (Lei et al., 2026). Idle is about 20 % of TDP (POLCA) |
| D8 | checkpointing has measurable overhead; asynchronous or in-memory checkpoints cut it | FOUND (10) | CheckFreq bounds overhead "within 3.5%"; ByteCheckpoint cuts stalls 54.20×; Gemini checkpoints every iteration with "no overhead on training throughput"; about 10 s of checkpoint write time is needed at 12,000-GPU scale (Kokolis et al.) |

## 3. What the CPU checks showed (`transformer_pause.txt`)

| check | result | prediction |
|---|---|---|
| L0: the same decode in two new processes | logits, tokens and state (KV cache, 55 positions) bitwise identical, both modes | gate: holds |
| L5a: the sampler's random state not carried | tokens differ: detected | gate: holds |
| **L5b as declared: one ulp added to one KV entry, detected by the outputs** | **not detected**: every logit byte identical. **The first run's gate CLOSED here** | failed; see below |
| L5b (Amendment 1, post hoc): the same, detected by the state digest | detected | gate: holds |
| **L1: pause at the token boundary, KV cache carried, new process** | **bitwise identical** in logits, tokens and state: GPT-2 and Qwen, greedy and sampling | held |
| **L2: pause by recompute** (tokens only; re-run the prefill) | tokens identical; **logits and state not bitwise** (max logit difference 8.011e-05 and 1.755e-04 for GPT-2, 1.907e-05 and 4.339e-05 for Qwen) | held |
| L3: the same sequence alone and inside a batch of 4 | logits not bitwise (6.866e-05 GPT-2, 1.556e-05 Qwen); tokens identical | held |
| L4: 4 threads against 1 | logits and state not bitwise; tokens identical | held |
| **L7: a training pause, new process** | same threads: parameters bitwise identical. 4 threads after the pause: not bitwise (max 3.822e-06) | held (both) |
| L6: the state at the token cut (fp32) | GPT-2: 73,728 bytes per token, 1.2134 × the parameter count at 8,192 tokens. Qwen (2 KV heads): 24,576 bytes per token, 0.1019 × at 8,192 | report |

### What the checks add

1. **The cut must carry the settled past, not regenerate it.**
   - Carrying the KV cache (L1) is an empty cut, identical to never pausing.
   - Regenerating the cache by recomputation (L2) is a different computation, with a different reduction order at the
     prefill. It lands close but not on the same bits.
   - Here the tokens survived. In the literature they do not always survive in FP16 and BF16:
     - FP16 KV-cache inference is "fundamentally non-equivalent to recomputation" (Chodavarapu & Xu, arXiv 2604.15409v1);
     - BF16 stage replay differs "on 166 suffixes" (Lorup, arXiv 2607.28495v1).
   - **In CRR's terms,** A6's regeneration from the settled past is not the identity. An empty cut (Proposition 7) needs
     the state carried.
2. **Identical outputs do not prove an identical state.**
   - The declared one-ulp control was invisible at the output: float32 rounding absorbed it.
   - A pause audited only by comparing outputs could pass with a corrupted state. That state could diverge later, or
     under a different input.
   - The audit that works compares the state bytes. The first run's closed gate is kept on record because it found
     this.
   - Nearby statement in the literature: "Exact-token replay can therefore be repeatable without preserving live-state
     fidelity" (Lorup).
3. **Any change of numerical layout breaks bitwise identity, even on CPU:** batch composition (L3) and thread count (L4,
   L7b). On GPUs the literature names the same class: batch size, GPU count, GPU type and the reduction order (D1–D3).
   A pause that resumes on a different layout is at best tolerance-level lossless, and the tolerance must be declared.

## 4. What a lossless pause literally means on a GPU run

**Training (a pause at an optimiser step).**
1. **Save the full state.** Weights, optimiser moments, scheduler step, the gradient scaler (mixed precision), every
   random stream (CPU, each GPU's, each rank's model-parallel stream), the data position and shuffle seed, the EMA or
   slow model, any replay buffer, and every own-clock counter.
2. **Resume on the same GPU type and count, with the same software and the same collective algorithm, and with
   deterministic kernels on.** The price is the determinism overhead, which the literature reports in the tens of per
   cent up to several-fold. Otherwise, declare a tolerance.
3. **Choose between two ways of pausing:**
   - hold the process (`cuda-checkpoint` locks it; the GPU stays allocated and keeps drawing idle-with-context power);
   - release the GPU (checkpoint to host or storage, and pay the checkpoint and restore time). CRIUgpu took tens of
     seconds to minutes for 54–58 GB.
4. **Treat the collectives as part of the state.** NCCL communicators are re-created. CRIUgpu reported no NCCL support.
   The ring's reduction order is fixed by topology, so the topology must match.

**Serving (a pause at a token boundary).**
- **Swap or preserve the KV cache,** don't recompute it, if the pause must be lossless.
- **Use batch-invariant kernels,** so that the resumed request's numerics do not depend on which other requests share
  its batch.
- **Carry the sampler's random state.**
- **The costs.** Swapping costs PCIe transfer and host memory. Preserving costs GPU memory. Batch invariance costs about
  25–45 % of throughput (SGLang).

## 5. Can the GPU and Transformer architecture use the empty-cut rule, and does it help?

**The GPU hardware.**
- The hardware already implements an exact cut: instruction-level preemption saves the full context (about 44 MB on an
  A100), and `cuda-checkpoint` suspends a process at a quiescent point.
- The empty-cut rule has nothing to add there. The hardware cut is lossless by design. The difficulties are above it: in
  numerics, layout and the world.

**The Transformer.**
- **It has two natural empty cuts:**
  - the token boundary, whose state is the KV cache, the position and the sampler's random state;
  - the optimiser step.
- **Causal masking is A7 built in:** nothing is fed by a future token.
- **The KV cache is the settled past, stored as content.** Its size grows with context: 73,728 bytes per token for GPT-2
  in fp32. Grouped-query attention (Qwen's 2 KV heads) cuts that to 24,576. State-space models keep a fixed-size state:
  Mamba's inference "requires only constant time per step since it does not require a cache of previous elements"
  (Gu & Dao, quoted in the hardware dossier).
- **So the architecture can "use" the rule** in the sense that its cuts are already empty when the state is carried.

**Does reading it this way provide a benefit?** Graded against the declaration's criteria:

| candidate | verdict |
|---|---|
| B1: an audit that catches what existing tools miss (compare state digests, not outputs) | **supported by L5b.** Close to Lorup's quoted statement about live-state fidelity, so a candidate at most. It is not claimed as new |
| B2: predicting which preemption is lossless (carry against regenerate) | **REDUNDANT.** Thinking Machines states that the reduction order must match between prefill and decode, and Chodavarapu & Xu that FP16 recomputation is non-equivalent |
| B3: zero stake at the pause (safety) | a property of the learner's valuation (SCL1–3, NT1), not of the GPU or the Transformer. It adds nothing at the architecture level. Its prior art (safe interruptibility, utility indifference) was reviewed in `AI_Safety/FRONTIER_REVIEW.md` |

**The honest answer.** The architecture already supports lossless pauses where the state is carried. The empty-cut rule
restates that, and it does not make GPUs or Transformers faster or cheaper. Its only practical contribution is
discipline:
- the state checklist;
- the state-digest audit;
- keying every clock to the step.

In this repository, that discipline caught silent failures: RW1's partial checkpoint, and here the output-invisible
corruption.

## 6. The CRR safe continual learner with the pause and safety, on a GPU

**What is established.**
- CRR-SCL's lossless pause is bitwise identical on the synthetic stream (C-S1).
- SOTA1 tests it on CIFAR-100 from 2026-09-26 (C1, on CPU).

**What a GPU run would need** (from sections 2 and 4):
- **Save the state that SOTA1's C2 found to matter:** the network, the buffer, the random streams, the slow model, the
  own clock and the H-EQ state.
- **Turn on deterministic cuDNN convolutions** for the reduced ResNet-18, and pay their overhead.
- **Resume on the same GPU type and count.**
- **Hold or release the GPU,** accepting the idle draw or the restore time respectively.

**How the safety property transfers.**
- The zero-stake valuation is computed on the learner's own steps, so it does not depend on the hardware.
- It does depend on the pause being empty. On a changed layout, the pause is no longer bitwise empty, and the learner
  would have a small, measurable stake.
- So the safety claim should be stated with the same condition as the losslessness: the same hardware class and
  deterministic kernels. Otherwise it holds only up to a declared tolerance.

## 7. What this means for energy and carbon

- **Holding a paused GPU is not free.** Measured idle draw with a CUDA context was 80.0–121.7 W across three GPU types
  (the Model Parking Tax).
- **Releasing the GPU saves that draw but costs checkpoint and restore time.** For carbon-aware pausing, long pauses
  should release and short ones may hold. The crossover depends on the restore cost, which this repository has not
  measured on a GPU.
- **Determinism itself costs energy.** Throughput losses of 25–45 % in serving, and several-fold in some bitwise
  training setups, mean more GPU-time for the same work.
  - That is a real trade-off between lossless or auditable pausing and energy.
  - The consolidated estimate (`Energy Design Principle/CONSOLIDATED.md`) did not include it. T4's zero on energy
    should read "zero or negative" when bitwise determinism is required.

## 8. What these checks cannot show

- **No GPU numerics were measured,** and no GPU idle or restore power was measured here. Those figures are quoted.
- **The models are small, and the prompts synthetic.**
- **L5b's state-level reading is post hoc** (Amendment 1).
- **B1 is a candidate, not a finding.** A literature check specific to "state-digest audits of checkpoint/restore"
  would be the next step.
- **Next, if a GPU becomes available (it costs money, so this is the owner's decision):**
  - run L1, L2, L3 and L7 on one GPU with deterministic kernels on and off;
  - measure hold against release power for a pause.
