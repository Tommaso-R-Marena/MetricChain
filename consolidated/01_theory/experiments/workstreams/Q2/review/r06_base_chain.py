#!/usr/bin/env python3
"""r06_base_chain.py -- referee: the design M = 0 of Theorem A, exactly: the chain T[B; alpha = 1, m] over the REAL
base family (two-sample bracket of Proposition 11.57(a) at the accuracy X_B(N) = c'_N), by recursion with own code.
Reports ln cost/(N a) (the report, section 7.2 B: 1.319, 1.007, 0.938, 0.919 at N = 1e3, 4e3, 1.6e4, 6.4e4, u = 1),
checks the claim of Proposition T at every level with E = E_frakB and the type of the base family (Q5(b), e = 0)
at every base node."""
import math, sys, time
sys.dont_write_bytecode = True
import rlib
from rlib import LN2, INF

t0 = time.time()
u = 1.0
cu = rlib.Cube(u)
alpha = 1.0
Efun = lambda d, x, Lam: rlib.E_frakB(cu, d, Lam)
print("# u = 1, alpha = 1, delta = 0.05 and e^-N; chain over the real base bracket at accuracy X_B(N)")
for N in (1000, 4000, 16000, 64000):
    for ldn, ld in (("0.05", math.log(0.05)), ("e^-N", -float(N))):
        calX = rlib.X_B(cu, N)
        Bp = cu.a
        m = rlib.Chain.design_m(cu, N, Bp, calX, alpha, -ld + N * LN2)
        ch = rlib.Chain(cu, N, Bp, calX, alpha, m)
        c = ch.c
        recs = []
        d, l = N, ld
        tab = rlib.tables(u, m, c) if N >= ch.d0 else None
        while d >= ch.d0:
            jd = ch.j(d)
            a_d = ch.alow + jd * ch.w
            lev = rlib.Level(u, d, m, c, c, c, math.log(c), 2 * math.exp(u) * m / c, a_d - ch.w, l, 2, tab=tab)
            recs.append((d, l, lev, a_d))
            d, l = d - m, lev.ldp
        t, _ = rlib.base_lcost(cu, d, ch.alow, l)
        viol = 0
        minsl = INF
        minbase = INF
        if t > d * Bp + ch.e0(-l + d * LN2) + 1e-9:
            viol += 1
        for (d, l, lev, a_d) in reversed(recs):
            lc1, r1 = rlib.base_lcost(cu, d - m, calX, lev.ldp)
            # type of the base family at this node: b <= (d-m) a + E_frakB(d-m; ln(1/delta') + (d-m) ln 2)
            sb = (d - m) * cu.a + rlib.E_frakB(cu, d - m, -lev.ldp + (d - m) * LN2) - lc1
            minbase = min(minbase, sb)
            if sb < -1e-9:
                viol += 1
            t = lev.lcmax([calX, a_d - ch.w], [lc1, t])
            sl = d * Bp + ch.E_T(d, -l + d * LN2, Efun) - t
            minsl = min(minsl, sl)
            if sl < -1e-9 or lev.x_out > a_d + 1e-12:
                viol += 1
        print("N = %6d  delta = %-5s  block m = %4d  levels %3d  ln cost/(N a) = %.4f   ln cost - N a = %9.2f   bound of Theorem A (M = 0): N a + %.1f   "
              "least slack of the induction %.1f, of the type of the base family %.1f; violations %d   [%.0f s]"
              % (N, ldn, m, len(recs), t / (N * cu.a), t - N * cu.a, ch.E_T(N, -ld + N * LN2, Efun), minsl, minbase, viol, time.time() - t0), flush=True)
