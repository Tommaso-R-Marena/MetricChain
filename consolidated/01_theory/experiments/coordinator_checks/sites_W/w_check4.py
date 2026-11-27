#!/usr/bin/env python3
"""Check 4 of workstream W (coordinator): the comparison columns of the worked example at e = 0, and the uniform four-letter site.

(a) zero residual: R_0(0) = max_t sum_j lam_j F_j(0, t), F_j(0, t) = -ln val(K_t^0) by linear programming;
(b) binary reductions of a three-state site: coarse-graining {a} | rest (law (pi(a), 1 - pi(a)), envelope (min_b d(a,b), min_b d(b,a)))
    and deletion of a state (pair {a, b}, renormalised law, envelope (d(a,b), d(b,a))); the maximum over the three choices;
(c) the uniform four-letter Hamming site at u = 1: F*(t) on a grid against the two groupings F*_2, F*_4; second differences."""
import math, numpy as np
from wv_lib import *
def R0(sites, lam, grid=200):
    Vs = [vertices(d) for (pi, d) in sites]
    ts = np.linspace(0.005, 0.995, grid)
    vals = [sum(l*F_game(pi, V, np.zeros(len(pi)), t)[0] for l, (pi, d), V in zip(lam, sites, Vs)) for t in ts]
    i = int(np.argmax(vals))
    # refine by a finer grid around the maximiser
    tt = np.linspace(ts[max(i-1, 0)], ts[min(i+1, grid-1)], 201)
    return max(sum(l*F_game(pi, V, np.zeros(len(pi)), t)[0] for l, (pi, d), V in zip(lam, sites, Vs)) for t in tt)
print("(a) zero residual R_0(0)   [report: path 0.080032, tri 0.065233, asym 0.033856, mix 0.052360, mix2 0.049065]")
for name, sites, lam in (("path", [SITES["path"]], [1.0]), ("tri", [SITES["tri"]], [1.0]), ("asym", [SITES["asym"]], [1.0]),
                         ("mix", [SITES["bin"], SITES["path"]], [0.5, 0.5]), ("mix2", [SITES["bin"], SITES["tri"]], [0.4, 0.6])):
    print(f"    {name:5s} {R0(sites, lam):.6f}")
print("(b) binary reductions at e = 0   [report: path 0.048586 / 0.115369, tri 0.053168 / 0.094950, asym 0.024685 / 0.058646]")
for name in ("path", "tri", "asym"):
    pi, d = SITES[name]; d = np.array(d, float); q = 3
    cut = 0; pair = 0
    for a in range(q):
        others = [b for b in range(q) if b != a]
        dd = [[0.0, min(d[a][b] for b in others)], [min(d[b][a] for b in others), 0.0]]
        cut = max(cut, Chain([([pi[a], 1 - pi[a]], dd)], [1.0]).Rmax(0.0)[0])
    for a in range(q):
        for b in range(a + 1, q):
            z = pi[a] + pi[b]
            pair = max(pair, Chain([([pi[a]/z, pi[b]/z], [[0.0, d[a][b]], [d[b][a], 0.0]])], [1.0]).Rmax(0.0)[0])
    print(f"    {name:5s} coarse-graining {cut:.6f}, deletion {pair:.6f}")
print("(c) uniform four-letter Hamming site, u = 1: F*(t) with all 14 vertices against the groupings k = 2 and k = 4")
u = 1.0
Psi = lambda k, s: math.log((math.exp(s) + k - 1)/k) - s/k
V4 = vertices(hamming(4, u)); pi4 = [0.25]*4
ts = np.linspace(0.02, 0.98, 97)
F = np.array([renyi_form(pi4, V4, t, starts=4)[0] for t in ts])
F2 = np.array([t*Psi(2, u) - Psi(2, t*u) for t in ts]); F4 = np.array([t*Psi(4, u) - Psi(4, t*u) for t in ts])
env = np.maximum(F2, F4)
print(f"    largest F* - max(F*_2, F*_4): {(F - env).max():.2e};  smallest: {(F - env).min():.2e}")
i = int(np.argmin(np.abs(F2 - F4)))
print(f"    the two groupings cross near t = {ts[i]:.3f} (F*_2 = {F2[i]:.6f}, F*_4 = {F4[i]:.6f}, F* = {F[i]:.6f})")
d2 = np.diff(F, 2)/(ts[1] - ts[0])**2
j = int(np.argmax(d2))
print(f"    second differences of F*: largest {d2[j]:+.4f} at t = {ts[j+1]:.3f}; typical {np.median(d2):+.4f}  (positive = not concave)")
