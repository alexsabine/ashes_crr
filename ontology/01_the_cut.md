# 01 — The cut: CRR's Now, as computed, needs the future

Every number here is in a pinned output; the row it comes from is given in brackets in the form
`batch NN row k` (files `theory/retrodictions/synthesis_batches/batch_NN.txt`), `synthesis row k`
(`theory/retrodictions/synthesis.txt`), `emptiness row k` (`theory/retrodictions/emptiness.txt`),
`AGENT_LOG n` (`notebook/AGENT_LOG.md`) or `checks fact n` (`ontology/checks/cut_on_a_machine.txt`).
The two facts about the instrument's code are read from `src/crr/instrument/core.py` as it stands.

## 1. What the axiom says

CRR.md A3: the cut "has no duration and no content", fires when the intrinsic phase has advanced
half a turn from the last cut, and "partitions the history into settled past and open future". A7:
"nothing is fed by a future". A8: "the future has no content". The emptiness battery graded the
statements themselves as definitions that hold exactly: a delta in phase has unit integral and zero
support (emptiness row 2), and the settled sum has no terms ahead of Now by construction (emptiness
row 4).

> **For a fifth grader.** CRR says that between one moment and the next there is a line, and the line
> is not a thing: it is not long, and there is nothing written on it. Also, nothing that has not
> happened yet can push on what is happening now.

## 2. What the instrument does

Two facts about the code that computes the cut and the unit:

- `intrinsic_phase` returns the unwrapped angle of `scipy.signal.hilbert(x)`. The Hilbert transform
  is a convolution with 1/(πt), a kernel with no compact support: the phase at any sample is a sum over
  the whole record, samples after the point included.
- `unit_sigma` detrends the occasion statistic with `savgol_filter(stat, 9, 2)`, a centred window:
  four occasions after each point enter the residual whose scale is the unit.

So every antipodal cut in every H-L5 row of this repository was located with samples after the cut,
and every unit σ that scales an arc was estimated with occasions after the occasion.

> **For a fifth grader.** To find the line on a page, our machine read the next page too. To decide
> how big one "step" is, it looked at the next four steps as well. It was peeking.

## 3. How much future the cut needs (batch 21 row 2)

The row re-ran the registered cut on the source battery's own sine with the record ending d samples
after each point, d = 0 being the causal reading.

| future allowed (samples) | phase error, rms (half-turns) | phase error, max | cuts placed |
|---|---|---|---|
| 0 | 0.2832 | 0.6289 | offsets mean +7.29, max 13 samples |
| 5 | 0.1177 | 0.2577 | 21 cuts (not 20) |
| 25 | 0.0476 | 0.1030 | 21 cuts (not 20) |
| 50 | 0.0246 | 0.0683 | 21 cuts (not 20) |
| 100 | 0.0154 | 0.0419 | offsets mean −0.53, max 2 samples |

The causal cut sits 0.146 half-turns from the registered one on average, and the registered cut
settles to within 2 samples only once 100 samples of future, two full half-turns, have arrived. With
the mean known in advance it settles after 50 samples, so the detrender consumes its own share of the
future. On the asymmetric surrogate the causal phase is not a phase at all: 5 cuts where the
registered instrument finds 20. The Poincaré section, which CRR.md names as the alternative intrinsic
phase, places the cuts within 1 sample of the registered ones with no future at all.

`checks fact 5` shows the mechanism at the level of one sample: with the future of a sine altered from
sample 1210 onward, the phase one sample before the alteration changes by 0.1600 half-turns when the
future is removed, 0.2973 when it is scaled by 3 and 0.3152 when it is shifted a quarter turn, falling
to 0.0058, 0.0005 and 0.0066 half-turns 100 samples before; the crossings of a section computed from
the settled samples alone are identical in every case. At a cycle boundary of the periodic transform
(sample 1200) the removed future produces no change at all, which is why the count of half-turns in a
record matters to this instrument.

> **For a fifth grader.** We tried to find the line without peeking. The machine put it in the wrong
> place, about a seventh of a page off, and it only agreed with the peeking machine after it had been
> allowed to read two more pages. A different, simpler rule ("the line is where the wave crosses the
> middle") found the right place without peeking at all.

## 4. The cut carries content in four further ways

Beyond needing the future, the cut as computed is not empty. Each of these is a pinned number; the
mathematics behind them is file 06.

- **The reset jump is at the cut and was counted as arc** (AGENT_LOG 18). In two threshold-reset
  rows the instantaneous reset was inside every occasion's arc, a constant 1 σ that lowers CV(arc) by
  arithmetic; on the rise alone the E-I cells read clock-regular 5/5 where they had read arc-regular
  4/5. The adder shows the same: the halving counted inside the arc lowers CV(arc) from 0.0749 to
  0.0571 (batch 13 row 1), and the sawtooth's class itself flips between "the crash is the cut"
  (CV(arc) 0.5055) and "the crash is content" (0.3114) (batch 18 row 3). `checks fact 4` gives the
  arithmetic: a constant jump of 1 at every cut halves the CV of rises with CV 0.2012 (0.1003, closed
  form 0.4986 of the original).
- **A delta in phase has clock mass** (batch 20 row 5). Integrated against the clock, each cut weighs
  1/|u′(t_k)|: 0.129949 at the first cut of a chirp, matching the composition rule of distribution
  theory to 1.1e-07, and the 28 masses sum to 1.7732 against 1.7267 for the half-turn durations. The
  cut is empty in phase and has a duration in time.
- **On a count carrier the cut's bin holds a constant** (batch 21 row 4). At the bin scale every
  interspike occasion carries 4 (jump counted) or 2 (jump excluded), CV(arc) = 0 whatever the neuron
  does, and on smoothed carriers a Poisson train reads arc-regular at every smoothing scale.
- **The antipode may never come** (synthesis row 4, batch 05 row 3, batch 25 row 5). On a three-level
  system with levels (0, 1, 3) no orthogonal state occurs (minimum overlap 0.2024); on a qubit off the
  equator the three readings of A3 disagree (rotor 3.1417, arc 3.6276, no antipode at θ = π/3); on
  spin-j states the arc reading and the antipode diverge as √(2j). An occasion whose end is defined by
  an event that may never happen is a wait, not a unit of becoming.

> **For a fifth grader.** Four more ways the line was not nothing: when the machine reset with a jump
> right at the line, the jump got counted as part of the page; the line, which has no width on the
> page, still takes time on the clock; when we count clicks, the click's own box always holds a
> number; and sometimes the "opposite point" the line is supposed to sit at never arrives.

## 5. What it means for the ontologies (from the scratchpad discussion, now with the rows)

CRR's A7 and A8 place it with the growing-block and open-future views of time (Broad 1923; Belnap
1992; Prior 1967 as context, not fetched): settled past with content, a contentless future, a Now
that partitions them. It contests eternalism (McTaggart's B-series; the block universe), where a
whole-record quantity is ontologically innocent. The rows bear on this in four ways.

1. **The instrument adopted the block.** The analytic signal defines the phase at t from the entire
   record. Batch 21 says the block does the work: withhold the future and the Now moves by 0.146
   half-turns. A growing-block reading can save this only by separating what is real at t from what is
   knowable at t, but A3 says the cut *does* things at t (settles the occasion, resets C, orients the
   next half-turn), and a cut that acts before it can be located has effects that precede their cause.
2. **The repair costs H-CUT.** The Poincaré section respects A7 (within 1 sample, no future). Batch 07
   row 3 found that under the oscillator's own phase-plane angle the half-turn from a maximum is
   identically the next minimum, so on a causal phase A3 is the peak cut on every one-dimensional
   trace and H-CUT (antipode against extremum) is empty. The choice between phases is a choice between
   keeping the open future and keeping the antipode.
3. **No discreteness of becoming was found.** Every occasion in 335 rows was cut by a phase criterion
   on continuous dynamics, the resolution ρ was reported and never found to be a fact of a carrier, and
   the occasions that needed no antipode were the domain's own events (the adder, the geyser, the
   laser). The rows support a growing block, if anything, over an occasion-block.
4. **The future's openness sits in the clock, not the content, on the carriers with own events.** On
   the geyser the arc of the coming refill is the volume the last eruption released, forward
   correlation 0.931 against backward 0.021 (batch 18 row 2). A8 survives there only as "fixed by the
   past is not content of its own". On Markov carriers the reverse holds: the deep past adds nothing
   beyond the present (batch 24 row 1, I(past; future | present) to 4.4e-16), which is a problem for
   A6, not A8.

> **For a fifth grader.** Some people think time is like a book already written; others think the
> pages are being written as we go and the future pages are blank. CRR is in the second group. But
> the machine it built reads ahead, like the first group. To stop reading ahead we have to use the
> simpler rule, and then one of CRR's other ideas (that the line is at a special "opposite" place, not
> just at the top of the wave) has nothing left to say.

## 6. Where this leaves the axiom

A3, A7 and A8 did not fail in the world. They failed in CRR's own instrument, in a measured way, and
the repair forces a decision the theory has not made: which intrinsic phase is A3's. File 05 gives the
three computations that would settle it, and file 06 the reason no computed cut can be empty.
