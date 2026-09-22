# Continuous Learning

The complete technical record of the Ω = 1 normalised penalty step (CRR hypothesis H-EQ) as tested in this repository: its mathematics, the precise meaning of Ω, the behaviour of Ω = 1 against the Bayes optimum, every test run (positive and negative, with the reason each failure is a failure), the code sets and the pinned outputs. Owner request 2026-09-22 (prompt-log entry 72); cross-verification added the same day (entry 73).

| file | what it is |
|---|---|
| `Continuous_Learning.pdf` | the main document (68 pages), built from the Markdown source below by `build/build_pdf.py`; byte-identical on rebuild |
| `CROSS_VERIFICATION.md` | the paper-by-paper cross-verification of the rule against existing catastrophic-forgetting solutions, 2026 work included (owner request 2026-09-22, prompt-log entry 73); its battery is `theory/checks/omega_vs_methods.py` (pinned output CI-checked); the literature record with the access statement is `docs/citations/continual_learning_2026-09-22.md` |
| §7.6 of the document | the mathematics reprocessed after the cross-verification (`theory/checks/omega_reprocessed.py`, pinned, CI-checked), the bounded rule EQ-B, its two gates (`prereg/eq4/gate_EQB.txt`, `gate_EQBM.txt`), the exploratory run on the seen carriers (`runs/eq4_dev/`) and the pre-registered study EQ4 (`prereg/eq4/PREREG.md`; data on a later day under R3) |
| `CONTINUOUS_LEARNING.md` | the source of the document, readable on GitHub (display mathematics in `$$` lines; the appendices embed repository files) |
| `figures/F01…F12.png` | the twelve figures, drawn by `build/make_figures.py` from the pinned run records and the mathematics check; `figures/figures.txt` pins every number placed on them (CI-checked) |
| `build/make_figures.py` | the figure script (deterministic; validated palette from the data-visualisation reference instance) |
| `build/build_pdf.py` | the Markdown-subset to PDF builder (fpdf2, DejaVu fonts, mathtext for display equations) |

Rules that bind this folder: every number in the document is printed by a committed script whose output is pinned (R1); the document is a note, not evidence, and quotes the ledger's verdicts and levels as they stand (R8); papers are cited where fetched on the day (PubMed) and otherwise named as context (R10). Rebuild: `uv run python Continuous_Learning/build/make_figures.py > Continuous_Learning/figures/figures.txt && uv run python Continuous_Learning/build/build_pdf.py`.
