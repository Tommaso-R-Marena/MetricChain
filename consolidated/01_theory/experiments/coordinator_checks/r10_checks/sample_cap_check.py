# Exploration: sample sizes of Algorithm 2L+ against the proposed cap 2 max(e^lam M_dag, M_ddag).
import sys, math, importlib.util, itertools
import numpy as np
spec = importlib.util.spec_from_file_location("fc", __import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)), "..", "..", "falsify_conjectures.py"))
fc = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(fc)
rng = np.random.default_rng(7)

def plateau_cone(n_o, u, d0, slope_frac=1.0):
    binom = [math.comb(n_o, j) for j in range(n_o + 1)]
    f = u * slope_frac * np.maximum(np.arange(n_o + 1, dtype=float) - d0, 0.0)
    return np.exp(-f), np.array(binom, dtype=float) / 2 ** n_o, float(-f[0])

def cap(C, par, n_o, u):
    lam, eta = par["lam"], par["eta"]
    Delta = math.ceil(lam / u - 1e-12)
    ball = C["ball"]
    if C["rdag"] >= Delta:
        Mdd = C["K"] / ((1 - eta) * (ball[C["rdag"] - Delta + 1] / 2 ** n_o))
    else:
        Mdd = C["K"] * 2 ** n_o / (1 - eta) * (1 + 1e-9)
    return 2 * max(math.exp(lam) * C["Mdag"], Mdd), Mdd

worst = 0.0; nruns = 0; above = 0
pars = [dict(lam=0.5, eta=0.25, etap=0.5, theta=0.5, b=1.0, delta=0.01, nu1=1.0),
        dict(lam=0.5, eta=0.25, etap=0.5, theta=2.0, b=0.5, delta=0.01, nu1=1.0),
        dict(lam=1.0, eta=0.5, etap=1.0, theta=2.0, b=3.0, delta=0.01, nu1=1.0),
        dict(lam=0.25, eta=0.25, etap=0.1, theta=1.0, b=0.5, delta=0.01, nu1=1.0),
        dict(lam=1.0, eta=0.5, etap=1.0, theta=0.3, b=1.0, delta=0.01, nu1=1.0)]
for n_o in (20, 24, 28):
    for u in (0.5, 1.0, 2.0):
        for par in pars:
            for d0 in range(0, 9):
                for sf in (1.0, 0.6):
                    vals, probs, lnw = plateau_cone(n_o, u, d0, sf)
                    for mode in (0, 1, 2):
                        run = fc.ba_two_level_plus(rng, vals, probs, lnw, n_o, n_o + 2, u, par, mode, max_points=2_000_000)
                        if "error" in run:
                            continue
                        C = run["C"]
                        c, Mdd = cap(C, par, n_o, u)
                        for lv in run["levels"] + [run["last"]]:
                            if lv["M"] > C["K"]:
                                ratio = lv["M"] / c
                                if ratio > worst:
                                    worst = ratio
                                    info = (n_o, u, par["lam"], par["theta"], d0, sf, mode, lv["M"], C["Mdag"], Mdd, C["Mbar"], C["rdag"], lv["pop"])
                                if lv["M"] > C["Mdag"]:
                                    above += 1
                        nruns += 1
print("runs", nruns, "samples above M_dag", above, "worst M / cap", worst)
print("at", info)
