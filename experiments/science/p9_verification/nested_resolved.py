#!/usr/bin/env python3
"""Coordinator's replication of workstream P9's sampler runs (P9_REPORT section 5.4; its request P9-E5) with a driver
that is not P9's and with another seed.

The theory division's nested sampler (their Proposition 11.113a) as implemented in pi_inference/nested_sampler.py
(main() unchanged), with
  the OUTER sandwich: the coordinator's window models + workstream P6's floating-point allowances + the window-form
      tables of workstream P9's stage 2, RE-BUILT here from P9's raw tables (as p9_verification/resolved_brackets.py:
      every subset charged to P9's stored choice of in-window sub-tuple, maximum over the given-up sites);
  the INNER sandwich: the fully resolved envelope  env(x) = (1 + 1e-9) sum_{T subset S(x), |T| = m} Theta_T(x_T)
      evaluated here from the same raw tables.
P9's: the raw tables (ws_P9/cache/theta2_*.npz) and the choice of sub-tuples (ws_P9/out/tables_*.npz, key s2_keep).
Mine: everything else in this file.  The seed is nested_sampler's default plus 1000 unless --seed is given (P9 used
the default).  A probability statement is replicated when the intervals of two independent runs overlap.

Run: python3 -B nested_resolved.py LKSE:12 H 4 7 W window --N 1200 --Nf 400000 > nested_resolved_LKSEc12_m4_w7.log
"""
import os, sys, glob, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "pi_inference"))
import nested_sampler as NS
import nested_sampler_ext as NX
from window_model_occ import build_window_models_occ, gibbs_sample
L, pw = NS.L, NS.pw
RND = 1.0 + 1e-9
P8, P9 = os.path.join(SCI, "ws_P8"), os.path.join(SCI, "ws_P9")
NS.HERE = HERE                                           # the driver's JSON record goes here


class ResolvedEnvelope:
    """the interface nested_sampler.main() uses: value(st), nsets, seconds."""

    def __init__(self, subs, tabs, n, k, x0):
        self.n = n; self.x0 = np.asarray(x0); self.subs = subs; self.tabs = tabs; self.seconds = 0.0; self.nsets = 0
        self.pos = [np.full(k[i], -1) for i in range(n)]
        for i in range(n):
            self.pos[i][[b for b in range(k[i]) if b != x0[i]]] = np.arange(k[i] - 1)

    def value(self, st):
        t1 = time.time(); st = np.atleast_2d(st); out = np.zeros(len(st))
        P = np.stack([self.pos[i][st[:, i]] for i in range(self.n)], axis=1)
        for T, tab in zip(self.subs, self.tabs):
            I = P[:, list(T)]; inS = (I >= 0).all(axis=1)
            if inS.any(): out[inS] += tab[tuple(I[inS].T)]
        self.nsets = max(self.nsets, len(np.unique(((st != self.x0[None]) * (1 << np.arange(self.n))[None]).sum(1))))
        self.seconds += time.time() - t1
        return out * RND


def build_mine(seq, bb, m, w, form, models, w3=None):
    assert form == "W" and models == "window" and bb == "H"
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]; M = m - 1
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    tabs = [None] * len(subs)
    for fn in sorted(glob.glob(os.path.join(P9, "cache", f"theta2_{tag}_m{m}*.npz"))):
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs), "raw tables of P9 missing"
    ZS = np.load(os.path.join(P9, "out", f"tables_{tag}_m{m}_w{w}.npz"))
    assert [tuple(int(v) for v in T) for T in ZS["s2_subs"]] == subs and [int(v) for v in ZS["x0"]] == x0
    keepK = [tuple(int(v) for v in str(s).split("_")) for s in ZS["s2_keep"]]; W = {}
    for T, tab, K in zip(subs, tabs, keepK):
        assert set(K) <= set(T) and K[-1] - K[0] <= w
        other = tuple(p for p in range(m) if T[p] not in K); red = tab.max(axis=other) if other else tab
        full = np.zeros([k[i] for i in K]); full[np.ix_(*[non[i] for i in K])] = red; W[K] = W.get(K, 0.0) + full
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None
    for f in sorted(os.listdir(os.path.join(P8, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst):
                vals = np.array(z["vals"][:tot], dtype=float); srcb = f"ws_P8/cache/{f}"; break
    assert vals is not None
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
        return vals_s[p]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
    del allst, code, order
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    XGo = gibbs_sample(pw, G, c0, h, J, x0, k, L.BETA, np.random.default_rng(4242))
    gs, g2 = L.banded_pair_form(n, m, w, np.zeros(n), np.zeros((n, n)), psi1, psi2, 0.0)
    lo, up, info = build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, d, w, L.EPS_G, M, gs, g2, None, XG=XGo, far_pairs="anchored")
    for K, tab in W.items():
        if len(K) == 1: lo.one[K[0]] = lo.one[K[0]] - tab * RND; up.one[K[0]] = up.one[K[0]] + tab * RND
        elif len(K) == 2: lo.add_pair(K[0], K[1], -tab * RND); up.add_pair(K[0], K[1], tab * RND)
        else: lo.add_multi(K, -tab * RND); up.add_multi(K, tab * RND)
    diff = NS.diff_window(lo, up)
    lo.sample = NX.cached_sampler(lo)
    NS.log(f"--- coordinator's replication: outer sandwich = window models (occ+) + P6's allowances + window-form tables of P9's stage 2 re-built here from its raw tables ({len(W)} tables); "
           f"inner sandwich = the fully resolved envelope of {len(subs)} raw tables; ball: {srcb}")
    return dict(seq=seq, bb=bb, tau=tau, m=m, M=M, w=w, w3=w, form=form, models=models, G=G, c0=c0, h=h, J=J, x0=np.array(x0), E0=E0, n=n, k=k,
                GF=None, Gam=float(sum(float(t.max()) for t in tabs)), d=d, nball=int(tot), srcb=srcb, srcp="ws_P9 raw tables", lo=lo, up=up, diff=diff, info=info,
                env=ResolvedEnvelope(subs, tabs, n, k, x0))


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--seed" not in a:
        sys.argv += ["--seed", str(2026112700 + 10 * int(a[2]) + 1000)]
    NS.build = build_mine
    NS.main()
