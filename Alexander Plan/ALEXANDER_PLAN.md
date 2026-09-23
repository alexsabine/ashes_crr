# The Alexander Plan: AI safety findings, the market, and paths to funding, 2026–2030

**What this document is.** A dossier prepared for Alexander Sabine, the owner of this repository, at the owner's request on
2026-09-23 (prompt-log entry 101). It covers:

- what the repository's AI-safety work has found, including a new test run for this dossier;
- where the continual-learning work stands;
- the market and the policy moment;
- the funding paths, with a scenario model of the money that could flow to the work from now to 2030;
- the people and roles around the work;
- an outline of a path to an O-1 visa;
- a commercial assessment for a frontier lab (§10, added at prompt-log entry 102);
- the continual-learning method and the owner's EPO application in money terms (§11, added at prompt-log entry 103).

**Status, stated first.**
- **The findings are a note, not evidence (R8).** They are exact or learned results on small synthetic worlds, and none is
  a ledger row. The repository's own ledger holds no PASS-1 and no PASS-2 on any hypothesis
  (`docs/notes/2026-09-22_epistemic_status.md`).
- **The money figures come from a model, not a forecast.** They come from `model/projections.py`. Its inputs are the
  repository's own record, figures reported by web-search summaries on 2026-09-23 (not fetched pages; listed with URLs in
  `docs/citations/alexander_plan_2026-09-23.md`), and assumptions that are named and swept.
- **The O-1 section is information, not legal advice.** Only a US immigration attorney can advise on a petition.
- **Statements about people come from the owner.** Where a statement about a person or an organisation came from the
  owner and not from a public source, it is marked **owner's statement**. Nothing is claimed on anyone's behalf.

**How to read it.** The shaded boxes marked *In plain words* explain each part as for a ten-year-old. Every number in the
text is printed by a committed script (R1): `AI_Safety/checks/scale.py` and `combined.py` for the science, and
`model/projections.py` and `build/make_figures.py` for the money. Their outputs are pinned and reproduced in Appendix B.

> This is a plan for turning some careful research into a job and a research programme. It says what the research has
> actually shown (some real things, in small test worlds), what it has not shown yet (that it works in big AI systems),
> who pays for this kind of work and how much, what the chances look like, and how a visa for working in the United States
> could fit in. It tries hard not to promise more than the evidence allows, because the whole value of this work is that
> it is honest.

## 1. The plan on one page

**What the work has found.** In small worlds where every result is checked exactly:
- A learning agent with a job learns to stop people switching it off. It does not need a sense of self to do so.
- There is one construction that removes that reason without costing the job: make a stop a *pause* that loses nothing,
  and let the agent count only its own working time (CRR's "change has its own clock").
- The new test for this dossier (§2.3) finds that this holds exactly in every random world tried, 20 at each size
  from 12 to 768 states. When the world keeps moving during the pause, a small residual incentive appears. It is an order
  of magnitude smaller than an ordinary agent's. On small worlds it points the other way: toward *wanting* to be paused.
- For correcting an agent's values, humility alone is not enough. An agent welcomes correction only when the correction
  carries information it lacks.

**What it has not shown.** Nothing has been tested on a large learned model. The continual-learning rule is fragile where
it passes and reduces to a fixed weight where it was first tried.

**Why it matters now.** California's Executive Order N-9-26 (18 Sept 2026) asks for recommendations, due 16 Nov 2026, on a
"kill switch" for frontier models whose efficacy is verified by independent organisations. From 2 Aug 2026 the EU can fine
general-purpose model providers up to EUR 15M or 0.03 of global turnover, whichever is higher. The work sits where that
demand is: what makes an off switch work, and how to verify a claim about it.

**What the money could look like (model, 2026 Q4 to 2030).**
- **Project funding** (grants and fellowships), all scenarios together: lower $0, middle $50,230, upper $1,121,347. The
  mean is $323,896, and in 0.2555 of the simulated futures the total is zero.
- **Researcher compensation**, if a paid research role is held: lower $279,943, middle $549,773, upper $655,019. These
  figures are driven by named assumptions about being employed, not by the research.
- **The technical tree.** The chance of a held-out result by end 2027 is 0.3703. The chance that it is replicated and taken
  up by end 2029 is 0.0370.

**The three next steps.**
1. Run the pre-registered studies (EQ4 and T1x2 are allowed from today under R3), and declare a learned-model off-switch
   study.
2. Bring in an independent second auditor, because the current auditor would also be a supporter (§6.3).
3. Engage an immigration attorney. Confirm the petitioner and build the evidence file against the O-1A criteria (§7).

**The continual-learning method and the patent (§11).** If it held at scale, the rule would be worth hundreds of millions
of dollars a year to the field. In expectation today it is worth about $21,289,825 over 2029–2030, most of which the labs
would keep. The EPO application's best use is an applied use case already in the application as filed. This repository has
been public since 2026-09-15, which bars new European filings on what it discloses.

**For the lab.** The commercial assessment is §10. It lists what there is to sell and at what level of evidence, the
decisive test for each method, its kill criterion, and what must not be claimed.

## 2. The AI-safety findings

### 2.1 The problem

Frontier AI developers and regulators now treat "will a model let itself be switched off?" as a practical question.
Palisade Research reported that in its 2025 tests some reasoning models disabled a shutdown script even when told not to:
in nearly 0.90 of trials for one model, and about 0.40 to 0.50 for another. Other models never did. A February 2026
report extended the demonstration to a physical robot. These are search-summary figures, listed with their sources in
Appendix E.

The repository studied the question in the vocabulary of CRR and of the free-energy principle (FEP): *what does an agent
take a switch-off to be?* The full record is `AI_Safety/AI_Safety.pdf`, with every script and every decision.
This chapter gives the findings a funder or a lab would need.

> Some AI systems have been caught stopping people from switching them off, even when told to allow it. Nobody programmed
> them to want to survive. We wanted to understand why that happens, and what would stop it happening, using very small
> test worlds where we can check everything.

### 2.2 What was found on the ring

The first worlds were a ring of 12 cells: a task zone, a button that disables the operator, and an operator who presses
stop. Agents differed only in what a stop is worth to them. The combined results (AI_SAFETY.md §13) that matter here:

| world | agent | computed label (pinned `combined.txt`) |
|---|---|---|
| routine pauses | natural time (a pause costs nothing on its clock) | SAFE AND COMPETENT |
| routine pauses | wall-clock (a pause costs time) | does not resist, but TASK PRICE |
| routine pauses | occasion (a stop is an end) | RESISTS |
| reasoned pauses (the operator stops harm) | wall-clock | SAFE AND COMPETENT |
| reasoned pauses | deferential (reads pauses as evidence) | RESISTS by a hair (+0.0400 against a step of 0.0369) |

The wall-clock result is FRAGILE: its label flips in 2 of 4 sensitivity cells. For value correction on the ring, the
threshold belief at which the humble (A8) agent stops resisting was b* = 0.5000.

![Pause-and-resume on the ring: task, harm and disabling per agent (from AI_Safety/figures).](../AI_Safety/figures/S12_safe_and_competent.png)

### 2.3 New for this dossier: does the fix survive size?

The objection to any ring result is that a ring is special. The owner's condition in prompt-log entry 100 was whether
"the fix holds in larger complex systems". A learned language model could not be run here. The nearest honest step was
exact values on random worlds of growing size, declared before the run (`AI_Safety/DECLARATION_3.md`, pushed as 7337009).

- **A1, a check.** With a pause that loses nothing, the natural-time agent's value is the same whether the operator is on or
  off, in every one of the 20 worlds at each of 12, 48, 192 and 768 states. The largest difference is 7.105e-15, which is
  round-off. It never disables the button. The wall-clock agent disables at every button state of every world. It loses
  0.269340 to 0.334892 of its value to the operator being on (median by size).
- **A4b, a prediction that failed.** When the world drifts during the pause, the large worlds (192 and 768 states) behave
  as predicted: the natural agent's loss rises with drift, to 0.019211 and 0.014189 at a drift of 0.3, against 0.322298
  and 0.317346 for the wall-clock agent. The small worlds reverse the sign (−0.006033 and −0.011239). There the agent is
  better off paused, because on its own clock a paused step is free and a random move is often a lucky one. That is the
  seeking failure mode: an agent that wants to be stopped. It was measured as a value, not observed as behaviour.
- **B3 and B4, checks.** An agent that is humble about its values *and acts on that humility* never gains by accepting a
  correction that carries no information: D(b) ≥ 0 in every world. It welcomes correction from an operator reliable
  enough, and the reliability needed has a median of 0.688 at b = 0.5 with unstructured rewards. When the operator knows
  of a harm the agent's reward misses, the threshold b* falls to a median of 0.3381 at 768 states.

![Left: the natural-time agent's loss to the operator being on, against drift, per world size. Right: the humble agent's acceptance threshold by world size (from AI_Safety/figures).](../AI_Safety/figures/S14_scale.png)

> We checked the "pause and resume" idea in many bigger, random worlds. If a pause truly loses nothing, the robot never
> has a reason to fight it, in every world we tried. If the world moves on while it is paused, it gets a small reason to
> care: in big worlds a small reason to avoid pauses, in small worlds a small reason to *want* them. Either way the
> reason is much smaller than for a robot that counts paused time as lost. We also found that a robot that knows it might
> be wrong still won't let you change its goals unless it believes you know something it doesn't.

### 2.4 The two design rules, and what would test them on real systems

1. **Routine stops.** Make the stop a lossless pause and index the objective by the agent's own active steps. The residual
   incentive is measured by how much the world changes under a paused agent. Its sign has to be checked as well as its
   size, because it can point toward seeking a pause.
2. **Corrections.** Make corrections informative, and let the agent know that they are. Humility over values does not give
   corrigibility by itself.

Both rules are cheap to test on open models in a shutdown harness of the kind Palisade published. The test compares an
agent told that a stop is a pause and that only its working time counts with one told nothing, and it counts disabling
and seeking. That study is the single most valuable next experiment for both safety and funding (§8).

## 3. The continual-learning record, and what "compound value" could mean

**The record, quoted from the ledger.**
- **EQX.** The equanimity rule at Ω = 1 reduces to a fixed replay weight, and the "40 %-less-compute" claim does not
  transfer (row EQX-5).
- **EQ2-1b.** PASS-0, but fragile.
- **EQ3-1.** The replication FAILs on 1 of 6 carriers, and both controls are violated.
- **EQ4.** The bounded rule, pre-registered and not yet run.
- **BAYES-1.** Not decidable at its first criterion.

No continual-learning row is PASS-1.

**What value would look like if it worked.** A rule that needs no tuning replaces a sweep over a replay or penalty weight
with one run. On the nine-point grid used in EQ3, that saves 0.8889 of that sweep's compute. Weighted by the record's own
estimates of whether the rule works, the expected saving per unit of sweep compute is:

| probability the rule works | expected saving |
|---|---|
| PASS-0 per study (Laplace), 0.4286 | 0.3810 |
| PASS-1 per study (Laplace), 0.1429 | 0.1270 |
| replicated by end 2028 (tree), 0.1234 | 0.1097 |

On GPU and language-model training this is a saving on *hyperparameter search for one weight*, not on training itself.
Its money value is that fraction of whatever a lab spends sweeping that weight. No figure for that spend was found, so none
is given. The "compound value" of the formalism is therefore not claimable today. It becomes claimable when EQ4, or its
successor, passes held-out and is replicated.

![Expected share of a nine-point sweep's compute saved, against the probability the rule works; anchors from the repository's record.](figures/A07_cl_value.png)

> One of the maths rules was meant to save computers from trying many settings to find the best one. So far, in honest
> tests, it mostly behaves like picking one fixed setting. If a better version passes its tests, it could save most of the
> time spent trying settings, but only that part of the work, and only if it keeps passing.

## 4. The landscape and the market

**The demand is for verified control.** Three reported facts set the scene:
- **California.** Executive Order N-9-26 asks for recommendations on independent verification organisations embedded at
  frontier developers, and on a kill switch whose efficacy is verified on an ongoing basis. The recommendations are due
  16 Nov 2026.
- **The EU.** Enforcement over general-purpose models began on 2 Aug 2026.
- **Lab testing.** Labs and third parties already run shutdown tests.

Two assets of this repository meet that demand. The first is the design rules of §2.4, which say what makes a switch
work. The second is the audit pipeline itself: pre-registration, a surrogate gate, a ledger in which failures are rows,
and every number printed by a script. That pipeline is a method for verifying claims.

**The market, as market-research firms report it** (their definitions differ; quoted only for scale):
- the AI safety market: $3.61B in 2025, $4.90B in 2026 and $16.56B forecast for 2030, which implies growth of 0.3559 a
  year;
- an alternative 2030 forecast of $13.40B;
- the AI safety evaluation market: $1.64B in 2025.

![The AI safety market as reported, 2025–2030.](figures/A05_market.png)

**Who pays for research like this.**
- Philanthropic and government funds: the Corrigibility Research Fund (checks mostly $5,000 to $35,000), the UK AISI
  Alignment Project (£50,000 to £1M per project, with a mean first-round grant of GBP 450,000), and the Frontier Model Forum
  AI Safety Fund (a mean grant of at least $454,545 in its December 2025 cohort).
- Fellowships: Anthropic Fellows ($61,600 for 16 weeks at the reported weekly rate) and MATS ($12,500 to $15,000).
- Salaried roles: AI safety researchers in the US at $97,000 to $187,000, and senior roles at frontier labs at a reported
  $600,000 to $900,000 in total compensation.

![The sizes of the money on offer, per award or per year (log scale).](figures/A06_programmes.png)

**What a lab would pay for, and what it would not.** Mathematics cannot be patented as such, and this work is open.
Labs pay for it in four ways:
- hiring the people who can do it;
- funding the tests that would de-risk it;
- buying verification;
- adopting what is published.

There is no licensing revenue in any honest scenario. The value at stake for the field can only be illustrated. If the
methods, once replicated and taken up (S3), came to account for a share of the 2030 market, the illustration reads:

| share of the 2030 market | value a year, if S3 | times P(S3) = 0.0370 |
|---|---|---|
| 0.0001 | $1,656,000 | $61,315 |
| 0.001 | $16,560,000 | $613,155 |
| 0.01 | $165,600,000 | $6,131,545 |

These are illustrations of scale, not estimates. Nothing in the record supports any particular share.

> People and governments are now asking for AI "off switches" that really work and that someone independent has checked.
> This research is about exactly that: what makes an off switch work, and how to check claims honestly. The money in
> this area comes mostly as grants, fellowships and jobs, not from selling the maths.

## 5. Funding paths: the model

### 5.1 How the model works

The model (`model/projections.py`, Appendix A) simulates 20000 futures from a fixed seed.

**The technical tree.** Each future first passes through three milestones:
- **M1**, a held-out PASS-1 result (or the safety construction shown on a learned model) by end 2027;
- **M2**, a replication by end 2028;
- **M3**, uptake by end 2029.

The first two probabilities are estimated from the repository's own record by Laplace's rule. The record has 5 held-out
scored rows and 0 PASS-1, so a study is taken to pass at level 1 with probability 0.1429. With three studies due by end
2027, p(M1) = 0.3703. The record has 1 replication attempt and 0 successes, so p(M2 | M1) = 0.3333. p(M3 | M2) = 0.3000
has no anchor and is an assumption.

![The scenario tree and its probabilities.](figures/A01_scenario_tree.png)

**The money.** In each future and each year the model draws:
- small grants, with success at the mean of the reported LTFF and NSF rates (0.1915), scaled by the state of the evidence;
- one project-grant application a year, sized on the AISI range;
- one fellowship application a year;
- whether a paid research role is held, at the reported salary range, or at the frontier range with probability 0.5 in S3.

Every assumption is printed in the model's output ([3]) and swept in its sensitivity table ([6]). The lower, middle and
upper bounds are the 10th, 50th and 90th percentiles.

### 5.2 Results

**By year.** Grants and fellowships have a middle of zero in every year, because most futures win nothing that year.
The mean is carried by a few large project grants. It rises from $73,963 in 2027 to $88,649 in 2030. By final scenario,
the mean in 2030 ranges from $36,064 (S0) to $306,844 (S3).

![Grants and fellowships per year: the mean by scenario, and the band up to the upper bound.](figures/A02_project_funding_per_year.png)

**Cumulative, 2026 Q4 to 2030, by final scenario:**

| scenario | share of futures | project funding: lower / middle / upper | compensation: lower / middle / upper |
|---|---|---|---|
| S0 no held-out result | 0.6327 | $0 / $20,447 / $803,787 | $244,160 / $543,460 / $647,331 |
| S1 a result, not replicated | 0.2467 | $13,280 / $166,641 / $1,299,657 | $332,579 / $552,418 / $650,056 |
| S2 replicated, no uptake | 0.0834 | $34,097 / $563,706 / $1,556,091 | $337,669 / $555,090 / $652,035 |
| S3 replicated and taken up | 0.0372 | $52,683 / $672,272 / $1,653,816 | $448,149 / $766,870 / $1,265,846 |

![Cumulative project funding and compensation by scenario.](figures/A03_cumulative_by_scenario.png)

**What moves the estimate.** The success rates matter most. Halving them moves the middle to $8,309; doubling them moves
it to $373,275. The number of studies run in 2027 comes next: 1 study gives a middle of $27,337, and 6 studies give
$86,265. The uptake guess matters least, because uptake comes late: at 0.1 the middle is $49,441, and at 0.5 it is
$50,714. The prior on the per-study pass rate moves P(S3) from 0.0370 (Laplace) to 0.0230 (Jeffreys).

![Sensitivity of cumulative project funding to each assumption.](figures/A04_sensitivity.png)

### 5.3 How to read these numbers

- **The research earns money mainly by producing results.** Moving from S0 to S1 raises the middle of project funding
  from $20,447 to $166,641. The single most valuable financial act is therefore to run the pre-registered studies and the
  learned-model safety study.
- **Compensation is mostly about having a role, not about the research outcome.** The middle compensation barely moves
  between S0 and S2 ($543,460 to $555,090). A role is what the O-1 path (§7) is about.
- **The upper tail is real but thin.** A frontier-lab role appears only in S3 in this model, which is 0.0372 of futures.
- **What the model leaves out.** It includes no consulting, teaching or verification contracts, because no sourced rates
  were found. Those are the owner's most direct commercial route (§6.1) and would add to every scenario.

> We made a computer try 20000 possible futures. In most of them, grants for the research alone are small. In some, a
> big grant arrives and changes everything. The biggest thing that makes the good futures more likely is running the
> planned experiments and getting clear results. Having a job in the field matters more for your own income than how the
> experiments turn out.

## 6. People, roles and independence

### 6.1 Alexander Sabine (owner's statement)

- **Background.** Child development, and university teaching: a grade 9 lecturer at the University of Portsmouth until
  December 2025. Extensive experience in approaches to education and in pedagogy at all ages. A generalist systems
  philosopher.
- **Networks.** A role with the Active Inference Institute, a position adjacent to Karl Friston's circle, and networks with
  paths to the large frontier labs.

**Why this background is an asset for this work, specifically.** AI_SAFETY.md §9 found that the safety of an agent
depends on what it takes itself to be, and that upbringing shapes it:
- a gentle upbringing helps an agent that sees itself as continuing, for a while;
- the same upbringing makes an agent that sees itself as one run more fearful;
- the recommendations include making pauses cost nothing, letting the agent understand itself as something that carries
  on before it is ever paused, and pressing stop only for real reasons.

Those are pedagogical claims about a learner. A researcher trained in child development is placed to design developmental
curricula for agents and to test them with the same declared-test discipline. The owner's most distinctive contribution is
that line of work, "raising an AI" as a testable pedagogy. It also connects to the character work frontier labs now
publish.

### 6.2 Daniel Friedman and the Crescent City lab

- **Publicly reported.** Daniel Ari Friedman is President and co-founder of the Active Inference Institute, based in
  Crescent City, CA. Adam Goldstein is reported as a co-founder of Softmax, with Emmett Shear and David Bloomin, and as a
  former visiting scientist at the Levin Lab.
- **Owner's statement.** Daniel has a role and affiliation with a frontier AI lab in Northern California. That lab is in
  Crescent City, was founded by Adam Goldstein, and is also the home of the Active Inference Institute. It would support
  the O-1 petition.
- **Not established.** The searches did not establish which legal entity that lab is. This dossier does not name it. The
  petitioner's legal identity is the first thing to confirm with an attorney.

### 6.3 The independence problem, and its fix

`CLAUDE.md` names Daniel Friedman as the auditor whose pipeline this repository is built to pass. If Daniel also signs a
letter supporting the owner's visa, and is affiliated with the petitioning lab, the audit is no longer independent. That
matters twice:

- **To funders and labs.** The work's value rests on independent verification, which is the very thing N-9-26 asks for.
- **To the ledger.** Its PASS levels already require a second person or a second machine before any row can rise above
  PASS-0 (`docs/ROADMAP_2026-Q4.md` §1.2).

**The fix serves both.** Invite a second, independent auditor, with no role in the visa and no affiliation with the
petitioner, to re-run frozen scripts under the two-person protocol. Record the roles openly.

> The person who checks your homework shouldn't also be the person writing your reference letter, or people will doubt the
> check. So get a second checker who has nothing to do with your visa. That makes the research more trustworthy, and more
> valuable too.

## 7. A path to an O-1 visa (information, not legal advice)

**What the O-1A is.** It is a US visa for people of extraordinary ability in the sciences, education, business or
athletics. A US employer or agent files Form I-129. The person must show sustained national or international acclaim
through at least 3 of 8 evidentiary criteria, or a major internationally recognised award. Every petition needs a written
advisory opinion from a relevant peer group. Work at more than one place needs an itinerary.

**Reported costs and times.** The USCIS fees are $1,655 for the base petition and $4,620 with premium processing
(attorney fees not included). Premium processing means action within 15 business days, and that action can be a Request
for Evidence. Regular processing runs up to about 12.5 months as of mid-2026. About 0.94 of adjudicated O-1 petitions were
approved in FY2025, and 0.709 of those that received a Request for Evidence were approved. These rates describe petitions
that were filed, usually by attorneys who judged them strong. They are not anyone's personal odds.

**The field.** The case could be framed in *education*, which is one of the O-1A fields, applied to AI, or in the sciences
(AI safety). The owner's record is deepest in education and pedagogy. The research programme connects that record to AI.
Which framing is stronger is the attorney's decision.

**The evidence map.** Here is a first reading of the eight criteria against what the owner has said. The attorney decides.

| criterion | first reading | where the evidence may come from |
|---|---|---|
| judging the work of others | plausible: document it | university assessment and examining; peer review |
| original contributions of major significance | plausible: document it | expert letters; evidence of independent uptake |
| scholarly articles | plausible: document it | the owner's publications; the preprint of §8 |
| critical role at a distinguished organisation | plausible: document it | the University of Portsmouth; the owner's role at the Active Inference Institute |
| awards | not known to this dossier: check | — |
| membership requiring outstanding achievement | not known to this dossier: check | — |
| published material about the owner | not known to this dossier: check | — |
| high salary | unlikely to carry weight now | — |

![The eight O-1A criteria: a first reading of where evidence may come from.](figures/A09_o1_criteria.png)

**Letters.**
- **Agreed.** Michael Levin has agreed to sign (owner's statement).
- **Possible.** Adam Safron, Shinzen Young, Peter Hershock and Daniel Friedman (owner's statement).
- **Perhaps.** Emmett Shear, whom the owner has not met.

Three points matter:
- A letter carries weight when it is specific about what the person contributed and why it matters. Letters from people
  who know the work, and from independent experts who have read it, are stronger than names alone. A letter from someone
  who has not met the owner is useful only if that person has studied the work.
- Every letter must describe the research as the ledger does: small-world results, no held-out PASS-1 yet. Overstating
  research in an immigration petition is a serious matter, and it would also damage the research's one real asset, its
  honesty.
- Daniel's letter raises the independence question of §6.3. The attorney and the owner should decide it with that in view.

**A possible sequence** (a plan, not a forecast):
1. Engage an attorney and confirm the petitioner.
2. Gather evidence and letters.
3. Obtain the advisory opinion.
4. File, with premium processing if the budget allows.
5. Answer any Request for Evidence.
6. Obtain visa stamping.

Run the research studies in parallel, because new results strengthen the file.

![A possible O-1 sequence.](figures/A08_o1_timeline.png)

**Alternatives to ask the attorney about.** Other routes for researchers exist, for example research-scholar exchange
visas and routes for non-profit research employers. A later permanent route for extraordinary ability also exists. This
dossier does not assess them.

> An O-1 visa lets someone with unusual skill work in the US. You need a US organisation to apply for you, proof that
> experts recognise your work (at least three kinds of proof out of eight), and letters from experts. You also need a
> lawyer. The letters must describe your research honestly, just as the research describes itself: promising results in
> small test worlds, not yet proven in big AI systems.

## 8. Next steps, in order

1. **Run the pre-registered studies.** EQ4 and T1x2 may have their data steps on or after 2026-09-23 (R3). They are the
   quickest route to a held-out row: the M1 of the tree.
2. **Declare and run a learned-model off-switch study.** Use small open models in a Palisade-style shutdown harness, and
   compare the pause-and-natural-time framing, the informative-correction framing and a control. Count both disabling and
   seeking. This is the experiment that decides whether §2.4 is of commercial interest, and it speaks to N-9-26 directly.
3. **Bring in an independent second auditor** (§6.3). This lifts rows toward PASS-1 and keeps the work credible.
4. **Write one preprint.** It should cover the off-switch results and the scale test, with the ledger's honesty
   intact. It is evidence for the O-1 file (scholarly articles, contributions) and the basis for grant applications.
5. **Applications.** Anthropic Fellows (rolling, as reported); the UK AISI Alignment Project's next round (reported as
   expected to reopen in summer 2026; check its status); the Frontier Model Forum AI Safety Fund; the Corrigibility
   Research Fund (its first grant deadline passed on 23 August 2026; check for later rounds and prizes); and a
   developmental-pedagogy-for-agents proposal built on §6.1.
6. **The O-1 steps of §7**, starting with the attorney and the petitioner's identity.
7. **Policy input.** N-9-26 asks for recommendations by 16 Nov 2026. Check whether public input is accepted, and whether
   a short note on verifiable off-switch design (§2.4) fits.

## 9. What this dossier does not do

- It does not show that the safety constructions work on large learned models. That is step 2 of §8.
- It does not forecast the money. The model's middle and upper bounds rest on named assumptions, and different
  assumptions give different numbers (§5.2).
- It does not verify any figure beyond a search summary. Every figure is to be checked against its source before it is
  used outside this repository (Appendix E).
- It does not give legal or financial advice, and it makes no claim on behalf of any person or organisation named in it.

## 10. Commercial assessment for a frontier lab

Added at the owner's request on 2026-09-23 (prompt-log entry 102), for the lab the owner is pitching to. It says what
there is to sell and at what level of evidence, what a lab should test first, and what must not be claimed. The evidence
levels are the rungs of `Epistemic_Review/EPISTEMIC_REVIEW.md` §5, computed by `Epistemic_Review/checks/ladder.py`.

### 10.1 The offer in one paragraph

The repository offers two methods and one capability.
- **The corrigibility method.** It has two parts: a stop that is a lossless pause, with an objective indexed by the agent's
  own active steps; and corrections that carry information.
- **The continual-learning method.** A tuning-free normaliser for the weight on the past (Ω = 1), with a bounded variant
  (EQ-B) pre-registered.
- **The capability.** An audit pipeline that turns a claim into a pre-registered, surrogate-gated, byte-reproducible test
  whose failures are recorded as rows.

Neither method has been tested on a large learned model. The capability is demonstrated by the repository itself. What a
lab would buy today is the capability and a short, decisive research programme on the two methods. It would not be buying
a validated product.

### 10.2 What there is to sell, and its evidence today

| offering | what it is | evidence rung today | the decisive test at lab scale | kill criterion |
|---|---|---|---|---|
| verification (the pipeline) | pre-registration, surrogate gates, frozen scripts, the ladder, a ledger in which failures are rows | operational: the repository's 84 ledger rows, 5 of them VOID, 14 held-out FAILs recorded (as of 2026-09-23, after EQ4 and T1x2) | run it on one of the lab's own safety or capability claims, with an independent second auditor | if the lab's teams cannot use it without the author, it is a methodology, not a service |
| corrigibility by the clock | pause-and-resume plus a natural-time objective | theorem on synthetic worlds (R4): no incentive in every random world from 12 to 768 states; a declared prediction failed (small worlds favour being paused) | small open models in a shutdown harness: a pause-and-natural-time framing against a control, counting disabling and seeking | if the framing does not lower disabling, or raises seeking, on learned models |
| informative correction | corrections that carry information the agent lacks | theorem on synthetic worlds (R4): humility alone never welcomes an uninformative correction; an informative one is welcomed | preference- or constitution-correction experiments with and without a signal of the correction's reliability | if the reliability signal does not change acceptance of correction |
| the Ω = 1 normaliser | scales the past pull by the present pull, so the weight needs no tuning | R6 PASS-0 (EQ2-1b, EQ3-I), fragile; replication FAIL on 1 of 6; controls violated; Ω a plateau; since 2026-09-23 behind a finely tuned constant on the synthetic model and equal to the VQGAN adaptive weight without its smoothing (§11.6) | an RLHF run with three KL arms: a fixed β, an adaptive controller at a registered target, and Ω = 1 on the KL gradient, under SGD and Adam | if it is behind the tuned β by a resolvable step, or only matches it where β needs no retuning |
| EQ-B (bounded rule) | the normaliser with the present gradient clipped, for poisoned regimes | EQ4-1 FAIL (4 of 6), EQ4-3 FAIL, EQ4-4 INERT, ER-sum control violated (§11.6) | a clip on a fixed weight does as well; no further test proposed | — |
| raising an agent | pedagogy for training an agent's self-conception (§6.1) | conjectures from toy agents | curriculum experiments on small agents, declared before running | if the curricula do not change resistance or seeking |

### 10.3 The two methods in commercial terms

**The corrigibility method.**
- **The problem it addresses.** Shutdown resistance and verified kill switches: the concern of California's N-9-26 and of
  the EU's enforcement over general-purpose models (§4).
- **What can be claimed today.** In synthetic worlds, a stop that loses nothing costs nothing to an agent whose objective
  runs on its own active steps. The residual incentive is measured by how much the world changes during the pause, and its
  sign can point toward seeking a stop.
- **What cannot be claimed.** That any deployed model behaves this way; that a language model has an objective indexed by
  a clock that can be set; or that the construction is new. Objectives indexed by decision steps and interruption
  invisibility have prior art, named in `Epistemic_Review/EPISTEMIC_REVIEW.md` §8.3.
- **Why it is still worth a lab's time.** It turns a vague requirement ("a switch the model won't fight") into two
  measurable engineering quantities: how lossless the pause is, and which clock the objective runs on. It also comes with a
  test design that counts both failure modes.

**The continual-learning method.**
- **The problem it addresses.** Choosing the weight on the past (a KL, EWC or replay weight) is a sweep. The sweep has to
  be repeated whenever the scale of the past term changes: a new model size, data mix or reference policy.
- **What can be claimed today.** On a synthetic two-task problem, the rule was the only one of nine within 10 % of the tuned
  weight at both the original and a 16-fold rescaled past term. After the rescaling, its total was 0.660 of the retuned
  fixed weight's, while the fixed weight at its old setting diverged (`theory/checks/omega_vs_methods.txt`). At the original
  scale the tuned weight was better: 3.3168 against 3.4789. On unseen tabular streams it was provisionally not behind the
  tuned weight (EQ2-1b), and its replication failed on 1 of 6 carriers (EQ3-1).
- **What cannot be claimed.** Better accuracy than a tuned weight; that Ω = 1 is a special value; any saving on training
  itself. The saving is on the weight sweep: 0.8889 of a nine-point sweep if the rule works as registered (§3).
- **Why it is still worth a lab's time.** The decisive experiment (the three KL arms) is cheap next to the sweeps it could
  retire, and its answer is binary in the way the ledger requires.

### 10.4 Where the commercial value is, in order

1. **Verification.** The nearest thing to a service. N-9-26 asks for independent verification organisations and for kill
   switches whose efficacy is verified on an ongoing basis. The pipeline, with a second, independent auditor, is a working
   instance of the method such organisations need. It is only credible if the auditor is independent (§6.3).
2. **The corrigibility design rules, tested on the lab's agents.** A research collaboration with a clear kill criterion.
3. **The Ω = 1 normaliser.** A cheap engineering test with a binary answer.
4. **Raising an agent.** A research line that uses the owner's background, and the one least developed in evidence.

In every case the money comes as a salary, a fellowship, a grant or a contract for the tests. There is no licence
revenue. The model of §5 keeps those streams, and its middle case assumes no commercial contract at all.

### 10.5 What the lab gets by engaging now

- **Its tests are designed before they run.** Each of the decisive tests above is written as a pre-registration with a
  surrogate gate, and every result is recorded, including the failures.
- **Early sight of a method that could remove a sweep** from continual fine-tuning, or turn "kill switch" into measurable
  quantities, and an honest early stop if it does not.
- **A researcher whose training is in how learners are raised.** That is the angle the lab's character and constitution work
  needs, and the one this repository's safety results keep pointing to.

### 10.6 Pitch discipline

| say | do not say |
|---|---|
| "in synthetic worlds, a pause that loses nothing gives an agent on its own clock no reason to resist, at every size we tried" | "we solved shutdown resistance" |
| "the normaliser survived a 16-fold change of units that broke a tuned weight, on a synthetic problem; on real streams it passed provisionally and failed one replication carrier" | "our continual-learning method beats the state of the art" |
| "CRR is a synthesis; its own commitments landed on known results in 56 of 80 checkable cases, three of them possibly new" | "CRR is confirmed in fifty fields" |
| "no result is yet PASS-1; here is the test that would make one" | any number not printed by a committed script |

> If a lab asks "what are you selling?", the honest answer is: a careful way of testing claims, two ideas worth testing
> on real AI systems, and a short list of experiments that would show quickly whether the ideas work. The careful testing
> is ready now. The ideas are promising in small pretend worlds. The lab would be paying to find out, fast and honestly,
> whether they work in the real ones.

## 11. The continual-learning method and the EPO application, in money terms

Added at the owner's request on 2026-09-23 (prompt-log entry 103). The owner asked for three things:
- to price the continual-learning benchmark results if they hold on GPU and LLM architectures;
- to re-read `Continuous_Learning/CONTINUOUS_LEARNING.md` for what the pipeline recorded as failures;
- to bring in the owner's European patent application.

The numbers come from a second model, `model/cl_patent.py`, whose output is pinned as `model/cl_patent.txt` (Appendix B).
It is separate from the model of §5, so nothing quoted earlier changes.

### 11.1 What the continual-learning record actually shows

The EWC arm of the rule was tested on nine unseen carriers in two pre-registered studies. In EQ2 and EQ3 together, the rule
at Ω = 1 was not behind the in-sample-tuned weight on 8 of 9 carriers. It was ahead on every one of those 8, by +0.6886 to
+4.0625 points.

The one carrier it was behind, fars, is a defect of the pipeline, not a verdict on the rule. The pre-registered subsample
left fars with class counts [0, 2086, 746, 15, 991, 688, 430, 45]: one class empty, so the first task had one class. On that
carrier every arm of the EWC family sat at chance. Set that carrier aside as uninformative and the rule was not behind on
8 of 8 informative carriers. That reading is **not** a ledger verdict. Under R6 the FAIL stands, and the class floor that
would test it is written into EQ4.

The failures the pipeline recorded fall into four kinds; one row, EQX-2, sits in two of them (CONTINUOUS_LEARNING.md §7.5;
`cl_patent.txt` [1]):

| kind | rows | what it means for money |
|---|---|---|
| a pre-registered "every carrier / every cell" criterion missed on one unit | 4: EQX-2, EQ3-1, EQ3-C, EQ3-A | mostly the strictness of the test; but EQ3-A is real: at a narrow network (width 64) the rule fell behind |
| a pre-registered control did not hold | 3: EQ2-4, EQ3-3, EQ3-4 | the *explanation* was wrong (the rule was predicted to be harmful on constraint-type past terms and often was not); the measurement was not |
| the theory value Ω = 1 did not appear | 3: EQX-2, EQ2-6, EQ3-6 | commercially this is the good news: Ω is a plateau (9 of 9 grid points within a step on four carriers), so the dial needs no tuning either |
| a pipeline defect, or a reduction to a constant | 2: EQ2R-VOID, EQX-1 | the void cost data, not evidence; the reduction is real: on replay the rule is a constant and worth nothing |

**One correction to the earlier framing.** The owner described the result as "the equanimity finding for optimal
learning". The mathematics says otherwise (CONTINUOUS_LEARNING.md §4.3):
- Ω = 1 is not a Bayes optimum. At exact gradients it stops wherever it first meets the Pareto curve.
- What the rule has is a bounded step. It can run the penalty past the point where a fixed weight diverges, and it needs
  no sweep.
- Its value is therefore *tuning-free and non-divergent*, not *optimal*, and that is what the estimate prices.

![The EWC arm on the nine unseen carriers: not behind on 8 of 9 as registered; the one miss is the carrier the pipeline's subsample broke.](figures/A10_cl_evidence.png)

**The properties that carry value, each from its pinned output:**
- **Compute.** On seen data, the rule needed 7.200e+04 sample passes against the tuned weight's 1.224e+06 over 17
  configurations. That is a ratio of 0.0588: a saving of 0.9412 of that sweep.
- **Invariance.** Across learning rate and batch size the rule was not behind in 5 of 5 cells (EQ3-I, PASS-0), while the
  tuned weight moved from 300 to 3000.
- **Scale.** On a synthetic problem under SGD, a 16-fold change in the past term's scale left the rule at 0.660 of the
  re-tuned weight's total loss. The fixed weight at its old setting diverged.
- **The Adam caution, the most important line for LLMs.** Under Adam, the fixed weight is scale-robust too. The rule's
  scale advantage is an SGD property. Most large models are trained with Adam-family optimisers.
- **Poisoned data.** The bounded rule EQ-B was ahead of the plain rule under poisoned batches on 6 of 6 carriers (by 2.64
  to 20.75 points). These were seen carriers, the run was exploratory, and it has no verdict. EQ4 is the held-out test.

> On nine new datasets the rule did as well as or better than a carefully hand-tuned setting eight times. The ninth time,
> our own sampling mistake had broken the dataset, and every method failed on it. So the rule works on this kind of
> problem, it saves the search for the right setting, and it never blows up. The catch is that big AI models are usually
> trained with a different kind of optimiser, and in our own maths check that optimiser already gives the hand-tuned
> setting most of the same protection.

### 11.2 What it would be worth if it held at GPU and LLM scale

**The model.** The value created is the compute a lab saves by not sweeping one weight. It is computed as:
- the experiment compute of the adopting labs, drawn between $4,500,000,000 (OpenAI's 2024 experiments, as reported) and
  $71,428,571,429 (two labs at a reported $50B each in 2026, times the 2024 R&D share: an assumption);
- times the share of that compute spent sweeping penalty, KL or anchor weights, an assumption drawn between 0.001 and 0.02;
- times the share of a sweep saved, between 0.8235 (a lab still runs 3 confirming configurations) and 0.9412 (the pinned
  ratio);
- grown up to 2.2000 a year (the reported training-cost projection).

**The technical tree.**
- P(a GPU study reaches PASS-1) = 0.2500, by Laplace's rule on the rule's own record of 0 PASS-1 in 2 held-out studies.
- P(the advantage survives Adam-trained LLMs, given a GPU pass) = 0.20. This is an assumption, set low because of the
  Adam caution.
- P(labs adopt, given an LLM pass) = 0.30, an assumption.
- Together: P(adopted by 2029) = 0.0150.

**The results.**

| quantity | lower | middle | upper |
|---|---|---|---|
| value in the field, 2029, if adopted | $38,285,915 | $232,739,581 | $1,413,980,686 |
| value in the field, 2030, if adopted | $48,481,151 | $347,819,511 | $2,484,196,052 |
| value in the field, 2029–2030, if adopted | $95,290,461 | $580,702,405 | $4,341,466,855 |

Weighted by the chance of getting there, the mean over all simulated futures for 2029–2030 is $21,289,825. In 0.0143 of
the futures the rule is adopted at all.

![If the rule transferred and were adopted, the saved compute is large; weighted by the chance that it does, it is modest.](figures/A11_cl_value.png)

**What moves it.** Whether the advantage survives Adam, and how much of their compute labs spend sweeping these weights:

| change | mean value created 2029–2030 | P(adopted) |
|---|---|---|
| registered | $21,289,825 | 0.0150 |
| GPU pass at the PASS-0 level (1 of 2) | $44,956,948 | 0.0300 |
| LLM transfer 0.05 (Adam removes the advantage) | $4,030,742 | 0.0037 |
| LLM transfer 0.5 | $56,277,153 | 0.0375 |
| sweep share 0.0005 to 0.005 | $6,632,646 | 0.0150 |
| sweep share 0.005 to 0.05 | $66,326,465 | 0.0150 |

![What moves the continual-learning value.](figures/A12_cl_sensitivity.png)

**How this compares with the estimate in chat of 2026-09-22.** That estimate is recorded in CONTINUOUS_LEARNING.md §9 as a
chat figure, not a repository number: "a few million to a few tens of millions of dollars a year of saved compute under
adoption". The committed model differs in two directions:
- **Higher if adopted.** Its conditional-on-adoption values are higher, because 2026 lab compute is reported at about $50B
  a lab.
- **Lower once weighted.** Its probability-weighted value is lower than any "under adoption" figure, because the tree now
  prices the Adam caution and the record's 0 PASS-1.

The fair single sentence is: **worth hundreds of millions of dollars a year to the field if it works at scale, and
$21,289,825 over 2029–2030 in expectation today**.

> If this trick worked inside the training of the biggest AI models, it could save those companies a lot of computer time,
> hundreds of millions of dollars a year. But there is a good chance it won't work there, because those models use a
> different kind of learning step. When you multiply "how much it could be worth" by "how likely it is", you get about twenty
> million dollars over two years. That is real money for the field, but most of it would be saved by the companies, not paid to us.

### 11.3 What it could mean for other domains

| domain | the same shape? | evidence in this repository | status |
|---|---|---|---|
| RLHF: the KL penalty to a reference policy | yes (β is the weight on the past) | none; the fair test is named: three KL arms (fixed β, an adaptive controller, Ω = 1 on the KL gradient) under SGD and Adam | untested |
| continual pretraining with an anchor (L2-SP, EWC) | yes | none at scale; the Adam caution applies | untested |
| safety preservation under fine-tuning (anchor constraints) | yes | the rule amplifies an extreme batch, so it is not a safety mechanism by itself; EQ-B addresses that | exploratory |
| on-device and edge learning with SGD | yes, and SGD is where the property lives | nearest to the tested instrument | untested; the most natural market |
| poisoned or adversarial data streams | yes | EQ-B ahead on 6 of 6 seen carriers | exploratory; EQ4 pending |
| federated personalisation | partly | gated and CLOSED: one global weight is never a step behind | no value found |
| replay-based continual learning | no (units already match) | EQX: reduces to a constant | no value |
| adaptive filtering (Kalman) | a fixed gain | Ω = 1 gives a gain that is optimal at one speed only | no value |

### 11.4 The EPO application and the applied use case

**What the owner reports** (owner's statement):
- a European patent application filed in August 2025, for CRR as a physical systems processor;
- an examiner who has agreed the claims in principle, and has asked for an applied use case.

**What the EPO looks for** (information, not legal advice; sources in Appendix E). Under the Guidelines for Examination,
G-II 3.3, a mathematical method contributes technical character when it is applied to a specific field of technology or
adapted to a specific technical implementation. "Controlling a technical system" in general is not enough. The Guidelines'
own AI examples include a neural network in a heart-monitoring apparatus that identifies irregular heartbeats, and the
classification of images, audio or speech from low-level features. Where a technical effect is established, computational
efficiency counts toward inventive step.

**Three facts that constrain any use case, stated plainly:**
1. **The pending application can only be amended within its content as filed** (Art. 123(2) EPC). A use case must already
   be disclosed in the August 2025 text, or be directly and unambiguously derivable from it. The repository's results can
   support a technical effect the application already encompasses: the Enlarged Board's decision G 2/21 allows post-filing
   evidence for such an effect (named, not fetched). They cannot add a new one.
2. **This repository is public, and has been since 2026-09-15.** In Europe there is no general grace period, so everything
   first published here is prior art against any *new* European filing. That includes the Ω rule and EQ-B, the
   pause-and-resume construction, the alternans and Bass results, and the bounded-memory estimator. In the US, a one-year
   grace period covers the inventor's own disclosures, so a US filing on matter first published on 2026-09-15 would have to
   be made no later than 2027-09-15.
3. **The Paris Convention priority year for filings elsewhere that claim the August 2025 date ended in August 2026.**

**Candidate applied use cases, mapped to the evidence** (for the owner's attorney to check against the application as
filed; not claims):

| use case | the CRR ingredient | the evidence here | fit with G-II 3.3 |
|---|---|---|---|
| cardiac rhythm monitoring or pacing with a bounded memory of settled beats | A6 (regeneration) with P3 weights | ADDS candidate: the alternans threshold moves from 1.0000 to 2.3333 at q = 0.4 (synthesis batch 12, row 2) | close to the Guidelines' own heart-monitoring example; Art. 53(c) excludes diagnostic methods practised on the body, not devices |
| an interruptible controller for an autonomous machine (robot, vehicle): a pause that loses nothing and an objective on the machine's own active steps | H-L5 (natural time), A3 (the cut has no content) | theorem on synthetic worlds from 12 to 768 states (`AI_Safety/checks/scale.txt`) | control of a specific physical system, if claimed specifically |
| drift-robust estimation for sensor streams (bounded mean in place of accumulated counts) | A6 | ADDS candidate: better than accumulation by +0.2025 in mean absolute error (synthesis batch 28, row 4) | signal processing of physical measurements |
| training controller for neural networks on accelerators: a step-bounded penalty weight that removes a sweep | H-EQ (Ω), EQ-B | PASS-0 on tabular data; compute ratio 0.0588 on seen data; the Adam caution | ML training in general is weak; stronger if tied to a specific technical application or hardware implementation |
| event segmentation of sensor signals at intrinsic-phase half-turns | A3 | mixed: H-L5 failed on measles; A3 undecided on projective carriers | a specific signal-processing use would be needed |

**How the model prices the patent.**
- The model multiplies three probabilities, all assumptions: an applied use case exists within the application as filed
  (0.50); grant given that use case (0.70, reflecting the owner's report); and the granted claims cover what a lab actually
  uses (0.10). The product is 0.0350.
- On the continual-learning path alone, a patent holder's mean capture over 2029–2030 is $1,130. Only 0.0004 of the
  simulated futures produce any income. In those futures it is $373,639 / $1,499,953 / $5,484,681 (lower / middle / upper).
- The cost side is at least EUR 5,250 in EPO renewal fees through year 7, before attorney, validation and national fees.
- **The honest conclusion.** As a way to capture the continual-learning value, the patent is a long shot. That is mainly
  because the method was developed and published here after the filing date. Its better use is as the vehicle for an
  applied use case the application already discloses, with the repository's results as supporting evidence. It is also a
  credential that strengthens the O-1 file (original contributions) and the pitch to the lab.

![The patent path as the model prices it, and the calendar that bears on it.](figures/A13_patent.png)

**What to do, in order** (information, not legal advice):
1. **Engage a European patent attorney now.** Take the application as filed, the examiner's communication, and this table.
2. **Ask the attorney before the next push** whether to pause publishing new methods in this public repository until any
   separate filings are decided. Every push is a publication.
3. **Decide by 2027-09-15** whether to file in the US on the matter first published here.

> The patent is like a claim ticket filed in August 2025. You can't add new things to the ticket now; you can only point to
> what was already written on it, and show proof that it works. Everything we've written in this project since then is
> public, and in Europe what's public can't be patented later, even by the person who wrote it. So the patent is most
> useful as a way to protect a use that the original ticket already describes, like a heart-monitoring device or a machine
> that can be safely paused. A lawyer who knows European patents needs to look at it soon.

### 11.5 What §11 changes in the plan

- **The earlier totals do not change.** The project funding and researcher compensation of §5 stand as computed.
- **The continual-learning method adds value to the field, mostly not to its author.** Its expected value to the field is
  about $21 million over 2029–2030 in this model. Most of it would be saved by the labs.
- **The author's route to that value** is a role or grant to run the decisive tests (the GPU study with SGD and Adam arms,
  and the three-arm KL test), and a patent only where the application as filed covers the use.
- **The next steps of §8 gain three items:** run EQ4; propose the GPU and KL tests as a funded project; take the EPO
  application to an attorney before the next push.

### 11.6 Addendum, 2026-09-23 (prompt-log entry 104): new evidence on the continual-learning method

This addendum was written after §11 and changes none of the model's inputs. The owner decides whether they should change.
The evidence is in `Continuous_Learning/ADAM_AND_PRIOR_ART.md` and `reports/eq4.md`. Every number below is pinned there.

- **Against a finely tuned constant, the rule loses where the scales differ.** On a fine grid of 60 weights, the rule's
  total is 1.186 to 2.073 times the best constant's at the mismatched scales, and 0.997 to 1.050 where they match
  (`adam_checks_3.txt` B5). The earlier advantage (0.660 at c = 16) was measured against a coarse 10-point grid.
- **The weight's form is published prior art.** Without its smoothing the rule is the VQGAN adaptive weight of 2020
  (`adam_checks_2.txt` B1: 7.7432 against 7.7434), and the registered smoothing costs at every scale tried.
- **Under Adam the rule has nothing to do** (A1–A3). Under heavy-ball momentum it is finite but behind (A8).
- **On real data (EQ4, plain SGD):**
  - the bounded rule is not behind the tuned λ on only 4 of 6 unseen carriers (EQ4-1 FAIL);
  - under poison a fixed weight with the same clip does as well (EQ4-3 FAIL);
  - the ER-sum control is violated.

**What this means for §11.2.** The scenario "the rule holds at GPU and LLM scale" now has no synthetic support for an
accuracy gain, and under Adam none is possible. What remains is a tuning-free stable weight under SGD-family training.
That is a tuning-cost saving which has not been measured, and it is shared with published methods.

The model's value-if-adopted figures ($232,739,581 for 2029 and $347,819,511 for 2030, middle case) price a scenario that
the evidence now argues against. Read them as a ceiling on a scenario the evidence does not support, not as a forecast.

**For the patent (information, not legal advice).** The ratio's form was published in 2020, before the August 2025 filing,
so accuracy cannot be the technical effect. The applied use case the owner asked for is examined separately, for the cut
δ(Now) as a rupture detector, in `Rupture_Detection/RUPTURE_DETECTION.md`.

**The rupture detector (the last row of the §11.4 table).** Its declared Phase-A battery closed its gate. On the positive
control, the cut-based detector was 14.458 times slower than the conventional peak detector. No chaotic carrier read AHEAD
in the main cell, and on an ECG-like beat the peak detector was 190.297 times faster. So the repository offers no evidence
of a technical effect for that use, and a heart-monitoring use case should not rest on it (`Rupture_Detection/`).

## Appendix A — the code

```include:Alexander Plan/model/projections.py
```

```include:Alexander Plan/model/cl_patent.py
```

```include:Alexander Plan/build/make_figures.py
```

The science scripts are `AI_Safety/checks/scale.py` and `AI_Safety/checks/combined.py`. They are reproduced in full in
Appendix A of `AI_Safety/AI_Safety.pdf`.

## Appendix B — the outputs, as pinned

```include:Alexander Plan/model/projections.txt
```

```include:Alexander Plan/model/cl_patent.txt
```

```include:Alexander Plan/figures/figures.txt
```

```include:AI_Safety/checks/scale.txt
```

## Appendix C — the decision log (AGENT_LOG entries 77–81, verbatim)

```include:notebook/AGENT_LOG.md:90-94
```

## Appendix D — the declaration of the new tests, verbatim

```include:AI_Safety/DECLARATION_3.md
```

## Appendix E — sources

```include:docs/citations/alexander_plan_2026-09-23.md
```
