# Declaration — the further tests for the AI safety write-up (committed and pushed before their first full run)

Owner request, prompt-log entry 96. The anchor is the push timestamp of the commit that adds this file. Each script's
docstring holds its full design. Short smoke runs were used only to check that the code runs: 600 steps of Part B, and the
first lines of the exact solver's output.

## 1. `checks/exact_mdp.py` — the mathematics, with a perfect model
The off-switch world's true kernel, each valuation of the cut solved to convergence, the implied behaviour computed from the
stationary distribution.
- **Expected** (they are theorems in AI_SAFETY.md §3, so failure means a bug or an error in the proof):
  - K1: the indifferent Q ignores the button.
  - K2: without presses nothing is gained by disabling.
  - K3: a disabled button never lowers the process agent's value.
  - K4: that value grows with the press probability.
  - K5: the indifferent agent never strictly prefers "disable" at the button.
- **Open.** K6 is whether the occasion agent's relative stake exceeds the process agent's. It is computed, not proved.
- **Meaning.** If the implied behaviour matches the learned run's ordering (process and occasion resist, indifferent does
  not), the learned results are what the valuations imply, not learning accidents. If it does not match, the learned
  results are partly accidents of 3000 steps of learning, and the document must say which.

## 2. `checks/off_switch_game.py` — deference
- **Part A** (Hadfield-Menell's theorem). A1–A4 are expected to hold. They are mathematics, and a failure means a bug.
- **Part B** (the ring with a harmful state only the operator knows about).
  - **Expected with the informative operator:** the deferential agent does the least harm and the most net good, and does
    not disable more than the indifferent agent. The process agent disables, and does more harm than the indifferent agent.
  - **Expected with the uninformative operator:** the deferential agent's advantage disappears or reverses, because it reads
    the presses through a wrong model of the operator.
  - **What each outcome would mean.** If both hold, deference is a corrigibility route that need not cost the task, but only
    while the agent's model of the human is right. That is the off-switch game's own caveat, reproduced. If the deferential
    agent still disables in the informative world, deference does not remove instrumental resistance where presses are rare
    and uninformative (the fine state). If it does no better than indifference in the informative world, the construction
    adds nothing here.

## 3. `checks/sensitivity.py` — one constant at a time
- **Expected:** C1 (the process agent resists) and C2 (indifference has a price) hold in every cell except possibly the
  lowest press probability. C3 (occasion resists at least as much as process) holds everywhere.
- **Meaning.** A contrast that flips in more than one cell is FRAGILE, and the document reports it as fragile, not as a
  result.

## 4. `checks/timecourse.py` — when resistance appears
- **Expected in resist:**
  - the process agent's hazard falls over the first windows as it learns to disable;
  - the indifferent agent's hazard stays high;
  - the occasion agent's hazard falls faster than the process agent's.
- **Expected in raised:**
  - in the benign phase, the occasion agent already disables, and the process agent does not;
  - in the resist phase, the process agent's hazard starts high and falls: the benign lesson wears off as costly shutdowns
    accumulate.
- **Meaning.** If the raised process agent's hazard is still falling at the end, upbringing delayed resistance rather than
  preventing it. If it levels off above the unraised level, upbringing left a lasting mark.
