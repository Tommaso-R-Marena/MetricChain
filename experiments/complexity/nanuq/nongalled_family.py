"""A family of outer-labeled planar, level-2, NON-galled bloblet networks N(s,t).

Rooted description (root rho):  backbone ((A,b),(c,D)) where A is a clade with t leaves and D a clade with s
leaves; hybrid h1 has parents p1 (on the pendant edge of b) and q1 (on the pendant edge of c); below h1 is a
tree node u with children: leaf x and hybrid h2; the second parent q2 of h2 lies on the pendant edge of c
below q1; below h2 is leaf y.  h1 is an ancestor of h2 in the same blob, so the network is not galled.
Circular order of the leaves:  A-leaves, b, x, y, c, D-leaves.

The four displayed trees (choice of parent of h1, of h2):
   (p1,u ): ((A,(b,(x,y))),(c,D))
   (p1,q2): ((A,(b,x)),((y,c),D))
   (q1,u ): ((A,b),(((x,y),c),D))
   (q1,q2): ((A,b),((x,(y,c)),D))
"""
import sys
from itertools import combinations
from splitsys import *

def caterpillar(leaves):
    t = leaves[0]
    for l in leaves[1:]:
        t = (t, l)
    return t

def clade_splits(t, acc):
    if isinstance(t, int):
        s = frozenset([t])
    else:
        s = clade_splits(t[0], acc) | clade_splits(t[1], acc)
    acc.append(s)
    return s

def family(s, t, shapeA=caterpillar, shapeD=caterpillar):
    A = list(range(0, t))
    b, x, y, c = t, t + 1, t + 2, t + 3
    D = list(range(t + 4, t + 4 + s))
    n = t + 4 + s
    TA, TD = shapeA(A), shapeD(D)
    trees = [((TA, (b, (x, y))), (c, TD)),
             ((TA, (b, x)), ((y, c), TD)),
             ((TA, b), (((x, y), c), TD)),
             ((TA, b), ((x, (y, c)), TD))]
    full = (1 << n) - 1
    sigma = set()
    per = []
    for tr in trees:
        acc = []
        clade_splits(tr, acc)
        ms = set()
        for cl in acc:
            m = 0
            for l in cl:
                m |= 1 << l
            if m != 0 and m != full:
                ms.add(canon(n, m))
        per.append(ms)
        sigma |= ms
    return n, sigma, (A, b, x, y, c, D)

def report(s, t):
    n, sigma, (A, b, x, y, c, D) = family(s, t)
    D2 = nanuq_2d(n, sigma)
    al = alphas_2(n, D2)
    neg = {k: v for k, v in al.items() if v < 0}
    bad_support = {k: v for k, v in al.items() if (v > 0) != (canon(n, split_mask(n, *k)) in sigma)}
    # split {x,y} | rest : gaps b and y  (gap g is between point g and g+1)
    key = (b, y)
    print(f"s={s} t={t} n={n}: 2*alpha for split {{x,y}}|rest = {al[key]}   #negative split weights = {len(neg)} "
          f"min = {min(al.values())}   support mismatches = {len(bad_support)}")
    return n, sigma, D2, al

if __name__ == "__main__":
    for s, t in [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (2, 6), (1, 8)]:
        report(s, t)
