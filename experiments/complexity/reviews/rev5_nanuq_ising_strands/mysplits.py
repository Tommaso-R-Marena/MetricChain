# mysplits.py -- REVIEWER'S OWN CODE: circular split systems, the NANUQ metric d_Sigma of a split
# system (Section 1 of NANUQ_LOCAL_CRITERION.md), split weights, the local terms Phi4/Phi5/Phi6.
# Points are 0..n-1 in circular order.  A split is the bitmask of its side NOT containing point 0.
# Nothing is imported from the repository under review.
import itertools
from fractions import Fraction
from functools import lru_cache
import numpy as np


def norm(m, n):
    full = (1 << n) - 1
    m &= full
    if m & 1:
        m ^= full
    return m


def interval(i, j, n):
    """mask of points i+1..j (cyclic), i != j"""
    m = 0
    k = (i + 1) % n
    while True:
        m |= 1 << k
        if k == j % n:
            break
        k = (k + 1) % n
    return m


def circular_splits(n):
    """all splits S_ij, as normalised masks (trivial ones included)"""
    out = set()
    for i in range(n):
        for j in range(n):
            if i != j:
                out.add(norm(interval(i, j, n), n))
    return out


def trivial_splits(n):
    return {norm(1 << i, n) for i in range(n)}


def compatible(a, b, n):
    full = (1 << n) - 1
    return (a & b) == 0 or (a & ~b & full) == 0 or (~a & b & full) == 0 or (~a & ~b & full) == 0


@lru_cache(None)
def planar_trees(n):
    """all binary trees on 0..n-1 whose splits are circular: maximal compatible sets of non-trivial
    circular splits (n-3 of them), returned as frozensets of masks INCLUDING trivial splits"""
    nontriv = sorted(s for s in circular_splits(n) if bin(s).count('1') not in (1, n - 1))
    res = set()
    def rec(start, chosen):
        if len(chosen) == n - 3:
            res.add(frozenset(chosen))
            return
        for k in range(start, len(nontriv)):
            s = nontriv[k]
            if all(compatible(s, c, n) for c in chosen):
                rec(k + 1, chosen + [s])
    rec(0, [])
    tr = frozenset(trivial_splits(n))
    return [frozenset(t | tr) for t in res]


@lru_cache(None)
def tree_generated(n):
    """all tree-generated circular split systems on n points (unions of planar binary trees)"""
    trees = planar_trees(n)
    if n <= 3:
        return [frozenset(trivial_splits(n))]
    seen = set()
    # closure under union, breadth first
    frontier = set(trees)
    seen |= frontier
    while frontier:
        new = set()
        for s in frontier:
            for t in trees:
                u = s | t
                if u not in seen:
                    seen.add(u)
                    new.add(u)
        frontier = new
    return sorted(seen, key=lambda s: sorted(s))


def displays(S, a, b, c, d):
    """does the split system S display ab|cd (some split separates {a,b} from {c,d})"""
    ab = (1 << a) | (1 << b)
    cd = (1 << c) | (1 << d)
    for m in S:
        x = m & ab
        y = m & cd
        if (x == ab and y == 0) or (x == 0 and y == cd):
            return True
    return False


def wgt(S, a, b, c, d):
    """weight w(ab|cd) for a,b,c,d in this circular order: 1 if only ab|cd is displayed, 1/2 if both
    planar quartets are, 0 if only ad|bc is"""
    p = displays(S, a, b, c, d)
    q = displays(S, a, d, b, c)
    assert p or q, "no planar quartet displayed (system not tree-generated?)"
    if p and q:
        return Fraction(1, 2)
    return Fraction(1 if p else 0)


def nanuq2(S, n):
    """2 * d_Sigma as an integer matrix (d_Sigma = 2n-4 + 2 sum rho; rho in {0,1/2,1} for planar systems;
    in general the average over the displayed quartets among the three topologies)"""
    D = [[Fraction(0)] * n for _ in range(n)]
    for x in range(n):
        for y in range(x + 1, n):
            D[x][y] = D[y][x] = Fraction(2 * n - 4)
    for q in itertools.combinations(range(n), 4):
        a, b, c, d = q
        tops = [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
        disp = [t for t in tops if displays(S, t[0][0], t[0][1], t[1][0], t[1][1])]
        assert disp
        for x, y in itertools.combinations(q, 2):
            nc = sum(1 for t in disp if (x, y) not in t)
            r = Fraction(nc, len(disp))
            D[x][y] += 2 * r
            D[y][x] += 2 * r
    M = np.zeros((n, n), dtype=object)
    for x in range(n):
        for y in range(n):
            v = 2 * D[x][y]
            assert v.denominator in (1, 3)
            M[x, y] = v
    return M


def alpha2(M, order=None):
    """dict {(i,j): alpha_ij} (times the scale of M) for the circular order (default identity)"""
    n = len(M)
    o = list(range(n)) if order is None else list(order)
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            out[(i, j)] = M[o[i]][o[j]] + M[o[(i + 1) % n]][o[(j + 1) % n]] - M[o[i]][o[(j + 1) % n]] - M[o[(i + 1) % n]][o[j]]
    return out


def split_ij(i, j, n, order=None):
    o = list(range(n)) if order is None else list(order)
    m = 0
    for k in range(i + 1, j + 1):
        m |= 1 << o[k]
    return norm(m, n)


def globally_good(S, n):
    """d_Sigma Kalmanson for the identity order with support exactly S"""
    M = nanuq2(S, n)
    for (i, j), a in alpha2(M).items():
        if a < 0:
            return False
        if (a > 0) != (split_ij(i, j, n) in S):
            return False
    return True


def kalmanson_identity(S, n):
    M = nanuq2(S, n)
    return all(a >= 0 for a in alpha2(M).values())


def dihedral_labellings(pts):
    """the 12 dihedral labellings of six points given in circular order"""
    pts = list(pts)
    out = []
    for r in range(6):
        rot = pts[r:] + pts[:r]
        out.append(rot)
        out.append([rot[0]] + rot[:0:-1])
    return out


def six_locally_good_6(S6):
    """S6: system on points 0..5.  all twelve labellings: Phi6(y1; y2,y3; y4; y5,y6) >= 0 with equality
    if y1y4|y5y6 is not displayed"""
    for lab in dihedral_labellings(range(6)):
        y1, y2, y3, y4, y5, y6 = lab
        # note: after a reflection the labels are in reversed circular order; the weights w(ab|cd) are
        # defined for 4 points in circular order and are invariant under reversal of the order
        f = phi6_any(S6, y1, y2, y3, y4, y5, y6)
        if f < 0:
            return False
        if f != 0 and not displays(S6, y1, y4, y5, y6):
            return False
    return True


def wq(S, a, b, c, d):
    """w of the quartet ab|cd where {a,b},{c,d} is a planar pairing (a,b adjacent among the four);
    order-agnostic version: 1 if ab|cd is the only displayed quartet of the 4-set, 1/2 if two are
    displayed, 0 if it is not displayed"""
    tops = [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
    disp = [displays(S, t[0][0], t[0][1], t[1][0], t[1][1]) for t in tops]
    k = sum(disp)
    assert k >= 1
    if not disp[0]:
        return Fraction(0)
    return Fraction(1, k)


def phi6_any(S, u1, z, w, up, v1, vq):
    """Phi6(z,w) = w(zw|v1vq) + w(zw|u1up) - w(zw|vq up) - w(zw|u1 v1)"""
    return wq(S, z, w, v1, vq) + wq(S, z, w, u1, up) - wq(S, z, w, vq, up) - wq(S, z, w, u1, v1)


def phi5_any(S, u1, z, up, v1, vq):
    return wq(S, u1, z, v1, vq) + wq(S, z, up, v1, vq) - wq(S, z, up, v1, u1) - wq(S, u1, z, up, vq)


def phi4_any(S, u1, up, v1, vq):
    return 2 * wq(S, u1, up, v1, vq)


def restrict(S, Y, n):
    """restriction of S to the points Y (sorted list); result on points 0..len(Y)-1"""
    Y = list(Y)
    k = len(Y)
    out = set()
    for m in S:
        r = 0
        for i, p in enumerate(Y):
            if (m >> p) & 1:
                r |= 1 << i
        if r and r != (1 << k) - 1:
            out.add(norm(r, k))
    return frozenset(out)


def six_locally_good(S, n):
    for Y in itertools.combinations(range(n), 6):
        if not six_locally_good_6(restrict(S, Y, n)):
            return False
    return True


def substitute(S1, n1, p, S2, n2, r):
    """Sigma_1 o_{p,r} Sigma_2 : points of X1 in order 0..n1-1 with p replaced by X2 minus r in the order
    following r.  Returns (system, n) on points 0..n1+n2-3."""
    n = n1 + n2 - 2
    # new index of the points of X1 other than p, and of X2 other than r
    new1 = {}
    for x in range(n1):
        if x < p:
            new1[x] = x
        elif x > p:
            new1[x] = x + (n2 - 2)
    new2 = {}
    for t in range(1, n2):
        y = (r + t) % n2
        new2[y] = p + t - 1
    X2mask = sum(1 << v for v in new2.values())
    X1mask = sum(1 << v for v in new1.values())
    out = set()
    for m in S1:
        r_ = 0
        for x in range(n1):
            if (m >> x) & 1:
                r_ |= X2mask if x == p else (1 << new1[x])
        if r_ and r_ != (1 << n) - 1:
            out.add(norm(r_, n))
    for m in S2:
        r_ = 0
        for y in range(n2):
            if (m >> y) & 1:
                r_ |= X1mask if y == r else (1 << new2[y])
        if r_ and r_ != (1 << n) - 1:
            out.add(norm(r_, n))
    return frozenset(out), n


def show(S, n):
    """non-trivial splits as strings of 1-based point labels of the side not containing point 1"""
    out = []
    for m in sorted(S, key=lambda m: (bin(m).count('1'), m)):
        k = bin(m).count('1')
        if k in (1, n - 1):
            continue
        out.append(''.join(str(i + 1) for i in range(n) if (m >> i) & 1))
    return ' '.join(out)


# ---------- search over all circular orders ----------
def kalmanson_some_order(M, nontrivial_only=True):
    """M: symmetric integer matrix (any positive scale of the metric).  Brute force over all
    (n-1)!/2 circular orders.  Returns an order with all alpha_ij >= 0 (non-trivial splits only if
    nontrivial_only) or None.  The search fixes point 0 first and removes reflections."""
    n = len(M)
    A = np.array(M, dtype=np.int64)
    rest = list(range(1, n))
    best = None
    I, J = [], []
    for i in range(n):
        for j in range(i + 1, n):
            if nontrivial_only and (j - i == 1 or (i == 0 and j == n - 1)):
                continue
            I.append(i); J.append(j)
    I = np.array(I); J = np.array(J)
    I1 = (I + 1) % n; J1 = (J + 1) % n
    chunk = []
    def flush(chunk):
        P = np.array(chunk, dtype=np.int64)          # (m, n)
        a = A[P[:, I], P[:, J]] + A[P[:, I1], P[:, J1]] - A[P[:, I], P[:, J1]] - A[P[:, I1], P[:, J]]
        ok = (a >= 0).all(axis=1)
        if ok.any():
            return list(P[np.argmax(ok)])
        return None
    for perm in itertools.permutations(rest):
        if perm[0] > perm[-1]:
            continue                                  # reflection
        chunk.append((0,) + perm)
        if len(chunk) >= 20000:
            r = flush(chunk)
            if r is not None:
                return r
            chunk = []
    if chunk:
        r = flush(chunk)
        if r is not None:
            return r
    return None
