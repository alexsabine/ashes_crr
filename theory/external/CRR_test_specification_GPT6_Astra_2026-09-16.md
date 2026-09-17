# Coherence–Rupture–Regeneration (CRR)
## Testable axiomatic specification for independent audit
### State: 16 September 2026

> **Epistemic status.** This is a candidate mathematical metatheory, not an established physical theory. It deliberately separates definitions and inherited mathematics from CRR-specific empirical hypotheses. The purpose of this version is to make CRR easy to falsify rather than easy to fit.

## 0. Label system

Every claim is tagged by status.

- **[P] Philosophical premise:** motivates the formalism but is not, by itself, an empirical result.
- **[D] Definition:** fixes notation or an operational quantity.
- **[A] Structural axiom:** part of the CRR architecture. If removed, the theory changes.
- **[T] Theorem / derived consequence:** follows mathematically from prior definitions/axioms.
- **[H] Empirical hypothesis:** a risky claim about real systems.
- **[O] Open / system-supplied quantity:** CRR does not predict this; it must be fixed independently.
- **[F] Falsification condition:** specifies what would count against a CRR hypothesis.

The distinction is essential. Fisher geometry, the triangle inequality, Fréchet means, and the scalar Kalman Riccati solution are not empirical evidence for CRR merely because CRR uses them.

---

# I. Philosophical commitments and their mathematical translation

## [P1] Process primacy

A system is treated primarily as a temporally extended process rather than as a sequence of unrelated static states. What happens between two states may matter even when the endpoints are identical.

**Mathematical translation:** represent the system by a path on a state manifold and distinguish path length from endpoint distance.

This is why CRR contains both an accumulated path quantity `C` and a chord/geodesic quantity `D`.

## [P2] Finitude and occasion

Any operational representation is finite and locally bounded. A process is therefore analyzed in completed temporal units, called **occasions**, rather than by assuming that one representation describes the whole future indefinitely.

**Mathematical translation:** an occasion occupies an interval between two independently identifiable cut events. CRR does not assume that every system supplies such events. If no canonical occasion boundary exists, quantitative occasion-based CRR returns **OPEN**.

## [P3] Continuity and rupture are distinct logical roles

Within an occasion, change is continuous in the carrier coordinates used by the system model. A rupture is the boundary at which one occasion is declared complete. The boundary does not need to contain a second hidden dynamics.

**Mathematical translation:** within-occasion evolution is a continuous path; rupture is a first-passage / boundary event. In the CRR coarse-graining the cut is idealized as zero-duration and content-free. Any finite physical transition time belongs to the underlying system dynamics, not to an extra CRR state.

## [P4] Historicity without future information

Regeneration may depend on settled past occasions, but future states are not allowed to enter the reset rule.

**Mathematical translation:** the regeneration target at a cut is measurable with respect to information available up to that cut. No future observation may be used in the carrier, cut, content map, salience score, memory selector, or reset target.

## [P5] Path-dependence is not the same thing as memory content

Two occasions may end at the same state after taking different paths. Conversely, two occasions can have the same path surplus while carrying different substantive content.

**Mathematical translation:** CRR separates a scalar **lived surplus** `S`, which may modulate influence, from an occasion-content object `Phi`, which says *what* is carried forward.

## [P6] Epistemic humility / non-final representation

The theory is not permitted to manufacture structure merely to make a system fit CRR.

**Mathematical translation:** no post-hoc statistical carrier, no post-hoc antipode, no post-hoc event boundary, and no retrospective choice of memory rule. Where the relevant structure is not independently identifiable, CRR returns **OPEN**.

## [P7] Equanimity as a quantitative conjecture

The philosophical idea of an undistorted or balanced scale is represented mathematically by taking one independently fixed Fisher unit as the characteristic salience scale.

**Mathematical translation:** the regeneration temperature `Omega` is hypothesized to equal 1 in the pre-registered Fisher unit. This is not made true by rescaling the metric after seeing the data. In empirical tests it becomes the fixed slope claim `lambda = 1`.

This is the principal place where a philosophical commitment becomes a risky numerical statement.

---

# II. Admissible statistical carrier

## [D1] Statistical state manifold

Let

\[
\mathcal M = \{p(y\mid \theta):\theta\in\Theta\}
\]

be a smooth statistical family supplied by the system model, with parameter coordinates `theta = (theta^1,...,theta^d)`.

The Fisher–Rao metric is

\[
g_{ij}(\theta)
=
\mathbb E_{\theta}
\left[
\partial_i\log p(Y\mid\theta)
\partial_j\log p(Y\mid\theta)
\right].
\]

The metric must be positive definite on the portion of the carrier being used. Singular or indefinite objects are not treated as Fisher–Rao carriers without an independently justified reduction to a regular statistical manifold.

## [A1] Canonical-carrier requirement

The likelihood family, elementary system event, and metric normalization must be fixed independently of the outcome used to test CRR.

An analyst may not choose between Gaussian, Poisson, Bernoulli, or another observation model after seeing which one makes CRR work. Smooth reparameterizations of one fixed statistical model are allowed; changing the statistical model is not a coordinate transformation and generally changes Fisher geometry.

### Consequence

If the same physical record admits several equally defensible statistical families and there is no independent reason to privilege one, quantitative CRR is **OPEN for that system** until the carrier ambiguity is resolved.

## [A1a] Per-elementary-event normalization

If Fisher information is additive across replicated observations,

\[
I_N = N I_1,
\]

CRR uses the Fisher metric associated with the pre-specified elementary system event or other independently justified intrinsic likelihood. The experimenter may not make the same physical displacement appear longer merely by collecting more replicated data.

This clause prevents dataset size from becoming an arbitrary salience amplifier.

## [T1] Reparameterization invariance

For a smooth one-to-one reparameterization `eta = eta(theta)`, the Fisher line element

\[
ds^2=g_{ij}d\theta^i d\theta^j
\]

is invariant when the metric is transformed correctly. Therefore the quantities below are coordinate-invariant **within a fixed statistical model**.

They are not invariant to changing the model itself.

---

# III. Occasion geometry: coherence, chord, and lived surplus

Let occasion `n` begin at cut time `tau_n` and state

\[
x_n=x(\tau_n)\in\mathcal M.
\]

For `t` before the next cut, define the following.

## [D2] Coherence accumulation

\[
C_n(t)
=
\int_{\tau_n}^{t}
\sqrt{
\dot\theta^i(\tau)
 g_{ij}(\theta(\tau))
\dot\theta^j(\tau)
}
\,d\tau.
\]

`C` is accumulated Fisher–Rao arc length. The word *coherence* here is technical: it means accumulated information-geometric traversal, not moral value, psychological wellness, order, or stability.

## [D3] Geodesic chord

\[
D_n(t)=d_{\rm FR}(x_n,x(t)),
\]

where `d_FR` is the geodesic distance induced by the same Fisher metric.

## [D4] Lived surplus

\[
S_n(t)=C_n(t)-D_n(t).
\]

At the completion of the occasion,

\[
C_n=C_n(\tau_{n+1}),\qquad
D_n=D_n(\tau_{n+1}),\qquad
S_n=C_n-D_n.
\]

## [T2] Non-negativity

Because geodesic distance is the infimum of the lengths of admissible curves joining two endpoints,

\[
\boxed{C_n(t)\ge D_n(t)}
\]

and therefore

\[
\boxed{S_n(t)\ge0}.
\]

This is inherited Riemannian geometry, not a novel empirical prediction of CRR.

## [T3] Equality condition

\[
S_n(t)=0
\]

if the realized path segment is itself a minimizing geodesic between its endpoints. If multiple minimizing geodesics exist, equality does not identify a unique path.

In a one-dimensional carrier, equality corresponds to a monotone traverse with no resolved backtracking.

## [T4] One-dimensional backtracking identity

Suppose a one-dimensional occasion has total forward Fisher travel `F` and total backward Fisher travel `B`, with positive net displacement `F >= B`.

Then

\[
C=F+B,
\qquad
D=F-B,
\]

so

\[
\boxed{S=2B}.
\]

Thus in one dimension lived surplus is exactly twice the resolved backward Fisher travel.

## Interpretation constraint

`S` is an excess-length statistic. It does not uniquely encode path shape, winding number, causal mechanism, semantic content, or valence. Distinct trajectories can have the same `S`.

---

# IV. Rupture and occasion completion

The earlier strong form `C Omega = 1` is **not** a fundamental rupture law in this specification. It mixed a geometric cut scale with a regeneration-temperature scale and was inconsistent whenever the measured half-turn length was not one Fisher unit.

## [A2] Canonical-cut requirement

An occasion ends only through a cut structure that is specified independently of the CRR outcome analysis.

Two admissible forms are recognized.

### [A2a] Canonical target / involution

The system supplies a target map

\[
A:\mathcal M\to\mathcal M
\]

with a physically or structurally justified target `A(x_n)`.

When it is genuinely antipodal one expects an involutive structure

\[
A(A(x))=x,
\]

although involution is not required for every non-antipodal event model.

The next cut is the first time

\[
\boxed{x(\tau_{n+1})=A(x_n)}.
\]

Define the target distance

\[
H_n=d_{\rm FR}(x_n,A(x_n)).
\]

At the cut,

\[
D_n=H_n.
\]

If the realized traverse is a minimizing geodesic,

\[
C_n=D_n=H_n,
\]

so the valid scalar monotone reduction is

\[
\boxed{\frac{C_n}{H_n}=1}.
\]

No `Omega` is needed in this cut condition.

### [A2b] Canonical event surface

Some systems supply an independently defined event surface `Sigma` rather than a unique antipodal target. Then

\[
\tau_{n+1}
=
\inf\{t>\tau_n:x(t)\in\Sigma_n\}.
\]

The actual cut endpoint is `x_{n+1}=x(tau_{n+1})`, and its chord is simply

\[
D_n=d_{\rm FR}(x_n,x_{n+1}).
\]

No universal half-turn distance is asserted.

## [A2c] No manufactured antipodes

If a statistical family has no canonical antipodal map, CRR does not create one simply because an antipodal picture is attractive.

Examples motivating this restriction include:

- the Bernoulli Fisher manifold, which is an interval in its native Fisher coordinate rather than a circle;
- higher-dimensional pure quantum systems, in which a state generally has an entire orthogonal subspace rather than a unique orthogonal ray;
- irreducible continuous-time Markov and finite-temperature Gibbs systems, whose probability distributions may never become disjoint at finite time.

An oriented cover may be added only if the orientation is independently part of the physical state. It is then extra state information, not something secretly contained in the projected probability coordinate.

## [D5] Rotor prototype

Where a genuine oriented rotor is independently appropriate,

\[
u\in\mathbb R/L\mathbb Z\cong S^1\cong SO(2),
\]

the canonical antipodal map is

\[
A(u)=u+\frac L2\pmod L.
\]

Then

\[
A^2={\rm id},
\]

giving the familiar `Z_2` cut on an `SO(2)` carrier.

This is the **canonical prototype** of CRR rupture. It is not asserted to be the literal native state-space topology of every physical system.

## [D6] Optional resolution index

If the system also supplies an independently measured minimum resolvable Fisher displacement `sigma_n`, define

\[
\rho_n=\frac{H_n}{\sigma_n}.
\]

`rho` is a descriptive resolution index: the cut distance expressed in resolvable steps. It is measured, not predicted, and it is not a universal rupture threshold.

---

# V. Settled occasion content and memory admissibility

## [D7] Occasion content

Each completed occasion may carry an observable content object

\[
\Phi_m\in\mathcal R,
\]

where `R` is a pre-specified metric regeneration space.

The map from raw occasion data to `Phi_m` must be fixed before the future outcome being predicted is observed.

`Phi_m` may equal a carrier state in some systems, but CRR does not require this universally.

## [A3] Surplus is weight, not content

`S_m` does not tell CRR what an occasion means or which state it represents. It only enters the salience hypothesis below.

Two occasions with equal `S` may have different `Phi`; two occasions with identical `Phi` may have different `S`.

This distinction is required by ordinary hysteretic examples in which equal total path surplus can end in different memory states.

## [D8] Admissible memory set

Let

\[
\mathcal H_n\subseteq\{0,1,\ldots,n\}
\]

be the set of settled occasions that are independently justified as potentially relevant to regeneration after cut `n`.

The rule selecting `H_n` is not inferred from the outcome that CRR is asked to predict.

## [A4] Screening-off / depth-one gate

If the independently specified system model says that the current cut state is a sufficient statistic for the future, then earlier occasions are screened off.

Operationally this is the depth-one case

\[
\mathcal H_n=\{n\}.
\]

With only one admissible occasion, any multiplicative salience factor cancels under normalization. CRR therefore predicts **no additional historical salience effect** in a correctly specified depth-one Markov system.

The exponential history law below is tested only where multiple settled occasions are independently admissible influences.

This clause prevents CRR from claiming historical effects in systems whose sufficient present state already contains all predictive information.

---

# VI. Regeneration law

## [D9] General salience temperature

For mathematical clarity first define a positive scale

\[
\Omega>0.
\]

The unnormalized salience of occasion `m` is

\[
a_m=\exp\!\left(\frac{S_m}{\Omega}\right).
\]

If no other independently justified memory constraint is present, normalized weights are

\[
\boxed{
\pi_{nm}
=
\frac{\mathbf 1[m\in\mathcal H_n]\exp(S_m/\Omega)}
{\sum_{j\in\mathcal H_n}\exp(S_j/\Omega)}
}.
\]

## [O1] Independent recency or retention kernel

A system may possess an independently justified age/retention factor

\[
r_{nm}>0.
\]

CRR does not derive its form universally.

When such a factor is warranted,

\[
\boxed{
\pi_{nm}
=
\frac{\mathbf 1[m\in\mathcal H_n]\,r_{nm}\,\exp(S_m/\Omega)}
{\sum_{j\in\mathcal H_n}r_{nj}\exp(S_j/\Omega)}
}.
\]

A geometric recency model is the special case

\[
r_{nm}=q^{k_{nm}},\qquad0<q\le1.
\]

`q` is not a universal CRR constant. If `Omega` is being tested, the recency model must be fixed or identified independently enough that `q` cannot simply compensate for a wrong salience slope.

## [H1] Equanimity / unit-slope hypothesis

CRR's distinctive quantitative conjecture is

\[
\boxed{\Omega=1}
\]

in the **pre-registered per-elementary-event Fisher unit**.

Equivalently define

\[
\lambda=\frac1\Omega.
\]

Then CRR predicts

\[
\boxed{\lambda=1}.
\]

This is not allowed to be made true by changing the Fisher scale after seeing the outcome.

## [T5] Pairwise influence-odds law

For two admissible occasions `i` and `j`,

\[
\log\frac{\pi_{ni}}{\pi_{nj}}
=
\frac{S_i-S_j}{\Omega}
+
\log\frac{r_{ni}}{r_{nj}}.
\]

Under the CRR equanimity hypothesis,

\[
\boxed{
\log\frac{\pi_{ni}}{\pi_{nj}}
=
(S_i-S_j)
+
\log\frac{r_{ni}}{r_{nj}}
}.
\]

If the occasions have equal age or otherwise equal retention factor,

\[
\boxed{
\log\frac{\pi_i}{\pi_j}=S_i-S_j
}.
\]

This is the cleanest CRR-specific numerical prediction currently available.

It eliminates the Fréchet mean, coupling strength, subsequent trajectory, and much system-specific dynamics from the test.

In words:

> **one additional Fisher unit of lived surplus multiplies relative historical influence by `e`.**

## [A5] Regeneration target

Given pre-specified contents `Phi_m` and normalized weights `pi_nm`, the CRR regeneration target is the weighted Fréchet barycenter

\[
\boxed{
\mu_{n+1}
\in
\operatorname*{arg\,min}_{y\in\mathcal R}
\sum_{m\in\mathcal H_n}
\pi_{nm}\,d_{\mathcal R}(y,\Phi_m)^2
}.
\]

If the minimizer is not unique, CRR predicts the **set of minimizers**. It does not invent an outcome-dependent tie-break rule.

For Euclidean scalar content this reduces to the ordinary weighted mean

\[
\mu_{n+1}=\sum_m\pi_{nm}\Phi_m.
\]

## [O2] Dynamical realization

CRR predicts a regeneration target / pattern of historical influence. It does not universally predict how strongly or how quickly the underlying physical dynamics moves toward that target.

A coupling strength, control law, Hamiltonian, reaction rate, learning rate, or relaxation equation must come from the system model or be independently measured.

The earlier free universal `kappa` is therefore not part of the CRR core.

---

# VII. Causality and information restriction

## [A6] Settled-past-only rule

Let `F_t` denote the information filtration generated by observations available up to time `t`.

At cut `tau_{n+1}`, every quantity used to construct the next CRR regeneration target must be `F_{tau_{n+1}}`-measurable.

Symbolically,

\[
\boxed{
\mu_{n+1}
=\mathcal R
\left(
\{C_m,D_m,S_m,\Phi_m:m\le n\};
\mathcal F_{\tau_{n+1}}
\right)
}
\]

with no dependence on observations from times later than `tau_{n+1}`.

This is CRR's formal no-future-content condition.

It does **not** claim that physics has no future boundary conditions in every possible formulation; it says the CRR regeneration operator, as tested here, is not permitted to leak future data.

---

# VIII. Conditional mathematical consequences

These are consequences of CRR's regeneration law under additional distributional assumptions. They are useful because they create further empirical targets without adding fitted parameters.

## [T6] Exponential surplus tail produces a power-law influence tail

Assume that in some domain the settled surplus has asymptotic tail

\[
P(S>s)\sim e^{-\beta s},\qquad\beta>0.
\]

Let

\[
W=e^{S/\Omega}.
\]

Then for large `w`,

\[
P(W>w)
=
P(S>\Omega\log w)
\sim
w^{-\beta\Omega}.
\]

Thus the weight-tail exponent is

\[
\boxed{\alpha=\beta\Omega}.
\]

Under CRR equanimity,

\[
\boxed{\alpha=\beta}.
\]

For an ideal regularly varying tail, moments obey the usual threshold rule: the `p`th moment is finite only for `p<alpha`. In particular,

- `alpha <= 1`: mean raw weight diverges asymptotically;
- `1 < alpha <= 2`: mean is finite but variance diverges;
- `alpha > 2`: mean and variance are finite.

Under iid or sufficiently weakly dependent sampling, the `alpha<1` regime implies strongly non-self-averaging normalized influence in which extreme past occasions can retain a macroscopic share of total weight.

This is a conditional prediction, not a claim that every system has an exponential surplus tail.

---

# IX. Optional inherited modules: not evidence for CRR

## [O3/T7] Scalar random-walk Kalman domain

For the standard scalar random walk

\[
x_{k+1}=x_k+w_k,\qquad w_k\sim N(0,q),
\]

\[
y_k=x_k+v_k,\qquad v_k\sim N(0,r),
\]

define

\[
v=\sqrt{q/r}.
\]

The steady-state Kalman gain is

\[
\boxed{
K(v)=\frac v2\left(\sqrt{v^2+4}-v\right)
}.
\]

At `v=1`,

\[
K(1)=\frac{\sqrt5-1}{2}=\frac1\varphi.
\]

If one defines an effective retention depth

\[
d(v)=\frac1{K(v)},
\]

then `d -> infinity` as `v -> 0`.

These are standard Riccati results. They are **not** counted as CRR predictions. CRR may use a separately justified Fisher-speed interpretation of `v`; evidence for CRR would require CRR to fix the relevant mapping prospectively rather than merely recognize the known formula.

No universal claim is made that every physical critical point satisfies `v -> 0`.

---

# X. Pre-cut balance construction

This is retained as a mathematical construct but is no longer called a universal law of criticality.

Let `H` be a fixed cut distance for the current occasion and define

\[
B(C)=e^{C/\Omega}(H-C),\qquad0\le C\le H.
\]

Then

\[
\frac{dB}{dC}
=e^{C/\Omega}
\left(
\frac{H-C}{\Omega}-1
\right).
\]

A stationary point therefore occurs at

\[
\boxed{C_a=H-\Omega}
\]

when `H>Omega`.

At the stationary point the second derivative is negative, so this is an interior maximum.

Under equanimity,

\[
\boxed{C_a=H-1}.
\]

Interpretation: this is a balance between increasing exponential salience and decreasing remaining headroom before a fixed cut. It becomes a physical criticality statement only if an independent system-specific argument links this balance function to an experimentally measured critical phenomenon.

---

# XI. Claims deliberately removed or narrowed

## 1. Universal `C Omega = 1` rupture

**Removed.**

Reason: if the actual canonical cut distance is `H` or `rho` Fisher units, a monotone cut occurs at `C=H`, not generally `C=1`. The old formula agrees only in the special normalization `H=1`. `Omega` now belongs to regeneration, not rupture geometry.

## 2. Universal Bernoulli `p=1/2` antipode

**Removed.**

Reason: the native Bernoulli Fisher manifold is an interval. `p=1/2` is a special midpoint relative to boundary starts, not a global oriented antipode from an arbitrary previous state. A doubled oriented cover is admissible only when the extra orientation is independently physical.

## 3. “Mixed quantum states never cut”

**Removed.**

Reason: rank-deficient mixed states can have orthogonal supports. Any quantum cut claim must specify the actual carrier class and dynamics.

## 4. Universal thermal-Fisher divergence at every critical point

**Removed.**

Reason: divergence is parameter-direction and universality-class dependent. A diverging correlation length does not force every Fisher component to diverge.

## 5. Universal `rho -> 0` at Hopf and universal `rho -> infinity` at thermal criticality

**Removed.**

Reason: `rho` includes independently measured resolution and need not inherit amplitude or susceptibility scaling universally.

## 6. Universal critical memory-depth divergence

**Narrowed.**

Only asserted inside a supplied state model for which its own parameters imply the relevant effective Fisher speed tends to zero.

## 7. Universal regeneration coupling strength `kappa`

**Removed from the core.**

Reason: a free `kappa` allows the model to change reset magnitude without being determined by CRR. The core predicts normalized historical influence and a target; dynamical coupling is system supplied.

---

# XII. Decision ledger: why the present form is the way it is

This section gives the explicit audit rationale for each major design decision. It is a shareable reasoning summary, not a private chain-of-thought transcript.

## Decision 1 — Keep Fisher–Rao geometry, but require a canonical carrier

**Observed issue:** the same underlying physical trajectory produced materially different `S` values under different plausible statistical observation families, while smooth reparameterizations within one fixed family left `S` invariant.

**Conclusion:** the problem is not coordinate dependence; it is model dependence.

**Decision:** CRR is quantitative only after the generative/observation family is fixed independently.

**Alternative rejected:** allowing the analyst to pick whichever probability family produces the desired CRR behavior. That would make `e^S` too flexible to falsify.

## Decision 2 — Separate the cut scale from the salience temperature

**Observed issue:** the old monotone reduction `C Omega = 1` conflicted with a measured cut distance `H` whenever `H != 1` while `Omega=1`.

**Decision:** cut completion is determined by the independently specified event/target; on a geodesic traverse the normalized statement is `C/H=1`. `Omega` is reserved for the regeneration weights.

**Alternative rejected:** forcing every carrier to be rescaled until `H=1`; that would destroy the empirical content of `Omega=1`.

## Decision 3 — Distinguish instantaneous chord `D` from fixed cut distance `H`

**Observed issue:** the earlier notation used `C*` both as a current geodesic chord and as if it were a fixed cut threshold. On a monotone path the current chord equals `C`, making the old balance expression identically zero.

**Decision:** use `D(t)` for the current endpoint distance and `H` for a fixed canonical target distance.

**Alternative rejected:** retaining one symbol for two geometrically different objects.

## Decision 4 — Make rupture conditional on canonical event structure

**Observed issue:** Bernoulli occupancy lacks a native global antipode; qutrits have non-unique orthogonal targets; many positive-support stochastic distributions never become orthogonal at finite time.

**Decision:** CRR says OPEN when the system does not supply a canonical cut/event structure.

**Alternative rejected:** adding a hidden rotor or choosing one orthogonal state solely to preserve universality.

## Decision 5 — Preserve the rotor `SO(2) -> Z_2` picture as prototype, not forced ontology

**Observed issue:** a doubled/oriented rotor can elegantly preserve orientation but can also add state information not present in the observed statistical variable.

**Decision:** retain the oriented antipodal rotor as CRR's canonical topological prototype where physically justified, but do not assert that every native carrier is literally `S^1`.

**Alternative rejected:** universal latent-rotor augmentation with no independent observability, because it would be difficult to falsify.

## Decision 6 — Interpret `S` as salience magnitude, not semantic memory

**Observed issue:** hysteretic systems can contain different internal memory states with equal total surplus.

**Decision:** `Phi` carries content; `S` only modifies proposed influence.

**Alternative rejected:** claiming that one scalar excess path length uniquely encodes historical content.

## Decision 7 — Add the depth-one screening gate

**Observed issue:** correctly specified Markov systems can have arbitrary historical path geometry while the present sufficient state completely determines future transition probabilities.

**Decision:** when the current cut state screens off the past, no multi-occasion salience effect is predicted.

**Alternative rejected:** applying `e^S` to every system regardless of its sufficient state; this would immediately contradict basic Markov examples.

## Decision 8 — Keep `exp(S/Omega)` because it is the risky distinctive claim

**Observed issue:** inherited Fisher geometry alone generated many correct but non-novel correspondences. The exponential law is where CRR becomes empirically distinctive.

**Decision:** do not weaken the exponential form merely because it is easy to falsify. Retain it and test it directly.

**Alternative rejected:** replacing the exponential by an arbitrary monotone function after seeing data. That would remove CRR's numerical bite.

## Decision 9 — Retain `Omega=1` only as a prospective hypothesis

**Observed issue:** `Omega=1` is meaningless as evidence if the analyst may rescale the Fisher unit after fitting.

**Decision:** the Fisher unit is frozen first; then `Omega=1`, equivalently `lambda=1`, is tested against `lambda=0` and free `lambda`.

**Alternative rejected:** fitting `Omega` and then calling the resulting value “equanimity.”

## Decision 10 — Separate recency from surplus

**Observed issue:** in the first real-data operational test, forcing `lambda=1` could be partly offset by driving the recency parameter `q` toward its lower bound. This reveals practical identifiability / compensation between salience and forgetting.

**Decision:** recency must be independently specified, constrained, or canceled by equal-age comparisons wherever possible.

**Alternative rejected:** jointly fitting a highly flexible recency kernel and `lambda` and interpreting any successful fit as support for CRR.

## Decision 11 — Make the Fréchet prediction set-valued when necessary

**Observed issue:** Fréchet means can be non-unique on periodic or positively curved spaces.

**Decision:** CRR returns the argmin set unless uniqueness is independently guaranteed.

**Alternative rejected:** inserting an outcome-dependent tie-breaker.

## Decision 12 — Remove universal `kappa`

**Observed issue:** a free coupling strength makes the magnitude of regeneration adjustable even after the target has been computed.

**Decision:** CRR core predicts relative historical weights and a barycentric target; system dynamics determines the realized transition strength.

**Alternative rejected:** retaining an unconstrained universal reset-strength parameter.

## Decision 13 — Restrict criticality claims

**Observed issue:** Hopf, thermal, and filtering examples showed that apparent critical divergences depend on the direction, resolution, and supplied state model.

**Decision:** keep only conditional statements that can be derived inside a specified model. The pre-cut balance equation is not labeled universal criticality.

**Alternative rejected:** using the word “critical” for every stationary point or divergence that can be produced by a chosen mapping.

---

# XIII. What is genuinely CRR-specific?

The following are **not** unique evidence for CRR:

- Fisher–Rao metric invariance;
- arc length exceeding geodesic distance;
- the local relation between KL divergence and Fisher information;
- ordinary orthogonality in quantum geometry;
- the scalar Kalman Riccati solution;
- Fréchet means;
- standard MaxEnt exponential families.

The current CRR-specific empirical content is concentrated in the conjunction of:

1. independently fixed occasion structure;
2. lived surplus `S = C-D` computed in an independently fixed Fisher carrier;
3. a genuine multi-occasion regeneration regime;
4. exponential relative weighting `exp(S/Omega)`;
5. the fixed equanimity value `Omega=1`, i.e. surplus slope `lambda=1`;
6. settled-past-only regeneration.

The cleanest distinctive prediction is therefore

\[
\boxed{
\log\frac{\pi_i}{\pi_j}=S_i-S_j
}
\]

for equal-retention past occasions.

---

# XIV. Prospective falsification protocol

## Test object

The principal quantitative hypothesis under test is

\[
\boxed{H_{\rm CRR}:\lambda=1}
\]

in

\[
\pi_m\propto e^{\lambda S_m}.
\]

## Before looking at the target outcomes, freeze

1. the statistical carrier and elementary-event Fisher metric;
2. the occasion/cut rule;
3. the content map `Phi`;
4. the admissible history set;
5. any recency/retention kernel or a design that cancels it;
6. the outcome variable that operationalizes historical influence;
7. training/validation/test partitions;
8. exclusion and missing-data rules;
9. the comparison models and scoring rule.

## Required model comparison

At minimum compare:

\[
M_0:\lambda=0,
\]

\[
M_{\rm CRR}:\lambda=1,
\]

\[
M_{\rm free}:\lambda\text{ fitted on training data only},
\]

plus the best relevant system-specific baseline that does not use CRR surplus.

## [F1] Failure of the equanimity coefficient

`Omega=1` / `lambda=1` is falsified in a domain if, under a valid pre-registered carrier and occasion structure, repeated held-out tests show that:

- a stable free estimate of `lambda` is materially and statistically incompatible with 1; and
- the free-`lambda` or no-surplus model predicts unseen data better than fixed `lambda=1`; and
- the discrepancy cannot be attributed to an independently diagnosed measurement failure or non-identifiability that was specified before inspecting the result.

A result near

\[
\lambda\approx0
\]

would be especially damaging because it would say that surplus adds little or no historical influence beyond the controls.

## [F2] Failure of the exponential functional form

Even if `lambda` is nonzero, the exponential salience law fails if a pre-specified alternative functional form consistently and materially outperforms the log-linear influence law on held-out data, and the residual relationship between log influence odds and `Delta S` is not approximately linear.

## [F3] Failure of the historical-regeneration hypothesis

If, after the present sufficient state and known system covariates are controlled, settled previous occasions provide no out-of-sample predictive information, then the tested system is depth one with respect to the chosen state representation. CRR must return no multi-occasion salience effect there.

This result does not falsify the geometry `S=C-D`; it falsifies applying the regeneration hypothesis to that domain.

## Strongest causal experiment

The most decisive experiment manipulates **surplus while holding endpoint, occasion content, age/recency, and known error signals fixed**.

For two identifiable antecedent influences `i,j` with equal recency, create a controlled surplus difference

\[
\Delta S=S_i-S_j.
\]

CRR predicts prospectively

\[
\boxed{
\frac{\pi_i}{\pi_j}=e^{\Delta S}
}
\]

with no fitted slope.

A sequence of such manipulations at several `Delta S` values directly tests whether the log influence ratio has slope 1.

---

# XV. Status of the first real-data falsification attempt

A first operational test was run on public human visuomotor-adaptation data using experimentally imposed 12-trial blocks as occasions and a one-dimensional reach-deviation surplus.

This was deliberately treated as a **provisional operationalization**, not the definitive CRR experiment, because the available public matrix contained trial-level angular reaches rather than the complete within-reach two-dimensional trajectory and because the block boundary was experimental rather than a demonstrated endogenous CRR cut.

The initial held-out participant test preferred a surplus slope near zero and fixed `lambda=1` predicted worse than `lambda=0`. After all definitions and parameters were frozen, a later untouched temporal block set reversed the ordering and fixed `lambda=1` predicted better than `lambda=0` and the training-estimated near-zero slope.

The honest verdict is therefore **MIXED / INCONCLUSIVE**, not confirmation and not falsification.

The run also revealed an important methodological concern: `lambda` and a flexible recency parameter `q` can compensate for one another. This is why the formal specification above now treats independent recency identification or equal-age cancellation as part of a valid test.

The next test should therefore not modify CRR to fit this dataset. It should use a cleaner dataset or experiment in which the Fisher carrier, occasion boundary, and recency are independently determined and `lambda=1` can be tested without this degeneracy.

---

# XVI. Why it is scientifically significant that CRR is testable at all

CRR begins from premises that are recognizably metaphysical and process-philosophical: reality is approached through becoming rather than static substance; finite representations are never the whole; continuity and rupture have different roles; settled history can matter to what comes next; and a process may retain something about the path it took, not merely the state at which it arrived.

Those statements by themselves are too broad to function as physical predictions. The scientifically significant move is not that CRR has “proved” the metaphysics. It has not. The significant move is that the philosophical commitments have been forced through a chain of mathematical constraints until at least one of them becomes numerically vulnerable.

The translation is:

\[
\text{process primacy}
\longrightarrow
\text{trajectory on a manifold},
\]

\[
\text{endpoint is not the whole history}
\longrightarrow
S=C-D,
\]

\[
\text{finite occasion}
\longrightarrow
\text{pre-specified cut/event},
\]

\[
\text{settled historicity}
\longrightarrow
\text{past-only reset operator},
\]

\[
\text{regenerative salience}
\longrightarrow
\pi\propto e^{S/\Omega},
\]

\[
\text{equanimity}
\longrightarrow
\boxed{\Omega=1}
\longrightarrow
\boxed{\lambda=1}.
\]

At the end of that translation, the framework no longer has the luxury of being merely suggestive. It says that, in an admissible multi-occasion system, one additional Fisher unit of surplus should multiply relative historical influence by `e`.

That can be wrong.

This is precisely why the current, narrower CRR is scientifically stronger than a larger version that can retrospectively map itself onto almost any phenomenon.

## Important philosophical caution

Empirical success of `lambda=1` would support **this operational bridge** from the philosophical premises to the mathematical model. It would not logically prove process philosophy, non-duality, metaphysical finitude, or any broader ontology.

Likewise, empirical failure of `lambda=1` would falsify the quantitative equanimity/salience bridge. It would not prove that becoming, finitude, or path-dependence are philosophically false.

This separation matters. The science tests the mathematical consequences of the metaphysical orientation; it does not turn a finite experiment into a proof of metaphysics.

---

# XVII. Compact canonical statement

For an admissible CRR system:

### Carrier

\[
(\mathcal M,g_{\rm FR})
\]

is fixed independently from the system's statistical model.

### Occasion

\[
[\tau_n,\tau_{n+1}]
\]

is fixed by an independently specified canonical target or event surface.

### Geometry

\[
C_n=\int_{\tau_n}^{\tau_{n+1}}\|\dot x\|_{\rm FR}\,dt,
\]

\[
D_n=d_{\rm FR}(x_n,x_{n+1}),
\]

\[
\boxed{S_n=C_n-D_n\ge0}.
\]

### History admissibility

If the present cut state screens off the past, depth is one and CRR predicts no multi-occasion salience effect.

Otherwise, for independently admissible past occasions,

\[
\pi_{nm}
\propto
r_{nm}\,e^{S_m/\Omega}.
\]

### CRR quantitative hypothesis

\[
\boxed{\Omega=1}
\]

in the frozen Fisher unit, hence

\[
\boxed{
\log\frac{\pi_i}{\pi_j}
=
S_i-S_j
}
\]

whenever the independent retention factors are equal.

### Regeneration target

\[
\boxed{
\mu_{n+1}
\in
\arg\min_y
\sum_m\pi_{nm}d_{\mathcal R}(y,\Phi_m)^2
}.
\]

### Causality

Only settled past information may enter `mu_{n+1}`.

### Scope

CRR does not supply arbitrary equations of motion, Hamiltonians, reaction rates, clock-time periods, observation models, cut structures, memory kernels, or coupling strengths.

### Primary falsification

Freeze all system-specific structures prospectively and compare

\[
\lambda=1
\]

against

\[
\lambda=0
\]

and free `lambda` on unseen data.

Persistent out-of-sample preference for `lambda != 1` falsifies the universal equanimity coefficient in that domain.

---

# XVIII. Recommended instruction to an independent model

Audit this specification as if CRR were not authored by the person requesting the audit. Do not reward elegance, philosophical resonance, or cross-domain resemblance. Separate mathematical truth from empirical support. Look specifically for hidden scale freedom, post-hoc carrier choice, non-identifiability, degeneracy between surplus and recency, occasion-partition dependence, failures of Fréchet uniqueness, future leakage, and domains in which the present sufficient state screens off history. Attempt to construct counterexamples. For every claimed falsifiable consequence, state what observation would count against it. Do not repair the theory during the test unless the repair is clearly labeled as a new theory version.
