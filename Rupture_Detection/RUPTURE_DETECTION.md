# The cut δ(Now) as a rupture detector: the gate is closed

**Status.** This is a note, not evidence (R8). It was written on 2026-09-23 at the owner's request (prompt-log entry 104),
after the battery `Rupture_Detection/checks/rupture_checks.py` ran. The design and expectations were declared in
`DECLARATION.md` and pushed at 2026-09-23T05:01:47Z, before the run.

**Sources.** Every number below is printed in `Rupture_Detection/checks/rupture_checks.txt`, which is pinned and
CI-checked. The literature is recorded in `docs/citations/continual_learning_2026-09-23.md` §C–D.

**What kind of evidence this is.** Synthetic carriers with known change times: a mechanism check at rung R4. It is not a
ledger row, and it is not a test of the owner's EPO application, whose text is not in this repository.

> In plain words. We built a smoke alarm that listens to a machine's rhythm and checks each half-beat for a change. Before
> trusting it, we tried it on a test machine built so that our alarm should win. It did not win. An ordinary alarm that
> times each beat from its peaks was faster. So we cannot say our alarm is better, and we stopped there, as the rules say.

## 1. The answer first

- **The gate is CLOSED.** The positive control PC1 is a sine whose speed wanders, with a change in its shape half-way. On
  such a carrier, sampling at the cut should win by construction (H-L5's mechanism), and here it does not.
  - The cut-based detector's median delay is 100.000 periods, and it detected the change in 8 of 40 runs.
  - The extremum (peak) detector's median delay is 6.917 periods, detecting in 38 of 40.
  - The ratio is 14.458, which reads BEHIND.
  - The two negative controls behaved as required: NC1 reads BEHIND and NC2 reads TIE, so neither is AHEAD. But both are
    FRAGILE.
- **No chaotic carrier reads AHEAD in the main cell.** The Rössler (T1, T2) and Lorenz (T3, T4) carriers read TIE. At the
  main settings, nothing detected the primary change in most runs:
  - on Rössler the cut detector found it in 0 of 40 (natural speed) and 3 of 40 (jittered);
  - on Lorenz it found it in 6 of 40 and 2 of 40.
- **The cut detector's only wins are at the larger change on Lorenz.** At the secondary change (ρ 28 → 33) it reads AHEAD
  in all three drift settings on both Lorenz carriers. At k = 0.5 its median delay is 12.040 periods against 100.000 for
  the best baseline (T3), and 9.688 against 104.167 (T4).
  - Those wins also carry early alarms: 9 of 40 and 4 of 40 runs alarmed before the change.
  - They are the reason T3 and T4 are FRAGILE. They are not the registered main cell.
- **On the ECG-like beat (T5) the extremum detector wins by a factor of 190.297.**
  - Its median delay is 1.095 periods, detecting in 37 of 40. The cut detector's is 208.333 periods, detecting in 3 of 40.
  - This holds in all six cells.
  - The beat's analytic phase advances about twice per true half-turn (1.9997), so the cut falls four times per beat and
    divides each beat inconsistently. The peak detector cuts once per peak.

| carrier | main-cell label | δ median delay (detected) | best baseline, median delay (detected) | δ / best | sensitivity |
|---|---|---|---|---|---|
| NC1 sine, constant speed (must not be AHEAD) | BEHIND | 100.000 (5/40) | clock 1.000 (36/40) | 100.000 | FRAGILE (3 of 5 flip) |
| NC2 amplitude jitter (must not be AHEAD) | TIE | 100.000 (3/40) | ews 85.000 (38/40) | 1.176 | FRAGILE (3 of 5) |
| PC1 speed jitter (must be AHEAD) | **BEHIND** | 100.000 (8/40) | peak 6.917 (38/40) | 14.458 | FRAGILE (2 of 5) |
| T1 Rössler x, natural speed | TIE | 104.167 (0/40) | clock 104.167 (6/40) | 1.000 | not fragile |
| T2 Rössler x, speed jitter | TIE | 108.696 (3/40) | clock 108.696 (1/40) | 1.000 | not fragile |
| T3 Lorenz z, natural speed | TIE | 100.000 (6/40) | clock 100.000 (3/40) | 1.000 | FRAGILE (3 of 5) |
| T4 Lorenz z, speed jitter | TIE | 104.167 (2/40) | clock 104.167 (2/40) | 1.000 | FRAGILE (3 of 5) |
| T5 ECG-like beat, heart-rate variability | BEHIND | 208.333 (3/40) | peak 1.095 (37/40) | 190.297 | not fragile |

A median delay equal to the remaining span (100 to 208 periods, depending on the carrier's realised period) means that
most runs either never alarmed after the change or alarmed before it. Those runs are censored at the span, as declared.

## 2. What the result says, and what it does not

**What it says.** In the one form v3.1 supports, the cut δ(Now) gives a change detector no advantage over conventional
windowings, and it is beaten by the conventional extremum segmentation on the carrier built to favour it. Under the
declaration's own rule, "no applied use case may rest on this operationalisation."

The result fits theory/CRR.md's own caution about A3: A3 "is testable only where the antipodal cut and the peak cut
disagree". Here they disagree on the ECG-like beat, and the extremum wins by two orders of magnitude.

**What it does not say.**
- **Why PC1 failed.** The printed numbers show that both segmentations cut about once per half-turn (R0: 0.9998 cuts per
  true half-turn for the cut, 0.9981 peak cuts per cut). So the difference lies in where in the cycle the cut lands, not
  in how many cuts there are. A diagnosis would be a new declared check.
- **Anything about other statistics or real systems.** It does not say that no statistic sampled at the cut could detect
  a change, or that the cut is useless in real systems.

By R12 no weaker or re-tuned operationalisation is run today. A different detector (another statistic, a causal phase, a
Poincaré section) is a new design. It must be declared and gated on a later day, and it is the owner's decision whether to
pursue it.

**The one positive trace, stated at its size.** On the Lorenz carriers at the larger change, the cut detector was faster
than every baseline, by factors of 0.120 and 0.093 of the best baseline's delay at k = 0.5. But it carried more early
alarms. These are secondary sensitivity cells, not the registered main cell, and the gate is closed. They are not a
result.

> In plain words. There was one situation, a bigger change in one chaotic system, where our alarm was quicker. But it also
> rang too early more often, it wasn't the test we had promised to judge by, and it failed the test machine. So it counts
> as a hint for a future, properly planned test, not as a finding.

## 3. How the detector differs from existing approaches

| approach | what it does | relation to the δ(Now) detector |
|---|---|---|
| CUSUM (Page 1954) | a cumulative-sum change detector on a monitored statistic | used unchanged for every windowing here; the δ detector is CUSUM on statistics sampled at the cut |
| early-warning signals (Scheffer et al. 2009) | rising variance and lag-1 autocorrelation before a transition | the `ews` baseline |
| computed order tracking (Fyfe and Munck 1997) | resample a variable-speed signal at constant shaft angle, then analyse in orders | the same idea as sampling at phase half-turns: prior art for phase-domain sampling |
| tacholess order tracking (review: Sensors 20(23):6924, 2020) | estimate the phase from the signal itself, often with the Hilbert transform | prior art for taking the cut's phase from the analytic signal of the measured channel |
| beat or peak detection | cut at extrema (R-peaks in an ECG) | the `peak` baseline, which won on PC1 and T5 |
| Bayesian online change-point detection (Adams and MacKay 2007) | a posterior over run lengths | not run; a stronger baseline for any future registered test |

The ingredients distinct to CRR are two:
- the oriented half-turn criterion, which cuts at the antipode rather than the extremum;
- the reading of each occasion by its arc and surplus.

The battery tested exactly those ingredients, and the conventional choice did better.

## 4. The applied use case for the EPO application (information, not legal advice)

The owner asked for an applied use case for claims in which "the Dirac delta of Now was used as a rupture detector on
chaotic systems". What this repository can honestly give is below.

1. **The repository's evidence does not support a technical effect for this detector.**
   - Under the Guidelines (G-II 3.3), a mathematical method contributes technical character through a specific technical
     purpose. An applied use case needs a technical effect that holds across the claimed scope.
   - On the synthetic test designed to favour it, the cut-based detector lost to the conventional extremum detector. On
     every chaotic carrier it was at best level in the registered cell.
   - Offering this battery as support would support the opposite of what is needed.
2. **The use case must already be in the application as filed** (Art. 123(2) EPC). This repository does not hold the
   application text. Whatever use case is chosen, the attorney must find its basis there.
3. **Among the candidate uses, the heart-monitoring one is the closest to the Guidelines' own example.** The Guidelines
   cite a neural network in a heart-monitoring apparatus that identifies irregular heartbeats. But on the ECG-like
   surrogate here, the cut divides each beat inconsistently, and the peak detector found a T-wave change 190.297 times
   sooner. If the application describes cardiac monitoring, the attorney should know this result before relying on it.
4. **What could change the picture.** Three things, in order:
   - a new detector design declared and gated on a later day, whose positive control reads AHEAD;
   - then a pre-registered study on real, unseen recordings. Candidates are the PhysioNet Autonomic Aging records
     0061–0120, which are unseen, or an annotated ST-T database, fetched and recorded on the day;
   - Bayesian online change-point detection and beat detection as baselines.

   Only a PASS-1 or better there could serve as post-filing evidence of a technical effect. The Enlarged Board's decision
   G 2/21 allows such evidence (named, not fetched). It cannot add a use the application does not disclose.
5. **Publication.** The owner has told the agent the repository is being made private. The material published here between
   2026-09-15 and the change remains prior art against any new European filing. The US one-year grace period for the
   inventor's own disclosures runs to 2027-09-15 (`Alexander Plan/ALEXANDER_PLAN.md` §11.4).

> In plain words. The patent office wants to see the idea doing a real, specific job better. On our own practice tests the
> half-beat alarm did not do the job better than an ordinary one, including on a pretend heartbeat. So these tests can't be
> the proof. A lawyer needs to look at what the original application says, and any new proof would have to come from a new,
> carefully planned test that the alarm passes first.

## 5. Reproduce

```
uv run python Rupture_Detection/checks/rupture_checks.py > Rupture_Detection/checks/rupture_checks.txt
uv run python Rupture_Detection/build/build_pdf.py
```

The battery is deterministic: every run is seeded, and the process pool uses a fixed ordered map.
