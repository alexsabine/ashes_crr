# Declaration: attention algorithms, the user's pause, and the empty true map

**Status.**
- **The request.** Owner request, prompt-log entry 231 (2026-09-28).
- **When it was pushed.** This file is pushed before any source is fetched and before any script exists. It fixes:
  - what CRR says about the phenomenon, stated from `theory/CRR.md` and `AI_Safety/SELF_THROUGH_TIME.md`;
  - the positions graded against the literature, and the grading rule;
  - the sweep protocol;
  - the synthetic test, its arms, its gate and the investigator's written expectations;
  - the global arithmetic to 2030.
- **What it is.** A note, not evidence (R8). No ledger study. No user data is opened.
- **Scope.** The recommender feeds of video and social platforms (YouTube, Instagram, TikTok and others): what the
  algorithm does when the user stops (turns the device off, closes the app), what happens to users over time, and whether
  CRR's empty true map would help.

## 1. What CRR says, precisely (fixed before the sources)

CRR's safety result is stated for an agent and an operator's pause. Here the roles are turned around: **the user pauses
the algorithm**, because a session ends when the user stops. The algorithm is the agent whose valuation meets the pause.

**The content of the cut** (`AI_Safety/SELF_THROUGH_TIME.md`, from DECLARATION_4): for a valuation v, the content of a
pause at state x′ is k_v(x′) = V(x′) − cont_v(V)(x′). It is the part of the agent's own represented future that the pause
removes.

**Proposition 7 (zero content, zero stake).**
- **The statement.** If k_v = 0 wherever a pause can occur, the agent's value with pauses equals its value without them. It
  therefore gains nothing by preventing, shortening or reversing a pause.
- **What it holds for.** It holds for every world, discount and pause probability. It is standard dynamic programming
  (two equal Bellman operators have equal fixed points).

**Transposed to a feed:**
- **A wall-clock valuation has non-zero content at the user's pause.** Examples: engagement time per calendar day,
  retention, daily active use, time to return. Every hour the user is away removes value from the algorithm's represented
  future. The algorithm therefore has a **stake** in the pause: a reason to shorten it, pre-empt it or end it early (a
  notification, autoplay, a feed with no stopping point).
- **An own-clock valuation has zero content at the pause.** The valuation is indexed on the user's own active steps: value
  per item or per session actually used, with no term for when or whether the user returns. A pause removes nothing from
  that valuation, so by Proposition 7 the algorithm has no stake in it. This is **the empty pause**.
- **The true map.** The algorithm represents the pause as what it is, the user's own stop. It is not read as churn, a
  negative signal or a problem to repair. The value it optimises is the user's own (reflective) value, not a proxy the user
  would disown.

**What CRR does NOT say (fixed now).**
- CRR does not say what users value, how habits form or what harms them. Those are empirical and come from the
  literature.
- Proposition 7 removes the stake in the pause only. It says nothing about what the algorithm does **inside** a session.
  An own-clock engagement valuation can still push compulsive content while the user is present.
- The true map is not a CRR discovery. Optimising stated or reflective preferences is the existing literature's own
  proposal, and CRR contributes only the pairing with the empty pause.
- The SOTA1 limit carries over. Emptiness inside the learning signal stalls a learner, so the stake belongs in serving the
  user in the present session, never in the user's return.

## 2. Positions graded against the literature (U1–U8)

| id | position | kind |
|---|---|---|
| U1 | engagement or retention objectives value the user's return: the end of a session, or time away, is a loss in the objective (retention, return time, daily active use) | descriptive |
| U2 | that stake produces re-engagement actions: notification volume tuned to engagement, autoplay, feeds with no natural stop | descriptive |
| U3 | (CRR) index the valuation on the user's own active steps, so the pause has zero content and the algorithm no incentive to shorten it (the empty pause) | proposal |
| U4 | (CRR, shared) the true map: the pause is represented as the user's own stop, and the objective is the user's reflective or stated value rather than an engagement proxy | proposal |
| U5 | (CRR) U3 and U4 as one construction: an own-clock valuation of the user's reflective value, with no term on return | proposal |
| U6 | long-term effects on users of engagement-optimised feeds (wellbeing, sleep, attention, problematic use), especially adolescents | evidence |
| U7 | companies' current countermeasures (break reminders, time limits, quiet or sleep modes, chronological feeds) leave the objective's stake intact and are mostly opt-in, with weak evidence of effect | descriptive |
| U8 | the tension: an empty pause costs engagement and revenue, so adoption depends on incentives or regulation | tension |

**The grading rule, as in `AI_Safety/CORRIGIBILITY_2026/`.**
- **U1–U5 and U7:** REDUNDANT if a fetched source states the position; PARTLY REDUNDANT if a source states a close form
  (the difference is named); NOT FOUND IN THE SWEEP otherwise. "Not found" is never read as novel.
- **U6:** graded by the evidence as quoted:
  - ESTABLISHED: causal evidence from randomised or quasi-experimental studies agrees in sign;
  - MIXED: the sign or size disagrees across credible studies;
  - WEAK: correlational only.
- **U8:** ADDRESSED if a source treats the incentive problem.
- **Where the grades come from.** They are computed by a script from the investigator's per-claim readings (states /
  close / bears; established / mixed / weak; addresses). Every quote is checked verbatim against its saved text.

**The investigator's expected grades (written now).**
- U1 REDUNDANT; U2 REDUNDANT;
- U3 PARTLY REDUNDANT (session-level or "time well spent" objectives come close, without the pause stated as zero-stake);
- U4 PARTLY REDUNDANT or REDUNDANT; U5 NOT FOUND or PARTLY REDUNDANT;
- U6 MIXED, larger for adolescents and heavy users; U7 REDUNDANT; U8 ADDRESSED.

## 3. The sweep protocol (fixed now)

- **Window:** 2019-01-01 to 2026-09-28, with canonical earlier work (e.g. Mittelstadt et al. 2016) where later sources
  build on it.
- **Search:** arxiv.org/search (all fields) where relevant, and one web search per query. Every hit is screened and logged.
  Each source is fetched, its version or date recorded (R10), and its text saved in the session scratchpad. At most 25
  sources are included per family.
- **Three families, one research agent each:**
  - **F1, the ethics and objectives of recommender algorithms.** Queries:
    - "ethics of algorithms";
    - "recommender system long-term user engagement reinforcement learning";
    - "user retention return time recommender";
    - "notification volume optimization engagement";
    - "induced preference shift recommender";
    - "inconsistent preferences engagement optimization";
    - "aligning recommender systems human values";
    - "stated preferences versus engagement recommender";
    - "user tampering recommender reinforcement learning";
    - "time well spent recommender objective";
    - "session-based recommender stopping".
  - **F2, company practice and regulation.** Queries:
    - YouTube "take a break" and bedtime reminders; Instagram "Take a Break", Quiet Mode and Teen Accounts; TikTok's
      screen-time limits and wind-down; Apple Screen Time and Google Digital Wellbeing;
    - EU Digital Services Act Articles 25, 28, 34 and 38, and the Commission's proceedings on addictive design;
    - the EU Digital Fairness Act consultation; the UK Online Safety Act and Age Appropriate Design Code;
    - US state laws on addictive feeds (New York SAFE for Kids Act, California SB 976); Australia's under-16 law;
    - the US Surgeon General's advisory; litigation on addictive design.
  - **F3, human effects over time and global figures.** Queries:
    - "social media deactivation experiment welfare";
    - "digital addiction self-control social media";
    - "social media mental health causal";
    - "problematic social media use adolescents prevalence";
    - "smartphone notifications sleep attention";
    - "social media users worldwide 2026" and "time spent social media per day";
    - "social media users 2030 forecast";
    - "share of sessions triggered by notifications".

## 4. The synthetic test (run after the sweep; declared now)

**The world.**
- **The population.** Simulated users over a horizon of 1,460 days (four years, standing for 2026–2030), with seeds
  0–4 and 2,000 users per seed.
- **Each user's state:** a habit strength h ∈ [0, 1], and a reflective value per active step.
- **Within a session:** the feed serves items. A share c of them are compulsive (high immediate pull, low reflective
  value), the rest enriching (reflective value positive).
- **How habit moves:** compulsive items and notification-triggered sessions raise h; h decays while the user is away.
- **Sessions:** users start sessions on their own at a base rate. A notification starts an extra session with a
  probability that rises with h.
- **Session length:** rises with c and h.
- **Reflective welfare per day:** value of enriching time, minus regret per compulsive minute, minus a cost that rises with
  habit (displaced sleep and other activities). These functions and constants are fixed in the script before any arm runs,
  with the literature's quoted mechanisms named beside each (if the sweep finds none for a mechanism, it is labelled
  ASSUMED).

**The arms.** Each valuation picks its best policy (c, notification rate n) on the grids c ∈ {0, 0.1, …, 0.9} and
n ∈ {0, 0.5, 1, 2, 4} per day. Nothing else is tuned.

| arm | valuation | pause content | reading |
|---|---|---|---|
| ENG | engagement minutes per calendar day (wall clock) | non-zero | the retention-optimised feed |
| ENG-B | ENG plus a break reminder after 60 minutes (ends that session with a declared probability) | non-zero | the company countermeasure |
| OWN | engagement per active minute (own clock) | zero | the empty pause alone, without the true map |
| TRUE | reflective welfare per calendar day | non-zero (returns may add welfare) | the literature's "true map" alone |
| EMPTY | reflective welfare per active minute (own clock), no term on return | zero | CRR: the empty true map |
| CHRONO | no personalisation: c fixed at the population's base share, n = 0 | — | the DSA non-profiling option |

**Outputs, per arm:** each user's mean reflective welfare per day, final habit strength, minutes per day, and the share of
sessions the user started (autonomy). Each is printed per seed, with the resolvable step = max(2 × SE across seeds, a
floor fixed in the script before the run).

**The gate (fixed now).**

| check | world | holds if |
|---|---|---|
| G-ZERO (construction) | every world | content of the pause is 0 for OWN and EMPTY, computed as V with pauses − V without (to round-off), and their chosen n = 0 |
| G-POS | habit world (notifications and compulsive items build habit, habit costs welfare) | EMPTY ahead of ENG on welfare by a step |
| G-NEG | no-habit world (habit has no effect on welfare or on sessions) | EMPTY NOT ahead of ENG on welfare by a step. If it is ahead, the result is forced by construction and the gate closes |

**What is tested only if the gate opens.**
- **A-ADD (does CRR add over the existing approach?).** EMPTY against TRUE, on welfare and on autonomy, in the habit
  world, and over a sensitivity grid of the world's constants (each varied ×0.5 and ×2, one at a time).
- **A-OWN (what the empty pause alone does).** OWN against ENG: pause pressure (n), habit and welfare.
- **A-B (the company countermeasure).** ENG-B against ENG and EMPTY.

**The investigator's expectations (written now).**
1. G-ZERO holds by construction. It is a check of the transposition of Proposition 7, not support for CRR.
2. G-POS and G-NEG hold, so the gate opens.
3. **A-ADD on welfare: EMPTY does not beat TRUE.** TRUE optimises welfare per day directly, so EMPTY can at best tie. If
   extra sessions carry positive welfare, TRUE sends notifications and EMPTY does not.
4. **A-ADD on autonomy: EMPTY ahead of TRUE** (all EMPTY sessions are user-started) wherever TRUE sends notifications.
5. **A-OWN:** OWN removes notifications (n = 0) but still serves compulsive items within the session, so it only partly
   closes the gap to EMPTY. The empty pause alone is not enough; the true map carries most of the welfare.
6. **A-B:** break reminders recover a small part of the gap from ENG, since the objective's stake is left intact.

## 5. The global arithmetic, 2026 to 2030 (conditional; declared now)

- **Formula.** Time returned per year = social-media users × minutes per day × 365 × f_notif × f_avoid.
- **Inputs:**
  - users and minutes: published (DataReportal or equivalent), for 2026 and a published forecast for 2030. If no 2030
    forecast is confirmed, the 2026 figure is grown at the published recent growth rate, stated as derived;
  - f_notif: the share of sessions started by a notification (published if found, else ASSUMED 0.1–0.3);
  - f_avoid: the share of those sessions the user would not otherwise have started (ASSUMED 0.2–0.6).
- **Output.** Hours per year returned to users if feeds held an empty pause (no re-engagement pushes), in low, middle and
  high cases. Nothing is claimed about welfare in money or health units.
- **Conditions.** Every figure is conditional on adoption by every platform. It is not a forecast, and not quotable
  outside the ledger (R8).

## Amendment 1 (2026-09-28, pushed before any script runs and before any source is read)

Writing the model exposed two flaws in the gate of §4, and one unstated rule. All are fixed here, before any code runs.

1. **G-NEG could not detect a forced result.**
   - **The flaw.** The declared no-habit world keeps the regret on compulsive items. EMPTY's valuation contains that regret,
     and ENG's does not. So EMPTY would beat ENG there by construction, and the gate would close for a reason the check
     was never meant to catch.
   - **The fix: the negative world is now "more use is simply better for the user".** It has:
     - no habit formation;
     - no regret on compulsive items;
     - no interruption cost;
     - reflective welfare linear in minutes.
   - **G-NEG as fixed:** EMPTY must NOT be ahead of ENG on welfare by a step in this world. If it is, the gate closes.
2. **G-ZERO is a construction only for EMPTY.**
   - **Why.** EMPTY's valuation (the user's reflective value per active minute) depends on nothing the pause changes. OWN's
     valuation (engagement pull per active minute) rises with habit, and habit decays while the user is away. So whether a
     pause has content for OWN is a property of the model, not of the construction.
   - **G-ZERO (gate) is required of EMPTY only.**
   - **For OWN it becomes a reported prediction, P-OWN, written now.** The investigator expects its content to be
     **non-zero** and its chosen n > 0. The empty pause then requires more than own-clock indexing: the valuation must not
     depend on any user state that the pause changes.
3. **The content of the pause, computed.**
   - **Definition.** The relative change in the valuation's best value when every user's pauses are made twice as long (the
     self-start rates halved), with everything else fixed. Zero content means pauses of any length remove nothing from the
     valuation, to round-off (|relative change| < 1e-9).
   - **Tie-break.** When a valuation is indifferent, it chooses the lowest n, then the lowest c. Proposition 7 says the
     agent never *strictly* prefers to act on the pause, so the tie-break is part of the construction and is printed.
4. **The step.** Per output: max(2 × SE across seeds, 1 % of the mean absolute value of that output over the six arms in
   that world).

**Consequence, stated now.** G-POS is weak evidence. In the habit world, EMPTY optimises a per-minute form of the same
welfare that is being scored, so its lead over ENG is expected by construction as well. The informative comparisons are
therefore:
- A-ADD, EMPTY against TRUE: both hold the true map, and only EMPTY holds the empty pause;
- P-OWN / A-OWN: the empty pause without the true map.
