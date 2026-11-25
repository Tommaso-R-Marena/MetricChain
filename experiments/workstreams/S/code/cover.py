#!/usr/bin/env python3
"""Covering numbers of the profile format from class tables (own implementation).

Instance: classes (h, gmin); a centre class a covers a client class y iff  L ||N^a - N^y||_1 <= e gmin(y) + eps,
where ||N^a - N^y||_1 = 5|dc1| + 3|dc2| + |dc3| is the L1 distance of the CUMULATIVE profiles
(c1 = h3, c2 = h3+h8, c3 = h3+h8+h11; cell widths 8-3, 11-8, 12-11), e = 1.
(NORM=w on the command line switches to 9|dh3| + 4|dh8| + |dh11|, which is only an upper bound for it.)  N_cov = minimum number of centres (set cover), solved with
dominance reductions and scipy's MILP (HiGHS); the returned pair is (lower bound, size of a verified cover).

usage: cover.py walk|bridge N Lnum Lden EPSnum EPSden [timelimit] [NORM=c|w]     (eps = EPSnum/EPSden * N)
"""
import sys, os
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix

HERE = os.path.dirname(os.path.abspath(__file__))
W = np.array([9, 4, 1])

def load(kind, N):
    H, G = [], []
    if kind == "walk":
        p = f"{HERE}/../eng_data/experiments/eng/chain_cover/data/dia_Sc12_n{N-3}.txt"
        for line in open(p):
            if line.startswith('#'): continue
            a = list(map(int, line.split())); H.append(a[:3]); G.append(a[4])
    else:
        p = f"{HERE}/../out/{kind}_N{N}.txt"
        for line in open(p):
            if line.startswith('#'): continue
            a = line.split(); H.append([int(a[0]), int(a[1]), int(a[2])]); G.append(int(a[4]))
    return np.array(H), np.array(G)

def dist_matrix(H, norm="c"):
    if norm == "w":
        return (np.abs(H[:, None, :] - H[None, :, :]) * W).sum(axis=2)
    Cm = np.cumsum(H, axis=1)
    return (np.abs(Cm[:, None, :] - Cm[None, :, :]) * np.array([5, 3, 1])).sum(axis=2)

def cover_matrix(H, G, L, eps, norm="c"):
    """C[a, y] = centre a covers client y; exact integer arithmetic"""
    den = L.denominator * eps.denominator
    Ls = int(L * den); es = int(eps * den)
    D = dist_matrix(H, norm)                                             # D[a, y]
    return Ls * D <= den * G[None, :] + es

def solve_cover(C, timelimit=120):
    k = C.shape[0]
    clients = np.arange(k); centres = np.arange(k)
    # client reduction: drop y if some other client y' has cov(y') subset of cov(y)
    Cf = C.astype(np.float32)
    M = (1 - Cf).T @ Cf                      # M[y, y'] = #centres covering y' but not y
    np.fill_diagonal(M, 1)
    keep = np.ones(k, bool)
    order = np.argsort(C.sum(axis=0))        # clients with few covering centres first
    for y in order[::-1]:                    # try to drop clients with many covering centres
        idx = np.where(keep)[0]
        dom = idx[(M[y, idx] == 0) & (idx != y)]
        if len(dom): keep[y] = False
    clients = np.where(keep)[0]
    C2 = C[:, clients]
    # centre reduction: drop a if some other centre a' covers a superset
    C2f = C2.astype(np.float32)
    Mc = C2f @ (1 - C2f).T                   # Mc[a, a'] = #clients covered by a but not by a'
    np.fill_diagonal(Mc, 1)
    keepc = np.ones(k, bool)
    for a in np.argsort(C2.sum(axis=1)):
        idx = np.where(keepc)[0]
        dom = idx[(Mc[a, idx] == 0) & (idx != a)]
        if len(dom): keepc[a] = False
    centres = np.where(keepc)[0]
    C3 = C2[centres, :]
    nA, nY = C3.shape
    res = milp(c=np.ones(nA), constraints=LinearConstraint(csr_matrix(C3.T.astype(float)), lb=np.ones(nY), ub=np.inf),
               integrality=np.ones(nA), bounds=Bounds(0, 1), options={"time_limit": timelimit, "mip_rel_gap": 0})
    if res.x is None:
        return None, None, (nA, nY)
    x = res.x > 0.5
    chosen = centres[x]
    assert C[chosen, :].any(axis=0).all(), "not a cover of the unreduced instance"
    lb = int(np.ceil(res.mip_dual_bound - 1e-6)) if res.mip_dual_bound is not None else None
    return lb, len(chosen), (nA, nY)

def main():
    kind = sys.argv[1]; N = int(sys.argv[2])
    L = Fr(int(sys.argv[3]), int(sys.argv[4])); e1 = Fr(int(sys.argv[5]), int(sys.argv[6]))
    tl = float(sys.argv[7]) if len(sys.argv) > 7 else 120
    norm = sys.argv[8] if len(sys.argv) > 8 else "c"
    H, G = load(kind, N)
    C = cover_matrix(H, G, L, e1 * N, norm)
    lb, ub, red = solve_cover(C, tl)
    print(f"{kind} N={N} classes={len(H)} L={L} eps={e1}*N norm={norm}: N_cov in [{lb}, {ub}]   (reduced instance: {red[0]} centres x {red[1]} clients)")

if __name__ == "__main__":
    main()
