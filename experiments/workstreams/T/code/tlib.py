"""Workstream T -- single-letter (type-level) formulas for a known part that is a function of the type,
f(x) = n*phi(|x|/n), on the cube with the class L_u of u-Lipschitz residuals.

Own code (numpy/scipy only); nothing imported from the repository.

Notation (report, section 2).  A *block profile* is a finite list of blocks j with fractions lam_j (sum 1) and
block types mu_j = P(X=1 | U=j).  Binary centre s of type m, profile z=(a,b), a=P(X=0|S=1), b=P(X=1|S=0):
blocks (S=1: lam=m, mu=1-a), (S=0: lam=1-m, mu=b).
    kappa(mu)   = sum lam_j mu_j                    (type of the point)
    MI(mu)      = h(kappa) - sum lam_j h(mu_j)      (I(U;X): density exponent of the profile class in its type class)
    dist(nu,mu) = sum lam_j |nu_j - mu_j|           (Hamming distance per site between the classes)
    alpha(mu)   = MI(mu) + I(kappa(mu))             (pi-measure exponent of the class)
Rate function of the type: I = phi - h - min(phi - h);  v = largest u-Lipschitz minorant of I.
An *exit landscape* lam(.) is a u-Lipschitz minorant of I (v for the flat-histogram instance H; c_chi - chi for the
symmetric instance chi).

Single-letter value (Theorem T3 of the report):
    V(mu, B; lam) = min{ MI(nu) : u*dist(nu,mu) + lam(kappa(nu)) <= B },
    R_lam(e)      = sup_mu V(mu, e + alpha(mu); lam).
The minimiser nu is a *clipping* of mu: nu_j = min(max(mu_j, c_lo), c_hi)  (KKT; report Lemma T4), so the inner
problem is two-dimensional for every number of blocks.
"""
import math
import numpy as np

LOG2 = math.log(2.0)


def hb(x):
    """binary entropy (nats), vectorised, exact zeros at 0 and 1"""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    m = (x > 0.0) & (x < 1.0)
    xm = x[m]
    out[m] = -(xm * np.log(xm) + (1.0 - xm) * np.log1p(-xm))
    return out


def hbf(x):
    """binary entropy for arrays, no masks (arguments clipped to [1e-300, 1-1e-16]); exact enough at 0 and 1"""
    x = np.clip(x, 1e-300, 1.0 - 1e-16)
    return -(x * np.log(x) + (1.0 - x) * np.log1p(-x))


def hb1(x):
    """scalar binary entropy"""
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -(x * math.log(x) + (1.0 - x) * math.log1p(-x))


def kl1(x, p):
    """scalar binary relative entropy KL(x||p)"""
    r = 0.0
    if x > 0:
        r += x * math.log(x / p)
    if x < 1:
        r += (1 - x) * math.log((1 - x) / (1 - p))
    return r


# ----------------------------------------------------------------------------------------------------------------------
# known parts
# ----------------------------------------------------------------------------------------------------------------------
def phi_cw(bJ, bB):
    """Curie-Weiss: phi(kappa) = -(bJ/2) mu^2 - bB mu, mu = 2 kappa - 1"""
    return lambda k: -(bJ / 2.0) * (2.0 * np.asarray(k, dtype=float) - 1.0) ** 2 - bB * (2.0 * np.asarray(k, dtype=float) - 1.0)


def phi_field(p):
    """field: phi(kappa) = theta*kappa, theta = ln((1-p)/p); then I = KL(.||p)"""
    th = math.log((1.0 - p) / p)
    return lambda k: th * np.asarray(k, dtype=float)


class Known:
    """rate function I of the type and its largest u-Lipschitz minorant v, for a known part n*phi(|x|/n)."""

    def __init__(self, phi, u, N=400001):
        self.phi = phi
        self.u = float(u)
        self.N = N
        k = np.linspace(0.0, 1.0, N)
        raw = phi(k) - hb(k)
        # global minimum of phi - h, polished by golden section around every local grid minimum
        loc = np.nonzero((raw[1:-1] <= raw[:-2]) & (raw[1:-1] <= raw[2:]))[0] + 1
        cands = [float(raw[0]), float(raw[-1])]
        self.minima = []
        from scipy.optimize import minimize_scalar
        f = lambda t: float(phi(np.array([t]))[0] - hb1(t))
        for i in loc:
            r = minimize_scalar(f, bounds=(k[i - 1], k[i + 1]), method="bounded", options={"xatol": 1e-15})
            cands.append(float(r.fun))
            self.minima.append((float(r.x), float(r.fun)))
        self.c0 = min(cands)
        self.minima = [(x, fv - self.c0) for (x, fv) in self.minima]
        self.grid = k
        self.Ig = raw - self.c0
        self.PL = np.minimum.accumulate(self.Ig - self.u * k)                  # min_{k'<=k} [I(k') - u k']
        self.PR = np.minimum.accumulate((self.Ig + self.u * k)[::-1])[::-1]    # min_{k'>=k} [I(k') + u k']

    def I(self, kap):
        kap = np.asarray(kap, dtype=float)
        return self.phi(kap) - hb(kap) - self.c0

    def v(self, kap):
        """largest u-Lipschitz minorant of I: v(k) = min_{k'} [I(k') + u|k-k'|]  (error O(h^2), h = 1/(N-1));
        I is interpolated linearly on the grid (error O(h^2))"""
        kap = np.clip(np.asarray(kap, dtype=float), 0.0, 1.0)
        x = kap * (self.N - 1)
        lo = x.astype(np.int64)
        hi = np.minimum(lo + 1, self.N - 1)
        fr = x - lo
        Il = self.Ig[lo] * (1.0 - fr) + self.Ig[hi] * fr
        return np.minimum(Il, np.minimum(self.PL[lo] + self.u * kap, self.PR[hi] - self.u * kap))

    def v_exact(self, kap):
        """the same with I evaluated analytically"""
        kap = np.clip(np.asarray(kap, dtype=float), 0.0, 1.0)
        x = kap * (self.N - 1)
        lo = np.floor(x).astype(np.int64)
        hi = np.minimum(lo + 1, self.N - 1)
        return np.minimum(self.I(kap), np.minimum(self.PL[lo] + self.u * kap, self.PR[hi] - self.u * kap))

    def contact_pieces(self, tol=1e-12):
        """connected pieces of the contact set {v = I} on the grid"""
        vg = np.minimum(self.Ig, np.minimum(self.PL + self.u * self.grid, self.PR - self.u * self.grid))
        flat = (self.Ig - vg) < tol
        idx = np.nonzero(flat)[0]
        if len(idx) == 0:
            return []
        cuts = np.nonzero(np.diff(idx) > 1)[0] + 1
        return [(float(self.grid[q[0]]), float(self.grid[q[-1]])) for q in np.split(idx, cuts)]

    def lam_additive(self, gamma):
        """exit landscape of the additive instance gamma*|x|: lam(k) = -gamma k - c_gamma, c_gamma = max_k[-gamma k - I(k)]"""
        c = float(np.max(-gamma * self.grid - self.Ig))
        return lambda kap: -gamma * np.asarray(kap, dtype=float) - c

    def lam_zero(self):
        return lambda kap: np.zeros_like(np.asarray(kap, dtype=float))


# ----------------------------------------------------------------------------------------------------------------------
# block profiles
# ----------------------------------------------------------------------------------------------------------------------
def bin_blocks(m, a, b):
    """binary centre -> (lams, mus)"""
    return np.array([m, 1.0 - m]), np.array([1.0 - a, b])


def MI_blocks(lams, mus):
    """I(U;X) for blocks; mus may have a leading batch dimension (..., k)"""
    mus = np.asarray(mus, dtype=float)
    kap = np.sum(lams * mus, axis=-1)
    return np.maximum(hb(kap) - np.sum(lams * hb(mus), axis=-1), 0.0)


def MI_bin(m, a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    kap = m * (1.0 - a) + (1.0 - m) * b
    return np.maximum(hb(kap) - m * hb(a) - (1.0 - m) * hb(b), 0.0)


def alpha_blocks(K, lams, mus):
    kap = float(np.sum(lams * mus))
    return float(MI_blocks(lams, mus)) + float(K.I(kap))


# ----------------------------------------------------------------------------------------------------------------------
# the inner problem  V(mu, B; lam) = min{ MI(nu) : u dist(nu,mu) + lam(kappa(nu)) <= B }   (clipping family)
# ----------------------------------------------------------------------------------------------------------------------
def _clip_eval(K, lams, mus, clo, chi, lam):
    """for arrays clo, chi (same shape): clipped profiles, constraint value C and MI"""
    nu = np.minimum(np.maximum(mus[None, :], clo[:, None]), chi[:, None])
    dist = np.sum(lams * np.abs(nu - mus[None, :]), axis=1)
    kap = np.sum(lams * nu, axis=1)
    C = K.u * dist + lam(kap)
    return nu, C, kap


def V_clip(K, lams, mus, B, lam, ng=161, zoom=5, full=False, nbis=40):
    """V(mu,B;lam) by a scan over c_lo; for each c_lo the least feasible c_hi (C is nonincreasing in c_hi) by bisection.
    lam must be u-Lipschitz (then C is nondecreasing in c_lo and nonincreasing in c_hi, and MI(clip) is nonincreasing
    in c_lo and nondecreasing in c_hi, so the minimum is on the boundary curve).  Scan of ng points, then `zoom`
    refinements (21 points each, factor 10) around the three best local minima of the scan (batched).
    Returns V (and (c_lo,c_hi))."""
    lams = np.asarray(lams, dtype=float)
    mus = np.asarray(mus, dtype=float)
    mu_max = float(mus.max())
    u = K.u
    hmu = float(np.sum(lams * hbf(mus)))

    def curve(clo):
        nu1 = np.maximum(mus[None, :], clo[:, None])
        C1 = u * ((nu1 - mus[None, :]) @ lams) + lam(nu1 @ lams)                                   # c_hi = 1
        feas = C1 <= B + 1e-15
        C0 = u * (np.abs(clo[:, None] - mus[None, :]) @ lams) + lam(clo)                           # c_hi = c_lo: merged
        merged = C0 <= B + 1e-15
        lo = clo.copy()
        hi = np.ones_like(clo)
        for _ in range(nbis):
            mid = 0.5 * (lo + hi)
            nu = np.minimum(nu1, mid[:, None])
            Cm = u * (np.abs(nu - mus[None, :]) @ lams) + lam(nu @ lams)
            ok = Cm <= B
            hi = np.where(ok, mid, hi)
            lo = np.where(ok, lo, mid)
        nu = np.minimum(nu1, hi[:, None])
        val = np.maximum(hbf(nu @ lams) - hbf(nu) @ lams, 0.0)
        val = np.where(merged, 0.0, val)
        val = np.where(feas, val, np.inf)
        return val, hi

    clo = np.linspace(0.0, mu_max, ng)
    val, chi = curve(clo)
    if not np.isfinite(val).any():
        return (np.inf, None) if full else np.inf
    fin = np.where(np.isfinite(val), val, 1e300)
    left = np.r_[1e300, fin[:-1]]
    right = np.r_[fin[1:], 1e300]
    # basins: strict decrease from the left (a plateau counts once), no increase to the right; the first feasible
    # point and the last feasible point (boundary of the feasible range: pure lower clipping) are always candidates
    locs = np.nonzero((fin < left) & (fin <= right) & (fin < 1e299))[0]
    locs = locs[np.argsort(fin[locs], kind="stable")][:4]
    feas_idx = np.nonzero(fin < 1e299)[0]
    locs = np.unique(np.r_[locs, feas_idx[0], feas_idx[-1]])
    nl = len(locs)
    a_ = clo[np.maximum(locs - 1, 0)]
    b_ = clo[np.minimum(locs + 1, ng - 1)]
    bv = val[locs].astype(float).copy()
    bc = clo[locs].copy()
    bh = chi[locs].copy()
    w = np.linspace(0.0, 1.0, 21)
    for _ in range(zoom):
        g = a_[:, None] + (b_ - a_)[:, None] * w[None, :]               # (nl, 21)
        vv, hh = curve(g.ravel())
        vv = vv.reshape(nl, 21)
        hh = hh.reshape(nl, 21)
        j = np.argmin(vv, axis=1)
        r = np.arange(nl)
        better = vv[r, j] <= bv
        bv = np.where(better, vv[r, j], bv)
        bc = np.where(better, g[r, j], bc)
        bh = np.where(better, hh[r, j], bh)
        a_ = g[r, np.maximum(j - 1, 0)]
        b_ = g[r, np.minimum(j + 1, 20)]
    i = int(np.argmin(bv))
    if full:
        return float(bv[i]), (float(bc[i]), float(bh[i]))
    return float(bv[i])


def V_bin(K, m, a, b, B, lam, ng=161, zoom=5, full=False):
    return V_clip(K, *bin_blocks(m, a, b), B, lam, ng=ng, zoom=zoom, full=full)


# ----------------------------------------------------------------------------------------------------------------------
# the hinted exponent R_lam(e) = sup_mu V(mu, e + alpha(mu); lam)
# ----------------------------------------------------------------------------------------------------------------------
def obj_blocks(K, e, lam, lams, mus, ng=161, zoom=5):
    """V(mu, e + alpha(mu); lam) for a block profile (0 if the class is not admissible)"""
    lams = np.asarray(lams, dtype=float)
    mus = np.asarray(mus, dtype=float)
    kap = float(np.sum(lams * mus))
    B = e + float(MI_blocks(lams, mus)) + float(K.I(kap))
    if B < float(lam(np.array([kap]))[0]) - 1e-15:
        return 0.0
    return V_clip(K, lams, mus, B, lam, ng=ng, zoom=zoom)


def obj_bin(K, e, lam, x, ng=161, zoom=5):
    """objective of the outer problem for a binary centre; x = (m, a, b)"""
    m, a, b = x
    if not (0.0 < m < 1.0 and 0.0 <= a < 1.0 and 0.0 <= b < 1.0 and a + b < 1.0):
        return 0.0
    return obj_blocks(K, e, lam, *bin_blocks(m, a, b), ng=ng, zoom=zoom)


def R_bin(K, e, lam, starts=None, ng=161, verbose=False, seed=0, nrand=4, ms=None, polish=True):
    """sup over binary centres (m,a,b): candidate starts = Gibbs shells of the cones around point centres of types ms,
    the uniform-cube shell, user starts and random points; the best `nrand`+2 candidates are polished by Nelder-Mead.
    Returns (R, argmax)."""
    from scipy.optimize import minimize
    rng = np.random.default_rng(seed)
    cands = list(starts) if starts is not None else []
    if ms is None:
        ms = np.linspace(0.1, 0.9, 9)
    for m in ms:
        _, (n0, n1) = Lam_m(K, m, full=True)          # Gibbs shell of the cone: mu = (1-a, b)
        cands.append((float(m), 1.0 - n0, n1))
    pu = 1.0 / (1.0 + math.exp(K.u))
    cands.append((0.5, pu, pu))
    # symmetric shells (m, x, x) in the type class m: for small u the optimum can sit on a narrow range of x where the
    # value at the uniform-cube shell x = p_u is still zero (found the hard way: t10, u = 0.3)
    for m in (0.5, 0.4, 0.6):
        for x in np.linspace(pu, 0.495, 10)[1:]:
            cands.append((m, float(x), float(x)))
    for _ in range(3 * nrand):
        cands.append((rng.uniform(0.15, 0.85), rng.uniform(0.01, 0.45), rng.uniform(0.01, 0.45)))
    vals = [obj_bin(K, e, lam, c, ng=ng) for c in cands]
    order = np.argsort(vals)[::-1]
    best = (float(vals[order[0]]), tuple(cands[order[0]]))
    if not polish:
        return best
    f = lambda x: -obj_bin(K, e, lam, x, ng=ng)
    done = 0
    for i in order:
        if done >= nrand + 2:
            break
        if vals[i] <= 0.0 and done > 0:
            break
        s = cands[i]
        r = minimize(f, np.array(s, dtype=float), method="Nelder-Mead",
                     options={"xatol": 1e-8, "fatol": 1e-13, "maxiter": 700, "initial_simplex": _simplex(s)})
        r2 = minimize(f, r.x, method="Nelder-Mead",
                      options={"xatol": 1e-9, "fatol": 1e-14, "maxiter": 400, "initial_simplex": _simplex(r.x, 0.003)})
        if -r2.fun > best[0]:
            best = (-float(r2.fun), tuple(float(t) for t in r2.x))
        if verbose:
            print("    start", np.round(s, 4), f"({vals[i]:.6f}) ->", -r2.fun, np.round(r2.x, 6), flush=True)
        done += 1
    return best


def _simplex(s, d=0.02):
    s = np.array(s, dtype=float)
    pts = [s]
    for i in range(len(s)):
        t = s.copy()
        t[i] += d if s[i] < 0.5 else -d
        pts.append(t)
    return np.array(pts)


# ----------------------------------------------------------------------------------------------------------------------
# cone formulas of the brief (O2):  Lam_m = min_z [MI + I(kappa_z) + u rho],  R_cone(e) = max_m min{MI : u rho + lam - Lam_m <= e}
# ----------------------------------------------------------------------------------------------------------------------
def cone_free_energy(K, lams, mu0, G=241, zoom=4, full=False):
    """V(mu0) = min_nu [ MI(nu) + I(kappa(nu)) + u dist(nu, mu0) ]  for two blocks (grid + zoom); mu0 = centre shell."""
    lams = np.asarray(lams, dtype=float)
    mu0 = np.asarray(mu0, dtype=float)
    assert len(lams) == 2
    lo = np.array([0.0, 0.0])
    hi = np.array([1.0, 1.0])
    best, arg = np.inf, None
    for it in range(zoom + 1):
        g0 = np.linspace(lo[0], hi[0], G)
        g1 = np.linspace(lo[1], hi[1], G)
        N0, N1 = np.meshgrid(g0, g1, indexing="ij")
        kap = lams[0] * N0 + lams[1] * N1
        val = np.maximum(hb(kap) - lams[0] * hb(N0) - lams[1] * hb(N1), 0.0) + K.I(kap) \
            + K.u * (lams[0] * np.abs(N0 - mu0[0]) + lams[1] * np.abs(N1 - mu0[1]))
        i, j = np.unravel_index(np.argmin(val), val.shape)
        if val[i, j] < best:
            best, arg = float(val[i, j]), (float(g0[i]), float(g1[j]))
        w0 = (hi[0] - lo[0]) / (G - 1) * 3
        w1 = (hi[1] - lo[1]) / (G - 1) * 3
        lo = np.array([max(arg[0] - w0, 0.0), max(arg[1] - w1, 0.0)])
        hi = np.array([min(arg[0] + w0, 1.0), min(arg[1] + w1, 1.0)])
    if full:
        return best, arg
    return best


def Lam_m(K, m, full=False):
    """free energy of the cone around a centre of type m (centre shell = the centre itself: mu0 = (1, 0))"""
    return cone_free_energy(K, np.array([m, 1.0 - m]), np.array([1.0, 0.0]), full=full)


def R_cone(K, e, lam, ms=None, full=False):
    """max_m min{ MI(z) : u rho(z) + lam(kappa_z) - Lam_m <= e }   (the brief's formula; dips centred at a point)"""
    from scipy.optimize import minimize_scalar
    f = lambda m: -V_bin(K, m, 0.0, 0.0, e + Lam_m(K, m), lam) if 0.0 < m < 1.0 else 0.0
    if ms is None:
        ms = np.linspace(0.04, 0.96, 24)
    vals = np.array([-f(m) for m in ms])
    i = int(np.argmax(vals))
    r = minimize_scalar(f, bounds=(ms[max(i - 1, 0)], ms[min(i + 1, len(ms) - 1)]), method="bounded",
                        options={"xatol": 1e-10})
    val = max(-float(r.fun), float(vals[i]))
    mm = float(r.x) if -r.fun >= vals[i] else float(ms[i])
    return (val, mm) if full else val


# ----------------------------------------------------------------------------------------------------------------------
# non-adaptive side
#   n_mu(X)          = min{ MI(nu) : MI(nu) + u dist(nu,mu) + lam(kappa(nu)) - alpha(mu) <= X }       (lam = v)
#   theta_shell(X;mu0) = min{ MI(nu) : MI(nu) + I(kappa(nu)) + u dist(nu,mu0) - V(mu0) <= X }         (truncated shell-cone)
# both over two blocks, on the full square of profiles nu (grid + zoom)
# ----------------------------------------------------------------------------------------------------------------------
def _min_MI_under(K, lams, cfun, X, G=601, zoom=5, full=False, ncand=4):
    """min{ MI(nu) : cfun(...) <= X } over nu in [0,1]^2 (two blocks): a global grid, then zooms (factor ~ G/8 each)
    around the `ncand` best well-separated feasible grid points."""
    lams = np.asarray(lams, dtype=float)

    def scan(lo, hi, g):
        g0 = np.linspace(lo[0], hi[0], g)
        g1 = np.linspace(lo[1], hi[1], g)
        N0, N1 = np.meshgrid(g0, g1, indexing="ij")
        kap = lams[0] * N0 + lams[1] * N1
        mi = np.maximum(hbf(kap) - lams[0] * hbf(N0) - lams[1] * hbf(N1), 0.0)
        ok = cfun(N0, N1, kap, mi) <= X
        return g0, g1, np.where(ok, mi, np.inf)

    g0, g1, mi2 = scan(np.array([0.0, 0.0]), np.array([1.0, 1.0]), G)
    if not np.isfinite(mi2).any():
        return (np.inf, None) if full else np.inf
    flat = np.argsort(mi2, axis=None)
    cands = []
    for idx in flat[:4000]:
        i, j = np.unravel_index(idx, mi2.shape)
        if not np.isfinite(mi2[i, j]):
            break
        if all(abs(i - a) + abs(j - b) > 12 for (a, b) in cands):
            cands.append((i, j))
        if len(cands) >= ncand:
            break
    best, arg = np.inf, None
    for (i, j) in cands:
        c = np.array([g0[i], g1[j]])
        w = 4.0 / (G - 1)
        v_, a_ = float(mi2[i, j]), (float(c[0]), float(c[1]))
        for it in range(zoom):
            lo = np.maximum(c - w, 0.0)
            hi = np.minimum(c + w, 1.0)
            h0, h1, m3 = scan(lo, hi, 81)
            if not np.isfinite(m3).any():
                break
            ii, jj = np.unravel_index(np.argmin(m3), m3.shape)
            if m3[ii, jj] <= v_:
                v_, a_ = float(m3[ii, jj]), (float(h0[ii]), float(h1[jj]))
            c = np.array([h0[ii], h1[jj]])
            w = w / 10.0
        if v_ < best:
            best, arg = v_, a_
    return (best, arg) if full else best


def n_mu_grid(K, lams, mus, X, lam, G=601, zoom=5, full=False):
    """the same as n_mu by a direct two-dimensional search (two blocks only); used as a cross-check"""
    lams = np.asarray(lams, dtype=float)
    mus = np.asarray(mus, dtype=float)
    al = alpha_blocks(K, lams, mus)
    cfun = lambda N0, N1, kap, mi: mi + K.u * (lams[0] * np.abs(N0 - mus[0]) + lams[1] * np.abs(N1 - mus[1])) + lam(kap) - al
    return _min_MI_under(K, lams, cfun, X, G=G, zoom=zoom, full=full)


def n_mu(K, lams, mus, X, lam, ne=24, full=False, ng=161, tol=1e-12):
    """n_mu(X) = min{ MI(nu) : MI(nu) + u dist(nu,mu) + lam(kappa(nu)) - alpha(mu) <= X }
               = min{ r_mu(e) : e + r_mu(e) <= X },   r_mu(e) = V(mu, e + alpha(mu); lam)
    (report, Lemma T8), computed through the robust clipping solver: the largest e with e + r_mu(e) <= X is located by
    a scan from above (S_mu(e) = e + r_mu(e) need not be monotone for a profile mu that is not optimal) and bisection.
    Returns n_mu(X) = r_mu(e_max)  (and e_max)."""
    lams = np.asarray(lams, dtype=float)
    mus = np.asarray(mus, dtype=float)
    al = alpha_blocks(K, lams, mus)
    kap = float(np.sum(lams * mus))
    e_min = float(lam(np.array([kap]))[0]) - al          # below it the class itself is not inside the dip
    r = lambda e: V_clip(K, lams, mus, e + al, lam, ng=ng)
    g = lambda e: e + r(e) - X
    if r(X) <= 0.0:
        return (0.0, X) if full else 0.0
    es = np.linspace(X, e_min, ne)
    hi = es[0]
    lo = None
    for e in es[1:]:
        if g(e) <= 0.0:
            lo = e
            break
        hi = e
    if lo is None:
        lo = e_min
    for _ in range(46):
        mid = 0.5 * (lo + hi)
        if g(mid) <= 0.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    val = r(lo)
    return (val, lo) if full else val


def theta_shell(K, lams, mu0, X, G=601, zoom=5, full=False):
    lams = np.asarray(lams, dtype=float)
    mu0 = np.asarray(mu0, dtype=float)
    V0 = cone_free_energy(K, lams, mu0)
    cfun = lambda N0, N1, kap, mi: mi + K.I(kap) + K.u * (lams[0] * np.abs(N0 - mu0[0]) + lams[1] * np.abs(N1 - mu0[1])) - V0
    return _min_MI_under(K, lams, cfun, X, G=G, zoom=zoom, full=full)


# ----------------------------------------------------------------------------------------------------------------------
# field control: closed forms of theory report, Theorem 11.59(b)
# ----------------------------------------------------------------------------------------------------------------------
def F_field(theta, u, gamma, t):
    """cosh form of the game function of the additive instance gamma|x| in the field theta"""
    if t <= 0:
        return 0.0
    C = lambda x: 2.0 * math.cosh(x / 2.0)
    lam = theta + gamma
    lp, lm = theta + u, theta - u
    num = math.sinh(t * (lp - lam) / 2.0) * C(lm) ** t + math.sinh(t * (lam - lm) / 2.0) * C(lp) ** t
    return math.log(num / math.sinh(t * u)) - t * math.log(C(lam))


def Fstar_field(theta, u, t):
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda g: -F_field(theta, u, g, t), bounds=(-u, u), method="bounded", options={"xatol": 1e-13})
    return max(-r.fun, F_field(theta, u, 0.0, t))


def Rmax_field(theta, u, e, gamma=None):
    """R^max(e) = max_{0<=t<=1} [F*(t) - t e]  (or R_gamma if gamma is given)"""
    from scipy.optimize import minimize_scalar
    F = (lambda t: Fstar_field(theta, u, t)) if gamma is None else (lambda t: F_field(theta, u, gamma, t))
    ts = np.linspace(1e-6, 1.0, 400)
    vals = np.array([F(t) - t * e for t in ts])
    i = int(np.argmax(vals))
    r = minimize_scalar(lambda t: -(F(t) - t * e), bounds=(ts[max(i - 1, 0)], ts[min(i + 1, 399)]), method="bounded",
                        options={"xatol": 1e-13})
    return max(-r.fun, float(vals[i]), 0.0)


def thetana_field(theta, u, x):
    """theta_na(x) = max_{0<=tau<1} (F*(tau) - tau x)/(1 - tau)"""
    from scipy.optimize import minimize_scalar
    f = lambda t: (Fstar_field(theta, u, t) - t * x) / (1.0 - t)
    ts = np.linspace(0.0, 0.9999, 600)
    vals = np.array([f(t) for t in ts])
    i = int(np.argmax(vals))
    r = minimize_scalar(lambda t: -f(t), bounds=(ts[max(i - 1, 0)], ts[min(i + 1, 599)]), method="bounded",
                        options={"xatol": 1e-13})
    return max(-r.fun, float(vals[i]))


def E_field(theta, u):
    """class threshold E = sup_{t>0} F*(t)/t = lim_{t->0}: max over lam in the window of the chord gap of ln C"""
    lC = lambda x: math.log(2.0 * math.cosh(x / 2.0))
    lp, lm = theta + u, theta - u
    from scipy.optimize import minimize_scalar
    g = lambda lam: ((lp - lam) * lC(lm) + (lam - lm) * lC(lp)) / (2 * u) - lC(lam)
    r = minimize_scalar(lambda lam: -g(lam), bounds=(lm, lp), method="bounded", options={"xatol": 1e-13})
    return -r.fun


# ----------------------------------------------------------------------------------------------------------------------
# beyond binary centres: symmetric block profiles (for a symmetric rate function, B = 0)
#   S2: {1-x, x};  S3: {1-x, 1/2, x} (a 'free' block of weight lf);  S4: {1-x, 1/2+d, 1/2-d, x};
#   S5: {1-x, 1-y, 1/2, y, x};  S6: {1-x, 1-y, 1-z, z, y, x}
# ----------------------------------------------------------------------------------------------------------------------
def sym_profile(kind, p):
    if kind == "S2":
        x, = p
        return np.array([0.5, 0.5]), np.array([1 - x, x])
    if kind == "S3":
        lf, x = p
        l = (1 - lf) / 2
        return np.array([l, lf, l]), np.array([1 - x, 0.5, x])
    if kind == "S4":
        lf, x, d = p
        l = (1 - lf) / 2
        return np.array([l, lf / 2, lf / 2, l]), np.array([1 - x, 0.5 + d, 0.5 - d, x])
    if kind == "S5":
        l2, lf, x, y = p
        l1 = (1 - lf - 2 * l2) / 2
        return np.array([l1, l2, lf, l2, l1]), np.array([1 - x, 1 - y, 0.5, y, x])
    if kind == "S6":
        l2, l3, x, y, z = p
        l1 = 0.5 - l2 - l3
        return np.array([l1, l2, l3, l3, l2, l1]), np.array([1 - x, 1 - y, 1 - z, z, y, x])
    raise ValueError(kind)


def _nm2(f, x0, step=0.02, it=1500):
    from scipy.optimize import minimize
    x0 = np.array(x0, dtype=float)
    sim = [x0] + [x0 + step * np.eye(len(x0))[i] * (1 if x0[i] < 0.5 else -1) for i in range(len(x0))]
    r = minimize(f, x0, method="Nelder-Mead", options={"xatol": 1e-8, "fatol": 1e-13, "maxiter": it, "initial_simplex": np.array(sim)})
    sim = [r.x] + [r.x + 0.2 * step * np.eye(len(x0))[i] for i in range(len(x0))]
    r = minimize(f, r.x, method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-14, "maxiter": it, "initial_simplex": np.array(sim)})
    return r.x, -r.fun


def R_sym(K, e, lam, kinds=("S2", "S3", "S4", "S5"), fine=True):
    """suprema over the symmetric families (Nelder-Mead; S3 from three dilutions); returns {kind: (R, lams, mus)}"""
    def f(kind):
        def g(p):
            lams, mus = sym_profile(kind, p)
            if lams.min() <= 1e-5 or mus.min() < 0 or mus.max() > 1:
                return 0.0
            return -obj_blocks(K, e, lam, lams, mus)
        return g
    out = {}
    pu = 1.0 / (1.0 + math.exp(K.u))
    best2 = (-1.0, None)
    for x0 in (pu + 0.03, pu + 0.1, 0.4):
        p, v = _nm2(f("S2"), [x0])
        if v > best2[0]:
            best2 = (v, p)
    p2 = best2[1]
    ps = {"S2": p2}
    if "S3" in kinds or "S4" in kinds or "S5" in kinds or "S6" in kinds:
        best3 = (-1.0, None)
        for lf0 in (0.05, 0.15, 0.3):
            p, v = _nm2(f("S3"), [lf0, p2[0] - 0.01])
            if v > best3[0]:
                best3 = (v, p)
        ps["S3"] = best3[1]
    if "S4" in kinds or "S6" in kinds:
        ps["S4"], _ = _nm2(f("S4"), [ps["S3"][0], ps["S3"][1], 0.06])
    if "S5" in kinds:
        ps["S5"], _ = _nm2(f("S5"), [0.1, max(ps["S3"][0] - 0.05, 0.02), ps["S3"][1] - 0.02, ps["S3"][1] + 0.08])
    if "S6" in kinds:
        lf4, x4, d4 = ps["S4"]
        best6 = (-1.0, None)
        for (l2_0, y0) in ((0.08, x4 + 0.06), (0.15, 0.5 * (x4 + 0.5 - d4))):
            p, v = _nm2(f("S6"), [l2_0, max(lf4 / 2, 0.03), x4 - 0.01, y0, 0.5 - max(d4, 0.03)])
            if v > best6[0]:
                best6 = (v, p)
        ps["S6"] = best6[1]
    for kind in kinds:
        lams, mus = sym_profile(kind, ps[kind])
        val = obj_blocks(K, e, lam, lams, mus, ng=2001, zoom=6) if fine else -f(kind)(ps[kind])
        out[kind] = (val, lams, mus)
    return out
