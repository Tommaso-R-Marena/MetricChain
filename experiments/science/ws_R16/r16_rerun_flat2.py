#!/usr/bin/env python3
"""
r16_rerun_flat2.py -- workstream R16, Item 4.  A RE-RUN of the THEORY DIVISION'S code (their referee's
r8_flat.flat_run, imported read-only from the export; run with  python3 -I -B  so that nothing is written there).
This is NOT part of my replication (r16lib.py imports nothing of theirs); it is a separate check, labelled "re-run".

Question: against which TWO-LEVEL number is the certified three-level bound a theorem-grade comparison?
At the flat instance psi = 0 the two-level run (base brackets inside) is deterministic, so its number of evaluations
is an exact number for every outer fraction -- a lower bound on the worst case of that two-level algorithm in every
sense (every run on that instance), with no search and no "mean run" model.  For each n this script scans the outer
fraction phi on a fine grid and prints the minimum over phi of the exact flat cost of two levels, next to the certified
three-level bound of my own replication (read from my logs/rep_<n>.log, column 'searched').

usage: python3 -I -B r16_rerun_flat2.py <path of experiments/reviews/R8 in the export> <my logs dir> <n,n,...> [step, default 0.01]
"""
import math
import os
import re
import resource
import sys
import time

sys.path.insert(0, sys.argv[1])
import r8_flat as F          # noqa: E402   THEIR code (re-run)

logs = sys.argv[2]
ns = [int(v) for v in sys.argv[3].split(",")]
step = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01
u = 1.0
pu = 1 / (1 + math.exp(u))
a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
MINE = re.compile(r"n=(\d+) phi_1=([0-9.]+): two ([0-9.]+) \[.*?\] \| tuned ([0-9.]+) \[.*?\] \| searched ([0-9.]+) \[")
print("# r16_rerun_flat2.py (re-run of the theory division's r8_flat.flat_run); started %s"
      % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("# u = 1; ln(.)/(n a); outer design of the README (defaults of flat_run); phi grid 0.30 ... 0.85, step %g" % step)
t0 = time.time()
for n in ns:
    three = None
    path = os.path.join(logs, "rep_%d.log" % n)
    if os.path.exists(path):
        vals = [(float(m.group(5)), float(m.group(2))) for m in map(MINE.match, open(path)) if m]
        three = min(vals) if vals else None
    rows = []
    k = 0
    while True:
        phi = round(0.30 + k * step, 6)
        if phi > 0.85 + 1e-9:
            break
        r = F.flat_run(u, n, phi)
        rows.append((r["lcost"] / (n * a), phi, r["lCmax"] / (n * a), r["n_o"]))
        k += 1
    fl = min(rows)
    cm = min((c, p) for (_, p, c, _) in rows)
    below = [p for (f, p, _, _) in rows if three is not None and f <= three[0]]
    print("n = %6d: two levels at the flat instance (exact, deterministic): min over %d fractions = %.4f at phi = %.2f"
          " (n_o = %d); two levels certified C_max: min %.4f at phi = %.2f; certified three-level bound (my replication, "
          "'searched'): %s; margin exact-flat-two minus certified-three: %s; fractions at which the two-level flat cost is NOT"
          " above the certified three-level bound: %s   [%.0f s]"
          % (n, len(rows), fl[0], fl[1], fl[3], cm[0], cm[1],
             ("%.4f at phi_1 = %g" % three) if three else "n/a",
             ("%+.4f n a = %+.0f nats" % (fl[0] - three[0], (fl[0] - three[0]) * n * a)) if three else "n/a",
             ("%d of %d (phi from %.2f to %.2f)" % (len(below), len(rows), min(below), max(below))) if below else "none",
             time.time() - t0), flush=True)
    print("      flat cost by fraction: " + " ".join("%.2f:%.4f" % (p, f) for (f, p, _, _) in rows))
print("# finished %s; elapsed %.0f s" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.time() - t0))
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
