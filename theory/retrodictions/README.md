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
