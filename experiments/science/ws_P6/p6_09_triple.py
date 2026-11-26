"""
P6 extension (beyond the brief; see report section 5A): shares to the TRIPLES of each subset T, |T| = m >= 3.

Lemma A' (report):  for chat_T >= 0, H_ijk := sum_{T contains i,j,k} chat_T, eta_ijk := H_ijk / C(m,3), and a window w:
   sum_{T subset S} chat_T  <=  sum_{i<j<k} eta_ijk s_i s_j s_k                                    (charge C(t,3)/C(m,3))
                            <=  sum_{in-window i<j<k} eta_ijk s_i s_j s_k + sum_{a<b} rho_ab s_a s_b,
   rho_ab := (1/3) sum_{c: {a,b,c} NOT in window} eta_abc = [ (m-2) G_ab - sum_{c: {a,b,c} in window} H_abc ] / (3 C(m,3)),
(an out-of-window triple is charged through s_i s_j s_k <= (s_i s_j + s_i s_k + s_j s_k)/3; "in window": max - min <= w),
and the pair part is then banded as in Lemma A (out-of-band pairs in halves to their sites).
H_ijk by inclusion-exclusion from P3's closed form with one, two and three sites excluded (no subset enumerated).

The model needs three-site terms inside a window of w+1 consecutive sites: TripleBandModel (a subclass of P3's
BandModel; P3's transfer matrix already eliminates site i from an array over the sites i..i+w, so such terms are exact).

For enumerable domains: triple sums against explicit enumeration of subsets; |remainder| <= penalty; m_- <= E <= m_+ at
every state; the two extreme members of the certified class (as p6_06_adversarial.py) at every state.

usage: python3 -B p6_09_triple.py SEQ BB TAU --m 4,5 [--bands 8,4] [--noenum]
"""
import sys, os, time, math, json, itertools
import numpy as np
import p6lib as L
pw = L.pw
BETA = L.BETA
MAXSUB = 500


def opt(a, key, default, cast=str):
    return cast(a[a.index(key) + 1]) if key in a else default


class TripleBandModel(pw.BandModel):
    """P3's BandModel plus three-site tables tri[(i, j, k)], i < j < k <= i + w, attached to site i."""

    def __init__(self, k, w):
        super().__init__(k, w)
        self.tri = {}

    def add_triple(self, i, j, kk, tab):
        assert i < j < kk and kk - i <= self.w
        self.tri[(i, j, kk)] = self.tri.get((i, j, kk), 0.0) + tab

    def energy(self, st):
        st = np.atleast_2d(st)
        e = super().energy(st)
        for (i, j, kk), tab in self.tri.items():
            e += tab[st[:, i], st[:, j], st[:, kk]]
        return e

    def _A(self, i, msg, scale):
        A = super()._A(i, msg, scale)
        nax = A.ndim
        for (a, j, kk), tab in self.tri.items():
            if a == i:
                sh = [1] * nax
                sh[0] = self.k[i]; sh[j - i] = self.k[j]; sh[kk - i] = self.k[kk]
                A = A + scale * tab.reshape(sh)
        return A


def to_triple(mdl):
    t = TripleBandModel(mdl.k, mdl.w)
    t.const = mdl.const
    t.one = [np.array(o, dtype=float) for o in mdl.one]
    t.pair = dict(mdl.pair)
    return t


def diff_triple(lo, up):
    d = TripleBandModel(lo.k, lo.w)
    d.const = up.const - lo.const
    d.one = [up.one[i] - lo.one[i] for i in range(lo.n)]
    for key in set(lo.pair) | set(up.pair):
        d.pair[key] = up.pair.get(key, 0.0) - lo.pair.get(key, 0.0)
    for key in set(lo.tri) | set(up.tri):
        d.tri[key] = up.tri.get(key, 0.0) - lo.tri.get(key, 0.0)
    return d


def window_triples(n, w):
    return [(i, j, kk) for i in range(n) for j in range(i + 1, n) for kk in range(j + 1, min(n, i + w + 1))]


def triple_form(n, m, w, Gp, H, psi1, psi2, absG, absH):
    """(site part gs, in-band pair part g2, in-window triple part eta) of the banded triple penalty, with the pair
    allocation of the floating-point allowance (psi1, psi2).  H: dict (i,j,k) -> raw triple sum for the triples that
    are in the window w (it may contain more)."""
    c3 = math.comb(m, 3)
    eta = {}
    insum = np.zeros((n, n)); nin = np.zeros((n, n))
    for (i, j, kk) in window_triples(n, w):
        v = H[(i, j, kk)]
        eta[(i, j, kk)] = (max(v, 0.0) + absH) / c3 * L.RND
        for a, b in ((i, j), (i, kk), (j, kk)):
            insum[a, b] += v; insum[b, a] += v; nin[a, b] += 1; nin[b, a] += 1
    gs = psi1.copy(); g2 = np.zeros((n, n))
    for a in range(n):
        for b in range(n):
            if a == b:
                continue
            rho = (max((m - 2) * max(Gp[a, b], 0.0) - insum[a, b], 0.0) + (m - 2) * absG + nin[a, b] * absH) / (3.0 * c3) * L.RND
            if abs(a - b) <= w:
                g2[a, b] = rho + psi2[a, b]
            else:
                gs[a] += 0.5 * (rho + psi2[a, b])
    return gs, g2, eta


def penalty_value3(st, x0, gs, g2, eta):
    s = (np.atleast_2d(st) != np.asarray(x0)[None]).astype(float)
    out = s @ gs + 0.5 * np.einsum("ni,ij,nj->n", s, g2, s)
    for (i, j, kk), v in eta.items():
        out += v * s[:, i] * s[:, j] * s[:, kk]
    return out


def build_triple_models(k, x0, c0, h, J, d, w, M, gs, g2, eta):
    lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2)          # P3's model + site and in-band pair penalties
    lo, up = to_triple(lo), to_triple(up)
    for (i, j, kk), v in eta.items():
        si = np.ones(k[i]); si[x0[i]] = 0.0
        sj = np.ones(k[j]); sj[x0[j]] = 0.0
        sk = np.ones(k[kk]); sk[x0[kk]] = 0.0
        tab = v * si[:, None, None] * sj[None, :, None] * sk[None, None, :]
        lo.add_triple(i, j, kk, -tab)
        up.add_triple(i, j, kk, +tab)
    return lo, up


def main():
    a = sys.argv[1:]
    seq, bb, tau = a[0], a[1], float(a[2])
    orders = [int(v) for v in opt(a, "--m", "4").split(",")]
    t0 = time.time()
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau)
    n, k = G.ns, G.k
    size = float(np.prod([float(v) for v in k]))
    enum = size <= 3.0e6 and "--noenum" not in a
    bands_opt = opt(a, "--bands", None)
    bands = [int(v) for v in bands_opt.split(",")] if bands_opt else sorted({n - 1, 4, 2} & set(range(2, n)), reverse=True)
    W = max(bands)
    print(f"=== triple shares: {seq} on {bb}, tau {tau}: atoms {G.nat}, sites {n}, |X| = {size:.6g}; anchor E = {E0:.6f}; orders {orders}; bands {bands}; "
          f"enumeration {enum} [{time.time() - t0:.1f}s]", flush=True)
    res = dict(seq=seq, bb=bb, tau=tau, n=n, size=size, anchor=list(x0), bands=bands, enum=enum, orders={})
    sup = L.EnvelopeSup(G)
    if enum:
        st, g, src = L.enumerate_g(G, seq, bb, tau)
        E = pw.f_energy(st, c0, h, J) + g
        lnZE = float(np.log(np.exp(-BETA * (E - E.min())).sum()) - BETA * E.min())
        sx = (st != np.array(x0)[None]); nch = sx.sum(1)
        print(f"    enumeration: {len(st)} states ({src}); ln Z(E) = {lnZE:.6f}", flush=True)
        res.update(lnZ_E=lnZE)
    nchk = nviol = nadv = nadv_viol = 0
    for m in orders:
        M = m - 1
        GF = L.GFBound2(G, x0, sup, K=m)
        Gam, S, Gp, srcp = L.load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, "gbn2", m, verbose=(n > 24), maxall=10 ** 6)   # ALL pair sums
        assert np.isfinite(Gp[~np.eye(n, dtype=bool)]).all(), "all pair sums are needed"
        z = np.load(os.path.join(L.HERE, "out", f"pairsums_{L.tagname(seq, bb, tau)}_m{m}.npz"))
        val = {tuple(int(v) for v in e if v >= 0): float(t) for e, t in zip(z["excl"], z["tot"])}
        t1 = time.time()
        tris = window_triples(n, W)
        se, cr = L.GFBatch(GF).totals(m, tris)
        H = {}
        for (i, j, kk), t3 in zip(tris, se + cr):
            H[(i, j, kk)] = (val[()] - val[(i,)] - val[(j,)] - val[(kk,)] + val[(i, j)] + val[(i, kk)] + val[(j, kk)]) - float(t3)
        absG = 5e-9 * Gam; absH = 1e-8 * Gam
        c3 = math.comb(m, 3)
        print(f"  -- m = {m}: Gamma_{m} = {Gam:.6e} kcal/mol; {len(tris)} in-window triple sums (window {W}) by the closed form with three excluded sites "
              f"[{time.time() - t1:.1f}s]; max H_ijk/C(m,3) = {max(H.values()) / c3:.4e}; sum over in-window triples / C(m,3) = {sum(H.values()) / c3:.6e} "
              f"({100 * sum(H.values()) / c3 / Gam:.2f} % of Gamma)", flush=True)
        R = dict(m=m, Gamma=Gam, n_triples=len(tris), in_window_share=sum(H.values()) / c3 / Gam, bands={})
        d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
        R["nball"] = int(nball)
        phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
        chat = None
        if enum and math.comb(n, m) <= MAXSUB:
            chat = L.enum_chat(GF, m)
            He = {}
            for T, v in chat.items():
                for tr in itertools.combinations(T, 3):
                    He[tr] = He.get(tr, 0.0) + v
            dH = max(abs(H[tr] - He.get(tr, 0.0)) for tr in tris)
            R["triple_check"] = dict(n_subsets=len(chat), n_triples=len(tris), dH_max=dH, rel=dH / Gam)
            print(f"     triple sums vs EXPLICIT ENUMERATION of {len(chat)} subsets: max |H_ijk - enum| = {dH:.2e} kcal/mol over {len(tris)} triples (relative to Gamma {dH / Gam:.1e})", flush=True)
            assert dH <= 1e-9 * Gam
            env = L.envelope_value(st, x0, chat)
            act = np.array([kk > 1 for kk in k])
            fpx = L.EPS_G * np.array([sum(math.comb(t, j) * 2 ** j for j in range(0, min(t, M) + 1)) for t in range(n + 1)])[(sx & act[None]).sum(1)]
            Itil = pw.expansion_value(d, st)
            fb = pw.f_energy(st, c0, h, J)
            Elow, Ehigh = fb + Itil - env - fpx, fb + Itil + env + fpx
        if enum:
            rem = g - pw.expansion_value(d, st)
        for w in bands:
            RW = {}
            gsS = L.site_form(n, m, S, phi1)
            gsB, g2B = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absG)
            gsT, g2T, eta = triple_form(n, m, w, Gp, H, psi1, psi2, absG, absH)
            if enum:
                z1 = np.zeros(n); z2 = np.zeros((n, n))
                g0, g20, eta0 = triple_form(n, m, w, Gp, H, z1, z2, 0.0, 0.0)
                pT = penalty_value3(st, x0, g0, g20, eta0)
                gb0, g2b0 = L.banded_pair_form(n, m, w, S, Gp, z1, z2, 0.0)
                pB = L.penalty_value(st, x0, gb0, g2b0)
                vr = int((np.abs(rem) > pT + 1e-9).sum())
                tol = 3e-9 * max(Gam, 1.0)
                RW["triple_le_pair"] = bool((pT <= pB + tol).all())
                RW["env_le_triple"] = bool((env <= pT + tol).all()) if chat is not None else None
                big = (nch >= m) & (np.abs(rem) > 1e-9)
                rat = pT[big] / np.abs(rem[big]) if big.any() else np.array([np.nan])
                RW["remainder"] = dict(viol=vr, ratio_min=float(rat.min()), ratio_max=float(rat.max()))
                nchk += len(st); nviol += vr
                assert RW["triple_le_pair"] and RW["env_le_triple"] is not False
            for form in ("S", "B", "T"):
                t1 = time.time()
                if form == "T":
                    lo, up = build_triple_models(k, x0, c0, h, J, d, w, M, gsT, g2T, eta)
                    diff = diff_triple(lo, up)
                else:
                    gs, g2 = (gsS, np.zeros((n, n))) if form == "S" else (gsB, g2B)
                    lo, up = L.build_models(k, x0, c0, h, J, d, w, M, gs, g2)
                    diff = L.diff_model(lo, up)
                lnZlo, lnZup = lo.lnZ(), up.lnZ()
                F = dict(lnZ_lo=lnZlo, lnZ_up=lnZup, width=lnZlo - lnZup, min_lo=lo.minimum(), rho_cert=diff.maximum())
                msg = f"     w = {w:2d} form {form}: ln Z(m_-) = {lnZlo:.6f}, ln Z(m_+) = {lnZup:.6f}, width {lnZlo - lnZup:.6f} nats; min m_- = {F['min_lo']:.6f}"
                if enum:
                    ml, mu = lo.energy(st), up.energy(st)
                    v9 = int((ml > E + 1e-9).sum()) + int((mu < E - 1e-9).sum())
                    lz = float(np.log(np.exp(-BETA * (ml - ml.min())).sum()) - BETA * ml.min())
                    F.update(viol=v9, dp_vs_enum=abs(lz - lnZlo), truth_inside=bool(lnZup <= lnZE <= lnZlo), states=int(len(st)))
                    nchk += 2 * len(st); nviol += v9
                    msg += f" | ENUM {len(st)} states: violations of m_- <= E <= m_+: {v9}; |DP - enum| = {F['dp_vs_enum']:.1e}; truth inside: {F['truth_inside']}"
                    if chat is not None:
                        va = int((ml > Elow + 1e-10).sum()) + int((mu < Ehigh - 1e-10).sum())
                        F.update(adv_viol=va, adv_slack=float(min((Elow - ml).min(), (mu - Ehigh).min())))
                        nadv += 2 * len(st); nadv_viol += va
                        msg += f"; EXTREME MEMBERS of the class: violations {va}, smallest slack {F['adv_slack']:.1e}"
                RW[form] = F
                print(msg + f" [{time.time() - t1:.1f}s]", flush=True)
            if enum:
                print(f"     w = {w:2d}: |remainder| <= triple penalty: violations {RW['remainder']['viol']}, ratio min {RW['remainder']['ratio_min']:.3g}; "
                      f"pointwise envelope <= triple: {RW['env_le_triple']}; triple <= banded pair: {RW['triple_le_pair']}", flush=True)
            R["bands"][str(w)] = RW
        res["orders"][str(m)] = R
    res.update(checks=nchk, violations=nviol, adv_checks=nadv, adv_violations=nadv_viol, seconds=time.time() - t0)
    json.dump(res, open(os.path.join(L.HERE, "out", f"triple_{L.tagname(seq, bb, tau)}.json"), "w"), indent=1)
    print(f"    checks with the real energy and of |remainder| <= penalty: {nchk}, violations {nviol}; checks of the extreme members: {nadv}, violations {nadv_viol}")
    print(f"DONE p6_09_triple {seq} {bb} {tau} [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
