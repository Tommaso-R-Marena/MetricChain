"""spot checks of Section 6.6 (table in the coupling, e = 0, u = 1) and of 'other couplings' in 6.7 (own code)."""
import time
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *
from r10tab import *
t0 = time.time()
ref = {1.12: (0.0291391, 0.2689, 0.0291391), 1.14: (0.0290694, 0.2689, 0.0290694), 1.20: (0.0283097, 0.2742, 0.0273828), 1.30: (0.0271307, 0.2831, 0.0202239), 1.75: (0.0230260, 0.3129, 0.0054940)}
print("# Section 6.6: bJ | binary sup-min at e=0 | optimal profile | report | cone formula | report | R_unif = 0.0291391")
for bJ, (rb, x, rc) in ref.items():
    M = Model(bJ, 0.0, 1.0)
    Rb, lb, mb = R_binary(M, 0.0, starts=[(0.5, 0.27, 0.27), (0.5, 0.3, 0.3), (0.45, 0.3, 0.26), (0.55, 0.26, 0.3)])
    Rc, mc = R_cone(M, 0.0)
    s2 = inner_dual(M, lb, mb, alpha(M, lb, mb), nk=1201, refine=5)[0]
    print(f"  {bJ}: {Rb:.7f} (S2 {s2:.7f}) [{fmt(lb, mb)}]  report {rb} (x={x})   cone {Rc:.7f} (m={mc:.3f})  report {rc}   t={time.time()-t0:.0f}", flush=True)
print("# Section 6.7, other couplings: bJ = 2.0")
M = Model(2.0, 0.0, 1.0)
print("   contact set", [(round(a, 3), round(b, 3)) for a, b in M.contact()], " (report [0.007,0.099] u [0.271,0.729] u [0.901,0.993])")
Rb, lb, mb = R_binary(M, 0.0, starts=[(0.5, 0.3249, 0.3249), (0.5, 0.3, 0.3), (0.45, 0.33, 0.3), (0.5, 0.9, 0.05), (0.5, 0.36, 0.36)])
print(f"   e=0: binary {Rb:.7f} [{fmt(lb, mb)}] (report 0.0213210, x = 0.3249)")
def s3(lf, x):
    return np.array([(1 - lf) / 2, lf, (1 - lf) / 2]), np.array([1 - x, 0.5, x])
for e, rb, rf, lf0, x0 in ((0.01, 0.0158308, 0.0163911, 0.271, 0.2863), (0.03, 0.0068042, 0.0084996, 0.274, 0.3002)):
    Rb, lb, mb = R_binary(M, e, starts=[(0.5, 0.33, 0.33), (0.5, 0.3, 0.3), (0.45, 0.33, 0.3)])
    def f(z):
        v = r_mu(M, *s3(min(max(z[0], 1e-4), 0.9), min(max(z[1], 0.01), 0.49)), e)
        return -v if np.isfinite(v) else 1.0
    res = optimize.minimize(f, [lf0, x0], method='Nelder-Mead', options={'xatol': 1e-9, 'fatol': 1e-14, 'maxiter': 800})
    l3, m3 = s3(*res.x)
    s2 = inner_dual(M, l3, m3, e + alpha(M, l3, m3), nk=1201, refine=5)[0]
    print(f"   e={e}: binary {Rb:.7f} (report {rb});  free block {-res.fun:.7f} at lf={res.x[0]:.4f}, x={res.x[1]:.4f}, S2 {s2:.7f} (report {rf}, lf={lf0}, x={x0});  R_unif {R_unif(e,1.0):.7f}   t={time.time()-t0:.0f}", flush=True)
print("time", time.time() - t0)
