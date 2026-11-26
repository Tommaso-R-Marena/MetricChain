#!/usr/bin/env python3
"""Z3: the nested construction of Z_REPORT sections 4-6 evaluated EXACTLY at small scale.

k levels of section 4 (one level over a grid family of the cut orbit curve, outer block by the proxy), each followed
by the chain of section 5 (q2lib.Chain: exact recursion with the constants of every level), over a base that
SATURATES the flat type b_0 (certified cost exactly d b_0 at every accuracy >= 1).  The certified cost of the whole
nest at (N, accuracy 1, delta) is computed by the recursion through all levels, chains and dimensions, with the two
exact one-level evaluators (q2lib.Ev), and compared with

    max over the lines of W_k of [N B - sigma]  +  E_k(N, 1; Lambda_0),        E_k the error unrolled as in section 6.

At every node visited (every level of section 4, every level of every chain, every call of a combined family) the
inequality of the induction is checked: (U-infinity), the accuracy, the type of Proposition Z3, the type of
Proposition Z4, and q2lib's own checks of Proposition T.
What this tests that z1_onelevel.py does not: the composition - failure probabilities handed down through levels
and chains, the error functions, the chain over a family that is itself a level over a chain.
What it does not test: the real base (Theorem A of Q2: forty levels more), sizes at which the bound is below N a.
Two sequences of curves (argument `mode`): 'cut' - the cut orbit curves from b_0 = h + eps1 (base: saturating flat type b_0);
'env' - the envelope sequence from b_0 = a (base: saturating flat type a; Z_ADDENDUM.md).
Usage: python3 z3_nest.py [u] [eps1] [N] [k] [mode]        (default 2.0 0.02 6000 2 cut)
"""
import math
import sys
import time

import numpy as np

import zetalib as Z

Q2 = Z.Q2
LN2 = math.log(2.0)
u = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
eps1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02
N = int(sys.argv[3]) if len(sys.argv) > 3 else 6000
k = int(sys.argv[4]) if len(sys.argv) > 4 else 2
mode = sys.argv[5] if len(sys.argv) > 5 else "cut"
t0 = time.time()
C = Z.make_chain(mode, u, k + 2, eps1)
ev = Q2.Ev(u, both=True)
cu = ev.cu
ld = math.log(0.05)
st = Q2.Stat()
calX = Z.X0(u, N) + 1.0
print("# cube u = %g: h = %.6f, a = %.6f; %s; horizon N = %d, k = %d levels; curves with values in [0, 1]: %s"
      % (u, C.h, C.a, ("cut orbit curves, s_t = L + 0.05, b_0 = h + %g" % eps1) if mode == "cut" else "envelope sequence from b_0 = a", N, k, C.range_ok))
print("# (b_j - h)/h, j = 0..%d: %s;   X = X_0(N) + 1 = %.2f" % (k, " ".join("%.4f" % ((b - C.h) / C.h) for b in C.b[:k + 1]), calX))

# the blocks of the chains, top-down, with the entry values of Lambda (section 6)
Lam = -ld + N * LN2
blocks = {}
for j in range(k, 0, -1):
    m = Q2.Chain.design_m(cu, N, C.b[j], calX, 1.0, Lam)
    ch = Q2.Chain(cu, N, C.b[j], calX, 1.0, m)
    blocks[j] = (m, Lam)
    Lam = ch.Lam_sharp(N, Lam)
    Lam += Q2.qSb(cu, N, Lam)
print("# blocks of the chains (top first): %s;  levels of a chain started at N: %s"
      % ([blocks[j][0] for j in range(k, 0, -1)], [Q2.Chain(cu, N, C.b[j], calX, 1.0, blocks[j][0]).j(N) for j in range(k, 0, -1)]))

fam = Z.SatFlat(C.b[0])
zs, chs = [], []
for j in range(k):
    z = Z.ZLevelFam(ev, fam, C.grid(j, N), C.grid(j + 1, N), C.b[j + 1], N, st)
    chf = Q2.ChainFam(ev, z, 1.0, N, st, blocks[j + 1][1], m=blocks[j + 1][0])
    fam = Z.ZHatFam(z, chf, st)
    zs.append(z)
    chs.append(chf)

rows = []
for (d, x) in ((N, 1.0), (N, calX), (N, calX + 0.02 * N), (N // 2, 1.0)):
    c = float(fam.costs(d, np.array([x]), ld)[0])
    Lam0 = -ld + d * LN2
    typ = zs[-1].type_major(d, x)
    Eb = fam.Ebound(d, x, Lam0)
    rows.append((d, x, c, typ, c - typ, Eb, c - d * C.h, d * (C.a - C.h)))
print("#      d      x     ln cost     type(W_k)   cost - type   error bound E_k   cost - d h    d (a - h)")
for r in rows:
    print("  %6d  %6.1f  %10.2f  %10.2f   %9.2f      %9.2f     %9.2f   %9.2f" % r)
print("# levels of section 4 evaluated: %s (per family, base first);  chain levels: %s;  checks: %d;  evaluators differ by at most %.1e"
      % ([z.nlev for z in zs], [c.nlev for c in chs], st.total(), ev.maxdiff))
for z, name in zip(zs, range(1, k + 1)):
    if z.loss:
        ls = [l for (_, _, l) in z.loss]
        print("#   level family %d: measured loss (ln C_max - type of W_%d) between %.1f and %.1f nats over %d evaluations" % (name, name, min(ls), max(ls), len(ls)))
print("least slack per inequality:")
for name in sorted(st.minslack):
    print("   %-45s %10.3f   (%d checks)" % (name, st.minslack[name][0], st.n[name]))
ok = (len(st.viol) == 0) and all(r[4] <= r[5] + 1e-9 for r in rows) and C.range_ok
print("violations: %d   [must be 0]" % len(st.viol))
for v in st.viol[:5]:
    print("   VIOLATION", v)
print("time %.0f s" % (time.time() - t0))
print("ALL CHECKS PASS" if ok else "A CHECK FAILED")
