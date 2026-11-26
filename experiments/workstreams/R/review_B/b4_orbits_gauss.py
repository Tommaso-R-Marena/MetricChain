"""Referee B, check 4: (P1)-(P3) on new pairs; section 10 (the Gaussian pair exactly).

 (P1) p_j convex, nondecreasing in B, nondecreasing in j, p_j(0) = 0  [grid of B, extended values handled]
 (P2) p_j(h) <= L, and the approach L - p_j(h) ~ 2 vartheta h / j     [j up to 10^5]
 (P3) p_j(B) >= j (B - h)/h
 Section 10: trace/determinant/eigenvalues of the Moebius matrix; psi = 2 arctan(sqrt(4B - 1)) (double angle);
             the closed form (k - 1) psi(B) + phi_0(B) = pi against the orbit; my simplification
             B_inf(k) = 1/(4 cos^2(pi/(2k + 1))); the expansion 1/4 + (pi^2/16)/(k + 1/2)^2 (1 + O(k^-2)).
"""
import math
import mpmath as mp
import blib

pairs = [blib.quad(), blib.cubroot(), blib.expo(), blib.shifted()]
for P in pairs:
    P.setup()

print("== (P1): second differences of p_j on a grid of B in [0, 1.5 h] (601 points), j = 1, 2, 3, 5, 8, 13, 21, 34")
for P in pairs:
    Bs = [1.5 * P.h * i / 600 for i in range(601)]
    worst, monoB, monoj, zero = 0.0, 0.0, 0.0, 0.0
    prev = [0.0] * len(Bs)
    cur = [0.0] * len(Bs)
    js = {1, 2, 3, 5, 8, 13, 21, 34}
    domain_ok = True
    for j in range(1, 35):
        cur = [P.sigma(B, s) if math.isfinite(s) else math.inf for B, s in zip(Bs, prev)]
        monoj = max(monoj, max((a - b) for a, b in zip(prev, cur) if math.isfinite(b)) if any(math.isfinite(b) for b in cur) else 0.0)
        zero = max(zero, abs(cur[0]))
        if j in js:
            fin = [math.isfinite(v) for v in cur]
            # the finite set must be an initial segment
            k = fin.index(False) if False in fin else len(fin)
            domain_ok = domain_ok and all(not f for f in fin[k:])
            for i in range(1, k - 1):
                d2 = cur[i + 1] - 2 * cur[i] + cur[i - 1]
                worst = max(worst, -d2 / max(1.0, abs(cur[i + 1])))
                monoB = max(monoB, cur[i - 1] - cur[i])
        prev = cur
    print("  %-28s most negative 2nd difference (relative) %.1e; decrease in B %.1e; decrease in j %.1e; |p_j(0)| %.1e; finite set an initial segment: %s"
          % (P.name, worst, monoB, monoj, zero, domain_ok))

print("== (P2): p_j(h) <= L;   j (L - p_j(h)) -> 2 vartheta h")
for P in pairs:
    s, row, ok = 0.0, [], True
    for j in range(1, 100001):
        s = P.sigma(P.h, s)
        ok = ok and s <= P.L + 1e-15
        if j in (10, 100, 1000, 10000, 100000):
            row.append(j * (P.L - s))
    print("  %-28s p_j(h) <= L for j <= 1e5: %s;  j (L - p_j(h)) at j = 10..1e5: %s   (2 vartheta h = %.5f)"
          % (P.name, ok, " ".join("%.5f" % x for x in row), 2 * P.vartheta * P.h))

print("== (P3): min over j <= 60 and 40 values of B in (h, 1.3 h] of p_j(B) - j (B - h)/h (finite values only)")
for P in pairs:
    worst = 1e9
    for i in range(1, 41):
        B = P.h * (1 + 0.3 * i / 40)
        s = 0.0
        for j in range(1, 61):
            s = P.sigma(B, s)
            if not math.isfinite(s):
                break
            worst = min(worst, s - j * (B - P.h) / P.h)
    print("  %-28s %.3e (>= 0)" % (P.name, worst))

print("== Section 10: the Gaussian pair")
mp.mp.dps = 40
B = mp.mpf("0.3")
M = mp.matrix([[1 - B, -B], [1, -B]])
ev = mp.eig(M, left=False, right=False)
psi = mp.atan(mp.sqrt(4 * B - 1) / (1 - 2 * B))
print("  B = 0.3: trace %s (1 - 2B = %s), det %s (B^2 = %s), |eigenvalue| %s, arg %s, psi %s, 2 arctan sqrt(4B-1) %s"
      % (mp.nstr(M[0, 0] + M[1, 1], 8), mp.nstr(1 - 2 * B, 8), mp.nstr(mp.det(M), 8), mp.nstr(B ** 2, 8), mp.nstr(abs(ev[0]), 8),
         mp.nstr(abs(mp.arg(ev[0])), 12), mp.nstr(psi, 12), mp.nstr(2 * mp.atan(mp.sqrt(4 * B - 1)), 12)))
# the map in y = 1 - s
s = mp.mpf("0.2")
y = 1 - s
print("  Moebius in y = 1 - s at (B, s) = (0.3, 0.2): 1 - Sigma = %s, ((1-B)y - B)/(y - B) = %s"
      % (mp.nstr(1 - B * (1 - s) / (1 - s - B), 15), mp.nstr(((1 - B) * y - B) / (y - B), 15)))


def p_finite(B, k):
    """is p_k(B) finite?  (all of s_0..s_{k-1} have s + B < 1)"""
    s = mp.mpf(0)
    for _ in range(k):
        if s + B >= 1:
            return False
        s = B * (1 - s) / (1 - s - B)
    return True


def Binf_orbit(k):
    lo, hi = mp.mpf(1) / 4, mp.mpf(1)
    for _ in range(110):
        mid = (lo + hi) / 2
        if p_finite(mid, k):
            lo = mid
        else:
            hi = mid
    return lo


def Binf_report(k):
    arccot = lambda x: mp.pi / 2 - mp.atan(x)
    f = lambda B: (k - 1) * mp.atan2(mp.sqrt(4 * B - 1), 1 - 2 * B) + arccot((1 - 3 * B) / ((1 - B) * mp.sqrt(4 * B - 1))) - mp.pi
    lo, hi = mp.mpf(1) / 4 + mp.mpf(10) ** (-30), mp.mpf(1) - mp.mpf(10) ** (-30)
    for _ in range(120):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo


print("   k   B_inf (orbit)            report's root - orbit   1/(4cos^2(pi/(2k+1))) - orbit   (B_inf - 1/4)(k + 1/2)^2/(pi^2/16) - 1   same * k^2")
for k in [1, 2, 3, 4, 5, 8, 16, 50, 100, 320, 1000]:
    bo = Binf_orbit(k)
    br = Binf_report(k)
    bc = 1 / (4 * mp.cos(mp.pi / (2 * k + 1)) ** 2)
    rel = (bo - mp.mpf(1) / 4) * (k + mp.mpf(1) / 2) ** 2 / (mp.pi ** 2 / 16) - 1
    print("  %4d  %s   %s   %s   %s   %s" % (k, mp.nstr(bo, 18), mp.nstr(br - bo, 3), mp.nstr(bc - bo, 3), mp.nstr(rel, 6), mp.nstr(rel * k * k, 6)))
print("  (3 - sqrt 5)/2 = %s;   Lean witnesses 3/8 <= B_inf(2), 3/10 <= B_inf(3): %s %s"
      % (mp.nstr((3 - mp.sqrt(5)) / 2, 18), 0.375 <= Binf_orbit(2), 0.3 <= Binf_orbit(3)))
print("  ratio B_inf(k) - 1/4 to (pi^2/16)/k^2 at k = 100, 160, 320: %s  (report section 11: 0.9902, 0.9938, 0.9969)"
      % " ".join(mp.nstr((1 / (4 * mp.cos(mp.pi / (2 * k + 1)) ** 2) - mp.mpf(1) / 4) * k * k / (mp.pi ** 2 / 16), 6) for k in [100, 160, 320]))
