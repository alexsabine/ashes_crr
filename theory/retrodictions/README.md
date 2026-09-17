# CRR retrodiction battery (issue #21) — reading

Script: `crr_retrodictions.py`. Output: `crr_retrodictions.txt` (committed; CI checks the
script reproduces it byte for byte). Every number below is in that file. Rules followed are
those of issue #21: one Python function per system, five grades plus OPEN, a symmetry check
wherever a result could hold by symmetry, at least four systems per class, and a `BORROWED`
field naming the mathematics inherited from the domain plus a `FLOW` field naming what
supplies the velocity inside the coherence integral C = ∫ √(ẋᵀ g ẋ) dt.

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
| (n) neural | 0 | 3 | 0 | 1 | 0 | 0 |
| (c) cardiac / physiological | 0 | 0 | 2 | 0 | 0 | 1 |
| (e) epidemiological | 0 | 0 | 1 | 0 | 0 | 2 |
| (p) population / evolutionary | 0 | 2 | 1 | 0 | 0 | 0 |
| (m) molecular / cellular | 0 | 0 | 1 | 0 | 0 | 2 |
| (b) behavioural / adaptive | 0 | 0 | 1 | 0 | 0 | 2 |
| all (19) | 0 | 5 | 6 | 1 | 0 | 7 |

**What has content.** The CONSIST rows are where a biological quantity already *is* the Fisher
geometry: the replicator equation is a gradient flow in the Shahshahani (Fisher) metric and the
Fisher speed of selection is the fitness standard deviation (Fisher's fundamental theorem);
the Fechner scale is the Fisher arc under Weber's law; a relaxation-oscillator neuron under a
varying drive and a noisy integrate-and-fire neuron keep arc rather than time, because their
threshold fixes the chord (the battery's S-G2 mechanism); and bacterial cell-size control is
the first system in any of the batteries that is **arc-regular by its own physiology rather than
by construction**: an adder adds a constant volume per cycle while its interdivision time varies
with growth rate (CV 0.075 against 0.322 on the model), a timer is the opposite. That row names
the real-data study it points at: an L5x row on single-cell growth data, gated first.

**The one FAILS.** "ρ → 0 at onset" (the issue text's criticality clause) is a property of class-2
(Hopf) neurons; class-1 (SNIC) neurons start firing at vanishing rate with full-size spikes
(rule 4). v3.1 makes no criticality claim.

**The H-L5 class map** (model systems; the ledger's real-data rows are MEAS2 for measles and
CARD, pending): arc-regular: integrate-and-fire (narrowly), FitzHugh–Nagumo under varying
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
| 4 | balanced LIF network (van Vreeswijk-Sompolinsky, Brunel) | DESCR |
| 5 | "balanced precision" (Tucker, Luu & Friston 2025) against CRR's two equanimity readings | TENSION |
| 6 | theta-gamma n:m locking, Resonant Oscillatory Coherence (Tucker & Luu 2026) | DESCR |
| 7 | avalanches at E-I balance as a critical branching process (Poil 2012) | FAILS |
| 8 | stabilised supralinear network (Ahmadian-Rubin-Miller 2013) | OPEN |
| 9 | homeostatic scaling | DESCR |
| 10 | cortical travelling wave (Kuramoto ring, twisted state) | DESCR |
| 11 | population Fisher information under differential correlations | DESCR |
| all (11) | 0 SHARP / 0 CONSIST / 5 DESCR / 1 FAILS / 1 TENSION / 4 OPEN | |

**Answer to the question asked: no.** Clauses that reach a known E-I result: 0 of 11. Every
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
at every registered noise level, but two of the four margins are below 0.01 and the noise-free
oscillator already has non-zero CVs because the half-turn cut alternates on an asymmetric
waveform (the A3 gate's S-C/S-E finding); a balanced LIF neuron reads arc-regular for the reason
the biological battery gave (the threshold fixes the chord). Neither is a result; both say what a
real-data row would have to gate against.

**Decisions taken while building it** (AGENT_LOG 16–17): the first run of four rows printed
numbers that contradicted their text (a fixed point where an oscillator was claimed, an
unlocked pair labelled locked, a mis-scaled balance metric, an anti-phase ring labelled a wave).
The models were corrected, not the wording, and every class or regime label in the output is
now computed from the number it describes.

## TENSION and the minimal rewording

One TENSION (row 16). Minimal resolution: give the two laws different names. Keep "equanimity"
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
