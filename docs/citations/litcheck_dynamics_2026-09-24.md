# Prior-art check: three "remembered feedback" dynamics claims (2026-09-24)

Scope: literature check only. Nothing in the repository was edited. Downloaded full texts and their
text extractions are in this folder (`*.pdf`, `*.txt`).

Blocked or unusable hosts (so these were NOT read): link.springer.com, sciencedirect.com,
journals.physiology.org, www.semanticscholar.org web pages, researchgate.net, journals.aps.org full text.
The Semantic Scholar API worked once and then rate-limited (429). Worked: arxiv.org/pdf, PubMed E-utilities,
Crossref API, OpenAlex API, author-hosted PDFs, WebSearch.

Legend: **[FT]** = I read the relevant full-text passage. **[ABS]** = abstract only (PubMed/Crossref).
**[SNIP]** = search-engine snippet only. **[MEM]** = from memory, not verified today.

## 0. Checking the claims' own arithmetic

I did these checks with numpy in the project env (`uv run --frozen python`, not committed):

- C1: `q - s(1-q)` at q=0.5: s=2.9 → -0.95; s=3.0 → -1.00; s=3.1 → -1.05. (1+q)/(1-q) = 3. Correct.
- C2: J = [[1-r(1-q), -rq], [1-q, q]], q=0.5. Eigenvalues at r=5.9: (-0.885, -0.565); at r=6.0: (-1.0, -0.5);
  at r=6.1: (-1.092, -0.458). det J = 0.5 = q. Correct: it is a flip at r=6, and no Neimark–Sacker is possible because det = q < 1.
- C3: at the equilibrium x* = c/d = 2, y* = a/b = 2, M* = 2, the characteristic polynomial is
  T λ³ + λ² + (b x*)(d y*) = λ³ + λ² + 0.5 (T=1). Roots: -1.29716 and **0.14858 ± 0.60281i**. Correct.

---

## Claim 1: cardiac restitution with exponentially smoothed DI; threshold s = (1+q)/(1-q)

### (a) Queries run
1. WebSearch: `Tolkacheva Schaeffer Gauthier Krassowska 2003 condition for alternans stability 1:1 response memory model`
2. WebSearch: `Fox Bodenschatz Gilmour 2002 period-doubling instability and memory in cardiac tissue PRL`
3. WebSearch: `Otani Gilmour 1997 memory models for the electrical properties of local cardiac systems J Theor Biol`
4. WebSearch: `alternans criterion "S12" "Sdyn" memory map stability 1:1 response restitution portrait Kalb 2004`
5. WebSearch: `cardiac restitution map exponentially weighted average of previous diastolic intervals memory alternans threshold slope`
6. WebSearch: `Tolkacheva criterion alternans "S12" "Sdyn" "1 + Sdyn" OR "(1/Sdyn" stability condition memory mapping model`
7. WebSearch: `Cherry Fenton 2007 "A tale of two dogs" memory alternans restitution slope greater than one`
8. WebSearch: `Nerlove 1958 adaptive expectations cobweb stability condition (2-β)/β slope ratio`
9. WebSearch: `Aicardi Invernizzi "Memory effects in discrete dynamical systems" logistic map geometric weights average`
10. WebSearch: `Bischi "fading memory" discrete dynamical systems exponentially weighted average past states period doubling stabilizing Naimzada`
11. PubMed efetch: PMIDs 12689098, 12225067, 9245581, 11893591, 15089319, 16035891; Crossref lookups for the same papers.

### (b) Closest works

1. **Tolkacheva EG, Schaeffer DG, Gauthier DJ, Krassowska W (2003).** Condition for alternans and stability of the 1:1
   response pattern in a "memory" model of paced cardiac dynamics. *Phys Rev E* 67:031904. doi:10.1103/PhysRevE.67.031904.
   [ABS] The model is A_{n+1} = F(A_n, D_n). "the stability criterion depends on the slope of both the dynamic and S1-S2
   restitution curves, and ... the pattern can be stable even when the individual slopes are greater or less than one."
   **I read the formula [FT] in the companion preprint:** Tolkacheva, Romeo, Gauthier, "Control of cardiac alternans in a
   mapping model with memory", arXiv:physics/0303099v1 (24 Mar 2003), which cites the PRE paper as [14]:
   "alternans can exist when |F′| = |1 − (1 + 1/S_dyn) S12| ≥ 1, (3) where F′ is the full derivative of F, with respect to
   A_n, evaluated at a fixed point [14]", with F′ = ∂F/∂A_n − ∂F/∂D_n ≡ µ and S12 = ∂F/∂D_n. It also says
   "the condition for the existence of alternans in the absence of control is given by µ ≤ −1".
   The published version is: Tolkacheva, Romeo, Guerraty, Gauthier, *PRE* 69:031904 (2004), doi:10.1103/PhysRevE.69.031904 [ABS].
2. **Fox JJ, Bodenschatz E, Gilmour RF Jr (2002).** Period-doubling instability and memory in cardiac tissue. *PRL* 89:138101.
   doi:10.1103/PhysRevLett.89.138101. [ABS] "Using linear stability analysis, we determined the onset of the alternans in the
   memory model and confirmed that the slope of the restitution curve was not predictive." This paper uses a physiological memory
   variable, not an exponential mean of DIs [MEM]. Its formula was not read.
3. **Otani NF, Gilmour RF Jr (1997).** Memory models for the electrical properties of local cardiac systems. *J Theor Biol*
   187:409–436. doi:10.1006/jtbi.1997.0447. [ABS] "The first of these models produces period-doubling and chaos ... when standard
   restitution dynamics would predict stability of the primary 1:1 pattern." This is the origin of the A_{n+1} = F(A_n, D_n) form
   (per arXiv:physics/0303099 [FT]). Its formula was not read.
4. **Watanabe MA, Koller ML (2002).** Mathematical analysis of dynamics of cardiac memory and accommodation: theory and experiment.
   *Am J Physiol Heart Circ Physiol* 282:H1534–H1547. doi:10.1152/ajpheart.00351.2001. [ABS] "a mathematical model treating memory
   as an exponentially decreasing shift of restitution curves shows that oscillatory DI,APD is expected with large ΔBCL, steep
   restitution slope, or increased cardiac accommodation." This is the closest in spirit (exponential memory). Its formula was
   not read because the host is blocked.
5. **Kalb SS et al. (2004)** The restitution portrait, *J Cardiovasc Electrophysiol* 15:698 (doi:10.1046/j.1540-8167.2004.03550.x), and
   **Kalb SS et al. (2005)** Restitution in mapping models with an arbitrary amount of memory, *Chaos* 15:023701 (doi:10.1063/1.1876912).
   [ABS/SNIP] These cover restitution portraits for maps with arbitrary memory. No exponential-smoothing formula was seen.
6. **Schaeffer DG et al. (2004)** An ionically based mapping model with memory for cardiac restitution, arXiv:q-bio/0407016v1
   (later in *Bull Math Biol* 2007). [FT] "A mapping leads to alternans when an eigenvalue ... of its Jacobian at the fixed point
   passes through −1" (λ ≈ −S12 in their specific model). It supports the criterion but is not this model.
7. **Nerlove M (1958).** Adaptive expectations and cobweb phenomena. *Q J Econ* 72:227–240. doi:10.2307/1880597.
   I did not read the original. [FT] of the secondary source Poitras G (2023), *J Hist Econ Thought* (doi:10.1017/S1053837222000116),
   which reproduces Nerlove's equation: with P*_t = βP_{t−1} + (1−β)P*_{t−1},
   "P_t − [(s1/d1 − 1)β + 1] P_{t−1} = (s0 − d0)β/d1", and says this gives "a much wider range of (s1/d1) values consistent
   with market stability than for first wave cobweb theory".
8. **Alonso-Sanz R, Losada JC, Porras MA (2017).** Bifurcation and chaos in the logistic map with memory. *Int J Bifurc Chaos*
   27:1750190. doi:10.1142/S0218127417501905. [ABS] The model is x_{T+1} = λ m_T(1−m_T), where m_T is the geometric-decay mean of
   past iterates: "most of the relevant properties of the dynamics can be explained by means of a scaling of the standard logistic
   map without memory." Related: Aicardi & Invernizzi (1992), *IJBC* 2:815 (two-term memory, doi:10.1142/S0218127492000458) [ABS];
   Alonso-Sanz (2011), *IJBC* 21:101 [ABS].

### (c) Does the published formula reproduce the number?

**Tolkacheva criterion.** If F is invertible near the fixed point (s ≠ 0), the claim's map can be written exactly in Tolkacheva
form. From A_n = F(M_{n−1}) we get M_{n−1} = F⁻¹(A_n), so

A_{n+1} = G(A_n, D_n) := F((1−q) D_n + q F⁻¹(A_n)).

At the fixed point:
- ∂G/∂D = s(1−q), which is S12.
- ∂G/∂A = q·s·(1/s) = q.
- The fixed points satisfy M* = D*, so the dynamic restitution curve is A = F(D) and S_dyn = s.
  (This agrees with S_dyn = G_D/(1 − G_A) = s(1−q)/(1−q) = s.)
- µ = 1 − (1 + 1/S_dyn)·S12 = 1 − (1 + 1/s)·s(1−q) = 1 − (s+1)(1−q) = **q − s(1−q)**. This is exactly the claim's multiplier.
- µ = −1 gives (s+1)(1−q) = 2, so s = (1+q)/(1−q). At q = 0.5: s = 3, with S12 = 1.5 and S_dyn = 3.

So the claim is the Tolkacheva et al. (2003) criterion evaluated at one particular choice of G.

**Nerlove cobweb (same linear structure).** The multiplier is 1 − β(1 + c) with c = s1/|d1|, and stability holds iff c < (2−β)/β.
With β = 1−q, (2−β)/β = (1+q)/(1−q). The claim's map, M_n = (1−q)(B − F(M_{n−1})) + q M_{n−1}, is the same exponentially
relaxed ("adaptive-expectations" or Mann) iteration of a one-dimensional map. Its multiplier 1 − β + β·(−s) = q − s(1−q) is
identical in form.

**Logistic map with geometric memory (Alonso-Sanz et al.).** This is derived, not read. Asymptotically m' = q m + (1−q) λ m(1−m),
which is a logistic map with parameter µ = q + (1−q)λ. Its flip at µ = 3 gives λ = (3−q)/(1−q). The memoryless slope at that λ is
2 − λ = −(1+q)/(1−q), so it is the same threshold.

### (d) Verdict: **FOUND**
A published general criterion, Tolkacheva et al. 2003 PRE (formula read in their arXiv:physics/0303099 companion), gives the
multiplier q − s(1−q) and the threshold (1+q)/(1−q) in one substitution. The identical linear result is also classical for
adaptive-expectation cobwebs (Nerlove 1958, read via Poitras 2023) and for maps with geometric memory. I did not find this exact
cardiac model, "APD responds to an EWMA of DIs", written down, but Watanabe & Koller 2002 (exponential memory, abstract only) is
close. The novelty is at most the choice of kernel, not the threshold.

---

## Claim 2: Ricker with remembered density M; first loss of stability moves from r = 2 to r = 2(1+q)/(1−q) = 6 (flip)

### (a) Queries run
1. WebSearch: `Levin May 1976 note on difference-delay equations stability x(t+1)=x(t)F(x(t-T))`
2. WebSearch: `Ricker map distributed delay discrete time geometric kernel exponentially weighted past densities stability flip bifurcation`
3. WebSearch: `Volterra difference equation convolution geometric kernel b^n stability condition Elaydi z-transform ...`
4. WebSearch: `discrete logistic Ricker equation x(n+1)=x(n)exp(r(1-sum p_i x(n-i))) local stability weights distributed delay Kocic Ladas`
5. WebSearch: `Alonso-Sanz "with memory" Ricker OR "Beverton-Holt" OR "population" map geometric decay memory of past iterations`
6. WebSearch: `discrete-time population model density dependence on exponentially weighted average of past densities stability boundary "flip" "determinant"`
7. WebSearch: `Royama second-order autoregressive model stability triangle delayed density dependence log abundance period-2 boundary`
8. Crossref: `Ricker model fading memory density dependence`; `Ricker map exponentially weighted moving average density`;
   `discrete population model geometric distributed delay stability`; `difference equation infinite delay geometric kernel population Ricker`;
   `delay difference equation exponential smoothing flip bifurcation threshold`; `Ricker equation with memory stability period doubling`.
9. Full-text greps: Braverman & Zhukovskiy arXiv:0901.1283; Gallas 1993 Physica A 195:417 (author PDF).

### (b) Closest works
1. **Levin SA, May RM (1976).** A note on difference-delay equations. *Theor Popul Biol* 9:178–187. doi:10.1016/0040-5809(76)90043-5.
   [SNIP] This covers x_{k+1} = x_k exp(α − x_{k−d}): "excessive time lags lead to stable limit cycle behavior". The condition
   0 < r < 2cos(Tπ/(2T+1)) is [MEM], unverified. It gives r < 1 for a pure one-step lag, lost through Neimark–Sacker. **This is
   not the claim's kernel.** The claim includes the current density with weight 1−q, and that is why the loss is a flip, not
   Neimark–Sacker.
2. **Royama T (1977, 1992)** second-order autoregressive (AR(2)) model of log abundance, X_t = β1 X_{t−1} + β2 X_{t−2}.
   [SNIP] Referenced in Barraquand et al. 2014 and Row et al. 2014. The stationarity/stability triangle, |β2| < 1 and
   β2 < 1 ± β1, is the standard AR(2) result (Box–Jenkins) [MEM]. Royama's own text was not read.
3. **Braverman E, Zhukovskiy S (2009/2012).** Absolute and delay-dependent stability of equations with a distributed delay.
   arXiv:0901.1283v1; *DCDS-A* 32:2041, doi:10.3934/dcds.2012.32.2041. [FT, grep] This is continuous-time distributed delay plus a
   bridge to difference equations. There is no Ricker–geometric-memory threshold.
4. **Liz E, Tkachenko V, Trofimchuk S (2006),** global stability in discrete models with delayed density dependence (*Math Biosci*),
   and **Kocić & Ladas (1993)**. [SNIP] These treat finite lags. No exponential-smoothing threshold was seen.
5. **Streipert S. (2024)** Derivation and dynamics of discrete population models with distributed delay in reproduction, SSRN
   doi:10.2139/ssrn.4742805. [title only] Not read. **This is the most likely place for a close variant. Unverified.**
6. **Elaydi S** and co-authors on linear Volterra difference equations of convolution type (z-transform). [SNIP] The general tool
   covers geometric kernels. No Ricker instance was seen.

### (c) Does the published formula reproduce the number?
Eliminate M from the linearisation:

δM_n = −(δx_{n+1} − δx_n)/r, so δx_{n+1} = (1 + q − r(1−q)) δx_n − q δx_{n−1}.

This is an AR(2) with β1 = 1 + q − r(1−q) and β2 = −q. The AR(2) (Jury/Royama) period-2 edge is 1 + β1 − β2 = 0:

1 + 1 + q − r(1−q) + q = 0, so **r = 2(1+q)/(1−q) = 6** at q = 0.5.

The other edges: 1 − β1 − β2 = r(1−q) > 0 always, and |β2| = q < 1 always. So the flip is the only way to lose stability. This
agrees with section 0. The general theorem therefore reproduces the number exactly once the model is written down. Levin–May, the
nearest classical population result, does not: it is a different kernel, with threshold 1 and Neimark–Sacker.

### (d) Verdict: **PARTIAL**
I found no paper stating the Ricker map with an exponentially smoothed (EWMA) density in the exponent, or the threshold
2(1+q)/(1−q). The result is an immediate textbook consequence (two lines) of the AR(2)/Jury stability triangle. Its qualitative
content, that averaging the feedback over past values while keeping weight on the present stabilises a flip, is known in the
cobweb and "maps with memory" literature (Claim 1 sources). So it is not mathematically novel, but I did not find this exact model
and formula stated. Streipert (2024) and Elaydi's geometric-kernel examples were not read in full.

---

## Claim 3: Lotka–Volterra with predators responding to exponentially remembered prey; neutral centre becomes an unstable spiral

### (a) Queries run
1. WebSearch: `Lotka-Volterra predator prey distributed delay weak kernel exponential neutral center becomes unstable Cushing 1977 MacDonald 1978`
2. WebSearch: `"Volterra" predator-prey "no self-limitation" OR "without density dependence" time delay predator numerical response ...`
3. WebSearch: `"weak kernel" OR "weak generic kernel" Lotka-Volterra predator prey "linear chain trick" characteristic equation cubic unstable equilibrium`
4. WebSearch: `predator-prey "exponentially fading memory" OR "exponential memory kernel" Lotka-Volterra ... Routh-Hurwitz cubic`
5. WebSearch: `Farkas 1984 stable oscillations predator-prey time lag weak kernel a exp(-at) Hopf bifurcation ...`
6. WebSearch: `MacDonald 1976 "Time delay in prey-predator models" Mathematical Biosciences 28 abstract ...`
7. WebSearch: `May 1973 "Time-delay versus stability" Ecology ...`
8. WebSearch: `Volterra hereditary predator prey model delay destabilizes neutral cycles "Cushing" 1977 ...`
9. Crossref/OpenAlex/PubMed lookups for Cushing 1976, 1977; MacDonald 1976, 1977, 1978; Farkas 1984.
10. Full-text reads: Ruan 2009 MMNP (author PDF), arXiv:1701.04703, arXiv:2203.13192, arXiv:2509.18222.

### (b) Closest works
1. **Ruan S (2009).** On nonlinear dynamics of predator–prey models with discrete delay. *Math Model Nat Phenom* 4(2):140–188.
   doi:10.1051/mmnp/20094207. [FT] The survey writes the Volterra model with a distributed delay in the predator equation,
   ẋ = x[r1 − a11 x − a12 y], ẏ = y[−r2 + a21 ∫ G(t−s) x(s) ds] (its eq. 1.3). It says this model "has been studied extensively
   (see Cushing [24], MacDonald [65], Dai [28], Farkas et al. [35], Stépán [81], etc.) and it has been shown that the time delay
   in (1.3) will destabilize the otherwise stable equilibrium and cause fluctuations in the populations via Hopf bifurcations."
   It also says: "The first predator-prey model with (distributed) delay was proposed by Volterra [84]." **Claim 3 is (1.3) with
   a11 = 0 and a weak kernel G(s) = e^{−s/T}/T.**
2. **Cushing JM (1976).** Predator prey interactions with time delays. *J Math Biol* 3:369–380. doi:10.1007/BF00275066. [ABS]
   "unlike the classical, non-delay Volterra-Lotka model, if the carrying capacity of the prey is too large then this equilibrium
   becomes unstable." The claim is the infinite-carrying-capacity end of this statement.
3. **Cushing JM (1977).** *Integrodifferential Equations and Delay Models in Population Dynamics*, Lecture Notes in Biomathematics 20,
   Springer. doi:10.1007/978-3-642-93073-7. Not read (Springer blocked).
4. **MacDonald N (1976).** Time delay in prey–predator models. *Math Biosci* 28:321–330. doi:10.1016/0025-5564(76)90130-9;
   **(1977)** II. Bifurcation theory, *Math Biosci* 33:227–234; **(1978)** *Time Lags in Biological Models*, LN Biomath 27,
   doi:10.1007/978-3-642-93107-9. [SNIP] Volterra prey–predator with prey limited by carrying capacity and delay "an integral with
   the weight function a exp(−at)". It also says "Lotka-Volterra cycles are unstable, but the Lotka-Volterra model with limited prey
   population can yield a limit cycle when time delay is included." Full text was not read.
5. **Farkas M (1984).** Stable oscillations in a predator–prey model with time lag. *J Math Anal Appl* 102:175–188.
   doi:10.1016/0022-247X(84)90211-7. [SNIP] "The Lotka-Volterra model with a time delay in the interspecies interaction terms ... by
   an integral with the weight kernel a exp(−at). A supercritical Hopf bifurcation takes place at a certain value a0." It uses
   logistic prey.
6. **May RM (1973).** Time-delay versus stability in population models with two and three trophic levels. *Ecology* 54:315–325.
   doi:10.2307/1934339. [SNIP] A delayed stabilising feedback gives instability. Background only.
7. **Volterra V (1931),** *Leçons sur la théorie mathématique de la lutte pour la vie*: the hereditary predator–prey model. Not read.

### (c) Does the published formula reproduce the number?
This is derived here from the model class above; the source papers were not read for this step. Linearise (1.3) with the weak
kernel at (x*, y*):

T λ³ + (1 + a11 x* T) λ² + a11 x* λ + a12 a21 x* y* = 0.

Routh–Hurwitz requires every coefficient to be positive and (1 + a11 x* T)·a11 x* > T·a12 a21 x* y*. This is the Hopf condition
that the Farkas/MacDonald a0 corresponds to [structure MEM; I did not read their exact formula]. At a11 = 0, the claim's model,
the λ coefficient vanishes. The equilibrium is then unstable for **every** T > 0, whatever the other parameters are.

With the claim's parameters (b x* = 1, d y* = 0.5, T = 1): λ³ + λ² + 0.5 = 0, with roots 0.148578 ± 0.602813i and −1.297157.
This reproduces +0.14858 ± 0.60281i. The qualitative result (destabilisation) is classical. The specific eigenvalue is just this
cubic evaluated at the chosen parameters.

### (d) Verdict: **FOUND**
The qualitative result is classical: a distributed delay in the predator's response to prey destabilises the Volterra equilibrium.
I read this in Ruan 2009's survey (full text), and Cushing 1976 states it in the abstract (large carrying capacity limit). The weak
exponential kernel is the standard case in MacDonald 1976/1978 and Farkas 1984. Claim 3 is the a11 = 0 corner of that model. The
numerical eigenvalue is new only as a number and has no independent content. Caveat: I did not read a source sentence stating
"a11 = 0 with a weak kernel gives an unstable spiral for all T". The unconditional statement comes from the Routh–Hurwitz step
above, applied to the published model class.

---

## Unverified items (mark before any use)
- The Levin–May stability bound formula [MEM].
- The exact equations in Fox 2002, Otani–Gilmour 1997, Watanabe–Koller 2002, Cushing 1977, MacDonald 1976/1978, Farkas 1984
  (abstracts or snippets only).
- Nerlove 1958's original text. The equation was read in Poitras 2023; the sign convention was reconstructed from PDF glyphs.
- Royama's AR(2) triangle, cited from standard AR(2) theory, not from Royama's text.
- Streipert 2024 (SSRN) was not read and may contain a close variant of Claim 2.
