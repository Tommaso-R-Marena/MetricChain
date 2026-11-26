"""Referee's independent code for circular split systems on points 0..n-1 (circular order 0,1,...,n-1).

A split is stored as the bitmask of its side NOT containing point 0.
"""
from fractions import Fraction
from itertools import combinations, product
from functools import lru_cache

HALF = Fraction(1, 2)


def popcount(m):
    return bin(m).count("1")


def canon(n, m):
    return ((1 << n) - 1) ^ m if (m & 1) else m


def arc(n, start, size):
    m = 0
    for t in range(size):
        m |= 1 << ((start + t) % n)
    return m


def circular_splits(n):
    """all circular splits (canonical masks), trivial ones included"""
    out = set()
    for start in range(n):
        for size in range(1, n):
            out.add(canon(n, arc(n, start, size)))
    return out


def is_trivial(n, m):
    return popcount(m) in (1, n - 1)


def trivial_splits(n):
    return frozenset(canon(n, 1 << p) for p in range(n))


def nontrivial_circular_splits(n):
    return sorted(m for m in circular_splits(n) if not is_trivial(n, m))


def compatible(n, a, b):
    full = (1 << n) - 1
    na, nb = full ^ a, full ^ b
    return (a & b) == 0 or (a & nb) == 0 or (na & b) == 0 or (na & nb) == 0


@lru_cache(maxsize=None)
def binary_trees(n):
    """all binary trees on 0..n-1 whose splits are circular: maximal families (size n-3) of pairwise compatible
    non-trivial circular splits.  Returned as a tuple of frozensets of non-trivial splits."""
    S = nontrivial_circular_splits(n)
    need = n - 3
    if need <= 0:
        return (frozenset(),)
    comp = {s: {t for t in S if t != s and compatible(n, s, t)} for s in S}
    out = []

    def rec(chosen, cands):
        if len(chosen) == need:
            out.append(frozenset(chosen))
            return
        if len(chosen) + len(cands) < need:
            return
        for i, c in enumerate(cands):
            rec(chosen + [c], [x for x in cands[i + 1:] if x in comp[c]])

    rec([], S)
    return tuple(out)


@lru_cache(maxsize=None)
def tree_generated_systems(n):
    """all unions of split systems of binary circular trees (non-trivial parts), as frozensets; closure by BFS."""
    trees = binary_trees(n)
    seen = set(trees)
    frontier = list(trees)
    while frontier:
        new = []
        for s in frontier:
            for t in trees:
                u = s | t
                if u not in seen:
                    seen.add(u)
                    new.append(u)
        frontier = new
    return frozenset(seen)


def is_tree_generated(n, nontriv):
    """independent characterisation: every split of the set lies in a binary tree contained in the set"""
    nontriv = frozenset(nontriv)
    if not nontriv and n > 3:
        return False
    trees = [t for t in binary_trees(n) if t <= nontriv]
    cover = frozenset().union(*trees) if trees else frozenset()
    return cover == nontriv


def with_trivial(n, nontriv):
    return frozenset(nontriv) | trivial_splits(n)


# ----------------------------------------------------------------------------------------------
# displayed quartets, NANUQ metric, split weights
# ----------------------------------------------------------------------------------------------
def separates(m, s1, s2):
    return ((m & s1) == s1 and (m & s2) == 0) or ((m & s1) == 0 and (m & s2) == s2)


def displays(sigma, x, y, z, w):
    """some split of sigma separates {x,y} from {z,w}"""
    s1, s2 = (1 << x) | (1 << y), (1 << z) | (1 << w)
    return any(separates(m, s1, s2) for m in sigma)


def weight(sigma, x, y, z, w):
    """w(xy|zw) in {0,1/2,1}; xy|zw must be one of the two planar quartets of the 4 points."""
    pts = sorted((x, y, z, w))
    ix, iy = pts.index(x), pts.index(y)
    assert (ix - iy) % 4 in (1, 3), "non-planar quartet"
    # the other planar quartet pairs x with its other circular neighbour
    other_x = [p for p in pts if p not in (x, y) and (pts.index(p) - ix) % 4 in (1, 3)][0]
    other_y = [p for p in pts if p not in (x, y, other_x)][0]
    P = displays(sigma, x, y, z, w)
    Q = displays(sigma, x, other_x, y, other_y)
    if not (P or Q):
        raise ValueError("no displayed quartet")
    if P and Q:
        return HALF
    return Fraction(1) if P else Fraction(0)


def nanuq(n, sigma):
    """NANUQ metric of the split system (matrix of Fractions); None if some 4-set displays no quartet."""
    D = [[Fraction(0) if x == y else Fraction(2 * n - 4) for y in range(n)] for x in range(n)]
    for a, b, c, d in combinations(range(n), 4):
        P = displays(sigma, a, b, c, d)      # ab|cd
        Q = displays(sigma, a, d, b, c)      # ad|bc
        k = P + Q
        if k == 0:
            return None
        quartets = []
        if P:
            quartets.append(({a, b}, {c, d}))
        if Q:
            quartets.append(({a, d}, {b, c}))
        for x, y in combinations((a, b, c, d), 2):
            notcherry = sum(1 for (s, t) in quartets if {x, y} != s and {x, y} != t)
            val = 2 * Fraction(notcherry, k)
            D[x][y] += val
            D[y][x] += val
    return D


def alphas(n, D):
    """(i,j), i<j -> (alpha_ij, canonical mask of S_ij), U_ij = {i+1..j}"""
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            a = D[i][j] + D[(i + 1) % n][(j + 1) % n] - D[i][(j + 1) % n] - D[(i + 1) % n][j]
            m = 0
            for p in range(i + 1, j + 1):
                m |= 1 << p
            out[(i, j)] = (a, canon(n, m))
    return out


def check(n, sigma):
    """'ok' iff all alpha >= 0 and alpha > 0 exactly on sigma; else 'neg' / 'support' / 'invalid'."""
    D = nanuq(n, sigma)
    if D is None:
        return "invalid", None
    al = alphas(n, D)
    neg = {k: v[0] for k, v in al.items() if v[0] < 0}
    if neg:
        return "neg", neg
    bad = {k: v[0] for k, v in al.items() if (v[0] > 0) != (v[1] in sigma)}
    if bad:
        return "support", bad
    return "ok", None


# ----------------------------------------------------------------------------------------------
# local terms (Proposition 2 of the working paper)
# ----------------------------------------------------------------------------------------------
def Phi4(sigma, u1, up, v1, vq):
    return 2 * weight(sigma, u1, up, v1, vq)


def Phi5(sigma, u1, z, up, v1, vq):
    return (weight(sigma, u1, z, v1, vq) + weight(sigma, z, up, v1, vq)
            - weight(sigma, z, up, v1, u1) - weight(sigma, u1, z, up, vq))


def Phi6(sigma, u1, z, w, up, v1, vq):
    return (weight(sigma, z, w, v1, vq) + weight(sigma, z, w, u1, up)
            - weight(sigma, z, w, vq, up) - weight(sigma, z, w, u1, v1))


def Psi(sigma, a, u, b, z, w):
    return 1 - weight(sigma, a, u, z, w) - weight(sigma, u, b, z, w) + weight(sigma, a, b, z, w)


def alpha_from_local_terms(n, sigma, i, j):
    """alpha_ij / 2 according to Proposition 2, and the list of 6-point terms"""
    U = [(i + 1 + t) % n for t in range((j - i) % n)]
    V = [(j + 1 + t) % n for t in range(n - len(U))]
    if len(U) == 1 or len(V) == 1:
        if len(V) == 1:
            U, V = V, U
        u = U[0]
        b, a = V[0], V[-1]
        rest = V[1:-1]
        tot = Fraction(n - 2)
        for z, w in combinations(rest, 2):
            tot += Psi(sigma, a, u, b, z, w)
        return tot, []
    u1, up, v1, vq = U[0], U[-1], V[0], V[-1]
    tot = Phi4(sigma, u1, up, v1, vq)
    six = []
    for z in U[1:-1]:
        tot += Phi5(sigma, u1, z, up, v1, vq)
    for z in V[1:-1]:
        tot += Phi5(sigma, v1, z, vq, u1, up)
    for z, w in combinations(U[1:-1], 2):
        t = Phi6(sigma, u1, z, w, up, v1, vq)
        six.append(t)
        tot += t
    for z, w in combinations(V[1:-1], 2):
        t = Phi6(sigma, v1, z, w, vq, u1, up)
        six.append(t)
        tot += t
    return tot, six


def dihedral_labellings(pts):
    """the 2*len(pts) dihedral relabellings of a circularly ordered list"""
    k = len(pts)
    out = []
    for r in range(k):
        rot = [pts[(r + t) % k] for t in range(k)]
        out.append(rot)
        out.append([rot[0]] + rot[1:][::-1])
    return out


def six_locally_good_on(sigma, six_points):
    """the Phi6 condition for the six points (sorted in circular order), in all 12 dihedral labellings"""
    for y in dihedral_labellings(sorted(six_points)):
        v = Phi6(sigma, *y)
        if v < 0:
            return False
        if v != 0 and not displays(sigma, y[0], y[3], y[4], y[5]):
            return False
    return True


def six_locally_good(n, sigma):
    return all(six_locally_good_on(sigma, Y) for Y in combinations(range(n), 6))


def locally_nanuq_positive(n, sigma):
    """the hypothesis of Theorem 4, literally"""
    for i in range(n):
        for j in range(i + 1, n):
            U = [(i + 1 + t) % n for t in range((j - i) % n)]
            V = [(j + 1 + t) % n for t in range(n - len(U))]
            if len(U) < 2 or len(V) < 2:
                continue
            m = 0
            for p in U:
                m |= 1 << p
            insig = canon(n, m) in sigma
            for (A, B) in ((U, V), (V, U)):
                u1, up, v1, vq = A[0], A[-1], B[0], B[-1]
                for z, w in combinations(A[1:-1], 2):
                    t = Phi6(sigma, u1, z, w, up, v1, vq)
                    if t < 0 or (t != 0 and not insig):
                        return False
    return True


# ----------------------------------------------------------------------------------------------
# restriction, relabelling, dihedral images
# ----------------------------------------------------------------------------------------------
def restrict(n, sigma, Y):
    """restriction to the points Y (sorted), relabelled 0..|Y|-1 in the induced circular order"""
    Y = sorted(Y)
    k = len(Y)
    out = set()
    for m in sigma:
        r = 0
        for idx, p in enumerate(Y):
            if (m >> p) & 1:
                r |= 1 << idx
        if r != 0 and r != (1 << k) - 1:
            out.add(canon(k, r))
    return frozenset(out)


def relabel(n, sigma, perm):
    """perm[p] = new label of point p"""
    out = set()
    for m in sigma:
        r = 0
        for p in range(n):
            if (m >> p) & 1:
                r |= 1 << perm[p]
        out.add(canon(n, r))
    return frozenset(out)


def dihedral_images(n, sigma):
    out = set()
    for r in range(n):
        out.add(relabel(n, sigma, [(p + r) % n for p in range(n)]))
        out.add(relabel(n, sigma, [(r - p) % n for p in range(n)]))
    return out


def dihedral_canon(n, sigma):
    return min(tuple(sorted(s)) for s in dihedral_images(n, sigma))


# ----------------------------------------------------------------------------------------------
# class A (trees with twin leaves) and substitution
# ----------------------------------------------------------------------------------------------
def adjacent_pair_sets(N, k):
    """all sets of k pairwise disjoint pairs {p, p+1 mod N}; each as a tuple of first positions p"""
    out = []

    def rec(start, chosen, used):
        if len(chosen) == k:
            out.append(tuple(chosen))
            return
        for p in range(start, N):
            q = (p + 1) % N
            if p in used or q in used:
                continue
            rec(p + 1, chosen + [p], used | {p, q})

    rec(0, [], frozenset())
    return out


def leaf_labels(N, pairs):
    """position -> leaf index, leaves numbered in circular order; number of leaves"""
    second = {(p + 1) % N: p for p in pairs}
    lab = {}
    nxt = 0
    for pos in range(N):
        if pos in second and second[pos] < pos:
            lab[pos] = lab[second[pos]]
        else:
            lab[pos] = nxt
            nxt += 1
    if 0 in second:            # wrap-around pair {N-1, 0}: position N-1 is the same leaf as position 0
        nxt -= 1
        lab[N - 1] = lab[0]
    return lab, nxt


def A_system_bruteforce(N, tree, pairs):
    """split system of the A-structure by brute force over all 2^k choices (definition)"""
    lab, n = leaf_labels(N, pairs)
    full = (1 << n) - 1
    arcs = list(tree) + [1 << p for p in range(N)]
    out = set()
    for choice in product((0, 1), repeat=len(pairs)):
        deleted = {(p + c) % N for p, c in zip(pairs, choice)}
        for A in arcs:
            m = 0
            for pos in range(N):
                if (A >> pos) & 1 and pos not in deleted:
                    m |= 1 << lab[pos]
            m2 = 0
            for pos in range(N):
                if not (A >> pos) & 1 and pos not in deleted:
                    m2 |= 1 << lab[pos]
            assert m & m2 == 0 and m | m2 == full
            if m and m2:
                out.add(canon(n, m))
    return frozenset(out), n


def A_system(N, tree, pairs):
    """same, using that an arc cuts at most two twin pairs and the choices are independent"""
    lab, n = leaf_labels(N, pairs)
    full = (1 << n) - 1
    twin = {}
    for p in pairs:
        twin[p] = (p + 1) % N
        twin[(p + 1) % N] = p
    out = set()
    for A in list(tree) + [1 << p for p in range(N)]:
        base, free = 0, set()
        for pos in range(N):
            if (A >> pos) & 1:
                if pos in twin and not (A >> twin[pos]) & 1:
                    free.add(lab[pos])
                else:
                    base |= 1 << lab[pos]
            elif pos in twin and (A >> twin[pos]) & 1:
                free.add(lab[pos])
        free = sorted(free)
        for sub in product((0, 1), repeat=len(free)):
            m = base
            for f, s in zip(free, sub):
                if s:
                    m |= 1 << f
            if m != 0 and m != full:
                out.add(canon(n, m))
    return frozenset(out), n


@lru_cache(maxsize=None)
def A_class(n):
    """all A-systems on n leaves (full systems, trivial splits included)"""
    out = set()
    for k in range(0, n + 1):
        N = n + k
        if N < 3:
            continue
        pair_sets = adjacent_pair_sets(N, k)
        for tree in binary_trees(N):
            for pairs in pair_sets:
                s, nn = A_system(N, tree, pairs)
                assert nn == n
                out.add(s)
    return frozenset(out)


def substitute(n1, s1, p, n2, s2, r):
    """s1 o_{p,r} s2: leaf p of s1 is replaced by the leaves of s2 other than r, in the order following r."""
    n = n1 + n2 - 2
    full = (1 << n) - 1
    new1 = {}
    for q in range(n1):
        if q < p:
            new1[q] = q
        elif q > p:
            new1[q] = q + n2 - 2
    new2 = {}
    for t in range(1, n2):
        new2[(r + t) % n2] = p + t - 1
    block = 0
    for q in new2.values():
        block |= 1 << q
    rest = full ^ block
    out = set()
    for m in s1:
        mm = 0
        for q in range(n1):
            if (m >> q) & 1:
                mm |= block if q == p else (1 << new1[q])
        if mm != 0 and mm != full:
            out.add(canon(n, mm))
    for m in s2:
        mm = 0
        for q in range(n2):
            if (m >> q) & 1:
                mm |= rest if q == r else (1 << new2[q])
        if mm != 0 and mm != full:
            out.add(canon(n, mm))
    return frozenset(out)


@lru_cache(maxsize=None)
def C_class(n):
    """closure of the A-systems under substitution, restricted to n leaves (factors on >= 3 leaves)"""
    out = set(A_class(n))
    for n1 in range(3, n):
        n2 = n + 2 - n1
        if n2 < 3:
            continue
        for s1 in C_class(n1):
            for s2 in C_class(n2):
                for p in range(n1):
                    for r in range(n2):
                        out.add(substitute(n1, s1, p, n2, s2, r))
    return frozenset(out)
