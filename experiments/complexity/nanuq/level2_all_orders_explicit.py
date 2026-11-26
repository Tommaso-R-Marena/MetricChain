"""Theorem 12' of docs/complexity/NANUQ_LOCAL_CRITERION.md on EXPLICIT ROOTED NETWORKS with general pendant subnetworks.

Networks are generated as in level2_explicit.py (nested level-2 blobs entered through the root or through a cut
edge, with leaves, trees, level-1 cycles and further nested blobs as pendant subnetworks); the metric is computed
from the switchings by netcalc.py.  For every nested blob whose critical split has negative weight, the five leaves
of the proof are taken from the circular order alone:

    B1 = the leaf just after the block of the x- and y-leaves,   Cc = the leaf just before it,
    Y  = any leaf at y,   X1 = any leaf at x_1,   Z = any leaf at a middle b-position (j in M),

and the three strict four-point inequalities are checked for every such choice, together with
    d(B1,Cc) + d(Y,X1) - d(B1,Y) - d(Cc,X1)  =  -alpha(S*).
For networks with at most BRUTE leaves all circular orders are tried as well (netcalc.kalmanson_orders).

Usage: python3 level2_all_orders_explicit.py [number of networks [seed [max leaves [BRUTE]]]]   (defaults 400, 5, 12, 8)
"""
import random
import sys

from netcalc import validate, leaves_of, nanuq_metric, split_weights, kalmanson_orders, blobs_and_level, \
    outer_labeled_planar_order
from level2_explicit import random_network, formula


def main(count, seed, maxleaves, brute):
    rng = random.Random(seed)
    done = 0
    stats = {"networks": 0, "nested blobs": 0, "negative critical weights": 0, "choices of five leaves": 0,
             "networks searched over all orders": 0, "entered through a cut edge": 0, "pendant position not a single leaf": 0}
    ok = True
    while done < count:
        net, order, records = random_network(rng, maxleaves)
        L = leaves_of(net)
        if len(L) < 5 or not records:
            continue
        validate(net)
        comps, levels = blobs_and_level(net)
        assert max(levels) <= 2 and outer_labeled_planar_order(net) is not None
        done += 1
        stats["networks"] += 1
        d = None
        n = len(order)
        any_negative = False
        for rc in records:
            kB, k1, k2 = rc["k"]
            stats["nested blobs"] += 1
            if not (k1 >= 1 and kB >= 2):
                continue
            inside = set(rc["y"])
            for lst in rc["x"]:
                inside |= set(lst)
            named = set(inside)
            for lst in rc["b"] + rc["c"]:
                if lst is not None:
                    named |= set(lst)
            outside = [l for l in order if l not in named]          # the entry position, if any
            beta = [len(lst) if lst is not None else len(outside) for lst in rc["b"]]
            gamma = [len(lst) if lst is not None else len(outside) for lst in rc["c"]]
            xi = [len(lst) for lst in rc["x"]]
            pred = formula(beta, xi, len(rc["y"]), gamma)
            if pred >= 0:
                continue
            if d is None:
                d, _ = nanuq_metric(net)
                w = split_weights(d, order)
            any_negative = True
            stats["negative critical weights"] += 1
            stats["entered through a cut edge"] += rc["entry"] != ("A",)
            stats["pendant position not a single leaf"] += any(v > 1 for v in beta + gamma + xi + [len(rc["y"])])
            crit = w.get(frozenset(inside), w.get(frozenset(set(L) - inside)))
            ok &= (crit == pred)
            # the block of the x- and y-leaves in the circular order
            s = next(i for i in range(n) if order[i] in inside and order[i - 1] not in inside)
            m = len(inside)
            block = [order[(s + i) % n] for i in range(m)]
            ok &= set(block) == inside and block[0] in rc["y"] and block[-1] in rc["x"][0]
            Cc, B1 = order[(s - 1) % n], order[(s + m) % n]
            M = range(2, kB + 1) if k2 >= 1 else range(2, kB)
            zs = []
            for j in M:
                lst = rc["b"][j - 1]
                zs += lst if lst is not None else outside
            ok &= len(zs) > 0 and B1 not in zs and Cc not in zs
            for Z in zs:
                for Y in rc["y"]:
                    for X1 in rc["x"][0]:
                        stats["choices of five leaves"] += 1
                        p1 = d[(B1, Cc)] + d[(Y, X1)]
                        ok &= p1 > d[(B1, Y)] + d[(Cc, X1)] and p1 > d[(B1, X1)] + d[(Cc, Y)]
                        ok &= p1 - d[(B1, Y)] - d[(Cc, X1)] == -pred
                        p2 = d[(B1, Cc)] + d[(Z, Y)]
                        ok &= p2 > d[(B1, Z)] + d[(Cc, Y)] and p2 > d[(B1, Y)] + d[(Z, Cc)]
                        p3 = d[(B1, Cc)] + d[(Z, X1)]
                        ok &= p3 > d[(B1, Z)] + d[(Cc, X1)] and p3 > d[(B1, X1)] + d[(Z, Cc)]
            if not ok:
                print("FAILURE", rc["k"], rc["entry"], beta, gamma, xi, len(rc["y"]))
                return False
        if any_negative and n <= brute:
            stats["networks searched over all orders"] += 1
            ok &= kalmanson_orders(d, L) == []
            if not ok:
                print("FAILURE: an order exists", order)
                return False
    print(f"explicit rooted networks of level <= 2 (seed {seed}, at most {maxleaves} leaves): {stats}")
    print("negative critical weight: the three strict four-point inequalities for every admissible choice of the five leaves, "
          f"the identity for the first difference, and no circular order at all up to {brute} leaves: {ok}")
    return ok


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:]]
    count, seed, maxleaves, brute = (a + [400, 5, 12, 8][len(a):])[:4]
    sys.exit(0 if main(count, seed, maxleaves, brute) else 1)
