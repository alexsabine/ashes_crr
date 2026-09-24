# Prior-art check: three "social" claims (SIR with remembered prevalence, Bass with fading word of mouth, OV traffic with remembered headway)

Date of check: 2026-09-24. Checked by: Claude (subagent). Access: EuropePMC REST (full-text XML where open access), arXiv abstract pages and PDFs,
Crossref API, OpenAlex API (citing-works listing), WebSearch. ScienceDirect, PMC (ncbi) and the tau.ac.il host were blocked by the egress
proxy. Semantic Scholar returned HTTP 429. So every Elsevier paper below was seen **by title/metadata only**, unless marked otherwise.

## Numerical re-check of the claims (my own run, not literature)

The script I ran is given below. I ran it with the repo's `uv` environment; the output was not committed.
```
SIR I0=1e-5: peak I (instantaneous) 0.0313551, (memory T=10) 0.0415020, ratio 1.32361   (I0=1e-4: 0.0313573 / 0.0415079, ratio 1.32371)
Bass (p=0.03,q=0.38) peak adopted fraction: kappa=0 0.4605 (t=6.19); 0.1 0.3981 (t=6.12); 0.3 0.2651 (t=5.19); 1 0.0863 (t=2.35)
OV + exponential headway memory, a=1, T=0.5: numerical threshold over all wavenumbers 0.333334; closed form a/(2(1+aT)) = 1/3 = 0.333333
```
- Claim 1 numbers match to within the effect of the unstated initial prevalence I0.
- Claim 2 numbers match to 4 decimals, and the peak does come earlier in time.
- Claim 3's "0.3335" is really 1/3 = 0.33333…. The long-wave mode is the one that goes unstable first, so the threshold is exactly a/(2(1+aT)).
  The quoted 0.3335 is off in the 4th decimal, probably from grid resolution.

```python
# script used (scipy solve_ivp, rtol 1e-10/1e-11)
# SIR: S'=-bSI, I'=bSI-0.1I, P'=(I-P)/10, b=0.3/(1+50*Pe), Pe = I (standard) or P (memory)
# Bass-with-fading-WOM: F'=(1-F)(p+qA), A'=F'-kappa*A  (A = age-weighted adoptions, exp(-kappa*age))
# OV: lambda(lambda+a)(1+lambda T) = a f (e^{i theta}-1); bisect f on max Re(lambda) over theta in (0,pi]
```

---

## Claim 1 — SIR with contact rate beta0/(1+kP), P = I or exponentially remembered prevalence (T = 10 d); memory raises the peak (0.041501 vs 0.031357)

### (a) Queries
- WebSearch: "d'Onofrio Manfredi information-related changes in contact patterns oscillations endemic prevalence information index exponential memory".
- WebSearch: "SIR epidemic peak prevalence delayed awareness memory kernel versus instantaneous information higher peak behavioural response".
- WebSearch: "\"information index\" epidemic \"peak\" memory \"fading memory\" SIR contact rate comparison instantaneous information".
- WebSearch: "Weitz 2020 PNAS awareness-driven behavior changes … short-term long-term awareness delay".
- EuropePMC: `"information index" AND (peak) AND (memory OR delay) AND (SIR OR epidemic)` (22 hits, all screened by title/abstract), plus title look-ups for each named paper.
- Full-text XML read (EuropePMC) for Ochab et al. 2023, Weitz et al. 2020 and Buonomo & Della Marca 2020. The arXiv abstract was read for Andò et al. 2025/2026.

### (b) Closest works
1. **Ochab M, Manfredi P, Puszynski K, d'Onofrio A (2023). "Multiple epidemic waves as the outcome of stochastic SIR epidemics with behavioral responses: a hybrid modeling approach." *Nonlinear Dynamics* 111:887–926. DOI 10.1007/s11071-022-07317-6 (PMC8923600). FULL TEXT read.**
   - Model: the Capasso–Serio epidemic SIR (μ = 0 variant of their eqs. 3–4), S' = −β(M) I S/N and I' = β(M) I S/N − γI.
   - Transmission: "β(M) = β0 M50^p/(M50^p + M^p)". For p = 1 this is exactly β0/(1 + M/M50), i.e. β0/(1 + kP).
   - Information index: M(t) = ∫ g(I(t−q)) K(q) dq with g(I) = kI.
   - Kernels: "The memoryless case K(q) = δ(q)" and "The exponentially fading memory kernel (EFK): K(q) = a Exp(−a q) … M′(t) = a(g(I) − M)", i.e. T = 1/a.
   - Delays studied: "a = 0.1/day and a = 0.05/day, corresponding to an average response delay of 10 and 20 days". So T = 10 d is one of their two cases.
   - Result quoted verbatim (stochastic simulations, first-peak prevalence, EFK): "Obviously, the larger the delay in the behavioral response, the larger the expected magnitude at the first peak."
   - They also state that "We assessed the effects of a delayed behavioral response in both the stochastic and in the deterministic case (see Appendix)". The memoryless deterministic and stochastic cases are shown (their Figs. 2–7, 18–19).
   - Their parameters are BRN ∈ {2, 15} (not R0 = 3), and results are given as PDFs and figures. The specific numbers 0.0415/0.0314 do not appear.
2. **Buonomo B, Della Marca R (2020). "Effects of information-induced behavioural changes during the COVID-19 lockdowns: the case of Italy." *R. Soc. Open Sci.* 7:201635. DOI 10.1098/rsos.201635. FULL TEXT read.**
   - Model: SEIR-like, with contact and quarantine rates depending on an information index with an exponential kernel of mean delay T_a = 1/a.
   - Quote: cumulative incidence, max(I_s) and deaths "increase … inversely to the information delay T_a: they reach the minimum for k = 1 and T_a = 1 day".
   - Their Table 3 gives max(I_s): 3.10e4 at T_a = 1 d, 3.45e4 at 3 d and 5.70e4 at 60 d (with a different k at 60 d). Direction: a longer memory delay gives a higher peak of the severe-infectious class.
   - They also report that the quarantine peak max(Q) is non-monotone in T_a.
3. **Weitz JS, Park SW, Eksin C, Dushoff J (2020). "Awareness-driven behavior changes can shift the shape of epidemics away from peaks and toward plateaus, shoulders, and oscillations." *PNAS* 117(51):32764–32771. DOI 10.1073/pnas.2009911117. FULL TEXT read.**
   - Model: SEIR with β/(1 + (δ/δc)^k + (D/Dc)^k). δ is the current death rate, which lags infection through an exponential hospital stage of mean 7–28 d. D is cumulative deaths ("long-term awareness").
   - Quote: "infections can overshoot the expected plateau given that awareness is driven by fatalities which are offset with respect to new infections".
   - Quote: increasing the case-to-death lag T_H from 7 to 28 d gives "increasing magnitude of oscillations as T_H increases".
   - This is a delayed signal rather than an exponentially averaged prevalence, and there is no explicit peak-size comparison against an instantaneous response.
4. **d'Onofrio A, Manfredi P (2009). "Information-related changes in contact patterns may trigger oscillations in the endemic prevalence of infectious diseases." *J. Theor. Biol.* 256:473–478. DOI 10.1016/j.jtbi.2008.10.005 (arXiv 1309.3327). Abstract only.**
   - This is the origin of β(M) with a memory kernel. It is endemic (μ > 0), and its result is oscillations and a Hopf bifurcation, not peak size.
5. Andò A, De Reggi S, Scarabel F, Vermiglio R, Wu J. "Behavior-induced oscillations in epidemic outbreaks with distributed memory…" arXiv 2511.21199 (2025-11-26); *Math. Biosci. Eng.* 2026, DOI 10.3934/mbe.2026004. Abstract only.
   - Gamma kernels, outbreak with negligible susceptible depletion. It says it gives "insight into how the period and peak of epidemic waves depend on the shape of the memory kernel". There is no SIR peak comparison in the abstract.
6. Buonomo B, Messina E, Panico C, Vecchio A (2024). *J. Math. Biol.* DOI 10.1007/s00285-024-02172-y. Abstract only: stability and oscillations under Erlang kernels.
7. Buonomo B (2020), SIRI with information-dependent vaccination, *Ricerche di Matematica* (PMC7144546). Abstract only: "cumulative incidence may be significantly reduced when … the information delay is short".
8. Background works, abstract only; none of them compares peak size under instantaneous vs remembered awareness in the abstract:
   - d'Onofrio, Manfredi & Salinelli (2007) *TPB* 71:301, DOI 10.1016/j.tpb.2007.01.001 (vaccination, not contact).
   - Buonomo, d'Onofrio & Lacitignola (2008) *Math. Biosci.*, DOI 10.1016/j.mbs.2008.07.011 (global stability, vaccination).
   - Funk, Salathé & Jansen (2010) *J R Soc Interface*, DOI 10.1098/rsif.2010.0142 (review).
   - Epstein et al. (2008) *PLoS ONE*, DOI 10.1371/journal.pone.0003955 (coupled fear/disease contagion).

### (c) Number and direction
- Direction (a delayed or remembered response gives a higher first peak): **reproduced** in the same model family.
  - Ochab et al. 2023 state it for exactly the claim's β0/(1 + kM) with an exponentially fading M, including a 10-day memory.
  - Buonomo & Della Marca 2020 show it in an SEIR variant.
  - Weitz 2020 gives the same "overshoot" mechanism.
- The specific numbers (0.041501 vs 0.031357, ratio 1.3235 at R0 = 3, k = 50, T = 10) are **not in print**. The literature uses other R0 and k values and reports stochastic PDFs.

### (d) Verdict: **FOUND** for the direction; the specific numbers are not published
- The same model structure (Capasso–Serio SIR, p = 1 information index, exponentially fading kernel, memoryless comparison case) and the same qualitative result are in Ochab et al. 2023.
- Caveats:
  - Their statement is made for stochastic simulations, comparing 10- vs 20-day delays.
  - An explicit deterministic memoryless-vs-memory peak table was not seen: their deterministic appendix figures were read by caption only.

---

## Claim 2 — Bass diffusion where imitation comes from exponentially age-weighted adoptions (rate kappa); the Bass plot bends below p+qF, the peak comes at a lower fraction and earlier, q > p is unchanged

### (a) Queries
- WebSearch: "Fibich Bass-SIR model diffusion of new products social networks Physical Review E 2016".
- WebSearch: "Bass diffusion model word-of-mouth influence decays with time since adoption \"recent adopters\" active adopters peak earlier".
- WebSearch: "Bass model \"limited duration\" OR \"time-limited\" word of mouth adopters stop talking diffusion peak lower adoption fraction".
- WebSearch: "Bass-SIR model peak sales time adoption fraction at peak recovery rate r".
- WebSearch: "Dodson Muller 1978 … forgetting active adopters".
- WebSearch: "Libai Muller Peres 2009 diffusion of services disadoption word of mouth current users only".
- OpenAlex: all 63 works citing Fibich 2016 (W2370824679), screened by title.
- arXiv full texts read: 1605.03615 (Fibich PRE), 1701.01669v2 (Fibich SIAP) and 2602.19488 (2026 survey of Bass-type models).
- Wharton-hosted PDF of Libai et al. 2009 read.

### (b) Closest works
1. **Fibich G (2016). "Bass-SIR model for diffusion of new products in social networks." *Phys. Rev. E* 94:032305. DOI 10.1103/PhysRevE.94.032305; arXiv 1605.03615v1 (2016-05-11). FULL TEXT (arXiv v1) read.**
   - Adopters are "contagious" and "recover" at rate r.
   - On a complete network, "the aggregate (macroscopic) diffusion dynamics is governed by S′(t) = −S(p+qI), I′(t) = S(p+qI) − rI, R′(t) = rI" (eq. 2), with f = I + R = 1 − S.
   - Solving I′ = f′ − rI with I(0) = 0 gives I(t) = ∫ f′(s) e^{−r(t−s)} ds. That is exactly the claim's exponentially age-weighted adoptions, with kappa = r. **The model is identical.**
   - Results stated: "As r increases, internal influences persist for shorter times, hence diffusion becomes slower. Therefore, f is monotonically decreasing in r". For r ≫ q, f ≈ 1 − e^{−pt}.
   - Nothing is said about the Bass plot, the adopted fraction at peak sales, or the peak timing.
2. **Fibich G (2017). "Diffusion of new products with recovering consumers." *SIAM J. Appl. Math.* DOI 10.1137/17M1112546; arXiv 1701.01669v2 (2017-05-19). FULL TEXT read.**
   - Same aggregate model (its eq. 7.2 with r_nl = 0).
   - Shows f is monotonically decreasing in r (3.5a), that the effect depends on r/q, and that the motivation is empirical: Graziano & Gillingham, "this effect of nearby systems diminished with time".
   - No peak-location or Bass-plot result.
3. **Libai B, Muller E, Peres R (2009). "The diffusion of services." *J. Marketing Research* 46(2):163–175. DOI 10.1509/jmkr.46.2.163. FULL TEXT read.**
   - Model: dN/dt = [p(m−N) + qN(m−N)/m] − δN.
   - Only retained customers spread word of mouth, and "disadopters return to the market potential". This is a different state structure: disadopters can re-adopt.
   - The solution is Bass-form with p/Δ, q/Δ and m/Δ. This is a close variant, not the claim's model.
4. Background, abstract/metadata only:
   - Dodson & Muller (1978) *Mgmt Sci* 24(15):1568, DOI 10.1287/mnsc.24.15.1568.
   - Easingwood, Mahajan & Muller (1983) NUI model (a non-uniform influence qF^δ that also bends the Bass plot; from memory, not re-read).
   - Peres, Muller & Mahajan (2010) *IJRM* review (not re-read).
   - Langrené et al. (2026) survey arXiv 2602.19488 (full text scanned): no Bass-SIR, fading word-of-mouth or memory section.
   - Scialla et al. (2026) arXiv 2608.15706: memory-window agent model, a different structure.
   - "Fractional Bass" models: not pursued beyond the search listing.

### (c) Number and direction
- The model is identical to Fibich's complete-network Bass-SIR, and Fibich gives the direction "slower diffusion" (lower f(t) at every t).
- The claim's specific results were not found in the texts read:
  1. the hazard f′/(1−f) = p + qI lies below p + qf;
  2. the peak fraction falls from 0.4606 to 0.3981, 0.2651 and 0.0863;
  3. the peak comes earlier in time;
  4. the interior-peak condition q > p is unchanged.
- (1) and (4) follow in one line from Fibich's eq. (2):
  - I ≤ f, so the hazard sits below the line.
  - At t = 0 the sales rate is s = p and s′(0) = −p² + qI′(0) = p(q − p), independent of r.
- (2) and (3) need integration. My numerics reproduce the claim's values; see the top of this file.
- The baseline 0.4606 = (q−p)/(2q) = 0.35/0.76 = 0.46053 is the standard Bass result. Note that the exact value rounds to 0.4605.

### (d) Verdict: **PARTIAL**
- The same model is published (Fibich 2016 PRE eq. 2; Fibich 2017 SIAP), along with the direction "diffusion slower, monotone in r".
- The peak-location, peak-timing and Bass-plot statements were not found. They are elementary consequences of the published model, so they add little.

---

## Claim 3 — OV model, driver responds to exponentially remembered headway (T); string-instability threshold falls from a/2 to 0.3335 at a = 1, T = 0.5

### (a) Queries
- WebSearch: "Stability of traffic flow behavior with distributed delays modeling the memory effects of the drivers Sipahi Atay Niculescu".
- WebSearch: "Cao 2015 … driver's sensory memory"; "Yu Shi 2015 … headway changes with memory".
- WebSearch: "optimal velocity model distributed delay exponential kernel memory headway linear stability condition V'(h) < a/(2(1+a tau))".
- WebSearch: "\"optimal velocity\" car-following \"distributed delay\" gamma kernel string stability memory drivers".
- WebSearch: "Bando … 1998 Analysis of optimal velocity model with explicit delay"; "Orosz Wilson Stépán Traffic jams: dynamics and control …".
- WebSearch: "Ngoduy 2015 linear stability … multi-anticipative … time delays"; "Density waves in a traffic flow model with reaction-time delay".
- WebSearch: "car-following model driver memory exponentially weighted past headway".
- Crossref look-ups for each title.
- Full texts read:
  - Bando et al. 1998 (arXiv patt-sol/9805002).
  - Orosz, Wilson & Krauskopf 2004 PRE (author PDF).
  - Orosz, Wilson & Stépán 2010 (BME-hosted PDF).
  - Chen, Liu, Ngoduy & Shi 2016 (White Rose accepted version).
  - Sun et al. arXiv 1803.09850.

### (b) Closest works
1. **Bando M, Hasebe K, Nakanishi K, Nakayama A (1998). "Analysis of optimal velocity model with explicit delay." *Phys. Rev. E* 58:5429. arXiv patt-sol/9805002. FULL TEXT read.**
   - Discrete delay τ. Critical curves are given graphically for aτ = 0, 0.2, 0.4, and "unstable modes increase as the explicit delay time τ becomes large".
   - Verbatim: "an analytical relation has not been clarified yet." No closed-form threshold is given.
2. **Orosz G, Wilson RE, Krauskopf B (2004). "Global bifurcation investigation of an optimal velocity traffic model with driver reaction time." *Phys. Rev. E* 70:026207. FULL TEXT read.**
   - Characteristic equation [λ² + aλ + aV′e^{−λ}]^n − [aV′e^{−λ}]^n = 0 (time rescaled so that τ = 1).
   - Neutral curves: V′(h*) = ω/(2cos(ω − kπ/n) sin(kπ/n)) and a = −ω cot(ω − kπ/n) (eq. 19).
   - Long-wave limit (my derivation from their eq. 19): with x = kπ/n → 0 and ω = cx, a → c/(1−c) and V′ → c/2. This gives **V′_c = a/(2(1+aτ))** in dimensional form. The paper does not state it in this form.
3. **Chen J, Liu R, Ngoduy D, Shi Z (2016). "A new multi-anticipative car-following model with consideration of the desired following distance." *Nonlinear Dyn.* 85(4):2705–2717. DOI 10.1007/s11071-016-2856-4. FULL TEXT (accepted version) read.**
   - Model (2): OV with reaction delay t_d on the headway.
   - Long-wave coefficients: "z1 = [αV′(se) + β]/(α + βT)" and "z2 = [−z1² + α Σ p_j V′(se)(j/2 − t_d z1) + β Σ q_j(j/2 − t_d z1)]/(α + βT)"; stable iff z2 > 0.
   - With β = 0, m = 1: z2 > 0 ⇔ α/2 > V′(1 + α t_d) ⇔ **V′ < α/(2(1 + α t_d))**. At α = 1, t_d = 0.5 this gives V′_c = 1/(2·1.5) = **0.33333**.
   - They attribute the delayed multi-anticipative OV to Hu et al. and the general delayed analysis to Ngoduy (2015, *CNSNS* 22:420; not read).
   - Yu L, Li T, Shi ZK (2010) *Physica A* 389:2607, DOI 10.1016/j.physa.2010.03.009 ("OV with reaction-time delay … stability condition obtained by linear stability theory") very likely states the same formula. **Unverified: ScienceDirect was blocked.**
4. **Sipahi R, Atay FM, Niculescu S-I (2007). "Stability of traffic flow behavior with distributed delays modeling the memory effects of the drivers." *SIAM J. Appl. Math.* 68(3):738–759. DOI 10.1137/060673813. Abstract only.**
   - "introducing a distribution of delays … memory capabilities of the drivers … exact stability regions in the parameter space of some realistic delay distributions". It uses gamma-type kernels.
   - The model is a constant-time-headway strategy, not the OV model. Their analysis is of asymptotic stability of spacing propagation.
   - Follow-ups:
     - Sipahi & Niculescu (2010) *Phil. Trans. R. Soc. A* 368:4563, DOI 10.1098/rsta.2010.0127 ("distributed delays with a gap"; abstract only).
     - Michiels, Morărescu & Niculescu (2009) *SIAM J. Control Optim.* 48(1):77–101 (γ-distribution with a gap; abstract only).
     - Sipahi, Niculescu & Atay (2024) SpringerBrief ch. 5, "Linear Stability of Traffic Flow Models with Distributed Delays", DOI 10.1007/978-3-031-58164-9_5 (not accessible; **unverified** whether it treats OV with an exponential kernel).
5. Other "memory" OV and car-following variants. All were seen by title only (ScienceDirect blocked). They appear to use discrete-lag memory terms such as h(t) − h(t−τ), not an exponential filter of the headway. **Unverified.**
   - Yu & Shi (2015) *Physica A* 421:1, DOI 10.1016/j.physa.2014.11.008 ("headway changes with memory").
   - Cao (2015) *Physica A* 427:218 ("driver's sensory memory"; per search snippet, "the stability region decreases when the driver's sensory buffer time increases").
   - Cao (2020) *Physica A*, DOI 10.1016/j.physa.2019.122903 ("headway memory and evolution trend").
   - Liu, Shi & Ai (2017) *CNSNS*, DOI 10.1016/j.cnsns.2016.11.007 ("short-term driving memory"; claimed to enhance stability).
6. Orosz, Wilson & Stépán (2010) *Phil. Trans. R. Soc. A* 368:4455, DOI 10.1098/rsta.2010.0205. FULL TEXT read.
   - Gives the no-delay long-wave condition F < ½(2G+H)H, i.e. V′ < a/2 for OV.
   - Notes that human memory can be modelled "by using distributed delays, as in Sipahi & Niculescu (2010)".
   - No closed form for an exponential kernel.

### (c) Number and direction
- Direction (memory or delay lowers the threshold): known since Bando 1998 (graphically) and in all the delay papers.
- Closed form: for a discrete delay τ the published long-wave boundary is V′_c = a/(2(1+aτ)) (Chen et al. 2016 eq. 13 with β = 0, m = 1; also derivable from Orosz et al. 2004 eq. 19).
- For the claim's exponential kernel, the linearised dispersion relation is λ(λ+a)(1+λT) = aV′(e^{iθ}−1).
  - O(θ) gives λ1 = V′. At O(θ²), a·λ2 = (1+aT)V′² − aV′/2.
  - So the long-wave threshold is **V′_c = a/(2(1+aT))**. At a = 1, T = 0.5 this is **1/3 = 0.33333**.
- This is the same formula as the discrete delay, because only the kernel's mean enters at O(θ²). Any delay kernel with mean T gives the same long-wave threshold.
- My full-wavenumber scan gives 0.333334, so the long-wave mode is the critical one.
- The claim's "0.3335" is therefore 1/3 up to numerical error. The published discrete-delay formula at τ = T reproduces it exactly.

### (d) Verdict: **PARTIAL** (leaning FOUND)
- Published: a closed-form threshold a/(2(1+aτ)) for the OV model with reaction delay, which gives the claimed value (1/3) at τ = T = 0.5. Published separately: distributed-delay ("driver memory") car-following models with gamma and exponential kernels (Sipahi et al. 2007 and later).
- Not located: a paper stating the threshold for the OV model with an exponential kernel on the headway specifically. Such a result would be a one-line corollary: the long-wave threshold depends only on the kernel's mean.
- Unverified: whether Sipahi, Niculescu & Atay 2024 (ch. 5), Ngoduy 2015 or Yu, Li & Shi 2010 already state the kernel-mean corollary.

---

## Summary table
| Claim | Closest prior art | Same model? | Same result? | Verdict |
|---|---|---|---|---|
| 1 SIR + remembered prevalence gives a higher peak | Ochab, Manfredi, Puszynski & d'Onofrio 2023 *Nonlinear Dyn* 111:887 (doi 10.1007/s11071-022-07317-6); Buonomo & Della Marca 2020 *RSOS*; Weitz et al. 2020 *PNAS* | Yes (β0 M50/(M50+M), exponential kernel, T = 10 d) | Direction yes (quoted); numbers no | **FOUND** (direction) |
| 2 Bass with fading word of mouth | Fibich 2016 *PRE* 94:032305 (Bass-SIR); Fibich 2017 *SIAP*; Libai, Muller & Peres 2009 *JMR* (variant) | Yes (identical aggregate ODE) | Slower diffusion yes; peak-fraction, peak-timing and Bass-plot statements not found | **PARTIAL** |
| 3 OV + remembered headway | Bando et al. 1998 *PRE* 58:5429; Orosz, Wilson & Krauskopf 2004 *PRE* 70:026207; Chen, Liu, Ngoduy & Shi 2016 *Nonlinear Dyn* 85:2705; Sipahi, Atay & Niculescu 2007 *SIAP* 68:738 | Discrete-delay OV yes; exponential kernel on OV headway not located | Threshold value 1/3 reproduced exactly by the published a/(2(1+aτ)); claimed 0.3335 is 1/3 up to numerical error | **PARTIAL** (leaning FOUND) |
