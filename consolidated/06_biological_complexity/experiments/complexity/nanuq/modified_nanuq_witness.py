"""A level-1 network on 8 leaves for which the Modified NANUQ distance rho = (1/2, 1, 1/2, 1) of
Allman-Banos-Rhodes-Wicke (2025) is not circular decomposable: a 5-cycle whose hybrid node has a cherry below
it, with cherries at two of the other four positions.  Recomputed from the explicit rooted network."""
from fractions import Fraction as F
from netcalc import *

NET = {
    "r": ["c1", "c2"],
    "c1": ["k1", "c0"], "k1": ["l1", "l1b"], "c0": ["l0", "h"],
    "c2": ["k2", "c3"], "k2": ["l2", "l2b"], "c3": ["l3", "h"],
    "h": ["kx"], "kx": ["l4", "l5"],
    "l0": [], "l1": [], "l1b": [], "l2": [], "l2b": [], "l3": [], "l4": [], "l5": [],
}
ORDER = ["l0", "l1", "l1b", "l2", "l2b", "l3", "l4", "l5"]

if __name__ == "__main__":
    root, hyb = validate(NET)
    comps, levels = blobs_and_level(NET)
    print("hybrid nodes:", hyb, "| hybrids per blob:", levels, "| galled:", is_galled(NET),
          "| outer-labeled planar:", outer_labeled_planar_order(NET) is not None)
    L = leaves_of(NET)
    for name, rho in (("NANUQ (0,1,1/2,1)", (F(0), F(1), F(1, 2), F(1))),
                      ("Modified NANUQ (1/2,1,1/2,1)", (F(1, 2), F(1), F(1, 2), F(1))),
                      ("(1/4,1,5/8,1): c+s = 2a", (F(1, 4), F(1), F(5, 8), F(1)))):
        d, splits = parametric_metric(NET, rho)
        w = split_weights(d, ORDER)
        neg = {tuple(sorted(U)): str(a) for U, a in w.items() if a < 0}
        bad = {tuple(sorted(U)): str(a) for U, a in w.items()
               if (a > 0) != any(frozenset([U, frozenset(L) - U]) == s for s in splits)}
        good = kalmanson_orders(d, L)
        print(f"{name}: negative weights for the planar order: {neg}; support mismatches: {len(bad)}; "
              f"circular orders (of 2520) for which d is Kalmanson: {len(good)}")
