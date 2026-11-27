"""N3: the instance-wise exponent with the oracle at additive instances (zero residual first).
   lower bounds:  plain dips of the forced centre type;  constrained sup over binary-label profiles (annular dips);
   upper bound:   the tilt bound  min_lambda R_gamma(e - c(lambda); theta - lambda)."""
import numpy as np, sys
from sl import *
from prof import *
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()

P("check: f at the plain-dip profile equals Rcc; unconstrained sup over profiles equals R_gamma")
for (p,u,g,fr) in ((0.3,1.0,0.0,0.2),(0.1,2.0,0.0,0.1),(0.1,2.0,-0.5,0.3),(0.5,1.0,0.0,0.2)):
    E0 = F_game(p,u,g,1e-6)/1e-6
    e = fr*E0
    _, p0, p1 = site_laws(p,u,0.0)
    for m in (0.3,0.5,0.7):
        P(f"   p={p} u={u} g={g} e={fr}E_g m={m}: f_profile(plain)={f_profile(p,u,g,m,p0[1],p1[1],e):.8f}  Rcc={Rcc(p,u,g,m,e):.8f}")
    sp = sup_profiles(p,u,g,e,grid=25)
    P(f"   sup over profiles = {sp[0]:.8f} at (m,v0,v1)=({sp[1][0]:.4f},{sp[1][1]:.5f},{sp[1][2]:.5f}); window=({p0[1]:.5f},{p1[1]:.5f}); R_gamma = {R_gamma(p,u,g,e):.8f}")

P("\nZERO RESIDUAL with a field.  columns: p u e/E_0 | R_0(e) no oracle | plain dips, forced type m_0: Rcc(0,m_0) | constrained sup over binary profiles (m,v0,v1) | tilt upper bound (lambda*) | ratio tilt/R_0")
for (p,u) in ((0.5,1.0),(0.3,1.0),(0.1,2.0),(0.1,1.0),(0.05,3.0),(0.2,0.5)):
    E0 = F_game(p,u,0.0,1e-6)/1e-6
    m0 = m_forced(p,u,0.0)
    for fr in (0.0,0.1,0.2,0.3,0.5,0.7):
        e = fr*E0
        r0 = R_gamma(p,u,0.0,e)
        rd = Rcc(p,u,0.0,m0,e)
        sc = sup_profiles(p,u,0.0,e,constrained=True,grid=31)
        tb, lam = tilt_bound(p,u,0.0,e,return_lam=True)
        P(f"{p:5.2f} {u:4.1f} {fr:3.1f} | {r0:.6f} | {rd:.6f} (m_0={m0:.4f}) | {sc[0]:.6f} at ({sc[1][0]:.3f},{sc[1][1]:.4f},{sc[1][2]:.4f}) | {tb:.6f} (lam={lam:+.4f}) | {tb/r0 if r0>0 else float('nan'):.4f}")
open('out/t04_instance.txt','w').write('\n'.join(out)+'\n')
