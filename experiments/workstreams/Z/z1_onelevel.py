#!/usr/bin/env python3
"""Z1: Proposition Z3 of docs/workstreams/Z_REPORT.md against the exact one-level evaluator.

For the cube of slope u, the chain of cut orbit curves (W_j, b_j) (s_t = L + 0.05, b_0 = h + eps1) and a horizon
N = d: the inner family SATURATES the type H^infty(grid of W_j; 0) -- its certified cost is exactly
max(0, max_lines [d' B - sigma x]) -- and the level L(d; n_o, y/n_o) of Lemma Z2 is evaluated exactly (two
independent evaluators, q2lib.Ev) for every admissible outer block n_o.  Checked, for each (j, d, xhat):

 (A) accuracy:      the accuracy of every level is at most xhat;
 (B) (U-infinity):  ln C_max(n_o) <= d * max_{lines of W_j} Psi_g(n_o/d) + ell_0(d, Lambda)          for every n_o;
 (C) exponent:      min_{n_o} d * max Psi_g(n_o/d)  <=  d * M_{W_{j+1}, b_{j+1}}(g) + 1 + a d_min    (Proposition Z1(2) + Lemma Z1a);
 (D) the type:      ln C_max at the n_o of the design (the minimiser of the proxy Pi_j(n_o) = d * max Psi_g(n_o/d))
                    <= max_{grid of W_{j+1}} [d B - sigma xhat] + X_0(d) + d_min ln 2 + 2 + ell_0(d, Lambda);
                    (the least ln C_max over all n_o is recorded as well: how much the proxy gives away).

Controls (each must FAIL somewhere): (D) without ell_0 and X_0; (C) with the curve W_{j+2} in place of W_{j+1}
(two levels' gain claimed for one); (C) for a NON-CONVEX family (the two lines (b_j, 0) and (h, 1) only are a
convex family -- instead the family {W_j above its chord}, see below, is not needed: the control used is the
line-by-line value, max over lines of [B - Sigma(B, s) g], which is BELOW the minimax value for a single
non-convex family and is what dead end D64 records).
Two sequences of curves (argument `mode`): 'cut' - the cut orbit curves restarted at b_0 = h + eps1 (R_REPORT section 6);
'env' - the envelope sequence from b_0 = a (zetalib.EnvZ; floating point on a grid).
Usage: python3 z1_onelevel.py [u] [eps1] [mode]        (default 1.0 0.003 cut)
"""
import math
import sys

import zetalib as Z

Q2 = Z.Q2
u = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
eps1 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.003
mode = sys.argv[3] if len(sys.argv) > 3 else "cut"
JMAX = 12
C = Z.make_chain(mode, u, JMAX + 2, eps1)
h, a = C.h, C.a
ev = Q2.Ev(u, both=True)
ld = math.log(0.05)
dm = Z.dmin(u)
print("# cube u = %g: h = %.6f a = %.6f; %s; curves with values in [0, 1] to level %d: %s (largest W %.3f)"
      % (u, h, a, ("cut orbit curves, s_t = L + 0.05, b_0 = h + %g" % eps1) if mode == "cut" else "envelope sequence from b_0 = a",
         JMAX + 2, C.range_ok, C.worstW))
print("# (b_j - h)/h, j = 0..%d: %s" % (JMAX, " ".join("%.4f" % ((b - h) / h) for b in C.b[:JMAX + 1])))
viol = {k: 0 for k in "ABCD"}
ctrl = {"D_no_losses": 0, "C_two_levels": 0}
worst = {k: -1e18 for k in "BCD"}
nlev = 0
gave = 0.0
rows = []
for d in (300, 1000, 3000, 10000):
    N = d
    X0 = Z.X0(u, d)
    Lam = -ld + d * math.log(2)
    ell0 = Q2.ell0(ev.cu, d, Lam)
    for j in ((0, 3, 5, 6, 8, 11) if mode == "cut" else (0, 1, 2, 3, 5, 8, 11)):
        lines = C.grid(j, N)
        nxt = C.grid(j + 1, N)
        nxt2 = C.grid(j + 2, N)
        inner = Q2.SatLines(lines)
        for xh in (X0 + 1, X0 + 3, X0 + 10, X0 + 0.003 * d, X0 + 0.01 * d, X0 + 0.03 * d, X0 + 0.1 * d, X0 + 0.3 * d, X0 + u * d):
            y = xh - X0
            g = y / d
            stride = max(1, (d - dm) // 400)
            best_lC, best_psi, best_no, lC_at_proxy = math.inf, math.inf, None, None
            for n_o in sorted(set(list(range(1, d - dm + 2, stride)) + [1, 2, 3, d - dm + 1])):
                phi = n_o / d
                e = y / n_o
                th = C.theta(e)
                lth = math.log(3.0 * (n_o + 1)) + 2 * u + math.exp(u) + y
                r = Q2.level_U(ev, d, n_o, lth, n_o * th, ld, inner)
                nlev += 1
                if r['c']['xout'] > xh + 1e-9:
                    viol["A"] += 1
                psi = d * max((1 - phi) * B + (1 - s) * phi * th for (B, s) in lines)
                exB = r['lC'] - (psi + ell0)
                worst["B"] = max(worst["B"], exB)
                if exB > 1e-9:
                    viol["B"] += 1
                best_lC = min(best_lC, r['lC'])
                if psi < best_psi:
                    best_psi, best_no, lC_at_proxy = psi, n_o, r['lC']
            M1 = d * Z.Mval(nxt, g)
            M2 = d * Z.Mval(nxt2, g)
            exC = best_psi - (M1 + 1 + a * dm + stride * a)       # a scan with a stride misses the best n_o by < stride
            worst["C"] = max(worst["C"], exC)
            if exC > 1e-9:
                viol["C"] += 1
            if best_psi - (M2 + 1 + a * dm + stride * a) > 1e-9:
                ctrl["C_two_levels"] += 1
            typ = max(d * B - s * xh for (B, s) in nxt)
            exD = lC_at_proxy - (typ + X0 + dm * math.log(2) + 2 + ell0 + stride * a)
            worst["D"] = max(worst["D"], exD)
            if exD > 1e-9:
                viol["D"] += 1
            if lC_at_proxy - typ > 1e-9:
                ctrl["D_no_losses"] += 1
            gave = max(gave, lC_at_proxy - best_lC)
            rows.append((d, j, xh, best_no, lC_at_proxy, typ, lC_at_proxy - typ, X0 + ell0, best_psi - M1))
print("# %d levels evaluated exactly; largest disagreement of the two evaluators %.2e" % (nlev, ev.maxdiff))
print("#      d   j      xhat   n_o*   ln C_max   type(j+1)   excess   X_0+ell_0   d*(min Psi - M_{j+1})")
for r in rows:
    if r[1] in ((0, 6, 11) if mode == "cut" else (1, 3, 8)) and r[0] in (1000, 10000):
        print("  %6d  %2d  %8.1f  %5d  %9.2f  %9.2f  %7.2f   %7.2f     %9.3f" % r)
print("violations: (A) accuracy %d, (B) (U-infinity) %d, (C) exponent %d, (D) the type %d   [each must be 0]"
      % (viol["A"], viol["B"], viol["C"], viol["D"]))
print("largest excess: (B) %.3f, (C) %.3f, (D) %.3f   [each must be <= 0]" % (worst["B"], worst["C"], worst["D"]))
print("the proxy choice of n_o costs at most %.3f nats more than the n_o with the least certified bound" % gave)
print("controls: (D) without its losses fails in %d cases; (C) with W_{j+2} for W_{j+1} fails in %d cases   [each must be > 0]"
      % (ctrl["D_no_losses"], ctrl["C_two_levels"]))
ok = all(v == 0 for v in viol.values()) and all(v > 0 for v in ctrl.values()) and C.range_ok
print("ALL CHECKS PASS" if ok else "A CHECK FAILED")
