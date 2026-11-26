"""The parametric family of quartet distances of Allman-Banos-Rhodes-Wicke (NANUQ+, 2025, Def. 3.1),
   rho = (rho_c, rho_s, rho_a, rho_o):
       quarnet tree-like, x,y a cherry        -> rho_c
       quarnet tree-like, x,y separated       -> rho_s
       quarnet cyclic,    x,y adjacent        -> rho_a
       quarnet cyclic,    x,y opposite        -> rho_o
   d_rho(x,y) = 2 * sum_{z,w} rho_xy + 2n - 4.          NANUQ is (0, 1, 1/2, 1).
extended to circular split systems ("cyclic" = both planar quartets displayed).

All split weights alpha_ij are affine-linear forms in (c, s, a, o); we collect, over all systems of the class
on n leaves, the forms that must be > 0 (displayed splits), = 0 (undisplayed splits)."""
import sys
from itertools import combinations
from fractions import Fraction
from splitsys import *
from twin_trees import closure_systems

def vec(c=0, s=0, a=0, o=0, k=0):
    return (c, s, a, o, k)

def add(u, v, sign=1):
    return tuple(x + sign * y for x, y in zip(u, v))

def param_d(n, sigma):
    """matrix of vectors: d(x,y) as (coef_c, coef_s, coef_a, coef_o, const)"""
    D = [[vec() for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(x + 1, n):
            D[x][y] = D[y][x] = vec(k=2 * n - 4)
    for a, b, c, d in combinations(range(n), 4):
        ab, cd = (1 << a) | (1 << b), (1 << c) | (1 << d)
        ad, bc = (1 << a) | (1 << d), (1 << b) | (1 << c)
        P = any(separates(m, ab, cd) for m in sigma)
        Q = any(separates(m, ad, bc) for m in sigma)
        assert P or Q
        def put(x, y, v):
            D[x][y] = add(D[x][y], v)
            D[y][x] = D[x][y]
        if P and Q:
            for x, y in ((a, b), (c, d), (a, d), (b, c)):
                put(x, y, vec(a=2))
            for x, y in ((a, c), (b, d)):
                put(x, y, vec(o=2))
        else:
            cher = ((a, b), (c, d)) if P else ((a, d), (b, c))
            for x, y in combinations((a, b, c, d), 2):
                put(x, y, vec(c=2) if (x, y) in cher else vec(s=2))
    return D

def param_alphas(n, D):
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            xi, xi1, xj, xj1 = i, (i + 1) % n, j, (j + 1) % n
            v = add(add(D[xi][xj], D[xi1][xj1]), add(D[xi][xj1], D[xi1][xj]), -1)
            out[(i, j)] = v
    return out

def normalise(v):
    from math import gcd
    g = 0
    for x in v:
        g = gcd(g, abs(x))
    if g == 0:
        return v
    return tuple(x // g for x in v)

def collect(n):
    pos, zero = set(), set()
    for s in closure_systems(n):
        D = param_d(n, set(s))
        al = param_alphas(n, D)
        for (i, j), v in al.items():
            m = canon(n, split_mask(n, i, j))
            if m in s:
                pos.add(normalise(v))
            else:
                zero.add(normalise(v))
    return pos, zero

if __name__ == "__main__":
    allpos, allzero = set(), set()
    for n in map(int, sys.argv[1:]):
        pos, zero = collect(n)
        allpos |= pos; allzero |= zero
        print(f"n={n}: forms that must vanish (undisplayed splits): {sorted(zero)}")
        print(f"       number of distinct forms that must be positive: {len(pos)}")
    print("all vanishing forms (c,s,a,o,const):", sorted(allzero))
    # evaluate at NANUQ
    def ev(v, r): return v[0]*r[0] + v[1]*r[1] + v[2]*r[2] + v[3]*r[3] + v[4]
    r0 = (0, 1, Fraction(1, 2), 1)
    print("NANUQ satisfies all:", all(ev(v, r0) > 0 for v in allpos) and all(ev(v, r0) == 0 for v in allzero))
    import pickle
    pickle.dump((allpos, allzero), open("/tmp/param_forms.pkl", "wb"))
