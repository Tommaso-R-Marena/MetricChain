"""
All displayed split systems of outer-labeled planar galled semi-directed networks (class N of
Holtgrefe et al., any level, any number of blobs) on n circularly ordered leaves, n small.

Blobs with 2 or 3 articulation nodes and 3-cycles do not change displayed tree topologies, so up to
displayed splits every network is obtained as follows (derivation: docs/complexity/NANUQ_NOTES.md):

  rooted piece  :=  a leaf
                 |  a tree node with two rooted pieces below
                 |  a blob shape B (a bloblet on m+1 >= 4 leaves) entered through a NON-hybrid leaf u,
                    with rooted pieces substituted for its other m leaves
  network       :=  two rooted pieces joined at their roots                    (root on a cut edge)
                 |  a blob shape all of whose leaves are hybrid leaves, with rooted pieces substituted
                    for all its leaves                                        (root only inside the blob)

A rooted piece on leaves 0..n-1 (in this linear order) is represented by its set of clusters: intervals
(a,b), a<=b, including (0,n-1) and all singletons.  A network on leaves 0..n-1 (circular order) is
represented by the set of canonical split masks (splitsys.canon).
"""
from functools import lru_cache
from itertools import product
from splitsys import canon, is_trivial, all_circular_splits
from networks import gen_bloblets


@lru_cache(maxsize=None)
def blob_shapes(m):
    """all (sigma, hybrid_leaf_frozenset) of bloblets with m leaves (labelled 0..m-1 in circular order),
    every level 1..m.  sigma = frozenset of canonical masks (side without leaf 0)."""
    out = set()
    for k in range(1, m + 1):
        for N, t, pairs, sigma, per_tree, leafmap in gen_bloblets(m, k):
            hyb = frozenset(leafmap[p] for p in pairs)
            out.add((sigma, hyb))
    return frozenset(out)


def compositions(total, parts):
    """all tuples of `parts` positive integers summing to total"""
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - parts + 2):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def mask_to_interval_without(m, mask, u):
    """mask: subset of {0..m-1} (bitmask), a circular interval not containing u.  Return positions as list in
    circular order starting after u."""
    return [p for p in range(m) if (mask >> p) & 1]


@lru_cache(maxsize=None)
def rooted_pieces(n, maxblob):
    """set of frozensets of clusters (a,b) on leaves 0..n-1.  Blob shapes with up to maxblob leaves."""
    if n == 1:
        return frozenset([frozenset([(0, 0)])])
    out = set()
    # tree node: two pieces
    for n1 in range(1, n):
        for c1 in rooted_pieces(n1, maxblob):
            for c2 in rooted_pieces(n - n1, maxblob):
                cl = set(c1) | {(a + n1, b + n1) for a, b in c2} | {(0, n - 1)}
                out.add(frozenset(cl))
    # blob entered at non-hybrid leaf u, m other leaves
    for m in range(3, min(n, maxblob - 1) + 1):
        M = m + 1
        full = (1 << M) - 1
        for sigma, hyb in blob_shapes(M):
            for u in range(M):
                if u in hyb:
                    continue
                # positions after u in circular order: u+1, ..., u+m  -> slots 0..m-1
                slot = {((u + 1 + s) % M): s for s in range(m)}
                # clusters of the blob = sides of splits not containing u, as slot intervals
                bclusters = set()
                for msk in sigma:
                    side = msk if not (msk >> u) & 1 else full ^ msk
                    slots = sorted(slot[p] for p in range(M) if (side >> p) & 1)
                    assert slots == list(range(slots[0], slots[-1] + 1)), (sigma, u, msk)
                    bclusters.add((slots[0], slots[-1]))
                for sizes in compositions(n, m):
                    starts = [sum(sizes[:i]) for i in range(m)]
                    base = {(starts[a], starts[b] + sizes[b] - 1) for a, b in bclusters}
                    base.add((0, n - 1))
                    for combo in product(*[rooted_pieces(sz, maxblob) for sz in sizes]):
                        cl = set(base)
                        for st, c in zip(starts, combo):
                            cl |= {(a + st, b + st) for a, b in c}
                        out.add(frozenset(cl))
    return frozenset(out)


def clusters_to_masks(n, clusters, offset):
    """clusters of a rooted piece placed at leaves offset..offset+size-1 of a circular order on n leaves"""
    out = set()
    full = (1 << n) - 1
    for a, b in clusters:
        m = 0
        for p in range(a + offset, b + offset + 1):
            m |= 1 << p
        if m == 0 or m == full:
            continue
        out.add(canon(n, m))
    return out


@lru_cache(maxsize=None)
def network_systems(n, maxblob):
    """all displayed split systems (frozensets of canonical masks, trivial splits included) of networks in N on
    n >= 2 leaves 0..n-1 in circular order."""
    out = set()
    full = (1 << n) - 1
    # (A) two rooted pieces joined at their roots; first piece on leaves 0..n1-1
    for n1 in range(1, n):
        for c1 in rooted_pieces(n1, maxblob):
            for c2 in rooted_pieces(n - n1, maxblob):
                s = clusters_to_masks(n, c1, 0) | clusters_to_masks(n, c2, n1)
                out.add(frozenset(s))
    # also all rotations of case (A) arise by choosing different cut edges/pieces? Not all: add rotations explicitly
    rot = set()
    for s in out:
        for r in range(n):
            rot.add(frozenset(canon(n, rotate(n, m, r)) for m in s))
    out |= rot
    # (B') blob shape with all leaves hybrid, pieces substituted
    for m in range(4, min(n, maxblob) + 1):
        fullm = (1 << m) - 1
        for sigma, hyb in blob_shapes(m):
            if len(hyb) != m:
                continue
            for sizes in compositions(n, m):
                starts = [sum(sizes[:i]) for i in range(m)]
                for combo in product(*[rooted_pieces(sz, maxblob) for sz in sizes]):
                    s = set()
                    for msk in sigma:
                        mm = 0
                        for p in range(m):
                            if (msk >> p) & 1:
                                for q in range(starts[p], starts[p] + sizes[p]):
                                    mm |= 1 << q
                        if mm != 0 and mm != full:
                            s.add(canon(n, mm))
                    for st, c in zip(starts, combo):
                        s |= clusters_to_masks(n, c, st)
                    for r in range(n):
                        out.add(frozenset(canon(n, rotate(n, x, r)) for x in s))
    # add trivial splits
    triv = frozenset(canon(n, 1 << p) for p in range(n))
    return frozenset(frozenset(s | triv) for s in out)


def rotate(n, mask, r):
    full = (1 << n) - 1
    return ((mask << r) | (mask >> (n - r))) & full
