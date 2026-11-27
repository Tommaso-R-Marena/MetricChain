"""
r10lib.py -- workstream R10 (science division): own library, written from the DEFINITIONS in
docs/workstreams/Y_REPORT.md (theory division, commit 658b77f) BEFORE opening any code of
experiments/workstreams/Y/.  Nothing here is copied from the theory division's code.

Conventions
-----------
* A finite space X with N points, a law pi (vector of length N), a family of "labels"
  phi (rows of an array, shape (m, N)), Gibbs laws  pi_phi = pi * exp(-phi) / E_pi exp(-phi).
* Site function (Y_REPORT section 1):
      F*(t) = max_M G_t(M),   G_t(M) = -t ln sum_x ( sum_phi M(phi) pi_phi(x)^t )^(1/t)
            = min_Q max_phi  -ln sum_x pi_phi(x)^t Q(x)^(1-t)             (0 < t < 1)
      E = min_Q max_phi KL(Q || pi_phi) = max_M [ sum_phi M ln Z(phi) - ln Z(sum_phi M phi) ]
      a = max_M I(M; W) = min_Q max_phi KL(pi_phi || Q)
  Every routine returns a duality bracket [lower, upper]: `lower` is the value of the max-side
  at the returned M (valid lower bound whatever M is), `upper` is the value of the min-side
  at the centre Q_M built from M, maximised over ALL supplied labels (valid upper bound for
  the supplied label family).  If the label family contains all vertices of the Lipschitz
  polytope, `upper` is an upper bound for the whole class (the maximum over the class is
  attained at a vertex: e^{-phi} ranges over a convex cone and the functional is concave in
  the unnormalised weights; see R10_REPORT section 2).
* Binary configurations: index k in [0, 2^n), bit i of k is the letter x_i in {0,1} of site
  i (i = 0..n-1); spin s_i = 1 - 2 x_i.
"""
import itertools
import numpy as np

# ----------------------------------------------------------------------------- basics


def bits(n):
    k = np.arange(1 << n)
    return ((k[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)


def spins(n):
    return (1 - 2 * bits(n)).astype(np.int8)


def binary_chain_law(n, p):
    """Stationary binary symmetric Markov chain with flip probability p on {0,1}^n."""
    x = bits(n)
    flips = (x[:, 1:] != x[:, :-1]).sum(axis=1) if n > 1 else np.zeros(1 << n, dtype=int)
    return 0.5 * p ** flips * (1 - p) ** (n - 1 - flips)


def gibbs(pi, phi):
    """Gibbs laws of the rows of phi w.r.t. pi.  Returns (W, lnZ) with W[m, x]."""
    phi = np.atleast_2d(phi)
    a = np.log(pi)[None, :] - phi
    mx = a.max(axis=1, keepdims=True)
    w = np.exp(a - mx)
    z = w.sum(axis=1, keepdims=True)
    return w / z, (np.log(z) + mx)[:, 0]


# ----------------------------------------------------------------------------- vertices


def hom_vertices(n):
    """All integer height functions f on the cube Q_n with f(0)=0 and |f(x)-f(x^i)|=1 on
    every edge.  For the Hamming envelope with one slope these are exactly the vertices of
    the Lipschitz polytope modulo constants (in units of the slope): a vertex has a connected
    graph of tight edges, hence f(x)-f(y) = dist(x,y) mod 2 for all x,y, hence every edge
    is tight.  Returns an int8 array of shape (count, 2^n)."""
    F = np.array([[0, 1], [0, -1]], dtype=np.int8)  # n = 1
    for m in range(1, n):  # build Q_{m+1} from Q_m
        N = 1 << m
        edges = [(v, v ^ (1 << i)) for v in range(N) for i in range(m) if v < v ^ (1 << i)]
        masks = np.arange(1 << N, dtype=np.int64) if N <= 16 else None
        if masks is None:
            raise ValueError("hom_vertices: n too large for this construction")
        B = ((masks[:, None] >> np.arange(N)[None, :]) & 1).astype(bool)  # s = +1 where bit set
        out = []
        for f0 in F:
            bad = np.zeros(1 << N, dtype=bool)
            for (v, w) in edges:
                hi, lo = (v, w) if f0[v] > f0[w] else (w, v)
                # forbidden: s(hi) = +1 and s(lo) = -1  (then f1(hi)-f1(lo) = 3)
                bad |= B[:, hi] & ~B[:, lo]
            good = B[~bad]
            s = np.where(good, 1, -1).astype(np.int8)
            f1 = f0[None, :] + s
            out.append(np.concatenate([np.broadcast_to(f0, f1.shape), f1], axis=1))
        F = np.concatenate(out, axis=0).astype(np.int8)
    return F


def sitewise_labels(n):
    """The 2^n additive vertices  phi_sigma(x) = -(1/2) sum_i sigma_i s_i  (units of the slope),
    shifted so that phi(0) = 0 is NOT enforced (constants are irrelevant)."""
    s = spins(n).astype(float)
    return -0.5 * (s @ s.T)  # row sigma, column x


def spanning_trees(nv, edges):
    """All spanning trees (as tuples of edge indices) of a graph on nv vertices."""
    trees = []
    for comb in itertools.combinations(range(len(edges)), nv - 1):
        parent = list(range(nv))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        ok = True
        for e in comb:
            a, b = find(edges[e][0]), find(edges[e][1])
            if a == b:
                ok = False
                break
            parent[a] = b
        if ok:
            trees.append(comb)
    return trees


def lipschitz_vertices(nv, edges, dfwd, dbwd, tol=1e-9):
    """Vertices (modulo constants, f[0]=0) of { f : f(a)-f(b) <= dfwd[e], f(b)-f(a) <= dbwd[e]
    for every edge e=(a,b) }.  Enumeration over spanning trees of tight edges with both
    orientations of tightness; complete (every vertex has a spanning tree of tight edges).
    Only for small graphs."""
    edges = list(edges)
    dfwd = np.asarray(dfwd, float)
    dbwd = np.asarray(dbwd, float)
    ea = np.array([e[0] for e in edges])
    eb = np.array([e[1] for e in edges])
    found = {}
    for tree in spanning_trees(nv, edges):
        # adjacency of the tree
        adj = [[] for _ in range(nv)]
        for e in tree:
            adj[edges[e][0]].append((edges[e][1], e, +1))  # going a -> b
            adj[edges[e][1]].append((edges[e][0], e, -1))  # going b -> a
        order = []
        seen = [False] * nv
        seen[0] = True
        stack = [0]
        while stack:
            v = stack.pop()
            for (w, e, dirn) in adj[v]:
                if not seen[w]:
                    seen[w] = True
                    order.append((v, w, e, dirn))
                    stack.append(w)
        for signs in itertools.product((0, 1), repeat=nv - 1):
            f = np.zeros(nv)
            for (v, w, e, dirn), sg in zip(order, signs):
                # tight in one of the two ways: f(a)-f(b) = dfwd  or  f(b)-f(a) = dbwd
                a_minus_b = dfwd[e] if sg == 0 else -dbwd[e]
                if dirn == +1:   # v = a, w = b
                    f[w] = f[v] - a_minus_b
                else:            # v = b, w = a
                    f[w] = f[v] + a_minus_b
            diff = f[ea] - f[eb]
            if np.all(diff <= dfwd + tol) and np.all(-diff <= dbwd + tol):
                key = tuple(np.round(f, 7))
                found[key] = f
    return np.array(list(found.values()))


def cube_graph(L):
    """Edges of Q_L as (a, b, site) with a < b (a has letter 0 at `site`, b has letter 1)."""
    return [(v, v | (1 << i), i) for v in range(1 << L) for i in range(L) if not (v >> i) & 1]


def cube_vertices_weighted(slopes):
    """Vertices of the Lipschitz polytope of the cube Q_L with symmetric site slopes."""
    L = len(slopes)
    E = cube_graph(L)
    w = [slopes[i] for (_, _, i) in E]
    return lipschitz_vertices(1 << L, [(a, b) for (a, b, _) in E], w, w)


# ----------------------------------------------------------------------------- solvers


def _dual_upper_t(W, Q, t):
    """max_phi (1-t) D_t(pi_phi || Q) = max_phi -ln sum_x W^t Q^(1-t)."""
    c = (W ** t) @ (Q ** (1 - t))
    return -np.log(c.min()), c


def renyi_bracket(W, t, M=None, iters=20000, tol=1e-11, Wt=None):
    """F*(t) for the label family W (rows = Gibbs laws).  Arimoto's iteration
        M <- M * c^(-t/(1-t)),   c_phi = sum_x W_phi(x)^t Q_M(x)^(1-t),
    with a duality bracket.  Returns dict(lower, upper, M, Q)."""
    m = W.shape[0]
    if Wt is None:
        Wt = W ** t
    if M is None:
        M = np.full(m, 1.0 / m)
    best = None
    expo = t / (1 - t)
    for it in range(iters):
        mix = M @ Wt                      # sum_phi M W^t
        r = mix ** (1.0 / t)
        S = r.sum()
        Q = r / S
        lower = -t * np.log(S)
        c = Wt @ (Q ** (1 - t))
        upper = -np.log(c.min())
        if best is None or upper - lower < best["upper"] - best["lower"]:
            best = dict(lower=lower, upper=upper, M=M.copy(), Q=Q.copy(), it=it)
        if upper - lower < tol:
            break
        M = M * c ** (-expo)
        M /= M.sum()
    return best


def capacity_bracket(W, M=None, iters=200000, tol=1e-11):
    """a = max_M I(M;W) = min_Q max_phi KL(pi_phi || Q).  Blahut-Arimoto with bracket."""
    m = W.shape[0]
    if M is None:
        M = np.full(m, 1.0 / m)
    lw = np.log(W)
    best = None
    for it in range(iters):
        Q = M @ W
        kl = (W * (lw - np.log(Q)[None, :])).sum(axis=1)
        lower = float(M @ kl)
        upper = float(kl.max())
        if best is None or upper - lower < best["upper"] - best["lower"]:
            best = dict(lower=lower, upper=upper, M=M.copy(), Q=Q.copy(), it=it)
        if upper - lower < tol:
            break
        M = M * np.exp(kl - kl.max())
        M /= M.sum()
    return best


def threshold_bracket(W, M=None, iters=200000, tol=1e-11, eta=1.0):
    """E = min_Q max_phi KL(Q || pi_phi) = max_M -ln sum_x prod_phi pi_phi(x)^M(phi).
    Exponentiated gradient on M with step halving; duality bracket."""
    m = W.shape[0]
    lw = np.log(W)
    if M is None:
        M = np.full(m, 1.0 / m)

    def evalM(M):
        g = M @ lw
        mx = g.max()
        r = np.exp(g - mx)
        S = r.sum()
        Q = r / S
        lower = -(np.log(S) + mx)
        kl = float(Q @ np.log(Q)) - lw @ Q
        return lower, kl, Q

    lower, kl, Q = evalM(M)
    best = dict(lower=lower, upper=float(kl.max()), M=M.copy(), Q=Q.copy(), it=0)
    for it in range(1, iters):
        if best["upper"] - best["lower"] < tol:
            break
        step = eta
        while True:
            M2 = M * np.exp(step * (kl - kl.max()))
            M2 /= M2.sum()
            lower2, kl2, Q2 = evalM(M2)
            if lower2 >= lower - 1e-15 or step < 1e-8:
                break
            step *= 0.5
        M, lower, kl, Q = M2, lower2, kl2, Q2
        if kl.max() - lower < best["upper"] - best["lower"]:
            best = dict(lower=lower, upper=float(kl.max()), M=M.copy(), Q=Q.copy(), it=it)
    return best


def golden_max(fun, lo, hi, tol=1e-7):
    """Golden-section maximisation of a unimodal function; returns (t, value)."""
    g = (np.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = fun(c), fun(d)
    while b - a > tol:
        if fc < fd:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = fun(d)
        else:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = fun(c)
    t = (a + b) / 2
    return t, fun(t)


# ----------------------------------------------------------------------------- closed forms


def cube_F(t, u):
    h = u / 2
    return t * np.log(np.cosh(h)) - np.log(np.cosh(t * h))


def cube_exponents(u):
    """(h, t*, a, E) of the uniform cube with Hamming slope u (closed forms)."""
    hh = u / 2
    E = np.log(np.cosh(hh))
    a = hh * np.tanh(hh) - E
    # F'(t) = ln cosh(hh) - hh tanh(t hh) = 0
    ts = np.arctanh(E / hh) / hh
    return cube_F(ts, u), ts, a, E


def E_F(p, u):
    h = u / 2
    return np.log((1 - p) * np.cosh(h) + np.sqrt((1 - p) ** 2 * np.sinh(h) ** 2 + p ** 2))
