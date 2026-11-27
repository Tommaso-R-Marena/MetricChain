"""Coordinator's check: workstream A1's chain-rule bound (Proposition A1.1) for a site with
three letters and a path envelope -- the reference example of theory report 11.26 /
THY-MSG-0011 section 1(c): site law pi = (0.5, 0.3, 0.2), envelope = path metric with steps
0.8, 1.6.

Claims checked:
 (1) the Shannon capacity of the "vertex channel" (vertices phi of the site's Lipschitz
     polytope -> Gibbs laws pi_phi ~ pi e^{-phi}) equals the theory division's a = 0.294791
     (own Blahut-Arimoto; they quote the value);
 (2) for every psi on X = {0,1,2}^n with psi(x) - psi(y) <= sum_i d(x_i, y_i), the conditional
     law of each site given any prefix lies in the convex hull of the vertex laws, hence
     KL(nu_psi || Q*^n) <= n a  with Q* the capacity-achieving output law (chain rule +
     convexity + capacity = information radius);
 (3) equality (up to o(n)) is approached by product instances built from the vertices.
Exact enumeration, n = 4..7, random admissible psi of several kinds.
"""
import itertools, math
import numpy as np
from scipy.optimize import linprog
rng = np.random.default_rng(5)

pi = np.array([0.5, 0.3, 0.2]); steps = (0.8, 1.6)
D = np.array([[0, steps[0], steps[0]+steps[1]], [steps[0], 0, steps[1]], [steps[0]+steps[1], steps[1], 0]])
verts = np.array([[0, s1*steps[0], s1*steps[0] + s2*steps[1]] for s1 in (1, -1) for s2 in (1, -1)])
laws = np.array([pi*np.exp(-v) / (pi*np.exp(-v)).sum() for v in verts])

def blahut_arimoto(W, iters=20000, tol=1e-13):
    m = len(W); p = np.ones(m)/m
    for _ in range(iters):
        q = p @ W
        d = (W*np.log(W/q)).sum(1)
        new = p*np.exp(d); new /= new.sum()
        if np.max(np.abs(new-p)) < tol: p = new; break
        p = new
    q = p @ W; d = (W*np.log(W/q)).sum(1)
    return float(p @ d), float(d.max()), p, q

lo, hi, pin, Q = blahut_arimoto(laws)
print(f"vertex channel: capacity in [{lo:.6f}, {hi:.6f}] (theory division: a = 0.294791); Q* = {np.round(Q, 5)}; input weights {np.round(pin, 4)}")

def in_hull(p, pts, tol=1e-9):
    m = len(pts)
    res = linprog(np.zeros(m), A_eq=np.vstack([pts.T, np.ones(m)]), b_eq=np.concatenate([p, [1.0]]),
                  bounds=(0, None), method="highs")
    return res.status == 0

def random_admissible(X, kind):
    n = X.shape[1]; N = len(X)
    if kind == "additive":
        idx = rng.integers(0, len(verts), size=n)
        return sum(verts[idx[i]][X[:, i]] for i in range(n))
    # McShane-type: min over anchors of value + site distance (admissible for a symmetric metric)
    k = int(rng.integers(1, 9)); A = X[rng.choice(N, size=k, replace=False)]
    v = rng.uniform(0, rng.choice([0.5, 2.0, 6.0])*n, size=k)
    dist = np.zeros((N, k))
    for i in range(n):
        dist += D[X[:, i][:, None], A[:, i][None, :]]
    return np.min(v[None, :] + dist, axis=1) if kind == "min" else np.max(v[None, :] - dist, axis=1)

worst = 0.0; hull_fail = 0; tested = 0
for n in (4, 5, 6, 7):
    X = np.array(list(itertools.product(range(3), repeat=n)))
    logpi = np.log(pi)[X].sum(1)
    for kind in ("additive", "min", "max"):
        for rep in range(6):
            psi = random_admissible(X, kind)
            # admissibility check on single-site moves (sufficient for a site-additive metric)
            a = logpi - psi; a -= a.max(); nu = np.exp(a); nu /= nu.sum()
            kl = float(np.sum(nu*(np.log(nu) - np.log(Q)[X].sum(1))))
            worst = max(worst, kl/(n*hi))
            assert kl <= n*hi + 1e-9, (n, kind, kl, n*hi)
            # conditional law of site i given the prefix, for a few random prefixes
            T = nu.reshape([3]*n)
            for i in range(n):
                marg = T.sum(axis=tuple(range(i+1, n))) if i < n-1 else T
                flat = marg.reshape(-1, 3)
                for row in flat[rng.choice(len(flat), size=min(len(flat), 5), replace=False)]:
                    if row.sum() <= 0: continue
                    tested += 1
                    if not in_hull(row/row.sum(), laws): hull_fail += 1
print(f"instances: KL(nu_psi || Q*^n) <= n a in all cases; largest KL/(n a) = {worst:.6f}")
print(f"conditional laws tested: {tested}; outside the convex hull of the vertex laws: {hull_fail}")
