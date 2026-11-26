"""r10_06: the Markov recursion ("DP") upper bound, Proposition F of Y_REPORT 5.1, re-derived
(R10_REPORT section 2) and re-evaluated with own code.

    F_inf(t) <= F^DP_L(t)/L,   F^DP_L = F*[ P^(L)(. | previous letter +); slopes (u,...,u,u*) ],
    u* = u + g(u*),  g(x) = ln[ ((1-p)e^x + p) / (p e^x + 1 - p) ].

 1. the fixed point u*;
 2. L = 1, 2, 3 at u = 1, p in {0.4,0.3,0.2,0.1}: h <= max_t, a <=, E <=  (all vertices of the
    weighted block polytope; duality brackets);
 3. a direct test of the finite-n inequality F*_n(t) <= sum_i max_b F*[P_i(b,.); d*_i](t)
    against the exact F*_n (all vertices), n <= 4.
usage: python3 r10_06_markov_recursion.py [u ...]
"""
import sys
import time
import numpy as np
from r10lib import *


def ustar(p, u, iters=10000):
    x = u
    for _ in range(iters):
        x = u + np.log(((1 - p) * np.exp(x) + p) / (p * np.exp(x) + 1 - p))
    return x


def ustar_seq(p, u, n):
    """d*_n = u, d*_i = u + g(d*_{i+1}): slopes for sites i = n, n-1, ..., 1 (returned for 1..n)."""
    xs = [u]
    for _ in range(n - 1):
        xs.append(u + np.log(((1 - p) * np.exp(xs[-1]) + p) / (p * np.exp(xs[-1]) + 1 - p)))
    return xs[::-1]


def cond_block_law(L, p, b=0):
    """P(x_1..x_L | previous letter b) for the binary symmetric chain."""
    x = bits(L)
    prev = np.concatenate([np.full((1 << L, 1), b), x[:, :-1]], axis=1)
    fl = (x != prev).sum(axis=1)
    return p ** fl * (1 - p) ** (L - fl)


def dp_block(p, u, L, us=None):
    us = ustar(p, u) if us is None else us
    slopes = [u] * (L - 1) + [us]
    V = cube_vertices_weighted(slopes)
    pi = cond_block_law(L, p, 0)
    W, _ = gibbs(pi, V)
    return W, len(V)


def exponents_from_W(W, per):
    low = lambda t: renyi_bracket(W, t, tol=1e-11)["lower"]
    tb, _ = golden_max(low, 0.05, 0.95, tol=1e-6)
    br = renyi_bracket(W, tb, tol=1e-12)
    ca = capacity_bracket(W, tol=1e-12)
    th = threshold_bracket(W, tol=1e-12)
    return (tb, br["lower"] / per, br["upper"] / per, ca["lower"] / per, ca["upper"] / per, th["lower"] / per, th["upper"] / per)


if __name__ == "__main__":
    t0 = time.time()
    us_list = [float(a) for a in sys.argv[1:]] or [1.0]
    theirs_us = {0.4: 1.218, 0.3: 1.526, 0.2: 1.981, 0.1: 2.750}
    theirs = {0.4: ((0.04053, 0.03889, 0.03736), 0.12970, (0.16935, 0.16921, 0.16917)),
              0.3: ((0.05484, 0.05180, 0.04902), 0.15401, (0.23419, 0.23324, 0.23285)),
              0.2: ((0.07202, 0.06672, 0.06197), 0.17747, (0.31886, 0.31554, 0.31376)),
              0.1: ((0.09157, 0.08299, 0.07542), 0.19678, (0.43245, 0.42378, 0.41799))}
    for u in us_list:
        hc, tc, ac, Ec = cube_exponents(u)
        print("u = %.2f   cube: h=%.6f a=%.6f E=%.6f" % (u, hc, ac, Ec))
        for p in (0.4, 0.3, 0.2, 0.1):
            us = ustar(p, u)
            K = np.log((1 - p) / p)
            print("p=%.1f  u*=%.4f (Y: %s)  g(u*)=%.4f < K=%.4f   E_F=%.6f" % (p, us, theirs_us.get(p) if u == 1.0 else "-", us - u, K, E_F(p, u)))
            for L in (1, 2, 3):
                W, nv = dp_block(p, u, L, us)
                tb, hl, hu, al, au, el, eu = exponents_from_W(W, L)
                ref = ""
                if u == 1.0:
                    ref = "   Y: h<=%.5f%s E<=%.5f" % (theirs[p][0][L - 1], (" a<=%.5f" % theirs[p][1]) if L == 3 else "", theirs[p][2][L - 1])
                print("   L=%d (%3d vertices): h <= %.6f (t=%.3f; bracket %.1e)  a <= %.6f  E <= %.6f%s   | h/cube %.3f"
                      % (L, nv, hu, tb, hu - hl, au, eu, ref, hu / hc))
        print()

    # 3. finite-n inequality against exact F*_n
    print("3. finite-n test: F*_n(t) <= F*[pi_1; d*_1](t) + sum_{i>=2} F*[P(+,.); d*_i](t)   (exact F*_n over all vertices)")
    worst = 1e9
    cnt = 0
    for p in (0.4, 0.3, 0.1):
        for n in (2, 3, 4):
            pi = binary_chain_law(n, p)
            Wn, _ = gibbs(pi, hom_vertices(n).astype(float))
            ds = ustar_seq(p, 1.0, n)
            for t in (0.25, 0.45, 0.65, 0.85):
                Fn = renyi_bracket(Wn, t, tol=1e-12)["upper"]
                rhs = 0.0
                for i, d in enumerate(ds):
                    law = np.array([0.5, 0.5]) if i == 0 else np.array([1 - p, p])
                    Wi, _ = gibbs(law, cube_vertices_weighted([d]))
                    rhs += renyi_bracket(Wi, t, tol=1e-12)["upper"]
                worst = min(worst, rhs - Fn)
                cnt += 1
    print("   %d cases, smallest (bound - exact) = %.5f  (must be >= 0)" % (cnt, worst))
    print("time %.1fs" % (time.time() - t0))
