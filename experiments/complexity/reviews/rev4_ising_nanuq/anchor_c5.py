"""External anchor for the referee's exposedness code: the face lattice of the cut polytope on 5 nodes.
Published (A. Deza, M. Deza, 'The combinatorial structure of small cut and metric polytopes', LIENS-95-1,
Section 3): f(c_5) = (16, 120, 560, 1780, ..., 3080, 640, 56); facets in 2 orbits, ridges in 3 orbits
(240, 240, 160), 7-faces in 7 orbits (120, 960, 480, 240, 160, 160, 960), 6-faces 10 orbits, 5-faces 11,
4-faces 8 orbits.  Here: every subset of the 16 states on 5 sites, by orbit representative, decided by LP."""
import itertools, numpy as np, sympy
from collections import Counter, defaultdict
from ising_core import *
from k5_table import orbit_data, types, NT

gorder, best = orbit_data()
reps, counts = np.unique(best[1:], return_counts=True)
fvec = Counter()
orbs = defaultdict(list)
nonfaces_by_size = Counter()
for r, c in zip(reps, counts):
    V = [types[i] for i in range(NT) if int(r) >> i & 1]      # states on 5 sites
    res = decide(V)
    K = len(V)
    if res.exposed:
        PV = Pmat(np.array(V))
        dim = sympy.Matrix((PV[1:] - PV[0:1]).tolist()).rank() if K > 1 else 0
        fvec[dim] += int(c)
        orbs[dim].append((int(c), K))
    else:
        nonfaces_by_size[K] += int(c)
print("faces of CUT_5 by dimension:", [fvec[d] for d in range(0, 11)])
for d in sorted(orbs):
    print("  dim %d: %d orbits, (orbit size, #vertices): %s" % (d, len(orbs[d]), sorted(orbs[d])))
print("non-faces by number of vertices:", dict(sorted(nonfaces_by_size.items())))
