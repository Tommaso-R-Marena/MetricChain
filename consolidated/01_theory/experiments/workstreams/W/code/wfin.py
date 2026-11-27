"""wfin.py -- exact finite-n sums over joint types (no asymptotics, no sampling).

A 'part' is one site type j of a chain at finite size: n_j sites, split into blocks u (the labels) of sizes
n_ju; every block has an integer-valued 'cost' function of the count vector k of the letters of a point in
that block.  Two cost functions are used:

 * 'transport' : c_u(k) = min-cost transport from the counts k (the exit point y, FIRST argument of d) to the
                 counts m_u of the centre class C  =  max over the vertices phi of L of <k - m_u, phi>,
                 so that  sum_u c_u = min_{x in C} d(y, x)  (block-wise integer transport is integral);
 * 'linear'    : c_u(k) = <k, phi_u> - n_ju min(phi_u)   (the value of the generalised cone sum_i phi_i(x_i)).

Costs are integer multiples of a lattice unit (the envelopes of wsites.py are multiples of a common unit).
The table  N[P, c] = #{ y of joint type P (within the part) with total cost c }  is built exactly (float64
counts, relative rounding only) by combining the blocks; everything else is read off it:

 * for ANY joint-type-invariant instance psi_g = g(type): the generalised dip  (r - Phi)_+ with
   Phi(y) = min_{x in C} [ d(y,x) - psi_g(y) + psi_g(x) ] = cost(y) + g(P_C) - g(P_y)   is admissible, its
   support is {Phi < r}, its effect on ln A is  E(r) = ln E_{mu_g} exp((r - Phi)_+)  and the density of its
   support in every joint-type class is exact  ->  certified: every algorithm that is (eps/2, delta)-correct
   makes at least (1 - 2 delta)/maxdens evaluations at psi_g whenever eps < E(r)  (GroupSampling.lean:
   group_queries_ge);
 * for the generalised cone: the weight is constant on (P, c)-cells, so the truncation at the orbit-wise
   q-quantiles and ln[A/A^tr] are exact  ->  certified non-adaptive bound (group_nonadaptive_queries_ge).
"""
import math

import numpy as np
from scipy.special import gammaln


def compositions(n, q):
    """all count vectors (rows) of length q with sum n"""
    if q == 1:
        return np.array([[n]], dtype=np.int64)
    if q == 2:
        k = np.arange(n + 1, dtype=np.int64)
        return np.stack([n - k, k], axis=1)
    out = []
    for k in range(n + 1):
        rest = compositions(n - k, q - 1)
        out.append(np.concatenate([rest, np.full((len(rest), 1), k, dtype=np.int64)], axis=1))
    return np.concatenate(out, axis=0)


def lmult(K):
    K = np.asarray(K, float)
    return gammaln(K.sum(axis=-1) + 1.0) - gammaln(K + 1.0).sum(axis=-1)


def round_counts(n, p):
    """integer vector with sum n closest to n*p (largest remainders)"""
    p = np.asarray(p, float)
    x = n * p
    k = np.floor(x).astype(np.int64)
    rem = n - int(k.sum())
    order = np.argsort(-(x - k))
    for i in range(rem):
        k[order[i]] += 1
    return k


class Part:
    """one site type at finite size: site, list of blocks (n_u, per-type integer cost array given by a callable)"""

    def __init__(self, site, sizes, unit):
        self.site = site
        self.q = site.q
        self.sizes = [int(s) for s in sizes]
        self.n = int(sum(self.sizes))
        self.unit = float(unit)
        self.stride = np.array([0] + [(self.n + 1) ** a for a in range(self.q - 1)], dtype=np.int64)
        self.sizeP = (self.n + 1) ** (self.q - 1)
        # all joint types of the part
        self.Ptypes = compositions(self.n, self.q)
        self.Pidx = self.Ptypes @ self.stride
        self.lTP = np.full(self.sizeP, -np.inf)
        self.lTP[self.Pidx] = lmult(self.Ptypes)

    def to_units(self, x, what="cost"):
        y = np.asarray(x, float) / self.unit
        yi = np.rint(y).astype(np.int64)
        assert np.max(np.abs(y - yi)) < 1e-6, f"{what} not on the lattice of unit {self.unit}"
        return yi

    def transport_costs(self, n_u, m_u):
        K = compositions(n_u, self.q)
        c = np.max((K - np.asarray(m_u)[None, :]) @ self.site.V.T, axis=1)
        return K, self.to_units(c)

    def linear_costs(self, n_u, phi):
        K = compositions(n_u, self.q)
        phi = np.asarray(phi, float)
        c = K @ (phi - phi.min())
        return K, self.to_units(c)

    def build(self, blocks, cmax):
        """blocks: list of (K, cost) per block (count vectors and integer costs); returns N[P_idx, c], c <= cmax"""
        C1 = int(cmax) + 1
        self.complete = int(cmax) >= sum(int(np.max(cost)) for (K, cost) in blocks)    # every possible cost is in the table
        self._scaled = False
        ent_key = np.array([0], dtype=np.int64)          # key = P_idx * C1 + c
        ent_cnt = np.array([1.0])
        for (K, cost) in blocks:
            order = np.argsort(cost, kind="stable")
            K, cost = K[order], cost[order]
            cnt = np.exp(lmult(K))
            keyu = (K @ self.stride) * C1 + cost
            acc = None
            acc = np.zeros(self.sizeP * C1)
            ent_c = ent_key % C1
            for e in range(len(ent_key)):
                m = int(np.searchsorted(cost, cmax - ent_c[e], side="right"))
                if m > 0:
                    acc[ent_key[e] + keyu[:m]] += ent_cnt[e] * cnt[:m]
            ent_key = np.nonzero(acc)[0]
            ent_cnt = acc[ent_key]
        self.C1 = C1
        self.N = acc.reshape(self.sizeP, C1)
        return self.N

    def dens_table(self):
        """f[P, c] = N[P, c]/|T_P| and its strict cumulative Fcum[P, i] = sum_{c < i} f[P, c].
        (N is rescaled in place: after this call self.N holds f.)"""
        if getattr(self, "_scaled", False):
            return self.N, self._F
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            scale = np.exp(-self.lTP)
        scale[~np.isfinite(scale)] = 0.0
        self.N *= scale[:, None]
        F = np.zeros((self.sizeP, self.C1 + 1))
        np.cumsum(self.N, axis=1, out=F[:, 1:])
        self._F = F
        self._scaled = True
        return self.N, F

    # ---- instance data on the joint types of the part ------------------------------------------------
    def g_additive(self, gamma):
        """psi_gamma as a function of the type (counts): g(P) = <P, gamma>; and the Gibbs masses of the type classes"""
        g = np.full(self.sizeP, np.inf)
        g[self.Pidx] = self.Ptypes @ np.asarray(gamma, float)
        pg = self.site.gibbs(gamma)
        lmass = np.full(self.sizeP, -np.inf)
        lmass[self.Pidx] = lmult(self.Ptypes) + self.Ptypes @ np.log(pg)
        return g, lmass

    def g_flat(self):
        """the flat-histogram instance psi_H = -n v(P/n) (lower envelope of the normalised additive instances):
        g(P) = -n v(P/n) and the Gibbs masses pi(T_P) exp(n v)/Z_H"""
        v = v_types(self.site, self.Ptypes / self.n)
        g = np.full(self.sizeP, np.inf)
        g[self.Pidx] = -self.n * v
        lw = lmult(self.Ptypes) + self.Ptypes @ np.log(self.site.pi) + self.n * v
        lZ = float(np.logaddexp.reduce(lw))
        lmass = np.full(self.sizeP, -np.inf)
        lmass[self.Pidx] = lw - lZ
        return g, lmass, lZ


def v_types(site, P):
    """v(P) = max_{gamma in L} [-E_P gamma - ln Z_gamma] for an array of laws P (rows), exactly (to 1e-12):
    the maximum of a concave function over the polytope L is at the unconstrained maximiser if it is in L,
    otherwise on the boundary; q = 2: an interval; q = 3: edges by bisection on the derivative."""
    P = np.asarray(P, float)
    q = site.q
    pi = site.pi

    def val(G):
        return -np.sum(P * G, axis=1) - np.log(np.sum(pi[None, :] * np.exp(-G), axis=1))

    best = np.full(len(P), -np.inf)
    # interior candidate gamma = -ln(P/pi) where P > 0
    pos = np.all(P > 0, axis=1)
    if np.any(pos):
        G = np.zeros_like(P)
        G[pos] = -np.log(P[pos] / pi[None, :])
        G = G - G[:, [0]]
        ok = pos & site.in_L(G, tol=1e-12)
        vv = val(G)
        best = np.where(ok, vv, best)
    # vertices
    for ph in site.V:
        best = np.maximum(best, val(np.broadcast_to(ph, P.shape)))
    if q >= 3:
        # edges: pairs of vertices that share q-2 tight constraints (for q = 3: adjacent vertices of the polygon)
        nv = site.nv
        tight = [frozenset((a, b) for a in range(q) for b in range(q)
                           if a != b and abs(site.V[k][a] - site.V[k][b] - site.d[a, b]) < 1e-9) for k in range(nv)]
        for k1 in range(nv):
            for k2 in range(k1 + 1, nv):
                if len(tight[k1] & tight[k2]) < q - 2:
                    continue
                g0, dg = site.V[k1], site.V[k2] - site.V[k1]
                lo, hi = np.zeros(len(P)), np.ones(len(P))
                for it in range(60):                      # derivative in s: -E_P dg + E_{pi_gamma(s)} dg, decreasing
                    mid = 0.5 * (lo + hi)
                    G = g0[None, :] + mid[:, None] * dg[None, :]
                    w = pi[None, :] * np.exp(-G)
                    w = w / w.sum(axis=1, keepdims=True)
                    der = -(P @ dg) + w @ dg
                    lo = np.where(der > 0, mid, lo)
                    hi = np.where(der > 0, hi, mid)
                mid = 0.5 * (lo + hi)
                best = np.maximum(best, val(g0[None, :] + mid[:, None] * dg[None, :]))
        if q > 3:
            raise NotImplementedError("v_types: faces of dimension >= 2 are not implemented (q <= 3 only)")
    return best


# ----------------------------------------------------------------------------------------------------------
# dips of an invariant instance: exact effect and exact orbit densities, for one or two parts
# ----------------------------------------------------------------------------------------------------------
class DipTable:
    def __init__(self, parts, deltas, lmasses):
        """parts: list of Part with built transport tables; deltas[j][P_idx] = g_j(P_C) - g_j(P) (inf off the
        lattice of types); lmasses[j][P_idx] = ln mu_g(T_P) of the part"""
        self.parts = parts
        self.tabs = [p.dens_table() for p in parts]
        self.deltas = deltas
        self.lmasses = lmasses
        # mass distribution of Phi_j = c*unit + delta_j(P): arrays (Phi value, mass) per part (nonzero cells only)
        self.phi, self.mass = [], []
        for p, (f, F), dl, lm in zip(parts, self.tabs, deltas, lmasses):
            rows, cols = np.nonzero(f)
            ph = dl[rows] + cols * p.unit
            ms = np.exp(lm[rows]) * f[rows, cols]
            keep = ms > 0
            self.phi.append(ph[keep])
            self.mass.append(ms[keep])
            assert ph[keep].min() > -1e-9, "negative slack: the instance is not admissible"

    def effect(self, r):
        """E(r) = ln E_mu exp((r - Phi)_+) = ln[1 + sum_{Phi < r} mass (e^{r - Phi} - 1)]  (exact)"""
        if len(self.parts) == 1:
            ph, ms = self.phi[0], self.mass[0]
            m = ph < r
            return math.log1p(float(np.sum(ms[m] * np.expm1(r - ph[m]))))
        assert len(self.parts) == 2
        (p1, m1), (p2, m2) = (self.phi[0], self.mass[0]), (self.phi[1], self.mass[1])
        o = np.argsort(p2)
        p2, m2 = p2[o], m2[o]
        c0 = np.concatenate([[0.0], np.cumsum(m2)])
        c1 = np.concatenate([[0.0], np.cumsum(m2 * np.exp(-p2))])
        use = p1 < r
        k = np.searchsorted(p2, r - p1[use], side="left")
        tot = np.sum(m1[use] * (np.exp(r - p1[use]) * c1[k] - c0[k]))
        return math.log1p(float(tot))

    def covered(self, r):
        """True if the tables contain every cost level that can lie below the threshold r"""
        for p, dl in zip(self.parts, self.deltas):
            raw = np.ceil((r - dl[p.Pidx]) / p.unit - 1e-9).max()
            if raw > p.C1 and not p.complete:
                return False
        return True

    def maxdens(self, r):
        """max over joint types of the density of {Phi < r} in the joint-type class (exact)"""
        assert self.covered(r), "cost tables too short for this threshold"
        if len(self.parts) == 1:
            p = self.parts[0]
            f, F = self.tabs[0]
            x = (r - self.deltas[0][p.Pidx]) / p.unit
            i = np.clip(np.ceil(x - 1e-9), 0, p.C1).astype(np.int64)
            d = F[p.Pidx, i]
            return float(d.max()), p.Ptypes[int(np.argmax(d))], int(i.max())
        assert len(self.parts) == 2
        pa, pb = self.parts
        fa, Fa = self.tabs[0]
        fb, Fb = self.tabs[1]
        best, arg, need = 0.0, None, 0
        xb = (r - self.deltas[1][pb.Pidx]) / pb.unit                   # threshold for c_b before subtracting Phi_a
        for ia, Pa in zip(pa.Pidx, pa.Ptypes):
            row = fa[ia]
            cs = np.nonzero(row)[0]
            if len(cs) == 0:
                continue
            da = self.deltas[0][ia]
            tot = np.zeros(len(pb.Pidx))
            for c in cs:
                x = xb - (da + c * pa.unit) / pb.unit
                i = np.clip(np.ceil(x - 1e-9), 0, pb.C1).astype(np.int64)
                if i.max() == 0:
                    break                                               # costs increase with c: nothing further
                need = max(need, int(i.max()))
                tot += row[c] * Fb[pb.Pidx, i]
            k = int(np.argmax(tot))
            if tot[k] > best:
                best, arg = float(tot[k]), (Pa, pb.Ptypes[k])
        return best, arg, need
