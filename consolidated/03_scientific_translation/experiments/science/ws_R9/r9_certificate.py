#!/usr/bin/env python3
"""R9, item 4: a human-checkable certificate that the semigroup of clean bridges generates the full lattice.
Five clean bridges (coordinates below) whose vectors (h3,h8,h11,g; N+3) have determinant +-1, and four whose projections
(h3,h8,h11; N+3) have determinant +-1 (found among all clean bridges with at most 12 beads).
Each walk is checked from coordinates: lattice sites, bonds, self-avoidance, bridge, the O(n^2) definition of (h,g), and
cleanliness by the definition (three linker sites above and below, pairs at chain separation >= 3)."""
import sys
sys.dont_write_bytecode = True
import r9_lat as L
from sympy import Matrix

walks = {
 (0, 2, 6, 5, 12): [(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 3, 1), (-2, 2, 0), (-3, 3, -1), (-4, 4, 0), (-3, 5, 1), (-2, 6, 0)],
 (0, 0, 1, 1, 7): [(0, 0, 0), (1, 1, 1), (0, 2, 2), (-1, 3, 1)],
 (1, 6, 11, 7, 14): [(0, 0, 0), (1, 1, 1), (0, 2, 2), (1, 3, 3), (2, 2, 4), (3, 1, 3), (4, 2, 2), (3, 3, 1), (2, 4, 2), (3, 5, 3), (4, 6, 2)],
 (0, 0, 1, 1, 8): [(0, 0, 0), (1, 1, 1), (0, 2, 2), (1, 3, 3), (2, 4, 2)],
 (0, 3, 6, 4, 12): [(0, 0, 0), (1, 1, 1), (0, 2, 2), (1, 3, 3), (0, 4, 4), (-1, 3, 5), (-2, 2, 4), (-3, 3, 3), (-2, 4, 2)],
}
ok = True
for v, w in walks.items():
    good = (L.check_walk(w) is None and L.is_bridge(w) and L.profile_brute(w) == v[:4] and L.profile(w) == v[:4]
            and len(w) + 3 == v[4] and L.is_clean(w))
    ok &= good
    print(v, "N =", len(w), "walk, bridge, (h,g), clean:", good, " A =", L.A_part(w, L.admissible_c1(w)[0]), " B =", L.B_part(w))
M = Matrix([list(v) for v in walks])
print("determinant of the five vectors (h3,h8,h11,g; N+3):", M.det())
# the projection: search four clean bridges with at most 12 beads
vec = {}
for n in range(3, 13):
    for x in L.enum_bridges(n):
        if L.is_clean(x):
            h = L.profile(x)
            vec.setdefault((h[0], h[1], h[2], n + 3), x)
import itertools
keys = sorted(vec, key=lambda v: v[3])
found = None
for comb in itertools.combinations(keys[:60], 4):
    if abs(Matrix([list(c) for c in comb]).det()) == 1:
        found = comb; break
print("four clean bridges whose (h3,h8,h11; N+3) have determinant +-1:")
for c in found:
    w = vec[c]
    assert L.check_walk(w) is None and L.is_bridge(w) and L.is_clean(w) and L.profile_brute(w)[:3] == c[:3]
    print("  ", c, w)
print("determinant:", Matrix([list(c) for c in found]).det())
# an exact point of K^br off the hyperplane g = 9 p3 - 3 p8 + p11 (so K^br has interior in R^4, without any error term)
v = (0, 2, 6, 5, 12)
print("clean 9-bead bridge (0,2,6,5): g - 9h3 + 3h8 - h11 =", v[3] - 9 * v[0] + 3 * v[1] - v[2], "!= 0; the point (h,g)/(N+3) =", tuple(c / 12 for c in v[:4]), "is in K^br exactly")
print("all checks passed:", ok)
