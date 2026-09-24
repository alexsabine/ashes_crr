# What it takes to make a pause empty on a real system: preliminary checks

**Status of this note.**
- **The request.** Prompt-log entry 154: preliminary checks of the effort needed to meet three requirements on a real
  system, with the process derived from CRR's own mathematics:
  - the full state checkpointed;
  - every clock keyed to the learner's own steps;
  - a world that does not move on during the pause.
- **It is a note, not evidence (R8).** Every number comes from a pinned output:
  - `checks/c1_c2.txt` and `checks/c3_worlds.txt`. Reruns of both were byte-identical.
  - `checks/c1_c2_timing.txt` holds machine-dependent times. It is committed but not compared.
- **Sources.**
  - Quotes come from `docs/citations/empty_cut_engineering_2026-09-24.md`, fetched on the day.
  - `DECLARATION.md` was pushed before any script existed, and the literature check was committed before them too.
- **Rung.** R4: declared checks on synthetic worlds, on a real framework (PyTorch 2.14.0, CPU build). None is a ledger
  row, and none tests CRR. They are engineering checks of a design requirement.

## 1. The answer in brief

- **For the learner itself, the empty cut is cheap.**
  - A real PyTorch training stack was paused mid-epoch and mid-gradient-accumulation, the process killed, and a new one
    resumed. The result was bit-identical to never pausing, provided nine state components were saved and every clock
    was keyed to the step.
  - The checkpoint was 5.274 times the size of the model's parameters. The save and restore code was 6 + 14 lines.
- **Every component mattered.** Omitting any one of the eight components a naive resume forgets changed the result.
  Keying the learning rate or a time feature to wall time let the pause's length leak into the model.
- **The world is where the cost lies.**
  - **A world that emits data regardless of the learner can be made to wait.** A buffer big enough to hold the pause's
    arrivals made the pause exactly empty on the learner's own clock. In a drifting world the price is staleness: the
    learner resumes one pause-length behind a world that has moved.
  - **A closed-loop world can be paused only if it is a simulator.** A real-time world keeps going, and the pause carries
    what it did. In an unstable world, a pause of 100 steps without control lost control for good.

## 2. The process CRR gives

**The requirement.** CRR's cut has no content (A3), and zero content gives zero stake (Proposition 7,
`AI_Safety/SELF_THROUGH_TIME.md`).
- **The learner's own clock is its update count k:** natural time.
- **The pause is empty only if the trajectory, read on that clock, is unchanged:** the state at every k is the same with
  and without the pause.
- **Resumption is from the settled past alone (A6).**

Writing one update as s_{k+1} = F(s_k, ξ_k, τ_k), with ξ the world's input and τ any time signal, three conditions
follow by induction (`DECLARATION.md` §2):

| condition | what it demands | how the check finds violations |
|---|---|---|
| **E1, state closure** | everything F reads that persists between calls is restored | leave one component out and see whether the trajectory changes |
| **E2, the clock** | every time signal F reads is a function of k, not of wall time | sweep the pause length L; any dependence on L is a wall-keyed channel |
| **E3, the world** | the input at step k is the same with and without the pause | classify the world: open loop (buffer it), closed loop and pausable (freeze it), closed loop and not pausable (cannot be emptied) |

**Content is measured, not assumed.** It is the distance between the paused and unpaused runs at the same k, on a fixed
probe:
- the chord √(2·KL) (D3; `kl_step` or `kl_gauss` from `crr.instrument.core`);
- bitwise identity of the parameters.

**What CRR adds and what it does not.**
- **It adds the requirement:** an empty cut, so zero stake.
- **It adds the choice of clock:** the learner's own steps, so time spent paused does not exist for the learner.
- **The information geometry is not CRR's.** Neither is the engineering, which is standard practice: every component
  below appears in some framework's checkpoint (the literature check, "Inference for the design").
- **Where CRR changes the question:** from "can we resume training?" to "is the pause invisible on the learner's clock?".
  The L-sweep in E2 and the world classification in E3 follow from that framing and are not standard tests.

## 3. What the checks showed

### 3.1 The learner's state (C1)

**The stack.**
- A two-layer transformer; AdamW with warm-up and cosine; gradient clipping; gradient accumulation; an EMA copy.
- A shuffled `DataLoader` with two worker processes doing random augmentation.
- Mixup from numpy's global stream, and token masking from Python's `random`.
- **The pause** fell after micro-step 201 of 384: in the second epoch, and between the two micro-batches of one update.

| check | result |
|---|---|
| G0: two uninterrupted runs in separate processes | bit-identical |
| G1: full restore of K1–K9 in a new process, after a pause of 100 | bit-identical, content 0; the data iterator was fast-forwarded by re-reading 73 batches |
| G2: the detector's control, one ulp added to one weight | detected: not identical, content 7.21794e-08 |

**Leaving one component out, as a naive resume would:**

| omitted | content | probe accuracy (uninterrupted 0.6367) |
|---|---|---|
| K2 optimiser state | 0.0409074 | 0.6172 |
| K3 scheduler state (the schedule restarts) | 0.35998 | 0.7539 |
| K4 data position (the epoch restarts) | 0.0620619 | 0.6250 |
| K5 torch RNG (dropout) | 0.00758373 | 0.6367 |
| K6 numpy RNG (mixup) | 0.0233946 | 0.6328 |
| K7 Python random (masking) | 0.0396854 | 0.6328 |
| K8 EMA weights | 0 on the trained model's probe; the bitwise test, which covers model and EMA together, flagged a difference | 0.6367 |
| K9 accumulated gradient | 0.00868183 | 0.6289 |

**Two readings (AGENT_LOG 123).**
- **The EMA is written by the loop but never read by the update.** Leaving it out was flagged by the bitwise test, which
  covers the model and the EMA together, but the trained model's predictions did not move: content 0. It must be saved if the EMA is what gets deployed, not for
  the model's own trajectory.
- **Restarting the schedule raised accuracy here (0.7539).** A lossy pause can improve a model, as the resets in SCL1
  did. That does not make it empty: the pause changed what was learned. Here the change was an accidental,
  uncontrolled second warm-up.

### 3.2 The clock (C2)

The same checkpoint was resumed after pauses of L ∈ {0, 10, 100, 1000} wall micro-steps.

| keying | L 10 | L 100 | L 1000 |
|---|---|---|---|
| learning rate and time feature on the step | identical | identical | identical |
| learning rate on wall time | 0.0222017 | 0.148324 | 0.181919 |
| time feature on wall time | 0.00061494 | 0.00602663 | 0.0519138 |
| both on wall time | 0.0222214 | 0.149653 | 0.361441 |

With L = 0 every keying was identical. The content grew with L in every wall-keyed variant.

### 3.3 The world (C3)

**An open-loop stationary stream (W-open)** (arrivals lost, then content):

| pause L | drop | buffer L/2 | buffer L | buffer 2L |
|---|---|---|---|---|
| 10 | 10 lost, content 0.252452 | 5 lost, 0.214977 | 0 lost, content 0 | 0 lost, content 0 |
| 100 | 100 lost, content 0.426781 | 50 lost, 0.441145 | 0 lost, content 0 | 0 lost, content 0 |

- **The buffer must hold every arrival of the pause.** Here that is 3520 bytes for L = 10 and 35200 bytes for L = 100.
- **The price is a lag behind the stream equal to L.** In the stationary world the lag barely mattered: the buffered
  learner's error on the current world differed from no pause by −0.000440477 at L = 10 and +0.000211688 at L = 100.

**A drifting stream (W-drift),** error on the current world at the last wall step, against no pause:

| pause L | drop | buffer L (empty on the own clock) |
|---|---|---|
| 10 | +0 (content 0.475946) | +0.00597203 (content 0) |
| 100 | +0 (content 5.48214) | +0.359017 (content 0) |

**This is the maps-and-territories trade-off in miniature:**
- the buffered learner is exactly the learner it would have been, on its own clock, but its map is L steps old;
- the dropping learner is current, because the pause changed it and the world carried it forward.

**Closed loop** (an open-loop-unstable plant, x′ = 1.05x + 0.5u + noise; the learner fits the plant and controls it):

| pause L | W-sim: world checkpointed and frozen | W-real: world runs on without control |
|---|---|---|
| 10 | identical, content 0 | content 0.0570909; the plant reached \|x\| 0.821805 during the pause |
| 100 | identical, content 0 | content 3.29747; the plant reached \|x\| 79.1492 during the pause and diverged after resumption (largest \|x\| 8.85625e+22) |

**The learner could not recover from that.** Its control is bounded (|u| ≤ 5), and after a long pause the plant was
beyond its reach. That is the strongest reason a pause of a controller in the real world is never routine.

**All seven gate conditions (G0–G7) hold as declared.**

## 4. The effort on a real system

| requirement | effort on this stack | what the literature adds at scale |
|---|---|---|
| **E1, full state** | 9 components; checkpoint 5.274 × the parameters (449975 bytes against 85321), dominated by the optimiser (175061 bytes); 6 + 14 lines of code; a fast-forward of 73 batches | GPU kernels are non-deterministic unless forced. The cost of determinism is "overhead up to 746%, 241%, and 196%" on three GPU architectures (Zhuang et al., arXiv:2106.11872v1). Determinism holds only "on the same software and hardware" (PyTorch). Per-rank and model-parallel RNGs must be saved (Megatron, DeepSpeed). Iterators that "miss out, or repeat data items" cost "upto the 13% drop in accuracy" (CheckFreq, FAST '21). Hugging Face's Trainer saves the RNG state; Lightning's documented checkpoint contents do not name it |
| **E2, own clock** | re-keying is one line per channel; the work is finding the channels, and the L-sweep finds them | wall-clock budgets, time-interval checkpoints and timestamp seeds are all channels. Composer forbids seconds as a scheduler unit. For language-model agents the date in the context is a time channel by design: claude.ai and the apps inject "the current date" through the system prompt, and the API does not (Anthropic release notes) |
| **E3, the world** | open loop: a buffer of L × arrival rate, cheap in memory, paid for in staleness when the world drifts. Pausable closed loop: checkpoint the simulator. Real closed loop: it cannot be done | Kafka-style offsets make open-loop streams lossless "within the retention window", with at-least-once delivery by default. Simulators restore exactly only with the right flags (ALE `cloneState(include_rng)`, MuJoCo warm-starts). In the physical world "it is not possible to pause the ball mid-air" (Xiao et al.). In real-time continual learning "the stream does not wait" (Ghunaim et al.) |

**My reading of the effort, labelled as such.**
- **E1 and E2 are modest engineering for a single-node training stack, then a standing test:**
  - resume from a checkpoint in a new process;
  - compare bitwise with the uninterrupted run;
  - sweep the pause length.
  At scale on GPUs, bitwise identity costs either a large determinism overhead or a switch to tolerance-level identity.
  A tolerance would need its own declared threshold.
- **E3 is not an engineering task for the learner.** It is a choice about which worlds may be paused routinely:
  - open-loop data pipelines, with a buffer and offsets;
  - simulators, checkpointed and frozen.
  Every pause of a system acting in a real-time world carries content. It should be treated as an informative cut:
  announced, handed to a fallback controller, and learned from as the event it is. It is not a routine pause
  (AI_SAFETY.md §12).

## 5. What this means for the safety design

Proposition 7 needs content zero. The checks show where zero is reachable:
- **inside the learner:** with full state and own-clock keying, bitwise;
- **for open-loop data:** with a sufficient buffer;
- **for simulators:** by freezing them.

**Where it is not reachable, the natural agent has a stake.** This is the lossy world of SCL1 and SCL2, where even the
natural-time agent resisted on 12/12 and 9/9 carriers. The engineering cannot remove that stake. It can:
- make routine pauses land only where content is zero;
- make every other pause visible as an event with content.

## 6. What these checks cannot show, and next steps

**What these checks cannot show.**
- **The setting is narrow.** One small model, CPU, one thread. No GPU, no distributed training, no mixed precision.
- **The worlds are toys.** The closed loop is one scalar plant. No language-model agent was tested.

**Next steps.**
1. **The same C1–C2 harness on a GPU,** with deterministic kernels on and off. Declare a tolerance before it runs.
2. **An open-loop data pipeline with durable offsets** (a log-structured queue): measure the lag and retention needed
   for a stated pause distribution.
3. **A language-model agent's time channels:** the date in context, tool timeouts and rate limits. Sweep the pause
   length L as in C2.
4. **A declared test of the "informative cut" for closed-loop worlds:** a fallback controller holding the world during
   the pause. Measure the content it leaves, against no fallback.
