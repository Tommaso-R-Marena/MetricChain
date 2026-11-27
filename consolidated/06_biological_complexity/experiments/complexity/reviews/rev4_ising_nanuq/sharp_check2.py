"""Incidental check of material that appeared in the working tree DURING the review (Corollary 5', Theorem 10'
of the NANUQ note, uncommitted): not part of the brief; own code only."""
import itertools
from fractions import Fraction
from sharp_check import *

trees = circular_trees(X)
cur = {frozenset(t) for t in trees}
frontier = set(cur)
while frontier:
    new = set()
    for s in frontier:
        for t in trees:
            u = s | t
            if u not in cur:
                cur.add(u); new.add(u)
    frontier = new
systems = list(cur)
NT = nontrivial_circular_splits(X)
three = [sp for sp in NT if min(len(a) for a in sp) == 3]
two = [sp for sp in NT if min(len(a) for a in sp) == 2]
mism = 0
nneg_free = 0
bad17 = []
for S in systems:
    Q = quartets_from_splits(S, X)
    anyneg = False
    for r in range(6):
        for refl in (1, -1):
            y = [X[(r + refl * k) % 6] for k in range(6)]
            u1, z, w, up, v1, vq = y
            phi = wq(Q, z, w, v1, vq) + wq(Q, z, w, u1, up) - wq(Q, z, w, vq, up) - wq(Q, z, w, u1, v1)
            zw = frozenset([frozenset([z, w]), FULL - {z, w}])
            pred = all(t in S for t in three) and zw not in S
            if (phi < 0) != pred:
                mism += 1
            anyneg |= phi < 0
    nneg_free += not anyneg
    if anyneg:
        bad17.append(S)
print("Corollary 5' (Phi6 < 0 iff three 3-splits present and the 2-split {z,w} absent): mismatches over 150 x 12:", mism)
print("six-point systems with Phi6 >= 0 in all labellings:", nneg_free, "; excluded:", len(bad17))

# Theorem 10'(c): alpha_S/2 = Phi4 + m (Phi5(z)+Phi5(w)) - m^2/2 for caterpillar blow-ups of z and w
def cat_blowup(S, order, z, w, m):
    groups = {x: [(x, 0)] for x in order}
    groups[z] = [(z, i) for i in range(m)]
    groups[w] = [(w, i) for i in range(m)]
    new_order = [g for x in order for g in groups[x]]
    full = frozenset(new_order)
    out = set()
    for sp in S:
        a, b = tuple(sp)
        A = frozenset(g for x in a for g in groups[x])
        out.add(frozenset([A, full - A]))
    for g in new_order:
        out.add(frozenset([frozenset([g]), full - {g}]))
    for x in (z, w):
        for i in range(2, m):
            A = frozenset(groups[x][:i])
            out.add(frozenset([A, full - A]))
    return out, new_order, groups

bad = 0
tot = 0
least = []
for S in bad17:
    Q = quartets_from_splits(S, X)
    done = False
    for r in range(6):
        for refl in (1, -1):
            y = [X[(r + refl * k) % 6] for k in range(6)]
            u1, z, w, up, v1, vq = y
            zw = frozenset([frozenset([z, w]), FULL - {z, w}])
            if not (all(t in S for t in three) and zw not in S):
                continue
            order = y if refl == 1 else y      # y is a circular order (possibly reversed)
            phi4 = 2 * wq(Q, u1, up, v1, vq)
            def phi5(zz):
                return wq(Q, u1, zz, v1, vq) + wq(Q, zz, up, v1, vq) - wq(Q, zz, up, v1, u1) - wq(Q, u1, zz, up, vq)
            f = phi5(z) + phi5(w)
            first = None
            for m in range(1, 5):
                S2, o2, groups = cat_blowup(S, order, z, w, m)
                d = nanuq_metric(S2, o2)
                # split U = {u1} + Z + W + {up} | {v1, vq}: alpha = d(vq,up) + d(u1,v1) - d(vq,v1) - d(u1,up)
                a = d[((vq, 0), (up, 0))] + d[((u1, 0), (v1, 0))] - d[((vq, 0), (v1, 0))] - d[((u1, 0), (up, 0))]
                want = 2 * (phi4 + m * f - Fraction(m * m, 2))
                tot += 1
                if a != want:
                    bad += 1
                if a < 0 and first is None:
                    first = m
            least.append(first)
            done = True
            break
        if done:
            break
print("Theorem 10'(c) formula on the %d excluded systems, m = 1..4: %d values, mismatches %d ; least m with negative weight: %s"
      % (len(bad17), tot, bad, sorted(least, key=lambda v: (v is None, v))))
