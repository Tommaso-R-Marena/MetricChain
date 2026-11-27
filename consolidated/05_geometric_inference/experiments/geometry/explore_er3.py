"""Exploration (O-3): second-moment rigid but not universally rigid?  Inverse construction.

For a 7-atom chain X and a set F of 5 measured pairs the framework (F u E0, X) has
16 = 3*7 - 6 + 1 bars and a one-dimensional space of equilibrium stresses omega, with stress
matrix Omega.  X is a critical point on the chain variety of H_c = sum_F c_ij |x_i - x_j|^2 with
c = s * omega|_F, and the constrained Hessian on the flexes is 2 s tr(V^T Omega V).
We look for instances where Omega is INDEFINITE (so no positive semidefinite stress: the
framework is not universally rigid, generically) while the Hessian form is DEFINITE on the
four-dimensional flex space (X is a strict local maximiser in R^3 for the right sign s), and
then test by multi-start whether X is the global maximiser over the 4-torus (then D_F(X) is an
exposed point of the realizable set and X is second-moment rigid on F)."""
import sys
import numpy as np
from scipy.optimize import minimize
from geomlib import chain, edm

n = 7
E0 = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
allF = [(i, j) for i in range(n) for j in range(i + 3, n)]


def stress(X, edges):
    R = np.zeros((len(edges), 3 * n))
    for e, (i, j) in enumerate(edges):
        R[e, 3 * i:3 * i + 3] = X[i] - X[j]
        R[e, 3 * j:3 * j + 3] = X[j] - X[i]
    U, s, Vt = np.linalg.svd(R.T)
    om = Vt[-1]
    Om = np.zeros((n, n))
    for w, (i, j) in zip(om, edges):
        Om[i, i] += w; Om[j, j] += w; Om[i, j] -= w; Om[j, i] -= w
    return om, Om, s


def flexes(X):
    T = []
    for m in range(n - 3):
        ax = X[m + 2] - X[m + 1]
        ax /= np.linalg.norm(ax)
        V = np.zeros((n, 3))
        V[m + 3:] = np.cross(ax, X[m + 3:] - X[m + 2])
        T.append(V)
    return T


def search(seed, trials):
    rng = np.random.default_rng(seed)
    found = []
    for t in range(trials):
        tors = rng.uniform(-np.pi, np.pi, n - 3)
        X = chain(n, tors)
        F = [allF[k] for k in sorted(rng.choice(len(allF), size=5, replace=False))]
        om, Om, sv = stress(X, E0 + F)
        if sv[-2] < 1e-6:            # stress space of dimension > 1
            continue
        ev = np.linalg.eigvalsh(Om)
        scale = np.abs(ev).max()
        pos, neg = (ev > 1e-8 * scale).sum(), (ev < -1e-8 * scale).sum()
        if pos + neg != 3 or pos == 0 or neg == 0:
            continue                  # semidefinite (universally rigid candidate) or rank-deficient
        T = flexes(X)
        Hq = np.array([[np.trace(a.T @ Om @ b) for b in T] for a in T])
        hv = np.linalg.eigvalsh((Hq + Hq.T) / 2)
        if hv.min() > 1e-6 * scale:
            s = -1.0
        elif hv.max() < -1e-6 * scale:
            s = 1.0
        else:
            continue                  # saddle in R^3
        c = s * om[len(E0):]
        H = lambda tt: -sum(cij * edm(chain(n, tt))[i, j] for (i, j), cij in zip(F, c))
        h0 = H(tors)
        better = 0
        for _ in range(60):
            r = minimize(H, rng.uniform(-np.pi, np.pi, n - 3), method="BFGS")
            if r.fun < h0 - 1e-7:
                better += 1
                break
        found.append((t, F, tors, ev / scale, hv / scale, better == 0))
        print(f"trial {t}: F={F} stress eig (normalised) {np.round(ev[np.abs(ev) > 1e-8 * scale] / scale, 3)} "
              f"flex Hessian eig {np.round(s * hv / scale, 4)}  strict local max in R^3; GLOBAL max: {better == 0}", flush=True)
        if better == 0:
            print("   torsions:", repr(tors.tolist()), " couplings c:", repr(c.tolist()))
    return found


if __name__ == "__main__":
    f = search(int(sys.argv[1]) if len(sys.argv) > 1 else 0, int(sys.argv[2]) if len(sys.argv) > 2 else 3000)
    print("strict local maxima with indefinite stress:", len(f), " of which global:", sum(1 for x in f if x[-1]))
