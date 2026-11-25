"""Check of the extensive form of the stability bound (Theorem 7' of INFERENCE_LIMITS.md v3).

Cube {0,1}^n, reference mu0 a product measure, features Phi = single-site indicators (so the
maximum-entropy refinement nu of the model against the one-body marginals is a product
measure), truth  mu ~ mu0 exp(-(lam.Phi + r))  with r of single-site bounded differences c
(beta absorbed).  Claim:
    KL(mu||nu) <= n c^2 / 2,      |E_mu psi - E_nu psi| <= a * n c / 2
for every psi with single-site bounded differences a (Marton's transport inequality for the
product measure nu + Kantorovich-Rubinstein + identity (i) of Theorem 7).
Remainders tried: distance to a random set, random pair couplings, code-cone (Theorem 2),
random Lipschitz functions (McShane extensions of random values).
"""
import itertools, math
import numpy as np
rng = np.random.default_rng(11)

def cube(n):
    return np.array(list(itertools.product([0, 1], repeat=n)), dtype=np.int8)

def bounded_diff(X, f):
    """max single-site difference of f on the cube (rows of X in lexicographic order)."""
    n = X.shape[1]; N = len(X)
    idx = np.arange(N)
    return max(float(np.max(np.abs(f - f[idx ^ (1 << (n-1-i))]))) for i in range(n))

def kl(p, q):
    return float(np.sum(p*(np.log(p) - np.log(q))))

def run(n, trials=300):
    X = cube(n); N = len(X)
    worst_kl = 0.0; worst_obs = 0.0
    for t in range(trials):
        p0 = rng.uniform(0.2, 0.8, size=n)
        logmu0 = (X*np.log(p0) + (1-X)*np.log(1-p0)).sum(1)
        lam = rng.normal(size=n)*rng.choice([0, 1.0])
        c = float(rng.choice([0.2, 0.5, 1.0, 2.0]))
        kind = rng.choice(["dist", "pairs", "lip", "code"])
        if kind == "dist":
            S = rng.choice(N, size=int(rng.integers(1, 6)), replace=False)
            r = np.min((X[:, None, :] != X[None, S, :]).sum(-1), axis=1).astype(float)
        elif kind == "pairs":
            perm = rng.permutation(n); r = np.zeros(N)
            for a, b in zip(perm[0::2], perm[1::2]):
                r += rng.choice([-1, 1])*0.5*(2*X[:, a]-1)*(2*X[:, b]-1)
        elif kind == "lip":
            S = rng.choice(N, size=8, replace=False); v = rng.uniform(0, n, size=8)
            D = (X[:, None, :] != X[None, S, :]).sum(-1)
            r = np.min(v[None, :] + D, axis=1)
        else:
            # distance to the even-weight repetition-like code {0..0, 1..1}
            r = np.minimum(X.sum(1), n - X.sum(1)).astype(float)
        bd = bounded_diff(X, r)
        if bd == 0: continue
        r = r/bd*c
        a = logmu0 - X@lam - r; a -= a.max(); mu = np.exp(a); mu /= mu.sum()
        m = mu @ X                                  # one-body marginals
        nu = np.exp((X*np.log(m) + (1-X)*np.log(1-m)).sum(1))   # product measure with these marginals
        K = kl(mu, nu)
        worst_kl = max(worst_kl, K/(n*c*c/2))
        assert K <= n*c*c/2 + 1e-9, (kind, K, n*c*c/2)
        for psi in (r/c, X.sum(1).astype(float), np.min((X[:, None, :] != X[None, rng.choice(N, 3), :]).sum(-1), axis=1).astype(float)):
            apsi = bounded_diff(X, psi)
            if apsi == 0: continue
            gap = abs(mu@psi - nu@psi)/(apsi*n*c/2)
            worst_obs = max(worst_obs, gap)
            assert gap <= 1 + 1e-9
    print(f"n={n}: {trials} instances; max KL(mu||nu)/(n c^2/2) = {worst_kl:.4f}; "
          f"max |E_mu psi - E_nu psi|/(a n c/2) = {worst_obs:.4f}")

for n in (6, 8, 10):
    run(n)
