"""Referee B, check 7: compare the recursion's tau_k (out_b6_*.txt, own grid implementation) with
   - the lower bound B_inf(k) of Proposition A (orbit of the slope map, blib, from the definition of theta),
   - the claimed limit c_*^2 = 2 pi^2 h^2 vartheta of Theorem R  (increments of 1/sqrt(tau_k - h) against 1/c_*),
   - for the kinked pairs: Proposition K's bound (L2 - L1) h/(k + 2) and the behaviour of k (tau_k - h).
Usage: python3 b7_compare.py pair outfile"""
import sys, math
import blib

name, fn = sys.argv[1], sys.argv[2]
P = blib.cube(float(name[4:])) if name.startswith("cube") and name != "cubroot" else \
    {"gauss": blib.gauss, "cubroot": blib.cubroot, "quad": blib.quad, "kink": blib.kink_author, "kinksmooth": blib.kink_smooth,
     "chord": blib.chord}[name]()
P.setup()
rows = []
for line in open(fn):
    if line.startswith("#"):
        continue
    f = line.split()
    rows.append((int(f[0]), float(f[1]), float(f[2])))
h = P.h
print("# %s: h = %.12f" % (P.name, h) + ("" if name in ("kink", "kinksmooth", "chord") else ", c_*^2 = %.8f, 1/c_* = %.6f" % (P.c2, 1 / P.cstar)))
if name in ("kink", "kinksmooth"):
    L1, L2 = (0.5, 0.75) if name == "kink" else (0.4 / 1.4, 0.5)
    print("# k   tau_k   B_inf(k)   tau_k - B_inf(k)   k (tau_k - h)   k (B_inf - h)   bound (L2-L1)h/(k+2)   1/(tau_k - h) increment   [(L2-L1)h = %.5f]" % ((L2 - L1) * h))
    prev = None
    for k, tA, tB in rows:
        if k > 12 and k % 4:
            prev = 1 / (tB - h)
            continue
        b = P.B_inf(k)
        inc = (1 / (tB - h) - prev) if prev is not None else float("nan")
        prev = 1 / (tB - h)
        print("%3d %.10f %.10f %+.3e  %.6f %.6f  %.6f  %.4f" % (k, tB, b, tB - b, k * (tB - h), k * (b - h), (L2 - L1) * h / (k + 2), inc))
elif name == "chord":
    print("# k   tau_k   B_inf(k)   tau_k - B_inf(k)   (tau_k - h)   ratio to previous   (B_inf - h) ratio to previous")
    pt = pb = None
    for k, tA, tB in rows:
        b = P.B_inf(k, tol=4e-16)
        print("%3d %.10f %.10f %+.3e  %.4e  %s  %s" % (k, tB, b, tB - b, tB - h, "%.4f" % ((tB - h) / pt) if pt else "-", "%.4f" % ((b - h) / pb) if pb and b > h else "-"))
        pt, pb = tB - h, b - h
else:
    print("# k   tau_k   B_inf(k)   tau_k - B_inf(k)   k^2(tau_k - h)/c_*^2   k^2(B_inf - h)/c_*^2   Q_k = 1/sqrt(tau_k - h)   (Q_k - Q_{k-4})/4 * c_*   offset c0 = c_* Q_k - k")
    Q = {}
    for k, tA, tB in rows:
        Q[k] = 1 / math.sqrt(tB - h)
    for k, tA, tB in rows:
        if k > 12 and k % 4:
            continue
        b = P.B_inf(k)
        sl = (Q[k] - Q[k - 4]) / 4 * P.cstar if k - 4 in Q else float("nan")
        print("%3d %.10f %.10f %+.3e  %.5f %.5f  %.4f  %.5f  %+.4f" % (k, tB, b, tB - b, k * k * (tB - h) / P.c2, k * k * (b - h) / P.c2, Q[k], sl, P.cstar * Q[k] - k))
