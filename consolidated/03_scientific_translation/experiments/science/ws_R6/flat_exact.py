"""
flat_exact.py -- workstream R6: the run of Algorithm 2L+ at the flat instance psi = 0 (deterministic), with the design of
K_REPORT 6.4 / ENG-RES-0008, the inner behaviour "bottom" ([W, W e^{x_l}]) and the costs C_l of the base brackets (Prop. K0).
My literal engine (r6lib.Run) is used unchanged: one class, exact block sizes, no sampling.  Output: ln(evaluations)/(n a),
to be compared with the column "flat instance at that phi" of ENG-RES-0008 (an implementation I have not read).
usage: python3 flat_exact.py <u> <n> <phi> [strategy: bottom|top|center]
"""
import sys, time, json
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__))
import numpy as np, mpmath as mp
import r6lib as R, instances as I, checks as C, everyn as EV

u, n, phi = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
strat = dict(bottom=R.S_BOTTOM, top=R.S_TOP, center=R.S_CENTER)[sys.argv[4] if len(sys.argv) > 4 else "bottom"]
t0 = time.time()
o, P0, xs, lnC = EV.two_level(n, u, phi, "K64")
costs = [mp.e ** c for c in lnC[1:]]
D = EV.DESIGNS["K64"]
P = R.Params2LP(n, P0.n_o, u, D["lam"], D["eta"], D["etap"], D["theta"], P0.nu1, D["b"], D["delta"], xs, costs, tables=P0.tab)
inst = I.radial(n, P.n_o, u, I.prof_flat(P.n_o, u), d0=0, s_in=0.0, strats=(strat,))
# one class only (all shells have the same value): merge
inst = R.ClassInstance(n, P.n_o, u, [0.0], [1], 0.0, [strat], 0, name="flat")
rng = np.random.default_rng(0)
run = R.Run(P, inst, R.SimOracle(P.xs, rng), rng).run()
st = [r["status"] for r in run.levels]
na = n * o["a"]
last = run.levels[-1]["passes"][-1]
res = dict(u=u, n=n, phi=phi, strat=sys.argv[4] if len(sys.argv) > 4 else "bottom", status=run.status, abort=run.abort_reason,
           cost_na=float(mp.log(run.queries())) / na, Cmax_na=o["Cmax_na"], hint_na=o["hint_na"], lnM_over_noa=float(mp.log(run.points_drawn)) / (P.n_o * o["a"]),
           close_r=int(last["r"]), rdag=P.rdag, pop=st.count("populated"), neg=st.count("negligible"), levels=len(st),
           width=float(run.result[1] - run.result[0]), x_out=float(P.x_out), secs=round(time.time() - t0, 1))
ck = C.check_2LP(run, extra_x=())
res.update(G=ck["G"], det=ck["det"][:3], good=ck["good"][:3], ratios=ck["ratios"])
print(json.dumps(res))
with open(HERE + "/data/flat_exact.jsonl", "a") as f:
    f.write(json.dumps(res) + "\n")
