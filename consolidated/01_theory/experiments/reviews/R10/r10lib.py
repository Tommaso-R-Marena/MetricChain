"""
r10lib.py -- referee R10, own library (numpy/scipy only; nothing imported from the workstream
or from the repository).

Setting: known part f(x) = n*phi(|x|/n), rate function I = phi - h - min(phi - h), v = largest
u-Lipschitz minorant of I.  Block profile = (lam, mu): weights lam_j > 0 (sum 1), mu_j in [0,1].

    MI(mu)     = h(mubar) - sum_j lam_j h(mu_j)
    dist(nu,mu)= sum_j lam_j |nu_j - mu_j|
    alpha(mu)  = MI(mu) + I(mubar)
    V(mu,B;lam)= min{ MI(nu) : u*dist(nu,mu) + landscape(nubar) <= B }
    r_mu(e)    = V(mu, e + alpha(mu); v)

Three inner solvers that share no approximation:
  S1  inner_clip    : two-parameter search over clippings on the boundary curve, landscape = table
                      of v (fast; used in searches).  Returns a FEASIBLE point => upper bound of V.
  S2  inner_dual    : for every exit type kappa' on a grid, the Lagrangian dual of the convex
                      problem "min MI at fixed type and distance budget (B - I(kappa'))/u", with
                      I itself (no table of v, no clipping lemma, no boundary curve).  By weak
                      duality every dual value is a LOWER bound of the minimum at that type.
  S3  inner_primal  : generic multi-start SLSQP over all exit profiles nu (split variables), with
                      I itself in the constraint.  Returns a feasible point => upper bound of V.
"""
import numpy as np
from scipy import optimize, special

EPS = 1e-300


def h(x):
    x = np.asarray(x, dtype=float)
    y = np.clip(x, 0.0, 1.0)
    with np.errstate(divide='ignore', invalid='ignore'):
        a = np.where(y > 0, -y * np.log(np.where(y > 0, y, 1.0)), 0.0)
        b = np.where(y < 1, -(1 - y) * np.log(np.where(y < 1, 1 - y, 1.0)), 0.0)
    return a + b


def kl(x, p):
    """binary relative entropy KL(x||p), scalars or arrays"""
    x = np.asarray(x, dtype=float)
    p = np.asarray(p, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        a = np.where(x > 0, x * np.log(np.where(x > 0, x, 1.0) / p), 0.0)
        b = np.where(x < 1, (1 - x) * np.log(np.where(x < 1, 1 - x, 1.0) / (1 - p)), 0.0)
    return a + b


def logit(x):
    return np.log(x / (1 - x))


def sigm(t):
    return 1.0 / (1.0 + np.exp(-t))


class Model:
    """rate function of a function-of-type known part; default Curie-Weiss."""

    def __init__(self, bJ=1.5, bB=0.0, u=1.0, phi=None, N=400001):
        self.bJ, self.bB, self.u = bJ, bB, u
        if phi is None:
            self.phi = lambda k: -(bJ / 2.0) * (2 * k - 1) ** 2 - bB * (2 * k - 1)
        else:
            self.phi = phi
        # minimum of phi - h on [0,1]: dense grid + polishing
        g = np.linspace(0.0, 1.0, 200001)
        f = self.phi(g) - h(g)
        i0 = int(np.argmin(f))
        lo, hi = g[max(i0 - 2, 0)], g[min(i0 + 2, len(g) - 1)]
        res = optimize.minimize_scalar(lambda k: float(self.phi(k) - h(k)), bounds=(lo, hi),
                                       method='bounded', options={'xatol': 1e-15})
        self.c0 = min(float(f[i0]), float(res.fun))
        self.kmin = float(res.x) if res.fun <= f[i0] else float(g[i0])
        # table of v
        self.N = N
        self.grid = np.linspace(0.0, 1.0, N)
        Ig = self.I(self.grid)
        d = 1.0 / (N - 1)
        idx = np.arange(N)
        fw = np.minimum.accumulate(Ig - u * d * idx) + u * d * idx
        bw = (np.minimum.accumulate((Ig + u * d * idx)[::-1])[::-1]) - u * d * idx
        self.vg = np.minimum(fw, bw)
        self.Ig = Ig

    def I(self, k):
        return self.phi(np.asarray(k, dtype=float)) - h(k) - self.c0

    def v(self, k):
        return np.interp(k, self.grid, self.vg)

    def contact(self, tol=1e-9):
        """pieces of the contact set {v = I} (from the table)"""
        c = (self.Ig - self.vg) < tol
        out = []
        i = 0
        N = self.N
        while i < N:
            if c[i]:
                j = i
                while j + 1 < N and c[j + 1]:
                    j += 1
                out.append((self.grid[i], self.grid[j]))
                i = j + 1
            else:
                i += 1
        return out


# ------------------------------------------------------------------ profiles

def MI(lam, mu):
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    return float(h(np.dot(lam, mu)) - np.dot(lam, h(mu)))


def alpha(model, lam, mu):
    return MI(lam, mu) + float(model.I(np.dot(lam, mu)))


def binary(m, a, b):
    """binary centre of type m with profile z = (a, b): block S=1 (weight m) has mu = 1-a,
    block S=0 (weight 1-m) has mu = b."""
    return np.array([m, 1 - m]), np.array([1 - a, b])


# ------------------------------------------------------------------ S1: clippings

def _g_only(model, lam, mu, clo, chi, land):
    """constraint value u*dist + land(type) of the clippings nu_j = min(max(mu_j, clo), chi)"""
    nu = np.minimum(np.maximum(mu, clo[..., None]), chi[..., None])
    typ = nu @ lam
    dist = np.abs(nu - mu) @ lam
    return model.u * dist + land(typ)


def _mi_only(lam, mu, clo, chi):
    nu = np.minimum(np.maximum(mu, clo[..., None]), chi[..., None])
    return _h(nu @ lam) - _h(nu) @ lam


def _h(x):
    x = np.clip(x, 0.0, 1.0)
    return special.entr(x) + special.entr(1.0 - x)


def _curve(model, lam, mu, B, par, land, which, rounds=6, sec=16):
    """boundary curve of the feasible set of clippings.
    which = 'lo': par = clo (array); returns for each clo the smallest feasible chi in [clo, 1]
                  (the constraint is nonincreasing in chi) and MI there (inf if none).
    which = 'hi': par = chi; returns the largest feasible clo in [0, chi] and MI there.
    Multi-section: `rounds` rounds with `sec` points each (bracket shrinks by sec-1 each)."""
    par = np.asarray(par, float)
    if which == 'lo':
        lo = par.copy()                    # infeasible end (or feasible: then answer = clo)
        hi = np.ones_like(par)             # feasible end, if feasible at all
        g_end = _g_only(model, lam, mu, par, hi, land)
    else:
        lo = np.zeros_like(par)            # feasible end, if feasible at all
        hi = par.copy()
        g_end = _g_only(model, lam, mu, lo, par, land)
    g_diag = _g_only(model, lam, mu, par, par, land)
    feas = g_end <= B
    diag_ok = g_diag <= B
    w = np.linspace(0.0, 1.0, sec)
    rows = np.arange(len(par))
    for _ in range(rounds):
        pts = lo[:, None] + (hi - lo)[:, None] * w[None, :]          # (G, sec)
        if which == 'lo':
            g = _g_only(model, lam, mu, np.broadcast_to(par[:, None], pts.shape), pts, land)
            ok = g <= B                                              # feasible for large chi
            j = np.argmax(ok, axis=1)                                # first feasible index
            j = np.where(ok.any(axis=1), j, sec - 1)
            j = np.maximum(j, 1)
            lo, hi = pts[rows, j - 1], pts[rows, j]
        else:
            g = _g_only(model, lam, mu, pts, np.broadcast_to(par[:, None], pts.shape), land)
            ok = g <= B                                              # feasible for small clo
            j = sec - 1 - np.argmax(ok[:, ::-1], axis=1)             # last feasible index
            j = np.where(ok.any(axis=1), j, 0)
            j = np.minimum(j, sec - 2)
            lo, hi = pts[rows, j], pts[rows, j + 1]
    if which == 'lo':
        other = np.where(diag_ok, par, hi)
        mi = _mi_only(lam, mu, par, other)
    else:
        other = np.where(diag_ok, par, lo)
        mi = _mi_only(lam, mu, other, par)
    mi = np.where(feas, mi, np.inf)
    return other, mi


def _candidates(F, ncand):
    """indices of the ncand smallest values of F that are pairwise at least 2 apart"""
    order = np.argsort(F, kind='stable')
    picked = []
    for i in order:
        if not np.isfinite(F[i]):
            break
        if all(abs(i - j) >= 2 for j in picked):
            picked.append(int(i))
            if len(picked) >= ncand:
                break
    return picked


def inner_clip(model, lam, mu, B, G=96, zooms=3, ncand=4, nz=21, land=None, both=True,
               rounds=6, sec=16):
    """S1.  min of MI over clippings of mu subject to u*dist + land(type) <= B (land = v by
    default; land must be u-Lipschitz, which makes the constraint monotone in each threshold).
    Returns (value, (clo, chi)).  The value is attained at a feasible clipping, so it is an
    upper bound of V; it equals V up to the scan resolution."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    if land is None:
        land = model.v
    mlo, mhi = float(mu.min()), float(mu.max())
    best = np.inf
    arg = (0.0, 1.0)
    for which in (('lo', 'hi') if both else ('lo',)):
        end = 0.0 if which == 'lo' else 1.0
        base = np.unique(np.clip(np.concatenate(([end], np.linspace(mlo, mhi, G), mu)), 0.0, 1.0))
        oth, F = _curve(model, lam, mu, B, base, land, which, rounds, sec)
        if not np.isfinite(F).any():
            continue
        i = int(np.argmin(F))
        if F[i] < best:
            best = float(F[i])
            arg = (float(base[i]), float(oth[i])) if which == 'lo' else (float(oth[i]), float(base[i]))
        cands = _candidates(F, ncand)
        a = np.array([base[max(i - 1, 0)] for i in cands])
        b = np.array([base[min(i + 1, len(base) - 1)] for i in cands])
        wz = np.linspace(0.0, 1.0, nz)
        for _ in range(zooms):
            gg = a[:, None] + (b - a)[:, None] * wz[None, :]          # (nc, nz)
            oz, Fz = _curve(model, lam, mu, B, gg.ravel(), land, which, rounds, sec)
            Fz = Fz.reshape(gg.shape)
            oz = oz.reshape(gg.shape)
            j = np.argmin(Fz, axis=1)
            rows = np.arange(len(cands))
            jm = int(np.argmin(Fz[rows, j]))
            if Fz[jm, j[jm]] < best:
                best = float(Fz[jm, j[jm]])
                p, o = float(gg[jm, j[jm]]), float(oz[jm, j[jm]])
                arg = (p, o) if which == 'lo' else (o, p)
            a = gg[rows, np.maximum(j - 1, 0)]
            b = gg[rows, np.minimum(j + 1, nz - 1)]
    return best, arg


def r_mu(model, lam, mu, e, **kw):
    """r_mu(e) by S1 (landscape v)."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    B = e + alpha(model, lam, mu)
    if B < float(model.v(np.dot(lam, mu))) - 1e-13:
        return np.nan
    return inner_clip(model, lam, mu, B, **kw)[0]


# ------------------------------------------------------------------ S2: dual per exit type, with I

def _gamma(eta, tau, mu):
    """Gamma_{tau,eta}(mu) = max_nu [h(nu) - eta*nu - tau*|nu - mu|] and the maximiser"""
    a = np.clip(eta + tau, -700, 700)
    b = np.clip(eta - tau, -700, 700)
    nplus = 1.0 / (1.0 + np.exp(a))    # h'(nu) = eta + tau   (raised blocks)
    nminus = 1.0 / (1.0 + np.exp(b))   # h'(nu) = eta - tau   (lowered blocks), nminus >= nplus
    nu = np.minimum(np.maximum(mu, nplus), nminus)
    val = h(nu) - eta * nu - tau * np.abs(nu - mu)
    return val, nu


def dual_fixed_type(lam, mu, kp, r, x0=None):
    """max over {nu: nubar = kp, dist(nu,mu) <= r} of sum lam_j h(nu_j), by its dual
    D(eta,tau) = eta*kp + tau*r + sum lam_j Gamma(mu_j), minimised over eta real, tau >= 0.
    Every value of D is an upper bound of the primal maximum (weak duality).
    Returns (Dmin, (eta, tau))."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)

    def D(z):
        eta, tau = z
        val, nu = _gamma(eta, tau, mu)
        f = eta * kp + tau * r + float(lam @ val)
        g = np.array([kp - float(lam @ nu), r - float(lam @ np.abs(nu - mu))])
        return f, g

    if x0 is None:
        kk = min(max(kp, 1e-9), 1 - 1e-9)
        x0 = np.array([np.log((1 - kk) / kk), 0.5])
    res = optimize.minimize(D, x0, jac=True, method='L-BFGS-B',
                            bounds=[(-60, 60), (0, 80)],
                            options={'maxiter': 500, 'ftol': 1e-15, 'gtol': 1e-12})
    return float(res.fun), res.x


def inner_dual(model, lam, mu, B, nk=1601, refine=3, use_v=False, verbose=False):
    """S2.  V(mu,B) = min over exit types kp of  h(kp) - Dmin(kp, r(kp)),  r = (B - I(kp))/u,
    over the exit types with r >= |kp - mubar|.  Scan + local refinement.  Uses I itself.
    Returns (value, kp*, list of local minima)."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    mb = float(lam @ mu)
    land = model.v if use_v else model.I
    u = model.u

    def m_of(kp, x0=None):
        r = (B - float(land(kp))) / u
        if r < abs(kp - mb) - 1e-15:
            return np.inf, None
        r = max(r, abs(kp - mb))
        Dm, z = dual_fixed_type(lam, mu, kp, r, x0)
        return float(h(kp)) - Dm, z

    ks = np.linspace(1e-6, 1 - 1e-6, nk)
    vals = np.full(nk, np.inf)
    z = None
    for i, kp in enumerate(ks):
        vals[i], z = m_of(kp, z)
        if z is None:
            z = None
    # local minima of the scan
    fin = np.isfinite(vals)
    loc = []
    for i in range(nk):
        if not fin[i]:
            continue
        l = vals[i - 1] if i > 0 else np.inf
        rr = vals[i + 1] if i < nk - 1 else np.inf
        if vals[i] <= l and vals[i] <= rr:
            loc.append(i)
    loc = sorted(loc, key=lambda i: vals[i])[:6]
    best = np.inf
    kbest = None
    out = []
    for i in loc:
        a = ks[max(i - 1, 0)]
        b = ks[min(i + 1, nk - 1)]
        f = lambda kp: m_of(kp)[0]
        vv, kk = vals[i], ks[i]
        for _ in range(refine):
            gg = np.linspace(a, b, 21)
            fv = np.array([f(x) for x in gg])
            j = int(np.argmin(fv))
            if fv[j] < vv:
                vv, kk = fv[j], gg[j]
            a = gg[max(j - 1, 0)]
            b = gg[min(j + 1, 20)]
        out.append((float(kk), float(vv)))
        if vv < best:
            best, kbest = vv, kk
    return float(best), kbest, out


# ------------------------------------------------------------------ S3: primal, generic

def inner_primal(model, lam, mu, B, nstart=60, seed=0, use_v=False):
    """S3.  minimise MI(nu) over all nu in [0,1]^k with u*dist(nu,mu) + I(nubar) <= B by
    multi-start SLSQP in split variables nu = mu + p - q (p, q >= 0).  Returns the least
    feasible value found (an upper bound of V) and its nu."""
    lam = np.asarray(lam, float)
    mu = np.asarray(mu, float)
    k = len(mu)
    u = model.u
    land = model.v if use_v else model.I
    rng = np.random.default_rng(seed)

    def nu_of(z):
        return np.clip(mu + z[:k] - z[k:], 0.0, 1.0)

    def obj(z):
        nu = nu_of(z)
        return float(h(lam @ nu) - lam @ h(nu))

    def con(z):
        nu = mu + z[:k] - z[k:]
        return B - u * float(lam @ (z[:k] + z[k:])) - float(land(np.clip(lam @ nu, 0, 1)))

    bounds = [(0.0, 1.0 - m) for m in mu] + [(0.0, m) for m in mu]
    best = MI(lam, mu) if con(np.zeros(2 * k)) >= 0 else np.inf
    bestnu = mu.copy()
    for s in range(nstart):
        # random target profile, pulled back along the segment until feasible
        tgt = rng.random(k)
        if s % 3 == 0:
            tgt = np.full(k, rng.random())
        z = np.concatenate((np.maximum(tgt - mu, 0), np.maximum(mu - tgt, 0)))
        t = 1.0
        for _ in range(60):
            if con(t * z) >= 0:
                break
            t *= 0.8
        z0 = t * z
        try:
            res = optimize.minimize(obj, z0, method='SLSQP', bounds=bounds,
                                    constraints=[{'type': 'ineq', 'fun': con}],
                                    options={'maxiter': 400, 'ftol': 1e-14})
        except Exception:
            continue
        zz = np.array([min(max(x, lo), hi) for x, (lo, hi) in zip(res.x, bounds)])
        c = con(zz)
        if c < 0:
            # pull back towards the feasible start
            t = 1.0
            for _ in range(80):
                zt = z0 + t * (zz - z0)
                if con(zt) >= 0:
                    zz = zt
                    break
                t *= 0.9
            else:
                continue
        val = obj(zz)
        if val < best:
            best, bestnu = val, nu_of(zz)
    return float(best), bestnu


# ------------------------------------------------------------------ closed forms, uniform cube

def Lam1(u):
    return np.log(2.0 / (1.0 + np.exp(-u)))


def p_u(u):
    return np.exp(-u) / (1.0 + np.exp(-u))


def R_unif(e, u):
    """KL((Lam1+e)/u || 1/2) for p_u <= rho <= 1/2, 0 beyond, -e below"""
    rho = (Lam1(u) + e) / u
    if rho >= 0.5:
        return 0.0
    if rho <= p_u(u):
        return -e
    return float(kl(rho, 0.5))
