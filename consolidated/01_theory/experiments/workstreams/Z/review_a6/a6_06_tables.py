#!/usr/bin/env python3
"""a6_06_tables.py  --  the tables and quoted numbers of A6a/A6b and of Theorem 11.58e(f) against the stored outputs
of the coordinator's scripts, and what the PRINTED decimals of z6_certified_tops.py certify.

 (1) the table of A6b (addendum) and the table of Theorem 11.58e(f) (theory report) against out_z6_certified_*.txt;
 (2) the quoted figures of A6b: h/a at three slopes; "3e-8 to 2e-3 of their distance to h"; "1.0009 at 400 levels";
 (3) a re-run of the coordinator's script (imported unchanged; u = 1, K = 3000, 8 levels): the stored lines are
     reproduced; the certified numbers are DOUBLES and the script prints them rounded to nearest -- how many of the
     printed decimals lie below the double they stand for;
 (4) quoted numbers of the paragraph "Where the loss is" (A6a) against out_z7_exactness_u1.txt and the referee's curves.
"""
import math
import os
import re
import sys
import time
from decimal import Decimal
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ZDIR = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
import a6lib as L                                               # noqa: E402
import a6exact as X                                             # noqa: E402

t00 = time.time()
FAIL = []


def check(name, ok, info=""):
    print("  [%s] %s %s" % ("ok" if ok else "FAIL", name, info))
    if not ok:
        FAIL.append(name)


def stored(fname):
    rows = {}
    for line in open(os.path.join(ZDIR, fname)):
        m = re.match(r"\s*(\d+) \| ([0-9.]+) \| ([0-9.]+) \|\s*(\d+) \| (\S+) \| \s*(\S+) \| ([0-9.]+)", line)
        if m:
            rows[int(m.group(1))] = dict(c=m.group(2), ratio=m.group(3), lines=int(m.group(4)), b=m.group(5), rel=m.group(6), sc=m.group(7), raw=line.rstrip("\n"))
    return rows


S1, S2, S05, S400 = stored("out_z6_certified_u1.txt"), stored("out_z6_certified_u2.txt"), stored("out_z6_certified_u0.5.txt"), stored("out_z6_certified_u1_J400.txt")

print("(1) the tables")
A6b = {
    "1": {2: "0.500410024", 3: "0.363300653", 4: "0.312791462", 5: "0.291376787", 6: "0.281323250", 8: "0.272750695", 10: "0.269065250",
          20: "0.264243938", 40: "0.263047017", 80: "0.262747193", 200: "0.262663126", 400: "0.262651110"},
    "2": {2: "0.505615446", 3: "0.383347314", 4: "0.341033400", 5: "0.323697863", 6: "0.315235252", 8: "0.307181543", 10: "0.303467854",
          20: "0.298465858", 40: "0.297189804"},
    "0.5": {2: "0.500026741", 3: "0.358645034", 4: "0.305680047", 5: "0.282897289", 6: "0.272167511", 8: "0.263247512", 10: "0.259553884",
            20: "0.254793046", 40: "0.253620656"}}
src = {"1": S1, "2": S2, "0.5": S05}
bad = []
for u_, tab in A6b.items():
    for j, v in tab.items():
        s = src[u_].get(j) or (S400.get(j) if u_ == "1" else None)
        if u_ == "1" and j in (200, 400):
            s = S400.get(j)
        if s is None or s["ratio"] != v:
            bad.append((u_, j, v, s["ratio"] if s else None))
check("addendum, table of A6b: all 30 entries are the printed ratios of the stored outputs (u = 1: j <= 80 from the K = 3000 run, 200 and 400 from the K = 4000 run)", not bad, "| %s" % bad if bad else "")
THY = {
    "1": {2: "0.500411", 3: "0.363301", 4: "0.312792", 5: "0.291377", 6: "0.281324", 8: "0.272751", 10: "0.269066", 20: "0.264244", 40: "0.263048",
          80: "0.262748", 400: "0.262652"},
    "2": {2: "0.505616", 3: "0.383348", 4: "0.341034", 5: "0.323698", 6: "0.315236", 8: "0.307182", 10: "0.303468", 20: "0.298466", 40: "0.297190"},
    "0.5": {2: "0.500027", 3: "0.358646", 4: "0.305681", 5: "0.282898", 6: "0.272168", 8: "0.263248", 10: "0.259554", 20: "0.254794", 40: "0.253621"}}
bad = []
for u_, tab in THY.items():
    for j, v in tab.items():
        s = S400.get(j) if (u_ == "1" and j == 400) else src[u_].get(j)
        # "rounded up in the last digit": the 6-digit value must be >= the printed 9-digit ratio + 5e-10 (the printed
        # ratio is itself a rounding to nearest of the certified double), and less than 1e-6 above it
        d = Decimal(v) - Decimal(s["ratio"])
        if not (Decimal("5e-10") <= d < Decimal("1e-6")):
            bad.append((u_, j, v, s["ratio"]))
check("theory report, table of Theorem 11.58e(f): all 29 entries are the stored ratios rounded UP to six digits (so they are valid whatever the last-digit rounding of the script's print)", not bad, "| %s" % bad if bad else "")

print("(2) quoted figures of A6b")
for u_, q in (("1", "0.262647098"), ("2", "0.296757"), ("0.5", "0.253231")):
    P = L.Cube(float(u_))
    check("h/a at u = %s: %.9f (addendum: %s)" % (u_, P.h / P.a, q), abs(P.h / P.a - float(q)) < 0.6 * 10 ** (-(len(q) - 2)))
rels = {}
for nm, S in (("u = 1", S1), ("u = 2", S2), ("u = 1/2", S05)):
    vals = [(float(r["rel"]), j) for j, r in S.items() if j >= 2 and r["rel"] not in ("-",)]
    rels[nm] = (min(vals), max(vals))
    print("     %s: (c_j - b_j)/(b_j - h), b_j the coordinator's floating-point envelope top: least %.2e (j = %d), largest %.2e (j = %d)" % (nm, min(vals)[0], min(vals)[1], max(vals)[0], max(vals)[1]))
allmin = min(v[0][0] for v in rels.values())
allmax = max(v[1][0] for v in rels.values())
check("'the certified tops exceed the floating-point envelope tops by 3e-8 to 2e-3 of their distance to h (the larger figure at 80 levels)'",
      1e-8 < allmin < 4e-8 and 1.5e-3 < allmax < 3e-3, "| over the three stored runs: %.1e to %.1e; the largest is at j = %d of u = 1 (%.2e), not at 80 (%.2e)" % (
          allmin, allmax, rels["u = 1"][1][1], rels["u = 1"][1][0], float(S1[80]["rel"])))
check("'at 400 levels j^2 (c_j - h)/c_*^2 = 1.0009'", abs(float(S400[400]["sc"]) - 1.0009) < 6e-5, "| stored: %s" % S400[400]["sc"])

print("(3) what the printed decimals certify: a re-run of the coordinator's script (u = 1, K = 3000, 8 levels)")
_argv = sys.argv
sys.argv = ["z6_certified_tops.py", "1", "8", "3000", "nocompare"]
sys.path.insert(0, ZDIR)
import z6_certified_tops as z6                                  # noqa: E402
sys.argv = _argv
V = z6.Curve([], [], z6.ABAR)
same = True
below_c = below_r = 0
print("       j   c_j as a double (exact decimal, 20 digits)   printed '%.12f'    printed below the double?    ratio double (17 digits)   printed '%.9f'   below?")
for j in range(1, 9):
    V = z6.step(V)
    cj = V.c
    ratio = math.nextafter(cj / z6.ALOW, math.inf)
    pc, pr = "%.12f" % cj, "%.9f" % ratio
    same &= (pc == S1[j]["c"] and pr == S1[j]["ratio"] and len(V.al) == S1[j]["lines"])
    bc = Fr(pc) < Fr(cj)
    br = Fr(pr) < Fr(ratio)
    below_c += bc
    below_r += br
    print("     %3d   %.20f                    %s        %-5s                    %.17f        %s      %s" % (j, cj, pc, bc, ratio, pr, br))
check("the stored output (out_z6_certified_u1.txt) is reproduced for j = 1..8: same printed tops, ratios and numbers of lines", same)
check("the printed decimals are roundings to NEAREST of the certified doubles: %d of 8 printed tops and %d of 8 printed ratios are BELOW the double" % (below_c, below_r),
      True, "| a rigorous reading of a printed value adds one unit in its last place (5e-13 resp. 5e-10 suffices)")
PX = X.CubeX("1")
check("re-run: abar >= a by the referee's enclosure", Fr(float(z6.ABAR)) >= PX.a_hi)

print("(4) 'Where the loss is' (A6a), against out_z7_exactness_u1.txt and the referee's curves")
P = L.Cube(1.0)
z7 = {}
for line in open(os.path.join(ZDIR, "out_z7_exactness_u1.txt")):
    m = re.match(r"\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+\(([0-9.]+), ([0-9.]+)\)\s+([0-9.]+)\s+([+-][0-9.e+-]+)", line)
    if m:
        z7[float(m.group(1))] = dict(theta=float(m.group(2)), R=float(m.group(3)), phi=float(m.group(4)), bg=float(m.group(5)), M2=float(m.group(6)), d=float(m.group(7)))
lt, lc = L.lines_sequence(P, 3, 20000, keep={2}, refine=500)
gt, gc = L.grid_sequence(P, 3, 20000, keep={2}, refine=500)
worst = 0.0
for r, row in sorted(z7.items()):
    g = r * P.eps
    ml = float(lc[2].M(np.array([g]))[0])
    mg = float(L.grid_M(gc[2][0], gc[2][1], np.array([g]))[0])
    worst = max(worst, abs(row["M2"] - ml) / P.a, abs(row["M2"] - mg) / P.a, abs(row["theta"] - float(P.theta(g))) / P.a)
check("the coordinator's columns theta_na(g) and M_2(g) at its 16 rates agree with the referee's (both brackets) to 5e-9 a", worst < 5e-9, "| largest difference %.1e a" % worst)
small = [row["d"] for r, row in z7.items() if r <= 0.2]
check("'M_2 - T_2 is 0.03 a to 0.13 a for g <= 0.2 eps*'", 0.025 < min(small) < 0.035 and 0.12 < max(small) < 0.135, "| stored: %.3f a to %.3f a" % (min(small), max(small)))
check("'3.7e-3 a, 1.8e-3 a, 7e-4 a at g = 0.4, 0.5, 0.6 eps*'", abs(z7[0.4]["d"] - 3.7e-3) < 5e-5 and abs(z7[0.5]["d"] - 1.8e-3) < 6e-5 and abs(z7[0.6]["d"] - 7e-4) < 6e-6,
      "| stored: %.3e, %.3e, %.3e" % (z7[0.4]["d"], z7[0.5]["d"], z7[0.6]["d"]))
check("'there M_2 = b_2 - g' (the cap line): the coordinator's M_2(g) = b_2 - g at g = 0.1, 0.2, 0.3 eps* to 5e-9 a (its grid value of b_2 is 2e-9 a low)",
      all(abs(z7[r]["M2"] - (lt[2] - r * P.eps)) < 5e-9 * P.a for r in (0.1, 0.2, 0.3)),
      "| differences %s a" % ", ".join("%+.1e" % ((z7[r]["M2"] - (lt[2] - r * P.eps)) / P.a) for r in (0.1, 0.2, 0.3)))
# where the cap line of W_2 ends: 1/m_2
V2 = lc[2]
m2 = float(V2.al[-1])
print("     the cap line of W_2 has slope m_2 = %.6f: M_2(g) = b_2 - g for g <= 1/m_2 = %.6f eps*;  the level T_2 leaves b_2 - g at x* = 0.356042 eps* (a6_04)" % (m2, 1 / m2 / P.eps))
check("1/m_2 = 0.349 eps* < x* = 0.356 eps* (the earlier referee's postscript)", abs(1 / m2 / P.eps - 0.349) < 1e-3)
print()
print("time %.0f s" % (time.time() - t00))
print("ALL CHECKS PASS" if not FAIL else "FAILED: %s" % FAIL)
