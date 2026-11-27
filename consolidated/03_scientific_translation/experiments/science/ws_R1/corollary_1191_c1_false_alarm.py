# R1: the first version of r_general returned MI(mu) when no grid point was feasible; this script exhibits one such
# false alarm (CW bJ=0.8, bB=0.1; profile with a tiny budget) and shows, by thinning the slice exit to the contact type
# (Lemma 11.77(b)), that a feasible exit with smaller MI exists.
import math, numpy as np
import corollary_1191_checks as C
from thm_1190 import Ray
u = 1.0
rate = C.Rate(C.cw(0.8, 0.1), u)
m, a, b, e = 0.8585, 0.7522, 0.6977, 0.0
kappa = m*a + (1-m)*b
I_k, v_k = float(rate.I(kappa)), float(rate.v(kappa))
print("kappa", kappa, "I", I_k, "v", v_k, "gap", I_k - v_k, "MI(mu)", float(C.MI2(m,a,b)))
# contact type kappa* attaining v(kappa)
g = rate.grid; vals = rate.Igrid + u*np.abs(g - kappa); i = int(np.argmin(vals)); ks = g[i]
print("kappa* =", ks, " I(kappa*) + u|kappa-kappa*| =", vals[i])
ray = Ray(m, kappa); l = 2*m*(a - kappa)
w = (e + (I_k - v_k) + ray.F(l))/u
print("ray l =", l, "budget w =", w, " l - w =", l - w, " r_slice =", ray.r_shell(l, e + I_k - v_k, u))
ls = max(l - w, 0.0)
nu = ray.ab(ls); print("slice exit nu_s =", nu, " MI =", float(C.MI2(m, nu[0], nu[1])), " dist =", m*abs(nu[0]-a) + (1-m)*abs(nu[1]-b))
# thinning to kappa*
if ks < kappa:
    nu2 = (nu[0]*ks/kappa, nu[1]*ks/kappa)
else:
    nu2 = (1 - (1-nu[0])*(1-ks)/(1-kappa), 1 - (1-nu[1])*(1-ks)/(1-kappa))
d2 = m*abs(nu2[0]-a) + (1-m)*abs(nu2[1]-b)
lhs = u*d2 + float(rate.I(m*nu2[0] + (1-m)*nu2[1]))
budget = e + float(C.MI2(m,a,b)) + I_k
print("thinned nu'' =", nu2, " type", m*nu2[0] + (1-m)*nu2[1], " MI =", float(C.MI2(m, nu2[0], nu2[1])), " constraint lhs =", lhs, " budget =", budget, " feasible:", lhs <= budget + 1e-12)
print("r_general (grid+SLSQP):", C.r_general(rate, "v", m, a, b, e, u, ngrid=801, polish=8))
