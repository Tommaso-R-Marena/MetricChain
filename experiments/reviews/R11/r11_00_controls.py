"""R11 / 00 -- controls: the uniform cube at u = 1 (which quantity is 0.029139?), the two-letter
site with a field (0.7, 0.3), and my moment-Lyapunov operator against exact enumeration.

Run:  python3 r11_00_controls.py   (a few seconds)
"""
import numpy as np
from r11lib import *

u = 1.0
h = u / 2

print("== (1) the cube value 0.029139: three independent expressions ==")
# (a) game function per site, closed form t ln cosh(u/2) - ln cosh(tu/2), maximised over t
hval, ts, a, E = cube_constants(u)
print(f"(a) max_t [t ln cosh(u/2) - ln cosh(tu/2)] = {hval:.7f} at t* = {ts:.4f};  a = {a:.7f};  E = ln cosh(u/2) = {E:.7f}")
# (b) Theorem 11.25(d), third row: ln 2 - h(Lambda_1/u), Lambda_1 = ln(2/(1+e^-u))
Lam1 = np.log(2 / (1 + np.exp(-u)))
rho = Lam1 / u
hb = lambda x: -x * np.log(x) - (1 - x) * np.log(1 - x)
print(f"(b) Theorem 11.25(d): ln 2 - h(Lambda_1/u) = {np.log(2) - hb(rho):.7f}   (Lambda_1 = {Lam1:.6f})")
# (c) Renyi form by own solver for one site with the two vertices -/+ h s
s, pi = chain_law(1, 0.5)
labels = np.array([[1], [-1]])
phis = -h * labels @ s.T
logP = gibbs_logs(np.log(pi), phis)
f = lambda t: maximise_G(logP, t)[0]
tt, hv = golden_max(f, 0.05, 0.95, tol=1e-7)
lo, up, M = maximise_G(logP, tt)
print(f"(c) own Renyi solver, one site, 2 vertices: h = [{lo:.7f}, {up:.7f}] at t* = {tt:.4f}")
lo, up, _ = maximise_a(logP)
print(f"    a = [{lo:.7f}, {up:.7f}]")
lo, up, _ = maximise_E(logP)
print(f"    E = [{lo:.7f}, {up:.7f}]")

print("\n== (2) blocks of 2 and 3 independent uniform sites as one super-site, site-wise labels ==")
for n in (2, 3):
    s, pi = chain_law(n, 0.5)
    labels = configs(n).astype(float)
    phis = -h * labels @ s.T
    logP = gibbs_logs(np.log(pi), phis)
    lo, up, M = maximise_G(logP, ts)
    lo_a, up_a, _ = maximise_a(logP)
    lo_e, up_e, _ = maximise_E(logP)
    print(f"n={n}: per site  F(t*) = [{lo/n:.7f}, {up/n:.7f}]   a = [{lo_a/n:.7f}, {up_a/n:.7f}]   E = [{lo_e/n:.7f}, {up_e/n:.7f}]")
print("   (upper ends here are duals over site-wise labels only; Lemma B (hand-checked) gives the product value over the whole class)")

print("\n== (3) two-letter site with a field, pi = (0.7, 0.3), u = 1 (report: h = 0.0250335, a = 0.0953005, E = 0.1031310) ==")
pi1 = np.array([0.7, 0.3])
s1 = np.array([[1], [-1]])
phis = -h * labels[:0]  # placeholder
phis = np.array([[-h, h], [h, -h]])          # the two vertices +/- h s
logP = gibbs_logs(np.log(pi1), phis)
f = lambda t: maximise_G(logP, t)[0]
tt, hv = golden_max(f, 0.05, 0.95, tol=1e-7)
lo, up, M = maximise_G(logP, tt)
la, ua, _ = maximise_a(logP)
le, ue, _ = maximise_E(logP)
print(f"h = [{lo:.7f}, {up:.7f}] at t* = {tt:.4f};  a = [{la:.7f}, {ua:.7f}];  E = [{le:.7f}, {ue:.7f}]")

print("\n== (4) moment Lyapunov operator against exact increments ln E_n - ln E_{n-1} ==")
cases = [(0.4236, 0.5, 0.2, 0.5), (0.4236, 0.5, 0.5, 0.3), (0.6931, 0.5, 0.1, 0.7), (1.0986, 0.5, 0.35, 0.45),
         (0.8, 0.25, 0.3, 2.0), (0.3, 0.05, 0.2, 12.0), (2.0, 0.3, 0.1, 3.0)]
for kappa, eta, q, r in cases:
    vals = [L_moment(q, kappa, eta, r, N=N) for N in (24, 48, 96)]
    ex = [np.log(Xi_exact_moment(q, kappa, eta, r, n)) for n in (15, 16, 17, 18)]
    inc = np.diff(ex)
    print(f"kappa={kappa:.4f} eta={eta:.2f} q={q:.2f} r={r:5.2f}: operator N=24,48,96: {vals[0]:.12f} {vals[1]:.12f} {vals[2]:.12f} | exact increments n=16,17,18: {inc[0]:.9f} {inc[1]:.9f} {inc[2]:.9f}")
