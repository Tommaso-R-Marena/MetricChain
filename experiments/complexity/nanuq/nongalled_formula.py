"""Exact weight of the split {x,y} | rest in the non-galled family N(s,t)  (Theorem 9(c) of
docs/complexity/NANUQ_LOCAL_CRITERION.md; formulas pointed out by the referee, COMPLEXITY-REV-0002 finding 9).

Two versions of the family, both given by their four displayed trees (choice of the parent of h1, of h2):

  bloblet version   the t leaves a_i and the s leaves d_j hang along the cycle (N* is s = 1, t = 2):
       T1 = ( Acat((b,(x,y))), Dcat(c) )          T2 = ( Acat((b,x)), Dcat((y,c)) )
       T3 = ( Acat(b), Dcat(((x,y),c)) )          T4 = ( Acat(b), Dcat((x,(y,c))) )
     with Acat(X) = (((X,a_t),a_{t-1}),...,a_1),  Dcat(X) = (((X,d_1),d_2),...,d_s);
  clade version     the a_i form one pendant clade A and the d_j one pendant clade D:
       T1 = ((A,(b,(x,y))),(c,D))   T2 = ((A,(b,x)),((y,c),D))   T3 = ((A,b),(((x,y),c),D))   T4 = ((A,b),((x,(y,c)),D)).

Circular order: a_1..a_t, b, x, y, c, d_1..d_s.  The split U|V = {x,y} | rest has U = (x,y), V = (c, d_1..d_s,
a_1..a_t, b), so by Proposition 2
       alpha/2 = Phi4 + sum_z Phi5'(z) + sum_{z<w} Phi6'(z,w),        z, w in {d_j} + {a_i},
and every term depends only on the restriction of the split system to x, y, c, b and the one or two leaves
z, w -- which is the split system of the family member with only those leaves (restrict the four trees).
So there are six numbers to compute (on 4, 5, 5, 6, 6, 6 leaves), and
       alpha/2 = Phi4 + s*f_d + t*f_a + C(s,2)*f_dd + s*t*f_da + C(t,2)*f_aa.
This script computes the six numbers for both versions and compares the resulting formula with the weight
computed directly from the metric for all 0 <= s, t <= 6.
"""
from itertools import combinations
from math import comb
from splitsys import canon, nanuq_2d, alphas_2
from local_terms import weight2, phi5, phi6


def splits_of(tree, n):
    full = (1 << n) - 1
    out = set()

    def rec(t):
        if isinstance(t, int):
            m = 1 << t
        else:
            m = rec(t[0]) | rec(t[1])
        if m != 0 and m != full:
            out.add(canon(n, m))
        return m
    rec(tree)
    return out


def family(s, t, version):
    A = list(range(0, t))
    b, x, y, c = t, t + 1, t + 2, t + 3
    D = list(range(t + 4, t + 4 + s))
    n = t + 4 + s

    def Acat(X):
        for a in reversed(A):
            X = (X, a)
        return X

    def Dcat(X):
        for d in D:
            X = (X, d)
        return X

    def clade(leaves):
        T = leaves[0]
        for l in leaves[1:]:
            T = (T, l)
        return T

    if version == "bloblet":
        trees = [(Acat((b, (x, y))), Dcat(c)), (Acat((b, x)), Dcat((y, c))),
                 (Acat(b), Dcat(((x, y), c))), (Acat(b), Dcat((x, (y, c))))]
    else:
        def withA(X):
            return (clade(A), X) if A else X

        def withD(X):
            return (X, clade(D)) if D else X
        trees = [(withA((b, (x, y))), withD(c)), (withA((b, x)), withD((y, c))),
                 (withA(b), withD(((x, y), c))), (withA(b), withD((x, (y, c))))]
    sigma = set()
    for tr in trees:
        sigma |= splits_of(tr, n)
    return n, sigma, (A, b, x, y, c, D)


def alpha2_direct(s, t, version):
    """2*alpha of {x,y}|rest from the metric."""
    n, sigma, (A, b, x, y, c, D) = family(s, t, version)
    al = alphas_2(n, nanuq_2d(n, sigma))
    i, j = sorted((b, y))           # U = {x_{i+1},...,x_j} = {x, y}: gaps b and y
    return al[(i, j)], al, sigma, n


def local_numbers(version):
    """2*Phi4, 2*Phi5'(d), 2*Phi5'(a), 2*Phi6'(d,d'), 2*Phi6'(d,a), 2*Phi6'(a,a')  (integers)."""
    out = {}
    n, sigma, (A, b, x, y, c, D) = family(0, 0, version)
    out["Phi4"] = 2 * weight2(sigma, n, x, y, c, b)              # 2*Phi4 = 2 * (2 w(xy|cb))
    # mirrored terms: (u1, z, up, v1, vq) := (c, z, b, x, y)  and  (u1, z, w, up, v1, vq) := (c, z, w, b, x, y)
    n, sigma, (A, b, x, y, c, D) = family(1, 0, version)
    out["d"] = phi5(sigma, n, c, D[0], b, x, y)
    n, sigma, (A, b, x, y, c, D) = family(0, 1, version)
    out["a"] = phi5(sigma, n, c, A[0], b, x, y)
    n, sigma, (A, b, x, y, c, D) = family(2, 0, version)
    out["dd"] = phi6(sigma, n, c, D[0], D[1], b, x, y)
    n, sigma, (A, b, x, y, c, D) = family(1, 1, version)
    out["da"] = phi6(sigma, n, c, D[0], A[0], b, x, y)
    n, sigma, (A, b, x, y, c, D) = family(0, 2, version)
    out["aa"] = phi6(sigma, n, c, A[0], A[1], b, x, y)
    return out


if __name__ == "__main__":
    for version in ("bloblet", "clade"):
        L = local_numbers(version)
        print(f"{version} version: 2*Phi4 = {L['Phi4']}, 2*Phi5'(d) = {L['d']}, 2*Phi5'(a) = {L['a']}, "
              f"2*Phi6'(d,d') = {L['dd']}, 2*Phi6'(d,a) = {L['da']}, 2*Phi6'(a,a') = {L['aa']}")
        ok = True
        rows = []
        for s in range(0, 7):
            for t in range(0, 7):
                a2, al, sigma, n = alpha2_direct(s, t, version)
                # alpha = 2*(alpha/2) = sum of the doubled local numbers; a2 is 2*alpha
                pred = 2 * (L["Phi4"] + s * L["d"] + t * L["a"] + comb(s, 2) * L["dd"] + s * t * L["da"] + comb(t, 2) * L["aa"])
                closed = 2 * (2 - comb(s + t, 2)) if version == "bloblet" else 2 * (2 - s * t)
                ok &= (a2 == pred == closed)
                rows.append((s, t, a2 // 2 if a2 % 2 == 0 else a2 / 2))
        print("   alpha({x,y}|rest) for s,t = 0..6:", " ".join(f"({s},{t}):{v}" for s, t, v in rows if s <= 3 and t <= 3))
        print("   formula from the six local numbers == direct computation == closed form "
              f"{'2 - C(s+t,2)' if version == 'bloblet' else '2 - s*t'} for all 0 <= s,t <= 6:", ok)
