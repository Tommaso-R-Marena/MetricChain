"""
r5lib.py -- independent implementation for review SCI-REV-0005 (workstream R5).

Written from the STATEMENTS of theory report section 11.26 (Theorems 11.98, 11.99) only,
before reading the authors' code (wv_lib.py, experiments/workstreams/W/code).  numpy/scipy only.

Objects
-------
site = (pi, d):  pi a probability vector with full support on q letters,
                 d a q x q matrix, d >= 0, zero diagonal, triangle inequality, possibly asymmetric.
L = {g : g[a] - g[b] <= d[a,b]}        (Lipschitz polytope; first argument = letter where g may be larger)
V = vertices of L modulo constants     (normalised g[0] = 0)
pi_phi  = pi * exp(-phi) / Z           (Gibbs law of phi)
game    K[a,phi] = (pi_phi[a]/pi_gamma[a])**t ;  val = min_M max_a (K M)[a] = max_Q min_phi (Q K)[phi]
F(gamma,t) = -ln val ;  Fstar(t) = max_{gamma in L} F(gamma,t)

Claim under review (Theorem 11.99):
   Fstar(t) = max_M  -t ln sum_a ( sum_phi M[phi] pi_phi[a]^t )^(1/t)          (primal, 'Sibson')
            = min_Q max_phi (1-t) D_t(pi_phi || Q)                             (dual,   'radius')
"""
import itertools
import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar, brentq
from scipy.special import logsumexp

# ----------------------------------------------------------------------------------------------
# geometry of the site
# ----------------------------------------------------------------------------------------------

def check_envelope(d, tol=1e-12):
    d = np.asarray(d, float)
    q = d.shape[0]
    assert d.shape == (q, q) and np.all(d >= -tol) and np.allclose(np.diag(d), 0)
    for a in range(q):
        for b in range(q):
            for c in range(q):
                assert d[a, c] <= d[a, b] + d[b, c] + 1e-9, ("triangle fails", a, b, c)
    return True


def vertices(d, tol=1e-9):
    """Vertices of L/R, L = {g : g[a]-g[b] <= d[a,b]}, normalised g[0] = 0.
    Brute force: every choice of q-1 linearly independent active constraints."""
    d = np.asarray(d, float)
    q = d.shape[0]
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    verts = []
    for S in itertools.combinations(cons, q - 1):
        A = np.zeros((q - 1, q - 1))
        rhs = np.zeros(q - 1)
        for r, (a, b) in enumerate(S):
            if a > 0:
                A[r, a - 1] += 1.0
            if b > 0:
                A[r, b - 1] -= 1.0
            rhs[r] = d[a, b]
        if abs(np.linalg.det(A)) < 1e-10:
            continue
        g = np.concatenate([[0.0], np.linalg.solve(A, rhs)])
        if all(g[a] - g[b] <= d[a, b] + tol for (a, b) in cons):
            if not any(np.max(np.abs(g - v)) < 1e-8 for v in verts):
                verts.append(g)
    return np.array(verts)


def in_L(g, d, tol=1e-9):
    g = np.asarray(g, float)
    return bool(np.all(g[:, None] - g[None, :] <= np.asarray(d) + tol))


def gibbs(pi, phi):
    """pi_phi = pi exp(-phi)/Z ; phi may be a matrix of row vectors."""
    pi = np.asarray(pi, float)
    phi = np.atleast_2d(np.asarray(phi, float))
    lw = np.log(pi)[None, :] - phi
    lw -= logsumexp(lw, axis=1, keepdims=True)
    return np.exp(lw)


class Site:
    def __init__(self, pi, d, name=""):
        self.pi = np.asarray(pi, float)
        self.d = np.asarray(d, float)
        assert abs(self.pi.sum() - 1) < 1e-12 and np.all(self.pi > 0)
        check_envelope(self.d)
        self.q = len(self.pi)
        self.V = vertices(self.d)              # rows: vertices, phi[0] = 0
        self.W = gibbs(self.pi, self.V)        # rows: Gibbs laws = the 'vertex channel' W[phi, a]
        self.logW = np.log(self.W)
        self.name = name
        self._cache = {}

# ----------------------------------------------------------------------------------------------
# the game (linear programme) -- route 1, uses nothing of the Renyi form
# ----------------------------------------------------------------------------------------------

def game_value(K):
    """val = min_M max_a (K M)[a], K of shape (rows a, columns phi).  Returns (val, M)."""
    na, nphi = K.shape
    c = np.zeros(nphi + 1)
    c[-1] = 1.0
    A_ub = np.hstack([K, -np.ones((na, 1))])
    b_ub = np.zeros(na)
    A_eq = np.zeros((1, nphi + 1))
    A_eq[0, :nphi] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * nphi + [(None, None)], method="highs")
    assert res.status == 0, res.message
    return res.x[-1], res.x[:nphi]


def F_game(site, gamma, t):
    """F(gamma, t) = -ln val(K),  K[a,phi] = (pi_phi[a]/pi_gamma[a])^t."""
    pg = gibbs(site.pi, gamma)[0]
    K = np.exp(t * (site.logW - np.log(pg)[None, :])).T      # (a, phi)
    val, M = game_value(K)
    return -np.log(val), M


def Fstar_blind(site, t, n_starts=6, seed=0):
    """max over gamma in L of the LP value of the game, by a blind search
    (gamma parametrised as a convex combination of the vertices; Nelder-Mead on softmax weights)."""
    rng = np.random.default_rng(seed)
    nv = len(site.V)

    def neg(z):
        w = np.exp(z - logsumexp(z))
        gamma = w @ site.V
        return -F_game(site, gamma, t)[0]

    best = (-np.inf, None)
    for s in range(n_starts):
        z0 = rng.normal(size=nv) * (0.0 if s == 0 else 1.5)
        res = minimize(neg, z0, method="Nelder-Mead",
                       options=dict(xatol=1e-10, fatol=1e-13, maxiter=6000, maxfev=6000))
        if -res.fun > best[0]:
            w = np.exp(res.x - logsumexp(res.x))
            best = (-res.fun, w @ site.V)
    return best

# ----------------------------------------------------------------------------------------------
# the Renyi form -- route 2 (primal in M) and route 3 (dual in Q), two different programmes
# ----------------------------------------------------------------------------------------------

def G_primal(site, M, t):
    """G_t(M) = -t ln sum_a ( sum_phi M[phi] W[phi,a]^t )^(1/t)   ( = (1-t) * Sibson information of order t )."""
    ls = logsumexp(t * site.logW, b=M[:, None], axis=0)        # ln s_a
    return -t * logsumexp(ls / t)


def centre_of(site, M, t):
    """Q_M  propto  ( sum_phi M W^t )^(1/t)."""
    ls = logsumexp(t * site.logW, b=M[:, None], axis=0) / t
    return np.exp(ls - logsumexp(ls))


def renyi_div_scaled(P, Q, t):
    """(1-t) * D_t(P || Q) = -ln sum_a P^t Q^(1-t)   (natural logarithm, 0 < t < 1)."""
    return -logsumexp(t * np.log(P) + (1 - t) * np.log(Q))


def radius_at(site, Q, t):
    """max_phi (1-t) D_t(pi_phi || Q)  -- an UPPER bound for (1-t) C_t for every Q."""
    return max(renyi_div_scaled(site.W[k], Q, t) for k in range(len(site.W)))


def _dv(site, M, t):
    """vector of (1-t) D_t(pi_phi || Q_M) and the value G_t(M)."""
    Q = centre_of(site, M, t)
    dv = -logsumexp(t * site.logW + (1 - t) * np.log(Q)[None, :], axis=1)
    return dv, G_primal(site, M, t)


def _grad_negG(site, M, t):
    """gradient of -G_t(M) with respect to M:  exp(G - (1-t)D_t(pi_phi||Q_M))   (derived by hand, see NOTES)."""
    dv, g = _dv(site, M, t)
    return np.exp(g - dv)


def _eg_primal(site, t, M0, iters=20000, tol=1e-13):
    """Exponentiated-gradient ascent on G_t(M) with backtracking; stops when the duality gap max_phi dv - G < tol."""
    M = np.maximum(M0, 1e-15)
    M /= M.sum()
    eta = 1.0
    dv, g = _dv(site, M, t)
    for it in range(iters):
        if dv.max() - g < tol:
            break
        while True:
            Mn = M * np.exp(eta * (dv - dv.max()))
            Mn /= Mn.sum()
            gn = G_primal(site, Mn, t)
            if gn >= g or eta < 1e-12:
                break
            eta *= 0.5
        M = Mn
        dv, g = _dv(site, M, t)
        eta *= 1.3
    return g, M


def renyi_primal(site, t, M0=None, tol=1e-12):
    """max_M G_t(M): SLSQP with the analytic gradient, then exponentiated-gradient polishing until the duality
    gap  max_phi (1-t)D_t(pi_phi||Q_M) - G_t(M)  is below tol.
    Returns (certified lower bound G_t(M), M, certified upper bound)."""
    nv = len(site.V)
    if M0 is None:
        M0 = np.full(nv, 1.0 / nv)
    cons = [dict(type="eq", fun=lambda M: M.sum() - 1.0, jac=lambda M: np.ones(nv))]
    f = lambda M: -G_primal(site, np.maximum(M, 1e-300), t)
    jac = lambda M: _grad_negG(site, np.maximum(M, 1e-300), t)
    res = minimize(f, M0, jac=jac, method="SLSQP", bounds=[(0, 1)] * nv, constraints=cons,
                   options=dict(ftol=1e-16, maxiter=500))
    M = np.maximum(res.x, 0)
    M /= M.sum()
    lo = G_primal(site, M, t)
    hi = radius_at(site, centre_of(site, M, t), t)
    if hi - lo > tol:
        lo2, M2 = _eg_primal(site, t, M, tol=tol)
        if lo2 >= lo:
            lo, M = lo2, M2
            hi = radius_at(site, centre_of(site, M, t), t)
    return lo, M, hi


def renyi_dual(site, t, Q0=None):
    """min_Q max_phi (1-t) D_t(pi_phi||Q) as an epigraph programme in (Q, z), solved by SLSQP with analytic
    Jacobians.  A programme different from renyi_primal (no M anywhere).  Returns (value, Q)."""
    q = site.q
    nv = len(site.W)
    if Q0 is None:
        Q0 = site.W.mean(axis=0)
    x0 = np.concatenate([Q0, [radius_at(site, Q0, t)]])
    Wt = site.W ** t

    def cons_fun(x):
        Q = np.maximum(x[:q], 1e-300)
        c = Wt @ Q ** (1 - t)
        return x[q] + np.log(c)

    def cons_jac(x):
        Q = np.maximum(x[:q], 1e-300)
        c = Wt @ Q ** (1 - t)
        J = np.zeros((nv, q + 1))
        J[:, :q] = (1 - t) * Wt * Q[None, :] ** (-t) / c[:, None]
        J[:, q] = 1.0
        return J

    e = np.zeros(q + 1)
    e[q] = 1.0
    s1 = np.concatenate([np.ones(q), [0.0]])
    res = minimize(lambda x: x[q], x0, jac=lambda x: e, method="SLSQP",
                   bounds=[(1e-12, 1)] * q + [(None, None)],
                   constraints=[dict(type="eq", fun=lambda x: x[:q].sum() - 1.0, jac=lambda x: s1),
                                dict(type="ineq", fun=cons_fun, jac=cons_jac)],
                   options=dict(ftol=1e-16, maxiter=1000))
    Q = np.maximum(res.x[:q], 1e-300)
    Q /= Q.sum()
    return radius_at(site, Q, t), Q


def Fstar_site(site, t):
    """F*_j(t) through the primal Renyi programme (certified lower bound); cached. F*(0)=F*(1)=0."""
    if t <= 0.0 or t >= 1.0:
        return 0.0
    key = round(float(t), 14)
    if key not in site._cache:
        lo, M, hi = renyi_primal(site, t)
        site._cache[key] = (lo, hi, M)
    return site._cache[key][0]


def Fstar_gap(site, t):
    Fstar_site(site, t)
    lo, hi, M = site._cache[round(float(t), 14)]
    return hi - lo

# ----------------------------------------------------------------------------------------------
# limits:  E (t -> 0)  and  a (t -> 1)
# ----------------------------------------------------------------------------------------------

def threshold_E(site):
    """E = max_M -ln sum_a prod_phi W[phi,a]^M[phi]  (lower bound)  = min_Q max_phi KL(Q||pi_phi) (upper bound at Q_M)."""
    nv = len(site.V)
    f = lambda M: logsumexp(M @ site.logW)
    res = minimize(f, np.full(nv, 1.0 / nv), method="SLSQP", bounds=[(0, 1)] * nv,
                   constraints=[dict(type="eq", fun=lambda M: M.sum() - 1.0)],
                   options=dict(ftol=1e-16, maxiter=1000))
    M = np.maximum(res.x, 0)
    M /= M.sum()
    lo = -logsumexp(M @ site.logW)
    lq = M @ site.logW
    Q = np.exp(lq - logsumexp(lq))
    hi = max(np.sum(Q * (np.log(Q) - site.logW[k])) for k in range(nv))
    return lo, hi, M


def capacity_a(site, iters=200000, tol=1e-13):
    """Shannon capacity of the vertex channel by Blahut-Arimoto; returns (lower, upper, M)."""
    nv = len(site.V)
    M = np.full(nv, 1.0 / nv)
    for it in range(iters):
        Q = M @ site.W
        D = np.sum(site.W * (site.logW - np.log(Q)[None, :]), axis=1)     # KL(pi_phi || Q)
        lo = float(M @ D)
        hi = float(D.max())
        if hi - lo < tol:
            break
        M = M * np.exp(D)
        M /= M.sum()
    return lo, hi, M

# ----------------------------------------------------------------------------------------------
# chains (several site types), exponents
# ----------------------------------------------------------------------------------------------

class Chain:
    def __init__(self, parts, name=""):
        """parts = [(lambda_j, Site_j), ...]"""
        self.parts = parts
        assert abs(sum(l for l, _ in parts) - 1) < 1e-12
        self.name = name

    def Fstar(self, t):
        return sum(l * Fstar_site(s, t) for l, s in self.parts)

    def E(self):
        return sum(l * threshold_E(s)[0] for l, s in self.parts)

    def a(self):
        return sum(l * capacity_a(s)[0] for l, s in self.parts)


def _maximise_1d(f, lo, hi, ngrid=400):
    """max of a continuous, possibly non-concave f on [lo,hi]: grid, then Brent on every grid cell that is a
    local grid maximum (handles kinks/two humps)."""
    ts = np.linspace(lo, hi, ngrid + 1)
    vals = np.array([f(t) for t in ts])
    best_val, best_t = vals.max(), ts[vals.argmax()]
    cand = [i for i in range(len(ts))
            if (i == 0 or vals[i] >= vals[i - 1]) and (i == len(ts) - 1 or vals[i] >= vals[i + 1])]
    for i in cand:
        l, r = ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)]
        res = minimize_scalar(lambda t: -f(t), bounds=(l, r), method="bounded",
                              options=dict(xatol=1e-12, maxiter=200))
        if -res.fun > best_val:
            best_val, best_t = -res.fun, res.x
    return best_val, best_t


def Rhat(Fstar, e, ngrid=400):
    """R^(e) = max_{0<=t<=1} [F*(t) - t e]."""
    return _maximise_1d(lambda t: Fstar(t) - t * e, 0.0, 1.0, ngrid)


def theta_na_direct(Fstar, x, ngrid=400, tmax=1 - 1e-6):
    """theta_na(x) = sup_{0<=tau<1} (F*(tau) - tau x)/(1 - tau)."""
    return _maximise_1d(lambda t: (Fstar(t) - t * x) / (1 - t), 0.0, tmax, ngrid)


def theta_na_pair(Fstar, x, ngrid=400):
    """theta_na(x) = R^(S^{-1}(x)),  S(e) = e + R^(e)   (the definition in the report)."""
    S = lambda e: e + Rhat(Fstar, e, ngrid)[0]
    lo, hi = -5.0, max(x, 1e-9) + 1.0
    e = brentq(lambda e: S(e) - x, lo, hi, xtol=1e-13)
    return Rhat(Fstar, e, ngrid)[0], e


# Gallager / sphere packing, written from the textbook definitions (not through F*):
def E0_site(site, rho):
    """max_M E_0(rho, M),  E_0(rho, M) = -ln sum_a ( sum_phi M W^(1/(1+rho)) )^(1+rho)."""
    if rho <= 0:
        return 0.0
    t = 1.0 / (1.0 + rho)
    return Fstar_site(site, t) / t      # (uses the identity G_t = t E_0; checked separately in tests)


def E0_gallager_raw(site, rho, M):
    """Gallager's E_0(rho, M) straight from its definition (no logs of logs) -- used to test the identity above."""
    s = (M[:, None] * site.W ** (1.0 / (1.0 + rho))).sum(axis=0)
    return -np.log(np.sum(s ** (1.0 + rho)))
