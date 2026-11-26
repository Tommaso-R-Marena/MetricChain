"""(k) Is Theorem F (stress certificate) non-vacuous for K >= 2 with INCOMPLETE data?
The report gives no instance.  For a 2-state ensemble (n atoms) and a pair set F we look for
    Omega >= 0,  Omega 1 = 0,  Omega z = 0,  Omega_ij = 0 off F u E0,  rank Omega = n - 7
by a semidefinite programme:  Omega = V W V^T  (V = orthonormal basis of the complement of
span(1, z)),  maximise lambda_min(W)  s.t.  (V W V^T)_ij = 0 on unmeasured pairs,  tr W = n - 7.
lambda_min(W) > 0  <=>  certificate exists.
"""
import sys
import numpy as np
import cvxpy as cp
from mylib import build_chain, sqdist, stack, e0_pairs, conic_system, nullspace


def run(n, w_band=None, extra_random=None, seed=0, K=2, verbose=True):
    rng = np.random.default_rng(300 + seed)
    bonds = np.ones(n - 1)
    alphas = np.full(n - 2, np.pi - np.deg2rad(97.0))
    w = rng.dirichlet(np.ones(K) * 4)
    Xs = [build_chain(rng.uniform(-np.pi, np.pi, n - 3), bonds, alphas) for _ in range(K)]
    Z = stack(Xs, w)
    m = 3 * K
    dim = m * (m + 1) // 2
    nulN = dim - nullspace(conic_system(Z, e0_pairs(n)), dim)[2]
    B = np.hstack([np.ones((n, 1)), Z])
    Q, _ = np.linalg.qr(B, mode="complete")
    V = Q[:, m + 1:]                                   # n x (n - m - 1)
    r = n - m - 1
    E0 = set(e0_pairs(n))
    allp = [(i, j) for i in range(n) for j in range(i + 1, n)]
    if w_band is not None:
        Fset = {(i, j) for (i, j) in allp if 3 <= j - i <= w_band}
        label = f"band 3 <= |i-j| <= {w_band}"
    else:
        free = [p for p in allp if p not in E0]
        idx = rng.choice(len(free), size=extra_random, replace=False)
        Fset = {free[t] for t in idx}
        label = f"{extra_random} random pairs"
    unmeasured = [p for p in allp if p not in E0 and p not in Fset]
    W = cp.Variable((r, r), symmetric=True)
    t = cp.Variable()
    cons = [W - t * np.eye(r) >> 0, cp.trace(W) == r]
    for (i, j) in unmeasured:
        cons.append(V[i] @ W @ V[j] == 0)
    prob = cp.Problem(cp.Maximize(t), cons)
    try:
        prob.solve(solver=cp.CLARABEL)
    except Exception as e:
        prob.solve(solver=cp.SCS, eps=1e-9)
    val = prob.value
    # affine independence of the restricted D(X_k) on F (hypothesis of Theorem F)
    Dk = [np.array([sqdist(X)[i, j] for (i, j) in sorted(Fset)]) for X in Xs]
    aff = np.linalg.norm(Dk[0] - Dk[1])
    if verbose:
        print(f"n={n} K={K} seed={seed}: dim N(z)={nulN} (CC: {nulN == K-1}); F = {label}: |F|={len(Fset)}, unmeasured={len(unmeasured)}, "
              f"dim Sym({r})={r*(r+1)//2}; SDP status {prob.status}; max lambda_min(W) = {val if val is None else round(float(val), 6)} "
              f"-> certificate {'EXISTS' if val is not None and val > 1e-6 else 'does not exist'}; ||D(X_1)-D(X_2)||_F on F = {aff:.2f}")
    if val is not None and val > 1e-6:
        Om = V @ W.value @ V.T
        ev = np.linalg.eigvalsh(Om)
        off = max(abs(Om[i, j]) for (i, j) in unmeasured) if unmeasured else 0.0
        print(f"     check: eigenvalues of Omega: {np.round(ev[:m+2], 8).tolist()} ... (kernel dim {int((ev < 1e-7).sum())} = 3K+1 = {m+1}); "
              f"max |Omega_ij| on unmeasured pairs {off:.1e}; |Omega 1| {np.abs(Om.sum(1)).max():.1e}; |Omega z| {np.abs(Om @ Z).max():.1e}")
    return val


if __name__ == "__main__":
    for n in (14, 16):
        for wb in (5, 6, 7, 8):
            run(n, w_band=wb)
    for cnt in (30, 39, 45, 55):
        run(14, extra_random=cnt)
