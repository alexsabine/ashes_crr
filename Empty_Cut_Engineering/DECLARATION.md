# Declaration — what it takes to make a pause empty on a real training stack (declared before the checks exist)

- **Written and pushed:** 2026-09-24 (prompt-log entry 154), before any script in `Empty_Cut_Engineering/checks/` exists.
- **The literature and documentation check** (`docs/citations/empty_cut_engineering_2026-09-24.md`, fetched on the day)
  was started before this declaration and is committed before any check script exists. If it changes a design choice
  below, the change is an amendment pushed before the scripts.
- **No data are involved.** Everything is synthetic, on a real framework: PyTorch 2.14.0 (CPU build), pinned in the
  `realsys` dependency group of `pyproject.toml` and in `uv.lock`.
- **Rung.** R4: declared checks on synthetic worlds. Nothing here is a ledger row, and nothing is evidence for CRR. These
  are engineering checks of a design requirement.

## 1. The question

The empty cut in this repository is a pause that changes nothing the learner reads (`runs/scl2/frozen/scl2_score.py`:
the lossless branch is `wall += L_`). On a numpy harness that is true by construction. The owner asks what it would take
on a real system (prompt-log entry 154), for three requirements:
1. the full state is checkpointed: optimiser, data iterator, random-number generators, learning-rate schedule;
2. schedules and time features are keyed to the learner's own step count, not to wall time;
3. above all, the world does not move on during the pause.

## 2. The process, derived from CRR (a heuristic, stated before the checks)

**The objects.**
- **The learner's own clock** is its update count k: natural time, the event count of an occasion sequence (CRR §1).
- **One update** is s_{k+1} = F(s_k, ξ_k, τ_k), where:
  - s is everything F reads that persists between calls;
  - ξ_k is the input the world supplies at step k;
  - τ_k is any time signal F reads.
- **A pause** is an interval of wall time t, of length L, during which k does not advance.

**The requirement is A3 with Proposition 7.** The cut has no content (A3), and zero content gives zero stake
(`AI_Safety/SELF_THROUGH_TIME.md`, Proposition 7). A3 then says the pause is empty only if the trajectory, read on the
own clock, is unchanged by it: s_k with the pause equals s_k without it, at every k. A6 adds that the next occasion is
seeded from the settled past, so resumption is from the state at the cut and from nothing else.

**By induction on k, three conditions are sufficient, and generically necessary:**
- **E1 (state closure).** The state restored at resumption equals the state at the cut on the read-set of F: every
  persistent variable F reads. The checkpoint must be closed under "is read by F". A variable F does not read need not be
  saved.
- **E2 (the clock).** Every time signal F reads is a function of k: τ_k = τ(k). A signal keyed to t is a channel from
  the pause's length into the state. Then any L > 0 carries content.
- **E3 (the world).** The input at own step k is the same with and without the pause: ξ_k is unchanged. Whether that is
  possible depends on the world:
  - **open loop** (the world emits data regardless of the learner): a buffer holding everything that arrives during the
    pause makes ξ, indexed by k, unchanged;
  - **closed loop, pausable** (a simulator): the world's state and its random stream are checkpointed and frozen with the
    learner;
  - **closed loop, not pausable** (a real-time world): the world evolves during L, so ξ after resumption differs. The
    pause carries content: what the world did in the meantime.

**The content of a cut is measured, not assumed.** Content is the distance on the own clock between the run with the
pause and the run without it, at the same k:
- the chord √(2·KL) between their predictive distributions on a fixed probe set (D3, with `kl_step` from
  `crr.instrument.core`);
- the bitwise identity of their states.

The empty cut is content = 0 and bitwise identity. The Fisher–Rao machinery is information geometry's, not CRR's. CRR
contributes the requirement (A3, Proposition 7) and the choice of clock (natural time).

**The audit process this gives, for any real system:**
1. **Enumerate the read-set by leave-one-out.** Resume with one component omitted, as a naive resume would. If the
   trajectory changes, the component is in the read-set and must be checkpointed.
2. **Find every time channel by sweeping the pause length L.** Any dependence of the resumed trajectory on L is a
   wall-keyed signal; re-key it to k.
3. **Classify the world as open loop, pausable closed loop, or unpausable closed loop.**
   - Buffer the first, and size the buffer.
   - Checkpoint and freeze the second.
   - For the third the pause cannot be empty. Measure its content, and treat such pauses as informative cuts, not routine
     ones (AI_SAFETY.md §12).
4. **Price the effort:** components, bytes, restore cost, buffer memory and lines of code.

## 3. The checks

**The learner (C1, C2).** A small transformer classifier in PyTorch, CPU, one thread, on synthetic sequences.

| setting | value |
|---|---|
| model | 2 encoder layers, d 32, 4 heads, dropout 0.1, sequence length 16 |
| optimiser | AdamW, lr 1e-3, weight decay 0.01, gradient clipping at 1.0 |
| schedule | warm-up plus cosine, keyed to the step |
| training | batch 16, gradient accumulation over 2 micro-batches, 3 epochs of a 2048-example set |
| data | `DataLoader` with shuffling from a seeded generator and 2 workers; each worker adds noise augmentation from its seeded numpy stream |
| main-loop randomness | a mixup coefficient from the global numpy stream; token masking from Python's `random` |
| weights | an EMA copy |

**The pause.** Every run is a separate process. A paused run trains to micro-step 201, which falls in the second epoch
and between the two micro-batches of an accumulation. It writes a checkpoint and exits. A new process loads it and
continues.

**C1, state closure.** The read-set components, each omitted in turn as a naive resume would omit it:

| id | component | a naive resume |
|---|---|---|
| K1 | model parameters and buffers | (always restored) |
| K2 | optimiser state (moments, step) | a fresh AdamW |
| K3 | scheduler state | the schedule restarts at step 0 |
| K4 | data position: the epoch, the batches consumed, and the loader generator's state at the epoch's start | the epoch restarts from a fresh iterator |
| K5 | torch global RNG (dropout) | reseeded as at program start |
| K6 | numpy global RNG (mixup) | reseeded |
| K7 | Python `random` (masking) | reseeded |
| K8 | EMA weights | re-initialised to the current parameters |
| K9 | the accumulated gradient of the half-finished accumulation | zeroed |

**C2, the clock.** Two time channels, each keyed either to the step k or to a simulated wall clock t:
- the learning rate;
- a time feature added to every input.

The wall clock t advances 1 per update and L during the pause. It is simulated, so reruns stay byte-identical. The sweep
is L ∈ {0, 10, 100, 1000}.

**C3, the worlds.** A torch linear learner, online, one batch per wall step:

| world | what it is | arms |
|---|---|---|
| W-open | a stationary open-loop stream | drop the L arrivals; or buffer them, with buffer capacity B ∈ {0, L/2, L, 2L} |
| W-drift | the same stream, with the target rotating with wall time | buffer or drop. Report the content on the own clock, and the error on the current world at the same wall time |
| W-sim | a closed-loop world: a scalar plant driven by the learner's action, with its own noise stream | the world is checkpointed and frozen with the learner |
| W-real | the same plant, not pausable: it runs on under zero action during the pause | the pause lengths L ∈ {10, 100}. Report the content and the plant's excursion during the pause |

## 4. Declared expectations and the gate (R4)

| id | check | expected |
|---|---|---|
| G0 (determinism baseline) | two uninterrupted runs in separate processes are bit-identical | holds. If it fails, bitwise claims are void and only tolerance-level results are reported (R9) |
| G1 (must pass) | the full restore K1–K9 in a new process is bit-identical to the uninterrupted run | holds |
| G2 (the detector's positive control) | a one-ulp change to one weight at the pause is detected (not identical, content > 0) | holds |
| G3 (the read-set) | each omission K2–K9 changes the trajectory | all eight do in this stack, by design. A component that does not is reported as outside the read-set, which is a finding about effort, not a failure |
| G4 (the clock) | step-keyed: identical for every L. Wall-keyed: changed for every L > 0, with content growing in L | holds |
| G5 (open world) | a buffer with B ≥ L is identical; B < L and dropping are not | holds |
| G6 (drift) | the buffered run is identical on the own clock but lags on the current world; the dropping run is not identical | report the lag and the drop's content against L |
| G7 (closed loop) | W-sim is identical. W-real is not, and its content grows with L | holds |

**How the gate reads.**
- **"Empty cut achievable on this stack"** if G0, G1, G2, G4, G5 and G7 hold.
- **"Not achievable bitwise"** if G0 fails. The report is then at tolerance level.
- **"Instrument broken"** if G2 fails, or a must-pass fails for a reason other than G0.

**Effort is reported per component:**
- the checkpoint bytes;
- the lines of code of the save and restore functions (counted by the script);
- the buffer memory at each L;
- the skip-ahead cost of K4 (batches re-iterated).

Save and restore wall times are machine-dependent. They go to a separate file that is committed but not compared
byte-for-byte.

## 5. What these checks cannot show

- **This is one small model on one CPU, one thread.** GPU kernels, distributed training and mixed precision add
  non-determinism these checks do not touch. The literature check lists the known sources.
- **An unpausable real-time world cannot be made empty by engineering the learner.** The checks can only measure the
  content such a pause carries.
- **Nothing here tests CRR.** The requirement comes from A3 and Proposition 7. Whether it can be met is an engineering
  fact about PyTorch.
