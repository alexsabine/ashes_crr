# Carlo Rovelli: research dossier on the physics (mathematics first)

Compiled 2026-09-24. Factual dossier; no CRR content.

**How sources were checked (R10 discipline).** WebFetch to `arxiv.org` was refused by the egress proxy
("EGRESS_BLOCKED"). I fetched each arXiv abstract page (`https://arxiv.org/abs/<id>`) with `curl`
through the session proxy on 2026-09-24, and read the version history off the "Submission history" block.
Where a formula or sentence is quoted from a paper body, I downloaded `https://arxiv.org/pdf/<id>` (latest
version) and extracted the text with `pypdf`. Formulas below are transcribed from that text (PDF extraction can garble
sub/superscripts, so I checked each one against its context). Tags used:
**[verified]** means read in the fetched text today. **[abstract]** means from the abstract page only.
**[standard]** means a textbook-level fact I did not re-derive from a fetched source today.
**[unverified]** means I could not fetch the source. Failed fetches: PhilSci-Archive and cambridge.org
(Swanson's paper) were refused by the proxy; the CORE mirror timed out; `export.arxiv.org` (the API) was refused;
the arXiv author page `arxiv.org/a/rovelli_c_1` returned an empty shell. The listing of Rovelli's papers since 2020
came from the arXiv search page (`arxiv.org/search/?searchtype=author&query=Rovelli, Carlo`).

---

## 1. Relational quantum mechanics (RQM)

### 1(a) Claims and formulas

**Rovelli 1996** (quant-ph/9609002) [verified]. The thesis: the measurement problem comes from the "notion of
observer-independent state of a system". The paper's framework:
- *Hypothesis 1 (all systems are equivalent):* "If the observer O can give a quantum description of the system S,
  then it is also legitimate for an observer P to give a quantum description of the system formed by the observer O."
- *Hypothesis 2 (completeness):* quantum mechanics as it stands is a complete description.
- *Postulate 1 (limited information):* "There is a maximum amount of relevant information that can be extracted from a
  system." For a system with Hilbert space dimension k, N is the smallest integer with N ≥ log₂k bits. Planck's
  constant is read as "the transformation coefficient between physical units (position × momentum) and information
  theoretical units (bits)".
- *Postulate 2 (unlimited information):* "It is always possible to acquire new information about a system."
- *Postulate 3 (superposition principle):* for two complete families of questions c and b, p(Q_c^(i), Q_b^(j)) =
  |U_cb^{ij}|², with unitary U_cb chosen so that U_cd = U_cb U_bd.
- Core statement: states are "values of physical quantities relative to other systems". A quantum description of S
  exists only relative to some system O that has interacted with S.

**The later "facts" formulation** (2109.09170, Oxford Handbook chapter) [abstract]: "RQM's technical core is the
realisation that quantum transition amplitudes determine physical probabilities only when their arguments are facts
relative to the same system." Schematically, P(b|a) = |⟨b|U|a⟩|² is licensed only when a and b are facts relative to
the same system. The "relativity of facts can be neglected in the approximation where decoherence hides interference".
Di Biagio & Rovelli 2020 (2006.15543) [abstract] add the distinction between *stable facts* and *relative facts*.

**Six-postulate reconstruction** used by Adlam & Rovelli 2022 (2203.13342) [verified]: (1) relative facts; (2) no
hidden variables (unitary QM is complete); (3) relations are intrinsic; (4) "Relativity of comparisons: it is
meaningless to compare the accounts relative to any two systems except by invoking a third system relative to which
the comparison is made"; (5) measurement as unitary entanglement relative to a third system W; (6) internally
consistent descriptions (W checking F's pointer agrees with W's own measurement of S).

**Cross-perspective links (CPL)** replace postulate 4. Definition 4.1 (verbatim): "In a scenario where some observer
Alice measures a variable V of a system S, then provided that Alice does not undergo any interactions which destroy
the information about V stored in Alice's physical variables, if Bob subsequently measures the physical variable
representing Alice's information about the variable V, then Bob's measurement result will match Alice's measurement
result." The price, stated in the abstract, is that the ontology "postulates a set of quantum events which are not
strictly relational".

**Di Biagio & Rovelli 2025** (2510.11349) [abstract]: relative facts are defined from "quantifiable notions of
information", "with no addition to orthodox quantum theory". Perspectives are attached to "commutative observables
rather than entire quantum systems", and measurement is shown to be "a continuous process".

### 1(b) Main critiques and open mathematical problems

1. **Which basis does a relative fact pick (the preferred-basis problem)?** Brukner 2021 (2107.03513) [verified]. With
   |ψ⟩_SO = (|↑↑⟩+|↓↓⟩)/√2 = (|→→⟩+|←←⟩)/√2, "RQM does not seem to give any prescription on how to resolve this
   ambiguity." Two assumptions are shown jointly inconsistent. DEFRS: any decomposition |ψ⟩_SO = Σ c_i|x_i⟩_S|X_i⟩_O
   makes the |X_i⟩ states of knowledge. DISRS: distinct relative states map to orthogonal observer states.
   *Concrete problem:* give a rule, internal to unitary QM, that selects the decomposition relative to which O holds
   a fact.
2. **Five no-go theorems** (Pienaar 2021, 2107.00670) [verified, conclusion section]. RQM:4 (comparisons are relative)
   conflicts with RQM:6 (shared facts) through a "loose frame loophole". Even with RQM:6 there can be disagreement
   "about which basis the measurement was performed in". Triplet Bell states "sustain perfect correlations in mutually
   incompatible bases" and so conflict with RQM:3 and RQM:5. His verdict: "it is not clear that RQM represents an
   internally coherent ontology for quantum theory."
3. **Relative facts against the Born rule** (Lawrence, Markiewicz & Żukowski, Quantum 7, 1015 (2023), 2208.11793)
   [abstract]. They derive "a GHZ-like contradiction showing that relative facts described by these statements are
   incompatible with quantum theory". Their criterion: any outcomes an interpretation introduces "must follow the
   probability distribution specified by the Born rule". Reply: Cavalcanti, Di Biagio & Rovelli 2023 (2305.07343)
   strengthen the argument but argue it "helps clarify how one should not think about a theory of relative facts".
   *Open problem:* there is no agreed joint probability space for facts relative to different systems. RQM denies such
   a space exists, while the critics require one.
4. **The third-person problem** (Laudisa 2017, 1710.07556) [abstract]: "it is far from clear what a relativization of
   states to observers exactly achieves."
5. **Ontology and non-locality** (Muciño, Okon & Sudarsky 2021/22, 2105.13338) [abstract]. RQM "fails to address the
   conceptual problems of standard quantum mechanics"; the claims about information exchange and locality are
   "unwarranted". Reply: Rovelli 2106.03205: the assessment "presupposes assumptions that are precisely those
   questioned".
6. **Iteration regress** (Riedel 2024, SHPS 104, 2403.04069) [abstract]. RQM is committed to an "Unrestricted
   Iteration Principle", "an infinite regress of relativisations", which forces "perspectival facts" rather than
   relations.
7. **Completeness against events** (Adlam 2026, 2604.12094) [abstract]. Collapse occurs when a system meets its own
   reference system, but "the solution requires accepting that quantum mechanics is not a complete description of all
   physical facts". This bears directly on Hypothesis 2 above.
8. **No agreed formal framework.** Lahti & Pellonpää (IJTP 62, 170 (2023), 2207.01380) [abstract]: "We search for a
   possible mathematical formulation of some of the key ideas." A standard, agreed mathematical definition of "a fact
   relative to S" (when it occurs, and in which basis) is still not settled across the literature.

Status: SEP entry "Relational Quantum Mechanics", first published 4 Feb 2002, substantive revision 4 Feb 2025,
copyright line "Carlo Rovelli" [verified from page HTML].

### 1(c) Citations (arXiv id, versions as fetched 2026-09-24)
- Rovelli, *Relational Quantum Mechanics*, quant-ph/9609002 v2 (24 Feb 1997; v1 31 Aug 1996); IJTP 35 (1996) 1637.
- Rovelli, *The Relational Interpretation of Quantum Physics*, 2109.09170 v3 (30 Sep 2021).
- Di Biagio & Rovelli, *Stable Facts, Relative Facts*, 2006.15543 v3 (28 Feb 2021); Found. Phys. 51, 30 (2021).
- Di Biagio & Rovelli, *RQM is about Facts, not States: reply to Pienaar and Brukner*, 2110.03610 v1 (7 Oct 2021).
- Adlam & Rovelli, *Information is Physical: Cross-Perspective Links in RQM*, 2203.13342 v2 (14 Apr 2022).
- Cavalcanti, Di Biagio & Rovelli, *On the consistency of relative facts*, 2305.07343 v2 (18 May 2023).
- Rovelli, *Can Alice do science and have friends…?*, 2410.20012 v2 (14 Dec 2024).
- Di Biagio & Rovelli, *Relative Information, Relative Facts*, 2510.11349 v2 (9 Feb 2026).
- Covoni & Rovelli, *Tractatus Quanticus*, 2512.06034 v2 (4 Jan 2026).
- Laudisa, *Open Problems in RQM*, 1710.07556 v1 (20 Oct 2017).
- Muciño, Okon & Sudarsky, *Assessing RQM*, 2105.13338 v2 (12 Sep 2022); Rovelli's reply 2106.03205 v1 (6 Jun 2021).
- Pienaar, *A quintet of quandaries*, 2107.00670 v2 (1 Sep 2021).
- Brukner, *Qubits are not observers*, 2107.03513 v1 (7 Jul 2021).
- Lawrence, Markiewicz & Żukowski, 2208.11793 v2 (17 May 2023).
- Riedel, 2403.04069 v2 (23 Mar 2024). Adlam, 2604.12094 v1 (13 Apr 2026). Lahti & Pellonpää, 2207.01380 v2 (20 Sep 2022).

---

## 2. The thermal time hypothesis (TTH)

### 2(a) Exact statement (Connes & Rovelli 1994, gr-qc/9406019) [verified]

Take a von Neumann algebra R with a cyclic and separating vector |Ψ⟩ (the GNS vector of a faithful state ω). Define
S A|Ψ⟩ = A*|Ψ⟩ (eq. 6), with polar decomposition S = J Δ^{1/2} (eq. 7). Tomita–Takesaki gives the modular group

  α_t(A) = Δ^{−it} A Δ^{it}  (eq. 8).

Footnote 3: "The modular group is usually defined with the opposite sign of t. We have reversed the sign convention in
order to make contact with standard physics usage."

**Hypothesis** (verbatim): "The physical time depends on the state. When the system is in a state ω, the physical time
is given by the modular group α_t of ω." In short: "the physical time is the modular flow of the thermal state."

**Gibbs reduction** (eqs. 27–29, 43–44). For ω = N e^{−βH},

  α_t A = e^{iβtH} A e^{−iβtH}, i.e. α_t = γ_{βt}, where γ is the Hamiltonian flow.

So the modular parameter s and the physical time are related by t_phys = β s (ħ = 1), "up to a constant rescaling β
of the unit of time". Temperature is then "the ratio between thermal time and geometrical time, defined only when the
second is meaningful".

**KMS form** (Rovelli, "Forget time", 0903.3832, eqs. 21–26) [verified]: ρ₀[α_t(A)B] = ρ₀[α_{(−t−iβ)}(B)A], and
W_AB(t) = W_BA(−t−iβ). For a generic state, the *thermal Hamiltonian* is H_ρ = −ln ρ (eq. 25) and the thermal flow is
α_{t_ρ}(A) = e^{i t_ρ H_ρ} A e^{−i t_ρ H_ρ} (eq. 26). In the classical version, the thermal time t_ρ is the Hamiltonian
flow of H_ρ = −ln ρ on the constraint surface Σ (eqs. 17–18), with footnote 9: "assume that ρ nowhere vanishes on Σ".

**State-independent part.** By the cocycle Radon–Nikodym theorem, the modular groups of two faithful states are
inner-equivalent. So "all states of a von Neumann algebra determine the same 1-parameter group in Out(R)", which CR
propose as a state-independent notion of time. [verified, §2.1 of CR]

**Local temperature** (Martinetti & Rovelli 2003, gr-qc/0212074) [verified]. If the modular flow is proportional to a
geometric flow with proper time τ, then β = 1/T ≡ −τ/s (eq. 18). Locally, β(s) = −dτ/ds (eq. 19). For a uniformly
accelerated observer of acceleration a with lifetime inside a double cone ("diamond") of half-size L, for a 4D conformal
QFT in the vacuum:

  β(τ) = (2π/(L a²)) (√(1+a²L²) − cosh aτ)  (eq. 54),  β₀ = 2πL/(√(a²L²+1) + 1)  (eq. 55).

As a → ∞, β₀ → 2π/a (the Davis–Unruh value). For an inertial observer (a = 0) with lifetime 𝒯 = 2L:
T_D = 2ħ/(π k_B 𝒯), the "diamond's temperature" [abstract and eq. 55].

**Tolman–Ehrenfest** (Rovelli & Smerlak 2011, 1005.2985) [abstract]: "at equilibrium, temperature is the rate of
thermal time with respect to proper time". **Haggard & Rovelli 2013** (1302.0724) [verified]: τ = (kT/ħ) t counts
distinguishable states transited. On a stationary spacetime with Killing field ξ, dτ = (kT/ħ)|ξ| dt (eq. 19).
Equilibrium means τ₁ = τ₂ (eq. 17), i.e. |ξ|T = const: "the net information flow between two systems must vanish".
**Chirco, Josset & Rovelli 2016** (1503.08725) [abstract]: equilibrium "acquires sense only when the system admits a
suitable split into three weakly interacting components": a clock plus two systems.

### 2(b) Open problems

1. **Which state?** Connes & Rovelli (conclusion): "It is not clear to us, for instance, whether one should consider all
   the states of a general covariant quantum system on the same ground, or whether some kind of maximal entropy
   mechanism able to select among states may make sense physically." *Problem:* find a selection principle for ω. Without
   one, "time" is as arbitrary as the state.
2. **Non-geometric modular flows.** CR: restricting to a region other than a wedge gives a flow that "unlike the Rindler
   case, will not have any obvious geometrical interpretation". The temperature β = −dτ/ds is defined only when the
   modular flow is proportional to a spacetime flow. Martinetti–Rovelli need a *conformally invariant* 4D QFT for this
   in a diamond [verified]. *Problem:* give a physical time and temperature for massive fields or interacting states,
   where the modular flow acts non-locally. [That the flow is non-geometric in the massive case is the standard
   expectation; I did not verify a specific theorem today.]
3. **Faithfulness.** Modular theory needs a faithful (cyclic and separating) state. For type I (finite-dimensional)
   algebras with ω(A) = Tr(ρA), the flow is A ↦ ρ^{it}Aρ^{−it}. This is inner, so the Out(R) flow is trivial, and a pure
   state defines no flow at all. [standard; follows directly from eq. 8 with Δ = ρ ⊗ ρ^{−1}] The state-independent
   Out(R) "time" is non-trivial only for non-type-I algebras (type III for local QFT). *Problem:* what the TTH says
   about finite quantum systems or pure states.
4. **Everything is always in equilibrium.** Every faithful state is KMS with respect to its own modular flow. CR reply
   that this "does not imply that evolution is frozen", because what is measured are perturbations around a thermal
   state. Swanson (*Can Quantum Thermodynamics Save Time?*, Philosophy of Science, 2021) raises, according to its
   published abstract as returned by search: two technical challenges ("the relationship between thermal time and proper
   time and the possibility of implementing the TTH in classical theories") and three conceptual ones ("the flow of time
   in nonequilibrium states and the extent to which the TTH is background independent and gauge invariant").
   **[unverified: PhilSci-Archive and Cambridge refused; I read only the search-engine abstract.]**
5. **Circularity.** Chua 2024, *The Time in Thermal Time* (2407.18948 v1, 11 Jul 2024; J. Gen. Phil. Sci., per search)
   [abstract]: "the thermal time hypothesis requires dynamics — and hence time — to get off the ground". Chua 2026,
   *Physical Coherence and Time's Emergence* (2605.24970 v1, 24 May 2026) applies a "physical coherence" criterion to
   thermal time.
6. **Normalisation conventions.** The constant between modular parameter and proper time depends on sign and 2π
   conventions. CR reverse the usual sign (footnote 3). Martinetti–Rovelli write β = −τ/s. Haggard–Rovelli use
   τ = kTt/ħ with no 2π. Bisognano–Wichmann boosts carry a 2π [standard]. Any quantitative use has to fix one convention.
7. **Statistical mechanics of covariant systems.** "A fully general-covariant formulation of statistical mechanics is
   still lacking" (Chirco, Haggard & Rovelli 2013, 1309.0777, abstract).
8. **Recent formal work.** van Neerven & Portal (JMP 65, 032105 (2024), 2306.13774 v2, 15 Mar 2024) [abstract] show the
   Connes–Rovelli thermal time of the harmonic oscillator is an *unsharp observable* (a POVM). Adjacent work, not about
   the TTH itself: Chandrasekaran, Longo, Penington & Witten (2206.10780 v5, 3 Jul 2023) build a type II₁ algebra for an
   observer in de Sitter. Witten (2308.03663 v3, 24 Sep 2023) proposes "an algebra of operators along an observer's
   worldline as a background-independent algebra". Both use modular-theoretic tools. Whether they bear on the TTH is my
   reading, not their claim. A search result also claimed that "Bamonti et al. (2025)" criticise thermal time. I could not
   locate such a paper; Bamonti & Thébault 2411.00541 (v2, 8 May 2025) is about cosmic time, not the TTH.
   **[unverified]**

### 2(c) Citations
- Connes & Rovelli, gr-qc/9406019 v1 (14 Jun 1994); CQG 11 (1994) 2899.
- Martinetti & Rovelli, gr-qc/0212074 v4 (2 Feb 2004); CQG 20 (2003) 4919.
- Rovelli & Smerlak, 1005.2985 v5 (18 Jan 2011); CQG 28, 075007.
- Haggard & Rovelli, 1302.0724 v1 (4 Feb 2013); PRD 87, 084001.
- Chirco, Haggard & Rovelli, 1309.0777 v1 (3 Sep 2013); PRD 88, 084027.
- Chirco, Josset & Rovelli, 1503.08725 v2 (14 Jun 2016); CQG 33, 045005.
- Rovelli, "Forget time", 0903.3832 v3 (27 Mar 2009).
- Rovelli 1993, *Statistical mechanics of gravity and the thermodynamical origin of time*, CQG 10, 1549. Cited in CR as
  ref. [4]; **not fetched**.

---

## 3. Loop quantum gravity and spin foams

### 3(a) Key equations

**Area spectrum** (Rovelli & Smolin, gr-qc/9411005 v1 (2 Nov 1994) [abstract]; Ashtekar & Lewandowski, gr-qc/9602046 v2
(23 Aug 1996) [abstract]). In the Zakopane lectures (1102.3660 v5, 3 Aug 2011) [verified], the area eigenvalues per link
are a_j = √(j(j+1)) in units L²_loop = 8πγħG (eqs. 37, 41). So

  A = 8πγ ℓ_P² Σ_p √(j_p(j_p+1)), j ∈ ℕ/2,  area gap A_min = 8πγ ℓ_P² √(3/4) = 4√3 πγ ℓ_P².

**Volume.** The spectrum is discrete (Rovelli–Smolin). Ashtekar & Lewandowski (gr-qc/9711031 v1, 10 Nov 1997) [abstract]
find "two natural regularization schemes". The difference "can be attributed directly to the standard quantization
ambiguity": one operator is sensitive to the differential structure at the vertices, the other only to topology (the
Rovelli–Smolin / De Pietri–Rovelli operator).

**Barbero–Immirzi parameter γ.** A^i_a = Γ^i_a + γK^i_a [standard]. All geometric spectra scale with γ. Rovelli &
Vidotto 2024 call it "a free parameter in LQG, akin to the θ_QCD angle" [verified].

**Black-hole entropy.**
- Rovelli 1996 (gr-qc/9603063) [abstract]: entropy ∝ area from counting microstates distinguishable from outside.
- ABCK 1997 (gr-qc/9710007) [abstract]: horizon described by Chern–Simons theory; S = A/4ℓ_P² for "an appropriate
  choice" of γ. The value given was γ_ABCK = ln2/(π√3) (quoted in Domagała–Lewandowski eq. 1) [verified].
- Domagała & Lewandowski 2004 (gr-qc/0407051) [verified]: the earlier counting "contains an error". They obtain
  (ln 2/(4πγℓ_P²)) a ≤ ln N(a) ≤ (ln 3/(4πγℓ_P²)) a, so ln2/π ≤ γ ≤ ln3/π.
- Meissner 2004 (gr-qc/0407052) [verified]: N(a) = C e^{2πγ_M a}, with 1 = Σ_{k≥1} 2 exp(−2πγ_M √(k(k+2)/4)) (eq. 7).
  This gives γ_M = 0.23753295796592… and S = (γ_M/(4γ)) A/ℓ_P².
- SU(2) Chern–Simons treatment (Engle, Noui & Perez, PRL 105, 031302, 0905.3168 v3) [verified]: log correction
  ΔS = −(3/2) log a_H "(instead of ΔS = −1/2 log a_H in the U(1) treatment)". The Immirzi value in this counting is
  γ = 0.274067… (quoted in Agullo et al., 0906.4529 v3, as agreeing with Ghosh & Mitra) [verified].
- Ghosh & Perez 2011 (1107.1320) [abstract]: with a local-observer energy, the results "are in agreement with Hawking's
  semiclassical analysis for all values of the Immirzi parameter".
- *Open:* the value of γ fixed by entropy depends on the counting scheme (0.127 → 0.2375 → 0.2741), or on none at all
  (Ghosh–Perez). No independent determination of γ exists.

**EPRL model** (Engle, Livine, Pereira & Rovelli, 0711.0146 v2 (13 Dec 2007); NPB 799, 136) [abstract; formulas from
the Zakopane lectures, verified]. The map Y_γ: |j; m, n⟩ ↦ |γj, j; (j, m), (j, n)⟩ embeds SU(2) spin networks into
SL(2,ℂ) unitary representations (p, k) = (γj, j) (eqs. 46, 50). The amplitude is Z_C = Σ_{j_f, i_e} ∏_f d_{j_f}
∏_v A_v, with

  A_v(h_l) = ∫_{SL(2,ℂ)} ∏′_n dg_n ∏_l K(h_l, g_{s(l)} g_{t(l)}^{-1}),  K(h, g) = Σ_j ∫_{SU(2)} dk d_j² χ^j(hk) χ^{γj,j}(kg)

(eqs. 56–57). Footnote 12 notes that the alternative p = γ(j+1) and Alexandrov's family of orderings H^r are other
possible choices, i.e. there is an ordering ambiguity.

**Semiclassics.** Barrett, Dowdall, Fairbairn, Gomes & Hellmann (0902.1170 v2, 20 Apr 2009; JMP 50, 112504)
[abstract]: for non-degenerate 4-simplex boundary data, "the asymptotic formula contains the Regge action". The
standard form is A_v ~ N₊e^{iS_R} + N₋e^{−iS_R} with S_R = Σ_f γ j_f Θ_f [standard; the explicit form was not
re-checked today]. The two terms are the "cosine problem". Engle's "proper vertex" (1111.2865 v4, 13 Sep 2013)
[abstract] modifies the vertex "so its asymptotics include only the one term of the form e^{iS_Regge}".

### 3(b) Open bottlenecks

1. **Flatness problem.** Bonzom 2009 (0905.1501 v2) [abstract]: "stationarity with respect to area variations requires
   spacetime geometry to be flat." Hellmann & Kaminski 2013 (1307.1679 v2) [abstract]: "geometric boundary data is
   suppressed unless its interior continuation satisfies certain accidental curvature constraints … most Regge manifolds
   are suppressed". They trace this to "an incorrect twisting of the face amplitude". Responses:
   - Engle & Rovelli 2021 (2111.03166 v1) [verified]: the constraint is "harmless"; it arises "from exchanging the order
     of limits". "For each boundary data there is a discretization for which the amplitude gives the correct result to
     any desired accuracy."
   - Han, Huang, Liu & Qu 2021 (2110.10670 v1; PRD 106, 044005) [abstract]: numerically find curved Regge geometries at
     complex critical points and state that the "long-standing confusion … is resolved".
   - Asante, Dittrich & Haggard 2020 (2004.07013 v2; PRL 125, 231301) [abstract]: effective spin foams "avoid flatness in
     a restricted regime of the parameter space".

   *Concrete problem:* prove, for the EPRL amplitude, that the joint limit (spins j → ∞ with refinement of the
   2-complex) exists in some ordering and reproduces curved Regge or GR dynamics.
2. **Continuum limit and renormalisation.**
   - Dittrich 2014 (1409.1450 v2, 24 Oct 2016) [abstract]: "The construction of a continuum limit for the dynamics of
     loop quantum gravity is unavoidable to complete the theory"; it is "equivalent to obtaining the continuum physical
     Hilbert space".
   - Bahr & Steinhaus 2016 (1605.07649 v2; PRL 117, 141302) [abstract]: in a hypercuboid truncation there are "strong
     indications for a phase transition", and at the fixed point "broken diffeomorphism symmetry is restored". Steinhaus
     review 2020 (2007.01315 v1).
   - Bruno, Colafranceschi, Mele & Rovelli 2026 (2603.16999 v2, 14 Sep 2026; PRD 114, 066005) [abstract]: "understanding
     the continuum limit of the theory remains a central open problem". Their no-go: "sufficiently strong notions of
     convergence necessarily lead to a topological theory". A distributional limit makes the cylinder amplitude "a
     rigging map". *Open:* whether a concrete model (EPRL) meets their weaker convergence assumptions.
3. **Hamiltonian constraint ambiguities and off-shell closure.**
   - Thiemann's QSD (gr-qc/9606089 v1, 1996) [abstract] gives an "anomaly-free" operator.
   - Nicolai, Peeters & Zamaklar (hep-th/0501114 v4, 18 Sep 2005) [abstract] emphasise "off-shell ('strong') closure of
     the constraint algebra" as "a crucial test", and point to "a large number of ambiguities, in particular in the
     formulation of the Hamiltonian constraint".
   - Varadarajan 2022 (2205.10779 v2, 25 Nov 2022) [abstract] claims non-trivial off-shell anomaly freedom for
     **Euclidean** LQG. The Lorentzian case is not covered by that abstract.
   - Lang, Liegener & Thiemann (1711.05685 v2; CQG 35, 245011) [abstract] propose Hamiltonian renormalisation.
   - *Open:* a Lorentzian, anomaly-free, ambiguity-controlled constraint, and its equivalence to the EPRL covariant
     dynamics. EPRL establishes the kinematic Hilbert-space match only ("a bridge").
4. **Recovering GR.** Nicolai et al.: "Developing suitable approximation methods to establish a connection with classical
   gravity … remains a major challenge." Alexandrov & Roche 2010 (1009.4475 v1) [abstract] challenge the treatment of
   "diffeomorphism and local Lorentz symmetries at the quantum level". Perez's Living Review (1205.2019 v1, 9 May 2012)
   [abstract] lists "conceptual and technical issues that remain open in four dimensions".
5. **Cosmological constant.**
   - Han 2011 (1105.2212 v2; PRD 84, 064010) [abstract]: a q-deformed Euclidean EPRL vertex whose "large-j asymptotics …
     gives the Regge action with a cosmological constant".
   - Haggard, Han, Kamiński & Riello (1512.07690 v2, 8 Nov 2017; ATMP 23 (2019) 1067) [abstract]: SL(2,ℂ) Chern–Simons
     theory gives curved 4-simplices with "Both signs of the curvature and associated cosmological constant".
   - Engle & Rovelli 2021 cite this extension [6] as part of "a tentative Lorentzian quantum theory".
   - *Open (my summary; no single quote found):* a full Lorentzian model with Λ whose continuum limit and flatness
     behaviour are controlled.

---

## 4. Black-to-white-hole transition and Planck stars

### 4(a) Claims and formulas

- **Planck stars** (Rovelli & Vidotto, 1401.6562 v4, 8 Feb 2014) [abstract]. Quantum pressure stops collapse at Planck
  *density*, not Planck size. The object at the end of evaporation can be "larger than planckian by a factor
  (m/m_P)^n", with arguments for n = 1/3 and n = 1.
- **Fireworks metric** (Haggard & Rovelli, 1407.0989 v2, 6 Jul 2014; PRD 92, 104020) [verified]. An exact vacuum
  metric exists outside a compact quantum region. Quantum effects "can first appear at a radius r ∼ (7/6)·2m" (eqs. 1,
  21) after an asymptotic time

    τ ∼ m²/ℓ_P (eq. 2); for b = 1, τ = 2k m²/ℓ_P (eq. 22), with k = 27(4b)^{b/2}/(b+6)^{3+b/2},

  and τ ∝ m^{2/b} in general (eq. 20). The total duration condition is τ = −8m ln v₀ > τ_q = 4k m²/ℓ_P (eq. 42; the
  process lasts twice the bounce time), so v₀ < e^{−km/(2ℓ_P)}. This is contrasted with "the Hawking evaporation time,
  which is of order m³".
- **LQG tunnelling amplitude** (Christodoulou, Rovelli, Speziale & Vilensky, 1605.05268 v3, 14 Sep 2016; PRD 94,
  084035) [verified]. The EPRL amplitude W(m, T), with the external bounce time T as a boundary-state parameter. The
  lifetime is defined by ∫₀^τ |W|² dT = (1 − 1/e) ∫₀^∞ |W|² dT (eq. 1), under the assumed exponential decay law
  p(T) = 1 − e^{−T/τ} (eq. 2). The expression is "too complicated for a straightforward numerical evaluation";
  "preliminary tentative indications … seem to support the quadratic dependence … τ ∼ m²".
- **Two time scales** (Christodoulou & D'Ambrosio, 1801.03027 v3, 25 Apr 2024) [verified, latest-version PDF]. The
  *crossing time* T_c ∝ m, agreeing with Ambrus–Hájíček and Barceló–Carballo-Rubio–Garay. The *lifetime*, for a
  "balanced" coherent state, is

    p ∼ e^{−m²Ξ/(ħG)} (eq. 57), τ ∼ m e^{m²Ξ/(ħG)} (eq. 58).

  Rovelli & Vidotto 2024 (App.) [verified] write τ(m) ∼ e^{Ξ/t(m)}, with Ξ = 24(ζ±)² ≈ 1820 and t(m) the state's spread
  parameter.
- **Hawking time and remnants** (Rovelli & Vidotto, 2407.09584 v4, 9 Sep 2024) [verified].
  - From P = dm/dt ∼ A T⁴ ∼ m^{−2}, τ_BH ∼ m₀³ (eqs. 27–28). The transition "could be as early as τ_BH ∼ m₀²".
  - The remnant settles into the superposition |m₀, m⟩ = α|m₀, m⟩_W + β|m₀, m⟩_B (eq. 35) at the area gap, with mass
    m = √(√3 γ cħ/(4G)) ∼ 14√γ μg (eq. 1).
  - Remnant dissipation |m₀, m_P⟩ → |0⟩ takes "at least of order m₀⁴".
  - Dark-matter window: m₀⁴ ≥ T_H together with m₀³ < T_H gives 10¹⁰ g ≤ m₀ < 10¹⁵ g (eqs. 46–48).
  - Earlier stability argument: Rovelli & Vidotto 2018 (1805.03872 v2) [abstract]: the superposition "is stable, because
    it is protected by the existence of a minimal eigenvalue of the area".
- **Remnants and information** (Bianchi, Christodoulou, D'Ambrosio, Haggard & Rovelli, 1802.04264 v2) [abstract]: white
  holes "with small masses but large finite interiors". Rovelli 1710.00218 v2 (28 Dec 2024; Universe 11, 6 (2025)): the
  number of interior states exceeds e^{S_BH}.
- **Geometry and amplitude programme.**
  - D'Ambrosio et al. 2021 Part I (2009.05016 v2; PRD 103, 106014) and Soltani, Rovelli & Martin-Dussaud Part II
    (2105.06876 v2; PRD 104, 066015): "an explicit expression for the transition amplitude from black to white hole
    horizon".
  - Han, Rovelli & Soltani 2023 (2302.03872 v1; PRD 107, 064011): a full metric in one asymptotic region, "determined by
    two parameters: the mass of the hole and the duration of the transition".
  - Fazzini, Rovelli & Soltani 2023 (2307.07797 v2; PRD 108, 044009): the Painlevé–Gullstrand discontinuity in the
    quantum Oppenheimer–Snyder model is "a coordinate effect", with no shock wave.
  - Rignon-Bret & Rovelli 2021 (2108.12823): a charged version.

### 4(b) Unresolved problems

1. **The lifetime is not determined.** Christodoulou & D'Ambrosio: "The lifetime is found to depend instead on the
   spread of the quantum state, and thus its dependence on the mass can take a large range of values … the
   truncation/approximation used here is not appropriate to estimate this observable with any certainty." Also: "we do
   not have a better argument for what should be the chosen value of t." *Problem:* fix the boundary coherent state's
   spread t(m) (possibly also depending on T/m) from first principles.
2. **Incompatible scalings in the literature:** m² (Haggard–Rovelli; the preliminary 2016 estimate), m³ (the transition
   at the end of Hawking evaporation, the 2018–2024 remnant scenario), e^{m²} (the balanced-state amplitude), and m for
   the crossing time. Bianchi, Brandsema, Czuprynski & Paraizo 2026 (2605.03922 v1, 5 May 2026) [abstract] derive a
   purification-time lower bound ∝ M₀⁴/ħ^{3/2}. If a Planck-mass hole is metastable, the time becomes exponential in M₀².
3. **Truncation.** The amplitude uses the first order in the vertex expansion (1605.05268). Christodoulou & D'Ambrosio
   consider "only 2-complexes without bulk faces, a significant limitation … it is not clear how our estimates will be
   affected under refinements". This is the continuum-limit problem of §3 in a concrete case. The dependence on the
   boundary surface (a "Heisenberg cut") is also discussed there.
4. **No complete calculation yet.** Donà, Haggard, Rovelli, Sreeram & Taddei 2025 (2507.16633 v2; PRD 112, 104004)
   [abstract] work in 3D Ponzano–Regge, "laying the basis for a future complete calculation of the amplitude in covariant
   Loop Quantum Gravity". Donà, Haggard, Rovelli & Vidotto 2024 (2402.09038 v2; PRD 109, 106016): "a precise
   identification of tunneling processes is still not known".
5. **Numerics.** Frisoni 2023 (2304.02691 v2; PRD 107, 126012) computes the crossing time numerically in the deep
   quantum regime and shows it "does not depend on the extrinsic geometry". Han, Qu & Zhang 2024 (2404.02796 v2; PRD 110,
   124055) use a 56-vertex complex and find the amplitude "dominated by the terms allowing the change in orientation".
   The role of orientation is therefore an open ingredient.
6. **White-hole instability.** Barceló, Carballo-Rubio & Garay 2016 (1511.00633 v2; JHEP 1601, 157) [abstract]:
   "transitions with long characteristic time scales are pathologically unstable". Rovelli & Vidotto 2024 reply that
   triggering the instability of a Planck-size hole needs trans-Planckian radiation, "likely not … allowed". They also
   concede that the remnant lifetime bound m₀⁴ "may not be correct".

---

## 5. Rovelli on time and his philosophical commitments

### 5(a) Formal content

- **Partial and complete observables** (gr-qc/0110035 v3, 21 Jan 2002; PRD 65, 124013) [abstract]. The extended
  configuration space C is "the space of the partial observables".
- **"Forget time"** (0903.3832 v3, 27 Mar 2009; FQXi essay) [verified].
  - Classical: a system is (C, Γ, f) with motions given by relations f(α, β) = 0, e.g. α − A sin(ωβ + φ) = 0. The
    dynamics is the constraint H(q^a, p_a) = 0 on T*C.
  - Quantum: kinematical states S ⊂ K ⊂ S′, and P = ∫ dτ e^{−iτH}.
  - Transition amplitudes W(s, s′) = ⟨s|P|s′⟩, probabilities P_{ss′} = |W(s, s′)|² (eqs. 5–7).
  - Physical states satisfy Hψ = 0. Complete observables satisfy [A, H] = 0 (eqs. 8–9).
  - The programme: "interpret mechanics as a theory of relations between variables, rather than the theory of the
    evolution of variables in time." On thermal time: "Time is, that is to say, the expression of our ignorance of the
    full microstate."
- **Is time's arrow perspectival?** (1505.01125 v2, 10 May 2015) [verified]. Coarse-grained entropy
  S_{A_n}(s) = log ∫_Γ ds′ ∏_n δ(A_n(s′) − A_n(s)) (eq. 1). *Conjecture:* "If the system is sufficiently complex and
  ergodic, for most paths s(t) that satisfy the dynamics and for each orientation of t, there is a family of observables
  A_n such that dS_{A_n}/dt ≥ 0" (eq. 3). Model: N balls with A_σ = mean x of subset σ. Coupling subsystems ("small
  balls", one per subset, 2^N of them) see low past entropy relative to their own coarse-graining. The abstract says the
  paper replies to Wald, Albert and Hartle.
- **Memory** (2003.06687 v1, 14 Mar 2020) [verified]. Traces form if (a) τ_em > t_tot, (b) T_e > T_m, (c) τ_m > t_m.
  The information bound is I < ΔS/k = C_m(T_e − T_m)²/(k T_e T_m) · (1 − e^{−τ_m/τ_em}) (eq. 6): "a mechanism that
  transforms initial low entropy … into available information".
- **Other papers on time and entropy.**
  - Causation (2211.00888 v2): "it is this gradient, and only this gradient, the source of the time orientation of
    causation".
  - Choice (2309.08557 v2): E > kT ln 2 per binary choice.
  - Becoming (1910.02474 v2; Found. Phys. 49, 1325): "Fundamental becoming is real, but local and unoriented."
  - Layers of time (2105.00540 v2).
  - Where was past low entropy? (1812.03578 v2).
  - Watanabe's theorem (Di Biagio & Rovelli, 2403.01062 v2): the no-backward-probability conclusion "does not follow".
  - Operational arrow (2010.05734).
  - Boltzmann brains (2407.13197; Wolpert, Rovelli & Scharnhorst 2507.10959 v4, 22 Jan 2026, Entropy 27, 1227): the
    entropy dynamics is formalised "as a time-symmetric, time-translation invariant Markov process". The Boltzmann-brain
    hypothesis and the second law "are equally legitimate (or not)".
  - Neuroscience and time (Buonomano & Rovelli, 2110.01976).
- **Books.** *L'ordine del tempo* (2017; English *The Order of Time*, 2018) and *Helgoland* (Italian 2020; English
  Riverhead/Allen Lane 2021). Years confirmed by search results only; **not verified against the publishers**.
  *Helgoland* invokes Nāgārjuna: "there is nothing that exists in itself, independently from something else" (per
  secondary sources in search; **book text not fetched**). Commitments visible in the fetched papers:
  - an ontology of relations, events or facts rather than substances or states ("Quantum mechanics is not about
    'quantum states': it is about values of physical variables", 1712.02894 v5);
  - naturalism with no privileged observers;
  - a "third way between realism and instrumentalism" (2512.06034).
  - Rovelli & Vidotto, *Philosophical Foundations of LQG* (2211.06718 v2) set out emergence of space and time, locality,
    truncation and observables.

### 5(b) Open problems

1. The perspectival-arrow claim is stated as a *conjecture* (eq. 3). No theorem is given for realistic
   (field-theoretic, gravitational) systems. *Problem:* prove or refute that for generic microstates of a sufficiently
   rich system, subsystems with low-past-entropy coarse-grainings exist generically. Give their measure.
2. How the thermal-time flow (a state-defined, orientation-free flow) relates to the entropy gradient that orients
   memory and causation. The fetched papers treat these separately. I found no derivation linking them. [my reading]
3. General-covariant statistical mechanics is "still lacking" (1309.0777).

---

## 6. Rovelli's recent papers (2020–2026)

The table is taken from the arXiv author search, sorted by announcement. Dates are those of the latest version shown.

| arXiv | latest version seen | title (short) | note |
|---|---|---|---|
| 2603.16999 | v2, 14 Sep 2026 | Structure of the continuum limit of spin foams (Bruno, Colafranceschi, Mele, Rovelli) | TQFT-style axioms; no-go for strong convergence; rigging map; PRD 114, 066005 |
| 2512.06034 | v2, 4 Jan 2026 | Tractatus Quanticus (Covoni, Rovelli) | RQM philosophy |
| 2510.11349 | v2, 9 Feb 2026 | Relative Information, Relative Facts (Di Biagio, Rovelli) | perspectives = commutative observables |
| 2507.16633 | v2, 5 Nov 2025 | Spinfoam tunneling in angle variables (Donà, Haggard, Rovelli, Sreeram, Taddei) | PRD 112, 104004 |
| 2507.10959 | v4, 22 Jan 2026 | Boltzmann brains, memory, second law (Wolpert, Rovelli, Scharnhorst) | Entropy 27, 1227 |
| 2410.20012 | v2, 14 Dec 2024 | Solipsism and RQM | reply to critics |
| 2407.09584 | v4, 9 Sep 2024 | Planck stars, white holes, remnants (Rovelli, Vidotto) | review |
| 2403.01062 | v2, 11 Sep 2024 | Time orientation of probabilistic theories | Watanabe |
| 2402.09038 | v2, 18 May 2024 | Tunneling of quantum geometries in spinfoams | PRD 109, 106016 |
| 2309.08557 | v2, 10 Jan 2024 | Thermodynamic cost of choosing | E > kT ln 2 |
| 2309.08238 | v3, 27 Sep 2024 | Detecting gravitationally interacting DM (Perez, Rovelli, Christodoulou) | Planck-mass DM |
| 2307.07797 | v2, 3 Aug 2023 | PG discontinuity in quantum OS model | PRD 108, 044009 |
| 2302.03872 | v1, 8 Feb 2023 | Geometry of the BH→WH transition in one region | PRD 107, 064011 |
| 2211.06718 | v2, 27 Nov 2022 | Philosophical foundations of LQG | |

Rows omitted here but cited above: 2305.07343, 2203.13342, 2111.03166, 2109.09170, 2105.06876, 2009.05016, 2211.00888,
2003.06687, 2105.00540, 1910.02474. Also on the list: 2407.13197, 2407.02840 (Boltzmann brains and bridges), 2305.05645 and
2202.03368 (gravity-mediated entanglement), 2207.06978 (remnant emission), 2009.10362 (gauge), 2007.05300 (agency). The search
returned 244 Rovelli records in total; this is a selection.

---

## 7. What I could not verify
- Swanson 2021 (TTH objections): only the search-engine abstract was available (PhilSci and Cambridge were refused,
  CORE timed out).
- Rovelli 1993 CQG, *The Order of Time* and *Helgoland* texts: not fetched.
- The explicit two-term EPRL asymptotic formula with S_R = Σ γ j Θ: stated as the standard result, not re-read today.
- The non-geometricity of massive-field modular flows in diamonds: the standard expectation, with no specific theorem
  fetched.
- The "Bamonti et al. (2025)" critique of thermal time mentioned in a search snippet: not located.
- Journal references given only in search results (Chua 2024 in J. Gen. Phil. Sci.; Swanson in Phil. Sci.) are unverified.
