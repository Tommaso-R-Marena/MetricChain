"""Finite-precision versions (INFERENCE_LIMITS_ADDENDA.md A9).  Exact enumeration.

(1) Noisy-codeword mixture nu_{C,b} (Theorem 2): for every character chi_T,
        E_nu[chi_T] = tanh(b/2)^{|T|}  if T is a word of the dual code,  0 otherwise      (exact).
    So ALL correlations, of every order, are within tanh(b/2)^{d_perp} of the uniform ensemble's.
(2) C-symmetrised dip (Theorem 4), balls disjoint:  for T in the dual code, |T| = j,
        E_mu[chi_T] = chi_T(a) * (1/Z) * |C| * 2^{-n} * sum_{d<r} C(n,d) (e^{u(r-d)} - 1) * kappa_j(d),
        kappa_j(d) = K_j(d) / C(n,j)   (Krawtchouk),   and 0 for T outside the dual code;
    hence |E_mu[chi_T]| <= (Z-1)/Z * max_{d<r} |kappa_j(d)|.
(3) Pinned ensembles with ABSOLUTE precision tau: ln Z from n pinned one-body marginals and one
    evaluation, error <= n * tau * (1 + e^u) + O(tau^2), in the class of constant u.
"""
import math, itertools
import numpy as np
from code_cone_check import rm1, simplex, span, dist_to_code
rng = np.random.default_rng(3)

def kraw(n, j, d):
    return sum((-1)**i * math.comb(d, i) * math.comb(n-d, j-i) for i in range(j+1))

def popcnt(a):
    a = a.copy(); c = np.zeros(a.shape, dtype=np.int64)
    while np.any(a): c += a & 1; a >>= 1
    return c

def chars(n, T, idx):
    return 1 - 2*(popcnt(idx & T) & 1)

for name, (n, gens) in (("simplex [15,4]", simplex(4)), ("RM(1,4) [16,5]", rm1(4))):
    code = span(gens, n); N = 1 << n; idx = np.arange(N, dtype=np.int64)
    # dual code membership: T orthogonal to all generators
    dual = [T for T in range(1, N) if all(bin(T & g).count("1") % 2 == 0 for g in gens)]
    dual_set = set(dual); dperp = min(bin(T).count("1") for T in dual)
    # (1) noisy-codeword mixture
    for b in (0.5, 1.0, 2.0):
        p = np.zeros(N)
        s = 1/(1+math.exp(-b))
        for c in code:
            dist = popcnt(idx ^ c)
            p += s**(n-dist) * (1-s)**dist
        p /= len(code)
        worst_in = worst_out = 0.0
        for T in [int(t) for t in rng.choice(N-1, size=300, replace=False)+1] + dual[:200]:
            e = float((chars(n, T, idx)*p).sum()); j = bin(T).count("1")
            if T in dual_set: worst_in = max(worst_in, abs(e - math.tanh(b/2)**j))
            else: worst_out = max(worst_out, abs(e))
        print(f"{name} (d_perp={dperp}) b={b}: max |E chi_T - tanh(b/2)^|T|| on dual words = {worst_in:.1e}; "
              f"max |E chi_T| off the dual code = {worst_out:.1e}; tanh(b/2)^d_perp = {math.tanh(b/2)**dperp:.4f}")
    # (2) symmetrised dip, radius r with disjoint balls
    dC = dist_to_code(n, code).astype(float)
    dmin = min(bin(c).count("1") for c in code if c)
    for u in (1.0, 2.0):
        for r in range(1, (dmin-1)//2 + 2):
            if 2*(r-1) >= dmin: continue          # open balls of radius r must be disjoint
            w = np.exp(u*np.maximum(r - dC, 0)); Z = w.mean()
            worst = 0.0; bound_ok = True
            for T in sorted(dual, key=lambda t: bin(t).count("1"))[:60]:
                j = bin(T).count("1")
                e = float((chars(n, T, idx)*w).mean()/Z)
                pred = len(code)/N*sum(math.comb(n, d)*math.expm1(u*(r-d))*kraw(n, j, d)/math.comb(n, j) for d in range(r))/Z
                worst = max(worst, abs(e - pred))
                bnd = (Z-1)/Z*max(abs(kraw(n, j, d))/math.comb(n, j) for d in range(r))
                bound_ok &= abs(e) <= bnd + 1e-12
            print(f"{name} u={u} r={r}: Z={Z:.4f}; formula for E chi_T on dual words exact to {worst:.1e}; bound holds: {bound_ok}")

# (3) pinned ensembles with absolute precision
n = 12; u = 1.0; X = np.array(list(itertools.product([0, 1], repeat=n)))
worst_ratio = 0.0
for trial in range(200):
    S = X[rng.choice(len(X), size=6, replace=False)]; v = rng.uniform(0, n*u, size=6)
    g = np.min(v[None, :] + u*(X[:, None, :] != S[None, :, :]).sum(-1), axis=1)      # u-Lipschitz
    wts = np.exp(-g); Z = wts.sum(); mu = wts/Z
    xs = X[rng.integers(len(X))]; tau = float(rng.choice([1e-4, 1e-3, 1e-2]))
    logprod = 0.0; mask = np.ones(len(X), bool)
    for i in range(n):
        cond = mu[mask]; sel = X[mask][:, i] == xs[i]
        m = cond[sel].sum()/cond.sum() + rng.uniform(-tau, tau)
        logprod += math.log(m); mask &= (X[:, i] == xs[i])
    idxs = int("".join(map(str, xs)), 2)
    err = abs((-g[idxs] - logprod) - math.log(Z))
    worst_ratio = max(worst_ratio, err/(n*tau*(1+math.exp(u))))
print(f"pinned ensembles, n={n}, u={u}: 200 instances, max |error of ln Z| / (n tau (1+e^u)) = {worst_ratio:.3f}")
