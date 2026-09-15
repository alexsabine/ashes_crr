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
5. `theory/SCOPE.md` — which domains can be tested under this protocol and
   why; proposed propositions P6–P9 proved in
   `theory/checks/verify_scope_math.py`. Planning only, not canonical.
6. `ledger/LEDGER.md` — every committed prediction and its outcome. Empty
   until a study runs.
7. `notebook/PROMPT_LOG.md` — every human prompt, verbatim (rule R13).

Status: no hypothesis has a held-out PASS. Study EQX (2026-09-15, three
unseen streams) found that the equanimity rule Ω = 1 reduces to a fixed
replay weight and does not beat ER-sum (`ledger/LEDGER.md` rows EQX-1..5,
`reports/eqx.md`). Study MEAS2 (2026-09-15, measles in 17 English cities,
the first Fisher-native carrier) found H-L5 fails in 0/17 cities under both
metrics (rows MEAS2-1..3, `reports/meas2.md`). The 2026-09-14 continual-learning bundle is archived under
`archive/` and recomputed in `audit/`; it is context, not evidence.

```
uv sync --frozen
uv run pytest instrument/tests
uv run python theory/checks/verify_math.py
uv run python theory/checks/verify_scope_math.py
uv run python surrogates/gate.py L5
uv run python surrogates/gate.py CUT
uv run python surrogates/gate.py T1
uv run python surrogates/gate.py EQ
uv run python surrogates/gate.py L5R
uv run python audit/recompute_2026-09-14.py
```
