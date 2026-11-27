"""
instances.py -- outer landscapes for the unit engine of r6lib (workstream R6).

A radial instance is  psi(a,b) = -F(d(a,c)) + s_in |b|  on Q_{n_o} x Q_{n_i}:  u-Lipschitz iff |F(d+1)-F(d)| <= u
and |s_in| <= u.  Fibre averages: W(a) = e^{F(d(a,c))} * A_in,  A_in = ((1+e^{-s_in})/2)^{n_i}.  We store
lnW(d) = F(d) (the constant ln A_in is absorbed into F) and the anchor offset kap = -ln A_in, so that
-psi(a, 0_i) = lnW + kap.  The reference point 0^n lies in the shell d0 of the centre c.
Classes = (shell, inner behaviour); the probability of a shell is C(n_o,d)/2^{n_o} (exact).
"""
import math
import numpy as np
import mpmath as mp
from r6lib import ClassInstance, Tables
import r6lib as R


def kap_of_slope(n_i, s_in):
    """anchor offset of the inner landscape s_in*|b|:  kap = -ln A_in = n_i ln(2/(1+e^{-s_in}))."""
    return float(n_i * math.log(2.0 / (1.0 + math.exp(-s_in))))


def radial(n, n_o, u, F, d0=0, s_in=0.0, strats=(R.S_CENTER,), weights=None, name=""):
    F = np.asarray(F, dtype=np.float64)
    assert len(F) == n_o + 1
    assert np.all(np.abs(np.diff(F)) <= u + 1e-12), "profile is not u-Lipschitz"
    assert abs(s_in) <= u + 1e-12
    n_i = n - n_o
    kap = kap_of_slope(n_i, s_in)
    if weights is None:
        weights = [mp.mpf(1) / len(strats)] * len(strats)
    lnW, prob, strat = [], [], []
    two = mp.mpf(2) ** n_o
    ref = None
    for d in range(n_o + 1):
        pd = mp.mpf(math.comb(n_o, d)) / two
        for s, w in zip(strats, weights):
            if d == d0 and ref is None:
                ref = len(lnW)
            lnW.append(F[d])
            prob.append(pd * w)
            strat.append(s)
    return ClassInstance(n, n_o, u, lnW, prob, kap, strat, ref, name=name)


# ---- profiles (lnW as a function of the distance d from the centre) -------------------------------------
def prof_flat(n_o, u):
    return np.zeros(n_o + 1)


def prof_cone(n_o, u, slope=None):
    s = u if slope is None else slope
    return -s * np.arange(n_o + 1, dtype=float)


def prof_dip(n_o, u, R_):
    """flat bulk with a peak of the weight (a dip of psi) of radius R_ at the centre."""
    d = np.arange(n_o + 1, dtype=float)
    return u * np.maximum(R_ - d, 0.0)


def prof_flattened_cone(n_o, u, R_):
    d = np.arange(n_o + 1, dtype=float)
    return -u * np.maximum(d, R_)


def prof_plateau_cone(n_o, u, R_):
    d = np.arange(n_o + 1, dtype=float)
    return -u * np.maximum(d - R_, 0.0)


def prof_equal_mass(n_o, u):
    """W(d) ~ 1/|B(n_o,d)| as far as the slope allows: every level carries about the same s p(s)."""
    F = [0.0]
    b = [sum(math.comb(n_o, j) for j in range(d + 1)) for d in range(n_o + 1)]
    for d in range(1, n_o + 1):
        step = min(u, math.log(b[d] / b[d - 1]))
        F.append(F[-1] - step)
    return np.array(F)


def prof_random_walk(n_o, u, rng, kind="uniform"):
    if kind == "uniform":
        steps = rng.uniform(-u, u, size=n_o)
    elif kind == "pm":
        steps = rng.choice([-u, u], size=n_o)
    elif kind == "down":
        steps = -rng.uniform(0, u, size=n_o)
    elif kind == "lazy":
        steps = rng.choice([-u, 0.0, 0.0, 0.0, u], size=n_o)
    else:
        raise ValueError(kind)
    return np.concatenate([[0.0], np.cumsum(steps)])


def prof_alternating(n_o, u):
    return (u / 2) * (-1.0) ** np.arange(n_o + 1)


def prof_staircase(n_o, u, step_every, height):
    """descending staircase: drops by `height` (<= u) every `step_every` shells."""
    d = np.arange(n_o + 1)
    return -height * (d // step_every).astype(float)


def snap_to_levels(F, ln_s0, lam, b, mode, u):
    """
    move the profile values onto the level grid (ties):  mode 'level' -> W in {s_j},  'tol' -> W in {s_j e^{-b}}.
    The snapped profile is re-checked for the Lipschitz condition by the caller (radial()).
    Rounding is downward in multiples of lam, so steps change by less than lam; use only with lam + step <= u.
    """
    F = np.asarray(F, dtype=float)
    off = 0.0 if mode == "level" else -float(b)
    j = np.floor((F - ln_s0 - off) / lam)
    return np.array([float(mp.mpf(ln_s0) + int(jj) * mp.mpf(lam) + off) for jj in j])
