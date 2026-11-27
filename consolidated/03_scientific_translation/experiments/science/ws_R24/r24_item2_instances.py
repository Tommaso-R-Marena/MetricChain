#!/usr/bin/env python3
"""R24, item 2 (iii): the Ensemble division's bound (b) on Lys5 and LKSE:5, recomputed by the referee, and its MOST FAVOURABLE
use as a falsification test that the referee could construct.

Taken from the programme: the energy of every state (the evaluator of workstreams P3/P6, as thermal_union_bound.py calls it:
the instance itself).  Everything else is computed here.
  reference  pi = product of the anchored one-body weights;  rest g = beta (E - first-order interpolant around the anchor);
  envelopes  one-sided  delta_i(s, t) = max over the other sites of g(s, .) - g(t, .);  symmetric = max(delta, delta^T).
Checks of what the texts say: these are the least site-additive envelopes (every single-site constraint is attained; general
pairs hold by telescoping -- tested on random pairs, control 0.99 delta); the least scale containing the truth is 1;
sigma, p, tau, sum tau, TV at the anchor; the one-site ratio test.
The most favourable use of (b), "TV(mu, mu*_{a,b}) <= sum_i tau_i(b) for members of the class of scale b":
  U1  every centre a (not 232): for each scale b all centres with every cap satisfied and sum tau < 1 are tested with the exact
      total variation (exhaustive after this pruning, which loses nothing: TV <= 1);
  U2  SUB-SYSTEMS: the marginal of a member on a set S of sites is a member of the class on S (sum the pair constraint over
      the other sites), so TV(mu_S, mu*_{a_S,b}) <= sum_{i in S} tau_i(b) -- fewer terms on the right; all S, all centres a_S;
  U3  for comparison the EXACT least scale consistent with the marginal on S: the ratio test on the sub-system,
      b_S = max_{x_S != y_S} [ln(mu_S(y) pi_S(x) / (mu_S(x) pi_S(y)))]_+ / d_S(x, y)   (exact: mu_S x pi_rest is then a member).
Run: python3 -B r24_item2_instances.py K5 > r24_item2_instances_K5.log ;  ... LKSE:5 > r24_item2_instances_LKSEc5.log
"""
import os, sys, math, time, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PI = os.path.normpath(os.path.join(HERE, "..", "pi_inference"))
sys.path.insert(0, HERE)
import r24_common as C


def energies(seq):
    fn = os.path.join(HERE, f"cache_E_{seq.replace(':', 'c')}.npz")
    if os.path.exists(fn):
        z = np.load(fn); return z["E"], [int(v) for v in z["k"]], [int(v) for v in z["x0"]], float(z["beta"]), "my cache of the evaluator's values"
    sys.path.insert(0, PI)
    import nested_sampler as NS
    L, pw = NS.L, NS.pw; tau = 0.60 if ":" in seq else 0.70
    G, c0, h, J, x0, E0 = L.setup(seq, "H", tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]
    st = np.stack(np.meshgrid(*[np.arange(v) for v in k], indexing="ij"), axis=-1).reshape(-1, n)
    E = pw.f_energy(st, c0, h, J) + np.concatenate([G.bulk_energy(st[s:s + 256]) for s in range(0, len(st), 256)])
    np.savez(fn, E=E, k=np.array(k), x0=np.array(x0), beta=L.BETA)
    return E, k, x0, float(L.BETA), "evaluated now"


def main():
    seq = sys.argv[1]; t0 = time.time(); E, k, x0, BETA, src = energies(seq); n = len(k); N = int(np.prod(k))
    E = (BETA * (E - E[np.ravel_multi_index(x0, k)])).reshape(k)
    w = np.exp(-(E - E.min())); mu = w / w.sum()
    ax = lambda i: tuple(j for j in range(n) if j != i); sh = lambda i: [k[i] if j == i else 1 for j in range(n)]
    one = [np.array(E[tuple(x0[j] if j != i else slice(None) for j in range(n))]) for i in range(n)]
    I1 = sum(one[i].reshape(sh(i)) for i in range(n)); g = E - I1
    pis = [np.exp(-(o - o.min())) / np.exp(-(o - o.min())).sum() for o in one]; marg = [mu.sum(axis=ax(i)) for i in range(n)]
    ball1 = max(float(np.abs(g[tuple(x0[j] if j != i else slice(None) for j in range(n))]).max()) for i in range(n))
    print(f"=== {seq}: {n} sites, states per site {k}, {N} states ({src}), anchor {x0}; population of the anchor {float(mu[tuple(x0)]):.4f}; mean number of sites off {float(sum(1 - marg[i][x0[i]] for i in range(n))):.4f}; "
          f"g: range [{g.min():.2f}, {g.max():.2f}] kT, Gibbs mean of |g| {float((mu * np.abs(g)).sum()):.3f}; |g| on the ball of radius 1: {ball1:.1e} [{time.time() - t0:.0f}s]", flush=True)
    dl1 = []
    for i in range(n):
        gi = np.moveaxis(g, i, 0).reshape(k[i], -1); dl1.append((gi[:, None, :] - gi[None, :, :]).max(axis=2))        # [s, t] = max over the others of g(s, .) - g(t, .)
    rng = np.random.default_rng(31)
    for nm, deltas in (("one-sided", dl1), ("symmetric", [np.maximum(D, D.T) for D in dl1])):
        # ---- least envelope, scale one
        tri = max(float((D[:, None, :] - D[:, :, None] - D[None, :, :]).max()) for D in deltas)
        P = 200000; xs = np.stack([rng.integers(0, kk, P) for kk in k], axis=1); ys = np.stack([rng.integers(0, kk, P) for kk in k], axis=1)
        dxy = sum(deltas[i][xs[:, i], ys[:, i]] for i in range(n)); gx = g[tuple(xs.T)]; gy = g[tuple(ys.T)]
        v1 = int((gx - gy > dxy + 1e-9).sum()); v99 = int((gx - gy > 0.99 * dxy + 1e-9).sum()); ratio = float(((gx - gy) / np.maximum(dxy, 1e-300))[dxy > 1e-9].max())
        # EVERY single-site pair of states (x, y differ in one site), directly on the array g: violations at scale 1 (must be 0) and at
        # scale 0.99 (must be positive: this is what "the least scale is 1" means); pairs at which the constraint is attained at scale 1
        v_one = 0; v_099 = 0; att = 0; totp = 0
        for i in range(n):
            gi = np.moveaxis(g, i, 0)
            for s in range(k[i]):
                for t in range(k[i]):
                    if s != t and deltas[i][s, t] > 1e-12:
                        df = gi[s] - gi[t]; totp += df.size; v_one += int((df > deltas[i][s, t] + 1e-9).sum()); v_099 += int((df > 0.99 * deltas[i][s, t] + 1e-9).sum())
                        att += int((np.abs(df - deltas[i][s, t]) < 1e-9).sum())
        print(f"--- {nm} envelope: triangle inequality violated by at most {max(tri, 0):.1e}; EVERY single-site pair of states ({totp}): g(x) - g(y) <= delta_i(x_i, y_i) violated at {v_one} (must be 0), attained at {att}; "
              f"control, the same against 0.99 delta: {v_099} violations (must be positive) -> the least site-additive envelope, least scale 1.  General pairs (which follow by telescoping): {P} random pairs, {v1} violations, "
              f"largest (g(x) - g(y)) / d(x, y) = {ratio:.4f}; against 0.99 d: {v99} violations (for information: random general pairs need not come near the extreme)")
        def member(b, a):
            ms = [pis[i] * np.exp(-b * deltas[i][:, a[i]]) for i in range(n)]; return [v / v.sum() for v in ms]

        def prodm(ms, S=None):
            S = range(n) if S is None else S; out = 1.0
            for q, i in enumerate(S): out = out * ms[i].reshape([len(ms[i]) if j == q else 1 for j in range(len(S))])
            return out
        ms = member(1.0, x0); sig = np.array([ms[i][x0[i]] for i in range(n)]); p = np.array([marg[i][x0[i]] for i in range(n)]); tau = 1 - p / sig; TV = 0.5 * float(np.abs(mu - prodm(ms)).sum())
        b1 = 0.0
        for i in range(n):
            lr = np.log(marg[i][None, :] * pis[i][:, None] / (marg[i][:, None] * pis[i][None, :]))
            with np.errstate(divide="ignore", invalid="ignore"): q = np.where(deltas[i] > 1e-12, lr / deltas[i], 0.0)
            np.fill_diagonal(q, 0.0); b1 = max(b1, float(q.max()))
        print(f"    at the anchor: sigma {', '.join(f'{v:.4f}' for v in sig)}; p {', '.join(f'{v:.4f}' for v in p)}; **sum tau = {float(tau.sum()):.4f}**, **TV = {TV:.4f}**; largest delta_i(s, t) {max(float(D.max()) for D in deltas):.1f} kT; "
              f"one-site ratio test: b >= **{b1:.4f}**")
        # ---- U1 / U2: (b) on the whole system and on every sub-system, EVERY centre, exhaustively.
        # Pruning that loses nothing: with pt = the product of the true one-site marginals on S,
        #     TV(mu_S, mu*_{a,b}) <= TV(mu_S, pt) + sum_{i in S} TV(marg_i, m_i^{a_i,b})        (triangle inequality; products),
        # so the test can fire at the centre a only if  sum_i [tau_i - t_i](b; a_i) < T0 := TV(mu_S, pt)  -- a separable condition.
        grid = [0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        def fire_scan(S):
            size = len(S); kS = [k[i] for i in S]; muS = mu.sum(axis=tuple(j for j in range(n) if j not in S)).reshape(kS)
            pt = prodm([marg[i] for i in S], range(size)) if size > 1 else marg[S[0]]; T0 = 0.5 * float(np.abs(muS - np.asarray(pt).reshape(kS)).sum())
            out = {}; ntest = 0; capped = False
            for b in grid:
                per = []
                for i in S:
                    M = pis[i][:, None] * np.exp(-b * deltas[i]); M = M / M.sum(axis=0, keepdims=True)              # column s: the one-site member centred at s
                    sg = np.diag(M).copy(); tauq = np.where(marg[i] <= sg * (1 + 1e-12), 1 - marg[i] / sg, np.inf)
                    tq = 0.5 * np.abs(marg[i][:, None] - M).sum(axis=0); per.append((tauq, tauq - tq, M))
                suff = [0.0] * (size + 1)
                for q in range(size - 1, -1, -1):
                    fin = per[q][1][np.isfinite(per[q][1])]; suff[q] = suff[q + 1] + (float(fin.min()) if len(fin) else np.inf)
                cand = []

                def rec(q, a, tot):
                    if len(cand) > 60000 or not np.isfinite(suff[q]) or tot + suff[q] >= T0: return
                    if q == size: cand.append((tot, tuple(a))); return
                    for s_ in np.argsort(per[q][1]):
                        v_ = per[q][1][s_]
                        if not np.isfinite(v_) or tot + v_ + suff[q + 1] >= T0: break
                        rec(q + 1, a + [int(s_)], tot + v_)
                rec(0, [], 0.0); capped = capped or len(cand) > 60000; fired = 0; bm = -1e9
                for _, a_ in cand:
                    mm = prodm([per[q][2][:, a_[q]] for q in range(size)], range(size)) if size > 1 else per[0][2][:, a_[0]]
                    tv = 0.5 * float(np.abs(muS - np.asarray(mm).reshape(kS)).sum()); st_ = float(sum(per[q][0][a_[q]] for q in range(size))); ntest += 1
                    fired += int(tv > st_ + 1e-12); bm = max(bm, tv - st_)
                out[b] = (fired, len(cand), bm)
            return out, T0, ntest, capped
        res_all, T0, ntest, capped = fire_scan(tuple(range(n))); bfire = max([b for b in grid if res_all[b][0] > 0], default=0.0)
        print(f"    U1 EVERY centre (exhaustive by a pruning that loses nothing{'; CAPPED at 60000 candidates somewhere' if capped else ''}; TV(mu, product of its own one-site marginals) = {T0:.4f}; {ntest} exact total variations): "
              + "; ".join(f"b = {b:g}: {res_all[b][0]} fire of {res_all[b][1]} candidates" + (f" (largest TV - sum tau {res_all[b][2]:+.4f})" if res_all[b][1] else "") for b in grid)
              + f"  ->  **(b) with the exact total variation as the datum, any centre, certifies b >= {bfire:g}** [{time.time() - t0:.0f}s]", flush=True)
        # ---- U2 on sub-systems; U3: the exact ratio test on the marginal of the sub-system
        rows = []
        for size in range(1, n):
            bS_fire = 0.0; bS_exact = 0.0; which = None; whichx = None; anycap = False
            for S in itertools.combinations(range(n), size):
                rS, _, _, cp = fire_scan(S); anycap = anycap or cp; bf = max([b for b in grid if rS[b][0] > 0], default=0.0)
                if bf > bS_fire: bS_fire = bf; which = S
                muS = mu.sum(axis=tuple(j for j in range(n) if j not in S)); kS = [k[i] for i in S]; NS_ = int(np.prod(kS))
                piS = prodm([pis[i] for i in S], range(size)) if size > 1 else pis[S[0]]
                lr = np.log(muS.reshape(kS) / np.asarray(piS).reshape(kS)).ravel()                                    # ln(mu_S / pi_S)
                XS = np.stack(np.meshgrid(*[np.arange(v) for v in kS], indexing="ij"), axis=-1).reshape(-1, size); bex = 0.0
                for c0_ in range(0, NS_, 512):
                    blk = XS[c0_:c0_ + 512]; dmat = sum(deltas[i][blk[:, q][:, None], XS[:, q][None, :]] for q, i in enumerate(S))   # d_S(x, y), x in the block
                    num = lr[None, :] - lr[c0_:c0_ + 512][:, None]                                                    # ln(mu(y) pi(x) / (mu(x) pi(y)))
                    with np.errstate(divide="ignore", invalid="ignore"): qq = np.where(dmat > 1e-12, num / dmat, 0.0)
                    bex = max(bex, float(qq.max()))
                if bex > bS_exact: bS_exact = bex; whichx = S
            rows.append((size, bS_fire, which, bS_exact, whichx, anycap))
        print("    | data: the marginals on every set of this many sites | (b) applied to the sub-system, every centre, with the exact TV of the marginal as the datum: certifies b >= | exact for these data (ratio test on the marginal): b >= |")
        print("    |---|---|---|")
        for size, bf, wh, bx, whx, cp in rows: print(f"    | {size} | {bf:g}{'' if wh is None else ' (sites ' + str(list(wh)) + ')'}{' [capped]' if cp else ''} | **{bx:.4f}** (sites {list(whx)}) |")
        print(f"    | {n} (the whole ensemble) | {bfire:g} | 1 (by construction) |  [{time.time() - t0:.0f}s]", flush=True)
        # the centre of least sum tau at scale 1: what (b) certifies as a statement about the ensemble, not as a test
        best = [int(np.argmin([1 - marg[i][s] / (pis[i][s] / float((pis[i] * np.exp(-deltas[i][:, s])).sum())) for s in range(k[i])])) for i in range(n)]
        msb = member(1.0, best); sgb = np.array([msb[i][best[i]] for i in range(n)]); pb = np.array([marg[i][best[i]] for i in range(n)])
        print(f"    as a statement, not a test: the centre of least sum tau at scale 1 is {best}: sum tau = {float((1 - pb / sgb).sum()):.4f}, TV = {0.5 * float(np.abs(mu - prodm(msb)).sum()):.4f} "
              f"(the class certifies that the ensemble is within {float((1 - pb / sgb).sum()):.2f} in total variation of that explicit product measure)")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {C.rss():.0f} MB")


if __name__ == "__main__":
    main()
