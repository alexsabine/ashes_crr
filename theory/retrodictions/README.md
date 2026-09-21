# CRR retrodiction battery (issue #21) — reading

Script: `crr_retrodictions.py`. Output: `crr_retrodictions.txt` (committed; CI checks the
script reproduces it byte for byte). Every number below is in that file. Rules followed are
those of issue #21: one Python function per system, five grades plus OPEN, a symmetry check
wherever a result could hold by symmetry, at least four systems per class, and a `BORROWED`
field naming the mathematics inherited from the domain plus a `FLOW` field naming what
supplies the velocity inside the coherence integral C = ∫ √(ẋᵀ g ẋ) dt.

## Grade reading, accepted 2026-09-18

The grades printed by the battery scripts are frozen with their pinned outputs. They are now read
as two labels (`docs/notes/2026-09-18_sharp_regime_review.md` §3): *kind* (DEF / INHERITED / CLASS /
COMPARATIVE) × *outcome* (AGREES / DISAGREES / SILENT / INTERNAL). CONSIST is INHERITED-AGREES
except where a row says the regularity is dynamical (the adder, the heteroclinic cycle,
FitzHugh–Nagumo under drive), which are CLASS-AGREES; DESCR is DEF-AGREES; FAILS is DISAGREES with
rule 4's reason; OPEN is SILENT; TENSION is INTERNAL. SHARP is retired for retrodictions: no CRR
row can reach it, because every coherence integral has a system-supplied velocity and every unit
is the system's own. The only forward-looking label is PROSPECTIVE CANDIDATE (the note's §3.2),
which is a ticket to a prereg and not evidence. A fourth kind, SYNTHESIS (prompt-log entry 60,
`docs/notes/2026-09-17_synthesis_class.md`, harness `synthesis.py`), asks a different question of a
row: not whether CRR agrees with the domain but whether CRR, taken whole, adds a checkable statement
the domain's own mathematics does not already contain; its outcomes are ADDS (candidate) / PROPOSES /
REDUNDANT-IG / REDUNDANT-DOMAIN / WRONG / INTERNAL / UNSTATED, computed from printed numbers.

## Tally

| class | SHARP | CONSIST | DESCR | FAILS | TENSION | OPEN |
|---|---|---|---|---|---|---|
| (a) two-state / occupancy | 0 | 2 | 1 | 1 | 0 | 0 |
| (b) quantum | 0 | 2 | 0 | 1 | 0 | 1 |
| (c) thermal | 0 | 3 | 0 | 1 | 0 | 0 |
| (d) estimation / filtering | 0 | 1 | 2 | 0 | 1 | 0 |
| (e) oscillators | 0 | 0 | 3 | 1 | 0 | 0 |
| (f) point processes / natural time | 0 | 1 | 2 | 0 | 0 | 1 |
| (g) gravitational / cosmological | 0 | 0 | 2 | 0 | 0 | 2 |
| (h) bifurcations / criticality | 0 | 1 | 0 | 2 | 0 | 1 |
| all (32) | 0 | 10 | 10 | 6 | 1 | 5 |

## Where the mathematics is borrowed, and what supplies the flow

Every one of the 32 rows borrows its metric or its distance from the domain: the Bernoulli and
Poisson Fisher metrics and their variance-stabilising coordinates (arcsine, square root); the
Fubini–Study angle; thermodynamic length (energy variance as the metric); the Riccati equation;
inverse-variance weighting; the analytic-signal phase; the elliptic-integral period; Onsager's
specific heat; post-Newtonian phase evolution. CRR supplies the *name* of the quantity (arc,
chord, surplus, cut, unit) and, where it exists, the occasion structure.

The coherence integral never supplies its own velocity. In 25 of 32 rows the ẋ inside C comes
from the system: mass-action rate constants, a voltage ramp, an incidence curve, a Hamiltonian,
a cooling or stiffness protocol, a Kalman recursion, the data order of a stream, a waveform, a
drive, an event rate, an orbit, a chirp, a normal form. In the remaining rows there is no flow
because there is no dynamics in the question (a static family, an orthogonality fact, a carrier
that does not exist). So "C on system X" is always "the domain's own equation of motion, read
in the domain's own Fisher metric, summed as arc length": the reading is CRR's, the rate is not.

## Reading by class

**(a) Occupancy.** Two CONSIST rows (two-state kinetics, Poisson counts) where C is the
arcsine or square-root transform the domain already uses; one DESCR (a channel ramp); one
FAILS: the "p = 1/2 antipode" of the issue text is the antipode of the boundary start only,
the Bernoulli manifold being an interval. v3.1 does not make that claim.

**(b) Quantum.** The π pulse is a geodesic to the orthogonal state (CONSIST, the time is the
Hamiltonian's); the Anandan–Aharonov speed limit is the triangle inequality C ≥ D in the
Fubini–Study metric (CONSIST, and the sharpest inherited identity in the battery); a qutrit has
no unique antipode (OPEN, as the spec's A2c says); "mixed states never cut" is false for
rank-deficient states (FAILS as universal).

**(c) Thermal.** Thermodynamic length of a two-level system is π/2 and the minimum-dissipation
protocol is the constant-speed geodesic, S = 0 (both CONSIST, both Crooks/Sivak/Salamon–Berry
results wearing CRR's names). The criticality claim of the issue text splits: mean-field Ising
and the Landau family have a finite Fisher metric at the transition (FAILS as universal), the
2-D Ising model has a logarithmic divergence (CONSIST, class-dependent).

**(d) Estimation.** Kalman K(1) = 1/φ is the Riccati solution (CONSIST); Fisher additivity and
the posterior-mean surplus are definitions (DESCR); and the one TENSION of the battery: the
issue text's A9 ("equal precision, never a ratio of pull magnitudes") and v3.1's H-EQ (a ratio
of gradient norms) are different laws, disagreeing whenever magnitudes are not precisions, with
the norm-ratio form unbounded as the past pull vanishes. Study EQ2's pass (ledger EQ2-1) lives
in that unbounded regime (cap 1e4) and is therefore not a test of the spec's equanimity law.

**(e) Oscillators.** Three DESCR rows (arc per half-turn is 2A; equal half-turn arcs hold only
by symmetry, which v3.1 already says; the pendulum with amplitude jitter is clock-regular like
measles) and one FAILS: "change has its own clock" cannot be derived, because period jitter
and amplitude jitter put a system in opposite classes and nothing in the axioms picks one. v3.1
says the same thing more quietly; the slogan overstates.

**(f) Point processes.** Natural time is a definition (DESCR); Omori's P5 is calculus (CONSIST);
the exponential-kernel Hawkes process is Markov in its intensity, so the depth-one gate must
return "no salience effect" (DESCR) — the spec's A4 is what stops the e^S law from making a
false prediction here; Varotsos's κ₁ = 0.070 is untouched by any clause (OPEN).

**(g) Gravitational.** Nothing but DESCR and OPEN: an ellipse's half-turns are equal by
reflection symmetry (and the Euclidean metric is not a Fisher metric, so A1 does not even
license the row); the chirp is phase-regular by definition of the cut; cosmology has a Fisher
metric but no occasion; spacetime has no statistical family. This class yields no CRR content.

**(h) Bifurcations.** Hopf amplitude scaling gives ρ → 0 only with the resolution held fixed
(CONSIST, conditional); the Kalman depth of an AR(1) state stays finite as its relaxation rate
goes to zero (FAILS for the issue text's D8; v3.1's O1 already declines); the Landau family's
Fisher information is finite through the bifurcation (FAILS as universal); period doubling has
no carrier (OPEN).

## The second battery (Daniel Friedman, PR #24)

Daniel ran the same task independently: `crr_retrodictions.py` at the repository root, output
pinned at `runs/phaseA/crr_retrodictions.txt`, 40 systems (5 per class). His tally: 0 SHARP,
14 CONSIST, 8 DESCR, 2 FAILS, 5 TENSION, 11 OPEN. The two batteries were written without
sight of each other and agree on the headline (no SHARP row anywhere; the gravitational class
has no content; the thermal and estimation classes are Fisher machinery on home ground) and on
one FAILS (the Bernoulli `p = 1/2` antipode as a pole-anchored special case). His battery also
fails the Rabi cut on the detuned member; this one grades the same trajectory CONSIST, as the
quantum speed limit (P1), rather than as an A3 claim. They differ in what they grade TENSION: his
finds four clause collisions inside the issue-#21 text's A3 family and between D1 and P6 and
D8 and A3; this one finds the collision between the two laws named "equanimity". Read together,
the framework's self-collisions are all in the clauses v3.1 does not carry (the issue text's
criticality and antipode parentheticals) plus the one v3.1 does (H-EQ against the spec's A9).
CI reproduces this battery byte for byte and Daniel's verdict by verdict (his Rössler row's return-time statistics drift at the third decimal across Python patch versions, as the chaotic gate rows do; the verdict does not).

## The external "SHARP" claims, re-run here (owner upload, 2026-09-17)

A third run, done outside this repository by another instance of the same model and supplied
as a PDF (`theory/external/CRR_retrodiction_outcomes_1_external_2026-09-17.pdf`, script not
supplied), reported 16 SHARP rows over 42 systems. `sharp_claims.py` re-derives each of its 15
unique SHARP claims (Schwarzschild, de Sitter and the Page point are cross-listed, and the
saddle-node repeats D8), reproduces every printed number (15/15), and applies the issue's
rules to the claim as stated. Result: **SHARP 0, CONSIST 6, DESCR 5, FAILS 4** (output pinned
in `sharp_claims.txt`).

- The seven occupancy rows (half-life, logistic inflection, K_M, pKa, Fermi level, laser
  threshold, Langmuir) share one premise: the Bernoulli half-turn from a pole is at p = 1/2
  for every monotone curve, so the prediction cannot come out otherwise (rule 3). Five of the
  seven coincide with a *definition* made at one-half (half-life, K_M, pKa, μ, K_ads): DESCR.
  Two fail on an asymmetric member (rule 4): the logistic inflection is at K/2 but Gompertz's
  is at K/e and Richards' moves with its exponent; and a two-level carrier cannot be inverted
  at all, while a real laser's threshold sits above the antipode by an amount the cavity sets.
- The quantum rows: the Mandelstam–Tamm saturation is the resonant (geodesic) member only,
  off resonance the framework has the bound (P1), which is Anandan–Aharonov's (CONSIST); the
  spin-j antipode at angle π holds for the highest-weight state and fails for |1, 0⟩, which
  never reaches an antipode under the same rotation (FAILS, rule 4); the neutrino row restates
  the two-flavour formula (CONSIST).
- Thermodynamic length (CONSIST, Salamon–Berry); the Schwarzschild and de Sitter rejections
  are the known negative heat capacity, i.e. the known absence of a canonical ensemble, with
  the microcanonical description still admissible, so nothing "forces the unitary side"
  (CONSIST); the memory-depth divergence exists only under the own-unit reading of the
  observation variance and vanishes at fixed instrument noise (CONSIST, rule 2, as rows 30 and
  h1 of the two batteries found); the Page point is the half-entropy point by definition, and
  "cut at half the count" is a rule v3.1's O3 and the spec's A2c do not allow (FAILS).

Three independent runs now agree: no clause of CRR forces a known result on its own. The
external run's SHARP rows are what the issue's rule 2 warns about: an observable, a unit or a
cut rule chosen after the fact, or a domain constant that was defined at the framework's point.

## The biological battery (owner request, 2026-09-17)

`bio_retrodictions.py` → `bio_retrodictions.txt` (pinned; CI reproduces it byte for byte). 19
model systems in six classes, model systems only (no dataset opened, R2), and for every system
with its own events the H-L5 class computed on the model with the repository's own instrument.

| class | SHARP | CONSIST | DESCR | FAILS | TENSION | OPEN |
|---|---|---|---|---|---|---|
| (n) neural | 0 | 2 | 0 | 1 | 0 | 1 |
| (c) cardiac / physiological | 0 | 0 | 2 | 0 | 0 | 1 |
| (e) epidemiological | 0 | 0 | 1 | 0 | 0 | 2 |
| (p) population / evolutionary | 0 | 2 | 1 | 0 | 0 | 0 |
| (m) molecular / cellular | 0 | 0 | 1 | 0 | 0 | 2 |
| (b) behavioural / adaptive | 0 | 0 | 1 | 0 | 0 | 2 |
| all (19) | 0 | 4 | 6 | 1 | 0 | 8 |

**What has content.** The CONSIST rows are where a biological quantity already *is* the Fisher
geometry: the replicator equation is a gradient flow in the Shahshahani (Fisher) metric and the
Fisher speed of selection is the fitness standard deviation (Fisher's fundamental theorem);
the Fechner scale is the Fisher arc under Weber's law; a relaxation-oscillator neuron under a
varying drive keeps arc rather than time because its threshold fixes the chord (the battery's
S-G2 mechanism); and bacterial cell-size control is
the first system in any of the batteries that is **arc-regular by its own physiology rather than
by construction**: an adder adds a constant volume per cycle while its interdivision time varies
with growth rate (CV 0.075 against 0.322 on the model), a timer is the opposite. That row names
the real-data study it points at: an L5x row on single-cell growth data, gated first.

**Correction, 2026-09-17 (AGENT_LOG 18; prompt-log entry 41).** The integrate-and-fire row was
first graded CONSIST, arc-regular (CV_arc 0.438 against CV_ISI 0.472), with the reset jump
counted inside the arc of every interspike interval. The jump is the cut, not arc (v3.1 A3: the
cut has no content), and as a constant 1 σ added to every occasion it lowers CV_arc by
arithmetic. On the rise alone the row reads CV_arc 0.471 against CV_ISI 0.472, a margin of
0.0017, below the 0.01 this battery treats as a reading, and the row is now OPEN. The reason is
general: the median rise arc is 11.84 σ, so the fixed chord is 8 % of the arc, and in the
fluctuation-driven regime the arc is the noise's total variation, which grows with elapsed time,
so the arc becomes a clock. The script now prints both segmentations; the instrument carries the
choice as a named parameter (`regularity(..., segment_end)`), default unchanged, and the gates
are unaffected (their outputs differ from the pinned files only on the two chaotic rows that
already differed before the change, AGENT_LOG 10 and 19). The E-I battery's balanced-LIF row had
the same bias and is corrected in the same commit.

**The one FAILS.** "ρ → 0 at onset" (the issue text's criticality clause) is a property of class-2
(Hopf) neurons; class-1 (SNIC) neurons start firing at vanishing rate with full-size spikes
(rule 4). v3.1 makes no criticality claim.

**The H-L5 class map** (model systems; the ledger's real-data rows are MEAS2 for measles and
CARD, pending): arc-regular: FitzHugh–Nagumo under varying
drive, respiratory sinus arrhythmia (by construction), the adder; clock-regular: pulsus
alternans, a fibrillation-like rhythm (neither is regular), the entrained circadian oscillator,
the timer. The forced-SIR row shows the map's limit: counting every peak makes it arc-regular by
a small margin, counting major epidemics makes both quantities exact on the deterministic orbit,
so the event rule, which the framework does not supply (v3.1 O3), decides the class; the model
neither confirms nor contradicts the measles ledger row.

**OPEN, and why it matters.** The quantities biology wants are not reached: the final size of an
epidemic, the Hill coefficient, burst size in gene expression, the habituation rate. And the one
place the framework and a standard model *disagree* is prospective: in the two-state model of
motor adaptation the path surplus of a block has no effect beyond the state it leaves (depth
one), while the occasion-weight law predicts one. That is the T5 experiment the roadmap names
and the spec's §XV system; it is not a retrodiction and is graded OPEN here.

## The E-I network battery (owner request, 2026-09-17, prompt-log entry 40)

`ei_networks.py` → `ei_networks.txt` (pinned; CI reproduces it byte for byte). Question asked:
does CRR add anything to what is already known about excitatory-inhibitory networks, with the
latest Tucker and Luu papers as the reference point. Literature record, checked on the day
(R10): `docs/citations/ei_networks_2026-09-17.md`. **Only abstracts were readable in this
environment** (the full-text hosts are blocked by the egress proxy); every statement the battery
attributes to a paper is taken from its abstract and marked so, and the full texts must be read
by Daniel or the owner before any prereg cites them. Model systems only; no dataset opened.

| row | system | grade |
|---|---|---|
| 1 | Wilson-Cowan inhibition-stabilised network, paradoxical effect (Ozeki 2009) | OPEN |
| 2 | Wilson-Cowan 1972 oscillator: Hopf onset and what sets the frequency | OPEN |
| 3 | the same oscillator with noise: H-L5 class of its half-cycles | OPEN |
| 4 | balanced LIF network (van Vreeswijk-Sompolinsky, Brunel); H-L5 on five cells, both segmentations | DESCR |
| 5 | "balanced precision" (Tucker, Luu & Friston 2025) against CRR's two equanimity readings | TENSION |
| 6 | theta-gamma n:m locking, Resonant Oscillatory Coherence (Tucker & Luu 2026) | DESCR |
| 7 | avalanches at E-I balance as a critical branching process (Poil 2012) | FAILS |
| 8 | stabilised supralinear network (Ahmadian-Rubin-Miller 2013) | OPEN |
| 9 | homeostatic scaling | DESCR |
| 10 | cortical travelling wave (Kuramoto ring, twisted state) | DESCR |
| 11 | population Fisher information under differential correlations | DESCR |
| 12 | the removed "one Ω before rupture" rule, C·Ω = 1, run on rows 3 and 4 (prompt-log entry 41) | FAILS |
| all (12) | 0 SHARP / 0 CONSIST / 5 DESCR / 2 FAILS / 1 TENSION / 4 OPEN | |

**Answer to the question asked: no.** Clauses that reach a known E-I result: 0 of 12. Every
result the domain owns is reproduced by the domain's own mathematics and none by a CRR clause:
the paradoxical decrease of inhibition under extra inhibitory drive (I from 2.1111 to 2.0000
in the ISN, an increase in the non-ISN) is linear algebra of the weight matrix; the onset of
the E-I rhythm is a Hopf bifurcation (amplitude² linear in w_EE with onset w_c = 14.36 on the
1972 parameter set) and its frequency is set by τ_I *together with* the recurrent gains
(f(τ_I = 1)/f(τ_I = 2) = 2.93, not the 2.00 of a pure 1/τ_I law); balance is a √K cancellation
(median ISI CV 0.83, net input 6.3 % of the excitatory input against the 15.8 % scale of 1/√K);
n:m locking fixes the count of gamma cycles per theta cycle by definition (exactly 5 with the
coupling, 5 or 6 without). On each, CRR names the cycle as an occasion and is silent on the
number the domain wants.

**Tucker and Luu.** Their abstracts state three things the battery can address. (i) "Balanced
feedforward (excitatory) and feedback (inhibitory) precision" as optimal updating: on one
Gaussian update equal precision is Bayes-optimal only at precision ratio 1 and inflates the
squared error 3.025× at ratios 0.1 and 10, and CRR's two readings of "equanimity" give
*different* gains on the same update (0.5000 from equal precision, 0.6180 from Fisher speed 1),
so the framework cannot say which balance it would predict: TENSION, internal, the same one
the main battery's row 16 records. (ii) Resonant Oscillatory Coherence, theta-gamma n:m
phase-phase coupling persisting "long enough" for NMDA facilitation: under locking a threshold
in gamma cycles and a threshold in clock time are the same statement, so CRR's natural time
adds nothing, and the abstract gives no duration or ratio to test against: DESCR. (iii)
Criticality at E-I balance: the standard model of neuronal avalanches (a branching process at
σ = 1) has a size-distribution slope of −1.57 at balance and −2.13 away from it, and the Fisher
information about the branching ratio is 1/σ, finite and smooth through the critical point.
The older text's "criticality is Fisher divergence" clause FAILS on it (the third such
counterexample across the batteries); v3.1 makes no criticality claim.

**What the E-I rows add to the H-L5 class map.** A noisy Wilson-Cowan rhythm reads arc-regular
at every registered noise level and under all three carriers (identity, Bernoulli-Fisher
0.757 vs 0.816, Poisson-Fisher 0.766 vs 0.813), but two of the four margins are below 0.01 and
the noise-free oscillator already has non-zero CVs because the half-turn cut alternates on an
asymmetric waveform (the A3 gate's S-C/S-E finding). The balanced LIF cells read arc-regular on
4 of 5 cells with the reset jump counted inside the arc and on 0 of 5 without it: in the
fluctuation-driven regime the rise arc is 11–13 σ against a chord of 1, so the chord's regularity
is not inherited and the arc is a clock (the correction above). Neither is a result; both say
what a real-data row would have to gate against.

**The "one Ω before rupture" rule (row 12, prompt-log entry 41).** The owner asked whether the
battery used the full CRR and the rule C·Ω = 1. It did not, and it should not: v3.1 holds the
antipodal cut A3 and says the scalar condition "is not the axiom"; D1 says ρ is measured, never
predicted; the external specification removed the rule (its §XI.1) because a monotone cut occurs
at C = ρ, not at C = 1/Ω. Row 12 records what the rule would have predicted on two of the E-I
models. On the noisy Wilson-Cowan rhythm the unit is σ = 0.0333 (A1′, training half) and
ρ = 4.54, so the rule cuts 9.29 times per antipodal half-turn at Ω = 1 (4.70 and 18.15 at Ω = 0.5
and 2); it coincides with A3 only where ρ = 1/Ω. On the balanced LIF neuron, with σ = the
threshold gap, the rise arc is 10.77 σ against a chord of 1.117, the C = 1 cut fires at 4 % of the
interspike interval and before the spike on 100 % of intervals, and the rule cuts 13.9 times per
spike at Ω = 1. The neuron's own event is a chord condition, C* = 1, the opposite reading of
"one unit before rupture". Graded FAILS as a clause of the older text. The rest of CRR that the
battery could not use is stated in the script: the gradient rule needs a learner with a past
penalty (no E-I row has one; homeostatic scaling is depth one), and the occasion-weight law
π ∝ e^{S/Ω} needs a measured influence of settled occasions, which no E-I observable supplies
(the surplus per half-turn, median 4.90 σ, is computed and nothing in the model reads it).

**Decisions taken while building it** (AGENT_LOG 16–19): the first run of four rows printed
numbers that contradicted their text (a fixed point where an oscillator was claimed, an
unlocked pair labelled locked, a mis-scaled balance metric, an anti-phase ring labelled a wave).
The models were corrected, not the wording, and every class or regime label in the output is
now computed from the number it describes.

## The driven-systems battery (owner request, 2026-09-17, prompt-log entry 42)

`driven_systems.py` → `driven_systems.txt` (pinned; CI reproduces it byte for byte). Nine model
systems in five classes no earlier battery covered: geophysical threshold systems, materials
with memory, engineered control loops, a chemical relaxation oscillator, and a two-parameter
thermodynamic protocol. Model systems only; no dataset opened. Where an event is a jump (a slip,
a window halving, an avalanche) the segmentation is exclusive, per prompt-log entry 41.

| row | system | grade |
|---|---|---|
| 1 | spring-slider fault: strength jitter / loading-rate jitter / both (the L5x question on a model) | OPEN |
| 2 | Olami-Feder-Christensen earthquake automaton: size exponent and recurrence of large events | DESCR |
| 3 | Kramers escape in a double well, unforced and periodically forced (tipping prototype) | DESCR |
| 4 | Paris-law fatigue under variable-amplitude loading: which path functional | DESCR |
| 5 | Preisach hysteresis: measured influence of each settled excursion vs the occasion-weight law (T5) | FAILS |
| 6 | AIMD congestion control: buffer-limited and random loss under RTT jitter | DESCR |
| 7 | M/M/1 busy periods: natural time against clock | DESCR |
| 8 | Oregonator under drifting recovery time or stoichiometry | OPEN |
| 9 | two-parameter harmonic-trap protocol: does S order the excess work | DESCR |
| all (9) | 0 SHARP / 0 CONSIST / 6 DESCR / 1 FAILS / 0 TENSION / 2 OPEN | |

**The one result with teeth: T5 fails where influence is measured (row 5).** The roadmap said
the occasion-weight law π ∝ e^{S/Ω} could only be tested on a carrier where the influence of a
settled occasion is *measured*, not imposed, and no battery had such a row. A Preisach ensemble
is one: the final magnetisation after six excursions of surplus 0.60, 1.10, 1.60, 0.90, 1.30 and
0.40 changes by 0.1490 when the largest excursion is removed and by exactly 0 when any of the
other five is removed. The law's log-odds between the two largest occasions is their surplus
difference, 0.30; the system's is infinite. Wiping-out (only the running maximum survives) is a
memory with depth greater than one that the MaxEnt form cannot express, so the spec's own
depth-one exemption does not cover it. This is the first FAILS on the law rather than on a clause
of the older text, and it names the class the law must exclude before T5 is pre-registered.

**The roadmap's 2-D thermodynamic question, answered on a model (row 9).** With centre and
stiffness as controls the Boltzmann family is Gaussian and its Fisher metric is a hyperbolic
half-plane, so the geodesic has a closed form (C* = 2.612, reproduced numerically). Three
protocols with the same endpoints and duration: the geodesic at constant Fisher speed (S = 0,
W_ex 0.1029), a detour at constant speed (S = 0.832, W_ex 0.2035), and the geodesic traversed
with 90 % of its length in 30 % of the time (S = 0, W_ex 0.3015). S does not order dissipation:
the zero-surplus bursty protocol dissipates 2.93× the constant-speed geodesic and more than the
positive-surplus detour. The exact trap friction tensor is not a scalar multiple of the Fisher
metric (the two conjugate forces relax at different rates), so even the geodesic CRR names is
not the minimum-dissipation one. Sivak-Crooks' bound in the friction length holds on all three.

**H-T1's analogue on a wear system (row 4).** Paris-law damage is path-dependent by construction
and the endpoint predicts nothing (R² 0.020), but the path functional the material obeys carries
the exponent m = 3 (R² 0.979) and the Fisher arc with exponent 1 is the wrong functional
(R² 0.958). H-T1 names path-dependence; the domain supplies which path integral.

**The class map, and the limit of H-L5.** The spring-slider shows the L5x question in its
simplest form: strength jitter makes arc and clock the same variable (an exact tie), loading
jitter makes the arc regular (0.001 against 0.029), both together give a margin below reading.
Which of the two a fault varies is what L5x measures. AIMD is arc-regular under both loss
processes (0.008 vs 0.027; 0.367 vs 0.717) because the window rises one per round trip, so the
arc *is* the round-trip count: the first engineered system arc-regular by design. The Oregonator
is arc-regular under recovery-time drift (0.007 vs 0.151) and a tie under stoichiometry drift.
The Kramers row generalises prompt-log entry 41's finding to a system with no threshold: unforced
and forced transitions both tie exactly (1.108 and 0.520 on both CVs), because the arc of a
noise-dominated path is the noise's total variation, which grows with elapsed time. H-L5 can
discriminate only where the surplus is small against the chord, and every L5-type prereg should
say so. The M/M/1 row is a definition: on a count carrier the arc is 2N − 1, so natural time and
coherence are one statistic (CVs 1.249 for N, 1.673 for the arc, 1.751 for the duration).

**OFC (row 2).** Size-distribution slope −1.99 on sizes 1–64 at α = 0.2, 1.22 % of avalanches at
64 sites or more, and the large events read arc-regular on the mean-stress carrier (0.837 vs
0.852). The exponent and its α-dependence are the automaton's.

## The cognitive-collective battery (owner request, 2026-09-17, prompt-log entry 48)

`cognitive_collective.py` → `cognitive_collective.txt` (pinned; CI reproduces it byte for byte). Nine
model systems in six classes no earlier battery covered: cognitive models, learning machines other
than the ledger's, an economic time series, collective synchronisation, an evolutionary game cycle
and social diffusion. Model systems only; no dataset opened.

| row | system | grade |
|---|---|---|
| 1 | drift-diffusion decision model at two drifts and two sampling steps | TENSION |
| 2 | Rescorla-Wagner learning rate against the Kalman gain at Fisher speed v (P4) | DESCR |
| 3 | retention in natural time vs clock time under variable-rate interference (P5) | DESCR |
| 4 | linear echo-state reservoir: measured influence of past input blocks, age (P3) vs surplus (P2) | FAILS |
| 5 | simulated annealing of a two-level system: three schedules of equal Fisher length | CONSIST |
| 6 | GARCH(1,1) volatility clustering vs i.i.d. returns, exceedance events | DESCR |
| 7 | Kuramoto synchronisation transition (exact order parameter) and the criticality clause | DESCR |
| 8 | rock-paper-scissors replicator with an attracting heteroclinic cycle, Fisher-native simplex | CONSIST |
| 9 | Bass diffusion of an innovation as one occasion | DESCR |
| all (9) | 0 SHARP / 2 CONSIST / 5 DESCR / 1 FAILS / 1 TENSION / 0 OPEN | |

**A theorem about the instrument, not the systems (row 1).** The Fisher arc of a Brownian path is
its total variation, which is not finite. On the drift-diffusion model the mean arc per trial falls
from 9.31 to 2.93 when the sampling step goes from 1e-3 to 1e-2 (ratio 3.18 against √10 = 3.16) while
the reaction times do not change. So on a diffusion carrier D2's C is a property of the sampling
step, and every arc-versus-clock comparison on such a carrier compares the clock with itself. This
is graded TENSION because it is internal to the framework: D2 presumes a rectifiable path. It is
also the explanation of the exact ties the Kramers and integrate-and-fire rows produced earlier. A
prereg on a diffusion carrier must name a smoothing scale or a rectifiable Fisher-native carrier.

**The second measured-influence system, and O2 decided against surplus (row 4).** On a linear
echo-state reservoir the influence of each past input block on the final state is measured by
removal. Age explains it with R² 0.918 and a fitted decay of 0.907 per step against the spectral
radius 0.9 (P3, which is the spectral radius renamed); the surplus explains 0.376 alone and adds
0.011 beyond age; what remains is the input's magnitude (R² 0.948 with age and log scale). P2's
exponential-in-surplus weights fail on the first system that meets O2's own condition (occasions
that differ in-family and recur), after failing on the Preisach ensemble. Two measured-influence
systems, two failures, one of each memory class.

**Arc-regular by dynamics on a Fisher-native carrier (row 8).** The rock-paper-scissors replicator
with an attracting heteroclinic cycle, integrated in log coordinates on the simplex with the
Shahshahani metric (P7), has dominance epochs whose durations grow without bound (last twelve: CV
0.274 at a = 1.1, 0.780 at a = 1.3) while the Fisher arc of each epoch converges to the
vertex-to-vertex distance π (last arcs 3.134 and 3.142; CV 0.030 and 0.074). Neutral cycles tie
exactly. This is the second system after the adder that is arc-regular by its own dynamics rather
than by construction, and the first on a carrier where the metric is not decorative. The saturation
value is a definition; the regularity is dynamical. CONSIST.

**Inherited optimality (row 5).** Three annealing schedules with identical Fisher length 1.307 give
lag integrals 0.1974 (linear in T), 0.0539 (linear in β) and 0.0441 (constant Fisher speed). The
length cannot rank them; the speed profile does, as on the two-parameter trap. CONSIST, inherited
from Salamon-Nulton.

**Readings (rows 2, 3, 6, 7, 9).** The Rescorla-Wagner optimum tracks the Kalman gain of the
environment's Fisher speed (best α 0.12, 0.30, 0.60 against K(v) 0.095, 0.258, 0.618 at v = 0.1,
0.3, 1), so 1/φ is privileged only at v = 1 and P4 says of itself that it is not CRR's. Retention
in natural time predicts by construction (R² 0.998 against 0.938 for clock time) and restates the
interference hypothesis. GARCH exceedances are more regular in realised-variation time than in
clock time (CV 2.400 against 2.984, margin 0.585; the i.i.d. control 0.887 against 0.899), which is
Clark's subordination reading with a chosen event (rule 2). Kuramoto's order parameter matches the
exact Lorentzian result to 0.013 above onset and vanishes into the finite-N floor at onset, a fourth
data point for the class dependence of the older criticality clause. Bass diffusion is a monotone
occasion with S = 0 and a depth-one state.

**Decisions** (AGENT_LOG 21): the first run's rock-paper-scissors row did not reach the heteroclinic
regime (linear-coordinate clipping) and the diffusion row's class flipped with the drift for no
mechanism; the models and the grading were corrected, not the wording.

## The wild-systems battery (owner request, 2026-09-18, prompt-log entry 51)

`wild_systems.py` → `wild_systems.txt` (pinned; CI reproduces it byte for byte). Eight model systems in
eight classes chosen to be as far from the earlier batteries as a computable model allows: road
traffic, handwriting, mast seeding, pulsar glitches, immune imprinting, maintenance scheduling, a
dripping tap and cache replacement. Model systems only; no dataset opened.

| row | system | grade |
|---|---|---|
| 1 | Nagel-Schreckenberg traffic, a tagged car's stop-to-stop occasions | OPEN |
| 2 | handwriting strokes: isochrony vs constant-speed timing | DESCR |
| 3 | mast seeding (Isagi resource-budget model) under weather-driven production | OPEN |
| 4 | pulsar glitches as threshold release: backward vs forward size/waiting-time correlations (A6) | FAILS |
| 5 | immune imprinting (antigenic seniority): measured influence, a third memory class | DESCR |
| 6 | maintenance scheduling: odometer vs calendar under variable usage | DESCR |
| 7 | dripping tap: Tate's-law drops vs variable pinch-off mass | DESCR |
| 8 | cache replacement: LRU (age weights) vs LFU (an accumulated count, A6) | FAILS |
| all (8) | 0 SHARP / 0 CONSIST / 4 DESCR / 2 FAILS / 0 TENSION / 2 OPEN | |

**Two clauses of A6 fail on ordinary engineered and astrophysical memories.** A6 says the next
occasion is seeded from the settled past and that regeneration "never" returns an accumulated
count. Row 4: in a variable-threshold reservoir model of glitching the next glitch carries no
information from the last (forward correlation −0.07, backward 1.00), while a variable-release model
gives the opposite (forward 1.00, backward −0.02); the forward dependence A6 asserts is a signature
of which quantity varies, not a consequence of regeneration. Row 8: a cache that re-counts its past
(LFU) keeps evicting and beats age weights by 0.118 in hit rate on a stationary Zipf stream, and loses
to them by 0.186 under drift. What survives of A6 is O2's condition: the better weighting depends on
whether the past recurs in-family.

**The clock-regular class has a physiology of its own (row 2).** Handwriting strokes under isochrony
give CV_arc 0.503 against CV_clock 0.053 (and 0.133 under the empirical weak scaling), clock-regular
by the motor system's own law, the mirror image of the adder. The slogan "change has its own clock"
has a natural counter-class, and the battery now records one.

**A resource-driven system that is not arc-regular (row 3).** The masting tree is an adder whose
store after a mast varies with the overshoot; at k = 1.5 and k = 3 it reads clock-regular (CV_arc
1.307 vs 0.412; 0.879 vs 0.503), and k = 0.5 collapses to annual flowering (2917 masts in 3000
years, the model's fixed point). The arc-regular class needs a fixed chord *and* a fixed reset;
the framework's slogan would have predicted the opposite here.

**Three memory classes are now on record (row 5, with the driven and cognitive batteries).**
Recency (the reservoir, age weights with q < 1), wiping-out (Preisach, influence 1 or 0), and
primacy (antigenic seniority, age weights with q = 1.67 > 1; masked to 1.08 by an antigenic-distance
kernel). The framework's P2/P3 distinguish none of them, and a T5 prereg must name the class before
the gate.

**Kitchen and fleet adders (rows 6 and 7).** The odometer (CV_arc 0.091 vs CV_clock 0.198 under
variable usage) and Tate's-law drops (0.027 vs 0.152 under variable flow) are arc-regular by
construction and tie when the threshold varies instead; they show how ordinary the arc-regular class
is when a threshold fixes the chord, and that the practice (mileage-based maintenance) predates the
framework. Traffic (row 1) reads arc-regular by 0.17 on both CVs near 2, a class assignment at one
density.

**Decisions** (AGENT_LOG 22): the masting row's first registered value collapsed to the annual fixed
point and the imprinting row mixed seniority with antigenic distance; the registered values and the
variants were corrected, not the wording.

## The twenty-systems battery (owner request, 2026-09-18, prompt-log entry 52)

`twenty_systems.py` → `twenty_systems.txt` (pinned; CI reproduces it byte for byte). Twenty model
systems in eighteen domains none of the eight earlier batteries touched. Model systems only; no
dataset opened. Tally: 0 SHARP / 1 CONSIST / 12 DESCR / 1 FAILS / 0 TENSION / 6 OPEN.

| row | system | grade |
|---|---|---|
| 1 | radioactive decay chain (Bateman): a Markov control | OPEN |
| 2 | passively Q-switched laser: gain build-up to a saturable-absorber threshold | DESCR |
| 3 | geyser eruptions (reservoir with variable release): forward size/interval rule | CONSIST |
| 4 | ENSO delayed oscillator with weather noise at two levels | OPEN |
| 5 | Paillard three-state ice-age model under synthetic orbital forcing | OPEN |
| 6 | tokamak sawtooth crashes, complete and incomplete | DESCR |
| 7 | two-process sleep model, entrained vs free-running | OPEN |
| 8 | bacterial run-and-tumble: run length vs run duration | DESCR |
| 9 | hippocampal theta phase precession (H-CUT) | FAILS |
| 10 | Rosenzweig-MacArthur predator-prey cycle with environmental noise | OPEN |
| 11 | bullwhip effect under moving-average forecasting (a windowed memory) | DESCR |
| 12 | fibre-bundle cascading failure: critical load and burst exponent | DESCR |
| 13 | TD(λ): accumulating vs replacing eligibility traces | DESCR |
| 14 | Kovacs memory effect in a two-mode glass model | DESCR |
| 15 | Elo ratings: best K-factor against skill volatility (P4) | DESCR |
| 16 | cricket chirps under drifting temperature (Dolbear's law) | DESCR |
| 17 | the spacing effect with ACT-R's activation-dependent decay | DESCR |
| 18 | cobweb model: a depth-one control | DESCR |
| 19 | RHEED growth oscillations as natural time | DESCR |
| 20 | fire regimes: fuel-limited vs ignition-limited | OPEN |

**The first H-CUT row, and it fails (row 9).** H-CUT says a system's own events sit at the phase
antipode. A place cell's spikes advance through the whole theta cycle as the animal crosses the
field: the mean resultant length of spike phases is 0.100 for the precessing cell against 0.879 for
an antipode-locked control with the same jitter. Phase precession is the best-known phase code in
neuroscience and it is exactly the class H-CUT must exclude before its gate is written.

**The one CONSIST is the geyser, and it is the pulsar row's mirror (row 3).** With a fixed threshold
and a variable release, the eruption size predicts the following interval (forward correlation 1.00,
backward −0.05), the rule Old Faithful's rangers use and the reading A6 gives. The wild-systems
battery's pulsar row showed the same clause failing when the threshold varies instead. A6 reads the
variable-release class correctly and is wrong about the other; the forward rule is the reservoir
model's, not regeneration's.

**Memory kernels: five on record, one covered.** The bullwhip forecast weights the past uniformly
over its window and not at all beyond (amplification 2.92 at window 5 and 1.34 at window 20, equal
to the closed form for the policy); the spacing effect's kernel is a power law in age (R² 1.000
against 0.577 for the geometric form), and spaced practice wins by 0.902 in activation only once
the decay rate depends on the state at practice, a regeneration rule the framework does not have;
TD(λ) traces are geometric by design, and at λ = 0.95 the counting trace loses to the capped one by
0.044 RMS, the opposite of the cache row's stationary case. With the reservoir (geometric),
Preisach (wiping-out) and antigenic seniority (primacy), five kernels are now measured and P2/P3
cover one.

**The adder in four more domains, with its two conditions visible.** The Q-switched laser (CV_arc
0.004 vs 0.250 under pump noise), the sawtooth with complete crashes (0.003 vs 0.092), cricket
chirps (0.029 vs 0.084) and RHEED oscillations (0.003 vs 0.104) are arc-regular by construction:
a fixed chord and a fixed reset. The incomplete sawtooth crash (0.506 vs 0.510) and the
threshold-jittered laser (0.128 vs 0.127) show what happens when either condition fails. The
ignition-limited fire regime is arc-regular (0.141 vs 0.505) for a reason that has nothing to do
with fire: the fuel saturates while waiting, so saturation fixes the chord.

**Class assignments where the framework predicts nothing.** ENSO ties at noise 0.3 and is within
0.002 at noise 0.6; the Paillard model reads arc-regular (0.262 vs 0.324) with terminations 55 kyr
apart under the synthetic forcing; the entrained sleep cycle ties within 0.001 because the gate
moves the threshold with the clock, while the free-running homeostat is an exact adder (0.000 vs
0.100); the predator-prey cycle reads clock-regular at the reading edge (0.041 vs 0.031).

**Controls and readings.** The decay chain and the cobweb are depth-one systems on which the
framework is correctly silent (the daughter peak at 4.02 and the amplitude ratio 0.640 are the
closed forms). The fibre bundle fails at 0.2509 per fibre against the exact 1/4 with a burst slope
of −3.07 on small sizes (asymptotic −5/2); the Kovacs hump (0.0031 against 1.7e-18 for the
equilibrium control) is a two-dimensional state read as path dependence; the Elo optimum rises
with volatility (K = 2, 128, 256 at v = 0.03, 0.1, 0.3), the Kalman reading in a logistic setting;
run-and-tumble at constant speed ties exactly because the arc is the clock times a constant.

**Decisions** (AGENT_LOG 23): seven rows' first numbers contradicted their text; the models and
estimators were corrected and every verdict is computed from its numbers.

## CRR at zero: the emptiness battery (owner request, 2026-09-18, prompt-log entry 54)

`emptiness.py` → `emptiness.txt` (pinned; CI reproduces it byte for byte). Not a set of systems but a
set of boundaries: what every definition, rule and instrument in the repository does at zero, plus the
theory's own two statements of no content. Thirteen rows in five groups. Tally: 0 SHARP / 0 CONSIST /
11 DESCR / 0 FAILS / 1 TENSION / 1 OPEN.

| row | boundary | grade |
|---|---|---|
| 1 | the empty occasion (a carrier that does not move): C = C* = S = 0, no unit | DESCR |
| 2 | the cut as a delta: unit count, zero measure; Now is the derivative of settlement | DESCR |
| 3 | a closed loop: endpoint displacement 2e-16, arc 2π, all of it surplus | DESCR |
| 4 | the future has no content: the settled sum has no terms ahead of Now | DESCR |
| 5 | the boundary of a Fisher-native carrier: infinitely curved, finitely far (2, π/2, π) | DESCR |
| 6 | a mostly-empty count carrier: arc is a sum of event jumps, the unit does not exist | DESCR |
| 7 | the normalised step at zero gradient: ∞ for an empty past, 0 for an empty present | TENSION |
| 8 | the Kalman identity at zero and infinite Fisher speed: K = 0 and K = 1 | DESCR |
| 9 | MaxEnt weights at zero surplus, zero temperature, zero age: uniform; only Now; all equal | DESCR |
| 10 | a signal below one resolvable step: the cut fires on pure noise (1248 cuts on nothing) | DESCR |
| 11 | zero, one, two, three events: the instrument refuses below two occasions and one unit | DESCR |
| 12 | the quantum vacuum under displacement: its antipode is never reached (3.119 at |α| = 3) | OPEN |
| 13 | zero surplus is the monotone path; one reversal makes S twice the backtrack | DESCR |

**What the framework says about emptiness.** Exactly two things, both definitions and both exact:
the cut has no content (a delta of unit integral and zero support, the derivative of the Heaviside
that partitions past from future) and the future has no content (the settled sum's upper limit is
the number of cuts so far). Everything else at zero is the mathematics of the borrowed objects
behaving as it must: Fisher boundaries are singular but at finite distance (Cencov); a loop has
zero displacement and full arc; MaxEnt with nothing to distinguish is uniform; the Kalman gain runs
between its two emptinesses with the golden ratio at speed one between them.

**The one TENSION (row 7).** The normalised step has opposite limits at its two zeros: as the past
gradient vanishes the weight on the past is unbounded (the cap EQ2 had to add), and as the present
gradient vanishes the weight on the past goes to zero. The second is the ordinary end state of every
training run, a converged learner that stops protecting old tasks, and no ledger row has tested it;
the EQ2 report did not name it. It belongs in the EQ3 prereg as a pre-registered diagnostic.

**The instrument at zero.** The instrument does not report zero; it refuses. A constant or
mostly-zero statistic has no unit (`unit_sigma` raises; R11's flat-channel gate), fewer than two
occasions give no regularity, one unit gives a sign test with p = 1. Conversely the antipodal cut,
being a phase criterion, fires on pure noise at the noise's own rate (1248 cuts on a signal of
amplitude zero against 20 true cycles at amplitude one), which is why ρ is reported and a floor is
pre-registered. Emptiness is a state the pipeline excludes, not one the theory describes.

**Nothing derived.** No row reaches a result about zero that the borrowed mathematics did not
already contain. The vacuum row is a control: displacement never reaches the vacuum's antipode, so
A3 never fires and the framework is correctly silent.

## CRR against Shannon information theory (owner request, prompt-log entry 58)

`shannon.py` → `shannon.txt` (pinned; CI reproduces it byte for byte). Twelve rows on the places where
the Fisher–Rao quantities CRR uses meet Shannon's; the 2026 literature status is in
`docs/citations/shannon_2026-09-17.md` (abstracts and snippets only). Tally: 0 SHARP / 4 CONSIST /
7 DESCR / 0 FAILS / 0 TENSION / 1 OPEN.

| row | bridge | grade |
|---|---|---|
| 1 | the Fisher metric is the Hessian of KL; D6's √(2KL) step is the Fisher–Rao distance to second order | DESCR |
| 2 | de Bruijn: entropy rate along the heat flow = half the Fisher information (checked to 5.5e-7) | CONSIST |
| 3 | Stam: entropy power × Fisher information ≥ 1 (Laplace 1.7305, Gaussian 1.0000) | DESCR |
| 4 | Jeffreys prior maximises mutual information (Bernoulli n = 200: 2.4123 nats at a = 0.5, the maximum) | CONSIST |
| 5 | Clarke–Barron: mutual information under Jeffreys = log of the number of resolvable steps (n = 10000: I 4.3362 vs log ρ 4.3310) | CONSIST |
| 6 | rate–distortion at the unit: R = log₂ ρ bits | DESCR |
| 7 | data-processing inequality = A4 (I(X;Y) 0.3725 ≥ I(X;Z) 0.0511) | DESCR |
| 8 | Landauer at a reset cut: log₂ ρ bits erased, ≥ 0.69 / 2.30 / 4.61 kT at ρ = 2 / 10 / 100 | OPEN |
| 9 | information length is D2 on a path of distributions (C 1.7737, C* 1.7267, S 0.0471) | CONSIST |
| 10 | BSC capacity is zero at the Fisher midpoint p = 1/2 (g = 4.00 there) | DESCR |
| 11 | natural time gives unit entropy per Poisson event (1.0000 nat at every rate) | DESCR |
| 12 | P2's weights are Shannon-entropy maximisers (0 of 2000 constrained alternatives higher) | DESCR |

**The bridges are real and none is CRR's.** Every identity that turns a Fisher quantity into a
Shannon quantity in this battery predates the framework: de Bruijn and Stam (1959), Bernardo (1979),
Clarke–Barron (1990), Landauer (1961), Jaynes (1957), information length (Kim). CRR's contribution on
each is a name. The strongest bridge is row 5: the resolution ρ that D1 says to report and never to
use in a threshold is exactly the count whose logarithm is the mutual information the record carries
about the parameter at n observations, asymptotically and under the Jeffreys prior. That is why ρ is
the right thing to report, and it is Clarke and Barron's theorem read with CRR's names.

**One place the framework is silent where physics is not (row 8).** A reset cut erases the settled
occasion's position; Landauer fixes the minimum cost at kT ln 2 per bit, which for ρ resolvable steps
is ln ρ in units of kT. A3 says the cut has no content, A6 says the settled past is retained as
reweighted content; the threshold-reset systems of the earlier batteries erase it. No clause says
which a system does or what it pays. A real-data row would need a measured erasure cost per occasion
(single-electron or optical-trap memories), gated first.

**The field's 2026 status against the battery (`docs/citations/shannon_2026-09-17.md`; abstracts and
snippets only).** Where the battery inherits, the field is still moving: the log-convexity of Fisher
information along the heat flow (the identity behind row 2) was reported disproved in dimension two
and above this year (Zou, Fan, Gao and Wang, arXiv:2605.18081, snippet), and de Bruijn identities now
exist for Tsallis and nonlocal Fisher informations; the Fisher–Rao metric in infinite dimensions
"lacks a bounded inverse" (Cheng and Tong, Entropy 28:374, PubMed), which bounds any nonparametric
carrier CRR might name; rate–distortion–perception theory is the live form of row 6's question and
its perceptual term's "theoretical origin" is stated as unclear. Where the battery says OPEN, the
field says the same in experiment: a 2026 DRAM erasure measurement reports that "the Landauer
limit was not achieved, even under effectively infinite-time bit erasure" (Shimizu et al., Phys Rev
Lett 136:117103, PubMed), so row 8's cost is a bound, not a value. The stated bottlenecks the
battery does not touch are estimation ("no accepted tests exist to detect when neural
network-based estimators fail", Abdelaleem et al., snippet), the information bottleneck's
"unresolved theoretical ambiguities", scaling laws ("no existing theory can quantitatively predict
the exponents", Cagnetta et al., snippet), and computationally bounded information (Finzi et al.,
"epiplexity"). None of these is a place where a Fisher arc, a cut or a surplus has a role the field
lacks; CRR has nothing to offer them and the battery does not pretend otherwise.

**What the data-processing inequality says about the batteries (row 7).** A4's depth one, the
ledger's "the old-probe endpoint predicts forgetting", and the reservoir and Kovacs rows are one
theorem: when the observed state is Markov the path carries nothing the state does not, and where
path dependence appeared the observed state was not the full state. Information theory answers
CRR's path-versus-endpoint question per system, and the answer is "name the state".

## CRR against loop quantum gravity (owner request, prompt-log entry 59)

`loop_gravity.py` → `loop_gravity.txt` (pinned; CI reproduces it byte for byte). Eight rows on the places
where a CRR quantity can be put next to loop quantum gravity or loop quantum cosmology at all; the 2026
literature status is in `docs/citations/loop_gravity_2026-09-17.md` (search snippets only; nothing in
this field is on PubMed). Tally: 0 SHARP / 0 CONSIST / 7 DESCR / 0 FAILS / 0 TENSION / 1 OPEN.

| row | placement | grade |
|---|---|---|
| 1 | black-hole entropy by puncture counting: three countings give γ = 0.1274, 0.2375, 0.2741 (all computed) | DESCR |
| 2 | the area spectrum as a fundamental unit against A1′'s estimated unit (A(1/2) = 5.170 l_P², gaps → 5.970) | DESCR |
| 3 | the LQC bounce with a massless scalar: an extremum, not an antipode; H_max 0.9267 = closed form | OPEN |
| 4 | the scalar field as LQC's relational clock: log-volume speed 0 at the bounce, 6.1400 far from it | DESCR |
| 5 | cyclic loop cosmology with a Tolman increment: arc-regular by construction (0.281 vs 0.548) | DESCR |
| 6 | spin-j coherent states: the antipode is orthogonal for every j; a half-turn spans √(2j) orthogonality distances | DESCR |
| 7 | the polymer oscillator (a Mathieu spectrum): corrections grow with excitation at the scale μ | DESCR |
| 8 | the instrument's unit run on the area spectrum's gaps returns 1.44e-05 l_P², not the quantum | DESCR |

**What loop quantum gravity gives the framework, and what it does not.** It gives a fundamental unit
(the area quantum), a rotor (spin coherent states, whose antipode is orthogonal for every j and whose
half-turn spans √(2j) distinguishable states), and a relational clock (the scalar field in LQC, in which
the volume's log-speed is constant away from the bounce and vanishes at it). CRR can name each and
predicts nothing about any of them. The one place a cut might have been claimed, the bounce, is a
turning point of the scale factor and not a phase antipode: there is no rotor, and O3 says the framework
is silent. Black-hole entropy is linear in the number of punctures, which is D1's resolvable-step count
of the horizon, but the constant is the counting's and the parameter that makes it A/4 is fixed from
outside.

**The unit question is the sharpest contrast.** LQG's unit is fundamental and fixed; A1′'s unit is a
residual scale estimated from the system's own change, with no floor. Row 8 makes the point with the
instrument: run on the area spectrum's own gaps, `unit_sigma` returns the residual of a converging
sequence, five orders of magnitude below the quantum. On a fundamentally discrete carrier a prereg would
have to name the quantum as the unit and skip the estimator, which A1′ as written does not provide for.

**The field's 2026 status against the battery.** The stated open problems are the continuum limit of
spin foams ("remains a central open problem", Bruno, Colafranceschi, Mele and Rovelli, snippet), the
Hamiltonian constraint's graph-changing action, triangulation dependence of spin-foam amplitudes, and the
clock ambiguity in relational time ("cannot be solved by a purely relational condition", Stoica,
snippet). Observationally, loop cosmology's prediction is a power-suppression scale set by the bounce
density, which depends on the Immirzi parameter and the area gap (Mena Marugán et al., snippet); a 2026
gamma-ray-burst analysis finds the data "compatible with Lorentz invariance ... to within 2.8σ" (Jiang,
Li and Wang, snippet). One 2026 abstract says that quantum gravity "typically violates some of the Čencov
assumptions, allowing the Fisher metric and Born rule to vary between observers" (Berglund et al.,
snippet): if so, A1's licence for a unique Fisher carrier does not extend to this domain at all. No 2026
paper puts a Fisher or Fubini–Study metric on spin-network states, and none uses "natural time". Nothing
in the battery bears on any of these problems.

## The SYNTHESIS class: does CRR add anything? (owner request, prompt-log entry 60)

`synthesis.py` → `synthesis.txt` (pinned; CI reproduces it byte for byte). The class, its three tests,
its gate and the expert protocol that closes it are in `docs/notes/2026-09-17_synthesis_class.md`. Each
row states one proposition Q about a domain, in the domain's own terms, built with a CRR-proper
ingredient, and the script computes the outcome from three tests: T-G (ablate the ingredient: agree
within 1 % → REDUNDANT-IG), T-N (the domain's own theorem gives the value → REDUNDANT-DOMAIN), T-C
(the check in the domain's mathematics: holds → ADDS, fails → WRONG, unavailable → PROPOSES). Eleven
rows: two gate controls and nine real domains. Gate: positive control ADDS, decoy WRONG, negative
control WRONG → GATE OPEN. Real-domain tally: 0 ADDS / 1 PROPOSES / 2 REDUNDANT-IG /
2 REDUNDANT-DOMAIN / 2 WRONG / 1 INTERNAL / 1 UNSTATED.

| row | domain, Q, ingredient | outcome |
|---|---|---|
| 1 | gate, positive: equal-total-variation cycles (2.0000 σ) with random height and duration; CV(C) 1.659e-13, CV(clock) 0.144, CV(amplitude) 0.164; decoy unit (amplitude) reads WRONG | ADDS |
| 2 | gate, negative: S-G clock-regular; CV(C) 0.134, CV(clock) 0.000 | WRONG |
| 3 | Bayesian estimation: the state after K occasions is the Fréchet mean of the per-occasion posteriors (A6); spread 0.3833 at K = 64 vs Bayes 0.0395 | WRONG |
| 4 | quantum mechanics: the cut is the first orthogonal state at the Mandelstam–Tamm time (A3); arc half-turn at 1.9238 vs antipode at 2.0944 on levels (0,1,2); no antipode on (0,1,3), minimum overlap 0.2024 | INTERNAL |
| 5 | two-tone signal: A3 occasion rate 1.9995 = 2 f₁, not 2 × centroid 2.1588; the analytic-signal theorem | REDUNDANT-DOMAIN |
| 6 | replicator: geodesic iff ≤ 2 distinct fitness values (S 6.43e-02 vs −2.56e-09); D4 is information geometry's | REDUNDANT-IG |
| 7 | heteroclinic RPS re-read: mean epoch arc 3.1416 = the edge length π (relative difference 6.54e-06) while durations run 32.9 → 544.5 | REDUNDANT-IG |
| 8 | adder with A6 + P3 memory: lag-2 partial coefficient 0.1290 (q = 0.3), 0.1634 (q = 0.6) vs 0.0080 (adder); needs lineage data | PROPOSES |
| 9 | Tolman cyclic cosmology: bounded cycle maxima (A6); Tolman growth 0.9702 vs A6 −0.0493 | WRONG |
| 10 | thermal time beside the arc clock: arc rate 0.0000 on a stationary state, thermal rate 1.0000; no Q | UNSTATED |
| 11 | horizon entropy per resolvable step: ln 2 under the j = ½ counting (the counting's definition); 1.8644 bits under the all-j counting | REDUNDANT-DOMAIN |

**What the class did that the earlier readings could not.** Row 6 is true, checkable and information
geometry's: T-G shows CRR added nothing. Row 7 re-reads a "dynamical CONSIST": the arc per epoch is the
simplex edge length, so the constant is geometry's and the CLASS label stands without the synthesis
credit. A6 read as a rule for any system with occasions is contradicted by two accumulating domains
(rows 3 and 9); its escape clause is a scope restriction and a new prereg (CLAUDE.md §10). A3 has two
readings on a projective carrier (row 4) and must be fixed by a theory change. The one PROPOSES (row 8)
is the hand-off: an adder whose setpoint references the age-weighted Fréchet mean of past birth sizes
predicts a positive lag-2 term the plain adder sets to zero, and single-cell lineage data can decide it.

**Decisions** (AGENT_LOG 29): the first run's rock–paper–scissors row used the payoff convention with
wins larger than losses, which makes the interior point attracting; the epochs were then noise
between near-equal components (arc 0.0000) and the label was wrong. The convention was matched to
the cognitive-collective battery (losses larger than wins) and the arc settled at π. Two T-G verdict
words and one bit count that had been written as text were made script-computed (R15).

## Synthesis batches: every CONSIST and DESCR row re-read under the class (owner request, prompt-log entry 61)

`synthesis_batches/QUEUE.md` (generated by `build_queue.py` from the pinned outputs) lists every CONSIST and
DESCR row across the twelve batteries in battery order: 127 rows (41 CONSIST, 86 DESCR) in 26 batches of five.
Each batch is a script `batch_NN.py` written from `BRIEF.md` with a pinned `batch_NN.txt` (CI reproduces every
one byte for byte); rows carry the source row, one proposition Q, the three tests and the computed outcome,
and, where noticed, an `elegance` note and a `child` (fifth-grader) explanation, which
`docs/pedagogy/build_elegance_ledger.py` collects into `docs/pedagogy/ELEGANCE_LEDGER.md` (a record, not evidence).

**Wave 1, batches 01–06 (queue rows 1–30: main battery rows 2–29, Daniel's rows a3–d3).** Tally over
30 rows: 0 ADDS / 0 PROPOSES / 12 REDUNDANT-IG / 9 REDUNDANT-DOMAIN / 3 WRONG / 6 INTERNAL / 0 UNSTATED.

| batch | rows | tally (ADDS / PROPOSES / R-IG / R-DOM / WRONG / INTERNAL / UNSTATED) |
|---|---|---|
| 01 | main 2, 3, 4, 5, 6 | 0 / 0 / 2 / 1 / 0 / 2 / 0 |
| 02 | main 9, 10, 12, 13, 14 | 0 / 0 / 1 / 2 / 1 / 1 / 0 |
| 03 | main 15, 17, 18, 20, 21 | 0 / 0 / 1 / 2 / 2 / 0 / 0 |
| 04 | main 22, 23, 25, 26, 29 | 0 / 0 / 3 / 2 / 0 / 0 / 0 |
| 05 | Daniel a3, a4, b1, c1, c2 | 0 / 0 / 3 / 1 / 0 / 1 / 0 |
| 06 | Daniel c3, c4, d1, d2, d3 | 0 / 0 / 2 / 1 / 0 / 2 / 0 |

**What the six INTERNAL rows say.** They cluster on three clauses, each with two readings on the domain:
- A3 on a projective carrier (batch 01 row 5, batch 05 row 3): rotor half-turn, arc half-turn and antipode
  coincide only on the geodesic set (the equator of the Bloch sphere); off it the rotor reading fires at the
  population extremum (the domain's generalised-Rabi time), the arc reading later, and the antipode never.
- A1′ on a Poisson carrier (batch 01 row 3): one event as the unit gives the waiting-time metric and a
  logarithmic arc (0.8109 for a rate change 4 → 9); the count-per-window reading gives 2.0000 at Δ = 1 and
  scales with √Δ, so the reporting interval sits inside the unit. The measles study scored the window
  reading at the reporting fortnight. A1′ named against A1′ estimated (batch 06 row 4): `unit_sigma` returns
  the Savitzky–Golay residual scale without the fit's leverage, 0.8629 of the Cramér–Rao unit at the
  registered window (AGENT_LOG 30; recorded, not repaired).
- Ω = 1 on the Kalman filter (batch 02 row 4, batch 06 row 3): the source rows' reading (Ω = 1 is Fisher
  speed 1) gives the golden-ratio gain 0.618034; H-EQ's text (equal pull) gives equal precisions and 0.5,
  which the Riccati equation places at speed 0.707107.

**What the three WRONG rows say.** The trap-stiffness protocol (batch 02 row 2): the domain's friction
tensor is the Fisher metric times a relaxation time that varies along the protocol, so CRR's global-scale
geodesic (exponential k) dissipates 0.25993 against the bound 0.25000; the main battery's row 10 had graded
CONSIST against a known line that named the Fisher geodesic as the optimum (AGENT_LOG 31; the pinned output
is not edited). The P2-weighted seed of batch posteriors (batch 03 row 1) loses to the accumulated mean at
every β ≠ 0 (relative MSE 1.4317 at β = 1), and the A6/P3 seed of a Poisson process (batch 03 row 5) loses to
the constant forecast (1.2933 against 1.0000 at q = 0.5): regeneration is not estimation, twice more.

**What the redundant rows say.** Twelve rows are information geometry's (surplus on a monotone path, the
half-orbit of an ellipse, the half-turn of a chirp, the diffusion carrier, the hysteresis half-period, the
Ising length through Tc); nine are the domain's own theorem (Cramér–Rao counts, Ramsey's β = 0 boundary,
the time-rescaling theorem, Salamon–Berry, Ruppeiner's isotherm length, the noisy Hopf precursor's
signal-to-noise). No row in the wave produced a proposition the domain lacks.

**Corrections and decisions** are AGENT_LOG 30–33. **Elegance**: 14 entries in the ledger after wave 1.

**Wave 2, batches 07–12 (queue rows 31–60: Daniel's rows d5–h5, sharp-claims rows 1–14, bio rows 2–12).**
Tally over 30 rows: 1 ADDS / 0 PROPOSES / 10 REDUNDANT-IG / 10 REDUNDANT-DOMAIN / 3 WRONG / 6 INTERNAL /
0 UNSTATED. Running total after 60 rows: 1 / 0 / 22 / 19 / 6 / 12 / 0.

| batch | rows | tally (ADDS / PROPOSES / R-IG / R-DOM / WRONG / INTERNAL / UNSTATED) |
|---|---|---|
| 07 | Daniel d5, e1, e2, e4, f2 | 0 / 0 / 3 / 1 / 0 / 1 / 0 |
| 08 | Daniel g1, g2, g4, h2, h3 | 0 / 0 / 0 / 5 / 0 / 0 / 0 |
| 09 | Daniel h4, h5; sharp 1, 3, 4 | 0 / 0 / 0 / 2 / 1 / 2 / 0 |
| 10 | sharp 5, 7, 8, 10, 11 | 0 / 0 / 3 / 0 / 2 / 0 / 0 |
| 11 | sharp 12, 13, 14; bio 2, 4 | 0 / 0 / 2 / 2 / 0 / 1 / 0 |
| 12 | bio 5, 6, 10, 11, 12 | 1 / 0 / 2 / 0 / 0 / 2 / 0 |

**The one ADDS is a candidate and carries a caution.** Batch 12 row 2: cardiac alternans in the
APD-restitution map with the diastolic interval replaced by the P3 age-weighted mean of the settled
intervals (A6). The threshold slope for alternans rises from 1.0000 to (1 + q)/(1 − q) (1.5000 at q = 0.2,
2.3333 at q = 0.4) and the pacing interval at onset falls from 312.24 to 181.40 ms. The label follows the
class's rule (the memoryless restitution criterion is the only domain theorem computed), and the row's
own weakness says why it may not survive the expert protocol: any exponential-kernel memory on the
diastolic interval gives the same multiplier, so the CRR content is the weights' shape and the bounded
strength, and the domain has memory-restitution models (Otani–Gilmour 1997, Fox 2002, Tolkacheva 2003,
named only, not fetched, R10) in which memory moves the threshold. It goes to the expert with question 1
("is Q known?") expected to matter most (AGENT_LOG 39).

**What wave 2 added to the INTERNAL list.** Three more places where a CRR clause has two readings on the
domain, each now a v3.2 decision: which intrinsic phase A3 cuts on (batch 07 row 3: under the oscillator's
own phase-plane angle the half-turn from a maximum is identically the next minimum, so on that reading A3
is the peak cut for every 1-D trace and H-CUT is empty; the antipode-versus-extremum split the Duffing
row found, 0.0066 cycles, is the analytic signal's; batch 12 row 5 finds three readings on the
Lotka–Volterra cycle); which carrier the pole-start "p = 1/2" cut lives on (batch 09 rows 3–4: on the
fraction carrier it is a definition, on the count-rate carrier a first-order decay cuts at two half-lives,
and on a receptor's ligation-state carrier 3 of 9 binding polynomials cut off the half-saturation
constant); and which reading of A1′ sets a memory depth or a seed (batch 09 row 2, batch 11 row 3, batch
12 row 4: fluctuation against displacement units, Fréchet against mixture seeds).

**What wave 2 added to the WRONG list.** The two-dial trap (batch 10 row 5) closes the escape batch 02
left open: with centre and stiffness both driven the friction tensor is Fisher times diag(1/k, 1/2k),
ratio 2 at every k, so no scalar unit makes CRR's geodesic the optimum (+12.29 %) and the S²/τ clause fails
on the domain's own optimum. Resonance fluorescence (batch 10 row 3) is arc-regular at 5 of 9 drives and
clock-regular at 3, so "arc-regular at every drive" fails on the one qubit with events of its own. The
FitzHugh–Nagumo re-read (batch 11 row 4) keeps the bare CV(arc) < CV(clock) reading but finds the
amplitude control the more regular quantity (CI [0.0189, 0.0383]), so H-L5 as stated fails there and
the SHARP review's "dynamical CONSIST" list is down to the adder (AGENT_LOG 34), whose own amplitude
control is batch 13's first task.

**Corrections to earlier batteries recorded in wave 2** (pinned outputs not edited): Daniel's row h3
multiplies a magnetisation by the square root of the field-direction metric (batch 08 row 5; his own row
h5 has the consistent reading), and his row h2's ρ → ∞ is the unit at the singular point, not the count
across a window, which is finite with exponent 8/15 (batch 08 row 4). **Decisions** are AGENT_LOG 34–39.
**Elegance**: 35 entries after wave 2.

**Wave 3, batches 13–18 (queue rows 61–90: bio rows 13–18, E-I rows 4–11, driven rows 2–9, cognitive rows
2–9, wild rows 2–7, twenty rows 2–11).** Written 2026-09-21 after the first six agents died on 2026-09-18
(usage credits; AGENT_LOG 40). Tally over 30 rows: 1 ADDS / 0 PROPOSES / 6 REDUNDANT-IG /
13 REDUNDANT-DOMAIN / 6 WRONG / 4 INTERNAL / 0 UNSTATED. Running total after 90 rows:
2 / 0 / 28 / 32 / 12 / 16 / 0.

| batch | rows | tally (ADDS / PROPOSES / R-IG / R-DOM / WRONG / INTERNAL / UNSTATED) |
|---|---|---|
| 13 | bio 13, 14, 18; E-I 4, 6 | 0 / 0 / 1 / 2 / 2 / 0 / 0 |
| 14 | E-I 9, 10, 11; driven 2, 3 | 0 / 0 / 0 / 2 / 2 / 1 / 0 |
| 15 | driven 4, 6, 7, 9; cognitive 2 | 0 / 0 / 1 / 1 / 2 / 1 / 0 |
| 16 | cognitive 3, 5, 6, 7, 8 | 0 / 0 / 0 / 5 / 0 / 0 / 0 |
| 17 | cognitive 9; wild 2, 5, 6, 7 | 1 / 0 / 1 / 2 / 0 / 1 / 0 |
| 18 | twenty 2, 3, 6, 8, 11 | 0 / 0 / 3 / 1 / 0 / 1 / 0 |

**The dynamical-CONSIST list is empty.** The SHARP review named three rows whose arc-regularity looked
dynamical. Wave 1 read the heteroclinic cycle as the simplex edge length, wave 2 read FitzHugh–Nagumo as
the loop's total variation, and batch 13 reads the adder: on the volume carrier a cell cycle is one
monotone traversal, so its arc is its added volume and H-L5's amplitude control is the arc itself
(CV 0.0749 against 0.0749, CI of the difference [0.0000, 0.0000]). The bare arc-regular class stands
(CV(clock) 0.3319) and it is the adder principle in CRR's words. Batch 18 reads the geyser, the
twenty-systems battery's one CONSIST, the same way: the refill arc is the volume the previous eruption
released (to 1.3e-03), and the class is the refill rate's.

**The second ADDS candidate, with the same caution as the first.** Batch 17 row 1: Bass diffusion with
the imitation pressure taken as the P3-faded adopter fraction instead of the accumulated count. The
Bass plot bends below its line and the peak fraction falls from 0.4606 to 0.3981, 0.2651 and 0.0863 at
κ = 0.1, 0.3, 1, while the existence condition q > p is unchanged. Any exponential-kernel memory bends
it, the CRR content is the weights' shape and bounded strength, and the domain has non-uniform-influence
models (named, not fetched); it goes to the expert protocol (AGENT_LOG 42).

**What wave 3 added to the WRONG list.** Six rows, four of them A6 or A3 read as a rule: a homeostatic
set point regenerated from the settled past is homogeneous of degree 1 in the rate, so the loop has a zero
eigenvalue and never restores its target (batch 14 row 1, settles at 5.1956 Hz against 5.0000); the
antipode reading of H-CUT puts a ring's breaking twist at half a turn where the domain's stability
boundary and the coupling force's extremum put it at a quarter turn (batch 14 row 2); A6-seeded ion
channel dwells would be correlated (0.6835) where the channel's are not (−0.0215 at SE 0.0224, batch 13
row 2); the balanced LIF cell is clock-regular on 5/5 cells once the reset is the cut (batch 13 row 4);
Paris-law damage is not a function of the Fisher path (R² 0.9642 against Miner's 1.000000, batch 15
row 1); and the two-parameter trap on the source's own endpoints (+21.08 %, batch 15 row 4).

**What wave 3 added to the INTERNAL list.** Which boundary jumps are arc on a queue (batch 15 row 3:
three readings, two classes); A1′ on a diffusion carrier (batch 14 row 5: the sampling unit gives the
clock, the two-state unit gives a constant, and every smoothing scale between moves the class); partial
resets (batch 18 row 3: the sawtooth's class flips between "the crash is the cut" and "the crash is
content"); and P3's normalisation (batch 17 row 3: MaxEnt on a finite history returns q = 1/s = 1.6667 and
reproduces the seniority profile, so primacy is P3's λ < 0 branch, while CRR.md's closed form
⟨k⟩ = q/(1 − q) assumes an infinite past and cannot represent it).

**Corrections to earlier batteries recorded in wave 3** (pinned outputs not edited): the driven battery's
AIMD row counted the descent from the previous loss inside the next occasion (batch 15 row 2; in the
loop's own units the random-loss variant is a tie, AGENT_LOG 41); its OFC row's arc-regular verdict was
against the avalanche count, and on the loading clock the automaton is clock-regular (batch 14 row 4,
AGENT_LOG 45); the bio battery's circadian row typed its zero CV(arc) (batch 13 row 3, a correct zero by
construction, AGENT_LOG 46); the cognitive battery's GARCH clustering belongs to the outside unit (batch
16 row 3). **Decisions** are AGENT_LOG 41–46. **Elegance**: 60 entries after wave 3.

## TENSION and the minimal rewording

One TENSION in the main battery (row 16); the cognitive-collective battery adds a second, internal one (D2 on diffusion carriers). Minimal resolution: give the two laws different names. Keep "equanimity"
for the occasion-weight law π ∝ e^{S/Ω}, Ω = 1 (spec H1, T5), which has a Fisher-unit meaning
and no ledger row yet; call v3.1's H-EQ what it is, a normalised-gradient step with a cap, and
carry its ledger (EQX, EQ2) under that name.

## One paragraph

Applied mechanically to 32 known systems, CRR v3.1 forces no known result on its own: the ten
CONSIST rows are the domain's own laws (arcsine and square-root transforms, Fubini–Study
angles, thermodynamic length, the Riccati gain, Omori calculus) read as arc lengths; the ten
DESCR rows are definitions and symmetries; the six FAILS are universal claims that the older
issue text made and v3.1 mostly does not (the Bernoulli antipode, mixed states, criticality,
memory depth) plus the slogan "change has its own clock", which is a measurement, not a
derivation; the gravitational class is empty of content; and the one TENSION is between the two
things called equanimity. Where CRR could be sharp — a multi-occasion salience test of
log(π_i/π_j) = S_i − S_j — no known system in the battery is such a test, which is the reason to
build one rather than to keep retrodicting.
