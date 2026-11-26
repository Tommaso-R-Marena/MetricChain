"""r10_15: sanity checks of the large-slope reversal on FINITE chains with ALL vertices.
 1. block form of Proposition F against exact values: n = 4 = two blocks of 2,
        F*_4(t) <= F*[pi_2; (u,u*)](t) + F*[P^(2)(.|+); (u,u*)](t),   a_4 <= the same with capacities.
 2. exact a_n, increments a_n - a_{n-1} and F*_n(t) increments against the cube (n <= 5; n = 5 by
    column generation over all 395094 vertices) -- finite chains, indicative only.
"""
import time
import numpy as np
from r10lib import *
from r10_06_markov_recursion import ustar, cond_block_law

t0 = time.time()
V = {n: hom_vertices(n).astype(float) for n in (1, 2, 3, 4)}
print("1. block form of the Markov recursion against exact values (n=4, all 990 vertices)")
worst = 1e9
for u in (1.0, 3.0, 4.0, 6.0):
    for p in (0.3, 0.1):
        us = ustar(p, u)
        Vb = cube_vertices_weighted([u, us])
        W1, _ = gibbs(binary_chain_law(2, p), Vb)
        W2, _ = gibbs(cond_block_law(2, p, 0), Vb)
        W4, _ = gibbs(binary_chain_law(4, p), u * V[4])
        a_ex = capacity_bracket(W4, tol=1e-11)["upper"]
        a_bd = capacity_bracket(W1, tol=1e-12)["upper"] + capacity_bracket(W2, tol=1e-12)["upper"]
        worst = min(worst, a_bd - a_ex)
        row = "u=%.0f p=%.1f: a_4 = %.6f <= %.6f" % (u, p, a_ex, a_bd)
        for t in (0.3, 0.5):
            f_ex = renyi_bracket(W4, t, tol=1e-11)["upper"]
            f_bd = renyi_bracket(W1, t, tol=1e-12)["upper"] + renyi_bracket(W2, t, tol=1e-12)["upper"]
            worst = min(worst, f_bd - f_ex)
            row += " | F*_4(%.1f) = %.6f <= %.6f" % (t, f_ex, f_bd)
        print("   " + row)
print("   smallest (bound - exact): %.5f (must be >= 0)" % worst)

print("2. exact finite chains against the cube (per site; increments)")
for u in (3.0, 4.0):
    hc, tc, ac, Ec = cube_exponents(u)
    for p in (0.3, 0.1):
        an = {}; fn = {}
        for n in (1, 2, 3, 4):
            W, _ = gibbs(binary_chain_law(n, p), u * V[n])
            an[n] = capacity_bracket(W, tol=1e-11)
            fn[n] = renyi_bracket(W, tc, tol=1e-11)
        nonadd = an[4]["M"]
        print("   u=%.0f p=%.1f: a_n/n = %s ; increments a_n - a_{n-1} = %s ; cube a = %.6f" % (
            u, p, " ".join("%.6f" % (an[n]["upper"] / n) for n in (1, 2, 3, 4)),
            " ".join("%.6f" % (an[n]["upper"] - an[n - 1]["upper"]) for n in (2, 3, 4)), ac))
        print("              F*_n(t_cube=%.3f)/n = %s ; increments = %s ; cube F = h = %.6f" % (
            tc, " ".join("%.6f" % (fn[n]["upper"] / n) for n in (1, 2, 3, 4)),
            " ".join("%.6f" % (fn[n]["upper"] - fn[n - 1]["upper"]) for n in (2, 3, 4)), hc))
print("time %.0fs" % (time.time() - t0))
