"""Development evidence on public real data: umbrella sampling of a valine chi torsion (26 umbrellas,
501 snapshots each; experiments/mbar/data/pymbar_umbrella/README.md).  No ground truth exists.

What is computed:
 1. MBAR free energies of the 26 umbrella states, by this division's solver and by PyMBAR (agreement).
 2. For three treatments of time correlation -- all snapshots; subsampled by PyMBAR's estimated
    statistical inefficiency (the example's recipe); every 10th snapshot -- the asymptotic standard
    errors, the likelihood-ratio confidence region (8 time-ordered batches) and its intervals for
    adjacent and distant umbrella pairs, and the classifier model check (does a histogram predictor of
    the umbrella label, trained on the past, beat MBAR's own predictor?).
 3. A design diagnostic for a scientifically relevant target: the free-energy difference between two
    rotamer wells of chi in the UNBIASED ensemble (two unsampled 'bin states').  Plug-in variance at
    the actual (equal) allocation, the certified-form efficiency bound evaluated at the plug-in
    distributions (an estimate, not a certificate), and the plug-in optimal allocation.

Run:  python experiments/mbar/bench/bench_public_umbrella.py
"""
import json
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar import population as pop  # noqa: E402
from d9mbar.certificates import (classifier_evalue, lr_confidence_region,  # noqa: E402
                                 restricted_interval)
from d9mbar.estimators import fitted_distributions, mbar, plugin_variance  # noqa: E402
from scipy.special import logsumexp  # noqa: E402

DATA = os.path.join(HERE, "..", "data", "pymbar_umbrella")
kB = 1.381e-23 * 6.022e23 / 1000.0
beta = 1.0 / (kB * 300.0)
K = 26


def load():
    cen = np.loadtxt(os.path.join(DATA, "centers.dat"))[:K]
    chi0, kspring = cen[:, 0], cen[:, 1] * (np.pi / 180) ** 2
    chis = []
    for k in range(K):
        v = np.array([float(l.split()[1]) for l in open(os.path.join(DATA, f"prod{k}_dihed.xvg"))
                      if l[0] not in "#@"])
        chis.append((v + 180.0) % 360.0 - 180.0)
    return chi0, kspring, chis


def energies(chi, chi0, kspring):
    d = chi[:, None] - chi0[None, :]
    d = (d + 180.0) % 360.0 - 180.0
    return beta * 0.5 * kspring[None, :] * d ** 2


def hist_classifier(x, y, U, bins=30, tau=20.0):
    def prob(b, prev, cur):
        fprev, _ = mbar(U[prev], y[prev])
        nprev = np.bincount(y[prev], minlength=K)
        Z = np.log(nprev / nprev.sum())[None, :] + fprev[None, :] - U[cur]
        pm = np.exp(Z - logsumexp(Z, axis=1)[:, None])
        edges = np.linspace(-180, 180, bins + 1)[1:-1]
        bp, bc = np.searchsorted(edges, x[prev]), np.searchsorted(edges, x[cur])
        cnt = np.zeros((bins, K))
        np.add.at(cnt, (bp, y[prev]), 1.0)
        return (cnt[bc] + tau * pm) / (cnt[bc].sum(axis=1, keepdims=True) + tau)
    return prob


def main():
    import pymbar
    from pymbar import timeseries
    chi0, kspring, chis = load()
    report = dict(dataset="pymbar umbrella-sampling-fes (Mobley et al. 2007)", K=K, treatments=[])
    g = []
    for k in range(K):
        r = np.deg2rad(chis[k])
        g.append(max(timeseries.statistical_inefficiency(np.cos(r)), timeseries.statistical_inefficiency(np.sin(r))))
    g = np.array(g)
    report["statistical_inefficiency"] = dict(min=float(g.min()), median=float(np.median(g)), max=float(g.max()))
    print("estimated statistical inefficiencies: min %.1f median %.1f max %.1f" % (g.min(), np.median(g), g.max()))
    pairs = [(0, 1), (12, 13), (0, 6), (0, 13)]
    for name in ("all_snapshots", "subsampled_by_g", "every_10th"):
        idx = []
        for k in range(K):
            n = len(chis[k])
            if name == "all_snapshots":
                idx.append(np.arange(n))
            elif name == "subsampled_by_g":
                idx.append(np.array(timeseries.subsample_correlated_data(np.deg2rad(chis[k]), g=g[k])))
            else:
                idx.append(np.arange(0, n, 10))
        x = np.concatenate([chis[k][idx[k]] for k in range(K)])
        y = np.concatenate([np.full(len(idx[k]), k) for k in range(K)])
        U = energies(x, chi0, kspring)
        counts = np.bincount(y, minlength=K)
        f, info = mbar(U, y)
        m = pymbar.MBAR(U.T, counts)
        res = m.compute_free_energy_differences()
        agree = float(np.max(np.abs(f - res["Delta_f"][0])))
        reg = lr_confidence_region(U, y, alpha=0.05, n_batches=8)
        rows = []
        for (i, j) in pairs:
            c = np.zeros(K)
            c[i], c[j] = -1.0, 1.0
            se = float(np.sqrt(plugin_variance(U, y, c, f=f)))
            lo, hi = reg.interval(c)
            rows.append(dict(pair=[i, j], estimate=float(f[j] - f[i]), asymptotic_se=se,
                             pymbar_se=float(res["dDelta_f"][i, j]), lr_interval=[float(lo), float(hi)],
                             lr_width_over_asymptotic_width=float((hi - lo) / (2 * 1.96 * se))))
        # contrast-specific intervals from the sub-ladder of umbrellas whose centres lie on the shorter
        # arc between the two centres (chosen from the design, not from the samples): Proposition B2'
        for r in rows:
            i, j = r["pair"]
            d = lambda a, b: abs((a - b + 180.0) % 360.0 - 180.0)          # noqa: E731
            arc = d(chi0[i], chi0[j])
            S = [k for k in range(K) if d(chi0[k], chi0[i]) + d(chi0[k], chi0[j]) <= arc + 1e-9]
            c = np.zeros(K)
            c[i], c[j] = -1.0, 1.0
            lo, hi, sub = restricted_interval(U, y, c, S, alpha=0.05, n_batches=8)
            r["sub_ladder_states"] = len(S)
            r["sub_ladder_interval"] = [float(lo), float(hi)]
            r["sub_ladder_width_over_asymptotic_width"] = float((hi - lo) / (2 * 1.96 * r["asymptotic_se"]))
        logE, einfo = classifier_evalue(U, y, hist_classifier(x, y, U), n_batches=8)
        t = dict(treatment=name, samples=int(len(y)), counts_min=int(counts.min()), counts_max=int(counts.max()),
                 max_abs_difference_to_pymbar=agree, region_status=reg.status, regret=reg.meta.get("regret"),
                 pairs=rows, model_check_logE=float(logE), model_check_rejects=bool(logE >= np.log(20)))
        report["treatments"].append(t)
        print(f"{name}: N={len(y)} status={reg.status} regret={reg.meta.get('regret')} | vs pymbar {agree:.1e} | "
              f"model check logE={logE:.1f} reject={logE >= np.log(20)}")
        for r in rows:
            print("   pair", r["pair"], "est %.3f  se %.3f  LR [%.3f, %.3f]  width ratio %.2f | sub-ladder of %d states: "
                  "[%.3f, %.3f] ratio %.2f"
                  % (r["estimate"], r["asymptotic_se"], r["lr_interval"][0], r["lr_interval"][1],
                     r["lr_width_over_asymptotic_width"], r["sub_ladder_states"], r["sub_ladder_interval"][0],
                     r["sub_ladder_interval"][1], r["sub_ladder_width_over_asymptotic_width"]))
        if name == "subsampled_by_g":
            keep = (x, y, U, f, counts)
    # ---- design diagnostic for the rotamer free-energy difference in the unbiased ensemble
    x, y, U, f, counts = keep
    inA = (x > -90) & (x < -30)                  # gauche-
    inB = (np.abs(x) > 150)                      # trans
    big = np.inf
    Uext = np.hstack([U, np.where(inA, 0.0, big)[:, None], np.where(inB, 0.0, big)[:, None]])
    fe, _ = mbar(Uext, y, check_support=False)
    P = fitted_distributions(Uext, y, fe)
    c = np.zeros(K + 2)
    c[K], c[K + 1] = -1.0, 1.0
    nu = pop.contrast_measure(P, c)
    n_act = np.concatenate([counts.astype(float), [0.0, 0.0]])
    V_act = pop.variance(P, n_act, nu)
    cost = np.concatenate([np.ones(K), [1e9, 1e9]])
    B = float(counts.sum())
    sopt, Vopt, oinfo = pop.optimal_allocation(P, nu, cost=cost, budget=B, tol=1e-7, iters=6000, kind="measure")
    eff_lb = pop.efficiency_lower_bound(P, n_act, nu, cost=cost, budget=B)
    top = np.argsort(-sopt[:K])[:6]
    report["design_diagnostic"] = dict(
        target="F(trans, |chi|>150) - F(gauche-, -90<chi<-30) in the unbiased ensemble",
        estimate=float(fe[K + 1] - fe[K]), plugin_se_actual_allocation=float(np.sqrt(V_act)),
        plugin_se_optimal_allocation=float(np.sqrt(Vopt)), plugin_variance_ratio_optimal_over_actual=float(Vopt / V_act),
        plugin_efficiency_lower_bound_of_actual=float(eff_lb),
        umbrellas_with_most_optimal_weight=[dict(umbrella=int(k), centre=float(chi0[k]), fraction=float(sopt[k] / B)) for k in top])
    d = report["design_diagnostic"]
    print("design diagnostic (plug-in estimates): rotamer dF = %.3f, se at the actual allocation %.3f, at the plug-in "
          "optimum %.3f (variance ratio %.3f; efficiency bound of the actual allocation >= %.3f)"
          % (d["estimate"], d["plugin_se_actual_allocation"], d["plugin_se_optimal_allocation"],
             d["plugin_variance_ratio_optimal_over_actual"], d["plugin_efficiency_lower_bound_of_actual"]))
    print("   umbrellas carrying the plug-in optimum:", [(u["centre"], round(u["fraction"], 3)) for u in d["umbrellas_with_most_optimal_weight"]])
    with open(os.path.join(HERE, "..", "results", "public_umbrella.json"), "w") as fh:
        json.dump(report, fh, indent=1)
    print("written results/public_umbrella.json")


if __name__ == "__main__":
    main()
