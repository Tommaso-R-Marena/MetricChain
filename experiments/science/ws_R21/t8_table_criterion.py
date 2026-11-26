"""T8 — the exact tuple-wise criterion (own code): a two-conformer ensemble with weights (w, 1-w) is determined
by its edge-length laws iff the non-negative table on the REALISABLE colourings with the prescribed marginals is
unique.  Written after the coordinator's note of 18:11Z relayed a finding of the Ensemble division's internal
review (an open set of pairs on K4 + vertex of degree two with three realisable chimeras and an identified
ensemble); this script is a replication of that finding with my own tools, not a finding of mine.

For random pairs on K4 + degree-2 vertex (matroid not connected) and, for comparison, on the wheel W5 and K5-e
(connected): the realisable colourings (EXACT method), the number of chimeras, and the largest mass that a table
with the right marginals can put on chimeras (linear programme; 0 <=> determined at the level of length vectors).
usage: python3 -B t8_table_criterion.py [n_pairs]
"""
import sys
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from r21_common import *

n_pairs = int(sys.argv[1]) if len(sys.argv) > 1 else 400
rng = np.random.default_rng(2108)
print("T8 table criterion  start", now(), " pairs per graph:", n_pairs)
w = np.array([0.4, 0.6])
for name in ("K4+deg2", "W5", "K5-e"):
    N, E = graph_table()[name]
    m = len(E)
    C = Constructor(name, N, E)
    col_all = all_colourings(2, m)
    is_const = ~nonconstant(col_all)
    stat = Counter()
    ex_examples = {}
    for trial in range(n_pairs):
        X = rng.standard_normal((2, N, 2))
        Tc = sqlen(X, E)
        T = splice_targets(Tc, col_all)
        ex, _ = C.defect(T)
        real = ex < 1e-9
        assert real[is_const].all()                       # control: the conformers are realisable
        R = col_all[real]
        nchim = int(real.sum()) - 2
        # table: nu >= 0 on R, for every edge e: sum_{a in R, a(e) = 0} nu(a) = w[0]; total mass 1
        A = np.vstack([(R == 0).T.astype(float), np.ones(len(R))])
        b = np.concatenate([np.full(m, w[0]), [1.0]])
        cobj = -(~np.all(R == R[:, :1], axis=1)).astype(float)
        lp = linprog(cobj, A_eq=A, b_eq=b, bounds=(0, None), method='highs')
        off = -lp.fun if lp.status == 0 else np.nan
        ident = off < 1e-9
        stat[(nchim, bool(ident))] += 1
        if (nchim, bool(ident)) not in ex_examples:
            ex_examples[(nchim, bool(ident))] = (sorted(''.join(map(str, r)) for r in R if len(set(r)) > 1), off)
    print(f"{name} (edges {E}): {n_pairs} random pairs, weights {w}")
    for key in sorted(stat):
        exm, off = ex_examples[key]
        print(f"    realisable chimeras: {key[0]:2d}; determined: {str(key[1]):5s}; pairs: {stat[key]:4d}; example of the chimera colourings "
              f"{exm if len(exm) <= 6 else exm[:6] + ['...']} (largest mass on chimeras {off:.3f})")
    tot_ident_with_chim = sum(v for (k, i), v in stat.items() if k > 0 and i)
    tot_chim = sum(v for (k, i), v in stat.items() if k > 0)
    print(f"    pairs with at least one chimera: {tot_chim}; of these determined all the same: {tot_ident_with_chim}; not determined: {tot_chim - tot_ident_with_chim}")
print("DONE t8_table_criterion", now())
