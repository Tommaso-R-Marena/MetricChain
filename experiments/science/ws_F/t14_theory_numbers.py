"""Do my profile formula and the theory division's r_mu agree?  Their output file (dcdfea6,
experiments/coordinator_checks/ratios/out_oracle_zero_types.txt), p=0.25, u=1, e=0.02, two-block profiles of type kappa:
   0.184:0.00485  0.238:0.01210  0.250:0.01294  0.292:0.01340  0.347:0.00942  0.401:0.00338
   max 0.01340 at type 0.292, (m, x1, x0) = (0.46, 0.497, 0.118).
Mine: sup of f over two-label profiles of the same type, (U) label laws unrestricted, (W) label laws in the window."""
import numpy as np, sys
from scipy.optimize import minimize
from sl import *
from prof import f_profile
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()
p, u, e = 0.25, 1.0, 0.02
_, p0, p1 = site_laws(p, u, 0.0)
def sup_type(kap, restrict):
    lo, hi = (p0[1], p1[1]) if restrict else (1e-4, 1 - 1e-4)
    best = (0.0, None)
    for m in np.linspace(0.02, 0.98, 97):
        for v0 in np.linspace(lo, hi, 121):
            v1 = (kap - (1 - m) * v0) / m
            if not (lo <= v1 <= hi): continue
            val = f_profile(p, u, 0.0, m, v0, v1, e)
            if val > best[0]: best = (val, (m, v0, v1))
    if best[1] is None: return best
    def neg(z):
        m, v0 = z
        if not (0 < m < 1 and lo <= v0 <= hi): return 1.0
        v1 = (kap - (1 - m) * v0) / m
        if not (lo <= v1 <= hi): return 1.0
        return -f_profile(p, u, 0.0, m, v0, v1, e)
    res = minimize(neg, best[1][:2], method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-13, 'maxiter': 3000})
    if -res.fun > best[0]:
        m, v0 = res.x; best = (-res.fun, (m, v0, (kap - (1 - m) * v0) / m))
    return best
P(f"window [{p0[1]:.4f}, {p1[1]:.4f}]")
P("type kappa | theirs | mine, unrestricted (m, v0, v1) | mine, window (m, v0, v1)")
for kap, th in ((0.184, 0.00485), (0.238, 0.01210), (0.250, 0.01294), (0.292, 0.01340), (0.347, 0.00942), (0.401, 0.00338)):
    a = sup_type(kap, False); b = sup_type(kap, True)
    fmt = lambda r: f"{r[0]:.5f} ({r[1][0]:.3f},{r[1][1]:.4f},{r[1][2]:.4f})" if r[1] is not None else "0 (no profile of this type with both label laws in the window has a positive value)"
    P(f"  {kap:.3f} | {th:.5f} | {fmt(a)} | {fmt(b)}")
open('out/t14_theory_numbers.txt', 'w').write('\n'.join(out) + '\n')
