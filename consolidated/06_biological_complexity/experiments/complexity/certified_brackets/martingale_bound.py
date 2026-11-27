"""A certified second-order upper bound for many weak pair terms on a correlated reference (docs/complexity/CERTIFIED_BRACKETS.md).

Model: n sites with d states, reference energy E0 (a tree or chain of strong pair tables plus one-body terms),
perturbation V = sum over weak pairs e of eps_e(x_i, x_j) with oscillation o_e.  With <.>_0 the reference average,

    -beta <V>_0   <=   ln < exp(-beta V) >_0   <=   -beta <V>_0  +  (beta^2 / 8) * sum_t ( sum_e Gamma[t,e] * o_e )^2 ,

where the sites are revealed in the order 0..n-1 and
    Gamma[t,e] = 0   if both sites of e come before t,
               = 1   if t is a site of e,
               = max over histories x_<t and states a, a' of the total-variation distance between the conditional
                 laws (under the reference) of the not yet revealed sites of e given (x_<t, a) and (x_<t, a')   otherwise.
The total-range bound replaces the last sum by (sum_e o_e)^2.  The Gamma bound is NOT always the smaller of the two:
it counts a pair at both of its sites.  A sharper valid variant ("column form") bounds the direct part at site t by
    max_a sum_{e containing t} U_e(a)  -  min_a sum_{e containing t} L_e(a),      U_e(a) = max_b eps_e(a,b),  L_e(a) = min_b eps_e(a,b),
and the bound with the exact ranges of the martingale increments is sharper still (and costlier to compute).
The "variance form" (Bennett's inequality for every increment) is
    ln < exp(-beta (V - <V>_0)) >_0  <=  sum_t  v_t * (exp(beta b_t) - 1 - beta b_t) / b_t^2 ,
with v_t >= the conditional variance of the increment D_t and b_t >= -D_t for every history; here v_t, b_t are the
exact suprema over histories, computed by brute force.

This script checks the inequalities by EXHAUSTIVE ENUMERATION with floating point on small random models (the
reference laws, the conditional laws and Gamma are all computed by brute force, not by elimination), and prints the
exact value next to the bounds.  It is a sanity check of the statement, not an efficient implementation.

Usage: python3 martingale_bound.py [seed]
"""
import itertools
import math
import sys

import numpy as np


def run(rng, n, d, strong_scale, weak_scale, n_weak, beta=1.0, tree=True, verbose=True):
    sites = list(range(n))
    # reference: random tree (or chain) of strong pair tables + one-body terms
    ref_pairs = {}
    for i in range(1, n):
        j = int(rng.integers(0, i)) if tree else i - 1
        ref_pairs[(j, i)] = strong_scale * rng.normal(size=(d, d))
    one = strong_scale * rng.normal(size=(n, d))
    cand = [(i, j) for i in range(n) for j in range(i + 1, n) if (i, j) not in ref_pairs]
    idx = rng.choice(len(cand), size=min(n_weak, len(cand)), replace=False)
    weak = {cand[k]: weak_scale * rng.normal(size=(d, d)) for k in idx}
    confs = np.array(list(itertools.product(range(d), repeat=n)))
    E0 = one[np.arange(n)[None, :], confs].sum(axis=1)
    for (i, j), tab in ref_pairs.items():
        E0 += tab[confs[:, i], confs[:, j]]
    w0 = np.exp(-beta * (E0 - E0.min()))
    p0 = w0 / w0.sum()
    terms = {e: tab[confs[:, e[0]], confs[:, e[1]]] for e, tab in weak.items()}
    V = sum(terms.values())
    exact = math.log(float((p0 * np.exp(-beta * V)).sum()))
    mean = float((p0 * V).sum())
    osc = {e: float(tab.max() - tab.min()) for e, tab in weak.items()}
    total_range = sum(osc.values())
    hoeffding = -beta * mean + beta ** 2 * total_range ** 2 / 8

    # Gamma by brute force
    edges = list(weak)
    Gamma = np.zeros((n, len(edges)))
    for t in sites:
        # group configurations by history x_<t
        keys = [tuple(c[:t]) for c in confs]
        groups = {}
        for k, key in enumerate(keys):
            groups.setdefault(key, []).append(k)
        for ei, e in enumerate(edges):
            if e[1] < t:                      # both sites revealed before t (e = (i, j), i < j)
                continue
            if t in e:
                Gamma[t, ei] = 1.0
                continue
            later = [s for s in e if s > t]
            best = 0.0
            for key, members in groups.items():
                members = np.array(members)
                laws = []
                for a in range(d):
                    sel = members[confs[members, t] == a]
                    mass = p0[sel].sum()
                    if mass <= 0:
                        continue
                    law = np.zeros([d] * len(later))
                    np.add.at(law, tuple(confs[sel][:, s] for s in later), p0[sel] / mass)
                    laws.append(law)
                for a in range(len(laws)):
                    for b in range(a + 1, len(laws)):
                        best = max(best, 0.5 * float(np.abs(laws[a] - laws[b]).sum()))
            Gamma[t, ei] = best
    o = np.array([osc[e] for e in edges])
    ranges = Gamma @ o
    martingale = -beta * mean + beta ** 2 * float((ranges ** 2).sum()) / 8
    # column form: direct part by per-state envelopes, indirect part by Gamma
    col_ranges = np.zeros(n)
    for t in sites:
        up, lo, indirect = np.zeros(d), np.zeros(d), 0.0
        for ei, e in enumerate(edges):
            if t in e:
                tab = weak[e] if e[0] == t else weak[e].T          # rows indexed by the state of t
                up += tab.max(axis=1)
                lo += tab.min(axis=1)
            else:
                indirect += Gamma[t, ei] * o[ei]
        col_ranges[t] = (up.max() - lo.min()) + indirect
    column = -beta * mean + beta ** 2 * float((col_ranges ** 2).sum()) / 8

    # exact martingale ranges (sup over histories of the range of the Doob martingale increment), for comparison
    exact_ranges = np.zeros(n)
    vmax, bmax = np.zeros(n), np.zeros(n)          # for the variance (Bennett) form
    for t in sites:
        keys_prev = {}
        for k, c in enumerate(confs):
            keys_prev.setdefault(tuple(c[:t]), {}).setdefault(int(c[t]), []).append(k)
        r = 0.0
        for key, bya in keys_prev.items():
            vals, masses = [], []
            for a, mem in bya.items():
                mem = np.array(mem)
                mass = p0[mem].sum()
                if mass > 0:
                    vals.append(float((p0[mem] * V[mem]).sum() / mass))
                    masses.append(float(mass))
            r = max(r, max(vals) - min(vals))
            vals, masses = np.array(vals), np.array(masses) / sum(masses)
            mu = float((masses * vals).sum())
            vmax[t] = max(vmax[t], float((masses * (vals - mu) ** 2).sum()))
            bmax[t] = max(bmax[t], mu - float(vals.min()))            # -D_t <= mu - min
        exact_ranges[t] = r
    azuma_exact = -beta * mean + beta ** 2 * float((exact_ranges ** 2).sum()) / 8
    bennett = -beta * mean + sum(vmax[t] * (math.exp(beta * bmax[t]) - 1 - beta * bmax[t]) / bmax[t] ** 2
                                 for t in sites if bmax[t] > 0)
    var = float((p0 * (V - mean) ** 2).sum())
    ok = (-beta * mean <= exact + 1e-12) and (exact <= azuma_exact + 1e-12) and (exact <= bennett + 1e-12) and (azuma_exact <= column + 1e-9) \
        and (column <= martingale + 1e-9) and (exact <= hoeffding + 1e-12) \
        and bool(np.all(exact_ranges <= col_ranges + 1e-9)) and bool(np.all(col_ranges <= ranges + 1e-9))
    if verbose:
        print(f"   n={n} d={d} weak pairs={len(edges)}  beta*sum o_e={beta*total_range:6.2f} | gap above -beta<V>:  exact={exact + beta*mean:7.4f}  "
              f"beta^2 Var/2={beta**2*var/2:7.4f}  variance form={bennett + beta*mean:7.4f}  exact ranges={azuma_exact + beta*mean:7.4f}  column form={column + beta*mean:7.4f}  "
              f"Gamma form={martingale + beta*mean:7.4f}  total range={hoeffding + beta*mean:7.4f}  {'ok' if ok else 'VIOLATION'}")
    return ok, exact + beta * mean, azuma_exact + beta * mean, column + beta * mean, martingale + beta * mean, hoeffding + beta * mean, bennett + beta * mean


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    rng = np.random.default_rng(seed)
    allok = True
    for label, cases in (("dense weak pairs on few sites (the regime where the site-wise bounds cannot help)",
                          [(6, 2, 1.0, 0.3, 6), (6, 3, 1.0, 0.3, 8), (7, 3, 0.5, 0.2, 12), (8, 2, 2.0, 0.3, 14),
                           (8, 3, 1.0, 0.15, 16), (9, 2, 0.3, 0.4, 20), (10, 2, 1.0, 0.2, 24), (7, 3, 3.0, 0.3, 10)]),
                         ("sparse weak pairs on more sites, weakly correlated reference",
                          [(12, 2, 0.2, 0.3, 8), (12, 2, 0.2, 0.3, 12), (13, 2, 0.1, 0.4, 10), (14, 2, 0.3, 0.2, 14),
                           (9, 3, 0.2, 0.3, 8), (14, 2, 0.05, 0.3, 14)])):
        print(label + " (exhaustive enumeration; all numbers are the excess over the first-order value -beta<V>_0):")
        gaps = []
        for (n, d, ss, ws, nw) in cases:
            for r in range(3):
                res = run(rng, n, d, ss, ws, nw, verbose=(r == 0))
                allok &= res[0]
                gaps.append(res[1:])
        g = np.array(gaps)
        print(f"   {len(gaps)} models: exact <= variance form; exact <= exact-range bound <= column form <= Gamma form; exact <= total-range bound: {allok}")
        print(f"   medians of (bound gap)/(total-range gap):  exact ranges {np.median(g[:,1]/g[:,4]):.3f},  column form {np.median(g[:,2]/g[:,4]):.3f},  "
              f"Gamma form {np.median(g[:,3]/g[:,4]):.3f},  variance form {np.median(g[:,5]/g[:,4]):.3f};   median of (exact gap)/(bound gap): exact ranges {np.median(g[:,0]/g[:,1]):.3f}, variance form {np.median(g[:,0]/g[:,5]):.3f}")
    print("ALL OK" if allok else "FAILED")
    sys.exit(0 if allok else 1)
