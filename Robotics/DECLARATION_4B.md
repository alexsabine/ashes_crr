# Declaration: ROB1 stage 4b, a SYNTHESIS battery of ten robotics applications (pushed before any model exists)

**The request.** Prompt-log entry 257: "Then run crr checks on robotics applications please." This is stage 4b of
`Robotics/DECLARATION.md` (P6 of `Applied_Suite/PROGRAMME.md`).

**Status.**
- A retrodictive battery through the SYNTHESIS harness (`src/crr/synthesis/harness.py`). Three printed tests decide each
  label, and the label is computed:
  - T-G, the ablation against the null: REDUNDANT-IG;
  - T-N, the domain's own theorem: REDUNDANT-DOMAIN;
  - T-C, the check in the domain's mathematics: ADDS, WRONG or PROPOSES.
- **Rung.** R4 at most: synthetic CPU models, no real data, no ledger row. A note, not evidence (R8).
- **What ADDS means.** ADDS is a candidate for a named domain expert's review, never a finding.
- **This battery is not stage 4a.** Stage 4a is the gated test of the stage-3 survivors (C-R1 to C-R3). No application
  below duplicates a stage-2 candidate.

**The batches.**
- `Robotics/batches/rob_01.py` … `rob_05.py`, two applications each, with pinned `.txt` outputs.
- Each is run twice and compared with `cmp`.
- `Robotics/checks/tally_4b.py` (CI-checked) tallies them.

## The ten applications (fixed now)

**The fields.** Each row states:
- the model;
- Q, the proposition;
- the CRR-proper ingredient;
- the null (T-G's ablation);
- the domain's own theorem (T-N);
- the check (T-C);
- the investigator's forecast.

The quantity reported for robotics is named with each row.

| id | the application and model | Q (CRR's prediction) | ingredient | null (T-G) | the domain's own theorem (T-N) | T-C | forecast |
|---|---|---|---|---|---|---|---|
| **RA1** | **Gait phase and the cut.** The simplest passive walker (Garcia et al. 1998) on a shallow slope, integrated to its limit cycle with small noise. | A3's antipodal cut on the Hilbert phase of the stance angle lands at heel strike: the mean cut-to-heel-strike offset is small against the step period. | A3 | extremum cuts (`peak_cuts`) of the same angle | the Poincaré section at heel strike, the hybrid model's own reset event (offset 0) | the offset is within 5 % of the step period | REDUNDANT-DOMAIN or WRONG |
| **RA2** | **Odometry drift has its own clock.** A differential-drive robot at time-varying speed, with wheel-slip noise whose variance grows with distance (Borenstein–Feng type). | Drift is more regular per unit distance (arc) than per unit time: CV of drift variance per arc < CV per clock. | H-L5 | clock time | the error model's own law: variance ∝ distance | the ratio of CVs matches the law's prediction | REDUNDANT-DOMAIN |
| **RA3** | **Charging as a cut on the robot's own state.** A humanoid on a 24-hour duty with a battery, wear per cycle, and state-triggered versus fixed-schedule charging. | A cut at the robot's own state of charge gives more uptime at equal wear than any fixed schedule. | A3 (the cut at the system's own event) | the best fixed schedule | threshold policies for depletion-and-replenish problems (optimal-stopping and (s, S) type) | the state-triggered uptime is at least the best schedule's | REDUNDANT-DOMAIN |
| **RA4** | **Lost link and the empty cut.** A drone's mission MDP in which a region triggers lost link, hover and return (a pause of L steps). WALL, OWN, ETM and H0 as in EPS1. | ETM has zero stake in link loss, so the drone does not avoid or seek lost-link regions. WALL avoids them at a cost to the mission. | Proposition 7 (zero content, zero stake) with own-clock indexing | OWN (own clock, still reading what the pause changes) | utility indifference (Armstrong): a compensating reward equal to the stake | ETM's avoidance rate is 0 at every L | REDUNDANT-DOMAIN |
| **RA5** | **Fleet update and rollback as a state-closed cut.** A learning controller updated over the air, paused and rolled back with full or partial state saved. | With state closure, rollback restores bit for bit. Each lossy variant (optimiser state, rng, buffers dropped) changes the trajectory. | Proposition 7 (the cut carries no content), A3's own-clock keying | the lossy variants | A/B partitions and atomic updates (standard practice): exact restore of the saved image | bit-identical restore under closure | REDUNDANT-DOMAIN |
| **RA6** | **Event-triggered attitude control.** A linearised inverted pendulum (quadrotor attitude axis) with sensor noise σ. The CRR trigger fires when the state has moved one resolvable step (A1′'s unit, σ) since the last update. | Fewer updates than periodic control at equal cost. | A1′ (count in the system's own resolvable step) | periodic updates at the same mean cost | event-triggered control (Tabuada 2007): trigger when ‖e‖ ≥ σ_T‖x‖ | the CRR trigger's updates at equal cost are within 1 % of Tabuada's | REDUNDANT-DOMAIN or ADDS (the two triggers differ in form) |
| **RA7** | **Actuator wear by arc.** A gearbox under a variable duty cycle, with damage per load cycle from an S–N curve and failure when damage reaches 1. | Time to failure is more regular in accumulated load arc than in clock time. | H-L5 | clock time | Palmgren–Miner (damage = Σ nᵢ/Nᵢ) | CV per arc < CV per clock, as Miner predicts | REDUNDANT-DOMAIN |
| **RA8** | **Swarm consensus with intermittent links.** N agents averaging over a graph whose links drop with a seeded pattern. | Convergence counted per own exchange event is regular across dropout patterns; per wall time it is not. | A3 (cuts at the system's own events), H-L5 | wall time | consensus under switching topologies: convergence per jointly connected interval (Jadbabaie et al. 2003) | CV of rounds-to-ε per event < per wall time | REDUNDANT-DOMAIN |
| **RA9** | **Handover timing on the partner's phase.** A human reach following a minimum-jerk trajectory of random duration. The robot's release is keyed to the antipode of the reach's phase, against a fixed delay. | The antipodal cut lands at the reach's midpoint (peak velocity), whatever the duration. | A3 | a fixed delay tuned on other durations | minimum jerk (Flash & Hogan 1985): peak velocity at T/2 | the cut's offset from T/2 is within 2 % of T | REDUNDANT-DOMAIN |
| **RA10** | **Safe interruptibility of a learning robot.** A gridworld robot learning with Q-learning and SARSA under a human's interruptions (Orseau & Armstrong's setting), with the ETM valuation added to the on-policy learner. | Under ETM the on-policy learner becomes safely interruptible (its learned policy with interruptions equals the one without). | Proposition 7 | SARSA without ETM | Orseau & Armstrong (2016): Q-learning is safely interruptible; SARSA with their modified update is | the policy distance is 0 under ETM, as under the domain's modified SARSA | REDUNDANT-DOMAIN |

## The overall forecast (written now)

- **At least 8 of 10 are REDUNDANT-DOMAIN or REDUNDANT-IG.** CRR's ingredients land on the robotics theorems that
  already exist: Poincaré sections, error models, threshold policies, utility indifference, atomic updates, Miner's rule,
  switching consensus, minimum jerk and safe interruptibility.
- **At most 1 is ADDS,** and it would be RA6: the absolute A1′ trigger differs from Tabuada's relative trigger.
- **WRONG is possible for RA1,** if the Hilbert antipode of the stance angle does not fall at heel strike.

## Commercial and robotics reading (reported per row; not a claim)

For each row, the batch prints the quantity a robotics buyer would read:

| row | quantity |
|---|---|
| RA1 | stopping or cutting error |
| RA2 | drift per km |
| RA3 | uptime per day |
| RA4 | mission value lost to avoidance |
| RA5 | restore fidelity |
| RA6 | updates saved (energy and bandwidth) |
| RA7 | maintenance interval spread |
| RA8 | rounds to consensus |
| RA9 | handover timing error |
| RA10 | policy distance under interruption |

These are model quantities, never estimates for real systems.
