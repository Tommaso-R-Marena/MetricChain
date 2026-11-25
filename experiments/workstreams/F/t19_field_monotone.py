"""t19: (i) is F*(t; theta) = max_gamma F(gamma, t) nonincreasing in the field theta >= 0, for every t in (0,1)?
(then R^max(e; theta) is nonincreasing in |theta| for every e, and largest at theta = 0);
(ii) is F(0, t; theta) <= F*(t; theta) with equality only at theta = 0 (the instance g = 0 is not the hardest)?
(iii) sites of two types: exponents do not add (common t): half the sites with field 0, half with field theta_2."""
import math, numpy as np, time
from flib import *
t0 = time.time()
ts = np.linspace(0.0, 1.0, 1001)
worst_inc = -math.inf; min_gap = math.inf
for u in (0.3, 1.0, 2.0, 4.0):
    prev = None
    thetas = np.linspace(0.0, 6.0, 121)
    for theta in thetas:
        p = 1 / (1 + math.exp(theta))
        gs = np.linspace(-u, u, 1601)
        Fg = F_game(p, u, gs[:, None], ts[None, :])
        Fstar = Fg.max(axis=0)
        F0 = F_game(p, u, 0.0, ts)
        if prev is not None:
            worst_inc = max(worst_inc, float((Fstar - prev).max()))
        if theta > 0:
            min_gap = min(min_gap, float((Fstar - F0)[1:-1].min()))
        prev = Fstar
print(f"(i) largest increase of F*(t; theta) between consecutive fields (grid of 121 fields in [0,6], 4 values of u, 1001 values of t): {worst_inc:.3e}  (<= 0 up to the gamma-grid error: nonincreasing)")
print(f"(ii) smallest value of F*(t;theta) - F(0,t;theta) over theta > 0, 0 < t < 1: {min_gap:.3e}  (>= 0)")
# (iii) two site types
u = 1.0
for theta2 in (1.0, 2.0, 3.0):
    w1, w2 = WorstPair(0.5, u), WorstPair(1 / (1 + math.exp(theta2)), u)
    Fmix = 0.5 * w1.Fstar + 0.5 * w2.Fstar
    E = Fmix[1] / w1.ts[1]
    for frac in (0.0, 0.3):
        e = frac * E
        Rmix = float(np.max(Fmix - e * w1.ts))
        avg = 0.5 * float(w1.R(e)) + 0.5 * float(w2.R(e))
        print(f"(iii) u={u}, fields (0, {theta2}) half and half, e = {frac} E (E = {E:.5f} = average of the thresholds {0.5*(w1.E+w2.E):.5f}): "
              f"R^max = max_t[sum_j lam_j F*_j(t) - t e] = {Rmix:.6f};  average of the two exponents at the same e = {avg:.6f}")
print("time", time.time() - t0)
