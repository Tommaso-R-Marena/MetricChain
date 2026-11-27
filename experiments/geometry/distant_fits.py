"""Distant configurations that fit sequence-local distances (an independent replication of
finding F1 of the Science division's review SCI-REV-0028 of Theorem L).

For an idealised trace X and a target r: minimise the root-mean-square error of the 4n - 10
distances of sequence separation <= 4 over configurations Y whose RMSD from X (after the best
rigid motion or reflection) is at least r.  Local optimisation (L-BFGS with a quadratic
penalty of increasing weight) from tails reflected in the plane of three consecutive points
and from random starts: every error printed is an UPPER bound for the true minimum, without
a certificate.  Written from the statement of the finding; it uses none of that division's
code and none of its stored configurations (which are not on its branch).

Usage: distant_fits.py            (about a minute; ends with ALL OK if a configuration farther
                                   than the radius of gyration fits the helix-like trace of 20
                                   points to 0.35 angstrom or better)
"""
import sys

import numpy as np
from scipy.optimize import minimize

from local_data_guarantees import trace
from local_data_upper import band_pairs


def rmsd(X, Y, improper=True):
    """After the best rigid motion or reflection (rigid motions only if not improper), with its
    gradient in Y."""
    Xc, Yc = X - X.mean(0), Y - Y.mean(0)
    U, s, Vt = np.linalg.svd(Yc.T @ Xc)
    if not improper and np.linalg.det(U @ Vt) < 0:
        U = U.copy()
        U[:, -1] = -U[:, -1]
    R = U @ Vt                                   # Yc R ~ Xc
    diff = Yc @ R - Xc
    val = np.sqrt((diff ** 2).sum() / len(X))
    grad = (diff @ R.T) / (len(X) * max(val, 1e-300))
    return val, grad - grad.mean(0)


def objective(y, X, J, K, dX, r, weight, improper=True):
    Y = y.reshape(-1, 3)
    diff = Y[J] - Y[K]
    d = np.linalg.norm(diff, axis=1)
    err = d - dX
    f = (err ** 2).mean()
    g = np.zeros_like(Y)
    coef = (2 * err / (len(err) * d))[:, None] * diff
    np.add.at(g, J, coef)
    np.add.at(g, K, -coef)
    val, gr = rmsd(X, Y, improper)
    if val < r:
        f += weight * (r - val) ** 2
        g += -2 * weight * (r - val) * gr
    return f, g.ravel()


def reflect_tail(X, i):
    """Points after i reflected in the plane of points i-2, i-1, i."""
    a, b, c = X[i - 2], X[i - 1], X[i]
    nrm = np.cross(b - a, c - a)
    nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 1:] = X[i + 1:] - 2 * ((X[i + 1:] - c) @ nrm)[:, None] * nrm
    return Y


def best_fit(X, r, rng, random_starts=4, improper=True):
    n = len(X)
    pairs = band_pairs(n)
    J = np.array([p[0] for p in pairs])
    K = np.array([p[1] for p in pairs])
    dX = np.linalg.norm(X[J] - X[K], axis=1)
    starts = [reflect_tail(X, i) for i in range(2, n - 2)]
    starts += [X + rng.normal(scale=r, size=X.shape) for _ in range(random_starts)]
    best = None
    for Y0 in starts:
        y = Y0.ravel().copy()
        for weight in (1.0, 10.0, 100.0, 1e3, 1e4):
            y = minimize(objective, y, args=(X, J, K, dX, r, weight, improper), jac=True, method="L-BFGS-B",
                         options=dict(maxiter=4000)).x
        Y = y.reshape(-1, 3)
        val = rmsd(X, Y, improper)[0]
        err = np.linalg.norm(Y[J] - Y[K], axis=1) - dX
        if val >= r * (1 - 1e-3):
            cand = (float(np.sqrt((err ** 2).mean())), float(np.abs(err).max()), float(val), Y)
            if best is None or cand[0] < best[0]:
                best = cand
    return best


def main():
    rng = np.random.default_rng(28)
    ok = True
    for name, geo, n, targets in (("helix-like", (2.3, 1.5, 100.0), 20, (1.0, 3.0, 5.0, 7.0, 9.0, 9.95)),
                                  ("helix-like", (2.3, 1.5, 100.0), 12, (3.0, 5.76, 6.35)),
                                  ("strand-like (160 deg)", (0.94, 3.3, 160.0), 20, (5.0, 12.0, 18.6))):
        X = trace(n, *geo)
        rg = float(np.sqrt(((X - X.mean(0)) ** 2).sum() / n))
        print(f"{name}, n = {n}: radius of gyration {rg:.2f}")
        for r in targets:
            res = best_fit(X, r, rng)
            if res is None:
                print(f"   RMSD >= {r:5.2f}: no configuration found")
                continue
            print(f"   RMSD >= {r:5.2f}: local distances fitted to rms {res[0]:.3f} (largest error {res[1]:.3f}) at RMSD {res[2]:.2f}")
            if name == "helix-like" and n == 20 and r >= 9.0:
                ok &= res[0] <= 0.35 and res[2] > rg
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
