"""Referee A, test 1b: the minimax identity behind Proposition U, many random cases, no brute force on R.

  F_inf(g) = inf_{e>g} (1 - g/e) S(g theta(e)/(e-g))      (R[T](g) <= F_inf by Lemma M, machine-checked for theta(e) > 0)
  U(g)     = sup_B (B - Sigma(B, W(B)) g)                  (the bound of Proposition U)
Theory: U <= F_inf trivially; the proof of Proposition U is F_inf <= U.  We look for F_inf > U.
Random convex nondecreasing piecewise-linear W (several shapes incl. W(0) > 0, flat pieces, W(b) = 1), random b in
(0.2 a, 1.2 a) (b may exceed a), g log-uniform in (1e-5 h, 30 h).
Usage: python3 a1b_minimax_many.py [seed] [ntrial per theta]
"""
import math, sys, time
import numpy as np
import a1_propU_lib as L
from ralib import Gauss, Cube, Expo, Power, Recip, PwLin

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 11
ntrial = int(sys.argv[2]) if len(sys.argv) > 2 else 150
blo = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2          # b uniform in (blo a, bhi a)
bhi = float(sys.argv[4]) if len(sys.argv) > 4 else 1.2
L.rng = np.random.default_rng(seed)
rng = L.rng
thetas = [
    Gauss(), Cube(1.0), Cube(3.0), Expo(1.0, 0.3, 0.0), Expo(1.0, 0.25, 0.08), Expo(0.2, 2.0, 0.05),
    Recip(1.0, 0.5, 2.0), Recip(3.0, 0.1, 1.0), Power(1.0, 1.0, 1.0, 2.0), Power(1.0, 0.7, 0.35, 1.5), Power(2.0, 0.5, 1.0, 1.0),
    PwLin([(1.0, 3.0), (0.5, 1.0)], 0.0, "kinked max(1-3e, 1/2-e, 0)"),
    PwLin([(1.0, 4.0), (0.7, 1.5), (0.4, 0.4)], 0.05, "pw-linear 3 pieces, floor 0.05"),
    PwLin([(1.0, 0.8)], 0.0, "single line (1 - 0.8 e)_+"),
    PwLin([(1.0, 0.5), (0.9, 0.3)], 0.6, "pw-linear, floor 0.6 > h?"),
]
print("# seed %d; %d (W, b) per theta, b in (%g a, %g a), 3 values of g each" % (seed, ntrial, blo, bhi))
print("# theta                                        h         max (F_inf-U)/a   min (F_inf-U)/a   cases")
t0 = time.time(); gmax = -1e9; gmin = 1e9; worst = None
for th in thetas:
    h = th.fixed_point()
    mx, mn, cnt = -1e9, 1e9, 0
    for _ in range(ntrial):
        b = rng.uniform(blo, bhi) * th.a
        xs, W, kind = L.make_W(b)
        for g in [10 ** rng.uniform(-5, -1) * h, rng.uniform(0.1, 2.0) * h, 10 ** rng.uniform(0.3, 1.5) * h]:
            U = L.U_and_Llow(th, xs, W, g, nB=600)[0]
            Fi = L.F_inf(th, xs, W, g)[0]
            d = (Fi - U) / th.a
            if d > mx:
                mx = d
                if d > gmax:
                    worst = (th.name, str(kind), b, [float(x) for x in xs], [float(x) for x in W], g, U, Fi)
            mn = min(mn, d); cnt += 1
    gmax = max(gmax, mx); gmin = min(gmin, mn)
    print("%-44s %.6f  %+.3e        %+.3e        %d" % (th.name, h, mx, mn, cnt)); sys.stdout.flush()
print("# overall max (F_inf - U)/a = %+.3e, min = %+.3e; %.0f s" % (gmax, gmin, time.time() - t0))
print("# worst:", worst)
