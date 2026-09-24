# Literature check: contemplative and somatic practice, equanimity, and "holding a representation lightly"

**Fetch date for every source below: 2026-09-24 (UTC, roughly 17:45 to 19:00).**
The retrieval routes were the Crossref REST API (metadata, sometimes abstracts), the Europe PMC REST API (abstracts, and full-text XML for PMC open-access items), the PubMed E-utilities/MCP, arXiv abs pages and PDFs, the OSF API (PsyArXiv), the Zenodo API, author and repository PDFs (text pulled with pdfminer), publisher landing pages, and WebSearch to find leads.
Every quotation below was copied from text fetched today, with one exception that is marked. Where a search-engine summary was the only source available, the entry says **SNIPPET ONLY, not verified verbatim**.

**What was blocked or failed today (R10):**
- Springer `link.springer.com` article pages redirected to an auth wall (303 to idp.springer.com). I used Crossref/Europe PMC abstracts or open repository copies instead.
- `tandfonline.com` and `sciencedirect.com` returned HTTP 403.
- `nature.com` article pages returned an empty stub. Kandasamy 2016 was read from Europe PMC full-text XML instead.
- `alignmentforum.org` returned 403.
- The OpenAlex API hit its daily budget (rate limit) after the first call. The Semantic Scholar API returned 429 some of the time.
- The Lebuda et al. 2016 abstract could not be fetched verbatim. Only a search snippet is available.
- The Hafenbrack & Vohs 2018 abstract came through Semantic Scholar (publisher abstract relayed). Access level: abstract.
- The Lehrer et al. 2020 meta-analysis has a Crossref-registered **correction** (10.1007/s10484-021-09526-y, 2021-10-08). Its content was not retrievable (no abstract, paywalled).
- The Starcke & Brand 2016 meta-analysis carries an erratum. Its text is included in the Crossref abstract (quoted below).

Access levels used: **FT** = full text read. **FT-AM** = author manuscript or accepted manuscript read. **ABS** = abstract only. **SNIP** = search snippet only.

---

## 1. Decentering and metacognitive awareness

**Teasdale, J. D., Moore, R. G., Hayhurst, H., Pope, M., Williams, S., & Segal, Z. V. (2002).** Metacognitive awareness and prevention of relapse in depression: empirical evidence. *J Consult Clin Psychol*, 70(2), 275–287. DOI [10.1037/0022-006X.70.2.275](https://doi.org/10.1037/0022-006X.70.2.275); PMID 11952186 (retrieved via PubMed). ABS.
> "Metacognitive awareness is a cognitive set in which negative thoughts/feelings are experienced as mental events, rather than as the self."
> "CT and MBCT may reduce relapse by changing relationships to negative thoughts rather than by changing belief in thought content."

**Fresco, D. M., Moore, M. T., van Dulmen, M. H. M., Segal, Z. V., Ma, S. H., Teasdale, J. D., & Williams, J. M. G. (2007).** Initial psychometric properties of the Experiences Questionnaire: validation of a self-report measure of decentering. *Behavior Therapy*, 38, 234–246. DOI [10.1016/j.beth.2006.08.003](https://doi.org/10.1016/j.beth.2006.08.003). ABS (Europe PMC).
> "Decentering is defined as the ability to observe one's thoughts and feelings as temporary, objective events in the mind, as opposed to reflections of the self that are necessarily true."
> "Findings from this series of studies offer initial support for the EQ as a measure of decentering."

**Bernstein, A., Hadash, Y., Lichtash, Y., Tanay, G., Shepherd, K., & Fresco, D. M. (2015).** Decentering and related constructs: A critical review and metacognitive processes model. *Perspectives on Psychological Science*, 10, 599–617. DOI [10.1177/1745691615594577](https://doi.org/10.1177/1745691615594577). ABS.
> "we propose that, to varying degrees, decentering-related constructs reflect a common mental phenomenon subserved by three interrelated metacognitive processes: meta-awareness, disidentification from internal experience, and reduced reactivity to thought content."

**Status of the MBCT outcome (context).** Kuyken, W., et al. (2016). Efficacy of mindfulness-based cognitive therapy in prevention of depressive relapse: an individual patient data meta-analysis from randomized trials. *JAMA Psychiatry*, 73(6), 565. DOI [10.1001/jamapsychiatry.2016.0076](https://doi.org/10.1001/jamapsychiatry.2016.0076). ABS.
> "patients receiving MBCT had a reduced risk of depressive relapse within a 60-week follow-up period compared with those who did not receive MBCT (hazard ratio, 0.69; 95% CI, 0.58-0.82)"

**Status of the mechanism.** Gu, J., Strauss, C., Bond, R., & Cavanagh, K. (2015). How do MBCT and MBSR improve mental health and wellbeing? A systematic review and meta-analysis of mediation studies. *Clinical Psychology Review*, 37, 1–12. DOI [10.1016/j.cpr.2015.01.006](https://doi.org/10.1016/j.cpr.2015.01.006) (Crossref lists an erratum, 10.1016/j.cpr.2016.09.011). ABS.
> "This review identified strong, consistent evidence for cognitive and emotional reactivity, moderate and consistent evidence for mindfulness, rumination, and worry, and preliminary but insufficient evidence for self-compassion and psychological flexibility as mechanisms"
> "Most reviewed mediation studies have several key methodological shortcomings which preclude robust conclusions regarding mediation."

**Related, and closest to "judging one's own case":** Grossmann, I., & Kross, E. (2014). Exploring Solomon's paradox: Self-distancing eliminates the self-other asymmetry in wise reasoning about close relationships in younger and older adults. *Psychological Science*, 25, 1571–1580. DOI [10.1177/0956797614535400](https://doi.org/10.1177/0956797614535400). ABS.
> "participants displayed wiser reasoning (i.e., recognizing the limits of their knowledge and the importance of compromise and future change, considering other people's perspectives) about another person's problems compared with their own. Across Studies 2 and 3, instructing individuals to self-distance (rather than self-immerse) eliminated this asymmetry."

Replication status: today's search found no independent direct replication. It was not checked exhaustively.

**Reading.** Decentering is a well-defined construct. The phrase "thoughts as mental events, not the self" is the field's own wording, so the note can quote it. The evidence has four limits:
- It is overwhelmingly from depression and clinical samples, and it rests on self-report (the EQ).
- MBCT's relapse benefit is replicated at the IPD level.
- That decentering *mediates* the benefit is only moderately supported, and the mediation designs are weak (Gu 2015).
- No evidence was found that decentering training changes how scientists or engineers hold *models, forecasts or plans*. That extension is an extrapolation.

---

## 2. Mindfulness and the sunk-cost bias

**Hafenbrack, A. C., Kinias, Z., & Barsade, S. G. (2014).** Debiasing the mind through meditation: mindfulness and the sunk-cost bias. *Psychological Science*, 25(2), 369–376 (online 2013-12-06). DOI [10.1177/0956797613503853](https://doi.org/10.1177/0956797613503853); PMID 24317419. FT (author copy, Wharton faculty site).
> "the results suggest that increased mindfulness reduces the tendency to allow unrecoverable prior costs to influence current decisions." (abstract)
> "The percentage of participants in the mindfulness condition who resisted the sunk-cost bias (78%) was higher than the percentage of participants in the control condition who resisted the sunk-cost bias (44%), χ2(1, N = 57) = 7.024, p = .004, Φ = 0.35"
> "An alpha level of .05, one-tailed, was used for all hypothesis tests."

Caveats computed from the paper's own numbers:
- Study 2a has N = 57 and Study 2b has N = 109. Each outcome is a single vignette choice.
- The tests are one-tailed. The reported χ² values give two-tailed p of 0.008 (χ² = 7.024) and 0.012 (χ² = 6.35). I computed these today from the printed statistics.
- Participants with asthma were excluded because the induction was a breathing meditation.

**Replication attempts:**

**Williams, E. C., & Polito, V. (2022).** Meditation in the workplace: Does mindfulness reduce bias and increase organisational citizenship behaviours? *Frontiers in Psychology*, 13, 747983. DOI [10.3389/fpsyg.2022.747983](https://doi.org/10.3389/fpsyg.2022.747983); PMC9035788. FT (Europe PMC XML).
> "While meditation significantly increased OCB intent, predictions relating to bias were not supported." (abstract)
> Experiment 1 (working adults, n = 47, repeated measures): "showed no significant difference in Sunk-Cost Resistance between the mindfulness ( M = 0.38, SD = 0.49) and control interventions ( M = 0.43, SD = 0.50), Wald χ 2 (1, N = 94) = 1.01, p = 0.315, OR = 1.19."
> Experiment 2 (students, N = 119): "showed no significant difference in Sunk-Cost Resistance scores between the mindfulness or control interventions, χ 2 (2, N = 119) = 1.10, p = 0.577, OR = 1.14."
> "outside of clinical research, mindfulness studies have rarely been replicated."

**Schmitzer-Torbert, N. (2020).** Mindfulness and decision making: sunk costs or escalation of commitment? *Cognitive Processing*, 21, 391–402. DOI [10.1007/s10339-020-00978-4](https://doi.org/10.1007/s10339-020-00978-4). ABS (Crossref; the Springer page was blocked).
> "trait mindfulness was most consistently related to reduced escalation of commitment, whereas the relationship between trait mindfulness and resistance to the effects of sunk costs was less consistently observed."

**Adjacent null (a different construct, Langerian or socio-cognitive mindfulness):** Thiedmann, P., Dejardin, F., Reiter, L., & Tran, U. S. (2025). Brief online socio-cognitive mindfulness interventions neither improve socio-cognitive mindfulness nor cognitive biases: a two-study conceptual replication and reanalysis of a randomized controlled trial. *Mindfulness*, 16, 1555–1568. DOI [10.1007/s12671-025-02575-y](https://doi.org/10.1007/s12671-025-02575-y). FT (open PDF via d-nb.info). Preregistered (aspredicted #93190, #127897), n = 591 and n = 335.
> "Intervention and control groups did not differ in cognitive-bias task performance or socio-cognitive mindfulness in either the two replication studies or the original RCT"

**Adjacent finding on motivation:** Hafenbrack, A. C., & Vohs, K. D. (2018). Mindfulness meditation impairs task motivation but not performance. *OBHDP*, 147, 1–15. DOI [10.1016/j.obhdp.2018.05.001](https://doi.org/10.1016/j.obhdp.2018.05.001). ABS (via Semantic Scholar).
> "Mindfulness inductions, relative to comparison conditions, reduced motivation to tackle mundane tasks (Experiments 1–4) and pleasant tasks (Experiment 2)."
> "inducing a state of mindfulness did not affect task performance"

**Reading.** The sunk-cost effect is **contested**:
- The original has small samples and one-tailed tests.
- The only experimental replications found (two, preregistration not stated) were null.
- The trait-level association is inconsistent for sunk cost and more consistent for escalation of commitment.
- No large preregistered direct replication was found. PubMed returns only the original and Williams & Polito for (mindfulness OR meditation) AND sunk-cost/escalation.

**Do not cite Hafenbrack 2014 as established.**

---

## 3. Decision-making, cognition, creativity, workplace; meta-analyses, critiques, harms

**Goldberg, S. B., Riordan, K. M., Sun, S., & Davidson, R. J. (2022).** The empirical status of mindfulness-based interventions: A systematic review of 44 meta-analyses of randomized controlled trials. *Perspectives on Psychological Science*, 17, 108–130 (online 2021-02-16). DOI [10.1177/1745691620968771](https://doi.org/10.1177/1745691620968771). ABS.
> "MBIs showed superiority to passive controls across most PICOS (ds = 0.10-0.89). Effects were typically smaller and less often statistically significant compared with active controls."
> "Statistical power may be lacking in meta-analyses, particularly for comparisons with active controls."

**Van Dam, N. T., et al. (2018).** Mind the hype: A critical evaluation and prescriptive agenda for research on mindfulness and meditation. *Perspectives on Psychological Science*, 13, 36–61. DOI [10.1177/1745691617709589](https://doi.org/10.1177/1745691617709589). ABS.
> "Misinformation and poor methodology associated with past studies of mindfulness may lead public consumers to be harmed, misled, and disappointed."

**Whitfield, T., et al. (2022).** The effect of mindfulness-based programs on cognitive function in adults: A systematic review and meta-analysis. *Neuropsychology Review*, 32, 677–702. DOI [10.1007/s11065-021-09519-y](https://doi.org/10.1007/s11065-021-09519-y). ABS.
> "the summary effect size for all studies favored MBPs over comparators and was small in magnitude (g = 0.15; [0.05, 0.24])"
> "Across all studies, MBPs outperformed inactive, but not active comparators."

**Creativity.** Lebuda, I., Zabelina, D. L., & Karwowski, M. (2016). Mind full of ideas: A meta-analysis of the mindfulness–creativity link. *Personality and Individual Differences*, 93, 22–26. DOI [10.1016/j.paid.2015.09.040](https://doi.org/10.1016/j.paid.2015.09.040). **SNIPPET ONLY, not verified verbatim.** The search summary says: 89 correlations from 20 samples, r = .22, moderated by mindfulness facet. The data are correlational.

Hughes, Z., Ball, L. J., Richardson, C., & Judge, J. (2023). A meta-analytical review of the impact of mindfulness on creativity. *Psychonomic Bulletin & Review*, 30, 2155–2186. DOI [10.3758/s13423-023-02327-w](https://doi.org/10.3758/s13423-023-02327-w). ABS.
> "Findings relating to the impact of mindfulness interventions on creative performance remain inconsistent"
> "A positive effect was identified between mindfulness and creativity, both for control group designs (d = 0.42, 95% CIs [0.29, 0.54]) and pretest-posttest designs (d = 0.59 ...)"
> The abstract also reports "more advantageous outcomes for convergent as opposed to divergent thinking tasks."

**Workplace.** Lomas, T., Medina, J. C., Ivtzan, I., Rupprecht, S., & Eiroa-Orosa, F. J. (2019). Mindfulness-based interventions in the workplace: An inclusive systematic review and meta-analysis of their impact upon wellbeing. *J Positive Psychology*, 14, 625–640 (online 2018-09-30). DOI [10.1080/17439760.2018.1519588](https://doi.org/10.1080/17439760.2018.1519588). ABS (via Semantic Scholar).
> The review pooled "35 randomized controlled trials".
> "job performance (SMD = 0.43)"
> "no effects were observed for emotional regulation. However, the quality of the studies was inconsistent"

Bartlett, L., et al. (2019). A systematic review and meta-analysis of workplace mindfulness training randomized controlled trials. *J Occup Health Psychol*, 24, 108–126. DOI [10.1037/ocp0000146](https://doi.org/10.1037/ocp0000146). ABS.
> "No conclusions could be drawn from pooled data for burnout due to ambivalence in results, for depression due to publication bias, or for work performance due to insufficient data."

Vonderlin, R., Biermann, M., Bohus, M., & Lyssenko, L. (2020). Mindfulness-based programs in the workplace: a meta-analysis of randomized controlled trials. *Mindfulness*, 11, 1579–1598. DOI [10.1007/s12671-020-01328-3](https://doi.org/10.1007/s12671-020-01328-3). ABS.
> "Results on work engagement and productivity were limited by low numbers of primary studies with outliers among their effect sizes."

**Vainre, M., Dalgleish, T., et al. (2025).** Mindfulness-based programmes for work performance: A systematic review and meta-analysis of randomised controlled trials. *Stress and Health*, 41 (Dec 2025), e70123. DOI [10.1002/smi.70123](https://doi.org/10.1002/smi.70123). ABS. This is the most recent and most rigorous synthesis found.
> "MBPs were found to improve task performance at post-intervention compared to passive control groups (k = 22, Hedges' g = 0.25, 95% CI 0.06-0.44, p = 0.01, I2 = 81.48%) but not compared to active control groups (k = 4, Hedges' g = 0.12, 95% CI -0.3-0.55, p = 0.43, I2 = 62.87%)."
> "Confidence in the review results, per Grading of Recommendations Assessment, Development and Evaluation (GRADE), is very low."

**Population-level nulls.** Fleming, W. J. (2024). Employee well-being outcomes from individual-level mental health interventions: Cross-sectional evidence from the United Kingdom. *Industrial Relations Journal*, 55, 162–182. DOI [10.1111/irj.12418](https://doi.org/10.1111/irj.12418). ABS. The design is cross-sectional (N = 46,336, 233 organisations), so selection bias is possible, and the paper addresses it.
> "Across multiple subjective well-being indicators, participants appear no better off."

Kuyken, W., et al. (2022). MYRIAD cluster randomised controlled trial. *Evidence-Based Mental Health*, 25, 99–109. DOI [10.1136/ebmental-2021-300396](https://doi.org/10.1136/ebmental-2021-300396). ABS. The sample was adolescents in 84 schools, n = 8,376.
> "Findings do not support the superiority of SBMT over TAU in promoting mental health in adolescence."

**Galante, J., et al. (2023).** IPD meta-analysis of mindfulness-based programs for mental health promotion. *Nature Mental Health*, 1, 462–476. DOI [10.1038/s44220-023-00081-5](https://doi.org/10.1038/s44220-023-00081-5). ABS (Crossref).
> "MBPs reduced average distress between one- and six-months post-intervention with a small to moderate effect size (standardised mean difference (SMD) -0.32; 95% confidence interval (CI) -0.41 to -0.24"
> "More research is needed to identify sources of variability in outcomes at an individual level."

**Adverse effects.** Britton, W. B., Lindahl, J. R., Cooper, D. J., Canby, N. K., & Palitsky, R. (2021). Defining and measuring meditation-related adverse effects in mindfulness-based programs. *Clinical Psychological Science*, 9, 1185–1204. DOI [10.1177/2167702621996340](https://doi.org/10.1177/2167702621996340). ABS. n = 96, MBCT variants.
> "Meditation-related adverse effects (MRAEs) with negative valences or negative impacts on functioning occurred in 58% and 37% of the sample, respectively. Lasting bad effects occurred in 6-14% of the sample"
> "Meditation practice in MBPs is associated with transient distress and negative impacts at similar rates to other psychological treatments."

Farias, M., Maraldi, E., Wallenkampf, K. C., & Lucchetti, G. (2020). Adverse events in meditation practices and meditation-based therapies: a systematic review. *Acta Psychiatrica Scandinavica*, 142, 374–393. DOI [10.1111/acps.13225](https://doi.org/10.1111/acps.13225). ABS.
> "The total prevalence of adverse events was 8.3% (95% CI 0.05-0.12), though this varied considerably across types of studies - 3.7% ... for experimental and 33.2% ... for observational studies."
> The review found adverse events "may occur in individuals with no previous history of mental health problems."

Lindahl, J. R., Fisher, N. E., Cooper, D. J., Rosen, R. K., & Britton, W. B. (2017). The varieties of contemplative experience. *PLOS ONE*, 12, e0176239. DOI [10.1371/journal.pone.0176239](https://doi.org/10.1371/journal.pone.0176239). ABS.
> "the associated level of distress and functional impairment ranged from minimal and transient to severe and enduring."

The domains of the 59-experience taxonomy include "sense of self". This matters for any programme that aims at loosening self-identification.

**Reading.**
- Cognitive effects are small (g ≈ 0.15), and they are **not** reliably better than active controls.
- Work-performance effects are g ≈ 0.25 against passive controls, non-significant against active controls, at GRADE very low certainty.
- Well-being effects are real but modest (SMD ≈ −0.3). They are heterogeneous, and large universal rollouts have been null (MYRIAD; Fleming, which is cross-sectional).
- Harms are non-trivial, and the "sense of self" category is one of the named harm domains.

---

## 4. Equanimity as a construct

**Desbordes, G., Gard, T., Hoge, E. A., Hölzel, B. K., Kerr, C., Lazar, S. W., Olendzki, A., & Vago, D. R. (2015).** Moving beyond mindfulness: Defining equanimity as an outcome measure in meditation and contemplative research. *Mindfulness*, 6, 356–372 (online 2014-01-21). DOI [10.1007/s12671-013-0269-8](https://doi.org/10.1007/s12671-013-0269-8). ABS.
> "Equanimity can be defined as an even-minded mental state or dispositional tendency toward all experiences or objects, regardless of their origin or their affective valence (pleasant, unpleasant, or neutral)."
> "we propose that equanimity captures potentially the most important psychological element in the improvement of well-being"

This is a proposal paper, not a test.

**Hadash, Y., Segev, N., Tanay, G., Goldstein, P., & Bernstein, A. (2016).** The decoupling model of equanimity: Theory, measurement, and test in a mindfulness intervention. *Mindfulness*, 7(5), 1214–1226. DOI [10.1007/s12671-016-0564-2](https://doi.org/10.1007/s12671-016-0564-2). The DOI in the brief was not given; this one was found via search and is Crossref-confirmed. ABS (University of Haifa CRIS page).
> "conceptualizing equanimity as the decoupling of desire (wanting and not wanting) from the hedonic tone of current or anticipated experience (pleasant and unpleasant)"
> "mindfulness training led to reductions in reactivity to unpleasant hedonic tone over time, as a function of responding to the training (i.e., elevation in state mindfulness). However, training did not lead to expected elevations in attitude of acceptance, regardless of degree of responding to the training."

Shoham, A., Hadash, Y., & Bernstein, A. (2018). Examining the decoupling model of equanimity in mindfulness training: an intensive experience sampling study. *Clinical Psychological Science*, 6, 704–720. DOI [10.1177/2167702618770446](https://doi.org/10.1177/2167702618770446). ABS. n = 82, no control arm stated in the abstract.
> "Mindfulness may therefore function to decouple desire (wanting and not wanting) from the hedonic tone of experience (pleasant and unpleasant)."

**Juneau, C., Pellerin, N., Trives, E., Ricard, M., Shankland, R., & Dambrun, M. (2020).** Reliability and validity of an equanimity questionnaire: the two-factor equanimity scale (EQUA-S). *PeerJ*, 8, e9405. DOI [10.7717/peerj.9405](https://doi.org/10.7717/peerj.9405). ABS.

Note: this is a scale-development paper, not a review. The brief's "Juneau et al. 2020 review" appears to refer to it. The systematic review is Weber 2021, below.
> "relatively few studies have empirically examined equanimity and measurement instruments are still lacking."
> The factor analysis found "two dimensions of equanimity: an even-minded state of mind (E-MSM) and a hedonic independence (HI) component." The sample was N = 265 and cross-sectional.

**Weber, J. (2021).** A systematic literature review of equanimity in mindfulness based interventions. *Pastoral Psychology*, 70, 151–165. DOI [10.1007/s11089-021-00945-6](https://doi.org/10.1007/s11089-021-00945-6). FT-AM (University of Bolton repository, accepted manuscript).
> "The review found that there is limited standardized inclusion of equanimity and poor reliability and generalizability surrounding this construct. Furthermore, there are no explicit instruments for measuring equanimity."

The search window was 2010–2018, and nine studies were included.

**Closest causal evidence for an "acceptance/equanimity" component:** Lindsay, E. K., Young, S., Smyth, J. M., Brown, K. W., & Creswell, J. D. (2018). Acceptance lowers stress reactivity: Dismantling mindfulness training in a randomized controlled trial. *Psychoneuroendocrinology*, 87, 63–73. DOI [10.1016/j.psyneuen.2017.09.015](https://doi.org/10.1016/j.psyneuen.2017.09.015). ABS. n = 153.
> "Monitor+Accept training reduced cortisol and systolic blood pressure reactivity compared to Monitor Only and control trainings. Participants in all three conditions reported moderate levels of subjective stress."

**Reading.** In this literature, "equanimity" means non-reactivity to the **hedonic tone** of experience. It does not mean non-attachment to being *right* about a belief. That mapping is the note's own. Measurement is young (EQUA-S 2020, the Hadash scale, ES-16), and the 2021 review calls reliability and generalisability poor. The evidence that training raises equanimity is mixed: Hadash found reactivity changed but acceptance did not. Lindsay 2018 is a single dismantling trial on physiological reactivity.

---

## 5. Somatic and interoceptive practice, HRV biofeedback, breathwork, stress and decisions

**Garfinkel, S. N., Seth, A. K., Barrett, A. B., Suzuki, K., & Critchley, H. D. (2015).** Knowing your own heart: Distinguishing interoceptive accuracy from interoceptive awareness. *Biological Psychology*, 104, 65–74. DOI [10.1016/j.biopsycho.2014.11.004](https://doi.org/10.1016/j.biopsycho.2014.11.004). ABS. N = 80.
> "In a normative sample (N=80), all three dimensions were distinct and dissociable. Interoceptive accuracy was only partly predicted by interoceptive awareness and interoceptive sensibility."

**Farb, N., et al. (2015).** Interoception, contemplative practice, and health. *Frontiers in Psychology*, 6, 763. DOI [10.3389/fpsyg.2015.00763](https://doi.org/10.3389/fpsyg.2015.00763). ABS. This is a theoretical and integrative review.
> "we introduce an expanded taxonomy of interoceptive processes, arguing that many of these processes can be understood through an emerging predictive coding model for mind-body integration."
> "contemplative practices may attenuate these interpretative biases, restoring a person's sense of presence and agency in the world."

**Measurement caveat.** Zamariola, G., Maurage, P., Luminet, O., & Corneille, O. (2018). Interoceptive accuracy scores from the heartbeat counting task are problematic: Evidence from simple bivariate correlations. *Biological Psychology*, 137, 12–17. DOI [10.1016/j.biopsycho.2018.06.006](https://doi.org/10.1016/j.biopsycho.2018.06.006). ABS. N = 572.
> "these scores massively (i.e., > 95%) reflect under-reports. Of concern too, the correlation between actual and reported heartbeats is low overall (r = .16)"

**Mindfulness and self-reported interoception.** Treves, I. N., ... Goldberg, S. B., Mehling, W., Schuman-Olivier, Z., & Khalsa, S. S. (2025). A meta-analysis of the effects of mindfulness meditation training on self-reported interoception. *Scientific Reports*. DOI [10.1038/s41598-025-22661-4](https://doi.org/10.1038/s41598-025-22661-4). ABS (Europe PMC). Preregistered, 29 RCTs.
> "Results showed a small-to-medium positive effect on interoception measures across all studies (g = 0.31, p < 0.001, 95% CI [0.21, 0.42])"

Note: this is *self-reported* interoception, not accuracy.

**Interoception and financial decisions (often cited).** Kandasamy, N., Garfinkel, S. N., Page, L., Hardy, B., Critchley, H. D., Gurnell, M., & Coates, J. M. (2016). Interoceptive ability predicts survival on a London trading floor. *Scientific Reports*, 6, 32986. DOI [10.1038/srep32986](https://doi.org/10.1038/srep32986); PMC5027524. FT (Europe PMC XML).
> "We recruited 18 male traders engaged in high frequency trading."
> "the interoceptive ability of traders predicted their relative profitability, and strikingly, how long they survived in the financial markets." (abstract)

Caveats:
- n = 18, and the design is correlational.
- The study used a heartbeat-detection/counting paradigm, the class of task criticised by Zamariola 2018.
- Today's search found no replication.

**HRV biofeedback.** Lehrer, P., et al. (2020). Heart rate variability biofeedback improves emotional and physical health and performance: A systematic review and meta analysis. *Applied Psychophysiology and Biofeedback*, 45, 109–129. DOI [10.1007/s10484-020-09466-z](https://doi.org/10.1007/s10484-020-09466-z). ABS. A **correction** exists (10.1007/s10484-021-09526-y); its content was not retrieved.
> "A significant small to moderate effect size was found favoring HRVB, which does not differ from that of other effective treatments."
> "Effect sizes are larger in comparison to inactive than active control conditions although significant for both."
> "Further research is needed to confirm its efficacy for particular applications."

Goessl, V. C., Curtiss, J. E., & Hofmann, S. G. (2017). The effect of heart rate variability biofeedback training on stress and anxiety: a meta-analysis. *Psychological Medicine*, 47, 2578–2586. DOI [10.1017/S0033291717001003](https://doi.org/10.1017/S0033291717001003). ABS. 24 studies, 484 participants, self-report outcomes.
> "The between-groups analysis comparing biofeedback to a control condition yielded Hedges' g = 0.83."
> "Although more well-controlled studies are needed"

**Breathwork.** Fincham, G. W., Strauss, C., Montero-Marin, J., & Cavanagh, K. (2023). Effect of breathwork on stress and mental health: A meta-analysis of randomised-controlled trials. *Scientific Reports*, 13 (article number not recorded; Crossref gives no page). DOI [10.1038/s41598-022-27247-y](https://doi.org/10.1038/s41598-022-27247-y). ABS.
> "g = - 0.35 [95% CI - 0.55, - 0.14]"
> "Most studies were deemed as being at moderate risk of bias."
> "we urge caution and advocate for nuanced research approaches with low risk-of-bias study designs to avoid a miscalibration between hype and evidence."

Balban, M. Y., et al. (2023). Brief structured respiration practices enhance mood and reduce physiological arousal. *Cell Reports Medicine*, 4, 100895. DOI [10.1016/j.xcrm.2022.100895](https://doi.org/10.1016/j.xcrm.2022.100895). ABS. One remote RCT (NCT05304000), with outcomes on mood and arousal, not decisions.
> "breathwork, especially the exhale-focused cyclic sighing, produces greater improvement in mood (p < 0.05) and reduction in respiratory rate (p < 0.05) compared with mindfulness meditation."

**Stress and decision quality.** Starcke, K., & Brand, M. (2016). Effects of stress on decisions under uncertainty: A meta-analysis. *Psychological Bulletin*, 142, 909–933. DOI [10.1037/bul0000060](https://doi.org/10.1037/bul0000060). ABS. An erratum exists (10.1037/bul0000068).
> "stress conditions lead to decisions that can be described as more disadvantageous, more reward seeking, and more risk taking than nonstress conditions (d = .17). In those situations in which increased reward seeking and risk taking is disadvantageous, stress had significant effects (d = .26), whereas in other situations, no effects were observed (d = .01)."

**Reading.** The chain has three links:
- **(a)** Acute lab stress slightly worsens some decisions (d ≈ 0.17).
- **(b)** HRVB and breathwork reduce self-reported stress and anxiety (small to moderate, moderate risk of bias).
- **(c)** Mindfulness raises *self-reported* interoception.

Each link is modestly supported. **No study found today shows that a somatic practice improves decision quality or model-revision in knowledge workers.** The trader study is n = 18, correlational, and uses a contested measure.

---

## 6. Intellectual humility (IH)

**Leary, M. R., et al. (2017).** Cognitive and interpersonal features of intellectual humility. *PSPB*, 43, 793–813. DOI [10.1177/0146167217697695](https://doi.org/10.1177/0146167217697695). ABS.
> "Four studies examined intellectual humility-the degree to which people recognize that their beliefs might be wrong."
> "people high in intellectual humility were more attuned to the strength of persuasive arguments than those who were low."

**Porter, T., & Schumann, K. (2018).** Intellectual humility and openness to the opposing view. *Self and Identity*, 17, 139–162 (online 2017-08-09). DOI [10.1080/15298868.2017.1361861](https://doi.org/10.1080/15298868.2017.1361861). FT-AM (author manuscript, Pitt CORE lab).
> "In Study 4, making salient a growth mindset of intelligence boosted intellectual humility, and, in turn, openness to opposing views."

**Zmigrod, L., Zmigrod, S., Rentfrow, P. J., & Robbins, T. W. (2019).** The psychological roots of intellectual humility: The role of intelligence and cognitive flexibility. *Personality and Individual Differences*, 141, 200–208. DOI [10.1016/j.paid.2019.01.016](https://doi.org/10.1016/j.paid.2019.01.016). FT (Cambridge repository copy of the VoR).
> "The results indicate that cognitive flexibility, measured with objective behavioural assessments, predicted intellectual humility."
> "either cognitive flexibility or intelligence are sufficient for high intellectual humility, but neither is necessary."

The paper reports that "108 participants completed the study in full". The design is correlational.

**Porter, T., Elnakouri, A., Meyers, E. A., Shibayama, T., Jayawickreme, E., & Grossmann, I. (2022).** Predictors and consequences of intellectual humility. *Nature Reviews Psychology*, 1, 524–536. DOI [10.1038/s44159-022-00081-9](https://doi.org/10.1038/s44159-022-00081-9). ABS.
> "identify the common element: a meta-cognitive ability to recognize the limitations of one's beliefs and knowledge."
> "We conclude by outlining initial attempts to boost intellectual humility"

**Fischer, H., Kause, A., & Huff, M. (2025).** Intellectual humility links to metacognitive ability. *Personality and Individual Differences*, 238, 113028. DOI [10.1016/j.paid.2024.113028](https://doi.org/10.1016/j.paid.2024.113028). ABS read from the PsyArXiv version (10.31234/osf.io/w8d3y), N = 999, survey.
> "more intellectually humble citizens exhibited a heightened capacity to adjust their confidence levels to the varying accuracy of their evidence interpretations–indicating higher metacognitive ability"
> "more intellectually humble citizens did not exhibit lower metacognitive bias"

**Mindfulness → IH link.** Crossref, WebSearch and PubMed searches today found **no RCT or meta-analysis testing whether meditation or mindfulness training increases intellectual humility**. The one causal manipulation found in this set is a growth-mindset prime (Porter & Schumann Study 4). Educational programmes also appear in the literature, but only as a search summary, not fetched.

**Reading.** IH is a valid, measurable construct. It is associated with openness, attention to argument strength, and metacognitive calibration. The link from contemplative practice to IH is a **hypothesis, not a finding**. It rests on conceptual overlap: decentering, meta-awareness and "recognising beliefs might be wrong".

---

## 7. Psychological safety

**Edmondson, A. (1999).** Psychological safety and learning behavior in work teams. *Administrative Science Quarterly*, 44(2), 350–383. DOI [10.2307/2666999](https://doi.org/10.2307/2666999). ABS.
> "a shared belief held by members of a team that the team is safe for interpersonal risk taking"
> "Results of a study of 51 work teams in a manufacturing company ... show that team psychological safety is associated with learning behavior, but team efficacy is not, when controlling for team psychological safety. As predicted, learning behavior mediates between team psychological safety and team performance."

**Frazier, M. L., Fainshmidt, S., Klinger, R. L., Pezeshkan, A., & Vracheva, V. (2017).** Psychological safety: A meta-analytic review and extension. *Personnel Psychology*, 70, 113–165 (online 2016-10-14). DOI [10.1111/peps.12183](https://doi.org/10.1111/peps.12183). ABS. The abstract gives scope, not effect sizes; the full text was not accessible today.
> "we aggregate theoretical and empirical works, and draw on 136 independent samples representing over 22,000 individuals and nearly 5,000 groups"

**Edmondson, A. C., & Bransby, D. P. (2023).** Psychological safety comes of age: Observed themes in an established literature. *Annual Review of Organizational Psychology and Organizational Behavior*, 10, 55–78. DOI [10.1146/annurev-orgpsych-120920-055217](https://doi.org/10.1146/annurev-orgpsych-120920-055217). ABS.
> "psychological safety—a state of reduced interpersonal risk"

**Reading.** Psychological safety is a *team-level shared belief* shaped by leadership and structure. It is robustly *associated* with learning behaviour and speaking up. The evidence is predominantly field-correlational, including the original 51-team study. It supports the note's claim that admitting error without cost enables learning. **No study was found showing that individual meditation practice raises team psychological safety.** The two should be argued separately: one concerns the organisation's incentives, the other an individual's practice.

---

## 8. Contemplative practice in organisations and labs (with evaluation evidence)

- **Search Inside Yourself (Google-originated).** Caporale-Berkowitz, N. A., et al. (2021). *Int J Workplace Health Mgmt*, 14, 593–604. DOI [10.1108/IJWHM-08-2020-0139](https://doi.org/10.1108/IJWHM-08-2020-0139). ABS. The design is uncontrolled pre–post, n = 123.
  > "Significant increases were detected in mindfulness and the "awareness of emotion" components of emotional intelligence four weeks post-course. No significant changes were found in participants' self-reported levels of burnout, active listening skill or the "management of emotion" components"
  > The paper describes itself as "the first academic, peer-reviewed assessment of SIY, a workplace mindfulness training program that has been taught to over 50,000 people worldwide."
- **Aetna.** Wolever, R. Q., et al. (2012). *J Occup Health Psychol*, 17, 246–258. DOI [10.1037/a0027278](https://doi.org/10.1037/a0027278). ABS. A randomized pilot with n = 239 and an assessment-only control.
  > "the mind-body interventions showed significantly greater improvements on perceived stress, sleep quality, and the heart rhythm coherence ratio of heart rate variability."
- **Software engineering.**
  - Bernárdez, B., Durán, A., Parejo, J. A., Juristo, N., & Ruiz-Cortés, A. (2022). Effects of mindfulness on conceptual modeling performance: A series of experiments. *IEEE TSE*, 48(2), 432–452. DOI [10.1109/TSE.2020.2991699](https://doi.org/10.1109/TSE.2020.2991699). ABS (summary text on the Zenodo artifact record 18323913). Three experiments, 130 students, public-speaking placebo control.
    > "the subjects who practiced mindfulness developed slightly better conceptual models (their quality was 8.16 percent higher) and they did it faster (they were 46.67 percent more productive) than the control group"
    > "more experimentation is needed in order to confirm the outcomes in other Software Engineering tasks and populations."
  - Romano, S., et al. (2024). MOOD: Mindfulness fOr sOftware Developers. *ESEM '24*, 598–602. DOI [10.1145/3674805.3695392](https://doi.org/10.1145/3674805.3695392). This is a trial *design* registered-report-style paper (metadata only; abstract not retrieved).
  - Romano, S., et al. (2025). MBSR at Work: Perspectives from an Instructor and Software Developers. arXiv [2506.11588](https://arxiv.org/abs/2506.11588) **v1** (2025-06-13). ABS. Qualitative.
    > "despite initial skepticism, the developers recognized personal improvements due to the MBSR practice, though the integration of MBSR techniques in the working context remained challenging."
- **Research students.** Xu, J.-Q., Tang, Y.-M. J., & Chen, H. Y. K. (2025). *BMC Psychology*, 13. DOI [10.1186/s40359-024-02233-3](https://doi.org/10.1186/s40359-024-02233-3). ABS. A waitlist RCT with n = 88, retrospectively registered.
  > "participants from the intervention group showed increased resilience (b = 0.88, p = .012), wellbeing literacy (b = 2.52, p = .04), trait mindfulness (b = 5.16, p = .006), and decreased emotional disturbances (b=-8.24, p = .015), while there were no changes in subjective wellbeing, sleeping quality, and self-compassion or compassion towards others compared to the waitlist controls."
- **Academic centres** (web pages fetched today; these are programme descriptions, not evidence):
  - UW–Madison Center for Healthy Minds: "Launched in 2014, Humin helps bring our science to life through tools like the free Healthy Minds Program app, which is now used by over a million people worldwide".
  - Mind & Life Institute: "Bridging science and contemplative wisdom to foster insight and inspire action toward flourishing."
  - Oxford Mindfulness: "We deliver research-based mindfulness for greater personal and collective well-being."
- **Not found:** any published programme or evaluation of contemplative practice inside an AI research lab, or any study linking such practice to research quality, forecasting calibration or error-reporting in a lab.

---

## 9. Active inference and predictive-processing readings of meditation (theory, not evidence)

**Laukkonen, R. E., & Slagter, H. A. (2021).** From many to (n)one: Meditation and the plasticity of the predictive mind. *Neuroscience & Biobehavioral Reviews*, 128, 199–217. DOI [10.1016/j.neubiorev.2021.06.021](https://doi.org/10.1016/j.neubiorev.2021.06.021). ABS.
> "deconstructive meditation brings one closer to the here and now by disengaging anticipatory processes. We propose that practicing meditation therefore gradually reduces counterfactual temporally deep cognition"
> "each technique relinquishes increasingly engrained habits of prediction, including the predicted self."

**Deane, G., Miller, M., & Wilkinson, S. (2020).** Losing ourselves: Active inference, depersonalization, and meditation. *Frontiers in Psychology*, 11, 539726. DOI [10.3389/fpsyg.2020.539726](https://doi.org/10.3389/fpsyg.2020.539726). ABS.
> "we propose an account of the experiences of selfhood as emerging from a temporally deep generative model."
> "we explore how depersonalization may result from an inferred loss of allostatic control"
> The paper aims to "elucidate both the therapeutic potential, and possible dangers, of meditation."

**Lutz, A., Mattout, J., & Pagnoni, G. (2019).** The epistemic and pragmatic value of non-action: a predictive coding perspective on meditation. *Current Opinion in Psychology*, 28, 166–171. DOI [10.1016/j.copsyc.2018.12.019](https://doi.org/10.1016/j.copsyc.2018.12.019). ABS.
> "we discuss a possible relationship between phenomenological notions such as opacity and de-reification, and the deployment of precision-weighting via the voluntary allocation of attention."

**Sandved-Smith, L., Hesp, C., Mattout, J., Friston, K., Lutz, A., & Ramstead, M. J. D. (2021).** Towards a computational phenomenology of mental action. *Neuroscience of Consciousness*, niab018. DOI [10.1093/nc/niab018](https://doi.org/10.1093/nc/niab018). ABS.
> "we cast mental action as policy selection over higher-level cognitive states and add a further hierarchical level to model meta-awareness states that modulate the expected confidence (precision) in the mapping between observations and hidden cognitive states."

**Laukkonen, R., Friston, K., & Chandaria, S. (2025).** A beautiful loop: An active inference theory of consciousness. *Neuroscience & Biobehavioral Reviews*, 176, 106296 (Sept 2025). DOI [10.1016/j.neubiorev.2025.106296](https://doi.org/10.1016/j.neubiorev.2025.106296). **It exists.** Preprint: PsyArXiv 10.31234/osf.io/daf5n, v1 2024-09-08 (Laukkonen and Chandaria only), v2 2025-03-11, v3 2025-06-16.

Published abstract (ABS, Crossref):
> "we propose a hyper-model for precision-control, whose latent states (or parameters) encode and control the overall structure and weighting rules for all layers of inference."
> "This Beautiful Loop Theory is also deeply revealing about altered states, meditation, and the full spectrum of conscious experience."

From the PsyArXiv v3 full text (FT; wording in the published version may differ):
> "By "contentless" we mean that first-order state estimates throughout the abstraction hierarchy are assigned very low precision—i.e. the system withholds confidence in what is out there—while the hyper-precision that says "whatever is there, take its possibilities seriously" is extremely high."
> "high levels of epistemic depth increase the probability, especially for advanced meditators, that phenomena will be perceived as mental constructions and therefore the commonsense phenomenology of naïve realism dissolves."
> "we also acknowledge that meditation states and psychedelic states (discussed later) are nebulous, and measuring and mapping them rigorously is notoriously difficult."

**Reading.** These papers describe meditation as retuning **precision**, meaning the confidence assigned to predictions and prediction errors, including predictions about the self. The "map not territory" language has a close formal cousin here: phenomena "perceived as mental constructions", "de-reification", "withholds confidence". But these are **theoretical proposals**. None of them reports a test showing that practice changes how people hold external models or forecasts. Deane et al. explicitly flag dangers (depersonalization).

---

## 10. FEP, self-evidencing and self-preservation (AI safety relevance)

**Friston, K. (2013).** Life as we know it. *J R Soc Interface*, 10, 20130475. DOI [10.1098/rsif.2013.0475](https://doi.org/10.1098/rsif.2013.0475); PMC3730701 (OA). ABS.
> "the internal states (and their blanket) will appear to engage in active Bayesian inference. In other words, they will appear to model-and act on-their world to preserve their functional and structural integrity, leading to homoeostasis and a simple form of autopoiesis."

**Hohwy, J. (2016).** The self-evidencing brain. *Noûs*, 50, 259–285 (online 2014-03-24). DOI [10.1111/nous.12062](https://doi.org/10.1111/nous.12062). ABS.
> "PEM implies that the brain is essentially self‐evidencing. This means it is imperative to identify an evidentiary boundary between the brain and its environment."

**Friston, K. J., Ramstead, M. J. D., et al. (2024).** Designing ecosystems of intelligence from first principles. arXiv [2212.01354](https://arxiv.org/abs/2212.01354): **v1 2022-12-02, v2 2024-01-11 (current)**. Journal reference: *Collective Intelligence*, 3(1), 2024, DOI [10.1177/26339137231222481](https://doi.org/10.1177/26339137231222481). FT (arXiv v2).
> "we understand intelligence as the capacity to accumulate evidence for a generative model of one's sensed world -- also known as self-evidencing."
> "Crucially, active inference foregrounds an existential imperative of intelligent systems; namely, curiosity or the resolution of uncertainty."
> "The persistence of such stable boundaries in a changing world (i.e., away from thermodynamic equilibrium) is possible only to the extent that the boundary conditions can be predicted and controlled"

**Ororbia, A., & Friston, K. (2023/2024).** Mortal computation: A foundation for biomimetic intelligence. arXiv [2311.09589](https://arxiv.org/abs/2311.09589): **v1 2023-11-16, v2 2024-02-03 (current)**. FT.
> "an artificial form of sentience: one that is capable of self-healing and self-repairing with autonomy — its existential imperative being to persist in (generalized) synchrony with its world."

**Wen, B. (2025).** A framework for inherently safer AGI through language-mediated active inference. arXiv [2508.05766](https://arxiv.org/abs/2508.05766) **v1 (2025-08-07), the only version**. FT. It is a single-author preprint with no journal reference, and it proposes experiments rather than reporting results. The paper's title is not "active inference and corrigibility", but it addresses corrigibility.
> "The drive to minimize surprise inherent in Active Inference promotes corrigibility and responsiveness to corrective feedback."
> "Self-Preservation and Social Instrumentality: Agents may maintain stability through strategic uncertainty calibration and conservative updates"
> "Future research should specifically monitor for ... the survival strategies developed by obsolete agents facing phase-out"

**Critiques of the FEP's generality and status:**
- Aguilera, M., Millidge, B., Tschantz, A., & Buckley, C. L. (2022). How particular is the physics of the free energy principle? *Physics of Life Reviews*, 40, 24–50. DOI [10.1016/j.plrev.2021.11.001](https://doi.org/10.1016/j.plrev.2021.11.001). ABS.
  > "two requirements of the FEP - the Markov blanket condition ... and stringent restrictions on its solenoidal flows ... - are only valid for a very narrow space of parameters."
- Bruineberg, J., Dołęga, K., Dewhurst, J., & Baltieri, M. (2022). The emperor's new Markov blankets. *Behavioral and Brain Sciences*, 45 (online 2021-10-22). DOI [10.1017/S0140525X21002351](https://doi.org/10.1017/S0140525X21002351). ABS.
  > "we propose to distinguish between "Pearl blankets" to refer to the original epistemic use of Markov blankets and "Friston blankets" to refer to the new metaphysical construct."
- Colombo, M., & Wright, C. (2021). First principles in the life sciences: the free-energy principle, organicism, and mechanism. *Synthese*, 198, 3463–3488. DOI [10.1007/s11229-018-01932-w](https://doi.org/10.1007/s11229-018-01932-w). ABS.
  > The abstract notes the FEP "has been called a postulate, an unfalsifiable principle, a natural law, and an imperative. ... its epistemic status is unclear."

**Reading.**
- FEP papers do say that self-organising systems "appear to ... act on their world to preserve their functional and structural integrity" (Friston 2013). Later papers speak of an "existential imperative": curiosity (2022/2024), and "to persist" for mortal computers (2023/2024).
- This is largely **descriptive or definitional**: any system that persists can be read *as if* self-evidencing. It is not a demonstrated engineered drive.
- Whether engineered active-inference agents have a built-in self-preservation drive is **unsettled and mostly un-tested**. The one AI-safety preprint found (Wen 2025, v1, unreviewed) argues the drive *promotes* corrigibility, yet it also lists "Self-Preservation" among expected instrumental-convergence behaviours.
- Today's search found no peer-reviewed empirical result either way. Technical critiques (Aguilera 2022) question how generally the FEP's formal conditions hold at all.
- The note should present "FEP agents want to survive" as an interpretation, not a result.

---

## 11. Daoist "empty centre" and Zen "beginner's mind"

**Laozi, *Dao De Jing*, ch. 11.** Tr. James Legge, *The Tao Teh King*, Sacred Books of the East vol. 39 (Oxford, 1891); public domain.
- Fetched from the Chinese Text Project (ctext.org/dao-de-jing; the page states "Source: "The Tao Te Ching", James Legge, 1891"; base text 《正統道藏》本王弼註道德真經).
- Cross-checked against Project Gutenberg eBook #216 ("Translator: James Legge"; release 1995-02-01, updated 2015-05-11).
- Chinese: 「三十輻，共一轂，當其無，有車之用。…故有之以為利，無之以為用。」
> "The thirty spokes unite in the one nave; but it is on the empty space (for the axle), that the use of the wheel depends. Clay is fashioned into vessels; but it is on their empty hollowness, that their use depends. ... Therefore, what has a (positive) existence serves for profitable adaptation, and what has not that for (actual) usefulness."

Caveats:
- Legge's parenthesis "(for the axle)" is his gloss.
- 無 (wu, "absence/non-being") is rendered very differently across translations. "Empty centre" is an interpretive paraphrase, not Legge's wording.
- If a modern scholarly translation (e.g., D. C. Lau, Penguin 1963) is preferred, it was **not** fetched today.

**Suzuki, S. (1970).** *Zen Mind, Beginner's Mind.* Weatherhill (original). Current editions from Shambhala Publications, whose pages were fetched today:
- 50th Anniversary Edition, 2020-06-02, ISBN 9781611808414, 176 pp.
- Shambhala Library, 2006-10-10, ISBN 9781590302675, 208 pp.

The quote below is as reproduced on the publisher's page, which describes it as the book's "famous opening line". The book text itself was not fetched, so no page number is given.
> "In the beginner's mind there are many possibilities, but in the expert's there are few."

These are literary and religious sources. They can illustrate the note's idea; they are not evidence for it.

---

## Summary table

| Claim the note might make | Evidence strength | Key sources | Caveats |
|---|---|---|---|
| Contemplative training can teach people to experience thoughts as mental events rather than as self or truth (decentering) | **Moderate** (for the construct and its link to depression outcomes) | Teasdale 2002; Fresco 2007; Bernstein 2015; Kuyken 2016 IPD (HR 0.69); Gu 2015 | Clinical/depression samples; self-report EQ; mediation evidence methodologically weak; no evidence it transfers to how scientists hold models or forecasts |
| Brief meditation reduces the sunk-cost bias ("no stake in having been right") | **Contested / weak** | Hafenbrack 2014 (N = 57, 109; one-tailed); Williams & Polito 2022 (two nulls); Schmitzer-Torbert 2020 (trait link inconsistent); Thiedmann 2025 (related bias null) | Small original samples, vignette outcomes; failed conceptual replications; no large preregistered direct replication found |
| Mindfulness improves cognition, decisions or work performance | **Weak** (small effects vs passive controls; not vs active controls) | Whitfield 2022 (g = 0.15); Vainre 2025 (g = 0.25 vs passive, ns vs active, GRADE very low); Goldberg 2022; Lomas 2019; Bartlett 2019 | Heterogeneity high (I² ≈ 81%); active-control comparisons underpowered; Fleming 2024 cross-sectional null; MYRIAD null |
| Mindfulness improves creativity | **Weak–moderate**, task-dependent | Lebuda 2016 (r = .22, correlational; snippet only); Hughes 2023 (d = 0.42 controlled) | Inconsistent; convergent more than divergent; moderated by length and control type |
| Meditation reliably reduces distress in volunteers | **Moderate** | Galante 2023 IPD (SMD −0.32); Goldberg 2022 | Volunteers; passive controls; individual variability; universal rollouts null |
| Meditation is low-risk | **Contested** | Britton 2021 (37% negative functional impact, 6–14% lasting); Farias 2020 (8.3%); Lindahl 2017 | Harms under-measured; "sense of self" disturbances are a named domain; a self-loosening programme needs screening and support |
| "Equanimity" is a trainable, measurable outcome | **Weak** (construct defined, measurement immature) | Desbordes 2015; Hadash 2016; Shoham 2018; Juneau 2020; Weber 2021; Lindsay 2018 | Means non-reactivity to hedonic tone, not detachment from being right; acceptance facet did not change in Hadash 2016; review reports poor reliability |
| Somatic practices (HRVB, breathwork) reduce stress and anxiety | **Moderate** (self-report, small to moderate) | Lehrer 2020 (correction exists); Goessl 2017 (g = 0.83, 24 small studies); Fincham 2023 (g = −0.35) | Moderate risk of bias; larger vs inactive controls; outcomes mostly self-report |
| Lower stress / better interoception → better decisions | **Weak** (indirect chain) | Starcke & Brand 2016 (d = .17); Kandasamy 2016 (n = 18); Garfinkel 2015; Zamariola 2018; Treves 2025 | No direct test in knowledge workers; heartbeat-counting measure problematic; mindfulness raises *self-reported* interoception only |
| Intellectual humility supports better belief revision | **Moderate** (correlational; one causal prime) | Leary 2017; Porter & Schumann 2018; Zmigrod 2019 (n = 108); Fischer 2025 (N = 999); Porter 2022 review | Mostly cross-sectional; self-report IH scales |
| Meditation increases intellectual humility | **No direct evidence found** | — | Conceptual overlap only (decentering, meta-awareness); state as hypothesis |
| Psychological safety enables admitting error and team learning | **Strong** as an association; causal evidence limited | Edmondson 1999 (51 teams); Frazier 2017 (136 samples); Edmondson & Bransby 2023 | Team-level, leader- and structure-driven; mostly correlational; no evidence meditation produces it |
| Organisations and labs have used contemplative programmes with demonstrated effect | **Weak** | SIY 2021 (uncontrolled, n = 123); Aetna 2012 (pilot RCT, stress); Xu 2025 (n = 88 postgrads); Bernárdez 2022 (130 SE students); MOOD 2024 (design) | No evaluation in an AI lab found; outcomes are well-being, not epistemic behaviour |
| Active inference frames meditation as precision/self-model retuning ("phenomena as mental constructions") | **Theoretical proposal** (not empirical) | Laukkonen & Slagter 2021; Deane 2020; Lutz 2019; Sandved-Smith 2021; Laukkonen, Friston & Chandaria 2025 | Untested predictions; Deane flags depersonalization risk |
| FEP / active-inference agents have a built-in self-preservation drive | **Contested / unsettled** | Friston 2013 ("appear to ... preserve"); Friston et al. 2024 (existential imperative = curiosity); Ororbia & Friston 2024 ("to persist"); Wen 2025 (claims promotes corrigibility; also lists self-preservation); Aguilera 2022; Bruineberg 2022; Colombo & Wright 2021 | Largely as-if/definitional; no empirical AI result found; FEP generality itself disputed |
| Daodejing ch. 11 / Suzuki "beginner's mind" | **Illustrative only** | Legge 1891 via ctext/Gutenberg; Shambhala editions 2006/2020 | Translation-dependent; "empty centre" is a paraphrase; the Suzuki quote comes from the publisher page, not a paginated edition |
