"""
kcore.py — small exact toolkit for workstream K (certified kinetics).

Finite product spaces X = prod_i {0..k_i-1}, move graphs, energies, envelopes,
minimax (bottleneck) barriers, McShane envelopes, reversible single-site dynamics,
exact spectral quantities.  Everything is brute force and exact up to floating point;
sizes are limited to a few thousand states.

Conventions
-----------
* A state is an integer index 0..N-1 in mixed radix; `S.cfg[idx]` is its tuple of site states.
* Move graph: by default *unrestricted single-site moves* (x ~ y iff they differ in exactly
  one site).  `site_graph="cycle"` restricts each site to moves s -> s±1 mod k (torsion voxels).
* Barrier B(a,b) = min over paths a..b of the max over ALL vertices of the path (endpoints
  included) of the energy.  Hence B(a,b) >= max(E(a),E(b)).
* Envelope d(x,y) is the largest allowed value of g(x) - g(y)  (theory report §1).
"""
from __future__ import annotations
import heapq
import itertools
import numpy as np


class Space:
    """Product space with a single-site move graph."""

    def __init__(self, ks, site_graph="complete"):
        self.ks = list(ks)
        self.n = len(self.ks)
        self.N = int(np.prod(self.ks))
        self.radix = np.ones(self.n, dtype=np.int64)
        for i in range(self.n - 2, -1, -1):
            self.radix[i] = self.radix[i + 1] * self.ks[i + 1]
        self.cfg = np.array(list(itertools.product(*[range(k) for k in self.ks])), dtype=np.int64)
        assert self.cfg.shape == (self.N, self.n)
        self.site_graph = site_graph
        # neighbour lists: nbrs[idx] = list of (neighbour idx, site)
        nb, ns = [], []
        for idx in range(self.N):
            l, ls = [], []
            x = self.cfg[idx]
            for i in range(self.n):
                k = self.ks[i]
                if site_graph == "complete":
                    targets = [s for s in range(k) if s != x[i]]
                elif site_graph == "cycle":
                    targets = sorted({(x[i] + 1) % k, (x[i] - 1) % k} - {x[i]})
                elif site_graph == "path":
                    targets = [s for s in (x[i] - 1, x[i] + 1) if 0 <= s < k]
                else:
                    raise ValueError(site_graph)
                for s in targets:
                    l.append(idx + (s - x[i]) * self.radix[i])
                    ls.append(i)
            nb.append(np.array(l, dtype=np.int64))
            ns.append(np.array(ls, dtype=np.int64))
        self.nbrs = nb
        self.nbr_site = ns

    def index(self, x):
        return int(np.dot(np.asarray(x, dtype=np.int64), self.radix))

    def edges(self):
        """All undirected edges (u<v) as an array of shape (M,2)."""
        out = []
        for u in range(self.N):
            for v in self.nbrs[u]:
                if u < v:
                    out.append((u, int(v)))
        return np.array(out, dtype=np.int64)

    # ---- envelopes -------------------------------------------------------
    def hamming_env(self, c):
        """Weighted Hamming envelope d(x,y) = sum_i c_i [x_i != y_i] as an N x N matrix."""
        c = np.asarray(c, dtype=float)
        D = np.zeros((self.N, self.N))
        for i in range(self.n):
            col = self.cfg[:, i]
            D += c[i] * (col[:, None] != col[None, :])
        return D

    def site_env(self, deltas):
        """Site-additive (possibly asymmetric) envelope d(x,y) = sum_i delta_i[x_i, y_i].
        Each delta_i must be a k_i x k_i matrix with zero diagonal satisfying the triangle inequality."""
        D = np.zeros((self.N, self.N))
        for i in range(self.n):
            col = self.cfg[:, i]
            D += np.asarray(deltas[i])[col[:, None], col[None, :]]
        return D


# ---------------------------------------------------------------------------
# energies
# ---------------------------------------------------------------------------
def pairwise_energy(S: Space, h, J):
    """E(x) = sum_i h[i][x_i] + sum_{i<j} J[(i,j)][x_i, x_j]."""
    E = np.zeros(S.N)
    for i in range(S.n):
        E += np.asarray(h[i])[S.cfg[:, i]]
    for (i, j), M in J.items():
        E += np.asarray(M)[S.cfg[:, i], S.cfg[:, j]]
    return E


def random_pairwise(S: Space, rng, graph="complete", scale_h=1.0, scale_J=1.0, integer=False):
    h = []
    for i in range(S.n):
        v = rng.normal(0, scale_h, S.ks[i])
        h.append(np.round(v * 4) / 4 if integer else v)
    J = {}
    for i in range(S.n):
        for j in range(i + 1, S.n):
            if graph == "complete" or (graph == "chain" and j == i + 1) or \
               (graph == "chain+" and (j == i + 1 or rng.random() < 0.25)):
                M = rng.normal(0, scale_J, (S.ks[i], S.ks[j]))
                J[(i, j)] = np.round(M * 4) / 4 if integer else M
    return h, J


def curie_weiss_energy(S: Space, Jc=1.0, hfield=0.0):
    """Binary sites, spins sigma=2x-1, E = -(Jc/(2n)) (sum sigma)^2 - hfield * sum sigma."""
    assert all(k == 2 for k in S.ks)
    m = (2 * S.cfg - 1).sum(axis=1)
    return -(Jc / (2.0 * S.n)) * m ** 2 - hfield * m


def ising_chain_energy(S: Space, Jc=1.0, hfield=0.0, periodic=False):
    assert all(k == 2 for k in S.ks)
    s = 2 * S.cfg - 1
    E = -hfield * s.sum(axis=1).astype(float)
    for i in range(S.n - 1):
        E -= Jc * s[:, i] * s[:, i + 1]
    if periodic:
        E -= Jc * s[:, -1] * s[:, 0]
    return E


# ---------------------------------------------------------------------------
# minimax barriers
# ---------------------------------------------------------------------------
def barrier_from(S: Space, E, a, allowed=None):
    """B(a, .) for all targets by a Dijkstra-type search in the (min,max) semiring.
    `allowed`: optional boolean mask restricting the vertex set (a must be allowed)."""
    E = np.asarray(E, dtype=float)
    B = np.full(S.N, np.inf)
    if allowed is not None and not allowed[a]:
        return B
    B[a] = E[a]
    heap = [(E[a], a)]
    done = np.zeros(S.N, dtype=bool)
    while heap:
        b, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v in S.nbrs[u]:
            if done[v] or (allowed is not None and not allowed[v]):
                continue
            nb = b if b >= E[v] else E[v]
            if nb < B[v]:
                B[v] = nb
                heapq.heappush(heap, (nb, int(v)))
    return B


def minimax_path(S: Space, E, a, b):
    """One optimal minimax path a..b (list of indices) and its value."""
    E = np.asarray(E, dtype=float)
    B = np.full(S.N, np.inf)
    par = np.full(S.N, -1, dtype=np.int64)
    B[a] = E[a]
    heap = [(E[a], 0, a)]
    done = np.zeros(S.N, dtype=bool)
    while heap:
        bb, hops, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        if u == b:
            break
        for v in S.nbrs[u]:
            if done[v]:
                continue
            nb = bb if bb >= E[v] else E[v]
            if nb < B[v]:
                B[v] = nb
                par[v] = u
                heapq.heappush(heap, (nb, hops + 1, int(v)))
    path = [b]
    while path[-1] != a:
        path.append(int(par[path[-1]]))
    return path[::-1], B[b]


def component_below(S: Space, E, a, t, strict=True):
    """Connected component of a in {E < t} (strict) or {E <= t}; empty mask if a is not in the set."""
    E = np.asarray(E)
    ok = (E < t) if strict else (E <= t)
    comp = np.zeros(S.N, dtype=bool)
    if not ok[a]:
        return comp
    stack = [a]
    comp[a] = True
    while stack:
        u = stack.pop()
        for v in S.nbrs[u]:
            if ok[v] and not comp[v]:
                comp[v] = True
                stack.append(int(v))
    return comp


def outer_boundary(S: Space, mask):
    out = np.zeros(S.N, dtype=bool)
    for u in np.nonzero(mask)[0]:
        out[S.nbrs[u]] = True
    return out & ~mask


def inner_boundary(S: Space, mask):
    return outer_boundary(S, ~mask)


def separates(S: Space, wall, a, b):
    """True iff every path a..b meets the vertex set `wall` (a or b in wall counts)."""
    if wall[a] or wall[b]:
        return True
    comp = np.zeros(S.N, dtype=bool)
    comp[a] = True
    stack = [a]
    while stack:
        u = stack.pop()
        for v in S.nbrs[u]:
            if not wall[v] and not comp[v]:
                if v == b:
                    return False
                comp[v] = True
                stack.append(int(v))
    return True


def connects(S: Space, region, a, b):
    """True iff a and b are joined by a path inside the vertex set `region`."""
    if not (region[a] and region[b]):
        return False
    return not separates(S, ~region, a, b)


def local_minima(S: Space, E, strict=False):
    E = np.asarray(E)
    out = []
    for u in range(S.N):
        nb = E[S.nbrs[u]]
        if (strict and np.all(nb > E[u])) or (not strict and np.all(nb >= E[u])):
            out.append(u)
    return out


def depth(S: Space, E, a):
    """Depth (0-dim persistence, elder rule without ties) of state a:
    min over b with E(b) < E(a) of B(a,b) - E(a); +inf if a is a global minimiser."""
    E = np.asarray(E, dtype=float)
    B = barrier_from(S, E, a)
    lower = E < E[a]
    if not lower.any():
        return np.inf
    return B[lower].min() - E[a]


# ---------------------------------------------------------------------------
# McShane envelopes, admissible residuals
# ---------------------------------------------------------------------------
def is_admissible(g, D, tol=1e-9):
    g = np.asarray(g)
    return bool(np.all(g[:, None] - g[None, :] <= D + tol))


def mcshane(D, A, v):
    """L(y) = max_a [v(a) - d(a,y)],  U(y) = min_a [v(a) + d(y,a)]."""
    A = np.asarray(A, dtype=np.int64)
    v = np.asarray(v, dtype=float)
    L = (v[:, None] - D[A, :]).max(axis=0)
    U = (v[:, None] + D[:, A].T).min(axis=0)
    return L, U


def cond_env(D, L, U):
    """Conditional envelope D_A(x,y) = min(d(x,y), U(x) - L(y))   (theory report Thm 11.1)."""
    return np.minimum(D, U[:, None] - L[None, :])


def random_admissible(D, rng, kind=None):
    """A random element of the admissible class {g : g(x)-g(y) <= d(x,y)} (not uniform).
    Built from McShane-type extensions of random data so that many constraints are tight."""
    N = D.shape[0]
    kind = kind or rng.choice(["mix", "upper", "lower", "scaled", "cone+", "cone-"])
    if kind == "cone+":
        a = rng.integers(N)
        return D[:, a].copy()
    if kind == "cone-":
        a = rng.integers(N)
        return -D[a, :].copy()
    if kind == "scaled":
        # kappa-Lipschitz function: random admissible scaled down
        g = random_admissible(D, rng, kind="mix")
        return rng.uniform(0, 1) * g
    # random consistent anchor data: sequentially sample within the McShane bracket
    m = int(rng.integers(1, min(N, 12) + 1))
    A = rng.choice(N, size=m, replace=False)
    v = np.zeros(m)
    for j in range(m):
        if j == 0:
            v[j] = 0.0
        else:
            L, U = mcshane(D, A[:j], v[:j])
            lam = rng.choice([0.0, 1.0, rng.uniform()])
            v[j] = (1 - lam) * L[A[j]] + lam * U[A[j]]
    L, U = mcshane(D, A, v)
    if kind == "upper":
        return U
    if kind == "lower":
        return L
    lam = rng.uniform()
    return (1 - lam) * L + lam * U


# ---------------------------------------------------------------------------
# reversible single-site dynamics
# ---------------------------------------------------------------------------
def generator(S: Space, E, beta, rule="metropolis"):
    """Continuous-time generator Q (N x N, rows sum to 0) of single-site dynamics reversible
    w.r.t. pi ∝ exp(-beta E).  Each ordered pair (x, y) of neighbours has proposal rate
    1/deg_max ... we use proposal rate 1 per neighbour ("one attempt per neighbour per unit time"),
    so rates are  metropolis: min(1, e^{-beta(E_y-E_x)});  midpoint: e^{-beta(E_y-E_x)/2};
    heatbath: e^{-beta E_y} / sum_{s} e^{-beta E(x^{i->s})}  (site i = the site that changes;
    the site itself is chosen at rate 1).
    """
    E = np.asarray(E, dtype=float)
    Q = np.zeros((S.N, S.N))
    for u in range(S.N):
        nb = S.nbrs[u]
        if rule == "metropolis":
            r = np.minimum(1.0, np.exp(-beta * (E[nb] - E[u])))
        elif rule == "midpoint":
            r = np.exp(-beta * (E[nb] - E[u]) / 2)
        elif rule == "heatbath":
            r = np.zeros(len(nb))
            sites = S.nbr_site[u]
            for i in set(sites.tolist()):
                sel = sites == i
                emin = min(E[u], E[nb[sel]].min())
                w = np.exp(-beta * (E[nb[sel]] - emin))
                r[sel] = w / (w.sum() + np.exp(-beta * (E[u] - emin)))
        else:
            raise ValueError(rule)
        Q[u, nb] = r
        Q[u, u] = -r.sum()
    return Q


def gibbs(E, beta):
    E = np.asarray(E, dtype=float)
    w = np.exp(-beta * (E - E.min()))
    return w / w.sum()


def conductances(Q, pi):
    """c(x,y) = pi(x) Q(x,y) (symmetric for a reversible chain), diagonal set to 0."""
    C = pi[:, None] * Q
    np.fill_diagonal(C, 0.0)
    return C


def spectral_gap(Q, pi):
    s = np.sqrt(pi)
    Asym = (s[:, None] * Q) / s[None, :]
    Asym = 0.5 * (Asym + Asym.T)
    ev = np.linalg.eigvalsh(-Asym)
    return ev[1], ev


def dirichlet_eig(Q, pi, A):
    """Principal Dirichlet eigenvalue lambda_A of -Q restricted to A (killed outside), the
    quasi-stationary distribution on A and the full spectrum + spectral weights of 1_A."""
    idx = np.nonzero(A)[0]
    s = np.sqrt(pi[idx])
    M = -(s[:, None] * Q[np.ix_(idx, idx)]) / s[None, :]
    M = 0.5 * (M + M.T)
    ev, V = np.linalg.eigh(M)
    v0 = V[:, 0] * np.sign(V[:, 0].sum())
    qsd = v0 * s
    qsd = qsd / qsd.sum()
    # spectral weights of the normalised vector sqrt(pi_A)
    u = s / np.linalg.norm(s)
    wts = (V.T @ u) ** 2
    return ev[0], qsd, ev, wts, idx


def mean_exit_time(Q, A):
    """E_x[tau_{A^c}] for x in A: solve -Q_AA w = 1."""
    idx = np.nonzero(A)[0]
    w = np.linalg.solve(-Q[np.ix_(idx, idx)], np.ones(len(idx)))
    out = np.zeros(Q.shape[0])
    out[idx] = w
    return out


def capacity(Q, pi, A, Bset):
    """cap(A,B) = min Dirichlet form over h=1 on A, 0 on B; returns (cap, equilibrium potential)."""
    N = Q.shape[0]
    h = np.zeros(N)
    h[A] = 1.0
    free = ~(A | Bset)
    idx = np.nonzero(free)[0]
    if len(idx):
        rhs = Q[np.ix_(idx, np.nonzero(A)[0])].sum(axis=1)
        h[idx] = np.linalg.solve(-Q[np.ix_(idx, idx)], rhs)
    C = conductances(Q, pi)
    cap = 0.5 * np.sum(C * (h[:, None] - h[None, :]) ** 2)
    return cap, h


def dirichlet_form(C, h):
    return 0.5 * np.sum(C * (h[:, None] - h[None, :]) ** 2)
