#!/usr/bin/env python3
"""WHICH SITE SHARES?  The theory division's Proposition 11.18f (read in their report at commit f7df44f) tested on an
enumerated real instance, with the structure that makes it computable -- coordinator's script (task: THY-RES-0012
section 3.2, "we have not tried this on your instances").

Setting.  chat_T >= 0 on the m-subsets T (workstream P3's certified constants), Gamma(R) = sum_{T subset R} chat_T (the
envelope of a changed set R).  A vector of site penalties gamma covers iff  sum_{i in R} gamma_i >= Gamma(R)  for every R.
Gamma is supermodular (a non-negative combination of unanimity games), so
  * the minimal covering vectors are the CORE of the convex game Gamma:  sum_{i in R} gamma_i >= Gamma(R), with equality
    at R = all sites;  the allocations of Proposition 11.18f at level 1 parametrise exactly the core (the core of a sum
    of convex games is the sum of the cores; the core of a unanimity game is the simplex on its set);
  * its vertices are the MARGINAL VECTORS of the orderings of the sites:  gamma_i = Gamma(R_i) - Gamma(R_i minus i),
    R_i = i and the sites after it  (Shapley 1971, from memory) -- the formula of Proposition 11.18f(c) is the vertex
    of the ordering "most frozen first", which is Edmonds' greedy solution of  min sum_i p_i gamma_i  over the core;
  * equal shares (workstream P3's site form) are the Shapley value, the barycentre of the marginal vectors.
With the evaluated model A = f + I_{m-1} g and  m_-/+ = A -/+ pen_gamma  (exact evaluated terms, no allowances here):
    ln Z(m_-) = ln Z(A) + U(gamma),  U = ln E_A exp(+beta pen)    CONVEX in gamma  -> minimised over the core by
                                                                   Frank-Wolfe, whose linear oracle is the greedy
                                                                   vertex for the ordering by the TILTED marginals;
    ln Z(m_+) = ln Z(A) - L(gamma),  L = -ln E_A exp(-beta pen)   CONCAVE in gamma -> minimised at a vertex, i.e. at
                                                                   an ORDERING; local search over adjacent swaps.
The floor (U) is the end that can delocalise; convexity is what protects it: the optimum never puts more on a site than
the tilted law tolerates.  This script, on Ace-Leu12-NMe on the helix (4 096 states, enumerated; off-anchor
frequencies 0.08, 0.11, 0.27 at three sites and ~0 at nine) at orders 4, 5, 6:
  (1) chat_T for every T by workstream P6's closed form (complement excluded); Gamma(R) for all R; supermodularity and
      the core property of every vector used are CHECKED exhaustively (4 096 sets);
  (2) U, L and the bracket U + L for: equal shares; the vertex "most frozen first" (ordering by the exact marginals of
      A; the theory division's rule); the vertex "most mobile first" (the opposite ordering); the Frank-Wolfe optimum
      of U; the best ordering found for L; and the combination  floor = Frank-Wolfe optimum, ceiling = best ordering;
  (3) for comparison: equal pair shares, equal triple shares (all in window), and the envelope itself;
  (4) the same greedy vertex computed WITHOUT enumerating subsets (n + 1 closed-form sums on nested sets), as it would
      be at thirty residues.
What is whose: the allocation problem, its convexity, the first-order rule -- the theory division (Proposition
11.18f); the certified constants -- P3; the closed forms -- P6; the reading as a convex game, Frank-Wolfe over the core
and the ordering search -- the coordinator (the game-theoretic facts are classical and cited from memory).
Run:  python3 -B allocation_core_test.py L12 H > allocation_core_test_L12_H.log               (orders 4, 5, 6)
      python3 -B allocation_core_test.py L12 H 3 m3 > allocation_core_test_L12_H_m3.log       (order 3; JSON suffix _m3)
"""
import os, sys, math, json, time, itertools, importlib, resource
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nested_sampler as NS                      # sets up the caches and imports p6lib (L), pwmodel (pw)
L, pw, BETA = NS.L, NS.pw, NS.BETA
from site_allocation_fw import waterfill_bound   # the a-priori bound for the site level (its statement is in its docstring)


def log(s): print(s, flush=True)


def marginal_vector(order, Gam_of_mask, n):
    """gamma for the ordering `order` (first = charged first = takes Gamma(N) - Gamma(N minus it))."""
    g = np.zeros(n); R = (1 << n) - 1
    for i in order:
        g[i] = Gam_of_mask[R] - Gam_of_mask[R & ~(1 << i)]; R &= ~(1 << i)
    return g


def main():
    seq = sys.argv[1] if len(sys.argv) > 1 else "L12"; bb = sys.argv[2] if len(sys.argv) > 2 else "H"
    orders = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else [4, 5, 6]
    tag = ("_" + sys.argv[4]) if len(sys.argv) > 4 else ""                                  # suffix of the JSON file, for runs at other orders
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    t0 = time.time(); out = []
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = np.array(x0)
    st, g, src = L.enumerate_g(G, seq, bb, tau, verbose=False)
    f = pw.f_energy(st, c0, h, J); E = f + g; lnZE = float(logsumexp(-BETA * E))
    ch = (st != x0[None]); mask = (ch * (1 << np.arange(n))[None]).sum(1)
    pE = np.exp(-BETA * E - lnZE); pi_true = pE @ ch
    log(f"=== {seq}/{bb}: {n} sites, states per site {k}, {len(st)} assignments enumerated; exact ln Z(E) = {lnZE:.9f}; "
        f"off-anchor frequencies under the true ensemble: " + " ".join(f"{v:.3f}" for v in pi_true))
    assert len(st) == np.prod(k)
    nm = 1 << n
    single_cost = np.array([BETA * (E[np.flatnonzero((mask == (1 << i)))].min() - E0) for i in range(n)])   # cheapest single change at site i, kT
    for m in orders:
        t1 = time.time(); M = m - 1
        GF = L.GFBound2(G, x0, L.EnvelopeSup(G), K=m)
        subs = list(itertools.combinations(range(n), m))
        se, cr = L.GFBatch(GF).totals(m, [tuple(i for i in range(n) if i not in T) for T in subs]); chat = np.maximum(se + cr, 0.0)
        # Gamma(R) for every set R (zeta transform over subsets)
        Gam = np.zeros(nm)
        for T, v in zip(subs, chat): Gam[sum(1 << i for i in T)] += v
        for i in range(n):
            bit = 1 << i; idx = np.arange(nm); hi = idx[(idx & bit) != 0]; Gam[hi] += Gam[hi ^ bit]
        GamN = Gam[nm - 1]
        # supermodularity, exhaustively: Gamma(R + i + j) - Gamma(R + i) - Gamma(R + j) + Gamma(R) >= 0
        worst = 0.0; idx = np.arange(nm)
        for i in range(n):
            for j in range(i + 1, n):
                R = idx[((idx >> i) & 1 == 0) & ((idx >> j) & 1 == 0)]
                worst = min(worst, float((Gam[R | (1 << i) | (1 << j)] - Gam[R | (1 << i)] - Gam[R | (1 << j)] + Gam[R]).min()))
        d, nball, srcb = L.ball_terms(G, x0, M, seq, bb, tau, verbose=False)
        A = f + pw.expansion_value(d, st); lnZA = float(logsumexp(-BETA * A)); pA = np.exp(-BETA * A - lnZA)
        env = Gam[mask]; rem = E - A
        assert (np.abs(rem) <= env + 1e-8).all()
        piA = pA @ ch
        bits = ((np.arange(nm)[:, None] >> np.arange(n)[None]) & 1).astype(float)          # (2^n, n)

        def pen_of(gam): return ch @ gam

        def UL(gam):
            p = BETA * pen_of(gam)
            return float(logsumexp(-BETA * A + p) - lnZA), float(lnZA - logsumexp(-BETA * A - p))

        def in_core(gam):
            return float((bits @ gam - Gam).min()), float(gam.sum() - GamN)

        def tilted(gam, sign):
            w = -BETA * A + sign * BETA * pen_of(gam); w = np.exp(w - logsumexp(w)); return w @ ch

        S = np.zeros(n)
        for T, v in zip(subs, chat):
            for i in T: S[i] += v
        g_eq = S / m
        # orderings: frozen first by the marginals of A, ties (marginal below 1e-12) by the cost of the cheapest single change
        key_frozen = sorted(range(n), key=lambda i: (round(float(piA[i]), 12), -single_cost[i]))
        g_fro = marginal_vector(key_frozen, Gam, n); g_mob = marginal_vector(key_frozen[::-1], Gam, n)
        # (4) the same vertex without enumerating subsets: n + 1 closed-form sums on nested sets
        nested = [tuple(key_frozen[:j]) for j in range(n + 1)]                              # excluded sets
        se2, cr2 = L.GFBatch(GF).totals(m, nested); tot2 = se2 + cr2
        g_fro_cf = np.zeros(n)
        for j, i in enumerate(key_frozen): g_fro_cf[i] = tot2[j] - tot2[j + 1]
        dev_cf = float(np.abs(g_fro_cf - g_fro).max())
        # Frank-Wolfe for U over the core; linear oracle = greedy vertex for the ordering by the tilted marginals (ascending)
        gam = g_fro.copy() if UL(g_fro)[0] < UL(g_eq)[0] else g_eq.copy(); gap = float("inf"); it = 0
        for it in range(1, 2001):
            pt = tilted(gam, +1.0)                                                         # gradient of U / beta
            order = sorted(range(n), key=lambda i: (pt[i], -single_cost[i])); v = marginal_vector(order, Gam, n)
            gap = BETA * float(pt @ (gam - v))                                             # duality gap of U, nats
            if gap < 1e-10: break
            # exact line search on the segment (U convex along it)
            lo_, hi_ = 0.0, 1.0
            for _ in range(60):
                a1 = lo_ + (hi_ - lo_) / 3; a2 = hi_ - (hi_ - lo_) / 3
                if UL(gam + a1 * (v - gam))[0] < UL(gam + a2 * (v - gam))[0]: hi_ = a2
                else: lo_ = a1
            gam = gam + 0.5 * (lo_ + hi_) * (v - gam)
        g_fw = gam; fw_it = it; fw_gap = gap
        # best ordering for L by adjacent swaps, from frozen first
        order = list(key_frozen); bestL = UL(marginal_vector(order, Gam, n))[1]; improved = True; swaps = 0
        while improved:
            improved = False
            for a_ in range(n - 1):
                o2 = order[:]; o2[a_], o2[a_ + 1] = o2[a_ + 1], o2[a_]; l2 = UL(marginal_vector(o2, Gam, n))[1]
                if l2 < bestL - 1e-13: order, bestL, improved = o2, l2, True; swaps += 1
        g_ord = marginal_vector(order, Gam, n)
        # comparison forms (exact evaluated terms, no allowances, all pairs / triples in window): equal pair and triple shares
        Gp = np.zeros((n, n)); G3 = {}
        for T, v in zip(subs, chat):
            for i, j in itertools.combinations(T, 2): Gp[i, j] += v
            for tr in itertools.combinations(T, 3): G3[tr] = G3.get(tr, 0.0) + v
        chf = ch.astype(float)
        pen_pair = np.einsum("si,ij,sj->s", chf, np.triu(Gp, 1), chf) / math.comb(m, 2)
        pen_tri = np.zeros(len(st))
        for (i, j, l_), v in G3.items(): pen_tri += v * (ch[:, i] & ch[:, j] & ch[:, l_])
        pen_tri /= math.comb(m, 3)

        def UL_pen(p):
            p = BETA * p; return float(logsumexp(-BETA * A + p) - lnZA), float(lnZA - logsumexp(-BETA * A - p))

        rows = []
        for name, gam in (("equal shares (P3's site form; the Shapley value)", g_eq), ("vertex, most frozen first (Proposition 11.18f(c))", g_fro),
                          ("vertex, most mobile first", g_mob), ("Frank-Wolfe optimum of U over the core", g_fw), ("best ordering found for L", g_ord)):
            u, l_ = UL(gam); c1, c2 = in_core(gam)
            assert c1 > -1e-9 * max(1.0, GamN) and abs(c2) < 1e-9 * max(1.0, GamN), (name, c1, c2)
            pmin = float((pen_of(gam) - env).min()); assert pmin > -1e-9 * max(1.0, GamN)
            a_, b_ = lnZA - l_, lnZA + u; assert a_ - 1e-9 <= lnZE <= b_ + 1e-9
            rows.append((name, u, l_, float(BETA * (pA @ pen_of(gam))), float(BETA * gam.max())))
        for name, p in (("equal pair shares, all pairs", pen_pair), ("equal triple shares, all triples", pen_tri), ("the envelope itself", env)):
            assert (p - env > -1e-9 * max(1.0, GamN)).all()
            u, l_ = UL_pen(p); rows.append((name, u, l_, float(BETA * (pA @ p)), float("nan")))
        u_fw, l_ord = UL(g_fw)[0], UL(g_ord)[1]
        a_i = np.array([float(pA[np.flatnonzero(mask == (1 << i))].max()) for i in range(n)])     # the cheapest single-change state at each site, under A
        wf, g_wf, lam = waterfill_bound(a_i, BETA * GamN)
        assert u_fw >= wf - 1e-9, (u_fw, wf)
        log(f"--- order {m}: Gamma_{m} = {BETA * GamN:.4f} kT from {len(subs)} constants; ball {nball}; supermodularity of Gamma over all sets: least second difference "
            f"{worst:.2e}; ln Z(A) = {lnZA:.9f} (ln Z(E) - ln Z(A) = {lnZE - lnZA:+.2e}); off-anchor frequencies under A: " + " ".join(f"{v:.3f}" for v in piA)
            + f"; cheapest single change, kT: " + " ".join(f"{v:.1f}" for v in single_cost) + f" [{time.time() - t1:.0f}s]")
        log(f"    ordering 'most frozen first': {key_frozen}; the same vertex from {n + 1} closed-form sums on nested sets, without enumerating subsets: "
            f"max deviation {dev_cf:.2e} kcal/mol; Frank-Wolfe: {fw_it} steps, duality gap {fw_gap:.1e} nats; ordering search: {swaps} improving swaps, final {order}")
        log("    site penalties, kT:  equal " + " ".join(f"{BETA * v:.2f}" for v in g_eq) + " | frozen first " + " ".join(f"{BETA * v:.2f}" for v in g_fro)
            + " | Frank-Wolfe " + " ".join(f"{BETA * v:.2f}" for v in g_fw))
        log("    allocation | U (upper end, floor model) | L (lower end, ceiling model) | U + L (bracket, nats) | first order 2 beta <pen>_A | largest site penalty, kT")
        for name, u, l_, fo, gmax in rows:
            log(f"    {name:52s} | {u:12.6g} | {l_:12.6g} | {u + l_:12.6g} | {2 * fo:10.4g} | {gmax:8.3f}")
        log(f"    COMBINATION floor = Frank-Wolfe optimum, ceiling = best ordering: bracket {u_fw + l_ord:.6g} nats: ln Z(E) in [{lnZA - l_ord:.6f}, {lnZA + u_fw:.6f}] "
            f"(exact {lnZE:.6f})")
        log(f"    A-PRIORI BOUND for the site level (water-filling over the cheapest single-change states): U >= {wf:.6g} for every covering vector of site "
            f"penalties (Frank-Wolfe optimum: {u_fw:.6g}); water-filling penalties, kT: " + " ".join(f"{v:.2f}" for v in g_wf))
        # the sharper form: the off-anchor marginals under A in place of the single-change states (docstring of waterfill_bound)
        wf2, g_wf2, lam2 = waterfill_bound(np.maximum(piA, 1e-300), BETA * GamN)
        assert u_fw >= wf2 - 1e-9, (u_fw, wf2)
        gw = g_wf2 / BETA; gw = gw * (GamN / gw.sum()) if gw.sum() > 0 else gw
        cmin, _ = in_core(gw); u_w, l_w = UL(gw)
        log(f"    SHARPER, with the off-anchor marginals under A in place of the single-change states: U >= {wf2:.6g} for every covering vector; "
            f"water-filling penalties, kT: " + " ".join(f"{v:.2f}" for v in g_wf2))
        log(f"    that water-filling vector as a penalty vector: least slack of the covering constraints over all {nm} sets {BETA * cmin:.4g} kT "
            f"({'it covers: a valid allocation' if cmin > -1e-9 * max(1.0, GamN) else 'it does NOT cover: not a valid allocation'}); "
            f"its U = {u_w:.6g}, L = {l_w:.6g} (meaningful only if it covers)")
        out.append(dict(m=m, Gamma_kT=BETA * GamN, supermod_min=worst, lnZA=lnZA, piA=[float(v) for v in piA], order_frozen=key_frozen, order_best_L=order,
                        dev_closed_form=dev_cf, fw_steps=fw_it, fw_gap=fw_gap, rows=[dict(name=r[0], U=r[1], L=r[2], first_order=2 * r[3], gmax_kT=r[4]) for r in rows],
                        combination=u_fw + l_ord, waterfill_bound=wf, waterfill_bound_marginals=wf2, waterfill_slack_kT=float(BETA * cmin), waterfill_U=u_w, waterfill_L=l_w, gamma_eq_kT=[float(BETA * v) for v in g_eq], gamma_frozen_kT=[float(BETA * v) for v in g_fro],
                        gamma_fw_kT=[float(BETA * v) for v in g_fw]))
    json.dump(dict(seq=seq, bb=bb, lnZE=lnZE, pi_true=[float(v) for v in pi_true], orders=out), open(os.path.join(HERE, f"allocation_core_test_{seq}_{bb}{tag}.json"), "w"), indent=1)
    log(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
