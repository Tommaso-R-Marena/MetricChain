#!/usr/bin/env python3
"""R22 Item 3(c), route A continued: how the answer depends on WHERE the differing torsions sit.
For each arrangement of the differing torsions (K = 2): enumerate the linear images of the stacked pair that are
chains (multi-start LM, as in t3c_linear_images.py), then the linear programme 'minimise the mass on the two true
states subject to equal M'.  Every competitor returned by the programme is VERIFIED directly: largest entry of
sum c_i D(Y_i) - M(mu) over all pairs, bond/1-3 errors of its states, and the squared Procrustes distance (reflections
allowed) of each of its states from the nearer true state.
Arrangements: one torsion (control, must be non-identifiable); (j, j+1); (j, j+2); (j, j+3); (j, j+4);
(j, j+1, j+2); (j, j+1, j+3); (j, j+2, j+4); four torsions two apart.
Run: OMP_NUM_THREADS=1 python3 -B t3c_short_segments.py > t3c_short_segments.log
"""
import time
import numpy as np
from scipy.optimize import least_squares, linprog
import r22lib as L

t0 = time.time()
COS = -1.0 / 3.0
W = (0.37, 0.63)


def enumerate_linear_images(z, nstart, rng, tol=1e-10):
    n, m = z.shape
    Ed = np.array([z[j] - z[i] for i, j in L.E0(n)])
    l2 = (Ed ** 2).sum(1)
    res = lambda a: ((Ed @ a.reshape(3, m).T) ** 2).sum(1) / l2 - 1.0

    def jac(a):
        AE = Ed @ a.reshape(3, m).T
        return (2.0 * AE[:, :, None] * Ed[:, None, :] / l2[:, None, None]).reshape(len(Ed), 3 * m)

    found, nconv = [], 0
    for s in range(nstart):
        a0 = rng.normal(size=3 * m) * rng.uniform(0.3, 2.5)
        sol = least_squares(res, a0, jac=jac, method="lm", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000)
        if np.abs(sol.fun).max() > tol:
            continue
        nconv += 1
        Y = z @ sol.x.reshape(3, m).T
        Dx = L.sqdist(Y)
        for f in found:
            if np.abs(f[0] - Dx).max() < 1e-5:
                break
        else:
            found.append((Dx, Y))
    return found, nconv


def lp(Ds, M, true_idx):
    n = M.shape[0]
    iu = [(i, j) for i in range(n) for j in range(i + 3, n)]
    Aeq = np.array([[D[i, j] for D in Ds] for (i, j) in iu] + [[1.0] * len(Ds)])
    beq = np.array([M[i, j] for (i, j) in iu] + [1.0])
    c = np.zeros(len(Ds))
    c[list(true_idx)] = 1.0
    return linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(Ds), method="highs",
                   options={"primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})


print("=== R22 3(c) route A, arrangements of the differing torsions (K = 2, weights 0.37/0.63, cos(bond angle) = -1/3); seed base 2210")
print("| differing torsions | n | segment sizes (atoms) | affine rank of z | dim N(z) | LM converged/starts | distinct images | "
      "LP min mass on true states | competitor: atoms with weight > 1e-9 | max |sum c D - M| | max E0-length error | min d_P^2 to a true state |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
rows = []
arrangements = [
    ("one torsion (control)", 16, [6]),
    ("j, j+1", 16, [5, 6]), ("j, j+1", 20, [8, 9]),
    ("j, j+2", 16, [5, 7]), ("j, j+2", 20, [7, 9]), ("j, j+2", 26, [10, 12]),
    ("j, j+3", 16, [5, 8]), ("j, j+3", 20, [7, 10]),
    ("j, j+4", 20, [6, 10]),
    ("j, j+1, j+2", 18, [6, 7, 8]), ("j, j+1, j+2", 24, [9, 10, 11]),
    ("j, j+1, j+3", 20, [7, 8, 10]),
    ("j, j+2, j+4", 20, [6, 8, 10]), ("j, j+2, j+4", 26, [9, 11, 13]),
    ("j, j+2, j+5", 22, [6, 8, 11]),
    ("j, j+3, j+6", 22, [6, 9, 12]),
    ("four torsions two apart", 26, [8, 10, 12, 14]),
    ("four consecutive torsions", 24, [8, 9, 10, 11]),
]
nid = {}
for idx, (name, n, hinges) in enumerate(arrangements):
    for rep in range(2):
        rng = np.random.default_rng(2210 + 17 * idx + rep)
        t1 = rng.uniform(-np.pi, np.pi, n - 3)
        t2 = t1.copy()
        for h in hinges:
            t2[h] += rng.uniform(0.5, 2.6) * rng.choice([-1, 1])
        X1, X2 = L.chain(t1, COS), L.chain(t2, COS)
        z = L.stack([X1, X2], W)
        rk = int(np.linalg.matrix_rank(z - z.mean(0), tol=1e-9))
        found, nconv = enumerate_linear_images(z, 500, rng)
        D1, D2 = L.sqdist(X1), L.sqdist(X2)
        M = W[0] * D1 + W[1] * D2
        others = [(D, Y) for (D, Y) in found if min(np.abs(D - D1).max(), np.abs(D - D2).max()) >= 1e-5]
        Ds = [D1, D2] + [D for D, _ in others]
        r = lp(Ds, M, (0, 1))
        bounds = [-1] + hinges + [n - 4]
        seg = [hinges[0] + 3] + [hinges[i + 1] - hinges[i] + 2 for i in range(len(hinges) - 1)] + [n - 1 - hinges[-1]]
        if r.status == 0:
            c = r.x
            sup = [i for i in range(2, len(Ds)) if c[i] > 1e-9]
            resid = np.abs(sum(c[i] * Ds[i] for i in range(len(Ds))) - M).max()
            lerr = max([max(abs(others[i - 2][0][a, b] - D1[a, b]) for a, b in L.E0(n)) for i in sup], default=0.0)
            dp = min([min(L.procrustes2(others[i - 2][1], X1), L.procrustes2(others[i - 2][1], X2)) for i in sup], default=float("nan"))
            print(f"| {name} {hinges} | {n} | {seg} | {rk} | {L.conic_nullity(z)[0]} | {nconv}/500 | {len(found)} | {r.fun:.6f} | {len(sup)} | {resid:.1e} | {lerr:.1e} | {dp:.3f} |")
            nid.setdefault(name, []).append(r.fun)
        else:
            print(f"| {name} {hinges} | {n} | {seg} | {rk} | {L.conic_nullity(z)[0]} | {nconv}/500 | {len(found)} | LP status {r.status} | | | | |")
print()
print("--- summary: LP minimum of the mass on the two true states per arrangement (1 = no competitor among the images found; < 1 = a verified competing ensemble)")
for name, vals in nid.items():
    print(f"    {name:28s}: " + ", ".join(f"{v:.4f}" for v in vals))
ctrl = int(not all(v < 1e-6 for v in nid.get("one torsion (control)", [1.0])))
print(f"control violations (one torsion must give a competitor): {ctrl}")
print(f"ALL DONE {time.time() - t0:.1f} s")
