#!/usr/bin/env python3
"""ER2: why the triangle with one violated bond satisfies the thermal union bound.
mu*_a for pi ~ exp(x1x2 + x2x3 - x1x3/2), a = (+,+,+), b = 1, in the disagreement variables e:
  * not log-supermodular (lattice condition fails);
  * positively associated: Cov(1_U, 1_W) >= 0 for all pairs of up-sets U, W of {0,1}^3 (20 up-sets);
  * conditionally increasing in sequence for the ordering (1, 3, 2), not for (1, 2, 3).
Positive association is all the coupling proof needs: every member mu = r mu* (r increasing) then dominates
mu* stochastically, a monotone coupling exists (Strassen), and TV <= P(X != Y) <= sum_i [mu(e_i=1) - mu*(e_i=1)]."""
import itertools
import numpy as np

E = np.array(list(itertools.product((0, 1), repeat=3)))
X = 1 - 2 * E                                           # a = (+,+,+)


def mustar(J12, J23, J13, b):
    lp = J12 * X[:, 0] * X[:, 1] + J23 * X[:, 1] * X[:, 2] + J13 * X[:, 0] * X[:, 2] - b * E.sum(axis=1)
    p = np.exp(lp); return p / p.sum()


def lsm(p):
    idx = {tuple(e): k for k, e in enumerate(E)}
    return all(p[idx[tuple(np.maximum(x, y))]] * p[idx[tuple(np.minimum(x, y))]] >= p[idx[tuple(x)]] * p[idx[tuple(y)]] * (1 - 1e-12)
               for x in E for y in E)


def upsets():
    out = []
    for mask in range(1 << 8):
        ind = np.array([(mask >> k) & 1 for k in range(8)], dtype=bool)
        if all((not ind[i]) or ind[j] for i in range(8) for j in range(8) if np.all(E[i] <= E[j])):
            out.append(ind)
    return out


def cis(p, order):
    """q_i(e_<i) = P(e_i = 1 | predecessors) non-decreasing in the predecessors, for every i."""
    for pos, i in enumerate(order):
        prev = list(order[:pos])
        q = {}
        for e in itertools.product((0, 1), repeat=len(prev)):
            same = np.all(E[:, prev] == np.array(e), axis=1) if prev else np.ones(8, dtype=bool)
            q[e] = p[same & (E[:, i] == 1)].sum() / p[same].sum()
        for e in q:
            for f in q:
                if all(a <= b for a, b in zip(e, f)) and q[e] > q[f] + 1e-13:
                    return False
    return True


U = upsets(); print(f"up-sets of the 3-cube: {len(U)}")
for J in ((1, 1, -0.5), (1, 1, -0.05), (0, 0, -0.5), (1, -0.5, 0)):
    p = mustar(*J, 1.0)
    mincov = min(p[u & w].sum() - p[u].sum() * p[w].sum() for u in U for w in U)
    print(f"J = {J}, b = 1: log-supermodular {lsm(p)}; smallest Cov(1_U, 1_W) over up-sets {mincov:+.4f} (positively associated: {mincov > -1e-13}); "
          f"CIS for the orderings (1,2,3), (1,3,2), (2,1,3): {cis(p, (0, 1, 2))}, {cis(p, (0, 2, 1))}, {cis(p, (1, 0, 2))}")
