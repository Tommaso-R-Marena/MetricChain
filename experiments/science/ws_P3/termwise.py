"""
P3 -- term-by-term ("Faa di Bruno") upper bounds on mixed differences of the GB polarisation
energy over a set T of sites (any order m = |T| >= 1), computed from the descreening tables
without enumerating joint states.

Structure (see P3_REPORT section 2 for the statements and proofs):

  g = -KAPPA * [ (1/2) sum_p q_p^2 ib_p(I_p)  +  sum_{p<q} q_p q_q h(ell_p(I_p) + ell_q(I_q); r_pq) ]

An "instance" of an atom is the atom together with the state of its own site (fixed atoms: one
instance).  Given the instance, I_p = base + sum_{i != host} C_i(x_i) is a sum of one-site
functions, so for a set B of sites not containing the host and a smooth phi
    |Delta_B phi(I_p)| <= sup|phi^(|B|)| * prod_{i in B} delta_i,   delta_i = osc of C_i     (L1)
and for u = ell_p + ell_q, with D_B := sup|ell_p^(|B|)| prod delta_i^p + sup|ell_q^(|B|)| prod delta_i^q,
    |Delta_T h(u)| <= sum_{partitions pi of T} sup|h^(|pi|)| prod_{B in pi} D_B.               (L2)
A site of T that hosts one of the two atoms is handled by the triangle inequality over its two
states (L3): |Delta_T F| <= W(b) + W(b'), W = bound for T minus that site with the host state fixed.

`mode`:
  "class"    : all state pairs at the sites of T, every context (the class constant c_T);
  "anchored" : state pairs (x0_i, a) at the sites of T, every context (what the remainder
               identity of the anchored expansion needs).
Derivative suprema are supplied by a provider object with methods
  sup_ib(k, atoms, Ilo, Ihi), sup_ell(k, atoms, Ilo, Ihi)   -> arrays over atoms
  sup_h(k, r, wlo, whi)                                     -> array like r
(`SampleSup` below: sampling, NOT rigorous, for exploration; `encl.EnvelopeSup`: rigorous).
"""
import itertools, math
import numpy as np
from p3core import KAPPA, KCAL
import dfun


def set_partitions(items):
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for part in set_partitions(rest):
        for i in range(len(part)):
            yield part[:i] + [[first] + part[i]] + part[i + 1:]
        yield [[first]] + part


class SampleSup:
    """sup of |derivative| by sampling the interval at `ns` points (NOT rigorous)."""

    def __init__(self, G, ns=17):
        self.G = G
        self.ns = ns

    def _samp(self, lo, hi):
        t = np.linspace(0.0, 1.0, self.ns)
        return lo[None] + (hi - lo)[None] * t.reshape((-1,) + (1,) * lo.ndim)

    def sup_ib(self, k, atoms, Ilo, Ihi):
        G = self.G
        I = self._samp(Ilo, Ihi)
        d = dfun.ib_derivs(I, G.orr[atoms], G.rad[atoms], G.al[atoms], G.be[atoms], G.ga[atoms])
        return np.abs(d[k]).max(axis=0)

    def sup_ell(self, k, atoms, Ilo, Ihi):
        G = self.G
        I = self._samp(Ilo, Ihi)
        d = dfun.ell_derivs(I, G.orr[atoms], G.rad[atoms], G.al[atoms], G.be[atoms], G.ga[atoms])
        return np.abs(d[k]).max(axis=0)

    def ell_range(self, atoms, Ilo, Ihi):
        G = self.G
        a = dfun.ell_derivs(Ilo, G.orr[atoms], G.rad[atoms], G.al[atoms], G.be[atoms], G.ga[atoms])[0]
        b = dfun.ell_derivs(Ihi, G.orr[atoms], G.rad[atoms], G.al[atoms], G.be[atoms], G.ga[atoms])[0]
        return a, b

    def sup_h(self, k, r, wlo, whi):
        w = self._samp(wlo, whi)
        D = r[None] ** 2 * np.exp(-w) / 4.0
        return np.abs(np.exp(-w / 2.0) * dfun.eta_k(k, D)).max(axis=0)


class Group:
    """atoms sharing a host: host = None (fixed atoms) or (site l, state b)."""
    pass


class TermBound:
    def __init__(self, G, sup=None, anchor=None, kmax=4, pad_I=0.0):
        self.G = G
        self.sup = sup if sup is not None else SampleSup(G)
        self.anchor = anchor
        self.kmax = kmax
        ns = G.ns
        self.groups = []
        self.gid = {}
        g = Group()
        g.host = None
        g.atoms = G.fixed
        g.base = G.I0
        g.C = [G.A[i] for i in range(ns)]                    # (k_i, natoms)
        g.X = G.Xf
        self._finish(g, pad_I)
        self.groups.append(g)
        self.gid[None] = 0
        for l in range(ns):
            for b in range(G.k[l]):
                g = Group()
                g.host = (l, b)
                g.atoms = G.mov[l]
                g.base = G.S[l][b]
                g.C = [G.T[(l, i)][b] if i != l else np.zeros((G.k[i], len(G.mov[l]))) for i in range(ns)]
                g.X = G.Xm[l][b]
                self._finish(g, pad_I)
                self.gid[(l, b)] = len(self.groups)
                self.groups.append(g)
        self._pairs = {}

    def _finish(self, g, pad_I):
        G = self.G
        ns = G.ns
        g.q = G.q[g.atoms]
        cmin = np.array([c.min(axis=0) for c in g.C])        # (ns, natoms)
        cmax = np.array([c.max(axis=0) for c in g.C])
        g.Ilo = g.base + cmin.sum(0) - pad_I
        g.Ihi = g.base + cmax.sum(0) + pad_I
        pad_d = pad_I / max(ns, 1)                           # allowance for the rounding of a table difference
        g.delta_class = np.where(cmax > cmin, cmax - cmin + pad_d, 0.0)          # (ns, natoms)
        if self.anchor is not None:
            da = np.array([np.abs(g.C[i] - g.C[i][self.anchor[i]][None]).max(axis=0) for i in range(ns)])
            g.delta_anch = np.where(da > 0, da + pad_d, 0.0)
        g.supB = [None] + [self.sup.sup_ib(k, g.atoms, g.Ilo, g.Ihi) for k in range(1, self.kmax + 1)]
        g.supL = [None] + [self.sup.sup_ell(k, g.atoms, g.Ilo, g.Ihi) for k in range(1, self.kmax + 1)]
        g.elo, g.ehi = self.sup.ell_range(g.atoms, g.Ilo, g.Ihi)

    def delta(self, g, mode):
        return g.delta_class if mode == "class" else g.delta_anch

    # ------------------------------------------------------------------ self part
    def _self_group(self, g, B, mode):
        """bound of sum_p (KAPPA/2) q_p^2 |Delta_B ib_p| for the atoms of group g, B not containing the host (kJ/mol)."""
        m = len(B)
        if m == 0:
            raise ValueError
        d = self.delta(g, mode)
        prod = np.ones(len(g.atoms))
        for i in B:
            prod = prod * d[i]
        return 0.5 * KAPPA * float((g.q ** 2 * g.supB[m] * prod).sum())

    def _combine_host(self, vals, l, T, mode):
        """vals: array over the states b of site l of bounds with the host state fixed.
        l in T: triangle inequality over the two states; l not in T: worst context."""
        if l in T:
            if len(vals) < 2:
                return 0.0
            if mode == "class":
                top = np.sort(vals)[-2:]
                return float(top.sum())
            x0 = self.anchor[l]
            return float(vals[x0] + np.delete(vals, x0).max())
        return float(vals.max())

    def self_bound(self, T, mode="class"):
        """upper bound (kcal/mol) on |Delta_T (self part of g)|."""
        G = self.G
        T = tuple(T)
        tot = self._self_group(self.groups[0], T, mode)
        for l in range(G.ns):
            B = tuple(i for i in T if i != l)
            if len(B) == 0:
                # |T| = 1 and l = T[0]: the one-site difference of the self energy of side chain l itself;
                # not a many-body term -- bounded crudely by the oscillation is not attempted here
                tot += float("nan")
                continue
            vals = np.array([self._self_group(self.groups[self.gid[(l, b)]], B, mode) for b in range(G.k[l])])
            tot += self._combine_host(vals, l, T, mode)
        return tot / KCAL

    # ------------------------------------------------------------------ cross part
    def _pair_data(self, i1, i2):
        key = (i1, i2)
        if key not in self._pairs:
            g1, g2 = self.groups[i1], self.groups[i2]
            d = g1.X[:, None, :] - g2.X[None, :, :]
            r = np.sqrt((d * d).sum(-1))
            coef = KAPPA * np.abs(g1.q[:, None] * g2.q[None, :])
            if i1 == i2:
                coef = np.triu(coef, 1)
                r = r + np.eye(len(g1.atoms))
            wlo = g1.elo[:, None] + g2.elo[None, :]
            whi = g1.ehi[:, None] + g2.ehi[None, :]
            supH = [None] + [self.sup.sup_h(k, r, wlo, whi) for k in range(1, self.kmax + 1)]
            self._pairs[key] = (coef, supH)
        return self._pairs[key]

    def _cross_pair(self, i1, i2, B, mode):
        """bound of sum_{p in g1, q in g2} KAPPA |q_p q_q| |Delta_B h(ell_p + ell_q)|, B avoiding both hosts (kJ/mol)."""
        g1, g2 = self.groups[i1], self.groups[i2]
        coef, supH = self._pair_data(i1, i2)
        d1, d2 = self.delta(g1, mode), self.delta(g2, mode)
        m = len(B)
        if m == 0:
            raise ValueError
        Dcache = {}

        def DB(block):
            key = tuple(block)
            if key not in Dcache:
                p1 = np.ones(len(g1.atoms)); p2 = np.ones(len(g2.atoms))
                for i in block:
                    p1 = p1 * d1[i]; p2 = p2 * d2[i]
                k = len(block)
                Dcache[key] = (g1.supL[k] * p1)[:, None] + (g2.supL[k] * p2)[None, :]
            return Dcache[key]

        theta = np.zeros(coef.shape)
        for part in set_partitions(B):
            term = supH[len(part)].copy()
            for block in part:
                term = term * DB(block)
            theta += term
        return float((coef * theta).sum())

    def cross_bound(self, T, mode="class"):
        """upper bound (kcal/mol) on |Delta_T (cross part of g)|."""
        G = self.G
        T = tuple(T)
        ns = G.ns
        gid = self.gid
        tot = self._cross_pair(0, 0, T, mode)                                  # fixed-fixed
        for l in range(ns):
            B = tuple(i for i in T if i != l)
            if len(B) == 0:
                tot += float("nan")
                continue
            # fixed - site l, and site l - site l
            vals = np.array([self._cross_pair(0, gid[(l, b)], B, mode) + self._cross_pair(gid[(l, b)], gid[(l, b)], B, mode)
                             for b in range(G.k[l])])
            tot += self._combine_host(vals, l, T, mode)
        for l in range(ns):
            for l2 in range(l + 1, ns):
                B = tuple(i for i in T if i != l and i != l2)
                if len(B) == 0:
                    tot += float("nan")
                    continue
                W = np.array([[self._cross_pair(gid[(l, b)], gid[(l2, b2)], B, mode) for b2 in range(G.k[l2])] for b in range(G.k[l])])
                tot += self._combine_two(W, l, l2, T, mode)
        return tot / KCAL

    def _combine_two(self, W, l, l2, T, mode):
        inl, inl2 = l in T, l2 in T
        if not inl and not inl2:
            return float(W.max())
        if inl and not inl2:
            return max(self._combine_host(W[:, b2], l, T, mode) for b2 in range(W.shape[1]))
        if inl2 and not inl:
            return max(self._combine_host(W[b, :], l2, T, mode) for b in range(W.shape[0]))
        # both hosts in T: four corners
        k1, k2 = W.shape
        if k1 < 2 or k2 < 2:
            return 0.0
        best = 0.0
        if mode == "class":
            for b, bb in itertools.combinations(range(k1), 2):
                row = W[b] + W[bb]
                top = np.sort(row)[-2:]
                best = max(best, float(top.sum()))
        else:
            a, a2 = self.anchor[l], self.anchor[l2]
            for b in range(k1):
                if b == a:
                    continue
                row = W[a] + W[b]
                best = max(best, float(row[a2] + np.delete(row, a2).max()))
        return best
