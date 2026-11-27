"""t06: sanity of finite.py in the uniform case (p = 1/2) against the report's exponents."""
import math, time, numpy as np
from flib import *
from finite import *
t0 = time.time()
u = 1.0; p = 0.5
estar = math.log(math.cosh(u / 2))
for n in (200, 400, 800):
    for frac in (0.25,):
        e1 = frac * estar
        flat = np.zeros(n + 1)
        d, kd = best_over_centres(n, p, u, e1 * n, "dip", logw0_t=flat, kgrid=[n // 4, n // 2, 3 * n // 4], refine=False)
        f, kf = best_over_centres(n, p, u, e1 * n, "flatten", kgrid=[n // 4, n // 2, 3 * n // 4], refine=False)
        Lam1 = math.log(2 / (1 + math.exp(-u)))
        print(f"n={n} eps1={e1:.5f}: hinted exact {d:.5f} (k={kd}) vs theta_hint={kls((Lam1+e1)/u,0.5):.5f};"
              f"  non-adaptive exact {f:.5f} (k={kf}) vs theta_na={maxmin_precise(Site(p,u),'na',e1)[0]:.5f};  t={time.time()-t0:.1f}s")
