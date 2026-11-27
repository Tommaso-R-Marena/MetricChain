#!/usr/bin/env python3
"""R9 — own diamond-lattice module in Python (written from the Setting paragraph of theory report §11.22 and the statement
of Lemma 11.68; independent of r9_semi.c only in language — same author — and independent of the theory division's
mylat.py / concat_check.py and of R2's code, none of which is imported).

Lattice: A = {(x,y,z) all even, x+y+z = 0 mod 4}, B = A + (1,1,1); bonds +a_i out of A sites, -a_i out of B sites,
a0=(1,1,1), a1=(1,-1,-1), a2=(-1,1,-1), a3=(-1,-1,1).  Height = y.
"""
import itertools, random

AV = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
DISP = {d: [v for v in itertools.product(range(-3, 4), repeat=3) if v[0] ** 2 + v[1] ** 2 + v[2] ** 2 == d] for d in (3, 8, 11)}


def is_site(p):
    x, y, z = p
    if x % 2 == 0 and y % 2 == 0 and z % 2 == 0:
        return (x + y + z) % 4 == 0
    if x % 2 == 1 and y % 2 == 1 and z % 2 == 1:
        return (x + y + z - 3) % 4 == 0
    return False


def is_A(p):
    return p[0] % 2 == 0


def add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])


def sq(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def nbrs(p):
    s = 1 if is_A(p) else -1
    return [(p[0] + s * a[0], p[1] + s * a[1], p[2] + s * a[2]) for a in AV]


def check_walk(w):
    if not all(is_site(p) for p in w):
        return "non-lattice site"
    if len(set(w)) != len(w):
        return "not injective"
    for i in range(len(w) - 1):
        if sq(w[i], w[i + 1]) != 3:
            return "beads %d, %d not bonded" % (i, i + 1)
    return None


def is_bridge(w):
    y0, yl = w[0][1], w[-1][1]
    return all(p[1] > y0 for p in w[1:]) and all(p[1] <= yl for p in w)


def profile(w):
    """(h3, h8, h11, g) from the definition, by dictionary look-ups"""
    idx = {p: i for i, p in enumerate(w)}
    assert len(idx) == len(w)
    h = [0, 0, 0]
    for q, p in enumerate(w):
        for t, d in enumerate((3, 8, 11)):
            for v in DISP[d]:
                j = idx.get((p[0] + v[0], p[1] + v[1], p[2] + v[2]))
                if j is not None and q - j >= 3:
                    h[t] += 1
    g = 0
    for i in range(len(w) - 3):
        d = sq(w[i], w[i + 3])
        assert d in (11, 19), d
        g += d == 11
    return (h[0], h[1], h[2], g)


def profile_brute(w):
    h = {3: 0, 8: 0, 11: 0}
    n = len(w)
    for p in range(n):
        for q in range(p + 3, n):
            d = sq(w[p], w[q])
            if d in h:
                h[d] += 1
    g = sum(1 for i in range(n - 3) if sq(w[i], w[i + 3]) == 11)
    return (h[3], h[8], h[11], g)


def admissible_c1(w):
    """b' if it is an up-bond, else the two up-bonds out of the last bead"""
    bp = sub(w[-2], w[-3])
    if bp[1] == 1:
        return [bp]
    P = w[-1]
    return [sub(q, P) for q in nbrs(P) if q[1] > P[1]]


def top_sites(w, c1, k=3):
    b = sub(w[-1], w[-2])
    out = []
    p = w[-1]
    for j in range(1, k + 1):
        p = add(p, c1 if j % 2 == 1 else b)
        out.append(p)
    return out


def bottom_sites(w, k=3):
    """s_1 = x_0 - u2, s_2 = s_1 - u1, s_3 = s_2 - u2, ...  (beads -1, -2, -3, ...)"""
    u1, u2 = sub(w[1], w[0]), sub(w[2], w[1])
    out = []
    p = w[0]
    for j in range(1, k + 1):
        p = sub(p, u2 if j % 2 == 1 else u1)
        out.append(p)
    return out


def _extra(idx, site, vi):
    c = [0, 0, 0]
    for t, d in enumerate((3, 8, 11)):
        for v in DISP[d]:
            j = idx.get((site[0] + v[0], site[1] + v[1], site[2] + v[2]))
            if j is not None and abs(vi - j) >= 3:
                c[t] += 1
    return c


def A_part(w, c1, idx=None):
    """(extra pairs of the three linker sites above the bridge at distances 3, 8, 11; [b' is a down-bond])"""
    if idx is None:
        idx = {p: i for i, p in enumerate(w)}
    n = len(w)
    c = [0, 0, 0]
    for j, s in enumerate(top_sites(w, c1, 3), start=1):
        assert s not in idx
        e = _extra(idx, s, n - 1 + j)
        c = [c[i] + e[i] for i in range(3)]
    return (c[0], c[1], c[2], 0 if sub(w[-2], w[-3])[1] == 1 else 1)


def B_part(w, idx=None):
    if idx is None:
        idx = {p: i for i, p in enumerate(w)}
    c = [0, 0, 0]
    for j, s in enumerate(bottom_sites(w, 3), start=1):
        assert s not in idx
        e = _extra(idx, s, -j)
        c = [c[i] + e[i] for i in range(3)]
    return (c[0], c[1], c[2], 0)


def is_clean(w):
    idx = {p: i for i, p in enumerate(w)}
    cs = admissible_c1(w)
    return sub(w[-2], w[-3])[1] == 1 and A_part(w, cs[0], idx) == (0, 0, 0, 0) and B_part(w, idx) == (0, 0, 0, 0)


def _gact(gi, v):
    sw, s1, s2 = gi & 1, (-1 if gi & 2 else 1), (-1 if gi & 4 else 1)
    return (s1 * v[0], v[1], s2 * v[2]) if not sw else (s1 * v[2], v[1], s2 * v[0])


def concat(x1, x2, c1):
    """the concatenation of Lemma 11.68: x1, three linker sites, phi(x2); returns (walk, index of the symmetry)"""
    b = sub(x1[-1], x1[-2])
    link = top_sites(x1, c1, 3)
    Q = add(link[2], b)
    u1, u2 = sub(x2[1], x2[0]), sub(x2[2], x2[1])
    gs = [g for g in range(8) if _gact(g, u1) == c1 and _gact(g, u2) == b]
    assert len(gs) == 1, gs
    g = gs[0]
    img = [add(Q, _gact(g, sub(p, x2[0]))) for p in x2]
    return list(x1) + link + img, g


def extend(w, c1, kh, kt):
    head = bottom_sites(w, kh)[::-1]
    tail = top_sites(w, c1, kt)
    return head + list(w) + tail


def rod(n):
    w = [(0, 0, 0)]
    ups = [(1, 1, 1), (-1, 1, 1)]
    for k in range(n - 1):
        w.append(add(w[-1], ups[k % 2]))
    return w


def helix(n):
    """bond indices 0,1,2,3,0,...; out of an A site +a_i, out of a B site -a_i (every bond an up-bond)"""
    w = [(0, 0, 0)]
    for k in range(n - 1):
        a = AV[k % 4]
        s = 1 if is_A(w[-1]) else -1
        w.append((w[-1][0] + s * a[0], w[-1][1] + s * a[1], w[-1][2] + s * a[2]))
    return w


def enum_bridges(n):
    """all bridges with n beads whose first two bonds are +a0, -a1 (generator)"""
    w = [(0, 0, 0), (1, 1, 1), (0, 2, 2)]
    occ = set(w)

    def rec(maxy):
        if len(w) == n:
            if w[-1][1] >= maxy:
                yield list(w)
            return
        if w[-1][1] + (n - len(w)) < maxy:
            return
        for q in nbrs(w[-1]):
            if q in occ or q[1] <= 0:
                continue
            occ.add(q); w.append(q)
            yield from rec(max(maxy, q[1]))
            occ.discard(q); w.pop()
    if n >= 3:
        yield from rec(2)


def random_compact_walk(n, rng, beta=1.5, drift=0.0):
    """growth walk: the next site is chosen among the free neighbours with weight exp(beta * #occupied sites within squared
    distance 8 + drift * dy); stops when trapped.  Not uniform — only a source of walks with dense surroundings."""
    w = [(0, 0, 0)]
    occ = {(0, 0, 0)}
    near = DISP[3] + DISP[8]
    while len(w) < n:
        cand = [q for q in nbrs(w[-1]) if q not in occ]
        if not cand:
            break
        ws = []
        for q in cand:
            c = sum(1 for v in near if (q[0] + v[0], q[1] + v[1], q[2] + v[2]) in occ)
            ws.append(pow(2.718281828, beta * c + drift * (q[1] - w[-1][1])))
        r = rng.random() * sum(ws)
        for q, wt in zip(cand, ws):
            r -= wt
            if r <= 0:
                break
        w.append(q); occ.add(q)
    return w


def bridge_of(w, minlen=3):
    """the sub-walk from the last minimum of the height to the last maximum after it (a bridge if it has >= 3 beads)"""
    ys = [p[1] for p in w]
    m = min(ys)
    i = max(k for k, y in enumerate(ys) if y == m)
    M = max(ys[i:])
    j = max(k for k in range(i, len(w)) if ys[k] == M)
    seg = w[i:j + 1]
    if len(seg) < minlen or not is_bridge(seg):
        return None
    return seg
