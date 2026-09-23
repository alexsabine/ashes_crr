# Safe_and_Continual/ — how the agents are modelled, where they fail and why

This folder is the comprehensive write-up asked for in prompt-log entry 122. It covers:
- the AI-safety agents and the continual-learning rules of this repository, with figures;
- the mathematics as each model implements it, and where each model fails and why;
- CRR as a heuristic that selected existing mathematics;
- the passes and the epistemic ladder, briefly;
- existing methods, references and next steps;
- every line of pipeline code behind these results;
- a glossary before §0 (what "no ego", "no self" and "equanimity" mean here, and how the literature uses the terms), and
  boxes "For the technical reader" in the register of corrigibility and continual-learning research (prompt-log entry 123).

It is a note, not evidence (R8).

| file | what it is |
|---|---|
| `Safe_and_Continual.pdf` | the document, built from the Markdown source by `build/build_pdf.py`; byte-identical on rebuild |
| `SAFE_AND_CONTINUAL.md` | the source, readable on GitHub; Appendix A embeds every script, Appendix B the key pinned outputs |
| `DECLARATION.md` | the round-off audit's declaration, pushed (commit c9f85bb) before its learned reruns |
| `checks/roundoff_audit.py` and `.txt` | the audit of the equal-pull agents' ratio guard (AGENT_LOG 100). It recomputes the affected lines of `exact_mdp`, `self_through_time`, `off_switch` and `self_model` with the pinned guard and with a round-off tolerance, side by side. The earlier scripts and outputs are unedited |
| `figures/F01…F14.png` | drawn by `build/make_figures.py` from the pinned outputs only; `figures/figures.txt` pins every number placed on them. The document also reuses `AI_Safety/figures/S01, S12, S14` and `Epistemic_Review/figures/E01` |
| `build/make_figures.py`, `build/build_pdf.py` | the figure script (validated palette, one slot per agent) and the PDF builder. The builder is a copy of `AI_Safety/build/build_pdf.py` with nested lists, rule-skipping, markup stripping in boxes and tables, and a second box type ('>> ', for the technical reader) |

Rules that bind this folder:
- **R1.** Every number is printed by a committed script whose output is pinned and CI-checked.
- **R8.** A note, not evidence. The AI-safety half is synthetic (rung R4); the continual-learning half quotes ledger rows
  at their own rungs.
- **R10.** `docs/citations/safe_and_continual_2026-09-23.md`.

Rebuild:

```
uv run python Safe_and_Continual/checks/roundoff_audit.py > Safe_and_Continual/checks/roundoff_audit.txt
uv run python Safe_and_Continual/build/make_figures.py > Safe_and_Continual/figures/figures.txt
uv run python Safe_and_Continual/build/build_pdf.py
```
