#!/usr/bin/env python3
"""Which evaluations are worth making?  (docs/science/OPEN_PROBLEMS.md D14; an estimate, not a certificate.)

The certificate evaluates g on the whole Hamming ball of radius m - 1; what is left is bounded by the resolved tables
Theta_T of the m-subsets T (workstream P9), and the first-order width of the box is 2 beta sum_T <Theta_T(x_T) [T off]>.
If a few subsets carry most of that sum, a down-closed family of subsets chosen by gain per evaluation -- evaluate g on
the states with exactly T off the anchor only for the subsets that matter -- reaches nearly the same box with far fewer
evaluations than the next ball.  This script measures how concentrated the sum is: for each m-subset T its
contribution c_T = beta <Theta_T(x_T) [all sites of T off the anchor]> on a Gibbs sample of the pairwise model with
the evaluated one-site terms (seed 4242, the guiding sample of first_order_recovery.py; uncertified), and its cost
n_T = prod_{i in T} (k_i - 1) evaluations.  Printed: the share of the subsets, and of the evaluations of the shell of
radius m, that carry 50, 90, 99, 99.9 per cent of the sum when subsets are taken (a) by contribution, (b) by
contribution per evaluation; the same split by the span of the subset (largest site minus smallest); and the Monte
Carlo error of the total.  Control: the same statistic for tables shuffled among the subsets (the concentration must
then be that of the occupation alone).
Because a sample of a thousand states leaves most subsets with no weight at all, the statistic is repeated with the
occupation taken from the product of the sample's one-site marginals (part (4)), where the control separates what the
tables contribute from what the occupation contributes.
Run: python3 -B subset_concentration.py K12 3 > subset_concentration_K12_m3.log
"""
import os, sys, time, glob, itertools, resource
import numpy as np
import nested_sampler as NS
from window_model_occ import gibbs_sample
L, pw = NS.L, NS.pw
BETA = L.BETA
HERE = os.path.dirname(os.path.abspath(__file__)); SCI = os.path.normpath(os.path.join(HERE, ".."))


def conc(c, cost, key):
    order = np.argsort(-key); cs = np.cumsum(c[order]) / c.sum(); ce = np.cumsum(cost[order]) / cost.sum(); out = []
    for q in (0.5, 0.9, 0.99, 0.999):
        j = int(np.searchsorted(cs, q)) + 1; out.append((q, j / len(c), float(ce[min(j, len(c)) - 1])))
    return out


def main():
    seq, m = sys.argv[1], int(sys.argv[2]); bb = "H"; t0 = time.time()
    tau = 0.60 if ":" in seq else dict(S=0.70, V=0.70, K=0.70, L=0.60, F=0.60)[seq[0]]
    tag = f"{seq.replace(':', 'c')}_{bb}_{tau:.2f}"
    G, c0, h, J, x0, E0 = L.setup(seq, bb, tau); n, k = G.ns, list(G.k); x0 = [int(v) for v in x0]; X0 = np.array(x0)
    subs = list(itertools.combinations(range(n), m)); non = [[b for b in range(k[i]) if b != x0[i]] for i in range(n)]
    files = sorted(glob.glob(os.path.join(SCI, "ws_P9", "cache", f"theta2_{tag}_m{m}*.npz"))) or sorted(glob.glob(os.path.join(SCI, "p9_verification", "cache", f"theta2_{tag}_m{m}*.npz")))
    tabs = [None] * len(subs)
    for fn in files:
        z = np.load(fn)
        for j in z["idx"]: tabs[int(j)] = np.array(z[f"t{int(j)}"], dtype=float)
    assert all(t is not None for t in tabs)
    X = gibbs_sample(pw, G, c0, h, J, x0, k, BETA, np.random.default_rng(4242))
    posn = [np.full(k[i], -1) for i in range(n)]
    for i in range(n): posn[i][non[i]] = np.arange(len(non[i]))
    off = X != X0[None]
    print(f"=== {seq} on {bb}, tau {tau}: {n} sites, states per site {k}; order m = {m}: {len(subs)} subsets; Gibbs sample of {len(X)} states (seed 4242), {float(off.sum(1).mean()):.2f} sites off the anchor on average [{time.time() - t0:.0f}s]", flush=True)

    def contributions(tables):
        c = np.zeros(len(subs)); c2 = np.zeros(len(subs))
        for q, (T, tab) in enumerate(zip(subs, tables)):
            sel = off[:, list(T)].all(1)
            if sel.any():
                v = tab[tuple(posn[i][X[sel, i]] for i in T)]; c[q] = BETA * v.sum() / len(X); c2[q] = BETA ** 2 * (v ** 2).sum() / len(X)
        return c, c2
    c, c2 = contributions(tabs); cost = np.array([np.prod([len(non[i]) for i in T]) for T in subs], dtype=float)
    tot = c.sum(); se = float(np.sqrt(max(c2.sum() - tot ** 2, 0.0) / len(X)))
    print(f"(1) first-order width of the box at order {m}: 2 beta <env> = {2 * tot:.4g} nats (Monte Carlo standard error of the sum, ignoring correlation along the chains: {2 * se:.2g}); "
          f"subsets with a non-zero contribution on the sample: {int((c > 0).sum())} of {len(subs)}; evaluations in the shell of radius {m}: {int(cost.sum())}")
    print("| subsets taken by | share of the sum | share of the subsets needed | share of the shell's evaluations they cost |")
    print("|---|---|---|---|")
    for name, key in (("contribution", c), ("contribution per evaluation", c / cost)):
        for q, fs, fe in conc(c, cost, key): print(f"| {name} | {q:g} | {fs:.3f} | {fe:.3f} |")
    span = np.array([T[-1] - T[0] for T in subs])
    print("(2) by the span of the subset (largest site minus smallest): " + "; ".join(f"span {s_}: {int((span == s_).sum())} subsets, {100 * c[span == s_].sum() / tot:.2f} % of the sum" for s_ in sorted(set(span.tolist()))))
    # control: tables shuffled among subsets of the same shape
    rng = np.random.default_rng(7); perm = rng.permutation(len(subs)); shuf = [None] * len(subs)
    for q in range(len(subs)):
        t = tabs[perm[q]]; shp = tuple(len(non[i]) for i in subs[q])
        shuf[q] = np.resize(t, shp) if t.shape != shp else t
    cs_, _ = contributions(shuf)
    a = conc(c, cost, c)[2]; b = conc(cs_, cost, cs_)[2]
    print(f"(3) control, tables shuffled among the subsets: 99 % of the sum then needs {b[1]:.3f} of the subsets (against {a[1]:.3f} with the true assignment); total {2 * cs_.sum():.4g} nats")
    # ---- the same with the occupation taken from the product of the sample's one-site marginals (no Monte Carlo sparsity: every subset has a weight)
    pm = [((np.bincount(X[:, i], minlength=k[i]) + 0.5) / (len(X) + 0.5 * k[i]))[non[i]] for i in range(n)]

    def contributions_product(tables):
        c = np.zeros(len(subs))
        for q, (T, tab) in enumerate(zip(subs, tables)):
            v = tab
            for p_ in reversed(range(len(T))): v = v @ pm[T[p_]]
            c[q] = BETA * float(v)
        return c
    cp = contributions_product(tabs); cps = contributions_product(shuf)
    print(f"(4) occupation from the product of the one-site marginals (smoothed counts; a model of the occupation, not the ensemble): 2 beta <env> = {2 * cp.sum():.4g} nats")
    print("| subsets taken by | share of the sum | share of the subsets needed | share of the shell's evaluations they cost | control: share of the subsets needed with shuffled tables |")
    print("|---|---|---|---|---|")
    ctrl = conc(cps, cost, cps)
    for (q, fs, fe), (_, fsc, _) in zip(conc(cp, cost, cp / cost), ctrl): print(f"| contribution per evaluation | {q:g} | {fs:.3f} | {fe:.3f} | {fsc:.3f} |")
    print("    by the span of the subset: " + "; ".join(f"span {s_}: {100 * cp[span == s_].sum() / cp.sum():.2f} %" for s_ in sorted(set(span.tolist()))))
    tmax = np.array([float(t.max()) for t in tabs])
    print(f"    the tables themselves: largest entry per subset from {BETA * tmax.min():.2e} to {BETA * tmax.max():.2e} kT (median {BETA * float(np.median(tmax)):.2e}); "
          f"the {max(1, len(subs) // 10)} subsets with the largest maxima hold {100 * np.sort(tmax)[::-1][:max(1, len(subs) // 10)].sum() / tmax.sum():.1f} % of the sum of the maxima")
    print(f"ALL DONE {time.time() - t0:.0f} s; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024:.0f} MB")


if __name__ == "__main__":
    main()
