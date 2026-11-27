"""Referee B, check 5: Proposition K (a kink at the fixed point) and the heuristic classification of section 9.
Sigma from the definition of theta (blib), not from J.

 (a) three kinked pairs: the author's max(1 - 3e, 1/2 - e, 0); a kink between two strictly convex / affine pieces,
     max((1 - sqrt e)^2, 1/4 + 0.4 (1/4 - e)); and the edge case L1 = 0: max(1 - 3e, 1/4) (theta flat to the right of h).
     D(h + delta, s) = delta/h exactly on [L1, s_max]; > delta/h just outside; p_n finite for n <= n*;
     B_inf(k) - h >= (L2 - L1) h/(k + 2); k (B_inf(k) - h) -> ?
 (b) p = 1 (theta affine near h; J has a corner): Gaussian with a chord.  Multipliers on the two sides of L,
     passage time ~ ln(1/delta) (1/ln(1/lam_-) + 1/ln(lam_+)), B_inf(k) - h geometric.
 (c) p = 4/3 (theta'' (h) = 0, quartic contact) and p = 3 (theta''(h) = inf, |x|^{3/2}): exponents of the passage time
     and of B_inf(k) - h against delta^{-(p-1)/p} and k^{-p/(p-1)}.
"""
import math
import blib


def kink_flat():
    th = lambda e: max(1.0 - 3.0 * e, 0.25)
    dth = lambda e: -3.0 if e < 0.25 else 0.0
    return blib.TPair("kink, L1 = 0: max(1 - 3e, 1/4)", th, dth, 1.0, finite_slope0=3.0)


print("== (a) Proposition K")
cases = [(blib.kink_author(), 0.25, 1.0, 3.0), (blib.kink_smooth(0.4), 0.25, 0.4, 1.0), (kink_flat(), 0.25, 0.0, 3.0)]
for P, h, r1, r2 in cases:
    P.h = P.fixed_point()
    L1, L2 = r1 / (1 + r1), r2 / (1 + r2)
    print("  %s: h = %.12f, [L1, L2] = [%.6f, %.6f]" % (P.name, P.h, L1, L2))
    # J = h on [L1, L2] (direct minimisation)
    print("     J(L1), J((L1+L2)/2), J(L2), J(L1 - 0.02), J(L2 + 0.02): " + " ".join("%.9f" % P.J_direct(t) for t in [L1, 0.5 * (L1 + L2), L2, max(L1 - 0.02, 0.0), L2 + 0.02]))
    for d in [1e-2, 1e-3, 1e-4]:
        w0 = d / h
        smax = L2 - (1 - L2) * w0
        errs = [abs(P.sigma_direct(h + d, s) - s - w0) for s in [L1, L1 + 0.3 * (smax - L1), L1 + 0.7 * (smax - L1), smax - 1e-9]]
        out_hi = P.sigma_direct(h + d, smax + 1e-3) - (smax + 1e-3) - w0
        out_lo = (P.sigma_direct(h + d, L1 - 1e-3) - (L1 - 1e-3) - w0) if L1 > 1e-3 else float("nan")
        nstar = math.floor((L2 - L1) / w0 - (1 - L2)) - 1
        orb = P.orbit(h + d, nstar + 40)
        nfin = max(i for i, v in enumerate(orb) if math.isfinite(v))
        print("     delta = %.0e: max |D - delta/h| on [L1, s_max] = %.1e;  D - delta/h at s_max + 1e-3: %+.2e, at L1 - 1e-3: %+.2e;  n* = %d, p_n finite for n <= %d (%s), p_{n*} <= s_max: %s"
              % (d, max(errs), out_hi, out_lo, nstar, nfin, "ok" if nfin >= nstar else "VIOLATION", orb[nstar] <= smax + 1e-12))
    row = []
    for k in [1, 2, 3, 5, 10, 20, 80, 320]:
        b = P.B_inf(k)
        row.append((k, b - h, (L2 - L1) * h / (k + 2)))
    print("     k: B_inf(k) - h  [bound (L2-L1)h/(k+2)]  k(B_inf - h):  " + "; ".join("%d: %.3e [%.3e] %.5f" % (k, x, y, k * x) for k, x, y in row))
    print("     all B_inf(k) - h >= bound: %s;   (L2 - L1) h = %.5f" % (all(x >= y - 1e-13 for _, x, y in row), (L2 - L1) * h))

print("== (b) p = 1: theta affine near h (Gaussian with the chord over [0.16, 0.36]); h = 0.26, L = 1/2")
C = blib.chord()
C.h = C.fixed_point()
L = 0.5
h = C.h
d = 1e-4
cm = (C.J_direct(L) - C.J_direct(L - d)) / d
cp = (C.J_direct(L) - C.J_direct(L + d)) / d
lam_m = (h - cm * L) / (h + cm * (1 - L))
lam_p = 1 + cp / (h - cp * (1 - L))
print("  h = %.10f; one-sided slopes of J at L: J'(L-) = %.6f, -J'(L+) = %.6f (corner);  predicted multipliers of Sigma(h, .) at L: %.6f below, %.6f above"
      % (h, cm, cp, lam_m, lam_p))
dd = 1e-6
print("  measured: (Sigma(h, L - x) - L)/(-x) at x = 1e-3, 1e-5: %.6f %.6f;   (Sigma(h, L + x) - L)/x: %.6f %.6f"
      % ((C.sigma(h, L - 1e-3) - L) / (-1e-3), (C.sigma(h, L - 1e-5) - L) / (-1e-5), (C.sigma(h, L + 1e-3) - L) / 1e-3, (C.sigma(h, L + 1e-5) - L) / 1e-5))
rate = 1.0 / (1.0 / math.log(1 / lam_m) + 1.0 / math.log(lam_p))
print("  passage time N_t(delta), s_t = 0.6:  delta, N, N/ln(1/delta)   [prediction 1/ln(1/lam_-) + 1/ln(lam_+) = %.4f]" % (1 / rate))
for ex in [3, 5, 7, 9, 11, 13]:
    dl = 10.0 ** (-ex)
    N = C.passage(h + dl, 0.6)
    print("     %.0e  %4d  %.4f" % (dl, N, N / math.log(1 / dl)))
print("  B_inf(k) - h and the ratio of consecutive values   [prediction exp(-rate) = %.5f]" % math.exp(-rate))
prev = None
for k in range(2, 31, 2):
    b = C.B_inf(k, tol=1e-16) - h
    print("     k = %2d: %.6e   ratio per level %s" % (k, b, "%.5f" % math.sqrt(b / prev) if prev else "-"))
    prev = b

print("== (c) other exponents p")


def quartic(c=8.0):
    x0 = (1.0 / (4 * c)) ** (1.0 / 3)

    def th(e):
        x = min(e - 0.25, x0)
        return 0.25 - x + c * x ** 4

    def dth(e):
        x = e - 0.25
        return -1.0 + 4 * c * x ** 3 if x < x0 else 0.0
    return blib.TPair("quartic contact: 1/4 - x + 8 x^4, x = e - 1/4  (p = 4/3)", th, dth, th(1e-300), finite_slope0=-dth(1e-300))


def threehalves(c=2.0):
    x0 = (1.0 / (1.5 * c)) ** 2

    def th(e):
        x = min(e - 0.25, x0)
        return 0.25 - x + c * abs(x) ** 1.5

    def dth(e):
        x = e - 0.25
        if x >= x0:
            return 0.0
        return -1.0 + 1.5 * c * math.copysign(abs(x) ** 0.5, x)
    return blib.TPair("|x|^{3/2} contact: 1/4 - x + 2 |x|^{3/2}  (p = 3)", th, dth, th(1e-300), finite_slope0=-dth(1e-300))


for P, p in [(quartic(), 4.0 / 3), (threehalves(), 3.0)]:
    P.h = P.fixed_point()
    h, L = P.h, 0.5
    # exponent of h - J near L
    e1 = math.log((h - P.J_direct(L + 0.02)) / (h - P.J_direct(L + 0.002))) / math.log(10.0)
    print("  %s: h = %.10f, a = %.5f;  local exponent of h - J(L + v) between v = 0.002 and 0.02: %.3f (p = %.3f)" % (P.name, h, P.a, e1, p))
    st = 0.5 * (L + 1 - h / P.a)
    Ns = []
    for ex in [4, 6, 8, 10]:
        dl = 10.0 ** (-ex)
        Ns.append((dl, P.passage(h + dl, st)))
    sl = [math.log(Ns[i + 1][1] / Ns[i][1]) / math.log(Ns[i][0] / Ns[i + 1][0]) for i in range(len(Ns) - 1)]
    print("     N_t(delta) at delta = 1e-4, 1e-6, 1e-8, 1e-10: %s;  local exponents %s  (prediction (p-1)/p = %.4f)"
          % (" ".join(str(n) for _, n in Ns), " ".join("%.4f" % x for x in sl), (p - 1) / p))
    ks = [10, 20, 40, 80, 160, 320]
    bs = [P.B_inf(k, tol=1e-16) - h for k in ks]
    sl = [math.log(bs[i] / bs[i + 1]) / math.log(ks[i + 1] / ks[i]) for i in range(len(ks) - 1)]
    print("     B_inf(k) - h at k = 10..320: %s;  local exponents %s  (prediction p/(p-1) = %.4f)"
          % (" ".join("%.3e" % b for b in bs), " ".join("%.4f" % x for x in sl), p / (p - 1)))
