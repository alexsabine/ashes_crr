# Prior-art check: three claims (economics, evolution, learning)

Date of check: 2026-09-24. Checker: Claude (subagent). Scope: literature search only; nothing in the repo was edited.

Access notes. The web search tool worked. Crossref worked, with some rate-limit failures. The PubMed MCP worked and returned full text for PMC items. arXiv abstract pages worked. These were blocked or rate-limited: Semantic Scholar (HTTP 429), OpenAlex (daily budget used up), ScienceDirect, IDEAS/RePEc, Frontiers, Springer Link, pmc/pubmed web pages (egress-blocked). So several key sources were readable **only as an abstract or a search-engine snippet**, and each one is marked as such below.

Arithmetic re-checks were run in scratch scripts `arith.py`, `c2.py` and `c3.py` in this folder, using the repo's `uv` environment for numpy. Their outputs are quoted below.

---

## Claim 1: Samuelson multiplier-accelerator with adaptive (permanent) income

**Model:** Y_t = C_t + I_t + G, I_t = v(C_t − C_{t−1}), C_t = c·P_{t−1}, P_t = (1−q)Y_t + qP_{t−1}.
**Claimed:** P_t = [(1−q)c(1+v)+q]P_{t−1} − (1−q)cv·P_{t−2}. The determinant is (1−q)cv, so v_c = 1/((1−q)c) = 2.5 at c = 0.8 and q = 0.5, against Samuelson's 1/c = 1.25.

### (a) Searches run
- Web search: "multiplier-accelerator model adaptive expectations consumption permanent income stability condition"
- Web search: "Samuelson multiplier accelerator distributed lag consumption stabilizing Hicks trade cycle"
- Web search: "Biederman 1993 'Permanent income and long-run stability' multiplier accelerator abstract"
- Web search: "'permanent income' multiplier accelerator 'makes stability more likely' current measured income destabilizing"
- Web search: "Kaskarelis Varelas 1996 permanent income credit rationing open economy multiplier accelerator"
- Web search: "Samuelson model consumption exponentially weighted past incomes Koyck lag accelerator stability condition textbook Allen Gandolfo"
- Web search: "Westerhoff 'Samuelson's multiplier-accelerator model revisited' Applied Economics Letters"
- Web search: "Hicks 1950 trade cycle distributed lags consumption damping ..."
- Web search: "Chow 1967 multiplier accelerator liquidity preference permanent income ..."
- Crossref: "permanent income multiplier accelerator stability"; "multiplier accelerator adaptive expectations consumption distributed lag"; "The permanent income hypothesis and long-run economic stability"; plus DOI lookups and Biederman's reference list.
- Full text read: Lines & Westerhoff (2006) PDF from uni-bamberg.de. Todorova MPRA 107480 PDF (grep only).

### (b) Closest works
1. **Biederman, D. K. (1993).** "Permanent income and long-run stability in a generalized multiplier/accelerator model." *Journal of Macroeconomics* 15(2): 249–272. DOI 10.1016/0164-0704(93)90027-J.
   - **Read as a search-engine snippet of the abstract only.** ScienceDirect and RePEc were blocked and Crossref carries no abstract.
   - The snippet, paraphrased by the search tool and **not verbatim-verified**, says: introducing a PIH-type consumption function into a multiplier/accelerator model "unambiguously makes stability more likely, provided current measured income influences permanent income"; but "when only previous measured incomes influence permanent income, then the PIH-type consumption function may actually be destabilizing."
   - The reference list, which Crossref does return, cites Samuelson 1939, Friedman 1957, Allen 1966, Chiang 1984, Sargent 1987, Bewley 1980 and Folsom 1976 (stability conditions for difference equations).
2. **Kaskarelis, I. A. & Varelas, E. (1996).** "Permanent income and credit rationing in the open economy multiplier/accelerator model: An exercise for the developing countries case." *J. Macroeconomics* 18(3): 531–549. DOI 10.1016/S0164-0704(96)80036-X.
   - **Abstract only, via search snippet.** "Stability conditions and simulations results show that government actions could be destabilizing if consumption patterns are closer to the Keynesian archetype than to the permanent income hypothesis."
3. **Lines, M. & Westerhoff, F. (2006).** "Expectations and the multiplier-accelerator model." In Puu & Sushko (eds.), *Business Cycle Dynamics*, Springer. DOI 10.1007/3-540-32168-3_10.
   - **Full text read.** Consumption is C_t = b·E_{t−1}[Y_t], where the expectation is a *nonlinear* mix of extrapolative and reverting rules. Their eq. (6) restates Samuelson's condition "b < 1/k".
   - This is not adaptive or permanent income, so it is not the claim's model.
4. **Hicks, J. R. (1950).** *A Contribution to the Theory of the Trade Cycle.* Oxford.
   - **Not read.** A secondary source (HET website, via search snippet) says Hicks uses a distributed-lag consumption function C_t = c₁Y_{t−1} + c₂Y_{t−2}, and that distributed lags stabilise in continuous-time versions (Matsumoto & Szidarovszky).
   - Related but not the geometric (adaptive) lag.
5. **Chow, G. C. (1967).** "Multiplier, accelerator, and liquidity preference in the determination of national income in the United States." *REStat* 49(1): 1–15. DOI 10.2307/1937879. **Not read.** It is an econometric multiplier-accelerator model; I did not verify whether it contains a permanent-income stability analysis.
6. Also relevant, but none checked in full text:
   - Westerhoff (2006), *Appl. Econ. Lett.* 13: 89–92, DOI 10.1080/13504850500390663. Nonlinear expectations of *investors*, not consumption.
   - Laffargue & Malgrange (1991), "Rationality and cycles in the multiplier-accelerator model," DOI 10.1007/978-1-349-11570-9_7. Blocked; content unknown.
   - Gandolfo, *Economic Dynamics*, and Allen (1966) textbooks. Could not access, so I cannot confirm whether an exercise states this exact recursion.

### (c) Reproduction of the number
- Re-derivation:
  - Substitute C_t = cP_{t−1} and I_t = cv(P_{t−1} − P_{t−2}) into Y_t. This gives Y_t = c(1+v)P_{t−1} − cvP_{t−2} + G.
  - Then P_t = (1−q)Y_t + qP_{t−1} gives the claimed recursion, with a₂ = (1−q)cv.
- Jury conditions:
  - 1 − a₁ + a₂ = (1−q)(1−c) > 0 always.
  - 1 + a₁ + a₂ > 0 always.
  - So the binding condition is (1−q)cv < 1, which gives v_c = 1/((1−q)c) = 1/(0.5·0.8) = **2.5**. Samuelson's is 1/0.8 = **1.25**.
- Numerical root moduli at c = 0.8, q = 0.5:

  | v | root modulus |
  |---|---|
  | 2.4 | 0.9798 |
  | 2.5 | 1.0000 |
  | 2.6 | 1.0198 |

  The claim's arithmetic is correct.
- No accessible source prints v_c = 1/((1−q)c). Biederman's abstract states the **direction**: PIH consumption is stabilising, with a timing caveat.
- **Caveat to resolve before claiming anything.** In the claim, C_t depends on P_{t−1}, which is built from Y_{t−1}, Y_{t−2}, …. That is, "only previous measured incomes" feed consumption. This is the case in which Biederman's abstract says PIH consumption "may actually be destabilizing".
  - The two need not conflict. The claim benchmarks against Samuelson's C_t = cY_{t−1}, and Biederman's baseline may be a current-income Keynesian function.
  - But this cannot be settled without Biederman's full text. **Unverified.**

### (d) Verdict: **PARTIAL**
- Stated in the literature: PIH or adaptive consumption in a multiplier/accelerator model, and its (conditional) stabilising effect on stability. Biederman 1993, abstract; Kaskarelis & Varelas 1996, abstract.
- Not found in an accessible text: the specific closed form v_c = 1/((1−q)c).
- It is a two-line substitution that could well be a textbook exercise (Allen 1966, Gandolfo, Chiang are all cited by Biederman), so novelty should not be claimed.

---

## Claim 2: Stabilising selection with inheritance from an exponentially weighted lineage mean

**Model:** fitness exp(−x²/2w²) with w² = 1; mutation variance μ = 0.01. The offspring seed is (1−q)x_parent + q·m_lineage, and x_child = seed + N(0, μ).
**Claimed:**

| | q = 0 | q = 0.5 |
|---|---|---|
| Equilibrium variance before selection | 0.10512 | 0.05639 |
| Load ½ln(1+V/w²) | 0.04998 | 0.02743 |
| Generations to halve a displacement | 7 | 14 |

### (a) Searches run
- Web search: "maternal effects model offspring phenotype weighted average ancestors mutation-selection balance stabilizing selection variance"
- Web search: "Day Bonduriansky 2011 unified approach ... stabilizing selection equilibrium"
- Web search: "nongenetic inheritance reduces mutation load or equilibrium variance stabilizing selection model 'grandparental' OR 'ancestral' inheritance quantitative trait"
- Web search: "Galton law of ancestral heredity geometric weights ancestors selection model equilibrium variance"
- Web search: "Tal Kisdi Jablonka 2010 epigenetic contribution covariance between relatives ..."
- Crossref: "evolution of maternal characters Kirkpatrick Lande"; "unified approach evolutionary consequences genetic and nongenetic inheritance"; "transmission of environmental deviation phenotypic variance stabilizing selection equilibrium"; "Lande Price 1989 ..."; "Hoyle Ezard benefits of maternal effects ..."; "Bonduriansky Day nongenetic inheritance ..."; "inheritance of acquired characters quantitative genetic model stabilizing selection equilibrium variance"; "Bulmer ... asexual Gaussian mutation stabilizing".
- PubMed: metadata for PMIDs 42396575, 9988590, 21750377 and 20100941. Full text of PMC13323190 (Hoyle, Ezard & Kuijper 2026).
- arXiv abstract page 1302.1293 (Altenberg).

### (b) Closest works
1. **Hoyle, R. B. & Ezard, T. H. G. (2012).** "The benefits of maternal effects in novel and in stable environments." *J. R. Soc. Interface* 9: 2403–2413. DOI 10.1098/rsif.2012.0183.
   - **Abstract only (Crossref), truncated:** "In a stable environment, negative maternal effects that slow phenotypic evolution actually minimize variance around the o[ptimum] ...".
   - Restated in the full text of their 2026 follow-up (below): "Positive cascading maternal effects can accelerate the response to selection ... at the cost of greater phenotypic variance and lower equilibrium population mean fitness. Conversely negative cascading maternal effects ... can slow the response to selection, and if they are not too strong can also reduce phenotypic variance and increase population mean fitness at equilibrium (Hoyle and Ezard)."
   - Also, from the 2026 paper: "in a noisy equilibrium environment mean fitness is maximised at a negative value of [m]".
2. **Hoyle, R. B., Ezard, T. H. G. & Kuijper, B. (2026).** "How to account for past selection when maternal effects are cascading." *Ecology and Evolution* 16(7): e73725. DOI 10.1002/ece3.73725.
   - **Full text read (PMC13323190); the equations did not render.**
   - Model: z_t = a + b·ε + m·z*_{t−1} + e. The phenotype therefore carries a geometrically weighted sum over all maternal-lineage ancestors ("each individual phenotype depends on the phenotypes of all its previous maternal lineage ancestors").
   - Gaussian stabilising selection, with Lande (1976) and Kirkpatrick & Lande (1989) machinery.
3. **Kirkpatrick, M. & Lande, R. (1989).** "The evolution of maternal characters." *Evolution* 43(3): 485–503. DOI 10.1111/j.1558-5646.1989.tb04247.x (erratum 1992, DOI 10.1111/j.1558-5646.1992.tb02004.x).
   - **Not read (metadata only).** This is the founding cascading-maternal-effect model (offspring phenotype depends on the mother's phenotype, hence on the whole lineage). It is known for time lags and momentum in the response to selection.
4. **Lande, R. & Price, T. (1989).** "Genetic correlations and maternal effect coefficients obtained from offspring-parent regression." *Genetics* 122(4): 915–922. DOI 10.1093/genetics/122.4.915. **Abstract only.** A dynamic maternal-effects model; not an equilibrium-variance-under-mutation result.
5. **Day, T. & Bonduriansky, R. (2011).** "A unified approach to the evolutionary consequences of genetic and nongenetic inheritance." *Am. Nat.* 178(2): E18–E36. DOI 10.1086/660911.
   - **Abstract only (PubMed).** A Price-equation framework applied to "nontransmissible environmental noise, maternal effects, ... transgenerational epigenetic inheritance ... cultural inheritance".
   - No equilibrium variance or load under an EWMA lineage mean is visible in the abstract.
   - Related work, also abstract only: Bonduriansky & Day (2009), *Annu. Rev. Ecol. Evol. Syst.* 40, DOI 10.1146/annurev.ecolsys.39.110707.173441; and Bonduriansky, Crean & Day (2012), *Evol. Appl.*, DOI 10.1111/j.1752-4571.2011.00213.x. The latter says "Theory suggests that nongenetic inheritance can increase the rate of both phenotypic and genetic change".
6. **Tal, O., Kisdi, E. & Jablonka, E. (2010).** "Epigenetic contribution to covariance between relatives." *Genetics* 184(4): 1037–1050. DOI 10.1534/genetics.109.112466.
   - **Abstract only.** It models "epigenetic transmissibility (the probability of transmission of ancestral phenotypes)" with reset opportunities. This is about covariances between relatives, not load.
7. **Galton's law of ancestral heredity (1885/1897); Bulmer, M. (1998),** "Galton's law of ancestral heredity," *Heredity* 81: 579–585, DOI 10.1046/j.1365-2540.1998.00418.x.
   - **Abstract only.** "the two parents contribute between them on average one-half of the total heritage of the offspring, the four grandparents one-quarter, and so on."
   - This is inheritance from a **geometrically (exponentially) weighted lineage**: the oldest precedent for the claim's inheritance rule. It has no mutation-selection equilibrium.
8. **Altenberg, L. (2013).** "Implications of the Reduction Principle for Cosmological Natural Selection." arXiv:1302.1293 (v2, 20 Feb 2013).
   - **Abstract read.** "When mechanisms of variation themselves vary, they are subject to Feldman's (1972) evolutionary Reduction Principle that selection favors greater faithfulness of replication ... The most faithful inheritance law dominates the ensemble of universes."
   - The claim's lineage memory is a more faithful inheritance law, since less new variation is transmitted. So its direction (lower load) is what the reduction principle predicts. Altenberg gives no Gaussian variance formula.
9. **The baseline (q = 0) number is standard.** Asexual Gaussian mutation-selection balance with Gaussian stabilising selection:
   - V_sel = V·w²/(V+w²) and V = V_sel + μ.
   - Hence V = [μ + √(μ² + 4μw²)]/2.
   - This is the Kimura/Lande/Bulmer Gaussian-approximation form (Bulmer 1972, *Genet. Res.* 19, DOI 10.1017/S0016672300014221, abstract read; Bulmer 1989, *Genome* 31, DOI 10.1139/g89-135, abstract read). I did not verify the exact printed formula in those texts. **It is textbook-standard, but no quote was verified.**

### (c) Reproduction of the numbers
- **Baseline:** [0.01 + √(0.0001 + 0.04)]/2 = **0.105125**. Load ½ln(1.105125) = **0.049979**. Both match the claim.
- **q = 0.5**, under the reading m_child = seed = (1−q)x_parent + q·m_parent, i.e. the lineage mean is an EWMA of ancestral selected phenotypes. I propagated the bivariate Gaussian (x, m) through Gaussian selection on x and got:
  - V = **0.0563904**
  - load = **0.0274289**
  - halving time = **7** generations (q = 0) against **14** (q = 0.5)

  All match the claim.
- Equivalent form: seed g, x = g + e, g' = g_sel + (1−q)e_sel. Only a fraction (1−q) of each new deviation becomes heritable. So this is a transmissibility-less-than-one model in the Tal–Kisdi–Jablonka / Day–Bonduriansky sense, and lower standing variance with slower response is the expected trade-off.
- No source found prints the q-dependent equilibrium variance, load or halving time for this rule.

### (d) Verdict: **PARTIAL**
- **Known:**
  - The baseline Gaussian mutation-selection balance.
  - The inheritance rule itself: geometric ancestral weighting (Galton; Bulmer 1998), and cascading maternal effects (Kirkpatrick & Lande 1989; Hoyle & Ezard 2012).
  - The *direction* of the trade-off. Hoyle & Ezard: inheritance that slows the response reduces variance around the optimum and raises equilibrium mean fitness; the reverse for effects that speed it up.
  - The evolutionary logic that more faithful inheritance lowers load and is favoured (Karlin/Feldman reduction principle; Altenberg 2013 for CNS).
- **Not found:** the closed-form or numerical equilibrium V, load and halving time under an EWMA-lineage-mean inheritance rule. Given how many near-variants exist, an exact equivalent in the maternal-effects literature cannot be excluded without the full texts of Kirkpatrick & Lande 1989 and Hoyle & Ezard 2012, which I could not access. **Mark as unverified-novel at most.**

---

## Claim 3: Switching contingency: forgetting against accumulated Dirichlet counts

**Setup:** Bernoulli p switching between 0.8 and 0.2 with hazard 0.005 per trial, over 20 000 trials.
**Claimed MAE:**

| Estimator | MAE |
|---|---|
| EWMA, rate 0.05 | 0.0886 |
| Accumulated Beta/Dirichlet counts | 0.2912 |
| Exact HMM filter (the ceiling) | 0.0333 |

### (a) Searches run
- Web search: "forgetting factor Beta Bernoulli volatile environment exponential forgetting outperforms Bayesian accumulation changepoint"
- Web search: "Meyniel ideal observer hidden Markov change point Bernoulli volatility compared leaky integrator exponential decay performance"
- Web search: "discounted Thompson sampling Beta counts non-stationary bandit abruptly changing environment outperforms"
- Web search: "active inference Dirichlet concentration parameters forgetting volatility decay learning rate reversal learning Friston"
- Web search: "Yu Dayan 2005 uncertainty neuromodulation attention change point exponential filter approximation"
- Web search: "Yu Cohen 2008 'Sequential effects: Superstition or rational behavior' dynamic belief model fixed belief model exponential filter"
- Web search: "'step-by-step tutorial on active inference' Smith Friston Whyte forgetting rate omega Dirichlet"
- Crossref: Wilson/Nassar/Gold; Kulhavý & Zarrop; Smith/Friston/Whyte; Behrens et al.; Nassar et al. 2010.
- PubMed: metadata for 26412953, 28030543, 30964861, 27375276, 27870614, 23935472 and 17676057. Full text of PMC5167251 (Friston et al. 2016).
- Full-text PDFs read: Yu & Cohen (NeurIPS 2008); Smith, Friston & Whyte (2022).
- arXiv abstracts: 0805.3415, 1707.09727, 0710.3742.

### (b) Closest works
1. **Yu, A. J. & Cohen, J. D. (2008).** "Sequential effects: Superstition or rational behavior?" *NeurIPS 21*: 1873–1880. PMID 26412953.
   - **Full text read.** This is the same three-way structure as the claim:
     - a *Fixed Belief Model* (FBM): accumulated Beta counts, p(γ|x) ∝ γ^{r_t+a−1}(1−γ)^{t−r_t+b−1};
     - a *Dynamic Belief Model* (DBM): an exact Bayesian filter for a Bernoulli rate that is redrawn with probability 1−α;
     - a linear exponential filter. They derive β ≈ (2/3)α and show it "track[s] the true Bayesian P_t very well".
   - Quote: "Linear exponential filtering thus appears to be both a good descriptive model of behavior, and a good normative model approximating Bayesian inference."
   - Quote on FBM: "inference in FBM leads to less variable and more accurate estimate of the underlying bias as the number of samples increases", which is true only under stationarity.
   - Their generative model redraws the rate from a Beta prior rather than switching between two known levels, and they report no MAE table.
2. **Behrens, T. E. J., Woolrich, M. W., Walton, M. E. & Rushworth, M. F. S. (2007).** "Learning the value of information in an uncertain world." *Nat. Neurosci.* 10(9): 1214–1221. DOI 10.1038/nn1954.
   - **Abstract only.** "the weight given to decision outcomes ... should be modulated by the volatility of the reward environment."
   - Their task uses switching reward probabilities; the claim's ordering is the premise of that paper.
3. **Nassar, M. R., Wilson, R. C., Heasly, B. & Gold, J. I. (2010).** *J. Neurosci.* 30(37): 12366–12378. DOI 10.1523/JNEUROSCI.0822-10.2010.
   - **Wilson, R. C., Nassar, M. R. & Gold, J. I. (2013).** *PLoS Comput. Biol.* 9(7): e1003150. DOI 10.1371/journal.pcbi.1003150.
   - **Abstracts only.** The 2013 paper says basic delta rules "are effective under only a restricted set of conditions in which the environment is stable", and that a mixture of delta rules approximates the exact Bayesian change-point solution.
   - This is the same ceiling ordering: exact change-point Bayes, then approximations, then a fixed rule.
4. **Adams, R. P. & MacKay, D. J. C. (2007).** "Bayesian Online Changepoint Detection." arXiv:0710.3742 (v1). **Abstract read.** The exact online change-point posterior, i.e. the ceiling filter class.
5. **Exponential forgetting in estimation and bandits:**
   - **Kulhavý, R. & Zarrop, M. B. (1993).** "On a general concept of forgetting." *Int. J. Control* 58(4): 905–924. DOI 10.1080/00207179308923034. **Metadata only.**
   - **Garivier, A. & Moulines, E. (2008/2011).** "On upper-confidence bound policies for non-stationary bandit problems." arXiv:0805.3415 (v1). **Abstract read.** Discounted and sliding-window UCB for rewards that "remain constant over epochs and change at unknown time instants"; nearly matching the lower bound.
   - **Raj, V. & Kalyani, S. (2017).** "Taming non-stationary bandits: a Bayesian approach." arXiv:1707.09727 (v1). **Abstract read.** "Applying discounting to the parameters of prior distribution ... to systematically reduce the effect of past observations". These are discounted Beta counts.
6. **Active inference:**
   - **Smith, R., Friston, K. J. & Whyte, C. J. (2022).** "A step-by-step tutorial on active inference and its application to empirical data." *J. Math. Psychol.* 107: 102632. DOI 10.1016/j.jmp.2021.102632. **Full text read.**
     - Eq. (34): d_{trial+1} = ω·d_trial + η·s.
     - Quote: "The omega (ω) parameter is a forgetting rate (scalar from 0–1), which influences how quickly learning in recent trial can 'overwrite' the changes in d that occurred in earlier trials."
     - It also notes that volatility "could also be implemented in a more principled manner in a hierarchical model (... the Hierarchical Gaussian Filter ...)".
   - **Friston, K., FitzGerald, T., Rigoli, F., Schwartenbeck, P., O'Doherty, J. & Pezzulo, G. (2016).** "Active inference and learning." *Neurosci. Biobehav. Rev.* 68: 862–879. DOI 10.1016/j.neubiorev.2016.06.022. **Full text read.** It shows accumulated context counts causing perseveration in reversal learning: "the number of perseverative trials before reversal, as a function of previous exposures to the original context".
7. Also relevant, all abstract only:
   - Meyniel, Maheu & Dehaene (2016), *PLoS CB* 12: e1005260, DOI 10.1371/journal.pcbi.1005260. A change-point Bayesian learner for transition probabilities.
   - Heilbron & Meyniel (2019), *PLoS CB* 15: e1006972, DOI 10.1371/journal.pcbi.1006972. Flat leaky learners "can learn efficiently, even in uncertain and changing environments".
   - Mathys et al. 2011 (HGF) and Yu & Dayan 2005 (*Neuron*) were not opened beyond search snippets.

### (c) Reproduction of the numbers
- These are simulation outputs; no paper reports these exact values.
- My independent re-simulation used the same parameters, one-step-ahead prediction, and three seeds:

  | Estimator | MAE range across 3 seeds |
  |---|---|
  | EWMA (rate 0.05) | 0.0873–0.0926 |
  | Beta(1,1) counts | 0.2800–0.2938 |
  | HMM forward filter | 0.0327–0.0353 |

  The claimed values are consistent with this.
- The accumulated-count figure is close to forced by arithmetic. With about 50% of the time in each state, the count mean converges to ≈ 0.5, so its MAE → |0.8 − 0.5| = 0.3.

### (d) Verdict: **FOUND** (as a qualitative statement); the numbers are a new simulation instance, not a new result
The statement is standard, with the ordering *exact change-point/HMM Bayes filter ≥ exponential forgetting (leaky integrator / delta rule / discounted Beta counts) ≫ accumulated counts in a switching environment*:
- Yu & Cohen 2008 (FBM vs DBM vs exponential filter, same structure);
- Behrens 2007;
- Nassar 2010 and Wilson et al. 2013;
- Garivier & Moulines;
- Raj & Kalyani;
- in active inference, the forgetting rate ω on Dirichlet counts (Smith et al. 2022) and the perseveration of accumulated counts in reversal (Friston et al. 2016).

Nothing novel should be claimed beyond the specific MAE values for this parameter set.

---

## Summary

| Claim | Verdict | Key prior art |
|---|---|---|
| 1. Multiplier-accelerator + adaptive permanent income | **PARTIAL** | Biederman 1993 (J. Macro 15: 249; abstract snippet only) states PIH consumption stabilises, with a timing caveat that must be checked against the claim's C_t = cP_{t−1}. Closed form v_c = 1/((1−q)c) not found in accessible text; the arithmetic is verified. |
| 2. Lineage-mean inheritance under stabilising selection | **PARTIAL** | Baseline 0.10512 is standard Gaussian mutation-selection balance. Geometric ancestral inheritance (Galton/Bulmer 1998) and cascading maternal effects (Kirkpatrick & Lande 1989; Hoyle & Ezard 2012: slower response gives lower variance and higher equilibrium fitness) give the direction; the reduction principle (Altenberg 2013) gives the logic. The q-dependent V, load and halving numbers were not found; they were reproduced under the reading m_child = seed. |
| 3. Forgetting vs accumulated counts vs HMM ceiling | **FOUND** (qualitative) | Yu & Cohen 2008 (FBM/DBM/exponential filter), Behrens 2007, Wilson et al. 2013, discounted bandits, and the active-inference forgetting rate (Smith et al. 2022). The MAE values are a new instance, consistent with re-simulation. |
