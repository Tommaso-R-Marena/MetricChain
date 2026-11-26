#!/usr/bin/env python3
"""R22 Item 3(c), the dual side: for two differing torsions the mixture is identifiable but the certificate phi of
Theorem G vanishes on six further conformations (kappa = 0).  Is there ANOTHER certificate that is linear in the data?
Linear programme on the grid of all re-hingings (mirrored components included, as in t3c_grid_lp.py):
    maximise t   subject to   f(x) = c0 + <Lambda, D(x)>,   f(X_1) = f(X_2) = 0,
                              f(x_g) >= t * min_k d_P(x_g, X_k)^2  for every grid conformation x_g,   |Lambda_ij| <= 1.
t* > 0 means: a certificate with quadratic growth exists on the grid, and then for every grid ensemble nu
    int min_k d_P^2 dnu <= (1/t*) <Lambda, M(nu) - M(mu)> <= (||Lambda||_1 / t*) max_ij |M(nu) - M(mu)|_ij.
Controls: one torsion and two half-turn torsions (not identifiable): t* must be 0;
the certificate phi of Theorem G, normalised the same way, must give growth 0 on the two-torsion grid (it vanishes at
the mirrored linear images).
Run: OMP_NUM_THREADS=1 python3 -B t3c_dual_certificate.py > t3c_dual_certificate.log
"""
import itertools
import time
import numpy as np
from scipy.optimize import linprog
import r22lib as L

t0 = time.time()
COS = -1.0 / 3.0
W = (0.37, 0.63)


def rot(axis, ang):
    a = axis / np.linalg.norm(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def rehinge(X1, hinges, rhos):
    X = X1.copy()
    B = np.eye(3)
    for h, rho in zip(hinges, rhos):
        p = h + 1
        B = B @ rho
        X[p:] = X[p] + (X1[p:] - X1[p]) @ B.T
    return X


def run(name, n, hinges, steps, N, seed):
    rng = np.random.default_rng(seed)
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    X1 = L.chain(t1, COS)
    h = 2 * np.pi / N
    t2 = t1.copy()
    for hj, s in zip(hinges, steps):
        t2[hj] += s * h
    X2 = L.chain(t2, COS)
    b = [X1[hj + 2] - X1[hj + 1] for hj in hinges]
    refl = []
    for j in range(len(hinges)):
        other = b[j + 1] if j + 1 < len(hinges) else (b[j - 1] if j > 0 else np.array([0.3, -0.5, 0.8]))
        e = np.cross(b[j], other)
        e /= np.linalg.norm(e)
        refl.append(np.eye(3) - 2 * np.outer(e, e))
    iu = np.array([(i, j) for i in range(n) for j in range(i + 3, n)])
    k = len(hinges)
    rows, d2 = [], []
    for eps in itertools.product([1, -1], repeat=k):
        for g in itertools.product(range(N), repeat=k):
            rhos = [rot(b[j], g[j] * h) @ (refl[j] if eps[j] < 0 else np.eye(3)) for j in range(k)]
            X = rehinge(X1, hinges, rhos)
            rows.append(L.sqdist(X)[iu[:, 0], iu[:, 1]])
            d2.append(min(L.procrustes2(X, X1), L.procrustes2(X, X2)))
    A = np.array(rows)                       # (grid points) x (pairs)
    d2 = np.array(d2)
    D1 = L.sqdist(X1)[iu[:, 0], iu[:, 1]]
    D2 = L.sqdist(X2)[iu[:, 0], iu[:, 1]]
    m = A.shape[1]
    # variables: Lambda (m), c0, t ; maximise t
    cost = np.zeros(m + 2)
    cost[-1] = -1.0
    A_ub = np.hstack([-A, -np.ones((len(A), 1)), d2[:, None]])     # -(f) + t d2 <= 0
    b_ub = np.zeros(len(A))
    A_eq = np.array([np.concatenate([D1, [1.0, 0.0]]), np.concatenate([D2, [1.0, 0.0]])])
    b_eq = np.zeros(2)
    bounds = [(-1, 1)] * m + [(None, None), (0, None)]
    r = linprog(cost, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    tstar = -r.fun if r.status == 0 else float("nan")
    lam = r.x[:m] if r.status == 0 else np.zeros(m)
    # the certificate phi of Theorem G written in the same form: f = -<Pi_perp, D>/2 restricted to pairs, same normalisation
    z = L.stack([X1, X2], W)
    Pp, _ = L.perp_projector(z)
    lam_phi = -Pp[iu[:, 0], iu[:, 1]]        # phi = -1/2 sum_{i != j} Pi_ij D_ij = - sum_{i<j} Pi_ij D_ij ; E0 pairs constant
    lam_phi = lam_phi / np.abs(lam_phi).max()
    f_phi = A @ lam_phi
    f_phi = f_phi - (D1 @ lam_phi)           # shift so that f(X_1) = 0 (then f(X_2) = 0 as well, to rounding)
    far = d2 > 1e-9
    growth_phi = float((f_phi[far] / d2[far]).min())
    chk_phi = abs(D2 @ lam_phi - D1 @ lam_phi)
    cons = float("nan")
    if r.status == 0 and tstar > 1e-9:
        cons = np.abs(lam).sum() / tstar
    print(f"| {name} | {n} | {hinges} | {[round(s * h, 3) for s in steps]} | {len(A)} | {tstar:.4e} | {np.abs(lam).sum():.2f} | {cons:.3e} | "
          f"{growth_phi:.2e} | {chk_phi:.0e} |", flush=True)
    return tstar, growth_phi


print("=== R22: a linear certificate beyond phi for states that share rigid segments (grid of all re-hingings); weights 0.37/0.63")
print("| case | n | hinges | torsion differences (rad) | grid conformations | t* = best quadratic growth of a certificate with |Lambda_ij| <= 1 | "
      "||Lambda||_1 | stability constant ||Lambda||_1 / t* | growth of phi (Theorem G) on the same grid, same normalisation | phi(X_2) - phi(X_1) |")
print("|---|---|---|---|---|---|---|---|---|---|")
res = {}
res["one"] = run("one torsion (control)", 20, [8], [17], 72, 2220)
res["two_a"] = run("two torsions", 20, [5, 12], (5, 9), 24, 2230)
res["two_b"] = run("two torsions", 20, [6, 11], (-7, 4), 24, 2231)
res["two_c"] = run("two torsions", 26, [8, 16], (10, -5), 24, 2232)
res["half"] = run("two half-turns (control)", 20, [5, 12], (12, 12), 24, 2240)
res["three"] = run("three torsions", 26, [5, 12, 19], (3, -4, 5), 12, 2250)
viol = int(res["one"][0] > 1e-7) + int(res["half"][0] > 1e-7) + sum(int(res[k][0] < 1e-6) for k in ("two_a", "two_b", "two_c", "three")) \
    + sum(int(abs(res[k][1]) > 1e-6) for k in ("two_a", "two_b", "two_c"))
print(f"violations (controls must give t* = 0; two and three torsions t* > 0; phi must have growth 0 for two torsions): {viol}")
print(f"ALL DONE {time.time() - t0:.1f} s")
