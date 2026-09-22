# Ω = 1 on existing mathematics: Bayes, the two-task quadratic, the Kalman filter (2026-09-22)

Owner request (prompt-log entry 69): comprehensive sweeps of the Ω = 1 equanimity rule on existing
mathematics before the continual-learning sweeps; check the claim that there is a threshold either side
of 1 and that 1 is the Bayes optimum; check the Kalman filter tuned against the fixed-parameter rule.
Every number here is printed by `theory/checks/omega_sweeps.py` (pinned output beside it, byte-identical
on rerun, CI-checked). External works are named as context, not fetched (R10). This is a note, not
evidence; the ledger is unchanged by it.

## 1. Is Ω = 1 the Bayes optimum?

Setting: a present batch (n_p samples) and a past batch (n_q samples) of a Gaussian mean, unit noise,
flat prior. The posterior mode is the count-weighted mean, and with batch-mean gradients the combination
g_present + w·g_past has fixed point (m_p + w·m_q)/(1 + w), which is the posterior mode iff w = n_q/n_p:
each sample counted once, summed log-likelihoods with weight 1 each. That is the Bayes optimum, and it is
a *constant* fixed by the counts, not a norm ratio.

The Ω rule with exact gradients does something different (the script's part 1): between the two means
the two gradients are antiparallel, so the update is (1 − Ω)·g_present. At Ω = 1 every point between
the means is a fixed point and the learner stays where it started (endpoints 0.1000, 0.5000, 0.9000 from
starts 0.1, 0.5, 0.9, at every count ratio). At Ω = 0.5 it goes to the present mean; at Ω = 2 it goes
to the past mean and chatters there (1.0973), where the past gradient vanishes and the ratio hits its
floor. So Ω = 1 coincides with the Bayes optimum only when the trajectory happens to stop at the
posterior mode, and the rule contains nothing that selects that point. With equal counts the Bayes
weight is w = 1, ER-sum, which is the constant study EQX found the rule reduced to (ledger EQX-1).

## 2. Is there a threshold either side of 1?

Setting: two quadratics in five dimensions, present (θ − a)ᵀH(θ − a)/2 and past penalty
(θ − b)ᵀF(θ − b)/2 with F sixteen times H (the gate's Fisher-scale mismatch), the learner starting at
the past optimum b, learning rate 0.05. Three facts, each computed:

- **A continuum of equilibria at Ω = 1.** The rule's update vanishes only where the two gradients are
  antiparallel, which is the Pareto curve θ(λ) = (H + λF)⁻¹(Ha + λFb), the set of equilibria of every
  fixed weight λ. On that curve the update has norm |1 − Ω|·|g_present| exactly (0.100000 at Ω = 0.9 and
  1.1, 0.000000 at Ω = 1, at all thirteen points tested). At Ω = 1 every point of the curve is
  stationary; off Ω = 1 none is. This is why Ω is a plateau in every study: the rule does not choose a
  point on the front, it stops wherever it first reaches it.
- **A knife edge, not two thresholds, with exact gradients.** With instantaneous norms (no smoothing),
  Ω from 0.25 to 0.71 ends with the past dropped (λ_eff 0.0001, past loss 69.6621), Ω = 1 ends on the
  curve at λ_eff 0.624 (below the stability edge, next point), Ω = 1.41 and 2 end at the past optimum with
  the present never learned, and Ω = 2.83 and 4 oscillate off the curve. The edge is at Ω = 1 exactly.
- **The stability edge of a fixed weight, and what smoothing does.** A fixed λ diverges under gradient
  descent when lr·(h_max + λ·f_max) > 2, here at λ* = 1.2575: fixed λ = 1 converges (total loss 3.2770)
  and λ = 1.5 diverges. With the registered estimator (an exponential moving average of the gradient
  vectors, smooth 0.9, cap 1e4) the lag lets the learner travel further before the norms balance: Ω = 1
  stops at λ_eff 0.0447 (total loss 19.8753), and every Ω above 1 oscillates. With mini-batch noise the
  best Ω is 1 in 11 of 15 cells over three noise levels, three smoothings and three caps, and the
  plateau (grid points within 10 % of the best total loss) has width 2, 1 and 3 at noise 0, 0.5 and 2.
  The cap never binds in this model (0 of 15 cells above 1 % of steps), because the tuned λ here is of
  order 1; the EQ2 regime, with tuned λ in the hundreds and the cap load-bearing, is a different regime.

So the "threshold either side of 1" is, in the exact model, a single knife edge at 1: below it the past
is eventually dropped, above it the present is never learned. The plateau seen on data (EQ2-6, over
0.5–1.41) is what smoothing and mini-batch noise make of that edge.

## 3. The Kalman filter: tuned against the fixed-parameter rule

Setting: the scalar random walk of P4, process variance q, observation variance r, v = √(q/r). The tuned
gain K(v) = (v/2)(√(v² + 4) − v) is the Bayes-optimal fixed weight. The two readings of Ω = 1 that the
batteries found (batch 06 row 3) give two fixed gains: Fisher speed 1 gives K(1) = 1/φ = 0.618034;
equal pull (prior and datum with equal precision) gives K = 1/2, which the Riccati equation places at
v = 0.707107. The normalised-gradient rule applied to the filter update is K = 1/2 at every v: a fixed
gain, not an adaptive one.

Steady-state error variance of a fixed gain, closed form and Monte Carlo (agreeing to the third decimal:
0.6180 against 0.6206 and 0.6153 at v = 1):

| v | K tuned | MSE ratio, K = 1/φ | MSE ratio, K = 1/2 |
|---|---|---|---|
| 0.01 | 0.0100 | 44.9472 | 33.5038 |
| 0.3 | 0.2584 | 1.7905 | 1.4063 |
| 0.707 | 0.4999 | 1.0653 | 1.0000 |
| 1 | 0.6180 | 1.0000 | 1.0787 |
| 3 | 0.9083 | 2.1849 | 3.6698 |
| 100 | 0.9999 | 1708.8220 | 3334.0000 |

The 1/φ rule is within 5 % of the tuned filter only at v = 1 and within 25 % only for v in 0.707–1.414;
the 1/2 rule within 5 % only at v = 0.707 and within 25 % for v in 0.5–1. The tuned gain needs q/r, which
an innovation-based estimator supplies from the data (Mehra 1970, named); the fixed rules do not, and
lose everywhere but at one speed each. Ω = 1 is Bayes-optimal for the filter at exactly one
signal-to-noise speed, and which speed depends on which reading of Ω = 1 is taken.

## 4. What this changes

- **Nothing in the ledger.** No row is edited; these are mathematics, not data.
- **The v3.2 decision list, item 5** ("which Ω = 1", `ontology/05_next_steps.md`) now has numbers on
  both sides: the two readings are K = 1/φ and K = 1/2 on the filter, and on the learner the rule is a
  stop-anywhere-on-the-front rule whatever the reading.
- **The design of the next continual-learning study** (EQ3, `prereg/eq3/PREREG.md`): a Bayes arm is
  added (the Laplace weight λ = 1/2 on the accumulated per-sample Fisher with equal task sizes, the
  constant §1 says Bayes gives), the nine-point Ω grid is run on the EWC arm so the plateau width can be
  measured, and the stability-edge reading of EQ2 is tested again on six unseen carriers with the
  learning-rate and batch perturbations CLAUDE.md §6 asks for.
- **What the rule is, in one sentence.** With exact gradients the Ω = 1 rule is a normalised-gradient
  method with a continuum of equilibria along the Pareto front of the two tasks; it is Bayes-optimal
  only by coincidence, its value on data comes from bounding the penalty step by the present step
  (which keeps it above a fixed weight's stability edge), and its plateau is the estimator's smoothing
  and the mini-batch noise acting on a knife edge.
