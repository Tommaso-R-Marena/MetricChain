"""V9 -- second, independent implementation (Python) of the objects of Theorem R9.1.

Written from the Setting paragraph of THEORY_REPORT 11.22 and the definitions of R9_REPORT 4.1; nothing of the
reviewed division's code was read.  From OUR repository only `mylat.py` is used (lattice sites, neighbours,
enumeration of bridges, the two profile counts) -- read-only, bytecode writing off.

Counting method here: dictionary look-up of all integer displacements of squared norm 3, 8, 11 around a site, with the
chain separation taken from explicit bead indices (t_j = beads n, n+1, n+2;  s_j = beads -1, -2, -3).
The C program v9_cobound.c counts the same things by plain double loops over pairs of beads.
"""
import sys, os, itertools
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))   # mylat.py of the parent directory
import mylat as ML

DISP = {d: [v for v in itertools.product(range(-3, 4), repeat=3) if v[0] ** 2 + v[1] ** 2 + v[2] ** 2 == d] for d in (3, 8, 11)}
SIGNED = [(perm, sg) for perm in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3)]


def act(g, v):
    perm, sg = g
    return (sg[0] * v[perm[0]], sg[1] * v[perm[1]], sg[2] * v[perm[2]])


# symmetries that preserve heights: linear part fixes e_y
HP = [g for g in SIGNED if act(g, (0, 1, 0)) == (0, 1, 0)]
assert len(HP) == 8
# the same set, defined as "preserves the order of heights" (image of e_y has positive y-component)
assert sorted(HP) == sorted(g for g in SIGNED if act(g, (0, 1, 0))[1] == 1)


def add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def up_bonds(p):
    return [sub(q, p) for q in ML.nbrs(p) if q[1] == p[1] + 1]


def index_of(x):
    idx = {}
    for i, p in enumerate(x):
        idx[p] = i
    assert len(idx) == len(x), "not injective"
    return idx


def admissible(x):
    bp = sub(x[-2], x[-3])
    if bp[1] == 1:
        return [bp]
    assert bp[1] == -1
    ub = up_bonds(x[-1])
    assert len(ub) == 2
    return ub


def sites_above(x, c1, k=3):
    b = sub(x[-1], x[-2])
    out = []
    p = x[-1]
    for j in range(k):
        p = add(p, c1 if j % 2 == 0 else b)
        out.append(p)
    return out


def sites_below(x, k=3):
    u1 = sub(x[1], x[0])
    u2 = sub(x[2], x[1])
    out = []
    p = x[0]
    for j in range(k):
        p = sub(p, u2 if j % 2 == 0 else u1)
        out.append(p)
    return out


def end_counts(sites, bead_numbers, idx):
    c = [0, 0, 0]
    for s, bn in zip(sites, bead_numbers):
        for t, d in enumerate((3, 8, 11)):
            for v in DISP[d]:
                j = idx.get((s[0] + v[0], s[1] + v[1], s[2] + v[2]))
                if j is not None and abs(bn - j) >= 3:
                    c[t] += 1
    return c


def A_of(x, c1, idx=None):
    idx = idx if idx is not None else index_of(x)
    n = len(x)
    c = end_counts(sites_above(x, c1), [n, n + 1, n + 2], idx)
    return (c[0], c[1], c[2], int(sub(x[-2], x[-3])[1] == -1))


def B_of(x, idx=None):
    idx = idx if idx is not None else index_of(x)
    c = end_counts(sites_below(x), [-1, -2, -3], idx)
    return (c[0], c[1], c[2], 0)


def is_clean(x, idx=None):
    idx = idx if idx is not None else index_of(x)
    bp = sub(x[-2], x[-3])
    if bp[1] != 1:
        return False
    return A_of(x, bp, idx) == (0, 0, 0, 0) and B_of(x, idx) == (0, 0, 0, 0)


def concat(x1, c1, x2):
    """x1, t1, t2, t3, phi(x2); returns the walk and the linear part of phi (unique: asserted)"""
    b = sub(x1[-1], x1[-2])
    t = sites_above(x1, c1)
    Q = add(t[2], b)
    u1 = sub(x2[1], x2[0])
    u2 = sub(x2[2], x2[1])
    gs = [g for g in HP if act(g, u1) == c1 and act(g, u2) == b]
    assert len(gs) == 1, "the height-preserving symmetry is not unique"
    g = gs[0]
    return x1 + t + [add(Q, act(g, sub(p, x2[0]))) for p in x2], g


def extend(x, c1, k, m):
    """zigzag head of k beads and zigzag tail of m beads"""
    return sites_below(x, k)[::-1] + list(x) + sites_above(x, c1, m)


def vadd(*vs):
    return tuple(sum(v[i] for v in vs) for i in range(len(vs[0])))


def nrm(d):
    """||(d3,d8,d11)||_c + |dg| for an arbitrary integer vector"""
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2]) + abs(d[3])


def check_bridge(x):
    assert ML.check_walk(x) is None, ML.check_walk(x)
    assert ML.is_bridge(x), "not a bridge"


def check_concat_identities(x1, c1, x2, hg=ML.profile_hash, cache=None):
    """all identities of R9.1(a) for one concatenation, from coordinates.  returns (y, error vector, number of c1'')"""
    def HG(x):
        if cache is None:
            return hg(x)
        k = tuple(x)
        if k not in cache:
            cache[k] = hg(x)
        return cache[k]
    y, g = concat(x1, c1, x2)
    assert len(y) == len(x1) + len(x2) + 3
    check_bridge(y)
    i1, i2, iy = index_of(x1), index_of(x2), index_of(y)
    hy, h1, h2 = hg(y), HG(x1), HG(x2)
    A1 = A_of(x1, c1, i1)
    B1 = B_of(x1, i1)
    B2 = B_of(x2, i2)
    err = tuple(hy[k] - h1[k] - h2[k] for k in range(4))
    assert err == vadd(A1, B2), ("first line of (a) fails", err, A1, B2)
    By = B_of(y, iy)
    assert By == B1, ("B(x1 o x2) != B(x1)", By, B1)
    ad2 = admissible(x2)
    ady = admissible(y)
    assert sorted(ady) == sorted(act(g, c) for c in ad2), "admissible bonds of the concatenation are not the images of those of x2"
    for c in ad2:
        A2 = A_of(x2, c, i2)
        Ay = A_of(y, act(g, c), iy)
        assert Ay == A2, ("A(x1 o x2, phi(c)) != A(x2, c)", Ay, A2)
        assert vadd(hy, Ay, By) == vadd(h1, A1, B1, h2, A2, B2), "q-hat not additive"
    c1ok = is_clean(x1, i1)
    c2ok = is_clean(x2, i2)
    cy = is_clean(y, iy)
    assert cy == (B1 == (0, 0, 0, 0) and len(ad2) == 1 and A_of(x2, ad2[0], i2) == (0, 0, 0, 0))
    if c1ok and c2ok:
        assert err == (0, 0, 0, 0) and cy
    return y, err, len(ad2), (c1ok and c2ok)
