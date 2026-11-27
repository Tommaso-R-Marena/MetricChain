"""Addendum A16, exploratory: does hiding the plateau twin on a visible TERRACE beat hiding it in the flat background?

Exponential-scale formulas only (no finite n).  Mask: flat background (level 0) + a visible cone basin at threshold
dominance (entropy s0 = h(sigma), energy -u e1 n, e1 = rho0 - sigma) + a visible, just sub-dominant plateau basin
("terrace") of radius rho_T at level -(ln 2 - h(rho_T)) n.  Twin: a cap of the terrace's rim sphere with entropy
s0 + eps1, dug down to the level of the datum; digging depth delta = (h(rho_T) - s0)/u in distance units.
Search cost exponent >= h(rho_T) - max over query points of the exponent of the number of twin centres whose
support can contain the point (the support is replaced by the larger ball of radius theta + depth, so this is a
valid lower bound on the cost within the family).  rho_T = 1/2 is the flat background (addendum A16, Proposition
A16.3).  Result: the maximum over rho_T is at rho_T = 1/2 in every case tried.  Evidence, not proof.

Usage: python3 terrace_twin_explore.py      (about one minute)
"""
import math, numpy as np
from scipy.optimize import brentq
def h(x):
    return 0.0 if x <= 0 or x >= 1 else -x*math.log(x) - (1 - x)*math.log(1 - x)
def hinv(y): return brentq(lambda x: h(x) - y, 1e-15, 0.5)
def J(rho, xi, R):
    """exponent of #{a' at distance rho n from the origin : d(x, a') <= R n}, for x at distance xi n"""
    klo = max(0.0, rho + xi - 1.0, (rho + xi - R)/2); khi = min(rho, xi)
    if klo > khi: return -math.inf
    val = lambda k: (xi*h(k/xi) if xi > 0 else 0.0) + ((1 - xi)*h((rho - k)/(1 - xi)) if xi < 1 else 0.0)
    kstar = rho*xi
    if klo <= kstar <= khi: return h(rho)
    return val(klo) if kstar < klo else val(khi)
def terrace(u, eps1, rhoT):
    sigma = 1/(1 + math.exp(u)); rho0 = math.log(2/(1 + math.exp(-u)))/u
    s0 = h(sigma); e1 = rho0 - sigma
    lT = -(math.log(2) - h(rhoT)); delta = (lT + u*e1)/u; target = s0 + eps1
    if h(rhoT) < target: return None
    theta = brentq(lambda t: J(rhoT, rhoT, t) - target, 1e-9, 2*rhoT*(1 - rhoT))
    wT = -lT/u; best = -math.inf; arg = None
    for xi in np.linspace(1e-6, 1 - 1e-6, 4001):
        dep = delta if xi <= rhoT else (delta + (xi - rhoT) if xi <= rhoT + wT else e1)
        v = J(rhoT, xi, theta + dep)
        if v > best: best, arg = v, xi
    return h(rhoT) - best, theta, delta, arg
if __name__ == "__main__":
    for u in (1.0, 2.0, 4.0):
        sigma = 1/(1 + math.exp(u)); rho0 = math.log(2/(1 + math.exp(-u)))/u; a = math.log(2) - h(sigma)
        for frac in (0.1, 0.25, 0.5, 0.75):
            eps1 = frac*a
            flat = math.log(2) - h(min(0.5, rho0 - sigma + hinv(h(sigma) + eps1)))
            hint = math.log(2) - h(min(0.5, rho0 + eps1/u))
            rows = []
            for rhoT in np.linspace(hinv(h(sigma) + eps1) + 1e-4, 0.5, 400):
                r = terrace(u, eps1, rhoT)
                if r: rows.append((r[0], rhoT))
            b = max(rows)
            assert abs(rows[-1][0] - flat) < 1e-6 and b[0] <= flat + 1e-6
            print(f"u={u} eps1={eps1:.4f}: flat-background plateau twin {flat:.5f} | best terrace {b[0]:.5f} at rho_T={b[1]:.4f} | no datum {hint:.5f}")
