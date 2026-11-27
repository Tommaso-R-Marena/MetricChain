#!/usr/bin/env python3
"""Coordinator's check of the one major finding of workstream R27 (its F1), and of the counterexample of its F2.

Written from the statements in docs/science/workstreams/R27_REPORT.md; it uses none of the referee's code.  It
reads one data file of the referee -- the configurations it stored -- and re-evaluates them with functions
written here.

(A) Stored configurations (experiments/science/ws_R27/item4_worstcase_found.npz): for an idealised trace X and a
    stored configuration Y, the root-mean-square and the largest error of the 4n - 10 distances of sequence
    separation at most 4, and the RMSD after the best rigid motion or reflection.  Claim: configurations that
    fit all local distances to a few tenths of an angstrom lie farther from the trace than its radius of
    gyration.
(B) A chain with one nearly coplanar interior four-point window: the tail reflected in the plane of three
    points changes exactly one squared distance, by 4 h- h+; the ratio  d_P / ||eta||_2  grows like 1/h, while
    the first-order constant 1/(2 mu) stays bounded.  (So no global constant can be 1/(2 mu).)
(C) Corollary L.2 needs the estimate in three dimensions: five points y_i = (x_i, eps w_i) in R^4, w the affine
    dependency of the five points, have ||eta||_2 = O(eps^2) and d_P = eps.

Traces: helix-like = radius 2.3, rise 1.5, 100 degrees per point; strand-like = radius 0.94, rise 3.3, 160
degrees per point (lengths in angstrom).  Run:  python3 -B r27_worstcase_check.py
"""
import math, os, resource, time
import numpy as np

resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, 2 * 1024**3))
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(HERE, "..", "ws_R27", "item4_worstcase_found.npz")


def trace(n, radius, rise, turn_deg):
    t = math.radians(turn_deg) * np.arange(n)
    return np.c_[radius * np.cos(t), radius * np.sin(t), rise * np.arange(n)]


def pairs(n, K=4):
    return [(j, k) for j in range(n) for k in range(j + 1, min(n, j + K + 1))]


def dists(X, P):
    return np.array([np.linalg.norm(X[j] - X[k]) for j, k in P])


def procrustes(X, Y, improper=True):
    """min over rigid motions (and reflections if improper) of ||Y - g X||_F, by the singular value decomposition."""
    Xc, Yc = X - X.mean(0), Y - Y.mean(0)
    U, s, Vt = np.linalg.svd(Xc.T @ Yc)
    best = (Xc**2).sum() + (Yc**2).sum() - 2 * s.sum()
    if not improper and np.linalg.det(U @ Vt) < 0:
        best = (Xc**2).sum() + (Yc**2).sum() - 2 * (s.sum() - 2 * s[-1])
    return math.sqrt(max(best, 0.0))


def rg(X):
    return math.sqrt(((X - X.mean(0))**2).sum() / len(X))


def half_jacobian(X, P):
    """A with eta = 2 A V + O(V^2) for squared distances: row (j,k) has (x_j - x_k) at j and -(x_j - x_k) at k."""
    n = len(X)
    A = np.zeros((len(P), 3 * n))
    for r, (j, k) in enumerate(P):
        d = X[j] - X[k]
        A[r, 3 * j:3 * j + 3] = d
        A[r, 3 * k:3 * k + 3] = -d
    return A


def main():
    print("r27_worstcase_check.py   started", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    bad = 0
    # ---------------- (A)
    data = np.load(NPZ, allow_pickle=False)
    print("(A) stored configurations of the referee, re-evaluated here")
    print("    case | rms distance error | largest | RMSD (reflections allowed) | radius of gyration of the trace | farther than it?")
    expect = {"helix-like n=20|0.3": (0.3000, 1.116, 9.950), "helix-like n=12|0.5": (0.5000, 1.172, 6.354),
              "strand-like 160 n=20|0.1": (0.1000, 0.338, 12.002), "strand-like 160 n=20|0.2": (0.2000, 0.488, 18.620),
              "helix-like n=20|0.1": (0.1000, 0.279, 0.907)}
    for key, (e_rms, e_max, e_rmsd) in expect.items():
        Y = data[key]
        n = len(Y)
        X = trace(n, 2.3, 1.5, 100.0) if key.startswith("helix") else trace(n, 0.94, 3.3, 160.0)
        P = pairs(n)
        assert len(P) == 4 * n - 10
        err = dists(Y, P) - dists(X, P)
        rms, mx = math.sqrt((err**2).mean()), np.abs(err).max()
        rmsd = procrustes(X, Y) / math.sqrt(n)
        ok = abs(rms - e_rms) < 6e-4 and abs(mx - e_max) < 6e-3 and abs(rmsd - e_rmsd) < 6e-3
        bad += int(not ok)
        print(f"    {key:26s} | {rms:.4f} | {mx:.3f} | {rmsd:7.3f} | {rg(X):6.2f} | {'yes' if rmsd > rg(X) else 'no'}"
              f"   [referee's log: {e_rms:.4f}, {e_max:.3f}, {e_rmsd:.3f}; agrees: {ok}]")
    # control: the trace against itself, and against its mirror image
    X = trace(20, 2.3, 1.5, 100.0)
    M = X * np.array([1.0, 1.0, -1.0])
    c1, c2, c3 = procrustes(X, X), procrustes(X, M, improper=True), procrustes(X, M, improper=False)
    print(f"    controls: trace against itself {c1:.1e}; against its mirror image with reflections {c2:.1e}, without {c3 / math.sqrt(20):.3f} (must be > 0)")
    bad += int(c1 > 1e-9) + int(c2 > 1e-9) + int(c3 < 1e-3)

    # ---------------- (B)
    print("(B) one nearly coplanar interior window: the reflected tail")
    rng = np.random.default_rng(27)
    n, i0 = 12, 4                       # window points i0+1, i0+2, i0+3 define the plane; i0+4 is put at height h
    b = rng.normal(size=(n - 1, 3))
    b /= np.linalg.norm(b, axis=1)[:, None]
    base = np.vstack([np.zeros(3), np.cumsum(b, axis=0)])
    P = pairs(n)
    rows = []
    for h in (0.1, 0.01, 0.001, 0.0001):
        X = base.copy()
        p1, p2, p3 = X[i0 + 1], X[i0 + 2], X[i0 + 3]
        nrm = np.cross(p2 - p1, p3 - p1)
        nrm /= np.linalg.norm(nrm)
        # move the tail (points i0+4 ...) rigidly so that x_{i0+4} is at signed height h over the plane
        shift = (h - (X[i0 + 4] - p1) @ nrm) * nrm
        X[i0 + 4:] += shift
        hm = (X[i0] - p1) @ nrm                              # height of the point before the window
        Y = X.copy()
        tail = X[i0 + 4:] - p1
        Y[i0 + 4:] = p1 + tail - 2 * np.outer(tail @ nrm, nrm)   # reflect the tail in the plane
        eta = dists(Y, P)**2 - dists(X, P)**2
        changed = int((np.abs(eta) > 1e-9).sum())
        dP = procrustes(X, Y)
        sv = np.linalg.svd(half_jacobian(X, P), compute_uv=False)
        mu = sv[3 * n - 7]                                   # the (3n-6)-th singular value
        rows.append((h, changed, np.linalg.norm(eta), abs(4 * hm * h), dP, dP / np.linalg.norm(eta), 1 / (2 * mu)))
        print(f"    h = {h:7.4f}: squared distances changed {changed} (of {len(P)}); ||eta||_2 = {np.linalg.norm(eta):.3e}, 4|h- h+| = {abs(4*hm*h):.3e};"
              f" d_P = {dP:.3f}; d_P/||eta||_2 = {dP/np.linalg.norm(eta):10.2f}; 1/(2 mu) = {1/(2*mu):.3f}")
    ratios = [rows[i + 1][5] / rows[i][5] for i in range(3)]
    mus = [r[6] for r in rows]
    print(f"    growth of the ratio per decade of h: {ratios[0]:.2f}, {ratios[1]:.2f}, {ratios[2]:.2f} (1/h law: 10);  1/(2 mu) between {min(mus):.3f} and {max(mus):.3f}")
    bad += int(any(r[1] != 1 for r in rows)) + int(any(abs(r[2] / r[3] - 1) > 1e-6 for r in rows))
    bad += int(any(abs(q - 10) > 1.0 for q in ratios)) + int(max(mus) / min(mus) > 1.5)

    # ---------------- (C)
    print("(C) five points of the helix-like trace lifted to four dimensions along their affine dependency")
    X5 = trace(5, 2.3, 1.5, 100.0)
    Mx = np.vstack([np.ones(5), X5.T])                       # 4 x 5; its null vector is the affine dependency
    w = np.linalg.svd(Mx)[2][-1]
    w /= np.linalg.norm(w)
    P5 = pairs(5)
    for eps in (0.1, 0.01, 0.001):
        X4 = np.c_[X5, np.zeros(5)]
        Y4 = np.c_[X5, eps * w]
        eta = dists(Y4, P5)**2 - dists(X4, P5)**2
        Xc, Yc = X4 - X4.mean(0), Y4 - Y4.mean(0)
        s = np.linalg.svd(Xc.T @ Yc, compute_uv=False)
        dP = math.sqrt(max((Xc**2).sum() + (Yc**2).sum() - 2 * s.sum(), 0.0))     # reflections allowed in R^4
        print(f"    eps = {eps}: ||eta||_2 = {np.linalg.norm(eta):.3e} = {np.linalg.norm(eta)/eps**2:.3f} eps^2; d_P = {dP:.3e} = {dP/eps:.4f} eps; d_P/||eta||_2 = {dP/np.linalg.norm(eta)*eps:.3f}/eps")
        bad += int(abs(dP / eps - 1) > 1e-6)
    print(f"statements that must hold and did not: {bad}")
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    print(f"ALL DONE   computed in {time.time() - T0:.1f} s   peak memory {peak:.0f} MB")
    assert bad == 0


if __name__ == "__main__":
    main()
