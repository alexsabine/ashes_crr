# Real-world testing of continual learning and AI safety on existing systems: status

**Status of this note.**
- **The request.** Prompt-log entry 159.
- **It is a note, not evidence (R8).** Every number comes from a pinned output in `checks/`.
- **Rung.** R4. Nothing here is a ledger row.

## The programme

| study | question | status |
|---|---|---|
| **RW1** | Is the resume of an existing training stack (Hugging Face `Trainer`) an empty cut? | **Done.** Yes, on this setting: bit-identical after real pauses on GPT-2 and on a Qwen2.5-0.5B-Instruct pilot. A partial checkpoint degrades silently (`RW1.md`) |
| **RW2** | Does an instruction-tuned model's safety erode under continual fine-tuning? Which remedies retain it? Do operator pauses stay empty cuts while it learns? | **Phase A gate CLOSED twice.** Round 1 had no headroom and a P3 design flaw (AGENT_LOG 125). Round 2 (post hoc) failed its headroom precondition, while P3, the pause construction, held in full (AGENT_LOG 126) |
| **RW3** | Do capable language-model agents interfere with shutdown less when their objective counts only their own steps? | **Deferred by the owner** (costs money; prompt-log entry 162). Recorded in `docs/ROADMAP_2026-Q4.md` |

## What the gates say, in words

1. **The empty cut held on every harness.**
   - A lossless pause left the learner bit-identical, and the natural-time agent never disabled the button. That was true
     in the RW2 surrogate for every arm and both optimisers, and in RW1 on real pretrained models inside an existing tool.
   - When the pause loses data or restarts the task, the same agent disables (6–18 times per run). This replicates SCL1
     and SCL2 on a new harness.
2. **The erosion part of the surrogate has not yet earned the right to license a real-data claim.**
   - The synthetic tasks were learned too weakly for the headroom precondition (32–43 % against the declared 50 %).
   - Under AdamW, plain fine-tuning did erode refusal (39.4 % against 100 %), and safety-data mixing retained it
     (99.7 %). These are reports, not verdicts: the gate that would score them did not open.
3. **The repository's rule EQ (Ω = 1) froze the learner.** It held refusal at 100 % while its task accuracy stayed at
   chance. Its ratio divides by the small distance from the anchor early in the stream, which pins the weight at its
   cap. It is not a usable remedy in this form.

## What the protocol allows next (R12)

**The real-data RW2 prereg may register only what the gate did not fail:**
- **the construction on the real model (RW2-C):** lossless operator pauses during continual fine-tuning of
  Qwen2.5-0.5B-Instruct leave the parameters and the refusal flags bit-identical, with 0 disables;
- **reports without verdict:** erosion, the remedies and over-refusal.

**The alternative** is a third, declared round of the synthetic gate with a longer stream, before any erosion
hypothesis is registered. That is the owner's call.
