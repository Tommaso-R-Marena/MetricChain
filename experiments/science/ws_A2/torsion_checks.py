#!/usr/bin/env python3
"""Workstream A2 — independent numerical checks of two chain-geometry statements of the theory report.

(1) C4 / Theorem 4.6(b),(c): for a torsion move by phi (atoms B rotated about an axis, atoms A fixed) the cost of the best
    re-superposition by a rotation about the SAME axis is
        C(phi) = 2S - 2 sqrt(S^2 - 4 I_A I_B sin^2(phi/2)) = 2 (S - |I_A + I_B e^{i phi}|),   S = I_A + I_B,
    (a planar weighted Procrustes residual), and the true Kabsch cost (best proper rotation + translation) is <= C(phi).
    We check: formula vs direct minimisation over psi; Kabsch <= C; 4 I_red sin^2 <= C <= 4 min(I_A,I_B) sin^2.

(2) G16 / Theorem 11.36 (lever-arm law): for a chain with tetrahedral bond angle the reduced moment of inertia about
    the axis of a torsion at distance m from the nearer chain end grows like m^3, so that the per-torsion RMSD constant
    2 sqrt(2 I_red) grows like m^{3/2}.  We compute I_A, I_B for all-trans chains and for regular helices (all torsions
    equal), report sup over these conformations of 2 sqrt(2 I_red) / (b m^{3/2}) and the fitted exponent.

Own code; nothing imported from the repository.
"""
import numpy as np

rng = np.random.default_rng(20261125)


def rot_axis(axis, ang):
    a = axis / np.linalg.norm(axis)
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)


def kabsch_cost(X, Y):
    """min over proper rotations R and translations t of sum |X_i - (R Y_i + t)|^2."""
    Xc = X - X.mean(0)
    Yc = Y - Y.mean(0)
    H = Yc.T @ Xc
    U, s, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    s2 = s.copy()
    s2[-1] *= d
    return (Xc ** 2).sum() + (Yc ** 2).sum() - 2 * s2.sum()


def inertia_about_axis(P, a0, a):
    """sum of squared distances of the rows of P from the line a0 + t a."""
    a = a / np.linalg.norm(a)
    D = P - a0
    par = D @ a
    return ((D ** 2).sum(1) - par ** 2).sum()


def check_c4(trials=20000):
    worst_formula = 0.0
    max_ratio = 0.0
    min_ratio = np.inf
    viol_k = 0
    viol_bounds = 0
    for _ in range(trials):
        nA, nB = rng.integers(1, 12), rng.integers(1, 12)
        a0 = rng.normal(size=3)
        a = rng.normal(size=3)
        a /= np.linalg.norm(a)
        A = rng.normal(size=(nA, 3)) * rng.uniform(0.3, 3)
        B = rng.normal(size=(nB, 3)) * rng.uniform(0.3, 3)
        phi = rng.uniform(-np.pi, np.pi)
        IA, IB = inertia_about_axis(A, a0, a), inertia_about_axis(B, a0, a)
        S = IA + IB
        C = 2 * S - 2 * np.sqrt(max(S * S - 4 * IA * IB * np.sin(phi / 2) ** 2, 0.0))
        # direct minimisation over psi of the coaxial cost
        psi = np.linspace(-np.pi, np.pi, 20001)
        direct = (2 * IA * (1 - np.cos(psi)) + 2 * IB * (1 - np.cos(phi - psi))).min()
        worst_formula = max(worst_formula, abs(direct - C) / (1 + C))
        # complex form
        C2 = 2 * (S - abs(IA + IB * np.exp(1j * phi)))
        worst_formula = max(worst_formula, abs(C2 - C) / (1 + C))
        X = np.vstack([A, B])
        Rphi = rot_axis(a, phi)
        Y = np.vstack([A, (B - a0) @ Rphi.T + a0])
        K = kabsch_cost(X, Y)
        if K > C * (1 + 1e-9) + 1e-9:
            viol_k += 1
        if C > 1e-12:
            max_ratio = max(max_ratio, K / C)
            min_ratio = min(min_ratio, K / C)
        Ired = IA * IB / S
        s2 = np.sin(phi / 2) ** 2
        if not (4 * Ired * s2 <= C * (1 + 1e-9) + 1e-12 and C <= 4 * min(IA, IB) * s2 * (1 + 1e-9) + 1e-12):
            viol_bounds += 1
    print(f"[C4] trials={trials}: max rel. deviation formula vs direct minimisation/complex form = {worst_formula:.2e}")
    print(f"[C4] Kabsch cost > coaxial cost in {viol_k} cases; Kabsch/coaxial ratio in [{min_ratio:.4f}, {max_ratio:.6f}]")
    print(f"[C4] violations of 4 I_red sin^2 <= C <= 4 min(I_A,I_B) sin^2: {viol_bounds}")


def chain(n_atoms, torsions, b=1.0, theta=np.deg2rad(109.4712206)):
    """Chain with unit bonds, bond angle theta, torsions[k] the dihedral of atoms k..k+3 (pi = trans)."""
    X = np.zeros((n_atoms, 3))
    X[1] = [b, 0, 0]
    X[2] = X[1] + b * np.array([-np.cos(theta), np.sin(theta), 0.0])
    for k in range(3, n_atoms):
        p1, p2, p3 = X[k - 3], X[k - 2], X[k - 1]
        bc = p3 - p2
        bc /= np.linalg.norm(bc)
        nrm = np.cross(p2 - p1, bc)
        nrm /= np.linalg.norm(nrm)
        m = np.cross(nrm, bc)
        tor = torsions[k - 3]
        d2 = np.array([-b * np.cos(theta), b * np.sin(theta) * np.cos(tor), b * np.sin(theta) * np.sin(tor)])
        X[k] = p3 + d2[0] * bc + d2[1] * m + d2[2] * nrm
    return X


def lever_arm():
    print("[G16] conformations: regular helices, all torsions = tau (tau = 180 deg is all-trans); N atoms, n = N-3 torsions")
    print("[G16] central torsion i = n/2, m = min(i, n+1-i); ratio = 2 sqrt(2 I_red) / (b m^{3/2}); "
          "ratio_min = 2 sqrt(min(I_A,I_B)) / (b m^{3/2})")
    taus = [180, 170, 150, 120, 90, 60, 30, 0]
    for N in (43, 83, 163, 323, 643, 1283):
        n = N - 3
        i = n // 2  # torsion about bond (i+1, i+2) in 0-based atoms
        m = min(i + 1, n - i)
        best = (0, None)
        best_min = (0, None)
        for tau in taus:
            X = chain(N, [np.deg2rad(tau)] * n)
            a0, a1 = X[i + 1], X[i + 2]
            ax = a1 - a0
            IA = inertia_about_axis(X[: i + 2], a0, ax)
            IB = inertia_about_axis(X[i + 2:], a0, ax)
            Ired = IA * IB / (IA + IB)
            r = 2 * np.sqrt(2 * Ired) / m ** 1.5
            rmin = 2 * np.sqrt(min(IA, IB)) / m ** 1.5
            if r > best[0]:
                best = (r, tau)
            if rmin > best_min[0]:
                best_min = (rmin, tau)
        print(f"[G16] N={N:5d} m={m:4d}: sup ratio = {best[0]:.4f} at tau={best[1]}, "
              f"sup ratio_min = {best_min[0]:.4f} at tau={best_min[1]}")
    # exponent fit for all-trans as a function of the distance m to the end (long chain, positions near one end)
    N = 2003
    n = N - 3
    X = chain(N, [np.pi] * n)
    ms, vals = [], []
    for m in (10, 20, 40, 80, 160, 320, 640):
        i = m - 1
        a0, a1 = X[i + 1], X[i + 2]
        ax = a1 - a0
        IA = inertia_about_axis(X[: i + 2], a0, ax)
        IB = inertia_about_axis(X[i + 2:], a0, ax)
        ms.append(m)
        vals.append(2 * np.sqrt(min(IA, IB)))
    slope = np.polyfit(np.log(ms), np.log(vals), 1)[0]
    print(f"[G16] all-trans, N={N}: 2 sqrt(min(I_A,I_B)) at distance m from the end, m={ms}:")
    print("[G16]   values/m^1.5 =", " ".join(f"{v / m ** 1.5:.4f}" for v, m in zip(vals, ms)), f"; fitted exponent = {slope:.4f}")
    # random-coil comparison: random torsions from {trans, gauche+, gauche-}
    ratios = []
    for rep in range(200):
        N = 403
        n = N - 3
        tors = rng.choice([np.pi, np.pi / 3, -np.pi / 3], size=n)
        X = chain(N, tors)
        i = n // 2
        m = min(i + 1, n - i)
        a0, a1 = X[i + 1], X[i + 2]
        ax = a1 - a0
        IA = inertia_about_axis(X[: i + 2], a0, ax)
        IB = inertia_about_axis(X[i + 2:], a0, ax)
        ratios.append((2 * np.sqrt(min(IA, IB)) / m ** 1.5, 2 * np.sqrt(min(IA, IB)) / m))
    ratios = np.array(ratios)
    print(f"[G16] random rotamer coils (phantom, N=403, m=200, 200 samples): 2 sqrt(min I)/m^1.5 median {np.median(ratios[:,0]):.4f}, "
          f"max {ratios[:,0].max():.4f};  2 sqrt(min I)/m median {np.median(ratios[:,1]):.3f}  (typical coils scale like m, extended ones like m^1.5)")


if __name__ == "__main__":
    check_c4()
    lever_arm()
