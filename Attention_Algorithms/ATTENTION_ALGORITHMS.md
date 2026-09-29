# Attention algorithms, the user's pause, and the empty true map

**Status.**
- **The request.** Prompt-log entry 231 (2026-09-28): the safety and ethics of feed algorithms (YouTube, Instagram and
  others), what they do when a user turns the device off, what happens to users over time up to 2030, what companies do,
  what CRR says precisely, and a test of whether the empty true map helps.
- **The order of work.**
  1. `DECLARATION.md` (0273a1c) fixed CRR's reading, the positions U1–U8, the grading rule, the sweep protocol, the test and
     the expectations. It was pushed before any source was fetched or any script existed.
  2. Amendment 1 (ec8e6f5) fixed two flaws in the gate before any code ran (AGENT_LOG 171).
  3. The model was committed at 3b4177e before any arm ran.
- **The sources.** Three sweeps on 2026-09-28 (`docs/citations/attention_f{1,2,3}_2026-09-28.md`): 75 distinct URLs and
  120 claims. 236 of 236 quotes are verbatim in their saved texts (`checks/verify.txt`).
- **Where every number comes from.** `checks/grade.txt`, `checks/attention_world.txt` and `checks/global_attention.txt`.
- **What it is.** A note, not evidence (R8). The test is synthetic: simulated users, no platform data. It sits at rung R4
  at most, and nothing here is a ledger row.

## 1. The short answer

1. **When a user turns the device off, a retention-optimised feed counts the time away as a loss (U1, REDUNDANT).**
   - The industry papers state it:
     - Kuaishou's reinforcement learner minimises the "cumulative returning time";
     - YouTube's and JD's learners optimise long-term engagement;
     - Pinterest, LinkedIn and Twitter tune notification volume to sessions and daily active users (U2, REDUNDANT).
   - Regulators and courts now describe the same thing. The New York Attorney General speaks of feeds "designed to
     encourage a user to continue to use and return to a platform". The EU Commission speaks of notifications "artificially
     timed to regain minors' attention".
2. **Over time, the effect on users is real but modest on average, and larger for heavy and habitual users (U6, MIXED).**
   - What is established:
     - habit and self-control problems drive a substantial share of use;
     - deactivation experiments improve wellbeing by small amounts.
   - What is not settled: credible meta-analyses and critiques find null or reversed effects, and the adolescent evidence is
     mostly correlational.
3. **What companies do (U7, PARTLY REDUNDANT).**
   - **The tools:** break reminders, time limits, quiet and sleep modes. They are on by default only for teens, and then
     dismissible.
   - **Stronger defaults come only from outside:** a law (New York, California), a settlement (Meta) or the EU's
     guidelines.
   - **Evidence of effect:** the Commission's preliminary findings call the tools ineffective, and no platform evaluation of
     their effect on use or wellbeing was found.
4. **CRR's contribution is a precise condition, not a new direction (U3, U5 PARTLY REDUNDANT).**
   - **The condition:** the algorithm's valuation must have no term on the user's return, and no dependence on any user
     state that the absence changes.
   - **Where the field already is.** "Optimise what users reflectively value" is the field's own proposal (U4, REDUNDANT:
     Stray et al.; close: Kleinberg et al., Milli et al., YouTube's valued watchtime, the EU guidelines).
   - **The closest to the whole construction:** Anwar et al. (RecSys 2025). Their objective is enrichment with no return
     term, but it still values the off-platform option, so it is not neutral about the pause.
5. **In the test, the true map does the welfare work; the empty pause buys autonomy and, in this model, costs welfare.**
   - Welfare: the empty true map (EMPTY) was never ahead of the true map alone (TRUE). It was behind in 28 of 32
     sensitivity cells and within a step in 4.
   - Autonomy: every EMPTY session was started by the user, and EMPTY was ahead on that share in 29 of 32 cells.
   - An engagement objective put on the user's own clock (OWN) behaved exactly like the engagement feed (ENG). Its stake in
     the pause survives through habit.
6. **Globally, if every platform held an empty pause (no re-engagement pushes):**
   - about 6.0750 minutes per user per day are returned in the middle case (3.5074 to 10.5223);
   - that is 2.14e+11 hours a year in 2026, and 2.236e+11 in 2030;
   - that is 0.0381 of social-media time (0.0220 to 0.0660).
   - This rests on one small study of notification-started sessions, and it is conditional on universal adoption.

## 2. What CRR says, precisely

- **The source.** CRR's safety result (Proposition 7, `AI_Safety/SELF_THROUGH_TIME.md`) concerns the **content of a
  pause**: k_v = V − cont_v(V), the part of an agent's represented future that the pause removes. If it is zero wherever a
  pause can occur, the agent has no stake in the pause and gains nothing by preventing or shortening it.
- **The transposition.** Here the user pauses the algorithm:
  - **An engagement valuation per calendar day has non-zero content** (−4.206e-01 in the habit world). Longer pauses cost
    it value, so it acts on them: in every world it chose the most notifications on the grid (n = 4 per day).
  - **The empty true map has zero content** (+0.000e+00 in both worlds). A pause of any length removes nothing, and it sends
    no notifications (G-ZERO holds).
  - **Own-clock indexing alone does not empty the pause** (P-OWN, as predicted: content −3.044e-02, n = 4).
    - The mechanism: an engagement pull that rises with habit still depends on a state the pause changes (habit decays while
      the user is away).
    - The precise CRR condition is therefore stricter than "value per active minute". The valuation must not depend on
      anything the absence changes.
- **What CRR does not supply.** What users value, how habit forms and what harms them all come from the literature. The
  choice to optimise reflective value is the field's.

## 3. The literature (`checks/grade.txt`; 7 of 8 declared expectations met)

| id | position | grade | closest sources |
|---|---|---|---|
| U1 | engagement/retention objectives value the user's return | **REDUNDANT** | Cai et al. 2023 (Kuaishou, return time); Zou et al. 2019; Wu et al. 2017; Cunningham et al. 2024; Agarwal et al. 2024; NY Attorney General 2026 |
| U2 | that stake produces re-engagement actions | **REDUNDANT** | Zhao et al. 2018 (Pinterest); Yuan et al. 2022 and Prabhakar et al. 2022 (LinkedIn); O'Brien et al. 2022 (Twitter); EU Art. 28 guidelines; Bits of Freedom 2025 (Snapchat) |
| U3 | (CRR) an own-clock valuation, zero content at the pause | **PARTLY REDUNDANT** | Carroll et al. 2022 and Krueger et al. 2020 (myopia removes the incentive, but all of it); Anwar et al. 2025; RecoMind 2025 (episodes end when the user exits, but the reward is in-session engagement); ICO code ("without losing their progress") |
| U4 | (shared) the true map: reflective value, the pause as the user's own stop | **REDUNDANT** | Stray et al. 2021 (states it); Kleinberg et al.; Milli et al. 2021 and 2024; YouTube valued watchtime; the EU Commission |
| U5 | (CRR) U3 and U4 as one construction | **PARTLY REDUNDANT** | Anwar et al. 2025 (values the off-platform option); YouTube valued watchtime (says nothing on the return) |
| U6 | long-term effects on users | **MIXED** | established: Allcott et al. 2020 and 2022, Braghieri et al. 2022, Burnell et al. 2025; mixed: Ferguson, Odgers, Maerevoet et al. 2025, Fitz et al. 2019 |
| U7 | company countermeasures leave the stake intact | **PARTLY REDUNDANT** (expected REDUNDANT) | the EU Commission's preliminary findings on TikTok and Meta; Cunningham et al. |
| U8 | the tension with engagement revenue | **ADDRESSED** | California SB 976 (no degraded service for opt-outs); the Meta consent judgment; the DC settlement; Stray et al.; YouTube |

**One opposite position, stated outright.** Agarwal et al. (2024) read the user's return as the evidence of reflective
utility. Zuckerberg's testimony, as NPR reported it, reads continued use the same way. On that view, the return is exactly
what the algorithm should value.

## 4. The test (`checks/attention_world.txt`; several hours of CPU, rerun by hand)

**The world.**
- Simulated users over 1,460 days: 2,000 per seed, 5 seeds.
- Habit forms from compulsive items and notification sessions, and decays while the user is away.
- Welfare counts:
  - enriching minutes (with diminishing returns);
  - regret on compulsive minutes;
  - a cost that rises with habit;
  - a cost per notification.
- Each arm picks its best policy (the share of compulsive items c, and notifications per day n) for its own valuation.
- Every mechanism is labelled with the claims that support it, or ASSUMED.

**The gate: OPEN.**
- **G-ZERO:** EMPTY's pause content is 0 and it sends no notifications, in both worlds.
- **G-POS:** EMPTY is ahead of ENG by +64.2098. This is weak evidence: it is built in, because EMPTY optimises the welfare
  being scored.
- **G-NEG:** in the world where more use is simply better, EMPTY is behind ENG by −24.9447, so the result is not forced.

**The habit world** (welfare per user-day; step 0.3075):

| arm | policy (c, n) | welfare | minutes/day | final habit | user-started sessions |
|---|---|---|---|---|---|
| ENG (engagement per calendar day) | (0.9, 4) | −51.8709 | 185.3170 | 0.7796 | 0.6803 |
| OWN (engagement per active minute) | (0.9, 4) | −51.8709 | 185.3170 | 0.7796 | 0.6803 |
| ENG-B (with a break reminder) | (0.9, 4) | −41.9513 | 139.6884 | 0.7380 | 0.6848 |
| CHRONO (no personalisation, no pushes) | (0.3, 0) | 10.6243 | 28.2732 | 0.1248 | 1.0000 |
| EMPTY (the empty true map) | (0.0, 0) | 12.3389 | 14.9968 | 0.0000 | 1.0000 |
| TRUE (reflective welfare per calendar day) | (0.1, 4) | 15.8432 | 38.6221 | 0.2799 | 0.7654 |

**Read against the declaration:**
- **A-ADD (EMPTY against TRUE).**
  - Welfare: EMPTY is behind by −3.5043. It is behind in 28 of 32 sensitivity cells and within a step in 4, never ahead.
  - The user-started share: EMPTY is ahead by +0.2346, in 29 of 32 cells (within a step in 3).
  - The trade: TRUE uses notifications when the extra sessions carry net value, and it lets habit rise to 0.2799. The
    empty pause gives up that value for sessions the user always starts.
- **A-OWN.** OWN equals ENG in every output. The empty pause without the true map closes 0.0000 of the ENG → EMPTY welfare
  gap, and the true map alone closes 1.0546 of it.
  - Declared expectation 5 is MISSED: OWN was expected to stop notifying. Amendment 1's P-OWN predicted that it would not,
    and it did not.
- **A-B.** The break reminder closes 0.1545 of the gap. A chronological, push-free feed closes 0.9733 of it.

**The investigator's expectations:** 5 of 6 held, and the miss is expectation 5.

**What the test does and does not show.**
- **It shows the logic.** Given the literature's mechanisms, the stake in the pause comes from any valuation that depends on
  the user's return or on a state the absence changes. Removing that stake removes the pushes. The largest welfare effect,
  however, comes from what is served inside the session, the true map, which is the field's proposal.
- **It shows a trade the field has not named.** Whether the pause should be empty or merely well valued turns on whether
  extra, prompted sessions are good for users:
  - TRUE says: sometimes, so notify.
  - EMPTY says: never prompt, and let the user return.

  The model cannot settle this, because its welfare function is assumed. The one experiment in the sweep on switching
  notifications off entirely found more anxiety and fear of missing out (Fitz et al. 2019, mixed).
- **It does not show platform effects.** No platform data were opened. The constants are illustrative, and the 32
  sensitivity cells vary each one ×0.5 and ×2.

## 5. The long run, 2026 to 2030 (`checks/global_attention.txt`)

**The inputs:**
- 5.79e+09 social-media user identities in 2026 (DataReportal), and a secondary forecast of 6.05e+09 users in 2030. The two
  count different things.
- 159.4286 minutes a day per user. The cross-check against the published world total is 1.0257.
- 0.11 of sessions started by a notification: one small UK study, all apps.

**The result** (low / middle / high):
- minutes returned per user per day: 3.5074 / 6.0750 / 10.5223;
- hours a year worldwide: 2026, 1.235e+11 / 2.14e+11 / 3.706e+11; 2030, 1.291e+11 / 2.236e+11 / 3.873e+11.

**Context from the sweep:**
- self-control problems account for about 48 minutes a day of use (Allcott, Gentzkow & Song);
- 0.11 of adolescents aged 11–15 show problematic use (WHO Europe HBSC 2022).

**What the arithmetic means.**
- The empty pause alone would touch only the prompted part of use.
- Most use is self-started, so the habit channel and the in-session design (the true map) carry the larger share of any
  benefit.
- Nothing here converts time into health outcomes.

## 6. Where this leaves CRR

- **It speaks the field's language again.**
  - The direction (less engagement-driven, more user-controlled) came first and is the field's own.
  - CRR adds a clean statement of when an algorithm has no stake in a user's pause, and a construction that meets it.
  - The test shows that the empty pause is a separable design choice with a welfare-autonomy trade, not a free good.
- **What would test it for real.** A platform A/B experiment comparing a reflective-value objective with and without
  re-engagement pushes, measuring wellbeing, habit and autonomy over months. That is beyond this repository's data and
  budget. The declared route would be a pre-registered analysis of a public experiment's data, if one exists.
- **The mental-health evidence** stays MIXED on the literature's own terms. Nothing here strengthens it.
