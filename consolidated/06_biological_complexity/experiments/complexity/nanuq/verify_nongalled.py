"""Independent verification of the non-galled family N(s,t) from an explicit DAG."""
import sys
from fractions import Fraction
from netcalc import *

def build(s, t):
    A = [f"a{i}" for i in range(1, t + 1)]
    D = [f"d{i}" for i in range(1, s + 1)]
    net = {}
    def cat(leaves, prefix):
        """caterpillar clade; returns its top node"""
        for l in leaves:
            net[l] = []
        top = leaves[0]
        for i, l in enumerate(leaves[1:]):
            node = f"{prefix}{i}"
            net[node] = [top, l]
            top = node
        return top
    topA = cat(A, "nA")
    topD = cat(D, "nD")
    for l in ("b", "x", "y", "c"):
        net[l] = []
    net["rho"] = ["vab", "vcd"]
    net["vab"] = [topA, "p1"]
    net["p1"] = ["b", "h1"]
    net["vcd"] = ["q1", topD]
    net["q1"] = ["h1", "q2"]
    net["q2"] = ["h2", "c"]
    net["h1"] = ["u"]
    net["u"] = ["x", "h2"]
    net["h2"] = ["y"]
    return net, A + ["b", "x", "y", "c"] + D

for s, t in [(1, 1), (2, 2), (3, 2), (2, 3)]:
    net, planar_order = build(s, t)
    root, hyb = validate(net)
    comps, levels = blobs_and_level(net)
    order = outer_labeled_planar_order(net)
    d, splits = nanuq_metric(net)
    L = leaves_of(net)
    n = len(L)
    w = split_weights(d, planar_order)
    neg = {tuple(sorted(U)): a for U, a in w.items() if a < 0}
    print(f"N({s},{t}): n={n} hybrids={hyb} blob levels={levels} galled={is_galled(net)} "
          f"outer-labeled planar={order is not None}")
    print("   circular order from a planar embedding:", order)
    print("   displayed trees (with multiplicity):", len(displayed_trees(net)), " distinct:", len(set(displayed_trees(net))))
    print("   negative split weights w.r.t. the order A,b,x,y,c,D:", neg)
    if n <= 9:
        good = kalmanson_orders(d, L)
        print("   circular orders (mod rotation/reflection) for which d_N is Kalmanson:", len(good), good[:3])
    if (s, t) == (2, 2):
        print("   distance matrix (order", planar_order, "):")
        for x in planar_order:
            print("     ", x, [str(d[(x, y)]) for y in planar_order])
