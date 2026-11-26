"""
Generator of outer-labeled planar, galled, level-k bloblet networks (class B_k of Holtgrefe et al.)
and their displayed split systems.

Structure used (derivation in docs/complexity/NANUQ_NOTES.md):
  A galled outer-labeled planar bloblet with k hybrids on n leaves  <-->  a binary unrooted tree T on
  N = n + k circularly ordered positions together with k pairwise disjoint pairs of circularly
  adjacent positions (the two "half-leaves" of a hybrid), such that merging each pair into one hybrid
  node (with a pendant leaf) yields a graph whose only cut edges are the pendant leaf edges.
  A displayed tree keeps exactly one half-leaf of each pair.

Trees compatible with a circular order are generated as maximal families of pairwise compatible
nontrivial circular splits (triangulations of the N-gon).
"""
from functools import lru_cache
from itertools import combinations, product
import networkx as nx


@lru_cache(maxsize=None)
def interval_trees(lo, hi):
    """All rooted binary trees on the leaf interval lo..hi (inclusive), as nested tuples."""
    if lo == hi:
        return (lo,)
    out = []
    for mid in range(lo, hi):
        for L in interval_trees(lo, mid):
            for R in interval_trees(mid + 1, hi):
                out.append((L, R))
    return tuple(out)


def unrooted_trees(N):
    """All unrooted binary trees on leaves 0..N-1 compatible with the circular order 0,1,...,N-1.
    Each is returned as a rooted binary tree on 1..N-1 with leaf 0 attached at the root (a bijection)."""
    return interval_trees(1, N - 1)


def clades(t, acc):
    """collect leaf sets (frozensets) of all subtrees of rooted nested-tuple tree t; returns leafset of t."""
    if isinstance(t, int):
        s = frozenset([t])
    else:
        s = clades(t[0], acc) | clades(t[1], acc)
    acc.append(s)
    return s


def tree_splits(N, t):
    """nontrivial + trivial splits of the unrooted tree (leaf 0 attached at root of t): list of frozensets
    (the side not containing 0)."""
    acc = []
    clades(t, acc)
    return acc  # each clade of t is a side not containing leaf 0; the root clade {1..N-1} is trivial split of 0


def tree_graph(N, t):
    """networkx graph of the unrooted binary tree; leaves are ints 0..N-1, internal nodes are tuples."""
    G = nx.Graph()
    def rec(u):
        if isinstance(u, int):
            return u
        a, b = rec(u[0]), rec(u[1])
        G.add_edge(u, a)
        G.add_edge(u, b)
        return u
    r = rec(t)
    G.add_edge(r, 0)
    return G


def adjacent_pair_choices(N, k):
    """all sets of k pairwise disjoint cyclically adjacent pairs (p, p+1 mod N), as tuples of p."""
    out = []
    for ps in combinations(range(N), k):
        used = set()
        ok = True
        for p in ps:
            q = (p + 1) % N
            if p in used or q in used:
                ok = False
                break
            used.add(p)
            used.add(q)
        if ok:
            out.append(ps)
    return out


def build_network(N, t, pairs):
    """Return (G, leafmap, n) where G is the undirected network graph after merging hybrid pairs,
    leafmap: position -> final leaf index (0..n-1 in circular order), or None if not a bloblet."""
    G = tree_graph(N, t)
    # final leaf indices in circular order
    second = {(p + 1) % N: p for p in pairs}
    leafmap = {}
    idx = 0
    # start numbering at a position that is not the second half of a pair wrapping around
    start = 0
    if 0 in second:  # position 0 is second half of pair (N-1, 0): start at N-1
        start = N - 1
    order = [(start + i) % N for i in range(N)]
    for pos in order:
        if pos in second:
            leafmap[pos] = leafmap[second[pos]]
        else:
            leafmap[pos] = idx
            idx += 1
    n = idx
    # merge pairs
    H = G.copy()
    for p in pairs:
        q = (p + 1) % N
        pp = next(iter(H[p]))
        pq = next(iter(H[q]))
        if pp == pq:
            return None  # cherry -> parallel edges (2-blob)
        H.remove_node(p)
        H.remove_node(q)
        hyb = ("h", p)
        H.add_edge(hyb, pp)
        H.add_edge(hyb, pq)
        H.add_edge(hyb, ("leaf", leafmap[p]))
    # relabel remaining leaves
    mapping = {pos: ("leaf", leafmap[pos]) for pos in range(N) if pos in H}
    H = nx.relabel_nodes(H, mapping)
    # bloblet check: bridges must be exactly the n pendant edges
    br = list(nx.bridges(H))
    if len(br) != n:
        return None
    return H, leafmap, n


def displayed_splits(N, t, pairs, leafmap, n):
    """set of canonical split masks (side not containing final leaf 0) over all 2^k displayed trees,
    including trivial splits.  Also returns list of per-tree split sets."""
    base = tree_splits(N, t)  # frozensets of positions (side without position 0)
    full = (1 << n) - 1
    allmasks = set()
    per_tree = []
    for choice in product((0, 1), repeat=len(pairs)):
        deleted = set()
        for c, p in zip(choice, pairs):
            deleted.add(p if c else (p + 1) % N)
        masks = set()
        for s in base:
            m = 0
            for pos in s:
                if pos not in deleted:
                    m |= 1 << leafmap[pos]
            # complement side: positions not in s and not deleted
            if m == 0 or m == full:
                continue
            if m & 1:
                m ^= full
            if m == 0:
                continue
            masks.add(m)
        per_tree.append(frozenset(masks))
        allmasks |= masks
    return frozenset(allmasks), per_tree


def gen_bloblets(n, k):
    """yield (N, t, pairs, sigma) for all labelled bloblets in B'_k-ish (exactly k hybrids) on n leaves
    whose final circular order is 0..n-1 (all rotations of hybrid positions are produced)."""
    N = n + k
    trees = unrooted_trees(N)
    pair_choices = adjacent_pair_choices(N, k)
    for t in trees:
        for pairs in pair_choices:
            res = build_network(N, t, pairs)
            if res is None:
                continue
            H, leafmap, nn = res
            assert nn == n
            sigma, per_tree = displayed_splits(N, t, pairs, leafmap, n)
            yield N, t, pairs, sigma, per_tree, leafmap
