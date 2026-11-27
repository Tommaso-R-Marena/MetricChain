"""A route that does not close the gap of Theorem L (docs/geometry/DEAD_ENDS.md DG-26).

For squared distances of sequence separation <= 4 every stress matrix is D^T diag(w) D, with
D the affine dependencies of consecutive five-point windows; it is positive semidefinite iff
w >= 0.  A stress of maximal rank gives a bound that is global and linear in Gram space, at
the price of the factor A = 1 + Lambda ||omega||_2 / lambda^+(Omega).  This script maximises
lambda^+ / ||omega|| over w on idealised traces and compares A with the factor C_L * 2 mu
between Theorem L and the first-order constant.  Floating point; an exploration, kept so
that the numbers quoted in LOCAL_DATA_STABILITY.md section 6 (v) can be reproduced.

Usage: stress_route.py     (a few seconds; ends with ALL OK if the stresses are stresses and
                            the factor A exceeds C_L * 2 mu from 20 points on)
"""
import sys

import numpy as np
from scipy.optimize import minimize

from local_data_guarantees import trace
from local_data_upper import band_pairs, sharp_constants


def dependencies(X):
    n = len(X)
    Dm = np.zeros((n - 4, n))
    for i in range(n - 4):
        v = np.linalg.svd(np.vstack([np.ones(5), X[i:i + 5].T]))[2][-1]
        Dm[i, i:i + 5] = v / np.linalg.norm(v)
    return Dm


def ratio(w, Dm, pairs):
    Om = Dm.T @ (w[:, None] * Dm)
    lam = np.linalg.eigvalsh(Om)[4]                  # smallest eigenvalue off the kernel span(1, x, y, z)
    om = np.array([-Om[j, k] for j, k in pairs])
    return lam / np.linalg.norm(om)


def main():
    ok = True
    for name, geo in (("helix-like", (2.3, 1.5, 100.0)), ("strand-like", (0.94, 3.3, 160.0))):
        for n in (12, 20, 40):
            X = trace(n, *geo)
            pairs = band_pairs(n)
            Dm = dependencies(X)
            mu, Lam, CL = sharp_constants(X)
            res = minimize(lambda lw: -np.log(ratio(np.exp(lw), Dm, pairs)), np.zeros(n - 4), method="L-BFGS-B")
            best = ratio(np.exp(res.x), Dm, pairs)
            A = 1 + Lam / best
            resid = np.linalg.norm((Dm.T @ Dm) @ np.column_stack([np.ones(n), X]))
            ok &= resid < 1e-9 and (n < 20 or A > CL * 2 * mu)
            print(f"{name:12s} n = {n:3d}: lambda+/||omega|| = {best:.2e} (uniform weights {ratio(np.ones(n - 4), Dm, pairs):.2e}); "
                  f"A = {A:.2e}; C_L * 2 mu = {CL * 2 * mu:.2e}")
    print("ALL OK" if ok else "SOME FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
