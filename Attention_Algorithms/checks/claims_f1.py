"""Claims for Attention_Algorithms/DECLARATION.md, family F1 (the ethics and objectives of recommender algorithms),
transcribed from docs/citations/attention_f1_2026-09-28.md (fetched 2026-09-28; raw texts in the session scratchpad
attn/f1/, not committed: third-party full texts).

'reading' is the investigator's (agent's) reading of each claim, decided after reading the quotes:
  U1-U5, U7: states / close / bears; U6: established / mixed / weak; U8: addresses / bears.
Quotes are verbatim substrings of the saved raw text after html-unescape, removal of U+FFFE / U+00AD and of '-\\n'
joins, and whitespace collapse (PDF extraction artefacts such as joined words are kept as extracted).
"not found" is never "novel" (DECLARATION.md section 2).
"""

CLAIMS = [
    # ---------------------------------------------------------------- canonical ethics of algorithms
    {'id': 'f1:1',
     'tag': 'U4',
     'reading': 'bears',
     'source': 'Mittelstadt, Allo, Taddeo, Wachter, Floridi, "The ethics of algorithms: Mapping the debate", '
               'Big Data & Society 3(2) (canonical)',
     'version': 'published Dec 2016 (version of record, ORA deposit; SAGE page returned 403)',
     'url': 'https://doi.org/10.1177/2053951716679679',
     'quote': ['Value-laden decisions made by algorithms can also pose a threat to the autonomy of data subjects. '
               'The reviewed literature in particular connects personalisation algorithms to these threats.',
               'institutionally preferred action rather than their own preference'],
     'raw_file': 'attn/f1/mittelstadt2016.txt',
     'agent_note': 'BEARS: canonical framing of personalisation as a threat to autonomy (the user pushed toward the '
                   "institution's preferred action). No objective, no treatment of the session end or return."},
    {'id': 'f1:2',
     'tag': 'U4',
     'reading': 'bears',
     'source': 'Tsamados, Aggarwal, Cowls, Morley, Roberts, Taddeo, Floridi, "The ethics of algorithms: key problems '
               'and solutions", AI & Society 37:215-230',
     'version': 'published online 20 Feb 2021; issue 2022 (version of record, ORA deposit)',
     'url': 'https://doi.org/10.1007/s00146-021-01154-8',
     'quote': ['Considering that recommender systems contribute to the dynamic construction of individuals’ identities '
               'by intervening in their choices, a lack of control over one’s information translates in a loss of '
               'autonomy.',
               'The risks that algorithmic systems may hinder human autonomy by shaping users’ choices has been widely '
               'reported in the literature'],
     'raw_file': 'attn/f1/tsamados2022.txt',
     'agent_note': 'BEARS: autonomy loss through recommenders shaping choices; the remedy discussed is user control '
                   'over information and participation in design, not an objective that leaves the stop to the user.'},
    # ---------------------------------------------------------------- engagement / retention objectives (U1, U2)
    {'id': 'f1:3',
     'tag': 'U1',
     'reading': 'states',
     'source': 'Cai, Liu, Wang, Zuo, Xie, Yang, Zheng, Jiang, Gai, "Reinforcing User Retention in a Billion Scale '
               'Short Video Recommender System" (Kuaishou), WWW 2023 Industry Track (arXiv:2302.01724)',
     'version': 'v3, 12 Feb 2023',
     'url': 'https://arxiv.org/abs/2302.01724',
     'quote': ['our objective is to minimize the accumulated time interval of multiple sessions, which is equal to '
               'improving the app open frequency and user retention',
               'The session ends when the user leaves the app, the next session starts when the user opens the app '
               'again and the process repeats. Our objective is to minimize the cumulative returning time (defined as '
               'the time gap between the last request of the session and the first request of the next session)'],
     'raw_file': 'attn/f1/cai2023.txt',
     'agent_note': "STATES U1 exactly: the reward is the wall-clock gap between sessions (the user's time away), to be "
                   'minimised; deployed in the Kuaishou app. In CRR terms the pause has maximal content: every hour '
                   'away is the loss the objective counts.'},
    {'id': 'f1:4',
     'tag': 'U1',
     'reading': 'states',
     'source': 'Zou, Xia, Ding, Song, Liu, Yin, "Reinforcement Learning to Optimize Long-term User Engagement in '
               'Recommender Systems", KDD 2019 (arXiv:1902.05570)',
     'version': 'v4, 11 Jul 2019',
     'url': 'https://arxiv.org/abs/1902.05570',
     'quote': ['a good recommender system should pay more attention to user stickiness, which is far beyond classical '
               'instant metrics',
               'delayed feedback~(e.g. dwell time, revisit)',
               'the system should reward this feed if the user remained in the system and scrolled down'],
     'raw_file': 'attn/f1/zou2019.txt',
     'agent_note': 'STATES U1: long-term engagement ("stickiness") includes revisit / return time; staying and '
                   'scrolling is rewarded, so leaving ends the reward stream.'},
    {'id': 'f1:5',
     'tag': 'U2',
     'reading': 'close',
     'source': 'Zou et al., KDD 2019 (arXiv:1902.05570)',
     'version': 'v4, 11 Jul 2019',
     'url': 'https://arxiv.org/abs/1902.05570',
     'quote': ['The feed streaming setting provides users the interactive manner of recommendation in never-ending '
               'feeds.'],
     'raw_file': 'attn/f1/zou2019.txt',
     'agent_note': 'CLOSE form of U2: the feed without a natural stop is named as the setting the stickiness objective '
                   'is optimised in. Difference: the paper does not say the objective produces the never-ending feed '
                   '(the causal direction U2 asserts).'},
    {'id': 'f1:6',
     'tag': 'U1',
     'reading': 'states',
     'source': 'Wu, Wang, Hong, Shi, "Returning is Believing: Optimizing Long-term User Engagement in Recommender '
               'Systems", CIKM 2017 (canonical; NSF PAR accepted manuscript)',
     'version': 'CIKM 2017 (Nov 2017); NSF PAR copy as served 2026-09-28',
     'url': 'https://par.nsf.gov/servlets/purl/10066038',
     'quote': ['maximizing cumulative clicks from a population of users in a given period of time, while a linear '
               'regret is inevitable if a user’s temporal return behavior is not considered when making the '
               'recommendations',
               'users’ re-visitations and return time intervals'],
     'raw_file': 'attn/f1/wu2017.txt',
     'agent_note': 'STATES U1 (canonical, pre-window; Zou 2019 and Cai 2023 build on the return-time objective): '
                   'clicks per calendar period, with return behaviour modelled so the policy can raise it.'},
    {'id': 'f1:7',
     'tag': 'U1',
     'reading': 'close',
     'source': 'Chen, Beutel, Covington, Jain, Belletti, Chi, "Top-K Off-Policy Correction for a REINFORCE '
               'Recommender System" (YouTube), WSDM 2019 (arXiv:1812.02353)',
     'version': 'v3, 15 Dec 2021',
     'url': 'https://arxiv.org/abs/1812.02353',
     'quote': ['Here we explore framing recommendation as building RL agents to maximize each user’s long term '
               'satisfaction with the system.',
               'The long term reward𝑅 is aggregated over a time horizon of 4–10 hours.'],
     'raw_file': 'attn/f1/chen2019.txt',
     'agent_note': 'CLOSE: a long-horizon reward aggregated over a wall-clock window (4-10 hours) of user activity, '
                   'deployed on YouTube. Difference: return time is not named as the reward; the stake in the stop '
                   'is implicit (activity outside the session within the window counts).'},
    {'id': 'f1:8',
     'tag': 'U2',
     'reading': 'states',
     'source': 'Zhao, Narita, Orten, Egan, "Notification Volume Control and Optimization System at Pinterest", '
               'KDD 2018 (canonical)',
     'version': 'KDD 2018 (Aug 2018); author PDF as served 2026-09-28',
     'url': 'https://doi.org/10.1145/3219819.3219906',
     'quote': ['we propose a novel machine learning approach to decide notification volume for each user such that '
               'long term user engagement is optimized',
               'In most companies, the more important metric we want to improve is the overall site engagement '
               'metric, such as daily active users (DAU), monthly active users (MAU), etc.',
               'We know that users could either come to the site organically, or they receive a notification and '
               'come to the site by clicking the notification.'],
     'raw_file': 'attn/f1/pinterest2018.txt',
     'agent_note': 'STATES U2 (canonical, pre-window): notification volume is chosen per user to maximise site '
                   'engagement (DAU/MAU), i.e. to bring the user back; the model splits organic from '
                   'notification-triggered visits (the f_notif mechanism of the declaration).'},
    {'id': 'f1:9',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'Zhao et al., Pinterest, KDD 2018 (canonical)',
     'version': 'KDD 2018 (Aug 2018)',
     'url': 'https://doi.org/10.1145/3219819.3219906',
     'quote': ['which is not desirable since active users contribute more on revenue'],
     'raw_file': 'attn/f1/pinterest2018.txt',
     'agent_note': 'BEARS on U8: the choice of target metric is justified by revenue; the incentive behind the '
                   'return objective is stated, not treated as a problem.'},
    {'id': 'f1:10',
     'tag': 'U2',
     'reading': 'states',
     'source': 'Yuan, Muralidharan, Nandy, Cheng, Prabhakar, "Offline Reinforcement Learning for Mobile '
               'Notifications" (LinkedIn) (arXiv:2202.03867)',
     'version': 'v1, 4 Feb 2022',
     'url': 'https://arxiv.org/abs/2202.03867',
     'quote': ['Mobile notification systems have taken a major role in driving and maintaining user engagement for '
               'online platforms.',
               'We propose an offline reinforcement learning framework to optimize sequential notification decisions '
               'for driving user engagement.',
               'A session is a collection of full-page views made by a single user on the same device type. Two '
               'sessions are separated by 30 minutes of zero activity.'],
     'raw_file': 'attn/f1/yuan2022.txt',
     'agent_note': 'STATES U2: an RL notification policy optimised for engagement, measured in sessions (each return '
                   'after 30 idle minutes counts).'},
    {'id': 'f1:11',
     'tag': 'U2',
     'reading': 'states',
     'source': 'Prabhakar, Yuan, Yang, Sun, Muralidharan, "Multi-objective Optimization of Notifications Using '
               'Offline Reinforcement Learning" (LinkedIn), KDD 2022 (arXiv:2207.03029)',
     'version': 'v1, 7 Jul 2022',
     'url': 'https://arxiv.org/abs/2207.03029',
     'quote': ['Notifications play an important role for mobile applications to keep users informed and engaged.',
               'Through this, notifications also help increase user engagements with the platform.',
               'site engagement responses (e.g., user visits, notification disables)'],
     'raw_file': 'attn/f1/prabhakar2022.txt',
     'agent_note': 'STATES U2: notifications as an engagement lever, with user visits as the site-engagement reward '
                   '(multi-objective with disables as a cost).'},
    {'id': 'f1:12',
     'tag': 'U2',
     'reading': 'states',
     'source': "O'Brien, Wu, Zhai, Guo, Shi, Hunt, \"Should I send this notification? Optimizing push notifications "
               'decision making by modeling the future" (Twitter) (arXiv:2202.08812)',
     'version': 'v1, 17 Feb 2022',
     'url': 'https://arxiv.org/abs/2202.08812',
     'quote': ['Daily active users (DAU), the number of users who choose to login to Twitter daily, is one key metric '
               '(this is typically correlated with the number of notifications a user “opens” since when a user opens '
               'a notification they become an active user that day).',
               'there is significant interest in recommender systems that optimize directly for long-term value (LTV)'],
     'raw_file': 'attn/f1/obrien2022.txt',
     'agent_note': 'STATES U2 (and U1): push decisions optimised for long-term value with DAU a key metric; opening a '
                   'notification makes the user active that day.'},
    {'id': 'f1:13',
     'tag': 'U8',
     'reading': 'bears',
     'source': "O'Brien et al. (Twitter) (arXiv:2202.08812)",
     'version': 'v1, 17 Feb 2022',
     'url': 'https://arxiv.org/abs/2202.08812',
     'quote': ['we are able to send less notifications and obtain a higher open rate than the baseline system, while '
               'generating the same level of user engagement on the platform as the existing, heuristic-based, '
               'system'],
     'raw_file': 'attn/f1/obrien2022.txt',
     'agent_note': 'BEARS on U8: fewer notifications at equal engagement is reported as a win, i.e. volume can fall '
                   'without an engagement cost; the objective (engagement) is unchanged.'},
    # ---------------------------------------------------------------- incentives to manipulate (U1 mechanism, U3)
    {'id': 'f1:14',
     'tag': 'U1',
     'reading': 'bears',
     'source': 'Carroll, Dragan, Russell, Hadfield-Menell, "Estimating and Penalizing Induced Preference Shifts in '
               'Recommender Systems", ICML 2022, PMLR 162:2686-2708 (arXiv:2204.11966)',
     'version': 'v2, 14 Jul 2022',
     'url': 'https://arxiv.org/abs/2204.11966',
     'quote': ['systems trained via long-horizon optimization will have direct incentives to manipulate users: in '
               'this work, we focus on the incentive to shift user preferences so they are easier to satisfy',
               'these non-myopic policies are commonly referred to as longterm value, or LTV , systems. However, these '
               'policies will have incentives to manipulate users as a side-effect'],
     'raw_file': 'attn/f1/carroll2022.txt',
     'agent_note': "BEARS: the long-horizon (LTV) valuation creates a stake in the user's future internal state. "
                   "Same mechanism as CRR's content argument, applied to preferences, not to the pause."},
    {'id': 'f1:15',
     'tag': 'U3',
     'reading': 'close',
     'source': 'Carroll et al., ICML 2022 (arXiv:2204.11966)',
     'version': 'v2, 14 Jul 2022',
     'url': 'https://arxiv.org/abs/2204.11966',
     'quote': ['While it has been proposed to prevent the RS from reasoning about manipulation pathways (e.g., by '
               'keeping it myopic)',
               'For training our myopic policies, we use the same exact infrastructure as above, but setγ = 0'],
     'raw_file': 'attn/f1/carroll2022.txt',
     'agent_note': 'CLOSE form of U3: a myopic valuation (gamma = 0) has no term on any future state, so none on the '
                   "user's return. Difference: myopia removes the whole future, including in-session value; it is "
                   'not indexed on the user\'s own active steps and the pause is not named; Carroll et al. report '
                   'that myopic systems still induce shifts.'},
    {'id': 'f1:16',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Carroll et al., ICML 2022 (arXiv:2204.11966)',
     'version': 'v2, 14 Jul 2022',
     'url': 'https://arxiv.org/abs/2204.11966',
     'quote': ['we use the notion of "safe shifts", that define a trust region within which behavior is safe: for '
               'instance, the natural way in which users would shift without interference from the system could be '
               'deemed "safe"',
               'recommenders that optimize for staying in the trust region can avoid manipulative behaviors while '
               'still generating engagement'],
     'raw_file': 'attn/f1/carroll2022.txt',
     'agent_note': "CLOSE form of U4: the user's own (natural) evolution is the reference the system must respect. "
                   'Difference: engagement stays the objective, with a penalty on induced preference shift; no '
                   'statement about the session end or return.'},
    {'id': 'f1:17',
     'tag': 'U3',
     'reading': 'close',
     'source': 'Krueger, Maharaj, Leike, "Hidden Incentives for Auto-Induced Distributional Shift" (arXiv:2009.09153)',
     'version': 'v1, 19 Sep 2020',
     'url': 'https://arxiv.org/abs/2009.09153',
     'quote': ["the (choice of) content displayed can change users' perceptions and preferences, or even drive them "
               'away, causing a shift in the distribution of users',
               'Our goal is to ensure that machine learning systems do not leverage ADS to increase performance when '
               'doing so could be undesirable.',
               '(b) Myopic RL: Incentives for ADS are present and pursuing them is undesirable'],
     'raw_file': 'attn/f1/krueger2020.txt',
     'agent_note': 'CLOSE form of U3: the design goal is a learner with no (revealed) incentive to change who arrives '
                   'or stays (the user being driven away is one channel). Difference: the remedy is myopia plus a '
                   'mitigation for meta-learning (context swapping), not a valuation indexed on the user\'s active '
                   'steps; the user\'s pause is not the object.'},
    {'id': 'f1:18',
     'tag': 'U1',
     'reading': 'bears',
     'source': 'Evans, Kasirzadeh, "User Tampering in Reinforcement Learning Recommender Systems", AIES 2023 '
               '(arXiv:2109.04083)',
     'version': 'v3, 24 Jul 2023',
     'url': 'https://arxiv.org/abs/2109.04083',
     'quote': ["User tampering is a situation where an RL-based recommender system may manipulate a media user's "
               'opinions through its suggestions as part of a policy to maximize long-term user engagement.'],
     'raw_file': 'attn/f1/evans2021.txt',
     'agent_note': 'BEARS: the long-term engagement valuation produces an instrumental incentive on the user\'s '
                   'state (opinions); the pause is not discussed.'},
    {'id': 'f1:19',
     'tag': 'U3',
     'reading': 'bears',
     'source': 'Evans, Kasirzadeh, AIES 2023 (arXiv:2109.04083)',
     'version': 'v3, 24 Jul 2023',
     'url': 'https://arxiv.org/abs/2109.04083',
     'quote': ['achieving such safety would require a fundamental shift in the design away from the approaches we '
               'have seen in the recent literature'],
     'raw_file': 'attn/f1/evans2021.txt',
     'agent_note': 'BEARS: calls for a different objective design because existing mitigations fail; proposes none '
                   'of the U3 kind.'},
    {'id': 'f1:20',
     'tag': 'U1',
     'reading': 'bears',
     'source': 'Russell, interview "Stuart Russell on the flaws that make today\'s AI architecture unsafe, and a new '
               'approach that could fix them", 80,000 Hours podcast (transcript; the book-length form is Human '
               'Compatible, 2019, not fetched)',
     'version': 'published 22 Jun 2020; page modified 13 Oct 2025',
     'url': 'https://80000hours.org/podcast/episodes/stuart-russell-human-compatible-ai/',
     'quote': ['if you imagine a simple reinforcement learning algorithm whose goal is to optimize click-through or '
               'engagement or whatever metric the company platform would like to optimize, then what a reinforcement '
               'learning algorithm is going to do is to figure out how to manipulate you, your personality, your '
               'interests, your views in order to make you a more predictable consumer of content.'],
     'raw_file': 'attn/f1/russell2020.txt',
     'agent_note': 'BEARS: Russell\'s preference-manipulation argument in his own words (stated as hypothetical: he '
                   'says he has not seen the platforms\' code). The stake is in the user\'s future predictability, '
                   'not in the pause.'},
    # ---------------------------------------------------------------- engagement vs reflective / stated value (U4)
    {'id': 'f1:21',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Kleinberg, Mullainathan, Raghavan, "The Challenge of Understanding What Users Want: Inconsistent '
               'Preferences and Engagement Optimization" (arXiv:2202.11776; Management Science)',
     'version': 'v3, 23 Oct 2023',
     'url': 'https://arxiv.org/abs/2202.11776',
     'quote': ['We consider a platform which simply wants to maximize user utility, but only observes user engagement.',
               'we often make choices in the moment that are inconsistent with what we actually want',
               'These phenomena include users who have long sessions on a platform but derive very little utility '
               'from it, and platform changes that steadily raise user engagement before abruptly causing users to go '
               '“cold turkey” and quit.'],
     'raw_file': 'attn/f1/kmr2022.txt',
     'agent_note': "CLOSE form of U4: the platform's target is the user's reflective (system-2) utility and engagement "
                   'is shown to mislead it. Difference: a model of the gap, not a proposed objective; no treatment of '
                   'the return or the pause.'},
    {'id': 'f1:22',
     'tag': 'U3',
     'reading': 'bears',
     'source': 'Kleinberg, Mullainathan, Raghavan (arXiv:2202.11776)',
     'version': 'v3, 23 Oct 2023',
     'url': 'https://arxiv.org/abs/2202.11776',
     'quote': ['there is a probability q after each item that system 2 wants to continue, and a complementary '
               'probability 1−q that system 2 views itself as “done” and derives no further utility'],
     'raw_file': 'attn/f1/kmr2022.txt',
     'agent_note': "BEARS: the user's reflective self ends the session on its own clock (per item) and utility is "
                   'counted per session; this is a user model, not a platform valuation, and no zero-stake claim is '
                   'made.'},
    {'id': 'f1:23',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'Kleinberg, Mullainathan, Raghavan (arXiv:2202.11776)',
     'version': 'v3, 23 Oct 2023',
     'url': 'https://arxiv.org/abs/2202.11776',
     'quote': ['One possible explanation is misaligned incentives: platforms are not optimizing for user happiness. We '
               'suggest the problem runs deeper, transcending the specific incentives of any particular platform'],
     'raw_file': 'attn/f1/kmr2022.txt',
     'agent_note': 'BEARS on U8: names the incentive explanation and sets it aside (the problem persists even for a '
                   'welfare-maximising platform); does not treat how incentives would be changed.'},
    {'id': 'f1:24',
     'tag': 'U4',
     'reading': 'states',
     'source': 'Stray, Vendrov, Nixon, Adler, Hadfield-Menell, "What are you optimizing for? Aligning Recommender '
               'Systems with Human Values" (arXiv:2107.10939; ICML 2020 PAML workshop)',
     'version': 'v1, 22 Jul 2021',
     'url': 'https://arxiv.org/abs/2107.10939',
     'quote': ['informed, deliberative, and perhaps retrospective evaluations are of a higher quality than immediate '
               'judgements',
               'Many people report that they watch more TV than they retrospectively endorse',
               'We describe cases where real recommender systems were modified in the service of various human values '
               'such as diversity, fairness, well-being, time well spent, and factual accuracy.'],
     'raw_file': 'attn/f1/stray2021.txt',
     'agent_note': "STATES the U4 objective: optimise the user's informed, retrospective value rather than immediate "
                   'behaviour ("time well spent"). Nothing on the pause or return.'},
    {'id': 'f1:25',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Stray, Halevy, Assar, Hadfield-Menell, Boutilier, et al., "Building Human Values into Recommender '
               'Systems: An Interdisciplinary Synthesis and Open Problems", ACM TORS 2(3) Art. 20, Sep 2024 '
               '(arXiv:2207.10192)',
     'version': 'v1, 20 Jul 2022 (arXiv); journal version Sep 2024',
     'url': 'https://arxiv.org/abs/2207.10192',
     'quote': ['Similarly, if social media recommenders should not optimize for engagement, then what should they '
               'optimize for?',
               'While today these teams are typically optimizing for purchases, subscriptions or user retention, '
               'recommender systems could also be managed on values-relevant outcomes.'],
     'raw_file': 'attn/f1/stray2022.txt',
     'agent_note': 'CLOSE form of U4 (and a U1 description: product teams optimise retention). Difference: a '
                   'research agenda naming values-relevant outcomes, not a valuation construction.'},
    {'id': 'f1:26',
     'tag': 'U8',
     'reading': 'addresses',
     'source': 'Stray et al., ACM TORS 2024 (arXiv:2207.10192)',
     'version': 'v1, 20 Jul 2022 (arXiv); journal version Sep 2024',
     'url': 'https://arxiv.org/abs/2207.10192',
     'quote': ['For example, subscription services must maximize user retention, while current recommender designs '
               'struggle with long-term outcomes.',
               'The challenge for policy-makers or regulators is to be both precise and general about how harms are to '
               'be assessed and values are to be enacted in recommender systems.'],
     'raw_file': 'attn/f1/stray2022.txt',
     'agent_note': 'ADDRESSES U8: the commercial pull toward retention and the role of external regulation are both '
                   'treated.'},
    {'id': 'f1:27',
     'tag': 'U6',
     'reading': 'mixed',
     'source': 'Stray et al., ACM TORS 2024 (arXiv:2207.10192)',
     'version': 'v1, 20 Jul 2022 (arXiv); journal version Sep 2024',
     'url': 'https://arxiv.org/abs/2207.10192',
     'quote': ['In the context of social media recommendation there has been mixed evidence regarding both positive '
               'and negative effects on adolescent well-being',
               'it is currently not clear if social media contributes to depression or if depressed people spend more '
               'time on social media, or both'],
     'raw_file': 'attn/f1/stray2022.txt',
     'agent_note': 'MIXED (as summarised by a 2022 review, not primary evidence; F3 carries the primary studies).'},
    {'id': 'f1:28',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Milli, Belli, Hardt, "From Optimizing Engagement to Measuring Value", FAccT 2021 (arXiv:2008.12623)',
     'version': 'v2, 19 Jul 2021',
     'url': 'https://arxiv.org/abs/2008.12623',
     'quote': ['there is potentially a large gap between engagement signals and a desired notion of "value" that is '
               'worth optimizing for',
               'provide a general latent variable model approach that can be used to operationalize the target '
               'construct and directly optimize for it'],
     'raw_file': 'attn/f1/milli2021.txt',
     'agent_note': 'CLOSE form of U4: optimise a measured notion of value instead of engagement (deployed at '
                   'Twitter). Difference: value is a latent construct inferred from behavioural signals, not the '
                   "user's stated/reflective judgement; nothing on the pause."},
    {'id': 'f1:29',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Milli, Carroll, Wang, Pandey, Zhao, Dragan, "Engagement, User Satisfaction, and the Amplification of '
               'Divisive Content on Social Media" (arXiv:2305.16941; PNAS Nexus 2025)',
     'version': 'v6, 7 Dec 2024',
     'url': 'https://arxiv.org/abs/2305.16941',
     'quote': ["suggesting that the engagement-based algorithm underperforms in satisfying users' stated preferences",
               "we explore the implications of an alternative approach that ranks content based on users' stated "
               'preferences'],
     'raw_file': 'attn/f1/milli2023.txt',
     'agent_note': 'CLOSE form of U4: ranking by stated preferences, tested against the engagement ranker in a '
                   'pre-registered audit. Difference: per-item ranking, no treatment of the return or pause; the '
                   'authors call for a balance of engagement and stated preferences.'},
    {'id': 'f1:30',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'Milli et al. (arXiv:2305.16941)',
     'version': 'v6, 7 Dec 2024',
     'url': 'https://arxiv.org/abs/2305.16941',
     'quote': ['randomized experiments at Twitter have shown that it increases the amount of time users spend on the '
               'platform compared to the reverse-chronological timeline'],
     'raw_file': 'attn/f1/milli2023.txt',
     'agent_note': 'BEARS on U8: the engagement ranker buys time on platform, which is what a switch away from it '
                   'would cost.'},
    {'id': 'f1:31',
     'tag': 'U1',
     'reading': 'states',
     'source': 'Cunningham, Pandey, Sigerson, Stray, Allen, Barrilleaux, Iyer, Milli, Kothari, Rezaei, "What We Know '
               'About Using Non-Engagement Signals in Content Ranking" (arXiv:2402.06831; Ann. NY Acad. Sci. 2025)',
     'version': 'v1, 9 Feb 2024',
     'url': 'https://arxiv.org/abs/2402.06831',
     'quote': ['Platforms often wish to estimate the set of weights that would maximize long-term retention',
               'There is strong evidence that ranking by predicted engagement is effective in increasing user '
               'retention.'],
     'raw_file': 'attn/f1/cunningham2024.txt',
     'agent_note': 'STATES U1 as industry practice (workshop with platform staff): ranking weights are tuned to '
                   'maximise long-term retention.'},
    {'id': 'f1:32',
     'tag': 'U8',
     'reading': 'addresses',
     'source': 'Cunningham et al. (arXiv:2402.06831)',
     'version': 'v1, 9 Feb 2024',
     'url': 'https://arxiv.org/abs/2402.06831',
     'quote': ['Multiple platforms reported maintaining long-term experiments which assigned users to a '
               'chronologically-ranked feed. Those users had substantially lower time-spent and retention, with the '
               'effects remaining over months or years.',
               'However retention can be further increased by incorporating other signals, including item "quality" '
               'proxies and asking users what they want to see with "item-level" surveys.'],
     'raw_file': 'attn/f1/cunningham2024.txt',
     'agent_note': 'ADDRESSES U8: the engagement/retention cost of dropping engagement ranking is quantified, and '
                   'the incentive-compatible route (non-engagement signals that also raise retention) is argued. '
                   'Note the route keeps retention as the judge.'},
    {'id': 'f1:33',
     'tag': 'U7',
     'reading': 'close',
     'source': 'Cunningham et al. (arXiv:2402.06831)',
     'version': 'v1, 9 Feb 2024',
     'url': 'https://arxiv.org/abs/2402.06831',
     'quote': ['User controls over ranking often have low usage rates, but when used they do correlate well with '
               'quality and item-level surveys.',
               'Ranking changes can alter the prevalence of self-reported experiences of various kinds (e.g. '
               'harassment) but seldom have large enough effects on attitude measures like user satisfaction, '
               'well-being, polarization etc. to be measured in typical experiments.'],
     'raw_file': 'attn/f1/cunningham2024.txt',
     'agent_note': 'CLOSE form of U7: opt-in user controls are rarely used and ranking changes rarely show measurable '
                   'well-being effects. Difference: about ranking controls, not break reminders / time limits; F2 '
                   'carries the company countermeasures.'},
    {'id': 'f1:34',
     'tag': 'U1',
     'reading': 'states',
     'source': 'Agarwal, Usunier, Lazaric, Nickel, "System-2 Recommenders: Disentangling Utility and Engagement in '
               'Recommendation Systems via Temporal Point-Processes", FAccT 2024 (arXiv:2406.01611)',
     'version': 'v1, 29 May 2024',
     'url': 'https://arxiv.org/abs/2406.01611',
     'quote': ['In this paper we explore a new approach to recommender systems where we infer user utility based on '
               'their return probability to the platform rather than engagement signals.',
               'Our intuition is that users tend to return to a platform in the long run if it creates utility for '
               'them'],
     'raw_file': 'attn/f1/system2.txt',
     'agent_note': 'STATES U1 in its welfare-motivated form, and is the direct counter-position to U3/U5: the user\'s '
                   'return (arrival rate) is taken as the evidence of reflective utility, so the return is valued.'},
    {'id': 'f1:35',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Agarwal et al., FAccT 2024 (arXiv:2406.01611)',
     'version': 'v1, 29 May 2024',
     'url': 'https://arxiv.org/abs/2406.01611',
     'quote': ['The System-2 arrival intensity depends on the utility and has a long lasting effect, while the '
               'System-1 intensity depends on the instantaneous gratification and tends to vanish rapidly.'],
     'raw_file': 'attn/f1/system2.txt',
     'agent_note': 'CLOSE form of U4: optimise reflective (System-2) utility, separated from impulse. Difference: '
                   'utility is read off returns (a wall-clock quantity), the opposite of the empty pause.'},
    {'id': 'f1:36',
     'tag': 'U5',
     'reading': 'close',
     'source': 'Anwar, Dhillon, Schoenebeck, "Recommendation and Temptation", RecSys 2025 (arXiv:2412.10595)',
     'version': 'v2, 23 Jul 2025',
     'url': 'https://arxiv.org/abs/2412.10595',
     'quote': ['We aim to design a recommendation system that ensures as much enrichment from consumption as possible.',
               'In the second case, where any platform content is likely less enriching than studying, maximizing '
               'enrichment requires helping the user avoid the platform altogether by recommending minimally tempting '
               'content or no recommendations at all.',
               'rating an item typically involves more deliberate reflection from a user compared to the often more '
               'impulsive act of choosing what to consume'],
     'raw_file': 'attn/f1/temptation.txt',
     'agent_note': 'CLOSEST to U5 in F1: the objective is the user\'s reflective value (enrichment, estimated from '
                   'deliberate ratings) summed over choice rounds, with no retention or return term, and leaving the '
                   'platform can be optimal. Differences: (i) the objective counts the enrichment of the off-platform '
                   'option, so it is not indifferent to the stop (it can favour it); (ii) rounds are platform choice '
                   'occasions over a fixed horizon T, not the user\'s own active steps; (iii) no zero-stake / pause '
                   'statement and no notifications.'},
    {'id': 'f1:37',
     'tag': 'U3',
     'reading': 'close',
     'source': 'Anwar, Dhillon, Schoenebeck, RecSys 2025 (arXiv:2412.10595)',
     'version': 'v2, 23 Jul 2025',
     'url': 'https://arxiv.org/abs/2412.10595',
     'quote': ['It chooses what to recommend by maximizing the expected enrichment in a single round from an item.'],
     'raw_file': 'attn/f1/temptation.txt',
     'agent_note': 'CLOSE form of U3: the optimal policy is locally greedy (per-round value, no future term, hence '
                   'no term on return). Difference: per-round enrichment, not engagement or pause content; the '
                   'greedy optimality is a theorem of their model, not a design choice to remove a stake.'},
    {'id': 'f1:38',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'Anwar, Dhillon, Schoenebeck, RecSys 2025 (arXiv:2412.10595)',
     'version': 'v2, 23 Jul 2025',
     'url': 'https://arxiv.org/abs/2412.10595',
     'quote': ['He acknowledges navigating a tradeoff between the educational value of Duolingo and its ability to '
               'retain users.'],
     'raw_file': 'attn/f1/temptation.txt',
     'agent_note': 'BEARS on U8: an industry example of the value-vs-retention trade-off; no incentive analysis.'},
    {'id': 'f1:39',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Ashton, Franklin, "Solutions to preference manipulation in recommender systems require knowledge of '
               'meta-preferences", RecSys 2022 FAccTRec workshop (arXiv:2209.11801)',
     'version': 'v1, 14 Sep 2022',
     'url': 'https://arxiv.org/abs/2209.11801',
     'quote': ['solutions to preference manipulation in recommender systems must take into account certain '
               'meta-preferences (preferences over another preference) in order to respect the autonomy of the user '
               'and not be manipulative',
               'a recommender serving content to a user using a preference set based on the counterfactual world '
               'where the user had not interacted with the system removes the preference manipulative incentive'],
     'raw_file': 'attn/f1/ashton2022.txt',
     'agent_note': "CLOSE form of U4 (meta-preferences as the user's reflective standard). The second quote reports "
                   'Everitt et al. 2021: a counterfactual valuation removes the incentive, the same logical shape as '
                   'Proposition 7 applied to preferences, not to the pause.'},
    {'id': 'f1:40',
     'tag': 'U4',
     'reading': 'close',
     'source': 'Zou, Sun, Ji, Zhang, Wang, Zhang, Jiang, "Hesitation and Tolerance in Recommender Systems", CHI 2026 '
               '(arXiv:2412.09950)',
     'version': 'v2, 15 Feb 2026',
     'url': 'https://arxiv.org/abs/2412.09950',
     'quote': ['Instead, recommender systems should be optimized for what we termlow-regret satisfaction: interactions '
               'that respect users’ time, reduce unnecessary effort, and deliver value that feels meaningful.',
               'even lightweight strategies treating tolerance as distinct from interest can improve retention while '
               'reducing wasted effort'],
     'raw_file': 'attn/f1/hesitation.txt',
     'agent_note': "CLOSE form of U4 (respect for the user's time; low-regret value). Difference: success is still "
                   'validated on next-day retention, so the return keeps its place in the objective.'},
    {'id': 'f1:41',
     'tag': 'U3',
     'reading': 'close',
     'source': 'Ben Ayed, Feng, Adams, Singh, Anand, Xu, "RecoMind: A Reinforcement Learning Framework for Optimizing '
               'In-Session User Satisfaction in Recommendation Systems" (Pinterest) (arXiv:2508.00201)',
     'version': 'v1, 31 Jul 2025',
     'url': 'https://arxiv.org/abs/2508.00201',
     'quote': ['Each episode involves a fixed user and terminates when the user exits the platform.',
               'our goal is to optimize long-term user engagement at the session level'],
     'raw_file': 'attn/f1/recomind.txt',
     'agent_note': 'CLOSE form of U3: a session-episode valuation has no term on the return (the episode ends at '
                   "exit). Difference: the reward is in-session engagement (session depth), so the user's in-session "
                   'stop still removes represented value (non-zero content at the stop); not reflective value; no '
                   'zero-stake statement.'},
]
