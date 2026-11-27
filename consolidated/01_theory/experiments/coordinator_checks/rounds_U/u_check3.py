#!/usr/bin/env python3
"""Coordinator's check of workstream U, Corollary U1.1: the round-limited recursion, three rounds at bounded accuracy.

T1 = theta_na;  T2(g) = min{theta_na(g), inf_{phi, beta, xi1 > xi2 = beta/(1-phi)} max{ mu + (1-phi) theta_na(xi1), min(mu, (1-phi) xi1) + (1-phi) theta_na(xi2) }},
mu = phi theta_na((g - beta)/phi)  (g > 0);   at g = 0: xi_L = 0, mu = phi a.
T3(0) = min over the ladders (1,1,1), (2,1), (1,2).  Every grid value is an upper bound for the recursion (a minimum over fewer points)."""
import numpy as np, math, time
u = 1.0
pu = 1/(1+math.exp(u)); L1 = math.log(2/(1+math.exp(-u)))
f = lambda r: r*np.log(2*r) + (1-r)*np.log(2*(1-r))
rho = np.linspace(pu, 0.5, 400001)
kk = f(rho) + u*rho - L1; ff = f(rho)
estar = float(kk[-1]); a = float(ff[0]); h = float(f(L1/u))
def th(e):
    e = np.asarray(e, float)
    return np.where(e >= estar, 0.0, np.interp(np.clip(e, 0, estar), kk, ff))
t0 = time.time()
# ---- T2 on a grid of accuracies
gs = np.linspace(0, estar, 97)
T2 = np.zeros_like(gs)
phis = np.linspace(0.02, 0.98, 97)[:, None, None]
for i, g in enumerate(gs):
    if i == 0:
        xi1 = np.linspace(1e-6, estar, 1500)[None, :, None]
        mu = phis * a
        v = np.maximum(mu + (1-phis)*th(xi1), np.minimum(mu, (1-phis)*xi1) + (1-phis)*a)
        T2[i] = min(a, float(v.min()))
    else:
        betas = np.linspace(g*0.01, g*0.99, 60)[None, None, :]
        xi2 = betas/(1-phis)
        mu = phis*th((g - betas)/phis)
        fr = np.linspace(0.0, 1.0, 140)[None, :, None]            # xi1 = xi2 + fr (estar - xi2)_+   (xi1 >= xi2)
        xi1 = xi2 + fr*np.maximum(estar - xi2, 0.0)
        v = np.maximum(mu + (1-phis)*th(xi1), np.minimum(mu, (1-phis)*xi1) + (1-phis)*th(xi2))
        T2[i] = min(float(th(g)), float(v.min()))
print(f"T2(0)/a = {T2[0]/a:.4f}   (closed form 0.6243);  T2 at g/estar = 0.1, 0.25, 0.5: {np.interp([0.1*estar, 0.25*estar, 0.5*estar], gs, T2)/a}  against theta_na/a = {th([0.1*estar, 0.25*estar, 0.5*estar])/a}   [{time.time()-t0:.0f}s]")
assert np.all(T2 <= th(gs) + 1e-12) and np.all(np.diff(T2) <= 1e-9), "T2 must be below theta_na and nonincreasing"
hint = f(np.clip((L1 + gs)/u, 0, 0.5)); hint = np.where((L1 + gs)/u >= 0.5, 0, hint)
print(f"lower barrier: min over the grid of T2 - theta_hint = {float((T2 - hint).min()):+.2e}  (must be >= 0)")
T2f = lambda x: np.interp(x, gs, T2)
# ---- T3(0)
phis2 = np.linspace(0.02, 0.98, 481)[:, None]
xi = np.linspace(1e-6, estar, 1500)[None, :]
mu = phis2*a
v21 = np.maximum(mu + (1-phis2)*T2f(xi), np.minimum(mu, (1-phis2)*xi) + (1-phis2)*a)
v12 = np.maximum(mu + (1-phis2)*th(xi), np.minimum(mu, (1-phis2)*xi) + (1-phis2)*T2[0])
# (1,1,1)
p3 = np.linspace(0.02, 0.98, 241)[:, None, None]
x1 = np.linspace(1e-6, estar, 300)[None, :, None]; x2 = np.linspace(1e-6, estar, 300)[None, None, :]
m3 = p3*a
v111 = np.maximum(np.maximum(m3 + (1-p3)*th(x1), np.minimum(m3, (1-p3)*x1) + (1-p3)*th(x2)), np.minimum(m3, (1-p3)*x2) + (1-p3)*a)
v111 = np.where(x1 > x2, v111, np.inf)
print(f"three rounds at bounded accuracy, u = 1:  ladder (2,1): {v21.min()/a:.4f} a;  (1,2): {v12.min()/a:.4f} a;  (1,1,1): {v111.min()/a:.4f} a;  T3(0) <= {min(v21.min(), v12.min(), v111.min(), T2[0])/a:.4f} a   (workstream: 0.541 a;  h/a = {h/a:.4f})   [{time.time()-t0:.0f}s]")
