"""(m) Helical states (constant torsion): a physically important non-generic family.

 1. one helix: is N(X) = 0 (Theorem A applies)?
 2. two helices: rank of the stacked configuration, dim N(z); (CC) fails at every length.
 3. are mixtures of two helices nevertheless identifiable?  Search for alternative ensembles
    in the set of linear images of the stacked configuration (restricted to its span) + LP.
 4. one helix + one generic chain.
"""
import sys
import numpy as np
from multiprocessing import Pool
from scipy.optimize import least_squares, linprog
from mylib import build_chain, sqdist, stack, e0_pairs, conic_system, nullspace

rng = np.random.default_rng(424242)
ANG = 97.0


def helix(n, tau):
    return build_chain(np.full(n - 3, tau), np.ones(n - 1), np.full(n - 2, np.pi - np.deg2rad(ANG)))


def randchain(n):
    return build_chain(rng.uniform(-np.pi, np.pi, n - 3), np.ones(n - 1), np.full(n - 2, np.pi - np.deg2rad(ANG)))


def solve_one(args):
    E, L2, r, seed = args
    g = np.random.default_rng(seed)

    def res(p):
        A = p.reshape(3, r)
        return ((E @ A.T) ** 2).sum(1) - L2

    def jac(p):
        A = p.reshape(3, r)
        Y = E @ A.T
        return (2 * Y[:, :, None] * E[:, None, :]).reshape(len(E), -1)

    p0 = g.normal(size=3 * r) * g.uniform(0.2, 2.0)
    meth = "lm" if len(L2) >= len(p0) else "trf"
    sol = least_squares(res, p0, jac=jac, method=meth, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=5000)
    return np.abs(sol.fun).max(), sol.x.reshape(3, r)


def alternatives(Xs, w, nstart=3000, label=""):
    """Linear images of the stacked configuration expressed in an orthonormal basis of its span."""
    n = len(Xs[0])
    Z = stack(Xs, w)
    Zc = Z - Z.mean(0)
    U, s, Vt = np.linalg.svd(Zc, full_matrices=False)
    r = int((s > 1e-9 * s[0]).sum())
    Y = U[:, :r] * s[:r]                                  # n x r, same squared distances as Z
    E = np.array([Y[j] - Y[i] for (i, j) in e0_pairs(n)])
    L2 = (E ** 2).sum(1)
    with Pool(4) as pool:
        out = pool.map(solve_one, [(E, L2, r, 17 * t + 3) for t in range(nstart)], chunksize=32)
    good = [A for res, A in out if res < 1e-12]
    Ps = np.array([A.T @ A for A in good])
    # the true states as points P_k = (coordinates of state k in the basis)
    true = []
    for k, X in enumerate(Xs):
        Ak, *_ = np.linalg.lstsq(Y, X - X.mean(0), rcond=None)       # X_c = Y A_k^T ... (r x 3)
        true.append(Ak @ Ak.T)
    iu = np.triu_indices(r)
    dtrue = np.array([[np.abs(P - T).max() for T in true] for P in Ps]) if len(Ps) else np.zeros((0, len(true)))
    other = Ps[(dtrue.min(1) > 1e-5)] if len(Ps) else Ps
    msg = f"   {label}: stack rank {r}; {len(good)}/{nstart} converged; points other than the true states: {len(other)}"
    if len(other) == 0:
        print(msg)
        return
    pts = true + list(other)
    Aeq = np.array([P[iu] for P in pts]).T
    beq = np.eye(r)[iu]
    cost = np.array([0.0] * len(true) + [-1.0] * len(other))
    lp = linprog(cost, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(pts), method="highs")
    if lp.status != 0:
        print(msg + f"; LP status {lp.status}")
        return
    c = lp.x
    supp = np.nonzero(c > 1e-9)[0]
    Asup = np.vstack([Aeq[:, supp], np.ones(len(supp))])
    csup, *_ = np.linalg.lstsq(Asup, np.concatenate([beq, [1.0]]), rcond=None)
    states = []
    for j in supp:
        P = pts[j]
        lam, Q = np.linalg.eigh(P)
        A = (Q[:, -3:] * np.sqrt(np.clip(lam[-3:], 0, None))).T       # 3 x r with A^T A = P
        states.append(Y @ A.T)
    Mtrue = sum(wk * sqdist(X) for wk, X in zip(w, Xs))
    Malt = sum(cj * sqdist(S) for cj, S in zip(csup, states))
    bond = max(abs(sqdist(S)[i, j] - sqdist(Xs[0])[i, j]) for S in states for (i, j) in e0_pairs(n))
    far = [min(np.abs(sqdist(S) - sqdist(X)).max() for X in Xs) for S in states]
    print(msg + f"; LP max mass off the true states = {-lp.fun:.4f}")
    if -lp.fun > 1e-6:
        print(f"      ALTERNATIVE ensemble, {len(supp)} states, weights {np.round(csup, 4).tolist()}: max|M(alt)-M(true)| = {np.abs(Malt-Mtrue).max():.1e}, "
              f"bond/1-3 deviation {bond:.1e}, distance of its states from the true states {np.round(far, 3).tolist()}")


if __name__ == "__main__":
    print("1. one helix: rank of the conic system (6 = no conic)")
    for n in (5, 6, 8, 12):
        for tau in (0.9, 2.2, -1.3):
            X = helix(n, tau)
            N, s, rank = nullspace(conic_system(X, e0_pairs(n)), 6)
            print(f"   n={n} tau={tau}: rank {rank}, smallest sv ratio {s[5]/s[0]:.2e}")
    print("2. two helices: rank of the stack, dim N(z) (K - 1 = 1 would be (CC))")
    for n in (12, 14, 20, 40):
        Xs = [helix(n, 0.9), helix(n, 2.2)]
        Z = stack(Xs, [0.4, 0.6])
        r = np.linalg.matrix_rank(Z - Z.mean(0), tol=1e-9)
        N, s, rank = nullspace(conic_system(Z, e0_pairs(n)), 21)
        print(f"   n={n}: affine rank of the stacked configuration {r} (6 needed); dim N(z) = {21 - rank}")
    print("3. alternatives to a mixture of two helices")
    for n in (14, 20):
        alternatives([helix(n, 0.9), helix(n, 2.2)], np.array([0.4, 0.6]), label=f"two helices, n={n}")
    print("4. one helix + one generic chain")
    for n in (12, 14):
        Xs = [helix(n, 0.9), randchain(n)]
        Z = stack(Xs, [0.4, 0.6])
        N, s, rank = nullspace(conic_system(Z, e0_pairs(n)), 21)
        print(f"   n={n}: dim N(z) = {21 - rank} (smallest kept sv ratio {s[rank-1]/s[0]:.1e})")
    print("5. control: two generic chains, n=14 (no alternatives expected)")
    alternatives([randchain(14), randchain(14)], np.array([0.4, 0.6]), nstart=1000, label="two generic chains, n=14")
