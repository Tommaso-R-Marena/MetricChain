"""Sharpness of the per-torsion superposition constants of theory report section 4.4 / 11.14
(answer to THY-MSG-0017 section 4, question 1).

(1) Rod model: the exact small-angle Kabsch cost of a single kink of angle phi at position s on
    a straight uniform rod of length L is   phi^2 * s^3 (L-s)^3 / (3 L^3)
    = I_red * phi^2 * (1 - 3x(1-x)),  x = s/L   -- a quarter of the coaxial cost at the middle.
    Checked on discrete all-trans chains.
(2) Worst conformations: maximise over the other torsions the true Kabsch distance (optimal
    superposition by an isometry) of one central torsion move of 120 degrees, for arms of m
    atoms; compare with the verified constant  2 sin(delta/2) sqrt(min(I_A, I_B))  and with
    the asymptote 0.824 b m^{3/2} of theory report Theorem 11.36.
"""
import sys
import numpy as np
from scipy.optimize import minimize
from geomlib import chain

THETA = np.deg2rad(111.0)


def procrustes(X, Y):
    """Frobenius distance after optimal superposition by an isometry (reflections allowed)."""
    A = X - X.mean(0)
    B = Y - Y.mean(0)
    s = np.linalg.svd(A.T @ B, compute_uv=False)
    return np.sqrt(max(0.0, (A ** 2).sum() + (B ** 2).sum() - 2 * s.sum()))


def axial_inertias(X, c):
    """Moments of inertia of the two sides about the axis of torsion c (bond c+1 -> c+2)."""
    a = X[c + 2] - X[c + 1]
    a /= np.linalg.norm(a)
    def I(P):
        r = P - X[c + 1]
        perp = r - np.outer(r @ a, a)
        return (perp ** 2).sum()
    return I(X[:c + 2]), I(X[c + 2:])


def kink_test(n):
    """All-trans chain, small move of the central torsion: true cost against the rod formula."""
    tors = np.full(n - 3, np.pi)
    c = (n - 3) // 2
    X = chain(n, tors, theta=THETA)
    d = 1e-4
    t2 = tors.copy()
    t2[c] += d
    Y = chain(n, t2, theta=THETA)
    true = procrustes(X, Y) / d
    IA, IB = axial_inertias(X, c)
    Ired = IA * IB / (IA + IB)
    return true ** 2 / Ired, true ** 2 / min(IA, IB)


def worst_conformation(m, delta=np.deg2rad(120.0), nstart=30, seed=0):
    n = 2 * m + 2                 # arms of m atoms on each side of the central bond
    c = m - 2                      # torsion about the bond (m-1, m): atoms 0..m-1 | m..2m+1
    rng = np.random.default_rng(seed)
    def dist(t):
        t2 = t.copy()
        t2[c] += delta
        return procrustes(chain(n, t, theta=THETA), chain(n, t2, theta=THETA))
    best = (0, None)
    starts = [np.full(n - 3, np.pi)]
    for g in (np.deg2rad(60), -np.deg2rad(60), np.deg2rad(90), np.deg2rad(120)):
        t = np.full(n - 3, np.pi)
        t[c - 1] = g
        t[c + 1] = g
        starts.append(t)
        t = np.full(n - 3, np.pi)
        t[c - 1] = g
        t[c + 1] = -g
        starts.append(t)
    starts += [rng.uniform(-np.pi, np.pi, n - 3) for _ in range(nstart)]
    for t0 in starts:
        r = minimize(lambda t: -dist(t), t0, method="L-BFGS-B")
        if -r.fun > best[0]:
            best = (-r.fun, r.x)
    t = best[1]
    X = chain(n, t, theta=THETA)
    IA, IB = axial_inertias(X, c)
    verified = 2 * np.sin(delta / 2) * np.sqrt(min(IA, IB))
    return dict(m=m, n=n, true_over_m32=best[0] / m ** 1.5, verified_at_that_conformation_over_m32=verified / m ** 1.5,
                ratio_verified_to_true=verified / best[0],
                all_trans_true_over_m32=dist(np.full(n - 3, np.pi)) / m ** 1.5)


if __name__ == "__main__":
    print("(1) single kink at the middle of an all-trans chain: true small-angle Kabsch cost / (I_red phi^2)  [rod model: 1/4],")
    print("    and / (min(I_A, I_B) phi^2)  [rod model: 1/8]")
    for n in (20, 60, 200, 600):
        a, b = kink_test(n)
        print(f"    n={n:4d}: {a:.4f}   {b:.4f}")
    print("(2) worst conformation for a 120-degree move of the central torsion, arms of m atoms")
    print("    (theory report Theorem 11.36: verified constants -> 0.824 b m^{3/2}; lower bound on valid constants 0.186)")
    for m in (8, 16, 32):
        print("   ", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in worst_conformation(m).items()}, flush=True)
