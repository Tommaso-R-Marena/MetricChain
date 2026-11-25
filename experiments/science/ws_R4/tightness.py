#!/usr/bin/env python3
"""R4 -- is the bound of Lemma 11.85 attained on the twins by an actual two-round algorithm?

Algorithm (knows the two blocks): batch 1 = M uniform points, each with its n neighbours.  A sampled
point of type (d1,d2), 1 <= d2 <= n2-1, whose block-2 neighbours take two different values
F(d1,d2-1) != F(d1,d2+1) reveals s^2 up to the antipode (as in Theorem 11.51); batch 2 = the two
points (x^1, c), (x^1, c-bar): there d2 in {0, n2}, outside W2, where F_D and F_S differ.
So one star detects with probability P(R), R = {(d1,d2): F(d1,d2-1) != F(d1,d2+1)}, and the twins are
told apart with about (n+1)/P(R) evaluations.  Lemma 11.85: no two-round algorithm does it with fewer
than about 1/(p1+p2).  The ratio P(R)/p1 measures how tight the lemma is on this pair.
"""
import sys
import numpy as np
from scipy.special import logsumexp
from twins_exact import Twins

for (u, n, n1, Tn) in [(1.0, 800, 360, 0.04216), (1.0, 1600, 800, 0.03987), (1.0, 3200, 1760, 0.03928),
                       (2.0, 1600, 880, 0.12555)]:
    n2 = n - n1
    t = Twins(n1, n2, u, Tn * n)
    out = []
    for name, F in (("D", t.FD), ("S", t.FS)):
        R = np.zeros_like(t.W1)
        R[:, 1:-1] = np.abs(F[:, 2:] - F[:, :-2]) > 1e-9
        lnPR = float(logsumexp(t.lp[R]))
        # the two probe points have d2 in {0, n2}: do the twins differ there for every d1 ?
        differ_at_centre = bool(np.all(np.abs(t.FD[:, 0] - t.FS[:, 0]) > 1e-9))
        out.append((name, lnPR, differ_at_centre))
    print(f"u={u} n={n} n1={n1} T/n={Tn}: gap={t.gap:.3f}  ln p1={t.lnp1:.3f}  ln p2={t.lnp2:.3f}  "
          + "  ".join(f"ln P(R_{nm})={v:.3f} (P(R)/p1={np.exp(v - t.lnp1):.3f}; twins differ at d2=0: {dc})"
                      for nm, v, dc in out)
          + f"   lower bound exponent {t.E():.5f}, star algorithm exponent <= {(-out[0][1] + np.log(n + 1)) / n:.5f}")
