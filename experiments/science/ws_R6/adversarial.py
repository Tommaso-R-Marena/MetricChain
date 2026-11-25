"""
adversarial.py -- workstream R6: adversarial search (hill climbing with restarts) over radial outer profiles, reference position,
inner offset and inner behaviour, with LITERAL runs of my engine (random outer samples), for one objective at a time:

  count   : max over levels and rungs of  (#points used at level j with W > s_j e^{-x_{l-1}}) / cnt(x_{l-1})        [claim (v)]
  calls   : max over levels and rungs of  (#calls of I_l during level j) / min{Mbar, cnt(x_{l-1})}                    [claim (vi)]
  ineq    : max over levels and x of  M_j^neg p(s_j e^{-x}) / (c_eta^{-1} e^lam nu e^x)                               [the count inequality]
  cap     : max sample / (2 max{e^lam M-dagger, M-ddagger})                                                           [remark of 40c5bd7]
  mbar    : max sample / M-dagger
  cost    : ln(queries)/ln(C_vi)

Every run is also checked for every claim (checks.check_2LP); any violation is printed and stored.
usage: python3 adversarial.py <cell-index> <objective> <evaluations> <seed>
"""
import sys, json, time, os
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
import numpy as np
import mpmath as mp
from fractions import Fraction
import r6lib as R, instances as I, checks as C, campaign as CP

CELLS = [
    CP.cell_general(200, 100, 2.0, 0.5, 1.0, Fraction(1, 2), 1.0, 1.0),                 # 0
    CP.cell_bounded(300, 120, 1.0, 4.0),                                                # 1
    CP.cell_general(160, 80, 2.0, 0.5, 0.5, Fraction(1, 2), 1.0, 0.5, nu1=1.0),         # 2
    CP.cell_general(120, 60, 3.0, 0.5, 0.5, Fraction(1, 2), 0.5, 0.5),                  # 3
    CP.cell_general(48, 24, 0.5, 0.5, 0.5, Fraction(1, 2), 1.0, 1.0),                   # 4  (the cell where the theory harness reports a sample of 3.7 M-dagger: n_o = 24, u = lam = 1/2)
    CP.cell_bounded(80, 40, 1.0, 4.0),                                                  # 5
    CP.cell_general(64, 32, 2.0, 1.0, 1.0, Fraction(1, 2), 1.0, 0.25, nu1=1.0),         # 6
]
STR = [R.S_BOTTOM, R.S_TOP, R.S_CENTER, R.S_ADV_HI, R.S_ADV_LO]


def evaluate(cell, P, genome, seed, objective):
    n, n_o, u = cell["n"], cell["n_o"], cell["u"]
    steps = np.clip(genome["steps"], -u, u)
    F = np.concatenate([[0.0], np.cumsum(steps)])
    rng = np.random.default_rng(seed)
    inst = I.radial(n, n_o, u, F, d0=int(genome["d0"]), s_in=float(np.clip(genome["s_in"], -u, u)), strats=(STR[int(genome["strat"])],))
    try:
        run = R.Run(P, inst, R.SimOracle(P.xs, rng), rng).run()
    except AssertionError:
        return None, None
    ck = C.check_2LP(run)
    rr = ck["ratios"]
    val = dict(count=rr.get("used_over_cnt", 0.0), calls=rr.get("calls_over_bound", 0.0), ineq=rr.get("count_ineq", 0.0),
               cap=rr["M_over_capnew"], mbar=rr["M_over_Mdag"], cost=rr["lnq_over_lnCmax"])[objective]
    return val, ck


def random_genome(cell, rng):
    n_o, u = cell["n_o"], cell["u"]
    kind = rng.integers(0, 6)
    if kind == 0:
        steps = np.zeros(n_o)
    elif kind == 1:
        steps = -u * np.ones(n_o)
    elif kind == 2:                      # cone then flat
        Rr = rng.integers(1, n_o)
        steps = np.where(np.arange(n_o) < Rr, -u, 0.0)
    elif kind == 3:                      # plateau then cone
        Rr = rng.integers(1, n_o)
        steps = np.where(np.arange(n_o) < Rr, 0.0, -u)
    elif kind == 4:
        steps = -rng.uniform(0, u, size=n_o)
    else:
        steps = rng.uniform(-u, u, size=n_o)
    return dict(steps=steps.astype(float), d0=int(rng.choice([0, n_o // 2, n_o])), s_in=float(rng.choice([0.0, u, -u])), strat=int(rng.integers(0, len(STR))))


def mutate(cell, g, rng):
    n_o, u = cell["n_o"], cell["u"]
    h = dict(steps=g["steps"].copy(), d0=g["d0"], s_in=g["s_in"], strat=g["strat"])
    k = rng.integers(0, 7)
    if k <= 2:                           # change a block of slopes
        a = rng.integers(0, n_o); ln_ = rng.integers(1, max(2, n_o // 4))
        h["steps"][a:a + ln_] = rng.choice([-u, 0.0, u, rng.uniform(-u, u)])
    elif k == 3:                         # shift a breakpoint
        s = rng.integers(-3, 4)
        h["steps"] = np.roll(h["steps"], s)
    elif k == 4:
        h["d0"] = int(np.clip(g["d0"] + rng.integers(-5, 6), 0, n_o))
    elif k == 5:
        h["s_in"] = float(rng.choice([0.0, u, -u, u / 2, -u / 2]))
    else:
        h["strat"] = int(rng.integers(0, len(STR)))
    return h


if __name__ == "__main__":
    ci, objective, nev, seed = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    cell = CELLS[ci]
    P = CP.make_params(cell)
    rng = np.random.default_rng(seed)
    best, bestg = -1.0, None
    viol = []
    t0 = time.time()
    hist = []
    ev = 0
    g = random_genome(cell, rng)
    cur = -1.0
    stall = 0
    TLIM = float(os.environ.get("R6_ADV_SECONDS", "330"))        # wall-clock budget; the result is written when it is used up
    while ev < nev and time.time() - t0 < TLIM:
        cand = random_genome(cell, rng) if (bestg is None or stall > 25) else mutate(cell, g, rng)
        if stall > 25:
            stall = 0
            cur = -1.0
        val, ck = evaluate(cell, P, cand, int(rng.integers(0, 2 ** 31)), objective)
        ev += 1
        if val is None:
            continue
        if ck["det"] or (ck["G"] and ck["good"]):
            viol.append(dict(det=[str(x) for x in ck["det"][:4]], good=[str(x) for x in ck["good"][:4]], G=ck["G"],
                             genome=dict(steps=cand["steps"].tolist(), d0=cand["d0"], s_in=cand["s_in"], strat=cand["strat"])))
        if val >= cur:
            if val > cur:
                stall = 0
            g, cur = cand, val
        else:
            stall += 1
        if val > best:
            best, bestg = val, cand
            hist.append((ev, round(best, 4)))
    out = dict(cell=CP.cell_tag(cell), objective=objective, evaluations=ev, seed=seed, best=best, violations=len(viol), viol=viol[:5],
               best_genome=dict(steps=[round(float(x), 4) for x in bestg["steps"]], d0=bestg["d0"], s_in=bestg["s_in"], strat=bestg["strat"]),
               history=hist, secs=round(time.time() - t0, 1), rdag=P.rdag, K=P.K)
    _os.makedirs(_os.path.join(HERE, "data"), exist_ok=True)
    with open(HERE + "/data/adversarial.jsonl", "a") as f:
        f.write(json.dumps(out) + "\n")
    print("cell", ci, objective, "evals", ev, "best", round(best, 4), "violations", len(viol), "time %.0fs" % (time.time() - t0), "history", hist[-4:])
