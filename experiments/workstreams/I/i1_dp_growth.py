#!/usr/bin/env python3
"""Workstream I (isoperimetry and tail functions on product spaces), experiment 1.

A rigorous lower bound, by induction over the sites, for the growth of neighbourhoods in a
product of binary sites with a product measure and an additive cost:

    g_n(m, t)  <=  inf { mu(E_t) : mu(E) >= m },     E_t = { y : c(x, y) <= t for some x in E }.

Induction step (site with law (q0, q1), costs c01 = cost(0 -> 1), c10 = cost(1 -> 0)):
for E with fibres E_0, E_1 of measures m_0, m_1 (m = q0 m_0 + q1 m_1),

    mu(E_t)  >=  q0 * max( g(m_0, t), g(m_1, t - c10) )  +  q1 * max( g(m_1, t), g(m_0, t - c01) ),

so  g_{n+1}(m, t) := inf over (m_0, m_1) with q0 m_0 + q1 m_1 >= m  of the right side is valid.
Grid: d = -ln m in steps hd; the adversary's fibre measures are rounded DOWN to the grid
(valid by monotonicity) and the constraint is relaxed by the factor exp(-hd) per site.

This file tests the sharpness for the uniform cube against Harper's theorem (balls are exact
minimisers) and prints the loss.  Floating point; nothing here is certified.
"""
import sys, math
import numpy as np

def make_index(K, hd, q0, q1):
    """idx[k, k0] = largest grid index k1 (smallest m_1) such that q0 m_{k0} + q1 m_{k1} >= m_k e^{-hd};
    K+1 means 'm_1 = 0 allowed' (empty fibre); -1 means infeasible."""
    d = np.arange(K + 1) * hd
    m = np.exp(-d)
    target = m * math.exp(-hd)                       # relaxed constraint
    need = (target[:, None] - q0 * m[None, :]) / q1  # required m_1
    idx = np.full((K + 1, K + 1), -1, dtype=np.int32)
    pos = need > 0
    with np.errstate(divide='ignore', invalid='ignore'):
        k1 = np.floor(-np.log(np.where(pos, need, 1.0)) / hd + 1e-12).astype(np.int64)
    feas = pos & (need <= 1.0)
    idx[feas] = np.minimum(k1[feas], K).astype(np.int32)
    idx[~pos] = K + 1
    # empty fibre 0: need m_1 >= target / q1
    need0 = target / q1
    idx_e0 = np.full(K + 1, -1, dtype=np.int32)
    f0 = need0 <= 1.0
    idx_e0[f0] = np.minimum(np.floor(-np.log(need0[f0]) / hd + 1e-12), K).astype(np.int32)
    return idx, idx_e0

def step(G, idx, idx_e0, q0, q1, c01, c10):
    """G[t, k] = g(m_k, t) for k = 0..K, and G[t, K+1] = 0 (empty set).  Returns the next G."""
    T1, K2 = G.shape
    K = K2 - 2
    Gn = np.zeros_like(G)
    zero = np.zeros(K2)
    feas = idx >= 0
    ii = np.where(feas, idx, 0)
    for t in range(T1):
        A = G[t]                                  # g(., t)
        B01 = G[t - c01] if t - c01 >= 0 else zero  # source fibre 0 serving y = 1
        B10 = G[t - c10] if t - c10 >= 0 else zero  # source fibre 1 serving y = 0
        # pairs (k0, k1 = idx[k, k0]):
        a0 = A[None, :K + 1]; b0 = B01[None, :K + 1]
        F = q0 * np.maximum(a0, B10[ii]) + q1 * np.maximum(A[ii], b0)
        F = np.where(feas, F, np.inf)
        best = F.min(axis=1)
        # empty fibre 0, fibre 1 = idx_e0[k]:
        f0 = idx_e0 >= 0
        j = np.where(f0, idx_e0, 0)
        e0 = np.where(f0, q0 * B10[j] + q1 * A[j], np.inf)
        Gn[t, :K + 1] = np.minimum(best, e0)
    return Gn

def binom_tail_ball(n, r):
    return sum(math.comb(n, j) for j in range(0, r + 1)) / 2.0 ** n if r >= 0 else 0.0

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    hd = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
    q1 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    q0 = 1 - q1
    dmax = n * math.log(1 / min(q0, q1)) + 1.0
    K = int(math.ceil(dmax / hd))
    T = n
    print(f"n={n} hd={hd} q1={q1} K={K} (grid of -ln m up to {K*hd:.2f}), budgets 0..{T}")
    idx, idx_e0 = make_index(K, hd, q0, q1)
    G = np.ones((T + 1, K + 2)); G[:, K + 1] = 0.0          # n = 0: a point
    for i in range(1, n + 1):
        G = step(G, idx, idx_e0, q0, q1, 1, 1)
    d = np.arange(K + 1) * hd
    if abs(q1 - 0.5) < 1e-12:
        print("uniform cube: DP bound against Harper (ball of radius r grown by t); the DP is evaluated at")
        print("m = (ball measure) * exp(-n*hd) rounded down to the grid, so a loss of n*hd in -ln m is built in")
        print(" r  t   -ln(ball r)  -ln(ball r+t)  -ln DP      loss(nats)")
        worst = 0.0
        for r in range(0, n // 2 + 1, max(1, n // 8)):
            for t in (1, 2, n // 8, n // 4, n // 2):
                if t < 1 or r + t > n: continue
                mb = binom_tail_ball(n, r)
                k = int(math.ceil(-math.log(mb) / hd - 1e-9))     # round m down to grid
                val = G[t, k]
                tru = binom_tail_ball(n, r + t)
                loss = -math.log(val) + math.log(tru)
                worst = max(worst, loss)
                print(f"{r:2d} {t:2d}  {-math.log(mb):10.4f}  {-math.log(tru):12.4f}  {-math.log(val):10.4f}  {loss:9.4f}")
        print(f"largest loss {worst:.4f} nats (grid slack up to about n*hd = {n*hd:.3f} in -ln m)")

if __name__ == "__main__":
    main()
