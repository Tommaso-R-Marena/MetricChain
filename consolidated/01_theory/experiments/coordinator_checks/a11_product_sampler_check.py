# Independent check (own code) of the science division's Proposition A1.1: on the cube with known part Bern(p)^n and a
# u-Lipschitz residual psi, the Gibbs law nu_psi has all conditionals in [a0, a1] and KL(nu_psi || Bern(r*)^n) <= n*a,
# a = information radius of the two letter laws = capacity; plus the truncation bound for importance sampling.
import numpy as np, itertools, math
from scipy.optimize import brentq
rng = np.random.default_rng(5)
sig = lambda t: 1 / (1 + math.exp(-t))
def kl(a, b): return a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b))
def radius(p, u):
    a0, a1 = sig(math.log(p / (1 - p)) - u), sig(math.log(p / (1 - p)) + u)
    r = brentq(lambda r: kl(a0, r) - kl(a1, r), a0 + 1e-12, a1 - 1e-12)
    return a0, a1, r, kl(a0, r)
def lipschitz(n, u, kind):
    X = np.array(list(itertools.product((0, 1), repeat=n)))
    if kind == "cone":
        c = X[rng.integers(len(X))]; return X, u * np.abs(X - c).sum(1)
    if kind == "anticone":
        c = X[rng.integers(len(X))]; return X, -u * np.abs(X - c).sum(1)
    if kind == "trunc":
        c = X[rng.integers(len(X))]; return X, u * np.maximum(np.abs(X - c).sum(1), rng.integers(0, n))
    # McShane extension of random values on a random subset
    k = int(rng.integers(1, 8)); idx = rng.choice(len(X), size=k, replace=False); vals = rng.uniform(-u * n, u * n, size=k)
    # make the anchor values consistent: lower envelope of cones
    D = np.abs(X[:, None, :] - X[idx][None, :, :]).sum(2)
    return X, (vals[None, :] + u * D).min(1)
worst = 0.0
for trial in range(600):
    n = int(rng.integers(3, 11)); p = float(rng.uniform(0.05, 0.6)); u = float(rng.uniform(0.3, 3.0))
    a0, a1, r, a = radius(p, u)
    X, psi = lipschitz(n, u, rng.choice(["cone", "anticone", "trunc", "mcshane"]))
    # check Lipschitz
    w = np.exp(-(psi - psi.min())) * np.prod(np.where(X == 1, p, 1 - p), axis=1)
    nu = w / w.sum()
    Q = np.prod(np.where(X == 1, r, 1 - r), axis=1)
    KL = float((nu * np.log(nu / Q)).sum())
    worst = max(worst, KL / (n * a))
    assert KL <= n * a + 1e-9, (KL, n * a)
    # conditionals given a prefix
    for k in range(n):
        for pref in itertools.product((0, 1), repeat=k):
            m = np.all(X[:, :k] == np.array(pref), axis=1) if k else np.ones(len(X), bool)
            s1 = nu[m & (X[:, k] == 1)].sum(); s0 = nu[m & (X[:, k] == 0)].sum()
            t = s1 / (s0 + s1)
            assert a0 - 1e-12 <= t <= a1 + 1e-12
    # truncation bound: E_Q |rho 1{rho<=tau} - E| part: E_Q[rho^2 1{rho <= tau}] <= tau
    rho = nu / Q
    for tau in (1.0, math.exp(n * a / 2), math.exp(n * a)):
        assert float((Q * rho ** 2 * (rho <= tau)).sum()) <= tau + 1e-9
print("600 instances: KL(nu_psi || Bern(r*)^n) <= n a, largest ratio", round(worst, 6), "(1 at cones)")
# the capacity-achieving output marginal against p and the uniform law
for p, u in ((0.3775, 2.0), (0.2689, 2.0), (0.1192, 2.0), (0.0474, 2.0), (0.5, 1.0)):
    a0, a1, r, a = radius(p, u)
    print(f"p={p} u={u}: letter laws ({a0:.4f}, {a1:.4f}), r*={r:.4f}, a={a:.5f}, with r=p the bound would be {max(kl(a0, p), kl(a1, p)):.5f}")
# range of the log-likelihood increments is at most 2u
for trial in range(2000):
    p = float(rng.uniform(0.02, 0.9)); u = float(rng.uniform(0.1, 4.0)); a0, a1, r, a = radius(p, u)
    vals = [math.log(t / r) for t in (a0, a1)] + [math.log((1 - t) / (1 - r)) for t in (a0, a1)]
    assert max(vals) - min(vals) <= 2 * u + 1e-9
print("range of the increments of the log-likelihood ratio <= 2u in 2000 parameter pairs")
