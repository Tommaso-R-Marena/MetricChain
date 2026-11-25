"""Is the theory division's rho_e(p) (two-block profiles of type p, cores NOT restricted to the window)
equal to my tilt bound?  And where does the excess mass of an unstable-core dip really sit?"""
import numpy as np, sys
from scipy.optimize import minimize
from sl import *
from prof import *
from ts import Grid
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()

def sup_free(p, u, e, kap, restrict):
    _, p0, p1 = site_laws(p, u, 0.0)
    lo, hi = (p0[1], p1[1]) if restrict else (1e-4, 1 - 1e-4)
    best = (0.0, None)
    for m in np.linspace(0.02, 0.98, 97):
        for v0 in np.linspace(lo, hi, 161):
            v1 = (kap - (1 - m) * v0) / m
            if not (lo <= v1 <= hi): continue
            val = f_profile(p, u, 0.0, m, v0, v1, e)
            if val > best[0]: best = (val, (m, v0, v1))
    def neg(z):
        m, v0 = z
        if not (0 < m < 1 and lo <= v0 <= hi): return 1.0
        v1 = (kap - (1 - m) * v0) / m
        if not (lo <= v1 <= hi): return 1.0
        return -f_profile(p, u, 0.0, m, v0, v1, e)
    res = minimize(neg, best[1][:2], method='Nelder-Mead', options={'xatol': 1e-11, 'fatol': 1e-14, 'maxiter': 4000})
    if -res.fun > best[0]:
        m, v0 = res.x; best = (-res.fun, (m, v0, (kap - (1 - m) * v0) / m))
    return best

for (p, u, e) in ((0.25, 1.0, 0.02), (0.1, 2.0, 0.2 * 0.201795), (0.3, 1.0, 0.0)):
    _, p0, p1 = site_laws(p, u, 0.0)
    a = sup_free(p, u, e, p, True); b = sup_free(p, u, e, p, False)
    tb, lam = tilt_bound(p, u, 0.0, e, return_lam=True)
    P(f"p={p} u={u} e={e:.5f}: window [{p0[1]:.5f},{p1[1]:.5f}]")
    P(f"   sup over two-block profiles of type p, cores in the window : {a[0]:.6f} at (m,v0,v1)=({a[1][0]:.4f},{a[1][1]:.5f},{a[1][2]:.5f})")
    P(f"   sup over two-block profiles of type p, cores unrestricted  : {b[0]:.6f} at (m,v0,v1)=({b[1][0]:.4f},{b[1][1]:.5f},{b[1][2]:.5f})")
    P(f"   tilt bound min_lambda R_0(e - c(lambda); theta - lambda)   : {tb:.6f} at lambda={lam:+.4f};  tilted cone laws: ({1/(1+np.exp(-(np.log(p/(1-p))+lam-u))):.5f}, {1/(1+np.exp(-(np.log(p/(1-p))+lam+u))):.5f})")

P("\nWhere the excess mass of an unstable-core annular dip sits (exact sums, zero residual):")
from t07_zero_residual_annular import ann
for (n, p, u, k, j1, j0, lift) in ((400, 0.25, 1.0, 180, 76, 10, 30.0), (400, 0.25, 1.0, 180, 76, 24, 30.0), (800, 0.1, 2.0, 280, 72, 0, 40.0), (800, 0.1, 2.0, 280, 72, 8, 40.0)):
    G = Grid(n, p, u, k)
    E, cE, D = ann(G, 0.0, j1, j0, lift)
    _, p0, p1 = site_laws(p, u, 0.0)
    P(f"   n={n} p={p} u={u} k={k} shell (j1,j0)=({j1},{j0}): label-0 core density {j0/(n-k):.4f} (window lower end {p0[1]:.4f}); shell type {(j1+j0)/n:.5f}; TRUE excess density {cE:.5f}; ln E = {np.log(E):.2f}")
open('out/t11_unrestricted_profiles.txt', 'w').write('\n'.join(out) + '\n')
