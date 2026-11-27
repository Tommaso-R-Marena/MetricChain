#!/usr/bin/env python3
"""Workstream I, experiment 8: the composition lemma for two blocks.

Blocks Q_{n1}, Q_{n2} with uniform measures and Hamming costs u1, u2 per flip (integers here).
Harper's theorem gives the exact growth function of each block; for a set E of the product with
fibre measures m_a (a in block 1) and A_s = {a : m_a >= s}:

    mu(E_t) >= g1( mu1(A_s), j1 ) * g2( s, j2 )          for all s in (0,1], u1 j1 + u2 j2 <= t,
    mu(E)   =  int_0^1 mu1(A_s) ds.

Hence  mu(E_t) >= v*(m, t) := inf { v : int_0^1 a_v(s) ds >= m },  a_v(s) = sup{ a : F(a, s) <= v },
F(a, s) = max over splits of g1(a, j1) g2(s, j2);  and (pigeonhole)  v* >= min{ F(a, s) : a s >= m / (2 K) },
K = ceil(log2(2/m)) + 1.

(1) exhaustive check on tiny products (all subsets): the bound is valid; how close.
(2) moderate sizes: v* against the union of neighbourhoods of a product of two balls (achievable).
Floating point; exploration."""
import sys, math, itertools
import numpy as np

def ball_table(n):
    b = [math.comb(n, j) / 2.0 ** n for j in range(n + 1)]
    cum = np.cumsum(b)
    return cum            # cum[r] = measure of the ball of radius r

def harper(n):
    """g(m, j): PL interpolation in m through ball measures (valid lower bound by Harper + LYM);
    for 0 < m <= 2^-n the set is at least a point."""
    cum = ball_table(n)
    def g(m, j):
        if m <= 0: return 0.0
        if j <= 0:
            return m
        if m <= cum[0]: return float(cum[min(j, n)])
        if m >= 1.0: return 1.0
        r = int(np.searchsorted(cum, m, side='right')) - 1      # cum[r] <= m < cum[r+1]
        f = (m - cum[r]) / (cum[r + 1] - cum[r])
        lo = cum[min(r + j, n)]; hi = cum[min(r + 1 + j, n)]
        return float(lo + f * (hi - lo))
    return g, cum

def F_factory(n1, n2, u1, u2, t):
    g1, c1 = harper(n1); g2, c2 = harper(n2)
    splits = [(j1, (t - u1 * j1) // u2) for j1 in range(0, t // u1 + 1)]
    def F(a, s):
        return max(g1(a, j1) * g2(s, j2) for (j1, j2) in splits)
    return F

def a_v(F, s, v):
    """sup{ a in [0,1] : F(a, s) <= v } (F nondecreasing in a); 0 if F(0+, s) > v."""
    if F(1.0, s) <= v: return 1.0
    lo, hi = 0.0, 1.0
    if F(1e-300, s) > v: return 0.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if F(mid, s) <= v: lo = mid
        else: hi = mid
    return lo

def vstar(F, m, ns=4000):
    """inf{ v : int_0^1 a_v(s) ds >= m }, by bisection on v; the integral by an upper Riemann sum on a
    geometric grid of s (a_v nonincreasing in s, so the upper sum over-estimates the integral: the
    resulting v is a valid, slightly smaller, bound)."""
    sgrid = np.concatenate([[0.0], np.exp(np.linspace(math.log(1e-12), 0.0, ns))])
    def integral(v):
        tot = 0.0
        for i in range(1, len(sgrid)):
            tot += (sgrid[i] - sgrid[i - 1]) * a_v(F, sgrid[i - 1] if sgrid[i - 1] > 0 else 1e-300, v)
        return tot
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if integral(mid) >= m: hi = mid
        else: lo = mid
    return lo

def pigeon(F, m, npts=400):
    K = math.ceil(math.log2(2.0 / m)) + 1
    target = m / (2 * K)
    best = 1.0
    for a in np.exp(np.linspace(math.log(target), 0.0, npts)):
        s = min(1.0, target / a)
        best = min(best, F(a, s))
    return best

def brute(n1, n2, u1, u2):
    n = n1 + n2; N = 1 << n
    pts = list(range(N))
    def cost(x, y):
        d = x ^ y
        return u1 * bin(d & ((1 << n1) - 1)).count('1') + u2 * bin(d >> n1).count('1')
    tmax = u1 * n1 + u2 * n2
    nb = {t: [sum(1 << y for y in pts if cost(x, y) <= t) for x in pts] for t in range(1, tmax + 1)}
    best = {}                                   # (cardinality, t) -> min |E_t|
    for mask in range(1, 1 << N):
        k = bin(mask).count('1')
        xs = [x for x in pts if mask >> x & 1]
        for t in range(1, tmax + 1):
            g = 0
            for x in xs: g |= nb[t][x]
            c = bin(g).count('1')
            if (k, t) not in best or c < best[(k, t)]: best[(k, t)] = c
    # monotone in cardinality: min over sets with at least k points
    for t in range(1, tmax + 1):
        for k in range(N - 1, 0, -1):
            best[(k, t)] = min(best[(k, t)], best.get((k + 1, t), N))
    return best, N, tmax

def main():
    print("(1) exhaustive: blocks Q_2 x Q_2, costs (1, 2); all 65535 nonempty subsets")
    best, N, tmax = brute(2, 2, 1, 2)
    worst_ratio = 1.0; bad = 0
    for t in (1, 2, 3, 4):
        F = F_factory(2, 2, 1, 2, t)
        row = []
        for k in (1, 2, 3, 4, 6, 8, 12):
            m = k / N
            v = vstar(F, m, ns=600)
            truth = best[(k, t)] / N
            if v > truth + 1e-9: bad += 1
            worst_ratio = min(worst_ratio, v / truth)
            row.append(f"k={k}: {v:.4f}/{truth:.4f}")
        print(f"  t={t}: bound/true min   " + "  ".join(row))
    print(f"  violations (bound above the true minimum): {bad}; smallest bound/truth = {worst_ratio:.3f}")
    assert bad == 0
    print("(2) moderate sizes: n1 = n2 = 10, costs (1, 2): bound against a product of two balls")
    n1 = n2 = 10; u1, u2 = 1, 2
    g1, c1 = harper(n1); g2, c2 = harper(n2)
    for (r1, r2) in ((1, 1), (2, 1), (1, 3), (3, 3), (4, 2)):
        m = c1[r1] * c2[r2]
        for t in (2, 4, 8):
            F = F_factory(n1, n2, u1, u2, t)
            v = vstar(F, m, ns=500); pg = pigeon(F, m)
            # neighbourhood of the product of balls: union over splits = {(x,y): u1 (|x|-r1)+ + u2 (|y|-r2)+ <= t}
            tot = 0.0
            for i in range(n1 + 1):
                for j in range(n2 + 1):
                    if u1 * max(i - r1, 0) + u2 * max(j - r2, 0) <= t:
                        tot += math.comb(n1, i) * math.comb(n2, j) / 2.0 ** (n1 + n2)
            print(f"  balls ({r1},{r2}) m={m:.3e} t={t}: v* = {v:.4e}, pigeonhole bound = {pg:.4e}, product of balls = {tot:.4e}  (ratio v*/achievable {v/tot:.3f})")

if __name__ == "__main__":
    main()
