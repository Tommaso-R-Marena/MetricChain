#!/usr/bin/env python3
"""Coordinator's check of workstream P9's STATE-RESOLVED bound at twelve residues, with code that is not P9's.

P9 claims: for every state x and every m-subset T of its changed set there is a table Theta_T (a function of the
rotamers x_T of the sites of T) such that
        | g(x) - I_{m-1} g(x) |  <=  sum_{T subset S(x), |T| = m}  Theta_T(x_T)          ("stage 2").
The tables are READ from ws_P9/cache/theta2_<tag>_m<m>*.npz -- they are P9's; nothing here recomputes them.  Mine:
the evaluation of g, the ball lookup, the interpolation formula (p8_verification/lys12_rerun.interp), the anchored
terms, the states, the summation of the tables over the subsets, the controls.
  (a) (only if the ball of radius m exists, i.e. m <= 4 with workstream P8's balls)  EVERY state with exactly m sites
      off the anchor: there g - I_{m-1} g is the anchored term d_T(x_T) = sum_{V subset T} (-1)^{|T - V|} g(x_V, x0), which
      the ball gives exactly; |d_T(x_T)| <= Theta_T(x_T) for all T and all x_T.  This is sharp per subset and per
      state: no sum over subsets can hide a table entry that is too small.
  (b) uniformly random states with s = m .. n sites off the anchor (my seed) and Gibbs states of the true ensemble (my
      sampler, my seed): | g - I_{m-1} g | <= sum of the tables, the left side with new evaluations of g.
  Controls that must FAIL in (a) -- a check that cannot fail checks nothing: C1 every table replaced by its minimum
  over the states; C2 every table reversed along each state axis (the right numbers at the wrong rotamers).
Run: python3 -B resolved_check12.py K12 0.70 4 > resolved_check12_K12_m4.log
"""
import os, sys, math, time, glob, itertools, resource
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SCI = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(SCI, "p8_verification"))
import lys12_rerun as R8                    # the coordinator's own: interp (the interpolation formula), gibbs; imports p6lib
L, pw, BETA = R8.L, R8.pw, R8.BETA
P8, P9 = os.path.join(SCI, "ws_P8"), os.path.join(SCI, "ws_P9")


def log(s): print(s, flush=True)


def main():
    seq, tau, m = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); bb = "H"; M = m - 1; t0 = time.time()
    rng = np.random.default_rng(20270101 + m)
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    tabs = [None] * len(subs); files = sorted(glob.glob(os.path.join(P9, "cache", f"theta2_{tag}_m{m}*.npz")))
    for fn in files:
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs), "tables of P9 missing"
    for T, tab in zip(subs, tabs): assert tab.shape == tuple(len(non[i]) for i in T)
    nstat = sum(t.size for t in tabs)
    log(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}, anchor {x0}; order m = {m}; {len(subs)} tables of workstream P9 "
        f"({nstat} entries, from {len(files)} file(s)); all entries positive: {bool(all((t > 0).all() for t in tabs))}; sum of the per-subset maxima "
        f"{BETA * sum(float(t.max()) for t in tabs):.4g} kT, of the per-subset minima {BETA * sum(float(t.min()) for t in tabs):.4g} kT")
    # ---- the ball (P8's cache), as in lys12_rerun.py
    fb = [f for f in sorted(os.listdir(os.path.join(P8, "cache"))) if f.startswith(f"ball_{tag}_M") and f.endswith(".npz") and "ckpt" not in f]
    best = None
    for f in fb:
        z = np.load(os.path.join(P8, "cache", f)); r = int(f.split("_M")[1].split("_")[0])
        if best is None or r > best[0]: best = (r, f, z)
    rad, fbn, zb = best
    states = np.array(zb["states"]); vals = np.array(zb["vals"], dtype=float)
    blocks, tot = pw.ball_states(k, x0, rad); pos = 0
    for _, b in blocks:
        assert np.array_equal(states[pos:pos + len(b)], b), "ball states differ from pwmodel.ball_states"; pos += len(b)
    assert pos == tot == states.shape[0]
    del blocks
    radix = np.array([int(np.prod(k[i + 1:])) for i in range(n)], dtype=np.int64)
    code = states.astype(np.int64) @ radix
    pick = rng.choice(tot, size=2000, replace=False); stp = states[pick].astype(np.int64)
    re = np.concatenate([G.bulk_energy(stp[s:s + 250]) for s in range(0, len(stp), 250)]); dev = float(np.abs(re - vals[pick]).max())
    order = np.argsort(code); code_s = code[order]; vals_s = vals[order]; del code, vals, states
    log(f"(0) ball of radius {rad} from ws_P8/cache/{fbn}: {tot} states equal to pwmodel.ball_states block by block; 2000 random values re-evaluated: "
        f"largest deviation {dev:.1e} kcal/mol [{time.time() - t0:.0f}s]")

    def lookup(st):
        c = np.atleast_2d(st).astype(np.int64) @ radix; p = np.searchsorted(code_s, c)
        assert np.array_equal(code_s[np.minimum(p, len(code_s) - 1)], c), "state outside the ball"
        return vals_s[p]
    # ---- (a) every state with exactly m sites off the anchor
    if rad >= m:
        nchk = 0; viol = 0; minr = np.inf; maxd = 0.0; v1 = v2 = 0; ratios = []
        for T, tab in zip(subs, tabs):
            grids = np.meshgrid(*[np.array(non[i]) for i in T], indexing="ij"); N = tab.size
            XT = np.stack([g_.reshape(-1) for g_ in grids], axis=1)                      # (N, m) states of the sites of T
            d = np.zeros(N)
            for r in range(m + 1):
                for V in itertools.combinations(range(m), r):
                    st = np.tile(np.array(x0, dtype=np.int64), (N, 1))
                    for p in V: st[:, T[p]] = XT[:, p]
                    d += (-1) ** (m - r) * lookup(st)
            ad = np.abs(d); th = tab.reshape(-1)
            viol += int((ad > th * (1 + 1e-12) + 1e-9).sum()); nchk += N; maxd = max(maxd, float(ad.max()))
            nz = ad > 1e-9
            if nz.any(): minr = min(minr, float((th[nz] / ad[nz]).min())); ratios.append(th[nz] / ad[nz])
            v1 += int((ad > th.min() + 1e-9).sum())
            rev = tab[tuple(slice(None, None, -1) for _ in range(m))].reshape(-1); v2 += int((ad > rev + 1e-9).sum())
        ratios = np.concatenate(ratios)
        log(f"(a) EVERY state with exactly {m} sites off the anchor: {nchk} states of {len(subs)} subsets; exact anchored term |d_T(x_T)| against P9's Theta_T(x_T): "
            f"violations {viol}; largest |d_T| {maxd:.4g} kcal/mol; ratio Theta/|d| (|d| > 1e-9): smallest {minr:.3f}, median {float(np.median(ratios)):.1f}; "
            f"CONTROLS (must fail): C1 minimum over the states in place of the value: {v1} violations; C2 tables reversed along every axis: {v2} violations "
            f"[{time.time() - t0:.0f}s]")
    else:
        log(f"(a) not possible: the ball has radius {rad} < m = {m}")
    # ---- (b) random states and Gibbs states
    lookupM = lookup
    NR = 250; XR = []
    for s in range(m, n + 1):
        for _ in range(NR):
            x = np.array(x0); S = rng.choice(n, size=s, replace=False)
            for i in S: x[i] = rng.choice(non[i])
            XR.append(x)
    XR = np.array(XR)
    XG = R8.gibbs(G, c0, h, J, x0, k, np.random.default_rng(31337), 8, 150, 30)
    XG = XG[(XG != np.array(x0)[None]).sum(1) >= m]                              # the remainder vanishes below m changed sites
    res = {}
    for name, X in (("uniformly random states", XR), ("Gibbs states with at least m sites off the anchor", XG)):
        if len(X) == 0:
            log(f"(b) {name}: none"); continue
        gX = np.concatenate([G.bulk_energy(X[s:s + 250]) for s in range(0, len(X), 250)])
        IX = R8.interp(X, x0, m, lookupM); Rm = np.abs(gX - IX)
        P = np.full((len(X), n), -1)
        for i in range(n):
            mp = np.full(k[i], -1); mp[non[i]] = np.arange(len(non[i])); P[:, i] = mp[X[:, i]]
        env = np.zeros(len(X)); envmax = np.zeros(len(X)); envrev = np.zeros(len(X))
        for T, tab in zip(subs, tabs):
            idx = P[:, list(T)]; inS = (idx >= 0).all(axis=1)
            if inS.any():
                ii = tuple(idx[inS].T); env[inS] += tab[ii]; envmax[inS] += tab.max()
                envrev[inS] += tab[tuple(slice(None, None, -1) for _ in range(m))][ii]
        viol = int((Rm > env * (1 + 1e-12) + 1e-9).sum()); nz = Rm > 1e-9
        log(f"(b) {name}: {len(X)} states; |g - I_{M} g| <= sum of P9's tables: violations {viol}; largest remainder {Rm.max():.4g} kcal/mol; "
            f"ratio bound/remainder (remainder > 1e-9; {int(nz.sum())} states): smallest {float((env[nz] / Rm[nz]).min()) if nz.any() else float('nan'):.2f}, "
            f"median {float(np.median(env[nz] / Rm[nz])) if nz.any() else float('nan'):.1f}; mean of the resolved bound {BETA * env.mean():.4g} kT against "
            f"{BETA * envmax.mean():.4g} kT with the per-subset maxima (ratio {envmax.mean() / env.mean():.1f}); control C2 (tables reversed): "
            f"{int((Rm > envrev + 1e-9).sum())} violations [{time.time() - t0:.0f}s]")
        res[name] = dict(n=int(len(X)), viol=viol, maxR=float(Rm.max()))
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
