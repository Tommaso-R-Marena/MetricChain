"""Coordinator's own diamond-lattice helpers for the spot checks of workstream S (written independently of ws/S/code/lat.py)."""
import itertools

BV = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]          # a_0..a_3
DISP = {d: [v for v in itertools.product(range(-3, 4), repeat=3) if v[0] ** 2 + v[1] ** 2 + v[2] ** 2 == d]
        for d in (3, 8, 11)}


def is_a(p):
    return p[0] % 2 == 0 and p[1] % 2 == 0 and p[2] % 2 == 0 and (p[0] + p[1] + p[2]) % 4 == 0


def is_b(p):
    return is_a((p[0] - 1, p[1] - 1, p[2] - 1))


def nbrs(p):
    s = 1 if is_a(p) else -1
    return [(p[0] + s * a[0], p[1] + s * a[1], p[2] + s * a[2]) for a in BV]


def sq(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2


def valid_walk(w):
    if len(set(w)) != len(w):
        return False
    for p in w:
        if not (is_a(p) or is_b(p)):
            return False
    return all(w[i + 1] in nbrs(w[i]) for i in range(len(w) - 1))


def profile(w):
    """(h3, h8, h11, gauche) straight from the definition: pairs p<q with q-p>=3 at squared distance 3, 8, 11;
    gauche torsions = index triples with |x_{i+3}-x_i|^2 = 11 (trans: 19)."""
    idx = {p: i for i, p in enumerate(w)}
    assert len(idx) == len(w)
    h = [0, 0, 0]
    for i, p in enumerate(w):
        for k, d in enumerate((3, 8, 11)):
            for v in DISP[d]:
                j = idx.get((p[0] + v[0], p[1] + v[1], p[2] + v[2]))
                if j is not None and j - i >= 3:
                    h[k] += 1
    g = 0
    for i in range(len(w) - 3):
        s = sq(w[i], w[i + 3])
        assert s in (11, 19)
        g += (s == 11)
    return (h[0], h[1], h[2], g)


def is_bridge(w):
    y0 = w[0][1]
    yl = w[-1][1]
    return all(p[1] > y0 for p in w[1:]) and all(p[1] <= yl for p in w)


def cnorm(d):
    """L1 norm of the cumulative profile difference: 5|d3| + 3|d3+d8| + |d3+d8+d11|"""
    return 5 * abs(d[0]) + 3 * abs(d[0] + d[1]) + abs(d[0] + d[1] + d[2])


def wnorm(d):
    return 9 * abs(d[0]) + 4 * abs(d[1]) + abs(d[2])


def enum_walks(nbeads, bridge=False):
    """all self-avoiding walks with nbeads beads from the origin (A site) with a fixed first bond (+a_0);
    yields lists of sites.  With bridge=True all bridges starting at the origin are produced instead
    (both up-bonds as first bond)."""
    start = (0, 0, 0)
    out = []
    w = [start]
    occ = {start}

    def rec():
        if len(w) == nbeads:
            if (not bridge) or all(p[1] <= w[-1][1] for p in w):
                out.append(list(w))
            return
        for q in nbrs(w[-1]):
            if q in occ:
                continue
            if bridge and q[1] <= 0:
                continue
            if (not bridge) and len(w) == 1 and q != (1, 1, 1):
                continue
            occ.add(q)
            w.append(q)
            rec()
            occ.discard(q)
            w.pop()

    rec()
    return out
