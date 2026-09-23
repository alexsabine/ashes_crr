# Alexander Plan/ — the owner's dossier

A dossier prepared at the owner's request on 2026-09-23 (prompt-log entry 101). It covers the AI-safety findings
(including the scale test run for it, `AI_Safety/checks/scale.py`), where the continual-learning work stands, the market
and the policy moment, a funding scenario model to 2030, the people and roles around the work, and an outline of an O-1
visa path. It is a note, not evidence (R8). The money figures come from a model, not a forecast. The O-1 section is
information, not legal advice.

| file | what it is |
|---|---|
| `Alexander_Plan.pdf` | the dossier, built from the Markdown source by `build/build_pdf.py`; byte-identical on rebuild |
| `ALEXANDER_PLAN.md` | the source, readable on GitHub; its appendices embed the model, its outputs, the decision-log entries, the declaration and the sources |
| `model/projections.py` and `.txt` | the scenario model: technical milestones anchored on the repository's record (Laplace), money figures from search summaries or named assumptions, 20000 seeded draws, lower/middle/upper = 10th/50th/90th percentiles, a sensitivity table |
| `figures/A01…A09.png` | the figures, drawn by `build/make_figures.py` from pinned outputs only (A08 and A09 are drawings of a plan and of a first reading, and say so); `figures/figures.txt` pins every number placed on them |
| `build/make_figures.py`, `build/build_pdf.py` | the figure script (the AI_Safety palette) and the PDF builder (a copy of AI_Safety's) |

Sources: `docs/citations/alexander_plan_2026-09-23.md`. These are search summaries, not fetched pages; check each figure
against its source before using it outside this repository. Decisions: AGENT_LOG entries 77–79.

Rebuild:

```
uv run python "Alexander Plan/model/projections.py" > "Alexander Plan/model/projections.txt"
uv run python "Alexander Plan/build/make_figures.py" > "Alexander Plan/figures/figures.txt"
uv run python "Alexander Plan/build/build_pdf.py"
```
