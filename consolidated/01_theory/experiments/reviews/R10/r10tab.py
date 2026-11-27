"""helpers for the spot checks of the tables (own code)."""
import numpy as np
from scipy import optimize
from r10lib import *
from r10search import *


def R_binary(model, e, land=None, starts=None, kw=None):
    """sup over binary centres (m; a, b) of r_mu(e) for the landscape `land` (default v)."""
    kw = dict(kw or {})
    if land is not None:
        kw['land'] = land
    if starts is None:
        starts = [(0.5, 0.3, 0.3), (0.45, 0.33, 0.27), (0.55, 0.27, 0.33), (0.4, 0.25, 0.3), (0.6, 0.3, 0.25)]
    best = (-1.0, None, None)
    for (m, a, b) in starts:
        val, l2, m2 = nm(model, e, *binary(m, a, b), kw=kw, maxiter=1500)
        if val > best[0]:
            best = (val, l2, m2)
    return best


def landscape_gamma(model, gamma):
    """lambda_gamma(kappa) = -gamma*kappa + min_k'[I(k') + gamma k'] (largest affine minorant of I with slope -gamma)"""
    g = model.grid
    f = model.Ig + gamma * g
    i = int(np.argmin(f))
    res = optimize.minimize_scalar(lambda k: float(model.I(k)) + gamma * k,
                                   bounds=(g[max(i - 2, 0)], g[min(i + 2, len(g) - 1)]), method='bounded',
                                   options={'xatol': 1e-14})
    c = min(float(f[i]), float(res.fun))
    return lambda k: -gamma * np.asarray(k, float) + c


def E_threshold(model, land=None, starts=None):
    """E = sup_mu { min_c [u*dist(c*1, mu) + land(c)] - alpha(mu) } over binary profiles
    (R_lambda(e) > 0 iff no constant exit is feasible for some profile)."""
    land = model.v if land is None else land
    u = model.u
    cg = np.linspace(0, 1, 4001)
    lg = land(cg)

    def val(theta):
        lam, mu = prof(theta, 2)
        d = np.abs(cg[:, None] - mu[None, :]) @ lam
        f = u * d + lg
        i = int(np.argmin(f))
        # refine: the minimum of a piecewise smooth function; the kinks are at the atoms
        cand = [f[i]]
        for c in mu:
            cand.append(u * float(np.abs(c - mu) @ lam) + float(land(c)))
        lo, hi = cg[max(i - 1, 0)], cg[min(i + 1, 4000)]
        r = optimize.minimize_scalar(lambda c: u * float(np.abs(c - mu) @ lam) + float(land(c)), bounds=(lo, hi), method='bounded', options={'xatol': 1e-13})
        cand.append(r.fun)
        return -(min(cand) - alpha(model, lam, mu))
    if starts is None:
        starts = [(0.5, 0.27, 0.27), (0.45, 0.3, 0.25), (0.55, 0.25, 0.3), (0.6, 0.3, 0.2), (0.4, 0.2, 0.3)]
    best = -np.inf
    arg = None
    for (m, a, b) in starts:
        x0 = unprof(*binary(m, a, b))
        res = optimize.minimize(val, x0, method='Nelder-Mead', options={'xatol': 1e-10, 'fatol': 1e-14, 'maxiter': 3000})
        if -res.fun > best:
            best, arg = -res.fun, prof(res.x, 2)
    return best, arg


def cone_shell(model, m, convex=False, G=161):
    """Gibbs shell of the cone around a centre of type m: argmin over nu = (nu1, nu0) of
    MI(nu) + I(nubar) + u*(m(1-nu1) + (1-m) nu0).  returns (Lam_m, nu)."""
    lam = np.array([m, 1 - m])
    u = model.u

    def Gf(nu):
        nu = np.clip(nu, 1e-12, 1 - 1e-12)
        return MI(lam, nu) + float(model.I(lam @ nu)) + u * (m * (1 - nu[0]) + (1 - m) * nu[1])
    g = np.linspace(0.002, 0.998, G)
    n1, n0 = np.meshgrid(g, g, indexing='ij')
    nb = m * n1 + (1 - m) * n0
    F = h(nb) - m * h(n1) - (1 - m) * h(n0) + model.I(nb) + u * (m * (1 - n1) + (1 - m) * n0)
    idx = np.argsort(F.ravel())[:1 if convex else 6]
    best = (np.inf, None)
    for i in idx:
        x0 = np.array([n1.ravel()[i], n0.ravel()[i]])
        res = optimize.minimize(Gf, x0, method='L-BFGS-B', bounds=[(1e-9, 1 - 1e-9)] * 2, options={'ftol': 1e-15, 'gtol': 1e-12})
        res2 = optimize.minimize(Gf, res.x, method='Nelder-Mead', options={'xatol': 1e-11, 'fatol': 1e-15})
        if res2.fun < best[0]:
            best = (float(res2.fun), np.clip(res2.x, 0, 1))
    return best


def a_cone(model, convex=False, ms=None):
    """max_m MI(z_c(m)): vanishing-accuracy exponent of truncated cones around points"""
    if ms is None:
        ms = np.linspace(0.05, 0.95, 37)
    vals = [MI(np.array([m, 1 - m]), cone_shell(model, m, convex)[1]) for m in ms]
    i = int(np.argmax(vals))
    res = optimize.minimize_scalar(lambda m: -MI(np.array([m, 1 - m]), cone_shell(model, m, convex)[1]),
                                   bounds=(ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]), method='bounded', options={'xatol': 1e-8})
    return -res.fun, res.x


def R_cone(model, e, land=None, ms=None, convex=False):
    """cone formula max_m min{MI(z): u*rho(z) + land(kappa_z) - Lam_m <= e}"""
    kw = {} if land is None else {'land': land}

    def term(m):
        Lm, _ = cone_shell(model, m, convex)
        lam = np.array([m, 1 - m])
        mu = np.array([1.0, 0.0])
        return inner_clip(model, lam, mu, e + Lm, **kw)[0]
    if ms is None:
        ms = np.linspace(0.1, 0.9, 33)
    vals = [term(m) for m in ms]
    i = int(np.argmax(vals))
    res = optimize.minimize_scalar(lambda m: -term(m), bounds=(ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]), method='bounded', options={'xatol': 1e-8})
    return max(-res.fun, vals[i]), res.x


def n_mu(model, lam, mu, X, ne=240, kw=None, land=None):
    """n_mu(X) = min{ MI(nu) : MI(nu) + u*dist + v(nubar) - alpha(mu) <= X } = r_mu(e_max),
    e_max = max{ e : e + r_mu(e) <= X }  (Theorem T8(b)); scan in e from X downwards, then bisection."""
    kw = dict(kw or {})
    if land is not None:
        kw['land'] = land
    al = alpha(model, lam, mu)
    emin = float((land or model.v)(float(np.dot(lam, mu)))) - al      # admissible e >= emin
    es = np.linspace(X, emin, ne)
    prev = None
    for e in es:
        r = inner_clip(model, lam, mu, e + al, **kw)[0]
        if e + r <= X:
            if prev is None:
                return r, e
            lo, hi = e, prev                                         # feasible at lo, infeasible at hi
            rlo = r
            for _ in range(50):
                mid = 0.5 * (lo + hi)
                rm = inner_clip(model, lam, mu, mid + al, **kw)[0]
                if mid + rm <= X:
                    lo, rlo = mid, rm
                else:
                    hi = mid
            return rlo, lo
        prev = e
    return MI(lam, mu), emin


def n_mu_grid(model, lam, mu, X, G=161, zooms=5, ncand=4, land=None):
    """n_mu(X) by a direct two-parameter search over clippings (clo <= chi):
    min MI(clip) subject to MI(clip) + u*dist + land(type) <= X + alpha(mu).  Grid + zoom around the
    best feasible points; the value is attained at a feasible clipping (upper bound of n_mu)."""
    from r10lib import _h
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    land = model.v if land is None else land
    al = alpha(model, lam, mu)
    u = model.u

    def ev(clo, chi):
        nu = np.minimum(np.maximum(mu, clo[..., None]), chi[..., None])
        typ = nu @ lam
        mi = _h(typ) - _h(nu) @ lam
        con = mi + u * (np.abs(nu - mu) @ lam) + land(typ) - al - X
        return np.where((con <= 0) & (clo <= chi), mi, np.inf)
    lo = min(float(mu.min()), 0.0)
    g = np.unique(np.concatenate((np.linspace(0.0, 1.0, G), mu)))
    A, Bc = np.meshgrid(g, g, indexing='ij')
    F = ev(A, Bc)
    if not np.isfinite(F).any():
        return MI(lam, mu)
    order = np.argsort(F.ravel())[:400]
    picked = []
    for o in order:
        i, j = np.unravel_index(o, F.shape)
        if not np.isfinite(F[i, j]):
            break
        if all(abs(i - a) > 2 or abs(j - b) > 2 for a, b in picked):
            picked.append((i, j))
            if len(picked) >= ncand:
                break
    best = float(F.min())
    for (i, j) in picked:
        a0, a1 = g[max(i - 2, 0)], g[min(i + 2, len(g) - 1)]
        b0, b1 = g[max(j - 2, 0)], g[min(j + 2, len(g) - 1)]
        for _ in range(zooms):
            ga = np.linspace(a0, a1, 41)
            gb = np.linspace(b0, b1, 41)
            AA, BB = np.meshgrid(ga, gb, indexing='ij')
            FF = ev(AA, BB)
            if not np.isfinite(FF).any():
                break
            ii, jj = np.unravel_index(int(np.argmin(FF)), FF.shape)
            best = min(best, float(FF[ii, jj]))
            a0, a1 = ga[max(ii - 2, 0)], ga[min(ii + 2, 40)]
            b0, b1 = gb[max(jj - 2, 0)], gb[min(jj + 2, 40)]
    return best
