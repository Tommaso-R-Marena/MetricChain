"""Pilot-based sample allocation against uniform allocation at matched total cost: actual errors of
the final MBAR estimate over independent replicates (not population variances).

Systems have exact independent samplers and exactly known free energies (development evidence).
Every method ends with the same estimator (MBAR on all its samples) and spends the same budget
B = sum_k cost_k n_k; methods differ only in how the samples are divided among the states:

  UNIFORM     equal counts in all states (the standard practice; identical to PyMBAR on such data)
  EQUALCOST   equal cost in all states (n_k ~ 1/cost_k); differs from UNIFORM only if costs differ
  PILOT2      this division: pilot with equal counts (20% of B), plug-in convex allocation from the
              pilot fit only, 25% safeguard mixture with uniform (estimators.pilot_allocation)
  PILOT2C     the same as PILOT2 with a cost-aware pilot: equal cost (not equal counts) per state
              (added after the first runs showed that an equal-count pilot wastes a third of the
              budget on a costly state the optimal design never samples; see VALIDATION.md)
  PILOT4      the same in four stages (20% / 40% / 70% / 100% of B), re-fitted at every stage
  NEYMAN1     established one-step rule: extra samples ~ s_k sqrt(Var_k(z)/cost_k) at the pilot
              allocation (Neyman allocation with frozen influence functions, as for EMUS)
  RESIST      pilot + allocation minimising the plug-in effective resistance c.L^+.c (handoff's earlier idea)
  ORACLE      allocation optimal for the true distributions (uses ground truth; a reference only)

Run:  python experiments/mbar/bench/bench_allocation.py [--reps 400]
"""
import argparse
import json
import os
import sys
import time
import warnings
from multiprocessing import Pool

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
from d9mbar import population as pop  # noqa: E402
from d9mbar.estimators import (fitted_distributions, integer_counts, mbar,  # noqa: E402
                               pilot_allocation)


# ----------------------------------------------------------------------------- systems
def harmonic_system(name, x0, ks, cost, contrast):
    x0, ks, cost = np.asarray(x0, float), np.asarray(ks, float), np.asarray(cost, float)
    f = -0.5 * np.log(2 * np.pi / ks)
    grid = np.linspace((x0 - 7 / np.sqrt(ks)).min(), (x0 + 7 / np.sqrt(ks)).max(), 6001)
    P = np.exp(-0.5 * ks[:, None] * (grid[None, :] - x0[:, None]) ** 2)
    P /= P.sum(axis=1, keepdims=True)

    def sample(rng, k, n):
        return rng.normal(x0[k], 1 / np.sqrt(ks[k]), n)

    def energies(x):
        return 0.5 * ks[None, :] * (x[:, None] - x0[None, :]) ** 2

    return dict(name=name, K=len(x0), f=f - f[0], cost=cost, c=np.asarray(contrast, float), P=P,
                sample=sample, energies=energies)


def discrete_system(name, P, cost, contrast, fs=None):
    P = np.asarray(P, float)
    K = P.shape[0]
    fs = np.zeros(K) if fs is None else np.asarray(fs, float)
    Ut = -np.log(np.maximum(P, 1e-300) * np.exp(-fs[:, None])).T

    def sample(rng, k, n):
        return rng.choice(P.shape[1], size=n, p=P[k])

    def energies(x):
        return Ut[x]

    return dict(name=name, K=K, f=fs - fs[0], cost=np.asarray(cost, float), c=np.asarray(contrast, float),
                P=P, sample=sample, energies=energies)


def systems():
    e = lambda K: np.r_[-1.0, np.zeros(K - 2), 1.0]          # noqa: E731  end-to-end contrast
    out = [
        harmonic_system("bottleneck", [0, 1, 2, 4.6, 5.6, 6.6], np.ones(6), np.ones(6), e(6)),
        harmonic_system("widths", 0.5 * np.arange(5), 2.0 ** np.arange(5), np.ones(5), e(5)),
        harmonic_system("costly_ends", 1.2 * np.arange(5), np.ones(5), [20, 1, 1, 1, 20], e(5)),
        harmonic_system("costly_middle", 1.2 * np.arange(5), np.ones(5), [1, 1, 20, 1, 1], e(5)),
        harmonic_system("homogeneous", 1.0 * np.arange(5), np.ones(5), np.ones(5), e(5)),
    ]
    rng = np.random.default_rng(777)
    for j in range(3):
        P = rng.dirichlet(np.full(12, [0.15, 0.4, 1.0][j]), size=4)
        out.append(discrete_system(f"dirichlet{j}", P, np.ones(4), e(4)))
    return out


# ----------------------------------------------------------------------------- helpers
def draw(rng, sysm, counts):
    xs, ys = [], []
    for k, n in enumerate(counts):
        if n > 0:
            xs.append(sysm["sample"](rng, k, int(n)))
            ys.append(np.full(int(n), k))
    x = np.concatenate(xs)
    return sysm["energies"](x), np.concatenate(ys)


def fellman(valgrad, a, B, lo, iters=3000, tol=1e-7):
    """Multiplicative rule for a convex, degree -1 homogeneous objective with gradient -g."""
    K = len(a)
    s = np.maximum(np.full(K, B / a.sum()), lo)
    s *= B / (a @ s)
    best = (np.inf, s)
    for _ in range(iters):
        V, g = valgrad(s)
        if V < best[0]:
            best = (V, s.copy())
        t = s * np.sqrt(np.maximum(g, 0) / a)
        free = np.ones(K, bool)
        new = t
        for _ in range(K + 1):
            rem = B - a[~free] @ lo[~free]
            new = np.where(free, t * rem / max(a[free] @ t[free], 1e-300), lo)
            viol = free & (new < lo - 1e-15)
            if not viol.any():
                break
            free &= ~viol
        if np.max(np.abs(new - s)) < tol * s.max():
            s = new
            break
        s = new
    return best[1] if best[0] < valgrad(s)[0] else s


def resistance_valgrad(P, c):
    def vg(s):
        nu = pop.contrast_measure(P, c)
        V = pop.variance(P, s, nu)
        g = pop.state_variances(P, s, nu)
        return V + np.sum(c * c / s), g + c * c / s**2
    return vg


def finish(rng, sysm, U, y, extra):
    if extra.sum() > 0:
        U2, y2 = draw(rng, sysm, extra)
        U, y = np.vstack([U, U2]), np.concatenate([y, y2])
    f, _ = mbar(U, y)
    return float(sysm["c"] @ f - sysm["c"] @ sysm["f"]), np.bincount(y, minlength=sysm["K"])


def one_rep(args):
    si, seed, B, pilot_frac = args
    sysm = systems()[si]
    rng = np.random.default_rng(seed)
    K, a, c = sysm["K"], sysm["cost"], sysm["c"]
    out = {}
    try:
        # UNIFORM and EQUALCOST: no pilot needed
        n_u = integer_counts(np.full(K, B / a.sum()), B, a)
        U, y = draw(rng, sysm, n_u)
        out["UNIFORM"] = (float(c @ mbar(U, y)[0] - c @ sysm["f"]), n_u.tolist(), 0.0)
        n_e = integer_counts(B / (K * a), B, a)
        U, y = draw(rng, sysm, n_e)
        out["EQUALCOST"] = (float(c @ mbar(U, y)[0] - c @ sysm["f"]), n_e.tolist(), 0.0)
        # ORACLE
        U, y = draw(rng, sysm, sysm["oracle_counts"])
        out["ORACLE"] = (float(c @ mbar(U, y)[0] - c @ sysm["f"]), list(map(int, sysm["oracle_counts"])), 0.0)
        # common pilot for the pilot-based methods
        n0 = integer_counts(np.full(K, pilot_frac * B / a.sum()), pilot_frac * B, a)
        n0 = np.maximum(n0, 2)
        Up, yp = draw(rng, sysm, n0)
        # PILOT2
        t0 = time.time()
        extra, info = pilot_allocation(Up, yp, c, B, cost=a, safeguard=0.25)
        dt = time.time() - t0
        err, cnt = finish(rng, sysm, Up, yp, extra)
        out["PILOT2"] = (err, cnt.tolist(), dt, info["fallback"] is not None)
        # PILOT4: stages at 40%, 70%, 100% of the budget
        t0 = time.time()
        Us, ys, dts, fb = Up, yp, 0.0, False
        for frac in (0.4, 0.7, 1.0):
            t1 = time.time()
            extra, info = pilot_allocation(Us, ys, c, frac * B, cost=a, safeguard=0.25)
            dts += time.time() - t1
            fb |= info["fallback"] is not None
            if extra.sum() > 0:
                U2, y2 = draw(rng, sysm, extra)
                Us, ys = np.vstack([Us, U2]), np.concatenate([ys, y2])
        out["PILOT4"] = (float(c @ mbar(Us, ys)[0] - c @ sysm["f"]), np.bincount(ys, minlength=K).tolist(), dts, fb)
        # PILOT2C: the same procedure with a cost-aware pilot (equal cost, not equal counts, per state)
        n0c = np.maximum(integer_counts(pilot_frac * B / (K * a), pilot_frac * B, a), 2)
        Upc, ypc = draw(rng, sysm, n0c)
        t0 = time.time()
        extra, info = pilot_allocation(Upc, ypc, c, B, cost=a, safeguard=0.25)
        dt = time.time() - t0
        err, cnt = finish(rng, sysm, Upc, ypc, extra)
        out["PILOT2C"] = (err, cnt.tolist(), dt, info["fallback"] is not None)
        # NEYMAN1 and RESIST from the same pilot
        rem = B - a @ n0
        try:
            fp, _ = mbar(Up, yp)
            Ph = fitted_distributions(Up, yp, fp)
            g = pop.state_variances(Ph, n0.astype(float), pop.contrast_measure(Ph, c))
            ney = n0 * np.sqrt(np.maximum(g, 0) / a)
            ney = ney * rem / max(a @ ney, 1e-300)
            sres = fellman(resistance_valgrad(Ph, c), a, B, n0.astype(float))
            res_extra = np.maximum(sres - n0, 0)
            res_extra *= rem / max(a @ res_extra, 1e-300)
        except (ValueError, RuntimeError, np.linalg.LinAlgError):
            ney = res_extra = np.full(K, rem / a.sum())
        uni = np.full(K, rem / a.sum())
        for name, ex in (("NEYMAN1", ney), ("RESIST", res_extra)):
            ex = integer_counts(0.75 * ex + 0.25 * uni, rem, a)
            err, cnt = finish(rng, sysm, Up, yp, ex)
            out[name] = (err, cnt.tolist(), 0.0)
    except (ValueError, RuntimeError) as err:
        out["FAILED"] = repr(err)
    return out


_ORACLE = {}


def prepare(si, B):
    sysm = systems()[si]
    nu = pop.contrast_measure(sysm["P"], sysm["c"])
    s, V, info = pop.optimal_allocation(sysm["P"], nu, cost=sysm["cost"], budget=B, iters=20000, tol=1e-8)
    a, K = sysm["cost"], sysm["K"]
    su = np.full(K, B / a.sum())
    se = B / (K * a)
    return dict(oracle=s, V_oracle=V, V_uniform=pop.variance(sysm["P"], su, nu),
                V_equalcost=pop.variance(sysm["P"], se, nu), eff_gap=info["kkt_gap"],
                eff_bound_uniform=pop.efficiency_lower_bound(sysm["P"], su, nu, cost=a))


def _init(oracles):
    global _ORACLE
    _ORACLE = oracles
    _orig = systems

    def patched():
        out = _orig()
        for i, sm in enumerate(out):
            if i in _ORACLE:
                sm["oracle_counts"] = _ORACLE[i]
        return out
    globals()["systems"] = patched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=400)
    ap.add_argument("--samples", type=float, default=3000.0, help="budget in units of the mean cost")
    ap.add_argument("--pilot", type=float, default=0.2)
    ap.add_argument("--procs", type=int, default=3)
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results", "allocation_benchmark.json"))
    a = ap.parse_args()
    syss = systems()
    report = dict(reps=a.reps, pilot_fraction=a.pilot, seed_base=5150, systems=[])
    for si, sysm in enumerate(syss):
        if a.only and sysm["name"] not in a.only.split(","):
            continue
        B = a.samples * sysm["cost"].mean()
        prep = prepare(si, B)
        oc = integer_counts(prep["oracle"], B, sysm["cost"])
        with Pool(a.procs, initializer=_init, initargs=({si: oc},)) as pool:
            rows = pool.map(one_rep, [(si, 5150 + 100000 * si + r, B, a.pilot) for r in range(a.reps)], chunksize=4)
        failed = [r for r in rows if "FAILED" in r]
        rows = [r for r in rows if "FAILED" not in r]
        methods = {}
        for m in ("UNIFORM", "EQUALCOST", "PILOT2", "PILOT2C", "PILOT4", "NEYMAN1", "RESIST", "ORACLE"):
            errs = np.array([r[m][0] for r in rows])
            mse = float(np.mean(errs**2))
            methods[m] = dict(rmse=float(np.sqrt(mse)), mse=mse, bias=float(errs.mean()),
                              mse_se=float(np.std(errs**2) / np.sqrt(len(errs))),
                              mean_counts=np.mean([r[m][1] for r in rows], axis=0).round(1).tolist(),
                              median_alloc_time=float(np.median([r[m][2] for r in rows])),
                              fallbacks=int(sum(bool(r[m][3]) for r in rows)) if len(rows[0][m]) > 3 else 0)
        mu = methods["UNIFORM"]["mse"]
        rngb = np.random.default_rng(1)
        eu = np.array([r["UNIFORM"][0] for r in rows]) ** 2
        for m, d in methods.items():
            em = np.array([r[m][0] for r in rows]) ** 2
            boots = [em[i].mean() / eu[j].mean() for i, j in
                     ((rngb.integers(len(em), size=len(em)), rngb.integers(len(eu), size=len(eu))) for _ in range(2000))]
            d["mse_ratio_vs_uniform"] = d["mse"] / mu
            d["mse_ratio_ci95"] = [float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))]
        summ = dict(name=sysm["name"], K=sysm["K"], cost=sysm["cost"].tolist(), budget=B, failed=len(failed),
                    population=dict(V_oracle=prep["V_oracle"], V_uniform=prep["V_uniform"],
                                    V_equalcost=prep["V_equalcost"], oracle_allocation=prep["oracle"].round(2).tolist(),
                                    predicted_ratio_oracle_vs_uniform=prep["V_oracle"] / prep["V_uniform"],
                                    efficiency_lower_bound_of_uniform=prep["eff_bound_uniform"]),
                    methods=methods)
        report["systems"].append(summ)
        print(sysm["name"], "predicted oracle/uniform", round(prep["V_oracle"] / prep["V_uniform"], 3),
              {m: (round(d["mse_ratio_vs_uniform"], 3), [round(x, 2) for x in d["mse_ratio_ci95"]]) for m, d in methods.items()},
              "failed", len(failed), flush=True)
    with open(a.out, "w") as fh:
        json.dump(report, fh, indent=1)
    print("written", a.out)


if __name__ == "__main__":
    main()
