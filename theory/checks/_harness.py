"""Shared scaffolding for the theory check scripts (#4).

verify_math.py and verify_scope_math.py both consume this module: the named
check() with its FAILS counter, and the standard exit contract. stdout lines
and exit codes are identical to the pre-refactor scripts.
"""


class Harness:
    """Accumulating check() plus the shared finish() contract:

    print(); if FAILS: print(f"{FAILS} check(s) FAILED"); return 1
    else print("all checks passed") and return 0.
    """

    def __init__(self):
        self.fails = 0

    def check(self, name, ok, detail=""):
        print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}")
        if not ok:
            self.fails += 1

    def finish(self) -> int:
        print()
        if self.fails:
            print(f"{self.fails} check(s) FAILED")
            return 1
        print("all checks passed")
        return 0
