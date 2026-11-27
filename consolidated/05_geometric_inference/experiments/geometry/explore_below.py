"""Exploration: two states, n = 7, 8, 9 -- below the threshold of Theorem I.  Sample chains
that are linear images of the stacked configuration (points P of the set P(z)) and ask, by a
linear program, whether the identity is a mixture that puts mass on points other than the two
states.  A positive answer is an explicit competing ensemble (non-identifiability among all
ensembles); a negative answer on a finite sample is only evidence."""
import sys
import numpy as np
from scipy.optimize import least_squares, linprog
from geomlib import chain, stack, edge_vectors, edm

def sample_points(Z, nstart, rng, tol=1e-20):
    E = np.array(edge_vectors(Z))
    L2 = (E ** 2).sum(1)
    m = Z.shape[1]
    def res(a):
        A = a.reshape(3, m)
        return ((E @ A.T) ** 2).sum(1) - L2
    pts = []
    for s in range(nstart):
        r = least_squares(res, rng.normal(size=3 * m) * rng.uniform(0.3, 2.0), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        if (r.fun ** 2).sum() < tol:
            A = r.x.reshape(3, m)
            P = A.T @ A
            if not any(np.linalg.norm(P - Q) < 1e-6 for Q in pts):
                pts.append(P)
    return pts

def run(n, seed, nstart):
    rng = np.random.default_rng(seed)
    w = rng.dirichlet(np.ones(2) * 3)
    Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(2)]
    Z = stack(Xs, w)
    true = [np.kron(np.diag([1.0 if j == k else 0.0 for j in range(2)]), np.eye(3)) / w[k] for k in range(2)]
    pts = sample_points(Z, nstart, rng)
    others = [P for P in pts if not any(np.linalg.norm(P - T) < 1e-4 for T in true)]
    allp = true + others
    Aeq = np.array([P.flatten() for P in allp]).T
    c = np.array([0.0, 0.0] + [-1.0] * len(others))
    r = linprog(c, A_eq=Aeq, b_eq=np.eye(6).flatten(), bounds=[(0, None)] * len(allp), method="highs")
    mass = -r.fun if r.status == 0 else float("nan")
    out = dict(n=n, seed=seed, sampled=len(pts), others=len(others), lp_status=r.status, max_mass_on_others=mass)
    if r.status == 0 and mass > 1e-6:
        cw = r.x
        states = []
        for cj, P in zip(cw, allp):
            if cj > 1e-9:
                lam, Q = np.linalg.eigh(P)
                A = (Q[:, -3:] * np.sqrt(np.clip(lam[-3:], 0, None))).T
                states.append((cj, Z @ A.T))
        M = sum(wk * edm(X) for wk, X in zip(w, Xs))
        M2 = sum(cj * edm(Y) for cj, Y in states)
        bonds = max(abs(np.linalg.norm(Y[1:] - Y[:-1], axis=1) - 1).max() for cj, Y in states)
        out.update(states=len(states), M_dev=float(np.abs(M - M2).max()), bond_dev=float(bonds))
    return out

if __name__ == "__main__":
    for n in [int(x) for x in sys.argv[1:]] or [7, 8, 9]:
        for seed in range(3):
            print(run(n, seed, 500 if n < 9 else 400), flush=True)
