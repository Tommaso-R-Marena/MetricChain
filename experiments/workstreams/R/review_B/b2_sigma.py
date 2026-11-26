"""Referee B, check 2: (Sigma1)-(Sigma7) of R_REPORT.md section 2, on pairs that the author did not use, with the slope
map computed from its definition (blib.sigma_direct / blib.sigma), never through J."""
import math, random, sys
import numpy as np
import blib

rng = random.Random(20261126)
pairs = [blib.quad(), blib.cubroot(), blib.expo(), blib.shifted(), blib.cube(2.0)]
for P in pairs:
    P.setup()


def psi_direct(P, s, w):
    """Psi_s(w) = inf_e [(1 - s) theta(e) + (s + w) e], directly."""
    vals = (1.0 - s) * P._thgrid + (s + w) * P._egrid
    i = int(np.argmin(vals))
    lo, hi = P._zgrid[max(i - 1, 0)], P._zgrid[min(i + 1, len(vals) - 1)]
    f = lambda z: -((1.0 - s) * P.theta(math.exp(z)) + (s + w) * math.exp(z))
    z, v = blib.golden_max(f, lo, hi)
    return min(-v, float(vals[i]))


def D_via_psi(P, B, s, direct=True):
    """min{w >= -s : Psi_s(w) >= B} by bisection (Psi_s nondecreasing); Psi directly or as (1 + w) J((s + w)/(1 + w))."""
    psi = (lambda w: psi_direct(P, s, w)) if direct else (lambda w: (1 + w) * P.J_direct((s + w) / (1 + w)))
    lo, hi = -s, 1.0
    if psi(lo) >= B:
        return lo
    while psi(hi) < B:
        hi *= 2
        if hi > 1e9:
            return math.inf
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if psi(mid) >= B:
            hi = mid
        else:
            lo = mid
    return hi


print("== (Sigma1) joint convexity / monotonicity (random points of the regular region, sigma_direct)")
for P in pairs:
    worst, mono = -1.0, 0.0
    for _ in range(1500):
        s1, s2 = rng.uniform(-0.3, 0.97), rng.uniform(-0.3, 0.97)
        B1, B2 = rng.uniform(0, (1 - s1) * P.a * 0.995), rng.uniform(0, (1 - s2) * P.a * 0.995)
        lam = rng.uniform(0.05, 0.95)
        Bm, sm = lam * B1 + (1 - lam) * B2, lam * s1 + (1 - lam) * s2
        v1, v2, vm = P.sigma_direct(B1, s1), P.sigma_direct(B2, s2), P.sigma_direct(Bm, sm)
        worst = max(worst, (vm - (lam * v1 + (1 - lam) * v2)) / max(1.0, v1, v2))
        dB, ds = rng.uniform(0, 0.01) * P.a, rng.uniform(0, 0.01)
        if B1 + dB < (1 - s1 - ds) * P.a:
            mono = max(mono, v1 - P.sigma_direct(B1 + dB, s1 + ds))
    print("  %-40s max [Sigma(mid) - mean]/scale = %+.2e   monotone violation = %.2e" % (P.name, worst, mono))

print("== (Sigma2) finite below the line B = (1 - s) a, infinite above (ratio at e = 1e-13, 1e-10 as a probe)")
for P in pairs:
    s = 0.3
    Bb = (1 - s) * P.a
    f = lambda B, e: (B - (1 - s) * P.theta(e)) / e
    print("  %-40s B = 0.999(1-s)a: Sigma = %.4f;   B = 1.001(1-s)a: ratio at e = 1e-10: %.3e, at 1e-13: %.3e"
          % (P.name, P.sigma_direct(0.999 * Bb, s), f(1.001 * Bb, 1e-10), f(1.001 * Bb, 1e-13)))

print("== (Sigma3) attainment.  Interior points: the scan maximiser is interior and the value is the sup.")
for P in pairs:
    ok = True
    for _ in range(200):
        s = rng.uniform(0, 0.9)
        B = rng.uniform(0.05, 0.98) * (1 - s) * P.a
        e, v = P.argmax_direct(B, s)
        ok = ok and (v <= 0 or (P.e_lo * 10 < e < P.e_hi / 10))
    print("  %-40s maximiser found in the interior of (0, inf) whenever Sigma > 0: %s" % (P.name, ok))
print("   BOUNDARY B = (1 - s) a with a finite slope at zero: 0 < Sigma < inf but the supremum is NOT attained")
Q = blib.quad()
s = 0.3
B = (1 - s) * Q.a
print("   quadratic pair, s = 0.3, B = 0.7: closed form (1 - s)(2 - e) for e <= 1: sup = %.3f = Sigma, ratio at e = 1e-1, 1e-3, 1e-6: %.6f %.6f %.6f"
      % (2 * (1 - s), (B - (1 - s) * Q.theta(0.1)) / 0.1, (B - (1 - s) * Q.theta(1e-3)) / 1e-3, (B - (1 - s) * Q.theta(1e-6)) / 1e-6))
E = blib.expo()
B = (1 - s) * E.a
print("   exp(-2e), s = 0.3, B = 0.7: sup = (1 - s)*2 = %.3f, ratio at e = 1e-1, 1e-3, 1e-6: %.6f %.6f %.6f (strictly below)"
      % (2 * (1 - s), (B - (1 - s) * E.theta(0.1)) / 0.1, (B - (1 - s) * E.theta(1e-3)) / 1e-3, (B - (1 - s) * E.theta(1e-6)) / 1e-6))

print("== (Sigma4) subgradient inequality at a maximiser e1 of (B1, s1)")
for P in pairs:
    worst = 0.0
    for _ in range(300):
        s1 = rng.uniform(0, 0.9)
        B1 = rng.uniform(0.2, 0.95) * (1 - s1) * P.a
        e1, v1 = P.argmax_direct(B1, s1)
        if v1 <= 0:
            continue
        s = rng.uniform(0, 0.95)
        B = rng.uniform(0, 0.99) * (1 - s) * P.a
        rhs = v1 + (B - B1) / e1 + (s - s1) * P.theta(e1) / e1
        worst = max(worst, rhs - P.sigma_direct(B, s))
    print("  %-40s max of RHS - Sigma(B, s) = %+.2e (should be <= 0 up to rounding)" % (P.name, worst))

print("== (Sigma5) D(B, s) = Sigma - s  against  min{w >= -s : Psi_s(w) >= B}, Psi direct and through J")
for P in pairs:
    w1 = w2 = 0.0
    for _ in range(60):
        s = rng.uniform(0, 0.9)
        B = rng.uniform(0.05, 0.97) * (1 - s) * P.a
        D = P.sigma_direct(B, s) - s
        w1 = max(w1, abs(D - D_via_psi(P, B, s, True)))
        w2 = max(w2, abs(D - D_via_psi(P, B, s, False)))
    # (2.1)
    w3 = 1e9
    for _ in range(400):
        s = rng.uniform(0, 0.95)
        B = rng.uniform(P.h, max(P.h, 0.99 * (1 - s) * P.a))
        if B < (1 - s) * P.a:
            w3 = min(w3, (P.sigma_direct(B, s) - s) - (B - P.h) / P.h)
    print("  %-40s |D - min w| direct %.1e, through J %.1e;   min of D - (B - h)/h over B >= h: %+.2e" % (P.name, w1, w2, w3))
print("   fixed points of s -> Sigma(B, s) against the roots of J(s) = B, for B = 0.8 h:")
for P in pairs:
    B = 0.8 * P.h
    roots = []
    for lo, hi in [(1e-9, P.L), (P.L, 1 - 1e-9)]:
        f = lambda t: P.J_direct(t) - B
        if f(lo) * f(hi) > 0:
            roots.append(None)
            continue
        for _ in range(70):
            mid = 0.5 * (lo + hi)
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
        roots.append(0.5 * (lo + hi))
    txt = "  ".join("s = %.8f: Sigma - s = %+.1e" % (t, P.sigma_direct(B, t) - t) if t is not None else "no root on this side" for t in roots)
    print("  %-40s %s" % (P.name, txt))
S = pairs[3]
print("   pair with theta(inf) = 0.1 > 0 and B = 0.05 < theta(inf): Sigma(B, 0) = %.3e (s = 0 IS a fixed point) while J(0) = %.4f != B"
      % (S.sigma_direct(0.05, 0.0), S.J_direct(0.0)))
print("   -> the sentence 'the fixed points are the solutions of J(s) = B: two for B < h' needs theta(inf) < B (wording).")
print("   multiplier at the saddle-node: Sigma(h, L) - L, the maximiser, and the two partial derivatives (central differences)")
for P in pairs:
    e, v = P.argmax_direct(P.h, P.L)
    d = 1e-5
    ds = (P.sigma(P.h, P.L + d) - P.sigma(P.h, P.L - d)) / (2 * d)
    dB = (P.sigma(P.h + d * P.h, P.L) - P.sigma(P.h - d * P.h, P.L)) / (2 * d * P.h)
    J2 = (P.J_direct(P.L + 1e-3) - 2 * P.J_direct(P.L) + P.J_direct(P.L - 1e-3)) / 1e-6
    print("  %-40s Sigma(h,L) - L = %+.1e   argmax/h = %.6f   dSigma/ds = %.6f   h dSigma/dB = %.6f   -1/J'' = %.5f vs vartheta = %.5f"
          % (P.name, P.sigma(P.h, P.L) - P.L, e / P.h, ds, P.h * dB, -1 / J2, P.vartheta))

print("== (Sigma6)  D(h + delta, L + v) h / (delta + v^2/(2 vartheta))")
vs = [-0.1, -0.03, -0.01, -0.003, -0.001, 0.0, 0.001, 0.003, 0.01, 0.03, 0.1]
for P in pairs:
    print("  %s" % P.name)
    print("     v =            " + "  ".join("%+7.3f" % v for v in vs))
    for d in [1e-2, 1e-4, 1e-6, 1e-8]:
        row = []
        for v in vs:
            D = P.sigma(P.h + d, P.L + v) - (P.L + v)
            row.append(D * P.h / (d + v * v / (2 * P.vartheta)))
        print("     delta = %.0e : " % d + "  ".join("%7.4f" % x for x in row))
print("   uniformity: sup over |v| <= eta, delta <= delta0 (grids of 41 x 9 points) of |ratio - 1|")
for P in pairs:
    row = []
    for eta, d0 in [(0.1, 1e-2), (0.03, 1e-3), (0.01, 1e-4), (0.003, 1e-5), (0.001, 1e-6)]:
        worst = 0.0
        for i in range(41):
            v = -eta + 2 * eta * i / 40
            for j in range(9):
                d = d0 * 10 ** (-j / 2.0)
                D = P.sigma(P.h + d, P.L + v) - (P.L + v)
                worst = max(worst, abs(D * P.h / (d + v * v / (2 * P.vartheta)) - 1))
        row.append(worst)
    print("  %-40s eta, delta0 = (.1,1e-2) (.03,1e-3) (.01,1e-4) (.003,1e-5) (.001,1e-6): " % P.name + "  ".join("%.4f" % x for x in row))

print("== (Sigma7) c(eta) = min{D(h, s) : 0 <= s <= s_t, |s - L| >= eta},  s_t = (L + 1 - h/a)/2")
for P in pairs:
    st = 0.5 * (P.L + 1 - P.h / P.a)
    row = []
    for eta in [0.1, 0.03, 0.01]:
        ss = [st * i / 2000 for i in range(2001)]
        vals = [(P.sigma(P.h, s) - s, s) for s in ss if abs(s - P.L) >= eta]
        row.append(min(vals))
    print("  %-40s s_t = %.4f: " % (P.name, st) + "  ".join("c = %.3e at s = %.3f" % x for x in row)
          + "   [eta^2/(2 vartheta h) = %.3e at eta = 0.01]" % (1e-4 / (2 * P.vartheta * P.h)))
