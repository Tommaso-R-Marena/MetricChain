"""
Workstream P6 -- library: pair sums of P3's certified tail constants without enumerating subsets,
and the banded pair form of P3's certified sandwich (floor and ceiling).

What is whose
-------------
* P3's code is IMPORTED READ-ONLY and unchanged (ws_P3: p3core.GBModel, encl.EnvelopeSup,
  gfbound.GFBound, pwmodel.*).  Nothing is written into ws_P3 (sys.dont_write_bytecode; the
  enclosure cache is redirected to ws_P6/cache, pre-filled with copies of P3's cached tables, as
  workstream P4 did).
* Mine: GFBound2.total_ex (P3's `total` with a SET of excluded sites: a line-by-line copy of P3's
  loop with `l != exclude` replaced by `l not in excl`), GFBatch (the same closed form evaluated
  for a batch of exclusion sets at once), pair_sums, the penalty allocations, build_models
  (P3's pwmodel.build_band_models called unchanged for everything except the in-band pair
  penalties, which are then added to the in-band pair tables).

Units: kcal/mol.
"""
import sys, os, glob, shutil, itertools, math, time, hashlib, json
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
P3 = os.path.normpath(os.path.join(HERE, "..", "ws_P3"))
if P3 not in sys.path:
    sys.path.insert(0, P3)
import numpy as np
import encl                                   # P3 (read-only)
MYCACHE = os.path.join(HERE, "cache")
os.makedirs(MYCACHE, exist_ok=True)
for _fn in glob.glob(os.path.join(P3, "cache", "atom_*.npz")) + glob.glob(os.path.join(P3, "cache", "zeta_*.npz")):
    _dst = os.path.join(MYCACHE, os.path.basename(_fn))
    if not os.path.exists(_dst):
        shutil.copy(_fn, _dst)
encl.CACHE = MYCACHE
from p3core import GBModel, KT300, BETA, KAPPA, KCAL     # P3 (read-only)
from encl import EnvelopeSup                              # P3 (read-only)
from gfbound import GFBound, RND, bell_arrays             # P3 (read-only)
import pwmodel as pw                                      # P3 (read-only)

EPS_G = 1e-7          # kcal/mol: P3's allowance for one evaluated value of g (run_floor.EPS_G)
REL_GF = 1e-9         # P3's claim (report 2.6): a generating-function sum of non-negative doubles is within 1e-9 relative
                      # of the real sum; P3 multiplies every such sum by RND = 1 + 1e-9


# ============================================================================= pair sums, simple form
class GFBound2(GFBound):
    """P3's GFBound with `total_ex`: the sum of chat_T over all T of order m that avoid a SET of sites."""

    def total_ex(self, m, excl=()):
        ex = sorted(set(int(i) for i in excl))
        exs = set(ex)
        G = self.G
        ns = G.ns
        F = self.F
        self._excl = ex if ex else None          # P3's theta / self_sum zero the delta rows d[self._excl]
        se = 0.0; cr = 0.0
        se += self.self_sum(F, "F", m, None)
        cr += self.theta(F, "F", F, "F", m, None)
        for l in range(ns):
            o = self.site[l]
            se += self.self_sum(o, "X", m, None)                                   # host l outside T
            cr += self.theta(F, "F", o, "X", m, None) + self.theta(o, "X", o, "X", m, None)
            if m - 1 >= 1 and l not in exs:                                        # host l inside T
                for t in ("A", "N"):
                    se += self.self_sum(o, t, m - 1, None)
                    cr += self.theta(F, "F", o, t, m - 1, None) + self.theta(o, t, o, t, m - 1, None)
            for l2 in range(l + 1, ns):
                o2 = self.site[l2]
                cr += self.theta(o, "X", o2, "X", m, None)
                if l not in exs:
                    cr += sum(self.theta(o, t, o2, "X", m - 1, None) for t in ("A", "N"))
                if l2 not in exs:
                    cr += sum(self.theta(o, "X", o2, t, m - 1, None) for t in ("A", "N"))
                if m - 2 >= 1 and l not in exs and l2 not in exs:
                    cr += sum(self.theta(o, t, o2, t2, m - 2, None) for t in ("A", "N") for t2 in ("A", "N"))
        self._excl = None
        return se / KCAL * RND, cr / KCAL * RND


# ============================================================================= pair sums, batched form
def _esym2_batch(dP, dQ, s):
    """dP (nb, ns, nP), dQ (nb, ns, nQ): e[a][b] (nb, nP, nQ), a + b <= s, coefficient of u^a v^b in
    prod_i (1 + u dP[:, i, p] + v dQ[:, i, q]) -- P3's esym2 with a leading batch axis."""
    nb, ns, nP = dP.shape
    nQ = dQ.shape[2]
    e = [[None] * (s + 1) for _ in range(s + 1)]
    for a in range(s + 1):
        for b in range(s + 1 - a):
            e[a][b] = np.zeros((nb, nP, nQ))
    e[0][0] += 1.0
    for i in range(ns):
        x = dP[:, i, :, None]; y = dQ[:, i, None, :]
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


class GFBatch:
    """The closed form of P3's Proposition 4 (gfbound.GFBound.total) evaluated for a batch of exclusion sets:
    out[b] = sum over all T of order m with T disjoint from excl[b] of chat_T  (self part, cross part).
    Uses the instances, merged ingredients and kernel suprema of a P3 GFBound object unchanged; only the
    summation over free sets carries a batch axis.  Chunked so that no array exceeds `maxel` elements."""

    def __init__(self, GF, maxel=2.0e6):
        self.GF = GF
        self.maxel = maxel

    def _weights(self, o1, t1, o2, t2, s):
        """W[a] (nP, nQ) for a = 0..s (b = s - a): coef * sum_{r1, r2} sup|h^(r1+r2)| Bell_{a,r1}(L^p) Bell_{b,r2}(L^q)."""
        GF = self.GF
        m1, m2 = o1.merged[t1], o2.merged[t2]
        sH = GF.supH(o1, t1, o2, t2)
        if sH is None:
            return None
        coef = GF._coef(o1, o2)
        B1 = bell_arrays(m1["supL"], s); B2 = bell_arrays(m2["supL"], s)
        W = []
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
            W.append(coef * M)
        return W

    def theta(self, o1, t1, o2, t2, s, mask):
        """mask (nb, ns) of 0/1 factors on the delta rows (0 = site excluded).  Returns (nb,) kJ/mol."""
        nb = mask.shape[0]
        if s < 1 or t1 not in o1.merged or t2 not in o2.merged:
            return np.zeros(nb)
        W = self._weights(o1, t1, o2, t2, s)
        if W is None:
            return np.zeros(nb)
        d1 = o1.merged[t1]["d"].copy(); d2 = o2.merged[t2]["d"].copy()
        for h in (o1.host, o2.host):
            if h is not None:
                d1[h] = 0.0; d2[h] = 0.0
        nP, nQ = d1.shape[1], d2.shape[1]
        out = np.zeros(nb)
        step = max(1, int(self.maxel // max(1, nP * nQ)))
        for c in range(0, nb, step):
            mk = mask[c:c + step]
            e = _esym2_batch(mk[:, :, None] * d1[None], mk[:, :, None] * d2[None], s)
            tot = np.zeros(mk.shape[0])
            for a in range(s + 1):
                tot += (e[a][s - a] * W[a][None]).sum(axis=(1, 2))
            out[c:c + step] = tot
        return out

    def self_sum(self, o, t, s, mask):
        nb = mask.shape[0]
        if s < 1 or t not in o.merged:
            return np.zeros(nb)
        mg = o.merged[t]
        dd = mg["d"]
        e = [np.ones((nb, dd.shape[1]))] + [np.zeros((nb, dd.shape[1])) for _ in range(s)]
        for i in range(dd.shape[0]):
            x = mask[:, i, None] * dd[i][None]
            if not x.any():
                continue
            for a in range(s, 0, -1):
                e[a] += x * e[a - 1]
        return 0.5 * KAPPA * (e[s] * (o.q ** 2 * mg["supB"][s])[None]).sum(axis=1)

    def totals(self, m, excl_list, progress=None):
        """for each exclusion set in excl_list (iterables of sites): (self, cross) in kcal/mol, rounded up by RND."""
        GF = self.GF
        ns = GF.G.ns
        nb = len(excl_list)
        mask = np.ones((nb, ns))
        for b, ex in enumerate(excl_list):
            for i in ex:
                mask[b, i] = 0.0
        F = GF.F
        se = np.zeros(nb); cr = np.zeros(nb)
        se += self.self_sum(F, "F", m, mask)
        cr += self.theta(F, "F", F, "F", m, mask)
        t0 = time.time()
        for l in range(ns):
            o = GF.site[l]
            inl = mask[:, l]                                    # 1 where host l may lie inside T
            se += self.self_sum(o, "X", m, mask)
            cr += self.theta(F, "F", o, "X", m, mask) + self.theta(o, "X", o, "X", m, mask)
            for t in ("A", "N"):
                se += inl * self.self_sum(o, t, m - 1, mask)
                cr += inl * (self.theta(F, "F", o, t, m - 1, mask) + self.theta(o, t, o, t, m - 1, mask))
            for l2 in range(l + 1, ns):
                o2 = GF.site[l2]
                inl2 = mask[:, l2]
                cr += self.theta(o, "X", o2, "X", m, mask)
                for t in ("A", "N"):
                    cr += inl * self.theta(o, t, o2, "X", m - 1, mask)
                    cr += inl2 * self.theta(o, "X", o2, t, m - 1, mask)
                if m - 2 >= 1:
                    for t in ("A", "N"):
                        for t2 in ("A", "N"):
                            cr += inl * inl2 * self.theta(o, t, o2, t2, m - 2, mask)
            if progress and (l % progress == 0 or l == ns - 1):
                print(f"      GFBatch: host site {l + 1}/{ns} done, {time.time() - t0:.0f}s", flush=True)
        return se / KCAL * RND, cr / KCAL * RND


# ============================================================================= pair sums: driver
def exclusion_sets(n, w=None):
    """[()] + singles + pairs (i < j); with w given only the pairs with j - i <= w."""
    ex = [()] + [(i,) for i in range(n)]
    ex += [(i, j) for i in range(n) for j in range(i + 1, n) if (w is None or j - i <= w)]
    return ex


def assemble_pair_sums(n, m, excl, tot):
    """From the totals over exclusion sets:  Gamma, S_i = sum_{T ni i} chat_T = Gamma - Gamma^(-i),
    G_ij = sum_{T contains i, j} chat_T = Gamma - Gamma^(-i) - Gamma^(-j) + Gamma^(-i,-j)  (nan where the pair
    exclusion was not computed).  `tot` are the upward-rounded P3 sums (factor RND)."""
    val = {tuple(e): float(t) for e, t in zip(excl, tot)}
    Gam = val[()]
    S = np.array([Gam - val[(i,)] for i in range(n)])
    Gp = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) in val:
                Gp[i, j] = Gp[j, i] = Gam - val[(i,)] - val[(j,)] + val[(i, j)]
    return Gam, S, Gp


def enum_chat(GF, m):
    """explicit enumeration: chat_T for every T of order m by P3's per-subset evaluation total(m, T)."""
    n = GF.G.ns
    out = {}
    for T in itertools.combinations(range(n), m):
        s_, c_ = GF.total(m, T=list(T))
        out[T] = float(s_ + c_)
    return out


def pair_sums_from_chat(n, chat):
    S = np.zeros(n); Gp = np.zeros((n, n))
    for T, v in chat.items():
        for i in T:
            S[i] += v
        for i, j in itertools.combinations(T, 2):
            Gp[i, j] += v; Gp[j, i] += v
    return float(sum(chat.values())), S, Gp


# ============================================================================= penalties
def fp_tables(n, k, x0, M):
    """P3's floating-point allowance for the evaluated terms: every d_U (1 <= |U| <= M) is an alternating sum of
    2^|U| values of g, each within EPS_G; d_U vanishes exactly unless U is inside the changed set.  So the
    rounding of the model at x is at most EPS_G (for g(x0)) + sum_{U subset S(x), 1 <= |U| <= M} phi_U,
    phi_U = EPS_G 2^|U|.  Returned: (phi1 (n,) = sum over U ni i of phi_U/|U|  [P3's site allocation],
    psi1 (n,) = phi_{i} [|U| = 1 only], psi2 (n, n) = sum over U containing i, j of phi_U / C(|U|, 2)
    [pair allocation of all U with |U| >= 2]).  Sites with a single state never change: no U through them."""
    act = [i for i in range(n) if k[i] > 1]
    na = len(act)
    phi1 = np.zeros(n); psi1 = np.zeros(n); psi2 = np.zeros((n, n))
    for i in act:
        phi1[i] = EPS_G * sum(math.comb(na - 1, s - 1) * 2 ** s / s for s in range(1, M + 1))
        psi1[i] = EPS_G * 2
    for i in act:
        for j in act:
            if i != j:
                psi2[i, j] = EPS_G * sum(math.comb(na - 2, s - 2) * 2 ** s / math.comb(s, 2) for s in range(2, M + 1))
    return phi1, psi1, psi2


def site_form(n, m, S, phi1):
    """P3's site penalties gamma_i = (1/m) sum_{T ni i} chat_T (+ P3's site allocation of the fp allowance)."""
    return np.maximum(S, 0.0) / m * RND + phi1


def pair_form(n, m, Gp, psi1, psi2, absallow):
    """pair penalties gamma_ij = sum_{T contains i,j} chat_T / C(m, 2) (+ pair allocation of the fp allowance).
    absallow: absolute allowance added to every G_ij for the rounding of the inclusion-exclusion."""
    c2 = math.comb(m, 2)
    g2 = (np.maximum(Gp, 0.0) + absallow) / c2 * RND + psi2
    np.fill_diagonal(g2, 0.0)
    return psi1.copy(), g2


def banded_pair_form(n, m, w, S, Gp, psi1, psi2, absallow):
    """Banded pair form (P4.6(iii)): in-band pairs (|i - j| <= w) keep gamma_ij; the share of every out-of-band
    pair goes in halves to its two sites.  Only in-band G_ij are needed: by double counting
        sum_{j != i} G_ij = (m - 1) S_i,   so   sum_{j: |i-j| > w} G_ij = (m - 1) S_i - sum_{0 < |i-j| <= w} G_ij.
    Returns (site part (n,), in-band pair part (n, n))."""
    c2 = math.comb(m, 2)
    gs = psi1.copy(); g2 = np.zeros((n, n))
    for i in range(n):
        inband = 0.0; psi_out = 0.0; nin = 0; nout = 0; direct = 0.0; have_all = True
        for j in range(n):
            if j == i:
                continue
            if abs(i - j) <= w:
                assert np.isfinite(Gp[i, j]), "in-band pair sum missing"
                g2[i, j] = (max(Gp[i, j], 0.0) + absallow) / c2 * RND + psi2[i, j]
                inband += Gp[i, j]; nin += 1
            else:
                psi_out += psi2[i, j]; nout += 1
                if np.isfinite(Gp[i, j]):
                    direct += max(Gp[i, j], 0.0) + absallow
                else:
                    have_all = False
        if nout == 0:
            far = 0.0                                     # no out-of-band pair through i: nothing to move
        elif have_all:
            far = direct                                  # every out-of-band pair sum is available: add them
        else:                                             # double-counting identity; each S carries 1 allowance unit,
            far = max((m - 1) * S[i] - inband, 0.0) + (m - 1 + nin) * absallow      # each in-band G one unit
        gs[i] += 0.5 * far / c2 * RND + 0.5 * psi_out
    return gs, g2


def penalty_value(st, x0, gs, g2):
    """sum_i gs_i s_i + sum_{i<j} g2_ij s_i s_j at the states st (N, n), s = [x != x0]."""
    s = (np.atleast_2d(st) != np.asarray(x0)[None]).astype(float)
    return s @ gs + 0.5 * np.einsum("ni,ij,nj->n", s, g2, s)


def envelope_value(st, x0, chat):
    """sum of chat_T over T inside the changed set (the m-body envelope), by enumeration of the subsets."""
    s = (np.atleast_2d(st) != np.asarray(x0)[None])
    out = np.zeros(s.shape[0])
    for T, v in chat.items():
        out += v * s[:, list(T)].all(axis=1)
    return out


# ============================================================================= models
def build_models(k, x0, c0, h, J, d, w, M, gs, g2, const=EPS_G):
    """Floor and ceiling  m_-/+ = [P3's banded minorant/majorant of f + I_M g] -/+ (const + sum_i gs_i s_i +
    sum_{i<j, j-i<=w} g2_ij s_i s_j).  P3's pwmodel.build_band_models is called UNCHANGED with the site part
    (it adds  -/+ gs_i [x_i != x0_i]  and  -/+ const); the in-band pair penalties are then added to the in-band pair
    tables.  g2 must vanish outside the band."""
    n = len(k)
    lo, up = pw.build_band_models(k, x0, c0, h, J, d, w, const, M, gam=np.asarray(gs, dtype=float))
    for i in range(n):
        for j in range(i + 1, n):
            v = float(g2[i, j])
            if v == 0.0:
                continue
            assert j - i <= w, "pair penalty outside the band"
            si = np.ones(k[i]); si[x0[i]] = 0.0
            sj = np.ones(k[j]); sj[x0[j]] = 0.0
            tab = v * np.outer(si, sj)
            lo.add_pair(i, j, -tab)
            up.add_pair(i, j, +tab)
    return lo, up


def diff_model(lo, up):
    n = lo.n
    diff = pw.BandModel(lo.k, lo.w)
    diff.const = up.const - lo.const
    diff.one = [up.one[i] - lo.one[i] for i in range(n)]
    for key in set(lo.pair) | set(up.pair):
        diff.pair[key] = up.pair.get(key, 0.0) - lo.pair.get(key, 0.0)
    return diff


# ============================================================================= instance set-up, ball, enumeration
def setup(seq, bb, tau, kind="gbn2"):
    G = GBModel(seq, bb, tau=tau, kind=kind)
    c0, h, J = pw.known_tables(G)
    x0, E0, nev = pw.icm_anchor(G, c0, h, J)
    return G, c0, h, J, x0, E0


def tagname(seq, bb, tau, kind="gbn2"):
    return f"{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_{kind}"


def ball_terms(G, x0, M, seq, bb, tau, kind="gbn2", verbose=True):
    """anchored terms d_U, |U| <= M, by P3's pwmodel.anchored_terms.  Ball values: (1) a prefix of a ball of
    larger radius cached by P3 or by me (the ball of radius M is the first N_ball(M) states of any larger ball:
    pwmodel.ball_states orders by |U|, then lexicographically -- checked state by state), (2) else evaluated
    with P3's bulk evaluator and cached in ws_P6/cache."""
    k = G.k
    blocks, tot = pw.ball_states(k, x0, M)
    allst = np.concatenate([b for _, b in blocks], axis=0)
    ah = hashlib.sha1(str((tuple(x0), [list(map(int, dd)) for dd in G.dom])).encode()).hexdigest()[:10]
    vals = None; src = None
    for cdir in (MYCACHE, os.path.join(P3, "cache")):
        for MM in range(M, 9):
            fn = os.path.join(cdir, f"ball_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_{kind}_M{MM}_{ah}.npz")
            if os.path.exists(fn):
                z = np.load(fn)
                if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst):
                    vals = np.array(z["vals"][:tot], dtype=float); src = fn
                    break
        if vals is not None:
            break
    if vals is None:
        vals = np.empty(tot)
        t0 = time.time()
        for s in range(0, tot, 4096):
            vals[s:s + 4096] = G.bulk_energy(allst[s:s + 4096])
            if verbose and (s // 4096) % 10 == 0:
                print(f"      ball evaluations {min(tot, s + 4096)}/{tot}  {time.time() - t0:.0f}s", flush=True)
        if tot >= 2000:
            np.savez(os.path.join(MYCACHE, f"ball_{seq.replace(':', 'c')}_{bb}_t{tau:.2f}_{kind}_M{M}_{ah}.npz"),
                     states=allst.astype(np.int16), vals=vals)
        src = "evaluated now"
    lut = {st.tobytes(): v for st, v in zip(allst.astype(np.int16), vals)}

    def lookup(st):
        st = np.atleast_2d(st).astype(np.int16)
        return np.array([lut[row.tobytes()] for row in st])
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None)
    assert nb == tot
    return d, tot, src


def _p2_grid(G, seq, bb, tau, ncheck=200):
    """g_GB on P3's product domain from workstream P2's stored enumeration (ws_P2/data/fb_*.npz), read with
    workstream P4's loader (p4lib.load_instance: P2's pruned product X' at tau).  Accepted only if the shape equals
    P3's domain and the values agree with P3's OWN evaluator (GBModel.energy) at `ncheck` random states and at the
    two corner states to 1e-8 kcal/mol (different states differ by far more).  Returns (g flat in C order, dev) or None."""
    P4 = os.path.normpath(os.path.join(HERE, "..", "ws_P4"))
    if P4 not in sys.path:
        sys.path.append(P4)
    import p4lib as L4                                   # P4 (read-only), which imports P2's anlib / an_main (read-only)
    fn = os.path.join(L4.P2, "data", f"fb_{seq.replace(':', 'c')}_{bb}_R3_t0.60.npz")
    if not os.path.exists(fn):
        return None
    inst = L4.load_instance(f"fb_{seq.replace(':', 'c')}_{bb}_R3_t0.60", tau)
    if inst is None or list(inst["shape"]) != list(G.k):
        return None
    g = np.ascontiguousarray(inst["R"]["GB"], dtype=float).reshape(-1)
    st = G.product_states()
    rng = np.random.default_rng(4242)
    pick = np.concatenate([[0, len(st) - 1], rng.integers(0, len(st), min(ncheck, len(st)))])
    dev = float(np.abs(g[pick] - G.energy(st[pick])).max())
    if not dev < 1e-8:
        return None
    return g, dev


def enumerate_g(G, seq, bb, tau, kind="gbn2", verbose=True, use_p2=True):
    """g on the whole product domain, cached in ws_P6/cache.  Source: (1) my cache; (2) for domains of more than
    20 000 states, P2's stored enumeration if it passes _p2_grid's checks (P2's block evaluator is the one P3's
    bulk_energy calls, so this is the same function evaluated earlier); (3) P3's bulk evaluator, as run_floor.py does."""
    ah = hashlib.sha1(str([list(map(int, dd)) for dd in G.dom]).encode()).hexdigest()[:10]
    fn = os.path.join(MYCACHE, f"enum_{tagname(seq, bb, tau, kind)}_{ah}.npy")
    st = G.product_states()
    if os.path.exists(fn):
        g = np.load(fn)
        if len(g) == len(st):
            return st, g, "cache"
    if use_p2 and kind == "gbn2" and len(st) > 20000:
        r = _p2_grid(G, seq, bb, tau)
        if r is not None:
            np.save(fn, r[0])
            return st, r[0], f"P2's stored enumeration; = P3's own evaluator at 202 states to {r[1]:.1e}"
    g = np.empty(len(st))
    t0 = time.time()
    for s in range(0, len(st), 16384):
        g[s:s + 16384] = G.bulk_energy(st[s:s + 16384])
        if verbose and (s // 16384) % 8 == 0 and len(st) > 60000:
            print(f"      enumeration {min(len(st), s + 16384)}/{len(st)}  {time.time() - t0:.0f}s", flush=True)
    np.save(fn, g)
    return st, g, "evaluated now"


# ============================================================================= one-call model builder (used by the sampler etc.)
def load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, kind, m, verbose=False, w=None, maxall=24):
    """(Gamma, S, G, source).  All pairs for chains of at most `maxall` sites; for longer chains only the in-band pair
    exclusions (j - i <= w) are computed (G is nan elsewhere; banded_pair_form then uses the double-counting identity)."""
    n = G.ns
    stem = os.path.join(HERE, "out", f"pairsums_{tagname(seq, bb, tau, kind)}_m{m}")
    cands = [stem + ".npz"] + ([f"{stem}_w{ww}.npz" for ww in range(n - 1, w - 1, -1)] if w is not None else [])
    for fn in cands:
        if os.path.exists(fn):
            z = np.load(fn)
            if list(z["anchor"]) == list(x0):
                return float(z["Gamma"]), z["S"], z["G"], "read from " + os.path.basename(fn)
    t1 = time.time()
    wsel = None if (n <= maxall or w is None) else w
    excl = exclusion_sets(n, wsel)
    se, cr = GFBatch(GF).totals(m, excl, progress=(max(1, n // 5) if verbose else None))
    Gam, S, Gp = assemble_pair_sums(n, m, excl, se + cr)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    fn = stem + (".npz" if wsel is None else f"_w{wsel}.npz")
    np.savez(fn, Gamma=Gam, S=S, G=Gp, tot=se + cr, se=se, cr=cr, anchor=np.array(x0), m=m, w=-1 if wsel is None else wsel,
             excl=np.array([list(e) + [-1] * (2 - len(e)) for e in excl]))
    return Gam, S, Gp, f"computed, {len(excl)} exclusion sets, {time.time() - t1:.1f}s"


def make_models(seq, bb, tau, m, w, form, kind="gbn2", setup_data=None):
    """(lo, up, info) for the instance, order m, band w and penalty form 'S' (site, P3) or 'B' (banded pair)."""
    if setup_data is None:
        setup_data = setup(seq, bb, tau, kind)
    G, c0, h, J, x0, E0 = setup_data
    n, k = G.ns, G.k
    sup = EnvelopeSup(G)
    GF = GFBound2(G, x0, sup, K=m)
    Gam, S, Gp, srcp = load_or_compute_pair_sums(G, GF, x0, seq, bb, tau, kind, m, w=w)
    M = m - 1
    d, nball, srcb = ball_terms(G, x0, M, seq, bb, tau, kind, verbose=False)
    phi1, psi1, psi2 = fp_tables(n, k, x0, M)
    if form == "S":
        gs, g2 = site_form(n, m, S, phi1), np.zeros((n, n))
    elif form == "B":
        gs, g2 = banded_pair_form(n, m, w, S, Gp, psi1, psi2, 5e-9 * Gam)
    else:
        raise ValueError(form)
    lo, up = build_models(k, x0, c0, h, J, d, w, M, gs, g2)
    return lo, up, dict(Gamma=Gam, nball=int(nball), pairsums=srcp, ball=srcb, setup=setup_data)
