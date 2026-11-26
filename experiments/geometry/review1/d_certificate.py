"""(d) Theorem G: the certificate phi(X) = ||Pi_perp X||_F^2.

 * identity  phi(X) = -1/2 <Pi_perp, D(X)>,  phi(X_k) = 0,  positivity on random chains;
 * local value of kappa at each state (smallest eigenvalue of Pi_perp on the flexes modulo
   infinitesimal isometries, in the metric of d_P);
 * global attack: minimise phi and the ratio phi / min_k d_P(X, X_k)^2 over the torsions from
   many starts; report the smallest ratio found and whether it is attained far from the states.

usage: python3 d_certificate.py [n] [seed] [nstart]
"""
import sys
import numpy as np
from scipy.optimize import minimize
from mylib import build_chain, sqdist, stack, procrustes_dist


def setup(n, seed, angle=97.0, K=2):
    rng = np.random.default_rng(900 + seed)
    bonds = np.ones(n - 1)
    alphas = np.full(n - 2, np.pi - np.deg2rad(angle))
    w = rng.dirichlet(np.ones(K) * 4)
    tors = [rng.uniform(-np.pi, np.pi, n - 3) for _ in range(K)]
    Xs = [build_chain(t, bonds, alphas) for t in tors]
    Z = stack(Xs, w)
    B = np.hstack([np.ones((n, 1)), Z])
    Q, R = np.linalg.qr(B)
    assert np.abs(np.diag(R)).min() > 1e-8, "stacked configuration does not span"
    Pp = np.eye(n) - Q @ Q.T
    return rng, bonds, alphas, w, tors, Xs, Z, Pp


def tangent_fields(X):
    """Velocity fields of the torsions: torsion t rotates atoms >= t+3 about x_{t+1} -> x_{t+2}."""
    n = len(X)
    T = []
    for t in range(n - 3):
        u = X[t + 2] - X[t + 1]
        u /= np.linalg.norm(u)
        V = np.zeros((n, 3))
        V[t + 3:] = np.cross(u, X[t + 3:] - X[t + 2])
        T.append(V)
    return T


def local_kappa(X, Pp):
    n = len(X)
    T = tangent_fields(X)
    iso = [np.tile(e, (n, 1)) for e in np.eye(3)] + [np.cross(e, X - X.mean(0)) for e in np.eye(3)]
    Bi = np.array([v.ravel() for v in iso]).T
    Qi, _ = np.linalg.qr(Bi)
    Tm = np.array([v.ravel() - Qi @ (Qi.T @ v.ravel()) for v in T]).T          # 3n x (n-3)
    G = Tm.T @ Tm
    PT = np.array([(Pp @ v).ravel() for v in T]).T
    H = PT.T @ PT
    ev = np.linalg.eigvals(np.linalg.solve(G, H)).real
    return np.sort(ev)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    nstart = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    rng, bonds, alphas, w, tors, Xs, Z, Pp = setup(n, seed)
    chain = lambda t: build_chain(t, bonds, alphas)
    phi = lambda X: float(np.sum((Pp @ X) ** 2))
    print(f"n={n} K=2 seed={seed} weights {np.round(w, 4).tolist()}; rank Pi_perp = {int(round(np.trace(Pp)))} (= n-1-3K = {n-7})")
    print("  phi at the states:", [f"{phi(X):.1e}" for X in Xs])
    rnd = [chain(rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(5000)]
    vals = np.array([phi(X) for X in rnd])
    ident = max(abs(phi(X) + 0.5 * np.sum(Pp * sqdist(X))) for X in rnd[:200])
    # invariance under isometries (reflection included)
    Rr, _ = np.linalg.qr(rng.normal(size=(3, 3)))
    inv = max(abs(phi(X @ Rr + rng.normal(size=3)) - phi(X)) for X in rnd[:50])
    ratios = np.array([phi(X) / min(procrustes_dist(X, Xk) for Xk in Xs) ** 2 for X in rnd])
    print(f"  identity phi = -1/2<Pi_perp, D>: max defect {ident:.1e}; isometry invariance defect {inv:.1e}")
    print(f"  5000 random chains: min phi = {vals.min():.4f}, min ratio phi/min_k d_P^2 = {ratios.min():.5f}, median ratio {np.median(ratios):.4f}")
    loc = [local_kappa(X, Pp) for X in Xs]
    for k, ev in enumerate(loc):
        print(f"  local kappa at state {k}: smallest eigenvalues {np.round(ev[:3], 6).tolist()} ... largest {ev[-1]:.4f}")
    # check the local value by finite displacement along the softest direction
    for k, X in enumerate(Xs):
        T = tangent_fields(X)
        n3 = n - 3
        iso = [np.tile(e, (n, 1)) for e in np.eye(3)] + [np.cross(e, X - X.mean(0)) for e in np.eye(3)]
        Bi = np.array([v.ravel() for v in iso]).T
        Qi, _ = np.linalg.qr(Bi)
        Tm = np.array([v.ravel() - Qi @ (Qi.T @ v.ravel()) for v in T]).T
        G = Tm.T @ Tm
        PT = np.array([(Pp @ v).ravel() for v in T]).T
        evs, vecs = np.linalg.eig(np.linalg.solve(G, PT.T @ PT))
        c = vecs[:, np.argmin(evs.real)].real
        r = []
        for eps in (1e-2, 1e-3, 1e-4):
            Xe = chain(tors[k] + eps * c)
            r.append(phi(Xe) / procrustes_dist(Xe, X) ** 2)
        print(f"     finite-step ratio along the softest flex of state {k}: {['%.6f' % x for x in r]} (limit {evs.real.min():.6f})")

    def ratio(t):
        X = chain(t)
        d2 = min(procrustes_dist(X, Xk) for Xk in Xs) ** 2
        return phi(X) / max(d2, 1e-300)

    # (i) minimise phi from random starts: local minima of phi away from the states
    far = []
    for s in range(nstart):
        sol = minimize(lambda t: phi(chain(t)), rng.uniform(-np.pi, np.pi, n - 3), method="BFGS",
                       options=dict(gtol=1e-10, maxiter=2000))
        X = chain(sol.x)
        d = min(procrustes_dist(X, Xk) for Xk in Xs)
        far.append((sol.fun, d, sol.fun / max(d * d, 1e-300)))
    far = np.array(far)
    away = far[far[:, 1] > 1e-3]
    at_state = (far[:, 1] <= 1e-3).sum()
    print(f"  minimising phi from {nstart} starts: {at_state} runs reach a true state (phi -> 0); "
          f"{len(away)} end in other local minima")
    if len(away):
        i = np.argmin(away[:, 0])
        j = np.argmin(away[:, 2])
        print(f"     smallest phi at a local minimum away from the states: {away[i,0]:.5f} (d_P = {away[i,1]:.3f}, ratio {away[i,2]:.5f})")
        print(f"     smallest ratio at such a minimum: {away[j,2]:.5f} (phi = {away[j,0]:.5f}, d_P = {away[j,1]:.3f})")
    # (ii) minimise the ratio directly (Nelder-Mead is robust to the kink of min_k and the 0/0 at the states)
    best = (np.inf, None, None)
    rr = []
    for s in range(nstart // 4):
        t0 = rng.uniform(-np.pi, np.pi, n - 3)
        sol = minimize(ratio, t0, method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-12, maxiter=20000, maxfev=20000))
        sol = minimize(ratio, sol.x, method="BFGS", options=dict(gtol=1e-10, maxiter=500))
        X = chain(sol.x)
        d = min(procrustes_dist(X, Xk) for Xk in Xs)
        rr.append((sol.fun, d))
        if sol.fun < best[0]:
            best = (sol.fun, d, sol.x)
    rr = np.array(rr)
    print(f"  minimising the ratio from {nstart // 4} starts: smallest ratio found {best[0]:.6f} at d_P = {best[1]:.4f} from the nearest state")
    print(f"     distribution of final ratios: min {rr[:,0].min():.6f}, 10% {np.quantile(rr[:,0], 0.1):.6f}, median {np.median(rr[:,0]):.6f}")
    print(f"     local values: {[float(np.round(ev[0], 6)) for ev in loc]}  => kappa (numerical) = {min(best[0], min(ev[0] for ev in loc)):.6f}")
    C1 = np.sqrt(n - 1 - 6) / (2 * min(best[0], min(ev[0] for ev in loc)))
    print(f"     constant of G(c): sqrt(n-1-dK)/(2 kappa) ~ {C1:.1f}")


if __name__ == "__main__":
    main()
