#!/usr/bin/env python3
"""Referee replication 1: constants, exponent functions, tables (independent code; mpmath only).

Nothing is imported from the coordinator's scripts.  Run:  python3 -B r1_constants.py
"""
from mpmath import mp, mpf, log, exp, findroot, binomial, diff

mp.dps = 40
LN2 = log(2)


def h2(x):
    return -x * log(x) - (1 - x) * log(1 - x)


def kl(x, y):
    return x * log(x / y) + (1 - x) * log((1 - x) / (1 - y))


def consts(u):
    u = mpf(u)
    pu = 1 / (1 + exp(u))
    a = kl(pu, mpf(1) / 2)
    rho0 = log(2 / (1 + exp(-u))) / u
    h = kl(rho0, mpf(1) / 2)
    ell = log((1 - rho0) / rho0) / u
    return dict(u=u, pu=pu, a=a, rho0=rho0, h=h, ell=ell)


def bisect(f, lo, hi, it=200):
    """Plain bisection (real arithmetic only); f(lo) and f(hi) must have opposite signs."""
    flo, fhi = f(lo), f(hi)
    assert flo * fhi < 0, (flo, fhi)
    for _ in range(it):
        mid = (lo + hi) / 2
        fm = f(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def hbar(lam, c):
    """KL(rho0 - lam/u || 1/2) - lam."""
    return kl(c['rho0'] - lam / c['u'], mpf(1) / 2) - lam


print("== constants ==")
for u in ['0.5', '1', '2']:
    c = consts(u)
    # consistency identities claimed in section 1
    id1 = c['rho0'] - (c['pu'] + c['a'] / c['u'])              # rho0 = p_u + a/u
    id2 = kl(c['rho0'], c['pu']) - c['h']                      # KL(rho0||p_u) = KL(rho0||1/2)
    id3 = (LN2 - h2(c['rho0'])) - c['h']                       # h = ln2 - h2(rho0)
    # Chernoff information between Bernoulli(1/2) and Bernoulli(p_u): max_t -ln sum p^t q^(1-t)
    J = lambda t: -log((mpf(1) / 2) ** (1 - t) * c['pu'] ** t + (mpf(1) / 2) ** (1 - t) * (1 - c['pu']) ** t)
    tstar = bisect(lambda t: diff(J, t), mpf('0.05'), mpf('0.95'))
    print(f"u={u}: p_u={mp.nstr(c['pu'],8)} a={mp.nstr(c['a'],8)} rho0={mp.nstr(c['rho0'],8)} "
          f"h={mp.nstr(c['h'],8)} ell={mp.nstr(c['ell'],6)} 1-ell={mp.nstr(1-c['ell'],6)}")
    print(f"      identities: rho0-(p_u+a/u)={mp.nstr(id1,3)}  KL(rho0||p_u)-h={mp.nstr(id2,3)}  ln2-h2(rho0)-h={mp.nstr(id3,3)}")
    print(f"      Chernoff information max_t J(t) = {mp.nstr(J(tstar),8)} at t*={mp.nstr(tstar,6)}  (report: h, at t=ell; "
          f"note: with J(t)=-ln sum (1/2)^(1-t) p^t the maximiser is the weight on Bernoulli(p_u))")
    # hbar properties
    d0 = diff(lambda x: hbar(x, c), mpf(0))
    da = diff(lambda x: hbar(x, c), c['a'] * (1 - mpf(10) ** -12))
    print(f"      hbar(0)-h={mp.nstr(hbar(mpf(0),c)-c['h'],3)}  hbar(a)={mp.nstr(hbar(c['a']*(1-mpf(10)**-30),c),3)}  "
          f"hbar'(0)={mp.nstr(d0,8)} (-(1-ell)={mp.nstr(-(1-c['ell']),8)})  hbar'(a-)={mp.nstr(da,3)}")
    # convexity / monotonicity on a grid
    ok_dec = all(hbar(c['a'] * mpf(i) / 400, c) > hbar(c['a'] * mpf(i + 1) / 400, c) for i in range(0, 399))
    ok_conv = all(hbar(c['a'] * mpf(i) / 400, c) + hbar(c['a'] * mpf(i + 2) / 400, c) - 2 * hbar(c['a'] * mpf(i + 1) / 400, c) > 0
                  for i in range(0, 398))
    ok_tan = all(hbar(c['a'] * mpf(i) / 400, c) >= c['h'] - (1 - c['ell']) * c['a'] * mpf(i) / 400 - mpf(10) ** -30 for i in range(0, 400))
    print(f"      hbar decreasing on [0,a): {ok_dec}; convex: {ok_conv}; hbar >= h-(1-ell)lam: {ok_tan}")
    # nu*: hbar(nu) = 2 nu
    nus = bisect(lambda x: hbar(x, c) - 2 * x, mpf(0), c['h'])
    print(f"      nu* = {mp.nstr(nus,7)}  nu*/h = {mp.nstr(nus/c['h'],5)}   check hbar(nu*)-2nu* = {mp.nstr(hbar(nus,c)-2*nus,3)}")
    # side condition of Corollary A': hbar(2 gamma) > gamma  (beta = 0)
    gs = bisect(lambda g: hbar(2 * g, c) - g, mpf(0), c['a'] / 2 * (1 - mpf(10) ** -20))
    print(f"      Cor A' side condition hbar(2g)=g at g={mp.nstr(gs,6)} (bound there {mp.nstr(hbar(2*gs,c),5)});  h/2={mp.nstr(c['h']/2,6)}")
    # alpha0, alpha1: h2(alpha)=h, h2(alpha)=a
    a0 = bisect(lambda x: h2(x) - c['h'], mpf(10) ** -12, mpf('0.5'))
    a1 = bisect(lambda x: h2(x) - c['a'], mpf(10) ** -12, mpf('0.5'))
    print(f"      alpha0 (h2=h) = {mp.nstr(a0,6)}   alpha1 (h2=a) = {mp.nstr(a1,6)}")
    # Rao remark: is hbar(h2(alpha/2)) < (1-alpha) h on the whole range where h2(alpha/2) < a ?
    a2 = bisect(lambda x: h2(x / 2) - c['a'], mpf(10) ** -12, mpf('0.999'))
    worst = min(((1 - a2 * mpf(i) / 2000) * c['h'] - hbar(h2(a2 * mpf(i) / 4000), c)) for i in range(1, 2000))
    print(f"      Rao remark: min over alpha in (0,{mp.nstr(a2,5)}) of (1-alpha)h - hbar(h2(alpha/2)) = {mp.nstr(worst,5)} (>0 means: cannot close)")
    # slopes of section 5
    print(f"      slopes at gamma=0: lower -2(1-ell) = {mp.nstr(-2*(1-c['ell']),5)}   upper -h/ln2 = {mp.nstr(-c['h']/LN2,5)}")

print()
print("== table of section 2.3 (u=1, beta=0) ==")
c = consts('1')
print("gamma    h-2g       hbar(2g)   (1-g/ln2)h   [hbar(2g)>g ?]")
for g in ['0', '0.002', '0.005', '0.010', '0.0145']:
    g = mpf(g)
    print(f"{mp.nstr(g,5):7s}  {mp.nstr(c['h']-2*g,6):9s}  {mp.nstr(hbar(2*g,c),6):9s}  {mp.nstr((1-g/LN2)*c['h'],6):9s}   {hbar(2*g,c) > g}")

print()
print("== finite-n check of the asymptotics of section 1 (exact big-number sums) ==")
# m_r = 2^-n sum_{j<r} C(n,j) (e^{u(r-j)}-1),  V(n,r)
def m_r(n, r, u):
    s = mpf(0)
    for j in range(0, r):
        s += binomial(n, j) * (exp(u * (r - j)) - 1)
    return s / mpf(2) ** n


def V(n, r):
    return sum(binomial(n, j) for j in range(0, r + 1))


for u in ['1']:
    c = consts(u)
    for rho in ['0.30', '0.35', '0.379885', '0.45']:
        rho = mpf(rho)
        row = []
        for n in [500, 2000, 8000]:
            r = int(rho * n)
            row.append((n, log(m_r(n, r, c['u'])) / n, log(mpf(2) ** n / V(n, r)) / n))
        print(f"u={u} rho={mp.nstr(rho,6)}: target u(rho-rho0)={mp.nstr(c['u']*(rho-c['rho0']),6)}  KL(rho||1/2)={mp.nstr(kl(rho,mpf(1)/2),6)}")
        for (n, x, y) in row:
            print(f"     n={n:5d}: ln(m_r)/n={mp.nstr(x,6)}   ln(2^n/V)/n={mp.nstr(y,6)}")

print()
print("== Theorem E, exponent of N* at finite n versus hbar(nu)-nu (u=1) ==")
c = consts('1')
for nu in ['0.004', '0.008', '0.0117']:
    nu = mpf(nu)
    for n in [2000, 8000]:
        eta1 = mpf(1) / 40
        m = exp(nu * n)
        K = m * m / eta1
        # smallest r with K m_r >= m/eta1
        lo, hi = 1, n // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if K * m_r(n, mid, c['u']) >= m / eta1:
                hi = mid
            else:
                lo = mid + 1
        r = lo
        Nstar = mpf(2) ** n / (K * V(n, r - 1))
        print(f"nu={mp.nstr(nu,5)} n={n}: r/n={mp.nstr(mpf(r)/n,6)} (rho0-nu/u={mp.nstr(c['rho0']-nu/c['u'],6)})  "
              f"ln N*/n={mp.nstr(log(Nstar)/n,6)}  hbar(nu)-nu={mp.nstr(hbar(nu,c)-nu,6)}  N*>=40m/eta1: {Nstar >= 40*m/eta1}")
