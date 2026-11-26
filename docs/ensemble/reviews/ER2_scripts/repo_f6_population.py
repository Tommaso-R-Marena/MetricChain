#!/usr/bin/env python3
"""ER2: what does check F6(iii) of experiments/ensemble/finite_temperature_checks.py actually compute?

The report (section 4a.2, numerical check F6) says: "chains of three sites with one violated bond: +0.23 to
+0.47, and there the population bound fails as well".  The script prints only the first return value of
ising_reference_case (the TV excess) for these five cases.  This driver replays the script's random stream
(tests F1..F5 first, then the body of test_F6 copied from the script) and prints BOTH return values.
It imports the repository module read-only (python -B); nothing is written to the repository.
"""
import sys, importlib.util
import numpy as np
import sys as _sys; _sys.dont_write_bytecode = True      # nothing is written next to the repository scripts
from er2_common import repo_root
REPO = repo_root()

path = REPO + "/experiments/ensemble/finite_temperature_checks.py"
spec = importlib.util.spec_from_file_location("ftc", path)
ftc = importlib.util.module_from_spec(spec); spec.loader.exec_module(ftc)

for fn in (ftc.test_F1, ftc.test_F2, ftc.test_F3, ftc.test_F4, ftc.test_F5):
    fn()                                     # advance the module-level generator exactly as main() does

rng = ftc.rng
# ---- body of test_F6, parts (i), (ii) unchanged (to keep the stream), part (iii) with both return values
w1 = wm1 = -np.inf
for t in range(6):
    n = 3; a = rng.choice((-1, 1), size=n)
    Jm = ftc.random_couplings(n, a, "chain" if t < 3 else "complete")
    w, wm = ftc.ising_reference_case(n, Jm, 0.7 * rng.normal(size=n), rng.uniform(0.4, 2.0), a)
    w1 = max(w1, w); wm1 = max(wm1, wm)
print(f"(i)  replayed: max TV excess {w1:+.2e}, max population excess {wm1:+.2e}   [stored output: +2.84e-14, +1.67e-16]")
w2 = wm2 = -np.inf
for n in (4, 5, 6, 7):
    for _ in range(3):
        a = rng.choice((-1, 1), size=n)
        w, wm = ftc.ising_reference_case(n, ftc.random_couplings(n, a, "complete", scale=0.6), 0.7 * rng.normal(size=n),
                                         rng.uniform(0.4, 2.0), a, exact=False)
        w2 = max(w2, w); wm2 = max(wm2, wm)
print(f"(ii) replayed: max TV excess {w2:+.2e}, max population excess {wm2:+.2e}   [stored output: +2.28e-15, +4.44e-16]")
rows = []
for _ in range(5):
    n = 3; a = rng.choice((-1, 1), size=n)
    Jm = ftc.random_couplings(n, a, "chain", floor=0.3); Jm[0, 1] = -Jm[0, 1]
    h = 0.7 * rng.normal(size=n); b = rng.uniform(0.4, 2.0)
    w, wm = ftc.ising_reference_case(n, Jm, h, b, a)
    rows.append((w, wm, Jm[0, 1] * a[0] * a[1], Jm[1, 2] * a[1] * a[2], b))
print("(iii) replayed, chains of three sites with the first bond violated:")
print("      TV excess (printed by the script) : " + ", ".join(f"{r[0]:+.3f}" for r in rows) + "   [stored output: +0.965, +0.522, +0.024, +0.062, +0.294]")
print("      population excess (NOT printed)   : " + ", ".join(f"{r[1]:+.3f}" for r in rows))
print("      J01 a0 a1 (violated), J12 a1 a2, b: " + "; ".join(f"({r[2]:+.2f}, {r[3]:+.2f}, {r[4]:.2f})" for r in rows))
print(f"      range of the TV excess: {min(r[0] for r in rows):+.3f} to {max(r[0] for r in rows):+.3f}   (the report quotes '+0.23 to +0.47')")
