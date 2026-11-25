#!/usr/bin/env python3
"""R8 / script 05 -- attempts to refute Conjecture A16.4 at the exponential scale.  Own code.

The conjecture:  theta_U(eps1) = ln2 - h(min(1/2, rho0 - sigma_u + sigma2(eps1))) =: theta_pl(eps1).
The plateau twin on a flat background proves ">=".  A refutation needs a visible instance g and a
family of twins (same mean energy, ln Z larger by eps1 n, equal to g outside D_j) whose hit
probability  max_x P_j(x in D_j)  is  e^{-n theta}  with  theta > theta_pl(eps1).

Everything here is at the exponential scale (rates per site; Laplace principle), i.e. evidence of
the kind the addendum itself uses for its 'terrace' family; candidates that beat theta_pl would
have to be confirmed by exact sums (none did).

Radial machinery (families F1, F5).  The visible landscape near the twin is radial about a point
a0:  g(x) = n G(d(x,a0)/n).  The twin is a plateau of level L and radius x_T n with walls of slope
u, centred at a' with d(a0,a') = pi n:   T = L + u (d(x,a')/n - x_T)_+ ,  g' = min(g, T).
A point x that differs from a' in alpha n of the pi n coordinates where a0 and a' differ and in
beta n of the others has d(x,a') = alpha+beta, d(x,a0) = pi-alpha+beta.  Placing a' uniformly on
the sphere of radius pi n about a0 (the orbit under the symmetries of g), a query at x lies in the
difference set D = {T < g} with probability exp(-n Phi(alpha,beta)),
   Phi = h(pi-alpha+beta) - pi h(alpha/pi) - (1-pi) h(beta/(1-pi)),
so the exponent of the family is   theta = min over D of Phi.
Twin: level L = U_vis (mean energy), entropy h(x_T) = s_vis + eps1 (identity ln Z = S - U).

 F1  visible = soft basin  G = -v (rho_c - delta)_+  of slope v <= u (v = u: the cone basin of the
     addendum; rho_c = 1: a global tilt), dominant; the twin anywhere (on the flat part, on the
     rim, on the slope).
 F5  visible = a remote dominant cone basin (sets U, S) + a sub-dominant terrace of depth u b n and
     radius rho_t n around a0; twin inside or across the terrace.
 F2  product landscape: flat block (phi n sites) x cone block; twin = ball in the flat block times
     a flooded cone.
 F3  K = e^{gamma n} visible basins; one twin on the flat background.
 F4  'egg carton'  g = u dist(x, C), C a code of rate gamma; twin = one flooded cell.
 G   the small-slope (Gaussian) limit: closed forms for F1 (tilt), F4 and the plateau twin, and the
     'column bound' of the report (any visible landscape, twin in a fresh random direction).

Run:  python3 r8_05_conjecture.py [quick]        (full: about 6 minutes)
"""
import math, sys, time
import numpy as np
from r8_lib import *


def hv(p):
    p = np.clip(p, 1e-300, 1 - 1e-16)
    return -p * np.log(p) - (1 - p) * np.log1p(-p)


def theta_radial(u, Gfun, L, xT, pi, ngrid=360, zoom=2):
    """exponent of the family: min over D = {T < G} of Phi.  Returns (theta, valid).
    valid: the typical point of the plateau's sphere, (alpha,beta) = (pi xT, (1-pi) xT), lies in D.
    Then the twin's mass has rate h(xT) - L exactly (on the wall the rate h(r) - L - u (r - xT)
    decreases because xT > sigma_u; inside the plateau the entropy is smaller), and its mean
    energy is L at this scale -- so no grid is involved in the two matching conditions."""
    om_typ = pi + xT * (1 - 2 * pi)
    valid = bool(Gfun(np.array([om_typ]))[0] > L + 1e-12)
    alo, ahi, blo, bhi = 1e-9, 1 - 1e-9, 1e-9, 1 - 1e-9
    theta = None
    for z in range(zoom + 1):
        a = np.linspace(alo, ahi, ngrid)[:, None]
        b = np.linspace(blo, bhi, ngrid)[None, :]
        al = pi * a; be = (1 - pi) * b
        om = pi - al + be
        T = L + u * np.maximum(al + be - xT, 0.0)
        Dm = T < Gfun(om) - 1e-12
        if not Dm.any():
            return None, False
        Phi = hv(om) - pi * hv(a) - (1 - pi) * hv(b)
        Phi_D = np.where(Dm, Phi, np.inf)
        k = np.unravel_index(np.argmin(Phi_D), Phi_D.shape)
        theta = float(Phi_D[k])
        da = (ahi - alo) / ngrid * 3; db = (bhi - blo) / ngrid * 3
        a0 = float(a[k[0], 0]); b0 = float(b[0, k[1]])
        alo, ahi = max(1e-9, a0 - da), min(1 - 1e-9, a0 + da)
        blo, bhi = max(1e-9, b0 - db), min(1 - 1e-9, b0 + db)
    return max(theta, 0.0), valid


# ------------------------------------------------------------------ F1
def family_F1(u, eps1, quick):
    s_u = sig(u)
    best = (-1.0, None)
    ref = theta_pl(u, eps1)
    vs = [u * f for f in ((0.3, 0.5, 0.7, 0.85, 1.0) if quick else (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0))]
    for v in vs:
        s_v = sig(v)
        if hb(s_v) + eps1 >= LN2:
            continue                      # no room for a twin above this visible state
        xT = hinv(hb(s_v) + eps1)
        # cap radius: from threshold dominance over the flat part upwards (rho_c <= 1/2), and beyond
        rc_thr = s_v + (LN2 - hb(s_v)) / v           # h(s_v) + v (rc - s_v) = ln 2
        rcs = [rc_thr + d for d in ((0.0005, 0.02, 0.06) if quick else (0.0005, 0.01, 0.03, 0.06, 0.1, 0.15))]
        rcs += [0.5, 0.6, 0.8, 1.0]
        for rc in rcs:
            if rc <= s_v or rc > 1.0:
                continue
            zb = hb(s_v) + v * (rc - s_v)
            zflat = LN2 if rc <= 0.5 else hb(rc)
            if zb < zflat:
                continue
            L = -v * (rc - s_v)
            G = lambda om, v=v, rc=rc: -v * np.maximum(rc - om, 0.0)
            pis = np.linspace(max(0.02, s_v - 0.05), 0.5, 9 if quick else 17)
            for pi in pis:
                th, ok = theta_radial(u, G, L, xT, float(pi), ngrid=160 if quick else 240, zoom=2)
                if th is None or not ok:
                    continue
                if th > best[0]:
                    best = (th, dict(v=v, rc=rc, pi=float(pi), xT=xT, L=L, zb=zb))
    return best, ref


# ------------------------------------------------------------------ F5
def family_F5(u, eps1, quick):
    s_u = sig(u)
    ref = theta_pl(u, eps1)
    best = (-1.0, None)
    xT = sigma2(u, eps1)
    for eA in [a_of(u) / u + d for d in ((0.0, 0.02) if quick else (0.0, 0.01, 0.03, 0.06))]:
        z = hb(s_u) + u * eA
        L = -u * eA
        for rt in ((0.3, 0.4, 0.45, 0.5) if quick else (0.25, 0.3, 0.35, 0.4, 0.44, 0.47, 0.5)):
            bmax = (z - hb(rt)) / u                       # sub-dominance of the terrace
            if bmax <= 0:
                continue
            for bf in ((0.0, 0.5, 1.0) if quick else (0.0, 0.25, 0.5, 0.75, 0.9, 1.0)):
                b = min(bf * bmax, eA)
                # terrace: plateau of depth u b, top radius rt, wall of slope u outside
                G = lambda om, b=b, rt=rt: -u * np.minimum(b, np.maximum(rt + b - om, 0.0))
                for pi in np.linspace(0.0 + 0.01, 0.5, 8 if quick else 14):
                    th, ok = theta_radial(u, G, L, xT, float(pi), ngrid=160 if quick else 240, zoom=2)
                    if th is None or not ok:
                        continue
                    if th > best[0]:
                        best = (th, dict(eA=eA, rt=rt, b=b, pi=float(pi), xT=xT))
    return best, ref


# ------------------------------------------------------------------ F2, F3, F4 (closed rate formulas)
def family_F2(u, eps1):
    s_u = sig(u); hs = hb(s_u)
    best = (0.0, None)
    for phi in np.linspace(0.02, 0.98, 97):
        lam = (1 - phi) / phi
        for tau in np.linspace(s_u + 1e-4, 0.5, 200):
            hx = LN2 + lam * (hs - hb(tau)) + eps1 / phi
            if hx > LN2 or hx <= 0:
                continue
            rx = hinv(hx)
            rad = rx + lam * (tau - s_u)
            if rad >= 0.5:
                continue
            th = phi * (LN2 - hb(rad))
            if th > best[0]:
                best = (th, dict(phi=float(phi), tau=float(tau), rho_x=rx))
    return best


def family_F3(u, eps1):
    s_u = sig(u); a = a_of(u)
    out = []
    for gam in np.linspace(0.0, max(0.0, a - eps1) * 0.999, 60):
        R = hinv(hb(s_u) + gam + eps1) + (a - gam) / u
        out.append((float(gam), LN2 - hb(R) if R < 0.5 else 0.0))
    return out


def family_F4(u, eps1):
    s_u = sig(u); a = a_of(u)
    best = (0.0, None)
    for gam in np.linspace(1e-4, max(1e-4, a - eps1) * 0.999, 400):
        rcov = hinv(LN2 - gam)
        rP = hinv(gam + hb(s_u) + eps1)
        R = rcov + rP - s_u
        th = min(gam, LN2 - hb(R)) if R < 0.5 else 0.0
        if th > best[0]:
            best = (th, dict(gamma=float(gam), rho_cov=rcov, rho_P=rP))
    return best


# ------------------------------------------------------------------ Gaussian limit
def gaussian_limit():
    print("== G: small-slope limit (rates in units of n u^2/4; e = eps1/a(u), e' = e/2) ==")
    print("    e      plateau twin     hinted, no datum    tilt (best v)    egg carton (best gamma)   column bound")
    for e in (0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7):
        ep = e / 2
        pl = max(math.sqrt(1 - e) - 0.5, 0.0) ** 2 / 2
        hint = (0.5 - ep) ** 2 / 2
        # tilt: Theta = (sqrt(v^2 - 2e') - v^2)^2 / (2 (1 - v^2)),  needs v^2 - 2e' > v^4
        bt = 0.0
        for v in np.linspace(0.01, 0.999, 2000):
            if v * v - 2 * ep > v ** 4:
                bt = max(bt, (math.sqrt(v * v - 2 * ep) - v * v) ** 2 / (2 * (1 - v * v)))
        # egg carton: (u^2/8)(sqrt(g)+sqrt(1-e-g)-1)^2  = in the present units  (..)^2/2
        bc = 0.0
        for g in np.linspace(0, 1 - e, 2000):
            val = math.sqrt(g) + math.sqrt(max(1 - e - g, 0)) - 1
            if val > 0:
                bc = max(bc, min(val * val / 2, g / 2))
        # column bound: b <= max_{q1 <= sqrt(1-2e')} (q1 - q1^2/2) - e'  ->  Theta <= b^2/2
        q1 = min(1.0, math.sqrt(max(1 - 2 * ep, 0)))
        b = q1 - q1 * q1 / 2 - ep
        col = max(b, 0) ** 2 / 2
        print(f"   {e:4.2f}     {pl:.5f}          {hint:.5f}            {bt:.5f}           {bc:.5f}                 {col:.5f}")
    print("   (the column bound equals the plateau value: with a visible landscape of ANY form and twins hidden in a")
    print("    fresh random direction, nothing beats the plateau twin in this limit -- see the report, section 5)")


if __name__ == "__main__":
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    t0 = time.time()
    gaussian_limit()
    # sanity: the machinery reproduces the plateau twin on the flat background
    print("== sanity: F1 with v = u, cap at threshold, twin far away reproduces theta_pl ==")
    for u, f in ((1.0, 0.3), (2.0, 0.5), (4.0, 0.25)):
        e1 = f * a_of(u)
        rc = rho0(u) + 0.0005
        G = lambda om, u=u, rc=rc: -u * np.maximum(rc - om, 0.0)
        th, ok = theta_radial(u, G, -u * (rc - sig(u)), sigma2(u, e1), 0.5, ngrid=400, zoom=2)
        print(f"   u={u} eps1={e1:.4f}: grid {th:.5f}   formula theta_pl(rho1=rc) {theta_pl(u, e1, rc):.5f}   valid: {ok}")
    cases = [(1.0, 0.1), (1.0, 0.3), (1.0, 0.5), (2.0, 0.1), (2.0, 0.3), (2.0, 0.6), (4.0, 0.1), (4.0, 0.3), (4.0, 0.6), (0.5, 0.3)]
    if quick:
        cases = [(1.0, 0.3), (2.0, 0.3), (4.0, 0.3)]
    print("== families at the exponential scale: best exponent found against theta_pl ==")
    print("    u   eps1/a   theta_pl   theta_hint |  F1 (soft basin/tilt)        F5 (terrace)        F2 (product)   F3 (K basins, best gamma)   F4 (egg carton)")
    worst = -np.inf
    for (u, f) in cases:
        e1 = f * a_of(u)
        (b1, p1), ref = family_F1(u, e1, quick)
        (b5, p5), _ = family_F5(u, e1, quick)
        b2, p2 = family_F2(u, e1)
        f3 = family_F3(u, e1)
        g3 = max(f3, key=lambda t: t[1])
        b4, p4 = family_F4(u, e1)
        d1 = f"(v/u={p1['v']/u:.2f},rc={p1['rc']:.3f},pi={p1['pi']:.2f})" if p1 else "(none valid)"
        d5 = f"(b={p5['b']:.3f},rt={p5['rt']:.2f},pi={p5['pi']:.2f})" if p5 else "(none valid)"
        print(f"   {u:3.1f}  {f:4.2f}    {ref:.5f}    {theta_hint(u,e1):.5f}  |  {b1:.5f} {d1}   "
              f"{b5:.5f} {d5}   {b2:.5f}        {g3[1]:.5f} (gamma={g3[0]:.3f})        {b4:.5f}", flush=True)
        worst = max(worst, b1 - ref, b5 - ref, b2 - ref, g3[1] - ref, b4 - ref)
    print(f"  largest (family exponent - theta_pl) over all cases: {worst:+.5f}   (grid resolution about 1e-3; a refutation needs a clear positive value)")
    print(f"  time {time.time()-t0:.0f}s")
