#!/usr/bin/env python3
"""r-round lower bounds from nested flat histograms, small-slope limit (units a = 1, h = 1/4).

Blocks 1..r with fractions phi_j = sigma_j^2.  Coordinates Y_j in [0, sigma_j] (Y_j = sigma_j is the bulk radius p_u of
block j), rate sum Y_j^2, Lipschitz metric 2 sum sigma_j |dY_j|, flat histogram -g_j = Y_j^2.
Round t knows the centres of blocks < t and sees the types with sum_{j>=t} Y_j^2 <= theta.
Masses of the types (X_1..X_{t-1}, Z_t) (later coordinates typical) under the nested capped McShane construction:
    m_1(Z_1) = 0,
    mu_t(X_{<t}; Z_t) = min_{0<=Z<=min(sigma_{t-1}, sqrt(theta))} [ m_{t-1}(X_{<t-1}; Z) + Z^2 - X_{t-1}^2
                           + 2 sigma_{t-1} |X_{t-1} - Z| + 2 sigma_t (Z_t - sqrt(theta - Z^2))_+ ] - Z_t^2,
    m_t = min(0, mu_t)                                            (cap: no visible type is heavier than the typical one)
Hidden gain after r rounds:
    Xi_r = max_{X_{<r-1}} min_Z [ m_{r-1}(X_{<r-1}; Z) + (sigma_{r-1} - Z)^2 + sigma_r^2 - 2 sigma_r sqrt(theta - Z^2) ].
r rounds with batches below e^{n theta} fail if Xi_r > 0 and theta < sigma_r^2 (the bulk of the last block is not seen).
usage: lbr_gauss.py [N]
"""
import sys, math, itertools
import numpy as np


def xi2(theta, phi, N=2001):
    s1, s2 = math.sqrt(phi[0]), math.sqrt(phi[1])
    Z = np.linspace(0, min(s1, math.sqrt(theta)), N)
    val = (s1 - Z) ** 2 + s2 ** 2 - 2 * s2 * np.sqrt(np.maximum(theta - Z ** 2, 0))
    return float(np.min(val))


def m2_table(theta, s1, s2, N):
    """m_2(X1; Z2) on a grid X1 in [0,s1], Z2 in [0, min(s2, sqrt theta)]."""
    X1 = np.linspace(0, s1, N)
    Z1 = np.linspace(0, min(s1, math.sqrt(theta)), N)
    Z2 = np.linspace(0, min(s2, math.sqrt(theta)), N)
    Y2s = np.sqrt(np.maximum(theta - Z1 ** 2, 0))                    # visible block-2 coordinate at anchor shell Z1
    # base[X1, Z1] = Z1^2 - X1^2 + 2 s1 |X1 - Z1|
    base = Z1[None, :] ** 2 - X1[:, None] ** 2 + 2 * s1 * np.abs(X1[:, None] - Z1[None, :])
    m2 = np.empty((N, N))
    for k, z2 in enumerate(Z2):
        extra = 2 * s2 * np.maximum(z2 - Y2s, 0.0)                   # (N,) over Z1
        mu = np.min(base + extra[None, :], axis=1) - z2 ** 2
        m2[:, k] = np.minimum(0.0, mu)
    return X1, Z2, m2


def xi3(theta, phi, N=201):
    s1, s2, s3 = (math.sqrt(p) for p in phi)
    X1, Z2, m2 = m2_table(theta, s1, s2, N)
    tail = (s2 - Z2) ** 2 + s3 ** 2 - 2 * s3 * np.sqrt(np.maximum(theta - Z2 ** 2, 0))
    val = np.min(m2 + tail[None, :], axis=1)                         # min over Z2, for each X1
    return float(np.max(val))


def xi4(theta, phi, N=61):
    s1, s2, s3, s4 = (math.sqrt(p) for p in phi)
    X1, Z2, m2 = m2_table(theta, s1, s2, N)                          # m2[X1, Z2], Z2 on [0, min(s2, sqrt theta)]
    X2 = np.linspace(0, s2, N)
    Z3 = np.linspace(0, min(s3, math.sqrt(theta)), N)
    Y3s = np.sqrt(np.maximum(theta - Z2 ** 2, 0))
    # mu3[X1, X2, Z3] = min_{Z2} [ m2[X1,Z2] + Z2^2 - X2^2 + 2 s2 |X2 - Z2| + 2 s3 (Z3 - Y3s(Z2))_+ ] - Z3^2
    base = m2[:, None, :] + Z2[None, None, :] ** 2 - X2[None, :, None] ** 2 + 2 * s2 * np.abs(X2[None, :, None] - Z2[None, None, :])
    best = -1e9
    m3 = np.empty((N, N, N))
    for k, z3 in enumerate(Z3):
        extra = 2 * s3 * np.maximum(z3 - Y3s, 0.0)
        mu = np.min(base + extra[None, None, :], axis=2) - z3 ** 2
        m3[:, :, k] = np.minimum(0.0, mu)
    tail = (s3 - Z3) ** 2 + s4 ** 2 - 2 * s4 * np.sqrt(np.maximum(theta - Z3 ** 2, 0))
    val = np.min(m3 + tail[None, None, :], axis=2)
    return float(np.max(val))


def root(fun, phi, lo=0.25, **kw):
    hi = phi[-1] * 0.999999
    if hi <= lo:
        return hi, hi
    if fun(lo, phi, **kw) <= 0:
        return 0.0, 0.0
    if fun(hi, phi, **kw) > 0:
        return hi, hi
    a, b = lo, hi
    for _ in range(40):
        mid = 0.5 * (a + b)
        if fun(mid, phi, **kw) > 0:
            a = mid
        else:
            b = mid
    return a, a


if __name__ == "__main__":
    N3 = int(sys.argv[1]) if len(sys.argv) > 1 else 161
    print("== r = 2 ==")
    best = (0, None)
    for p1 in np.linspace(0.3, 0.8, 501):
        t, _ = root(xi2, (p1, 1 - p1))
        if t > best[0]:
            best = (t, p1)
    print(f"theta_2* = {best[0]:.5f} at phi = ({best[1]:.3f}, {1-best[1]:.3f});  Xi_2(h) there = {xi2(0.25, (best[1], 1-best[1])):+.5f}")
    print("== r = 3 ==  (grid N = %d)" % N3)
    best = (0, None)
    for p3 in np.linspace(0.26, 0.5, 13):
        for p2 in np.linspace(0.05, 0.6, 12):
            p1 = 1 - p2 - p3
            if p1 <= 0.02:
                continue
            x = xi3(0.25, (p1, p2, p3), N=81)
            if x <= 0:
                continue
            t, _ = root(xi3, (p1, p2, p3), N=81)
            if t > best[0]:
                best = (t, (p1, p2, p3))
    print("coarse:", best)
    if best[1] is not None:
        p1c, p2c, p3c = best[1]
        for p3 in np.linspace(max(0.251, p3c - 0.02), p3c + 0.02, 9):
            for p2 in np.linspace(max(0.02, p2c - 0.05), p2c + 0.05, 9):
                p1 = 1 - p2 - p3
                if p1 <= 0.02:
                    continue
                t, _ = root(xi3, (p1, p2, p3), N=N3)
                if t > best[0]:
                    best = (t, (p1, p2, p3))
        phi = best[1]
        print(f"theta_3* >= {best[0]:.5f} at phi = ({phi[0]:.3f}, {phi[1]:.3f}, {phi[2]:.3f});  Xi_3(h) there = {xi3(0.25, phi, N=N3):+.5f}; "
              f"grid check N={2*N3-1}: Xi_3(theta_3*) = {xi3(best[0], phi, N=2*N3-1):+.6f}")
    # a scan of Xi_3(h) to see whether three rounds at budget h can fail at all
    print("scan of Xi_3(h = 0.25):")
    for p3 in (0.26, 0.3, 0.35, 0.4, 0.5):
        row = []
        for p2 in (0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
            p1 = 1 - p2 - p3
            row.append("   --  " if p1 <= 0.02 else f"{xi3(0.25, (p1, p2, p3), N=121):+.4f}")
        print(f"  phi3={p3:.2f}: " + " ".join(row) + "   (phi2 = 0.05, 0.1, 0.2, 0.3, 0.4, 0.5)")
