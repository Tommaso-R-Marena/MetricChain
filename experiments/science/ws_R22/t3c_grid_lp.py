#!/usr/bin/env python3
"""R22 Item 3(c), route B (the test the brief prescribes): a linear programme over a GRID of the differing torsions.
Two states of a chain that differ in 1 (control), 2, 3 torsions; segments of at least 6 atoms.
Columns: every conformation in which each shared segment is kept rigid, i.e. re-hinged about the hinge bonds --
INCLUDING the components in which segments are mirrored (the brief's sketch mentions them; a grid over the torsions
alone would be one of 2, 4, 8 components).  Component eps in {+,-}^h, angles on a grid; rho_j = rot(b_j, angle) for +,
rot(b_j, angle) @ (reflection in a plane through b_j) for -.  The two true states are grid nodes.
LP1: minimise the mass on the two true nodes subject to sum c_g D(x_g) = M(mu) (all pairs), c >= 0, sum c = 1.
LP2: minimise the mass within `rad` grid steps of the two true nodes subject to |sum c_g D(x_g) - M(mu)| <= eps entrywise.
Controls: one torsion (LP1 must return 0: competitors exist); two half-turn torsions (LP1 must return 1 - 2 min w,
predicted on paper and found by route A); LP1 restricted to the proper component for comparison.
Run: OMP_NUM_THREADS=1 python3 -B t3c_grid_lp.py > t3c_grid_lp.log
"""
import itertools
import time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack, hstack
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


def setup(n, hinges, steps, N, rng):
    """state 1 random; state 2 = state 1 re-hinged by steps[j] grid steps at hinge j (a torsion change of that angle)"""
    t1 = rng.uniform(-np.pi, np.pi, n - 3)
    X1 = L.chain(t1, COS)
    h = 2 * np.pi / N
    t2 = t1.copy()
    for hj, s in zip(hinges, steps):
        t2[hj] += s * h
    X2 = L.chain(t2, COS)
    b = [X1[hj + 2] - X1[hj + 1] for hj in hinges]
    # reflection planes: through b_j and the next (or previous) hinge direction
    refl = []
    for j in range(len(hinges)):
        other = b[j + 1] if j + 1 < len(hinges) else (b[j - 1] if j > 0 else np.array([0.3, -0.5, 0.8]))
        e = np.cross(b[j], other)
        e /= np.linalg.norm(e)
        refl.append(np.eye(3) - 2 * np.outer(e, e))
    return X1, X2, b, refl, h


def columns(X1, hinges, b, refl, N, h, comps):
    n = len(X1)
    iu = np.array([(i, j) for i in range(n) for j in range(i + 3, n)])
    cols, labels = [], []
    for eps in comps:
        for g in itertools.product(range(N), repeat=len(hinges)):
            rhos = [rot(b[j], g[j] * h) @ (refl[j] if eps[j] < 0 else np.eye(3)) for j in range(len(hinges))]
            D = L.sqdist(rehinge(X1, hinges, rhos))
            cols.append(D[iu[:, 0], iu[:, 1]])
            labels.append((eps, g))
    return np.array(cols).T, labels, iu


def solve(A, bvec, cost, eps=0.0):
    nrow, ncol = A.shape
    ones = np.ones((1, ncol))
    if eps == 0.0:
        r = linprog(cost, A_eq=np.vstack([A, ones]), b_eq=np.concatenate([bvec, [1.0]]), bounds=[(0, None)] * ncol,
                    method="highs", options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9})
    else:
        r = linprog(cost, A_ub=np.vstack([A, -A]), b_ub=np.concatenate([bvec + eps, -bvec + eps]), A_eq=ones, b_eq=[1.0],
                    bounds=[(0, None)] * ncol, method="highs")
    return r


def run(name, n, hinges, steps, N, seed, rad=1, eps_list=(1e-1, 1e-2, 1e-3, 1e-4), all_components=True):
    rng = np.random.default_rng(seed)
    X1, X2, b, refl, h = setup(n, hinges, steps, N, rng)
    k = len(hinges)
    comps = list(itertools.product([1, -1], repeat=k)) if all_components else [tuple([1] * k)]
    A, labels, iu = columns(X1, hinges, b, refl, N, h, comps)
    D1, D2 = L.sqdist(X1), L.sqdist(X2)
    M = W[0] * D1 + W[1] * D2
    bvec = M[iu[:, 0], iu[:, 1]]
    plus = tuple([1] * k)
    i1 = labels.index((plus, tuple([0] * k)))
    i2 = labels.index((plus, tuple(s % N for s in steps)))
    chk = max(np.abs(A[:, i1] - D1[iu[:, 0], iu[:, 1]]).max(), np.abs(A[:, i2] - D2[iu[:, 0], iu[:, 1]]).max())
    cost = np.zeros(A.shape[1])
    cost[[i1, i2]] = 1.0
    r1 = solve(A, bvec, cost)
    out = f"| {name} | {n} | {hinges} | {[round(s * h, 3) for s in steps]} | {N} | {len(comps)} | {A.shape[1]} | {np.linalg.matrix_rank(A, tol=1e-8)} | {chk:.0e} | "
    if r1.status == 0:
        sup = [(labels[i], float(r1.x[i])) for i in np.argsort(-r1.x)[:8] if r1.x[i] > 1e-9 and i not in (i1, i2)]
        resid = np.abs(A @ r1.x - bvec).max()
        out += f"{r1.fun:.6f} | {resid:.0e} | "
    else:
        sup, out = [], out + f"status {r1.status} | | "
    # LP2 with tolerance: mass within rad grid steps of the true nodes (proper component)
    near = np.zeros(A.shape[1])
    for i, (eps_, g) in enumerate(labels):
        if eps_ == plus:
            for tgt in (tuple([0] * k), tuple(s % N for s in steps)):
                if all(min((g[j] - tgt[j]) % N, (tgt[j] - g[j]) % N) <= rad for j in range(k)):
                    near[i] = 1.0
    vals = []
    for eps in eps_list:
        r2 = solve(A, bvec, near, eps)
        vals.append(f"{r2.fun:.4f}" if r2.status == 0 else f"st{r2.status}")
    out += ", ".join(vals) + " |"
    print(out, flush=True)
    return r1.fun if r1.status == 0 else None, sup


print("=== R22 3(c) route B: grid linear programme over all re-hingings (mirrored components included); weights 0.37/0.63; cos(bond angle) = -1/3")
print("LP1 = minimal mass on the two true nodes with EQUAL M;  LP2 = minimal mass within 1 grid step of the true nodes with |M(nu) - M(mu)| <= eps entrywise")
print("| case | n | hinge torsions | torsion differences (rad) | grid N per angle | components | columns | rank of the data map on the columns | true states are grid nodes (err) | "
      "LP1 | LP1 residual | LP2 at eps = 1e-1, 1e-2, 1e-3, 1e-4 |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
res = {}
res["one"] = [run("one torsion (control)", 20, [8], [s], 72, 2220 + i)[0] for i, s in enumerate((17, 29))]
two = []
for i, (n, hinges, steps) in enumerate(((20, [5, 12], (5, 9)), (20, [6, 11], (-7, 4)), (26, [8, 16], (10, -5)), (26, [7, 15], (3, 8)))):
    v, sup = run("two torsions", n, hinges, steps, 24, 2230 + i)
    two.append(v)
res["two"] = two
res["two_proper_only"] = [run("two torsions, proper component only", 20, [5, 12], (5, 9), 24, 2230, all_components=False)[0]]
v, sup = run("two torsions, both half-turns", 20, [5, 12], (12, 12), 24, 2240)
res["half"] = [v]
print("    half-turn case, support of the LP1 optimum besides the true nodes (component, grid node, weight): " + "; ".join(f"{l[0]} {l[1]} {w:.4f}" for l, w in sup))
v, _ = run("two torsions, both half-turns, proper component only", 20, [5, 12], (12, 12), 24, 2240, all_components=False)
res["half_proper_only"] = [v]
three = []
for i, (n, hinges, steps) in enumerate(((26, [5, 12, 19], (3, -4, 5)), (26, [6, 12, 18], (-2, 5, 3)))):
    v, _ = run("three torsions", n, hinges, steps, 12, 2250 + i, eps_list=(1e-1, 1e-2, 1e-3))
    three.append(v)
res["three"] = three
res["three_half"] = [run("three torsions, all half-turns", 26, [5, 12, 19], (6, 6, 6), 12, 2260, eps_list=(1e-1, 1e-2))[0]]
print()
print("--- summary of LP1 (minimal mass on the two true states among grid ensembles with exactly the same M)")
for k_, v in res.items():
    print(f"    {k_:20s}: " + ", ".join("None" if x is None else f"{x:.6f}" for x in v))
ctrl = int(not all(x is not None and x < 1e-6 for x in res["one"])) + int(not (res["half"][0] is not None and abs(res["half"][0] - (1 - 2 * min(W))) < 1e-6))
print(f"control violations (one torsion must give 0; two half-turns must give 1 - 2 min w = {1 - 2 * min(W):.2f}): {ctrl}")
print(f"ALL DONE {time.time() - t0:.1f} s")
