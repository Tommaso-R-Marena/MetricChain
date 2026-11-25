"""r10_lyap.py: moment Lyapunov exponents of products of random 2x2 positive matrices, own code.

Xi_{kappa,eta}(b) = sum_tau exp( kappa sum_i b_i tau_i tau_{i+1} + eta sum_i tau_i ),  b_i = +-1 i.i.d.,
P(b=-1) = q.   L_q(kappa, eta; r) = lim (1/n) ln E[ Xi^r ].

Two numerically independent methods:
 A. exact enumeration over all 2^(n-1) bond patterns (vectorised doubling), increments
    ln E[Xi_n^r] - ln E[Xi_{n-1}^r]  (converge geometrically);
 B. transfer operator on the projective coordinate z = ln(y(+)/y(-)),
       (T f)(z) = sum_b P(b) g_b(z)^r f(2 eta + phi_b(z)),
    discretised by Chebyshev interpolation on the invariant interval; L = ln(spectral radius).
"""
import numpy as np


# ---------------------------------------------------------------- method A: exact enumeration
def exact_log_moments(kappa, eta, q, r, nmax):
    """Returns list a[n] = ln E[Xi_n^r] for n = 1..nmax (a[0] = nan)."""
    yp = np.array([np.exp(eta)])     # y(+) for every bond pattern so far
    ym = np.array([np.exp(-eta)])
    lw = np.array([0.0])             # log-probability of the pattern
    logscale = 0.0                   # true y = exp(logscale) * (yp, ym)
    out = [np.nan, r * np.log(yp[0] + ym[0])]
    ek, emk = np.exp(kappa), np.exp(-kappa)
    ee, eme = np.exp(eta), np.exp(-eta)
    for n in range(2, nmax + 1):
        parts = []
        if q < 1:    # bond b = +1
            parts.append((ee * (yp * ek + ym * emk), eme * (yp * emk + ym * ek), lw + np.log1p(-q)))
        if q > 0:    # bond b = -1
            parts.append((ee * (yp * emk + ym * ek), eme * (yp * ek + ym * emk), lw + np.log(q)))
        yp = np.concatenate([a for a, _, _ in parts])
        ym = np.concatenate([b for _, b, _ in parts])
        lw = np.concatenate([c for _, _, c in parts])
        s = yp + ym
        la = lw + r * np.log(s)
        mx = la.max()
        out.append(mx + np.log(np.exp(la - mx).sum()) + r * logscale)
        c = s.max()
        yp = yp / c; ym = ym / c
        logscale += np.log(c)
    return out


def lyap_exact(kappa, eta, q, r, nmax=20):
    a = exact_log_moments(kappa, eta, q, r, nmax)
    inc = [a[n] - a[n - 1] for n in range(2, nmax + 1)]
    # Aitken extrapolation of the last three increments
    x0, x1, x2 = inc[-3], inc[-2], inc[-1]
    den = (x2 - x1) - (x1 - x0)
    ait = x2 - (x2 - x1) ** 2 / den if abs(den) > 1e-300 else x2
    return inc[-1], ait, inc


# ---------------------------------------------------------------- method B: transfer operator
def cheb_nodes(N, lo, hi):
    k = np.arange(N)
    x = np.cos(np.pi * (2 * k + 1) / (2 * N))          # Chebyshev points of the first kind
    return 0.5 * (lo + hi) + 0.5 * (hi - lo) * x, x


def cheb_interp_matrix(xn, xe):
    """Barycentric interpolation matrix from values at first-kind nodes xn (in [-1,1]) to
    points xe (in [-1,1])."""
    N = len(xn)
    k = np.arange(N)
    w = (-1.0) ** k * np.sin(np.pi * (2 * k + 1) / (2 * N))
    d = xe[:, None] - xn[None, :]
    exact = np.abs(d) < 1e-14
    d[exact] = 1.0
    c = w[None, :] / d
    M = c / c.sum(axis=1, keepdims=True)
    rows = exact.any(axis=1)
    M[rows] = exact[rows].astype(float)
    return M


def lyap_operator(kappa, eta, q, r, N=48):
    """ln(spectral radius) of the transfer operator, Chebyshev collocation with N nodes."""
    if abs(kappa) < 1e-14:
        return r * np.log(2 * np.cosh(eta))
    lo, hi = 2 * eta - 2 * abs(kappa), 2 * eta + 2 * abs(kappa)
    z, xn = cheb_nodes(N, lo, hi)
    A = np.zeros((N, N))
    # common scale for the growth factors (avoids overflow of g^r for large r)
    lg_ref = np.log(np.exp(-eta) * (np.exp(hi + abs(kappa)) + np.exp(abs(kappa))))
    for b, pb in ((+1, 1 - q), (-1, q)):
        if pb == 0:
            continue
        kb = kappa * b
        # y'(+) = e^eta (y+ e^kb + y- e^-kb),  y'(-) = e^-eta (y+ e^-kb + y- e^kb),  y = m (e^z, 1)
        num = np.exp(z + kb) + np.exp(-kb)
        den = np.exp(z - kb) + np.exp(kb)
        z2 = 2 * eta + np.log(num / den)
        lg = -eta + np.log(den) - lg_ref
        xe = (2 * z2 - (lo + hi)) / (hi - lo)
        xe = np.clip(xe, -1.0, 1.0)
        A += pb * np.exp(r * lg)[:, None] * cheb_interp_matrix(xn, xe)
    ev = np.linalg.eigvals(A)
    return float(np.log(np.max(ev.real)) + r * lg_ref)


def G_inf(t, c, p, u, N=48):
    """Proposition H (Y_REPORT 5.3), per site, n -> infinity:
       G_inf(t;c) = L_{p_c}(K',h;t) - t L_p(c, t h; 1/t) - t ln(2 cosh K') + ln(2 cosh c)."""
    h = u / 2
    Kp = 0.5 * np.log((1 - p) / p)
    pc = 1.0 / (1.0 + np.exp(2 * c))
    return (lyap_operator(Kp, h, pc, t, N) - t * lyap_operator(c, t * h, p, 1.0 / t, N)
            - t * np.log(2 * np.cosh(Kp)) + np.log(2 * np.cosh(c)))


def G_finite(t, c, p, u, n):
    """Proposition H for finite n (exact enumeration of both moments)."""
    h = u / 2
    Kp = 0.5 * np.log((1 - p) / p)
    pc = 1.0 / (1.0 + np.exp(2 * c))
    a1 = exact_log_moments(Kp, h, pc, t, n)[n]
    a2 = exact_log_moments(c, t * h, p, 1.0 / t, n)[n]
    lnZ0K = np.log(2) + (n - 1) * np.log(2 * np.cosh(Kp))
    lnZ0c = np.log(2) + (n - 1) * np.log(2 * np.cosh(c))
    return a1 - t * a2 - t * lnZ0K + lnZ0c
