# Declaration 3 — the redesigned gate (a post-hoc redesign, committed and pushed before its first full run)

Owner request, prompt-log entry 107. The anchor is the push timestamp of the commit that adds this file. The script is
`Adam_SGD/checks/drift_battery_2.py`. A smoke run on thinned grids (two seeds) checked that the code runs; its output was
discarded unread.

**This is a post-hoc redesign.** Declaration 2's battery ran, its output is pinned (`checks/drift_battery.txt`), and its
gate is CLOSED under its own rule. Everything below was designed after seeing that output. Any result here is weaker
evidence than a pre-declared one, and is labelled "post hoc" wherever it is quoted.

## Why a redesign, and why only these changes

Declaration 2's positive control could not have been passed by any arm. That is an instrument defect, not a verdict on the
rule; under CLAUDE.md §3.3 a positive control that fails means "the instrument cannot see the effect". AGENT_LOG 92
records the diagnosis.

1. **No headroom.** With F = 16 H, the true objective's optimum sits near the starting point. So a constant with a tiny
   learning rate, which barely moves, scored 3.3545 against 3.2775 for the oracle that knows the units. That is 0.977, and
   the threshold for AHEAD was 0.9. The ratio rule equalled the oracle (1.000) and beat the constant on 10 of 10 held-out
   seeds, but it could not clear a threshold the oracle itself could not clear.
2. **Grid edges.** Chosen learning rates sat on the bottom edge for the constant and on the top edge for the rule.

**The fixes.**
- **The drifting two-task worlds use make_model(mismatch = 1).** The past term is drawn like the present one, so standing
  still is far from optimal.
- **Every world prints its headroom,** h = oracle / best constant. A world is DECISIVE for a win only if h ≤ 0.9; otherwise
  it reads UNDECIDABLE-FOR-WIN.
- **Every grid is extended in both directions,** and every chosen setting carries an EDGE flag.
- **The gate's drifting world is UNDECIDABLE,** rather than open or closed, if its headroom exceeds 0.9 or any chosen
  setting (constant, ratio rule or oracle) sits on an edge.

**Everything else is unchanged:**
- the units reading with scaled noise, with the low-signal world T3′ unscaled;
- 10 tuning seeds and 10 held-out seeds;
- the arms, the labels, the eight-task sequences T1 and T2, the optimisers, and the sensitivity design.

The changes do not favour either arm:
- the grids widen for both;
- the headroom check limits what any arm can claim;
- T1 and T2, where the rule lost by 24–50 %, are rerun on the wider grids and not otherwise changed.

## Expectations

| world | expected | reason |
|---|---|---|
| G-STAT2 (stationary, c = 16) | ratio TIE; registered TIE or BEHIND; **neither AHEAD** | stationary, so the rule reduces to a constant |
| G-DRIFT2 (units drift 4096-fold) | headroom h ≤ 0.9; ratio rule AHEAD, near the oracle | Declaration 2 showed ratio = oracle; now the oracle has room |
| T0′ (wandering units) | ratio AHEAD if its headroom allows; the same under momentum and decoupled Adam; coupled Adam open | the mechanism, not monotone |
| T1 (calibrated eight-task sequence) | **BEHIND** | λ = 1 is exact Bayes; equal pull ignores the accumulated past |
| T2 (miscalibrated eight-task sequence) | **BEHIND**, unless the wider learning-rate grid changes it | Declaration 2: 1.239–1.500 on 0 of 10 seeds; the oracle's headroom there was 0.928 |
| T3′ (low-signal past) | open; BEHIND if AS3b's failure mode carries over | AS3b |

## What the outcomes mean

- **Gate OPEN, T0′ AHEAD, T1 and T2 BEHIND.** The rule, or the ratio family if only smoothing 0 wins, has a narrow niche
  on synthetic worlds. The niche is a penalty or replay term whose units drift within a run, in a two-term balance.
  - It loses in the realistic continual-learning setting where importance accumulates over many tasks.
  - That loss is the more important result for a frontier lab. It says what any real-data study must include, and it
    says the equal-pull principle needs revising for accumulating pasts: a new hypothesis, declared separately, not
    added here.
- **Gate UNDECIDABLE.** The redesign still cannot see the effect, and the rule's niche remains unshown.
- **Gate CLOSED.** The rule does not win even where the units drift by construction with room to win. By R12, the
  equanimity rule stops here in this operationalisation.
