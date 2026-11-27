#!/usr/bin/env python3
"""Check 3: convex case, the junction with the uniform cube, the pair identity, ferromagnets against the uniform cube."""
import numpy as np, time
from scipy.optimize import minimize, minimize_scalar
from tv_lib import *
t0 = time.time()
def kl(a, p): return a * np.log(a / p) + (1 - a) * np.log((1 - a) / (1 - p))
def R_unif(e, u):
    L1 = np.log(2 / (1 + np.exp(-u))); rho = (L1 + e) / u
    return float(kl(rho, 0.5)) if rho < 0.5 else 0.0
def best_binary(M, e, starts, maxfev=260):
    def f(p):
        m, a, b = p
        if not (0.02 < m < 0.98 and 0.005 < a < 0.995 and 0.005 < b < 0.995): return 1.0
        lam = np.array([m, 1 - m]); mu = np.array([1 - a, b])
        Bv = e + alpha(M, lam, mu)
        if Bv < float(M.v((lam * mu).sum())): return 1.0
        return -r_fast(M, lam, mu, Bv)
    best = (0, None)
    for st in starts:
        r = minimize(f, st, method="Nelder-Mead", options={"xatol": 1e-6, "fatol": 1e-11, "maxfev": maxfev})
        if -r.fun > best[0]: best = (-r.fun, r.x)
    return best
print("== F. junction with the uniform cube (B = 0, u = 1, e = 0): symmetric shells and general binary centres")
print(f"   R_unif(0) = {R_unif(0, 1):.7f};  bJ* = 1 + u c2/(2L) with rho = Lambda_1/u:")
L1 = np.log(2 / (1 + np.exp(-1.0))); rho = L1; c2 = 1 / (2 * rho * (1 - rho)) - 2; L = np.log((1 - rho) / rho)
print(f"   rho = {rho:.6f}, c2 = {c2:.6f}, L = {L:.6f}, bJ* = {1 + c2 / (2 * L):.5f}")
for bJ, claim in [(0.9, 0.0291391), (1.10, 0.0291391), (1.12, 0.0291391), (1.14, 0.0290694), (1.20, 0.0283097), (1.75, 0.0230260)]:
    M = Model(curie_weiss(bJ, 0.0), 1.0)
    r = minimize_scalar(lambda x: -r_of_e(M, np.array([0.5, 0.5]), np.array([1 - x, x]), 0.0), bounds=(0.22, 0.40), method="bounded", options={"xatol": 1e-7})
    print(f"   bJ = {bJ:.2f}: max over symmetric shells {-r.fun:.7f} at x = {r.x:.4f}   (report {claim:.7f});  ratio to R_unif {-r.fun / R_unif(0, 1):.5f}   [{time.time()-t0:.0f}s]", flush=True)
print("== G. one phase with a field (bJ = 0.5, bB = 0.3, u = 1), e = 0.029737: report R_H = 0.011685 (centre type 0.4282)")
M = Model(curie_weiss(0.5, 0.3), 1.0)
val, arg = best_binary(M, 0.029737, ([0.43, 0.3, 0.2], [0.5, 0.3, 0.3], [0.4, 0.35, 0.15]))
print(f"   best binary: {val:.7f} at (m, a, b) = {np.round(arg, 4)}   [{time.time()-t0:.0f}s]", flush=True)
# cone formula for the same model:  max_m min{MI(z) : u rho(z) + v(kappa_z) - Lambda_m <= e},  Lambda_m = min_z [MI + I + u rho]
def cone_formula(M, e, ms, G=700):
    a = np.linspace(0, 1, G); A, Bb = np.meshgrid(a, a, indexing="ij")
    out = (0, None)
    for m in ms:
        kap = m * (1 - A) + (1 - m) * Bb; rho_ = m * A + (1 - m) * Bb
        mi = hb(kap) - m * hb(A) - (1 - m) * hb(Bb)
        Lam = (mi + M.I(kap) + M.u * rho_).min()
        feas = M.u * rho_ + M.v(kap) - Lam <= e
        val = mi[feas].min() if feas.any() else np.inf
        if val > out[0]: out = (val, m)
    return out
cf = cone_formula(M, 0.029737, np.linspace(0.3, 0.6, 31))
print(f"   cone formula (grid 700): {cf[0]:.6f} at m = {cf[1]:.3f}   [{time.time()-t0:.0f}s]", flush=True)
print("== H. pair identity at the two-phase binary optimum (bJ = 1.5, B = 0, u = 1): n_mu(X) at X = S(e) = e + R(e)")
M = Model(curie_weiss(1.5, 0.0), 1.0)
def n_mu_direct(M, lam, mu, X, G=2400):
    """min{MI(nu) : MI(nu) + u dist + v(nu_bar) - alpha(mu) <= X} on a fine grid over (nu_1, nu_0), then polished by SLSQP"""
    ax = np.linspace(0, 1, G); N1, N0 = np.meshgrid(ax, ax, indexing="ij")
    nb = lam[0] * N1 + lam[1] * N0
    mi = hb(nb) - lam[0] * hb(N1) - lam[1] * hb(N0)
    g = mi + M.u * (lam[0] * np.abs(N1 - mu[0]) + lam[1] * np.abs(N0 - mu[1])) + M.v(nb) - alpha(M, lam, mu) - X
    val = np.where(g <= 0, mi, np.inf)
    i = np.unravel_index(np.argsort(val, axis=None)[:5], val.shape)
    best = float(val[i[0][0], i[1][0]])
    cons = {"type": "ineq", "fun": lambda z: X + alpha(M, lam, mu) - float(MI(lam, z)) - M.u * float((lam * np.abs(z - mu)).sum()) - float(M.v((lam * z).sum()))}
    for a, b in zip(i[0], i[1]):
        r = minimize(lambda z: float(MI(lam, z)), [ax[a], ax[b]], bounds=[(1e-9, 1 - 1e-9)] * 2, constraints=[cons], method="SLSQP", options={"ftol": 1e-15, "maxiter": 300})
        if r.success and cons["fun"](r.x) > -1e-10: best = min(best, float(r.fun))
    return best
for e, x, R in [(0.0, 0.29803, 0.0251012), (0.02, 0.30553, 0.0152765), (-0.05, 0.2821, 0.0575961)]:
    lam = np.array([0.5, 0.5]); mu = np.array([1 - x, x])
    X = e + R
    nd = n_mu_direct(M, lam, mu, X)
    # through r_mu:  n_mu(X) = min{ r_mu(e') : e' + r_mu(e') <= X }
    es = np.linspace(e - 0.01, e + 0.01, 81)
    rv = np.array([r_of_e(M, lam, mu, ee) for ee in es])
    ok = es + rv <= X + 1e-12
    print(f"   e = {e:+.3f}: R = {R:.7f}, X = {X:.7f}:  n_mu direct = {nd:.7f},  through r_mu = {rv[ok].min():.7f}   [{time.time()-t0:.0f}s]", flush=True)
print("== I. shell-cone directly: theta_shell(X; mu0) = min{MI : G_mu0(nu) - min G_mu0 <= X}, mu0 = optimal shell, X = S(0); and the cone around a point")
def theta_shell(M, m, mu0, X, G=2400):
    ax = np.linspace(0, 1, G); N1, N0 = np.meshgrid(ax, ax, indexing="ij")
    lam = np.array([m, 1 - m])
    nb = lam[0] * N1 + lam[1] * N0
    mi = hb(nb) - lam[0] * hb(N1) - lam[1] * hb(N0)
    Gf = mi + M.I(nb) + M.u * (lam[0] * np.abs(N1 - mu0[0]) + lam[1] * np.abs(N0 - mu0[1]))
    Gf = Gf - Gf.min()
    return float(mi[Gf <= X].min())
print(f"   shell-cone around (1/2; 0.29803, 0.29803) at X = 0.0251012: {theta_shell(M, 0.5, np.array([1 - 0.29803, 0.29803]), 0.0251012):.6f}   (report 0.0251012)")
print(f"   cone around a point of type 1/2 at the same X: {theta_shell(M, 0.5, np.array([1.0, 0.0]), 0.0251012):.6f}   (report 0.0020379)")
print("== J. ferromagnets are never harder than the uniform cube (T9(e)): random profiles, r_mu(e) <= R_unif(e)")
rng = np.random.default_rng(3); worst = -1
for bJ, bB in [(1.5, 0.0), (0.8, 0.2), (2.0, 0.1)]:
    M = Model(curie_weiss(bJ, bB), 1.0)
    for _ in range(60):
        k = int(rng.integers(2, 5)); lam = rng.dirichlet(np.ones(k) * 2); mu = rng.uniform(0.02, 0.98, k)
        if rng.random() < 0.5:   # profiles near the uniform cube's optimum
            k = 2; lam = np.array([0.5, 0.5]) + rng.normal(0, 0.03) * np.array([1, -1]); mu = np.array([1 - 0.27, 0.27]) + rng.normal(0, 0.03, 2)
        e = float(rng.choice([0.0, 0.01, 0.03]))
        Bv = e + alpha(M, lam, mu)
        if Bv < float(M.v((lam * mu).sum())): continue
        worst = max(worst, r_fast(M, lam, mu, Bv) - R_unif(e, 1.0))
print(f"   largest r_mu(e) - R_unif(e) over 180 profiles, three ferromagnets: {worst:+.2e}   [{time.time()-t0:.0f}s]")
