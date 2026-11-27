"""t01: (i) uniform case reproduces the report; (ii) game formula vs rate-distortion form at g = 0;
(iii) the shift identity."""
import math, numpy as np
from flib import *

rng = np.random.default_rng(1)
# (iii) identity  Icone = I + KL(kappa||p) + u P(X != S) - Lam(m)
worst = 0.0
for _ in range(20000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.05, 5)
    st = Site(p, u)
    m, x, y = rng.uniform(0.001, 0.999, size=3)
    worst = max(worst, abs(kl_shift_identity_check(st, m, x, y)))
print("shift identity, max abs error over 20000 random (p,u,m,x,y):", worst)

# (i) uniform case
for u in (0.5, 1.0, 2.0):
    st = Site(0.5, u)
    Lam1 = math.log(2 / (1 + math.exp(-u)))
    estar = math.log(math.cosh(u / 2))
    for frac in (0.0, 0.25, 0.5, 0.75):
        e = frac * estar
        rho = (Lam1 + e) / u
        th_report = kls(rho, 0.5)
        g, tb = R_additive(0.5, u, 0.0, e)
        rd = hint0_rd(st, e)
        print(f"u={u} eps1={e:.5f}: report KL(rho||1/2)={th_report:.6f}  game={g:.6f} (t*={tb:.3f})  rate-dist={rd[0]:.6f} (m*={rd[1]:.3f})")

# (ii) biased: game formula vs rate-distortion form at g = 0
print("biased sites, g = 0: game vs rate-distortion")
worst = 0.0
for p in (0.05, 0.1, 0.2, 0.3, 0.4):
    for u in (0.5, 1.0, 2.0, 4.0):
        st = Site(p, u)
        thr = thr_additive(p, u, 0.0)
        for frac in (0.0, 0.2, 0.5, 0.8):
            e = frac * thr
            g, tb = R_additive(p, u, 0.0, e)
            rd = hint0_rd(st, e, nm=200001)
            worst = max(worst, abs(g - rd[0]))
            if frac in (0.0, 0.5):
                print(f"p={p} u={u} eps1={e:.5f} (thr={thr:.5f}): game={g:.7f} t*={tb:.3f}  rd={rd[0]:.7f} m*={rd[1]:.4f} rho*={rd[2]:.4f}")
print("max |game - rd| =", worst)
