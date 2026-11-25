"""wlib.py -- workstream W: heteropolymer product landscapes (several site types, alphabets q >= 2,
site laws pi_j, site envelopes d_j, not necessarily symmetric).

Conventions (kept everywhere in this directory):
  * a site is (pi, d): pi a probability vector of full support, d[a, b] >= 0, d[a, a] = 0, triangle
    inequality; the class is  psi(x) - psi(y) <= sum_i d(x_i, y_i)   (FIRST argument = the point where psi is
    larger).  Additive members: gamma with gamma[a] - gamma[b] <= d[a, b]  (the polytope L).
  * tilde(g) = g + ln Z_g, Z_g = sum_a pi[a] exp(-g[a]);  pi_g = pi * exp(-tilde g)  (Gibbs law of g).
  * game of the additive instance gamma at slope t:  K[a, phi] = (pi_phi[a] / pi_gamma[a])**t,
    phi over the vertices of L / constants;  F(gamma, t) = -ln max_Q min_phi sum_a Q[a] K[a, phi].
  * transport cost  W(P', P) = min sum kappa[c, b] d[c, b]  over couplings with FIRST marginal P'
    = max_{phi in vert(L)} <P' - P, phi>.

Own code, numpy/scipy only.  Nothing is imported from the repository.
"""
import itertools
import math

import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar, brentq

TOL = 1e-9


# ----------------------------------------------------------------------------------------------------------
# sites
# ----------------------------------------------------------------------------------------------------------
def closure(d):
    """shortest-path closure (triangle inequality) of a nonnegative matrix with zero diagonal"""
    d = np.array(d, float)
    q = len(d)
    for k in range(q):
        d = np.minimum(d, d[:, [k]] + d[[k], :])
    return d


def lip_vertices(d):
    """vertices of {g : g[a]-g[b] <= d[a,b], g[0]=0}; rows of the returned array"""
    q = len(d)
    pairs = [(a, b) for a in range(q) for b in range(q) if a != b]
    out = []
    for comb in itertools.combinations(pairs, q - 1):
        A = np.zeros((q - 1, q - 1))
        rhs = np.zeros(q - 1)
        for r, (a, b) in enumerate(comb):
            if a > 0:
                A[r, a - 1] += 1.0
            if b > 0:
                A[r, b - 1] -= 1.0
            rhs[r] = d[a, b]
        if abs(np.linalg.det(A)) < 1e-12:
            continue
        g = np.concatenate([[0.0], np.linalg.solve(A, rhs)])
        ok = True
        for (a, b) in pairs:
            if g[a] - g[b] > d[a, b] + 1e-9:
                ok = False
                break
        if not ok:
            continue
        if not any(np.max(np.abs(g - h)) < 1e-9 for h in out):
            out.append(g)
    return np.array(out)


class Site:
    def __init__(self, pi, d, name=""):
        self.pi = np.array(pi, float)
        self.pi = self.pi / self.pi.sum()
        self.q = len(self.pi)
        d = np.array(d, float)
        assert d.shape == (self.q, self.q) and np.all(np.diag(d) == 0) and np.all(d >= 0)
        dc = closure(d)
        if np.max(np.abs(dc - d)) > 1e-12:
            print(f"[Site {name}] envelope was not transitively closed; closed (max change {np.max(np.abs(dc-d)):.3g})")
        self.d = dc
        self.name = name
        self.V = lip_vertices(self.d)            # (nv, q), normalised phi[0] = 0
        self.nv = len(self.V)
        self.Vt = self.tilde(self.V)             # normalised vertices: E_pi exp(-Vt) = 1
        # which vertices are distance functions d(., b) (single dips)?
        self.is_dist = np.zeros(self.nv, bool)
        for b in range(self.q):
            g = self.d[:, b] - self.d[0, b]
            for k in range(self.nv):
                if np.max(np.abs(self.V[k] - g)) < 1e-8:
                    self.is_dist[k] = True

    # --- elementary site functions -------------------------------------------------------------------
    def lnZ(self, g):
        g = np.asarray(g, float)
        return np.log(np.sum(self.pi * np.exp(-g), axis=-1))

    def tilde(self, g):
        g = np.asarray(g, float)
        return g + self.lnZ(g)[..., None]

    def gibbs(self, g):
        return self.pi * np.exp(-self.tilde(g))

    def in_L(self, g, tol=1e-9):
        g = np.asarray(g, float)
        diff = g[..., :, None] - g[..., None, :]
        return np.all(diff <= self.d + tol, axis=(-1, -2))

    def W(self, P1, P):
        """transport cost with first marginal P1 (the 'exit' / larger-psi side): max over vertices <P1-P, phi>"""
        return np.max((np.asarray(P1) - np.asarray(P)) @ self.V.T, axis=-1)

    def v(self, P):
        """v(P) = max_{gamma in L} [ -E_P gamma - ln Z_gamma ]  (concave maximisation; zoom + polish)"""
        val, g = max_over_L(self, lambda G: -(G @ np.asarray(P, float)) - self.lnZ(G))
        return val, g

    # --- the game ----------------------------------------------------------------------------------
    def Kmat(self, gamma, t):
        """K[..., a, phi] for a batch of gamma (..., q) and scalar or batch t"""
        gt = self.tilde(gamma)                                  # (..., q)
        sig = self.Vt.T[None, ...] - gt[..., :, None] if gt.ndim > 1 else self.Vt.T - gt[:, None]
        t = np.asarray(t, float)
        if t.ndim > 0:
            t = t[..., None, None]
        return np.exp(-t * sig)

    def F(self, gamma, t, cols=None):
        """F(gamma, t) = -ln val(K_t^gamma); vectorised over gamma (N, q) and t (scalar or (N,))"""
        gamma = np.asarray(gamma, float)
        single = gamma.ndim == 1
        if single:
            gamma = gamma[None, :]
        K = self.Kmat(gamma, t)
        if cols is not None:
            K = K[..., cols]
        val = game_value_batch(K)
        F = -np.log(val)
        return F[0] if single else F

    def sig0(self, gamma):
        gt = self.tilde(np.asarray(gamma, float))
        return self.Vt.T[None, ...] - gt[..., :, None]         # (N, q, nv): tilde phi[a] - tilde gamma[a]

    def thr(self, gamma, cols=None):
        """threshold of the additive instance gamma: min_Q max_phi E_Q[tilde phi - tilde gamma] = lim F(gamma,t)/t"""
        gamma = np.asarray(gamma, float)
        single = gamma.ndim == 1
        if single:
            gamma = gamma[None, :]
        S = self.sig0(gamma)
        if cols is not None:
            S = S[..., cols]
        val = -game_value_batch(-S)
        return val[0] if single else val

    def Fstar_game(self, t, cols=None, return_gamma=False):
        """F*_j(t) = max_{gamma in L} F(gamma, t) by a grid-and-zoom search over L (slow, accurate to about 1e-6
        only: the maximum over gamma is a kink).  Kept as an independent check of Fstar."""
        if t <= 0.0:
            return (0.0, np.zeros(self.q)) if return_gamma else 0.0
        val, g = max_over_L(self, lambda G: self.F(G, t, cols=cols))
        return (val, g) if return_gamma else val

    def Estar_game(self, cols=None, return_gamma=False):
        """class threshold of the site by the zoom search: max_gamma thr(gamma)"""
        val, g = max_over_L(self, lambda G: self.thr(G, cols=cols))
        return (val, g) if return_gamma else val

    # --- the maximised game function in closed variational form (report, Theorem W3.1) ----------------
    def _W(self, cols=None):
        W = self.pi[None, :] * np.exp(-self.Vt)                 # (nv, q): Gibbs laws of the vertices
        return W if cols is None else W[np.asarray(cols)]

    def renyi(self, t, cols=None):
        """F*(t) = max_gamma F(gamma,t) = -t ln min_M sum_a ( sum_phi M[phi] pi_phi[a]^t )^(1/t)
                 = (1 - t) * (Renyi capacity of order t of the channel  vertex phi -> pi_phi).
        Returns dict(F, upper, M, Q, gamma): F = value at the M found (a lower bound of F*),
        upper = (1-t) max_phi D_t(pi_phi || Q) (an upper bound of F*), Q = Sibson centre = Gibbs law of the
        hardest additive instance gamma (normalised gamma[0] = 0)."""
        W = self._W(cols)
        nv = len(W)
        lW = np.log(W)
        Wt = np.exp(t * lW)

        def N(M):
            s = np.maximum(M, 0.0) @ Wt
            return float(np.sum(s ** (1.0 / t)))

        def gN(M):
            s = np.maximum(M, 1e-300) @ Wt
            return (Wt * (s ** (1.0 / t - 1.0))[None, :]).sum(axis=1) / t

        cons = [{"type": "eq", "fun": lambda M: M.sum() - 1.0, "jac": lambda M: np.ones(nv)}]
        best = None
        starts = [np.ones(nv) / nv]
        if nv > 2:
            rng = np.random.default_rng(12345)
            starts += [rng.dirichlet(np.ones(nv)) for _ in range(2)]
        for M0 in starts:
            res = minimize(N, M0, jac=gN, method="SLSQP", bounds=[(0.0, 1.0)] * nv, constraints=cons,
                           options={"ftol": 1e-16, "maxiter": 1000})
            if best is None or res.fun < best.fun:
                best = res
        M = np.maximum(best.x, 0.0)
        M[M < 1e-12] = 0.0
        M = M / M.sum()
        m = (M @ Wt) ** (1.0 / t)
        Q = m / m.sum()
        F = -t * math.log(m.sum())
        upper = max(-math.log(float(np.sum(Wt[k] * Q ** (1.0 - t)))) for k in range(nv))
        gam = -np.log(Q / self.pi)
        gam = gam - gam[0]
        return {"F": F, "upper": upper, "M": M, "Q": Q, "gamma": gam}

    def Fstar(self, t, cols=None, return_gamma=False):
        if t <= 0.0 or t >= 1.0:
            return (0.0, np.zeros(self.q)) if return_gamma else 0.0
        r = self.renyi(t, cols)
        return (r["F"], r["gamma"]) if return_gamma else r["F"]

    def Estar(self, cols=None, full=False):
        """class threshold E = lim F*(t)/t = max_M -ln sum_a prod_phi pi_phi[a]^M[phi] = min_Q max_phi KL(Q || pi_phi)"""
        W = self._W(cols)
        nv = len(W)
        lW = np.log(W)

        def N(M):
            return float(np.sum(np.exp(M @ lW)))

        def gN(M):
            return lW @ np.exp(M @ lW)

        cons = [{"type": "eq", "fun": lambda M: M.sum() - 1.0, "jac": lambda M: np.ones(nv)}]
        res = minimize(N, np.ones(nv) / nv, jac=gN, method="SLSQP", bounds=[(0.0, 1.0)] * nv, constraints=cons,
                       options={"ftol": 1e-16, "maxiter": 1000})
        M = np.maximum(res.x, 0.0)
        M = M / M.sum()
        m = np.exp(M @ lW)
        Q = m / m.sum()
        E = -math.log(m.sum())
        upper = max(float(np.sum(Q * np.log(Q / W[k]))) for k in range(nv))
        if full:
            gam = -np.log(Q / self.pi)
            return {"E": E, "upper": upper, "M": M, "Q": Q, "gamma": gam - gam[0]}
        return E

    def capacity(self, cols=None, full=False):
        """a = lim F*(t)/(1-t) = Shannon capacity max_M I(M; pi_.) = min_Q max_phi KL(pi_phi || Q)  (Blahut-Arimoto)"""
        W = self._W(cols)
        nv = len(W)
        M = np.ones(nv) / nv
        for it in range(200000):
            Q = M @ W
            D = np.sum(W * np.log(W / Q[None, :]), axis=1)
            lo, hi = float(M @ D), float(D.max())
            if hi - lo < 1e-13:
                break
            M = M * np.exp(D)
            M = M / M.sum()
        if full:
            return {"a": lo, "upper": hi, "M": M, "Q": Q}
        return lo

    def strategies(self, gamma, t):
        """optimal strategies of the game K_t^gamma by LP: (value, Q (sampler, on letters), M (adversary, on vertices))"""
        K = self.Kmat(np.asarray(gamma, float)[None, :], t)[0]
        return game_lp(K)


# ----------------------------------------------------------------------------------------------------------
# matrix games
# ----------------------------------------------------------------------------------------------------------
def game_lp(K):
    """max_Q min_c sum_a Q[a] K[a, c]; returns (val, Q, M) with M the optimal mix of the column player"""
    q, nc = K.shape
    c = np.zeros(q + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-K.T, np.ones((nc, 1))])
    b_ub = np.zeros(nc)
    A_eq = np.zeros((1, q + 1))
    A_eq[0, :q] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0],
                  bounds=[(0, None)] * q + [(None, None)], method="highs")
    assert res.status == 0, res.message
    Q = res.x[:q]
    val = res.x[-1]
    M = -np.asarray(res.ineqlin.marginals)
    M = np.maximum(M, 0.0)
    if M.sum() > 0:
        M = M / M.sum()
    return val, Q, M


def game_value_batch(K):
    """value max_Q min_c <Q, K[..., :, c]> for a batch K[..., q, nc]; exact enumeration for q = 2, 3"""
    K = np.asarray(K, float)
    q, nc = K.shape[-2], K.shape[-1]
    batch = K.shape[:-2]
    Kf = K.reshape((-1, q, nc))
    if q == 2:
        val = _game2(Kf)
    elif q == 3:
        val = _game3(Kf)
    else:
        val = np.array([game_lp(k)[0] for k in Kf])
    return val.reshape(batch)


def _game2(K):
    A = K[:, 0, :]
    B = K[:, 1, :] - K[:, 0, :]
    nc = K.shape[2]
    best = np.maximum(np.min(A, axis=1), np.min(A + B, axis=1))
    for c1 in range(nc):
        for c2 in range(c1 + 1, nc):
            den = B[:, c2] - B[:, c1]
            with np.errstate(divide="ignore", invalid="ignore"):
                x = (A[:, c1] - A[:, c2]) / den
            ok = np.isfinite(x) & (x > 0) & (x < 1)
            xx = np.where(ok, x, 0.0)
            val = np.min(A + B * xx[:, None], axis=1)
            best = np.where(ok, np.maximum(best, val), best)
    return best


def _game3(K):
    A = K[:, 0, :]
    B = K[:, 1, :] - K[:, 0, :]
    C = K[:, 2, :] - K[:, 0, :]
    nc = K.shape[2]

    def val_at(x, y):
        return np.min(A + B * x[:, None] + C * y[:, None], axis=1)

    N = K.shape[0]
    z, o = np.zeros(N), np.ones(N)
    best = np.maximum.reduce([val_at(z, z), val_at(o, z), val_at(z, o)])
    eps = 1e-13
    for c1 in range(nc):
        for c2 in range(c1 + 1, nc):
            with np.errstate(divide="ignore", invalid="ignore"):
                # edge y = 0
                x = (A[:, c1] - A[:, c2]) / (B[:, c2] - B[:, c1])
                ok = np.isfinite(x) & (x > 0) & (x < 1)
                xx = np.where(ok, x, 0.0)
                best = np.where(ok, np.maximum(best, val_at(xx, z)), best)
                # edge x = 0
                y = (A[:, c1] - A[:, c2]) / (C[:, c2] - C[:, c1])
                ok = np.isfinite(y) & (y > 0) & (y < 1)
                yy = np.where(ok, y, 0.0)
                best = np.where(ok, np.maximum(best, val_at(z, yy)), best)
                # edge x + y = 1 : f = A + C + (B - C) x
                x = ((A[:, c1] + C[:, c1]) - (A[:, c2] + C[:, c2])) / ((B[:, c2] - C[:, c2]) - (B[:, c1] - C[:, c1]))
                ok = np.isfinite(x) & (x > 0) & (x < 1)
                xx = np.where(ok, x, 0.0)
                best = np.where(ok, np.maximum(best, val_at(xx, 1.0 - xx)), best)
    for c1 in range(nc):
        for c2 in range(c1 + 1, nc):
            for c3 in range(c2 + 1, nc):
                a11 = B[:, c1] - B[:, c2]
                a12 = C[:, c1] - C[:, c2]
                a21 = B[:, c1] - B[:, c3]
                a22 = C[:, c1] - C[:, c3]
                r1 = A[:, c2] - A[:, c1]
                r2 = A[:, c3] - A[:, c1]
                det = a11 * a22 - a12 * a21
                with np.errstate(divide="ignore", invalid="ignore"):
                    x = (r1 * a22 - a12 * r2) / det
                    y = (a11 * r2 - a21 * r1) / det
                ok = np.isfinite(x) & np.isfinite(y) & (x > eps) & (y > eps) & (x + y < 1 - eps)
                xx = np.where(ok, x, 0.0)
                yy = np.where(ok, y, 0.0)
                best = np.where(ok, np.maximum(best, val_at(xx, yy)), best)
    return best


# ----------------------------------------------------------------------------------------------------------
# maximisation over the Lipschitz polytope L (global: grid + zoom; q = 2, 3; q >= 4: random + zoom)
# ----------------------------------------------------------------------------------------------------------
def max_over_L(site, fun, n0=41, nz=11, levels=14, shrink=0.35):
    """maximise fun(G) (vectorised over rows G of shape (N, q), G[:, 0] = 0) over L; returns (value, argmax)"""
    q = site.q
    lo = site.V.min(axis=0)[1:]
    hi = site.V.max(axis=0)[1:]
    best_val, best_g = -np.inf, None
    centre = 0.5 * (lo + hi)
    half = 0.5 * (hi - lo)
    n = n0
    for lev in range(levels):
        axes = [np.linspace(max(lo[i], centre[i] - half[i]), min(hi[i], centre[i] + half[i]), n) for i in range(q - 1)]
        mesh = np.meshgrid(*axes, indexing="ij")
        G = np.concatenate([np.zeros((mesh[0].size, 1))] + [m.reshape(-1, 1) for m in mesh], axis=1)
        ok = site.in_L(G, tol=1e-12)
        G = G[ok]
        if len(G) == 0:
            break
        vals = fun(G)
        k = int(np.argmax(vals))
        if vals[k] > best_val:
            best_val, best_g = float(vals[k]), G[k].copy()
        centre = best_g[1:].copy()
        half = half * shrink if lev > 0 else half * (4.0 / (n0 - 1))
        n = nz
    return best_val, best_g


# ----------------------------------------------------------------------------------------------------------
# chains: several site types with fractions lam
# ----------------------------------------------------------------------------------------------------------
class Chain:
    def __init__(self, sites, lam, name="", cols=None):
        self.sites = list(sites)
        self.lam = np.array(lam, float)
        self.lam = self.lam / self.lam.sum()
        self.name = name
        self.cols = cols if cols is not None else [None] * len(self.sites)   # optional restriction of the vertex sets
        self._cache = [dict() for _ in self.sites]

    def renyi_j(self, j, t):
        key = round(float(t), 14)
        c = self._cache[j]
        if key not in c:
            s = self.sites[j]
            if t <= 0.0 or t >= 1.0:
                c[key] = {"F": 0.0, "upper": 0.0, "M": None, "Q": None, "gamma": np.zeros(s.q)}
            else:
                c[key] = s.renyi(float(t), cols=self.cols[j])
        return c[key]

    def Fstar_j(self, j, t):
        r = self.renyi_j(j, t)
        return r["F"], r["gamma"]

    def Fstar(self, t):
        return sum(l * self.renyi_j(j, t)["F"] for j, l in enumerate(self.lam))

    def Fstar_upper(self, t):
        return sum(l * self.renyi_j(j, t)["upper"] for j, l in enumerate(self.lam))

    def gammas(self, t):
        return [self.renyi_j(j, t)["gamma"] for j in range(len(self.sites))]

    def Ms(self, t):
        return [self.renyi_j(j, t)["M"] for j in range(len(self.sites))]

    def E(self):
        return sum(l * s.Estar(cols=c) for l, s, c in zip(self.lam, self.sites, self.cols))

    def table(self, nt=201):
        ts = np.linspace(0.0, 1.0, nt)
        return ts, np.array([self.Fstar(t) for t in ts])

    def R(self, e, nt=201, return_t=False):
        """R(e) = max_{0<=t<=1} [F*(t) - t e]"""
        ts, Fs = self.table(nt)
        obj = Fs - ts * e
        k = int(np.argmax(obj))
        a, b = ts[max(k - 1, 0)], ts[min(k + 1, nt - 1)]
        res = minimize_scalar(lambda t: -(self.Fstar(t) - t * e), bounds=(a, b), method="bounded",
                              options={"xatol": 1e-10})
        val, tt = -res.fun, res.x
        if obj[k] > val:
            val, tt = obj[k], ts[k]
        return (val, tt) if return_t else val

    def a(self, nt=201):
        """a = theta_na(0+) = sup_{t<1} F*(t)/(1-t) = sum_j lam_j * (Shannon capacity of the vertex channel of site j)"""
        val = sum(l * s.capacity(cols=c) for l, s, c in zip(self.lam, self.sites, self.cols))
        return val, None

    def S(self, e, nt=201):
        return e + self.R(e, nt)

    def Sinv(self, x, nt=201):
        """the e >= e_c with e + R(e) = x (x > 0)"""
        lo = -self.a(nt)[0] - 1.0
        hi = max(x, 1e-12) + 1.0
        return brentq(lambda e: self.S(e, nt) - x, lo, hi, xtol=1e-12)

    def theta_na(self, x, nt=201):
        e = self.Sinv(x, nt)
        return self.R(e, nt), e

    def theta_na_direct(self, x, nt=201):
        """max_{tau<1} (F*(tau) - tau x)/(1 - tau)"""
        ts, Fs = self.table(nt)
        obj = (Fs[:-1] - ts[:-1] * x) / (1 - ts[:-1])
        k = int(np.argmax(obj))
        a, b = ts[max(k - 1, 0)], min(ts[min(k + 1, nt - 1)], 1 - 1e-9)
        res = minimize_scalar(lambda t: -(self.Fstar(t) - t * x) / (1 - t), bounds=(a, b), method="bounded",
                              options={"xatol": 1e-10})
        return max(-res.fun, obj[k]), res.x


# ----------------------------------------------------------------------------------------------------------
# binary closed forms (theory report, Theorem 11.59(b)) -- used as controls only
# ----------------------------------------------------------------------------------------------------------
def F_binary_closed(p, u, gamma, t):
    """site {0,1}, pi = (1-p, p), d = u*Hamming, additive instance gamma*|x|"""
    theta = math.log((1 - p) / p)
    lam = theta + gamma
    lp, lm = theta + u, theta - u
    C = lambda x: 2 * math.cosh(x / 2)
    num = math.sinh(t * (lp - lam) / 2) * C(lm) ** t + math.sinh(t * (lam - lm) / 2) * C(lp) ** t
    return math.log(num / math.sinh(t * u)) - t * math.log(C(lam))


def binary_site(p, u, name=""):
    return Site([1 - p, p], [[0, u], [u, 0]], name=name or f"bin(p={p},u={u})")


def klb(a, b):
    out = 0.0
    if a > 0:
        out += a * math.log(a / b)
    if a < 1:
        out += (1 - a) * math.log((1 - a) / (1 - b))
    return out
