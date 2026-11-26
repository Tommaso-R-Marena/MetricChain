"""(library part of a1_propU.py: sigma_vec, make_W, U_and_Llow, F_inf)
Referee A, test 1: Proposition U by brute force on the operator R itself.

For a pair theta, a convex nondecreasing piecewise-linear W : [0, b] -> [0, 1] (given by its kinks, so that
T := M_{W,b} is EXACTLY the upper envelope of finitely many lines) and g > 0 compare

  R_bf  : brute force on R[T](g): min over a (phi, beta)-grid (+ local refinement) of the sup over a gamma-grid
          (no shortcut for the sup over gamma) -- an UPPER estimate of R[T](g) up to the gamma-discretisation;
  F_inf : inf_{e > g} (1 - g/e) S(g theta(e)/(e - g)),  S(X) = max_B [B + (1 - W(B)) X]   (Lemma M: R <= F_inf);
  U     : sup_B (B - Sigma(B, W(B)) g)   (the bound of Proposition U),  Sigma by direct maximisation over e;
  Llow  : sup_B (B - max(W(B), Sigma(B, W(B))) g)   (Lemma L: R[T] >= Llow, since every line of W is a minorant of T).

Proposition U says R <= U; its proof says F_inf <= U (minimax).  Reported: max of (F_inf - U)/a, (R_bf - U)/a,
min of (R_bf - Llow)/a, and where the sup over gamma was attained.
Usage: python3 a1_propU.py [seed] [ntrial]
"""
import math, sys, time
import numpy as np
from ralib import Gauss, Cube, Expo, Power, Recip, PwLin, Envelope, R_bruteforce

rng = np.random.default_rng(1)
GR = (math.sqrt(5) - 1) / 2


def sigma_vec(theta, B, s):
    """vectorised Sigma(B_i, s_i): grid over e, then golden section (the ratio is quasi-concave in e)."""
    B = np.asarray(B, dtype=float); s = np.asarray(s, dtype=float)
    out = np.empty(len(B))
    if theta.vertices is not None:
        for i in range(len(B)):
            out[i] = theta.sigma(B[i], s[i])
        return out
    e = theta.egrid(); th = theta(e)
    y = 1.0 - s
    for c0 in range(0, len(B), 400):
        sl = slice(c0, c0 + 400)
        r = (B[sl, None] - y[sl, None] * th[None, :]) / e[None, :]
        i = np.argmax(r, axis=1)
        best = r[np.arange(r.shape[0]), i]
        lo = e[np.maximum(i - 1, 0)]; hi = e[np.minimum(i + 1, len(e) - 1)]
        Bc, yc = B[sl], y[sl]
        fun = lambda x: (Bc - yc * theta(x)) / x
        x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
        f1, f2 = fun(x1), fun(x2)
        for _ in range(60):
            m = f1 >= f2
            hi = np.where(m, x2, hi); lo = np.where(m, lo, x1)
            nx1 = hi - GR * (hi - lo); nx2 = lo + GR * (hi - lo)
            x1, x2 = nx1, nx2
            f1, f2 = fun(x1), fun(x2)
        best = np.maximum(best, np.maximum(f1, f2))
        out[sl] = np.maximum(best, 0.0)
    out[B > y * theta.a * (1 + 1e-15)] = np.inf
    out[B == 0] = 0.0
    return out


def make_W(b, kind=None):
    """kinks (B_k, W_k) of a convex nondecreasing piecewise-linear W on [0, b] with values in [0, 1]."""
    kind = kind or rng.choice(["rand", "rand", "rand", "flat0", "zero", "const", "linear", "touch1", "one", "w0pos"])
    if kind == "zero":
        return np.array([0.0, b]), np.array([0.0, 0.0]), kind
    if kind == "one":
        return np.array([0.0, b]), np.array([1.0, 1.0]), kind
    if kind == "const":
        c = rng.uniform(0.05, 0.95)
        return np.array([0.0, b]), np.array([c, c]), kind
    if kind == "linear":
        c = rng.uniform(0.1, 1.0)
        return np.array([0.0, b]), np.array([0.0, c]), kind
    nk = rng.integers(1, 5)
    xs = np.sort(rng.uniform(0, b, nk))
    xs = np.concatenate([[0.0], xs, [b]])
    slopes = np.sort(rng.exponential(1.0, nk + 1))
    if kind in ("flat0", "touch1"):
        slopes[0] = 0.0
    w0 = rng.uniform(0.0, 0.4) if kind == "w0pos" else 0.0
    W = w0 + np.concatenate([[0.0], np.cumsum(slopes * np.diff(xs))])
    top = 1.0 if kind == "touch1" else rng.uniform(0.3, 1.0)
    if W[-1] > w0:
        W = w0 + (W - w0) * (top - w0) / (W[-1] - w0) if top > w0 else np.full_like(W, w0)
    return xs, W, kind


def U_and_Llow(theta, xs, W, g, nB=1500):
    Bg = np.unique(np.concatenate([np.linspace(0, xs[-1], nB), xs]))
    Wg = np.interp(Bg, xs, W)
    sig = sigma_vec(theta, Bg, Wg)
    fin = np.isfinite(sig)
    valsU = np.where(fin, Bg - np.where(fin, sig, 0) * g, -np.inf)
    valsL = np.where(fin, Bg - np.maximum(Wg, np.where(fin, sig, 0)) * g, -np.inf)
    iU = int(np.argmax(valsU))
    # refine U around iU (the function B -> B - Sigma(B, W(B)) g is concave): golden section between neighbours
    lo, hi = Bg[max(iU - 1, 0)], Bg[min(iU + 1, len(Bg) - 1)]
    def fU(B):
        s_ = float(np.interp(B, xs, W))
        v = theta.sigma(B, s_) if theta.vertices is not None else float(sigma_vec(theta, np.array([B]), np.array([s_]))[0])
        return B - v * g if math.isfinite(v) else -math.inf
    x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
    f1, f2 = fU(x1), fU(x2)
    for _ in range(45):
        if f1 >= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo); f1 = fU(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo); f2 = fU(x2)
    U = max(float(valsU[iU]), f1, f2)
    return U, float(valsL.max()), float(Bg[iU]), float(sig[iU]), float(Wg[iU])


def F_inf(theta, xs, W, g):
    """inf_{e>g} (1 - g/e) S(g theta(e)/(e-g)); S exact (max over the kinks).  With e = g (1 + t), t = exp(z):
    (1 - g/e) S(theta(e)/t) = max_k [ B_k t/(1+t) + (1 - W_k) theta(e)/(1+t) ]   (no cancellation as t -> 0).
    Grid in z, then golden section (F is quasi-convex in e as a maximum of quasi-convex functions)."""
    def F(z):
        z = np.atleast_1d(np.asarray(z, dtype=float))
        t = np.exp(z)
        e = g * (1 + t)
        th = theta(e)
        return np.max(xs[None, :] * (t / (1 + t))[:, None] + (1 - W[None, :]) * (th / (1 + t))[:, None], axis=1)
    z = np.linspace(-36, 18, 10801)
    v = F(z)
    i = int(np.argmin(v))
    best = float(v[i])
    lo, hi = z[max(i - 1, 0)], z[min(i + 1, len(z) - 1)]
    fz = lambda zz: float(F(zz)[0])
    x1, x2 = hi - GR * (hi - lo), lo + GR * (hi - lo)
    f1, f2 = fz(x1), fz(x2)
    for _ in range(70):
        if f1 <= f2:
            hi, x2, f2 = x2, x1, f1
            x1 = hi - GR * (hi - lo); f1 = fz(x1)
        else:
            lo, x1, f1 = x1, x2, f2
            x2 = lo + GR * (hi - lo); f2 = fz(x2)
    return min(best, f1, f2), float(g * (1 + math.exp(z[i])))


