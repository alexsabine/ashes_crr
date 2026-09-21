# 06 — Why the cut carries content when the axiom says it is empty

A3 says the cut has no duration and no content. Every implementation of it in this repository gave
the cut both, by measured amounts (file 01). This file gives the mathematical reasons, each with the
pinned number behind it, and then says what those reasons suggest about mathematics in general,
about machines, and about number. The five facts about boundaries in finite arithmetic are printed
by `checks/cut_on_a_machine.py` (`checks fact n` below). External works are named as context, not
fetched (R10). Each section ends with a fifth-grader line.

## 1. Six reasons, each a theorem or an arithmetic fact

**R1. On a grid a point is a cell.** A record of n samples gives every sample measure 1/n of the
record, never zero (`checks fact 1`: 1.00e-02 at n = 100, 1.00e-05 at n = 100000). A cut placed at a
sample owns that share, and the instrument must assign the sample to an occasion: that is exactly
the `segment_end` choice (inclusive or exclusive) of `regularity`, which AGENT_LOG 18 had to add
because the default assigned the cut's sample, and the reset jump on it, to the arc.

**R2. A delta has zero support and unit mass.** The emptiness battery graded A3's "no content" as
the zero-measure support of a delta and its "counts once" as the delta's unit integral (emptiness
row 2). On a grid the delta is one cell of height 1/dx and still integrates to 1 (`checks fact 3`:
height 500.0 at n = 1000, integral 1.000000). "No content" and "counts once" are the same object seen
from two sides, and a machine can only hold the second.

**R3. A delta in phase is not a delta in time.** A3 fixes its delta in the phase variable. Integrated
against the clock each cut weighs 1/|u′(t_k)| by the composition rule δ(g(t)) = Σ δ(t − t_k)/|g′(t_k)|
(batch 20 row 5: 0.129949 at the first cut of a chirp, matching to 1.1e-07; 28 masses summing to
1.7732 against 1.7267 for the half-turn durations). The cut has no duration in phase and a duration
in time, and the two are related by the very phase velocity the cut is supposed to be independent of.

**R4. A displacement at the cut is arc.** The arc is the total variation of the path in the metric,
and a reset is a finite displacement with no duration located at the cut. Unless the segmentation
excludes it, it is content: a constant jump added to every occasion halves the CV of the rises
(`checks fact 4`: 0.2012 to 0.1003, closed form 0.4986 of the original), which is how two threshold-
reset rows read arc-regular before AGENT_LOG 18 (E-I cells 4/5 arc-regular with the jump, 0/5
without), how the adder's CV(arc) fell from 0.0749 to 0.0571 with the halving inside (batch 13 row 1),
and how the sawtooth's class flipped (0.5055 against 0.3114, batch 18 row 3). A jump that varies does
not regularise (`checks fact 4`: 0.1404), so the effect is specifically a constant content at the cut.

**R5. The phase is non-local.** The analytic signal at a sample is a sum over the whole record with
the kernel 1/(πt), which has no compact support. Altering the future from sample 1210 of a sine
changes the phase one sample before by 0.1600 half-turns (future removed), 0.2973 (scaled by 3) or
0.3152 (shifted a quarter turn), falling to 0.0058, 0.0005 and 0.0066 a hundred samples before
(`checks fact 5`); at a cycle boundary of the periodic transform the removed future produces no
change, which is the FFT's periodicity and not the world's. So where the "empty" cut sits is fixed by
content elsewhere, including content after it (batch 21 row 2: 0.146 half-turns at the causal
reading). A section computed from the settled samples alone is unchanged in every case.

**R6. A cut is a number.** `antipodal_cuts` interpolates the half-turn crossing between two samples
and returns an index: the cut is a real number rounded to a grid. Dedekind's construction (1872)
says what that number is: a cut of the rationals into a lower and an upper set with no member of its
own. It is empty of rationals and it *is* the irrational (`checks fact 2`: no rational with
denominator up to 1000 squares to 2; the nearest below and above √2 differ by 2.49e-06). On a machine
the cut acquires a width, one unit in the last place (`checks fact 2`: 2.220e-16 at √2), and √2 in
float64 is 1.4142135623730951 exactly, a rational. The cut that was to have no content has, on the
machine, the content of one ulp, and the number it names is one of the rationals it was supposed to
separate.

> Six reasons the line is not nothing when a machine draws it: a dot on graph paper is a square;
> a spike that is "nothing wide" still has to add up to one; a line with no width on the page still
> takes time on the clock; a jump that happens right at the line gets counted as travel; where the
> line goes depends on the pages after it; and a line between numbers is itself a number, which on a
> computer is a tiny box, not a point.

## 2. What this suggests about mathematics

The continuum has a boundary with no content: Dedekind's cut, the measure-zero point, Aristotle's now
that is a limit of time and not a part of it (Physics IV, as context). Every finite computation lacks
that object. Brouwer and Weyl (1918, 1921, as context) argued that the continuum is not a set of
points and that a real number is a never-completed sequence of nested intervals; on that view a cut
always has a width, and the width is the current state of the approximation. The rows are a
demonstration of that position by instrument: the cut's width is the sample (R1), the ulp (R6), the
settling time (R5) or the reset (R4), and it never reaches zero. A3's "no content" is a statement in
classical analysis about an object a computation cannot instantiate. The honest mathematical
reading is that the cut is the *limit* of a sequence of contentful boundaries, and A3 should say
which sequence.

## 3. What this suggests about machines

A Turing machine's head is always on a cell; a step is the primitive act; there is no state between
two cells. The cut on a machine is therefore a step, and a step is one unit of the machine's own
change. That is A1′ read back onto A3: on a machine the cut's content is exactly one resolvable step.
The two instrument findings of this repository say the same from two sides. The unit estimator needs
occasions on both sides of a point to say what one step is (file 01 §2), and the phase needs samples
on both sides of a point to say where the cut is (R5). A machine cannot locate a boundary without
content on both sides of it, because the machine has no boundaries, only cells. This is why the
Poincaré section works where the analytic signal fails: a section is a comparison of two adjacent
cells (one below a level, the next at or above it), the smallest thing a machine can do, and it
consumes exactly one step of future, the cell in which the crossing is declared (batch 21 row 2:
within 1 sample).

> A computer cannot point at a place between two of its boxes. So when it draws a line, the line is a
> box, one step wide. That is why the simple "crossing the middle" rule works: it only looks at two
> boxes next to each other.

## 4. What this suggests about number

Three things, stated as suggestions and not results.

- **The cut is the origin of counting, not its absence.** A delta "counts once" (R2); the section
  declares a crossing and the count n(t) steps by one; Peano's successor is a cut between n and n + 1
  with no content of its own and it is what makes n + 1. The natural numbers are what cuts count.
  A3's "no content" and D5's "one occasion" are the two faces of the successor function.
- **Irrationals are cuts with width on any machine.** R6's ulp is the machine's version of the
  Dedekind gap; a "unit" in A1′'s sense is the smallest gap the system resolves, and for float64 at 1
  that gap is 2.220e-16. A theory whose axiom demands a contentless cut and whose unit is a resolvable
  step is asking for the continuum and the integers at once. Kronecker's remark that the integers are
  given and the rest is human work (as context) is the older form of the same tension.
- **The phase velocity is a Jacobian, and the cut's clock mass is its inverse.** R3 says the cut's
  weight in time is 1/|u′|. A count of cuts is therefore an integral of the phase velocity, and
  "natural time" (the count) and clock time are related by a change of variables whose Jacobian is
  the cut's own content. Natural time is a number theory of the record: an integer count with a real
  Jacobian.

The suggestion for the theory is a rewording that keeps the picture and drops the impossibility:
*the cut has no duration in phase and carries one count*. That is what the delta says, what the
machine does, and what every pinned row measured. Whether "one count" is then A1′'s unit (as the
machine reading implies) is the decision that would unify A1′, A3 and D5, and it is a decision the
owner and Daniel can make; the pipeline can then gate it.

> Counting starts with a line: one, then a line, then two. So the line is not "nothing", it is the
> thing that makes the next number. CRR could say that instead: the line is not long, but it counts
> as one.
