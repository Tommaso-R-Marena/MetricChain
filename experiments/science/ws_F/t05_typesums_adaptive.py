"""N4: exact type-class sums, n = 100 ... 6400: the lower bound WITH the one-body oracle (compensated base,
cyclically symmetrised dips of one exact centre type) against the classical bound without oracle and against R^max.

For each (p,u,eps1): gamma* = hardest additive instance at eps1, eps = eps1*n; scan the centre type k near m* n.
  with oracle:    E|Q| >= (1-2delta) * exp(lnLB),  lnLB = -ln n - ln max_x P_{s in T_k}(x in D_s),  depth r: ln(1+E/(1+b)) > eps
  without oracle: E|Q| >= (1-2delta) * exp(lnLB0), lnLB0 = -ln max_x P_s(x in D_s),                 depth r: ln(1+E) > eps
Everything is an exact finite sum (float64, log domain)."""
import numpy as np, sys
from sl import *
from ts import *
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()

NS = (100, 200, 400, 800, 1600, 3200)
cases = ((0.3, 1.0, 0.3), (0.1, 2.0, 0.3), (0.1, 2.0, 0.05), (0.2, 1.0, 0.5), (0.5, 1.0, 0.3), (0.05, 3.0, 0.2))
for (p, u, f) in cases:
    E = E_threshold(p, u)
    e1 = f * E
    R, t, m, Q, g = Rmax(p, u, e1, return_all=True)
    P(f"\n=== p={p} u={u} eps1={f}E={e1:.6f}: R^max={R:.6f}, gamma*={g:+.5f}, m*={m:.5f}, t*={t:.4f}; density of gamma*: {Q[1]:.5f}, cone density at m*: {cone_density(p,u,m):.5f}")
    P("   n |   k  | with oracle: lnLB/n   b      c_E      r-eps  | no oracle: lnLB0/n | (lnLB - lnLB0)  |  R^max - lnLB/n  [x n/ln n]")
    for n in NS:
        eps = e1 * n
        best = None
        k0 = int(round(m * n))
        for k in ([kk for kk in range(max(1, k0 - 6), min(n - 1, k0 + 6) + 1)] if n <= 400 else [k0 - 4, k0 - 2, k0, k0 + 2, k0 + 4]):
            G = Grid(n, p, u, k)
            B = compensated_dip(n, p, u, g, k, eps, G)
            if B['b'] < 0: continue
            if best is None or B['lnLB'] > best[1]['lnLB']:
                best = (k, B, uncompensated_dip(n, p, u, g, k, eps, G))
        k, B, U0 = best
        gap = R - B['lnLB'] / n
        P(f"{n:5d} | {k:4d} | {B['lnLB']/n:.6f}  {B['b']:.4f}  {B['cE']:.5f}  {B['r']-eps:+.4f} | {U0['lnLB']/n:.6f} | {B['lnLB']-U0['lnLB']:+.3f} | {gap:+.6f} [{gap*n/np.log(n):.3f}]")
open('out/t05_typesums_adaptive.txt', 'w').write('\n'.join(out) + '\n')
