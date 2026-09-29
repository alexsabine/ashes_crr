# Attention algorithms — family F2: company practice and regulation (sweep of 2026-09-28)

- **Date:** 2026-09-28 (all fetches on this day).
- **Purpose:** Attention_Algorithms DECLARATION, prompt-log 231, family F2 (company practice and regulation for recommender
  feeds: YouTube, Instagram/Facebook, TikTok, Snapchat; EU, UK, US-state, Australian and US federal instruments; litigation).
- **Who:** agent-fetched (the F2 literature agent). Every source was fetched by the agent on the day; raw texts are saved in
  the session scratchpad under `attn/f2/` and are not committed (third-party texts).
- **Window:** 2019-01-01 to 2026-09-28. **Budget:** at most 25 sources; 25 included.
- **Claims:** 45 claims, 91 verbatim quotes, transcribed into
  `Attention_Algorithms/checks/claims_f2.py`. Each quote was checked as an exact substring of its saved raw text after
  whitespace collapsing (html-unescape, soft hyphens removed, '-\n' joins removed): 91 of 91 found.
- **Readings** are the investigator's (states / close / bears for U1-U5 and U7; addresses / bears for U8). "Not found" is
  never read as novel. Litigation items are allegations, settlements or a jury verdict under appeal, and are labelled so.

## 1. Tally of claims by tag and reading

| tag | reading | claims |
|---|---|---|
| U1 | bears | 1 |
| U1 | close | 1 |
| U1 | states | 1 |
| U2 | bears | 3 |
| U2 | close | 5 |
| U2 | states | 3 |
| U3 | close | 1 |
| U4 | bears | 2 |
| U4 | close | 3 |
| U5 | close | 1 |
| U7 | bears | 14 |
| U7 | close | 2 |
| U8 | addresses | 4 |
| U8 | bears | 4 |


## 2. Search log

One WebSearch per declared query (queries grouped by the declaration's F2 topics; extra searches were run where the first
did not reach a primary text, and are logged too). Every hit is listed with the screening decision. I = included (fetched,
quoted); F = fetched but not included; X = excluded. Hits that repeat an earlier row are marked "dup".

**Q1. `YouTube "take a break" reminder bedtime reminder help`**
| hit | decision | reason |
|---|---|---|
| howtogeek.com, "These Obscure Features Will Help You Stop Watching YouTube" | X | secondary how-to; primary help pages found |
| fastcompany.com, "YouTube now has a bedtime reminder" | X | secondary news (2020); primary available |
| thenextweb.com, "YouTube now tells you to go to bed" | X | secondary news |
| support.google.com/youtube/answer/9012523, "Take a break reminder - Android" | I | primary help page (S01) |
| engadget.com, "YouTube can tell you to stop watching and go to sleep" | X | secondary news |
| support.google.com/youtube/answer/9884905, "Set a bedtime reminder - Android" | I | primary help page (S02) |
| YouTube Help Community thread 48055830 | X | community forum, not an official statement |
| youtube.com video "How to Set or Turn Off Take a Break Reminders" | X | third-party video |
| phonearena.com, "YouTube tries to be your mom" | X | secondary news |
| techcrunch.com (2018-05-11), "youtube rolls out new tools" | X | before the window; secondary |

**Q2. `Instagram Teen Accounts sleep mode time limit reminders Quiet Mode`**
| hit | decision | reason |
|---|---|---|
| about.instagram.com, "Teen Accounts" blog | X | duplicate of the Meta newsroom post (same text family); newsroom version used |
| about.fb.com/news/2024/09/instagram-teen-accounts/ | I | primary company announcement (S03) |
| familycenter.meta.com, "Protect Teens on Instagram" | X | overlapping product page; newsroom posts carry dated statements |
| screenagersmovie.com blog | X | commentary |
| parentmap.com | X | secondary |
| about.fb.com/news/2023/01/instagram-quiet-mode-... | I | primary company announcement (S04) |
| techxplore.com (AP tech tip) | X | secondary |
| help.instagram.com/455298907304715, "Manage your Teen Account settings" | X | help page; newsroom states the same defaults with dates |
| screenwiseapp.com guide | X | third-party guide |
| nexspy.com blog | X | commercial third party |

**Q3. `TikTok 60-minute daily screen time limit teens wind down feature`**
| hit | decision | reason |
|---|---|---|
| thedrum.com | X | secondary |
| newsroom.tiktok.com, "New ways we're supporting parents..." (2025-03-11) | I | primary (S06) |
| routenote.com blog | X | secondary |
| variety.com (2023) | X | secondary |
| newsroom.tiktok.com, "New features for teens and families on TikTok" (2023-03-01) | I | primary (S05) |
| techcrunch.com (2023-03-01) | X | secondary |
| allsides.com | X | aggregator |
| goodreads.com blog copy | X | copy of a news item |
| axios.com (2023-03-01) | X | secondary |
| gulfnews.com | X | secondary |

**Q4. `Apple Screen Time Google Digital Wellbeing app timers bedtime mode`**
| hit | decision | reason |
|---|---|---|
| aura.com | X | commercial third party |
| yahoo.com lifestyle article | X | secondary |
| internetmatters.org Digital Wellbeing guide | X | third-party guide |
| macworld.com comparison | X | secondary |
| popsci.com | X | secondary |
| support.google.com/android/answer/9346420 | I | primary OS help page (S07) |
| play.google.com Digital Wellbeing listing | X | store listing, no statements beyond S07 |
| thetest.com guide | X | third party |
| tech.yahoo.com | X | secondary |
| techcrunch.com/?p=1996666 | X | secondary |
Note: no Apple primary page was fetched (budget of 25; the OS-level, opt-in tool class is represented by S07). Not a finding about Apple.

**Q5. `European Commission preliminary findings TikTok addictive design Digital Services Act`**
| hit | decision | reason |
|---|---|---|
| epthinktank.eu, "Addictive design on online platforms" (2026-05-06) | X | EP research briefing (secondary synthesis); primaries used |
| amnesty.org (2026-02) | X | NGO statement |
| blogs.lse.ac.uk Media@LSE (2026-03-04) | X | commentary |
| business-humanrights.org | X | aggregator |
| computerweekly.com | X | secondary |
| digital-strategy.ec.europa.eu news item (TikTok) | F | fetched; same text as the press corner release, which was used |
| schjodt.com | X | law-firm commentary |
| ec.europa.eu/commission/presscorner IP/26/312 | I | primary (S08; text via the press corner API) |
| matheson.com | X | law-firm commentary |
| servulo.com | X | law-firm commentary |

**Q6. `Commission opens formal proceedings Meta Facebook Instagram protection of minors addictive design rabbit hole DSA`**
| hit | decision | reason |
|---|---|---|
| scl.org | X | secondary |
| socialmediatoday.com | X | secondary |
| ec.europa.eu presscorner IP/24/2664 (opening, 2024-05-16) | F | fetched and saved; excluded as superseded by the 2026 preliminary findings (budget) |
| euronews.com (2026-07-10) | X | secondary |
| digital-strategy.ec.europa.eu news item (Meta) | F | fetched; same text as IP/26/1579 |
| ec.europa.eu presscorner IP/26/1579 | I | primary (S09) |
| techtimes.com | X | secondary |
| theregister.com (2024-05-16) | X | secondary |
| phonearena.com | X | secondary |

**Q7. `Digital Services Act Regulation (EU) 2022/2065 Article 25 Article 38 recommender system not based on profiling eur-lex`**
| hit | decision | reason |
|---|---|---|
| mozillafoundation.org blog | X | commentary |
| dsa-observatory.eu (2025-05-19) | X | commentary |
| techpolicy.press | X | commentary |
| fpf.org | X | commentary |
| arxiv.org/pdf/2503.05764 | X | academic (F1/F3 scope), not regulation text |
| ceur-ws.org Vol-3898 | X | academic |
| blog.galalaw.com | X | commentary |
| arxiv.org/pdf/2403.18623 | X | off topic |
| arxiv.org/pdf/2309.10776 | X | off topic |
| dsa-observatory.eu (2024-11-22) | X | commentary |
The act itself (S10) was fetched directly: EUR-Lex HTML/PDF/ELI returned HTTP 202 (bot wall) five times; the text was
fetched from the Publications Office Cellar (`publications.europa.eu/resource/celex/32022R2065`, xhtml).

**Q8. `Commission guidelines protection of minors Article 28 DSA 2025 addictive design streaks notifications`**
| hit | decision | reason |
|---|---|---|
| epthinktank.eu (dup) | X | dup, secondary |
| dev.to | X | blog |
| taylorwessing.com | X | law-firm commentary |
| freshfields.com | X | law-firm commentary |
| digital-strategy.ec.europa.eu library, "Commission publishes guidelines on the protection of minors" | I | landing page; the linked document (redirection/document/118226) is S11 |
| merlin.obs.coe.int | X | secondary |
| insideprivacy.com | X | law-firm commentary |
| interface-eu.org | X | think-tank |
| hlc.com | X | law-firm commentary |
| edpb.europa.eu ECPAT response | X | stakeholder submission |

**Q9. `Digital Fairness Act public consultation addictive design European Commission 2025`**
| hit | decision | reason |
|---|---|---|
| en.wikipedia.org, "Digital Fairness Act" | X | tertiary |
| europarl.europa.eu Legislative Train | X | secondary summary |
| osborneclarke.com | X | law-firm commentary |
| digital-strategy.ec.europa.eu consultation page | I | primary (S12) |
| digitalfairnessact.com (4 pages) | X | unofficial tracker site |
| digital-fairness-act.com | X | unofficial tracker site |
| youth.europa.eu (ro) | X | duplicate announcement, Romanian |
Note: the consultation questionnaire (where the Commission lists infinite scroll, autoplay, streak penalties and
engagement-steered recommenders, per search summaries) was not fetched; only the announcement is quoted.

**Q10. `ICO Age Appropriate Design Code standard nudge techniques detrimental use of data`**
| hit | decision | reason |
|---|---|---|
| esrb.org blog | X | commentary |
| ico.org.uk "Code standards" | F | fetched (index page only); standard 5 page used instead |
| privacylaws.com PDF copy of the code | X | third-party copy; ICO page used |
| gdprlocal.com | X | commentary |
| hausfeld.com | X | commentary |
| ico.org.uk code landing page | X | index |
| ico.org.uk "13. Nudge techniques" | X | about privacy nudges, less relevant than standard 5 (budget) |
| ico.org.uk audit toolkit, nudge techniques | X | audit toolkit |
| palindrometech.com | X | commentary |
The standard 5 page (S13) was fetched by direct URL.

**Q11. `Ofcom Protection of Children Codes Online Safety Act recommender feeds July 2025`**
| hit | decision | reason |
|---|---|---|
| taylorwessing.com | X | law-firm commentary |
| lewissilkin.com | X | law-firm commentary |
| whitecase.com | X | law-firm commentary |
| reedsmith.com | X | law-firm commentary |
| ofcom.org.uk, "New rules for a safer generation of children online" | X | fetch returned HTTP 403 (Cloudflare challenge); no primary text |
| techuk.org | X | trade body |
| ofcom.org.uk additional safety measures consultation | X | not fetched (same host blocked) |
| lexology.com | X | commentary |
| bristows.com | X | commentary |
UK Online Safety Act: no primary text included (Ofcom blocked). The UK is represented by the ICO code (S13).

**Q12. `New York SAFE for Kids Act addictive feeds attorney general proposed rules notifications midnight 6 am`**
| hit | decision | reason |
|---|---|---|
| mychamplainvalley.com | X | secondary |
| ag.ny.gov press release 2026 (final rules) | I | primary (S14) |
| hunton.com | X | law-firm commentary |
| governor.ny.gov | X | same announcement; AG release used |
| news10.com | X | secondary |
| fingerlakes1.com | X | secondary |
| tribuneindia.com (2 URLs) | X | secondary |
| ag.ny.gov "Protecting Children Online" | X | index page |
| barchart.com | X | secondary |

**Q13. `California SB 976 ... Ninth Circuit`**
| hit | decision | reason |
|---|---|---|
| courthousenews.com | X | secondary (injunction reporting) |
| en.wikipedia.org | X | tertiary |
| hunton.com | X | commentary |
| natlawreview.com | X | commentary |
| leginfo.legislature.ca.gov SB-976 bill text | I | primary, chaptered (S15) |
| legiscan.com | X | mirror of an amended version |
| calmatters digitaldemocracy | X | secondary |
| alstonprivacy.com | X | commentary |
| tagteam.harvard.edu | X | aggregator |
The Ninth Circuit opinion (NetChoice v. Bonta, 2025-09-09) was not fetched; its status is reported from search summaries only.

**Q14. `Australia Online Safety Amendment (Social Media Minimum Age) Act 2024 eSafety December 10 2025`**
| hit | decision | reason |
|---|---|---|
| quinnemanuel.com | X | commentary |
| peo.gov.au | X | education summary |
| minterellison.com | X | commentary |
| en.wikipedia.org | X | tertiary |
| esafety.gov.au media release | X | fetch returned HTTP 403 |
| legislation.gov.au C2024A00127/asmade | I | primary; the HTML is script-rendered, the authorised PDF was fetched (S16) |
| en.wikipedia.org Online Safety Act | X | tertiary |
| privacymatters.dlapiper.com | X | commentary |
| aph.gov.au bill page | X | HTTP 403 |

**Q15. `Surgeon General advisory social media and youth mental health 2023 pdf design features maximize engagement`** (two result lists returned)
| hit | decision | reason |
|---|---|---|
| hhs.gov sg-youth-mental-health-social-media-advisory.pdf | X | HTTP 403 (Akamai) by curl and WebFetch; Wayback tunnel closed by proxy |
| ncbi.nlm.nih.gov/books/NBK594757 | X | reCAPTCHA wall |
| arxiv.org/pdf/2410.16137 | X | off topic |
| researchgate.net | X | not the advisory |
| medrxiv.org | X | off topic |
| chconline.org | X | copy site |
| pubmed 37721985 | X | abstract only (Europe PMC also abstract only) |
| hhs.gov (hi-IN) | X | dup, 403 |
| integrationacademy.ahrq.gov | X | secondary |
| hhs.gov summary PDF | X | 403 |
| pmc PMC12967810 | X | F3 scope (review of effects) |
| hhs.gov advisory PDF | X | dup, 403 |
| psychologytoday.com | X | commentary |
| public-health.uiowa.edu | X | commentary |
| behavioralhealthnews.org | X | commentary |
| arxiv.org/pdf/2409.02358 | X | F1/F3 scope |
| hhs.gov surgeon general social media page | X | 403 |
| ncbi PMC10028523 | X | off topic |
| kidsandteenspc.com | X | commentary |

**Q16. `social media addiction trial verdict 2026 Meta YouTube jury Los Angeles JCCP`**
| hit | decision | reason |
|---|---|---|
| cnbc.com (2026-03-25) | X | secondary; NPR report used |
| npr.org (2026-03-25) | I | SECONDARY reputable report (S22); court records not reachable |
| abc7.com | X | secondary |
| nighgoldenberg.com | X | plaintiff law-firm marketing |
| spencer-law.com | X | law-firm marketing |
| mdlupdate.com JCCP 5255 | X | unofficial tracker |
| mdlupdate.com MDL 3047 | X | unofficial tracker |
| foxnews.com live updates | X | secondary |
| aljazeera.com | X | secondary |

**Q17. `attorneys general Meta settlement 2026 youth social media addiction design changes multistate`**
| hit | decision | reason |
|---|---|---|
| portal.ct.gov press release | X | same settlement; DC release used |
| edsource.org | X | secondary |
| publichealth.jhu.edu | X | commentary |
| oag.dc.gov release | I | primary (S19) |
| variety.com | X | secondary |
| sec.gov Meta 10-Q (2026-06-30) | X | not fetched (budget); would bear on U8 (financial exposure) |
| npr.org (2026-08-26) | X | secondary |
| sec.gov Meta 10-Q (2026-03-31) | X | not fetched |
| cnbc.com (2026-08-26) | X | secondary |

**Q18. `multistate attorneys general complaint Meta October 2023 unredacted complaint pdf ...`**
| hit | decision | reason |
|---|---|---|
| oag.dc.gov release | I | dup of S19 |
| oag.maryland.gov 102423.pdf | X | same announcement; Colorado (lead state) used |
| michigan.gov press release | X | same announcement |
| coag.gov Exhibit 1 MDL Consent Judgment PDF | I | primary court filing (S20) |
| coag.gov press release (2023-10-24) | I | primary (S21), lead state |
| sec.gov Meta 10-Q FY2023 (3 items) and 10-K tables | X | financial tables, not relevant |
| ag.ny.gov (2023) | X | same announcement |

**Q19. `"design features that attempt to maximize time, attention, and engagement" Surgeon General`**
| hit | decision | reason |
|---|---|---|
| chiefhealthcareexecutive.com | I | SECONDARY report quoting the 2023 advisory (S17); primary 403 |
| hhs.gov advisory PDF | X | dup, 403 |
| socialmediamdl.com | X | plaintiff marketing site |
| bhr.stern.nyu.edu | X | commentary |
| cnn.com (2026-05-20) new advisory | I | SECONDARY report of the 2026 advisory (S18); primary on hhs.gov not reachable |
| arxiv.org/html/2411.12083v1, "Extended-Use Designs on Very Large Online Platforms" | X | academic, F1 scope (passed to F1 by name only) |
| arxiv.org/pdf/2405.06478 | X | academic |
| link.springer.com | X | off topic |
| arxiv.org/pdf/2605.31146 | X | off topic |

**Q20. `"sg-youth-mental-health-social-media-advisory.pdf"`** (mirror search)
| hit | decision | reason |
|---|---|---|
| scribd.com copy | X | login wall, unverifiable copy |
| hhs.gov PDF | X | dup, 403 |
| youthvillages.org | X | secondary |
| lumatehealth.com | X | secondary |
| pubmed 37721985 | X | dup, abstract only |
| ncbi NBK594761 | X | reCAPTCHA (curl and WebFetch) |
| bhavanalearning.com PDF of the HHS press release | X | HTTP 202 empty body |
| hhs.gov (hi-IN) | X | dup |
| hhs.gov expert quotes PDF | X | 403 host |

**Q21. `YouTube blog "On YouTube's recommendation system" valued watchtime satisfaction surveys`** (company statements on objectives)
| hit | decision | reason |
|---|---|---|
| blog.youtube "On YouTube's recommendation system" | I | primary (S23) |
| recommender-systems.com | X | repost |
| arxiv.org/html/2501.15048v1 | X | academic, F1 scope |
| hi.shopify.com | X | commercial |
| youtube.googleblog.com 2019 "Continuing our work to improve recommendations" (tracking link) | X | tracking-wrapped link; S23 covers the objective statements |
| scribd.com (2 items) | X | unverifiable copies |
| deccanherald.com | X | secondary |
| sundayscaries.substack.com | X | blog |

**Q22. `evaluation effectiveness "take a break" reminders time limit nudges social media randomized study usage reduction`**
| hit | decision | reason |
|---|---|---|
| pmc PMC13062480 / mhealth.jmir.org / sciencedirect (Wellspent RCT, 2026) | X | JMIR fetch returned HTTP 202 (bot wall); third-party app, F3 scope; passed to F3 by name |
| diva-portal.org thesis | X | thesis, F3 scope |
| mhealth.jmir.org PDF | X | dup |
| frontiersin.org (activity breaks) | X | off topic |
| ncbi PMC10740995 (digital detox) | X | F3 scope |
| researchgate.net (digital nudges RCT) | X | F3 scope |
| econtent.hogrefe.com (Instagram interruption pilot RCT) | X | F3 scope, paywalled |
| ncbi PMC11758673 | X | F3 scope |
No platform-published evaluation of break reminders or time limits was found in this family beyond the uptake and
retention figures in S05, S06 and S25, and the regulators' findings in S08, S09.

**Q23. `push notifications re-engagement social media teens regulator default off statement 2025 Snapchat streaks notifications`**
| hit | decision | reason |
|---|---|---|
| internetmatters.org Snapchat guide | X | third-party guide |
| bitsoffreedom.nl report PDF (2025-11-24) | I | NGO audit of notification practice (S24) |
| snapchat.com topic page | X | marketing page |
| atraxialaw.com | X | law-firm marketing |
| safer.deeper.org.in | X | blog |
| braze.com push best practices | X | vendor marketing; would bear on U2 but not a platform statement |
| newsroom.snap.com | X | index page |
| cbc.ca (2019) | X | secondary |
| axios.com (2024-02-07) | X | secondary |

**Q24. `Meta Teen Accounts "97%" teens stayed in built-in protections 2025 newsroom`**
| hit | decision | reason |
|---|---|---|
| about.fb.com/news/2025/04/introducing-new-built-in-restrictions-... | I | primary (S25) |
| about.fb.com/news/2025/04/meta-parents-new-technology-enroll-teens | X | age-detection topic (budget) |
| meta.com/safety/teen-safety-lawsuits | X | litigation position page; not fetched (budget) |
| meta.com/safety/teen | X | index |
| foxnews.com | X | secondary |
| scarymommy.com | X | secondary |
| annarborfamily.com | X | secondary |
| about.fb.com/news/2025/07/expanding-teen-account-protections | X | child-safety DMs topic |
| cyberguy.com | X | secondary |
| techcrunch.com (2025-04-08) | X | secondary |

**Totals.** 24 searches, 238 hit rows screened (including duplicates); 25 sources included (22 primary, 3 SECONDARY reports
used because the primary was blocked); 4 further texts fetched and not included (IP/24/2664, kept in the
scratchpad; the two digital-strategy duplicates and the ICO index page, discarded). Blocked on the day: hhs.gov (403), NCBI Bookshelf (reCAPTCHA),
ofcom.org.uk (403), esafety.gov.au (403), aph.gov.au (403), EUR-Lex HTML (202, bot wall), JMIR (202), web.archive.org
(tunnel closed by the proxy).

## 3. Sources and claims

### S01. YouTube Help, "Take a break reminder" (Android)
- **Publisher:** Google / YouTube (help centre)
- **Kind:** company help page
- **Date / version as shown:** help page as served 2026-09-28 (no date shown)
- **URL:** https://support.google.com/youtube/answer/9012523?hl=en&co=GENIE.Platform%3DAndroid
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/yt_take_a_break.txt` (session scratchpad)

**f2:0** — tag **U7**, reading **bears**

> The take a break reminder lets you set a reminder to take a break while watching videos. The reminder will pause your video until you dismiss it or resume playing the video.

> Note: For users aged 13–17 on YouTube, the take a break reminder is set to “On” by default. For users 18 or over, the default setting is “Off.”

> If you close the app, sign out, switch devices, or pause a video for more than 30 minutes, the timer will reset.

*Note:* Default ON for 13-17, opt-in (default OFF) for adults; dismissible by the user. A countermeasure beside the recommender, not a change to its objective. No effect evidence given.

### S02. YouTube Help, "Set a bedtime reminder" (Android)
- **Publisher:** Google / YouTube (help centre)
- **Kind:** company help page
- **Date / version as shown:** help page as served 2026-09-28 (no date shown)
- **URL:** https://support.google.com/youtube/answer/9884905?hl=en&co=GENIE.Platform%3DAndroid
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/yt_bedtime.txt` (session scratchpad)

**f2:1** — tag **U7**, reading **bears**

> Note: For users aged 13-17 on YouTube, the bedtime reminder is set to On by default. For users 18 or over, the default setting is Off.

> When your bedtime reminder goes off, you can dismiss it by tapping in the top-right corner, or you can tap Remind Me Again to get another reminder in 15 minutes.

*Note:* Default ON for 13-17, opt-in for adults; a dismissible/snoozable reminder. No effect evidence given.

### S03. Meta Newsroom, "Introducing Instagram Teen Accounts: Built-In Protections for Teens, Peace of Mind for Parents"
- **Publisher:** Meta Platforms (newsroom)
- **Kind:** company announcement
- **Date / version as shown:** published 2024-09-17, page shows update 2025-10-22
- **URL:** https://about.fb.com/news/2024/09/instagram-teen-accounts/
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/ig_teen_accounts.txt` (session scratchpad)

**f2:2** — tag **U7**, reading **bears**

> These protections are turned on automatically, and parents decide if teens under 16 can change any of these settings to be less strict:

> Time limit reminders: Teens will get notifications telling them to leave the app after 60 minutes each day.

> Sleep mode enabled: Sleep mode will be turned on between 10 PM and 7 AM, which will mute notifications overnight and send auto-replies to DMs.

*Note:* Default ON for teens (under-16s need parental permission to loosen). The 60-minute item is a reminder, not a cap; hard daily limits exist only as an opt-in parental supervision setting. No effect evidence in this post.

**f2:3** — tag **U4**, reading **bears**

> Teen Accounts will limit who can contact teens and the content they see, and help ensure their time is well spent.

> Teens will also get access to a new feature, made just for them, that lets them select topics they want to see more of in Explore and their recommendations

*Note:* Bears on U4 only: 'time well spent' is a product goal and stated topic choice is an input to recommendations; the ranking objective is not said to be the teen's stated or reflective value.

### S04. Meta Newsroom, "Instagram Quiet Mode: A New Way to Manage Your Time and Focus"
- **Publisher:** Meta Platforms (newsroom)
- **Kind:** company announcement
- **Date / version as shown:** published 2023-01-19, page shows update 2025-09-04 (renamed Sleep mode)
- **URL:** https://about.fb.com/news/2023/01/instagram-quiet-mode-manage-your-time-and-focus/
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/ig_quiet_mode.txt` (session scratchpad)

**f2:4** — tag **U7**, reading **bears**

> Anyone can use Quiet mode, but we’ll prompt teens to do so when they spend a specific amount of time on Instagram late at night.

> once the feature is turned off, we’ll show you a quick summary of notifications so you can catch up on what you missed.

*Note:* Opt-in at launch (teens prompted); since 2024 on by default for teens as Sleep mode (f2:2). The post-pause notification summary releases what the pause held back. No effect evidence.

### S05. TikTok Newsroom, "New features for teens and families on TikTok" (Cormac Keenan)
- **Publisher:** TikTok (newsroom)
- **Kind:** company announcement
- **Date / version as shown:** 2023-03-01
- **URL:** https://newsroom.tiktok.com/en-us/new-features-for-teens-and-families-on-tiktok-us
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/tiktok_2023_limits.txt` (session scratchpad)

**f2:5** — tag **U7**, reading **bears**

> In the coming weeks, every account belonging to a user below age 18 will automatically be set to a 60-minute daily screen time limit.

> If the 60-minute limit is reached, teens will be prompted to enter a passcode in order to continue watching, requiring them to make an active decision to extend that time.

> So we're also prompting teens to set a daily screen time limit if they opt out of the 60-minute default and spend more than 100 minutes on TikTok in a day.

> our tests found this helped increase the use of our screen time tools by 234%.

*Note:* Default ON for under-18s but self-overridable by passcode (teens can opt out). The only effect figure is uptake of the tools (+234%), not reduced use or wellbeing.

### S06. TikTok Newsroom, "New ways we're supporting parents and helping teens build balanced digital habits" (Adam Presser)
- **Publisher:** TikTok (newsroom)
- **Kind:** company announcement
- **Date / version as shown:** 2025-03-11
- **URL:** https://newsroom.tiktok.com/en-us/new-ways-we-are-supporting-parents-and-helping-teens-build-balanced-digital-habits
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/tiktok_2025_winddown.txt` (session scratchpad)

**f2:6** — tag **U7**, reading **bears**

> If a teen under 16 is on TikTok after 10pm, their For You feed will be interrupted with our new wind down feature.

> If a teen decides to spend additional time on TikTok after the first reminder, we show a second, harder to dismiss, full-screen prompt. As before, we deliberately do not send push notifications to teens at night, which cannot be changed.

> In countries where this has already been piloted, the vast majority of teens decide to keep this reminder on.

*Note:* Wind-down default for under-16s; night push notifications off for teens and not changeable (a default that removes a night re-engagement channel). Effect evidence is only that most teens keep the reminder on, not that use falls.

### S07. Android Help, "Manage how you spend time on your Android phone with Digital Wellbeing"
- **Publisher:** Google (Android help centre)
- **Kind:** OS vendor help page
- **Date / version as shown:** help page as served 2026-09-28 (no date shown)
- **URL:** https://support.google.com/android/answer/9346420?hl=en
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/android_dw.txt` (session scratchpad)

**f2:7** — tag **U7**, reading **bears**

> For example, you can set app timers and schedule display changes.

> Choose which apps you want to pause. When Focus mode is on, you can't use these apps and won't get notifications from them.

> To use the app again before midnight, follow steps 1–4 above and delete the app timer.

*Note:* OS-level, opt-in tools outside any platform objective; the user can delete a timer to continue. No effect evidence given.

### S08. European Commission press release IP/26/312, "Commission preliminarily finds TikTok's addictive design in breach of the Digital Services Act"
- **Publisher:** European Commission (press corner)
- **Kind:** regulator press release
- **Date / version as shown:** 2026-02-06
- **URL:** https://ec.europa.eu/commission/presscorner/detail/en/ip_26_312
- **Fetch status (2026-09-28):** OK (HTTP 200, press corner JSON API; HTML page is script-rendered)
- **Raw text:** `attn/f2/ec_tiktok_prelim_2026.txt` (session scratchpad)

**f2:9** — tag **U2**, reading **close**

> This includes features such as infinite scroll, autoplay, push notifications, and its highly personalised recommender system.

> by constantly ‘rewarding' users with new content, certain design features of TikTok fuel the urge to keep scrolling and shift the brain of users into ‘autopilot mode'.

*Note:* Close to U2: names push notifications, autoplay, infinite scroll and the personalised recommender as addictive design. Difference: it does not attribute them to an objective that values the user's return. Preliminary finding.

**f2:10** — tag **U1**, reading **bears**

> TikTok disregarded important indicators of compulsive use of the app, such as the time that minors spend on TikTok at night, the frequency with which users open the app, and other potential indicators.

*Note:* Bears on U1: the frequency of opening the app (returns) is read by the regulator as a compulsion indicator; it says nothing about the objective valuing returns.

**f2:11** — tag **U7**, reading **close**

> The time management tools do not seem to be effective in enabling users to reduce and control their use of TikTok because they are easy to dismiss and introduce limited friction.

> TikTok needs to change the basic design of its service. For instance, by disabling key addictive features such as ‘infinite scroll' over time, implementing effective ‘screen time breaks', including during the night, and adapting its recommender system.

*Note:* Close to U7: a regulator finds the tools ineffective (easy to dismiss) and asks for change to the basic design including the recommender. Difference: it does not say the tools are opt-in, nor frame the failure as the objective's stake left intact. Preliminary; effect evidence (internal data) not published.

### S09. European Commission press release IP/26/1579, "Commission preliminarily finds the addictive design of Instagram and Facebook in breach of the Digital Services Act"
- **Publisher:** European Commission (press corner)
- **Kind:** regulator press release
- **Date / version as shown:** 2026-07-10
- **URL:** https://ec.europa.eu/commission/presscorner/detail/en/ip_26_1579
- **Fetch status (2026-09-28):** OK (HTTP 200, press corner JSON API)
- **Raw text:** `attn/f2/ec_meta_prelim_2026.txt` (session scratchpad)

**f2:12** — tag **U7**, reading **close**

> Instagram's and Facebook's time management tools, including those activated by default for teens, can be easily dismissed and do not lead to a meaningful reduction and control of the usage of the service.

*Note:* Close to U7 (weak effect), and notable: even the DEFAULT-on teen tools are found ineffective, so "mostly opt-in" is not the whole reason. Difference: no statement about the objective's stake. Preliminary finding.

**f2:13** — tag **U4**, reading **close**

> disabling key addictive features such as 'autoplay' and ‘infinite scroll' by default, implementing effective ‘screen time breaks', and adapting its recommender system to make it less engagement-oriented.

*Note:* Close to U4: the regulator asks for a less engagement-oriented recommender. Difference: it names no replacement objective (stated or reflective value) and nothing about how the pause is represented.

**f2:14** — tag **U2**, reading **close**

> Meta did not consider certain design features of Instagram and Facebook, such as highly personalised recommendations, autoplay and infinite scroll, which constantly show users new content.

> how the optimisation of its different formats - such as reels and stories - could lead to excessive or compulsive use of the services.

*Note:* Close to U2: optimisation of formats is linked to excessive use, and features with no stopping point are named. Difference: re-engagement after a pause (notifications timed to absence) is not singled out; the link to a return-valuing objective is not drawn.

### S10. Regulation (EU) 2022/2065 (Digital Services Act), recital 83 and Article 34(1)
- **Publisher:** EU (Official Journal; Publications Office Cellar)
- **Kind:** legislation
- **Date / version as shown:** OJ L 277, 27.10.2022 (original act; Cellar xhtml, EUR-Lex HTML bot-walled)
- **URL:** https://eur-lex.europa.eu/eli/reg/2022/2065/oj
- **Fetch status (2026-09-28):** OK via Cellar (HTTP 200); EUR-Lex HTML/PDF/ELI returned HTTP 202 bot wall
- **Raw text:** `attn/f2/dsa_text.txt` (session scratchpad)

**f2:15** — tag **U2**, reading **bears**

> or from online interface design that may stimulate behavioural addictions of recipients of the service.

> serious negative consequences to the person’s physical and mental well-being.

*Note:* Bears on U2: the DSA names interface design that may stimulate behavioural addiction as a systemic risk VLOPs must assess (Art. 34). No mechanism (objective, return) is stated.

**f2:16** — tag **U7**, reading **bears**

> shall provide at least one option for each of their recommender systems which is not based on profiling as defined in Article 4, point (4), of Regulation (EU) 2016/679.

> Providers of online platforms shall not design, organise or operate their online interfaces in a way that deceives or manipulates the recipients of their service or in a way that otherwise materially distorts or impairs the ability of the recipients of their service to make free and informed decisions.

*Note:* The Art. 38 non-profiling option is a mandated alternative the user must choose (opt-in); the profiled feed stays the default. No effect evidence in the text.

### S11. European Commission, Guidelines on measures to ensure a high level of privacy, safety and security for minors online, pursuant to Article 28(4) DSA, C(2025) 6826 final
- **Publisher:** European Commission
- **Kind:** regulator guidelines (non-binding)
- **Date / version as shown:** document dated Brussels, 7.10.2025 (as served by the Commission library link; guidelines announced 2025-07-14 per search summaries, not verified)
- **URL:** https://ec.europa.eu/newsroom/dae/redirection/document/118226
- **Fetch status (2026-09-28):** OK (HTTP 200, PDF; text extracted with pypdf, some intra-word spaces from extraction)
- **Raw text:** `attn/f2/ec_minors_guidelines_2025.txt` (session scratchpad)

**f2:17** — tag **U2**, reading **states**

> Ensuring that minors are not exposed to persuasive design features that are aimed predominantly at engagement and that may lead to extensive use or overuse of the platform or problematic or compulsive behavioural habits.

> artificially timed to regain minors’ attention

*Note:* States U2 for minors: design aimed at engagement, including notifications timed to regain attention (re-engagement after absence), infinite scroll and autoplay. Not legally binding; used by the Commission to assess Art. 28(1).

**f2:18** — tag **U7**, reading **bears**

> vi. the default autoplay of videos and hosting live streams are turned off.

> vii. push notifications are turned off by default and are always off during core

> To be effective, these tools should deter minors from spending more time on the platform.

*Note:* Regulator asks that the countermeasures be DEFAULTS for minors (autoplay off, push off, off in sleep hours) and that time tools be judged by whether they deter use. No effect evidence.

**f2:19** — tag **U4**, reading **close**

> Prioritise ‘explicit user-provided signals’ to determine the content displayed and recommended to minors.

> including the stated and deliberative selection of topics of interest, surveys, reporting

*Note:* Close to U4: stated, deliberative preferences are to be prioritised over implicit engagement signals (time spent, click-through). Difference: these are input signals, not the optimised objective; the pause is not addressed.

### S12. European Commission, "Commission launches open consultation on the forthcoming Digital Fairness Act"
- **Publisher:** European Commission (DG CNECT page)
- **Kind:** consultation announcement
- **Date / version as shown:** published 2025-07-17 (consultation open 2025-07-17 to 2025-10-24; page last update 2025-08-04)
- **URL:** https://digital-strategy.ec.europa.eu/en/consultations/commission-launches-open-consultation-forthcoming-digital-fairness-act
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/dfa_consultation.txt` (session scratchpad)

**f2:20** — tag **U8**, reading **bears**

> addictive design of digital products and unfair personalisation practices, especially where consumer vulnerabilities are exploited for commercial purposes.

*Note:* Bears on U8: addictive design is linked to commercial exploitation and slated for consumer law. The consultation questionnaire itself was not fetched.

### S13. ICO, Age appropriate design: a code of practice for online services, standard 5 "Detrimental use of data"
- **Publisher:** UK Information Commissioner's Office
- **Kind:** statutory code of practice
- **Date / version as shown:** web page as served 2026-09-28 (no page date shown)
- **URL:** https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/childrens-information/childrens-code-guidance-and-resources/age-appropriate-design-a-code-of-practice-for-online-services/5-detrimental-use-of-data/
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/ico_aadc_detrimental.txt` (session scratchpad)

**f2:21** — tag **U2**, reading **close**

> Strategies used to extend user engagement, sometimes referred to as ‘sticky’ features can include mechanisms such as reward loops, continuous scrolling, notifications and auto-play features which encourage users to continue playing a game, watching video content or otherwise staying online.

> avoid features which use personal data to automatically extend use instead of requiring children to make an active choice about whether they want to spend their time in this way (data-driven autoplay features)

*Note:* Close to U2: engagement-extension strategies named (notifications, autoplay, continuous scroll). Difference: framed as extending a session, not as re-engagement driven by a stake in the user's return.

**f2:22** — tag **U3**, reading **close**

> in a way that makes it easy for them to disengage without feeling pressurised or disadvantaged if they do so.

> present options to continue playing or otherwise engaging with your service neutrally without suggesting that children will lose out if they don’t;

> introduce mechanisms such as pause buttons which allow children to take a break at any time without losing their progress in a game

*Note:* Close to U3 from the user's side: a pause that costs the child nothing and neutral framing of continuing. Difference: the ICO removes the loss to the USER at the pause; U3 removes the pause's content in the SERVICE's valuation (its incentive). No objective is specified.

### S14. New York Attorney General press release, "Attorney General James and Governor Hochul Release Final SAFE for Kids Act Rules to Protect Children Online"
- **Publisher:** Office of the New York State Attorney General
- **Kind:** regulator press release (rules)
- **Date / version as shown:** 2026-07-28 (rules to be published in the State Register 2026-07-29; Act effective 2027-01-25)
- **URL:** https://ag.ny.gov/press-release/2026/attorney-general-james-and-governor-hochul-release-final-safe-kids-act-rules
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/ny_ag_final_rules_2026.txt` (session scratchpad)

**f2:23** — tag **U1**, reading **states**

> Algorithmically personalized feeds, or addictive feeds, recommend or personalize content for users in an endless stream based on data that the platform gathers about the user. They are designed to encourage a user to continue to use and return to a platform.

*Note:* States U1 as a regulator's description: the feed's design aim includes the user's return. It does not use objective/loss language; it is a descriptive characterisation, not evidence of a specific company's objective.

**f2:24** — tag **U8**, reading **bears**

> Instead of the default algorithmically personalized feeds designed to keep young people on the platform, users under 18 will only be shown content from other accounts they follow or otherwise select in a set sequence, such as chronological order, unless they get parental consent for an addictive feed.

> The law also prohibits social media platforms from sending notifications to users under 18 from 12 a.m. to 6 a.m. without parental consent.

> kids' safety should come before Big Tech’s profits

*Note:* Bears on U8: regulation flips the DEFAULT for minors (chronological feed, no night notifications) and a sponsor names the safety/profit conflict; the incentive mechanism itself is not analysed.

### S15. California SB 976, Protecting Our Kids from Social Media Addiction Act (Stats. 2024, ch. 321)
- **Publisher:** California Legislature (leginfo)
- **Kind:** legislation
- **Date / version as shown:** Chaptered, approved by Governor 2024-09-20
- **URL:** https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=202320240SB976
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/ca_sb976.txt` (session scratchpad)

**f2:25** — tag **U2**, reading **bears**

> However, some social media platforms have evolved to include addictive features, including the algorithmic delivery of content and other design features, that pose a significant risk of harm to the mental health and well-being of children and adolescents.

*Note:* Legislative finding; bears on U2 (algorithmic delivery as an addictive feature). Litigation status (NetChoice v. Bonta; Ninth Circuit 2025-09-09 upheld the feed provisions, parts enjoined) is from search summaries only, not fetched.

**f2:26** — tag **U8**, reading **addresses**

> This setting shall be set by the operator as on by default, in a manner in which the child’s access is limited to one hour per day unless modified by the verified parent.

> the operator of an addictive internet-based service or application shall not withhold, degrade, lower the quality of, or increase the price of, any product, service, or feature, other than as required by this chapter, due to a user or parent availing themselves of the rights provided by this chapter

*Note:* Addresses U8: the statute anticipates the operator's incentive to penalise users who opt out and forbids it, and makes the time limit a default. (Default-on status of these parental controls may be affected by the litigation; not verified here.)

### S16. Online Safety Amendment (Social Media Minimum Age) Act 2024 (Cth), No. 127, 2024
- **Publisher:** Australian Government, Federal Register of Legislation
- **Kind:** legislation
- **Date / version as shown:** Authorised Version C2024A00127 registered 12/12/2024 (as made)
- **URL:** https://www.legislation.gov.au/C2024A00127/asmade/2024-12-10/text/original/pdf
- **Fetch status (2026-09-28):** OK (HTTP 200, authorised PDF; HTML text view script-rendered)
- **Raw text:** `attn/f2/au_min_age_act_2024.txt` (session scratchpad)

**f2:27** — tag **U8**, reading **bears**

> The object of this Part is to reduce the risk of harm to age-restricted users from certain kinds of social media platforms.

> A provider of an age-restricted social media platform must take reasonable steps to prevent age-restricted users having accounts with the age-restricted social media platform.

*Note:* Bears on U8: the regulatory route chosen here excludes under-16s rather than changing the objective; nothing about incentives or design. (Commencement 2025-12-10 is from search summaries.)

### S17. SECONDARY: Chief Healthcare Executive, "Surgeon General warns social media poses risks to kids, and health groups back him up", quoting the 2023 U.S. Surgeon General's Advisory (hhs.gov PDF returned 403)
- **Publisher:** Chief Healthcare Executive (MJH Life Sciences)
- **Kind:** SECONDARY news report quoting the 2023 Surgeon General advisory
- **Date / version as shown:** report on the advisory of 2023-05-23; report date not shown in the saved text
- **URL:** https://www.chiefhealthcareexecutive.com/view/surgeon-general-warns-social-media-poses-risks-to-kids-and-health-groups-back-him-up
- **Fetch status (2026-09-28):** OK (HTTP 200); primary hhs.gov 403
- **Raw text:** `attn/f2/che_sg_advisory_2023_report.txt` (session scratchpad)

**f2:28** — tag **U2**, reading **close**

> The advisory also suggests companies should “avoid design features that attempt to maximize time, attention, and engagement.”

> And for too many children, social media use is compromising their sleep and valuable in-person time with family and friends,

*Note:* Close to U2 (via a report quoting the advisory): design features that maximise time and engagement. Difference: no statement about returns or re-engagement after absence. Primary blocked (HTTP 403 on hhs.gov; NCBI Bookshelf reCAPTCHA).

### S18. SECONDARY: CNN, "New surgeon general's advisory raises alarm about screen time risks for kids and teens", reporting the 2026 HHS/Surgeon General advisory on screen time (primary not fetched: hhs.gov 403)
- **Publisher:** CNN
- **Kind:** SECONDARY news report on the 2026 HHS/Surgeon General advisory
- **Date / version as shown:** 2026-05-20
- **URL:** https://www.cnn.com/2026/05/20/health/surgeon-general-advisory-screen-time-wellness
- **Fetch status (2026-09-28):** OK (HTTP 200); primary hhs.gov 403
- **Raw text:** `attn/f2/cnn_sg_advisory_2026.txt` (session scratchpad)

**f2:29** — tag **U7**, reading **bears**

> Tech companies display warnings about harmful screen use and adhere to and enforce age minimums.

> nearly half of adolescents admit that they lose track of the amount of time they spend on their phones.

*Note:* As reported, the 2026 advisory asks companies for warnings and age minimums, i.e. more countermeasures beside the objective. No effect evidence reported.

### S19. Office of the Attorney General for the District of Columbia, "Attorney General Schwalb Announces That Meta Will Pay Up to $17.1 Billion for Exploiting Kids with Intentionally Addictive Social Media Platforms"
- **Publisher:** Office of the Attorney General for the District of Columbia
- **Kind:** regulator press release (settlement)
- **Date / version as shown:** 2026-08-26
- **URL:** https://oag.dc.gov/release/attorney-general-schwalb-announces-meta-will-pay
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/dc_ag_meta_settlement_2026.txt` (session scratchpad)

**f2:32** — tag **U8**, reading **addresses**

> This bipartisan, nationwide investigation found that Meta, with the goal of driving ever-increasing advertising revenue, designed Facebook and Instagram’s features to addict children

> Meta will pay an additional $5 billion—increasingly the total settlement amount to $17.1 billion—and enhance the new safety features it is implementing if and when other major social media companies also agree to adopt these features.

*Note:* Addresses U8: names the revenue motive and builds the remedy around the competitive incentive (stronger limits only if rivals adopt them). A settlement, not an adjudicated finding.

**f2:33** — tag **U7**, reading **bears**

> Meta will adopt a combined two-hour daily time limit with mandatory pauses after 15 minutes of continuous use and again at 60 and 90 minutes to interrupt endless scrolling.

> Regular assessment by an independent auditor of the implementation and efficacy of the safety features

*Note:* Imposed countermeasures, DEFAULT and hard-capped for children (not opt-in); efficacy is to be audited later, so no effect evidence yet.

### S20. Meta and State AGs' [Proposed] Consent Judgment, Exhibit 1, In re Social Media Adolescent Addiction (N.D. Cal. No. 4:23-cv-05448-YGR), Doc. 572-1
- **Publisher:** U.S. District Court, N.D. Cal. filing (hosted by the Colorado AG)
- **Kind:** court document
- **Date / version as shown:** filed 2026-08-26 (130 pp.)
- **URL:** https://coag.gov/app/uploads/2026/08/01-Exhibit-1-MDL-Consent-Judgment-FINAL-Settlment-Agreement-Fully-Executed.pdf
- **Fetch status (2026-09-28):** OK (HTTP 200, PDF, 130 pp.; pypdf extraction, line numbers interleaved)
- **Raw text:** `attn/f2/meta_consent_judgment_2026.txt` (session scratchpad)

**f2:34** — tag **U7**, reading **bears**

> Meta must implement productive pauses and notices as described herein designed to reduce or prevent excessive, mindless, or unintended teen usage.

> Meta shall provide the Independent Auditor with data on the efficacy of the productive pauses and notices

> Meta, however, retains discretion to determine the changes to be made.

*Note:* Court-filed obligations: pauses are defaults, loosened only by a supervising parent; efficacy data go to an auditor but Meta keeps discretion over changes. The ranking objective itself is not regulated here. No effect evidence yet.

**f2:35** — tag **U8**, reading **addresses**

> “Industry-Wide Adoption” shall mean, with respect to any Contingent Time Management Obligation as it applies to any Settling State, the period during which all Core Industry Members and any New SMP Entrant following its New SMP Effective Date have:

*Note:* Addresses U8: the stricter time-management obligations are contingent on all core rivals adopting equivalent ones (by settlement, law or audited voluntary action), a coordination device against the competitive cost of limiting use.

**f2:36** — tag **U2**, reading **bears**

> Meta SMPs shall not recommend or otherwise suggest that the Teen User utilize a different Meta SMP or engage in messaging or the watching of Longform Content

> From 10 p.m. to 7 a.m., based on the device’s local time zone, Meta SMPs shall disable push notifications for Teen Users, unless modified by a Supervising Parent.

*Note:* Bears on U2: the decree forbids redirecting a capped teen to other Meta surfaces and silences night notifications, i.e. it anticipates re-engagement at the stop. No statement of why the platform would redirect.

### S21. Colorado Attorney General press release, "Bipartisan coalition of attorneys general file lawsuits against Meta for harming youth mental health through its social media platforms"
- **Publisher:** Colorado Attorney General
- **Kind:** regulator press release (complaint)
- **Date / version as shown:** 2023-10-24
- **URL:** https://coag.gov/press-releases/bipartisan-coalition-of-attorneys-general-file-lawsuits-against-meta-for-harming-youth-mental-health-through-its-social-media-platforms/
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/coag_meta_complaint_2023.txt` (session scratchpad)

**f2:30** — tag **U2**, reading **states**

> Its platform algorithms push users into descending “rabbit holes” in an effort to maximize engagement. Features like infinite scroll and near-constant alerts were created with the express goal of hooking young users. These manipulative tactics continually lure children and teens back onto the platform.

*Note:* States U2 as an ALLEGATION (complaint summary): alerts and infinite scroll built to maximise engagement and to bring young users back. Allegation, not a finding.

**f2:31** — tag **U8**, reading **bears**

> Meta chose to maximize its profits at the expense of public health

*Note:* Bears on U8: the profit/health conflict is asserted (an AG statement), not analysed.

### S22. SECONDARY: NPR, "Jury holds Meta and Google liable for role in young woman's mental health issues" (K.G.M. v. Meta et al., Los Angeles Superior Court, JCCP 5255 bellwether)
- **Publisher:** NPR
- **Kind:** SECONDARY news report of a jury verdict
- **Date / version as shown:** 2026-03-25
- **URL:** https://www.npr.org/2026/03/25/nx-s1-5746125/meta-youtube-social-media-trial-verdict
- **Fetch status (2026-09-28):** OK (HTTP 200); court records not reachable
- **Raw text:** `attn/f2/npr_kgm_verdict_2026.txt` (session scratchpad)

**f2:37** — tag **U1**, reading **close**

> KGM's legal team showed the jury internal documents from Meta in which CEO Mark Zuckerberg and other executives described the company's efforts to attract and keep kids and teens on its platforms.

> Another internal memo showed that 11-year-olds were four times as likely to keep coming back to Instagram, compared with competing apps

*Note:* Close to U1 (reported trial evidence): internal documents track and value users coming back. Difference: reported second-hand; not the ranking objective itself. Court records not fetched.

**f2:38** — tag **U2**, reading **close**

> Meta's apps, including Instagram, and Google's YouTube, the jury concluded, were deliberately built to be addictive and the companies' executives knew this and failed to protect their youngest users.

> They argued that features like infinite scroll, constant notifications, autoplaying videos and beauty filters made apps like Instagram and YouTube equivalent to a "digital casino,"

*Note:* Close to U2: a jury finding of deliberately addictive design, with notifications and autoplay argued. Difference: the objective-to-feature link is the plaintiff's argument; defendants vowed to appeal.

**f2:39** — tag **U4**, reading **bears**

> "If people feel like they're not having a good experience, why would they keep using the product?"

*Note:* Bears on U4 as the counter-position: continued use (return) is read as evidence of a good experience, i.e. revealed preference, the view the "true map" rejects.

### S23. YouTube Official Blog, "On YouTube's recommendation system" (Cristos Goodrow)
- **Publisher:** YouTube Official Blog
- **Kind:** company statement on objectives
- **Date / version as shown:** 2021-09-15
- **URL:** https://blog.youtube/inside-youtube/on-youtubes-recommendation-system/
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/yt_recsys_blog.txt` (session scratchpad)

**f2:40** — tag **U4**, reading **close**

> We don’t want viewers regretting the videos they spend time watching and realized we needed to do even more to measure how much value you get from your time on YouTube.

> we measure what we call “valued watchtime”—the time spent watching a video that you consider valuable.

*Note:* Close to U4: a company states it optimises survey-stated satisfaction (valued watchtime) to avoid regret. Difference: the value is still weighted by time watched and predicted by a model; nothing on how the pause or return is represented.

**f2:41** — tag **U5**, reading **close**

> Only videos that you rate highly with four or five stars are counted as valued watchtime.

> Based on the responses we do get, we’ve trained a machine learning model to predict potential survey responses for everyone.

*Note:* Close to U5 on one half: time actually spent watching (the user's own active steps) counted only when stated as valuable. Difference: nothing says the valuation has no term on return; whether it is aggregated per calendar day is not stated; clicks, watchtime, shares etc. remain signals; the pause is not discussed.

**f2:42** — tag **U8**, reading **addresses**

> When we first incorporated watchtime into recommendations, we saw an immediate 20% drop in views. But we believed that it was more important for us to deliver more value to viewers.

> Responsibility is good for business.

*Note:* Addresses U8 from the company side: a short-run engagement cost accepted and a claim that responsibility and business align (about borderline content and views, not about pauses).

### S24. Bits of Freedom (C. Mohanlal), "How Snapchat's notifications manipulate users"
- **Publisher:** Bits of Freedom (Dutch digital-rights NGO)
- **Kind:** NGO audit report
- **Date / version as shown:** 2025-11-24
- **URL:** https://www.bitsoffreedom.nl/wp-content/uploads/2025/12/20251124-report-snapchats_manipulating_notifications.pdf
- **Fetch status (2026-09-28):** OK (HTTP 200, PDF; some words run together in extraction)
- **Raw text:** `attn/f2/bof_snapchat_notifications_2025.txt` (session scratchpad)

**f2:43** — tag **U2**, reading **states**

> We received the most notifications in the condition where we did not open Snapchat and did not follow any other accounts.

> In the conditions in which we opened the app four times per day (Con3 & Con6), there were significantly fewer push notifications (15; 14%) than in the conditions in which we did not open the app (Con1 & Con4) (57; 52%)

> these notifications are not there to meet user needs, but

*Note:* States U2 empirically for one VLOP: push volume rose with the user's absence (the most pushes to an account never opened). A six-week audit of six test accounts (109 notifications) plus 13 interviews; a small sample, by an NGO arguing a DSA Art. 25 breach.

**f2:44** — tag **U7**, reading **bears**

> We recommend that notifications be disabled by default and that users be able to indicate which ones they want to receive per category.

> But users do not specifically turn off these notifications; they find notification settings within the app too complicated and too much hassle.

*Note:* Bears on U7: recommended-content notifications are on by default and the opt-out goes unused because settings are a hassle, so default matters. Interview evidence (N=13), not a usage study.

### S25. Meta Newsroom, "We're Introducing New Built-In Restrictions for Instagram Teen Accounts, and Expanding to Facebook and Messenger"
- **Publisher:** Meta Platforms (newsroom)
- **Kind:** company announcement
- **Date / version as shown:** published 2025-04-08, page shows update 2025-07-09
- **URL:** https://about.fb.com/news/2025/04/introducing-new-built-in-restrictions-instagram-teen-accounts-expanding-facebook-messenger/
- **Fetch status (2026-09-28):** OK (HTTP 200, curl)
- **Raw text:** `attn/f2/meta_teen_accounts_2025_04.txt` (session scratchpad)

**f2:8** — tag **U7**, reading **bears**

> Since making these changes, 97% of teens aged 13-15 have stayed in these built-in restrictions, which we believe offer the most age-appropriate experience for younger teens.

> They also have notifications turned off overnight and reminders to leave the app after 60 minutes

*Note:* Company-reported default retention (97% of 13-15s; loosening needs parental permission). This is evidence that defaults stick, not that reminders reduce use or improve wellbeing.

