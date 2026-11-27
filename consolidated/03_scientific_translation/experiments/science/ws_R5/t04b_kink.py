"""t04b_kink.py -- precise numbers for the label switch of the triangle site (Proposition 11.100) and of the uniform
four-letter Hamming site (DEAD_ENDS D52 item 3)."""
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from r5lib import *
from t04_beyond_two_letters import F_k, hamming

tri = Site([0.2, 0.5, 0.3], [[0, 1, 2], [1, 0, 1.5], [2, 1.5, 0]], "tri")
E = threshold_E(tri)[0]
F = lambda t: Fstar_site(tri, t)
# the two branches: restrict the mixture to the two supports seen on either side of the switch
left_idx, right_idx = [2, 4, 5], [1, 2, 4]

def branch(idx):
    sub = Site.__new__(Site)
    sub.pi, sub.d, sub.q, sub.name = tri.pi, tri.d, tri.q, "sub"
    sub.V, sub.W, sub.logW, sub._cache = tri.V[idx], tri.W[idx], tri.logW[idx], {}
    return lambda t: Fstar_site(sub, t)

FL, FR = branch(left_idx), branch(right_idx)
tc = brentq(lambda t: FL(t) - FR(t), 0.36, 0.40, xtol=1e-13)
h = 1e-5
sL = (FL(tc + h) - FL(tc - h)) / (2 * h)
sR = (FR(tc + h) - FR(tc - h)) / (2 * h)
print(f"triangle site: branches cross at t_c = {tc:.6f}; F*(t_c) = {F(tc):.9f}; max(FL,FR) - F* at 5 points around t_c: "
      f"{[float(f'{max(FL(t), FR(t)) - F(t):.1e}') for t in (tc-0.02, tc-0.005, tc, tc+0.005, tc+0.02)]}")
print(f"   slope of the left branch {sL:.6f}, of the right branch {sR:.6f}: jump {sR - sL:+.6f}   [theirs +0.0052]")
# corner of R^: common tangent
def gap(e):
    l = minimize_scalar(lambda t: -(F(t) - t * e), bounds=(0.30, tc), method="bounded", options=dict(xatol=1e-12))
    r = minimize_scalar(lambda t: -(F(t) - t * e), bounds=(tc, 0.46), method="bounded", options=dict(xatol=1e-12))
    return (-l.fun) - (-r.fun), l.x, r.x
ec = brentq(lambda e: gap(e)[0], sL, sR, xtol=1e-14)
_, tl, tr = gap(ec)
print(f"   corner of R^ at e_c = {ec:.6f} = {ec/E:.4f} E; the maximiser jumps from t = {tr:.4f} to t = {tl:.4f}  "
      f"(slopes of R^: {-tr:.3f} -> {-tl:.3f})   [theirs: 0.1996 E, -0.383 -> -0.373]")
# mix2: best split against R^ near the switch
binr = Site([0.7, 0.3], [[0, 1], [1, 0]], "bin")
ch = Chain([(0.4, binr), (0.6, tri)])
def conc_tri(t):
    # concave envelope of F*_tri: replace by the chord between tl and tr inside (tl, tr)
    if tl < t < tr:
        return F(tl) + (F(tr) - F(tl)) * (t - tl) / (tr - tl)
    return F(t)
worst = 0
for e in np.linspace(0.02, 0.07, 26):
    R = Rhat(ch.Fstar, e, ngrid=600)[0]
    Rs = Rhat(lambda t: 0.4 * Fstar_site(binr, t) + 0.6 * conc_tri(t), e, ngrid=600)[0]
    worst = max(worst, Rs - R)
print(f"   chain mix2: max over e of [best split R^split - R^] = {worst:.2e}   [theirs 8e-7]")
print()
s4 = Site(np.full(4, 0.25), hamming(4, 1.0), "ham4")
ts = np.linspace(0.02, 0.98, 97)
dev = max(abs(Fstar_site(s4, t) - max(F_k(2, 1.0, t), F_k(4, 1.0, t))) for t in ts)
tx = brentq(lambda t: F_k(2, 1.0, t) - F_k(4, 1.0, t), 0.3, 0.9, xtol=1e-12)
print(f"uniform four-letter Hamming site, u = 1: max_t |F*(t) - max(F_2(t), F_4(t))| = {dev:.1e}; F_2 = F_4 at t = {tx:.4f}"
      f"  [D52 item 3: switch from pairs to singletons at t = 0.65]")
print(f"   F_2 > F_4 for t < {tx:.3f}: {F_k(2,1.0,0.3) > F_k(4,1.0,0.3)};  for t > {tx:.3f}: {F_k(2,1.0,0.9) > F_k(4,1.0,0.9)}")
