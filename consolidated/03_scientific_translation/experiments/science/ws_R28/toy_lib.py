"""R28 — own implementation of the cell-wise sandwich (Proposition A17.24) for an open chain of
angles with nearest-neighbour terms.  Written from the STATEMENT of items 97–98 of
INFERENCE_LIMITS_ADDENDA.md (lines 4167–4239), before the script under review was opened.

Grid model: every angle on N equally spaced points, reference nu_i = normalised weights on the grid
(uniform, or proportional to exp(-e_i) when the one-body terms are put into the reference).
Cells: k closed cells per angle, each with m+1 = N/k+1 grid points; the two end points of a cell
carry half their weight (trapezoid rule), so that the cells are a MIXTURE decomposition of nu_i.

Everything is done in the log domain (the all-H penalty can be hundreds of nats).
"""
import numpy as np
from scipy.special import logsumexp


def grid(N):
    return 2.0 * np.pi * np.arange(N) / N


def cell_index(N, k):
    """idx[c, a] = grid index of point a (0..m) of closed cell c;  tw[a] trapezoid weights."""
    assert N % k == 0
    m = N // k
    idx = (np.arange(k)[:, None] * m + np.arange(m + 1)[None, :]) % N
    tw = np.ones(m + 1)
    tw[0] = tw[-1] = 0.5
    return idx, tw


def halfopen_index(N, k):
    """Genuine partition of the grid: cell c holds points c*m .. (c+1)*m-1, all with full weight."""
    assert N % k == 0
    m = N // k
    idx = (np.arange(k)[:, None] * m + np.arange(m)[None, :]) % N
    tw = np.ones(m)
    return idx, tw


class Chain:
    """Open chain.  w[i] : unnormalised reference weights on the grid (length N) for site i.
    pair[i] : N x N array, V_i(x_i = grid[j], x_{i+1} = grid[l]).
    one[i]  : optional one-body term (length N) kept as a TERM of V (not in the reference); or None.
    """

    def __init__(self, w, pair, one=None):
        self.n = len(w)
        self.N = len(w[0])
        self.w = [np.asarray(a, float) for a in w]
        self.pair = pair
        self.one = one
        assert len(pair) == self.n - 1

    # ---------------------------------------------------------------- exact value on the grid
    def lnZ_exact(self):
        lognu = [np.log(a / a.sum()) for a in self.w]
        f = lognu[0].copy()
        if self.one is not None:
            f = f - self.one[0]
        for i in range(self.n - 1):
            f = logsumexp(f[:, None] - self.pair[i], axis=0) + lognu[i + 1]
            if self.one is not None:
                f = f - self.one[i + 1]
        return float(logsumexp(f))


class Cells:
    """All cell tables of a chain for a given cell decomposition (idx, tw)."""

    def __init__(self, chain, idx, tw):
        self.ch = chain
        n = chain.n
        self.n = n
        self.k = idx.shape[0]
        self.idx = idx
        k = self.k
        # conditional measures P[i][c, a] and cell weights v[i][c]
        self.P, self.v = [], []
        for i in range(n):
            ww = chain.w[i][idx] * tw[None, :]
            vc = ww.sum(axis=1)
            self.P.append(ww / vc[:, None])
            self.v.append(vc / chain.w[i].sum())
        # pair tables
        self.A, self.mn, self.mx = [], [], []
        self.oL, self.oR = [], []            # both coordinates in mode H
        self.R_HM, self.oL_HM = [], []       # left H, right M
        self.R_MH, self.oR_MH = [], []       # left M, right H
        for i in range(n - 1):
            V4 = chain.pair[i][idx[:, :, None, None], idx[None, None, :, :]]   # (k, m+1, k, m+1)
            Pl, Pr = self.P[i], self.P[i + 1]
            self.A.append(np.einsum('ca,db,cadb->cd', Pl, Pr, V4, optimize=True))
            self.mn.append(V4.min(axis=(1, 3)))
            self.mx.append(V4.max(axis=(1, 3)))
            maxa, mina = V4.max(axis=1), V4.min(axis=1)        # (k, k, m+1): functions of right coord b
            maxb, minb = V4.max(axis=3), V4.min(axis=3)        # (k, m+1, k): functions of left coord a
            self.oL.append((maxa - mina).max(axis=2))          # osc in x_i, sup over x_{i+1}
            self.oR.append((maxb - minb).max(axis=1))          # osc in x_{i+1}, sup over x_i
            # right coordinate minimised (mode M), left in H: function of a
            self.R_HM.append(np.einsum('ca,cad->cd', Pl, minb))
            self.oL_HM.append(minb.max(axis=1) - minb.min(axis=1))
            # left coordinate minimised, right in H: function of b
            self.R_MH.append(np.einsum('db,cdb->cd', Pr, mina))
            self.oR_MH.append(mina.max(axis=2) - mina.min(axis=2))
        # one-body terms kept as terms of V
        self.one_mean = self.one_min = self.one_max = self.one_osc = None
        if chain.one is not None:
            self.one_mean, self.one_min, self.one_max, self.one_osc = [], [], [], []
            for i in range(n):
                e = chain.one[i][idx]
                self.one_mean.append((self.P[i] * e).sum(axis=1))
                self.one_min.append(e.min(axis=1))
                self.one_max.append(e.max(axis=1))
                self.one_osc.append(e.max(axis=1) - e.min(axis=1))

    # ---------------------------------------------------------------- pairwise discrete models
    def _lnZ_pairwise(self, tabs, ones=None):
        n = self.n
        f = np.log(self.v[0])
        if ones is not None:
            f = f - ones[0]
        for i in range(n - 1):
            f = logsumexp(f[:, None] - tabs[i], axis=0) + np.log(self.v[i + 1])
            if ones is not None:
                f = f - ones[i + 1]
        return float(logsumexp(f))

    def lnZ_jensen(self):
        return self._lnZ_pairwise(self.A, self.one_mean)

    def lnZ_minima(self):       # upper end by cell minima (term by term)
        return self._lnZ_pairwise(self.mn, self.one_min)

    def lnZ_maxima(self):       # lower end by cell maxima (term by term)
        return self._lnZ_pairwise(self.mx, self.one_max)

    # ---------------------------------------------------------------- the upper end (c), any modes
    def upper_tables(self, H):
        """H[i][c] True = (site i, cell c) in mode H.  Returns per pair term: R, oscL, oscR  (k x k)."""
        Rs, oLs, oRs = [], [], []
        for i in range(self.n - 1):
            hl = H[i][:, None]
            hr = H[i + 1][None, :]
            R = np.where(hl & hr, self.A[i],
                         np.where(hl & ~hr, self.R_HM[i],
                                  np.where(~hl & hr, self.R_MH[i], self.mn[i])))
            oscL = np.where(hr, self.oL[i], self.oL_HM[i])      # used only where hl
            oscR = np.where(hl, self.oR[i], self.oR_MH[i])      # used only where hr
            Rs.append(R)
            oLs.append(oscL)
            oRs.append(oscR)
        return Rs, oLs, oRs

    def lnZ_upper(self, H, scale=1.0, return_parts=False):
        """ln of  sum_s v_s exp(-sum_T R_T + (1/8) sum_{i in H(s)} c_i(s)^2).
        scale multiplies every oscillation (scale < 1 is the 'too small oscillation' control)."""
        n, k = self.n, self.k
        Rs, oLs, oRs = self.upper_tables(H)
        lv = [np.log(a) for a in self.v]
        one_R = None
        one_o = [np.zeros(k) for _ in range(n)]
        if self.one_mean is not None:
            one_R = [np.where(H[i], self.one_mean[i], self.one_min[i]) for i in range(n)]
            one_o = [np.where(H[i], self.one_osc[i], 0.0) for i in range(n)]
        # site 1
        c1 = (one_o[0][:, None] + oLs[0]) * scale
        F = lv[0][:, None] + lv[1][None, :] - Rs[0] + np.where(H[0][:, None], c1 ** 2 / 8.0, 0.0)
        if one_R is not None:
            F = F - one_R[0][:, None] - one_R[1][None, :]
        for i in range(1, n - 1):                       # site i (0-based), middle of (i-1, i, i+1)
            Fn = np.empty((k, k))
            for b in range(k):
                if H[i][b]:
                    c = (one_o[i][b] + oRs[i - 1][:, b][:, None] + oLs[i][b, :][None, :]) * scale
                    G = F[:, b][:, None] + c ** 2 / 8.0
                    Fn[b, :] = logsumexp(G, axis=0)
                else:
                    Fn[b, :] = logsumexp(F[:, b])
            Fn = Fn + lv[i + 1][None, :] - Rs[i]
            if one_R is not None:
                Fn = Fn - one_R[i + 1][None, :]
            F = Fn
        cn = (one_o[n - 1][None, :] + oRs[n - 2]) * scale
        F = F + np.where(H[n - 1][None, :], cn ** 2 / 8.0, 0.0)
        return float(logsumexp(F))

    def all_H(self):
        return [np.ones(self.k, bool) for _ in range(self.n)]

    def all_M(self):
        return [np.zeros(self.k, bool) for _ in range(self.n)]

    def cmax_allH(self):
        """q[i][c] = max over the neighbours' cells of c_i(s) with every coordinate in mode H."""
        n, k = self.n, self.k
        q = []
        for i in range(n):
            t = np.zeros(k)
            if self.one_osc is not None:
                t = t + self.one_osc[i]
            if i > 0:
                t = t + self.oR[i - 1].max(axis=0)
            if i < n - 1:
                t = t + self.oL[i].max(axis=1)
            q.append(t)
        return q

    def modes_by_threshold(self, tau):
        q = self.cmax_allH()
        return [qi <= tau for qi in q]


# -------------------------------------------------------------------------------------------------
def brute_force_check(chain, idx, tw, H, scale=1.0):
    """Direct check FROM THE DEFINITIONS for a tiny chain: enumerate every discrete state s, and
    for each s compute <e^{-V}>_s, sum_T <V_T>_s, sum_T R_T, c_i(s) by explicit loops over the cell
    points; return max violations of (a), (b), (c) and the three lnZ values.  Exponential cost."""
    import itertools
    n, N = chain.n, chain.N
    k, mp = idx.shape
    P, v = [], []
    for i in range(n):
        ww = chain.w[i][idx] * tw[None, :]
        vc = ww.sum(axis=1)
        P.append(ww / vc[:, None])
        v.append(vc / chain.w[i].sum())

    def Vfull(pts):         # pts: grid indices of all n sites
        e = 0.0
        for i in range(n - 1):
            e += chain.pair[i][pts[i], pts[i + 1]]
        if chain.one is not None:
            for i in range(n):
                e += chain.one[i][pts[i]]
        return e

    acc_exact, acc_low, acc_up = [], [], []          # logs, summed with logsumexp at the end
    worst_b = worst_c = -np.inf
    for s in itertools.product(range(k), repeat=n):
        vs = np.prod([v[i][s[i]] for i in range(n)])
        Hs = [i for i in range(n) if H[i][s[i]]]
        Ms = [i for i in range(n) if not H[i][s[i]]]
        # <e^{-V}>_s and <V>_s by enumeration over the product of cells
        mean_exp = 0.0
        mean_V = 0.0
        for a in itertools.product(range(mp), repeat=n):
            pr = np.prod([P[i][s[i], a[i]] for i in range(n)])
            if pr == 0.0:
                continue
            pts = [idx[s[i], a[i]] for i in range(n)]
            e = Vfull(pts)
            mean_exp += pr * np.exp(-e)
            mean_V += pr * e
        # W = sum_T V_T^s as a function of the H-coordinates (inf over M-coordinates of each term)
        def term_inf(i, aH):      # pair term i between sites i, i+1 ; aH dict site -> point index a
            lr = []
            for site in (i, i + 1):
                if site in aH:
                    lr.append([idx[s[site], aH[site]]])
                else:
                    lr.append(list(idx[s[site], :]))
            return min(chain.pair[i][p, q] for p in lr[0] for q in lr[1])

        def one_inf(i, aH):
            if chain.one is None:
                return 0.0
            if i in aH:
                return chain.one[i][idx[s[i], aH[i]]]
            return min(chain.one[i][idx[s[i], :]])

        def W(aH):
            return sum(term_inf(i, aH) for i in range(n - 1)) + sum(one_inf(i, aH) for i in range(n))

        meanW = 0.0
        for a in itertools.product(range(mp), repeat=len(Hs)):
            pr = np.prod([P[Hs[j]][s[Hs[j]], a[j]] for j in range(len(Hs))]) if Hs else 1.0
            meanW += pr * W({Hs[j]: a[j] for j in range(len(Hs))})
        # c_i(s) from the definition: sum over terms containing i of sup over the other H-coordinates
        # of the term of the oscillation in x_i
        pen = 0.0
        for i in Hs:
            ci = 0.0
            terms = []
            if i > 0:
                terms.append(i - 1)
            if i < n - 1:
                terms.append(i)
            for t in terms:                 # term t couples sites t and t+1
                other = i + 1 if t == i else i - 1
                if other in Hs:
                    sup = 0.0
                    for ao in range(mp):
                        vals = [term_inf(t, {i: ai, other: ao}) for ai in range(mp)]
                        sup = max(sup, max(vals) - min(vals))
                else:
                    vals = [term_inf(t, {i: ai}) for ai in range(mp)]
                    sup = max(vals) - min(vals)
                ci += sup
            if chain.one is not None:
                e = chain.one[i][idx[s[i], :]]
                ci += e.max() - e.min()
            pen += (scale * ci) ** 2 / 8.0
        log_low = -mean_V                       # ln of the right-hand side of (b)
        log_up = -meanW + pen                   # ln of the right-hand side of (c)
        log_mid = np.log(mean_exp)
        worst_b = max(worst_b, log_low - log_mid)       # > 0 would violate (b)
        worst_c = max(worst_c, log_mid - log_up)        # > 0 would violate (c)
        acc_exact.append(np.log(vs) + log_mid)
        acc_low.append(np.log(vs) + log_low)
        acc_up.append(np.log(vs) + log_up)
    return dict(lnZ_cells=float(logsumexp(acc_exact)), lnZ_low=float(logsumexp(acc_low)),
                lnZ_up=float(logsumexp(acc_up)), worst_b=worst_b, worst_c=worst_c)
