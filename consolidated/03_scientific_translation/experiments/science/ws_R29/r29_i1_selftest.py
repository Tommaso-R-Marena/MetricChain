#!/usr/bin/env python3
"""r29_i1_selftest.py -- tests of my own library r29lib.py, each with a control that must fail.

 T1  DI (my interval arithmetic) against mpmath at 80 digits: ln, exp, KL -- the mp value must lie in the interval.
     control: a deliberately damaged series (remainder dropped, one term less) must lose the containment.
 T2  upper_hull / PL against brute force on random line sets (exact).  control: a damaged hull must be caught.
 T3  top_exact: c' + abar V(c') = abar exactly.  control: a top moved down by 2^-100 must fail (S1).
 T4  the cube pair in multiprecision: Sigma through J against Sigma by direct maximisation; theta(h) = h;
     theta_na(e + theta_hint(e)) = theta_hint(e); J(L) = h; KL shift identity.  control: a wrong Lambda must fail.
"""
import random
import sys
from fractions import Fraction as Fr

import r29lib as R

R.cap_memory()
import mpmath  # noqa: E402

mp = mpmath.mp
mp.dps = 80
fails = 0


def inside(I, x, slack=mpmath.mpf(10) ** -70):
    lo = mpmath.mpf(I.lo) / mpmath.mpf(2) ** R.DI.P
    hi = mpmath.mpf(I.hi) / mpmath.mpf(2) ** R.DI.P
    return lo - slack <= x <= hi + slack


def frac_mp(q):
    return mpmath.mpf(q.numerator) / mpmath.mpf(q.denominator)


# ------------------------------------------------------------------------------------------------------------ T1
rng = random.Random(29)
n_ok = n_bad = 0
maxw = 0
for _ in range(400):
    q = Fr(rng.randrange(1, 10 ** 12), rng.randrange(1, 10 ** 12)) * Fr(2) ** rng.randrange(-40, 40)
    I = R.DI.of(q).log()
    x = mpmath.log(frac_mp(q))
    maxw = max(maxw, I.hi - I.lo)
    if inside(I, x, 0):
        n_ok += 1
    else:
        n_bad += 1
for _ in range(100):
    q = Fr(rng.randrange(0, 8 * 10 ** 6), 10 ** 6)
    I = R.DI.exp_rational(q)
    if inside(I, mpmath.exp(frac_mp(q)), 0):
        n_ok += 1
    else:
        n_bad += 1
for u in ("1/2", "1", "2", "7/3"):
    C = R.CubeDI(Fr(u))
    um = frac_mp(Fr(u))
    pu = 1 / (1 + mpmath.exp(um))
    for _ in range(100):
        rho = Fr(rng.randrange(1, 2 ** 40), 2 ** 40)
        E, TH = C.pair_enclosures(rho)
        r = frac_mp(rho)
        e = r * mpmath.log(r / pu) + (1 - r) * mpmath.log((1 - r) / (1 - pu))
        th = r * mpmath.log(2 * r) + (1 - r) * mpmath.log(2 * (1 - r))
        for I, x in ((E, e), (TH, th)):
            maxw = max(maxw, I.hi - I.lo)
            if inside(I, x, 0):
                n_ok += 1
            else:
                n_bad += 1
    a = pu * mpmath.log(2 * pu) + (1 - pu) * mpmath.log(2 * (1 - pu))
    n_ok, n_bad = (n_ok + 1, n_bad) if inside(C.A, a, 0) else (n_ok, n_bad + 1)
    n_ok, n_bad = (n_ok + 1, n_bad) if inside(C.ESTAR, mpmath.log(mpmath.cosh(um / 2)), 0) else (n_ok, n_bad + 1)
print("T1  DI against mpmath (80 digits): %d containments verified, %d violations; widest interval %.2e"
      % (n_ok, n_bad, float(Fr(maxw, 1 << R.DI.P))))
fails += n_bad

# control: damage the atanh series (drop the remainder and the last 30 terms) -- containment must fail somewhere
orig = R.DI._atanh


def damaged(z, nterms):
    one = 1 << R.DI.P
    z2 = z * z
    term, total = z, z
    for i in range(1, max(2, nterms - 30)):
        term = term * z2
        total = total + term / R.DI(one * (2 * i + 1), one * (2 * i + 1))
    return total


R.DI._atanh = staticmethod(damaged)
R.DI._LN2 = None
c_bad = 0
for _ in range(200):
    q = Fr(rng.randrange(1, 10 ** 12), rng.randrange(1, 10 ** 12))
    if not inside(R.DI.of(q).log(), mpmath.log(frac_mp(q)), 0):
        c_bad += 1
R.DI._atanh = staticmethod(orig)
R.DI._LN2 = None
print("T1  control (series truncated 30 terms early, no remainder): %d of 200 containments fail  [must be > 0]" % c_bad)
if c_bad == 0:
    fails += 1

# ------------------------------------------------------------------------------------------------------------ T2
n_cmp = n_bad = 0
for trial in range(300):
    n = rng.randrange(1, 40)
    c = Fr(rng.randrange(1, 1000), 1000)
    lines = []
    for _ in range(n):
        al = Fr(rng.randrange(-3, 60), rng.randrange(1, 12))
        be = Fr(rng.randrange(0, 40), rng.randrange(1, 60))
        lines.append((al, be))
    if trial % 5 == 0:                                   # degenerate: several lines through one point, equal slopes
        x0 = c / 3
        lines += [(Fr(k), Fr(k) * x0) for k in range(1, 6)] + [(Fr(2), Fr(2) * x0 + Fr(1, 7))]
    V = R.PL(lines, c)
    pts = [Fr(rng.randrange(0, 10 ** 6), 10 ** 6) * c for _ in range(30)] + [v[0] for v in V.vertices()] + [Fr(0), c]
    for B in pts:
        brute = max([Fr(0)] + [al * B - be for al, be in lines])
        n_cmp += 1
        if V.val(B) != brute or V.val_brute(B) != brute:
            n_bad += 1
    # M(g): against brute force over all pairwise crossings is expensive; compare with a fine rational grid from below
    g = Fr(rng.randrange(0, 300), 100)
    m = V.M(g)
    grid_max = max(B - g * max([Fr(0)] + [al * B - be for al, be in lines]) for B in [c * Fr(i, 200) for i in range(201)])
    n_cmp += 1
    if grid_max > m:
        n_bad += 1
print("T2  upper hull against brute force: %d exact comparisons, %d violations" % (n_cmp, n_bad))
fails += n_bad

# control: a hull that never pops (keeps dominated lines) must disagree with brute force
orig_hull = R.upper_hull


def damaged_hull(lines, c):
    c = Fr(c)
    st = [(Fr(0), Fr(0), Fr(0))]
    for al, be in sorted(set((Fr(a_), Fr(b_)) for a_, b_ in lines if a_ > 0)):
        a0, b0, x0 = st[-1]
        if al == a0:
            continue
        x = (be - b0) / (al - a0)
        if x0 < x < c:
            st.append((al, be, x))
    return st


R.upper_hull = damaged_hull
c_bad = 0
for trial in range(100):
    n = rng.randrange(2, 30)
    c = Fr(rng.randrange(1, 1000), 1000)
    lines = [(Fr(rng.randrange(1, 60), rng.randrange(1, 12)), Fr(rng.randrange(0, 40), rng.randrange(1, 60))) for _ in range(n)]
    V = R.PL(lines, c)
    for B in [Fr(rng.randrange(0, 10 ** 6), 10 ** 6) * c for _ in range(20)]:
        if V.val(B) != max([Fr(0)] + [al * B - be for al, be in lines]):
            c_bad += 1
R.upper_hull = orig_hull
print("T2  control (hull without popping): %d of 2000 comparisons fail  [must be > 0]" % c_bad)
if c_bad == 0:
    fails += 1

# ------------------------------------------------------------------------------------------------------------ T3
n_cmp = n_bad = c_bad = 0
for trial in range(200):
    n = rng.randrange(1, 25)
    c = Fr(rng.randrange(500, 1000), 1000)
    abar = Fr(rng.randrange(100, 900), 1000)
    lines = [(Fr(rng.randrange(1, 60), rng.randrange(1, 12)), Fr(rng.randrange(0, 40), rng.randrange(1, 60))) for _ in range(n)]
    V = R.PL(lines, c)
    t = R.top_exact(V, abar)
    n_cmp += 1
    if t == V.c:
        if not (V.c + abar * V.val_brute(V.c) < abar or V.c + abar * V.val_brute(V.c) == abar):
            n_bad += 1
    else:
        if t + abar * V.val_brute(t) != abar or not (0 < t < V.c):
            n_bad += 1
        t2 = t - Fr(1, 2 ** 100)                         # control: just below the root (S1) must fail
        if not (t2 + abar * V.val_brute(t2) < abar):
            pass
        else:
            c_bad += 1
print("T3  top_exact: %d cases, %d violations; control (top lowered by 2^-100): (S1) fails in %d cases  [must be > 0]" % (n_cmp, n_bad, c_bad))
fails += n_bad + (1 if c_bad == 0 else 0)

# ------------------------------------------------------------------------------------------------------------ T4
mp.dps = 40
worst = {}
for u in ("0.5", "1", "2"):
    P = R.CubeMP(u, dps=40)
    w = mpmath.mpf(0)
    for _ in range(25):
        B = mpmath.mpf(rng.random()) * P.a * 0.95
        s = mpmath.mpf(rng.random()) * 0.9
        if B >= (1 - s) * P.a * 0.98:
            continue
        s1, s2 = P.Sigma(B, s), P.Sigma_direct(B, s)
        w = max(w, abs(s1 - s2) / (1 + abs(s1)))
    idn = max(abs(P.theta(P.h) - P.h), abs(P.J(P.L) - P.h), abs(P.Jp(P.L)))
    for _ in range(10):
        e = mpmath.mpf(rng.random()) * P.estar * 0.999
        idn = max(idn, abs(P.theta(e + P.theta_hint(e)) - P.theta_hint(e)))
        r = P.pu + (P.half - P.pu) * mpmath.mpf(rng.random())
        idn = max(idn, abs(P.e_of(r) - (P.th_of(r) + P.u * r - P.lam1)))
    worst[u] = (w, idn)
    print("T4  u = %s: a = %s  h = %s  L = %s  eps* = %s  c_*^2 = %s" % (u, mpmath.nstr(P.a, 20), mpmath.nstr(P.h, 20), mpmath.nstr(P.L, 15), mpmath.nstr(P.estar, 15), mpmath.nstr(P.cs2, 12)))
    print("    max |Sigma(J) - Sigma(direct)|/(1+Sigma) = %s;  max defect of theta(h)=h, J(L)=h, J'(L)=0, (11.18.1), shift identity = %s"
          % (mpmath.nstr(w, 3), mpmath.nstr(idn, 3)))
    if w > mpmath.mpf(10) ** -20 or idn > mpmath.mpf(10) ** -30:
        fails += 1
# control: a wrong Lambda (slope u + 1/100 inside J) must break the agreement
P = R.CubeMP("1", dps=40)
origJ = P.J
P.J = lambda t: P.Lam(t * (P.u + mpmath.mpf(1) / 100)) - t * P.lam1
w = mpmath.mpf(0)
for _ in range(10):
    B = mpmath.mpf(rng.random()) * P.a * 0.5
    s = mpmath.mpf(rng.random()) * 0.4
    w = max(w, abs(P.Sigma(B, s) - P.Sigma_direct(B, s)))
print("T4  control (wrong Lambda in J): max |Sigma(J) - Sigma(direct)| = %s  [must be large]" % mpmath.nstr(w, 3))
if w < mpmath.mpf(10) ** -6:
    fails += 1

print("SELFTEST: %s (%d failures)" % ("ALL PASS" if fails == 0 else "FAILED", fails))
R.finish("r29_i1_selftest")
sys.exit(0 if fails == 0 else 1)
