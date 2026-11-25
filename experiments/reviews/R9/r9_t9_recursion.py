# R9 test 9: the level recursion  T_{k+1} = min(T_k, R[T_k]),
#   R[T](g) = inf_{0<phi<1, 0<beta<g} sup_{gamma>=beta} [ min(gamma, phi*theta_na((g-beta)/phi)) + (1-phi) T(gamma/(1-phi)) ],
# with the pair (theta_na, R^max) of the report (own code, own grids).
#  (1) super-solution property on random tuples, evaluated with the exact functions (no grid in g):
#      sup_gamma [...] with T = R^max is >= R^max(g) for every (phi, beta, g);
#  (2) the iteration on a grid from T_1 = theta_na and from T_1 = ln 2: never below R^max; distance to R^max after K levels;
#  (3) mutation: the same recursion with theta_na replaced by R_0 o (id + R_0)^{-1} (the pair of the instance g = 0)
#      falls below R^max, i.e. below the lower bound of Theorem F1(a).
# usage: python3 r9_t9_recursion.py p u K
import numpy as np, sys, time
from math import log
from r9lib import Par
p, u, K = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3])
t0 = time.time(); rng = np.random.default_rng(5)
P = Par(p, u); E, gE, E0 = P.E(); a = -P.ec(); ts, Fs, _ = P.table()
def Rv(e):
    e = np.atleast_1d(np.asarray(e, dtype=float)); out = np.empty(e.size)
    for i in range(0, e.size, 4000):
        ee = e.ravel()[i:i + 4000]
        out[i:i + 4000] = np.maximum((Fs[None, :] - ts[None, :] * ee[:, None]).max(axis=1), np.maximum(0.0, -ee))
    return out.reshape(e.shape)
# theta_na = R o S^{-1}: parametric table (x = e + R(e), theta = R(e)), e in [-a, E]
eg = np.concatenate([np.linspace(-a, 0, 6001)[:-1], np.linspace(0, E, 6001)])
Rg = Rv(eg); xg = eg + Rg
keep = np.concatenate([[True], np.diff(xg) > 1e-15]); xg, thg = xg[keep], Rg[keep]
def theta_na(x):
    x = np.asarray(x, dtype=float)
    return np.where(x >= E, 0.0, np.interp(np.clip(x, 0, E), xg, thg))
def Rmax(e): return Rv(e)
print(f"p={p} u={u}: E={E:.6f} a={a:.6f} h={float(Rmax(0.0)[0]):.6f}; theta_na(h)-h = {float(theta_na(float(Rmax(0.0)[0])))-float(Rmax(0.0)[0]):+.2e}")
# (1) super-solution on random tuples
worst = np.inf
for trial in range(20000):
    g = E * rng.uniform(0.001, 1.0); phi = rng.uniform(0.001, 0.999); beta = g * rng.uniform(0.0005, 0.999)
    mu = phi * float(theta_na((g - beta) / phi))
    gam = np.concatenate([[beta, max(beta, mu)], np.linspace(beta, max(beta, mu), 40)])
    br = np.minimum(gam, mu) + (1 - phi) * Rmax(gam / (1 - phi))
    worst = min(worst, float(br.max()) - float(Rmax(g)[0]))
print(f"(1) 20000 random (phi, beta, g): min over tuples of [sup_gamma bracket(T = R^max) - R^max(g)] = {worst:+.3e}  (must be >= 0)")
# (2) iteration on grids
N = 240
gg = E * (np.arange(1, N + 1) / N) ** 1.6
phis = np.unique(np.concatenate([np.linspace(0.01, 0.99, 99), 1 - np.geomspace(1e-3, 0.3, 30), np.geomspace(1e-3, 0.3, 30)]))
betas = np.geomspace(1e-4, 0.9, 20)
def step(T, tna):
    """T: values on gg (T(y) for y > E taken as T(E) continued: for the report's families T = 0 beyond E only if T_1 = theta_na)"""
    def Tfun(y):
        return np.where(y >= gg[-1], T[-1], np.interp(y, gg, T, left=T[0]))   # T(0+) := T[0] (upper bound: T nonincreasing)
    out = np.empty(N)
    for i, g in enumerate(gg):
        ph = phis[:, None, None]; be = (g * betas)[None, :, None]
        mu = ph * tna((g - be) / ph)                                   # (nphi, nbeta, 1)
        top = np.maximum(be, mu)
        s = np.linspace(0, 1, 48)[None, None, :]
        gam = be + s * (top - be)                                      # includes gamma = beta and gamma = max(beta, mu)
        br = np.minimum(gam, mu) + (1 - ph) * Tfun(gam / (1 - ph))
        out[i] = br.max(axis=2).min()
    return np.minimum(T, out)
Rgg = Rmax(gg)
for name, T1, tna in (('T_1 = theta_na', theta_na(gg), theta_na), ('T_1 = ln 2', np.full(N, log(2.0)), theta_na)):
    T = T1.copy(); below = 0.0
    idx = [int(np.argmin(np.abs(gg - f * E))) for f in (0.001, 0.02, 0.1, 0.25, 0.5, 0.75)]
    print(f"(2) {name}; columns g/E = 0.001, 0.02, 0.1, 0.25, 0.5, 0.75; entries T_k/a")
    for k in range(1, K + 1):
        if k in (1, 2, 3, 4, 6, 8, 12, K):
            print(f"    k={k:2d}: " + " ".join(f"{T[i]/a:.4f}" for i in idx) + f"   min(T_k - R^max) = {np.min(T - Rgg):+.2e}, max(T_k - R^max)/a = {np.max(T - Rgg)/a:.4f}   [{time.time()-t0:.0f}s]")
            sys.stdout.flush()
        below = min(below, float(np.min(T - Rgg)))
        if k < K: T = step(T, tna)
    print("    R^max/a: " + " ".join(f"{Rgg[i]/a:.4f}" for i in idx) + f";   R_0/a: " + " ".join(f"{P.R0(gg[i])/a:.4f}" for i in idx))
    print(f"    most negative T_k - R^max over all levels: {below:+.2e}")
# (3) mutation: pair of g = 0
R0g = np.array([P.R0(e) for e in eg]); x0 = eg + R0g
order = np.argsort(x0); x0s, th0s = x0[order], R0g[order]
kp = np.concatenate([[True], np.diff(x0s) > 1e-15]); x0s, th0s = x0s[kp], th0s[kp]
def theta_na0(x):
    x = np.asarray(x, dtype=float)
    return np.where(x >= E0, 0.0, np.interp(np.clip(x, x0s[0], E0), x0s, th0s))
T = theta_na0(gg).copy()
for k in range(1, min(K, 10)): T = step(T, theta_na0)
print(f"(3) mutation (theta_na replaced by R_0 o (id+R_0)^-1): after {min(K,10)} levels min(T_k - R^max)/a = {np.min(T - Rgg)/a:+.4f}  (negative = below the lower bound)")
print(f"[{time.time()-t0:.0f}s]")
