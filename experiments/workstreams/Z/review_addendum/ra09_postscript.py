#!/usr/bin/env python3
"""RA09 -- postscript.  The addendum was changed while the review was in progress: two sections (A6a, A6b) were added
that are NOT part of the brief and were not refereed.  Three numerical remarks only, because they touch numbers of
this review:

 (1) the certified tops c_j of A6b (copied from the table of the addendum) against the referee's grid-free envelope
     tops b_j: Corollary A4 requires c_j >= b_j for every admissible sequence from the same start;
 (2) Proposition A12(b), "b_{j+1} = tau(M_{W_j, b_j})", tau(T) = inf_x a (x + T#(x))/(a + x), and M# = M:
     inf_x a (x + M_{W_j,b_j}(x))/(a + x)  against  b_{j+1}   (referee's structural sequence);
 (3) Proposition A12(c), "theta# = max(theta, a - .) = M_{W_1, a}", on a grid of rates.
Usage: python3 -B ra09_postscript.py
"""
import math

import numpy as np

import ra_lib as R

GOLD = R.GOLD
cert = {
    1.0: {2: 0.500410024, 3: 0.363300653, 4: 0.312791462, 5: 0.291376787, 6: 0.281323250, 8: 0.272750695, 10: 0.269065250,
          20: 0.264243938, 40: 0.263047017, 80: 0.262747193, 200: 0.262663126, 400: 0.262651110},
    2.0: {2: 0.505615446, 3: 0.383347314, 4: 0.341033400, 5: 0.323697863, 6: 0.315235252, 8: 0.307181543, 10: 0.303467854,
          20: 0.298465858, 40: 0.297189804},
    0.5: {2: 0.500026741, 3: 0.358645034, 4: 0.305680047, 5: 0.282897289, 6: 0.272167511, 8: 0.263247512, 10: 0.259553884,
          20: 0.254793046, 40: 0.253620656},
}
seqs = {}
print("== (1) certified tops of A6b (from the table of the addendum) against the grid-free envelope tops ==")
allok = True
for u in (1.0, 2.0, 0.5):
    P = R.Cube(u).setup()
    S = R.EnvSeq(P, max(cert[u]))
    seqs[u] = (P, S)
    print("# cube u = %g: h/a = %.9f" % (u, P.h / P.a))
    print("#    j     certified c_j/a    b_j/a (referee)    (c_j - b_j)/a    (c_j - b_j)/(b_j - h)    j^2 (c_j - h)/c_*^2    j^2 (b_j - h)/c_*^2")
    for j, c in cert[u].items():
        b = S.b[j] / P.a
        ok = c >= b - 5e-10                        # the table gives nine digits
        allok = allok and ok
        print("   %4d    %.9f       %.9f       %+.2e         %+.2e              %.4f                 %.4f   %s"
              % (j, c, b, c - b, (c - b) * P.a / (S.b[j] - P.h), j * j * (c * P.a - P.h) / P.cstar2, j * j * (S.b[j] - P.h) / P.cstar2, "" if ok else "  <-- c_j < b_j"))
print("c_j >= b_j at every listed level and slope (to the nine digits of the table): %s" % allok)


def tau_of_M(S, P, j):
    """inf over x > 0 of a (x + M_{W_j, b_j}(x))/(a + x)"""
    a = P.a
    f = lambda x: a * (x + S.M(j, x)[0]) / (a + x)
    xs = np.exp(np.linspace(math.log(1e-6 * a), math.log(50 * a), 400))
    vals = np.array([f(x) for x in xs])
    k = int(np.argmin(vals))
    lo, hi = xs[max(k - 1, 0)], xs[min(k + 1, len(xs) - 1)]
    for _ in range(100):
        m1 = hi - GOLD * (hi - lo)
        m2 = lo + GOLD * (hi - lo)
        if f(m1) > f(m2):
            lo = m1
        else:
            hi = m2
    return min(float(vals[k]), f(0.5 * (lo + hi)))


print("\n== (2) Proposition A12(b): tau(M_{W_j, b_j}) against b_{j+1} ==")
for name, P, S in (("cube u = 1", seqs[1.0][0], seqs[1.0][1]), ("Gaussian pair", R.Gauss().setup(), None)):
    if S is None:
        S = R.EnvSeq(P, 14)
    w = 0.0
    for j in range(0, 13):
        t = tau_of_M(S, P, j)
        w = max(w, abs(t - S.b[j + 1]) / P.a)
    print("%-14s max over j = 0..12 of |tau(M_{W_j,b_j}) - b_{j+1}|/a = %.2e" % (name, w))

print("\n== (3) Proposition A12(c): M_{W_1, a} against max(theta, a - x) ==")
for name, P in (("cube u = 1", seqs[1.0][0]), ("Gaussian pair", R.Gauss().setup())):
    S = R.EnvSeq(P, 2)
    w = 0.0
    for x in np.exp(np.linspace(math.log(1e-5 * P.a), math.log(1.2 * P.epsstar), 300)):
        w = max(w, abs(S.M(1, x)[0] - max(P.theta(x), P.a - x)) / P.a)
    print("%-14s max over 300 rates of |M_{W_1,a}(x) - max(theta(x), a - x)|/a = %.2e" % (name, w))
