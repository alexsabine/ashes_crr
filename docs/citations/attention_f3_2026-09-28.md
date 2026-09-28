# Attention sweep, family F3 (human effects over time and global figures), 2026-09-28

- **Date.** 2026-09-28.
- **Purpose.** `Attention_Algorithms/DECLARATION.md` (prompt-log entry 231), family F3: the evidence for position U6 (the
  long-term effects of engagement-optimised feeds on users) and the published inputs for the global arithmetic of §5
  (users, minutes per day, a 2030 forecast, the share of sessions started by a notification).
- **Who fetched.** A literature agent, on the day. This is a note, not evidence (R8). It judges no novelty and does not
  grade U6; the grade is computed by the declared script from the per-claim readings in
  `Attention_Algorithms/checks/claims_f3.py`.
- **Raw texts.** Saved in the session scratchpad at `attn/f3/<short_name>.txt` (not committed: third-party texts). HTML was
  stripped with Python's `html.parser`; PDFs were extracted with pypdf 6.19.0 (`uv run --no-project --with pypdf`).
  As a result some PDF words carry the ligature U+FB01 ("ﬁ") or a stray space ("noti ﬁcations", "well -being"); quotes
  keep them exactly as extracted.
- **Quote check.** Every quote is a verbatim substring of its raw file after html-unescape, removal of U+FFFE/U+00AD,
  removal of "-\n" joins and whitespace collapsing (the normalisation of
  `AI_Safety/CORRIGIBILITY_2026/checks/verify_claims.py`). **Result: 67 of 67 quotes found, 34 claims, 25 sources.**
- **Readings.** established (causal RCT or quasi-experimental evidence of an effect, sign stated); mixed (credible
  studies disagree on sign or size, or a null or tiny effect); weak (correlational or uncontrolled only); figure (a
  number used for arithmetic). Claims per reading: established 12, mixed 7, weak 5, figure 10.

## Search log

**Web search (one per declared query, 2026-09-28; hits = result links returned).**

| # | query | hits | kept |
|---|---|---|---|
| 1 | social media deactivation experiment welfare | 10 | Allcott et al. 2020 (AER); Allcott et al. emotional state (NBER w33697 / Stanford PDF) |
| 2 | digital addiction self-control social media | 9 | Allcott, Gentzkow & Song 2022 (AER); Hamilton Project brief |
| 3 | social media mental health causal | 9 | Maerevoet et al. 2025 (Frontiers, null RCT) |
| 4 | problematic social media use adolescents prevalence | 9 | WHO Europe HBSC release (25 Sep 2024) |
| 5 | smartphone notifications sleep attention | 9 | none directly (press and how-to pages; led to targeted searches) |
| 6a | social media users worldwide 2026 | 10 | none directly (aggregators; led to DataReportal) |
| 6b | time spent social media per day | 9 | none directly (aggregators, Gallup teen poll not fetched) |
| 7 | social media users 2030 forecast | 9 | BusinessStats (secondary); Statista page (fetched, numbers masked); DataReportal |
| 8 | share of sessions triggered by notifications | 9 | none (vendor help pages; no published share of sessions) |

**Targeted searches for the priority sources and gaps (one web search each).**

| query (short) | hits | kept |
|---|---|---|
| Heitmayer Lahlou smartphone interactions self-initiated | 10 | LSE news release (screened, not counted) |
| "Why are smartphones disruptive" eprints | 10 | Heitmayer & Lahlou 2021 accepted version |
| DataReportal Digital 2026 global overview | 9 | Digital 2026 report; social-media-users page |
| Braghieri Levy Makarin AER 2022 | 10 | AER PDF on author site |
| Odgers 2024 Nature review | 9 | Nature review d41586-024-00902-2 (the first URL, d41586-024-01488-5, was a correspondence and was replaced) |
| Kushlev Proulx Dunn 2016 | 10 | ScienceDaily release (secondary; ACM and ResearchGate 403, kushlev.com 404) |
| emotional-state paper, where published | 10 | AEA page: AEJ: Economic Policy (forthcoming); arXiv 2606.00900 (Felton) |
| Orben Przybylski 2019 NHB | 9 | nature.com article page (ORA accepted manuscript also fetched, dropped: line numbers interleaved) |
| Fitz Kushlev 2019 batching | 9 | journal PDF on kushlev.com |
| JAMA 2025 addictive screen use ABCD | 9 | Xiao et al. 2025 via PubMed (PMC returned a reCAPTCHA page) |
| Ferguson 2024 social media experiments meta | 9 | Ferguson proof PDF; Thrul et al. 2025 reanalysis (PubMed) |
| JAMA Netw Open 2025 social media detox | 10 | Calvert et al. 2025 (PubMed) |
| RCT smartphone restriction bedtime sleep | 9 | He et al. 2020 (PubMed) |
| push notification direct open rate benchmark | 9 | none (vendor benchmarks, secondary; not a share of sessions) |
| "The effects of social media restriction: Meta-analytic evidence" | 9 | Burnell et al. 2025 (RTI page; ScienceDirect returned an empty page); Lopes et al. 2026 medRxiv (web page blocked, read via api.medrxiv.org) |
| SCREENS cluster RCT Denmark sleep | 9 | Pedersen et al. 2022 JAMA Pediatrics (PubMed) |
| Pielot in-situ notifications | 10 | Pielot, Vradi & Park 2018 "Dismissed!"; Pielot et al. 2014 fetched, dropped for the cap |

**arXiv search** (`arxiv.org/search/?query=<q>&searchtype=all&order=-announced_date_first&size=50`, HTTP 200 on all nine
declared queries). Hits: q1 0, q2 0, q3 9, q4 0, q5 0, q6 1, q7 0, q8 0, q9 0. The nine q3 hits are NLP corpora for
mental-health posts, except 2505.09254 (Bak-Coleman et al., "Moving towards informative and actionable social media
research", v3 23 Apr 2026), fetched and dropped for the cap (a methods critique that overlaps Felton). The q6 hit is a
COVID-19 data paper (not relevant).

**Totals.** 243 web-search result links and 10 arXiv hits screened (253). 25 sources included, at the cap.

**Failures on the day.** dl.acm.org and researchgate.net: 403. pmc.ncbi.nlm.nih.gov: reCAPTCHA page (PubMed abstracts
read through NCBI E-utilities instead). medrxiv.org web page: blocked (read through api.medrxiv.org). sciencedirect.com:
empty page. statista.com: page fetched but the numbers are masked for non-subscribers. The primary Statista 2030
forecast is therefore not verified.

**Not found in the sweep.** No platform-level published share of social-media sessions started by a push
notification. The only direct figure is a small wearable-camera study (Heitmayer & Lahlou 2021, 11% of sessions, all
apps). Pielot et al. 2018 give a per-notification open rate for social notifications (26.55%), which is not the same
quantity.

**Priority-list note.** The brief's "Allcott et al. 2024 PNAS" is the political-outcomes paper on the same 2020
deactivation experiment. The emotional-state results are in a separate paper, listed by the AEA as forthcoming in
AEJ: Economic Policy (NBER w33697); that paper is the one used here (S5).

## Sources

### S1. Allcott, Braghieri, Eichmeyer & Gentzkow, "The Welfare Effects of Social Media"
- **Venue and version.** AER 110(3):629–76, March 2020 (aeaweb.org page fetched). The text read is the author version
  dated November 8, 2019.
- **URL and status.** https://web.stanford.edu/~gentzkow/research/facebook.pdf, HTTP 200. Raw file `allcott2020_welfare.txt`.
- **Claims.** f3:1 and f3:2, both established. Randomised Facebook deactivation for four weeks, US 2018.

> Our overall index of subjective well-being improved by 0.09 standard deviations.

> However, we also show that the magnitudes of our causal eﬀects are far smaller than those we would have estimated using the correlational approach of much prior literature.

> Deactivating Facebook freed up 60 minutes per day for the average person in our Treatment group.

> Several weeks later, the Treatment group’s reported usage of the Facebook mobile app was about 11 minutes (22 percent) lower than in Control.

### S2. Allcott, Gentzkow & Song, "Digital Addiction"
- **Venue and version.** AER 112(7):2424–63, July 2022 (aeaweb.org). The text read is NBER WP 28936 (June 2021,
  revised March 2022).
- **URL and status.** https://www.nber.org/system/files/working_papers/w28936/w28936.pdf, HTTP 200. Raw file `allcott2022_addiction.txt`.
- **Claims.** f3:3 and f3:4, both established. An RCT with a bonus for reduced use and a self-set limit tool.

> Temporary incentives to reduce social media use have persistent effects, suggesting social media are habit forming.

> Allowing people to set limits on their future screen time substantially reduces use, suggesting self-control problems.

> The limit treatment reduced FITSBY screen time by 22 minutes per day (16 percent) over 12 weeks.

> Looking at these facts through the lens of our model suggests that self-control problems cause 31 percent of social media use.

> statistically insigniﬁcant changes in measures of happiness, life satisfaction, anxiety, and depression.

### S3. Hamilton Project (Brookings) brief by Allcott, Gentzkow & Song, "Digital addiction: Evidence and policy implications"
- **Version.** Web page, no date in the fetched text.
- **URL and status.** https://www.hamiltonproject.org/publication/paper/digital-addiction-evidence-and-policy-implications/, HTTP 200. Raw file `hamilton_addiction.txt`.
- **Claim.** f3:5, established. It is the same RCT as S2.

> They estimate that self-control problems, exacerbated by habit formation, account for an average of 31 percent (48 minutes per day) of social media use for participants in the experiment.

> they contribute less than 10 minutes of excess use per day for 22 percent of participants and more than 60 minutes for another 32 percent.

### S4. Braghieri, Levy & Makarin, "Social Media and Mental Health"
- **Venue and version.** AER 112(11):3660–93, November 2022, read as the published PDF on the author's site.
- **URL and status.** https://alexeymakarin.github.io/assets/Braghieri_Levy_Makarin_AER_2022.pdf, HTTP 200. Raw file `braghieri2022.txt`.
- **Claim.** f3:6, established. A difference-in-differences design on the staggered roll-out of Facebook across US
  colleges.

> We find that the rollout of Facebook at a college had a negative impact on student mental health.

> increased by 0.085 standard deviation units as a result of the introduction of Facebook.

> this magnitude is around 22 percent of the effect of losing one’s job on mental health

### S5. Allcott, Gentzkow, Wittenbrink et al. (with Meta researchers), "The Effect of Deactivating Facebook and Instagram on Users' Emotional State"
- **Venue and version.** AEJ: Economic Policy (forthcoming, aeaweb.org page fetched); also NBER WP 33697. The text read
  is the undated author PDF.
- **URL and status.** https://web.stanford.edu/~gentzkow/research/emotional_state.pdf, HTTP 200. Raw file `allcott_emotional.txt`.
- **Claim.** f3:7, established, small effect. Two randomised deactivation experiments before the 2020 US election.

> People who deactivated Facebook for the six weeks before the election reported a 0.060 standard deviation improvement in an index of happiness, depression, and anxiety

> People who deactivated Instagram for those six weeks reported a 0.041 standard deviation improvement relative to controls.

> However, the estimated effect sizes are smaller than benchmarks such as the effects of psychological interventions, nationwide mental health trends, and previous experimental estimates in smaller samples.

### S6. Orben & Przybylski, "The association between adolescent well-being and digital technology use"
- **Venue and version.** Nature Human Behaviour 3:173–182, published 14 January 2019.
- **URL and status.** https://www.nature.com/articles/s41562-018-0506-1, HTTP 200. Raw file `orben2019_nature.txt`.
- **Claim.** f3:8, weak. Correlational, and a critique of the harm thesis.

> The association we find between digital technology use and adolescent well-being is negative but small, explaining at most 0.4% of the variation in well-being.

> Taking the broader context of the data into account suggests that these effects are too small to warrant policy change.

### S7. Odgers, "The great rewiring: is social media really behind an epidemic of teenage mental illness?"
- **Venue and version.** Nature 628:29–30, 2024. A review of Haidt's *The Anxious Generation*.
- **URL and status.** https://www.nature.com/articles/d41586-024-00902-2, HTTP 200. Raw file `odgers2024.txt`.
- **Claim.** f3:9, mixed. A critique of the harm thesis.

> Our efforts have produced a mix of no, small and mixed associations. Most data are correlative.

> When associations over time are found, they suggest not that social-media use predicts or causes depression, but that young people who already have mental-health problems use such platforms more often or in different ways from their healthy peers

### S8. WHO Regional Office for Europe, "Teens, screens and mental health"
- **What it is.** A news release on the HBSC 2021/2022 international report, Volume 6, dated 25 September 2024.
- **URL and status.** https://www.who.int/europe/news/item/25-09-2024-teens--screens-and-mental-health, HTTP 200. Raw file `who_hbsc2024.txt`.
- **Claims.** f3:10 (figure, prevalence) and f3:11 (weak, survey associations).

> a sharp rise in problematic social media use among adolescents, with rates increasing from 7% in 2018 to 11% in 2022.

> Girls reported higher levels of problematic social media use than boys (13% vs 9%).

> problematic social media use has been associated with less sleep and later bedtimes

> Adolescents who are heavy but non-problematic users reported stronger peer support and social connections.

### S9. Ferguson, "Do Social Media Experiments Prove a Link With Mental Health: A Methodological and Meta-Analytic Review"
- **Venue and version.** Psychology of Popular Media 14(2):201–206. The text read is the author-hosted page proof
  (ppm0000541).
- **URL and status.** https://www.christopherjferguson.com/Social%20Media%20Experiments%20Meta.pdf, HTTP 200. Raw file `ferguson2024.txt`.
- **Claim.** f3:12, mixed. A critique of the harm thesis.

> Nonetheless, meta-analytic evidence for causal effects was statistically no different than zero.

> the overall estimate for d across studies was 0.088, which was nonsigni ﬁcant and well below the SESOI (r = .10, d = 0.21).

> All studies, regardless of outcome, have fairly straightforward weaknesses related to demand characteristics.

### S10. Thrul, Devkota, AlJuboori, Regan, Alomairah & Vidal, "Social Media Reduction or Abstinence Interventions Are Providing Mental Health Benefits: Reanalysis of a Published Meta-Analysis"
- **Venue and version.** Psychology of Popular Media 14(2):207–209, April 2025. Read as the PubMed record (PMID 40453192).
- **URL and status.** https://pubmed.ncbi.nlm.nih.gov/40453192/, read through E-utilities, HTTP 200. Raw file `reanalysis2025_pubmed.txt`.
- **Claim.** f3:13, mixed. The sign of the effect depends on the length of the intervention.

> Stratified analyses indicated that interventions of <1 week resulted in significantly worse mental health outcomes (d = -0.175), while interventions of 1 week or longer resulted in significant improvements (d = 0.156).

### S11. Burnell, Meter, Andrade, Slocum & George, "The effects of social media restriction: Meta-analytic evidence from randomized controlled trials"
- **Venue and version.** SSM – Mental Health 7:100459, 2025. Read as the abstract on the RTI publication page.
- **URL and status.** https://www.rti.org/publication/the-effects-of-social-media-restriction-meta-analytic-evidence-fr, HTTP 200. Raw file `burnell2025_rti.txt`.
- **Claim.** f3:14, established. The pooled effect is g = 0.17 (95% CI 0.08–0.27), small.

> Thirty-two articles fit our criteria and were included in analyses (5544 individuals; 91 effect sizes).

> Although significant, the pooled estimates were small in magnitude, suggesting only weak support for the effectiveness of restricting social media use.

### S12. Lopes, Branje, David, Gennara, Haidt, Rausch, … Goldfield, "Effect of Social Media Constraints on Mental Health: A Systematic Review and Meta-Analysis of Experiments"
- **Venue and version.** medRxiv 10.64898/2026.06.01.26354614, v2 of 2026-06-09 (v1 2026-06-02). A preprint, **not peer
  reviewed**. Its co-authors include proponents of the harm thesis.
- **URL and status.** https://www.medrxiv.org/content/10.64898/2026.06.01.26354614v2. The web page was blocked, so the
  text was read through api.medrxiv.org (HTTP 200). Raw file `lopes2026_medrxiv.txt`.
- **Claim.** f3:15, established.

> consistent with a beneficial response for depressive symptoms (g = 0.22; 95% CI, 0.12 to 0.32)

> anxiety symptoms (g = 0.19; 95% CI, 0.05 to 0.34)

> Heterogeneity was substantial for several outcomes (I2 > 75%).

### S13. Maerevoet, Van de Casteele, Van de Putte, Debeer, Hoorelbeke, Vansteenkiste & Koster, "Causal effects of social media use on self-esteem, mindfulness, sleep and emotional well-being: a social media restriction study"
- **Venue and version.** Frontiers in Public Health 13, published 30 May 2025.
- **URL and status.** https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2025.1548504/full, HTTP 200. Raw file `frontiers2025_restriction.txt`.
- **Claim.** f3:16, mixed. A null RCT: n = 67, two weeks at no more than 30 minutes a day.

> Results indicate a main effect of time for most outcomes, but the implemented SMU restriction did not moderate these effects.

> In conclusion, this study found no benefits from a temporary social media reduction on mental health outcomes.

### S14. Calvert, Cipriani, … Torous, "Social Media Detox and Youth Mental Health"
- **Venue and version.** JAMA Network Open 8(11):e2545245, 3 November 2025. Read as the PubMed record (PMID 41284297).
- **URL and status.** https://pubmed.ncbi.nlm.nih.gov/41284297/, via E-utilities, HTTP 200. Raw file `detox2025_jamanetopen_pubmed.txt`.
- **Claim.** f3:17, weak. The detox was optional and there was no randomised control.

> 295 (79.1%) opting into a detox intervention that reduced symptoms anxiety by 16.1%

> In this cohort of young adults, reducing social media use for 1 week was associated with reductions in symptoms of depression, anxiety, and insomnia

### S15. Xiao, Meng, Brown, Keyes & Mann, "Addictive Screen Use Trajectories and Suicidal Behaviors, Suicidal Ideation, and Mental Health in US Youths"
- **Venue and version.** JAMA 334(3):219–228, 15 July 2025. Read as the PubMed record (PMID 40531519).
- **URL and status.** https://pubmed.ncbi.nlm.nih.gov/40531519/, via E-utilities, HTTP 200. Raw file `xiao2025_pubmed.txt`.
- **Claim.** f3:18, weak. ABCD cohort, observational.

> increasing addictive use of social media had a risk ratio of 2.14 [95% CI, 1.61-2.85] for suicidal behaviors

> Total screen time at baseline was not associated with outcomes.

### S16. He, Tu, Xiao, Su & Tang, "Effect of restricting bedtime mobile phone use on sleep, arousal, mood, and working memory: A randomized pilot trial"
- **Venue and version.** PLoS One 15(2):e0228756, 10 February 2020. Read as the PubMed record (PMID 32040492).
- **URL and status.** https://pubmed.ncbi.nlm.nih.gov/32040492/, via E-utilities, HTTP 200. Raw file `he2020_bedtime_pubmed.txt`.
- **Claim.** f3:19, established. A pilot RCT with n = 38.

> Restricting mobile phone use before bedtime for four weeks was effective in reducing sleep latency, increasing sleep duration, improving sleep quality, reducing pre-sleep arousal, and improving positive affect and working memory.

### S17. Pedersen, Rasmussen, … Grøntved, "Effects of Limiting Recreational Screen Media Use on Physical Activity and Sleep in Families With Children: A Cluster Randomized Clinical Trial" (SCREENS)
- **Venue and version.** JAMA Pediatrics 176(8):741–749, 1 August 2022. Read as the PubMed record (PMID 35604678).
- **URL and status.** https://pubmed.ncbi.nlm.nih.gov/35604678/, via E-utilities, HTTP 200. Raw file `screens2022_pubmed.txt`.
- **Claim.** f3:20, mixed. Null on EEG-measured sleep; positive on physical activity.

> No significant between-group mean differences were observed between intervention and control for the electroencephalography-based sleep outcomes.

> intention-to-treat between-group mean difference, 45.8 minutes per day

### S18. Kushlev, Proulx & Dunn, "'Silence Your Phones': Smartphone Notifications Increase Inattention and Hyperactivity Symptoms"
- **Venue and version.** CHI 2016, canonical earlier work.
- **URL and status.** **Secondary.** Read through the University of Virginia release on ScienceDaily (2016-05-09),
  https://www.sciencedaily.com/releases/2016/05/160509191843.htm, HTTP 200, because ACM and ResearchGate returned 403.
  Raw file `kushlev2016_sciencedaily.txt`.
- **Claim.** f3:21, established. A within-subject experiment with n = 221.

> The results showed that the participants experienced significantly higher levels of inattention and hyperactivity when alerts were turned on.

> 221 students at the University of British Columbia drawn from the general student population were assigned for one week to maximize phone interruptions

### S19. Fitz, Kushlev, Jagannathan, Lewis, Paliwal & Ariely, "Batching smartphone notifications can improve well-being"
- **Venue and version.** Computers in Human Behavior 101:84–94, 2019, read as the journal PDF on the author's site.
- **URL and status.** https://www.kushlev.com/s/2019-Fitz-Batching.pdf, HTTP 200. Raw file `fitz2019.txt`.
- **Claims.** f3:22 (established: batching helps) and f3:23 (mixed: no notifications at all raised anxiety and FoMO).

> we conducted a randomized ﬁeld experiment (n = 237)

> participants whose noti ﬁcations were batched three-times-a-day felt more attentive, productive, in a better mood, and in greater control of their phones.

> In contrast, participants who did not receive noti ﬁcations at all reaped few of those bene ﬁts, but experienced higher levels of anxiety and “fear of missing out ” (FoMO).

### S20. Heitmayer & Lahlou, "Why are smartphones disruptive? An empirical study of smartphone use in real-life contexts"
- **Venue and version.** Computers in Human Behavior 116:106637, 2021. The text read is the author accepted version.
- **URL and status.** https://researchonline.lse.ac.uk/id/eprint/107820/1/Why_Are_Smartphones_Disruptive_compressed_Final_Submission.pdf, HTTP 200. Raw file `heitmayer2021.txt`.
- **Claims.** f3:24 (figure, the share of sessions started by a notification) and f3:25 (weak, observational).

> Importantly, we find that 89% of smartphone interactions are initiated by users, not by notifications.

> about 11% of the full sessions were initiated by notifications, the rest by users

> Many users seem to find it difficult to only use their phones briefly, and to only do what they originally intended to do with it.

> smartphone use appears to be more purpose -driven when users receive notifications, and more distraction -seeking when it is self -initiated.

### S21. Pielot, Vradi & Park, "Dismissed! A Detailed Exploration of How Mobile Phone Users Handle Push Notifications"
- **Venue and version.** MobileHCI '18, Barcelona, 2018. Canonical earlier work.
- **URL and status.** https://www.interruptions.net/literature/Pielot-MobileHCI18.pdf, HTTP 200. Raw file `pielot2018_dismissed.txt`.
- **Claims.** f3:26 and f3:27, both figures.

> We analyzed 794,525 notiﬁcations from 278 mobile phone users

> Our participants received a median number of 56 notiﬁcations per day

> notiﬁcations from non-messenger apps are consumed at much lower rates (Email: 15.47%, Social, 26.55%, NonSocial: 16.19%).

### S22. DataReportal (Kepios with Meltwater and We Are Social), "Digital 2026: Global Overview Report"
- **Version.** Published October 2025, with data to October 2025.
- **URL and status.** https://datareportal.com/reports/digital-2026-global-overview-report, HTTP 200. Raw file `datareportal2026.txt`.
- **Claims.** f3:28 and f3:32, both figures. The report warns that "user identities" may not be unique individuals.

> Kepios analysis reveals that global social media user identities now stand at 5.66 billion, with that figure equivalent to 68.7 percent of the global population.

> The total user identities figure increased by 4.8 percent in the 12 months to October 2025

> the typical TikTok user spends 1 hour and 37 minutes per day using the platform’s Android app

> users opening the platform’s Android app an average of 10 times per day

### S23. DataReportal, "Global Social Media Statistics"
- **Version.** Live page with figures for the start of April 2026; the analysis is credited to "Manochi".
- **URL and status.** https://datareportal.com/social-media-users, HTTP 200. Raw file `datareportal_smu.txt`.
- **Claims.** f3:29, f3:30 and f3:31, all figures.

> there were 5.79 billion social media “user identities” around the world at the start of April 2026.

> That equates to annualised growth of 5.4 percent

> spends an average of 18 hours and 36 minutes using social media each week, which includes browsing social networks and watching online videos on platforms like YouTube, TikTok, Instagram, and Facebook.

> the world spends over 15 billion hours consuming content on social platforms each day

### S24. BusinessStats, "Number of Worldwide Social Network Users 2017–2030"
- **What it is.** A **secondary** aggregator. It cites the Statista Digital Economy Compass, DataReportal and GWI. The
  Statista page itself (statistics/278414) was fetched but masks its numbers.
- **Version.** Undated page that treats 2025 as the current year.
- **URL and status.** https://businesstats.com/number-of-worldwide-social-network-users/, HTTP 200. Raw file `businesstats_forecast.txt`.
- **Claim.** f3:33, figure.
- **Base caveat.** Its base counts unique users (5.42 billion in 2025), which is lower than DataReportal's identity
  count. The two series must not be mixed.

> 2.73B (2017) → 5.42B (2025) → 6.05B (2030 proj).

> 2026–2030 projections based on Statista Digital Economy Compass demographic modelling

### S25. Felton, "Notes on Randomized Controlled Trials for Studying Social Media Harms"
- **Venue and version.** arXiv:2606.00900 [stat.ME], v1, submitted 30 May 2026.
- **URL and status.** https://arxiv.org/abs/2606.00900, HTTP 200. Raw file `arxiv_2606.00900.txt`.
- **Claim.** f3:34, mixed. A methodological critique that cuts both ways: deactivation RCTs measure a local effect.

> published RCTs typically identify effects of a \textit{local}, or small-scale, intervention: a person is assigned to quit social media, but her immediate peers continue using it in large numbers.

> Such global interventions alter both the proximal social environment and the broader culture, potentially harming teenagers who abstain from social media entirely.

## Global figures

| item | value | unit | year | source | verbatim |
|---|---|---|---|---|---|
| social media user identities | 5.79e9 | identities, monthly active, worldwide | 2026 (April) | DataReportal social-media-users (S23) | yes |
| social media user identities | 5.66e9 | identities, monthly active, worldwide | 2025 (October) | DataReportal Digital 2026 (S22) | yes |
| growth of user identities | 5.4 | percent per year (to April 2026) | 2026 | S23 | yes |
| growth of user identities | 4.8 | percent per year (to October 2025) | 2025 | S22 | yes |
| time on social media per user | 1116 | minutes per week (18 h 36 min; GWI, internet users 16+, includes video platforms) | 2026 | S23 | yes |
| time on social media per user (derived) | 159.4 | minutes per day (1116 / 7) | 2026 | derived from S23 | no (derived) |
| world time on social platforms | 1.5e10 | hours per day | 2026 | S23 | yes ("over 15 billion hours") |
| TikTok time per Android user | 97 | minutes per day (1 h 37 min, Similarweb) | 2025 | S22 | yes |
| social media users, projection | 6.05e9 | unique users, monthly, worldwide | 2030 | BusinessStats citing Statista (S24), **secondary** | yes (secondary; the primary Statista value is not verifiable) |
| share of sessions started by a notification | 0.11 | share of smartphone sessions (all apps; N = 37, UK, ages 21–29) | 2021 | Heitmayer & Lahlou (S20) | yes |
| open rate of social-network notifications | 0.2655 | share of social notifications that open the app | 2018 | Pielot et al. (S21) | yes |
| notifications received per user | 56 | per day (median, 278 Android users) | 2018 | Pielot et al. (S21) | yes |
| problematic social media use, adolescents | 0.11 | share of 11-, 13- and 15-year-olds (HBSC, 44 countries and regions) | 2022 | WHO Europe (S8) | yes |
| excess use from self-control problems | 48 | minutes per day, 31 percent of use (US adults in the RCT) | 2020 | Allcott, Gentzkow & Song brief (S3) | yes |

**Notes for the §5 arithmetic.**
- **Bases.** The 2026 users figure (DataReportal identities) and the 2030 forecast (a unique-user basis, secondary) sit
  on different bases.
- **Deriving 2030 on one base.** Growing 5.79e9 at 5.4% a year is the declaration's fallback. The forecast source
  itself expects growth to slow to about 2% a year by 2028–30.
- **f_notif.** 0.11 is the only published share of sessions found. It comes from one small study, covers all apps, and
  its participants mostly kept their phones on silent.

## What the causal evidence says (for the U6 grade; the script computes the grade)

**Randomised and quasi-experimental studies agree on the sign for adults and college students.** Less social media
means slightly better well-being. The effects are small:
- Facebook deactivation for four weeks: +0.09 SD on subjective well-being (S1).
- The six-week pre-election deactivations: +0.060 SD for Facebook and +0.041 SD for Instagram, the Instagram estimate
  not significant at the preregistered threshold (S5).
- The Facebook college roll-out: +0.085 SD on a poor-mental-health index, about 22% of the effect of job loss (S4).
- Pooled restriction RCTs: g = 0.17 (S11). The medRxiv preprint gives g = 0.22 for depression and 0.19 for anxiety,
  with high heterogeneity (S12).

**Habit and self-control are established.**
- A pause lowers later use: 22% lower several weeks after deactivation (S1).
- A three-week use incentive has persistent effects, and self-set limits cut use by 22 minutes a day (S2).
- Self-control problems account for about 31% of use, or 48 minutes a day, with large heterogeneity (S2, S3).

**The null results and critiques are credible.**
- The pooled experimental effect is d = 0.088 and not significant; the author also names demand characteristics (S9).
- The sign flips with intervention length: under one week d = −0.175, one week or longer d = +0.156 (S10).
- A small null RCT (S13).
- Correlational associations explain at most 0.4% of variance (S6), and longitudinal associations may run in reverse
  (S7).
- Individual RCTs measure a local effect, not the effect of a platform on a population (S25).
- For adolescents, the causal evidence found is quasi-experimental on college students (S4). Evidence on younger
  adolescents is correlational or prevalence data: problematic use rose from 7% in 2018 to 11% in 2022 (S8), and
  addictive-use trajectories carry a risk ratio of 2.14 for suicidal behaviour (S15).

**Sleep evidence is mixed.** A pilot RCT with n = 38 finds that restricting the phone at bedtime improves sleep (S16).
A cluster RCT with EEG-measured sleep finds no difference (S17).

**Notifications.**
- Two experiments find harm to attention from notification alerts. Alerts-on raises inattention and hyperactivity
  (S18, secondary). Batching notifications three times a day improves attention and mood (S19).
- Switching notifications off entirely raised anxiety and FoMO in the same trial (S19).
- About 89% of interactions and 89% of sessions are user-started (S20). Habit, not the push, carries most use.

**The agent's overall reading.** Small beneficial effects of pauses are established for adults. Adolescent harm rests on
weaker designs. Across all of U6 the evidence reads as mixed in size, with the sign mostly favouring less use. This
matches the investigator's expectation of MIXED; the grade itself is left to the script.
