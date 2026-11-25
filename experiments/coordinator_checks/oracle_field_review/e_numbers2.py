import math, numpy as np
from e_numbers import f_profile, kl
p, u, e = 0.25, 1.0, 0.02
q = 1 - p
pm = p * math.exp(-u) / (q + p * math.exp(-u)); pp = p * math.exp(u) / (q + p * math.exp(u))
# one block at p-, weight wa; the other at vb = (p - wa p-)/(1 - wa) <= p+
best = (0, None)
for wa in np.linspace(0.30, 0.70, 40001):
    vb = (p - wa * pm) / (1 - wa)
    if vb > pp: continue
    val = f_profile(1 - wa, pm, vb, e, p, u)      # weights: block0 (weight 1-m = wa) at p-, block1 (weight m = 1 - wa) at vb
    if val > best[0]: best = (val, (wa, vb))
print("window-restricted, one block at p-:", best)
# brute force of the inner minimisation at the optimum, to check f_profile itself
wa, vb = best[1]
m = 1 - wa; v0, v1 = pm, vb
budget = (e + (1 - m) * kl(v0, p) + m * kl(v1, p)) / u
bestI = math.inf
for a0 in np.linspace(0.0, 1.0, 4001):
    rem = budget - (1 - m) * abs(a0 - v0)
    if rem < 0: continue
    for sgn in (-1, 1):
        a1 = v1 + sgn * rem / m
        if not 0 <= a1 <= 1: continue
        bar = (1 - m) * a0 + m * a1
        I = (1 - m) * kl(a0, bar) + m * kl(a1, bar)
        bestI = min(bestI, I)
print("inner minimum by brute force:", bestI, " f_profile:", f_profile(m, v0, v1, e, p, u))
