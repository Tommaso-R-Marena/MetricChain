"""The theory division's number for Proposition 11.109(e) (commit dcdfea6): p = 1/4, u = 1, e = 0.02:
   'rho_e(kappa) unimodal, 0.0134 at kappa ~ 0.29 and 0.0129 at kappa = p'.
   My quantities at the same point."""
import numpy as np, sys
from sl import *
from prof import *
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()
p, u, e = 0.25, 1.0, 0.02
E0 = F_game(p, u, 0.0, 1e-6) / 1e-6
r0, t0 = R_gamma(p, u, 0.0, e, return_t=True)
r0c, mstar = R0_closed(p, u, e, return_m=True)
m0 = m_forced(p, u, 0.0)
P(f"p={p} u={u} e={e} (E_0={E0:.6f}, e/E_0={e/E0:.4f})")
P(f"R_0(e) = {r0:.6f} (closed form max_m: {r0c:.6f} at centre type m*={mstar:.4f}; excess (cone) density at m*: {cone_density(p,u,mstar):.5f})   [theirs: 0.0134 at type ~0.29]")
P(f"(a) plain dips, forced centre type m_0={m0:.4f}: Rcc = {Rcc(p,u,0.0,m0,e):.6f}")
sc = sup_profiles(p, u, 0.0, e, constrained=True, grid=41)
P(f"(b) constrained sup over binary annular profiles: {sc[0]:.6f} at (m,v0,v1)=({sc[1][0]:.4f},{sc[1][1]:.5f},{sc[1][2]:.5f})   [theirs: rho_e(p) = 0.0129]")
tb, lam = tilt_bound(p, u, 0.0, e, return_lam=True)
P(f"(c) tilt upper bound: {tb:.6f} at lambda={lam:+.4f}")
P(f"decrease: (b) {100*(1-sc[0]/r0):.2f} %, (c) {100*(1-tb/r0):.2f} %   [theirs: about 3.5 %]")
# type-resolved profile exponent rho_e(kappa) = sup over binary annular profiles with core density kappa
P("type-resolved sup over binary annular profiles, rho_e(kappa):")
_, p0, p1 = site_laws(p, u, 0.0)
for kap in (0.20, 0.22, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.30, 0.31, 0.32, 0.34):
    best = 0.0
    for m in np.linspace(0.02, 0.98, 97):
        for v0 in np.linspace(p0[1], p1[1], 121):
            v1 = (kap - (1 - m) * v0) / m
            if not (p0[1] <= v1 <= p1[1]): continue
            best = max(best, f_profile(p, u, 0.0, m, v0, v1, e))
    P(f"   kappa={kap:.2f}: {best:.6f}")
open('out/t10_theory_e.txt', 'w').write('\n'.join(out) + '\n')
