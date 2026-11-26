"""External anchor: reproduce the published NANUQ distances of Table 1 of arXiv:2507.17308 (6-taxon bloblets
of class B_2) with the referee's code.  (a) is the level-1 6-cycle; (b)-(e) are matched against the NANUQ
matrices of all 6-leaf galled outer-labeled planar bloblets of level <= 2 found by random hybrid insertion."""
import pickle, sys
from fractions import Fraction
import rnet, gen

def tri(rows):
    """upper-triangular rows (a: b..f, b: c..f, ...) -> symmetric 6x6"""
    M = [[0] * 6 for _ in range(6)]
    for i, r in enumerate(rows):
        for k, v in enumerate(r):
            M[i][i + 1 + k] = M[i + 1 + k][i] = v
    return M

TABLE1 = {
    "a": tri([[14, 17, 18, 17, 14], [11, 16, 19, 20], [15, 18, 19], [15, 16], [11]]),
    "b": tri([[14, 18, 18, 17, 13], [14, 17, 18, 17], [13, 17, 18], [14, 18], [14]]),
    "c": tri([[11, 16, 18, 18, 17], [13, 19, 19, 18], [14, 19, 18], [13, 16], [11]]),
    "d": tri([[13, 16, 18, 17, 16], [11, 17, 20, 19], [16, 19, 18], [13, 16], [11]]),
    "e": tri([[14, 17, 18, 17, 14], [11, 17, 19, 19], [16, 18, 18], [13, 16], [13]]),
}

def dihedral(M):
    out = set()
    n = len(M)
    for r in range(n):
        for sgn in (1, -1):
            perm = [(r + sgn * t) % n for t in range(n)]
            out.add(tuple(tuple(M[perm[i]][perm[j]] for j in range(n)) for i in range(n)))
    return out

# (a): 6-sunlet with hybrid leaf a
SUN = {"rho": ["vc", "vd"], "vc": ["c", "vb"], "vb": ["b", "h"], "vd": ["d", "ve"], "ve": ["e", "vf"],
       "vf": ["f", "h"], "h": ["a"], "a": [], "b": [], "c": [], "d": [], "e": [], "f": []}
L, per_tree, Q = rnet.displayed(SUN)
d = rnet.nanuq_metric(L, Q)
M = [[d[(x, y)] for y in "abcdef"] for x in "abcdef"]
print("Table 1(a) reproduced by the 6-cycle network with hybrid a:", M == TABLE1["a"])

mats = {}
for fn in sys.argv[1:]:
    for net, order, f, st in pickle.load(open(fn, "rb")):
        if f["n"] != 6 or not f["bloblet"] or f["level"] > 2:
            continue
        Ls, per2, quads, Qsets = gen.displayed_fast(net)
        D = gen.nanuq_fast(6, quads, Qsets)
        li = [Ls.index(l) for l in order]
        Mo = tuple(tuple(D[li[i]][li[j]] for j in range(6)) for i in range(6))
        key = min(dihedral(Mo))
        mats.setdefault(key, (net, f["level"]))
print("distinct NANUQ matrices (up to dihedral relabelling) of 6-leaf level<=2 galled OLP bloblets:", len(mats))
for name, T in TABLE1.items():
    key = min(dihedral(tuple(tuple(Fraction(v) for v in row) for row in T)))
    hit = mats.get(key)
    print(f"   Table 1({name}): matched by a generated bloblet: {hit is not None}" + (f" (level {hit[1]})" if hit else ""))
