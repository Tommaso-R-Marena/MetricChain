"""Coordinator's own library for checking workstream W (sites with any alphabet, site law pi, envelope d, possibly asymmetric).

Written from the statements of the report, not from its code.  Orientation: gamma in L iff gamma(a) - gamma(b) <= d(a, b).
Vertices of L modulo constants; Gibbs laws pi_phi ~ pi e^{-phi};
  game form   F(gamma, t) = -ln val( K ),  K[a, phi] = (pi_phi(a)/pi_gamma(a))^t   (sampler mixes letters = rows; adversary mixes vertices)
  Renyi form  F*(t) = max_M  -t ln sum_a ( sum_phi M(phi) pi_phi(a)^t )^(1/t)
  E = max_M -ln sum_a prod_phi pi_phi(a)^M(phi),   a = max_M I(M; pi_.)  (Shannon capacity of the vertex channel)."""
import itertools, math
import numpy as np
from scipy.optimize import linprog, minimize

def vertices(d, tol=1e-9):
    """vertices of {g : g[a] - g[b] <= d[a][b]} with g[0] = 0 (q - 1 free coordinates; q - 1 tight independent constraints)"""
    q = len(d)
    cons = [(a, b) for a in range(q) for b in range(q) if a != b]
    out = []
    for S in itertools.combinations(cons, q - 1):
        A = np.zeros((q - 1, q - 1)); rhs = np.zeros(q - 1)
        for i, (a, b) in enumerate(S):
            if a > 0: A[i, a - 1] += 1
            if b > 0: A[i, b - 1] -= 1
            rhs[i] = d[a][b]
        if abs(np.linalg.det(A)) < 1e-12: continue
        g = np.concatenate([[0.0], np.linalg.solve(A, rhs)])
        if all(g[a] - g[b] <= d[a][b] + tol for a, b in cons) and not any(np.allclose(g, h, atol=1e-8) for h in out):
            out.append(g)
    return out

def gibbs(pi, g):
    w = np.asarray(pi)*np.exp(-np.asarray(g)); return w/w.sum()

def game_value(K):
    """min over mixed columns M of max over rows a of (K M)(a)  (LP)"""
    nr, nc = K.shape
    c = np.zeros(nc + 1); c[-1] = 1.0
    A_ub = np.hstack([K, -np.ones((nr, 1))]); b_ub = np.zeros(nr)
    A_eq = np.zeros((1, nc + 1)); A_eq[0, :nc] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)]*nc + [(None, None)], method="highs")
    return res.x[-1], res.x[:nc]

def F_game(pi, V, gamma, t):
    pg = gibbs(pi, gamma)
    K = np.array([(gibbs(pi, phi)/pg)**t for phi in V]).T          # rows: letters, columns: vertices
    v, M = game_value(K)
    return -math.log(v), M

def renyi_form(pi, V, t, starts=6, seed=0):
    """max_M -t ln sum_a (sum_phi M pi_phi^t)^(1/t) by projected exponentiated-gradient + SLSQP polish; returns (value, M, upper bound from the dual)"""
    P = np.array([gibbs(pi, phi) for phi in V])                     # vertices x letters
    Pt = P**t
    def N(M): return float(((M @ Pt)**(1/t)).sum())
    rng = np.random.default_rng(seed)
    best = None
    for s in range(starts):
        M0 = np.ones(len(V))/len(V) if s == 0 else rng.dirichlet(np.ones(len(V)))
        res = minimize(N, M0, method="SLSQP", bounds=[(0, 1)]*len(V), constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1}],
                       options={"ftol": 1e-15, "maxiter": 500})
        M = np.clip(res.x, 0, None); M /= M.sum()
        if best is None or N(M) < best[0]: best = (N(M), M)
    Nv, M = best
    val = -t*math.log(Nv)
    m = (M @ Pt)**(1/t); Q = m/m.sum()
    # dual: (1 - t) max_phi D_t(pi_phi || Q) >= F*  (D_t = ln sum pi_phi^t Q^(1-t) / (t - 1))
    upper = max(-math.log(float((Pt[i]*Q**(1 - t)).sum())) for i in range(len(V)))
    return val, M, upper, Q

def E_and_a(pi, V):
    P = np.array([gibbs(pi, phi) for phi in V]); lP = np.log(P)
    cons = [{"type": "eq", "fun": lambda M: M.sum() - 1}]
    bnd = [(0, 1)]*len(V)
    best_E = -1; best_a = -1
    rng = np.random.default_rng(1)
    for s in range(8):
        M0 = np.ones(len(V))/len(V) if s == 0 else rng.dirichlet(np.ones(len(V)))
        r1 = minimize(lambda M: math.log(float(np.exp(M @ lP).sum())), M0, method="SLSQP", bounds=bnd, constraints=cons, options={"ftol": 1e-15, "maxiter": 500})
        best_E = max(best_E, -r1.fun)
        def negI(M):
            M = np.clip(M, 1e-300, None); Qm = M @ P
            return -float((M[:, None]*P*np.log(P/Qm[None, :])).sum())
        r2 = minimize(negI, M0, method="SLSQP", bounds=bnd, constraints=cons, options={"ftol": 1e-15, "maxiter": 500})
        best_a = max(best_a, -r2.fun)
    return best_E, best_a

class Chain:
    """several site types with fractions lam"""
    def __init__(self, sites, lam):
        self.sites = sites; self.lam = lam
        self.V = [vertices(d) for (pi, d) in sites]
        self.cache = {}
    def Fstar(self, t):
        if t <= 1e-12 or t >= 1 - 1e-12: return 0.0
        key = round(t, 12)
        if key not in self.cache:
            self.cache[key] = sum(l*renyi_form(pi, V, t)[0] for l, (pi, d), V in zip(self.lam, self.sites, self.V))
        return self.cache[key]
    def Rmax(self, e, grid=400):
        ts = np.linspace(0, 1, grid + 1)
        vals = [self.Fstar(t) - t*e for t in ts]
        i = int(np.argmax(vals))
        lo, hi = ts[max(i - 1, 0)], ts[min(i + 1, grid)]
        g = (math.sqrt(5) - 1)/2
        f = lambda t: -(self.Fstar(t) - t*e)
        a, b = lo, hi
        c, dd = b - g*(b - a), a + g*(b - a); fc, fd = f(c), f(dd)
        for _ in range(60):
            if fc < fd: b, dd, fd = dd, c, fc; c = b - g*(b - a); fc = f(c)
            else: a, c, fc = c, dd, fd; dd = a + g*(b - a); fd = f(dd)
        t = (a + b)/2
        return max(-f(t), 0.0), t
    def theta_na(self, x, grid=400):
        ts = np.linspace(0, 0.999, grid + 1)
        vals = [(self.Fstar(t) - t*x)/(1 - t) for t in ts]
        i = int(np.argmax(vals))
        f = lambda t: -(self.Fstar(t) - t*x)/(1 - t)
        a, b = ts[max(i - 1, 0)], ts[min(i + 1, grid)]
        g = (math.sqrt(5) - 1)/2
        c, dd = b - g*(b - a), a + g*(b - a); fc, fd = f(c), f(dd)
        for _ in range(60):
            if fc < fd: b, dd, fd = dd, c, fc; c = b - g*(b - a); fc = f(c)
            else: a, c, fc = c, dd, fd; dd = a + g*(b - a); fd = f(dd)
        return max(-f((a + b)/2), 0.0)
    def E_a(self):
        Ea = [E_and_a(pi, V) for (pi, d), V in zip(self.sites, self.V)]
        return sum(l*x[0] for l, x in zip(self.lam, Ea)), sum(l*x[1] for l, x in zip(self.lam, Ea))

def hamming(q, u): return [[0.0 if a == b else u for b in range(q)] for a in range(q)]
SITES = {
    "bin":  ([0.7, 0.3], hamming(2, 1.0)),
    "path": ([0.5, 0.3, 0.2], [[0, 0.8, 2.4], [0.8, 0, 1.6], [2.4, 1.6, 0]]),
    "tri":  ([0.2, 0.5, 0.3], [[0, 1.0, 2.0], [1.0, 0, 1.5], [2.0, 1.5, 0]]),
    "asym": ([0.5, 0.3, 0.2], [[0, 1, 2], [0.5, 0, 1.5], [1, 0.5, 0]]),
}
