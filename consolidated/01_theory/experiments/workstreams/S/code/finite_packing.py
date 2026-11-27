#!/usr/bin/env python3
"""Rigorous lower bounds for the covering number N^P_cov(eps1*N) at a GIVEN chain length N, from explicit walks.

Family: rung-folded lamellae (M x Q stems of ell periods, code/lamella.py) whose last stem is prolonged by an
all-trans tail so that the walk has exactly N beads.  For each walk the exact (h3, h8, h11, #gauche) is computed
from its coordinates.  A set of these walks with  L ||h_i - h_j||_c > g_i + g_j + 2 eps1 N  pairwise (profile norm
of cumulative counts) forces that many evaluations: no centre covers two of them (the radius of the class of
walk i is gmin + eps <= g_i + eps).  The packing is found greedily and verified.

usage: finite_packing.py N1 N2 ...
"""
import sys
import numpy as np
from lat import *
import lamella as lam

def lamella_tail(M, Q, ell, N):
    w = lam.lamella(M, Q, ell)
    t = N - len(w)
    if t < 0: return None
    # prolong the last stem: rod (M-1, Q-1) upwards, positions 2*ell+2, ...
    m, q = M - 1, Q - 1
    w = w + [lam.site(m, q, 2 * ell + 1 + i) for i in range(1, t + 1)]
    return w

def cum(h):
    return np.array([h[0], h[0] + h[1], h[0] + h[1] + h[2]])

def best_packing(pts, L, eps):
    """pts: list of (h3,h8,h11,g); condition L*||dh||_c > g_i + g_j + 2 eps.  greedy with several orders."""
    H = np.array([cum(p[:3]) for p in pts]); G = np.array([p[3] for p in pts])
    Wc = np.array([5, 3, 1])
    n = len(pts); best = []
    orders = [np.argsort(H @ Wc), np.argsort(-(H @ Wc)), np.argsort(G), np.argsort(H[:, 0] * 1000 + H[:, 2])]
    rng = np.random.default_rng(0)
    for k in range(12): orders.append(np.argsort(H @ (Wc * rng.random(3)) + 3 * rng.random() * G))
    for order in orders:
        alive = np.ones(n, bool); chosen = []
        for i in order:
            if not alive[i]: continue
            chosen.append(i)
            d = (np.abs(H - H[i]) * Wc).sum(axis=1)
            alive &= (L * d > G + G[i] + 2 * eps)
        if len(chosen) > len(best): best = chosen
    B = best
    for a in range(len(B)):
        for b in range(a + 1, len(B)):
            d = (np.abs(H[B[a]] - H[B[b]]) * Wc).sum()
            assert L * d > G[B[a]] + G[B[b]] + 2 * eps
    return len(best)

def main():
    print("#     N  walks  distinct (h,g) | max ||h||_c/N   min g/N at that point | packing lower bounds for N_cov:  L=1,eps=N/2   L=1,eps=N/4   L=1/5,eps=N/2   L=1/5,eps=N/4")
    for N in map(int, sys.argv[1:]):
        pts = {}
        nw = 0
        # all-trans rod
        Ms = [m for m in range(1, 200, 2)]
        for M in Ms:
            for Q in range(1, M + 1, 2):
                if 2 * M * Q * 2 > N + 4: break
                # stem length values: all for small N, a coarse grid for large N
                lmax = (N + M * Q) // (2 * M * Q) + 1
                ells = range(2, lmax + 1) if lmax <= 40 else sorted(set(np.unique(np.linspace(2, lmax, 40).astype(int))))
                for ell in ells:
                    w = lamella_tail(M, Q, ell, N)
                    if w is None: continue
                    nw += 1
                    assert len(w) == N and is_walk(w)          # every member is checked to be a self-avoiding lattice walk
                    p = profile(w)
                    key = p[:3]
                    if key not in pts or p[3] < pts[key]: pts[key] = p[3]
        P = [k + (g,) for k, g in pts.items()]
        P.append((0, 0, 0, 0))                       # the all-trans chain
        ext = max((9 * p[0] + 4 * p[1] + p[2]) / N for p in P)
        gext = min(p[3] / N for p in P if abs((9 * p[0] + 4 * p[1] + p[2]) / N - ext) < 1e-12)
        res = [best_packing(P, L, e * N) for (L, e) in ((1, 0.5), (1, 0.25), (0.2, 0.5), (0.2, 0.25))]
        print(f"  {N:6d} {nw:6d} {len(P):6d}        |   {ext:7.3f}        {gext:6.3f}            |          {res[0]:6d}        {res[1]:6d}         {res[2]:6d}          {res[3]:6d}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
