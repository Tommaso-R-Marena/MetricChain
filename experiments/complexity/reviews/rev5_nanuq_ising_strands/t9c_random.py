# t9c_random.py n trials seed -- REVIEWER'S OWN CODE: random tree-generated systems on n = 9..11 points
# (unions of a few random planar trees): Theorem 4, Theorem 10'(a), and Remark 1 of 7.1 (K'\K => wrong support?)
import itertools, collections, time, sys, random
import numpy as np
from mysplits import *

n = int(sys.argv[1]); trials = int(sys.argv[2]); seed = int(sys.argv[3])
rng = random.Random(seed)

def random_planar_tree(n, rng):
    """random triangulation of the n-gon -> set of non-trivial circular splits (masks)"""
    out = set()
    def rec(i, j):
        # polygon side from i to j (i<j), vertices i..j ; choose apex k
        if j - i < 2: return
        k = rng.randint(i + 1, j - 1)
        for (a, b) in ((i, k), (k, j)):
            if b - a >= 2:
                # diagonal (a,b) separates points a+1..b  (points labelled by gaps): use vertices as gaps:
                out.add(norm(sum(1 << t for t in range(a, b)), n))
            rec(a, b)
    rec(0, n - 1)
    # leaves = sides of the polygon: side t between vertex t and t+1 (t = 0..n-2), and the root side (n-1,0)
    return out

three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = [norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)]
lg_cache = {}; pat_cache = {}
def lg6(R):
    if R not in lg_cache: lg_cache[R] = six_locally_good_6(R)
    return lg_cache[R]
def pat6(R):
    if R not in pat_cache: pat_cache[R] = all(a in R for a in three) and any(t not in R for t in two)
    return pat_cache[R]
quads = list(itertools.combinations(range(n), 4))
def nanuq_fast(S):
    M = np.full((n, n), 2 * (2 * n - 4), dtype=np.int64); np.fill_diagonal(M, 0)
    for (a, b, c, d) in quads:
        p = displays(S, a, b, c, d); q = displays(S, a, d, b, c)
        assert p or q
        if p and q:
            for (x, y) in ((a, b), (c, d), (a, d), (b, c)): M[x, y] += 2; M[y, x] += 2
            for (x, y) in ((a, c), (b, d)): M[x, y] += 4; M[y, x] += 4
        elif p:
            for (x, y) in ((a, c), (b, d), (a, d), (b, c)): M[x, y] += 4; M[y, x] += 4
        else:
            for (x, y) in ((a, c), (b, d), (a, b), (c, d)): M[x, y] += 4; M[y, x] += 4
    return M
triv = trivial_splits(n)
subsets6 = list(itertools.combinations(range(n), 6))
st = collections.Counter(); ex = []
t0 = time.time(); seen = set()
# sanity: the random trees are planar binary trees
for _ in range(50):
    t = random_planar_tree(n, rng)
    assert len(t) == n - 3 and all(compatible(a, b, n) for a in t for b in t)
while st['systems'] < trials:
    k = rng.choice((2, 2, 2, 3, 3, 4, 5))
    S = set(triv)
    for _ in range(k): S |= random_planar_tree(n, rng)
    S = frozenset(S)
    if S in seen: continue
    seen.add(S)
    rs = [restrict(S, Y, n) for Y in subsets6]
    inKp = not any(pat6(R) for R in rs)
    if not inKp:
        st['outside K\' (skipped)'] += 1
        continue
    inK = all(lg6(R) for R in rs)
    st['systems'] += 1
    cls = 'K' if inK else "K'\\K"
    M = nanuq_fast(S); al = alpha2(M)
    kal = all(a >= 0 for a in al.values())
    supp_ok = all((a > 0) == (split_ij(i, j, n) in S) for (i, j), a in al.items())
    pos_on_S = all(a > 0 for (i, j), a in al.items() if split_ij(i, j, n) in S)
    st[(cls, 'Kalmanson' if kal else 'NOT Kalmanson', 'exact support' if (kal and supp_ok) else 'wrong support')] += 1
    if inK and not (kal and supp_ok): st['THEOREM 4 VIOLATION'] += 1
    if not (kal and pos_on_S): st["THEOREM 10'(a) VIOLATION"] += 1
    if cls == "K'\\K" and kal and supp_ok and len(ex) < 5: ex.append(show(S, n))
print("n =", n, "seed", seed, "time %.0fs" % (time.time() - t0))
for kk in sorted(st, key=str): print("  ", kk, st[kk])
print("  systems of K'\\K with exact support:", ex)
