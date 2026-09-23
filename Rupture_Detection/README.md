# Rupture Detection

The cut δ(Now) of CRR v3.1 (axiom A3) tested as a rupture detector on chaotic and oscillatory carriers, and the applied use
case the owner asked for (prompt-log entry 104). A note, not evidence (R8).

| file | what it is |
|---|---|
| `DECLARATION.md` | the tests, the gate, the expectations and what each outcome means; pushed before the first full run |
| `checks/rupture_checks.py` | the Phase-A battery (synthetic carriers with known change times; CUSUM on occasion statistics against clock windows, extremum occasions and the variance / lag-1 autocorrelation pair, at a matched false-alarm rate) |
| `checks/rupture_checks.txt` | its pinned output (CI-checked, byte-identical on rerun) |
| `RUPTURE_DETECTION.md`, `Rupture_Detection.pdf` | the result, how it differs from existing methods, and the applied use case mapped to the EPO's criteria (information, not legal advice) |
| `build/build_pdf.py` | the PDF builder (a copy of `AI_Safety/build/build_pdf.py` with the paths and title changed) |

Rebuild: `uv run python Rupture_Detection/checks/rupture_checks.py > Rupture_Detection/checks/rupture_checks.txt && uv run python Rupture_Detection/build/build_pdf.py`.
