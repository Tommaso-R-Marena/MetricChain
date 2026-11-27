#!/usr/bin/env python3
"""R17: extra evaluations of formula (5.2) with r17_formula.py (own code):
 (1) Theorem Q9(d): accuracies eps_n = n^{-A} (the referee R12: ratio (bound - nh)/sqrt(n ln n) between 3.1 and 6.0
     for A in {1/2, 1, 3}, n <= 1e12);
 (2) the side condition T q* <= Lam_0 of Proposition Q9a at the best M of the table, and Lam_T/Lam_0;
 (3) sup over a grid of (bound - nh)/sqrt(n ln n) with min(bound, n ln 2) at u = 1/2, 2, 4 (referee O1: 2.77, 8.74, 32.2)."""
import math, resource, time
import r17_formula as F
t0 = time.time()
C = F.Cube(1.0)
print("== (1) eps_n = n^-A, u = 1, delta = 0.05: ratio (bound - nh)/sqrt(n ln n) at the best M ==")
lo, hi = 1e9, -1e9
for A in (0.5, 1.0, 3.0):
    row = []
    for e10 in (3, 4, 5, 6, 8, 10, 12):
        n = 10 ** e10
        best, rows, ep = F.best_M(C, n, n ** (-A), math.log(20.0))
        bound = min(best[1], n * math.log(2))
        r = (bound - n * C.h) / math.sqrt(n * math.log(n))
        row.append("1e%d: %.2f (M=%d)" % (e10, r, best[0]))
        if e10 >= 4:
            lo, hi = min(lo, r), max(hi, r)
    print("A=%g: %s" % (A, "; ".join(row)))
print("range over n = 1e4..1e12: %.2f .. %.2f" % (lo, hi))
print("\n== (2) side condition of Prop Q9a at the best M (u=1, eps=1, delta=0.05) ==")
for n in (16000, 64000, 10 ** 6, 10 ** 8, 10 ** 10, 10 ** 12):
    best, rows, ep = F.best_M(C, n, 1.0, math.log(20.0))
    M = best[0]
    d, J, k, B, R, phi = ep
    Lam0 = math.log(20.0) + n * math.log(2)
    eh, c, alpha = F.accuracies(1.0, M)
    qstar = max([F.q_S(C, n, 2 * Lam0)] + [F.q_D(C, n, 2 * Lam0, c[m]) for m in range(M)])
    det = F.E_total(C, n, 1.0, math.log(20.0), M, ep=ep, detail=True)
    print("n=%.3g M=%d T=%d q*=%.1f (q*/ln n = %.2f)  T q*/Lam_0 = %.4f   Lam_T/Lam_0 = %.4f"
          % (n, M, k[M] - 1, qstar, qstar / math.log(n), (k[M] - 1) * qstar / Lam0, det['LamT'] / det['Lam0']))
print("\n== (3) sup of (min(bound, n ln 2) - nh)/sqrt(n ln n) over n = 10^(j/20), 2 <= n <= 1e12 ==")
for u in (0.5, 1.0, 2.0, 4.0):
    Cu = F.Cube(u)
    best_r = (-1e9, None)
    j = 7
    while j <= 240:
        n = int(round(10 ** (j / 20.0)))
        b, rows, ep = F.best_M(Cu, n, 1.0, math.log(20.0))
        bound = min(b[1], n * math.log(2))
        r = (bound - n * Cu.h) / math.sqrt(n * math.log(n))
        if r > best_r[0]:
            best_r = (r, n, b[0], bound == n * math.log(2))
        j += 1
    b, rows, ep = F.best_M(Cu, 10 ** 12, 1.0, math.log(20.0))
    r12 = (b[1] - 10 ** 12 * Cu.h) / math.sqrt(10 ** 12 * math.log(10 ** 12))
    print("u=%g: sup %.2f at n=%d (M=%d%s); at 1e12: %.2f; C_* = %.2f"
          % (u, best_r[0], best_r[1], best_r[2], ", enumeration" if best_r[3] else "", r12, Cu.Cstar))
print("LAST LINE r17_formula_extra.py: completed; wall %.1f s; peak RSS %.1f MB"
      % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
