"""Step 3(b)/4 -- lower bounds from site-wise labels with Markov label laws: the Lyapunov form.
(1) the transfer-operator value of the moment Lyapunov exponent against exact enumeration;
(2) the formula G_t(M_c) against the brute-force Renyi form on a chain of 8 sites;
(3) scan of G_inf(t; c) over (t, c) for p = 0.5 .. 0.1 at u = 1: lower bounds for h, a; closed form E_F for E."""
import sys, time, math, itertools
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *
from ylyap import *

t0 = time.time(); u = 1.0
print("(1) moment Lyapunov exponent: transfer operator (N = 32, 48, 64) against exact ln E_n - ln E_{n-1}, n = 13, 15")
worst = 0.0
for (kappa, eta, q, r) in [(0.4236, 0.5, 0.2, 0.5), (0.4236, 0.5, 0.5, 0.3), (0.6931, 0.5, 0.1, 0.7), (1.0986, 0.5, 0.35, 0.45),
                            (0.8, 0.25, 0.3, 2.0), (1.5, 0.1, 0.3, 5.0), (0.3, 0.05, 0.2, 12.0), (2.0, 0.3, 0.1, 3.0)]:
    Ls = [moment_lyap(kappa, eta, q, r, N) for N in (32, 48, 64)]
    e13 = moment_exact(kappa, eta, q, r, 13) - moment_exact(kappa, eta, q, r, 12)
    e15 = moment_exact(kappa, eta, q, r, 15) - moment_exact(kappa, eta, q, r, 14)
    worst = max(worst, abs(Ls[2] - e15))
    print("  kappa=%.4f eta=%.2f q=%.2f r=%5.2f : N=32 %.12f  N=48 %.12f  N=64 %.12f | exact n=13: %.12f  n=15: %.12f" % (kappa, eta, q, r, Ls[0], Ls[1], Ls[2], e13, e15))
print("  largest |operator(N=64) - exact increment at n=15| = %.2e" % worst)

print("\n(2) G_t(M_c) on a chain of n = 8 sites: Lyapunov-type formula (enumeration of bonds) against the brute-force Renyi form")
n = 8; worst = 0.0
S = np.array(list(itertools.product((1.0, -1.0), repeat=n)))          # 256 spin configurations (also the label sequences)
for p in (0.4, 0.3, 0.1):
    Kp = 0.5 * math.log((1 - p) / p); h = u / 2
    e_pi = Kp * (S[:, :-1] * S[:, 1:]).sum(axis=1)
    W = np.exp(e_pi[None, :] + h * S @ S.T)                           # rows: labels sigma, columns: s
    Z = W.sum(axis=1); P = W / Z[:, None]
    for c in (0.0, 0.3, 0.8):
        M0 = np.exp(c * (S[:, :-1] * S[:, 1:]).sum(axis=1)); M0 /= M0.sum()
        for t in (0.2, 0.5, 0.8):
            M = M0 * Z ** t; M /= M.sum()
            brute = -t * math.log(float(((M @ P ** t) ** (1 / t)).sum()))
            form = G_finite(t, c, p, u, n)
            worst = max(worst, abs(brute - form))
    # the optimal label law among ALL laws on the 256 site-wise labels (Arimoto), against the best tilted Markov law
    t = 0.45
    lo, up, Mopt, Q = renyi_F(P, t, tol=1e-10)
    bestc = max(((G_finite(t, c, p, u, n), c) for c in np.linspace(0, 1.5, 31)))
    print("  p=%.1f t=%.2f: optimal law on the 256 site-wise labels: F = [%.8f, %.8f];  best tilted Markov law: %.8f at c = %.2f;  c = 0: %.8f;  cube: %.8f"
          % (p, t, lo, up, bestc[0], bestc[1], G_finite(t, 0.0, p, u, n), n * (t * math.log(math.cosh(u / 2)) - math.log(math.cosh(t * u / 2)))))
print("  largest |brute force - formula| over 27 cases = %.2e" % worst)

print("\n(3) n -> infinity: G_inf(t; c) per site, u = 1")
hc, ac, Ec = cube_numbers(u)
print("  cube: h = %.6f, a = %.6f, E = %.6f" % (hc, ac, Ec))
res = {}
for p in (0.5, 0.4, 0.3, 0.2, 0.1):
    # h: maximise over (t, c)
    def best_c(t, grid=np.linspace(0.0, 2.5, 26)):
        vals = [G_inf(t, c, p, u) for c in grid]; i = int(np.argmax(vals))
        c, v = golden_max(lambda c: G_inf(t, c, p, u), grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)], it=30)
        return v, c
    ts = np.linspace(0.1, 0.9, 17); vals = [best_c(t)[0] for t in ts]; i = int(np.argmax(vals))
    tst, hlow = golden_max(lambda t: best_c(t)[0], ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)], it=25)
    cst = best_c(tst)[1]
    h0t, h0 = maximise_on_grid(lambda t: G_inf(t, 0.0, p, u), 0.05, 0.95, 36)
    # a: sup_t G/(1-t), evaluated near t = 1
    alow = []
    for t in (0.9, 0.99, 0.999):
        v, c = best_c(t); alow.append((v / (1 - t), c))
    a0 = G_inf(0.999, 0.0, p, u) / 0.001
    # E: G/t for small t with large c -> E_F
    Elow = max(G_inf(0.02, c, p, u) / 0.02 for c in (0.5, 1.0, 2.0, 3.0, 4.0))
    # convergence in N at the optimum
    conv = abs(G_inf(tst, cst, p, u, 48) - G_inf(tst, cst, p, u, 96))
    res[p] = (hlow, tst, cst, h0, alow, a0, E_F(p, u), Elow)
    print("  p=%.1f: h >= %.6f (t*=%.3f, c*=%.3f; N=48 vs 96: %.1e) [c=0: %.6f at t=%.3f] | a >= %.6f (t=.9, c=%.2f), %.6f (t=.99, c=%.2f), %.6f (t=.999, c=%.2f) [c=0: %.6f] | E >= E_F = %.6f  (G/t at t=.02, best c: %.6f)"
          % (p, hlow, tst, cst, conv, h0, h0t, alow[0][0], alow[0][1], alow[1][0], alow[1][1], alow[2][0], alow[2][1], a0, E_F(p, u), Elow))
print("\n  ratios to the cube:  " + "  ".join("p=%.1f: h x%.3f, a x%.3f, E x%.3f" % (p, res[p][0] / hc, max(x[0] for x in res[p][4]) / ac, res[p][6] / Ec) for p in res))
print("%.1f s" % (time.time() - t0))
