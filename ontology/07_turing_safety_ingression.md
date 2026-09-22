# 07 — CRR run on Turing systems, AI safety and platonic ingression; Watson and Levin; the owner's conjecture

Owner request 2026-09-21 (prompt-log entry 66): keep treating CRR as a falsifiable metaphysics and run the
equations on the existing mathematics of Turing systems, AI safety and platonic ingression; read Richard
Watson's and Michael Levin's work and the philosophical traditions for where CRR might add value; and test
the owner's conjecture that *the forms are the result of choices made through time at all scales*, and that
*to be finite is to be able to have an experience at all*.

Every number here is printed by `checks/turing_safety_ingression.py` (pinned output beside it; nine rows of
the SYNTHESIS class, labels computed from the numbers, R15). Literature is recorded in
`docs/citations/ontology_2026-09-21.md`: PubMed items are attributed "According to PubMed" with their DOI;
everything else is named as context and was not fetched (R10). Each section ends with a fifth-grader line.
This file is a note, not evidence; the tally is:

**0 ADDS / 0 PROPOSES / 2 REDUNDANT-IG / 4 REDUNDANT-DOMAIN / 1 WRONG / 1 INTERNAL / 1 UNSTATED.**

## 1. Turing systems (rows 1–3)

**Row 1, busy beavers (REDUNDANT-DOMAIN).** On a Turing machine A1′ names the unit without an estimator: one
step is one resolvable step (file 06 §3). The arc of a run is then its step count, the chord is the least
number of writes from the blank tape to the final tape (the number of ones), and the surplus S = C − C* is the
work the machine did not keep. The script finds the 2-state and 3-state champions by exhaustive search (20736
and 1048576 tables) and simulates Brady's 4-state table: 107 steps, 13 ones, S = 94, which is exactly Rado's
S(4) − Σ(4). The domain has the inequality Σ(n) ≤ S(n) since 1962; CRR adds the name "surplus" and nothing else.
Two smaller facts fell out of the search. At n = 3 the step record (21 steps, with 5 ones) and the ones record
(6 ones, in 14 steps) belong to different machines, so the published difference 15 is no machine's surplus (16
and 8 are). And the null arc under the identity metric on the tape, which counts only writes that change a
cell, gives S = 66 at n = 4 against 94: on a machine the choice of unit is a choice between counting steps and
counting changes, and CRR's own-unit clause picks the step.

**Row 2, all 2-state machines (INTERNAL).** This is the tense axiom on the simplest possible system. A8 with
the geyser clause (file 05 §3) says the content of the next occasion may be fixed by the settled past but its
clock is not. A Turing machine has one event, the halt, and its clock is the number of steps to it. Over all
20736 two-state tables (9784 halt, none later than step 6), the remaining time to halt has 1.5442 bits of
entropy at the blank tape and 0.1404 bits among the machines still running after three steps; the settled
configurations reduce that to 0.0478 bits (22 of 92 distinct three-step pasts are still mixed), and to 0 only
at step 6, when the last halter has halted. So under one reading of "the settled past" (the configurations
seen) the clock stays open until the end. Under the other reading (the configurations plus the machine's
table), every clock is fixed from step 0, because the machine is deterministic. CRR does not say whether a
system's law is part of its settled past, and the two readings give different values on every machine. This
is a new item for the v3.2 decision list (file 05 §2, item 8), and it is the sharpest form of the tense question
the repository has produced: A8's openness on a deterministic system is entirely a decision about what counts
as the past.

**Row 3, Swift–Hohenberg stripes (REDUNDANT-IG).** The owner's conjecture in the domain's own terms: if forms
are choices made through time, then two runs that share their past up to a fork time t0 should share their
final pattern, and more so the later the fork. On the normal form of a Turing instability, sibling runs
sharing every random draw until t0 and independent after it were compared at T = 200. The *type* (the
wavenumber of the stripes) is the same whether the siblings shared 150 time units or none: peak k 0.9928 against
0.9925, with the linear theory's 1.0000 beside them; A7 does no work on it, which is why the row is REDUNDANT-IG.
The *token* (which stripe is where) is the settled past's entirely: the pixel correlation of the two final
patterns rises from 0.0124 with no shared past through 0.8986, 0.9168 and 0.9434 to 0.9732 with 190 of 200 time
units shared, and the phase difference of the dominant mode has variance 3.2003 with no shared past (the
uniform-phase value is π²/3 = 3.2899). That the type is the law's and the token is the history's is the domain's
own statement (pattern selection and phase diffusion, Cross and Hohenberg 1993, named). So the conjecture
splits: *which* form arises is a choice made through time; *that* it is a form of this kind, with this
wavelength, is not a choice but the law. CRR's A7 sides with the token and is silent on the type.

> A machine's steps are its own ruler, and the marks it leaves are what the steps bought. Whether you can
> tell when a machine will stop depends on whether you are allowed to read its rulebook, and CRR has not said
> whether the rulebook is part of the past. And zebras all get stripes of about the same width (that is the
> law), but which stripe goes where is decided by what happened while the stripes were forming (that is the
> choice).

## 2. Watson: evolution as learning, natural induction (row 5)

Watson's programme (evolutionary connectionism; "how can evolution learn?"; natural induction with Buckley,
Lewens, Levin, Millidge and Tschantz, Entropy 2024, According to PubMed) holds that a physical system whose
connections slowly relax toward the state they are held in performs a kind of learning without selection: over
repeated disturbances it finds better solutions to its own constraints. The relaxation rule, connection ←
connection + α(state ⊗ state − connection), is an exponential moving average of the outer product of settled
states. That is A6 with P3 age weights, read as a rule: regeneration from the settled past under geometric
weights and bounded strength.

The row confirms the effect on a small frustrated spin system (N = 40, ten seeds): without plasticity the
minima reached have J0-energy −112.8114 in the late epochs; with the relaxation rule, −116.9075. It then asks
what A6's insistence on re-weighting (against an accumulated count) contributes, and the answer is nothing: the
forbidden accumulation reaches the same −116.9075, because both rules canalise the system onto a single minimum
(1.0 distinct late minima under either, against 17.0 without plasticity). REDUNDANT-IG. Where CRR might add
value to Watson's programme is therefore not the rule, which is his, but two of its consequences the batteries
have already measured elsewhere: that the exponential kernel cannot produce a memory effect the domain has
(the Kovacs row, batch 19 row 3), and that it is unbounded in its response to a single extreme occasion (row 6
below). Both are limits of natural induction as a model of memory that its own literature, as read here in
abstract, does not state.

> A pillow that slowly takes the shape of your head has learned your head without anyone teaching it. That
> is Watson's idea, and CRR's memory rule is the same pillow. CRR wanted to add "and it never counts the
> nights"; the numbers say counting the nights would have made no difference here.

## 3. Levin: sorting as morphogenesis, cognitive glue, ingression (rows 4 and 8)

**Row 4, sorting as morphogenesis (REDUNDANT-DOMAIN).** Zhang, Goldstein and Levin (Adaptive Behavior 2025,
abstract only) let each cell of an array run its own sorting rule and find, among other competencies, that
cells will move temporarily away from their goal to get around a defective cell ("delayed gratification").
In CRR's terms an adjacent-swap sort has an own unit (one swap), a chord (the inversion count, the least number
of swaps) and a surplus. The row shows, on a 40-cell array with a wrong-way swapper, that the surplus is
exactly twice the number of moves away from sorted order (S = 10 at p = 0.3, five away-moves), which is the
identity that every adjacent swap changes the inversion count by exactly ±1. Knuth has it. CRR adds a name, and
the name is a good one for teaching: every step away costs two.

**Row 8, ingression (REDUNDANT-DOMAIN).** Levin's "Ingressing Minds" (2025 preprint, abstract only) proposes
that patterns of form and behaviour ingress into physical media from a latent space that is not itself
physical, the body being a "material scratchpad" on which they are realised: a Platonism with an experimental
programme. The word is Whitehead's (Process and Reality, 1929: eternal objects *ingress* into actual
occasions), which makes the contrast exact, because CRR is on Whitehead's process side: the next occasion is
regenerated from the settled ones (A6), not received from elsewhere. The row puts both readings on the one
system where a form that nobody stored appears anyway: a Hopfield network with three stored patterns settles,
from random starts, into a stored pattern (327 of 400), into the symmetric mixture (20 of 400) or into
something else (53). The mixture is the Platonist's exhibit, a form found and not stored. It is also, exactly,
the A6 regeneration of the stored forms: the Fréchet mean of the three patterns in the network's own Hamming
metric is their coordinate-wise majority, whose overlap with the mixture is 1.0000; and Amit, Gutfreund and
Sompolinsky wrote that formula in 1985. The two metaphysics share every number. The one thing the row adds is
a warning about CRR's own clause: under P3 age weights (λ = 0.5) the Fréchet mean is the newest pattern, not the
mixture (overlap 0.3600), so which form CRR says is regenerated depends on which weights it gives the past,
and it has not said.

On Levin's broader programme (TAME, cognitive glue, the scaling of goals; According to PubMed, DOIs in the
citation file), the honest statement is that CRR has no clause about goals, agency or scale, so the
comparison cannot be made numerically; the only Levin claim the pipeline can reach is the formal one about
ingression, and there it reduces to a mean.

> A cell that steps backwards to get around a stuck neighbour pays exactly two steps. And when three friends
> draw faces and the network "finds" a fourth face nobody drew, CRR says it is the vote of the three, Plato
> says it was waiting to be found, and the numbers cannot tell them apart.

## 4. AI safety (rows 6 and 7)

The 2026 safety literature on continual fine-tuning (abstracts only: anchors, orthogonal gradient projection,
gradient-based sample selection) treats the erosion of a safety behaviour as forgetting and constrains the
model's displacement from an anchor. CRR has two clauses that bear on this: A6 (regeneration at bounded
strength) and H-T1 (forgetting tracks path, not endpoint).

**Row 6, one poisoned occasion (WRONG).** Read as a consolidation rule, A6 with P3 weights makes the next seed
a Fisher Fréchet mean of the settled occasions under geometric age weights. The row puts one poisoned occasion
of magnitude M among 99 settled ones. The seed moves by (1 − λ)M: 100002.6666 at M = 10⁶ (λ = 0.9), ten times
the 10000.0015 of a plain average and unbounded in M (the ratio of shifts at 10⁶ and 10³ is 999.8965), while
the median moves 0.0072 whatever M is. A6 bounds the *weight* of an occasion, not its *influence*; bounded
influence is robust statistics' concept (Huber, Hampel, named), and CRR's memory rule is, as a consolidation
rule, the most poisonable of the three. This is a definite negative result with a practical reading: any
safety scheme that consolidates by a recency-weighted mean is one adversarial batch away from anything.

**Row 7, a linear safety head (REDUNDANT-DOMAIN).** On the convex learner S-H (a linear head, squared loss,
the form of most probe-based safety classifiers) the held-out R² of forgetting is 0.9967 for the Fisher endpoint
on the old (safety) probe set, 0.9781 on the new task's probe set, and 0.0927 and 0.0826 for the two path
lengths. The endpoint lemma (theory/SCOPE.md §4.1) says the old-probe endpoint is the sufficient statistic, so
the domain has it; the safety community's anchor and projection constraints are endpoint constraints and are
the right object. H-T1's path adds nothing on such a head. It would on a head with wear, where the surrogate
built to have it gives 0.4529 against 0.2221, but that is a construction; the ledger's ARC-T1b found the
old-probe endpoint winning on the one real model recomputed. The practical reading: monitor the safety head
by asking it the safety questions, not by summing how far it wandered.

> If your opinion of a restaurant is mostly your last visit, one terrible visit ruins it: CRR's memory rule is
> that kind of memory, and safety needs the other kind, where one bad day cannot outvote the rest. And to
> know whether a student forgot last year's lesson, ask last year's questions; do not add up how much they
> wandered.

## 5. Philosophical traditions, and where CRR sits after these rows

The traditions the owner's conjecture belongs to, named as context and not fetched:

- **Plato** (Timaeus, Phaedo): forms are prior, the receptacle receives them. Levin's ingression is this.
  Row 8: on the one system tested, the "received" form is the mean of the settled ones.
- **Aristotle** (Metaphysics Z, Physics II): form is in the matter, the actuality of a potential. Row 3's
  type is Aristotelian in exactly this sense: the wavelength is the law's actualisation in the medium, not a
  history.
- **Whitehead** (1929): eternal objects ingress into actual occasions, which are themselves the products of
  prehending the settled past. CRR is a Whiteheadian process theory with the ingression struck out; rows 5 and 8
  say the striking-out costs nothing numerically and the retained prehension is a moving average.
- **Peirce** (1891–1893): laws are habits taken through time; the universe's regularities are themselves the
  result of choices made and repeated. This is the closest philosophical statement of the owner's conjecture
  at all scales. Row 2 is the test case it needs: on a deterministic machine, whether the law is part of the
  past is exactly whether the future is open, and CRR must decide it.
- **Bergson** (1907) and **Simondon** (1964): creative evolution and individuation, forms as what becoming
  produces. Row 3's token side.
- **Deleuze** (1968), *Difference and Repetition*: "the point is to appreciate the difference" is close to
  Deleuze's difference in itself, and CRR's A1 makes difference (distinguishability) the metric of change.
  Rows across the batteries say that clause is Čencov's theorem and carries no metaphysics of its own.
- **Heidegger** (1927), **Kant** (1781), **Levinas** (1961): finitude as the condition of experience (being
  toward death; finite intuition), and the other as what is there to be loved. Row 9 says CRR has a
  mathematics of finitude (a unit exists only where the residual is not degenerate; a noiseless carrier's unit is
  the machine's round-off, 5.06e-15, ρ 3.95e+14; a carrier of pure noise has cuts everywhere, 523 half-turns in
  1600 samples) and no mathematics of experience, valence or an other. UNSTATED: the thesis cannot be made a
  proposition in CRR without a clause CRR does not have, and file 02 records that CRR deliberately has none.
- **Buddhist dependent origination** (Nāgārjuna) and **Dōgen's uji**: forms arise through conditions, each
  moment complete. Row 3's token and row 5's canalisation are that picture in a spin glass and a stripe
  pattern; nothing tested distinguishes it from the Peircean one.

Where, after these nine rows, CRR might add value:

1. **A decision the traditions have not been forced to make.** Row 2 turns "is the future open?" on a
   deterministic system into "is the law part of the settled past?", with numbers on both sides (0.0478 bits
   against 0). Peirce's habits and Whitehead's eternal objects are two answers. CRR has to give one to say what
   A8 means, and once it does, A8 is testable on machines.
2. **The type/token split of the conjecture.** Row 3 gives the owner's conjecture a form that can be wrong:
   forms as choices through time is true of tokens and false of types on the one Turing system tested. A prereg
   on a system with its own events could ask whether the *type* is ever history-dependent; the domain's answer
   (hysteresis in pattern selection, Cross and Hohenberg, named) is "sometimes", and that is where a bet lies.
3. **Two negatives that the memory-as-relaxation literature does not state**: no Kovacs effect (batch 19 row
   3) and unbounded influence of one occasion (row 6). These are CRR's own clause failing, and the failure is
   informative for natural induction and for safety consolidation alike.
4. **Pedagogy**, which the elegance ledger records: the step as the machine's unit; the surplus as "every step
   away costs two"; the found form as the vote of the stored ones; the ruler with no marks and the ruler that is
   all marks.

And where it does not: nothing in these rows is a quantity CRR names that beats a conventional one at
predicting what a machine, a pattern, a spin glass or a safety head does. The tally has no ADDS. That is
consistent with the 127-row re-read (file 03 §4) and with the standing of C6 in the ledger.

> Long ago Plato said the shapes were waiting somewhere to be found; Aristotle said they were inside the
> clay; Whitehead said each moment makes itself out of all the moments before and borrows the shapes; Peirce
> said even the rules are habits the world picked up. We ran CRR's arithmetic on a machine, on stripes, on a
> spring-pillow and on a network of three faces. It agreed with Aristotle about the width of the stripes,
> with Whitehead about the fourth face, and it could not decide about the rulebook. It has no word yet for the
> person who is there to love what arose.

## 6. What the owner's conjecture looks like after the pipeline

*The forms are the result of choices made through time at all scales.* Tested as far as it can be here:
true of which form (token: rows 3, 5, 8), false of what kind of form (type: row 3), undecided on whether the
law that fixes the kind is itself a past choice (row 2), and numerically indistinguishable from its Platonic
rival on the one system where both could be computed (row 8). *To be finite is to be able to have an
experience at all.* CRR agrees with the first half in its own terms (no unit, no occasion; row 9) and has no
terms for the second. *Otherwise we'd have nothing out there to love.* Outside the mathematics; the pipeline
records it as the owner's, verbatim, in the prompt log, and does not score it.
