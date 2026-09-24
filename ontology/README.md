# ontology/ — CRR's commitments, what the pipeline did to them, and what comes next

Written 2026-09-21 at the owner's direction (prompt-log entry 65) and extended 2026-09-22 (entries 66 and 67). This folder is a set of notes to the
auditor and the owner, not evidence: nothing here is a result, every number here is printed by a
committed script (the pinned battery outputs under `theory/retrodictions/`, the ledger, and the one
check script in `checks/`), and every external work is named by author and year as context only,
not fetched, per R10. The one curated document of this repository remains `ledger/LEDGER.md`.

## What is in the folder

| file | what it does |
|---|---|
| `01_the_cut.md` | the finding this folder starts from: CRR's Now, as computed, needs the future; with citations to the pinned rows and a fifth-grader explanation of each step |
| `02_commitments.md` | the six metaphysical commitments of CRR v3.1, unpacked against philosophy, contemplative traditions and metaphysics, and sorted into what is testable and what is not |
| `03_review_of_findings.md` | a fair review of everything the repository has found: ledger studies, gates, 197 retrodiction rows, 138 synthesis runs, corrections, instrument findings, the elegance ledger |
| `04_falsifiability_and_metaphysics.md` | what making CRR falsifiable has so far done to its metaphysics, and what remains outside any test |
| `05_next_steps.md` | the programme: a causal instrument, a gate for tense, the v3.2 decision list, the studies, and what would count as the metaphysics being found |
| `06_cut_as_content.md` | the mathematical reasons the cut carries content when the axiom says it is empty, and what that suggests about mathematics, machines and number theory |
| `checks/cut_on_a_machine.py` and `.txt` | the five small facts about boundaries in finite arithmetic that file 06 quotes; deterministic, pinned, CI-checked |
| `07_turing_safety_ingression.md` | CRR run on Turing systems, AI safety and platonic ingression; Watson's natural induction and Levin's sorting and ingression; the philosophical traditions; the owner's conjecture on forms as choices through time and on finitude (prompt-log entry 66) |
| `08_exploratory_genesis.md` | **EXPLORATORY** (prompt-log entry 67): from emptiness with CRR as stated; the line, the circle, π, the sine and the integers appear from one posited distinction and one posited motion; regeneration stops the first universe at 1/2; nine changes CRR would need; no gate, no verdict |
| `checks/genesis_from_emptiness.py` and `.txt` | the computations file 08 quotes, each 'change required' printed where a computation returned nothing, raised or stayed fixed; deterministic, pinned, CI-checked |
| `09_free_energy_principle.md` | the free-energy principle read with CRR (prompt-log entries 77–78): the clock against the domain's own clock (batch 27: 0 ADDS / 2 REDUNDANT-IG / 1 REDUNDANT-DOMAIN / 2 WRONG), the Dirac boundary, Ω = 1 as equanimity, precision as a measurable, A6 against Dirichlet accumulation, curiosity as a chord (batch 28: 1 ADDS / 1 PROPOSES / 3 WRONG); rows in `theory/retrodictions/synthesis_batches/batch_27.py`, `batch_28.py`; literature in `docs/citations/fep_2026-09-22.md` |
| `10_fep_and_crr.md` | FEP and CRR side by side (prompt-log entry 79): time as nested blankets against nested occasions, Markovian and non-Markovian commitments, the tallies read plainly (41 CONSIST / 86 DESCR of 197; 84 of 138 synthesis runs redundant, 3 ADDS candidates in 148), the ontological, metaphysical and contemplative comparison, whether the FEP says when a model must end, the content of the future in each, and a design for the tense gate; no new computation |
| `checks/delta_now.py` and `.txt` | the re-check of file 09 §5: A3's delta(Now) is a delta in the phase (one cut per half-turn on every speed profile; the time spacing varies), row 28-1's delta was the FEP's likelihood delta on a belief with no rotor; the strong form C·Ω = 1 is the removed spec law, and the registered rule degrades one grid step above Ω = 1 without diverging; deterministic, pinned, CI-checked |
| `11_tense_test.md` | the tense test (prompt-log entry 91): what it can and cannot test (no program can show the future has content; A7 holds for every program), then A8's operational shadow: a valence-free A6 regenerator against an active-inference planner on four worlds; the planner is ahead by a resolvable margin on drift and switch, a weak tie on delayed, not decidable on the martingale; the separating test (a regenerator that carries a forecast) is named, not run |
| `checks/tense_gate.py` and `.txt` | the computations file 11 quotes: gate (martingale tie, drift planner ahead), the table, the floor per world, the sensitivity; deterministic, pinned, CI-checked |
| `12_self_representation.md` | the self-representation test (prompt-log entries 92–93), declared before it ran: a self-model with no given goal, acting to postpone its own ending, closes most of the regenerator's gap to the planner (the rest confounded by exploration); representing its own in-flight actions helps narrowly; equanimity (Ω = 1) is a midpoint, never the best balance, and reduces to a fixed equal weight; leaning on the imagined future buys persistence and costs surprise at its own ending; a phenomenological exploration marked as interpretation |
| `checks/self_model.py` and `.txt` | the computations file 12 quotes; imports the tense test's worlds unchanged; deterministic, pinned, CI-checked |
| `13_mortal_computation_and_safety.md` | mortal computation (Ororbia and Friston), the von Neumann split and self-modelling in FEP and CRR terms; neuromorphic substrates and agents in the world; the contemplative reading of egoic representation through time; existential AI safety for CRR, the FEP / active inference and other predictive world models; the equanimity rule read again; raising an agent (prompt-log entry 94); the off-switch test, declared before it ran: a task alone produces resistance with no ego, only a contentless cut (A3) is corrigible and it costs task, equanimity between task and self is not corrigibility, mortality blocks learned but not built-in resistance, a benign upbringing helps only a process-identified agent |
| `checks/off_switch.py` and `.txt` | the computations file 13 quotes; deterministic, pinned, CI-checked; literature in `docs/citations/mortal_2026-09-23.md` |
| `../AI_Safety/` | the full write-up of files 11–13's safety line (prompt-log entry 96): the mathematics checked, four further tests declared before they ran (exact solution, deference, sensitivity, time course), recommendations for raising an AI, and the contemplative comparisons under an explicit legitimacy rule |
| `14_smolin_rovelli_gough.md` | Smolin, Rovelli and Gough through CRR (prompt-log entry 130): the physics and the metaphysics, and a search for CRR ADDS in Rovelli's and Smolin's mathematical bottlenecks; synthesis batches 29 (Rovelli: 0 ADDS / 3 REDUNDANT-DOMAIN / 2 WRONG) and 30 (Smolin: 1 ADDS candidate / 1 REDUNDANT-DOMAIN / 1 WRONG), declared first in `DECLARATION_29_30.md`; dossiers in `docs/citations/*_dossier_2026-09-24.md` |
| `15_grammar_to_theory.md` | what CRR is, epistemically, and how it could become a theory (prompt-log entries 134-136): a framework theory with explanatory unification and consilience of retrodictions but no corroborated novel fact (69 of 97 landing; 0 of 109 dynamics supplied; 0 clean novelties after the literature check); five routes from grammar to theory, the regeneration law q* = 1 - K(v) (O1) recommended, with a mathematical theory of regeneration in parallel; book titles; recommended next steps |
| `checks/turing_safety_ingression.py` and `.txt` | the nine SYNTHESIS-class rows file 07 quotes (0 ADDS / 2 REDUNDANT-IG / 4 REDUNDANT-DOMAIN / 1 WRONG / 1 INTERNAL / 1 UNSTATED); deterministic, pinned, CI-checked; literature in `docs/citations/ontology_2026-09-21.md` |

## The whole folder in one paragraph

CRR says the world proceeds by occasions: stretches of change measured in the system's own unit,
each ended by a cut that has no duration and no content, seeded from a settled past by re-weighting
rather than counting, with a future that has no content at all. Three hundred and thirty-five
computed rows across some fifty fields found that the part of CRR everyone shares, the geometry of
distinguishability, is present wherever there is a statistical description, which is a theorem and
not a discovery; that the parts that are CRR's own were either restatements of the field, wrong
where the field accumulates or has an extremum, or not yet one rule; and that the cut, the very
thing the theory says is empty, is computed from the future and carries a measurable content in
every implementation. That last fact is not a defeat. It is the first place where an axiom about
time was turned into a number that an instrument can get wrong, and it forces a choice the theory
has not yet made.

## For a fifth grader

Imagine a story told one page at a time. CRR says every page ends at a line, and the line itself is
nothing: no words on it, no time spent on it. We built a machine to find where the lines go. It
turned out the machine had to peek at the next page to decide where the line on this page went, and
the line always took up a little bit of the page. So either the line is not really nothing, or we
need a different machine that can find the line without peeking. This folder is about that, and
about what it means for a theory that says the future is blank.
