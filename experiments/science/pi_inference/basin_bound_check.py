"""Check of the basin-population bound for k-wise uniform ensembles (science division, PI thread).

Claim (Theorem D of docs/science/INFERENCE_LIMITS.md).  Let mu be ANY probability measure on
{0,1}^n whose marginals on at most k = 2t coordinates are uniform.  With Krawtchouk sums
    F_t(d) = sum_{j<=t} K_j(d),  K_j(d) = sum_i (-1)^i C(d,i) C(n-d,j-i),   M_t = F_t(0) = sum_{j<=t} C(n,j),
every Hamming ball satisfies
    mu(B(a,r)) <= M_t / min_{d<=r} F_t(d)^2        (whenever F_t > 0 on [0,r]).
In particular a single configuration has mass at most 1/M_t (the Rao bound, weighted form).

Checked here: (i) the orthonormality identity E_mu f^2 = M_t for f = sum_{|T|<=t} chi_T(a) chi_T,
on C-invariant measures built from RM(1,m) (k = 3, t = 1) and from random coset weights;
(ii) the inequality for all centres a and radii r; (iii) how close the code-cone mixture
comes (attained / bound).
"""
import math, itertools
import numpy as np
from code_cone_check import rm1, simplex, span, dist_to_code

def kraw(n, j, d):
    return sum((-1)**i * math.comb(d, i) * math.comb(n-d, j-i) for i in range(0, j+1))

def F(n, t, d):
    return sum(kraw(n, j, d) for j in range(t+1))

def popcount(a):
    return np.array([bin(int(v)).count("1") for v in a], dtype=np.int64) if a.dtype == object else _pc(a)

def _pc(a):
    a = a.copy(); c = np.zeros(a.shape, dtype=np.int64)
    while np.any(a):
        c += (a & 1); a >>= 1
    return c

def check(name, n, gens, t, rng, ntrial=6):
    code = span(gens, n); N = 1 << n
    idx = np.arange(N, dtype=np.int64)
    d_code = dist_to_code(n, code)
    M = F(n, t, 0)
    Fd = np.array([F(n, t, d) for d in range(n+1)], dtype=float)
    print(f"\n== {name}: n={n}, |C|={len(code)}, t={t}, M_t={M}")
    # representative of each coset: use canonical id = min element of coset
    rep = idx.copy()
    for c in code:
        rep = np.minimum(rep, idx ^ c)
    reps, inv = np.unique(rep, return_inverse=True)
    worst = 0.0
    for trial in range(ntrial):
        if trial == 0:
            b = 3.0; w = np.exp(-b*d_code.astype(float)); label = "exp(-3 dist(x,C))"
        elif trial == 1:
            b = 8.0; w = np.exp(-b*d_code.astype(float)); label = "exp(-8 dist(x,C))"
        else:
            cw = rng.dirichlet(np.ones(len(reps))*rng.choice([0.02, 0.2, 1.0])); w = cw[inv]; label = "random coset weights"
        p = w/w.sum()
        for a in [0, int(rng.integers(N)), int(code[len(code)//2])]:
            dist = _pc(idx ^ a)
            f = Fd[dist]
            Ef2 = float((p*f*f).sum())
            assert abs(Ef2 - M) < 1e-6*M, (Ef2, M)
            mass_by_d = np.bincount(dist, weights=p, minlength=n+1)
            cum = np.cumsum(mass_by_d)
            for r in range(0, n//2):
                if np.min(Fd[:r+1]) <= 0: break
                bound = M/np.min(Fd[:r+1])**2
                assert cum[r] <= bound + 1e-12, (label, a, r, cum[r], bound)
                worst = max(worst, cum[r]/bound)
        print(f"  {label:22s}: E f^2 = M_t verified; max attained/bound over centres and radii so far = {worst:.4f}")

rng = np.random.default_rng(7)
n, gens = rm1(3); check("RM(1,3), k=3", n, gens, 1, rng)
n, gens = rm1(4); check("RM(1,4), k=3", n, gens, 1, rng)
n, gens = simplex(4); check("simplex [15,4], k=2", n, gens, 1, rng)
