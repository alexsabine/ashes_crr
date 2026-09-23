# Epistemic_Review/ — what a PASS means here

The owner asked for this review on 2026-09-23 (prompt-log entry 102). It places every result in the repository on one
ladder of epistemic rungs, computed from the pinned outputs and the ledger. It defines every label (SHARP, CONSIST, DESCR,
FAILS, TENSION, OPEN, the synthesis outcomes, and the PASS levels), and computes why SHARP was unreachable (the FLOW audit).
It shows the ADDS dimension, reads CRR and the FEP on time (including the AI-safety clock result), and proposes the ladder
as a reporting rule. It is a note, not evidence (R8). It adds no ledger row and edits no earlier file.

| file | what it is |
|---|---|
| `Epistemic_Review.pdf` | the review, built from the Markdown source by `build/build_pdf.py`; byte-identical on rebuild |
| `EPISTEMIC_REVIEW.md` | the source, readable on GitHub; its appendices embed the script, its output and the decision-log entry |
| `checks/ladder.py` and `.txt` | the ladder: battery grades and the FLOW audit, synthesis outcomes and the CONSIST/DESCR crosswalk, the retrodictive hit rate, the per-commitment table, every ledger row allocated, the AI-safety record by kind |
| `figures/E01…E05.png`, `figures/figures.txt` | the figures, drawn by `build/make_figures.py` from `ladder.txt` only; `figures.txt` pins every number placed on them |

Decision: AGENT_LOG entry 80. Rebuild:

```
uv run python Epistemic_Review/checks/ladder.py > Epistemic_Review/checks/ladder.txt
uv run python Epistemic_Review/build/make_figures.py > Epistemic_Review/figures/figures.txt
uv run python Epistemic_Review/build/build_pdf.py
```
