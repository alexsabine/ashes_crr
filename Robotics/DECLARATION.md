# Declaration: ROB1, the frontier bottlenecks of robotics and drones, double-checked, then read through CRR (pushed before any search)

**The request.** Prompt-log entry 257 (2026-09-30T07:11Z), P5 and P6 of `Applied_Suite/PROGRAMME.md`:
- "run crr checks applied to robotics including an array of frontier bottlenecks";
- "Check Aria and arxiv papers as well as news feeds, drone bottlenecks";
- "Double check their known bottlenecks before applying crr";
- "Then run crr checks on robotics applications".

**The method is OB1's** (`Open_Bottlenecks/DECLARATION.md`):
1. open bottlenecks first;
2. then CRR's points of disagreement;
3. then targeted prior art before any code;
4. then a synthetic gate that can close.

**One addition here: the double check.** Every bottleneck that stage 1 reads as open is attacked by a second, independent
agent, which tries to show it is solved or not open. This happens before any CRR reading.

## Stage 1: the harvest (five families; 2025–2026 sources first; one dossier each)

The dossiers are `docs/citations/rob1_r{1..5}_2026-09-30.md`. The claims are in `Robotics/checks/claims_r{1..5}.py`, in
OB1's format. Every quote is verified against its fetched text by `Robotics/checks/verify.py`. The raw texts live outside
the repository under `/tmp/claude-0/rob_src/`.

| family | scope |
|---|---|
| **R1: programmes** | ARIA (the UK Advanced Research and Invention Agency): its robotics programmes and opportunity spaces, with their stated targets and the reasons they give that the targets are not met today. Corroboration from other public programmes with stated robotics targets (DARPA, EU Horizon/euROBIN, NSF), where reachable. |
| **R2: robot learning** | Generalist and foundation robot policies (vision-language-action models), sim-to-real transfer, data scarcity, generalisation, long-horizon tasks, lifelong and continual robot learning (for example LIBERO-type benchmarks), and on-robot adaptation and forgetting (arXiv 2025–26 surveys, benchmarks and position papers). |
| **R3: drones** | Endurance and energy, GPS-denied state estimation and drift, perception in adverse conditions, agile flight and disturbance rejection, swarms and communication-denied operation, beyond-visual-line-of-sight operation and detect-and-avoid, lost-link and fail-safe behaviour, on-board compute, and counter-UAS. Sources are arXiv, regulators (FAA, EASA, CAA) and industry. |
| **R4: safety, trust and security** | Emergency stop and safe interruptibility of learned robot controllers, human–robot collaboration and humanoid safety standards, verification and runtime monitoring of learned policies, adversarial and jailbreak attacks on robot policies, the privacy of robots' sensor data, and cybersecurity of robot fleets. |
| **R5: news and industry feeds** | Deployment bottlenecks reported in 2025–26 (humanoids, warehouses, field robots and delivery drones): reliability and uptime, battery life, cost, dependence on teleoperation, and the cost of data collection. **A news claim enters only with a primary source**: a paper, a regulator, a standards body or a company's own statement. |

**The record for each bottleneck** (as OB1):

| field | content |
|---|---|
| B-a | a quote stating the problem |
| B-b | a 2025–26 quote stating that it is open, unsolved or a main challenge |
| B-c | the best result the sources report on a named benchmark or metric, against a target (a programme goal, a regulatory requirement, a human baseline or an oracle), with the numbers quoted |
| B-d | the method families tried, and the assumption each makes about time, clocks, boundaries, interruptions, memory or tuning |
| B-e | whether it can be tested on this machine's CPU (yes or no, and why) |

## Stage 1b: the double check (independent agents; before stage 2)

**The attack.** For each bottleneck read as open, a second agent that did not harvest it searches for the strongest
contrary evidence:
- a 2025–26 source reporting the target reached;
- a deployed system that does it;
- or a source saying that the bottleneck is misframed.

**The label, computed by `Robotics/checks/table.py`** from the two agents' verified claims:

| label | condition |
|---|---|
| **OPEN (double-checked)** | the B-a, B-b and B-c quotes are verified, and the check found no verified contrary claim |
| **CONTESTED** | a verified contrary claim exists, but it does not show the target reached on the named metric |
| **NOT OPEN** | a verified contrary claim shows the target reached |

## Stage 2: the CRR reading (the investigator; `Robotics/CRR_READING.md`; before any stage-3 search)

**For each OPEN or CONTESTED bottleneck:**
- **the CRR ingredient,** from `theory/CRR.md` only: A1′, A3/D5, A6, P2/P3, H-L5, D6/H-T1, H-EQ, A7/A8 and Proposition 7
  (the empty cut). The record's methods are named as what they are: SEC is a Laplace weight with a units calibration, not
  a CRR rule. The empty-true-map pause is Proposition 7's construction.
- **the frontier's assumption** (from B-d), and whether CRR agrees with it, denies it or is silent;
- **if CRR denies it,** the prediction: what a method on CRR's side does that the frontier's does not, as a direction or an
  inequality on the B-c metric.

**Labels:** DISAGREES (a candidate), RESTATES or SILENT.

**What the record already says, and must be respected:**
- The own-clock pause reduces to Wald's sequential test in energy terms (`Energy Design Principle/checks/clock_cut.txt`).
- Event-triggered control and usage-based maintenance are established literatures.
- Safe interruptibility is published (Orseau & Armstrong 2016).
- The own-step objective was compared with DReST (`AI_Safety/NT1/`).
- H-L5 failed on both real carriers it met (measles, the pulse).
- The empty pause's construction holds on real stacks (`Empty_Cut_Engineering/`, `Real_World/RW1.md`).

## Stage 3: targeted prior art (agents; before any code)

- **The search.** One search per DISAGREES candidate, for its specific mechanism: robotics, control and AI venues
  2023–2026, with verified quotes.
- **The grade:** REDUNDANT, PARTLY REDUNDANT, or NOT FOUND IN THE SWEEP.
- **Only NOT FOUND goes on,** or a PARTLY REDUNDANT candidate whose missing part is the part CRR predicts.

## Stage 4 (P6): the robotics application checks (each declared separately before code)

**4a. Gated simulations for the survivors of stage 3.**
- CPU simulations only (numpy/scipy): planar quadrotor, pendulum, cart-pole, planar arm, gridworld and fleet models.
- Each has the frontier method as its baseline, a must-fail control and a gate that can close.
- A pre-registration follows only if a gate opens, and its data step is on a later day (R3).

**4b. A declared SYNTHESIS battery on robotics applications** (as PRED70 and EPS1).
- The applications are named in a declaration pushed before any model. Each has CRR's prediction, its ingredient, the
  null, the domain's best model (H0) and the investigator's forecast.
- The applications are run through the SYNTHESIS harness (`src/crr/synthesis/harness.py`: T-G, T-N and T-C decide
  REDUNDANT-IG, REDUNDANT-DOMAIN, ADDS, WRONG or PROPOSES).
- They are tallied by a CI-checked script.

## Stop conditions (R12)

- If stage 2 reads nothing as DISAGREES, stage 4a does not run. The finding is recorded: "on the open robotics bottlenecks
  found, CRR has no point of disagreement with the frontier". Stage 4b still runs, as a retrodictive battery; it is not a
  test.
- If stage 3 finds every candidate published, stage 4a does not run, and the prior art is named.

## Forecasts (written now)

1. Stage 1 finds at least 15 bottlenecks with B-a, B-b and B-c quoted. After the double check, at least 10 remain OPEN
   and at least 2 are CONTESTED or NOT OPEN.
2. Stage 2 reads **at most 3** as DISAGREES. The likely points:
   - clock-indexed schedules (control rates, maintenance, replanning, learning-rate and consolidation schedules) where CRR
     indexes by the system's own change;
   - interruption and lost-link handling that changes the task's value, where Proposition 7's empty cut does not;
   - externally supplied task boundaries in lifelong robot learning.
3. Stage 3 finds most of those mechanisms published: event-triggered and self-triggered control, safe interruptibility,
   usage-based maintenance, task-free continual learning. At most one candidate reaches a gate.
4. Stage 4b grades most robotics applications REDUNDANT-DOMAIN or REDUNDANT-IG. ADDS, if any, is a candidate for expert
   review, never a finding.
