"""
Workstream P8 -- sharper computable forms of P3's term-by-term bound, per subset T of sites.

P3's Theorem 3 is a statement per host state.  For a pair of atoms p, q with hosts h1, h2 (0, 1 or 2 hosts; two atoms
of one side chain share the host and its state), a set T (|T| = m >= 3), a context z and states y_T (anchored: z_T = x0_T):

    |Delta_T t_pq(z; y_T)|  <=  sum_{c1 in St1} sum_{c2 in St2} theta_pq^{(c1, c2)}(T \\ hosts),
        St_i = {z_{h_i}}             if h_i is not in T          (one state: the context's),
        St_i = {x0_{h_i}, y_{h_i}}   if h_i is in T              (two states: anchor and the other one),

where theta^{(c1, c2)}(B) is built from ingredients of THOSE host states: the deviations delta_i of the descreening
contributions of the free sites i in B, sup|ell^(k)| over the hull of I at that host state, sup|d^k h/dw^k| at the pair's
distance in those states over the hull of ell_p + ell_q (self terms: sup|b^(k)| and delta).

Four computable forms ("variants") of the constant of a subset T are evaluated here from the SAME rigorous ingredients
(P3's GFBound: per_state data, merged data, _supH_states, supH; enclosures, PAD_TAB and the final factor RND unchanged):

  'P3'  P3's own: host outside T -> every ingredient maximised over all states of the host (type X);
        host in T -> anchor state (type A) + ingredients maximised over the non-anchor states (type N).
        Reproduces gfbound.GFBound.total(m, T)  (asserted by the drivers).
  'S'   STATE-RESOLVED (Proposition S): the maximum over host states is taken of the BOUND, pair by pair:
        host outside T -> max over all its states b of the bound at b;
        host in T      -> max over the non-anchor states b of [bound at the anchor + bound at b]  (jointly for two hosts).
        chat^S_T >= c_T^anch(g), and chat^S_T <= chat^P3_T summand by summand.
  'AH'  ANCHORED HOSTS, P3's types (Theorem AH): host outside T -> anchor state only (type A); host in T -> A + N (merged).
        Has a closed form over all T (AHBound.total_ah).
  'SA'  both: host outside T -> anchor state; host in T -> max over b of [anchor + b].
  'AH' and 'SA' do NOT bound the anchored constants c_T^anch (all contexts); they bound the mixed differences that occur
  in the remainder identity when the hosts of each pair are ordered last (P8_REPORT.md, Theorem AH), so that
        |g(x) - I_{m-1} g(x)| <= sum_{T subset S(x), |T| = m} chat_T      holds for all four variants.

Units: kcal/mol.
"""
import numpy as np
from p8lib import *

VARIANTS = ("P3", "S", "AH", "SA")


def hom2(xs, ys):
    """c[a], a = 0..s: coefficient of u^a v^(s-a) in prod_{i=1..s} (u xs[i] + v ys[i]) (broadcastable arrays):
    the sum over the splittings of the s sites into a sites taken with x and s - a sites taken with y."""
    c = [1.0]
    for x, y in zip(xs, ys):
        new = [None] * (len(c) + 1)
        for a in range(len(c) + 1):
            v = 0.0
            if a > 0:
                v = v + x * c[a - 1]
            if a < len(c):
                v = v + y * c[a]
            new[a] = v
        c = new
    return c


class SRBound(GFDecomp):
    """P3's GFBound (through GFDecomp) plus per-subset bounds in the four variants."""

    # ------------------------------------------------------------------ ingredient stacks
    def _stack(self, o):
        """per-state ingredients stacked over the host states: d (k, ns, na), supL (k, K+1, na), supB (k, K+1, na);
        and the merged pseudo-states of P3's types, in the order of o._types: A, N, X (fixed atoms: F)."""
        if not hasattr(o, "_sr"):
            o._types = [t for t in ("F", "A", "N", "X") if t in o.merged]
            o._sr = dict(d=np.stack([s["d"] for s in o.per_state]), supL=np.stack([s["supL"] for s in o.per_state]),
                         supB=np.stack([s["supB"] for s in o.per_state]),
                         md=np.stack([o.merged[t]["d"] for t in o._types]), mL=np.stack([o.merged[t]["supL"] for t in o._types]),
                         mB=np.stack([o.merged[t]["supB"] for t in o._types]))
        return o._sr

    def _Hstack(self, o1, o2):
        """sup|d^k h/dw^k| for all pairs of host states (K+1, k1, k2, n1, n2) [same host: (K+1, k, n, n)], and for P3's
        type pairs (K+1, t1, t2, n1, n2) [same host: (K+1, t, n, n), equal types]."""
        key = (o1.host, o2.host)
        if not hasattr(self, "_Hs"):
            self._Hs = {}
        if key not in self._Hs:
            self._stack(o1); self._stack(o2)
            same = o1.host is not None and o1.host == o2.host
            if same:
                st = np.stack([self._supH_states(o1, b, o2, b) for b in range(len(o1.states))], axis=1)
                ty = np.stack([self.supH(o1, t, o2, t) for t in o1._types], axis=1)
            else:
                st = np.stack([np.stack([self._supH_states(o1, b1, o2, b2) for b2 in range(len(o2.states))], axis=1)
                               for b1 in range(len(o1.states))], axis=1)
                ty = np.stack([np.stack([self.supH(o1, t1, o2, t2) for t2 in o2._types], axis=1) for t1 in o1._types], axis=1)
            self._Hs[key] = (st, ty)
        return self._Hs[key]

    def _M(self, o1, o2, s, typed):
        """M[a] (a = 0..s; b = s - a) = sum_{r1, r2} H_{r1+r2} Bell_{a,r1}(L^p) Bell_{b,r2}(L^q), over the (pseudo-)state
        pairs of the block; independent of the subset.  Cached."""
        key = (o1.host, o2.host, s, typed)
        if not hasattr(self, "_Mc"):
            self._Mc = {}
        if key not in self._Mc:
            s1, s2 = self._stack(o1), self._stack(o2)
            H = self._Hstack(o1, o2)[1 if typed else 0]
            same = o1.host is not None and o1.host == o2.host
            La, Lb = (s1["mL"], s2["mL"]) if typed else (s1["supL"], s2["supL"])
            if same:
                L1 = [La[:, k, :, None] for k in range(self.K + 1)]; L2 = [Lb[:, k, None, :] for k in range(self.K + 1)]
            else:
                L1 = [La[:, None, k, :, None] for k in range(self.K + 1)]; L2 = [Lb[None, :, k, None, :] for k in range(self.K + 1)]
            B1 = bell_arrays(L1, s); B2 = bell_arrays(L2, s)
            out = []
            for a in range(s + 1):
                b = s - a
                M = 0.0
                for r1 in range(0, a + 1):
                    if a > 0 and r1 == 0:
                        continue
                    for r2 in range(0, b + 1):
                        if b > 0 and r2 == 0:
                            continue
                        M = M + H[r1 + r2] * B1[a][r1] * B2[b][r2]
                out.append(np.ascontiguousarray(M))
            self._Mc[key] = out
        return self._Mc[key]

    def _theta(self, o1, o2, B, typed):
        """theta for the free set B for all (pseudo-)state pairs of the block: (k1, k2, n1, n2) or (k, n, n) for a shared
        host; kJ/mol without the factor KAPPA |q_p q_q|.  B contains neither host."""
        s = len(B)
        s1, s2 = self._stack(o1), self._stack(o2)
        same = o1.host is not None and o1.host == o2.host
        Da, Db = (s1["md"], s2["md"]) if typed else (s1["d"], s2["d"])
        if same:
            xs = [Da[:, i, :, None] for i in B]; ys = [Db[:, i, None, :] for i in B]
        else:
            xs = [Da[:, None, i, :, None] for i in B]; ys = [Db[None, :, i, None, :] for i in B]
        c = hom2(xs, ys)
        M = self._M(o1, o2, s, typed)
        tot = 0.0
        for a in range(s + 1):
            tot = tot + c[a] * M[a]
        return tot

    # ------------------------------------------------------------------ combination over host states
    def _comb1(self, per, typ, o, inT):
        """one host.  per: array (k, ...) over the host states; typ: array (types, ...) over o._types.
        Returns dict variant -> array (...)."""
        if o.host is None:
            v = per[0]
            return dict(P3=typ[0], S=v, AH=typ[0], SA=v)
        a = self.anchor[o.host]
        tA = o._types.index("A"); tX = o._types.index("X")
        if not inT:
            return dict(P3=typ[tX], S=per.max(axis=0), AH=typ[tA], SA=per[a])
        if "N" not in o._types:                               # a one-state site cannot be in T (no mixed difference)
            z = np.zeros(per.shape[1:])
            return dict(P3=typ[tA], S=z, AH=typ[tA], SA=z)
        tN = o._types.index("N")
        rest = np.delete(per, a, axis=0)
        s_ = per[a] + rest.max(axis=0)
        p3 = typ[tA] + typ[tN]
        return dict(P3=p3, S=s_, AH=p3, SA=s_)

    def _comb2(self, per, typ, o1, o2, in1, in2):
        """two different hosts.  per (k1, k2, ...), typ (t1, t2, ...)."""
        a1, a2 = self.anchor[o1.host], self.anchor[o2.host]
        A1, X1 = o1._types.index("A"), o1._types.index("X"); A2, X2 = o2._types.index("A"), o2._types.index("X")
        N1 = o1._types.index("N") if "N" in o1._types else None; N2 = o2._types.index("N") if "N" in o2._types else None
        tail = per.shape[2:]
        z = np.zeros(tail)
        if not in1 and not in2:
            return dict(P3=typ[X1, X2], S=per.reshape((-1,) + tail).max(axis=0), AH=typ[A1, A2], SA=per[a1, a2])
        if in1 and not in2:
            if N1 is None:
                return dict(P3=typ[A1, X2], S=z, AH=typ[A1, A2], SA=z)
            rest = np.delete(per, a1, axis=0)                               # (k1 - 1, k2, ...)
            both = per[a1][None] + rest                                     # anchor + b1, for every state b2 of the outside host
            return dict(P3=typ[A1, X2] + typ[N1, X2], S=both.reshape((-1,) + tail).max(axis=0),
                        AH=typ[A1, A2] + typ[N1, A2], SA=both[:, a2].max(axis=0))
        if in2 and not in1:
            if N2 is None:
                return dict(P3=typ[X1, A2], S=z, AH=typ[A1, A2], SA=z)
            rest = np.delete(per, a2, axis=1)                               # (k1, k2 - 1, ...)
            both = per[:, a2][:, None] + rest
            return dict(P3=typ[X1, A2] + typ[X1, N2], S=both.reshape((-1,) + tail).max(axis=0),
                        AH=typ[A1, A2] + typ[A1, N2], SA=both[a1].max(axis=0))
        if N1 is None or N2 is None:
            return dict(P3=typ[A1, A2], S=z, AH=typ[A1, A2], SA=z)
        r1 = np.delete(per, a1, axis=0)                                     # (k1 - 1, k2, ...)
        r12 = np.delete(r1, a2, axis=1)                                     # (k1 - 1, k2 - 1, ...)
        four = per[a1, a2][None, None] + np.delete(per[a1], a2, axis=0)[None, :] + r1[:, a2][:, None] + r12
        s_ = four.reshape((-1,) + tail).max(axis=0)
        p3 = typ[A1, A2] + typ[A1, N2] + typ[N1, A2] + typ[N1, N2]
        return dict(P3=p3, S=s_, AH=p3, SA=s_)

    # ------------------------------------------------------------------ the bound of one subset
    def total_T(self, m, T, decomp=False, variants=VARIANTS):
        """dict variant -> (self part, cross part) in kcal/mol for the subset T (|T| = m);
        with decomp=True: dict variant -> (self part, cross part, self vector (N,), symmetric pair matrix (N, N))."""
        T = [int(i) for i in T]
        assert len(T) == m and len(set(T)) == m and m <= self.K
        G = self.G
        ns = G.ns; N = G.nat
        Tset = set(T)
        F = self.F
        sv = {v: np.zeros(N) for v in variants}
        pm = {v: np.zeros((N, N)) for v in variants} if decomp else None
        cr = {v: 0.0 for v in variants}

        def add_pair(o1, o2, res, coef, tri=False):
            for v in variants:
                blk = coef * res[v]
                if tri:
                    blk = np.triu(blk, 1)
                cr[v] += float(blk.sum())
                if decomp:
                    pm[v][np.ix_(o1.atoms, o2.atoms)] += blk

        def self_arr(o, B, typed):
            st_ = self._stack(o)
            d, sb = (st_["md"], st_["mB"]) if typed else (st_["d"], st_["supB"])
            return 0.5 * KAPPA * (o.q ** 2)[None, :] * sb[:, len(B), :] * np.prod(d[:, list(B), :], axis=1)

        # self terms
        res = self._comb1(self_arr(F, T, False), self_arr(F, T, True), F, False)
        for v in variants:
            sv[v][F.atoms] += res[v]
        for l in range(ns):
            o = self.site[l]
            B = [i for i in T if i != l]
            res = self._comb1(self_arr(o, B, False), self_arr(o, B, True), o, l in Tset)
            for v in variants:
                sv[v][o.atoms] += res[v]
        # cross terms
        per = self._theta(F, F, T, False)[0, 0]; typ = self._theta(F, F, T, True)[0, 0]
        add_pair(F, F, dict(P3=typ, S=per, AH=typ, SA=per), KAPPA * np.abs(F.q[:, None] * F.q[None, :]), tri=True)
        for l in range(ns):
            o = self.site[l]
            inl = l in Tset
            B = [i for i in T if i != l]
            res = self._comb1(self._theta(F, o, B, False)[0], self._theta(F, o, B, True)[0], o, inl)
            add_pair(F, o, res, KAPPA * np.abs(F.q[:, None] * o.q[None, :]))
            res = self._comb1(self._theta(o, o, B, False), self._theta(o, o, B, True), o, inl)
            add_pair(o, o, res, KAPPA * np.abs(o.q[:, None] * o.q[None, :]), tri=True)
            for l2 in range(l + 1, ns):
                o2 = self.site[l2]
                B2 = [i for i in T if i != l and i != l2]
                res = self._comb2(self._theta(o, o2, B2, False), self._theta(o, o2, B2, True), o, o2, inl, l2 in Tset)
                add_pair(o, o2, res, KAPPA * np.abs(o.q[:, None] * o2.q[None, :]))
        out = {}
        for v in variants:
            se_ = float(sv[v].sum()) / KCAL * RND; cr_ = cr[v] / KCAL * RND
            if decomp:
                p_ = pm[v] / KCAL * RND
                out[v] = (se_, cr_, sv[v] / KCAL * RND, p_ + p_.T)
            else:
                out[v] = (se_, cr_)
        return out


class BlockBound(SRBound):
    """The state-wise maximum taken BLOCK BY BLOCK -- P3's own per-subset form (termwise.TermBound, P3 report 2.3, first
    bullet), here in anchored mode and vectorised.  All terms of a block share their host states, so the bound of the
    block at given host states is the SUM of its per-state summands, and the maximum over the host states is taken of
    that sum (never larger than the sum of the pair-wise maxima of variants 'S' / 'SA').  Blocks, as in P3's termwise:
        ('self', l)        self terms of the atoms of side chain l                    (l = -1: fixed atoms)
        ('cross1', l)      pairs fixed atom -- atom of l and pairs inside l           (l = -1: pairs of fixed atoms)
        ('cross2', l, l2)  pairs between the side chains l < l2
    Variants:  'Sb'  host outside T -> max over all its states; host in T -> max over b of [anchor + b]   (bounds c_T^anch)
               'SAb' host outside T -> anchor state;            host in T -> the same                      (Theorem AH)"""

    def _c1(self, v, host, inT, anchored):
        """v: (k,) block sums over the states of one host."""
        if host is None:
            return float(v[0])
        a = self.anchor[host]
        if not inT:
            return float(v[a]) if anchored else float(v.max())
        if len(v) < 2:
            return 0.0
        return float(v[a] + np.delete(v, a).max())

    def _c2(self, W, l, l2, in1, in2, anchored):
        """W: (k1, k2) block sums over the states of two hosts."""
        a1, a2 = self.anchor[l], self.anchor[l2]
        k1, k2 = W.shape
        if not in1 and not in2:
            return float(W[a1, a2]) if anchored else float(W.max())
        if in1 and not in2:
            if k1 < 2:
                return 0.0
            both = W[a1][None, :] + np.delete(W, a1, axis=0)               # (k1 - 1, k2)
            return float(both[:, a2].max()) if anchored else float(both.max())
        if in2 and not in1:
            if k2 < 2:
                return 0.0
            both = W[:, a2][:, None] + np.delete(W, a2, axis=1)            # (k1, k2 - 1)
            return float(both[a1].max()) if anchored else float(both.max())
        if k1 < 2 or k2 < 2:
            return 0.0
        r1 = np.delete(W, a1, axis=0)
        four = W[a1, a2] + np.delete(W[a1], a2)[None, :] + r1[:, a2][:, None] + np.delete(r1, a2, axis=1)
        return float(four.max())

    def total_T_blocks(self, m, T):
        """dict variant ('Sb', 'SAb') -> dict block key -> bound of the block for the subset T (kcal/mol, factor RND)."""
        T = [int(i) for i in T]
        assert len(T) == m and len(set(T)) == m and m <= self.K
        G = self.G
        ns = G.ns
        Tset = set(T)
        F = self.F
        out = {"Sb": {}, "SAb": {}}
        sc = RND / KCAL

        def put(key, v, host=None, inT=False, W=None, hosts=None, ins=None):
            for name, anch in (("Sb", False), ("SAb", True)):
                if W is None:
                    out[name][key] = self._c1(v, host, inT, anch) * sc
                else:
                    out[name][key] = self._c2(W, hosts[0], hosts[1], ins[0], ins[1], anch) * sc

        def self_sum_states(o, B):
            st_ = self._stack(o)
            return (0.5 * KAPPA * (o.q ** 2)[None, :] * st_["supB"][:, len(B), :] * np.prod(st_["d"][:, list(B), :], axis=1)).sum(axis=1)

        put(("self", -1), self_sum_states(F, T))
        cFF = np.triu(KAPPA * np.abs(F.q[:, None] * F.q[None, :]), 1)
        put(("cross1", -1), np.array([float((cFF * self._theta(F, F, T, False)[0, 0]).sum())]))
        for l in range(ns):
            o = self.site[l]
            inl = l in Tset
            B = [i for i in T if i != l]
            put(("self", l), self_sum_states(o, B), host=l, inT=inl)
            v = (KAPPA * np.abs(F.q[:, None] * o.q[None, :])[None] * self._theta(F, o, B, False)[0]).sum(axis=(1, 2)) \
                + (np.triu(KAPPA * np.abs(o.q[:, None] * o.q[None, :]), 1)[None] * self._theta(o, o, B, False)).sum(axis=(1, 2))
            put(("cross1", l), v, host=l, inT=inl)
            for l2 in range(l + 1, ns):
                o2 = self.site[l2]
                B2 = [i for i in T if i != l and i != l2]
                W = (KAPPA * np.abs(o.q[:, None] * o2.q[None, :])[None, None] * self._theta(o, o2, B2, False)).sum(axis=(2, 3))
                put(("cross2", l, l2), None, W=W, hosts=(l, l2), ins=(inl, l2 in Tset))
        return out


class AHBound(BlockBound):
    """ANCHORED HOSTS, closed form over all subsets: gfbound.GFBound.total with the type of a host OUTSIDE T changed from
    "X" to "A" -- a line-by-line copy of P3's `total` with that one change (variant 'AH' summed over all T; asserted equal
    to the sum of total_T(...)['AH'] on the enumerated instances)."""

    def total_ah(self, m, T=None, exclude=None):
        G = self.G
        ns = G.ns
        F = self.F
        self._excl = exclude

        def sub(hosts_in_T, hosts):
            if T is None:
                return None
            for h in hosts:
                if (h in T) != (h in hosts_in_T):
                    return False
            return tuple(i for i in T if i not in hosts)

        se = 0.0; cr = 0.0
        B = sub((), ())
        se += self.self_sum(F, "F", m, B)
        cr += self.theta(F, "F", F, "F", m, B)
        for l in range(ns):
            o = self.site[l]
            B = sub((), (l,))
            if B is not False:
                se += self.self_sum(o, "A", m, B)
                cr += self.theta(F, "F", o, "A", m, B) + self.theta(o, "A", o, "A", m, B)
            B = sub((l,), (l,))
            if B is not False and m - 1 >= 1 and l != exclude:
                for t in ("A", "N"):
                    se += self.self_sum(o, t, m - 1, B)
                    cr += self.theta(F, "F", o, t, m - 1, B) + self.theta(o, t, o, t, m - 1, B)
            for l2 in range(l + 1, ns):
                o2 = self.site[l2]
                B = sub((), (l, l2))
                if B is not False:
                    cr += self.theta(o, "A", o2, "A", m, B)
                B = sub((l,), (l, l2))
                if B is not False and l != exclude:
                    cr += sum(self.theta(o, t, o2, "A", m - 1, B) for t in ("A", "N"))
                B = sub((l2,), (l, l2))
                if B is not False and l2 != exclude:
                    cr += sum(self.theta(o, "A", o2, t, m - 1, B) for t in ("A", "N"))
                B = sub((l, l2), (l, l2))
                if B is not False and m - 2 >= 1 and l != exclude and l2 != exclude:
                    cr += sum(self.theta(o, t, o2, t2, m - 2, B) for t in ("A", "N") for t2 in ("A", "N"))
        self._excl = None
        return se / KCAL * RND, cr / KCAL * RND
