"""The SYNTHESIS-class harness: outcome rule, row record and printer shared by every synthesis battery
(design: docs/notes/2026-09-17_synthesis_class.md; first battery: theory/retrodictions/synthesis.py).

A row states ONE proposition Q about a domain in the domain's own terms, built with at least one CRR-proper
ingredient. Three printed tests decide the label (R15: the label is computed from the numbers, never written):

  T-G  ablation: the decisive quantity with the ingredient (`crr`) and with its null replacement (`null`);
       agreement within TOL_G means the ingredient did no work -> REDUNDANT-IG
  T-N  the domain's own theorem for the same target (`domain`, or None if none is cited); agreement within
       TOL_N means the domain already has Q -> REDUNDANT-DOMAIN
  T-C  the check in the domain's own mathematics (`check`: True / False / None) -> ADDS / WRONG / PROPOSES

INTERNAL: two readings of the ingredient disagree on the domain. UNSTATED: no Q could be formed.
ADDS is always a candidate: novelty is judged only by a named domain expert (note, section 4).

Elegance record (owner request, prompt-log entry 61): a row may carry an `elegance` note and a `child`
explanation (a fifth-grader version). They are printed with the row, pinned with it, and collected into
docs/pedagogy/ELEGANCE_LEDGER.md by docs/pedagogy/build_elegance_ledger.py. They are a record, not evidence,
and they carry no number that the row does not print.
"""
from __future__ import annotations

TOL_G = 1e-2     # T-G: the ingredient did work only if CRR value and null differ by more than 1 % (relative)
TOL_N = 1e-2     # T-N: the domain already has Q if its own theorem gives the CRR value within 1 % (relative)
LABELS = ("ADDS", "PROPOSES", "REDUNDANT-IG", "REDUNDANT-DOMAIN", "WRONG", "INTERNAL", "UNSTATED")
FIELDS = ("source", "Q", "ingredient", "null", "domain", "numbers", "tg", "tn", "tc", "outcome", "reading",
          "weakness", "elegance", "child")


def rel(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1e-12)


def outcome(crr=None, null=None, domain=None, check=None, internal: bool = False, unstated: bool = False) -> str:
    """The label, from the numbers only."""
    if unstated:
        return "UNSTATED"
    if internal:
        return "INTERNAL"
    if rel(crr, null) <= TOL_G:
        return "REDUNDANT-IG"
    if domain is not None and rel(crr, domain) <= TOL_N:
        return "REDUNDANT-DOMAIN"
    if check is None:
        return "PROPOSES"
    return "ADDS" if check else "WRONG"


def make_row(cls: str, system: str, *, source: str = "", Q: str, ingredient: str, null: str, domain: str | None,
             numbers: str, tg: str, tn: str, tc: str, out: str, reading: str, weakness: str = "",
             elegance: str = "", child: str = "") -> dict:
    if out not in LABELS:
        raise ValueError(out)
    return dict(cls=cls, system=system, source=source, Q=Q, ingredient=ingredient, null=null, domain=domain,
                numbers=numbers, tg=tg, tn=tn, tc=tc, outcome=out, reading=reading, weakness=weakness,
                elegance=elegance, child=child)


def print_rows(rows: list[dict], start: int = 1) -> None:
    for k, r in enumerate(rows, start):
        print(f"[{k:2d}] ({r['cls']}) {r['system']}")
        if r.get("source"):
            print(f"     source:     {r['source']}")
        print(f"     Q:          {r['Q']}")
        print(f"     ingredient: {r['ingredient']}")
        print(f"     null:       {r['null']}")
        print(f"     domain:     {r['domain'] if r['domain'] else 'none cited'}")
        print(f"     numbers:    {r['numbers']}")
        print(f"     T-G:        {r['tg']}")
        print(f"     T-N:        {r['tn']}")
        print(f"     T-C:        {r['tc']}")
        print(f"     OUTCOME:    {r['outcome']}")
        print(f"     reading:    {r['reading']}")
        if r.get("weakness"):
            print(f"     weakness:   {r['weakness']}")
        if r.get("elegance"):
            print(f"     elegance:   {r['elegance']}")
        if r.get("child"):
            print(f"     child:      {r['child']}")
        print()


def tally_line(rows: list[dict], label: str = "TALLY") -> str:
    return f"{label}: " + " / ".join(f"{sum(1 for r in rows if r['outcome'] == lab)} {lab}" for lab in LABELS)


def run_batch(title: str, rows: list[dict]) -> int:
    """Print a batch in the standard form. Returns 0 (the batch has no gate; the class gate is synthesis.py's)."""
    print(title)
    print(f"T-G tolerance {TOL_G:g} (relative), T-N tolerance {TOL_N:g} (relative); labels computed by outcome() from the numbers (R15)")
    print()
    print_rows(rows)
    print(tally_line(rows))
    return 0
