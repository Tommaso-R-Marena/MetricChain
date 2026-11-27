#!/usr/bin/env python3
"""R8 / script 11 -- exact finite-n validation of the exponential-scale machinery of script 05
on NON-flat visible landscapes (a soft basin / a global tilt), with an explicit pair.

Visible:  g(x) = -v (r_c - |x|)_+           (slope v <= u about a0 = 0^n; r_c = n: a global tilt)
Twin:     T(x) = L + u (d(x,a') - r_T)_+ ,  |a'| = P,   g' = min(g, T)
Exact sums over (i,j): x differs from a' in i of the P ones of a' and j of its n-P zeros
(C(P,i) C(n-P,j) points, d(x,a') = i+j, |x| = P-i+j).  The level L is the root of the excess
identity (U' = U exactly); r_T is the smallest plateau radius whose gap exceeds eps.
Hit probability of the family {a' : |a'| = P} at a query of weight w:
     p(w) = sum_{(i,j) in D, P-i+j = w} C(w,j) C(n-w,i) / C(n,P),     exponent = -ln max_w p(w) / n,
compared with (i) the rate computed by r8_05_conjecture.theta_radial for the same parameters and
(ii) the exact plateau twin on the flat background with the cone basin (same n, u, eps).

Run: python3 r8_11_tilt_exact.py      (about 1 minute)
"""
import math, io, contextlib
import numpy as np
from scipy.special import logsumexp, gammaln
from r8_lib import *
import r8_02_twin as TW
import r8_05_conjecture as C5


def lnbin(n, k):
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def study(n, u, v, rc, P, eps1):
    d = np.arange(n + 1)
    gvis = -v * np.maximum(rc - d, 0.0)
    lnZ, U, S = radial_stats(n, gvis)
    i = np.arange(P + 1)[:, None]; j = np.arange(n - P + 1)[None, :]
    lc = lnC(P)[:, None] + lnC(n - P)[None, :]
    dp = (i + j).astype(float); wt = (P - i + j)
    g = gvis[wt]
    eps = eps1 * n
    def twin(rT):
        def F(L):
            T = L + u * np.maximum(dp - rT, 0.0)
            m = T < g
            if not m.any(): return None
            lE = float(logsumexp(lc[m] - T[m] + np.log1p(-np.exp(T[m] - g[m]))))
            Fv = float(np.sum(np.exp(lc[m] - T[m] - lE) * (T[m] - U) - np.exp(lc[m] - g[m] - lE) * (g[m] - U)))
            return Fv, lE, m
        lo, hi = U - u * n, U + 1.0          # F(hi) > 0 (level above U - 1 ... shallow end), F(lo) < 0
        flo, fhi = F(lo), F(hi)
        if flo is None or fhi is None or not (flo[0] < 0 < fhi[0]): return None
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            fm = F(mid)
            if fm is None or fm[0] > 0: hi = mid
            else: lo = mid
        L = 0.5 * (lo + hi)
        Fv, lE, m = F(L)
        return L, float(np.logaddexp(0.0, lE - lnZ)), m
    res = None
    for rT in range(int(sig(v) * n), n // 2 + 1):
        t = twin(rT)
        if t is not None and t[1] > eps:
            res = (rT, t)
            break
    if res is None:
        print(f"  n={n} u={u} v={v} rc={rc} P={P} eps1={eps1}: no twin with a plateau radius below n/2"); return
    rT, (L, gap, m) = res
    # hit probability
    lnp = np.full(n + 1, -np.inf)
    ii, jj = np.nonzero(m)
    w = P - ii + jj
    terms = lnbin(w, jj) + lnbin(n - w, ii) - lnbin(n, P)
    for k in range(len(w)):
        lnp[w[k]] = np.logaddexp(lnp[w[k]], terms[k])
    wbest = int(np.argmax(lnp))
    expo = -float(lnp[wbest]) / n
    # the rate machinery for the same parameters
    G = lambda om: -v * np.maximum(rc / n - om, 0.0)
    th, ok = C5.theta_radial(u, G, L / n, rT / n, P / n, ngrid=400, zoom=2)
    # the plateau twin on the flat background, same n, u, eps
    with contextlib.redirect_stdout(io.StringIO()):
        r = TW.find_case(n, u, rho0(u) + 0.01, eps1, 0.5)
    lbt = ln_ball_table(n)
    ex_pl = (n * LN2 - float(lbt[r["r2"] - 1])) / n
    print(f"  n={n} u={u} v={v} rc={rc} P={P} eps1={eps1:.4f}: visible S/n={S/n:.4f} U={U:.2f}; twin: plateau radius {rT}, level L={L:.3f} (U'=U exactly), "
          f"gap={gap:.2f} > {eps:.2f}")
    print(f"       exact hit probability: exponent {expo:.5f} (worst query weight {wbest});  rate machinery: {th:.5f};  "
          f"plateau twin on the flat background (rho1 = rho0+0.01): {ex_pl:.5f} (asymptotic theta_pl {theta_pl(u,eps1):.5f})")


if __name__ == "__main__":
    print("== exact pairs on non-flat visible landscapes ==")
    # soft basin with the twin far away on the flat part; soft basin with the twin on the rim; a global tilt
    u = 2.0
    for (n, v, rcf, Pf, e1f) in ((600, 1.4, None, 0.5, 0.15), (600, 1.4, None, 0.40, 0.15), (600, 1.0, None, 0.45, 0.10),
                                 (600, 1.2, 1.0, 0.45, 0.10), (600, 0.8, 1.0, 0.40, 0.05)):
        s_v = sig(v)
        rc = n if rcf == 1.0 else int((s_v + (LN2 - hb(s_v)) / v + 0.02) * n)
        study(n, u, v, rc, int(Pf * n), e1f * a_of(u))
