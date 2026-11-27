"""Workstream Y -- own library (written from the statements of theory report 11.26; shares no code with wv_lib.py).

Conventions.  A "site" is (pi, V): a law pi on q letters and a list V of vertices of its Lipschitz polytope
{g : g(a) - g(b) <= d(a,b)} (modulo constants).  The vertex channel sends a vertex phi to its Gibbs law
pi_phi ~ pi e^{-phi}.  For 0 < t < 1
    F*(t) = max_M  -t ln sum_a ( sum_phi M(phi) pi_phi(a)^t )^(1/t)  =  min_Q max_phi  -ln sum_a pi_phi(a)^t Q(a)^(1-t)
    E     = max_M  -ln sum_a prod_phi pi_phi(a)^M(phi)               =  min_Q max_phi KL(Q || pi_phi)
    a     = max_M  I(M; pi_.)                                        =  min_Q max_phi KL(pi_phi || Q)
Every solver returns (lower, upper, M, Q): lower is the primal value at M, upper the dual value at the Q built from M.
"""
import itertools, math
import numpy as np
from scipy.optimize import linprog, minimize

# ----------------------------------------------------------------------------- Gibbs laws
def gibbs_rows(pi, V):
    """rows: Gibbs laws of the vertices (stable in logs)"""
    lp = np.log(np.asarray(pi, float))[None, :] - np.asarray(V, float)
    lp -= lp.max(axis=1, keepdims=True)
    P = np.exp(lp)
    return P / P.sum(axis=1, keepdims=True)

# ----------------------------------------------------------------------------- Renyi form (Arimoto iteration + duality bracket)
def renyi_F(P, t, tol=1e-12, itmax=200000, M0=None):
    """F*(t) for the channel with rows P.  Returns (lower, upper, M, Q).  lower <= F* <= upper always (weak duality)."""
    Pt = P ** t
    nv = P.shape[0]
    M = np.full(nv, 1.0 / nv) if M0 is None else np.array(M0, float)
    best = None
    for it in range(itmax):
        s = M @ Pt
        N = float((s ** (1.0 / t)).sum())
        alpha = s ** ((1.0 - t) / t)
        r = Pt @ alpha
        lower = -t * math.log(N)
        upper = -math.log(float(r.min())) + (1.0 - t) * math.log(N)
        if best is None or upper - lower < best[1] - best[0]:
            Q = s ** (1.0 / t); Q /= Q.sum()
            best = (lower, upper, M.copy(), Q)
        if upper - lower < tol:
            break
        M = M * (r / N) ** (-t / (1.0 - t))
        M /= M.sum()
    return best

def renyi_F_slsqp(P, t, starts=4, seed=0):
    """independent primal solver (SLSQP on the simplex); returns the best value found (a lower bound)"""
    Pt = P ** t; nv = P.shape[0]
    f = lambda M: float(((np.clip(M, 0, None) @ Pt) ** (1.0 / t)).sum())
    rng = np.random.default_rng(seed); best = None
    for k in range(starts):
        M0 = np.full(nv, 1.0 / nv) if k == 0 else rng.dirichlet(np.ones(nv))
        res = minimize(f, M0, method="SLSQP", bounds=[(0, 1)] * nv,
                       constraints=[{"type": "eq", "fun": lambda M: M.sum() - 1}], options={"ftol": 1e-15, "maxiter": 1000})
        M = np.clip(res.x, 0, None); M /= M.sum()
        v = -t * math.log(f(M))
        if best is None or v > best: best = v
    return best

def game_value(K):
    """value of the matrix game: min over mixed columns of max over rows of (K M)(a)  (linear programme)"""
    nr, nc = K.shape
    c = np.zeros(nc + 1); c[-1] = 1.0
    A_ub = np.hstack([K, -np.ones((nr, 1))]); b_ub = np.zeros(nr)
    A_eq = np.zeros((1, nc + 1)); A_eq[0, :nc] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * nc + [(None, None)], method="highs")
    return res.x[-1], res.x[:nc]

def F_game(P, Q, t):
    """game form at the instance whose Gibbs law is Q:  F(gamma,t) = -ln val(K), K[a,phi] = (pi_phi(a)/Q(a))^t.
    An inner solver that shares nothing with the Arimoto iteration (linear programming)."""
    K = ((P / Q[None, :]) ** t).T
    v, M = game_value(K)
    return -math.log(v), M

# ----------------------------------------------------------------------------- thresholds E and capacities a
def E_threshold(P, tol=1e-12, itmax=400000):
    """E = max_M -ln sum_a prod_phi P[phi,a]^M[phi] = min_Q max_phi KL(Q||P_phi).  Returns (lower, upper, M, Q)."""
    lP = np.log(P); nv = P.shape[0]
    M = np.full(nv, 1.0 / nv); eta = 1.0; best = None
    def val(M):
        z = M @ lP; zm = z.max(); w = np.exp(z - zm); S = w.sum()
        return -(zm + math.log(S)), w / S
    lower, Q = val(M)
    for it in range(itmax):
        kl = (Q * np.log(Q)).sum() - lP @ Q               # KL(Q||P_phi) for every phi
        upper = float(kl.max())
        if best is None or upper - lower < best[1] - best[0]: best = (lower, upper, M.copy(), Q.copy())
        if upper - lower < tol: break
        # exponentiated gradient with backtracking (the objective is concave in M, gradient = kl + const)
        while True:
            M2 = M * np.exp(eta * (kl - kl.max())); M2 /= M2.sum()
            l2, Q2 = val(M2)
            if l2 >= lower - 1e-16 or eta < 1e-8: break
            eta *= 0.5
        M, lower, Q = M2, l2, Q2
        eta *= 1.3
    return best

def capacity(P, tol=1e-12, itmax=400000):
    """Shannon capacity by Blahut-Arimoto.  Returns (lower, upper, M, Q)."""
    nv = P.shape[0]; M = np.full(nv, 1.0 / nv); lP = np.log(P); best = None
    for it in range(itmax):
        Q = M @ P
        kl = (P * (lP - np.log(Q)[None, :])).sum(axis=1)
        lower = float(M @ kl); upper = float(kl.max())
        if best is None or upper - lower < best[1] - best[0]: best = (lower, upper, M.copy(), Q.copy())
        if upper - lower < tol: break
        M = M * np.exp(kl - kl.max()); M /= M.sum()
    return best

# ----------------------------------------------------------------------------- exponents from a game function
def golden_max(f, a, b, it=80):
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a); fc, fd = f(c), f(d)
    for _ in range(it):
        if fc > fd: b, d, fd = d, c, fc; c = b - g * (b - a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a + g * (b - a); fd = f(d)
    x = (a + b) / 2
    return x, f(x)

def maximise_on_grid(f, lo, hi, grid=60, it=80):
    ts = np.linspace(lo, hi, grid + 1)
    vals = [f(t) for t in ts]
    i = int(np.argmax(vals))
    return golden_max(f, ts[max(i - 1, 0)], ts[min(i + 1, grid)], it=it)

class GameFunction:
    """wraps t -> (lower, upper) of F*(t) per site (already divided by the block length if wanted), caches"""
    def __init__(self, P, scale=1.0, tol=1e-11):
        self.P = P; self.scale = scale; self.tol = tol; self.cache = {}
    def F(self, t):
        if t <= 1e-9 or t >= 1 - 1e-9: return (0.0, 0.0)
        k = round(t, 13)
        if k not in self.cache:
            lo, up, M, Q = renyi_F(self.P, t, tol=self.tol)
            self.cache[k] = (lo / self.scale, up / self.scale)
        return self.cache[k]
    def Rhat(self, e, grid=60):
        """max_t [F*(t) - t e] -> (t*, lower, upper at t*)"""
        t, v = maximise_on_grid(lambda t: self.F(t)[0] - t * e, 1e-4, 1 - 1e-4, grid)
        return t, max(v, 0.0), max(self.F(t)[1] - t * e, 0.0)
    def theta_na(self, x, grid=60):
        t, v = maximise_on_grid(lambda t: (self.F(t)[0] - t * x) / (1 - t), 1e-4, 1 - 1e-3, grid)
        return t, max(v, 0.0), max((self.F(t)[1] - t * x) / (1 - t), 0.0)

def cube_numbers(u):
    """closed forms for the uniform binary cube at slope u: (h, a, E)"""
    Psi = lambda s: math.log(math.cosh(s / 2))
    t, h = maximise_on_grid(lambda t: t * Psi(u) - Psi(t * u), 1e-6, 1 - 1e-6, 400)
    pu = 1 / (1 + math.exp(u))
    a = math.log(2) + pu * math.log(pu) + (1 - pu) * math.log(1 - pu)
    return h, a, Psi(u)

# ----------------------------------------------------------------------------- hypercube blocks: laws and vertices
def bits(x, L):
    return [(x >> i) & 1 for i in range(L)]            # site i = bit i (site 0 is the left end of the block)

def bsc_block_law(L, p):
    """stationary law of L consecutive sites of the binary symmetric chain with flip probability p (= free-b.c. block law)"""
    P = np.zeros(2 ** L)
    for x in range(2 ** L):
        b = bits(x, L); w = 0.5
        for i in range(L - 1): w *= (p if b[i] != b[i + 1] else 1 - p)
        P[x] = w
    return P

def bsc_block_law_cond(L, p, prev):
    """law of sites 1..L given the letter prev of site 0"""
    P = np.zeros(2 ** L)
    for x in range(2 ** L):
        b = [prev] + bits(x, L); w = 1.0
        for i in range(L): w *= (p if b[i] != b[i + 1] else 1 - p)
        P[x] = w
    return P

def cube_edges(L):
    return [(x, x | (1 << i), i) for x in range(2 ** L) for i in range(L) if not (x >> i) & 1]

def spanning_trees(L):
    E = cube_edges(L); nv = 2 ** L; out = []
    for S in itertools.combinations(range(len(E)), nv - 1):
        parent = list(range(nv))
        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a = parent[a]
            return a
        ok = True
        for k in S:
            a, b = find(E[k][0]), find(E[k][1])
            if a == b: ok = False; break
            parent[a] = b
        if ok: out.append([E[k] for k in S])
    return out

def lip_vertices_trees(wts, tol=1e-9):
    """ALL vertices of {f : |f(x) - f(x^i)| <= wts[i]} on the cube Q_L, f(0) = 0, by enumeration of spanning trees of tight
    edges with signs (complete: the tight graph of a vertex is connected, so it contains a spanning tree).  L <= 3."""
    L = len(wts); nv = 2 ** L; E = cube_edges(L); seen = {}
    for T in spanning_trees(L):
        adj = {v: [] for v in range(nv)}
        for (a, b, i) in T: adj[a].append((b, i)); adj[b].append((a, i))
        order = []; par = {0: None}; stack = [0]
        while stack:
            v = stack.pop()
            for (w, i) in adj[v]:
                if w not in par: par[w] = (v, i); order.append(w); stack.append(w)
        for signs in itertools.product((1.0, -1.0), repeat=nv - 1):
            f = np.zeros(nv)
            for k, w in enumerate(order):
                v, i = par[w]; f[w] = f[v] + signs[k] * wts[i]
            if all(abs(f[a] - f[b]) <= wts[i] + tol for (a, b, i) in E):
                seen[tuple(np.round(f, 9))] = f
    return [seen[k] for k in sorted(seen)]

def height_functions(L):
    """all f : Q_L -> Z with f(0) = 0 and |f(x) - f(y)| = 1 on every edge (times the slope: the vertices for a uniform slope)"""
    nv = 2 ** L; order = sorted(range(nv), key=lambda x: (bin(x).count("1"), x)); out = []; f = [None] * nv
    nb = {x: [x ^ (1 << i) for i in range(L)] for x in range(nv)}
    def rec(k):
        if k == nv: out.append(list(f)); return
        x = order[k]
        if k == 0: f[x] = 0; rec(1); f[x] = None; return
        vals = None
        for y in nb[x]:
            if f[y] is not None:
                c = {f[y] - 1, f[y] + 1}
                vals = c if vals is None else vals & c
        for v in sorted(vals):
            f[x] = v; rec(k + 1)
        f[x] = None
    rec(0)
    return np.array(out, float)

def sitewise_labels(wts):
    """the 2^L additive vertices phi_sigma(x) = sum_i wts[i] * [x_i != sigma_i]"""
    L = len(wts); out = []
    for s in range(2 ** L):
        sb = bits(s, L)
        out.append([sum(wts[i] for i in range(L) if ((x >> i) & 1) != sb[i]) for x in range(2 ** L)])
    return np.array(out, float)

def is_vertex(f, wts, tol=1e-9):
    """Lipschitz and tight graph connected"""
    L = len(wts); nv = 2 ** L
    comp = list(range(nv))
    def find(a):
        while comp[a] != a:
            comp[a] = comp[comp[a]]; a = comp[a]
        return a
    for (a, b, i) in cube_edges(L):
        dlt = abs(f[a] - f[b])
        if dlt > wts[i] + tol: return False
        if dlt > wts[i] - tol: comp[find(a)] = find(b)
    return len({find(v) for v in range(nv)}) == 1

# ----------------------------------------------------------------------------- fast (vectorised) tree enumeration, L <= 3
_TREE_CACHE = {}
def _tree_data(L):
    if L in _TREE_CACHE: return _TREE_CACHE[L]
    nv = 2 ** L; data = []
    for T in spanning_trees(L):
        adj = {v: [] for v in range(nv)}
        for k, (a, b, i) in enumerate(T): adj[a].append((b, k)); adj[b].append((a, k))
        B = np.zeros((nv, nv - 1)); seen = {0}; stack = [0]
        while stack:
            v = stack.pop()
            for (w, k) in adj[v]:
                if w not in seen:
                    seen.add(w); B[w] = B[v]; B[w, k] = 1.0; stack.append(w)
        data.append((B, np.array([i for (_, _, i) in T])))
    signs = np.array(list(itertools.product((1.0, -1.0), repeat=nv - 1)))
    E = cube_edges(L)
    ea = np.array([a for (a, b, i) in E]); eb = np.array([b for (a, b, i) in E]); ei = np.array([i for (a, b, i) in E])
    _TREE_CACHE[L] = (data, signs, ea, eb, ei)
    return _TREE_CACHE[L]

def lip_vertices(wts, tol=1e-9):
    """same set as lip_vertices_trees (complete), vectorised over the sign patterns; L <= 3"""
    L = len(wts); wts = np.asarray(wts, float)
    data, signs, ea, eb, ei = _tree_data(L); seen = {}
    for (B, dirs) in data:
        F = (signs * wts[dirs][None, :]) @ B.T                       # (2^(nv-1)) x nv
        ok = (np.abs(F[:, ea] - F[:, eb]) <= wts[ei][None, :] + tol).all(axis=1)
        for f in F[ok]: seen[tuple(np.round(f, 9))] = f
    return np.array([seen[k] for k in sorted(seen)])

# ----------------------------------------------------------------------------- certified bracket for h = max_t F*(t)
def h_bracket(P, scale=1.0, tol=1e-11, coarse=0.02, fine=5e-4, halfwidth=0.02):
    """h = max_t F*(t)/scale.  Lower: the best primal value.  Upper: on every grid interval [t1,t2],
    F*(t) <= min( U(t1) t2/t1 , U(t2) (1-t1)/(1-t2) )  because F*(t)/t is nonincreasing and F*(t)/(1-t) nondecreasing
    (W_REPORT Theorem W3(c)); U = dual values.  Returns (h_lower, h_upper, t*)."""
    cache = {}
    def F(t):
        k = round(t, 12)
        if k not in cache: cache[k] = renyi_F(P, t, tol=tol)[:2]
        return cache[k]
    ts = list(np.arange(coarse, 1 - coarse / 2, coarse))
    i = int(np.argmax([F(t)[0] for t in ts]))
    tst, _ = golden_max(lambda t: F(t)[0], ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)], it=40)
    ts += list(np.arange(max(tst - halfwidth, 1e-3), min(tst + halfwidth, 1 - 1e-3), fine)) + [tst]
    ts = sorted(set(round(t, 12) for t in ts))
    lo = max(F(t)[0] for t in ts); up = max(F(ts[0])[1] / (1 - ts[0]), F(ts[-1])[1] / ts[-1])
    for t1, t2 in zip(ts[:-1], ts[1:]):
        up = max(up, min(F(t1)[1] * t2 / t1, F(t2)[1] * (1 - t1) / (1 - t2)))
    return lo / scale, up / scale, tst

def haE(pi, V, scale=1.0):
    """brackets ((h_lo,h_up,t*),(a_lo,a_up),(E_lo,E_up)) per unit `scale`"""
    P = gibbs_rows(pi, V)
    h = h_bracket(P, scale)
    a = capacity(P); E = E_threshold(P)
    return h, (a[0] / scale, a[1] / scale), (E[0] / scale, E[1] / scale)

def ustar(u, p, it=200):
    """fixed point of x = u + g(x), g(x) = ln[((1-p)e^x + p)/(p e^x + 1-p)] (one-sided slack of the Markov recursion)"""
    q = max(p, 1 - p); x = u
    for _ in range(it): x = u + math.log((q * math.exp(x) + 1 - q) / ((1 - q) * math.exp(x) + q))
    return x

# ----------------------------------------------------------------------------- active-set solver (fast and sharp for small alphabets)
def solve_active(P, kind, t=None, tol=1e-11, maxrounds=80, warm=60):
    """kind in {'renyi','E','a'}.  A few multiplicative steps, then repeatedly: restrict to the support plus the most violating
    vertices, solve the reduced convex programme by SLSQP, re-evaluate primal and dual on ALL vertices.
    Returns (lower, upper, M, Q) with lower <= value <= upper (weak duality; no trust in the inner solver is needed)."""
    nv, q = P.shape; lP = np.log(P)
    if kind == "renyi": Pt = P ** t
    def evaluate(M):
        if kind == "renyi":
            s = M @ Pt; N = float((s ** (1.0 / t)).sum()); r = Pt @ (s ** ((1.0 - t) / t))
            Q = s ** (1.0 / t) / N
            return -t * math.log(N), -math.log(float(r.min())) + (1.0 - t) * math.log(N), -r / N, Q
        if kind == "E":
            z = M @ lP; zm = z.max(); w = np.exp(z - zm); S = w.sum(); Q = w / S
            kl = float((Q * np.log(Q)).sum()) - lP @ Q
            return -(zm + math.log(S)), float(kl.max()), kl, Q
        Qm = M @ P; kl = (P * (lP - np.log(Qm)[None, :])).sum(axis=1)
        return float(M @ kl), float(kl.max()), kl, Qm
    def mult(M, score):
        if kind == "renyi": M2 = M * (-score) ** (-t / (1.0 - t))
        else: M2 = M * np.exp(score - score.max())
        return M2 / M2.sum()
    M = np.full(nv, 1.0 / nv); best = None
    for _ in range(warm):
        lo, up, score, Q = evaluate(M)
        if best is None or up - lo < best[1] - best[0]: best = (lo, up, M.copy(), Q)
        if up - lo < tol: return best
        M = mult(M, score)
    for rnd in range(maxrounds):
        lo, up, score, Q = evaluate(M)
        if up - lo < best[1] - best[0]: best = (lo, up, M.copy(), Q)
        if up - lo < tol: break
        A = np.where(M > 1e-10 * M.max())[0]
        top = np.argsort(-score)[:max(4, q)]
        A = np.unique(np.concatenate([A, top]))
        if len(A) > 400: A = np.unique(np.concatenate([np.argsort(-M)[:300], top]))
        m0 = M[A] + 1e-6; m0 /= m0.sum()
        if kind == "renyi":
            PA = Pt[A]
            fun = lambda m: float(((np.clip(m, 0, None) @ PA) ** (1.0 / t)).sum())
            jac = lambda m: (PA @ ((np.clip(m, 0, None) @ PA) ** ((1.0 - t) / t))) / t
        elif kind == "E":
            LA = lP[A]
            def fun(m):
                z = m @ LA; zm = z.max(); return float(zm + math.log(np.exp(z - zm).sum()))
            def jac(m):
                z = m @ LA; w = np.exp(z - z.max()); return LA @ (w / w.sum())
        else:
            PA = P[A]; LA = lP[A]
            def fun(m):
                m = np.clip(m, 1e-300, None); Qm = m @ PA; return -float(m @ (PA * (LA - np.log(Qm)[None, :])).sum(axis=1))
            def jac(m):
                m = np.clip(m, 1e-300, None); Qm = m @ PA; return -((PA * (LA - np.log(Qm)[None, :])).sum(axis=1) - 1.0)
        res = minimize(fun, m0, jac=jac, method="SLSQP", bounds=[(0, 1)] * len(A),
                       constraints=[{"type": "eq", "fun": lambda m: m.sum() - 1, "jac": lambda m: np.ones_like(m)}],
                       options={"ftol": 1e-16, "maxiter": 400})
        m = np.clip(res.x, 0, None); m /= m.sum()
        Mn = np.zeros(nv); Mn[A] = m
        lo2 = evaluate(Mn)[0]
        if lo2 >= lo - 1e-13: M = Mn
        else: M = mult(M, score)                      # the inner solver failed: fall back to a multiplicative step
    return best

def h_quick(P, scale=1.0, tol=1e-11, coarse=0.05):
    """h = max_t F*(t)/scale: coarse scan, golden section on the primal value, duality bracket AT t* (not a certificate over all t)."""
    cache = {}
    def F(t):
        k = round(t, 12)
        if k not in cache: cache[k] = solve_active(P, "renyi", t, tol=tol)[:2]
        return cache[k]
    ts = list(np.arange(coarse, 1 - coarse / 2, coarse))
    vals = [F(t)[0] for t in ts]; i = int(np.argmax(vals))
    nloc = sum(1 for j in range(1, len(vals) - 1) if vals[j] > vals[j - 1] and vals[j] > vals[j + 1])
    tst, _ = golden_max(lambda t: F(t)[0], ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)], it=30)
    return F(tst)[0] / scale, F(tst)[1] / scale, tst, nloc

def haE_fast(pi, V, scale=1.0):
    P = gibbs_rows(pi, V)
    h = h_quick(P, scale)
    a = solve_active(P, "a"); E = solve_active(P, "E")
    return h, (a[0] / scale, a[1] / scale), (E[0] / scale, E[1] / scale)

# ----------------------------------------------------------------------------- the default fast routines (multiplicative solvers)
def h_mult(P, scale=1.0, tol=1e-10, coarse=0.05, itmax=100000):
    """h = max_t F*(t)/scale: coarse scan, golden section on the primal value, duality bracket AT t*.
    Returns (lower, upper, t*, number of interior local maxima of the coarse scan)."""
    cache = {}
    def F(t):
        k = round(t, 12)
        if k not in cache: cache[k] = renyi_F(P, t, tol=tol, itmax=itmax)[:2]
        return cache[k]
    ts = list(np.arange(coarse, 1 - coarse / 2, coarse))
    vals = [F(t)[0] for t in ts]; i = int(np.argmax(vals))
    nloc = sum(1 for j in range(1, len(vals) - 1) if vals[j] > vals[j - 1] and vals[j] > vals[j + 1])
    tst, _ = golden_max(lambda t: F(t)[0], ts[max(i - 1, 0)], ts[min(i + 1, len(ts) - 1)], it=30)
    return F(tst)[0] / scale, F(tst)[1] / scale, tst, nloc

def haE_mult(pi, V, scale=1.0, tol=1e-9, itmax=60000):
    P = gibbs_rows(pi, V)
    h = h_mult(P, scale)
    a = capacity(P, tol=tol, itmax=itmax); E = E_threshold(P, tol=tol, itmax=itmax)
    return h, (a[0] / scale, a[1] / scale), (E[0] / scale, E[1] / scale)
