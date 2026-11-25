#!/usr/bin/env python3
"""Two-round lower bound: exact finite-n evaluation of the pair (F_D, F_S) of Theorem U3.

Cube Q_n = Q_{n1} x Q_{n2}; types (d1, d2) = (d(x^1, s^1), d(x^2, s^2)); P_j = Bin(n_j, 1/2).
  W1 = {(d1,d2) : -ln P1(d1) - ln P2(d2) <= T}       (what a blind batch sees),  p1 = P((D1,D2) not in W1)
  W2 = central interval of d2 with P(D2 not in W2) <= p1 (the smallest such: "balance"), V2 = {d2 in W2},
       p2 = P(D2 not in W2)                           (what a batch sees that knows s^1)
  g_j(d)      = - (largest u-Lipschitz minorant of  ln P_j(mode) - ln P_j(d))     ("flat histogram" of block j)
  F_deep      = lower McShane envelope of g_1 from W1:  max_{e in W1} [ g_1(e1) - u|d1-e1| - u|d2-e2| ]
  F_cap       = max(F_deep, g_1(d1) + g_2(d2))        (cap = 1 keeps every type of V2 at mass <= that of the typical type;
                                                       cap = 0: F_cap = F_deep, the first version of this script)
  F_D, F_S    = lower / upper McShane envelopes of F_cap from V2:  F_cap(d1, b) -/+ u |d2 - b|,  b = end point of W2.
All four are u-Lipschitz in each argument (checked); F_D = F_S on V2 (by construction, checked); F_cap = g_1 on W1 (checked).
Lemma U2 (with R1's set W1 cap V2, on which F_D = F_S = g_1(d1)): a two-round algorithm with batches M1, M2 that is
(eps/2, delta)-correct on L_u has  M1 (p1 + p2) + M2 p2 >= 1 - 2 delta  whenever  eps < gap := ln A(F_D) - ln A(F_S);
hence  max(M1, M2) >= (1 - 2 delta)/(p1 + 2 p2).  All probabilities in log space.
usage: lb2_exact.py u eps cap n [n ...]
"""
import sys, math, time
import numpy as np
from ulib import Cube, log_binom_pmf, logsumexp, LN2


def build(u, n1, n2, T, balance=True, cap=True):
    lp1, lp2 = log_binom_pmf(n1), log_binom_pmf(n2)
    c1, c2 = -lp1, -lp2                        # costs of shells
    lcdf2 = np.logaddexp.accumulate(lp2)       # ln P(D2 <= j)
    half = n2 // 2
    # W1 slices: for each e1 the interval [lo, n2-lo] of e2 with c2 <= T - c1[e1]
    rem = T - c1
    left = c2[:half + 1]                       # decreasing
    lo = np.full(n1 + 1, -1, dtype=int)
    ok = rem >= c2[half]
    lo[ok] = np.searchsorted(-left, -rem[ok], side="left")
    valid = lo >= 0
    if not valid.any():
        return None
    hi = np.where(valid, n2 - lo, -1)
    # ln p1
    terms = np.where(valid, np.where(lo >= 1, lp1 + LN2 + lcdf2[np.clip(lo - 1, 0, n2)], -np.inf), lp1)
    lnp1 = logsumexp(terms[np.isfinite(terms)]) if np.isfinite(terms).any() else -np.inf
    # W2
    lo2 = int(np.min(lo[valid]))               # the d2-projection of W1
    if balance:
        j = lo2
        while j + 1 <= half and LN2 + lcdf2[j] <= lnp1:
            j += 1
        lo2 = j
    hi2 = n2 - lo2
    proj_ok = lo2 <= int(np.min(lo[valid]))
    lnp2 = LN2 + lcdf2[lo2 - 1] if lo2 >= 1 else -np.inf
    # g: flat histogram, minus the largest u-Lipschitz minorant of t = lp1[mode] - lp1
    mg = lp1[n1 // 2] - lp1
    for d in range(1, n1 + 1):
        mg[d] = min(mg[d], mg[d - 1] + u)
    for d in range(n1 - 1, -1, -1):
        mg[d] = min(mg[d], mg[d + 1] + u)
    g = -mg
    # F_deep
    d2 = np.arange(n2 + 1)[None, :]
    F = np.maximum(0, np.maximum(lo[:, None] - d2, d2 - hi[:, None])).astype(float)
    F *= -u
    F += g[:, None]
    F[~valid, :] = -np.inf
    for e in range(1, n1 + 1):
        np.maximum(F[e], F[e - 1] - u, out=F[e])
    for e in range(n1 - 1, -1, -1):
        np.maximum(F[e], F[e + 1] - u, out=F[e])
    if cap:
        mg2 = lp2[n2 // 2] - lp2
        for d in range(1, n2 + 1):
            mg2[d] = min(mg2[d], mg2[d - 1] + u)
        for d in range(n2 - 1, -1, -1):
            mg2[d] = min(mg2[d], mg2[d + 1] + u)
        np.maximum(F, g[:, None] - mg2[None, :], out=F)          # F_cap
    # F_D (stored in F) and F_S: extensions from V2 = {lo2 <= d2 <= hi2}
    Fs = F.copy()
    if lo2 > 0:
        k = np.arange(lo2, 0, -1)[None, :]                       # distances lo2 - d for d = 0..lo2-1
        Fs[:, :lo2] = F[:, [lo2]] + u * k
        Fs[:, hi2 + 1:] = F[:, [hi2]] + u * np.arange(1, n2 - hi2 + 1)[None, :]
        F[:, :lo2] = F[:, [lo2]] - u * k
        F[:, hi2 + 1:] = F[:, [hi2]] - u * np.arange(1, n2 - hi2 + 1)[None, :]
    return dict(lp1=lp1, lp2=lp2, lo=lo, hi=hi, valid=valid, lo2=lo2, hi2=hi2, lnp1=float(lnp1), lnp2=float(lnp2),
                g=g, F=F, Fs=Fs, proj_ok=proj_ok)


def checks(u, B):
    F, Fs, g = B["F"], B["Fs"], B["g"]
    tol = 1e-9
    lipF = max(np.max(np.abs(np.diff(F, axis=0))), np.max(np.abs(np.diff(F, axis=1))))
    lipS = max(np.max(np.abs(np.diff(Fs, axis=0))), np.max(np.abs(np.diff(Fs, axis=1))))
    ok_lip = bool(lipF <= u + tol and lipS <= u + tol)
    n1 = F.shape[0] - 1
    err = 0.0
    for e1 in range(n1 + 1):                         # F_D = F_S = g_1 on W1 cap V2
        if B["valid"][e1]:
            l0, h0 = max(B["lo"][e1], B["lo2"]), min(B["hi"][e1], B["hi2"])
            if l0 <= h0:
                err = max(err, float(np.max(np.abs(F[e1, l0:h0 + 1] - g[e1]))), float(np.max(np.abs(Fs[e1, l0:h0 + 1] - g[e1]))))
    ok_w1 = err <= tol
    ok_v2 = float(np.max(np.abs(F[:, B["lo2"]:B["hi2"] + 1] - Fs[:, B["lo2"]:B["hi2"] + 1]))) <= tol
    ok_order = bool(np.all(Fs >= F - tol))
    return ok_lip, ok_w1, ok_v2, ok_order, bool(B["proj_ok"])


def lnA(B, which):
    return logsumexp((B["lp1"][:, None] + B["lp2"][None, :] - B[which]).ravel())


CAP = True


def gap_at(u, n1, n2, theta):
    B = build(u, n1, n2, theta * (n1 + n2), cap=CAP)
    if B is None:
        return None
    return lnA(B, "F") - lnA(B, "Fs"), B


def best_for(u, n, eps_req, phis, steps=20):
    cube = Cube(u)
    best = None
    for phi1 in phis:
        n1 = int(round(phi1 * n)); n2 = n - n1
        lo_t, hi_t = 0.5 * cube.h, min(1.2 * cube.a, 0.69 * n2 / n)
        r = gap_at(u, n1, n2, lo_t)
        if r is None or r[0] <= eps_req:
            continue
        for _ in range(steps):
            mid = 0.5 * (lo_t + hi_t)
            r = gap_at(u, n1, n2, mid)
            if r is not None and r[0] > eps_req:
                lo_t = mid
            else:
                hi_t = mid
        gap, B = gap_at(u, n1, n2, lo_t)
        # R1 must stay in W1 and in V2 = {d2 in W2}: failure probability <= p1 + p2; R2 in V2: p2
        expo = -float(np.logaddexp(B["lnp1"], math.log(2.0) + B["lnp2"])) / n
        if best is None or expo > best[0]:
            best = (expo, n1, n2, lo_t, gap, B)
    return best


if __name__ == "__main__":
    u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
    eps_req = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    CAP = bool(int(sys.argv[3])) if len(sys.argv) > 3 else True
    ns = [int(x) for x in sys.argv[4:]] or [200, 400, 800, 1600, 3200]
    cube = Cube(u)
    print(f"u={u}: a={cube.a:.6f} h={cube.h:.6f} p_u={cube.pu:.4f}; required gap > eps = {eps_req}; cap = {CAP}")
    print("n n1 n2 | T/(n a) | -ln(p1)/n -ln(p2)/n | gap = lnA(F_D)-lnA(F_S), gap/n | bulk type of F_D | "
          "E = -ln(p1+2 p2)/n, E/a, E/h | hinted bound 2^n/|B(k*)| exponent | checks (Lipschitz; F_D=F_S=g_1 on W1 cap V2; F_D=F_S on V2; F_S>=F_D; [W1 inside V2])")
    for n in ns:
        t0 = time.time()
        phis = (0.45, 0.5, 0.55, 0.6, 0.64, 0.68) if n <= 3200 else (0.56, 0.6, 0.64)
        best = best_for(u, n, eps_req, phis, steps=20 if n <= 3200 else 14)
        if best is None:
            print(f"{n}: no admissible theta with gap > {eps_req}")
            continue
        expo, n1, n2, th, gap, B = best
        ok = checks(u, B)
        i1, i2 = np.unravel_index(np.argmax(B["lp1"][:, None] + B["lp2"][None, :] - B["F"]), B["F"].shape)
        # hinted lower bound exponent at the same accuracy (Theorem 11.25(a)): least k with Delta_k > eps
        lpn = log_binom_pmf(n)
        j = np.arange(n + 1)
        kstar = None
        lcdf = np.logaddexp.accumulate(lpn)
        for k in range(n):
            # ln( 2^{-n} sum_{j<=k} C(n,j) (e^{u(k+1-j)} - 1) )
            x = u * (k + 1 - j[:k + 1])
            val = logsumexp(lpn[:k + 1] + x + np.log1p(-np.exp(-x)))
            if val > math.log(math.expm1(eps_req)):
                kstar = k
                break
        hint = float(-lcdf[kstar] / n)
        print(f"{n} {n1} {n2} | {th/cube.a:.4f} | {-B['lnp1']/n:.5f} {-B['lnp2']/n:.5f} | {gap:.3f} {gap/n:.5f} | ({i1/n1:.3f},{i2/n2:.3f}) | "
              f"{expo:.5f} {expo/cube.a:.4f} {expo/cube.h:.4f} | {hint:.5f} | {ok} ({time.time()-t0:.0f}s)", flush=True)
        del B, best
