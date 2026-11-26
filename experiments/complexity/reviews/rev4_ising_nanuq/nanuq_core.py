"""
Referee's own implementation (review4) for the NANUQ part.  Written from the definitions in
NANUQ_LOCAL_CRITERION.md section 1 and Holtgrefe et al. arXiv:2507.17308v2 section 2 (Defs. 2.1-2.5, 4.1)
BEFORE reading the author's code.  Everything starts from explicit rooted binary networks (DAGs).

Rooted network: dict  node -> list of children  (leaves: nodes with no children; names are strings).
"""
import itertools, random
from fractions import Fraction
import networkx as nx


# ====================================================================== rooted networks
class RNet:
    def __init__(self, children, root):
        self.ch = {u: list(vs) for u, vs in children.items()}
        for u in list(self.ch):
            for v in self.ch[u]:
                self.ch.setdefault(v, [])
        self.root = root
        self.par = {u: [] for u in self.ch}
        for u, vs in self.ch.items():
            for v in vs:
                self.par[v].append(u)

    # ---------- basic sets
    def leaves(self):
        return sorted(u for u in self.ch if not self.ch[u])

    def hybrids(self):
        return [u for u in self.ch if len(self.par[u]) == 2]

    def edges(self):
        return [(u, v) for u in self.ch for v in self.ch[u]]

    def topo(self):
        indeg = {u: len(self.par[u]) for u in self.ch}
        stack = [u for u in self.ch if indeg[u] == 0]
        out = []
        while stack:
            u = stack.pop()
            out.append(u)
            for v in self.ch[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    stack.append(v)
        return out if len(out) == len(self.ch) else None

    def descendants(self, c):
        seen = {c}
        stack = [c]
        while stack:
            u = stack.pop()
            for v in self.ch[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen

    # ---------- validity: Def. 2.1 + LSA condition
    def degree_ok(self):
        for u in self.ch:
            i, o = len(self.par[u]), len(self.ch[u])
            if u == self.root:
                if (i, o) != (0, 2):
                    return False
            elif (i, o) not in ((1, 0), (1, 2), (2, 1)):
                return False
        return True

    def reach_avoiding(self, avoid):
        seen = {self.root}
        stack = [self.root]
        while stack:
            u = stack.pop()
            for v in self.ch[u]:
                if v != avoid and v not in seen:
                    seen.add(v)
                    stack.append(v)
        return seen

    def root_is_lsa(self):
        L = self.leaves()
        if len(L) < 2:
            return False
        for v in self.ch:
            if v == self.root or not self.ch[v]:
                continue
            r = self.reach_avoiding(v)
            if not any(x in r for x in L):
                return False          # every root-leaf path passes through v
        return True

    def simple(self):
        return all(len(set(vs)) == len(vs) for vs in self.ch.values())

    def is_valid(self, allow_parallel=False):
        if self.topo() is None or not self.degree_ok():
            return False
        if not allow_parallel and not self.simple():
            return False
        if len(self.reach_avoiding(None)) != len(self.ch):
            return False
        return self.root_is_lsa()

    # ---------- underlying undirected multigraph (root kept as a node of degree 2; cycles are the same
    #            as in the semi-directed network)
    def ugraph(self):
        G = nx.MultiGraph()
        G.add_nodes_from(self.ch)
        for u, v in self.edges():
            G.add_edge(u, v)
        return G

    def hybrid_edge_set(self):
        H = set(self.hybrids())
        return [(u, v) for (u, v) in self.edges() if v in H]

    def is_galled(self):
        """Def. 2.3(vi), literally: for every hybrid node h with hybrid edges (v,h),(v',h) there is a cycle of
        the underlying graph containing both and no other hybrid edge."""
        H = set(self.hybrids())
        G = nx.Graph()
        G.add_nodes_from(self.ch)
        for u, v in self.edges():
            if v not in H:
                G.add_edge(u, v)
        for h in H:
            v, v2 = self.par[h]
            if v == v2:
                continue                       # parallel edges: the 2-cycle itself
            # a cycle through (v,h),(v2,h) with no other hybrid edge = a path v..v2 of non-hybrid edges avoiding h
            G2 = G.copy()
            G2.remove_node(h)
            if not nx.has_path(G2, v, v2):
                return False
        return True

    def planar_order(self):
        """None if not outer-labeled planar, else a circular order of the leaves induced by an embedding."""
        G = nx.Graph()
        G.add_nodes_from(self.ch)
        for u, v in self.edges():
            G.add_edge(u, v)
        hub = "__hub__"
        L = self.leaves()
        for x in L:
            G.add_edge(hub, x)
        ok, emb = nx.check_planarity(G)
        if not ok:
            return None
        return list(emb.neighbors_cw_order(hub))

    def admits_order(self, order):
        """is the circular order induced by some outer-labeled planar embedding?
        (add the cycle through the leaves in this order and a hub adjacent to all leaves: for n >= 4 the
        wheel is 3-connected and the network must lie in the face bounded by the cycle)"""
        G = nx.Graph()
        for u, v in self.edges():
            G.add_edge(u, v)
        hub = "__hub__"
        n = len(order)
        assert sorted(order) == self.leaves()
        if n <= 3:
            return self.planar_order() is not None
        for i, x in enumerate(order):
            G.add_edge(hub, x)
            G.add_edge(x, order[(i + 1) % n])
        ok, _ = nx.check_planarity(G)
        return ok

    def level(self):
        """(max number of hybrid nodes in a blob, number of non-trivial blobs); blobs = components of the
        underlying graph after deleting the cut edges (the rooted partner is a simple graph)"""
        G = nx.Graph()
        G.add_nodes_from(self.ch)
        for u, v in self.edges():
            G.add_edge(u, v)
        G.remove_edges_from(list(nx.bridges(G)))
        H = set(self.hybrids())
        best = nblob = 0
        for comp in nx.connected_components(G):
            if len(comp) > 1:
                nblob += 1
                best = max(best, len(comp & H))
        return best, nblob

    def is_bridge(self, u, v):
        G = self.ugraph()
        if G.number_of_edges(u, v) > 1:
            return False
        G.remove_edge(u, v)
        return not nx.has_path(G, u, v)

    def mu(self):
        """number of hybrid nodes whose child is not a leaf"""
        return sum(1 for h in self.hybrids() if self.ch[self.ch[h][0]])

    # ---------- displayed trees as split systems
    def displayed_trees(self, Y=None):
        """set of displayed trees restricted to the leaf set Y (default all), each as a frozenset of
        splits; a split is a frozenset of two frozensets.  One hybrid edge deleted per hybrid node."""
        L = self.leaves() if Y is None else sorted(Y)
        Lset = set(L)
        full = frozenset(L)
        order = self.topo()
        H = self.hybrids()
        trees = set()
        for choice in itertools.product([0, 1], repeat=len(H)):
            keep = {h: self.par[h][c] for h, c in zip(H, choice)}
            below = {}
            for u in reversed(order):
                if not self.ch[u]:
                    below[u] = frozenset([u]) if u in Lset else frozenset()
                else:
                    s = frozenset()
                    for v in self.ch[u]:
                        if v in keep and keep[v] != u:
                            continue
                        s |= below[v]
                    below[u] = s
            # parallel edges: if both parents equal, keep[v]==u holds for both copies; the union is unaffected
            splits = set()
            for u, s in below.items():
                if s and s != full:
                    splits.add(frozenset([s, full - s]))
            trees.add(frozenset(splits))
        return trees

    def split_system(self, Y=None):
        out = set()
        for t in self.displayed_trees(Y):
            out |= t
        return out

    # ---------- Def. 2.5, literally: union of all up-down paths between leaves of Y
    def updown_union(self, Y):
        """edges (u,v) of the rooted partner lying on some simple up-down path between two leaves of Y"""
        Y = sorted(Y)
        used = set()

        def down(u, target, visited, path_edges):
            # extend downward from u to target, simple
            if u == target:
                used.update(path_edges)
                return
            for v in self.ch[u]:
                if v in visited:
                    continue
                visited.add(v)
                path_edges.append((u, v))
                down(v, target, visited, path_edges)
                path_edges.pop()
                visited.discard(v)

        def up(u, target, visited, path_edges):
            # u is the current top of the upward part; try u as apex, then go further up
            for v in self.ch[u]:
                if v in visited:
                    continue
                visited.add(v)
                path_edges.append((u, v))
                down(v, target, visited, path_edges)
                path_edges.pop()
                visited.discard(v)
            for p in self.par[u]:
                if p in visited:
                    continue
                visited.add(p)
                path_edges.append((p, u))
                up(p, target, visited, path_edges)
                path_edges.pop()
                visited.discard(p)

        for a in range(len(Y)):
            for b in range(a + 1, len(Y)):
                up(Y[a], Y[b], {Y[a]}, [])
        return used

    def subnetwork_trees(self, Y):
        """displayed trees of N|_Y computed from the union U of up-down paths (orientation inherited).
        Returns (set of trees, number of sources of U, all switchings connected?)."""
        U = self.updown_union(Y)
        nodes = set()
        par = {}
        ch = {}
        for u, v in U:
            nodes.add(u); nodes.add(v)
            par.setdefault(v, []).append(u)
            ch.setdefault(u, []).append(v)
        sources = [u for u in nodes if u not in par]
        H = [u for u in nodes if len(par.get(u, [])) == 2]
        full = frozenset(Y)
        trees = set()
        connected = True
        # topological order of U
        indeg = {u: len(par.get(u, [])) for u in nodes}
        stack = [u for u in nodes if indeg[u] == 0]
        order = []
        while stack:
            u = stack.pop()
            order.append(u)
            for v in ch.get(u, []):
                indeg[v] -= 1
                if indeg[v] == 0:
                    stack.append(v)
        for choice in itertools.product([0, 1], repeat=len(H)):
            keep = {h: par[h][c] for h, c in zip(H, choice)}
            below = {}
            for u in reversed(order):
                if u in full and not ch.get(u):
                    below[u] = frozenset([u])
                else:
                    s = frozenset()
                    for v in ch.get(u, []):
                        if v in keep and keep[v] != u:
                            continue
                        s |= below[v]
                    below[u] = s
            if not any(below[s] == full for s in sources):
                connected = False
            splits = set()
            for u, s in below.items():
                if s and s != full:
                    splits.add(frozenset([s, full - s]))
            trees.add(frozenset(splits))
        return trees, len(sources), connected


# ====================================================================== split systems and metrics
def split_mask(split, index):
    a, b = tuple(split)
    m = 0
    for x in a:
        m |= 1 << index[x]
    return m


def quartets_from_splits(splits, leaves):
    """dict frozenset(4 leaves) -> set of displayed quartets, a quartet = frozenset({frozenset(pair), frozenset(pair)})"""
    Q = {}
    for sp in splits:
        A, B = tuple(sp)
        if len(A) < 2 or len(B) < 2:
            continue
        for p in itertools.combinations(sorted(A), 2):
            for q in itertools.combinations(sorted(B), 2):
                key = frozenset(p + q)
                Q.setdefault(key, set()).add(frozenset([frozenset(p), frozenset(q)]))
    return Q


def nanuq_metric(splits, leaves):
    """NANUQ metric (Def. 4.1 with Eq. (10)) from the displayed quartets; exact Fractions.
    Every 4-set must display at least one quartet (true for split systems of networks)."""
    n = len(leaves)
    Q = quartets_from_splits(splits, leaves)
    d = {}
    for x, y in itertools.combinations(leaves, 2):
        tot = Fraction(0)
        rest = [z for z in leaves if z != x and z != y]
        for z, w in itertools.combinations(rest, 2):
            qs = Q[frozenset([x, y, z, w])]
            pxy = frozenset([x, y])
            tot += Fraction(sum(1 for q in qs if pxy not in q), len(qs))
        d[(x, y)] = d[(y, x)] = 2 * tot + 2 * n - 4
    for x in leaves:
        d[(x, x)] = Fraction(0)
    return d


# parametric family (author's reading for outer-labeled planar networks): value = linear form in
# (rho_c, rho_s, rho_a, rho_o) plus constant;  stored as tuple (const, c, s, a, o) of integers
def param_metric(splits, order):
    n = len(order)
    pos = {x: i for i, x in enumerate(order)}
    Q = quartets_from_splits(splits, order)
    d = {}
    for x, y in itertools.combinations(order, 2):
        cnt = [0, 0, 0, 0]
        rest = [z for z in order if z != x and z != y]
        for z, w in itertools.combinations(rest, 2):
            qs = Q[frozenset([x, y, z, w])]
            pxy = frozenset([x, y])
            if len(qs) == 1:
                (q,) = tuple(qs)
                cnt[0 if pxy in q else 1] += 1
            elif len(qs) == 2:
                four = sorted([x, y, z, w], key=lambda t: pos[t])
                i, j = four.index(x), four.index(y)
                adjacent = (abs(i - j) in (1, 3))
                cnt[2 if adjacent else 3] += 1
            else:
                raise ValueError("three quartets displayed: not outer-labeled planar")
        d[(x, y)] = d[(y, x)] = (2 * n - 4, 2 * cnt[0], 2 * cnt[1], 2 * cnt[2], 2 * cnt[3])
    for x in order:
        d[(x, x)] = (0, 0, 0, 0, 0)
    return d


def ev(form, rho):
    return form[0] + sum(Fraction(a) * Fraction(r) for a, r in zip(form[1:], rho))


def circ_splits(order):
    """list of (i, j, split) for the circular splits S_ij, U_ij = {x_{i+1},...,x_j}, each split once"""
    n = len(order)
    out = []
    full = frozenset(order)
    seen = set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            U = frozenset(order[k % n] for k in range(i + 1, i + 1 + ((j - i) % n)))
            sp = frozenset([U, full - U])
            if sp in seen:
                continue
            seen.add(sp)
            out.append((i, j, sp))
    return out


def alpha(d, order, i, j, add=lambda a, b: a + b, sub=lambda a, b: a - b):
    n = len(order)
    xi, xj, xi1, xj1 = order[i], order[j], order[(i + 1) % n], order[(j + 1) % n]
    return sub(sub(add(d[(xi, xj)], d[(xi1, xj1)]), d[(xi, xj1)]), d[(xi1, xj)])


def vadd(a, b):
    return tuple(p + q for p, q in zip(a, b))


def vsub(a, b):
    return tuple(p - q for p, q in zip(a, b))


def alpha_forms(splits, order):
    """dict split -> linear form (const, c, s, a, o) of alpha_ij for the parametric family"""
    d = param_metric(splits, order)
    return {sp: alpha(d, order, i, j, vadd, vsub) for i, j, sp in circ_splits(order)}


NANUQ = (0, 1, Fraction(1, 2), 1)
MODIFIED = (Fraction(1, 2), 1, Fraction(1, 2), 1)


def check_conclusion(splits, order, rho=NANUQ):
    """(all alpha >= 0, support == splits, min alpha, list of bad splits)"""
    forms = alpha_forms(splits, order)
    ok_nonneg = True
    ok_support = True
    bad = []
    mn = None
    for sp, f in forms.items():
        a = ev(f, rho)
        mn = a if mn is None else min(mn, a)
        if a < 0:
            ok_nonneg = False
            bad.append((sp, a))
        if (a > 0) != (sp in splits):
            ok_support = False
            bad.append((sp, a))
    # every split of the system must be circular
    if any(sp not in forms for sp in splits):
        ok_support = False
    return ok_nonneg, ok_support, mn, bad


# ====================================================================== substitution of split systems
def substitute(S1, X1, p, S2, X2, r):
    """Sigma_1 o_{p,r} Sigma_2 on (X1 - p) + (X2 - r)"""
    A = frozenset(X1) - {p}
    B = frozenset(X2) - {r}
    full = A | B
    out = set()
    for sp in S1:
        s, t = tuple(sp)
        s2 = (s - {p}) | B if p in s else s
        if s2 and s2 != full:
            out.add(frozenset([s2, full - s2]))
    for sp in S2:
        s, t = tuple(sp)
        s2 = (s - {r}) | A if r in s else s
        if s2 and s2 != full:
            out.add(frozenset([s2, full - s2]))
    return out


# ====================================================================== generators
def random_tree(leaves, rng):
    """random rooted binary tree by random edge insertion"""
    leaves = list(leaves)
    rng.shuffle(leaves)
    cnt = itertools.count()
    root = "r"
    ch = {root: [leaves[0], leaves[1]]}
    for x in leaves[2:]:
        edges = [(u, v) for u in ch for v in ch[u]]
        if rng.random() < 1.0 / (len(edges) + 1):
            # above the root
            new = "t%d" % next(cnt)
            ch[new] = ch.pop(root)
            ch[root] = [new, x]
        else:
            u, v = rng.choice(edges)
            new = "t%d" % next(cnt)
            ch[u][ch[u].index(v)] = new
            ch[new] = [v, x]
    return RNet(ch, root)


def insert_hybrid(net, e1, e2, tag):
    """subdivide e1=(u1,v1) by a tree node a and e2=(u2,v2) by a hybrid node h, add a->h.
    e1 == 'ROOT' : a becomes a new root above the old root.  Returns a new RNet or None (cycle)."""
    ch = {u: list(vs) for u, vs in net.ch.items()}
    a, h = "a" + tag, "h" + tag
    root = net.root
    u2, v2 = e2
    if e1 == "ROOT":
        if net.root in net.descendants(v2) and False:
            return None
        ch[u2][ch[u2].index(v2)] = h
        ch[h] = [v2]
        ch[a] = [root, h]
        root = a
    else:
        u1, v1 = e1
        if e1 == e2:
            return None
        if u1 in net.descendants(v2):
            return None
        ch[u1][ch[u1].index(v1)] = a
        ch[a] = [v1]
        ch[u2][ch[u2].index(v2)] = h
        ch[h] = [v2]
        ch[a].append(h)
    return RNet(ch, root)


def random_network(n, k, rng, galled=True, planar=True, tries=200, leaf_child_only=False):
    """random rooted binary LSA network with k hybrid nodes (fewer if insertion keeps failing), obtained by
    successive hybrid insertions into a random tree; every intermediate network satisfies the filters
    (validity, and literally Def. 2.3(vi) / outer-labeled planarity when requested)."""
    net = random_tree(["x%d" % i for i in range(n)], rng)
    for step in range(k):
        for _ in range(tries):
            E = net.edges()
            e2 = rng.choice(E)
            e1 = "ROOT" if rng.random() < 0.08 else rng.choice(E)
            new = insert_hybrid(net, e1, e2, str(step))
            if new is None or not new.is_valid():
                continue
            if galled and not new.is_galled():
                continue
            if planar and new.planar_order() is None:
                continue
            if leaf_child_only and new.mu() > 0:
                continue
            net = new
            break
    return net


def canonical_key(net):
    """a cheap invariant used to count distinct networks: the multiset of displayed trees with multiplicity
    is not enough for isomorphism, so use a canonical form of the labelled DAG by iterated hashing."""
    order = net.topo()
    code = {}
    for u in reversed(order):
        if not net.ch[u]:
            code[u] = u
        else:
            code[u] = "(" + ",".join(sorted(code[v] for v in net.ch[u])) + ")" + ("H" if len(net.par[u]) == 2 else "")
    return code[net.root]
