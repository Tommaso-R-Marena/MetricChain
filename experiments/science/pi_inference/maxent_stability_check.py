"""Check of the stability bound for maximum-entropy refinement (science division, PI thread).

Setting.  X finite, reference mu0, features phi: X -> R^K, true ensemble
    mu  ~  mu0 * exp(-(lam . phi + r)),          osc(r) = max r - min r =: omega
(beta absorbed).  Data: m = E_mu[phi], exact.  MaxEnt refinement: nu ~ mu0 * exp(-lam' . phi)
with E_nu[phi] = m (the I-projection of mu0 on the data).

Claim (paper proof in docs/science/INFERENCE_LIMITS.md):
    KL(mu||nu) + KL(nu||mu) = E_nu[r] - E_mu[r] <= omega * TV(mu,nu),
    TV(mu,nu) <= omega/4,       KL(mu||nu) + KL(nu||mu) <= omega^2/4,
independently of |X|, K, phi, lam, mu0.  Also KL(mu||mu0) = KL(mu||nu) + KL(nu||mu0).
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(20261125)

def kl(p, q):
    mask = p > 0
    return float(np.sum(p[mask]*(np.log(p[mask]) - np.log(np.maximum(q[mask], 1e-300)))))

def maxent(mu0, phi, m):
    """minimise the convex dual  ln sum mu0 exp(-l.phi) + l.m  over l."""
    if phi.shape[1] == 0:
        return mu0.copy(), None
    def dual(l):
        a = np.log(mu0) - phi @ l
        mx = a.max()
        lz = mx + np.log(np.exp(a-mx).sum())
        p = np.exp(a - lz)
        return lz + l @ m, m - p @ phi
    res = minimize(lambda l: dual(l)[0], np.zeros(phi.shape[1]), jac=lambda l: dual(l)[1],
                   method="BFGS", options={"gtol": 1e-12, "maxiter": 5000})
    a = np.log(mu0) - phi @ res.x
    a -= a.max()
    p = np.exp(a); p /= p.sum()
    return p, res

worst_tv_ratio = 0.0; worst_j_ratio = 0.0; worst_pyth = 0.0; worst_id = 0.0; trials = 0
for trial in range(4000):
    N = int(rng.integers(2, 40)); K = int(rng.integers(0, min(N-1, 6)+1))
    mu0 = rng.dirichlet(np.ones(N)*rng.choice([0.3, 1.0, 5.0]))
    mu0 = np.maximum(mu0, 1e-9); mu0 /= mu0.sum()
    phi = rng.normal(size=(N, K)) * rng.choice([0.3, 1.0, 3.0])
    lam = rng.normal(size=K) * rng.choice([0.0, 1.0, 3.0])
    omega = float(rng.choice([0.05, 0.3, 1.0, 3.0, 8.0]))
    shape = rng.choice(["uniform", "twolevel", "spike"])
    if shape == "uniform":
        r = rng.uniform(0, 1, size=N)
    elif shape == "twolevel":
        r = (rng.uniform(size=N) < rng.uniform(0.1, 0.9)).astype(float)
    else:
        r = np.zeros(N); r[rng.integers(N)] = 1.0
    if r.max() == r.min():
        continue
    r = (r - r.min())/(r.max() - r.min())*omega
    a = np.log(mu0) - phi @ lam - r; a -= a.max()
    mu = np.exp(a); mu /= mu.sum()
    m = mu @ phi
    nu, res = maxent(mu0, phi, m)
    if K and np.max(np.abs(nu @ phi - m)) > 1e-7:
        continue                      # optimiser did not converge; skip (counted below)
    if mu.min() < 1e-250 or nu.min() < 1e-250:
        continue                      # numerically degenerate instance; skip
    trials += 1
    tv = 0.5*np.abs(mu - nu).sum()
    J = kl(mu, nu) + kl(nu, mu)
    ident = abs(J - (nu @ r - mu @ r))
    pyth = abs(kl(mu, mu0) - kl(mu, nu) - kl(nu, mu0))
    worst_id = max(worst_id, ident); worst_pyth = max(worst_pyth, pyth)
    worst_tv_ratio = max(worst_tv_ratio, tv/(omega/4))
    worst_j_ratio = max(worst_j_ratio, J/(omega**2/4))
    assert tv <= omega/4 + 1e-7, (tv, omega)
    assert J <= omega**2/4 + 1e-7, (J, omega)
print(f"trials used: {trials}")
print(f"max TV/(omega/4)   = {worst_tv_ratio:.6f}   (claim: <= 1)")
print(f"max J/(omega^2/4)  = {worst_j_ratio:.6f}   (claim: <= 1)")
print(f"max |J - (E_nu r - E_mu r)| = {worst_id:.2e}; max Pythagoras defect = {worst_pyth:.2e}")
# the extremal case: two points, no features
for omega in [0.01, 0.1, 1.0]:
    mu = np.array([1.0, np.exp(-omega)]); mu /= mu.sum(); nu = np.array([0.5, 0.5])
    print(f"two-point, omega={omega}: TV/(omega/4) = {0.5*np.abs(mu-nu).sum()/(omega/4):.6f}")
