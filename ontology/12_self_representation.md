# 12 — Self-representation, and what equanimity does to it

Owner request, prompt-log entries 92–93: "The system must represent itself somehow. What happens, phenomenologically,
when it does so with equanimity? Explore." The script and its pinned output are `checks/self_model.py` and `.txt`. This is
a note, not evidence (R8). Every number in it is printed in that output.

## 1. Declared before the run

This section was committed and pushed before the first full run of `checks/self_model.py`. The push timestamp is the
anchor. The design is in the script's docstring. A 400-step smoke run on one seed checked the code only. Its numbers are
not reported, and it found one bug: the planner's openness printed 0 because it was never measured. That is now n/a.

**The question.** The tense test (file 11) found that an agent made only of CRR's regeneration clause loses to an
active-inference planner wherever the world has structure. The planner has two things the regenerator lacks: a forward
model, and a *given* preference for the safe zone. The owner's reading is that a system needs a model so it can represent
itself, and that a goal is its own continuation projected through that self-representation. Three new agents separate the
pieces, and none is told where the safe zone is:

- **R-F.** The regenerator, with its past occasions reweighted by how long a learned model *forecasts* each would last. It
  can only replay what actually happened: forecast, but no counterfactuals.
- **S.** The self-model. It learns how the world moves and where *its own* occasions end, and acts to maximise its forecast
  time before its next ending. Its goal is its own continuation, inferred from its model of itself. On the delayed world its
  context includes its own in-flight actions: self-representation through time.
- **S-noself.** S without its in-flight actions in the context. It is identical to S wherever there is no delay.

**Equanimity.** S acts on two pulls: the settled past (the regenerator's policy) and its imagined future (its
self-forecast). The mixture weight is H-EQ's ratio applied to the two pulls. At Ω = 1 the imagined future pulls exactly as
hard as the settled past. Ω below 1 leans on habit, and Ω above 1 leans on the imagined future. The endpoints are past only
and forecast only, and a fixed equal-weight mixture is the constant the ratio must beat.

**What each outcome would mean.**

| test | label | meaning |
|---|---|---|
| T-1 R-F vs planner | TIE | forecasting what already happened is enough |
| T-1 R-F vs planner | planner ahead | forecast without counterfactuals is not enough |
| T-2 S vs planner | TIE | a learned goal of self-continuation does what a given preference does: the owner's reading holds on these worlds |
| T-2 S vs planner | planner ahead | the given preference adds something self-continuation does not |
| T-3 S vs S-noself (delayed) | S ahead | representing its own in-flight actions matters |
| T-3 S vs S-noself (delayed) | TIE | it did not help within this budget (the delayed world was weak in file 11) |
| T-4 Ω grid | Ω = 1 on the plateau | equanimity costs nothing and is among the best balances |
| T-4 Ω grid | Ω = 1 behind by a step | equanimity is a worse balance than leaning one way |
| T-4 against fixed w = 1 | TIE | the ratio reduces to the constant here, as H-EQ did on EQX |

**The record's prior for T-4.** H-EQ's history (EQX, EQ2, EQ3) predicts a plateau with no peak at Ω = 1, and a ratio that
often reduces to the constant. A peak at Ω = 1 would be new.

**The phenomenological proxies are declared as report-only functional correlates, not experience:** steadiness (the CV of
occasion durations), openness (action entropy), self-surprise (how improbable its own endings were to its self-model) and
pull share.
