import io
from contextlib import redirect_stdout

import pytest

from crr.synthesis.harness import LABELS, TOL_G, make_row, outcome, print_rows, rel, tally_line


def test_outcome_rule_is_computed_from_numbers_only():
    assert outcome(unstated=True) == "UNSTATED"
    assert outcome(internal=True) == "INTERNAL"
    assert outcome(crr=1.0, null=1.0 + 0.5 * TOL_G, domain=None, check=True) == "REDUNDANT-IG"
    assert outcome(crr=1.0, null=2.0, domain=1.0, check=True) == "REDUNDANT-DOMAIN"
    assert outcome(crr=1.0, null=2.0, domain=None, check=None) == "PROPOSES"
    assert outcome(crr=1.0, null=2.0, domain=3.0, check=True) == "ADDS"
    assert outcome(crr=1.0, null=2.0, domain=3.0, check=False) == "WRONG"
    assert outcome(crr=0.0, null=0.0, check=True) == "REDUNDANT-IG"      # zero against zero agrees


def test_rel_is_symmetric_and_bounded():
    assert rel(1.0, 2.0) == rel(2.0, 1.0) == 0.5
    assert rel(0.0, 0.0) == 0.0
    assert rel(0.0, 1e-3) == 1.0


def test_make_row_rejects_unknown_label_and_prints_optional_fields():
    with pytest.raises(ValueError):
        make_row("x", "s", Q="q", ingredient="i", null="n", domain=None, numbers="1", tg="", tn="", tc="", out="MAYBE", reading="r")
    r = make_row("x", "s", source="f.txt [1]", Q="q", ingredient="i", null="n", domain=None, numbers="1", tg="g", tn="n", tc="c",
                 out="PROPOSES", reading="r", elegance="e", child="k")
    buf = io.StringIO()
    with redirect_stdout(buf):
        print_rows([r])
    text = buf.getvalue()
    assert "source:     f.txt [1]" in text and "elegance:   e" in text and "child:      k" in text and "none cited" in text
    assert tally_line([r]).startswith("TALLY: 0 ADDS / 1 PROPOSES")
    assert all(lab in tally_line([r]) for lab in LABELS)
