# 14. Smolin, Rovelli and Gough through CRR: the physics, the metaphysics, and where CRR adds

**Status of this note**
- **Scope.** Owner request 2026-09-24 (prompt-log entry 130). A note, not evidence (R8).
- **Where the numbers come from:** the pinned outputs of synthesis batches 29 (Rovelli) and 30 (Smolin), which were
  declared first in `theory/retrodictions/synthesis_batches/DECLARATION_29_30.md`, and the ladder
  (`Epistemic_Review/checks/ladder.txt`).
- **The authors' own statements** come from three research dossiers compiled from primary texts on 2026-09-24:
  `docs/citations/{rovelli,smolin,gough}_dossier_2026-09-24.md`, indexed in
  `docs/citations/smolin_rovelli_gough_2026-09-24.md` with arXiv versions.
- **Rungs.** Every synthesis row is a retrodiction at rung R1–R3. None is a ledger row, and nothing here is a finding.

## 0. The result in one table

| row | author, bottleneck | CRR ingredient | outcome | what it says |
|---|---|---|---|---|
| 29-1 | Rovelli, thermal time | H-L5 natural time (arc of the state) | REDUNDANT-DOMAIN | along thermal time, CRR's clock ticks at √(Var K), the capacity of entanglement (1.024690 against 1.024690) |
| 29-2 | Rovelli, thermal equilibrium (Haggard–Rovelli) | H-EQ between two arc clocks | **WRONG** | equal natural-time rates put T₂/T₁ at 0.5011, where heat still flows; thermal time, not the arc clock, is the equilibrium clock |
| 29-3 | Rovelli, "every state is in equilibrium with its own flow" | A3 the cut | REDUNDANT-DOMAIN | the cut never fires on a finite-temperature thermal flow (closest approach 0.462117 = (1 − x)/(1 + x)) |
| 29-4 | Rovelli, relational QM's stable facts | A3/D5 | **WRONG** | the cut fires in both a 2-spin and a 12-spin environment; only redundancy (N) makes a fact stable |
| 29-5 | Rovelli, the white-hole lifetime's undetermined spread | H-EQ between conjugate spreads | REDUNDANT-DOMAIN | equal pull gives t = ħG/m², their "balanced" state (n = 2) |
| 30-1 | Smolin, precedence lock-in | A6 bounded memory | **WRONG** | lock-in spread falls (0.1870 → 0.0869) but outcomes become correlated (lag-1 +0.4990); quantum mechanics needs 0 |
| 30-2 | Smolin, the unspecified inheritance kernel of cosmological natural selection | A6 lineage memory | **ADDS (candidate)** | lineage memory lowers the equilibrium load (0.02743 against 0.04998) at the cost of a slower climb (14 against 7 generations) |
| 30-3 | Smolin, "a time is required to count generations" | D5 + H-L5 natural time | REDUNDANT-DOMAIN | in generations the ensemble sits at the peak of black-hole number (0.3000); in clock time it moves (0.2500) |

**Tally.** 1 ADDS candidate, 4 REDUNDANT-DOMAIN, 3 WRONG. With these rows the ladder reads 154 real-domain synthesis
rows and a retrodictive hit rate of 61 of 88 = 0.6932 (Wilson 95 % interval 0.5904 to 0.7798), unchanged in
character.

**The short answer to the owner's question:**
- **Rovelli.** There is no CRR ADDS in Rovelli's mathematics.
  - Where CRR touches his open problems of state selection (which state defines time; which boundary state sets the
    white hole's lifetime), it supplies a *reason* for a choice he has already made.
  - Where it touches equilibrium and facts, it is wrong.
  - Where his bottlenecks are dynamical (spin-foam flatness, the continuum limit, the Hamiltonian constraint), CRR has
    nothing to say, because it supplies no dynamics.
- **Smolin.** There is one ADDS candidate, in the least specified part of his work: the inheritance law of cosmological
  natural selection.
  - CRR's regeneration axiom supplies a law there, with a checkable consequence.
  - The candidate is still unreviewed. Karlin's reduction principle (Altenberg 1302.1293 v2) already predicts its
    direction, and the transgenerational-inheritance literature may already contain the kernel.

---

## 1. Rovelli through CRR: the physics

### 1.1 Thermal time and change time (rows 29-1, 29-3)

**The earlier gap.** Synthesis row 10 of `synthesis.txt` could not form a proposition relating Connes–Rovelli thermal
time to CRR's clock: one is the state's *flow*, the other the state's *change*.

**Row 29-1 forms one.**
- **The construction.** Purify the Gibbs state, and let the modular flow act on one side (the flow Connes and Rovelli
  call time).
- **The result.** CRR's arc per unit of thermal time is √(Var K), with K = −ln ρ the modular Hamiltonian. That is the
  square root of the *capacity of entanglement* (Yao–Qi; de Boer et al.), which for a Gibbs state equals the square
  root of the heat capacity in k_B.
- **The value.** The pinned value is 1.024690 on all three expressions.

**The CRR reading.** Thermal time counts ticks; CRR's time counts distinguishable change. They differ by one number, the
system's capacity to hold heat. A state with no energy spread has thermal time and no natural time: a clock ticking over
nothing.

**Row 29-3 adds the other half.** On a finite-temperature Gibbs state the thermal flow never reaches an antipode.
- **The number.** On an equally spaced spectrum, the closest approach to orthogonality is (1 − x)/(1 + x), 0.462117 at
  βΔ = 1. At infinite temperature the flow does reach it.
- **The reading.** CRR's occasion ends at a cut (A3). Thermal time is a flow without cuts: in Rovelli's time things
  flow, in CRR's time things happen.
- **Why it is only a reading.** The numbers are the characteristic function's closed form, so the row is
  REDUNDANT-DOMAIN.
- **What the domain adds.** Exact zeros do appear in the thermodynamic limit (dynamical phase transitions, the spectral
  form factor's dip). So "no cut in thermal time" is a finite-system statement.

### 1.2 Equilibrium (row 29-2): CRR is wrong, and Rovelli is right

**Haggard–Rovelli's reading.** Haggard and Rovelli (1302.0724) read thermal time as τ = kT·t/ħ, "counting
distinguishable states transited". They define equilibrium as equal τ rates, which is equal temperatures, the zeroth
law.

**The CRR proposition.** CRR's count of distinguishable states along the same flow is the arc of row 29-1, whose rate
per unit physical time is √C·T. Equal *arc* rates between two systems would be CRR's equanimity (H-EQ, Ω = 1) applied
between them.

**The test.**
- **The setup.** A 4-mode and a 16-mode system in the same band.
- **The result.** Equal arc rates put T₂/T₁ at 0.5011, and the golden-rule heat current there is 5.298e-01 of the
  one-way current. That is not equilibrium.
- **What this shows.** The equilibrium clock counts distinguishable change *per degree of freedom* (kT/ħ). CRR's arc
  counts it for the whole state, and so grows with the square root of the system's size.

**The lesson for CRR.** Equanimity as "equal clock rates between systems" is contradicted by the zeroth law. Rovelli's
count is the one that equalises.

### 1.3 Relational facts (row 29-4): the cut is not a stable fact

**Rovelli's side.** In relational quantum mechanics, facts are relative to a system. Stable facts arise through
decoherence (Di Biagio–Rovelli).

**The CRR candidate.** A fact is fixed at a cut: the first time the two branch records become orthogonal.

**The test.** In Zurek's spin environment the cut fires in both environments:
- N = 12: at t = 1.0537;
- N = 2: at t = 1.2368.

After it, both records partly recohere:
- N = 12: the maximum overlap is 0.1181;
- N = 2: it is 0.9946.

The large environment becomes stable only from t = 14.7096, 14.0 times its cut time. The small one never does in the
window.

**The reading.** Stability is a property of *how many* systems hold the record (redundancy, quantum Darwinism). A single
orthogonality event does not make a fact. CRR's cut, read as the moment of a fact, is wrong here. Relational facts are
many-record facts.

### 1.4 The white-hole lifetime (row 29-5): equanimity is their balanced state

**The open parameter.** The black-to-white-hole lifetime from the covariant amplitude depends on the boundary state's
spread t (Christodoulou–D'Ambrosio 1801.03027 v3):
- the conjugate spreads are Δζ ∼ √t and ΔA ∼ ħG/√t (eq. 53);
- semiclassicality needs ħG/m² ≪ √t ≪ 1 (eq. 54);
- the authors choose the geometric mean, t = ħG/m² (eq. 56), for want of a better argument ("we do not have a better
  argument for what should be the chosen value of t");
- the lifetime is then τ ∼ m·e^{m²Ξ/ħG} (eq. 58).

**The row.**
- **With equal pull.** H-EQ between the two relative spreads (each variable in its own unit: Δζ/1 = ΔA/A) gives
  t = ħG/m², the same state (n = 2.0000 against their 2.0000).
- **The naive balance.** Equal absolute spreads give n = 0, outside the window.

**What CRR supplies.** A reason for their choice: hold each conjugate variable equally loosely in its own unit. It
supplies no new number. The open problem moves from "why the balanced state" to "why Ω = 1", which CRR does not derive
either (`reports/eq2.md`, `reports/eq3.md`: Ω is a plateau).

### 1.5 Loop quantum gravity's kinematics and dynamics: where CRR is silent

**Kinematics.** Earlier rows put CRR's unit on LQG's kinematics (`batch_25.txt`, `batch_26.txt`, `synthesis.txt` row
11). The area spectrum's smallest spacing, the entropy per puncture and the polymer oscillator's expansion parameter
were all the domain's own numbers (REDUNDANT-DOMAIN or INTERNAL).

**Dynamics.** Rovelli's hardest bottlenecks are dynamical:
- the flatness problem of the EPRL semiclassical limit;
- the continuum limit and coarse graining (Dittrich, Bahr–Steinhaus; a 2026 no-go for strong convergence);
- the ambiguity of the Hamiltonian constraint (Varadarajan's anomaly-free result is Euclidean only);
- the cosmological constant in spin foams.

**Why CRR says nothing on the dynamical side.** This is the same fact as the FLOW audit of the retrodiction batteries:
the domain supplies the velocity in 98 of 109 rows and the framework in none. CRR has no equations of motion (CRR.md
§0). A theory that supplies coordinates, a unit and a bookkeeping cannot fix a spin-foam amplitude.

---

## 2. Rovelli through CRR: the metaphysics

**What is shared, which is a great deal:**
- **Relations over substances.** Rovelli: "there is nothing that exists in itself, independently from something else"
  (Helgoland, after Nāgārjuna). CRR: the carrier is a system's own manifold; its unit is the system's own resolvable
  step (A1′); tense is relational (A7: "what is future for a system can only be fed by what is already past for
  something").
- **Events, not states.** RQM's ontology is of events (values of variables at interactions). CRR's is of occasions
  ended by cuts.
- **No global time.** Thermal time is state-dependent. CRR's natural time is the system's own event count or arc. Both
  deny a master clock, and row 29-1 shows exactly how the two local clocks relate.
- **Emptiness.** Rovelli reads Nāgārjuna's emptiness as the absence of intrinsic existence. CRR's cut has no duration and
  no content (A3), and the future has no content (A8).

**Where they part:**
1. **Becoming.** Rovelli: "fundamental becoming is real, but local and unoriented" (1910.02474). Orientation comes from
   the entropy gradient and is perspectival (1505.01125, stated as a conjecture). CRR orients becoming at every cut (A3:
   "orients the next half-turn"), so orientation is primitive and local rather than statistical. Row 29-3 sharpens the
   difference: Rovelli's thermal flow has no cuts, so it cannot orient anything. The orientation must come from
   elsewhere, which on his account is entropy and on CRR's is the cut.
2. **What a fact is.** Row 29-4: RQM's stable facts need many records. CRR's single cut is not enough. On facts,
   Rovelli's decoherence account carries the weight; the cut does not.
3. **What time counts.** Row 29-2: time as distinguishable change per degree of freedom (Rovelli) passes the zeroth
   law. Time as the whole state's change (CRR's arc) fails it. A CRR that wants equanimity between systems must count
   per degree of freedom, which is a change to H-EQ, not a vindication of it.

**A CRR paradigmatic reading of Rovelli.** Thermal time is a system's *ignorance flowing* ("time is the expression of
our ignorance of the full microstate", "Forget time"). CRR's time is a system's *change accumulating*. The two meet in
the capacity of entanglement, which measures how much change a state's own flow can carry. Where the capacity is zero
(a pure state, a ground state), Rovelli's flow is trivial and CRR's clock stops. Where it is large, the thermal clock
carries much change per tick. A contemplative gloss, marked as such: Rovelli's time is the rain; CRR's is the river the
rain fills.

---

## 3. Smolin through CRR: the physics

### 3.1 Precedence (row 30-1): bounded memory treats lock-in and breaks independence

**Smolin's principle** (1205.3707 v1, Postulate 6): a measurement's outcome is a random draw from the outcomes of its
precedents. He names the problem himself: "all future measurements would repeat the first random choice" (lock-in). As
a sampling law, precedence is a Pólya urn.

**A6 is the obvious CRR repair:** a bounded, age-weighted precedent, never an accumulated count.

**The run.** 200 worlds, Born p = 0.3, 5 % free draws.
- **Lock-in.** A6 cuts the spread of the long-run frequency across worlds from 0.1870 to 0.0869. The binomial spread
  is 0.0065.
- **Independence.** A6's precedent is a small, self-feeding sample, so successive outcomes are correlated: lag-1
  +0.4990, against −0.0009 for precedence as stated.

**The verdict.** Quantum mechanics requires independent outcomes on independently prepared systems, so the row is
WRONG. Neither form of precedence recovers Born statistics from precedent alone, which is Smolin's open problem ("a
novel principle" for the small-n regime). On quantum outcomes, CRR's "never an accumulated count" is on the wrong side
of that problem.

### 3.2 Cosmological natural selection (rows 30-2, 30-3): the one candidate

**What is missing.** CNS (hep-th/0612185 v1) is a branching process on the space of parameters, and it lacks a defined
process:
- the mutation kernel is unspecified;
- the fitness functional is qualitative;
- the convergence to local maxima is asserted, not proved;
- the measure over generations is open.

In Smolin's words, "a time is required to count generations".

**Row 30-2: CRR supplies the inheritance law.**
- **The law (A6).** A universe's seed parameter is the bounded, age-weighted mean of its lineage, not its parent's
  value alone.
- **The consequence, in a Gaussian replicator–mutator** (black-hole fitness ∝ e^{−x²/2}, mutation variance 0.01):
  - the equilibrium variance falls from 0.10512 to 0.05639;
  - the mutation load falls from 0.04998 to 0.02743;
  - so universes sit closer to a local maximum of black-hole production.

This sharpens Smolin's master prediction M: almost every small change in the parameters lowers black-hole production.

**The price.** The climb is slower: 14 generations to halve a displacement against 7.

**The label.** The harness labels the row ADDS: the domain's closed form gives the parent-only value exactly, and no
formula for the A6 kernel was found. It is a *candidate*:
- the direction, that more faithful inheritance raises mean fitness, is Karlin's reduction principle, which Altenberg
  applied to CNS;
- the kernel may exist in the transgenerational-inheritance literature (Kirkpatrick & Lande 1989, maternal effects;
  Day & Bonduriansky 2011), which was not fetched.

**Row 30-3: CRR names the clock.**
- **The claim.** Counted in natural time (generations: one universe, one occasion), the ensemble concentrates at the
  maximum of black-hole number (mode 0.3000), which is Smolin's fitness.
- **The contrast.** Counted in clock time, when fitter universes take longer, it concentrates near the Malthusian
  optimum (0.2500; the rate's argmax is 0.2450).
- **The label.** REDUNDANT-DOMAIN: the generation theorem of branching processes gives the number. CRR's contribution
  is the choice: the prediction is a statement in the system's own time, generations, as H-L5 says it should be.

### 3.3 What CRR cannot help with

**The neutron-star bound.** CNS's sharpest prediction is Smolin's upper bound on neutron-star mass, revised in 2012
(1202.3373) to under 2 solar masses. It is under strain from measured masses:
- PSR J0740+6620: 2.08 ± 0.07 (2104.00880 v2);
- PSR J0952−0607: 2.35 ± 0.11 (2512.05099 v1).

Brown, Lee and Rho (0802.2997) state that any mass above 2 solar masses puts the kaon-condensation chain, and with it
this CNS prediction, "in serious doubt".

**No Smolin reply after 2019 was found.** CRR has nothing to add to nuclear physics. Row 30-2's sharper
concentration at a local maximum makes CNS's predictions *more* committal, not less. It does not rescue the bound.

**The other programmes.** Energetic causal sets, the causal theory of views (variety), the real-ensemble formulation and
the Autodidactic Universe are each read structurally in §4. No row was formed, for different reasons:
- **Energetic causal sets:** the open problems are measure factors and embeddability, which are dynamics again;
- **Variety:** the definition is not unique, and CRR has no uniqueness argument either;
- **Real ensemble:** its open problem is the relaxation to |ψ|². That is the same Born-weight gap as row 30-1, and
  row 30-1 shows A6 does not close it.

---

## 4. Smolin through CRR: the metaphysics

**Smolin's metaphysics is the closest to CRR of the three.** Temporal naturalism (*Time Reborn*; Unger & Smolin, *The
Singular Universe*) holds that:
- time is real;
- the present is all that exists;
- the future is open;
- laws evolve.

**CRR's corresponding commitments:**
- the future has no content (A8);
- nothing is fed by a future (A7);
- the next occasion is seeded from the settled past (A6).

**Precedence is CRR's regeneration applied to laws.** Nature does what it did before: the settled past seeds the next
occasion. The difference is the one row 30-1 tested: Smolin's precedent accumulates; CRR's is reweighted at bounded
strength.

**The metalaw regress.** Smolin's cosmological dilemma asks what law governs the evolution of laws. CRR's answer would be
that no law governs it: only regeneration from the settled past at bounded strength, with maximum-entropy weights (P2,
P3). That is a proposal, not a theorem, and it inherits the unfixed constants (β, q, κ).

**Where they part:**
1. **Accumulation.** Smolin's laws gain authority by accumulating precedent. CRR forbids the accumulated count (A6). On
   quantum outcomes, row 30-1 favours Smolin. On inheritance between universes, row 30-2 favours CRR. The difference is
   whether the domain needs *independence* (outcomes) or *faithfulness* (lineages).
2. **The cut.** CNS's reproduction is a black-hole bounce: a singularity resolved into a new beginning. That is CRR's
   cut in its strongest form (A3: settles the occasion, resets C, orients the next). In CRR's terms a universe is one
   occasion. Its content settles at the bounce and seeds the next universe by regeneration, and row 30-3 counts its
   evolution in occasions, not clock time. Smolin needs a quantum-gravity bounce with parameter change, which is
   unproved (dossier §1d.6). CRR supplies the reading, not the bounce.
3. **Novelty.** Smolin's "freedom in the absence of precedent" is a genuine novelty clause. CRR has no novelty clause:
   A6 only reweights the settled past. A CRR that wants genuinely new laws needs something like Smolin's free draws, the
   5 % in row 30-1, which the axioms do not provide.

---

## 5. Gough through CRR

Julian Gough's proposal is in `gough_dossier_2026-09-24.md` (Substack 2022–2026; unpublished book *The Egg and the
Rock*; "Blowtorch Theory" 2025).

**The proposal: a three-stage CNS.**
1. Direct-collapse supermassive black holes form first, from smooth gas.
2. Stellar black holes come second.
3. Technological black holes come third, credited to Vidal, Smart, Price and Crane.

Life and intelligence are thereby selected for. The universe is "an egg, not a rock": development within a universe,
evolution between universes.

**Why there are no synthesis rows.** Gough's claims are qualitative, and his quantities shift between posts. The first
wave of black holes goes from "a couple of hundred million" (2023) to "a trillion" (2025), and the formation window
from "≤300 Myr" (2022) to "first 50–100 Myr" (2025). No domain mathematics was found in which a CRR ingredient could be
checked. Physicists have responded only in press quotes, and no peer-reviewed assessment was found.

**The CRR reading, a reading only:**
- **Development and evolution map onto CRR's two phases.** Development within an occasion is coherence accumulating
  (D2, the arc since the last cut). Evolution between occasions is regeneration (A6) across a cut (A3). Gough's
  egg/rock contrast is CRR's claim that a system's history is occasions with content, not a decaying trajectory.
- **The three stages are three kinds of cut.** Each adds a way for an occasion (a universe) to end and seed successors.
  In row 30-3's terms, more reproductive events per universe raise f, and a technological stage raises it further. That
  makes life part of the fitness, as Gough says.
- **"The oldest way of reproducing is retained"** is regeneration from the settled past (A6): the seed carries the
  lineage. Row 30-2 says lineage memory makes the family sit nearer its peak. Gough's claim that the first stage is kept
  is the qualitative form of that.
- **The empirical risk is shared.** Gough's stage 2 is Smolin's stellar black holes. The neutron-star mass bound (§3.3)
  bears on it, and Gough's JWST predictions are checkable, but not by CRR.

---

## 6. Where CRR adds, and why there and not elsewhere

**The earlier map, and this batch.** The map of prompt-log entry 129 sorted CRR's retrodictions by kind of system.
- **Where they work:** systems whose sufficient statistic has one scale, one clock and one bounded memory.
- **Where they fail:** driven systems with several relaxation times, history stored in a state variable, evidence that
  must accumulate, memoryless processes, and inference agents.

This batch fits that map.

**Rovelli's bottlenecks are of two kinds:**
- **Dynamics** (spin foams, constraints, the continuum): CRR has nothing.
- **State selection** (which state defines time; which boundary state fixes the lifetime): CRR's equal pull reproduces
  the choice the domain already made (rows 29-1, 29-5).

Where CRR's own clock is put in charge (equilibrium, facts), it fails, because the domain's quantity counts per degree of
freedom or per record (rows 29-2, 29-4).

**Smolin's bottlenecks are missing process rules:** an inheritance kernel, a precedent rule, a measure. That is exactly
what CRR's regeneration axiom and natural time supply. The result is one candidate that holds (30-2), one that fails
(30-1) and one that names the domain's own clock (30-3).

CRR is therefore more useful to a process metaphysics that needs rules (Smolin, Gough) than to a quantum-gravity
programme that needs dynamics (Rovelli).

**The lesson for CRR is also double:**
- **Accumulation is sometimes right.** "Never an accumulated count" is right where faithfulness matters (lineages). It
  is wrong where independence matters (quantum outcomes).
- **Equal pull needs the right units.** Equal pull between systems is not equilibrium unless it counts per degree of
  freedom.

Both are changes a v3.2 would have to consider. They are recorded here, not made (CLAUDE.md §10: a reinterpretation is
a new prereg).

## 7. Next steps

1. **Expert review of row 30-2.** Ask a population geneticist, or the author of the reduction-principle treatment of
   CNS, the class note's three questions (`docs/notes/2026-09-17_synthesis_class.md`): is the A6 inheritance kernel and
   its lower load already in the literature? Until then it stays R3, a candidate.
2. **Fetch and read the transgenerational-inheritance literature** named in row 30-2's weakness line: Kirkpatrick &
   Lande 1989; Day & Bonduriansky 2011.
3. **Test "equanimity per degree of freedom" as a declared synthetic check.** Row 29-2 shows H-EQ between systems
   fails in whole-state units. A version counting per degree of freedom would reproduce the zeroth law by construction,
   so it must be gated before it is claimed.
4. **Nothing here licenses a ledger study.** No row predicts a quantity measurable on unseen data. The closest is row
   30-1, and quantum mechanics already contradicts it.

> **For a fifth grader.** Three scientists have ideas about time and the universe. Rovelli says a warm thing carries its
> own clock. CRR says time is how much something changes. We found that the two clocks are linked by how much heat the
> thing can hold. But when two things touch, it is Rovelli's clock that has to match, not ours. Smolin says baby
> universes are born inside black holes and are copies of their parents with small mistakes. CRR says each baby should
> also remember its grandparents. That keeps the family closer to the best recipe, and that might be new. Gough says the
> universe grows like an egg, and that life helps it make more babies. That is a lovely story, but it does not yet have
> the kind of maths we can check.

**Addendum, 2026-09-24 (the literature check, prompt-log entry 132).** Row 30-2, CNS with lineage-memory inheritance, is
**PARTIAL** after the literature check (`theory/retrodictions/synthesis_batches/literature_check.txt`). Its direction is
already published: Galton's ancestral law (Bulmer 1998), cascading maternal effects (Kirkpatrick & Lande 1989), and
Hoyle & Ezard 2012 on inheritance that slows the response while lowering variance and raising equilibrium fitness. The
variance, load and halving time as functions of q were not found. It stays R3, marked "direction known", and is no
longer the clean candidate §0 calls it.
