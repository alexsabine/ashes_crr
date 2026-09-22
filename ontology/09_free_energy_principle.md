# 09 — The free-energy principle read with CRR: the clock, the boundary, equanimity, precision (2026-09-22)

Owner request (prompt-log entries 77 and 78): run FEP checks to see whether CRR's clock holds there; read the Dirac
delta as a boundary in time distributing unit mass; read Ω = 1 as equanimity and the offset as grasping or thrashing;
treat precision as a measurable variable; and say which current FEP questions CRR's ontological commitments reach.
This file is a note, not evidence (R8). Every number is printed by `theory/retrodictions/synthesis_batches/batch_27.py`
and `batch_28.py` (pinned outputs beside them, CI-checked; ten SYNTHESIS rows, no data opened, R2). Every label is
computed by the harness from the numbers (R15). Literature is named by name and year only, not fetched (R10):
Friston 2010; Feldman and Friston 2010; Parr, Pezzulo and Friston 2022; Da Costa et al. 2021; Crooks 2007; Kim 2021;
Costa, Santos and Strapasson 2015; Rao and Ballard 1999; Mehra 1970; Hampel 1974 (`docs/citations/fep_2026-09-22.md`).

## 1. The sharper question

Under the free-energy principle a belief updates by natural-gradient descent on variational free energy in the Fisher
metric. Along that flow the Fisher speed obeys dF/dt = −speed², so the arc between two events is the integral of the
speed and the free-energy drop is the integral of its square. The domain therefore has its **own** clock that is not
wall time: free energy. H-L5 in this domain is not "arc beats clock" but "arc beats the clock **and** the free-energy
drop", and it can only do so where the speed varies, that is, under changing precision. That is the question batch 27
asks five times.

| row | system | events | CV(arc) | CV(chord) | CV(clock) | CV(dF or surprise) | outcome |
|---|---|---|---|---|---|---|---|
| 27-1 | Gaussian belief relaxing to a jumping target, precision switching | target jumps | 0.3188 | 0.3188 | 0.2944 | 1.1931 | REDUNDANT-IG |
| 27-2 | Kalman filter, hidden switching process noise | innovation-gated resets | 1.6133 | 0.4782 | 1.8002 | 1.6202 | REDUNDANT-DOMAIN |
| 27-3 | discrete active-inference agent, policy precision 2..16 | policy switches | 1.9247 | 1.1941 | 2.1346 | 2.0013 | WRONG |
| 27-4 | predictive-coding node, clock-scheduled stimuli (negative control) | stimulus switches | 0.2943 | 0.2943 | 0.0413 | 0.5577 | (control: fails, as it must) |
| 27-4 | the same, arc-scheduled stimuli (positive control) | stimulus switches | 0.2387 | 0.2387 | 2.2132 | 0.5455 | REDUNDANT-IG (passes, as the chord) |
| 27-5 | predictive-coding node, sensory precision switching | precision shifts | 0.3699 | 0.7970 | 0.3079 | 0.9490 | WRONG |

What this says, row by row:

- **The relaxation theorem (27-1).** On a complete monotone relaxation the arc *is* the chord (relative difference
  6.40e-13) and equals the jump's own Fisher length (relative difference 2.15e-03 from CV(|J|/s) = 0.3181). Its
  regularity is the stimulus's, precision-free by construction; the free-energy drop carries the precision, the arc
  does not. The bound arc² ≤ clock × dF (Cauchy–Schwarz) held on every interval. H-L5 fails here (CV(arc) above
  CV(clock)) for the domain's reason, not CRR's.
- **The linear-Gaussian case (27-2).** Between gated resets the arc and the accumulated surprise are the same clock
  within tolerance (relative difference 4.30e-03): both add up the noise-driven wiggle of the posterior step by step.
  The steadiest quantity is the chord (CV 0.4782): what is regular between resets is the displacement, not the
  travel.
- **The agent (27-3).** The arc beats the trial count and the surprise, but the chord beats the arc (1.1941 against
  1.9247), and the verdict is stable across the two precision ranges. A policy switch is the belief crossing the
  decision boundary, so the displacement between crossings is set by the boundary: the domain's own decision rule,
  which the arc merely inherits. H-L5's content is the travel; the travel loses.
- **The controls (27-4).** The instrument behaves in this domain as in the battery: clocked stimuli defeat the arc,
  arc-paced stimuli pass, and the pass is the chord's as much as the arc's (relative difference 3.60e-11).
- **Attention (27-5).** With precision shifts as the events, the arc per dwell is dwell time times a
  precision-dependent speed (CV of the mean speed 0.1671) and inherits both variabilities: it is less regular than
  the clock. H-L5 fails on the event kind the FEP itself names.

**Verdict on the clock.** In five FEP systems CRR's clock never beat the domain's own clock by its own content. Where
the arc was regular, the chord was regular for the domain's reason (a monotone relaxation, a boundary crossing);
where the speed varied, the arc inherited the variation. This is the same finding the synthesis batches recorded in
some fifty other fields (`03_review_of_findings.md`), now in the domain whose own mathematics is closest to CRR's.

> Free energy is the brain's own stopwatch. We asked whether CRR's ruler (how far a belief travels) keeps steadier
> time than that stopwatch. It did not, in any of five toy brains. Where the ruler looked steady, it was because the
> straight-line distance was steady, and a straight line is not CRR's idea.

## 2. The boundary in time, equanimity, precision, memory, curiosity (batch 28)

| row | proposition Q | outcome |
|---|---|---|
| 28-1 | a Dirac-precision datum is a cut: the belief's Fisher arc concentrates at the deltas and the occasions between them empty | WRONG |
| 28-2 | Ω is a precision dial: below 1 the datum wins (thrashing), above 1 the prior wins (grasping), at 1 the belief rests where it is | WRONG |
| 28-3 | precision is measurable: the A1′ unit of the innovation record recovers the model's precision under outliers | WRONG |
| 28-4 | a bounded mean (A6) tracks a switching contingency better than accumulated counts | ADDS |
| 28-5 | the epistemic term of expected free energy is half the expected squared Fisher chord | PROPOSES |

**The Dirac delta as a boundary in time (28-1).** The owner's reading is the FEP's infinite-precision observation,
and the domain already states the unit mass: the Kalman gain at the deltas reaches 0.9995 at precision 10⁴, so the
datum's whole mass lands at the instant. What the row found is where the *belief's change* lives: not at the cuts
(0.1922 of the total Fisher arc at precision 10⁴, rising from 0.0177 at precision 1) but in the twenty steps after
each cut (0.3495), because the delta collapses the belief's variance and the ordinary observations re-inflate it, and
in the Fisher geometry that re-inflation is travel. The jump's own length grows as the log of the precision ratio
(5.8341 measured against 5.4816 from the variance-collapse closed form). So the boundary distributes the datum's mass
at once and spreads the belief's change over the occasion that follows. A3's "the jump is the cut, not content" is
right about the datum and wrong about the belief.

**Ω = 1 as equanimity, the offset as grasping or thrashing (28-2).** On a one-dimensional prior–datum node with exact
gradient norms the owner's dial holds: below 1 the belief goes to the datum, above 1 to the prior, and at 1 it rests
wherever it starts (at the prior when started there, at 0.5 when started at the midpoint). With the **registered**
estimator (an exponential moving average, smoothing 0.9) the dial breaks above 1: Ω = 1.41 and Ω = 2 oscillate around
the prior (spread over the last half 0.3594 and 0.1128 against 0.0649 at Ω = 1), so the offset above 1 is not
grasping the prior but thrashing around it. Equanimity at Ω = 1 is a stalemate, not a compromise: it is not the Bayes
point (0.5000 at equal precision) and not the fixed-weight point (0.5000), and with the precision ratio raised to 4
the Bayes gain moves to 0.8000 while the rule at Ω = 1 rests at 0.2204. The rule does not see the precision; the
one-dimensional knife edge of `theory/checks/omega_sweeps.txt` [2] is what the FEP reading meets.

**Precision as a measurable (28-3).** The A1′ unit (robust scale of the detrended innovation residual) read as a
precision does two things a prereg must state. On a record with 5 % outliers at ten times the noise it over-reads
the clean innovation variance by 15 % on average (ratios 1.0642 to 1.2036 over observation variances 1/16 to 16),
because the outliers kick the non-robust filter and the innovations after a kick are genuinely larger; the sample
variance, which is how a predictive-coding node estimates precision, reads 5.291 times the clean value. On the clean
record the unit under-reads by the registered detrender's leverage on white noise (0.7403 measured, 0.7446 from the
centre Savitzky–Golay weight): A1′'s unit on a white record is the residual scale, not the noise scale. Precision is
measurable, and CRR's unit measures the filter's actual precision rather than the model's nominal one, with a known
factor.

**Memory (28-4).** A6's "never an accumulated count" is the one CRR commitment that read ADDS here. On a Bernoulli
contingency switching between 0.8 and 0.2 at rate 0.005, accumulated Dirichlet counts reach a mean absolute error of
0.2912, a bounded exponential mean at the registered rate 0.05 reaches 0.0886 (sweep: 0.1569 at 0.01, 0.1166 at
0.2), and the exact two-state filter, which knows the levels and the switch rate, reaches 0.0333. A6 names the
practice (active inference forgets counts by a decay in practice) and the domain owns the optimum; the rate is a knob
A6 does not fix, and it was chosen in sample. ADDS is a candidate for a named expert, as the class requires.

**Curiosity (28-5).** The epistemic value of an action (expected information gain) and half the expected squared
Fisher chord of the belief update agree to 5.11e-02 on average and within 0.074 at worst. CRR's vocabulary reaches
the epistemic drive, and information geometry owns it (KL = d²/2 + O(d⁴)). The surplus S = C − C*, the part of the
belief's travel that buys no information, is a proposition for a later row.

> Four ideas were tried on toy brains: that a perfectly sharp fact is a cut (half right: the fact lands at once, but
> the mind keeps moving afterwards); that "equal pull" is a balanced mind (no: it is a rope that does not move,
> wherever the knot happens to be, and with the real estimator it wobbles); that the wobble in your predictions
> measures how much to trust them (yes, with two known corrections); and that a memory that fades beats one that only
> adds up (yes, and the best fading rate is how fast the world changes). Curiosity turned out to be a distance
> squared.

## 3. Which current FEP questions CRR's commitments reach

- **The event structure of belief updating.** Active inference has policies, precision shifts and resets but no
  clause saying when an occasion ends. CRR's A3/D5 supplies one, and batch 27 shows the arc-between-cuts version
  does not beat the domain's own clock. The chord version (displacement between decisions is set by the decision
  boundary) is the domain's own rule.
- **Precision as the unit of change (A1′).** Feldman and Friston's "attention as precision" and CRR's "resolvable
  step" are the same number seen from two sides, with the two corrections of 28-3. This is the one place the two
  frameworks share an operational definition, and it is a shared one, not CRR's.
- **Forgetting and the settled past (A6, A7).** The FEP's learning of concentration parameters accumulates; CRR's
  regeneration is a bounded mean. 28-4 is the only ADDS, and its content is a decay rate the domain's optimal filter
  already sets from the world's switching rate. A study that learns the rate online (an HMM filter that must infer
  its own switch rate) is the fair next comparison.
- **The knife edge.** The FEP's aberrant-precision story (over- and under-precise priors) is a gain between 0 and 1;
  CRR's Ω = 1 is a stalemate at the current position and the offset is a two-sided instability with the registered
  estimator. Nothing here recommends Ω = 1 as a model of a balanced mind.
- **Tense (A7/A8).** No row could be formed: the FEP's generative model treats past and future as one joint
  distribution, and CRR's settled past and open present would need an active-inference agent whose past beliefs are
  frozen and whose future has no content. That is the gate for tense named in `05_next_steps.md`, still unbuilt.

## 4. Tally and standing

Batch 27: 0 ADDS / 0 PROPOSES / 2 REDUNDANT-IG / 1 REDUNDANT-DOMAIN / 2 WRONG. Batch 28: 1 ADDS / 1 PROPOSES /
0 REDUNDANT-IG / 0 REDUNDANT-DOMAIN / 3 WRONG. No ledger row exists or is proposed from this file; retrodiction and
synthesis rows are not ledger rows (CLAUDE.md §7). The one ADDS goes to the expert protocol with the two earlier
candidates (`05_next_steps.md`).
