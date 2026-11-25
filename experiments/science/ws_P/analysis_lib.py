"""
Analysis helpers for workstream P: envelope constants of real residuals on enumerated torsion
grids.  Energies in kcal/mol; kT = 0.596161 kcal/mol at 300 K.
"""
import itertools, math, os
import numpy as np

KT300 = 0.0019872041 * 300.0
HERE = os.path.dirname(os.path.abspath(__file__))


def load(alphabet, n):
    """Returns dict: k, m (number of torsion sites), mask-ready arrays shaped (k,)*m."""
    path = os.path.join(HERE, "data", f"grid_{alphabet}_n{n}.npz")
    if os.path.exists(path):
        d = dict(np.load(path))
    else:      # merge parts
        parts = sorted(p for p in os.listdir(os.path.join(HERE, "data"))
                       if p.startswith(f"grid_{alphabet}_n{n}_part"))
        assert parts, path
        ds = [dict(np.load(os.path.join(HERE, "data", p))) for p in parts]
        ds.sort(key=lambda z: int(z["lo"]))
        d = dict(ds[0])
        for key in ds[0]:
            if ds[0][key].ndim == 1 and len(ds[0][key]) == int(ds[0]["hi"]) - int(ds[0]["lo"]) and key not in ("phi_states", "psi_states"):
                d[key] = np.concatenate([z[key] for z in ds])
    k = int(d["k"]); m = 2 * n
    out = {"k": k, "m": m, "n": n, "alphabet": alphabet, "phi_states": d["phi_states"],
           "psi_states": d["psi_states"]}
    shape = (k,) * m
    for key, v in d.items():
        if getattr(v, "ndim", 0) == 1 and v.size == k ** m:
            out[key] = v.reshape(shape)
    return out


def residuals(d):
    """name -> array (k,)*m.  'f' is the known part (vacuum ff14SB, conformation-dependent part)."""
    f = d["tors"] + d["lj"] + d["coul"]
    r = {"f": f, "GB": d["gbn2"], "GBSA": d["gbn2"] + d["sa"]}
    if "obc2" in d:
        r["OBC2-GBn2"] = d["obc2"] - d["gbn2"]
    for ff in ("ff99SB", "ff19SB", "ff03", "ff15ipq"):
        if ff + "_tors" in d:
            e = d[ff + "_tors"] + d[ff + "_lj"] + d[ff + "_coul"]
            if ff == "ff19SB":
                e = e + d["ff19SB_cmap"]
            r[ff + "-ff14SB"] = e - f
    r["coul"] = d["coul"]
    r["coul+GB"] = d["coul"] + d["gbn2"]
    return r


def site_names(n):
    out = []
    for r in range(1, n + 1):
        out += [f"phi{r}", f"psi{r}"]
    return out


# ----------------------------------------------------------------------------------------
# first-order constants
def first_order(g, mask):
    """c_i = max over pairs differing in site i only (both in mask) of |g - g'|.
    Returns (c, rms, argmax list) with c shape (m,), rms the root-mean-square single-flip
    difference over valid pairs."""
    m = g.ndim; k = g.shape[0]
    c = np.zeros(m); rms = np.zeros(m); arg = []
    gm = np.where(mask, g, np.nan)
    for i in range(m):
        G = np.moveaxis(gm, i, 0).reshape(k, -1)
        best = 0.0; where = None; ss = 0.0; cnt = 0
        for a in range(k):
            for b in range(a + 1, k):
                dlt = G[a] - G[b]
                ok = ~np.isnan(dlt)
                if ok.any():
                    ad = np.abs(np.where(ok, dlt, 0.0))
                    j = int(np.argmax(ad))
                    if ad[j] > best:
                        best = ad[j]; where = (a, b, j)
                    ss += (ad[ok] ** 2).sum(); cnt += int(ok.sum())
        c[i] = best; rms[i] = math.sqrt(ss / max(cnt, 1)); arg.append(where)
    return c, rms, arg


def directed_first_order(g, mask):
    """delta_i(a,b) = max_x [g(x^{i->a}) - g(x^{i->b})] (asymmetric single-site envelopes)."""
    m = g.ndim; k = g.shape[0]
    out = np.zeros((m, k, k))
    gm = np.where(mask, g, np.nan)
    for i in range(m):
        G = np.moveaxis(gm, i, 0).reshape(k, -1)
        for a in range(k):
            for b in range(k):
                if a != b:
                    dlt = G[a] - G[b]
                    if (~np.isnan(dlt)).any():
                        out[i, a, b] = np.nanmax(dlt)
    return out


def residue_constants(g, mask):
    """C_r = max |g - g'| over pairs differing only in residue r (phi_r and psi_r)."""
    m = g.ndim; k = g.shape[0]; n = m // 2
    gm = np.where(mask, g, np.nan)
    C = np.zeros(n)
    for r in range(n):
        G = np.moveaxis(gm, (2 * r, 2 * r + 1), (0, 1)).reshape(k * k, -1)
        with np.errstate(all="ignore"):
            hi = np.nanmax(G, axis=0); lo = np.nanmin(G, axis=0)
        v = hi - lo
        C[r] = np.nanmax(v) if (~np.isnan(v)).any() else 0.0
    return C


# ----------------------------------------------------------------------------------------
# mixed second differences
def second_order(g, mask):
    """c_ij = max |g(a,b) - g(a',b) - g(a,b') + g(a',b')| over x and state pairs, all four
    points in mask.  Returns symmetric (m, m) array (diag 0) and rms array."""
    m = g.ndim; k = g.shape[0]
    gm = np.where(mask, g, np.nan)
    C = np.zeros((m, m)); R = np.zeros((m, m))
    for i in range(m):
        for j in range(i + 1, m):
            G = np.moveaxis(gm, (i, j), (0, 1)).reshape(k, k, -1)
            best = 0.0; ss = 0.0; cnt = 0
            for a in range(k):
                for a2 in range(a + 1, k):
                    for b in range(k):
                        for b2 in range(b + 1, k):
                            D = G[a, b] - G[a2, b] - G[a, b2] + G[a2, b2]
                            ok = ~np.isnan(D)
                            if ok.any():
                                ad = np.abs(D[ok])
                                best = max(best, ad.max()); ss += (ad ** 2).sum(); cnt += ad.size
            C[i, j] = C[j, i] = best
            R[i, j] = R[j, i] = math.sqrt(ss / max(cnt, 1))
    return C, R


# ----------------------------------------------------------------------------------------
# functional ANOVA on the full product grid (uniform weights)
def anova(g):
    """Orthogonal (Hoeffding) decomposition of g on the full product grid.
    Returns dict: var_total, var_by_order[o], var_by_span[(order, span)] with span =
    max site index - min site index of the interacting set, and the coefficient tensor."""
    m = g.ndim; k = g.shape[0]
    # orthonormal basis per site: constant + (k-1) contrasts (Helmert)
    H = np.zeros((k, k)); H[0] = 1.0 / math.sqrt(k)
    for r in range(1, k):
        H[r, :r] = 1.0; H[r, r] = -r
        H[r] /= np.linalg.norm(H[r])
    T = g.astype(float)
    for ax in range(m):
        T = np.moveaxis(np.tensordot(H, T, axes=(1, ax)), 0, ax)
    T = T / math.sqrt(k ** m)           # so that sum of squares = mean square of g
    sq = T ** 2
    idx = np.indices(sq.shape).reshape(m, -1)
    active = idx > 0
    order = active.sum(axis=0)
    sqf = sq.reshape(-1)
    by_order = np.bincount(order, weights=sqf, minlength=m + 1)
    first = np.where(active.any(0), active.argmax(0), 0)
    last = np.where(active.any(0), m - 1 - active[::-1].argmax(0), 0)
    span = last - first
    by_span = {}
    for o in range(1, m + 1):
        sel = order == o
        if sel.any():
            bs = np.bincount(span[sel], weights=sqf[sel], minlength=m)
            for s_, v in enumerate(bs):
                if v > 0:
                    by_span[(o, s_)] = v
    return {"var_total": by_order[1:].sum(), "by_order": by_order, "by_span": by_span,
            "coef": T, "order": order.reshape(sq.shape), "span": span.reshape(sq.shape)}


def anova_truncate(an, g, max_order=None, max_span=None):
    """Reconstruct the part of g with interaction order <= max_order and span <= max_span."""
    m = g.ndim; k = g.shape[0]
    keep = np.ones(an["coef"].shape, dtype=bool)
    if max_order is not None:
        keep &= an["order"] <= max_order
    if max_span is not None:
        keep &= (an["span"] <= max_span) | (an["order"] <= 1)
    T = np.where(keep, an["coef"], 0.0) * math.sqrt(k ** m)
    H = np.zeros((k, k)); H[0] = 1.0 / math.sqrt(k)
    for r in range(1, k):
        H[r, :r] = 1.0; H[r, r] = -r
        H[r] /= np.linalg.norm(H[r])
    for ax in range(m):
        T = np.moveaxis(np.tensordot(H.T, T, axes=(1, ax)), 0, ax)
    return T


# ----------------------------------------------------------------------------------------
# design matrices for low-order torsion models on a (masked) subset
def design_low_order(states, k, order=1, max_sep=None, sites=None):
    """states: (M, m) int array.  One-hot features for all single sites (order>=1) and all
    site pairs with |i-j| <= max_sep (order 2).  Returns scipy.sparse CSR matrix (with an
    intercept column).  Redundant (non-identified) columns are fine for least squares / LP."""
    import scipy.sparse as sp
    M, m = states.shape
    cols = [np.zeros(M, dtype=np.int64)]; rows = [np.arange(M)]
    ncol = 1
    for i in range(m):
        cols.append(ncol + states[:, i]); rows.append(np.arange(M)); ncol += k
    if order >= 2:
        for i in range(m):
            for j in range(i + 1, m):
                if max_sep is not None and j - i > max_sep:
                    continue
                cols.append(ncol + states[:, i].astype(np.int64) * k + states[:, j]); rows.append(np.arange(M)); ncol += k * k
    if order >= 3:
        for i in range(m):
            for j in range(i + 1, m):
                for l in range(j + 1, m):
                    if max_sep is not None and l - i > max_sep:
                        continue
                    cols.append(ncol + (states[:, i].astype(np.int64) * k + states[:, j]) * k + states[:, l])
                    rows.append(np.arange(M)); ncol += k ** 3
    rows = np.concatenate(rows); cols = np.concatenate(cols)
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(M, ncol))
    return A


def fit_ls(A, y):
    """Least-squares fit; returns (prediction, rank-ish info)."""
    from scipy.sparse.linalg import lsqr
    sol = lsqr(A, y, atol=1e-12, btol=1e-12, iter_lim=20000)
    return A @ sol[0], sol[0]


def fit_sup(A, y, bound=None, time_limit=600):
    """Chebyshev (sup-norm) fit by linear programming: min eta s.t. |y - A theta| <= eta,
    optionally |theta_j| <= bound_j (array or scalar; None = free).  Returns (eta, theta)."""
    import scipy.sparse as sp
    from scipy.optimize import linprog
    M, p = A.shape
    A = sp.csr_matrix(A)
    ones = sp.csr_matrix(np.ones((M, 1)))
    Aub = sp.vstack([sp.hstack([A, -ones]), sp.hstack([-A, -ones])]).tocsr()
    bub = np.concatenate([y, -y])
    c = np.zeros(p + 1); c[-1] = 1.0
    if bound is None:
        bnds = [(None, None)] * p + [(0, None)]
    else:
        b = np.broadcast_to(np.asarray(bound, dtype=float), (p,))
        bnds = [(-bb if np.isfinite(bb) else None, bb if np.isfinite(bb) else None) for bb in b] + [(0, None)]
    res = linprog(c, A_ub=Aub, b_ub=bub, bounds=bnds, method="highs",
                  options={"time_limit": time_limit, "presolve": True})
    if res.x is None:
        return float("nan"), None
    return float(res.x[-1]), res.x[:-1]


def states_of(mask):
    """int array (M, m) of the grid states of the conformations in mask (C order)."""
    return np.argwhere(mask).astype(np.int16)


def design_subsets(states, k, subsets):
    """One-hot interaction tables for each subset of sites (tuple of site indices), plus an
    intercept.  states: (M, m) ints.  Returns CSR matrix and the list of column offsets."""
    import scipy.sparse as sp
    M = states.shape[0]
    rows = [np.arange(M)]; cols = [np.zeros(M, dtype=np.int64)]
    ncol = 1; offs = []
    for S in subsets:
        code = np.zeros(M, dtype=np.int64)
        for site in S:
            code = code * k + states[:, site]
        offs.append(ncol)
        cols.append(ncol + code); rows.append(np.arange(M)); ncol += k ** len(S)
    A = sp.csr_matrix((np.ones(sum(len(r) for r in rows)), (np.concatenate(rows), np.concatenate(cols))), shape=(M, ncol))
    # drop empty columns (state combinations that never occur in the domain)
    nz = np.asarray(A.sum(axis=0)).ravel() > 0
    return A[:, nz], offs


def model_subsets(m, kind, w=None):
    """Named families of low-order torsion models."""
    singles = [(i,) for i in range(m)]
    if kind == "1body":
        return singles
    if kind == "res1":            # one table per residue (phi_r, psi_r)
        return [(2 * r, 2 * r + 1) for r in range(m // 2)]
    if kind == "2body":           # all torsion pairs with |i-j| <= w
        return singles + [(i, j) for i in range(m) for j in range(i + 1, m) if w is None or j - i <= w]
    if kind == "3body":
        return singles + [(i, j) for i in range(m) for j in range(i + 1, m) if w is None or j - i <= w] + \
            [(i, j, l) for i in range(m) for j in range(i + 1, m) for l in range(j + 1, m) if w is None or l - i <= w]
    if kind == "res2":            # residue pairs with |r-s| <= w: 4-site tables
        n = m // 2
        return [(2 * r, 2 * r + 1) for r in range(n)] + \
            [(2 * r, 2 * r + 1, 2 * s, 2 * s + 1) for r in range(n) for s in range(r + 1, n) if w is None or s - r <= w]
    if kind == "res3":
        n = m // 2
        return [(2 * r, 2 * r + 1, 2 * s, 2 * s + 1) for r in range(n) for s in range(r + 1, n) if w is None or s - r <= w] + \
            [(2 * r, 2 * r + 1, 2 * s, 2 * s + 1, 2 * t, 2 * t + 1) for r in range(n) for s in range(r + 1, n) for t in range(s + 1, n) if w is None or t - r <= w]
    raise ValueError(kind)


# ----------------------------------------------------------------------------------------
# pair-distance-profile class (theory report 11.17): g = c0 + sum_{pairs} phi_type(s_pq),
# s = squared distance, phi piecewise linear in s on knots s_k = r_k^2, phi = 0 beyond S_c.
AMBER_TYPE = {("ACE", "HH31"): "HC", ("ACE", "HH32"): "HC", ("ACE", "HH33"): "HC", ("ACE", "CH3"): "CT",
              ("ACE", "C"): "C", ("ACE", "O"): "O",
              ("ALA", "N"): "N", ("ALA", "H"): "H", ("ALA", "CA"): "CX", ("ALA", "HA"): "H1",
              ("ALA", "CB"): "CT", ("ALA", "HB1"): "HC", ("ALA", "HB2"): "HC", ("ALA", "HB3"): "HC",
              ("ALA", "C"): "C", ("ALA", "O"): "O",
              ("NME", "N"): "N", ("NME", "H"): "H", ("NME", "CH3"): "CT", ("NME", "HH31"): "H1",
              ("NME", "HH32"): "H1", ("NME", "HH33"): "H1"}


def pair_types(P, scheme, minsep=3):
    """Returns (i, j, type_index, type_names) for atom pairs separated by >= minsep bonds.
    scheme: 'one' | 'heavy' (heavy-atom pairs only, one type) | 'elem' | 'amber' | 'charge'
    ('charge': two types by the sign of the product of ff14SB partial charges)."""
    iu = np.triu_indices(P.natoms, 1)
    sel = P.topdist[iu] >= minsep
    i, j = iu[0][sel], iu[1][sel]
    atoms = list(P.top.atoms())
    if scheme == "one":
        lab = ["all"] * len(i)
    elif scheme == "heavy":
        keep = (P.elements[i] != "H") & (P.elements[j] != "H")
        i, j = i[keep], j[keep]
        lab = ["heavy"] * len(i)
    elif scheme == "elem":
        lab = ["-".join(sorted((P.elements[a], P.elements[b]))) for a, b in zip(i, j)]
    elif scheme == "amber":
        ty = [AMBER_TYPE[(a.residue.name, a.name)] for a in atoms]
        lab = ["-".join(sorted((ty[a], ty[b]))) for a, b in zip(i, j)]
    elif scheme == "charge":
        lab = ["like" if P.charges[a] * P.charges[b] > 0 else "unlike" for a, b in zip(i, j)]
    else:
        raise ValueError(scheme)
    names = sorted(set(lab))
    idx = np.array([names.index(l) for l in lab])
    return i, j, idx, names


def profile_features(P, X, scheme, knots_r, minsep=3, chunk=2048):
    """F[x, type, bin] = sum over pairs of the type of |[s_pq, S_c] cap [s_k, s_{k+1}]|,
    so that for phi piecewise linear in s with slopes phi'_k and phi(S_c)=0:
        sum_pairs phi(s_pq) = - sum_{type,bin} phi'_{type,bin} F[x, type, bin].
    Returns F reshaped (M, ntypes*nbins) and metadata."""
    i, j, tidx, names = pair_types(P, scheme, minsep)
    sk = np.asarray(knots_r, dtype=float) ** 2
    nb = len(sk) - 1
    nt = len(names)
    M = X.shape[0]
    F = np.zeros((M, nt, nb))
    onehot = np.zeros((len(i), nt)); onehot[np.arange(len(i)), tidx] = 1.0
    for s0 in range(0, M, chunk):
        x = X[s0:s0 + chunk]
        s = ((x[:, i] - x[:, j]) ** 2).sum(axis=2)
        for b in range(nb):
            contrib = np.clip(sk[b + 1] - np.maximum(s, sk[b]), 0.0, None)
            F[s0:s0 + chunk, :, b] = contrib @ onehot
    return F.reshape(M, nt * nb), dict(types=names, nbins=nb, knots_r=np.asarray(knots_r), npairs=len(i),
                                       width_s=np.diff(sk))
