"""Diamond-lattice helpers shared by the workstream-S scripts."""
import itertools

A = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
DISP = {d: [v for v in itertools.product(range(-3, 4), repeat=3) if sum(c * c for c in v) == d] for d in (3, 8, 11)}

def is_A(p):
    return p[0] % 2 == 0 and p[1] % 2 == 0 and p[2] % 2 == 0 and (p[0] + p[1] + p[2]) % 4 == 0

def is_B(p):
    return is_A((p[0] - 1, p[1] - 1, p[2] - 1))

def is_site(p):
    return is_A(p) or is_B(p)

def nbrs(p):
    """the four lattice neighbours of site p"""
    s = 1 if is_A(p) else -1
    return [(p[0] + s * a[0], p[1] + s * a[1], p[2] + s * a[2]) for a in A]

def add(p, q):
    return (p[0] + q[0], p[1] + q[1], p[2] + q[2])

def sub(p, q):
    return (p[0] - q[0], p[1] - q[1], p[2] - q[2])

def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2

def is_walk(pos):
    """valid self-avoiding lattice walk?"""
    if len(set(pos)) != len(pos):
        return False
    if not all(is_site(p) for p in pos):
        return False
    return all(d2(pos[i], pos[i + 1]) == 3 for i in range(len(pos) - 1))

def profile(pos):
    """(h3, h8, h11, gauche) of a walk given as a list of sites, computed from the site set (Lemma G1)."""
    S = set(pos)
    N = len(pos)
    e = []
    for d in (3, 8, 11):
        c = 0
        for p in pos:
            for v in DISP[d]:
                if add(p, v) in S:
                    c += 1
        e.append(c // 2)
    g = sum(1 for i in range(N - 3) if d2(pos[i], pos[i + 3]) == 11)
    return (e[0] - (N - 1), e[1] - (N - 2) if N >= 2 else 0, e[2], g)

def profile_def(pos):
    """the same from the definition (pairs with q-p >= 3)"""
    N = len(pos)
    h = [0, 0, 0]
    for p in range(N):
        for q in range(p + 3, N):
            s = d2(pos[p], pos[q])
            if s == 3: h[0] += 1
            elif s == 8: h[1] += 1
            elif s == 11: h[2] += 1
    g = sum(1 for i in range(N - 3) if d2(pos[i], pos[i + 3]) == 11)
    return (h[0], h[1], h[2], g)

def is_bridge(pos):
    y0 = pos[0][1]
    return all(p[1] > y0 for p in pos[1:]) and all(p[1] <= pos[-1][1] for p in pos)

def bridges(N, start=(0, 0, 0)):
    """all y-bridges with N beads starting at `start` (an A or B site), as lists of sites"""
    out = []
    pos = [start]
    occ = {start}
    y0 = start[1]
    def rec():
        if len(pos) == N:
            if all(p[1] <= pos[-1][1] for p in pos):
                out.append(list(pos))
            return
        for q in nbrs(pos[-1]):
            if q in occ or q[1] <= y0:
                continue
            occ.add(q); pos.append(q)
            rec()
            occ.discard(q); pos.pop()
    rec()
    return out

# the eight linear maps that preserve y and the lattice up to a translation: (x,z) -> (+-x,+-z) or (+-z,+-x)
YMAPS = []
for sx in (1, -1):
    for sz in (1, -1):
        YMAPS.append(lambda v, sx=sx, sz=sz: (sx * v[0], v[1], sz * v[2]))
        YMAPS.append(lambda v, sx=sx, sz=sz: (sx * v[2], v[1], sz * v[0]))
