"""Check of the 'code-cone' non-identifiability construction (science division, PI thread).

Claim.  Let C be a binary linear code of length n with dual distance d_perp > k.  Then every
probability measure on {0,1}^n that is invariant under translation by C has exactly uniform
marginals on every set of at most k coordinates.  In particular mu_b(x) ~ exp(-b * dist(x, C))
(a Gibbs measure whose energy c*dist(x,C) has single-site bounded differences c, b = beta*c)
is k-wise uniform for every b, while its entropy tends to n*h(sigma(b)) + O(log|C|), the
minimum n*h(sigma(b)) allowed in the bounded-difference class.

This script verifies, exactly by enumeration:
  (i)   k-wise uniformity of mu_b for C = RM(1,m) (dual = extended Hamming, d_perp = 4, k = 3)
        and C = simplex code (dual = Hamming, d_perp = 3, k = 2), and failure at order k+1;
  (ii)  the class lower bound S >= n*h(sigma(b));
  (iii) the entropy of mu_b against n*h(sigma(b)) and n*ln 2.
"""
import itertools, math, sys
import numpy as np

def hb(p):
    return 0.0 if p <= 0 or p >= 1 else -p*math.log(p) - (1-p)*math.log(1-p)

def sigma(b):
    return 1.0/(1.0+math.exp(-b))

def span(gens, n):
    words = {0}
    for g in gens:
        words |= {w ^ g for w in words}
    return sorted(words)

def rm1(m):
    """generators of RM(1,m), length 2^m, as bit masks"""
    n = 1 << m
    gens = [(1 << n) - 1]
    for j in range(m):
        g = 0
        for pos in range(n):
            if (pos >> j) & 1:
                g |= 1 << pos
        gens.append(g)
    return n, gens

def simplex(m):
    """simplex code of length 2^m - 1 (dual of Hamming)"""
    n = (1 << m) - 1
    gens = []
    for j in range(m):
        g = 0
        for pos in range(1, n+1):
            if (pos >> j) & 1:
                g |= 1 << (pos-1)
        gens.append(g)
    return n, gens

def dist_to_code(n, code):
    """array of dist(x, C) for all x in {0,1}^n, by BFS from the code (multi-source)."""
    N = 1 << n
    d = np.full(N, -1, dtype=np.int16)
    frontier = np.array(code, dtype=np.int64)
    d[frontier] = 0
    r = 0
    while frontier.size:
        r += 1
        nxt = []
        for i in range(n):
            y = frontier ^ (1 << i)
            y = y[d[y] < 0]
            if y.size:
                y = np.unique(y)
                d[y] = r
                nxt.append(y)
        frontier = np.unique(np.concatenate(nxt)) if nxt else np.array([], dtype=np.int64)
    return d

def max_marginal_deviation(p, n, order):
    """max over all coordinate subsets of size `order` of |marginal - uniform| (sup over cells)."""
    N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    bits = [((idx >> i) & 1).astype(np.int64) for i in range(n)]
    worst = 0.0
    for S in itertools.combinations(range(n), order):
        key = np.zeros(N, dtype=np.int64)
        for t, i in enumerate(S):
            key |= bits[i] << t
        marg = np.bincount(key, weights=p, minlength=1 << order)
        worst = max(worst, float(np.max(np.abs(marg - 1.0/(1 << order)))))
    return worst

def run(name, n, gens, k, bs):
    code = span(gens, n)
    d = dist_to_code(n, code).astype(np.float64)
    print(f"\n== {name}: n={n}, |C|={len(code)}, covering radius={int(d.max())}, claimed k={k}")
    for b in bs:
        w = np.exp(-b*d)
        Z = w.sum()
        p = w/Z
        S = float(-(p*np.log(p)).sum())
        dev_k = max(max_marginal_deviation(p, n, j) for j in range(1, k+1))
        dev_k1 = max_marginal_deviation(p, n, k+1)
        lo = n*hb(sigma(b))
        print(f"  b={b:4.1f}  S={S:9.5f}  class min n*h(sigma(b))={lo:9.5f}  n ln2={n*math.log(2):9.5f}"
              f"  S-lo={S-lo:8.5f} (ln|C|={math.log(len(code)):.3f})"
              f"  max|marg-unif| orders<= {k}: {dev_k:.2e}; order {k+1}: {dev_k1:.3e}")
        assert S >= lo - 1e-9, "class lower bound violated"
        assert dev_k < 1e-12, "not k-wise uniform"

if __name__ == "__main__":
    bs = [0.5, 1.0, 2.0, 4.0]
    n, gens = simplex(3); run("simplex [7,3,4], dual Hamming d=3", n, gens, 2, bs)
    n, gens = rm1(3);     run("RM(1,3) [8,4,4], self-dual, d_perp=4", n, gens, 3, bs)
    n, gens = simplex(4); run("simplex [15,4,8], dual Hamming d=3", n, gens, 2, bs)
    n, gens = rm1(4);     run("RM(1,4) [16,5,8], dual ext. Hamming d=4", n, gens, 3, bs)
