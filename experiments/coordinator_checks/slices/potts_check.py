#!/usr/bin/env python3
"""More than two letters (theory report 11.25, remark): the comparison with the uniform cube fails.

(1) Potts pair P(b, x) ~ a_b c_x exp(s 1[b = x]) on [q] x [q]: the marginals that maximise the mutual information are uniform on
    k*(s) letters, k* = 2 for small s (random restarts of Nelder-Mead over the 2q fields; q = 3, 4).
(2) Uniform k-ary cubes with the Hamming distance: R_k(e) = max_t [t Psi_k(u) - Psi_k(tu) - te], Psi_k(s) = ln((e^s + k - 1)/k) - s/k.
    R_2 > R_3 for small slopes: a known part that pins the composition of a ternary system onto two letters is harder than none.
(3) The game function as an integral of the mutual information along the tilting path: F*(t) = t u int_{tu}^{u} I(s) s^-2 ds
    (binary slices: against the closed forms of slice_lib; uniform k-ary cubes: against (2))."""
import math, numpy as np
from scipy.optimize import minimize, brentq
from scipy.integrate import quad
from slice_lib import Psi, F, lam_range, golden
def mi_table(P):
    P = P/P.sum(); pb = P.sum(1, keepdims=True); px = P.sum(0, keepdims=True)
    m = P > 1e-300
    return float((P[m]*np.log(P[m]/(pb*px)[m])).sum())
def mi_fields(q, s, z):
    z = np.clip(z, -30, 30)
    return mi_table(np.exp(z[:q])[:, None]*np.exp(s*np.eye(q))*np.exp(z[q:])[None, :])
def mi_unif(k, s):
    p = math.exp(s)/(math.exp(s) + k - 1)
    return math.log(k) + p*math.log(p) + (1-p)*math.log((1-p)/(k-1))
rng = np.random.default_rng(3)
print("(1) maximal mutual information of a Potts pair over both marginals (40 restarts each):")
for q in (3, 4):
    for s in (0.2, 0.5, 1.0, 1.5, 3.0):
        best = -1
        for trial in range(40):
            res = minimize(lambda z: -mi_fields(q, s, z), rng.normal(0, 2.0, 2*q), method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-13, "maxiter": 6000})
            if -res.fun > best:
                best = -res.fun; z = np.clip(res.x, -30, 30)
                P = np.exp(z[:q])[:, None]*np.exp(s*np.eye(q))*np.exp(z[q:])[None, :]; P /= P.sum()
                supp = int((P.sum(1) > 1e-4).sum())
        ks = [mi_unif(k, s) for k in range(2, q+1)]
        print(f"    q = {q}, s = {s:3.1f}: max = {best:.6f} on {supp} letters;  uniform on k = 2..{q} letters: " + ", ".join(f"{v:.6f}" for v in ks) + f";  max - best uniform = {best - max(ks):.1e}")
print(f"    crossings of the uniform laws: I_2 = I_3 at s = {brentq(lambda s: mi_unif(2, s) - mi_unif(3, s), 0.3, 2):.6f},  I_3 = I_4 at s = {brentq(lambda s: mi_unif(3, s) - mi_unif(4, s), 0.6, 4):.6f}")
def Psi_k(k, s): return np.log((np.exp(s) + k - 1)/k) - s/k
def R_k(k, u, e=0.0):
    f = lambda t: -(t*Psi_k(k, u) - Psi_k(k, t*u) - t*e)
    v, _ = golden(f, 0.0, 1.0)
    return max(-v, 0.0)
print("(2) uniform k-ary cubes, zero residual:  u, R_2(0), R_3(0), R_4(0)")
for u in (0.25, 0.5, 0.75, 1.0, 2.0, 4.0):
    print(f"    {u:4.2f}  " + "  ".join(f"{R_k(k, u):.6f}" for k in (2, 3, 4)))
print(f"    R_2(0) = R_3(0) at u = {brentq(lambda u: R_k(2, u) - R_k(3, u), 0.5, 1.0):.4f};  R_3(0) = R_4(0) at u = {brentq(lambda u: R_k(3, u) - R_k(4, u), 1.0, 2.0):.4f}")
print("(3) F*(t) = t u int_{tu}^{u} I(s)/s^2 ds:")
w = 0
for k in (2, 3, 4):
    for u in (0.5, 2.0):
        for t in (0.2, 0.6):
            val = t*u*quad(lambda s: mi_unif(k, s)/s**2, t*u, u)[0]
            w = max(w, abs(val - (t*Psi_k(k, u) - Psi_k(k, t*u))))
print(f"    uniform k-ary cubes: largest difference {w:.1e}")
w = 0
for (m, kap) in ((0.5, 0.5), (0.4, 0.3), (0.3, 0.6)):
    for u in (0.7, 2.0):
        for t in (0.25, 0.7):
            def I_s(s):
                hi = lam_range(m, kap)[1]
                _, l = golden(lambda l: -(s*l - F(m, kap, l)), 0.0, hi*(1 - 1e-13))
                return F(m, kap, l)
            val = t*u*quad(lambda s: I_s(s)/s**2, t*u, u, epsabs=1e-12, epsrel=1e-10)[0]
            w = max(w, abs(val - (t*Psi(m, kap, u) - Psi(m, kap, t*u))))
print(f"    binary type classes (three pairs (m, kappa)): largest difference {w:.1e}")
