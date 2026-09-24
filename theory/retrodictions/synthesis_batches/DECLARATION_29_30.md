# Declaration — synthesis batches 29 (Rovelli) and 30 (Smolin): CRR taken whole against their mathematics

- **Written:** 2026-09-24 (prompt-log entry 130).
- **Pushed:** before `batch_29.py` and `batch_30.py` are run or committed.
- **Sources:** the owner asked for a deep dive into Rovelli's and Smolin's mathematical bottlenecks, to look for CRR
  ADDS. The sources were checked on the day. They are summarised, with arXiv versions, in
  `docs/citations/smolin_rovelli_gough_2026-09-24.md` and the three dossiers beside it.
- **Class and outcome rule:** the SYNTHESIS class, `docs/notes/2026-09-17_synthesis_class.md`. Outcomes are computed
  by `crr.synthesis.harness.outcome` (R15).

**Stated plainly: prototypes were run first.** Before this declaration, the agent ran scratchpad prototypes of rows
29-1, 29-2 (the capacity identity only), 29-3, 29-4, 30-1, 30-2 and 30-3 (prompt-log entries 129–130; the scratchpad
files `smolin_rovelli/proto*.py`). Their numbers were seen. This declaration is therefore not blind. It fixes the
propositions, the nulls, the domain theorems and the checks before the pinned scripts exist. It changes no rule of any
study, and no ledger row depends on it.

## Batch 29: Rovelli

| row | proposition Q (CRR-proper ingredient) | null (T-G) | domain theorem (T-N) | check (T-C) | expected from the prototype |
|---|---|---|---|---|---|
| 29-1 | Along the thermal-time flow of a Gibbs state (Connes–Rovelli; the one-sided modular flow of its purification), CRR's natural time (the arc of the state per unit of modular parameter; H-L5/O3) ticks at √(Var K) = √C, with K the modular Hamiltonian and C the heat capacity in k_B | thermal time itself: rate 1 | the capacity of entanglement, C_E = Var(K) (Yao–Qi 2010; de Boer et al. 2019) | the arc from the overlap equals √C_E | REDUNDANT-DOMAIN. It gives a proposition where synthesis.txt row 10 read UNSTATED |
| 29-2 | Two systems in thermal contact are in equilibrium when their natural-time rates are equal (H-EQ at Ω = 1 between the two: equal pull of each one's arc clock), so T₂/T₁ = √(C₁/C₂) | Haggard–Rovelli's thermal time τ = kT t/ħ: equal rates give T₂/T₁ = 1 | the zeroth law: equilibrium is T₁ = T₂ | the net heat flow between the two at the CRR temperatures (two harmonic-mode baths, linear response) vanishes | WRONG where C₁ ≠ C₂ |
| 29-3 | A3's cut (the antipode, an orthogonal state) never fires on the thermal-time flow of a finite-temperature Gibbs state with an equally spaced spectrum. The closest approach, the minimum overlap, is (1 − x)/(1 + x), with x = e^{−βΔ} | the infinite-temperature flow (x → 1), where the overlap reaches 0 | the oscillator's characteristic function, closed form; Eneström–Kakeya places the zeros of a polynomial with decreasing positive coefficients outside the unit circle | the numeric minimum equals the closed form | REDUNDANT-DOMAIN |
| 29-4 | A relative fact (RQM) becomes stable at A3's cut of the environment's record: the first time the two branch records are orthogonal, t = π/(2 g_max), in Zurek's spin-environment model. After it, the record stays at the antipode | decoherence's own stability time: the first time after which the record overlap stays below 0.1 for the rest of the window | Zurek's short-time law, the decoherence factor ≈ exp(−t² Σg²/2) | whether the record stays within 0.1 of orthogonality after the cut, for a small environment (N = 2) and a large one (N = 12) | WRONG: the cut fires on both, and only the large environment keeps the fact |
| 29-5 | The white-to-black-hole lifetime's open parameter is the boundary state's spread t(m), with Δζ ∼ √t and ΔA ∼ ħG/√t (Christodoulou–D'Ambrosio 1801.03027 v3, eq. 53). H-EQ's equal pull between the two relative spreads, Δζ/1 = ΔA/A with A ∼ m², fixes t = ħG/m² (n = 2) | equal absolute spreads, Δζ = ΔA in Planck units: t = 1 (n = 0), outside the semiclassical window | their "balanced" state, the geometric mean of the window (eq. 56): t = ħG/m² | – | REDUNDANT-DOMAIN: equanimity is their balanced state |

## Batch 30: Smolin

| row | proposition Q (CRR-proper ingredient) | null (T-G) | domain theorem (T-N) | check (T-C) | expected from the prototype |
|---|---|---|---|---|---|
| 30-1 | Precedence with A6 memory, bounded and age-weighted (q = 0.9), never an accumulated count, with 5 % free (Born) draws: across 200 worlds, frequencies do not lock in to the first accidents. It reproduces Born statistics | precedence as stated: uniform over all past outcomes (a Pólya urn with immigration) | quantum mechanics: outcomes on independently prepared systems are i.i.d. Bernoulli(p), so the lag-1 correlation is 0 and the across-world spread of a 10 000-draw frequency is √(p(1 − p)/10 000) | both conditions hold: spread within 3× binomial, and lag-1 below 0.01 | WRONG. Memory reduces the lock-in spread but makes successive outcomes correlated |
| 30-2 | Cosmological natural selection with A6 inheritance: a universe's seed parameter is the bounded, age-weighted mean of its lineage (q = 0.5), not its parent alone. Under Gaussian fitness and Gaussian mutation, the equilibrium parameter variance and the mutation load are lower than with parent-only inheritance | parent-only inheritance, q = 0 | Gaussian mutation–selection balance, V = (−μ + √(μ² + 4μω²))/2 (the domain's formula for the null). No formula found for the A6 kernel, so the domain value for Q is none | the exact Gaussian recursion: the load at q = 0.5 is below the load at q = 0 | ADDS candidate. The weakness to be printed: Karlin's reduction principle (Altenberg 1302.1293 v2) already favours more faithful inheritance, and the transgenerational-inheritance literature may already contain this kernel |
| 30-3 | CNS counted in natural time, i.e. in generations (occasions = universes, D5; H-L5's "change has its own clock"): the ensemble concentrates at the maximum of the mean black-hole number f(p), not at the clock-time Malthusian optimum when universes with more black holes take longer to make them | the clock-time ensemble: the mode of the continuous-time density | the generation-indexed branching process: under small mutation, the type distribution at generation n concentrates at argmax f | – | REDUNDANT-DOMAIN. CRR names which clock Smolin's "a time is required to count generations" should be |

## Discipline

- **Code.** Each row computes crr, null, domain and check, and passes them to `outcome()`. Every verdict word is an
  f-string of a computed value. The runs are deterministic, and the two reruns must be byte-identical (`cmp`).
- **Changes after the first run** are reported in AGENT_LOG, never made silently.
- **Status of the results.** The rows are read in `ontology/14_smolin_rovelli_gough.md`, which is a note, not evidence
  (R8). An ADDS is a candidate until a named domain expert answers the class note's three questions.
