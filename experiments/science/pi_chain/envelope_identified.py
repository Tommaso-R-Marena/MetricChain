"""Identified sets under a model, a first-order envelope class, and averaged data (PI thread).

Configuration space: torsion patterns x in {t, g+, g-}^n of a diamond-lattice chain, self-avoiding
ones only carry weight under the model mu0 (hard core as known part); the unknown residual g is
defined on all patterns and satisfies |g(x) - g(y)| <= c whenever x, y differ in one torsion
(the theory division's weighted-Hamming envelope; b = beta*c).  In the weights w = exp(-beta g)
the class is the cone  w(y) <= e^b w(x)  for single-torsion neighbours (theory report, remark
after Theorem 11.12), and for a target psi and data E_mu[Phi] = m:

    max / min   sum_x mu0(x) w(x) psi(x)
    s.t.        sum_x mu0(x) w(x) = 1,   sum_x mu0(x) w(x) (Phi(x) - m) = 0,
                w(y) - e^b w(x) <= 0   for all ordered single-torsion neighbour pairs,  w >= 0

(Charnes-Cooper form of the linear-fractional programme).  Solved exactly with HiGHS.
Reported: the identified interval with (i) the envelope only, (ii) data only (model-free),
(iii) both, as a function of b.
"""
from __future__ import annotations
import sys, itertools, json, os, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, vstack, csr_matrix

A_BONDS = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]

def build_pattern(pattern):
    """positions for a torsion pattern in {0:t, 1:g+, 2:g-}^n; returns (positions, self_avoiding)."""
    n = len(pattern)
    pos = [(0, 0, 0)]
    b0 = A_BONDS[0]; pos.append(b0)
    b1 = tuple(-v for v in A_BONDS[1]); pos.append(tuple(pos[1][k] + b1[k] for k in range(3)))
    bonds = [b0, b1]
    for k, s in enumerate(pattern):
        j = k + 3
        sign = 1 if (j - 1) % 2 == 0 else -1
        prev, prev2 = bonds[-1], bonds[-2]
        cands = []
        for a in A_BONDS:
            b = (sign * a[0], sign * a[1], sign * a[2])
            if b == (-prev[0], -prev[1], -prev[2]):
                continue
            cands.append(b)
        trans = [b for b in cands if b == prev2]
        gau = sorted(b for b in cands if b != prev2)
        # orient the two gauche choices by the sign of the triple product (prev2 x prev) . b
        def chir(b):
            cx = (prev2[1]*prev[2]-prev2[2]*prev[1], prev2[2]*prev[0]-prev2[0]*prev[2], prev2[0]*prev[1]-prev2[1]*prev[0])
            return cx[0]*b[0] + cx[1]*b[1] + cx[2]*b[2]
        gau.sort(key=chir)
        b = trans[0] if s == 0 else (gau[1] if s == 1 else gau[0])
        bonds.append(b); pos.append(tuple(pos[-1][k2] + b[k2] for k2 in range(3)))
    return pos, len(set(pos)) == len(pos)

def features(pos):
    N = len(pos)
    P = np.array(pos)
    D = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    iu = np.triu_indices(N, 3)
    d = D[iu]
    prof = [int((d == s).sum()) for s in (3, 8, 11)]
    return prof, int(D[np.triu_indices(N, 1)].sum()), int(D[0, N-1])

def setup(n):
    pats = list(itertools.product(range(3), repeat=n))
    idx = {p: i for i, p in enumerate(pats)}
    M = len(pats)
    sa = np.zeros(M, bool); prof = np.zeros((M, 3)); rg2 = np.zeros(M); ree2 = np.zeros(M); gau = np.zeros(M)
    for i, p in enumerate(pats):
        pos, ok = build_pattern(p)
        sa[i] = ok; gau[i] = sum(1 for s in p if s)
        if ok:
            pr, r, e = features(pos); prof[i] = pr; rg2[i] = r / (n + 3) ** 2; ree2[i] = e
    rows = []; cols = []
    for i, p in enumerate(pats):
        for k in range(n):
            for s in range(3):
                if s != p[k]:
                    q = p[:k] + (s,) + p[k+1:]
                    rows.append(i); cols.append(idx[q])
    return dict(n=n, M=M, sa=sa, prof=prof, rg2=rg2, ree2=ree2, gau=gau,
                nb_from=np.array(rows), nb_to=np.array(cols))

def interval(S, mu0, psi, b=None, Phi=None, m=None):
    M = S["M"]
    A_eq = [mu0[None, :]]; b_eq = [1.0]
    if Phi is not None:
        for k in range(Phi.shape[1]):
            A_eq.append((mu0 * (Phi[:, k] - m[k]))[None, :]); b_eq.append(0.0)
    A_eq = np.vstack(A_eq)
    scale = np.maximum(np.abs(A_eq).max(axis=1), 1e-12)
    A_eq = A_eq / scale[:, None]; b_eq = np.array(b_eq) / scale
    A_ub = None; b_ub = None
    if b is not None:
        E = len(S["nb_from"]); r = np.arange(E)
        A_ub = coo_matrix((np.concatenate([np.ones(E), -np.exp(b) * np.ones(E)]),
                           (np.concatenate([r, r]), np.concatenate([S["nb_to"], S["nb_from"]]))),
                          shape=(E, M)).tocsr()
        b_ub = np.zeros(E)
    out = []
    for sgn in (1.0, -1.0):
        res = linprog(sgn * mu0 * psi, A_ub=A_ub, b_ub=b_ub, A_eq=csr_matrix(A_eq), b_eq=b_eq,
                      bounds=(0, None), method="highs")
        if res.status != 0:
            return None
        out.append(sgn * res.fun)
    return out[0], out[1]

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    S = setup(n)
    sa = S["sa"]
    print(f"n={n}: {S['M']} torsion patterns, {int(sa.sum())} self-avoiding", flush=True)
    model = sa.astype(float); model /= model.sum()                       # the model: athermal chain
    thr = np.quantile(S["rg2"][sa], 0.10)
    targets = {"gauche fraction": S["gau"] / n,
               "end-to-end R2": S["ree2"],
               "P(compact decile)": (sa & (S["rg2"] <= thr)).astype(float)}
    # the truth: attractive chain (weight exp(+c3)), i.e. residual g = -c3/beta ... outside or inside the class
    truths = {"truth = model (athermal)": model,
              "truth = attractive (exp(+0.5*c3))": (lambda w: w / w.sum())(sa * np.exp(0.5 * S["prof"][:, 0]))}
    results = []
    for tname, tr in truths.items():
        print(f"\n--- {tname}")
        for dname, Phi in (("no data", None), ("Rg2", S["rg2"][:, None]), ("three-shell profile", S["prof"])):
            m = None if Phi is None else tr @ Phi
            for sname, psi in targets.items():
                line = f"{dname:20s} {sname:18s} truth {float(tr @ psi):8.4f} |"
                for b in (None, 0.25, 0.5, 1.0, 2.0):
                    if Phi is None and b is None:
                        iv = (float(psi[sa].min()), float(psi[sa].max()))
                    else:
                        iv = interval(S, model, psi, b=b, Phi=Phi, m=m)
                    tag = "class-free" if b is None else f"b={b}"
                    if iv is None:
                        line += f" {tag}: infeasible |"
                    else:
                        line += f" {tag}: [{iv[0]:.4f}, {iv[1]:.4f}] |"
                    results.append(dict(n=n, truth=tname, data=dname, target=sname, b=b,
                                        lo=None if iv is None else iv[0], hi=None if iv is None else iv[1],
                                        truth_value=float(tr @ psi)))
                print(line, flush=True)
    json.dump(results, open(f"envelope_identified_n{n}.json", "w"), indent=1)
