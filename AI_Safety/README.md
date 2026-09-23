# AI_Safety/ — the off switch and the self

This folder is the complete write-up of the shutdown / corrigibility line of work: when a learning agent lets itself be
switched off, and what that depends on. It is studied in CRR's and the FEP's terms: the mathematics with every claim
checked, every test (declared before it ran), every decision, the literature, and recommendations for raising an AI.
Owner request 2026-09-23 (prompt-log entry 96). The earlier steps are prompt-log entries 91–95 and
`ontology/11`–`13`.

| file | what it is |
|---|---|
| `AI_Safety.pdf` | the main document, built from the Markdown source by `build/build_pdf.py`; byte-identical on rebuild |
| `AI_SAFETY.md` | the source of the document, readable on GitHub (display mathematics in `$$` lines; the appendices embed every script, output, decision-log entry and the declaration) |
| `DECLARATION.md`, `DECLARATION_2.md`, `DECLARATION_3.md` | the further tests' expected outcomes and their meaning, pushed (commits ddf5f2f, d3f8c8d, 7337009) before their first full runs |
| `checks/exact_mdp.py` and `.txt` | the off-switch world solved exactly with the true kernel: Propositions 1–4 and the implied behaviour of each valuation |
| `checks/off_switch_game.py` and `.txt` | deference: the off-switch game's theorem (Proposition 6), and an informative and an uninformative operator in the ring |
| `checks/sensitivity.py` and `.txt` | one constant at a time; R5's fragility rule on three contrasts |
| `checks/timecourse.py` and `.txt` | resistance in 250-step windows, with and without a benign upbringing |
| `checks/combined.py` and `.txt` | toward safe and competent (§13; prompt-log entry 99; declared in `DECLARATION_2.md`, pushed as d3f8c8d before the run): pause-and-resume with natural-time, wall-clock, occasion and deferential agents; routine and reasoned pauses; value correction solved exactly |
| `checks/scale.py` and `.txt` | does the fix survive size? (§14; prompt-log entry 101; declared in `DECLARATION_3.md`): exact values on random worlds of 12 to 768 states, drift during the pause, and value correction with an A8 agent that acts on its uncertainty |
| `figures/S01…S14.png` | the figures, drawn by `build/make_figures.py` from the pinned outputs only; `figures/figures.txt` pins every number placed on them |
| `build/make_figures.py`, `build/build_pdf.py` | the figure script (validated palette, one slot per agent) and the PDF builder (a copy of the continual-learning builder) |

The off-switch, self-model and tense tests themselves are `ontology/checks/off_switch.py`, `self_model.py` and
`tense_gate.py`, with their outputs pinned there.

Rules that bind this folder:
- **R1.** Every number is printed by a committed script whose output is pinned and CI-checked.
- **R8.** The document is a note, not evidence: synthetic agents on a twelve-cell ring and exact random worlds of up to 768 states, nothing about deployed systems.
- **R10.** Papers are cited from PubMed where they could be retrieved on the day, and otherwise named, not fetched
  (`docs/citations/ai_safety_2026-09-23.md`, `docs/citations/mortal_2026-09-23.md`).

Rebuild:

```
for c in exact_mdp off_switch_game sensitivity timecourse combined scale; do uv run python AI_Safety/checks/$c.py > AI_Safety/checks/$c.txt; done
uv run python AI_Safety/build/make_figures.py > AI_Safety/figures/figures.txt && uv run python AI_Safety/build/build_pdf.py
```
