# Coordinator's check of referee R10, m12: a_cone = max_m MI(Gibbs shell of the cone around a centre of type m); bJ = 1.5, B = 0, u = 1.
import numpy as np
from scipy.optimize import minimize
bJ, u = 1.5, 1.0
hb = lambda x: -(x*np.log(x) + (1-x)*np.log(1-x))
raw = lambda k: -(bJ/2)*(2*k-1)**2 - hb(k)
kk = np.linspace(1e-6, 1-1e-6, 2000001); c = raw(kk).min()
I = lambda k: raw(k) - c
def G_MI(m, a, b):
    k = m*(1-a) + (1-m)*b
    mi = hb(k) - m*hb(a) - (1-m)*hb(b)
    return mi + I(k) + u*(m*a + (1-m)*b), mi
def shells(m):
    ax = np.linspace(1e-4, 1-1e-4, 1500)
    A, Bm = np.meshgrid(ax, ax, indexing="ij")
    g, mi = G_MI(m, A, Bm)
    # all local minima on the grid, polished
    out = []
    loc = (g[1:-1,1:-1] <= g[:-2,1:-1]) & (g[1:-1,1:-1] <= g[2:,1:-1]) & (g[1:-1,1:-1] <= g[1:-1,:-2]) & (g[1:-1,1:-1] <= g[1:-1,2:])
    for i, j in zip(*np.nonzero(loc)):
        r = minimize(lambda z: G_MI(m, z[0], z[1])[0], [ax[i+1], ax[j+1]], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-15, maxiter=4000))
        out.append((r.fun, G_MI(m, r.x[0], r.x[1])[1], r.x[0], r.x[1]))
    out.sort()
    return out
for m in (0.45, 0.49, 0.5, 0.5025, 0.51, 0.55):
    s = shells(m)
    print(f"m={m}: " + "; ".join(f"G={g:.7f} MI={mi:.6f} (a={a:.4f}, b={b:.4f})" for g, mi, a, b in s[:3]))
