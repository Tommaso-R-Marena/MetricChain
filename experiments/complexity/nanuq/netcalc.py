"""Independent calculator: explicit rooted binary phylogenetic networks (DAGs) -> displayed trees -> displayed
quartets -> NANUQ metric (Holtgrefe et al., Def. 4.1) -> Kalmanson tests.  Written independently of
splitsys.py / networks.py (no shared code) so that it can serve as a cross-check.

A network is a dict  node -> list of children.  Leaves are the nodes with no children; their names are the
taxon labels.  The root is the unique node with no parent.
"""
from itertools import combinations, permutations, product
from fractions import Fraction
import networkx as nx


def parents_of(net):
    par = {v: [] for v in net}
    for v, ch in net.items():
        for c in ch:
            par.setdefault(c, []).append(v)
    return par


def validate(net):
    """checks binary rooted network: root outdeg 2 indeg 0; tree nodes (1,2); hybrid nodes (2,1); leaves (1,0); acyclic."""
    par = parents_of(net)
    roots = [v for v in net if len(par[v]) == 0]
    assert len(roots) == 1, roots
    root = roots[0]
    hyb = []
    for v in net:
        i, o = len(par[v]), len(net[v])
        if v == root:
            assert o == 2, ("root", v, o)
        elif o == 0:
            assert i == 1, ("leaf", v, i)
        elif i == 1 and o == 2:
            pass
        elif i == 2 and o == 1:
            hyb.append(v)
        else:
            raise AssertionError(("bad degrees", v, i, o))
    G = nx.DiGraph([(v, c) for v in net for c in net[v]])
    assert nx.is_directed_acyclic_graph(G)
    return root, hyb


def leaves_of(net):
    return sorted(v for v in net if len(net[v]) == 0)


def displayed_trees(net):
    """list of (frozenset of clusters) for every choice of parent per hybrid node (with multiplicity).
    A cluster is a frozenset of leaves below a node of the cleaned tree."""
    root, hyb = validate(net)
    par = parents_of(net)
    L = set(leaves_of(net))
    out = []
    for choice in product((0, 1), repeat=len(hyb)):
        children = {v: list(ch) for v, ch in net.items()}
        for h, c in zip(hyb, choice):
            p = par[h][c]           # delete edge p -> h
            children[p].remove(h)
        # cluster of each node = set of labelled leaves reachable
        memo = {}
        def cl(v):
            if v in memo:
                return memo[v]
            if v in L:
                r = frozenset([v])
            else:
                r = frozenset().union(*[cl(c) for c in children[v]]) if children[v] else frozenset()
            memo[v] = r
            return r
        clusters = set()
        for v in children:
            c = cl(v)
            if c:
                clusters.add(c)
        out.append(frozenset(clusters))
    return out


def tree_splits_from_clusters(clusters, L):
    L = frozenset(L)
    s = set()
    for c in clusters:
        if 0 < len(c) < len(L):
            s.add(frozenset([c, L - c]))
    return s


def displayed_quartets(net):
    """dict 4-set (sorted tuple) -> set of quartets, each quartet a frozenset of two frozensets of size 2."""
    L = leaves_of(net)
    trees = displayed_trees(net)
    splitsets = [tree_splits_from_clusters(t, L) for t in trees]
    Q = {}
    for q in combinations(L, 4):
        a, b, c, d = q
        qs = set()
        for ss in splitsets:
            for (p1, p2) in ((frozenset([a, b]), frozenset([c, d])), (frozenset([a, c]), frozenset([b, d])),
                             (frozenset([a, d]), frozenset([b, c]))):
                for sp in ss:
                    A, B = tuple(sp)
                    if (p1 <= A and p2 <= B) or (p1 <= B and p2 <= A):
                        qs.add(frozenset([p1, p2]))
                        break
        assert qs, ("no displayed quartet on", q)
        Q[q] = qs
    return Q, set().union(*splitsets)


def nanuq_metric(net):
    """dict (x,y) -> Fraction, the NANUQ metric of Def. 4.1."""
    L = leaves_of(net)
    n = len(L)
    Q, splits = displayed_quartets(net)
    d = {}
    for x, y in combinations(L, 2):
        tot = Fraction(2 * n - 4)
        for z, w in combinations([l for l in L if l not in (x, y)], 2):
            q = tuple(sorted((x, y, z, w)))
            qs = Q[q]
            notcherry = sum(1 for quart in qs if frozenset([x, y]) not in quart)
            tot += 2 * Fraction(notcherry, len(qs))
        d[(x, y)] = d[(y, x)] = tot
    for x in L:
        d[(x, x)] = Fraction(0)
    return d, splits


def split_weights(d, order):
    """alpha_ij for the circular order `order` (list of leaves).  Returns dict frozenset(U) -> alpha, where
    U|V is the split S_ij, U = {order[i+1..j]}."""
    n = len(order)
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            xi, xi1, xj, xj1 = order[i], order[(i + 1) % n], order[j], order[(j + 1) % n]
            a = d[(xi, xj)] + d[(xi1, xj1)] - d[(xi, xj1)] - d[(xi1, xj)]
            U = frozenset(order[i + 1:j + 1])
            out[U] = a
    return out


def kalmanson_orders(d, L):
    """all circular orders (up to rotation and reflection) for which d is Kalmanson (all alpha >= 0)."""
    L = list(L)
    first, rest = L[0], L[1:]
    good = []
    for perm in permutations(rest):
        if perm[0] > perm[-1]:
            continue        # reflection
        order = [first] + list(perm)
        if all(a >= 0 for a in split_weights(d, order).values()):
            good.append(order)
    return good


def undirected(net):
    G = nx.MultiGraph()
    for v, ch in net.items():
        for c in ch:
            G.add_edge(v, c)
    return G


def outer_labeled_planar_order(net):
    """returns a circular order of the leaves induced by a planar embedding with all leaves on the outer face,
    or None.  (Suppressing the root does not affect planarity.)"""
    G = nx.Graph(undirected(net))
    L = leaves_of(net)
    apex = "__apex__"
    for l in L:
        G.add_edge(apex, l)
    ok, emb = nx.check_planarity(G)
    if not ok:
        return None
    return list(emb.neighbors_cw_order(apex))


def blobs_and_level(net):
    G = nx.Graph(undirected(net))
    root, hyb = validate(net)
    # suppress the root: connect its two children directly
    c1, c2 = net[root]
    H = nx.MultiGraph(undirected(net))
    H.remove_node(root)
    H.add_edge(c1, c2)
    Hs = nx.Graph(H)
    bridges = set()
    # bridges in a multigraph: an edge of Hs is a bridge iff it is a bridge of Hs and has multiplicity one
    for u, v in nx.bridges(Hs):
        if H.number_of_edges(u, v) == 1:
            bridges.add(frozenset([u, v]))
    K = nx.Graph()
    K.add_nodes_from(Hs.nodes())
    for u, v in Hs.edges():
        if frozenset([u, v]) not in bridges:
            K.add_edge(u, v)
    comps = [c for c in nx.connected_components(K) if len(c) > 1]
    levels = [sum(1 for h in hyb if h in c) for c in comps]
    return comps, levels


def is_galled(net):
    root, hyb = validate(net)
    par = parents_of(net)
    hyb_edges = {(p, h) for h in hyb for p in par[h]}
    for h in hyb:
        p, q = par[h]
        G = nx.Graph()
        for v, ch in net.items():
            for c in ch:
                if (v, c) in hyb_edges:
                    continue
                G.add_edge(v, c)
        if p not in G or q not in G or not nx.has_path(G, p, q):
            return False
    return True
