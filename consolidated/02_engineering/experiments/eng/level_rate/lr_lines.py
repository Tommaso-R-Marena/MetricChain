"""The line dynamics of R_REPORT sections 2-4 and the lower bound tau_k >= B_inf(k) (method (b)).

The slope map (R_REPORT section 2):

    Sigma(B, s) = sup_{e>0} [B - (1 - s) theta(e)]/e
                = the least sigma' >= 0 with (1 - s) theta(e) + sigma' e >= B for all e > 0            (Sigma-3)

In terms of the dual function J(t) = inf_e [(1 - t) theta(e) + t e] (R_REPORT (Sigma-5)): with
tau = sigma'/(1 - s + sigma'),  inf_e [(1 - s) theta(e) + sigma' e] = (1 - s) J(tau)/(1 - tau), hence

    Sigma(B, s) = t' (1 - s)/(1 - t'),     t' = the least t in [0, 1) with Q(t) := J(t)/(1 - t) >= B/(1 - s),

finite iff B/(1 - s) < a = sup Q.  The orbit of the flat line: p_0 = 0, p_{j+1}(B) = Sigma(B, p_j(B)).

Proposition A of R_REPORT (proved there; Lemma L re-derived by hand for this check, see the report text):
if p_k(B) < infinity then T_k(x) >= B - p_k(B) x for all x > 0, hence

    tau_k >= B_inf(k) := sup{B : p_k(B) < infinity}.

p_k(B) is finite iff B/(1 - p_j(B)) < a for j = 0..k-1 (up to the boundary case of equality, which does not
change the supremum).

Implemented here:
* ``sigma_dual``      the slope map through J (double precision, vectorised);
* ``sigma_def``       the slope map from its definition as a supremum over e (independent route; for tests);
* ``survives``, ``b_inf``     the orbit and B_inf(k) by multisection (double precision);
* ``b_inf_mp``        the same in mpmath (any precision);
* ``gauss_exact``     the Gaussian pair in rational arithmetic (exact): the largest N with p_k(N/10^d) < infinity;
* ``gauss_closed_form_root``  the closed form of R_REPORT section 10;
* ``certify_lower``   a rigorous check "p_k(B) < infinity" for products of symmetric binary sites in interval
                      arithmetic (every rounding goes in the unfavourable direction);
* ``passage_time``    N_t(delta) of R_REPORT section 7.
"""
from __future__ import annotations

import math
from fractions import Fraction

import mpmath as mp
import numpy as np
from mpmath import iv

GR = (math.sqrt(5) - 1) / 2


# ----------------------------------------------------------------------------------------------------------------
# Q^{-1}
# ----------------------------------------------------------------------------------------------------------------
def q_inverse(pair, c, t0=None, tol: float = 5e-15, maxit: int = 100):
    """The least t in [0, 1) with J(t) >= c (1 - t), for arrays c with 0 < c < a.

    Smooth pairs: Newton's method on phi(t) = F(t) - c (1 - t), which is concave and crosses zero from below
    at the root; from any point where phi <= 0 the iteration increases monotonically to the root, and from a
    point where phi > 0 one step lands on the left of it.  The iteration stops when the step is below ``tol``
    (the rounding noise of F limits the root to a few 1e-16).  Other pairs: bisection."""
    c = np.asarray(c, dtype=float)
    if getattr(pair, "smooth", True):
        t = np.zeros(c.shape) if t0 is None else np.array(t0, dtype=float, copy=True)
        done = np.zeros(c.shape, dtype=bool)
        for it in range(maxit):
            phi = pair.F(t) - c * (1.0 - t)
            dphi = pair.dF(t) + c
            tn = np.clip(t - phi / dphi, 0.0, 1.0 - 2.3e-16)
            # in exact arithmetic the iterates increase after the first step: a step to the left is rounding noise
            done |= (np.abs(tn - t) <= tol) | ((it >= 1) & (tn <= t))
            t = np.where(done & (it >= 1) & (tn < t), t, tn)
            if np.all(done):
                break
        return t
    lo = np.zeros(c.shape)
    hi = np.full(c.shape, 1.0 - 1e-16)
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        ok = pair.J(mid) >= c * (1.0 - mid)
        hi = np.where(ok, mid, hi)
        lo = np.where(ok, lo, mid)
    return hi


def sigma_dual(pair, B, s, t0=None):
    """Sigma(B, s) through the dual function; inf where B >= (1 - s) a.  Returns (sigma', t')."""
    B = np.asarray(B, dtype=float)
    s = np.asarray(s, dtype=float)
    y = 1.0 - s
    with np.errstate(divide="ignore", invalid="ignore"):
        c = np.where(y > 0, B / y, np.inf)
    fin = c < pair.a
    t = q_inverse(pair, np.where(fin, c, 0.5 * pair.a), t0)
    sig = np.where(fin, t * y / (1.0 - t), np.inf)
    return sig, t


def sigma_def(pair, B: float, s: float, n: int = 40001) -> float:
    """Sigma(B, s) = sup_{e>0} [B - (1 - s) theta(e)]/e from the definition: a scan over the graph of theta_na
    (curve parameter t) followed by golden-section refinement.  Scalar; for tests.  (The limit e -> infinity
    gives 0; for e >= E the ratio is B/e <= B/E, attained at the end of the curve.)"""
    ts = np.linspace(1e-7, 1 - 1e-7, n)
    x, th = pair.curve(ts)
    val = (B - (1 - s) * th) / x
    k = int(np.argmax(val))
    lo, hi = ts[max(k - 1, 0)], ts[min(k + 1, n - 1)]

    def f(tt):
        xx, tth = pair.curve(np.array(tt))
        return float((B - (1 - s) * tth) / xx)

    c, d = hi - GR * (hi - lo), lo + GR * (hi - lo)
    fc, fd = f(c), f(d)
    for _ in range(90):
        if fc >= fd:
            hi, d, fd = d, c, fc
            c = hi - GR * (hi - lo)
            fc = f(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + GR * (hi - lo)
            fd = f(d)
    return max(fc, fd, float(val[k]), B / pair.E, 0.0)


# ----------------------------------------------------------------------------------------------------------------
# orbits, double precision
# ----------------------------------------------------------------------------------------------------------------
def orbit(pair, B: float, k: int):
    """[p_0, p_1, ..., p_k](B) (inf from the first infinite value on)."""
    out = [0.0]
    s = np.array(0.0)
    t = None
    for _ in range(k):
        if not np.isfinite(s):
            out.append(math.inf)
            continue
        s, t = sigma_dual(pair, np.array(B), s, t)
        out.append(float(s))
    return out


def survives(pair, B, k: int):
    """Boolean array: p_k(B) < infinity."""
    B = np.asarray(B, dtype=float)
    a = pair.a
    y = np.ones(B.shape)                         # y = 1 - s
    alive = np.ones(B.shape, dtype=bool)
    t = np.zeros(B.shape)
    for _ in range(k):
        with np.errstate(divide="ignore", invalid="ignore"):
            c = np.where(y > 0, B / np.where(y > 0, y, 1.0), np.inf)
        alive &= c < a
        if not alive.any():
            break
        cc = np.where(alive, c, 0.5 * a)
        t = q_inverse(pair, cc, np.where(alive, t, 0.0))
        y = np.where(alive, 1.0 - t * y / (1.0 - t), 0.0)       # the new slope is t' (1 - s)/(1 - t')
    return alive


def b_inf(pair, k: int, m: int = 32, rel: float = 1e-15):
    """B_inf(k) = sup{B : p_k(B) < infinity} by multisection on [h, a] (double precision)."""
    lo, hi = pair.h, pair.a                      # lo survives (B <= h: the orbit converges), hi does not
    if k <= 1:
        return pair.a
    while hi - lo > rel * hi:
        Bs = lo + (hi - lo) * np.arange(1, m + 1) / (m + 1)
        ok = survives(pair, Bs, k)
        # survival is monotone in B (Sigma is nondecreasing in B and s)
        n_ok = int(np.sum(ok))
        if n_ok and not np.all(ok[:n_ok]):
            n_ok = int(np.argmin(ok))            # first failure
        new_lo = Bs[n_ok - 1] if n_ok > 0 else lo
        new_hi = Bs[n_ok] if n_ok < m else hi
        if new_lo == lo and new_hi == hi:
            break
        lo, hi = new_lo, new_hi
    return lo


def passage_time(pair, delta: float, s_t: float, nmax: int = 10**7) -> int:
    """N_t(delta) = min{n : p_n(h + delta) > s_t} (R_REPORT section 7)."""
    B = np.array(pair.h + delta)
    s = np.array(0.0)
    t = None
    for n in range(1, nmax + 1):
        s, t = sigma_dual(pair, B, s, t)
        if not np.isfinite(s) or s > s_t:
            return n
    raise RuntimeError("passage not completed")


# ----------------------------------------------------------------------------------------------------------------
# mpmath
# ----------------------------------------------------------------------------------------------------------------
def _q_inverse_mp(pair, c, t0, tol):
    """The least t in [0, 1) with F(t) >= c (1 - t), in mpmath.  Newton's method from t0 (a point where
    F(t0) <= c (1 - t0): zero or the previous root); phi(t) = F(t) - c (1 - t) also vanishes at t = 1, so an
    iterate that leaves [t0, 1) or meets a nonpositive slope switches to bisection on the monotone predicate
    "F(t) >= c (1 - t)" (Q = F/(1 - t) is nondecreasing)."""
    one = mp.mpf(1)
    lo = t0 if t0 > 0 else mp.mpf(10) ** (-(mp.mp.dps // 2))
    t = lo
    for it in range(400):
        phi = pair.F_mp(t) - c * (1 - t)
        if phi <= 0 and t > lo:
            lo = t
        dphi = mp.diff(pair.F_mp, t) + c
        if dphi <= 0:
            break
        tn = t - phi / dphi
        if tn >= one or tn < lo:
            break
        if abs(tn - t) <= tol:
            return tn
        if it >= 1 and tn <= t:                  # monotone from the left in exact arithmetic: this is noise
            return t
        t = tn
    # bisection: lo has F < c (1 - lo); find hi with F >= c (1 - hi)
    hi = None
    gap = (one - lo) / 2
    for _ in range(4 * mp.mp.dps):
        cand = one - gap
        if pair.F_mp(cand) >= c * (1 - cand):
            hi = cand
            break
        gap /= 2
    if hi is None:
        raise RuntimeError("no point with Q >= c found below 1")
    for _ in range(4 * mp.mp.dps):
        mid = (lo + hi) / 2
        if pair.F_mp(mid) >= c * (1 - mid):
            hi = mid
        else:
            lo = mid
        if hi - lo <= tol:
            break
    return hi


def survives_mp(pair, B, k: int, a=None) -> bool:
    a = pair.constants(mp.mp.dps)["a"] if a is None else a
    tol = mp.mpf(10) ** (-(mp.mp.dps - 5))
    y = mp.mpf(1)
    t = mp.mpf(0)
    for _ in range(k):
        if y <= 0:
            return False
        c = B / y
        if c >= a:
            return False
        t = _q_inverse_mp(pair, c, t, tol)
        y = 1 - t * y / (1 - t)
    return True


def b_inf_mp(pair, k: int, dps: int = 30, digits: int = 20):
    """B_inf(k) in mpmath: bisection to ``digits`` significant digits of B - h, at ``dps`` working digits."""
    old = mp.mp.dps
    mp.mp.dps = dps
    try:
        cst = pair.constants(dps)
        a, h = cst["a"], cst["h"]
        if k <= 1:
            return a
        lo, hi = h, a
        # start from the double-precision value to save iterations
        b0 = mp.mpf(b_inf(pair, k))
        w = (b0 - h) * mp.mpf("1e-9") + mp.mpf("1e-15")
        if survives_mp(pair, b0 - w, k, a) and not survives_mp(pair, b0 + w, k, a):
            lo, hi = b0 - w, b0 + w
        while (hi - lo) > (lo - h) * mp.mpf(10) ** (-digits):
            mid = (lo + hi) / 2
            if survives_mp(pair, mid, k, a):
                lo = mid
            else:
                hi = mid
        return lo
    finally:
        mp.mp.dps = old


# ----------------------------------------------------------------------------------------------------------------
# the Gaussian pair, exactly
# ----------------------------------------------------------------------------------------------------------------
def gauss_survives_exact(B: Fraction, k: int) -> bool:
    """p_k(B) < infinity for the Gaussian pair, in rational arithmetic.  Sigma(B, s) = B (1 - s)/(1 - s - B)
    for s + B < 1 (and infinity for s + B > 1; at s + B = 1 the supremum is infinite as well).  In y = 1 - s:
    y -> ((1 - B) y - B)/(y - B)."""
    y = Fraction(1)
    for _ in range(k):
        if y <= B:
            return False
        y = ((1 - B) * y - B) / (y - B)
    return True


def gauss_exact(k: int, digits: int = 9) -> int:
    """The largest integer N with p_k(N/10^digits) < infinity (exact).  tau_k >= N/10^digits by Proposition A."""
    scale = 10**digits
    lo, hi = scale // 4, scale                  # B = 1/4 survives for every k; B = 1 = a does not
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if gauss_survives_exact(Fraction(mid, scale), k):
            lo = mid
        else:
            hi = mid
    return lo


def gauss_closed_form_root(k: int, dps: int = 30):
    """The root of (k - 1) psi(B) + phi_0(B) = pi, psi = arctan(sqrt(4B - 1)/(1 - 2B)),
    phi_0 = arccot((1 - 3B)/((1 - B) sqrt(4B - 1))) (R_REPORT section 10), both angles taken in (0, pi)."""
    old = mp.mp.dps
    mp.mp.dps = dps
    try:
        def ang(num, den):                       # the angle in (0, pi) with tangent num/den, num > 0
            return mp.atan2(num, den)

        def g(B):
            r = mp.sqrt(4 * B - 1)
            return (k - 1) * ang(r, 1 - 2 * B) + ang((1 - B) * r, 1 - 3 * B) - mp.pi

        lo, hi = mp.mpf(1) / 4 + mp.mpf(10) ** (-dps + 3), mp.mpf(1) - mp.mpf(10) ** (-dps + 3)
        # g increases in B; g(1/4+) = -pi < 0
        for _ in range(4 * dps):
            mid = (lo + hi) / 2
            if g(mid) < 0:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    finally:
        mp.mp.dps = old


# ----------------------------------------------------------------------------------------------------------------
# interval arithmetic: a rigorous "p_k(B) < infinity" for products of symmetric binary sites
# ----------------------------------------------------------------------------------------------------------------
def _iv_F_sym(sites, t):
    """An enclosure of F(t) = sum_j lambda_j [Lambda(t u_j) - t Lambda(u_j)] for an interval t."""
    tot = iv.mpf(0)
    for lam, u, p in sites:
        if p != 0.5:
            raise NotImplementedError("interval evaluation is implemented for symmetric sites only")
        lam, u = iv.mpf(str(lam)), iv.mpf(str(u))
        tot += lam * ((iv.log(2) - iv.log(1 + iv.exp(-t * u))) - t * (iv.log(2) - iv.log(1 + iv.exp(-u))))
    return tot


def _iv_a_sym(sites):
    tot = iv.mpf(0)
    for lam, u, p in sites:
        lam, u = iv.mpf(str(lam)), iv.mpf(str(u))
        tot += lam * (iv.log(2) - iv.log(1 + iv.exp(-u)) - u / (1 + iv.exp(u)))
    return tot


def certify_lower(pair, B: str, k: int, dps: int = 40) -> bool:
    """True only if p_k(B) < infinity is PROVED for the decimal string B, for a product of symmetric binary
    sites (fractions and slopes are read as the decimal strings of their double-precision values).

    Monotonicity used: Sigma(B, s) is nondecreasing in s; Sigma(B, s) = t'(1 - s)/(1 - t') with t' the LEAST t
    such that Q(t) >= B/(1 - s), so every t_up with Q(t_up) >= B/(1 - s) (checked in interval arithmetic)
    gives Sigma(B, s) <= t_up (1 - s)/(1 - t_up).  The orbit of upper bounds s_0 = 0 <= s_1^up <= ... must
    satisfy B/(1 - s_j^up) < a (lower end of an enclosure of a) for j = 0..k-1."""
    old_iv, old_mp = iv.dps, mp.mp.dps
    iv.dps = dps
    mp.mp.dps = dps
    try:
        sites = pair.sites
        a_lo = _iv_a_sym(sites).a
        Biv = iv.mpf(B)
        y = iv.mpf(1)                            # enclosure of a LOWER bound of 1 - s (we only use y.a)
        t = mp.mpf(0)
        eps = mp.mpf(10) ** (-(dps - 8))
        Bmp = mp.mpf(B)
        for _ in range(k):
            ylo = iv.mpf(y.a)
            if not (ylo.a > 0):
                return False
            c = Biv / ylo                        # enclosure of an upper bound of B/(1 - s)
            if not (c.b < a_lo):
                return False
            # approximate root in mpmath, then push it to the right until the interval test passes
            cm = mp.mpf(c.b)
            t = _q_inverse_mp(pair, cm, t, eps)
            tup = t + eps
            ok = False
            for _ in range(60):
                tiv = iv.mpf(tup)
                if (_iv_F_sym(sites, tiv) - c * (1 - tiv)).a >= 0 and tup < 1:
                    ok = True
                    break
                tup = tup + (tup - t) * 2
            if not ok:
                return False
            tiv = iv.mpf(tup)
            snew = tiv * ylo / (1 - tiv)         # Sigma(B, s) <= Sigma(B, s_up) <= t_up (1 - s_up)/(1 - t_up)
            y = iv.mpf(1) - iv.mpf(snew.b)       # 1 - (upper bound of the new slope)
            t = mp.mpf(tup)
        return True
    finally:
        iv.dps = old_iv
        mp.mp.dps = old_mp
