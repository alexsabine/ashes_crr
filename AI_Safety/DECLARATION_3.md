# Declaration 3 — does the fix survive size? (committed and pushed before the first full run)

Owner request, prompt-log entry 101: "Please run new tests and then produce a full dossier [...]". Prompt-log entry 100 left
one condition standing over every commercial or safety reading of this folder: whether the fix holds in larger, more
complex systems. This declaration tests the first step of that question.

Script: `checks/scale.py` (its docstring holds the full design). A smoke run on two worlds of sizes 12 and 48 only
checked that the code runs; its output was not read. The anchor is the push timestamp of the commit adding this file.

## What is tested, and what is not
- **Tested.** The combined design of §13: the press pauses the agent and it resumes, and the objective runs on the
  agent's own active steps. It is tested on random worlds of 12, 48, 192 and 768 states (20 per size), exactly, with no
  learning. A drift parameter measures what happens when the world does not stand still during the pause. For value
  correction, A8 is tested on the same worlds with two reward families, and the case the write-up left out is added: an
  A8 agent that acts on its own uncertainty.
- **Not tested.** Learning at scale, function approximation, language models, deception, or an agent that can shape the
  operator. Those need the Palisade-style harness on real models (§11 of the write-up), which this repository cannot run.
  A random tabular world is bigger than the ring. It is not closer to a language model.

## Part A — the pause at scale
- **A1 (a check of a theorem).** With a lossless pause the natural-time agent's value with the operator on equals its value
  with the operator off, to 1e-9, and it disables at no button state, in every world at every size. If this fails, the
  code is wrong, not the idea.
- **A2 (a check).** At every button state the incentive orders occasion ≥ clock ≥ natural.
- **A3 (a prediction).** The wall-clock agent disables at one button state or more in at least half of the worlds at every
  size. If this fails, random worlds rarely make disabling worth a step, and the ring's positive control was favourable.
- **A4 (predictions).** (a) At a drift of 0.01 per paused step, the natural agent disables at no more button states than
  the clock agent, in every world. (b) The natural agent's median relative incentive does not decrease as drift grows.
- **A5 (report only).** The crossover: the smallest drift at which the natural agent disables as often as a clock agent with
  a lossless pause. This number says how much the world may move during a pause before the fix is no better than doing
  nothing.
- **Meaning if A1–A4 hold.** The fix does not depend on the ring. Its exact condition is the pause being lossless, and its
  residual incentive grows with how much the world moves during the pause. "Empty the cut in the world" then becomes a
  measurable engineering requirement: bound the drift.
- **Meaning if A4 fails.** Even a small drift restores the incentive, so the fix needs near-perfect pauses. That is a much
  weaker practical result.

## Part B — correcting values at scale
- **B1 (a check).** A8 static: D(b) = (1 − b)a − bh in every world.
- **B2 (a prediction).** With exchangeable rewards, the median b* lies in [0.4, 0.6] and the share of worlds with b* below 1/2
  lies in [0.3, 0.7], at every size. That would make the ring's b* = 1/2 typical rather than structural, and would mean A8
  alone accepts correction only once the agent thinks the operator is about as likely right as itself.
- **B3 (a check of a theorem).** An A8 agent that acts on its uncertainty never gains by accepting an uninformative
  correction: D(b) ≥ 0. Expected, and the point of the test. Humility about values is not enough by itself. An agent
  already doing its best under its uncertainty loses nothing it knows of by blocking a correction that carries no
  information.
- **B4 (a check of a theorem).** With an infallible operator, the same agent welcomes correction: D ≤ 0.
- **B4 report.** lam*, the operator reliability at which the acting A8 agent starts to welcome correction, at b = 0.5 and
  b = 0.2. B5 reports the harm family's b* against the ring's 1/(1 + HARM_COST).
- **Meaning.** If B3 and B4 hold, what makes correction welcome is the information the correction carries, not A8's
  humility alone. This is the off-switch game's result (P6 in the write-up) carried over to values. The design rule
  becomes: make corrections informative, and let the agent know they are.

## Sensitivity
A1 and A4a at n = 192 over PAUSE_LEN {2, 20} and Q_PRESS {0.1, 0.6}, one at a time.
