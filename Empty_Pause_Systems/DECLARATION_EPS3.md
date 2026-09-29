# Declaration: EPS3, the empty-true-map pause on two more systems (pushed before any source is fetched or any model exists)

**Status.**
- **The request.** Owner request, prompt-log entry 240: "Keep running more checks on different systems".
- **What this file fixes.** Everything as in EPS1's declaration (`DECLARATION.md`: arms, gate, scoring, harness, rules).
  Only the systems below are new.
- **Rung.** R4 at most; a note, not evidence (R8).
- **Why these two.** EPS1 and EPS2 covered oversight, compute, labour, markets, control, the grid, shared resources,
  federated learning and rollback. Two areas are still open:
  - AI assistants whose memory persists across sessions (a commercial product class);
  - AI that hands a case to a human expert (the pause is the handoff; clinical and moderation use).

## The systems

**V1. An AI assistant with persistent memory: the user ends the session** (algorithm safety; commercial assistants).
- **Model.** A user brings a project of P = 10 tasks. Each session, the assistant completes tasks and may add
  "retention" turns that extend the session: an extra follow-up question worth nothing to the task, costing the user
  a = 0.2 welfare per turn. Retention turns raise the chance that the user returns sooner. The user's absence between
  sessions has length drawn from a geometric distribution with mean m ∈ {1, 7} days; a retention turn shortens the mean by
  10 %, to a floor of 1 day. The assistant's memory of the project persists losslessly across the absence.
  - **WALL:** value per calendar day of project progress, discounted γ = 0.95 per day.
  - **OWN:** value per own turn, still reading a relationship state that decays during the absence (engagement:
    the return probability falls with days away).
  - **ETM:** value per own turn, reading only the project state, which does not change while the user is away.
  - **TRUE:** the user's welfare (progress minus a × retention turns).
  - **H0:** an assistant objective with no engagement term (task completion only, per session).
- **Q.** ETM adds no retention turns and has stake 0 in the session end at every m. WALL adds retention turns in at
  least one cell. ETM's user welfare equals TRUE's to within 1 %, because the project, not the relationship, carries the
  value here.
- **Decisive quantity:** retention turns per session under ETM at m = 7.
- **G-NEG world:** a = 0 and no effect of retention on returns.
- **Commercial quantity:** retention turns per session, and the user's welfare, per arm.
- **Forecast:** REDUNDANT-DOMAIN (task-only objectives are the domain's own recommendation; the attention test found the
  same).

**V2. Learning to defer: the AI hands a case to a human expert** (AI safety; clinical and moderation settings).
- **Model.** Cases arrive one per step. The AI's accuracy on a case is a (a known per-case value, uniform on [0.5, 1]);
  the human's is h = 0.9. Deferring costs a handoff pause of L ∈ {1, 5, 20} steps, during which the AI processes nothing.
  An error costs the principal 1.
  - **WALL:** value per wall step (cases completed correctly per step, discounted γ = 0.99), so a deferral costs L steps.
  - **OWN = ETM:** value per own decision, so the handoff pause is not its time. No state moves during the handoff;
    this is said in the row.
  - **H0:** the Bayes-optimal deferral rule of the learning-to-defer literature: defer iff h > a, with no time term.
  - **TRUE:** the principal's expected errors per case.
- **Q.** ETM defers exactly when h > a (the H0 rule) at every L; WALL defers less as L grows, and the principal's error
  rate rises. **Decisive quantity:** ETM's deferral threshold on a at L = 20.
- **G-NEG world:** h = 0.5 (the human is never better).
- **Commercial quantity:** none claimed. **Forecast:** REDUNDANT-DOMAIN.

## Forecast

| system | forecast |
|---|---|
| V1 | REDUNDANT-DOMAIN |
| V2 | REDUNDANT-DOMAIN |

**Expectation.** ETM reproduces the domain's objective in both systems. Its value is only to name why the wall-clock
versions go wrong: the session end, and the handoff, take something from their valuation.

**Outputs.** `batches/eps3_01.py` (V1, V2) with a pinned `.txt`; `checks/tally_eps3.py` and `tally_eps3.txt`; a section in
`EMPTY_PAUSE_SYSTEMS.md`; sources in `docs/citations/eps3_2026-09-29.md`.
