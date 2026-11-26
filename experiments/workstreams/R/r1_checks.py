"""R1: numerical checks of the statements of docs/workstreams/R_REPORT.md (floating point; nothing here is certified).

  1. (Sigma1)  joint convexity and monotonicity of the slope map                         [random midpoints]
  2. (P1)      convexity and monotonicity of the orbit curves p_j                         [second differences]
  3. (Sigma6)  D(h + delta, L + v) h / (delta + v^2/(2 vartheta)) -> 1                    [table]
  4. Lemma PT  sqrt(delta) N_t(delta) -> pi h sqrt(2 vartheta)                            [table]
  5. Proposition U:  R[T](g) <= sup_B (B - Sigma(B, W(B)) g)  for T = M_{W,b}, random convex W  [brute force on R]
  6. Proposition K:  the kinked pair, D = delta/h exactly on the flat part, p_k(h + delta) finite for
     k <= (L2 - L1) h/delta - (1 - L2) - 1
Usage: python3 r1_checks.py [seed]
"""
import math, random, sys
import numpy as np
from rlib import Gauss, Cube, Kinked

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20261126
rng = random.Random(seed)
pairs = [Gauss().setup(), Cube(1.0).setup(), Cube(2.0).setup()]
allok = True


def report(name, ok, extra=""):
    global allok
    allok = allok and ok
    print("  %-58s %s  %s" % (name, "ok" if ok else "FAILED", extra))


print("== 1. joint convexity and monotonicity of Sigma")
for P in pairs:
    worst, mono, n = 0.0, 0.0, 0
    for _ in range(4000):
        s1, s2 = rng.uniform(0, 0.95), rng.uniform(0, 0.95)
        B1, B2 = rng.uniform(0, (1 - s1) * P.a * 0.98), rng.uniform(0, (1 - s2) * P.a * 0.98)
        lam = rng.uniform(0.05, 0.95)
        Bm, sm = lam * B1 + (1 - lam) * B2, lam * s1 + (1 - lam) * s2
        v1, v2, vm = P.sigma(B1, s1), P.sigma(B2, s2), P.sigma(Bm, sm)
        worst = max(worst, vm - (lam * v1 + (1 - lam) * v2))
        # monotone: increase B or s a little
        dB, ds = rng.uniform(0, 0.01) * P.a, rng.uniform(0, 0.01)
        if P.regular(B1 + dB, s1 + ds):
            mono = max(mono, v1 - P.sigma(B1 + dB, s1 + ds))
        n += 1
    report("%s: Sigma(mid) - mean  (max over %d)" % (P.name, n), worst <= 1e-9, "%.2e;  monotone violation %.2e" % (worst, mono))
    allok = allok and mono <= 1e-10

print("== 2. orbit curves p_j convex and nondecreasing in B (second differences on a grid, j <= 40)")
for P in pairs:
    Bs = [P.h * 0.2 + i * (P.h * 1.6 - P.h * 0.2) / 400 for i in range(401)]
    worst, wj = 0.0, 0
    for j in [1, 2, 3, 5, 8, 12, 20, 40]:
        vals = [P.orbit(B, j)[-1] for B in Bs]
        fin = [v for v in vals if math.isfinite(v)]
        for i in range(1, len(fin) - 1):
            d2 = fin[i + 1] - 2 * fin[i] + fin[i - 1]
            sc = max(1.0, abs(fin[i]))
            if -d2 / sc > worst:
                worst, wj = -d2 / sc, j
        assert all(fin[i + 1] >= fin[i] - 1e-12 for i in range(len(fin) - 1))
    report("%s: most negative second difference" % P.name, worst <= 1e-9, "%.2e (j = %d)" % (worst, wj))

print("== 3. (Sigma6): D(h + delta, L + v) * h / (delta + v^2/(2 vartheta))")
for P in pairs:
    print("  %s" % P.name)
    for d in [1e-3, 1e-5, 1e-7]:
        row = []
        for v in [-0.03, -0.01, -0.003, 0.0, 0.003, 0.01, 0.03]:
            D = P.sigma(P.h + d * P.h, P.L + v) - (P.L + v)
            row.append(D * P.h / (d * P.h + v * v / (2 * P.vartheta)))
        print("     delta/h = %.0e : " % d + "  ".join("%.4f" % x for x in row))
    D0 = P.sigma(P.h + 1e-7 * P.h, P.L) - P.L
    report("%s: ratio at v = 0, delta/h = 1e-7" % P.name, abs(D0 * P.h / (1e-7 * P.h) - 1) < 1e-3)

print("== 4. Lemma PT: sqrt(delta) N_t(delta) / (pi h sqrt(2 vartheta)),  s_t = L + 0.05")
for P in pairs:
    cstar = math.pi * P.h * math.sqrt(2 * P.vartheta)
    row = []
    for d in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        N = P.passage(P.h + d * P.h, P.L + 0.05)
        row.append(math.sqrt(d * P.h) * N / cstar)
    print("  %s  delta/h = 1e-2 .. 1e-6 : " % P.name + "  ".join("%.5f" % x for x in row))
    report("%s: within 1 per cent at delta/h = 1e-6, increasing to 1" % P.name, abs(row[-1] - 1) < 0.01 and row[-1] > row[0])

print("== 5. Proposition U by brute force: R[M_{W,b}](g) against U(g) = sup_B (B - Sigma(B, W(B)) g)")


def prop_u(P, theta, ntrial, nB=1500, nphi=200, concave=False):
    """returns (max, min) of R_ref - U over the cases, R_ref = the bracket of R minimised over phi = g/e (grid, then
    golden section: the function is quasi-convex in e) at beta = 1e-9 g -- an UPPER estimate of R[T](g)."""
    worst, tight, cnt = -1e9, 1e9, 0
    for _ in range(ntrial):
        b = rng.uniform(0.3, 1.0) * P.a
        # random convex nondecreasing piecewise-linear W on [0, b] with values in [0, 1]
        c1, c2 = sorted([rng.uniform(0, b), rng.uniform(0, b)])
        a1, a2 = rng.uniform(0, 2 / b), rng.uniform(0, 6 / b)
        w0 = rng.choice([0.0, 0.0, rng.uniform(0, 0.3)])
        Bg = np.linspace(0, b, nB)
        W = np.maximum(w0, np.maximum(a1 * (Bg - c1), a2 * (Bg - c2)))
        if W[-1] > 1:
            W = W / W[-1] * rng.uniform(0.5, 1.0)
        if concave:
            # NEGATIVE CONTROL: a nondecreasing but concave W (not admissible in Proposition U)
            W = rng.uniform(0.3, 0.9) * np.sqrt(Bg / b)
        M = lambda x: float(np.max(Bg - W * x))
        sig = np.array([P.sigma(float(B), float(w)) for B, w in zip(Bg, W)])
        fin = np.isfinite(sig)
        for g in [rng.uniform(0.01, 1.2) * P.h for _ in range(3)]:
            U = float(np.max(Bg[fin] - sig[fin] * g))
            beta = 1e-9 * g

            def bracket(phi):
                # for nonincreasing T with x + T nondecreasing the supremum over gamma is at max(beta, mu)
                mu = phi * theta((g - beta) / phi)
                return mu + (1 - phi) * M(max(beta, mu) / (1 - phi))
            # minimise over e = g (1 + exp(z)), z in [-25, 12] (phi = g/e from 1 - 1e-11 down to 6e-6): grid, then golden
            # section (the function is quasi-convex in e, hence unimodal in z; its minimum can be a sharp V between
            # two lines, or be approached only as e -> g, i.e. phi -> 1)
            fz = lambda z: bracket(1.0 / (1.0 + math.exp(z)))
            zs = [-25 + 37 * i / nphi for i in range(nphi + 1)]
            vals = [(fz(z), i) for i, z in enumerate(zs)]
            best, ib = min(vals)
            lo, hi = zs[max(ib - 1, 0)], zs[min(ib + 1, nphi)]
            gr = (math.sqrt(5) - 1) / 2
            x1, x2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
            f1, f2 = fz(x1), fz(x2)
            for _ in range(70):
                if f1 <= f2:
                    hi, x2, f2 = x2, x1, f1
                    x1 = hi - gr * (hi - lo)
                    f1 = fz(x1)
                else:
                    lo, x1, f1 = x1, x2, f2
                    x2 = lo + gr * (hi - lo)
                    f2 = fz(x2)
            best = min(best, f1, f2)
            worst = max(worst, (best - U) / P.a)
            tight = min(tight, (best - U) / P.a)
            cnt += 1
    return worst, tight, cnt


G = pairs[0]
w, t, c = prop_u(G, G.theta_na, 60)
report("Gaussian: (R_ref - U)/a  (max, min over %d cases)" % c, True, "max %+.3e  min %+.3e" % (w, t))
gauss_w, gauss_t = w, t
C1 = pairs[1]
w, t, c = prop_u(C1, C1.theta_na, 20, nB=800)
report("cube u = 1: (R_ref - U)/a  (max, min over %d cases)" % c, True, "max %+.3e  min %+.3e" % (w, t))
cube_w, cube_t = w, t
print("     (R_ref is an upper estimate of R[T](g); Proposition U says R <= U, and its proof gives equality for the")
print("      choice beta -> 0: R_ref should agree with U up to the discretisation of W, 1e-5 a)")
report("R_ref <= U + 1e-5 a in all cases (Proposition U)", gauss_w <= 1e-5 and cube_w <= 1e-5)
report("R_ref >= U - 1e-5 a in all cases (the bound is attained)", gauss_t >= -1e-5 and cube_t >= -1e-5)
w, t, c = prop_u(G, G.theta_na, 30, concave=True)
report("NEGATIVE CONTROL, concave W (Gaussian, %d cases): the line-by-line value is exceeded" % c, w > 1e-3,
       "max (R_ref - U)/a = %+.3e  (convexity of W cannot be dropped)" % w)

print("== 6. Proposition K: the kinked pair theta = max(1 - 3e, 1/2 - e, 0)")
K = Kinked()
K.h, K.L1, K.L2 = 0.25, 0.5, 0.75
ok = True
for d in [1e-2, 1e-3, 1e-4]:
    w0 = d / K.h
    smax = K.L2 - (1 - K.L2) * w0
    for s in [0.5, 0.55, 0.6, 0.7, smax]:
        ok = ok and abs(K.sigma(K.h + d, s) - s - w0) < 1e-12
    nstar = math.floor((K.L2 - K.L1) / w0 - (1 - K.L2)) - 1
    orb = K.orbit(K.h + d, nstar + 5)
    n_fin = max(i for i, v in enumerate(orb) if math.isfinite(v))
    first_inf = n_fin + 1 if n_fin + 1 < len(orb) else None
    print("  delta = %.0e: D = delta/h on [L1, s_max]; n* = %d; p_n finite for n <= %d of %d computed; p_{n*} = %.6f <= s_max = %.6f"
          % (d, nstar, n_fin, len(orb) - 1, orb[nstar], smax))
    ok = ok and math.isfinite(orb[nstar]) and orb[nstar] <= smax + 1e-12
report("kinked pair: D = delta/h exactly; p_n finite up to n*", ok)
for k in [5, 20, 80, 320]:
    # lower bound of Proposition A by bisection: largest B with p_k(B) finite
    lo, hi = K.h, K.a
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if math.isfinite(K.orbit(mid, k)[-1]):
            lo = mid
        else:
            hi = mid
    print("  k = %4d: B_inf(k) - h = %.6e,  k (B_inf - h) = %.5f   (Proposition K: >= (L2 - L1) h k/(k + 2) = %.5f)"
          % (k, lo - K.h, k * (lo - K.h), 0.0625 * k / (k + 2)))
    allok = allok and (lo - K.h) >= 0.0625 / (k + 2) - 1e-12

print("ALL CHECKS PASS" if allok else "SOME CHECK FAILED")
