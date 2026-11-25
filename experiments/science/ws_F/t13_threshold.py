"""Thresholds with the oracle at the zero residual: E_0(theta) = lim_{t->0} F(0,t;theta)/t (above it the hinted cost is
bounded); with the oracle the tilt gives the threshold bound  E_0^orc <= min_lambda [ E_0(theta - lambda) + c(lambda) ]."""
import numpy as np, sys
from scipy.optimize import minimize_scalar
from sl import *
from prof import c_tilt
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s); sys.stdout.flush()
def E0(p, u):
    return F_game(p, u, 0.0, 1e-6) / 1e-6
P("p u | E_0 (zero residual, no oracle) | class threshold E | tilt bound on the threshold with oracle (lambda*) | ratio to E_0")
for (p, u) in ((0.5, 1.0), (0.4, 1.0), (0.3, 1.0), (0.25, 1.0), (0.2, 0.5), (0.1, 1.0), (0.1, 2.0), (0.05, 3.0), (0.02, 2.0)):
    def val(lam):
        pl = 1 / (1 + np.exp(-(np.log(p / (1 - p)) + lam)))
        return E0(pl, u) + c_tilt(p, 0.0, lam)
    lams = np.linspace(-4, 4, 401); vals = [val(l) for l in lams]; i = int(np.argmin(vals))
    res = minimize_scalar(val, bounds=(lams[max(i - 1, 0)], lams[min(i + 1, 400)]), method='bounded')
    P(f"{p:5.2f} {u:4.1f} | {E0(p,u):.6f} | {E_threshold(p,u):.6f} | {res.fun:.6f} ({res.x:+.4f}) | {res.fun/E0(p,u):.4f}")
open('out/t13_threshold.txt', 'w').write('\n'.join(out) + '\n')
