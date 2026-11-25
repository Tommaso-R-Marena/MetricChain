#!/usr/bin/env python3
"""t15 -- the accuracy e0 above which a free block beats the binary centre (symmetric two-phase case):
the binary branch R2(e) = max_x V(S2(x)) against the diluted branch R3(e) = local maximum of V(S3(lf, x)) near lf ~ 0.14.
usage: python3 t15_e0.py bJ u [lf_start x_start]"""
import sys, math, time
import numpy as np
import tlib as T
bJ, u = float(sys.argv[1]), float(sys.argv[2])
lf0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.14
x0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.272
K = T.Known(T.phi_cw(bJ, 0.0), u)
t0 = time.time()
def branches(e, warm):
    f2 = lambda p: -T.obj_blocks(K, e, K.v, *T.sym_profile("S2", p)) if 0 < p[0] < 0.5 else 0.0
    f3 = lambda p: -T.obj_blocks(K, e, K.v, *T.sym_profile("S3", p)) if (0.01 < p[0] < 0.9 and 0 < p[1] < 0.5) else 0.0
    p2, v2 = T._nm2(f2, [warm[0]])
    p3, v3 = T._nm2(f3, [warm[1], warm[2]])
    return v2, v3, p2, p3
warm = (0.298, lf0, x0)
rows = []
for e in np.linspace(0.006, -0.004, 11):
    v2, v3, p2, p3 = branches(e, warm)
    warm = (p2[0], p3[0], p3[1])
    rows.append((e, v2, v3))
    print(f"e={e:+.4f}: binary branch {v2:.8f} (x={p2[0]:.4f}) | diluted branch {v3:.8f} (lf={p3[0]:.4f}, x={p3[1]:.4f}) | diff {v3-v2:+.2e}   [{time.time()-t0:.0f}s]", flush=True)
rows = np.array(rows)
d = rows[:, 2] - rows[:, 1]
i = np.nonzero((d[:-1] > 0) & (d[1:] <= 0))[0]
if len(i):
    j = i[0]
    e0 = rows[j, 0] + (rows[j + 1, 0] - rows[j, 0]) * d[j] / (d[j] - d[j + 1])
    print(f"crossing: e0 = {e0:.5f}  (linear interpolation between the grid points {rows[j+1,0]:+.4f} and {rows[j,0]:+.4f})")
