# FED Phase A — the heterogeneous-node (federated personalisation) gate for H-EQ: CLOSED (2026-09-22)

Owner request: prompt-log entry 89 ("more continual learning checks"). A synthetic Phase-A gate, no data, so no R2/R3
issue. The design is the one sketched in the answers to entries 76 and 86. Scripts and pinned outputs:
`theory/checks/fed_heterogeneous_v1.py/.txt` (the first run, kept as run) and `theory/checks/fed_heterogeneous.py/.txt`
(after the one correction round). Both are CI-checked byte for byte. This is a note, not evidence (R8). Every number below
is printed in one of the two pinned outputs.

## The question
One shared anchor model with a centrally computed Fisher F. Several nodes personalise from it under the past term
2F(θ − θ*), with the weight removed. The nodes differ in one registered way. Does one global weight, tuned on a reference
node, fail somewhere, while the registered rule (Ω = 1) holds on every node? And on a node carrying poisoned batches, does
EQ-B hold where the rule does not? The gate needs the first claim to PASS on heterogeneous nodes and FAIL on identical
nodes. It needs the second to PASS on the poisoned row and FAIL on a clean row.

## First run (v1): CLOSED on two design defects
- **No trade-off.** The local classes could be learned without disturbing the anchor. The per-node oracle weight was 1024
  on all five loss-scale nodes, so the global knob was the oracle on every node (behind by +0.0000).
- **The poison statistic was mis-specified.** Poison wrecked every fixed weight on that node, the oracle included
  (error 0.6065), while EQ-B held (0.0281). The v1 statistic asked whether the rule was behind that wrecked oracle.

## Correction (one round, committed to before the rerun; AGENT_LOG 71)
Each node's local world has every class mean shifted, and the metric is the mean of retention error (central classes 0–5)
and local error. That makes the two objectives pull apart. The poison statistic became EQ-B against the rule (gate_EQBM's
comparison). A global-knob-plus-clip arm was added to separate the clip from the ratio.

## Second run: still CLOSED (one violation)
- **The mechanism now exists but costs nothing.** On the heterogeneous loss-scale row the oracle weight moves with the node's
  loss scale: 64, 128, 256, 256, 512 for factors 0.25 to 4. But the error landscape is flat near its floor. The global knob is
  never behind by a step: its worst node is +0.0007 against a step of 0.0100. So FED-1 FAILs where it must PASS. The rule is
  within a step on every clean node, and behind the oracle on all of them (worst +0.0082 at factor 0.25).
- **Identical nodes:** FED-1 FAILs, as required.
- **The poisoned node:** every fixed weight is wrecked (oracle 0.2097) and the rule is too (0.2454). EQ-B holds at 0.0014,
  so FED-B PASSes, as required. **The global knob with the same clip holds too, at 0.0011.** The clip does the work, not
  the ratio. EQ4 already has that arm (`fixedclip`) and will test it on unseen carriers.
- **Input-unit heterogeneity (informational):** nothing for the rule to fix. The global knob is within +0.0002 of the oracle
  on every node.

## What this means
No federated H-EQ study will be pre-registered from this gate (R4; R12's spirit). On this surrogate, heterogeneous loss
scales do move the best weight roughly in proportion, as the rule's mechanism says. But the cost of one global weight
stays below one resolvable step, so the rule has nothing to win. The safety-shaped part survives only as the clip, which
works equally well with a fixed weight.

A harder surrogate might open the gate: one where the error floor sits well above a step. That would be a new design,
declared before it is run, and it is the owner's call. Tuning this surrogate until it passes is exactly what the protocol
forbids in spirit.

## What a surrogate would have done
This note is the surrogate. The gate table is the last block of `theory/checks/fed_heterogeneous.txt`.
