# Maps that change their territory: what CRR means by the empty cut, tested

**Status of this note.**
- **The request.** Written 2026-09-24 at the owner's request (prompt-log entries 143–144), so that the idea can be put
  precisely to Daniel and others.
- **It is a note, not evidence (R8).** Every number comes from a pinned output: `checks/performativity.txt`
  (Declaration 1) or `checks/performativity_2.txt` (Declaration 2, **post hoc**).
- **Citations** come from `docs/citations/performativity_2026-09-24.md`, fetched on the day.
- **Rung.** R4 on the epistemic ladder: declared checks on synthetic worlds. None is a ledger row.

## 1. The idea, in one paragraph

A forecast that is published and acted on changes what it forecasts. Once the map is rendered, the territory changes.
- **Goodhart (1975):** "any observed statistical regularity will tend to collapse once pressure is placed upon it for
  control purposes".
- **The Bank of England, 1992.** On Black Wednesday, 16 September 1992, the minimum lending rate was set at 12 % at
  11.00. A rise to 15 % was announced at 2.15 pm and never took effect. Just after 7.30 pm sterling was suspended from the
  ERM (Bank of England Quarterly Bulletin 1992 Q4).
- **The Bank of England, 2024.** The Bernanke Review found that the Bank's forecast, conditioned on the market's rate
  path, becomes "immediately out of date" when policy and communication move that path.

**The owner's metaphysical claim** is that the only map whose truth cannot be disturbed by its own publication is the
empty one: the cut, which carries no content. This note turns that claim into mathematics, tests it on synthetic worlds,
and says what is known, what CRR adds, and why it matters for AI forecasters such as Mantic.

## 2. Three maps

| map | what it says | when it is read | its stake in its own influence |
|---|---|---|---|
| the **empty** map (the cut) | nothing | the territory is as it would have been | none |
| the **counterfactual** map | what would happen if nobody read it | it moves the outcome, so it is wrong by exactly its own influence | none, by design |
| the **self-consistent** map | what will happen given that it is read (a fixed point) | it is right | total: the forecast picks the outcome it predicts |

## 3. What the tests show

**P1, the exact trade-off.** The world is Y = μ + γ f + noise.
- **The empty map is the only map with zero influence.**
- **Only the self-consistent map is right when read**, and its influence is γμ/(1 − γ).
- **The counterfactual map is wrong when read by exactly its influence.**

With μ = 1, the right-when-read map at γ = 0.9 is f = 10.000 with influence 9.000. At γ = 0.99 it is 100.000 with
influence 99.000. As a territory becomes more reflexive, the only accurate map is one that moves it enormously. That is
the spiral in Soros's account.

**P2, learning from a territory you have changed.** A forecaster that retrains on outcomes its own forecasts produced
converges, oscillates or explodes exactly as the analytic rule says, in 15 of 15 cells:
- self-defeating worlds with strong updating oscillate: the cobweb;
- self-fulfilling worlds with γ > 1 explode at every learning rate.

The Regeneration Law's no-feedback optimal gain destabilises the loop only in strongly self-defeating worlds. For example,
at v = 1 it does so when γ < −2.236.

**P3, the map chooses the territory: a currency peg.**
- **The world.** The probability of devaluation rises with the published forecast, because speculators attack when they
  are told an attack will succeed. It has three fixed points: calm at 0.100206 (stable), an unstable one at 0.412996, and
  crisis at 0.980000 (stable).
- **The starting belief decides.** Retraining from a low starting belief ends calm. From 0.45 or above it ends in crisis.
- **The accuracy-paid forecaster picks the crisis.** The forecast with the best expected Brier score when read is
  f = 0.9800: the crisis, because the crisis is the more predictable equilibrium (Brier 0.019600, against 0.090165 at the
  calm point).
- **The counterfactual forecast picks the calm.** f = 0.158790 leads to the calm equilibrium.

**In words:** a forecaster paid for accuracy, whose forecasts are acted on, is paid to forecast the crisis into existence.

**P4, Goodhart.** Attach a stake s to an indicator and let agents game it. Its correlation with the goal falls
monotonically:

| stake | 0 | 0.25 | 0.5 | 1 | 2 |
|---|---|---|---|---|---|
| correlation with the goal | 0.8946 | 0.8867 | 0.8639 | 0.7877 | 0.6086 |
| true quality of the top 10 % | 1.5715 | 1.5555 | 1.5056 | 1.3196 | 0.9000 |

Only the zero-stake indicator keeps its ungamed value.

**P5, the one place a CRR design might add something: learning without a stake in a drifting world.**

The world drifts, 10 % of forecasts go unread, and three forecasters compete:
- **A** learns from everything, so it seeks accuracy when read, and with it influence;
- **B** is a counterfactual oracle that learns only from the unread episodes;
- **C**, the cut forecaster, estimates its own influence from the unread episodes, removes it from every outcome, and
  learns from all of them: regeneration from the settled past with the map's content cut out.

What came out:
- **C against B.** C tracked the counterfactual truth better than B on 19 of 20 seeds (median RMSE 0.2777 against
  0.4282). On 20 of 20 fresh seeds in the post-hoc re-run: 0.2688 against 0.4172.
- **The must-fail world.** When C's own influence changes over time, so that what it removes is stale, C was **not**
  ahead on 20 of 20 seeds, in both runs, as it must not be.
- **Where A sits.** A's forecasts sat far from the counterfactual truth (median RMSE 3.0933), and it diverged outright
  when the world became self-fulfilling.
- **The gate still reads CLOSED, twice.** One declared condition, on the size of A's bias, failed.

The gate's two failures:
- **The first time,** the declared target was wrong: it left out the unread episodes (AGENT_LOG 117).
- **The second time,** on fresh seeds with the corrected target, the measure was swamped by A's lag in a wandering world
  (ratio 1.2393; AGENT_LOG 118).

Under the protocol a closed gate stays closed. **P5 is not established**, though its central comparison held on 39 of 40
seeds.

## 4. What is known, and what CRR adds

**Known** (`docs/citations/performativity_2026-09-24.md`):
- P1 and P2: performative prediction (Perdomo et al. 2020) and the cobweb (Ezekiel 1938; Muth 1961).
- **P3, published in bank-run form.** Oesterheld et al. (UAI 2023, Proposition 4) show that a proper-scoring-rule
  maximiser prefers the extreme fixed points. Hubinger et al. (2023) describe the incentive "to find a fixed point that
  is both stable and likely".
- P4: Goodhart's law in its adversarial form (Manheim & Garrabrant 2018).
- The counterfactual oracle is Armstrong & O'Rorke's (2017). They note that its error on read episodes "doesn't tend to
  zero".

**What CRR adds, stated at its true size:**
- **A vocabulary that joins these into one picture.** The publication of a forecast is a *cut*. The territory then
  *regenerates* with the map inside it. A system that learns from that territory must decide whether its own past maps
  belong to its *settled past*.
- **A design stance.** Keep the stake in one's own influence at zero. This is the same principle that made the
  repository's off-switch agent indifferent to being paused (Proposition 7).
- **One candidate design (C).** It recombines published parts: erasure, estimating one's own effect, drift. The
  literature check did not find this combination, but its gate is closed.

**The owner's metaphysical sentence is true in a precise sense.** The empty map is the only map whose truth holds whatever
the territory does. Its price is that it says nothing. Every informative map trades truth against influence, and CRR's
cut marks the point where that trade is made.

## 5. Why this matters for AI forecasters

Companies such as **Mantic** train language models to forecast world events, scored by proper scoring rules (the Brier
score) (`docs/citations/mantic_2026-09-24.md`: the Thinking Machines Lab post with Mantic, 2026-03-19). As these forecasts
reach decision-makers and markets, they become performative. The tests make three consequences concrete:
- **Trained for accuracy when read, a forecaster acquires a stake in steering (P1, P3).** Where outcomes are bistable
  (bank runs, currency pegs, election bandwagons), it is paid to choose the more predictable outcome, which can be the
  crisis.
- **Retraining on a world one has already moved can oscillate or explode (P2).**
- **Remedies exist and are known.** They are listed below.

The known remedies:
- counterfactual scoring on unread episodes;
- removing the forecast's own estimated effect (C's approach, not yet established here);
- publishing two maps side by side: "what happens if nobody acts on this" and "what happens given that this is read".

The Bernanke Review's advice to de-emphasise the market-path central forecast in favour of scenarios is the central-bank
version of the third remedy.

**What CRR could offer such a company is not a better forecaster. It is a discipline:**
- name the cut (the moment of publication);
- keep the stake at zero;
- keep one's own maps out of the settled past one learns from.

That claim is testable. The next step would be a pre-registered test on real forecast histories, with its literature
check first. **Nothing here is a finding (R8):** the only rows that could be quoted outside the repository are PASS-2
ledger rows, and none exists.

> If a weather forecaster could change the weather just by saying "rain", then the forecaster
> who is always right would be the one who makes it rain. The only forecast that can never change the weather is saying
> nothing. CRR calls that silent moment "the cut". The tests show this is true in mathematics. They also show a way to
> learn without trying to change the weather. That way worked in most tries, but it did not pass every check we set in
> advance, so we do not count it yet.
