"""
P3 -- certified bounds on ANCHORED mixed differences of the GB energy, summed over all subsets
T of a given order m without enumerating the subsets ("generating-function" form of the
term-by-term bound).

For the anchor x0 and a set T of sites define the anchored-pair constant
    c_T^anch = sup over contexts z and states x_T of |Delta_T g(z; x0_T -> x_T)|.
The remainder identity (P3_REPORT, Proposition 1) gives for every x, with S(x) = {i: x_i != x0_i},
    | g(x) - sum_{T subset S(x), |T| < m} d_T(x_T) |  <=  sum_{T subset S(x), |T| = m} c_T^anch
                                                      <=  Gamma_m := sum_{|T| = m} chat_T,
and this module computes Gamma_m = sum over ALL T of order m of the term-by-term bound chat_T.

Instance types of an atom of side chain l (fixed atoms have the single type F):
    A : host state x0_l;   N : host state != x0_l, all ingredients maximised over those states;
    X : any host state (maximum of A and N).
For a pair of atoms and a set T: hosts outside T take type X (worst context); a host inside T is
handled by the triangle inequality over its two states, bounded by (type A) + (type N), with the
host removed from T.  For the remaining "free" set B (no host in it):
    |Delta_B h(ell_p + ell_q)| <= sum_{partitions pi of B} sup|h^(|pi|)| prod_{blocks} D_block,
    D_block = L^p_|block| prod delta^p + L^q_|block| prod delta^q.
Summing over all B of size s among the free sites and all partitions:
    sum_{a+b=s} e_{a,b}(delta^p, delta^q) * sum_{r1, r2} sup|h^(r1+r2)| Bell_{a,r1}(L^p) Bell_{b,r2}(L^q),
e_{a,b} = coefficient of u^a v^b in prod_{i free} (1 + u delta_i^p + v delta_i^q).

Units: kcal/mol.  `sup` is a provider of rigorous derivative suprema (encl.EnvelopeSup).
"""
import math, itertools
import numpy as np
from p3core import KAPPA, KCAL
from termwise import set_partitions

PAD_TAB = 2e-10      # nm^-1: budget for the floating-point error of a difference of two table entries
RND = 1.0 + 1e-9     # outward rounding factor applied to every final sum of products of positive doubles


def bell_arrays(L, s):
    """partial Bell polynomials B[a][r] (arrays like L[1]) for 0 <= r <= a <= s; L[k] = k-th derivative bound."""
    one = np.ones_like(L[1])
    B = [[None] * (s + 1) for _ in range(s + 1)]
    B[0][0] = one
    for a in range(1, s + 1):
        B[a][0] = np.zeros_like(one)
        for r in range(1, a + 1):
            acc = np.zeros_like(one)
            for j in range(1, a - r + 2):
                prev = B[a - j][r - 1]
                if prev is None:
                    continue
                acc = acc + math.comb(a - 1, j - 1) * L[j] * prev
            B[a][r] = acc
    return B


def esym2(dP, dQ, s):
    """e[a][b] (nP, nQ) for a + b <= s: coefficient of u^a v^b in prod_i (1 + u dP[i, p] + v dQ[i, q])."""
    nP, nQ = dP.shape[1], dQ.shape[1]
    e = [[None] * (s + 1) for _ in range(s + 1)]
    e[0][0] = np.ones((nP, nQ))
    for a in range(s + 1):
        for b in range(s + 1 - a):
            if a + b:
                e[a][b] = np.zeros((nP, nQ))
    for i in range(dP.shape[0]):
        x = dP[i][:, None]; y = dQ[i][None, :]
        if not (x.any() or y.any()):
            continue
        for tot in range(s, 0, -1):
            for a in range(tot, -1, -1):
                b = tot - a
                if a > 0:
                    e[a][b] += x * e[a - 1][b]
                if b > 0:
                    e[a][b] += y * e[a][b - 1]
    return e


def esym1(d, s):
    """elementary symmetric polynomials e[a] (n_atoms,) of the rows of d (n_sites, n_atoms), a <= s."""
    e = [np.ones(d.shape[1])] + [np.zeros(d.shape[1]) for _ in range(s)]
    for i in range(d.shape[0]):
        for a in range(s, 0, -1):
            e[a] += d[i] * e[a - 1]
    return e


class Inst:
    pass


class GFBound:
    def __init__(self, G, anchor, sup, K=6, mode="anchored"):
        self.G, self.sup, self.K, self.mode = G, sup, K, mode
        self.anchor = tuple(int(a) for a in anchor)
        ns = G.ns
        self.F = self._instances(None)
        self.site = [self._instances(l) for l in range(ns)]
        self._hcache = {}
        self._excl = None
        assert mode == "anchored", "the A + N treatment of a host inside T is only valid for anchored pairs"

    # ------------------------------------------------------------------ instances
    def _state_data(self, atoms, base, C, host):
        """ingredients for one host state: delta (ns, na), supB/supL (K+1, na), ell range."""
        G = self.G
        ns = G.ns
        cmin = np.array([c.min(axis=0) for c in C]); cmax = np.array([c.max(axis=0) for c in C])
        Ilo = base + cmin.sum(0) - ns * PAD_TAB
        Ihi = base + cmax.sum(0) + ns * PAD_TAB
        if self.mode == "anchored":
            d = np.array([np.abs(C[i] - C[i][self.anchor[i]][None]).max(axis=0) for i in range(ns)])
        else:
            d = cmax - cmin
        d = np.where(d > 0, d + PAD_TAB, 0.0)
        if host is not None:
            d[host] = 0.0
        supB = np.zeros((self.K + 1, len(atoms))); supL = np.zeros((self.K + 1, len(atoms)))
        for k in range(1, self.K + 1):
            supB[k] = self.sup.sup_ib(k, atoms, Ilo, Ihi)
            supL[k] = self.sup.sup_ell(k, atoms, Ilo, Ihi)
        elo, ehi = self.sup.ell_range(atoms, Ilo, Ihi)
        return dict(d=d, supB=supB, supL=supL, elo=elo, ehi=ehi, Ilo=Ilo, Ihi=Ihi)

    def _instances(self, l):
        G = self.G
        ns = G.ns
        o = Inst()
        o.host = l
        if l is None:
            o.atoms = G.fixed
            o.q = G.q[o.atoms]
            o.states = [None]
            o.per_state = [self._state_data(o.atoms, G.I0, [G.A[i] for i in range(ns)], None)]
            o.X = [G.Xf]
            o.types = {"F": [0]}
        else:
            o.atoms = G.mov[l]
            o.q = G.q[o.atoms]
            o.states = list(range(G.k[l]))
            o.per_state = []
            for b in o.states:
                C = [G.T[(l, i)][b] if i != l else np.zeros((G.k[i], len(o.atoms))) for i in range(ns)]
                o.per_state.append(self._state_data(o.atoms, G.S[l][b], C, l))
            o.X = [G.Xm[l][b] for b in o.states]
            a = self.anchor[l]
            o.types = {"A": [a], "N": [b for b in o.states if b != a], "X": list(o.states)}
        o.merged = {}
        for t, sts in o.types.items():
            if not sts:
                continue
            o.merged[t] = dict(d=np.max([o.per_state[b]["d"] for b in sts], axis=0),
                               supB=np.max([o.per_state[b]["supB"] for b in sts], axis=0),
                               supL=np.max([o.per_state[b]["supL"] for b in sts], axis=0))
        return o

    # ------------------------------------------------------------------ kernel suprema
    def _supH_states(self, o1, b1, o2, b2):
        key = (o1.host, b1, o2.host, b2)
        if key not in self._hcache:
            X1, X2 = o1.X[b1], o2.X[b2]
            dd = X1[:, None, :] - X2[None, :, :]
            r = np.sqrt((dd * dd).sum(-1))
            same = (o1.host == o2.host)
            if same:
                r = r + np.eye(len(o1.atoms))
            s1, s2 = o1.per_state[b1], o2.per_state[b2]
            wlo = s1["elo"][:, None] + s2["elo"][None, :]
            whi = s1["ehi"][:, None] + s2["ehi"][None, :]
            out = np.zeros((self.K + 1,) + r.shape)
            for k in range(1, self.K + 1):
                out[k] = self.sup.sup_h(k, r, wlo, whi)
            self._hcache[key] = out
        return self._hcache[key]

    def supH(self, o1, t1, o2, t2):
        """(K+1, n1, n2): sup|h^(k)| maximised over the compatible host states of the two types."""
        best = None
        for b1 in o1.types[t1]:
            for b2 in o2.types[t2]:
                if o1.host is not None and o1.host == o2.host and b1 != b2:
                    continue
                v = self._supH_states(o1, b1, o2, b2)
                best = v if best is None else np.maximum(best, v)
        return best

    # ------------------------------------------------------------------ theta
    def _coef(self, o1, o2):
        c = KAPPA * np.abs(o1.q[:, None] * o2.q[None, :])
        if o1.host == o2.host:
            c = np.triu(c, 1)                    # unordered pairs p < q inside one group
        return c

    def theta(self, o1, t1, o2, t2, s, subset=None):
        """sum over free sets B of size s (or the single set `subset`) of the pair bound, kJ/mol."""
        if s < 1:
            raise ValueError("order of the free set must be >= 1")
        if t1 not in o1.merged or t2 not in o2.merged:
            return 0.0
        m1, m2 = o1.merged[t1], o2.merged[t2]
        d1, d2 = m1["d"].copy(), m2["d"].copy()
        if self._excl is not None:
            d1[self._excl] = 0.0; d2[self._excl] = 0.0
        for h in (o1.host, o2.host):
            if h is not None:
                d1[h] = 0.0; d2[h] = 0.0
        sH = self.supH(o1, t1, o2, t2)
        if sH is None:
            return 0.0
        coef = self._coef(o1, o2)
        if subset is not None:
            B = tuple(subset)
            assert len(B) == s
            tot = np.zeros(coef.shape)
            for part in set_partitions(B):
                term = sH[len(part)].copy()
                for block in part:
                    k = len(block)
                    term = term * ((m1["supL"][k] * np.prod(d1[list(block)], axis=0))[:, None]
                                   + (m2["supL"][k] * np.prod(d2[list(block)], axis=0))[None, :])
                tot += term
            return float((coef * tot).sum())
        e = esym2(d1, d2, s)
        B1 = bell_arrays(m1["supL"], s); B2 = bell_arrays(m2["supL"], s)
        tot = np.zeros(coef.shape)
        for a in range(s + 1):
            b = s - a
            M = np.zeros(coef.shape)
            for r1 in range(0, a + 1):
                if a > 0 and r1 == 0:
                    continue
                for r2 in range(0, b + 1):
                    if b > 0 and r2 == 0:
                        continue
                    M += sH[r1 + r2] * B1[a][r1][:, None] * B2[b][r2][None, :]
            tot += e[a][b] * M
        return float((coef * tot).sum())

    def self_sum(self, o, t, s, subset=None):
        """sum over free sets of size s of (KAPPA/2) sum_p q_p^2 sup|ib^(s)| prod delta, kJ/mol."""
        if s < 1:
            raise ValueError
        if t not in o.merged:
            return 0.0
        m = o.merged[t]
        dd = m["d"]
        if self._excl is not None:
            dd = dd.copy(); dd[self._excl] = 0.0
        if subset is not None:
            prod = np.prod(dd[list(subset)], axis=0)
        else:
            prod = esym1(dd, s)[s]
        return 0.5 * KAPPA * float((o.q ** 2 * m["supB"][s] * prod).sum())

    # ------------------------------------------------------------------ totals
    def site_penalties(self, m):
        """gamma_i = (1/m) sum_{T ni i, |T| = m} chat_T  (kcal/mol), so that for every set S of sites
        sum_{T subset S, |T| = m} chat_T <= sum_{i in S} gamma_i  (every T inside S is counted m times a m-th).
        Computed as (Gamma_m - Gamma_m without site i)/m by n + 1 generating-function evaluations."""
        tot = sum(self.total(m))
        gam = np.array([(tot - sum(self.total(m, exclude=i))) / m for i in range(self.G.ns)])
        return np.maximum(gam, 0.0) * RND, tot

    def total(self, m, T=None, exclude=None):
        """Gamma_m = sum over all T of order m of the term-by-term bound (kcal/mol); with T given: the bound
        chat_T of that single subset (same conventions; used to validate the generating functions); with
        exclude = i: the sum over the subsets that do not contain site i.
        Returns (self part, cross part)."""
        G = self.G
        ns = G.ns
        F = self.F
        self._excl = exclude

        def sub(hosts_in_T, hosts):
            """free subset for a pair whose hosts are `hosts`, or False if T is incompatible with the case."""
            if T is None:
                return None
            for h in hosts:
                if (h in T) != (h in hosts_in_T):
                    return False
            return tuple(i for i in T if i not in hosts)

        se = 0.0; cr = 0.0
        # fixed atoms
        B = sub((), ())
        se += self.self_sum(F, "F", m, B)
        cr += self.theta(F, "F", F, "F", m, B)
        for l in range(ns):
            o = self.site[l]
            # host l outside T
            B = sub((), (l,))
            if B is not False:
                se += self.self_sum(o, "X", m, B)
                cr += self.theta(F, "F", o, "X", m, B) + self.theta(o, "X", o, "X", m, B)
            # host l inside T
            B = sub((l,), (l,))
            if B is not False and m - 1 >= 1 and l != exclude:
                for t in ("A", "N"):
                    se += self.self_sum(o, t, m - 1, B)
                    cr += self.theta(F, "F", o, t, m - 1, B) + self.theta(o, t, o, t, m - 1, B)
            for l2 in range(l + 1, ns):
                o2 = self.site[l2]
                B = sub((), (l, l2))
                if B is not False:
                    cr += self.theta(o, "X", o2, "X", m, B)
                B = sub((l,), (l, l2))
                if B is not False and l != exclude:
                    cr += sum(self.theta(o, t, o2, "X", m - 1, B) for t in ("A", "N"))
                B = sub((l2,), (l, l2))
                if B is not False and l2 != exclude:
                    cr += sum(self.theta(o, "X", o2, t, m - 1, B) for t in ("A", "N"))
                B = sub((l, l2), (l, l2))
                if B is not False and m - 2 >= 1 and l != exclude and l2 != exclude:
                    cr += sum(self.theta(o, t, o2, t2, m - 2, B) for t in ("A", "N") for t2 in ("A", "N"))
        return se / KCAL * RND, cr / KCAL * RND
