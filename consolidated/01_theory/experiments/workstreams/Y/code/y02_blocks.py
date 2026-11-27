"""Step 3(a),(b) -- block bounds for the binary symmetric chain at slope u = 1, blocks of L = 1, 2, 3 sites, ALL vertices of the
block's Lipschitz polytope (complete enumeration by spanning trees of tight edges).

 (U)   upper, algorithmic:  block law = stationary L-marginal, slopes (u+K, u, .., u, u+K)  [L=1: u+2K];   per site: divide by L
 (DP)  upper, on the game function: block law = P(. | previous letter), slopes (u, .., u, u*), u* = u + g(u*);   divide by L
 (L')  lower: block law = stationary L-marginal, slopes (u-kappa_m, u, .., u, u-kappa_m) [L=1: u-2kappa_m];     divide by L+m
 (L)   lower, accuracy version: plain block (slopes u), accuracy shifted by kappa_m per block;                    divide by L+m
 plain: stationary L-marginal with slopes u (neither bound; F_inf is within t*K/L of it)
Every number is a duality bracket [lower, upper]."""
import sys, time, math
import os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ylib import *

t0 = time.time(); u = 1.0
hc, ac, Ec = cube_numbers(u)
print("cube: h=%.6f a=%.6f E=%.6f" % (hc, ac, Ec))
fmt = lambda b: "[%.6f,%.6f]" % (b[0], b[1])
rows = []
PS = [float(x) for x in sys.argv[1:]] or [0.5, 0.4, 0.3, 0.2, 0.1]
for p in PS:
    K = math.log((1 - p) / p); lam = 1 - 2 * p; us = ustar(u, p)
    print("\n=== p = %.1f   K = %.4f   u* = %.4f  (one-sided slack g(u*) = %.4f)" % (p, K, us, us - u))
    for L in (1, 2, 3):
        pi = bsc_block_law(L, p)
        # plain
        h, a, E = haE_mult(pi, lip_vertices([u] * L), L)
        print("plain L=%d            h=%s a=%s E=%s" % (L, fmt(h), fmt(a), fmt(E)))
        rows.append((p, "plain", L, 0, h[0], h[1], a[0], a[1], E[0], E[1]))
        # (U)
        w = [u + 2 * K] if L == 1 else [u + K] + [u] * (L - 2) + [u + K]
        V = lip_vertices(w); h, a, E = haE_mult(pi, V, L)
        print("(U)   L=%d |V|=%4d   h=%s a=%s E=%s" % (L, len(V), fmt(h), fmt(a), fmt(E)))
        rows.append((p, "U", L, 0, h[0], h[1], a[0], a[1], E[0], E[1]))
        # (DP)
        w = [u] * (L - 1) + [us]
        V = lip_vertices(w); h, a, E = haE_mult(bsc_block_law_cond(L, p, 0), V, L)
        print("(DP)  L=%d |V|=%4d   h=%s a=%s E=%s" % (L, len(V), fmt(h), fmt(a), fmt(E)))
        rows.append((p, "DP", L, 0, h[0], h[1], a[0], a[1], E[0], E[1]))
        # (L') and (L)
        Pplain = gibbs_rows(pi, lip_vertices([u] * L)); Gp = GameFunction(Pplain, 1.0, tol=1e-9)
        Eplain = E_threshold(Pplain)
        for m in range(0, 6):
            kap = math.log((1 + lam ** (m + 1)) / (1 - lam ** (m + 1))) if p != 0.5 else 0.0
            red = 2 * kap if L == 1 else kap
            if u - red > 1e-9:
                w = [u - 2 * kap] if L == 1 else [u - kap] + [u] * (L - 2) + [u - kap]
                V = lip_vertices(w); h, a, E = haE_mult(pi, V, L + m)
                s1 = "(L')  L=%d m=%d |V|=%3d h=%s a=%s E=%s" % (L, m, len(V), fmt(h), fmt(a), fmt(E))
                rows.append((p, "Lp", L, m, h[0], h[1], a[0], a[1], E[0], E[1]))
            else:
                s1 = "(L')  L=%d m=%d  not available (kappa_m = %.3f too large)" % (L, m, kap)
            # (L): max_t [F_L(t) - t kappa_m]/(L+m);  E >= (E_L - kappa_m)/(L+m);  a-type: theta_na(kappa_m)/(L+m)
            tt, lo = maximise_on_grid(lambda t: Gp.F(t)[0] - t * kap, 0.05, 0.95, 18, it=28); up = Gp.F(tt)[1] - tt * kap
            lo, up = max(lo, 0.0), max(up, 0.0)
            tn, nlo = maximise_on_grid(lambda t: (Gp.F(t)[0] - t * kap) / (1 - t), 0.05, 0.99, 47, it=28); nup = (Gp.F(tn)[1] - tn * kap) / (1 - tn)
            nlo, nup = max(nlo, 0.0), max(nup, 0.0)
            rows.append((p, "L", L, m, lo / (L + m), up / (L + m), nlo / (L + m), nup / (L + m), max(Eplain[0] - kap, 0) / (L + m), max(Eplain[1] - kap, 0) / (L + m)))
            print(s1 + "   || (L): h>=%.6f a>=%.6f E>=%.6f" % (lo / (L + m), nlo / (L + m), max(Eplain[0] - kap, 0) / (L + m)))
            if p == 0.5: break
import pickle
pickle.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "y02_rows_%s.pkl" % "_".join(str(x) for x in PS)), "wb"))

print("\n==== summary: best bounds from blocks L <= 3 (per site), cube values h=%.6f a=%.6f E=%.6f" % (hc, ac, Ec))
print("  p   | h: lower(L')  lower(L)  upper(DP)  upper(U) | a: lower(L')  lower(L)  upper(DP)  upper(U) | E: lower(L')  lower(L)  upper(DP)  upper(U)")
for p in PS:
    def best(kind, col, f):
        v = [r[col] for r in rows if r[0] == p and r[1] == kind]
        return f(v) if v else float("nan")
    print(" %.1f  |   %.6f   %.6f   %.6f   %.6f |   %.6f   %.6f   %.6f   %.6f |   %.6f   %.6f   %.6f   %.6f" % (
        p, best("Lp", 4, max), best("L", 4, max), best("DP", 5, min), best("U", 5, min),
        best("Lp", 6, max), best("L", 6, max), best("DP", 7, min), best("U", 7, min),
        best("Lp", 8, max), best("L", 8, max), best("DP", 9, min), best("U", 9, min)))
print("%.1f s" % (time.time() - t0))
