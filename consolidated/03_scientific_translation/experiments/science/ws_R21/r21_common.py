"""R21 common tools (own code, written before opening any script of the reviewed branch).

Planar bar frameworks: squared-edge-length map, rigidity matrix, rank, brute-force
connectivity of the generic rigidity matroid, stress-matrix test of generic global rigidity,
a batched Levenberg-Marquardt realisation solver, and exact realisability tests
(Gram/EDM test for complete graphs, angle-sum test for wheels).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
import itertools
import time
import numpy as np


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def complete(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def wheel(n_rim):
    """hub 0, rim 1..n_rim"""
    E = [(0, i) for i in range(1, n_rim + 1)]
    E += [(i, i + 1) for i in range(1, n_rim)] + [(1, n_rim)]
    return sorted(E)


def graph_table():
    """name -> (N, edge list). Planar examples used in R21."""
    G = {}
    G["K3"] = (3, complete(3))
    G["K4"] = (4, complete(4))
    G["K4-e"] = (4, [e for e in complete(4) if e != (0, 1)])
    G["K5"] = (5, complete(5))
    G["K5-e"] = (5, [e for e in complete(5) if e != (3, 4)])
    G["W5"] = (5, wheel(4))
    G["K4+deg2"] = (5, complete(4) + [(0, 4), (1, 4)])
    G["K6"] = (6, complete(6))
    G["W6"] = (6, wheel(5))
    k33 = [(i, j) for i in range(3) for j in range(3, 6)]
    G["K33"] = (6, k33)
    G["K33+e"] = (6, sorted(k33 + [(0, 1)]))
    # two K4 sharing the edge (0,1): vertices {0,1,2,3} and {0,1,4,5}
    two = sorted(set(complete(4)) | {(0, 1), (0, 4), (0, 5), (1, 4), (1, 5), (4, 5)})
    G["2K4_edge"] = (6, two)
    G["2K4_2sum"] = (6, [e for e in two if e != (0, 1)])
    # triangular prism
    G["prism"] = (6, sorted([(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5), (0, 3), (1, 4), (2, 5)]))
    return G


def sqlen(P, E):
    """P: (..., N, d) -> (..., m) squared edge lengths."""
    I = np.array([e[0] for e in E])
    J = np.array([e[1] for e in E])
    D = P[..., I, :] - P[..., J, :]
    return np.sum(D * D, axis=-1)


def rigidity_matrix(P, E):
    """P: (N, d) -> (m, N*d); the Jacobian of sqlen is twice this."""
    N, d = P.shape
    R = np.zeros((len(E), N * d))
    for k, (u, v) in enumerate(E):
        R[k, u * d:(u + 1) * d] = P[u] - P[v]
        R[k, v * d:(v + 1) * d] = P[v] - P[u]
    return R


def num_rank(M, tol=1e-9):
    if M.size == 0:
        return 0
    s = np.linalg.svd(M, compute_uv=False)
    if s.size == 0 or s[0] == 0:
        return 0
    return int(np.sum(s > tol * s[0]))


def matroid_separators(P, E, tol=1e-9):
    """Brute force: all J (proper, non-empty, containing edge 0 or not; reported once per
    complementary pair) with r(J) + r(E \\ J) = r(E).  Returns (rank, list of separators)."""
    R = rigidity_matrix(P, E)
    m = len(E)
    r_all = num_rank(R, tol)
    seps = []
    cache = {}

    def rk(mask):
        if mask not in cache:
            rows = [i for i in range(m) if (mask >> i) & 1]
            cache[mask] = num_rank(R[rows], tol)
        return cache[mask]

    full = (1 << m) - 1
    for mask in range(1, 1 << (m - 1)):  # subsets not containing the last edge: one per complementary pair
        if rk(mask) + rk(full ^ mask) == r_all:
            seps.append(mask)
    return r_all, seps


def stress_rank(P, E, rng, tol=1e-8):
    """Rank of a random equilibrium stress matrix at P (0 if no stress).  For generic P:
    rank == N - d - 1 iff the graph is generically globally rigid (Connelly 2005 / Gortler-Healy-Thurston 2010)."""
    N, d = P.shape
    R = rigidity_matrix(P, E)
    U, s, Vt = np.linalg.svd(R.T, full_matrices=True)  # R^T w = 0
    r = int(np.sum(s > tol * s[0]))
    null = Vt[r:].T  # (m, m - r)
    if null.shape[1] == 0:
        return 0, 0
    w = null @ rng.standard_normal(null.shape[1])
    Om = np.zeros((N, N))
    for k, (u, v) in enumerate(E):
        Om[u, v] -= w[k]
        Om[v, u] -= w[k]
        Om[u, u] += w[k]
        Om[v, v] += w[k]
    return num_rank(Om, 1e-7), null.shape[1]


def vertex_connectivity(N, E):
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(range(N))
    g.add_edges_from(E)
    return nx.node_connectivity(g)


def redundantly_rigid(P, E, tol=1e-9):
    N, d = P.shape
    full = d * N - d * (d + 1) // 2
    R = rigidity_matrix(P, E)
    if num_rank(R, tol) < full:
        return False
    for k in range(len(E)):
        if num_rank(np.delete(R, k, axis=0), tol) < full:
            return False
    return True


# ---------------------------------------------------------------------------------------
# gauge-fixed planar parametrisation: p_0 = (0,0), p_1 = (z_0, 0), p_k = (z_{2k-3}, z_{2k-2})
# ---------------------------------------------------------------------------------------

def embed(Z, N):
    B = Z.shape[0]
    P = np.zeros((B, N, 2))
    P[:, 1, 0] = Z[:, 0]
    P[:, 2:, :] = Z[:, 1:].reshape(B, N - 2, 2)
    return P


def gauge(P):
    """P: (N,2) -> z in R^{2N-3} (translate p_0 to 0, rotate p_1 onto the x-axis)."""
    Q = P - P[0]
    a = np.arctan2(Q[1, 1], Q[1, 0])
    c, s = np.cos(-a), np.sin(-a)
    Rot = np.array([[c, -s], [s, c]])
    Q = Q @ Rot.T
    return np.concatenate([[Q[1, 0]], Q[2:].ravel()])


class Realiser:
    """Batched Levenberg-Marquardt for  min_p || sqlen(p) - t ||^2  in the gauge-fixed chart."""

    def __init__(self, N, E):
        self.N = N
        self.E = E
        self.m = len(E)
        self.n = 2 * N - 3
        self.I = np.array([e[0] for e in E])
        self.J = np.array([e[1] for e in E])
        # column index of (vertex, coord) in z, or -1
        col = -np.ones((N, 2), dtype=int)
        col[1, 0] = 0
        for k in range(2, N):
            col[k, 0] = 2 * k - 3
            col[k, 1] = 2 * k - 2
        self.col = col

    def res_jac(self, Z, T, want_jac=True):
        B = Z.shape[0]
        P = embed(Z, self.N)
        D = P[:, self.I, :] - P[:, self.J, :]          # (B, m, 2)
        r = np.sum(D * D, axis=-1) - T                  # (B, m)
        if not want_jac:
            return r, None
        Jc = np.zeros((B, self.m, self.n))
        ar = np.arange(self.m)
        for c in range(2):
            ci = self.col[self.I, c]
            ok = ci >= 0
            Jc[:, ar[ok], ci[ok]] += 2 * D[:, ok, c]
            cj = self.col[self.J, c]
            ok = cj >= 0
            Jc[:, ar[ok], cj[ok]] -= 2 * D[:, ok, c]
        return r, Jc

    def solve(self, T, Z0, iters=120, lam0=1e-2):
        """T: (B, m); Z0: (B, n).  Returns (Z, residual 2-norm)."""
        Z = Z0.copy()
        B = Z.shape[0]
        lam = np.full(B, lam0)
        r, Jc = self.res_jac(Z, T)
        cost = np.sum(r * r, axis=1)
        eye = np.eye(self.n)
        for _ in range(iters):
            g = np.einsum('bmn,bm->bn', Jc, r)
            H = np.einsum('bmn,bmk->bnk', Jc, Jc)
            dg = np.einsum('bnn->bn', H)
            A = H + (lam[:, None] * (dg + 1e-12))[:, :, None] * eye[None]
            try:
                step = np.linalg.solve(A, -g[:, :, None])[:, :, 0]
            except np.linalg.LinAlgError:
                step = -g / (dg + 1e-12) * 0.1
            Zn = Z + step
            rn, _ = self.res_jac(Zn, T, want_jac=False)
            cn = np.sum(rn * rn, axis=1)
            acc = np.isfinite(cn) & (cn < cost)
            if acc.any():
                Z[acc] = Zn[acc]
                cost[acc] = cn[acc]
            lam = np.where(acc, lam * 0.3, lam * 5.0)
            lam = np.clip(lam, 1e-14, 1e14)
            r, Jc = self.res_jac(Z, T)
        return Z, np.sqrt(cost)

    def multistart(self, T, starts, rng, iters=120, scale=1.5, chunk=40000):
        """For every target row: best residual 2-norm over `starts` random starts, the best z,
        and the number of starts that reached a residual below 1e-9."""
        B = T.shape[0]
        best = np.full(B, np.inf)
        bestZ = np.zeros((B, self.n))
        hits = np.zeros(B, dtype=int)
        for s in range(starts):
            for a in range(0, B, chunk):
                b = min(B, a + chunk)
                Z0 = scale * rng.standard_normal((b - a, self.n))
                Z, res = self.solve(T[a:b], Z0, iters=iters)
                better = res < best[a:b]
                idx = np.arange(a, b)[better]
                best[idx] = res[better]
                bestZ[idx] = Z[better]
                hits[a:b] += (res < 1e-9)
        return best, bestZ, hits


# ---------------------------------------------------------------------------------------
# exact realisability tests
# ---------------------------------------------------------------------------------------

def gram_defect(T, n, E, d=2):
    """T: (B, m) squared lengths on the COMPLETE graph on n vertices with edge list E.
    Returns the defect  sum of |eigenvalues| of the centred Gram matrix beyond the d largest
    (+ negative parts of the d largest): zero iff realisable in R^d."""
    B = T.shape[0]
    D = np.zeros((B, n, n))
    for k, (u, v) in enumerate(E):
        D[:, u, v] = T[:, k]
        D[:, v, u] = T[:, k]
    Jm = np.eye(n) - np.ones((n, n)) / n
    G = -0.5 * Jm @ D @ Jm
    ev = np.linalg.eigvalsh(G)[:, ::-1]                 # descending
    defect = np.sum(np.abs(ev[:, d:]), axis=1) + np.sum(np.maximum(0.0, -ev[:, :d]), axis=1)
    return defect


def wheel_defect(T, E, n_rim):
    """Exact test for the wheel with hub 0 and rim 1..n_rim (edge list E as produced by wheel()).
    Returns (defect, feasible): defect = min over signs of |sum s_k theta_k mod 2 pi| when all
    hub triangles satisfy the triangle inequality (feasible), else the largest |cos| overshoot."""
    B = T.shape[0]
    idx = {e: k for k, e in enumerate(E)}
    rim = [(i, i + 1) for i in range(1, n_rim)] + [(1, n_rim)]
    cosv = np.zeros((B, n_rim))
    for q, (i, j) in enumerate(rim):
        ri2 = T[:, idx[(0, i)]]
        rj2 = T[:, idx[(0, j)]]
        dij2 = T[:, idx[(i, j)]]
        cosv[:, q] = (ri2 + rj2 - dij2) / (2 * np.sqrt(ri2 * rj2))
    over = np.max(np.abs(cosv), axis=1) - 1.0
    feasible = over <= 0
    th = np.arccos(np.clip(cosv, -1, 1))
    best = np.full(B, np.inf)
    for signs in itertools.product([1.0, -1.0], repeat=n_rim - 1):
        s = np.array((1.0,) + signs)
        tot = th @ s
        w = np.abs((tot + np.pi) % (2 * np.pi) - np.pi)
        best = np.minimum(best, w)
    defect = np.where(feasible, best, 1.0 + over)
    return defect, feasible


def all_colourings(K, m):
    """All maps [m] -> [K] as an array (K^m, m), lexicographic."""
    return np.array(list(itertools.product(range(K), repeat=m)), dtype=np.int8)


def splice_targets(Tc, col):
    """Tc: (K, m) squared lengths of the conformers; col: (B, m) colourings -> (B, m) targets."""
    return Tc[col, np.arange(Tc.shape[1])[None, :]]


def nonconstant(col):
    return ~np.all(col == col[:, :1], axis=1)


# ---------------------------------------------------------------------------------------
# exact constructive realisability test (second, non-iterative method)
# ---------------------------------------------------------------------------------------

CONSTRUCTION = {
    # name: (base edge, [(vertex, parent, parent), ...]); every construction edge must be an edge of the graph
    "K4": ((0, 1), [(2, 0, 1), (3, 0, 1)]),
    "K4-e": ((2, 3), [(0, 2, 3), (1, 2, 3)]),
    "K5": ((0, 1), [(2, 0, 1), (3, 0, 1), (4, 0, 1)]),
    "K5-e": ((0, 1), [(2, 0, 1), (3, 0, 1), (4, 0, 1)]),
    "W5": ((0, 1), [(2, 0, 1), (3, 0, 2), (4, 0, 3)]),
    "W6": ((0, 1), [(2, 0, 1), (3, 0, 2), (4, 0, 3), (5, 0, 4)]),
    "K6": ((0, 1), [(2, 0, 1), (3, 0, 1), (4, 0, 1), (5, 0, 1)]),
    "K33+e": ((0, 1), [(3, 0, 1), (4, 0, 1), (5, 0, 1), (2, 3, 4)]),
    "K4+deg2": ((0, 1), [(2, 0, 1), (3, 0, 1), (4, 0, 1)]),
    "2K4_edge": ((0, 1), [(2, 0, 1), (3, 0, 1), (4, 0, 1), (5, 0, 1)]),
    "2K4_2sum": ((2, 3), [(0, 2, 3), (1, 2, 3), (4, 0, 1), (5, 0, 1)]),
}


class Constructor:
    """Exact realisability of a vector of squared edge lengths for a graph that has a spanning
    subgraph built from one edge by adding vertices of degree two (ruler-and-compass order).
    Every realisation of the graph restricts to a realisation of that subgraph, and those are
    enumerated completely: 2^(N-3) flip patterns modulo a global reflection.  The vector is
    realisable iff for some pattern all circle pairs meet and the remaining ('check') edges
    have the prescribed lengths.  defect = min over feasible patterns of max |check residual|
    (np.inf when no pattern is feasible)."""

    def __init__(self, name, N, E):
        self.N, self.E = N, E
        self.idx = {e: k for k, e in enumerate(E)}
        self.base, self.steps = CONSTRUCTION[name]
        used = {tuple(sorted(self.base))}
        for (v, a, b) in self.steps:
            used.add(tuple(sorted((v, a))))
            used.add(tuple(sorted((v, b))))
        assert used <= set(E), "construction uses a non-edge"
        placed = set(self.base) | {v for v, _, _ in self.steps}
        assert placed == set(range(N))
        self.check = [e for e in E if e not in used]

    def realisations(self, T):
        """T: (B, m).  Yields (P (B,N,2), feasible (B,)) for every flip pattern."""
        B = T.shape[0]
        t = lambda u, v: T[:, self.idx[tuple(sorted((u, v)))]]
        nflip = len(self.steps) - 1
        for bits in range(1 << max(nflip, 0)):
            P = np.zeros((B, self.N, 2))
            feas = np.ones(B, dtype=bool)
            a0, b0 = self.base
            P[:, b0, 0] = np.sqrt(t(a0, b0))
            for q, (v, a, b) in enumerate(self.steps):
                sgn = 1.0 if q == 0 else (1.0 if (bits >> (q - 1)) & 1 == 0 else -1.0)
                dvec = P[:, b] - P[:, a]
                D2 = np.sum(dvec * dvec, axis=1)
                D = np.sqrt(D2)
                ra2, rb2 = t(a, v), t(b, v)
                with np.errstate(divide='ignore', invalid='ignore'):
                    al = (ra2 - rb2 + D2) / (2 * D)
                    h2 = ra2 - al * al
                    ok = (h2 >= 0) & (D > 0)
                    h = np.sqrt(np.where(ok, h2, 0.0))
                    ux = dvec / D[:, None]
                perp = np.stack([-ux[:, 1], ux[:, 0]], axis=1)
                P[:, v] = P[:, a] + al[:, None] * ux + sgn * h[:, None] * perp
                feas &= ok
            yield P, feas

    def defect(self, T):
        B = T.shape[0]
        best = np.full(B, np.inf)
        bestP = np.zeros((B, self.N, 2))
        ci = [self.idx[e] for e in self.check]
        for P, feas in self.realisations(T):
            L = sqlen(P, self.check) if self.check else np.zeros((B, 0))
            dev = np.max(np.abs(L - T[:, ci]), axis=1) if self.check else np.zeros(B)
            dev = np.where(feas & np.isfinite(dev), dev, np.inf)
            better = dev < best
            best[better] = dev[better]
            bestP[better] = P[better]
        return best, bestP


# ---------------------------------------------------------------------------------------
# generic batched Levenberg-Marquardt (residual function supplied)
# ---------------------------------------------------------------------------------------

def batched_lm(fun, Z0, iters=200, lam0=1e-2):
    """fun(Z, want_jac) -> (r (B,q), J (B,q,n) or None).  Minimises sum r^2 per row."""
    Z = Z0.copy()
    B, n = Z.shape
    lam = np.full(B, lam0)
    r, Jc = fun(Z, True)
    cost = np.sum(r * r, axis=1)
    eye = np.eye(n)
    for _ in range(iters):
        g = np.einsum('bmn,bm->bn', Jc, r)
        H = np.einsum('bmn,bmk->bnk', Jc, Jc)
        dg = np.einsum('bnn->bn', H)
        A = H + (lam[:, None] * (dg + 1e-12))[:, :, None] * eye[None]
        try:
            step = np.linalg.solve(A, -g[:, :, None])[:, :, 0]
        except np.linalg.LinAlgError:
            step = -g / (dg + 1e-12) * 0.1
        Zn = Z + step
        rn, _ = fun(Zn, False)
        cn = np.sum(rn * rn, axis=1)
        acc = np.isfinite(cn) & (cn < cost)
        if acc.any():
            Z[acc] = Zn[acc]
            cost[acc] = cn[acc]
        lam = np.clip(np.where(acc, lam * 0.3, lam * 5.0), 1e-14, 1e14)
        r, Jc = fun(Z, True)
    g = np.einsum('bmn,bm->bn', Jc, r)
    return Z, cost, np.linalg.norm(g, axis=1)
