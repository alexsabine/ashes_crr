"""Claims for Attention_Algorithms/DECLARATION.md, family F2 (company practice and regulation), transcribed from
docs/citations/attention_f2_2026-09-28.md (fetched 2026-09-28 by the F2 literature agent; raw texts saved in the session
scratchpad under attn/f2/, not committed: third-party texts). 'reading' is the investigator's reading, decided after reading
the quotes: for U1-U5 and U7 'states' / 'close' (the difference is named in agent_note) / 'bears'; for U8 'addresses' /
'bears'. Every quote is an exact substring of its raw file after whitespace collapsing (checked by hand on 2026-09-28).
Sources marked SECONDARY in 'source' are reputable reports quoting a primary that was blocked (HTTP 403) on the day.
"""

CLAIMS = [
    # ---------------------------------------------------------------- company tools (U7)
    {'id': 'f2:0',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'YouTube Help, "Take a break reminder" (Android)',
     'version': 'help page as served 2026-09-28 (no date shown)',
     'url': 'https://support.google.com/youtube/answer/9012523?hl=en&co=GENIE.Platform%3DAndroid',
     'quote': ['The take a break reminder lets you set a reminder to take a break while watching videos. The reminder will '
               'pause your video until you dismiss it or resume playing the video.',
               'Note: For users aged 13–17 on YouTube, the take a break reminder is set to “On” by default. For users 18 or '
               'over, the default setting is “Off.”',
               'If you close the app, sign out, switch devices, or pause a video for more than 30 minutes, the timer will '
               'reset.'],
     'raw_file': 'attn/f2/yt_take_a_break.txt',
     'agent_note': 'Default ON for 13-17, opt-in (default OFF) for adults; dismissible by the user. A countermeasure beside '
                   'the recommender, not a change to its objective. No effect evidence given.'},
    {'id': 'f2:1',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'YouTube Help, "Set a bedtime reminder" (Android)',
     'version': 'help page as served 2026-09-28 (no date shown)',
     'url': 'https://support.google.com/youtube/answer/9884905?hl=en&co=GENIE.Platform%3DAndroid',
     'quote': ['Note: For users aged 13-17 on YouTube, the bedtime reminder is set to On by default. For users 18 or over, '
               'the default setting is Off.',
               'When your bedtime reminder goes off, you can dismiss it by tapping in the top-right corner, or you can tap '
               'Remind Me Again to get another reminder in 15 minutes.'],
     'raw_file': 'attn/f2/yt_bedtime.txt',
     'agent_note': 'Default ON for 13-17, opt-in for adults; a dismissible/snoozable reminder. No effect evidence given.'},
    {'id': 'f2:2',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Meta Newsroom, "Introducing Instagram Teen Accounts: Built-In Protections for Teens, Peace of Mind for '
               'Parents"',
     'version': 'published 2024-09-17, page shows update 2025-10-22',
     'url': 'https://about.fb.com/news/2024/09/instagram-teen-accounts/',
     'quote': ['These protections are turned on automatically, and parents decide if teens under 16 can change any of these '
               'settings to be less strict:',
               'Time limit reminders: Teens will get notifications telling them to leave the app after 60 minutes each day.',
               'Sleep mode enabled: Sleep mode will be turned on between 10 PM and 7 AM, which will mute notifications '
               'overnight and send auto-replies to DMs.'],
     'raw_file': 'attn/f2/ig_teen_accounts.txt',
     'agent_note': 'Default ON for teens (under-16s need parental permission to loosen). The 60-minute item is a reminder, '
                   'not a cap; hard daily limits exist only as an opt-in parental supervision setting. No effect evidence '
                   'in this post.'},
    {'id': 'f2:3',
     'tag': 'U4',
     'reading': 'bears',
     'source': 'Meta Newsroom, "Introducing Instagram Teen Accounts: Built-In Protections for Teens, Peace of Mind for '
               'Parents"',
     'version': 'published 2024-09-17, page shows update 2025-10-22',
     'url': 'https://about.fb.com/news/2024/09/instagram-teen-accounts/',
     'quote': ['Teen Accounts will limit who can contact teens and the content they see, and help ensure their time is well '
               'spent.',
               'Teens will also get access to a new feature, made just for them, that lets them select topics they want to '
               'see more of in Explore and their recommendations'],
     'raw_file': 'attn/f2/ig_teen_accounts.txt',
     'agent_note': "Bears on U4 only: 'time well spent' is a product goal and stated topic choice is an input to "
                   'recommendations; the ranking objective is not said to be the teen\'s stated or reflective value.'},
    {'id': 'f2:4',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Meta Newsroom, "Instagram Quiet Mode: A New Way to Manage Your Time and Focus"',
     'version': 'published 2023-01-19, page shows update 2025-09-04 (renamed Sleep mode)',
     'url': 'https://about.fb.com/news/2023/01/instagram-quiet-mode-manage-your-time-and-focus/',
     'quote': ['Anyone can use Quiet mode, but we’ll prompt teens to do so when they spend a specific amount of time on '
               'Instagram late at night.',
               'once the feature is turned off, we’ll show you a quick summary of notifications so you can catch up on what '
               'you missed.'],
     'raw_file': 'attn/f2/ig_quiet_mode.txt',
     'agent_note': 'Opt-in at launch (teens prompted); since 2024 on by default for teens as Sleep mode (f2:2). The '
                   'post-pause notification summary releases what the pause held back. No effect evidence.'},
    {'id': 'f2:5',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'TikTok Newsroom, "New features for teens and families on TikTok" (Cormac Keenan)',
     'version': '2023-03-01',
     'url': 'https://newsroom.tiktok.com/en-us/new-features-for-teens-and-families-on-tiktok-us',
     'quote': ['In the coming weeks, every account belonging to a user below age 18 will automatically be set to a 60-minute '
               'daily screen time limit.',
               "If the 60-minute limit is reached, teens will be prompted to enter a passcode in order to continue watching, "
               "requiring them to make an active decision to extend that time.",
               "So we're also prompting teens to set a daily screen time limit if they opt out of the 60-minute default and "
               "spend more than 100 minutes on TikTok in a day.",
               'our tests found this helped increase the use of our screen time tools by 234%.'],
     'raw_file': 'attn/f2/tiktok_2023_limits.txt',
     'agent_note': 'Default ON for under-18s but self-overridable by passcode (teens can opt out). The only effect figure '
                   'is uptake of the tools (+234%), not reduced use or wellbeing.'},
    {'id': 'f2:6',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'TikTok Newsroom, "New ways we\'re supporting parents and helping teens build balanced digital habits" '
               '(Adam Presser)',
     'version': '2025-03-11',
     'url': 'https://newsroom.tiktok.com/en-us/new-ways-we-are-supporting-parents-and-helping-teens-build-balanced-digital-habits',
     'quote': ['If a teen under 16 is on TikTok after 10pm, their For You feed will be interrupted with our new wind down '
               'feature.',
               'If a teen decides to spend additional time on TikTok after the first reminder, we show a second, harder to '
               'dismiss, full-screen prompt. As before, we deliberately do not send push notifications to teens at night, '
               'which cannot be changed.',
               'In countries where this has already been piloted, the vast majority of teens decide to keep this reminder '
               'on.'],
     'raw_file': 'attn/f2/tiktok_2025_winddown.txt',
     'agent_note': 'Wind-down default for under-16s; night push notifications off for teens and not changeable (a default '
                   'that removes a night re-engagement channel). Effect evidence is only that most teens keep the reminder '
                   'on, not that use falls.'},
    {'id': 'f2:7',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Android Help, "Manage how you spend time on your Android phone with Digital Wellbeing"',
     'version': 'help page as served 2026-09-28 (no date shown)',
     'url': 'https://support.google.com/android/answer/9346420?hl=en',
     'quote': ['For example, you can set app timers and schedule display changes.',
               "Choose which apps you want to pause. When Focus mode is on, you can't use these apps and won't get "
               'notifications from them.',
               'To use the app again before midnight, follow steps 1–4 above and delete the app timer.'],
     'raw_file': 'attn/f2/android_dw.txt',
     'agent_note': 'OS-level, opt-in tools outside any platform objective; the user can delete a timer to continue. No '
                   'effect evidence given.'},
    {'id': 'f2:8',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Meta Newsroom, "We\'re Introducing New Built-In Restrictions for Instagram Teen Accounts, and Expanding to '
               'Facebook and Messenger"',
     'version': 'published 2025-04-08, page shows update 2025-07-09',
     'url': 'https://about.fb.com/news/2025/04/introducing-new-built-in-restrictions-instagram-teen-accounts-expanding-facebook-messenger/',
     'quote': ['Since making these changes, 97% of teens aged 13-15 have stayed in these built-in restrictions, which we '
               'believe offer the most age-appropriate experience for younger teens.',
               'They also have notifications turned off overnight and reminders to leave the app after 60 minutes'],
     'raw_file': 'attn/f2/meta_teen_accounts_2025_04.txt',
     'agent_note': 'Company-reported default retention (97% of 13-15s; loosening needs parental permission). This is '
                   'evidence that defaults stick, not that reminders reduce use or improve wellbeing.'},
    # ---------------------------------------------------------------- EU regulator (DSA)
    {'id': 'f2:9',
     'tag': 'U2',
     'reading': 'close',
     'source': 'European Commission press release IP/26/312, "Commission preliminarily finds TikTok\'s addictive design in '
               'breach of the Digital Services Act"',
     'version': '2026-02-06',
     'url': 'https://ec.europa.eu/commission/presscorner/detail/en/ip_26_312',
     'quote': ['This includes features such as infinite scroll, autoplay, push notifications, and its highly personalised '
               'recommender system.',
               "by constantly ‘rewarding' users with new content, certain design features of TikTok fuel the urge to keep "
               "scrolling and shift the brain of users into ‘autopilot mode'."],
     'raw_file': 'attn/f2/ec_tiktok_prelim_2026.txt',
     'agent_note': 'Close to U2: names push notifications, autoplay, infinite scroll and the personalised recommender as '
                   'addictive design. Difference: it does not attribute them to an objective that values the user\'s '
                   'return. Preliminary finding.'},
    {'id': 'f2:10',
     'tag': 'U1',
     'reading': 'bears',
     'source': 'European Commission press release IP/26/312 (TikTok, preliminary findings)',
     'version': '2026-02-06',
     'url': 'https://ec.europa.eu/commission/presscorner/detail/en/ip_26_312',
     'quote': ['TikTok disregarded important indicators of compulsive use of the app, such as the time that minors spend on '
               'TikTok at night, the frequency with which users open the app, and other potential indicators.'],
     'raw_file': 'attn/f2/ec_tiktok_prelim_2026.txt',
     'agent_note': 'Bears on U1: the frequency of opening the app (returns) is read by the regulator as a compulsion '
                   'indicator; it says nothing about the objective valuing returns.'},
    {'id': 'f2:11',
     'tag': 'U7',
     'reading': 'close',
     'source': 'European Commission press release IP/26/312 (TikTok, preliminary findings)',
     'version': '2026-02-06',
     'url': 'https://ec.europa.eu/commission/presscorner/detail/en/ip_26_312',
     'quote': ['The time management tools do not seem to be effective in enabling users to reduce and control their use of '
               'TikTok because they are easy to dismiss and introduce limited friction.',
               "TikTok needs to change the basic design of its service. For instance, by disabling key addictive features "
               "such as ‘infinite scroll' over time, implementing effective ‘screen time breaks', including during the "
               "night, and adapting its recommender system."],
     'raw_file': 'attn/f2/ec_tiktok_prelim_2026.txt',
     'agent_note': 'Close to U7: a regulator finds the tools ineffective (easy to dismiss) and asks for change to the basic '
                   'design including the recommender. Difference: it does not say the tools are opt-in, nor frame the '
                   'failure as the objective\'s stake left intact. Preliminary; effect evidence (internal data) not '
                   'published.'},
    {'id': 'f2:12',
     'tag': 'U7',
     'reading': 'close',
     'source': 'European Commission press release IP/26/1579, "Commission preliminarily finds the addictive design of '
               'Instagram and Facebook in breach of the Digital Services Act"',
     'version': '2026-07-10',
     'url': 'https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1579',
     'quote': ["Instagram's and Facebook's time management tools, including those activated by default for teens, can be "
               'easily dismissed and do not lead to a meaningful reduction and control of the usage of the service.'],
     'raw_file': 'attn/f2/ec_meta_prelim_2026.txt',
     'agent_note': 'Close to U7 (weak effect), and notable: even the DEFAULT-on teen tools are found ineffective, so '
                   '"mostly opt-in" is not the whole reason. Difference: no statement about the objective\'s stake. '
                   'Preliminary finding.'},
    {'id': 'f2:13',
     'tag': 'U4',
     'reading': 'close',
     'source': 'European Commission press release IP/26/1579 (Meta, preliminary findings)',
     'version': '2026-07-10',
     'url': 'https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1579',
     'quote': ["disabling key addictive features such as 'autoplay' and ‘infinite scroll' by default, implementing effective "
               "‘screen time breaks', and adapting its recommender system to make it less engagement-oriented."],
     'raw_file': 'attn/f2/ec_meta_prelim_2026.txt',
     'agent_note': 'Close to U4: the regulator asks for a less engagement-oriented recommender. Difference: it names no '
                   'replacement objective (stated or reflective value) and nothing about how the pause is represented.'},
    {'id': 'f2:14',
     'tag': 'U2',
     'reading': 'close',
     'source': 'European Commission press release IP/26/1579 (Meta, preliminary findings)',
     'version': '2026-07-10',
     'url': 'https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1579',
     'quote': ['Meta did not consider certain design features of Instagram and Facebook, such as highly personalised '
               'recommendations, autoplay and infinite scroll, which constantly show users new content.',
               'how the optimisation of its different formats - such as reels and stories - could lead to excessive or '
               'compulsive use of the services.'],
     'raw_file': 'attn/f2/ec_meta_prelim_2026.txt',
     'agent_note': 'Close to U2: optimisation of formats is linked to excessive use, and features with no stopping point '
                   'are named. Difference: re-engagement after a pause (notifications timed to absence) is not '
                   'singled out; the link to a return-valuing objective is not drawn.'},
    {'id': 'f2:15',
     'tag': 'U2',
     'reading': 'bears',
     'source': 'Regulation (EU) 2022/2065 (Digital Services Act), recital 83 and Article 34(1)',
     'version': 'OJ L 277, 27.10.2022 (original act; Cellar xhtml, EUR-Lex HTML bot-walled)',
     'url': 'https://eur-lex.europa.eu/eli/reg/2022/2065/oj',
     'quote': ['or from online interface design that may stimulate behavioural addictions of recipients of the service.',
               'serious negative consequences to the person’s physical and mental well-being.'],
     'raw_file': 'attn/f2/dsa_text.txt',
     'agent_note': 'Bears on U2: the DSA names interface design that may stimulate behavioural addiction as a systemic risk '
                   'VLOPs must assess (Art. 34). No mechanism (objective, return) is stated.'},
    {'id': 'f2:16',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Regulation (EU) 2022/2065 (Digital Services Act), Articles 38 and 25(1)',
     'version': 'OJ L 277, 27.10.2022 (original act)',
     'url': 'https://eur-lex.europa.eu/eli/reg/2022/2065/oj',
     'quote': ['shall provide at least one option for each of their recommender systems which is not based on profiling as '
               'defined in Article 4, point (4), of Regulation (EU) 2016/679.',
               'Providers of online platforms shall not design, organise or operate their online interfaces in a way that '
               'deceives or manipulates the recipients of their service or in a way that otherwise materially distorts or '
               'impairs the ability of the recipients of their service to make free and informed decisions.'],
     'raw_file': 'attn/f2/dsa_text.txt',
     'agent_note': 'The Art. 38 non-profiling option is a mandated alternative the user must choose (opt-in); the '
                   'profiled feed stays the default. No effect evidence in the text.'},
    {'id': 'f2:17',
     'tag': 'U2',
     'reading': 'states',
     'source': 'European Commission, Guidelines on measures to ensure a high level of privacy, safety and security for '
               'minors online, pursuant to Article 28(4) DSA, C(2025) 6826 final',
     'version': 'document dated Brussels, 7.10.2025 (as served by the Commission library link; guidelines announced '
                '2025-07-14 per search summaries, not verified)',
     'url': 'https://ec.europa.eu/newsroom/dae/redirection/document/118226',
     'quote': ['Ensuring that minors are not exposed to persuasive design features that are aimed predominantly at '
               'engagement and that may lead to extensive use or overuse of the platform or problematic or compulsive '
               'behavioural habits.',
               'artificially timed to regain minors’ attention'],
     'raw_file': 'attn/f2/ec_minors_guidelines_2025.txt',
     'agent_note': 'States U2 for minors: design aimed at engagement, including notifications timed to regain attention '
                   '(re-engagement after absence), infinite scroll and autoplay. Not legally binding; used by the '
                   'Commission to assess Art. 28(1).'},
    {'id': 'f2:18',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'European Commission, Art. 28 DSA guidelines on minors, C(2025) 6826 final',
     'version': 'document dated Brussels, 7.10.2025',
     'url': 'https://ec.europa.eu/newsroom/dae/redirection/document/118226',
     'quote': ['vi. the default autoplay of videos and hosting live streams are turned off.',
               'vii. push notifications are turned off by default and are always off during core',
               'To be effective, these tools should deter minors from spending more time on the platform.'],
     'raw_file': 'attn/f2/ec_minors_guidelines_2025.txt',
     'agent_note': 'Regulator asks that the countermeasures be DEFAULTS for minors (autoplay off, push off, off in sleep '
                   'hours) and that time tools be judged by whether they deter use. No effect evidence.'},
    {'id': 'f2:19',
     'tag': 'U4',
     'reading': 'close',
     'source': 'European Commission, Art. 28 DSA guidelines on minors, C(2025) 6826 final',
     'version': 'document dated Brussels, 7.10.2025',
     'url': 'https://ec.europa.eu/newsroom/dae/redirection/document/118226',
     'quote': ['Prioritise ‘explicit user-provided signals’ to determine the content displayed and recommended to minors.',
               'including the stated and deliberative selection of topics of interest, surveys, reporting'],
     'raw_file': 'attn/f2/ec_minors_guidelines_2025.txt',
     'agent_note': 'Close to U4: stated, deliberative preferences are to be prioritised over implicit engagement signals '
                   '(time spent, click-through). Difference: these are input signals, not the optimised objective; the '
                   'pause is not addressed.'},
    {'id': 'f2:20',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'European Commission, "Commission launches open consultation on the forthcoming Digital Fairness Act"',
     'version': 'published 2025-07-17 (consultation open 2025-07-17 to 2025-10-24; page last update 2025-08-04)',
     'url': 'https://digital-strategy.ec.europa.eu/en/consultations/commission-launches-open-consultation-forthcoming-digital-fairness-act',
     'quote': ['addictive design of digital products and unfair personalisation practices, especially where consumer '
               'vulnerabilities are exploited for commercial purposes.'],
     'raw_file': 'attn/f2/dfa_consultation.txt',
     'agent_note': 'Bears on U8: addictive design is linked to commercial exploitation and slated for consumer law. The '
                   'consultation questionnaire itself was not fetched.'},
    # ---------------------------------------------------------------- UK
    {'id': 'f2:21',
     'tag': 'U2',
     'reading': 'close',
     'source': 'ICO, Age appropriate design: a code of practice for online services, standard 5 "Detrimental use of data"',
     'version': 'web page as served 2026-09-28 (no page date shown)',
     'url': 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/5-detrimental-use-of-data/',
     'quote': ['Strategies used to extend user engagement, sometimes referred to as ‘sticky’ features can include mechanisms '
               'such as reward loops, continuous scrolling, notifications and auto-play features which encourage users to '
               'continue playing a game, watching video content or otherwise staying online.',
               'avoid features which use personal data to automatically extend use instead of requiring children to make '
               'an active choice about whether they want to spend their time in this way (data-driven autoplay features)'],
     'raw_file': 'attn/f2/ico_aadc_detrimental.txt',
     'agent_note': 'Close to U2: engagement-extension strategies named (notifications, autoplay, continuous scroll). '
                   'Difference: framed as extending a session, not as re-engagement driven by a stake in the user\'s return.'},
    {'id': 'f2:22',
     'tag': 'U3',
     'reading': 'close',
     'source': 'ICO, Age appropriate design code, standard 5 "Detrimental use of data"',
     'version': 'web page as served 2026-09-28',
     'url': 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/5-detrimental-use-of-data/',
     'quote': ['in a way that makes it easy for them to disengage without feeling pressurised or disadvantaged if they do so.',
               'present options to continue playing or otherwise engaging with your service neutrally without suggesting '
               'that children will lose out if they don’t;',
               'introduce mechanisms such as pause buttons which allow children to take a break at any time without losing '
               'their progress in a game'],
     'raw_file': 'attn/f2/ico_aadc_detrimental.txt',
     'agent_note': "Close to U3 from the user's side: a pause that costs the child nothing and neutral framing of "
                   'continuing. Difference: the ICO removes the loss to the USER at the pause; U3 removes the pause\'s '
                   "content in the SERVICE's valuation (its incentive). No objective is specified."},
    # ---------------------------------------------------------------- US states
    {'id': 'f2:23',
     'tag': 'U1',
     'reading': 'states',
     'source': 'New York Attorney General press release, "Attorney General James and Governor Hochul Release Final SAFE '
               'for Kids Act Rules to Protect Children Online"',
     'version': '2026-07-28 (rules to be published in the State Register 2026-07-29; Act effective 2027-01-25)',
     'url': 'https://ag.ny.gov/press-release/2026/attorney-general-james-and-governor-hochul-release-final-safe-kids-act-rules',
     'quote': ['Algorithmically personalized feeds, or addictive feeds, recommend or personalize content for users in an '
               'endless stream based on data that the platform gathers about the user. They are designed to encourage a '
               'user to continue to use and return to a platform.'],
     'raw_file': 'attn/f2/ny_ag_final_rules_2026.txt',
     'agent_note': "States U1 as a regulator's description: the feed's design aim includes the user's return. It does "
                   'not use objective/loss language; it is a descriptive characterisation, not evidence of a specific '
                   "company's objective."},
    {'id': 'f2:24',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'New York Attorney General press release (SAFE for Kids Act final rules)',
     'version': '2026-07-28',
     'url': 'https://ag.ny.gov/press-release/2026/attorney-general-james-and-governor-hochul-release-final-safe-kids-act-rules',
     'quote': ['Instead of the default algorithmically personalized feeds designed to keep young people on the platform, '
               'users under 18 will only be shown content from other accounts they follow or otherwise select in a set '
               'sequence, such as chronological order, unless they get parental consent for an addictive feed.',
               'The law also prohibits social media platforms from sending notifications to users under 18 from 12 a.m. '
               'to 6 a.m. without parental consent.',
               "kids' safety should come before Big Tech’s profits"],
     'raw_file': 'attn/f2/ny_ag_final_rules_2026.txt',
     'agent_note': 'Bears on U8: regulation flips the DEFAULT for minors (chronological feed, no night notifications) '
                   'and a sponsor names the safety/profit conflict; the incentive mechanism itself is not analysed.'},
    {'id': 'f2:25',
     'tag': 'U2',
     'reading': 'bears',
     'source': 'California SB 976, Protecting Our Kids from Social Media Addiction Act (Stats. 2024, ch. 321)',
     'version': 'Chaptered, approved by Governor 2024-09-20',
     'url': 'https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB976',
     'quote': ['However, some social media platforms have evolved to include addictive features, including the algorithmic '
               'delivery of content and other design features, that pose a significant risk of harm to the mental health '
               'and well-being of children and adolescents.'],
     'raw_file': 'attn/f2/ca_sb976.txt',
     'agent_note': 'Legislative finding; bears on U2 (algorithmic delivery as an addictive feature). Litigation status '
                   '(NetChoice v. Bonta; Ninth Circuit 2025-09-09 upheld the feed provisions, parts enjoined) is from '
                   'search summaries only, not fetched.'},
    {'id': 'f2:26',
     'tag': 'U8',
     'reading': 'addresses',
     'source': 'California SB 976 (Stats. 2024, ch. 321), Health and Safety Code §§ 27002, 27004',
     'version': 'Chaptered, approved by Governor 2024-09-20',
     'url': 'https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB976',
     'quote': ['This setting shall be set by the operator as on by default, in a manner in which the child’s access is '
               'limited to one hour per day unless modified by the verified parent.',
               'the operator of an addictive internet-based service or application shall not withhold, degrade, lower the '
               'quality of, or increase the price of, any product, service, or feature, other than as required by this '
               'chapter, due to a user or parent availing themselves of the rights provided by this chapter'],
     'raw_file': 'attn/f2/ca_sb976.txt',
     'agent_note': 'Addresses U8: the statute anticipates the operator\'s incentive to penalise users who opt out and '
                   'forbids it, and makes the time limit a default. (Default-on status of these parental controls may be '
                   'affected by the litigation; not verified here.)'},
    # ---------------------------------------------------------------- Australia
    {'id': 'f2:27',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth), No. 127, 2024',
     'version': 'Authorised Version C2024A00127 registered 12/12/2024 (as made)',
     'url': 'https://www.legislation.gov.au/C2024A00127/asmade/2024-12-10/text/original/pdf',
     'quote': ['The object of this Part is to reduce the risk of harm to age-restricted users from certain kinds of social '
               'media platforms.',
               'A provider of an age-restricted social media platform must take reasonable steps to prevent '
               'age-restricted users having accounts with the age-restricted social media platform.'],
     'raw_file': 'attn/f2/au_min_age_act_2024.txt',
     'agent_note': 'Bears on U8: the regulatory route chosen here excludes under-16s rather than changing the objective; '
                   'nothing about incentives or design. (Commencement 2025-12-10 is from search summaries.)'},
    # ---------------------------------------------------------------- US Surgeon General (SECONDARY)
    {'id': 'f2:28',
     'tag': 'U2',
     'reading': 'close',
     'source': 'SECONDARY: Chief Healthcare Executive, "Surgeon General warns social media poses risks to kids, and '
               'health groups back him up", quoting the 2023 U.S. Surgeon General\'s Advisory (hhs.gov PDF returned 403)',
     'version': 'report on the advisory of 2023-05-23; report date not shown in the saved text',
     'url': 'https://www.chiefhealthcareexecutive.com/view/surgeon-general-warns-social-media-poses-risks-to-kids-and-health-groups-back-him-up',
     'quote': ['The advisory also suggests companies should “avoid design features that attempt to maximize time, attention, '
               'and engagement.”',
               'And for too many children, social media use is compromising their sleep and valuable in-person time with '
               'family and friends,'],
     'raw_file': 'attn/f2/che_sg_advisory_2023_report.txt',
     'agent_note': 'Close to U2 (via a report quoting the advisory): design features that maximise time and engagement. '
                   'Difference: no statement about returns or re-engagement after absence. Primary blocked (HTTP 403 on '
                   'hhs.gov; NCBI Bookshelf reCAPTCHA).'},
    {'id': 'f2:29',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'SECONDARY: CNN, "New surgeon general\'s advisory raises alarm about screen time risks for kids and teens", '
               'reporting the 2026 HHS/Surgeon General advisory on screen time (primary not fetched: hhs.gov 403)',
     'version': '2026-05-20',
     'url': 'https://www.cnn.com/2026/05/20/health/surgeon-general-advisory-screen-time-wellness',
     'quote': ['Tech companies display warnings about harmful screen use and adhere to and enforce age minimums.',
               'nearly half of adolescents admit that they lose track of the amount of time they spend on their phones.'],
     'raw_file': 'attn/f2/cnn_sg_advisory_2026.txt',
     'agent_note': 'As reported, the 2026 advisory asks companies for warnings and age minimums, i.e. more countermeasures '
                   'beside the objective. No effect evidence reported.'},
    # ---------------------------------------------------------------- litigation
    {'id': 'f2:30',
     'tag': 'U2',
     'reading': 'states',
     'source': 'Colorado Attorney General press release, "Bipartisan coalition of attorneys general file lawsuits against '
               'Meta for harming youth mental health through its social media platforms"',
     'version': '2023-10-24',
     'url': 'https://coag.gov/press-releases/bipartisan-coalition-of-attorneys-general-file-lawsuits-against-meta-for-harming-youth-mental-health-through-its-social-media-platforms/',
     'quote': ['Its platform algorithms push users into descending “rabbit holes” in an effort to maximize engagement. '
               'Features like infinite scroll and near-constant alerts were created with the express goal of hooking young '
               'users. These manipulative tactics continually lure children and teens back onto the platform.'],
     'raw_file': 'attn/f2/coag_meta_complaint_2023.txt',
     'agent_note': 'States U2 as an ALLEGATION (complaint summary): alerts and infinite scroll built to maximise '
                   'engagement and to bring young users back. Allegation, not a finding.'},
    {'id': 'f2:31',
     'tag': 'U8',
     'reading': 'bears',
     'source': 'Colorado Attorney General press release (multistate complaint against Meta)',
     'version': '2023-10-24',
     'url': 'https://coag.gov/press-releases/bipartisan-coalition-of-attorneys-general-file-lawsuits-against-meta-for-harming-youth-mental-health-through-its-social-media-platforms/',
     'quote': ['Meta chose to maximize its profits at the expense of public health'],
     'raw_file': 'attn/f2/coag_meta_complaint_2023.txt',
     'agent_note': 'Bears on U8: the profit/health conflict is asserted (an AG statement), not analysed.'},
    {'id': 'f2:32',
     'tag': 'U8',
     'reading': 'addresses',
     'source': 'Office of the Attorney General for the District of Columbia, "Attorney General Schwalb Announces That Meta '
               'Will Pay Up to $17.1 Billion for Exploiting Kids with Intentionally Addictive Social Media Platforms"',
     'version': '2026-08-26',
     'url': 'https://oag.dc.gov/release/attorney-general-schwalb-announces-meta-will-pay',
     'quote': ['This bipartisan, nationwide investigation found that Meta, with the goal of driving ever-increasing '
               'advertising revenue, designed Facebook and Instagram’s features to addict children',
               'Meta will pay an additional $5 billion—increasingly the total settlement amount to $17.1 billion—and '
               'enhance the new safety features it is implementing if and when other major social media companies also '
               'agree to adopt these features.'],
     'raw_file': 'attn/f2/dc_ag_meta_settlement_2026.txt',
     'agent_note': 'Addresses U8: names the revenue motive and builds the remedy around the competitive incentive (stronger '
                   'limits only if rivals adopt them). A settlement, not an adjudicated finding.'},
    {'id': 'f2:33',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Office of the Attorney General for the District of Columbia (Meta multistate settlement)',
     'version': '2026-08-26',
     'url': 'https://oag.dc.gov/release/attorney-general-schwalb-announces-meta-will-pay',
     'quote': ['Meta will adopt a combined two-hour daily time limit with mandatory pauses after 15 minutes of continuous use '
               'and again at 60 and 90 minutes to interrupt endless scrolling.',
               'Regular assessment by an independent auditor of the implementation and efficacy of the safety features'],
     'raw_file': 'attn/f2/dc_ag_meta_settlement_2026.txt',
     'agent_note': 'Imposed countermeasures, DEFAULT and hard-capped for children (not opt-in); efficacy is to be audited '
                   'later, so no effect evidence yet.'},
    {'id': 'f2:34',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Meta and State AGs\' [Proposed] Consent Judgment, Exhibit 1, In re Social Media Adolescent Addiction '
               '(N.D. Cal. No. 4:23-cv-05448-YGR), Doc. 572-1',
     'version': 'filed 2026-08-26 (130 pp.)',
     'url': 'https://coag.gov/app/uploads/2026/08/01-Exhibit-1-MDL-Consent-Judgment-FINAL-Settlment-Agreement-Fully-Executed.pdf',
     'quote': ['Meta must implement productive pauses and notices as described herein designed to reduce or prevent '
               'excessive, mindless, or unintended teen usage.',
               'Meta shall provide the Independent Auditor with data on the efficacy of the productive pauses and notices',
               'Meta, however, retains discretion to determine the changes to be made.'],
     'raw_file': 'attn/f2/meta_consent_judgment_2026.txt',
     'agent_note': 'Court-filed obligations: pauses are defaults, loosened only by a supervising parent; efficacy data go '
                   'to an auditor but Meta keeps discretion over changes. The ranking objective itself is not regulated '
                   'here. No effect evidence yet.'},
    {'id': 'f2:35',
     'tag': 'U8',
     'reading': 'addresses',
     'source': 'Meta and State AGs\' [Proposed] Consent Judgment, Exhibit 1 (N.D. Cal. No. 4:23-cv-05448-YGR, Doc. 572-1)',
     'version': 'filed 2026-08-26',
     'url': 'https://coag.gov/app/uploads/2026/08/01-Exhibit-1-MDL-Consent-Judgment-FINAL-Settlment-Agreement-Fully-Executed.pdf',
     'quote': ['“Industry-Wide Adoption” shall mean, with respect to any Contingent Time Management Obligation as it applies '
               'to any Settling State, the period during which all Core Industry Members and any New SMP Entrant '
               'following its New SMP Effective Date have:'],
     'raw_file': 'attn/f2/meta_consent_judgment_2026.txt',
     'agent_note': 'Addresses U8: the stricter time-management obligations are contingent on all core rivals adopting '
                   'equivalent ones (by settlement, law or audited voluntary action), a coordination device against '
                   'the competitive cost of limiting use.'},
    {'id': 'f2:36',
     'tag': 'U2',
     'reading': 'bears',
     'source': 'Meta and State AGs\' [Proposed] Consent Judgment, Exhibit 1 (N.D. Cal. No. 4:23-cv-05448-YGR, Doc. 572-1)',
     'version': 'filed 2026-08-26',
     'url': 'https://coag.gov/app/uploads/2026/08/01-Exhibit-1-MDL-Consent-Judgment-FINAL-Settlment-Agreement-Fully-Executed.pdf',
     'quote': ['Meta SMPs shall not recommend or otherwise suggest that the Teen User utilize a different Meta SMP or engage '
               'in messaging or the watching of Longform Content',
               'From 10 p.m. to 7 a.m., based on the device’s local time zone, Meta SMPs shall disable push notifications '
               'for Teen Users, unless modified by a Supervising Parent.'],
     'raw_file': 'attn/f2/meta_consent_judgment_2026.txt',
     'agent_note': 'Bears on U2: the decree forbids redirecting a capped teen to other Meta surfaces and silences night '
                   'notifications, i.e. it anticipates re-engagement at the stop. No statement of why the platform would '
                   'redirect.'},
    {'id': 'f2:37',
     'tag': 'U1',
     'reading': 'close',
     'source': 'SECONDARY: NPR, "Jury holds Meta and Google liable for role in young woman\'s mental health issues" '
               '(K.G.M. v. Meta et al., Los Angeles Superior Court, JCCP 5255 bellwether)',
     'version': '2026-03-25',
     'url': 'https://www.npr.org/2026/03/25/nx-s1-5746125/meta-youtube-social-media-trial-verdict',
     'quote': ['KGM\'s legal team showed the jury internal documents from Meta in which CEO Mark Zuckerberg and other '
               'executives described the company\'s efforts to attract and keep kids and teens on its platforms.',
               'Another internal memo showed that 11-year-olds were four times as likely to keep coming back to Instagram, '
               'compared with competing apps'],
     'raw_file': 'attn/f2/npr_kgm_verdict_2026.txt',
     'agent_note': 'Close to U1 (reported trial evidence): internal documents track and value users coming back. '
                   'Difference: reported second-hand; not the ranking objective itself. Court records not fetched.'},
    {'id': 'f2:38',
     'tag': 'U2',
     'reading': 'close',
     'source': 'SECONDARY: NPR report on the K.G.M. verdict (2026-03-25)',
     'version': '2026-03-25',
     'url': 'https://www.npr.org/2026/03/25/nx-s1-5746125/meta-youtube-social-media-trial-verdict',
     'quote': ["Meta's apps, including Instagram, and Google's YouTube, the jury concluded, were deliberately built to be "
               'addictive and the companies\' executives knew this and failed to protect their youngest users.',
               'They argued that features like infinite scroll, constant notifications, autoplaying videos and beauty '
               'filters made apps like Instagram and YouTube equivalent to a "digital casino,"'],
     'raw_file': 'attn/f2/npr_kgm_verdict_2026.txt',
     'agent_note': 'Close to U2: a jury finding of deliberately addictive design, with notifications and autoplay argued. '
                   'Difference: the objective-to-feature link is the plaintiff\'s argument; defendants vowed to appeal.'},
    {'id': 'f2:39',
     'tag': 'U4',
     'reading': 'bears',
     'source': 'SECONDARY: NPR report on the K.G.M. verdict (2026-03-25), quoting Mark Zuckerberg\'s testimony',
     'version': '2026-03-25',
     'url': 'https://www.npr.org/2026/03/25/nx-s1-5746125/meta-youtube-social-media-trial-verdict',
     'quote': ['"If people feel like they\'re not having a good experience, why would they keep using the product?"'],
     'raw_file': 'attn/f2/npr_kgm_verdict_2026.txt',
     'agent_note': 'Bears on U4 as the counter-position: continued use (return) is read as evidence of a good experience, '
                   'i.e. revealed preference, the view the "true map" rejects.'},
    # ---------------------------------------------------------------- company objective statements
    {'id': 'f2:40',
     'tag': 'U4',
     'reading': 'close',
     'source': 'YouTube Official Blog, "On YouTube\'s recommendation system" (Cristos Goodrow)',
     'version': '2021-09-15',
     'url': 'https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/',
     'quote': ['We don’t want viewers regretting the videos they spend time watching and realized we needed to do even more '
               'to measure how much value you get from your time on YouTube.',
               'we measure what we call “valued watchtime”—the time spent watching a video that you consider valuable.'],
     'raw_file': 'attn/f2/yt_recsys_blog.txt',
     'agent_note': 'Close to U4: a company states it optimises survey-stated satisfaction (valued watchtime) to avoid '
                   'regret. Difference: the value is still weighted by time watched and predicted by a model; nothing on '
                   'how the pause or return is represented.'},
    {'id': 'f2:41',
     'tag': 'U5',
     'reading': 'close',
     'source': 'YouTube Official Blog, "On YouTube\'s recommendation system" (Cristos Goodrow)',
     'version': '2021-09-15',
     'url': 'https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/',
     'quote': ['Only videos that you rate highly with four or five stars are counted as valued watchtime.',
               'Based on the responses we do get, we’ve trained a machine learning model to predict potential survey '
               'responses for everyone.'],
     'raw_file': 'attn/f2/yt_recsys_blog.txt',
     'agent_note': "Close to U5 on one half: time actually spent watching (the user's own active steps) counted only "
                   'when stated as valuable. Difference: nothing says the valuation has no term on return; whether it is '
                   'aggregated per calendar day is not stated; clicks, watchtime, shares etc. remain signals; the pause is '
                   'not discussed.'},
    {'id': 'f2:42',
     'tag': 'U8',
     'reading': 'addresses',
     'source': 'YouTube Official Blog, "On YouTube\'s recommendation system" (Cristos Goodrow)',
     'version': '2021-09-15',
     'url': 'https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/',
     'quote': ['When we first incorporated watchtime into recommendations, we saw an immediate 20% drop in views. But we '
               'believed that it was more important for us to deliver more value to viewers.',
               'Responsibility is good for business.'],
     'raw_file': 'attn/f2/yt_recsys_blog.txt',
     'agent_note': 'Addresses U8 from the company side: a short-run engagement cost accepted and a claim that '
                   'responsibility and business align (about borderline content and views, not about pauses).'},
    # ---------------------------------------------------------------- notifications audit (NGO)
    {'id': 'f2:43',
     'tag': 'U2',
     'reading': 'states',
     'source': 'Bits of Freedom (C. Mohanlal), "How Snapchat\'s notifications manipulate users"',
     'version': '2025-11-24',
     'url': 'https://www.bitsoffreedom.nl/wp-content/uploads/2025/12/20251124-report-snapchats_manipulating_notifications.pdf',
     'quote': ['We received the most notifications in the condition where we did not open Snapchat and did not follow any '
               'other accounts.',
               'In the conditions in which we opened the app four times per day (Con3 & Con6), there were significantly '
               'fewer push notifications (15; 14%) than in the conditions in which we did not open the app (Con1 & Con4) '
               '(57; 52%)',
               'these notifications are not there to meet user needs, but'],
     'raw_file': 'attn/f2/bof_snapchat_notifications_2025.txt',
     'agent_note': 'States U2 empirically for one VLOP: push volume rose with the user\'s absence (the most pushes to an '
                   'account never opened). A six-week audit of six test accounts (109 notifications) plus 13 interviews; '
                   'a small sample, by an NGO arguing a DSA Art. 25 breach.'},
    {'id': 'f2:44',
     'tag': 'U7',
     'reading': 'bears',
     'source': 'Bits of Freedom, "How Snapchat\'s notifications manipulate users"',
     'version': '2025-11-24',
     'url': 'https://www.bitsoffreedom.nl/wp-content/uploads/2025/12/20251124-report-snapchats_manipulating_notifications.pdf',
     'quote': ['We recommend that notifications be disabled by default and that users be able to indicate which ones they '
               'want to receive per category.',
               'But users do not specifically turn off these notifications; they find notification settings within the app '
               'too complicated and too much hassle.'],
     'raw_file': 'attn/f2/bof_snapchat_notifications_2025.txt',
     'agent_note': 'Bears on U7: recommended-content notifications are on by default and the opt-out goes unused because '
                   'settings are a hassle, so default matters. Interview evidence (N=13), not a usage study.'},
]
