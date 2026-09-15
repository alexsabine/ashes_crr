"""The verify scripts must run in a clean subprocess from the repo root and
exit 0 (#4)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run(script):
    return subprocess.run([sys.executable, script], cwd=ROOT,
                          capture_output=True, text=True)


def test_verify_math_exits_zero():
    r = _run("theory/checks/verify_math.py")
    assert r.returncode == 0, f"stdout:\n{r.stdout}\nstderr:\n{r.stderr}"
    assert "all checks passed" in r.stdout


def test_verify_scope_math_exits_zero():
    r = _run("theory/checks/verify_scope_math.py")
    assert r.returncode == 0, f"stdout:\n{r.stdout}\nstderr:\n{r.stderr}"
    assert "all checks passed" in r.stdout
