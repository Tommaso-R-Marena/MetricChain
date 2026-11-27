#!/usr/bin/env python3
"""P9 stretch -- the theory division's nested sampler (their Proposition 11.113a) as the coordinator implemented it
(pi_inference/nested_sampler.py: its main() is called UNCHANGED), with
  (i)  the OUTER sandwich built from the state-resolved tables (window form 'W', stage 2: p9_05_brackets.py), and
  (ii) the INNER sandwich from the fully resolved envelope  env(x) = sum_{T subset S(x), |T| = m} Theta^2_T(x_T)
       (P9_REPORT Theorem R), read from the stored tables cache/theta2_<tag>_m<m>*.npz.
What is whose: the algorithm and its error bound -- the theory division; nested_sampler.py, the inner sandwich with
its clipping and allowances, cached_sampler -- the coordinator; the models and the envelope object -- this workstream.
nested_sampler.py is imported under the same guard as the other foreign modules (it tries to fill a cache directory
of pi_inference at import: refused and counted); its output file is redirected to ws_P9/out (NS.HERE).

usage: python3 -B p9_07_nested.py SEQ H M W W window [--N n] [--Nf nf] [--seed s]
       (arguments as nested_sampler.py: sequence, backbone, order, band, form -- only 'W' --, models -- only 'window')
writes logs/nested_<tag>_m<M>_w<W>.log (a copy of the output), out/nested_sampler_<...>.json
"""
import sys
import p9lib as P9
from p9lib import *
shutil.copy = P9._guard_copy; os.makedirs = P9._guard_makedirs
try:
    import nested_sampler as NS                           # coordinator (read-only)
    import nested_sampler_ext as NX                       # coordinator (read-only): cached_sampler
finally:
    shutil.copy = P9._real_copy; os.makedirs = P9._real_makedirs
encl.CACHE = MYCACHE; L.MYCACHE = MYCACHE; NS.CACHE = MYCACHE; NS.HERE = OUT


class ResolvedEnvelope:
    """env(x) = RND * sum over the m-subsets T of the changed set of Theta^2_T(x_T) (kcal/mol); the interface of
    nested_sampler.Envelope that main() uses: value(st), nsets, seconds."""

    def __init__(self, tag, m, n, k, x0):
        self.n = n; self.x0 = np.asarray(x0); self.seconds = 0.0; self.nsets = 0
        self.subs = list(itertools.combinations(range(n), m)); self.tabs = [None] * len(self.subs)
        for fn in sorted(glob.glob(os.path.join(MYCACHE, f"theta2_{tag}_m{m}*.npz"))):
            z = np.load(fn)
            for j in z["idx"]:
                self.tabs[int(j)] = np.array(z[f"t{int(j)}"])
        assert all(t is not None for t in self.tabs), "stage-2 tables missing: run p9_03_tables.py with --keeptabs"
        non = nonanchor(k, x0, range(n)); self.pos = [np.full(k[i], -1) for i in range(n)]
        for i in range(n):
            self.pos[i][non[i]] = np.arange(len(non[i]))

    def value(self, st):
        t1 = time.time(); st = np.atleast_2d(st); out = np.zeros(len(st))
        P = np.stack([self.pos[i][st[:, i]] for i in range(self.n)], axis=1)
        for T, tab in zip(self.subs, self.tabs):
            I = P[:, list(T)]; inS = (I >= 0).all(axis=1)
            if inS.any():
                out[inS] += tab[tuple(I[inS].T)]
        self.nsets = max(self.nsets, len(np.unique(((st != self.x0[None]) * (1 << np.arange(self.n))[None]).sum(1))))
        self.seconds += time.time() - t1
        return out * RND


def build_p9(seq, bb, m, w, form, models, w3=None):
    assert form == "W" and models == "window" and "--enum" not in sys.argv
    tau = tau_of(seq); tag = tagname(seq, bb, tau); M = m - 1
    G, c0, h, J, x0, E0 = setup(seq, bb, tau); n, k = G.ns, list(G.k)
    LD = Loaded(os.path.join(OUT, f"tables_{tag}_m{m}_w{w}.npz")); assert LD.x0 == x0 and LD.k == k
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None
    for f in sorted(os.listdir(os.path.join(P8DIR, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8DIR, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst):
                vals = np.array(z["vals"][:tot], dtype=float)
                pick = np.random.default_rng(11).choice(tot, size=min(tot, 1000), replace=False)
                dev = float(np.abs(np.concatenate([G.bulk_energy(allst[pick[s:s + 250]]) for s in range(0, len(pick), 250)]) - vals[pick]).max()); assert dev < 1e-8, dev
                srcb = f"ws_P8/cache/{f} (1000 random values re-evaluated: largest deviation {dev:.1e} kcal/mol)"; break
            del z
    assert vals is not None
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
        return vals_s[p]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
    del allst, code, order
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    XGo = load_gibbs(tag, 4242)[0]
    gs, g2 = L.banded_pair_form(n, m, w, np.zeros(n), np.zeros((n, n)), psi1, psi2, 0.0)
    lo, up, info = build_window_models_occ(WindowModel, k, x0, c0, h, J, d, w, EPS_G, M, gs, g2, None, XG=XGo, far_pairs="anchored")
    g1, gp, g3 = window_form(LD.W[2])
    for K, tab in g1.items():
        lo.one[K[0]] = lo.one[K[0]] - tab; up.one[K[0]] = up.one[K[0]] + tab
    for (i, j), tab in gp.items():
        lo.add_pair(i, j, -tab); up.add_pair(i, j, tab)
    for U, tab in g3.items():
        lo.add_multi(U, -tab); up.add_multi(U, tab)
    diff = diff_window(lo, up)
    lo.sample = NX.cached_sampler(lo)
    env = ResolvedEnvelope(tag, m, n, k, x0)
    NS.log(f"--- P9: outer sandwich = window models (occ+) + P6's allowances + state-resolved window-form tables of stage 2 ({len(g1)} site, {len(gp)} pair, {len(g3)} window tables); "
           f"inner sandwich = the fully resolved envelope of {len(env.subs)} stored tables; ball: {srcb}; foreign writes attempted during import (refused): {len(P9.FOREIGN_WRITES)}")
    return dict(seq=seq, bb=bb, tau=tau, m=m, M=M, w=w, w3=w, form=form, models=models, G=G, c0=c0, h=h, J=J, x0=np.array(x0), E0=E0, n=n, k=k,
                GF=None, Gam=float(LD.TB[1].sab.sum()), d=d, nball=int(tot), srcb=srcb, srcp="ws_P9 tables", lo=lo, up=up, diff=diff, info=info, env=env)


if __name__ == "__main__":
    a = sys.argv[1:]; seq, bb, m, w = a[0], a[1], int(a[2]), int(a[3])
    NS.build = build_p9
    NS.main()
