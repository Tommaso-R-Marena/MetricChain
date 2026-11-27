"""
Referee's independent calculator (review2).  No code shared with the author's programs.

A rooted binary phylogenetic network is a dict  node -> list of children  (leaves: empty list).
Everything is computed from the explicit DAG:

  * validity (degrees, acyclicity, LSA condition: the root is the least stable ancestor of X)
  * the semi-directed network (root suppressed) as an undirected multigraph with marked hybrid edges
  * blobs, level, bloblet, galled (Def. 2.3(vi) of arXiv:2507.17308, literally), articulation criterion
  * outer-labeled planarity (planarity of network + apex joined to all leaves) and an induced circular order
  * displayed trees (delete one parent edge per hybrid node), their splits, and their quartets
    (quartets are determined with the FOUR-POINT CONDITION on path lengths, not from splits)
  * NANUQ metric (Def. 4.1), exact rationals
  * split weights alpha_ij, Kalmanson tests for one order / all orders
"""
from fractions import Fraction
from itertools import combinations, permutations, product
from collections import deque
import networkx as nx


# ----------------------------------------------------------------------------------------------
# basic structure
# ----------------------------------------------------------------------------------------------
def parent_lists(net):
    par = {v: [] for v in net}
    for v, ch in net.items():
        for c in ch:
            par[c].append(v)
    return par


def classify(net):
    """returns (root, tree_nodes, hybrids, leaves); raises ValueError if not a binary rooted network."""
    for v, ch in net.items():
        for c in ch:
            if c not in net:
                raise ValueError(f"child {c} of {v} is not a node")
        if len(set(ch)) != len(ch):
            raise ValueError(f"parallel edges below {v} in the rooted network")
    par = parent_lists(net)
    roots = [v for v in net if not par[v]]
    if len(roots) != 1:
        raise ValueError(f"roots: {roots}")
    root = roots[0]
    tree_nodes, hybrids, leaves = [], [], []
    for v in net:
        i, o = len(par[v]), len(net[v])
        if v == root:
            if o != 2:
                raise ValueError("root must have out-degree 2")
        elif (i, o) == (1, 0):
            leaves.append(v)
        elif (i, o) == (1, 2):
            tree_nodes.append(v)
        elif (i, o) == (2, 1):
            hybrids.append(v)
        else:
            raise ValueError(f"node {v} has in/out degree {(i, o)}")
    # acyclicity (Kahn)
    indeg = {v: len(par[v]) for v in net}
    q = deque([root])
    seen = 0
    while q:
        v = q.popleft()
        seen += 1
        for c in net[v]:
            indeg[c] -= 1
            if indeg[c] == 0:
                q.append(c)
    if seen != len(net):
        raise ValueError("directed cycle")
    return root, tree_nodes, hybrids, sorted(leaves, key=str)


def is_lsa_network(net):
    """True iff the root is the least stable ancestor of the leaf set: no other node lies on ALL
    directed root-leaf paths (for all leaves)."""
    root, _, _, leaves = classify(net)
    L = set(leaves)
    for m in net:
        if m == root or m in L:
            continue
        # is some leaf reachable from the root while avoiding m ?
        stack, seen, ok = [root], {root}, False
        while stack and not ok:
            v = stack.pop()
            for c in net[v]:
                if c == m or c in seen:
                    continue
                if c in L:
                    ok = True
                    break
                seen.add(c)
                stack.append(c)
        if not ok:
            return False
    return True


# ----------------------------------------------------------------------------------------------
# semi-directed network
# ----------------------------------------------------------------------------------------------
def semi_directed(net):
    """Undirected multigraph of the semi-directed network (root suppressed).
    Edge attribute 'head' = hybrid node the edge points to (hybrid edge) or None."""
    root, tree_nodes, hybrids, leaves = classify(net)
    H = set(hybrids)
    G = nx.MultiGraph()
    G.add_nodes_from(v for v in net if v != root)
    for v, ch in net.items():
        if v == root:
            continue
        for c in ch:
            G.add_edge(v, c, head=(c if c in H else None))
    c1, c2 = net[root]
    assert not (c1 in H and c2 in H)
    head = c1 if c1 in H else (c2 if c2 in H else None)
    G.add_edge(c1, c2, head=head)
    return G, H, leaves


def bridges_multigraph(G):
    S = nx.Graph(G)
    out = set()
    for u, v in nx.bridges(S):
        if G.number_of_edges(u, v) == 1:
            out.add(frozenset((u, v)))
    return out


def blobs(net):
    """list of (node set, number of hybrid nodes) for the blobs with more than one node."""
    G, H, leaves = semi_directed(net)
    br = bridges_multigraph(G)
    K = nx.Graph()
    K.add_nodes_from(G.nodes())
    for u, v in nx.Graph(G).edges():
        if frozenset((u, v)) not in br:
            K.add_edge(u, v)
    out = []
    for comp in nx.connected_components(K):
        if len(comp) > 1:
            out.append((frozenset(comp), sum(1 for h in H if h in comp)))
    return out


def level(net):
    b = blobs(net)
    return max((k for _, k in b), default=0)


def is_bloblet(net):
    """single non-leaf blob  <=>  every cut edge is pendant and the internal nodes form one blob"""
    G, H, leaves = semi_directed(net)
    br = bridges_multigraph(G)
    L = set(leaves)
    for e in br:
        if not (e & L):
            return False
    internal = [v for v in G.nodes() if v not in L]
    b = blobs(net)
    if len(internal) == 1:
        return True
    return len(b) == 1 and set(b[0][0]) == set(internal)


def is_galled_def(net):
    """Definition 2.3(vi), literally, on the semi-directed multigraph: for every hybrid node h with hybrid
    edges e=(v,h), e'=(v',h) there is a cycle through e and e' containing no other hybrid edge."""
    G, H, leaves = semi_directed(net)
    for h in H:
        tails = [u if v == h else v for u, v, d in G.edges(h, data=True) if d["head"] == h]
        assert len(tails) == 2, (h, tails)
        v1, v2 = tails
        if v1 == v2:
            continue  # the two parallel hybrid edges form a 2-cycle with no other hybrid edge
        K = nx.Graph()
        K.add_nodes_from(n for n in G.nodes() if n != h)
        for u, v, d in G.edges(data=True):
            if d["head"] is None and u != h and v != h:
                K.add_edge(u, v)
        if not nx.has_path(K, v1, v2):
            return False
    return True


def is_galled_articulation(net):
    """'every hybrid node is an articulation node' (incident to a cut edge)."""
    G, H, leaves = semi_directed(net)
    br = bridges_multigraph(G)
    for h in H:
        if not any(h in e for e in br):
            return False
    return True


def is_galled_ancestor(net):
    """'no hybrid node is ancestral to another hybrid node of the same blob'."""
    root, tree_nodes, hybrids, leaves = classify(net)
    bl = blobs(net)
    blob_of = {}
    for idx, (comp, _) in enumerate(bl):
        for v in comp:
            blob_of[v] = idx
    D = nx.DiGraph([(v, c) for v in net for c in net[v]])
    for h in hybrids:
        desc = nx.descendants(D, h)
        for g in hybrids:
            if g != h and g in desc and blob_of.get(g) == blob_of.get(h):
                return False
    return True


def planar_circular_order(net):
    """a circular order of the leaves induced by a planar embedding with all leaves on one face, or None."""
    G, H, leaves = semi_directed(net)
    S = nx.Graph(G)
    apex = ("__apex__",)
    for l in leaves:
        S.add_edge(apex, l)
    ok, emb = nx.check_planarity(S)
    if not ok:
        return None
    return list(emb.neighbors_cw_order(apex))


# ----------------------------------------------------------------------------------------------
# displayed trees
# ----------------------------------------------------------------------------------------------
def switchings(net):
    """yield, for every choice of one deleted parent edge per hybrid node, the pruned undirected tree
    (networkx Graph; degree-2 nodes are NOT suppressed; all leaves are labelled leaves)."""
    root, tree_nodes, hybrids, leaves = classify(net)
    par = parent_lists(net)
    L = set(leaves)
    for choice in product((0, 1), repeat=len(hybrids)):
        dele = {(par[h][c], h) for h, c in zip(hybrids, choice)}
        T = nx.Graph()
        T.add_nodes_from(net)
        for v, ch in net.items():
            for c in ch:
                if (v, c) not in dele:
                    T.add_edge(v, c)
        # recursively delete unlabelled leaves (and an unlabelled root of degree <= 1)
        changed = True
        while changed:
            changed = False
            for v in list(T.nodes()):
                if v not in L and T.degree(v) <= 1:
                    T.remove_node(v)
                    changed = True
        assert nx.is_tree(T), "switching is not a tree"
        yield T


def tree_leaf_distances(T, leaves):
    dist = {}
    for a in leaves:
        dl = nx.single_source_shortest_path_length(T, a)
        for b in leaves:
            dist[(a, b)] = dl[b]
    return dist


def quartet_of(dist, a, b, c, d):
    """topology of the binary tree on {a,b,c,d} by the four-point condition: returns frozenset of 2 pairs."""
    s = [(dist[(a, b)] + dist[(c, d)], frozenset((frozenset((a, b)), frozenset((c, d))))),
         (dist[(a, c)] + dist[(b, d)], frozenset((frozenset((a, c)), frozenset((b, d))))),
         (dist[(a, d)] + dist[(b, c)], frozenset((frozenset((a, d)), frozenset((b, c)))))]
    s.sort(key=lambda t: t[0])
    assert s[0][0] < s[1][0] == s[2][0], "unresolved quartet in a binary tree?"
    return s[0][1]


def tree_splits(T, leaves):
    """set of splits (frozenset of two frozensets) of the tree T (degree-2 nodes allowed)."""
    Lset = frozenset(leaves)
    out = set()
    for u, v in T.edges():
        T2 = T.copy()
        T2.remove_edge(u, v)
        comp = nx.node_connected_component(T2, u)
        A = frozenset(x for x in comp if x in Lset)
        B = Lset - A
        if A and B:
            out.add(frozenset((A, B)))
    return out


def displayed(net):
    """returns (leaves, list of per-switching split sets, Q) where Q: 4-tuple -> set of quartet topologies."""
    root, tree_nodes, hybrids, leaves = classify(net)
    per_tree = []
    Q = {q: set() for q in combinations(leaves, 4)}
    for T in switchings(net):
        per_tree.append(frozenset(tree_splits(T, leaves)))
        dist = tree_leaf_distances(T, leaves)
        for q in Q:
            Q[q].add(quartet_of(dist, *q))
    return leaves, per_tree, Q


def nanuq_metric(leaves, Q):
    """Def. 4.1: d(x,y) = sum_{ {z,w} } 2 rho_xy(N|xyzw) + 2n-4,  rho = unweighted average over the SET of
    displayed quartets of [x,y not a cherry]."""
    n = len(leaves)
    d = {}
    for x, y in combinations(leaves, 2):
        tot = Fraction(2 * n - 4)
        pair = frozenset((x, y))
        for z, w in combinations([l for l in leaves if l != x and l != y], 2):
            key = tuple(l for l in leaves if l in (x, y, z, w))
            qs = Q[key]
            tot += 2 * Fraction(sum(1 for t in qs if pair not in t), len(qs))
        d[(x, y)] = d[(y, x)] = tot
    for x in leaves:
        d[(x, x)] = Fraction(0)
    return d


# ----------------------------------------------------------------------------------------------
# circular orders, split weights, Kalmanson
# ----------------------------------------------------------------------------------------------
def alphas(d, order):
    """dict: frozenset(U_ij) -> alpha_ij for all i<j (Prop. 2.8), U_ij = {x_{i+1},...,x_j}."""
    n = len(order)
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            xi, xi1, xj, xj1 = order[i], order[(i + 1) % n], order[j], order[(j + 1) % n]
            out[frozenset(order[i + 1:j + 1])] = d[(xi, xj)] + d[(xi1, xj1)] - d[(xi, xj1)] - d[(xi1, xj)]
    return out


def kalmanson_direct(d, order):
    """the Kalmanson inequalities in their usual form, for all i<j<k<l of the order."""
    n = len(order)
    for i, j, k, l in combinations(range(n), 4):
        a, b, c, e = order[i], order[j], order[k], order[l]
        cross = d[(a, c)] + d[(b, e)]
        if d[(a, b)] + d[(c, e)] > cross or d[(a, e)] + d[(b, c)] > cross:
            return False
    return True


def is_metric(d, leaves):
    for x, y, z in permutations(leaves, 3):
        if d[(x, y)] > d[(x, z)] + d[(z, y)]:
            return False
    return True


def all_circular_orders(leaves):
    first, rest = leaves[0], leaves[1:]
    for perm in permutations(rest):
        if str(perm[0]) > str(perm[-1]):
            continue
        yield [first] + list(perm)


def kalmanson_orders(d, leaves):
    good, total = [], 0
    for order in all_circular_orders(list(leaves)):
        total += 1
        if all(a >= 0 for a in alphas(d, order).values()):
            good.append(order)
    return good, total


def split_is_circular(split, order):
    A, B = tuple(split)
    n = len(order)
    flags = [x in A for x in order]
    changes = sum(1 for i in range(n) if flags[i] != flags[(i + 1) % n])
    return changes == 2


def check_theorem(net, order=None):
    """The conclusion of Theorem 7 for one network and one circular order.
    returns (status, info); status in {'ok','notcircular','neg','support'}"""
    leaves, per_tree, Q = displayed(net)
    sigma = set().union(*per_tree)
    if order is None:
        order = planar_circular_order(net)
    for s in sigma:
        if not split_is_circular(s, order):
            return "notcircular", s
    d = nanuq_metric(leaves, Q)
    al = alphas(d, order)
    Lset = frozenset(leaves)
    neg = {tuple(sorted(map(str, U))): a for U, a in al.items() if a < 0}
    if neg:
        return "neg", neg
    bad = {}
    for U, a in al.items():
        sp = frozenset((U, Lset - U))
        if (a > 0) != (sp in sigma):
            bad[tuple(sorted(map(str, U)))] = a
    if bad:
        return "support", bad
    return "ok", None
