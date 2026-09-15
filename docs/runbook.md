# Runbook — environment, commands, reproduction

> Explanatory procedures. The binding command sequence is CLAUDE.md §8;
> on any conflict it wins. See also
> [protocol/study-lifecycle.md](protocol/study-lifecycle.md) for the
> study narrative and [protocol/rules.md](protocol/rules.md) for R9.

## Environment

- **`uv` is the only entry point.** Never `pip`, never a bare `python`
  or `pytest` — they bypass the lockfile or pick the wrong interpreter.
- `uv.lock` is committed (R9). Its sha256 is part of the audit receipts
  ([audit record](audit/2026-09-15-audit.md)) and the `uv lock` hash is
  recorded in every run log.
- `.python-version` pins the interpreter (environment PR, audit #11);
  `pyproject.toml` declares `requires-python >= 3.11` and packages the
  library from `src/crr` (hatchling).
- Dependencies: numpy, scipy, sympy, pytest, opentimestamps-client.

```bash
uv sync --frozen        # exact locked environment
uv lock --check         # lockfile is current
```

## Full command sequence

The full check chain:

```bash
uv sync --frozen
uv run pytest tests                                        # tests/ mirrors src/crr/
uv run python theory/checks/verify_math.py                 # every [P] in CRR.md
uv run python theory/checks/verify_scope_math.py           # proposed P6–P9 + lemma
uv run python -m crr.surrogates.gate L5
uv run python -m crr.surrogates.gate CUT
uv run python -m crr.surrogates.gate T1
```

Or everything at once through the thin orchestrator — which sequences,
and does nothing but sequence:

```bash
bash scripts/check_all.sh
```

Its order: provenance header (git commit sha, sha256 of `uv.lock`,
`uv run python --version`) → `uv sync --frozen` → `uv lock --check` →
`uv run pytest tests` → `verify_math.py` → `verify_scope_math.py` →
gates L5 / CUT / T1. The header is the provenance record the audit
reads (audit #11).

Gate output is committed evidence: redirect to
`prereg/<study>/gate_<HYP>.txt` for a study ([lifecycle step 1](protocol/study-lifecycle.md));
the Phase A reference tables live in [`runs/phaseA/`](../runs/phaseA/).

For a study, follow [protocol/study-lifecycle.md](protocol/study-lifecycle.md)
exactly: prereg → `sha256sum` over the sorted file list → `uv run ots
stamp` → signed tag → **only then** data → frozen run → ledger row →
report.

## Reproduction policy (R9)

- **Deterministic seeds everywhere.** Every generator and bootstrap
  takes an explicit `seed` and defaults are fixed.
- **Two reruns of one unit must be byte-identical**, checked with `cmp`:

  ```bash
  uv run python runs/<study>/frozen/<study>_score.py > runs/<study>/stdout.txt
  uv run python runs/<study>/frozen/<study>_score.py > runs/<study>/stdout_rerun.txt
  cmp runs/<study>/stdout.txt runs/<study>/stdout_rerun.txt
  ```

- Byte-identity holds **on the locked versions** — that is what the
  lockfile buys. The ODE surrogates integrate with `solve_ivp` (RK45,
  tight tolerances); a scipy upgrade can change low-order digits, which
  is why the environment, not goodwill, carries the guarantee. If a
  component genuinely cannot be byte-identical (the protocol's example
  is an LSODA-class adaptive integrator), document why and report
  tolerance-level reproduction instead — that is the only sanctioned
  downgrade, and it must be stated in the run log.

## Where committed evidence lives

| path | contents |
|---|---|
| [`runs/phaseA/`](../runs/phaseA/) | the committed gate tables (`gate_L5.txt`, `gate_CUT.txt`, `gate_T1.txt`) — the emitting output for gate statistics quoted anywhere (R1) |
| `prereg/<study>/` | PREREG.md, gate output, `HASH.txt`, `*.ots` — write-once after the tag |
| `runs/<study>/` | frozen scripts copied at hash time + stdout + JSON outputs |
| [`ledger/LEDGER.md`](../ledger/LEDGER.md) | the one curated table — empty until a study runs; append-only |
| [`data/SEEN.md`](../data/SEEN.md) | every record ever opened in any CRR work (R11) |
| [`notebook/PROMPT_LOG.md`](../notebook/PROMPT_LOG.md) | every human prompt, verbatim (R13) |
