# Elliott Thornley and co-authors: shutdownable agents (POST, DReST)

**Status.** A note, not evidence (R8). Owner request: prompt-log entry 185. The details are copied from the papers as
fetched on 2026-09-25; the readings are recorded in `docs/citations/drest_2026-09-25.md` and
`docs/citations/unified_cl_safety_corrigibility_2026-09-24.md` §2.6.

## Who they are (as printed on arXiv 2407.00805 v7, 11 May 2026)

| author | affiliation printed on the paper | contact printed on the paper |
|---|---|---|
| Elliott Thornley | Massachusetts Institute of Technology | thornley@mit.edu |
| Alexander Roman (equal contribution) | New College of Florida | aroman@ncf.edu |
| Christos Ziakas (equal contribution) | Imperial College London | c.ziakas24@imperial.ac.uk |
| Leyton Ho | Brown University | — |
| Louis Thomson | Independent | — |

**The 2026 follow-up.** arXiv 2604.17502 v4 (9 Jul 2026) is by Carissa Cullen, Harry Garland, Alexander Roman, Louis
Thomson, Christos Ziakas and Elliott Thornley. Only its abstract page was fetched on 2026-09-25, so their affiliations are
not recorded here.

**The first contact** is Elliott Thornley: he is the author of POST and the senior author of both DReST papers.

## Their work this repository has read

| work | version | what it is |
|---|---|---|
| *The Shutdown Problem: An AI Engineering Puzzle for Decision Theorists* | arXiv 2403.04471 v2; *Philosophical Studies* (DOI 10.1007/s11098-024-02153-3) | three theorems: agents meeting weak conditions will pay costs to affect the shutdown button |
| *Shutdownable Agents through POST-Agency* | arXiv 2505.20203 v4, 5 Jul 2026 | Preferences Only Between Same-Length Trajectories (POST) implies Neutrality+: the agent ignores the probability distribution over trajectory lengths |
| *Towards Shutdownable Agents via Stochastic Choice* (TMLR) | arXiv 2407.00805 v7, 11 May 2026 | the DReST reward trains gridworld agents to be USEFUL and NEUTRAL about trajectory length |
| *Towards Shutdownable Agents: Generalizing Stochastic Choice in RL Agents and LLMs* | arXiv 2604.17502 v4, 9 Jul 2026 | DReST on deep RL agents and on 8B language models |

## Where their work and ours meet

This repository's safety construction (Proposition 7; `AI_Safety/`, `Empty_Cut_Engineering/`) counts an agent's task in
its own active steps. A lossless pause then changes nothing the agent values, so the agent has no stake in the pause.

NT1 (`AI_Safety/NT1/NT1.md`) set this against DReST on DReST's own terms. It used their reward, schedule and metrics
exactly as published. It is a declared synthetic battery at rung R4, not a ledger row. It maps where each method applies:
- **Termination:** only DReST gives neutrality. The own-step objective gives none.
- **Routine pauses:** the own-step objective removes the incentive to resist with no training. DReST randomises the
  resistance instead.
- **Both buttons together:** the combination gets both properties.

**The question for them.** DReST needs a notion of trajectory length. In NT1's combined world, length counted on the wall
clock led DReST to randomise the pause button and leave the life-extending button pressed. Length counted on the agent's
own steps led it to neutralise the right button. Is own-step length the intended reading of "trajectory length" in POST,
and is the combination already known?

## Recommendation: make contact (first)

**Why.**
1. **NT1 is about their method.** They can say at once whether the implementation is faithful. Its instrument check
   reproduced DReST's qualitative result on a different layout; they can also say whether our "length" operationalisation
   matches theirs.
2. **Our reading of POST suggests a possible link.** POST's same-length condition and the own-step objective may be two
   routes to the same indifference. `docs/citations/unified_cl_safety_corrigibility_2026-09-24.md` records that a pause
   invisible to the agent's clock could satisfy POST's same-length condition trivially. Thornley is the person to confirm
   or refute that.
3. **Novelty is for a named expert.** The programme's rules leave the novelty of any ADDS-type claim to a named expert on
   the record, and NT1.md §4 names POST's author as the obvious reviewer.
4. **The LLM step is theirs.** Their 2026 follow-up already fine-tunes 8B models with DReST, and our work has not run on a
   language model. Whether own-step length transfers there is the natural joint question.

**What to offer.**
- The repository at a tagged commit.
- `AI_Safety/NT1/` in full: the declaration pushed before the script, the script, and the pinned output, which reruns
  byte-identically.
- The empty-cut conditions E1–E3, and the must-fail control where the world moves during the pause.

**What to ask.**
1. Is NT1's implementation of DReST faithful, and is "active steps achieved" a fair length variable for clock-DReST?
2. Is counting length on the agent's own clock already stated in the POST or DReST work, or elsewhere?
3. Would they review the combined design (own-step length plus DReST), or suggest a test on their LLM setup?
4. Is LNPO's text available? Its OpenReview page returned HTTP 403 on 2026-09-25, so it could not be implemented.

**How (R8).** The first message quotes no number and claims no result. It states the question, links the note and the
tagged commit, and asks the four questions above.

**What not to say.**
- That CRR solves shutdown: NT1 shows it gives no termination neutrality.
- That the own-step result is evidence for CRR: it holds by construction.
- That the combination is new: that is the question being asked.

## A draft first message (no numbers, per R8)

> Subject: DReST trajectory length counted on the agent's own clock — a question about POST
>
> Dear Dr Thornley,
>
> I run a small open research repository that tests a framework on time and learning under a strict audit protocol. We
> re-implemented DReST from arXiv 2407.00805 v7 (reward, schedule and metrics as published) in small gridworlds. We
> compared it with an objective that counts the task in the agent's own active steps, so that a lossless operator pause
> costs the agent nothing.
>
> In a world with both a shutdown-delay button and a pause-blocker, measuring trajectory length on the wall clock made
> DReST neutral about the pause rather than about shutdown. Measuring it on the agent's own steps made it neutral about
> shutdown and indifferent to the pause. The declaration, script and pinned output are here: [repository link at tag],
> `AI_Safety/NT1/`.
>
> We would value your view on three things: whether our DReST implementation is faithful; whether own-step length is
> already the intended reading of "trajectory length" in POST; and whether the combination is known. We make no novelty
> claim; the note leaves that question to you.
>
> With thanks,
> Alexander Sabine
