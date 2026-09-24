# Prior-art check: the "regeneration law" alpha* = K(v) = (v/2)(sqrt(v^2+4) - v)

Checked 2026-09-24. Access: Crossref REST API, Semantic Scholar API (rate-limited), Europe PMC REST (abstracts and
full-text XML), NCBI E-utilities (PMC full text), arXiv abstract pages, NBER/author-hosted PDFs (text extracted with pypdf),
and the WebSearch tool. JSTOR, Taylor & Francis (403), Wiley and APS full texts were **not** reachable. So Muth (1960),
Stein (1989), Fairhall et al. (2001), Behrens et al. (2007) and Nelson & Foster (1994) are cited here from abstracts or
secondary sources, and each place says so. "Full text" below means I read the passage myself in the downloaded
document. "Abstract" means the publisher/PubMed/Crossref abstract. "Snippet" means a search-engine summary, which is
weaker evidence. Volume, issue and page numbers of the journal items were checked against Crossref
metadata on 2026-09-24.

The law under test has four parts. They need to be kept apart because the literature treats them differently:

- **(L1) Formula.** K(v) is the steady-state (filtered) Kalman gain of a random walk observed in white noise. v is
  sd(drift)/sd(noise).
- **(L2) Optimality.** An EWMA with that weight is the minimum-MSE forecaster for that process.
- **(L3) Descriptive claim for inferential agents.** Real forecasters, animals and neurons actually use alpha = K(v).
- **(L4) Universality.** Every system whose state is an EWMA of its inputs, *including non-inferential physical
  systems*, has alpha = K(v) with v taken from its environment. There is no free parameter. The denominator of v also
  includes the system's own reporting/quantisation resolution.

A useful identity (own algebra, easy to check): K(v) is the positive root of K^2 + v^2 K - v^2 = 0. Equivalently
**v^2 = K^2/(1-K)**. Any fitted EWMA weight alpha therefore has an *implied* v = alpha/sqrt(1-alpha). So every
estimated gain can be turned into the v it would need. It can be tested only against an *independently measured* v.

---

## 1. Muth (1960): EWMA optimal for random walk plus noise; the gain vs signal-to-noise ratio

**Queries run.** Crossref `Muth 1960 optimal properties exponentially weighted forecasts`. WebSearch `Muth 1960 optimal
properties exponentially weighted forecasts weight signal-to-noise ratio random walk plus noise formula`; `Muth (1960)
adaptive expectations Kalman gain "signal-to-noise ratio" ...`; `local level model steady state Kalman gain
signal-to-noise ratio q ... Harvey`; `Kalata 1984 tracking index alpha filter ...`. Semantic Scholar DOI lookup (abstract
elided by publisher; OA status CLOSED).

**Closest works.**
- Muth, J. F. (1960). Optimal properties of exponentially weighted forecasts. *JASA* 55(290), 299-306.
  DOI 10.1080/01621459.1960.10482064. Corrigenda: *JASA* 1962, DOI 10.2307/2281826. **Full text not reachable** (T&F 403,
  JSTOR paywalled). A search snippet summarising the paper says: "The exponentially weighted average can be interpreted
  as the expected value of a time series made up of two kinds of random components: one lasting a single time period
  (transitory) and the other lasting through all subsequent periods (permanent). Such a time series may be regarded as a
  random walk with 'noise' superimposed." (snippet; this is the paper's abstract as indexed.)
- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *J. Basic Eng.* 82, 35-45.
  DOI 10.1115/1.3662552.
- McCulloch, J. H. "Adaptive Least Squares: Recursive Least Squares with Constant Noise-to-Signal Ratio". Working
  paper, version dated July 20, 2026, https://www.asc.ohio-state.edu/mcculloch.2/papers/ALS/ALS.pdf (**full text**). It
  states the relation explicitly. The model is y_t = mu_t + eps_t, mu_t = mu_{t-1} + eta_t, with signal/noise variance
  ratio rho = sigma_eta^2/sigma_eps^2. Quote: "[the gain] is bounded below by its long-run value
  gamma_LR = 1/(1/2 + sqrt(1/4 + 1/rho)) (7), which is the unique positive root of the quadratic equation
  gamma_LR^2 + rho gamma_LR - rho [= 0] ... The Cagan/Muth constant gain AE formula (1) is therefore valid only in this
  limit, and only if the limiting long run gain gamma_LR is determined by (7), with rho appropriately estimated from the
  data." Also: "Muth (1960) and Kalman (1960) independently demonstrated that (1) in fact gives the long-run behavior of
  the optimal signal-extraction forecast ... provided the long-run gain coefficient is computed as a certain function of
  the empirical noise/signal ratio. The gain coefficient is therefore not an arbitrary subjective learning parameter ...
  but rather should take on a specific value determined by the process itself." And: "Although Muth (1960) developed
  only the constant long-run gain coefficient ..."
- Koopman, S. J. (2011). *Introduction to Local Level Model and Kalman Filter*, lecture slides, and 2016 Aarhus slides
  (**full text**). They give the steady state: "P-bar = P-bar(1 - P-bar/(P-bar + sigma_eps^2)) + sigma_eta^2, which
  reduces to the quadratic x^2 - xq - q = 0, where x = P-bar/sigma_eps^2 and q = sigma_eta^2/sigma_eps^2, with solution
  P-bar = sigma_eps^2 (q + sqrt(q^2+4q))/2". Also "K_t -> P-bar/(P-bar + sigma_eps^2)", and the exercise "Show that the
  forecasts of the Kalman filter (in a steady state) are the same as those generated by the ... EWMA ... Derive the
  relationship between lambda and the signal-to-noise ratio q". The ARIMA(0,1,1) form is theta = (sqrt(q^2+4q) - 2 - q)/2.
- Harvey, A. C. (1989/1990). *Forecasting, Structural Time Series Models and the Kalman Filter*. CUP.
  DOI 10.1017/cbo9781107049994 (textbook source cited by both of the above; not opened).
- Shepherd, B. (2011). When are adaptive expectations rational? A generalization. MPRA 34644 (**full text**). It gives a
  Kalman-filter re-proof of Muth's result.
- Tracking-filter literature. Kalata, P. R. (1984). The tracking index: a generalized parameter for alpha-beta and
  alpha-beta-gamma target trackers. *IEEE TAES* 20(2), 174-182, DOI 10.1109/TAES.1984.310438. The "tracking index" is
  defined as process-noise sd over measurement-noise sd, which is the same dimensionless ratio as v. The Wikipedia
  "Alpha beta filter" page (last edit 5 Sep 2026) gives, for the one-state alpha filter, alpha = (-lambda^2 +
  sqrt(lambda^4 + 16 lambda^2))/8 with lambda = sigma_w T^2/sigma_v. With lambda = 2v this is algebraically the same as
  K(v), so the scaling convention differs by a factor of 2. I could **not** verify this against Kalata's full text.
  Treat it as unverified.

**Exact relation (own algebra, consistent with McCulloch eq. 7 and Koopman's steady state).** Let q = rho =
sigma_eta^2/sigma_eps^2 and v = sqrt(q). Then the Muth/Kalman steady-state weight on the newest observation is

  K = P-bar/(P-bar + sigma_eps^2) = (sqrt(q^2+4q) - q)/2 = (v/2)(sqrt(v^2+4) - v) = 1/(1/2 + sqrt(1/4 + 1/q)).

The EWMA memory (discount) is 1 - K = -theta (MA(1) coefficient). This is **exactly** the law's formula with v = sd of the
random-walk step / sd of the observation noise.

**Verdict for L1 + L2: FOUND.** The formula, its optimality for random walk plus noise, and its dependence on the
signal-to-noise ratio are textbook results (Muth 1960; Kalman 1960; Harvey 1989; tracking index, Kalata 1984). What is
**not** standard in the law is the proposed denominator "noise + the system's own reporting/quantisation resolution"
added as sds. The standard treatment adds quantisation as extra measurement-noise **variance** (about Delta^2/12,
Widrow & Kollar 2008, *Quantization Noise*, DOI 10.1017/cbo9780511754661), or treats it with a nonlinear quantised-
measurement filter (Curry 1970, MIT Press, DOI 10.7551/mitpress/2837.001.0001; Sviestins & Wigren 2000, *IEEE TAC*,
DOI 10.1109/9.847118). Adding sds rather than variances is a departure from optimal filtering, not a restatement of it.

---

## 2. Do forecasters' and households' gains equal the optimal (Muth/Kalman) gain?

**Queries run.** Crossref: `Coibion Gorodnichenko What can survey forecasts tell us about information rigidities`;
`Coibion Gorodnichenko Information rigidity and the expectations formation process`; `Mankiw Reis sticky information
versus sticky prices`; `Carroll macroeconomic expectations of households and professional forecasters`; `Malmendier Nagel
learning from inflation experiences`; `Mankiw Reis Wolfers disagreement about inflation expectations`; `Bordalo
Gennaioli Ma Shleifer Overreaction in macroeconomic expectations`; `Afrouzi ... Overreaction in expectations`; `Massey Wu
Detecting regime shifts`; `Kohlhas Walther Asymmetric attention`. WebSearch: `Malmendier Nagel ... gain parameter theta
3.044 constant gain 0.0180`; `Carroll 2003 epidemiological expectations ... lambda 0.25 per quarter`. Full texts from
NBER w16537 and w14586, the author copies of Carroll (QJE 2003) and Malmendier-Nagel, and Reis's copy of MRW (2003).

**Works and numbers.**
- Coibion, O. & Gorodnichenko, Y. (2015). Information rigidity and the expectations formation process: a simple
  framework and new facts. *AER* 105(8), 2644-78. DOI 10.1257/aer.20110306 (NBER w16537, DOI 10.3386/w16537,
  **full text** of the WP). Under noisy information, mean forecast error = ((1-G)/G) x mean revision, "where G is the
  Kalman gain which represents the relative weight placed on new information relative to previous forecasts". Estimates:
  "From 1969-2010, we find beta-hat = 1.23 (0.50) ... [lambda-hat ~ 0.55] ... agents put a weight of less than one-half
  on new information and more than one-half on their previous forecasts" (implied G ~ 0.45 per quarter, SPF inflation).
  Pooled over SPF variables and horizons: "new information moves forecasts by 70% of what it would be under
  full-information" (G ~ 0.7). Pooled since 1981: "a weight of 60% being assigned to new information".
  **Closest test to L3.** They regress country x variable rigidities on persistence and a measured noise-signal ratio
  kappa (sd of data revisions, or of forecast disagreement, over sd of innovations). Quote: "imperfect information models
  imply that the degree of information rigidity should be decreasing in the persistence of the series being forecasted
  and increasing in the amount of noise in the signal ... When using the noise-signal ratio measured using data-revisions
  ... the coefficient is positive, as expected, but not significantly different from zero ... [robust S-regressions]
  point to a positive and statistically significant effect ... this simple specification can account for about 20-30
  percent of the heterogeneity in informational rigidities." That is a **directional** test (sign of the dependence on
  kappa). There is **no level test** of G = K(measured v).
- Coibion, O. & Gorodnichenko, Y. (2012). What can survey forecasts tell us about information rigidities? *JPE* 120(1),
  116-159. DOI 10.1086/665662 (NBER w14586, **full text**). Abstract: "mean forecasts fail to completely adjust on impact
  ... the half life of forecast errors is roughly between 6 months and a year."
- Mankiw, N. G. & Reis, R. (2002). Sticky information versus sticky prices. *QJE* 117(4), 1295-1328.
  DOI 10.1162/003355302320935034. Assumes an updating probability lambda = 0.25 per quarter (confirmed via Carroll's
  quote below). This is an **assumed** gain-like parameter, not derived from any signal-to-noise ratio.
- Mankiw, Reis & Wolfers (2003). Disagreement about inflation expectations. *NBER Macro Annual* 18,
  DOI 10.1086/ma.18.3585256 (**full text**): "For the Livingston Survey, the optimal lambda is 0.10, implying that the
  professional economists surveyed are updating their expectations about every 10 months, on average. For the Michigan
  series, the value of lambda that maximizes the correlation ... is 0.08, implying that the general public updates their
  expectations on average every 12.5 months." ("Optimal" here means best fit to dispersion, not MSE-optimal.)
- Carroll, C. D. (2003). Macroeconomic expectations of households and professional forecasters. *QJE* 118(1), 269-298.
  DOI 10.1162/00335530360535207 (**full text**, author copy). Households' expectation is an EWMA of the professional
  (SPF) forecast. Quote: "The point estimate lambda = 0.27 is remarkably close to the value of 0.25 assumed by Mankiw and
  Reis ... in each quarter, only about one fourth of households have a completely up-to-date forecast". Also: "the
  typical household is estimated to update expectations roughly once a year". No comparison with an optimal Kalman gain.
- Malmendier, U. & Nagel, S. (2016). Learning from inflation experiences. *QJE* 131(1), 53-87. DOI 10.1093/qje/qjv037
  (**full text**, author copy). Decreasing gain gamma = theta/age: "we estimate a gain parameter theta of 3.044 (s.e.
  0.233)". Aggregate equivalent: "We use the constant gain for which the constant-gain algorithm minimizes the squared
  deviations from the average learning-from-experience weights. The result is a constant gain of gamma = 0.0180 [per
  quarter] ... virtually the same as the gain required to match aggregate expectations and macro time-series data. For
  example, Milani (2007) reports [gamma = 0.0183]". They compare with other *fitted* gains, **not** with a gain derived
  from inflation's signal-to-noise ratio. (Own arithmetic: the implied v for 0.018 is 0.018. For Carroll's 0.27 it is
  0.32. For CG's 0.45 it is 0.61.)
- Evidence that gains are **not** set by the environment's statistics:
  - Bordalo, Gennaioli, Ma & Shleifer (2020). Overreaction in macroeconomic expectations. *AER* 110(9), 2748-82.
    DOI 10.1257/aer.20181219 (abstract): "individual forecasters typically overreact to news, while consensus forecasts
    under-react relative to full-information rational expectations."
  - Afrouzi, Kwon, Landier, Ma & Thesmar (2023). Overreaction in expectations: evidence and theory. *QJE* 138(3), 1713-1764.
    DOI 10.1093/qje/qjad009 (abstract). This is a controlled experiment with a known process: "forecasts display
    significant overreaction to the most recent observation. Second, overreaction is stronger for less persistent
    processes."
  - Massey, C. & Wu, G. (2005). Detecting regime shifts: the causes of under- and overreaction. *Management Science*
    51(6), 932-947. DOI 10.1287/mnsc.1050.0386 (abstract): "System-neglect hypothesis: Individuals react primarily to the
    signals they observe and secondarily to the environmental system that produced the signal ... Underreaction is most
    common in unstable environments with precise signals, and overreaction is most common in stable environments with
    noisy signals." In the law's terms, human gains are **compressed** relative to K(v): too low at high v and too high
    at low v.

**Verdict for L3 in economics: PARTIAL.** The literature interprets forecaster rigidity *as* a Kalman gain (CG 2015) and
finds the directional dependence on a measured noise/signal ratio (weak, 20-30% of cross-sectional variance). It
estimates gains of about 0.45-0.7 per quarter (SPF), 0.27 per quarter (households vs SPF, Carroll), 0.08-0.10 per month
(MRW), and 0.018 per quarter (MN). No study I found tests whether the **level** of the fitted gain equals K(v) computed
from independently measured drift and noise sds. Where the process is controlled (Afrouzi et al. 2023; Massey & Wu 2005),
the gain departs systematically from the optimum. Individual forecasters overreact while consensus underreacts
(Bordalo et al. 2020). This evidence goes **against** L3 as a no-free-parameter law for human forecasters.

---

## 3. Volatility-tracking learning rates in humans/animals

**Queries run.** Crossref: `Behrens Woolrich Walton Rushworth learning the value of information in an uncertain world`;
`Nassar Wilson Heasly Gold approximately Bayesian delta-rule`; `Mathys Bayesian foundation for individual learning under
uncertainty`; `Daw Gershman Seymour Dayan Dolan model-based influences`. Europe PMC: `Do learning rates adapt to the
distribution of rewards`; `A model for learning based on the joint estimation of stochasticity and volatility`;
`Anxious individuals have difficulty learning the causal statistics of aversive environments`. Full text of Daw et al.
2011 (PMC3077926) and Browning et al. 2015 (PMC4644067) from Europe PMC. Behrens 2007 PDF: TLS failure and HTTP 503, so
abstract only.

**Works.**
- Behrens, Woolrich, Walton & Rushworth (2007). Learning the value of information in an uncertain world. *Nat.
  Neurosci.* 10(9), 1214-21. DOI 10.1038/nn1954 (abstract): "the weight given to decision outcomes should reflect their
  salience in predicting future outcomes, and this salience should be modulated by the volatility of the reward
  environment. We show that human subjects assess volatility in an optimal manner and adjust decision-making
  accordingly ... variations in this ACC signal across the population predict variations in subject learning rates."
- Nassar, Wilson, Heasly & Gold (2010). An approximately Bayesian delta-rule model explains the dynamics of belief
  updating in a changing environment. *J. Neurosci.* 30(37), 12366-78. DOI 10.1523/JNEUROSCI.0822-10.2010 (abstract):
  "the influence of an outcome depends on both the error made in predicting that outcome and the number of similar
  outcomes experienced previously ... the exact nature of these tendencies varies considerably across subjects ... A prior
  that quantifies the expected frequency of such environmental changes accounts for individual variability". The
  environment here is change-point, not random-walk, and the gain varies over time.
- Mathys, Daunizeau, Friston & Stephan (2011). A Bayesian foundation for individual learning under uncertainty. *Front.
  Hum. Neurosci.* 5:39. DOI 10.3389/fnhum.2011.00039 (abstract): the HGF "assumes Gaussian random walks of states at all
  but the first level ... The coupling between levels is controlled by parameters that shape the influence of uncertainty
  on learning in a subject-specific fashion". The model is built with **subject-specific free parameters** (kappa, omega,
  theta), which is the opposite of "no free parameter".
- Browning, Behrens, Jocham, O'Reilly & Bishop (2015). *Nat. Neurosci.* 18, 590-596. DOI 10.1038/nn.3961 (**full
  text**): "Participants with low levels of trait anxiety altered their learning rate between the stable and volatile
  blocks to an equivalent degree to the ideal Bayesian learner ... As trait anxiety levels increased, participants
  diverged increasingly from the optimal change in learning rate". So adaptation to volatility is individually variable.
- Piray, P. & Daw, N. D. (2021). A model for learning based on the joint estimation of stochasticity and volatility.
  *Nat. Commun.* 12, 6587. DOI 10.1038/s41467-021-26731-9 (abstract): "learning rates are jointly determined by the
  comparison between volatility and a second factor, moment-to-moment stochasticity." This is the v-ratio idea stated as
  normative Kalman logic for learners.
- Burge, Ernst & Banks (2008). The statistical determinants of adaptation rate in human reaching. *J. Vision* 8(4):20.
  DOI 10.1167/8.4.20 (abstract): "Increasing measurement uncertainty caused similar decreases in recalibration rate ...
  more variation in systematic error increased recalibration rate. However ... Inserting random error by perturbing
  feedback position causes slower adaptation in Kalman filters but had no effect in humans." This is a direct
  manipulation of both drift and noise, with partial agreement and one clear failure of the Kalman prediction.
- Daw, Gershman, Seymour, Dayan & Dolan (2011). Model-based influences on humans' choices and striatal prediction errors.
  *Neuron* 69(6), 1204-15. DOI 10.1016/j.neuron.2011.02.027 (**full text**, PMC3077926). Drift: "these reward
  probabilities were diffused at each trial by adding independent Gaussian noise (mean 0, SD .025), with reflecting
  boundaries at .25 and .75." Fitted (Table 1, median [25th-75th pctile]): alpha1 = 0.54 [0.46-0.87],
  alpha2 = 0.42 [0.21-0.71].
  **Own computation, not from the literature.** Outcomes are Bernoulli with sd sqrt(p(1-p)) = 0.43-0.50, so
  v = 0.025/0.43..0.50 = 0.050-0.058 and K(v) = 0.049-0.056. The second-stage learning rate alpha2 (the one that tracks
  the drifting reward probability) has a median about **8x the optimal gain**. Its 25th percentile is still about 4x.
  Adding the law's "own resolution" to the denominator would lower K(v) further and widen the gap. (For the Daw et al.
  2006 restless bandit, diffusion sd 2.8 and observation sd 4 give v = 0.7 and K = 0.50. There the optimum itself is
  large.) I found no paper that states this factor for the two-step task. Treat it as my computation.
- Gershman (2015). Do learning rates adapt to the distribution of rewards? *Psychon. Bull. Rev.* 22, 1320-27.
  DOI 10.3758/s13423-014-0790-3 (abstract): the predicted adaptation of learning-rate asymmetry to reward rate was
  "largely insensitive to the average reward rate". That concerns asymmetry, not volatility, but it is another case where
  learning rates do not follow the normative environmental prediction.

**Verdict for L3 in learning tasks: PARTIAL.** It is well established that learning rates *increase with volatility and
decrease with noise*, qualitatively and sometimes near the ideal observer (Behrens 2007; Browning 2015 for low-anxiety
subjects; Burge 2008). Models implementing this (Mathys 2011; Piray & Daw 2021) use subject-specific free parameters.
Quantitative level matches fail in standard tasks (Daw 2011 two-step: fitted about 0.42 vs optimal about 0.05, own
computation), in anxious individuals (Browning 2015), and under added feedback noise (Burge 2008).

---

## 4. Sensory adaptation time constants scaling with stimulus statistics

**Queries run.** Crossref `Fairhall Lewen Bialek de Ruyter van Steveninck efficiency and ambiguity`; `Wark Fairhall Rieke
timescales of inference in visual adaptation`. Europe PMC abstracts. PMC full text of Wark et al. (NCBI efetch,
PMC2677143).

**Works.**
- Fairhall, Lewen, Bialek & de Ruyter van Steveninck (2001). Efficiency and ambiguity in an adaptive neural code.
  *Nature* 412, 787-792. DOI 10.1038/35090500 (abstract): "Adaptation to these statistics occurs over a wide range of
  timescales - from tens of milliseconds to minutes ... The speed with which information is optimized and ambiguities
  are resolved approaches the physical limit imposed by statistical sampling and noise." Wark et al. (2009) cite Fairhall
  2001 among studies describing adaptation "as a linear process with a wide range of time scales, producing, e.g., a
  power-law dependence of response on time" (secondary).
- Wark, Fairhall & Rieke (2009). Timescales of inference in visual adaptation. *Neuron* 61(5), 750-761.
  DOI 10.1016/j.neuron.2009.01.019 (**full text**, PMC2677143). "Adapting optimally requires matching the dynamics of
  adaptation to those of changes in the stimulus distribution." "The average effective time constant of adaptation
  scales approximately linearly across a broad range of switching periods (~8-32s) ... These results indicate that a
  fixed first-order process does not govern the dynamics of contrast adaptation in mouse retina. Instead, the adapting
  machinery has access to multiple timescales." Their model is change-detection inference (switching variance/mean), not
  a random walk.
- Related: DeWeese & Zador (1998), Asymmetric dynamics in optimal variance adaptation, *Neural Comput.* 10, 1179-1202
  (cited by Wark et al.; not opened). Kording, Tenenbaum & Shadmehr (2007), The dynamics of memory as a consequence of
  optimal adaptation to a changing body, *Nat. Neurosci.* 10, 779-786, DOI 10.1038/nn1901 (abstract): memory timescales
  follow from Bayesian (Kalman) credit assignment across multiple random-walk disturbance timescales. This is the closest
  statement of "memory dynamics = optimal filter for the environment's drift statistics" for a biological system.

**Verdict: PARTIAL.** Adaptation timescales depend on stimulus statistics and are argued to be near-optimal inference.
The environments are switching or change-point, and the finding is linear scaling with switching period and multiple
timescales (a single fixed exponential does not fit). None states alpha = K(sd drift/sd noise) for a random walk. The
"multiple timescales / power law" finding argues against the law's premise that the state is a single EWMA.

---

## 5. Implied volatility / RiskMetrics as exponentially weighted memory; optimal filter gain for variance

**Queries run.** WebSearch: `RiskMetrics Technical Document 1996 decay factor 0.94 ...`; `VIX implied variance
exponentially weighted average of past realized variance decay parameter estimated optimal filter Kalman gain`; `Nelson
Foster 1994 asymptotic filtering theory ...`; `Stein 1989 Overreactions in the options market ...`. Crossref for Nelson &
Foster, Nelson (1992), Stein (1989), Christensen & Prabhala (1998), Poon & Granger. Full text of the RiskMetrics Technical
Document (4th ed., 1996, MSCI-hosted PDF). IDEAS/RePEc abstracts.

**Works.**
- J.P. Morgan/Reuters (1996). *RiskMetrics - Technical Document*, 4th ed. (**full text**). The decay factor is chosen
  **empirically** per series by RMSE: "associated with each series is an optimal decay factor that minimizes the root
  mean squared error of the variance forecast". One decay is then pooled: "one for the daily data set (lambda = 0.94),
  and the other for the monthly data set (lambda = 0.97)". Table 5.8 shows per-series optima ranging from 0.835 to 0.995
  (e.g. Swiss 5-yr swaps 0.835, Finland FX 0.995). They add that for risk management "the decay factor should allow
  enough stability" (a non-statistical criterion). No derivation from a variance signal-to-noise ratio.
- Nelson, D. B. & Foster, D. P. (1994). Asymptotic filtering theory for univariate ARCH models. *Econometrica* 62(1),
  1-41. DOI 10.2307/2951474 (abstract, IDEAS): the paper characterises "asymptotically optimal ARCH conditional variance
  estimates. They apply their results to derive optimal ARCH filters for three diffusion models, and to examine in detail
  the filtering properties of GARCH(1,1) ...". This is the closest statement that an exponentially weighted variance
  filter has an *optimal* weight set by the variance process's own dynamics (vol-of-vol vs return noise). The paper
  treats it as a design result for econometricians, not a claim about markets. Full text is a scanned PDF and was not
  read.
- Nelson (1992). Filtering and forecasting with misspecified ARCH models I. *J. Econometrics* 52, 61-90 (companion; see
  Nelson & Foster NBER t0132 abstract): misspecified ARCH "may do a good job at estimating conditional variances ... [but]
  may perform disastrously at medium and long term forecasting".
- Stein, J. (1989). Overreactions in the options market. *J. Finance* 44(4), 1011-23. DOI 10.1111/j.1540-6261.1989.tb02635.x
  (snippet of abstract): long-maturity implied volatilities move more than rational expectations imply given the
  measured mean reversion of short-maturity implied volatility ("overreact"). This is the implied-vol analogue of a gain
  above the rational one.
- Christensen & Prabhala (1998). The relation between implied and realized volatility. *JFE* 50(2), 125-150.
  DOI 10.1016/S0304-405X(98)00034-8 (abstract): "implied volatility outperforms past volatility in forecasting future
  volatility and even subsumes the information content of past volatility in some of our specifications".

**Verdict: NOT FOUND** for "VIX's memory of realised variance equals the optimal filter gain of the realised-variance
process". PARTIAL for the pieces: EWMA variance weights are fitted empirically (RiskMetrics 0.94/0.97, with large
per-series spread). Optimal ARCH filter weights exist in theory (Nelson & Foster 1994). Implied vol is documented to
over-react relative to rational benchmarks (Stein 1989).

---

## 6. Physical systems: soil temperature at depth

**Queries run.** WebSearch `soil temperature damping depth "D = sqrt(2" thermal diffusivity angular frequency ...
Hillel Campbell Norman`. Crossref for Campbell & Norman, Carslaw & Jaeger, Hillel. Full text of the open textbook
chapter below.

**Works.**
- *Physical Processes in Ecosystems*, ch. 13.5 "Use of the Heat Conduction Equation" (open bookdown textbook,
  https://bookdown.org/huckley/Physical_Processes_In_Ecosystems/13-5-soilheatflow-heatconduction.html, **full text**):
  "A(z) = A(0) exp(-z/D) (13.12) and B(z) = -z/D (13.13) where D is termed the damping depth, and is related to the
  thermal properties of the soil and the frequency of the temperature wave by the expression D = (2K/omega)^{1/2}
  (13.14)" [K = thermal diffusivity = k/C]. The worked example gives D = 15.2 cm for a sand soil at the diurnal
  frequency.
- Standard textbooks (not opened today; cite for the same result): Carslaw, H. S. & Jaeger, J. C. (1959). *Conduction of
  Heat in Solids*, 2nd ed., Oxford (periodic surface temperature, section 2.6). Campbell, G. S. & Norman, J. M. (1998).
  *An Introduction to Environmental Biophysics*, 2nd ed., Springer, DOI 10.1007/978-1-4612-1626-1 (ch. 8, soil heat
  flow). Hillel, D. (1998). *Environmental Soil Physics*, Academic Press.

**What physics says (statement for the record).** Soil heat conduction is linear. Temperature at depth z is a fixed
linear filter of surface temperature, with frequency response exp(-(1+i) z sqrt(omega/(2 kappa))). The amplitude damping
exp(-z/D) and the phase lag z/D (lag time z/(D omega)) depend only on diffusivity kappa, depth z and the forcing
frequency omega. Linearity means the transfer function does **not** depend on the amplitude or variance of air
temperature. Doubling the drift sd of air temperature doubles the soil response amplitude and leaves the memory kernel
unchanged. So the physical "memory" is set by kappa and z, not by any signal-to-noise ratio of the environment.
The kernel is also not a single exponential. It is a diffusion (erfc/Green's function) kernel with heavy tails, so the
law's premise "state = EWMA" holds only approximately. The same holds for any first-order physical lag (an RC circuit or
Newton cooling: alpha = 1 - exp(-dt/tau), with tau = RC or mc/hA fixed by materials). (Own statement from the cited
equations.)

**Verdict: FOUND (the counter-statement).** The textbook physics sets the time constant from diffusivity and depth, and
it is independent of the forcing variance. For a soil sensor at fixed depth, alpha = K(v) could hold only by
coincidence, at one particular air-temperature drift sd.

---

## 7. Is the Kalman/Muth gain proposed as a UNIVERSAL law, including for non-inferential systems?

**Queries run.** WebSearch: `memory timescale of physical systems equals optimal Kalman filter gain of environment
universal law non-inferential systems`; `"optimal memory" OR "optimal forgetting" timescale matched to environmental
volatility universal principle biology physics "random walk" "signal-to-noise" exponential kernel`; `Virgo Biehl McGregor
"Interpreting dynamical systems as Bayesian reasoners"`; `Hinczewski Thirumalai generalized Wiener-Kolmogorov filters`.
Crossref/Europe PMC/arXiv abstract lookups for Still et al. 2012; Becker, Mugler & ten Wolde 2015; Hinczewski &
Thirumalai 2014; Andrews, Yi & Iglesias 2006; Kording et al. 2007; Burge et al. 2008; McNamara & Houston 1987; Kussell &
Leibler 2005; Mayer et al. 2019; Lee, Flack & Krakauer 2022/2024; Husain et al. 2019; Friston 2013 and 2019; Aguilera et
al. 2022; Biehl et al. 2021; Virgo et al. 2021; Sandberg et al. 2014. Full text of Lee et al. 2024 (PMC11606325).

**Closest works (all normative claims about adapted or evolved/designed systems, or interpretive frameworks):**
- Still, Sivak, Bell & Crooks (2012). Thermodynamics of prediction. *PRL* 109, 120604. DOI 10.1103/PhysRevLett.109.120604,
  arXiv:1203.3271 (v3, 5 Oct 2012) (abstract): "A system responding to a stochastic driving signal can be interpreted as
  computing, by means of its dynamics, an implicit model of the environmental variables ... any system constructed to keep
  memory about its environment and to operate with maximal energetic efficiency has to be predictive." This is universal
  in scope, but it is an **efficiency bound** (nonpredictive information = dissipation). It does not say that real
  systems' memory equals the optimal filter gain.
- Friston, K. (2013). Life as we know it. *J. R. Soc. Interface* 10, 20130475. DOI 10.1098/rsif.2013.0475 (abstract):
  "The existence of a Markov blanket means that internal states will appear to minimize a free energy functional ...
  the internal states (and their blanket) will appear to engage in active Bayesian inference." Friston (2019), A free
  energy principle for a particular physics, arXiv:1906.10184. This is the **closest universal claim**: any NESS system
  with a Markov blanket can be read as inferring its environment. For a linear-Gaussian world this reading would imply a
  Kalman-type posterior mean. The FEP does not state the gain formula. It assumes a stationary (NESS) density, which a
  random-walk environment lacks. It is contested in exactly the linear case:
  - Aguilera, Millidge, Tschantz & Buckley (2022). How particular is the physics of the free energy principle? *Phys.
    Life Rev.* 40, 24-50. DOI 10.1016/j.plrev.2021.11.001 (abstract): the FEP's conditions "are only valid for a very
    narrow space of parameters ... a mathematically central step ... relies on an implicit equivalence between the
    dynamics of the average states of a system with the average of the dynamics of those states. This equivalence does
    not hold in general even for linear stochastic systems". See also Biehl, Pollock & Kanai (2021), *Entropy* 23, 293,
    DOI 10.3390/e23030293, and Friston's reply (2022), DOI 10.1016/j.plrev.2022.05.002.
  - Virgo, Biehl & McGregor (2021). Interpreting dynamical systems as Bayesian reasoners. arXiv:2112.13523 (ECML-PKDD
    workshop, DOI 10.1007/978-3-030-93736-2_52) (abstract): "we begin the development of a general theory that would tell
    us when it is appropriate to interpret states as representing beliefs". Whether a system *can be interpreted* as a
    filter depends on a chosen model. Such an interpretation is not a prediction of the gain.
- Lee, Flack & Krakauer (2024). Constructing stability: optimal learning in noisy ecological niches. *Proc. R. Soc. B*
  291, 20241606. DOI 10.1098/rspb.2024.1606 (**full text**, PMC11606325). Preprint: Outsourcing memory through niche
  construction, arXiv:2209.00476 (v2, 8 Jan 2023). Abstract: "We derive a universal scaling law for optimal memory
  duration, taking into account memory precision as well as two components of environmental volatility, bias and
  stability. We find sublinear scaling". Full text: "The weight beta determines how quickly the previous state of the
  system is forgotten ... tau_m = -1/log beta". This is **the nearest "universal law" of optimal EWMA memory vs
  environmental timescale**. It is normative, it is for *learning agents* (organisms and their niche), and its exponent
  comes from a KL-cost trade-off rather than from the Kalman formula. (For comparison, K(v) gives memory ~ 1/v for small
  v, i.e. memory ~ (drift variance)^(-1/2), which is also sublinear. Own remark.)
- McNamara, J. M. & Houston, A. I. (1987). Memory and the efficient use of information. *J. Theor. Biol.* 125, 385-395.
  DOI 10.1016/S0022-5193(87)80209-6 (abstract): "how an animal's memory should be designed in order to cope with a
  stochastic and changing environment ... an exponential weighting of past observations is a sufficient statistic ... The
  weighting factors ... each is shown to be a function of the rate at which the environment is changing." This is a
  normative statement of the law's idea for animal memory (L2 applied to foragers), not a universality claim.
- Kording, Tenenbaum & Shadmehr (2007), DOI 10.1038/nn1901: motor memory timescales as optimal (Kalman) adaptation to a
  changing body. Burge et al. (2008), DOI 10.1167/8.4.20: adaptation rate vs drift and noise, mostly Kalman-like, with
  one failure.
- Cellular filters: Andrews, Yi & Iglesias (2006), *PLoS Comput. Biol.* 2(11):e154, DOI 10.1371/journal.pcbi.0020154
  (abstract): E. coli chemotaxis cutoff frequency from an optimal-filtering problem, "good agreement between the theory,
  simulations, and published experimental data". Becker, Mugler & ten Wolde (2015), *PRL* 115, 258103,
  DOI 10.1103/PhysRevLett.115.258103, arXiv:1512.02124 (abstract): "Single-layer networks generate exponential response
  kernels, which suffice to predict Markovian signals optimally ... the integration time of its response kernel arises
  from a trade-off between rapid response and noise suppression." Hinczewski & Thirumalai (2014), *PRX* 4, 041017,
  DOI 10.1103/PhysRevX.4.041017, arXiv:1406.3290 (abstract): push-pull motif "effectively behaves as a Wiener-Kolmogorov
  (WK) optimal noise filter". Husain, Pittayakanchit, Pattanayak & Rust (2019), arXiv:1903.07103 (abstract): cells
  "raise their sensitivity to new external information in epochs of frequent challenging stress, much like a Kalman
  filter with adaptive gain". These are evolved biochemical systems. Their optimality is a hypothesis tested case by case,
  and the claim is "can implement" or "near", never "every system".
- Kussell & Leibler (2005), *Science* 309, 2075-78, DOI 10.1126/science.1114383 (abstract): "The optimal switching rates
  then mimic the statistics of environmental changes." Mayer, Balasubramanian, Walczak & Mora (2019), *PNAS* 116,
  8815-23, DOI 10.1073/pnas.1812810116, arXiv:1806.05753 (abstract): the immune memory as "a dynamic Bayesian machinery
  that updates its memory repertoire by balancing evidence from new pathogen encounters against past experience".
  Evolved-optimality claims again.
- Physical implementation of Kalman filters: Sandberg, Delvenne, Newton & Mitter (2014), *PRE* 90, 042119,
  DOI 10.1103/PhysRevE.90.042119 (abstract): a Kalman-Bucy feedback demon realised as an electrical circuit; "any
  implementation of the demon must necessarily include an external power source". This cuts against L4: a passive
  physical system does not implement the optimal filter for free.

**Verdict for L4 (universality incl. non-inferential physical systems): NOT FOUND.** No work I found claims that the
memory depth of *every* exponentially-weighted system, including passive physical ones like soil, equals the steady-
state Kalman gain of its environment with no free parameter. The nearest claims are:
(a) normative optimal-memory laws for learning or evolved agents (McNamara & Houston 1987; Kording et al. 2007; Lee,
Flack & Krakauer 2024, "universal scaling law", sublinear);
(b) case studies of biochemical networks as near-optimal WK/Kalman filters (Andrews 2006; Hinczewski & Thirumalai 2014;
Becker et al. 2015; Husain et al. 2019);
(c) interpretive universality (FEP: Friston 2013/2019; Still et al. 2012), which says a system can be *read* as
modelling its environment. For linear systems this reading has been shown to fail generally (Aguilera et al. 2022), and
interpretation is model-relative (Virgo et al. 2021).
So the universality claim would be new. The prior physics (section 6: linear response, a time constant fixed by
material parameters and independent of forcing variance) and the behavioural evidence (sections 2-3: systematic
over- and under-reaction, system neglect, fitted rates far from K(v)) are direct evidence **against** it. A new claim of
this kind would have to show alpha tracking a *manipulated* environmental v in a passive system, which linear response
theory says will not happen.

---

## Summary table

| # | Question | Verdict |
|---|---|---|
| 1 | Muth/Kalman: EWMA weight = K(v) optimal for random walk + noise | **FOUND**. K = (sqrt(q^2+4q) - q)/2, q = v^2 = sigma_eta^2/sigma_eps^2 (Muth 1960; Kalman 1960; Harvey 1989; stated explicitly by McCulloch 2026 WP eq. 7 and Koopman's slides). The law's "sd + resolution" denominator is non-standard. |
| 2 | Forecasters/households use the optimal gain | **PARTIAL**. Gains are estimated (CG15: G ~ 0.45 to 0.7 per quarter; Carroll: 0.27 per quarter; MRW: 0.08-0.10 per month; MN: 0.018 per quarter). Only the direction vs a measured noise/signal ratio is tested (CG15, 20-30% of variance). No level test. Controlled experiments show systematic departures (Afrouzi 2023; Massey & Wu 2005; Bordalo 2020). |
| 3 | Learning rates match the optimal Kalman gain | **PARTIAL**. The direction with volatility and noise is established (Behrens 2007; Browning 2015; Burge 2008; Piray & Daw 2021). Levels are often far off: Daw 2011 two-step alpha2 median 0.42 vs K about 0.05 (own computation). Models carry subject-specific free parameters (Mathys 2011). |
| 4 | Sensory adaptation timescales match the environment | **PARTIAL**. Timescales scale with switching period and are multi-timescale/power-law (Fairhall 2001; Wark 2009). Not K(v) for a random walk. |
| 5 | VIX/EWMA memory = optimal variance-filter gain | **NOT FOUND** as stated. RiskMetrics lambda is fitted by RMSE (0.94 daily, 0.97 monthly; per-series 0.835-0.995). Optimal ARCH filter theory exists (Nelson & Foster 1994). Implied vol over-reacts (Stein 1989). |
| 6 | Soil temperature memory set by physics, not air-temperature variability | **FOUND** (counter-statement). D = sqrt(2 kappa/omega), amplitude exp(-z/D), lag z/D. Linear, so independent of forcing variance. |
| 7 | Kalman gain as universal law incl. non-inferential systems | **NOT FOUND**. Nearest: Lee/Flack/Krakauer 2024 (universal sublinear optimal-memory scaling for learners), McNamara & Houston 1987, the FEP (interpretive, contested by Aguilera et al. 2022), Still et al. 2012 (efficiency bound). |
