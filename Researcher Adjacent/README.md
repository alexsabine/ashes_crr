# Researcher Adjacent

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 185, "make a folder in the repo called Researcher
Adjacent and add the Thornley and FOREVER group details in there please. Recommendation to make contact."

**What this folder is.** It lists research groups whose published work sits next to this repository's work closely enough
that contact is worth making. For each group it records:
- who they are, as printed on their papers;
- which of their work this repository has read and used;
- where their work and this repository's meet;
- a recommendation on contact, including what to offer and what to ask.

**Where the details come from.**
- Every name, affiliation and contact address is copied from the paper's own author block as fetched on 2026-09-25.
- Each paper's full reading is recorded in `docs/citations/` (R10).
- Affiliations change, so check each group's current page before writing.
- No contact has been made. The owner decides whether and when to write.

| group | their work used here | our work that meets it | page |
|---|---|---|---|
| Elliott Thornley and co-authors (shutdownable agents: POST, DReST) | DReST, arXiv 2407.00805 v7; POST, arXiv 2505.20203 v4 | `AI_Safety/NT1/` (own-step objective against DReST); the own-step construction (Proposition 7) | [THORNLEY_GROUP.md](THORNLEY_GROUP.md) |
| Yujie Feng, Xiao-Ming Wu and co-authors (FOREVER) | FOREVER, arXiv 2601.03938 v2 | `Continuous_Learning/FOREVER/` (the mathematics, the comparative battery, the safe pause) | [FOREVER_GROUP.md](FOREVER_GROUP.md) |

## The rule for any message sent from this work (R8)

CLAUDE.md R8 says any external document, email included, "quotes the ledger or nothing".
- **The results these groups would care about are not ledger rows.** NT1, the comparative battery and the safe-pause
  checks are declared synthetic batteries at rung R4, recorded as notes.
- **The ledger has no PASS-2.** Nothing in this repository may be quoted outside it as a finding.

So a first message should:
- describe the question, not claim a result;
- quote no number;
- link the repository at a tagged commit and the note it concerns;
- ask the reviewer's question: is this new, is it correct, and where does it fail?

That is also the review the programme needs: `AI_Safety/NT1/NT1.md` §4 leaves the novelty question to a named expert.

## Order of contact recommended

1. **Thornley's group first.** NT1 bears directly on their method. It raises a concrete question they are best placed to
   answer: should DReST's trajectory length be counted on the agent's own clock? It also opens the expert review that
   `AI_Safety/NT1/NT1.md` §4 already names ("POST's author is the obvious reviewer").
2. **The FOREVER group second.** What we offer them is a precise, implementation-level safety checklist for their method.
   It is useful to them, but it is engineering, not a claim about their results. Their continual-learning results stand as
   published, and in our miniatures the Fisher-arc clock tied FOREVER's clock in all seven worlds
   (`Continuous_Learning/FOREVER/COMPARATIVE.md`, arm C1).
