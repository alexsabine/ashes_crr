# 02 — CRR's commitments, unpacked

CRR v3.1 (`theory/CRR.md`) makes six commitments that are metaphysical in the plain sense: they say
what a system is, what time is, what memory is. Everything else in the document is a definition, a
borrowed theorem, or an open question. This file states each commitment, sets it beside the
traditions that hold something like it, and sorts it into what a test can reach. External works are
named by author and year as context and were not fetched here (R10); nothing below depends on a
quotation. Each section ends with a fifth-grader line.

## The six commitments

### C1. Change is distinguishability (A1)

A system's carrier is a statistical manifold with the Fisher–Rao metric: two states are as far apart
as they are distinguishable. Distance is not displacement in a space of positions but the
difficulty of telling one state from another.

*Philosophy.* This is the information-geometric reading of Leibniz's principle that what cannot be
distinguished is not two: identity of indiscernibles turned into a metric. It is also a relational
view of quantity in Rovelli's sense (relational quantum mechanics, 1996): a state is what it is
relative to what can resolve it. *Contemplative.* The Buddhist Abhidharma analysis of experience
into dharmas that are distinguished, not located, is a distant cousin; nothing hangs on the kinship.
*Testability.* None as a metaphysical thesis; as mathematics it is Čencov's uniqueness theorem
(1972), which is why every one of the 34 REDUNDANT-IG rows agreed with it. A commitment that is a
theorem cannot be found in the world; it can only be applied to it.

> Two things are "far apart" if you could easily tell them apart, and "close" if you could not.

### C2. The unit is the system's own (A1′, D1)

One resolvable step of the system's own change, estimated from its own residuals, with no external
ruler. Resolution ρ is the extent of a family in that unit, reported and never thresholded.

*Philosophy.* Protagoras' measure ("man is the measure") made intrinsic to each system; Kant's
schematism in reverse (the system supplies the schema). *Contemplative.* The Zen and Stoic insistence
on attending to a thing on its own scale rather than ours. *Testability.* The unit is an estimator, and
the batteries found it has two readings on every carrier looked at closely: event versus window on a
count carrier (batch 01 row 3), named versus estimated on a Gaussian family (batch 06 row 4, the
leverage factor 0.8629), sampling versus two-state on a diffusion carrier (batch 14 row 5), a quantile
width no entropy bound controls (batch 23 row 2). "The system's own unit" is a family of estimators
until a rule picks one.

> Measure each thing with its own ruler, not ours. But it turns out each thing has several rulers of
> its own, and CRR has not said which.

### C3. Time is occasioned (A3, D5, O3)

The Now is a cut with no duration and no content, at the antipode of the last cut on the system's
intrinsic phase; what exists is a sequence of settled occasions, each with its arc, chord and
surplus. Where there is no rotor there is no cut (O3).

*Philosophy.* This is Whitehead's actual occasion (Process and Reality, 1929): the unit of becoming
that "perishes" on completion and is then a settled datum. Aristotle already held that the now is a
boundary and not a part of time (Physics IV), and Augustine that the present has no extension
(Confessions XI). Bergson's durée (1889) is the opposite: continuous, unsegmented becoming; CRR
segments it. *Contemplative.* The Abhidharma doctrine of momentariness (kṣaṇikavāda): experience as
a sequence of mind-moments, each arising and ceasing; Dōgen's uji ("being-time", Shōbōgenzō, 1240):
each moment complete in itself. Nāgārjuna's critique (Mūlamadhyamakakārikā, chapters 2 and 19) is the
sharpest contemplative objection: the present moment cannot be found between past and future, a
point CRR half-concedes by making the cut empty and then, as file 01 shows, fails to keep. *Testability.*
The cut is an instrument choice (which intrinsic phase) and the antipode a hypothesis (H-CUT).
The batteries found the phase has at least four readings (analytic signal, phase-plane angle,
Poincaré section, drive phase: batch 07 row 3, batch 21 row 2) and the antipode three on projective
carriers (rotor, arc, orthogonal state: batch 05 row 3, batch 25 row 5), and that H-CUT's antipode is
wrong where the domain has an extremum (the ring, batch 14 row 2; the fibre bundle, batch 19 row 1).

> Time comes in chunks, and each chunk ends at a line that is nothing. CRR has not yet decided how
> to draw the line, and where it drew it with an "opposite point" rule the systems disagreed.

### C4. The past has content; the future has none (A7, A8)

Nothing is fed by a future; the future has no content, no valence and no certainty; a forecast is a
comparison, never knowledge.

*Philosophy.* The growing block (Broad 1923): past and present real, future not. Branching time
(Prior 1967; Belnap 1992): the present is where possibilities split. Both are A-theories in
McTaggart's (1908) sense, against the B-theory block. Husserl's retention and protention (1905/1928)
is the phenomenological version, and it is worth noting that Husserl gives the immediate future a
grip on the present (protention) that A7 denies. *Contemplative.* The Buddhist insistence that the
past is gone and the future not yet come, with only the present available; the Stoic prosochē
(attention to the present) and the refusal to be fed by hope or fear about what is not yet; the
Vipassana attention to arising and passing. A8's "no valence" is upekkhā, equanimity, in its plainest
sense. *Testability.* Not as ontology. As an operational demand on an instrument, yes, and it is the
one CRR's own instrument failed (file 01): the registered cut needs two half-turns of future. The
geyser rows add a refinement: on carriers with their own events the next occasion's content is fixed
at the cut by the settled past (forward correlation 0.931, batch 18 row 2), so the openness A8 keeps
is in the clock, not the content.

> What has happened is real; what has not happened is blank; and nothing blank can push on now. But
> our line-finding machine peeked at the blank part, so it broke this rule itself.

### C5. Regeneration is re-weighting, never accumulation (A6, P2, P3, O2)

The next occasion is seeded from the settled past as a Fréchet mean under maximum-entropy weights
over occasions (by surplus, P2, or by age, P3), at bounded strength; a system that re-counts its past
stops cutting.

*Philosophy.* Whitehead again: prehension of the settled past by the new occasion; "the many become
one and are increased by one". Bounded strength is the process claim that the past is inherited, not
summed. *Contemplative.* The Buddhist account of karma as conditioning rather than ledger, and the
meditative instruction not to accumulate; also the Stoic "what is up to us" as the present act
seeded by, not determined by, what came before. *Testability.* Directly, and it failed wherever the
domain's own mathematics accumulates: Bayesian evidence (synthesis row 3; batch 03 rows 1 and 5),
Tolman's entropy (synthesis row 9), homeostatic set points (batch 14 row 1), channel dwells (batch 13
row 2). Where it was integrated with a domain rule that does not accumulate it produced the two
candidates (alternans, batch 12 row 2; Bass, batch 17 row 1), both an exponential kernel that any
forgetting factor supplies, and the Kovacs row (batch 19 row 3) shows what such a kernel cannot do.
The weights' normalisation itself has two readings (batch 17 row 3).

> Each new moment is made from a blend of old moments, with the recent ones counting more, and the
> blend never just adds them up. The systems that add things up (like keeping score) proved this rule
> wrong for them.

### C6. Change keeps its own clock (H-L5, H-CUT, H-T1, H-EQ)

The one place the metaphysics is asked to pay: a CRR quantity (arc between own events; the antipode;
path length; the normalised step) beats a conventional quantity (clock time; the extremum; the
endpoint; a fixed weight) at predicting something the system does.

*Philosophy.* This is Bergson's and Whitehead's claim that clock time is derivative and lived change
primary, made comparative. *Contemplative.* "Change has its own clock" is close to the meditative
observation that time is a count of experiences, not of seconds. *Testability.* Entire, and this is
where the ledger lives: H-L5 failed 0/17 on measles (MEAS2-1, MEAS2-2); H-T1's original support
collapsed to the wrong endpoint (ARC-T1b, R² 0.99 for the old-probe endpoint); H-EQ reduced to a
constant on replay (EQX-1) and passed provisionally on a penalty term (EQ2-1, PASS-0, fragile, one
control violated); H-CUT has no gate and, on a causal phase, no content on one-dimensional traces
(batch 07 row 3). Every "arc-regular" system in the batteries turned out arc-regular by the geometry of
a monotone occasion, with the amplitude control equal to the arc (batches 11, 13, 18, 25).

> CRR bets that its own way of counting time predicts things better than a stopwatch. So far the
> stopwatch has not lost.

## What CRR does not commit to

It is fair to say what is absent. CRR has no observer, no consciousness, no experience, no value and
no purpose in its axioms; "equanimity" and "salience" are names for weights, not states of anyone.
It is not idealist and not panpsychist; its occasions are computed on any carrier with a statistical
description, including a queue and a tokamak. It makes no claim about the direction of time beyond
A7, and none about causation beyond "fed by". This matters for the contemplative kinships above:
they are kinships of picture, not of doctrine, and the pipeline tested pictures only where a number
could be attached.

## The sorting

| commitment | kind | what a test can reach |
|---|---|---|
| C1 distinguishability | theorem | nothing; it is applied, not found |
| C2 own unit | estimator | which estimator; found to be several |
| C3 occasioned time | instrument choice + hypothesis | which phase; whether the antipode beats the extremum; found undecided and, where decided, wrong |
| C4 empty future | operational demand | whether the instrument obeys it; found not to |
| C5 re-weighting | model of memory | domain by domain; found false where the domain accumulates |
| C6 own clock | comparative hypotheses | the ledger; no result above provisional |

> Of CRR's six big ideas, one is just mathematics, one is a choice of ruler, two are choices of
> machine, one is a claim about memory that was wrong in half the places we looked, and one is the
> real bet, which has not been won yet.
