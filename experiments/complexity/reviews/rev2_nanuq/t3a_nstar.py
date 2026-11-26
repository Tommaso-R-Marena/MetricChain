"""Task 3(a): the network N* of Section 6 of the working paper, recomputed with the referee's code."""
from rnet import *

NSTAR = {
    "rho": ["w1", "w3"], "w1": ["a1", "w2"], "w2": ["a2", "p1"], "p1": ["b", "h1"],
    "w3": ["d", "q1"], "q1": ["h1", "q2"], "q2": ["h2", "c"],
    "h1": ["u"], "u": ["x", "h2"], "h2": ["y"],
    "a1": [], "a2": [], "b": [], "x": [], "y": [], "c": [], "d": [],
}
ORDER = ["a1", "a2", "b", "x", "y", "c", "d"]
PAPER_MATRIX = [
    [0, 21, 23, 26, 26, 23, 21],
    [21, 0, 17, 24, 26, 27, 25],
    [23, 17, 0, 20, 24, 29, 27],
    [26, 24, 20, 0, 20, 24, 26],
    [26, 26, 24, 20, 0, 20, 24],
    [23, 27, 29, 24, 20, 0, 17],
    [21, 25, 27, 26, 24, 17, 0],
]


def newick_unrooted(splits, leaves):
    return sorted(sorted(sorted(min(s, key=lambda side: (len(side), sorted(side)))) for s in splits if min(len(x) for x in s) > 1))


if __name__ == "__main__":
    root, tree_nodes, hybrids, leaves = classify(NSTAR)
    print("valid binary rooted network; root:", root, "| hybrids:", hybrids, "| leaves:", leaves)
    print("LSA network (root is the LSA of X):", is_lsa_network(NSTAR))
    G, H, _ = semi_directed(NSTAR)
    print("semi-directed network: nodes", G.number_of_nodes(), "edges", G.number_of_edges(),
          "| all internal degrees 3:", all(G.degree(v) == 3 for v in G if v not in leaves))
    br = bridges_multigraph(G)
    print("cut edges:", sorted(tuple(sorted(e)) for e in br), "| all pendant:", all(e & set(leaves) for e in br))
    bl = blobs(NSTAR)
    print("non-trivial blobs (size, #hybrids):", [(len(c), k) for c, k in bl], "| bloblet:", is_bloblet(NSTAR),
          "| level:", level(NSTAR))
    print("galled, Def 2.3(vi):", is_galled_def(NSTAR), "| articulation criterion:", is_galled_articulation(NSTAR),
          "| ancestor criterion:", is_galled_ancestor(NSTAR))
    po = planar_circular_order(NSTAR)
    print("outer-labeled planar:", po is not None, "| induced circular order from embedding:", po)
    # is the paper's order the same circular order?
    def canon(o):
        i = o.index("a1"); r = o[i:] + o[:i]
        rr = [r[0]] + r[1:][::-1]
        return min(tuple(r), tuple(rr))
    print("same circular order as the paper's (a1,a2,b,x,y,c,d):", canon(po) == canon(ORDER))

    leaves, per_tree, Q = displayed(NSTAR)
    print("displayed trees (non-trivial splits, small side), with multiplicity:")
    for sp in per_tree:
        print("    ", newick_unrooted(sp, leaves))
    print("distinct displayed trees:", len(set(per_tree)))
    d = nanuq_metric(leaves, Q)
    M = [[d[(a, b)] for b in ORDER] for a in ORDER]
    print("NANUQ matrix (order a1,a2,b,x,y,c,d):")
    for row in M:
        print("    ", [str(v) for v in row])
    print("equals the matrix printed in the working paper:", M == PAPER_MATRIX)
    print("is a metric (triangle inequality):", is_metric(d, leaves))
    al = alphas(d, ORDER)
    xy = frozenset(("x", "y"))
    print("alpha({x,y}|rest) =", al[xy], " = d(b,y)+d(x,c)-d(b,c)-d(x,y) =",
          d[("b", "y")], "+", d[("x", "c")], "-", d[("b", "c")], "-", d[("x", "y")])
    sigma = set().union(*per_tree)
    print("{x,y}|rest is a displayed split:", frozenset((xy, frozenset(leaves) - xy)) in sigma)
    print("all split weights for the planar order (U: alpha, displayed?):")
    for U, a in sorted(al.items(), key=lambda kv: (len(kv[0]), sorted(kv[0]))):
        disp = frozenset((U, frozenset(leaves) - U)) in sigma
        if a != 0 or disp:
            print("     ", sorted(U), a, "displayed" if disp else "NOT displayed", "<-- NEGATIVE" if a < 0 else "")
    good, total = kalmanson_orders(d, leaves)
    print("circular orders tested:", total, "| orders with all alpha_ij >= 0:", len(good))
    cnt = sum(1 for o in all_circular_orders(list(leaves)) if kalmanson_direct(d, o))
    print("orders satisfying the Kalmanson inequalities in direct form:", cnt)
    # restriction claim in the 'Why' paragraph
    for ai in ("a1", "a2"):
        Y = ["d", ai, "b", "x", "y", "c"]
        rest = set()
        for s in sigma:
            A, B = tuple(s)
            A2, B2 = frozenset(A) & set(Y), frozenset(B) & set(Y)
            if len(A2) >= 2 and len(B2) >= 2:
                rest.add(frozenset((A2, B2)))
        order6 = [l for l in ORDER if l in Y]
        allnt = set()
        for i in range(6):
            for j in range(i + 1, 6):
                U = frozenset(order6[i + 1:j + 1])
                if 2 <= len(U) <= 4:
                    allnt.add(frozenset((U, frozenset(order6) - U)))
        missing = allnt - rest
        print(f"restriction to {Y}: {len(rest)} of {len(allnt)} non-trivial circular splits; missing:",
              [sorted(min(s, key=len)) for s in missing])
