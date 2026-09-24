# 15 — What CRR is, epistemically, and how it could become a theory: recommended next steps

**Status of this note**
- **Source.** Written 2026-09-24 at the owner's request (prompt-log entry 136) from two scratchpad answers (entries 134
  and 135). It is a note and a recommendation, not evidence (R8).
- **Numbers.** Every number is printed by `Epistemic_Review/checks/ladder.py` (pinned in `ladder.txt`), by
  `theory/retrodictions/synthesis_batches/literature_check.py`, or by a pinned batch output.
- **Literature.** Philosophers and scientists are named by name and year as context only. They were not fetched (R10),
  except where a `docs/citations/` file is named.

---

## Part I — What CRR is, in epistemic terms (prompt-log entry 134)

### The facts the answer rests on

| fact | value | source |
|---|---|---|
| real-domain synthesis rows | 164 | ladder.txt |
| where a CRR-proper ingredient changed the number and could be checked, it landed on the domain's result | 69 of 97 (0.7113; Wilson 95 % 0.6145–0.7921) | ladder.txt |
| rows that are information geometry's, not CRR's (R1) | 39 | ladder.txt |
| rows whose dynamics the framework supplies (FLOW audit) | 0 of 109 (the domain: 98) | ladder.txt |
| SHARP rows (the axioms force a known result with no outside constant) | 0 of 197 | ladder.txt |
| ADDS rows that survive the literature check as clean candidates | 0 of 10: 3 redundant by the literature, 6 direction known, 1 artefact | literature_check.txt |

### The epistemic kind

1. **A framework theory, not an object theory.** It belongs with thermodynamics, information theory and Bayesian
   inference. CRR has no equations of motion (`theory/CRR.md` §0). It supplies form: a unit, a state function, an event,
   a rule of succession. Its reach comes from being silent about mechanism.
2. **Explanatory unification without novel prediction.**
   - *Kitcher 1981, 1989:* one argument pattern, "occasion → cut → regeneration from the settled past", instantiated
     across many fields.
   - *Whewell 1840:* a consilience of retrodictions. It is not yet the consilience that counts most, where a
     hypothesis built for one class of facts predicts an unexpected class.
3. **A Lakatosian research programme** (Lakatos 1970).
   - The hard core is A3, A6, A7/A8, H-L5 and H-EQ; the protective belt is the [M] modelling steps.
   - It is not refuted: it lands about 70 % of the time where it can be checked.
   - It is not yet progressive: no novel fact has been corroborated.
   - Heuristic power is high; excess empirical content so far is none.
4. **Why one formalism works in so many places.** CRR's working parts are the mathematics of invariance and maximum
   entropy:
   - the Fisher metric is the unique invariant metric (Čencov 1982);
   - one constraint gives exponential or geometric weights (Jaynes 1957; Shore & Johnson 1980).

   That mathematics is universal because it is derived from symmetry and minimal assumption, not from the world. The
   literature check showed the consequence. CRR's regeneration with P3 weights *is* the exponential memory kernel each
   field rediscovered:
   - Nerlove's adaptive expectations;
   - Friedman's permanent income;
   - Rescorla–Wagner and the Kalman gain;
   - MacDonald's weak kernel;
   - Tolkacheva's memory criterion (`docs/citations/litcheck_*_2026-09-24.md`).

   CRR found the common form that many fields independently had to invent. This is a real finding, and it is
   universality inherited from the mathematics. The failures confirm it: CRR goes wrong where a field's sufficient
   statistic is not one-scale, one-clock, one-memory (`docs/notes/2026-09-24_in_paradigm_predictions.md`;
   `ontology/14_smolin_rovelli_gough.md` §6).
5. **Structural realism, read cautiously** (Worrall 1989). CRR catalogues structure that recurs across domains:
   occasions, bounded memory, a system's own clock. On structural realism, that kind of structure is what survives
   theory change. CRR is then a candidate periodic table of how finite things continue, not a theory of what they are.
6. **A formal process ontology.** CRR's *occasion* is Whitehead's "actual occasion" (Whitehead 1929), given an
   information-geometric bookkeeping. That is probably its deepest philosophical lineage.
7. **The risk: breadth from flexibility.** The author chose which CRR ingredient to apply per domain, and 28 rows were
   still WRONG. A framework that fits everything would be empty. This one is not, because it fails where the domain's
   statistic is multi-scale, accumulative, memoryless or state-stored. That is the evidence that it is not merely
   flexible.

**One line.** CRR is a correct abstraction of what many sciences independently had to discover; it has not yet told any
of them something they did not know.

### Names for it, and titles for a book

**Epistemic names:**
- a grammar of becoming;
- a framework theory;
- a unifying schema;
- a formal process ontology;
- a thermodynamics of occasions (form without mechanism);
- a lens, or a heuristic over existing mathematics, as the repository already says.

**Titles.** They are built from its commitments: the occasion, the contentless cut, the settled past, the empty
future, the system's own clock, equanimity.
- *The Grammar of Becoming: Coherence, Rupture and Regeneration* (it says exactly what the thing is).
- *Change Has Its Own Clock.*
- *Occasions: How Finite Things Continue.*
- *The Empty Cut.*
- *The Settled Past and the Open Future.*
- A subtitle that is honest and distinctive: *… : A Metaphysics That Submitted to Pre-Registration.* Few metaphysical
  systems have been put through surrogate gates, hashed predictions and a literature check of their own "discoveries".

---

## Part II — How CRR could become a theory (prompt-log entry 135)

### The diagnosis

**CRR fixes nothing.** CRR.md says so in its own words:
- "CRR does not fix β" (P2);
- "does not fix q" (P3);
- "does not predict ρ" (D1).

κ is free. Ω = 1 is a plateau and reduces to a constant (EQX, EQ2, EQ3). The framework supplies the dynamics in 0 of 109
rows. So once a domain plugs in its own parameter, every CRR prediction becomes the domain's. That is why the ADDS rows
dissolved: Kalman fixes q, Tolkacheva's slopes fix the alternans threshold.

**A grammar becomes a theory when it fixes something.** It must supply at least one of:
- a constant;
- a parameter the domain leaves free;
- a relation between two quantities the domain treats as independent;
- a dynamics.

The fixed value must be risky, CRR-only and confirmed on unseen data, and then replicated (PASS-2).

### Five routes, ranked by realism

1. **The regeneration law: fix the memory depth. The recommended empirical route.**
   - **The question.** CRR.md lists it as open (O1): does a system's memory depth follow from its own state model at
     Ω = 1 with no other parameter?
   - **The candidate law, with zero free parameters.** For any system that regenerates from its settled past,
     **q\* = 1 − K(v)**. Here v is the drift of the system's environment per occasion, measured in the system's own
     resolvable steps (A1′), and K is P4's Kalman function.
   - **What is CRR's alone.** Kalman derived this for optimal linear-Gaussian filters. CRR would claim it for every
     regenerating system, including ones that do no inference, with v counted in the system's own unit rather than the
     instrument's.
   - **How to test it.** Measure v and the memory kernel independently on unseen data in three or more unrelated fields.
     Candidates:
     - sensory adaptation time constants against stimulus volatility;
     - animal learning rates against reward volatility;
     - forecasters' smoothing against inflation volatility;
     - physiological or immune set-points against input variability.
   - **Baselines that can win:** the domain's own fitted memory, and a constant memory.
   - **Its known neighbour:** optimal learners track volatility (e.g. Behrens et al. 2007; Fairhall et al. 2001 on
     adaptation). **The literature check comes first.**
2. **A dimensionless invariant.** One number the same across unrelated systems, as Feigenbaum's δ or a critical exponent
   is. An example is the resolvable steps per occasion at the cut.
   - It is the boldest route and the least likely to survive. The earlier strong form, C·Ω = 1, was removed after it
     failed (`ontology/checks/delta_now.txt`).
   - It is cheap to gate on the existing synthetic batteries before anything is registered.
3. **A dynamics: a variational principle.** For example: occasions minimise surplus, or they travel at constant Fisher
   speed.
   - This is the thermodynamics → statistical mechanics move. It would supply the flow the FLOW audit found missing.
   - The danger is already on record. In batch 02 row 2, batch 10 row 5 and batch 15 row 4, the domain's friction is
     the Fisher metric times a relaxation tensor, so "the Fisher geodesic" is not the optimum.
4. **A mathematical theory of regeneration: theorems, not predictions.** Two results would form its core:
   - the lemma family found on 2026-09-24: a bounded exponential memory multiplies a one-dimensional map's flip
     threshold by (1 + q)/(1 − q), and adds phase lag to a continuous feedback loop; the direction depends only on the
     model's type;
   - Proposition 7 for learners (zero stake under a lossless pause on the system's own clock).

   This makes CRR a formal theory, like decision theory: true, useful, publishable, not empirical. It is the recommended
   companion route.
5. **An engineering and normative theory: design rules that work by construction.** Examples are the corrigible pause
   and the continual-learning rules (`AI_Safety/`, `Safe_and_Continual/`). This is where CRR's distinctive commitments,
   the contentless cut and the system's own clock, actually did work. It needs its own literature check against safe
   interruptibility (Orseau & Armstrong 2016) and utility indifference (Armstrong 2010) before any novelty is claimed.

### Lessons the attempt must carry (from this repository's record)

- **Fix the ingredient first.** Decide which CRR ingredient applies *before* looking at a domain; do not choose it per
  domain after the fact.
- **Check the literature before declaring anything, not after.** The ten ADDS rows dissolved afterwards
  (AGENT_LOG 110).
- **Use estimators independent of the event definition.** Batch 32 row 2's pass was forced by the analytic signal's
  arithmetic (AGENT_LOG 109).
- **Keep the full protocol:**
  - a blind declaration;
  - OpenTimestamps anchoring (now working and Bitcoin-attested; `runs/scl3/ots_upgrade.txt`);
  - a surrogate that must fail;
  - a baseline that can win;
  - unseen data;
  - per-unit scoring;
  - replication by a second person (Daniel).
- **State success and failure in advance.**
  - Success: a zero-free-parameter prediction reaching PASS-2 on two or more unrelated unseen carriers.
  - Failure: CRR stays a grammar, a legitimate outcome (R12).

---

## Recommended next steps

1. **Route 1, step 1: the literature check.** Is "memory depth tracks environmental volatility" already a law in each
   candidate field, and in what form? Use the dossier method of prompt-log entries 130 and 132, with the rule for how
   findings bind fixed first.
2. **Route 1, step 2: derive the law formally.** State exactly how v (drift per occasion, in own resolvable steps) and
   q (memory depth) are measured, independently of each other. Write down what would make the law fail.
3. **Route 1, step 3: gate it.** Use synthetic regenerators on which the law must pass and ones on which it must fail,
   under R4.
4. **Route 1, step 4: three blind, anchored preregistrations** on three unrelated unseen fields, each with the domain's
   fitted memory as a baseline that can win, then replication.
5. **In parallel, route 4.** Write the mathematical core: the regeneration-kernel theorems and Proposition 7, with
   proofs checked by script, as `theory/checks/` already does for the [P] items.
6. **Route 5's literature check** before any AI-safety or continual-learning novelty is claimed outside the repository.

**What each outcome means.**
- If route 1 passes and replicates, CRR has its first law and becomes a theory.
- If it fails, the book is *The Grammar of Becoming* plus its theorems, told honestly. That is still a real
  contribution.

> **For a fifth grader.** CRR is like a grammar: a set of rules for how things in the world keep going, stop, and start
> again. It fits a surprising number of things, but so far, whenever it fits, it turns out scientists already knew that
> part. To become a real theory it has to guess one number that nobody knew and get it right on something nobody has
> looked at yet. We have a good idea for which number to try: how much of the past a thing remembers.
