"""Exact type-class sums for dips and cones on the p-biased cube (float64 in the log domain).

A centre s with k ones; a point x is described by (kappa, j): kappa = |x|, j = #{i : x_i = s_i = 1}.
  number of x for a given s:        N(kappa,j) = C(k,j) C(n-k, kappa-j)
  number of s in T_k for a given x: C(kappa,j) C(n-kappa, k-j)
  d(x,s) = k + kappa - 2j
Everything below is a finite sum over the (n+1)(k+1) classes; no asymptotics.
"""
import numpy as np
from scipy.special import gammaln, logsumexp
from sl import pgam, site_laws


def lbinom(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ok = (b >= 0) & (b <= a)
    out = np.full(np.broadcast(a, b).shape, -np.inf)
    aa, bb = np.broadcast_arrays(a, b)
    out[ok] = gammaln(aa[ok] + 1) - gammaln(bb[ok] + 1) - gammaln(aa[ok] - bb[ok] + 1)
    return out


class Grid:
    def __init__(self, n, p, u, k):
        self.n, self.p, self.u, self.k = n, p, u, k
        q = 1 - p
        kap = np.arange(n + 1)[:, None]            # kappa
        j = np.arange(k + 1)[None, :]
        self.kap, self.j = kap, j
        self.valid = (j <= kap) & (kap - j <= n - k)
        self.lN = lbinom(k, j) + lbinom(n - k, kap - j)                   # ln #x per centre
        self.lS = lbinom(kap, j) + lbinom(n - kap, k - j) - lbinom(n, k)  # ln P_s(joint type | x)
        self.lNT = lbinom(n, kap)                                          # ln |T_kappa|
        self.d = k + kap - 2 * j
        self.lpi = kap * np.log(p) + (n - kap) * np.log(q)                # ln pi(x)
        self.lZs = k * np.log(p + q * np.exp(-u)) + (n - k) * np.log(q + p * np.exp(-u))
        self.lcone = self.lpi - u * self.d - self.lZs                     # ln pi_s(x)

    def lprod(self, gamma):
        """ln pi_gamma^n(x)"""
        pg = pgam(self.p, gamma)
        return self.kap * np.log(pg) + (self.n - self.kap) * np.log1p(-pg) + 0 * self.j


def dip(G, gamma, r):
    """dip of depth r at a centre of type k on the normalised additive component gamma.
    returns E (excess mass), c_E (its one-body density), lhit = ln max_kappa P_{s in T_k}(x in D_s), mask D"""
    lb = G.lprod(gamma)
    a = r + G.lcone
    D = G.valid & (a > lb)
    if not D.any():
        return 0.0, np.nan, -np.inf, D
    with np.errstate(divide='ignore', invalid='ignore', over='ignore'):
        lterm = np.where(D, G.lN + a + np.log1p(-np.exp(np.minimum(lb - a, 0.0)) + 1e-300 * 0), -np.inf)
    lE = logsumexp(lterm)
    w = np.exp(lterm - lE)
    cE = float((w * G.kap).sum() / G.n)
    lh = np.where(D, G.lS, -np.inf)
    lhit_k = logsumexp(lh, axis=1)
    return float(np.exp(lE)), cE, float(lhit_k.max()), D


def compensated_dip(n, p, u, gamma, k, eps, G=None):
    """smallest depth r with ln(1 + E/(1+b)) > eps; returns the dict of everything."""
    G = G or Grid(n, p, u, k)
    p1 = pgam(p, gamma)

    def build(r):
        E, cE, lhit, D = dip(G, gamma, r)
        if E == 0.0:
            return None
        g2 = -u if cE > p1 else u
        p2 = pgam(p, g2)
        b = (cE - p1) / (p2 - cE) if cE != p1 else 0.0
        sep = np.log1p(E / (1 + b)) if b >= 0 else -np.inf
        return dict(r=r, E=E, cE=cE, lhit=lhit, g2=g2, p2=p2, b=b, sep=sep, D=D)
    lo, hi = -50.0, eps + 30.0
    for _ in range(60):
        mid = (lo + hi) / 2
        B = build(mid)
        if B is not None and B['sep'] > eps: hi = mid
        else: lo = mid
    B = build(hi)
    B['lnLB'] = -np.log(n) - B['lhit']            # ln of the bound on E|Q| without the factor (1-2 delta)
    B['p1'] = p1
    return B


def uncompensated_dip(n, p, u, gamma, k, eps, G=None):
    """the classical bound (no oracle): smallest r with ln(1+E) > eps"""
    G = G or Grid(n, p, u, k)
    lo, hi = -50.0, eps + 30.0
    for _ in range(60):
        mid = (lo + hi) / 2
        E, cE, lhit, D = dip(G, gamma, mid)
        if np.log1p(E) > eps: hi = mid
        else: lo = mid
    E, cE, lhit, D = dip(G, gamma, hi)
    return dict(r=hi, E=E, cE=cE, lhit=lhit, lnLB=-lhit)


# ------------------------------------------------------------------ cones and their type-wise truncations

def truncated_cone(G, lq):
    """type-wise truncation of the (normalised) cone at upper quantiles of density <= q = e^{lq}.
    returns ln A_c (=0), A_t, densities c_0, c_t, c_Delta, and the largest density of the difference set"""
    n, k, u = G.n, G.k, G.u
    # density of {j' > j} in T_kappa
    lNn = np.where(G.valid, G.lN - G.lNT, -np.inf)
    # cumulative from the top over j
    rev = lNn[:, ::-1]
    cum = np.logaddexp.accumulate(rev, axis=1)[:, ::-1]        # ln density{j' >= j}
    above = np.concatenate([cum[:, 1:], np.full((n + 1, 1), -np.inf)], axis=1)   # ln density{j' > j}
    # j* = min{ j valid : density{j'>j} <= q }
    okj = G.valid & (above <= lq)
    jstar = np.where(okj.any(1), okj.argmax(1), -1)             # first True along j
    lw = G.lcone - G.lpi                                        # ln normalised cone weight, per class
    lt = np.array([lw[kk, jstar[kk]] if jstar[kk] >= 0 else np.inf for kk in range(n + 1)])[:, None]
    flat = G.valid & (G.j > jstar[:, None])                     # the truncated (flattened) region
    lwt = np.where(flat, lt + 0 * lw, lw)
    lA_c_terms = np.where(G.valid, G.lN + G.lpi + lw, -np.inf)
    lA_t_terms = np.where(G.valid, G.lN + G.lpi + lwt, -np.inf)
    lAc = logsumexp(lA_c_terms); lAt = logsumexp(lA_t_terms)
    c0 = float((np.exp(lA_c_terms - lAc) * G.kap).sum() / n)
    ct = float((np.exp(lA_t_terms - lAt) * G.kap).sum() / n)
    # removed mass
    with np.errstate(divide='ignore', invalid='ignore'):
        lrem = np.where(flat, G.lN + G.lpi + lw + np.log1p(-np.exp(np.minimum(lwt - lw, 0.0))), -np.inf)
    lAd = logsumexp(lrem)
    cD = float((np.exp(lrem - lAd) * G.kap).sum() / n) if np.isfinite(lAd) else np.nan
    ldens = logsumexp(np.where(flat, lNn, -np.inf), axis=1).max()
    return dict(lAc=float(lAc), lAt=float(lAt), lAd=float(lAd), c0=c0, ct=ct, cD=cD, ldens=float(ldens), flat=flat)


def compensated_pair(n, p, u, k, lq, G=None):
    """the non-adaptive pair with compensation.  w = truncated cone (mass A_t, density c_t), Delta = removed mass.
    b = A_t (c_D - c_t)/(p_2 - c_D);  separation = ln(1 + A_D/(A_t + b))."""
    G = G or Grid(n, p, u, k)
    T = truncated_cone(G, lq)
    if not np.isfinite(T['lAd']):
        return None
    At, Ad = np.exp(T['lAt']), np.exp(T['lAd'])
    cD, ct = T['cD'], T['ct']
    g2 = -u if cD > ct else u
    p2 = pgam(p, g2)
    b = At * (cD - ct) / (p2 - cD) if cD != ct else 0.0
    T.update(g2=g2, p2=p2, b=b, sep=(np.log1p(Ad / (At + b)) if b >= 0 else -np.inf), sep0=np.log1p(Ad / At))
    return T
