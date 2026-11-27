"""Theorem A of SCI-RES-0006 at large n by exact type-class sums (own code): the lower bound with the one-body oracle
(1 - 2 delta)/(n H_{k,r}) at the compensated instance, against R^max(e)."""
import math, sys
import numpy as np
from math import lgamma

def lbinom(n, k):
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)

def consts(p, u):
    q = 1 - p
    return q, -math.log(q + p * math.exp(-u)), -math.log(p + q * math.exp(-u))

def F(p, u, g, t):
    q, L0, L1 = consts(p, u)
    return (-t * math.log(q + p * math.exp(-g))
            + math.log((1 - math.exp(-t * (u + g))) * math.exp(-t * L0) + (1 - math.exp(-t * (u - g))) * math.exp(-t * (L1 + g)))
            - math.log(1 - math.exp(-2 * t * u)))

def saddle(p, u, efrac):
    T = np.linspace(1e-4, 1, 4001); G = np.linspace(-u * (1 - 1e-9), u * (1 - 1e-9), 2001)
    Fv = np.array([[F(p, u, g, t) for t in T] for g in G])
    Fs = Fv.max(axis=0)
    E = float((Fs / T).max())
    e = efrac * E
    val = Fs - T * e
    it = int(val.argmax()); ig = int(Fv[:, it].argmax())
    return E, e, float(val[it]), float(T[it]), float(G[ig])

def rho(p, u, g, t, m):
    q = 1 - p
    pg = p * math.exp(-g) / (q + p * math.exp(-g))
    pm = p * math.exp(-u) / (q + p * math.exp(-u)); pp = p * math.exp(u) / (q + p * math.exp(u))
    pi0, pi1, pig = (1 - pm, pm), (1 - pp, pp), (1 - pg, pg)
    return max((1 - m) * (pi0[a] / pig[a]) ** t + m * (pi1[a] / pig[a]) ** t for a in (0, 1))

def H_exact(n, k, p, u, g, r):
    """max over the type j of x of P_{s uniform in T_k}[Phi_s(x) < r], Phi_s(x) = sum_i ln(pi_gamma(x_i)/pi_{s_i}(x_i))."""
    q = 1 - p
    pg = p * math.exp(-g) / (q + p * math.exp(-g))
    pm = p * math.exp(-u) / (q + p * math.exp(-u)); pp = p * math.exp(u) / (q + p * math.exp(u))
    l = {(a, b): math.log(((1 - pg, pg)[a]) / (((1 - pm, pm), (1 - pp, pp))[b][a])) for a in (0, 1) for b in (0, 1)}
    best = -math.inf
    lb = lbinom(n, k)
    for j in range(n + 1):                       # x has j ones
        i = np.arange(max(0, k - (n - j)), min(j, k) + 1)   # ones of x inside the ones of s
        # counts: (x=1,s=1): i ; (x=1,s=0): j - i ; (x=0,s=1): k - i ; (x=0,s=0): n - j - k + i
        Phi = i * l[(1, 1)] + (j - i) * l[(1, 0)] + (k - i) * l[(0, 1)] + (n - j - k + i) * l[(0, 0)]
        sel = Phi < r
        if not sel.any():
            continue
        lw = np.array([lbinom(j, int(ii)) + lbinom(n - j, int(k - ii)) for ii in i[sel]]) - lb
        m = lw.max()
        best = max(best, m + math.log(np.exp(lw - m).sum()))
    return best                                    # ln H

if __name__ == "__main__":
    p, u, ef = 0.3, 1.0, 0.3
    E, e, Rmax, ts, gs = saddle(p, u, ef)
    ms = min(np.linspace(0.001, 0.999, 9981), key=lambda m: rho(p, u, gs, ts, m))
    print(f"(p,u)=({p},{u}): E={E:.6f} e={e:.6f} R^max(e)={Rmax:.6f} t*={ts:.4f} gamma*={gs:+.4f} m*={ms:.4f}")
    q = 1 - p
    pm = p * math.exp(-u) / (q + p * math.exp(-u)); pp = p * math.exp(u) / (q + p * math.exp(u)); om = pp - pm
    for n in (100, 200, 400, 800, 1600, 3200):
        k = round(ms * n); m = k / n; omm = om * min(m, 1 - m)
        eps = e * n
        # smallest r with ln(1 + (e^r - 1)/(1 + beta(r))) > eps
        lo, hi = 1e-9, eps + 50
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            kap = omm - 1 / math.expm1(mid) if mid < 700 else omm
            ok = kap > 0 and math.log1p(math.expm1(mid) / (1 + om / kap)) > eps if mid < 700 else True
            lo, hi = (lo, mid) if ok else (mid, hi)
        r = hi
        lH = H_exact(n, k, p, u, gs, r)
        print(f"  n={n:5d} k={k:5d} r={r:9.3f} (eps={eps:8.3f})  ln(1/(n H))/n = {(-lH - math.log(n)) / n:.6f}   -ln H/n = {-lH / n:.6f}")
