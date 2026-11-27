#!/usr/bin/env python3
"""r29_i1_mytops.py u J K [mpJ]  --  my own certified tops (multi-rate sequence of Proposition A13), from the statement.

Differences from z6_certified_tops.py (deliberate, so that the two computations share no numerical choice):
  * all lines, tops, hulls, the cap and every comparison are exact rationals (Fractions); stored lines are rounded
    one-sidedly to multiples of 2^-128 (slope down, beta up), the top UP, the cap slope UP;
  * the pairs (e', th) come from my own integer interval arithmetic (r29lib.DI, 256 bits), not from mpmath `iv`;
    they are multiples of 2^-96 (finer than doubles);
  * rates: the tangency point rho = 1/(1 + exp(t'u)) of the slope map at the sample point, t' from J (closed form),
    rounded to 40 bits -- not a golden-section search;
  * sample points: c (k/K)^0.8 and a geometric family towards the top -- not a uniform grid;
  * every step is then checked by an independent exact checker (r29lib.check_step) that sees only the two curves
    and the certificates, and every pair is cross-checked against plain multiprecision (mpmath mp, 50 digits).
Output: my tops c_j (rigorous upper bounds of tau_j GIVEN Lemma A1 / Proposition A8, like theirs), compared with
  * the semi-analytic envelope tops b_j (r29env.EnvSA; multiprecision for j <= mpJ, doubles beyond): c_j >= b_j must
    hold (Corollary A4), and the difference is the quality of the certified sequence;
  * their committed certified tops (out_z6_certified_u*.txt, read only), which must also be >= b_j.
Controls (each must be REJECTED by the checker): pairs rounded down; a slope rounded up; the cap slope lowered;
the top lowered; abar replaced by a lower bound of a.
"""
import math
import os
import sys
from fractions import Fraction as Fr

import r29lib as R
import r29env as E

R.cap_memory()
import mpmath  # noqa: E402

u_str = sys.argv[1] if len(sys.argv) > 1 else "1"
JMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 6
K = int(sys.argv[3]) if len(sys.argv) > 3 else 200
MPJ = int(sys.argv[4]) if len(sys.argv) > 4 else min(JMAX, 6)
EXPORT = "/tmp/claude-0/-home-user-MetricChain/625a5006-6913-5629-a308-2f7fb488fbbb/scratchpad/thy_ro_07cde81/experiments/workstreams/Z"

ufr = Fr(u_str)
cube = R.CubeDI(ufr)
abar = cube.abar(96)
alow = cube.alow(96)


def samples(c):
    pts = [c * Fr(int(round((k / K) ** 0.8 * 2 ** 30)), 2 ** 30) for k in range(1, K)]
    pts += [c * (1 - Fr(1, 2 ** 40) * int(round(2 ** 40 * 2.0 ** (-i / 3.0)))) for i in range(6, 6 + K // 3)]
    return sorted(set(p for p in pts if 0 < p < c))


def fr2mp(q):
    return mpmath.mpf(q.numerator) / mpmath.mpf(q.denominator)


print("# my certified tops, cube pair, u = %s; K = %d sample points (+%d near the top); levels up to %d" % (u_str, K, K // 3, JMAX))
print("# a in [%s, %s]; abar - a <= %.2e" % (mpmath.nstr(fr2mp(alow), 25), mpmath.nstr(fr2mp(abar), 25), float(abar - alow)))

# ---- the sequence, each step checked
V = R.PL([], abar)                       # V_0 = 0 on [0, abar]
seq = [V]
allcerts = [None]
viol_total = 0
npairs = 0
mpP = R.CubeMP(ufr, dps=50)
pair_viol = 0
for j in range(1, JMAX + 1):
    Vn, certs = R.build_step(V, cube, abar, samples)
    bad = R.check_step(V, Vn, certs, cube, abar)
    viol_total += len(bad)
    # cross-check of the pairs against plain multiprecision (independent of DI)
    for ln, ct in certs.items():
        cts = [ct] if ct[0] == "img" else [w[1] for w in (ct[1], ct[2]) if w[1] is not None]
        for c_ in cts:
            _, parent, rho, e, th = c_
            r = fr2mp(rho)
            npairs += 1
            if not (fr2mp(e) >= mpP.e_of(r) and fr2mp(th) >= mpP.th_of(r)):
                pair_viol += 1
    seq.append(Vn)
    allcerts.append(certs)
    V = Vn
    print("   level %2d built: top c_%d = %.15f, %d hull lines, checker violations: %d" % (j, j, float(Vn.c), len(Vn.lines()), len(bad)), flush=True)
print("# independent exact checker: %d violations over %d steps;  pairs cross-checked in multiprecision: %d, violations %d"
      % (viol_total, JMAX, npairs, pair_viol))

# ---- semi-analytic envelope tops
envmp = E.EnvSA(R.CubeMP(ufr, dps=30), MPJ) if MPJ >= 1 else None
envf = E.EnvSA(E.CubeF(float(ufr)), JMAX)
mpmath.mp.dps = 30

# ---- their committed tops (read only)
theirs = {}
name = {"1": "out_z6_certified_u1.txt", "2": "out_z6_certified_u2.txt", "1/2": "out_z6_certified_u0.5.txt"}.get(u_str)
if name and os.path.exists(os.path.join(EXPORT, name)):
    for line in open(os.path.join(EXPORT, name)):
        if line.startswith("#") or "|" not in line:
            continue
        f = [x.strip() for x in line.split("|")]
        try:
            theirs[int(f[0])] = (float(f[1]), float(f[2]))
        except ValueError:
            pass

Pf = E.CubeF(float(ufr))
h = Pf.h
print("# columns: j | my certified c_j | c_j/a (upper) | b_j semi-analytic (mp to j=%d, then doubles) | (c_j - b_j)/(b_j - h) | their committed c_j | (theirs - b_j)/(b_j - h) | mine >= b_j | theirs >= b_j" % MPJ)
ok_mine = ok_theirs = True
for j in range(1, JMAX + 1):
    cj = seq[j].c
    use_mp = envmp is not None and j <= MPJ
    bj = envmp.b[j] if use_mp else mpmath.mpf(envf.b[j])
    tol = mpmath.mpf(0) if use_mp else mpmath.mpf(10) ** -12       # the doubles of EnvSA are good to about 1e-13
    bjf = float(bj)
    d_mine = fr2mp(cj) - bj
    m_ok = bool(d_mine >= -tol)
    ok_mine = ok_mine and m_ok
    ratio_up = cj / alow
    th_c = theirs.get(j)
    if th_c:
        d_th = mpmath.mpf(th_c[0]) - bj
        t_ok = bool(d_th >= -tol - mpmath.mpf(5) * mpmath.mpf(10) ** -13)   # their print has 12 decimals (rounded to nearest)
        ok_theirs = ok_theirs and t_ok
        ts = "%.12f | %+.3e | " % (th_c[0], float(d_th) / (bjf - h))
    else:
        t_ok = None
        ts = "- | - | "
    print("%4d | %.15f | %.12f | %.15f | %+.3e | %s%s | %s" % (j, float(cj), float(ratio_up) + 5e-13, bjf, float(d_mine) / (bjf - h), ts, m_ok, t_ok))
print("# all my tops >= semi-analytic envelope tops: %s;   all their committed tops >= semi-analytic envelope tops: %s" % (ok_mine, ok_theirs))

# ---- certified majorants at three rates, as their script prints them
gs = [Fr(h).limit_denominator(10 ** 12) * Fr(1, 10), Fr(h).limit_denominator(10 ** 12) * Fr(1, 2), Fr(h).limit_denominator(10 ** 12)]
print("# certified M_j(g) = max_B (B - V_j(B) g) at g = 0.1h, 0.5h, h (exact maxima over the vertices, mine):")
for j in range(1, min(JMAX, 6) + 1):
    print("   j = %d: %s" % (j, "  ".join("%.9f" % (float(seq[j].M(g)) + 5e-10) for g in gs)))

# ---- controls: each must be rejected by the checker
print("# controls (each must be REJECTED by the independent checker):")
V1, V2, c2s = seq[1], seq[2], allcerts[2]
nrej = 0
# (c1) pairs rounded down by one unit of 2^-96 in e'
bad_certs = {}
for ln, ct in c2s.items():
    if ct[0] == "img":
        _, parent, rho, e, th = ct
        bad_certs[ln] = ("img", parent, rho, e - Fr(1, 2 ** 60), th)
    else:
        bad_certs[ln] = ct
r1 = R.check_step(V1, V2, bad_certs, cube, abar)
print("   (c1) e' lowered by 2^-60 in every certificate: %d violations" % len(r1)); nrej += bool(r1)
# (c2) one slope raised by 2^-100
lines = V2.lines()
k = len(lines) // 2
ln = lines[k]
ln_bad = (ln[0] + Fr(1, 2 ** 100), ln[1])
V2b = R.PL([l for l in lines if l != ln] + [ln_bad], V2.c)
certs_b = dict(c2s)
certs_b[ln_bad] = c2s[ln]
r2 = R.check_step(V1, V2b, certs_b, cube, abar)
print("   (c2) one stored slope raised by 2^-100: %d violations" % len(r2)); nrej += bool(r2)
# (c3) the cap slope lowered by 2^-90 (the cap line is then above the hull near the tangent vertex)
cap = [l for l in lines if c2s[l][0] == "cap"]
if cap:
    m, bL = cap[0]
    m2 = m - Fr(1, 2 ** 90)
    cap_bad = (m2, m2 * V2.c - 1)
    V2c = R.PL([l for l in lines if l != cap[0]] + [cap_bad], V2.c)
    certs_c = dict(c2s)
    certs_c[cap_bad] = c2s[cap[0]]
    r3 = R.check_step(V1, V2c, certs_c, cube, abar)
    print("   (c3) cap slope lowered by 2^-90: %d violations" % len(r3)); nrej += bool(r3)
else:
    print("   (c3) no cap line at level 2 (unexpected)")
# (c4) the top lowered by 2^-100
V2d = R.PL(lines, V2.c - Fr(1, 2 ** 100))
r4 = R.check_step(V1, V2d, c2s, cube, abar)
print("   (c4) top lowered by 2^-100: %d violations" % len(r4)); nrej += bool(r4)
# (c5) abar replaced by a lower bound of a
r5 = R.check_step(V1, V2, c2s, cube, alow)
print("   (c5) abar := lower bound of a: %d violations" % len(r5)); nrej += bool(r5)
print("# controls rejected: %d of 5" % nrej)
print("MYTOPS: %s" % ("ALL CHECKS PASS" if (viol_total == 0 and pair_viol == 0 and ok_mine and nrej == 5) else "CHECK FAILED"))
R.finish("r29_i1_mytops u=%s J=%d K=%d" % (u_str, JMAX, K))
