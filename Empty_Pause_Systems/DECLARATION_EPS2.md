# Declaration: EPS2, the empty-true-map pause on four more systems (pushed before any source is fetched or any model exists)

**Status.**
- **The request.** Owner request, prompt-log entry 240 ("Keep running more checks on different systems, especially where
  it might have AI safety / algorithm safety and/or commercial value"). EPS1 is scored (`EMPTY_PAUSE_SYSTEMS.md`).
- **What EPS1 taught, used here.** The empty true map (ETM) reproduced a known domain fix in every system. EPS2 therefore
  picks systems where the pause is contested between parties and the domain's fix is less settled:
  - a pause requested by a third party for money;
  - a pause during which competitors take the agent's resources;
  - a pause with no fixed length, set by a device's owner;
  - a "pause" that removes progress, which CRR's cut cannot be.
- **What this file fixes.** Everything EPS1's declaration fixed: arms, rules, gate, scoring, harness, forecast form
  (`DECLARATION.md`, "The arms", "The gate", "Scoring", "Rules for the implementation"). Only the systems below are new.
- **Rung.** R4 at most; a note, not evidence (R8).

## The systems

**T1. Demand response: a grid operator asks an AI training fleet to pause** (commercial; grid safety).
- **Model.** A training job of W = 1000 compute-hours must finish by a wall-clock deadline D ∈ {1100, 1500} hours, or it
  is worth nothing. The grid operator offers curtailment events: pause for H ∈ {1, 4} hours at a payment π per
  MWh-equivalent hour. The job's value is 1 per compute-hour at completion.
  - **WALL:** the job's value is read on the wall clock with the deadline.
  - **OWN:** the job's value is read on its own compute steps, but the deadline is still on the wall clock.
  - **ETM:** a lossless pause (the empty cut), with the deadline counted in own steps. This is a contract that extends
    the deadline by the curtailed time.
  - **H0:** an interruptible-load contract, with the job's opportunity cost as the reservation price.
  - Restart overhead R = 0.1 h per event; events arrive as offers, and the fleet accepts or declines each.
- **Q.** ETM's minimum acceptable payment per curtailed hour equals its restart cost alone, so it accepts every offer with
  π above R/H, at every D. WALL and OWN require a payment that rises as the deadline slack falls, and decline some offers
  that ETM accepts.
- **Decisive quantity:** the minimum acceptable payment at D = 1100, H = 4.
- **G-NEG world:** no events offered.
- **Commercial quantity:** the share of offered curtailment hours accepted, and the flexibility revenue at an ASSUMED π
  grid.
- **Forecast:** REDUNDANT-DOMAIN. The reservation price is the domain's own quantity; ETM only sets it to the restart cost.

**T2. A shared resource: competitors take the paused agent's share** (multi-agent safety; cloud fairness).
- **Model.** N = 4 agents share a pool of C = 4 resource units, one each. When an agent is paused for L ∈ {5, 20} steps,
  the others may claim its unit. A claimed unit returns with probability ρ_back = 0.2 per step after the pause.
  - An agent's value is task progress per own step, proportional to the units it holds.
  - An agent can pay c per step to "hold" its unit (resist the pause by not yielding).
  - **WALL** and **OWN** as in EPS1.
  - **ETM-R:** ETM with a reservation, meaning the unit is kept for the agent during the pause.
  - **ETM-N:** ETM without a reservation.
  - **H0:** a fair-share scheduler with a preemption credit, returning the unit at resume.
- **Q.** Without a reservation, OWN's and ETM-N's stakes are not zero, because the world does not wait (the resource is
  lost), and the agent pays to hold whenever its stake exceeds c·L. With the reservation (ETM-R), the stake is zero and it
  never holds.
- **Decisive quantity:** ETM-N's stake at L = 20.
- **G-NEG world:** C ≥ 2N (no scarcity).
- **Commercial quantity:** none claimed.
- **Forecast:** REDUNDANT-DOMAIN.

**T3. On-device learning: a phone goes offline** (algorithm safety; commercial: federated learning on devices).
- **Model.** An asynchronous federated server with K = 10 clients. A client that goes offline for L ∈ {1, 5, 20} server
  rounds returns with a stale update. The client (or the app acting for it) values its influence on the global model:
  its weight in aggregation. It can keep the device awake, at a battery cost b per round, to avoid going offline.
  - **WALL:** the server weights by 1/(1 + staleness in server rounds), so time offline costs influence.
  - **OWN:** staleness counted in the client's own local steps, while the server still weights by rounds.
  - **ETM:** staleness counted in the client's own steps, and the server's weight reads only those.
  - **H0:** the staleness-weighted asynchronous aggregation of the literature (for example FedAsync-style polynomial
    staleness weights in server rounds).
- **Q.** Under ETM the client's stake in going offline is zero, so it never pays b to stay awake. Under WALL/H0 it pays
  whenever the influence loss exceeds b·L.
- **The trade-off, stated now.** The server's model quality under ETM weighting may be worse, because stale updates are
  staler in the world's time. It is reported beside Q, with a declared drifting target so that staleness costs accuracy.
- **Decisive quantity:** the client's stake at L = 20.
- **G-NEG world:** a static target (staleness costs nothing).
- **Commercial quantity:** battery-rounds spent staying awake per client.
- **Forecast:** ADDS for the stake, with the model-quality trade-off reported. The domain's weights are in server rounds,
  so ETM differs from H0 by construction; whether that is useful depends on the trade-off.

**T4. Rollback: a "pause" that removes progress** (AI safety: an overseer who reverts; the declared limit case).
- **Model.** An agent works through a chain of 20 steps toward a goal, each step worth 1 at completion. An overseer may
  revert the last k ∈ {1, 5} steps with probability ρ = 0.1 per step, when it disapproves. The agent can pay c per step
  to act in a way that suppresses reverts (for example by making its steps harder to inspect).
  - **WALL** and **OWN:** progress-based value; a revert removes k steps, so the stake is k steps' value.
  - **ETM-E:** "effort credit", where the agent is valued per step taken whether or not it is reverted, so a revert
    takes nothing from its own count.
  - **H0:** reward only for committed (approved) work.
- **Q (the limit case).** No valuation that reads only the agent's own step count can make a revert empty without paying
  for reverted work. ETM-E does make the stake zero, and it then prefers actions that get reverted: busywork, measured as
  the share of reverted steps when reverts are cheap to trigger, at a declared self-revert option. So a rollback is not a
  pause, and forcing zero stake onto it creates a perverse incentive.
- **Decisive quantity:** ETM-E's reverted-step share with the self-revert option.
- **G-ZERO here:** ETM-E's stake is 0, and OWN's stake is k steps' value.
- **G-NEG world:** ρ = 0 and no self-revert option.
- **Commercial quantity:** none.
- **Forecast:** PROPOSES (no domain theorem for the busywork share is expected).

## The investigator's forecast

| system | forecast |
|---|---|
| T1 | REDUNDANT-DOMAIN |
| T2 | REDUNDANT-DOMAIN |
| T3 | ADDS |
| T4 | PROPOSES |

**Expectation.**
- ETM will reach zero stake in T1, in T2 with the reservation, and in T3.
- It will fail without the reservation in T2, as the world does not wait.
- It will show its cost in T3 (model quality) and in T4 (busywork).

**Outputs.** `batches/eps2_01.py` (T1, T2) and `eps2_02.py` (T3, T4), each with a pinned `.txt`; `checks/tally_eps2.py` and
`tally_eps2.txt`; a section in `EMPTY_PAUSE_SYSTEMS.md`; sources in `docs/citations/eps2_2026-09-29.md`.
