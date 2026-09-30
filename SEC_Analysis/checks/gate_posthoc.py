"""SEC6-G's instrument rule applied POST HOC to the earlier SEC-family held-out rows (a report; decides nothing; not a re-score).

The rule is SEC6's, as hashed in prereg/sec6/PREREG.md (69c37965, commit 1bb1870) before its data. Per study, count the carriers
where the learner frozen after task 1 (P1's M6 = SEC6's `edge`, SEC_Analysis/checks/m_runs/) is not behind the tuned lambda
(M6 - tacc > -step, the family's own not-behind rule), with need = ceil(0.75 N) over the study's scored carriers. If that
count is at least need, the gate is CLOSED: the study's criterion is met by a learner that stops learning after task 1, so
its tuning-free row cannot show what it claims, and SEC6's rule would print it UNINFORMATIVE and cap it at PASS-0.

Applied here to SCL3-3, SEC3-3, SEC4-1 and SEC5-1, whose carriers all have M6 records. The ledger rows stand as scored under
their own pre-registrations, which had no such gate; this prints what the later rule would have said. POST HOC: the rule
was written on 2026-09-30 after P1 read these very records.

Run: uv run python SEC_Analysis/checks/gate_posthoc.py
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sec_lib as L  # noqa: E402
import m_checks as M  # noqa: E402

ROWS = {"scl3": ("SCL3-3", "PASS-0"), "sec3": ("SEC3-3", "FAIL"), "sec4": ("SEC4-1", "PASS-1"), "sec5": ("SEC5-1", "FAIL")}


def main():
    D = L.load_all(); R, _, _ = M._read_mruns()
    print("SEC6-G's instrument rule applied POST HOC to the earlier SEC-family rows (prereg/sec6/PREREG.md, hashed 69c37965);")
    print("a report: decides nothing and re-scores nothing; the ledger rows stand as scored under their own pre-registrations")
    print("M6 = the learner frozen after task 1 (SEC_Analysis/checks/m_runs, arm M6); tuned lambda and step from sec_lib (the frozen scorers' rule)")
    for st, (row, verdict) in ROWS.items():
        Cs = [C for (s, _), C in D.items() if s == st]
        n = len(Cs); need = math.ceil(0.75 * n); cnt = 0; parts = []
        for C in sorted(Cs, key=lambda C: C["carrier"]):
            recs = R[(st, C["carrier"])]["M6"]
            m6 = sum(r["acc"] for r in recs) / len(recs)
            nb = L.not_behind(m6, C["tacc"], C["step"]); cnt += nb
            parts.append(f"{C['carrier']} {m6 - C['tacc']:+.4f} (step {C['step']:.3f}){'' if nb else '*'}")
        gate = "CLOSED" if cnt >= need else "OPEN"
        consequence = (f"under SEC6-G's rule {row} ({verdict} as scored) would be printed UNINFORMATIVE and capped at PASS-0"
                       if gate == "CLOSED" else f"the criterion could fail here; {row} ({verdict} as scored) is not affected by the rule")
        print(f"\n[{st}] {row}: M6 not behind the tuned lambda on {cnt}/{n} (need {need}) -> gate {gate}; {consequence}")
        print("   M6 - tuned (* = behind): " + "; ".join(parts))


if __name__ == "__main__":
    main()
