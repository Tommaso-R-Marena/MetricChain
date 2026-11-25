"""Addendum A16, Lemma A16.5 (isoperimetry with an energy constraint) and Proposition A16.6.

Lemma.  Units beta = 1.  Among all u-Lipschitz g on Q_n that vanish outside a set of at most N points and have
mean energy U(g) >= U0, the PLATEAU on the initial segment B_N of the simplicial order,
        g_pl = -min(c, u * dist(x, complement of B_N)),   c chosen with U(g_pl) = U0
(the full cone, c = infinity, if even that has U >= U0), has the largest partition function.

Proof (addendum): Lagrangian Z <= sum_x f_eta(t(x)), f_eta(t) = (1 - eta U0) t - eta t ln t; pointwise the best
admissible value is the level t* clipped to [e^{-u rho}, e^{u rho}], rho = distance to the complement of the
support; the resulting sum is a nondecreasing function of rho, so Harper's theorem applies; strong duality at
the plateau.

Checks.
 1. ALL subsets D of Q_4 (65 534) and random subsets of Q_5, Q_6: the best energy-feasible modification
    supported on D (explicit: the clipped level) against the plateau on the initial segment of the same size.
 2. Random members of the class with a zero background (dips AND hills, n <= 10): Z(g) <= Z_pl(N(g), U(g)).
 3. Proposition A16.6: at the visible cone basin g0 of Proposition A16.3, the upper bound
        ln Z' - ln Z0 <= G(N) := ln Z_pl(N + |V|, U0) - ln Z0      for every g' = g0 outside N points, U(g') = U0,
    evaluated at ball sizes, against the gaps of the exact plateau twins of plateau_twin_check.json.

Usage: python3 energy_isoperimetry_check.py        (about 2 minutes)
"""
from __future__ import annotations
import math, json, os, itertools
import numpy as np
from scipy.special import gammaln, logsumexp
from scipy.optimize import brentq

def cube(n):
    return ((np.arange(2**n)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)

def simplicial_order(n):
    """indices of Q_n in Harper's simplicial order: by weight, then lexicographically by the positions of the ones"""
    X = cube(n)
    keys = [(int(x.sum()), tuple(np.nonzero(x)[0])) for x in X]
    return sorted(range(2**n), key=lambda k: keys[k])

def dist_to_complement(n, inD):
    """rho(x) = Hamming distance from x to the complement of D (0 outside D); BFS over single flips"""
    N = 2**n; rho = np.where(inD, -1, 0).astype(int); frontier = np.nonzero(~inD)[0]; k = 0
    idx = np.arange(N)
    while len(frontier):
        k += 1; nxt = []
        for i in range(n):
            nb = frontier ^ (1 << i); new = nb[rho[nb] == -1]
            rho[new] = k; nxt.append(new)
        frontier = np.unique(np.concatenate(nxt)) if nxt else np.array([], dtype=int)
    assert (rho >= 0).all()
    return rho

def best_on_support(rho_counts, u, U0, total):
    """rho_counts[k] = number of points with rho = k (k >= 1); background: total - sum points at energy 0.
    Profile m(x) = min(c, u rho(x)); U_c strictly decreasing in c.  Returns max Z over c with U_c >= U0."""
    ks = np.array(sorted(rho_counts)); cnt = np.array([rho_counts[k] for k in ks], dtype=float)
    bg = total - cnt.sum()
    def ZU(c):
        m = np.minimum(c, u*ks); w = cnt*np.exp(m); Z = bg + w.sum()
        return Z, -(w*m).sum()/Z
    cmax = u*ks.max()
    Z, U = ZU(cmax)
    if U >= U0: return Z
    c = brentq(lambda c: ZU(c)[1] - U0, 0.0, cmax, xtol=1e-13)
    return ZU(c)[0]

def counts(rho):
    v, c = np.unique(rho[rho > 0], return_counts=True)
    return dict(zip(v.tolist(), c.tolist()))

def check_subsets():
    rng = np.random.default_rng(5); worst = -math.inf; ncases = 0
    for n, mode in ((4, "all"), (5, "random"), (6, "random")):
        N = 2**n; order = np.array(simplicial_order(n))
        ball = {}
        for size in range(1, N):
            inB = np.zeros(N, bool); inB[order[:size]] = True
            ball[size] = counts(dist_to_complement(n, inB))
        if mode == "all":
            subsets = range(1, N_all := 2**N - 1)
        else:
            subsets = None
        params = [(u, U0) for u in (0.5, 1.5, 3.0) for U0 in (-0.05, -0.5, -2.0)]
        def one(inD):
            nonlocal worst, ncases
            size = int(inD.sum()); rc = counts(dist_to_complement(n, inD))
            for (u, U0) in params:
                zd = best_on_support(rc, u, U0, N); zb = best_on_support(ball[size], u, U0, N)
                worst = max(worst, math.log(zd/zb)); ncases += 1
                assert zd <= zb*(1 + 1e-9), (n, size, u, U0, zd, zb)
        if mode == "all":
            bits = np.arange(N)
            for s in range(1, 2**N - 1):
                one(((s >> bits) & 1).astype(bool))
        else:
            for _ in range(4000):
                size = int(rng.integers(1, N)); inD = np.zeros(N, bool); 
                if rng.random() < 0.5:                       # random subset
                    inD[rng.choice(N, size, replace=False)] = True
                else:                                        # union of a few balls (clustered supports)
                    X = cube(n)
                    for _ in range(int(rng.integers(1, 4))):
                        c0 = X[rng.integers(0, N)]; r = int(rng.integers(0, n))
                        inD |= ((X != c0).sum(axis=1) <= r)
                    if inD.all(): inD[rng.integers(0, N)] = False
                one(inD)
        print(f"check 1, n = {n} ({mode}): supports x (u, U0) cases so far {ncases}; largest ln[Z_best(D)/Z_plateau(ball)] = {worst:.2e} (must be <= 0)", flush=True)

def check_members():
    """random members with zero background, dips and hills: Z(g) <= Z_pl(#{g != 0}, U(g))"""
    rng = np.random.default_rng(7); worst = -math.inf; cnt = 0; tight = 0
    for trial in range(1500):
        n = int(rng.integers(4, 11)); u = float(rng.choice([0.5, 1.0, 2.0, 4.0])); N = 2**n; X = cube(n)
        g = np.zeros(N)
        for _ in range(int(rng.integers(1, 4))):
            c0 = X[rng.integers(0, N)]; d = (X != c0).sum(axis=1).astype(float); r = int(rng.integers(1, max(2, n//2 + 1)))
            kind = rng.random()
            if kind < 0.45:   g = np.minimum(g, -u*np.maximum(r - d, 0))                               # cone dip
            elif kind < 0.8:  g = np.minimum(g, -u*np.minimum(rng.uniform(0.2, r), np.maximum(r - d, 0)))  # plateau dip
            else:             g = np.where(g == 0, np.maximum(g, 0) + 0.0, g); g = np.maximum(g, np.where(g < 0, g, u*rng.uniform(0.1, 1)*np.maximum(r - d, 0)*(g == 0)))
        # enforce membership by one McShane projection pass is unnecessary for min/max of Lipschitz pieces; verify:
        ok = all(np.max(np.abs(g - g[np.arange(N) ^ (1 << i)])) <= u + 1e-9 for i in range(n))
        if not ok or not (g != 0).any() or (g != 0).all(): continue
        Z = float(np.exp(-g).sum()); U = float((g*np.exp(-g)).sum()/Z); size = int((g != 0).sum())
        order = np.array(simplicial_order(n)); inB = np.zeros(N, bool); inB[order[:size]] = True
        zb = best_on_support(counts(dist_to_complement(n, inB)), u, min(U, 0.0), N)
        worst = max(worst, math.log(Z/zb)); cnt += 1; tight += (Z > zb*(1 - 1e-6))
        assert Z <= zb*(1 + 1e-9), (n, u, size, U, Z, zb)
    print(f"check 2: {cnt} random members with zero background (dips and hills, n = 4..10): Z(g) <= Z_plateau(N(g), U(g)); "
          f"largest ln ratio {worst:.2e}; equality (g itself a plateau on a ball) in {tight} cases", flush=True)

def logbinom(n, d):
    return gammaln(n + 1) - gammaln(d + 1) - gammaln(n - d + 1)

def plateau_ball_upper(n, u, R, U0, extra_log=None):
    """ln Z (units 2^n) of the best energy-feasible instance supported on the ball B(n, R) [rho(d) = R + 1 - d]"""
    d = np.arange(0, R + 1); lb = logbinom(n, d) - n*math.log(2); rho = (R + 1 - d).astype(float)
    lbg = math.log1p(-math.exp(logsumexp(lb)))                 # background mass 1 - |B|/2^n
    def ZU(c):
        m = np.minimum(c, u*rho); lw = lb + m; lZ = np.logaddexp(lbg, logsumexp(lw))
        return lZ, -math.exp(logsumexp(lw + np.log(m)) - lZ)
    cmax = u*(R + 1); lZ, U = ZU(cmax)
    if U >= U0: return lZ, cmax
    c = brentq(lambda c: ZU(c)[1] - U0, 1e-9, cmax, xtol=1e-12)
    return ZU(c)[0], c

def check_exactness():
    rows = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "plateau_twin_check.json")))
    seen = set()
    print("check 3 (Proposition A16.6): at the visible basin, lower bound = exact plateau twin of radius r2 (supported in B(a', r2-1)); "
          "upper bound G(R) for every alternative that agrees with g0 outside |B(n,R)| - |V| points")
    for r in rows:
        key = (r["n"], r["u"], r["eps1"])
        if key in seen: continue
        seen.add(key)
        n, u, r1, r2 = r["n"], r["u"], r["r1"], r["r2"]; U0 = r["U0_over_n"]*n
        # ln Z0 in units of 2^n, recomputed: flat + cone basin of radius r1
        d = np.arange(0, r1); lb = logbinom(n, d) - n*math.log(2)
        lZ0 = math.log1p(math.exp(logsumexp(lb + u*(r1 - d))) - math.exp(logsumexp(lb)))
        out = []
        for R in (r2 - 2, r2 - 1, r2):
            lZ, c = plateau_ball_upper(n, u, R, U0)
            out.append((R, lZ - lZ0, c/u))
        # the twin lives in B(a', r2-1); with the visible basin the alternative differs from flat on at most |B(r2-1)| + |B(r1-1)| <= |B(r2)| points
        assert out[2][1] >= r["gap"] - 1e-6, (out, r["gap"])
        print(f"  n={n} u={u}: twin r2={r2}, kappa*={r['kappa']:.2f}, gap={r['gap']:.3f} | upper bounds G(R): "
              + ", ".join(f"R={R}: {G:.3f} (level {k:.2f})" for (R, G, k) in out)
              + f" | gap <= G(r2): {r['gap'] <= out[2][1] + 1e-9}; G(r2-2) < gap: {out[0][1] < r['gap']}", flush=True)

if __name__ == "__main__":
    check_exactness()
    check_members()
    check_subsets()
