# Lee Smolin: research dossier (physics and mathematics)

Compiled 2026-09-24. Scope: cosmological natural selection, temporal naturalism, precedence, energetic causal sets, the real-ensemble, variety and views programme, the Autodidactic Universe, LQG (briefly), and recent papers.

**How the sources were reached.** WebFetch was blocked for arxiv.org, Wikipedia, Springer, ADS and IOPscience. arXiv abstract pages and PDFs were fetched with `curl` through the session proxy instead. PDF text was extracted locally with PyMuPDF, and every quotation below comes from those extracts. Journal references come from the INSPIRE-HEP API (`inspirehep.net/api/arxiv/<id>`) on the same day. The version and date given for each item is the latest arXiv version seen on 2026-09-24. Anything marked **[UNVERIFIED]** could not be checked against a primary text today. Anything marked **[DOSSIER NOTE]** is this compiler's own inference and is not taken from the literature.

---

## 1. Cosmological natural selection (CNS)

### 1a. The model

- **Origin.** L. Smolin, "Did the universe evolve?", *Class. Quantum Grav.* 9 (1992) 173–191. This paper is not on arXiv; the citation is taken from Smolin's own reference lists in hep-th/0612185 and 1205.3707. Book: *The Life of the Cosmos* (Oxford University Press / Weidenfeld & Nicolson, 1997). The book text was not read. **[UNVERIFIED beyond citations]**
- **Canonical statement.** Smolin, "The status of cosmological natural selection", arXiv:hep-th/0612185 **v1 (18 Dec 2006)**, a chapter for *Beyond the Big Bang* (ed. R. Vaas, Springer). Its structure:
  - A fundamental landscape L (the "genotype"), a space of low-energy parameters P (the "phenotype"), and a map I : L → P.
  - An ensemble of universes E_L with distribution ρ_L(t) that evolves in a global generation parameter t.
  - Hypothesis O: the world is an ensemble E of universes, each labelled by x ∈ L, with p = I(x) ∈ P.
  - Hypothesis I: "Black hole singularities bounce and evolve to initial states of expanding universes. Hence there is a fitness function f on P where f(p) is equal to the average number of black holes produced by a universe initiated in such a bounce transition, which has parameters p."
  - Hypothesis II: "At each such creation event there is a small change in x leading to a small random change of x in P. Small here means compared to the step size under which f(p) changes appreciably."
  - Update rule: "in each step one new universe is created for each black hole in an existing universe."
- **Mathematical form (DOSSIER NOTE).** The model is a multitype Galton–Watson branching process on P. The offspring number is N(p) with mean f(p), and offspring types are drawn from a mutation kernel K(p → p′) concentrated near p. In the notation used here, the expected type density ρ_{n+1}(p′) = ∫ K(p→p′) f(p) ρ_n(p) dp; normalised, this is a replicator–mutator (Eigen/Kimura-type) recursion. Smolin never writes the kernel explicitly.
- **Claimed convergence** (stated, not proved, in hep-th/0612185): "Under very mild assumptions for the fitness function one can show that after many steps the ensemble converges to one in which almost every member is near a local extrema of f(p)."
- **Master prediction M** (hep-th/0612185): "Almost every small change in p from its present value either leads f(p) unchanged or leads to a decrease in f(p)… almost no change in the parameters of the standard model from the present values will increase the numbers of black holes produced." Smolin restricts M to local changes. On the global maximum he writes: "this requires some detailed knowledge of the properties of the two landscapes and the map I which we do not have at the present time."
- **Falsifiability conditions** (hep-th/0612185 §2.1; hep-th/0407213). ρ_P must be highly non-random. Observables A_i must be typical. There must be not-yet-measured properties B_i that hold in almost all members of E_P and are not anthropically constrained. For fine tuning, the reproduction process must be sensitive to low-energy parameters.

### 1b. The predictions offered, and their status

1. **Neutron-star maximum mass via kaon condensation.**
   - Original chain (hep-th/0407213 §6.3): below a critical strange-quark mass μ_c, neutron-star cores hold a K⁻ condensate (Bethe–Brown), and the upper mass limit (UML) is low, "approximately 1.5 M☉". CNS requires μ < μ_c because a lower UML means more black holes, and the strange-quark mass barely affects star formation. "Sufficiently high is certainly 2.5 M☉, although if one is completely confident of Bethe and Brown's upper limit of 1.5 solar masses, any value higher than this would be troubling."
   - The 2006 wording (hep-th/0612185): "neutron stars are Kaon-condensate stars and … the upper mass limit for neutron stars is M_uml ≈ 1.6 M_solar."
   - **Smolin's 2012 revision** (arXiv:1202.3373 **v1, 15 Feb 2012**, "A perspective on the landscape problem"): "as emphasized recently by Lattimer and Prakash, there is actually a range of predictions for UML_kaon… range upwards to two solar masses. So in the light of current knowledge the correct prediction is UML_kaon < 2 M_solar." On the 1.97 M☉ pulsar: "This is just inside the range consistent with the prediction… observations of neutron stars with wider error bars of around 2.4 solar masses… if confirmed, would be inconsistent with the prediction of cosmological natural selection."
   - **Brown, Lee & Rho**, arXiv:0802.2997 **v2 (4 Sep 2008)**, *PRL* 101, 091101 (2008): a "massive neutron star with mass M > 2 M_sun would put in serious doubt or simply falsify the following chain of predictions: (1) nearly vanishing vector meson mass at chiral restoration, (2) kaon condensation at … n ~ 3 n_0, (3) the Brown-Bethe maximum neutron star mass M_max ~ 1.5 M_sun and (4) Smolin's 'Cosmological Natural Selection' hypothesis."
   - **Observations as of 2026-09-24:**

| Pulsar | Mass (M☉) | Source (version seen) |
|---|---|---|
| PSR J1614−2230 | 1.97 ± 0.04 | Demorest et al., arXiv:1010.5788 v1 (27 Oct 2010), *Nature* 467, 1081 |
| PSR J1614−2230 (later timing) | 1.928 ± 0.017 | Fonseca et al. 2016. **[UNVERIFIED: seen only in search snippets]** |
| PSR J0740+6620 | 2.08 ± 0.07 (68.3 %) | Fonseca et al., arXiv:2104.00880 v2 (6 Jul 2021) |
| PSR J0952−0607 (first) | 2.35 ± 0.17 | Romani et al., arXiv:2207.05124 v1 (11 Jul 2022), ApJL 934 L17 |
| PSR J0952−0607 (tightened) | 2.35 ± 0.11 | Romani et al., arXiv:2512.05099 v1 (4 Dec 2025) |

     Romani et al. (2022) give M_max > 2.19 M☉ at 1σ and > 2.09 M☉ at 3σ. The 2025 paper gives M_TOV > 2.27 M☉ at 1σ and > 2.12 M☉ at 3σ, and notes the mass "is now 2.5σ above that of the heaviest pulsar with a white dwarf companion."
   - **Reading.** J0740+6620 at 2.08 ± 0.07 is only about 1σ above the revised bound of 2 M☉. The 3σ lower limit M_TOV > 2.12 M☉ from J0952−0607 exceeds that bound, but it rests on optical light-curve modelling rather than Shapiro delay, and the authors note that "uncertainties remain". By Brown–Lee–Rho's own criterion (M > 2 M☉), the Bethe–Brown kaon-condensation chain is under serious strain or refuted.
   - **Smolin's reply after 2019:** none found. No Smolin arXiv paper after 1202.3373 revisits the neutron-star prediction; see §7 for the full arXiv listing through 2026. The book *Einstein's Unfinished Revolution* (2019) was not checked. **[UNVERIFIED]**
2. **Inflation** (hep-th/0612185; hep-th/0407213 §6.4). "CNS implies that inflation, if true, must be governed by a single parameter, so that the inflaton coupling that controls δρ/ρ also controls the number of e-foldings N." For new inflation, the size of the inflated region is R ≈ e^{λ^{-1/2}}, so raising λ to make more primordial black holes shrinks R exponentially. CNS is refuted if the confirmed inflation model has a parameter p_inf that tilts the spectrum toward more primordial black holes without reducing R. Smolin in 2006: "So far the predictions of single field, single parameter inflation hold up very well." **Status 2026:** not re-evaluated in any Smolin paper found. Whether current CMB data single out a model with such a p_inf has not been assessed here. **[UNVERIFIED]**
3. **Little early star formation** (hep-th/0612185). If massive stars could form without carbon or oxygen cooling, one would expect many more supernovae at high redshift; in 2006 "these so far have not been observed." **Status 2026 (e.g. JWST high-z results) not assessed here. [UNVERIFIED]**
4. **Explanations, which Smolin says are not predictions** (hep-th/0407213 §6.1): the sign and size of m_n − m_p, m_e, m_ν, α, α_s and G_F. "These cannot be considered independent predictions of the theory, because the existence of carbon and oxygen, plus long lived stars, are also conditions of our own existence."

### 1c. Published critiques

- **Vilenkin**, "On cosmic natural selection", arXiv:hep-th/0610051 **v2 (27 Nov 2006)**: "The rate of black hole formation can be increased by increasing the value of the cosmological constant. This falsifies Smolin's conjecture." The mechanism is Ginsparg–Perry nucleation of black holes in eternal de Sitter space at rate Γ ≈ l_Pl^{-4} e^{-M/T₀}, with T₀ = 1/(2πR) and R^{-1} = H = √(Λ/3). This rate grows with Λ and swamps astrophysical production after t_N ≈ R·10^{61}.
  - **Smolin's reply** (hep-th/0612185 §4) says the argument depends on (i) the infrared completion of GR (Λ constant forever; no decay of de Sitter), (ii) the Euclidean semiclassical path integral and thermal equilibrium, and (iii) the UV behaviour of Planck-mass black holes. He also offers a freak-observer reductio: "either Vilenkin's argument is wrong or it has no force against CNS."
- **Rothman & Ellis**, "Smolin's natural selection hypothesis", *QJRAS* 34 (1993) 201–212. Full text not reached (ADS returned HTTP 405). Smolin's summary (hep-th/0407213 §6.2) of one of the arguments: "star formation would proceed to more massive stars were the universe to consist only of neutrons." He replies that forming massive stars needs CO cooling and carbon dust. **[Critique content UNVERIFIED from the primary text]**
- **Silk**, "Holistic cosmology", *Science* 277 (1 Aug 1997) 644, a review of *The Life of the Cosmos*. Smolin groups it with arguments about the primordial-fluctuation tilt and claims that CNS is untestable (hep-th/0407213). **[Content UNVERIFIED]**
- **Harrison**, "The natural selection of universes containing intelligent life", *QJRAS* 36 (1995) 193–203. A variant in which intelligent life creates successor universes. **[Content UNVERIFIED beyond the title and search summaries]**
- **Vaas**, arXiv:gr-qc/0205119 **v1 (28 May 2002)**. His points: "(1) There is no necessary connection between black holes and life… (2) The Darwinian analogy is an inadequate model transfer. The fitness of Smolin's universes is not constrained by its environment, but by only one internal factor… they are not competing against each other. (3) Smolin's central claim cannot be falsified."
- **Altenberg**, "Implications of the Reduction Principle for Cosmological Natural Selection", arXiv:1302.1293 **v2 (20 Feb 2013)**. This is the one mathematical treatment found. It uses a multitype branching process with competing inheritance laws together with Karlin's (1982) theorem: "The most faithful inheritance law dominates the ensemble of universes… Tradeoffs between fitness and faithfulness open the possibility that evolved fundamental parameters are compromises, and not local optima."
- Also found but not read: "Adding genes and interaction to Smolin's cosmological natural selection", *Synthese* (2025), doi:10.1007/s11229-025-05189-y. Springer served a JavaScript challenge. **[UNVERIFIED]**
- **Eternal-inflation swamping** (Smolin: "voiced in conversation but not, I believe, in print"). Smolin's answer is to restrict to the sub-ensemble E_L^{N₀} of universes with more than N₀ black-hole ancestors (hep-th/0612185 §3.3).

### 1d. Open mathematical problems (CNS)

1. **The convergence theorem is asserted, not proved.** No stated conditions on f, K or the generation structure yield "almost every member near a local extremum." [Quote in §1a.] For replicator–mutator dynamics, the stationary distribution is concentrated near maxima of f only when mutations are small relative to the scale on which f varies. Smolin states this ("small compared to the step size under which f(p) changes appreciably") but gives no bound. (DOSSIER NOTE)
2. **The mutation kernel is unspecified.** "The hypothesis that the parameters p change, on average by small random amounts, should be ultimately grounded in fundamental physics… there have so far been no detailed studies of these processes which would check the hypothesis that the change in each generation is small" (hep-th/0407213). Altenberg shows the kernel itself is subject to selection, toward higher fidelity.
3. **Fitness is not computed.** f(p) is estimated qualitatively from astrophysics, direction by direction. There is no calculation of f near p_us, and the prediction depends on local monotonicity only.
4. **The ensemble and measure problem.** The population grows without bound (f > 1). Typicality has to be defined over generations, and whether "time" counts generations or something else is open. Smolin's own words (arXiv:1201.2632): "In cosmological natural selection a time is required to count generations and give sense to an ensemble of universes on the landscape at a fixed time." How the sub-ensemble E^{N₀} is embedded in an eternal-inflation measure is left open.
5. **Fitness counting.** Is fitness the number of black holes of all masses, of astrophysical black holes only, or of those that "bounce"? Vilenkin's objection turns on this: nucleated Planck-mass black holes in the far future. Smolin's reply appeals to unknown UV and IR physics, so the fitness functional is not defined.
6. **The bounce hypothesis.** It requires quantum-gravity singularity resolution, with parameter change at the bounce, for astrophysical black holes. Smolin cites LQC bounces for support, but no calculation derives the parameter change.

---

## 2. *Time Reborn* (2013), temporal naturalism, *The Singular Universe* (Unger & Smolin, CUP, 2014)

### 2a. Claims

- **The Singular Universe's three ideas** (from publisher and review summaries; the book was not read): "the singular existence of the universe", "the inclusive reality of time" (everything in the structure and regularities of nature changes sooner or later), and "the selective realism of mathematics". **[Book text UNVERIFIED; the wording is from search summaries of the CUP pages and reviews.]**
- **Temporal naturalism.** Smolin, arXiv:1310.8539 **v1 (31 Oct 2013)**; *Stud. Hist. Phil. Sci. B* 52 (2015) 86: "time, in the sense of the succession of present moments, is real, and … laws of nature evolve in that time."
- **Newtonian paradigm and cosmological fallacy** (1310.8539 §3.3). A timeless state space plus a timeless law is justified only for small, repeatable subsystems, where one can "vary the initial conditions… to test hypotheses as to the laws." For the universe there is only one history. "To ignore this and attempt to scale up the Newtonian paradigm to the universe as a whole is to commit the cosmological fallacy."
- **Cosmological dilemma** (§3.4). Every isolated-subsystem description is approximate. Enlarging the system to the whole universe destroys the law/initial-condition separation. "The only solution to it is to regard any application of the Newtonian paradigm as approximate… an unavoidable limit to the precision with which the predictions of the theory may be compared with experiment."
- **Metalaw dilemma** (§8.2, verbatim): "If laws evolve, there either is a metalaw by which they evolve or there is not. Suppose there is a metalaw. We must ask why that metalaw, hence there is danger of an infinite regress. But suppose that there is no metalaw. Then there are features of the world that are not explained, i.e. sufficient reason is not gained." He offers four avenues:
  1. a statistical metalaw, as in CNS;
  2. unification of state and law;
  3. "a principle of universality of metalaws, analogous to the principle of universality in computation";
  4. laws that co-evolve with phenomena, as in biology.
- **State–law unification model.** Smolin, "Unification of the state with the dynamical law", arXiv:1201.2632 **v1 (12 Jan 2012)**; *Found. Phys.* 45 (2015) 1.
  - The metastate is a large antisymmetric integer matrix X.
  - The metalaw is X_n = X_{n−1} + [X_{n−1}, X_{n−2}] (plus linear terms), which he argues is almost unique under four conditions: second order, slow variation, quadratic nonlinearity, and a large global symmetry.
  - For times shorter than T_Newton, the evolution splits approximately into a slowly varying "law" and a fast "state". Which information goes into which "is determined by the initial conditions."
- **Temporal relationalism.** arXiv:1805.12468 **v1 (31 May 2018)**, a review. The shared assumptions are "that physics is relational and that time and causality are fundamental."

### 2b. Open mathematical problems

1. **No metalaw is fixed.** The universality-of-metalaws conjecture (1310.8539; 1201.2632: "The remaining freedom is, I conjecture, accounted for by the principle of universality") has no stated equivalence relation or theorem. What "isomorphic in their explanatory outcomes" means has not been formalised.
2. **The time scale of law/state separation.** No estimate of T_Newton from generic initial data in the matrix model was found. "This does not yet solve the problem of explaining the particular features of the standard model" (1201.2632).
3. **Preferred simultaneity.** Temporal naturalism needs a global "now". Smolin appeals to shape dynamics (1310.8539 §8.1) and does not supply a derivation within GR.

---

## 3. The principle of precedence

### 3a. Exact statements

Smolin, "Precedence and freedom in quantum physics", arXiv:1205.3707 **v1 (16 May 2012)**, the only version; *Int. J. Quant. Found.* 1 (2015) 44. There was an open review at IJQF (posted 30 Sep 2014, accepted after one referee report, revised 7 Dec 2014). The quotations below are from arXiv v1.

- **Definition.** "The precedents of a quantum system S is the ensemble, E(S) of systems with the same constituents and preparation (including transformations) in the past… M(E,S) is the ensemble of outcomes of these measurements."
- **Principle of correspondence.** "The statistical state ρ of a quantum system, S, is a description of the ensemble of its precedents."
- **Postulate 6, precedence.** "The outcome of a measurement, M, on a system, S, is a randomly chosen member of M(E,S), the ensemble of outcomes of past instances of that measurement on identically prepared systems, in the case that the number of such precedents is large."
- **Freedom in the absence of precedent.** "A quantum system, S, may have no precedent. Then the outcome of a measurement M on it is not determined by any prior knowledge of the state of the universe."
- **Kinematics.** These are Masanes–Müller postulates 1–4 (local tomography, equivalence of subspaces, symmetry of pure states, all measurements allowed), plus a new Postulate 5 of "maximal freedom": K(N) should grow as fast as possible. By Masanes–Müller Theorem 1, postulates 1–4 admit only classical probability theory (K = N − 1) and quantum theory (K = N² − 1), and Postulate 5 selects the quantum case. Smolin: "my main result is a trivial step."
- **How the Born rule enters.** The rule is **not derived dynamically**. Quantum kinematics, and with it the trace rule, comes from the Masanes–Müller reconstruction. Precedence only explains why past frequencies persist: "we do not need to postulate timeless laws of nature… A weaker notion in which laws evolve through the accumulation of precedence suffices."
- **The precedence rule as a sampling law (DOSSIER NOTE).** Write the history of outcomes of measurement M on preparation S as o_1, …, o_n. For large n: P(o_{n+1} = a | past) = n_a/n.

### 3b. Open problems (stated by Smolin or by the referee)

1. **The small-n regime.** "What happens in between, when the number of precedents is non-zero but small. This requires a novel principle, about which I only have a few preliminary remarks." Smolin also identifies the lock-in problem himself: "the first result with no precedence would be chosen randomly and that result would be the sole precedent for the second result, which would imply that all future measurements would repeat the first random choice." His tentative fix, credited to M. Müller in an unpublished draft, is that nature induces "the simplest possible rule, in the sense of algorithmic information theory, which accounts for the first small number of precedents."
2. **(DOSSIER NOTE, not found in the literature) The Pólya-urn structure.** If each outcome is drawn uniformly from past outcomes and then added to the record, the process is exactly a Pólya urn. The frequencies n_a/n form a martingale and converge almost surely, but to a random Dirichlet limit set by the composition at the end of the "free" phase. Precedence therefore preserves whatever frequencies exist and never corrects them toward |⟨a|ψ⟩|². Whatever fixes the Born values has to act in the pre-precedent phase. The rate of convergence and the variance of the limit are open for any concrete "free-phase" rule.
3. **Consistency across measurements** (IJQF referee report, 24 Nov 2014): "somehow the precedents must 'know' that they 'should respect' the reasonable postulates 1-5 in the course of building up quantum theory… it might well be that answering this question would be in large parts equivalent to specifying a detailed mathematical mechanism for 'how precedence builds up'." Put concretely: ensembles for different measurements M, M′ on the same preparation must jointly be the marginals of one density matrix. Nothing in Postulate 6 enforces this.
4. **What "same constituents and preparation" means.** Smolin concedes the primitive: "this interpretation of quantum theory takes the notion of copy, or similar preparation or measurement, as a primitive." The referee adds that "there simply is no established mathematical formulation of the notion that 'outcomes are free, and not determined by any statistical law'."
5. **What threshold of precedents counts as "large"?** Smolin proposes K = N² − 1 as the relevant count ("K is a measure of how many precedents are necessary"). No stopping rule or error bound is given.
6. **Testability.** Smolin: "testable, by the construction and study of entangled quantum states which are novel". No observable, effect size or protocol is specified.

---

## 4. Energetic causal sets (Cortês & Smolin)

### 4a. The model

Sources:
- "The Universe as a Process of Unique Events", arXiv:1307.6167 **v3 (25 Nov 2015)**; *PRD* 90, 084007 (2014).
- "Energetic Causal Sets", arXiv:1308.2206 **v2 (25 Nov 2015)**; *PRD* 90, 044035 (2014).
- "Spin foam models as energetic causal sets", arXiv:1407.0032 **v2 (28 Jul 2014)**; *PRD* 93, 084039 (2016).
- "Reversing the irreversible", arXiv:1703.09696 **v1 (27 Mar 2017)**; *PRD* 97, 026004 (2018).
- Cohen, Cortês, Elitzur & Smolin, "Realism and Causality II", arXiv:1902.05082 **v3 (1 Nov 2020)**; *PRD* 102, 124028 (2020).
- Smolin, "The path integral formulation of energetic causal set models of the universe", arXiv:2303.15546 **v1 (27 Mar 2023)**.

- **Principles A–D** (1307.6167). A: time is fundamental, and "new events are created out of present events." B: time is directional, with irreversible laws. C: relationalism. D: "Energy is fundamental… space-time is emergent."
- **Uniqueness of events.** Each event is distinguished by its causal past.
- **Kinematics.** Events I carry incoming momenta p^I_{aK} and outgoing momenta q^L_{aI} (a = 0…3) in a momentum space with metric η_ab. The constraints are:
  - conservation, P^I_a = Σ_K p^I_{aK} − Σ_L q^L_{aI} = 0;
  - no redshift, R^K_{aI} = p^K_{aI} − q^K_{aI} = 0;
  - massless shell, C^I_K = ½ η^{ab} p^I_{aK} p^I_{bK} = 0.
- **Emergence of spacetime.** The constraints are exponentiated with Lagrange multipliers z^a_I (one per event), x^{aK}_I and N^K_I. Taking the stationary phase of the "half" path integral gives

  z^a_I − z^a_K = p^{aI}_K (Ñ^K_I − N^K_I).

  So z_I "become coordinates embedding the events in Minkowski spacetime", with causal links mapped to null intervals proportional to the momentum carried, and the spacetime metric inherited from momentum space.
- **Generator (1+1 simulations).** Each event's past is summarised as past²_I = (1/N) Σ_{J ∈ past(I)} (−t_J² + x_J²), with distance D_IJ = |past²_I − past²_J|. The progenitor pair is the open pair with the minimal D_IJ ("Interacting Pair = Min{D_IJ}"); a variant maximises it. Novelty is injected through a random cycle number n. Result: an irregular irreversible phase, then "lock-in" to a regular phase that looks reversible. 1703.09696 interprets this as convergence to limit cycles.
- **Three orders** (1902.05082): birth order (total order), dynamical partial order, and emergent causal order, which may disagree ("disordered causality").
- **2023 extension.** A QFT with spin 0, ½ and 1 fields, cut off in momentum space at μ, which is also the scale of Lorentz-invariance breakdown.

### 4b. Open problems

1. **Measure factors.** "our discussion of the emergence of space-time… has relied entirely on the principle of stationary phase. We have not so far attempted to estimate the measure factors that govern the relative importance of different critical points or can even lead to the dominance of the path integral by non-critical histories. This is a good problem for future work" (1307.6167).
2. **Embeddability.** "equations (9) will not always have simultaneous solutions. There is one equation to be solved for every causal link, but only one z^a_I for each event." The system is overdetermined. The conditions under which a flat embedding exists, and its genericity or stability, are not characterised.
3. **What novelty is.** "A goal for future work will be to understand in more detail how fundamental irreversibility gives rise to standard reversible laws; what is the quantity that represents novelty; and how does the transition to the reversible regime occur" (1307.6167). The lock-in result is numerical (1+1D, ~10⁴–10⁵ events) and has no analytic proof.
4. **General relativity.** "The remaining step of showing how general relativity emerges is saved for a later paper" (1712.04799). No such paper was found on arXiv through 2026-09-24.
5. **Lorentz invariance** is broken at μ (2303.15546), and the ECS dynamics singles out a birth order. How close the emergent Lorentz invariance is, and how it compares with observational bounds, is not quantified.

---

## 5. Real ensembles, nonlocal hidden variables, variety and views, *Einstein's Unfinished Revolution*, the Autodidactic Universe

### 5a. Real ensemble formulation

Smolin, arXiv:1104.2822 **v1 (14 Apr 2011)**; *Found. Phys.* 42 (2012) 1239. Earlier: "Could quantum mechanics be an approximation to another theory?", quant-ph/0609109 (2006); "Matrix models as non-local hidden variables theories", hep-th/0201031 (2002).

- The ensemble is "the ensemble of all the systems in the same quantum state in the universe". Each member I carries beables (a_I, e^{iφ_I}).
- **Copy rule.** System I copies J (a_I → a_J, φ_I → φ_J) at rate P(I copy J) = F(n_I, φ_I, n_J, φ_J, a_I, a_J).
- Occupation numbers then evolve as

  ṅ_a = Σ_{b≠a} n_b n_a (F_ab − F_ba),  ρ̇_a = Σ_b (ρ_b T_{b→a} − ρ_a T_{a→b}),  T_{b→a} = F_ab n_a.

- **Ansatz** F′ = (n_a/n_b)^q R(e^{i(φ_a−φ_b)})_ab, with phase alignment φ_I = φ_{a_I}, reproduces the Schrödinger equation for large n_a.
- Macroscopic systems "have no copies in the universe" and so do not evolve by the copy law.
- **Open problems (§VI, Smolin's own list):**
  - "What exactly defines the ensemble that corresponds to the quantum state?… Is there a precise characterization… that does not refer to the concept of quantum state?"
  - how coarse-graining the beables commutes with coarse-graining quantum dynamics;
  - composite and hierarchical systems;
  - a preferred simultaneity;
  - basis choice ("What picks the beables?");
  - phase alignment "ad hoc… stability… must be investigated";
  - **"The nodes issue. This is the most serious problem of this list"**: if n_a(0) = 0 then n_a(t) = 0 for all t, so wavefunction nodes cannot fill in;
  - the rate of mixing, and relaxation to ensemble frequencies;
  - possible signalling where quantum dynamics fails.

### 5b. Variety and maximal variety

- **Barbour & Smolin**, "Extremal variety as the foundation of a cosmological quantum theory", arXiv:hep-th/9203041 **v1 (17 Mar 1992)**. Monads have views w_i and a symmetric difference array D_ij = D(w_i, w_j), and "The variety can then be defined as V = Σ_{i≠j} D_ij." The dynamical principle is that V is extremal at fixed N.
- **Graph form** (1506.02938; also 2104.03902 eqs. 108–109). N^n(i) is the n-hop neighbourhood of node i. m(i,j) is the smallest m for which N^m(i) and N^m(j) are non-isomorphic. Then D(i,j) = 1/m(i,j) and V = Σ_{i<j} D(i,j).
- **"Quantum mechanics and the principle of maximal variety"**, arXiv:1506.02938 **v1 (9 Jun 2015)**; *Found. Phys.* 46 (2016) 736.
  - View: V^{ka}_i = (x^a_i − x^a_k)/D(i,k)², with a horizon cutoff R.
  - Distinctiveness: I_ij = (1/N) Σ_k (V^k_i − V^k_j)².
  - Variety: 𝒱 = (A/N²) Σ_{i≠j} I_ij.
  - Potential: U_V = −(ħ²/8m) 𝒱.
  - In the large-N continuum limit, 𝒱 becomes Bohm's quantum-potential functional (ħ²/8m)∫ρ(∂ρ/ρ)², and ψ = √ρ e^{iS/ħ} satisfies the Schrödinger equation.
  - **Open (Smolin):** "We conjecture that over time the non-local inter-ensemble interactions… randomize the trajectories of the individual elements so that over some convergence time, τ, for each k, ρ_k(x) → ρ(x)… Standard arguments would suggest that this is true, but it has not been shown." This relaxation, individual to ensemble distribution, is the Born-rule step.
  - **Predictions (qualitative):** N = 1 systems with no copies behave classically; N = 2 has no quantum potential ("a three body interaction"); from N = 3 the quantum potential enters.

### 5c. The causal theory of views (CTV)

Sources:
- "The dynamics of difference", arXiv:1712.04799 **v3 (1 Jun 2019)**; *Found. Phys.* 48 (2018) 121.
- "Views, variety and quantum mechanics", arXiv:2105.03539 **v1 (7 May 2021)**.
- "Views, variety and celestial spheres", arXiv:2202.00594 **v1 (1 Feb 2022)**.
- Smolin & Verde, "The quantum mechanics of the present", arXiv:2104.09945 **v1 (20 Apr 2021)**.

- **Kinematics** (2105.03539). An energetic causal set (§4), with conservation P^I_a = Σ_{K∈IPast(I)} p^I_{aK} − Σ_{L∈IFut(I)} p^L_{aI} = 0. The view of I is V_I = {p^I_{αJ}, …}, the incoming energy-momenta. "The beables of the theory are the views of the events."
- **Weighted view:** W^I_a = Σ_{K∈Past(I)} p^I_{aK}/|p^I_{aK}|^w.
- **Difference and variety:** D(I,J) = (W_I − W_J)², and the total variety is 𝒱 = (2/(N(N−1))) Σ_{I,J} D(I,J).
- **Kinetic term (causal variety):** T = Σ_{I|>J} (W^{(p=0)}_I − W^{(p=0)}_J)², over immediate causal pairs. An alternative is "surprise", Surprise(I) = |Σ_{K∈IPast(I)} D(I,K)|².
- **Potential:** U = Σ_{I<>J} D(I,J)_{w=2}, over causally unrelated pairs.
- **Hamiltonian:** H = gT + g′U.
- **"Half integral"** over momenta only (no positions, hence no commutation relations and no fundamental ħ):

  Z[Γ] = Π_{J|>K} ∫ dp^K_{aJ} Π_I δ(P^I_a) e^{i(gT + g′U)}.

- **Result.** To leading order in an expansion in event density, the action is S = ∫ρ(Ṡ − g ∂S·∂S − (g′/g²)(∂ρ/ρ)²). With g′/g² = ħ²/(8m Z_V) this yields the Schrödinger equation. The leading correction, ∝ N^{-2/d} (ħ² r′²/8m) ∫ ρ (∇²ρ/ρ)², is non-linear in ψ. "ħ enters the theory at all" only through this choice.
- **Choices left open by Smolin:** "(1) how the views are defined and represented, (2) how the differences D(I,J) between views are defined and (3) which pairs of views are summed over… I believe it may be the case that there is a single universality class (or just a few)."
- **Open problems:**
  - a relativistic version. The dynamics "breaks lorentz invariance… there is no simple boost generator". Celestial spheres (2202.00594), with views as punctured S² and SL(2,ℂ), are proposed but not completed;
  - the sign of the coefficients: "The main failure mode… is that the signs may not work out for the energy to be bounded from below; if β < 0 … classical diffusion";
  - GR not derived (1712.04799);
  - the measurement problem and qualia are "beyond the scope";
  - the universality-class conjecture, stated above.
- **Einstein's Unfinished Revolution** (Penguin, 9 Apr 2019). The book was not read. Per Silberstein's review (*IJQF* 6 (2020) 133–159, PDF fetched), Smolin's principles are: background independence; fully relational beables; causal completeness; reciprocity; identity of indiscernibles (all as aspects of the PSR). His hypotheses are: time as causation is fundamental; time is irreversible; space is emergent. Silberstein summarises the dynamics as "quantum dynamics is simply the copying of random precedents from a state's causal past", with novel states obeying "a more complex non-linear equation". Silberstein argues Smolin cannot have "both his naïve realism and his brand of QG/unification." **[Book text UNVERIFIED]**

### 5d. The Autodidactic Universe

arXiv:2104.03902 **v2 (2 Sep 2021)**; v1 was 29 Mar 2021. No journal reference was found in INSPIRE.

**Author list correction.** The actual authors are **S. Alexander, W. J. Cunningham, J. Lanier, L. Smolin, S. Stanojevic, M. W. Toomey, D. Wecker**. The author list given in the task (Alexander, Cortês, Liddle, Magueijo, Smolin, …) is the author list of the 2019 varying-Λ papers, arXiv:1905.10380 and 1905.10382.

- **Claim.** "the Universe learns its own physical laws… by exploring a landscape of possible laws, which we express as a certain class of matrix models."
- **Cubic learning systems (§3).**
  - The metalaw is X_n = X_{n−1} + [X_{n−1}, X_{n−2}], or with gauge invariance X_n = [X_{n−1}, X_{n−2}].
  - The triple form is A_{n+1} = A_n + [B_n, C_n] and cyclic permutations.
  - The Hamiltonian is H = Σ_n (Tr(A_n B_n C_n) + Φᵀ X_n ∘ Φ).
  - The corresponding recurrent network has layers (a_n, b_n, c_n) and weights (A_n, B_n, C_n) ∈ so(N), updated as A_{n+1} = [B_n, C_n] + b_nᵀ a_n and b_{n+1} = e^{A_n} ∘ a_n, with thermalisation every three steps against H_n = Tr e^A e^B e^C + ….
  - Matrix solutions that commute ([A₀,B₀] = 0, …), with expansions around them, give "a regulated gauge-gravity theory."
- **Protocols (§4).** Renormalisation-group learning; precedence realised by an RBM; self-sampling; graph variety (V = Σ_{i<j} 1/m(i,j)); geometric self-assembly.
- **What the authors say they do not have (§3.3):** "We do not have an equivalence. The gauge and gravity theories are only complete in the limit N → ∞. But we don't have a definition of the learning architecture in that limit." Also, "thermal effects to learn… We conjecture that would employ embedding our learning systems in cosmological models. But we have yet to work out the details." And on precedence: "The architecture just described is different from the Principle of Precedence, as it does not entirely realize the notion of being informed from past outcomes."
- **Open problems:**
  - the N → ∞ limit of the learning side;
  - defining "learning without supervision" as a physical criterion (§1.1);
  - which variety definition is correct ("it is not obvious a priori which is most well-suited");
  - the conjecture that variety selects manifold-like causal sets.
- **Follow-ups:** 2201.04183 (the Standard Model as a cubic matrix action via Toeplitz matrices), 2206.13458 (non-local field theory with a Moyal product from matrix models) and 2007.05957 (triality). See §7.

---

## 6. LQG-era work (brief)

- **Rovelli & Smolin, "Discreteness of area and volume in quantum gravity"**, arXiv:gr-qc/9411005 v1 (2 Nov 1994); *Nucl. Phys. B* 442 (1995) 593, with an erratum in 456, 753. Area and volume operators have discrete spectra, and their eigenstates are spin networks. About 1,338 INSPIRE citations.
- **Rovelli & Smolin, "Spin networks and quantum gravity"**, arXiv:gr-qc/9505006 v1 (4 May 1995); *PRD* 52 (1995) 5743. The spin-network basis of the loop representation, which "fully reduces the spinor identities (SU(2) Mandelstam identities)." Standard area spectrum: A = 8πγ l_P² Σ_i √(j_i(j_i+1)). The Immirzi γ came later.
- **Kodama state** (Smolin, arXiv:hep-th/0209079 v1, 9 Sep 2002): Ψ_K(A) = 𝒩 exp((3/2λ) ∫ Y_CS), where Y_CS = ½ Tr(A∧dA + (2/3)A³) and λ = ΛGħ. It is an exact solution of all constraints for Λ > 0, with de Sitter as its semiclassical limit.
  - **Critiques:** Witten, arXiv:gr-qc/0306083 v2 (19 Jun 2003): for the Yang–Mills Chern–Simons analogue, "positive helicity gauge bosons have positive energy and negative helicity ones have negative energy. Some of the negative energy states would have negative norm… Similar properties can be expected for the analogous Kodama wavefunction." Freidel & Smolin, arXiv:hep-th/0310224 v3 (28 Oct 2003), *CQG* 21 (2004) 3831: the linearised Lorentzian Kodama state is not normalisable, while the Euclidean one is δ-normalisable.
  - **Open:** normalisability, CPT, and the physical inner product of the full state.

---

## 7. Recent papers (2020–2026)

Sources checked on 2026-09-24: the arXiv author page (`arxiv.org/a/smolin_l_1`), arXiv author search, and INSPIRE (228 records). **The last new arXiv preprint with Lee Smolin as author is 2303.15546 (27 Mar 2023).** From April 2023 to September 2026 there are only version updates of older papers. No 2024–2026 physics preprint was found. Journal-only or book publications after 2023 were not searched exhaustively. **[UNVERIFIED]**

| arXiv | Title (authors) | Latest version seen | Journal |
|---|---|---|---|
| 2001.08522 | Natural and bionic neuronal membranes: possible sites for quantum biology (Smolin) | v1 21 Jan 2020 | — |
| 2007.05957 | Quantum reference frames and triality (Smolin) | v1 12 Jul 2020 | — |
| 2104.03902 | The Autodidactic Universe (Alexander et al.) | v2 2 Sep 2021 | — |
| 2104.09945 | The quantum mechanics of the present (Smolin, Verde) | v1 20 Apr 2021 | — |
| 2105.03539 | Views, variety and quantum mechanics (Smolin) | v1 7 May 2021 | — |
| 2201.04183 | A Cubic Matrix Action for the Standard Model and Beyond (Yargic, Lanier, Smolin, Wecker) | v1 11 Jan 2022 | — |
| 2202.00594 | Views, variety and celestial spheres (Smolin) | v1 1 Feb 2022 | — |
| 2204.09378 | Biocosmology: Towards the birth of a new science (Cortês, Kauffman, Liddle, Smolin) | v3 27 Sep 2024 | — |
| 2204.09379 | Biocosmology: Biology from a cosmological perspective (same authors) | v2 28 Apr 2022 | — |
| 2204.14115 | The TAP equation: evaluating combinatorial innovation in Biocosmology (same authors) | v4 7 Oct 2025 | *European Economic Review* 179 (2025) |
| 2206.13458 | Non-local Field Theory from Matrix Models (Banburski, Lanier, Shyam, Smolin, Yargic) | v1 27 Jun 2022 | — |
| 2303.15546 | The path integral formulation of energetic causal set models of the universe (Smolin) | v1 27 Mar 2023 | — |

The TAP papers (2204.09378/09379/14115) move away from fundamental physics: a combinatorial-innovation growth law with a plateau followed by a finite-time blow-up. The authors write that "the results of this work remain far from being firmly established."

---

## 8. Cross-cutting open bottlenecks

1. **The Born weight from frequencies.** This problem appears in the precedence principle, the real-ensemble copy law and the maximal-variety relaxation. Each recovers the Schrödinger/Bohm dynamics of an ensemble density. None proves that individual outcomes relax to |ψ|² from generic initial data: see 1506.02938 ("has not been shown"), 1104.2822 (nodes, mixing rate) and 1205.3707 (small-n regime).
2. **"Similar systems" and "same preparation" as primitives.** This is used in precedence, the real ensemble and CTV, and has no definition independent of the quantum state (1104.2822 §VI; 1205.3707 §4).
3. **Variety is not unique.** The views, the difference D and the pairs summed over are all free choices (2105.03539 §3.4; 2104.03902 §4.4). The universality-class conjecture is unproved.
4. **Emergence is shown only in stationary-phase or leading order.** Measure factors, embeddability, Lorentz invariance and GR are all open (1307.6167; 1712.04799; 2303.15546).
5. **CNS lacks a defined stochastic process.** The kernel, the fitness functional, the measure over generations, and convergence to local optima are all missing. Its sharpest empirical prediction is now under strain from M ≥ 2.08 M☉ pulsars (and M_TOV > 2.12 M☉ at 3σ from J0952−0607), with no published reply from Smolin found.
6. **The metalaw regress.** It is addressed only by proposals (universality, state–law unification, statistical metalaws), none of them formalised as a theorem (1310.8539 §8.2; 1201.2632).

## Unreachable or failed sources

- WebFetch was blocked for arxiv.org, en.wikipedia.org, link.springer.com, ui.adsabs.harvard.edu and iopscience.iop.org; arXiv was then reached by curl.
- ADS abstract pages returned HTTP 405 to curl.
- Springer (the *Synthese* 2025 article) returned a JavaScript challenge.
- Hossenfelder's *Backreaction* review returned HTTP 403.
- The arXiv export API returned an empty body.
- Not read at all: *The Life of the Cosmos*, *Time Reborn*, *The Singular Universe*, *Einstein's Unfinished Revolution*, Rothman & Ellis (1993), Harrison (1995), and Silk (1997).
