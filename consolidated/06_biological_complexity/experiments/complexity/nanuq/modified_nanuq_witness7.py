"""A smaller witness for Theorem 11(c), found by the referee of COMPLEXITY-REV-0004 and recomputed here from the
explicit rooted network: a level-1 network on SEVEN leaves — a 6-cycle (the hybrid node and five tree nodes, each
with one pendant leaf) with a cherry below the hybrid node — for which the Modified NANUQ distance
rho = (1/2, 1, 1/2, 1) gives the displayed split "hybrid cherry | rest" the weight -1 and is Kalmanson for none of
the 360 circular orders.  Also: which placements of two cherries on the 5-cycle of modified_nanuq_witness.py fail."""
from fractions import Fraction as F
from itertools import combinations
from netcalc import *

NET7 = {
    "r": ["a1", "b1"],
    "a1": ["l1", "a2"], "a2": ["l2", "h"],
    "b1": ["l5", "b2"], "b2": ["l4", "b3"], "b3": ["l3", "h"],
    "h": ["kx"], "kx": ["x1", "x2"],
    "l1": [], "l2": [], "l3": [], "l4": [], "l5": [], "x1": [], "x2": [],
}
ORDER7 = ["l1", "l2", "x1", "x2", "l3", "l4", "l5"]
MOD = (F(1, 2), F(1), F(1, 2), F(1))
NANUQ = (F(0), F(1), F(1, 2), F(1))


def report(name, net, order):
    root, hyb = validate(net)
    comps, levels = blobs_and_level(net)
    L = leaves_of(net)
    out = [f"{name}: hybrids per blob {levels}, galled {is_galled(net)}, planar {outer_labeled_planar_order(net) is not None}"]
    for nm, rho in (("NANUQ", NANUQ), ("Modified NANUQ", MOD)):
        d, splits = parametric_metric(net, rho)
        w = split_weights(d, order)
        neg = {tuple(sorted(U)): str(a) for U, a in w.items() if a < 0}
        bad = sum(1 for U, a in w.items() if (a > 0) != any(frozenset([U, frozenset(L) - U]) == s for s in splits))
        good = kalmanson_orders(d, L) if len(L) <= 8 else None
        out.append(f"   {nm}: negative weights (planar order) {neg}; support mismatches {bad}; Kalmanson orders: "
                   f"{len(good) if good is not None else 'not searched'}")
    return "\n".join(out)


def five_cycle(cherries):
    """5-cycle r(suppressed) - c1 - c0 - h - c3 - c2 with a cherry below h; `cherries` = subset of the four other
    positions {c1, c0, c3, c2} that carry a cherry instead of a leaf.  c0 and c3 are adjacent to h."""
    net = {"r": ["c1", "c2"], "h": ["kx"], "kx": ["x1", "x2"], "x1": [], "x2": []}
    order = {}
    for pos, (nxt, tag) in {"c1": ("c0", "p1"), "c0": ("h", "p0"), "c2": ("c3", "p2"), "c3": ("h", "p3")}.items():
        if pos in cherries:
            net[pos] = [tag + "k", nxt]
            net[tag + "k"] = [tag + "a", tag + "b"]
            net[tag + "a"], net[tag + "b"] = [], []
            order[pos] = [tag + "a", tag + "b"]
        else:
            net[pos] = [tag, nxt]
            net[tag] = []
            order[pos] = [tag]
    circ = order["c1"] + order["c0"] + ["x1", "x2"] + order["c3"] + order["c2"]
    return net, circ


if __name__ == "__main__":
    print(report("6-cycle with a cherry below the hybrid node (7 leaves)", NET7, ORDER7))
    print("5-cycle with a cherry below the hybrid node and cherries at two of the other four positions (8 leaves):")
    for pair in combinations(["c1", "c0", "c3", "c2"], 2):
        net, circ = five_cycle(set(pair))
        d, splits = parametric_metric(net, MOD)
        L = leaves_of(net)
        w = split_weights(d, circ)
        neg = {tuple(sorted(U)): str(a) for U, a in w.items() if a < 0}
        bad = sum(1 for U, a in w.items() if (a > 0) != any(frozenset([U, frozenset(L) - U]) == s for s in splits))
        good = kalmanson_orders(d, L)
        adj = [p for p in pair if p in ("c0", "c3")]
        print(f"   cherries at {pair} ({len(adj)} adjacent to the hybrid node): negative weights {neg}; support "
              f"mismatches {bad}; Kalmanson orders (of 2520): {len(good)}")
