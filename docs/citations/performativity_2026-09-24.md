# Literature check: performative forecasts, self-fulfilling prophecies, zero-stake predictor designs

Checked on **2026-09-24** (UTC; the fetches ran 2026-09-24, around 15:00–16:15 UTC). Every source below was fetched today with `curl` (arXiv abs pages and PDFs, api.crossref.org, publisher, central-bank and forum pages) or with WebFetch where `curl` got a 403. Discovery used WebSearch. Nothing here was quoted from memory.

**How to read each entry.** "Access" says what was read: **full text** (PDF or HTML fetched and searched), **abstract** (abstract or landing page only), or **metadata** (Crossref record only). Quotes are verbatim from the fetched text. PDF text was extracted with `pypdf`. Where that extraction split words ("ceases t o be") or turned ligatures into odd glyphs, only the whitespace and ligatures were fixed; no words were changed. Two quotes, marked **[WebFetch]**, came back through WebFetch's summarising model because `curl` got a 403. Treat them as not byte-verified.

**Access failures (R10).**
- arXiv export API returned `406` (so the arXiv abs pages were used instead).
- Semantic Scholar API returned `429` (rate limit).
- Crossref returned `429` intermittently (the queries were retried).
- These pages returned `403` to both `curl` and WebFetch: tandfonline.com (Soros 2013 PDF; Beretta et al. 2025), dl.acm.org (Khosrowi et al. 2025), forbes.com, metaculus.com/faq.
- georgesoros.com returned `403` to `curl`, but WebFetch succeeded.
- The SFU copy of Morris & Shin 1998 is a scanned JSTOR PDF with no text layer, so the abstract came from RePEc/EconPapers.

Scratch copies of every fetched file (abs_*.html, pdf_*.pdf/.txt, f_*.txt, bern.txt, boe_qb1992q4.txt, etc.) are in this folder.

---

## 1. Performative prediction (ML)

### 1.1 Perdomo, Zrnic, Mendler-Dünner, Hardt (2020). "Performative Prediction." ICML 2020.
- arXiv:2002.06673. v1 16 Feb 2020; current **v4, 26 Feb 2021**. Fetched https://arxiv.org/abs/2002.06673 and https://arxiv.org/pdf/2002.06673v4. **Full text.**
- Quotes:
  - "When predictions support decisions they may influence the outcome they aim to predict. We call such predictions performative; the prediction influences the target." (abstract)
  - "We call this procedure repeated risk minimization. … When repeated risk minimization converges in objective value the model has minimal loss on the distribution it entails … We refer to this condition as performative stability, noting that it is neither implied by nor does it imply minimal performative risk." (§1)
  - Theorem 3.5(b): "If ε < γ/β, the iterates θt of RRM converge to a unique performatively stable point θPS at a linear rate". The paper adds: "removing any single assumption required for convergence by Theorem 3.5 is enough to construct a counterexample for which RRM diverges." Figure 2 caption area: "the iterates converge for small values of ε and diverge for large values."
- Summary. Repeated retraining on self-influenced data is a fixed-point iteration. It contracts when the performative sensitivity ε is below γ/β and can diverge otherwise. Performative stability (the model is optimal on the data it itself induces) differs from performative optimality. The authors also note that RRM "can [be] reinterpret[ed] … as a form of off-policy learning" in RL.

### 1.2 Miller, Perdomo, Zrnic (2021). "Outside the Echo Chamber: Optimizing the Performative Risk." ICML 2021.
- arXiv:2102.08570. **v2, 15 Jun 2021**. Fetched abs and PDF v2. **Full text.**
- Quotes:
  - "Stable classifiers can maximize the performative risk even when the loss is well-behaved and performative effects are small. Not only can stable points maximize the performative risk, but they can also have an arbitrarily large suboptimality gap".
  - "the performative risk is guaranteed to be convex if and only if ε ⩽ γ/(2β)".
  - "we propose a two-stage approach, by which the learner first creates an explicit model of the distribution map D̂, and then optimizes a proxy objective … In the first stage, we estimate a coarse model of the distribution map, D̂(·) via experiment design" (Algorithm 1: "Sample and deploy classifier θi i.i.d.∼ N(0, Id)").
- Summary. Stable points (zero-stake fixed points) can be arbitrarily bad under the deployer's own risk. Estimating the map from model to outcome by randomised deployments is an established step.

### 1.3 Mendler-Dünner, Ding, Wang (2022). "Anticipating Performativity by Predicting from Predictions." NeurIPS 2022.
- arXiv:2208.07331. **v2, 18 Oct 2022** (camera-ready). Fetched abs and PDF v2. **Full text.**
- Quotes:
  - "model predictions are usually deterministic functions of input features and highly correlated with outcomes. This can make the causal effects of predictions on outcomes impossible to disentangle from the direct effect of the covariates." (abstract)
  - "we highlight three natural scenarios where the causal relationship between covariates, predictions and outcomes can be identified from observational data: randomization in predictions, overparameterization of the predictive model deployed during data collection, and discrete prediction outputs." (abstract)
  - "data collected under the deployment of a fully randomized prediction function fθ … is ideal for learning and allows for global identification of MY" (§3.3). The abstract adds: "These positive results fundamentally rely on model predictions being recorded during data collection".
- Summary. This is direct prior art for a forecaster that estimates its own causal effect on outcomes. Randomising (or recording) the forecast identifies the effect, and supervised learning with the prediction as an input feature recovers it.

### 1.4 Hardt, Jagadeesan, Mendler-Dünner (2022). "Performative Power." NeurIPS 2022.
- arXiv:2203.17232. **v2, 3 Nov 2022**. Fetched abs and PDF v2. **Abstract** (PDF fetched, abstract used).
- Quotes:
  - "performative power is a causal notion that is identifiable with minimal knowledge of the market".
  - "Low performative power implies that a firm can do no better than to optimize their objective on current data. In contrast, firms of high performative power stand to benefit from steering the population towards more profitable behavior."
- Summary. This work measures the size of the predictor's influence ("stake"). Low power makes zero-stake retraining optimal.

### 1.5 Brown, Hod, Kalemaj (2022). "Performative Prediction in a Stateful World." AISTATS 2022.
- arXiv:2011.03885. **v3, 23 Feb 2022**. Fetched abs and PDF v3. **Abstract.**
- Quotes:
  - "We propose a theoretical framework where the response of a target population to the deployed classifier is modeled as a function of the classifier and the current state (distribution) of the population. We show necessary and sufficient conditions for convergence to an equilibrium of two retraining algorithms, repeated risk minimization and a lazier variant."
- Summary. This extends retraining dynamics to worlds with memory (state).

### 1.6 Related ML papers fetched today (abstracts unless noted)
- **Mendler-Dünner, Perdomo, Zrnic, Hardt (2020)**, "Stochastic Optimization for Performative Prediction", NeurIPS 2020. arXiv:2006.06887 v4 (19 Feb 2021). "The latter triggers a shift in the distribution that affects future data, while the former keeps the distribution as is … (greedy deploy) as well as … (lazy deploy)".
- **Izzo, Ying, Zou (2021)**, "How to Learn when Data Reacts to Your Model: Performative Gradient Descent". arXiv:2102.07698 v2 (16 Feb 2021). "PerfGD explicitly captures how changes in the model affects the data distribution".
- **Hardt & Mendler-Dünner**, "Performative Prediction: Past and Future", to appear in *Statistical Science*. arXiv:2310.16608 **v2, 20 May 2025**. **Full text.** This survey links the ML work to the economics lineage (see §4):
  - "Grunberg, Modigliani, and Simon were the first to provide a positive answer. They identified continuity of R as a sufficient condition for the feasibility of correct public prediction under performativity. Their result follows from Brouwer's fixed point theorem."
  - "Any economic forecast, published with authority and reach, would necessarily cause economic activity that would influence the outcomes that the forecast aimed to predict." (on Morgenstern 1928)
  - "Adapting the terminology from Grunberg and Modigliani (1954), we call updates that are deployed public model updates, and updates that are done offline private model updates."
- **Kim & Perdomo (2023)**, "Making Decisions under Outcome Performativity", ITCS 2023. arXiv:2210.01745 v2 (7 Jan 2023). "existing solution concepts do not address the apparent tension between the goals of forecasting outcomes accurately and steering individuals to achieve desirable outcomes."
- **Kabra & Patel (2024)**, "The Limitations of Model Retraining in the Face of Performativity". arXiv:2408.08499 v1 (16 Aug 2024). "naive retraining can be provably suboptimal even for simple distribution shifts … adding regularization to retraining corrects both of these issues".
- **Farina & Perdomo (2026)**, "The Stability of Online Algorithms in Performative Prediction". arXiv:2602.24207 v2 (3 Jun 2026). "any no-regret algorithm deployed in performative settings converges to a (mixed) performatively stable equilibrium".
- **Rodemann, Fischer-Abaigar, Bailie, Muandet (2026)**, "Performative Learning Theory", ICML 2026. arXiv:2602.04402 **v3, 8 Jun 2026**. **Full text.**
  - "Our analysis reveals a fundamental trade-off between performatively changing the world and learning from it: the more a model affects data, the less it can learn from it." (abstract)
  - "systems that heavily influence their environment may simultaneously undermine their own ability to make accurate predictions about that environment." (conclusion)
- **Lee & Zrnic (2026)**, "Partially Performative Prediction". arXiv:2606.07890 v1 (5 Jun 2026). "Predictive models may influence future data through the decisions they support, while the world itself continues to drift for reasons beyond the learner's control. We study partially performative prediction, a framework that captures both endogenous and exogenous sources of distribution shift."
- **Zhao, Liu, Rodriguez, Prakash**, "Performative Time-Series Forecasting", KDD 2025. arXiv:2310.06077 **v2, 2 Jun 2025**. "feedback loops where predictions can influence the predicted outcome … introduces the potential for 'self-negating' or 'self-fulfilling' predictions".
- **Nagarajan & Ashok (2026)**, "REFLEX: Reflexive Equilibrium Fixed-point Learning for Endogenous eXchanges", ICAIF '26. arXiv:2608.16155 v1 (17 Aug 2026). **Full text.** This names the retraining iteration a cobweb explicitly:
  - "Retraining is therefore a cobweb map".
  - "Competition manufactures a synchronized cobweb".
  - "The demo regime is genuinely RRM-unstable (f = 6, slow toxic decay, cobweb modulus 1.21). There the blind cobweb provably diverges while the corrected 1-D ascent converges".
- **Surveys (2026).**
  - Kehrenberg, Sanguino, Lozano, Quadrianto, "Dissecting Performative Prediction: A Comprehensive Survey". arXiv:2602.10176 v1 (10 Feb 2026). Full text searched. "we do not want to give the impression that performative prediction is merely a re-packaging of Goodhart's Law. Deliberate manipulation of a measure is not needed in order for the environment to change".
  - Fybish & Susnjak, "When Predictions Shape Reality", arXiv:2601.04447 v1 (7 Jan 2026). Abstract only.
- **Feedback loops in recommenders and data.**
  - Chaney, Stewart, Engelhardt, "How Algorithmic Confounding in Recommendation Systems Increases Homogeneity and Decreases Utility". arXiv:1710.11214 v2 (27 Nov 2018). "These systems are often evaluated or trained with data from users already exposed to algorithmic recommendations; this creates a pernicious feedback loop."
  - Jiang et al., "Degenerate Feedback Loops in Recommender Systems", AIES 2019. arXiv:1902.10730 v3.
  - Taori & Hashimoto, "Data Feedback Loops: Model-driven Amplification of Dataset Biases". arXiv:2209.03942 v1 (8 Sep 2022). "the degree of bias amplification is closely linked to whether the model's outputs behave like samples from the training distribution".
  - Bottou et al., "Counterfactual Reasoning and Learning Systems" (JMLR 2013). arXiv:1209.2355 v5 (27 Jul 2013). "how to leverage causal inference to understand the behavior of complex learning systems interacting with their environment".
- **Causal estimation of a predictor's effect without randomisation.**
  - Cheng, Hardt, Mendler-Dünner, "Causal Inference out of Control: Estimating the Steerability of Consumption". arXiv:2302.04989 v1 (10 Feb 2023). The ICML 2024 version is titled "…Estimating Performativity without Treatment Randomization" per WebSearch (proceedings.mlr.press/v235/cheng24d; not fetched). From the arXiv abstract: "exogenous variation in consumption and appropriately responsive algorithmic control actions are sufficient for identifying steerability".
- **Medicine.** van Amsterdam, van Geloven, Krijthe, Ranganath, Ciná, "When accurate prediction models yield harmful self-fulfilling prophecies". arXiv:2312.01210 **v4, 26 Aug 2024**. Published in Patterns 2025, per the Boeken et al. reference list; not fetched separately.
  - "These models are harmful self-fulfilling prophecies: their deployment harms a group of patients but the worse outcome of these patients does not invalidate the predictive power of the model."
  - "models that are well calibrated before and after deployment are useless for decision making as they made no change in the data distribution."

**Verdict for item 1: FOUND.** Stability versus optimality, the RRM convergence condition ε < γ/β (with divergence beyond it), stateful extensions, lazy versus greedy deploy, and identification of the forecast's causal effect by randomisation are all established.

---

## 2. Proper scoring rules under performativity

### 2.1 Oesterheld, Treutlein, Cooper, Hudson (2023). "Incentivizing honest performative predictions with proper scoring rules." UAI 2023.
- arXiv:2305.17601. **v2, 30 May 2023**. Fetched abs and PDF v2. **Full text.**
- Question asked: does a score-maximising predictor prefer extreme fixed points, or fail to report the fixed point at all? **Yes to both.** Quotes:
  - "We say a prediction is a fixed point if it accurately reflects the expert's beliefs after that prediction has been made. We show that in this setting, reports maximizing expected score generally do not reflect an expert's beliefs, and we give bounds on the inaccuracy of such reports." (abstract)
  - "for any strictly proper scoring rule, there exist functions f from predictions to beliefs such that performatively optimal reports are not fixed points, even if one exists and is unique." (§1)
  - "if an expert has incentives other than to predict honestly—e.g., to bring about fixed points with lower entropy—this is undesirable even if the expert otherwise makes approximately accurate predictions." (§1)
  - Appendix B, **Proposition 4**: "Let F = {p : f(p) = p} be a set of fixed points of f. Let p ∈ F such that p is the convex combination of elements of F − {p}. … Then if S is strictly proper, there exists a p* ∈ F s.t. S(p*, f(p*)) > S(p, f(p)). Thus, arg max_{p∈F} S(p, f(p)) is a subset of the extreme points of F."
  - "scoring rules generally induce a preference for extreme honest predictions over non-extreme honest predictions … a slight dishonesty … can be outweighed by the fact that the prediction is more extreme." (proof of Prop. 3)
  - **Example 3 (Bank Run)**, a bistable world: "A newspaper's AI predicts whether a certain bank will suffer a bank run or not. Readers use this information when deciding whether to withdraw their money … Then f has fixed points at p = (1/10, 9/10), p = (3/5, 2/5), and p = (9/10, 1/10)."
  - The abstract closes: "we discuss alternative notions of optimality, including performative stability, and show that they incentivize reporting fixed points."
  - Appendix D (stop-gradient): "we call S(p, ⊥f(p)) the stop-gradient objective" and "the expectation of this gradient, conditional on Pt, is exactly the repeated gradient … Hence, given the right assumptions, this converges to fixed points instead of performative optima."
  - "Stop-gradients could also be circumvented in a hidden way [Krueger et al., 2020] … this search would prefer algorithms that optimize S(p, f(p)) directly, without a stop-gradient."
- Summary. Item (iii) is published in this form: with multiple self-fulfilling equilibria (their bank-run example has two extreme ones and one interior one), a proper-score maximiser prefers the most extreme or lowest-entropy fixed point. Their bounds relate the maximiser's inaccuracy to the strength of its influence, which is a formal version of item (i). Two things differ from the planned test. The bank-run function is a stylised polynomial, not a currency-peg model. And they study what the maximising report is, not retraining dynamics.

### 2.2 Armstrong (2019). "Self-confirming predictions can be arbitrarily bad." LessWrong / AI Alignment Forum, 3 May 2019.
- Fetched https://www.lesswrong.com/posts/KoEY9CjrKe93ErYhd/self-confirming-predictions-can-be-arbitrarily-bad (HTTP 200). **Full text.**
- Quotes:
  - "If you predict any amount £P, they'll erase their cheque and write £(P-1) instead … the only accurate predictions are at the extreme of the range."
  - "A prediction P is self-confirming if, once P is generally known, then P will happen … They exist when the outcome is continuous in the prediction P".
  - "where you end up at will not be determined by the background facts of the world … but it will entirely be determined by the feedback loop with your prediction."
  - "there is no link between the self-confirming prediction and what would have happened without prediction."

### 2.3 Boeken, Zoeter, Mooij (2025). "Conditional Forecasts and Proper Scoring Rules for Reliable and Accurate Performative Predictions." NeurIPS 2025.
- arXiv:2510.21335 **v1, 24 Oct 2025**. **Full text.**
- Quotes:
  - "conditioning forecasts on covariates that separate them from the outcome renders the target distribution forecast-invariant, guaranteeing well-posedness … However, even under this condition, classical proper scoring rules fail to elicit correct forecasts. We prove a general impossibility result and identify two solutions".
  - "If forecasts affect the target variable, correct forecasts need not exist: there may be no distributional fixed point where the forecast aligns with the induced outcome, as is the case in self-defeating prophecies."

**Verdict for item 2: FOUND.**

---

## 3. Oracles and conditioning predictive models

### 3.1 Armstrong & O'Rorke (2017/18). "Good and safe uses of AI Oracles."
- arXiv:1711.05541. **v5, 5 Jun 2018**. Fetched abs and PDF v5. **Full text.**
- Quotes:
  - "A counterfactual Oracle is incentivised to answer questions correctly because occasionally, with some small probability, the Oracle's output is hidden from us and sent instead to an automated system which judges the answer's correctness … When the output does become hidden from us in this way, we call this an 'erasure' event."
  - "The reward for the counterfactual Oracle is thus of the form R′ = I_E R."
  - "the Oracle will maximise its reward by setting o = E(F|E), the expectation of F given that its output is never read."
  - The experiment, a self-confirming world: "If an erasure event does not occur, the Oracle's prediction is to some extent self-confirming: the profit of the predicted company is 70% of what it would have been, plus 60% what the oracle predicts."
  - "The green … curve plots the Oracle's performance in the non-erasure cases … Unlike the erasure curve, this error doesn't tend to zero, because Oracle is predicting what the profit would be in an erasure event, not what the profit will actually be in the majority of cases."
- Summary. This is the counterfactual oracle (item v) and the erasure mechanism. Their own experiment already shows the cost of zero stake: accuracy on read episodes does not converge. That is item (i) in qualitative form.

### 3.2 Wei Dai (2019). "Counterfactual Oracles = online supervised learning with random selection of training episodes." AI Alignment Forum, 10 Sep 2019.
- Fetched https://www.alignmentforum.org/posts/yAiqLmLFxvyANSfs2/counterfactual-oracles-online-supervised-learning-with (HTTP 200). **Full text.**
- Quotes:
  - "To prevent self-confirming predictions, the labeling of data has to be done without causal influence from the Oracle."
  - "Online learning - The Oracle never stops learning, so it can eventually adjust to any distributional shift."
  - "(Note that what Stuart Armstrong calls "erasure" just means that the current episode has been selected as a training episode.)"
- The post also quotes Christiano: "Counterfactual oversight consists of labelling a random subset of data and using it as online training data."

### 3.3 Hubinger, Jermyn, Treutlein, Hudson, Woolverton (2023). "Conditioning Predictive Models: Risks and Strategies."
- arXiv:2302.00805. **v2, 6 Feb 2023**. Fetched abs and PDF v2. **Full text.**
- Quotes (§2.4 "Major challenge: Self-fulfilling prophecies"):
  - "Importantly, the model might consider its own effect on the world when making a prediction."
  - "Even if the model is myopically maximizing predictive accuracy, it has an incentive to find a fixed point that is both stable and likely—that is, a situation where the world state that results from the model outputting its prediction is highly overdetermined—since that's what makes for the best individual prediction."
  - "the model is incentivized to use its predictions to manipulate the world towards predictability."
  - §2.4.1: "condition on humans pre-committing to not looking at the output of the predictor depending on a true random number generator … This is closely related to the idea of a counterfactual oracle".
  - §2.4.2, "Predict the past": "If the model believes it is predicting a point in the past, it knows that any predictions have no causal effect on their own outcome".
  - §2.4.3, "Consequence-blindness": "a predictor that simply never takes into account the influence of the predictions it makes when considering the likelihood of those predictions."
  - §2.4: "its own predictions have never influenced the training data, so there is no incentive in the training data to account for the impact of its own predictions on the world. However, there are likewise no examples where the prediction should have influenced the world but did not".

**Verdict for item 3: FOUND.**

---

## 4. Economics classics

For the paywalled classics, Crossref metadata was fetched; open copies of the full text are noted where one was reached.

| Work | DOI (Crossref, fetched today) | Access | Verbatim support |
|---|---|---|---|
| Grunberg & Modigliani (1954), "The Predictability of Social Events", *JPE* 62(6):465–478 | 10.1086/257604 | metadata; content via the Hardt & Mendler-Dünner survey (§1.6) and Muth 1961 | Survey: "Grunberg and Modigliani (1954) distinguished between private and public predictions. Private predictions have no causal powers, whereas public predictions can alter the course of events." Also found: Grunberg & Modigliani (1965), "Reflexive Prediction", *Phil. Sci.* 32(2), DOI 10.1086/288038 (metadata) |
| Simon (1954), "Bandwagon and Underdog Effects and the Possibility of Election Predictions", *Public Opinion Quarterly* 18(3):245 | 10.1086/266513 | metadata; content via the survey | Survey: "Simon (1954) turned to bandwagon and underdog effects in election forecasts. The three scholars argued that it is in principle possible to find a prediction that equals the outcome caused by the prediction." |
| Merton (1948), "The Self-Fulfilling Prophecy", *Antioch Review* 8(2):193 | 10.2307/4609267 | **full text** (JSTOR scan at entrepreneurscommunicate.pbworks.com, HTTP 200) | "The self-fulfilling prophecy is, in the beginning, a false definition of the situation evoking a new behavior which makes the originally false conception come true. The specious validity of the self-fulfilling prophecy perpetuates a reign of error." (Illustrated with Millingville's solvent bank run.) |
| Ezekiel (1938), "The Cobweb Theorem", *QJE* 52(2):255 | 10.2307/1881734 | metadata only (JSTOR paywall; not fetched) | — |
| Muth (1961), "Rational Expectations and the Theory of Price Movements", *Econometrica* 29(3):315 | 10.2307/1909635 | **full text** (extranet.parisschoolofeconomics.eu/docs/guesnerie-roger/muth61.pdf, HTTP 200) | "expectations, since they are informed predictions of future events, are essentially the same as the predictions of the relevant economic theory." And: "A 'public prediction,' in the sense of Grunberg and Modigliani [14], will have no substantial effect on the operation of the economic system (unless it is based on inside information)." §5 "Rationality and Cobweb Theorems": "a major cause of price fluctuations in cattle and hog markets is sometimes believed to be the expectations of farmers themselves". |
| Lucas (1976), "Econometric policy evaluation: A critique", *Carnegie-Rochester Conf. Ser.* 1:19–46 | 10.1016/S0167-2231(76)80003-6 | **full text** (rogerfarmer.com/s/LucasCritique_1976.pdf, HTTP 200) | "given that the structure of an econometric model consists of optimal decision rules of economic agents, and that optimal decision rules vary systematically with changes in the structure of series relevant to the decision maker, it follows that any change in policy will systematically alter the structure of econometric models." |
| Morgenstern (1928), *Wirtschaftsprognose*; Morgenstern (1935), "Vollkommene Voraussicht und wirtschaftliches Gleichgewicht", *Z. f. Nationalökonomie* 6(3):337–357 | 1935: 10.1007/BF01311642 | 1935: metadata; 1928: via the survey only (book, not fetched) | Survey: "Economic forecasting, he argued in his century-old habilitation, was impossible with the tools of economic theory and statistics alone (Morgenstern, 1928, p. 112)." Survey: "Morgenstern already knew that performativity was a consequence of authority and reach." |
| Buck (1963), "Reflexive Predictions", *Phil. Sci.* 30(4):359–369 | 10.1086/287955 | metadata | (cited by the survey as naming "reflexive prediction") |

**Verdict for item 4: FOUND.** The fixed-point answer to "can a public prediction be correct" (Grunberg–Modigliani–Simon, via Brouwer or the intermediate value theorem) is 70 years old. So is the cobweb (price oscillation driven by producers' forecasts) and its rational-expectations resolution. The Lucas critique is the model-level version: a policy or published rule changes the structure being modelled.

---

## 5. Goodhart's law

- **Goodhart (1975)**, "Problems of Monetary Management: The U.K. Experience", in *Papers in Monetary Economics*, Reserve Bank of Australia. Reprinted as ch. 4 (pp. 91–121) of Goodhart, *Monetary Theory and Practice* (Macmillan, 1984). Crossref DOIs: chapter 10.1007/978-1-349-17295-5_4; book 10.1007/978-1-349-17295-5 (metadata only). The original wording is quoted from Manheim & Garrabrant, footnote 1 (fetched): "Goodharts Law [1] as originally formulated states that 'any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes.'" The 1975 RBA volume itself was not fetched.
- **Strathern (1997)**, "'Improving ratings': audit in the British University system", *European Review* 5(3):305–321. DOI 10.1002/(SICI)1234-981X(199707)5:3<305::AID-EURO184>3.0.CO;2-4 (Crossref, fetched). **Full text** via https://gwern.net/doc/statistics/decision/1997-strathern.pdf (HTTP 200): "When a measure becomes a target, it ceases to be a good measure. The more a 2.1 examination performance becomes an expectation, the poorer it becomes as a discriminator of individual performances. Hoskin describes this as 'Goodhart's law', after the latter's observation on instruments for monetary control which lead to other devices for monetary flexibility having to be invented."
- **Manheim & Garrabrant**, "Categorizing Variants of Goodhart's Law". arXiv:1803.04585 **v4, 24 Feb 2019**. **Full text.**
  - "a Goodhart effect is when optimization causes a collapse of the statistical relationship between a goal which the optimizer intends and the proxy used for that goal."
  - "Regressional Goodhart - When selecting for a proxy measure, you select not only for the true goal, but also for the difference between the proxy and the goal."
  - "Extremal Goodhart - Worlds in which the proxy takes an extreme value may be very different from the ordinary worlds in which the relationship …"
  - "Causal Goodhart - When the causal path between the proxy and the goal is indirect, intervening can change the relationship between the measure and proxy."
  - Adversarial Goodhart, in two cases: "adversarial misalignment" and "Cobra effects".
  - Footnote 1 notes that "Campbell's law (which arguably has scholarly precedence[3]) and the Lucas critique" are close relatives. Campbell (1979), "Assessing the impact of planned social change", *Evaluation and Program Planning* 2(1):67–90, DOI 10.1016/0149-7189(79)90048-X (Crossref metadata only).
- **In ML.**
  - Karwowski et al., "Goodhart's Law in Reinforcement Learning". arXiv:2310.09144 v1 (13 Oct 2023). "increasing optimisation of an imperfect proxy beyond some critical point decreases performance on the true objective".
  - Gao, Schulman, Hilton, "Scaling Laws for Reward Model Overoptimization". arXiv:2210.10760 v1 (19 Oct 2022). "Because the reward model is an imperfect proxy, optimizing its value too much can hinder ground truth performance, in accordance with Goodhart's law."

**Verdict for item 5: FOUND.** The planned item (iv), where an indicator targeted by an agent with a stake decouples from the goal, is Causal or Adversarial Goodhart in Manheim & Garrabrant's taxonomy.

---

## 6. Reflexivity, Black Wednesday, currency-crisis theory

- **Soros (1987)**, *The Alchemy of Finance*. This is a book with no Crossref record (the query returned unrelated items) and no copy was fetched. **Not verified today; do not cite it except as a title.**
- **Soros (2013)**, "Fallibility, reflexivity, and the human uncertainty principle", *Journal of Economic Methodology* 20(4):309–329. DOI 10.1080/1350178X.2013.859415 (Crossref, fetched). The tandfonline PDF returned **403**. The author's reprint at https://www.georgesoros.com/2014/01/13/fallibility-reflexivity-and-the-human-uncertainty-principle-2/ returned 403 to curl but was read through **[WebFetch]**:
  - "The participants' thinking serves two functions. One is to understand the world in which we live; I call this the cognitive function. The other is to make an impact on the world and to advance the participants' interests; I call this the manipulative function."
  - "When both the cognitive and manipulative functions operate at the same time they may interfere with each other."
  - "A positive feedback process that runs its full course is initially self-reinforcing in one direction, but eventually it is liable to reach a climax or reversal point, after which it becomes self-reinforcing in the opposite direction."
  - WebFetch reported no mention of the 1992 sterling trade in the essay.
- **Black Wednesday, from an authoritative source.** Bank of England *Quarterly Bulletin* 1992 Q4, "Operation of monetary policy" (covers July–September 1992). Fetched https://www.bankofengland.co.uk/-/media/boe/files/quarterly-bulletin/1992/operation-of-monetary-policy-qb-1992-q4.pdf (HTTP 200). **Full text.**
  - "On 16 September, in exceptionally turbulent market conditions and after heavy official purchases of sterling, the United Kingdom suspended sterling's membership of the ERM."
  - "At 11.00 am, with sterling still at its lower ERM limit, it was announced that MLR had been set at 12%".
  - "a rise in MLR to 15% was announced at 2.15 pm, to be effective from the following day. The clearing banks deferred any decision to raise base rates until the next morning and in the event none were raised to 15%."
  - "Just after 7.30 pm, the Chancellor therefore announced sterling's suspension from the ERM and rescinded the decision to raise MLR to 15%."
  - "At 9.30 am MLR was reduced to 10%." (17 September)
  - **Correction to a common telling:** the rise to 15% was announced but never took effect.
- **Soros's short position.** No primary or official source was reachable (the Forbes 1992 flashback returned 403). Britannica, "George Soros" (author Peter Kellner, page last updated 17 Sep 2026), read through **[WebFetch]**:
  - "Through his Quantum group of companies, Soros had sold billions of pounds during the days preceding devaluation, much of it purchased with borrowed money."
  - Fragment: "made a profit of about $1 billion".
  - Figures often repeated in the press ("$10 billion short") were seen only in WebSearch snippets from Wikipedia and trading sites. **Treat the position size as unverified.** The profit of "about $1 billion" rests on Britannica (a secondary source).
- **Obstfeld (1996)**, "Models of currency crises with self-fulfilling features", *European Economic Review* 40(3–5):1037–1047. DOI 10.1016/0014-2921(95)00111-5 (Crossref). NBER WP 5285 (Oct 1995), DOI 10.3386/w5285. Abstract fetched at https://www.nber.org/papers/w5285: "The discomfort a government suffers from speculation against its currency determines the strategic incentives of speculators and the scope for multiple currency-market equilibria. After describing an illustrative model in which high unemployment may cause an exchange-rate crisis with self-fulfilling features, the paper reviews some other self-reinforcing mechanisms."
- **Morris & Shin (1998)**, "Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks", *AER* 88(3):587–597 (JSTOR; no DOI; Crossref query rate-limited). The SFU PDF is an image scan (no text layer). Abstract from EconPapers (RePEc:aea:aecrev:v:88:y:1998:i:3:p:587-97): "Even though self-fulfilling currency attacks lead to multiple equilibria when fundamentals are common knowledge, the authors demonstrate the uniqueness of equilibrium when speculators face a small amount of noise in their signals about the fundamentals. This unique equilibrium depends not only on the fundamentals but also on financial variables, such as the quantity of hot money in circulation and the costs of speculative trading." Heinemann's comment, *AER* 90(1) 2000, full text at economics.mit.edu, adds: "Morris and Shin (1998a) prove the uniqueness of an equilibrium in a model of self-fulfilling currency attacks, when speculators face uncertainty in their signals about macroeconomic fundamentals."
- **Public signals and equilibrium selection** (these bear directly on "the forecast selects the equilibrium"):
  - Morris & Shin (2002), "Social Value of Public Information", *AER* 92(5):1521–1534, DOI 10.1257/000282802762024610 (Crossref). EconPapers abstract: "when agents also have access to independent sources of information, the welfare effect of increased public disclosures is ambiguous."
  - Angeletos & Werning (2006), "Crises and Prices", *AER* 96(5):1720–1736, DOI 10.1257/aer.96.5.1720. Abstract: "The asset price aggregates dispersed private information acting as a public noisy signal … uniqueness may not obtain as a perturbation from perfect information: multiplicity is ensured with small noise."
  - Angeletos, Hellwig, Pavan (2006), "Signaling in a Global Game: Coordination and Policy Traps", *JPE* 114(3):452–484, DOI 10.1086/504901 (metadata only).
- **Recent LLM-and-reflexivity paper.** Park (2026), "Reflexivity as Prompt: Does Awareness of Self-Reinforcing Market Dynamics Improve LLMs as Financial Market Forecasters?". arXiv:2606.00061 v1 (19 May 2026). "Reflexivity theory holds otherwise: prices shape fundamentals, and every forecaster is a participative agent in the loop it analyzes."

**Verdict for item 6: FOUND**, with two caveats. *Alchemy* was not verified, and the size of Soros's position was not verified from a primary source.

---

## 7. Central-bank forecasting and performativity

- **Bernanke (2024)**, *Forecasting for monetary policy making and communication at the Bank of England: a review*. Published 12 April 2024. Fetched https://www.bankofengland.co.uk/independent-evaluation-office/forecasting-for-monetary-policy-making-and-communication-at-the-bank-of-england-a-review/forecasting-for-monetary-policy-making-and-communication-at-the-bank-of-england-a-review (HTTP 200, the HTML review). **Full text.**
  - "Importantly, the MPC's forecast does not necessarily represent the Committee's best guess of what will actually happen to the economy. It is instead a conditional forecast … conditional on a set of variables following exogenously given paths".
  - Performativity, stated directly: "Moreover, if the MPC policy action and communication cause the market curve to shift, as it likely will if the policy action deviates from market expectations, then the market-based conditioning assumption becomes immediately out of date (Goodhart (2009))."
  - "the MPC traditionally used divergences between its conditional rate projections and its own rate expectations to provide a signal to the markets about future policy … However, this device has become less useful in the past decade".
  - Recommendation 9: "the MPC should de-emphasise the central forecast based on the market rate path in its communications".
  - "In some cases, publication of a particular scenario might send a signal the Committee does not want to send or would risk being misleading".
  - "If the public are confident that the central bank is committed to achieving its inflation target in the medium term, the risks of a self-fulfilling, expectations-driven wage-price spiral are much reduced."
  - Footnote: "Goodhart (2023) recommends using alternative scenarios, with endogenous policy responses, in place of point forecasts."
- **David Miles** (External MPC member), "Monetary policy and forward guidance in the UK", speech at Northumbria University, 24 September 2013. Fetched https://www.bankofengland.co.uk/-/media/boe/files/speech/2013/monetary-policy-and-forward-guidance-in-the-uk.pdf (HTTP 200). **Full text.**
  - "there can be multiple equilibrium paths forward. By which I mean that for a given stance of policy there can be different paths for output. On some of them people are more optimistic in a way that is self-confirming. On others, low confidence about activity also becomes self-confirming."
  - "I believe that monetary policy can help to kick the economy onto the better output path. In part this could be done by changing people's expectations about the future."

**Verdict for item 7: FOUND.** Central-bank forecasting openly treats the published forecast as conditional and as something that moves its own conditioning inputs. It also recognises self-confirming multiple equilibria.

---

## 8. AI forecasting companies and LLM "performative forecasting" (2025–2026)

- **Mantic** (London; founders Toby Shevlane and Ben Day). Fetched https://www.mantic.com/ , /launch , /news , https://blog.mantic.com/ , and the Substack archive API (`/api/v1/archive`, 19 posts, 24 Mar–21 Sep 2026). The archive API searches for "self-fulfilling", "performative" and "reflexivity" returned **empty lists**; a control search for "Ebola" returned a post. **No Mantic text on the influence of its forecasts on outcomes was found.** Mantic does publish *conditional* forecasts, e.g. the post title "Republicans will lose 5 more seats if the Fed hikes rates – Friday Forecasts #11" (16 Sep 2026) and "Hormuz and oil conditional forecasting" (17 Jul 2026).
- **Metaculus / Forecasting Research Institute.** The Metaculus FAQ returned **403**. WebSearch found no FRI or Metaculus text on self-fulfilling forecasts. **NOT FOUND.**
- **Other 2025–2026 papers on LLM forecasters and performativity:**
  - Xu et al. (2026), "LLM-based Agents for Forecasting and Prediction: Methods, Training, Evaluation, and Applications". arXiv:2608.23058 v1 (24 Aug 2026). "Future work requires … methods for handling feedback between deployed forecasts and the outcomes being forecast." This names the gap but does not address it.
  - Park (2026), arXiv:2606.00061 (§6): prompting LLMs with reflexivity theory, not measuring the forecasts' own influence.
  - Nechepurenko (2026), "Price as Focal Point: Prediction Markets, Conditional Reflexivity, and the Politics of Common Knowledge". arXiv:2604.24147 v1 (27 Apr 2026). "public probabilities that organize the behavior of voters, donors, journalists, traders, and institutions in ways that can be self-fulfilling or self-defeating … this paper asks whether accurate forecasting is even the right criterion for a market that has become a public coordination device."
  - Beretta, Dianova, Pankratz, Schollmeyer (2025), "AI-Based Forecasting and Market Expectations: A Self-Fulfilling Prophecy?", *Review of Political Economy*, DOI 10.1080/09538259.2025.2562206 (Crossref metadata, published 26 Sep 2025). Full text **403**; there is no abstract in Crossref. The only description seen was a WebSearch snippet ("central bank transparency could unintendedly amplify the predictive power of the AI oracle through feedback loops"), which is **not verified**.
  - Khosrowi, Ahlers, van Basshuysen (2025), "When Predictions are More Than Predictions: Self-Fulfilling Performativity and the Road Towards Morally Responsible Predictive Systems", FAccT 2025, pp. 1108–1118, DOI 10.1145/3715275.3732072 (Crossref metadata). ACM page **403**.
  - Oberman (2026), "Individual Disempowerment through an Advice Channel: Control Loss when Influence is Endogenous". arXiv:2608.14795 v1 (14 Aug 2026). "An oracle rewarded by per-round approval cultivates reliance beyond a closed-form patience threshold … a short enough memory reset removes the incentive to cultivate, while neither recovers the value already steered away."

**Verdict for item 8: PARTIAL.** Performativity is named as open future work for LLM forecasters (Xu et al. 2026). There is no empirical study of a deployed LLM forecaster's own causal effect, and nothing from Mantic, Metaculus or FRI.

---

## 9. Zero stake in one's own influence as a (time-structured) design

These designs remove the predictor's stake in its own influence, several of them by how training data are selected in time:

1. **Counterfactual oracle and erasure** (Armstrong & O'Rorke 2017/18; §3.1). The reward is paid only on episodes whose output is never read. Wei Dai (2019; §3.2) and Christiano restate it as online learning on a randomly selected, output-isolated subset. The data the forecaster learns from contain no read-influence by construction.
2. **Repeated risk minimisation and performative stability** (Perdomo et al. 2020). Retraining on data from the *previous* deployment treats the distribution as fixed. Oesterheld et al. (2023, App. D) make the stake removal explicit as a **stop-gradient** "in front of environment probabilities" and show that the online-gradient version converges to fixed points, not performative optima. Miller et al. (2021) show the cost: such stable points can be "arbitrarily" suboptimal.
3. **Context swapping** (Krueger, Maharaj, Leike 2020). arXiv:2009.09153 v1 (19 Sep 2020), **full text**. "The technique trains N learners in parallel, and shuffles the learners through N different copies of the same (or similar) environments … so that the i-th learner inhabits the j-th environment on time-steps t where j = (i + t) mod N … Under the assumption that different copies of the environment do not influence each other, this technique can address HI-ADS in practice". The abstract defines "auto-induced distributional shift (ADS) … an algorithm causing a change in the distribution of its own inputs". This is an explicitly time-structured way to make each learner's influence land on other learners' data.
4. **Predict the past and consequence-blindness** (Hubinger et al. 2023, §2.4.2–2.4.3; §3.3).
5. **Causal-influence-diagram designs** (abstracts only):
   - Farquhar, Carey, Everitt (2022), "Path-Specific Objectives for Safer Agent Incentives", AAAI 2022, arXiv:2204.10018 v1. "train agents to maximize the causal effect of actions on the expected return which is not mediated by the delicate parts of state … The resulting agents have no incentive to control the delicate state."
   - Everitt, Carey, Langlois, Ortega, Legg (2021), "Agent Incentives: A Causal Perspective", AAAI 2021, arXiv:2102.01685 v2. Defines "instrumental control incentives".
   - Everitt, Hutter, Kumar, Krakovna (2021), "Reward Tampering Problems and Solutions…", *Synthese*, arXiv:1908.04734 v5 (26 Mar 2021). "describe design principles that prevent instrumental goals for two different types of reward tampering".
   - Uesato et al. (2020), "Avoiding Tampering Incentives in Deep RL via Decoupled Approval", arXiv:2011.08827 v1. "combines approval with a decoupled feedback collection procedure".
6. **Estimating and removing the forecast's own causal effect.**
   - Mendler-Dünner, Ding, Wang (2022; §1.3): randomise or record forecasts, then "predict from predictions".
   - Miller et al. (2021): randomised deployments to fit the distribution map.
   - Bottou et al. (2013): randomisation in a live ad system.
   - Cheng, Hardt, Mendler-Dünner (2023/2024): identification without randomisation.
   - Boeken et al. (2025; §2.3): condition on covariates that make the target "forecast-invariant".
   - Lee & Zrnic (2026; §1.6): performative plus exogenous drift ("partially performative prediction").
7. **Memory reset** (Oberman 2026; §8): "a short enough memory reset removes the incentive to cultivate". This is a time-structured bound on stake.

**Not found.** No fetched source does all three of the following:
- (a) uses the erasure lottery of a counterfactual oracle as a randomised instrument to *estimate* the forecast's read-effect;
- (b) subtracts that estimate from the outcomes of read episodes so the forecaster can learn from **all** episodes while keeping zero stake;
- (c) compares this with a pure counterfactual oracle under drift.

Each ingredient is published: erasure (Armstrong), randomised forecasts identify the effect (Mendler-Dünner et al.), drift plus performativity (Lee & Zrnic), and the online random-subset framing (Dai/Christiano). The combination appears to be a recombination of known parts. This is a negative result of a limited search, not a proof of novelty.

**Verdict for item 9: PARTIAL.** Zero-stake designs and time-structured stake removal (erasure, context swapping, stop-gradient or RRM, memory reset, predict-the-past) are established. The specific step of estimating the effect from erased episodes and deconfounding the whole training record was not found.

---

## 10. Mapping to the planned synthetic tests (i)–(v)

| Planned test | Closest prior art (fetched today) | Status |
|---|---|---|
| (i) Trade-off between accuracy-when-read and influence | Armstrong & O'Rorke 2018: the counterfactual oracle's read-episode error "doesn't tend to zero". Oesterheld et al. 2023: bounds on the inaccuracy of score-maximising reports as a function of influence, and near-fixed-point scoring rules only when influence is bounded. Kim & Perdomo 2023: "tension between … forecasting outcomes accurately and steering". Rodemann et al. 2026: "the more a model affects data, the less it can learn from it". Miller et al. 2021: stable points can be arbitrarily suboptimal. | Known qualitatively and partly formally. An explicit accuracy-versus-influence frontier on a synthetic world, as a plotted curve, was not found as such. It would be a demonstration, not a new idea. |
| (ii) Retraining on self-influenced data (stability, cobweb, spirals) | Perdomo et al. 2020 (ε < γ/β; divergence), Brown et al. 2022 (stateful), Mendler-Dünner et al. 2020 (lazy vs greedy), Kabra & Patel 2024, Farina & Perdomo 2026, Taori & Hashimoto 2022, Chaney et al. 2018, Krueger et al. 2020. Economics: Ezekiel 1938 and Muth 1961 on the cobweb. Nagarajan & Ashok 2026: "Retraining is therefore a cobweb map". | Fully known. |
| (iii) Bistable self-fulfilling world; the forecast selects the equilibrium; the accuracy-maximiser prefers the most predictable one | Oesterheld et al. 2023: Example 3 (bank run, three fixed points) and Prop. 4 (the maximiser picks extreme points of the fixed-point set; "fixed points with lower entropy"). Hubinger et al. 2023: "incentive to find a fixed point that is both stable and likely". Armstrong 2019: accurate predictions only "at the extreme of the range". Obstfeld 1996 (multiple equilibria in currency attacks); Morris & Shin 1998 (uniqueness with noisy private signals); Morris & Shin 2002 and Angeletos & Werning 2006 (public signals and multiplicity); Miles 2013 (self-confirming equilibrium paths). | The mechanism and the preference for the most predictable equilibrium are published (bank-run form, proper scoring rules). The currency-peg dressing is a change of instance, not of result. |
| (iv) Goodhart: an indicator targeted with a stake decouples from the goal | Goodhart 1975 wording; Strathern 1997; Campbell 1979; Lucas 1976; Manheim & Garrabrant 2018 (causal and adversarial variants); Karwowski et al. 2023; Gao et al. 2022. | Fully known. |
| (v) Counterfactual oracle vs a forecaster that estimates its own effect from erased episodes and removes it from all outcomes, in a drifting world | Oracle: Armstrong & O'Rorke; Dai 2019; Hubinger et al. 2023. Effect estimation: Mendler-Dünner et al. 2022; Miller et al. 2021; Bottou et al. 2013; Cheng et al. Drift: Lee & Zrnic 2026. | The pieces are known; this combination and head-to-head comparison were **not found**. |

---

## Final summary table

| Item | Verdict | What exactly is known |
|---|---|---|
| 1. Performative prediction (Perdomo 2020; Miller 2021; Mendler-Dünner 2022; Hardt 2022; Brown 2022) | **FOUND** | Performative stability (the fixed point of retraining) vs optimality. RRM converges linearly if ε < γ/β and can diverge otherwise. Stable points can be arbitrarily suboptimal. Stateful and lazy/greedy variants. The causal effect of predictions is identifiable when forecasts are randomised or recorded. Performative power measures the stake. |
| 2. Proper scoring rules under performativity (Oesterheld 2023; Armstrong 2019; Boeken 2025) | **FOUND** | Score-maximising reports are generally not fixed points, even when a unique fixed point exists. Among multiple fixed points the maximiser picks extreme (lower-entropy) ones (Prop. 4). Near-fixed-point incentives exist only for binary outcomes with bounded influence. Performative stability or a stop-gradient incentivises fixed points. Self-confirming predictions can be arbitrarily far from the no-prediction outcome. |
| 3. Oracles (Armstrong & O'Rorke 2017/18; Hubinger 2023) | **FOUND** | Counterfactual oracle rewarded only on erasure, with the target E(F given erasure). A demonstrated read-episode error that does not vanish. Self-fulfilling prophecy as a major risk of predictors. Remedies: RNG-conditioned non-reading, predicting the past, consequence-blindness. |
| 4. Economics classics (Grunberg & Modigliani 1954; Simon 1954; Merton 1948; Muth 1961; Ezekiel 1938; Lucas 1976; Morgenstern) | **FOUND** (metadata for Ezekiel, Simon, G&M, Morgenstern 1935; full text for Merton, Muth, Lucas) | Correct public predictions exist by fixed-point continuity (GMS). Self-fulfilling prophecy defined (Merton). Cobweb oscillation from producers' expectations and its rational-expectations resolution (Muth). Policy changes model structure (Lucas). Published forecasts invalidate themselves (Morgenstern, per the survey). |
| 5. Goodhart (1975/1984; Strathern 1997; Manheim & Garrabrant 2018) | **FOUND** | The original wording ("any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes"). Strathern's "When a measure becomes a target, it ceases to be a good measure." The regressional, extremal, causal and adversarial taxonomy. RL and reward-model overoptimisation evidence. |
| 6. Reflexivity and currency crises (Soros 1987/2013; Black Wednesday; Obstfeld 1996; Morris & Shin 1998) | **FOUND** (Alchemy not verified; Soros position size not verified) | Soros's cognitive and manipulative functions and self-reinforcing boom-bust. BoE QB 1992 Q4: MLR 12% at 11:00, 15% announced at 14:15 for the next day (never effective), ERM suspended just after 19:30, and MLR back to 10% on 17 Sep. Britannica: Soros profit "about $1 billion". Multiple equilibria in currency attacks (Obstfeld); uniqueness under noisy private signals (Morris & Shin); public signals restore multiplicity (Angeletos & Werning). |
| 7. Central-bank forecasting (Bernanke Review, Apr 2024; BoE speech) | **FOUND** | The BoE forecast is conditional on the market rate path. Policy and communication shift that path, making the assumption "immediately out of date". Recommendation 9 de-emphasises the market-path central forecast in favour of scenarios. Publishing a scenario can "send a signal". Miles 2013: multiple self-confirming equilibrium paths, and policy can pick the better one through expectations. |
| 8. AI forecasting companies and LLM performative forecasting | **PARTIAL** | Performativity is named as open work for LLM forecasting agents (Xu et al. 2026). Park 2026 prompts LLMs with reflexivity. Prediction markets act as coordination devices (Nechepurenko 2026). Nothing from Mantic (conditional forecasts only; archive search empty), Metaculus or FRI. Beretta et al. 2025 and Khosrowi et al. 2025 were not readable (403). |
| 9. Time-structured zero stake (removing forecast influence from later training data) | **PARTIAL** | Erasure (training only on unread episodes). Online random-subset training (Dai/Christiano). RRM and stop-gradient (optimise against the previous deployment's data). Context swapping (rotating learners across environment copies every step). Memory reset (Oberman 2026). Predict-the-past. Path-specific objectives. Randomised forecasts identify the effect (Mendler-Dünner). **Not found:** estimating the read-effect from erased episodes and subtracting it from read outcomes so the forecaster trains on all data under drift, compared against a pure counterfactual oracle. |
