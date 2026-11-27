"""(c) Theorem D, numerically and constructively.

 n = 6: a random chain in R^4 (and in R^5) with unit bonds and fixed inner product of
        consecutive bond vectors has a quadric through its 9 constrained edge directions; its
        squared-distance matrix is decomposed into a mixture of chains in R^3 (recursively).
 n = 7: a random chain in R^4 has NO quadric through its 11 edge directions; a separating
        linear functional  X -> ||Pi_perp X||^2  (zero at the 4D chain, positive on every 3D
        chain) is evaluated by multi-start minimisation over the 4 torsions of 3D chains.
"""
import numpy as np
from scipy.optimize import minimize
from mylib import build_chain, sqdist, e0_pairs, conic_system, nullspace, unvech


def random_chain_Rd(n, dim, gamma, rng):
    """unit bonds u_a in S^{dim-1}, u_a.u_{a+1} = gamma."""
    U = [rng.normal(size=dim)]
    U[0] /= np.linalg.norm(U[0])
    for a in range(1, n - 1):
        v = rng.normal(size=dim)
        v -= (v @ U[-1]) * U[-1]
        v /= np.linalg.norm(v)
        U.append(gamma * U[-1] + np.sqrt(1 - gamma ** 2) * v)
    return np.vstack([np.zeros(dim), np.cumsum(U, axis=0)])


def reduce_rank(Y, tol=1e-7):
    """Express the configuration in coordinates of its affine span."""
    Yc = Y - Y.mean(0)
    U, s, Vt = np.linalg.svd(Yc, full_matrices=False)
    r = int((s > tol * s[0]).sum())
    return U[:, :r] * s[:r]


def decompose(Y, weight, out, depth=0):
    """Recursively write D(Y) as a mixture of configurations of rank <= 3 with the same lengths
    on E0 (possible whenever a quadric through the edge directions exists)."""
    Y = reduce_rank(Y)
    n, r = Y.shape
    if r <= 3:
        out.append((weight, np.hstack([Y, np.zeros((n, 3 - r))])))
        return
    A = conic_system(Y, e0_pairs(n))
    N, s, rank = nullspace(A, r * (r + 1) // 2)
    assert len(N) >= 1, "no quadric: extreme point of rank %d" % r
    S = unvech(N[-1], r)
    ev, Q = np.linalg.eigh(S)
    tp, tm = -1.0 / ev[0], -1.0 / ev[-1]           # I + tS singular at these (tp > 0 > tm)
    lam = -tm / (tp - tm)
    for t, wgt in ((tp, lam), (tm, 1 - lam)):
        lamb = np.clip(1 + t * ev, 0, None)
        lamb[np.argmin(lamb)] = 0.0                # the eigenvalue that vanishes at t (exactly)
        decompose(Y @ (Q * np.sqrt(lamb)), weight * wgt, out, depth + 1)


if __name__ == "__main__":
    rng = np.random.default_rng(31415)
    ang = 97.0
    gamma = np.cos(np.pi - np.deg2rad(ang))        # inner product of consecutive unit bond vectors
    print(f"bond angle {ang} deg, gamma = u_a.u_(a+1) = {gamma:.6f}")
    print("== n = 6: chains in R^4 and R^5 decompose into chains in R^3 (Theorem D(a)) ==")
    for dim in (4, 5):
        for rep in range(4):
            Y = random_chain_Rd(6, dim, gamma, rng)
            A = conic_system(Y, e0_pairs(6))
            N, s, rank = nullspace(A, dim * (dim + 1) // 2)
            out = []
            decompose(Y, 1.0, out)
            DY = sqdist(Y)
            Dmix = sum(wt * sqdist(X) for wt, X in out)
            bond_dev = max(abs(sqdist(X)[i, j] - DY[i, j]) for wt, X in out for (i, j) in e0_pairs(6))
            ranks = [np.linalg.matrix_rank(X - X.mean(0), tol=1e-8) for wt, X in out]
            sv4 = np.linalg.svd(Y - Y.mean(0), compute_uv=False)
            print(f"  R^{dim} chain (singular values {np.round(sv4, 3).tolist()}): quadric space dim {len(N)}; "
                  f"mixture of {len(out)} chains in R^3, weights {np.round([wt for wt, X in out], 4).tolist()}, "
                  f"ranks {ranks}; max|D(Y) - sum w D(X)| = {np.abs(DY - Dmix).max():.1e}; bond/1-3 deviation {bond_dev:.1e}")
    print("== n = 7: a random chain in R^4 has no quadric through its 11 edge directions (Theorem D(b)) ==")
    for rep in range(6):
        Y = random_chain_Rd(7, 4, gamma, rng)
        A = conic_system(Y, e0_pairs(7))
        s = np.linalg.svd(A, compute_uv=False)
        # separating functional: phi(X) = ||Pi_perp X||^2 with Pi_perp the projector onto the
        # orthogonal complement of span(1, columns of Y);  phi(Y) = 0, phi >= 0.
        B = np.hstack([np.ones((7, 1)), Y])
        Qb, _ = np.linalg.qr(B)
        Pp = np.eye(7) - Qb @ Qb.T
        bonds = np.ones(6)
        alphas = np.full(5, np.pi - np.deg2rad(ang))
        phi = lambda t: np.sum((Pp @ build_chain(t, bonds, alphas)) ** 2)
        best = np.inf
        for start in range(300):
            sol = minimize(phi, rng.uniform(-np.pi, np.pi, 4), method="BFGS", options=dict(gtol=1e-12))
            best = min(best, sol.fun)
        print(f"  4D chain {rep}: singular values of the 11x10 quadric system: min {s[-1]:.3e}, max {s[0]:.3e} "
              f"(nullity {10 - int((s > 1e-9 * s[0]).sum())}); min over 3D chains of ||Pi_perp X||^2 = {best:.3e} > 0 "
              f"(300 starts)  => D(Y) is separated from conv D(C)")
