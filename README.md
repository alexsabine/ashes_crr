# crr-validation

Empirical validation of CRR (Coherence–Rupture–Regeneration), a process theory
of how finite systems move through time, under an audit-grade protocol.

Start here, in this order:

1. `theory/CRR.md` — the complete statement of the theory. Nothing outside
   this file is canonical.
2. `theory/checks/verify_math.py` — proves every proposition in it
   (`uv run python theory/checks/verify_math.py`).
3. `CLAUDE.md` — the working protocol (hash-before-data, surrogate gate,
   per-record scoring, one ledger). Binding for humans and agents alike.
4. `instrument/` and `surrogates/` — the measurement library and the gate.
5. `ledger/LEDGER.md` — every committed prediction and its outcome. Empty
   until a study runs.

Status: no hypothesis has a held-out PASS. Earlier work on CRR (before
September 2026) was withdrawn after independent audit and is not part of
this repository.

```
uv sync
uv run pytest instrument/tests
uv run python theory/checks/verify_math.py
uv run python surrogates/gate.py L5
uv run python surrogates/gate.py CUT
```
