#!/usr/bin/env python3
"""Pairs between two parallel all-trans rods (direction (0,1,1)) per period, for all rod-lattice offsets.

Rod (m,q) = rod (0,0) + m(2,2,0) + q(2,0,2).  For every offset (m,q) with |m|,|q| <= 6: the number of pairs at squared
distance 3, 8, 11 between ONE period of rod (0,0) (the sites t = 0, 1) and the whole rod (m,q).
Result used in Proposition 4.3: only the eight offsets +-(1,0), +-(0,1) [type 1], +-(1,-1) [type 2], +-(1,1) [type 3]
interact, with (1,4,3), (0,2,4), (0,0,2) pairs per period.  Also the pairs inside one rod beyond chain separation 2.
"""
from lat import *
import lamella as lam

def pairs(m, q, T=40):
    c = {3: 0, 8: 0, 11: 0}
    other = [lam.site(m, q, t) for t in range(-T, T)]
    for t0 in (0, 1):
        p = lam.site(0, 0, t0)
        for o in other:
            s = d2(p, o)
            if s in c: c[s] += 1
    return (c[3], c[8], c[11])

res = {}
for m in range(-6, 7):
    for q in range(-6, 7):
        if (m, q) == (0, 0): continue
        r = pairs(m, q)
        if r != (0, 0, 0): res[(m, q)] = r
print("interacting offsets (m,q): pairs per period at squared distances (3, 8, 11) [each pair counted once per period of rod (0,0)]")
for k in sorted(res): print("  ", k, res[k])
# minimal squared distance between rod (0,0) and far rods
far = min(d2(lam.site(0, 0, t0), lam.site(m, q, t)) for m in range(-6, 7) for q in range(-6, 7) if (m, q) not in res and (m, q) != (0, 0)
          for t0 in (0, 1) for t in range(-40, 40))
print("smallest squared distance to a non-interacting rod with |m|,|q| <= 6:", far)
# inside a rod: squared distances between t and t+k
print("inside a rod: squared distance between positions t and t+k, k = 1..6:", [d2(lam.site(0, 0, 0), lam.site(0, 0, k)) for k in range(1, 7)])
