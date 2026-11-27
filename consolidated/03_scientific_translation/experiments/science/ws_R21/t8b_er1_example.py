"""T8b - the explicit pair of Counterexample 2 of THEIR internal review (ER1, F2; coordinates as printed there,
four decimals), checked with my own tools: realisable colourings by the EXACT method, and the largest mass
that a non-negative table with the right marginals can put on chimeras (LP), for three weightings.
Edge order of my K4+deg2: (0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(0,4),(1,4); colouring digit 0 = first conformer."""
import numpy as np
from scipy.optimize import linprog
from r21_common import *
name = "K4+deg2"
N, E = graph_table()[name]
m = len(E)
X = np.array([[(0, 0), (2, 0), (0.6, 1.1), (1.6, -0.9), (1, 1.1180)],
              [(0, 0), (5, 0), (1.5, 1.1), (4, -0.9), (2.775, 1.1399)]], dtype=float)
Tc = sqlen(X, E)
print("T8b start", now())
print("pendant lengths (4-0, 4-1): conformer 1 %.4f %.4f ; conformer 2 %.4f %.4f ; base |x0 x1|: %.1f, %.1f"
      % (np.sqrt(Tc[0, 6]), np.sqrt(Tc[0, 7]), np.sqrt(Tc[1, 6]), np.sqrt(Tc[1, 7]), np.sqrt(Tc[0, 0]), np.sqrt(Tc[1, 0])))
col = all_colourings(2, m)
T = splice_targets(Tc, col)
ex, _ = Constructor(name, N, E).defect(T)
real = ex < 1e-9
R = col[real]
nonconst = ~np.all(R == R[:, :1], axis=1)
print("realisable colourings:", [''.join(map(str, r)) for r in R], "; chimeras:", int(nonconst.sum()),
      "; smallest exact defect among the non-realisable:", "%.3e" % ex[~real].min())
best, _, _ = Realiser(N, E).multistart(T[real], 30, np.random.default_rng(0))
print("LM residuals of the realisable colourings (30 starts):", np.array2string(best, precision=2))
for w0 in (0.5, 0.3, 0.8):
    A = np.vstack([(R == 0).T.astype(float), np.ones(len(R))])
    b = np.concatenate([np.full(m, w0), [1.0]])
    lp = linprog(-nonconst.astype(float), A_eq=A, b_eq=b, bounds=(0, None), method='highs')
    print("weights (%.1f, %.1f): largest mass on chimeras compatible with the eight laws = %.2e (LP status %d)" % (w0, 1 - w0, -lp.fun, lp.status))
print("DONE t8b_er1_example", now())
