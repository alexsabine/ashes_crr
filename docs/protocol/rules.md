# The protocol in plain language — R1 to R13

> Explanatory summary. **CLAUDE.md is normative** — its §1 "Standing
> rules" override any task prompt; on any conflict, CLAUDE.md wins. Rule
> ids here match CLAUDE.md §1 exactly. For the lifecycle that ties them
> together, see [study-lifecycle.md](study-lifecycle.md).

---

**R1 — A number exists only if a committed script prints it.**
Every figure that appears in any table, ledger, report or README is
emitted by a script in this repo, and the stdout/JSON it came from is
committed beside it. No numbers from chat, memory, docstrings, or
previous bundles; if you cannot regenerate it, delete it.
*Where it lives:* every committed output under `runs/` — the Phase A gate
tables in `runs/phaseA/` are the existing examples.
*What breaks if violated:* unreproducible transcribed numbers — one of
the four failure modes the September 2026 audit found in every prior
"positive finding".

**R2 — Hash before you look.**
Prereg + frozen scoring script in `prereg/<study>/`; the frozen
instrument + theory code in `runs/<study>/frozen/`. Compute ONE
`sha256sum` over the two folders together (sorted file list) and write
it to `prereg/<study>/HASH.txt`, anchor with OpenTimestamps, and commit
with a signed git tag. Only after the tag exists may any data for that
study be downloaded or opened. The proof of "before" is the anchor,
never a sentence in a file — and never "logged before scoring" or
"sha256 in the logs": write the hash.
*Where it lives:* `prereg/<study>/`, lifecycle step 3–4 in
[study-lifecycle.md](study-lifecycle.md) (CLAUDE.md §8).
*What breaks:* "we pre-registered" becomes unverifiable — a prereg could
have been edited after seeing data and nothing could tell.

**R3 — One prereg per dataset; no same-day rule reuse.**
A rule, unit, estimator or threshold defined or changed after seeing any
dataset may not be used on another dataset the same calendar day, and
never without a fresh prereg that names the change and the dataset it was
learned on. "Frozen" means the hash covers it.
*Where it lives:* `prereg/` discipline.
*What breaks:* a rule quietly fitted on dataset A leaks into dataset B
on the same day, and "held-out" loses its meaning.

**R4 — Every hypothesis must fail on a surrogate.**
Before a hypothesis is written into a prereg, run it on the surrogate
battery. If any surrogate passes, the hypothesis is not about CRR and is
deleted. The surrogate results are committed in the prereg folder and
covered by the hash.
*Where it lives:* `src/crr/surrogates/gate.py` over the battery in
`src/crr/surrogates/battery.py`; committed outputs in `runs/phaseA/`;
catalogue in [modules/surrogates.md](../modules/surrogates.md).
*What breaks:* the "hypothesis" is satisfied by a sine wave — a claim
about generic signals, not about CRR.

**R5 — Implement what you claim to test.**
If the claim involves the antipodal cut, the code cuts at the antipode on
an intrinsic phase, not with `find_peaks`. If the claim involves a unit,
the unit is ONE named statistic — real-valued, no integer floor. Every
estimator constant is a named parameter, listed in the prereg, and swept
in a required sensitivity table. ρ (resolution) is reported, never used
inside a threshold.
*Where it lives:* `src/crr/instrument/core.py`
([modules/instrument.md](../modules/instrument.md)).
*What breaks:* the pipeline measures something adjacent to the claim —
e.g. waveform extrema standing in for A3 — and passes or fails for the
wrong reason.

**R6 — Score as committed; show the distribution.**
Per-record / per-level / per-seed criteria, not medians. Two-sided unless
the prereg says why not. Aggregation, denominator and strict/non-strict
stated in the prereg; the full per-unit distribution reported alongside
the verdict; no post-hoc exemptions for a carrier, level or seed that
failed; NaN handling and exclusions pre-registered, counted and listed.
*Where it lives:* `prereg/PREREG_TEMPLATE.md` fields; the per-unit
helpers in the instrument (`sign_test_units()`).
*What breaks:* a median hides per-record failures — another of the
audit's failure modes.

**R7 — Baselines that can win.**
Every comparison includes the strongest simple alternative and, where one
exists, the published method it is closest to. If a CRR rule ties the
constant it reduces to, the report says it reduces to the constant.
*Where it lives:* the per-study baseline lists in CLAUDE.md §4–§6; in the
gate, `E_old` is the required endpoint baseline for T1.
*What breaks:* a win over a strawman — no evidence value.

**R8 — The ledger is the only curated document.**
There is no POSITIVE_FINDINGS. `ledger/LEDGER.md` lists every committed
prediction in prereg order with threshold, observed value, PASS/FAIL, and
a link to the emitting script and log. Failures are rows, not footnotes.
Any external document quotes the ledger or nothing.
*Where it lives:* `ledger/LEDGER.md` (currently empty — that is the
honest state); report format rules in CLAUDE.md §7.
*What breaks:* a second curated document drifts from the evidence, and
external claims lose their anchor.

**R9 — Pinned environment.**
`uv` project with a committed lockfile; `uv lock` hash recorded in every
run log; deterministic seeds; two reruns of one unit must be
byte-identical (`cmp`); if not, document why and report tolerance-level
reproduction.
*Where it lives:* `pyproject.toml`, `uv.lock`, `.python-version`, run
procedures in [runbook.md](../runbook.md).
*What breaks:* results that depend on an unpinned interpreter or library
version and cannot be reproduced by an auditor.

**R10 — Citations are checked on the day.**
Any external paper cited is fetched and its current version noted (arXiv
vN, date). If code/data links 404, say so. No "state of the art
recommends" without a quoted sentence and version.
*Where it lives:* `theory/SCOPE.md` (data sources flagged "unverified
until fetched").
*What breaks:* citations to papers or data that turn out not to exist in
the cited form.

**R11 — Data hygiene.**
Every dataset: version, record IDs, download date, sha256 of raw files,
and which records have EVER been opened in any prior CRR work
(`data/SEEN.md`). Held-out means absent from SEEN.md before the prereg
hash. Quality gates (flat channel, ρ below floor, missing metadata) are
pre-registered and applied before scoring.
*Where it lives:* `data/SEEN.md`, `data/manifest.py`, `data/fetch_*.py`
(the latter two to be written before the first study — see
[study-lifecycle.md](study-lifecycle.md)).
*What breaks:* "held-out" data that an earlier bundle already opened.

**R12 — Stop conditions.**
If Phase A leaves no hypothesis standing, stop, write that in the ledger,
and report. Do not invent a weaker hypothesis to have something to run.
*Where it lives:* lifecycle gate in
[study-lifecycle.md](study-lifecycle.md).
*What breaks:* motivated hypothesis invention — science as busywork.

**R13 — Every human prompt is logged verbatim.**
Every prompt the human gives the agent is appended, word for word and
with a UTC timestamp, to `notebook/PROMPT_LOG.md`, in the same commit as
the work it directed and before that work is pushed. Nothing is
paraphrased or omitted — including prompts that change scope, thresholds
or hypotheses, and prompts that ask the agent to break a rule (those are
logged together with the refusal).
*Where it lives:* `notebook/PROMPT_LOG.md`.
*What breaks:* scope or threshold changes that no one can attribute —
the audit pipeline reads the curated layer against this log.
