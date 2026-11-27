"""For each linear form F among  s-o, o-s (mixed pairs), a-c (same-side pairs), 2a-s (pairs of a trivial split):
an A-structure with at most 6 leaves and a placement in which the local term of the pair (z,w) is F and z, w are
NOT hybrid leaves.  Replacing z and w by clades of m leaves keeps the structure in class A, and the split weight
becomes  2 m^2 F(rho) + O(m)  (Proposition 2: the m^2 pairs (z',w') all have the local term F, pairs inside a
clade have local term 0, the remaining terms are O(m))."""
from networks import unrooted_trees, adjacent_pair_choices
from twin_trees import system_of, leafmap_for
from parametric_local import T, TP, displayed

def placements(n):
    for r in range(n):
        for sgn in (1, -1):
            yield [(r + sgn * t) % n for t in range(n)]

want = {("TM", (0, 1, 0, -1)): None, ("TM", (0, -1, 0, 1)): None, ("T6", (-1, 0, 1, 0)): None, ("TP", (0, -1, 2, 0)): None}
for n in (5, 6):
    for k in range(1, 4):
        N = n + k
        for t in unrooted_trees(N):
            for pairs in adjacent_pair_choices(N, k):
                sig, nn = system_of(N, t, pairs)
                leafmap, _ = leafmap_for(N, pairs)
                hyb = {leafmap[p] for p in pairs}
                s = set(sig)
                for pl in placements(n):
                    if n == 6:
                        u1, z, up, v1, w, vq = pl
                        if z not in hyb and w not in hyb and displayed(s, u1, up, v1, vq):
                            key = ("TM", T(s, u1, up, v1, vq, z, w))
                            if key in want and want[key] is None:
                                want[key] = (k, t, pairs, sorted(hyb), pl)
                        u1, z, w, up, v1, vq = pl
                        if z not in hyb and w not in hyb and displayed(s, u1, up, v1, vq):
                            key = ("T6", T(s, u1, up, v1, vq, z, w))
                            if key in want and want[key] is None:
                                want[key] = (k, t, pairs, sorted(hyb), pl)
                    if n == 5:
                        a, u, b, z, w = pl
                        if z not in hyb and w not in hyb:
                            key = ("TP", TP(s, a, u, b, z, w))
                            if key in want and want[key] is None:
                                want[key] = (k, t, pairs, sorted(hyb), pl)
        if all(v is not None for v in want.values()):
            break
for key, v in want.items():
    print(key, "->", "NOT FOUND" if v is None else
          f"level {v[0]}, tree {v[1]}, twin pairs at positions {v[2]}, hybrid leaves {v[3]}, placement {v[4]}")
