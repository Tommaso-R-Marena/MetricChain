#!/usr/bin/env python3
"""R22 Item 4, point (4): what another observable changes.  ONE differing torsion is never identified by the mean
SQUARED distances (the control of t3c_*).  Add the mean FOURTH powers <d_ij^4> (the second moments of the squared
distances): on the hinge circle d^4 = (a + b cos + c sin)^2 has harmonics up to 2, and the trigonometric moment
curve of order 2 is 2-neighbourly (Caratheodory), so a two-point mixture should become identifiable.
Because <d^2> is still part of the data, Lemma 2.2 still confines every competitor to the linear images of z, i.e.
to the re-hingings (rotations AND reflections about the hinge), so a programme over the two circles is complete up to
the grid.  LP1: minimal mass on the two true nodes with equal data; LP2: minimal mass within 15 grid steps (15 degrees, the window of t3c_grid_lp.py)
with |data difference| <= eps (relative to the largest entry).  Control: the same programme with <d^2> only (must
return 0).
Run: OMP_NUM_THREADS=1 python3 -B t4_fourth_moment.py > t4_fourth_moment.log
"""
import time
import numpy as np
from scipy.optimize import linprog
import r22lib as L

t0 = time.time(); COS = -1.0 / 3.0; W = (0.37, 0.63); N = 360


def rot(axis, ang):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def solve(A, b, cost, eps=0.0):
    ncol = A.shape[1]; ones = np.ones((1, ncol))
    if eps == 0.0:
        return linprog(cost, A_eq=np.vstack([A, ones]), b_eq=np.concatenate([b, [1.0]]), bounds=[(0, None)] * ncol, method="highs",
                       options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9})
    return linprog(cost, A_ub=np.vstack([A, -A]), b_ub=np.concatenate([b + eps, -b + eps]), A_eq=ones, b_eq=[1.0],
                   bounds=[(0, None)] * ncol, method="highs")


print("=== R22: one differing torsion, data <d^2> alone (control) and <d^2> with <d^4>; grid of 360 angles on each of the two circles (rotations, reflections)")
print("| n | hinge | torsion difference (deg) | data | rank of the data map on the 720 columns | LP1: minimal mass on the two true states | LP2 at eps = 1e-3, 1e-4, 1e-5 (relative) |")
print("|---|---|---|---|---|---|---|")
viol = 0
for i, (n, h, step) in enumerate(((16, 6, 77), (20, 9, 131), (26, 11, 203))):
    rng = np.random.default_rng(2300 + i)
    t1 = rng.uniform(-np.pi, np.pi, n - 3); X1 = L.chain(t1, COS)
    b = X1[h + 2] - X1[h + 1]; e = np.cross(b, np.array([0.3, -0.5, 0.8])); e /= np.linalg.norm(e); S = np.eye(3) - 2 * np.outer(e, e)
    iu = np.array([(a, c) for a in range(n) for c in range(a + 3, n)])
    cols2, cols4, lab = [], [], []
    for refl in (0, 1):
        for g in range(N):
            B = rot(b, 2 * np.pi * g / N) @ (S if refl else np.eye(3))
            X = X1.copy(); X[h + 1:] = X[h + 1] + (X1[h + 1:] - X1[h + 1]) @ B.T
            D = L.sqdist(X)[iu[:, 0], iu[:, 1]]
            cols2.append(D); cols4.append(D ** 2); lab.append((refl, g))
    A2, A4 = np.array(cols2).T, np.array(cols4).T
    i1, i2 = lab.index((0, 0)), lab.index((0, step))
    cost = np.zeros(2 * N); cost[[i1, i2]] = 1.0
    near = np.zeros(2 * N)
    for j, (refl, g) in enumerate(lab):
        if refl == 0 and min(min((g - t) % N, (t - g) % N) for t in (0, step)) <= 15:
            near[j] = 1.0
    for name, A in (("<d^2> (control)", A2), ("<d^2> and <d^4>", np.vstack([A2, A4]))):
        bvec = W[0] * A[:, i1] + W[1] * A[:, i2]
        r1 = solve(A, bvec, cost)
        sc = np.abs(bvec).max()
        v2 = [solve(A, bvec, near, eps * sc).fun for eps in (1e-3, 1e-4, 1e-5)]
        print(f"| {n} | {h} | {step} | {name} | {np.linalg.matrix_rank(A, tol=1e-8)} | {r1.fun:.6f} | " + ", ".join(f"{v:.4f}" for v in v2) + " |", flush=True)
        if "control" in name:
            viol += int(r1.fun > 1e-7)
        else:
            viol += int(abs(r1.fun - 1.0) > 1e-6)
print(f"violations (control must give 0; with <d^4> the prediction is 1): {viol}")
print(f"ALL DONE {time.time() - t0:.1f} s")
