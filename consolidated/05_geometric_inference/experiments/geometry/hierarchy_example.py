"""Theorem E(d), a numerical instance: a globally rigid 6-atom chain X whose averaged data on
the measured pairs are reproduced exactly by a two-state ensemble of other chains.

Chain: unit bonds, bond angle 111 degrees (statewise constraints E0: 5 bonds, 4 one-three
distances).  Measured pairs F = {14, 25, 36, 16} (1-based).  The framework (F u E0, X) has
13 = 3*6 - 6 + 1 bars, hence a one-dimensional space of equilibrium stresses; its stress
matrix has rank 2 = n - 4 (so the generic framework is globally rigid in R^3:
Gortler-Healy-Thurston), and we pick X with an INDEFINITE stress matrix (not universally
rigid: Gortler-Thurston).

Steps (floating point, residuals printed):
 1. find torsions with an indefinite stress matrix;
 2. find a realisation Y in R^4 with the same lengths on F u E0 (a flex into the 4th dimension);
 3. Y has 9 constrained edge directions in R^4 and dim Sym(4) = 10, so a quadric S through them
    exists; I + tS stays positive semidefinite for t in [t-, t+] and has rank 3 at the ends;
 4. X+ = Y (I + t+ S)^{1/2}, X- = Y (I + t- S)^{1/2} are chains in R^3 (same bond data), and
    D(Y) = lam D(X+) + (1 - lam) D(X-) with lam = -t-/(t+ - t-).
Hence the ensemble {X+ (lam), X- (1-lam)} has the averaged squared distances of X on F, while
neither state is congruent to X.
"""
import sys
import numpy as np
from scipy.optimize import least_squares
from geomlib import chain, edm, sym_index, quad_row, sym_from_vec

n = 6
E0 = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
F = [(0, 3), (1, 4), (2, 5), (0, 5)]
G = E0 + F


def rigidity_matrix(X, edges):
    R = np.zeros((len(edges), X.size))
    dim = X.shape[1]
    for e, (i, j) in enumerate(edges):
        R[e, dim * i:dim * i + dim] = X[i] - X[j]
        R[e, dim * j:dim * j + dim] = X[j] - X[i]
    return R


def stress_matrix(X, edges):
    R = rigidity_matrix(X, edges)
    U, s, Vt = np.linalg.svd(R.T)
    omega = Vt[-1]                      # left null vector of R (dimension 1 for generic X)
    resid = np.linalg.norm(R.T @ omega)
    Om = np.zeros((n, n))
    for w, (i, j) in zip(omega, edges):
        Om[i, i] += w; Om[j, j] += w; Om[i, j] -= w; Om[j, i] -= w
    return Om, resid, s


def main(seed=0, verbose=True):
    rng = np.random.default_rng(seed)
    # 1. indefinite stress
    for _ in range(1000):
        tors = rng.uniform(-np.pi, np.pi, n - 3)
        X = chain(n, tors)
        Om, resid, s = stress_matrix(X, G)
        ev = np.linalg.eigvalsh(Om)
        big = np.abs(ev) > 1e-8 * np.abs(ev).max()
        if big.sum() == 2 and ev[big].min() < -0.15 * np.abs(ev).max() and ev[big].max() > 0.15 * np.abs(ev).max():
            break
    else:
        raise RuntimeError("no indefinite stress found")
    target = np.array([((X[i] - X[j]) ** 2).sum() for (i, j) in G])
    # 2. realisation in R^4: start from X with a fourth coordinate along an isotropic vector of Omega
    lam_, vec = np.linalg.eigh(Om)
    ip, im = np.argmax(lam_), np.argmin(lam_)
    q = vec[:, ip] / np.sqrt(lam_[ip]) + vec[:, im] / np.sqrt(-lam_[im])      # q^T Omega q = 0
    best = None
    for h in (0.3, 0.5, 0.8, -0.3, -0.5):
        Y0 = np.hstack([X, h * q[:, None]])
        def res(y):
            Y = y.reshape(n, 4)
            r = [((Y[i] - Y[j]) ** 2).sum() - t for (i, j), t in zip(G, target)]
            # gauge: atom 0 at the origin; pin the height of the fourth coordinate spread
            r += list(Y[0])
            r.append((Y[:, 3] - Y[:, 3].mean()).std() - abs(h) * q.std())
            return np.array(r)
        sol = least_squares(res, Y0.flatten(), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=20000)
        if np.abs(sol.fun).max() < 1e-11:
            Y = sol.x.reshape(n, 4)
            sv = np.linalg.svd(Y - Y.mean(0), compute_uv=False)
            if sv[3] > 1e-3:
                best = (Y, np.abs(sol.fun).max(), sv)
                break
    if best is None:
        raise RuntimeError("no four-dimensional realisation found")
    Y, res4, sv4 = best
    # 3. quadric through the 9 constrained edge directions of Y
    idx = sym_index(4)
    A = np.array([quad_row(Y[j] - Y[i], idx) for (i, j) in E0])
    S = sym_from_vec(np.linalg.svd(A)[2][-1], 4, idx)
    quad_resid = np.abs(A @ np.array([S[i, j] for (i, j) in idx])).max()
    ev = np.linalg.eigvalsh(S)
    tp, tm = -1.0 / ev.min(), -1.0 / ev.max()       # I + tS singular at t = -1/eig
    # 4. the two three-dimensional chains
    def image(t):
        lam, Q = np.linalg.eigh(np.eye(4) + t * S)
        lam = np.clip(lam, 0, None)
        keep = np.argsort(lam)[1:]                  # drop the zero eigenvalue
        return Y @ (Q[:, keep] * np.sqrt(lam[keep]))
    Xp, Xm = image(tp), image(tm)
    lam = -tm / (tp - tm)
    DY, DX = edm(Y), edm(X)
    Dmix = lam * edm(Xp) + (1 - lam) * edm(Xm)
    checks = dict(
        stress_residual=resid,
        stress_eigenvalues=np.round(np.linalg.eigvalsh(Om), 6).tolist(),
        fourD_residual=res4,
        fourD_singular_values=np.round(sv4, 4).tolist(),
        quadric_residual=quad_resid,
        weights=(lam, 1 - lam),
        max_dev_statewise_Xp=max(abs(edm(Xp)[i, j] - DX[i, j]) for (i, j) in E0),
        max_dev_statewise_Xm=max(abs(edm(Xm)[i, j] - DX[i, j]) for (i, j) in E0),
        max_dev_mixture_vs_Y_all_pairs=np.abs(Dmix - DY).max(),
        max_dev_mixture_vs_X_on_F=max(abs(Dmix[i, j] - DX[i, j]) for (i, j) in F),
        Xp_differs_from_X_on_F=max(abs(edm(Xp)[i, j] - DX[i, j]) for (i, j) in F),
        Xm_differs_from_X_on_F=max(abs(edm(Xm)[i, j] - DX[i, j]) for (i, j) in F),
        mixture_differs_from_X_on_unmeasured=max(abs(Dmix[i, j] - DX[i, j]) for (i, j) in [(0, 4), (1, 5)]),
    )
    ok = (checks["max_dev_statewise_Xp"] < 1e-9 and checks["max_dev_statewise_Xm"] < 1e-9
          and checks["max_dev_mixture_vs_X_on_F"] < 1e-9 and 0 < lam < 1
          and checks["Xp_differs_from_X_on_F"] > 1e-3 and checks["Xm_differs_from_X_on_F"] > 1e-3)
    if verbose:
        print("torsions of X (degrees):", np.round(np.rad2deg(tors), 3).tolist())
        for k, v in checks.items():
            print(f"  {k}: {v}")
        print("OK: the two-state ensemble reproduces the averaged data of X on F" if ok else "FAIL")
    return ok, checks


if __name__ == "__main__":
    ok, _ = main(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    sys.exit(0 if ok else 1)
