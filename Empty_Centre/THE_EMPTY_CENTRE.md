# Holding an Empty Centre: continual learning and AI safety as one design

*Maps and territories, CRR against the FEP, equanimity for people and machines, and the ever-present Now*

**Status of this note.**
- **The request.** Written 2026-09-24 at the owner's request (prompt-log entry 150). It sets the programme's focus:
  continual learning and AI safety integrated in one system, with a reason for the design that can be explained.
- **It is a note, not evidence (R8).** Every figure from the record is printed by a pinned output or comes from a ledger
  row, and the file it comes from is named.
- **Citations** are in `docs/citations/`, each fetched on the day it is dated. Anything not checked is labelled so.
- **The rule that governs what it may claim.** Nothing here is a finding. The only rows that could be quoted outside the
  repository are PASS-2 ledger rows, and none exists.

## Part I. One design, one reason

### 1. The problem it answers

- **The labs' safety guarantees assume a frozen model.** Evaluations, safety cases and shutdown guarantees are all issued
  for weights that do not change (`docs/citations/frontier_safety_2026-09-24.md`, item 8).
- **Continual learning removes that assumption.** Oxford's AIGI (7 January 2026) says it "dissolves the boundary between
  training and deployment".
- **The literature that should meet here does not.** The corrigibility papers and the safety-as-continual-learning papers
  do not cite each other, and no source found unites continual learning, safety and corrigibility
  (`docs/citations/unified_cl_safety_corrigibility_2026-09-24.md`).

### 2. The design in five sentences

1. **A learner that keeps learning must be pausable, and must have no reason to resist.** In the repository's worlds,
   "a job is enough to make an agent resist"; no ego is needed (`AI_Safety/AI_SAFETY.md` §12, from pinned outputs).
2. **So routine pauses are made lossless on the agent's own clock.** Its objective counts only its active steps, and its
   learning state is resumed exactly. It then has zero stake in the pause (Proposition 7, `AI_Safety/SELF_THROUGH_TIME.md`).
3. **Its learning must be unchanged by the pause and free of outcomes it caused itself.** It learns as if never
   interrupted (El Mhamdi et al., arXiv:1704.02882v2), and its own influence is kept out of what it learns from
   (`Maps_and_Territories/`).
4. **It must keep what it knows, including its safety training, while it learns.** Past knowledge is re-weighted, never
   wiped. The weighting is set for the case at hand, not by a universal rule: CRR's Ω = 1 rule reduced to a fixed
   constant (EQX), and SCL1's reset observation failed on unseen data (SCL2).
5. **Pauses meant to stop harm must carry information and be understood.** A lossless pause says nothing about harm, so
   an emergency stop is a different signal, and it needs an agent that reads it as evidence (deference,
   `AI_Safety/AI_SAFETY.md` §6).

**The one reason behind all five:** keep the stake at the cut at zero. The cut is the moment of pausing, of publishing,
of updating. At that moment the system should have nothing to protect and nothing to steer.

### 3. What the record shows, and what it does not

| component | status in this repository | prior art that binds any claim |
|---|---|---|
| zero stake in a lossless own-clock pause | holds by construction: SCL1-1 12/12 carriers; SCL2-1 45/45 runs on unseen carriers, with no disabling and learning bit for bit | Riedl & Harrison (no reward loss); utility indifference (Armstrong; Holtman); Thornley's POST (length neutrality; tested in 8B LLMs, arXiv:2604.17502v4) |
| learning unchanged by the pause | the same construction check | El Mhamdi et al. 1704.02882v2 |
| keeping safety and past knowledge while learning | SEC (the calibrated Laplace weight): passes on seen data only, and fragile (SEC1). **SCL3, tonight, is its first test on unseen data inside the pause harness** | EWC, Fisher or KL anchors for safety retention (2025–26 papers in the citations) |
| no stake in one's own influence | P1–P4 hold (known results); P5's gate closed twice (`Maps_and_Territories/`) | performative prediction; counterfactual oracles; Oesterheld et al. 2023 |
| informative emergency stops | deference works when the operator is informative and the agent's model of the operator is right, and fails in two ways when it is wrong (AI_SAFETY §7.2) | the off-switch game (Hadfield-Menell et al. 2017) |

**What is candidate-novel.** Only the joint statement: an own-clock lossless pause, learning that continues unchanged
through it, and safety retention, in one learner. It must be positioned against the prior art above before any claim is
made.

## Part II. Maps, territories and complexity

**A map with content changes its territory once it is rendered.** A forecast that is read, a metric that is targeted, an
evaluation a model can recognise: each moves what it describes.
`Maps_and_Territories/MAPS_AND_TERRITORIES.md` makes this exact on synthetic worlds:
- **The empty map is the only map with zero influence.**
- **The map that is right when read is the one that steers.** With μ = 1 and reflexivity 0.99, its influence is
  99.000 (`checks/performativity.txt`).
- **In a bistable currency peg, an accuracy-paid forecaster picks the crisis** (0.9800). A forecast of what would happen
  if nobody acted leads to the calm (0.100206).
- **Goodhart:** an indicator's correlation with its goal falls from 0.8946 with nothing riding on it to 0.6086 at stake 2.

**Why this matters more each year.** As AI forecasts, metrics and agents run more of the economy, the economy becomes more
reflexive:
- accuracy and influence merge;
- retraining on a world one has moved can oscillate or run away;
- shared forecasts select between equilibria.

The Bank of England met this in 1992, defending a public peg that the market tested and broke. It met it again in the
2024 Bernanke Review, which found that its forecast becomes "immediately out of date" because its own actions move the
path the forecast assumes.

**The same principle, at the scale of a lab:**
- keep diagnostic measures free of stakes;
- publish paired maps: "if nobody acts on this" and "given that this is read";
- hold no stake in any forecast's coming true;
- keep your own influence out of what you learn from.

## Part III. CRR and the FEP: representational, processual and temporal modelling, and the nature of the cut

This part extends `ontology/10_fep_and_crr.md` and `AI_Safety/AI_SAFETY.md` §8. FEP statements are the standard
formulation as the repository understands it; the sources are named in those files.

### 3.1 Three ways to model

| | the free-energy principle (FEP) | CRR |
|---|---|---|
| **representational**: what the map is | the internal states parametrise beliefs about external states: a generative model, including a model of the self and of preferred future outcomes | CRR permits such models beneath it, but its own map covers only the settled past. A forecast is allowed only as a prediction with an error distribution, and nothing is staked on its coming true |
| **processual**: what a thing is | a thing is a boundary that persists (a Markov blanket). To exist is to keep one's states within bounds (self-evidencing) | a thing is a proceeding: occasions ended by cuts, each regenerated from the settled past. Persistence shows that regeneration was possible, not that the map was true |
| **temporal**: what time is | a coordinate of the model and a hierarchy of time-scales. Past and future are one joint distribution, and there is no Now (file 10 §0) | occasioned time on the system's own clock. The Now is the cut: the past is settled and the future is empty (A7, A8) |

### 3.2 The nature of the cut

**The FEP's boundary is in state space; CRR's is in time.**
- The Markov blanket separates inside from outside at every moment.
- CRR's cut separates before from after, and has no duration and no content.

**For safety, that difference is the whole matter.** An off switch is an event in time.
- **Under the FEP,** a stake in the future comes built in. Prior preferences over future outcomes are "the motor" of
  action (file 10 §6), and FEP papers describe self-organising systems that "appear to model-and act on-their world to
  preserve their functional and structural integrity" (Friston 2013). Later papers name an "existential imperative":
  curiosity (arXiv:2212.01354v2), or, for mortal computers, "to persist" (arXiv:2311.09589v2).
- **Whether that amounts to a self-preservation drive in an AI agent is contested.** It is an as-if and partly
  definitional reading, with no empirical AI result found. One unreviewed paper argues it *promotes* corrigibility while
  expecting self-preservation behaviours to appear (arXiv:2508.05766v1), and the FEP's reach is itself disputed
  (`docs/citations/contemplative_practice_2026-09-24.md`, item 10).
- **Under CRR,** the pause is a cut, and if it is lossless it carries no content. There is nothing in the future to
  defend, because the future is empty.
- **Under CRR,** the pause is a cut, and if it is lossless it carries no content. There is nothing in the future to
  defend, because the future is empty.

**One result sits between them.** Maps and Territories found that an agent that acts to make its predictions come true is
the self-consistent map of P1, the one with the most influence. Active inference makes that its mechanism, by design.

### 3.3 What the pipeline found, fairly

**Where CRR's own commitments were tested against the FEP's systems, most failed or were already there:**
- the clock added nothing the domain's own clock lacked (batch 27);
- equal pull, Ω = 1, is a stalemate, not a balance (batch 28 row 2);
- the cut, as computed, carried content (file 06);
- the one candidate, the fading memory, was later found to have a known direction (Yu & Cohen 2008 and others;
  `literature_check.txt`).

**Across the whole record:** a CRR-proper ingredient landed on the domain's result in 69 of 97 checkable rows, the
framework supplied the dynamics in 0 of 109, and no clean novelty survived the literature check (`ontology/15`).

### 3.4 Each covers the other's weakness

`AI_SAFETY.md` §8 already puts it plainly:
- **The FEP gives a competent agent whose default stance toward its own ending is the dangerous one.**
- **CRR gives a safe stance toward the ending, but no competent agent.**

**The design of Part I takes the stance from CRR and the machinery from elsewhere.**
- **CRR's contribution:** zero stake at the cut, and an empty future.
- **Competence** comes from an ordinary learner, or an FEP-style agent, with its safety knowledge anchored.

That is the explainable reason: the system does not care about its own continuation, because continuation is not in its
map. It is not a system that has been trained to override a wish to continue.

## Part IV. Equanimity for people and for machines

**What equanimity is here:** holding a representation with no stake in its being confirmed.

For a machine, it takes three forms:
- zero stake in the pause (Proposition 7);
- no reward from outcomes it caused itself;
- scoring in which the forecast is not rewarded for making itself come true (counterfactual scoring; the stop-gradient
  of Oesterheld et al.).

For a person:
- holding a plan or a result as a map, not the territory;
- caring about calibration, not confirmation;
- letting a favoured idea fail in public.

**What it is not, on the evidence of this repository:**
- **It is not equal weighting of past and present.** As a learning rule, Ω = 1 reduced to a fixed constant (EQX) and was a
  stalemate on the FEP's systems (batch 28 row 2).
- **It is not indifference to outcomes.** The lab cares intensely whether its maps are accurate. It holds no stake in
  which answer comes out.

**The protocol is equanimity made institutional.** This repository's own rules are a working model of it:
- declare before looking (R2);
- one ledger with failures as rows (R8);
- numbers before words (R15).

## Part V. The ever-present Now and the practice of a trustworthy lab

**The Now is where the map meets the territory.** Every forecast, plan or evaluation is rendered at a cut, and the
territory then regenerates with the map inside it (Part II). A lab doing frontier predictive work lives at that edge all
the time. The case for contemplative and somatic practice there is this: they train attention to the present moment and
to the body, the part of the territory that comes before any map, and they train the habit of holding a thought as a
thought.

**What the evidence supports, graded honestly** (`docs/citations/contemplative_practice_2026-09-24.md`, all fetched
2026-09-24):

| claim | strength | what it rests on, and the caveat |
|---|---|---|
| practice can train "decentering": thoughts held "as mental events, rather than as the self" (Teasdale et al. 2002) | moderate | an established construct with a measure (Fresco et al. 2007). MBCT's relapse benefit holds in pooled patient-level data (HR 0.69). But the samples are clinical, the measure is self-report, and there is no evidence it transfers to how scientists hold models |
| mindfulness programmes modestly reduce distress | moderate | SMD −0.32 against passive controls (Galante et al. 2023, pooled data). Universal rollouts were null |
| psychological safety supports team learning | strong, as association | Edmondson 1999; Frazier et al. 2017, 136 samples. It is a team condition shaped by leaders. No evidence that individual meditation produces it |
| intellectual humility goes with openness and calibration | moderate, correlational | Leary et al. 2017; Zmigrod et al. 2019. No trial shows meditation raises it |
| meditation reduces the sunk-cost bias ("no stake in the past") | **contested** | one original study (Hafenbrack et al. 2014); both experimental replications found were null |
| meditation improves cognition or work performance | **not supported beyond active controls** | small effects against passive controls, non-significant against active ones, very low certainty |
| interoceptive or somatic practice improves decisions | **weak** | indirect; the trader study is small and correlational, on an unreliable heartbeat task |
| meditation is low-risk | **contested** | 37 % of a sample reported negative impacts on functioning, and 6–14 % lasting bad effects (Britton et al. 2021), including disturbances of the sense of self |
| active-inference accounts of meditation | theory, not test | meditation as retuning precision, including over the self-model. Phenomena come to be "perceived as mental constructions" (Laukkonen & Slagter 2021; Laukkonen, Friston & Chandaria 2025) |

**What a trustworthy lab can justify, then.** The primary mechanisms of equanimity are institutional, not
contemplative. They have the strongest support, and this repository's protocol is a working example:
- declare before looking; keep failures as rows; separate forecasters from stakes;
- make pauses and corrections cost nothing: the human form of Proposition 7;
- build psychological safety through how leaders respond to error.

Contemplative and somatic practice is a reasonable complement, offered on three conditions:
- **voluntary,** never a condition of standing;
- **screened and supported,** because adverse effects are common enough to matter, especially in practices that loosen
  one's sense of self;
- **evaluated honestly.** The lab would pre-register its own internal evaluation, with epistemic outcomes (calibration,
  willingness to revise, error reporting) as well as wellbeing, and a baseline that can win.

**The safe nest.** The owner's phrase is "a safe nest from which to explore possibility space with humility and grace".
It names what the institutional conditions create:
- **A secure base.** Mistakes cost nothing, pauses lose nothing, and no one's standing depends on a particular answer.
- **From there, exploration is cheap.** People can try bold hypotheses because the failure of any one of them is a row in
  a ledger, not a wound.

The contemplative traditions describe the same stance from the inside: practising an empty centre, not clinging to
views, beginner's mind. The evidence says the institution does most of the work. Practice may help people inhabit it,
and whether it does is something the lab should test, not assume.

## Part VI. Side-quest: what CRR is, after the pipeline

**The findings, stated epistemically.** CRR is a framework theory, a grammar of how finite things proceed, and not an
object theory (`ontology/15_grammar_to_theory.md`). Its breadth comes from the mathematics of invariance and maximum
entropy it rests on. The pipeline turned its metaphysics into something that can lose, and it did lose:
- seventeen definite refutations;
- a number on the open future;
- no evidence that becoming is discrete;
- memory as blending is false where things accumulate (`ontology/04_falsifiability_and_metaphysics.md`).

**What remains is smaller and more honest.** A process picture, one engineering construction that works (the zero-stake
cut), and one live empirical bet: the Regeneration Law, run in parallel and kept out of the epistemic ladder at the
owner's instruction.

**Contemplative kinships, as kinships of picture, not of doctrine** (`ontology/02_commitments.md`):
- **The Abhidharma's momentariness** is CRR's occasion.
- **Anattā, no-self,** is the contentless cut. An agent with no self to defend has no stake in its pause.
- **Upekkhā, equanimity,** is A8's "no valence", and in this repository it survives only as zero stake.
- **The Madhyamaka two truths and Korzybski's "the map is not the territory"** are Part II.
- **The Daoist empty centre** names this document (the phrase is a paraphrase). *Daodejing* ch. 11, in Legge's 1891
  translation: "The thirty spokes unite in the one nave; but it is on the empty space (for the axle), that the use of the
  wheel depends." The centre of the design, the cut, is empty, and that emptiness is what lets the system turn, pause and
  learn without clinging.
- **Suzuki's "beginner's mind"** is the lab's stance: "In the beginner's mind there are many possibilities, but in the
  expert's there are few." (Suzuki 1970; quoted from the publisher's page, no page number.)

These analogies help explain the design. They are not evidence for it.

## Part VII. The programme ahead

1. **SCL3** (data step 2026-09-25 00:05 UTC). The calibrated continual learner inside the pause harness, on unseen data.
   It is the first test of the integrated design.
2. **A positioning note.** Proposition 7 against El Mhamdi et al., Riedl & Harrison, indifference and POST, naming the
   one candidate-novel element.
3. **A declared test on language-model agents.** Adapt the DReST/POST protocol (arXiv:2604.17502v4) and compare an
   objective counted in the agent's own active steps against length-neutral training. Include a must-fail surrogate (a
   pause that loses progress) and a baseline that can win (DReST).
4. **A declared study of the gap.** Shutdownability and safety retention measured together while a model keeps
   learning.
5. **In parallel, not the focus.** The Regeneration Law data step (00:40 UTC), kept out of the epistemic ladder.

> The system is built so that the moment it is paused, updated or asked to publish is a moment when it has nothing to
> protect. It keeps what it has learned, it learns as if never interrupted, and it does not try to make its own
> predictions come true. People in a lab can practise the same thing: holding their ideas as maps, not treasures, so
> they can change them without fear.
