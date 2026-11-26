"""
Workstream P4 -- library.

What is P2's code and what is mine (so that "replication" and "re-run" can be told apart):
  * P2's code is used ONLY to read the enumerated grids and to rebuild its domain X' :
      anlib.load_fb, anlib.restrict, anlib.residuals, an_main.pruned_product, an_main.subselect
    (ws_P2 is read-only; nothing is written there: sys.dont_write_bytecode).
  * Everything else here is my own code, written from the statements of the theory report at
    24a3c27 (Theorems 11.16-11.18a, Propositions 11.18b, 11.18c): class constants of order two and
    three (a different algorithm from P2's: range over the last axis instead of all state pairs),
    tables at the reference, the star part and the interpolant of order two, the lower models,
    the share flow (Edmonds-Karp in exact rational arithmetic) and its verification by additions.

Conventions: a grid is an array of shape (k_1, ..., k_n) over the product domain X' ; x0 is an
index tuple; energies in kcal/mol; kT = 0.596161 kcal/mol (300 K), as in P2.
"""
import sys, os, math, itertools
from fractions import Fraction
import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
P2 = os.path.normpath(os.path.join(HERE, "..", "ws_P2"))
if P2 not in sys.path:
    sys.path.insert(0, P2)
import anlib      # P2 (read-only): loaders
import an_main    # P2 (read-only): pruned_product, subselect

KT = anlib.KT300
BETA = anlib.BETA
RESIDUALS = ("GB", "coul+GB", "ff03-ff14SB", "ff15ipq-ff14SB", "ff99SB-ff14SB")


# ------------------------------------------------------------------------------------------ data
def load_instance(tag, tau):
    """P2's instance (tag, tau) on its pruned clash-free product X'.  Returns None if a site has no
    state.  Keys: shape (of X'), f (known part = ff14SB vacuum energy), R (dict of residual grids),
    shape_raw (product X of the one-site admissible states), Xt (mask of the pair-clash-free
    domain X_tau inside X), keep (positions of the states of X' inside X, per site)."""
    d0 = anlib.load_fb(tag)
    d = anlib.restrict(d0, tau) if tau > d0["tau_enum"] + 1e-12 else dict(d0, tau=tau)
    shape = d["shape"]
    if min(shape) == 0:
        return None
    Xt = d["s2min"] > tau
    if Xt.all():
        dp = d
        keep = [np.arange(k) for k in shape]
    else:
        keep = an_main.pruned_product(d, tau)
        dp = an_main.subselect(d, keep)
    assert (dp["s2min"] > tau).all()
    R = anlib.residuals(dp)
    return dict(tag=tag, tau=tau, seq=d["seq"], bb=d["bb"], shape_raw=tuple(shape), Xt=Xt, keep=keep,
                shape=tuple(dp["shape"]), f=R["f"], R=R, Rraw=anlib.residuals(d))


def argmin_index(E):
    return tuple(int(v) for v in np.unravel_index(int(np.argmin(E)), E.shape))


# ------------------------------------------------------------------------------------------ class constants (own algorithm)
def c2_matrix(g):
    """c_ij = max over all rectangles of the product (all base points, all pairs of states at i and
    at j) of |g(ab) - g(a'b) - g(ab') + g(a'b')|.  Algorithm: for a < a' the difference
    D = g[a] - g[a'] is a function of (b, rest); the maximum over b, b' of |D[b] - D[b']| is the
    range of D along b."""
    n = g.ndim
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            G = np.moveaxis(g, (i, j), (0, 1))
            ki = G.shape[0]
            best = 0.0
            for a in range(ki - 1):
                D = G[a][None] - G[a + 1:]                    # (ki-a-1, kj, rest)
                r = float((D.max(axis=1) - D.min(axis=1)).max())
                best = max(best, r)
            C[i, j] = C[j, i] = best
    return C


def c3_dict(g, triples=None):
    """c_T, |T| = 3: max over all boxes of the product of the absolute third mixed difference."""
    n = g.ndim
    out = {}
    for (i, j, k) in (triples if triples is not None else itertools.combinations(range(n), 3)):
        G = np.moveaxis(g, (i, j, k), (0, 1, 2))
        ki, kj = G.shape[0], G.shape[1]
        best = 0.0
        for a in range(ki - 1):
            for a2 in range(a + 1, ki):
                D = G[a] - G[a2]                              # (kj, kk, rest)
                for b in range(kj - 1):
                    DD = D[b][None] - D[b + 1:]               # (kj-b-1, kk, rest)
                    r = float((DD.max(axis=1) - DD.min(axis=1)).max())
                    if r > best:
                        best = r
        out[(i, j, k)] = best
    return out


def c2_anchored(g, x0):
    """Anchored second-order constants: the maximum over those rectangles only that the proof of
    Theorem 11.16 visits -- one state of each of the two sites is the reference state, the base is
    arbitrary.  (Not P2's constants; a smaller, also valid input for the star at x0.)"""
    n = g.ndim
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            G = np.moveaxis(g, (i, j), (0, 1))
            D = G - G[x0[i]][None]                            # difference in i against the reference state
            DD = D - D[:, x0[j]][:, None]                     # then in j
            C[i, j] = C[j, i] = float(np.abs(DD).max())
    return C


def c3_anchored(g, x0):
    n = g.ndim
    out = {}
    for (i, j, k) in itertools.combinations(range(n), 3):
        G = np.moveaxis(g, (i, j, k), (0, 1, 2))
        D = G - G[x0[i]][None]
        D = D - D[:, x0[j]][:, None]
        D = D - D[:, :, x0[k]][:, :, None]
        out[(i, j, k)] = float(np.abs(D).max())
    return out


# ------------------------------------------------------------------------------------------ tables at the reference
def line(h, x0, i):
    idx = list(x0); idx[i] = slice(None)
    return h[tuple(idx)]


def second_diff(h, x0, i, j):
    """(k_i, k_j) table h(x0; i->a, j->b) - h(x0; i->a) - h(x0; j->b) + h(x0), i < j."""
    assert i < j
    idx = list(x0); idx[i] = slice(None); idx[j] = slice(None)
    return h[tuple(idx)] - line(h, x0, i)[:, None] - line(h, x0, j)[None, :] + h[x0]


def changed(shape, x0):
    n = len(shape)
    out = []
    for i in range(n):
        v = np.ones(shape[i]); v[x0[i]] = 0.0
        sh = [1] * n; sh[i] = shape[i]
        out.append(v.reshape(sh))
    return out


def star_part(g, x0):
    n = g.ndim
    out = np.full(g.shape, g[x0])
    for i in range(n):
        sh = [1] * n; sh[i] = g.shape[i]
        out = out + (line(g, x0, i) - g[x0]).reshape(sh)
    return out


def interp2(g, x0):
    """interpolant of order two around x0 (Theorem 11.18a(a)): star part + second mixed differences at x0."""
    n = g.ndim
    out = star_part(g, x0)
    for i in range(n):
        for j in range(i + 1, n):
            sh = [1] * n; sh[i] = g.shape[i]; sh[j] = g.shape[j]
            out = out + second_diff(g, x0, i, j).reshape(sh)
    return out


def pair_penalty(shape, x0, P):
    """sum_{i<j both changed} P[i, j] as a grid."""
    ch = changed(shape, x0)
    n = len(shape)
    W = np.zeros(shape)
    for i in range(n):
        for j in range(i + 1, n):
            if P[i, j] != 0.0:
                W = W + P[i, j] * ch[i] * ch[j]
    return W


def site_penalty(shape, x0, gam):
    ch = changed(shape, x0)
    W = np.zeros(shape)
    for i, v in enumerate(ch):
        if gam[i] != 0.0:
            W = W + gam[i] * v
    return W


def triple_penalty(shape, x0, c3):
    ch = changed(shape, x0)
    W = np.zeros(shape)
    for (i, j, k), v in c3.items():
        if v != 0.0:
            W = W + v * ch[i] * ch[j] * ch[k]
    return W


def excitations(E, x0):
    """list over sites of A_i(a) = E(x0; i->a) - E(x0) (array over the states of site i)."""
    return [line(E, x0, i) - E[x0] for i in range(E.ndim)]


def min_excitation(A, x0):
    """Delta_i = least single-site excitation energy; +inf for a site with a single state."""
    out = []
    for i, a in enumerate(A):
        v = np.delete(a, x0[i])
        out.append(float(v.min()) if v.size else math.inf)
    return out


def lnZ(E, beta=BETA):
    e = E.ravel()
    m = e.min()
    return float(np.log(np.exp(-beta * (e - m)).sum()) - beta * m)


def margin_at(L, x0):
    """min over x != x0 of L(x) - L(x0)  (>= 0 iff x0 minimises L)."""
    v = L[x0]
    M = L.copy()
    M[x0] = np.inf
    return float(M.min() - v) if M.size > 1 else math.inf


# ------------------------------------------------------------------------------------------ deficits (Proposition 11.18b(d))
def deficits(c, Tpair, x0, shape):
    """w_ij = max over a != x0_i, b != x0_j of [c_ij - T_ij(a, b)]_+ ;  c: (n, n) array of pair
    constants (or pair penalties), Tpair(i, j) -> (k_i, k_j) table of second differences at x0.
    Pairs with a single-state site get 0 (the maximum over an empty set of changed states)."""
    n = len(shape)
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if shape[i] < 2 or shape[j] < 2:
                continue
            T = Tpair(i, j)
            T = np.delete(np.delete(T, x0[i], axis=0), x0[j], axis=1)
            w[i, j] = w[j, i] = max(float((c[i, j] - T).max()), 0.0)
    return w


# ------------------------------------------------------------------------------------------ share flow, exact
def _F(x):
    return Fraction(x) if not isinstance(x, Fraction) else x


def share_flow(w, Delta):
    """Shares of Proposition 11.18b: s_ij, s_ji >= 0 with s_ij + s_ji >= w_ij (i != j) and
    sum_{j != i} s_ij <= Delta_i.  w: symmetric (n, n) array of floats >= 0; Delta: list of floats
    (may be +inf; may be negative).  All arithmetic is exact (the floats are converted to
    rationals).  Returns dict(ok, s (dict (i, j) -> Fraction, ordered pairs) or None,
    S (an over-dense set, sorted list) or None, excess (Fraction: sum of w inside S minus sum of
    Delta over S), total, flow)."""
    n = len(Delta)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n) if w[i][j] > 0]
    neg = [i for i in range(n) if Delta[i] < 0]
    if neg:
        i = neg[0]
        return dict(ok=False, s=None, S=[i], excess=-_F(Delta[i]), total=sum((_F(float(w[i][j])) for (i, j) in pairs), Fraction(0)), flow=None)
    # nodes: 0 source, 1..P pair nodes, P+1..P+n site nodes, P+n+1 sink
    P = len(pairs)
    src, snk = 0, P + n + 1
    N = P + n + 2
    cap = {}
    adj = [[] for _ in range(N)]

    def add(u, v, c):
        if (u, v) not in cap:
            cap[(u, v)] = Fraction(0); cap[(v, u)] = cap.get((v, u), Fraction(0))
            adj[u].append(v); adj[v].append(u)
        cap[(u, v)] += c

    total = Fraction(0)
    BIG = None
    for p, (i, j) in enumerate(pairs):
        wij = _F(float(w[i][j]))
        total += wij
        add(src, 1 + p, wij)
        add(1 + p, P + 1 + i, wij)          # capacity w_ij is as good as infinite here
        add(1 + p, P + 1 + j, wij)
    inf_sites = set()
    for i in range(n):
        if Delta[i] == math.inf:
            inf_sites.add(i)
    for i in range(n):
        add(P + 1 + i, snk, total + 1 if i in inf_sites else _F(float(Delta[i])))
    cap0 = dict(cap)
    flow = Fraction(0)
    while True:                              # Edmonds-Karp
        prev = {src: None}
        queue = [src]
        while queue and snk not in prev:
            u = queue.pop(0)
            for v in adj[u]:
                if v not in prev and cap[(u, v)] > 0:
                    prev[v] = u
                    queue.append(v)
        if snk not in prev:
            reach = set(prev)
            break
        b = None
        v = snk
        while prev[v] is not None:
            u = prev[v]
            b = cap[(u, v)] if b is None else min(b, cap[(u, v)])
            v = u
        v = snk
        while prev[v] is not None:
            u = prev[v]
            cap[(u, v)] -= b; cap[(v, u)] += b
            v = u
        flow += b
    if flow == total:
        s = {}
        for p, (i, j) in enumerate(pairs):
            s[(i, j)] = cap0[(1 + p, P + 1 + i)] - cap[(1 + p, P + 1 + i)]
            s[(j, i)] = cap0[(1 + p, P + 1 + j)] - cap[(1 + p, P + 1 + j)]
        return dict(ok=True, s=s, S=None, excess=None, total=total, flow=flow)
    S = sorted(i for i in range(n) if (P + 1 + i) in reach)
    exc = sum((_F(float(w[i][j])) for (i, j) in pairs if i in S and j in S), Fraction(0)) - sum((_F(float(Delta[i])) for i in S), Fraction(0))
    return dict(ok=False, s=None, S=S, excess=exc, total=total, flow=flow)


def verify_shares(w, Delta, s):
    """The checker of Proposition 11.18b: additions and comparisons only, exact arithmetic.
    True iff s >= 0, s_ij + s_ji >= w_ij for every pair, and every load is at most Delta_i."""
    n = len(Delta)
    for v in s.values():
        if v < 0:
            return False
    for i in range(n):
        for j in range(i + 1, n):
            if s.get((i, j), Fraction(0)) + s.get((j, i), Fraction(0)) < _F(float(w[i][j])):
                return False
    for i in range(n):
        load = sum((s.get((i, j), Fraction(0)) for j in range(n) if j != i), Fraction(0))
        if Delta[i] != math.inf and load > _F(float(Delta[i])):
            return False
    return True


def verify_overdense(w, Delta, S):
    """exact: sum_{i<j in S} w_ij > sum_{i in S} Delta_i  (a witness that no shares exist)."""
    if any(Delta[i] == math.inf for i in S):
        return False
    lhs = sum((_F(float(w[i][j])) for i in S for j in S if i < j), Fraction(0))
    rhs = sum((_F(float(Delta[i])) for i in S), Fraction(0))
    return lhs > rhs


def densest_excess(w, Delta):
    """brute force over all sets S of sites (n <= 20): max of sum_{i<j in S} w_ij - sum_{i in S} Delta_i
    (floating point); returns (value, S).  <= 0 iff shares exist (Proposition 11.18b(b))."""
    n = len(Delta)
    act = [i for i in range(n) if Delta[i] != math.inf]
    m = len(act)
    if m == 0:
        return 0.0, []
    bits = ((np.arange(1 << m)[:, None] >> np.arange(m)[None, :]) & 1).astype(float)   # (2^m, m)
    val = -bits @ np.array([Delta[i] for i in act])
    for a in range(m):
        for b in range(a + 1, m):
            wab = w[act[a]][act[b]]
            if wab != 0.0:
                val = val + wab * bits[:, a] * bits[:, b]
    val[0] = -np.inf
    k = int(np.argmax(val))
    return float(val[k]), [act[a] for a in range(m) if (k >> a) & 1]


def rowsum_ok(w, Delta):
    """the split in halves: (1/2) sum_{j != i} w_ij <= Delta_i for every site (exact arithmetic)."""
    n = len(Delta)
    for i in range(n):
        if Delta[i] == math.inf:
            continue
        half = sum((_F(float(w[i][j])) for j in range(n) if j != i), Fraction(0)) / 2
        if half > _F(float(Delta[i])):
            return False
    return True


# ------------------------------------------------------------------------------------------ state-dependent shares (an LP; my refinement, not in the theory report)
def state_shares_lp(c, Tpair, A, x0, shape):
    """Shares that may depend on the state of the site that carries them:
         s_ij(a) >= 0,  s_ij(a) + s_ji(b) >= c_ij - T_ij(a, b)   (a != x0_i, b != x0_j),
         sum_{j != i} s_ij(a) + t <= A_i(a)                        (a != x0_i);   maximise t.
    t >= 0 is sufficient for x0 to minimise  sum_i A_i + sum_{i<j changed} (T_ij - c_ij)
    (same proof as Proposition 11.18b(d)); constant shares give the certificate of the proposition.
    Returns (t, s) with s a dict (i, j) -> array over the states of i (0 at the reference state)."""
    from scipy.optimize import linprog
    import scipy.sparse as sp
    n = len(shape)
    act = [i for i in range(n) if shape[i] >= 2]
    off = {}
    nv = 0
    for i in act:
        for j in act:
            if i != j:
                off[(i, j)] = nv
                nv += shape[i]
    tvar = nv
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for i in act:
        for j in act:
            if i < j:
                T = Tpair(i, j)
                for a in range(shape[i]):
                    if a == x0[i]:
                        continue
                    for b in range(shape[j]):
                        if b == x0[j]:
                            continue
                        need = c[i, j] - T[a, b]
                        if need <= 0:
                            continue
                        rows += [r, r]; cols += [off[(i, j)] + a, off[(j, i)] + b]; vals += [-1.0, -1.0]
                        rhs.append(-need); r += 1
    for i in act:
        for a in range(shape[i]):
            if a == x0[i]:
                continue
            for j in act:
                if j != i:
                    rows.append(r); cols.append(off[(i, j)] + a); vals.append(1.0)
            rows.append(r); cols.append(tvar); vals.append(1.0)
            rhs.append(float(A[i][a])); r += 1
    Aub = sp.csr_matrix((vals, (rows, cols)), shape=(r, nv + 1))
    cost = np.zeros(nv + 1); cost[tvar] = -1.0
    res = linprog(cost, A_ub=Aub, b_ub=np.array(rhs), bounds=[(0, None)] * nv + [(None, None)], method="highs")
    if res.x is None:
        return float("nan"), None
    s = {(i, j): res.x[off[(i, j)]:off[(i, j)] + shape[i]].copy() for (i, j) in off}
    return float(res.x[tvar]), s


def verify_state_shares(c, Tpair, A, x0, shape, s):
    """exact check by additions of a state-dependent share certificate (after clipping at 0):
    returns the exact minimum slack of the load constraints after the cover constraints have been
    repaired exactly (shares raised where the LP solution misses a cover constraint by rounding)."""
    n = len(shape)
    act = [i for i in range(n) if shape[i] >= 2]
    S = {key: [max(Fraction(float(v)), Fraction(0)) for v in arr] for key, arr in s.items()}
    for i in act:
        for j in act:
            if i < j:
                T = Tpair(i, j)
                for a in range(shape[i]):
                    if a == x0[i]:
                        continue
                    for b in range(shape[j]):
                        if b == x0[j]:
                            continue
                        need = Fraction(float(c[i, j])) - Fraction(float(T[a, b]))
                        gap = need - S[(i, j)][a] - S[(j, i)][b]
                        if gap > 0:
                            S[(i, j)][a] += gap                  # repair: now the cover constraint holds exactly
    slack = None
    for i in act:
        for a in range(shape[i]):
            if a == x0[i]:
                continue
            load = sum((S[(i, j)][a] for j in act if j != i), Fraction(0))
            sl = Fraction(float(A[i][a])) - load
            slack = sl if slack is None else min(slack, sl)
    return slack


# ------------------------------------------------------------------------------------------ non-product domains (Proposition 11.18c)
def dprime_mask(Xt, x0):
    """D'(x0) for a domain given by pairwise exclusions (mask Xt on a product, x0 in the domain):
    {x in D : every changed state of x is compatible with the reference state of every other site}
    = {x in D : the star point x0[i -> x_i] lies in D for every site i}."""
    assert Xt[x0]
    n = Xt.ndim
    out = Xt.copy()
    for i in range(n):
        ok = line(Xt, x0, i)
        sh = [1] * n; sh[i] = Xt.shape[i]
        out = out & ok.reshape(sh)
    return out


def c2_matrix_masked(g, mask):
    """second-order constants over the rectangles that lie inside the mask (all four corners)."""
    n = g.ndim
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            G = np.moveaxis(g, (i, j), (0, 1)); M = np.moveaxis(mask, (i, j), (0, 1))
            ki = G.shape[0]
            best = 0.0
            for a in range(ki - 1):
                V = M[a][None] & M[a + 1:]                       # (ki-a-1, kj, rest): both corners of the i-edge inside
                D = G[a][None] - G[a + 1:]
                hi = np.where(V, D, -np.inf).max(axis=1)
                lo = np.where(V, D, np.inf).min(axis=1)
                r = hi - lo                                     # -inf where no valid b; 0 where one
                r = r[np.isfinite(r)]
                if r.size:
                    best = max(best, float(r.max()))
            C[i, j] = C[j, i] = best
    return C


def c3_dict_masked(g, mask):
    """third-order constants over the boxes that lie inside the mask (all eight corners)."""
    n = g.ndim
    out = {}
    for (i, j, k) in itertools.combinations(range(n), 3):
        G = np.moveaxis(g, (i, j, k), (0, 1, 2)); M = np.moveaxis(mask, (i, j, k), (0, 1, 2))
        ki, kj = G.shape[0], G.shape[1]
        best = 0.0
        for a in range(ki - 1):
            for a2 in range(a + 1, ki):
                V = M[a] & M[a2]                               # (kj, kk, rest)
                if not V.any():
                    continue
                D = G[a] - G[a2]
                for b in range(kj - 1):
                    VV = V[b][None] & V[b + 1:]
                    if not VV.any():
                        continue
                    DD = D[b][None] - D[b + 1:]
                    hi = np.where(VV, DD, -np.inf).max(axis=1)
                    lo = np.where(VV, DD, np.inf).min(axis=1)
                    r = hi - lo
                    r = r[np.isfinite(r)]
                    if r.size:
                        v = float(r.max())
                        if v > best:
                            best = v
        out[(i, j, k)] = best
    return out
