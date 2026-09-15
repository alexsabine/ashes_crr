# Repository architecture

> Explanatory map of the tree. The protocol's own layout statement is
> CLAUDE.md §2; on any conflict it wins.

The repo separates **what is believed** (canonical), **what is measured**
(instrument), **what is proved** (symbolic checks), and **what was
actually run** (evidence). `docs/` — this tree — is a fourth, strictly
explanatory layer.

## The tree

```text
crr-validation (hosted as ashes_crr)
├── CLAUDE.md                  binding protocol (normative for humans and agents)
├── pyproject.toml, uv.lock    pinned environment (R9); .python-version pins the interpreter
├── theory/
│   ├── CRR.md                 the theory — canonical, human-owned
│   ├── SCOPE.md               domain scope review; proposed P6–P9 (planning only, not canonical)
│   └── checks/
│       ├── verify_math.py         proves every [P] in CRR.md
│       ├── verify_scope_math.py   proves proposed P6–P9 + the convex-learner lemma
│       └── _harness.py            shared check scaffolding
├── src/crr/                   the measurement layer (installable package)
│   ├── instrument/core.py     instrument definitions: unit (A1′), arc/chord/surplus (D2–D4),
│   │                          cut (A3), regularity (H-L5), learner path length (D6)
│   └── surrogates/
│       ├── battery.py         deterministic synthetic signals — NO CRR content
│       └── gate.py            the hypothesis gate (R4)
├── tests/                     mirrors src/: instrument/, surrogates/, theory/
├── scripts/
│   └── check_all.sh           thin orchestrator: provenance header → sync → lock-check → tests → checks → gates
├── prereg/                    one folder per study: PREREG.md, gate output, HASH.txt, *.ots
│   └── PREREG_TEMPLATE.md
├── data/                      SEEN.md (R11) + fetch/manifest helpers (to be written); raw data gitignored
├── runs/
│   ├── phaseA/                committed gate outputs (gate_*.txt) — the emitting evidence for gate numbers
│   └── <study>/               frozen scripts copied at hash time + stdout + JSON outputs
├── ledger/LEDGER.md           the one curated table (R8) — currently empty
├── reports/                   narrative per study, written AFTER the ledger row
├── notebook/PROMPT_LOG.md     every human prompt, verbatim (R13)
└── docs/                      this explanatory tree
```

## Layers

**Canonical layer — human-owned, PRs do not touch it.**
[`theory/CRR.md`](../theory/CRR.md) is the complete statement of the
theory: every [A]/[D]/[P]/[H]/[O] line lives there and nowhere else.
[`CLAUDE.md`](../CLAUDE.md) is the binding protocol: the standing rules
R1–R13, the surrogate battery specification, the per-study designs and
the command sequence. Both are linked, explained — never paraphrased
into authority — by [docs/theory/primer.md](theory/primer.md) and
[docs/protocol/rules.md](protocol/rules.md).

**Measurement layer — `src/crr/instrument`.**
The instrument implements exactly the definitions the theory names: the
unit σ (`unit_sigma`, A1′), arc/chord/surplus (`arc_length`/`chord`/
`surplus`, D2–D4), the cut (`intrinsic_phase` + `antipodal_cuts`, A3 —
with `peak_cuts` present only to show disagreement), regularity
(`regularity`, H-L5), and learner path length (`kl_step`/`kl_gauss`/
`path_length`, D6). Function-by-function reference:
[modules/instrument.md](modules/instrument.md). Studies may extend it,
never bypass it — and a study runs the copy frozen in its run dir.

**Measurement layer — `src/crr/surrogates`.**
`battery.py` holds the deterministic generators with no CRR content;
`gate.py` runs each hypothesis against them and flags violations. This
is rule R4 made executable. Catalogue and semantics:
[modules/surrogates.md](modules/surrogates.md). Its tests
(`tests/surrogates/test_gate.py`) pin the per-control verdicts and the
GATE OPEN contract for every gate (audit #3).

**Verification layer — `theory/checks`.**
`verify_math.py` proves every [P] in the canonical theory;
`verify_scope_math.py` proves the *proposed* P6–P9 and the
convex-learner lemma that SCOPE.md relies on. See
[modules/theory-checks.md](modules/theory-checks.md). Its tests
(`tests/theory/test_checks.py`) run both scripts from the repo root and
assert exit 0.

**Evidence chain — `prereg/ → runs/ → ledger/ → reports/`.**
Written-once after hash: `prereg/<study>/` (prereg + gate output +
`HASH.txt` + OpenTimestamps proof) and `runs/<study>/frozen/` (scripts
copied at hash time). Committed stdout/JSON under `runs/<study>/` are
the only source a report may quote. `ledger/LEDGER.md` is the one
curated document (R8); `reports/<study>.md` may contain no number
absent from `runs/`. Lifecycle: [protocol/study-lifecycle.md](protocol/study-lifecycle.md).

**Lab notebook — `notebook/PROMPT_LOG.md`, `data/SEEN.md`.**
The audit pipeline reads the curated layer against the lab notebook:
every human prompt verbatim (R13), and every record ever opened in any
CRR work (R11), so "held-out" means something.

## The data-flow of a study

```text
  instrument (src/crr/instrument)      gate (src/crr/surrogates/gate.py)
              │                                │
              └──────────┬─────────────────────┘
                         ▼
        prereg/<study>/  PREREG.md + gate_<HYP>.txt
                         │  sha256 over sorted file list → HASH.txt
                         │  OpenTimestamps anchor (HASH.txt.ots)
                         │  signed tag prereg-<study>-<date>
                         ▼
                    data fetched and opened (checked against data/SEEN.md)
                         ▼
        runs/<study>/frozen/  →  run once → rerun → cmp byte-identical (R9)
                         ▼
        ledger/LEDGER.md  one row per committed prediction (appended, never edited)
                         ▼
        reports/<study>.md  narrative quoting the ledger, nothing else
```

Nothing may jump a stage: no data before the tag (R2), no ledger row
without a frozen run, no report number without a row (R1, R8). The full
narration is [protocol/study-lifecycle.md](protocol/study-lifecycle.md).
