"""
t04_beyond_two_letters.py -- the 'two-letter statements that fail beyond two letters' (THY-MSG-0011 section 1(d);
Propositions 11.100, 11.103), with r5lib (own implementation).

(a) the site function of the triangle site (1, 1.5, 2), pi = (0.2, 0.5, 0.3) is not concave: label switch near t = 0.378
(b) three letters, Hamming envelope, u = 1: the uniform site law is not the hardest near the threshold
(c) small slopes: three letters uniform against laws close to (1/2, 1/2, 0); crossing of h at u = ln 2, of a near 0.5194
(d) uniform four-letter Hamming site, u = 1: h = h_2, a = a_4, E = E_2
(e) exact crossing h_k = h_{k+1} at e^u = k(k-1)  (closed forms; high precision with mpmath)
"""
import time
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
from r5lib import *

np.set_printoptions(precision=6, suppress=True, linewidth=160)


def hamming(q, u):
    d = u * (np.ones((q, q)) - np.eye(q))
    return d


def Psi(k, s):
    return np.log((np.exp(s) + k - 1) / k) - s / k


def F_k(k, u, t):
    return t * Psi(k, u) - Psi(k, t * u)


def h_k(k, u):
    return Rhat(lambda t: F_k(k, u, t), 0.0, ngrid=400)[0]


def a_k(k, u):
    p = np.exp(u) / (np.exp(u) + k - 1)
    r = (1 - p) / (k - 1)
    return np.log(k) + p * np.log(p) + (k - 1) * r * np.log(r)


def E_k(k, u):
    return Psi(k, u)


def site_h(s):
    return Rhat(lambda t: Fstar_site(s, t), 0.0, ngrid=300)


if __name__ == "__main__":
    t0 = time.time()
    # ------------------------------------------------------------------------------------------ (a)
    print("== (a) triangle site (1, 1.5, 2), pi = (0.2, 0.5, 0.3): F* is not concave ==")
    tri = Site([0.2, 0.5, 0.3], [[0, 1, 2], [1, 0, 1.5], [2, 1.5, 0]], "tri")
    ts = np.linspace(0.30, 0.46, 161)
    F = np.array([Fstar_site(tri, t) for t in ts])
    gaps = max(Fstar_gap(tri, t) for t in ts)
    d2 = F[2:] - 2 * F[1:-1] + F[:-2]
    i = int(np.argmax(d2))
    print(f"grid step 0.001 on [0.30,0.46]; largest duality gap {gaps:.1e}; largest second difference {d2.max():+.3e} at t = {ts[i+1]:.3f}"
          f" (all others: max {np.delete(d2, i).max():+.3e})")
    # supports of M* on both sides and the slope jump
    def support(t):
        lo, M, hi = renyi_primal(tri, t)
        return [(tuple(np.round(tri.V[k], 2).tolist()), round(float(M[k]), 3)) for k in range(len(M)) if M[k] > 1e-5]
    for t in (0.36, 0.37, 0.375, 0.378, 0.38, 0.385, 0.40):
        print(f"   t={t:.3f}  F*={Fstar_site(tri, t):.9f}  M* = {support(t)}")
    # locate the switch: bisection on 'number of support points / presence of vertex (0,-1,0.5)'
    def n_dips(t):
        lo, M, hi = renyi_primal(tri, t)
        return int(np.sum(M > 1e-5))
    # slope from the left and from the right of the kink by one-sided differences
    tc_lo, tc_hi = 0.37, 0.39
    def which(t):
        lo, M, hi = renyi_primal(tri, t)
        k = [j for j in range(len(M)) if M[j] > 1e-5]
        return tuple(k)
    wl, wh = which(tc_lo), which(tc_hi)
    for _ in range(40):
        mid = 0.5 * (tc_lo + tc_hi)
        if which(mid) == wl:
            tc_lo = mid
        else:
            tc_hi = mid
    tc = 0.5 * (tc_lo + tc_hi)
    hstep = 1e-4
    sl = (Fstar_site(tri, tc - 1e-6) - Fstar_site(tri, tc - 1e-6 - hstep)) / hstep
    sr = (Fstar_site(tri, tc + 1e-6 + hstep) - Fstar_site(tri, tc + 1e-6)) / hstep
    E_tri = threshold_E(tri)[0]
    print(f"   label switch at t_c = {tc:.5f} (support {wl} -> {wh}); slope left {sl:+.5f}, right {sr:+.5f}, jump {sr-sl:+.5f}"
          f"  [theirs: t_c = 0.378, jump +0.0052]")
    print(f"   corner of R^ at e in [-slope right, -slope left]... as fraction of E: [{-sr/E_tri:.4f}, {-sl/E_tri:.4f}]  [theirs: corner at 0.1996 E,"
          f" slopes -0.383 -> -0.373]")
    # concave envelope gap: is F* strictly below its concave envelope somewhere?
    tt = np.linspace(0.0, 1.0, 2001)
    FF = np.array([Fstar_site(tri, t) for t in tt])
    # upper concave envelope by a monotone-chain hull
    hull = []
    for x, y in zip(tt, FF):
        while len(hull) >= 2 and (hull[-1][0] - hull[-2][0]) * (y - hull[-2][1]) - (hull[-1][1] - hull[-2][1]) * (x - hull[-2][0]) >= 0:
            hull.pop()
        hull.append((x, y))
    hx, hy = np.array(hull).T
    env = np.interp(tt, hx, hy)
    k = int(np.argmax(env - FF))
    print(f"   concave envelope minus F*: max {np.max(env-FF):.3e} at t = {tt[k]:.4f}  (positive => F* is not concave)")
    # two-letter control: concavity on a few binary sites
    worst = -np.inf
    for u in (0.3, 1.0, 2.0, 4.0):
        for th in (0.0, 0.7, 2.0, 5.0):
            p = 1 / (1 + np.exp(th))
            s = Site([1 - p, p], [[0, u], [u, 0]])
            tg = np.linspace(0.01, 0.99, 99)
            Fg = np.array([Fstar_site(s, t) for t in tg])
            worst = max(worst, (Fg[2:] - 2 * Fg[1:-1] + Fg[:-2]).max())
    print(f"   control: 16 two-letter sites, largest second difference of F* on a grid of step 0.01: {worst:+.2e} (negative = concave)")
    print()
    # ------------------------------------------------------------------------------------------ (b)
    print("== (b) three letters, Hamming, u = 1: thresholds ==")
    s_uni = Site([1/3, 1/3, 1/3], hamming(3, 1.0), "ham3")
    s_tilt = Site([0.05, 0.5, 0.45], hamming(3, 1.0), "ham3tilt")
    cube = Site([0.5, 0.5], hamming(2, 1.0), "cube")
    for nm, s, ref in (("uniform", s_uni, 0.119499), ("(0.05,0.5,0.45)", s_tilt, 0.120196), ("two-letter cube", cube, 0.120115)):
        lo, hi, M = threshold_E(s)
        print(f"   E[{nm}] in [{lo:.9f}, {hi:.9f}]   theirs {ref:.6f}   diff {lo-ref:+.1e}   (#vertices {len(s.V)})")
    print(f"   vertices of the uniform three-letter Hamming site: {np.round(s_uni.V, 3).tolist()}")
    # F*(t; tilt) > F*(t; uniform) for small t ?
    for t in (0.01, 0.03, 0.05, 0.1, 0.3):
        print(f"   t={t}: F*(tilt) - F*(uniform) = {Fstar_site(s_tilt, t) - Fstar_site(s_uni, t):+.3e}")
    hu, au = site_h(s_uni)[0], capacity_a(s_uni)[0]
    print(f"   h, a for the uniform law at u=1: {hu:.6f}, {au:.6f}   [W_REPORT: 0.030654, 0.123284]")
    print()
    # ------------------------------------------------------------------------------------------ (c)
    print("== (c) small slopes: three letters uniform against site laws close to (1/2,1/2,0) ==")
    for u, what in ((0.5, "h"), (0.3, "a")):
        su = Site([1/3, 1/3, 1/3], hamming(3, u))
        vals = []
        for eta in (1e-2, 1e-4, 1e-6):
            sd = Site([(1 - eta) / 2, (1 - eta) / 2, eta], hamming(3, u))
            vals.append((eta, site_h(sd)[0], capacity_a(sd)[0]))
        c2 = Site([0.5, 0.5], hamming(2, u))
        print(f"   u={u}: uniform: h={site_h(su)[0]:.6f} a={capacity_a(su)[0]:.6f}; closed forms h_3={h_k(3,u):.6f} a_3={a_k(3,u):.6f};"
              f" two-letter cube: h_2={h_k(2,u):.6f} (site {site_h(c2)[0]:.6f}) a_2={a_k(2,u):.6f} (site {capacity_a(c2)[0]:.6f})")
        for eta, hh, aa in vals:
            print(f"        law ((1-eta)/2,(1-eta)/2,eta), eta={eta:g}: h={hh:.6f} a={aa:.6f}")
    print("   [theirs: h_2=0.007673 > h_3=0.007425 at u=0.5;  a_2=0.011125 > a_3=0.010582 at u=0.3]")
    ucross_h = brentq(lambda u: h_k(2, u) - h_k(3, u), 0.3, 1.2, xtol=1e-12)
    ucross_a = brentq(lambda u: a_k(2, u) - a_k(3, u), 0.3, 1.2, xtol=1e-12)
    print(f"   crossing of h_2 and h_3: u = {ucross_h:.9f}  (ln 2 = {np.log(2):.9f});  crossing of a_2 and a_3: u = {ucross_a:.6f} [theirs 0.5194]")
    for u in (0.6, np.log(2) - 0.02, np.log(2) + 0.02, 0.8):
        su = Site([1/3, 1/3, 1/3], hamming(3, u))
        sd = Site([(1 - 1e-6) / 2, (1 - 1e-6) / 2, 1e-6], hamming(3, u))
        print(f"   u={u:.4f}: h(uniform three letters) = {site_h(su)[0]:.8f}, h(law near (1/2,1/2,0)) = {site_h(sd)[0]:.8f}, "
              f"difference {site_h(sd)[0]-site_h(su)[0]:+.2e}")
    print()
    # ------------------------------------------------------------------------------------------ (d)
    print("== (d) uniform q-letter Hamming sites: each of E, a, h against the best equal grouping ==")
    for q in (3, 4):
        divs = [k for k in range(2, q + 1) if q % k == 0]
        for u in (0.5, 1.0, 2.0, 3.0):
            s = Site(np.full(q, 1.0 / q), hamming(q, u))
            E = threshold_E(s)
            a = capacity_a(s)
            h = site_h(s)[0]
            Ek = {k: E_k(k, u) for k in divs}
            ak = {k: a_k(k, u) for k in divs}
            hk = {k: h_k(k, u) for k in divs}
            bE, ba, bh = max(Ek, key=Ek.get), max(ak, key=ak.get), max(hk, key=hk.get)
            print(f"   q={q} u={u}: #vertices {len(s.V)}; E={E[0]:.6f} (best grouping k={bE}: {Ek[bE]:.6f}, diff {E[0]-Ek[bE]:+.1e});"
                  f" a={a[0]:.6f} (k={ba}: {ak[ba]:.6f}, diff {a[0]-ak[ba]:+.1e}); h={h:.6f} (k={bh}: {hk[bh]:.6f}, diff {h-hk[bh]:+.1e})")
    print("   [theirs, q=4, u=1: h = h_2 = 0.029139, a = a_4 = 0.117993, E = E_2 = 0.120115]")
    print()
    # ------------------------------------------------------------------------------------------ (e)
    print("== (e) exact crossing h_k = h_{k+1} at e^u = k(k-1): closed form, 40 digits ==")
    mp.mp.dps = 40

    def h_closed(k, u):
        # h_k = ln k - H_b(c) - (1-c) ln(k-1),  c = ln((e^u+k-1)/k)/u  (derived by hand, see NOTES/REPORT)
        k = mp.mpf(k)
        c = mp.log((mp.e ** u + k - 1) / k) / u
        return mp.log(k) + c * mp.log(c) + (1 - c) * mp.log(1 - c) - (1 - c) * mp.log(k - 1) if k > 1 else mp.mpf(0)

    def h_numeric(k, u):
        k = mp.mpf(k)
        f = lambda t: t * (mp.log((mp.e ** u + k - 1) / k) - u / k) - (mp.log((mp.e ** (t * u) + k - 1) / k) - t * u / k)
        tstar = mp.findroot(lambda t: mp.diff(f, t), mp.mpf("0.5"))
        return f(tstar), tstar

    for k in range(2, 9):
        u = mp.log(k * (k - 1))
        d = h_closed(k, u) - h_closed(k + 1, u)
        hn, ts_ = h_numeric(k, u)
        hn1, ts1 = h_numeric(k + 1, u)
        ck = mp.log((mp.e ** u + k - 1) / k) / u
        ck1 = mp.log((mp.e ** u + k) / (k + 1)) / u
        eps = mp.mpf("0.01")
        dm = h_closed(k, u - eps) - h_closed(k + 1, u - eps)
        dp = h_closed(k, u + eps) - h_closed(k + 1, u + eps)
        print(f"   k={k}: u=ln {k*(k-1)} = {mp.nstr(u, 8)}; h_k = {mp.nstr(hn, 12)} (t*={mp.nstr(ts_, 6)}), h_k+1 = {mp.nstr(hn1, 12)} (t*={mp.nstr(ts1, 6)});"
              f" closed-form difference {mp.nstr(d, 3)}; numeric max - closed: {mp.nstr(hn - h_closed(k, u), 3)}; c_k + c_k+1 - 1 = {mp.nstr(ck + ck1 - 1, 3)};"
              f" sign below/above: {mp.nstr(dm, 3)} / {mp.nstr(dp, 3)}")
    # which k is the hardest equal grouping at slope u?
    for u in (0.5, 1.0, 2.0, 3.0, 4.0, 6.0):
        hs = [float(h_closed(k, mp.mpf(u))) for k in range(2, 60)]
        kbest = 2 + int(np.argmax(hs))
        print(f"   u={u}: argmax_k h_k = {kbest}; (k-1)(k-2) = {(kbest-1)*(kbest-2)} <= e^u = {np.exp(u):.2f} <= k(k-1) = {kbest*(kbest-1)};  e^(u/2) = {np.exp(u/2):.2f}")
    print(f"[{time.time()-t0:.1f} s]")
