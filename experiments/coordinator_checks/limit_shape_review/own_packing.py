#!/usr/bin/env python3
"""Assistant B — an OWN greedy packing in the hull of the 14 proved points (4 exact + 10 verified bridges), to see
what an independent search gives next to the reviewer's 116 / 451 / 8 / 19.  Same principle (Theorem 11.71(b) with the
uncertainty margin), own candidate generation (a grid in u-coordinates with an LP for the least credit, a triangular
grid in T0, the vertices), own greedy orders; the result is verified pairwise in exact rational arithmetic.
usage: own_packing.py L eps1 step G0      (L, eps1 as fractions, e.g. 1 1/2 0.125 96)"""
import sys, itertools, time
from fractions import Fraction as Fr
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import linprog
from scipy.spatial import Delaunay
from verify_packing import my_points, cnorm

L = Fr(sys.argv[1]); e1 = Fr(sys.argv[2]); step = float(sys.argv[3]); G0 = int(sys.argv[4])
t0 = time.time()
V = my_points()                       # (p3, p8, p11, g, delta) as Fractions
k = len(V)
P = np.array([[float(c) for c in v[:3]] for v in V]); G = np.array([float(v[3]) for v in V]); D = np.array([float(v[4]) for v in V])
mx = max(L, Fr(1))
U = np.array([[5, 0, 0], [3, 3, 0], [1, 1, 1]], float)
Pu = P @ U.T
hull = Delaunay(P)
cost = G + float(mx) * D
cands = []                            # (exact (p, g, d), weights)
def add(lam):
    s = sum(lam)
    if s == 0:
        return
    lam = [x / s for x in lam]
    q = tuple(sum(lam[i] * V[i][j] for i in range(k)) for j in range(5))
    cands.append(q)
lo = Pu.min(0); hi = Pu.max(0)
off = 0.37 * step
for a in np.arange(lo[0] + off, hi[0], step):
    for b in np.arange(lo[1] + off, hi[1], step):
        for c in np.arange(lo[2] + off, hi[2], step):
            p = np.linalg.solve(U, np.array([a, b, c]))
            if hull.find_simplex(p) < 0:
                continue
            r = linprog(cost, A_eq=np.vstack([P.T, np.ones(k)]), b_eq=np.append(p, 1.0), bounds=(0, None), method="highs")
            if r.status != 0:
                continue
            add([Fr(float(x)).limit_denominator(10 ** 5) if x > 1e-9 else Fr(0) for x in r.x])
ngrid = len(cands)
for i in range(k):
    add([Fr(1) if j == i else Fr(0) for j in range(k)])
for a in range(G0 + 1):               # triangle T0 = conv(V[0], V[1], V[2]), exact, g = 0, d = 0
    for b in range(G0 + 1 - a):
        add([Fr(G0 - a - b), Fr(a), Fr(b)] + [Fr(0)] * (k - 3))
n = len(cands)
Cu = np.array([[float(c) for c in q[:3]] for q in cands]) @ U.T
rad = np.array([float(q[3] + e1 + mx * q[4]) for q in cands])
Lf = float(L)
rng = np.random.default_rng(1)
orders = [np.argsort(rad, kind="stable"), np.argsort(rad + 0.05 * Cu.sum(1)), np.argsort(rad - 0.05 * Cu.sum(1)),
          np.argsort(rad + 0.03 * Cu[:, 0]), np.argsort(rad + 0.03 * Cu[:, 2])]
for _ in range(10):
    orders.append(np.argsort(rad + 0.2 * rng.random(n)))
best = []
for o in orders:
    ch = []; C = np.empty((0, 3)); R = np.empty(0)
    for i in o:
        if len(ch) == 0 or np.all(Lf * np.abs(C - Cu[i]).sum(1) > (R + rad[i]) + 1e-7):
            ch.append(i); C = np.vstack([C, Cu[i]]); R = np.append(R, rad[i])
    if len(ch) > len(best):
        best = ch
ok = True; worst = None
for i, j in itertools.combinations(best, 2):
    a, b = cands[i], cands[j]
    m = L * cnorm([a[t] - b[t] for t in range(3)]) - ((a[3] + b[3]) + 2 * e1 + mx * (a[4] + b[4]))
    ok &= (m > 0)
    worst = m if worst is None or m < worst else worst
nT0 = sum(1 for i in best if cands[i][3] == 0 and cands[i][4] == 0)
print(f"(L, eps1) = ({L}, {e1}): step {step}, T0 grid {G0}: {n} candidates ({ngrid} from the 3-d grid); own greedy packing: {len(best)} points "
      f"({nT0} in T0); exact pairwise verification: {ok}; smallest margin {float(worst):.2e}; {time.time()-t0:.0f} s", flush=True)
