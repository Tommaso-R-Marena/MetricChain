"""Theorem L and Theorem K(c') of docs/geometry/LOCAL_DATA_STABILITY.md, checked on instances.

Theorem L (global upper bound).  X: n points in R^3; windows W_i = (x_i, .., x_{i+3});
P_i = [x_{i+1}-x_i, x_{i+2}-x_i, x_{i+3}-x_i]; tau = min_i sigma_min(P_i), D = max_i sigma_max(P_i),
b = max bond length.  For EVERY configuration Y in R^3 whose squared distances satisfy

    (S)   max over |j-k| <= 4 of | d_jk(Y)^2 - d_jk(X)^2 |  <=  tau^4 / (73 D^2)

there is an isometry g with

    || Y - g X ||_F  <=  6.9 (b / tau^2) n (n+1) || eta ||_2,
    eta = ( d_jk(Y)^2 - d_jk(X)^2 )  over the pairs with |j-k| <= 3.

Theorem K(c') (rigorous lower bound in a tube).  If the points lie within distance rho of the
z-axis with axial coordinates z_i = (i - 1/2) h, then for every set F of pairs
    s_7(R)^2 <= 196 pi^4 rho^2 sum_F |x_j - x_k|^2 / (n L^4),   L = n h.

This script (a) evaluates both sides of Theorem L on perturbations of thick chains and of
helices, including perturbations along the softest mode, and reports the largest ratio
left/right (must be <= 1) and how far from 1 it is; (b) checks that a chain with one window
reflected violates (S) (the hypothesis is not idle); (c) evaluates the tube bound on helices.

Usage: python3 local_data_upper.py [seed]
"""
import sys
import numpy as np
from geomlib import chain
from local_data_bounds import rigidity_matrix


def windows(X):
    return [np.column_stack([X[i + 1] - X[i], X[i + 2] - X[i], X[i + 3] - X[i]]) for i in range(len(X) - 3)]


def thickness(X):
    sv = [np.linalg.svd(P, compute_uv=False) for P in windows(X)]
    return min(s[-1] for s in sv), max(s[0] for s in sv)


def sqd(X, sep):
    n = len(X)
    return {(j, k): float(((X[j] - X[k]) ** 2).sum()) for j in range(n) for k in range(j + 1, min(n, j + sep + 1))}


def d_procrustes(X, Y):
    """min over isometries (reflections allowed) of ||Y - gX||_F."""
    A, B = X - X.mean(0), Y - Y.mean(0)
    s = np.linalg.svd(A.T @ B, compute_uv=False)
    return float(np.sqrt(max(0.0, (A ** 2).sum() + (B ** 2).sum() - 2 * s.sum())))


def theorem_L_sides(X, Y):
    n = len(X)
    tau, D = thickness(X)
    b = max(np.linalg.norm(X[i + 1] - X[i]) for i in range(n - 1))
    dX4, dY4 = sqd(X, 4), sqd(Y, 4)
    S = max(abs(dY4[p] - dX4[p]) for p in dX4) <= tau ** 4 / (73 * D ** 2)
    eta = np.sqrt(sum((dY4[p] - dX4[p]) ** 2 for p in dX4 if p[1] - p[0] <= 3))
    left = d_procrustes(X, Y)
    right = 6.9 * b / tau ** 2 * n * (n + 1) * eta
    return S, left, right, tau, D


def thick_chain(n, rng, theta=np.deg2rad(111.0), lo=0.7, hi=2.4):
    """Random torsions bounded away from 0 and pi, so that all windows are thick."""
    t = rng.uniform(lo, hi, n - 3) * rng.choice([-1, 1], n - 3)
    return chain(n, t, theta=theta), t


def helix(n, tors, theta=np.deg2rad(111.0)):
    return chain(n, np.full(n - 3, tors), theta=theta)


def softest_mode(X, K=4):
    n = len(X)
    edges = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
    R = rigidity_matrix(X, edges)
    _, s, Vt = np.linalg.svd(R)
    return Vt[-7].reshape(n, 3), s[-7]


def helix_axis_frame(X):
    """Axis direction, radius and rise of an exact helix (from three consecutive bonds)."""
    b = np.diff(X, axis=0)
    ax = np.cross(b[1] - b[0], b[2] - b[1])
    ax /= np.linalg.norm(ax)
    h = float(b[0] @ ax)
    if h < 0:
        ax, h = -ax, -h
    # centre of the axis: least squares on the projections orthogonal to ax
    Pp = X - np.outer(X @ ax, ax)
    A = np.column_stack([2 * Pp, np.ones(len(X))])
    sol = np.linalg.lstsq(A, (Pp ** 2).sum(1), rcond=None)[0]
    c = sol[:3] - (sol[:3] @ ax) * ax
    rho = float(np.sqrt(np.mean(((Pp - c) ** 2).sum(1))))
    spread = float(np.std(np.sqrt(((Pp - c) ** 2).sum(1))))
    return ax, h, rho, spread


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    rng = np.random.default_rng(seed)
    ok = True

    print("(a) Theorem L on perturbations (Y is an arbitrary nearby point set, not a chain):")
    worst, used, skipped = 0.0, 0, 0
    best_tight = 0.0
    for trial in range(120):
        n = int(rng.integers(10, 90))
        if trial % 3 == 0:
            X = helix(n, rng.choice([1.0, 1.3, 2.0, -1.7]))
        else:
            X, _ = thick_chain(n, rng)
        tau, D = thickness(X)
        kind = trial % 4
        scale = tau ** 4 / (73 * D ** 2)
        if kind == 0:                                   # random displacement of every point
            V = rng.normal(size=X.shape)
        elif kind == 1:                                 # softest mode of the local rigidity matrix
            V, _ = softest_mode(X)
        elif kind == 2:                                 # smooth bending field
            z = np.linspace(0, 1, n)
            V = np.column_stack([np.cos(np.pi * z), np.sin(2 * np.pi * z), 0 * z]) @ np.linalg.qr(rng.normal(size=(3, 3)))[0]
        else:                                           # change of the torsions (stays a chain)
            V = None
        for amp in (1.0, 0.3, 0.05):
            if V is None:
                Xc, t = thick_chain(n, rng)
                X = Xc
                tau, D = thickness(X)
                scale = tau ** 4 / (73 * D ** 2)
                Y = chain(n, t + amp * scale * 0.2 * rng.normal(size=n - 3) / np.sqrt(n))
            else:
                Y = X + amp * scale * 0.05 * V / np.abs(V).max()
            S, left, right, tau, D = theorem_L_sides(X, Y)
            if not S:
                skipped += 1
                continue
            used += 1
            worst = max(worst, left / right if right > 0 else 0.0)
            if kind == 1:
                best_tight = max(best_tight, left / right)
    print(f"    {used} pairs (X, Y) satisfying (S) ({skipped} skipped): largest left/right = {worst:.4f} (must be <= 1); "
          f"along softest modes the bound is attained up to the factor {1 / best_tight:.0f}")
    ok &= worst <= 1.0 and used > 100

    print("(b) the smallness condition is not idle: reflecting the tail of a chain in the plane of three consecutive atoms")
    X, t = thick_chain(30, rng)
    i = 12
    p0, u, v = X[i + 1], X[i + 2] - X[i + 1], X[i + 3] - X[i + 1]
    nrm = np.cross(u, v)
    nrm /= np.linalg.norm(nrm)
    Y = X.copy()
    Y[i + 4:] = X[i + 4:] - 2 * np.outer((X[i + 4:] - p0) @ nrm, nrm)
    S, left, right, tau, D = theorem_L_sides(X, Y)
    dX3, dY3 = sqd(X, 3), sqd(Y, 3)
    e3 = max(abs(dY3[p] - dX3[p]) for p in dX3)
    dX4, dY4 = sqd(X, 4), sqd(Y, 4)
    e4 = max(abs(dY4[p] - dX4[p]) for p in dX4)
    print(f"    separation <= 3 data unchanged (max |d^2 difference| = {e3:.1e}), separation-4 data change by {e4:.3f} "
          f"> tau^4/(73 D^2) = {tau**4/(73*D**2):.1e}; (S) holds: {S}; d_P(X, Y) = {left:.2f}")
    ok &= (not S) and e3 < 1e-9 and left > 0.5

    print("(c) tube bound on helices (all pairs of sequence separation <= K):")
    for tors, K in ((np.deg2rad(60.0), 4), (np.deg2rad(150.0), 4), (np.deg2rad(60.0), 6)):
        rows = []
        for n in (40, 80, 160):
            X = helix(n, tors)
            ax, h, rho, spread = helix_axis_frame(X)
            edges = [(i, j) for i in range(n) for j in range(i + 1, min(n, i + K + 1))]
            R = rigidity_matrix(X, edges)
            s7 = np.sort(np.linalg.svd(R, compute_uv=False))[6]
            L = n * h
            sumsq = sum(((X[i] - X[j]) ** 2).sum() for i, j in edges)
            bound = np.sqrt(196 * np.pi ** 4 * rho ** 2 * sumsq / (n * L ** 4))
            rows.append((n, s7, bound, spread))
            ok &= s7 <= bound and spread < 1e-8
        tau, D = thickness(helix(40, tors))
        txt = ", ".join(f"n = {n}: s_7 = {s7:.2e} <= {bd:.2e}" for n, s7, bd, _ in rows)
        print(f"    torsion {np.rad2deg(tors):.0f} deg, K = {K}: rise h = {h:.3f}, radius rho = {rho:.3f}, tau = {tau:.3f}, D = {D:.3f}; {txt}; "
              f"n^2 s_7 = {rows[-1][1] * rows[-1][0] ** 2:.1f}, n^2 bound = {rows[-1][2] * rows[-1][0] ** 2:.0f}")
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
