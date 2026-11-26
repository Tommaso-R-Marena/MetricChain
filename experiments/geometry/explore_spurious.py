"""Exploration: for a 2-state ensemble with n atoms, search for 3D chains that are linear
images of the stacked configuration z (i.e. P = A^T A in I + N(z), PSD, rank <= 3) other
than the two true states.  Their absence (plus Theorem B') means identifiability among all
ensembles."""
import sys
import numpy as np
from scipy.optimize import least_squares
from geomlib import chain, stack, edge_vectors

def run(K, n, seed, nstart=400, tol=1e-18):
    rng = np.random.default_rng(seed)
    w = rng.dirichlet(np.ones(K) * 3)
    Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3)) for _ in range(K)]
    Z = stack(Xs, w)
    E = np.array(edge_vectors(Z))
    L2 = (E ** 2).sum(1)
    m = 3 * K
    def res(a):
        A = a.reshape(3, m)
        return ((E @ A.T) ** 2).sum(1) - L2
    sols = []
    for s in range(nstart):
        a0 = rng.normal(size=3 * m) * rng.uniform(0.3, 2.0)
        r = least_squares(res, a0, method="trf", xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        if (r.fun ** 2).sum() < tol:
            A = r.x.reshape(3, m)
            P = A.T @ A
            if not any(np.linalg.norm(P - Q) < 1e-5 for Q in sols):
                sols.append(P)
    true = [np.kron(np.diag([1.0 if j == k else 0.0 for j in range(K)]), np.eye(3)) / w[k] for k in range(K)]
    ntrue = sum(any(np.linalg.norm(P - T) < 1e-4 for P in sols) for T in true)
    spurious = [P for P in sols if not any(np.linalg.norm(P - T) < 1e-4 for T in true)]
    return len(sols), ntrue, len(spurious), spurious, w

if __name__ == "__main__":
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    for n in [int(x) for x in sys.argv[2:]] or [9, 10, 11, 12]:
        for seed in range(4):
            tot, ntrue, nsp, sp, w = run(K, n, seed)
            extra = ""
            if nsp and nsp < 30:
                extra = " spurious eig ranks: " + str([int((np.linalg.eigvalsh(P) > 1e-7).sum()) for P in sp])
            print(f"K={K} n={n} seed={seed}: distinct solutions={tot} (true found {ntrue}/{K}), spurious={nsp}{extra}", flush=True)
