#!/usr/bin/env bash
# Thin orchestrator (R9/R11): sequences the standing checks. No logic beyond
# sequencing — each line is one documented command; the provenance header
# is the environment pin the CI log records.
set -euo pipefail

echo "== provenance =="
echo "commit: $(git rev-parse HEAD)"
if command -v sha256sum >/dev/null 2>&1; then
  echo "uv.lock sha256: $(sha256sum uv.lock | cut -d' ' -f1)"
else
  echo "uv.lock sha256: $(shasum -a 256 uv.lock | cut -d' ' -f1)"
fi
uv run python --version
echo

echo "== environment =="
uv sync --frozen
uv lock --check
echo

echo "== tests =="
uv run pytest tests
echo

echo "== theory checks =="
uv run python theory/checks/verify_math.py
uv run python theory/checks/verify_scope_math.py
echo

echo "== gates =="
uv run python -m crr.surrogates.gate L5
uv run python -m crr.surrogates.gate CUT
uv run python -m crr.surrogates.gate T1
echo

echo "== all checks done =="
