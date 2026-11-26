"""(b),(f) Search in the set  P(z) = { P in I + N(z) : P >= 0, rank P <= 3 }  (Lemma 2.2 /
Theorem B'): every state of every competing ensemble is a linear image A z with A^T A in P(z).

 * multi-start least squares over A in R^{3 x 3K} (gauge-fixed: first 3x3 block lower
   triangular) for |A e|^2 = |e|^2 on the 2n-3 constrained stacked edge vectors;
 * classification of the solutions (forced points E_k/w_k versus others);
 * linear program: is I a convex combination of points of P(z) with positive mass outside the
   forced points?  If yes, the explicit alternative ensemble is built and verified directly
   (bond data of every state, mean squared-distance matrix, non-congruence).

usage: python3 b_pz.py K n nstart [seed] [angle_deg]
"""
import sys
import time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import least_squares, linprog
from mylib import build_chain, sqdist, stack, e0_pairs, conic_system, nullspace

TRI = np.tril_indices(3)


def unpackA(p, m):
    A = np.zeros((3, m))
    A[TRI] = p[:6]
    A[:, 3:] = p[6:].reshape(3, m - 3)
    return A


def make_problem(K, n, seed, angle_deg=97.0):
    rng = np.random.default_rng(5000 + seed)
    bonds = np.ones(n - 1)
    alphas = np.full(n - 2, np.pi - np.deg2rad(angle_deg))
    w = rng.dirichlet(np.ones(K) * 4)
    Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(K)]
    Z = stack(Xs, w)
    E = np.array([Z[j] - Z[i] for (i, j) in e0_pairs(n)])
    L2 = (E ** 2).sum(1)
    return dict(K=K, n=n, w=w, Xs=Xs, Z=Z, E=E, L2=L2, bonds=bonds, alphas=alphas)


def solve_one(args):
    E, L2, m, seed = args
    rng = np.random.default_rng(seed)

    def res(p):
        A = unpackA(p, m)
        return ((E @ A.T) ** 2).sum(1) - L2

    def jac(p):
        A = unpackA(p, m)
        Y = E @ A.T                                    # edges x 3
        Jfull = 2 * Y[:, :, None] * E[:, None, :]      # d r_e / d A_{c i} = 2 (A e)_c e_i
        J1 = Jfull[:, TRI[0], TRI[1]]
        J2 = Jfull[:, :, 3:].reshape(len(E), -1)
        return np.hstack([J1, J2])

    p0 = rng.normal(size=6 + 3 * (m - 3)) * rng.uniform(0.2, 2.0)
    meth = "lm" if len(L2) >= len(p0) else "trf"
    sol = least_squares(res, p0, jac=jac, method=meth, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=5000)
    A = unpackA(sol.x, m)
    return np.abs(sol.fun).max(), A


def main():
    K = int(sys.argv[1]); n = int(sys.argv[2]); nstart = int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    angle = float(sys.argv[5]) if len(sys.argv) > 5 else 97.0
    pr = make_problem(K, n, seed, angle)
    m = 3 * K
    Z, E, L2, w = pr["Z"], pr["E"], pr["L2"], pr["w"]
    dimN = m * (m + 1) // 2 - nullspace(conic_system(Z, e0_pairs(n)), m * (m + 1) // 2)[2]
    t0 = time.time()
    with Pool(4) as pool:
        out = pool.map(solve_one, [(E, L2, m, 31 * seed + 104729 * s + 1) for s in range(nstart)], chunksize=16)
    good = [A for r, A in out if r < 1e-12]
    forced = [np.kron(np.diag([1.0 if j == k else 0.0 for j in range(K)]), np.eye(3)) / w[k] for k in range(K)]
    Ps = [A.T @ A for A in good]
    # distinct solutions
    distinct, counts, As = [], [], []
    for P, A in zip(Ps, good):
        for t, Q in enumerate(distinct):
            if np.abs(P - Q).max() < 1e-6:
                counts[t] += 1
                break
        else:
            distinct.append(P); counts.append(1); As.append(A)
    isforced = [any(np.abs(P - Fk).max() < 1e-6 for Fk in forced) for P in distinct]
    nforced_found = sum(any(np.abs(P - Fk).max() < 1e-6 for P in distinct) for Fk in forced)
    print(f"K={K} n={n} seed={seed} angle={angle}: dim N(z)={dimN}, weights {np.round(w, 4).tolist()}; "
          f"{nstart} starts, {len(good)} converged (|res|<1e-12), {time.time()-t0:.0f}s")
    print(f"   distinct points of P(z) found: {len(distinct)}  (forced points found: {nforced_found}/{K}; "
          f"other points: {len(distinct) - sum(isforced)})")
    spur = [(P, A, c) for P, A, c, f in zip(distinct, As, counts, isforced) if not f]
    if len(spur) <= 40:
        for P, A, c in spur:
            ev = np.linalg.eigvalsh(P)
            Y = Z @ A.T
            dmin = min(np.abs(sqdist(Y) - sqdist(X)).max() for X in pr["Xs"])
            print(f"     other point: hits {c:4d}, eigenvalues {np.round(ev, 4).tolist()}, "
                  f"chain max|D - D(X_k)| >= {dmin:.3f}")
    # LP: maximise the mass outside the forced points in a representation of I
    pts = forced + [P for P, A, c in spur]
    iu = np.triu_indices(m)
    Aeq = np.array([P[iu] for P in pts]).T
    beq = np.eye(m)[iu]
    cost = np.array([0.0] * K + [-1.0] * len(spur))
    lp = linprog(cost, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(pts), method="highs")
    if lp.status != 0:
        print("   LP status", lp.status, lp.message)
        return
    mass = -lp.fun
    print(f"   LP: max mass outside the forced points in a representation of I = {mass:.6f}")
    if mass > 1e-6:
        c = lp.x
        supp = np.nonzero(c > 1e-10)[0]
        # polish the weights on the support by least squares (exact affine combination)
        Asup = np.vstack([Aeq[:, supp], np.ones(len(supp))])
        bsup = np.concatenate([beq, [1.0]])
        csup, *_ = np.linalg.lstsq(Asup, bsup, rcond=None)
        states, weights = [], []
        for j, cj in zip(supp, csup):
            if j < K:
                Y = pr["Xs"][j]
            else:
                Y = Z @ spur[j - K][1].T
            states.append(Y); weights.append(cj)
        weights = np.array(weights)
        Mtrue = sum(wk * sqdist(X) for wk, X in zip(w, pr["Xs"]))
        Malt = sum(cj * sqdist(Y) for cj, Y in zip(weights, states))
        # every state must be a chain with the prescribed bond data
        Dref = sqdist(pr["Xs"][0])
        bond_dev = max(abs(sqdist(Y)[i, j] - Dref[i, j]) for Y in states for (i, j) in e0_pairs(n))
        noncong = [min(np.abs(sqdist(Y) - sqdist(X)).max() for X in pr["Xs"]) for Y in states]
        print(f"   ALTERNATIVE ENSEMBLE with {len(supp)} states: weights {np.round(weights, 5).tolist()} (min {weights.min():.2e}, sum {weights.sum():.12f})")
        print(f"      max |M(alt) - M(true)| = {np.abs(Malt - Mtrue).max():.2e};  max bond/1-3 deviation of its states = {bond_dev:.2e}")
        print(f"      distance of each state from the true states (max|D - D(X_k)|): {np.round(noncong, 3).tolist()}")
        np.savez(f"alt_K{K}_n{n}_s{seed}.npz", weights=weights, states=np.array(states), w=w, Xs=np.array(pr["Xs"]))


if __name__ == "__main__":
    main()
