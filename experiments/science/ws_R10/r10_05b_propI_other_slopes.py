"""r10_05b: Proposition I (block-wise labels, <= 2 walls per block) at other slopes: lower bounds
for a = sup_t F_inf(t)/(1-t) and for h, to sharpen the (p,u) map near the crossover of `a`."""
import sys, time
import numpy as np
import r10_05_block_labels as B
from r10lib import cube_exponents
t0 = time.time()
for u in (1.5, 2.0):
    B.u = u; B.h = u / 2
    hc, tc, ac, Ec = cube_exponents(u)
    for p in (0.4, 0.3, 0.2):
        best_a = (0, None); best_h = (0, None)
        for L in (6, 10):
            for t in (0.97, 0.99, 0.999):
                v = B.prop_I(p, L, t, iters=1500) / (1 - t)
                if v > best_a[0]: best_a = (v, (L, t))
            for t in (tc - 0.04, tc, tc + 0.04):
                v = B.prop_I(p, L, t, iters=1500)
                if v > best_h[0]: best_h = (v, (L, round(t, 3)))
        print("u=%.1f p=%.1f: a >= %.6f at (L,t)=%s  (cube %.6f; ratio %.4f)   h >= %.6f at %s (cube %.6f; ratio %.4f)   (%.0fs)"
              % (u, p, best_a[0], best_a[1], ac, best_a[0] / ac, best_h[0], best_h[1], hc, best_h[0] / hc, time.time() - t0), flush=True)
