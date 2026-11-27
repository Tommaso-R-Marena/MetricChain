#!/usr/bin/env python3
"""a6_02_verify_z6_output.py [u] [levels] [K]  --  an independent check of an OUTPUT of z6_certified_tops.py.

The coordinator's script is imported unchanged (its module-level code reads sys.argv; its main() is not called) and
its own `step` is run for a small instance.  Then every curve it produced is verified with code that shares nothing
with it: the referee's interval arithmetic on integers (a6exact.py; no mpmath intervals) and exact fractions.

For each level j -> j+1 (V = V_j on [0, c], V' = V_{j+1} on [0, c']):
 (T)  the top, exactly:  c' <= c  and  ( c' = c  or  c' + abar V(c') >= abar ),  abar >= a  (a enclosed independently);
 (F)  V' is a family, exactly:  slopes > 0, betas >= 0, V'(c') <= 1;  the stored lines are exactly the upper hull;
 (L)  every line (alpha, beta) of V' except the cap line:  a line l = (a0, b0) of V (or the zero line) and a RATIONAL
      pair (e0, th0) are exhibited with
            alpha B - beta  =  [B - th0 (1 - l(B))]/e0   identically,      and      th0 >= theta(e0)   PROVED
      by a rational witness rho in (0, 1/2] with  KL(rho || p_u) <= e0  and  KL(rho || 1/2) <= th0  (enclosures of the
      two divergences by the referee's own series for exp and log, 200 bits);
 (C)  the cap line (through (c', <= 1)) is in general NOT of that form (it is tangent to the hull of several such
      lines): it is verified to lie, on all of [0, c'], below the maximum of the zero line, of the lines certified in
      (L) and of lines of the referee's own making for the same step (own sample points, own rates, own rigorous pairs)
      -- an exact comparison at every vertex of that maximum;
 (M)  the script's M_upper(g) is the least double above the exact maximum over the vertices.
Negative controls: four mutations of the output, each of which must be rejected.

What this does and does not show: that THIS output is an admissible multi-rate sequence in the sense of Proposition
A13, by an independent verifier.  It is not a proof that the script is correct on every input.
"""
import math
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
JLEV = int(sys.argv[2]) if len(sys.argv) > 2 else 6
KS = int(sys.argv[3]) if len(sys.argv) > 3 else 300
CONTROLS = not (len(sys.argv) > 4 and sys.argv[4] == "nocontrols")      # the mutations may be skipped for a large instance

sys.path.insert(0, HERE)
import a6exact as X                                             # noqa: E402
import a6lib as L                                               # noqa: E402
from mpmath import mp, mpf                                      # noqa: E402  (non-interval, as a root finder only)

# ---- import the script under review, unchanged, for this instance
_argv = sys.argv
sys.argv = ["z6_certified_tops.py", u_str, str(JLEV), str(KS), "nocompare"]
sys.path.insert(0, os.path.dirname(HERE))
import z6_certified_tops as z6                                  # noqa: E402
sys.argv = _argv

t00 = time.time()
mp.dps = 60
PX = X.CubeX(u_str)
Pf = L.Cube(float(u_str))
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)
    return ok


print("# independent verification of an output of z6_certified_tops.py: cube, u = %s, %d levels, K = %d sample points" % (u_str, JLEV, KS))

# ---- run the coordinator's construction
curves = [(list(map(float, [])), list(map(float, [])), float(z6.ABAR))]
V = z6.Curve([], [], z6.ABAR)
for j in range(1, JLEV + 1):
    V = z6.step(V)
    curves.append(([float(x) for x in V.al], [float(x) for x in V.be], float(V.c)))
    last_curve_obj = V
print("# the script's tops c_j:", ", ".join("%.15g" % c[2] for c in curves[1:]))
print("# lines per level:", ", ".join(str(len(c[0])) for c in curves[1:]))

ABAR = float(z6.ABAR)
print("(0) abar")
check("abar = %.17g >= a (referee's enclosure: a <= %.17g; abar - a <= %.2e)" % (ABAR, float(PX.a_hi), float(Fr(ABAR) - PX.a_lo)), Fr(ABAR) >= PX.a_hi)
check("the script's ALOW = %.17g <= a" % float(z6.ALOW), Fr(float(z6.ALOW)) <= PX.a_lo)


# ---- witnesses (mpmath as a root finder; the proof is PX.valid_pair)
def mp_kl(r, p):
    return r * mp.log(r / p) + (1 - r) * mp.log((1 - r) / (1 - p))


PU_MP = 1 / (1 + mp.exp(mpf(PX.u.numerator) / mpf(PX.u.denominator)))
A_MP = mp_kl(PU_MP, mpf(1) / 2)
EPS_MP = mp_kl(mpf(1) / 2, PU_MP)


def mp_root(f, df, x0, lo, hi):
    x = mpf(x0)
    for _ in range(60):
        fx = f(x)
        d = df(x)
        if d == 0:
            break
        xn = x - fx / d
        if not (lo < xn < hi):
            xn = (x + (lo if fx * d > 0 else hi)) / 2
        if abs(xn - x) < mpf(10) ** (-52):
            x = xn
            break
        x = xn
    return x


def witness(e0, th0):
    """a rational rho in (0, 1/2] that should satisfy KL(rho||p_u) <= e0 and KL(rho||1/2) <= th0 (or None)"""
    e, th = mpf(e0.numerator) / mpf(e0.denominator), mpf(th0.numerator) / mpf(th0.denominator)
    half = mpf(1) / 2
    if e >= EPS_MP:
        rb = half
    else:                                                       # largest rho with KL(rho || p_u) <= e
        r0 = float(Pf.rho_of_t(Pf.t_of_e(np.array([float(e)]))[0]))
        r0 = min(max(r0, float(PU_MP) * (1 + 1e-12)), 0.5 * (1 - 1e-12))
        rb = mp_root(lambda r: mp_kl(r, PU_MP) - e, lambda r: mp.log(r / (1 - r)) - mp.log(PU_MP / (1 - PU_MP)), r0, PU_MP, half)
    if th >= mp.log(2):
        ra = mpf(0)
    elif th <= 0:
        ra = half
    else:                                                       # smallest rho with KL(rho || 1/2) <= th
        lo_, hi_ = 1e-300, 0.5
        for _ in range(200):
            mid = 0.5 * (lo_ + hi_)
            if math.log(2) + mid * math.log(mid) + (1 - mid) * math.log1p(-mid) > float(th):
                lo_ = mid
            else:
                hi_ = mid
        r0 = min(max(hi_, 1e-290), 0.5 * (1 - 1e-12))
        ra = mp_root(lambda r: mp_kl(r, half) - th, lambda r: mp.log(r / (1 - r)), r0, mpf(0), half)
    if ra > rb:
        return None, float(rb - ra)
    mid = (ra + rb) / 2
    if mid <= 0:
        mid = rb / 2
    rho = Fr(int(mp.floor(mid * mpf(2) ** 190)), 1 << 190)
    if rho <= 0:
        return None, float(rb - ra)
    return min(rho, Fr(1, 2)), float(rb - ra)


def certify_line(al, be, prev_al, prev_be):
    """find a line of the previous level (index -1: the zero line) and a proved-valid rational pair that reproduce
    the line (al, be) exactly.  Returns (index, e0, th0, rho, window) or None."""
    a0 = np.concatenate([[0.0], np.asarray(prev_al, float)])
    b0 = np.concatenate([[0.0], np.asarray(prev_be, float)])
    den = al - be * a0 / (1.0 + b0)
    with np.errstate(divide="ignore", invalid="ignore"):
        e0 = np.where(den > 0, 1.0 / den, np.nan)
        th0 = be * e0 / (1.0 + b0)
        margin = th0 - Pf.theta(np.nan_to_num(e0, nan=1.0))
    margin = np.where(np.isfinite(e0) & (th0 >= 0), margin, -np.inf)
    order = np.argsort(-margin)
    for k in order[:6]:
        if not margin[k] > -1e-7:
            break
        A0, B0 = Fr(float(a0[k])), Fr(float(b0[k]))
        d = Fr(al) - Fr(be) * A0 / (1 + B0)
        if d <= 0:
            continue
        E0 = 1 / d
        TH0 = Fr(be) * E0 / (1 + B0)
        # the identity alpha = (1 + th0 a0)/e0, beta = th0 (1 + b0)/e0, exactly
        assert (1 + TH0 * A0) / E0 == Fr(al) and TH0 * (1 + B0) / E0 == Fr(be)
        rho, window = witness(E0, TH0)
        if PX.valid_pair(E0, TH0, rho):
            return int(k) - 1, E0, TH0, rho, window
    return None


def own_lines(prev, c, Bs):
    """the referee's own certified lines for the step from prev = (al, be, c_prev), at the sample points Bs"""
    Vp = X.XCurve(list(zip(prev[0], prev[1])), prev[2])
    out = []
    for B in Bs:
        B = float(B)
        i = Vp.active(B)
        a0, b0 = (Vp.al[i], Vp.be[i]) if i >= 0 else (0.0, 0.0)
        s = max(0.0, a0 * B - b0)
        if not (s < 1.0 and B < (1.0 - s) * Pf.a * (1 - 1e-12)):
            continue
        t = float(Pf.sigma_t(np.array([B]), np.array([s]))[0])
        rho = float(Pf.rho_of_t(t))
        if not (0.0 < rho <= 0.5):
            continue
        E, TH = PX.pair(rho)
        al = X.fl_dn((1 + TH * Fr(a0)) / E)
        be = X.fl_up(TH * (1 + Fr(b0)) / E)
        if al > 0:
            out.append((al, be))
    return out


def verify_level(prev, cur, label, quiet=False, examples=0):
    """all checks for one step; returns (ok, stats)"""
    (pal, pbe, pc), (al, be, c) = prev, cur
    okall = True
    say = (lambda *a, **k: None) if quiet else print
    Vp = X.XCurve(list(zip(pal, pbe)), pc)
    C, CP, A = Fr(c), Fr(pc), Fr(ABAR)
    # (T) the top
    top_ok = (C <= CP) and (C == CP or C + A * Vp.val_exact(c) >= A)
    okall &= top_ok
    # (F) family
    lines = list(zip(al, be))
    vc = max([Fr(0)] + [Fr(a_) * C - Fr(b_) for a_, b_ in lines])
    fam_ok = all(a_ > 0 for a_ in al) and all(b_ >= 0 for b_ in be) and vc <= 1 and c > 0
    hull, _ = X.exact_hull(lines, c)
    hull_ok = (hull == lines)
    okall &= fam_ok and hull_ok
    # (L) the lines
    certs, unmatched = [], []
    zero_gen = 0
    minwin = math.inf
    for k, (a_, b_) in enumerate(lines):
        r = certify_line(a_, b_, pal, pbe)
        if r is None:
            unmatched.append(k)
        else:
            certs.append((k, r))
            zero_gen += (r[0] == -1)
            if r[1] < PX.eps_hi:
                minwin = min(minwin, r[4])
    # (C) the cap line(s)
    cap_ok = True
    cap_info = ""
    if unmatched:
        cert_lines = [lines[k] for k, _ in certs]
        for k in unmatched:
            m, bL = lines[k]
            # where the candidate cap line becomes active
            others = X.XCurve([l for i, l in enumerate(lines) if i != k], c)
            xt = None
            for (x, v) in others.vertices():
                if Fr(m) * x - Fr(bL) >= v and x > 0:
                    xt = x
                    break
            xt = float(xt) if xt is not None else 0.0
            w = c - xt
            Bs = np.unique(np.concatenate([
                np.linspace(max(0.0, xt - 0.02 * w), min(c, xt + 0.05 * w), 700),
                np.linspace(xt, c, 900)[:-1],
                c * (1.0 - np.geomspace(1e-11, 0.3, 300))]))
            Bs = Bs[(Bs > 0) & (Bs < c)]
            mine = own_lines(prev, c, Bs)
            G = X.XCurve(cert_lines + mine, c)
            worst = None
            for (x, v) in G.vertices():
                slack = v - (Fr(m) * x - Fr(bL))
                if worst is None or slack < worst[0]:
                    worst = (slack, x)
            this_ok = worst[0] >= 0
            cap_ok &= this_ok
            cap_info += " line %d (slope %.6g, value at c' %.17g): active from B = %.6g; least slack of [max(0, certified, own) - line] over %d vertices: %.2e at B = %.6g (%d own lines);" % (
                k, m, float(Fr(m) * C - Fr(bL)), xt, len(G.vertices()), float(worst[0]), float(worst[1]), len(mine))
    okall &= cap_ok and (len(unmatched) <= 1)
    say("%s: c' = %.15g (c = %.15g, %s) | %d lines: %d certified by a single (line, pair) [%d from the zero line], %d not of that form"
        % (label, c, pc, "c' = c" if C == CP else "c' + abar V(c') >= abar exactly", len(lines), len(certs), zero_gen, len(unmatched)))
    if not quiet:
        check("%s (T) top" % label, top_ok)
        check("%s (F) family: slopes > 0, betas >= 0, V'(c') = %.17g <= 1; stored lines = exact upper hull" % (label, float(vc)), fam_ok and hull_ok)
        check("%s (L) every other line is exactly [B - th0 (1 - l(B))]/e0 with th0 >= theta(e0) proved" % label, len(certs) + len(unmatched) == len(lines) and len(unmatched) <= 1,
              "| narrowest witness window rho_b - rho_a: %.1e" % minwin)
        if unmatched:
            check("%s (C) the cap line is below max(0, certified lines, referee's own lines) on [0, c']" % label, cap_ok, "|" + cap_info)
        for k, r in certs[:examples]:
            i, E0, TH0, rho, win = r
            l0 = (pal[i], pbe[i]) if i >= 0 else (0.0, 0.0)
            print("       e.g. line (alpha, beta) = (%.17g, %.17g)  <-  l = (%.17g, %.17g)%s,  e0 = %.17g, th0 = %.17g, witness rho = %.20g"
                  % (lines[k][0], lines[k][1], l0[0], l0[1], " [zero line]" if i < 0 else "", float(E0), float(TH0), float(rho)))
    return okall, dict(certified=len(certs), unmatched=len(unmatched), top_ok=top_ok, fam_ok=fam_ok, hull_ok=hull_ok, cap_ok=cap_ok)


print("(1) the levels")
for j in range(1, JLEV + 1):
    verify_level(curves[j - 1], curves[j], "level %d" % j, examples=1 if j <= 3 else 0)
    print("       [%.0f s]" % (time.time() - t00), flush=True)

print("(2) the certified majorant: the script's M_upper(g) against the exact maximum over the vertices")
okM = True
al, be, c = curves[JLEV]
Vx = X.XCurve(list(zip(al, be)), c)
for g in (0.0, 0.1 * Pf.h, 0.5 * Pf.h, Pf.h, 0.5 * Pf.eps, 3.0):
    mine = X.fl_up(Vx.M_exact(g))
    theirs = last_curve_obj.M_upper(g)
    okM &= (mine == theirs)
    print("       g = %.12g: script %.17g, referee %.17g" % (g, theirs, mine))
check("M_upper is the least double >= the exact maximum (level %d, six rates)" % JLEV, okM)

if not CONTROLS:
    print()
    print("(3) negative controls: skipped for this instance (run without the fourth argument)")
    print()
    print("time %.0f s" % (time.time() - t00))
    print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
    sys.exit(0)
print("(3) negative controls (each mutation of the output must be rejected)")
jm = min(3, JLEV)
prev, cur = curves[jm - 1], curves[jm]
base_ok, st = verify_level(prev, cur, "control base", quiet=True)
check("unmutated level %d accepted" % jm, base_ok)
# m1: one line raised by a relative 1e-9 (beta lowered)
al, be, c = [list(cur[0]), list(cur[1]), cur[2]]
k = len(al) // 3
be1 = list(be)
be1[k] = be[k] * (1 - 1e-9)
ok1, st1 = verify_level(prev, (al, be1, c), "m1", quiet=True)
check("m1: a line raised by 1e-9 (relative, in beta) is rejected", not ok1, "| %s" % st1)
# m2: the top lowered by a relative 1e-9
c2 = cur[2] * (1 - 1e-9)
ok2, st2 = verify_level(prev, (al, be, c2), "m2", quiet=True)
check("m2: the top lowered by 1e-9 (relative) is rejected", not ok2, "| %s" % st2)
# m3: the cap line made flatter through (c, 1) by 1e-3 (it then exceeds the image near its tangency point)
vals = [Fr(a_) * Fr(c) - Fr(b_) for a_, b_ in zip(al, be)]
kc = max(range(len(al)), key=lambda i: al[i])
if float(vals[kc]) > 1 - 1e-12:
    al3, be3 = list(al), list(be)
    al3[kc] = al[kc] * (1 - 1e-3)
    be3[kc] = al3[kc] * c - float(vals[kc])
    ok3, st3 = verify_level(prev, (al3, be3, c), "m3", quiet=True)
    check("m3: the cap line made flatter by 1e-3 through (c', 1) is rejected", not ok3, "| %s" % st3)
else:
    print("  (m3 skipped: level %d has no cap line)" % jm)
# m4: a slope raised by 1e-9
al4 = list(al)
k4 = len(al) // 2
al4[k4] = al[k4] * (1 + 1e-9)
ok4, st4 = verify_level(prev, (al4, be, c), "m4", quiet=True)
check("m4: a slope raised by 1e-9 (relative) is rejected", not ok4, "| %s" % st4)
# m5: abar below a
check("m5: an 'abar' below a is rejected by check (0)", not (Fr(float(z6.ALOW)) * (1 - Fr(1, 10 ** 9)) >= PX.a_hi))

print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
