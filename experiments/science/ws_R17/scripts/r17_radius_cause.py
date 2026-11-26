#!/usr/bin/env python3
"""R17: why the exact closing radius of a slope-step level exceeds the radius floor(rho_h n_o) + 1 of Lemma Q4:
sizes of the two candidate causes, in nats, on exact tables (our r16lib.Tab):
 (i)  theta of the level against the threshold of the lemma: ln(c_eta theta) - [ln(n_o+1) + 2u + e^u + n_o h];
 (ii) the bound (2.2)/(a) of the lemma against the exact Gamma~ at r_1 = floor(rho_h n_o) + 1:
      [ln(n_o+1) + 2u + e^u + n_o h] - ln Gamma~(r_1).
Their sum is ln(c_eta theta) - ln Gamma~(r_1), the room that lets the radius grow beyond r_1."""
import math, os, resource, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "ws_R16"))
import r16lib as R
import r17_formula as F
t0 = time.time()
print("# u n n_o xhat | (i) theta vs threshold | (ii) lemma bound vs exact Gamma~(r_1) | sum | r_1, first r with Gamma~(r) > c_eta theta "
      "(= r_dag + 1 if [P] decides), ln Gamma~ there, ln(c_eta theta)")
for (u, n, no) in ((1.0, 2000, 400), (1.0, 3000, 1000), (1.0, 600, 8), (2.0, 600, 100), (2.0, 1200, 600), (0.5, 2500, 250),
                   (1.0, 64000, 63362)):
    C = F.Cube(u)
    if no == 63362:
        xhat = C.h * n
    else:
        xhat = 1 + F.c_log(C, n) + C.h * (no + 0.5)
    n_o = math.floor((xhat - 1 - F.c_log(C, n)) / C.h)
    assert n_o == no, (n_o, no)
    y = xhat - 1
    ltheta = y + math.log1p(-(3 * math.e + 1 + (2 * C.p) ** n / math.e) * math.exp(-y))
    lct = ltheta - math.log(3)                      # ln(c_eta theta), eta = 1/2
    lem = math.log(n_o + 1) + 2 * u + math.exp(u) + n_o * C.h
    t = R.tab(n_o, u)
    r1 = min(n_o - 1, math.floor(C.rho_h * n_o) + 1)
    lG = t.lGt
    first = next((r for r in range(n_o) if lG[r] > lct), None)
    print("%g %d %d %.3f | %.2f | %.2f | %.2f | r_1=%d, first=%s, lnGamma~(first)=%.2f, lnGamma~(r_1)=%.2f, ln(c_eta theta)=%.2f"
          % (u, n, n_o, xhat, lct - lem, lem - lG[r1], lct - lG[r1], r1, first, lG[first] if first is not None else float('nan'),
             lG[r1], lct))
    R.clear_tabs()
print("LAST LINE r17_radius_cause.py: completed; wall %.1f s; peak RSS %.1f MB"
      % (time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))
