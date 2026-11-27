"""Re-examine, from the explicit rooted network alone (netcalc.py), the example networks printed by
six_leaf_survey.py: validity, hybrid nodes per blob, galled or not, outer-labeled planarity, displayed trees, NANUQ
metric, split weights for the planar order 0..5, displayed splits, and the circular orders for which the metric is
Kalmanson (all 60 are tried).

Usage:  python3 six_leaf_examples.py LOGFILE        (the log of six_leaf_survey.py)
"""
import re
import sys
from netcalc import validate, leaves_of, blobs_and_level, is_galled, outer_labeled_planar_order, nanuq_metric, \
    split_weights, kalmanson_orders, displayed_trees


def parse(desc):
    net = {}
    for part in desc.split(";"):
        part = part.strip()
        if not part:
            continue
        v, ch = part.split(":")
        net[v.strip()] = [c.strip() for c in ch.split(",")]
    for v in list(net):
        for c in net[v]:
            net.setdefault(c, [])
    return net


def newick(clusters, L):
    cl = sorted(clusters, key=len)

    def build(c):
        if len(c) == 1:
            return next(iter(c))
        kids = [k for k in cl if k < c and not any(k < m < c for m in cl)]
        return "(" + ",".join(sorted(build(k) for k in kids)) + ")"
    return build(frozenset(L))


if __name__ == "__main__":
    lines = open(sys.argv[1]).read().split("\n")
    order = [f"L{q}" for q in range(6)]
    for i, l in enumerate(lines):
        m = re.match(r"\s*\[(.+?)\] first seen with (\d+) hybrid nodes; missing splits \(masks\) (.*)", l)
        if not m:
            continue
        status, k, missing = m.group(1), int(m.group(2)), m.group(3)
        net = parse(lines[i + 1])
        root, hyb = validate(net)
        comps, levels = blobs_and_level(net)
        L = leaves_of(net)
        d, splits = nanuq_metric(net)
        w = split_weights(d, order)
        Lset = frozenset(L)
        neg = {"".join(sorted(x[1] for x in U)): str(a) for U, a in w.items() if a < 0}
        wrong = {"".join(sorted(x[1] for x in U)): str(a) for U, a in w.items()
                 if a > 0 and frozenset([U, Lset - U]) not in splits}
        zero = {"".join(sorted(x[1] for x in U)): str(a) for U, a in w.items()
                if a == 0 and frozenset([U, Lset - U]) in splits}
        good_orders = kalmanson_orders(d, L)
        trees = sorted({newick(t, L) for t in displayed_trees(net)})
        print(f"[{status}] {k} hybrid nodes; missing splits {missing}")
        print(f"    network: {lines[i + 1].strip()}")
        print(f"    hybrid nodes per blob: {levels}; galled: {is_galled(net)}; outer-labeled planar: "
              f"{outer_labeled_planar_order(net) is not None}; distinct displayed trees: {len(trees)}")
        for t in trees:
            print(f"        {t}")
        print(f"    planar order 0..5: negative weights {neg}; positive on undisplayed splits {wrong}; zero on displayed"
              f" splits {zero}")
        print(f"    circular orders (of 60) for which the metric is Kalmanson: {len(good_orders)}")
