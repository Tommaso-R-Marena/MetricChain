#!/usr/bin/env python3
"""Referee R12, check 6: statements around the main theorem.

Part A  the lower bound quoted in Theorem Q(c): with k*(eps) the least k such that 2^{-n} E_k(n) > e^eps - 1 (Theorem
        11.25(a),(c) of the theory report),  ln[(1 - 2 delta) 2^n/|B(n, k*)|] - n h  for n up to 256000: is it
        >= -O(ln n) ?  (Referee's two-line bound:  k* <= rho_h n + (eps + ln 2)/u, hence
        ln LB >= n h - ((eps + ln 2)/u) ln((1-rho_h)/rho_h) + ln(1 - 2 delta)  as soon as k*/n <= 1/2:  n h - O(1).)
Part B  Proposition Q5(a) for the base family on a wide grid (d = 1..300 and up to 64000; x = 1e-6 ... 3ud; delta from
        0.999 to e^{-10 d}), with Lambda = ln(1/delta) (the weakest form), and Proposition Q5(b) at the least accuracy
        it allows and its consequence.
Part C  an explicit constant for Theorem Q(c): sup over 2 <= n <= 10^12 (40 sizes per decade) of
        ( min{ n ln 2, min_M [n B_M + E_M] } - n h ) / sqrt(n ln n).
Part D  sensitivity of r_dagger to the tolerance used in comparisons of table entries (ties).
Part E  the smallest slope-step level and its cost (can Theorem K1 be simulated in the regime of Q?).

usage: python3 r12_06_misc.py > out_06_misc.txt       (about 15 s)
"""
import sys, os, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r12lib
from r12lib import Cube, Tab, TabCache, Formula, Stats, Base, level_consts, LN2, INF

t0 = time.time()
print("# Referee R12, check 6: the lower bound, the base family, an explicit constant")

# ------------------------------------------------------------------------------------------ Part A
print("\n# Part A: ln LB - n h,  LB = (1 - 2 delta) 2^n/|B(n, k*(eps))|,  delta = 0.05;  'ref' = the referee's bound"
      " -((eps + ln 2)/u) ln((1-rho_h)/rho_h) + ln(1 - 2 delta)")
print("#   u    eps      ref     | n: ln LB - n h  [k* - rho_h n]")
nbad = 0
for u in (0.5, 1.0, 2.0):
    cu = Cube(u)
    for eps in (0.01, 0.1, 1.0, 10.0):
        ref = -((eps + LN2) / u) * math.log((1 - cu.rho_h) / cu.rho_h) + math.log(0.9)
        row = []
        for n in (10, 100, 1000, 4000, 16000, 64000, 256000):
            t = Tab(n, u)
            target = n * LN2 + math.log(math.expm1(eps))
            ks = int(np.searchsorted(t.lE, target, side='right'))              # least k with E_k > 2^n (e^eps - 1)
            ks = min(ks, n)
            lLB = math.log(0.9) + n * LN2 - t.lB[ks]
            row.append("%d: %.3f [%.2f]" % (n, lLB - n * cu.h, ks - cu.rho_h * n))
            if ks / n <= 0.5 and lLB - n * cu.h < ref - 1e-9:
                nbad += 1
            if ks > cu.rho_h * n + (eps + LN2) / u + 1e-9:
                nbad += 1
        print("  %.1f  %5.2f  %8.3f   | %s" % (u, eps, ref, ';  '.join(row)))
print("# violations of the referee's bound: %d   (so ln N >= n h - O(1) for fixed eps and delta < 1/2; the report says n h - O(ln n))" % nbad)
# the corner: small n, where the radius of the argument, ceil(rho_h n + (eps + ln 2)/u - 1), can be below p_u n and the median step
# does not apply as written.  Scan: is  ln LB >= n h - c0 ln((1-rho_h)/rho_h) + ln(1-2 delta),  c0 = (eps + ln 2)/u,  true for EVERY n
# with k*(eps) <= n/2 ?  and with  c0' = max(1, c0)  (which the argument does give for every such n) ?
nc = 0
v_c0 = 0
v_c1 = 0
worst = (INF, None)
ncorner = 0
for u in (0.3, 0.7, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0):
    cu = Cube(u)
    slope = math.log((1 - cu.rho_h) / cu.rho_h)
    for n in range(2, 201):
        t = Tab(n, u)
        for eps in (1e-3, 0.01, 0.03, 0.1, 0.3, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0):
            target = n * LN2 + math.log(math.expm1(eps))
            ks = min(int(np.searchsorted(t.lE, target, side='right')), n)
            if ks > n / 2:
                continue
            nc += 1
            c0 = (eps + LN2) / u
            k0 = math.ceil(cu.rho_h * n + c0 - 1)
            ncorner += (k0 < cu.p * n)
            val = n * LN2 - t.lB[ks] - n * cu.h              # ln LB - n h - ln(1 - 2 delta)
            if val < -c0 * slope - 1e-9:
                v_c0 += 1
            if val < -max(1.0, c0) * slope - 1e-9:
                v_c1 += 1
            if val + c0 * slope < worst[0]:
                worst = (val + c0 * slope, (u, n, eps, ks))
print("#   small sizes: u in {0.3 ... 12}, n = 2 ... 200, eps in {0.001 ... 20}: %d cases with k* <= n/2, of which %d have the radius of the argument below p_u n;"
      % (nc, ncorner))
print("#   violations of the bound with c0 = (eps + ln 2)/u: %d (least slack %.4f at (u, n, eps, k*) = %s);  with max(1, c0): %d" % (v_c0, worst[0], worst[1], v_c1))

# ------------------------------------------------------------------------------------------ Part B
print("\n# Part B: Proposition Q5(a):  b_G0(d, x, delta) <= d a + E_base(d, x; ln(1/delta))")
print("#   u     cases    violations   least slack at (d, x, ln delta)     cases with enumeration   largest cost - d ln 2")
for u in (0.1, 0.5, 1.0, 2.0, 4.0):
    cu = Cube(u)
    fm = Formula(cu)
    st = Stats()
    tabs = TabCache(u, 8)
    base = Base(cu, tabs, st, fm)
    nc = nv = nen = 0
    mins = (INF, None)
    mx = -INF
    ds = list(range(1, 301)) + [400, 700, 1000, 2000, 4000, 8000, 16000, 32000, 64000]
    for d in ds:
        xs = [1e-6, 1e-3, 0.05, 0.3, 0.8715, 1.0, 2.0, 2.2, 3.0, 10.0, 0.01 * u * d, 0.1 * u * d, cu.eps_star * d * 0.5,
              cu.h * d, cu.eps_star * d, u * d, 3 * u * d]
        for x in xs:
            if x <= 0:
                continue
            for ld in (math.log(0.999), math.log(0.05), -40.0, -float(d) - 5, -10.0 * d - 5):
                c, kind, rs = base.raw(d, x, ld)
                nc += 1
                nen += (kind == 'enum')
                sl = d * cu.a + fm.Ebase(d, x, -ld) - c
                mx = max(mx, c - d * LN2)
                if sl < mins[0]:
                    mins = (sl, (d, round(x, 6), round(ld, 2)))
                if sl < -1e-9:
                    nv += 1
    print("  %.1f   %6d   %4d   %9.3f at %s   %6d   %.1e" % (u, nc, nv, mins[0], mins[1], nen, mx))
print("#\n#         Proposition Q5(b): x >= 2 ln 3, x >= ln 12 + 2 ln(d+1) + 2u + e^u + d e  =>  b <= d theta_na(e) + ln(8K) + ln(d+1),"
      " K = ceil(18 ln(4/delta));")
print("#         and for x >= max(c'_d, 2 ln 3):  b <= d theta_na(x/d) + u sqrt(d c'_d/2) + ln(8K(d+1)),  c'_d = ln 12 + 2 ln(d+1) + 2u + e^u")
print("#   u     cases (b)   violations   least slack    | cases (consequence)   violations   least slack")
for u in (0.5, 1.0, 2.0):
    cu = Cube(u)
    fm = Formula(cu)
    st = Stats()
    tabs = TabCache(u, 8)
    base = Base(cu, tabs, st, fm)
    n1 = v1 = n2 = v2 = 0
    m1 = m2 = INF
    for d in list(range(1, 60)) + [100, 300, 1000, 3000, 10000, 64000]:
        cd = math.log(12) + 2 * math.log(d + 1) + 2 * u + math.exp(u)
        for ld in (math.log(0.5), math.log(0.05), -float(d)):
            K = math.ceil(18 * (math.log(4) - ld))
            for ef in (0.0, 0.01, 0.1, 0.5, cu.h / cu.eps_star, 0.9, 1.0, 2.0):
                e = ef * cu.eps_star
                x = max(2 * math.log(3), cd + d * e)
                c = base.raw(d, x, ld)[0]
                sl = d * cu.theta_na(e) + math.log(8 * K) + math.log(d + 1) - c
                n1 += 1
                m1 = min(m1, sl)
                v1 += (sl < -1e-9)
            for xf in (1.0, 1.5, 3.0, 10.0, 100.0):
                x = max(cd, 2 * math.log(3)) * xf
                c = base.raw(d, x, ld)[0]
                sl = d * cu.theta_na(x / d) + u * math.sqrt(d * cd / 2) + math.log(8 * K * (d + 1)) - c
                n2 += 1
                m2 = min(m2, sl)
                v2 += (sl < -1e-9)
    print("  %.1f   %6d   %4d   %9.3f     | %6d   %4d   %9.3f" % (u, n1, v1, m1, n2, v2, m2))

# ------------------------------------------------------------------------------------------ Part C
print("\n# Part C: an explicit constant.  ratio(n) = ( min{n ln 2, min_M [n B_M + E_M(n, eps, delta)]} - n h )/sqrt(n ln n),")
print("#         maximised over 2 <= n <= 10^12 (every integer up to 300, then 40 sizes per decade up to 10^6 and 10 per decade above);")
print("#         M ranges over the epochs with k_M <= max(100, 0.15 sqrt(n)) (the minimum is interior: asserted)")
print("#   u    eps     delta      sup of the ratio   at n       (which bound there)     ratio at 1e12    2 sqrt((a-h)(a/h+4))    C_*")


def E_total_fast(fm, n, eps, ld, M, ep):
    """(5.2), the same recursion as r12lib.Formula.E_total with the n-dependent constants of c_S, q_S taken out of the loop"""
    c = fm.c
    eh, cm, alpha = fm.schedule(eps, M)
    Lam = -ld + n * LN2
    A = fm.A(n)
    c0 = math.log(2) + math.log(A) + math.log(fm.mbarS(n)) + math.log(n + 3)
    const2 = math.log(4 * (n + 1)) + math.log(A) + math.log(24 * math.e * (math.e - 1))
    base1 = 1 + 2 * math.log(A) + math.log(18 * math.e * (math.e - 1)) + math.log(n + 3)
    tot = 0.0
    for m in range(M - 1, -1, -1):
        B, R = ep['B'][m], ep['R'][m]
        tot += fm.cD(n, Lam, B, R, cm[m])
        Lam += fm.qD(n, Lam, cm[m])
        const1 = (1 + fm.clog(n) + c.h) * B / c.h + base1
        for _ in range(ep['J'][m]):
            lk = math.log(18 * (Lam + c0) + 1)
            tot += const1 + lk
            Lam += const2 + lk
    return tot + fm.Ebase(n, alpha[0], Lam)


def best_formula(fm, n, eps, ld, ep):
    kcap = max(100.0, 0.15 * math.sqrt(n))
    b = (INF, -1)
    last = 0
    for M in range(200):
        if ep['k'][M] > kcap:
            break
        v = n * ep['B'][M] + E_total_fast(fm, n, eps, ld, M, ep)
        last = M
        if v < b[0]:
            b = (v, M)
    assert b[1] < last
    return b


# self-test of the fast recursion
_c = Cube(1.0)
_f = Formula(_c)
_ep = _c.epochs(200)
for (_n, _M) in ((1000, 3), (64000, 5), (1e8, 17), (1e10, 25)):
    assert abs(E_total_fast(_f, _n, 1.0, math.log(0.05), _M, _ep) - _f.E_total(_n, 1.0, math.log(0.05), _M)[0]) < 1e-6 * _n ** 0.5

for (u, eps, delta) in ((1.0, 1.0, 0.05), (0.5, 1.0, 0.05), (2.0, 1.0, 0.05), (1.0, 0.01, 0.05), (1.0, 1.0, 1e-9), (4.0, 1.0, 0.05)):
    cu = Cube(u)
    fm = Formula(cu)
    ep = cu.epochs(200)
    ld = math.log(delta)
    sizes = (list(range(2, 301)) + [int(round(10 ** x)) for x in np.arange(2.5, 6.0001, 0.025)]
             + [int(round(10 ** x)) for x in np.arange(6.1, 12.0001, 0.1)])
    sup = (-INF, None, None)
    last = None
    for n in sizes:
        val, M = best_formula(fm, n, eps, ld, ep)
        triv = n * LN2
        v = min(val, triv)
        r = (v - n * cu.h) / math.sqrt(n * math.log(n))
        if r > sup[0]:
            sup = (r, n, 'enumeration 2^n' if triv <= val else 'formula, M = %d' % M)
        last = r
    print("  %.1f  %5.2f  %8.1e      %7.3f        %9d   %-22s    %7.3f          %7.3f              %.3f"
          % (u, eps, delta, sup[0], sup[1], sup[2], last, 2 * math.sqrt((cu.a - cu.h) * (cu.a / cu.h + 4)), cu.Cstar))
    sys.stdout.flush()

# ------------------------------------------------------------------------------------------ Part D
print("\n# Part D: r_dagger with the comparison tolerance +1e-12 (as used), -1e-9 and +1e-9; K_REPORT 6.4 design (n_o = n/2) and slope-step levels")
nd = 0
ntot = 0
for u in (0.5, 1.0, 2.0):
    cu = Cube(u)
    fm = Formula(cu)
    for n in (1000, 1400, 2000, 4000, 8000, 16000, 32000):
        res = []
        for tol in (1e-12, -1e-9, 1e-9):
            r12lib.TOL = tol
            t = Tab(n // 2, u)
            cs = level_consts(cu, t, n, n // 2, 0.2, 0.05, 0.05, math.log(0.05), 2 * math.exp(u) * (n // 2) / 0.05, 0.5, math.log(0.05), 40)
            xh = 0.7 * cu.h * n
            if xh >= fm.X0(n):
                n_o = math.floor((xh - 1 - fm.clog(n)) / cu.h + 1e-12)
                t2 = Tab(n_o, u)
                lth = (xh - 1) + math.log1p(-((3 * math.e + 1) + math.exp(n * math.log(2 * cu.p) - 1)) * math.exp(-(xh - 1)))
                cs2 = level_consts(cu, t2, n, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, math.log(0.05), math.ceil(xh))
                res.append((cs['rdag'], cs2['rdag']))
            else:
                res.append((cs['rdag'], None))
        r12lib.TOL = 1e-12
        ntot += 1
        nd += (len(set(res)) > 1)
print("  %d designs, r_dagger depends on the tolerance in %d" % (ntot, nd))
# ------------------------------------------------------------------------------------------ Part E
print("\n# Part E: the smallest slope-step level (least n with h n >= X_0(n)), and what it costs: could Theorem K1 be simulated in this regime?")
from r12lib import build_design, level_cmax
bestn = None
for i in range(50, 601, 5):
    uu = i / 100
    c_ = Cube(uu)
    f_ = Formula(c_)
    n = 2
    while c_.h * n < f_.X0(n):
        n += 1
    if bestn is None or n < bestn[0]:
        bestn = (n, uu)
print("  least first size over u in {0.50, 0.55, ..., 6.00}: n = %d at u = %.2f" % bestn)
print("#   u      n    xhat = X_0   n_o   L    K      ln C_max (level as built)   ln(K C_1) (the first K points each need the first rung)   base family at the same accuracy   n ln 2")
for uu in (1.0, 2.0, bestn[1], 4.0):
    c_ = Cube(uu)
    f_ = Formula(c_)
    n = 2
    while c_.h * n < f_.X0(n):
        n += 1
    fam, fams, fm_, st_ = build_design(c_, 1.0, 1)
    S = fams[1]
    xh = f_.X0(n)
    ld = math.log(0.05)
    lev = S.level(n, xh, ld)
    n_o = math.floor((xh - 1 - f_.clog(n)) / c_.h + 1e-12)
    n_i = n - n_o
    x1 = min(math.ceil(xh), math.ceil(2 * uu * n_i) - 1)
    lth = (xh - 1) + math.log1p(-((3 * math.e + 1) + math.exp(n * math.log(2 * c_.p) - 1)) * math.exp(-(xh - 1)))
    cs = level_consts(c_, Tab(n_o, uu), n, n_o, 1.0, 0.5, 1.0, lth, 1.0, 1.0, ld, x1)
    c1 = fams[0].raw(n_i, float(x1), cs['ldeltap'])[0]
    print("  %.2f  %5d   %7.2f   %3d  %3d  %5d      %8.1f                    %8.1f                                              %8.1f                   %8.1f"
          % (uu, n, xh, n_o, x1, cs['K'], lev, cs['lK'] + c1, fams[0].raw(n, xh, ld)[0], n * LN2))

print("\n# done in %.0f s" % (time.time() - t0))
