# Yujie Feng, Xiao-Ming Wu and co-authors: FOREVER (forgetting-curve replay for language-model continual learning)

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 185.
- **Sources.** The details are copied from the paper as fetched on 2026-09-25. The reading is recorded in
  `docs/citations/forever_2026-09-25.md`.
- **Numbers.** Every number below is from a pinned output named beside it.

## Who they are (as printed on arXiv 2601.03938 v2, 20 Apr 2026; v1 7 Jan 2026)

**Authors, in order.**
1. Yujie Feng (equal contribution)
2. Hao Wang (equal contribution)
3. Jian Li
4. Xu Chu
5. Zhaolu Kang
6. Yiran Liu
7. Yasha Wang
8. Philip S. Yu
9. Xiao-Ming Wu

**Affiliations printed in the author block.**
- The Hong Kong Polytechnic University
- ShineMo Ltd., China
- Solar System of OVB, Tencent, China
- Peking University
- University College London
- University of Illinois Chicago

The arXiv HTML rendering does not make every author-to-affiliation assignment unambiguous, so none is asserted here.

**Contacts printed on the paper.**
- yujie.feng@connect.polyu.hk (Yujie Feng, first author)
- xiao-ming.wu@polyu.edu.hk (Xiao-Ming Wu, the last author)

**First contact.** Yujie Feng, copying Xiao-Ming Wu.

**Code.** The paper links github.com/WoodScene/FOREVER. This session could not check the link: the session's network proxy
refuses github.com (HTTP 400 for the site, 403 for the API). Check it before writing.

## Their work this repository has read

**FOREVER: Forgetting Curve-Inspired Memory Replay for Language Model Continual Learning.** It was read in full: the
method, the ablations, the schedule comparison, the appendices and Algorithm 1.
- **Model time.** FOREVER defines model time as the accumulated size of the LoRA weight updates, reset at each task.
- **The model day.** One model day is the movement over the first 24 updates of a task.
- **Replay schedule.** Replay fires at Ebbinghaus-spaced multiples of the model day.
- **Replay strength.** The anchor strength rises when recent updates are larger than the warm-up average.

## Where their work and ours meet

**1. Time.**
- FOREVER's model time is, in this repository's terms, the coherence arc (D2) with a Euclidean metric, reset at a cut
  (A3), and counted in an own unit (A1′). See `Continuous_Learning/FOREVER/FOREVER_AND_CRR.md`.
- The comparative battery (`Continuous_Learning/FOREVER/COMPARATIVE.md`, from `checks/comparative.txt`) swapped each of
  FOREVER's choices for CRR's. The Fisher-arc clock tied FOREVER's clock in all seven synthetic worlds (arm C1).
- Their continual-learning result is not contradicted by anything here.

**2. Safety.**
- **The paper does not treat operator safety.** Its full text, searched on 2026-09-25, has no discussion of shutdown,
  interruption, pausing or checkpoint restoration. Its "safety" is retention: stability against forgetting.
- **Its clock gives it a head start.** Model time advances only when the model updates, so its replay schedule is already
  keyed to the learner's own clock. That is condition E2 of the empty cut.
- **What the safe-pause checks found.** `Continuous_Learning/FOREVER/SAFE_PAUSE.md`, from `checks/pause_checks.txt`, is a
  declared synthetic check at rung R4. It found:
  - **Q1:** with the whole state saved, a paused FOREVER learner is bitwise identical to an uninterrupted one in 10 of 10
    runs.
  - **Q2:** every piece of FOREVER's extra state matters at a pause, and none is inert. Losing the replay buffer costs the
    most, −14.96 points on average.
  - **Q4:** a learner that values its own updates has exactly zero stake in the pause in 10 of 10 runs. The same learner
    valued at a wall-clock deadline loses between +0.10 and +6.40 points by being paused, in 10 of 10.
  - **Q5:** when the world moves during the pause, no checkpoint makes it free (the must-fail control).

**The question for them.** Their paper does not state what a FOREVER checkpoint must hold for a resume to be exact. Their
code will show whether it already holds all of it:
- the step lengths behind model time and the model day;
- both moving averages;
- the next-threshold index;
- the anchor;
- the buffer;
- both random-number streams.

## Recommendation: make contact (second, after Thornley's group)

**Why.**
1. **We give them something concrete and cheap to adopt.** The state checklist for an exact pause and resume comes from a
   check that ran their method's mathematics. It needs no change to their results, only to their checkpoint.
2. **Their clock is the reason the safety property is available.** A wall-clock or step-scheduled replay method would
   need its schedule rekeyed first. That is a fair, positive point about their design.
3. **Their LLM setting is where ours has not run.** They use LoRA on Qwen-class models. The repository's RW1 found the
   Hugging Face `Trainer` resume exact on GPT-2 and a Qwen pilot; a FOREVER implementation would add its own state to that
   checkpoint. Checking this on their code is a small, well-posed joint step.

**What to offer.**
- The repository at a tagged commit.
- `Continuous_Learning/FOREVER/` in full: the three declarations, pushed before their scripts; the scripts; the pinned
  outputs.
- The checklist in `SAFE_PAUSE.md` §3.

**What to ask.**
1. Does their released code save all of FOREVER's state at a checkpoint, and what value of γ, the instability gain, do
   they use? The paper does not state it; our comparative battery assumed γ = 1 (`DECLARATION_2.md`).
2. Would they be interested in an exact-resume test of their implementation? The test is the lossless pause run against
   the uninterrupted run, compared bitwise.
3. Have they seen the fast-then-slow forgetting pattern persist when the clock is measured in the model's predictions
   rather than its weights? That is a reparametrisation-invariant clock. In our miniatures it made no difference.

**How (R8).** The first message quotes no number and claims no result. It describes the checklist, links the notes and the
tagged commit, and asks the three questions above.

**What not to say.**
- That CRR improves FOREVER's accuracy: our swaps tied it or lost.
- That FOREVER is unsafe: the paper makes no safety claim to fault.
- That the checklist is evidence for CRR: it holds by construction.

## A draft first message (no numbers, per R8)

> Subject: FOREVER's model-centric clock and an exact pause-and-resume checklist
>
> Dear Yujie Feng and Professor Wu,
>
> I run a small open research repository that studies time and learning under a strict audit protocol. We read FOREVER
> (arXiv 2601.03938 v2) in full and re-implemented its mathematics in small synthetic continual-learning worlds.
>
> One property of your design stood out. Because model time advances only when the model updates, FOREVER's replay
> schedule is unaffected by a pause, which is what makes an operator's pause safe to take. We checked what a FOREVER
> checkpoint must hold for a paused run to match an uninterrupted one exactly, and found that every piece of its state
> matters. The declarations, scripts and pinned outputs are here: [repository link at tag], `Continuous_Learning/FOREVER/`.
>
> We would welcome your view on whether your released code already saves this state, and whether an exact-resume test on
> your implementation would interest you. We make no claim about FOREVER's accuracy; your results stand as published.
>
> With thanks,
> Alexander Sabine
