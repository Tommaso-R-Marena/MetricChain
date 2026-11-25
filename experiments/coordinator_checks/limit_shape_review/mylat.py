#!/usr/bin/env python3
"""Assistant B — own diamond-lattice code, written from the 'Setting' paragraph of theory report §11.22
(not from the harness helpers ls_*, not from the reviewer's r2_lattice.py).

Lattice: sublattice A = integer points with all coordinates even and x+y+z = 0 mod 4; B = A + (1,1,1).
Bond vectors a0=(1,1,1), a1=(1,-1,-1), a2=(-1,1,-1), a3=(-1,-1,1): out of an A site +a_i, out of a B site -a_i.
Two lattice sites are bonded iff their squared distance is 3.
Walk: injective sequence of lattice sites, consecutive ones bonded.
Profile (cutoff S_c = 12): h_d = #{p<q : q-p >= 3, |x_q-x_p|^2 = d}, d in {3, 8, 11};  g = #{i : |x_{i+3}-x_i|^2 = 11}.
Bridge: first bead strictly lowest, last bead (weakly) highest in the coordinate y.
"""
import itertools
import numpy as np

A_VEC = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]


def is_site(p):
    x, y, z = int(p[0]), int(p[1]), int(p[2])
    if x % 2 == 0 and y % 2 == 0 and z % 2 == 0:
        return (x + y + z) % 4 == 0
    if x % 2 == 1 and y % 2 == 1 and z % 2 == 1:
        return (x + y + z - 3) % 4 == 0
    return False


def is_A(p):
    return int(p[0]) % 2 == 0


def sq(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def check_walk(w):
    """returns None if w is a self-avoiding lattice walk, else a string saying what fails"""
    if not all(is_site(p) for p in w):
        return "non-lattice site"
    if len(set(map(tuple, w))) != len(w):
        return "not injective"
    for i in range(len(w) - 1):
        if sq(w[i], w[i + 1]) != 3:
            return "consecutive beads %d,%d not bonded" % (i, i + 1)
    return None


def is_bridge(w):
    y0 = w[0][1]
    yl = w[-1][1]
    return all(p[1] > y0 for p in w[1:]) and all(p[1] <= yl for p in w)


def profile_bruteforce(w):
    """(h3, h8, h11, g) straight from the definition, O(N^2) over all pairs p < q with q - p >= 3"""
    n = len(w)
    h = {3: 0, 8: 0, 11: 0}
    for p in range(n):
        for q in range(p + 3, n):
            d = sq(w[p], w[q])
            if d in h:
                h[d] += 1
    g = 0
    for i in range(n - 3):
        d = sq(w[i], w[i + 3])
        assert d in (11, 19), "1-4 squared distance %d" % d
        g += (d == 11)
    return (h[3], h[8], h[11], g)


_DISP = None


def _disp():
    global _DISP
    if _DISP is None:
        _DISP = {}
        for d in (3, 8, 11):
            _DISP[d] = [v for v in itertools.product(range(-4, 5), repeat=3) if v[0] ** 2 + v[1] ** 2 + v[2] ** 2 == d]
    return _DISP


def profile_hash(w):
    """(h3, h8, h11, g) by looking up, for every bead, all integer displacements of squared norm 3, 8, 11"""
    idx = {}
    for i, p in enumerate(w):
        idx[(int(p[0]), int(p[1]), int(p[2]))] = i
    assert len(idx) == len(w), "not injective"
    D = _disp()
    h = []
    for d in (3, 8, 11):
        c = 0
        for i, p in enumerate(w):
            x, y, z = int(p[0]), int(p[1]), int(p[2])
            for v in D[d]:
                j = idx.get((x + v[0], y + v[1], z + v[2]))
                if j is not None and j - i >= 3:
                    c += 1
        h.append(c)
    g = 0
    for i in range(len(w) - 3):
        d = sq(w[i], w[i + 3])
        assert d in (11, 19)
        g += (d == 11)
    return (h[0], h[1], h[2], g)


def profile_kdtree(w):
    """(h3, h8, h11, g) with a k-d tree on the coordinates: all pairs within distance 3.4 (squared 11.56)"""
    from scipy.spatial import cKDTree
    X = np.asarray(w, dtype=np.int64)
    t = cKDTree(X.astype(float))
    pr = t.query_pairs(r=3.4, output_type="ndarray")
    i = np.minimum(pr[:, 0], pr[:, 1])
    j = np.maximum(pr[:, 0], pr[:, 1])
    d = ((X[i] - X[j]) ** 2).sum(1)
    far = (j - i) >= 3
    h = tuple(int(((d == dd) & far).sum()) for dd in (3, 8, 11))
    # chain neighbours: separation 1 -> 3, separation 2 -> 8
    assert int(((d == 3) & (j - i == 1)).sum()) == len(w) - 1
    assert int(((d == 8) & (j - i == 2)).sum()) == len(w) - 2
    assert set(np.unique(d).tolist()) <= {3, 8, 11}, np.unique(d)
    d14 = ((X[3:] - X[:-3]) ** 2).sum(1)
    assert set(np.unique(d14).tolist()) <= {11, 19}
    g = int((d14 == 11).sum())
    return (h[0], h[1], h[2], g)


def check_walk_np(w):
    """vectorised version of check_walk + is_bridge for long walks; returns (ok_walk, ok_bridge)"""
    X = np.asarray(w, dtype=np.int64)
    par = X % 2
    even = (par == 0).all(1)
    odd = (par == 1).all(1)
    s = X.sum(1)
    site = (even & (s % 4 == 0)) | (odd & ((s - 3) % 4 == 0))
    bonded = (((X[1:] - X[:-1]) ** 2).sum(1) == 3).all()
    inj = len(np.unique(X, axis=0)) == len(X)
    y = X[:, 1]
    bridge = bool((y[1:] > y[0]).all() and (y <= y[-1]).all())
    return bool(site.all() and bonded and inj), bridge


def cnorm(d):
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])


def helix(nbeads):
    """bond indices 0,1,2,3,0,1,...: out of an A site +a_i, out of a B site -a_i"""
    w = [(0, 0, 0)]
    for k in range(nbeads - 1):
        a = A_VEC[k % 4]
        s = 1 if is_A(w[-1]) else -1
        w.append((w[-1][0] + s * a[0], w[-1][1] + s * a[1], w[-1][2] + s * a[2]))
    return w


def nbrs(p):
    s = 1 if is_A(p) else -1
    return [(p[0] + s * a[0], p[1] + s * a[1], p[2] + s * a[2]) for a in A_VEC]


def enum_bridges(nbeads):
    """all bridges with nbeads beads starting at the origin (an A site); generator of lists"""
    w = [(0, 0, 0)]
    occ = {(0, 0, 0)}

    def rec():
        if len(w) == nbeads:
            if all(p[1] <= w[-1][1] for p in w):
                yield list(w)
            return
        for q in nbrs(w[-1]):
            if q in occ or q[1] <= 0:
                continue
            occ.add(q)
            w.append(q)
            yield from rec()
            occ.discard(q)
            w.pop()

    yield from rec()
