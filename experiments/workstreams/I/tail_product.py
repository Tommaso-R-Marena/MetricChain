#!/usr/bin/env python3
"""Workstream I: tail functions on a product of binary sites with a product measure and an additive
envelope, from an induction over the sites (docs/workstreams/I_REPORT.md).

Sites: (p1, c01, c10) — P(x_i = 1) = p1, costs c01 = rho_i(0, 1), c10 = rho_i(1, 0) as nonnegative
integers (multiples of a common unit; the envelope is  unit * sum_i c_i(x_i, z_i)).

  growth_tables(sites, hd, T)      G[t, k] <= inf{ mu(E_t) : mu(E) >= exp(-k hd) }      (Lemma I1)
  tails_from_growth(G, hd, unit)   Xi[k]  >= sup{ int_D (e^{rho(x -> D^c)} - 1) dmu : mu(D) <= exp(-k hd) }
                                   Theta[k] <= inf{ int e^{-rho(S -> z)} dmu : mu(S) >= exp(-k hd) }
  theta_laplace(sites, unit, dgrid)  the closed form exp(-Phi(d)) of Theorem I3 (lower tail), by a
                                   numerical concave envelope and max-plus convolution over the sites.

Everything is floating point.  The DP rounds in the directions that keep the bounds valid (see the
report, I1.3), but the arithmetic itself is not interval arithmetic: nothing here is a certificate.
"""
import math
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i1_dp_growth import make_index, step

def growth_tables(sites, hd, T, dmax=None):
    if dmax is None:
        dmax = sum(math.log(1 / min(p1, 1 - p1)) for (p1, _, _) in sites) + 1.0
    K = int(math.ceil(dmax / hd))
    G = np.ones((T + 1, K + 2)); G[:, K + 1] = 0.0
    cache = {}
    for (p1, c01, c10) in sites:
        if p1 not in cache:
            cache[p1] = make_index(K, hd, 1 - p1, p1)
        idx, idx_e0 = cache[p1]
        G = step(G, idx, idx_e0, 1 - p1, p1, c01, c10)
    return G

def tails_from_growth(G, hd, unit):
    """Xi[k] is valid for sets D with mu(D) <= m_k = exp(-k hd); Theta[k] for sets S with mu(S) >= m_k."""
    T1, K2 = G.shape
    T = T1 - 1; K = K2 - 2
    m = np.exp(-np.arange(K + 1) * hd)
    # lower tail: sum_j (e^{-unit j} - e^{-unit (j+1)}) g(q, j); beyond T the growth is bounded below by G[T]
    wts = np.array([math.exp(-unit * j) - math.exp(-unit * (j + 1)) for j in range(T)] + [math.exp(-unit * T)])
    Theta = (wts[:, None] * G[:, :K + 1]).sum(axis=0)
    # upper tail: sum_{j>=1} (e^{unit j} - e^{unit (j-1)}) * M(q, j-1),  M(q, t) <= m_{kmin-1},
    # kmin = min{k : G[t, k] <= q}  (G[t, .] is nonincreasing in k)
    Xi = np.zeros(K + 1)
    for k in range(K + 1):
        q = m[k]
        tot = 0.0
        for j in range(1, T + 2):
            t = j - 1
            if t > T:
                Mq = 1.0 if G[T, 0] <= q else None
            row = G[min(t, T), :K + 1]
            ok = np.nonzero(row <= q * (1 + 1e-12))[0]
            if len(ok) == 0:
                break                          # no set of any measure on the grid has g(m, t) <= q: interior empty
            kmin = int(ok[0])
            Mq = 1.0 if kmin == 0 else m[kmin - 1]
            tot += (math.exp(unit * j) - math.exp(unit * (j - 1))) * Mq
            if t >= T:
                tot = float('inf'); break      # table too short to bound deeper layers
        Xi[k] = tot
    return m, Xi, Theta

def _site_phi(p1, c01, c10, unit, dgrid, lam=1.0):
    """phi(d) = sup{ r(P) : D(P || mu_i) <= d },  r(P) = min_Q [ D(Q || mu_i) + lam * unit * transport(P, Q) ]
    for a binary site; returned on dgrid together with its least concave majorant."""
    p = p1
    xs = np.linspace(1e-9, 1 - 1e-9, 4001)                 # P(x = 1) under P
    def kl(a, b):
        return a * np.log(a / b) + (1 - a) * np.log((1 - a) / (1 - b))
    D = kl(xs, p)
    # r(x) = min over y of kl(y, p) + lam*unit*( c01 (y - x)_+ + c10 (x - y)_+ )
    Y = xs[None, :]; X = xs[:, None]
    cost = lam * unit * (c01 * np.maximum(Y - X, 0) + c10 * np.maximum(X - Y, 0))
    r = (kl(Y, p) + cost).min(axis=1)
    phi = np.zeros_like(dgrid)
    order = np.argsort(D)
    Ds = D[order]; rs = np.maximum.accumulate(r[order])    # sup over D(P) <= d
    idx = np.searchsorted(Ds, dgrid, side='right') - 1
    phi = np.where(idx >= 0, rs[np.maximum(idx, 0)], 0.0)
    # least concave majorant on the grid (upper hull)
    hull = []
    for i, (d, v) in enumerate(zip(dgrid, phi)):
        while len(hull) >= 2:
            (d1, v1), (d2, v2) = hull[-2], hull[-1]
            if (v2 - v1) * (d - d1) <= (v - v1) * (d2 - d1): hull.pop()
            else: break
        hull.append((d, v))
    hd_, hv_ = zip(*hull)
    return np.interp(dgrid, hd_, hv_)

def theta_laplace(sites, unit, dgrid):
    """exp(-Phi(d)) on dgrid (uniform grid starting at 0): Phi = max-plus convolution of the concave site
    functions.  The grid makes this approximate (from below for Phi up to interpolation error)."""
    Phi = np.zeros_like(dgrid)
    first = True
    for (p1, c01, c10) in sites:
        f = _site_phi(p1, c01, c10, unit, dgrid)
        if first:
            Phi = f.copy(); first = False
        else:
            K = len(dgrid)
            new = np.full(K, -np.inf)
            for i in range(K):
                # d_i = d_j + d_{i-j}
                cand = Phi[:i + 1] + f[i::-1]
                new[i] = cand.max()
            Phi = new
    # safe direction: a real split (d_1, ..., d_n) rounded up to the grid sums to at most d + n*h, so the
    # true Phi(d) is at most the grid value at d + n*h; the site functions carry an error of at most
    # unit * c_max * (grid step of the letter probabilities), added here as well.
    n = len(sites); K = len(dgrid)
    shifted = np.concatenate([Phi[n:], np.full(n, Phi[-1] + n * (dgrid[1] - dgrid[0]))])
    cmax = max(max(c01, c10) for (_, c01, c10) in sites)
    return np.exp(-(shifted + n * unit * cmax * 2.5e-4))

# ---------------------------------------------------------------------------------------------------
def _exhaustive_check(sites, unit, hd):
    """All proper nonempty subsets of a product of at most four sites: the growth bound, the tail
    functions computed from it, and the Laplace closed form, against the definitions."""
    n = len(sites); N = 1 << n
    w = np.empty(N)
    for x in range(N):
        v = 1.0
        for i, (p1, _, _) in enumerate(sites):
            v *= p1 if (x >> i) & 1 else (1 - p1)
        w[x] = v
    def cost(x, y):
        c = 0
        for i, (_, c01, c10) in enumerate(sites):
            xi = (x >> i) & 1; yi = (y >> i) & 1
            if xi != yi: c += c01 if xi == 0 else c10
        return c
    C = [[cost(x, y) for y in range(N)] for x in range(N)]
    T = max(max(r) for r in C)
    G = growth_tables(sites, hd, T)
    m, Xi, Theta = tails_from_growth(G, hd, unit)
    K = len(m) - 1
    dgrid = np.arange(0, K + 1) * hd
    ThL = theta_laplace(sites, unit, dgrid)
    M = 1 << N
    full = M - 1
    low = np.zeros(M, dtype=np.int64)                       # index of the lowest set bit
    for mask in range(1, M):
        low[mask] = (mask & -mask).bit_length() - 1
    meas = np.zeros(M)
    for mask in range(1, M):
        meas[mask] = meas[mask & (mask - 1)] + w[low[mask]]
    def grow_table(nbmask):
        g = np.zeros(M, dtype=np.int64)
        for mask in range(1, M):
            g[mask] = g[mask & (mask - 1)] | nbmask[low[mask]]
        return g
    fwd = [grow_table([sum(1 << z for z in range(N) if C[x][z] <= t) for x in range(N)]) for t in range(T + 1)]
    rev = [grow_table([sum(1 << x for x in range(N) if C[x][z] <= t) for z in range(N)]) for t in range(T + 1)]
    masks = np.arange(1, M - 1)
    mu = meas[masks]
    k_dn = np.minimum(np.ceil(-np.log(mu) / hd - 1e-9).astype(np.int64), K)     # m_k <= mu
    k_up = np.maximum(np.floor(-np.log(mu) / hd + 1e-9).astype(np.int64), 0)    # m_k >= mu
    res = dict(sets=len(masks))
    # growth
    bad = 0; tight = np.inf
    for t in range(T + 1):
        mut = meas[fwd[t][masks]]
        bnd = G[t, k_dn]
        bad += int(np.sum(bnd > mut * (1 + 1e-9)))
        tight = min(tight, float(np.min(mut / bnd)))
    res['bad_growth'] = bad; res['closest_growth'] = tight
    # upper tail of D = mask:  sum_{j>=1} (e^{uj} - e^{u(j-1)}) mu( D minus rev_{j-1}(D^c) )
    comp = full ^ masks
    val = np.zeros(len(masks))
    for j in range(1, T + 1):
        deep = masks & ~rev[j - 1][comp]
        val += (math.exp(unit * j) - math.exp(unit * (j - 1))) * meas[deep]
    xb = Xi[k_up]
    res['bad_xi'] = int(np.sum(val > xb * (1 + 1e-9)))
    res['closest_xi'] = float(np.max(np.where(np.isfinite(xb), val / xb, 0.0)))
    # lower tail of S = mask: sum_{j>=0} (e^{-uj} - e^{-u(j+1)}) mu(S_j), S_T = everything
    lowv = np.zeros(len(masks))
    for j in range(0, T + 1):
        wt = math.exp(-unit * j) - math.exp(-unit * (j + 1)) if j < T else math.exp(-unit * T)
        lowv += wt * meas[fwd[j][masks]]
    res['bad_theta'] = int(np.sum(lowv < Theta[k_dn] * (1 - 1e-9)))
    res['closest_theta'] = float(np.min(lowv / Theta[k_dn]))
    res['bad_laplace'] = int(np.sum(lowv < ThL[k_dn] * (1 - 1e-9)))
    res['closest_laplace'] = float(np.min(lowv / ThL[k_dn]))
    return res

if __name__ == "__main__":
    print("exhaustive validity on products of four binary sites (all proper nonempty subsets):")
    for name, sites, unit in (
            ("uniform, unit cost, u = 1", [(0.5, 1, 1)] * 4, 1.0),
            ("two slopes (1, 1, 2, 2), u = 0.7", [(0.5, 1, 1), (0.5, 1, 1), (0.5, 2, 2), (0.5, 2, 2)], 0.7),
            ("biased and asymmetric", [(0.5, 1, 1), (0.3, 2, 1), (0.2, 1, 1), (0.6, 1, 3)], 0.5)):
        r = _exhaustive_check(sites, unit, 0.01)
        print(f"  {name}: {r['sets']} sets; violations growth/Xi/Theta/Laplace = "
              f"{r['bad_growth']}/{r['bad_xi']}/{r['bad_theta']}/{r['bad_laplace']}; closest: "
              f"mu(E_t)/bound >= {r['closest_growth']:.4f}, value/Xi <= {r['closest_xi']:.4f}, "
              f"value/Theta >= {r['closest_theta']:.4f}, value/Laplace >= {r['closest_laplace']:.4f}")
        assert r['bad_growth'] == r['bad_xi'] == r['bad_theta'] == r['bad_laplace'] == 0
    # uniform cube against the exact Harper-based formulas
    n, u, hd = 14, 1.0, 0.005
    G = growth_tables([(0.5, 1, 1)] * n, hd, n)
    m, Xi, Theta = tails_from_growth(G, hd, u)
    b = [math.comb(n, j) / 2.0 ** n for j in range(n + 1)]
    print(f"uniform cube n={n}, u={u}, hd={hd}: tail functions from the growth DP against the exact ones at ball sizes")
    wx = 0.0; wt = 1.0
    for r in range(0, n - 1):
        q = sum(b[:r + 1])
        xi_ex = sum(b[j] * (math.exp(u * (r - j + 1)) - 1) for j in range(r + 1))
        th_ex = sum(b[j] * math.exp(-u * max(j - r, 0)) for j in range(n + 1))
        kx = int(math.floor(-math.log(q) / hd + 1e-9)); kt = int(math.ceil(-math.log(q) / hd - 1e-9))
        if kx < 1 or not np.isfinite(Xi[kx]):
            continue                               # q rounds up to 1 on the grid: no statement
        rx = Xi[kx] / xi_ex; rt = Theta[kt] / th_ex
        assert rx >= 1 - 1e-9 and rt <= 1 + 1e-9
        wx = max(wx, rx); wt = min(wt, rt)
    print(f"  largest Xi(DP)/Xi(exact) = {wx:.4f}; smallest Theta(DP)/Theta(exact) = {wt:.4f}  (grid slack n*hd = {n*hd:.3f})")
    print("ALL CHECKS PASSED")
