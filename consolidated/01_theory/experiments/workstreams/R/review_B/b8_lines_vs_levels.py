"""Referee B, check 8: Proposition A at POSITIVE accuracy.  The level functions T_k of the recursion (computed by
b6_recursion.py, saved with SAVE_LEVELS=...) against the minorant lines  B - p_k(B) x  of Proposition A, for many B.
Reports  max over B and x of [B - p_k(B) x - T_k(x)]  (should be <= 0 up to the accuracy of the grid computation) and
how close the envelope of the lines comes to T_k.
Usage: python3 b8_lines_vs_levels.py pair level [level ...]"""
import sys, math
import numpy as np
import blib

name = sys.argv[1]
P = {"gauss": blib.gauss, "cubroot": blib.cubroot, "kink": blib.kink_author, "chord": blib.chord}[name]()
P.setup()
for lev in [int(v) for v in sys.argv[2:]]:
    x, T = np.load("T_%s_level%d.npy" % (name, lev))
    tau = T[0]
    binf = P.B_inf(lev, tol=4e-16)
    worst, where = -1e9, None
    env = np.full(len(x), -np.inf)
    nB = 400
    for i in range(1, nB + 1):
        B = binf * i / nB * (1 - 1e-9)
        s = P.p(B, lev)
        if not math.isfinite(s):
            continue
        line = B - s * x[1:]
        d = line - T[1:]
        j = int(np.argmax(d))
        if d[j] > worst:
            worst, where = float(d[j]), (B, s, float(x[1 + j]))
        env[1:] = np.maximum(env[1:], line)
    gap = T[1:] - env[1:]
    sel = (x[1:] > 1e-4) & (T[1:] > 1e-3)
    print("%s level %d: tau = %.10f, B_inf = %.10f;  max_{B,x} [line - T_k] = %+.2e at (B, slope, x) = (%.5f, %.4f, %.3e);  T_k - envelope of the lines: median %.2e, max %.2e (x > 1e-4, T > 1e-3)"
          % (name, lev, tau, binf, worst, where[0], where[1], where[2], float(np.median(gap[sel])), float(np.max(gap[sel]))))
