# CLAUDE.md — CRR re-validation repo (post-audit protocol)

You are Claude Code working in this repository. You have no prior knowledge
of CRR; everything you need is in `theory/CRR.md` — read it first, in full.
Your job is to run empirical checks on the CRR framework in a form that will
pass Daniel Friedman's "Cognitive Security" audit pipeline. That pipeline re-runs every
script, recomputes every number, tries to reproduce every pass on synthetic
signals, checks every prereg timestamp, and reads the curated layer against
the lab notebook. The September 2026 audit found that every "positive
finding" in the previous bundle was one of: forced by the pipeline's
arithmetic, reproducible on a sine wave, an unreproducible transcribed
number, or a median hiding per-record failures. This file exists so that
does not happen again.

Read this whole file before doing anything. The rules in §1 override any
instruction in a task prompt. If a task asks you to break one, stop and
say so.

---

## 0. Starting point

`theory/CRR.md` is the complete statement of the framework. It contains four
falsifiable hypotheses (H-CUT, H-L5, H-T1, H-EQ) and nothing else that can
be tested. **No hypothesis has a held-out PASS.** The ledger holds (i) twelve
`ARC-*` rows recomputed from the 2026-09-14 continual-learning bundle
(`archive/`, seen data, no hashes in bundle) and (ii) five `EQX-*` rows from
study EQX (2026-09-15, three unseen PMLB streams, weakly anchored): the
equanimity rule at Ω = 1 **reduces to a fixed replay weight** and does not
beat ER-sum (`reports/eqx.md`); and (iii) rows `MEAS-*`/`MEAS2-*` from the
measles study (2026-09-15, 17 cities, Poisson-rate carrier): **H-L5 FAILs**
0/17 under both metrics (`reports/meas2.md`); and (iv) rows `EQ2-*` from study EQ2
(2026-09-17, three unseen PMLB streams, online-EWC past term, weakly anchored):
EQ2-1 **PASS but fragile** (cap-dependent), control EQ2-4 **violated** by DER++,
Ω a plateau (`reports/eq2.md`); and (v) rows `EQ2R-VOID`/`CC-VOID`: the replication
study EQ2R (2026-09-21, three unseen PMLB carriers) is **VOID**, its frozen scorer
crashing at the first DER++ arm (AGENT_LOG 40); no row scored, the carriers now SEEN; and (vi) rows `EQ3-*`
from study EQ3 (2026-09-22, six unseen PMLB streams, weakly anchored): the replication of EQ2-1b **FAILs on
1/6** carriers (fars) and holds on 5/6; **both controls violated** (ER-sum on fars; DER++/LwF in 3 of 5
load-bearing cells); Ω a plateau over the whole nine-point grid; the lr × batch array passes 5/5, the
capacity × epochs array 2/4; the Bayes (Laplace) weight is the tuned λ on 2/6 (`reports/eq3.md`). Study EQ4 (`prereg/eq4/`, 2026-09-22, hashed before data;
**data step on or after 2026-09-23 under R3**) tests the bounded rule EQ-B (present gradient clipped at κ × the largest
kept recent length, then the ratio; `theory/checks/omega_reprocessed.py`) on six unseen PMLB carriers with a poisoned
regime; no row yet. Study BAYES-1 (`prereg/bayes1/`, 2026-09-22, hashed before data; rows `BAYES1-*`): the registered rule
against the exact sequential Bayes posterior on six unseen PMLB regression streams; **B0 NOT DECIDABLE** (the Bayes arm's
optimiser error 0.18–0.89 sd against a 0.1 tolerance), B1–B3 reported without verdict (the rule 5–18 sd from the posterior,
miscalibrated Bayes closer, no invariance under mini-batch noise; `reports/bayes1.md`). The epistemic status of the whole record is stated once in
`docs/notes/2026-09-22_epistemic_status.md` (read it before quoting any row).
Two earlier results (below) motivated H-L5
and H-T1; they were produced under a pipeline the audit rejected and are
context, not evidence. Both are *comparative* claims: a quantity CRR names
beats a conventional quantity at predicting something the system does.

- **L5 (p4581 stick-slip).** Fisher arc travelled since the last slip is a
  more regular predictor of the next slip than clock time: CV(arc-to-slip)
  < CV(time-to-slip) at 11/12 stress levels, stable under six segmentation
  perturbations, thinnest margin 0.5 %. Slogan: "change has its own clock."
- **T1 (toy LM).** Forgetting of an old task tracks Fisher path length
  travelled during fine-tuning (Σ√(2·KL_step)) better than the endpoint
  displacement (KL base→final on the new task): R² 0.89 vs 0.76, n = 20
  runs, gap opening on sawtooth schedules. Confounded by learning rate.
  Recomputed 2026-09-15 (ledger ARC-T1b): the endpoint KL on the **old**
  probe gives R² 0.99 on the same runs — the path did not beat the endpoint,
  it beat the wrong endpoint.

Treat all prior "confirmations" as if they do not exist. Do not cite them,
and do not go looking for earlier CRR documents or repositories: any
formulation not in `theory/CRR.md` is superseded and will confuse you.

---

## 1. Standing rules (non-negotiable)

**R1 — A number exists only if a committed script prints it.**
Every figure that appears in any table, ledger, report or README is emitted
by a script in this repo, and the stdout/JSON it came from is committed
beside it. No numbers from chat, memory, docstrings, or previous bundles.
If you cannot regenerate it, delete it.

**R2 — Hash before you look.**
Prereg + frozen scoring script in `prereg/<study>/`, and the frozen
instrument + theory code in `runs/<study>/frozen/`. Compute one `sha256sum`
over the two folders together (sorted file list — one hash over the prereg
folder plus the frozen-script folder), write it to
`prereg/<study>/HASH.txt`, anchor with OpenTimestamps (`ots stamp`), and
commit with a signed tag (`git tag -s prereg-<study>-<date>`). Only after
the tag exists may any data for that study be downloaded or opened. The
proof of "before" is the anchor, never a sentence in a file. Never write
"logged before scoring" or "sha256 in the logs" — write the hash.

**R3 — One prereg per dataset; no same-day rule reuse.**
A rule, unit, estimator or threshold defined or changed after seeing any
dataset may not be used on another dataset the same calendar day, and never
without a fresh prereg that names the change and the dataset it was
learned on. "Frozen" means the hash covers it.

**R4 — Every hypothesis must fail on a surrogate.**
Before a hypothesis is written into a prereg, run it on the surrogate
battery (§3). If any surrogate passes, the hypothesis is not about CRR and
is deleted. The surrogate results are committed in the prereg folder and
covered by the hash. The prereg states, per hypothesis, which surrogates
fail it and by how much.

**R5 — Implement what you claim to test.**
If the claim involves the antipodal cut, the code cuts at the antipode on
an intrinsic phase, not with `find_peaks`. If the claim involves a unit,
the unit is ONE named statistic (not "amplitude, drop or interval"),
real-valued, with no integer floor. Every estimator constant (filter
window, MAD vs std, ε guards, smoothing β, caps) is a named parameter,
listed in the prereg, and swept in a required sensitivity table.
Thresholds are never finer than one resolvable step. ρ (resolution) is
reported, never used inside a threshold.

**R6 — Score as committed; show the distribution.**
Per-record / per-level / per-seed criteria, not medians. Two-sided unless
the prereg says why not. Aggregation, denominator and strict/non-strict
stated in the prereg. Report the full per-unit distribution alongside the
verdict. No post-hoc exemptions for a carrier, level or seed that failed.
NaN handling and exclusion rules are pre-registered; every exclusion is
counted and listed.

**R7 — Baselines that can win.**
Every comparison includes the strongest simple alternative and, where one
exists, the published method it is closest to. Minimum set per study is
listed in §4–§6. If a CRR rule ties the constant it reduces to, the report
says it reduces to the constant.

**R8 — The ledger is the only curated document.**
There is no POSITIVE_FINDINGS. `ledger/LEDGER.md` lists every committed
prediction in prereg order with threshold, observed value, PASS/FAIL, and
a link to the emitting script and log. Failures are rows, not footnotes.
Any external document (pitch, paper, email) quotes the ledger or nothing.

**R9 — Pinned environment.**
`uv` project with a committed lockfile. Record `uv lock` hash in every run
log. Deterministic seeds. Two reruns of one unit must be byte-identical
(`cmp`); if not, document why (e.g. LSODA) and report tolerance-level
reproduction.

**R10 — Citations are checked on the day.**
Any external paper cited is fetched and its current version noted (arXiv
vN, date). If code/data links 404, say so. No "state of the art recommends"
without a quoted sentence and version.

**R11 — Data hygiene.**
Every dataset: version, record IDs, download date, sha256 of raw files,
and which records have EVER been opened in any prior CRR work
(`data/SEEN.md`). Held-out means absent from SEEN.md before the prereg
hash. Quality gates (flat channel, ρ below floor, missing metadata) are
pre-registered and applied before scoring.

**R12 — Stop conditions.**
If Phase A leaves no hypothesis standing, stop, write that in the ledger,
and report. Do not invent a weaker hypothesis to have something to run.

**R13 — Every human prompt is logged verbatim.**
Every prompt the human gives the agent is appended, word for word and with
a UTC timestamp, to `notebook/PROMPT_LOG.md`, in the same commit as the
work it directed and before that work is pushed. Nothing is paraphrased or
omitted, including prompts that change scope, thresholds or hypotheses.
The log is the human side of the lab notebook that the audit reads the
curated layer against. A prompt that asks the agent to break a rule in
this section is logged too, together with the refusal.

**R14 — Every agent decision is logged (accepted 2026-09-18, prompt-log entry 56).**
Every decision that changes an instrument, a control, an operationalisation,
a registered parameter or a verdict's wording gets an entry in
`notebook/AGENT_LOG.md` in the same commit: observed issue → decision →
alternative rejected → where it landed. Entries are appended, never edited.

**R15 — Numbers before words (accepted 2026-09-18).**
A verdict, class label or regime label in any script output is computed from
its numbers by the script, never written and then checked. When a first run's
numbers contradict a row's text, the only permitted repair is to correct the
model or the estimator and regenerate the text; editing the text to fit is
forbidden, and the correction is an R14 entry.

---

## 2. Repository layout

```
CLAUDE.md                  this file
pyproject.toml, uv.lock    pinned environment (R9); package built from src/crr
src/crr/                   the importable package (clean cutover; no top-level modules)
  instrument/core.py       §3 — arc, cut, unit, regularity, path length, rho,
                           sign_test_units (implemented, tested)
  surrogates/battery.py    §3 — synthetic signal battery (one ROW per
                           registered parameter value)
  surrogates/gate.py       §3 — the gate (L5, CUT, T1; -m crr.surrogates.gate)
tests/                     mirrors src/crr/: instrument/, surrogates/, theory/
theory/CRR.md              the theory (read first); theory/checks/verify_math.py proves every [P]
theory/SCOPE.md            domain scope review; proposed P6–P9 proved in theory/checks/verify_scope_math.py
theory/external/           owner-uploaded external documents, verbatim, with provenance (context, not theory)
theory/SPEC_RECONCILIATION.md  clause-by-clause reading of the external spec against CRR.md v3.1
theory/checks/verify_spec_math.py  every [T] item of the external spec, checked (output committed beside it)
theory/retrodictions/      issue-#21 retrodiction battery: script, pinned output, reading
theory/retrodictions/synthesis_batches/  SYNTHESIS re-reads of every CONSIST/DESCR row, five per batch
                           (QUEUE.md generated by build_queue.py; batch_NN.py + pinned batch_NN.txt; BRIEF.md)
src/crr/synthesis/harness.py  the SYNTHESIS outcome rule, row record and printer (tests/synthesis/)
docs/pedagogy/             ELEGANCE_LEDGER.md (generated by build_elegance_ledger.py from the pinned synthesis
                           outputs): pedagogical easement / elegance noticed while running the class; a record, not evidence
docs/notes/                notes to the auditor; quote the ledger or nothing (R8)
ontology/                  CRR's commitments against philosophy, contemplative traditions and metaphysics; the cut finding;
                           a fair review of all findings; next steps (notes, not evidence; every number from a pinned
                           output; checks/*.py + .txt pinned and CI-checked: cut_on_a_machine, turing_safety_ingression,
                           genesis_from_emptiness (exploratory, no verdict)); 09_free_energy_principle.md reads synthesis
                           batches 27-28 (the FEP: the clock, the Dirac boundary, equanimity, precision); 10_fep_and_crr.md the
                           side-by-side reading (time, Markov commitments, the tallies, the end of a model, future content)
Continuous_Learning/      the technical document on the Omega = 1 rule (PDF + Markdown source, figures drawn from pinned
                           records by build/make_figures.py with figures.txt pinned and CI-checked, build/build_pdf.py); a
                           note, not evidence (R8); CROSS_VERIFICATION.md reads the rule against existing methods
                           (battery theory/checks/omega_vs_methods.py, pinned, CI-checked); §7.6 the reprocessed mathematics
                           (theory/checks/omega_reprocessed.py) and the bounded rule EQ-B (gates EQB/EQBM; studies/eq4)
scripts/check_all.sh       thin orchestrator: provenance header + env + tests + checks + gates
prereg/PREREG_TEMPLATE.md  the pre-registration template (fields R4/R6/R9 require)
prereg/<study>/            PREREG.md, scoring script, surrogate results, HASH.txt, *.ots
data/                      raw data (gitignored) + SEEN.md + sha256 manifests
runs/<study>/              frozen scripts copied at hash time + logs + JSON outputs
runs/phaseA/               standing gate outputs (gate_L5.txt, gate_CUT.txt, gate_T1.txt)
ledger/LEDGER.md           §7 — the one curated table
notebook/PROMPT_LOG.md     R13 — every human prompt, verbatim, timestamped
notebook/AGENT_LOG.md      the agent-side decision ledger (observed issue, decision, alternative rejected)
docs/ROADMAP_2026-Q4.md    the programme: readiness for HumLab, studies in order, applied implications
reports/<study>.md         narrative, written AFTER the ledger row, quoting it
```

Rules for the layout:
- `prereg/` and `runs/<study>/frozen/` are write-once after the tag.
- `src/crr/` may evolve, but a study uses the copy frozen in its run dir
  (frozen-copy semantics unchanged: the hash covers the copy, not the tip).
- Nothing in `reports/` may contain a number absent from `runs/`.

---

## 3. Phase A — instrument and surrogate gate (no real data)

### 3.1 Instrument (`src/crr/instrument/core.py`) — implemented and tested

Run `uv run pytest tests` before anything else. The library provides
(extend it, never bypass it); every estimator constant is a named argument:

1. `arc_length(x, sigma=1.0, metric=None)` — real-valued Fisher–Rao arc
   length of a sampled path, in units of sigma. No integer step counting.
   The metric is a parameter: None (identity), a diagonal `g` (d,), or a
   full constant `g` (d,d). Companions: `chord(x, sigma, metric)` and
   `surplus(x, sigma, metric) -> (C, C*, S)`; S >= 0 by P1 up to
   floating-point round-off — report the sign distribution, never clamp.
2. `intrinsic_phase(x, detrend=True)` — unwrapped analytic-signal phase
   (radians). This is the ONE implemented intrinsic phase; a prereg may
   name another (a Poincaré section is a named alternative in
   `theory/CRR.md`), which must then be implemented and both reported.
3. `antipodal_cuts(phase, start=0, half_turn=pi)` — cut where the phase
   advances by half a turn from the last cut (oriented, sub-sample
   interpolated; strictly increasing indices, undersampling collisions
   dropped). This is A3. `peak_cuts(x, prominence, distance)`
   (find_peaks, maxima + minima) exists only so the two can be compared
   and the prereg can name cases where they differ.
4. `unit_sigma(stat, detrend_window=9, detrend_order=2, scale="mad",
   min_sigma=None)` — ONE resolvable-step statistic per study, chosen by
   name in the prereg. Robust scale of the detrended residual across
   TRAINING occasions; raises (rejects the record) on degenerate
   residuals or below min_sigma — no floor, no additive epsilon.
   `rho(extent, sigma) = extent/sigma` (A1' resolution) is for REPORTING
   (gates, reports, preregs); it is never an input to a threshold (R5).
5. `regularity(x, events, sigma=1.0, dt=1.0, n_boot=2000, seed=0,
   segment_end="inclusive")` — the
   L5 statistic: CVs of arc, clock and amplitude between consecutive
   events, mean arc per occasion (C_mean, in sigma), and paired bootstrap
   95% CIs on cv_arc−cv_clock and on cv_arc−cv_amp (the amplitude
   control). Raises below 3 events. `cv(v)` is unsigned (denominator
   |mean|). For cross-unit scoring use
   `sign_test_units(unit_stats) -> (win fraction, exact binomial p)` —
   per-unit first, then the sign test (R6). `segment_end="exclusive"` leaves a
   jump located at the event (an instantaneous reset) out of the arc: the
   jump is the cut, not content (A3); name the choice in the prereg.
6. `path_length(snapshots, kl=kl_step)` — C = Σ√(2·KL_step) on a fixed
   probe set; E = endpoint KL; C* = √(2E); S = C − C* (sign distribution
   reported). KL choices: `kl_step` (categorical (N,K); rows renormalised
   after the log guard) or `kl_gauss(mu_old, mu_new, var=1.0)` (regression;
   √(2KL) is then the exact Fisher–Rao distance, SCOPE.md P8).
   `occasions(x, cuts, sigma)` returns per-occasion (C, C*, S) between
   consecutive cuts.

---

### 3.2 Surrogate battery (`src/crr/surrogates/battery.py`) — implemented

Deterministic generators (one ROW per registered parameter value; row
names encode the parameter). Present now:

- S-A pure sine; S-A′ sine with period jitter (FM); S-A″ sine with
  amplitude jitter (AM); S-A‴ AM+FM.
- S-B sine + one Gaussian bump on the descent (the "dicrotic" surrogate).
- S-C two sin² lobes on a linear ramp (the "ECG" surrogate), registered
  at λ ∈ {0, 0.25, 0.5, 1}.
- S-D white noise added to S-A at ρ ∈ {5, 10, 20, 40, 80}.
- S-E asymmetric multi-harmonic (sin t + 1.2 sin 2t + 0.6 sin 3t).
- S-F van der Pol (μ = 5 and a registered μ = 1 row), Rössler
  (a=0.2, b=0.2, c=5.7), forced Duffing (δ=0.15, γ=0.3, ω=1). Integrators
  pinned to explicit RK45 on fixed eval grids (byte-identical reruns on
  the locked scipy, R9).
- S-G relaxation oscillator, clock-regular by construction (negative control
  for H-L5); S-G2 arc-regular by construction (positive control).
- S-H convex learner (linear model, squared loss): forgetting is a function
  of the endpoint only (lemma in `theory/checks/verify_scope_math.py`);
  H-T1 and H-EQ must FAIL on it. S-H2 wear learner: path-dependent
  forgetting by construction; H-T1 must PASS. Both in `LEARNER_BATTERY`.

### 3.3 The gate (`src/crr/surrogates/gate.py`) — implemented for L5, CUT and T1

`uv run python -m crr.surrogates.gate L5`, `... CUT` and `... T1` print one
row per surrogate with PASS/FAIL and flag any violation: a PASS on a negative
control (the hypothesis holds on a signal with no CRR content) or a FAIL on
a positive control (the instrument cannot see the effect). All three gates
currently read GATE OPEN; the standing Phase-A outputs are committed at
`runs/phaseA/gate_<hyp>.txt`. Commit the output into the prereg folder for
any study that uses the hypothesis; if you change the instrument, re-run the
gate and commit the new output.

Gated and CLOSED (2026-09-17): SAL — the occasion-weight law π ∝ e^{λS} as
salience-weighted replay (`prereg/sal/PHASE_A.md`, ledger SAL-A): no positive control
exists; a different operationalisation is a new study with its own gate.

Still to gate before use:
- EQ: add `gate_EQ` (design in `theory/SCOPE.md` §4.3: a convex replay
  learner on which H-EQ must FAIL, and a mismatched-gradient-scale learner
  on which it must PASS, both against ER-*sum*).
- H-F: add `gate_F` (design in `theory/SCOPE.md` §5: S-A″ and S-G must
  FAIL, S-A′ and S-G2 must PASS, on the quota-forecaster error) before any
  forecasting prereg.
- Any new hypothesis: add it to `MUST_FAIL`/`MUST_PASS` with a reason, then
  gate it. No hypothesis enters a prereg without a gate table.

---

## 4. Study L5x — "change has its own clock"

**Question.** Is Fisher arc accumulated since the last boundary a more
regular predictor of the next boundary than clock time, on systems and
records never used before?

**Data (must be absent from `data/SEEN.md`).**
- Marone-lab stick-slip experiments other than p4581, from the PSU
  ScholarSphere / lab repository (verify availability and version on the
  day; record DOI). Prefer experiments with several normal-stress levels.
- PhysioNet Autonomic Aging 1.0.0, records **0061–0120** (0001–0060 are
  SEEN). Boundary = pressure upstroke onset; quantity = arc from the
  dicrotic notch to the next onset vs clock.
- Optional third system after Daniel's review: Cascadia/Nankai slow-slip
  catalogues (natural time = events).

**Baselines (R7).** Clock CV; CV of amplitude-to-cut; CV of a
random-walk-scaled arc (arc computed with identity metric); CV of arc under
`peak_cut`. L5x is a result only if `antipodal_cut` arc beats all four.

**Pre-registered hypotheses (template; fill thresholds after the gate).**
- L5x-1 per level/subject: CV_arc < CV_clock. PASS if ≥ 80 % of
  levels/subjects and the paired-bootstrap 95 % CI of the median difference
  excludes 0. FAIL if < 60 % or CI includes 0.
- L5x-2 margin: median relative margin ≥ the smallest margin that survives
  the sensitivity sweep (state the number). Report all margins.
- L5x-3 antipode specificity — **diagnostic only, not a hypothesis** (v3.1):
  arc under `antipodal_cut` vs arc under `peak_cut`. `gate_A3` shows this
  comparison passes on jittered asymmetric surrogates with no CRR content
  (S-C, S-E) because the peak finder segments them inconsistently; it is
  reported per unit, never scored. A3 is tested only by H-CUT (own events
  vs antipode vs extremum), which needs its own gate.
- Quality gate: exclude units with ρ < ρ_floor (state it), flat channel,
  or < N cycles; count exclusions.
- Sensitivity table (required): phase method × filter window × prominence
  × ρ_floor. A verdict that flips in > 1 cell is reported as "fragile".

---

## 5. Study T1x — path length vs endpoint as a forgetting predictor

**Question.** Does forgetting track Fisher path travelled rather than
endpoint displacement, once learning rate is controlled?

**Design (the lr confound must be broken).**
- Fix lr; vary path length only through schedule: constant, sawtooth,
  cosine-with-restarts, injected gradient noise, and "loop" schedules that
  return near the start. Within each lr, path length must vary ≥ 3×.
- Separately vary lr at fixed schedule. Report partial correlation of
  forgetting with C_new, C_old, E_new, E_old controlling for lr and for
  final new-task loss.
- Fit predictors on half the runs, score R² on the held-out half. No
  in-sample R².
- n ≥ 60 runs per model.

**Models.** (a) a byte-level LM (`lm_bench.py`) — prior-work artifact, not
in this tree; recreate and freeze before T1x;
(b) GPT-2-small class model on a public domain stream; (c) the public
RL's Razor data (Shenfeld et al. 2025 — fetch, record version and link
status per R10) re-scored with path length if per-step checkpoints or
logs are available; if not, say so.

**Pre-registered hypotheses.**
- T1x-1: held-out R²(best of C_new, C_old) ≥ R²(best of E_new, E_old,
  EWC Fisher-weighted endpoint distance) + 0.05 with lr controlled. FAIL if
  any endpoint predictor wins by ≥ 0.05. (E_old is required: on a convex
  learner it is a sufficient statistic for forgetting — `theory/SCOPE.md`
  §4.1 — so a win over E_new alone would only show old probe beats new probe.)
- T1x-2: on the fixed-lr arm alone, Spearman(C, F) ≥ 0.6 and
  Spearman(E_new, F) < Spearman(C, F) − 0.2.
- T1x-3 (surrogate S-H control, in-prereg): on the convex learner,
  R²(C) − R²(E) ≤ 0.02 (`gate.py T1`; S-H2 must PASS in the same table).
- Report S/C* per run and whether high-S runs fall off the endpoint curve.

---

## 6. Study EQ — the "Ω = 1" equanimity rule, with the control it lacked

**What the ledger actually showed.** The adaptive rule
w = Ω·‖ḡ_present‖/‖ḡ_past‖ with Ω = 1 was within 1 pt of a fixed w = 1,
Fisher vs Euclidean made no difference, and the ER baseline in
`mlp_bench.py` (prior-work artifact, not in this tree; recreate and freeze
before any EQ prereg) concatenates stream and replay batches into one mean
loss (replay weight ≈ r), so "Ω = 1" may simply be "sum the two losses",
which is standard ER. The prereg estimator was also changed after Q1 failed.

**Design.**
- Use a standard CL framework for baselines (Mammoth, aimagelab) so ER,
  ER-ACE, DER++, CLS-ER, A-GEM, GEM and MEGA-I come from their reference
  implementations, not hand-rolled code. Record commit hash.
- Control arms (all pre-registered): ER-sum (replay loss summed, not
  averaged in) at every r; fixed w ∈ {r, 0.5, 1, 2, 4} at every r;
  loss-ratio balancing (MEGA-I) smoothed and unsmoothed.
- Estimator frozen at hash time: `ratio=ema, smooth=0.9, Fisher metric`.
  No change permitted after any run (R3). The Ω grid is
  {0.25, 0.35, 0.5, 0.71, 1, 1.41, 2, 2.83, 4}.
- Datasets: Split-CIFAR-10 (conv) — SEEN (confirmatory only per R11);
  Split-CIFAR-100 (10 tasks), Split-TinyImageNet, plus one LM domain
  stream (unseen). MNIST-family are SEEN and
  excluded. Standard and recurring streams. Seeds 0–4.
- lr × {¼, 1, 4} and batch × {½, 1, 2} on one dataset for invariance.

**Pre-registered hypotheses.**
- EQ-1 (reduction test, the important one): if EQ(Ω=1) is within 1.0 pt of
  the best fixed w on ≥ 2 of 3 image datasets, the rule REDUCES to a
  constant; report it as such and stop calling it adaptive.
- EQ-2 (theory value): Ω = 1 is the best grid point on ≥ 3 of 4 datasets
  and both neighbours (0.71, 1.41) trail by > 1.0. FAIL otherwise.
- EQ-3 (against real baselines): EQ(Ω=1, r=0.2) ≥ ER-sum(r=0.2) + 1.0 and
  ≥ best of {ER-ACE, DER++, CLS-ER} − 1.0 at equal compute. FAIL if
  ER-sum matches it.
- EQ-4 (invariance): optimum stays at Ω = 1 across lr and batch
  perturbations.
- EQ-5 (abundant memory, Cho effect): report only; no claim.
- Compute accounting: forward/backward counts per stream sample, logged.

If EQ-1 triggers, the ledger row reads "Ω = 1 ≡ fixed replay weight 1
(standard ER-sum)". That is an acceptable result.

---

## 7. Ledger and report format

`ledger/LEDGER.md`, one row per committed prediction, prereg order:

| id | prereg hash | dataset (unseen? Y/N) | prediction | threshold | observed | per-unit pass fraction | verdict | script | log |

Rules:
- Rows are appended, never edited; corrections are new rows referencing
  the old id.
- A PASS carries a level (accepted 2026-09-18; `docs/notes/2026-09-18_sharp_regime_review.md` §4):
  **PASS-0** (provisional): R2–R9 satisfied as written. **PASS-1** (a result):
  PASS-0 and the sensitivity table flips in at most one cell, no pre-registered
  control violated, no reduction to a constant, strong anchoring (OpenTimestamps
  or the two-person protocol), carrier admissibility stated (smoothing scale on
  a noisy carrier; segmentation rule for reset jumps). **PASS-2** (a finding):
  PASS-1 replicated on a second unseen carrier under a fresh prereg on a later
  day (R3), or by a second person on a second machine with the same frozen
  scripts, both rows referencing each other. Only a PASS-2 may be quoted
  outside the ledger as a finding.
- Retrodiction rows (theory/retrodictions/) are not ledger rows. Their grades
  are read as kind × outcome (DEF / INHERITED / CLASS / COMPARATIVE ×
  AGREES / DISAGREES / SILENT / INTERNAL); SHARP is retired for retrodictions
  and PROSPECTIVE CANDIDATE (the note's §3.2) is the only forward-looking label.
- A fourth kind, **SYNTHESIS** (owner request 2026-09-17, prompt-log entry 60;
  `docs/notes/2026-09-17_synthesis_class.md`; harness `theory/retrodictions/synthesis.py`):
  CRR taken whole against a domain's own mathematics, one proposition Q per row
  built with a CRR-proper ingredient (A3/D5, A6, P2/P3, A1′/D1, H-L5, D6/H-T1, H-EQ,
  A7/A8; the Fisher–Rao metric, arc, chord and surplus are information geometry's,
  not CRR's). Three printed tests decide the outcome: T-G ablation against the null
  (agree within 1 % → REDUNDANT-IG), T-N the domain's own theorem (→ REDUNDANT-DOMAIN),
  T-C the check in the domain's mathematics (holds → ADDS, fails → WRONG, unavailable
  → PROPOSES); INTERNAL and UNSTATED as in the note. ADDS is always a candidate: novelty
  is judged only by a named domain expert answering the note's three questions on the
  record. The harness carries its own gate (a positive control that must read ADDS, a
  decoy unit and a negative control that must not).
- "Observed" is printed at full precision plus rounded; never rounded
  alone at a boundary.
- Each study report (`reports/<study>.md`) is written after its rows exist,
  contains no number not in a row, includes the sensitivity table and the
  exclusion count, and ends with a "What a surrogate would have done"
  paragraph pointing at the gate table.

---

## 8. Command sequence for a study (copy this, in this order)

```bash
# 0. environment
uv sync --frozen && uv lock --check && uv run python -c "import numpy, scipy; print('ok')"

# 1. Phase A: instrument tests + surrogate gate
uv run pytest tests
uv run python -m crr.surrogates.gate <hypothesis-id> > prereg/<study>/gate_<hypothesis-id>.txt

# 2. write PREREG.md; copy frozen scripts
mkdir -p prereg/<study> runs/<study>/frozen
cp src/crr/instrument/core.py prereg/<study>/<study>_score.py theory/CRR.md runs/<study>/frozen/

# 3. hash + anchor + tag (BEFORE any data) — one hash over the prereg folder
#    plus the frozen-script folder (R2)
( cd prereg/<study> && find . ../../runs/<study>/frozen -type f | sort | xargs sha256sum > HASH.txt )
uv run ots stamp prereg/<study>/HASH.txt          # produces HASH.txt.ots
git add -A && git commit -m "prereg <study>" && git tag -s prereg-<study>-$(date -I) -m "prereg"
git push --tags

# 4. data (only now) — fetch_* and manifest are to write before the first study
uv run python data/fetch_<dataset>.py --records <range> && uv run python data/manifest.py
# append opened records to data/SEEN.md in the same commit

# 5. run once
uv run python runs/<study>/frozen/<study>_score.py > runs/<study>/stdout.txt
uv run python runs/<study>/frozen/<study>_score.py > runs/<study>/stdout_rerun.txt && cmp runs/<study>/stdout.txt runs/<study>/stdout_rerun.txt

# 6. ledger + report — append.py is to write before the first study
uv run python ledger/append.py runs/<study>/results.json
```

Never run step 4 or 5 before step 3's tag exists. If you find you must
change a script after step 3, the study is void: start a new study id.
`data/fetch_<dataset>.py`, `data/manifest.py` and `ledger/append.py` do not
exist yet: write them before the first study that needs them, and commit
them before that study's hash step.

---

## 9. What to send Daniel

The repo link at a tagged commit, plus:
- `ledger/LEDGER.md`
- `prereg/*/HASH.txt` and `.ots` proofs
- `data/SEEN.md` and manifests
- the gate tables
Nothing else. No summary slide, no "positive findings". If he asks for a
summary, it is the ledger with a one-line note per row.

---

## 10. Things you will be tempted to do; don't

- Widen a band "to the range seen so far".
- Report a median when the prereg said "per subject".
- Re-run with a different window and keep the better one.
- Write "held-out" about a rule learned on the same day.
- Quote a number from a docstring.
- Add a hypothesis after the gate because the list looks thin.
- Reinterpret a fail as "the information is in S but the shape can't use
  it". A fail is a fail; the reinterpretation is a new prereg.
