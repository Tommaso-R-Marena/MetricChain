import sys
import numpy as np
from scipy.optimize import minimize, least_squares
from geomlib import chain, edm
n = 7
E0 = [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
allF = [(i, j) for i in range(n) for j in range(i + 3, n)]

def stress(X, F, c):
    rhs = np.zeros(3 * n)
    for (i, j), cij in zip(F, c):
        d = X[i] - X[j]; rhs[3*i:3*i+3] += cij * d; rhs[3*j:3*j+3] -= cij * d
    A = np.zeros((3 * n, len(E0)))
    for e, (i, j) in enumerate(E0):
        d = X[i] - X[j]; A[3*i:3*i+3, e] = d; A[3*j:3*j+3, e] = -d
    lam = np.linalg.lstsq(A, rhs, rcond=None)[0]
    Om = np.zeros((n, n))
    for (i, j), l in zip(E0, lam):
        Om[i, i] += l; Om[j, j] += l; Om[i, j] -= l; Om[j, i] -= l
    for (i, j), cij in zip(F, c):
        Om[i, i] -= cij; Om[j, j] -= cij; Om[i, j] += cij; Om[j, i] += cij
    return Om, np.linalg.norm(A @ lam - rhs)

def analyse(seed, ntrial=300, nstart=80):
    rng = np.random.default_rng(seed)
    out = []
    for trial in range(ntrial):
        F = [allF[t] for t in sorted(rng.choice(len(allF), size=5, replace=False))]
        c = rng.normal(size=5)
        H = lambda t: -sum(cij * edm(chain(n, t))[i, j] for (i, j), cij in zip(F, c))
        best = []
        for s in range(nstart):
            r = minimize(H, rng.uniform(-np.pi, np.pi, n - 3), method="BFGS", options=dict(gtol=1e-12))
            r = minimize(H, r.x, method="Nelder-Mead", options=dict(xatol=1e-13, fatol=1e-15, maxiter=4000))
            best.append((r.fun, r.x))
        best.sort(key=lambda p: p[0])
        f0 = best[0][0]
        tops = []
        for f, x in best:
            if f - f0 < 1e-9:
                D = edm(chain(n, x))
                if not any(np.abs(D - D2).max() < 1e-4 for D2 in tops):
                    tops.append(D)
        second = next((f - f0 for f, x in best if f - f0 > 1e-6), None)
        X = chain(n, best[0][1])
        Om, res = stress(X, F, c)
        ev = np.linalg.eigvalsh(Om)
        sv = np.linalg.svd(X - X.mean(0), compute_uv=False)
        scale = np.abs(ev).max()
        neg = ev.min() / scale
        if len(tops) == 1 and sv[2] > 0.15 and neg < -1e-3 and res < 1e-6:
            out.append((F, c, best[0][1], ev, second, sv[2], res))
            print("CANDIDATE", F, np.round(c, 4), "torsions", np.round(best[0][1], 6), "\n   eig(Omega)=", np.round(ev, 6),
                  "gap to next local max", second, "sigma3", round(sv[2], 3), "resid", res, flush=True)
    return out

if __name__ == "__main__":
    cands = analyse(int(sys.argv[1]) if len(sys.argv) > 1 else 0, ntrial=int(sys.argv[2]) if len(sys.argv) > 2 else 120)
    print("number of candidates:", len(cands))
