"""
capcorner.py -- workstream R6: the degenerate branch r-dagger < Delta = ceil(lam/u) of the cap remark of 40c5bd7.
Small outer cubes, lam = 1 > u, eta = 1/2 (so that M-ddagger = K 2^{n_o}/(1-eta) = K 2^{n_o+1} lies in the doubling sequence),
valid and invalid inner behaviours.  Per run: is the cap respected; did a pass with M = M-ddagger exactly occur while unpopulated,
and did it close (section 2.8 of the report: it must, when r-dagger >= 1 and the previous level was populated).
usage: python3 capcorner.py <nruns> <seed>
"""
import sys, json, os, time
import numpy as np, mpmath as mp
from fractions import Fraction
import r6lib as R, instances as I, checks as C, campaign as CP

HERE = os.path.dirname(os.path.abspath(__file__))
nruns, seed = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
S = dict(runs=0, degenerate=0, rdag_ge1_degenerate=0, pass_at_Mdd=0, pass_at_Mdd_unpop=0, pass_at_Mdd_unpop_notclosed=0, cap_viol=0, det_viol=0,
         good_viol=0, max_M_over_cap=0.0, sample_eq_2Mdd=0, closed=0, abort=0, rdag_hist={},
         rge1_unpop_at_Mdd=0, rge1_notclosed_after_pop=0, rge1_notclosed_after_neg=0, rge1_max_M_over_cap=0.0, rle0_max_M_over_cap=0.0)
bad = []
t0 = time.time()
for it in range(nruns):
    u = float(rng.choice([0.15, 0.2, 0.3, 0.45]))
    n_o = int(rng.integers(3, 13))
    n = n_o + int(rng.integers(2, 10))
    theta = float(rng.choice([0.003, 0.01, 0.03, 0.1, 0.3, 1.0]))
    nu1 = float(rng.choice([1.0, 30.0, 2 * np.e ** u * n_o / theta, 1e4]))
    b = float(rng.choice([0.25, 0.5, 1.0]))
    b = min(b, 0.6 * 2 * u * (n - n_o))            # the ladder needs x_L <= b < x_0 = 2 u n_i
    cell = CP.cell_general(n, n_o, u, b, 1.0, Fraction(1, 2), float(rng.choice([0.5, 1.0])), theta, nu1=nu1, L_ext=int(rng.integers(0, 4)))
    cell["Kov"] = int(rng.choice([0, 0, 4, 16])) or None
    P = CP.make_params(cell)
    prof = str(rng.choice(["cone", "cone_half", "dip", "flatcone", "platcone", "rw_uniform", "rw_down", "flat", "two_plateaus", "eqmass"]))
    F = CP.make_profile(prof, cell, P, rng)
    sname = str(rng.choice(list(CP.STRAT_SETS) + ["inv_above", "inv_below", "inv_mix"]))
    strats = dict(CP.STRAT_SETS, **CP.INVALID_SETS)[sname]
    w = [mp.mpf(1) / len(strats)] * len(strats)
    inst = I.radial(n, n_o, u, F, d0=int(rng.choice([0, n_o // 2, n_o])), s_in=float(rng.choice([0.0, u, -u])), strats=strats, weights=w)
    run = R.Run(P, inst, R.SimOracle(P.xs, rng), rng).run()
    ck = C.check_2LP(run)
    S["runs"] += 1
    S["closed"] += run.status == "closed"
    S["abort"] += run.status == "abort"
    deg = P.rdag < P.Delta
    S["degenerate"] += deg
    S["rdag_ge1_degenerate"] += (deg and P.rdag >= 1)
    S["rdag_hist"][str(P.rdag)] = S["rdag_hist"].get(str(P.rdag), 0) + 1
    Mdd = P.Mddag
    maxM = 0
    prev_status = None
    for rec in run.levels:
        for ps in rec["passes"]:
            maxM = max(maxM, ps["M"])
            if deg and ps["M"] == Mdd:
                S["pass_at_Mdd"] += 1
                if not ps["populated"]:
                    S["pass_at_Mdd_unpop"] += 1
                    if P.rdag >= 1:
                        S["rge1_unpop_at_Mdd"] += 1
                    if not ps["closed"]:
                        S["pass_at_Mdd_unpop_notclosed"] += 1
                        if P.rdag >= 1:
                            S["rge1_notclosed_after_pop" if prev_status == "populated" else "rge1_notclosed_after_neg"] += 1
        prev_status = rec["status"]
    if maxM > P.K:
        S["max_M_over_cap"] = max(S["max_M_over_cap"], float(maxM / P.cap_new))
        key = "rge1_max_M_over_cap" if (deg and P.rdag >= 1) else ("rle0_max_M_over_cap" if deg else None)
        if key:
            S[key] = max(S[key], float(maxM / P.cap_new))
        if maxM >= P.cap_new:
            S["cap_viol"] += 1
            bad.append(dict(cell=CP.cell_tag(cell), prof=prof, strat=sname, rdag=P.rdag, Delta=P.Delta, ratio=float(maxM / P.cap_new)))
        if deg and maxM == 2 * Mdd:
            S["sample_eq_2Mdd"] += 1
    S["det_viol"] += bool(ck["det"])
    S["good_viol"] += bool(ck["G"] and ck["good"])
    if ck["det"]:
        bad.append(dict(cell=CP.cell_tag(cell), prof=prof, strat=sname, det=[str(x) for x in ck["det"][:3]]))
print("capcorner seed", seed, "time %.0fs" % (time.time() - t0))
print(json.dumps(S, indent=1))
for x in bad[:8]:
    print("BAD", x)
with open(os.path.join(HERE, "data", "capcorner_%d.json" % seed), "w") as f:
    json.dump(dict(summary=S, bad=bad[:50]), f)
