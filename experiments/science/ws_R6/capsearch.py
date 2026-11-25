"""
capsearch.py -- workstream R6: how close does the largest sample come to the cap 2 max{e^lam M-dagger, M-ddagger} of the remark of 40c5bd7?
Structured sweep on the cell of the theory division's own example (n_o = 24, u = lam = 1/2) and neighbours: landscapes "plateau, then cone"
(all plateau radii), cones, "cone, then flat", with every reference position and every inner behaviour; literal runs.
usage: python3 capsearch.py <seed> [seconds]
"""
import sys, json, os, time
import numpy as np, mpmath as mp
from fractions import Fraction
import r6lib as R, instances as I, checks as C, campaign as CP

HERE = os.path.dirname(os.path.abspath(__file__))
seed = int(sys.argv[1]); tlim = float(sys.argv[2]) if len(sys.argv) > 2 else 240
rng = np.random.default_rng(seed)
cells = [CP.cell_general(48, 24, 0.5, 0.5, 0.5, Fraction(1, 2), 1.0, th, nu1=nu1) for th in (0.3, 1.0, 3.0) for nu1 in (1.0, None)] + \
        [CP.cell_general(48, 24, 0.5, 0.5, 0.5, Fraction(1, 4), 0.5, 0.5), CP.cell_general(60, 30, 0.5, 1.0, 0.5, Fraction(1, 2), 1.0, 1.0, nu1=1.0),
         CP.cell_general(40, 20, 1.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0, nu1=1.0), CP.cell_general(40, 16, 1.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.3)]
best = dict(ratio=0.0)
runs = viol = 0
t0 = time.time()
hist = {}
while time.time() - t0 < tlim:
    ci = int(rng.integers(0, len(cells)))
    cell = cells[ci]
    P = CP.make_params(cell)
    n, n_o, u = cell["n"], cell["n_o"], cell["u"]
    kind = str(rng.choice(["platcone", "platcone", "platcone", "cone", "coneflat", "platconeflat"]))
    d = np.arange(n_o + 1, dtype=float)
    R1 = int(rng.integers(0, n_o)); R2 = int(rng.integers(R1, n_o + 1))
    if kind == "platcone":
        F = -u * np.maximum(d - R1, 0.0)
    elif kind == "cone":
        F = -u * d
    elif kind == "coneflat":
        F = -u * np.minimum(d, R1)
    else:
        F = -u * np.clip(d - R1, 0.0, R2 - R1)
    strat = int(rng.choice([R.S_BOTTOM, R.S_TOP, R.S_CENTER, R.S_ADV_HI, R.S_ADV_LO]))
    inst = I.radial(n, n_o, u, F, d0=int(rng.choice([0, n_o // 2, n_o, int(rng.integers(0, n_o + 1))])), s_in=float(rng.choice([0.0, u, -u])), strats=(strat,))
    try:
        run = R.Run(P, inst, R.SimOracle(P.xs, rng), rng).run()
    except AssertionError:
        continue
    ck = C.check_2LP(run)
    runs += 1
    if ck["det"] or (ck["G"] and ck["good"]):
        viol += 1
    r = ck["ratios"]["M_over_capnew"]
    hist[ci] = max(hist.get(ci, 0.0), r)
    if r > best["ratio"]:
        best = dict(ratio=r, cell=CP.cell_tag(cell), kind=kind, R1=R1, R2=R2, strat=strat, M_over_Mdag=ck["ratios"]["M_over_Mdag"], rdag=P.rdag,
                    cap_over_Mdag=float(P.cap_new / P.Mdag), Mbar_over_Mdag=float(P.Mbar / P.Mdag))
out = dict(seed=seed, runs=runs, violations=viol, best=best, best_per_cell={str(k): v for k, v in hist.items()}, secs=round(time.time() - t0, 1))
json.dump(out, open(os.path.join(HERE, "data", "capsearch_%d.json" % seed), "w"), indent=1)
print(json.dumps(out, indent=1))
