"""
NANUQ metric of a circular split system (exact rational arithmetic).

Points 0..n-1 are in circular order.  Gap g lies between point g and point g+1 (mod n).
The circular split S_{ij} (i != j gaps) is U|V with U = {i+1,...,j} (cyclically).

For a set Sigma of circular splits, the 4-set {a,b,c,d} (in circular order a,b,c,d)
"displays" ab|cd iff some split of Sigma separates {a,b} from {c,d}, and ad|bc iff some
split separates {a,d} from {b,c}.  (ac|bd is never displayed by a circular system.)

rho_xy(q) = average over the displayed quartets t of q of [x,y is not a cherry of t].
d(x,y)   = sum_{ {z,w} } 2*rho_xy({x,y,z,w}) + 2n - 4          (x != y),  d(x,x) = 0.
alpha_ij = d(x_i,x_j) + d(x_{i+1},x_{j+1}) - d(x_i,x_{j+1}) - d(x_{i+1},x_j).

All values of 2*d are integers; we return 2*d and 2*alpha as Python ints.
"""
from itertools import combinations


def split_mask(n, i, j):
    """bitmask of U = {i+1,...,j} cyclically (i != j)."""
    m = 0
    k = (i + 1) % n
    while True:
        m |= 1 << k
        if k == j:
            break
        k = (k + 1) % n
    return m


def canon(n, m):
    """canonical mask of a split: the side not containing point 0."""
    full = (1 << n) - 1
    return m if not (m & 1) else full ^ m


def all_circular_splits(n):
    """dict: canonical mask -> (i,j) with i<j (gaps)."""
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            out[canon(n, split_mask(n, i, j))] = (i, j)
    return out


def is_trivial(n, m):
    c = bin(m).count("1")
    return c == 1 or c == n - 1


def separates(m, s1, s2):
    """split with canonical mask m separates point set mask s1 from s2."""
    return ((m & s1) == s1 and (m & s2) == 0) or ((m & s1) == 0 and (m & s2) == s2)


def quartet_table(n, sigma):
    """For every 4-set (a<b<c<d): (P, Q) with P = [ab|cd displayed], Q = [ad|bc displayed]."""
    tab = {}
    for a, b, c, d in combinations(range(n), 4):
        ab, cd = (1 << a) | (1 << b), (1 << c) | (1 << d)
        ad, bc = (1 << a) | (1 << d), (1 << b) | (1 << c)
        P = any(separates(m, ab, cd) for m in sigma)
        Q = any(separates(m, ad, bc) for m in sigma)
        tab[(a, b, c, d)] = (P, Q)
    return tab


def nanuq_2d(n, sigma, tab=None):
    """returns matrix of 2*d (ints) or None if some 4-set displays no quartet."""
    if tab is None:
        tab = quartet_table(n, sigma)
    D = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(x + 1, n):
            D[x][y] = D[y][x] = 2 * (2 * n - 4)
    for (a, b, c, d), (P, Q) in tab.items():
        if not (P or Q):
            return None
        # 4*rho for each pair
        # ab|cd: cherries ab, cd -> rho=0 for them, 1 for others
        # ad|bc: cherries ad, bc
        k = P + Q
        def add(x, y, val4):  # val4 = 4*rho_xy ; 2*d gets 2*2*rho = val4
            D[x][y] += val4
            D[y][x] += val4
        # pairs: ab, cd, ad, bc, ac, bd
        rho_ab = (0 if P else 0) + (1 if Q else 0)   # number of displayed quartets where ab is NOT a cherry
        rho_ad = (1 if P else 0) + (0 if Q else 0)
        add(a, b, 4 * rho_ab // k)
        add(c, d, 4 * rho_ab // k)
        add(a, d, 4 * rho_ad // k)
        add(b, c, 4 * rho_ad // k)
        add(a, c, 4)
        add(b, d, 4)
    return D


def alphas_2(n, D):
    """dict (i,j) i<j gaps -> 2*alpha_ij computed from 2*d."""
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            xi, xi1, xj, xj1 = i, (i + 1) % n, j, (j + 1) % n
            out[(i, j)] = D[xi][xj] + D[xi1][xj1] - D[xi][xj1] - D[xi1][xj]
    return out


def check(n, sigma):
    """returns (status, detail).  status in {'invalid','ok','neg','support'}"""
    D = nanuq_2d(n, sigma)
    if D is None:
        return "invalid", None
    al = alphas_2(n, D)
    neg = {k: v for k, v in al.items() if v < 0}
    if neg:
        return "neg", neg
    bad = {}
    for (i, j), v in al.items():
        m = canon(n, split_mask(n, i, j))
        if (v > 0) != (m in sigma):
            bad[(i, j)] = v
    if bad:
        return "support", bad
    return "ok", None
