"""Task 1: are the 'displayed quartets of N' in the sense of the paper (via quarnets N|_xyzw, up-down paths)
the quartets of the displayed trees of N?  Tested on N* and on random networks of all kinds
(galled or not, planar or not)."""
import random, sys
from itertools import combinations
from collections import Counter
import rnet, gen, quarnet
from t3a_nstar import NSTAR

def compare(net, max_sets=None, rng=None):
    leaves, per_tree, Q = rnet.displayed(net)
    quads = list(combinations(leaves, 4))
    if max_sets and len(quads) > max_sets:
        quads = rng.sample(quads, max_sets)
    bad = 0
    for q in quads:
        viaq, sub = quarnet.quartets_via_quarnet(net, q)
        if viaq != Q[q]:
            bad += 1
            print("MISMATCH", q, viaq, Q[q], net)
    return len(quads), bad

tot, bad = compare(NSTAR)
print("N*: 4-sets compared:", tot, "mismatches:", bad)
rng = random.Random(11)
stats = Counter()
T = B = 0
nets = 0
for trial in range(int(sys.argv[1]) if len(sys.argv) > 1 else 300):
    n = rng.choice([5, 6, 7, 8]); k = rng.choice([1, 2, 2, 3, 3, 4])
    net = gen.grow(n, k, rng)
    if net is None:
        continue
    if not rnet.is_lsa_network(net):
        stats["notLSA"] += 1
        continue
    nets += 1
    g = rnet.is_galled_def(net); p = rnet.planar_circular_order(net) is not None
    stats[("galled" if g else "non-galled", "OLP" if p else "non-planar")] += 1
    t, b = compare(net, 35, rng)
    T += t; B += b
print("random LSA networks:", nets, dict(stats))
print("4-sets compared:", T, "| mismatches between quarnet-displayed quartets and quartets of displayed trees:", B)
