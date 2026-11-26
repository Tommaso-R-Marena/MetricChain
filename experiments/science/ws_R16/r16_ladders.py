#!/usr/bin/env python3
"""
r16_ladders.py -- workstream R16: the certified two-level bound C_max (Theorem 11.56, base brackets inside) for TWO
ladders of the same outer constants (b = 0.5, lam = 0.2, eta = eta' = theta = 0.05, delta = 0.05, nu_1 = 2 e^u n_o/theta):
  (G) the geometric ladder of 40 rungs from 2 u n_i to b  -- the outer design of THY-RES-0013 section 4 / remark (1b) /
      the README (= the referee's r8_flat.flat_run; the engineering division's ENG-RES-0014 uses it);
  (K) the ladder of inner rates eps* 0.85^i (i < 40) of K_REPORT section 6.4 / theory report remark (1a) -- the design of
      the engineering division's ENG-RES-0008 (its line "ladder of inner rates eps*.0.85^i (i < 40)") and of our R6.
Own code (r16lib).  Purpose: the two-level worst cases quoted in remark (1b) at n = 1400, 2000, 8000, 32000, 64000 come
from ENG-RES-0008, i.e. from design (K); the certified three-level bound they are compared with is for design (G).
usage: python3 r16_ladders.py <n,n,...> <phi,phi,...>
"""
import math
import sys
import time
import r16lib as R

u = 1.0
a = R.a_of(u)
ns = [int(v) for v in sys.argv[1].split(",")]
phis = [float(v) for v in sys.argv[2].split(",")]
est = math.log(math.cosh(u / 2))
t0 = time.time()
print("# r16_ladders.py started %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("# ln(C_max)/(n a), two levels, u = 1")
for n in ns:
    for phi in phis:
        R.clear_tabs()
        n_o = R.n_outer(phi, n)
        n_i = n - n_o
        b, lam, eta, etap, theta = 0.5, 0.2, 0.05, 0.05, 0.05
        out = []
        for name in ("G", "K"):
            if name == "G":
                xs = R.geometric_ladder(2 * u * n_i, b, 40)
            else:
                xs = [2 * u * n_i]
                for i in range(40):
                    x = est * 0.85 ** i * n_i
                    if x > b * 1.0000001 and x < xs[-1]:
                        xs.append(x)
                xs.append(b)
            lev = R.Level(u, n, n_o, lam, eta, etap, math.log(theta), 2 * math.exp(u) * n_o / theta, b, math.log(0.05), xs)
            lcm, lC = R.two_level_bound(u, lev)
            out.append((name, lev.L, lcm / (n * a), lev.xout))
        print("n=%6d phi=%.2f: geometric ladder (L=%d): %.4f | ladder eps*0.85^i (L=%d): %.4f | difference %+.4f   [%.0f s]"
              % (n, phi, out[0][1], out[0][2], out[1][1], out[1][2], out[0][2] - out[1][2], time.time() - t0), flush=True)
print("# finished %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("peak RSS MB", R.peak_rss_mb())
