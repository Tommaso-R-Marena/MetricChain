# rn.py -- REVIEW 6, referee's own code, written from the definitions (HABIMRW arXiv:2507.17308v2,
# Defs. 2.1-2.5, 4.1, Eq. (10)) as restated in NANUQ_LOCAL_CRITERION.md section 1.
# Imports nothing from the repository under review.
#
# A rooted binary network is a dict  node -> list of children  (a DAG).  Leaves have no children.
# Displayed trees: one parent kept at every hybrid node (a switching).  Displayed quartets on a 4-set:
# the quartet topologies of the switching trees (Lemma 0 of the note; tested literally by earlier referees).
# NANUQ metric (Def. 4.1): d(x,y) = 2n-4 + 2*sum_{z,w} rho_xy(N|xyzw),  rho_xy = UNWEIGHTED average over the
# distinct displayed quartet trees of [x,y is not a cherry].   We return 6*d as integers.
import itertools
import numpy as np
import networkx as nx


class Net:
    def __init__(self, ch):
        ch = {u: list(vs) for u, vs in ch.items()}
        nodes = set(ch)
        for vs in list(ch.values()):
            nodes.update(vs)
        for v in nodes:
            ch.setdefault(v, [])
        self.ch = ch
        self.nodes = sorted(nodes, key=str)
        self.par = {v: [] for v in self.nodes}
        for u in self.nodes:
            for v in ch[u]:
                self.par[v].append(u)
        roots = [v for v in self.nodes if not self.par[v]]
        assert len(roots) == 1, roots
        self.root = roots[0]
        self.leaves = sorted([v for v in self.nodes if not ch[v]], key=str)
        self.hyb = sorted([v for v in self.nodes if len(self.par[v]) == 2], key=str)
        self.n = len(self.leaves)

    # ---- validity: binary, acyclic, root = least stable ancestor of the leaves --------------------
    def topo(self):
        indeg = {v: len(self.par[v]) for v in self.nodes}
        st = [v for v in self.nodes if indeg[v] == 0]
        out = []
        while st:
            u = st.pop()
            out.append(u)
            for v in self.ch[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    st.append(v)
        return out if len(out) == len(self.nodes) else None

    def valid(self):
        for v in self.nodes:
            i, o = len(self.par[v]), len(self.ch[v])
            if v == self.root:
                if (i, o) != (0, 2):
                    return False
            elif (i, o) not in ((1, 0), (1, 2), (2, 1)):
                return False
        if self.topo() is None:
            return False
        L = set(self.leaves)
        for v in self.nodes:            # no stable ancestor of all leaves below the root
            if v == self.root or v in L:
                continue
            seen = {self.root}
            st = [self.root]
            while st:
                u = st.pop()
                for x in self.ch[u]:
                    if x != v and x not in seen:
                        seen.add(x)
                        st.append(x)
            if not (seen & L):
                return False
            # every leaf must be reachable at all
        return True

    # ---- blobs and level ------------------------------------------------------------------------------
    def ugraph(self):
        G = nx.MultiGraph()
        G.add_nodes_from(self.nodes)
        for u in self.nodes:
            for v in self.ch[u]:
                G.add_edge(u, v)
        return G

    def blobs(self):
        """2-edge-connected components of the underlying multigraph with the root suppressed is the same
        as with the root kept for counting hybrids; returns list of node sets with >= 2 nodes."""
        G = self.ugraph()
        H = nx.Graph(G)
        bridges = set()
        # an edge is a bridge of the multigraph iff it is a bridge of the simple graph and not parallel
        mult = {}
        for u, v in G.edges():
            k = frozenset((u, v))
            mult[k] = mult.get(k, 0) + 1
        for u, v in nx.bridges(H):
            if mult[frozenset((u, v))] == 1:
                bridges.add(frozenset((u, v)))
        H2 = nx.Graph()
        H2.add_nodes_from(self.nodes)
        for u, v in H.edges():
            if frozenset((u, v)) not in bridges:
                H2.add_edge(u, v)
        return [set(c) for c in nx.connected_components(H2) if len(c) >= 2]

    def level(self):
        bl = self.blobs()
        hy = set(self.hyb)
        return max([len(b & hy) for b in bl], default=0)

    # ---- outer-labeled planarity and an induced circular order -----------------------------------------
    def planar_order(self):
        H = nx.Graph(self.ugraph())
        apex = ("apex",)
        for x in self.leaves:
            H.add_edge(apex, x)
        ok, emb = nx.check_planarity(H)
        if not ok:
            return None
        return list(emb.neighbors_cw_order(apex))

    # ---- switchings ----------------------------------------------------------------------------------
    def switchings(self):
        base = {v: self.par[v][0] for v in self.nodes if v != self.root}
        for choice in itertools.product((0, 1), repeat=len(self.hyb)):
            pm = dict(base)
            for h, c in zip(self.hyb, choice):
                pm[h] = self.par[h][c]
            yield pm

    def leafdist(self, pm, L):
        n = len(L)
        anc = []
        for x in L:
            d = {}
            v, k = x, 0
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
                D[i, j] = D[j, i] = min(ai[v] + aj[v] for v in ai if v in aj)
        return D

    def tree_clusters(self, pm, L):
        """clusters (frozensets of leaves) below every node in the switching tree pm"""
        below = {v: set() for v in self.nodes}
        for x in L:
            v = x
            while True:
                below[v].add(x)
                if v == self.root:
                    break
                v = pm[v]
        return {frozenset(s) for s in below.values() if s}

    def displayed_splits(self, L=None):
        """set of frozenset({A, B}) for all non-trivial and trivial splits of the displayed trees"""
        L = L or self.leaves
        full = frozenset(L)
        out = set()
        for pm in self.switchings():
            for c in self.tree_clusters(pm, L):
                if c and c != full:
                    out.add(frozenset((c, full - c)))
        return out

    # ---- displayed quartets and the NANUQ metric -----------------------------------------------------
    def quartet_masks(self, L=None):
        """for every 4-subset (a<b<c<d as indices into L) a bitmask of displayed topologies:
        bit0 ab|cd, bit1 ac|bd, bit2 ad|bc"""
        L = L or self.leaves
        n = len(L)
        Q = np.array(list(itertools.combinations(range(n), 4)), dtype=np.int64)
        a, b, c, d = Q[:, 0], Q[:, 1], Q[:, 2], Q[:, 3]
        mask = np.zeros(len(Q), dtype=np.int64)
        for pm in self.switchings():
            D = self.leafdist(pm, L)
            S = np.stack([D[a, b] + D[c, d], D[a, c] + D[b, d], D[a, d] + D[b, c]])
            t = np.argmin(S, axis=0)
            srt = np.sort(S, axis=0)
            assert np.all(srt[0] < srt[1]) and np.all(srt[1] == srt[2]), "unresolved quartet in a displayed tree"
            mask |= (1 << t)
        return Q, mask

    def nanuq6(self, L=None):
        """6 * NANUQ metric as an integer matrix, in the leaf order L"""
        L = L or self.leaves
        n = len(L)
        Q, mask = self.quartet_masks(L)
        D6 = np.zeros((n, n), dtype=np.int64)
        pairs_of_top = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
        for q, m in zip(Q, mask):
            cnt = bin(int(m)).count("1")
            for j in range(3):
                has = (int(m) >> j) & 1
                val = 12 * (cnt - has) // cnt            # 12*rho, an integer for cnt in {1,2,3}
                assert (12 * (cnt - has)) % cnt == 0
                for (i1, i2) in pairs_of_top[j]:
                    x, y = q[i1], q[i2]
                    D6[x, y] += val
                    D6[y, x] += val
        D6 += 6 * (2 * n - 4) * (1 - np.eye(n, dtype=np.int64))
        return D6


# ---- split weights for a circular order (Chepoi-Fichet / HABIMRW Prop. 2.8) ----------------------------
def alphas(D, order_idx):
    """D: matrix; order_idx: list of indices in circular order.  Returns dict {(i,j): alpha_ij}, i<j positions,
    alpha_ij = d(x_i,x_j)+d(x_{i+1},x_{j+1})-d(x_i,x_{j+1})-d(x_{i+1},x_j), split U = {x_{i+1..j}}."""
    n = len(order_idx)
    o = order_idx
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            i1, j1 = (i + 1) % n, (j + 1) % n
            out[(i, j)] = int(D[o[i], o[j]] + D[o[i1], o[j1]] - D[o[i], o[j1]] - D[o[i1], o[j]])
    return out


def is_kalmanson(D, order_idx):
    o = order_idx
    for a, b, c, d in itertools.combinations(range(len(o)), 4):
        s = D[o[a], o[c]] + D[o[b], o[d]]
        if s < D[o[a], o[b]] + D[o[c], o[d]] or s < D[o[a], o[d]] + D[o[b], o[c]]:
            return False
    return True


def kalmanson_search(D, first=None, limit=None):
    """Exact search for a circular order for which D is Kalmanson.  Backtracking by insertion; returns an order
    (list of indices) or None.  'first' = optional list of indices to insert first."""
    n = D.shape[0]
    idx = list(range(n))
    if first:
        idx = list(first) + [i for i in idx if i not in first]
    # allowed crossing pairings for each 4-set, computed on demand

    def ok_insert(order, pos, x):
        # new circular list: order[:pos] + [x] + order[pos:]
        new = order[:pos] + [x] + order[pos:]
        k = len(new)
        p = pos
        # all 4-subsets containing position p
        others = [i for i in range(k) if i != p]
        for i1 in range(len(others)):
            for i2 in range(i1 + 1, len(others)):
                for i3 in range(i2 + 1, len(others)):
                    q = sorted((others[i1], others[i2], others[i3], p))
                    a, b, c, d = new[q[0]], new[q[1]], new[q[2]], new[q[3]]
                    s = D[a, c] + D[b, d]
                    if s < D[a, b] + D[c, d] or s < D[a, d] + D[b, c]:
                        return None
        return new

    nodes_visited = [0]

    def rec(order, t):
        nodes_visited[0] += 1
        if limit and nodes_visited[0] > limit:
            raise RuntimeError("search limit")
        if t == n:
            return order
        x = idx[t]
        for pos in range(1, len(order) + 1):
            new = ok_insert(order, pos, x)
            if new is not None:
                r = rec(new, t + 1)
                if r is not None:
                    return r
        return None

    if n <= 3:
        return idx
    return rec(idx[:3], 3)


def brute_kalmanson(D):
    """all circular orders up to rotation/reflection (n <= 9)"""
    n = D.shape[0]
    found = []
    for perm in itertools.permutations(range(1, n)):
        if perm[0] > perm[-1]:
            continue
        o = [0] + list(perm)
        if is_kalmanson(D, o):
            found.append(o)
    return found
