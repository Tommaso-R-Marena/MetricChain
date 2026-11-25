"""Workstream F -- exact finite-n exponents (binomial sums) for
  * the hinted lower bound at a permutation-symmetric instance w0(type): dips on density balls;
  * the non-adaptive lower bound: a cone flattened on a density ball.
Each returns n^{-1} ln(1/max_type density) of the smallest set whose effect exceeds eps."""
import math
import numpy as np
from scipy.special import logsumexp
from birad import *


def dip_effect(C, logw0_t, inside, u):
    """ln A(w') - ln A(w0) for the deepest admissible dip supported on `inside` at the symmetric instance"""
    lw0 = logw0_t[C.t]
    lw1 = np.where(inside, C.lower_envelope_logw(lw0, inside, u), lw0)
    return C.logA(lw1) - C.logA(lw0)


def flatten_drop(C, inside, u):
    """ln A(cone) - ln A(cone flattened on `inside`): the smallest weights on `inside` compatible with the cone outside"""
    lw0 = -u * C.dist.astype(float)
    lw1 = np.where(inside, C.upper_envelope_logw(lw0, inside, u), lw0)
    return C.logA(lw0) - C.logA(lw1)


def smallest_set(C, effect_fn, eps, lo=None):
    """bisection on ln q for the smallest density ball with effect > eps; returns (-ln maxdens)/n or None"""
    n = C.n
    hi = 0.0
    if lo is None:
        lo = -n * math.log(2) - 5
    ins, mx = C.density_ball(hi - 1e-9)
    if effect_fn(C, ins) <= eps:
        return None
    for _ in range(34):
        mid = (lo + hi) / 2
        ins, mx = C.density_ball(mid)
        if ins.any() and (~ins).any() and effect_fn(C, ins) > eps:
            hi = mid
        else:
            lo = mid
    ins, mx = C.density_ball(hi)
    return -mx / n


def best_over_centres(n, p, u, eps, kind, logw0_t=None, kgrid=None, refine=True):
    """max over the centre weight k of the exponent; kind = 'dip' (needs logw0_t) or 'flatten'"""
    if kind == "dip":
        fn = lambda C, ins: dip_effect(C, logw0_t, ins, u)
    else:
        fn = lambda C, ins: flatten_drop(C, ins, u)
    def val(k):
        C = Centre(n, int(k), p)
        r = smallest_set(C, fn, eps)
        return -1.0 if r is None else r
    if kgrid is None:
        kgrid = sorted(set(int(round(x)) for x in np.linspace(0.06 * n, 0.94 * n, 23)))
    vals = [val(k) for k in kgrid]
    i = int(np.argmax(vals))
    best, kb = vals[i], kgrid[i]
    if refine:
        lo, hi = kgrid[max(i - 1, 0)], kgrid[min(i + 1, len(kgrid) - 1)]
        while hi - lo > 2:
            m1 = lo + (hi - lo) // 3
            m2 = hi - (hi - lo) // 3
            v1, v2 = val(m1), val(m2)
            if v1 > best: best, kb = v1, m1
            if v2 > best: best, kb = v2, m2
            if v1 < v2: lo = m1
            else: hi = m2
    return best, kb
