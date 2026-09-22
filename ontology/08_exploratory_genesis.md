# 08 — EXPLORATORY: from emptiness, with CRR as stated; do the line and the circle grow?

**Status: exploratory.** Owner request 2026-09-22 (prompt-log entry 67): start with emptiness and build a
universe with CRR; test whether mathematical forms can appear from the CRR equations as stated; follow the
geometric laws of CRR through line and circle; state wherever a change to the equations as written is
required. This is not a battery, not a retrodiction and not a synthesis row: it has no gate and no verdict.
Every number below is printed by `checks/genesis_from_emptiness.py` (pinned output beside it, byte-identical
on rerun, CI-checked); every "change required" below is one the script printed where a computation returned
nothing, raised, or stayed fixed (R15). Philosophical works are named as context and were not fetched (R10).
Each section ends with a fifth-grader line.

## 0. Emptiness

A carrier with nothing to distinguish is, under A1, a statistical manifold of one distribution: a point,
dimension 0. The script runs CRR's own instrument on it. The arc length of any path is 0 (D2). The unit
estimator rejects the record ("degenerate residual"), so there is no unit and no ρ (A1′, D1). The phase of a
flat record advances 0.0000 rad and the cut finder returns nothing after its start index (A3, O3). And CRR
v3.1 §0 says of itself that it has no equations of motion. So emptiness is stable under CRR as written: nothing
leaves it. The owner's concession is the first change required, and the script prints it as [A0]: **a first
distinguishable state and a first motion must be posited.** CRR cannot produce either.

> With nothing to tell apart, CRR's ruler has no marks, its clock has no ticks, and its line-drawer draws no
> line. Something has to be different from something else before anything starts, and CRR does not say what
> makes the first difference.

## 1. The first distinction: the line, and the circle inside it

Posit one distinction: this / not-this. Under A1 the least statistical manifold with two distinguishable
states is the Bernoulli family, p ∈ (0, 1), with Fisher information 1/(p(1−p)). Everything in this section is
then a theorem, and the script computes it.

- **The line.** The Fisher–Rao length of the whole family, ∫√(1/(p(1−p))) dp from 0 to 1, is 3.1415926536:
  π. In the arc-length coordinate u = 2·arcsin√p the manifold is a geodesic segment from u = 0 to u = 3.1416.
  The first form is a line, and its length is π.
- **The circle.** Written in amplitudes, ψ = (√p, √(1−p)), the family lies on the unit circle: |ψ| = 1 at every
  p to 1.1e-16. The normalisation p + (1−p) = 1 *is* cos² + sin² = 1. The circle is the first distinction's
  normalisation, read in the coordinates the Fisher metric prefers; the Fisher–Rao distance is twice the angle
  on it (d(0, 1) = 3.141593 = 2 × 1.570796), so the manifold is a quarter of a circle of radius 2.
- **Two chords.** Between the pure states there is CRR's chord (D3, the geodesic on the manifold), which is
  the arc of length π, and the straight line through the embedding, which is √2 (radius 1) or 2√2 (radius 2).
  CRR's "line" is an arc of the circle; the straight line is not a CRR quantity at all.

So the line and the circle both appear at the first distinction, and both come from the metric (Čencov),
not from any clause CRR adds. The batteries said this of every REDUNDANT-IG row (file 03 §4); here it is said
of the first two forms.

> Once there is one thing that can be this or that, CRR's way of measuring already draws a line of length π
> and bends it into a quarter of a circle. That is a fact about the measuring, not a new idea of CRR's.

## 2. Motion: the sinusoid, the rotor, and negation as the cut

CRR names one speed, Fisher speed 1 (the Ω = 1 reading of H-EQ, which the batteries found has two readings,
file 05 §2 item 5). The least motion to posit is a geodesic at that speed: in the arc-length coordinate the
geodesic equation is u″ = 0, so u(t) = t, and at the ends of the segment the least continuation is reflection.
The script prints this as the second change required, [A2]: **a law of motion**, which CRR says it does not have.

With it, three things appear at once.

- **The sinusoid.** The reflected unit-speed motion makes u(t) a triangle wave between 0 and π, and
  p(t) = sin²(u/2) equals (1 − cos t)/2 to 2.6e-15. The first distinction moving at CRR's one speed is a
  sine wave in probability.
- **The rotor.** The reflected segment is a circle of circumference 2π (p = sin²(v/2), v = t mod 2π): the
  circle double-covers the line. A3's rotor, which v3.1 assumes "where the system is cyclic", exists here and
  is derived; the script prints [A3a]: **the rotor must be derived, not assumed.** In amplitude coordinates
  the derivation is the sign of √p, which is the same double cover.
- **The cut is negation.** CRR's own instrument on the sampled sinusoid finds the half-turn cuts at p = 0, 1,
  0, 1, 0, 1: the antipode of p is 1 − p. On the first distinction the cut is "not". The first occasions are
  monotone traversals of the whole line with C = 3.141593, C* = 3.141593 and S = 0.000000 (D4).

> Let the one thing move at the only speed CRR knows, bouncing between "this" and "that", and its
> probability traces a perfect wave. CRR's line-drawer then draws its lines exactly at "this" and at "that":
> the cut is the word "not".

## 3. The unit and the count

A1′ gives two readings of the unit, and the perfect first distinction decides between them by breaking one.
The trace reading (an occasion statistic, its residual, a robust scale) has nothing to work on: the amplitude
of every turn is 1, the residual is degenerate, and the estimator rejects the record. The script prints
[A1′a]: **on a carrier without variability A1′ gives no unit.** The point-process reading survives: one cut is
one event is one step, and natural time is the count of half-turns, 1, 2, 3, … The integers appear here, as
file 06 §4 suggested they would: the cut is the successor.

The count is also the only thing in this universe that grows. If the first distinction is *sampled*, one more
outcome after n moves the empirical point by 1/n of the line: the step falls from 0.339837 at n = 2 to
0.003891 at n = 256, and the resolution ρ = π/step rises from 9.2444 to 807.3873, with ρ/n approaching π
(3.1539 at n = 256). Resolution grows linearly with the count.

> CRR's ruler cannot mark a perfect wave, because every wave is the same. But it can count the waves: one,
> two, three. Counting is the only thing that gets bigger.

## 4. Regeneration: the first universe dies of memory

A6 seeds the next occasion from the settled past as the Fisher–Rao Fréchet mean of "occasion contents Φ_m"
under MaxEnt weights, "at a fixed strength κ". Two changes are required before the clause can be run at all,
and the script prints both: [A6a] **Φ_m is not defined** (D5 gives an occasion (C, C*, S) and no content on
the manifold), and [A6b] **κ appears in the prose and not in the formula.** The script runs two readings of
Φ_m: (a) the state at the cut, (b) the occasion's own path mean.

Under either reading the first regeneration is the same: the Fréchet mean of the two pure states is p =
0.500000 (grid argmin and closed form agree), and reading (b) gives 1/2 at once. But 1/2 is the fixed point of
the cut's negation, |1/2 − (1 − 1/2)| = 0.0. An occasion seeded there travels its half-turn and comes back:
C = π, C* = 0.0000, S = 3.141593 = π, the largest surplus the line allows. Regeneration seeds the universe at
the one state the cut cannot distinguish from its antipode.

The recurrence under reading (a) with P3 age weights q^age shows how fast:

| q | seeds p | S per occasion | S at occasion 40 | seed within 0.01 of 1/2 |
|---|---|---|---|---|
| 0.00 | 0, 1, 0, 1, … | 0, 0, 0, … | 0.000000 | never |
| 0.25 | 0.0955, 0.7369, 0.3764, 0.5625, … | 1.2566, 2.1542, 2.6421, … | 3.141593 | occasion 7 |
| 0.50 | 0.25, 0.5374, 0.4975, 0.5001, … | 2.0944, 2.992, 3.1316, … | 3.141593 | occasion 3 |
| 1.00 | 0.5, 0.5, … | 3.1416, … | 3.141593 | occasion 1 |

The script's computed line: the universe keeps cutting between its pure states only for q = 0, that is, only
when regeneration remembers nothing but the last occasion. With any memory it settles on 1/2 and every later
occasion is pure surplus. P2's surplus weights cannot rescue it: the first two occasions both have S = 0, so
no β can tell them apart, and the seed is 1/2 whatever β does afterwards. The script prints [A6c]: **as
stated, A6 with any memory drives the first universe to the state the cut cannot distinguish from its
antipode; persistence needs either no memory or a content that carries orientation, not position.**

This is the most interesting thing the exploration found, and it should be said carefully. "The many become
one and are increased by one" (Whitehead, named) is exactly A6's Fréchet mean, and on the first distinction
the mean of "this" and "that" is "neither", which is the only state the cut cannot cut. A universe of one
distinction that remembers dies of its memory in a handful of occasions. If CRR wants regeneration to carry
a universe forward, the content it regenerates from must include which way the last occasion was going, not
only where it ended. That is a change to A6, and it is the same change the tense rows asked for from the other
side (file 01: the cut needs orientation; file 07 row 2: the settled past needs its law).

> The universe's first memory is "sometimes this, sometimes that", so it starts the next moment at
> "halfway", and halfway is the one place where "not halfway" is still halfway. So it goes round and round
> and never gets anywhere. To keep going it would have to remember which way it was heading, and CRR's
> memory rule only remembers where it was.

## 5. A second distinction cannot arise

A6's Fréchet mean of points on the manifold lies on the manifold: the mean of 50 weighted points has an
amplitude vector of norm 1 to 0.0e+00 and no component outside the two-outcome span, because there is no
third axis to have one. Nothing in A1–A8 adds a dimension. The script prints [A9]: **a rule that creates a
distinction is absent**; without it the universe stays one-dimensional for ever. Spencer-Brown's "draw a
distinction" (Laws of Form, 1969, named) is the classical statement of what is missing.

If a second distinction is posited, the carrier is the octant of the sphere of radius 2, and the three pure
states are pairwise at distance 3.141593: an equilateral triangle of side π, every pure state at the antipode
of every other. A3's half-turn then needs a chosen great circle, and the script prints [A3b]: **on two or more
distinctions the rotor needs a plane**, which v3.1 does not give.

> CRR can blend old things into new ones, but a blend of "this" and "that" is always somewhere between
> "this" and "that". It can never invent a third thing. And once there are three things, "opposite" stops
> meaning one thing.

## 6. What grew, and what did not

| form | from which line of CRR |
|---|---|
| the line (a geodesic segment of length π) | A1 with the first distinction |
| the circle (normalisation as cos² + sin² = 1) | A1's metric, its Hellinger embedding: a theorem |
| π | A1: the integral of the square root of the Fisher information |
| √2 (the straight chord) | the embedding, not CRR; D3's chord is the arc π |
| the sinusoid (1 − cos t)/2 | posited unit Fisher speed with reflection (A2, a change) |
| the integers (natural time) | A1′, point-process reading |
| negation as the cut (p → 1 − p) | A3 on the derived rotor |
| 1/2 | A6: the mean of the two pure states, and the fixed point of the cut |

Did not appear: a second dimension (A9), a law of motion (A2), the real continuum (A1 presupposes it: a
statistical manifold imports the reals, calculus and the Fisher metric before anything is built), and the
golden ratio of P4 (a Kalman model with q and r, which nothing here supplies).

The honest answer to the owner's question, "can mathematics itself grow from the CRR equations from scratch",
is therefore: no, and the script prints where it stops. Mathematics does not grow from CRR; CRR is written
inside mathematics (a manifold, a metric, the reals), and inside that, from one posited distinction and one
posited motion, the Fisher metric alone produces the line, the circle, π, the sine and the integers, while
CRR's own clauses produce negation as the cut, the state 1/2, and a universe that stops at 1/2 unless it
forgets. The forms that arose are information geometry's; the death is CRR's.

## 7. The nine changes, in the order the script found them

1. [A0] A first distinguishable state and a first motion must be posited.
2. [A2] A law of motion (unit Fisher speed on the geodesic, reflected, was posited here).
3. [A3a] The rotor must be derived (the reflected geodesic; the signed amplitude), not assumed.
4. [A1′a] On a carrier without variability A1′ gives no unit; the unit must be named or variability posited.
5. [A6a] Φ_m, the content regenerated from, is undefined.
6. [A6b] κ, the bounded strength, is in the prose and not in the formula.
7. [A6c] A6 with any memory kills the first universe; the content must carry orientation.
8. [A9] A rule that creates a distinction is absent.
9. [A3b] On two or more distinctions the rotor needs a plane.

Items 3, 5 and 7 are the same decision the v3.2 list already carries from the other batteries (file 05 §2,
items 1 and 7; file 07 row 2's item 8). Items 1, 2, 8 and 9 are new, and they are the ones a "universe from
emptiness" needs and a data study does not: they say CRR as written is a theory of how a given system moves,
not of how systems come to be.

> We tried to grow a whole world from CRR's rules starting with nothing. We had to add the first
> difference ourselves, and the first push. After that the maths made a line, a circle, a wave and the
> counting numbers all by itself. Then CRR's own memory rule stopped the world at "halfway", and nothing in
> CRR could ever make a second kind of thing. So CRR is a story about how things go, not about how things
> begin.
