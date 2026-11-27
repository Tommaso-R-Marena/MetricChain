# t9b_eight.py -- REVIEWER'S OWN CODE: all tree-generated systems on 8 points; classes K, K'\K, outside K';
# Theorem 4, Theorem 10'(a); is Remark 1 of Section 7.1 ("a system of K'\K ... gives positive weight to a
# split that no tree of the system has") true on 8 points?
import itertools, collections, time, sys
import numpy as np
from mysplits import *

t0 = time.time()
n = 8
trees = planar_trees(n)
# closure under union with integer bitsets over the list of circular splits
allsp = sorted(circular_splits(n))
sid = {s: i for i, s in enumerate(allsp)}
tb = [sum(1 << sid[s] for s in t) for t in trees]
seen = set(tb); frontier = set(tb)
while frontier:
    new = set()
    for s in frontier:
        for t in tb:
            u = s | t
            if u not in seen:
                seen.add(u); new.add(u)
    frontier = new
print("tree-generated systems on 8 points:", len(seen), "(planar trees %d)  %.0fs" % (len(trees), time.time() - t0), flush=True)

three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = [norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)]
lg_cache = {}; pat_cache = {}
def lg6(R):
    if R not in lg_cache: lg_cache[R] = six_locally_good_6(R)
    return lg_cache[R]
def pat6(R):
    if R not in pat_cache: pat_cache[R] = all(a in R for a in three) and any(t not in R for t in two)
    return pat_cache[R]

# fast NANUQ of a split system on n points (integers, 2*d)
quads = list(itertools.combinations(range(n), 4))
def nanuq_fast(S):
    M = np.full((n, n), 2 * (2 * n - 4), dtype=np.int64); np.fill_diagonal(M, 0)
    for (a, b, c, d) in quads:
        p = displays(S, a, b, c, d); q = displays(S, a, d, b, c)
        # planar quartets only (circular system): ab|cd and ad|bc
        if p and q:
            for (x, y) in ((a, b), (c, d), (a, d), (b, c)):
                M[x, y] += 2; M[y, x] += 2
            for (x, y) in ((a, c), (b, d)):
                M[x, y] += 4; M[y, x] += 4
        elif p:
            for (x, y) in ((a, c), (b, d), (a, d), (b, c)):
                M[x, y] += 4; M[y, x] += 4
        else:
            for (x, y) in ((a, c), (b, d), (a, b), (c, d)):
                M[x, y] += 4; M[y, x] += 4
    return M

subsets6 = list(itertools.combinations(range(n), 6))
st = collections.Counter(); ex = []
limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
for cnt, bits in enumerate(sorted(seen)):
    if limit and cnt >= limit: break
    S = frozenset(allsp[i] for i in range(len(allsp)) if (bits >> i) & 1)
    rs = [restrict(S, Y, n) for Y in subsets6]
    inKp = not any(pat6(R) for R in rs)
    inK = inKp and all(lg6(R) for R in rs)
    cls = 'K' if inK else ("K'\\K" if inKp else "outside K'")
    st[cls] += 1
    if cls == "outside K'" and cnt % 7:      # sample the big class
        continue
    M = nanuq_fast(S)
    al = alpha2(M)
    kal = all(a >= 0 for a in al.values())
    supp_ok = all((a > 0) == (split_ij(i, j, n) in S) for (i, j), a in al.items())
    pos_on_S = all(a > 0 for (i, j), a in al.items() if split_ij(i, j, n) in S)
    st[(cls, 'Kalmanson' if kal else 'not Kalmanson', 'exact support' if (kal and supp_ok) else 'wrong')] += 1
    if inK and not (kal and supp_ok): st['THEOREM 4 VIOLATION'] += 1
    if inKp and not (kal and pos_on_S): st["THEOREM 10'(a) VIOLATION"] += 1
    if cls == "K'\\K" and kal and supp_ok:
        if len(ex) < 5: ex.append(show(S, n))
for k in sorted(st, key=str): print("  ", k, st[k])
print("systems in K'\\K whose metric is Kalmanson with EXACT support (would contradict Remark 1 of 7.1):", len(ex), ex[:5])
print("time %.0fs" % (time.time() - t0))
