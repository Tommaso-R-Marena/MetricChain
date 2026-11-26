# mynet.py -- REVIEWER'S OWN CODE (review5), written from the definitions of
# Holtgrefe et al., arXiv:2507.17308v2 (Defs 2.1-2.5, 4.1, Eq. (10), Prop. 2.8).
# It imports nothing from the repository under review.
#
# A rooted binary network is given by children lists (parallel edges allowed).
# NANUQ metric: d(x,y) = 2n-4 + 2*sum_{z,w} rho_xy(N|xyzw),  rho = UNWEIGHTED average over the
# quartet trees displayed by the quarnet.  We use Lemma 0 of the note (displayed quartets =
# restrictions of displayed trees); mylemma0.py tests that lemma against a literal Def. 2.5.
import itertools
import numpy as np
import networkx as nx


class Net:
    def __init__(self, children, root):
        ch = {u: list(vs) for u, vs in children.items()}
        nodes = set(ch)
        for vs in list(ch.values()):
            nodes.update(vs)
        for v in nodes:
            ch.setdefault(v, [])
        self.ch = ch
        self.root = root
        self.nodes = sorted(nodes, key=str)
        self.par = {v: [] for v in self.nodes}
        for u in self.nodes:
            for v in ch[u]:
                self.par[v].append(u)
        self.leaves = sorted([v for v in self.nodes if not ch[v]], key=str)
        self.hyb = sorted([v for v in self.nodes if len(self.par[v]) == 2], key=str)
        self._topo = None

    # ---------- validity (Def. 2.1 + LSA condition) ----------
    def topo(self):
        if self._topo is not None:
            return self._topo
        indeg = {v: len(self.par[v]) for v in self.nodes}
        stack = [v for v in self.nodes if indeg[v] == 0]
        order = []
        while stack:
            u = stack.pop()
            order.append(u)
            for v in self.ch[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    stack.append(v)
        if len(order) != len(self.nodes):
            return None
        self._topo = order
        return order

    def degree_ok(self):
        for v in self.nodes:
            i, o = len(self.par[v]), len(self.ch[v])
            if v == self.root:
                if (i, o) != (0, 2):
                    return False
            elif (i, o) not in ((1, 0), (1, 2), (2, 1)):
                return False
        return True

    def reach_avoiding(self, avoid=None):
        seen = {self.root}
        st = [self.root]
        while st:
            u = st.pop()
            for v in self.ch[u]:
                if v != avoid and v not in seen:
                    seen.add(v)
                    st.append(v)
        return seen

    def is_valid(self, need_lsa=True):
        if not self.degree_ok():
            return False
        if self.topo() is None:
            return False
        if len(self.reach_avoiding()) != len(self.nodes):
            return False
        if need_lsa:
            L = set(self.leaves)
            for v in self.nodes:
                if v == self.root or v in L:
                    continue
                if not (self.reach_avoiding(v) & L):
                    return False       # v is a stable ancestor below the root
        return True

    # ---------- switchings and displayed trees ----------
    def switchings(self):
        """yield parent maps (one parent per non-root node)"""
        hyb = self.hyb
        base = {v: self.par[v][0] for v in self.nodes if v != self.root}
        for choice in itertools.product((0, 1), repeat=len(hyb)):
            pm = dict(base)
            for h, c in zip(hyb, choice):
                pm[h] = self.par[h][c]
            yield pm

    def leaf_dist(self, pm):
        """path lengths between leaves in the spanning tree given by the parent map pm"""
        L = self.leaves
        n = len(L)
        anc = []
        for x in L:
            d = {}
            v = x
            k = 0
            while True:
                d[v] = k
                if v == self.root:
                    break
                v = pm[v]
                k += 1
            anc.append(d)
        D = np.zeros((n, n), dtype=np.int64)
        for i in range(n):
            ai = anc[i]
            for j in range(i + 1, n):
                aj = anc[j]
                best = min(ai[v] + aj[v] for v in ai if v in aj)
                D[i, j] = D[j, i] = best
        return D

    def tree_splits(self, pm):
        """splits (bitmask of the side not containing leaf 0) of the tree displayed by pm"""
        L = self.leaves
        idx = {x: i for i, x in enumerate(L)}
        full = (1 << len(L)) - 1
        cl = {v: 0 for v in self.nodes}
        for x in L:
            cl[x] = 1 << idx[x]
        for v in reversed(self.topo()):
            if v != self.root:
                cl[pm[v]] |= cl[v]
        out = set()
        for v in self.nodes:
            m = cl[v]
            if m and m != full:
                if m & 1:
                    m = full ^ m
                out.add(m)
        return frozenset(out)

    def displayed_trees(self):
        """set of displayed trees, each as a frozenset of splits"""
        return {self.tree_splits(pm) for pm in self.switchings()}

    def displayed_splits(self):
        s = set()
        for t in self.displayed_trees():
            s |= t
        return s

    # ---------- displayed quartets and the NANUQ metric ----------
    def quartet_table(self):
        """returns (quads, disp): quads = array of 4-subsets (indices into self.leaves),
        disp[q, t] = True iff topology t is displayed, t=0: ab|cd, 1: ac|bd, 2: ad|bc"""
        n = len(self.leaves)
        quads = np.array(list(itertools.combinations(range(n), 4)), dtype=np.int64)
        disp = np.zeros((len(quads), 3), dtype=bool)
        if len(quads) == 0:
            return quads, disp
        A, B, C, Dd = quads.T
        rows = np.arange(len(quads))
        for pm in self.switchings():
            D = self.leaf_dist(pm)
            s = np.stack([D[A, B] + D[C, Dd], D[A, C] + D[B, Dd], D[A, Dd] + D[B, C]], axis=1)
            t = s.argmin(axis=1)
            ss = np.sort(s, axis=1)
            assert (ss[:, 0] < ss[:, 1]).all(), "unresolved quartet in a binary tree?"
            disp[rows, t] = True
        return quads, disp

    def nanuq6(self):
        """6 * (NANUQ metric of Def. 4.1), integer matrix in the order of self.leaves"""
        return nanuq6_from_quartets(len(self.leaves), *self.quartet_table())

    def dqm_num(self):
        """numerator of the multiplicity-weighted displayed quartet metric (Sec. 3 of the paper):
        returns (matrix M, mu) with d~ = M/mu ; used only as a cross-check of Corollary 3.4"""
        n = len(self.leaves)
        mu = 2 ** len(self.hyb)
        quads = np.array(list(itertools.combinations(range(n), 4)), dtype=np.int64)
        M = np.full((n, n), (2 * n - 4) * mu, dtype=np.int64)
        np.fill_diagonal(M, 0)
        A, B, C, Dd = quads.T
        pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        cherry_of_top = {0: (0, 5), 1: (1, 4), 2: (2, 3)}
        for pm in self.switchings():
            D = self.leaf_dist(pm)
            s = np.stack([D[A, B] + D[C, Dd], D[A, C] + D[B, Dd], D[A, Dd] + D[B, C]], axis=1)
            t = s.argmin(axis=1)
            for pi, (u, v) in enumerate(pairs):
                noncherry = np.ones(len(quads), dtype=np.int64)
                for top, chs in cherry_of_top.items():
                    if pi in chs:
                        noncherry[t == top] = 0
                np.add.at(M, (quads[:, u], quads[:, v]), 2 * noncherry)
                np.add.at(M, (quads[:, v], quads[:, u]), 2 * noncherry)
        return M, mu

    # ---------- undirected structure ----------
    def ugraph(self):
        G = nx.MultiGraph()
        G.add_nodes_from(self.nodes)
        for u in self.nodes:
            for v in self.ch[u]:
                G.add_edge(u, v)
        return G

    def cut_edges(self):
        G = self.ugraph()
        S = nx.Graph(G)
        br = set()
        for u, v in nx.bridges(S):
            if G.number_of_edges(u, v) == 1:
                br.add(frozenset((u, v)))
        return br

    def blobs(self):
        """non-trivial blobs of the rooted network: list of node sets"""
        G = self.ugraph()
        br = self.cut_edges()
        H = nx.MultiGraph()
        H.add_nodes_from(G.nodes)
        for u, v in G.edges():
            if frozenset((u, v)) not in br:
                H.add_edge(u, v)
        return [set(c) for c in nx.connected_components(H) if len(c) > 1]

    def level(self):
        hs = set(self.hyb)
        return max([len(b & hs) for b in self.blobs()] + [0])

    def circular_order(self):
        """an induced circular order (list of leaves) if outer-labeled planar, else None"""
        S = nx.Graph(self.ugraph())
        apex = ('*apex*',)
        for x in self.leaves:
            S.add_edge(apex, x)
        ok, emb = nx.check_planarity(S)
        if not ok:
            return None
        return list(emb.neighbors_cw_order(apex))

    def is_galled(self):
        """Def. 2.3(vi), literally: for every hybrid node, its two hybrid edges lie on a cycle of the
        underlying graph that contains no other hybrid edge."""
        hyb_edges = set()
        for h in self.hyb:
            for p in self.par[h]:
                hyb_edges.add((p, h))
        for h in self.hyb:
            p1, p2 = self.par[h]
            if p1 == p2:
                continue                      # parallel edges: a 2-cycle of the two hybrid edges
            G = nx.Graph()
            G.add_nodes_from(self.nodes)
            for u in self.nodes:
                for v in self.ch[u]:
                    if (u, v) in hyb_edges:
                        continue
                    G.add_edge(u, v)
            G.remove_node(h)
            if not nx.has_path(G, p1, p2):
                return False
        return True


def nanuq6_from_quartets(n, quads, disp):
    M = np.full((n, n), 6 * (2 * n - 4), dtype=np.int64)
    np.fill_diagonal(M, 0)
    if len(quads) == 0:
        return M
    nd = disp.sum(axis=1)
    assert (nd >= 1).all()
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    cherry_tops = {0: 0, 5: 0, 1: 1, 4: 1, 2: 2, 3: 2}   # pair index -> topology in which it is a cherry
    for pi, (u, v) in enumerate(pairs):
        t = cherry_tops[pi]
        nc = nd - disp[:, t].astype(np.int64)            # number of displayed quartets where pair is NOT a cherry
        val = 12 * nc // nd
        assert (val * nd == 12 * nc).all()
        np.add.at(M, (quads[:, u], quads[:, v]), val)
        np.add.at(M, (quads[:, v], quads[:, u]), val)
    return M


def alphas(M, order_idx):
    """split weights alpha_ij (Prop. 2.8) for the circular order given as a list of matrix indices.
    returns dict {(i,j): alpha} for 0<=i<j<n ; S_ij = {x_{i+1..j}} | rest, positions in the order."""
    n = len(order_idx)
    o = order_idx
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            a = M[o[i], o[j]] + M[o[(i + 1) % n], o[(j + 1) % n]] - M[o[i], o[(j + 1) % n]] - M[o[(i + 1) % n], o[j]]
            out[(i, j)] = int(a)
    return out


def split_mask_of(order_idx, i, j, n):
    """bitmask (matrix indices) of the side of S_ij not containing matrix index 0"""
    m = 0
    for k in range(i + 1, j + 1):
        m |= 1 << order_idx[k]
    full = (1 << n) - 1
    if m & 1:
        m = full ^ m
    return m
