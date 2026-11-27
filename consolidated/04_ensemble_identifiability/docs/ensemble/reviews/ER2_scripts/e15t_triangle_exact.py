#!/usr/bin/env python3
"""ER2: E15T, "the bound holds without frustration, and only then" -- is 'only then' true?

Independent of linear programming.  For uniform slopes b the class {w : w(x^(i)) <= e^b w(x)} is a cone whose
extreme rays are w = exp(-b g), g an integer height function on the cube with |g(x) - g(y)| <= 1 on edges and
a connected graph of tight edges (38 of them for three sites; enumerated here by brute force over all integer
functions -- this is Theorem E13(a), which survived the attack in e13_polytope.py and is re-checked below
against the LP).  TV(mu, mu*) - sum_i [mu*_i - mu_i] is convex in mu and the population excess is linear, so
their maxima over the class are attained at the vertices mu_g ~ pi exp(-b g).  Evaluated with mpmath at 40
digits.
"""
import itertools, sys
import mpmath as mp
mp.mp.dps = 40

n = 3
X = list(itertools.product((1, -1), repeat=n))          # spins; centre a = (+,+,+); e_i = (1 - x_i)/2
N = len(X); idx = {x: k for k, x in enumerate(X)}
edges = [(i, j) for i in range(N) for j in range(i + 1, N) if sum(a != b for a, b in zip(X[i], X[j])) == 1]
heights = []
for vals in itertools.product(range(-3, 4), repeat=N - 1):
    g = (0,) + vals
    if any(abs(g[i] - g[j]) > 1 for i, j in edges):
        continue
    parent = list(range(N))
    def find(u):
        while parent[u] != u:
            u = parent[u]
        return u
    for i, j in edges:
        if abs(g[i] - g[j]) == 1:
            parent[find(i)] = find(j)
    if len({find(u) for u in range(N)}) == 1:
        heights.append(g)
assert len(heights) == 38


def analyse(J12, J23, J13, h, b):
    b = mp.mpf(b)
    logpi = [mp.mpf(J12) * x[0] * x[1] + mp.mpf(J23) * x[1] * x[2] + mp.mpf(J13) * x[0] * x[2]
             + sum(mp.mpf(hi) * xi for hi, xi in zip(h, x)) for x in X]
    pi = [mp.e ** v for v in logpi]
    e = [[(1 - xi) // 2 for xi in x] for x in X]
    star = [p * mp.e ** (-b * sum(ei)) for p, ei in zip(pi, e)]; Z = sum(star); star = [s / Z for s in star]
    mstar = [sum(s for s, ei in zip(star, e) if ei[i] == 0) for i in range(n)]
    # log-supermodularity of pi in e: pair couplings 4 J_ij a_i a_j >= 0
    worst_tv = mp.mpf("-inf"); worst_pop = mp.mpf("-inf"); eq = 0
    for g in heights:
        mu = [p * mp.e ** (-b * gi) for p, gi in zip(pi, g)]; Zm = sum(mu); mu = [m / Zm for m in mu]
        tv = sum(abs(m - s) for m, s in zip(mu, star)) / 2
        marg = [sum(m for m, ei in zip(mu, e) if ei[i] == 0) for i in range(n)]
        exc = tv - sum(ms - mg for ms, mg in zip(mstar, marg))
        worst_tv = max(worst_tv, exc); worst_pop = max(worst_pop, max(mg - ms for ms, mg in zip(mstar, marg)))
        eq += abs(exc) < mp.mpf(10) ** (-30)
    return worst_tv, worst_pop, eq


print("three sites, pi ~ exp(J12 x1x2 + J23 x2x3 + J13 x1x3 + h.x), centre a = (+,+,+), slopes b; 38 vertices, 40 digits")
print("   J12   J23    J13     h              b     max over the class of TV - sum_i[mu*_i - mu_i]    max population excess    vertices with equality")
cases = [(1, 1, 0.25, (0, 0, 0), 1), (1, 1, 0, (0, 0, 0), 1),
         (1, 1, -0.05, (0.05, -1, 0.05), 1),          # the LP example of e15t_interacting.py (K = 4, kappa = 0.2, field -2)
         (1, 1, -0.05, (0, 0, 0), 1), (1, 1, -0.1, (0, 0, 0), 1), (1, 1, -0.25, (0, 0, 0), 1), (1, 1, -0.5, (0, 0, 0), 1),
         (2, 2, -0.25, (0, 0, 0), 1), (0.5, 0.5, -0.1, (0, 0, 0), 1), (0.5, 0.5, -0.1, (0, 0, 0), 2), (1, 1, -0.1, (0, 0, 0), 0.5),
         (0, 0, -0.5, (0, 0, 0), 1), (1, -0.5, 0, (0, 0, 0), 1)]
for J12, J23, J13, h, b in cases:
    tvx, popx, eq = analyse(J12, J23, J13, h, b)
    viol = "violated bond" if min(J12, J23, J13) < 0 else "all bonds satisfied"
    print(f"   {J12:4} {J23:5} {J13:6}   {str(h):14} {b:4}    {mp.nstr(tvx, 6):>12}                                   {mp.nstr(popx, 6):>12}            {eq:2d}     ({viol})")
