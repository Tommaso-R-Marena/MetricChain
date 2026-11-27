"""Referee B, check 1: constants of the cube from the DEFINITIONS of the theory report (not from rlib.py).

Definitions used (docs/THEORY_REPORT.md, section 11.18, lines 4709-4715 and 5250-5251):
    p_u = 1/(1 + e^u),   Lambda_1 = ln(2/(1 + e^{-u})),   KL(x||y) = x ln(x/y) + (1-x) ln((1-x)/(1-y)),
    theta_na(e)   = KL(rho_e || 1/2),  rho_e in [p_u, 1/2] the solution of KL(rho || p_u) = e   (0 for e >= eps*),
    theta_hint(e) = KL((Lambda_1 + e)/u || 1/2),
    a = theta_na(0+) = KL(p_u || 1/2),   h = theta_hint(0) = KL(Lambda_1/u || 1/2).
Everything below is computed with mpmath at 40 digits; derivatives by mpmath.diff (numerical, high order).
Quantities of R_REPORT.md section 1:
    h  : root of theta_na(h) = h                       (compared with KL(Lambda_1/u || 1/2))
    r  = -theta_na'(h),  L = r/(1 + r)
    vartheta = theta_na''(h)/(1 + r)^3                  (compared with theta_hint''(0), with 1/(u^2 rho_h (1 - rho_h)),
               and with -1/J''(L) where J(t) = inf_e [(1 - t) theta_na(e) + t e] is minimised NUMERICALLY)
    c2 = 2 pi^2 h^2 vartheta
"""
import mpmath as mp

mp.mp.dps = 40


def KL(x, y):
    return x * mp.log(x / y) + (1 - x) * mp.log((1 - x) / (1 - y))


def constants(u):
    u = mp.mpf(u)
    pu = 1 / (1 + mp.e ** u)
    Lam1 = mp.log(2 / (1 + mp.e ** (-u)))
    epsstar = mp.log(mp.cosh(u / 2))
    a = KL(pu, mp.mpf(1) / 2)

    def rho_of_e(e):
        # solution in [p_u, 1/2] of KL(rho || p_u) = e
        f = lambda rho: KL(rho, pu) - e
        return mp.findroot(f, (pu + mp.mpf(10) ** (-30), mp.mpf(1) / 2), solver="anderson", tol=mp.mpf(10) ** (-35))

    def theta_na(e):
        if e >= epsstar:
            return mp.mpf(0)
        return KL(rho_of_e(e), mp.mpf(1) / 2)

    def theta_hint(e):
        return KL((Lam1 + e) / u, mp.mpf(1) / 2)

    # h as the fixed point of theta_na, by bisection (theta_na(e) - e is decreasing)
    lo, hi = mp.mpf(10) ** (-12), epsstar
    for _ in range(140):
        mid = (lo + hi) / 2
        if theta_na(mid) - mid > 0:
            lo = mid
        else:
            hi = mid
    h_fix = (lo + hi) / 2
    h_hint = theta_hint(0)
    # derivatives of theta_na at h: implicit differentiation done by hand as a second route:
    #   e = KL(rho||p_u), theta = KL(rho||1/2);  d theta/d e = KL'(rho||1/2)/KL'(rho||p_u)
    rho_h = rho_of_e(h_fix)
    d1half = mp.log(rho_h / (1 - rho_h))                      # d/drho KL(rho||1/2)
    d1pu = mp.log(rho_h / (1 - rho_h)) - mp.log(pu / (1 - pu))  # d/drho KL(rho||p_u) = logit(rho) + u
    th1 = d1half / d1pu
    d2 = 1 / (rho_h * (1 - rho_h))                            # second derivative of both KLs in rho
    # d^2 theta/de^2 = (d/drho (d1half/d1pu)) / d1pu
    th2 = ((d2 * d1pu - d1half * d2) / d1pu ** 2) / d1pu
    th1_num = mp.diff(theta_na, h_fix, 1, h=mp.mpf(10) ** (-8))
    th2_num = mp.diff(theta_na, h_fix, 2, h=mp.mpf(10) ** (-6))
    r = -th1
    L = r / (1 + r)
    vartheta = th2 / (1 + r) ** 3
    vartheta_hint = mp.diff(theta_hint, 0, 2)
    vartheta_closed = 1 / (u ** 2 * (Lam1 / u) * (1 - Lam1 / u))
    L_hint = -mp.diff(theta_hint, 0, 1)

    # J by direct numerical minimisation over e of (1 - t) theta_na(e) + t e   (golden section; convex in e)
    def J(t):
        g = lambda e: (1 - t) * theta_na(e) + t * e
        lo, hi = mp.mpf(10) ** (-10), epsstar * 2
        gr = (mp.sqrt(5) - 1) / 2
        x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        f1, f2 = g(x1), g(x2)
        for _ in range(110):
            if f1 <= f2:
                hi, x2, f2 = x2, x1, f1
                x1 = hi - gr * (hi - lo)
                f1 = g(x1)
            else:
                lo, x1, f1 = x1, x2, f2
                x2 = lo + gr * (hi - lo)
                f2 = g(x2)
        return min(f1, f2)

    def Jclosed(t):          # the report's formula  J(t) = Lambda(t u) - t Lambda(u)
        return mp.log(2 / (1 + mp.e ** (-t * u))) - t * Lam1

    dJ = max(abs(J(t) - Jclosed(t)) for t in [mp.mpf("0.1"), mp.mpf("0.3"), L, mp.mpf("0.7"), mp.mpf("0.9")])
    d = mp.mpf(10) ** (-5)
    J2_num = (J(L + d) - 2 * J(L) + J(L - d)) / d ** 2
    J2_closed = mp.diff(Jclosed, L, 2)
    c2 = 2 * mp.pi ** 2 * h_fix ** 2 * vartheta
    print("u = %s" % mp.nstr(u, 3))
    print("  p_u = %s   Lambda_1 = %s   eps* = %s" % (mp.nstr(pu, 12), mp.nstr(Lam1, 12), mp.nstr(epsstar, 12)))
    print("  a  = KL(p_u||1/2)                 = %s" % mp.nstr(a, 12))
    print("  h  (root of theta_na(h) = h)      = %s" % mp.nstr(h_fix, 12))
    print("  h  (KL(Lambda_1/u||1/2))          = %s    difference %s" % (mp.nstr(h_hint, 12), mp.nstr(h_fix - h_hint, 3)))
    print("  rho_h = %s  vs  Lambda_1/u = %s" % (mp.nstr(rho_h, 12), mp.nstr(Lam1 / u, 12)))
    print("  theta_na'(h) = %s (implicit)  %s (numerical)" % (mp.nstr(th1, 12), mp.nstr(th1_num, 12)))
    print("  theta_na''(h) = %s (implicit)  %s (numerical)" % (mp.nstr(th2, 12), mp.nstr(th2_num, 12)))
    print("  L = r/(1+r)                       = %s    (-theta_hint'(0) = %s)" % (mp.nstr(L, 12), mp.nstr(L_hint, 12)))
    print("  vartheta = theta_na''(h)/(1+r)^3  = %s" % mp.nstr(vartheta, 12))
    print("  theta_hint''(0) (numerical)       = %s" % mp.nstr(vartheta_hint, 12))
    print("  1/(u^2 rho_h (1 - rho_h))         = %s" % mp.nstr(vartheta_closed, 12))
    print("  -1/J''(L), J minimised numerically= %s   (closed form of J: %s)" % (mp.nstr(-1 / J2_num, 9), mp.nstr(-1 / J2_closed, 12)))
    print("  max |J_numerical - (Lambda(tu) - t Lambda(u))| at 5 points = %s" % mp.nstr(dJ, 3))
    print("  L < 1 - h/a ?   L = %s,  1 - h/a = %s" % (mp.nstr(L, 8), mp.nstr(1 - h_fix / a, 8)))
    print("  2 pi^2 h^2 vartheta               = %s   = %s * a" % (mp.nstr(c2, 12), mp.nstr(c2 / a, 8)))
    print("  c_* = pi h sqrt(2 vartheta)       = %s" % mp.nstr(mp.pi * h_fix * mp.sqrt(2 * vartheta), 12))
    return dict(a=a, h=h_fix, L=L, vartheta=vartheta, c2=c2)


if __name__ == "__main__":
    for u in [1, 2]:
        constants(u)
    print("report (section 0/1), u = 1:  h = 0.02913914  L = 0.490034  vartheta = 4.244977  a = 0.11094407  2pi^2h^2vartheta = 0.0711473 = 0.64129 a")
    # Gaussian pair, by hand: theta = (1 - sqrt x)^2, h = 1/4, theta'(h) = -(1 - sqrt h)/sqrt h = -1, theta''(h) = 1/(2 h^{3/2}) = 4
    h = mp.mpf(1) / 4
    r = (1 - mp.sqrt(h)) / mp.sqrt(h)
    th2 = 1 / (2 * h ** mp.mpf("1.5"))
    print("Gaussian pair: r = %s, theta''(h) = %s, vartheta = %s, 2 pi^2 h^2 vartheta = %s  (pi^2/16 = %s)"
          % (mp.nstr(r, 6), mp.nstr(th2, 6), mp.nstr(th2 / (1 + r) ** 3, 6), mp.nstr(2 * mp.pi ** 2 * h ** 2 * th2 / (1 + r) ** 3, 12), mp.nstr(mp.pi ** 2 / 16, 12)))
