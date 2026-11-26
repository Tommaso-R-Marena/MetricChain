"""Coordinator's check for THY-RES-0008 section 2 (F-T1 (ii)), second attempt.
At a NEGATIVE argument e, compare
   G(e)  = max_{0<=t<=1} [F(gamma,t) - t e]     (what workstream F's code evaluates inside the tilt bound U; sl.R_gamma)
   C(e)  = max_m Rcc(gamma, m; e)                (plain dips of centre type m; dual with t unrestricted: sl.Rcc)
   -e
On the uniform cube the truth is known in closed form from balls: ln2 - h(rho0 + e/u) for -a <= e <= 0 and -e below.
Expectation: G = C for -a_gamma <= e <= 0 (dual optimum t <= 1); for e < -a_gamma, G = -e while C > -e (t > 1: the
over-estimate the theory division warns against)."""
import sys, math
sys.path.insert(0, '/home/user/MetricChain/experiments/science/ws_F')
import numpy as np, sl
from scipy.optimize import minimize_scalar
def h(x): return -x*math.log(x) - (1-x)*math.log(1-x)
print("F(gamma, 1) at nine additive bases (should vanish: the input law with MW = pi_gamma exists):")
for (p, u) in ((0.25, 1.0), (0.3, 1.0), (0.1, 2.0)):
    for g in (0.0, 0.4 * u, -0.5 * u):
        print(f"   p={p} u={u} gamma={g:+.2f}: F(gamma,1) = {sl.F_game(p, u, g, 1.0):+.2e}")
print(f"{'p':>5}{'u':>5}{'gamma':>7}{'e/a_g':>8}{'e':>10} | {'G: game t<=1':>13}{'C: max_m Rcc':>14}{'-e':>10}{'G-C':>11}{'G-(-e)':>11}{'cube truth':>12}")
for (p, u, g) in ((0.5, 1.0, 0.0), (0.25, 1.0, 0.0), (0.1, 2.0, 0.0), (0.25, 1.0, 0.4), (0.1, 2.0, -1.0)):
    a_g = -(sl.F_game(p, u, g, 1.0) - sl.F_game(p, u, g, 1.0 - 1e-6)) / 1e-6
    for frac in (0.25, 0.6, 0.9, 1.2, 2.0):
        e = -frac * a_g
        G = sl.R_gamma(p, u, g, e)
        ms = np.linspace(0.02, 0.98, 49)
        vals = [sl.Rcc(p, u, g, m, e) for m in ms]
        i = int(np.argmax(vals))
        res = minimize_scalar(lambda m: -sl.Rcc(p, u, g, m, e), bounds=(ms[max(i-1,0)], ms[min(i+1,48)]), method='bounded')
        C = max(-res.fun, vals[i])
        truth = ''
        if p == 0.5 and g == 0.0:
            rho0 = math.log(2/(1+math.exp(-u)))/u; a = math.log(2) - h(1/(1+math.exp(u)))
            truth = f"{(math.log(2) - h(rho0 + e/u)) if e >= -a else -e:12.6f}"
        print(f"{p:5.2f}{u:5.1f}{g:7.2f}{-frac:8.2f}{e:10.5f} | {G:13.6f}{C:14.6f}{-e:10.5f}{G-C:11.2e}{G+e:11.2e}{truth:>12}")
