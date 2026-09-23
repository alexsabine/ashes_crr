# Declaration — the cut δ(Now) as a rupture detector (committed and pushed before the first full run)

Owner request, prompt-log entry 104: "In the IP claims, the Dirac delta of Now was used as a rupture detector on chaotic
systems. I still need to provide the applied use case." The anchor is the push timestamp of the commit that adds this
file. The script is `Rupture_Detection/checks/rupture_checks.py`, and its docstring holds every constant.

A smoke run (3 null and 3 change runs per carrier, 80 periods) checked that the code runs. Its output was discarded
unread. No constant was changed after it.

## What this is and is not

- **Not a test of the EPO application.** The application's text is not in this repository. The test is the one reading
  of "δ(Now) as a rupture detector" that theory/CRR.md v3.1 supports:
  - the cut A3, δ(Now) = δ(u(t) − u(t_n) − L/2), marks occasions on the carrier's intrinsic phase;
  - the occasion numbers (the arc C and the surplus S) are monitored;
  - a change in them is the alarm.
- **Why not the older law.** The older "rupture when C·Ω = 1" law was removed from v3.1
  (`ontology/checks/delta_now.txt` [2]), so it is not used.
- **What kind of evidence it gives.** The carriers are synthetic, and the ground truth (when the dynamics changed) is
  known. This is a mechanism check at rung R4, not a ledger row and not a finding.
- **The phase is computed offline.** The analytic phase uses the whole record, so this is an offline detector. An online
  device needs a causal phase estimator, which is not tested here.

## The comparison (R7: baselines that can win)

The same CUSUM and the same matched false-alarm rate (5 % over the monitoring stretch, calibrated on 40 null runs per
carrier) are run on four windowings:
- **δ**: occasions between antipodal cuts, with features C and S.
- **clock**: clock windows of the same mean length, with features C and S.
- **peak**: occasions between detected extrema, with features C and S. This is the extremum cut that H-CUT sets against
  the antipode.
- **ews**: one-period clock windows with variance and lag-1 autocorrelation. These are the standard early-warning signals
  (Scheffer et al. 2009).

The score is the median delay, in mean periods, from the change to the first alarm after it. Early alarms and misses are
censored at the remaining span. The label is δ/best-baseline: at most 0.8 reads AHEAD, at least 1.25 reads BEHIND, and
anything between reads TIE.

## Expectations, carrier by carrier

| carrier | what it is | expected | why |
|---|---|---|---|
| NC1 | sine + 2nd harmonic, constant speed | not AHEAD (**must**) | a clock window and an occasion hold the same stretch of cycle |
| NC2 | NC1 with amplitude jitter | not AHEAD (**must**) | the clock is the regular one (H-L5's AM control) |
| PC1 | NC1 with speed jitter | AHEAD (**must**) | an occasion holds one half-turn whatever the speed; a clock window does not |
| T1 | Rössler x, natural speed | TIE | Rössler is phase-coherent; its phase speed varies little |
| T2 | Rössler x, speed-jittered | AHEAD | the PC1 mechanism on a chaotic orbit |
| T3 | Lorenz z, natural speed | open | loop times vary near the saddle, so the clock may be irregular enough for δ to gain |
| T4 | Lorenz z, speed-jittered | AHEAD | the PC1 mechanism |
| T5 | ECG-like beat with heart-rate variability 0.1 | open | the analytic phase of a spiky beat may not advance one turn per beat ([R0] reports it); the peak cut is natural on a beat and may win |

**The gate.** NC1 and NC2 must not read AHEAD, and PC1 must read AHEAD. If the gate is closed, the detector's advantage is
not about the cut, and no applied use case may rest on this operationalisation. The battery then says so, and the
applied-use-case note reports it.

**Sensitivity.** Two further settings are varied:
- the CUSUM drift k ∈ {0.25, 0.5, 1};
- the change size: primary or secondary. The sizes are harmonic 0.30 → 0.36 or 0.45; Rössler c 5.7 → 5.4 or 5.0;
  Lorenz ρ 28 → 30 or 33; T wave 0.30 → 0.36 or 0.45.

A carrier whose label flips in more than one of the five non-main cells is FRAGILE.

## What each outcome means for the applied use case

- **Gate open, with T2, T4 (and T5) AHEAD.** The measurable technical effect is shorter detection delay at a matched
  false-alarm rate for a change in an oscillatory physical system whose rate varies. Examples of such systems are a heart
  with rate variability, a machine running up or down, and a combustor or plasma with drifting frequency.
  - That effect belongs to a known family: angular resampling and order tracking in machine monitoring, including
    tacholess order tracking from the Hilbert phase.
  - So the note must name that family and say what, if anything, the cut adds beyond it.
- **Gate open, but the chaotic carriers only TIE.** The cut has no advantage on natural chaotic speeds. The applied case
  must be a system with an external rate drift, not "chaos" as such.
- **Gate closed.** This operationalisation gives the application no technical effect, and the note says so plainly.

The note that follows the run, `Rupture_Detection/RUPTURE_DETECTION.md`, maps the outcome to the EPO's criteria (Guidelines
G-II 3.3: a specific technical purpose; Art. 123(2): nothing added beyond the application as filed). It is information, not
legal advice.
