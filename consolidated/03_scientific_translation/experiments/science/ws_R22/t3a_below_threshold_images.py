#!/usr/bin/env python3
"""R22 Item 3(a) continued: generic pairs BELOW the conic threshold n0(2) = 12 -- which linear images of z are chains,
and can they carry mass?  (Own LM enumeration + LP as in t3c_short_segments.py; a cross-check of my enumeration
against the Geometry division's statements: n >= 10 only the two states [their Theorem I at 7c2a3d1, exact];
n = 9 four to six further real images that carry no mass; n = 7, 8 a surface of images and competing ensembles.)
Run: OMP_NUM_THREADS=1 python3 -B t3a_below_threshold_images.py > t3a_below_threshold_images.log
"""
import time
import numpy as np
from scipy.optimize import least_squares, linprog
import r22lib as L

t0 = time.time(); COS = -5.0 / 13.0; W = (0.37, 0.63)


def enumerate_linear_images(z, nstart, rng, tol=1e-10):
    n, m = z.shape
    Ed = np.array([z[j] - z[i] for i, j in L.E0(n)]); l2 = (Ed ** 2).sum(1)
    res = lambda a: ((Ed @ a.reshape(3, m).T) ** 2).sum(1) / l2 - 1.0
    def jac(a):
        AE = Ed @ a.reshape(3, m).T
        return (2.0 * AE[:, :, None] * Ed[:, None, :] / l2[:, None, None]).reshape(len(Ed), 3 * m)
    found, nconv = [], 0
    for s in range(nstart):
        a0 = rng.normal(size=3 * m) * rng.uniform(0.3, 2.5)
        meth = "lm" if len(Ed) >= 3 * m else "trf"
        sol = least_squares(res, a0, jac=jac, method=meth, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        if np.abs(sol.fun).max() > tol:
            continue
        nconv += 1
        Y = z @ sol.x.reshape(3, m).T; Dx = L.sqdist(Y)
        for f in found:
            if np.abs(f[0] - Dx).max() < 1e-5:
                break
        else:
            found.append((Dx, Y))
    return found, nconv


def lp(Ds, M):
    n = M.shape[0]; iu = [(i, j) for i in range(n) for j in range(i + 3, n)]
    Aeq = np.array([[D[i, j] for D in Ds] for (i, j) in iu] + [[1.0] * len(Ds)]); beq = np.array([M[i, j] for (i, j) in iu] + [1.0])
    c = np.zeros(len(Ds)); c[[0, 1]] = 1.0
    return linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(Ds), method="highs",
                   options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})


print("=== R22: generic pairs below the conic threshold (K = 2, cos(bond angle) = -5/13, weights 0.37/0.63); 600 LM starts each; seed base 2310")
print("| n | instance | dim N(z) | converged/starts | distinct linear images that are chains | of these other than the two states | "
      "LP: minimal mass on the two true states | competitor atoms | max |sum c D - M| | min d_P^2 of a competitor state to a true state |")
print("|---|---|---|---|---|---|---|---|---|---|")
for n in (8, 9, 10, 11, 12):
    for inst in range(3):
        rng = np.random.default_rng(2310 + 10 * n + inst)
        X1, X2 = L.chain(rng.uniform(-np.pi, np.pi, n - 3), COS), L.chain(rng.uniform(-np.pi, np.pi, n - 3), COS)
        z = L.stack([X1, X2], W)
        found, nconv = enumerate_linear_images(z, 600, rng)
        D1, D2 = L.sqdist(X1), L.sqdist(X2); M = W[0] * D1 + W[1] * D2
        others = [(D, Y) for D, Y in found if min(np.abs(D - D1).max(), np.abs(D - D2).max()) >= 1e-5]
        Ds = [D1, D2] + [D for D, _ in others]
        r = lp(Ds, M)
        sup = [i for i in range(2, len(Ds)) if r.x[i] > 1e-9] if r.status == 0 else []
        resid = np.abs(sum(r.x[i] * Ds[i] for i in range(len(Ds))) - M).max() if r.status == 0 else float("nan")
        dp = min([min(L.procrustes2(others[i - 2][1], X1), L.procrustes2(others[i - 2][1], X2)) for i in sup], default=float("nan"))
        print(f"| {n} | {inst} | {L.conic_nullity(z)[0]} | {nconv}/600 | {len(found)} | {len(others)} | {r.fun:.6f} | {len(sup)} | {resid:.1e} | {dp:.3f} |", flush=True)
print(f"ALL DONE {time.time() - t0:.1f} s")
