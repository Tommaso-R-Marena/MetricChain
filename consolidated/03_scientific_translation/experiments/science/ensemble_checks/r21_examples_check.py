#!/usr/bin/env python3
"""Coordinator's own check of two examples of workstream R21 (review of the Ensemble division's Theorem E7), written without
R21's code.
D1 (exact rational arithmetic): on K4 in the plane, two conformers with no edge length in common whose equal-weight ensemble
    has the same law on every edge as a second, non-congruent two-conformer ensemble.
D2 (random instances): on K5 minus the edge 34 (generically globally rigid in the plane), two conformers that share the
    triangle 012; exchanging the positions of vertex 4 gives a second ensemble with the same law on every measured edge.
Controls that must fail: D1 with one coordinate of x2 changed (the laws must then differ); D2 with the edge 34 measured
(the laws must then differ).  Also checked for D2: the rank of the rigidity matrix (7 = 2N - 3) and of a stress matrix
(N - 3 = 2, the Connelly / Gortler-Healy-Thurston criterion of generic global rigidity) at a random framework.
Run: python3 -B r21_examples_check.py > r21_examples_check.log
"""
import itertools
from fractions import Fraction as F
import numpy as np


def sq(p, e): return sum((a - b) ** 2 for a, b in zip(p[e[0]], p[e[1]]))


def laws(ens, edges): return [sorted(sq(p, e) for p in ens) for e in edges]


def congruent(p, q, tol=0):
    """labelled frameworks are congruent iff all pair distances agree"""
    return all(abs(sq(p, e) - sq(q, e)) <= tol for e in itertools.combinations(range(len(p)), 2))


K4 = list(itertools.combinations(range(4), 2))
x1 = ((F(1, 2), F(2)), (F(3), F(3)), (F(-1), F(0)), (F(1), F(0))); x2 = ((F(1, 2), F(3, 2)), (F(3, 2), F(-4)), (F(-2), F(0)), (F(2), F(0)))
y = ((F(1, 2), F(2)), (F(3), F(-3)), (F(-1), F(0)), (F(1), F(0))); yp = ((F(1, 2), F(3, 2)), (F(3, 2), F(4)), (F(-2), F(0)), (F(2), F(0)))
print("D1  squared lengths on", K4)
for nm, p in (("x1", x1), ("x2", x2), ("y", y), ("y'", yp)): print(f"    {nm}: {[str(sq(p, e)) for e in K4]}")
same = laws([x1, x2], K4) == laws([y, yp], K4); common = set(sq(x1, e) for e in K4) & set(sq(x2, e) for e in K4)
noncong = not any(congruent(a, b) for a in (y, yp) for b in (x1, x2))
print(f"D1  every edge has the same two-point law under (x1, x2) and (y, y'): {same} (must be True); edge lengths common to x1 and x2: {len(common)} (must be 0); "
      f"y, y' congruent to x1 or x2: {not noncong} (must be False)")
x2c = (x2[0], (F(3, 2), F(-4) + F(1, 100)), x2[2], x2[3]); ypc = (yp[0], (F(3, 2), F(4) - F(1, 100)), yp[2], yp[3])
ctrl = laws([x1, x2c], K4) == laws([y, ypc], K4)
print(f"D1  control, vertex 1 of the second kite moved by 1/100 (and its mirror image likewise): the laws agree: {ctrl} (must be False)")
assert same and not common and noncong and not ctrl
# ---- D2
rng = np.random.default_rng(20261126); E = [e for e in itertools.combinations(range(5), 2) if e != (3, 4)]; bad = 0; ctrl_bad = 0; nonc = 0
for rep in range(200):
    T = rng.normal(size=(3, 2)); P3, P4, P3p, P4p = (rng.normal(size=2) for _ in range(4))
    a, b = np.vstack([T, P3, P4]), np.vstack([T, P3p, P4p]); c, d = np.vstack([T, P3, P4p]), np.vstack([T, P3p, P4])
    L1 = np.array(laws([a, b], E)); L2 = np.array(laws([c, d], E)); bad += int(np.abs(L1 - L2).max() > 1e-12)
    L1f = np.array(laws([a, b], E + [(3, 4)])); L2f = np.array(laws([c, d], E + [(3, 4)])); ctrl_bad += int(np.abs(L1f - L2f).max() > 1e-6)
    nonc += int(not any(congruent(u, v, 1e-9) for u in (c, d) for v in (a, b)))
print(f"D2  200 random pairs of conformers sharing the triangle 012 on K5 - 34: instances in which some measured edge has different laws under (x1, x2) and (y, y'): {bad} (must be 0); "
      f"instances in which y, y' are congruent to neither conformer: {nonc} (must be 200); control, the edge 34 measured: the laws differ in {ctrl_bad} of 200 (must be 200)")
assert bad == 0 and nonc == 200 and ctrl_bad == 200
# generic global rigidity of K5 - 34 in the plane: rigidity matrix rank 2N - 3 and a stress matrix of rank N - 3
p = rng.normal(size=(5, 2)); Rm = np.zeros((len(E), 10))
for r, (u, v) in enumerate(E): Rm[r, 2 * u:2 * u + 2] = p[u] - p[v]; Rm[r, 2 * v:2 * v + 2] = p[v] - p[u]
rank = np.linalg.matrix_rank(Rm); _, s, Vt = np.linalg.svd(Rm.T); null = Vt[rank:]            # stresses: left kernel of the rigidity matrix
best = 0
for trial in range(20):
    w = null.T @ rng.normal(size=len(null)); Om = np.zeros((5, 5))
    for r, (u, v) in enumerate(E): Om[u, v] -= w[r]; Om[v, u] -= w[r]; Om[u, u] += w[r]; Om[v, v] += w[r]
    best = max(best, np.linalg.matrix_rank(Om, tol=1e-9))
print(f"D2  K5 - 34 at a random framework: rank of the rigidity matrix {rank} (2N - 3 = 7), dimension of the stress space {len(null)}, largest rank of a stress matrix {best} (N - 3 = 2: generically globally rigid)")
assert rank == 7 and best == 2
print("ALL DONE")
