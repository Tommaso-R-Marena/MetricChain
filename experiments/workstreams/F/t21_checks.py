"""t21: checks of statements of REPORT.md that the other scripts do not cover.
 (i)   Theorem F2(f): dF/dgamma(0,t) = t g(t)/[(1-e^{-tu})(A0^t + A1^t)], g = A0^t (p+q e^{-tu}) - A1^t (q+p e^{-tu});
       it is nonzero with the sign of p - 1/2 on (0,1)  (finite differences).
 (ii)  Theorem F2(c): R_gamma(e) = max_m min{ I : u rho - Lam_m + v_gamma(kappa) <= e } for gamma != 0.
 (iii) Theorem F4(a): type-wise quantiles are Lipschitz and the truncation psi^{tr,q} is in L_u (brute force, n <= 10).
 (iv)  Theorem F4(c): ln[A(psi_s)/A(psi_s^{tr})] >= n F_m(theta + 3 ln(n+1)/n) - 5 ln(n+2) (exact sums, n up to 2000)."""
import math, time, numpy as np
from scipy.optimize import minimize, minimize_scalar
from flib import *
from birad import *
t0 = time.time()
rng = np.random.default_rng(21)

# (i)
worst = 0.0; sign_ok = True
for _ in range(4000):
    p = rng.uniform(0.02, 0.98); u = rng.uniform(0.1, 5); t = rng.uniform(0.02, 0.98)
    q = 1 - p
    A0, A1 = q + p * math.exp(-u), p + q * math.exp(-u)
    g = A0 ** t * (p + q * math.exp(-t * u)) - A1 ** t * (q + p * math.exp(-t * u))
    form = t * g / ((1 - math.exp(-t * u)) * (A0 ** t + A1 ** t))
    hh = 1e-5
    fd = (float(F_game(p, u, hh, t)) - float(F_game(p, u, -hh, t))) / (2 * hh)
    worst = max(worst, abs(form - fd))
    if abs(p - 0.5) > 0.01 and (form > 0) != (p > 0.5):
        sign_ok = False
print(f"(i) derivative formula vs central differences: max abs error {worst:.2e}; sign of dF/dgamma(0,t) = sign(p - 1/2) in all cases: {sign_ok}")

# (ii)
def maxmin_gamma(st, gam, e):
    lnZ = math.log(st.q + st.p * math.exp(-gam))
    c = lambda m, x, y: st.u * (m * x + (1 - m) * y) - st.Lam(m) - gam * (m * (1 - x) + (1 - m) * y) - lnZ
    def inner(m):
        cons = [{"type": "ineq", "fun": lambda z: e - c(m, z[0], z[1])}]
        best = math.inf
        for w in (0.2, 0.5, 0.8):
            xi, yi = w, 1 - w
            if c(m, xi, yi) <= e:
                return 0.0
            lo, hi = 0.0, 1.0
            for _ in range(60):
                mid = (lo + hi) / 2
                if c(m, 1e-6 + mid * (xi - 1e-6), 1e-6 + mid * (yi - 1e-6)) <= e: lo = mid
                else: hi = mid
            z0 = [1e-6 + lo * (xi - 1e-6), 1e-6 + lo * (yi - 1e-6)]
            res = minimize(lambda z: hs(m * (1 - z[0]) + (1 - m) * z[1]) - m * hs(z[0]) - (1 - m) * hs(z[1]), z0, method="SLSQP",
                           constraints=cons, bounds=[(1e-12, 1 - 1e-12)] * 2, options=dict(ftol=1e-15, maxiter=500))
            if c(m, res.x[0], res.x[1]) <= e + 1e-10:
                best = min(best, hs(m * (1 - res.x[0]) + (1 - m) * res.x[1]) - m * hs(res.x[0]) - (1 - m) * hs(res.x[1]))
        return best
    ms = np.linspace(0.02, 0.98, 49)
    vals = [inner(m) for m in ms]
    i = int(np.argmax(vals))
    res = minimize_scalar(lambda m: -inner(m), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, 48)]), method="bounded", options=dict(xatol=1e-10))
    return max(vals[i], -res.fun)
worst = 0.0
for p, u in ((0.1, 2.0), (0.3, 1.0), (0.6, 1.5)):
    st = Site(p, u)
    for gam in (-0.6 * u, 0.3 * u, 0.9 * u):
        thr = thr_additive(p, u, gam)
        for frac in (0.0, 0.4):
            e = frac * thr
            worst = max(worst, abs(maxmin_gamma(st, gam, e) - R_additive(p, u, gam, e)[0]))
print(f"(ii) max-min form of R_gamma against the game formula, 18 cases with gamma != 0: max abs difference {worst:.2e}")

# (iii)
def cube(n):
    N = 2 ** n; idx = np.arange(N)
    pop = np.array([bin(x).count("1") for x in range(N)])
    return pop, pop[idx[:, None] ^ idx[None, :]]
bad = 0; checks = 0
for n in (6, 8, 10):
    pop, D = cube(n)
    for trial in range(30):
        u = float(rng.choice([0.5, 1.0, 2.0]))
        N = 2 ** n
        kind = trial % 4
        idx = rng.choice(N, size=int(rng.integers(1, 7)), replace=False)
        v = rng.uniform(0, u * n, size=len(idx))
        psi = (v[:, None] + u * D[idx, :]).min(0) if kind == 0 else ((v[:, None] - u * D[idx, :]).max(0) if kind == 1 else
              (u * D[int(rng.integers(N))].astype(float) if kind == 2 else (rng.normal(0, u * n * 0.3, size=N)[:, None] + u * D).min(0)))
        w = np.exp(-psi)
        for q in (0.03, 0.2, 0.6):
            tk = np.zeros(n + 1)
            for k in range(n + 1):
                vals = np.sort(np.unique(w[pop == k]))
                wk = w[pop == k]
                tk[k] = next(tau for tau in vals if (wk > tau).mean() <= q)
            if np.any(np.abs(np.diff(np.log(tk))) > u + 1e-9): bad += 1
            psitr = np.maximum(psi, -np.log(tk)[pop])
            if not (np.abs(psitr[:, None] - psitr[None, :]) <= u * D + 1e-9).all(): bad += 1
            Dset = w > tk[pop]
            if max(Dset[pop == k].mean() for k in range(n + 1)) > q + 1e-12: bad += 1
            if not np.allclose(psitr[~Dset], psi[~Dset]): bad += 1
            checks += 4
print(f"(iii) quantile truncation: {checks} checks on random Lipschitz functions (n = 6, 8, 10), failures: {bad}")

# (iv)
def F_m(st, m, th):
    """min{ Icone_m(z) : I_m(z) <= th }"""
    obj = lambda z: m * kls(z[0], st.eta1) + (1 - m) * kls(z[1], st.eta0)
    Ifun = lambda z: hs(m * (1 - z[0]) + (1 - m) * z[1]) - m * hs(z[0]) - (1 - m) * hs(z[1])
    if Ifun([st.eta1, st.eta0]) <= th:
        return 0.0
    best = math.inf
    for w in (0.3, 0.5, 0.7):
        xi, yi = w, 1 - w
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if Ifun([st.eta1 + mid * (xi - st.eta1), st.eta0 + mid * (yi - st.eta0)]) > th: lo = mid
            else: hi = mid
        z0 = [st.eta1 + hi * (xi - st.eta1), st.eta0 + hi * (yi - st.eta0)]
        res = minimize(obj, z0, method="SLSQP", constraints=[{"type": "ineq", "fun": lambda z: th - Ifun(z)}],
                       bounds=[(1e-12, 1 - 1e-12)] * 2, options=dict(ftol=1e-15, maxiter=500))
        best = min(best, obj(z0))
        if Ifun(res.x) <= th + 1e-10:
            best = min(best, obj(res.x))
    return best
ok = True; rows = []
for p, u in ((0.1, 2.0), (0.3, 1.0)):
    st = Site(p, u)
    for n in (500, 1000, 2000):
        for m in (0.3, 0.5):
            k = int(round(m * n)); mm = k / n
            C = Centre(n, k, p)
            for th in (0.02, 0.05):
                inside, mx = C.density_ball(-n * th)
                # rho_t: first distance outside D on each type diagonal; truncated weight e^{-u rho_t} on D
                dist = C.dist.astype(float)
                big = np.where(inside, np.inf, dist)
                rho_t = np.full(n + 1, np.inf)
                np.minimum.at(rho_t, C.t.ravel(), big.ravel())
                lw0 = -u * dist
                lw1 = np.where(inside, -u * rho_t[C.t], lw0)
                assert is_lipschitz_grid(lw1, u)
                drop = C.logA(lw0) - C.logA(lw1)
                bound = n * F_m(st, mm, th + 3 * math.log(n + 1) / n) - 5 * math.log(n + 2)
                lim = F_m(st, mm, th)
                ok &= drop >= bound - 1e-9
                rows.append((p, u, n, m, th, drop / n, bound / n, lim))
for r in rows[::3]:
    print("     p=%.1f u=%.1f n=%d m=%.1f theta=%.2f: exact drop/n = %.5f >= bound/n = %.5f   (limit F_m(theta) = %.5f)" % r)
print(f"(iv) truncated cones: exact drop of ln A is at least the bound of Theorem F4(c) in all {len(rows)} cases: {ok}")
print("time %.0fs" % (time.time() - t0))
