"""The 7-leaf counterexample N*: an outer-labeled planar, level-2, NON-galled bloblet whose NANUQ metric is not
circular decomposable.  Everything is recomputed from the explicit rooted network (netcalc.py, exact rationals).

Rooted partner of N* (children lists):
    rho: w1, w3        w1: a1, w2       w2: a2, p1       p1: b, h1
    w3: d, q1          q1: h1, q2       q2: h2, c
    h1: u              u: x, h2         h2: y
Hybrid nodes h1 (parents p1, q1) and h2 (parents u, q2); h1 is an ancestor of h2 inside the same blob.
"""
from netcalc import *

NET = {
    "rho": ["w1", "w3"], "w1": ["a1", "w2"], "w2": ["a2", "p1"], "p1": ["b", "h1"],
    "w3": ["d", "q1"], "q1": ["h1", "q2"], "q2": ["h2", "c"],
    "h1": ["u"], "u": ["x", "h2"], "h2": ["y"],
    "a1": [], "a2": [], "b": [], "x": [], "y": [], "c": [], "d": [],
}
ORDER = ["a1", "a2", "b", "x", "y", "c", "d"]

def newick(clusters, L):
    """Newick string of the rooted tree given by its clusters"""
    cl = sorted(clusters, key=len)
    def build(c):
        if len(c) == 1:
            return next(iter(c))
        kids = [k for k in cl if k < c and not any(k < m < c for m in cl)]
        return "(" + ",".join(sorted(build(k) for k in kids)) + ")"
    return build(frozenset(L)) + ";"

if __name__ == "__main__":
    root, hyb = validate(NET)
    L = leaves_of(NET)
    comps, levels = blobs_and_level(NET)
    # bloblet: the only bridges of the semi-directed network are the 7 pendant edges
    import networkx as nx
    H = nx.MultiGraph(undirected(NET)); c1, c2 = NET[root]; H.remove_node(root); H.add_edge(c1, c2)
    bridges = [e for e in nx.bridges(nx.Graph(H)) if H.number_of_edges(*e) == 1]
    print("hybrid nodes:", hyb, "| blobs with their numbers of hybrids:", levels, "| bridges:", len(bridges),
          "(= number of leaves:", len(bridges) == len(L), ")")
    print("galled:", is_galled(NET), "| outer-labeled planar:", outer_labeled_planar_order(NET) is not None,
          "| a planar circular order:", outer_labeled_planar_order(NET))
    print("displayed trees:")
    for t in displayed_trees(NET):
        print("   ", newick(t, L))
    d, splits = nanuq_metric(NET)
    print("NANUQ metric d_N (rows/columns in the order", ORDER, "):")
    for xx in ORDER:
        print("   ", [int(d[(xx, yy)]) for yy in ORDER])
    w = split_weights(d, ORDER)
    print("split weights alpha w.r.t. the planar order (U -> alpha), negative ones marked:")
    for U, a in sorted(w.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
        disp = any(frozenset([U, frozenset(L) - U]) == s for s in splits)
        mark = "  <-- NEGATIVE" if a < 0 else ""
        if a != 0 or disp:
            print("    ", sorted(U), a, "(displayed)" if disp else "(not displayed)", mark)
    good = kalmanson_orders(d, L)
    print("number of circular orders (out of 360) for which d_N is Kalmanson:", len(good))
