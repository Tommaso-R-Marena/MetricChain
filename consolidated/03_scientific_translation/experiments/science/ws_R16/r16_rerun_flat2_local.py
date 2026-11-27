#!/usr/bin/env python3
"""
r16_rerun_flat2_local.py -- workstream R16, Item 4 (RE-RUN of the theory division's r8_flat.flat_run; python3 -I -B).
The exact two-level cost at the flat instance for EVERY outer dimension n_o in a window around the minimum found on the
grid of step 0.01 (r16_rerun_flat2.py), so that the minimum over the outer fraction is not an artefact of the grid.
usage: python3 -I -B r16_rerun_flat2_local.py <R8 dir of the export> <n> <n_o from> <n_o to> [stride]
"""
import math
import resource
import sys
import time

sys.path.insert(0, sys.argv[1])
import r8_flat as F          # noqa: E402   THEIR code (re-run)

n, lo, hi = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
stride = int(sys.argv[5]) if len(sys.argv) > 5 else 1
u = 1.0
pu = 1 / (1 + math.exp(u))
a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
t0 = time.time()
print("# r16_rerun_flat2_local.py started %s; n = %d, n_o = %d ... %d step %d" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), n, lo, hi, stride))
rows = []
for n_o in range(lo, hi + 1, stride):
    phi = (n_o + 0.5) / n                      # floor(phi n) = n_o
    r = F.flat_run(u, n, phi)
    assert r["n_o"] == n_o
    rows.append((r["lcost"] / (n * a), n_o))
best = min(rows)
print("n = %d: exact two-level cost at the flat instance, every n_o in [%d, %d] step %d (%d values): minimum %.4f at n_o = %d"
      " (phi = %.4f); values at the ends %.4f, %.4f   [%.0f s]"
      % (n, lo, hi, stride, len(rows), best[0], best[1], best[1] / n, rows[0][0], rows[-1][0], time.time() - t0))
print("      " + " ".join("%d:%.4f" % (no, c) for (c, no) in rows[::max(1, len(rows) // 40)]))
print("# finished %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("peak RSS MB", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)
