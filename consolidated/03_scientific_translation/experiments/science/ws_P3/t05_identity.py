"""
P3 test 5: numerical check of Proposition 1 (remainder identity of the anchored expansion) on fully
enumerated grids, for the real g_GB and for a random function:
   g(x) - sum_{T subset S(x), |T| < m} d_T(x_T) = sum_{T subset S(x), |T| = m} Delta_T g(z^{T,x}; x_T),
   z^{T,x} = (x on the sites < min T, x0 elsewhere),
for every x and every m.  Also checks the Leibniz/chain-rule Corollary L1 on a random additive u.
"""
import sys, itertools
import numpy as np
from p3core import GBModel


def delta(g, base, T, y):
    """Delta_T g(base; y_T) = sum_{U subset T} (-1)^{|T|-|U|} g(base with U replaced by y)."""
    tot = 0.0
    for r in range(len(T) + 1):
        for U in itertools.combinations(T, r):
            z = list(base)
            for i in U:
                z[i] = y[i]
            tot += (-1) ** (len(T) - r) * g[tuple(z)]
    return tot


def check(g, x0, rng, nx=40):
    n = g.ndim
    worst = 0.0
    for _ in range(nx):
        x = tuple(int(rng.integers(0, k)) for k in g.shape)
        S = [i for i in range(n) if x[i] != x0[i]]
        for m in range(1, len(S) + 1):
            lhs = g[x] - sum(delta(g, x0, T, x) for r in range(m) for T in itertools.combinations(S, r))
            rhs = 0.0
            for T in itertools.combinations(S, m):
                z = [x[i] if i < min(T) else x0[i] for i in range(n)]
                rhs += delta(g, z, T, x)
            worst = max(worst, abs(lhs - rhs))
    return worst


rng = np.random.default_rng(11)
G = GBModel("V6", "P2", tau=0.70)
g = G.energy(G.product_states()).reshape(G.k)
x0 = tuple(int(v) for v in np.unravel_index(np.argmin(g), g.shape))
print("remainder identity, g_GB of Val6/PPII (729 states), 40 random x, all m: max |lhs - rhs| =", f"{check(g, x0, rng):.2e}", "kcal/mol")
r = rng.normal(size=(3, 4, 2, 3, 3))
print("remainder identity, random function on a 3x4x2x3x3 grid, anchor (1,2,0,1,2):           max |lhs - rhs| =", f"{check(r, (1, 2, 0, 1, 2), rng):.2e}")
# Corollary L1: |Delta_T phi(c + sum a_i)| <= sup|phi^(m)| prod |a_i(y_i) - a_i(z_i)|, phi = tanh
worst = -np.inf
for _ in range(2000):
    m = int(rng.integers(1, 5))
    a0 = rng.normal(size=m); a1 = rng.normal(size=m) * 0.3 + a0
    c = rng.normal()
    val = 0.0
    for bits in itertools.product((0, 1), repeat=m):
        u = c + sum(a1[i] if b else a0[i] for i, b in enumerate(bits))
        val += (-1) ** (m - sum(bits)) * np.tanh(u)
    lo = c + np.minimum(a0, a1).sum(); hi = c + np.maximum(a0, a1).sum()
    t = np.tanh(np.linspace(lo, hi, 4001)); s = 1 - t * t
    der = [None, s, -2 * t * s, 2 * s * (3 * t * t - 1), 8 * t * s * (2 - 3 * t * t)][m]
    bound = np.abs(der).max() * np.prod(np.abs(a1 - a0))
    worst = max(worst, abs(val) - bound * (1 + 1e-3))
print("Corollary L1 (phi = tanh, orders 1..4, 2000 random cases): max(|Delta| - bound) =", f"{worst:.2e}", "(must be <= 0)")
