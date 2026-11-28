"""Baselines B1-B5 and the methods M5/M6 of the Phase II protocol (PROTOCOL.md section 3).

Lumping (Proposition 8.1) is used wherever a problem is built on a sample: points with equal (phi, f, L, U) are
merged with their multiplicities as weights.  This is an exact identity of the problem (the sums in Psi are
unchanged), used only for speed.  A bootstrap resample is a multinomial draw of those multiplicities, which is the
same law as resampling the points.
"""
from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import logsumexp

from instances import ci

N_BOOT = 200
N_GRID = 32


# ------------------------------------------------------------------------------------------------ helpers
def lump_sample(f, phi, L, U):
    key = np.column_stack([phi, f, L, U])
    uq, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
    m = phi.shape[1]
    return uq[:, m], uq[:, :m], uq[:, m + 1], uq[:, m + 2], cnt.astype(float)


def _ends(P):
    hi = ci.solve_upper(P)[0]
    lo = -ci.solve_upper(P.negated())[0]
    return lo, hi


# ------------------------------------------------------------------------------------------------ B1
def b1_bootstrap(f, phi, L, U, region, rng, n_boot: int = N_BOOT):
    """Plug-in sharp bounds on the sample (dual via ci.solve_upper, empirical measure) and a percentile bootstrap:
    nominal 95 % interval [2.5 % quantile of the lower end, 97.5 % quantile of the upper end]."""
    n = f.size
    uf, uphi, uL, uU, cnt = lump_sample(f, phi, L, U)
    P = ci.Problem(uf, uphi, Lw=uL, Gw=uU - uL, region=region, wt=cnt / n)
    plo, phi_ = _ends(P)
    los, his = [], []
    for _ in range(n_boot):
        cb = rng.multinomial(n, cnt / n).astype(float)
        keep = cb > 0
        Pb = ci.Problem(uf[keep], uphi[keep], Lw=uL[keep], Gw=uU[keep] - uL[keep], region=region, wt=cb[keep] / n)
        lo, hi = _ends(Pb)
        if hi < lo - 1e-9 or not math.isfinite(hi) or not math.isfinite(lo):
            los.append(np.nan)
            his.append(np.nan)
        else:
            los.append(lo)
            his.append(hi)
    los, his = np.array(los), np.array(his)
    n_empty = int(np.isnan(los).sum())
    if n_empty == n_boot:
        return dict(lo=math.nan, hi=math.nan, plug_lo=plo, plug_hi=phi_, n_empty=n_empty, n_unique=int(uf.size))
    return dict(lo=float(np.nanquantile(los, 0.025)), hi=float(np.nanquantile(his, 0.975)), plug_lo=float(plo),
                plug_hi=float(phi_), n_empty=n_empty, n_unique=int(uf.size))


# ------------------------------------------------------------------------------------------------ B2
def b2_maxent(f, phi, centre):
    """Weights proportional to exp(-lam . phi) on the sample, lam fitted so that the reweighted averages equal the
    centre of the data.  Returns the reweighted target and Kish's effective sample size."""
    n = f.size
    uf, uphi, _, _, cnt = lump_sample(f, phi, np.zeros(n), np.zeros(n))
    lc = np.log(cnt)
    c = np.asarray(centre, float)

    def obj(lam):
        a = lc - uphi @ lam
        lse = logsumexp(a)
        w = np.exp(a - lse)
        return lse + lam @ c, c - w @ uphi

    r = minimize(obj, np.zeros(uphi.shape[1]), jac=True, method="BFGS", options=dict(gtol=1e-10, maxiter=2000))
    a = lc - uphi @ r.x
    w = np.exp(a - logsumexp(a))
    resid = float(np.abs(w @ uphi - c).max())
    ok = resid < 1e-6
    wpt = w / cnt                              # weight of one draw
    kish = float(1.0 / (cnt @ wpt ** 2))
    return dict(value=float(w @ uf), kish=kish, resid=resid, ok=bool(ok), lam=r.x.tolist())


# ------------------------------------------------------------------------------------------------ B3
def b3_pool(f, phi, region):
    """Model-free linear programme on the sampled pool: Lw = 0, Gw = 1 on the sampled points."""
    n = f.size
    uf, uphi, _, _, _ = lump_sample(f, phi, np.zeros(n), np.zeros(n))
    out = ci.interval(ci.Problem(uf, uphi, Lw=0.0, Gw=1.0, region=region))
    return dict(lo=float(out["lo"]), hi=float(out["hi"]), empty=bool(out["empty"]), n_unique=int(uf.size))


# ------------------------------------------------------------------------------------------------ B4
def b4_information(pi, f, rho_max: float, f_lo=-1.0, f_hi=1.0):
    """E_p f - E_pi f <= inf_c [ln E_pi e^{c(f - E_pi f)} + rho^2/2]/c (and the same for -f), exact on the space."""
    uf, inv = np.unique(f, return_inverse=True)
    w = np.bincount(inv, weights=pi)
    w = w / w.sum()
    mean = float(w @ uf)
    kl = rho_max ** 2 / 2

    def one(g, gm):
        def val(t):
            c = math.exp(t)
            return (float(logsumexp(c * (g - gm), b=w)) + kl) / c
        r = minimize_scalar(val, bounds=(-12, 8), method="bounded", options=dict(xatol=1e-10))
        return min(val(r.x), val(-12), val(8))

    hi = mean + one(uf, mean)
    lo = mean - one(-uf, -mean)
    return dict(lo=max(lo, f_lo), hi=min(hi, f_hi), mean=mean)


# ------------------------------------------------------------------------------------------------ B5
def b5_no_data(pi, f, rho_vec):
    """The threshold rule without data (m = 0), exact on the space (lumped by (f, rho))."""
    key = np.column_stack([f, rho_vec])
    uq, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.reshape(-1)
    l = np.bincount(inv, weights=pi * np.exp(-rho_vec))
    u = np.bincount(inv, weights=pi * np.exp(rho_vec))
    out = ci.interval(ci.box_problem(l, u, uq[:, 0], np.zeros((len(uq), 0)), ci.Box()))
    return dict(lo=float(out["lo"]), hi=float(out["hi"]))


# ------------------------------------------------------------------------------------------------ M5 / M6
def _spread(eta, phi_lo, phi_hi, h):
    a, b = eta * phi_lo, eta * phi_hi
    return h - float(np.maximum(a, b).sum()), h - float(np.minimum(a, b).sum())


def m56_upper(f_va, phi_va, L_va, U_va, eta, tau_train, region, dec, L_max: float, delta_end: float, kind: str):
    """M5 (Hoeffding) / M6 (empirical Bernstein): the same eta as M3, 32 thresholds between the training optimum
    and the top of the range, each tested at level delta_end/32 with the a-priori range of psi = U s+ - L s-.
    The certified end is the smallest threshold whose upper confidence bound is <= 0."""
    eta = np.asarray(eta, float).reshape(-1)
    ucb = ci.hoeffding_ucb if kind == "hoeffding" else ci.bernstein_ucb
    h = region.h(eta)
    sl, sh = _spread(eta, dec.phi_lo, dec.phi_hi, h)
    s_min, s_max = dec.f_lo + sl, dec.f_hi + sh
    s0 = f_va - phi_va @ eta + h
    t0 = tau_train if math.isfinite(tau_train) else dec.f_lo
    t0 = min(max(t0, dec.f_lo), dec.f_hi)
    grid = np.linspace(t0, dec.f_hi, N_GRID)
    lev = delta_end / N_GRID
    for tau in grid:
        s = s0 - tau
        z = U_va * np.maximum(s, 0.0) - L_va * np.maximum(-s, 0.0)
        lo_r = -L_max * max(tau - s_min, 0.0)
        hi_r = dec.U_max * max(s_max - tau, 0.0)
        if hi_r <= lo_r:
            if np.mean(z) <= 0:
                return float(tau), "certified"
            continue
        if ucb(z, lo_r, hi_r, lev) <= 0.0:
            return float(tau), "certified"
    return float(dec.f_hi), "trivial"


def m56_interval(valid, up, low, region, dec, L_max, delta, kind):
    """Both ends at delta/2 each, with the multipliers of M3's two certificates (Bound objects ``up``, ``low``)."""
    if up.status in ("abstain", "void") or low.status in ("abstain", "void"):
        return dict(lo=dec.f_lo, hi=dec.f_hi, st_lo=low.status, st_hi=up.status)
    hi, sh = m56_upper(valid.f, valid.phi, valid.L, valid.U, up.eta, up.tau_train, region, dec, L_max, delta / 2, kind)
    nd = dec.negated()
    lo_neg, sl = m56_upper(-valid.f, valid.phi, valid.L, valid.U, low.eta, -low.tau_train, region, nd, L_max, delta / 2, kind)
    return dict(lo=-lo_neg, hi=hi, st_lo=sl, st_hi=sh)
