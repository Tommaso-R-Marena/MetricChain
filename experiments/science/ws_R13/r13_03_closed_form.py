#!/usr/bin/env python3
"""R13 / item 1 (ii)-(iii): the constants, and a test of the CLOSED FORM against the EPOCH RECURSION.

(A) constants kappa, c1, c2 for the cube at u = 0.5, 1, 2 (and a few more) with mpmath at 40 digits,
    from the definitions  p_u = 1/(1+e^u), Lam1 = ln(2/(1+e^-u)), a = KL(p_u||1/2), h = KL(Lam1/u||1/2),
    kappa = h^2 a/((a-h)(a+h)(2a-h)), c1 = h(1+kappa)/kappa, c2 = (a+h)(2a-h)/(h a) - 2.
(B) the epoch recursion of statement (a):  d_0 = h/(a-h), k_0 = 1, J_m = ceil(d_m),
        d_{m+1} = d_m (J_m a + h)/(J_m a - h d_m),   k_{m+1} = k_m + J_m + 1,
    gives B_k <= h(1+1/d_m) for k_m <= k < k_{m+1}.  The closed form claims h/d_m <= c1/(k+c2) for those k.
    Tested in EXACT rational arithmetic (fractions.Fraction; a, h rational) at the worst k of every epoch
    (k = k_{m+1}-1; the right side decreases in k), together with the intermediate claims
        d_{m+1} - d_m > (J_m+1) kappa,    d_m >= d_0 + kappa (k_m - 1),
    and the limsup statement: k (B_k - h) at the worst k of late epochs against a.
(C) the same in floating point for many pairs (a, h), h/a from 1e-4 to 1-1e-4.

Nothing here uses the theory division's code.  Usage: python3 r13_03_closed_form.py
"""
import math, random
from fractions import Fraction as Fr
import mpmath as mp


def cube_consts_mp(u):
    mp.mp.dps = 40
    u = mp.mpf(u)
    p = 1 / (1 + mp.e ** u)
    lam = mp.log(2 / (1 + mp.e ** (-u)))
    kl = lambda r, q: r * mp.log(r / q) + (1 - r) * mp.log((1 - r) / (1 - q))
    a = kl(p, mp.mpf(1) / 2)
    h = kl(lam / u, mp.mpf(1) / 2)
    estar = mp.log(mp.cosh(u / 2))
    kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
    c1 = h * (1 + kappa) / kappa
    c2 = (a + h) * (2 * a - h) / (h * a) - 2
    return dict(p=p, lam=lam, estar=estar, a=a, h=h, kappa=kappa, c1=c1, c2=c2)


def consts(a, h):
    kappa = h * h * a / ((a - h) * (a + h) * (2 * a - h))
    c1 = h * (1 + kappa) / kappa
    c2 = (a + h) * (2 * a - h) / (h * a) - 2
    return kappa, c1, c2


def ceil_fr(x):
    return -((-x.numerator) // x.denominator)


def epochs_exact(a, h, kmax):
    """exact rational epoch recursion; returns list of (k_m, J_m, d_m) and the checks."""
    kappa, c1, c2 = consts(a, h)
    d, k = h / (a - h), 1
    d0 = d
    worst = Fr(0)
    ok_gain = ok_lin = ok_closed = True
    rows = []
    while k <= kmax:
        J = ceil_fr(d)
        klast = k + J                      # last level of the epoch
        ratio = (h / d) / (c1 / (klast + c2))
        worst = max(worst, ratio)
        ok_closed &= ratio <= 1
        ok_lin &= d >= d0 + kappa * (k - 1)
        dn = d * (J * a + h) / (J * a - h * d)
        ok_gain &= (dn - d) > (J + 1) * kappa
        rows.append((k, J, float(d), float(ratio), float(klast * (h / d) / a)))
        d, k = dn, k + J + 1
        # keep the rationals small enough: stop the exact run when the numbers explode
        if d.denominator.bit_length() > 60000:
            break
    return rows, float(worst), ok_gain, ok_lin, ok_closed


def epochs_float(a, h, kmax):
    kappa, c1, c2 = consts(a, h)
    d, k = h / (a - h), 1
    d0 = d
    worst = 0.0
    last_scaled = None
    bad = 0
    n = 0
    while k <= kmax:
        J = math.ceil(d - 1e-13)
        klast = k + J
        ratio = (h / d) / (c1 / (klast + c2))
        worst = max(worst, ratio)
        if ratio > 1 + 1e-9 or d < (d0 + kappa * (k - 1)) * (1 - 1e-9):
            bad += 1
        last_scaled = klast * (h / d) / a
        d, k = d * (J * a + h) / (J * a - h * d), k + J + 1
        n += 1
    return worst, last_scaled, bad, n


if __name__ == '__main__':
    print("# r13_03_closed_form.py")
    print("## (A) constants of the cube (mpmath, 40 digits; printed to 12)")
    print("   u |      p_u       |      Lam1      |      eps*      |       a        |       h        |   kappa    |     c1     |     c2     | c1/a")
    for u in ('0.25', '0.5', '1', '2', '4'):
        c = cube_consts_mp(u)
        print(f"{u:>4} | {mp.nstr(c['p'],12):>14} | {mp.nstr(c['lam'],12):>14} | {mp.nstr(c['estar'],12):>14} | {mp.nstr(c['a'],12):>14} | "
              f"{mp.nstr(c['h'],12):>14} | {mp.nstr(c['kappa'],8):>10} | {mp.nstr(c['c1'],8):>10} | {mp.nstr(c['c2'],8):>10} | {mp.nstr(c['c1']/c['a'],6)}")
    print("   identities checked at 40 digits: theta_na(h) = h means KL(Lam1/u || p_u) = h; eps* = KL(1/2||p_u) = u/2 - Lam1")
    for u in ('0.5', '1', '2'):
        c = cube_consts_mp(u)
        uu = mp.mpf(u)
        kl = lambda r, q: r * mp.log(r / q) + (1 - r) * mp.log((1 - r) / (1 - q))
        e1 = kl(c['lam'] / uu, c['p']) - c['h']
        e2 = kl(mp.mpf(1) / 2, c['p']) - c['estar']
        e3 = uu / 2 - c['lam'] - c['estar']
        print(f"   u={u}: KL(Lam1/u||p_u) - h = {mp.nstr(e1,3)};  KL(1/2||p_u) - eps* = {mp.nstr(e2,3)};  u/2 - Lam1 - eps* = {mp.nstr(e3,3)}")

    print("## (B) exact rational test of the closed form against the epoch recursion")
    print("   (a, h) rational; columns: epochs run | last k reached | worst (h/d_m)/(c1/(k+c2)) over epochs (must be <= 1) | gain>(J+1)kappa | d_m>=d_0+kappa(k_m-1) | closed form")
    pairs = []
    for u in ('0.5', '1', '2'):
        c = cube_consts_mp(u)
        pairs.append((f"cube u={u} (a,h rounded to 12 digits)", Fr(int(mp.floor(c['a'] * 10**12)), 10**12), Fr(int(mp.floor(c['h'] * 10**12)), 10**12)))
    pairs += [("gauss pair a=1,h=1/4", Fr(1), Fr(1, 4)), ("a=1,h=1/2 (d_0=1, integer)", Fr(1), Fr(1, 2)),
              ("a=3,h=2 (d_0=2, integer)", Fr(3), Fr(2)), ("a=1,h=9/10", Fr(1), Fr(9, 10)), ("a=1,h=999/1000", Fr(1), Fr(999, 1000)),
              ("a=1,h=1/100", Fr(1), Fr(1, 100)), ("a=1,h=1/3", Fr(1), Fr(1, 3)), ("a=7,h=5", Fr(7), Fr(5))]
    allok = True
    for name, a, h in pairs:
        rows, worst, g, l, cl = epochs_exact(a, h, 10**7)
        allok &= g and l and cl
        print(f"   {name:42s} | {len(rows):3d} | k={rows[-1][0] + rows[-1][1]:>9d} | {worst:.6f} | {g} | {l} | {cl}")
        if name.startswith("cube u=1"):
            print("      first epochs (k_m, J_m, d_m, ratio at the last level of the epoch, k(B_k-h)/a there):")
            for r in rows[:8]:
                print(f"        k_m={r[0]:5d} J_m={r[1]:4d} d_m={r[2]:10.4f} ratio={r[3]:.4f} k(B-h)/a={r[4]:.4f}")
            print(f"        ... last: k_m={rows[-1][0]} J_m={rows[-1][1]} d_m={rows[-1][2]:.3f} ratio={rows[-1][3]:.4f} k(B-h)/a={rows[-1][4]:.4f}")
    print(f"   all exact checks passed: {allok}")

    print("## (C) floating-point scan, k up to 1e9, 4000 random pairs (a, h) + a structured ladder")
    random.seed(13)
    worst_all, worst_pair, nbad = 0.0, None, 0
    lims = []
    tests = []
    for i in range(4000):
        a = 10 ** random.uniform(-3, 3)
        t = random.random()
        if i % 3 == 0:
            r = 10 ** random.uniform(-4, 0) * 0.9999
        elif i % 3 == 1:
            r = 1 - 10 ** random.uniform(-4, 0) * 0.9999
        else:
            r = random.uniform(0.0001, 0.9999)
        tests.append((a, a * r))
    for r in (0.0001, 0.001, 0.01, 0.1, 0.25, 0.2627, 1 / 3, 0.4999999, 0.5, 0.5000001, 2 / 3, 0.75, 0.9, 0.99, 0.999, 0.9999):
        tests.append((1.0, r))
    for a, h in tests:
        worst, last_scaled, bad, n = epochs_float(a, h, 10**9)
        nbad += bad
        lims.append(last_scaled)
        if worst > worst_all:
            worst_all, worst_pair = worst, (a, h)
    print(f"   pairs: {len(tests)}; violations of the closed form or of d_m >= d_0 + kappa(k_m-1): {nbad}")
    print(f"   largest (h/d_m)/(c1/(k+c2)) over all pairs and epochs: {worst_all:.9f} at (a,h)={worst_pair} (h/a={worst_pair[1]/worst_pair[0]:.6f})")
    print(f"   k(B_k-h)/a at the last level of the last epoch (k ~ 1e9): min {min(lims):.6f}, max {max(lims):.6f}   (limsup claim: <= 1)")
    print("# END")
