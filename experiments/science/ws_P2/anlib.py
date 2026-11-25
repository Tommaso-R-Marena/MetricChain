"""
Analysis helpers for workstream P2: class constants of a residual on an enumerated rotamer grid
with NON-uniform numbers of states per site and an arbitrary (non-product) domain mask.

Conventions: an enumerated grid is an array g of shape (k_1, ..., k_n), axis i = site i; `mask`
is a boolean array of the same shape (the domain).  Energies in kcal/mol; kT = 0.596161.
"""
import os, math, json, itertools
import numpy as np

KT300 = 0.0019872041 * 300.0
BETA = 1.0 / KT300
HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------------------- data
def load_fb(tag):
    """load data/<tag>.npz written by enum_fb.py; grid arrays are reshaped to the product shape."""
    z = dict(np.load(os.path.join(HERE, "data", tag + ".npz"), allow_pickle=False))
    shape = tuple(int(v) for v in z["shape"])
    off = z["dom_off"]
    d = dict(tag=tag, seq=str(z["seq"]), bb=str(z["bb"]), grid=str(z["grid"]), tau_enum=float(z["tau_enum"]),
             shape=shape, n=len(shape), CA=z["CA"], CB=z["CB"], natoms=int(z["natoms"]), s_fixed=float(z["s_fixed"]),
             sites=z["sites"], chi_tab=z["chi_tab"], ffs=[str(v) for v in z["ffs"]])
    d["dom"] = [z["dom_flat"][off[i]:off[i + 1]] for i in range(len(shape))]
    d["s1"] = [z["s1_flat"][off[i]:off[i + 1]] for i in range(len(shape))]
    size = int(np.prod(shape))
    for key, v in z.items():
        if getattr(v, "ndim", 0) == 1 and v.size == size and key not in ("dom_flat", "s1_flat", "shape", "dom_off", "sites", "ffs"):
            d[key] = v.reshape(shape)
    return d


GRID_KEYS = ("gb", "tors", "lj", "coul", "s1min", "s2min", "ff03", "ff15ipq", "ff99SB")


def restrict(d, tau):
    """sub-product of the states whose one-site clash score exceeds tau (>= the enumeration threshold)."""
    keep = [np.flatnonzero(s > tau) for s in d["s1"]]
    out = dict(d)
    ix = np.ix_(*keep)
    for key in GRID_KEYS:
        if key in d:
            out[key] = d[key][ix]
    out["shape"] = tuple(len(k) for k in keep)
    out["dom"] = [d["dom"][i][keep[i]] for i in range(d["n"])]
    out["s1"] = [d["s1"][i][keep[i]] for i in range(d["n"])]
    out["tau"] = tau
    return out


def residuals(d):
    """name -> grid array.  'f' = ff14SB vacuum energy (known part)."""
    f = d["tors"] + d["lj"] + d["coul"]
    r = {"f": f, "GB": d["gb"], "coul": d["coul"], "coul+GB": d["coul"] + d["gb"]}
    for ff in ("ff03", "ff15ipq", "ff99SB"):
        if ff in d:
            r[ff + "-ff14SB"] = d[ff] - f
    return r


# ---------------------------------------------------------------------------------------- constants
def pairdiff(G, axis):
    """stack over state pairs a < b of G[a] - G[b] along `axis`."""
    k = G.shape[axis]
    ia, ib = np.triu_indices(k, 1)
    return np.take(G, ia, axis=axis) - np.take(G, ib, axis=axis)


def _acc(D, acc):
    ad = np.abs(D)
    bad = np.isnan(ad)
    nb = int(bad.sum())
    if nb:
        ad[bad] = 0.0
    if ad.size:
        acc[0] = max(acc[0], float(ad.max()))
        acc[1] += float((ad * ad).sum())
        acc[2] += ad.size - nb


def mixed(g, mask, axes):
    """max and rms of |mixed difference of order len(axes)| over the sites `axes`: all state
    pairs at each of the sites, all base points, every evaluation point inside the mask.
    Returns (max, rms, number of valid differences)."""
    gm = np.where(mask, g, np.nan)
    G = np.moveaxis(gm, axes, range(len(axes)))
    acc = [0.0, 0.0, 0]
    k0 = G.shape[0]
    for a in range(k0):
        for b in range(a + 1, k0):
            D = G[a] - G[b]
            for ax in range(len(axes) - 1):
                D = pairdiff(D, ax)
            _acc(D, acc)
    return acc[0], math.sqrt(acc[1] / max(acc[2], 1)), acc[2]


def first_order(g, mask):
    """c_i, rms_i, counts; plus the location of the maximum (flat indices of the two points)."""
    n = g.ndim
    c = np.zeros(n); rms = np.zeros(n); cnt = np.zeros(n, dtype=np.int64)
    for i in range(n):
        c[i], rms[i], cnt[i] = mixed(g, mask, (i,))
    return c, rms, cnt


def first_order_argmax(g, mask, i):
    """(x, y): index tuples of the pair realising c_i."""
    gm = np.where(mask, g, np.nan)
    G = np.moveaxis(gm, i, 0)
    k = G.shape[0]
    best = (-1.0, None)
    for a in range(k):
        for b in range(a + 1, k):
            D = np.abs(G[a] - G[b])
            D[np.isnan(D)] = -1.0
            j = int(np.argmax(D))
            if D.reshape(-1)[j] > best[0]:
                rest = np.unravel_index(j, D.shape)
                best = (float(D.reshape(-1)[j]), (a, b, rest))
    a, b, rest = best[1]
    x = list(rest); x.insert(i, a)
    y = list(rest); y.insert(i, b)
    return tuple(int(v) for v in x), tuple(int(v) for v in y), best[0]


def second_order(g, mask):
    n = g.ndim
    C = np.zeros((n, n)); R = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            C[i, j], R[i, j], _ = mixed(g, mask, (i, j))
            C[j, i], R[j, i] = C[i, j], R[i, j]
    return C, R


def third_order(g, mask, triples=None):
    """dict (i,j,k) -> (max, rms)."""
    n = g.ndim
    out = {}
    for t in (triples if triples is not None else itertools.combinations(range(n), 3)):
        mx, rms, _ = mixed(g, mask, t)
        out[tuple(t)] = (mx, rms)
    return out


# ---------------------------------------------------------------------------------------- expansions
def star_part(g, x0):
    """additive interpolant on the star of x0: g(x0) + sum_i [g(x0 with site i -> x_i) - g(x0)]."""
    n = g.ndim
    out = np.full(g.shape, g[x0])
    for i in range(n):
        idx = list(x0); idx[i] = slice(None)
        line = g[tuple(idx)] - g[x0]
        sh = [1] * n; sh[i] = g.shape[i]
        out = out + line.reshape(sh)
    return out


def anchored2(g, x0):
    """anchored (cut-HDMR) expansion of order two at x0 (uses g on the Hamming ball of radius 2)."""
    n = g.ndim
    out = star_part(g, x0)
    for i in range(n):
        for j in range(i + 1, n):
            idx = list(x0); idx[i] = slice(None); idx[j] = slice(None)
            plane = g[tuple(idx)]                                        # (k_i, k_j)
            ii = list(x0); ii[i] = slice(None)
            jj = list(x0); jj[j] = slice(None)
            dij = plane - g[tuple(ii)][:, None] - g[tuple(jj)][None, :] + g[x0]
            sh = [1] * n; sh[i] = g.shape[i]; sh[j] = g.shape[j]
            out = out + dij.reshape(sh)
    return out


def changed(shape, x0):
    """list over sites of broadcastable 0/1 arrays [x_i != x0_i]."""
    n = len(shape)
    out = []
    for i in range(n):
        v = np.ones(shape[i]); v[x0[i]] = 0.0
        sh = [1] * n; sh[i] = shape[i]
        out.append(v.reshape(sh))
    return out


def pair_weight(shape, x0, C):
    """W(x) = sum_{i<j, both changed relative to x0} C[i, j]."""
    ch = changed(shape, x0)
    W = np.zeros(shape)
    n = len(shape)
    for i in range(n):
        for j in range(i + 1, n):
            if C[i, j] != 0.0:
                W = W + C[i, j] * ch[i] * ch[j]
    return W


def hamming(shape, x0):
    ch = changed(shape, x0)
    H = np.zeros(shape)
    for v in ch:
        H = H + v
    return H


def weighted_hamming(shape, x0, c):
    ch = changed(shape, x0)
    H = np.zeros(shape)
    for v, ci in zip(ch, c):
        H = H + ci * v
    return H


# ---------------------------------------------------------------------------------------- fits
def anova_fit(g, order):
    """L2-optimal approximation of g on the FULL product grid (uniform weights) by a sum of
    functions of at most `order` sites (order 1 or 2): the truncated ANOVA decomposition."""
    n = g.ndim
    mu = g.mean()
    out = np.full(g.shape, mu)
    main = []
    for i in range(n):
        ax = tuple(a for a in range(n) if a != i)
        m = g.mean(axis=ax, keepdims=True) - mu
        main.append(m)
        out = out + m
    if order >= 2:
        for i in range(n):
            for j in range(i + 1, n):
                ax = tuple(a for a in range(n) if a not in (i, j))
                out = out + (g.mean(axis=ax, keepdims=True) - mu - main[i] - main[j])
    return out


def design(states, shape, subsets):
    """sparse one-hot design matrix: an intercept and one table per subset of sites."""
    import scipy.sparse as sp
    M = states.shape[0]
    rows = [np.arange(M)]; cols = [np.zeros(M, dtype=np.int64)]
    ncol = 1
    for S in subsets:
        code = np.zeros(M, dtype=np.int64); size = 1
        for site in S:
            code = code * shape[site] + states[:, site]
            size *= shape[site]
        cols.append(ncol + code); rows.append(np.arange(M)); ncol += size
    A = sp.csr_matrix((np.ones(sum(len(r) for r in rows)), (np.concatenate(rows), np.concatenate(cols))), shape=(M, ncol))
    nz = np.asarray(A.sum(axis=0)).ravel() > 0
    return A[:, nz]


def subsets_of_order(n, order):
    s = [(i,) for i in range(n)]
    if order >= 2:
        s += [(i, j) for i in range(n) for j in range(i + 1, n)]
    return s


def fit_ls(A, y):
    from scipy.sparse.linalg import lsqr
    sol = lsqr(A, y, atol=1e-13, btol=1e-13, iter_lim=50000)
    return A @ sol[0]


def fit_sup(A, y, time_limit=900):
    """Chebyshev fit: min eta s.t. |y - A theta| <= eta (linear programme, HiGHS)."""
    import scipy.sparse as sp
    from scipy.optimize import linprog
    M, p = A.shape
    A = sp.csr_matrix(A)
    ones = sp.csr_matrix(np.ones((M, 1)))
    Aub = sp.vstack([sp.hstack([A, -ones]), sp.hstack([-A, -ones])]).tocsr()
    bub = np.concatenate([y, -y])
    c = np.zeros(p + 1); c[-1] = 1.0
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * p + [(0, None)], method="highs",
                  options={"time_limit": time_limit, "presolve": True})
    if res.x is None:
        return float("nan")
    return float(res.x[-1])


def low_order_fits(g, mask, lp_limit=30000):
    """remainders (rms, max) of the best one-site and two-site least-squares fits on the domain,
    and the Chebyshev (sup-optimal) remainders if the domain is small enough."""
    shape = g.shape
    n = g.ndim
    st = np.argwhere(mask)
    y = g[mask]
    out = {}
    full = bool(mask.all())
    for order in (1, 2):
        if order == 2 and n < 2:
            continue
        if full:
            pred = anova_fit(g, order)[mask]
        else:
            pred = fit_ls(design(st, shape, subsets_of_order(n, order)), y)
        r = y - pred
        out[f"ls{order}_rms"] = float(np.sqrt((r * r).mean())); out[f"ls{order}_max"] = float(np.abs(r).max())
        A = design(st, shape, subsets_of_order(n, order))
        out[f"npar{order}"] = int(A.shape[1])
        if len(y) <= lp_limit and A.shape[1] < 0.8 * len(y):
            out[f"sup{order}"] = fit_sup(A, y)
    out["std"] = float(y.std()); out["range"] = float(y.max() - y.min()); out["M"] = int(len(y))
    return out


# ---------------------------------------------------------------------------------------- free energies
def lnZ(E, mask, beta=BETA):
    e = E[mask]
    m = e.min()
    return float(np.log(np.exp(-beta * (e - m)).sum()) - beta * m)


def gibbs(E, mask, beta=BETA):
    w = np.where(mask, np.exp(-beta * (np.where(mask, E, 0.0) - E[mask].min())), 0.0)
    return w / w.sum()


def lncosh_sum(c, beta=BETA):
    u = beta * np.asarray(c) / 2.0
    return float(np.sum(np.logaddexp(u, -u) - math.log(2.0)))
