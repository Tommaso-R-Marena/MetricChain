# Validation target of SCI-REV-0015 (R15-T2): the first block of the table of its report, section 3.5, from our own code.
# Eight independent sites, four frozen (p = 0.01) and four mobile (p = 0.3), all 56 triples with equal constants c.
import math, itertools
import numpy as np
from scipy.optimize import minimize
n, m = 8, 3
p = np.array([0.01] * 4 + [0.3] * 4)
f = np.log((1 - p) / p)
sp = lambda z: np.log1p(np.exp(z))
subs = list(itertools.combinations(range(n), m))
def ends(gam):
    U = float(np.sum(sp(gam - f) - sp(-f))); L = float(np.sum(sp(-f) - sp(-f - gam)))
    return U, L
def site_vector(c, t1, t2):
    """triples with j frozen sites give the fraction t_j of their constant to their frozen sites (equally), the rest to the mobile ones"""
    g = np.zeros(n)
    for T in subs:
        fr = [i for i in T if i < 4]; mo = [i for i in T if i >= 4]
        if len(fr) == 0 or len(fr) == 3:
            for i in T: g[i] += c / 3
        else:
            t = t1 if len(fr) == 1 else t2
            for i in fr: g[i] += c * t / len(fr)
            for i in mo: g[i] += c * (1 - t) / len(mo)
    return g
print("c | U equal | U vertex | U minimum (symmetric two-parameter family) | L equal | L vertex | largest gamma_vertex - f")
for c in (0.03, 0.1, 0.3, 1.0):
    g_eq = np.zeros(n); g_vx = np.zeros(n)
    for T in subs:
        for i in T: g_eq[i] += c / 3
        g_vx[min(T)] += c                       # sites are numbered most frozen first
    Ue, Le = ends(g_eq); Uv, Lv = ends(g_vx)
    best = min((minimize(lambda t: ends(site_vector(c, min(max(t[0], 0), 1), min(max(t[1], 0), 1)))[0], x0, method='Nelder-Mead',
                         options=dict(xatol=1e-10, fatol=1e-12)).fun) for x0 in ([0.5, 0.5], [1, 1], [0, 0], [0.9, 0.9]))
    print("%.2f | %.3f | %.3f | %.3f | %.3f | %.3f | %+.2f" % (c, Ue, Uv, best, Le, Lv, float(np.max(g_vx - f))))
print("the division's rows: 0.03: 0.280 0.057 0.055 0.242 0.048 -0.76; 0.1: 1.102 0.260 0.230 0.675 0.137 -0.55; 0.3: 4.866 3.185 1.978 1.257 0.315 +1.71; 1.0: 33.12 36.12 32.87 1.465 0.586 +16.4")
