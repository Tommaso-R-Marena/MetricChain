#!/usr/bin/env python3
"""Workstream I, experiment 3: tail functions on a product of binary sites by induction over sites.

For a product measure mu = prod(pi_i) and an additive envelope rho(x, z) = sum_i c_i(x_i, z_i):

  upper tail  Xi(q)    >=  sup { int_D (e^{rho(x -> D^c)} - 1) dmu : mu(D) <= q }        (TU)
  lower tail  Theta(q) <=  inf { int e^{-rho(S -> z)} dmu(z)       : mu(S) >= q }        (TL)

Induction over the last site (law (p0, p1), costs c01 = c(0 -> 1), c10 = c(1 -> 0)), for D with
fibres D_0, D_1 of measures s_0, s_1 and U(A) = int e^{rho(x -> A)} dmu, A = D^c:

  U(A) = sum_x p_x int min_y [ e^{c(x,y)} e^{rho'(x', A_y)} ] dmu'  <=  sum_x p_x min_y e^{c(x,y)} U'(A_y),

  1 + Xi_{n+1}(q) := sup over p0 s_0 + p1 s_1 <= q  of
        p0 * min( 1 + Xi_n(s_0), e^{c01} (1 + Xi_n(s_1)) )  +  p1 * min( 1 + Xi_n(s_1), e^{c10} (1 + Xi_n(s_0)) ),

and likewise  Theta_{n+1}(q) := inf over p0 s_0 + p1 s_1 >= q  of
        p0 * max( Theta_n(s_0), e^{-c10} Theta_n(s_1) )  +  p1 * max( Theta_n(s_1), e^{-c01} Theta_n(s_0) )

(y = 0 is reached from S_0 at no cost and from S_1 at the cost c10).  Base: Xi_0(q) = 0 for q < 1
(D empty), Theta_0(q) = 1 for q > 0.  Grid in -ln q with step hd; the adversary's fibre values are
rounded to the grid in the direction that keeps the bound valid, and the constraint is relaxed by
exp(+-hd) per site.  Floating point: nothing here is certified; this file measures sharpness.
"""
import sys, math
import numpy as np

def grids(K, hd):
    d = np.arange(K + 1) * hd
    return d, np.exp(-d)

def xi_index(K, hd, p0, p1):
    """For target k and fibre-0 index k0 (0..K, K+1 = empty): the smallest index k1 (largest s_1)
    with p0 s_{k0} + p1 s_{k1} <= q_k e^{hd}; -1 if infeasible; K+1 if only s_1 = 0 fits."""
    d, q = grids(K, hd)
    s0 = np.concatenate([q, [0.0]])
    lim = (q[:, None] * math.exp(hd) - p0 * s0[None, :]) / p1          # allowed s_1
    idx = np.full(lim.shape, -1, dtype=np.int32)
    feas = lim >= 0
    with np.errstate(divide='ignore', invalid='ignore'):
        k1 = np.ceil(-np.log(np.where(lim > 0, np.minimum(lim, 1.0), 1.0)) / hd - 1e-12).astype(np.int64)
    k1 = np.where(lim > 0, np.minimum(k1, K + 1), K + 1)
    k1 = np.where((lim > 0) & (k1 > K), K + 1, k1)
    idx[feas] = k1[feas].astype(np.int32)
    return idx

def xi_step(X, idx, p0, p1, c01, c10):
    """X[k] = Xi(q_k), k = 0..K; X[0] = inf (q = 1); X[K+1] = 0 (empty set)."""
    K = len(X) - 2
    H = 1.0 + X
    feas = idx >= 0
    j = np.where(feas, idx, K + 1)
    h0 = H[None, :]                      # fibre 0 at index k0 (columns 0..K+1)
    h1 = H[j]
    with np.errstate(invalid='ignore'):
        val = p0 * np.minimum(h0, math.exp(c01) * h1) + p1 * np.minimum(h1, math.exp(c10) * h0) - 1.0
    val = np.where(feas, val, -np.inf)
    Xn = np.empty_like(X)
    Xn[:K + 1] = val.max(axis=1)
    Xn[K + 1] = 0.0
    Xn[0] = np.inf
    return np.maximum(Xn, 0.0)

def th_index(K, hd, p0, p1):
    """For target k and fibre-0 index k0: the largest index k1 (smallest s_1) with
    p0 s_{k0} + p1 s_{k1} >= q_k e^{-hd}; K+1 if s_1 = 0 will do; -1 if infeasible."""
    d, q = grids(K, hd)
    s0 = np.concatenate([q, [0.0]])
    need = (q[:, None] * math.exp(-hd) - p0 * s0[None, :]) / p1
    idx = np.full(need.shape, -1, dtype=np.int32)
    with np.errstate(divide='ignore', invalid='ignore'):
        k1 = np.floor(-np.log(np.where(need > 0, need, 1.0)) / hd + 1e-12).astype(np.int64)
    ok = (need > 0) & (need <= 1.0)
    idx[ok] = np.minimum(k1[ok], K).astype(np.int32)
    idx[need <= 0] = K + 1
    return idx

def th_step(Th, idx, p0, p1, c01, c10):
    """Th[k] = Theta(q_k), k = 0..K; Th[K+1] = 0 (empty)."""
    K = len(Th) - 2
    feas = idx >= 0
    j = np.where(feas, idx, K + 1)
    t0 = Th[None, :]
    t1 = Th[j]
    val = p0 * np.maximum(t0, math.exp(-c10) * t1) + p1 * np.maximum(t1, math.exp(-c01) * t0)
    val = np.where(feas, val, np.inf)
    Tn = np.empty_like(Th)
    Tn[:K + 1] = val.min(axis=1)
    Tn[K + 1] = 0.0
    return Tn

def run(sites, hd, K):
    """sites: list of (p1, c01, c10).  Returns (d-grid, Xi, Theta) after all sites."""
    X = np.zeros(K + 2); X[0] = np.inf
    Th = np.ones(K + 2); Th[K + 1] = 0.0
    cache = {}
    for (p1, c01, c10) in sites:
        p0 = 1 - p1
        if p1 not in cache:
            cache[p1] = (xi_index(K, hd, p0, p1), th_index(K, hd, p0, p1))
        ix, it = cache[p1]
        X = xi_step(X, ix, p0, p1, c01, c10)
        Th = th_step(Th, it, p0, p1, c01, c10)
    return np.arange(K + 1) * hd, X, Th

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    u = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    hd = float(sys.argv[3]) if len(sys.argv) > 3 else 0.01
    K = int(math.ceil((n * math.log(2) + 1.0) / hd))
    d, X, Th = run([(0.5, u, u)] * n, hd, K)
    b = [math.comb(n, j) / 2.0 ** n for j in range(n + 1)]
    print(f"uniform cube n={n}, u={u}, hd={hd}: DP tail functions against the exact ones at ball sizes")
    print("(the DP is read at q*exp(+-n*hd), the slack that the grid builds in; ratio = DP / exact)")
    print("  r   -ln q     Xi exact      Xi DP      ratio   | Theta exact   Theta DP   ratio")
    worst_x = worst_t = 1.0
    for r in range(0, n):
        q = sum(b[:r + 1])
        xi_ex = sum(b[j] * (math.exp(u * (r - j + 1)) - 1) for j in range(r + 1))
        th_ex = sum(b[j] * math.exp(-u * max(j - r, 0)) for j in range(n + 1))
        kx = int(math.floor(-math.log(q) / hd + 1e-9))          # q rounded up to the grid (Xi nondecreasing)
        kt = int(math.ceil(-math.log(q) / hd - 1e-9))           # q rounded down (Theta nondecreasing)
        if kx < 1: continue
        rx = X[kx] / xi_ex; rt = Th[min(kt, K)] / th_ex
        worst_x = max(worst_x, rx); worst_t = min(worst_t, rt)
        print(f" {r:3d} {-math.log(q):8.4f}  {xi_ex:11.4e} {X[kx]:11.4e} {rx:8.4f}  | {th_ex:11.4e} {Th[min(kt,K)]:11.4e} {rt:8.4f}")
    print(f"largest Xi ratio {worst_x:.4f}; smallest Theta ratio {worst_t:.4f}")

if __name__ == "__main__":
    main()
