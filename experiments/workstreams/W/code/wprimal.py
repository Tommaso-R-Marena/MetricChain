"""wprimal.py -- PRIMAL single-letter solvers (minimisation over exit kernels / couplings), independent of the
game formula of wlib.py: no duality, no Lipschitz vertices, no Lagrange multiplier in t.

A labelled profile of a chain with site types j: for every j a law Pj[u] on labels u and letter laws
mu_j[u, a]  (the law of (U, T, X): P(T=j) = lam_j, P(U=u|T=j) = Pj[u], P(X=a|U=u,T=j) = mu_j[u,a]).

  MI(nu)     = sum_j lam_j sum_u Pj[u] KL(nu_ju || nubar_j)                      (= I(X';U|T))
  dist(nu->mu) = sum_j lam_j sum_u Pj[u] W_j(nu_ju, mu_ju)   (cost d_j[b, a], b = exit letter, a = letter of the profile)
  alpha(mu)  = sum_j lam_j sum_u Pj[u] KL(mu_ju || pi_j)                         (product measure)
  v(P)       = sum_j lam_j min_{P'} [ KL(P'||pi_j) + W_j(P', P_j) ]              (flat-histogram landscape)
  v_gamma(P) = sum_j lam_j [ -E_{P_j} gamma_j - ln Z_{gamma_j} ]                 (additive instance gamma)

  r_mu(e; landscape) = min { MI(nu) : dist(nu->mu) + landscape(nubar) <= e + alpha(mu) }
  cone(M; x)        = min { MI(nu) : sum_j lam_j sum_u Pj[u] KL(nu_ju || pi_{phi_u}) <= x }   (truncated generalised cone)

Solver: scipy SLSQP on couplings with analytic gradients (a convex programme: any KKT point is the minimum).
"""
import numpy as np
from scipy.optimize import minimize

EPS = 1e-300


def kl(p, q):
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    m = p > 0
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


class Profile:
    def __init__(self, P, mu):
        """P: list over site types of label laws; mu: list over site types of arrays (k_j, q_j)"""
        self.P = [np.asarray(p, float) / np.sum(p) for p in P]
        self.mu = [np.asarray(m, float) / np.asarray(m, float).sum(axis=1, keepdims=True) for m in mu]

    def mean(self):
        return [p @ m for p, m in zip(self.P, self.mu)]


def alpha(chain, prof):
    return sum(l * sum(p[u] * kl(m[u], s.pi) for u in range(len(p)))
               for l, s, p, m in zip(chain.lam, chain.sites, prof.P, prof.mu))


def MI(chain, prof, nu=None):
    nu = prof.mu if nu is None else nu
    out = 0.0
    for l, p, n in zip(chain.lam, prof.P, nu):
        nb = p @ n
        out += l * sum(p[u] * kl(n[u], nb) for u in range(len(p)))
    return out


def Irate(chain, P):
    return sum(l * kl(Pj, s.pi) for l, s, Pj in zip(chain.lam, chain.sites, P))


def v_dual(chain, P):
    """v via the maximum over additive instances (uses the polytope L; for cross-checks only)"""
    return sum(l * s.v(Pj)[0] for l, s, Pj in zip(chain.lam, chain.sites, P))


# ----------------------------------------------------------------------------------------------------------
class _Layout:
    """index bookkeeping for the variable vector: couplings K_ju[b, a] and (optionally) second-stage K'_j[c, b]"""

    def __init__(self, chain, prof, second):
        self.chain, self.prof, self.second = chain, prof, second
        self.off = []
        n = 0
        for j, s in enumerate(chain.sites):
            k = len(prof.P[j])
            self.off.append(n)
            n += k * s.q * s.q
        self.off2 = []
        if second:
            for j, s in enumerate(chain.sites):
                self.off2.append(n)
                n += s.q * s.q
        self.n = n

    def K(self, z, j):
        s = self.chain.sites[j]
        k = len(self.prof.P[j])
        return z[self.off[j]: self.off[j] + k * s.q * s.q].reshape(k, s.q, s.q)

    def K2(self, z, j):
        s = self.chain.sites[j]
        return z[self.off2[j]: self.off2[j] + s.q * s.q].reshape(s.q, s.q)

    def x0(self, shrink=0.0, rng=None):
        z = np.zeros(self.n)
        for j, s in enumerate(self.chain.sites):
            k = len(self.prof.P[j])
            K = self.K(z, j)
            for u in range(k):
                ker = np.eye(s.q)
                if rng is not None:
                    ker = (1 - shrink) * np.eye(s.q) + shrink * rng.dirichlet(np.ones(s.q), size=s.q).T
                K[u] = ker * self.prof.mu[j][u][None, :]
            if self.second:
                nb = self.prof.P[j] @ K.sum(axis=2)
                self.K2(z, j)[:] = np.diag(nb)
        return z

    def eq_matrix(self):
        rows, rhs = [], []
        for j, s in enumerate(self.chain.sites):
            k = len(self.prof.P[j])
            q = s.q
            for u in range(k):
                for a in range(q):
                    r = np.zeros(self.n)
                    for b in range(q):
                        r[self.off[j] + (u * q + b) * q + a] = 1.0
                    rows.append(r)
                    rhs.append(self.prof.mu[j][u][a])
            if self.second:
                for b in range(q):
                    r = np.zeros(self.n)
                    for c in range(q):
                        r[self.off2[j] + c * q + b] = 1.0
                    for u in range(k):
                        for a in range(q):
                            r[self.off[j] + (u * q + b) * q + a] -= self.prof.P[j][u]
                    rows.append(r)
                    rhs.append(0.0)
        return np.array(rows), np.array(rhs)


def _mi_and_grad(lay, z):
    chain, prof = lay.chain, lay.prof
    g = np.zeros(lay.n)
    val = 0.0
    for j, s in enumerate(chain.sites):
        K = lay.K(z, j)
        P = prof.P[j]
        nu = np.maximum(K.sum(axis=2), EPS)            # (k, q) exit laws
        nb = np.maximum(P @ nu, EPS)
        lr = np.log(nu / nb[None, :])
        val += chain.lam[j] * float(np.sum(P[:, None] * nu * lr))
        gj = chain.lam[j] * P[:, None] * lr           # d/d nu[u, b]
        lay.K(g, j)[:] = gj[:, :, None]
    return val, g


def _solve(lay, cons_fun, starts=3, seed=0, tol=1e-13, maxiter=1500):
    A, rhs = lay.eq_matrix()
    cons = [{"type": "eq", "fun": lambda z: A @ z - rhs, "jac": lambda z: A},
            {"type": "ineq", "fun": lambda z: -cons_fun(z)[0], "jac": lambda z: -cons_fun(z)[1]}]
    rng = np.random.default_rng(seed)
    best = None
    for it in range(starts):
        z0 = lay.x0() if it == 0 else lay.x0(shrink=0.02 * it, rng=rng)
        res = minimize(lambda z: _mi_and_grad(lay, z), z0, jac=True, method="SLSQP",
                       bounds=[(0.0, 1.0)] * lay.n, constraints=cons,
                       options={"ftol": tol, "maxiter": maxiter})
        z = res.x
        viol = max(float(np.max(np.abs(A @ z - rhs))), max(cons_fun(z)[0], 0.0))
        if viol < 1e-7 and (best is None or res.fun < best[0]):
            best = (float(res.fun), z, viol, res.status)
    if best is None:
        raise RuntimeError("primal solver: no feasible KKT point found")
    return best


def r_primal(chain, prof, e, landscape="H", gammas=None, starts=3, seed=0, B=None, full=False, Ifun=None):
    """min{ MI(nu) : dist(nu->mu) + landscape(nubar) <= e + alpha(mu) };
    landscape: 'H' (v, by a second-stage coupling), 'I' (the rate function itself), 'add' (additive instance gammas),
    'fun' (a general rate function of the joint type of a chain with ONE site type: Ifun(P) -> (value, gradient);
    B must be given)"""
    second = landscape == "H"
    lay = _Layout(chain, prof, second)
    Bv = (e + alpha(chain, prof)) if B is None else B

    def cons_fun(z):
        val = -Bv
        g = np.zeros(lay.n)
        for j, s in enumerate(chain.sites):
            K = lay.K(z, j)
            P = prof.P[j]
            lam = chain.lam[j]
            val += lam * float(np.sum(P[:, None, None] * K * s.d[None, :, :]))
            lay.K(g, j)[:] = lam * P[:, None, None] * s.d[None, :, :]
            nu = K.sum(axis=2)
            nb = P @ nu
            if landscape == "H":
                K2 = lay.K2(z, j)
                Pp = np.maximum(K2.sum(axis=1), EPS)
                val += lam * float(np.sum(K2 * s.d)) + lam * float(np.sum(Pp * np.log(Pp / s.pi)))
                lay.K2(g, j)[:] = lam * (s.d + (np.log(Pp / s.pi) + 1.0)[:, None])
            elif landscape == "I":
                nbs = np.maximum(nb, EPS)
                val += lam * float(np.sum(nbs * np.log(nbs / s.pi)))
                gj = lam * P[:, None] * (np.log(nbs / s.pi) + 1.0)[None, :]
                lay.K(g, j)[:] += gj[:, :, None]
            elif landscape == "fun":
                iv, ig = Ifun(np.maximum(nb, EPS))
                val += lam * iv
                gj = lam * P[:, None] * ig[None, :]
                lay.K(g, j)[:] += gj[:, :, None]
            elif landscape == "add":
                gam = np.asarray(gammas[j], float)
                val += lam * (-float(nb @ gam) - float(s.lnZ(gam)))
                gj = -lam * P[:, None] * gam[None, :]
                lay.K(g, j)[:] += gj[:, :, None]
            else:
                raise ValueError(landscape)
        return val, g

    val, z, viol, status = _solve(lay, cons_fun, starts=starts, seed=seed)
    if full:
        nus = [lay.K(z, j).sum(axis=2) for j in range(len(chain.sites))]
        return val, nus, lay, z
    return val


def cone_primal(chain, prof_labels, phis, x, starts=3, seed=0, full=False):
    """min{ MI(nu) : sum_j lam_j sum_u Pj[u] KL(nu_ju || pi_{phi_ju}) <= x }  (variables: the laws nu_ju directly)

    prof_labels: list over site types of label laws Pj; phis: list over site types of arrays (k_j, q_j) of site
    functions (members of L_j, e.g. vertices)."""
    lam = chain.lam
    sizes = [(len(P), s.q) for P, s in zip(prof_labels, chain.sites)]
    offs = np.cumsum([0] + [k * q for k, q in sizes])
    n = offs[-1]
    gib = [np.array([s.gibbs(ph) for ph in phj]) for s, phj in zip(chain.sites, phis)]

    def unpack(z):
        return [np.maximum(z[offs[j]: offs[j + 1]].reshape(sizes[j]), EPS) for j in range(len(sizes))]

    def obj(z):
        nus = unpack(z)
        val, g = 0.0, np.zeros(n)
        for j, nu in enumerate(nus):
            P = np.asarray(prof_labels[j], float)
            nb = P @ nu
            lr = np.log(nu / nb[None, :])
            val += lam[j] * float(np.sum(P[:, None] * nu * lr))
            g[offs[j]: offs[j + 1]] = (lam[j] * P[:, None] * lr).ravel()
        return val, g

    def con(z):
        nus = unpack(z)
        val, g = -x, np.zeros(n)
        for j, nu in enumerate(nus):
            P = np.asarray(prof_labels[j], float)
            lr = np.log(nu / gib[j])
            val += lam[j] * float(np.sum(P[:, None] * nu * lr))
            g[offs[j]: offs[j + 1]] = (lam[j] * P[:, None] * (lr + 1.0)).ravel()
        return val, g

    rows, rhs = [], []
    for j, (k, q) in enumerate(sizes):
        for u in range(k):
            r = np.zeros(n)
            r[offs[j] + u * q: offs[j] + (u + 1) * q] = 1.0
            rows.append(r)
            rhs.append(1.0)
    A, rhs = np.array(rows), np.array(rhs)
    cons = [{"type": "eq", "fun": lambda z: A @ z - rhs, "jac": lambda z: A},
            {"type": "ineq", "fun": lambda z: -con(z)[0], "jac": lambda z: -con(z)[1]}]
    rng = np.random.default_rng(seed)
    best = None
    for it in range(starts):
        z0 = np.concatenate([g.ravel() for g in gib])
        if it > 0:
            z0 = np.concatenate([((1 - 0.02 * it) * g + 0.02 * it * rng.dirichlet(np.ones(g.shape[1]), size=g.shape[0])).ravel() for g in gib])
        res = minimize(obj, z0, jac=True, method="SLSQP", bounds=[(1e-14, 1.0)] * n, constraints=cons,
                       options={"ftol": 1e-13, "maxiter": 1500})
        z = res.x
        viol = max(float(np.max(np.abs(A @ z - rhs))), max(con(z)[0], 0.0))
        if viol < 1e-7 and (best is None or res.fun < best[0]):
            best = (float(res.fun), z)
    if best is None:
        raise RuntimeError("cone solver failed")
    if full:
        return best[0], unpack(best[1])
    return best[0]


def dip_profile(chain, t, gammas=None, use_lp=False):
    """the generalised-dip profile of the game at slope t: labels = vertices carrying weight in the adversary's
    optimal mix M_j (the maximiser of the Renyi form, or -- use_lp -- the LP solution of the game K_t^{gamma_j}),
    letter law of label phi = Gibbs law pi_phi.  Returns (Profile, phis, Ms, gammas)"""
    if gammas is None:
        gammas = chain.gammas(t)
    P, mu, phis, Ms = [], [], [], []
    for j, s in enumerate(chain.sites):
        if use_lp:
            val, Q, M = s.strategies(gammas[j], t)
        else:
            M = chain.Ms(t)[j]
        keep = np.where(M > 1e-9)[0]
        P.append(M[keep] / M[keep].sum())
        V = s.V if chain.cols[j] is None else s.V[np.asarray(chain.cols[j])]
        phis.append(V[keep])
        mu.append(np.array([s.gibbs(ph) for ph in V[keep]]))
        Ms.append(M)
    return Profile(P, mu), phis, Ms, gammas
