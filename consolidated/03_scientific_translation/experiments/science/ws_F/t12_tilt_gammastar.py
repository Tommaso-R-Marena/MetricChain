"""The hardest ADDITIVE instance gamma*(e) with the oracle: tilt upper bound U_{gamma*}(e) < R^max(e) when p != 1/2.
(With the oracle the hardest instance is no longer additive: the two-component base keeps R^max.)"""
import numpy as np, sys
from sl import *
from prof import *
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()
P("p u e/E | R^max(e) = R_{gamma*}(e) | gamma* | tilt upper bound at gamma* (lambda) | ratio | stable two-block profiles of type p_{gamma*} (lower bound)")
for (p, u) in ((0.5, 1.0), (0.3, 1.0), (0.1, 2.0), (0.05, 3.0)):
    E = E_threshold(p, u)
    for f in (0.0, 0.3, 0.6):
        e = f * E
        R, t, m, Q, g = Rmax(p, u, e, return_all=True)
        tb, lam = tilt_bound(p, u, g, e, return_lam=True)
        sc = sup_profiles(p, u, g, e, constrained=True, grid=25)
        P(f"{p:5.2f} {u:4.1f} {f:3.1f} | {R:.6f} | {g:+.4f} | {tb:.6f} ({lam:+.4f}) | {tb/R:.4f} | {sc[0]:.6f}")
open('out/t12_tilt_gammastar.txt', 'w').write('\n'.join(out) + '\n')
