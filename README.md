# crr-validation

*crr-validation — hosted as [`ashes_crr`](https://github.com/alexsabine/ashes_crr).*

![CI](https://github.com/alexsabine/ashes_crr/actions/workflows/ci.yml/badge.svg)

## What is CRR

CRR (Coherence–Rupture–Regeneration) is a process theory of how a finite
system moves through time. It has one state function — coherence, the
Fisher–Rao arc length travelled since the last cut on a statistical
manifold — one kind of event, the cut, and one rule for what comes after
a cut: regeneration from what has settled. It is shaped like
thermodynamics, not like mechanics: it supplies a unit, a state function,
an inequality that is an equality in a limiting case, and
maximum-entropy forms for what it cannot derive. It has no equations of
motion.

CRR is tested at cuts, and comparatively: a quantity CRR names must
predict something the system does better than the conventional quantity —
clock time, or endpoint displacement in a learner. The theory contains
four falsifiable hypotheses (H-CUT, H-L5, H-T1, H-EQ) and nothing else
that can be tested; every one must fail on a named synthetic surrogate
before it may enter a pre-registration, and a prediction that a generic
smooth signal would also satisfy is not a prediction of CRR.

CRR cannot forecast the content or the clock time of a future occasion.
Its predictions are relations that hold at cuts, inequalities, and
comparisons of regularity; persistence proves regeneratability, not
truth. What is future for a system can only be fed by what is already
past for something — nothing is fed by a future.

## Status

**No hypothesis has a held-out PASS.** Earlier work on CRR (before
September 2026) was withdrawn after independent audit and is not part of
this repository — see [docs/audit/2026-09-15-audit.md](docs/audit/2026-09-15-audit.md)
for the audit record.

## Reading order

Start here, in this order:

1. [docs/theory/primer.md](docs/theory/primer.md) — optional on-ramp:
   CRR in eight short sections, before the canonical statement.
2. [theory/CRR.md](theory/CRR.md) — the complete statement of the
   theory. Nothing outside this file is canonical.
3. [theory/checks/verify_math.py](theory/checks/verify_math.py) — proves
   every proposition in it
   (`uv run python theory/checks/verify_math.py`).
4. [CLAUDE.md](CLAUDE.md) — the working protocol (hash-before-data,
   surrogate gate, per-record scoring, one ledger). Binding for humans
   and agents alike.
5. [docs/runbook.md](docs/runbook.md) — environment, the full command
   sequence, and the reproduction policy.
6. [src/crr/instrument/core.py](src/crr/instrument/core.py) and
   [src/crr/surrogates/gate.py](src/crr/surrogates/gate.py) — the
   measurement library and the gate (references:
   [docs/modules/instrument.md](docs/modules/instrument.md),
   [docs/modules/surrogates.md](docs/modules/surrogates.md)).
7. [theory/SCOPE.md](theory/SCOPE.md) — which domains can be tested
   under this protocol and why; proposed propositions P6–P9 proved in
   [theory/checks/verify_scope_math.py](theory/checks/verify_scope_math.py).
   Planning only, not canonical.
8. [ledger/LEDGER.md](ledger/LEDGER.md) — every committed prediction and
   its outcome. Empty until a study runs.
9. [notebook/PROMPT_LOG.md](notebook/PROMPT_LOG.md) — every human
   prompt, verbatim (rule R13).
10. [docs/audit/2026-09-15-audit.md](docs/audit/2026-09-15-audit.md) —
    the 2026-09-15 audit record and the restructure programme it
    produced.

Status: no hypothesis has a held-out PASS. Study EQX (2026-09-15, three
unseen streams) found that the equanimity rule Ω = 1 reduces to a fixed
replay weight and does not beat ER-sum (`ledger/LEDGER.md` rows EQX-1..5,
`reports/eqx.md`). Study MEAS2 (2026-09-15, measles in 17 English cities,
the first Fisher-native carrier) found H-L5 fails in 0/17 cities under both
metrics (rows MEAS2-1..3, `reports/meas2.md`). The 2026-09-14 continual-learning
bundle is archived under `archive/` and recomputed in `audit/`; it is context,
not evidence.

The map of the repository — canonical, measurement, verification and
evidence layers, and how a number flows from instrument to report — is
[docs/architecture.md](docs/architecture.md).

## The protocol in one paragraph

The standing rules R1–R13 exist so that no number exists without a
committed script: every figure is emitted by code in this repository
with its output committed beside it; pre-registrations are hashed,
OpenTimestamps-anchored and signed-tagged before any data is touched;
every hypothesis must fail on a surrogate battery before it may enter a
prereg; scoring is per-record with the full distribution shown; the
ledger is the only curated document and it is append-only (rows ARC-*,
EQX-*, MEAS-*, MEAS2-* at the time of writing; no held-out PASS). The plain-language version is
[docs/protocol/rules.md](docs/protocol/rules.md) and the binding text is
[CLAUDE.md](CLAUDE.md).

## Contributing

[`theory/CRR.md`](theory/CRR.md) is canonical and human-owned: PRs do
not touch it. The protocol in [`CLAUDE.md`](CLAUDE.md) is binding for
humans and agents alike; every human prompt is logged verbatim in
[notebook/PROMPT_LOG.md](notebook/PROMPT_LOG.md) (rule R13). A PR must
leave the surrogate gates reading **GATE OPEN** and the ledger
append-only; if your change moves a gate number, re-run the gate and
commit the new output beside it.

```
uv run pytest tests
uv run python theory/checks/verify_math.py
uv run python theory/checks/verify_scope_math.py
uv run python -m crr.surrogates.gate L5
uv run python -m crr.surrogates.gate CUT
uv run python -m crr.surrogates.gate T1
uv run python -m crr.surrogates.gate EQ
uv run python -m crr.surrogates.gate L5R
uv run python -m crr.surrogates.gate A3
uv run python audit/recompute_2026-09-14.py
bash scripts/check_all.sh
```
