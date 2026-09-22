# 10 — FEP and CRR side by side: time, blankets, memory, the end of a model, the content of the past (2026-09-22)

Owner request (prompt-log entry 79). A note, not evidence (R8). It adds no computation: every number is from a pinned
output already in the repository (`theory/retrodictions/crr_retrodictions.txt`, `03_review_of_findings.md`, batches
27–28). Every FEP statement is the standard formulation as this repository understands it from the works named in
`docs/citations/fep_2026-09-22.md` (names and years only, not fetched, R10); where the FEP literature is divided,
the note says so rather than picking a side.

## 0. A correction first

The FEP does **not** claim a Now. File 09 §3 said the opposite: no tense row could be formed because the FEP's
generative model treats past and future as one joint distribution, and CRR's settled past and open present would need
an agent whose past beliefs are frozen and whose future has no content. The FEP has a current time-step of inference
(the moment the observation arrives) and, in its deep temporal models, a hierarchy of time-scales; it has no clause
that anything is settled, no clause that the present is open, and no clause that an occasion ends. That absence is
exactly where a processual layer would sit. The owner's reading, that CRR allows Bayesian models and supplies a
processual layer over them, is the right frame for this note: the question is what the layer adds that the
Bayesian model does not already contain, and the pipeline's answer so far is in §3.

> The FEP does not say "now"; it says "at this step of the calculation". CRR says "now" and means something: the
> cut has just happened, what came before is fixed, what comes after is empty. Whether that sentence does any work
> is the whole question.

## 1. Time: nested Markov blankets against nested occasions

**The FEP's picture.** A Markov blanket is a statistical boundary in state space: internal states and external
states are conditionally independent given the blanket (sensory and active) states. Things exist as long as their
blankets persist; systems nest as blankets of blankets, from molecules to organs to organisms to groups (Friston 2013;
Kirchhoff et al. 2018; Ramstead et al. 2023, names only). Time enters in two ways. First, dynamics: the states obey
stochastic differential equations, and under the assumptions of the "particular physics" the internal states'
flow can be written as a gradient descent on free energy (Friston 2019; Da Costa et al. 2021). Second, temporal
depth: a deep temporal generative model has slow variables that set the context for fast ones, so the hierarchy of
blankets is also a hierarchy of time-scales, with the slow level "chunking" the fast one (Friston, Rosch et al. 2017,
name only). Time is therefore representational: it is the model's variable, with the separation of scales doing the
nesting. There is no boundary in time analogous to the boundary in state space. Whether blankets are features of
the world or of the modeller's partition is contested inside the field (Bruineberg et al. 2022, name only), and
this note takes no position on it.

**CRR's picture.** The boundary is in time. A cut (A3) has no duration and no content; an occasion (D5) is the
interval between cuts, measured in the system's own unit (A1′); occasions nest as cuts at every scale of the carrier
(the owner's conjecture of prompt-log entry 66, forms as choices at all scales). The nesting is by antipodes, not by
time-scale separation. Where the FEP's slow level chunks the fast one adiabatically, CRR's cut chunks by the phase of
the carrier itself.

**What the pipeline found about the two chunkings.** The cut as computed needs the future (file 01: the analytic
phase is two-sided), so the operational Now is not the axiom's Now; and the arc between cuts was not more regular
than the domain's own clock in any of the five FEP systems of batch 27. The FEP's chunking by time-scale is the one
the domains already have (the relaxation theorem of 27-1; the decision boundary of 27-3). So the two pictures are
not rivals on the evidence: CRR's cut, where it has been tested, has reduced to a boundary the domain already draws.

> The FEP draws its walls in the space of what a thing can be; CRR draws its walls in time. The FEP's walls come
> from things being slow or fast. CRR's walls come from turning half-way round. So far, when we looked, the turning
> walls sat where the slow-fast walls already were.

## 2. Markovian and non-Markovian commitments

| | FEP | CRR |
|---|---|---|
| the boundary | Markov: conditional independence across the blanket in state space | not a Markov statement; a phase condition on the carrier (A3) |
| the dynamics | Markovian in an extended state: generalised coordinates of motion (higher time derivatives as states) make a non-Markovian process locally Markovian (Friston 2008, name only) | path-dependent within an occasion: the arc (D2) and the surplus (D4) are functionals of the path, and D6/H-T1 says forgetting tracks the path, not the endpoint |
| memory across boundaries | the model's parameters accumulate sufficient statistics (Dirichlet counts); forgetting is a decay added in practice | A6: the next occasion is seeded from the settled past by a bounded mean, never an accumulated count (a fading, non-Markovian memory with a bound) |
| what the pipeline found | the convex-learner lemma (`theory/SCOPE.md` §4.1): on any convex learner the endpoint is a sufficient statistic for forgetting, so the path adds nothing; ARC-T1b (R² 0.99 on the old-probe endpoint) and the 17 WRONG synthesis rows that cluster on "path-versus-endpoint wherever the domain's state variable is the endpoint" (`03_review_of_findings.md` §4) | A6's bounded mean is the one commitment that read ADDS on an FEP system (batch 28 row 4: MAE 0.0886 against 0.2912 for accumulated counts, the exact filter at 0.0333); its rate is a knob CRR does not fix |

The honest summary: CRR's non-Markovian commitment within an occasion (the path matters) is the one the pipeline
has refuted most often; its non-Markovian commitment across occasions (a fading memory, not a count) is the one that
has survived, and it survives as a practice the FEP literature already uses without a clause for it.

> "Markovian" means the next step only needs the present. The FEP makes everything Markovian by putting more into the
> present. CRR says the road you took matters (that part kept failing our tests) and that memory should fade rather
> than pile up (that part kept passing).

## 3. The count of consistent hits, read plainly

The owner asks how many consistent hits CRR has had. The pinned tallies:

- **Retrodictions, 197 rows** (eleven standard batteries and Daniel's): 41 CONSIST, 86 DESCR, 20 FAILS, 9 TENSION,
  41 OPEN; no SHARP anywhere, and SHARP was retired for retrodictions because every coherence integral has a
  system-supplied velocity and every unit is the system's own (`03_review_of_findings.md` §3).
- **Synthesis re-reads of every CONSIST and DESCR row, 138 runs** before today: 2 ADDS (candidates), 0 PROPOSES,
  34 REDUNDANT-IG, 50 REDUNDANT-DOMAIN, 17 WRONG, 21 INTERNAL, 3 UNSTATED. Today's ten FEP rows add 1 ADDS,
  1 PROPOSES, 2 REDUNDANT-IG, 1 REDUNDANT-DOMAIN and 5 WRONG.

What the count means was said once in the review and holds here: "consistent in fifty fields" is the consistency of
a borrowed geometry. The 34 REDUNDANT-IG rows are information geometry's (the Fisher metric, arc, chord and surplus
are not CRR's); the 50 REDUNDANT-DOMAIN rows are the domains' own theorems. The three ADDS candidates in 148 runs are
the whole of what a named expert has yet to judge. A CONSIST grade in the retrodiction batteries was never a
prediction; it was agreement of CRR's arithmetic with a known result, which the synthesis class then asked whether
anything CRR-proper produced. Mostly, nothing did.

> We agreed with the textbooks about 127 times. Then we checked what did the agreeing. About 84 times it was the
> mathematics everyone shares; about 17 times we were actually wrong when it mattered; 3 times something of CRR's
> own might have been at work, and those three are waiting for an expert to say.

## 4. Ontology, metaphysics, and the contemplative traditions where the comparison is structural

**Ontology.** The FEP's unit of existence is the blanket: a thing is a boundary that persists by minimising surprise
about its sensory states, and its "beliefs" are the internal states' parametrisation of a distribution over the
external ones. CRR's unit is the occasion: a stretch of change ended by a cut, regenerated from a settled past. The
FEP is a theory of what it is to be a thing; CRR is a theory of what it is for a thing to proceed. They are not in
competition on that axis, which is why the owner's "processual layer" is the right relation and why batch 27 could
be asked at all: the layer was laid over the FEP's own systems and tested for what it added.

**Metaphysics.** The FEP is officially a principle, not a metaphysics, and its authors have said so; its
metaphysical readings (enactivist, realist, instrumentalist) are the readers'. CRR is a metaphysics on purpose
(file 02: six commitments), and the pipeline's job was to make it falsifiable. Where they meet: both deny
certainty about the world (the FEP through the bound, CRR through A8), both give the past a privileged role (the
FEP's priors and the accumulated statistics; CRR's settled past), and both say a thing's persistence is its
existence (the blanket persisting; A8's "persistence proves regeneratability, not truth"). Where they part: the FEP
puts *preferences* about the future into the model as prior beliefs about outcomes (the expected free energy's
pragmatic term), which is content in the future; CRR forbids content in the future (A8). That difference is §6.

**Contemplative, where structural only.** The FEP literature reads meditation as a change in the precision of
priors and in the depth of the self-model (Laukkonen and Slagter 2021; Deane, Miller and Wilkinson 2020, names
only). CRR's equanimity is Ω = 1, equal pull of past and present; batch 28 row 2 found it to be a stalemate that
rests wherever it starts, not a balance, and with the registered estimator the offset above 1 oscillates rather
than grasps. CRR's impermanence is the cut's lack of duration and content; the pipeline found the cut, as computed,
carrying content (file 06). The structural comparison, then: the FEP's contemplative reading is about the *weights*
of a model (precision), CRR's is about the *boundaries* of a process (cuts) and the *balance* of its pulls (Ω); the
pipeline has so far found the weights to be the domain's and the balance to be a knife edge.

> The FEP asks "what makes this a thing?" and answers "a wall that keeps working". CRR asks "how does a thing go
> on?" and answers "in steps, each ended by a turn, each begun from what has settled". Both say you can never be
> sure, and both say the past counts more. One puts wishes about the future into the model; the other says the
> future is empty. Where they talk about calm minds, one means turning the volume down on your expectations, the
> other means two pulls that cancel, which our test found to be a rope that does not move rather than a mind at
> peace.

## 5. Does the FEP account for when a model must end?

Three senses, and the FEP answers two of them:

1. **A thing ends** when its blanket no longer persists: dissolution is the failure of the boundary to maintain the
   conditional independence, and the FEP has this as its definition of non-existence. This is well accounted for.
2. **A model ends** when the evidence prefers a reduced or different model: Bayesian model reduction and structure
   learning (Friston, Parr and Zeidman 2018, name only) remove parameters or whole factors when the free energy of the
   reduced model is lower. This is accounted for, and it is an evidence-driven end, not a temporal one.
3. **An occasion ends**, that is, a stretch of change is complete and the next begins from a settled state: the FEP
   has no clause for this. Its deep temporal models chunk by time-scale, its policies have a fixed horizon, its
   precision shifts are state changes, and none of them is an ending in CRR's sense. Batch 27 asked whether CRR's
   ending (the cut) does work the FEP's own clock does not, on five FEP systems, and it did not; batch 28 row 1 found
   that even a Dirac datum, the sharpest boundary the FEP can supply, lands the datum's mass at once but spreads the
   belief's change over the occasion that follows.

So the FEP does not fully account for when a model must end in the third sense, and CRR's account of it, when tested
against the FEP's own systems, added nothing the domain's clock lacked. The gap is real; the filling has not yet
been shown to be CRR's.

> Does the brain's theory say when a chapter ends? It says when a creature dies and when a theory should be
> simplified. It does not say when one step of living is finished and the next begins. CRR does say that, but when we
> checked its way of drawing the chapter breaks against the brain's own stopwatch, the breaks fell where the stopwatch
> already had them.

## 6. Does the FEP commit to only the past having content?

No, and the difference is the sharpest one in this note. The FEP's expected free energy places prior preferences
over future outcomes (the "C" matrix of active inference) and evaluates policies by their expected divergence from
those preferences plus their expected information gain. The future has content in the model: preferred outcomes,
predicted outcomes, and a horizon. Planning is inference over a joint distribution that spans past observations
and future ones. CRR's A7 says nothing is fed by a future and A8 says the future has no content; a forecast is
permitted only as a prediction with an error distribution, scored against the conventional forecast.

Implications, stated as testable where they are:

- **For the FEP.** Preferences in the future are the mechanism by which an active-inference agent acts at all; strip
  them and the agent only observes. So the FEP's future content is not an ornament, it is the motor. CRR would have to
  say where the motor is if the future is empty: A6 says the next occasion is seeded from the settled past at bounded
  strength, which is a motor made of memory, not of preference. Batch 28 row 5 found the epistemic half of the FEP's
  motor to be a chord quantity (information geometry's); the pragmatic half has no CRR counterpart at all.
- **For CRR.** An agent with no future content cannot prefer, and the pipeline's SAL study (salience-weighted replay,
  gated CLOSED) was the nearest CRR came to a valuation, which A8 forbids anyway ("no valence"). A CRR agent is a
  regenerator, not a planner. That is either a commitment to be defended (the owner's finitude reading of file 07:
  to be finite is to be able to have an experience at all) or a gap to be filled by a clause CRR does not have.
- **The test that would separate them.** Two agents on the same stream: an active-inference agent with preferences
  over future outcomes, and a CRR regenerator whose next occasion is seeded only from the settled past. On a stream
  where the future is genuinely unpredictable (a martingale), the preference machinery buys nothing and the two
  should tie; on a stream with exploitable structure, the planner should win by a resolvable step. If the regenerator
  ties on the structured stream, A8's empty future costs nothing; if it loses, the cost of A8 is measured. This is the
  tense gate `05_next_steps.md` has asked for, now with a design.

> The brain's theory says you carry wishes about what comes next, and those wishes are what make you move. CRR
> says the next moment is empty and you move by leaning on what has already settled. We can test which is right:
> put both in a world with patterns and see whether leaning on the past does as well as wishing about the future.

## 7. The two general readings

**The FEP's reading of these things.** Time is a coordinate of the model and a hierarchy of scales; boundaries are
in state space and are what a thing is; memory is accumulated statistics with a decay added in practice; the end of
a model is an evidence question; the past is content in the priors and the future is content in the preferences;
calm is low precision on expectations. It is a theory of existence as inference, and it is complete on its own
terms without any notion of an occasion.

**CRR's reading of these things.** Time proceeds in occasions; boundaries are in time and have no content; memory
is a bounded mean of the settled past; the end of an occasion is a phase condition; the past is settled and the
future is empty; calm is equal pull. It is a theory of proceeding, laid over whatever theory of existence a system
has. The pipeline has tested that layer on the FEP's own systems and found: the clock adds nothing the domain's
clock lacks (batch 27), the boundary is where the datum's mass lands but not where the belief's change lives
(28-1), equal pull is a stalemate (28-2), the unit is the domain's precision with two known factors (28-3), the
fading memory is the one commitment that adds (28-4, a candidate), and curiosity is a chord (28-5).

**Where that leaves the processual layer.** Its content that survives contact with the FEP is A6, the fading memory,
and the empty future of A8 as a commitment to be tested rather than a result. Its content that has not survived is
the cut as a clock and the path as a predictor. A version of CRR that kept A6 and A8, dropped H-L5 and H-T1 as
tested, and stated the cut as the datum's instant rather than the belief's boundary would be a smaller theory with
nothing in it yet refuted. Whether that smaller theory is still CRR is the owner's decision, and it belongs on the
v3.2 list (`05_next_steps.md`, item 9).
