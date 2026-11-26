"""Referee's random generator of rooted binary phylogenetic networks by HYBRID INSERTION into random trees
(not the author's 'tree with twin leaves' construction), and fast displayed-tree computations.

insert_hybrid(net, target edge (u,v), source edge (a,b)):
    u -> h -> v   (new hybrid node h on the target edge)
    a -> t -> b   (new tree node t on the source edge)
    t -> h
allowed iff the edges are different and a is not v nor a descendant of v (acyclicity).
Classification (galled per Def. 2.3(vi), outer-labeled planar by a planarity test, level, blobs, ...) is
done afterwards on the explicit network with rnet.py.
"""
import random
from fractions import Fraction
from itertools import combinations, product
from collections import deque
import rnet


def random_tree(n, rng):
    net = {"r": ["L0", "L1"], "L0": [], "L1": []}
    cnt = 0
    for i in range(2, n):
        edges = [(v, c) for v in net for c in net[v]]
        edges.append(None)  # None = new root above the current root
        e = rng.choice(edges)
        leaf = f"L{i}"
        net[leaf] = []
        cnt += 1
        t = f"t{cnt}"
        if e is None:
            old = [v for v in net if v != leaf and all(v not in ch for ch in net.values())]
            assert len(old) == 1
            net[t] = [old[0], leaf]
        else:
            u, v = e
            net[u] = [t if c == v else c for c in net[u]]
            net[t] = [v, leaf]
    return net


def descendants_or_self(net, v):
    seen, stack = {v}, [v]
    while stack:
        x = stack.pop()
        for c in net[x]:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def insert_hybrid(net, target, source, tag):
    u, v = target
    a, b = source
    if (u, v) == (a, b):
        return None
    if a in descendants_or_self(net, v):
        return None
    new = {x: list(ch) for x, ch in net.items()}
    h, t = f"H{tag}", f"s{tag}"
    new[u] = [h if c == v else c for c in new[u]]
    new[h] = [v]
    new[a] = [t if c == b else c for c in new[a]]
    new[t] = [b, h]
    return new


def all_edges(net):
    return [(v, c) for v in net for c in net[v]]


def grow(n, k, rng, per_step=None, max_tries=60):
    """random tree on n leaves, then k hybrid insertions.  per_step(net) -> bool is an optional acceptance
    test applied after every insertion (rejection sampling).  Returns a network or None."""
    net = random_tree(n, rng)
    for i in range(k):
        for _ in range(max_tries):
            E = all_edges(net)
            cand = insert_hybrid(net, rng.choice(E), rng.choice(E), i + 1)
            if cand is None:
                continue
            if per_step is None or per_step(cand):
                net = cand
                break
        else:
            return None
    return net


# ----------------------------------------------------------------------------------------------
# fast displayed-tree computations (own implementation; cross-checked against rnet.displayed)
# ----------------------------------------------------------------------------------------------
def displayed_fast(net):
    """returns (leaves, per_tree_splits, Q).  Splits from clusters of the switching (rooted at the root),
    quartets from the four-point condition on leaf-to-leaf path lengths in the switching."""
    root, tree_nodes, hybrids, leaves = rnet.classify(net)
    par = rnet.parent_lists(net)
    L = list(leaves)
    idx = {l: i for i, l in enumerate(L)}
    n = len(L)
    full = (1 << n) - 1
    quads = list(combinations(range(n), 4))
    Qsets = [set() for _ in quads]
    per_tree = []
    # topological order (parents before children)
    indeg = {v: len(par[v]) for v in net}
    order, dq = [], deque([root])
    while dq:
        v = dq.popleft()
        order.append(v)
        for c in net[v]:
            indeg[c] -= 1
            if indeg[c] == 0:
                dq.append(c)
    for choice in product((0, 1), repeat=len(hybrids)):
        keep_parent = {}
        for h, c in zip(hybrids, choice):
            keep_parent[h] = par[h][1 - c]
        parent = {}
        for v in net:
            if v == root:
                continue
            parent[v] = keep_parent[v] if v in keep_parent else par[v][0]
        # clusters
        cl = {v: 0 for v in net}
        for l in L:
            cl[l] = 1 << idx[l]
        for v in reversed(order):
            if v != root:
                cl[parent[v]] |= cl[v]
        splits = set()
        for v in net:
            c = cl[v]
            if v != root and c != 0 and c != full:
                splits.add(min(c, full ^ c))
        per_tree.append(frozenset(splits))
        # depth and leaf-leaf distances via ancestor chains
        depth = {root: 0}
        for v in order:
            if v != root:
                depth[v] = depth[parent[v]] + 1
        anc = []
        for l in L:
            chain = {}
            v = l
            while True:
                chain[v] = depth[v]
                if v == root:
                    break
                v = parent[v]
            anc.append(chain)
        dist = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                v = L[j]
                while v not in anc[i]:
                    v = parent[v]
                dd = depth[L[i]] + depth[L[j]] - 2 * depth[v]
                dist[i][j] = dist[j][i] = dd
        for qi, (a, b, c, d) in enumerate(quads):
            s1 = dist[a][b] + dist[c][d]
            s2 = dist[a][c] + dist[b][d]
            s3 = dist[a][d] + dist[b][c]
            m = min(s1, s2, s3)
            assert (s1 == m) + (s2 == m) + (s3 == m) == 1
            Qsets[qi].add(0 if s1 == m else (1 if s2 == m else 2))
    return L, per_tree, quads, Qsets


def nanuq_fast(n, quads, Qsets):
    """matrix of Fractions; topology code 0: ab|cd, 1: ac|bd, 2: ad|bc for a<b<c<d (indices)."""
    D = [[Fraction(0)] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x != y:
                D[x][y] = Fraction(2 * n - 4)
    cherry = {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)), 2: ((0, 3), (1, 2))}
    for q, qs in zip(quads, Qsets):
        k = len(qs)
        for i, j in combinations(range(4), 2):
            notch = sum(1 for t in qs if (i, j) not in cherry[t])
            val = 2 * Fraction(notch, k)
            x, y = q[i], q[j]
            D[x][y] += val
            D[y][x] += val
    return D


def check_fast(net, order=None):
    """conclusion of Theorem 7 w.r.t. a circular order (default: one induced by a planar embedding).
    returns (status, detail, sigma_masks_in_order_positions, n)"""
    L, per_tree, quads, Qsets = displayed_fast(net)
    n = len(L)
    if order is None:
        order = rnet.planar_circular_order(net)
    pos = {l: i for i, l in enumerate(order)}
    full = (1 << n) - 1
    def to_pos(mask):
        m = 0
        for i, l in enumerate(L):
            if (mask >> i) & 1:
                m |= 1 << pos[l]
        return m if not (m & 1) else full ^ m
    sigma = set()
    for sp in per_tree:
        for m in sp:
            sigma.add(to_pos(m))
    # circularity of displayed splits
    def is_arc(m):
        ch = 0
        for i in range(n):
            if ((m >> i) & 1) != ((m >> ((i + 1) % n)) & 1):
                ch += 1
        return ch == 2
    for m in sigma:
        if not is_arc(m):
            return "notcircular", m, sigma, n
    D = nanuq_fast(n, quads, Qsets)
    li = [L.index(l) for l in order]
    neg, bad = {}, {}
    for i in range(n):
        for j in range(i + 1, n):
            a = (D[li[i]][li[j]] + D[li[(i + 1) % n]][li[(j + 1) % n]]
                 - D[li[i]][li[(j + 1) % n]] - D[li[(i + 1) % n]][li[j]])
            m = 0
            for p in range(i + 1, j + 1):
                m |= 1 << p
            m = m if not (m & 1) else full ^ m
            if a < 0:
                neg[(i, j)] = a
            if (a > 0) != (m in sigma):
                bad[(i, j)] = a
    if neg:
        return "neg", neg, sigma, n
    if bad:
        return "support", bad, sigma, n
    return "ok", None, sigma, n


def features(net):
    root, tree_nodes, hybrids, leaves = rnet.classify(net)
    Lset = set(leaves)
    bl = rnet.blobs(net)
    return {
        "n": len(leaves),
        "hyb": len(hybrids),
        "level": max((k for _, k in bl), default=0),
        "nblobs": len(bl),
        "bloblet": rnet.is_bloblet(net),
        "nonleaf_hyb_children": sum(1 for h in hybrids if net[h][0] not in Lset),
        "blob_levels": tuple(sorted(k for _, k in bl)),
    }
