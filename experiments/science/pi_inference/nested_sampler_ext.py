#!/usr/bin/env python3
"""The nested sampler (nested_sampler.py, unchanged) on a sandwich built from EXTERNAL per-subset constants --
coordinator's script for the charged peptides of workstream P8.

nested_sampler.py takes the constants chat_T from workstream P3's closed form.  Workstream P8 computed sharper
per-subset constants for the charged sequences (variants 'Sb': P3's theorem with the maximum over host rotamers taken
state-wise; 'SAb': the same with P8's Theorem AH).  This driver replaces nested_sampler.build by a function that
  * reads chat_T from ws_P8/out/g12_<tag>_m<m>.npz / g12b_<tag>_m<m>.npz (twelve residues) or from
    ws_P8/out/bc_<tag>.json (the enumerated instances),
  * forms the site, pair and in-window triple sums by plain summation over the subsets (allowance 1e-12 Gamma for the
    rounding of sums of at most C(n, m) positive doubles),
  * takes the ball from P8's cache when it has one whose states equal pwmodel.ball_states (a random sample of its
    values is re-evaluated), else evaluates it,
  * builds the outer sandwich with the window models, and the envelope sum_{T subset S(x)} chat_T as a table,
and then calls nested_sampler.main() as it is.  Hypothesis used, for both sandwiches:
      |g(x) - I_{m-1} g(x)|  <=  sum_{T subset S(x), |T| = m} chat_T          (P3's theorem for 'Sb'; Theorem AH for 'SAb').
The --enum mode of nested_sampler.py is not available here (it compares the envelope with P3's closed form).

Run:  python3 -B nested_sampler_ext.py K5 H 4 4 T window --chat SAb --N 1200 --Nf 400000 > nested_sampler_K5_H_m4_w4_T_window_SAb.log
      python3 -B nested_sampler_ext.py K12 H 5 7 T window --chat SAb --N 1200 --Nf 400000 > nested_sampler_K12_H_m5_w7_T_window_SAb.log
      ... --reduce occ+ > nested_sampler_K12_H_m5_w7_T_window_SAb_occ.log     (the outer sandwich with window_model_occ.py)
"""
import os, sys, json, math, itertools
import numpy as np
import nested_sampler as NS
L, pw, T9, window_model = NS.L, NS.pw, NS.T9, NS.window_model
P8 = os.path.join(NS.SCI, "ws_P8")
VAR = NS.opt(sys.argv, "--chat", "SAb")
RED = NS.opt(sys.argv, "--reduce", "pair"); assert RED in ("pair", "occ+")


class TableEnvelope(NS.Envelope):
    def __init__(self, chat, m, n, x0):
        self.B = None; self.m = m; self.n = n; self.x0 = np.asarray(x0); self.cache = {}; self.seconds = 0.0
        self.pow = (1 << np.arange(n)).astype(np.int64); self.table = True; self.nsets = 0
        subs = list(itertools.combinations(range(n), m)); assert len(chat) == len(subs)
        self.Tmask = np.array([sum(1 << i for i in T) for T in subs], dtype=np.int64); self.chat = np.asarray(chat, dtype=float)

    def value_closed_form(self, st):
        raise RuntimeError("no closed form for external constants")


def cached_sampler(model, beta=L.BETA):
    """workstream P3's BandModel.sample (pwmodel.py, copied line by line) with the transfer-matrix messages computed ONCE.
    P3's method recomputes them at every call; nested_sampler.draw_q calls it once per batch, which costs a full
    transfer-matrix pass per batch (20-40 s each for Lys12 at band 7, about a hundred batches)."""
    _, As = model.dp(-beta, "logsumexp", keep=True)
    n, w, kk = model.n, model.w, model.k

    def sample(N, rng):
        st = np.zeros((N, n), dtype=int)
        for i in range(n - 1, -1, -1):
            A = As[i]; hi = min(i + w, n - 1)
            idx = (slice(None),) + tuple(st[:, j] for j in range(i + 1, hi + 1))
            lw = A[idx]
            if lw.ndim == 1: lw = np.repeat(lw[:, None], N, 1)
            lw = lw - lw.max(axis=0, keepdims=True)
            p = np.exp(lw); p /= p.sum(axis=0, keepdims=True)
            cdf = np.cumsum(p, axis=0)
            u = rng.random(N)
            st[:, i] = np.minimum((u[None, :] > cdf).sum(axis=0), kk[i] - 1)
        return st
    return sample


def build_ext(seq, bb, m, w, form, models, w3=None):
    assert models == "window" and "--enum" not in sys.argv
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    w3 = w if w3 is None else w3; M = m - 1
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"; subs = list(itertools.combinations(range(n), m))
    f12, f12b, fbc = (os.path.join(P8, "out", f) for f in (f"g12_{tag}_m{m}.npz", f"g12b_{tag}_m{m}.npz", f"bc_{tag}.json"))
    if os.path.exists(f12b):
        Z = np.load(f12); Zb = np.load(f12b); assert [int(v) for v in Zb["anchor"]] == x0 and [tuple(int(v) for v in T) for T in Zb["T"]] == subs
        V = [str(v) for v in Z["variants"]]; Vb = [str(v) for v in Zb["variants"]]
        chat = Zb["Cb"][:, Vb.index(VAR)] if VAR in Vb else Z["C"].sum(axis=2)[:, V.index(VAR)]; srcp = f"ws_P8/out/{os.path.basename(f12b if VAR in Vb else f12)}, variant '{VAR}'"
    else:
        Jd = json.load(open(fbc))["per_subset"][VAR]; chat = np.array([float(Jd["-".join(map(str, T))]) for T in subs]); srcp = f"ws_P8/out/{os.path.basename(fbc)}, variant '{VAR}'"
        Zm = np.load(os.path.join(P8, "out", f"m1_{tag}.npz")); assert [int(v) for v in Zm["anchor"]] == x0
    Gam = float(chat.sum()); S = np.zeros(n); Gp = np.zeros((n, n)); tris = T9.window_triples(n, w3); H = {tr: 0.0 for tr in tris}
    for T, v in zip(subs, chat):
        for i in T: S[i] += v
        for i, j in itertools.combinations(T, 2): Gp[i, j] += v; Gp[j, i] += v
        for tr in itertools.combinations(T, 3):
            if tr in H: H[tr] += v
    absA = 1e-12 * Gam
    # the ball
    blocks, tot = pw.ball_states(k, x0, M); allst = np.concatenate([b for _, b in blocks], axis=0); vals = None
    for f in sorted(os.listdir(os.path.join(P8, "cache"))):
        if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f:
            z = np.load(os.path.join(P8, "cache", f))
            if z["states"].shape[0] >= tot and np.array_equal(z["states"][:tot], allst):
                vals = np.array(z["vals"][:tot], dtype=float)
                pick = np.random.default_rng(11).choice(tot, size=min(tot, 1000), replace=False)
                dev = float(np.abs(np.concatenate([G.bulk_energy(allst[pick[s:s + 250]]) for s in range(0, len(pick), 250)]) - vals[pick]).max()); assert dev < 1e-8, dev
                srcb = f"ws_P8/cache/{f} (1000 random values re-evaluated: largest deviation {dev:.1e} kcal/mol)"; break
    if vals is None:
        vals = np.concatenate([G.bulk_energy(allst[s:s + 256]) for s in range(0, tot, 256)]); srcb = "evaluated now"
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = allst.astype(np.int64) @ radix; order = np.argsort(code); code_s = code[order]; vals_s = vals[order]

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c); assert np.array_equal(code_s[p], c)
        return vals_s[p]
    d, nb, _ = pw.anchored_terms(G, x0, M, energy=lookup, cache_file=None); assert nb == tot
    phi1, psi1, psi2 = L.fp_tables(n, k, x0, M)
    if form == "S": tabs = (L.site_form(n, m, S, phi1), np.zeros((n, n)), None)
    elif form == "B": tabs = L.banded_pair_form(n, m, w, S, Gp, psi1, psi2, absA) + (None,)
    else: tabs = window_model.triple_form_two_windows(T9.window_triples, L.RND, n, m, w, w3, Gp, H, psi1, psi2, absA, absA)
    if RED == "pair":
        lo, up, info = NS.build_window_models(k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs); redtxt = "workstream P3's rule (window_model.py, 'pair')"
    else:                                                # the occupancy-aware rule with the anchored split of the far pairs (window_model_occ.py)
        from window_model_occ import build_window_models_occ, gibbs_sample
        XGo = gibbs_sample(pw, G, c0, h, J, x0, k, L.BETA, np.random.default_rng(4242))
        lo, up, info = build_window_models_occ(NS.WindowModel, k, x0, c0, h, J, d, w, L.EPS_G, M, *tabs, XG=XGo, far_pairs="anchored")
        redtxt = "occupancy-aware rule with the anchored split of the far pairs (window_model_occ.py; guided by a Gibbs sample of 960 states, seed 4242)"
    diff = NS.diff_window(lo, up)
    lo.sample = cached_sampler(lo)                       # P3's backward sampler with its messages computed once (see cached_sampler)
    NS.log(f"--- EXTERNAL CONSTANTS: {len(subs)} constants from {srcp}; ball: {srcb}; reduction of the terms that do not fit the band: {redtxt}; "
           f"floor sampler: workstream P3's backward sampling with the transfer-matrix messages computed once")
    return dict(seq=seq, bb=bb, tau=tau, m=m, M=M, w=w, w3=w3, form=form, models=models, G=G, c0=c0, h=h, J=J, x0=np.array(x0), E0=E0, n=n, k=k,
                GF=None, Gam=Gam, d=d, nball=int(tot), srcb=srcb, srcp=srcp, lo=lo, up=up, diff=diff, info=info, env=TableEnvelope(chat, m, n, x0))


if __name__ == "__main__":
    NS.build = build_ext
    a = sys.argv[1:]; seq, bb, m, w, form, models = a[0], a[1], int(a[2]), int(a[3]), a[4], a[5]
    NS.main()
    tagj = f"{seq.replace(':', 'c')}_{bb}_m{m}_w{w}_{form}_{models}"
    src = os.path.join(NS.HERE, f"nested_sampler_{tagj}.json"); dst = os.path.join(NS.HERE, f"nested_sampler_{tagj}_{VAR}" + ("_occ" if RED != "pair" else "") + ".json")
    os.replace(src, dst)
