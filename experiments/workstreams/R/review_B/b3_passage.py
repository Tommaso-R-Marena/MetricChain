"""Referee B, check 3: Lemma PT (the passage time) on pairs that are neither the Gaussian pair nor the cube at u = 1.

  (a) sqrt(delta) N_t(delta) / (pi h sqrt(2 vartheta))  for delta/h = 1e-2 ... 1e-10 and two cut levels s_t
  (b) the bounded correction:  N_t(delta) - c_*/sqrt(delta)  (should stay bounded: the limit is approached like 1 - C sqrt(delta))
  (c) the mechanism of the proof for one pair and one window: with eta fixed, eps := sup |ratio - 1| of (Sigma6) measured
      on the window, kappa = 3 A (1 + eps) eta / h, Dbar = (1 + eps)(delta0 + A eta^2)/h, the proof's two-sided bound on
      n1 - n0, the increments of G, and the count outside the window.
Sigma is computed from the definition of theta (blib.sigma: tangent point by bisection, value = the ratio)."""
import math, sys
import blib

pairs = [blib.quad(), blib.cubroot(), blib.expo(), blib.shifted(), blib.cube(2.0), blib.cube(3.0)]
for P in pairs:
    P.setup()

print("== (a), (b): N_t(delta) against c_*/sqrt(delta)")
for P in pairs:
    smax = 1 - P.h / P.a
    print("  %s:  h = %.8f  L = %.6f  vartheta = %.6f  c_* = %.6f  (L, 1 - h/a) = (%.4f, %.4f)" % (P.name, P.h, P.L, P.vartheta, P.cstar, P.L, smax))
    for st in [P.L + 0.02, P.L + 0.9 * (smax - P.L)]:
        rowa, rowb = [], []
        for ex in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if P.name.startswith("cube") and ex > 8:
                continue                      # theta of the cube is evaluated by bisection: keep the run short
            d = P.h * 10.0 ** (-ex)
            N = P.passage(P.h + d, st)
            rowa.append(math.sqrt(d) * N / P.cstar)
            rowb.append(N - P.cstar / math.sqrt(d))
        print("     s_t = %.4f:  ratio   " % st + " ".join("%.5f" % x for x in rowa))
        print("                   N - c_*/sqrt(delta) " + " ".join("%+.2f" % x for x in rowb))

print("== (c): the proof's inequalities, pair (1 - sqrt e)_+^3")
P = pairs[1]
A = 1.0 / (2.0 * P.vartheta)
st = P.L + 0.5 * (1 - P.h / P.a - P.L)
for eta, delta0 in [(0.01, 1e-5), (0.003, 1e-6)]:
    # eps measured on the window (grid 201 x 13)
    eps = 0.0
    for i in range(201):
        v = -eta + 2 * eta * i / 200
        for j in range(13):
            d = delta0 * 10 ** (-j / 2.0)
            D = P.sigma(P.h + d, P.L + v) - (P.L + v)
            eps = max(eps, abs(D * P.h / (d + A * v * v) - 1))
    eps *= 1.05
    kappa = 3 * A * (1 + eps) * eta / P.h
    Dbar = (1 + eps) * (delta0 + A * eta * eta) / P.h
    # c(eta) on [0, s_t] outside the window
    c_eta = min(P.sigma(P.h, s) - s for s in [st * i / 4000 for i in range(4001)] if abs(s - P.L) >= eta)
    K = st / c_eta + 2
    print("  eta = %g, delta0 = %g: measured eps = %.4f, kappa = %.4f, Dbar = %.3e <= eta/2 = %.3e: %s, c(eta) = %.3e, K(eta) = %.1f"
          % (eta, delta0, eps, kappa, Dbar, eta / 2, Dbar <= eta / 2, c_eta, K))
    for d in [delta0, delta0 / 100, delta0 / 1e4]:
        G = lambda x: math.atan((x - P.L) * math.sqrt(A / d)) / math.sqrt(A * d)
        x, n = 0.0, 0
        n0 = n1 = None
        incmin, incmax, outside = 1e99, -1e99, 0
        while x <= st:
            if n0 is None and x >= P.L - eta:
                n0, x_n0 = n, x
            if n1 is None and x > P.L + eta:
                n1 = n
            xn = P.sigma(P.h + d, x)
            if abs(x - P.L) <= eta:
                inc = G(xn) - G(x)
                incmin, incmax = min(incmin, inc), max(incmax, inc)
            else:
                outside += 1
            x = xn
            n += 1
        N = n
        lo_inc, hi_inc = (1 - eps) / ((1 + kappa) * P.h), (1 + eps) / ((1 - kappa) * P.h)
        lo_n = (math.pi / math.sqrt(A * d) - 3 / (A * eta)) * P.h * (1 - kappa) / (1 + eps)
        hi_n = math.pi * P.h * (1 + kappa) / ((1 - eps) * math.sqrt(A * d))
        print("     delta = %.0e: N_t = %d, n1 - n0 = %d in [%.1f, %.1f]: %s;  outside the window: %d <= K: %s;  x_{n0} - (L - eta) = %.2e <= Dbar: %s"
              % (d, N, n1 - n0, lo_n, hi_n, lo_n <= n1 - n0 <= hi_n, outside, outside <= K, x_n0 - (P.L - eta), x_n0 - (P.L - eta) <= Dbar))
        print("                    increments of G inside the window in [%.4f, %.4f], proof: [%.4f, %.4f]: %s;   N_t in [n1 - n0, n1 - n0 + K]: %s"
              % (incmin, incmax, lo_inc, hi_inc, lo_inc <= incmin and incmax <= hi_inc, n1 - n0 <= N <= n1 - n0 + K))
