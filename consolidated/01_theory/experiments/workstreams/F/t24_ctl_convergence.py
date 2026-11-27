"""t24: convergence in n of the raw difference e - chi(theta) of Theorem F6 for two fixed shapes at the predicted extremal
centre type (p = 0.1, u = 2): the density ball at density e^{-n theta0}, and the anisotropic ball {alpha a + beta b < c}
tangent to it at the optimal exit profile.  If the exponent of Theorem F6 is right, the difference is O(ln n / n)."""
import math, sys, numpy as np
from flib import *
from birad import *
p, u = 0.1, 2.0
st = Site(p, u); wp = WorstPair(p, u)
es = np.linspace(wp.ec - 0.3, wp.E, 40001); Rs = wp.R(es)
chi = lambda th: -th if th >= Rs[0] else float(np.interp(th, Rs[::-1], es[::-1]))
e0 = 0.25 * wp.E
val, mstar, xs, ys, kap = maxmin_precise(st, "H", e0)
a_, b_ = mstar * xs, (1 - mstar) * ys
lr = lambda z: math.log((1 - z) / z)
al, be = lr(kap) + lr(xs), lr(ys) - lr(kap)            # -dI/da, -dI/db at the exit profile
c = al * a_ + be * b_
print(f"p={p} u={u} e0={e0:.5f}: R^max(e0)={val:.6f}, m*={mstar:.4f}, exit profile a={a_:.4f} b={b_:.4f}; normal (alpha,beta)=({al:.4f},{be:.4f}), c={c:.4f}")
for n in [int(x) for x in sys.argv[1].split(",")]:
    k = int(round(mstar * n)); C = Centre(n, k, p)
    tt = np.arange(n + 1); lwH_t = logw_H(n, p, u, tt)
    lnZH = float(np.log(np.sum(np.exp(lnC(n, tt) + tt * math.log(p) + (n - tt) * math.log(1 - p) + lwH_t))))
    lw0 = lwH_t[C.t]
    ii, jj = np.broadcast_arrays(C.i, C.j)
    out = []
    for name, ins in (("density ball", C.density_ball(-n * val)[0]), ("anisotropic ball", al * ii + be * jj < c * n)):
        lw1 = C.lower_envelope_logw(lw0, ins, u)
        mass = C.logmass[ins]
        th = -(float(logsumexp(mass + lw0[ins])) - lnZH) / n
        e = (float(logsumexp(mass + lw1[ins])) - lnZH) / n
        out.append(f"{name}: theta={th:.5f} e={e:.5f} chi(theta)={chi(th):.5f} diff={e - chi(th):+.5f} = {(e - chi(th)) * n / math.log(n):+.2f} ln(n)/n")
    print(f"  n={n}: " + ";  ".join(out), flush=True)
