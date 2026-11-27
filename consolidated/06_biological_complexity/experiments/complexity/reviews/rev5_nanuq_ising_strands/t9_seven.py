# t9_seven.py -- REVIEWER'S OWN CODE: all tree-generated systems on 7 points.
# Theorem 4 / Theorem 10'(a) on them, and the side remarks of Section 7.1:
#  Remark 1: "A system of K' \ K has a Kalmanson metric which gives positive weight to a split that no tree has."
#  Remark 3: single systems outside K' may be Kalmanson.
import itertools, collections, time
from mysplits import *

t0 = time.time()
n = 7
TG7 = tree_generated(7)
print("tree-generated systems on 7 points:", len(TG7), " (planar trees: %d)" % len(planar_trees(7)), "time %.0fs" % (time.time() - t0))
three = sorted({norm(interval(i, i + 3, 6), 6) for i in range(3)})
two = [norm((1 << i) | (1 << ((i + 1) % 6)), 6) for i in range(6)]
def pattern6(R):
    return all(a in R for a in three) and any(t not in R for t in two)
lg_cache = {}
def lg6(R):
    if R not in lg_cache:
        lg_cache[R] = six_locally_good_6(R)
    return lg_cache[R]
st = collections.Counter()
ex = []
for S in TG7:
    rs = [restrict(S, Y, 7) for Y in itertools.combinations(range(7), 6)]
    inK = all(lg6(R) for R in rs)
    inKp = not any(pattern6(R) for R in rs)
    M = nanuq2(S, 7); al = alpha2(M)
    kal = all(a >= 0 for a in al.values())
    supp_ok = all((a > 0) == (split_ij(i, j, 7) in S) for (i, j), a in al.items())
    pos_on_S = all(a > 0 for (i, j), a in al.items() if split_ij(i, j, 7) in S)
    cls = 'K' if inK else ("K'\\K" if inKp else "outside K'")
    st[cls] += 1
    st[(cls, 'Kalmanson' if kal else 'not Kalmanson', 'exact support' if (kal and supp_ok) else 'wrong support/sign')] += 1
    if inK and not (kal and supp_ok): st['THEOREM 4 VIOLATION'] += 1
    if inKp and not (kal and pos_on_S): st["THEOREM 10'(a) VIOLATION"] += 1
    if cls == "K'\\K" and kal and supp_ok and len(ex) < 3:
        ex.append(show(S, 7))
for k in sorted(st, key=str): print("  ", k, st[k])
print("examples of systems in K'\\K with Kalmanson metric and EXACT support (contradicting Remark 1 read literally):")
for e in ex: print("    ", e)
print("time %.0fs" % (time.time() - t0))
