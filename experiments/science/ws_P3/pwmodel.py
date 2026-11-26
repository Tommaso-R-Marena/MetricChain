"""
P3 -- pairwise models on the product domain: known part, anchors, anchored expansion data,
banded lower/upper models, exact partition functions and exact sampling by transfer matrix.
"""
import itertools, math, time
import numpy as np
from p3core import KT300, BETA


def known_tables(G, name="ff14SB"):
    """(c0, [h_i], {(i,j): J_ij}) of the ff14SB vacuum energy restricted to the domain of G (kcal/mol);
    exact one- and two-site tables built by P2's fbmodel (validated there against OpenMM)."""
    c0, h, J = G.fb.site_tables(name)
    h = [h[i][G.dom[i]] for i in range(G.ns)]
    J = {(i, j): tab[np.ix_(G.dom[i], G.dom[j])] for (i, j), tab in J.items()}
    return c0, h, J


def f_energy(st, c0, h, J):
    st = np.atleast_2d(st)
    e = np.full(st.shape[0], c0)
    for i in range(len(h)):
        e += h[i][st[:, i]]
    for (i, j), tab in J.items():
        e += tab[st[:, i], st[:, j]]
    return e


def icm_anchor(G, c0, h, J, sweeps=20):
    """coordinate descent: first on f, then on E = f + g.  Returns (state tuple, E, number of g evaluations)."""
    n = G.ns
    x = np.zeros(n, dtype=int)
    for _ in range(sweeps):                       # f only (tables)
        changed = False
        for i in range(n):
            cand = np.repeat(x[None], G.k[i], 0); cand[:, i] = np.arange(G.k[i])
            b = int(np.argmin(f_energy(cand, c0, h, J)))
            if b != x[i]:
                x[i] = b; changed = True
        if not changed:
            break
    nev = 0
    for _ in range(sweeps):
        changed = False
        for i in range(n):
            cand = np.repeat(x[None], G.k[i], 0); cand[:, i] = np.arange(G.k[i])
            e = f_energy(cand, c0, h, J) + G.energy(cand); nev += len(cand)
            b = int(np.argmin(e))
            if b != x[i]:
                x[i] = b; changed = True
        if not changed:
            break
    E = float(f_energy(x[None], c0, h, J)[0] + G.energy(x[None])[0])
    return tuple(int(v) for v in x), E, nev


# ----------------------------------------------------------------------------- anchored expansion
def ball_states(k, x0, M):
    """all states within Hamming distance M of x0, grouped by the changed set U.
    Returns (list of (U, block of states (m_U, n)), total)."""
    n = len(k)
    out = []
    tot = 0
    base = np.array(x0, dtype=int)
    for s in range(M + 1):
        for U in itertools.combinations(range(n), s):
            alts = [[a for a in range(k[i]) if a != x0[i]] for i in U]
            if any(len(a) == 0 for a in alts):
                continue
            if s == 0:
                blk = base[None].copy()
            else:
                grid = np.stack([gg.reshape(-1) for gg in np.meshgrid(*alts, indexing="ij")], axis=1)
                blk = np.repeat(base[None], grid.shape[0], 0)
                blk[:, list(U)] = grid
            out.append((U, blk))
            tot += blk.shape[0]
    return out, tot


def anchored_terms(G, x0, M, chunk=4096, progress=None, energy=None):
    """Anchored (cut-HDMR) terms d_U(x_U), |U| <= M, of the GB energy at the anchor x0, from the values of g on
    the Hamming ball of radius M (evaluated here).  Returns (dict U -> array over ALL states of the sites of U
    (zero where some x_i = x0_i), number of evaluations, dict U -> g on the full sub-grid)."""
    k = G.k
    blocks, tot = ball_states(k, x0, M)
    allst = np.concatenate([b for _, b in blocks], axis=0)
    ef = energy if energy is not None else G.energy
    vals = np.empty(tot)
    t0 = time.time()
    for s in range(0, tot, chunk):
        vals[s:s + chunk] = ef(allst[s:s + chunk])
        if progress and (s // chunk) % progress == 0:
            print(f"      ball evaluations {min(tot, s + chunk)}/{tot}  {time.time() - t0:.0f}s", flush=True)
    gval = {}
    pos = 0
    for U, b in blocks:
        alts = [k[i] - 1 for i in U]
        gval[U] = vals[pos:pos + b.shape[0]].reshape(alts) if U else vals[pos]
        pos += b.shape[0]
    gfull, d = {}, {}
    for U, _ in blocks:
        s = len(U)
        if s == 0:
            gfull[U] = np.array(gval[U]); d[U] = np.array(gval[U])
            continue
        arr = np.empty([k[i] for i in U])
        non = [[a for a in range(k[i]) if a != x0[i]] for i in U]
        for r in range(s + 1):
            for Vpos in itertools.combinations(range(s), r):
                V = tuple(U[p] for p in Vpos)
                idx = [non[p] if p in Vpos else [x0[U[p]]] for p in range(s)]
                src = gval[V] if V else gval[()]
                shape = [len(ix) for ix in idx]
                arr[np.ix_(*idx)] = np.asarray(src).reshape(shape)
        gfull[U] = arr
        dd = arr.copy()
        for a, i in enumerate(U):
            dd = dd - np.take(dd, [x0[i]], axis=a)
        d[U] = dd
    return d, tot, gfull


def expansion_value(d, st, M=None):
    """sum over U (|U| <= M) of d_U(x_U) at the states st (N, n)."""
    st = np.atleast_2d(st)
    out = np.zeros(st.shape[0])
    for U, arr in d.items():
        if M is not None and len(U) > M:
            continue
        if len(U) == 0:
            out += float(arr)
        else:
            out += arr[tuple(st[:, i] for i in U)]
    return out


# ----------------------------------------------------------------------------- banded pairwise models
class BandModel:
    """const + sum_i one[i][x_i] + sum_{i<j<=i+w} pair[(i,j)][x_i, x_j]   (kcal/mol)."""

    def __init__(self, k, w):
        self.k = list(k); self.n = len(k); self.w = w
        self.const = 0.0
        self.one = [np.zeros(ki) for ki in k]
        self.pair = {}

    def add_pair(self, i, j, tab):
        if i > j:
            i, j = j, i; tab = tab.T
        assert 0 < j - i <= self.w
        self.pair[(i, j)] = self.pair.get((i, j), 0.0) + tab

    def energy(self, st):
        st = np.atleast_2d(st)
        e = np.full(st.shape[0], self.const)
        for i in range(self.n):
            e += self.one[i][st[:, i]]
        for (i, j), tab in self.pair.items():
            e += tab[st[:, i], st[:, j]]
        return e

    def _A(self, i, msg, scale):
        """array over the sites i..min(i+w, n-1): message + scaled terms attached to site i."""
        n, w, k = self.n, self.w, self.k
        hi = min(i + w, n - 1)
        nax = hi - i + 1
        A = np.zeros([k[s] for s in range(i, hi + 1)])
        if msg is not None:
            A = A + msg.reshape(msg.shape + (1,) * (nax - msg.ndim))
        sh = [1] * nax; sh[0] = k[i]
        A = A + scale * self.one[i].reshape(sh)
        for j in range(i + 1, hi + 1):
            if (i, j) in self.pair:
                sh = [1] * nax; sh[0] = k[i]; sh[j - i] = k[j]
                A = A + scale * self.pair[(i, j)].reshape(sh)
        return A

    def dp(self, scale, mode="logsumexp", keep=False):
        """mode 'logsumexp': ln sum_x exp(scale * (energy - const)) + scale*const;
        mode 'max': max_x scale * energy.  keep=True also returns the pre-reduction arrays (for sampling / argmax)."""
        msg = None
        As = []
        for i in range(self.n):
            A = self._A(i, msg, scale)
            if keep:
                As.append(A)
            if mode == "max":
                msg = A.max(axis=0)
            else:
                mx = A.max(axis=0)
                msg = mx + np.log(np.exp(A - mx[None]).sum(axis=0))
        val = float(msg) + scale * self.const
        return (val, As) if keep else val

    def lnZ(self, beta=BETA):
        return self.dp(-beta, "logsumexp")

    def minimum(self):
        return -self.dp(-1.0, "max")

    def maximum(self):
        return self.dp(1.0, "max")

    def sample(self, N, rng, beta=BETA):
        """N independent samples from exp(-beta * energy)/Z by backward sampling (inverse CDF)."""
        _, As = self.dp(-beta, "logsumexp", keep=True)
        n, w = self.n, self.w
        st = np.zeros((N, n), dtype=int)
        for i in range(n - 1, -1, -1):
            A = As[i]
            hi = min(i + w, n - 1)
            idx = (slice(None),) + tuple(st[:, j] for j in range(i + 1, hi + 1))
            lw = A[idx]                                  # (k_i, N) or (k_i,) broadcast
            if lw.ndim == 1:
                lw = np.repeat(lw[:, None], N, 1)
            lw = lw - lw.max(axis=0, keepdims=True)
            p = np.exp(lw); p /= p.sum(axis=0, keepdims=True)
            cdf = np.cumsum(p, axis=0)
            u = rng.random(N)
            st[:, i] = np.minimum((u[None, :] > cdf).sum(axis=0), self.k[i] - 1)
        return st


def _additive_split(P, sense):
    """bound a two-site table P(x_i, x_j) by a_i(x_i) + b_j(x_j): from below (sense=-1) or above (sense=+1).
    b_j = column means; a_i = row min (max) of the rest."""
    b = P.mean(axis=0)
    R = P - b[None, :]
    a = R.min(axis=1) if sense < 0 else R.max(axis=1)
    return a, b


def build_band_models(k, x0, c0, h, J, d, w, Gamma, M, gam=None):
    """Lower and upper banded pairwise models of E = f + g from the anchored terms d_U (|U| <= M) and the certified
    remainder constant Gamma (which must bound |g - sum_{|U|<=M} d_U| and include the floating-point allowance).
    Pairs beyond the band and all terms of order 3..M are replaced by exact minorants / majorants that depend on
    at most two in-band sites.  Returns (lower, upper, info)."""
    n = len(k)
    lo, up = BandModel(k, w), BandModel(k, w)
    slack = dict(far_pairs=0.0, order3=0.0, order4=0.0)
    for mdl, sense in ((lo, -1), (up, +1)):
        # remainder: constant Gamma, or (gam given) site penalties gam_i [x_i != x0_i] plus the constant Gamma
        mdl.const = c0 + float(d[()]) + sense * Gamma
        for i in range(n):
            mdl.one[i] = mdl.one[i] + h[i] + d.get((i,), np.zeros(k[i]))
            if gam is not None:
                pen = np.full(k[i], sense * gam[i]); pen[x0[i]] = 0.0
                mdl.one[i] = mdl.one[i] + pen
        for i in range(n):
            for j in range(i + 1, n):
                P = J[(i, j)] + d.get((i, j), 0.0)
                if j - i <= w:
                    mdl.add_pair(i, j, P)
                else:
                    a, b = _additive_split(P, sense)
                    mdl.one[i] = mdl.one[i] + a
                    mdl.one[j] = mdl.one[j] + b
        for U, arr in d.items():
            s = len(U)
            if s < 3:
                continue
            # choose the in-band pair of U whose minorant/majorant has the smallest sup slack
            best = None
            for pa, pb in itertools.combinations(range(s), 2):
                if U[pb] - U[pa] > w:
                    continue
                other = tuple(p for p in range(s) if p not in (pa, pb))
                red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                sl = float(np.abs(arr - np.expand_dims(red, other)).max())
                if best is None or sl < best[0]:
                    best = (sl, pa, pb, red)
            if best is not None:
                mdl.add_pair(U[best[1]], U[best[2]], best[3])
            else:
                other = tuple(range(1, s))
                red = arr.min(axis=other) if sense < 0 else arr.max(axis=other)
                mdl.one[U[0]] = mdl.one[U[0]] + red
    return lo, up
