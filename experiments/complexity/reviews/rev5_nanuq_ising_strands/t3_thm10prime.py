# t3_thm10prime.py -- REVIEWER'S OWN CODE: Theorem 10'(c),(d)
import itertools, collections, sys, time
from fractions import Fraction
from mysplits import *

TG6 = tree_generated(6)
three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = {i: norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)}
pat = [S for S in TG6 if all(a in S for a in three) and any(t not in S for t in two.values())]
assert len(pat) == 17

def caterpillar(m, cherry_low=True):
    """split system of the planar caterpillar on points 0..m (0 = attachment point r, clade leaves 1..m)
    cherry_low: clusters {1,2},{1,2,3},... ; else {m-1,m},{m-2,..,m},..."""
    S = set(trivial_splits(m + 1))
    for k in range(2, m):
        if cherry_low:
            mask = sum(1 << i for i in range(1, k + 1))
        else:
            mask = sum(1 << i for i in range(m - k + 1, m + 1))
        S.add(norm(mask, m + 1))
    return frozenset(S)

def blowup(S6, zi, m, variant=(True, True)):
    """rotate S6 so that the labelling is (u1,z,w,up,v1,vq) = (0,1,2,3,4,5) with {z,w} = {zi,zi+1};
    replace z and w by caterpillar clades of m leaves.  returns (system, n, indices of the pieces)"""
    rot = [(zi - 1 + k) % 6 for k in range(6)]     # new point k is old point rot[k]
    S = restrict(S6, rot, 6) if False else None
    # relabel
    def relabel(mask):
        r = 0
        for k in range(6):
            if (mask >> rot[k]) & 1:
                r |= 1 << k
        return norm(r, 6)
    S = frozenset(relabel(s) for s in S6)
    if m == 1:
        return S, 6, dict(u1=[0], Z=[1], W=[2], up=[3], v1=[4], vq=[5])
    cat = caterpillar(m, variant[0])
    # substitute w (point 2) first, then z (point 1) so indices stay simple
    S, n = substitute(S, 6, 2, caterpillar(m, variant[1]), m + 1, 0)
    S, n = substitute(S, n, 1, cat, m + 1, 0)
    Z = list(range(1, 1 + m)); W = list(range(1 + m, 1 + 2 * m))
    return S, n, dict(u1=[0], Z=Z, W=W, up=[1 + 2 * m], v1=[2 + 2 * m], vq=[3 + 2 * m])

t0 = time.time()
results = []
for S6 in pat:
    miss = [i for i in range(6) if two[i] not in S6]
    for zi in miss:
        # terms of Sigma_6 in the labelling (u1,z,w,up,v1,vq) = rotation
        S, n, idx = blowup(S6, zi, 1)
        F4 = phi4_any(S, 0, 3, 4, 5); F5z = phi5_any(S, 0, 1, 3, 4, 5); F5w = phi5_any(S, 0, 2, 3, 4, 5)
        F6 = phi6_any(S, 0, 1, 2, 3, 4, 5)
        assert F6 == Fraction(-1, 2)
        least = None
        ok_formula = True
        for m in range(1, 7):
            for variant in ((True, True), (True, False), (False, True), (False, False)):
                Sm, nm, idm = blowup(S6, zi, m, variant)
                M = nanuq2(Sm, nm)
                al = alpha2(M)
                # split S = {u1} u Z u W u {up} | {v1,vq} : S_ij with U = points 0..2m+1 -> i = n-1, j = 2m+1
                i, j = 2 * m + 1, nm - 1       # S_ij = {x_{i+1..j}} = {v1,vq}
                a = Fraction(al[(i, j)], 2)     # alpha (M is 2*d)
                pred = 2 * (F4 + m * (F5z + F5w) - Fraction(m * m, 2))
                if a != pred:
                    ok_formula = False
                if a < 0 and least is None:
                    least = m
                if m == 1:
                    break
        results.append((S6, zi, F4, F5z, F5w, least, ok_formula))
print("pairs (system, missing 2-split):", len(results), " formula of (c) holds for m=1..6 (all four clade orientations):",
      all(r[6] for r in results), " time %.0fs" % (time.time() - t0))
print("least m with negative weight, histogram over pairs:", dict(collections.Counter(r[5] for r in results)))
per_sys = {}
for S6, zi, F4, F5z, F5w, least, okf in results:
    per_sys.setdefault(S6, []).append((least, zi, F4, F5z, F5w))
print("least m per system (min over its missing 2-splits):", dict(collections.Counter(min(v)[0] for v in per_sys.values())))
print("(Phi4, Phi5(z), Phi5(w)) values:", dict(collections.Counter((str(r[2]), str(r[3]), str(r[4])) for r in results)))

# (d): for the least m, Kalmanson for no circular order (all (n-1)!/2 orders, non-trivial splits only)
do_orders = len(sys.argv) > 1 and sys.argv[1] == 'orders'
if do_orders:
    t0 = time.time()
    none_cnt = 0; found = []
    for S6, v in per_sys.items():
        least, zi, F4, F5z, F5w = min(v)
        for variant in ((True, True), (True, False), (False, True), (False, False)):
            Sm, nm, idm = blowup(S6, zi, least, variant)
            M = nanuq2(Sm, nm)
            Mi = [[int(x) for x in row] for row in M]
            o = kalmanson_some_order(Mi, nontrivial_only=True)
            if o is None:
                none_cnt += 1
            else:
                found.append((show(S6, 6), zi, least, variant, o))
            if least == 1:
                break
    print("blow-ups at the least m (per system; 4 clade orientations when m>1): no Kalmanson order in", none_cnt,
          "cases; an order exists in", len(found), "cases", " time %.0fs" % (time.time() - t0))
    for f in found[:10]:
        print("   ORDER FOUND:", f)
    # control: the search finds an order for the 133 systems of K'_6 after scrambling labels
    import random
    rng = random.Random(5)
    Kp = [S for S in TG6 if S not in pat]
    okc = 0
    for S in Kp:
        M = nanuq2(S, 6)
        perm = list(range(6)); rng.shuffle(perm)
        Mi = [[int(M[perm[a]][perm[b]]) for b in range(6)] for a in range(6)]
        okc += kalmanson_some_order(Mi) is not None
    print("control: order found for", okc, "of", len(Kp), "scrambled metrics of K'_6")
    # how many of the 17 six-point systems are Kalmanson for SOME order (m = 1)
    c = 0
    for S in pat:
        M = nanuq2(S, 6)
        c += kalmanson_some_order([[int(x) for x in row] for row in M]) is not None
    print("of the 17 six-point systems, Kalmanson for some circular order:", c)
