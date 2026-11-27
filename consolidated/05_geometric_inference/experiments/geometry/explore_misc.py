"""Exploration: (1) K=2,n=9 -- is I still uniquely represented although spurious rank-3 points
exist?  (2) K=3 nonlinear threshold (predicted 14).  (3) n=7 four-dimensional chain: is it an
extreme point of the SDP set (no quadric through its 11 edge directions in R^4)?"""
import sys
import numpy as np
from scipy.optimize import linprog, least_squares
from geomlib import chain, stack, edge_vectors, sym_index, quad_row
from explore_spurious import run

what = sys.argv[1]
if what == "lp":
    for seed in range(6):
        tot, ntrue, nsp, sp, w = run(2, 9, seed, nstart=600)
        K = 2
        true = [np.kron(np.diag([1.0 if j == k else 0.0 for j in range(K)]), np.eye(3)) / w[k] for k in range(K)]
        pts = true + sp
        # all representations  sum_j c_j P_j = I, c >= 0 : maximise the mass on spurious points
        Aeq = np.array([P.flatten() for P in pts]).T
        beq = np.eye(6).flatten()
        c = np.array([0, 0] + [-1.0] * len(sp))
        r = linprog(c, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(pts), method="highs")
        print(f"seed={seed}: spurious={nsp}  LP status={r.status} max spurious mass={-r.fun if r.status==0 else None}")
elif what == "k3":
    for n in (13, 14, 15):
        for seed in range(2):
            tot, ntrue, nsp, sp, w = run(3, n, seed, nstart=500)
            print(f"K=3 n={n} seed={seed}: distinct={tot} true={ntrue}/3 spurious={nsp}", flush=True)
elif what == "4d":
    # random 4D chains with 7 atoms, unit bonds and fixed 1-3 distance: nullity of the quadric system
    rng = np.random.default_rng(0)
    def chain4(n, c2):
        # build by rejection-free construction: bond directions u_a in S^3 with u_a.u_{a+1} = gamma
        gamma = (c2 - 2) / 2.0          # |u_a + u_{a+1}|^2 = 2 + 2 gamma = c2
        U = [rng.normal(size=4)]
        U[0] /= np.linalg.norm(U[0])
        for a in range(1, n - 1):
            v = rng.normal(size=4)
            v -= (v @ U[-1]) * U[-1]
            v /= np.linalg.norm(v)
            U.append(gamma * U[-1] + np.sqrt(1 - gamma ** 2) * v)
        X = np.vstack([np.zeros(4), np.cumsum(U, axis=0)])
        return X
    c2 = 2 - 2 * np.cos(np.deg2rad(111.0))
    for n in (6, 7, 8):
        X = chain4(n, c2)
        E = edge_vectors(X)
        idx = sym_index(4)
        A = np.array([quad_row(e, idx) for e in E])
        s = np.linalg.svd(A, compute_uv=False)
        print(f"4D chain n={n}: {len(E)} edge directions, dim Sym(4)=10, singular values min={s[-1]:.3e} -> nullity {10 - int((s > 1e-9 * s[0]).sum())}")
