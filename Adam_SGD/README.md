# Adam / SGD

The Ω = 1 equanimity rule re-examined under the optimisers that matter (plain SGD, heavy-ball momentum, Adam coupled and
decoupled). The earlier assumptions about the value of a fixed parameter are audited first, and the rule then gets the test
it was never given: a world in which the right weight moves. Owner request, prompt-log entry 107.

A note, not evidence (R8). Every battery is declared and pushed before it runs, and every number is printed by a pinned
script.

| file | what it is |
|---|---|
| `DECLARATION_1.md` | the assumption audit: which objective, which noise, selection bias, the step size as a fixed parameter; the lessons that bind the next battery |
| `checks/common.py` | shared trajectory code (the two-task quadratic of `theory/checks/omega_sweeps.py`, with the scale's reading and the noise made explicit) |
| `checks/assumptions.py` | the audit (AS1–AS6); pinned output `checks/assumptions.txt` |
| `DECLARATION_2.md` | the drifting-world battery: a gate (a stationary world where the rule must not win, a drifting-units world where it must) and four realistic worlds (wandering units, a calibrated eight-task sequence, a miscalibrated one, a low-signal past gradient) under SGD, momentum and Adam coupled and decoupled |
| `checks/engine.py` | the batched engine (all weights and seeds at once, paired random draws; reproduces `common.run`) |
| `checks/drift_battery.py` | the battery; pinned output `checks/drift_battery.txt` |
| `checks/drift_battery.txt` | Declaration 2's output as it fell: GATE CLOSED (no headroom in the must-win world; grid edges) |
| `DECLARATION_3.md` | the redesigned gate, POST HOC: a headroom precondition, grids widened both ways with edge flags; everything else unchanged |
| `checks/drift_battery_2.py` | the redesigned battery; pinned output `checks/drift_battery_2.txt` |
