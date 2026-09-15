# docs/ — the explanatory layer

Everything in this tree **explains and links**; it changes no claim and
owns nothing canonical. The theory is
[`theory/CRR.md`](../theory/CRR.md) and the binding protocol is
[`CLAUDE.md`](../CLAUDE.md) — on any conflict, those win.

## Index

| path | what it is |
|---|---|
| [architecture.md](architecture.md) | map of the repository: canonical / measurement / verification / evidence layers, and how a number flows from instrument to report |
| [theory/primer.md](theory/primer.md) | CRR for a newcomer: the theory's moving parts, the four testable hypotheses, and the code that implements each definition |
| [protocol/rules.md](protocol/rules.md) | the standing rules R1–R13 in plain language: what each says, where it lives, what breaks if violated |
| [protocol/study-lifecycle.md](protocol/study-lifecycle.md) | a study end to end: gate → prereg → hash → tag → data → frozen run → ledger → report, with what is forbidden at each step |
| [modules/instrument.md](modules/instrument.md) | the measurement library `src/crr/instrument/core.py`, function by function, with the definition each implements |
| [modules/surrogates.md](modules/surrogates.md) | the surrogate battery and the hypothesis gate: every generator, its control role, and how to run a gate |
| [modules/theory-checks.md](modules/theory-checks.md) | what `theory/checks/verify_math.py` and `verify_scope_math.py` prove, and which propositions are canonical vs proposed |
| [runbook.md](runbook.md) | environment, the full command sequence, the reproduction policy, and where committed evidence lives |
| [audit/2026-09-15-audit.md](audit/2026-09-15-audit.md) | the itemized audit record: method, baseline receipts, findings and dispositions |

## Suggested reading paths

- **Newcomer to the theory:** [theory/primer.md](theory/primer.md) →
  [`theory/CRR.md`](../theory/CRR.md) →
  [architecture.md](architecture.md).
- **About to run a study:** [protocol/rules.md](protocol/rules.md) →
  [protocol/study-lifecycle.md](protocol/study-lifecycle.md) →
  [runbook.md](runbook.md) →
  [`CLAUDE.md`](../CLAUDE.md) §4–§8 for the study brief.
- **Auditing the repo:** [audit/2026-09-15-audit.md](audit/2026-09-15-audit.md)
  → [`ledger/LEDGER.md`](../ledger/LEDGER.md) →
  [runbook.md](runbook.md) (reproduce everything yourself).
