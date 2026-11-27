"""t04c_split.py -- Proposition 11.100: 'after the best split of the accuracy the exponents add' fails for mix2 near the
label switch of the triangle site (theirs: by 8e-7, relative 2.5e-5)."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from r5lib import *

tri = Site([0.2, 0.5, 0.3], [[0, 1, 2], [1, 0, 1.5], [2, 1.5, 0]], "tri")
binr = Site([0.7, 0.3], [[0, 1], [1, 0]], "bin")
F = lambda t: Fstar_site(tri, t)
Fb = lambda t: Fstar_site(binr, t)
tl, tr, ec = 0.3731, 0.3829, 0.056860
# recompute the bitangent points precisely
def tang(e, lo, hi):
    r = minimize_scalar(lambda t: -(F(t) - t * e), bounds=(lo, hi), method="bounded", options=dict(xatol=1e-13))
    return r.x, -r.fun
ec = brentq(lambda e: tang(e, 0.30, 0.377987)[1] - tang(e, 0.377987, 0.46)[1], 0.0541, 0.0596, xtol=1e-15)
tl, tr = tang(ec, 0.30, 0.377987)[0], tang(ec, 0.377987, 0.46)[0]
def conc(t):
    return F(tl) + (F(tr) - F(tl)) * (t - tl) / (tr - tl) if tl < t < tr else F(t)
h = 1e-6
e0 = 0.4 * (Fb(0.378 + h) - Fb(0.378 - h)) / (2 * h) + 0.6 * ec
print(f"bitangent of F*_tri: t in ({tl:.5f}, {tr:.5f}), slope e_c = {ec:.6f}; chain mix2 has its common slope inside for e near {e0:.6f}")
best = (0, None)
for e in np.linspace(e0 - 0.0015, e0 + 0.0015, 61):
    def mx(f):
        ts = np.linspace(0.36, 0.40, 401)
        v = [f(t) - t * e for t in ts]
        i = int(np.argmax(v))
        r = minimize_scalar(lambda t: -(f(t) - t * e), bounds=(ts[max(i-1,0)], ts[min(i+1,400)]), method="bounded", options=dict(xatol=1e-13))
        return max(max(v), -r.fun)
    R = mx(lambda t: 0.4 * Fb(t) + 0.6 * F(t))
    Rs = mx(lambda t: 0.4 * Fb(t) + 0.6 * conc(t))
    if Rs - R > best[0]:
        best = (Rs - R, e, R)
print(f"max over e of [R^split(e) - R^(e)] = {best[0]:.2e} at e = {best[1]:.6f} (R^ = {best[2]:.6f}, relative {best[0]/best[2]:.1e})   [theirs: 8e-7, relative 2.5e-5]")
