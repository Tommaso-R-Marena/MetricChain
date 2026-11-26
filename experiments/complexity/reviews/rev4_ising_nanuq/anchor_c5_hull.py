"""Independent of the LP code: faces of CUT_5 from its facets (known: 40 triangle inequalities and 16
pentagonal/equicut inequalities), as intersections of facet vertex sets; dimension by exact rank."""
import itertools, numpy as np, sympy
from collections import Counter
from scipy.spatial import ConvexHull
from ising_core import all_states, Pmat

S = all_states(5)
P = Pmat(S).astype(float)
hull = ConvexHull(P, qhull_options="QJ")       # joggle not needed? use exact check below instead
# exact facets: derive candidate facet normals from hull equations, rounded to integers, then verify
facets = set()
for eq in hull.equations:
    a, b = eq[:-1], eq[-1]
    a = a / np.abs(a).max()
    # scale to small integers
    for s in range(1, 7):
        ai = np.rint(a * s)
        if np.abs(ai - a * s).max() < 1e-6:
            break
    vals = P @ ai
    mx = vals.max()
    roots = frozenset(np.nonzero(np.abs(vals - mx) < 1e-9)[0].tolist())
    # verify it is a facet: valid (by construction max) and roots affinely span dimension 9
    R = Pmat(S[sorted(roots)])
    if sympy.Matrix((R[1:] - R[0:1]).tolist()).rank() == 9:
        facets.add(roots)
print("facets:", len(facets), Counter(len(f) for f in facets))
faces = set(facets)
frontier = set(facets)
while frontier:
    new = set()
    for f in frontier:
        for g in facets:
            h = f & g
            if h and h not in faces:
                faces.add(h)
                new.add(h)
    frontier = new
fv = Counter()
for f in faces:
    R = Pmat(S[sorted(f)])
    d = sympy.Matrix((R[1:] - R[0:1]).tolist()).rank() if len(f) > 1 else 0
    fv[d] += 1
print("f-vector from facet intersections:", [fv[d] for d in range(10)])
