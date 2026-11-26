#!/usr/bin/env python3
"""z08: the range condition W_j(b_j) <= 1 and the ratio j^2 (b_j - h)/c_*^2 for the chain of the cube, own code, to deeper
levels and for other cut levels than the report's (s_t = L + 0.05, b_0 = h + 0.003).  Usage: python3 z08_range.py J"""
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
import zrev

J = int(sys.argv[1]) if len(sys.argv) > 1 else 300
cu = zrev.Cube(1.0)
for dst, eps1, JJ in ((0.05, 0.003, J), (0.15, 0.003, min(J, 200))):
    t = time.time()
    C = zrev.Chain(cu, dst, eps1, JJ)
    js = [j for j in (10, 20, 40, 80, 160, 240, 320, 480) if j <= JJ]
    print("u = 1, s_t = L + %.2f, b_0 = h + %g: range condition for all j <= %d: %s (largest W_j(b_j) = %.4f at j = %d; W_j(b_j) at the last level %.4f)"
          % (dst, eps1, JJ, C.range_ok, max(C.Wtop), int(np.argmax(C.Wtop)), C.Wtop[-1]))
    print("    j^2 (b_j - h)/c_*^2 at j = %s: %s   [%.0f s]" % (js, " ".join("%.4f" % (j * j * (C.b[j] - cu.h) / cu.cstar2) for j in js), time.time() - t))
    sys.stdout.flush()
