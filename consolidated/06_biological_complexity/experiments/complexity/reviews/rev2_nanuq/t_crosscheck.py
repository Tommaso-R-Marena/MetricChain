"""cross-check gen.displayed_fast / nanuq_fast / check_fast against the slow rnet implementation"""
import random
import rnet, gen
from t3a_nstar import NSTAR, ORDER
rng = random.Random(7)
cnt = 0
agree = 0
for trial in range(400):
    n = rng.choice([5, 6, 7]); k = rng.choice([0, 1, 2, 3])
    net = gen.grow(n, k, rng)
    if net is None: continue
    cnt += 1
    leaves, per_tree, Q = rnet.displayed(net)
    L, per2, quads, Qsets = gen.displayed_fast(net)
    assert L == leaves
    # splits
    s1 = set().union(*per_tree)
    full = (1 << len(L)) - 1
    s2 = set()
    for sp in per2:
        for m in sp:
            A = frozenset(L[i] for i in range(len(L)) if (m >> i) & 1)
            s2.add(frozenset((A, frozenset(L) - A)))
    assert s1 == s2, (net,)
    # quartets
    for q, qs in zip(quads, Qsets):
        a, b, c, d = [L[i] for i in q]
        conv = set()
        for t in qs:
            if t == 0: conv.add(frozenset((frozenset((a, b)), frozenset((c, d)))))
            if t == 1: conv.add(frozenset((frozenset((a, c)), frozenset((b, d)))))
            if t == 2: conv.add(frozenset((frozenset((a, d)), frozenset((b, c)))))
        assert conv == Q[(a, b, c, d)]
    d = rnet.nanuq_metric(leaves, Q)
    D = gen.nanuq_fast(len(L), quads, Qsets)
    for i, x in enumerate(L):
        for j, y in enumerate(L):
            assert d[(x, y)] == D[i][j]
    order = rnet.planar_circular_order(net)
    if order is not None:
        a1 = rnet.check_theorem(net, order)[0]
        a2 = gen.check_fast(net, order)[0]
        assert a1 == a2, (a1, a2, net)
        agree += 1
print("networks cross-checked:", cnt, "| planar ones with identical verdicts:", agree)
print("N*: slow:", rnet.check_theorem(NSTAR, ORDER)[0], "fast:", gen.check_fast(NSTAR, ORDER)[:2])
