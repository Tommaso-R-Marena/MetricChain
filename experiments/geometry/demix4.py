"""DEMIX-4: demixing below the conic threshold by a degree-4 linearisation of the rank conditions
(docs/geometry/ENSEMBLE_RIGIDITY.md, section 6.2, Proposition 6.2).

The method is not ours: it is the algorithm of Johnston, Lovitz and Vijayaraghavan, "Computing
linear sections of varieties" (FOCS 2023, arXiv 2212.03851) -- the first level of the
Nullstellensatz hierarchy -- applied to the subspace L below and the symmetric matrices of
rank at most 3.  Their guarantees are for generic subspaces; L is structured, and this script
is the evidence for where the method works on chains.

Input: the matrix M of ensemble-averaged squared distances and the statewise data (unit bonds,
bond angle).  Let Z be a configuration with D(Z) = M (rank 3K) and

    L = { P in Sym(3K) :  e^T P e = c * l_e^2  for all constrained edge vectors e of Z, some c },

a linear space of dimension m that contains the K block projectors P_k (rank 3) of the states.
Under the conic condition m = K and DEMIX reads the blocks off one element of L.  Below it
m > K, and the states are the points of rank <= 3 of L -- a MinRank problem.  DEMIX-4 treats
the 4 x 4 minors of P(t) = sum_a t_a B_a as LINEAR equations on the quartic forms in t:

  1. J = span of all 4 x 4 minors, as quartic forms on L;   HF = dim Sym^4(L*) - dim J.
     CERTIFICATE:  HF = K.   (Then the points of rank <= 3 of L are exactly the K projectors,
     also over the complex numbers, and the ensemble is identifiable -- Proposition 6.2.)
  2. The annihilator of J in Sym^4(L) is spanned by the fourth powers of the K projectors;
     contracting it with cubic forms gives span{P_1, ..., P_K} inside L.
  3. A generic element of that span has the K blocks as eigenspaces (as in DEMIX).

No monomial basis is used: quartic forms are handled through their values at random points.
Floating point.  Cost: a singular value decomposition of size about C(m+3, 4).  All minors are
used (up to symmetry): a random sample of them does NOT span the same space (for four states
at 38 atoms 30 000 of the 122 760 minors leave HF = 13 instead of 4).

Usage: python3 demix4.py            (K = 2, n = 11 and K = 3, n = 19 ... 22, with checks)
"""
import itertools
import math
import sys
import numpy as np
from geomlib import chain, edm, kabsch_rmsd

THETA = np.deg2rad(111.0)


def stack_from_M(M, tol=1e-9):
    n = len(M)
    J = np.eye(n) - np.ones((n, n)) / n
    G = -0.5 * J @ M @ J
    w, V = np.linalg.eigh(G)
    keep = w > tol * w.max()
    return V[:, keep] * np.sqrt(w[keep])


def space_L(Z, theta=THETA, tol=1e-9):
    n, N = Z.shape
    idx = [(i, j) for i in range(N) for j in range(i, N)]
    E = [Z[i + 1] - Z[i] for i in range(n - 1)] + [Z[i + 2] - Z[i] for i in range(n - 2)]
    ell = [1.0] * (n - 1) + [2 - 2 * np.cos(theta)] * (n - 2)
    A = np.array([[e[i] * e[j] * (1 if i == j else 2) for (i, j) in idx] + [-l] for e, l in zip(E, ell)])
    _, s, Vt = np.linalg.svd(A)
    rank = int((s > tol * s[0]).sum())
    basis = []
    for v in Vt[rank:]:
        S = np.zeros((N, N))
        for t, (i, j) in enumerate(idx):
            S[i, j] = S[j, i] = v[t]
        basis.append(S)
    return np.array(basis)


def demix4(M, theta=THETA, rng=None, max_minors=40000, verbose=False, principal_only=False):
    rng = rng or np.random.default_rng(0)
    Z = stack_from_M(M)
    n, N = Z.shape
    if N % 3:
        return None, {"error": f"rank {N} is not a multiple of 3"}
    K = N // 3
    B = space_L(Z, theta)
    m = len(B)
    nmon = math.comb(m + 3, 4)
    S = nmon + max(30, nmon // 10)
    T = rng.normal(size=(S, m))
    P = np.einsum("sa,aij->sij", T, B)
    combos = list(itertools.combinations(range(N), 4))
    pairs = [(a, b) for ia, a in enumerate(combos) for b in combos[ia:]]
    if principal_only:                    # planted error for the mutation test: principal minors only
        pairs = [(a, a) for a in combos]
    if len(pairs) > max_minors:
        pairs = [pairs[i] for i in rng.choice(len(pairs), max_minors, replace=False)]
    Mat = np.empty((len(pairs), S))
    for r, (a, b) in enumerate(pairs):
        Mat[r] = np.linalg.det(P[:, list(a)][:, :, list(b)])
    Mat = Mat[np.linalg.norm(Mat, axis=1) > 1e-9 * np.abs(Mat).max()]
    _, sv, Vt = np.linalg.svd(Mat, full_matrices=True)
    rank = int((sv > 1e-8 * sv[0]).sum())
    hf = nmon - rank
    info = {"K": K, "n": n, "dim_L": m, "quartic_monomials": nmon, "minors_used": len(Mat), "HF": hf,
            "gap": float(sv[rank - 1] / sv[rank]) if rank < len(sv) else float("inf")}
    if hf != K:
        info["error"] = f"certificate fails: HF = {hf}, not K = {K}"
        return None, info
    # annihilator, represented by coefficient vectors a on the evaluation functionals at the points T
    ker = Vt[rank:]                                   # (S - rank) x S ; contains the (S - nmon)-dim trivial part
    W = []
    for _ in range(3 * K + 6):
        u = rng.normal(size=m)
        cub = (T @ u) ** 3
        W.append((ker * cub) @ T)                     # rows: sum_s a_s (u.t_s)^3 t_s  in L-coordinates
    W = np.vstack(W)
    _, s2, V2 = np.linalg.svd(W, full_matrices=False)
    r2 = int((s2 > 1e-7 * s2[0]).sum())
    info["span_dim"] = r2
    if r2 != K:
        info["error"] = f"the contraction has rank {r2}, not K = {K}"
        return None, info
    span = np.einsum("ja,akl->jkl", V2[:K], B)       # K matrices spanning span{P_k}
    g = rng.normal(size=K)
    Tm = np.einsum("j,jkl->kl", g, span)
    ev, U = np.linalg.eigh(Tm)
    order = np.argsort(ev)
    ev, U = ev[order], U[:, order]
    blocks = [U[:, 3 * k:3 * k + 3] for k in range(K)]
    info["eigen_split"] = float(min(ev[3 * k + 3] - ev[3 * k + 2] for k in range(K - 1)) /
                                max(max(ev[3 * k + 2] - ev[3 * k] for k in range(K)), 1e-300))
    states, weights = [], []
    for Q in blocks:
        Y = Z @ Q
        wk = float(np.mean([np.sum((Y[i + 1] - Y[i]) ** 2) for i in range(n - 1)]))
        weights.append(wk)
        states.append(Y / np.sqrt(wk))
    return (states, weights), info


def demo(K, n, seed, principal_only=False):
    rng = np.random.default_rng(seed)
    w = rng.dirichlet(np.ones(K) * 4)
    Xs = [chain(n, rng.uniform(-np.pi, np.pi, n - 3), theta=THETA) for _ in range(K)]
    M = sum(wk * edm(X) for wk, X in zip(w, Xs))
    out, info = demix4(M, rng=np.random.default_rng(seed + 100), principal_only=principal_only)
    if out is None:
        return False, info, None
    states, weights = out
    err_state, err_w = 0.0, 0.0
    used = set()
    for X, wk in zip(Xs, w):
        d = [kabsch_rmsd(X, Y) for Y in states]
        j = int(np.argmin(d))
        used.add(j)
        err_state = max(err_state, d[j])
        err_w = max(err_w, abs(weights[j] - wk))
    ok = len(used) == K and err_state < 1e-5 and err_w < 1e-6
    return ok, info, (err_state, err_w)


def main():
    ok = True
    conic = {2: 12, 3: 23}
    for K, n in ((2, 11), (3, 22), (3, 21), (3, 20), (3, 19)):
        good, info, errs = demo(K, n, seed=7 * K + n)
        ok &= good
        tail = (f"states recovered to RMSD {errs[0]:.1e}, weights to {errs[1]:.1e}" if errs else info.get("error"))
        print(f"K = {K}, n = {n} (conic threshold {conic[K]}): dim L = {info['dim_L']}, quartic forms "
              f"{info['quartic_monomials']}, HF = {info['HF']}; {tail}   {'OK' if good else 'FAIL'}", flush=True)
    # the certificate must refuse where the rank-3 locus is larger
    good, info, errs = demo(2, 10, seed=3)
    refused = (not good) and info["HF"] == 7
    ok &= refused
    print(f"K = 2, n = 10: HF = {info['HF']} (the two states and the structural point of length 5 at infinity): "
          f"refused   {'OK' if refused else 'FAIL'}")
    print("ALL OK" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
