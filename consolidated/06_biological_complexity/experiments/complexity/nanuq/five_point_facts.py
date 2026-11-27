"""The 5-point facts used in the local criterion, checked on EVERY tree-generated circular split system on
5 points (there are 16) in every dihedral placement:

   (F5a)  Phi5(u1; z; up; v1, vq) >= 0
   (F5b)  Phi5 = 0 whenever the quartet u1 up | v1 vq is not displayed
   (F5c)  Psi(a; u; b; z, w)  >= 0
   (F4)   every 4-point tree-generated system: Phi4 = 2 w(u1 up | v1 vq) in {0,1,2}, > 0 iff displayed (definition)
"""
from itertools import combinations
from splitsys import *
from localcrit import tree_generated
from local_terms import phi5, displayed
from localcrit import psi2

n = 5
allsp = all_circular_splits(n)
triv = [m for m in allsp if is_trivial(n, m)]
nontriv = [m for m in allsp if not is_trivial(n, m)]
systems = []
for r in range(n - 3, len(nontriv) + 1):
    for sub in combinations(nontriv, r):
        if tree_generated(n, sub):
            systems.append(set(triv) | set(sub))
print("tree-generated systems on 5 points:", len(systems))
ok = True
vals5, valsP = set(), set()
for s in systems:
    for r in range(5):
        for sgn in (1, -1):
            pts = [(r + sgn * t) % 5 for t in range(5)]
            u1, z, up, v1, vq = pts
            v = phi5(s, n, u1, z, up, v1, vq)
            vals5.add(v)
            if v < 0 or (not displayed(s, u1, up, v1, vq) and v != 0):
                ok = False
            a, u, b, zz, w = pts
            p = psi2(s, n, a, u, b, zz, w)
            valsP.add(p)
            if p < 0:
                ok = False
print("values of 2*Phi5:", sorted(vals5), " values of 2*Psi:", sorted(valsP), " all 5-point facts hold:", ok)
