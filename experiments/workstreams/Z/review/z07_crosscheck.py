#!/usr/bin/env python3
"""z07: rows of the coordinator's table of section 7.1 (experiments/workstreams/Z/out_z1_onelevel_u1.txt) recomputed with this
review's code (own chain, the Q2 referee's level evaluator): ln C_max at the coordinator's n_o, the type of the next curve, and
the exact minimiser of the proxy over ALL admissible n_o (the coordinator scans with a stride at d = 10^4)."""
import math
import sys

import numpy as np

sys.dont_write_bytecode = True
import zrev
import zlev

u = 1.0
cu = zrev.Cube(u)
C = zrev.Chain(cu, 0.05, 0.003, 14)
ld = math.log(0.05)
rows = [(1000, 0, 1.0, 17, 49.54, 26.28), (1000, 0, 10.0, 161, 46.66, 22.93), (1000, 6, 10.0, 287, 45.03, 18.32), (1000, 11, 30.0, 637, 38.00, 11.41),
        (10000, 0, 1.0, 25, 341.01, 314.68), (10000, 6, 1.0, 601, 332.51, 294.68), (10000, 6, 100.0, 3145, 270.99, 237.89),
        (10000, 11, 100.0, 2953, 269.82, 237.03), (10000, 11, 1000.0, 9913, 33.43, 6.78)]
print("#     d   j     xhat  n_o(coord.)  ln C_max: coord. / here    type(j+1): coord. / here   | exact argmin of the proxy, ln C_max there, Pi(argmin) - Pi(coord. n_o)")
worst = 0.0
for d, j, dy, no_c, lC_c, typ_c in rows:
    N = d
    X0 = zlev.X0(u, d)
    xh = X0 + dy
    y = dy
    Bs, Ws = C.grid(j, N)
    lines = zlev.Lines(Bs, np.minimum(Ws, 1.0))
    Bn, Wn = C.grid(j + 1, N)
    nxt = zlev.Lines(Bn, np.minimum(Wn, 1.0))
    inner = zlev.Sat(lines)
    r = zlev.level_Z2(cu, d, no_c, y, ld, inner.cost)
    typ = float(nxt.major(d, [xh])[0])
    nos, Pi = zlev.proxy_all(cu, d, y, lines)
    kb = int(np.argmin(Pi))
    r2 = zlev.level_Z2(cu, d, int(nos[kb]), y, ld, inner.cost)
    worst = max(worst, abs(r['lC'] - lC_c), abs(typ - typ_c))
    print("  %6d  %2d  %7.1f   %6d        %8.2f / %8.2f          %8.2f / %8.2f      | %6d  %8.2f  %9.4f"
          % (d, j, xh, no_c, lC_c, r['lC'], typ_c, typ, int(nos[kb]), r2['lC'], Pi[kb] - Pi[no_c - 1]))
print("largest difference to the coordinator's printed values: %.3f (they are printed with two decimals)" % worst)
